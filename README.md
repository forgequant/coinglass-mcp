# CoinGlass MCP Server

MCP server for [CoinGlass](https://www.coinglass.com) cryptocurrency derivatives analytics. Provides AI agents access to 80+ API endpoints covering open interest, funding rates, liquidations, whale tracking, ETF flows, and market indicators.

## Installation

```bash
pip install coinglass-mcp
```

Or with uv:

```bash
uv pip install coinglass-mcp
```

## Configuration

Set your CoinGlass API key:

```bash
export COINGLASS_API_KEY="your-api-key"
export COINGLASS_PLAN="standard"  # hobbyist, startup, standard, professional, enterprise
```

Get your API key at [coinglass.com/pricing](https://www.coinglass.com/pricing).

## Usage

### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "coinglass": {
      "command": "coinglass-mcp",
      "env": {
        "COINGLASS_API_KEY": "your-api-key",
        "COINGLASS_PLAN": "standard"
      }
    }
  }
}
```

### Standalone

```bash
coinglass-mcp
```

## Available Tools (22)

### Market Data
- `coinglass_market_info` - Supported coins, pairs, exchanges
- `coinglass_market_data` - Real-time market summaries
- `coinglass_price_history` - OHLC price candles

### Open Interest
- `coinglass_oi_history` - OI OHLC history (pair/aggregated/stablecoin/coin-margin)
- `coinglass_oi_distribution` - OI breakdown by exchange

### Funding Rates
- `coinglass_funding_history` - Funding rate OHLC
- `coinglass_funding_current` - Current rates, accumulated, arbitrage

### Long/Short Ratio
- `coinglass_long_short` - Global ratio, top accounts, top positions

### Liquidations
- `coinglass_liq_history` - Liquidation OHLC history
- `coinglass_liq_orders` - Real-time liquidation stream (Standard+)
- `coinglass_liq_heatmap` - Liquidation heatmaps (Professional+)

### Order Book
- `coinglass_ob_history` - Bid/ask depth history
- `coinglass_ob_large_orders` - Whale walls detection

### Whale Tracking
- `coinglass_whale_positions` - Hyperliquid whale positions (Startup+)
- `coinglass_whale_index` - Whale activity index

### Taker Volume
- `coinglass_taker` - Taker buy/sell volume and ratio

### Spot Market
- `coinglass_spot` - Spot market data and prices

### Options
- `coinglass_options` - Max pain, OI, volume (BTC/ETH)

### On-Chain
- `coinglass_onchain` - Exchange balances, flows, transfers

### ETF
- `coinglass_etf` - Bitcoin/Ethereum ETF flows and data
- `coinglass_grayscale` - Grayscale holdings and premium

### Indicators
- `coinglass_indicators` - RSI, Fear & Greed, Rainbow, Pi Cycle, etc.

### Meta
- `coinglass_search` - Discover tools by keyword
- `coinglass_config` - View available exchanges, intervals, features

## Plan Features

| Feature | Hobbyist | Startup | Standard | Professional |
|---------|----------|---------|----------|--------------|
| Basic intervals (h4, h8, d1) | Yes | Yes | Yes | Yes |
| Extended intervals (m1-h1) | - | Yes | Yes | Yes |
| Whale alerts/positions | - | Yes | Yes | Yes |
| Liquidation orders | - | - | Yes | Yes |
| Liquidation heatmaps | - | - | - | Yes |

## Examples

```python
# Get BTC open interest across all exchanges
coinglass_oi_history(action="aggregated", symbol="BTC")

# Check current funding rates
coinglass_funding_current(action="rates")

# Find funding arbitrage opportunities
coinglass_funding_current(action="arbitrage")

# Track whale positions on Hyperliquid
coinglass_whale_positions(action="positions", symbol="BTC")

# Get Fear & Greed index
coinglass_indicators(action="fear_greed")

# Search for available tools
coinglass_search(query="liquidation")
```

## Development

```bash
# Clone and install
git clone https://github.com/your-org/coinglass-mcp.git
cd coinglass-mcp
uv pip install -e ".[dev]"

# Run tests
pytest

# Run server locally
python -m coinglass_mcp.server
```

## License

MIT
