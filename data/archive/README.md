# Archived Scorecard Files

This directory contains versioned backups and superseded versions of scorecard data files.

## Versioned Backups

These are dated snapshots created when the canonical scorecard is updated:

### `scorecard_main_presentation_2026-01-22.xlsx`

- **Date:** January 22, 2026
- **Status:** Pre-rename archive of presentation file
- **Structure:** 7 sheets (UN_194, SADC, ECOWAS, Global, Sheet1, Sheet5, Sheet2)
- **Note:** Saved before renaming to `data/scorecard/scorecard_main.xlsx`

### `scorecard_2026-01-21.xlsx`

- **Date:** January 21, 2026
- **Status:** Previous root convenience copy
- **Structure:** Single sheet
- **Note:** Archived when new canonical structure adopted

## Superseded Files

### `scorecard_main.xlsx`

- **Date:** January 13, 2025
- **Status:** ARCHIVED - Superseded by later versions
- **Reason:** Less complete data (139/194 AI policies vs 145 in later versions)
- **Structure:** Single sheet, 25 columns, 194 rows

### `scorecard_main_ALL_filled_sources.xlsx`

- **Date:** January 20, 2026
- **Status:** ARCHIVED - Superseded by canonical version
- **Reason:** Less complete than September 2025 presentation file
- **Note:** Name suggests all source URLs filled, but verification incomplete
- **Structure:** Single sheet, 25 columns, 194 rows

## Current Canonical File

The active canonical file is: **`data/scorecard/scorecard_main.xlsx`**

Features:
- 194 countries with 10 indicators each
- Calculated risk indices
- Regional analysis breakdowns (SADC, ECOWAS)
- Color-coded groupings
- 7 sheets total

A convenience copy is maintained at `scorecard.xlsx` (root) for quick reference.

## Archiving Process

When the canonical file is updated:

1. Read "Last Updated" date from existing `scorecard.xlsx` (root)
2. Archive `scorecard.xlsx` → `data/archive/scorecard_YYYY-MM-DD.xlsx`
3. Copy new canonical → `scorecard.xlsx` (root)
4. Update date metadata in canonical file
