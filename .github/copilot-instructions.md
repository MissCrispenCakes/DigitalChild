<!-- Copilot / AI agent instructions for DigitalChild repo -->
# AI Agent Guide — DigitalChild

Purpose: short, actionable guidance to help an AI coding agent be productive immediately.

- Project entry points: `pipeline_runner.py` (main CLI / orchestration), `init_project.py` (setup).
- Primary domains: `scrapers/` (fetch documents), `processors/` (convert, normalize, tag, enrich, export), `configs/` (tags, url dicts), `data/` (raw → processed → exports), `utils/` (helpers/detectors).

Key architecture notes
- The pipeline is driven from `pipeline_runner.py` which maps `SCRAPER_MAP` to scrapers and writes into `data/raw/<source>` and `data/processed/<subdir>`.
- Each scraper lives under `scrapers/` and exposes a `scrape(**kwargs)` function that writes raw files to `data/raw/<source>`.
- Converters and enrichers are in `processors/`. Common pattern: `convert(raw_path, proc_dir)` → returns text path; `apply_tags(text, tags_config)` → returns tag dict.
- Metadata is centrally stored at `data/metadata/metadata.json` and updated via `update_metadata()` in `pipeline_runner.py`. Scorecard enrichment runs over that metadata (see `processors/scorecard_enricher.py`).

Data flow (concise)
- Scraper -> writes raw files to `data/raw/<source>`.
- `pipeline_runner` converts raw -> text via `processors/pdf_to_text`, `docx_to_text`, `html_to_text`, or `fallback_handler`.
- Text passes to `processors/tagger` and `processors/recommendations` and then `update_metadata()` records results.
- Scorecard enrichment (`processors/scorecard_enricher`) reads/updates `data/metadata/metadata.json` and `processors/scorecard_export` writes `data/exports/`.

Developer workflows & commands
- Quickstart (local):
  - Run `python init_project.py` then `pip install -r requirements.txt`.
  - Execute `python pipeline_runner.py` (defaults to `--source au_policy --mode scraper`).
- Run specific modes:
  - Scrape a source: `python pipeline_runner.py --source ohchr`
  - Process URL dictionaries: `python pipeline_runner.py --mode urls`
  - Scorecard-only ops: `python pipeline_runner.py --mode scorecard --scorecard-action enrich`
  - Filter by country: `python pipeline_runner.py --source upr --country "South Africa"`
  - Custom tags version: `python pipeline_runner.py --tags-version tags_v2`
- Tests and CI:
  - Run unit tests: `pytest tests/ --maxfail=1 --disable-warnings -q` (CI also runs coverage for `processors` and `scrapers`).
  - Pre-commit / formatting: `pre-commit run --all-files`. CI checks `mdformat --check README.md docs/`.
  - Debug test failures: `pytest tests/test_tagger.py::test_apply_tags -v -s`
  - Check logs: Look in `logs/` directory for run-specific logs or `logs/tests/` for test logs.
- CI specifics:
  - Runs on Python 3.11/3.12 across different jobs
  - Pre-downloads test data in CI to bypass firewall blocks (see `.github/workflows/ci.yml`)
  - Network tests use mocked `requests` calls to avoid external dependencies

Project-specific conventions & patterns
- Scraper contract: implement `scrape(**kwargs)` and write raw files to `data/raw/<source>`. Prefer deterministic filenames (used as `id` in metadata).
- Text converters return a path to a UTF-8 text file. Always call `convert_to_text(raw_path, proc_dir, logger)` or equivalent to ensure consistent logging and error handling.
- Tagging and recommendations use JSON configs in `configs/` (`recs_v1.json`, tags manifests). Use `resolve_tags_config(version)` in `pipeline_runner.py` for correct path resolution.
- Metadata normalization: `processors/json_normalizer.py` is applied before saving metadata. Add normalized fields rather than mutating external callers.
- Logging: use `processors/logger.get_logger()` and `set_run_logfile()` to ensure logs are captured consistently under runs/.

