# CoinGlass API Specification

## Base Configuration

| Parameter | Value |
|-----------|-------|
| Base URL | `https://open-api-v4.coinglass.com` |
| Authentication | Header `CG-API-KEY: {api_key}` |
| Response Format | JSON: `{"code": "0", "msg": "success", "data": ...}` |

## Rate Limits by Plan

| Plan | Requests/min | Minimum Interval | Special Features |
|------|-------------|------------------|------------------|
| Hobbyist | 30 | ≥4h | Basic endpoints |
| Startup | 80 | ≥30m | + Whale alerts |
| Standard | 300 | No restrictions | + Liquidation orders |
| Professional | 600 | No restrictions | + Heatmaps, Maps |
| Enterprise | 1200 | No restrictions | Everything |

## Endpoint Inventory (80+)

### Market Data (6 endpoints)
| Endpoint | Path | Description |
|----------|------|-------------|
| supported-coins | `/api/futures/supported-coins` | List of supported futures coins |
| supported-exchange-pairs | `/api/futures/supported-exchange-pairs` | Trading pairs by exchange |
| pairs-markets | `/api/futures/pairs-markets` | Per-pair market metrics |
| coins-markets | `/api/futures/coins-markets` | Per-coin aggregated metrics |
| price-change-list | `/api/futures/price-change-list` | Price changes across timeframes |
| ohlc-history | `/api/price/ohlc-history` | Historical price OHLC |

### Open Interest (6 endpoints)
| Endpoint | Path | Description |
|----------|------|-------------|
| ohlc-history | `/api/futures/openInterest/ohlc-history` | Single pair OI OHLC |
| ohlc-aggregated-history | `/api/futures/openInterest/ohlc-aggregated-history` | Aggregated OI OHLC |
| ohlc-aggregated-stablecoin | `/api/futures/openInterest/ohlc-aggregated-stablecoin` | USDT-margined OI |
| ohlc-aggregated-coin-margin | `/api/futures/openInterest/ohlc-aggregated-coin-margin-history` | Coin-margined OI |
| exchange-list | `/api/futures/openInterest/exchange-list` | OI by exchange |
| exchange-history-chart | `/api/futures/openInterest/exchange-history-chart` | Historical OI by exchange |

### Funding Rate (6 endpoints)
| Endpoint | Path | Description |
|----------|------|-------------|
| ohlc-history | `/api/futures/fundingRate/ohlc-history` | Single pair funding OHLC |
| oi-weight-ohlc-history | `/api/futures/fundingRate/oi-weight-ohlc-history` | OI-weighted funding |
| vol-weight-ohlc-history | `/api/futures/fundingRate/vol-weight-ohlc-history` | Volume-weighted funding |
| exchange-list | `/api/futures/fundingRate/exchange-list` | Current rates by exchange |
| accumulated-exchange-list | `/api/futures/fundingRate/accumulated-exchange-list` | Cumulative funding |
| arbitrage | `/api/futures/fundingRate/arbitrage` | Arbitrage opportunities |

### Long/Short Ratio (4 endpoints)
| Endpoint | Path | Description |
|----------|------|-------------|
| global-long-short-account-ratio | `/api/futures/globalLongShortAccountRatio/history` | Global L/S ratio |
| top-long-short-account-ratio | `/api/futures/topLongShortAccountRatio/history` | Top traders accounts |
| top-long-short-position-ratio | `/api/futures/topLongShortPositionRatio/history` | Top traders positions |
| exchange-list | `/api/futures/taker-buy-sell-volume/exchange-list` | Taker ratio by exchange |

### Liquidation (13 endpoints)
| Endpoint | Path | Description |
|----------|------|-------------|
| history | `/api/futures/liquidation/history` | Single pair liquidations |
| aggregated-history | `/api/futures/liquidation/aggregated-history` | Aggregated by coin |
| coin-list | `/api/futures/liquidation/coin-list` | Liquidations by coin |
| exchange-list | `/api/futures/liquidation/exchange-list` | Liquidations by exchange |
| order | `/api/futures/liquidation/order` | Real-time liq orders |
| heatmap/model1-3 | `/api/futures/liquidation/heatmap/model{1,2,3}` | Pair heatmap |
| aggregated-heatmap/model1-3 | `/api/futures/liquidation/aggregated-heatmap/model{1,2,3}` | Coin heatmap |
| map | `/api/futures/liquidation/map` | Pair leverage map |
| aggregated-map | `/api/futures/liquidation/aggregated-map` | Coin leverage map |

### Order Book (5 endpoints)
| Endpoint | Path | Description |
|----------|------|-------------|
| ask-bids-history | `/api/futures/orderbook/ask-bids-history` | Pair bid/ask history |
| aggregated-ask-bids-history | `/api/futures/orderbook/aggregated-ask-bids-history` | Aggregated depth |
| history | `/api/futures/orderbook/history` | Orderbook heatmap |
| large-limit-order | `/api/futures/orderbook/large-limit-order` | Current whale walls |
| large-limit-order-history | `/api/futures/orderbook/large-limit-order-history` | Historical large orders |

