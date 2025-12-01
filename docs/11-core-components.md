# Core Components

## Overview

Core components provide the infrastructure for all MCP tools.

| Component | File | Purpose |
|-----------|------|---------|
| Response | `core/response.py` | Unified response format |
| Client | `core/client.py` | HTTP client with smart retry |
| Cache | `core/cache.py` | Pluggable cache backends |
| Validation | `core/validation.py` | Plan gating and param validation |
| Errors | `core/errors.py` | Typed exceptions |
| Normalized | `models/normalized.py` | Data normalization models |

---

## Unified Response Format

All tools return the same response structure for consistency.

### `core/response.py`

```python
from dataclasses import dataclass
from typing import Any, Literal
from datetime import datetime

ResponseLevel = Literal["raw", "normalized", "summary"]

@dataclass
class MCPResponse:
    """Unified response contract for all tools."""
    success: bool
    action: str
    data: Any
    metadata: dict

    @classmethod
    def ok(
        cls,
        action: str,
        data: Any,
        *,
        level: ResponseLevel = "normalized",
        cached: bool = False,
        total_records: int | None = None,
        truncated: bool = False,
        symbol: str | None = None,
        exchange: str | None = None,
        interval: str | None = None,
        **extra_meta
    ) -> dict:
        """Success response."""
        metadata = {
            "level": level,
            "cached": cached,
            "timestamp": datetime.utcnow().isoformat(),
            **{k: v for k, v in {
                "total_records": total_records,
                "truncated": truncated,
                "symbol": symbol,
                "exchange": exchange,
                "interval": interval,
            }.items() if v is not None},
            **extra_meta
        }

        return {
            "success": True,
            "action": action,
            "data": data,
            "metadata": metadata
        }

    @classmethod
    def error(
        cls,
        action: str,
        error_type: str,
        message: str,
        *,
        hint: str | None = None,
        required_plan: str | None = None,
        current_plan: str | None = None,
        missing_params: list[str] | None = None
    ) -> dict:
        """Error response."""
        error_data = {
            "error": error_type,
            "message": message,
        }

        if hint:
            error_data["hint"] = hint
        if required_plan:
            error_data["required_plan"] = required_plan
            error_data["current_plan"] = current_plan
        if missing_params:
            error_data["missing_params"] = missing_params

        return {
            "success": False,
            "action": action,
            **error_data
        }
```

### Response Examples

**Success:**
```json
{
  "success": true,
  "action": "aggregated",
  "data": [...],
  "metadata": {
    "level": "normalized",
    "cached": false,
    "timestamp": "2025-12-01T12:00:00Z",
    "total_records": 500,
    "symbol": "BTC",
    "interval": "h4"
  }
}
```

**Error:**
```json
{
  "success": false,
  "action": "pair",
  "error": "ValidationError",
  "message": "Missing required parameters",
  "missing_params": ["exchange", "pair"],
  "hint": "Action 'pair' requires: exchange, pair, interval"
}
```

---

## HTTP Client with Smart Retry

### `core/client.py`

```python
import httpx
from dataclasses import dataclass
from tenacity import (
    retry, stop_after_attempt, wait_exponential,
    retry_if_exception
)

def is_retryable(exc: BaseException) -> bool:
    """Retry only 5xx and network errors."""
    if isinstance(exc, httpx.TimeoutException):
        return True
    if isinstance(exc, httpx.ConnectError):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        return 500 <= exc.response.status_code < 600
    return False

@dataclass
class CoinGlassClient:
    http_client: httpx.AsyncClient
    api_key: str
    base_url: str = "https://open-api-v4.coinglass.com"

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception(is_retryable)
    )
    async def request(
        self,
        endpoint: str,
        params: dict | None = None,
        trace_id: str | None = None
    ) -> dict:
        """Make authenticated request."""
        headers = {
            "CG-API-KEY": self.api_key,
            "Accept": "application/json"
        }
        if trace_id:
            headers["X-Trace-ID"] = trace_id

        response = await self.http_client.get(
            f"{self.base_url}{endpoint}",
            params=params,
            headers=headers,
            timeout=30.0
        )

        # Extract rate limit info
        rate_info = {
            "limit": response.headers.get("API-KEY-MAX-LIMIT"),
            "used": response.headers.get("API-KEY-USE-LIMIT"),
        }

        # Handle specific errors without retry
        if response.status_code == 429:
            raise RateLimitError(
                f"Rate limit exceeded: {rate_info['used']}/{rate_info['limit']}"
            )
        if response.status_code == 401:
            raise AuthError("Invalid API key")
        if response.status_code == 403:
            raise PlanLimitError("Feature requires higher plan")

        response.raise_for_status()

        data = response.json()

        if data.get("code") != "0":
            raise APIError(f"API error: {data.get('msg')}")

        return {
            "data": data.get("data"),
            "rate_info": rate_info
        }
```

### Retry Policy

