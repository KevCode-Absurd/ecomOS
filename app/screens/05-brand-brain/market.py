"""Competitors and market for the brand brain screen: the Ad Library pages against the brand, and what to make next.

Reads only the brain (app/brain/<brand>/) and the brand's Apify config (config/apify.json). Never pulls.
A re-pull is only estimated here (app/connectors/apify.py prices, by page id, within the caps); the button
on the screen logs a decision, and the connector runs it later inside its ledger.

What it computes, all in code, brand-agnostic:
- `pages(brain)`: one row per configured Ad Library page (the brand's own page from role `self`, the
  competitors from role `competitor`), joined to the `competitors` records the Ad Library extractor
  wrote (formats, hook forms, run lengths, offers, platforms) and the descriptive competitor records
  (positioning, price band, what they push, angles). Shares are share of ads seen on that page.
- `gaps(brain)`: the format and hook-form gaps between the brand and the competitor median, each with
  the numbers, the baseline and the rule, in the audit evidence shape. audit.py turns them into findings.
- `repull(brain)`: what a fresh pull would cost, against the per-run and weekly caps, and the age of the
  current snapshot. Unavailable when the config or the price is missing, never 0.

Competitor ads are signals, never copied. Nothing here stores ad text, logos, products or faces; the
records hold counts and short labels only.
"""
from __future__ import annotations

import datetime as dt
import importlib.util
import json
import re
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parents[1]

FORMATS = ["video", "image", "carousel", "dco", "dpa"]
FORMAT_LABEL = {"video": "Video", "image": "Static image", "carousel": "Carousel", "dco": "Dynamic creative", "dpa": "Catalog (DPA)"}
FORMAT_ALIAS = {"catalog": "dpa", "dynamic": "dco", "static": "image", "photo": "image"}
HOOKS = ["statement", "question", "first_person", "number", "offer"]
HOOK_LABEL = {"statement": "Statement", "question": "Question", "first_person": "First person", "number": "Number led", "offer": "Offer led"}
MIN_ADS_FOR_MEDIAN = 20        # a competitor page with fewer ads seen does not set the median
GAP_MIN_THEM_SHARE = 0.15      # a format or hook form counts as a gap only when the competitor median share is at least this
GAP_RATIO = 0.5                # ... and the brand's share is under half of it
LONG_RUNNER_GAP_RATIO = 0.5    # long-runner share gap: ours under half of the competitor median
SNAPSHOT_STALE_DAYS = 7        # room spec: competitor snapshot stale after 7 days


def _apify_mod():
    p = APP / "connectors" / "apify.py"
    if not p.is_file():
        return None
    name = "ecomos_apify_bb"
    if name in sys.modules:
        return sys.modules[name]
    try:
        spec = importlib.util.spec_from_file_location(name, p)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod
        spec.loader.exec_module(mod)
        return mod
    except Exception:  # noqa: BLE001
        return None


def config(brain) -> dict:
    p = brain.dir / "config" / "apify.json"
    if not p.is_file():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", (name or "").lower()).strip("_")


def _norm_counts(raw: dict | None, keys: list[str], alias: dict | None = None) -> dict:
    out = {k: 0 for k in keys}
    for k, v in (raw or {}).items():
        kk = (alias or {}).get(k, k)
        if kk in out and isinstance(v, (int, float)):
            out[kk] += v
    return out


def _shares(counts: dict, total: int | None) -> dict:
    if not total:
        return {k: None for k in counts}
    return {k: round(v / total, 3) for k, v in counts.items()}


def _age(date_s: str | None, today: dt.date) -> int | None:
    if not date_s:
        return None
    try:
        return (today - dt.date.fromisoformat(str(date_s)[:10])).days
    except ValueError:
        return None


