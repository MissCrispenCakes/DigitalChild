# Scorecard Visualization

Interactive visualization of human rights indicators across 194 countries.

## Quick Overview

<div class="grid cards" markdown>

-   :fontawesome-solid-earth-americas:{ .lg .middle } **194 Countries**

    ---

    Comprehensive global coverage across all UN member states and territories

-   :material-chart-line:{ .lg .middle } **10 Indicators**

    ---

    AI Policy, Data Protection, LGBTQ+ Status, Child Protection, and more

-   :material-link:{ .lg .middle } **2,543 Source URLs**

    ---

    Validated authoritative sources from UNESCO, UNCTAD, ILGA, UNICEF, etc.

-   :material-update:{ .lg .middle } **January 2026**

    ---

    Last updated with latest policy changes and new data

</div>

## Accessing Data

### Via REST API

Get scorecard data programmatically via the REST API — the copy-paste examples (health
check, per-country, statistics, filtering) live in the API Quick Start:

[:octicons-rocket-24: API Quick Start](../api/quickstart.md){ .md-button .md-button--primary }
[:octicons-book-24: Full API Docs](../api/reference.md){ .md-button }

### Interactive Visualizations

Explore the scorecard interactively below. Charts are rendered in your browser from a published static dataset — no server required. To filter, search, sort, and compare individual countries, use the [Data Explorer](explorer.md).

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

**Note:** Countries with low data completeness (<50%) should be interpreted cautiously as composite scores may not reflect full picture.

## Exporting Data

### Via REST API or CSV

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

**Update Frequency:**

- Manually reviewed quarterly
- Automated monitoring alerts when sources change
- Community contributions via GitHub issues

## Contributing Data

Found an error or have updated information?

1. **Verify** - Check the source URL in `scorecard_main.xlsx`
2. **Report** - Open [GitHub Issue](https://github.com/MissCrispenCakes/DigitalChild/issues) with:
    ```txt
    - Country name
    - Indicator
    - Current value vs. correct value
    - Authoritative source URL
    ```
3. **Update** - Maintainer reviews and updates
4. **Re-export** - Updated data regenerated

## Citing Scorecard Data

When using scorecard data in publications:

```bibtex
@misc{littlerainbowrights2025scorecard,
  title = {LittleRainbowRights Scorecard: Child and LGBTQ+ Digital Rights Indicators},
  author = {Vollmer, D.T. and Vollmer, S.C.},
  year = {2025},
  doi = {10.5281/zenodo.18318098},
  howpublished = {\url{https://grimdata.org/scorecard/}},
  note = {Licensed under CC BY 4.0. ORCID: 0000-0002-5035-3395 (D.T. Vollmer), 0000-0002-3359-2810 (S.C. Vollmer)}
}
```

Or:

> Vollmer, D.T., & Vollmer, S.C. (2025). *LittleRainbowRights Scorecard: Child and LGBTQ+ Digital Rights Indicators*.
> DOI: 10.5281/zenodo.18318098. Available at: https://grimdata.org/scorecard/.
> Licensed under CC BY 4.0.
> ORCID: [0000-0002-5035-3395](https://orcid.org/0000-0002-5035-3395) (D.T. Vollmer), [0000-0002-3359-2810](https://orcid.org/0000-0002-3359-2810) (S.C. Vollmer)

## Limitations & Disclaimers

!!! warning "Important Considerations"
    **Point-in-time data:** Reflects information as of January 2026
    **Binary categorization:** Complex policies simplified into discrete categories
    **Source availability:** Some countries lack accessible English-language sources
    **Implementation vs. policy:** Tracks official policy, not enforcement
    **Regional variation:** Federal systems may have state/provincial differences

!!! info "Use Responsibly"
    This scorecard is a research tool, not legal advice. Always:
    ```txt
    - Verify source URLs before citing
    - Consider local context and nuance
    - Acknowledge limitations in publications
    - Cross-reference with other datasets
    ```

## Future Enhancements

Planned features (see [Roadmap](../ROADMAP.md)):

- [x] **Interactive choropleth map, indicator & regional charts** ✅ **LIVE** (Plotly.js, this page)
- [x] **Country comparison tool** ✅ **LIVE** (radar comparison in the [Data Explorer](explorer.md))
- [ ] Time-series tracking of policy changes
- [x] **API for programmatic access** ✅ **COMPLETE** (14 endpoints live, production-ready, see [API docs](../api/index.md))
- [ ] Real-time source monitoring alerts
- [ ] Expanded indicators (15-20 total)
- [ ] Sub-national data (states/provinces)

## Technical Details

For technical documentation:

- [Scorecard Workflow Guide](../guides/SCORECARD_WORKFLOW.md) - Complete system overview
- [Metadata Schema](../standards/METADATA_SCHEMA.md) - Data structure
- [Architecture](../ARCHITECTURE.md) - System design

## Support & Feedback

- **Data quality issues:** [Open Issue](https://github.com/MissCrispenCakes/DigitalChild/issues)
- **Feature requests:** [Start Discussion](https://github.com/MissCrispenCakes/DigitalChild/discussions)
- **General questions:** [FAQ](../FAQ.md)

______________________________________________________________________

**Note:** Interactive visualizations are under active development. Check back for updates or [watch the repository](https://github.com/MissCrispenCakes/DigitalChild) for notifications.
