"""Tag one Meta Ad Library item by format, hook, layout, mood, offer and topic terms.

Rules in code over the ad's public text and snapshot fields; no model call. The ad text
is read here and dropped: only a quote of at most 140 characters leaves this module.
"""
from __future__ import annotations

import datetime as dt
import re

QUOTE_MAX = 140

FORMATS = {"IMAGE": "image", "VIDEO": "video", "CAROUSEL": "carousel", "DCO": "dco", "DPA": "dpa"}

# Topic terms kept as tags. Relevance rules compare these with brain fields, so they are
# plain words a brain record would also use. Each key is the tag; values are the words
# that mark it in ad text (matched on word starts).
TOPICS = {
    "sock": ["sock"], "underwear": ["underwear", "boxer", "brief"], "t-shirt": ["t-shirt", "tee"],
    "slipper": ["slipper"], "bralette": ["bralette"],
    "comfort": ["comfort", "comfy", "soft", "felt fine", "feel fine", "feels good"],
    "slip": ["slip", "fall down", "ride down", "stay up", "stays put"],
    "heel": ["heel"], "arch": ["arch"], "cushion": ["cushion"], "seam": ["seam"],
    "compression": ["compression"], "blister": ["blister"],
    "durability": ["wear out", "they last", "lasts", "last longer", "durab", "holes", "guaranteed for life"],
    "warmth": ["warm", "wool", "merino"], "smell": ["smell", "odor"],
    "shift": ["shift", "long day", "on my feet", "on your feet"],
    "hiking": ["hike", "hiker", "hiking", "trail"], "running": ["run ", "runner", "running"],
    "gift": ["gift"], "kids": ["kid", "toddler"], "giving": ["donate", "donated", "give back"],
    "price": ["price", "expensive", "worth", "value"], "fit": ["fit", "size", "sizing", "tight"],
    "shipping": ["shipping", "delivery"], "prints": ["print", "pattern", "color"],
}

_WORD = re.compile(r"[a-z0-9']+")


def quote(text: str | None, limit: int = QUOTE_MAX) -> str:
    """At most `limit` characters, cut on a word boundary. Never the whole copy when longer."""
    text = " ".join((text or "").split())
    if len(text) <= limit:
        return text
    cut = text[:limit]
    if " " in cut:
        cut = cut[: cut.rfind(" ")]
    return cut.rstrip(" ,;:")[:limit]


def ad_text(item: dict) -> str:
    snap = item.get("snapshot") or {}
    body = snap.get("body")
    text = body.get("text") if isinstance(body, dict) else body
    if not text:
        cards = snap.get("cards") or []
        text = next((c.get("body") for c in cards if c.get("body")), "")
    return text or snap.get("title") or ""


def _has(text: str, word: str) -> bool:
    if " " in word or "-" in word:
        return word in text
    return re.search(r"\b" + re.escape(word), text) is not None


def topics(text: str) -> list[str]:
    low = " " + text.lower() + " "
    return [tag for tag, words in TOPICS.items() if any(_has(low, w) for w in words)]


def hook_type(text: str) -> str | None:
    first = re.split(r"(?<=[.?!])\s+", text.strip(), maxsplit=1)[0] if text.strip() else ""
    low = first.lower()
    if not first:
        return None
    if first.endswith("?"):
        return "question"
    if re.match(r"(i|i'm|i've|my|we|our team)\b", low):
        return "first_person"
    if re.match(r"(tired of|sick of|no more|stop)\b", low):
        return "problem"
    if re.match(r"\d+\s+(reasons|ways|things)", low):
        return "listicle"
    if re.search(r"\d+\s?%|\$\d|free shipping|buy \d", low):
        return "offer_led"
    if re.match(r"(new|introducing|just dropped)\b", low) or "just dropped" in low:
        return "launch"
    if re.match(r"(guaranteed|every|the only)\b", low):
        return "claim"
    return "statement"


