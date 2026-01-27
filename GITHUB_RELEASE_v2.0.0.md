# Release v2.0.0 - REST API + Documentation Restructure

**Release Date:** January 26, 2026
**Zenodo DOI:** [10.5281/zenodo.18318098](https://doi.org/10.5281/zenodo.18318098)

Major release adding production-ready REST API (Phase 4) and complete documentation reorganization.

---

## 🎉 What's New

### REST API (Phase 4 Complete)

Production-ready REST API with **14 endpoints** for programmatic data access:

- **Documents API** - List, filter, paginate, sort documents with 9 filter options
- **Scorecard API** - Country indicators, summary statistics, regional filtering
- **Tags API** - Frequency analysis, version management, multi-dimensional filtering
- **Timeline API** - Temporal analysis (tags over time, year × tag matrices)
- **Export API** - CSV downloads with SPDX license headers

**Features:**
- Optional API key authentication with dynamic rate limiting (100-2000 req/hr)
- Redis caching with 15min-1hr TTLs
- Complete Docker deployment (docker-compose, Nginx, Redis)
- 104 integration tests (100% pass rate, 100% endpoint coverage)

📖 **API Documentation:** https://grimdata.org/api/

### Documentation Restructure

Complete reorganization with dedicated landing pages:

- **API Landing Page** - Overview, features, quick start examples
- **Scorecard Landing Page** - Design, methodology, data access guides
- **Projects Landing Page** - LittleRainbowRights and SGBV-UPR overviews
- Clean professional navigation throughout

### Technical Improvements

- **Test Coverage:** Expanded from 124 → 274 tests (170 pipeline + 104 API)
- **Codebase:** Grew from 15,000+ → 21,000+ lines of Python
- **Dependencies:** Updated Flask ecosystem to latest stable versions
- **CITATION.cff:** Updated with REST API keywords, SGBV journal article DOI

---

## 📦 Installation

```bash
# Clone and install
git clone https://github.com/MissCrispenCakes/DigitalChild.git
cd DigitalChild
pip install -r requirements.txt

# Run API server
pip install -r api_requirements.txt
python run_api.py

# Access at http://localhost:5000
curl http://localhost:5000/api/health
```

---

## 🔧 Changed

- Test coverage: 124 → 274 tests
- Codebase: 15k → 21k+ lines
- Documentation structure reorganized
- API docs moved to docs/website/api/
- Scorecard docs moved to docs/website/scorecard/
- Navigation structure improved

---

## 🐛 Fixed

- Navigation links consistency
- Duplicate content removed
- TOC integration in sidebar
- 404 errors on Projects pages
- Scorecard v1.0.0 release notes corrected

---

## 📊 Metrics

- **14 API endpoints** operational
- **194 countries** tracked
- **10 indicators** per country
- **2,543 source URLs** validated
- **274 tests** passing (100% success rate)
- **21,000+ lines** of code
- **75+ documentation** files

---

## 🔗 Links

- **Website:** https://grimdata.org
- **API Docs:** https://grimdata.org/api/
- **Scorecard:** https://grimdata.org/scorecard/
- **Deployment Guide:** [docs/guides/PRODUCTION_DEPLOYMENT.md](docs/guides/PRODUCTION_DEPLOYMENT.md)
- **Zenodo Archive:** https://doi.org/10.5281/zenodo.18318098

---

## 📖 Citation

```bibtex
@software{digitalchild2026,
  title = {DigitalChild: Human Rights Data Pipeline for Child and LGBTQ+ Digital Protection},
  author = {Vollmer, S.C. and Vollmer, D.T.},
  year = {2026},
  version = {2.0.0},
  url = {https://github.com/MissCrispenCakes/DigitalChild},
  doi = {10.5281/zenodo.18318098},
  note = {Available at: https://grimdata.org. ORCID: 0000-0002-3359-2810 (S.C. Vollmer)}
}
```

---

## 🙏 Acknowledgments

- Python 3.12, Flask, BeautifulSoup4, Selenium, pandas, pypdf, pytest
- Redis, Docker, Nginx for production infrastructure
- GitHub Actions for CI/CD
- MkDocs Material for documentation

---

**Full Changelog:** https://github.com/MissCrispenCakes/DigitalChild/blob/basecamp/CHANGELOG.md
