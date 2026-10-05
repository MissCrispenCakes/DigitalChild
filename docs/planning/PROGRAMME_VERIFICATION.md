# GRIMdata research programme verification

Implementation baseline: `70c5aeab4ee642ad900dd96fea737211af35dfed` (DigitalChild/basecamp).

- Strict MkDocs build passed with pinned documentation requirements.
- Built-site verification passed: 67 HTML pages, 10,775 internal links/assets; all prior public routes and content IDs retained against the baseline build. Replaced sections keep aliases beside corresponding substantive content.
- Browser checks passed: 13 principal pages at desktop and 390px mobile widths, light/dark presentation, unique article IDs, instant navigation, Back/Forward, refresh and rainbow divider deduplication.
- Tested legacy upcoming-project, dataset-citation, research-context and roadmap anchors; root citation compatibility reaches the technical citation.
- Explorer checks passed: 194 countries; search; region filter; 132 fully documented rows; slider range switching; ascending/descending sort; empty/reset states; keyboard detail opening/closing; comparison cap and removal.
- Chart-choice checks passed: no unsolicited CDN request, failure/retry state and reload reset. Real Plotly 2.27.0 and geographic assets were retrieved through the execution proxy and supplied to the browser for rendering tests; map, indicators, regional and comparison charts rendered. Native direct browser-to-CDN transport could not be tested in this execution environment.
- Source Transparency Watch filters passed: 29 total signals; datasets 10, structures 9, documents 5, APIs 5; topical filtering.
- Search returned new research-history content. Internal planning/review material remains outside search; the source-feasibility task guide is intentionally searchable.
- Actual HTTP JSON/CSV downloads match baseline bytes; 194 country records retained. No research data regenerated.
- Keyboard skip link and visible action focus passed.
- Axe WCAG 2/2.1 A/AA checks returned zero violations on Home, About, Research History, Research Directions, SGBV-UPR, Explorer and Documentation in both themes. This is a bounded automated check, not a complete accessibility certification.
- Three JavaScript syntax checks and Git whitespace check (preserving existing CRLF conventions) passed.
- No EthicalCarbon public copy, contact cards, collaboration/support solicitations or portfolio links added. HumanRights was neither accessed nor changed; no private archival material transferred.

Limits: full backend/scraper suite was not rerun for these documentation and presentation changes; it relies partly on live third-party sources. Hosting retention practices and every external source URL were not independently verified. Live deployment verification follows the push.
