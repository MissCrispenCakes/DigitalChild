"""
Country Utilities
-----------------
Helpers for normalizing country names and mapping to ISO codes.
"""

import re

# Minimal ISO 3166-1 alpha-2 mapping (extend as needed)
ISO_MAP = {
    "Kenya": "KE",
    "Nigeria": "NG",
    "South Africa": "ZA",
    "Uganda": "UG",
    "Ghana": "GH",
    "African Union": "AU"
}


def normalize_country(country_raw):
    """
    Normalize country names and map to ISO alpha-2 code.
    Returns (country_raw, normalized_name, iso_code).
    """
    if not country_raw:
        return None, None, None

    cleaned = re.sub(r"\s+", " ", country_raw).strip().title()

    iso_code = ISO_MAP.get(cleaned)
    return country_raw, cleaned, iso_code