### Whale/Large Traders (4 endpoints)
| Endpoint | Path | Description |
|----------|------|-------------|
| whale-alert | `/api/hyperliquid/whale-alert` | Real-time whale alerts |
| whale-position | `/api/hyperliquid/whale-position` | Positions >$1M |
| position | `/api/hyperliquid/position` | All Hyperliquid positions |
| whale-index | `/api/index/whale-index` | Whale Index history |

### Taker Buy/Sell (4 endpoints)
| Endpoint | Path | Description |
|----------|------|-------------|
| history | `/api/futures/taker-buy-sell-volume/history` | Pair taker volume |
| aggregated-history | `/api/futures/taker-buy-sell-volume/aggregated-history` | Aggregated futures |
| spot-history | `/api/spot/taker-buy-sell-volume/history` | Spot taker volume |
| spot-aggregated-history | `/api/spot/taker-buy-sell-volume/aggregated-history` | Aggregated spot |

### Spot (11 endpoints)
Mirror of futures endpoints for spot markets:
- supported-coins, supported-exchange-pairs
- pairs-markets, coins-markets
- price-change-list, ohlc-history
- orderbook endpoints

### Options (4 endpoints)
| Endpoint | Path | Description |
|----------|------|-------------|
| max-pain | `/api/option/max-pain` | Max pain price |
| info | `/api/option/info` | OI/volume summary |
| exchange-oi-history | `/api/option/exchange-oi-history` | OI over time |
| exchange-vol-history | `/api/option/exchange-vol-history` | Volume over time |

### On-Chain (4 endpoints)
| Endpoint | Path | Description |
|----------|------|-------------|
| assets | `/api/exchange/assets` | Exchange holdings |
| balance/list | `/api/exchange/balance/list` | Balances by asset |
| balance/chart | `/api/exchange/balance/chart` | Historical balances |
| chain/tx/list | `/api/exchange/chain/tx/list` | ERC-20 transfers |

### ETF (12 endpoints)
| Endpoint | Path | Description |
|----------|------|-------------|
| bitcoin/list | `/api/etf/bitcoin/list` | Bitcoin ETF list |
| bitcoin/flows | `/api/etf/bitcoin/flows` | Daily flows |
| bitcoin/net-assets | `/api/etf/bitcoin/net-assets` | AUM history |
| bitcoin/premium-discount | `/api/etf/bitcoin/premium-discount` | Premium/discount |
| bitcoin/history | `/api/etf/bitcoin/history` | ETF history |
| bitcoin/detail | `/api/etf/bitcoin/detail` | ETF details |
| bitcoin/price | `/api/etf/bitcoin/price` | OHLC price |
| ethereum/* | Same structure for Ethereum ETFs |
| grayscale/holdings | `/api/grayscale/holdings` | Grayscale holdings |
| grayscale/premium | `/api/grayscale/premium` | Premium history |

### Indicators (16 endpoints)
| Endpoint | Path | Description |
|----------|------|-------------|
| rsi | `/api/indicator/rsi` | RSI for all coins |
| basis | `/api/indicator/basis` | Futures basis |
| coinbase-premium | `/api/indicator/coinbase-premium` | Coinbase premium |
| fear-greed | `/api/index/fear-greed-history` | Fear & Greed index |
| ahr999 | `/api/index/ahr999` | AHR999 indicator |
| puell | `/api/index/puell-multiple` | Puell Multiple |
| stock-flow | `/api/index/stock-to-flow` | Stock-to-Flow |
| pi-cycle | `/api/index/pi-cycle-top` | Pi Cycle Top |
| rainbow | `/api/index/rainbow-chart` | Rainbow chart |
| bubble | `/api/index/bitcoin-bubble-index` | Bubble index |
| 2y-ma | `/api/index/two-year-ma-multiplier` | 2-Year MA |
| 200w-ma | `/api/index/two-hundred-week-ma-heatmap` | 200-Week MA |
| profitable-days | `/api/index/bitcoin-profitable-days` | Profitable days |
| stablecoin-mcap | `/api/index/stablecoin-market-cap` | Stablecoin mcap |
| bull-peak | `/api/index/bull-market-peak-signals` | Bull peak signals |
| borrow-rate | `/api/indicator/borrow-rate` | Exchange borrow rates |

## Response Format

### Success Response
```json
{
  "code": "0",
  "msg": "success",
  "data": [...]
}
```

### Error Response
```json
{
  "code": "40001",
  "msg": "Invalid API key",
  "data": null
}
```

### Common Error Codes
| Code | Description |
|------|-------------|
| 40001 | Invalid API key |
| 40003 | Rate limit exceeded |
| 40004 | Feature requires higher plan |
| 50001 | Internal server error |

## Rate Limit Headers
```
API-KEY-MAX-LIMIT: 300
API-KEY-USE-LIMIT: 45
```
