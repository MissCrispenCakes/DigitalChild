# Year extraction test placeholder
import re
import pytest


def extract_year(filename, txt_path=None, logger=None):
    """
    Extract year from filename and/or text file.
    Always returns (year or None, source).
    """

    YEAR_PATTERN = r"(19|20)\d{2}"

    # 1. From filename
    matches = re.finditer(YEAR_PATTERN, filename)
    for m in matches:
        year_str = m.group(0)
        # Reject if part of a longer number (look before and after)
        start, end = m.span()
        if (start > 0 and filename[start-1].isdigit()) or (end < len(filename) and filename[end].isdigit()):
            continue
        return int(year_str), "filename"

    # 2. From text
    if txt_path:
        try:
            with open(txt_path, "r", encoding="utf-8") as f:
                text = f.read(1000)
                matches = re.finditer(YEAR_PATTERN, text)
                for m in matches:
                    year_str = m.group(0)
                    start, end = m.span()
                    if (start > 0 and text[start-1].isdigit()) or (end < len(text) and text[end].isdigit()):
                        continue
                    return int(year_str), "first_page"
        except Exception as e:
            if logger:
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

# def test_extract_year(filename, expected):
#     year, _ = extract_year(filename)  # ignore source
#     assert year == expected

def test_extract_year(filename, expected):
    result = extract_year(filename)
    assert isinstance(result, tuple)
    assert result[0] == expected
