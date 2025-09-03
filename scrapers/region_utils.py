"""
Region Utilities
----------------
Helpers for normalizing region names/codes and mapping to countries.
"""

import json
import os

# Quick ref and expanded region files
REGION_REF_FILE = os.path.join("configs", "filters", "countries", "regions.json")
REGION_FILE = os.path.join("configs", "filters", "countries", "regions_iso2.json")

with open(REGION_REF_FILE, "r", encoding="utf-8") as f:
    REGION_CODES = json.load(f)  # e.g. {"AFU": "AFU", "GLOBAL": "XX", ...}

with open(REGION_FILE, "r", encoding="utf-8") as f:
    REGIONS = json.load(f)  # expanded regions with "countries" or "ref"


def normalize_region(region_raw: str):
    """
    Normalize region names/codes.
    Returns (raw_input, normalized_code, region_data).
    - region_data comes from regions_iso2.json.
    """
    if not region_raw:
        return None, None, None

    region_clean = region_raw.strip().upper()

    # Direct code match
    if region_clean in REGIONS:
        return region_raw, region_clean, REGIONS[region_clean]

    # Quick ref mapping
    if region_clean in REGION_CODES:
        code = REGION_CODES[region_clean]
        if code in REGIONS:
            return region_raw, code, REGIONS[code]

    return region_raw, None, None


def get_countries_for_region(region_code: str):
    """
    Return list of ISO2 country codes for a region code,
    resolving refs if necessary.
    """
    if not region_code or region_code not in REGIONS:
        return []

    entry = REGIONS[region_code]
    if "countries" in entry:
        return entry["countries"]
    if "ref" in entry:
        return get_countries_for_region(entry["ref"])
    return []


def get_regions_for_country(iso_code: str):
    """
    Reverse lookup: given an ISO2 country code, return all regions that include it.
    Resolves nested refs.
    """
    if not iso_code:
        return []

    iso = iso_code.upper()
    matched = []

    for region_code, entry in REGIONS.items():
        countries = get_countries_for_region(region_code)
        if iso in countries:
            matched.append(region_code)

    return matched
