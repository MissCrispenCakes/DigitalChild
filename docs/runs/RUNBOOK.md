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
python utils/pipeline_runner_DEMO.py
```

---

## 🟢 Run Pipeline

Sample runs varied inputs:

``` bash
python pipeline_runner.py --no-module-logs

python pipeline_runner.py --source au_policy --tags-version latest
python pipeline_runner.py --source au_policy --tags-version v1 --no-module-logs
python pipeline_runner.py --source au_policy --tags-version latest

python pipeline_runner.py --source ohchr
python pipeline_runner.py --source upr
python pipeline_runner.py --source unicef

python pipeline_runner.py --source acerwc
python pipeline_runner.py --source acerwc --base-url https://au.int/en/documents/acerwc-42-session
python pipeline_runner.py --source achpr --base-url https://www.achpr.org/communications

python pipeline_runner.py --source unicef --base-url https://www.unicef.org/digital-reports

python pipeline_runner.py --source upr --country kenya
python pipeline_runner.py --source upr --base-url https://www.ohchr.org/en/hr-bodies/upr --country kenya

python pipeline_runner.py --source upr --countries-file configs/countries/upr_countries.txt

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
