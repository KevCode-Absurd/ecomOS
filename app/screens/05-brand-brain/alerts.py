"""The weekly alert digest: everything due or changed across the brain in one message, with what is new since the
last digest.

Sources, all modules this screen already runs: site changes not reviewed, the competitor snapshot age, assets and
consents expiring or expired, section reviews overdue, peaks inside 30 days with decisions waiting, red lines
without a reason, rejected ideas due for review, questions open, and the changes log. Each alert has a kind, a line,
a block on the page and a due date when it has one. The founder marks the digest sent (a founder record
`team.last_digest_on`) and the next one flags what appeared since. Delivery is copy or print until a Slack or email
connector exists; the digest says so.
"""
from __future__ import annotations

import datetime as dt

PEAK_WINDOW = 30


def last_digest(brain) -> str | None:
    r = next((x for x in brain.records("team") if x.get("field") == "last_digest_on"), None)
    return r.get("value") if r and isinstance(r.get("value"), str) else None


def build(brain, parts: dict) -> dict:
    since = last_digest(brain)
    items = []

    def add(kind, text, block, due=None, when=None, severity="low"):
        items.append({"kind": kind, "text": text, "block": block, "due": due, "when": when, "severity": severity, "new": bool(when and since and when > since) or (since is None)})

    site = parts.get("site") or {}
    for c in (site.get("changes") or [])[:10]:
        if not c.get("reviewed"):
            add("site", f"Site change: {c.get('what') or c.get('field')} ({c.get('kind')})", "site", None, site.get("new"), "medium")
    mk = parts.get("market") or {}
    age = mk.get("snapshot_age_days")
    if age is None:
        add("competitors", "Competitor snapshot: never pulled", "market", None, None, "low")
    elif age > 7:
        add("competitors", f"Competitor snapshot is {age} days old", "market", None, None, "low")
    for a in (parts.get("assets") or {}).get("assets") or []:
        if a["state"] in ("expired_live", "inside_window"):
            add("asset", f"{a['name']}: " + ("right expired, still live" if a["state"] == "expired_live" else f"right ends {a['expires_on']}, {a['days_left']} days"), "assets", a.get("expires_on"), a.get("date"), "high" if a["state"] == "expired_live" else "medium")
    for c in (parts.get("consents") or {}).get("consents") or []:
        if c["state"] in ("expired", "expiring"):
            add("consent", f"{c['name']}'s consent " + ("expired" if c["state"] == "expired" else f"ends {c['expires_on']}"), "ugc", c.get("expires_on"), c.get("date"), "medium")
    for r in (parts.get("owners") or {}).get("rows") or []:
        if r["state"] == "overdue":
            add("review", f"{r['label'].capitalize()} review overdue by {-r['due_in']} days" + (f" ({r['owner']})" if r.get("owner") else ""), "owners", None, r.get("last"), "medium")
    for p in (parts.get("peaks") or {}).get("peaks") or []:
        gaps = [c["label"].lower() for c in p["checks"] if c["status"] == "gap"]
        if gaps and p.get("days_to") is not None and p["days_to"] <= PEAK_WINDOW:
            add("peak", f"{p['label']} in {p['days_to']} days: {', '.join(gaps)}", "peaks", p.get("date"), None, "high")
    rl = parts.get("redlines") or {}
    if rl.get("counts", {}).get("without_reason"):
        add("redline", f"{rl['counts']['without_reason']} red lines without a reason", "redlines", None, None, "low")
    for v in (parts.get("rejected") or []):
        if v.get("due"):
            add("idea", f"Rejected idea {v['idea_id']} is due for review", "unlocks", v.get("review_on"), v.get("rejected_on"), "low")
    qs = parts.get("questions") or []
    if qs:
        add("question", f"{len(qs)} questions open; top: {qs[0]['question'][:80]}", "questions", None, None, "low")
    ch = parts.get("changes") or {}
    week = ch.get("week") or []
    if week:
        add("changes", f"{len(week)} changes this week in the brain", "changes", None, None, "low")
    order = {"high": 0, "medium": 1, "low": 2}
    items.sort(key=lambda x: (order[x["severity"]], x["due"] or "9999", x["kind"]))
    new = [x for x in items if x["new"]]
    lines = [f"Brain alerts for {brain.brand}, {brain.today.isoformat()}" + (f" (since the digest of {since})" if since else " (first digest)"), ""]
    for x in items:
        lines.append(f"- [{x['severity']}] {x['text']}" + (f", due {x['due']}" if x["due"] else "") + (" (new)" if x["new"] and since else ""))
    if not items:
        lines.append("Nothing due or changed. Enjoy the quiet.")
    lines += ["", "Open the brain screen for the block each line names. Delivery: copy this; no Slack or email connector yet."]
    return {"items": items, "counts": {"total": len(items), "new": len(new), "high": sum(1 for x in items if x["severity"] == "high"), "medium": sum(1 for x in items if x["severity"] == "medium")}, "since": since, "text": "\n".join(lines),
            "delivery": {"app": "this screen", "slack": None, "email": None, "reason": "no Slack or email connector yet; copy the digest"},
            "note": "One message from every check the screen runs: site, competitors, assets, consents, reviews, peaks, red lines, rejected ideas, questions, changes. Mark it sent and the next digest flags what is new since."}


def sent_record(brain) -> dict:
    return {"id": f"{brain.brand}.team.last_digest_on", "brand": brain.brand, "section": "team", "field": "last_digest_on", "value": brain.today.isoformat(), "text": f"Last alert digest sent on {brain.today.isoformat()}.",
            "tier": "approved", "confidence": 1.0, "visibility": "private", "source": {"type": "founder", "ref": "05-brand-brain alerts", "captured_at": brain.today.isoformat()}}
