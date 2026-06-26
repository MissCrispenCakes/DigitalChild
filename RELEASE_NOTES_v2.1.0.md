# Release Notes - v2.1.0

**Date:** 2026-06-26
**Zenodo DOI:** [10.5281/zenodo.18318098](https://doi.org/10.5281/zenodo.18318098) (concept DOI; a new version DOI is minted on release)

## 🎨 Minor Release: Visualization Phase Begins

This release opens **Phase 5 (Visualization)**. It adds an interactive, server-free
visualization layer to the GRIMdata.org site and a new transparency-monitoring
feature. All changes are **additive and non-breaking** — the pipeline, REST API,
data schema, and CLI are unchanged.

## 🚀 What's New

### Interactive Scorecard Visualization

Live at [grimdata.org/scorecard/visualization](https://grimdata.org/scorecard/visualization/):

- **Choropleth world map** with switchable metric: Protection Score (0–20), Risk Index (0–100), or data completeness.
- **Indicator distribution** charts (how all 194 countries score 0/1/2 on each of the 10 indicators).
- **Regional comparison** (average protection by region).
- Rendered in-browser with Plotly from a **published static dataset** — no server required.

### Scorecard Data Explorer

Live at [grimdata.org/scorecard/explorer](https://grimdata.org/scorecard/explorer/):

- Filter (region, indicator, score), search, and **sortable table** with a colour-coded indicator heatmap.
- **Country detail panel** — per-indicator score, scoring-rule, free-text justification, and source links.
- **Data-completeness indicator** ("documented X/10") flagging under-documented countries.
- **Country-comparison radar** overlaying up to five countries' indicator profiles.

### Source Transparency Watch

Live at [grimdata.org/transparency-watch](https://grimdata.org/transparency-watch/):

- Tracks when **peer organisations adopt open-data / primary-source transparency**, dated via the Internet Archive Wayback CDX API.
- Adoption **timeline** + per-source cards across 10 monitored bodies (UNCTAD, UNESCO, ILGA, Human Dignity Trust, Privacy International, OECD.AI, Freedom House, Access Now, Ranking Digital Rights, DLA Piper).
- Honest coverage handling — domains too large to scan reliably are marked "not yet assessed" rather than reported as a false negative.

## 🛠️ Technical

- **Static-data generators** (read-only; write only into `docs/`, never touching canonical sources):
  - `utils/build_scorecard_viz_data.py` → `docs/scorecard/data/scorecard.json`
  - `utils/build_transparency_watch_data.py` → `docs/transparency-watch/data/transparency.json`
- **Source Availability Log** (`docs/maintenance/SOURCE_AVAILABILITY_LOG.md`) — records previously-available sources that have gone dead (link rot), the inverse of the Transparency Watch.
- **CI hardening** — the live-download demonstration step now tolerates individual rotted source URLs (a single dead third-party link no longer aborts the run).
- **Test suite:** 347 tests passing.

## 🔒 Security

- Dependency updates (via Dependabot): Flask 3.1.2 → 3.1.3, Werkzeug 3.1.5 → 3.1.6, ujson 5.10.0 → 5.13.0, pymdown-extensions 10.20 → 10.21.3, python-dotenv 1.0.1 → 1.2.2.

## 📚 Data Sources

Scorecard data is the project's designated visualization dataset; source-URL
validation is an ongoing, separate workflow, so figures are point-in-time. See
the [methodology](https://grimdata.org/scorecard/design/) and on-page caveats.

## 📖 Documentation

- **Visualization:** https://grimdata.org/scorecard/visualization/
- **Data Explorer:** https://grimdata.org/scorecard/explorer/
- **Transparency Watch:** https://grimdata.org/transparency-watch/
- **Changelog:** see `CHANGELOG.md` (`[2.1.0]`)

## ⬆️ Upgrade Notes

No action required for existing users — no breaking changes. Pipeline, REST API,
data schema, and CLI are unchanged.
