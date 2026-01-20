# Scorecard System Workflow

This document describes the complete scorecard system for the DigitalChild project, which tracks 10 human rights indicators across countries and enriches document metadata.

## Overview

The scorecard system provides country-level data on digital child protection policies and LGBTQ+ rights. It consists of:

1. **Data Source**: `scorecard_main.xlsx` - Excel file with country indicators
1. **Loader**: `processors/scorecard.py` - Loads and caches scorecard data
1. **Enricher**: `processors/scorecard_enricher.py` - Adds scorecard data to document metadata
1. **Exporter**: `processors/scorecard_export.py` - Creates CSV exports for website/analysis
1. **Validator**: `processors/scorecard_validator.py` - Checks source URLs for broken links
1. **Diff Checker**: `processors/scorecard_diff.py` - Monitors sources for changes

## Indicators

The scorecard tracks 10 indicators (each with value + source URL):

1. **AI_Policy_Status** - National AI policy/strategy status
1. **Data_Protection_Law** - Data protection/privacy legislation
1. **Children_Data_Safeguards** - Child-specific data protection measures
1. **SOGI_Sensitive_Data** - Sexual orientation/gender identity data protections
1. **DPA_Independence** - Data Protection Authority independence
1. **DPIA_Required_High_Risk_AI** - Data protection impact assessments for AI
1. **LGBTQ_Legal_Status** - Legal status of LGBTQ+ people
1. **Promotion_Propaganda_Offences** - Anti-LGBTQ+ propaganda laws
1. **COP_Strategy** - Child online protection strategy
1. **SIM_Biometric_ID_Linkage** - SIM registration and biometric requirements

## Architecture

```
scorecard_main.xlsx
        ↓
    scorecard.py (loader)
        ↓
    ┌───────────┴───────────┐
    ↓                       ↓
scorecard_enricher.py  scorecard_export.py
(add to metadata)      (CSV exports)
    ↓
metadata.json
(enriched documents)
```

## Workflows

### 1. Initial Scorecard Setup

```bash
# 1. Place scorecard_main.xlsx in project root
# 2. Test scorecard loads correctly
python -c "from processors.scorecard import load_scorecard; print(load_scorecard())"

# 3. Run tests to verify
pytest tests/test_scorecard.py -v
```

### 2. Enrich Document Metadata

Add scorecard indicators to documents based on their country:

```bash
# Enrich all documents in metadata.json
python processors/scorecard_enricher.py

# Dry run (don't save changes)
python processors/scorecard_enricher.py --dry-run

# Show enrichment summary only
python processors/scorecard_enricher.py --summary
```

**Programmatic usage:**

```python
from processors.scorecard_enricher import enrich_document, enrich_all_metadata

# Enrich single document
doc = {"id": "doc-1", "country": "Albania"}
enriched_doc = enrich_document(doc)

# Enrich all metadata
stats = enrich_all_metadata(save=True)
print(f"Enriched {stats['enriched']} documents")
```

**Output format:**

```json
{
  "id": "doc-1",
  "country": "Albania",
  "scorecard": {
    "matched_country": "Albania",
    "enriched_at": "2024-01-15T10:30:00Z",
    "indicators": {
      "AI_Policy_Status": {
        "value": "Draft policy under development (2023)",
        "source": "https://..."
      },
      "Data_Protection_Law": {
        "value": "Law No. 9887 (2008), aligned with GDPR",
        "source": "https://..."
      }
      // ... 8 more indicators
    }
  }
}
```

### 3. Export Scorecard Data

Generate CSV exports for website/analysis:

```bash
# From Python code
from processors.scorecard_export import export_scorecard

exports = export_scorecard()
# Returns:
# {
#   "summary": "data/exports/scorecard_summary.csv",
#   "sources": "data/exports/scorecard_sources.csv",
#   "indicator_counts": "data/exports/scorecard_indicator_counts.csv"
# }
```

**Export types:**

1. **Summary CSV**: All countries with all indicators (for main table)
1. **Sources CSV**: All source URLs (for verification/citation)
1. **Indicator Counts**: Distribution of values per indicator (for charts)
1. **By Indicator**: Individual CSV per indicator
1. **By Region**: Countries filtered by region

**Programmatic usage:**

```python
from processors.scorecard_export import ScorecardExporter

exporter = ScorecardExporter()

# Export specific region
exporter.export_by_region("Africa", "data/exports/africa.csv")

# Export specific indicator
exporter.export_by_indicator("LGBTQ_Legal_Status", "data/exports/lgbtq_status.csv")

# Export all at once
exports = exporter.export_all()
```

### 4. Validate Source URLs

Check all source URLs for broken/redirected links:

```bash
# Run validation
python processors/scorecard_validator.py

# Custom worker count
python processors/scorecard_validator.py --workers 20

# Don't save reports
python processors/scorecard_validator.py --no-save
```

**Output:**

- `data/exports/scorecard_url_validation.json` - Full validation report
- `data/exports/scorecard_broken_links.csv` - Broken links only (for review)

