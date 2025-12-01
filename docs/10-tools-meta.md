# Tools: Meta / Discovery

## Overview

Meta tools help discover available operations and understand server configuration.

| Tool | Description |
|------|-------------|
| `coinglass_search` | Discover operations |
| `coinglass_config` | Configuration metadata |

---

## coinglass_search

Search available CoinGlass operations.

### Description
Use this tool for discovery when unsure which tool to use. Returns matching tools, actions, and required parameters.

### Parameters

```python
@mcp.tool
async def coinglass_search(
    query: Annotated[str, Field(description="Search: 'liquidation BTC' or 'funding arbitrage'")],
    ctx: Context
) -> dict:
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | str | Yes | Search query |

### Search Patterns

| Query Type | Example | Matches |
|------------|---------|---------|
| By domain | `"liquidation"` | All liquidation tools |
| By feature | `"arbitrage"` | funding_current(arbitrage) |
| By symbol | `"BTC OI"` | OI tools for BTC |
| By action | `"heatmap"` | liq_heatmap, ob_history(heatmap) |

### Examples

```python
# Find liquidation-related operations
coinglass_search(query="liquidation")

# Find arbitrage opportunities
coinglass_search(query="funding arbitrage")

# Find whale tracking
coinglass_search(query="whale positions")

# Find historical data
coinglass_search(query="history OHLC")
```

### Response

```json
{
  "success": true,
  "action": "search",
  "data": {
    "query": "liquidation",
    "matches": [
      {
        "tool": "coinglass_liq_history",
        "description": "Get liquidation history data",
        "actions": ["pair", "aggregated", "by_coin", "by_exchange"],
        "relevance": 1.0
      },
      {
        "tool": "coinglass_liq_orders",
        "description": "Get real-time liquidation orders",
        "min_plan": "standard",
        "relevance": 0.9
      },
      {
        "tool": "coinglass_liq_heatmap",
        "description": "Get liquidation heatmap visualizations",
        "actions": ["pair_heatmap", "coin_heatmap", "pair_map", "coin_map"],
        "min_plan": "professional",
        "relevance": 0.8
      }
    ],
    "suggestions": [
      "Use coinglass_liq_history(action='aggregated', symbol='BTC') for BTC liquidations",
      "Use coinglass_liq_orders() for real-time liquidation feed (Standard+ plan)"
    ]
  },
  "metadata": {
    "total_matches": 3
  }
}
```

### Cache
Not cached (instant lookup)

---

## coinglass_config

Get CoinGlass configuration and metadata.

### Actions

| Action | Description |
|--------|-------------|
| `exchanges` | List supported exchanges |
| `intervals` | Available data intervals |
| `rate_limits` | Current API usage |
| `plan_features` | Plan capabilities |

### Parameters

```python
ActionConfig = Literal["exchanges", "intervals", "rate_limits", "plan_features"]

@mcp.tool
async def coinglass_config(
    action: Annotated[ActionConfig, Field(
        description="exchanges: list | intervals: available intervals | rate_limits: current usage | plan_features: plan capabilities"
    )],
    ctx: Context
) -> dict:
```

### Examples

```python
# List exchanges
coinglass_config(action="exchanges")

# Check rate limits
coinglass_config(action="rate_limits")

# Check plan features
coinglass_config(action="plan_features")
```

### Response (exchanges)

```json
{
  "success": true,
  "action": "exchanges",
  "data": {
    "futures": [
      "Binance", "OKX", "Bybit", "dYdX", "Bitget",
      "Huobi", "Gate", "CoinEx", "Kraken", "BingX"
    ],
    "spot": [
      "Binance", "OKX", "Coinbase", "Bybit", "Kraken",
      "Huobi", "Gate", "Bitfinex", "KuCoin"
    ],
    "options": [
      "Deribit", "OKX", "Binance", "Bybit"
    ]
  },
  "metadata": {...}
}
```

### Response (intervals)

```json
{
  "success": true,
  "action": "intervals",
  "data": {
    "all": ["m1", "m5", "m15", "m30", "h1", "h4", "h8", "h12", "d1", "w1"],
    "by_plan": {
      "hobbyist": ["h4", "h8", "h12", "d1", "w1"],
      "startup": ["m30", "h1", "h4", "h8", "h12", "d1", "w1"],
      "standard": ["m1", "m5", "m15", "m30", "h1", "h4", "h8", "h12", "d1", "w1"],
      "professional": ["m1", "m5", "m15", "m30", "h1", "h4", "h8", "h12", "d1", "w1"],
      "enterprise": ["m1", "m5", "m15", "m30", "h1", "h4", "h8", "h12", "d1", "w1"]
    },
    "descriptions": {
      "m1": "1 minute",
      "m5": "5 minutes",
      "m15": "15 minutes",
      "m30": "30 minutes",
      "h1": "1 hour",
      "h4": "4 hours",
      "h8": "8 hours (funding)",
      "h12": "12 hours",
      "d1": "1 day",
      "w1": "1 week"
    }
  },
  "metadata": {...}
}
```

### Response (rate_limits)

```json
{
  "success": true,
  "action": "rate_limits",
  "data": {
    "plan": "standard",
    "limit_per_minute": 300,
    "used_this_minute": 45,
    "remaining": 255,
    "reset_at": "2025-12-01T12:01:00Z"
  },
  "metadata": {...}
}
```

### Response (plan_features)

```json
{
  "success": true,
  "action": "plan_features",
  "data": {
    "current_plan": "standard",
    "features": {
      "liquidation_orders": true,
      "liquidation_heatmap": false,
      "liquidation_map": false,
      "whale_alerts": true,
      "whale_positions": true,
      "min_interval": "m1"
    },
    "upgrade_benefits": {
      "professional": [
        "Liquidation heatmaps (3 models)",
        "Liquidation leverage maps",
        "Higher rate limits (600/min)"
      ]
    }
  },
  "metadata": {...}
}
```

### Cache TTL
- `exchanges`: 30 minutes
- `intervals`: 30 minutes
- `rate_limits`: Not cached
- `plan_features`: 5 minutes

---

## Common Usage Patterns

### Discovery Flow

```python
# 1. Search for relevant operations
result = coinglass_search(query="funding rate")

# 2. Check plan capabilities
features = coinglass_config(action="plan_features")

# 3. Check available intervals
intervals = coinglass_config(action="intervals")

# 4. Execute the appropriate tool
data = coinglass_funding_history(action="oi_weighted", symbol="BTC")
```

### Error Handling

```python
# Check rate limits before batch operations
limits = coinglass_config(action="rate_limits")

if limits["data"]["remaining"] < 10:
    # Wait or reduce batch size
    pass
```

### Plan-Aware Usage

```python
# Check if feature is available
features = coinglass_config(action="plan_features")

if features["data"]["features"]["liquidation_heatmap"]:
    heatmap = coinglass_liq_heatmap(action="coin_heatmap", symbol="BTC")
else:
    # Fall back to basic liquidation history
    history = coinglass_liq_history(action="aggregated", symbol="BTC")
```