| Error Type | Retry | Max Attempts |
|------------|-------|--------------|
| 5xx Server Error | Yes | 3 |
| Timeout | Yes | 3 |
| Connection Error | Yes | 3 |
| 429 Rate Limit | No | - |
| 401 Auth Error | No | - |
| 403 Plan Limit | No | - |
| 4xx Client Error | No | - |

---

## Pluggable Cache

### `core/cache.py`

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Protocol
import hashlib
import json

class CacheBackend(Protocol):
    """Cache backend interface."""

    async def get(self, key: str) -> Any | None: ...
    async def set(self, key: str, value: Any, ttl: timedelta) -> None: ...
    async def delete(self, key: str) -> None: ...
    async def clear(self) -> None: ...

@dataclass
class MemoryCache:
    """In-memory cache implementation."""

    _store: dict[str, tuple[Any, datetime]] = field(default_factory=dict)

    async def get(self, key: str) -> Any | None:
        entry = self._store.get(key)
        if entry is None:
            return None
        value, expires_at = entry
        if datetime.utcnow() > expires_at:
            del self._store[key]
            return None
        return value

    async def set(self, key: str, value: Any, ttl: timedelta) -> None:
        self._store[key] = (value, datetime.utcnow() + ttl)

    async def delete(self, key: str) -> None:
        self._store.pop(key, None)

    async def clear(self) -> None:
        self._store.clear()

@dataclass
class NullCache:
    """No-op cache (disabled)."""

    async def get(self, key: str) -> Any | None:
        return None

    async def set(self, key: str, value: Any, ttl: timedelta) -> None:
        pass

    async def delete(self, key: str) -> None:
        pass

    async def clear(self) -> None:
        pass
```

### TTL Configuration

```python
ENDPOINT_TTL = {
    # Static data - rarely changes
    "/api/futures/supported-coins": timedelta(minutes=30),
    "/api/futures/supported-exchange-pairs": timedelta(minutes=30),

    # Market summaries - frequent updates
    "/api/futures/coins-markets": timedelta(seconds=15),
    "/api/futures/pairs-markets": timedelta(seconds=15),
    "/api/futures/price-change-list": timedelta(seconds=10),

    # Historical OHLC - can cache longer
    "/api/price/ohlc-history": timedelta(minutes=2),
    "/api/futures/openInterest/ohlc-history": timedelta(minutes=2),
    "/api/futures/fundingRate/ohlc-history": timedelta(minutes=2),

    # Real-time data - minimal TTL
    "/api/futures/liquidation/order": timedelta(seconds=3),
    "/api/futures/orderbook/large-limit-order": timedelta(seconds=5),
    "/api/hyperliquid/whale-alert": timedelta(seconds=5),

    # Indicators - medium TTL
    "/api/index/fear-greed-history": timedelta(minutes=5),
    "/api/index/whale-index": timedelta(minutes=1),

    # Default
    "_default": timedelta(minutes=1),
}

def get_ttl(endpoint: str) -> timedelta:
    """Get TTL for endpoint."""
    return ENDPOINT_TTL.get(endpoint, ENDPOINT_TTL["_default"])

def make_cache_key(endpoint: str, params: dict | None) -> str:
    """Generate cache key."""
    param_str = json.dumps(params or {}, sort_keys=True)
    return hashlib.md5(f"{endpoint}:{param_str}".encode()).hexdigest()
```

---

## Plan Gating and Validation

### `core/validation.py`

```python
from dataclasses import dataclass
from typing import Literal

Plan = Literal["hobbyist", "startup", "standard", "professional", "enterprise"]

# Minimum plan for actions
ACTION_REQUIRED_PLAN: dict[str, Plan] = {
    # Liquidation
    "orders": "standard",
    "pair_heatmap": "professional",
    "coin_heatmap": "professional",
    "pair_map": "professional",
    "coin_map": "professional",

    # Whale
    "alerts": "startup",
    "positions": "startup",
    "all_positions": "startup",
}

# Minimum intervals by plan
PLAN_MIN_INTERVALS: dict[Plan, set[str]] = {
    "hobbyist": {"h4", "h8", "h12", "d1", "w1"},
    "startup": {"m30", "h1", "h4", "h8", "h12", "d1", "w1"},
    "standard": {"m1", "m5", "m15", "m30", "h1", "h4", "h8", "h12", "d1", "w1"},
    "professional": {"m1", "m5", "m15", "m30", "h1", "h4", "h8", "h12", "d1", "w1"},
    "enterprise": {"m1", "m5", "m15", "m30", "h1", "h4", "h8", "h12", "d1", "w1"},
}

PLAN_HIERARCHY: dict[Plan, int] = {
    "hobbyist": 0,
    "startup": 1,
    "standard": 2,
    "professional": 3,
    "enterprise": 4,
}

