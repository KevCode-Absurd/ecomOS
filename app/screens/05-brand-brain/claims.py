"""Claims desk for the brand brain screen: what we can and cannot say, and a scanner for any draft.

Reads only the brain. Rules, no model:
- `desk(brain)`: every claims record with tier, category, source, age, where the ladders use it, and the verdict
  (usable, needs your call, forbidden). Tier counts for the bar. Untiered claims older than UNTIERED_DAYS are
  the finding BRN-R13 in audit.py.
- `scan(brain, text)`: checks a draft (ad, email, page section) against the brain. Hits:
    forbidden      a phrase the founder forbade (claims tier forbidden) appears;
    needs_proof    an absolute or medical word appears with no approved claim behind it (generic list);
    stale_fact     a number in the draft disagrees with the brain (free shipping threshold, returns window,
                   first order discount, giving count) by keyword;
    unapproved     a sentence leans on a claim whose tier is not approved or site backed;
    reading_level  the draft reads above the tenth grade (Flesch-Kincaid, computed in code).
  Every hit names the record and the fix. A draft with a forbidden or stale hit fails; the rest is a warning.
"""
from __future__ import annotations

import datetime as dt
import re

UNTIERED_DAYS = 7
USABLE = ("approved", "site_backed")
NEEDS_PROOF = ["guaranteed to", "the best", "#1", "number one", "clinically proven", "doctor recommended", "cures", "heals",
               "medical grade", "never fails", "100 percent", "100%", "world's", "worlds", "softest", "strongest", "only sock",
               "risk free", "risk-free", "scientifically", "lab tested", "proven to"]
STOP = set("the a an and or of to in on for with is are was were be it its this that these those you your we our us they them by as at from not no".split())
FORBID_LEAD = re.compile(r"\b(?:never say|do not say|don't say|must not say|never claim|forbidden:?|cannot say)\b\s*", re.I)
GRADE_MAX = 10.0


def _sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+|\n+", (text or "").strip())
    return [p.strip() for p in parts if p.strip()]