Integration points & external dependencies
- Selenium-based scrapers exist (files named *_sel.py). These require a Selenium driver in CI/local environment.
- External config files: `configs/url_dict/*.json` and `configs/tags_*.json` drive many behaviors; treat them as authoritative sources for tagging and URL inputs.
- Scorecard exports rely on `pandas` and `openpyxl`; tests may expect those packages.

Examples from repo (copy/paste patterns)
- Tag application (pipeline):
  - `tags = tagger.apply_tags(text, tags_config)`
  - `recs = recommendations.apply_recommendations(text, "configs/recs_v1.json")`
- Updating metadata:
  - `update_metadata(doc_id=filename, source=source, country_raw=country_name, year=year, tags=tags, tag_version=tags_version, file_type=file_type, recommendations_list=recs)`
- Year extraction utilities: `extract_year(filename, txt_path, logger)` returns `(year, source)`; use when populating metadata.
- Scraper implementation pattern:
  ```python
  def scrape(**kwargs):
      countries = kwargs.get('countries', [])
      raw_dir = os.path.join("data", "raw", "source_name")
      os.makedirs(raw_dir, exist_ok=True)
      # Download logic here
  ```
- Logging setup:
  ```python
  from processors.logger import get_logger, set_run_logfile
  set_run_logfile("my_operation", module_logs=True)
  logger = get_logger("my_module")
  ```
- Country/region detection: `country_name, country_iso, regions_list = detect_country_region(filename=filename, text=text[:2000])`

What to avoid / non-obvious constraints
- Do not assume filenames are URLs — many scrapers write local filenames; use the `id` (filename) consistently.
- Tests and CI run on Python 3.11/3.12 in different jobs — avoid using bleeding-edge 3.12-only stdlib features without CI verification.
- Avoid writing into `data/` in ways that break existing metadata shape; always go through `update_metadata()` when modifying documents.

If you change or add a scraper
- Add a mapping in `SCRAPER_MAP` in `pipeline_runner.py` and ensure `doc_type` mapping in `DOC_TYPES` and `configs/urls_dict_*` if needed.
- Ensure filenames are stable and documented in metadata so scorecard enrichment can join on `id`.

Where to look first when investigating a bug
- `processors/logger.py` for run logs and set_run_logfile usage.
- `pipeline_runner.py` for orchestration and how data flows between `scrapers/` and `processors/`.
- `processors/json_normalizer.py`, `processors/scorecard_enricher.py`, and `processors/scorecard_export.py` for transformations affecting exports and metadata.
- Common issues:
  - Network timeouts in CI: Check if pre-download step in `.github/workflows/ci.yml` covers the URLs
  - Missing metadata fields: Verify `json_normalizer.normalize_document()` is being called
  - Test failures: Look for mocked `requests` calls vs real network calls in `tests/`
  - Selenium issues: Ensure driver setup in `scrapers/selenium_setup.py` matches CI environment
  - File conversion errors: Check `processors/fallback_handler.py` for unsupported file types

Quick checklist for PRs
- Run `pytest tests/` and `pre-commit run --all-files` locally.
- Add a short entry to `docs/runs/` if behavior of pipeline changes (CI has docs checks).
- Update `configs/` JSON manifest versions if adding or changing tags/recommendations.

If anything here seems incomplete or you want a deeper explanation of a specific area (scrapers, scorecard, tagging), ask and I will expand this file with precise code pointers and examples.
# Copilot Coding Agent Instructions for DigitalChild

## Project Overview

**DigitalChild** (GRIMdata / LittleRainbowRights) is a Python-based pipeline for scraping, processing, and analyzing human rights documents, policies, and reports with focus on child and LGBTQ+ digital protection.

- **Size**: ~30MB, 53 Python files, 24 JSON configs, 27 Markdown docs
- **Language**: Python 3.12
- **Type**: Data pipeline with scrapers, processors, and exporters
- **Key Frameworks**: BeautifulSoup4, Selenium, pandas, pytest
- **CI**: GitHub Actions (Python 3.12, pre-commit hooks, pytest with coverage)

## Build & Test Commands

