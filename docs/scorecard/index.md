# Digital Rights Scorecard

**Tracking 10 key indicators across 194 countries to assess digital rights protections for vulnerable populations**

---

## What is the Scorecard?

The Digital Rights Scorecard is a comprehensive research tool that tracks **10 critical indicators** of digital rights protections across **194 countries worldwide**. It focuses specifically on the intersection of digital technology governance and the rights of vulnerable populations, particularly **LGBTQ+ individuals** and **children**.

Each country receives scores on a 0-1-2 scale for each indicator, enabling comparative analysis of digital rights frameworks globally.

---

## Why It Exists

As digital technologies—especially artificial intelligence, biometric systems, and data-driven platforms—become increasingly embedded in daily life, their impact on vulnerable communities requires systematic monitoring.

**The gap this addresses:**
- Existing digital rights indices focus on general privacy or internet freedom
- Few track LGBTQ+-specific or child-specific digital protections
- This scorecard brings child and LGBTQ+ rights into the same comparative framework for examining digital governance

**Research foundation:**
This scorecard was developed for the research paper *"Queer AI for the digital child: Examining the response to advanced digital technologies on the human rights of LGBTQ+ children in Africa"* presented at the 2nd International Conference on Children's Rights (Stellenbosch, September 2025).

---

## Quick Stats

<div class="grid cards" markdown>

-   :fontawesome-solid-earth-americas:{ .lg .middle } **194 Countries**

    ---

    Country assessments spanning the published scorecard

-   :material-chart-line:{ .lg .middle } **10 Indicators**

    ---

    AI Policy, Data Protection, LGBTQ+ Status, Child Protection, and more

-   :material-link:{ .lg .middle } **2,581 Source Links**

    ---

    Links exported from the canonical workbook; inspect each country’s evidence

-   :material-update:{ .lg .middle } **26 June 2026**

    ---

    Visualization snapshot generated; source-verification stamp 9 September 2025

</div>

---

## What It Tracks

### The 10 Indicators

1. **Data Protection Law** - Existence of comprehensive data protection legislation
2. **DPA Independence** - Independence of Data Protection Authority from executive control
3. **Children's Data Safeguards** - Binding child-specific privacy/data-protection safeguards
4. **Child Online Protection Strategy** - National framework addressing online harms to children
5. **SOGI Sensitive Data** - Legal recognition of sexual orientation/gender identity as sensitive data
6. **LGBTQ+ Legal Status** - Legal recognition and protection of LGBTQ+ individuals
7. **LGBTQ+ Promotion/Propaganda Offences** - Laws restricting LGBTQ+ expression or advocacy
8. **AI Policy Status** - National AI strategy or framework adoption
9. **DPIA Required for High-Risk AI** - Requirement for Data Protection Impact Assessments for AI
10. **SIM Card Biometric ID Linkage** - Biometric data requirements for SIM card registration

### Scoring System

**0-1-2 Scale per indicator:**
- **2 (Best)** - Comprehensive protections or safeguards in place
- **1 (Middle)** - Partial protections or mixed implementation
- **0 (Worst)** - No protections, harmful policies, or heightened risk

**Composite Metrics:**
- **Protection Score:** Sum of all 10 indicators (0-20 scale)
- **Risk Index:** 100 − (Protection Score / 20 × 100) [inverted scale]
- **Data Completeness:** Percentage of indicators with written justifications in the published visualization snapshot

---

## Explore the Scorecard

Choose your path based on your needs:

<div class="grid cards" markdown>

-   :material-book-open-variant:{ .lg .middle } **Design & Methodology**

    ---

    Understand how the scorecard was designed

    - Detailed indicator definitions
    - Scoring methodology
    - Data sources and validation
    - Limitations and caveats

    [Learn About Design →](design.md)

-   :material-api:{ .lg .middle } **Data Access (API)**

    ---

    Access scorecard data programmatically

    - REST API endpoints
    - CSV exports
    - Python examples
    - Direct file access

    [Access the Data →](data-access.md)

