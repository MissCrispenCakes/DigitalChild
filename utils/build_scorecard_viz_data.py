#!/usr/bin/env python3
"""Build the static scorecard dataset that powers the GRIMdata.org visualizations.

READ-ONLY w.r.t. all canonical/source files. This script reads the designated
visualization workbook (``Global_QueerAI_Child_Scorecard_MASTER.xlsx`` -- see
``data/scorecard/README.md``: "Clean visualization version ... Use this for:
Generating heatmaps") plus region metadata from the canonical
``scorecard_main.xlsx`` (read only), and writes a single static JSON into the
published docs tree:

    docs/scorecard/data/scorecard.json

It never writes back into any Excel source, the root convenience copies, or the
``data/exports`` CSVs -- so it cannot erase pipeline work. The website depends
only on the JSON *schema* below, not on which workbook is canonical; when the
source-validation pipeline settles the official numbers, just point this
generator at the authoritative sheet and re-run -- the front-end is unchanged.

Usage:
    python utils/build_scorecard_viz_data.py
    python utils/build_scorecard_viz_data.py --viz-xlsx PATH --canonical-xlsx PATH --out PATH

Run from the repository root.
"""
import argparse
import json
import math
import os
import sys
from datetime import datetime, timezone

import pandas as pd

# Make repo root importable so we can reuse the project's country normalizer.
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

try:
    from scrapers.country_utils import normalize_country
except Exception:  # pragma: no cover - fallback if import path changes
    normalize_country = None

try:
    import pycountry
except Exception:  # pragma: no cover
    pycountry = None

VIZ_XLSX = os.path.join(
    REPO_ROOT, "data", "scorecard", "Global_QueerAI_Child_Scorecard_MASTER.xlsx"
)
CANONICAL_XLSX = os.path.join(REPO_ROOT, "data", "scorecard", "scorecard_main.xlsx")
OUT_JSON = os.path.join(REPO_ROOT, "docs", "scorecard", "data", "scorecard.json")

# Indicator metadata: (short key, numeric score column, free-text column, label).
# Score columns/text columns are from the QueerAI "Scorecard" sheet.
INDICATORS = [
    ("AI", "AI_Score", "AI_Policy_Status", "AI Policy Status"),
    ("DP", "DP_Score", "Data_Protection_Law", "Data Protection Law"),
    (
        "ChildData",
        "ChildData_Score",
        "Children_Data_Safeguards",
        "Children's Data Safeguards",
    ),
    ("SOGI", "SOGI_Score", "SOGI_Sensitive_Data", "SOGI Sensitive Data"),
    ("DPA", "DPA_Ind_Score", "DPA_Independence", "DPA Independence"),
    ("DPIA", "DPIA_Score", "DPIA_Required_High_Risk_AI", "DPIA for High-Risk AI"),
    ("LGBTQ", "LGBTQ_Score", "LGBTQ_Legal_Status", "LGBTQ+ Legal Status"),
    (
        "Promo",
        "Promo_Score",
        "Promotion_Propaganda_Offences",
        "Anti-LGBT Propaganda Offences",
    ),
    ("COP", "COP_Score", "COP_Strategy", "Child Online Protection"),
    ("SIM", "SIM_Score", "SIM_Biometric_ID_Linkage", "SIM–Biometric ID Linkage"),
]


def _clean(val):
    """Return a clean string, or None for NaN/empty."""
    if val is None:
        return None
    if isinstance(val, float) and math.isnan(val):
        return None
    s = str(val).strip()
    return s or None


def _score(val):
    """Return 0/1/2 int, or None if not scored."""
    if val is None or (isinstance(val, float) and math.isnan(val)):
        return None
    try:
        return int(round(float(val)))
    except (TypeError, ValueError):
        return None


def parse_legend(viz_xlsx):
    """Map free-text column -> {0,1,2: description} from the Legend sheet."""
    rules = {}
    try:
        lg = pd.read_excel(viz_xlsx, sheet_name="Legend")
    except Exception:
        return rules
    for _, row in lg.iterrows():
        vals = list(row.values)
        if not vals:
            continue
        col = _clean(vals[0])
        raw = _clean(vals[-1])  # "Scoring_Rules" e.g. "2=Adopted; 1=Draft; 0=None"
        if not col or not raw:
            continue
        mapping = {}
        for part in str(raw).split(";"):
            if "=" in part:
                k, _, v = part.partition("=")
                k = k.strip()
                if k in {"0", "1", "2"}:
                    mapping[k] = v.strip()
        if mapping:
            rules[col] = mapping
    return rules


def build_canonical_lookup(canonical_xlsx):
    """normalized country -> {region, region_specific, sources:{key: text}}.

    Region and per-indicator source references come from the canonical
    scorecard_main.xlsx (UN_194 sheet). Read only -- never written back.
    Each indicator's source column is ``<text_field>_Source``.
    """
    lookup = {}
    try:
        df = pd.read_excel(canonical_xlsx, sheet_name="UN_194")
    except Exception as exc:
        print(f"  ! Could not read canonical data from {canonical_xlsx}: {exc}")
        return lookup
    broad = "Region - Broad"
    specific = "Region - Specific"
    for _, row in df.iterrows():
        name = _clean(row.get("Country"))
        if not name:
            continue
        sources = {}
        for short, _score_col, text_col, _label in INDICATORS:
            sources[short] = _clean(row.get(text_col + "_Source"))
        lookup[_norm_key(name)] = {
            "region": _clean(row.get(broad)),
            "region_specific": _clean(row.get(specific)),
            "sources": sources,
        }
    return lookup


