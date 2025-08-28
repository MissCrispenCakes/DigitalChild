---
🌍 Project Domains:
- https://GRIMdata.org
- https://ALLRainbowRights.com
- https://LittleRainbowRights.com
---

# RUNBOOK: Commands to Run Pipelines and Tools

This document lists commands for running the pipeline and tools.
It is **for execution** only (not dev notes).

---

## 🟢 Bootstrap Project

``` bash
python init_project.py
```

---

## 🟢 Install Requirements

``` bash
pip install -r requirements.txt
```

---

## 🟢 Run AU Policy Demo Pipeline

Default (unified + module logs):

``` bash
python pipeline_runner.py
```

Unified log only:

``` bash
python pipeline_runner.py --no-module-logs
```

---

## 🟢 Run Tests

``` bash
pytest tests/ -v
```

Run a specific test:

``` bash
pytest tests/test_year_extraction.py -v
```

---

## 🟢 Run Logging Tests

``` bash
pytest tests/test_logging.py -v
```

---

## 🟢 Pre-commit Checks

``` bash
pre-commit run --all-files
```
