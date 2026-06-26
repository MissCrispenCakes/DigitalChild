# DigitalChild Documentation

Welcome to the complete documentation for **DigitalChild** (LittleRainbowRights), a Python pipeline for analyzing human rights documents with focus on child and LGBTQ+ digital protections.

## Quick Links

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } **Getting Started**

    ---

    Install and run your first pipeline

    [:octicons-arrow-right-24: Quick Start](website/getting-started/quickstart.md)

-   :material-api:{ .lg .middle } **REST API**

    ---

    Access data programmatically via 14 endpoints

    [:octicons-arrow-right-24: API Documentation](api/index.md)

-   :material-chart-bar:{ .lg .middle } **Scorecard**

    ---

    Explore 10 indicators across 194 countries

    [:octicons-arrow-right-24: Digital Rights Scorecard](scorecard/index.md)

-   :material-help-circle:{ .lg .middle } **Help & Support**

    ---

    Common questions and troubleshooting

    [:octicons-arrow-right-24: FAQ](FAQ.md)

</div>

## Documentation Sections

### Getting Started
- [Installation](website/getting-started/installation.md) - Set up DigitalChild on your system
- [Quick Start](website/getting-started/quickstart.md) - Run your first pipeline in 5 minutes
- [First Run Errors](guides/FIRST_RUN_ERRORS.md) - Troubleshooting guide

### Core Guides
- [Runbook](guides/RUNBOOK.md) - Complete pipeline operations guide
- [Scorecard Workflow](guides/SCORECARD_WORKFLOW.md) - Country indicator system
- [Production Deployment](guides/PRODUCTION_DEPLOYMENT.md) - Deploy the API in production

### API Documentation
- [API Overview](api/index.md) - REST API features and quickstart
- [API Reference](api/reference.md) - All 14 endpoints with examples
- [API Quick Reference](api/quick-reference.md) - Endpoint cheat sheet

### Scorecard
- [Scorecard Overview](scorecard/index.md) - What it tracks and why
- [Design & Methodology](scorecard/design.md) - How indicators are defined
- [Data Access](scorecard/data-access.md) - API, CSV, and file access
- [Visualization](scorecard/visualization.md) - Interactive map, indicator & regional charts
- [Data Explorer](scorecard/explorer.md) - Filter, search, sort & compare countries

### Transparency Watch
- [Source Transparency Watch](transparency-watch/index.md) - When peer organisations adopt open-data transparency

### Standards & Specifications
- [Metadata Schema](standards/METADATA_SCHEMA.md) - Document metadata structure
- [Tags Config Format](standards/TAGS_CONFIG_FORMAT.md) - Tagging system format
- [Scraper Structure](standards/SCRAPER_STRUCTURE.md) - How to build scrapers
- [File Naming Standards](standards/FILE_NAMING_STANDARDS.md) - Naming conventions

### Technical Architecture
- [Architecture](ARCHITECTURE.md) - System design overview
- [Roadmap](ROADMAP.md) - Development phases and progress

### Project Information
- [FAQ](FAQ.md) - Frequently asked questions
- [Contributing](CONTRIBUTING.md) - How to contribute
- [License](https://github.com/MissCrispenCakes/DigitalChild/blob/basecamp/LICENSE) - MIT License

## Project Structure

```
DigitalChild/
├── pipeline_runner.py      # Main entry point
├── scrapers/               # Web scrapers for document sources
├── processors/             # Text extraction and tagging
├── api/                    # Flask REST API (Phase 4)
├── data/
│   ├── raw/               # Downloaded documents
│   ├── processed/         # Extracted text
│   ├── metadata/          # Document metadata with tags
│   └── exports/           # CSV exports for analysis
├── configs/               # Tag configurations and URL dictionaries
├── docs/                  # This documentation
└── tests/                 # Test suite (347 tests)
```

## Key Features

- **Document Pipeline:** Scrape → Process → Tag → Enrich → Export
- **REST API:** 14 production endpoints with authentication and rate limiting
- **Scorecard System:** 10 indicators × 194 countries for digital rights analysis
- **Flexible Tagging:** Regex-based tagging with version control
- **Data Quality:** Automated validation of 2,543 source URLs
- **Open Source:** MIT license for code, CC BY 4.0 for data

## Support

- **Issues & Bugs:** [GitHub Issues](https://github.com/MissCrispenCakes/DigitalChild/issues)
- **Discussions:** [GitHub Discussions](https://github.com/MissCrispenCakes/DigitalChild/discussions)
- **Questions:** [FAQ](FAQ.md)
- **Website:** [grimdata.org](https://grimdata.org)

## Citation

```bibtex
@software{littlerainbowrights2025,
  title = {DigitalChild / LittleRainbowRights: Child and LGBTQ+ Digital Rights Analysis Pipeline},
  author = {Vollmer, D.T. and Vollmer, S.C.},
  year = {2025},
  version = {2.0.1},
  url = {https://github.com/MissCrispenCakes/DigitalChild},
  doi = {10.5281/zenodo.18318098},
  license = {MIT}
}
```

---

**Version:** 2.1.0 (live) · last archived release 2.0.1 (DOI: 10.5281/zenodo.18318098)
**Last Updated:** June 2026
**License:** MIT (code) / CC BY 4.0 (data)
