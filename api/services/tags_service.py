# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights
# SPDX-License-Identifier: MIT

"""
Tags service layer

Provides tag frequency analysis with filtering by version, country,
region, and year. Wraps metadata processing with caching.
"""

import json
from collections import Counter
from typing import Dict, List, Optional

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


def get_available_versions() -> List[str]:
    """
    Get list of available tag versions

    Returns:
        List of version identifiers (e.g., ['tags_v1', 'tags_v2', 'tags_v3'])
    """
    metadata = load_metadata()
    versions = set()

    for doc in metadata.get("documents", []):
        for tag_entry in doc.get("tags_history", []):
            version = tag_entry.get("version")
            if version:
                versions.add(version)

    return sorted(list(versions))


def get_tag_frequency(
    version: Optional[str] = None,
    country: Optional[str] = None,
    region: Optional[str] = None,
    year: Optional[int] = None,
    year_min: Optional[int] = None,
    year_max: Optional[int] = None,
) -> Dict:
    """
    Calculate tag frequency with optional filters

    Args:
        version: Tag version to analyze (e.g., 'tags_v3')
        country: Filter by country name
        region: Filter by region name
        year: Filter by specific year
        year_min: Filter by minimum year (inclusive)
        year_max: Filter by maximum year (inclusive)

    Returns:
        {
            "tags": [
                {"tag": "AI", "count": 42, "percentage": 45.5},
                {"tag": "ChildRights", "count": 38, "percentage": 41.3},
                ...
            ],
            "total_documents": 92,
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

    if year:
        filtered_docs = [d for d in filtered_docs if d.get("year") == year]

    if year_min:
        filtered_docs = [
            d for d in filtered_docs if d.get("year") and d.get("year") >= year_min
        ]

    if year_max:
        filtered_docs = [
            d for d in filtered_docs if d.get("year") and d.get("year") <= year_max
        ]

    # Extract tags from filtered documents
    tag_counter = Counter()

    for doc in filtered_docs:
        tags_history = doc.get("tags_history", [])

        # If version specified, only use tags from that version
        if version:
            for tag_entry in tags_history:
                if tag_entry.get("version") == version:
                    tags = tag_entry.get("tags", [])
                    tag_counter.update(tags)
        else:
            # Use latest tags (most recent entry)
            if tags_history:
                latest_tags = tags_history[-1].get("tags", [])
                tag_counter.update(latest_tags)

    # Calculate percentages
    total_docs = len(filtered_docs)
    tag_list = []

    for tag, count in tag_counter.most_common():
        percentage = round((count / total_docs) * 100, 2) if total_docs > 0 else 0
        tag_list.append({"tag": tag, "count": count, "percentage": percentage})

    # Build filters summary
    filters_applied = {}
    if version:
        filters_applied["version"] = version
    if country:
        filters_applied["country"] = country
    if region:
        filters_applied["region"] = region
    if year:
        filters_applied["year"] = year
    if year_min:
        filters_applied["year_min"] = year_min
    if year_max:
        filters_applied["year_max"] = year_max

    return {
        "tags": tag_list,
        "total_documents": total_docs,
        "filters_applied": filters_applied,
    }
