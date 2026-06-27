# Site IA Plan — Diátaxis everywhere ("See vs Build")

**Date:** 2026-06-27
**Status:** Phase 1 (nav) ✅ done · Phases 2–3 (page splits + cross-links) proposed
**Framework:** [Diátaxis](https://diataxis.fr/start-here/)
**Goal:** Organise every part of grimdata.org by what the reader is trying to *do*, so a
visitor who just wants to look at the scorecard isn't dropped into methodology, and a
developer who wants the full reference isn't stuck in a quick-start.

> No content is deleted — pages are **regrouped**, and where one page mixes two jobs it is
> **split** so each piece lands in the right mode. Relocations leave a pointer, never a gap.
> The "how it got built" trail stays intact.

## The framework

[Diátaxis](https://diataxis.fr) sorts documentation by two axes (acquisition vs application
of skill; practical vs theoretical knowledge) into four modes. We add **Explore** for the
live product — the "see the data" front that sits above the docs.

| Mode | Reader's question | Examples here |
|---|---|---|
| **Explore** *(product)* | "Show me the data" | Scorecard map & charts, Data Explorer, Transparency Watch |
| **Tutorials** | "Get me started" | Install & first run, first API call |
| **How-to guides** | "Help me do X" | Get the data, run the pipeline, deploy, troubleshoot |
| **Reference** | "Tell me the facts" | API endpoints, config/standards, glossary, schemas |
| **Explanation** | "Help me understand why" | Scorecard methodology, architecture, governance, research context |

`littlerainbowrights.com` is the top-of-funnel "see" front door; grimdata.org is where all
five modes live below it.

## The mixing problem (what prompted this)

- **API docs** repeated the same install/quick-start/endpoint/deployment content across
  `reference.md`, `quick-reference.md`, `quickstart.md`, and `index.md`, and carried stale
  "Phase 4 complete / January 2026" status copy. *(Fixed — see Phase 0 below.)*
- **`scorecard/visualization.md`** is ~2,000 words / ~18 phone-screens because it embeds the
  charts *inside* methodology, exports, citation, and limitations — four modes on one page.
- **Getting Started** mixed a tutorial with troubleshooting.
- **Projects** buried ~33 dev/process docs (standards, notes, planning, reviews) under one tab.

## Phase 0 — API de-stale & de-dup ✅ done (2026-06-27)

- `api/reference.md` trimmed to a pure **endpoint reference**: removed the duplicated Quick
  Start (now points to `api/quickstart.md`), removed the duplicated weekly dev-history and
  the roadmap wishlist, replaced the embedded Gunicorn/Docker how-to with a pointer to the
  Production Deployment guide, and replaced the Service-Layer code dump with a pointer to
  Architecture (Explanation). Added a "Beyond this reference" signpost block.
- Week-by-week build trail **relocated** to `api/IMPLEMENTATION_HISTORY.md` (trail preserved,
  reference kept clean).
- `api/quick-reference.md` deployment section collapsed to a pointer; stale footer refreshed.

## Phase 1 — Diátaxis nav regroup ✅ done (2026-06-27)

`mkdocs.yml` nav reshaped from 7 ad-hoc sections into **Explore / Tutorials / How-to guides /
Reference / Explanation** (plus Projects and About). **No files moved** — file paths and
therefore URLs are unchanged, so no in-page links broke and no redirects were needed. Every
prior nav entry is preserved; the dev docs that were buried under *Projects → Development*
now sit in Reference (standards, notes, glossary, docs index) and Explanation (pipeline flow,
logging, governance, research context).

## Phase 2 — split the mixed pages (proposed)

The only remaining *content* moves. Each split relocates-by-pointer; nothing is lost.

| Page | Action |
|---|---|
| `scorecard/visualization.md` | Cut to **visuals only** (map + charts + a one-line "How it's scored →"). Move scoring/methodology → `scorecard/design.md` (Explanation); exports/API examples → `scorecard/data-access.md` (How-to); citation/limitations → Explanation. (~2,000 → ~400 words.) |
| `scorecard/index.md` | Slim to a routing hub: *See it* (Explore) · *Understand it* (Explanation) · *Get it* (How-to). |
| `api/index.md` | Confirm it reads as a Reference **overview/landing**, not a second quick-start. |
| `website/getting-started/{installation,quickstart}.md` | Decide whether these stay two Tutorial pages or merge into one "Install & First Run"; today they're distinct (full install vs first run) and both are linked from project pages, so keep separate unless they actually overlap. |

## Phase 3 — cross-links so the modes connect (proposed)

- Every **Explore** page gets a quiet "How it's scored / how this works →" link into its
  Explanation counterpart.
- Every **Explanation** page gets a "See it live →" link back to the map/explorer.
- **Tutorial ⟷ Reference** cross-link both ways (Quick Start ⟷ Endpoint Reference — already
  wired in Phase 0).

## Out of scope / preserved

- No deletions; all pages remain (regrouped/split). Redirects/anchors only if a URL must
  change — Phase 1 changed none.
- `littlerainbowrights.com` (the bespoke "see" front door) is unchanged by this — it already
  links into Explore.
