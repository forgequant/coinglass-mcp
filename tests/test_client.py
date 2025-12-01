"""Tests for CoinGlass HTTP client."""

import pytest
import httpx
from unittest.mock import AsyncMock

from coinglass_mcp.client import (
    CoinGlassClient,
    RateLimitError,
    PlanLimitError,
    APIError,
    _is_retryable,
)


class TestIsRetryable:
    """Test _is_retryable function."""

    def test_timeout_is_retryable(self):
        """Timeout exceptions should be retried."""
        exc = httpx.TimeoutException("timeout")
        assert _is_retryable(exc) is True

    def test_connect_error_is_retryable(self):
        """Connection errors should be retried."""
        exc = httpx.ConnectError("connection failed")
        assert _is_retryable(exc) is True

    def test_500_is_retryable(self):
        """5xx HTTP errors should be retried."""
        response = AsyncMock()
        response.status_code = 500
        exc = httpx.HTTPStatusError("server error", request=None, response=response)
        assert _is_retryable(exc) is True

    def test_502_is_retryable(self):
        """502 Bad Gateway should be retried."""
        response = AsyncMock()
        response.status_code = 502
        exc = httpx.HTTPStatusError("bad gateway", request=None, response=response)
        assert _is_retryable(exc) is True

    def test_400_is_not_retryable(self):
        """4xx errors should not be retried."""
        response = AsyncMock()
        response.status_code = 400
        exc = httpx.HTTPStatusError("bad request", request=None, response=response)
        assert _is_retryable(exc) is False

    def test_random_exception_is_not_retryable(self):
        """Random exceptions should not be retried."""
        exc = ValueError("some error")
        assert _is_retryable(exc) is False


class TestCoinGlassClient:
    """Test CoinGlassClient."""

    async def test_request_success(self, client, mock_http, mock_response):
        """Successful API request returns data."""
        mock_http.get.return_value = mock_response({"coins": ["BTC", "ETH"]})

        result = await client.request("/api/futures/supported-coins")

        assert result == {"coins": ["BTC", "ETH"]}
        mock_http.get.assert_called_once()

    async def test_request_with_params(self, client, mock_http, mock_response):
        """Request includes query parameters."""
        mock_http.get.return_value = mock_response([{"symbol": "BTC"}])

        await client.request("/api/futures/coins-markets", {"symbol": "BTC"})

        call_kwargs = mock_http.get.call_args.kwargs
        assert call_kwargs["params"] == {"symbol": "BTC"}

    async def test_request_filters_none_params(self, client, mock_http, mock_response):
        """None values are filtered from params."""
        mock_http.get.return_value = mock_response([])

        await client.request(
            "/api/futures/coins-markets",
            {"symbol": "BTC", "exchange": None},
        )

        call_kwargs = mock_http.get.call_args.kwargs
        assert call_kwargs["params"] == {"symbol": "BTC"}

    async def test_request_includes_api_key(self, client, mock_http, mock_response):
        """Request includes API key header."""
        mock_http.get.return_value = mock_response([])

        await client.request("/api/test")

        call_kwargs = mock_http.get.call_args.kwargs
        assert call_kwargs["headers"]["CG-API-KEY"] == "test-api-key"

    async def test_rate_limit_error(self, client, mock_http):
        """429 response raises RateLimitError."""
        response = AsyncMock()
        response.status_code = 429
        mock_http.get.return_value = response

        with pytest.raises(RateLimitError):
            await client.request("/api/test")

    async def test_plan_limit_error(self, client, mock_http):
        """403 response raises PlanLimitError."""
        response = AsyncMock()
        response.status_code = 403
        mock_http.get.return_value = response

        with pytest.raises(PlanLimitError):
            await client.request("/api/test")

    async def test_invalid_api_key_error(self, client, mock_http):
        """401 response raises APIError."""
        response = AsyncMock()
        response.status_code = 401
        mock_http.get.return_value = response

        with pytest.raises(APIError, match="Invalid API key"):
            await client.request("/api/test")

    async def test_api_error_response(self, client, mock_http, mock_response):
        """Non-zero code in response raises APIError."""
        mock_http.get.return_value = mock_response(
            None,
            code="1",
            msg="Invalid parameter",
        )

        with pytest.raises(APIError, match="Invalid parameter"):
            await client.request("/api/test")
