# Tools: Derivatives (OI, Funding, Long/Short)

## Overview

Derivatives tools provide access to futures market analytics.

| Tool | Description |
|------|-------------|
| `coinglass_oi_history` | Open Interest OHLC history |
| `coinglass_oi_distribution` | OI breakdown by exchange |
| `coinglass_funding_history` | Funding rate OHLC history |
| `coinglass_funding_current` | Current rates and arbitrage |
| `coinglass_long_short` | Long/Short ratio data |

---

## coinglass_oi_history

Get Open Interest OHLC history.

### Actions

| Action | Description | Endpoint | Required Params |
|--------|-------------|----------|-----------------|
| `pair` | Single pair OI | `/api/futures/openInterest/ohlc-history` | exchange, pair |
| `aggregated` | All exchanges | `/api/futures/openInterest/ohlc-aggregated-history` | symbol |
| `stablecoin` | USDT-margined | `/api/futures/openInterest/ohlc-aggregated-stablecoin` | symbol |
| `coin_margin` | Coin-margined | `/api/futures/openInterest/ohlc-aggregated-coin-margin-history` | symbol |

### Parameters

```python
ActionOIHistory = Literal["pair", "aggregated", "stablecoin", "coin_margin"]

@mcp.tool
async def coinglass_oi_history(
    action: Annotated[ActionOIHistory, Field(
        description="pair: single pair OI | aggregated: all exchanges | stablecoin: USDT-margined | coin_margin: coin-margined"
    )],
    symbol: Annotated[str | None, Field(description="Coin symbol for aggregated actions")] = None,
    exchange: Annotated[str | None, Field(description="Exchange for pair action")] = None,
    pair: Annotated[str | None, Field(description="Trading pair for pair action")] = None,
    interval: Annotated[str, Field(description="h1, h4, d1")] = "h4",
    limit: Annotated[int, Field(ge=1, le=4500)] = 500,
    ctx: Context
) -> dict:
```

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `action` | Literal | Yes | - | OI data type |
| `symbol` | str | Conditional | None | Coin for aggregated actions |
| `exchange` | str | Conditional | None | Exchange for pair action |
| `pair` | str | Conditional | None | Trading pair for pair action |
| `interval` | str | No | "h4" | Candle interval |
| `limit` | int | No | 500 | Number of candles |

### Examples

```python
# Aggregated BTC OI across all exchanges
coinglass_oi_history(action="aggregated", symbol="BTC", interval="h4")

# Specific pair OI on Binance
coinglass_oi_history(action="pair", exchange="Binance", pair="BTCUSDT", interval="h1")

# USDT-margined ETH OI
coinglass_oi_history(action="stablecoin", symbol="ETH", interval="d1")
```

### Response

```json
{
  "success": true,
  "action": "aggregated",
  "data": [
    {
      "timestamp": "2025-12-01T08:00:00Z",
      "open": 25000000000,
      "high": 25500000000,
      "low": 24800000000,
      "close": 25300000000
    }
  ],
  "metadata": {
    "level": "normalized",
    "symbol": "BTC",
    "interval": "h4",
    "total_records": 500
  }
}
```

### Cache TTL
2 minutes

---

## coinglass_oi_distribution

Get Open Interest distribution across exchanges.

### Actions

| Action | Description | Endpoint |
|--------|-------------|----------|
| `by_exchange` | Current OI breakdown | `/api/futures/openInterest/exchange-list` |
| `exchange_chart` | Historical by exchange | `/api/futures/openInterest/exchange-history-chart` |

### Parameters

```python
ActionOIDist = Literal["by_exchange", "exchange_chart"]

@mcp.tool
async def coinglass_oi_distribution(
    action: Annotated[ActionOIDist, Field(
        description="by_exchange: current OI breakdown | exchange_chart: historical by exchange"
    )],
    symbol: Annotated[str, Field(description="Coin symbol: BTC, ETH")],
    range: Annotated[str | None, Field(description="For exchange_chart: 4h, 12h, 24h, 3d")] = None,
    ctx: Context
) -> dict:
```

### Examples

```python
# Current BTC OI by exchange
coinglass_oi_distribution(action="by_exchange", symbol="BTC")

# Historical OI distribution over 24h
coinglass_oi_distribution(action="exchange_chart", symbol="BTC", range="24h")
```

### Response (by_exchange)

```json
{
  "success": true,
  "action": "by_exchange",
  "data": [
    {
      "exchange": "Binance",
      "open_interest_usd": 8500000000,
      "change_24h": 1.5,
      "share_pct": 34.0
    },
    {
      "exchange": "OKX",
      "open_interest_usd": 5200000000,
      "change_24h": -0.8,
      "share_pct": 20.8
    }
  ],
  "metadata": {
    "symbol": "BTC",
    "total_oi_usd": 25000000000
  }
}
```

---

## coinglass_funding_history

Get funding rate OHLC history.

### Actions

| Action | Description | Endpoint | Required Params |
|--------|-------------|----------|-----------------|
| `pair` | Single pair | `/api/futures/fundingRate/ohlc-history` | exchange, pair |
| `oi_weighted` | OI-weighted avg | `/api/futures/fundingRate/oi-weight-ohlc-history` | symbol |
| `vol_weighted` | Volume-weighted avg | `/api/futures/fundingRate/vol-weight-ohlc-history` | symbol |

