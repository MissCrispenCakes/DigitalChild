#!/usr/bin/env python3
"""Build the "Source Transparency Watch" dataset for the GRIMdata site.

Tracks whether peer organisations (the aggregators behind our scorecard
indicators, plus related rights / data-transparency bodies) are adopting
primary-source / open-data transparency, and *when* they did.

Engine: the Internet Archive Wayback **CDX API**. For each monitored domain we
query the capture history for URLs matching transparency-signal patterns
(machine-readable datasets, per-document/legal-file manifests, API endpoints,
open-data / structural sections) and record the **first archived appearance**
of each — a reproducible, bot-friendly proxy for "first offered publicly".

Read-only: writes only docs/transparency-watch/data/transparency.json (the data
contract the public page renders). No source/canonical files are touched.

Usage:
    python utils/build_transparency_watch_data.py
    python utils/build_transparency_watch_data.py --only unctad,hdt --out PATH

Caveat: Wayback coverage is incomplete, so a first-seen date is an *upper bound*
on adoption (they may have offered it earlier, unarchived). Absence of a signal
is not proof it never existed. The page states this.
"""
import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone

import requests

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_JSON = os.path.join(
    REPO_ROOT, "docs", "transparency-watch", "data", "transparency.json"
)

# Monitored sources: indicator aggregators + peer rights/transparency bodies.
SOURCES = [
    {
        "key": "unctad",
        "name": "UNCTAD — Cyberlaw / Data Protection Tracker",
        "domains": ["unctad.org", "storage.unctad.org"],
        "topic": r"cyberlaw|data.?protection|privacy|e-?commerce|legislation",
        "homepage": "https://unctad.org/page/data-protection-and-privacy-legislation-worldwide",
    },
    {
        "key": "unesco_ai",
        "name": "UNESCO — AI Ethics / Observatory",
        "domains": ["unesco.org"],
        "topic": r"artificial.?intelligence|/ai|ethics|recommendation|observatory",
        "homepage": "https://www.unesco.org/en/artificial-intelligence",
    },
    {
        "key": "ilga",
        "name": "ILGA World",
        "domains": ["ilga.org"],
        "topic": r"sexual.?orientation|lgb|sogi|criminali|law|map",
        "homepage": "https://database.ilga.org/en",
    },
    {
        "key": "hdt",
        "name": "Human Dignity Trust",
        "domains": ["humandignitytrust.org"],
        "topic": r"country-profile|criminali|lgbt|map-of|the-law",
        "homepage": "https://www.humandignitytrust.org/lgbt-the-law/map-of-criminalisation/",
    },
    {
        "key": "privacy_intl",
        "name": "Privacy International",
        "domains": ["privacyinternational.org"],
        "topic": r"biometric|sim|surveillance|data|privacy",
        "homepage": "https://privacyinternational.org/",
    },
    {
        "key": "oecd_ai",
        "name": "OECD.AI Policy Observatory",
        "domains": ["oecd.ai"],
        "topic": r"ai|policy|observatory|dashboard",
        "homepage": "https://oecd.ai/",
    },
    {
        "key": "freedom_house",
        "name": "Freedom House",
        "domains": ["freedomhouse.org"],
        "topic": r"freedom|net|democracy|country|report",
        "homepage": "https://freedomhouse.org/",
    },
    {
        "key": "access_now",
        "name": "Access Now",
        "domains": ["accessnow.org"],
        "topic": r"data|rights|digital|shutdown|tracker",
        "homepage": "https://www.accessnow.org/",
    },
    {
        "key": "dla_piper_dp",
        "name": "DLA Piper — Data Protection Laws of the World",
        "domains": ["dlapiperdataprotection.com"],
        "topic": r"data.?protection|privacy|law|country",
        "homepage": "https://www.dlapiperdataprotection.com/",
    },
]

