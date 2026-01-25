# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights
# SPDX-License-Identifier: MIT

"""
Standard response formatter for API endpoints

Provides consistent JSON response structure across all endpoints.
"""

from datetime import datetime
from typing import Any, Dict, Optional

from flask import jsonify


def success_response(data: Any, status_code: int = 200):
    """
    Create a standardized success response

    Args:
        data: Response data (will be nested under "data" key)
        status_code: HTTP status code (default: 200)

    Returns:
        Flask JSON response with standard format
    """
    response = {
        "status": "success",
        "data": data,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    return jsonify(response), status_code


def error_response(
    message: str,
    code: str = "ERROR",
    status_code: int = 500,
    details: Optional[Dict] = None,
):
    """
    Create a standardized error response

    Args:
        message: Human-readable error message
        code: Error code (e.g., "NOT_FOUND", "VALIDATION_ERROR")
        status_code: HTTP status code (default: 500)
        details: Additional error details (optional)

    Returns:
        Flask JSON response with standard error format
    """
    response = {
        "status": "error",
        "error": {
            "code": code,
            "message": message,
            "details": details or {},
        },
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    return jsonify(response), status_code


def paginated_response(
    items: list, page: int, per_page: int, total: int, status_code: int = 200
):
    """
    Create a standardized paginated response

    Args:
        items: List of items for current page
        page: Current page number (1-indexed)
        per_page: Items per page
        total: Total number of items across all pages
        status_code: HTTP status code (default: 200)

    Returns:
        Flask JSON response with pagination metadata
    """
    total_pages = (total + per_page - 1) // per_page  # Ceiling division

    data = {
        "items": items,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1,
        },
    }

    return success_response(data, status_code)
