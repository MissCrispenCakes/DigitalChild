---
🌍 Project Domains:
- https://GRIMdata.org
- https://ALLRainbowRights.com
- https://LittleRainbowRights.com
---

# PIPELINE FLOW

This document explains the flow of data through the pipeline.

---

## 1. Input Sources

- **Scrapers** pull content from:
  - AU policy PDFs (demo implemented)
  - OHCHR Treaty Body Database (planned)
  - UPR, UNICEF, ACERWC, ACHPR (planned)

- **Manual files** can be dropped into `data/raw/manual/`.

---

## 2. Processing

- **File type detection**
  Attempt to process based on extension.
  - `.pdf` → `pdf_to_text.py`
  - `.docx` → `docx_to_text.py`
  - `.html` → `html_to_text.py`
  - Fallback → try processors in order until success.

- **Normalization**
  `json_normalizer.py` cleans country/region names.
  Preserves `_raw` fields for provenance.

- **Tagging**
  `tagger.py` applies regex rules from `configs/tags_v1.json`.
  Tags are stored in `tags_history` in `metadata.json`.

- **Recommendations**
  (future) Config-driven extraction of recommendations.

---

## 3. Metadata

- `metadata.json` tracks:
  - Project identity
  - Documents ingested
  - Tags history (with versions)
  - Recommendations history (with versions)
  - Last processed timestamp

---

## 4. Exports

- `tags_summary.py` → counts tags, outputs CSV with branding footer
- `tags_timeline*.py` → (future) timeline exports
- `comparison.py` → (future) compare tagging/recommendations across versions

---

## 5. Logging

- `logger.py` provides unified + per-module logging
- Controlled via `--no-module-logs` flag in `pipeline_runner.py`
- Logs written to `logs/` directory

---

## 6. Review

- Researchers can inspect:
  - Raw files in `data/raw/`
  - Processed text in `data/processed/`
  - Metadata in `data/metadata/metadata.json`
  - Exports in `data/exports/`
  - Logs in `logs/`
