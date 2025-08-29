# Tags Visualization Plan

This document describes how tag data will be visualized for researchers.

---

## Goals

- Show how frequently tags appear across documents.
- Allow filtering by region, country, year, source.
- Compare across tag versions.

---

## Planned Visualizations

1. **Tag Frequency Bar Chart**
   - X-axis: Tags
   - Y-axis: Count of documents
   - Filter: Region/country

2. **Timeline View**
   - X-axis: Year
   - Y-axis: Count or % of documents
   - Multiple lines for each tag
   - Useful for trend analysis

3. **Heatmap**
   - Rows: Countries
   - Columns: Tags
   - Color intensity = frequency
   - Highlights regional gaps

4. **Comparison Mode**
   - Side-by-side view of v1 vs v3 (or other versions)
   - Shows how new terms expanded coverage

---

## Export Strategy

- Data exported as CSV (`tags_summary.csv`, `tags_timeline.csv`).
- Visualizations generated via a research dashboard (future).
- Frontend: likely D3.js or Plotly; backend: Flask APIs.

---

## Notes

- Start with CSV + simple matplotlib prototypes.
- Move toward web-based dashboards for interactive exploration.
