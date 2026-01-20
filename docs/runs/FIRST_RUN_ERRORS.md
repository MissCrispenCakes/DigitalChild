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
