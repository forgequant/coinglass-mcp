# Tools: ETF & Indicators

## Overview

ETF and indicator tools provide access to crypto ETF data and market metrics.

| Tool | Description |
|------|-------------|
| `coinglass_etf` | Crypto ETF data (Bitcoin/Ethereum) |
| `coinglass_grayscale` | Grayscale fund data |
| `coinglass_indicators` | Market indicators and metrics |

---

## coinglass_etf

Get crypto ETF data.

### Actions

| Action | Description | Endpoint | Required Params |
|--------|-------------|----------|-----------------|
| `list` | All ETFs | `/api/etf/{asset}/list` | - |
| `flows` | Daily flows | `/api/etf/{asset}/flows` | - |
| `net_assets` | AUM history | `/api/etf/{asset}/net-assets` | - |
| `premium` | Premium/discount | `/api/etf/{asset}/premium-discount` | ticker |
| `detail` | ETF info | `/api/etf/{asset}/detail` | ticker |
| `price` | OHLC price | `/api/etf/{asset}/price` | ticker |

### Parameters

```python
ActionETF = Literal["list", "flows", "net_assets", "premium", "detail", "price"]

@mcp.tool
async def coinglass_etf(
    action: Annotated[ActionETF, Field(
        description="list: all ETFs | flows: daily flows | net_assets: AUM history | premium: premium/discount | detail: ETF info | price: OHLC"
    )],
    asset: Annotated[Literal["bitcoin", "ethereum"], Field(description="BTC or ETH ETFs")] = "bitcoin",
    ticker: Annotated[str | None, Field(description="ETF ticker: IBIT, GBTC, ETHE")] = None,
    region: Annotated[Literal["us", "hk"] | None, Field(description="US or Hong Kong")] = "us",
    interval: Annotated[str | None, Field(description="For price: h1, d1")] = None,
    limit: Annotated[int, Field(ge=1, le=500)] = 100,
    ctx: Context
) -> dict:
```

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `action` | Literal | Yes | - | ETF data type |
| `asset` | Literal | No | "bitcoin" | Bitcoin or Ethereum |
| `ticker` | str | Conditional | None | Required for premium/detail/price |
| `region` | Literal | No | "us" | US or Hong Kong |
| `interval` | str | No | None | For price action |
| `limit` | int | No | 100 | Number of records |

### Examples

```python
# List all Bitcoin ETFs
coinglass_etf(action="list", asset="bitcoin")

# Daily ETF flows
coinglass_etf(action="flows", asset="bitcoin")

# IBIT premium/discount
coinglass_etf(action="premium", asset="bitcoin", ticker="IBIT")

# ETH ETF details
coinglass_etf(action="detail", asset="ethereum", ticker="ETHE")
```

### Response (list)

```json
{
  "success": true,
  "action": "list",
  "data": [
    {
      "ticker": "IBIT",
      "name": "iShares Bitcoin Trust",
      "issuer": "BlackRock",
      "aum_usd": 45000000000,
      "holdings_btc": 461538,
      "expense_ratio": 0.25,
      "inception_date": "2024-01-11"
    }
  ],
  "metadata": {
    "asset": "bitcoin",
    "region": "us"
  }
}
```

### Response (flows)

```json
{
  "success": true,
  "action": "flows",
  "data": [
    {
      "date": "2025-12-01",
      "total_flow_usd": 485000000,
      "etfs": [
        {
          "ticker": "IBIT",
          "flow_usd": 320000000
        },
        {
          "ticker": "FBTC",
          "flow_usd": 125000000
        },
        {
          "ticker": "GBTC",
          "flow_usd": -85000000
        }
      ]
    }
  ],
  "metadata": {...}
}
```

### Response (premium)

```json
{
  "success": true,
  "action": "premium",
  "data": [
    {
      "timestamp": "2025-12-01T00:00:00Z",
      "nav": 97.50,
      "market_price": 97.85,
      "premium_pct": 0.36
    }
  ],
  "metadata": {
    "ticker": "IBIT",
    "asset": "bitcoin"
  }
}
```

### Cache TTL
5 minutes

---

## coinglass_grayscale

Get Grayscale fund data.

### Actions

| Action | Description | Endpoint |
|--------|-------------|----------|
| `holdings` | Current holdings | `/api/grayscale/holdings` |
| `premium` | Premium history | `/api/grayscale/premium` |

### Parameters

```python
ActionGrayscale = Literal["holdings", "premium"]

@mcp.tool
async def coinglass_grayscale(
    action: Annotated[ActionGrayscale, Field(
        description="holdings: current holdings | premium: premium history"
    )],
    fund: Annotated[str | None, Field(description="Fund: GBTC, ETHE, etc")] = None,
    range: Annotated[str | None, Field(description="For premium: 30d, 90d, 1y")] = None,
    ctx: Context
) -> dict:
```

### Examples

