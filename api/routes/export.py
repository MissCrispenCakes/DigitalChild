# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights
# SPDX-License-Identifier: MIT

"""
Export API routes

Endpoints for downloading datasets in CSV format.
"""

from flask import Blueprint, Response, request

from api.extensions import limiter
from api.middleware.auth import optional_api_key
from api.middleware.error_handlers import APIError
from api.middleware.rate_limit import rate_limit_export
from api.services.export_service import generate_export, get_available_formats
from api.utils.response import success_response
from api.utils.validators import validate_string

export_bp = Blueprint("export", __name__, url_prefix="/api/export")


@export_bp.route("", methods=["GET"])
def list_formats():
    """
    GET /api/export

    Get list of available export formats.

    Returns:
        {
            "status": "success",
            "data": {
                "formats": [
                    {
                        "format": "scorecard_summary",
                        "filename": "scorecard_summary.csv",
                        "description": "Scorecard summary (all countries)"
                    },
                    ...
                ],
                "count": 3
            }
        }
    """
    result = get_available_formats()
    return success_response(result)


@export_bp.route("/<format_id>", methods=["GET"])
@optional_api_key
@limiter.limit(rate_limit_export)
def download_export(format_id: str):
    """
    GET /api/export/:format

    Download dataset in specified format.

    Path parameters:
        - format_id: Export format (e.g., 'scorecard_summary', 'tags_summary')

    Query parameters:
        - version: Tag version (for tags_summary only)

    Rate limiting:
        - Public: 20 requests/hour
        - Authenticated: 200 requests/hour

    Returns:
        CSV file download with appropriate headers
    """
    # Validate format_id
    format_id = validate_string(format_id, "format", max_length=50)

    # Get query parameters
    version = request.args.get("version")
    kwargs = {}

    if version:
        kwargs["version"] = validate_string(version, "version", max_length=50)

    try:
        # Generate export
        csv_content, filename, content_type = generate_export(format_id, **kwargs)

        # Return as downloadable file
        return Response(
            csv_content,
            mimetype=content_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )

    except ValueError as e:
        raise APIError(message=str(e), status_code=400, error_code="INVALID_FORMAT")
