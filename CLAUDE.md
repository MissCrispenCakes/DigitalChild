# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## ⚠️ CRITICAL: Before Every Commit

**READ `CLAUDE_PRE_COMMIT_CHECKLIST.md` BEFORE EVERY COMMIT**

ALWAYS run before committing:

```bash
pre-commit run --all-files
```

**Every CI failure costs money. Every failed push wastes time. CHECK BEFORE YOU PUSH.**

## Project Overview

DigitalChild (GRIMdata / LittleRainbowRights) is a Python 3.12 data pipeline for scraping, processing, and analyzing human rights documents, policies, and reports with focus on child and LGBTQ+ digital protection.

**Key Tech**: BeautifulSoup4, Selenium, pandas, pypdf, pytest, Flask (API backend)

## Essential Commands

### Bootstrap (ALWAYS run first on fresh clone)

```bash
python init_project.py
```

Creates directory structure and placeholder files. Safe to re-run (idempotent).

### Install Dependencies

```bash
pip install -r requirements.txt
```

For CI/development, also install:

```bash
pip install pytest pytest-cov pre-commit
```

For API development (Phase 4):

```bash
pip install -r api_requirements.txt
```

### Pre-commit Setup

Install hooks (REQUIRED before committing):

```bash
pre-commit install
```

Run all checks (MUST pass before pushing):

```bash
pre-commit run --all-files
```

Pre-commit runs: black, isort, flake8, markdownlint, trailing-whitespace, end-of-file-fixer, check-yaml, check-json, detect-private-key.

**Linting config**: Line length 88 (black standard), flake8 ignores E203,E501,W503.

### Run Tests

**IMPORTANT:** Activate virtual environment first to ensure all dependencies (pypdf, python-docx) are available.

```bash
# Activate virtual environment
source .LittleRainbow/bin/activate  # On Windows: .LittleRainbow\Scripts\activate

# Full test suite (~106 seconds, 347 tests)
pytest tests/ -v

# Specific test file
pytest tests/test_year_extraction.py -v

# With coverage (as CI does)
pytest tests/ --maxfail=1 --disable-warnings -q --cov=processors --cov=scrapers --cov-report=term-missing
```

### Run Pipeline

```bash
# Basic run (AU policies)
python pipeline_runner.py --source au_policy

# With options
python pipeline_runner.py --source au_policy --tags-version latest
python pipeline_runner.py --source upr --country kenya
python pipeline_runner.py --mode scorecard --scorecard-action all

# Demo pipeline
python utils/pipeline_runner_DEMO.py
```

**IMPORTANT**: Always run from repository root for imports to work.

### Run API (Phase 4)

```bash
# Install API dependencies
pip install -r api_requirements.txt

# Run development server
python run_api.py

# Test API endpoints
python test_api.py

# Quick curl test
curl http://localhost:5000/api/health
```

API available at `http://127.0.0.1:5000`. See [api/README.md](api/README.md) for endpoint documentation.

## Architecture

### Pipeline Flow

```
Scraper → Raw Files → Processor → Text → Tagger → Metadata → Exports
```

1. **Scrapers** (`scrapers/`) fetch documents from web sources → `data/raw/[source]/`
1. **Processors** (`processors/`) convert PDFs/DOCX/HTML to text → `data/processed/[region]/[org]/text/`
1. **Tagger** applies regex rules from `configs/tags_*.json`
1. **Metadata** stored in `data/metadata/metadata.json` (tracks tags history, recommendations)
1. **Exports** generate CSV summaries in `data/exports/`

### Key Components

**pipeline_runner.py** - Main entry point with three modes:

- `scraper` mode: Run scrapers, process docs, tag, export
- `urls` mode: Process from static URL dictionaries in `configs/url_dict/`
- `scorecard` mode: Enrich/export/validate scorecard data

**SCRAPER_MAP** in pipeline_runner.py:46-60 maps source names to:

- Scraper module
- Output directory path
- Document type

Each source has both a requests-based scraper and a Selenium variant (`_sel` suffix).

**Fallback Handler** (`processors/fallback_handler.py`):

- Tries processors in sequence until one succeeds
- Used for unknown file types

**Year Extraction** (pipeline_runner.py:212-244):

- Pattern: `(19|20)\d{2}` with boundary checks
- Sources: filename first, then first 1000 chars of text

**Country/Region Detection** (`utils/detectors.py`):

- Uses filename, URL keys, and text content
- Normalizes via `json_normalizer.py` (preserves `_raw` fields)

### Scorecard System

Separate workflow for country-level indicators (10 metrics per country):

