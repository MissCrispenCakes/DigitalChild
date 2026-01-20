# First Run Errors Guide

This file documents common issues when running the pipeline for the first time.

______________________________________________________________________

## 🟢 Missing Dependencies

**Error:** `ModuleNotFoundError: No module named 'requests'`
**Fix:** Install requirements.

```bash
pip install -r requirements.txt
```

______________________________________________________________________

## 🟢 Pandoc / PDF Generation

**Error:** `pdflatex not found`
**Cause:** Pandoc tries to use LaTeX to generate PDFs.
**Fix:** The pipeline does not require Pandoc. Use ReportLab for generating test PDFs.

```bash
pip install reportlab
```

______________________________________________________________________

## 🟢 Metadata Errors

**Error:** `FileNotFoundError: data/metadata/metadata.json`
**Fix:** Run `init_project.py` to create scaffolding.

```bash
python init_project.py
```

______________________________________________________________________

## 🟢 Logging Issues

**Symptom:** No logs appear in `logs/`
**Fix:** Ensure `pipeline_runner.py` is invoked from project root.

```bash
python pipeline_runner.py --source au_policy
```

______________________________________________________________________

## 🟢 Import Errors

**Error:** `ModuleNotFoundError: No module named 'processors'`
**Fix:** Run commands from project root.

```bash
pytest tests/ -v
```

______________________________________________________________________

## 🟢 Virtual Environment Not Activated

**Symptom:** Dependencies not found even after `pip install -r requirements.txt`
**Cause:** Virtual environment not activated.
**Fix:** Activate the virtual environment.

```bash
source .LittleRainbow/bin/activate  # Linux/Mac
# OR
.LittleRainbow\Scripts\activate  # Windows
```

______________________________________________________________________

## 🟢 Python Version Mismatch

**Error:** `SyntaxError` or features not available
**Cause:** Project requires Python 3.12.
**Fix:** Check Python version and upgrade if needed.

```bash
python --version  # Should show Python 3.12.x
# If not, install Python 3.12 and recreate venv
```

______________________________________________________________________

## 🟢 Pre-commit Hook Failures

**Error:** `black` or `flake8` failures during commit
**Cause:** Code doesn't meet formatting standards.
**Fix:** Run pre-commit to auto-fix issues.

```bash
pre-commit run --all-files
# Review changes and commit again
```

______________________________________________________________________

## 🟢 Test Failures

**Error:** Tests fail with `AssertionError` or other exceptions
**Fix:** Run tests with verbose output to see details.

```bash
pytest tests/ -v --tb=long
# Run specific failing test
pytest tests/test_validators.py::TestURLValidation::test_validate_url_valid_https -vv
```

______________________________________________________________________

## 🟢 Scorecard File Not Found

**Error:** `FileNotFoundError: scorecard_main.xlsx`
**Cause:** Scorecard Excel file missing or in wrong location.
**Fix:** Ensure `scorecard_main.xlsx` is in project root.

```bash
ls -la scorecard_main.xlsx  # Should exist in project root
```

______________________________________________________________________

## 🟢 Selenium/Browser Driver Issues

**Error:** `WebDriverException: chromedriver not found`
**Cause:** Selenium scrapers (\_sel variants) need browser drivers.
**Fix:** Use non-Selenium scrapers or install ChromeDriver.

```bash
# Use regular scraper (no Selenium)
python pipeline_runner.py --source au_policy

# Or install ChromeDriver for Selenium scrapers
# See: https://chromedriver.chromium.org/downloads
```

______________________________________________________________________

## 🟢 Permission Denied Errors

**Error:** `PermissionError: [Errno 13] Permission denied`
**Cause:** Insufficient permissions to write files or create directories.
**Fix:** Check directory permissions.

```bash
# Ensure data directories are writable
chmod -R u+w data/ logs/

# Or run init_project.py again
python init_project.py
```
