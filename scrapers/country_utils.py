"""
Country Utilities
-----------------
Helpers for normalizing country names and mapping to ISO codes.
"""

import json
import os
import re

# Path to canonical ISO country list
COUNTRY_FILE = os.path.join("configs", "filters", "countries", "countries_iso2.json")
with open(COUNTRY_FILE, "r", encoding="utf-8") as f:
    ISO_MAP = json.load(f)  # e.g. {"Kenya": "KE", "Nigeria": "NG", ...}

# Lowercase lookup for fuzzy matches
ISO_MAP_LOWER = {k.lower(): v for k, v in ISO_MAP.items()}

# Reverse lookup (ISO2 → Country Name)
ISO_REVERSE = {v: k for k, v in ISO_MAP.items()}


def normalize_country(country_raw: str):
    """
    Normalize country names and map to ISO alpha-2 code.
    Returns (raw_input, normalized_name, iso_code).
    """
    if not country_raw:
        return None, None, None

    cleaned = re.sub(r"\s+", " ", country_raw).strip()

    # Exact match
    if cleaned in ISO_MAP:
        return country_raw, cleaned, ISO_MAP[cleaned]

    # Case-insensitive
    if cleaned.lower() in ISO_MAP_LOWER:
        std_name = [k for k in ISO_MAP if k.lower() == cleaned.lower()][0]
        return country_raw, std_name, ISO_MAP_LOWER[cleaned.lower()]

    # Partial match
    for cname, iso in ISO_MAP_LOWER.items():
        if cleaned.lower() in cname:
            std_name = [k for k, v in ISO_MAP.items() if v == iso][0]
            return country_raw, std_name, iso

    return country_raw, None, None


def get_country_from_iso(iso_code: str):
    """
    Reverse lookup: ISO alpha-2 → Country name.
    Returns country name or None if not found.
    """
    if not iso_code:
        return None
    return ISO_REVERSE.get(iso_code.upper())
