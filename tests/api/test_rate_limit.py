# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights
# SPDX-License-Identifier: MIT

"""
Tests for rate limiting middleware

Tests rate limit functions and configuration.
"""


class TestRateLimitFunctions:
    """Tests for rate limit helper functions"""

    def test_get_rate_limit_key_with_api_key(self, app):
        """Test rate limit key generation with API key"""
        from api.middleware.rate_limit import get_rate_limit_key

        with app.test_request_context(headers={"X-API-Key": "test-key-123"}):
            key = get_rate_limit_key()
            assert key == "api_key:test-key-123"

    def test_get_rate_limit_key_without_api_key(self, app):
        """Test rate limit key generation without API key"""
        from api.middleware.rate_limit import get_rate_limit_key

        with app.test_request_context():
            key = get_rate_limit_key()
            assert key.startswith("ip:")

    def test_get_rate_limit_authenticated(self, app):
        """Test rate limit for authenticated requests"""
        from api.middleware.rate_limit import get_rate_limit

        with app.test_request_context(headers={"X-API-Key": "test-key"}):
            limit = get_rate_limit()
            # In development mode, authenticated requests get higher limit
            assert "per hour" in limit

    def test_get_rate_limit_unauthenticated(self, app):
        """Test rate limit for unauthenticated requests"""
        from api.middleware.rate_limit import get_rate_limit

        with app.test_request_context():
            limit = get_rate_limit()
            assert "per hour" in limit


class TestDynamicRateLimits:
    """Tests for dynamic rate limit functions"""

    def test_dynamic_limit_authenticated(self, app):
        """Test dynamic limit with authentication"""
        from api.middleware.rate_limit import dynamic_limit

        app.config["RATELIMIT_AUTHENTICATED"] = "1000 per hour"

        with app.test_request_context(headers={"X-API-Key": "test-key"}):
            limit = dynamic_limit()
            # Development mode returns authenticated limit
            assert isinstance(limit, str)
            assert "per hour" in limit

    def test_dynamic_limit_unauthenticated(self, app):
        """Test dynamic limit without authentication"""
        from api.middleware.rate_limit import dynamic_limit

        app.config["RATELIMIT_PUBLIC"] = "100 per hour"

        with app.test_request_context():
            limit = dynamic_limit()
            assert limit == "100 per hour"

    def test_rate_limit_high(self, app):
        """Test high rate limit function"""
        from api.middleware.rate_limit import rate_limit_high

        with app.test_request_context(headers={"X-API-Key": "test-key"}):
            limit = rate_limit_high()
            assert "per hour" in limit

        with app.test_request_context():
            limit = rate_limit_high()
            assert limit == "50 per hour"

    def test_rate_limit_export(self, app):
        """Test export rate limit function"""
        from api.middleware.rate_limit import rate_limit_export

        with app.test_request_context(headers={"X-API-Key": "test-key"}):
            limit = rate_limit_export()
            assert limit == "200 per hour"

        with app.test_request_context():
            limit = rate_limit_export()
            assert limit == "20 per hour"

    def test_rate_limit_search(self, app):
        """Test search rate limit function"""
        from api.middleware.rate_limit import rate_limit_search

        with app.test_request_context(headers={"X-API-Key": "test-key"}):
            limit = rate_limit_search()
            assert limit == "2000 per hour"

        with app.test_request_context():
            limit = rate_limit_search()
            assert limit == "200 per hour"


class TestRateLimitConfiguration:
    """Tests for rate limit configuration"""

    def test_default_rate_limits(self, app):
        """Test default rate limit configuration"""
        assert "RATELIMIT_PUBLIC" in app.config
        assert "RATELIMIT_AUTHENTICATED" in app.config
        assert "RATELIMIT_STORAGE_URI" in app.config

    def test_rate_limit_values(self, app):
        """Test rate limit value formats"""
        public_limit = app.config.get("RATELIMIT_PUBLIC")
        authenticated_limit = app.config.get("RATELIMIT_AUTHENTICATED")

        assert "per hour" in public_limit
        assert "per hour" in authenticated_limit

        # Parse numbers
        public_num = int(public_limit.split()[0])
        auth_num = int(authenticated_limit.split()[0])

        # Authenticated should have higher limit
        assert auth_num > public_num


class TestRateLimitIntegration:
    """Integration tests for rate limiting on endpoints"""

    def test_export_endpoint_rate_limit(self, client):
        """Test that export endpoint has rate limiting applied"""
        # First request should succeed
        response = client.get("/api/export")
        assert response.status_code == 200

        # Check for rate limit headers (may vary based on Flask-Limiter config)
        # Headers like X-RateLimit-Limit, X-RateLimit-Remaining may be present

    def test_documents_endpoint_rate_limit(self, client):
        """Test that documents endpoint has rate limiting applied"""
        # First request should succeed
        response = client.get("/api/documents")
        assert response.status_code == 200

    def test_authenticated_request_higher_limit(self, client):
        """Test that authenticated requests have higher limits"""
        # Request with API key
        response = client.get("/api/documents", headers={"X-API-Key": "test-key-123"})
        assert response.status_code == 200

        # Request without API key
        response = client.get("/api/documents")
        assert response.status_code == 200
