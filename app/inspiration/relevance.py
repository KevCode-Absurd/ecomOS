"""Relevance of a reference to a brand: the 9 rules of app/contracts/inspiration.md section 3.

Each rule reads brain records through Brain(<brand>) and returns one reasons entry, naming
the brain field, the record id and the matched value, plus a template sentence; or None.
Score is the capped sum of the fired weights. Under 0.3 a reference is stored, not shown.
No model call and no free text from a model.
"""
from __future__ import annotations

import datetime as dt
import json
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BRAIN_DIR = HERE.parent / "brain"
if str(BRAIN_DIR) not in sys.path:
    sys.path.insert(0, str(BRAIN_DIR))

from store import Brain  # noqa: E402

from app.inspiration.tag import TOPICS  # noqa: E402

REGISTRY = json.loads((HERE / "registry.json").read_text(encoding="utf-8"))
WEIGHTS = {r["id"]: r["weight"] for r in REGISTRY["relevance_rules"]}
RULE_DOMAINS = {r["id"]: set(r["domains"]) for r in REGISTRY["relevance_rules"]}
SHOW_AT = REGISTRY["show_threshold"]
OBJECTION_MIN_QUOTES = 10
STOP = {"and", "the", "a", "of", "for", "brand", "focused", "based", "made", "giftcard"}

# Theme of an objection ladder -> topic tags that speak to it. Theme words are matched too.
THEME_TAGS = {
    "price_and_value": {"price"}, "durability": {"durability"}, "fit_and_sizing": {"fit", "slip"},
    "comfort_and_feel": {"comfort", "cushion", "blister", "seam"}, "order_and_delivery": {"shipping"},
    "mission_trust": {"giving"}, "marketplace_trust": set(),
}
# Calendar windows (month, day) the rule can match, and the words that mark a brand as running one.
WINDOWS = {
    "bfcm": ((11, 20), (12, 2), ("bfcm", "black friday", "cyber monday")),
    "holiday gifting": ((11, 1), (12, 24), ("holiday", "christmas", "gifting season")),
    "back to school": ((7, 15), (9, 10), ("back to school", "back_to_school")),
}
# Offer record id fragment -> offer type, for the brand's own offers section.
OFFER_IDS = [("first_order_code", "first_order_code"), ("free_shipping_threshold", "free_shipping_threshold"),
             ("guarantee", "guarantee"), ("bundle", "bundle"), ("gift", "gift"), ("promo_", "percent_off")]


def _singular(word: str) -> str:
    w = word.lower().strip()
    return w[:-1] if w.endswith("s") and not w.endswith("ss") and len(w) > 3 else w


def _norm(name: str) -> str:
    return re.sub(r"[^a-z0-9 ]+", "", (name or "").lower()).strip()


def _same_brand(a: str, b: str) -> bool:
    a, b = _norm(a), _norm(b)
    return bool(a and b) and (a == b or a.startswith(b + " ") or b.startswith(a + " "))


def _topic_tags(ref: dict) -> list[str]:
    return [t for t in ref.get("tags", []) if ":" not in t]


def _reason(rule: str, field: str, record: str | None, match: str, sentence: str) -> dict:
    return {"rule": rule, "brain_field": field, "record": record, "match": match,
            "weight": WEIGHTS[rule], "sentence": sentence}


class Facts:
    """Brain records the rules read, loaded once per brand."""

    def __init__(self, brand: str, brain: Brain | None = None):
        self.brand = brand
        self.brain = brain or Brain(brand)
        self.name = brand.replace("_", " ").title()
        self._by: dict[str, list[dict]] = {}

    def section(self, name: str) -> list[dict]:
        if name not in self._by:
            self._by[name] = self.brain.records(name)
        return self._by[name]

    def one(self, rid_suffix: str, section: str) -> dict | None:
        return next((r for r in self.section(section) if r["id"].endswith("." + rid_suffix)), None)


# ---- the rules ------------------------------------------------------------------------

def same_category(ref: dict, f: Facts) -> dict | None:
    tags = set(_topic_tags(ref))
    cat = f.one("category", "identity")
    if cat and isinstance(cat["value"], str):
        for word in _WORDS.findall(cat["value"].lower()):
            term = _singular(word)
            if term not in STOP and term in tags:
                return _reason("same_category", "identity.category", cat["id"], term,
                               f"Same category: {term}, as in {f.name}'s \"{cat['value']}\"")
    lines = f.one("lines", "products")
    if lines and isinstance(lines["value"], list):
        for line in lines["value"]:
            term = _singular(str(line))
            if term in tags:
                return _reason("same_category", "products.lines", lines["id"], str(line),
                               f"Same category: {term}, a line {f.name} sells")
    return None


