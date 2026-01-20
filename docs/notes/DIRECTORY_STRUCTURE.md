# Project Directory Structure

This document explains the purpose of each folder and subfolder in the DigitalChild project.

______________________________________________________________________

## Top-Level Files

- `pipeline_runner.py` → Main entry point for running pipelines (scraper, urls, scorecard modes)
- `init_project.py` → Bootstrap script to create directory structure and placeholders
- `requirements.txt` → Python dependencies
- `CLAUDE.md` → Comprehensive guide for Claude Code AI assistant
- `README.md` → Project quickstart and documentation
- `scorecard_main.xlsx` → Scorecard data (194 countries, 10 indicators each)
- `.github/workflows/ci.yml` → GitHub Actions CI pipeline
- `.pre-commit-config.yaml` → Pre-commit hooks configuration

______________________________________________________________________

## Scrapers (`scrapers/`)

Code for fetching raw documents from various sources.

**NO `__init__.py`** - Modules are imported directly by name.

### Implemented Scrapers

- `au_policy.py` → African Union policy documents
- `au_policy_sel.py` → AU policy (Selenium variant)
- `ohchr.py` → OHCHR Treaty Body database documents
- `ohchr_sel.py` → OHCHR (Selenium variant)
- `upr.py` → Universal Periodic Review documents
- `upr_sel.py` → UPR (Selenium variant)
- `unicef.py` → UNICEF reports and publications
- `unicef_sel.py` → UNICEF (Selenium variant)
- `acerwc.py` → African Committee of Experts on the Rights and Welfare of the Child
- `acerwc_sel.py` → ACERWC (Selenium variant)
- `achpr.py` → African Commission on Human and Peoples' Rights
- `achpr_sel.py` → ACHPR (Selenium variant)

**Notes:**

- Each scraper implements a `scrape()` function
- Returns list of downloaded file paths
- Writes to `data/raw/<source>/`
- Skips existing files automatically

______________________________________________________________________

## Processors (`processors/`)

Code for processing raw documents and enriching metadata.

**HAS `__init__.py`** - Proper Python package.

### Document Processing

- `pdf_to_text.py` → Extract text from PDF files
- `docx_to_text.py` → Extract text from DOCX files
- `html_to_text.py` → Extract text from HTML files
- `fallback_handler.py` → Tries multiple processors until success

### Feature Extraction

- `tagger.py` → Applies regex-based tag rules to documents
- `tags_summary.py` → Generates CSV summary of tag frequencies
- `recommendations.py` → Extracts recommendations from treaty body docs (regex-based)

### Scorecard System

- `scorecard.py` → Loads scorecard data from Excel, provides query functions
- `scorecard_enricher.py` → Enriches metadata with country-level indicators
- `scorecard_export.py` → Exports scorecard to CSV formats (summary, sources, by-indicator, by-region)
- `scorecard_validator.py` → Validates all source URLs (parallel workers, retry logic)
- `scorecard_diff.py` → Monitors sources for changes, detects stale entries

### Validation & Security

- `validators.py` → Centralized validation module (68 tests)
  - URL validation (malicious pattern blocking)
  - Path validation (traversal protection)
  - File validation (size, extension checks)
  - String validation (length, patterns, regex)
  - Config validation (JSON, tags, structure)
  - Schema validation (metadata, documents)

### Utilities

- `logger.py` → Unified logging system (console + file logging)
- `json_normalizer.py` → Normalizes country/region names, preserves `_raw` fields

______________________________________________________________________

## Configs (`configs/`)

JSON configuration files for tags, recommendations, and filters.

### Tags Configs

- `tags_v1.json` → Original tag rules
- `tags_v2.json` → Expanded tag rules
- `tags_v3.json` → Current comprehensive tag rules
- `tags_digital.json` → Digital-specific tags
- `tags_main.json` → Version mapping and `latest` alias

### URL Dictionaries

- `url_dict/` → Static URL dictionaries for sources
  - Used when scraping isn't feasible
  - Processed via `--mode urls` in pipeline_runner

### Future Configs

- `recommendations/` → Recommendations extraction configs (planned)
- `comparison/` → Comparison configuration files (planned)
- `filters/` → Filter configuration files (planned)

______________________________________________________________________

## Data (`data/`)

All data directories are **gitignored** - not committed to version control.

### Raw Data (`data/raw/`)

Source documents as scraped or manually uploaded.

- `data/raw/au_policy/` → AU policy PDFs
- `data/raw/ohchr/` → OHCHR treaty body documents
- `data/raw/upr/` → UPR reports
- `data/raw/unicef/` → UNICEF publications
- `data/raw/acerwc/` → ACERWC documents
- `data/raw/achpr/` → ACHPR documents
- `data/raw/manual/` → Manually uploaded files

### Processed Data (`data/processed/`)

Converted text, structured data, OCR results.

Organized as: `data/processed/<region>/<org>/text/`

Example:
- `data/processed/Africa/AU/text/`
- `data/processed/Global/OHCHR/text/`

### Metadata (`data/metadata/`)

- `metadata.json` → Central metadata file
  - Project identity
  - Documents list with tags_history, recommendations_history, scorecard
  - Full schema in `docs/standards/METADATA_SCHEMA.md`

### Exports (`data/exports/`)

Output summaries, comparisons, timelines, scorecard exports.

