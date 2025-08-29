# Project Directory Structure

This document explains the purpose of each folder and subfolder.

---

## Top-Level

- `pipeline_runner.py` → Entry point for running pipelines.
- `requirements.txt` → Python dependencies.
- `.github/workflows/ci.yml` → GitHub Actions CI pipeline.

---

## Scrapers

- `scrapers/` → Code for fetching raw documents from sources.
  - `au_policy.py` → AU PDFs.
  - `ohchr_tb.py`, `upr.py`, etc. → placeholders for other treaty bodies.

---

## Processors

- `processors/` → Code for processing raw documents.
  - `pdf_to_text.py` → PDF → text.
  - `docx_to_text.py` → DOCX → text.
  - `html_to_text.py` → HTML → text.
  - `fallback_handler.py` → Tries multiple processors.
  - `tagger.py` → Applies tag rules.
  - `tags_summary.py` → Produces CSV summary.

---

## Configs

- `configs/` → JSON config files for tags and filters.
  - `tags_v1.json`, `tags_v2.json`, `tags_v3.json`, `tags_digital.json`.
  - `tags_master.json` → points to versions.
  - `filters/` → filter configs.

---

## Data

- `data/raw/` → Source documents as scraped or uploaded.
- `data/processed/` → Converted text, json, or OCR.
- `data/metadata/metadata.json` → Central metadata file.
- `data/exports/` → Output summaries, comparisons, timelines.

---

## Logs

- `logs/` → Unified and per-module logs per run.

---

## Docs

- `docs/` → Documentation files (setup, standards, notes).

---

## Tests

- `tests/` → Unit tests and integration tests.
