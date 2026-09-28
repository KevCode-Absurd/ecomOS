"""Site diff between crawls: did a price, an offer, a policy or a claim change without anyone noticing?

A snapshot is the flattened output of the site crawl (app/brain/<brand>/raw/a-site/*.json: identity, products, offers,
policies, claims, voice, visual, site_map, stack), one row per record id with its value, text and capture date.
Snapshots live under app/brain/<brand>/snapshots/site/<date>.json. The first one is seeded from the crawl on
file, so a brand with one crawl shows "1 snapshot, the next crawl gives the first diff" rather than a fake diff.

`diff(brain)` compares the two newest snapshots: added, removed and changed records with old and new values.
Kind and severity come from the section: offers, policies, claims and product prices are high (they change what
copy, ads and CX may say), the rest low. A change stays open until a person marks it reviewed (reviewed.json).
Open changes are the finding BRN-R14 in audit.py. No network call here; the crawl itself is app/brain/extract/site.py.
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

SITE_SECTIONS = ["identity", "products", "offers", "policies", "claims", "voice", "visual", "site_map", "stack"]
HIGH = {"offers", "policies", "claims"}
PRICE_FIELDS = ("price", "usd", "cost", "threshold")
KIND = {"offers": "offer", "policies": "policy", "claims": "claim", "products": "product", "identity": "identity", "voice": "voice",
        "visual": "visual", "site_map": "site map", "stack": "stack"}


def snap_dir(brain) -> Path:
    return brain.dir / "snapshots" / "site"


def read_raw(brain) -> tuple[dict[str, dict], str | None]:
    """Current crawl output as {record id: row}, plus the newest capture date it carries."""
    rows: dict[str, dict] = {}
    newest = None
    for sec in SITE_SECTIONS:
        p = brain.dir / "raw" / "a-site" / f"{sec}.json"
        if not p.is_file():
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        for r in data:
            if not isinstance(r, dict) or not r.get("id"):
                continue
            src = r.get("source") or {}
            cap = str(src.get("captured_at") or "")[:10] or None
            if cap and (newest is None or cap > newest):
                newest = cap
            rows[r["id"]] = {"id": r["id"], "section": r.get("section") or sec, "field": r.get("field"), "value": r.get("value"),
                             "text": r.get("text"), "captured_at": cap, "ref": src.get("ref")}
    return rows, newest


def snapshots(brain) -> list[dict]:
    d = snap_dir(brain)
    if not d.is_dir():
        return []
    out = []
    for p in sorted(d.glob("*.json")):
        if p.name == "reviewed.json":
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        out.append({"date": p.stem, "records": len(data.get("records") or {}), "path": p.name, "source": data.get("source")})
    return out


def _load(brain, date: str) -> dict[str, dict]:
    try:
        return json.loads((snap_dir(brain) / f"{date}.json").read_text(encoding="utf-8")).get("records") or {}
    except (OSError, ValueError):
        return {}


def take(brain, date: str | None = None, source: str = "raw/a-site") -> dict:
    """Store the current crawl output as a snapshot dated by its newest capture (or today when asked)."""
    rows, newest = read_raw(brain)
    if not rows:
        return {"ok": False, "reason": "no crawl output under raw/a-site; run the site extractor first"}
    stamp = date or newest or brain.today.isoformat()
    d = snap_dir(brain)
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{stamp}.json").write_text(json.dumps({"date": stamp, "source": source, "records": rows}, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return {"ok": True, "date": stamp, "records": len(rows)}


def ensure_first(brain) -> None:
    """Seed the first snapshot from the crawl on file, so the diff has a baseline. Idempotent."""
    if not snapshots(brain):
        take(brain)


def reviewed_ids(brain) -> dict:
    p = snap_dir(brain) / "reviewed.json"
    try:
        return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}
    except (OSError, ValueError):
        return {}


def mark_reviewed(brain, pair: str, ids: list[str], who: str = "founder") -> dict:
    rv = reviewed_ids(brain)
    entry = rv.setdefault(pair, {})
    for i in ids:
        entry[i] = {"at": brain.today.isoformat(), "who": who}
    snap_dir(brain).mkdir(parents=True, exist_ok=True)
    (snap_dir(brain) / "reviewed.json").write_text(json.dumps(rv, indent=1) + "\n", encoding="utf-8")
    return {"pair": pair, "reviewed": len(entry)}


def _same(a, b) -> bool:
    return json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


def _severity(section: str, field: str | None) -> str:
    if section in HIGH:
        return "high"
    if section == "products" and any(w in (field or "") for w in PRICE_FIELDS):
        return "high"
    if section in ("identity", "stack"):
        return "medium"
    return "low"


def _short(v) -> str:
    s = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)
    return s if len(s) <= 140 else s[:137] + "..."


def diff(brain) -> dict:
    ensure_first(brain)
    snaps = snapshots(brain)
    if len(snaps) < 2:
        one = snaps[0] if snaps else None
        return {"snapshots": snaps, "pair": None, "changes": [], "counts": {"changes": None, "open": None, "high": None},
                "unavailable_reason": (f"1 snapshot on file ({one['date']}, {one['records']} records). The next crawl gives the first diff." if one
                                       else "no crawl output yet; run the site extractor, then snapshot it"),
                "note": "A change stays open until you mark it reviewed. Offers, policies, claims and prices are high: they change what copy, ads and CX may say."}
    old_d, new_d = snaps[-2]["date"], snaps[-1]["date"]
    old, new = _load(brain, old_d), _load(brain, new_d)
    pair = f"{old_d}..{new_d}"
    rv = reviewed_ids(brain).get(pair, {})
    changes = []
    for rid in sorted(set(old) | set(new)):
        a, b = old.get(rid), new.get(rid)
        if a and b and _same(a.get("value"), b.get("value")):
            continue
        section = (b or a)["section"]
        field = (b or a).get("field")
        change = "added" if not a else ("removed" if not b else "changed")
        sev = _severity(section, field)
        changes.append({"id": rid, "section": section, "field": field, "kind": KIND.get(section, section), "change": change, "severity": sev,
                        "old": a.get("value") if a else None, "new": b.get("value") if b else None,
                        "old_text": _short(a.get("value")) if a else None, "new_text": _short(b.get("value")) if b else None,
                        "ref": (b or a).get("ref"), "captured_at": (b or a).get("captured_at"),
                        "reviewed": rv.get(rid), "action": _action(section, field, change, sev)})
    order = {"high": 0, "medium": 1, "low": 2}
    changes.sort(key=lambda c: (bool(c["reviewed"]), order.get(c["severity"], 9), c["id"]))
    open_ = [c for c in changes if not c["reviewed"]]
    return {"snapshots": snaps, "pair": pair, "old": old_d, "new": new_d, "changes": changes,
            "counts": {"changes": len(changes), "open": len(open_), "high": sum(1 for c in open_ if c["severity"] == "high"),
                       "by_section": {s: sum(1 for c in changes if c["section"] == s) for s in SITE_SECTIONS if any(c["section"] == s for c in changes)}},
            "unavailable_reason": None,
            "note": "A change stays open until you mark it reviewed. Offers, policies, claims and prices are high: they change what copy, ads and CX may say."}


def _action(section: str, field: str | None, change: str, sev: str) -> dict:
    f = (field or "").replace("_", " ")
    if section in ("offers", "policies"):
        return {"title": f"Carry the new {f} into copy, ads, email and CX", "owner": "agent_drafts", "capability": "BRN-C01", "artefact": "copy",
                "steps": [{"n": 1, "who": "agent", "text": f"Accept the new {f} into the brain (the site wins unless you decided otherwise)."},
                          {"n": 2, "who": "agent", "text": "Scan live ads, emails and page sections for the old value. The draft scanner now blocks it."},
                          {"n": 3, "who": "person", "text": "Approve the edits. Each ships from its own screen."}]}
    if section == "claims":
        return {"title": f"Re-tier the {f} claim after the site change", "owner": "person", "capability": "BRN-C03", "artefact": "brain_record",
                "steps": [{"n": 1, "who": "agent", "text": "Show the old and the new claim text side by side with the page."},
                          {"n": 2, "who": "person", "text": "Approve the new wording or forbid it in the claims desk."},
                          {"n": 3, "who": "agent", "text": "Re-point the ladder rungs and flag copy that used the old claim."}]}
    if section == "products":
        return {"title": f"Check listings and ads for the {f} change", "owner": "agent", "capability": "BRN-C01", "artefact": "listing_fix",
                "steps": [{"n": 1, "who": "agent", "text": "Compare the new product facts with the marketplace listings and the active ads."},
                          {"n": 2, "who": "agent", "text": "Propose listing and ad fixes where a price, a pack size or a line no longer matches."},
                          {"n": 3, "who": "person", "text": "Approve the fixes."}]}
    return {"title": f"Note the {section.replace('_', ' ')} change: {f}", "owner": "agent", "capability": "BRN-C01", "artefact": "brain_record",
            "steps": [{"n": 1, "who": "agent", "text": "Accept the new value into the brain and log it in the changes section."},
                      {"n": 2, "who": "person", "text": "Mark it reviewed here."}]}
