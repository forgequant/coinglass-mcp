# Configuration & Deployment

## Requirements

### `requirements.txt`

```
fastmcp>=2.13.0
httpx>=0.25.0
pydantic>=2.0.0
tenacity>=8.2.0
python-dotenv>=1.0.0
```

### Python Version
Python 3.11+

---

## Environment Variables

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `COINGLASS_API_KEY` | CoinGlass API key | `abc123...` |

### Optional

| Variable | Description | Default |
|----------|-------------|---------|
| `COINGLASS_PLAN` | API plan level | `standard` |
| `CACHE_BACKEND` | Cache type | `memory` |
| `LOG_LEVEL` | Logging level | `INFO` |

### `.env` Example

```bash
# Required
COINGLASS_API_KEY=your_api_key_here

# Optional
COINGLASS_PLAN=standard
CACHE_BACKEND=memory
LOG_LEVEL=INFO
```

---

## Server Configuration

### `server.py`

```python
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
import os
import uuid
import httpx
from fastmcp import FastMCP, Context

from core.client import CoinGlassClient
from core.cache import MemoryCache, NullCache, CacheBackend
from core.validation import Plan

@dataclass
class AppContext:
    """Application context with shared resources."""
    client: CoinGlassClient
    cache: CacheBackend
    plan: Plan

    def new_trace_id(self) -> str:
        """Generate trace ID for request tracking."""
        return str(uuid.uuid4())[:8]

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Initialize and cleanup shared resources."""

    api_key = os.environ.get("COINGLASS_API_KEY")
    if not api_key:
        raise ValueError("COINGLASS_API_KEY environment variable required")

    plan: Plan = os.environ.get("COINGLASS_PLAN", "standard").lower()
    cache_backend = os.environ.get("CACHE_BACKEND", "memory").lower()

    # Select cache backend
    cache: CacheBackend
    if cache_backend == "none":
        cache = NullCache()
    else:
        cache = MemoryCache()

    async with httpx.AsyncClient() as http_client:
        client = CoinGlassClient(
            http_client=http_client,
            api_key=api_key
        )

        yield AppContext(
            client=client,
            cache=cache,
            plan=plan
        )

mcp = FastMCP(
    name="coinglass",
    instructions="""
    CoinGlass MCP provides crypto derivatives analytics: open interest, funding rates,
    liquidations, whale tracking, ETF flows, and market indicators.

    Use coinglass_search to discover operations.
    Common patterns:
    - Market overview: coinglass_market_data(action="coins_summary")
    - BTC open interest: coinglass_oi_history(action="aggregated", symbol="BTC")
    - Funding rates: coinglass_funding_current(action="rates")
    - Liquidations: coinglass_liq_history(action="aggregated", symbol="BTC")
    - Whale activity: coinglass_whale_positions(action="positions")
    """,
    lifespan=app_lifespan
)

# Import and register all tools
from tools import register_all_tools
register_all_tools(mcp)
```

---

## FastMCP Cloud Deployment

### Entry Point

```
server.py:mcp
```

### Cloud Configuration

```yaml
# fastmcp.yaml (if needed)
name: coinglass
version: 1.0.0
entry_point: server.py:mcp

environment:
  - COINGLASS_API_KEY
  - COINGLASS_PLAN
  - CACHE_BACKEND
```

---

## Local Development

### Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export COINGLASS_API_KEY=your_api_key
export COINGLASS_PLAN=standard

# Run server
python -m fastmcp dev server.py:mcp
```

### Testing

```bash
# Run unit tests
pytest tests/test_tools.py -v

# Run smoke tests (requires API key)
pytest tests/test_smoke.py -v --real-api
```

---

## Tool Registration

### `tools/__init__.py`

```python
from fastmcp import FastMCP

def register_all_tools(mcp: FastMCP) -> None:
    """Register all CoinGlass tools."""

    # Market
    from .market import (
        coinglass_market_info,
        coinglass_market_data,
        coinglass_price_history
    )

    # Derivatives
    from .open_interest import (
        coinglass_oi_history,
        coinglass_oi_distribution
    )
    from .funding import (
        coinglass_funding_history,
        coinglass_funding_current
    )
    from .long_short import coinglass_long_short

    # Liquidation & Order Book
    from .liquidation import (
        coinglass_liq_history,
        coinglass_liq_orders,
        coinglass_liq_heatmap
    )
    from .orderbook import (
        coinglass_ob_history,
        coinglass_ob_large_orders
    )

    # Whale & Taker
    from .whale import (
        coinglass_whale_positions,
        coinglass_whale_index
    )
    from .taker import coinglass_taker

    # Spot, Options, On-Chain
    from .spot import coinglass_spot
    from .options import coinglass_options
    from .onchain import coinglass_onchain

    # ETF & Indicators
    from .etf import coinglass_etf, coinglass_grayscale
    from .indicators import coinglass_indicators

    # Meta
    from .meta import coinglass_search, coinglass_config

    # All tools are registered via @mcp.tool decorator
```

---

## Health Check

The server can be health-checked via the `coinglass_config` tool:

```python
# Check API connectivity and rate limits
result = await coinglass_config(action="rate_limits")

if result["success"]:
    print(f"API OK: {result['data']['remaining']} requests remaining")
else:
    print(f"API Error: {result['message']}")
```

---

## Monitoring

### Logging

```python
import logging

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO"),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger("coinglass")
```

### Trace IDs

All requests include a trace ID for debugging:

```
[abc12345] Fetching aggregated OI from CoinGlass
[abc12345] Cache miss, making API request
[abc12345] Cached 500 records, TTL=120s
```

### Rate Limit Tracking

Rate limit info is available in response headers and via `coinglass_config(action="rate_limits")`.
