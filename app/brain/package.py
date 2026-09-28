"""Build the brain context one capability needs, inside a token budget.

Usage: python3 app/brain/package.py example '{"id":"CREA-C01","brain_sections":{"offers":"T2"}}'
       from package import package; package("example", capability, budget=4000)

Contract: app/contracts/brand-brain.md section 5. Tiers, cheapest first:
T0 card (always), T1 one summary per named section, T2 records of the sections
marked T2 until the budget is spent. T3 evidence is only on request. Private
records are left out when the capability is public_facing. Every record line
carries its tier and date. The stable part (T0 plus T1) comes first so prompt
caching works. Packages are cached by (brand, capability, brain version).

A capability is a dict: id, brain_sections {section: "T1" or "T2"},
brain_budget, public_facing. A string id is looked up in OVERLAY, which S1.2b
writes, so agents/catalogue.json is never read here.

T1 summaries are built in code from record text until the summary agent
exists; each cites the record ids it covers.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from store import HERE, TIER_RANK, Brain

OVERLAY = HERE / "capabilities.overlay.json"
DEFAULT_BUDGET = 4000
T1_CHARS = 480  # about 120 tokens
_CACHE: dict[tuple, dict] = {}


def tokens(text: str) -> int:
    """Rough token count: 4 characters per token. No tokenizer needed."""
    return (len(text) + 3) // 4


def resolve(capability) -> dict:
    if isinstance(capability, dict):
        return capability
    caps = json.loads(OVERLAY.read_text(encoding="utf-8")) if OVERLAY.exists() else {}
    if capability not in caps:
        raise KeyError(f"capability {capability} has no brain_sections; see {OVERLAY.name}")
    return {"id": capability, **caps[capability]}


def _fact(rec: dict) -> str:
    if rec.get("text"):
        return rec["text"]
    return f"{rec.get('field') or rec['id'].split('.', 2)[2]}: {json.dumps(rec.get('value'), ensure_ascii=False)}"


def label(rec: dict) -> str:
    """Tier and date, e.g. "site_backed, 2026-09-28, 3 days old"."""
    parts = [rec["tier"], rec["date"]]
    if rec["age_days"] is not None:
        parts.append(f"{rec['age_days']} days old")
    if rec["status"] == "stale":
        parts.append("stale")
    if rec["tier"] == "unverified" and rec.get("added_by"):
        parts.append(f"added by {rec['added_by']}")
    return ", ".join(parts)


def line(rec: dict) -> str:
    return f"- [{label(rec)}] {rec['id']}: {_fact(rec)}"


def order(recs: list[dict]) -> list[dict]:
    """Active before stale, highest confidence first, then stronger tier, then id."""
    return sorted(recs, key=lambda r: (r["status"] != "active",
                                       -(r["confidence"] if r["confidence"] is not None else -1),
                                       TIER_RANK.get(r["tier"], 9), r["id"]))


def t0_card(brain: Brain, public: bool = False) -> str:
    recs = [r for r in brain.records() if not (public and r["visibility"] == "private")]
    by_sec: dict[str, list[dict]] = {}
    for r in recs:
        by_sec.setdefault(r["section"], []).append(r)

    def first(sec):
        live = order(by_sec.get(sec, []))
        return _fact(live[0]) if live else "unknown yet"

    out = [f"# {brain.brand}: brand card (T0)",
           f"Identity: {first('identity')}",
           f"Diagnosis: {first('diagnosis')}"]
    red = [r for r in recs if r["tier"] == "forbidden"]
    out.append("Red lines: " + ("; ".join(_fact(r) for r in red) if red else "none recorded"))
    claims = [r for r in order(by_sec.get("claims", [])) if r["tier"] in ("approved", "site_backed")][:5]
    out.append("Top claims:" + ("".join(f"\n{line(r)}" for r in claims) if claims else " none approved yet"))
    promos = [r for r in by_sec.get("offers", []) if r.get("field") == "current_promos" and r["status"] != "retired"]
    out.append("Current promos:" + ("".join(f"\n{line(r)}" for r in promos) if promos else " none recorded"))
    stale = {}
    for r in recs:
        if r["status"] == "stale":
            stale[r["section"]] = stale.get(r["section"], 0) + 1
    out.append("Freshness: " + ("; ".join(f"{n} stale in {s}" for s, n in sorted(stale.items()))
                                if stale else "all records in date"))
    return "\n".join(out)


def t1_summary(brain: Brain, section: str, public: bool = False) -> str:
    recs = order([r for r in brain.records(section) if not (public and r["visibility"] == "private")])
    if not recs:
        return f"## {section} (T1): no records yet."
    dates = [r["date"] for r in recs if r["date"] != "undated"]
    stale = sum(1 for r in recs if r["status"] == "stale")
    head = f"## {section} (T1): {len(recs)} records, last update {max(dates) if dates else 'undated'}, {stale} stale."
    body, ids = "", []
    for r in recs:
        fact = _fact(r)
        if body and len(body) + len(fact) + 1 > T1_CHARS:
            break
        body = f"{body} {fact}".strip()
        ids.append(r["id"])
    return f"{head}\n{body}\nCites: {', '.join(ids)}"


def package(brand: str, capability, budget: int | None = None, root: Path | None = None,
            today=None, use_cache: bool = True) -> dict:
    cap = resolve(capability)
    brain = Brain(brand, root, today)
    budget = budget or cap.get("brain_budget") or DEFAULT_BUDGET
    public = bool(cap.get("public_facing"))
    key = (brand, cap.get("id"), brain.version(), budget, public, brain.today)
    if use_cache and key in _CACHE:
        return _CACHE[key]

    sections = cap.get("brain_sections") or {}
    parts = [{"tier": "T0", "text": t0_card(brain, public)}]
    used = tokens(parts[0]["text"])
    for sec in sections:
        text = t1_summary(brain, sec, public)
        if used + tokens(text) > budget:
            break
        parts.append({"tier": "T1", "section": sec, "text": text})
        used += tokens(text)

    records = []
    for sec, tier in sections.items():
        if tier != "T2":
            continue
        for rec in order(brain.records(sec)):
            if public and rec["visibility"] == "private":
                continue
            text = line(rec)
            if used + tokens(text) > budget:
                break
            records.append({"id": rec["id"], "section": sec, "tier": rec["tier"], "date": rec["date"],
                            "age_days": rec["age_days"], "status": rec["status"],
                            "confidence": rec["confidence"], "text": text})
            used += tokens(text)
    if records:
        parts.append({"tier": "T2", "text": "## Records (T2)\n" + "\n".join(r["text"] for r in records)})

    result = {"brand": brand, "capability": cap.get("id"), "version": brain.version(),
              "budget": budget, "tokens": used, "public_facing": public,
              "parts": parts, "records": records,
              "text": "\n\n".join(p["text"] for p in parts)}
    _CACHE[key] = result
    return result


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    cap = json.loads(argv[1]) if argv[1].startswith("{") else argv[1]
    pkg = package(argv[0], cap, int(argv[2]) if len(argv) > 2 else None)
    print(pkg["text"])
    print(f"\n[{pkg['tokens']} of {pkg['budget']} tokens, brain {pkg['version']}]")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
