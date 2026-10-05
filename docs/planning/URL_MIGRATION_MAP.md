---
search:
  exclude: true
---

# URL migration map

This reference lists current page locations and the destinations of earlier GRIMdata links. Existing page routes remain available; older root fragments lead to their corresponding sections in the technical overview.

| Existing URL | Current content | Compatibility |
| --- | --- | --- |
| `/` | GRIMdata umbrella home: purpose, tracks, platform entrances | The old technical home is copied in full to `/docs/technical-overview/`; old root fragments redirect to the corresponding preserved section. |
| `/website/` | About GRIMdata: contributions, stance, history and publications | The About tab opens this page. Relevant content and existing heading fragments remain; technical detail is linked from its documentation; the home button points to `/`. |
| `/website/projects/` | Retained project overview, publications and upcoming-project anchors | Retained, including both future-project anchors; home button points to `/`. |
| `/website/projects/littlerainbowrights/` | Digital rights research detail | Retained. Splash site is labelled as the public introduction. |
| `/website/projects/sgbv/` | Published SGBV-UPR study, methods and planned renewal | Retained. |
| `/website/getting-started/start-here/` | Audience orientation | Retained; linked from Documentation outside the four content types. |
| `/website/getting-started/quickstart/` | Guided first pipeline run | Retained under Tutorials; commands and examples retained. |
| `/website/getting-started/installation/` | Installation task guide | Retained under How-to guides. |
| `/scorecard/`, `/scorecard/visualization/`, `/scorecard/explorer/`, `/scorecard/data-access/`, `/scorecard/design/` | Research overview, exploration, task guide, and explanation | All routes and existing Markdown heading anchors retained; interactive controls improved. |
| `/transparency-watch/` | Interactive archive-signal exploration | Retained with keyboard-accessible filters and source labels. |
| `/api/*`, `/guides/*`, `/standards/*`, `/notes/*` | Established documentation | File routes preserved; navigation reorganised by purpose. API is accurately described as self-hosted. |
| `/ARCHITECTURE/`, `/DATA_GOVERNANCE/`, `/RESEARCH_CONTEXT/`, `/ROADMAP/`, `/CONTRIBUTING/`, `/FAQ/`, `/GLOSSARY/`, `/DOCS_INDEX/` | Established research and technical record | Retained. |
| `LittleRainbowRights.com` and future splash domains | Public big-idea introductions | Project introductions link to GRIMdata for tools, methods and evidence. |

Historical development pages retain their URLs and anchors. Longer planning and review records are linked from their summaries. The source-feasibility checklist is available under How-to guides.

## Research programme additions

| URL | Role | Parallel entrances |
| --- | --- | --- |
| `/research-history/` | Research origins, intellectual contributions and scholarly milestones | Home, About and both established project pages |
| `/research-directions/` | Available work, intended next investigations and dependencies across four tracks | Projects, About and project-specific next-step links |
| `/projects/` | Primary research-track catalogue | Home and project navigation |
| `/ROADMAP/` | DigitalChild/LRR software milestones and outstanding technical work | Documentation → Reference → Development Records |
| `/api/IMPLEMENTATION_HISTORY/` | Historical self-hosted API build record | Documentation → Reference → Development Records |

Research Context and Data Governance keep their URLs and full explanations, with concise excerpts and contextual links on Home, About and project pages. Earlier topic anchors lead to the corresponding research, licensing or technical guidance.

## New entrances

| New URL | Purpose |
| --- | --- |
| `/explore/` | Interactive data, source-watch tools, downloads, and limits |
| `/projects/` | Concise established/planned research track index |
| `/docs/` | Explicit Diátaxis hub: Tutorials, How-to guides, Reference, Explanation |
| `/docs/technical-overview/` | Preserved former root technical content and software citation |
| `/tutorials/first-country/` | Guided browser-only first assessment tutorial |
| `/practices/` | Browsing choices, optional charts, data handling and attribution |
| `/scorecard/data/scorecard.csv` | Download of the existing published visualization snapshot, with evidence columns |

## Root fragment compatibility

The original root fragments remain in a visible continuation section linking to the complete technical overview:

`#digitalchild-documentation`, `#quick-links`, `#documentation-sections`, `#getting-started`, `#core-guides`, `#api-documentation`, `#scorecard`, `#transparency-watch`, `#standards-specifications`, `#technical-architecture`, `#project-information`, `#project-structure`, `#key-features`, `#support`, `#citation`.

Generated code-line anchors (`__span-*` and `__codelineno-*`) from the original root are also retained and redirect to the corresponding unchanged code blocks.

The corresponding sections exist at `/docs/technical-overview/#<fragment>`. Recognised root fragments redirect with `location.replace` to the corresponding technical-overview fragment. A visible continuation pointer also works without JavaScript.

## Navigation and refresh

Material's instant navigation remains enabled. The rainbow-divider initializer subscribes to `document$` and deduplicates each heading rule. Research tools also initialise after page replacement. Home buttons use the new canonical umbrella home; `/website/` remains reachable for historical links.

## Publication boundary

Research routes and fragments remain available. Recognised legacy root fragments lead to the corresponding technical content.
