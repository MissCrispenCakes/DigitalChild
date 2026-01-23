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
- [x] Comprehensive test suite (124 tests passing)
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

## Phase 3: Advanced Processing (⏳ IN PROGRESS - 73% Complete)

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
- [ ] Complete ISO 3166-1 alpha-2 mapping
- [ ] Automatic doc type classification (Policy, Law, TreatyBody, etc.)
- [ ] Source reliability scoring

______________________________________________________________________

## Phase 4: Research Dashboard (🔜 PLANNED)

### Backend API

- [ ] Flask backend for serving metadata/exports
- [ ] RESTful API endpoints:
  - [ ] `/api/documents` - list/filter documents
  - [ ] `/api/tags` - tag frequency and filters
  - [ ] `/api/scorecard` - country indicators
  - [ ] `/api/timeline` - temporal analysis
  - [ ] `/api/export` - download datasets
- [ ] Authentication and rate limiting
- [ ] Caching layer for performance

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
- ✅ Validation and security framework - 124 tests passing (68 validator tests)
- ✅ Recommendations extraction system - Regex-based with versioning and history tracking
- ✅ Timeline exports - Global, by-country, and by-region analysis over time
- ✅ Comparison analytics - Compare tags and recommendations across versions
- ✅ Comprehensive documentation (40 markdown files)

**In Progress (Phase 3 - 73% Complete):**

- ⏳ Complete ISO 3166-1 alpha-2 country code mapping
- ⏳ Automatic doc type classification (Policy, Law, TreatyBody, etc.)
- ⏳ Source reliability scoring
- ⏳ NLP-based recommendations extraction (planned)

**Next Priority:**

- 🎯 Complete remaining Phase 3 normalization features
- 🎯 Begin research dashboard prototyping (Phase 4)
- 🎯 Interactive scorecard visualizations

______________________________________________________________________

## Metrics

- **Lines of Code:** ~15,000+ (Python, config, tests)
- **Test Coverage:** 124 tests passing, comprehensive validation
- **Documentation:** 40 markdown files, 1 comprehensive guide (CLAUDE.md)
- **Data Sources:** 7 scrapers (AU, OHCHR, UPR, UNICEF, ACERWC, ACHPR, manual)
- **Countries Tracked:** 194 (via scorecard)
- **Indicators:** 10 per country
- **Source URLs:** 2,543 tracked and validated
- **Tags Versions:** 4 (v1, v2, v3, digital)

______________________________________________________________________

## Contributing

The project is actively developed. Contributions welcome in:

1. **New scrapers** for additional sources
1. **Enhanced processors** (OCR, image extraction)
1. **Visualization components** for dashboard
1. **Documentation** improvements and examples
1. **Testing** coverage expansion
1. **Performance** optimizations

See [CLAUDE.md](https://github.com/MissCrispenCakes/DigitalChild/blob/basecamp/CLAUDE.md) for development guide.

______________________________________________________________________

## Notes

- End-to-end pipeline is production-ready for AU Policy + scorecard workflow
- Future work focuses on expanding analytics and building research dashboard
- All core infrastructure is stable and well-tested (124 tests passing in ~106 seconds)
- Documentation is comprehensive and up-to-date
- **Known:** PyPDF2 deprecation warning - planned migration to `pypdf` library in future update

______________________________________________________________________

Last updated: January 2026