def pages(brain) -> dict:
    cfg = config(brain).get("meta_ad_library") or {}
    conf_pages = cfg.get("pages") or []
    proposed = cfg.get("proposed_pages") or []
    # records the Ad Library extractor wrote, keyed by page id
    pulled: dict[str, dict] = {}
    for r in brain.records("competitors"):
        v = r.get("value")
        if isinstance(v, dict) and v.get("page_id") and "formats" in v and isinstance(v["formats"], dict):
            pulled[str(v["page_id"])] = r
    signals: dict[str, dict] = {}   # learnings adlib_<page>_formats by page name slug
    for r in brain.records("learnings"):
        v = r.get("value")
        if isinstance(v, dict) and v.get("page") and isinstance(v.get("formats"), dict) and v.get("signal_only"):
            signals[_slug(v["page"])] = r
    described: dict[str, dict] = {}
    for r in brain.records("competitors"):
        v = r.get("value")
        if isinstance(v, dict) and v.get("page_id") and "positioning" in v:
            described[str(v["page_id"])] = r
    reddit: dict[str, dict] = {}
    for r in brain.records("competitors"):
        v = r.get("value")
        if isinstance(v, dict) and "recommended_instead" in v and v.get("competitor"):
            reddit[_slug(v["competitor"])] = v
    patterns = next((r.get("value") for r in brain.records("learnings") if r.get("field") == "competitor_patterns" and isinstance(r.get("value"), dict)), {}) or {}
    own_hooks = next((r.get("value") for r in brain.records("learnings") if r.get("field") == "hook_types" and isinstance(r.get("value"), dict)), None)
    frame = next((r for r in brain.records("competitors") if r.get("field") == "competitor_frame"), None)
    lookalike = next((r for r in brain.records("competitors") if r.get("field") == "lookalike_page"), None)

    rows = []
    for cp in conf_pages:
        name, role, pid = cp.get("name"), cp.get("role") or "competitor", cp.get("page_id")
        slug = _slug(name)
        rec = pulled.get(str(pid)) if pid else None
        sig = signals.get(slug) or (signals.get(_slug(name + " socks")) if name else None)
        v = (rec or {}).get("value") or {}
        sv = (sig or {}).get("value") or {}
        formats_raw = v.get("formats") or sv.get("formats")
        hooks_raw = v.get("hook_types") or sv.get("hook_types")
        formats = _norm_counts(formats_raw, FORMATS, FORMAT_ALIAS) if formats_raw else None
        hooks = _norm_counts(hooks_raw, HOOKS) if hooks_raw else None
        ads_seen = v.get("ads_seen") or (sum(formats.values()) if formats else None)
        long30 = sv.get("long_runners_30d")
        desc = (described.get(str(pid)) or {}).get("value") or {}
        captured = (rec or sig or {}).get("date")
        red = reddit.get(slug) or next((x for k, x in reddit.items() if k and (k in slug or slug.startswith(k))), None)
        flags = []
        if red:
            flags.append({"key": "reddit", "text": f"Reddit recommends it instead in {red.get('recommended_instead')} threads"})
        if any(_slug(x) in slug or slug in _slug(x) for x in patterns.get("compression_overlap") or []):
            flags.append({"key": "overlap", "text": "fights us on the same product line"})
        if any(_slug(x) in slug or slug in _slug(x) for x in patterns.get("no_discount") or []):
            flags.append({"key": "no_discount", "text": "sells without a discount"})
        if any(_slug(x) in slug or slug in _slug(x) for x in patterns.get("heavy_dynamic") or []):
            flags.append({"key": "dynamic", "text": "leans on dynamic creative"})
        row = {
            "name": name, "role": role, "page_id": pid, "slug": slug,
            "ad_library_url": desc.get("ad_library_url") or (f"https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=US&view_all_page_id={pid}" if pid else None),
            "pulled": bool(rec or sig), "captured_at": captured if captured != "undated" else None, "age_days": _age(captured, brain.today),
            "ads_seen": ads_seen, "active_ads": v.get("active_ads"), "longest_run_days": v.get("longest_run_days"),
            "median_run_days": sv.get("median_run_days"), "long_runners_30d": long30,
            "long_runner_share": (round(long30 / ads_seen, 3) if isinstance(long30, (int, float)) and ads_seen else None),
            "formats": formats, "format_share": _shares(formats, ads_seen) if formats else None,
            "hooks": hooks, "hook_share": _shares(hooks, ads_seen) if hooks else None,
            "offers_seen": v.get("offers_seen") or [], "platforms": v.get("platforms") or [],
            "positioning": desc.get("positioning"), "price_band": desc.get("price_band_usd"), "what_they_push": desc.get("what_they_push"),
            "angles": desc.get("hook_types") or (list(own_hooks.keys()) if role == "self" and own_hooks else []),
            "flags": flags, "record_ids": [x["id"] for x in (rec, sig) if x] + ([described[str(pid)]["id"]] if pid and str(pid) in described else []),
        }
        row["verdict"] = _verdict(row)
        rows.append(row)
    rows.sort(key=lambda r: (r["role"] != "self", -(r["ads_seen"] or 0), r["name"] or ""))
    us = next((r for r in rows if r["role"] == "self"), None)
    them = [r for r in rows if r["role"] == "competitor" and r["pulled"]]
    return {"pages": rows, "us": us, "competitors_pulled": len(them), "competitors_configured": sum(1 for r in rows if r["role"] == "competitor"),
            "not_pulled": [r["name"] for r in rows if r["role"] == "competitor" and not r["pulled"]],
            "proposed": [{"name": p.get("name"), "score": p.get("score"), "reasons": [x.get("why") for x in p.get("reasons") or []], "next": p.get("next")} for p in proposed],
            "medians": medians(rows), "frame": {"text": frame.get("text"), "tier": frame.get("tier"), "id": frame.get("id")} if frame else None,
            "lookalike": {"text": lookalike.get("text"), "id": lookalike.get("id"), "page_id": (lookalike.get("value") or {}).get("page_id"), "date": lookalike.get("date")} if lookalike else None,
            "snapshot_age_days": max([r["age_days"] for r in rows if r["age_days"] is not None], default=None),
            "note": "Signals from the Meta Ad Library by page id. Shares are of ads seen on that page in the pull. Layout and mood only: never copy text, logos, products or faces."}


