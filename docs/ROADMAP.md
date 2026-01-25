# Project Roadmap

This roadmap outlines the milestones for the GRIMdata / LittleRainbowRights pipeline.

______________________________________________________________________

## Phase 1: Core Pipeline (✅ COMPLETE)

- [x] Project scaffolding (`init_project.py`)
- [x] AU Policy scraper (requests and Selenium variants)
- [x] PDF → text processor
- [x] DOCX → text processor
- [x] HTML → text processor
- [x] Fallback handler for multi-format processing
- [x] Tagging system (v1, v2, v3, digital versions)
- [x] Tags version management (`tags_main.json`)
- [x] Metadata tracking with history
- [x] Unified logging system with per-module logs
- [x] Comprehensive test suite (170 tests passing)
- [x] Documentation (setup, structure, standards, pipeline flow)
- [x] CI/CD pipeline with GitHub Actions
- [x] Pre-commit hooks (black, isort, flake8, markdown, yaml)

______________________________________________________________________

## Phase 2: Data Enrichment & Validation (✅ COMPLETE)

### Scorecard System

- [x] Scorecard data loading (194 countries, 10 indicators each)
- [x] Scorecard metadata enrichment
- [x] Scorecard CSV exports (summary, sources, by-indicator, by-region)
- [x] URL validation system (parallel workers, retry logic)
- [x] Source change detection and monitoring
- [x] Diff checking for stale scorecard entries
- [x] Integration with pipeline runner

**Note:** System infrastructure complete; country-level data population and validation ongoing (0-1-2 scoring framework finalized January 2026).

### Validation & Security

- [x] Centralized validators module (68 tests)
- [x] URL validation with malicious pattern blocking
- [x] Path validation with traversal protection
- [x] File validation (size limits, extension checks)
- [x] String validation (length, patterns, regex)
- [x] Config validation (JSON, tags, structure)
- [x] Schema validation (metadata, documents)
- [x] Security improvements across all processors

### Expanded Sources

- [x] OHCHR Treaty Body scraper
- [x] UPR documents scraper
- [x] UNICEF reports scraper
- [x] ACERWC scraper
- [x] ACHPR scraper
- [x] Manual upload ingestion (via `data/raw/manual/`)
- [x] Static URL dictionary processing

______________________________________________________________________

## Phase 3: Advanced Processing (✅ COMPLETE - 8/9 Tasks)

### Recommendations System

- [x] Recommendations extraction (regex-based)
- [x] Recommendations config format (`recs_v1.json`)
- [x] Recommendations versioning and history tracking
- [ ] NLP-based recommendations extraction (future)
- [x] Recommendations export to CSV

### Comparison & Analysis

- [x] Timeline exports (`tags_timeline.py`, `tags_timeline_country.py`, `tags_timeline_region.py`)
- [x] Comparison across tagging versions
- [x] Comparison across recommendations versions
- [x] Comparison export to CSV with version headers
- [x] Year-over-year trend analysis (via timeline exports)

### Enhanced Normalization

- [x] Country/region normalization with ISO codes
- [x] Preservation of `_raw` fields for provenance
- [x] Complete ISO 3166-1 alpha-2 mapping (194 countries)
- [x] Automatic doc type classification (Policy, Law, TreatyBody, etc.)
- [ ] Source reliability scoring (Phase 4)

### Scorecard Maintenance

- [x] Alternative source identification for failed monitors
- [x] Phase 1 critical updates (6 countries, 18 fields, 20+ year old entries)
- [x] Multi-format exports (CSV, XLSX, ODS, Google Sheets JSON)
- [x] Update documentation and workflows
- [ ] Phase 2-4 updates (ongoing maintenance)

______________________________________________________________________

## Phase 4: Research Dashboard (🚧 IN PROGRESS - 2/4 Complete)

### Backend API (✅ COMPLETE - Week 1 & 2)

- [x] Flask backend infrastructure (app factory, config, extensions)
- [x] RESTful API endpoints:
  - [x] `/api/health` - API health check
  - [x] `/api/info` - System statistics
  - [x] `/api/documents` - list/filter documents (9 filters, pagination, sorting)
  - [x] `/api/documents/:id` - document detail
  - [x] `/api/scorecard` - countries summary (with region filter)
  - [x] `/api/scorecard/:country` - country indicators
  - [x] `/api/scorecard/indicators/statistics` - indicator value distribution
  - [ ] `/api/tags` - tag frequency and filters (Week 3)
  - [ ] `/api/timeline` - temporal analysis (Week 3)
  - [ ] `/api/export` - download datasets (Week 3)
- [ ] Authentication and rate limiting (Week 4)
- [x] Caching layer for performance (15min documents, 1hr scorecard)
- [x] Request validation and error handling
- [x] Standard JSON response format
- [x] 39 test cases written (12 unit + 27 integration)
- [x] API documentation (README, Quick Start, Week 1/2 summaries)

**Status:** 9 endpoints working (100% pass rate), ready for frontend integration

### Visualization Frontend

- [ ] Interactive dashboard (React or Vue.js)
- [ ] Tag frequency bar charts and heatmaps
- [ ] Timeline visualizations (D3.js or Plotly)
- [ ] Country/region filtering
- [ ] Scorecard indicator displays
- [ ] Interactive filters (region, country, tags, year, source)
- [ ] Export/download UI for datasets
- [ ] Mobile-responsive design

### Charts & Analysis

- [ ] Tag frequency bar charts
- [ ] Timeline view (tags over time)
- [ ] Geographic heatmaps (countries × tags)
- [ ] Comparison mode (version side-by-side)
- [ ] Scorecard indicator visualizations
- [ ] Gap analysis (missing data visualization)
- [ ] Correlation analysis (tags vs indicators)

