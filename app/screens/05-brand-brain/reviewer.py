"""Review first: one route for any draft. Every check this screen owns runs on the draft in one call, and the result is
a route: who fixes what before a person reads it.

Checks, all rules and no model: the claims scan (forbidden phrases, unproven absolutes, stale numbers, unapproved
claims, the avoid list, the reading grade); the channel's rule set when a channel is named (built-in plus the
founder's own); the US disclosure gate for the draft's kind (email, ad, page, policy); the locked lines (a draft that
speaks of free shipping, returns or the guarantee must carry the locked line word for word); colours in the draft
against the palette when any hex code appears; quoted lines that read as testimonials (consent must be on file, and
review sites are never quoted as testimonials). The verdict is fail when anything blocks, warn when something needs
a look, pass otherwise. The route follows: blocking hits go to the agent first with the fix per hit; warnings go to
the person with the draft; a pass goes straight to the person's approval. Capability LOOP-C27 gates the disclosures,
BRN-C03 the claims; this screen composes them.
"""
from __future__ import annotations

import re

KIND_BY_CHANNEL = {"meta": "ad", "google": "ad", "email": "email", "amazon": "pdp", "sms": None}
SNIPPET_WORDS = {"free_shipping": ["free shipping", "ships free", "free delivery"], "standard_shipping": ["standard shipping", "shipping cost"], "returns": ["return", "refund"], "guarantee": ["guarantee", "make it right"], "giving": ["donate", "donation", "giving", "give a pair", "gives a pair"], "first_order": ["first order", "welcome code", "% off your first"]}
QUOTE = re.compile(r"[\"“”']([^\"“”']{30,240})[\"“”']")
REVIEW_SITES = re.compile(r"\b(reddit|r/[a-z0-9_]+|trustpilot|amazon review|yelp|sitejabber)\b", re.I)


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9$%. ]+", " ", (s or "").lower()).strip()


def locked_lines_check(text: str, snippets: dict) -> list[dict]:
    hits = []
    low = (text or "").lower()
    for row in snippets.get("snippets") or []:
        if row.get("status") != "locked" or not row.get("locked"):
            continue
        words = SNIPPET_WORDS.get(row["key"], [])
        if not any(w in low for w in words):
            continue
        locked = _norm(row["locked"])
        if locked and locked not in _norm(text):
            hits.append({"kind": "locked_line", "severity": "warn", "match": f"the draft speaks of {row['key'].replace('_', ' ')} without the locked line", "record": row.get("locked_record"), "tier": "voice", "fix": f"Paste the locked line word for word: {row['locked']}"})
    return hits


def quotes_check(text: str, brain=None, ugc_mod=None) -> list[dict]:
    hits = []
    for m in QUOTE.finditer(text or ""):
        q = m.group(1).strip()
        if len(q.split()) < 6:
            continue
        near = (text or "")[max(0, m.start() - 80): m.end() + 80]
        if REVIEW_SITES.search(near):
            hits.append({"kind": "quote", "severity": "fail", "match": q[:80], "record": None, "tier": "consent", "fix": "A review site line is never quoted as a testimonial. Use the doubt it names in your own words."})
            continue
        consent = ugc_mod.match(brain, q) if (ugc_mod is not None and brain is not None) else None
        if consent and consent.get("state", "active") != "expired" and (consent.get("expires_on") is None or consent["expires_on"] >= brain.today.isoformat()):
            hits.append({"kind": "quote", "severity": "info", "match": q[:80], "record": consent["record"], "tier": "consent", "fix": f"Consent on file from {consent.get('name')} ({consent.get('channel')}, {consent.get('granted_on')})" + (f", until {consent['expires_on']}" if consent.get("expires_on") else "") + "."})
        elif consent:
            hits.append({"kind": "quote", "severity": "fail", "match": q[:80], "record": consent["record"], "tier": "consent", "fix": f"The consent from {consent.get('name')} expired on {consent.get('expires_on')}. Renew it or drop the quote."})
        else:
            hits.append({"kind": "quote", "severity": "warn", "match": q[:80], "record": None, "tier": "consent", "fix": "A quoted line reads as a testimonial: consent must be on file (name, channel, date, term) before it runs. Draft the request in UGC permission."})
    return hits


