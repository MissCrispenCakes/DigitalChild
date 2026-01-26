# Release Notes - v2.0.0 (DRAFT)

**Date:** TBD
**Zenodo DOI:** [10.5281/zenodo.18318099](https://doi.org/10.5281/zenodo.18318099)

## 🎉 Major Release: Production REST API + Documentation Platform

This major release adds a production-ready REST API backend and comprehensive documentation platform, transforming LittleRainbowRights from a data pipeline into a complete research platform.

## 🚀 What's New

### REST API Backend (Phase 4 Complete)

**14 Production-Ready Endpoints:**

- **Health & Info:** System status and data statistics
- **Documents API:** List with filters, pagination, sorting, detail view
- **Scorecard API:** Countries summary, country detail, indicator statistics
- **Tags API:** Frequency analysis, version management, temporal filtering
- **Timeline API:** Tag trends over time
- **Export API:** CSV downloads with SPDX license headers

**Features:**
- ✅ API key authentication (optional)
- ✅ Dynamic rate limiting (100-2000 req/hr based on auth level)
- ✅ Response caching for performance
- ✅ Comprehensive error handling
- ✅ CORS support for frontend integration
- ✅ Docker deployment with Redis and Nginx

**Testing:**
- 104 API integration tests (100% pass rate)
- Full endpoint coverage
- Authentication and rate limiting tests

### Documentation Platform

**New Documentation Site:** [grimdata.org](https://grimdata.org)

- Complete MkDocs Material theme deployment
- Comprehensive API documentation
- Interactive guides and tutorials
- Projects landing page showcasing both LRR and SGBV-UPR
- Consistent navigation across all pages
- Search functionality
- Dark/light mode support

### Enhanced Scorecard System

**10 Digital Rights Indicators** (CORRECTED - see note below):

1. **Data Protection Law** - Existence of comprehensive data protection legislation governing personal data processing
2. **DPA Independence** - Whether the national Data Protection Authority operates independently from executive control
3. **Children's Data Safeguards** - Binding child-specific privacy/data-protection safeguards in law or regulation (not general child welfare law)
4. **Child Online Protection Strategy** - National COP framework addressing online harms to children; may include parental tools/rights
5. **SOGI Sensitive Data** - Whether sexual orientation and gender identity are legally recognized as sensitive personal data
6. **LGBTQ+ Legal Status** - Legal recognition and protection of LGBTQ+ individuals
7. **LGBTQ+ Promotion/Propaganda Offences** - Laws restricting discussion, visibility, or advocacy related to LGBTQ+ identities
8. **AI Policy Status** - Whether a country has adopted a national AI strategy or framework
9. **DPIA Required for High-Risk AI** - Legal requirement to conduct Data Protection Impact Assessments for high-risk AI systems
10. **SIM Card Biometric ID Linkage** - Requirement to provide biometric data when registering SIM cards, either directly or through linkage to biometric national ID systems

**Scoring System:**
- 0-1-2 scale per indicator (0=worst, 2=best)
- Protection Score: Sum of all indicators (0-20)
- Risk Index: 100 - (Protection Score / 20 × 100)
- Data Completeness: Percentage of indicators with data

## 📊 Project Statistics

- **Countries Tracked:** 194 globally
- **Source URLs:** 2,543 validated authoritative sources
- **Codebase:** 21,000+ lines of Python 3.12
- **Tests:** 274 comprehensive tests (170 pipeline + 104 API)
- **API Endpoints:** 14 production-ready
- **Documentation Pages:** 50+ comprehensive guides

## 🛠️ Technical Details

### Core Dependencies
- Python 3.12
- Flask 3.0 (REST API)
- BeautifulSoup4 & Selenium (web scraping)
- pandas (data analysis)
- pytest & pytest-cov (testing)
- MkDocs Material (documentation)

### Production Deployment
- Docker & docker-compose
- Redis caching
- Nginx reverse proxy
- Gunicorn WSGI server
- Environment-based configuration

### Security Features
- API key authentication
- Rate limiting (configurable per endpoint)
- Input validation (path traversal protection, URL validation)
- File size limits
- CORS configuration
- Secure headers

## 📚 Data Sources

All data sourced from authoritative international organizations:

- **UNESCO** - AI policy observatory
- **UNCTAD** - Data protection legislation tracking
- **ILGA World** - LGBTQ+ legal status (State-Sponsored Homophobia report)
- **UNICEF** - Child protection measures
- **ITU** - Telecom and internet regulations
- **Privacy International** - Surveillance and privacy tracking
- **Human Rights Watch** - Human rights monitoring

## 🐛 Bug Fixes

- Fixed navigation consistency across all documentation pages
- Removed duplicate scorecard pages
- Fixed 404 errors for Projects landing page
- Corrected table of contents integration in left sidebar
- Standardized all internal links

## ⚠️ Important Note: Corrected Indicator List

**The v1.0.0 release notes contained INCORRECT indicators #6-10.** The release mistakenly listed:

❌ Digital Services Taxation
❌ Internet Penetration
❌ Mobile Coverage
❌ Digital Skills Investment
❌ Online Content Regulation

These were **NEVER** part of the LittleRainbowRights scorecard. The correct indicators are listed above and have been used throughout all project documentation and data analysis.

## 📖 Documentation

- **Quick Start:** [grimdata.org/api/QUICK_START](https://grimdata.org/api/QUICK_START/)
- **Full API Docs:** [grimdata.org/api/README](https://grimdata.org/api/README/)
- **Installation Guide:** [grimdata.org/getting-started/installation](https://grimdata.org/getting-started/installation/)
- **Scorecard:** [grimdata.org/scorecard](https://grimdata.org/scorecard/)

## 📝 Citation

When using LittleRainbowRights data:

```bibtex
@misc{littlerainbowrights2025,
  title = {LittleRainbowRights: Child and LGBTQ+ Digital Rights Scorecard},
  author = {Vollmer, S.C. and Vollmer, D.T.},
  year = {2025},
  howpublished = {\url{https://grimdata.org/projects/littlerainbowrights/}},
  note = {Licensed under CC BY 4.0. ORCID: 0000-0002-3359-2810},
  doi = {10.5281/zenodo.18318099}
}
```

## 🔗 Links

- **Website:** [grimdata.org](https://grimdata.org)
- **GitHub:** [github.com/MissCrispenCakes/DigitalChild](https://github.com/MissCrispenCakes/DigitalChild)
- **Zenodo:** [10.5281/zenodo.18318099](https://doi.org/10.5281/zenodo.18318099)
- **Published Research:** [Vollmer & Vollmer (2025)](https://doi.org/10.5281/zenodo.18318099)

## 🙏 Acknowledgments

This research was presented at the 2nd International Conference on Children's Rights (Stellenbosch, September 9-11, 2025).

## 📄 License

- **Code:** MIT License
- **Data & Documentation:** CC BY 4.0

---

**Full Changelog:** [v1.0.1...v2.0.0](https://github.com/MissCrispenCakes/DigitalChild/compare/v1.0.1...v2.0.0)