```python
# All Grayscale holdings
coinglass_grayscale(action="holdings")

# GBTC premium history
coinglass_grayscale(action="premium", fund="GBTC", range="90d")
```

### Response (holdings)

```json
{
  "success": true,
  "action": "holdings",
  "data": [
    {
      "fund": "GBTC",
      "asset": "BTC",
      "shares_outstanding": 348000000,
      "holdings": 195000,
      "holdings_usd": 19012500000,
      "nav_per_share": 54.63,
      "market_price": 52.15,
      "premium_pct": -4.54
    }
  ],
  "metadata": {...}
}
```

### Cache TTL
10 minutes

---

## coinglass_indicators

Get market indicators and on-chain metrics.

### Actions

| Action | Description | Symbol Required |
|--------|-------------|-----------------|
| `rsi` | RSI for all coins | No |
| `basis` | Futures basis | Yes |
| `coinbase_premium` | Coinbase premium | No (BTC only) |
| `fear_greed` | Fear & Greed index | No (BTC only) |
| `ahr999` | AHR999 indicator | No (BTC only) |
| `puell` | Puell Multiple | No (BTC only) |
| `stock_flow` | Stock-to-Flow | No (BTC only) |
| `pi_cycle` | Pi Cycle Top | No (BTC only) |
| `rainbow` | Rainbow chart | No (BTC only) |
| `bubble` | Bubble index | No (BTC only) |
| `ma_2year` | 2-Year MA | No (BTC only) |
| `ma_200week` | 200-Week MA | No (BTC only) |
| `profitable_days` | Profitable days | No (BTC only) |
| `stablecoin_mcap` | Stablecoin mcap | No |
| `bull_peak` | Bull peak signals | No (BTC only) |
| `borrow_rate` | Exchange borrow rates | Yes + exchange |

### Parameters

```python
ActionIndicators = Literal[
    "rsi", "basis", "coinbase_premium", "fear_greed",
    "ahr999", "puell", "stock_flow", "pi_cycle", "rainbow",
    "bubble", "ma_2year", "ma_200week", "profitable_days",
    "stablecoin_mcap", "bull_peak", "borrow_rate"
]

@mcp.tool
async def coinglass_indicators(
    action: Annotated[ActionIndicators, Field(
        description="Market indicator to retrieve"
    )],
    symbol: Annotated[str | None, Field(description="Coin for rsi/basis/borrow_rate")] = None,
    exchange: Annotated[str | None, Field(description="Exchange for borrow_rate")] = None,
    interval: Annotated[str | None, Field(description="For basis: h1, h4, d1")] = None,
    range: Annotated[str | None, Field(description="Time range for historical")] = None,
    limit: Annotated[int, Field(ge=1, le=1000)] = 500,
    ctx: Context
) -> dict:
```

### Examples

```python
# Fear & Greed index
coinglass_indicators(action="fear_greed")

# RSI for all coins
coinglass_indicators(action="rsi")

# BTC basis
coinglass_indicators(action="basis", symbol="BTC", interval="h4")

# Borrow rate
coinglass_indicators(action="borrow_rate", symbol="BTC", exchange="Binance")

# Rainbow chart
coinglass_indicators(action="rainbow", range="1y")
```

### Response (fear_greed)

```json
{
  "success": true,
  "action": "fear_greed",
  "data": [
    {
      "timestamp": "2025-12-01T00:00:00Z",
      "value": 72,
      "classification": "Greed"
    }
  ],
  "metadata": {...}
}
```

### Response (rsi)

```json
{
  "success": true,
  "action": "rsi",
  "data": [
    {
      "symbol": "BTC",
      "rsi_1h": 55.2,
      "rsi_4h": 62.8,
      "rsi_1d": 58.5
    },
    {
      "symbol": "ETH",
      "rsi_1h": 48.7,
      "rsi_4h": 51.2,
      "rsi_1d": 54.3
    }
  ],
  "metadata": {...}
}
```

### Response (rainbow)

```json
{
  "success": true,
  "action": "rainbow",
  "data": [
    {
      "timestamp": "2025-12-01T00:00:00Z",
      "price": 97500.5,
      "band": "Is this a bubble?",
      "band_index": 7
    }
  ],
  "metadata": {
    "bands": [
      "Maximum bubble",
      "Sell. Seriously.",
      "FOMO intensifies",
      "Is this a bubble?",
      "HODL!",
      "Still cheap",
      "Accumulate",
      "BUY!",
      "Fire sale"
    ]
  }
}
```

### Fear & Greed Classifications

| Value | Classification |
|-------|----------------|
| 0-24 | Extreme Fear |
| 25-44 | Fear |
| 45-55 | Neutral |
| 56-75 | Greed |
| 76-100 | Extreme Greed |

### Cache TTL
- Real-time (rsi): 1 minute
- Daily indicators: 5 minutes
- Historical: 10 minutes
