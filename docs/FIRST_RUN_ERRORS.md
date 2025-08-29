# First Run Errors Guide

This file documents common issues when running the pipeline for the first time.

---

## 🟢 Missing Dependencies

**Error:** `ModuleNotFoundError: No module named 'requests'`  
**Fix:** Install requirements.  
(bash)
pip install -r requirements.txt

---

## 🟢 Pandoc / PDF Generation

**Error:** `pdflatex not found`  
**Cause:** Pandoc tries to use LaTeX to generate PDFs.  
**Fix:** The pipeline does not require Pandoc. Use ReportLab for generating test PDFs.  
(bash)
pip install reportlab

---

## 🟢 Metadata Errors

**Error:** `FileNotFoundError: data/metadata/metadata.json`  
**Fix:** Run `python init_project.py` to create scaffolding.

---

## 🟢 Logging Issues

**Symptom:** No logs appear in `logs/`  
**Fix:** Ensure `pipeline_runner.py` is invoked from project root.  
(bash)
python pipeline_runner.py --source au_policy

---

## 🟢 Import Errors

**Error:** `ModuleNotFoundError: No module named 'processors'`  
**Fix:** Run commands from project root.  
(bash)
pytest tests/ -v