# URL fragments that are tracking / framework / asset / artifact noise.
NOISE = re.compile(
    r"gtm[./]|gtag|googletagmanager|google-analytics|doubleclick|facebook|"
    r"hotjar|recaptcha|/wp-content/|/wp-includes/|/wp-json/|jquery|bootstrap|"
    r"\.min\.(js|css)|/fonts?/|cookie|consent|/cdn-cgi/|analytics|pixel|"
    r"robots\.txt|favicon|facetwp|/packed/|/https?:/"  # last: double-scheme redirect artifact
)
# Page assets (never a dataset / API / document signal).
STATIC_ASSET = re.compile(r"\.(js|css|png|jpe?g|svg|gif|ico|woff2?|ttf|eot|map)(\?|$)")

# (signal type, human label, regex on the lowercased captured URL).
# Order matters: first match wins when classifying a URL.
PATTERNS = [
    ("document", "Per-document link manifest", r"document[_-]links"),
    ("dataset", "CSV dataset download", r"\.csv($|\?)"),
    ("dataset", "Excel dataset download", r"\.xlsx?($|\?)"),
    (
        "dataset",
        "“Get the data” export",
        r"get[-_]the[-_]data|/get-data|/download-data",
    ),
    ("api", "API endpoint", r"//api\.|/api/|/v1/|/v2/|/rest/|/graphql"),
    ("api", "JSON data endpoint", r"/data/[^?]*\.json($|\?)|/data\.json"),
    ("document", "Bulk downloads section", r"/downloads?/"),
    (
        "structure",
        "Open-data / data portal",
        r"open[-_]data|data[-_]portal|/datasets?/",
    ),
    ("structure", "XML sitemap", r"sitemap[^/]*\.xml"),
]
# One combined CDX filter so each domain is a single query.
COMBINED_RE = "|".join("(" + p[2] + ")" for p in PATTERNS)

SESSION = requests.Session()
SESSION.headers["User-Agent"] = (
    "Mozilla/5.0 (compatible; DigitalChild-TransparencyTicker/0.1)"
)
CDX = "http://web.archive.org/cdx/search/cdx"


def ymd(t):
    return f"{t[:4]}-{t[4:6]}-{t[6:8]}" if len(t) >= 8 else t


def cdx_query(domain, **params):
    p = {
        "url": domain,
        "matchType": "domain",
        "output": "json",
        "fl": "timestamp,original,statuscode",
        "collapse": "urlkey",
    }
    p.update(params)
    # Retry on transient failures (large CDX responses can end prematurely).
    for attempt in range(3):
        try:
            r = SESSION.get(CDX, params=p, timeout=90)
            if r.status_code != 200:  # 5xx/504 are transient failures, not "empty"
                raise requests.HTTPError(f"HTTP {r.status_code}")
            if not r.text.strip():
                return []  # genuine clean-empty result
            data = r.json()
            return data[1:] if data and len(data) > 1 else []
        except Exception as e:  # noqa: BLE001 - network best-effort
            if attempt == 2:
                print(f"    ! CDX error for {domain} (gave up): {e}")
                return None  # signal a failed query (distinct from clean-empty [])
            time.sleep(2)
    return None


def is_real_api(low):
    """True only for genuine API roots — an ``api.`` host or ``/api`` (or
    ``/v1`` etc.) right after the host — not deep page-internal AJAX widgets
    like ``/country-profile/x/api/v1``."""
    return bool(
        re.search(r"//api\.", low)
        or re.match(r"https?://[^/]+/api/", low)
        or re.match(r"https?://[^/]+/(v[12]|rest|graphql)/", low)
    )


def classify(url):
    low = url.lower()
    for stype, label, rx in PATTERNS:
        if re.search(rx, low):
            return stype, label
    return None, None