def _verdict(r: dict) -> dict:
    if r["role"] == "self":
        return {"kind": "info", "text": "Us", "reason": "the brand's own page"}
    if not r["pulled"]:
        return {"kind": "wait", "text": "Not pulled", "reason": "no page id on file, or the page ran no ads in the market"}
    lr = r["long_runner_share"]
    if isinstance(lr, (int, float)) and lr >= 0.4:
        return {"kind": "new", "text": "Study", "reason": f"{round(lr * 100)} percent of its ads have run 30 days or more: proven layouts to learn from"}
    if isinstance(r.get("longest_run_days"), (int, float)) and r["longest_run_days"] < 14:
        return {"kind": "watch", "text": "Fresh flight", "reason": f"its longest ad has run {r['longest_run_days']} days: a new test flight, read again in 2 weeks"}
    return {"kind": "keep", "text": "Watch", "reason": "steady mix, no proven long runners yet"}


def medians(rows: list[dict]) -> dict:
    them = [r for r in rows if r["role"] == "competitor" and r["pulled"] and (r["ads_seen"] or 0) >= MIN_ADS_FOR_MEDIAN]
    out = {"n": len(them), "format_share": {}, "hook_share": {}, "long_runner_share": None, "median_run_days": None}
    for k in FORMATS:
        vals = [r["format_share"][k] for r in them if r["format_share"] and r["format_share"][k] is not None]
        out["format_share"][k] = round(statistics.median(vals), 3) if vals else None
    for k in HOOKS:
        vals = [r["hook_share"][k] for r in them if r["hook_share"] and r["hook_share"][k] is not None]
        out["hook_share"][k] = round(statistics.median(vals), 3) if vals else None
    vals = [r["long_runner_share"] for r in them if r["long_runner_share"] is not None]
    out["long_runner_share"] = round(statistics.median(vals), 3) if vals else None
    vals = [r["median_run_days"] for r in them if isinstance(r["median_run_days"], (int, float))]
    out["median_run_days"] = round(statistics.median(vals), 1) if vals else None
    return out


