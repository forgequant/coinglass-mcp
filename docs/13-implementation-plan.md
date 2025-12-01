# Implementation Plan

## Overview

Phased development approach for the CoinGlass MCP server.

| Phase | Focus | Duration |
|-------|-------|----------|
| Phase 1 | Core Foundation | 2 days |
| Phase 2 | Key Tools | 3 days |
| Phase 3 | Extended Tools | 2 days |
| Phase 4 | Meta & Polish | 1-2 days |

**Total:** 8-9 days

---

## Phase 1: Core Foundation (2 days)

### Day 1: Infrastructure

- [ ] Project structure setup
- [ ] `core/client.py` — HTTP client with smart retry
- [ ] `core/response.py` — unified response format
- [ ] `core/errors.py` — typed exceptions
- [ ] `core/validation.py` — plan gating

### Day 2: Cache & Server

- [ ] `core/cache.py` — pluggable cache
- [ ] `models/enums.py` — Literal types for actions
- [ ] `server.py` — lifespan and base server
- [ ] Basic tests for core components

### Deliverables
- Working server skeleton
- HTTP client with retry logic
- Cache infrastructure
- Plan validation system

---

## Phase 2: Key Tools (3 days)

### Day 3: Market & OI

- [ ] `coinglass_market_info`
- [ ] `coinglass_market_data`
- [ ] `coinglass_price_history`
- [ ] `coinglass_oi_history`
- [ ] `coinglass_oi_distribution`

### Day 4: Funding & Long/Short

- [ ] `coinglass_funding_history`
- [ ] `coinglass_funding_current`
- [ ] `coinglass_long_short`
- [ ] `models/normalized.py` — OI, Funding, L/S normalization

### Day 5: Liquidation & Order Book

- [ ] `coinglass_liq_history`
- [ ] `coinglass_liq_orders`
- [ ] `coinglass_liq_heatmap`
- [ ] `coinglass_ob_history`
- [ ] `coinglass_ob_large_orders`

### Deliverables
- 13 tools implemented
- Data normalization for key types
- Unit tests for all tools

---

## Phase 3: Extended Tools (2 days)

### Day 6: Whale & Taker & Spot

- [ ] `coinglass_whale_positions`
- [ ] `coinglass_whale_index`
- [ ] `coinglass_taker`
- [ ] `coinglass_spot`

### Day 7: Options, On-Chain, ETF, Indicators

- [ ] `coinglass_options`
- [ ] `coinglass_onchain`
- [ ] `coinglass_etf`
- [ ] `coinglass_grayscale`
- [ ] `coinglass_indicators`

### Deliverables
- All 22 tools implemented
- Full API coverage

---

## Phase 4: Meta & Polish (1-2 days)

### Day 8: Discovery & Documentation

- [ ] `coinglass_search`
- [ ] `coinglass_config`
- [ ] Comprehensive tests (happy path + errors)
- [ ] README documentation

### Day 9 (Optional): Production Readiness

- [ ] Smoke tests with real API
- [ ] Performance tuning
- [ ] Cache optimization
- [ ] Monitoring setup

### Deliverables
- Complete tool set
- Full test coverage
- Production-ready deployment

---

## Implementation Order Rationale

### Why This Order?

1. **Core first** — All tools depend on client, cache, validation
2. **High-value tools early** — OI, Funding, Liquidation are most used
3. **Related tools together** — Easier to share patterns and tests
4. **Meta last** — Search/config depend on knowing all tools

### Dependencies

```
Phase 1 (Core)
    │
    ├── Phase 2 (Key Tools)
    │       │
    │       └── Phase 3 (Extended Tools)
    │               │
    │               └── Phase 4 (Meta)
    │
    └── Tests (parallel throughout)
```

---

## Testing Strategy

### Unit Tests (Every Phase)

```python
# tests/test_tools.py
import pytest
from unittest.mock import AsyncMock

@pytest.fixture
def mock_client():
    client = AsyncMock()
    client.request.return_value = {
        "data": [...],
        "rate_info": {"limit": "300", "used": "45"}
    }
    return client

async def test_oi_history_aggregated(mock_client):
    result = await coinglass_oi_history(
        action="aggregated",
        symbol="BTC",
        interval="h4",
        ctx=mock_context(client=mock_client)
    )

    assert result["success"] is True
    assert result["action"] == "aggregated"
    assert "data" in result
```

### Integration Tests (Phase 4)

```python
# tests/test_smoke.py
import pytest

@pytest.mark.real_api
async def test_real_market_data():
    result = await coinglass_market_data(action="coins_summary")

    assert result["success"] is True
    assert len(result["data"]) > 0
    assert "BTC" in [d["symbol"] for d in result["data"]]
```

---

## Risk Mitigation

### API Changes
- Version lock endpoints in config
- Graceful degradation for missing fields

### Rate Limits
- Per-endpoint TTL configuration
- Smart caching reduces API calls by 60-80%

### Plan Restrictions
- Clear error messages with upgrade hints
- Graceful fallbacks where possible

---

## Success Criteria

### Phase 1
- [ ] Server starts without errors
- [ ] HTTP client handles retries correctly
- [ ] Cache stores and retrieves data
- [ ] Plan validation blocks restricted actions

### Phase 2
- [ ] All 13 tools return valid responses
- [ ] Data normalization works correctly
- [ ] Error handling is consistent

### Phase 3
- [ ] All 22 tools implemented
- [ ] No regressions in existing tools

### Phase 4
- [ ] Search returns relevant results
- [ ] Config shows accurate information
- [ ] All tests pass
- [ ] Documentation is complete

---

## Final Metrics

| Metric | Target |
|--------|--------|
| MCP Tools | 22 |
| API Coverage | 80+ endpoints |
| Test Coverage | >80% |
| Cache Hit Rate | >60% |
| Context Token Savings | ~75% |
