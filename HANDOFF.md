# HANDOFF — GRIMdata site cleanup

**Last session:** 2026-06-27 · **Branch:** `basecamp` · **Resume:** 2026-06-28

This is a working resume note (kept at repo root so MkDocs does **not** publish it).
It captures where the grimdata.org documentation cleanup stands, the decisions made,
and what's left. Delete it whenever the cleanup is done.

## How to resume

```bash
cd /mnt/h/DigitalChild
source .LittleRainbow/bin/activate
git pull origin basecamp
mkdocs build --clean          # local preview build (NOT --strict; warnings don't fail CI)
mkdocs serve                  # live preview at http://127.0.0.1:8000
# Before any push:
pre-commit run --all-files
# Deploy = push to basecamp -> GitHub Actions (.github/workflows/deploy-docs.yml) -> grimdata.org
```

## Settled direction (don't re-litigate)

- **Two sites.** `littlerainbowrights.com` = the streamlined, professional **live product**
  (map, country-compare, charts; own repo `MissCrispenCakes/LittleRainbowRights`, deploy-from-branch,
  live-fetches data from grimdata). `grimdata.org` = the **reference hub** (full content, API,
  data, methodology, portfolio; DigitalChild repo, GitHub Actions). Do NOT strip the visuals out
  of grimdata — directive is "keep grimdata's content, just clean it up."
- **Docs organised by Diátaxis** (Explore / Tutorials / How-to / Reference / Explanation + Projects, About).
- **De-dup style:** one canonical copy + links (approved).
- **API port is 5000** everywhere — confirmed in `run_api.py` (`DEV_PORT`), `.env.example`,
  `wsgi.py`, `Dockerfile`, `docker-compose.yml`. `:8000` appears in 0 docs. No port problem.

## Done this session (6 commits, all pushed to basecamp)

1. `ec4c215` — Diátaxis nav reorg + API reference de-stale/de-dup; relocated API build-history to `api/IMPLEMENTATION_HISTORY.md`.
2. `7123af6` — stopped publishing 11 stale internal process docs via `exclude_docs` in `mkdocs.yml` (kept in git).
3. `db1f2ae` — citation normalization to `CITATION.cff` canon; restored dropped co-author; year/title/ORCID/format consistent.
4. `dc7c4bd` — de-dup `scorecard/visualization.md` (459 → 335 lines): removed verbatim 10-indicator block → links to `design.md#the-10-indicators`.
5. `8444a34` — new **Start Here** audience-routing page (`docs/website/getting-started/start-here.md`, first Tutorials entry); removed misplaced audience guidance from `design.md` and home `Use Cases`.
6. `6b59a75` — finished snippet sweep (curl de-dup on scorecard pages), fixed 3 broken anchors, added left-nav legibility CSS.

## TODO (resume here, roughly in priority order)

1. **Eyeball the nav CSS on the live site** (`docs/website/stylesheets/extra.css`, bottom block).
   It differentiates section groups / page links / integrated page-TOC. Material's exact DOM
   for `navigation.sections` + `navigation.tabs` + `toc.integrate` may need a selector tweak after
   you see it render. This is the one change that should be visually verified.
2. **De-bloat the long pages** — `scorecard/data-access.md` (624 lines, 4 access methods crammed
   in one) and `api/index.md` (459). Bigger restructure; overlaps the tab decision (#5).
3. **Project-page audience sections** — `website/projects/littlerainbowrights/index.md` and
   `projects/sgbv/index.md` still have "For Researchers/Advocates/Policymakers" (left intentionally —
   project-specific). Point them at Start Here if you want them thinner.
4. **Two-homepage quirk** — `docs/index.md` is served at `grimdata.org/` while the nav's "GRIMdata
   Home" is `website/index.md` at `/website/`. Reconcile during the structure pass.
5. **Settle the top-level tab structure** (deferred until pages are lean). `navigation.tabs` means
   top-level nav entries = the tab row. Since LRR.com is the product front, grimdata leads as the
   reference hub but must still surface Explore (scorecard/transparency) + Projects, not bury them.
   Options discussed: (a) product-first tabs + one "Documentation" tab w/ Diátaxis sidebar;
   (b) "Explore" hub + Docs tab; (c) everything-as-tabs (crowded). Leaning (a)/(b).

## Deferred decisions (need maintainer)

- **Code-vs-data authorship split.** Whether the non-coding co-author comes off the *software/code*
  citations (CITATION.cff `authors:`, README/docs `@software`) while staying on data + publications.
  For now BOTH are kept everywhere. **S.C. Vollmer is the code author** (stays on code if split).
  See `CITATION.cff` and the citation-and-authorship memory.
- **Lower-priority de-dup not done:** the "2,543 sources" stat (~19 files — a prose number,
  awkward to link, low drift risk) and `pip install` across setup pages (contextual, left as-is).
  A real fix would be a shared snippet include (mkdocs `snippets` extension — not currently installed).

## Canonical references

- **Citations:** `CITATION.cff` is the source of truth. Software = `@software{digitalchild2025}`
  (S.C., D.T.; year 2025; v2.1.0; DOI 10.5281/zenodo.18318098). Data = `@misc{littlerainbowrights2025scorecard}`
  (D.T., S.C.; 2025; CC-BY-4.0). ORCIDs: S.C. `0000-0002-3359-2810`, D.T. `0000-0002-5035-3395`.
- **Timeline:** work began 2019; SGBV conf 2021 + journal 2022; Queer AI conf paper 2025;
  new journal article in progress 2026; LRR repo 2025–2026; software v2.1.0 released 2026-06-26.
- **Plan doc:** `docs/planning/SITE_IA_SEE_VS_BUILD_PLAN.md`.
- **What's NOT published:** see `exclude_docs:` in `mkdocs.yml`. Dead/disappeared external sources:
  `docs/maintenance/SOURCE_AVAILABILITY_LOG.md`.

## Gotchas

- `gh` browser-auth fails as root — use `GH_TOKEN`/PAT (it isn't set in this shell; releases are run by the user).
- Never touch Microsoft 365 DNS records (MX/SPF/DMARC/autodiscover/sip) on GoDaddy.
- Pre-existing broken anchors fixed this session; if `mkdocs build` still shows anchor INFO lines,
  they're new — check the link's slug against the built HTML id.
- Untracked working files present and intentionally not committed: `landing/` (the separate
  LittleRainbowRights repo staging artifact), `presentations/CAIS_2026_abstract_DRAFT.md`.
