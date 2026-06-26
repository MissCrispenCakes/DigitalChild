# GRIMdata Research Projects

[:octicons-home-24: Back to GRIMdata Home](../index.md){ .md-button }

**Two complementary research tracks analyzing human rights through automated document analysis**

______________________________________________________________________

## Current Projects

<div class="grid cards" markdown>

-   :rainbow:{ .lg .middle } __LittleRainbowRights__

    ---

    **Status:** Active | **Scope:** Global (194 countries)

    Child and LGBTQ+ digital rights research tracking 10 indicators across all countries. Features production-ready REST API with 14 endpoints, comprehensive scorecard, and 2,543 validated sources.

    **Key Features:**

    - 10 digital rights indicators
    - 194 countries tracked
    - 2,543 validated source URLs
    - 14 REST API endpoints
    - Open-source Python pipeline

    **Published:** [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18318098.svg)](https://doi.org/10.5281/zenodo.18318098)

    [:octicons-arrow-right-24: Explore Project](littlerainbowrights/index.md){ .md-button .md-button--primary }
    [:octicons-database-24: View Scorecard](../../scorecard/){ .md-button }

-   :material-hand-heart:{ .lg .middle } __SGBV-UPR__

    ---

    **Status:** Published (2022) | **Scope:** SADC → Expanding globally

    Sexual and gender-based violence analysis using Universal Periodic Review recommendations. Foundational research demonstrating automated UPR analysis methodology at regional scale.

    **Key Features:**

    - UPR recommendations analysis
    - SGBV thematic focus
    - Regional to global expansion
    - Peer-reviewed methodology
    - Published research (2022)

    **Published:** [Vollmer & Vollmer (2022), Stellenbosch Law Review](https://doi.org/10.47348/SLR/2022/i1a1)

    [:octicons-arrow-right-24: View Project](sgbv/index.md){ .md-button .md-button--primary }

</div>

______________________________________________________________________

## Research Evolution

**SGBV-UPR** (2019-2022) validated the core methodology for automated human rights document analysis at regional scale, focusing on SADC member states and SGBV themes. This foundational work was published in peer-reviewed literature.

**LittleRainbowRights** (2025-present) expands this approach to global digital rights analysis, tracking 10 indicators across 194 countries with comprehensive testing, production-ready API, and reproducible workflows.

Both projects share the same commitment to:

- **Open data** - CC BY 4.0 licensing
- **Transparent methodology** - Fully documented pipelines
- **Authoritative sources** - Validated URLs from UN agencies, NGOs, governments
- **Research quality** - Peer review, testing, version control

## Technical Stack

Both projects use the GRIMdata pipeline infrastructure:

- **Python 3.12** - Core language
- **BeautifulSoup4 & Selenium** - Web scraping
- **pandas** - Data analysis
- **Flask** - REST API (LittleRainbowRights)
- **pytest** - Testing framework (347 tests total)
- **MkDocs Material** - Documentation

## Publications

### LittleRainbowRights

- Vollmer, DT and Vollmer, SC. (2025). *Queer AI for the digital child: Examining the response to advanced digital technologies on the human rights of LGBTQ+ children in Africa.* Presented at the Second International Conference on Children's Rights, Stellenbosch, South Africa, September 9-11, 2025. [DOI: 10.5281/zenodo.18318098](https://doi.org/10.5281/zenodo.18318098)

### SGBV-UPR

- Vollmer, SC and Vollmer, DT. (2022). *Global perspectives of Africa: Harnessing the universal periodic review to process sexual and gender-based violence in SADC member states.* Stellenbosch Law Review, 33(1), 8–41. [DOI: 10.47348/SLR/2022/i1a1](https://doi.org/10.47348/SLR/2022/i1a1)

## Get Involved

<div class="grid cards" markdown>

-   :material-download:{ .lg .middle } __Use the Data__

    ---

    Access datasets via REST API or direct downloads

    [:octicons-arrow-right-24: API Quick Start](../../api/quickstart.md)

-   :material-code-tags:{ .lg .middle } __Run the Pipeline__

    ---

    Install and run the analysis yourself

    [:octicons-arrow-right-24: Installation Guide](../getting-started/installation.md)

-   :material-bug:{ .lg .middle } __Report Issues__

    ---

    Found data quality issues? Let us know

    [:octicons-arrow-right-24: Open Issue](https://github.com/MissCrispenCakes/DigitalChild/issues)

-   :material-hands-pray:{ .lg .middle } __Contribute__

    ---

    Code, documentation, or data contributions welcome

    [:octicons-arrow-right-24: Contributing Guide](../../CONTRIBUTING.md)

</div>

______________________________________________________________________

**Making human rights data accessible, transparent, and actionable.**
