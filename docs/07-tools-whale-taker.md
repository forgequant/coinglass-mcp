# Tools: Whale & Taker

## Overview

Whale and taker tools provide insights into large trader activity and market order flow.

| Tool | Description | Min Plan |
|------|-------------|----------|
| `coinglass_whale_positions` | Whale tracking on Hyperliquid | Startup |
| `coinglass_whale_index` | Whale Index history | Hobbyist |
| `coinglass_taker` | Taker buy/sell volume | Hobbyist |

---

## coinglass_whale_positions

Track whale activity on Hyperliquid.

### Plan Requirement
**Startup+ plan required**

### Actions

| Action | Description | Endpoint |
|--------|-------------|----------|
| `alerts` | Real-time whale alerts | `/api/hyperliquid/whale-alert` |
| `positions` | Positions >$1M | `/api/hyperliquid/whale-position` |
| `all_positions` | All Hyperliquid positions | `/api/hyperliquid/position` |

### Parameters

```python
ActionWhale = Literal["alerts", "positions", "all_positions"]

@mcp.tool
async def coinglass_whale_positions(
    action: Annotated[ActionWhale, Field(
        description="alerts: real-time whale alerts | positions: >$1M positions | all_positions: all Hyperliquid positions"
    )],
    symbol: Annotated[str | None, Field(description="Filter by coin")] = None,
    user: Annotated[str | None, Field(description="Wallet address filter")] = None,
    page: Annotated[int, Field(ge=1)] = 1,
    ctx: Context
) -> dict:
```

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `action` | Literal | Yes | - | Whale data type |
| `symbol` | str | No | None | Filter by coin |
| `user` | str | No | None | Filter by wallet address |
| `page` | int | No | 1 | Page number |

### Examples

```python
# Real-time whale alerts
coinglass_whale_positions(action="alerts")

# BTC whale positions
coinglass_whale_positions(action="positions", symbol="BTC")

# Track specific wallet
coinglass_whale_positions(action="all_positions", user="0x1234...")
```

### Response

```json
{
  "success": true,
  "action": "positions",
  "data": [
    {
      "user_address": "0x1234...abcd",
      "symbol": "BTC",
      "side": "long",
      "size": 15.5,
      "size_usd": 1512750,
      "entry_price": 96500.0,
      "mark_price": 97500.5,
      "liq_price": 85000.0,
      "leverage": 10,
      "unrealized_pnl": 15507.75,
      "pnl_pct": 1.025,
      "timestamp": "2025-12-01T11:00:00Z"
    }
  ],
  "metadata": {
    "symbol": "BTC",
    "total_records": 25,
    "page": 1
  }
}
```

### Cache TTL
- `alerts`: 5 seconds
- `positions`: 30 seconds
- `all_positions`: 30 seconds

---

## coinglass_whale_index

Get historical Whale Index values.

### Description
The Whale Index measures aggregate whale activity and sentiment. Higher values indicate increased whale activity.

### Parameters

```python
@mcp.tool
async def coinglass_whale_index(
    range: Annotated[str, Field(description="Time range: 24h, 7d, 30d")] = "7d",
    ctx: Context
) -> dict:
```

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `range` | str | No | "7d" | Time range |

### Valid Ranges

| Range | Description |
|-------|-------------|
| `24h` | Last 24 hours |
| `7d` | Last 7 days |
| `30d` | Last 30 days |

### Examples

```python
# 7-day whale index
coinglass_whale_index(range="7d")

# 30-day whale index
coinglass_whale_index(range="30d")
```

### Response

```json
{
  "success": true,
  "action": "whale_index",
  "data": [
    {
      "timestamp": "2025-12-01T00:00:00Z",
      "index_value": 72.5,
      "change_24h": 3.2
    },
    {
      "timestamp": "2025-11-30T00:00:00Z",
      "index_value": 69.3,
      "change_24h": -1.5
    }
  ],
  "metadata": {
    "range": "7d",
    "total_records": 7
  }
}
```

### Cache TTL
1 minute

---

## coinglass_taker

Get taker buy/sell volume data.

### Actions

| Action | Description | Endpoint |
|--------|-------------|----------|
| `pair_history` | Single pair | `/api/futures/taker-buy-sell-volume/history` |
| `coin_history` | Aggregated | `/api/futures/taker-buy-sell-volume/aggregated-history` |
| `by_exchange` | Ratio by exchange | `/api/futures/taker-buy-sell-volume/exchange-list` |

### Parameters

```python
ActionTaker = Literal["pair_history", "coin_history", "by_exchange"]

@mcp.tool
async def coinglass_taker(
    action: Annotated[ActionTaker, Field(
        description="pair_history: single pair | coin_history: aggregated | by_exchange: ratio by exchange"
    )],
    symbol: Annotated[str | None, Field(description="Coin for coin_history/by_exchange")] = None,
    exchange: Annotated[str | None, Field(description="Exchange for pair_history")] = None,
    pair: Annotated[str | None, Field(description="Trading pair for pair_history")] = None,
    interval: Annotated[str, Field(description="m5, m15, h1, h4, d1")] = "h1",
    market: Annotated[Literal["futures", "spot"], Field(description="Market type")] = "futures",
    limit: Annotated[int, Field(ge=1, le=4500)] = 500,
    ctx: Context
) -> dict:
```

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `action` | Literal | Yes | - | Taker data type |
| `symbol` | str | Conditional | None | Coin for aggregated |
| `exchange` | str | Conditional | None | Exchange for pair |
| `pair` | str | Conditional | None | Trading pair |
| `interval` | str | No | "h1" | Candle interval |
| `market` | Literal | No | "futures" | Market type |
| `limit` | int | No | 500 | Number of records |

### Examples

```python
# Aggregated BTC taker volume
coinglass_taker(action="coin_history", symbol="BTC", interval="h1")

# Specific pair taker volume
coinglass_taker(
    action="pair_history",
    exchange="Binance",
    pair="BTCUSDT",
    interval="m15"
)

# Taker ratio by exchange
coinglass_taker(action="by_exchange", symbol="BTC")

# Spot market taker volume
coinglass_taker(action="coin_history", symbol="ETH", market="spot")
```

### Response (coin_history)

```json
{
  "success": true,
  "action": "coin_history",
  "data": [
    {
      "timestamp": "2025-12-01T11:00:00Z",
      "buy_volume": 125000000,
      "sell_volume": 98000000,
      "buy_ratio": 0.561
    }
  ],
  "metadata": {
    "symbol": "BTC",
    "interval": "h1",
    "market": "futures"
  }
}
```

### Response (by_exchange)

```json
{
  "success": true,
  "action": "by_exchange",
  "data": [
    {
      "exchange": "Binance",
      "buy_volume": 85000000,
      "sell_volume": 72000000,
      "buy_ratio": 0.541,
      "share_pct": 35.2
    },
    {
      "exchange": "OKX",
      "buy_volume": 42000000,
      "sell_volume": 38000000,
      "buy_ratio": 0.525,
      "share_pct": 18.0
    }
  ],
  "metadata": {
    "symbol": "BTC"
  }
}
```

### Cache TTL
30 seconds

### Interpretation

| Buy Ratio | Signal |
|-----------|--------|
| > 0.55 | Strong buying pressure |
| 0.50 - 0.55 | Neutral to bullish |
| 0.45 - 0.50 | Neutral to bearish |
| < 0.45 | Strong selling pressure |
