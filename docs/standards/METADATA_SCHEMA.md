# Metadata Schema

This document defines the complete schema for `data/metadata/metadata.json`.

______________________________________________________________________

## Top-Level Structure

```json
{
  "project_identity": { ... },
  "documents": [ ... ]
}
```

______________________________________________________________________

## Project Identity

```json
{
  "project_identity": {
    "name": "GRIMdata / LittleRainbowRights",
    "domains": [
      "https://GRIMdata.org",
      "https://LittleRainbowRights.com"
    ],
    "note": "Pipeline for analyzing child & LGBTQ+ digital protections."
  }
}
```

______________________________________________________________________

## Document Schema

### Core Fields

```json
{
  "id": "AU_Digital_Compact_2024.pdf",
  "source": "au_policy",
  "file_type": "PDF",
  "ingestion_method": "scraper",
  "last_processed": "2025-08-28T15:22:00Z"
}
```

**Field Descriptions:**

- `id` (string, required): Unique document identifier (usually filename)
- `source` (string, required): Source scraper or ingestion method
  - Examples: `au_policy`, `ohchr`, `upr`, `unicef`, `manual`
- `file_type` (string): File format
  - Examples: `PDF`, `DOCX`, `HTML`, `TXT`
- `ingestion_method` (string): How document was obtained
  - Examples: `scraper`, `manual`, `api`, `url_dict`
- `last_processed` (string, ISO 8601): Last processing timestamp

### Geographic Fields

```json
{
  "country": "African_Union",
  "country_raw": "African Union",
  "country_iso": "AU",
  "region": "Africa",
  "region_raw": "Sub-Saharan Africa"
}
```

**Field Descriptions:**

- `country` (string): Normalized country name (underscores, no special chars)
- `country_raw` (string): Original country name as extracted
- `country_iso` (string, optional): ISO 3166-1 alpha-2 code
  - Examples: `KE` (Kenya), `NG` (Nigeria), `ZA` (South Africa)
- `region` (string): Normalized region name
- `region_raw` (string): Original region string as extracted

### Temporal Fields

```json
{
  "year": 2024,
  "year_extracted_from": "filename"
}
```

**Field Descriptions:**

- `year` (integer, optional): Document publication year (1900-2100)
- `year_extracted_from` (string, optional): Extraction source
  - Examples: `filename`, `first_page`, `metadata`, `url`

### Classification Fields

```json
{
  "doc_type": "Policy"
}
```

**Field Descriptions:**

- `doc_type` (string, optional): Document type classification
  - Examples: `Policy`, `Law`, `Treaty`, `UPR`, `Observation`, `Report`, `Research`

### Tags History

```json
{
  "tags_history": [
    {
      "tags": ["AI", "DigitalPolicy", "ChildRights"],
      "version": "tags_v3",
      "timestamp": "2025-08-28T15:22:00Z"
    },
    {
      "tags": ["AI", "ChildRights"],
      "version": "tags_v1",
      "timestamp": "2025-08-20T10:15:00Z"
    }
  ]
}
```

**Field Descriptions:**

- `tags_history` (array): Historical record of tag applications
  - `tags` (array of strings): Tags matched for this version
  - `version` (string): Tag config version used
    - Examples: `tags_v1`, `tags_v2`, `tags_v3`, `tags_digital`, `latest`
  - `timestamp` (string, ISO 8601): When tags were applied

**Notes:**

- Multiple entries allow comparison across tag versions
- Most recent entry typically at index 0
- Empty array `[]` if document hasn't been tagged

### Recommendations History

```json
{
  "recommendations_history": [
    {
      "recommendations": [
        "The Committee recommends that the State Party adopt...",
        "urges the Government to ensure..."
      ],
      "version": "recs_v1",
      "timestamp": "2025-08-28T16:00:00Z"
    }
  ]
}
```

**Field Descriptions:**

- `recommendations_history` (array): Historical record of recommendations extraction
  - `recommendations` (array of strings): Extracted recommendation texts
  - `version` (string): Recommendations config version
  - `timestamp` (string, ISO 8601): When recommendations were extracted

**Notes:**

- Used for treaty body documents, UPR reports, observations
- Empty array `[]` if no recommendations found or not yet processed

### Scorecard Integration

