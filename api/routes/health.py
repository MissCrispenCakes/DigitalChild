"""
Health check and info endpoints

Provides endpoints for monitoring API health and getting system information.
"""

import os
from datetime import datetime
from pathlib import Path

from flask import Blueprint, current_app

from api.utils.response import success_response

health_bp = Blueprint("health", __name__, url_prefix="/api")


@health_bp.route("/health", methods=["GET"])
def health_check():
    """
    Health check endpoint

    Returns basic health status of the API.
    Use for monitoring and load balancer health checks.

    Returns:
        200: API is healthy
    """
    return success_response(
        {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "version": current_app.config.get("API_VERSION", "v1"),
        }
    )


@health_bp.route("/info", methods=["GET"])
def system_info():
    """
    System information endpoint

    Returns statistics about available data including document count,
    scorecard coverage, and data freshness.

    Returns:
        200: System information
    """
    from api.services.metadata_service import get_metadata_stats
    from api.services.scorecard_service import get_scorecard_stats

    # Get metadata statistics
    metadata_stats = get_metadata_stats()

    # Get scorecard statistics
    scorecard_stats = get_scorecard_stats()

    # Check data file timestamps
    metadata_file = Path(current_app.config["METADATA_FILE"])
    scorecard_file = Path(current_app.config["SCORECARD_FILE"])

    data_freshness = {}
    if metadata_file.exists():
        data_freshness["metadata_updated"] = datetime.fromtimestamp(
            metadata_file.stat().st_mtime
        ).isoformat() + "Z"

    if scorecard_file.exists():
        data_freshness["scorecard_updated"] = datetime.fromtimestamp(
            scorecard_file.stat().st_mtime
        ).isoformat() + "Z"

    return success_response(
        {
            "version": current_app.config.get("API_VERSION", "v1"),
            "environment": current_app.config.get("FLASK_ENV", "unknown"),
            "documents": metadata_stats,
            "scorecard": scorecard_stats,
            "data_freshness": data_freshness,
        }
    )
