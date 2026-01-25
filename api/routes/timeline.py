# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights
# SPDX-License-Identifier: MIT

"""
Timeline API routes

Endpoints for temporal analysis of tags over time.
"""

from flask import Blueprint, request

from api.services.timeline_service import get_tags_timeline
from api.utils.response import success_response
from api.utils.validators import validate_integer, validate_string

timeline_bp = Blueprint("timeline", __name__, url_prefix="/api/timeline")


@timeline_bp.route("/tags", methods=["GET"])
def tags_timeline():
    """
    GET /api/timeline/tags

    Get tags over time analysis with year × tag matrix.

    Query parameters:
        - version: Tag version (e.g., 'tags_v3')
        - year_min: Minimum year (inclusive)
        - year_max: Maximum year (inclusive)
        - country: Filter by country name
        - region: Filter by region name

    Returns:
        {
            "status": "success",
            "data": {
                "timeline": [
                    {"year": 2020, "tags": {"AI": 5, "Privacy": 3}},
                    {"year": 2021, "tags": {"AI": 8, "Privacy": 7}},
                    ...
                ],
                "years": [2020, 2021, 2022, ...],
                "all_tags": ["AI", "Privacy", "ChildRights", ...],
                "total_documents": 45,
                "filters_applied": {...}
            }
        }
    """
    # Parse query parameters
    version = request.args.get("version")
    year_min = request.args.get("year_min")
    year_max = request.args.get("year_max")
    country = request.args.get("country")
    region = request.args.get("region")

    # Validate year parameters
    if year_min:
        year_min = validate_integer(year_min, "year_min", min_value=1900, max_value=2100)

    if year_max:
        year_max = validate_integer(year_max, "year_max", min_value=1900, max_value=2100)

    # Validate string parameters
    if version:
        version = validate_string(version, "version", max_length=50)

    if country:
        country = validate_string(country, "country", max_length=100)

    if region:
        region = validate_string(region, "region", max_length=100)

    # Get timeline data
    result = get_tags_timeline(
        version=version,
        year_min=year_min,
        year_max=year_max,
        country=country,
        region=region,
    )

    return success_response(result)