```json
{
  "scorecard": {
    "matched_country": "Kenya",
    "enriched_at": "2025-01-15T10:30:00Z",
    "indicators": {
      "AI_Policy_Status": {
        "value": "Draft policy under development (2024)",
        "source": "https://unesco.org/ai-policy-observatory/kenya"
      },
      "Data_Protection_Law": {
        "value": "In force - Data Protection Act 2019",
        "source": "https://unctad.org/data-protection-tracker"
      },
      "LGBTQ_Legal_Status": {
        "value": "Criminalized - Penal Code Sections 162-165",
        "source": "https://ilga.org/kenya-profile"
      }
    }
  }
}
```

**Field Descriptions:**

- `scorecard` (object, optional): Country-level human rights indicators
  - `matched_country` (string): Country name matched in scorecard
  - `enriched_at` (string, ISO 8601): When scorecard data was added
  - `indicators` (object): Dictionary of indicator data
    - Each indicator has:
      - `value` (string): Indicator status/description
      - `source` (string): Source URL for verification

**Available Indicators (10 per country):**

1. **AI_Policy_Status** - National AI policy/strategy status
1. **Data_Protection_Law** - Data protection legislation status
1. **LGBTQ_Legal_Status** - Legal status of LGBTQ+ rights
1. **Child_Online_Protection** - Child protection laws and policies
1. **SIM_Biometric** - SIM card registration requirements
1. **Encryption_Backdoors** - Government encryption/backdoor requirements
1. **Promotion_Propaganda** - LGBTQ+ promotion/propaganda laws
1. **DPA_Independence** - Data Protection Authority independence
1. **Content_Moderation** - Content moderation legal framework
1. **Age_Verification** - Age verification requirements

**Notes:**

- Scorecard is added during enrichment step
- Only present if document has a country field AND country exists in scorecard
- 194 countries currently tracked in `scorecard_main.xlsx`
- 2,543 source URLs tracked and validated

______________________________________________________________________

## Complete Example

```json
{
  "project_identity": {
    "name": "GRIMdata / LittleRainbowRights",
    "domains": [
      "https://GRIMdata.org",
      "https://LittleRainbowRights.com"
    ],
    "note": "Pipeline for analyzing child & LGBTQ+ digital protections."
  },
  "documents": [
    {
      "id": "Kenya_UPR_Report_2020.pdf",
      "source": "upr",
      "country": "Kenya",
      "country_raw": "Kenya",
      "country_iso": "KE",
      "region": "Africa",
      "region_raw": "Sub-Saharan Africa",
      "year": 2020,
      "year_extracted_from": "filename",
      "doc_type": "UPR",
      "file_type": "PDF",
      "ingestion_method": "scraper",
      "tags_history": [
        {
          "tags": ["ChildRights", "LGBTQ", "Privacy", "OnlineRights"],
          "version": "tags_v3",
          "timestamp": "2025-08-28T15:22:00Z"
        }
      ],
      "recommendations_history": [
        {
          "recommendations": [
            "The Committee recommends that Kenya adopt comprehensive child online protection legislation",
            "urges the State to decriminalize consensual same-sex conduct"
          ],
          "version": "recs_v1",
          "timestamp": "2025-08-28T16:00:00Z"
        }
      ],
      "scorecard": {
        "matched_country": "Kenya",
        "enriched_at": "2025-01-15T10:30:00Z",
        "indicators": {
          "AI_Policy_Status": {
            "value": "Draft policy under development (2024)",
            "source": "https://unesco.org/ai-policy-observatory/kenya"
          },
          "Data_Protection_Law": {
            "value": "In force - Data Protection Act 2019",
            "source": "https://unctad.org/data-protection-tracker"
          },
          "LGBTQ_Legal_Status": {
            "value": "Criminalized - Penal Code Sections 162-165",
            "source": "https://ilga.org/kenya-profile"
          }
        }
      },
      "last_processed": "2025-08-28T15:22:00Z"
    }
  ]
}
```

______________________________________________________________________

## Validation

Documents are validated using `processors/validators.py`:

```python
from processors.validators import validate_document_metadata

# Validates:
# - Required fields (id, source)
# - Field types (year must be int, tags_history must be list)
# - Value constraints (year 1900-2100, non-empty strings)

validate_document_metadata(document)
```

See [../VALIDATORS_USAGE.md](../VALIDATORS_USAGE.md) for complete validation guide.

______________________________________________________________________

## Notes

- All timestamps use ISO 8601 format with UTC timezone
- Fields with `_raw` preserve original values for provenance
- History arrays allow version comparison and research reproducibility
- Empty arrays `[]` are valid for history fields if not yet processed
- Optional fields may be omitted entirely or set to `null`
- Scorecard enrichment is independent of tags/recommendations
- Schema evolves as features are added; maintain backward compatibility

______________________________________________________________________

Last updated: January 2026