1. **Load**: `processors/scorecard.py` reads `data/scorecard/scorecard_main.xlsx` (canonical source)
1. **Enrich**: `processors/scorecard_enricher.py` adds indicators to document metadata
1. **Export**: `processors/scorecard_export.py` generates CSV exports
1. **Validate**: `processors/scorecard_validator.py` checks source URLs
1. **Diff**: `processors/scorecard_diff.py` monitors sources for changes

Run scorecard workflow:

```bash
python pipeline_runner.py --mode scorecard --scorecard-action all
```

Or individual steps:

```bash
python processors/scorecard_enricher.py
python -c "from processors.scorecard_export import export_scorecard; export_scorecard()"
```

### Website Visualizations & Transparency Watch

The GRIMdata site (`docs/`, Material for MkDocs) deploys to GitHub Pages on push
to `basecamp` (via `.github/workflows/deploy-docs.yml`). Its interactive features
are **static** — driven by published JSON, no server required — produced by two
**read-only generators** that write ONLY into `docs/` (they never modify
canonical sources):

- `utils/build_scorecard_viz_data.py` → `docs/scorecard/data/scorecard.json`.
  Drives the scorecard map/charts/explorer (`docs/website/javascripts/scorecard.js`).
  Reads scores from the **`Heatmap`/`Scorecard` sheets of
  `Global_QueerAI_Child_Scorecard_MASTER.xlsx`** (the designated visualization
  workbook — note this differs from the pipeline's canonical `scorecard_main.xlsx`),
  plus region + per-indicator source URLs from `scorecard_main.xlsx`.
- `utils/build_transparency_watch_data.py` → `docs/transparency-watch/data/transparency.json`.
  Drives the Source Transparency Watch (`docs/website/javascripts/transparency.js`).
  Engine: Internet Archive Wayback CDX (first-seen of transparency-signal URLs per
  monitored peer domain). Edit the `SOURCES` list to add monitored orgs.

To update the live site: re-run the relevant generator, commit the regenerated
JSON, and push to `basecamp`. Dead/disappeared external sources are recorded in
`docs/maintenance/SOURCE_AVAILABILITY_LOG.md`.

### Package Structure

- **scrapers/**: NO `__init__.py` (modules imported directly by name)
- **processors/**: HAS `__init__.py` (proper package)
- **tests/conftest.py**: Adds project root to sys.path for imports

### Metadata Schema

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
  "file_type": "PDF",
  "ingestion_method": "scraper",
  "tags_history": [
    {
      "tags": ["AI", "DigitalPolicy"],
      "version": "tags_v3",
      "timestamp": "2025-08-28T15:22:00Z"
    }
  ],
  "recommendations_history": [],
  "scorecard": {
    "matched_country": "Albania",
    "enriched_at": "2024-01-15T10:30:00Z",
    "indicators": {
      "AI_Policy_Status": {"value": "...", "source": "..."},
      ...
    }
  },
  "last_processed": "2025-08-28T15:22:00Z"
}
```

### Tags Configuration

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

Version resolution via `configs/tags_main.json`:

```json
{
  "versions": {
    "latest": "tags_v3.json",
    "v1": "tags_v1.json",
    "v2": "tags_v2.json"
  }
}
```

### Logging System

Unified + per-module logging (`processors/logger.py`):

```python
from processors.logger import get_logger, set_run_logfile

# At pipeline start
set_run_logfile("source_run", module_logs=True)  # Creates logs/source_run.log

# In modules
logger = get_logger("module_name")
logger.info("Message")
```

Disable module logs with `--no-module-logs` flag.

## CI Pipeline

GitHub Actions runs on push/PR to `main`, `homebase`, `basecamp` branches.

**Job 1: test** (Python 3.12, ubuntu-latest)

1. Install deps: `pip install -r requirements.txt pytest pytest-cov pre-commit`
1. Run pre-commit: `pre-commit run --all-files --show-diff-on-failure`
1. Run tests: `pytest tests/ --maxfail=1 --disable-warnings -q --cov=processors --cov=scrapers --cov-report=term-missing`

**Job 2: docs** (Python 3.11, ubuntu-latest)

1. Install: `pip install mdformat`
1. Check: `mdformat --check README.md docs/`

**CRITICAL**: If pre-commit fails, CI fails. Always run `pre-commit run --all-files` before pushing.

## Common Development Tasks

### Add New Scraper

1. Create `scrapers/new_source.py`
1. Implement `scrape()` function returning list of file paths
1. Add to `SCRAPER_MAP` in `pipeline_runner.py`
1. Add tests in `tests/test_new_source.py`

Scraper template:

```python
# scrapers/new_source.py
import os
import requests
from processors.logger import get_logger

RAW_DIR = "data/raw/new_source"
logger = get_logger(__name__)

def scrape(base_url=None, countries=None):
    """Download documents to RAW_DIR. Returns list of file paths."""
    os.makedirs(RAW_DIR, exist_ok=True)
    downloaded = []

    # Your scraping logic here
    for name, url in URLS.items():
        filepath = os.path.join(RAW_DIR, f"{name}.pdf")
        if os.path.exists(filepath):
            logger.info(f"Skipping (exists): {filepath}")
            continue

        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        with open(filepath, "wb") as f:
            f.write(resp.content)
        downloaded.append(filepath)

    return downloaded
```

### Add New Processor

1. Create `processors/new_processor.py`
1. Implement `convert(input_path, output_dir)` function
1. Update `fallback_handler.py` if needed
1. Add tests in `tests/test_new_processor.py`

Processor template:

```python
# processors/new_processor.py
import os
from processors.logger import get_logger

logger = get_logger(__name__)

def convert(input_path, output_dir):
    """
    Convert input file to text.
    Returns path to .txt file or None if failed.
    """
    os.makedirs(output_dir, exist_ok=True)
    basename = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(output_dir, f"{basename}.txt")

    try:
        # Your conversion logic here
        text = extract_text(input_path)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        return output_path
    except Exception as e:
        logger.error(f"Conversion failed for {input_path}: {e}")
        return None
```

### Modify Tags Configuration

1. Edit or create `configs/tags_vX.json`
1. Update version mapping in `configs/tags_main.json` if needed
1. Run tests: `pytest tests/test_tagger.py -v`
1. Test with demo: `python utils/pipeline_runner_DEMO.py`
1. Verify exports in `data/exports/`

### Update Scorecard Data

1. Edit `data/scorecard/scorecard_main.xlsx` (canonical source) with new data
1. Re-enrich: `python processors/scorecard_enricher.py`
1. Re-export: `python -c "from processors.scorecard_export import export_scorecard; export_scorecard()"`
1. Validate: `python processors/scorecard_validator.py`
1. Update convenience copy: `cp data/scorecard/scorecard_main.xlsx scorecard.xlsx`

## File Naming Standards

Use underscores, include year when available:

- ✅ `AU_Digital_Compact_2024.pdf`
- ✅ `Kenya_UPR_Report_2020.pdf`
- ❌ `digital compact final.pdf` (spaces, no year)
- ❌ `doc1.pdf` (non-descriptive)

Year extraction depends on `(19|20)\d{2}` regex with boundary checks.

## Common Issues

### Missing Dependencies

Error: `ModuleNotFoundError: No module named 'requests'`
Fix: `pip install -r requirements.txt`

### Metadata File Not Found

Error: `FileNotFoundError: data/metadata/metadata.json`
Fix: `python init_project.py`

### Import Errors

Error: `ModuleNotFoundError: No module named 'processors'`
Fix: Run commands from project root, not subdirectories

### Pre-commit Hook Failures

Always run `pre-commit run --all-files` before committing. Common auto-fixes:

- Trailing whitespace
- Missing end-of-file newline
- Black formatting: `pre-commit run black --all-files`
- Import order: `pre-commit run isort --all-files`

## Important Context from .github/copilot-instructions.md

- **ALWAYS** run `python init_project.py` on fresh clone
- Test suite takes ~106 seconds for 347 tests
- pypdf deprecation warning is expected (migration to pypdf planned)
- Pre-commit hooks are CRITICAL - CI fails if they fail
- Line length: 88 characters (black standard)
- Import sorting: isort with `--profile black`
- Scrapers have NO `__init__.py`, processors HAVE `__init__.py`
- Use `from processors.logger import get_logger` for logging
- Country/region normalization preserves `_raw` fields for provenance
- Tags history tracks versions and timestamps
- Scorecard enrichment is separate from main pipeline
- Static URL dictionaries live in `configs/url_dict/`
- All data directories (`data/raw/`, `data/processed/`, `data/exports/`, `logs/`) are gitignored

## Documentation References

- `docs/guides/FIRST_RUN_ERRORS.md` - Troubleshooting first run
- `docs/notes/PIPELINE_FLOW.md` - Detailed pipeline flow
- `docs/guides/SCORECARD_WORKFLOW.md` - Complete scorecard system guide
- `docs/standards/METADATA_SCHEMA.md` - Metadata structure
- `docs/standards/TAGS_CONFIG_FORMAT.md` - Tags configuration format
- `docs/standards/SCRAPER_STRUCTURE.md` - Scraper implementation guide
- `docs/standards/FILE_NAMING_STANDARDS.md` - File naming conventions
- `docs/notes/PIPELINE_LOGGING.md` - Logging system details
