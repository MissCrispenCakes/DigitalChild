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

### Via self-hosted REST API {#via-rest-api}

Get scorecard data programmatically via the REST API — the copy-paste examples (health
check, per-country, statistics, filtering) live in the API Quick Start:

[:octicons-rocket-24: API Quick Start](../api/quickstart.md){ .md-button .md-button--primary }
[:octicons-book-24: Full API Docs](../api/reference.md){ .md-button }

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
page — the single source of truth, so the numbers here and the definitions there can't drift apart.

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

**Formula:** (Number of known indicators / 10) × 100

- **Maximum:** 100% (all 10 indicators have data)
- **Minimum:** 0% (no indicator data available)
- **Interpretation:** Percentage of metrics with verified data for the country

Use the completeness measure to identify countries where more source research is needed before comparison.

## Exporting Data

### Via self-hosted REST API or CSV {#via-rest-api-or-csv}

Access scorecard data programmatically (REST API) or as CSV exports — every method, with
copy-paste examples in cURL / Python / R, is documented on the **[Data Access](data-access.md)** page.

### From the Pipeline

Run the scorecard export workflow:

```bash
python pipeline_runner.py --mode scorecard --scorecard-action export
```

This generates:

- `scorecard_summary.csv` - Countries × Indicators table
- `scorecard_sources.csv` - All source URLs with validation status
- `scorecard_by_indicator.csv` - Grouped by indicator
- `scorecard_by_region.csv` - Regional aggregations

### CSV Format

**scorecard_summary.csv:**

| Country      | AI_Policy_Status | Data_Protection_Law | LGBTQ_Legal_Status | ... |
| ------------ | ---------------- | ------------------- | ------------------ | --- |
| Kenya        | Framework        | Comprehensive Law   | No Protections     | ... |
| South Africa | Strategy         | Comprehensive Law   | Some Protections   | ... |

**scorecard_sources.csv:**

| Country | Indicator | Value     | Source_URL  | Validated | Last_Checked |
| ------- | --------- | --------- | ----------- | --------- | ------------ |
| Kenya   | AI_Policy | Framework | https://... | ✅        | 2026-01-15   |

## Data Explorer

Want to filter by region or indicator, search for a country, sort the full table, or compare countries side-by-side?

[:octicons-search-24: Open the Data Explorer](explorer.md){ .md-button .md-button--primary }

## Validation & Quality

### URL Validation

All 2,543 source URLs are automatically validated:

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
- Policy updates
- Broken links
- New data available

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

When using scorecard data in publications:

<div class="language-bibtex highlight"><pre><span></span><code><span id="__span-4-1"><a href="#__codelineno-4-1" id="__codelineno-4-1" name="__codelineno-4-1"></a><span class="nc">@misc</span><span class="p">{</span><span class="nl">littlerainbowrights2025scorecard</span><span class="p">,</span>
</span><span id="__span-4-2"><a href="#__codelineno-4-2" id="__codelineno-4-2" name="__codelineno-4-2"></a><span class="w">  </span><span class="na">title</span><span class="w"> </span><span class="p">=</span><span class="w"> </span><span class="s">{LittleRainbowRights Scorecard: Child and LGBTQ+ Digital Rights Indicators}</span><span class="p">,</span>
</span><span id="__span-4-3"><a href="#__codelineno-4-3" id="__codelineno-4-3" name="__codelineno-4-3"></a><span class="w">  </span><span class="na">author</span><span class="w"> </span><span class="p">=</span><span class="w"> </span><span class="s">{Vollmer, D.T. and Vollmer, S.C.}</span><span class="p">,</span>
</span><span id="__span-4-4"><a href="#__codelineno-4-4" id="__codelineno-4-4" name="__codelineno-4-4"></a><span class="w">  </span><span class="na">year</span><span class="w"> </span><span class="p">=</span><span class="w"> </span><span class="s">{2025}</span><span class="p">,</span>
</span><span id="__span-4-5"><a href="#__codelineno-4-5" id="__codelineno-4-5" name="__codelineno-4-5"></a><span class="w">  </span><span class="na">doi</span><span class="w"> </span><span class="p">=</span><span class="w"> </span><span class="s">{10.5281/zenodo.18318098}</span><span class="p">,</span>
</span><span id="__span-4-6"><a href="#__codelineno-4-6" id="__codelineno-4-6" name="__codelineno-4-6"></a><span class="w">  </span><span class="na">howpublished</span><span class="w"> </span><span class="p">=</span><span class="w"> </span><span class="s">{\url{https://grimdata.org/scorecard/}}</span><span class="p">,</span>
</span><span id="__span-4-7"><a href="#__codelineno-4-7" id="__codelineno-4-7" name="__codelineno-4-7"></a><span class="w">  </span><span class="na">note</span><span class="w"> </span><span class="p">=</span><span class="w"> </span><span class="s">{Licensed under CC BY 4.0. ORCID: 0000-0002-5035-3395 (D.T. Vollmer), 0000-0002-3359-2810 (S.C. Vollmer)}</span>
</span><span id="__span-4-8"><a href="#__codelineno-4-8" id="__codelineno-4-8" name="__codelineno-4-8"></a><span class="p">}</span>
</span></code></pre></div>

Or:

> Vollmer, D.T., & Vollmer, S.C. (2025). *LittleRainbowRights Scorecard: Child and LGBTQ+ Digital Rights Indicators*.
> DOI: 10.5281/zenodo.18318098. Available at: https://grimdata.org/scorecard/.
> Licensed under CC BY 4.0.
> ORCID: [0000-0002-5035-3395](https://orcid.org/0000-0002-5035-3395) (D.T. Vollmer), [0000-0002-3359-2810](https://orcid.org/0000-0002-3359-2810) (S.C. Vollmer)

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
- [x] **API for programmatic access** ✅ **COMPLETE** (14 endpoints implemented for self-hosting, see [API docs](../api/index.md))
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
