# URL migration map

This revamp keeps existing public file routes and adds umbrella entrances. No production domain swap or path-wide rewrite is required. Only recognised legacy root fragments redirect to their corresponding preserved technical sections. Old overview URLs remain explicit compatibility pages to preserve fragments and the research record.

| Existing URL | Role after the revamp | Compatibility |
| --- | --- | --- |
| `/` | GRIMdata umbrella home: purpose, tracks, platform entrances | The old technical home is copied in full to `/docs/technical-overview/`; old root fragments redirect to the corresponding preserved section. |
| `/website/` | About GRIMdata and full research overview | The About tab opens this page. Full substantive content and heading fragments remain; the home button points to `/`. |
| `/website/projects/` | Full project scopes and publications | Retained, including both future-project anchors; home button points to `/`. |
| `/website/projects/littlerainbowrights/` | Digital rights research detail | Retained. Splash site is labelled as the public introduction. |
| `/website/projects/sgbv/` | Published precursor and reconstruction context | Retained. |
| `/website/getting-started/start-here/` | Audience orientation | Retained; linked from Documentation outside the four content types. |
| `/website/getting-started/quickstart/` | Guided first pipeline run | Retained under Tutorials; commands and examples retained. |
| `/website/getting-started/installation/` | Installation task guide | Retained under How-to guides. |
| `/scorecard/`, `/scorecard/visualization/`, `/scorecard/explorer/`, `/scorecard/data-access/`, `/scorecard/design/` | Research overview, exploration, task guide, and explanation | All routes and existing Markdown heading anchors retained; interactive controls improved. |
| `/transparency-watch/` | Interactive archive-signal exploration | Retained with keyboard-accessible filters and source labels. |
| `/api/*`, `/guides/*`, `/standards/*`, `/notes/*` | Established documentation | File routes preserved; navigation reorganised by purpose. API is accurately described as self-hosted. |
| `/ARCHITECTURE/`, `/DATA_GOVERNANCE/`, `/RESEARCH_CONTEXT/`, `/ROADMAP/`, `/CONTRIBUTING/`, `/FAQ/`, `/GLOSSARY/`, `/DOCS_INDEX/` | Established research and technical record | Retained. |
| `LittleRainbowRights.com` and future splash domains | Public big-idea introductions | No external domain changes or deployments in this review. GRIMdata houses the tools and evidence. |

Historical planning notes and implementation test reports keep their existing URLs and content anchors, but are omitted from primary navigation and search. The source-feasibility checklist is available under How-to guides.

## New entrances

| New URL | Purpose |
| --- | --- |
| `/explore/` | Interactive data, source-watch tools, downloads, and limits |
| `/projects/` | Concise established/planned research track index |
| `/docs/` | Explicit Diátaxis hub: Tutorials, How-to guides, Reference, Explanation |
| `/docs/technical-overview/` | Preserved former root technical content and software citation |
| `/tutorials/first-country/` | Guided browser-only first assessment tutorial |
| `/practices/` | Reviewed site behaviour, optional charts, data handling, participation and uncertainty |
| `/scorecard/data/scorecard.csv` | Download of the existing published visualization snapshot, with evidence columns |

## Root fragment compatibility

The original root fragments remain in a visible continuation section linking to the complete technical overview:

`#digitalchild-documentation`, `#quick-links`, `#documentation-sections`, `#getting-started`, `#core-guides`, `#api-documentation`, `#scorecard`, `#transparency-watch`, `#standards-specifications`, `#technical-architecture`, `#project-information`, `#project-structure`, `#key-features`, `#support`, `#citation`.

Generated code-line anchors (`__span-*` and `__codelineno-*`) from the original root are also retained and redirect to the corresponding unchanged code blocks.

The corresponding sections exist at `/docs/technical-overview/#<fragment>`. This preserves inbound links while making the root an umbrella home. Recognised root fragments redirect with `location.replace` to the corresponding technical-overview fragment, preserving the expected subject rather than landing on an unrelated home section. A visible continuation pointer also works without JavaScript.

## Navigation and refresh

Material's instant navigation remains enabled. The rainbow-divider initializer subscribes to `document$` and deduplicates each heading rule. Research tools also initialise after page replacement. Home buttons use the new canonical umbrella home; `/website/` remains reachable for historical links.

## Publication boundary

The migration is live. Existing research routes remain available, and recognised legacy root fragments lead to the corresponding technical content.
