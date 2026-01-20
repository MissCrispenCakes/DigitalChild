# DigitalChild

### GRIMdata / LittleRainbowRights

[![CI Pipeline](https://github.com/MissCrispenCakes/DigitalChild/actions/workflows/ci.yml/badge.svg?branch=basecamp)](https://github.com/MissCrispenCakes/DigitalChild/actions/workflows/ci.yml)
[![Docs Health](https://img.shields.io/badge/docs-health-brightgreen)](docs/guides/FIRST_RUN_ERRORS.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Data License: CC BY 4.0](https://img.shields.io/badge/Data%20License-CC%20BY%204.0-lightgrey.svg)](LICENSE-DATA)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)

**Open-source data pipeline for analyzing human rights documents with focus on child and LGBTQ+ digital protection.**

Scrape, process, tag, and analyze policy documents from international organizations. Track 10 human rights indicators across 194 countries. Support evidence-based advocacy and research.

🌍 **Website:** [GRIMdata.org](https://grimdata.org) | [LittleRainbowRights.com](https://littlerainbowrights.com)
📖 **Documentation:** [docs/](docs/)
💬 **Discussions:** [GitHub Discussions](https://github.com/MissCrispenCakes/DigitalChild/discussions)

______________________________________________________________________

## ✨ Key Features

### 📥 Data Collection

- **Multiple data sources** - International organizations (UN, AU), treaty bodies (OHCHR, UPR, UNICEF, ACERWC, ACHPR), government sources, NGOs, legal databases, research publications
- **Global and regional coverage** - African, global, and country-specific sources across multiple regions
- **Direct URL tracking** - Government postings, public notices, community organizations, business/legal sources, policy documents
- **Multi-format support** - PDF, DOCX, HTML document processing
- **Automated scraping** - Respectful, rate-limited web scraping with fallback handlers

### 🏷️ Analysis & Tagging

- **Regex-based tagging** - Identify child rights, LGBTQ+, AI, privacy, and digital policy themes
- **Versioned tags** - Compare results across different tag rule sets
- **Tags history** - Track all tagging operations with timestamps

### 📊 Scorecard System

- **194 countries** tracked with 10 human rights indicators
- **2,543 source URLs** - Authoritative sources from UNESCO, UNCTAD, ILGA, UNICEF, etc.
- **Automated validation** - Check source URLs for availability, detect changes
- **CSV exports** - Summary tables, by-indicator breakdowns, regional analysis

### 🔒 Security & Validation

- **68 validator tests** - Comprehensive input validation
- **Path traversal protection** - Prevent malicious file access
- **URL validation** - Block javascript:, file:, and other dangerous patterns
- **File size limits** - Protect against file bombs

### 📈 Export & Research

- **CSV exports** - Tags summaries, scorecard data, analysis results
- **Metadata tracking** - Complete provenance for every document
- **Reproducible** - Version-controlled configs and timestamps

______________________________________________________________________

## 🚀 Quick Start

### Prerequisites

- **Python 3.12** (required)
- 1GB+ disk space for code and small dataset
- Internet connection for scraping

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/MissCrispenCakes/DigitalChild.git
cd DigitalChild

# 2. Set up virtual environment
python3 -m venv .LittleRainbow
source .LittleRainbow/bin/activate  # On Windows: .LittleRainbow\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize project structure
python init_project.py
```

### Basic Usage

```bash
# Run complete pipeline for AU Policy documents
python pipeline_runner.py --source au_policy

# Run with latest tags
python pipeline_runner.py --source au_policy --tags-version latest

# Process specific country (UPR documents)
python pipeline_runner.py --source upr --country kenya

# Run scorecard workflow
python pipeline_runner.py --mode scorecard --scorecard-action all
```

Exports appear in `data/exports/` as CSV files ready for analysis.

______________________________________________________________________

## 📋 Project Status

**Phase 1-2 Complete:**

- ✅ Core pipeline (scraping, processing, tagging) - Multiple sources: 6 automated scrapers + direct URL tracking
- ✅ Scorecard system - 194 countries, 10 indicators, 2,543 source URLs tracked
- ✅ Validation & security framework - 68 validator tests, 124 total tests passing
- ✅ Comprehensive documentation - 25 markdown files

**Phase 3 In Progress:** Recommendations extraction, timeline exports, comparison analytics

See [docs/ROADMAP.md](docs/ROADMAP.md) for detailed feature roadmap and future phases.

______________________________________________________________________

## 📚 Documentation

- **[FAQ](docs/FAQ.md)** - Frequently asked questions
- **[Architecture](docs/ARCHITECTURE.md)** - System design and components
- **[Glossary](docs/GLOSSARY.md)** - Key terms and definitions
- **[Runbook](docs/guides/RUNBOOK.md)** - Complete command reference
- **[Scorecard Workflow](docs/guides/SCORECARD_WORKFLOW.md)** - Indicator tracking system
- **[Data Governance](docs/DATA_GOVERNANCE.md)** - Privacy, ethics, responsible research
- **[Roadmap](docs/ROADMAP.md)** - Development phases and future features

See [docs/DOCS_INDEX.md](docs/DOCS_INDEX.md) for full documentation index.

______________________________________________________________________

## 🛠 Troubleshooting

**Common issues:**

- **Virtual environment** - Activate before installing dependencies
- **Python version** - Must use Python 3.12 specifically
- **Import errors** - Run commands from project root, not subdirectories
- **Pre-commit failures** - Run `pre-commit run --all-files` to fix formatting

See [First Run Error Checklist](docs/guides/FIRST_RUN_ERRORS.md) for detailed solutions.

______________________________________________________________________

## 🤝 Contributing

We welcome contributions from researchers, developers, and human rights advocates!

**Ways to contribute:**

- Report bugs and issues
- Add new data sources (scrapers)
- Improve documentation
- Add test coverage
- Suggest features

**Getting started:**

1. Read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines
1. Check [issues](https://github.com/MissCrispenCakes/DigitalChild/issues) labeled `good first issue`
1. Fork the repo and create a feature branch
1. Submit a pull request

**Developer setup:**

```bash
# Install development tools
pip install pre-commit pytest pytest-cov

# Set up pre-commit hooks (required before committing)
pre-commit install

# Run tests
pytest tests/ -v

# Run all quality checks
pre-commit run --all-files
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

______________________________________________________________________

## 📄 License

**Dual licensing for different components:**

- **Code:** [MIT License](LICENSE) - Free to use, modify, and distribute
- **Data & Documentation:** [CC BY 4.0](LICENSE-DATA) - Attribution required

This means:

- ✅ Use the code freely, including commercial applications
- ✅ Use and share the scorecard data with attribution
- ✅ Fork, modify, and redistribute
- ❌ Don't remove attribution from data/docs

See [LICENSE](LICENSE) and [LICENSE-DATA](LICENSE-DATA) for full terms.

______________________________________________________________________

## 📖 Citation

If you use this project in your research, please cite it:

```bibtex
@software{digitalchild2025,
  title = {DigitalChild: Human Rights Data Pipeline for Child and LGBTQ+ Digital Protection},
  author = {Vollmer, S.C. and Vollmer, D.T.},
  year = {2025},
  url = {https://github.com/MissCrispenCakes/DigitalChild},
  note = {Available at: https://grimdata.org. ORCID: 0000-0002-3359-2810}
}
```

For complete citation information including the conference presentation, see [CITATION.cff](CITATION.cff).

**For the scorecard data specifically:**

> Vollmer, D.T., & Vollmer, S.C. (2025). LittleRainbowRights Scorecard: Child and LGBTQ+ Digital Rights Indicators. Licensed under CC BY 4.0. Available at: https://github.com/MissCrispenCakes/DigitalChild. ORCID: [0000-0002-3359-2810](https://orcid.org/0000-0002-3359-2810)

______________________________________________________________________

## 🔒 Security

Found a security vulnerability? **Do not open a public issue.**

Report via [GitHub Security Advisories](https://github.com/MissCrispenCakes/DigitalChild/security) - click "Report a vulnerability"

See [SECURITY.md](SECURITY.md) for full responsible disclosure policy.

______________________________________________________________________

## 🙏 Acknowledgments

This project analyzes publicly available human rights documents from:

- United Nations (OHCHR, UPR, UNICEF)
- African Union (AU Policy, ACERWC, ACHPR)
- UNESCO, UNCTAD, ILGA World, and other authoritative sources

Data sources tracked with 2,543 validated URLs ensuring transparency and verification.

**Built with:**

- Python 3.12, BeautifulSoup4, Selenium, pandas, PyPDF2, pytest
- GitHub Pages for documentation
- MkDocs Material for website

**Maintained by:** PhD student as part of human rights research (please be patient with response times!)

______________________________________________________________________

## 📞 Contact & Support

- **Issues:** [GitHub Issues](https://github.com/MissCrispenCakes/DigitalChild/issues)
- **Discussions:** [GitHub Discussions](https://github.com/MissCrispenCakes/DigitalChild/discussions)
- **Website:** [GRIMdata.org](https://grimdata.org)

Support the project:

- ⭐ Star this repository
- 📢 Share with researchers and advocates
- 💻 Contribute code or documentation
- 📝 Cite in your publications

______________________________________________________________________

**Last updated:** January 2026
