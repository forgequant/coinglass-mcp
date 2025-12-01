# Architecture

## Design Principles

1. **Semantic tool separation** — one tool = one conceptual operation
2. **Literal-typed actions** — LLM sees concrete options
3. **Clear symbol/pair separation** — `symbol` for aggregated data, `pair` for specific contracts
4. **Unified response contract** — all tools return identical structure
5. **Plan-aware gating** — clear errors when exceeding plan limits

## Project Structure

```
coinglass-mcp/
├── server.py                 # Entry point + lifespan
├── config.py                 # Constants, plans, TTL
├── tools/
│   ├── __init__.py          # Register all tools
│   ├── market.py            # coinglass_market_*
│   ├── open_interest.py     # coinglass_oi_*
│   ├── funding.py           # coinglass_funding_*
│   ├── long_short.py        # coinglass_ls_*
│   ├── liquidation.py       # coinglass_liq_*
│   ├── orderbook.py         # coinglass_ob_*
│   ├── whale.py             # coinglass_whale_*
│   ├── taker.py             # coinglass_taker_*
│   ├── spot.py              # coinglass_spot_*
│   ├── options.py           # coinglass_options
│   ├── onchain.py           # coinglass_onchain
│   ├── etf.py               # coinglass_etf
│   ├── indicators.py        # coinglass_indicators
│   └── meta.py              # coinglass_search, coinglass_config
├── core/
│   ├── __init__.py
│   ├── client.py            # HTTP client + smart retry
│   ├── cache.py             # Pluggable cache backend
│   ├── response.py          # Unified response format
│   ├── errors.py            # Typed errors
│   └── validation.py        # Plan gating + param validation
├── models/
│   ├── __init__.py
│   ├── params.py            # Pydantic input models
│   ├── normalized.py        # Normalized output models
│   └── enums.py             # Literal types for actions
├── tests/
│   ├── conftest.py          # Fixtures + mock client
│   ├── test_tools.py        # Unit tests
│   └── test_smoke.py        # Integration with real API
├── requirements.txt
└── README.md
```

## Module Responsibilities

### `server.py`
- FastMCP server initialization
- Lifespan management (startup/shutdown)
- Shared resources (HTTP client, cache, config)
- Tool registration

### `tools/`
Each tool module contains:
- Literal type definitions for actions
- Tool function with Annotated parameters
- Endpoint mapping
- Input validation
- Response formatting

### `core/`
Shared infrastructure:
- **client.py** — HTTP client with smart retry (only retryable errors)
- **cache.py** — Pluggable cache backends (memory, null)
- **response.py** — Unified response format for all tools
- **errors.py** — Typed exceptions with context
- **validation.py** — Plan gating, parameter validation

### `models/`
Data models:
- **enums.py** — All Literal types for actions
- **params.py** — Pydantic models for tool inputs
- **normalized.py** — Normalized output models (OHLC, ratios, etc.)

## Data Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   LLM       │────▶│  MCP Tool   │────▶│  Validation │
└─────────────┘     └─────────────┘     └─────────────┘
                                               │
                                               ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Response   │◀────│  Normalize  │◀────│   Cache     │
└─────────────┘     └─────────────┘     └─────────────┘
                                               │
                                               ▼
                                        ┌─────────────┐
                                        │ HTTP Client │
                                        └─────────────┘
                                               │
                                               ▼
                                        ┌─────────────┐
                                        │ CoinGlass   │
                                        │    API      │
                                        └─────────────┘
```

## Request Processing Steps

1. **LLM invokes tool** with action + parameters
2. **Validation layer** checks:
   - Required parameters for action
   - Plan access for action/interval
   - Parameter value constraints
3. **Cache lookup** with endpoint + params key
4. **HTTP request** if cache miss
5. **Error handling** with smart retry
6. **Data normalization** (raw → normalized)
7. **Cache storage** with endpoint-specific TTL
8. **Response formatting** with unified structure

## Symbol vs Pair Semantics

| Context | Parameter | Example | Use Case |
|---------|-----------|---------|----------|
| Aggregated | `symbol` | `BTC`, `ETH` | OI across all exchanges |
| Specific | `pair` | `BTCUSDT` | Single trading pair |
| Specific | `exchange` | `Binance` | Required with pair |

### Examples

```python
# Aggregated: BTC open interest across all exchanges
coinglass_oi_history(action="aggregated", symbol="BTC")

# Specific: BTCUSDT on Binance
coinglass_oi_history(action="pair", exchange="Binance", pair="BTCUSDT")
```

## Error Hierarchy

```
BaseError
├── ValidationError      # Missing/invalid parameters
├── PlanLimitError       # Feature requires higher plan
├── RateLimitError       # Rate limit exceeded
├── AuthError            # Invalid API key
├── APIError             # CoinGlass API error
└── NetworkError         # Connection/timeout
```

## Caching Strategy

### TTL by Data Type

| Data Type | TTL | Examples |
|-----------|-----|----------|
| Static metadata | 30 min | supported-coins, exchanges |
| Market summaries | 15 sec | coins-markets, pairs-markets |
| Historical OHLC | 2 min | price history, OI history |
| Real-time orders | 3-5 sec | liquidation orders, whale alerts |
| Indicators | 1-5 min | fear-greed, whale index |

### Cache Key Generation

```python
key = md5(f"{endpoint}:{json.dumps(params, sort_keys=True)}")
```