def _words(s: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9']+", (s or "").lower()) if w not in STOP and len(w) > 2}


def _syllables(word: str) -> int:
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    groups = re.findall(r"[aeiouy]+", w)
    n = len(groups)
    if w.endswith("e") and not w.endswith(("le", "ee")) and n > 1:
        n -= 1
    return max(1, n)


def reading_grade(text: str) -> float | None:
    """Flesch-Kincaid grade level, in code. None when there is too little text."""
    sents = _sentences(text)
    words = re.findall(r"[A-Za-z][A-Za-z']*", text or "")
    if len(words) < 8 or not sents:
        return None
    syl = sum(_syllables(w) for w in words)
    grade = 0.39 * (len(words) / len(sents)) + 11.8 * (syl / len(words)) - 15.59
    return round(max(0.0, grade), 1)


def forbidden_phrases(brain) -> list[dict]:
    out = []
    for r in brain.records("claims"):
        if r["tier"] != "forbidden":
            continue
        raw = r.get("text") or (r.get("value") if isinstance(r.get("value"), str) else "")
        phrase = FORBID_LEAD.split(raw)[-1].strip().strip(".").strip('"').strip("'") if raw else ""
        if len(phrase) >= 4:
            out.append({"id": r["id"], "phrase": phrase, "text": raw})
    return out


def desk(brain) -> dict:
    ladders = [r for r in brain.records("objection_ladders") if isinstance(r.get("value"), dict)]
    used: dict[str, list[dict]] = {}
    for lad in ladders:
        theme = lad["value"].get("theme") or lad.get("field")
        for rung in lad["value"].get("rungs") or []:
            for pid in rung.get("proof_ids") or []:
                used.setdefault(pid, []).append({"ladder": lad["id"], "theme": theme, "level": rung.get("level"), "uses": rung.get("uses") or []})
    rows = []
    counts = {t: 0 for t in ("approved", "site_backed", "reported", "evidence", "inferred", "unverified", "forbidden")}
    for r in brain.records("claims"):
        tier = r["tier"] if r["tier"] in counts else "unverified"
        counts[tier] += 1
        src = r.get("source") or {}
        val = r.get("value")
        category = None
        if isinstance(val, str) and " claim" in val:
            category = val.split(" claim")[0].split(":")[0].strip()
        elif isinstance(val, dict):
            category = val.get("category")
        where = used.get(r["id"], [])
        surfaces = sorted({u for w in where for u in w["uses"]})
        if tier in USABLE:
            v = {"kind": "keep", "text": "Usable", "reason": f"{tier.replace('_', ' ')}; {len(where)} rung{'s' if len(where) != 1 else ''} use it"}
        elif tier == "forbidden":
            v = {"kind": "stop", "text": "Forbidden", "reason": "never appears in copy; the scanner blocks it"}
        else:
            age = r["age_days"]
            v = {"kind": "fix" if (age is not None and age > UNTIERED_DAYS) else "watch", "text": "Needs your call",
                 "reason": f"{tier}; " + (f"{age} days untiered" if age is not None else "undated") + (f"; used by {len(where)} rungs" if where else "")}
        rows.append({"id": r["id"], "field": r.get("field"), "text": r.get("text") or (val if isinstance(val, str) else ""), "tier": tier, "category": category,
                     "source": {"type": src.get("type"), "ref": src.get("ref")}, "date": None if r["date"] == "undated" else r["date"], "age_days": r["age_days"],
                     "confidence": r["confidence"], "used_by": where, "surfaces": surfaces, "verdict": v, "expires_at": r.get("expires_at")})
    order = {"stop": 0, "fix": 1, "watch": 2, "keep": 3}
    rows.sort(key=lambda x: (order.get(x["verdict"]["kind"], 9), -len(x["used_by"]), x["id"]))
    return {"claims": rows, "counts": counts, "total": len(rows), "usable": sum(counts[t] for t in USABLE),
            "needs_call": sum(1 for x in rows if x["verdict"]["kind"] in ("fix", "watch")), "forbidden": counts["forbidden"],
            "forbidden_phrases": forbidden_phrases(brain), "untiered_days": UNTIERED_DAYS,
            "note": "A claim is usable in customer-facing copy only when it is approved by you or quoted from a live page. Forbidden phrases block a draft in the scanner."}


def _words_avoided(brain) -> list[str]:
    r = next((x for x in brain.records("voice") if x.get("field") == "words_avoided"), None)
    if not r:
        return []
    v = r.get("value")
    t = ", ".join(v) if isinstance(v, list) else (v if isinstance(v, str) else (r.get("text") or ""))
    return [w.strip().lower() for w in re.split(r"[,;\n]+", t) if len(w.strip()) > 1]


def _brain_facts(brain) -> list[dict]:
    """Numbers the scanner can check a draft against, by keyword. Generic keywords, the numbers come from the brain."""
    facts = []
    def rec(section, field):
        return next((r for r in brain.records(section) if r.get("field") == field and r["tier"] in USABLE), None)
    r = rec("offers", "free_shipping_threshold_usd")
    if r and isinstance(r.get("value"), (int, float)):
        facts.append({"id": r["id"], "keywords": ["free shipping", "ships free"], "kind": "usd", "value": float(r["value"]), "label": "free shipping threshold"})
    r = rec("policies", "returns_window_days")
    if r and isinstance(r.get("value"), (int, float)):
        facts.append({"id": r["id"], "keywords": ["return", "returns", "refund"], "kind": "days", "value": float(r["value"]), "label": "returns window in days"})
    r = rec("offers", "first_order_code")
    if r and isinstance(r.get("value"), dict) and isinstance(r["value"].get("discount_pct"), (int, float)):
        facts.append({"id": r["id"], "keywords": ["first order", "welcome", "% off", "percent off"], "kind": "pct", "value": float(r["value"]["discount_pct"]), "label": "first order discount"})
    r = rec("offers", "standard_shipping_cost")
    if r and isinstance(r.get("value"), dict) and isinstance(r["value"].get("cost_usd"), (int, float)):
        facts.append({"id": r["id"], "keywords": ["shipping cost", "shipping is", "standard shipping"], "kind": "usd", "value": float(r["value"]["cost_usd"]), "label": "standard shipping cost"})
    return facts


# Channel rule sets: generic platform vocabulary, not brand facts. Each rule: a pattern, why it fails or warns, and the fix.
# They are guidance from the platforms' public policies as read on 28 Sep 2026, kept short; a person signs off before anything ships.
CHANNELS = {
    "amazon": {"label": "Amazon listing", "rules": [
        (re.compile(r"\b(free shipping|best ?seller|#1|number one|on sale|sale|discount|% off|percent off|deal|limited time)\b", re.I), "fail", "promotional wording is not allowed in titles and bullets", "Move offers out of the listing; state the product facts only."),
        (re.compile(r"https?://|www\.", re.I), "fail", "external links are not allowed", "Remove the link."),
        (re.compile(r"\b(guarantee|guaranteed|warranty)\b", re.I), "warn", "guarantee wording needs the terms on the listing", "Say what the guarantee covers, or drop it."),
        (re.compile(r"[A-Z]{5,}"), "warn", "all caps words read as shouting and fail style checks", "Use sentence case."),
    ]},
    "meta": {"label": "Meta ad", "rules": [
        (re.compile(r"\b(you are|you're|are you|do you)\s+(?:\w+\s+){0,2}(overweight|fat|sick|depressed|broke|in debt|lonely|ugly|old)\b", re.I), "fail", "asserting a personal attribute about the reader", "Speak about the product, not the person."),
        (re.compile(r"\b(before and after|before/after)\b", re.I), "warn", "before and after imagery and wording draw review", "Show the product in use instead."),
        (re.compile(r"\b(cure|cures|treat|treats|heal|heals|medical|clinically)\b", re.I), "warn", "health claims need substantiation and can be rejected", "Use comfort and feel language, not medical outcomes."),
        (re.compile(r"\b(creator|influencer|partner|ambassador)\b", re.I), "warn", "a creator mention needs the paid partnership label", "Add the paid partnership label."),
    ]},
    "google": {"label": "Google ad", "rules": [
        (re.compile(r"!"), "fail", "exclamation marks are not allowed in headlines", "Remove them."),
        (re.compile(r"\b[A-Z]{4,}\b"), "fail", "all caps words fail editorial review", "Use sentence case."),
        (re.compile(r"\b(click here|click now)\b", re.I), "fail", "generic click prompts are not allowed", "Say what the click gets: Shop the 4 pack."),
        (re.compile(r"\b(best|#1|number one|cheapest|lowest price)\b", re.I), "warn", "superlatives need third-party verification on the landing page", "Drop it or link the proof."),
    ]},
    "email": {"label": "Email", "rules": [
        (re.compile(r"\b(unsubscribe|opt[- ]?out|manage preferences)\b", re.I), "must", "an unsubscribe line", "Add a one-click unsubscribe line in the footer."),
        (re.compile(r"\b(re:|fwd:)", re.I), "fail", "a fake reply or forward subject line is deceptive", "Write the subject plainly."),
        (re.compile(r"\b(free|winner|urgent|act now|last chance)\b", re.I), "warn", "spam-trigger words hurt placement", "Say the offer plainly, once."),
    ]},
    "sms": {"label": "SMS", "rules": [
        (re.compile(r"\b(reply stop|text stop|stop to opt out|stop=)\b", re.I), "must", "an opt-out instruction", "Add: Reply STOP to opt out."),
        (re.compile(r"\b(brand|from)\b", re.I), "must", "the brand name", "Name the brand in the first line."),
    ]},
}


RULE_KINDS = ("fail", "warn", "must")


def founder_rules(brain) -> dict:
    """The founder's own channel rules and mutes: claims records `channel_rule_<channel>_<n>` (value: channel, pattern,
    regex, kind, why, fix) and `channel_mute_<channel>_<i>` (value: channel, index of the built-in rule)."""
    rules: dict[str, list[dict]] = {c: [] for c in CHANNELS}
    muted: dict[str, set[int]] = {c: set() for c in CHANNELS}
    for r in brain.records("claims"):
        f = r.get("field") or ""
        v = r.get("value") if isinstance(r.get("value"), dict) else {}
        ch = v.get("channel")
        if ch not in CHANNELS:
            continue
        if f.startswith("channel_rule_") and v.get("pattern"):
            try:
                pat = re.compile(v["pattern"] if v.get("regex") else re.escape(v["pattern"]), re.I)
            except re.error:
                continue
            rules[ch].append({"record": r["id"], "channel": ch, "pattern": v["pattern"], "regex": bool(v.get("regex")), "kind": v.get("kind") if v.get("kind") in RULE_KINDS else "warn", "why": v.get("why") or "your rule", "fix": v.get("fix") or "", "compiled": pat, "date": r["date"]})
        elif f.startswith("channel_mute_") and isinstance(v.get("index"), int):
            muted[ch].add(v["index"])
    return {"rules": rules, "muted": muted}


def channel_sets(brain) -> dict:
    """Every channel's rules for the screen: built-in with an index and a muted flag, plus the founder's own."""
    fr = founder_rules(brain)
    out = {}
    for ch, spec in CHANNELS.items():
        built = [{"index": i, "kind": kind, "why": why, "fix": fix, "pattern": pat.pattern[:80], "muted": i in fr["muted"][ch]} for i, (pat, kind, why, fix) in enumerate(spec["rules"])]
        mine = [{k: r[k] for k in ("record", "pattern", "regex", "kind", "why", "fix", "date")} for r in fr["rules"][ch]]
        out[ch] = {"label": spec["label"], "built_in": built, "founder": mine, "counts": {"built_in": len(built), "muted": len(fr["muted"][ch]), "founder": len(mine)}}
    return {"channels": out, "kinds": list(RULE_KINDS), "note": "Built-in rules are the platform's public vocabulary; mute one when it does not apply to you. Your rules are plain phrases (or a regex when you say so): fail blocks, warn flags, must fails when the phrase is absent. The scanner applies both on every draft for that channel."}


def channel_scan(brain, text: str, channel: str) -> dict:
    """The channel's rules on top of the brain scan. `must` rules fail when the pattern is absent; others when present.
    The founder's mutes drop a built-in rule; the founder's own rules run after the built-in ones."""
    base = scan(brain, text)
    ch = CHANNELS.get(channel)
    if not ch:
        return dict(base, channel=None, channel_hits=[], channels=sorted(CHANNELS))
    fr = founder_rules(brain)
    hits = []
    rules = [(pat, kind, why, fix, None) for i, (pat, kind, why, fix) in enumerate(ch["rules"]) if i not in fr["muted"][channel]]
    rules += [(r["compiled"], r["kind"], r["why"], r["fix"], r["record"]) for r in fr["rules"][channel]]
    for pat, kind, why, fix, record in rules:
        m = pat.search(text or "")
        if kind == "must":
            if not m:
                hits.append({"kind": "channel_missing", "severity": "fail", "match": why, "record": record, "tier": channel, "fix": fix})
        elif m:
            if channel == "email" and pat.pattern.startswith("\\b(unsubscribe"):
                continue
            hits.append({"kind": "channel_rule", "severity": kind, "match": m.group(0)[:60] + (": " + why), "record": record, "tier": channel, "fix": fix})
    fails = base["fails"] + sum(1 for h in hits if h["severity"] == "fail")
    warns = base["warns"] + sum(1 for h in hits if h["severity"] == "warn")
    return dict(base, channel=channel, channel_label=ch["label"], channel_hits=hits, hits=base["hits"] + hits, fails=fails, warns=warns,
                verdict="fail" if fails else ("warn" if warns else "pass"), channels=sorted(CHANNELS))


SPELLING_CHECK = None  # set by the api to glossary.check


def scan(brain, text: str) -> dict:
    text = text or ""
    hits = []
    low = text.lower()
    for fp in forbidden_phrases(brain):
        if fp["phrase"].lower() in low:
            hits.append({"kind": "forbidden", "severity": "fail", "match": fp["phrase"], "record": fp["id"], "tier": "forbidden",
                         "fix": "Remove it. The founder forbade this phrase."})
    approved_text = " ".join((r.get("text") or "").lower() for r in brain.records("claims") if r["tier"] in USABLE)
    for w in NEEDS_PROOF:
        if w in low and w not in approved_text:
            hits.append({"kind": "needs_proof", "severity": "warn", "match": w, "record": None, "tier": None,
                         "fix": "Back it with an approved claim, or soften it to what a live page says."})
    sents = _sentences(text)
    for fact in _brain_facts(brain):
        for s in sents:
            sl = s.lower()
            if not any(k in sl for k in fact["keywords"]):
                continue
            if fact["kind"] == "usd":
                nums = [float(x.replace(",", "")) for x in re.findall(r"\$\s?(\d[\d,]*(?:\.\d+)?)", s)]
            elif fact["kind"] == "pct":
                nums = [float(x) for x in re.findall(r"(\d+(?:\.\d+)?)\s?(?:%|percent)", sl)]
            else:
                nums = [float(x) for x in re.findall(r"(\d+)\s?(?:-?\s?days?|day)", sl)]
            for n in nums:
                if abs(n - fact["value"]) > 0.01:
                    hits.append({"kind": "stale_fact", "severity": "fail", "match": s[:120], "record": fact["id"], "tier": "brain",
                                 "fix": f"The brain says {fact['label']} is {fact['value']:g}. The draft says {n:g}."})
    weak = [r for r in brain.records("claims") if r["tier"] not in USABLE and r["tier"] != "forbidden"]
    for r in weak:
        cw = _words(r.get("text") or "")
        if len(cw) < 4:
            continue
        for s in sents:
            if len(cw & _words(s)) >= 4:
                hits.append({"kind": "unapproved", "severity": "warn", "match": s[:120], "record": r["id"], "tier": r["tier"],
                             "fix": "Approve the claim in the claims desk, or drop the sentence."})
                break
    for w in _words_avoided(brain):
        if re.search(r"\b" + re.escape(w) + r"\b", low):
            hits.append({"kind": "avoided_word", "severity": "warn", "match": w, "record": f"{brain.brand}.voice.words_avoided", "tier": "voice",
                         "fix": "A word on the voice sheet's avoid list. Swap it for a plain one."})
    grade = reading_grade(text)
    if grade is not None and grade > GRADE_MAX:
        hits.append({"kind": "reading_level", "severity": "warn", "match": f"grade {grade}", "record": None, "tier": None,
                     "fix": f"Shorter sentences and plainer words. Target is below grade {GRADE_MAX:g}."})
    if SPELLING_CHECK is not None:
        try:
            hits += SPELLING_CHECK(brain, text)  # the glossary's spelling hits, last
        except Exception:  # noqa: BLE001
            pass
    fails = sum(1 for h in hits if h["severity"] == "fail")
    warns = len(hits) - fails
    return {"verdict": "fail" if fails else ("warn" if warns else "pass"), "fails": fails, "warns": warns, "hits": hits,
            "reading_grade": grade, "words": len(re.findall(r"[A-Za-z][A-Za-z']*", text)), "sentences": len(sents),
            "checked": {"forbidden_phrases": len(forbidden_phrases(brain)), "facts": len(_brain_facts(brain)), "weak_claims": len(weak)}}
