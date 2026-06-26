# DigitalChild

### GRIMdata / LittleRainbowRights

[![CI](https://github.com/MissCrispenCakes/DigitalChild/actions/workflows/ci.yml/badge.svg?branch=basecamp&event=push)](https://github.com/MissCrispenCakes/DigitalChild/actions/workflows/ci.yml)
[![CD](https://github.com/MissCrispenCakes/DigitalChild/actions/workflows/deploy-docs.yml/badge.svg?branch=basecamp)](https://github.com/MissCrispenCakes/DigitalChild/actions/workflows/deploy-docs.yml)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18318098.svg)](https://doi.org/10.5281/zenodo.18318098)
[![REUSE status](https://api.reuse.software/badge/github.com/MissCrispenCakes/DigitalChild)](https://api.reuse.software/info/github.com/MissCrispenCakes/DigitalChild)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Data License: CC BY 4.0](https://img.shields.io/badge/Data%20License-CC%20BY%204.0-lightgrey.svg)](LICENSE-DATA)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)

**Open-source data pipeline for analyzing human rights documents with focus on child and LGBTQ+ digital protection.**

Scrape, process, tag, and analyze policy documents from international organizations. Track 10 human rights indicators across 194 countries. Support evidence-based advocacy and research.

🌍 **Website:** [GRIMdata.org](https://grimdata.org) | [LittleRainbowRights.com](https://littlerainbowrights.com)
📖 **Documentation:** [docs/](docs/index.md)
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
- **REST API** - 14 production-ready endpoints for programmatic data access (Flask backend)
  - Documents: list with filters, pagination, sorting, detail view
  - Scorecard: countries summary, indicators, statistics
  - Tags: frequency analysis, version management, filtering
  - Timeline: temporal analysis of tags over time
  - Export: CSV downloads with SPDX license headers
  - API key authentication, dynamic rate limiting (100-2000 req/hr)
  - Docker deployment with Redis caching and Nginx reverse proxy

______________________________________________________________________

## 🎯 Why This Work Matters

Digital systems (AI, surveillance, biometric identification, identity verification systems) are being deployed rapidly affecting children and LGBTQ+ youth. We don't yet know whether these systems help or harm—but decisions are being made RIGHT NOW with permanent consequences.

**The problem:** Who should control vulnerable populations' digital rights?

- **Parents?** May not understand digital safety (already posting kids' photos publicly)
- **Governments?** May weaponize systems (countries criminalizing LGBTQ+ people using biometric data for tracking)
- **Companies?** May lack security (data "everywhere forever, easily hacked")

**Without transparent tracking:** Assumptions → decisions → irreversible consequences → by the time we know we were wrong, TOO LATE to reverse.

This pipeline tracks digital rights deployments across 194 countries, enabling evidence-based decisions BEFORE consequences become irreversible.

**Research approach:** We document facts and analyze enforcement mechanisms without imposing Western-centric values. Our methodology recognizes cultural context while focusing on protecting vulnerable populations' autonomy. See [Data Governance](docs/DATA_GOVERNANCE.md#-cultural-sensitivity-research-stance) for our cultural sensitivity framework.

**Methodological foundation:** [Research Context](docs/RESEARCH_CONTEXT.md) | **Published work:** [Vollmer & Vollmer (2022)](https://doi.org/10.47348/SLR/2022/i1a1)

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

### 🆕 Using the API (Alternative to Pipeline)

**Don't want to run the pipeline?** Access data via REST API:

```bash
# Install API dependencies
pip install -r api_requirements.txt

# Start API server
python run_api.py
```

Access data programmatically:

```bash
# Health check
curl http://localhost:5000/api/health

# Get all documents
curl http://localhost:5000/api/documents

# Filter by country
curl "http://localhost:5000/api/documents?country=Kenya"

# Get scorecard
curl http://localhost:5000/api/scorecard/Kenya
```

**Python example:**

```python
import requests

# Optional: Use API key for higher rate limits
headers = {"X-API-Key": "your-api-key"}

# Get Kenya's scorecard
response = requests.get("http://localhost:5000/api/scorecard/Kenya", headers=headers)
data = response.json()["data"]
print(data["indicators"])

# Get documents about AI policy
response = requests.get("http://localhost:5000/api/documents?tags=AI", headers=headers)
documents = response.json()["data"]["items"]

# Get tag frequency for Africa
response = requests.get("http://localhost:5000/api/tags?region=Africa", headers=headers)
tags = response.json()["data"]["tags"]

# Download scorecard CSV
response = requests.get("http://localhost:5000/api/export/scorecard_summary", headers=headers)
with open("scorecard.csv", "wb") as f:
    f.write(response.content)
```

**14 endpoints available:**

- **Documents:** list, filter, detail (with pagination and sorting)
- **Scorecard:** summary, country detail, statistics
- **Tags:** frequency analysis, version list (filterable by country/region/year)
- **Timeline:** tags over time (year × tag matrix)
- **Export:** list formats, download CSVs
- **Health:** status check, system info

**Features:**
- API key authentication (optional, higher rate limits when authenticated)
- Rate limiting: 100 req/hr public, 1000 req/hr authenticated
- Caching: 15min-1hr TTLs for optimal performance
- Docker deployment ready with Redis and Nginx

📖 **Full API documentation:** [docs/api/index.md](docs/api/index.md) | [Quick Reference](docs/api/quick-reference.md) | [Production Deployment](docs/guides/PRODUCTION_DEPLOYMENT.md)

______________________________________________________________________

## 📋 Project Status

**Phase 1-2 Complete:**

- ✅ Core pipeline (scraping, processing, tagging) - Multiple sources: 6 automated scrapers + direct URL tracking
- ✅ Scorecard system - 194 countries, 10 indicators, 2,543 source URLs tracked
- ✅ Validation & security framework - 170 tests passing (68 validator tests)
- ✅ Recommendations extraction system - Regex-based with versioning and history tracking
- ✅ Timeline exports - Global, by-country, and by-region analysis over time
- ✅ Comparison analytics - Compare tags and recommendations across versions

**Phase 3 Complete (8/9 tasks):** Advanced processing features operational

- ✅ ISO 3166-1 alpha-2 country code mapping - 194 countries fully mapped
- ✅ Document type classifier - Multi-stage rules-based classification
- ✅ Scorecard maintenance system - Phase 1 critical updates completed (6 countries, 18 fields updated)
- ✅ Multi-format scorecard exports - CSV, XLSX, ODS, Google Sheets JSON

**Phase 4 Complete (5/5 weeks):** REST API backend operational

- ✅ **Flask API backend (Week 1-2)** - Foundation and core endpoints
  - App factory pattern, configuration management, extensions
  - Documents API (list, filter, detail) with pagination and sorting
  - Scorecard API (countries, indicators, statistics)
  - Health and system info endpoints
  - Request validation, caching (15min-1hr TTLs), error handling
- ✅ **Extended APIs (Week 3)** - Tags, Timeline, Export endpoints
  - Tags API: frequency analysis, version management, filtering
  - Timeline API: temporal analysis (year × tag matrices)
  - Export API: CSV downloads with SPDX license headers
- ✅ **Authentication & Rate Limiting (Week 4)** - Security features
  - API key authentication via X-API-Key header
  - Dynamic rate limiting (100/1000 req/hr public/authenticated)
  - Custom limits for expensive operations (exports, search)
- ✅ **Production Deployment (Week 5)** - Infrastructure ready
  - Docker + docker-compose configuration
  - Redis caching and rate limiting storage
  - Nginx reverse proxy with SSL/TLS
  - Complete deployment guide (678 lines)
- ✅ **Testing & Quality** - 104 tests passing (100% success rate)
- ⏳ **Interactive dashboard frontend** - Planned for Phase 5

See [docs/ROADMAP.md](docs/ROADMAP.md) for detailed roadmap and [docs/api/index.md](docs/api/index.md) for API documentation.

______________________________________________________________________

## 📚 Documentation

- **[FAQ](docs/FAQ.md)** - Frequently asked questions
- **[Architecture](docs/ARCHITECTURE.md)** - System design and components
- **[Glossary](docs/GLOSSARY.md)** - Key terms and definitions
- **[Runbook](docs/guides/RUNBOOK.md)** - Complete command reference
- **[Scorecard Workflow](docs/guides/SCORECARD_WORKFLOW.md)** - Indicator tracking system
- **[Data Governance](docs/DATA_GOVERNANCE.md)** - Privacy, ethics, responsible research
- **[Roadmap](docs/ROADMAP.md)** - Development phases and future features
- **[API Documentation](docs/api/index.md)** - REST API endpoints, usage, examples
- **[API Quick Start](docs/api/quickstart.md)** - Fast reference for API usage

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

**MIT License** - see [LICENSE](LICENSE) file

This project uses dual licensing:

- **Code (software):** MIT License - Free to use, modify, and distribute
- **Data & Documentation:** CC BY 4.0 - Attribution required (see [LICENSE-DATA](LICENSE-DATA))

This means:

- ✅ Use the code freely, including commercial applications
- ✅ Use and share the scorecard data with attribution
- ✅ Fork, modify, and redistribute
- ❌ Don't remove attribution from data/docs

**Full license terms:** [LICENSE](LICENSE) (MIT) and [LICENSE-DATA](LICENSE-DATA) (CC BY 4.0)

______________________________________________________________________

## 📖 Citation

If you use this project in your research, please cite it:

```bibtex
@software{digitalchild2026,
  title = {DigitalChild: Human Rights Data Pipeline for Child and LGBTQ+ Digital Protection},
  author = {Vollmer, S.C. and Vollmer, D.T.},
  year = {2026},
  version = {2.0.1},
  url = {https://github.com/MissCrispenCakes/DigitalChild},
  doi = {10.5281/zenodo.18318098},
  note = {Available at: https://grimdata.org. ORCID: 0000-0002-3359-2810 (S.C. Vollmer)}
}
```

Or use the format in [CITATION.cff](CITATION.cff).

**For the scorecard data specifically:**

> Vollmer, D.T., & Vollmer, S.C. (2025). LittleRainbowRights Scorecard: Child and LGBTQ+ Digital Rights Indicators.
> Licensed under CC BY 4.0.
> Available at: https://github.com/MissCrispenCakes/DigitalChild
> ORCID: [0000-0002-3359-2810](https://orcid.org/0000-0002-3359-2810) (S.C. Vollmer)

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

- Python 3.12, BeautifulSoup4, Selenium, pandas, pypdf, pytest
- Flask, Flask-CORS, Flask-Caching for REST API
- GitHub Pages for documentation
- MkDocs Material for website

**Maintained by:** PhD student (passion project, please be patient with response times!)

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

**Last updated:** June 2026
