# GRIMdata platform revamp verification

Review branch: `revamp/grimdata-platform-2026-10`. Base source: `267f9c3393f7ae9c74831ec832a798d8ece4f0bb` (`basecamp`). The owner subsequently authorised direct publication after checks, without a separate offline approval.

## Architecture and compatibility

The root is the umbrella home. Explore, Projects, and Documentation have separate entrances. Documentation explicitly groups Tutorials, How-to guides, Reference, and Explanation. The previous root technical home is preserved at `/docs/technical-overview/`; recognised legacy root fragments redirect to their corresponding sections. `/website/` and all other existing public routes retain their substantive content and anchors.

The [URL migration map](URL_MIGRATION_MAP.md) records old/new destinations. A baseline build of the original source was compared against the new build: no public page routes or content anchors lost, including generated code-line anchors.

## Checks before publication

- `python -m mkdocs build --clean --strict`: passed, no build warnings.
- `python utils/verify_site_links.py --baseline /tmp/grim-baseline-site`: 65 pages, 10,639 local links/assets; no missing targets, anchors, or existing content destinations.
- Syntax checks for all three custom JavaScript files: passed.
- Focused jsdom interaction regressions against generated HTML and actual custom scripts: passed. Covered 194 initial explorer rows; loading state; sorting direction and ARIA; country filters; reset; 20/2 score ranges; detail focus/restoration; repeated instant-navigation initialization; comparison maximum/removal; no external chart script before choice; failed chart retry; theme rerender; Watch counts (29 total/5 API) and empty results.
- Original published scorecard JSON: unchanged. New CSV: 194 rows, all indicator scores checked against JSON. CSV includes assessment/source columns and spreadsheet formula escaping.
- Repository hooks for whitespace/EOF/YAML/size/private keys, Black, isort, and Flake8: passed on changed files.
- New/replaced Markdown pages: passed with a MkDocs-aware temporary profile allowing intentional HTML/cards and metadata titles. The repository's generic Markdownlint invocation reports existing Material/admonition formatting incompatibilities; no broad lint-policy changes were made. Its pre-commit Node bootstrap was blocked by the runtime's Git-package install policy, so the same CLI version was run from the standard npm registry.
- Backend pipeline/API behaviour is unchanged; a new full remote-source scraping run is outside this presentation/tool-UI change.

## Audited interaction changes

Removed automatic Google Fonts, Twemoji images, DOI badge requests, and the theme's GitHub repository-statistics fetch. The repository header remains a static link. Interactive charts require an explicit page-local choice to request Plotly/map assets from its provider. Table/watch filters remain browser-local against same-origin static JSON. External links retain normal navigation unless deliberately labelled as opening a new tab. Material may store appearance preferences locally. No configured analytics, account, visitor upload, or submission form was found; hosting logs and retention are not verified.

EthicalCarbon is a separate resident-led group. The Canadian oversight stream is planned national research. Research provenance/institutional continuity is proposed; Insight Grant funding is explicitly unconfirmed.

## Live verification

GitHub documentation deployment and CI both passed for the initial revamp commit. Live browser checks confirmed:

- The new root, explicit documentation navigation, future-project scopes, and preserved root citation redirect.
- Instant navigation from Home to Explorer to Maps to Watch; exactly one heading rainbow rule on research pages, matching refresh behaviour.
- Keyboard country sorting ascending/descending, Canada filtering, detail focus, close/focus restoration, and reset.
- Real Plotly comparison rendering; dark-theme switch; the map draws 194 country paths, indicator chart 30 bars, and regional chart five bars. Changing the map metric updates the title.
- Watch initial 29 signals, API filter five signals, source-link labels, and refresh reset.
- Documentation search returns the provenance track and correct deep links.
- A downloaded live CSV matches the checked repository file byte-for-byte and contains 194 rows.

The visual browser check found a low-contrast hero statistics panel and icon-only external links losing their names. A follow-up corrects the hero text colours, preserves descriptive social-link names, and uses a MkDocs hook to retain bundled SVG icons while emitting ordinary emoji as local Unicode text. No remote emoji images appear in the generated pages. Light and dark live homepage contrast and descriptive social-link names were verified after the follow-up deployment. A final audit also removed the automatically fetched GitHub source statistics; no Mermaid diagrams are currently present, and modern browsers use their built-in ResizeObserver.

## Remaining limits

- Mobile grids and source-card overflow were reviewed in CSS. This browser interface provides no supported viewport/device emulation, so a physical phone layout was not exercised. Desktop and theme checks used the actual live browser.
- Local preview infrastructure could not start because the supervisor sandbox could not mount `/proc`; live browser checks replaced that stage after the owner authorised publication.
- The website review does not establish hosting-provider logging or retention practices.
- The scorecard is the existing point-in-time snapshot, not a fresh policy validation. Both new research streams remain plans; no tracker database or confirmed grant is implied.
- Generic Markdownlint still reports existing MkDocs formatting incompatibilities. The actual GitHub CI and documentation deployment passed; no unrelated repository-wide formatting overhaul was attempted.
