# CoinGlass MCP Server

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastMCP](https://img.shields.io/badge/FastMCP-2.3+-green.svg)](https://github.com/jlowin/fastmcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Tests](https://img.shields.io/badge/tests-45%20passed-brightgreen.svg)](#testing)

> MCP server for [CoinGlass](https://www.coinglass.com) cryptocurrency derivatives analytics. Provides AI agents access to **80+ API endpoints** through **22 unified tools**.

---

## Features

- **22 MCP Tools** — Unified interface to 80+ CoinGlass API endpoints
- **Plan-Aware Gating** — Automatic feature restrictions based on subscription tier
- **Response Caching** — Built-in caching via FastMCP middleware (60s TTL)
- **Retry Logic** — Automatic retries for transient failures (5xx, timeouts)
- **Type-Safe** — Full type hints with Literal-typed actions for LLM clarity
- **Async-First** — Built on httpx + FastMCP for high performance

---

## Quick Start

### Installation

```bash
pip install coinglass-mcp
```

Or with [uv](https://github.com/astral-sh/uv):

```bash
uv pip install coinglass-mcp
```

### Configuration

```bash
export COINGLASS_API_KEY="your-api-key"
export COINGLASS_PLAN="standard"  # hobbyist | startup | standard | professional | enterprise
```

> Get your API key at [coinglass.com/pricing](https://www.coinglass.com/pricing)

### Run

```bash
coinglass-mcp
```

---

## Claude Desktop Integration

Add to your `claude_desktop_config.json`:

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

---

## Available Tools

| Category | Tool | Description |
|----------|------|-------------|
| **Market** | `coinglass_market_info` | Supported coins, pairs, exchanges |
| | `coinglass_market_data` | Real-time market summaries |
| | `coinglass_price_history` | OHLC price candles |
| **Open Interest** | `coinglass_oi_history` | OI OHLC (pair/aggregated/stablecoin/coin-margin) |
| | `coinglass_oi_distribution` | OI breakdown by exchange |
| **Funding** | `coinglass_funding_history` | Funding rate OHLC |
| | `coinglass_funding_current` | Current rates, accumulated, arbitrage |
| **Long/Short** | `coinglass_long_short` | Global ratio, top accounts, top positions |
| **Liquidation** | `coinglass_liq_history` | Liquidation OHLC history |
| | `coinglass_liq_orders` | Real-time liquidation stream ⚡ |
| | `coinglass_liq_heatmap` | Liquidation heatmaps 🔥 |
| **Order Book** | `coinglass_ob_history` | Bid/ask depth history |
| | `coinglass_ob_large_orders` | Whale walls detection |
| **Whale** | `coinglass_whale_positions` | Hyperliquid whale positions ⚡ |
| | `coinglass_whale_index` | Whale activity index |
| **Taker** | `coinglass_taker` | Taker buy/sell volume and ratio |
| **Spot** | `coinglass_spot` | Spot market data and prices |
| **Options** | `coinglass_options` | Max pain, OI, volume (BTC/ETH) |
| **On-Chain** | `coinglass_onchain` | Exchange balances, flows, transfers |
| **ETF** | `coinglass_etf` | Bitcoin/Ethereum ETF flows |
| | `coinglass_grayscale` | Grayscale holdings and premium |
| **Indicators** | `coinglass_indicators` | RSI, Fear & Greed, Rainbow, Pi Cycle, etc. |
| **Meta** | `coinglass_search` | Discover tools by keyword |
| | `coinglass_config` | View exchanges, intervals, features |

> ⚡ Requires Startup+ plan | 🔥 Requires Professional+ plan

---

## Plan Features

| Feature | Hobbyist | Startup | Standard | Professional |
|---------|:--------:|:-------:|:--------:|:------------:|
| Basic intervals (h4, h8, d1) | ✅ | ✅ | ✅ | ✅ |
| Extended intervals (m1-h1) | ❌ | ✅ | ✅ | ✅ |
| Whale alerts & positions | ❌ | ✅ | ✅ | ✅ |
| Liquidation orders stream | ❌ | ❌ | ✅ | ✅ |
| Liquidation heatmaps | ❌ | ❌ | ❌ | ✅ |

---

## Usage Examples

### Market Overview

```python
# Get all coins summary
coinglass_market_data(action="coins_summary")

# Get BTC metrics only
coinglass_market_data(action="coins_summary", symbol="BTC")
```

### Open Interest Analysis

```python
# BTC OI across all exchanges
coinglass_oi_history(action="aggregated", symbol="BTC")

# OI distribution by exchange
coinglass_oi_distribution(action="by_exchange", symbol="BTC")
```

### Funding Rate Arbitrage

```python
# Current funding rates
coinglass_funding_current(action="rates")

# Find arbitrage opportunities
coinglass_funding_current(action="arbitrage")
```

### Whale Tracking

```python
# Recent whale alerts (Hyperliquid)
coinglass_whale_positions(action="alerts")

# Large BTC positions
coinglass_whale_positions(action="positions", symbol="BTC")
```

### Market Sentiment

```python
# Fear & Greed Index
coinglass_indicators(action="fear_greed")

# Bitcoin Rainbow Chart
coinglass_indicators(action="rainbow")
```

### Tool Discovery

```python
# Search for liquidation-related tools
coinglass_search(query="liquidation")

# Check available features for your plan
coinglass_config(action="plan_features")
```

---

## Architecture

```
coinglass-mcp/
├── src/coinglass_mcp/
│   ├── server.py    # FastMCP server + 22 tools
│   ├── client.py    # HTTP client with retry logic
│   └── config.py    # Plan tiers, intervals, features
├── tests/
│   ├── test_client.py
│   └── test_tools.py
└── pyproject.toml
```

**Design Principles:**
- **3-file architecture** — Optimized for AI agent comprehension
- **Domain facade pattern** — 22 tools → 80+ endpoints
- **Literal-typed actions** — Helps LLMs select correct operations
- **Lifespan pattern** — Shared httpx.AsyncClient for efficiency

---

## Development

### Setup

```bash
git clone https://github.com/forgequant/coinglass-mcp.git
cd coinglass-mcp
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
```

### Testing

```bash
pytest -v
```

```
======================== 45 passed in 0.69s ========================
```

### Run Locally

```bash
export COINGLASS_API_KEY="your-key"
python -m coinglass_mcp.server
```

---

## FastMCP Cloud Deployment

**Entry point:** `coinglass_mcp.server:mcp`

**Environment variables:**
- `COINGLASS_API_KEY` — Your CoinGlass API key
- `COINGLASS_PLAN` — Subscription tier (default: `standard`)

---

## API Reference

Full CoinGlass API documentation: [open-api.coinglass.com](https://open-api.coinglass.com/)

---

## License

MIT

---

## Links

- [CoinGlass](https://www.coinglass.com) — Cryptocurrency derivatives analytics
- [FastMCP](https://github.com/jlowin/fastmcp) — Fast, Pythonic MCP server framework
- [MCP Protocol](https://modelcontextprotocol.io) — Model Context Protocol specification
