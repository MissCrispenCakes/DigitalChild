# DigitalChild Project

## GRIMdata / LittleRainbowRights Pipeline

[![CI Pipeline](https://github.com/MissCrispenCakes/DigitalChild/actions/workflows/ci.yml/badge.svg)](https://github.com/MissCrispenCakes/DigitalChild/actions/workflows/ci.yml)
[![Docs Health](https://img.shields.io/badge/docs-health-brightgreen)](docs/runs/FIRST_RUN_ERRORS.md)
![Coverage Status](https://img.shields.io/badge/coverage-auto--generated-lightgrey)

Pipeline for scraping, processing, and analyzing, human rights documents,
policies, and reports, with a focus on child and LGBTQ+ digital protection.

______________________________________________________________________

## 🚀 Quickstart

```bash
python init_project.py
pip install -r requirements.txt
python pipeline_runner.py
```

Exports will appear under `data/exports/`.

______________________________________________________________________

## 📋 Project Status

**Phase 1-2 Complete:**

- ✅ Core pipeline (scraping, processing, tagging) - 7 sources supported
- ✅ Scorecard system - 194 countries, 10 indicators, 2,543 source URLs tracked
- ✅ Validation & security framework - 68 validator tests, 124 total tests passing
- ✅ Comprehensive documentation - 25 markdown files

**Phase 3 In Progress:** Recommendations extraction, timeline exports, comparison analytics

See [docs/ROADMAP.md](docs/ROADMAP.md) for detailed feature roadmap and future phases.

______________________________________________________________________

## 🛠 Troubleshooting

If you hit issues during setup or first run, see the:
[First Run Error Checklist](docs/runs/FIRST_RUN_ERRORS.md).

______________________________________________________________________

## 🐈🐱🐈💻 Developer Setup

Install pre-commit to catch formatting and docs issues before pushing:

```bash
pip install pre-commit
pre-commit install
```

Now, whenever you commit, pre-commit will:

- Format Markdown files (mdformat)
- Check YAML syntax
- Fix trailing whitespace
- Validate Markdown links (with markdown-link-checker)
