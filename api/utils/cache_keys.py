"""
Cache key generators for Flask-Caching

Provides consistent cache key generation for service functions.
"""


def make_cache_key_documents(filters, page, per_page, sort_by, sort_order):
    """
    Generate cache key for documents list

    Args:
        filters: Dictionary of filter criteria
        page: Page number
        per_page: Items per page
        sort_by: Sort field
        sort_order: Sort direction

    Returns:
        Cache key string
    """
    # Sort filters for consistent key generation
    filter_str = "_".join(
        f"{k}={v}" for k, v in sorted(filters.items()) if v is not None
    )

    return f"documents:list:{filter_str}:p{page}:pp{per_page}:s{sort_by}:{sort_order}"


def make_cache_key_document(doc_id):
    """Generate cache key for single document"""
    return f"documents:detail:{doc_id}"


def make_cache_key_scorecard_summary(region, page, per_page):
    """Generate cache key for scorecard summary"""
    region_str = region or "all"
    return f"scorecard:summary:{region_str}:p{page}:pp{per_page}"


def make_cache_key_country(country):
    """Generate cache key for country scorecard"""
    return f"scorecard:country:{country.lower()}"


def make_cache_key_indicator_stats():
    """Generate cache key for indicator statistics"""
    return "scorecard:indicator_stats"