### Parameters

```python
ActionFundingHistory = Literal["pair", "oi_weighted", "vol_weighted"]

@mcp.tool
async def coinglass_funding_history(
    action: Annotated[ActionFundingHistory, Field(
        description="pair: single pair | oi_weighted: OI-weighted avg | vol_weighted: volume-weighted avg"
    )],
    symbol: Annotated[str | None, Field(description="Coin for weighted actions")] = None,
    exchange: Annotated[str | None, Field(description="Exchange for pair action")] = None,
    pair: Annotated[str | None, Field(description="Trading pair for pair action")] = None,
    interval: Annotated[str, Field(description="h1, h4, h8, d1")] = "h8",
    limit: Annotated[int, Field(ge=1, le=4500)] = 500,
    ctx: Context
) -> dict:
```

### Examples

```python
# OI-weighted BTC funding rate
coinglass_funding_history(action="oi_weighted", symbol="BTC", interval="h8")

# Specific pair funding on Binance
coinglass_funding_history(action="pair", exchange="Binance", pair="BTCUSDT")
```

### Response

```json
{
  "success": true,
  "action": "oi_weighted",
  "data": [
    {
      "timestamp": "2025-12-01T08:00:00Z",
      "open": 0.0082,
      "high": 0.0095,
      "low": 0.0078,
      "close": 0.0085
    }
  ],
  "metadata": {
    "symbol": "BTC",
    "interval": "h8"
  }
}
```

---

## coinglass_funding_current

Get current funding rate data across exchanges.

### Actions

| Action | Description | Endpoint |
|--------|-------------|----------|
| `rates` | Current rates | `/api/futures/fundingRate/exchange-list` |
| `accumulated` | Cumulative funding | `/api/futures/fundingRate/accumulated-exchange-list` |
| `arbitrage` | Arb opportunities | `/api/futures/fundingRate/arbitrage` |

### Parameters

```python
ActionFundingCurrent = Literal["rates", "accumulated", "arbitrage"]

@mcp.tool
async def coinglass_funding_current(
    action: Annotated[ActionFundingCurrent, Field(
        description="rates: current rates | accumulated: cumulative | arbitrage: arb opportunities"
    )],
    symbol: Annotated[str | None, Field(description="Filter by coin")] = None,
    ctx: Context
) -> dict:
```

### Examples

```python
# All current funding rates
coinglass_funding_current(action="rates")

# BTC funding rates
coinglass_funding_current(action="rates", symbol="BTC")

# Arbitrage opportunities
coinglass_funding_current(action="arbitrage")
```

### Response (arbitrage)

```json
{
  "success": true,
  "action": "arbitrage",
  "data": [
    {
      "symbol": "BTC",
      "long_exchange": "Bybit",
      "short_exchange": "dYdX",
      "long_rate": 0.0045,
      "short_rate": 0.0125,
      "spread": 0.0080,
      "annual_yield_pct": 29.2
    }
  ],
  "metadata": {...}
}
```

---

## coinglass_long_short

Get long/short ratio data.

### Actions

| Action | Description | Endpoint |
|--------|-------------|----------|
| `global` | Global ratio | `/api/futures/globalLongShortAccountRatio/history` |
| `top_accounts` | Top traders accounts | `/api/futures/topLongShortAccountRatio/history` |
| `top_positions` | Top traders positions | `/api/futures/topLongShortPositionRatio/history` |
| `taker_ratio` | Taker buy/sell | `/api/futures/taker-buy-sell-volume/exchange-list` |

### Parameters

```python
ActionLS = Literal["global", "top_accounts", "top_positions", "taker_ratio"]

@mcp.tool
async def coinglass_long_short(
    action: Annotated[ActionLS, Field(
        description="global: global ratio | top_accounts: top traders accounts | top_positions: top traders positions | taker_ratio: taker buy/sell"
    )],
    exchange: Annotated[str, Field(description="Exchange: Binance, OKX, Bybit")],
    pair: Annotated[str, Field(description="Trading pair: BTCUSDT")],
    interval: Annotated[str, Field(description="m5, m15, m30, h1, h4, d1")] = "h4",
    limit: Annotated[int, Field(ge=1, le=4500)] = 500,
    ctx: Context
) -> dict:
```

**Note:** `taker_ratio` uses `symbol` instead of `pair`.

### Examples

```python
# Global L/S ratio for BTCUSDT on Binance
coinglass_long_short(action="global", exchange="Binance", pair="BTCUSDT")

# Top traders position ratio
coinglass_long_short(action="top_positions", exchange="Binance", pair="BTCUSDT")
```

### Response

```json
{
  "success": true,
  "action": "global",
  "data": [
    {
      "timestamp": "2025-12-01T08:00:00Z",
      "long_ratio": 52.5,
      "short_ratio": 47.5,
      "ratio": 1.105
    }
  ],
  "metadata": {
    "exchange": "Binance",
    "pair": "BTCUSDT",
    "interval": "h4"
  }
}
```