def check_plan_access(action: str, current_plan: Plan) -> tuple[bool, Plan | None]:
    """Check if action is available for plan."""
    required = ACTION_REQUIRED_PLAN.get(action)
    if required is None:
        return True, None

    if PLAN_HIERARCHY[current_plan] >= PLAN_HIERARCHY[required]:
        return True, None

    return False, required

def check_interval_access(interval: str, current_plan: Plan) -> tuple[bool, str | None]:
    """Check if interval is available for plan."""
    allowed = PLAN_MIN_INTERVALS[current_plan]
    if interval in allowed:
        return True, None

    # Find minimum required plan
    for plan in ["startup", "standard", "professional"]:
        if interval in PLAN_MIN_INTERVALS[plan]:
            return False, plan

    return False, "standard"
```

### Parameter Requirements

```python
@dataclass
class ParamRequirement:
    """Required parameters for an action."""
    required: list[str]
    optional: list[str] = None

    def validate(self, params: dict) -> list[str]:
        """Return list of missing required params."""
        return [p for p in self.required if not params.get(p)]

ACTION_PARAMS: dict[str, ParamRequirement] = {
    # OI History
    "pair": ParamRequirement(["exchange", "pair", "interval"]),
    "aggregated": ParamRequirement(["symbol", "interval"]),
    "stablecoin": ParamRequirement(["symbol", "interval"]),
    "coin_margin": ParamRequirement(["symbol", "interval"]),

    # OI Distribution
    "by_exchange": ParamRequirement(["symbol"]),
    "exchange_chart": ParamRequirement(["symbol", "range"]),

    # Funding
    "oi_weighted": ParamRequirement(["symbol", "interval"]),
    "vol_weighted": ParamRequirement(["symbol", "interval"]),

    # Long/Short
    "global": ParamRequirement(["exchange", "pair", "interval"]),
    "top_accounts": ParamRequirement(["exchange", "pair", "interval"]),
    "top_positions": ParamRequirement(["exchange", "pair", "interval"]),
    "taker_ratio": ParamRequirement(["symbol"]),

    # Price history
    "price_history": ParamRequirement(["exchange", "pair", "interval"]),
}
```

---

## Data Normalization

### `models/normalized.py`

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal

class OHLCCandle(BaseModel):
    """Normalized OHLC candle."""
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float

    @classmethod
    def from_raw(cls, raw: dict) -> "OHLCCandle":
        """Parse from CoinGlass raw format."""
        return cls(
            timestamp=datetime.fromtimestamp(raw["t"] / 1000),
            open=float(raw["o"]),
            high=float(raw["h"]),
            low=float(raw["l"]),
            close=float(raw["c"]),
        )

class OICandle(OHLCCandle):
    """Open Interest OHLC with unit."""
    unit: Literal["USD", "contracts"] = "USD"

class FundingCandle(OHLCCandle):
    """Funding rate OHLC (values are percentages)."""
    pass

class LiquidationSummary(BaseModel):
    """Aggregated liquidation data."""
    timestamp: datetime
    long_usd: float
    short_usd: float
    total_usd: float
    long_count: int = 0
    short_count: int = 0

    @classmethod
    def from_raw(cls, raw: dict) -> "LiquidationSummary":
        return cls(
            timestamp=datetime.fromtimestamp(raw["t"] / 1000),
            long_usd=float(raw.get("longLiquidationUsd", 0)),
            short_usd=float(raw.get("shortLiquidationUsd", 0)),
            total_usd=float(raw.get("liquidationUsd", 0)),
            long_count=int(raw.get("longCount", 0)),
            short_count=int(raw.get("shortCount", 0)),
        )

class LongShortRatio(BaseModel):
    """Long/short ratio data point."""
    timestamp: datetime
    long_ratio: float = Field(ge=0, le=100)
    short_ratio: float = Field(ge=0, le=100)
    ratio: float

    @classmethod
    def from_raw(cls, raw: dict) -> "LongShortRatio":
        long_pct = float(raw.get("longRate", raw.get("longAccount", 50)))
        short_pct = float(raw.get("shortRate", raw.get("shortAccount", 50)))
        return cls(
            timestamp=datetime.fromtimestamp(raw["t"] / 1000),
            long_ratio=long_pct,
            short_ratio=short_pct,
            ratio=long_pct / short_pct if short_pct > 0 else 0,
        )
```

### Normalization Helpers

```python
def normalize_ohlc_list(raw_list: list[dict], model_cls=OHLCCandle) -> list[dict]:
    """Normalize list of OHLC candles."""
    return [model_cls.from_raw(item).model_dump() for item in raw_list]

def normalize_liquidations(raw_list: list[dict]) -> list[dict]:
    """Normalize liquidation data."""
    return [LiquidationSummary.from_raw(item).model_dump() for item in raw_list]

def normalize_long_short(raw_list: list[dict]) -> list[dict]:
    """Normalize long/short ratio data."""
    return [LongShortRatio.from_raw(item).model_dump() for item in raw_list]
```
