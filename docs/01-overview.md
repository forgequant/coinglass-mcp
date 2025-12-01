# CoinGlass MCP Server - Overview

**Version:** 2.0
**Date:** December 1, 2025
**Purpose:** Technical specification for CoinGlass MCP server implementation using FastMCP Cloud

## Executive Summary

CoinGlass API contains **80+ endpoints** across 13 categories of cryptocurrency analytics. The architecture uses a **Domain Facade pattern** with semantic operation separation, optimized for LLM consumption:

- **22 MCP tools** (instead of 16) — split by semantic groups to reduce cognitive load
- **Literal-typed actions** — easier for LLM to substitute concrete values
- **Three-tier data abstraction** — raw / normalized / summary
- **Pluggable cache** with endpoint-specific TTLs
- **Plan-aware gating** with clear error messages

## Key Metrics

| Metric | Value |
|--------|-------|
| **MCP Tools** | 22 |
| **API Endpoints Covered** | 80+ |
| **Literal-typed Actions** | 45+ |
| **Data Levels** | raw / normalized / summary |
| **TTL Categories** | 7 (from 3 sec to 30 min) |
| **Tokens for Descriptions** | ~3,500 (vs ~15,000 with 1:1 mapping) |
| **Context Savings** | ~75% |

## Architecture Guarantees

- LLM-friendly interface with Literal typing
- Clear symbol/pair semantic separation
- Unified response contract for all tools
- Plan-aware gating with clear errors
- Pluggable cache with endpoint-specific TTLs
- Smart retry only for recoverable errors
- Data normalization for key domains
- Request tracing via trace_id

## Documentation Structure

| Document | Content |
|----------|---------|
| `02-api-specification.md` | CoinGlass API details, endpoints, rate limits |
| `03-architecture.md` | Project structure and design principles |
| `04-tools-market.md` | Market data tools specification |
| `05-tools-derivatives.md` | Open Interest, Funding, Long/Short tools |
| `06-tools-liquidation.md` | Liquidation and Order Book tools |
| `07-tools-whale-taker.md` | Whale tracking and Taker Buy/Sell tools |
| `08-tools-spot-options.md` | Spot, Options, On-Chain tools |
| `09-tools-etf-indicators.md` | ETF and Indicators tools |
| `10-tools-meta.md` | Search and Config meta tools |
| `11-core-components.md` | Response, Client, Cache, Validation code |
| `12-deployment.md` | Configuration and deployment guide |
| `13-implementation-plan.md` | Phased development plan |

## Quick Reference: Tool Categories

### Market Data (3 tools)
- `coinglass_market_info` — Static metadata (coins, pairs, exchanges)
- `coinglass_market_data` — Real-time summaries
- `coinglass_price_history` — Historical OHLC

### Derivatives (5 tools)
- `coinglass_oi_history` — Open Interest OHLC
- `coinglass_oi_distribution` — OI by exchange
- `coinglass_funding_history` — Funding rate OHLC
- `coinglass_funding_current` — Current rates, arbitrage
- `coinglass_long_short` — Long/Short ratios

### Liquidation & Order Book (5 tools)
- `coinglass_liq_history` — Liquidation history
- `coinglass_liq_orders` — Real-time liquidation orders
- `coinglass_liq_heatmap` — Heatmap visualizations
- `coinglass_ob_history` — Order book depth
- `coinglass_ob_large_orders` — Whale walls

### Whale & Taker (3 tools)
- `coinglass_whale_positions` — Whale tracking
- `coinglass_whale_index` — Whale Index
- `coinglass_taker` — Taker buy/sell volume

### Spot, Options, On-Chain (3 tools)
- `coinglass_spot` — Spot market data
- `coinglass_options` — Options analytics
- `coinglass_onchain` — On-chain exchange data

### ETF & Indicators (3 tools)
- `coinglass_etf` — Crypto ETF data
- `coinglass_grayscale` — Grayscale funds
- `coinglass_indicators` — Market indicators

### Meta (2 tools)
- `coinglass_search` — Discover operations
- `coinglass_config` — Configuration metadata
