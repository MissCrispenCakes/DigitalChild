# ISO 3166-1 alpha-2 Country Code Mapping

## Overview

The DigitalChild project uses a complete ISO 3166-1 alpha-2 country code mapping for all 194 UN member states. This standardized mapping ensures consistent country identification across all data sources, exports, and visualizations.

## Location

- **Module**: `utils/iso_mapping.py`
- **Config**: `configs/filters/countries/countries_iso2.json`
- **Tests**: `tests/test_iso_mapping.py`

## Coverage

- **Total Countries**: 194 UN member states
- **Standard**: ISO 3166-1 alpha-2 (two-letter codes)
- **Source**: Generated using `pycountry` library with manual overrides for UN-specific naming conventions

## Usage

### Basic Lookup

```python
from utils.iso_mapping import get_iso_code, get_country_name

# Get ISO code for a country name
code = get_iso_code("Kenya")  # Returns "KE"

# Get country name for an ISO code (case-insensitive)
country = get_country_name("KE")  # Returns "Kenya"
country = get_country_name("ke")  # Also returns "Kenya"
```

### Normalize Country with ISO Code

```python
from utils.iso_mapping import normalize_country_to_iso

# Returns tuple of (country_name, iso_code)
country, iso = normalize_country_to_iso("Kenya")
# Returns: ("Kenya", "KE")

# Returns (None, None) for unknown countries
country, iso = normalize_country_to_iso("Unknown Country")
# Returns: (None, None)
```

### Direct Dictionary Access

```python
from utils.iso_mapping import ISO_COUNTRY_MAPPING, ISO_CODE_TO_COUNTRY

# Forward mapping (country → ISO code)
code = ISO_COUNTRY_MAPPING["Kenya"]  # Returns "KE"

# Reverse mapping (ISO code → country)
country = ISO_CODE_TO_COUNTRY["KE"]  # Returns "Kenya"
```

## Special Cases

The mapping handles several special naming conventions used by the UN:

- **Côte d'Ivoire**: Uses curly apostrophe (') as per UN data
- **Democratic People's Republic of Korea**: North Korea (KP)
- **Republic of Korea**: South Korea (KR)
- **Bolivia (Plurinational State of)**: BO
- **Iran (Islamic Republic of)**: IR
- **Venezuela (Bolivarian Republic of)**: VE
- **Türkiye**: TR (updated from Turkey)
- **Viet Nam**: VN (two words as per UN convention)

## Integration Points

### 1. Country Normalization (`scrapers/country_utils.py`)

The country_utils module loads the ISO mapping from the config file:

```python
from scrapers.country_utils import normalize_country

# Returns (raw_name, normalized_name, iso_code)
raw, normalized, iso = normalize_country("kenya")
# Returns: ("kenya", "Kenya", "KE")
```

### 2. Scorecard System (`processors/scorecard.py`)

The scorecard loader automatically adds ISO codes to the dataframe:

```python
from processors.scorecard import load_scorecard

df = load_scorecard()
# DataFrame has 'Country_ISO' column with ISO codes
```

### 3. Document Metadata

Documents enriched with scorecard data include ISO codes:

```json
{
  "id": "Kenya_Report_2024.pdf",
  "country": "Kenya",
  "country_iso": "KE",
  "scorecard": {
    "matched_country": "Kenya",
    "enriched_at": "2024-01-15T10:30:00Z",
    "indicators": { ... }
  }
}
```

## Data Consistency

The ISO mapping ensures consistency across:

1. **Scorecard Data** (`data/scorecard/scorecard_main.xlsx`)
   - UN_194 sheet contains all 194 countries
   - Country names match ISO_COUNTRY_MAPPING keys exactly

2. **Config File** (`configs/filters/countries/countries_iso2.json`)
   - Generated from utils/iso_mapping.py
   - Used by country_utils.py for normalization

3. **Test Suite** (`tests/test_iso_mapping.py`)
   - Validates all 194 countries have mappings
   - Tests bidirectional lookup
   - Verifies integration with scorecard and country_utils

## Generating the Mapping

The ISO mapping was generated using the following approach:

1. Load all 194 UN member states from scorecard_main.xlsx
2. Use `pycountry.countries.get()` to find ISO codes
3. Apply manual overrides for UN-specific naming:
   - "Viet Nam" → VN (pycountry uses "Vietnam")
   - "Türkiye" → TR (updated from "Turkey")
   - "Democratic People's Republic of Korea" → KP
   - "Republic of Korea" → KR
   - Various parenthetical country names

4. Create bidirectional mappings (country→ISO and ISO→country)

## Character Encoding Notes

Some country names use special Unicode characters:

- **Côte d'Ivoire**: Uses curly apostrophe (U+2019: ')
- **Türkiye**: Uses Turkish lowercase i with dot (U+00FC: ü)

These characters must match exactly for lookups to work. The test suite validates these special cases.

## Validation

Run the ISO mapping tests:

```bash
pytest tests/test_iso_mapping.py -v
```

The test suite validates:

- All 194 countries have valid ISO codes
- All ISO codes map back to countries
- Bidirectional mapping consistency
- Special character handling (Côte d'Ivoire, Türkiye)
- Integration with country_utils.py
- Integration with scorecard system
- Config file synchronization

## Future Maintenance

When the UN adds new member states:

1. Add country to `data/scorecard/scorecard_main.xlsx` (UN_194 sheet)
2. Regenerate ISO mapping using pycountry
3. Update `utils/iso_mapping.py` with new mapping
4. Regenerate `configs/filters/countries/countries_iso2.json`
5. Add test case to `tests/test_iso_mapping.py`
6. Run full test suite to verify

## Regions

Regions are normalized but `_raw` values are preserved for provenance:

- `Sub-Saharan Africa` → `Africa`
- `SSA` → `Africa`
- `North Africa` → `Africa`
- `Middle East and North Africa` → `MENA`

## Metadata Fields

- `country`: normalized country name
- `country_raw`: as extracted from source
- `country_iso`: ISO 3166-1 alpha-2 code
- `region`: normalized region
- `region_raw`: original region string

## References

- **ISO 3166-1**: [https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)
- **pycountry**: [https://pypi.org/project/pycountry/](https://pypi.org/project/pycountry/)
- **UN Member States**: [https://www.un.org/en/about-us/member-states](https://www.un.org/en/about-us/member-states)