### Bootstrap (ALWAYS run first on fresh clone)

```bash
python init_project.py
```

Creates directory structure and placeholder files. Safe to re-run (idempotent).

### Install Dependencies

```bash
pip install -r requirements.txt
```

**IMPORTANT**: Always run this after cloning or when requirements.txt changes. The CI installs pytest and pre-commit separately:

```bash
pip install pytest pytest-cov pre-commit
```

### Run Tests

```bash
pytest tests/ -v
```

Run specific test file:

```bash
pytest tests/test_year_extraction.py -v
```

Run with coverage (as CI does):

```bash
pytest tests/ --maxfail=1 --disable-warnings -q --cov=processors --cov=scrapers --cov-report=term-missing
```

**Test execution time**: ~33 seconds for full suite (56 tests).

### Pre-commit Hooks

Install hooks:

```bash
pre-commit install
```

Run all checks:

```bash
pre-commit run --all-files
```

**Pre-commit checks** (ALL must pass for CI):

1. trailing-whitespace
1. end-of-file-fixer
1. check-yaml
1. check-json
1. check-toml
1. check-for-added-large-files
1. detect-private-key
1. **black** (Python formatter, line-length=88)
1. **isort** (import sorter, --profile black)
1. **flake8** (linter, max-line-length=88, ignore E203,E501,W503)
1. **markdownlint** (disable MD013 line-length rule)

### Linting Configuration

- `.flake8`: max-line-length=88, ignore E203,E501,W503
- `.pre-commit-config.yaml`: black 25.1.0, isort 6.0.1, flake8 7.3.0
- Pre-commit uses Python 3.12

### Run Pipeline

Basic run:

```bash
python pipeline_runner.py --source au_policy
```

Demo pipeline (AU policies only):

```bash
python utils/pipeline_runner_DEMO.py
```

Various options:

```bash
# Available tags versions: v1, v2, v3, digital, queerai
python pipeline_runner.py --source au_policy --tags-version v3
python pipeline_runner.py --source au_policy --no-module-logs
python pipeline_runner.py --source upr --country kenya
python pipeline_runner.py --mode scorecard --scorecard-action all
```

**IMPORTANT**: Always run from repository root for imports to work.

## CI Pipeline (.github/workflows/ci.yml)

Two jobs run on push/PR to main, homebase, basecamp branches:

### Job 1: test (Python 3.12, ubuntu-latest)

1. Checkout repository
1. Set up Python 3.12
1. Install dependencies: `pip install -r requirements.txt pytest pytest-cov pre-commit`
1. Run pre-commit: `pre-commit run --all-files --show-diff-on-failure`
1. Run tests: `pytest tests/ --maxfail=1 --disable-warnings -q --cov=processors --cov=scrapers --cov-report=term-missing`

**CRITICAL**: If pre-commit fails, the test job fails. Always run `pre-commit run --all-files` before pushing.

### Job 2: docs (Python 3.11, ubuntu-latest)

1. Checkout repository
1. Set up Python 3.11
1. Install doc tools: `pip install mdformat`
1. Check Markdown: `mdformat --check README.md docs/`

**NOTE**: This job uses Python 3.11 (not 3.12) but only for mdformat.

## Project Architecture

### Directory Structure

