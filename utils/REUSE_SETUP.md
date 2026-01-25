# REUSE Compliance Setup

This directory contains scripts to set up [REUSE](https://reuse.software) compliance for the DigitalChild project.

## What is REUSE?

REUSE is a specification from the Free Software Foundation Europe (FSFE) for declaring copyright and licenses in a standardized, machine-readable way. It makes licensing crystal clear, especially for projects with multiple licenses (like our dual MIT/CC-BY-4.0 setup).

## Why Add REUSE Compliance?

1. **Already 70% there** - We have docstrings in Python files and footers in CSV exports
2. **Professional standard** - Used by Linux Foundation, KDE, Nextcloud, and other major projects
3. **Clear per-file licensing** - Each file explicitly declares its license
4. **Machine-readable** - Tools can automatically verify compliance
5. **Better than current LICENSE files** - GitHub shows "Unknown" for dual licensing; REUSE fixes this

## Quick Start

### Option 1: Master Script (Recommended)

Run everything at once:

```bash
# Preview changes (dry run)
bash utils/setup_reuse_all.sh --dry-run

# Apply all changes
bash utils/setup_reuse_all.sh
```

### Option 2: Step by Step

Run each script individually:

```bash
# 1. Create LICENSES/ directory and .reuse/dep5 file
python utils/setup_reuse.py

# 2. Add SPDX headers to Python files (preview first)
python utils/add_spdx_headers.py --dry-run
python utils/add_spdx_headers.py

# 3. Add license info to CSV footers
python utils/update_csv_licenses.py --dry-run
python utils/update_csv_licenses.py
```

## What Changes Will Be Made?

### 1. LICENSES/ Directory

Creates `LICENSES/` with official license texts:

```
LICENSES/
  MIT.txt         # Full MIT license text
  CC-BY-4.0.txt   # Full CC BY 4.0 text (from LICENSE-DATA)
```

### 2. .reuse/dep5 File

Bulk license declarations for files that can't have headers:

```
.reuse/
  dep5  # Declares licenses for *.md, *.json, *.xlsx, etc.
```

### 3. SPDX Headers in Python Files

Adds headers to all `.py` files:

```python
# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights
# SPDX-License-Identifier: MIT

"""
Your existing docstring
"""
```

### 4. CSV Export License Footers

Updates CSV export functions to include:

```csv
# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights
# SPDX-License-Identifier: CC-BY-4.0

# Project: GRIMdata / LittleRainbowRights
# ... (existing footer)
```

### 5. Updated .gitignore

Adds `.reuse/` to ignore REUSE tool cache.

## Files Modified

- **~100 Python files** - SPDX headers added at top
- **3 CSV export functions** - License lines added to footers
  - `processors/tags_summary.py`
  - `processors/scorecard_export.py`
  - `processors/comparison_export.py`
- **New directories**:
  - `LICENSES/`
  - `.reuse/`
- **Updated**: `.gitignore`

## After Running Scripts

### 1. Verify Changes

```bash
git status
git diff
```

### 2. Install REUSE Tool

```bash
pip install reuse
```

### 3. Run REUSE Linter

```bash
reuse lint
```

Expected output:
```
✓ All files have license information
✓ Licenses are valid
✓ All files have copyright information
```

### 4. Add REUSE Badge to README

Add this badge to the top of README.md:

```markdown
[![REUSE status](https://api.reuse.software/badge/github.com/MissCrispenCakes/DigitalChild)](https://api.reuse.software/info/github.com/MissCrispenCakes/DigitalChild)
```

### 5. Commit Changes

```bash
git add -A
git commit -m "Add REUSE compliance (SPDX headers, LICENSES/ directory)

- Add SPDX-FileCopyrightText and SPDX-License-Identifier to all Python files
- Create LICENSES/ directory with MIT.txt and CC-BY-4.0.txt
- Add .reuse/dep5 for bulk declarations (docs, configs, data)
- Update CSV export functions to include license in footers
- Comply with REUSE 3.0 specification

This makes licensing crystal clear per-file and machine-readable.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

git push
```

## License Mapping

| Files | License |
|-------|---------|
| Python code (`.py`) | MIT |
| Documentation (`.md`, `docs/`) | CC BY 4.0 |
| Configs, data exports | CC BY 4.0 |
| Scorecard data (`.xlsx`) | CC BY 4.0 |
| Raw scraped data (`data/raw/`) | Public Domain (from sources) |
| GitHub Actions, build files | MIT |

## Rollback (If Needed)

If you need to undo changes:

```bash
# Restore from last commit
git checkout HEAD -- .

# Or reset specific files
git checkout HEAD -- processors/ scrapers/ api/
```

## Troubleshooting

### "ModuleNotFoundError" when running scripts

Make sure you're in the project root:

```bash
cd /path/to/DigitalChild
python utils/setup_reuse.py
```

### REUSE lint shows errors

Common issues:

1. **Missing license file**: Add missing license to `LICENSES/`
2. **Missing copyright**: Add to `.reuse/dep5` or file header
3. **Invalid SPDX identifier**: Use exact names from https://spdx.org/licenses/

### Scripts skip all files

Files already have SPDX headers. Check with:

```bash
head -5 processors/tagger.py
```

If you see `SPDX-License-Identifier`, headers are already present.

## Learn More

- **REUSE Website**: https://reuse.software
- **REUSE Tutorial**: https://reuse.software/tutorial/
- **REUSE FAQ**: https://reuse.software/faq/
- **SPDX License List**: https://spdx.org/licenses/

## Support

Questions? Check:
1. This README
2. REUSE documentation: https://reuse.software/tutorial/
3. GitHub Discussions: https://github.com/MissCrispenCakes/DigitalChild/discussions
