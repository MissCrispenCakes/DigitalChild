"""
Metadata service layer

Provides functions for loading, filtering, and paginating document metadata.
Wraps the metadata.json file with caching and filtering logic.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional

from flask import current_app

from api.middleware.error_handlers import NotFoundError

# In-memory cache for metadata
_metadata_cache = {"data": None, "mtime": None}


def load_metadata(force_reload: bool = False) -> Dict:
    """
    Load metadata.json with file modification time caching

    Args:
        force_reload: Force reload from disk, ignoring cache

    Returns:
        Metadata dictionary with "documents" key

    Raises:
        FileNotFoundError: If metadata file doesn't exist
    """
    metadata_file = Path(current_app.config["METADATA_FILE"])

    if not metadata_file.exists():
        raise FileNotFoundError(f"Metadata file not found: {metadata_file}")

    # Check if cache is valid
    current_mtime = metadata_file.stat().st_mtime

    if (
        not force_reload
        and _metadata_cache["data"] is not None
        and _metadata_cache["mtime"] == current_mtime
    ):
        return _metadata_cache["data"]

    # Load from disk
    with open(metadata_file, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    # Update cache
    _metadata_cache["data"] = metadata
    _metadata_cache["mtime"] = current_mtime

    current_app.logger.debug(
        f"Loaded metadata: {len(metadata.get('documents', []))} documents"
    )

    return metadata


def get_documents(
    filters: Optional[Dict] = None,
    page: int = 1,
    per_page: int = 20,
    sort_by: str = "last_processed",
    sort_order: str = "desc",
) -> Dict:
    """
    Get filtered and paginated list of documents

    Args:
        filters: Dictionary of filter criteria (country, region, tags, year, etc.)
        page: Page number (1-indexed)
        per_page: Items per page
        sort_by: Field to sort by
        sort_order: "asc" or "desc"

    Returns:
        Dictionary with "documents" and "pagination" keys
    """
    metadata = load_metadata()
    docs = metadata.get("documents", [])

    # Apply filters
    if filters:
        docs = _apply_filters(docs, filters)

    # Apply sorting
    docs = _apply_sorting(docs, sort_by, sort_order)

    # Calculate pagination
    total = len(docs)
    start = (page - 1) * per_page
    end = start + per_page

    return {
        "documents": docs[start:end],
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": (total + per_page - 1) // per_page,
            "has_next": end < total,
            "has_prev": page > 1,
        },
    }


def get_document(doc_id: str) -> Dict:
    """
    Get single document by ID

    Args:
        doc_id: Document ID

    Returns:
        Document dictionary

    Raises:
        NotFoundError: If document not found
    """
    metadata = load_metadata()
    docs = metadata.get("documents", [])

    for doc in docs:
        if doc.get("id") == doc_id:
            return doc

    raise NotFoundError(f"Document not found: {doc_id}")


def get_metadata_stats() -> Dict:
    """
    Get statistics about document metadata

    Returns:
        Dictionary with counts and breakdowns
    """
    metadata = load_metadata()
    docs = metadata.get("documents", [])

    # Count by source (convert None to string "unknown")
    sources = {}
    for doc in docs:
        source = doc.get("source") or "unknown"
        sources[source] = sources.get(source, 0) + 1

    # Count by region (convert None to string "unknown")
    regions = {}
    for doc in docs:
        region = doc.get("region") or "unknown"
        regions[region] = regions.get(region, 0) + 1

    # Count by doc type (convert None to string "unknown")
    doc_types = {}
    for doc in docs:
        doc_type = doc.get("doc_type") or "unknown"
        doc_types[doc_type] = doc_types.get(doc_type, 0) + 1

    # Year range (handle empty list)
    years = [doc.get("year") for doc in docs if doc.get("year")]
    year_range = (
        {"min": min(years), "max": max(years)} if years else {"min": None, "max": None}
    )

    return {
        "total": len(docs),
        "by_source": sources,
        "by_region": regions,
        "by_doc_type": doc_types,
        "year_range": year_range,
    }


def _apply_filters(docs: List[Dict], filters: Dict) -> List[Dict]:
    """
    Apply filter criteria to document list

    Args:
        docs: List of documents
        filters: Filter criteria

    Returns:
        Filtered list of documents
    """
    filtered = docs

    # Filter by country
    if filters.get("country"):
        country = filters["country"]
        filtered = [
            d
            for d in filtered
            if d.get("country") == country or d.get("country_raw") == country
        ]

    # Filter by region
    if filters.get("region"):
        region = filters["region"]
        filtered = [
            d
            for d in filtered
            if d.get("region") == region or d.get("region_raw") == region
        ]

    # Filter by source
    if filters.get("source"):
        source = filters["source"]
        filtered = [d for d in filtered if d.get("source") == source]

    # Filter by doc_type
    if filters.get("doc_type"):
        doc_type = filters["doc_type"]
        filtered = [d for d in filtered if d.get("doc_type") == doc_type]

    # Filter by year
    if filters.get("year"):
        year = int(filters["year"])
        filtered = [d for d in filtered if d.get("year") == year]

    # Filter by year range
    if filters.get("year_min"):
        year_min = int(filters["year_min"])
        filtered = [d for d in filtered if d.get("year") and d["year"] >= year_min]

    if filters.get("year_max"):
        year_max = int(filters["year_max"])
        filtered = [d for d in filtered if d.get("year") and d["year"] <= year_max]

    # Filter by tags
    if filters.get("tags"):
        # Tags can be comma-separated
        required_tags = (
            filters["tags"].split(",")
            if isinstance(filters["tags"], str)
            else filters["tags"]
        )
        filtered = _filter_by_tags(filtered, required_tags)

    return filtered


def _filter_by_tags(docs: List[Dict], required_tags: List[str]) -> List[Dict]:
    """
    Filter documents by required tags

    Args:
        docs: List of documents
        required_tags: List of tag names to match

    Returns:
        Documents that have all required tags
    """
    result = []

    for doc in docs:
        tags_history = doc.get("tags_history", [])
        if not tags_history:
            continue

        # Get latest tags
        latest_tags = tags_history[-1].get("tags", [])

        # Check if all required tags are present
        if all(tag in latest_tags for tag in required_tags):
            result.append(doc)

    return result


def _apply_sorting(docs: List[Dict], sort_by: str, sort_order: str) -> List[Dict]:
    """
    Sort documents by specified field

    Args:
        docs: List of documents
        sort_by: Field to sort by
        sort_order: "asc" or "desc"

    Returns:
        Sorted list of documents
    """
    reverse = sort_order == "desc"

    # Handle None values in sorting
    def sort_key(doc):
        value = doc.get(sort_by)
        # Put None values at the end by using a tuple (sort_order, value)
        # Python sorts tuples element by element
        if value is None:
            # None sorts last
            return (1, "")
        else:
            # Real values sort first
            return (0, value)

    try:
        return sorted(docs, key=sort_key, reverse=reverse)
    except Exception as e:
        current_app.logger.warning(f"Sorting failed: {e}, returning unsorted")
        return docs
