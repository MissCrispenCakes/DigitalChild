"""
Documents API routes

Provides endpoints for listing and retrieving document metadata.
"""

from flask import Blueprint, current_app, request

from api.extensions import cache
from api.middleware.error_handlers import NotFoundError
from api.services.metadata_service import get_document, get_documents
from api.utils.response import paginated_response, success_response
from api.utils.validators import (
    ValidationError,
    validate_enum,
    validate_page,
    validate_per_page,
    validate_string,
    validate_year,
)

documents_bp = Blueprint("documents", __name__, url_prefix="/api/documents")


@documents_bp.route("", methods=["GET"])
def list_documents():
    """
    List documents with optional filtering and pagination

    Query parameters:
        - country: Filter by country name
        - region: Filter by region
        - source: Filter by source (e.g., "au_policy", "upr")
        - doc_type: Filter by document type
        - tags: Comma-separated list of tags to match
        - year: Filter by specific year
        - year_min: Filter by minimum year
        - year_max: Filter by maximum year
        - page: Page number (default: 1)
        - per_page: Items per page (default: 20, max: 100)
        - sort_by: Field to sort by (default: "last_processed")
        - sort_order: "asc" or "desc" (default: "desc")

    Returns:
        200: Paginated list of documents
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
        filters = {}

        if country := request.args.get("country"):
            filters["country"] = validate_string(country, "country")

        if region := request.args.get("region"):
            filters["region"] = validate_string(region, "region")

        if source := request.args.get("source"):
            filters["source"] = validate_string(source, "source")

        if doc_type := request.args.get("doc_type"):
            filters["doc_type"] = validate_string(doc_type, "doc_type")

        if tags := request.args.get("tags"):
            filters["tags"] = validate_string(tags, "tags")

        if year := request.args.get("year"):
            filters["year"] = validate_year(year)

        if year_min := request.args.get("year_min"):
            filters["year_min"] = validate_year(year_min)

        if year_max := request.args.get("year_max"):
            filters["year_max"] = validate_year(year_max)

        # Validate sorting parameters
        sort_by = validate_enum(
            request.args.get("sort_by", "last_processed"),
            [
                "last_processed",
                "year",
                "country",
                "region",
                "source",
                "doc_type",
                "id",
            ],
            "sort_by",
        )

        sort_order = validate_enum(
            request.args.get("sort_order", "desc"),
            ["asc", "desc"],
            "sort_order",
        )

        # Get documents from service
        result = get_documents(
            filters=filters,
            page=page,
            per_page=per_page,
            sort_by=sort_by,
            sort_order=sort_order,
        )

        # Return paginated response
        return paginated_response(
            items=result["documents"],
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


@documents_bp.route("/<doc_id>", methods=["GET"])
@cache.cached(timeout=900, key_prefix=lambda: f"doc:{request.view_args['doc_id']}")
def get_document_detail(doc_id):
    """
    Get detailed information for a single document

    Path parameters:
        - doc_id: Document ID

    Returns:
        200: Document details
        404: Document not found

    Cache: 15 minutes (documents rarely change)
    """
    try:
        document = get_document(doc_id)
        return success_response(document)

    except NotFoundError as e:
        from api.utils.response import error_response

        return error_response(
            message=str(e.message),
            code="NOT_FOUND",
            status_code=404,
        )
