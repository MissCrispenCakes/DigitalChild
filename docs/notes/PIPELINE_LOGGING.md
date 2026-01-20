# Pipeline Logging

This document describes the logging system for the pipeline.

______________________________________________________________________

## Logger Design

- Implemented in `processors/logger.py`.
- Supports:
  - Console output
  - Unified run log file
  - Optional per-module log files

______________________________________________________________________

## Unified Run Log

- Named as `<timestamp>_<pipeline>.log`
- Example: `2025-08-28_12-22-40_au_policy_run.log`

______________________________________________________________________

## Module Logs

- Each module (scraper, processor) may also have its own log file.
- Controlled by `--no-module-logs` flag in `pipeline_runner.py`.

______________________________________________________________________

## Levels

- `INFO` → normal progress (scraping, processing, tagging)
- `WARNING` → recoverable issues (year not found, missing tag matches)
- `ERROR` → non-recoverable (download failure, unreadable PDF)

______________________________________________________________________

## Best Practices

- Always run from project root so log paths resolve correctly.
- Logs are stored in `logs/`.
- Do not commit logs to Git (ignored via `.gitignore`).
