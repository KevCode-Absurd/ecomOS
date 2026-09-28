"""The brain file agents read: one markdown file per capability, strict rules apart from judgement rules, plus a
machine-readable index of this screen's read routes.

`build` writes, in this order: the strict rules the scanner enforces (never say, locked lines word for word, words we
avoid, the numbers the brain holds with their record ids, the channel rules including the founder's own, what a
public-facing agent may not repeat, the standing rules on competitor ads and review quotes); the judgement rules
that guide (the voice sheet, the positioning frame and proof points, the objection ladder rungs with proof); then the
package the capability gets (T0, T1, T2 within its budget, from package.py); then where to check (the review route,
ask, the record routes). Everything comes from records and the modules that read them; nothing is written by a model.
`endpoints` parses this api's own route table into a JSON index an agent or an MCP wrapper can read. Web pass idea 14.
"""
from __future__ import annotations

import re

ROUTE = re.compile(r"^  (GET|POST)\s+(\S+)\s+(.*)$")
NUMBER_FIELDS = [("offers", "free_shipping_threshold_usd", "free shipping threshold"), ("policies", "returns_window_days", "returns window, days"), ("offers", "first_order_code", "first order code"),
                 ("products", "pack_sizes", "pack sizes"), ("policies", "shipping_options", "shipping options"), ("offers", "standard_shipping_cost", "standard shipping cost"), ("identity", "donation_milestone", "donation milestone")]


def _rec(brain, section, field):
    rows = [r for r in brain.records(section) if r.get("field") == field]
    rows.sort(key=lambda r: ({"approved": 0, "site_backed": 1}.get(r["tier"], 2), r["id"]))
    return rows[0] if rows else None


def _val(r) -> str:
    v = r.get("value")
    if isinstance(v, dict):
        return ", ".join(f"{k} {x}" for k, x in v.items() if isinstance(x, (str, int, float)))[:160]
    if isinstance(v, list):
        return ", ".join(str(x) if not isinstance(x, dict) else " ".join(str(y) for y in x.values() if isinstance(y, (str, int, float))) for x in v)[:160]
    return str(v)[:160]


def strict_rules(brain, claims_mod, voice_mod, visibility_mod, public: bool) -> list[dict]:
    rules = []
    forb = claims_mod.forbidden_phrases(brain)
    if forb:
        reasons = {r["id"]: (r.get("value") or {}).get("reason") for r in brain.records("claims") if isinstance(r.get("value"), dict)}
        rules.append({"key": "never_say", "label": "Never say", "lines": [f"{f['phrase']}" + (f" (because {reasons[f['id']]})" if reasons.get(f["id"]) else "") + f" ({f['id']})" for f in forb[:20]], "check": "claims scan blocks it"})
    try:
        sn = voice_mod.snippets(brain)
        locked = [r for r in sn.get("snippets") or [] if r.get("status") == "locked" and r.get("locked")]
    except Exception:  # noqa: BLE001
        locked = []
    if locked:
        rules.append({"key": "locked_lines", "label": "Locked lines, word for word", "lines": [f"{r['key'].replace('_', ' ')}: {r['locked']}" for r in locked], "check": "the review route fails a draft that alters the line"})
    try:
        fl = [r for r in brain.records("content") if (r.get("field") or "").startswith("locked_") and isinstance(r.get("value"), dict) and r["value"].get("text")]
    except Exception:  # noqa: BLE001
        fl = []
    if fl:
        rules.append({"key": "locked_zones", "label": "Locked zones: never rewrite, add word for word where required", "lines": [f"{r['value'].get('label')} ({', '.join(r['value'].get('scope') or ['all'])}{', required' if r['value'].get('required', True) else ''}): {r['value']['text']}" for r in fl], "check": "the review route fails a draft in scope that drops or alters it"})
    try:
        avoided = voice_mod.words_avoided(brain)
    except Exception:  # noqa: BLE001
        avoided = []
    if avoided:
        rules.append({"key": "words_avoided", "label": "Words we avoid", "lines": [", ".join(avoided[:40])], "check": "claims scan flags them"})
    nums = []
    for sec, field, label in NUMBER_FIELDS:
        r = _rec(brain, sec, field)
        if r is not None and not (public and r.get("visibility") == "private"):
            nums.append(f"{label}: {_val(r)} ({r['id']}, {r['tier'].replace('_', ' ')})")
    if nums:
        rules.append({"key": "numbers", "label": "The numbers, from the records; never another value", "lines": nums, "check": "claims scan blocks a number the brain contradicts"})
    try:
        cs = claims_mod.channel_sets(brain)
        ch_lines = []
        for ch, c in cs["channels"].items():
            active = [f"{b['kind']}: {b['why']}" for b in c["built_in"] if not b["muted"]] + [f"{f['kind']}: '{f['pattern']}'" + (f" ({f['why']})" if f.get("why") else "") for f in c["founder"]]
            if active:
                ch_lines.append(f"{c['label']}: " + "; ".join(active)[:400])
        if ch_lines:
            rules.append({"key": "channel_rules", "label": "Channel rules (name the channel when you review)", "lines": ch_lines, "check": "the channel scan applies them"})
    except Exception:  # noqa: BLE001
        pass
    if public:
        try:
            v = visibility_mod.audit(brain)
            priv = [r["section"].replace("_", " ") + f" ({r['private']})" for r in v["rows"] if r["private"]]
        except Exception:  # noqa: BLE001
            priv = []
        rules.append({"key": "public_facing", "label": "You are public facing: private records are not in your package and are never repeated", "lines": [", ".join(priv) or "no private record"], "check": "the package builder leaves them out"})
    rules.append({"key": "standing", "label": "Standing rules", "lines": ["Competitor ads are signals: layout and mood only, never their text, logos, products or faces.", "Review and Reddit lines are never quoted as testimonials; a quote needs consent on file.", "Missing or unsupported values read unavailable, never 0. Numbers are computed in code.", "Short sentences, digits, plain words, no em dashes, below tenth grade."], "check": "the review route"})
    return rules


