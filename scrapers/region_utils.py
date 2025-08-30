"""
Region Utilities
----------------
Helpers for normalizing region names (Africa, MENA, etc.).
"""

# Example normalization dictionary
REGION_NORMALIZATION = {
    "Sub-Saharan Africa": "Africa",
    "SSA": "Africa",
    "North Africa": "Africa",
    "Middle East and North Africa": "MENA",
    "Latin America and the Caribbean": "Americas",
    "European Union": "Europe",
}


def normalize_region(region_raw):
    """
    Normalize region names but preserve the raw value.
    Returns (region_raw, normalized).
    """
    if not region_raw:
        return None, None
    region_clean = region_raw.strip()
    normalized = REGION_NORMALIZATION.get(region_clean, region_clean)
    return region_raw, normalized
