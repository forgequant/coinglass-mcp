"""Pytest configuration and fixtures for CoinGlass MCP tests."""

import pytest
import httpx
from unittest.mock import AsyncMock, MagicMock

from coinglass_mcp.client import CoinGlassClient


@pytest.fixture
def mock_http():
    """Create mock httpx.AsyncClient."""
    mock = AsyncMock(spec=httpx.AsyncClient)
    return mock


@pytest.fixture
def client(mock_http):
    """Create CoinGlassClient with mock HTTP client."""
    return CoinGlassClient(
        http=mock_http,
        api_key="test-api-key",
    )


@pytest.fixture
def mock_response():
    """Factory for creating mock API responses."""

    def _create(data, code="0", msg="success"):
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {
            "code": code,
            "msg": msg,
            "data": data,
        }
        response.raise_for_status = MagicMock()
        return response

    return _create


@pytest.fixture
def mock_context():
    """Create mock FastMCP Context with lifespan data."""

    class MockRequestContext:
        def __init__(self, plan="standard"):
            self.lifespan_context = {
                "client": None,  # Will be set in tests
                "plan": plan,
            }

    class MockContext:
        def __init__(self, plan="standard"):
            self.request_context = MockRequestContext(plan)

    return MockContext