_WORDS = re.compile(r"[a-z][a-z'-]+")


def same_avatar(ref: dict, f: Facts) -> dict | None:
    for tag in _topic_tags(ref):
        words = TOPICS.get(tag, [])
        if tag in ("sock", "underwear", "t-shirt", "slipper", "bralette"):
            continue  # product nouns name the category, not a buyer's pain
        for av in f.section("avatars"):
            val = av.get("value") if isinstance(av.get("value"), dict) else {}
            for key in ("pains", "triggers"):
                for phrase in val.get(key) or []:
                    low = " " + phrase.lower() + " "
                    if any(re.search(r"\b" + re.escape(w.strip()), low) for w in words):
                        return _reason("same_avatar", f"avatars.{key}", av["id"], phrase,
                                       f"Same buyer: {val.get('name', av['id'])}, who names \"{phrase}\"")
    return None


def brand_offers(f: Facts) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for rec in f.section("offers"):
        for frag, kind in OFFER_IDS:
            if frag in rec["id"] and kind not in out:
                out[kind] = rec
    return out


def _offer_sentence(kind: str, rec: dict, f: Facts) -> str:
    v = rec["value"]
    if kind == "first_order_code" and isinstance(v, dict):
        return f"Same offer type: a {v.get('discount_pct'):g} percent first-order code, like {v.get('code')}"
    if kind == "free_shipping_threshold":
        return f"Same offer type: free shipping over a threshold, like {f.name}'s ${v:g}" if isinstance(v, (int, float)) \
            else "Same offer type: free shipping over a threshold"
    if kind == "bundle" and isinstance(v, list):
        return f"Same offer type: a pack bundle, like {f.name}'s {', '.join(map(str, v[1:4]))}"
    if kind == "percent_off" and isinstance(v, dict):
        return f"Same offer type: {v.get('promo')}, like {f.name}'s ads"
    short = str(v).split(",")[0].strip()[:60]
    return f"Same offer type: a {kind.replace('_', ' ')}, like {f.name}'s \"{short}\""


def same_offer_type(ref: dict, f: Facts) -> dict | None:
    kind = (ref.get("signals") or {}).get("offer_type")
    if not kind:
        return None
    offers = brand_offers(f)
    look = "first_order_code" if kind == "code" else kind
    rec = offers.get(look)
    if not rec:
        return None
    return _reason("same_offer_type", "offers", rec["id"], look, _offer_sentence(look, rec, f))


def same_price_band(ref: dict, f: Facts) -> dict | None:
    price = (ref.get("signals") or {}).get("price_usd")
    if not price:
        return None
    tags = set(_topic_tags(ref))
    for rec in f.section("products"):
        if "price_ladder" not in rec["id"] or not isinstance(rec["value"], dict):
            continue
        v = rec["value"]
        if _singular(str(v.get("line", ""))) not in tags:
            continue
        med = v.get("median_usd")
        if med is None and v.get("min_usd") and v.get("max_usd"):
            med = math.sqrt(v["min_usd"] * v["max_usd"])  # no median on file: geometric midpoint of the ladder
        if med and 0.6 * med <= price <= 1.6 * med:
            field = "products." + rec["id"].split(".")[-1]
            return _reason("same_price_band", field, rec["id"], f"${price:g} near ${med:.0f}",
                           f"Same price band: ${price:g}, near the ${med:.0f} middle of {f.name}'s {v.get('line', '').lower()} ladder")
    return None


def _in_window(day: dt.date, start: tuple, end: tuple) -> bool:
    return (day.month, day.day) >= start and (day.month, day.day) <= end


def same_calendar(ref: dict, f: Facts) -> dict | None:
    sig = ref.get("signals") or {}
    try:
        day = dt.date.fromisoformat(sig.get("start_date") or ref["captured_at"])
    except (TypeError, ValueError):
        return None
    for label, (start, end, words) in WINDOWS.items():
        if not _in_window(day, start, end):
            continue
        for rec in f.section("calendar"):
            blob = (rec["id"] + " " + json.dumps(rec.get("value")) + " " + (rec.get("text") or "")).lower()
            if any(w in blob for w in words):
                return _reason("same_calendar", "calendar", rec["id"], label,
                               f"Same calendar: runs in {label}, a window {f.name} also runs")
    return None