def build_source(src):
    print(f"  • {src['key']}: querying {', '.join(src['domains'])} ...")
    topic = re.compile(src.get("topic", r"(?!)"))  # never-match if no topic
    signals = {}
    all_dates = []
    failed_domains = 0
    for domain in src["domains"]:
        rows = cdx_query(
            domain, filter="original:.*(" + COMBINED_RE + ").*", limit="4000"
        )
        if rows is None:  # query failed (e.g. domain too large to scan reliably)
            failed_domains += 1
            continue
        for ts, original, _status in rows:
            low = original.lower()
            # Skip noise, page assets, and mangled multi-URL capture artifacts
            # (a captured URL embedding a second scheme, e.g. .../77https:/...;
            # Wayback may collapse "://" to ":/", so count scheme tokens).
            if (
                ts == "ERR"
                or NOISE.search(low)
                or STATIC_ASSET.search(low)
                or len(re.findall(r"https?:/", low)) > 1
            ):
                continue
            stype, label = classify(original)
            if not label:
                continue
            if stype == "api" and not is_real_api(low):
                continue
            date = ymd(ts)
            all_dates.append(date)
            on_topic = bool(topic.search(original.lower()))
            cur = signals.get(label)
            if cur is None:
                signals[label] = {
                    "type": stype,
                    "label": label,
                    "first_seen": date,
                    "count": 1,
                    "example": original,
                    "topical_first_seen": None,
                    "topical_example": None,
                }
                cur = signals[label]
            else:
                cur["count"] += 1
                if date < cur["first_seen"]:
                    cur["first_seen"] = date
                    cur["example"] = original
            if on_topic and (
                cur["topical_first_seen"] is None or date < cur["topical_first_seen"]
            ):
                cur["topical_first_seen"] = date
                cur["topical_example"] = original

    # Prefer the on-topic example/date for display when we have one.
    for s in signals.values():
        s["topical"] = s["topical_first_seen"] is not None
        if s["topical"]:
            s["display_date"] = s["topical_first_seen"]
            s["display_url"] = s["topical_example"]
        else:
            s["display_date"] = s["first_seen"]
            s["display_url"] = s["example"]

    sig_list = sorted(
        signals.values(), key=lambda s: (not s["topical"], s["display_date"])
    )
    return {
        "key": src["key"],
        "name": src["name"],
        "domains": src["domains"],
        "homepage": src["homepage"],
        "first_signal": min(all_dates) if all_dates else None,
        "last_signal": max(all_dates) if all_dates else None,
        "query_ok": failed_domains < len(src["domains"]),
        "signals": sig_list,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default=OUT_JSON)
    ap.add_argument("--only", help="comma-separated source keys to limit to")
    args = ap.parse_args()

    only = set(args.only.split(",")) if args.only else None
    sources = [s for s in SOURCES if not only or s["key"] in only]

    print(f"Building transparency watch for {len(sources)} sources...")
    built = [build_source(s) for s in sources]

    # Global timeline = every signal's first-seen, newest first (the "ticker").
    timeline = []
    for s in built:
        for sig in s["signals"]:
            timeline.append(
                {
                    "date": sig["display_date"],
                    "source": s["name"],
                    "source_key": s["key"],
                    "type": sig["type"],
                    "label": sig["label"],
                    "url": sig["display_url"],
                    "topical": sig["topical"],
                }
            )
    timeline.sort(key=lambda x: x["date"], reverse=True)

    payload = {
        "meta": {
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "source_count": len(built),
            "signal_types": ["dataset", "document", "api", "structure"],
            "method": (
                "First archived appearance (Internet Archive Wayback CDX) of "
                "transparency-signal URLs per domain."
            ),
            "caveat": (
                "Wayback coverage is incomplete: a first-seen date is an UPPER "
                "BOUND on public adoption (it may have appeared earlier, "
                "unarchived), and absence of a signal is not proof it never "
                "existed. Treat as indicative, verify before citing."
            ),
        },
        "sources": built,
        "timeline": timeline,
    }

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"\nWrote {args.out}")
    print(f"  sources={len(built)} timeline_events={len(timeline)}")
    for s in built:
        print(
            f"  - {s['key']:14} signals={len(s['signals'])} "
            f"span={s['first_signal']}..{s['last_signal']}"
        )


if __name__ == "__main__":
    sys.exit(main())
