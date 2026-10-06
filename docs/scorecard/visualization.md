# Scorecard Visualization

Interactive visualization of human rights indicators across 194 countries.

## Quick Overview

<div class="grid cards" markdown>

-   :fontawesome-solid-earth-americas:{ .lg .middle } **194 Countries**

    ---

    Countries represented in the published research snapshot

-   :material-chart-line:{ .lg .middle } **10 Indicators**

    ---

    AI Policy, Data Protection, LGBTQ+ Status, Child Protection, and more

-   :material-link:{ .lg .middle } **132 Fully Documented**

    ---

    Countries with written justifications for all ten scored indicators

-   :material-update:{ .lg .middle } **26 June 2026**

    ---

    Snapshot generated; source-verification stamp: 9 September 2025

</div>

## Accessing Data

<span id="via-rest-api"></span>

### Interactive Visualizations

Explore the scorecard interactively below. Charts are rendered in your browser from a published static dataset — no server required. To filter, search, sort, and compare individual countries, use the [Data Explorer](explorer.md).

<div id="sc-chart-permission" class="sc-chart-permission">
  <p><strong>Optional interactive charts</strong> load Plotly and map assets from <code>cdn.plot.ly</code>. Your browser sends that service a request, including your IP address. Table filters stay in your browser. This choice applies to this page only.</p>
  <button type="button" id="sc-load-charts" class="md-button md-button--primary">Load interactive charts</button>
  <a href="../../practices/">Data handling details</a>
  <p id="sc-chart-status" role="status" aria-live="polite">Charts are off. Use the country table or downloads without them.</p>
</div>

