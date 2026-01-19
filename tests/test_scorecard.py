"""
Tests for Scorecard Modules
---------------------------
Tests for scorecard loading, validation, enrichment, diff checking, and export.
"""

import os
from unittest.mock import Mock, patch

# Test imports
from processors.scorecard import (
    INDICATOR_COLUMNS,
    extract_all_source_urls,
    get_all_indicators,
    get_countries_list,
    get_country_scorecard,
    get_indicator,
    get_regions,
    load_scorecard,
)


class TestScorecardLoader:
    """Tests for scorecard.py loader module."""

    def test_load_scorecard_returns_dataframe(self):
        """Test that load_scorecard returns a DataFrame."""
        import pandas as pd

        df = load_scorecard(force_reload=True)
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0

    def test_load_scorecard_has_required_columns(self):
        """Test that loaded scorecard has expected columns."""
        df = load_scorecard()
        assert "Country" in df.columns
        assert "Region - Broad" in df.columns
        # Check at least one indicator
        assert "AI_Policy_Status" in df.columns

    def test_get_country_scorecard_found(self):
        """Test looking up a country that exists."""
        result = get_country_scorecard("Afghanistan")
        assert result is not None
        assert result.get("Country") == "Afghanistan"

    def test_get_country_scorecard_case_insensitive(self):
        """Test case-insensitive country lookup."""
        result = get_country_scorecard("AFGHANISTAN")
        assert result is not None
        assert result.get("Country") == "Afghanistan"

    def test_get_country_scorecard_not_found(self):
        """Test looking up a country that doesn't exist."""
        result = get_country_scorecard("NotARealCountry")
        assert result is None

    def test_get_indicator(self):
        """Test getting a specific indicator for a country."""
        result = get_indicator("Albania", "AI_Policy_Status")
        assert result is not None
        assert "value" in result
        assert "source" in result

    def test_get_all_indicators(self):
        """Test getting all indicators for a country."""
        result = get_all_indicators("Albania")
        assert result is not None
        assert len(result) == len(INDICATOR_COLUMNS)
        assert "AI_Policy_Status" in result

    def test_extract_all_source_urls(self):
        """Test extracting all source URLs."""
        urls = extract_all_source_urls()
        assert len(urls) > 0
        # Check structure
        assert "country" in urls[0]
        assert "indicator" in urls[0]
        assert "url" in urls[0]
        # Check URLs are valid
        for item in urls[:10]:
            assert item["url"].startswith("http")

    def test_get_countries_list(self):
        """Test getting list of countries."""
        countries = get_countries_list()
        assert len(countries) > 100  # Should have many countries
        assert "Afghanistan" in countries

    def test_get_regions(self):
        """Test getting countries grouped by region."""
        regions = get_regions()
        assert isinstance(regions, dict)
        # Africa should be a region with countries
        if "Africa" in regions:
            assert len(regions["Africa"]) > 0


class TestScorecardEnricher:
    """Tests for scorecard_enricher.py module."""

    def test_enrich_document_with_country(self):
        """Test enriching a document that has a country."""
        from processors.scorecard_enricher import enrich_document

        doc = {"id": "test-1", "country": "Albania"}
        enriched = enrich_document(doc)

        assert "scorecard" in enriched
        assert enriched["scorecard"]["matched_country"] == "Albania"

    def test_enrich_document_without_country(self):
        """Test enriching a document without a country field."""
        from processors.scorecard_enricher import enrich_document

        doc = {"id": "test-2"}
        enriched = enrich_document(doc)

        # Should still return doc, just without scorecard
        assert enriched["id"] == "test-2"

    def test_enrich_document_country_not_in_scorecard(self):
        """Test enriching a document with unknown country."""
        from processors.scorecard_enricher import enrich_document

        doc = {"id": "test-3", "country": "NotARealCountry"}
        enriched = enrich_document(doc)

        # scorecard field may be absent or empty
        assert enriched["id"] == "test-3"


class TestScorecardExport:
    """Tests for scorecard_export.py module."""

    def test_export_summary_csv(self, tmp_path):
        """Test exporting scorecard summary to CSV."""
        from processors.scorecard_export import ScorecardExporter

        filepath = str(tmp_path / "test_summary.csv")
        exporter = ScorecardExporter()
        result = exporter.export_summary_csv(filepath)

        assert os.path.exists(result)
        # Check file has content
        with open(result, "r") as f:
            lines = f.readlines()
            assert len(lines) > 1  # Header + data

    def test_export_sources_csv(self, tmp_path):
        """Test exporting source URLs to CSV."""
        from processors.scorecard_export import ScorecardExporter

        filepath = str(tmp_path / "test_sources.csv")
        exporter = ScorecardExporter()
        result = exporter.export_sources_csv(filepath)
        assert os.path.exists(result)


class TestScorecardValidator:
    """Tests for scorecard_validator.py module."""

    @patch("processors.scorecard_validator.requests.head")
    def test_validate_url_success(self, mock_head):
        """Test validating a URL that works."""
        from processors.scorecard_validator import validate_url

        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.url = "https://www.google.com"
        mock_head.return_value = mock_response

        result = validate_url("https://www.google.com")
        assert result["ok"] is True
        assert result["status_code"] == 200

    @patch("processors.scorecard_validator.requests.head")
    def test_validate_url_broken(self, mock_head):
        """Test validating a URL that doesn't exist."""
        import requests

        from processors.scorecard_validator import validate_url

        # Mock connection error
        mock_head.side_effect = requests.exceptions.ConnectionError(
            "Name or service not known"
        )

        result = validate_url("https://thisdomaindoesnotexist12345.com")
        assert result["ok"] is False
        assert result["error"] is not None

    @patch("processors.scorecard_validator.requests.head")
    def test_validate_url_timeout(self, mock_head):
        """Test validating with timeout."""
        import requests

        from processors.scorecard_validator import validate_url

        # Mock timeout error to test timeout handling (will retry twice)
        mock_head.side_effect = requests.exceptions.Timeout("Request timed out")

        result = validate_url("https://www.example.com", timeout=0.001)
        assert "url" in result
        assert result["error"] == "Timeout"
        assert result["ok"] is False

        # Verify timeout was passed to requests.head (called twice due to retry logic)
        assert mock_head.call_count == 2
        for call in mock_head.call_args_list:
            assert call[1]["timeout"] == 0.001


class TestScorecardDiff:
    """Tests for scorecard_diff.py module."""

    def test_hash_content(self):
        """Test content hashing is consistent."""
        from processors.scorecard_diff import hash_content

        content1 = "Hello World"
        content2 = "Hello World"
        content3 = "Different Content"

        assert hash_content(content1) == hash_content(content2)
        assert hash_content(content1) != hash_content(content3)

    def test_monitored_sources_defined(self):
        """Test that monitored sources are defined."""
        from processors.scorecard_diff import MONITORED_SOURCES

        assert len(MONITORED_SOURCES) > 0
        # Each source should have required fields
        for _key, source in MONITORED_SOURCES.items():
            assert "name" in source or "base_url" in source
