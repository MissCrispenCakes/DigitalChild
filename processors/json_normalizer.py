"""
JSON Normalizer
---------------
Normalizes metadata and processed document JSON records.
Uses country_utils and region_utils for consistency.
"""

from processors.logger import get_logger
from scrapers import country_utils, region_utils

logger = get_logger("json_normalizer")


def normalize_region(region_raw):
    """
    Normalize region names using region_utils.
    Returns (region_raw, normalized_region_code).
    """
    if not region_raw:
        return None, None
    r_raw, region_norm, _ = region_utils.normalize_region(region_raw)
    return r_raw, region_norm


def normalize_country(country_raw):
    """
    Normalize country names using country_utils.
    Returns (country_raw, normalized_name, iso_code).
    """
    if not country_raw:
        return None, None, None
    c_raw, country_norm, iso = country_utils.normalize_country(country_raw)
    return c_raw, country_norm, iso


def normalize_document(doc):
    """
    Normalize a document dict in-place.
    Ensures:
      - country_raw, country, country_iso, country_display
      - region_raw, region, regions_memberships
    """
    if "region" in doc:
        doc["region_raw"], doc["region"] = normalize_region(doc["region"])

    if "country" in doc:
        c_raw, country_norm, iso = normalize_country(doc["country"])
        doc["country_raw"] = c_raw
        doc["country"] = country_norm
        doc["country_iso"] = iso
        doc["country_display"] = (
            country_utils.get_country_from_iso(iso) if iso else None
        )
        doc["regions_memberships"] = (
            region_utils.get_regions_for_country(iso) if iso else []
        )

    return doc
