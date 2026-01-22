# GRIMdata

## Global Rights Index Monitoring

**GRIMdata** is an open research initiative analyzing human rights through automated document analysis pipelines. We develop tools to track digital rights, protections for vulnerable populations, and policy implementation across countries.

**Mission:** Support evidence-based human rights research and advocacy through transparent, reproducible data analysis.

!!! quote "Research Foundation"
    "During periods of political and economic instability, some of the first rights to be infringed are specifically those which allow for women, LGBTQ+ members, and often specifically trans individuals, to assert their independence and retain self-autonomy and respect."

    — Vollmer & Vollmer (2022), *Stellenbosch Law Review* [DOI: 10.47348/SLR/2022/i1a1](https://doi.org/10.47348/SLR/2022/i1a1)

**GRIMdata's response:** Decisions affecting marginalized populations' fundamental rights are being made RIGHT NOW with PERMANENT consequences—often by the wrong actors, based on assumptions rather than evidence. Both research tracks (SGBV-UPR for violence documentation, LittleRainbowRights for digital system deployments) use transparent tracking to replace assumptions with evidence BEFORE consequences become irreversible.

**Core principle:** Evidence-based governance, not governance by assumption.

[:octicons-book-16: Read Full Research Context](RESEARCH_CONTEXT.md){ .md-button }

______________________________________________________________________

## Current Projects

<div class="grid cards" markdown>

- :rainbow:{ .lg .middle } __LittleRainbowRights__

  **Status:** Active | **Scope:** Global (194 countries)

  Child and LGBTQ+ digital rights research tracking 10 indicators: AI policy, data protection, LGBTQ+ legal status, child online protection, and more. Features open-source pipeline, validated data sources, and comprehensive scorecard.

  **Presented:** 2nd International Conference on Children's Rights (Stellenbosch, September 2025)

  **Published:** [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18318099.svg)](https://doi.org/10.5281/zenodo.18318099) Vollmer & Vollmer (2026), Zenodo

  **Repository:** [DigitalChild](https://github.com/MissCrispenCakes/DigitalChild) (Python pipeline)

  [:octicons-arrow-right-24: Full Documentation](projects/littlerainbowrights/index.md){ .md-button .md-button--primary }

- :material-hand-heart:{ .lg .middle } __SGBV-UPR__

  **Status:** Published (2022) | **Scope:** SADC member states → Expanding globally

  Sexual and gender-based violence analysis using Universal Periodic Review recommendations. Precursor research demonstrating methodology at regional scale. Updating for UPR Cycle 4 and global expansion.

  **Presented:** International Conference on The Responsiveness of the African Human Rights System to SGBV (September 2021, Session: Diverse Gender Identities)

  **Published:** [Vollmer & Vollmer (2022), Stellenbosch Law Review](https://doi.org/10.47348/SLR/2022/i1a1)

  **Repository:** Under reconstruction (see project page for details)

  [:octicons-arrow-right-24: Project Overview](projects/sgbv/index.md){ .md-button }

</div>

## Research Evolution

**SGBV-UPR** (2019-2022) demonstrated the feasibility of automated analysis of UPR recommendations at regional scale, focusing on SADC member states and SGBV themes. This work was published in academic literature and validated the core methodology.

**LittleRainbowRights** (2025-present) expands this approach to global digital rights analysis, tracking 10 indicators across all 194 countries with 2,543 validated sources. The project advances the pipeline with comprehensive testing, security frameworks, and reproducible workflows.

## What GRIMdata Provides

<div class="grid cards" markdown>

- :material-database:{ .lg .middle } __Open Data__

  All datasets include authoritative source URLs, validation status, and transparent provenance. Data licensed under CC BY 4.0 for academic and advocacy use.

- :material-code-tags:{ .lg .middle } __Open Source Code__

  Complete pipelines available on GitHub with MIT licensing. Modular design enables adaptation for other human rights research projects.

- :material-book-open-variant:{ .lg .middle } __Documentation__

  Comprehensive guides covering installation, usage, methodology, and standards. Full architectural documentation for researchers and developers.

- :material-shield-check:{ .lg .middle } __Research Quality__

  Security testing, input validation, automated source monitoring, and version control ensure data integrity and reproducibility.

</div>

## Technology Stack

- **Python 3.12** - Core language
- **BeautifulSoup4 & Selenium** - Web scraping
- **pandas** - Data analysis
- **pytest** - Testing framework (124+ tests)
- **MkDocs Material** - Documentation

All pipelines follow best practices for security, validation, and error handling.

## Getting Started with LittleRainbowRights

The **LittleRainbowRights** project is ready for use:

1. **[Install the pipeline](getting-started/installation.md)** - Setup in ~5 minutes
1. **[Quick start guide](getting-started/quickstart.md)** - Run your first analysis
1. **[Explore the scorecard](scorecard/index.md)** - Browse 194-country dataset
1. **[Read the documentation](projects/littlerainbowrights/index.md)** - Complete project overview

[Get Started with LittleRainbowRights](projects/littlerainbowrights/index.md){ .md-button .md-button--primary }

## Use Cases

**For Researchers:**

- Systematic literature reviews of human rights policies
- Cross-country comparative analysis
- Longitudinal policy tracking
- Data-driven advocacy campaigns

**For NGOs & Advocates:**

- Evidence-based policy recommendations
- Monitor country compliance with commitments
- Identify gaps in protections
- Track implementation progress

**For Policy Makers:**

- Benchmark against peer countries
- Identify best practices
- Gap analysis for policy development
- Regional cooperation insights

## Publications & Outputs

**SGBV-UPR Research:**

- Vollmer, SC and Vollmer, DT. (2022). Global perspectives of Africa: Harnessing the universal periodic review to process sexual and gender-based violence in SADC member states. *Stellenbosch Law Review*, 33(1), 8–41. [DOI: 10.47348/SLR/2022/i1a1](https://doi.org/10.47348/SLR/2022/i1a1)

**LittleRainbowRights Research:**

- Vollmer, DT and Vollmer, SC. (2025). Queer AI for the digital child: Examining the response to advanced digital technologies on the human rights of LGBTQ+ children in Africa. Presented at the Second International Conference on Children's Rights, Stellenbosch, South Africa, September 9-11, 2025.

## Open Source & Licensing

**Code:** MIT License - Free for any use including commercial applications

**Data & Documentation:** CC BY 4.0 - Attribution required

This dual licensing ensures maximum utility while giving credit to the research effort.

## About the Initiative

GRIMdata is maintained by an independent researcher alongside other work. Both projects represent passion projects aimed at making human rights data more accessible and analysis more transparent.

!!! warning "Maintained by PhD Student"
This project is maintained part-time by one person alongside PhD research. Response times may vary. Your patience is appreciated!

## Contact & Contributing

- **GitHub (LittleRainbowRights):** [DigitalChild Repository](https://github.com/MissCrispenCakes/DigitalChild)
- **GitHub (SGBV-UPR):** Repository under reconstruction (see [SGBV project page](projects/sgbv/index.md))
- **Issues & Discussions:** Use [DigitalChild repository](https://github.com/MissCrispenCakes/DigitalChild/discussions)
- **Contributing:** See [Contributing Guidelines](CONTRIBUTING.md)

## Support This Work

- ⭐ Star the repositories on GitHub
- 📢 Share with researchers and advocates in your network
- 🐛 Report data quality issues or bugs
- 💻 Contribute code or documentation improvements
- 📝 Cite in your publications and presentations

______________________________________________________________________

**Making human rights data accessible, transparent, and actionable.**