- `tags_summary.csv` → Tag frequency counts
- `scorecard_summary.csv` → Country indicators summary
- `scorecard_sources.csv` → All source URLs (2,543 tracked)
- `scorecard_url_validation.json` → URL validation results
- `scorecard_broken_links.csv` → Broken links report
- `scorecard_diff_report.json` → Source change detection results
- `scorecard_<indicator>.csv` → Per-indicator exports
- `scorecard_<region>.csv` → Per-region exports

### Cache (`data/cache/`)

Temporary cache files for scorecard source monitoring.

- `scorecard_sources/` → Content hashes for change detection

______________________________________________________________________

## Logs (`logs/`)

**Gitignored** - not committed to version control.

Unified and per-module logs per run.

- Format: `<timestamp>_<pipeline>.log`
- Example: `2025-08-28_12-22-40_au_policy_run.log`
- Controlled via `--no-module-logs` flag in `pipeline_runner.py`

______________________________________________________________________

## Docs (`docs/`)

Comprehensive documentation (24+ markdown files).

### Main Docs (`docs/`)

- `README.md` → Documentation overview and navigation
- `DOCS_INDEX.md` → Complete index of all documentation
- `ROADMAP.md` → Project roadmap and development phases
- `SCORECARD_WORKFLOW.md` → Complete scorecard system guide
- `SCORECARD_REVIEW_SUMMARY.md` → Scorecard review and analysis
- `VALIDATORS_USAGE.md` → Using the centralized validation module
- `TAGS_VISUALIZATION_PLAN.md` → Future visualization plans
- `SOURCE_FEASIBILITY_CHECKLIST.md` → Checklist for evaluating new sources

### Implementation Notes (`docs/notes/`)

- `DIRECTORY_STRUCTURE.md` → This file
- `PIPELINE_FLOW.md` → End-to-end data flow
- `PIPELINE_LOGGING.md` → Logging system details
- `TAGS_MAIN_NOTES.md` → Tag version management
- `TAGS_EXPORT_NOTES.md` → How to read tag exports
- `COMPARISON_EXPORT_NOTES.md` → Comparison export format

### Run Guides (`docs/runs/`)

- `RUNBOOK.md` → Common commands for pipelines and tests
- `FIRST_RUN_ERRORS.md` → Troubleshooting first-run issues
- `PROCESSOR_TEST_RUN.md` → Testing individual processors

### Standards (`docs/standards/`)

- `METADATA_SCHEMA.md` → Complete metadata JSON schema
- `TAGS_CONFIG_FORMAT.md` → Tag configuration structure
- `RECOMMENDATIONS_CONFIG_FORMAT.md` → Recommendations config format
- `COMPARISON_CONFIG_FORMAT.md` → Comparison config format
- `FILE_NAMING_STANDARDS.md` → File naming conventions
- `DOC_TYPE_STANDARDS.md` → Document type classifications
- `ISO_MAPPING.md` → Country/region ISO mapping
- `SCRAPER_STRUCTURE.md` → How to build scrapers

______________________________________________________________________

## Tests (`tests/`)

Comprehensive test suite (124 tests, 100% passing).

### Test Files

- `conftest.py` → Pytest configuration, adds project root to path
- `test_validators.py` → 68 tests for validators module
- `test_scorecard.py` → 20 tests for scorecard system
- `test_tagger.py` → Tagging functionality tests
- `test_metadata.py` → Metadata operations tests
- `test_logging.py` → Logging system tests
- `test_fallback_handler.py` → Multi-format processing tests
- `test_year_extraction.py` → Year extraction tests
- `test_country_region.py` → Country/region normalization tests
- `test_comparison.py` → Comparison export tests
- `test_recommendations.py` → Recommendations extraction tests
- `test_csv_footer.py` → CSV footer formatting tests

### Test Data

- `test_data/` → Sample files for testing
- Temporary files created during tests are cleaned up automatically

______________________________________________________________________

## GitHub Actions (`.github/`)

CI/CD pipeline configuration.

- `.github/workflows/ci.yml` → Runs on push/PR to main/homebase/basecamp
  - **Job 1: test** - Python 3.12, runs pre-commit + pytest
  - **Job 2: docs** - Python 3.11, checks markdown formatting

______________________________________________________________________

## Virtual Environment (`.LittleRainbow/`)

**Gitignored** - Python virtual environment.

- Created with: `python3 -m venv .LittleRainbow`
- Activated with: `source .LittleRainbow/bin/activate`
- Contains all dependencies from `requirements.txt`

______________________________________________________________________

## Summary

```
DigitalChild/
├── pipeline_runner.py         # Main entry point
├── init_project.py            # Bootstrap script
├── requirements.txt           # Dependencies
├── scorecard_main.xlsx        # Scorecard data
├── CLAUDE.md                  # AI assistant guide
├── README.md                  # Project quickstart
├── scrapers/                  # Data fetching (no __init__.py)
├── processors/                # Data processing (has __init__.py)
├── configs/                   # Tag/rec configs, URL dictionaries
├── data/                      # Data storage (gitignored)
│   ├── raw/                   # Source documents
│   ├── processed/             # Converted text
│   ├── metadata/              # Central metadata.json
│   ├── exports/               # CSV/JSON outputs
│   └── cache/                 # Temporary cache
├── logs/                      # Run logs (gitignored)
├── docs/                      # Documentation (24+ files)
│   ├── notes/                 # Implementation notes
│   ├── runs/                  # Run guides
│   └── standards/             # Format standards
├── tests/                     # Test suite (124 tests)
└── .github/                   # CI/CD configuration
```

______________________________________________________________________

Last updated: January 2026
