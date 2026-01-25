# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights
# SPDX-License-Identifier: MIT

"""
Tests for ISO 3166-1 alpha-2 Country Code Mapping
==================================================

Tests the complete ISO mapping for all 194 UN member states.
"""

from utils.iso_mapping import (
    ISO_CODE_TO_COUNTRY,
    ISO_COUNTRY_MAPPING,
    TOTAL_COUNTRIES,
    get_country_name,
    get_iso_code,
    normalize_country_to_iso,
)


class TestISOMapping:
    """Test ISO country code mapping dictionaries."""

    def test_total_countries(self):
        """Test that we have all 194 UN member states."""
        assert TOTAL_COUNTRIES == 194
        assert len(ISO_COUNTRY_MAPPING) == 194
        assert len(ISO_CODE_TO_COUNTRY) == 194

    def test_mapping_completeness(self):
        """Test that forward and reverse mappings are complete."""
        # All countries map to codes
        for country in ISO_COUNTRY_MAPPING:
            assert ISO_COUNTRY_MAPPING[country] is not None
            assert len(ISO_COUNTRY_MAPPING[country]) == 2

        # All codes map back to countries
        for code in ISO_CODE_TO_COUNTRY:
            assert ISO_CODE_TO_COUNTRY[code] is not None

    def test_known_countries(self):
        """Test a sample of well-known countries."""
        test_cases = [
            ("Kenya", "KE"),
            ("Nigeria", "NG"),
            ("South Africa", "ZA"),
            ("Brazil", "BR"),
            ("France", "FR"),
            ("China", "CN"),
            ("India", "IN"),
            ("United States of America", "US"),
            ("United Kingdom of Great Britain and Northern Ireland", "GB"),
            ("Japan", "JP"),
        ]

        for country, expected_code in test_cases:
            assert ISO_COUNTRY_MAPPING[country] == expected_code

    def test_special_cases(self):
        """Test countries with special naming conventions."""
        test_cases = [
            (
                "Côte d’Ivoire",
                "CI",
            ),  # Special characters (curly apostrophe from UN data)
            ("Democratic People's Republic of Korea", "KP"),  # North Korea
            ("Republic of Korea", "KR"),  # South Korea
            ("Bolivia (Plurinational State of)", "BO"),
            ("Iran (Islamic Republic of)", "IR"),
            ("Venezuela (Bolivarian Republic of)", "VE"),
            ("Türkiye", "TR"),  # Turkey
            ("Viet Nam", "VN"),  # Vietnam
        ]

        for country, expected_code in test_cases:
            assert ISO_COUNTRY_MAPPING[country] == expected_code

    def test_reverse_mapping(self):
        """Test ISO code to country name reverse lookup."""
        test_cases = [
            ("KE", "Kenya"),
            ("US", "United States of America"),
            ("GB", "United Kingdom of Great Britain and Northern Ireland"),
            ("CD", "Democratic Republic of the Congo"),
            ("CG", "Congo (Republic of the)"),
        ]

        for code, expected_country in test_cases:
            assert ISO_CODE_TO_COUNTRY[code] == expected_country


class TestISOFunctions:
    """Test ISO mapping helper functions."""

    def test_get_iso_code_found(self):
        """Test getting ISO code for a valid country."""
        assert get_iso_code("Kenya") == "KE"
        assert get_iso_code("France") == "FR"
        assert get_iso_code("United States of America") == "US"

    def test_get_iso_code_not_found(self):
        """Test getting ISO code for an invalid country."""
        assert get_iso_code("Invalid Country") is None
        assert get_iso_code("") is None

    def test_get_country_name_found(self):
        """Test getting country name for a valid ISO code."""
        assert get_country_name("KE") == "Kenya"
        assert get_country_name("ke") == "Kenya"  # Case insensitive
        assert get_country_name("FR") == "France"
        assert get_country_name("US") == "United States of America"

    def test_get_country_name_not_found(self):
        """Test getting country name for an invalid ISO code."""
        assert get_country_name("XX") is None
        assert get_country_name("ZZZ") is None

    def test_normalize_country_to_iso_found(self):
        """Test normalizing country name with ISO code."""
        country, iso = normalize_country_to_iso("Kenya")
        assert country == "Kenya"
        assert iso == "KE"

        country, iso = normalize_country_to_iso("United States of America")
        assert country == "United States of America"
        assert iso == "US"

    def test_normalize_country_to_iso_not_found(self):
        """Test normalizing invalid country name."""
        country, iso = normalize_country_to_iso("Invalid Country")
        assert country is None
        assert iso is None


class TestConfigIntegration:
    """Test integration with config files."""

    def test_config_file_matches_mapping(self):
        """Test that config file contains all 194 countries."""
        import json

        with open("configs/filters/countries/countries_iso2.json", "r") as f:
            config_data = json.load(f)

        assert len(config_data) == 194
        # Verify a few entries match
        assert config_data["Kenya"] == "KE"
        assert config_data["France"] == "FR"


class TestCountryUtils:
    """Test country_utils integration."""

    def test_country_utils_normalize(self):
        """Test that country_utils uses the complete mapping."""
        from scrapers.country_utils import normalize_country

        # Test exact match
        raw, normalized, iso = normalize_country("Kenya")
        assert normalized == "Kenya"
        assert iso == "KE"

        # Test case insensitive
        raw, normalized, iso = normalize_country("kenya")
        assert normalized == "Kenya"
        assert iso == "KE"

        # Test special case
        raw, normalized, iso = normalize_country("United States of America")
        assert iso == "US"

    def test_country_utils_all_194(self):
        """Test that country_utils can normalize all 194 countries."""
        from scrapers.country_utils import ISO_MAP

        assert len(ISO_MAP) == 194


class TestScorecard:
    """Test scorecard integration with ISO codes."""

    def test_scorecard_uses_iso_codes(self):
        """Test that scorecard loader adds ISO codes."""
        from processors.scorecard import load_scorecard

        df = load_scorecard()

        # Check that Country_ISO column exists
        assert "Country_ISO" in df.columns

        # Check that all countries have ISO codes
        assert df["Country_ISO"].notna().all()

        # Check a few specific countries
        kenya_row = df[df["Country"] == "Kenya"].iloc[0]
        assert kenya_row["Country_ISO"] == "KE"

        us_row = df[df["Country"] == "United States of America"].iloc[0]
        assert us_row["Country_ISO"] == "US"
