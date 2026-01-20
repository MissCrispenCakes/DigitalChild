"""
Scorecard Export
----------------
Export scorecard data to CSV format for analysis and visualization.
"""

import csv
import os
from typing import Dict

import pandas as pd

from processors.logger import get_logger
from processors.scorecard import (
    INDICATOR_COLUMNS,
    extract_all_source_urls,
    load_scorecard,
)
from processors.validators import PathValidationError, validate_output_path

EXPORT_DIR = os.path.join("data", "exports")

# Extract just the value column names for exports
INDICATOR_COLS = [col[0] for col in INDICATOR_COLUMNS]


class ScorecardExporter:
    """Export scorecard data to various formats."""

    def __init__(self, logger=None):
        self.logger = logger or get_logger("scorecard_export")
        self._df = None

    def _load(self):
        """Lazy load scorecard DataFrame."""
        if self._df is None:
            self._df = load_scorecard()
        return self._df

    def to_dataframe(self):
        """Return scorecard as DataFrame."""
        return self._load()

    def get_all_sources(self):
        """Return all source URLs."""
        return extract_all_source_urls()

    def export_summary_csv(self, filepath: str = None) -> str:
        """
        Export scorecard summary to CSV.
        One row per country, columns for each indicator.
        """
        filepath = filepath or os.path.join(EXPORT_DIR, "scorecard_summary.csv")

        # Validate output path
        try:
            filepath = validate_output_path(filepath)
        except PathValidationError as e:
            self.logger.error(f"Invalid export path: {e}")
            raise

        df = self.to_dataframe()

        # Select relevant columns
        cols = ["Country", "Region - Broad", "Region - Specific"] + INDICATOR_COLS
        export_df = df[[c for c in cols if c in df.columns]].copy()

        export_df.to_csv(filepath, index=False, encoding="utf-8")
        self.logger.info(f"Exported scorecard summary to {filepath}")
        return filepath

    def export_sources_csv(self, filepath: str = None) -> str:
        """
        Export all source URLs to CSV.
        One row per URL with country/indicator context.
        """
        filepath = filepath or os.path.join(EXPORT_DIR, "scorecard_sources.csv")

        # Validate output path
        try:
            filepath = validate_output_path(filepath)
        except PathValidationError as e:
            self.logger.error(f"Invalid export path: {e}")
            raise

        sources = self.get_all_sources()

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["country", "indicator", "url"])
            writer.writeheader()
            writer.writerows(sources)

        self.logger.info(f"Exported {len(sources)} source URLs to {filepath}")
        return filepath

    def export_by_indicator(self, indicator: str, filepath: str = None) -> str:
        """
        Export single indicator for all countries.
        """
        if indicator not in INDICATOR_COLS:
            raise ValueError(f"Unknown indicator: {indicator}")

        filepath = filepath or os.path.join(
            EXPORT_DIR, f"scorecard_{indicator.lower()}.csv"
        )

        # Validate output path
        try:
            filepath = validate_output_path(filepath)
        except PathValidationError as e:
            self.logger.error(f"Invalid export path: {e}")
            raise

        df = self.to_dataframe()
        cols = [
            "Country",
            "Region - Broad",
            "Region - Specific",
            indicator,
            f"{indicator}_Source",
        ]
        export_df = df[[c for c in cols if c in df.columns]].copy()

        export_df.to_csv(filepath, index=False, encoding="utf-8")
        self.logger.info(f"Exported {indicator} to {filepath}")
        return filepath

    def export_by_region(self, region: str, filepath: str = None) -> str:
        """
        Export scorecard for specific region.
        """
        filepath = filepath or os.path.join(
            EXPORT_DIR, f"scorecard_{region.lower().replace(' ', '_')}.csv"
        )

        # Validate output path
        try:
            filepath = validate_output_path(filepath)
        except PathValidationError as e:
            self.logger.error(f"Invalid export path: {e}")
            raise

        df = self.to_dataframe()

        # Filter by region (broad or specific)
        mask = (df["Region - Broad"].str.lower() == region.lower()) | (
            df["Region - Specific"].str.lower() == region.lower()
        )
        export_df = df[mask].copy()

        if export_df.empty:
            self.logger.warning(f"No countries found for region: {region}")
            return None

        cols = ["Country", "Region - Broad", "Region - Specific"] + INDICATOR_COLS
        export_df = export_df[[c for c in cols if c in df.columns]]

        export_df.to_csv(filepath, index=False, encoding="utf-8")
        self.logger.info(
            f"Exported {len(export_df)} countries for region {region} to {filepath}"
        )
        return filepath

    def export_indicator_counts(self, filepath: str = None) -> str:
        """
        Export counts/distribution for each indicator.
        Useful for charts and visualization.
        """
        filepath = filepath or os.path.join(
            EXPORT_DIR, "scorecard_indicator_counts.csv"
        )

        # Validate output path
        try:
            filepath = validate_output_path(filepath)
        except PathValidationError as e:
            self.logger.error(f"Invalid export path: {e}")
            raise

        df = self.to_dataframe()
        rows = []

        for indicator in INDICATOR_COLS:
            if indicator not in df.columns:
                continue

            # Extract status prefix (e.g., "Legal", "None", "Partial", etc.)
            values = df[indicator].dropna().apply(self._extract_status)
            counts = values.value_counts().to_dict()

            for status, count in counts.items():
                rows.append(
                    {
                        "indicator": indicator,
                        "status": status,
                        "count": count,
                    }
                )

        result_df = pd.DataFrame(rows)
        result_df.to_csv(filepath, index=False, encoding="utf-8")
        self.logger.info(f"Exported indicator counts to {filepath}")
        return filepath

    def _extract_status(self, value: str) -> str:
        """Extract status prefix from indicator value."""
        if pd.isna(value):
            return "Unknown"
        value = str(value).strip()
        # Common prefixes
        prefixes = [
            "Legal",
            "Criminalized",
            "Partial",
            "None",
            "Yes",
            "No",
            "In force",
            "Draft",
            "Independent",
            "Moderate",
            "ID mandatory",
            "Biometric mandatory",
            "DPA exists",
            "No DPA",
        ]
        for prefix in prefixes:
            if value.lower().startswith(prefix.lower()):
                return prefix
        # Return first word if no match
        return value.split()[0] if value else "Unknown"

    def export_all(self) -> Dict[str, str]:
        """
        Export all scorecard data to multiple files.
        Returns dict of export type -> filepath.
        """
        exports = {}
        exports["summary"] = self.export_summary_csv()
        exports["sources"] = self.export_sources_csv()
        exports["indicator_counts"] = self.export_indicator_counts()
        return exports


def export_scorecard() -> Dict[str, str]:
    """
    Convenience function to export all scorecard data.
    Returns dict of export type -> filepath.
    """
    exporter = ScorecardExporter()
    return exporter.export_all()


def export_scorecard_summary(filepath: str = None) -> str:
    """Export scorecard summary CSV."""
    exporter = ScorecardExporter()
    return exporter.export_summary_csv(filepath)


def export_summary_csv(filepath: str = None) -> str:
    """Export scorecard summary CSV (wrapper for tests)."""
    exporter = ScorecardExporter()
    return exporter.export_summary_csv(filepath)


def export_sources_csv(filepath: str = None) -> str:
    """Export scorecard sources CSV (wrapper for tests)."""
    exporter = ScorecardExporter()
    return exporter.export_sources_csv(filepath)
