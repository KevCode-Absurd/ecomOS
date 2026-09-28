"""Files in, deeper: rule-based extraction of a text or markdown file into proposed brain records.

No model call. Rules only, so the same file gives the same records:
- a heading (`# ...`) sets the section for the lines under it, from the words in the heading;
- a key-value line (`Key: value`, `Key = value`) becomes one record, field from the key, section from the key
  words, else from the heading;
- a bullet (`- ...`, `* ...`, `1. ...`) under a heading becomes one record in the heading's section;
- a sentence that says something was tried, tested or did not work becomes a learnings record;
- a sentence that says never say, do not say or forbidden becomes a claims record with tier forbidden;
- a sentence that says we decided becomes a decisions record.

Every record is proposed (status `proposed`), tier `unverified` unless the rule says forbidden, with the file
as its source and the line as evidence. Nothing reaches the brain until a person accepts it in the review
queue. The file itself is kept as it is. Binary files and urls are not read.
"""
from __future__ import annotations

import re

MAX_RECORDS = 40
MIN_LINE = 12
TEXT_SUFFIXES = (".md", ".markdown", ".txt", ".text")

# words in a heading or a key that place a line in a section; generic vocabulary, not brand facts
SECTION_WORDS = [
    ("voice", ["voice", "tone", "how we write", "writing", "words we", "style"]),
    ("offers", ["offer", "discount", "promo", "bundle", "free shipping", "shipping threshold", "code", "coupon", "loyalty", "referral program"]),
    ("policies", ["policy", "return", "refund", "exchange", "guarantee", "warranty", "shipping policy", "privacy"]),
    ("claims", ["claim", "can say", "cannot say", "never say", "must not say", "forbidden", "approved language"]),
    ("competitors", ["competitor", "versus", "compare", "rival"]),
    ("avatars", ["customer", "avatar", "who buys", "persona", "audience", "segment"]),
    ("decisions", ["decision", "decided", "agreed", "sign off", "signed off"]),
    ("learnings", ["learning", "learned", "tested", "test", "tried", "did not work", "didn't work", "worked", "result", "experiment"]),
    ("products", ["product", "sku", "line", "collection", "material", "size", "sizing", "fit"]),
    ("identity", ["mission", "founded", "founder", "about us", "brand story", "who we are", "values", "b corp", "giving"]),
    ("team", ["team", "hire", "hiring", "role", "agency", "approver", "approval"]),
    ("operations", ["supplier", "3pl", "warehouse", "fulfil", "fulfill", "lead time", "carrier", "inventory", "stock"]),
    ("economics", ["margin", "cac", "mer", "roas", "revenue", "aov", "ltv", "budget", "cash", "target"]),
    ("channels", ["channel", "meta", "google", "tiktok", "email", "sms", "affiliate", "amazon ads"]),
    ("calendar", ["calendar", "launch date", "season", "holiday", "black friday", "peak"]),
    ("positioning", ["positioning", "frame", "differentiat", "why us", "category"]),
]
TRIED = re.compile(r"\b(we tried|we tested|did not work|didn't work|did not move|worked well|failed|never propose|stopped working|no lift|no effect)\b", re.I)
FORBID = re.compile(r"\b(never say|do not say|don't say|must not say|must never|never claim|forbidden|not allowed to say|cannot say)\b", re.I)
DECIDED = re.compile(r"\b(we decided|decision:|we agreed|signed off|sign-off:)\b", re.I)
HEADING = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$")
BULLET = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+(.+?)\s*$")
KEYVAL = re.compile(r"^\s*([A-Za-z][A-Za-z0-9 /&()'-]{1,60}?)\s*[:=]\s+(.{2,400})$")
CODE_FENCE = re.compile(r"^\s*```")


def slug(text: str, n: int = 40) -> str:
    return re.sub(r"[^a-z0-9]+", "_", (text or "").lower()).strip("_")[:n].strip("_") or "line"


def section_for(text: str, default: str | None = None) -> str | None:
    t = (text or "").lower()
    for sec, words in SECTION_WORDS:
        if any(w in t for w in words):
            return sec
    return default


def is_text_file(name: str) -> bool:
    return (name or "").lower().endswith(TEXT_SUFFIXES)


def extract(text: str, brand: str, doc_file: str, today: str) -> list[dict]:
    """Proposed records from one text file. `doc_file` is the manifest path (documents/<name>)."""
    out: list[dict] = []
    seen: set[str] = set()
    doc = slug(doc_file.rsplit("/", 1)[-1].rsplit(".", 1)[0], 30)
    heading, heading_sec, in_code = None, None, False
    n_under = 0

    def add(section: str, field: str, value, line: str, tier: str = "unverified") -> None:
        if len(out) >= MAX_RECORDS:
            return
        field = slug(field, 50)
        rid = f"{brand}.{section}.{doc}_{field}"
        i = 2
        while rid in seen:
            rid = f"{brand}.{section}.{doc}_{field}_{i}"
            i += 1
        seen.add(rid)
        out.append({"id": rid, "brand": brand, "section": section, "field": rid.split(".", 2)[2], "value": value, "text": line.strip()[:400],
                    "tier": tier, "status": "proposed", "visibility": "private",
                    "source": {"type": "document", "ref": doc_file, "captured_at": today, "heading": heading},
                    "evidence": [{"quote": line.strip()[:300], "ref": doc_file}]})

    for raw in (text or "").splitlines():
        line = raw.rstrip()
        if CODE_FENCE.match(line):
            in_code = not in_code
            continue
        if in_code or not line.strip():
            continue
        h = HEADING.match(line)
        if h:
            heading = h.group(1).strip()
            heading_sec = section_for(heading)
            n_under = 0
            continue
        body = line.strip()
        b = BULLET.match(line)
        if b:
            body = b.group(1).strip()
        if len(body) < MIN_LINE:
            continue
        if FORBID.search(body):
            add("claims", "never_" + slug(FORBID.split(body)[-1] or body, 30), body, body, tier="forbidden")
            continue
        if DECIDED.search(body):
            add("decisions", slug(DECIDED.split(body)[-1] or body, 30), body, body)
            continue
        if TRIED.search(body):
            add("learnings", slug(body, 30), body, body)
            continue
        kv = KEYVAL.match(body)
        if kv and not body.lower().startswith(("http", "note")):
            key, val = kv.group(1).strip(), kv.group(2).strip()
            sec = section_for(key) or heading_sec or section_for(val) or "learnings"
            add(sec, key, _coerce(val), body)
            continue
        if b and heading:
            n_under += 1
            sec = heading_sec or section_for(body) or "learnings"
            add(sec, f"{slug(heading, 24)}_{n_under}", body, body)
            continue
        if heading and heading_sec and len(body) >= 40 and n_under == 0:
            # the first paragraph under a heading that names a section is the section's note
            n_under += 1
            add(heading_sec, slug(heading, 30), body, body)
    return out


def _coerce(text: str):
    t = text.strip().replace(",", "").replace("$", "")
    if re.fullmatch(r"-?\d+(\.\d+)?%?", t):
        return float(t.rstrip("%"))
    return text.strip()


def summary(records: list[dict]) -> dict:
    by_sec: dict[str, int] = {}
    for r in records:
        by_sec[r["section"]] = by_sec.get(r["section"], 0) + 1
    return {"proposed": len(records), "sections": sorted(by_sec), "by_section": by_sec,
            "forbidden": sum(1 for r in records if r["tier"] == "forbidden")}
