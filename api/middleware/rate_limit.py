# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights
# SPDX-License-Identifier: MIT

"""
Rate limiting middleware

Provides rate limiting decorators for API endpoints.
Uses Flask-Limiter with configurable storage backends.
"""

from flask import current_app, request

from api.middleware.auth import is_authenticated


def get_rate_limit_key():
    """
    Generate rate limit key based on authentication status

    Returns:
        Rate limit key (API key if authenticated, IP address otherwise)
    """
    api_key = request.headers.get("X-API-Key")
    if api_key:
        return f"api_key:{api_key}"
    return f"ip:{request.remote_addr}"


def get_rate_limit():
    """
    Get rate limit based on authentication status

    Returns:
        Rate limit string (e.g., "1000 per hour" for authenticated,
        "100 per hour" for unauthenticated)
    """
    if is_authenticated():
        return current_app.config.get("RATELIMIT_AUTHENTICATED", "1000 per hour")
    return current_app.config.get("RATELIMIT_PUBLIC", "100 per hour")


# Rate limit decorators using dynamic limits
def dynamic_limit():
    """
    Dynamic rate limit based on authentication status

    - Authenticated: 1000 requests/hour
    - Public: 100 requests/hour

    Returns:
        Rate limit string for current request
    """
    return get_rate_limit()


# Custom rate limits for specific use cases
def rate_limit_high():
    """
    High rate limit for expensive operations

    Returns:
        "50 per hour" for public, "500 per hour" for authenticated
    """
    if is_authenticated():
        return "500 per hour"
    return "50 per hour"


def rate_limit_export():
    """
    Rate limit for CSV export operations

    Returns:
        "20 per hour" for public, "200 per hour" for authenticated
    """
    if is_authenticated():
        return "200 per hour"
    return "20 per hour"


def rate_limit_search():
    """
    Rate limit for search/filter operations

    Returns:
        "200 per hour" for public, "2000 per hour" for authenticated
    """
    if is_authenticated():
        return "2000 per hour"
    return "200 per hour"