def same_margin_band(ref: dict, f: Facts) -> dict | None:
    depth = (ref.get("signals") or {}).get("discount_pct")
    if depth is None:
        return None
    gm, red = f.one("gross_margin_model", "economics"), f.one("red_line", "economics")
    if gm and red and isinstance(gm["value"], dict) and isinstance(red["value"], (int, float)):
        room = gm["value"].get("gross_margin_after_fulfilment_pct", 0) - red["value"]
        field, rid = "economics.red_line", red["id"]
    else:
        cm = f.one("contribution_margin_model", "economics")
        if not cm or not isinstance(cm["value"], dict) or cm["value"].get("contribution_margin_pct") is None:
            return None
        # No red line on file: the room is the modelled contribution margin (a discount deeper loses money).
        room = cm["value"]["contribution_margin_pct"]
        field, rid = "economics.contribution_margin_model", cm["id"]
    if 0 < depth <= room:
        return _reason("same_margin_band", field, rid, f"{depth:g} percent within {room:g}",
                       f"Fits the margin: {depth:g} percent off sits inside the {room:g} percent room in {f.name}'s margin model")
    return None


def answers_objection(ref: dict, f: Facts) -> dict | None:
    tags = set(_topic_tags(ref))
    for lad in f.section("objection_ladders"):
        val = lad.get("value") if isinstance(lad.get("value"), dict) else {}
        theme = val.get("theme") or lad["id"].split(".")[-1]
        n = (val.get("counts") or {}).get("one_star") or 0
        if n < OBJECTION_MIN_QUOTES:
            continue
        terms = THEME_TAGS.get(theme, set()) | {_singular(w) for w in theme.split("_and_")}
        hit = sorted(tags & terms)
        if hit:
            return _reason("answers_objection", "objection_ladders", lad["id"], hit[0],
                           f"Answers a doubt: {theme.replace('_', ' ')}, raised in {n} complaint quotes")
    return None


def competitor_in_frame(ref: dict, f: Facts) -> dict | None:
    name = (ref.get("origin") or {}).get("brand") or ""
    if (ref.get("origin") or {}).get("role") == "own":
        return None
    for rec in f.section("competitors"):
        key = rec["id"].split(".")[-1]
        v = rec.get("value")
        if key in ("competitor_frame", "competitor_set") and isinstance(v, list):
            for other in v:
                if _same_brand(name, str(other)):
                    return _reason("competitor_in_frame", f"competitors.{key}", rec["id"], str(other),
                                   f"In {f.name}'s competitor set: {other}")
        if key.startswith("reddit_recommended_") and isinstance(v, dict) and _same_brand(name, v.get("competitor", "")):
            return _reason("competitor_in_frame", "competitors.reddit_recommended", rec["id"], v["competitor"],
                           f"Reddit recommends {v['competitor']} instead of {f.name} {v.get('recommended_instead')} times")
    return None


def own_brand(ref: dict, f: Facts) -> dict | None:
    if (ref.get("origin") or {}).get("role") != "own":
        return None
    return _reason("own_brand", "origin.role", None, "own", f"{f.name}'s own ad: yours to reuse")


RULES = [same_category, same_avatar, same_offer_type, same_price_band, same_calendar,
         same_margin_band, answers_objection, competitor_in_frame, own_brand]


def score(ref: dict, facts: Facts) -> dict:
    """The relevance block: {score, shown, reasons}. Own-brand references score 1.0 and are always shown."""
    domain = ref.get("domain")
    reasons = [r for rule in RULES if domain in RULE_DOMAINS[rule.__name__] for r in [rule(ref, facts)] if r]
    if any(r["rule"] == "own_brand" for r in reasons):
        total = 1.0
    else:
        total = min(1.0, round(sum(r["weight"] for r in reasons), 2))
    return {"score": total, "shown": total >= SHOW_AT, "reasons": reasons}


def sentence(ref: dict) -> str:
    """The one line a card shows: the highest-weight reason's sentence."""
    reasons = sorted((ref.get("relevance") or {}).get("reasons", []), key=lambda r: -r.get("weight", 0))
    return reasons[0]["sentence"] if reasons else ""