-   :material-chart-bar:{ .lg .middle } **Visualization**

    ---

    Explore visualizations and export options

    - Live: Interactive choropleth map, indicator & regional charts, country cards
    - Also: CSV exports, API queries

    [View Visualizations →](visualization.md)

-   :material-table-search:{ .lg .middle } **Data Explorer**

    ---

    Interactive data exploration tool

    - Live: Filter, search, sort, compare countries
    - Also: API or CSV exports

    [Try Explorer →](explorer.md)

</div>

---

## Use Cases

### Research Applications

**Comparative Analysis:**
Compare digital rights frameworks across regions to identify patterns and gaps

**Risk Assessment:**
Evaluate digital safety environments for vulnerable populations by country

**Policy Tracking:**
Monitor changes in digital governance policies over time

**Advocacy Evidence:**
Provide data-backed evidence for human rights advocacy

### Example Research Questions

- Which countries have comprehensive child data protections but criminalize LGBTQ+ identities?
- How does biometric SIM registration correlate with LGBTQ+ legal status?
- Which African countries have adopted AI strategies with data protection frameworks?
- Where are LGBTQ+ children most at risk from digital surveillance?

---

## Data Quality & Sources

### Authoritative Sources

Sources include national laws and policy documents as well as international organizations and rights groups:

- **UNESCO** - AI Policy Observatory
- **UNCTAD** - Data Protection and Privacy Legislation Database
- **ILGA World** - State-Sponsored Homophobia report (LGBTQ+ legal status)
- **UNICEF** - Child protection measures and COP strategies
- **ITU** - Telecom and internet regulations
- **Privacy International** - Surveillance and biometric tracking
- **Human Rights Watch** - Human rights monitoring

### Validation & Monitoring

**Quality Assurance:**
- URL checks record HTTP status, redirects and broken links
- Change detection compares source content between runs
- Country assessments bring together source evidence and interpretation

