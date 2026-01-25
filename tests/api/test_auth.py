# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights
# SPDX-License-Identifier: MIT

"""
Tests for API authentication middleware

Tests API key authentication, decorators, and error handling.
"""

import json

import pytest


class TestAPIKeyAuthentication:
    """Tests for API key authentication"""

    def test_valid_api_key(self, client):
        """Test request with valid API key"""
        # In development mode without configured keys, all requests are allowed
        response = client.get("/api/documents", headers={"X-API-Key": "test-key-12345"})

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"

    def test_missing_api_key(self, client):
        """Test request without API key (allowed in development)"""
        response = client.get("/api/documents")

        # Development mode allows requests without API key
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"

    def test_optional_auth_endpoint(self, client):
        """Test endpoint with optional authentication"""
        # Test without API key
        response = client.get("/api/documents")
        assert response.status_code == 200

        # Test with API key
        response = client.get("/api/documents", headers={"X-API-Key": "test-key-12345"})
        assert response.status_code == 200


class TestAuthenticationHelpers:
    """Tests for authentication helper functions"""

    def test_get_api_key_from_request(self, app):
        """Test extracting API key from request headers"""
        from api.middleware.auth import get_api_key_from_request

        with app.test_request_context(headers={"X-API-Key": "test-key"}):
            api_key = get_api_key_from_request()
            assert api_key == "test-key"

    def test_get_api_key_missing(self, app):
        """Test extracting API key when not present"""
        from api.middleware.auth import get_api_key_from_request

        with app.test_request_context():
            api_key = get_api_key_from_request()
            assert api_key is None

    def test_validate_api_key_development(self, app):
        """Test API key validation in development mode"""
        from api.middleware.auth import validate_api_key

        with app.app_context():
            # Development mode without configured keys should allow any key
            assert validate_api_key("any-key") is True
            assert validate_api_key(None) is False

    def test_is_authenticated(self, app):
        """Test checking if request is authenticated"""
        from api.middleware.auth import is_authenticated

        with app.test_request_context(headers={"X-API-Key": "test-key"}):
            # Development mode allows authentication
            assert is_authenticated() is True

        with app.test_request_context():
            # No key should not be authenticated
            assert is_authenticated() is False


class TestAuthenticationErrors:
    """Tests for authentication error handling"""

    def test_authentication_error_format(self):
        """Test AuthenticationError exception format"""
        from api.middleware.auth import AuthenticationError

        error = AuthenticationError(
            message="Custom error message", details={"field": "api_key"}
        )

        assert error.status_code == 401
        assert error.error_code == "AUTHENTICATION_FAILED"
        assert error.message == "Custom error message"
        assert error.details == {"field": "api_key"}

    def test_authentication_error_defaults(self):
        """Test AuthenticationError with default values"""
        from api.middleware.auth import AuthenticationError

        error = AuthenticationError()

        assert error.status_code == 401
        assert error.error_code == "AUTHENTICATION_FAILED"
        assert error.message == "Authentication required"


class TestAPIKeyConfiguration:
    """Tests for API key configuration"""

    def test_get_api_keys_from_string(self, app):
        """Test parsing API keys from comma-separated string"""
        from api.middleware.auth import get_api_keys

        # Set config with comma-separated keys
        app.config["API_KEYS"] = "key1,key2,key3"

        with app.app_context():
            keys = get_api_keys()
            assert keys == ["key1", "key2", "key3"]

    def test_get_api_keys_empty(self, app):
        """Test getting API keys when none configured"""
        from api.middleware.auth import get_api_keys

        app.config["API_KEYS"] = ""

        with app.app_context():
            keys = get_api_keys()
            assert keys == []

    def test_get_api_keys_list(self, app):
        """Test getting API keys when provided as list"""
        from api.middleware.auth import get_api_keys

        app.config["API_KEYS"] = ["key1", "key2"]

        with app.app_context():
            keys = get_api_keys()
            assert keys == ["key1", "key2"]


@pytest.fixture
def app_with_required_auth(app):
    """Fixture for app with required authentication"""
    app.config["FLASK_ENV"] = "production"
    app.config["API_KEYS"] = "valid-key-1,valid-key-2"
    return app


class TestProductionAuthentication:
    """Tests for authentication in production mode"""

    def test_valid_key_in_production(self, app_with_required_auth):
        """Test request with valid API key in production"""
        from api.middleware.auth import validate_api_key

        with app_with_required_auth.app_context():
            assert validate_api_key("valid-key-1") is True
            assert validate_api_key("valid-key-2") is True

    def test_invalid_key_in_production(self, app_with_required_auth):
        """Test request with invalid API key in production"""
        from api.middleware.auth import validate_api_key

        with app_with_required_auth.app_context():
            assert validate_api_key("invalid-key") is False
            assert validate_api_key(None) is False
            assert validate_api_key("") is False