**Programmatic usage:**

```python
from processors.scorecard_validator import run_validation

report = run_validation(save_reports=True)
print(f"{report['ok']} OK, {report['broken']} broken, {report['redirected']} redirected")
```

### 5. Monitor for Changes

Check monitored sources for content changes:

```bash
# Check all monitored sources
python processors/scorecard_diff.py

# Check specific country sources
python processors/scorecard_diff.py --country "South Africa"

# Check sources only (skip stale entry detection)
python processors/scorecard_diff.py --sources-only
```

**Monitored sources:**

- UNESCO AI Policy Observatory
- UNCTAD Data Protection Tracker
- ILGA World Maps
- Human Dignity Trust
- GSMA SIM Registration

**Programmatic usage:**

```python
from processors.scorecard_diff import run_diff_check, check_country_sources

# Full check
report = run_diff_check(save_report=True)

# Check specific country
results = check_country_sources("Kenya")
```

## Integration with Pipeline

The scorecard enrichment is **not** part of the main pipeline (`pipeline_runner.py`) by default. It's a separate step run after documents are processed.

**Typical workflow:**

```bash
# 1. Run pipeline to scrape and process documents
python pipeline_runner.py --source upr --country "Kenya"

# 2. Enrich metadata with scorecard
python processors/scorecard_enricher.py

# 3. Export scorecard data for website
python -c "from processors.scorecard_export import export_scorecard; export_scorecard()"
```

## Adding to Pipeline (Optional)

To integrate scorecard enrichment into the pipeline:

```python
# In pipeline_runner.py, after process_documents():

from processors.scorecard_enricher import enrich_all_metadata

# After processing is complete
if args.enrich_scorecard:
    logger.info("Enriching metadata with scorecard indicators...")
    stats = enrich_all_metadata(save=True)
    logger.info(f"Enriched {stats['enriched']} documents")
```

## Maintenance Tasks

### Update Scorecard Data

1. Edit `scorecard_main.xlsx` with new data
1. Force reload: `load_scorecard(force_reload=True)`
1. Re-enrich metadata: `python processors/scorecard_enricher.py`
1. Re-export: `python -c "from processors.scorecard_export import export_scorecard; export_scorecard()"`

### Verify Data Quality

```bash
# Check for broken links
python processors/scorecard_validator.py

# Check for stale entries
python processors/scorecard_diff.py

# Run all scorecard tests
pytest tests/test_scorecard.py -v
```

### Add New Indicator

1. Add column pair to `scorecard_main.xlsx`:

   - `New_Indicator` (value column)
   - `New_Indicator_Source` (source URL column)

1. Update `INDICATOR_COLUMNS` in `processors/scorecard.py`:

   ```python
   INDICATOR_COLUMNS = [
       # ... existing indicators
       ("New_Indicator", "New_Indicator_Source"),
   ]
   ```

1. Re-run enrichment and exports

## File Locations

- **Source Data**: `scorecard_main.xlsx` (project root)
- **Exports**: `data/exports/scorecard_*.csv`
- **Validation Reports**: `data/exports/scorecard_url_validation.json`
- **Diff Reports**: `data/exports/scorecard_diff_report.json`
- **Cache**: `data/cache/scorecard_sources/*.json`

## Testing

```bash
# Run all scorecard tests
pytest tests/test_scorecard.py -v

# Run specific test class
pytest tests/test_scorecard.py::TestScorecardLoader -v

# Run with coverage
pytest tests/test_scorecard.py --cov=processors/scorecard --cov-report=html
```

## Troubleshooting

### Country Not Found

**Problem**: Document country doesn't match scorecard country names

**Solution**: The loader tries multiple normalization methods:

- Exact match (case-insensitive)
- ISO code lookup
- Fuzzy matching

Check country names in metadata vs scorecard:

```python
from processors.scorecard import get_countries_list

countries = get_countries_list()
print(countries)  # List all scorecard countries
```

### Missing Indicators

**Problem**: Enriched document missing some indicators

**Solution**: Check for empty cells in `scorecard_main.xlsx`. Empty values are skipped.

### Validation Timeouts

**Problem**: URL validation takes too long

**Solution**: Reduce worker count or increase timeout:

```python
from processors.scorecard_validator import validate_all_urls

report = validate_all_urls(max_workers=5)  # Slower but more reliable
```

## Future Enhancements

1. **Auto-update from sources**: Automatically scrape monitored sources and update scorecard
1. **Version tracking**: Track scorecard changes over time
1. **API endpoint**: Serve scorecard data via REST API for website
1. **Visualization**: Generate charts/maps from scorecard data
1. **Comparison mode**: Compare countries side-by-side
1. **Timeline view**: Show indicator changes over time per country

## Related Documentation

- [METADATA_SCHEMA.md](../standards/METADATA_SCHEMA.md) - Document metadata structure
- [PIPELINE_FLOW.md](../notes/PIPELINE_FLOW.md) - Main pipeline workflow
- [ISO_MAPPING.md](../standards/ISO_MAPPING.md) - Country code standards
