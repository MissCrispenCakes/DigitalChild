"""
Scorecard API routes

Provides endpoints for accessing scorecard data and country indicators.
"""

from flask import Blueprint, current_app, request

from api.extensions import cache
from api.middleware.error_handlers import NotFoundError
from api.services.scorecard_service import (
    get_country_details,
    get_indicator_statistics,
    get_scorecard_summary,
)
from api.utils.response import paginated_response, success_response
from api.utils.validators import (
    ValidationError,
    validate_page,
    validate_per_page,
    validate_string,
)

scorecard_bp = Blueprint("scorecard", __name__, url_prefix="/api/scorecard")


@scorecard_bp.route("", methods=["GET"])
def list_countries():
    """
    Get summary of all countries in scorecard

    Query parameters:
        - region: Filter by region (optional)
        - page: Page number (default: 1)
        - per_page: Items per page (default: 20, max: 100)

    Returns:
        200: Paginated list of countries with indicator counts
        400: Validation error
    """
    try:
        # Validate pagination parameters
        page = validate_page(request.args.get("page"))
        per_page = validate_per_page(
            request.args.get("per_page"),
            default=current_app.config.get("DEFAULT_PAGE_SIZE", 20),
            max_value=current_app.config.get("MAX_PAGE_SIZE", 100),
        )

        # Validate filter parameters
        region = None
        if region_param := request.args.get("region"):
            region = validate_string(region_param, "region")

        # Get scorecard summary from service
        result = get_scorecard_summary(
            region=region,
            page=page,
            per_page=per_page,
        )

        # Return paginated response
        return paginated_response(
            items=result["countries"],
            page=result["pagination"]["page"],
            per_page=result["pagination"]["per_page"],
            total=result["pagination"]["total"],
        )

    except ValidationError as e:
        from api.utils.response import error_response

        details = {}
        if e.field:
            details["field"] = e.field

        return error_response(
            message=e.message,
            code="VALIDATION_ERROR",
            status_code=400,
            details=details,
        )


@scorecard_bp.route("/<country>", methods=["GET"])
@cache.cached(timeout=3600, key_prefix=lambda: f"scorecard:{request.view_args['country']}")
def get_country_scorecard(country):
    """
    Get full scorecard details for a specific country

    Path parameters:
        - country: Country name (e.g., "Kenya", "Albania")

    Returns:
        200: Full scorecard with all indicators
        404: Country not found

    Cache: 1 hour (scorecard updates weekly)
    """
    try:
        scorecard = get_country_details(country)
        return success_response(scorecard)

    except NotFoundError as e:
        from api.utils.response import error_response

        return error_response(
            message=str(e.message),
            code="NOT_FOUND",
            status_code=404,
        )


@scorecard_bp.route("/indicators/statistics", methods=["GET"])
@cache.cached(timeout=3600, key_prefix="scorecard:indicator_stats")
def get_indicator_stats():
    """
    Get statistics about indicator values across all countries

    Returns value distribution for each indicator (e.g., how many countries
    have "In force", "None", etc. for Data_Protection_Law).

    Returns:
        200: Indicator statistics

    Cache: 1 hour (scorecard updates weekly)
    """
    stats = get_indicator_statistics()
    return success_response(stats)
