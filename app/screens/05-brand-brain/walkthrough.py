"""The brain end to end: the steps a new brand goes through, each read from the records, with the next one named.

Eleven steps, in the order a founder meets them: name the brand; the site read; a source connected; the founder
notes read into the review queue; the opening questions answered; a claim approved or forbidden; an audience
profile approved and a default set; the positioning frame approved; a line locked; the next peak decided; a decision
taken on the master list. Each step is done, next (the first not done), todo or not applicable, with the evidence
and the block on the page where it happens. The same list runs on any brain folder, so a second brand shows exactly
how far it is. No step writes anything; the founder does each one on its own block.
"""
from __future__ import annotations


def steps(brain, mods: dict) -> dict:
    recs = brain.records()
    by_sec: dict[str, list] = {}
    for r in recs:
        by_sec.setdefault(r["section"], []).append(r)
    out = []

    def add(key, label, done, evidence, block, todo_text, na=False):
        out.append({"key": key, "label": label, "status": "na" if na else ("done" if done else "todo"), "evidence": evidence, "block": block, "todo": todo_text})

    ident = by_sec.get("identity", [])
    named = any(r.get("field") in ("name", "site_url", "one_line_pitch", "category") for r in ident)
    add("named", "Name the brand", named, f"{len(ident)} identity records" if ident else "no identity record", "newbrand", "Type the name, the store url and the category in Start a new brain, or edit the profile.")
    site = [r for r in recs if r["tier"] == "site_backed" or (r.get("source") or {}).get("type") == "site"]
    add("site", "Read the site", bool(site), f"{len(site)} site-backed records" if site else "nothing read from the site", "health", "Run the site crawl from the connectors block; policies, prices and claims fill from it.")
    try:
        con = mods["health"].connectors(brain)
        n_con = con["counts"]["connected"]
    except Exception:  # noqa: BLE001
        n_con = 0
    add("connector", "Connect a source", n_con > 0, f"{n_con} sources connected" if n_con else "no source connected", "health", "Connect the store or the email tool, read-only; each one answers questions before they are asked.")
    docs = brain.documents()
    unread = [d for d in docs if not d.get("extracted")]
    add("documents", "Read the files in", bool(docs) and not unread, f"{len(docs)} files, {len(unread)} not read" if docs else "no file dropped", "files", "Drop the brand book or the call notes in Files in; text files are read into the review queue.", na=not docs)
    oq = by_sec.get("open_questions", [])
    answered = [r for r in oq if isinstance(r.get("value"), dict) and r["value"].get("answered_on")]
    add("questions", "Answer the opening questions", bool(answered) or any(c for c in by_sec.get("changes", []) if isinstance(c.get("value"), dict) and c["value"].get("kind") == "answer"), f"{len(answered)} answered, {len(oq) - len(answered)} open" if oq else "no question on file", "questions", "Answer the top question in a line, or connect the source that answers it.")
    claims = by_sec.get("claims", [])
    decided = [r for r in claims if r["tier"] in ("approved", "forbidden")]
    add("claims", "Approve or forbid a claim", bool(decided), f"{len(decided)} of {len(claims)} claims decided" if claims else "no claim on file", "claims", "In the claims desk, approve what you can back and forbid what must never be said.")
    try:
        au = mods["audiences"].profiles(brain, mods.get("ladderproof"))
        au_done = au["counts"]["approved"] > 0 and "ads" in au["defaults"]
        au_ev = f"{au['counts']['approved']} approved, defaults for {', '.join(au['defaults']) or 'none'}" if au["profiles"] else "no avatar on file"
        au_na = not au["profiles"]
    except Exception:  # noqa: BLE001
        au_done, au_ev, au_na = False, "unavailable", False
    add("audience", "Approve an audience profile and set the default for ads", au_done, au_ev, "audiences", "Approve the real profiles and pick the default for ads.", na=au_na)
    frame = next((r for r in by_sec.get("positioning", []) if r["id"].endswith(".positioning.frame")), None)
    add("positioning", "Approve the positioning frame", bool(frame and frame["tier"] == "approved"), f"frame is {frame['tier'].replace('_', ' ')}" if frame else "no frame on file", "profile", "Edit the frame in the profile in your words; an edit is an approval.")
    try:
        lk = mods["locks"].zones(brain, mods.get("voice"))
        locked = lk["counts"]["lines"] > 0
        lk_ev = f"{lk['counts']['lines']} locked lines, {lk['counts']['facts']} locked facts"
    except Exception:  # noqa: BLE001
        locked, lk_ev = False, "unavailable"
    add("locks", "Lock a line", locked, lk_ev, "locks", "Lock the guarantee line or a disclaimer; no agent draft alters it.")
    try:
        pk = mods["peaks"].readiness(brain, mods["market"].angles_of, mods.get("legal"), mods.get("assumptions"))
        peaks_in = pk["peaks"]
        decided_peak = any(any(c["key"] == "offer" and c["status"] == "ok" for c in p["checks"]) for p in peaks_in)
        pk_ev = f"{pk['counts']['peaks']} peaks in 90 days, {sum(1 for p in peaks_in if any(c['key'] == 'offer' and c['status'] == 'ok' for c in p['checks']))} decided"
    except Exception:  # noqa: BLE001
        peaks_in, decided_peak, pk_ev = [], False, "unavailable"
    add("peak", "Decide the next peak", decided_peak, pk_ev, "peaks", "Open the next peak and decide the offer; every screen reads it.", na=not peaks_in)
    try:
        dl = mods["decisions_log"](brain)
        n_dec = dl["counts"]["action"] + dl["counts"]["snoozed"]
    except Exception:  # noqa: BLE001
        n_dec = 0
    add("decision", "Decide one action on the plan", n_dec > 0, f"{n_dec} decisions on actions" if n_dec else "no decision yet", "plan", "Approve, hand off or snooze the top action on the plan.")
    nxt = next((s for s in out if s["status"] == "todo"), None)
    if nxt:
        nxt["status"] = "next"
    done = sum(1 for s in out if s["status"] == "done")
    applicable = sum(1 for s in out if s["status"] != "na")
    return {"steps": out, "next": nxt, "counts": {"done": done, "applicable": applicable, "na": len(out) - applicable, "pct": round(100 * done / applicable) if applicable else None},
            "note": "Read from the records: every step is done when the brain holds what it produces. The same list runs on any brain folder. Nothing here writes; each step happens on its own block."}
