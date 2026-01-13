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
