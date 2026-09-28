"""UGC permission on file: who said we could quote them or reuse their content, on which channel, for how long.

A consent is a founder record in the content section (`consent_<slug>`: the person's name and handle, the channel the
consent came on, what was granted (the quote or the asset), the scope (ads, site, email), when it was granted and the
term). The register shows each consent's state: active, expiring inside 30 days, expired, or no term on file. The
request drafter writes the permission ask in plain words (the exact use, the term, no incentive) for a person to
send; nothing is sent from here. `match` finds the consent behind a quote by word overlap, so the review route can
pass a quoted line that has consent and warn on one that does not. Review sites are never a consent: a Reddit or
review-site line is not quotable as a testimonial whatever is on file. Rule BRN-R31 (consent expiring or expired while
in scope). Web pass idea 16; the FTC endorsement guides are the reason.
"""
from __future__ import annotations

import datetime as dt
import re

CHANNELS = ("instagram", "tiktok", "email", "dm", "form", "phone", "other")
SCOPES = ("ads", "site", "email", "social", "amazon")
WINDOW_DAYS = 30
STOP = set("the a an and or of to in on for with is are was were be it its this that these those i my me you your we our so very".split())


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", (s or "").lower()).strip("_")[:60]


def _words(s) -> set[str]:
    return {w for w in re.findall(r"[a-z']{3,}", str(s or "").lower()) if w not in STOP}


def stored(brain) -> list[dict]:
    out = []
    for r in brain.records("content"):
        if (r.get("field") or "").startswith("consent_") and isinstance(r.get("value"), dict):
            v = r["value"]
            out.append({"record": r["id"], "key": r["field"][8:], "name": v.get("name"), "handle": v.get("handle"), "channel": v.get("channel"), "what": v.get("what"), "scope": v.get("scope") or [],
                        "granted_on": v.get("granted_on"), "term_months": v.get("term_months"), "expires_on": v.get("expires_on"), "evidence": v.get("evidence"), "date": None if r["date"] == "undated" else r["date"]})
    return out


def register(brain) -> dict:
    today = brain.today
    rows = []
    for c in stored(brain):
        days_left = None
        if c["expires_on"]:
            try:
                days_left = (dt.date.fromisoformat(c["expires_on"]) - today).days
            except ValueError:
                days_left = None
        if not c["expires_on"]:
            state, verdict = "no_term", {"kind": "wait", "text": "No term on file"}
        elif days_left is None:
            state, verdict = "bad_date", {"kind": "fix", "text": "Date unreadable"}
        elif days_left < 0:
            state, verdict = "expired", {"kind": "stop", "text": f"Expired {-days_left} d ago"}
        elif days_left <= WINDOW_DAYS:
            state, verdict = "expiring", {"kind": "fix", "text": f"{days_left} d left"}
        else:
            state, verdict = "active", {"kind": "keep", "text": f"{days_left} d left"}
        rows.append(dict(c, days_left=days_left, state=state, verdict=verdict))
    rows.sort(key=lambda r: ({"expired": 0, "expiring": 1, "no_term": 2, "bad_date": 2, "active": 3}[r["state"]], r["days_left"] if r["days_left"] is not None else 10 ** 6, str(r["name"])))
    return {"consents": rows, "channels": list(CHANNELS), "scopes": list(SCOPES), "window_days": WINDOW_DAYS,
            "counts": {"on_file": len(rows), "active": sum(1 for r in rows if r["state"] == "active"), "expiring": sum(1 for r in rows if r["state"] == "expiring"), "expired": sum(1 for r in rows if r["state"] == "expired"), "no_term": sum(1 for r in rows if r["state"] in ("no_term", "bad_date"))},
            "note": "A consent is what the person granted, in their words, on the channel they granted it, with the scope and the term. Review sites are never a consent. The review route passes a quoted line that matches a consent on file and warns on one that does not."}


def match(brain, quote: str) -> dict | None:
    qw = _words(quote)
    if not qw:
        return None
    best, score = None, 0.0
    for c in stored(brain):
        cw = _words(c.get("what"))
        if not cw:
            continue
        s = len(qw & cw) / max(1, min(len(qw), len(cw)))
        if s > score:
            best, score = c, s
    return dict(best, overlap=round(score, 2)) if best and score >= 0.6 else None


def request_draft(brain, name: str, what: str, scope: list[str], term_months: int | None, brand_name: str | None) -> str:
    brand = brand_name or brain.brand.replace("_", " ").title()
    uses = ", ".join(s for s in scope if s in SCOPES) or "our site"
    term = f"for {term_months} months" if term_months else "for 12 months"
    return (f"Hi {name or 'there'},\n\nThank you for what you said about {brand}. We would like to use it: \"{(what or '').strip()[:240]}\"\n\n"
            f"Where: {uses}. How long: {term}. We would credit you by first name and handle, or not at all, as you prefer. Nothing changes in your words.\n\n"
            f"If that is fine, reply yes to this message and we will keep your reply on file with the date. You can withdraw any time by writing to us, and we take it down.\n\n{brand}")


def record(brain, body: dict) -> dict | tuple[int, dict]:
    name = str(body.get("name") or "").strip()[:80]
    what = str(body.get("what") or "").strip()[:400]
    if not name or not what:
        return 400, {"error": "name and what (the quote or the asset) are required"}
    channel = str(body.get("channel") or "other")
    if channel not in CHANNELS:
        return 400, {"error": "channel must be one of " + ", ".join(CHANNELS) + "; a review site is never a consent"}
    scope = body.get("scope") if isinstance(body.get("scope"), list) else [x.strip() for x in str(body.get("scope") or "").split(",") if x.strip()]
    scope = [s for s in scope if s in SCOPES]
    granted = str(body.get("granted_on") or brain.today.isoformat())[:10]
    try:
        g = dt.date.fromisoformat(granted)
    except ValueError:
        return 400, {"error": "granted_on must be a date like 2026-09-28"}
    term = body.get("term_months")
    try:
        term = int(term) if term not in (None, "") else None
    except (TypeError, ValueError):
        return 400, {"error": "term_months must be a number"}
    expires = None
    if term:
        m = g.month - 1 + term
        expires = dt.date(g.year + m // 12, m % 12 + 1, min(g.day, 28)).isoformat()
    key = slug(name + " " + what[:40])
    v = {"name": name, "handle": str(body.get("handle") or "").strip()[:60] or None, "channel": channel, "what": what, "scope": scope, "granted_on": granted, "term_months": term, "expires_on": expires, "evidence": str(body.get("evidence") or "").strip()[:200] or None}
    text = f"{name}" + (f" ({v['handle']})" if v["handle"] else "") + f" agreed on {channel} on {granted} that we may use: \"{what[:120]}\"" + (f" on {', '.join(scope)}" if scope else "") + (f" until {expires}." if expires else "; no term on file.")
    return {"id": f"{brain.brand}.content.consent_{key}", "brand": brain.brand, "section": "content", "field": f"consent_{key}", "value": v, "text": text, "tier": "approved", "confidence": 1.0, "visibility": "private",
            "source": {"type": "founder", "ref": "05-brand-brain UGC permission", "captured_at": brain.today.isoformat()}}