______________________________________________________________________

## Phase 5: Global Expansion (📅 FUTURE)

### Geographic Expansion

- [ ] European sources (EU, Council of Europe)
- [ ] Asian sources (ASEAN, national bodies)
- [ ] Americas sources (OAS, IACHR)
- [ ] Merge African + global content
- [ ] Multi-language support (translation pipeline)

### Advanced Features

- [ ] Machine learning for document classification
- [ ] Automated entity extraction (organizations, people, dates)
- [ ] Sentiment analysis on recommendations
- [ ] Network analysis (document citations)
- [ ] Automated report generation
- [ ] Email alerts for new documents
- [ ] Collaborative annotation tools

### Integration & API

- [ ] Public API for researchers
- [ ] Integration with human rights databases
- [ ] Data export to common formats (JSON-LD, RDF)
- [ ] Citation management integration (Zotero, Mendeley)
- [ ] SPARQL endpoint for semantic queries

______________________________________________________________________

## Phase 6: Sustainability & Community (📅 FUTURE)

### Infrastructure

- [ ] Cloud deployment (AWS/GCP/Azure)
- [ ] Automated daily scraper runs
- [ ] Database migration (from JSON to PostgreSQL)
- [ ] Data versioning and snapshots
- [ ] Disaster recovery and backups

### Community & Documentation

- [ ] Contributor guidelines
- [ ] Research methodology documentation
- [ ] User guides and tutorials
- [ ] Video walkthroughs
- [ ] Academic publications and citations
- [ ] Conference presentations

### Quality & Maintenance

- [ ] Automated data quality checks
- [ ] Link rot monitoring and alerts
- [ ] Performance optimization (caching, indexing)
- [ ] Code refactoring and technical debt reduction
- [ ] Security audits and updates

______________________________________________________________________

## Current Status Summary

**Completed:**

- ✅ Core pipeline (scraping, processing, tagging) - Multiple sources: 6 automated scrapers + direct URL tracking
- ✅ Scorecard system (194 countries, 10 indicators, 2,543 source URLs tracked)
- ✅ Validation and security framework - 170 tests passing (68 validator tests)
- ✅ Recommendations extraction system - Regex-based with versioning and history tracking
- ✅ Timeline exports - Global, by-country, and by-region analysis over time
- ✅ Comparison analytics - Compare tags and recommendations across versions
- ✅ ISO 3166-1 alpha-2 country code mapping - 194 countries fully mapped
- ✅ Document type classifier - Multi-stage rules-based classification
- ✅ Scorecard maintenance - Phase 1 critical updates (6 countries, 18 fields updated)
- ✅ Multi-format scorecard exports - CSV, XLSX, ODS, Google Sheets JSON
- ✅ Comprehensive documentation (40+ markdown files)

**In Progress (Phase 4 - Week 1 & 2 Complete):**

- ✅ Flask API backend (9 endpoints working, documented, tested)
- ⏳ Tags, Timeline, Export APIs (Week 3-5)
- ⏳ Authentication and rate limiting (Week 4)
- ⏳ Dashboard frontend (Phase 4 later)
- ⏳ NLP-based recommendations extraction (planned for Phase 5)

**Next Priority:**

- 🚧 **Phase 4 API (Weeks 3-5):** Tags, Timeline, Export endpoints + Authentication
- 🎯 Interactive dashboard frontend (React/Vue.js with D3.js visualizations)
- 🎯 Source reliability scoring
- 🎯 Continue scorecard maintenance (Phases 2-4: 41 remaining stale entries)

______________________________________________________________________

## Metrics

- **Lines of Code:** ~18,000+ (Python, config, tests, API)
- **Test Coverage:** 209 tests (170 pipeline + 39 API)
- **Documentation:** 45+ markdown files, comprehensive API docs
- **Data Sources:** 7 scrapers (AU, OHCHR, UPR, UNICEF, ACERWC, ACHPR, manual)
- **Countries Tracked:** 194 (via scorecard, all with ISO 3166-1 alpha-2 codes)
- **Documents Tracked:** 78 (via metadata.json)
- **Indicators:** 10 per country (29 total indicator fields tracked)
- **Source URLs:** 2,543 tracked and validated
- **Tags Versions:** 4 (v1, v2, v3, digital)
- **Export Formats:** CSV, XLSX, ODS, Google Sheets JSON (scorecard)
- **API Endpoints:** 9 working (health, info, documents × 2, scorecard × 5)

______________________________________________________________________

## Contributing

The project is actively developed. Contributions welcome in:

1. **New scrapers** for additional sources
1. **Enhanced processors** (OCR, image extraction)
1. **Visualization components** for dashboard
1. **Documentation** improvements and examples
1. **Testing** coverage expansion
1. **Performance** optimizations

______________________________________________________________________

## Notes

- End-to-end pipeline is production-ready for AU Policy + scorecard workflow
- Future work focuses on expanding analytics and building research dashboard
- All core infrastructure is stable and well-tested (170 tests passing in ~106 seconds)
- Documentation is comprehensive and up-to-date
- **Recent Completions (January 2026):**
  - Migrated from PyPDF2 to pypdf - no more deprecation warnings
  - ISO 3166-1 alpha-2 mapping for all 194 countries
  - Document type classifier (multi-stage rules-based)
  - Scorecard Phase 1 maintenance (6 countries, 18 fields updated)
  - **Flask API backend (Week 1-2):** 9 endpoints, filtering, pagination, caching, validation

______________________________________________________________________

Last updated: January 2026