def judgement_rules(brain, voice_mod, market_mod, ladderproof_mod) -> list[dict]:
    rules = []
    try:
        sh = voice_mod.sheet(brain)
        lines = [f"{f['label']}: {f['text']}" for f in sh.get("fields") or [] if f.get("text")]
        if lines:
            rules.append({"key": "voice", "label": "Voice", "lines": lines})
        ex = [e for e in (sh.get("examples") or []) if e.get("liked")]
        if ex:
            rules.append({"key": "liked", "label": "Lines the founder liked", "lines": [str(e.get("text"))[:160] for e in ex[:5]]})
    except Exception:  # noqa: BLE001
        pass
    frame = next((r for r in brain.records("positioning") if r["id"].endswith(".positioning.frame")), None)
    proof = _rec(brain, "positioning", "proof_points")
    lines = []
    if frame:
        lines.append(f"Frame ({frame['tier'].replace('_', ' ')}): {frame.get('text') or _val(frame)}")
    if proof:
        lines.append(f"Proof points: {_val(proof)}")
    if lines:
        rules.append({"key": "positioning", "label": "Positioning", "lines": lines})
    try:
        m = ladderproof_mod.matrix(brain)
        rungs = sorted(m.get("rungs") or [], key=lambda r: -(r.get("one_star") or 0))[:6]
        if rungs:
            rules.append({"key": "ladders", "label": "The doubts buyers raise, with the proof to answer them", "lines": [f"{r['theme'].replace('_', ' ')} {r['level']}: {r['doubt']} ({r['one_star'] or 0} one-star). " + (f"Proof: {r['proof']}" if r.get("proof") and r["status"] == "proved" else "No proof on file: do not answer it with a claim.") for r in rungs]})
    except Exception:  # noqa: BLE001
        pass
    return rules


def build(brain, capability: str, package_view: dict, mods: dict) -> dict:
    public = bool(package_view.get("public_facing"))
    strict = strict_rules(brain, mods["claims"], mods["voice"], mods["visibility"], public)
    judge = judgement_rules(brain, mods["voice"], mods.get("market"), mods["ladderproof"])
    if mods.get("audiences") is not None:
        try:
            au = mods["audiences"].profiles(brain, mods["ladderproof"])
            if au["profiles"]:
                order = sorted(au["profiles"], key=lambda p: (0 if p["default_for"] else 1, 0 if p["approved"] else 1, -(p["share"] or 0)))
                judge.insert(0, {"key": "audience", "label": "Write for one of these people (defaults first; approved ones are safe to name)", "lines": [("default for " + ", ".join(p["default_for"]) + ": " if p["default_for"] else "") + p["line"] + (" [approved]" if p["approved"] else " [evidence only]") for p in order[:6]]})
        except Exception:  # noqa: BLE001
            pass
    out = [f"# {brain.brand}: brain file for {capability}" + (f" ({package_view.get('name')})" if package_view.get("name") else ""), "",
           f"Generated {brain.today.isoformat()}, brain version {brain.version()}. Read this before you write. Strict rules are checked by the scanner and block; judgement rules guide. Records are named by id; ask for one with GET records/<section>.", ""]
    out.append("## Strict rules (checked, never break)")
    for r in strict:
        out.append(f"### {r['label']}")
        out += [f"- {ln}" for ln in r["lines"]]
        out.append(f"Check: {r['check']}.")
        out.append("")
    out.append("## Judgement rules (guide)")
    for r in judge:
        out.append(f"### {r['label']}")
        out += [f"- {ln}" for ln in r["lines"]]
        out.append("")
    out.append(f"## What you are told (the package, {package_view.get('tokens')} of {package_view.get('budget')} tokens)")
    out.append("")
    out.append(package_view.get("text") or "")
    out.append("")
    out.append("## Where to check")
    out += ["- Review a draft: POST /api/05-brand-brain/review/draft {text, channel, kind}. Blocking hits come back with a fix each.",
            "- Ask the brain: GET /api/05-brand-brain/ask?q=... A sourced answer, or an open question with an owner.",
            "- A record: GET /api/05-brand-brain/records/<section>?reader=<your capability id>. Name yourself so the read is logged.",
            "- The route index: GET /api/05-brand-brain/agentfile/endpoints."]
    text = "\n".join(out)
    return {"capability": capability, "public_facing": public, "text": text, "tokens": mods["package"].tokens(text), "strict": [{"key": r["key"], "label": r["label"], "n": len(r["lines"])} for r in strict],
            "judgement": [{"key": r["key"], "label": r["label"], "n": len(r["lines"])} for r in judge], "package_tokens": package_view.get("tokens"), "version": brain.version()}


def endpoints(api_doc: str) -> list[dict]:
    rows = []
    for ln in (api_doc or "").splitlines():
        m = ROUTE.match(ln)
        if m:
            method, path, what = m.groups()
            rows.append({"method": method, "path": "/api/05-brand-brain/" + path, "what": what.strip(), "read_only": method == "GET"})
        elif rows and ln.startswith("                                ") and ln.strip():
            rows[-1]["what"] += " " + ln.strip()
    return rows
