# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights
# SPDX-License-Identifier: MIT

"""
Authentication middleware

Provides API key authentication and decorators for protecting endpoints.
"""

from functools import wraps

from flask import current_app, request

from api.middleware.error_handlers import APIError


class AuthenticationError(APIError):
    """Raised when authentication fails"""

    status_code = 401
    error_code = "AUTHENTICATION_FAILED"
    message = "Authentication required"


def get_api_keys():
    """
    Get list of valid API keys from configuration

    Returns:
        List of valid API keys
    """
    keys = current_app.config.get("API_KEYS", "")
    if isinstance(keys, str):
        # Parse comma-separated keys from environment variable
        return [k.strip() for k in keys.split(",") if k.strip()]
    return keys


def validate_api_key(api_key):
    """
    Validate an API key

    Args:
        api_key: API key to validate

    Returns:
        True if valid, False otherwise
    """
    if not api_key:
        return False

    valid_keys = get_api_keys()

    # In development with no keys configured, allow all requests
    if current_app.config.get("FLASK_ENV") == "development" and not valid_keys:
        current_app.logger.debug("Development mode: Allowing request without API key")
        return True

    return api_key in valid_keys


def require_api_key(f):
    """
    Decorator to require API key authentication

    Usage:
        @require_api_key
        def protected_endpoint():
            return {"data": "secret"}

    API key should be provided in X-API-Key header.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get("X-API-Key")

        if not validate_api_key(api_key):
            current_app.logger.warning(
                f"Authentication failed for {request.path} from {request.remote_addr}"
            )
            raise AuthenticationError(
                message="Invalid or missing API key",
                details={"hint": "Provide API key in X-API-Key header"},
            )

        current_app.logger.debug(f"Authenticated request to {request.path}")
        return f(*args, **kwargs)

    return decorated_function


def optional_api_key(f):
    """
    Decorator for endpoints that work with or without API key

    If API key is provided and valid, it's available in request context.
    If no key or invalid key, request continues without authentication.

    Usage:
        @optional_api_key
        def endpoint():
            is_authenticated = hasattr(request, 'authenticated')
            return {"authenticated": is_authenticated}
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get("X-API-Key")

        if api_key and validate_api_key(api_key):
            request.authenticated = True
            current_app.logger.debug(
                f"Authenticated request to {request.path} (optional auth)"
            )
        else:
            request.authenticated = False
            current_app.logger.debug(
                f"Unauthenticated request to {request.path} (optional auth)"
            )

        return f(*args, **kwargs)

    return decorated_function


def get_api_key_from_request():
    """
    Extract API key from current request

    Returns:
        API key string or None
    """
    return request.headers.get("X-API-Key")


def is_authenticated():
    """
    Check if current request is authenticated

    Returns:
        True if request has valid API key, False otherwise
    """
    api_key = get_api_key_from_request()
    return validate_api_key(api_key)
