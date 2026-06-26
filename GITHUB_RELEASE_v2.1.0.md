# Release v2.1.0 - Visualization Phase Begins

**Release Date:** June 26, 2026
**Zenodo DOI:** [10.5281/zenodo.18318098](https://doi.org/10.5281/zenodo.18318098) (concept DOI — resolves to latest)

Minor, **non-breaking** release opening Phase 5 (Visualization): an interactive, server-free visualization layer on GRIMdata.org plus a new transparency-monitoring feature. Pipeline, REST API, data schema, and CLI are unchanged.

---

## 🎨 What's New

### Interactive Scorecard Visualization — [view](https://grimdata.org/scorecard/visualization/)

- Choropleth world map (Protection Score / Risk Index / data-completeness metrics)
- Indicator-distribution and regional-comparison charts
- Rendered in-browser (Plotly) from a published static dataset — no server needed

### Scorecard Data Explorer — [view](https://grimdata.org/scorecard/explorer/)

- Filter / search / sortable table with a colour-coded indicator heatmap
- Per-country **detail panel** (score, scoring rule, justification, source links)
- **Data-completeness** indicator ("documented X/10")
- **Country-comparison radar** (overlay up to 5 countries)

### Source Transparency Watch — [view](https://grimdata.org/transparency-watch/)

- Tracks when peer organisations adopt open-data / primary-source transparency, dated via the Internet Archive Wayback CDX API
- Adoption timeline + per-source cards across 10 monitored bodies

## 🛠️ Technical

- Read-only static-data generators (`utils/build_scorecard_viz_data.py`, `utils/build_transparency_watch_data.py`) — write only into `docs/`
- Source Availability Log for link-rot (`docs/maintenance/SOURCE_AVAILABILITY_LOG.md`)
- CI live-download demo hardened against individual dead source URLs
- 347 tests passing

## 🔒 Security

Dependency updates (Dependabot): Flask 3.1.3, Werkzeug 3.1.6, ujson 5.13.0, pymdown-extensions 10.21.3, python-dotenv 1.2.2.

## ⬆️ Upgrade Notes

No breaking changes — no action required for existing users.

**Full Changelog:** v2.0.1...v2.1.0
