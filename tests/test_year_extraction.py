import pytest

from pipeline_runner import extract_year  # ✅ use real implementation


@pytest.mark.parametrize(
    "filename,expected",
    [
        ("AU_AI_Strategy_2024.pdf", 2024),
        ("African_Union_Policy_1999.pdf", 1999),
        ("ChildRights_NoYear.pdf", None),
        ("AI_Strategy_2023_Final_2024.pdf", 2023),
        ("AU_Policy_20x4.pdf", None),
        ("AU_Policy_203.pdf", None),
        ("AU_Policy_20245.pdf", None),
    ],
)
def test_extract_year(filename, expected):
    year, src = extract_year(filename)
    assert year == expected
    assert isinstance(src, str)
