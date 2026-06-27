# Update Summary — June 2026 (Visualization Phase)

**Date:** 2026-06-26
**Release:** v2.1.0 — concept DOI [10.5281/zenodo.18318098](https://doi.org/10.5281/zenodo.18318098) (this version: 10.5281/zenodo.20950631)
**Status:** ✅ Live on [grimdata.org](https://grimdata.org)

This summary captures the state of the DigitalChild / LittleRainbowRights upgrade at the start of **Phase 5 (Visualization)**, following the v2.0.x API/JOSS work.

## What shipped in this cycle

### Interactive scorecard visualization (LIVE)

- **Choropleth world map** — Protection Score (0–20), Risk Index (0–100), or data-completeness, switchable. [/scorecard/visualization/](https://grimdata.org/scorecard/visualization/)
- **Indicator-distribution** and **regional-comparison** charts.
- **Data Explorer** — filter/search/sortable table with a colour-coded indicator heatmap, per-country **detail panel** (score + scoring rule + justification + source links), a **"documented X/10" completeness indicator**, and a **country-comparison radar**. [/scorecard/explorer/](https://grimdata.org/scorecard/explorer/)
- All rendered in-browser (Plotly) from a **published static dataset** — no server required.

### Source Transparency Watch (NEW, LIVE)

- Tracks when **peer organisations adopt open-data / primary-source transparency**, dated via the Internet Archive Wayback CDX API. [/transparency-watch/](https://grimdata.org/transparency-watch/)
- Adoption timeline + per-source cards across **10 monitored bodies** (UNCTAD, UNESCO, ILGA, Human Dignity Trust, Privacy International, OECD.AI, Freedom House, Access Now, Ranking Digital Rights, DLA Piper).
- Honest coverage handling — large domains that can't be scanned reliably are marked "not yet assessed," not a false negative.

### Architecture & provenance

- Two **read-only static-data generators** (`utils/build_scorecard_viz_data.py`, `utils/build_transparency_watch_data.py`) write only into `docs/`; canonical sources are never modified.
- **Source Availability Log** (`docs/maintenance/SOURCE_AVAILABILITY_LOG.md`) records previously-available sources that have gone dead (link rot) — the inverse of the Transparency Watch.
- **CI hardening** — the live-download demonstration now tolerates individual rotted source URLs.
- Dependency updates (Flask 3.1.3, Werkzeug 3.1.6, ujson 5.13.0, pymdown-extensions 10.21.3, python-dotenv 1.2.2).

## Current metrics

| Metric | Value |
|---|---|
| Countries | 194 |
| Scorecard indicators | 10 (0–2 scale + composite Protection Score / Risk Index) |
| Validated source URLs | 2,543 |
| REST API endpoints | 14 |
| Tests | 347 passing |
| Monitored transparency peers | 10 |

## Roadmap position

Phase 5 (Visualization) is **in progress** — delivered as a static, server-free implementation (Plotly + vanilla JS on the MkDocs site) rather than a JS-framework SPA. Remaining Phase 5 candidates: time-series tracking of policy changes, targeted Wayback queries for very large domains (UNESCO, Privacy International), a scheduled refresh of the Transparency Watch, and a fuller comparison/gap-analysis dashboard. See [ROADMAP](ROADMAP.md).

## References

- Prior work: Vollmer & Vollmer (2022), *Stellenbosch Law Review* (SGBV-UPR); conference paper "Queer AI for the digital child" (Second International Conference on Children's Rights, Stellenbosch, Sept 2025).
- Changelog: see `CHANGELOG.md` (`[2.1.0]`).
