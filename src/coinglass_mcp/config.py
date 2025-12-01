"""CoinGlass MCP configuration."""

from typing import Literal

# API Configuration
BASE_URL = "https://open-api-v4.coinglass.com"
TIMEOUT = 30.0

# Plan types
Plan = Literal["hobbyist", "startup", "standard", "professional", "enterprise"]

# Plan hierarchy for comparison
PLAN_HIERARCHY: dict[str, int] = {
    "hobbyist": 0,
    "startup": 1,
    "standard": 2,
    "professional": 3,
    "enterprise": 4,
}

# Available intervals by plan
PLAN_INTERVALS: dict[str, set[str]] = {
    "hobbyist": {"h4", "h8", "h12", "d1", "w1"},
    "startup": {"m30", "h1", "h4", "h8", "h12", "d1", "w1"},
    "standard": {"m1", "m5", "m15", "m30", "h1", "h4", "h8", "h12", "d1", "w1"},
    "professional": {"m1", "m5", "m15", "m30", "h1", "h4", "h8", "h12", "d1", "w1"},
    "enterprise": {"m1", "m5", "m15", "m30", "h1", "h4", "h8", "h12", "d1", "w1"},
}

# Features available by plan
PLAN_FEATURES: dict[str, set[str]] = {
    "hobbyist": set(),
    "startup": {"whale_alerts", "whale_positions", "all_positions"},
    "standard": {"whale_alerts", "whale_positions", "all_positions", "liq_orders"},
    "professional": {"whale_alerts", "whale_positions", "all_positions", "liq_orders", "heatmaps", "maps"},
    "enterprise": {"whale_alerts", "whale_positions", "all_positions", "liq_orders", "heatmaps", "maps"},
}

# Action -> minimum required plan
ACTION_PLAN: dict[str, str] = {
    # Liquidation
    "orders": "standard",
    "pair_heatmap": "professional",
    "coin_heatmap": "professional",
    "pair_map": "professional",
    "coin_map": "professional",
    # Whale
    "alerts": "startup",
    "positions": "startup",
    "all_positions": "startup",
}

# Action -> required parameters
ACTION_PARAMS: dict[str, list[str]] = {
    # OI History
    "pair": ["exchange", "pair"],
    "aggregated": ["symbol"],
    "stablecoin": ["symbol"],
    "coin_margin": ["symbol"],
    # OI Distribution
    "by_exchange": ["symbol"],
    "exchange_chart": ["symbol"],
    # Funding
    "oi_weighted": ["symbol"],
    "vol_weighted": ["symbol"],
    # Long/Short
    "global": ["exchange", "pair"],
    "top_accounts": ["exchange", "pair"],
    "top_positions": ["exchange", "pair"],
    # Price
    "price_history": ["exchange", "pair", "interval"],
}

# Cache TTL (seconds) - used with ResponseCachingMiddleware
CACHE_TTL = 60
