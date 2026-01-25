# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights
# SPDX-License-Identifier: MIT

"""
Tags API routes

Endpoints for tag frequency analysis and version management.
"""

from flask import Blueprint, request

from api.services.tags_service import get_available_versions, get_tag_frequency
from api.utils.response import success_response
from api.utils.validators import validate_integer, validate_string

tags_bp = Blueprint("tags", __name__, url_prefix="/api/tags")


@tags_bp.route("", methods=["GET"])
def list_tags():
    """
    GET /api/tags

    Get tag frequency with optional filters.

    Query parameters:
        - version: Tag version (e.g., 'tags_v3')
        - country: Filter by country name
        - region: Filter by region name
        - year: Filter by specific year
        - year_min: Minimum year (inclusive)
        - year_max: Maximum year (inclusive)

    Returns:
        {
            "status": "success",
            "data": {
                "tags": [
                    {"tag": "AI", "count": 42, "percentage": 45.5},
                    ...
                ],
                "total_documents": 92,
                "filters_applied": {...}
            }
        }
    """
    # Parse query parameters
    version = request.args.get("version")
    country = request.args.get("country")
    region = request.args.get("region")
    year = request.args.get("year")
    year_min = request.args.get("year_min")
    year_max = request.args.get("year_max")

    # Validate year parameters
    if year:
        year = validate_integer(year, "year", min_value=1900, max_value=2100)

    if year_min:
        year_min = validate_integer(
            year_min, "year_min", min_value=1900, max_value=2100
        )

    if year_max:
        year_max = validate_integer(
            year_max, "year_max", min_value=1900, max_value=2100
        )

    # Validate string parameters
    if version:
        version = validate_string(version, "version", max_length=50)

    if country:
        country = validate_string(country, "country", max_length=100)

    if region:
        region = validate_string(region, "region", max_length=100)

    # Get tag frequency
    result = get_tag_frequency(
        version=version,
        country=country,
        region=region,
        year=year,
        year_min=year_min,
        year_max=year_max,
    )

    return success_response(result)


@tags_bp.route("/versions", methods=["GET"])
def list_versions():
    """
    GET /api/tags/versions

    Get list of available tag versions.

    Returns:
        {
            "status": "success",
            "data": {
                "versions": ["tags_v1", "tags_v2", "tags_v3", "digital"],
                "count": 4
            }
        }
    """
    versions = get_available_versions()

    return success_response({"versions": versions, "count": len(versions)})
