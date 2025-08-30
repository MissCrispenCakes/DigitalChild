# Project Roadmap

This roadmap outlines the milestones for the GRIMdata / LittleRainbowRights pipeline.

---

## Phase 1: Core Pipeline (✅ in progress)

- [x] Project scaffolding (`init_project.py`)
- [x] AU Policy scraper
- [x] PDF → text processor
- [x] Tagging (v1, v2, v3, digital)
- [x] Metadata tracking
- [x] Logging system
- [x] Tests for processors, tagging, logging, metadata
- [x] Docs (setup, structure, standards, pipeline flow)

---

## Phase 2: Expanded Sources (⏳ next)

- [ ] Scrapers for OHCHR Treaty Body database
- [ ] UPR documents
- [ ] UNICEF reports
- [ ] ACERWC reports
- [ ] ACHPR reports
- [ ] Manual upload ingestion

---

## Phase 3: Advanced Processing

- [ ] Recommendations extraction (regex + NLP configs)
- [ ] Timeline exports (tags_timeline.py)
- [ ] Comparison across tagging/recs versions
- [ ] Normalization of country/region to ISO codes
- [ ] Doc type classification (Policy, Law, TreatyBody, etc.)

---

## Phase 4: Research Dashboard

- [ ] Flask backend for serving metadata/exports
- [ ] Visualization frontend (tags frequency, timelines, heatmaps)
- [ ] Interactive filters (region, country, tags, year)
- [ ] Export/download UI for datasets

---

## Phase 5: Global Expansion

- [ ] Extend scrapers to other regions (Europe, Asia, Americas)
- [ ] Merge African + global content
- [ ] Global comparative analysis

---

## Notes

- End-to-end MVP already works with AU Policy pipeline.
- Future work extends sources and visualizations.