```
.
├── pipeline_runner.py          # Main entry point for pipelines
├── init_project.py             # Bootstrap script (creates dirs/files)
├── requirements.txt            # Python dependencies
│
├── scrapers/                   # Web scrapers for document sources
│   ├── au_policy.py           # African Union policy PDFs
│   ├── ohchr.py, upr.py       # UN treaty bodies
│   ├── unicef.py, acerwc.py   # Child-focused sources
│   ├── achpr.py               # African Commission
│   ├── *_sel.py               # Selenium variants of scrapers
│   ├── utils.py               # Shared scraper utilities
│   ├── country_utils.py       # Country normalization
│   └── region_utils.py        # Region detection
│
├── processors/                 # Document processors
│   ├── pdf_to_text.py         # PDF → text conversion
│   ├── docx_to_text.py        # Word → text conversion
│   ├── html_to_text.py        # HTML → text conversion
│   ├── fallback_handler.py    # Try processors in sequence
│   ├── json_normalizer.py     # Normalize country/region names
│   ├── tagger.py              # Apply regex tag rules
│   ├── recommendations.py      # Extract recommendations
│   ├── comparison.py          # Compare tag/rec versions
│   ├── tags_summary.py        # Export CSV summary
│   ├── tags_timeline*.py      # Timeline exports
│   ├── logger.py              # Unified + per-module logging
│   ├── scorecard_*.py         # Scorecard processing
│   └── __init__.py            # Makes processors a package
│
├── configs/                    # JSON configuration files
│   ├── tags_v1.json           # Tag rules version 1
│   ├── tags_v2.json           # Tag rules version 2
│   ├── tags_v3.json           # Tag rules version 3
│   ├── tags_digital.json      # Digital-specific tags
│   ├── tags_main.json         # Main tags config
│   ├── recs_v1.json           # Recommendations config
│   ├── comparison.json        # Comparison config
│   ├── url_dict/              # Static URL dictionaries for processing
│   └── filters/               # Filter configs (countries, regions)
│
├── data/                       # Data directories (mostly .gitignored)
│   ├── raw/                   # Downloaded documents (IGNORED)
│   │   ├── au_policy/
│   │   ├── ohchr/, upr/, unicef/, acerwc/, achpr/
│   │   └── manual/            # Manually uploaded docs
│   ├── processed/             # Converted text/JSON (IGNORED)
│   │   ├── Africa/African_Union/text/
│   │   ├── Global/OHCHR/text/
│   │   └── [region]/[country or org]/text/
│   ├── metadata/              # Metadata tracking (IGNORED)
│   │   └── metadata.json
│   └── exports/               # CSV outputs (IGNORED)
│
├── logs/                       # Runtime logs (IGNORED)
├── utils/                      # Utility scripts
│   └── pipeline_runner_DEMO.py # Demo pipeline
├── tests/                      # Pytest test suite
│   ├── conftest.py            # Adds project root to sys.path
│   ├── test_year_extraction.py
│   ├── test_csv_footer.py
│   ├── test_logging.py
│   ├── test_tagger.py
│   ├── test_fallback_handler.py
│   ├── test_metadata.py
│   ├── test_comparison.py
│   ├── test_country_region.py
│   ├── test_recommendations.py
│   └── test_scorecard.py
└── docs/                       # Extensive documentation
    ├── README.md
    ├── FIRST_RUN_ERRORS.md    # Common setup issues
    ├── ROADMAP.md
    ├── DOCS_INDEX.md
    ├── runs/                  # Run documentation
    ├── standards/             # Format standards
    │   ├── METADATA_SCHEMA.md
    │   ├── FILE_NAMING_STANDARDS.md
    │   ├── TAGS_CONFIG_FORMAT.md
    │   ├── SCRAPER_STRUCTURE.md
    │   └── DOC_TYPE_STANDARDS.md
    └── notes/                 # Technical notes
        ├── PIPELINE_FLOW.md
        ├── PIPELINE_LOGGING.md
        └── DIRECTORY_STRUCTURE.md
```

### Package Structure

