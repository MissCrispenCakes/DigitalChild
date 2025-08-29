# Year extraction test placeholder
import re
import pytest

def extract_year(filename: str):
    """Extract a year (1900–2099) from a filename using regex."""
    match = re.search(r"(19|20)\d{2}", filename)
    return int(match.group()) if match else None


@pytest.mark.parametrize("filename,expected", [
    ("AU_AI_Strategy_2024.pdf", 2024),           # normal case
    ("African_Union_Policy_1999.pdf", 1999),     # older year
    ("ChildRights_NoYear.pdf", None),            # no year
    ("AI_Strategy_2023_Final_2024.pdf", 2023),   # multiple years → takes first
    ("AU_Policy_20x4.pdf", None),                # malformed year
    ("AU_Policy_203.pdf", None),                 # incomplete year
    ("AU_Policy_20245.pdf", None),               # 5-digit → invalid
])
def test_extract_year(filename, expected):
    assert extract_year(filename) == expected
