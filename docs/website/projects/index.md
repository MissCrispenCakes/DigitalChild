# GRIMdata Research Projects

[:octicons-home-24: Back to GRIMdata Home](../../index.md){ .md-button }

**Established human-rights research and upcoming environmental oversight and research-continuity tracks**

______________________________________________________________________

## Active & Upcoming Projects

<div class="grid cards grim-projects" markdown>

-   :material-chart-timeline-variant:{ .lg .middle } __LittleRainbowRights__

    ---

    **Status:** Active | **Scope:** Global (194 countries)

    Child and LGBTQ+ digital rights research tracking 10 indicators across all countries. Includes a self-hosted API with 14 endpoints, a scorecard, and source-linked country assessments.

    **Key Features:**

    - 10 digital rights indicators
    - 194 countries tracked
    - Source-linked assessments
    - 14 REST API endpoints
    - Open-source Python pipeline

    **Published:** [DOI: 10.5281/zenodo.18318098](https://doi.org/10.5281/zenodo.18318098)

    [:octicons-arrow-right-24: Explore Project](littlerainbowrights/index.md){ .md-button .md-button--primary }
    [:octicons-database-24: View Scorecard](../../scorecard/index.md){ .md-button }

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

-   :material-leaf:{ .lg .middle } __Canadian Projects & Environmental Oversight__

    ---

    **Status:** Coming soon | **Scope:** Canada first

    A planned public-interest tracker for Build Canada and other major Canadian projects: environmental oversight, Indigenous rights and land relationships, climate commitments, affordability claims, and changes over time.

    Supporting needed housing, renewable energy, and infrastructure through transparent evidence about what is being built, how decisions are made, and who carries the long-term costs.

    [Read the upcoming plan](index.md#canadian-projects-environmental-oversight){ .md-button }

-   :material-source-branch:{ .lg .middle } __Research Provenance & Institutional Continuity__

    ---

    **Status:** Proposed future research | **Scope:** Research across institutions and time

    A planned extension of GRIMdata to trace research across grants, institutions, people, methods, and outputs. AI-assisted analysis with human verification will examine contribution histories, attribution, trainee transitions, and what enables research to continue when people or funding move on.

    **Insight Grant track:** AI-Assisted Research Provenance, Institutional Continuation & Public Accountability. Funding is not confirmed.

    [Read the future research plan](index.md#research-provenance-institutional-continuity){ .md-button }

</div>

______________________________________________________________________


## Canadian Projects & Environmental Oversight

**Coming soon · Canada first**

This planned GRIMdata stream will track Build Canada projects and other major Canadian developments alongside the rules, evidence, and decisions shaping them. The aim is to support needed housing, renewable energy, and infrastructure while making ecological consequences, Indigenous rights, and public accountability visible.

The planned work brings together:

- **Project histories:** announcements, stated objectives, approval stages, public commitments, and subsequent changes.
- **Environmental oversight:** assessment requirements, oversight mechanisms, regulatory changes, and evidence of implementation.
- **Indigenous rights and land relationships:** documented consultation, consent-related commitments, and affected lands, with careful source attribution.
- **Climate and affordability claims:** what proponents promise, what evidence supports those claims, and which costs or risks may be deferred.
- **Change over time:** historical baselines, source-linked timelines, maps, and comparisons rather than isolated announcements.

The planned outputs are an open, reproducible research workflow, documented sources, and public visualizations. The tracker and methods are in development.

## Research Provenance & Institutional Continuity

**Proposed future research · Insight Grant track · Funding not confirmed**

**AI-Assisted Research Provenance, Institutional Continuation & Public Accountability** is a proposed research direction extending GRIMdata's existing open-source document-analysis framework.

The project will investigate how research trajectories develop across grants, institutions, people, methods, outputs, and time—and what happens to contributions and knowledge when researchers, trainees, or funding leave an institution.

Planned computational, qualitative, and comparative work will examine contribution provenance, attribution, handoffs, re-engagement, and onboarding and offboarding. AI will assist classification, entity resolution, and event identification, with human verification of research evidence.

Drawing on **Viability.^.**, developed through doctoral research, this track will consider how unequal institutional power and continuity practices affect the futures available to research and its contributors.

Planned outputs include a validated methodology, an open-source workflow, research-continuity guidance, and practical approaches to handoff and public accountability.

## Research Evolution

**SGBV-UPR** (2019-2022) validated the core methodology for automated human rights document analysis at regional scale, focusing on SADC member states and SGBV themes. This foundational work was published in peer-reviewed literature.

**LittleRainbowRights** (2025-present) expands this approach to global digital rights analysis, tracking 10 indicators across 194 countries with comprehensive testing, self-hosted API tooling, and reproducible workflows.

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
