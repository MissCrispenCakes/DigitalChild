# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights
# SPDX-License-Identifier: MIT

"""
Timeline service layer

Provides temporal analysis of tags over time with year × tag matrices.
"""

import json
from collections import defaultdict
from typing import Dict, Optional

from flask import current_app


def load_metadata() -> Dict:
    """Load metadata from JSON file"""
    metadata_file = current_app.config["METADATA_FILE"]
    try:
        with open(metadata_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        current_app.logger.error(f"Metadata file not found: {metadata_file}")
        return {"documents": []}


def get_tags_timeline(
    version: Optional[str] = None,
    year_min: Optional[int] = None,
    year_max: Optional[int] = None,
    country: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict:
    """
    Get tags over time analysis

    Args:
        version: Tag version to analyze (e.g., 'tags_v3')
        year_min: Minimum year (inclusive)
        year_max: Maximum year (inclusive)
        country: Filter by country name
        region: Filter by region name

    Returns:
        {
            "timeline": [
                {"year": 2020, "tags": {"AI": 5, "Privacy": 3}},
                {"year": 2021, "tags": {"AI": 8, "Privacy": 7}},
                ...
            ],
            "years": [2020, 2021, 2022, ...],
            "all_tags": ["AI", "Privacy", "ChildRights", ...],
            "total_documents": 45,
            "filters_applied": {...}
        }
    """
    metadata = load_metadata()
    documents = metadata.get("documents", [])

    # Apply document-level filters
    filtered_docs = documents

    if country:
        filtered_docs = [
            d for d in filtered_docs if d.get("country", "").lower() == country.lower()
        ]

    if region:
        filtered_docs = [
            d for d in filtered_docs if d.get("region", "").lower() == region.lower()
        ]

    # Build year × tag matrix
    year_tag_counts = defaultdict(lambda: defaultdict(int))
    all_tags = set()
    years = set()

    for doc in filtered_docs:
        doc_year = doc.get("year")

        # Skip documents without year
        if not doc_year:
            continue

        # Apply year filters
        if year_min and doc_year < year_min:
            continue
        if year_max and doc_year > year_max:
            continue

        years.add(doc_year)

        # Extract tags
        tags_history = doc.get("tags_history", [])

        if version:
            # Use specific version
            for tag_entry in tags_history:
                if tag_entry.get("version") == version:
                    tags = tag_entry.get("tags", [])
                    for tag in tags:
                        year_tag_counts[doc_year][tag] += 1
                        all_tags.add(tag)
        else:
            # Use latest tags
            if tags_history:
                latest_tags = tags_history[-1].get("tags", [])
                for tag in latest_tags:
                    year_tag_counts[doc_year][tag] += 1
                    all_tags.add(tag)

    # Build timeline array
    timeline = []
    sorted_years = sorted(years)

    for year in sorted_years:
        timeline.append({"year": year, "tags": dict(year_tag_counts[year])})

    # Build filters summary
    filters_applied = {}
    if version:
        filters_applied["version"] = version
    if country:
        filters_applied["country"] = country
    if region:
        filters_applied["region"] = region
    if year_min:
        filters_applied["year_min"] = year_min
    if year_max:
        filters_applied["year_max"] = year_max

    return {
        "timeline": timeline,
        "years": sorted_years,
        "all_tags": sorted(list(all_tags)),
        "total_documents": len(filtered_docs),
        "filters_applied": filters_applied,
    }