[Use the country table instead](explorer.md){ .md-button }
[Download the published snapshot](data-access.md#published-snapshot-downloads){ .md-button }

<div class="sc-viz">
  <p id="sc-meta" class="sc-meta"></p>
  <div id="sc-loading" class="sc-loading">Loading scorecard data…</div>

  <div class="sc-controls">
    <label for="sc-map-metric">Map metric:</label>
    <select id="sc-map-metric">
      <option value="protection_score">Protection Score (0–20, higher = stronger)</option>
      <option value="risk_index">Risk Index (0–100, higher = greater risk)</option>
      <option value="documented">Data completeness (documented indicators, 0–10)</option>
    </select>
  </div>
  <div id="sc-map" class="sc-chart"></div>
  <p class="sc-hint">Click a country on the map for its full indicator breakdown and sources.</p>
  <div id="sc-detail" class="sc-detail"></div>

  <div id="sc-indicators" class="sc-chart"></div>

  <div id="sc-regions" class="sc-chart"></div>
</div>

!!! note "About this data"
    Visualizations are generated from the project's designated visualization dataset and are **point-in-time**. Source-URL verification is an ongoing, separate workflow, so figures may be revised. The canonical pipeline data lives in `scorecard_main.xlsx`. See [Data Access](data-access.md) for the API and CSV exports.

## Indicators Tracked

!!! info "Scoring System"
    Each indicator uses a 0-1-2 scale where higher scores indicate stronger protections:

    - **2 (Best)** - Comprehensive protections or safeguards in place
    - **1 (Middle)** - Partial protections or mixed implementation
    - **0 (Worst)** - No protections, harmful policies, or heightened risk

    Risk analysis examines **combinations** of indicators (e.g., LGBTQ criminalization × biometric ID linkage).

The scorecard tracks **10 indicators** spanning data protection, child online safety, LGBTQ+
rights, AI policy, and digital identification. The full definition, sources, and per-category
(0/1/2) rubric for every indicator live on the **[Scorecard Design & Methodology](design.md#the-10-indicators)**
page.

## Composite Scores

In addition to the 10 individual indicators, the scorecard calculates composite metrics:

### Protection Score

**Formula:** Sum of all 10 indicator scores (0–20 scale)

- **Maximum:** 20 (all indicators score 2)
- **Minimum:** 0 (all indicators score 0)
- **Interpretation:** Higher scores indicate stronger digital rights protections

**Example:** Country with 7 indicators at (2), 2 at (1), 1 at (0) = 14 + 2 + 0 = 16 Protection Score

### Risk Index

**Formula:** 100 − (Protection_Score / 20 × 100)

- **Maximum:** 100 (no protections, highest risk)
- **Minimum:** 0 (full protections, lowest risk)
- **Interpretation:** Inverted scale where higher values indicate greater risk

**Example:** Protection Score of 16 → Risk Index = 100 − (16/20 × 100) = 100 − 80 = 20

### Data Completeness

**Formula:** (Indicators with written justifications / 10) × 100

- **Maximum:** 100% (all 10 indicators have data)
- **Minimum:** 0% (no indicator data available)
- **Interpretation:** Percentage of indicators with written justifications in the published visualization snapshot

Use the completeness measure to identify countries where more source research is needed before comparison.

## Exporting Data

### Via self-hosted REST API or CSV {#via-rest-api-or-csv}

Start your own instance using the [API Quick Start](../api/quickstart.md). The API queries local pipeline inputs; the downloadable browser snapshot is a separate scored output.

Access scorecard data programmatically (REST API) or as CSV exports — every method, with
copy-paste examples in cURL / Python / R, is documented on the **[Data Access](data-access.md)** page.

### From the Pipeline

Run the scorecard export workflow:

```bash
python pipeline_runner.py --mode scorecard --scorecard-action export
```

The standard export generates `scorecard_summary.csv`, `scorecard_sources.csv` and `scorecard_indicator_counts.csv`. Regional and individual-indicator exports are [separate operations](data-access.md#generated-files).

### CSV Format

**scorecard_summary.csv:**

| Country      | AI_Policy_Status | Data_Protection_Law | LGBTQ_Legal_Status | ... |
| ------------ | ---------------- | ------------------- | ------------------ | --- |
| Kenya        | Framework        | Comprehensive Law   | No Protections     | ... |
| South Africa | Strategy         | Comprehensive Law   | Some Protections   | ... |

**scorecard_sources.csv:**

| country | indicator | url |
| --- | --- | --- |
| Kenya | AI_Policy_Status | Source URL extracted from the workbook |

## Data Explorer

Want to filter by region or indicator, search for a country, sort the full table, or compare countries side-by-side?

[:octicons-search-24: Open the Data Explorer](explorer.md){ .md-button .md-button--primary }

## Validation & Quality

### URL Validation

Run URL checks on the pipeline source register:

```bash
python pipeline_runner.py --mode scorecard --scorecard-action validate
```

Generates `validation_report.csv` with:

- HTTP status codes
- Redirect chains
- Broken links
- Response times

### Change Detection

Monitor sources for updates:

```bash
python processors/scorecard_diff.py
```

Detects:

- Content changes (via hashing)
- Page changes requiring policy review
- Broken links
- Changed access or content requiring review

### Data Quality

**Authoritative Sources:**

- UNESCO - AI policies and digital education
- UNCTAD - Data protection legislation
- ILGA World - LGBTQ+ legal status
- UNICEF - Child protection measures
- ITU - Telecom regulations
- Privacy International - Surveillance measures

**Updating assessments:**

Source checks and content comparisons identify material for review. Changes to an assessment are recorded with the supporting source and date.

<span id="__span-3-1"></span>
<span id="__codelineno-3-1"></span>
<span id="__span-3-2"></span>
<span id="__codelineno-3-2"></span>
<span id="__span-3-3"></span>
<span id="__codelineno-3-3"></span>
<span id="__span-3-4"></span>
<span id="__codelineno-3-4"></span>

## Updating an assessment {#contributing-data}

Record the country, indicator, existing value, proposed correction and source. After reviewing the evidence, update the workbook and regenerate the exports using the [Scorecard Workflow](../guides/SCORECARD_WORKFLOW.md).

[Data Governance](../DATA_GOVERNANCE.md) explains how sources and revisions are recorded.

## Citing Scorecard Data

Identify *LittleRainbowRights Scorecard*, the snapshot generation date (**26 June 2026**), your access date and the particular assessments used. Record the **9 September 2025** source-verification stamp when discussing evidence freshness. Link to the [published downloads](data-access.md#published-snapshot-downloads) and relevant original sources.

Cite [DigitalChild v2.1.0](https://doi.org/10.5281/zenodo.20950631) separately for the software.

<span id="__span-4-1"></span>
<span id="__codelineno-4-1"></span>
<span id="__span-4-2"></span>
<span id="__codelineno-4-2"></span>
<span id="__span-4-3"></span>
<span id="__codelineno-4-3"></span>
<span id="__span-4-4"></span>
<span id="__codelineno-4-4"></span>
<span id="__span-4-5"></span>
<span id="__codelineno-4-5"></span>
<span id="__span-4-6"></span>
<span id="__codelineno-4-6"></span>
<span id="__span-4-7"></span>
<span id="__codelineno-4-7"></span>
<span id="__span-4-8"></span>
<span id="__codelineno-4-8"></span>
<span id="__span-5-1"></span>
<span id="__codelineno-5-1"></span>
<span id="__span-5-2"></span>
<span id="__codelineno-5-2"></span>
<span id="__span-5-3"></span>
<span id="__codelineno-5-3"></span>
<span id="__span-5-4"></span>
<span id="__codelineno-5-4"></span>

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

- [x] **Interactive choropleth map, indicator & regional charts** ✅ **LIVE** (Plotly.js, this page)
- [x] **Country comparison tool** ✅ **LIVE** (radar comparison in the [Data Explorer](explorer.md))
- [ ] Time-series tracking of policy changes
- [x] **API for programmatic access** ✅ **COMPLETE** (12 endpoints implemented for self-hosting, see [API docs](../api/index.md))
- [ ] Real-time source monitoring alerts
- [ ] Expanded indicators (15-20 total)
- [ ] Sub-national data (states/provinces)

## Technical Details

For technical documentation:

- [Scorecard Workflow Guide](../guides/SCORECARD_WORKFLOW.md) - Complete system overview
- [Metadata Schema](../standards/METADATA_SCHEMA.md) - Data structure
- [Architecture](../ARCHITECTURE.md) - System design

## Further guidance {#support-feedback}

[Methodology](design.md) · [Data access](data-access.md) · [FAQ](../FAQ.md)

______________________________________________________________________

Software development is recorded in the [repository](https://github.com/MissCrispenCakes/DigitalChild) and [roadmap](../ROADMAP.md).