def offer(text: str) -> dict:
    """Promo facts in the ad text: type, depth, code, threshold. Empty dict when no promo."""
    low = text.lower()
    out: dict = {}
    code = re.search(r"\bcode\s+([A-Z0-9]{4,})", text)
    pct = re.search(r"(\d{1,2})\s?%\s?off", low)
    thresh = re.search(r"free shipping on orders (?:over|above|of) \$(\d+)", low)
    bogo = re.search(r"buy (\d+),? get (\d+) free", low)
    if code or "first order" in low:
        out["offer_type"] = "first_order_code" if "first order" in low else "code"
    elif bogo or re.search(r"\bbundle|\d+-pack|\bpack of \d", low):
        out["offer_type"] = "bundle"
    elif thresh or "free shipping" in low:
        out["offer_type"] = "free_shipping_threshold"
    elif re.search(r"guarantee|replace them|no questions asked", low):
        out["offer_type"] = "guarantee"
    elif pct:
        out["offer_type"] = "percent_off"
    elif re.search(r"\bfree gift|gift with", low):
        out["offer_type"] = "gift"
    if not out:
        return out
    if pct:
        out["discount_pct"] = float(pct.group(1))
    if bogo:
        buy, free = int(bogo.group(1)), int(bogo.group(2))
        out["discount_pct"] = round(100 * free / (buy + free), 1)
    if code:
        out["code"] = code.group(1)
    if thresh:
        out["threshold_usd"] = float(thresh.group(1))
    price = re.search(r"\$(\d+(?:\.\d{2})?)(?!\d)", text)
    if price and not thresh:
        out["price_usd"] = float(price.group(1))
    out["promo"] = quote(_promo_clause(text), 80)
    return out


def _promo_clause(text: str) -> str:
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        if re.search(r"%|\$|free|code|guarantee|replace|bundle|pack|get \d", sentence, re.I):
            return sentence
    return ""


def layout(fmt: str | None, hook: str | None, promo: dict, n_cards: int) -> str:
    parts = []
    if hook == "question" or hook == "problem":
        parts.append("problem")
    elif hook == "first_person":
        parts.append("personal story")
    elif hook == "listicle":
        parts.append("list of reasons")
    elif hook == "launch":
        parts.append("product reveal")
    elif hook == "claim":
        parts.append("promise")
    else:
        parts.append("product")
    if hook in ("question", "problem"):
        parts.append("product fix")
    if hook == "first_person":
        parts.append("proof")
    if promo:
        parts.append("offer")
    if fmt == "carousel" and n_cards:
        parts.append(f"{n_cards} cards")
    return " then ".join(parts)


def mood(text: str, promo: dict) -> str:
    low = text.lower()
    if promo and re.search(r"this week|today|ends|last chance|now\b|!", low):
        return "urgent"
    if re.search(r"hike|trail|outdoor|merino|winter", low):
        return "outdoor"
    if re.search(r"honest|review|i wore|my feet", low):
        return "candid"
    if re.search(r"new|drop|print|color", low):
        return "playful"
    if re.search(r"guarantee|for life|no questions", low):
        return "reassuring"
    return "calm"


def run_days(item: dict, captured_at: str) -> int | None:
    start = item.get("start_date")
    if not start:
        return None
    day0 = _day(start)
    end = _day(item["end_date"]) if item.get("end_date") else dt.date.fromisoformat(captured_at)
    return max((end - day0).days, 0) if day0 else None


def _day(v) -> dt.date | None:
    if isinstance(v, (int, float)):
        return dt.datetime.fromtimestamp(v, dt.timezone.utc).date()
    try:
        return dt.date.fromisoformat(str(v)[:10])
    except ValueError:
        return None


def signals(item: dict, captured_at: str) -> tuple[dict, list[str]]:
    """Signals dict and tag list for one ad item."""
    snap = item.get("snapshot") or {}
    text = ad_text(item)
    fmt = FORMATS.get((snap.get("display_format") or "").upper(), (snap.get("display_format") or "").lower() or None)
    hook = hook_type(text)
    promo = offer(text)
    start = _day(item["start_date"]) if item.get("start_date") else None
    sig = {"format": fmt, "hook_type": hook, "run_days": run_days(item, captured_at),
           "layout": layout(fmt, hook, promo, len(snap.get("cards") or [])), "mood": mood(text, promo),
           "offer_type": promo.get("offer_type"),
           "platforms": sorted(p.lower() for p in item.get("publisher_platform") or []),
           "start_date": start.isoformat() if start else None, "active": item.get("is_active")}
    for k in ("discount_pct", "code", "threshold_usd", "price_usd", "promo"):
        if k in promo:
            sig[k] = promo[k]
    tags = topics(text)
    if fmt:
        tags.append(f"format:{fmt}")
    if hook:
        tags.append(f"hook:{hook}")
    return sig, tags
