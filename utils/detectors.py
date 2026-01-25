# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights
# SPDX-License-Identifier: MIT

"""
Detectors
---------
Helpers to infer country and region codes from filenames, URLs, or text content.
"""

import json
import os
import re

from scrapers import country_utils, region_utils

# Load country names and ISO2 codes
COUNTRY_FILE = os.path.join("configs", "filters", "countries", "countries_iso2.json")
with open(COUNTRY_FILE, "r", encoding="utf-8") as f:
    ISO_MAP = json.load(f)
ISO_LOWER = {k.lower(): v for k, v in ISO_MAP.items()}


def detect_country_region(filename=None, url_key=None, text=None):
    """
    Try to infer (country_name, iso_code, regions_list) from filename, url_key, or text.
    Priority: filename > url_key > text scan.
    """

    # 1. From filename (look for iso2 or country name)
    if filename:
        # Match ISO2 code like "_KE_" or "-NG-"
        match = re.search(r"[_\-]([A-Z]{2})[_\-\.]", filename)
        if match:
            iso = match.group(1)
            name = country_utils.get_country_from_iso(iso)
            if name:
                return name, iso, region_utils.get_regions_for_country(iso)

        # Match country name
        for cname, iso in ISO_LOWER.items():
            if cname in filename.lower():
                return cname.title(), iso, region_utils.get_regions_for_country(iso)

    # 2. From url_key (like "upr_kenya_index")
    if url_key:
        for cname, iso in ISO_LOWER.items():
            if cname in url_key.lower():
                return cname.title(), iso, region_utils.get_regions_for_country(iso)

    # 3. From text (basic scan for country names)
    if text:
        for cname, iso in ISO_LOWER.items():
            if re.search(rf"\b{re.escape(cname)}\b", text, flags=re.IGNORECASE):
                return cname.title(), iso, region_utils.get_regions_for_country(iso)

    return None, None, []
