# Documentation Overview

This directory contains comprehensive documentation for the **DigitalChild** pipeline - the Python codebase powering the **LittleRainbowRights** project within the **GRIMdata.org** platform.

**GRIMdata** (grimdata.org) hosts multiple human rights research projects:

- **LittleRainbowRights** - Child and LGBTQ+ digital rights (this repository: DigitalChild)
- **SGBV-UPR** - Sexual and gender-based violence analysis (separate repository: HumanRights - *currently private, under construction*)

## Quick Navigation

### Getting Started

- **[website/getting-started/installation.md](website/getting-started/installation.md)** - Installation and setup instructions
- **[website/getting-started/quickstart.md](website/getting-started/quickstart.md)** - Quick start guide for first-time users
- **[api/index.md](api/index.md)** - 🆕 **REST API Documentation** (14 endpoints for programmatic access - production ready)
- **[api/quick-reference.md](api/quick-reference.md)** - 🆕 **API Quick Reference** (skimmable cheat sheet)
- **[DOCS_INDEX.md](DOCS_INDEX.md)** - Complete index of all documentation files
- **[guides/FIRST_RUN_ERRORS.md](guides/FIRST_RUN_ERRORS.md)** - Common errors and solutions for first-time users

### Core Documentation

#### Architecture & Standards

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Complete system architecture overview
- **[FAQ.md](FAQ.md)** - Frequently asked questions
- **[GLOSSARY.md](GLOSSARY.md)** - Definitions of key terms
- **[DATA_GOVERNANCE.md](DATA_GOVERNANCE.md)** - Privacy, ethics, data handling
- **[notes/DIRECTORY_STRUCTURE.md](notes/DIRECTORY_STRUCTURE.md)** - Project folder structure explained
- **[notes/PIPELINE_FLOW.md](notes/PIPELINE_FLOW.md)** - End-to-end data flow through the pipeline
- **[standards/METADATA_SCHEMA.md](standards/METADATA_SCHEMA.md)** - Metadata JSON structure and fields
- **[standards/FILE_NAMING_STANDARDS.md](standards/FILE_NAMING_STANDARDS.md)** - File naming conventions

#### Processing & Features

- **[guides/VALIDATORS_USAGE.md](guides/VALIDATORS_USAGE.md)** - Using the centralized validation module
- **[guides/SCORECARD_WORKFLOW.md](guides/SCORECARD_WORKFLOW.md)** - Complete scorecard system guide
- **[standards/TAGS_CONFIG_FORMAT.md](standards/TAGS_CONFIG_FORMAT.md)** - Tag configuration structure
- **[standards/SCRAPER_STRUCTURE.md](standards/SCRAPER_STRUCTURE.md)** - How to build scrapers

#### Development & Testing

- **[guides/RUNBOOK.md](guides/RUNBOOK.md)** - Common commands for running pipelines and tests
- **[reviews/PROCESSOR_TEST_RUN.md](reviews/PROCESSOR_TEST_RUN.md)** - Testing individual processors
- **[ROADMAP.md](ROADMAP.md)** - Project roadmap and development phases

## Documentation Organization

### `/docs` (Root)

Core documentation and project overview (not website content):

- Architecture overview
- FAQ and glossary
- Data governance policies
- Project roadmap
- Documentation index

### `/docs/guides` (User Guides)

Operational guides for users:

- Runbook with all commands
- First-run troubleshooting
- Scorecard workflow guide
- Validators usage guide

### `/docs/planning` (Planning Documents)

Feature planning and feasibility:

- Source feasibility checklists
- Visualization plans
- Future feature proposals

### `/docs/reviews` (Test & Review)

Test results and reviews:

- Processor test runs
- Scorecard reviews
- Analysis summaries

### `/docs/notes` (Implementation Notes)

Technical notes about how systems work:

- Pipeline flow and logging details
- Tags versioning and exports
- Comparison exports
- Directory structure

### `/docs/standards` (Standards & Formats)

Format specifications and conventions:

- Metadata schema
- Config file formats (tags, recommendations, comparisons)
- File naming rules
- Document type standards
- ISO country/region mapping
- Scraper structure

### `/docs/website` (Website Content)

MkDocs website-specific content (separated from core documentation):

- `index.md` - Website landing page
- `getting-started/` - Installation and quickstart guides for new users
- `projects/` - Project overview pages (LittleRainbowRights, SGBV-UPR)
- `scorecard/` - Interactive scorecard visualizations and data explorer
- `javascripts/` - Custom JavaScript for website functionality
- `stylesheets/` - Custom CSS for website styling

**Note:** This content is for the public-facing website (grimdata.org), while documentation in `/docs` root and subdirectories is for developers and researchers working with the pipeline.

## Key Features Documented

### Core Pipeline (Phase 1 - Complete)

- ✅ Document scraping (AU Policy, OHCHR, UPR, UNICEF, etc.)
- ✅ Multi-format processing (PDF, DOCX, HTML)
- ✅ Metadata tracking and versioning
- ✅ Tagging system with version control
- ✅ Comprehensive logging
- ✅ Full test suite (170 tests)

### Scorecard System (Phase 2 - Complete)

- ✅ Country-level indicator tracking (10 metrics per country, 194 countries)
- ✅ Metadata enrichment with scorecard data
- ✅ CSV export functionality (summary, sources, indicators)
- ✅ URL validation and monitoring
- ✅ Source change detection
- ✅ Multi-format exports (CSV, XLSX, ODS, Google Sheets JSON)
- ✅ Maintenance documentation and update workflows

### Validation & Security (Phase 2 - Complete)

- ✅ Centralized validation module (68 tests)
- ✅ URL validation with malicious pattern blocking
- ✅ Path validation with traversal protection
- ✅ File size and extension validation
- ✅ Config and schema validation

### Advanced Processing (Phase 3 - Complete, 8/9 tasks)

- ✅ ISO 3166-1 alpha-2 country code mapping (194 countries)
- ✅ Document type classification system (rules-based multi-stage)
- ✅ Scorecard data maintenance (Phase 1 critical updates: 6 countries, 18 fields)
- ✅ Alternative source monitoring (replaced 2 failed sources)
- ⬜ Research dashboard (Phase 4 kickoff) - Planned

## Project Identity

**Name:** GRIMdata / LittleRainbowRights

**Domains:**

- https://GRIMdata.org
- https://LittleRainbowRights.com

**Purpose:** Pipeline for analyzing child & LGBTQ+ digital protections through automated scraping, processing, and analysis of human rights documents.

**Tech Stack:** Python 3.12, BeautifulSoup4, Selenium, pandas, pypdf, pytest

## Getting Help

1. **First-time setup issues?** → See [guides/FIRST_RUN_ERRORS.md](guides/FIRST_RUN_ERRORS.md)
1. **Need to understand a feature?** → Check [DOCS_INDEX.md](DOCS_INDEX.md) for relevant docs
1. **Want to contribute?** → Read [ROADMAP.md](ROADMAP.md) for planned features

## Documentation Maintenance

All documentation is maintained in Markdown format and version-controlled in Git. When features are added or modified:

1. Update relevant documentation files
1. Add new sections to appropriate subdirectories
1. Update [DOCS_INDEX.md](DOCS_INDEX.md) with new files
1. Keep examples and commands current with actual implementation

Last major update: January 2026
