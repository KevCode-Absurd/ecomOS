"""Copy screen logic shared by api.py and audit.py: claim check, voice check, message match,
language bank rows, the copy set stub and the live ad copy inventory.

Everything is rules in code over the brain (app/brain/<brand>/ through store.py) and the
screen's fixtures. No model call, no connector, no writes. The QA gate: a claim may appear
in customer-facing copy only when its brain record has tier approved or site_backed.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parents[1]
if str(APP / "brain") not in sys.path:
    sys.path.insert(0, str(APP / "brain"))

from store import TIER_RANK, Brain  # noqa: E402

FIXTURES = HERE / "fixtures"
QUOTE = re.compile(r"[“\"]([^”\"]{3,300})[”\"]")
SENTENCE_END = re.compile(r"(?<=[.!?])\s+|\n+")
WORD = re.compile(r"[A-Za-z0-9$%'’-]+")
SIMULATED_NOTE = ("Bombas is the sample brand. Claims, voice and customer words come from public sources. "
                  "Ad copy, ads and spend are simulated.")


def _json(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def rules() -> dict:
    return _json("copy_rules.json")


def copy_sets() -> list[dict]:
    return _json("ad_copy.json")["sets"]


def norm(text: str) -> str:
    """Lower case, straight quotes, letters and digits only, single spaces."""
    t = str(text or "").lower().replace("’", "'").replace("'", "")
    return " ".join(re.sub(r"[^a-z0-9$%]+", " ", t).split())


def url_key(url: str) -> str:
    return re.sub(r"^https?://", "", str(url or "")).split("?")[0].rstrip("/").lower()


def sentences(text: str) -> list[str]:
    return [s.strip() for s in SENTENCE_END.split(str(text or "")) if s and s.strip()]


# ---------------------------------------------------------------- brain views

def claim_records(brain: Brain, r: dict) -> list[dict]:
    """Every record a line of copy can cite, with its tier and whether the gate allows it."""
    allowed = set(r["allowed_tiers"])
    out = []
    for sec in r["claim_sections"]:
        for rec in brain.records(sec):
            src = rec.get("source") or {}
            out.append({"id": rec["id"], "section": sec, "field": rec.get("field"), "text": rec.get("text") or "",
                        "tier": rec["tier"], "allowed": rec["tier"] in allowed, "date": rec["date"],
                        "status": rec["status"], "source_type": src.get("type"), "source_ref": src.get("ref")})
    out.sort(key=lambda c: (TIER_RANK.get(c["tier"], 9), c["section"], c["id"]))
    return out


def _ref_tier(brain: Brain, rid: str) -> str:
    rec = brain.get(rid)
    return rec["tier"] if rec and rec["status"] not in ("retired", "proposed") else "missing"


def is_reddit(rec: dict) -> bool:
    v = rec.get("value") or {}
    return bool(isinstance(v, dict) and v.get("subreddit")) or "not for testimonial" in str(rec.get("notes") or "")


def _bank_texts(rec: dict) -> list[str]:
    v = rec.get("value") or {}
    texts = [v.get("phrase") or ""] + [x.get("quote") or "" for x in (v.get("reviews") or [])]
    texts += [e.get("quote") or "" for e in (rec.get("evidence") or [])]
    return [norm(t) for t in texts if t]


def bank_index(brain: Brain) -> list[dict]:
    return [{"id": r["id"], "reddit": is_reddit(r), "tier": r["tier"], "texts": _bank_texts(r),
             "subreddit": (r.get("value") or {}).get("subreddit")} for r in brain.records("language_bank")]


# ---------------------------------------------------------------- checks

def fk_grade(text: str) -> float | None:
    """Flesch-Kincaid grade level with a vowel-group syllable count."""
    words = WORD.findall(text)
    sents = max(1, len(sentences(text)))
    if not words:
        return None
    syl = 0
    for w in words:
        w = re.sub(r"[^a-z]", "", w.lower())
        if not w:
            syl += 1
            continue
        n = len(re.findall(r"[aeiouy]+", w))
        if w.endswith("e") and not w.endswith(("le", "ee")) and n > 1:
            n -= 1
        syl += max(1, n)
    return max(0.0, round(0.39 * len(words) / sents + 11.8 * syl / len(words) - 15.59, 1))


def plural(n, word: str, many: str | None = None) -> str:
    return f"{n} {word if n == 1 else (many or word + 's')}"


def voice_short(v: dict) -> str:
    """The voice breaks as one short phrase: "1 em dash, 5 inflated words and grade 15.9"."""
    parts = []
    if v["em_dashes"]:
        parts.append(plural(v["em_dashes"], "em dash", "em dashes"))
    if v["inflated"]:
        parts.append(plural(len(v["inflated"]), "inflated word"))
    if v["long_sentences"]:
        parts.append(plural(len(v["long_sentences"]), "sentence") + " over the word limit")
    if v["grade"] is not None and v["breaks"] and any(b.startswith("reads at grade") for b in v["breaks"]):
        parts.append(f"a reading grade of {v['grade']}")
    return parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + " and " + parts[-1] if parts else ""


def voice_check(text: str, r: dict) -> dict:
    v = r["voice"]
    low = str(text or "").lower()
    dashes = sum(low.count(d) for d in v["em_dashes"])
    inflated = sorted({w for w in v["inflated_words"] if re.search(r"\b" + re.escape(w) + r"\b", low)})
    long = [{"text": s, "words": len(WORD.findall(s))} for s in sentences(text)
            if len(WORD.findall(s)) > v["max_sentence_words"]]
    n_words = len(WORD.findall(text))
    grade = fk_grade(text) if n_words >= v["grade_min_words"] else None
    breaks = []
    if dashes:
        breaks.append(plural(dashes, "em dash", "em dashes"))
    if inflated:
        breaks.append("inflated words: " + ", ".join(inflated))
    if long:
        breaks.append(plural(len(long), "sentence") + f" over {v['max_sentence_words']} words")
    if grade is not None and grade > v["max_grade"]:
        breaks.append(f"reads at grade {grade}, above {v['max_grade']}")
    return {"em_dashes": dashes, "inflated": inflated, "long_sentences": long, "grade": grade,
            "words": n_words, "breaks": breaks, "pass": not breaks}


def _testimonial(sentence: str, bank: list[dict]) -> dict | None:
    for m in QUOTE.finditer(sentence):
        q = norm(m.group(1))
        if len(q.split()) < 3:
            continue
        hits = [b for b in bank if any(q in t for t in b["texts"])]
        if not hits:
            continue
        hit = next((b for b in hits if b["reddit"]), hits[0])
        return {"quote": m.group(1), "id": hit["id"], "reddit": hit["reddit"], "tier": hit["tier"],
                "subreddit": hit["subreddit"]}
    return None


def check_sentence(s: str, brain: Brain, r: dict, bank: list[dict]) -> dict:
    low = s.lower()
    allowed = set(r["allowed_tiers"])
    risks = [{"id": p["id"], "reason": p["reason"], "brain_ref": p.get("brain_ref"),
              "match": re.search(p["pattern"], low).group(0)}
             for p in r["risk_patterns"] if re.search(p["pattern"], low)]
    matches = []
    for cp in r["claim_patterns"]:
        hit = next((re.search(p, low) for p in cp["patterns"] if re.search(p, low)), None)
        if hit:
            tier = _ref_tier(brain, cp["ref"])
            matches.append({"id": cp["ref"], "kind": cp["kind"], "label": cp["label"], "term": hit.group(0),
                            "tier": tier, "allowed": tier in allowed})
    quote = _testimonial(s, bank)
    claim_like = bool(risks or matches or quote or re.search(r["claim_like"], low))
    reasons = [x["reason"] for x in risks]
    if quote and quote["reddit"]:
        reasons.append("Reddit words used as a testimonial (Reddit language is never one)")
    elif quote and quote["tier"] not in allowed:
        reasons.append(f"review quote used as a testimonial; its record is {quote['tier'].replace('_', ' ')}")
    for m in matches:
        if not m["allowed"]:
            reasons.append(f"{m['label']}: record is {m['tier'].replace('_', ' ')}, not approved or site backed")
    if claim_like and not matches and not risks and not quote:
        reasons.append("claim-like line with no claim record on file")
    verdict = "not_a_claim" if not claim_like else ("flagged" if reasons else "allowed")
    return {"text": s, "claim_like": claim_like, "verdict": verdict, "matches": matches, "risks": risks,
            "testimonial": quote, "never_testimonial": bool(quote and quote["reddit"]), "reasons": reasons}


def check_text(text: str, brain: Brain, r: dict | None = None, bank: list[dict] | None = None) -> dict:
    r = r or rules()
    bank = bank if bank is not None else bank_index(brain)
    rows = [check_sentence(s, brain, r, bank) for s in sentences(text)]
    flagged = [x for x in rows if x["verdict"] == "flagged"]
    return {"sentences": rows, "claims": sum(1 for x in rows if x["claim_like"]), "flagged": len(flagged),
            "allowed": sum(1 for x in rows if x["verdict"] == "allowed"),
            "never_testimonial": any(x["never_testimonial"] for x in rows),
            "voice": voice_check(text, r), "pass": not flagged}


def set_text(cs: dict) -> str:
    """Headline and primary text as one block, headline first, each ending a sentence."""
    head = cs.get("headline") or ""
    if head and not head.rstrip().endswith((".", "!", "?")):
        head += "."
    return (head + "\n" + (cs.get("primary_text") or "")).strip()


# ---------------------------------------------------------------- message match

def page_records(brain: Brain, url: str, r: dict) -> list[dict]:
    """Brain records captured from this exact page (source or evidence ref). Not a live page scrape."""
    key = url_key(url)
    out = []
    for sec in r["claim_sections"] + ["voice"]:
        for rec in brain.records(sec):
            refs = [(rec.get("source") or {}).get("ref")] + [e.get("ref") for e in (rec.get("evidence") or [])]
            if any(url_key(x) == key for x in refs if x):
                out.append({"id": rec["id"], "tier": rec["tier"], "text": rec.get("text") or ""})
    return out


def message_match(cs: dict, brain: Brain, r: dict, bank: list[dict]) -> dict:
    """The ad's promise items (claims and offers it names) against the landing page's records."""
    chk = check_text(set_text(cs), brain, r, bank)
    page = page_records(brain, cs["destination_url"], r)
    on_page = {p["id"] for p in page}
    items, seen = [], set()
    for s in chk["sentences"]:
        for m in s["matches"]:
            if m["id"] in seen:
                continue
            seen.add(m["id"])
            items.append({"ref": m["id"], "label": m["label"], "kind": m["kind"], "term": m["term"],
                          "on_page": m["id"] in on_page})
    matched = sum(1 for i in items if i["on_page"])
    return {"set_id": cs["id"], "name": cs["name"], "destination_url": cs["destination_url"],
            "items": items, "matched": matched, "total": len(items),
            "score": round(100 * matched / len(items)) if items else None,
            "page_claims": [p["id"] for p in page], "page_captured": bool(page),
            "gaps": [i for i in items if not i["on_page"]]}


# ---------------------------------------------------------------- language bank

def _stars(v: dict) -> list[int]:
    s = {int(k) for k, n in (v.get("count_by_star") or {}).items() if n and str(k).isdigit()}
    s |= {x["star"] for x in (v.get("reviews") or []) if isinstance(x.get("star"), int)}
    return sorted(s)


def _link(rec: dict) -> str | None:
    v = rec.get("value") or {}
    for x in v.get("reviews") or []:
        if str(x.get("url") or "").startswith("http"):
            return x["url"]
    ref = (rec.get("source") or {}).get("ref") or ""
    m = re.search(r"https?://\S+", ref)
    return m.group(0) if m else None


def _use(theme: str | None, reddit: bool) -> str:
    if reddit:
        return "research only: Reddit words, never a testimonial"
    if theme == "complaint":
        return "objection words: answer them, do not quote them"
    return "echo in copy: customer words, not a quote"


def language_rows(brain: Brain) -> list[dict]:
    out = []
    for rec in brain.records("language_bank"):
        v = rec.get("value") or {}
        phrase = str(v.get("phrase") or "")
        reddit = is_reddit(rec)
        sources = sorted({x.get("source") for x in (v.get("reviews") or []) if x.get("source")}) or [
            (rec.get("source") or {}).get("type") or "none"]
        count = v.get("count") or v.get("count_in_sample") or (len(v.get("reviews") or []) or None)
        out.append({"id": rec["id"], "theme": v.get("theme") or "none", "phrase": phrase[:220],
                    "stars": _stars(v), "sources": sources, "subreddit": v.get("subreddit"), "count": count,
                    "upvotes": v.get("weight") if reddit else None, "link": _link(rec), "tier": rec["tier"],
                    "never_testimonial": reddit, "use": _use(v.get("theme"), reddit),
                    "copy_ready": len(phrase.split()) <= 12 and not reddit and v.get("theme") != "complaint",
                    "date": rec["date"]})
    out.sort(key=lambda x: (x["theme"], -(x["count"] or 0), x["id"]))
    return out


# ---------------------------------------------------------------- copy set stub

def gate_line(line: dict, limit: int, brain: Brain, r: dict, bank: list[dict]) -> dict:
    chk = check_text(line["text"], brain, r, bank)
    tiers = {ref: _ref_tier(brain, ref) for ref in line["refs"]}
    reasons = [f"{ref.split('.')[-1].replace('_', ' ')} is {t.replace('_', ' ')}"
               for ref, t in tiers.items() if t not in r["allowed_tiers"]]
    reasons += [x for s in chk["sentences"] for x in s["reasons"] if x not in reasons]
    reasons += chk["voice"]["breaks"]
    if len(line["text"]) > limit:
        reasons.append(f"{len(line['text'])} characters, limit {limit}")
    return {"text": line["text"], "refs": line["refs"], "tiers": tiers, "chars": len(line["text"]),
            "limit": limit, "pass": not reasons, "reasons": reasons}


def copy_set_stub(brain: Brain, r: dict | None = None, bank: list[dict] | None = None) -> list[dict]:
    """One starter set per format from brain-backed lines, with the QA gate applied to each line."""
    r = r or rules()
    bank = bank if bank is not None else bank_index(brain)
    out = []
    for f in r["formats"]:
        heads = [gate_line(x, f["headline_max"], brain, r, bank) for x in r["lines"]["headline"]]
        prims = [gate_line(x, f["primary_max"], brain, r, bank) for x in r["lines"]["primary"]]
        out.append({"format": f["id"], "label": f["label"], "cta": f["cta"],
                    "headline_max": f["headline_max"], "primary_max": f["primary_max"],
                    "headlines": [h for h in heads if h["pass"]][:3], "primary": [p for p in prims if p["pass"]][:2],
                    "blocked": [dict(x, slot=slot) for slot, xs in (("headline", heads), ("primary text", prims))
                                for x in xs if not x["pass"]]})
    return out


# ---------------------------------------------------------------- live inventory

def set_for_ad(ad_id: str, sets: list[dict]) -> dict:
    digits = re.sub(r"\D", "", str(ad_id)) or "0"
    return sets[int(digits) % len(sets)]


def ad_inventory(metric, brand: str, sets: list[dict], days: int = 7, end: str | None = None) -> dict:
    """Live Meta ads from the ad table (spend by ad, last `days` days) with the copy set each one runs.

    `metric(name, **kw)` is the server's Data.metric (or metrics.compute bound to data).
    An ad is live when it spent on the window's last day. Unavailable passes through, never 0.
    """
    kw = {"end": end} if end else {}
    try:
        res = metric("spend", brand=brand, channel="meta", by="ad", window=f"{days}d", **kw)
    except (KeyError, ValueError) as exc:
        res = {"unavailable": True, "reason": f"the ad table could not be read: {exc}"}
    if res.get("unavailable") or res.get("value") is None:
        return {"available": False, "reason": res.get("reason") or "the ad table is not readable",
                "fix": res.get("fix"), "ads": [], "by_set": {}}
    win = res.get("window") or {}
    end = win.get("end") or win.get("ends_on")
    groups = res.get("groups") or []
    if not end:
        end = max((g.get("last_day") or "" for g in groups), default=None)
    ads, by_set = [], {}
    for g in groups:
        cs = set_for_ad(g["ad"], sets)
        live = g.get("last_day") == end and (g.get("spend") or 0) > 0
        ads.append({"ad_id": g["ad"], "campaign": g.get("campaign_name"), "format": g.get("format"),
                    "spend": g.get("spend"), "impressions": g.get("impressions"), "purchases": g.get("purchases"),
                    "last_day": g.get("last_day"), "live": live, "set_id": cs["id"],
                    "dynamic_creative": bool(g.get("dynamic_creative"))})
        if live:
            b = by_set.setdefault(cs["id"], {"live_ads": 0, "spend": 0.0, "ad_ids": []})
            b["live_ads"] += 1
            b["spend"] = round(b["spend"] + (g.get("spend") or 0), 2)
            b["ad_ids"].append(g["ad"])
    return {"available": True, "window": {"days": days, "end": end, "start": win.get("start")},
            "ads": ads, "by_set": by_set, "spend_total": res.get("value")}


def brain_for(brand: str, root: Path | None = None, today: dt.date | None = None) -> Brain:
    return Brain(brand, root, today)