**Transparency:**
- Country panels display source links and written assessments where available
- Local URL-check outputs are documented in the [Scorecard Workflow](../guides/SCORECARD_WORKFLOW.md#4-validate-source-urls)
- Full methodology documented in [Design & Methodology](design.md)

---

## Quick Start Examples

### API Access

Query the scorecard via the REST API — copy-paste examples (per-country, region filters, and
indicator statistics) live in the **[API Quick Start](../api/quickstart.md)**.

<span id="__span-0-8"></span>
<span id="__codelineno-0-8"></span>
<span id="__span-0-9"></span>
<span id="__codelineno-0-9"></span>
<span id="__span-0-10"></span>
<span id="__codelineno-0-10"></span>
<span id="__span-0-11"></span>
<span id="__codelineno-0-11"></span>
<span id="__span-0-12"></span>
<span id="__codelineno-0-12"></span>
<span id="__span-0-13"></span>
<span id="__codelineno-0-13"></span>
<span id="__span-0-14"></span>
<span id="__codelineno-0-14"></span>
<span id="__span-0-15"></span>
<span id="__codelineno-0-15"></span>
<span id="__span-0-16"></span>
<span id="__codelineno-0-16"></span>

### Python Analysis

Use the [snapshot query example](data-access.md#find-countries-with-specific-indicators) for scored indicator combinations, or the [API examples](data-access.md#python-examples) for local country values and sources.

<span id="__span-1-1"></span>
<span id="__codelineno-1-1"></span>
<span id="__span-1-2"></span>
<span id="__codelineno-1-2"></span>
<span id="__span-1-3"></span>
<span id="__codelineno-1-3"></span>
<span id="__span-1-4"></span>
<span id="__codelineno-1-4"></span>
<span id="__span-1-5"></span>
<span id="__codelineno-1-5"></span>
<span id="__span-1-6"></span>
<span id="__codelineno-1-6"></span>
<span id="__span-1-7"></span>
<span id="__codelineno-1-7"></span>
<span id="__span-1-8"></span>
<span id="__codelineno-1-8"></span>

### CSV Export

```bash
# Export scorecard data
python pipeline_runner.py --mode scorecard --scorecard-action export

# Generates:
# - data/exports/scorecard_summary.csv (countries × indicators)
# - data/exports/scorecard_sources.csv (all source URLs)
# - data/exports/scorecard_indicator_counts.csv (status distributions)
```

---

<span id="__span-2-1"></span>
<span id="__codelineno-2-1"></span>
<span id="__span-2-2"></span>
<span id="__codelineno-2-2"></span>
<span id="__span-2-3"></span>
<span id="__codelineno-2-3"></span>
<span id="__span-2-4"></span>
<span id="__codelineno-2-4"></span>
<span id="__span-2-5"></span>
<span id="__codelineno-2-5"></span>
<span id="__span-2-6"></span>
<span id="__codelineno-2-6"></span>
<span id="__span-2-7"></span>
<span id="__codelineno-2-7"></span>
<span id="__span-2-8"></span>
<span id="__codelineno-2-8"></span>

## Citation

For the published scorecard, cite *LittleRainbowRights Scorecard*, snapshot generated **26 June 2026**, your access date and the source-linked assessments used. [Project citation guidance](../website/projects/littlerainbowrights/index.md#citing-this-work) distinguishes the research presentation, dataset and software.

The [DigitalChild release DOI](https://doi.org/10.5281/zenodo.20950631) identifies software. Project-authored scorecard data uses CC BY 4.0 where specified; third-party sources retain their own terms.



## Reading the assessments {#limitations-disclaimers}

The scorecard compares documented laws and policy frameworks using a three-point scale. Read the country assessments alongside their original sources, with attention to:

- **Dates:** the snapshot was generated on 26 June 2026; the source-verification stamp is 9 September 2025.
- **Coverage:** written justifications and accessible sources vary across countries and indicators.
- **Context:** enforcement, local experience and differences within federal systems add detail beyond a national comparison.
- **Relationships:** indicators such as criminalization and biometric identification may interact in ways that merit closer study.

[Design & Methodology](design.md) explains the scoring rules and analytical scope. Include the snapshot date and relevant sources when citing an assessment.

---

## Future Enhancements

Planned features (see [Roadmap](../ROADMAP.md)):

- [x] **REST API software for self-hosted programmatic access** — implementation available; separate from the public static website
- [x] **Interactive map & charts (Plotly.js)** ✅ **LIVE** (see [Visualization](visualization.md))
- [x] **Country comparison tool** ✅ **LIVE** (radar comparison in the [Data Explorer](explorer.md))
- [x] **Source transparency monitoring** ✅ **LIVE** (see [Transparency Watch](../transparency-watch/index.md))
- [ ] Time-series tracking of policy changes
- [ ] Real-time source monitoring alerts
- [ ] Expanded indicators (target: 15-20 total)
- [ ] Sub-national data (states/provinces for federal systems)
- [ ] Integration with other digital rights indices

---

## Assessment records {#contributing}

Source-linked assessments and published versions should retain dates, interpretation and limitations. [Data Governance](../DATA_GOVERNANCE.md) describes these responsibilities.

---

## Technical Documentation

For developers and researchers working with the scorecard system:

- [Scorecard Workflow Guide](../guides/SCORECARD_WORKFLOW.md) - Complete system overview
- [Metadata Schema](../standards/METADATA_SCHEMA.md) - Data structure
- [Architecture](../ARCHITECTURE.md) - System design
- [API Documentation](../api/index.md) - Programmatic access

---

## Interpretation and guidance {#support-feedback}

[Scorecard methods](design.md) · [Documentation](../docs/index.md) · [Data Governance](../DATA_GOVERNANCE.md) · [FAQ](../FAQ.md)

---

## License

- **Scorecard Data:** CC BY 4.0
- **Code & Pipeline:** MIT License

See [LICENSE-DATA](https://github.com/MissCrispenCakes/DigitalChild/blob/basecamp/LICENSE-DATA) and [LICENSE](https://github.com/MissCrispenCakes/DigitalChild/blob/basecamp/LICENSE) for details.
