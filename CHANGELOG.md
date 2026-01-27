# Changelog

All notable changes to the DigitalChild / LittleRainbowRights project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0] - 2026-01-26

### Added
- **REST API (Phase 4 Complete)** - 14 production-ready endpoints for programmatic data access
  - Documents API: list with filters, pagination, sorting, detail view
  - Scorecard API: countries summary, country details, indicator statistics
  - Tags API: frequency analysis, version management, filtering
  - Timeline API: temporal analysis of tags over time
  - Export API: CSV downloads with SPDX license headers
- **Authentication & Rate Limiting** - Optional API key authentication with dynamic rate limits (100-2000 req/hr)
- **Production Deployment** - Docker, docker-compose, Redis caching, Nginx reverse proxy
- **API Tests** - 104 integration tests (100% pass rate, 100% endpoint coverage)
- **Documentation Site Restructure** - Complete reorganization with landing pages for API and Scorecard sections
- **API Landing Page** - Comprehensive overview at /api/ explaining features, use cases, and quick examples
- **Scorecard Landing Page** - Overview at /scorecard/ with clear navigation to sub-sections
- **Scorecard Design & Methodology Page** - Detailed indicator definitions, scoring system, and limitations
- **Scorecard Data Access Page** - Comprehensive guide to API, CSV exports, direct file access, and pipeline integration
- **Projects Landing Page** - Dedicated overview page for LittleRainbowRights and SGBV-UPR projects
- **Navigation Improvements** - Clean, professional navigation without emojis, proper nesting of sections

### Changed
- **Test Coverage** - Expanded from 124 to 274 tests (170 pipeline + 104 API)
- **Codebase Size** - Grew from 15,000+ to 21,000+ lines of Python code
- **Documentation Structure** - Reorganized API docs to website/api/, Scorecard docs to website/scorecard/
- **Navigation Structure** - Scorecard and Data Explorer now properly nested under Scorecard section
- **API Documentation** - Moved from docs/api/ to docs/website/api/ for consistency
- **CITATION.cff** - Updated to v2.0.0 with confirmed Zenodo DOI: 10.5281/zenodo.18318098

### Fixed
- **Navigation Links** - Consistent links throughout documentation, removed broken cross-references
- **Duplicate Content** - Removed duplicate scorecard and API pages
- **TOC Integration** - Fixed table of contents display in left sidebar
- **404 Errors** - Fixed missing Projects landing page
- **Emoji Usage** - Removed unprofessional emojis from navigation labels
- **Scorecard v1.0.0 Release Notes** - Corrected incorrect indicator list in historical release notes

## [1.0.1] - 2026-01-20

### Added
- Zenodo archival integration for citation purposes

### Removed
- Unpublished slides and personal contact information

## [1.0.0] - 2026-01-20 - Initial Public Release

### Core Components

**Data Collection Sources (7):**
- AU Policy, OHCHR, UPR, UNICEF, ACERWC, ACHPR, manual upload

**Document Processing:**
- Multi-format handling: PDF, DOCX, HTML
- Versioned tagging framework: 4 tag versions (v1, v2, v3, digital) with 20+ rights themes

**Scorecard Indicators (10) - CORRECT LIST:**

1. **Data Protection Law** - Comprehensive data protection legislation
2. **DPA Independence** - Data Protection Authority operates independently
3. **Children's Data Safeguards** - Child-specific data governance safeguards in binding law
4. **Child Online Protection Strategy** - National COP framework addressing online harms
5. **SOGI Sensitive Data** - Sexual orientation and gender identity recognized as sensitive data
6. **LGBTQ+ Legal Status** - Legal recognition and protection of LGBTQ+ individuals
7. **LGBTQ+ Promotion/Propaganda Offences** - Laws restricting LGBTQ+ discussion or advocacy
8. **AI Policy Status** - National AI strategy or framework adoption
9. **DPIA Required for High-Risk AI** - Data Protection Impact Assessments required for high-risk AI
10. **SIM Card Biometric ID Linkage** - Biometric data required for SIM registration

**NOTE:** The v1.0.0 GitHub release notes incorrectly listed indicators #6-10 as "Digital Services Taxation, Internet Penetration, Mobile Coverage, Digital Skills Investment, Online Content Regulation" - these were NEVER part of the LittleRainbowRights scorecard and were listed in error.

### Technical Details

- **Language:** Python 3.12
- **Codebase:** ~15,000 lines of code
- **Tests:** 124 tests + 68 validator tests
- **Dependencies:** BeautifulSoup4, Selenium, pandas, PyPDF2
- **Security:** Path traversal protection, URL validation, file size limits

### Scope

- **Countries:** 194 tracked globally
- **Source URLs:** 2,543 authoritative sources validated
- **Organizations:** UNESCO, UNCTAD, ILGA World, UNICEF, ITU, Privacy International, Human Rights Watch

### Known Limitations

- PDF extraction quality varies by document format
- Regional coverage concentration in certain areas
- Some indicators have incomplete data for certain countries

[Unreleased]: https://github.com/MissCrispenCakes/DigitalChild/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/MissCrispenCakes/DigitalChild/releases/tag/v2.0.0
[1.0.1]: https://github.com/MissCrispenCakes/DigitalChild/releases/tag/v1.0.1
[1.0.0]: https://github.com/MissCrispenCakes/DigitalChild/releases/tag/v1.0.0
