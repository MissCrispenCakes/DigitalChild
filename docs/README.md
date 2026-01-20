# Documentation Overview

This directory contains comprehensive documentation for the DigitalChild (GRIMdata / LittleRainbowRights) project - a Python data pipeline for scraping, processing, and analyzing human rights documents with focus on child and LGBTQ+ digital protection.

## Quick Navigation

### Getting Started

- **[../README.md](../README.md)** - Project README with setup instructions and quickstart
- **[../CLAUDE.md](../CLAUDE.md)** - Comprehensive guide for Claude Code AI assistant
- **[DOCS_INDEX.md](DOCS_INDEX.md)** - Complete index of all documentation files
- **[runs/FIRST_RUN_ERRORS.md](runs/FIRST_RUN_ERRORS.md)** - Common errors and solutions for first-time users

### Core Documentation

#### Architecture & Standards

- **[notes/DIRECTORY_STRUCTURE.md](notes/DIRECTORY_STRUCTURE.md)** - Project folder structure explained
- **[notes/PIPELINE_FLOW.md](notes/PIPELINE_FLOW.md)** - End-to-end data flow through the pipeline
- **[standards/METADATA_SCHEMA.md](standards/METADATA_SCHEMA.md)** - Metadata JSON structure and fields
- **[standards/FILE_NAMING_STANDARDS.md](standards/FILE_NAMING_STANDARDS.md)** - File naming conventions

#### Processing & Features

- **[VALIDATORS_USAGE.md](VALIDATORS_USAGE.md)** - Using the centralized validation module
- **[SCORECARD_WORKFLOW.md](SCORECARD_WORKFLOW.md)** - Complete scorecard system guide
- **[standards/TAGS_CONFIG_FORMAT.md](standards/TAGS_CONFIG_FORMAT.md)** - Tag configuration structure
- **[standards/SCRAPER_STRUCTURE.md](standards/SCRAPER_STRUCTURE.md)** - How to build scrapers

#### Development & Testing

- **[runs/RUNBOOK.md](runs/RUNBOOK.md)** - Common commands for running pipelines and tests
- **[runs/PROCESSOR_TEST_RUN.md](runs/PROCESSOR_TEST_RUN.md)** - Testing individual processors
- **[ROADMAP.md](ROADMAP.md)** - Project roadmap and development phases

## Documentation Organization

### `/docs` (Main Documentation)

Top-level guides and workflow documentation:

- Setup guides and troubleshooting
- Feature workflows (scorecard, validators, tags)
- Project planning (roadmap, feasibility checklists)
- Comprehensive index

### `/docs/notes` (Implementation Notes)

Technical notes about how systems work:

- Pipeline flow and logging details
- Tags versioning and exports
- Comparison exports
- Directory structure

### `/docs/runs` (Run Guides)

Practical guides for running the pipeline:

- First-run error solutions
- Test commands
- Pipeline execution recipes

### `/docs/standards` (Standards & Formats)

Format specifications and conventions:

- Metadata schema
- Config file formats (tags, recommendations, comparisons)
- File naming rules
- Document type standards
- ISO country/region mapping
- Scraper structure

## Key Features Documented

### Core Pipeline (Phase 1 - Complete)

- ✅ Document scraping (AU Policy, OHCHR, UPR, UNICEF, etc.)
- ✅ Multi-format processing (PDF, DOCX, HTML)
- ✅ Metadata tracking and versioning
- ✅ Tagging system with version control
- ✅ Comprehensive logging
- ✅ Full test suite (124 tests)

### Scorecard System (Phase 2 - Complete)

- ✅ Country-level indicator tracking (10 metrics per country, 194 countries)
- ✅ Metadata enrichment with scorecard data
- ✅ CSV export functionality (summary, sources, indicators)
- ✅ URL validation and monitoring
- ✅ Source change detection

### Validation & Security (Phase 2 - Complete)

- ✅ Centralized validation module (68 tests)
- ✅ URL validation with malicious pattern blocking
- ✅ Path validation with traversal protection
- ✅ File size and extension validation
- ✅ Config and schema validation

## Project Identity

**Name:** GRIMdata / LittleRainbowRights

**Domains:**

- https://GRIMdata.org
- https://LittleRainbowRights.com

**Purpose:** Pipeline for analyzing child & LGBTQ+ digital protections through automated scraping, processing, and analysis of human rights documents.

**Tech Stack:** Python 3.12, BeautifulSoup4, Selenium, pandas, PyPDF2, pytest

## Getting Help

1. **First-time setup issues?** → See [runs/FIRST_RUN_ERRORS.md](runs/FIRST_RUN_ERRORS.md)
2. **Need to understand a feature?** → Check [DOCS_INDEX.md](DOCS_INDEX.md) for relevant docs
3. **Want to contribute?** → Read [ROADMAP.md](ROADMAP.md) for planned features
4. **Using Claude Code?** → See [../CLAUDE.md](../CLAUDE.md) for AI assistant guidance

## Documentation Maintenance

All documentation is maintained in Markdown format and version-controlled in Git. When features are added or modified:

1. Update relevant documentation files
2. Add new sections to appropriate subdirectories
3. Update [DOCS_INDEX.md](DOCS_INDEX.md) with new files
4. Keep examples and commands current with actual implementation

Last major update: January 2026
