# GRIMdata platform revamp verification

Review branch: `revamp/grimdata-platform-2026-10`. Base source: `267f9c3393f7ae9c74831ec832a798d8ece4f0bb` (`basecamp`). The owner subsequently authorised direct publication after checks, without a separate offline approval.

## Architecture and compatibility

The root is the umbrella home. Explore, Projects, and Documentation have separate entrances. Documentation explicitly groups Tutorials, How-to guides, Reference, and Explanation. The previous root technical home is preserved at `/docs/technical-overview/`; recognised legacy root fragments redirect to their corresponding sections. `/website/` and all other existing public routes retain their substantive content and anchors.

The [URL migration map](URL_MIGRATION_MAP.md) records old/new destinations. A baseline build of the original source was compared against the new build: no public page routes or content anchors lost.

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

Removed automatic Google Fonts, Twemoji images, and DOI badge requests. Interactive charts require an explicit page-local choice to request Plotly/map assets from its provider. Table/watch filters remain browser-local against same-origin static JSON. External links retain normal navigation unless deliberately labelled as opening a new tab. Material may store appearance preferences locally. No configured analytics, account, visitor upload, or submission form was found; hosting logs and retention are not verified.

EthicalCarbon is a separate resident-led group. The Canadian oversight stream is planned national research. Research provenance/institutional continuity is proposed; Insight Grant funding is explicitly unconfirmed.

## Live verification

To be completed after the production deployment: actual Plotly/geography rendering, browser navigation/refresh/history, documentation search, responsive layouts, theme switching, keyboard operation, and representative downloads/external links. Local preview infrastructure could not start: the supervisor's sandbox could not mount `/proc`. Focused DOM tests mock Plotly and fetch; they do not establish actual browser chart rendering.