def review(brain, text: str, channel: str | None, kind: str | None, claims_mod, legal_mod, voice_mod, visual_mod, ugc_mod=None, locks_mod=None, glossary_mod=None) -> dict:
    text = text or ""
    checks = []
    hits: list[dict] = []
    sc = claims_mod.channel_scan(brain, text, channel) if channel and channel in claims_mod.CHANNELS else dict(claims_mod.scan(brain, text), channel=None, channel_hits=[])
    brain_hits = [h for h in sc["hits"] if h.get("kind") not in ("channel_rule", "channel_missing")]
    checks.append({"key": "brain", "label": "Claims, numbers and words", "status": "fail" if any(h["severity"] == "fail" for h in brain_hits) else ("warn" if brain_hits else "pass"), "hits": len(brain_hits)})
    hits += brain_hits
    if channel and channel in claims_mod.CHANNELS:
        ch_hits = sc.get("channel_hits") or []
        checks.append({"key": "channel", "label": f"{claims_mod.CHANNELS[channel]['label']} rules", "status": "fail" if any(h["severity"] == "fail" for h in ch_hits) else ("warn" if ch_hits else "pass"), "hits": len(ch_hits)})
        hits += ch_hits
    else:
        checks.append({"key": "channel", "label": "Channel rules", "status": "skipped", "hits": 0, "reason": "no channel named"})
    gk = kind if kind in ("email", "ad", "pdp", "policy", "subscription") else KIND_BY_CHANNEL.get(channel or "")
    if gk:
        g = legal_mod.gate(brain, gk, text, claims_mod)
        g_hits = [{"kind": "disclosure", "severity": "fail", "match": m["label"], "record": None, "tier": "legal", "fix": m["fix"]} for m in g.get("missing") or []]
        checks.append({"key": "legal", "label": f"US disclosures for {'an ' + gk if gk in ('email', 'ad') else 'a ' + gk}", "status": "fail" if g_hits else "pass", "hits": len(g_hits)})
        hits += g_hits
    else:
        checks.append({"key": "legal", "label": "US disclosures", "status": "skipped", "hits": 0, "reason": "no kind for this draft (SMS has no disclosure gate here)"})
    try:
        sn = voice_mod.snippets(brain)
    except Exception:  # noqa: BLE001
        sn = {"snippets": []}
    l_hits = locked_lines_check(text, sn)
    if locks_mod is not None:
        gk_scope = kind if kind in ("email", "ad", "pdp", "policy", "subscription") else KIND_BY_CHANNEL.get(channel or "")
        z_hits = locks_mod.check(brain, text, channel, gk_scope, voice_mod)
        l_hits = [h for h in l_hits if not any(x["record"] == h.get("record") for x in z_hits)] + z_hits
    checks.append({"key": "locked", "label": "Locked zones", "status": "fail" if any(h["severity"] == "fail" for h in l_hits) else ("warn" if l_hits else "pass"), "hits": len(l_hits)})
    hits += l_hits
    if re.search(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b|rgba?\(", text):
        v = visual_mod.check_text(brain, text)
        v_hits = [{"kind": "off_palette", "severity": "warn", "match": r["hex"] + (f" (nearest {r['nearest']})" if r.get("nearest") else ""), "record": None, "tier": "visual", "fix": f"Use {r['nearest_hex']} ({r['nearest']})" if r.get("nearest_hex") else "Use a brand colour."} for r in v.get("off_palette") or []]
        v_hits += [{"kind": "off_font", "severity": "warn", "match": f["name"], "record": None, "tier": "visual", "fix": "Use a brand font."} for f in v.get("off_fonts") or []]
        checks.append({"key": "visual", "label": "Colours and fonts", "status": "warn" if v_hits else ("pass" if v.get("palette_available") else "skipped"), "hits": len(v_hits)})
        hits += v_hits
    else:
        checks.append({"key": "visual", "label": "Colours and fonts", "status": "skipped", "hits": 0, "reason": "no colour code in the draft"})
    if glossary_mod is not None:
        g_hits = glossary_mod.check(brain, text)
        checks.append({"key": "spelling", "label": "The brand's own words", "status": "warn" if g_hits else "pass", "hits": len(g_hits)})
        hits += g_hits
    q_hits = quotes_check(text, brain, ugc_mod)
    consented = sum(1 for h in q_hits if h["severity"] == "info")
    checks.append({"key": "quotes", "label": "Quotes and testimonials", "status": "fail" if any(h["severity"] == "fail" for h in q_hits) else ("warn" if any(h["severity"] == "warn" for h in q_hits) else "pass"), "hits": len(q_hits) - consented, "consented": consented})
    hits += q_hits
    fails = [h for h in hits if h["severity"] == "fail"]
    warns = [h for h in hits if h["severity"] == "warn"]
    verdict = "fail" if fails else ("warn" if warns else "pass")
    route = []
    if fails:
        route.append({"n": 1, "who": "agent", "text": f"Fix the {len(fails)} blocking hit{'s' if len(fails) != 1 else ''}: " + "; ".join((h.get("fix") or h["match"])[:90] for h in fails[:4]) + ("; and more" if len(fails) > 4 else "") + "."})
        route.append({"n": 2, "who": "agent", "text": "Run this review again. Nothing reaches a person while a hit blocks."})
    if warns:
        route.append({"n": len(route) + 1, "who": "person", "text": f"Read the {len(warns)} warning{'s' if len(warns) != 1 else ''} with the draft: " + "; ".join(h["match"][:70] for h in warns[:4]) + ("; and more" if len(warns) > 4 else "") + "."})
    route.append({"n": len(route) + 1, "who": "person", "text": "Approve the draft, or send it back with a line." if not fails else "Approve once the agent's fixes come back clean."})
    return {"verdict": verdict, "checks": checks, "hits": hits, "fails": len(fails), "warns": len(warns), "route": route, "channel": channel if channel in getattr(claims_mod, "CHANNELS", {}) else None, "kind": gk,
            "reading_grade": sc.get("reading_grade"), "words": len(text.split()),
            "owner": "agent_drafts" if fails else "person", "capability": {"id": "LOOP-C27" if any(h["kind"] == "disclosure" for h in fails) else "BRN-C03", "autonomy": "founder_gate"},
            "note": "Every check is a rule; no model read the draft. The route is the order of work: blocking hits go back to the agent with a fix each, warnings go to the person with the draft, a clean draft goes straight to approval."}
