# Project README

## GRIMdata / LittleRainbowRights / ALLRainbowRights Pipeline

[![CI Pipeline](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/ci.yml)
[![Docs Health](https://img.shields.io/badge/docs-health-brightgreen)](docs/FIRST_RUN_ERRORS.md)
![Coverage Status](https://img.shields.io/badge/coverage-auto--generated-lightgrey)

Pipeline for scraping, processing, and analyzing human rights documents,
policies, and reports with a focus on child and LGBTQ+ digital protection.

---

## 🚀 Quickstart

``` bash
python init_project.py
pip install -r requirements.txt
python pipeline_runner.py
```

Exports will appear under `data/exports/`.

---

## 🛠 Troubleshooting

If you hit issues during setup or first run, see the:
[First Run Error Checklist](docs/runs/FIRST_RUN_ERRORS.md).

---

## 🐈🐱🐈💻 Developer Setup

Install pre-commit to catch formatting and docs issues before pushing:

``` bash
pip install pre-commit
pre-commit install
```

Now, whenever you commit, pre-commit will:

- Format Markdown files (mdformat)
- Check YAML syntax
- Fix trailing whitespace
- Validate Markdown links (with markdown-link-checker)
