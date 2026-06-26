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
    <label>Min score
      <input type="range" id="sc-f-minscore" min="0" max="2" step="1" value="0">
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

  <p id="sc-count" class="sc-count"></p>
  <div id="sc-table"></div>
  <div id="sc-detail" class="sc-detail"></div>
</div>

!!! info "Reading the table"
    Each indicator column (`AI`, `DP`, `ChildData`, …) shows the 0–2 score, colour-coded
    **<span style="color:#2e8b57">2 = best</span> / <span style="color:#e8a33d">1 = partial</span> / <span style="color:#d64545">0 = worst</span>** (hover a column header for its full name). **Prot.** is the Protection Score (0–20); **Risk** is the Risk Index (0–100). **Doc** is data completeness — how many of the 10 indicators carry a documented justification (rows below 10/10 are flagged). **Click any row** to open a country detail panel with each indicator's assessment and sources; **click a column header** to sort. The "Min score" slider filters on the selected indicator, or on Protection Score when "All" is selected.

## Compare countries

Select up to five countries to overlay their indicator profiles (0–2 on each of the 10 indicators).

<div class="sc-explorer">
  <div class="sc-controls">
    <label for="sc-compare">Countries (Ctrl/⌘-click for multiple):</label>
    <select id="sc-compare" multiple size="6" style="min-width:14rem"></select>
  </div>
  <div id="sc-radar" class="sc-chart"></div>
</div>

## Other ways to access the data

The explorer above reads the same underlying scored dataset you can pull programmatically.

=== "CSV export"

    ```bash
    python pipeline_runner.py --mode scorecard --scorecard-action export
    ```

    Produces `data/exports/scorecard_*.csv` for use in Excel, Google Sheets, pandas, R, Tableau, or Power BI. See [Data Access](data-access.md).

=== "REST API (self-hosted)"

    Clone the repo and run the bundled API locally to query the data programmatically:

    ```bash
    python run_api.py
    curl http://localhost:5000/api/scorecard
    curl http://localhost:5000/api/scorecard/Kenya
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
