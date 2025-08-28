"""
JSON Normalizer
---------------
Normalizes metadata and processed document JSON records.
Preserves _raw fields alongside normalized ones.
"""

import re
from processors.logger import get_logger

logger = get_logger("json_normalizer")

# Example mapping for region names
REGION_NORMALIZATION = {
    "Sub-Saharan Africa": "Africa",
    "SSA": "Africa",
    "Middle East and North Africa": "MENA",
    "North Africa": "Africa"
}

def normalize_region(region_raw):
    """Normalize region names but preserve the raw value too."""
    if not region_raw:
        return None, None
    for key, val in REGION_NORMALIZATION.items():
        if region_raw.strip().lower() == key.lower():
            return region_raw, val
    return region_raw, region_raw  # if no mapping, keep as-is

def normalize_country(country_raw):
    """Basic country name normalization (placeholder)."""
    if not country_raw:
        return None, None
    # Example: strip extra spaces, unify case
    cleaned = re.sub(r"\s+", " ", country_raw).strip()
    return country_raw, cleaned

def normalize_document(doc):
    """
    Takes a document dict, normalizes fields while keeping _raw.
    Example:
      input: {"country": "Sub-Saharan Africa", ...}
      output: {
        "country_raw": "Sub-Saharan Africa",
        "country": "Africa",
        ...
      }
    """
    if "region" in doc:
        doc["region_raw"], doc["region"] = normalize_region(doc["region"])
    if "country" in doc:
        doc["country_raw"], doc["country"] = normalize_country(doc["country"])
    return doc
