"""
Scorecard Loader & Processor
----------------------------
Reads scorecard_main.xlsx, normalizes country names, and provides
lookup functions for enriching metadata with scorecard indicators.
"""

import os
import re
from typing import Any, Dict, List, Optional

import pandas as pd

from processors.logger import get_logger
from scrapers.country_utils import normalize_country

SCORECARD_FILE = os.path.join(
    os.path.dirname(__file__), "..", "data", "scorecard", "scorecard_main.xlsx"
)

# Indicator columns (value + source pairs)
INDICATOR_COLUMNS = [
    ("AI_Policy_Status", "AI_Policy_Status_Source"),
    ("Data_Protection_Law", "Data_Protection_Law_Source"),
    ("Children_Data_Safeguards", "Children_Data_Safeguards_Source"),
    ("SOGI_Sensitive_Data", "SOGI_Sensitive_Data_Source"),
    ("DPA_Independence", "DPA_Independence_Source"),
    ("DPIA_Required_High_Risk_AI", "DPIA_Required_High_Risk_AI_Source"),
    ("LGBTQ_Legal_Status", "LGBTQ_Legal_Status_Source"),
    ("Promotion_Propaganda_Offences", "Promotion_Propaganda_Offences_Source"),
    ("COP_Strategy", "COP_Strategy_Source"),
    ("SIM_Biometric_ID_Linkage", "SIM_Biometric_ID_Linkage_Source"),
]

# Cache for loaded scorecard
_scorecard_cache: Optional[pd.DataFrame] = None
_scorecard_by_country: Dict[str, Dict[str, Any]] = {}


def load_scorecard(filepath: str = None, force_reload: bool = False) -> pd.DataFrame:
    """
    Load scorecard Excel file into a DataFrame.
    Caches result for repeated calls.

    Args:
        filepath: Path to scorecard Excel file (default: scorecard_main.xlsx)
        force_reload: Force reload from disk even if cached

    Returns:
        DataFrame with scorecard data
    """
    global _scorecard_cache

    logger = get_logger("scorecard")
    filepath = filepath or SCORECARD_FILE

    if _scorecard_cache is not None and not force_reload:
        return _scorecard_cache

    if not os.path.exists(filepath):
        logger.error(f"Scorecard file not found: {filepath}")
        raise FileNotFoundError(f"Scorecard file not found: {filepath}")

    logger.info(f"Loading scorecard from {filepath}")
    df = pd.read_excel(filepath, sheet_name="Sheet1")

    # Clean column names
    df.columns = df.columns.str.strip()

    # Drop duplicate RowNumber column if present
    if "RowNumber.1" in df.columns:
        df = df.drop(columns=["RowNumber.1"])

    # Normalize country names (compute once, unpack both values)
    def normalize_and_unpack(country_name):
        if pd.notna(country_name):
            _, normalized, iso = normalize_country(str(country_name))
            return pd.Series([normalized, iso])
        return pd.Series([None, None])

    df[["Country_Normalized", "Country_ISO"]] = df["Country"].apply(
        normalize_and_unpack
    )

    _scorecard_cache = df
    _build_country_index(df)

    logger.info(f"Loaded {len(df)} countries from scorecard")
    return df


def _build_country_index(df: pd.DataFrame) -> None:
    """Build lookup index by normalized country name and ISO code."""
    global _scorecard_by_country
    _scorecard_by_country = {}

    for _, row in df.iterrows():
        record = row.to_dict()

        # Index by original name (lowercase)
        if pd.notna(row["Country"]):
            _scorecard_by_country[row["Country"].lower()] = record

        # Index by normalized name (lowercase)
        if pd.notna(row.get("Country_Normalized")):
            _scorecard_by_country[row["Country_Normalized"].lower()] = record

        # Index by ISO code
        if pd.notna(row.get("Country_ISO")):
            _scorecard_by_country[row["Country_ISO"].lower()] = record


def get_country_scorecard(country: str) -> Optional[Dict[str, Any]]:
    """
    Look up scorecard data for a country.

    Args:
        country: Country name, normalized name, or ISO code

    Returns:
        Dictionary with all scorecard fields, or None if not found
    """
    if not _scorecard_by_country:
        load_scorecard()

    if not country:
        return None

    key = country.lower().strip()
    return _scorecard_by_country.get(key)


def get_indicator(country: str, indicator: str) -> Optional[Dict[str, str]]:
    """
    Get a specific indicator for a country.

    Args:
        country: Country name or ISO code
        indicator: Indicator name (e.g., "AI_Policy_Status")

    Returns:
        Dict with 'value' and 'source', or None
    """
    record = get_country_scorecard(country)
    if not record:
        return None

    source_col = f"{indicator}_Source"
    if indicator in record:
        return {
            "value": record.get(indicator),
            "source": record.get(source_col),
        }
    return None


def get_all_indicators(country: str) -> Optional[Dict[str, Dict[str, str]]]:
    """
    Get all indicators for a country.

    Args:
        country: Country name or ISO code

    Returns:
        Dict mapping indicator name to {value, source}
    """
    record = get_country_scorecard(country)
    if not record:
        return None

    indicators = {}
    for value_col, source_col in INDICATOR_COLUMNS:
        if value_col in record:
            indicators[value_col] = {
                "value": record.get(value_col),
                "source": record.get(source_col),
            }
    return indicators


def extract_all_source_urls() -> List[Dict[str, Any]]:
    """
    Extract all source URLs from the scorecard for validation.

    Returns:
        List of dicts with country, indicator, url
    """
    df = load_scorecard()
    urls = []

    for _, row in df.iterrows():
        country = row.get("Country", "Unknown")
        for _, source_col in INDICATOR_COLUMNS:
            source_val = row.get(source_col)
            if pd.notna(source_val) and source_val:
                # Split multiple URLs (often separated by ; or newlines)
                for url in re.split(r"[;\n]", str(source_val)):
                    url = url.strip()
                    if url.startswith("http"):
                        urls.append(
                            {
                                "country": country,
                                "indicator": source_col.replace("_Source", ""),
                                "url": url,
                            }
                        )

    return urls


def get_countries_list() -> List[str]:
    """Get list of all countries in the scorecard."""
    df = load_scorecard()
    return df["Country"].dropna().tolist()


def get_regions() -> Dict[str, List[str]]:
    """
    Get countries grouped by region.

    Returns:
        Dict mapping region to list of countries
    """
    df = load_scorecard()
    regions = {}

    for _, row in df.iterrows():
        region = row.get("Region - Broad")
        country = row.get("Country")

        if pd.notna(region) and pd.notna(country):
            if region not in regions:
                regions[region] = []
            regions[region].append(country)

    return regions


def scorecard_to_dict() -> Dict[str, Dict[str, Any]]:
    """
    Export entire scorecard as a dictionary keyed by country.

    Returns:
        Dict mapping country name to full scorecard record
    """
    df = load_scorecard()
    return {
        row["Country"]: row.to_dict()
        for _, row in df.iterrows()
        if pd.notna(row.get("Country"))
    }
