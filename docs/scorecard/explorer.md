# Data Explorer

Filter, search, sort, and compare the Digital Rights Scorecard across 194 countries — entirely in your browser, from a published static dataset (no server required).

<div class="sc-explorer" id="sc-explorer">
  <p id="sc-meta" class="sc-meta"></p>
  <div id="sc-loading" class="sc-loading">Loading scorecard data…</div>

  <div class="sc-controls sc-controls--grid">
    <label>Region
      <select id="sc-f-region"><option value="all">All regions</option></select>
    </label>
    <label>Indicator
      <select id="sc-f-indicator"><option value="all">All (use Protection Score)</option></select>
    </label>
    <label><span id="sc-f-minscore-label">Minimum Protection Score (0–20)</span>
      <input type="range" id="sc-f-minscore" min="0" max="20" step="1" value="0">
      <span id="sc-f-minscore-val">0</span>
    </label>
    <label>Search country
      <input type="search" id="sc-f-search" placeholder="e.g. Kenya">
    </label>
    <label class="sc-check">
      <input type="checkbox" id="sc-f-documented"> Only fully documented (10/10)
    </label>
    <button type="button" id="sc-f-reset" class="md-button">Reset</button>
  </div>

  <p id="sc-count" class="sc-count" role="status" aria-live="polite"></p>
  <div id="sc-table"></div>
  <div id="sc-detail" class="sc-detail"></div>
</div>

!!! info "Reading the table"
    Each indicator column (`AI`, `DP`, `ChildData`, …) shows the 0–2 score, colour-coded
    **2 = best / 1 = partial / 0 = worst** (see the indicator glossary below). **Prot.** is the Protection Score (0–20); **Risk** is the Risk Index (0–100). **Doc** is data completeness — how many of the 10 indicators carry a documented justification (rows below 10/10 are flagged). **Activate a country button** to open a country detail panel with each indicator's assessment and sources; **activate a column-header button** to sort. The "Min score" slider filters on the selected indicator, or on Protection Score when "All" is selected.

## Indicator glossary

Column abbreviations refer to the following measures:

- **AI** — AI Policy Status
- **DP** — Data Protection Law
- **ChildData** — Children's Data Safeguards
- **SOGI** — SOGI Sensitive Data
- **DPA** — DPA Independence
- **DPIA** — DPIA for High-Risk AI
- **LGBTQ** — LGBTQ+ Legal Status
- **Promo** — Anti-LGBT Propaganda Offences
- **COP** — Child Online Protection
- **SIM** — SIM–Biometric ID Linkage

## Compare countries

Add up to five countries to compare their indicator profiles (0–2 on each of ten indicators). Missing values remain gaps. Enable the optional charts when you are ready.

<div id="sc-chart-permission" class="sc-chart-permission">
  <p><strong>Optional interactive charts</strong> load Plotly and map assets from <code>cdn.plot.ly</code>. That provider receives normal request information. Your table filters run locally. This choice applies to this page only.</p>
  <button type="button" id="sc-load-charts" class="md-button md-button--primary">Load interactive charts</button>
  <a href="../../practices/">Data handling details</a>
  <p id="sc-chart-status" role="status" aria-live="polite">Charts are off. Use the country table or downloads without them.</p>
</div>


<div class="sc-explorer">
  <div class="sc-controls">
    <label for="sc-compare">Choose a country</label>
    <select id="sc-compare"><option value="">Select a country</option></select>
    <button type="button" id="sc-compare-add" class="md-button">Add to comparison</button>
  </div>
  <div id="sc-selected" aria-label="Selected countries"></div>
  <p id="sc-compare-status" role="status" aria-live="polite"></p>
  <div id="sc-radar" class="sc-chart"></div>
</div>

## Other ways to access the data

The explorer above reads the same underlying scored dataset you can pull programmatically.

[Download this snapshot as JSON or CSV](data-access.md#published-snapshot-downloads){ .md-button }

=== "CSV export"

    ```bash
    python pipeline_runner.py --mode scorecard --scorecard-action export
    ```

    Produces `data/exports/scorecard_*.csv` for use in Excel, Google Sheets, pandas, R, Tableau, or Power BI. See [Data Access](data-access.md).

=== "REST API (self-hosted)"

    Clone the repo and run the bundled API locally to query the data programmatically:

    ```bash
    python run_api.py
    ```

    The API is provided so anyone can run their own local data polling/extraction using the project's methods. See the [API docs](../api/index.md).

=== "Direct file"

    Open `data/scorecard/scorecard_main.xlsx` (canonical) for the full data with source URLs, or `Global_QueerAI_Child_Scorecard_MASTER.xlsx` for the clean scored visualization view.

!!! note "About this data"
    Point-in-time data derived from the project's designated visualization dataset. Source-URL verification is an ongoing, separate workflow, so figures may be revised. See the [Design & Methodology](design.md) for indicator definitions and the 0-1-2 scoring rules.

## Contribute

Spotted an error or have an updated source? Please [open an issue](https://github.com/MissCrispenCakes/DigitalChild/issues) with the country, indicator, current vs. corrected value, and an authoritative source URL.

______________________________________________________________________

For indicator definitions and scoring methodology, see [Design & Methodology](design.md). For the at-a-glance charts (map, distributions, regional comparison), see [Visualization](visualization.md).