def _norm_key(name):
    """Normalized join/match key for a country name."""
    if normalize_country:
        try:
            _, normalized, _iso = normalize_country(str(name))
            if normalized:
                return str(normalized).strip().lower()
        except Exception:
            pass
    return str(name).strip().lower()


def _iso3(name):
    """Best-effort ISO 3166-1 alpha-3 code for Plotly's choropleth.

    ``normalize_country`` yields alpha-2; convert to alpha-3 via pycountry.
    Fall back to a direct pycountry name lookup (fuzzy) if needed.
    """
    alpha2 = None
    if normalize_country:
        try:
            _, _normalized, iso = normalize_country(str(name))
            if iso and len(str(iso).strip()) == 2:
                alpha2 = str(iso).strip().upper()
        except Exception:
            pass
    if alpha2 and pycountry:
        rec = pycountry.countries.get(alpha_2=alpha2)
        if rec:
            return rec.alpha_3
    if pycountry:
        try:
            matches = pycountry.countries.search_fuzzy(str(name))
            if matches:
                return matches[0].alpha_3
        except Exception:
            pass
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--viz-xlsx", default=VIZ_XLSX)
    ap.add_argument("--canonical-xlsx", default=CANONICAL_XLSX)
    ap.add_argument("--out", default=OUT_JSON)
    args = ap.parse_args()

    if not os.path.exists(args.viz_xlsx):
        raise SystemExit(f"Visualization workbook not found: {args.viz_xlsx}")

    print(f"Reading visualization data: {args.viz_xlsx}")
    sc = pd.read_excel(args.viz_xlsx, sheet_name="Scorecard")
    legend = parse_legend(args.viz_xlsx)
    canon = build_canonical_lookup(args.canonical_xlsx)

    # Source verification date (max Last_Verified_Timestamp), best effort.
    source_date = None
    if "Last_Verified_Timestamp" in sc.columns:
        ts = sc["Last_Verified_Timestamp"].dropna().astype(str)
        if len(ts):
            source_date = sorted(ts)[-1]

    countries = []
    missing_iso = []
    missing_region = []
    for _, row in sc.iterrows():
        name = _clean(row.get("Country"))
        if not name:
            continue
        key = _norm_key(name)
        iso = _iso3(name)
        if not iso:
            missing_iso.append(name)
        reg = canon.get(key, {})
        region = reg.get("region")
        if not region:
            missing_region.append(name)

        scores = {}
        text = {}
        for short, score_col, text_col, _label in INDICATORS:
            scores[short] = _score(row.get(score_col))
            text[short] = _clean(row.get(text_col))

        # "Documented" = how many indicators carry a free-text justification.
        # This varies country-to-country and is the meaningful completeness
        # signal (the file's Data_Completeness_% is a uniform 100).
        documented = sum(1 for v in text.values() if v)
        sources = reg.get("sources", {})

        protection = _score(row.get("Protection_Score"))
        risk = row.get("Risk_Index")
        risk = (
            None
            if (risk is None or (isinstance(risk, float) and math.isnan(risk)))
            else int(round(float(risk)))
        )
        completeness = row.get("Data_Completeness_%")
        completeness = (
            None
            if (
                completeness is None
                or (isinstance(completeness, float) and math.isnan(completeness))
            )
            else int(round(float(completeness)))
        )

        countries.append(
            {
                "country": name,
                "iso3": iso,
                "region": region,
                "region_specific": reg.get("region_specific"),
                "protection_score": protection,
                "risk_index": risk,
                "completeness": completeness,
                "documented": documented,
                "scores": scores,
                "text": text,
                "sources": sources,
            }
        )

    indicators_meta = [
        {
            "key": short,
            "label": label,
            "score_field": score_col,
            "text_field": text_col,
            "rules": legend.get(text_col, {}),
        }
        for (short, score_col, text_col, label) in INDICATORS
    ]

    region_set = sorted({c["region"] for c in countries if c["region"]})

    payload = {
        "meta": {
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "source_file": os.path.basename(args.viz_xlsx),
            "source_verified": source_date,
            "country_count": len(countries),
            "scored_country_count": sum(
                1 for c in countries if c["protection_score"] is not None
            ),
            "fully_documented_count": sum(
                1 for c in countries if c["documented"] == len(INDICATORS)
            ),
            "indicator_count": len(INDICATORS),
            "protection_score_range": [0, 20],
            "indicators": indicators_meta,
            "regions": region_set,
            "note": (
                "Visualization dataset derived from the project's designated "
                "'clean visualization' workbook. Source-URL validation is an "
                "ongoing, separate workflow; figures are point-in-time and may "
                "be revised. Canonical pipeline data lives in scorecard_main.xlsx."
            ),
        },
        "countries": countries,
    }

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")  # keep end-of-file-fixer (pre-commit) happy

    print(f"Wrote {args.out}")
    print(
        f"  countries={len(countries)} "
        f"scored={payload['meta']['scored_country_count']} "
        f"regions={len(region_set)} indicators={len(indicators_meta)}"
    )
    if missing_iso:
        print(
            f"  ! {len(missing_iso)} without ISO-3 (map may skip): "
            f"{', '.join(missing_iso[:8])}{'...' if len(missing_iso) > 8 else ''}"
        )
    if missing_region:
        print(
            f"  ! {len(missing_region)} without region: "
            f"{', '.join(missing_region[:8])}{'...' if len(missing_region) > 8 else ''}"
        )


if __name__ == "__main__":
    main()