def gaps(brain) -> list[dict]:
    """Format, hook-form and long-runner gaps between the brand and the competitor median. Each has the rule in numbers."""
    d = pages(brain)
    us, med = d["us"], d["medians"]
    out = []
    if not us or not us["pulled"] or not med["n"]:
        return out
    who = [r for r in d["pages"] if r["role"] == "competitor" and r["pulled"]]
    for k in FORMATS:
        them = med["format_share"].get(k)
        ours = (us["format_share"] or {}).get(k)
        if them is None or ours is None or them < GAP_MIN_THEM_SHARE or ours >= them * GAP_RATIO:
            continue
        leaders = sorted([r for r in who if r["format_share"] and r["format_share"][k] is not None], key=lambda r: -r["format_share"][k])[:3]
        out.append({"kind": "format", "key": k, "label": FORMAT_LABEL[k], "us": ours, "them": them, "us_n": us["formats"][k], "us_total": us["ads_seen"],
                    "leaders": [{"name": r["name"], "share": r["format_share"][k], "n": r["formats"][k]} for r in leaders],
                    "record_ids": us["record_ids"] + [i for r in leaders for i in r["record_ids"][:1]]})
    for k in HOOKS:
        them = med["hook_share"].get(k)
        ours = (us["hook_share"] or {}).get(k)
        if them is None or ours is None or them < GAP_MIN_THEM_SHARE or ours >= them * GAP_RATIO:
            continue
        leaders = sorted([r for r in who if r["hook_share"] and r["hook_share"][k] is not None], key=lambda r: -r["hook_share"][k])[:3]
        out.append({"kind": "hook", "key": k, "label": HOOK_LABEL[k], "us": ours, "them": them, "us_n": us["hooks"][k], "us_total": us["ads_seen"],
                    "leaders": [{"name": r["name"], "share": r["hook_share"][k], "n": r["hooks"][k]} for r in leaders],
                    "record_ids": us["record_ids"] + [i for r in leaders for i in r["record_ids"][:1]]})
    # hook forms competitors use in numbers that we never use at all (them share under the gap floor but non-zero across 3 or more pages)
    for k in HOOKS:
        if any(g["kind"] == "hook" and g["key"] == k for g in out):
            continue
        ours = (us["hook_share"] or {}).get(k)
        users = [r for r in who if r["hooks"] and r["hooks"][k] >= 5]
        if ours == 0 and len(users) >= 3:
            leaders = sorted(users, key=lambda r: -r["hooks"][k])[:3]
            out.append({"kind": "hook", "key": k, "label": HOOK_LABEL[k], "us": 0.0, "them": med["hook_share"].get(k), "us_n": 0, "us_total": us["ads_seen"],
                        "leaders": [{"name": r["name"], "share": r["hook_share"][k], "n": r["hooks"][k]} for r in leaders], "never": True,
                        "record_ids": us["record_ids"] + [i for r in leaders for i in r["record_ids"][:1]]})
    lr_them, lr_us = med["long_runner_share"], us["long_runner_share"]
    if lr_them is not None and lr_us is not None and lr_us < lr_them * LONG_RUNNER_GAP_RATIO:
        leaders = sorted([r for r in who if r["long_runner_share"] is not None], key=lambda r: -r["long_runner_share"])[:3]
        out.append({"kind": "long_runner", "key": "long_runner", "label": "Ads that run 30 days or more", "us": lr_us, "them": lr_them,
                    "us_n": us["long_runners_30d"], "us_total": us["ads_seen"],
                    "leaders": [{"name": r["name"], "share": r["long_runner_share"], "n": r["long_runners_30d"]} for r in leaders],
                    "record_ids": us["record_ids"] + [i for r in leaders for i in r["record_ids"][:1]]})
    return out


def repull(brain) -> dict:
    """Cost of a fresh pull of every configured page by id, against the caps. Never runs anything."""
    cfg = config(brain)
    ml = cfg.get("meta_ad_library") or {}
    budget = cfg.get("budget") or {}
    ids = [p for p in ml.get("pages") or [] if p.get("page_id")]
    limit = ml.get("limit_per_source") or 150
    actor = ml.get("actor")
    apify = _apify_mod()
    est = None
    reason = None
    if not ids or not actor:
        reason = "no pages with a page id in config/apify.json"
    elif apify is None:
        reason = "app/connectors/apify.py could not be loaded"
    else:
        try:
            est = apify.estimate_usd(actor, len(ids) * limit)
        except Exception as exc:  # noqa: BLE001
            reason = str(exc)
    per_run, weekly = budget.get("max_usd_per_run"), budget.get("max_usd_per_week")
    runs_needed = None
    if est is not None and per_run:
        runs_needed = 1 if est <= per_run else -(-len(ids) // max(1, int(per_run // max(0.01, est / len(ids)))))
    return {"pages": len(ids), "items_max": len(ids) * limit, "actor": actor, "estimate_usd": est, "estimate_reason": reason,
            "cap_per_run_usd": per_run, "cap_per_week_usd": weekly, "runs_needed": runs_needed,
            "week_spent_usd": None, "week_spent_reason": "the spend ledger is not readable from this screen; the connector checks it before any run",
            "by_page_id_only": True, "note": "Pages only, never search terms. The connector refuses a run over a cap and shows the estimate first."}