- **scrapers/**: NO `__init__.py` (imported directly by module name)
- **processors/**: HAS `__init__.py` to make it a package
- **tests/conftest.py**: Adds project root to sys.path for imports

### Key Configuration Files

- `.flake8`: Linting config (line-length 88, ignore E203,E501,W503)
- `.pre-commit-config.yaml`: Pre-commit hooks config
- `.gitignore`: Excludes data/, logs/, __pycache__, .pytest_cache, etc.
- `requirements.txt`: Production + dev dependencies

## Pipeline Flow

1. **Input**: Scrapers pull documents from web or use static URL dictionaries
1. **Processing**: Convert PDF/DOCX/HTML → text via appropriate processor
1. **Normalization**: Clean country/region names, preserve `_raw` fields
1. **Tagging**: Apply regex rules from `configs/tags_*.json`
1. **Metadata**: Update `data/metadata/metadata.json` with tags history
1. **Export**: Generate CSV summaries in `data/exports/`
1. **Logging**: Unified + per-module logs in `logs/`

## Common Issues & Solutions

### Missing Dependencies

**Error**: `ModuleNotFoundError: No module named 'requests'`\
**Fix**: `pip install -r requirements.txt`

### Metadata File Not Found

**Error**: `FileNotFoundError: data/metadata/metadata.json`\
**Fix**: `python init_project.py`

### Import Errors

**Error**: `ModuleNotFoundError: No module named 'processors'`\
**Fix**: Run commands from project root, not subdirectories

### PyPDF2 Deprecation Warning

Expected warning during tests. The project uses PyPDF2 (will migrate to pypdf later).

### Pre-commit Hook Failures

Always run `pre-commit run --all-files` before committing. Common failures:

- Trailing whitespace → Auto-fixed by hook
- Missing end-of-file newline → Auto-fixed by hook
- Black formatting → Run `pre-commit run black --all-files`
- Isort import order → Run `pre-commit run isort --all-files`
- Flake8 violations → Fix manually per error message
- Markdownlint → Fix manually per error message

## File Naming Standards

Use underscores, include year when available:

- ✅ `AU_Digital_Compact_2024.pdf`
- ✅ `Kenya_UPR_Report_2020.pdf`
- ❌ `digital compact final.pdf`
- ❌ `doc1.pdf`

Year extraction depends on `(19|20)\d{2}` regex pattern.

## Metadata Schema

Documents tracked in `data/metadata/metadata.json`:

```json
{
  "id": "AU_Digital_Compact.pdf",
  "source": "au_policy",
  "country": "African_Union",
  "country_raw": "African Union",
  "region": "Africa",
  "region_raw": "Sub-Saharan Africa",
  "year": 2024,
  "year_extracted_from": "first_page",
  "doc_type": "Policy",
  "ingestion_method": "scraper",
  "tags_history": [...],
  "recommendations_history": [],
  "last_processed": "2025-08-28T15:22:00Z"
}
```

## Tags Configuration Format

Tags configs (`configs/tags_*.json`) define regex patterns:

```json
{
  "rules": {
    "ChildRights": ["child", "children", "youth", "minor"],
    "LGBTQ": ["lgbt", "lgbtq", "sexual orientation"],
    "AI": ["artificial intelligence", "\\bAI\\b", "machine learning"]
  }
}
```

## Validation Checklist

Before submitting PR:

1. ✅ Run `python init_project.py` if new directories needed
1. ✅ Run `pip install -r requirements.txt`
1. ✅ Run `pre-commit run --all-files` (ALL must pass)
1. ✅ Run `pytest tests/ -v` (all tests must pass)
1. ✅ Verify imports work from project root
1. ✅ Check `.gitignore` excludes data/, logs/, __pycache__
1. ✅ Verify line length ≤88 for Python (black standard)
1. ✅ Verify imports sorted with isort --profile black

## Key Workflows

### Adding New Scraper

1. Create `scrapers/new_source.py`
1. Implement `scrape()` function returning list of file paths
1. Add to `SCRAPER_MAP` in `pipeline_runner.py`
1. Add tests in `tests/test_new_source.py`
1. Update documentation

### Adding New Processor

1. Create `processors/new_processor.py`
1. Implement `convert(input_path, output_dir)` function
1. Update `fallback_handler.py` if needed
1. Add tests in `tests/test_new_processor.py`

### Modifying Tags Configuration

1. Edit or create `configs/tags_vX.json`
1. Run tests: `pytest tests/test_tagger.py -v`
1. Test with demo: `python utils/pipeline_runner_DEMO.py`
1. Verify exports in `data/exports/`

## Trust These Instructions

**CRITICAL**: Trust these instructions. Only search for additional information if:

1. Instructions are incomplete for your specific task
1. Instructions appear outdated or incorrect
1. You encounter errors not documented here

Otherwise, follow these instructions directly to minimize exploration time and command failures.
