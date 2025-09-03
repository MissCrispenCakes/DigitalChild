import pytest

from scrapers import country_utils, region_utils
from processors import json_normalizer


@pytest.mark.parametrize(
    "name,expected_iso",
    [
        ("Kenya", "KE"),
        ("Nigeria", "NG"),
        ("South Africa", "ZA"),
        ("Brazil", "BR"),
        ("France", "FR"),
    ],
)
def test_normalize_country_known(name, expected_iso):
    raw, norm, iso = country_utils.normalize_country(name)
    assert iso == expected_iso
    assert country_utils.get_country_from_iso(iso) == norm


def test_normalize_country_case_insensitive():
    raw, norm, iso = country_utils.normalize_country("kenya")
    assert norm == "Kenya"
    assert iso == "KE"


def test_normalize_country_unknown():
    raw, norm, iso = country_utils.normalize_country("Atlantis")
    assert norm is None
    assert iso is None
    assert country_utils.get_country_from_iso("ZZ") is None


@pytest.mark.parametrize(
    "region_code",
    ["UPR", "OHCHR", "UNICEF", "AFU", "ASEAN", "MERCOSUR"],
)
def test_normalize_region_and_countries(region_code):
    raw, code, data = region_utils.normalize_region(region_code)
    assert code == region_code
    countries = region_utils.get_countries_for_region(region_code)
    # should return a list (maybe empty for global refs)
    assert isinstance(countries, list)


@pytest.mark.parametrize(
    "iso,expected_region",
    [
        ("KE", "AFU"),  # Kenya in Africa Union
        ("NG", "AFU"),  # Nigeria
        ("BR", "MERCOSUR"),  # Brazil
        ("FR", "EUR"),  # France in Europe
    ],
)
def test_get_regions_for_country(iso, expected_region):
    regions = region_utils.get_regions_for_country(iso)
    assert expected_region in regions


def test_normalize_document_enriches():
    doc = {
        "id": "test.pdf",
        "source": "upr",
        "country": "Kenya",
        "region": "UPR",
        "year": 2025,
    }
    normalized = json_normalizer.normalize_document(doc)
    assert normalized["country_iso"] == "KE"
    assert normalized["country_display"] == "Kenya"
    assert "AFU" in normalized["regions_memberships"]
