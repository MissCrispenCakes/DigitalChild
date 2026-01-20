# GRIMdata / LittleRainbowRights

## Open-Source Human Rights Data Pipeline

**Analyze child and LGBTQ+ digital protection through automated document analysis**

[Get Started](getting-started/installation.md){ .md-button .md-button--primary }
[View Scorecard](scorecard/index.md){ .md-button }
[GitHub](https://github.com/MissCrispenCakes/DigitalChild){ .md-button }

______________________________________________________________________

## What is GRIMdata?

**GRIMdata** (Global Rights Information Monitoring) is a research initiative using automated data pipelines to analyze human rights documents from international organizations. The platform hosts multiple focused projects, each examining specific human rights themes.

### Our Projects

<div class="grid cards" markdown>

- :rainbow:{ .lg .middle } **LittleRainbowRights**

  ______________________________________________________________________

  Child and LGBTQ+ digital rights research. Tracks 10 indicators across 194 countries: AI policy, data protection, LGBTQ+ legal status, child online protection, and more.

  [:octicons-arrow-right-24: Explore Project](projects/littlerainbowrights/index.md)

- :material-hand-heart:{ .lg .middle } **SGBV-UPR**

  ______________________________________________________________________

  Sexual and gender-based violence analysis using Universal Periodic Review recommendations. Published research examining SGBV patterns across countries.

  [:octicons-arrow-right-24: Explore Project](projects/sgbv/index.md)

</div>

Each project has its own dedicated page accessible via its own domain:

- **grimdata.org** - Main hub (this site)
- **grimdata.org/projects/littlerainbowrights/** - LittleRainbowRights project
- **grimdata.org/projects/sgbv/** - SGBV-UPR project
- **littlerainbowrights.com** - Direct link to LittleRainbowRights (redirects to project page)

## What is DigitalChild?

**DigitalChild** is the open-source Python pipeline powering these analyses. It scrapes, processes, and analyzes human rights documents with flexible tagging and enrichment capabilities.

The pipeline is designed to be:

- **Modular** - Easy to add new data sources and analysis methods
- **Transparent** - All processing steps documented and reproducible
- **Secure** - Input validation protects against malicious data
- **Extensible** - Researchers can adapt for their own projects

## Key Features

<div class="grid cards" markdown>

- :material-download:{ .lg .middle } **Automated Scraping**

  ______________________________________________________________________

  Collect documents from 7 international sources including AU, OHCHR, UPR, and UNICEF. Respectful, rate-limited scraping with robust error handling.

  [:octicons-arrow-right-24: Learn more](guides/RUNBOOK.md)

- :material-tag-multiple:{ .lg .middle } **Intelligent Tagging**

  ______________________________________________________________________

  Regex-based tagging system identifies themes: child rights, LGBTQ+ rights, AI, privacy, digital policy. Versioned tags enable comparison.

  [:octicons-arrow-right-24: See formats](standards/TAGS_CONFIG_FORMAT.md)

- :material-chart-bar:{ .lg .middle } **Comprehensive Scorecard**

  ______________________________________________________________________

  Track 10 indicators across 194 countries. 2,543 validated source URLs ensure transparency. Automated validation and change detection.

  [:octicons-arrow-right-24: View scorecard](scorecard/index.md)

- :material-shield-check:{ .lg .middle } **Security First**

  ______________________________________________________________________

  68 validator tests protect against path traversal, URL injection, and malicious input. Built-in security from the ground up.

  [:octicons-arrow-right-24: Security policy](../SECURITY.md)

</div>

## Quick Example

```bash
# Install and run
python init_project.py
pip install -r requirements.txt
python pipeline_runner.py --source au_policy --tags-version latest

# Results appear in data/exports/
ls data/exports/
# tags_summary.csv
# scorecard_summary.csv
```

## Who Is This For?

<div class="grid cards" markdown>

- :fontawesome-solid-graduation-cap:{ .middle } **Researchers**

  ______________________________________________________________________

  Academics studying digital rights trends, child protection policies, LGBTQ+ legal status across countries.

- :fontawesome-solid-building-columns:{ .middle } **NGOs & Advocates**

  ______________________________________________________________________

  Human rights organizations tracking protections, building evidence for campaigns, monitoring policy changes.

- :fontawesome-solid-chart-line:{ .middle } **Policy Analysts**

  ______________________________________________________________________

  Government and UN policy staff comparing policies across countries, identifying gaps and best practices.

- :fontawesome-solid-newspaper:{ .middle } **Journalists**

  ______________________________________________________________________

  Investigative reporters researching digital rights stories with verified data and authoritative sources.

</div>

## Project Status

!!! success "Phase 1-2 Complete"
\- ✅ Core pipeline operational (7 sources)
\- ✅ Scorecard system live (194 countries, 10 indicators)
\- ✅ Security framework implemented (124 tests passing)
\- ✅ Comprehensive documentation

!!! info "Phase 3 In Progress"
\- 🔄 Recommendations extraction (NLP-based)
\- 🔄 Timeline visualizations
\- 🔄 Comparison analytics

See [Roadmap](ROADMAP.md) for detailed development plan.

## Scorecard Indicators

The scorecard tracks 10 critical indicators:

1. **AI Policy Status** - Published AI strategies and frameworks
1. **Data Protection Law** - Comprehensive data protection legislation
1. **LGBTQ+ Legal Status** - Legal recognition and protections
1. **Child Online Protection** - Measures safeguarding children online
1. **SIM Biometric Registration** - Biometric requirements for mobile SIM cards
1. **Encryption Backdoors** - Government-mandated encryption weaknesses
1. **Promotion/Propaganda Laws** - Restrictions on LGBTQ+ discussion
1. **DPA Independence** - Data Protection Authority autonomy
1. **Content Moderation** - Regulations on harmful content removal
1. **Age Verification** - Requirements to verify user age

Each indicator includes the current status and authoritative source URL.

[Explore Scorecard Data](scorecard/index.md){ .md-button }

## Technology Stack

- **Python 3.12** - Modern language features
- **BeautifulSoup4** - HTML parsing for scrapers
- **Selenium** - Dynamic website scraping
- **pandas** - Data manipulation and analysis
- **PyPDF2** - PDF text extraction
- **pytest** - Comprehensive test suite (124 tests)
- **MkDocs Material** - Beautiful documentation

## Open Source & Open Data

**Dual licensing for transparency and attribution:**

- **Code:** MIT License - Use freely, including commercial applications
- **Data & Documentation:** CC BY 4.0 - Attribution required

This ensures the pipeline is freely usable while giving credit to the research effort behind the scorecard compilation.

## Get Involved

<div class="grid" markdown>

!!! tip "For Users"
1\. [Install](getting-started/installation.md) the pipeline
2\. Review [FAQ](FAQ.md) for common questions
3\. Check [First Run Errors](guides/FIRST_RUN_ERRORS.md) if issues arise
4\. [Cite](../CITATION.cff) in your publications

!!! example "For Contributors"
1\. Read [Contributing Guide](../CONTRIBUTING.md)
2\. Find [good first issues](https://github.com/MissCrispenCakes/DigitalChild/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)
3\. Submit pull requests
4\. Improve [documentation](README.md)

</div>

## Contact & Support

- **Issues:** [GitHub Issues](https://github.com/MissCrispenCakes/DigitalChild/issues)
- **Discussions:** [GitHub Discussions](https://github.com/MissCrispenCakes/DigitalChild/discussions)
- **Website:** [LittleRainbowRights.com](https://littlerainbowrights.com)

!!! warning "Maintained by PhD Student"
This project is maintained part-time by one person alongside PhD research. Response times may vary. Your patience is appreciated!

## Acknowledgments

This project analyzes publicly available human rights documents from:

- United Nations (OHCHR, UPR, UNICEF)
- African Union (AU Policy, ACERWC, ACHPR)
- UNESCO, UNCTAD, ILGA World, and other authoritative sources

All 2,543 source URLs are validated and publicly accessible for verification.

______________________________________________________________________

**Mission:** Support evidence-based human rights research and advocacy for vulnerable populations in the digital age.
