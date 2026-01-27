# DigitalChild v1.0.0 - Initial Public Release

First stable release of the DigitalChild data pipeline for analyzing human rights documents with focus on child and LGBTQ+ digital protection.

## 🎯 What's Included

### Core Pipeline
- **7 automated scrapers** - AU Policy, OHCHR, UPR, UNICEF, ACERWC, ACHPR, manual upload
- **Multi-format processing** - PDF, DOCX, HTML document conversion
- **Versioned tagging system** - 4 tag versions (v1, v2, v3, digital) with 20+ rights themes
- **Recommendations extraction** - Regex-based extraction with versioning and history tracking
- **Timeline analysis** - Global, by-country, and by-region temporal analysis
- **Comparison analytics** - Side-by-side version comparison for tags and recommendations

### Scorecard System
- **194 countries tracked** with 10 human rights indicators per country
- **2,543 authoritative source URLs** validated and monitored
- **Automated validation** - URL checking, change detection, link rot monitoring
- **CSV exports** - Summary tables, by-indicator breakdowns, regional analysis

### Quality & Testing
- **124 tests** - Comprehensive test coverage (scrapers, processors, validators, scorecard)
- **68 validator tests** - Input validation, path traversal protection, URL validation, file size limits
- **CI/CD pipeline** - Automated testing with GitHub Actions
- **Pre-commit hooks** - Code formatting (black, isort, flake8), markdown linting

### Documentation
- **25+ markdown files** - Installation guides, API docs, standards, architecture
- **CLAUDE.md** - Comprehensive development guide for AI assistants
- **Website deployment** - Material for MkDocs with GitHub Pages integration

## 📊 Dataset Highlights

- **10 indicators tracked per country:**
  - Data Protection Law
  - DPA Independence
  - Children's Data Safeguards
  - Child Online Protection Strategy
  - SOGI Sensitive Data Protections
  - LGBTQ+ Legal Status
  - LGBTQ+ Promotion/Propaganda Offences
  - AI Policy Status
  - DPIA Required for High-Risk AI
  - SIM Card Biometric ID Linkage

!!! warning "Correction Notice"
    The original v1.0.0 release notes (published 2026-01-20) incorrectly listed indicators #6-10 as "Digital Services Taxation, Internet Penetration, Mobile Coverage, Digital Skills Investment, Online Content Regulation." These indicators were NEVER part of the LittleRainbowRights scorecard. The correct indicators are listed above and have been used throughout all project documentation and data analysis since inception.

- **Data sources:** UNESCO, UNCTAD, ILGA, UNICEF, national governments, treaty bodies

## 🔧 Technical Specifications

- **Language:** Python 3.12
- **Key libraries:** BeautifulSoup4, Selenium, pandas, PyPDF2, pytest
- **Lines of code:** ~15,000+ (Python, config, tests)
- **Export formats:** CSV, JSON
- **License:** MIT (code), CC BY 4.0 (data)

## 📝 Citation

```bibtex
@software{digitalchild2026,
  author = {Vollmer, S.C.},
  title = {DigitalChild: Human Rights Data Pipeline for Child and LGBTQ+ Digital Protection},
  year = {2026},
  version = {1.0.1},
  url = {https://github.com/MissCrispenCakes/DigitalChild},
  doi = {10.5281/zenodo.18318099}
}
```

## 🌍 Related Projects

- **GRIMdata.org** - Main platform website
- **LittleRainbowRights.com** - Child & LGBTQ+ digital rights project
- **SGBV-UPR Research** - Precursor research on SGBV and Universal Periodic Review

## ⚠️ Known Limitations

- Scorecard sources require periodic manual validation (some URLs change)
- PDF extraction may have OCR limitations for scanned documents
- Regional coverage currently strongest in Africa (global expansion planned)

## 🚀 What's Next (Phase 4)

- Research dashboard with interactive visualizations
- REST API for data access
- NLP-based recommendations extraction
- Global expansion (Europe, Asia, Americas)

## 📖 Documentation

- Full docs: https://grimdata.org
- Installation: See [README.md](README.md)
- API docs: See [docs/](docs/)

---

**Note:** This is the first public release suitable for research, citation, and replication. Future versions will include dashboard features and expanded geographic coverage.
