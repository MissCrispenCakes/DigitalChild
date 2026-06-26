# Source Availability Log

A running record of **external source documents that were previously available and are no longer reachable** from the URL we used (link rot, relocation, takedown, or access regression).

This is the inverse of the [Source Transparency Watch](../transparency-watch/index.md): that page tracks when peers *add* open access; this log tracks when previously-available primary sources *disappear*. For a research tool that cites primary documents, "this document used to be here and isn't anymore" is itself a finding worth preserving — for provenance, reproducibility, and to flag entries that may need a new source.

## How entries are recorded

Each entry captures, as far as can be established:

- **Document / target** — what we were fetching, and where it was used (CI demo set, scorecard source, etc.).
- **Source URL** — the URL that is no longer serving the file.
- **Previously available** — evidence it worked (commit date it was added, last successful use, and/or Wayback "last-seen" date).
- **Current status** — the HTTP status now (e.g. `301`/`404`) and whether the Internet Archive has a copy.
- **Noted** — date this disappearance was recorded.
- **Action** — what was done (removed from active set, replaced with a mirror, archived copy located, etc.).

> Wayback "last-seen" dates are an upper bound and may be absent if the URL was never archived. Combine with our own repo history.

## Entries

### AU Digital Economy report — `AU_Digital_Economy_2021.pdf`

- **Target:** "Building an Enabling Environment for Inclusive Digital Transformation in Africa" — part of the **CI live-download demonstration set** (`.github/workflows/ci.yml`).
- **Source URL:** `https://africaportal.org/wp-content/uploads/2023/06/Building-an-Enabling-Environment-for-Inclusive-Digital-Transformation-Africa-R_DQzy95E.pdf`
- **Previously available:** added to CI **2026-01-13** (commit `6953891`) and downloaded successfully in CI until ~June 2026.
- **Current status:** **HTTP 301** → redirects to a non-file page (document moved or removed). **No Internet Archive capture exists** for this URL (0 Wayback snapshots), so no archived copy is recoverable from there.
- **Noted:** 2026-06-26.
- **Action:** Removed from the CI demonstration set (the step now tolerates individual source failures regardless). The other 9 AU documents remain live. **TODO:** locate a working mirror of this report (e.g. an au.int or AfDB-hosted copy) and re-add, or source an alternative AU digital-economy document.

______________________________________________________________________

_Maintained alongside the URL validator (`processors/scorecard_validator.py`, which flags currently-broken scorecard source URLs). A future enhancement would auto-populate this log: cross-reference broken/redirected URLs against their Wayback last-seen dates to distinguish "transient outage" from "previously-available, now-gone."_
