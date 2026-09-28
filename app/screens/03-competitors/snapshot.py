"""Ad Library snapshots for the competitors screen: page ids in, one signal row per ad out.

A snapshot is `fixtures/snapshots/<brand>/<YYYY-MM-DD>.json`. It holds no competitor ad
text, no media and no faces: per ad it keeps the page, the ad id and its public Ad Library
link, start and end dates, days live, format, call to action, platforms, the number of
versions Meta groups under it, the kind of first line (question, number, first person,
quote, offer, problem, statement) and the tags that rules in this file set, each with the
word that set it. For the brand's own page the first line is kept too (it is our copy).

Pull: `plan(brand)` returns the pages, the item cap and the Apify estimate before anything
runs. `pull(brand, live=True)` runs curious_coder~facebook-ads-library-scraper through
app/connectors/apify.py, which checks the per-run and weekly caps in the brand's
config/apify.json and reserves and settles the run in the spend ledger. Pages without a
page id are skipped and listed: the Ad Library is read by page id only, never by keyword.
Mock mode reads the connector fixture and writes nothing unless `write=True`.

CLI: python3 app/screens/03-competitors/snapshot.py --brand bombas --plan
     python3 app/screens/03-competitors/snapshot.py --brand bombas --live
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BRAIN = ROOT / "app" / "brain"
SNAPSHOTS = HERE / "fixtures" / "snapshots"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

ACTOR = "curious_coder~facebook-ads-library-scraper"
PAGE_URL = ("https://www.facebook.com/ads/library/?active_status={status}&ad_type=all&country={country}"
            "&view_all_page_id={page_id}&search_type=page")
AD_URL = "https://www.facebook.com/ads/library/?id={id}"

# Angle tags: the first matching word sets the tag and is kept as the reason. Rules, not judgement.
ANGLES = [
    ("relief", "Relief and health", ["relief", "pain", "plantar", "swelling", "circulation", "pots", "blood pooling",
                                     "doctor", "medical", "nurse", "recovery", "aching", "sore"]),
    ("comfort", "Comfort", ["comfort", "comfy", "soft", "cushion", "butter", "cozy", "cosy", "plush"]),
    ("durability", "Durability and guarantee", ["lifetime", "guarantee", "durable", "durability", "holes", "last longer",
                                                "built to last", "wear out", "warranty"]),
    ("performance", "Performance and sport", ["running", "run ", "runner", "hike", "hiking", "trail", "training",
                                              "workout", "performance", "sweat", "moisture", "blister", "athlete", "marathon"]),
    ("fit", "Fit that stays put", ["stay up", "stays up", "slip", "grip", "seamless", "no-show", "no show", "fit"]),
    ("material", "Material story", ["merino", "wool", "cotton", "bamboo", "organic", "fabric", "cashmere", "linen"]),
    ("style", "Style and new colours", ["style", "color", "colour", "new arrival", "collection", "look great", "fashion",
                                        "pattern", "drop", "limited"]),
    ("proof", "Reviews and proof", ["review", "testimonial", "social proof", "5-star", "5 star", "stars", "rated", "best seller", "bestseller",
                                    "customers", "loved by", "award", "tested"]),
    ("giving", "Giving and mission", ["donate", "donation", "giving", "give back", "one purchased", "homeless", "mission"]),
    ("gifting", "Gifting and season", ["gift", "holiday", "stocking", "christmas", "father's day", "mother's day",
                                       "fall ", "winter", "cold weather"]),
]
OFFERS = [
    ("percent_off", "Percent off", re.compile(r"\b\d{1,2}\s?% off\b")),
    ("free_shipping", "Free shipping", re.compile(r"\bfree shipping\b")),
    ("bundle", "Bundle or pack saving", re.compile(r"\b(bundle|pack(s)? (and|&) save|buy \d+|save up to|multi-?pack)\b")),
    ("code", "Promo code", re.compile(r"\bcode [a-z0-9]{3,}\b")),
    ("sale", "Sale event", re.compile(r"\b(sale|black friday|cyber monday|clearance)\b")),
    ("guarantee", "Guarantee", re.compile(r"\b(guarantee|guaranteed|warranty|free returns)\b")),
    ("gift_with_purchase", "Gift with purchase", re.compile(r"\b(free gift|gift with purchase)\b")),
]
FIRST_LINE = [
    ("question", lambda s: "?" in s[:140]),
    ("quote", lambda s: s[:1] in "\"“'"),
    ("number", lambda s: bool(re.match(r"^\W*\d", s))),
    ("first_person", lambda s: bool(re.match(r"^\W*(i |i'm |i've |my |me )", s.lower()))),
    ("problem", lambda s: bool(re.match(r"^\W*(tired of|sick of|stop |no more|why do|say goodbye|goodbye)", s.lower()))),
    ("offer", lambda s: bool(re.search(r"\d+% off|free shipping|\bsale\b|\bcode\b", s.lower()))),
]
FIRST_LINE_LABEL = {"question": "Question", "quote": "Quote or testimonial", "number": "Number first",
                    "first_person": "First person", "problem": "Problem first", "offer": "Offer first",
                    "statement": "Plain statement", "none": "No text (catalog)"}
FORMATS = {"video": "video", "image": "image", "carousel": "carousel", "dco": "dynamic", "dpa": "catalog",
           "multi_images": "carousel", "multi_medias": "carousel", "page_like": "image", "event": "image"}
FORMAT_LABEL = {"video": "Video", "image": "Static image", "carousel": "Carousel", "dynamic": "Dynamic creative",
                "catalog": "Catalog", "other": "Other"}
TEMPLATE = re.compile(r"\{\{\s*product\.[a-z_]+\s*\}\}")
CREATOR = ["i wore", "honest review", "i tried", "my feet", "unboxing", "pov", "obsessed", "game changer", "@"]


def config(brand: str, root: Path = BRAIN) -> dict:
    return json.loads((root / brand / "config" / "apify.json").read_text(encoding="utf-8"))


def _clean(text) -> str:
    return re.sub(r"\s+", " ", str(text or "")).strip()


def first_line(body: str) -> str:
    body = str(body or "").strip()
    line = re.split(r"[\n\r]+", body, maxsplit=1)[0]
    m = re.match(r"(.{12,}?[.!?])(\s|$)", line)
    return _clean(m.group(1) if m else line)[:160]


def line_kind(line: str) -> str:
    if not line or TEMPLATE.search(line):
        return "none"
    for k, fn in FIRST_LINE:
        if fn(line):
            return k
    return "statement"


def tag_angles(text: str) -> list[dict]:
    t = f" {text.lower()} "
    out = []
    for key, _label, words in ANGLES:
        for w in words:
            if w in t:
                out.append({"tag": key, "word": w.strip()})
                break
    return out


def tag_offers(text: str) -> list[dict]:
    t = text.lower()
    out = []
    for key, _label, rx in OFFERS:
        m = rx.search(t)
        if m:
            out.append({"tag": key, "word": m.group(0)})
    return out


def _date(v) -> str | None:
    if v in (None, ""):
        return None
    if isinstance(v, (int, float)):
        return dt.datetime.fromtimestamp(int(v), dt.timezone.utc).date().isoformat()
    s = str(v)
    return s[:10] if re.match(r"\d{4}-\d{2}-\d{2}", s) else None


def ad_row(item: dict, role: str, captured: dt.date) -> dict:
    snap = item.get("snapshot") or {}
    body = snap.get("body")
    body = body.get("text") if isinstance(body, dict) else body
    cards = snap.get("cards") or []
    if not body and cards:
        body = (cards[0] or {}).get("body")
    title = snap.get("title") or ((cards[0] or {}).get("title") if cards else "") or ""
    text = _clean(f"{body or ''} {title}")
    fmt_raw = str(snap.get("display_format") or "other").lower()
    fmt = FORMATS.get(fmt_raw, "other")
    start, end = _date(item.get("start_date")), _date(item.get("end_date"))
    last = dt.date.fromisoformat(end) if end and not item.get("is_active") else captured
    days = (last - dt.date.fromisoformat(start)).days if start else None
    line = first_line(body or "")
    ad_id = str(item.get("ad_archive_id") or item.get("ad_id") or "")
    link = str(snap.get("link_url") or "")
    row = {"page_id": str(item.get("page_id") or ""), "page": item.get("page_name") or "", "role": role,
           "ad_id": ad_id, "url": AD_URL.format(id=ad_id) if ad_id.isdigit() else item.get("url"),
           "start": start, "end": end, "active": bool(item.get("is_active")), "days_live": days,
           "format": fmt, "cta": _clean(snap.get("cta_text") or snap.get("cta_type") or "") or None,
           "platforms": sorted({str(p).lower() for p in item.get("publisher_platform") or []}),
           "versions": int(item.get("collation_count") or 1),
           "link_domain": re.sub(r"^https?://(www\.)?", "", link).split("/")[0] or None,
           "first_line_kind": line_kind(line), "first_line_words": len(line.split()) if line else 0,
           "angles": tag_angles(text), "offers": tag_offers(text),
           "creator": any(c in text.lower() for c in CREATOR)}
    if role == "self":
        row["first_line"] = line
    return row


def summarise(rows: list[dict]) -> dict:
    """Page level numbers from the ad rows. Computed on read so the rules can change without a re-pull."""
    days = sorted(r["days_live"] for r in rows if r["days_live"] is not None)
    med = None
    if days:
        mid = len(days) // 2
        med = days[mid] if len(days) % 2 else round((days[mid - 1] + days[mid]) / 2, 1)
    n = len(rows)
    return {"ads": n, "active": sum(r["active"] for r in rows),
            "formats": dict(Counter(r["format"] for r in rows)),
            "median_days": med, "longest_days": days[-1] if days else None,
            "offer_share": round(sum(1 for r in rows if r["offers"]) / n, 3) if n else None,
            "cta": Counter(r["cta"] for r in rows if r["cta"]).most_common(1)[0][0] if any(r["cta"] for r in rows) else None,
            "first_lines": dict(Counter(r["first_line_kind"] for r in rows)),
            "angles": dict(Counter(a["tag"] for r in rows for a in r["angles"])),
            "offers": dict(Counter(o["tag"] for r in rows for o in r["offers"])),
            "creator": sum(1 for r in rows if r["creator"])}


def plan(brand: str, root: Path = BRAIN) -> dict:
    """What a pull would read and cost, before it runs."""
    from app.connectors import apify
    cfg = config(brand, root)
    ad = cfg.get("meta_ad_library") or {}
    pages = ad.get("pages") or []
    ready = [p for p in pages if p.get("page_id")]
    skipped = [p["name"] for p in pages if not p.get("page_id")]
    per = int(ad.get("limit_per_source") or 100)
    max_items = per * max(len(ready), 1)
    budget = cfg.get("budget") or {}
    est = apify.estimate_usd(ad.get("actor") or ACTOR, max_items)
    try:
        client = apify.ApifyClient(mode="live", brand=brand, budget=budget)
        spent, token = client.week_spent_usd(), True
    except apify.ApifyError:
        spent, token = None, False
    weekly, per_run = budget.get("max_usd_per_week"), budget.get("max_usd_per_run")
    fits = est <= (per_run or 0) and (spent is None or weekly is None or spent + est <= weekly)
    return {"actor": ad.get("actor") or ACTOR, "pages": [{"name": p["name"], "page_id": p["page_id"], "role": p.get("role")}
                                                         for p in ready],
            "skipped": skipped, "skipped_reason": "no page id; the Ad Library is read by page id only",
            "limit_per_page": per, "max_items": max_items, "estimate_usd": est,
            "cap_per_run_usd": per_run, "cap_week_usd": weekly, "week_spent_usd": None if spent is None else round(spent, 2),
            "fits_caps": bool(fits), "token": token}


def build(brand: str, items: list[dict], pages: list[dict], captured: dt.date, run: dict) -> dict:
    roles = {str(p["page_id"]): p.get("role", "competitor") for p in pages if p.get("page_id")}
    names = {str(p["page_id"]): p["name"] for p in pages if p.get("page_id")}
    rows = [ad_row(it, roles[str(it.get("page_id"))], captured) for it in items if str(it.get("page_id")) in roles]
    rows.sort(key=lambda r: (r["role"] != "self", r["page"], -(r["days_live"] or 0), r["ad_id"]))
    by_page = {}
    for pid, name in names.items():
        mine = [r for r in rows if r["page_id"] == pid]
        by_page[pid] = {"name": name, "page_name": mine[0]["page"] if mine else None, "role": roles[pid],
                        "pulled": bool(mine)}
    return {"brand": brand, "captured_at": captured.isoformat(), "actor": run.get("actor"), "run_id": run.get("run_id"),
            "mode": run.get("mode"), "usd": run.get("usd"), "items": len(items), "kept": len(rows),
            "pages": by_page, "note": "Signals only. No competitor ad text, media or faces are stored.", "ads": rows}


def pull(brand: str, live: bool = False, write: bool | None = None, root: Path = BRAIN, today: dt.date | None = None) -> dict:
    from app.connectors import apify
    cfg = config(brand, root)
    ad = cfg["meta_ad_library"]
    pages = [p for p in ad.get("pages") or [] if p.get("page_id")]
    status, country = ad.get("active_status", "active"), ad.get("country", "US")
    per = int(ad.get("limit_per_source") or 100)
    client = apify.ApifyClient(mode="live" if live else "mock", brand=brand, budget=cfg.get("budget"), today=today)
    actor_input = {"urls": [{"url": PAGE_URL.format(status=status, country=country, page_id=p["page_id"])} for p in pages],
                   "scrapeAdDetails": bool(ad.get("scrape_ad_details", False)), "limitPerSource": per,
                   "scrapePageAds.activeStatus": status, "scrapePageAds.countryCode": country}
    items = client.run(ad.get("actor") or ACTOR, actor_input, per * len(pages), lane="adlibrary-competitors")
    snap = build(brand, items, pages, client.today, client.last_run or {})
    if write if write is not None else live:
        out = SNAPSHOTS / brand / f"{snap['captured_at']}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(snap, indent=0, ensure_ascii=False), encoding="utf-8")
        snap["path"] = str(out.relative_to(ROOT))
    return snap


def snapshots(brand: str, folder: Path = SNAPSHOTS) -> list[Path]:
    d = folder / brand
    return sorted(d.glob("????-??-??.json")) if d.is_dir() else []


def load(brand: str, folder: Path = SNAPSHOTS, before: str | None = None) -> dict | None:
    """The latest snapshot (or the latest strictly before a date), or None."""
    paths = [p for p in snapshots(brand, folder) if before is None or p.stem < before]
    return json.loads(paths[-1].read_text(encoding="utf-8")) if paths else None


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--brand", default="bombas")
    ap.add_argument("--plan", action="store_true", help="show pages, cap and estimate; run nothing")
    ap.add_argument("--live", action="store_true", help="run the actor through the capped connector and write a snapshot")
    ns = ap.parse_args()
    if ns.plan or not ns.live:
        print(json.dumps(plan(ns.brand), indent=1))
    else:
        s = pull(ns.brand, live=True)
        print(json.dumps({k: v for k, v in s.items() if k != "ads"}, indent=1))
