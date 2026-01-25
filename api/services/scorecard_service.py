# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights
# SPDX-License-Identifier: MIT

"""
Scorecard service layer

Wraps existing scorecard functions from processors/scorecard.py
with caching and API-friendly formatting.
Works with pandas DataFrames returned by load_scorecard().
"""

from typing import Dict, Optional

import pandas as pd
from flask import current_app

from api.middleware.error_handlers import NotFoundError

# Import existing scorecard functions
try:
    from processors.scorecard import (
        get_all_indicators,
        get_country_scorecard,
        load_scorecard,
    )
except ImportError:
    current_app.logger.warning(
        "processors.scorecard not available, using stub functions"
    )

    # Stub functions for testing without processors
    def load_scorecard():
        return pd.DataFrame()

    def get_country_scorecard(country):
        return None

    def get_all_indicators(country):
        return {}


def get_scorecard_summary(
    region: Optional[str] = None, page: int = 1, per_page: int = 20
) -> Dict:
    """
    Get summary of all countries in scorecard

    Args:
        region: Filter by region (optional)
        page: Page number (1-indexed)
        per_page: Items per page

    Returns:
        Dictionary with "countries" and "pagination" keys
    """
    df = load_scorecard()  # Returns pandas DataFrame

    # Filter by region if specified
    if region and "Region - Broad" in df.columns:
        df = df[df["Region - Broad"].str.lower() == region.lower()]

    # Calculate pagination
    total = len(df)
    start = (page - 1) * per_page
    end = start + per_page

    # Get page of data
    page_df = df.iloc[start:end]

    # Format countries for API
    countries = []
    for _, row in page_df.iterrows():
        countries.append(
            {
                "country": row.get("Country"),
                "region": row.get("Region - Broad"),
                "region_specific": row.get("Region - Specific"),
                "indicator_count": _count_indicators(row),
            }
        )

    return {
        "countries": countries,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": (total + per_page - 1) // per_page,
            "has_next": end < total,
            "has_prev": page > 1,
        },
    }


def get_country_details(country: str) -> Dict:
    """
    Get full scorecard details for a country

    Args:
        country: Country name

    Returns:
        Dictionary with country info and all indicators

    Raises:
        NotFoundError: If country not found
    """
    scorecard_row = get_country_scorecard(country)

    if scorecard_row is None:
        raise NotFoundError(f"Country not found in scorecard: {country}")

    indicators = get_all_indicators(country)

    # get_country_scorecard returns a pandas Series or dict
    if hasattr(scorecard_row, "get"):
        # It's a Series or dict
        return {
            "country": scorecard_row.get("Country"),
            "region": scorecard_row.get("Region - Broad"),
            "region_specific": scorecard_row.get("Region - Specific"),
            "indicators": indicators,
        }
    else:
        # Fallback
        return {
            "country": country,
            "region": "Unknown",
            "region_specific": "Unknown",
            "indicators": indicators,
        }


def get_indicator_statistics() -> Dict:
    """
    Get statistics about indicator values across all countries

    Returns:
        Dictionary with value distribution for each indicator
    """
    df = load_scorecard()

    # Define indicator columns (excluding metadata columns)
    metadata_cols = [
        "RowNumber",
        "Country",
        "Region - Broad",
        "Region - Specific",
        "Country_Normalized",
        "Country_ISO",
    ]
    indicator_cols = [
        col
        for col in df.columns
        if col not in metadata_cols and not col.endswith("_Source")
    ]

    stats = {}

    for indicator in indicator_cols:
        # Get value counts for this indicator
        value_counts = df[indicator].value_counts().to_dict()

        stats[indicator] = {
            "total_countries": len(df),
            "value_distribution": value_counts,
        }

    return stats


def get_scorecard_stats() -> Dict:
    """
    Get high-level statistics about scorecard data

    Returns:
        Dictionary with counts and coverage info
    """
    df = load_scorecard()

    # Count by region (filter out None/NaN values)
    region_counts = {}
    if "Region - Broad" in df.columns:
        # Filter out NaN values before counting
        region_series = df["Region - Broad"].dropna()
        region_counts = region_series.value_counts().to_dict()
        # Convert any remaining None keys to strings
        region_counts = {str(k): v for k, v in region_counts.items() if k is not None}

    return {
        "total_countries": len(df),
        "by_region": region_counts,
    }


def _count_indicators(row) -> int:
    """
    Count how many indicators have non-empty values

    Args:
        row: Pandas Series representing a scorecard row

    Returns:
        Count of populated indicators
    """
    metadata_cols = [
        "RowNumber",
        "Country",
        "Region - Broad",
        "Region - Specific",
        "Country_Normalized",
        "Country_ISO",
    ]
    count = 0

    for key in row.index:
        # Skip metadata and source columns
        if key not in metadata_cols and not key.endswith("_Source"):
            value = row[key]
            # Count if value is not null, not empty string, and not "Unknown"
            if pd.notna(value) and str(value).strip() and str(value) != "Unknown":
                count += 1

    return count
