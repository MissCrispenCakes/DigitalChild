# Year extraction test placeholder
import re
import pytest


def extract_year(filename, txt_path, logger):
    # 1. From filename (all matches, prefer first)
    matches = re.findall(r"\b(19|20)\d{2}\b", filename)
    if matches:
        return int(matches[0]), "filename"

    # 2. From text (first 1000 chars)
    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            text = f.read(1000)
            matches = re.findall(r"\b(19|20)\d{2}\b", text)
            if matches:
                return int(matches[0]), "first_page"
    except Exception as e:
        logger.warning(f"Error scanning text for year in {filename}: {e}")

    return None, "unknown"



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
