"""The keeper: what the brain is missing, and the few questions worth asking.

Usage: python3 app/brain/keeper.py example [--connected shopify,klaviyo] [--declined quickbooks]

Contract: app/contracts/brand-brain.md sections 6.1 and 7 (the scheduled ask).
`gaps(brain)` lists expired records, empty fields a room needs, conflicts and
low-confidence records. `ask(brain, connected, declined, n=5)` applies the
pull-first rule from `questions.bank.json` and `sources.registry.json`:

- a question whose fields are filled and healthy is not asked;
- a question a connected source answers is dropped (the next sync fills it);
- a question a not-connected private source could answer becomes
  "connect X, or answer this in a line";
- a declined source is never offered again, nor is any source in its category
  (a brand connects at most one per category), so its questions are asked plainly;
- public sources run for every brand, so they are never offered and never drop
  a question: if one ran and the field is still empty, the question stands.

Importance is weight x blocked rooms. Money at stake is not computable yet, so
that factor is 1. Ties go to the higher weight, then the id. No paid calls.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from store import HERE, Brain

LOW_CONFIDENCE = 0.5
BANK = HERE / "questions.bank.json"
REGISTRY = HERE / "sources.registry.json"


def load_bank(path: Path = BANK) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))["questions"]


def load_registry(path: Path = REGISTRY) -> dict[str, dict]:
    return {s["id"]: s for s in json.loads(path.read_text(encoding="utf-8"))["sources"]}


def _as_brain(brand) -> Brain:
    return brand if isinstance(brand, Brain) else Brain(brand)


def _split(field: str) -> tuple[str, str | None]:
    """"economics.gross_margin_pct" -> ("economics", "gross_margin_pct"); "avatars" -> ("avatars", None)."""
    sec, _, name = field.partition(".")
    return sec, name or None


def _matches(rec: dict, field: str) -> bool:
    sec, name = _split(field)
    return rec["section"] == sec and (name is None or rec.get("field") == name)


def _conflicts(recs: list[dict]) -> list[dict]:
    """Active records that share a section and field but hold different scalar values.

    Dict and list values (an avatar, a story) are many-per-field by design, so
    they are never a conflict.
    """
    groups: dict[tuple, list[dict]] = {}
    for r in recs:
        v = r.get("value")
        if r.get("field") and v is not None and not isinstance(v, (dict, list)):
            groups.setdefault((r["section"], r["field"]), []).append(r)
    out = []
    for (sec, field), group in sorted(groups.items()):
        if len({json.dumps(r["value"], sort_keys=True) for r in group}) > 1:
            out.append({"kind": "conflict", "section": sec, "field": f"{sec}.{field}",
                        "records": sorted(r["id"] for r in group),
                        "values": [r["value"] for r in sorted(group, key=lambda r: r["id"])]})
    return out


def gaps(brand, bank: list[dict] | None = None) -> list[dict]:
    """Everything still missing after the pull: expired, empty, conflict, low_confidence."""
    brain = _as_brain(brand)
    bank = load_bank() if bank is None else bank
    recs = brain.records()
    out = []
    for r in recs:
        if r["status"] == "stale":
            out.append({"kind": "expired", "section": r["section"], "record": r["id"],
                        "expires_at": r.get("expires_at")})
    rooms_by_field: dict[str, set] = {}
    for q in bank:
        for f in q["fills"]:
            rooms_by_field.setdefault(f, set()).update(q["unblocks_rooms"])
    for f in sorted(rooms_by_field):
        if not any(_matches(r, f) for r in recs):
            out.append({"kind": "empty", "section": _split(f)[0], "field": f,
                        "rooms": sorted(rooms_by_field[f])})
    out += _conflicts(recs)
    for r in recs:
        c = r.get("confidence")
        if c is not None and c < LOW_CONFIDENCE:
            out.append({"kind": "low_confidence", "section": r["section"], "record": r["id"],
                        "confidence": c})
    return out


def _open_fields(q: dict, gap_list: list[dict], recs: list[dict]) -> list[str]:
    """The question's fields that are empty, or whose records are stale, conflicted or weak."""
    empty = {g["field"] for g in gap_list if g["kind"] == "empty"}
    weak_ids = {g["record"] for g in gap_list if g["kind"] in ("expired", "low_confidence")}
    weak_ids |= {rid for g in gap_list if g["kind"] == "conflict" for rid in g["records"]}
    out = []
    for f in q["fills"]:
        if f in empty or any(r["id"] in weak_ids and _matches(r, f) for r in recs):
            out.append(f)
    return out


def ask(brand, connected_sources=(), declined_sources=(), n: int = 5,
        bank: list[dict] | None = None, registry: dict | None = None) -> list[dict]:
    """The top n questions for this round, ranked by weight x blocked rooms."""
    brain = _as_brain(brand)
    bank = load_bank() if bank is None else bank
    registry = load_registry() if registry is None else registry
    connected, declined = set(connected_sources), set(declined_sources)
    declined_cats = {registry[s]["category"] for s in declined if s in registry}
    recs = brain.records()
    gap_list = gaps(brain, bank)
    asks = []
    for q in bank:
        fields = _open_fields(q, gap_list, recs)
        if not fields:
            continue
        if connected & set(q["answerable_by"]):
            continue
        offer = [s for s in q["answerable_by"]
                 if s in registry and registry[s]["access"] != "public"
                 and s not in declined and registry[s]["category"] not in declined_cats]
        rooms = sorted(q["unblocks_rooms"])
        item = {"id": q["id"], "asks": q["asks"], "why": q["why"], "fills": fields,
                "rooms": rooms, "weight": q["weight"], "importance": q["weight"] * len(rooms),
                "kind": "connect_or_answer" if offer else "plain", "connect": offer,
                "attach": True}
        if offer:
            names = " or ".join(registry[s]["name"] for s in offer[:3])
            item["text"] = f"Connect {names}, or answer this in a line: {q['asks']} ({q['why']})"
        else:
            item["text"] = q["asks"]
        asks.append(item)
    asks.sort(key=lambda a: (-a["importance"], -a["weight"], a["id"]))
    return asks[:n]


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    opts = {"--connected": [], "--declined": []}
    for i, a in enumerate(argv[1:], 1):
        if a in opts and i + 1 < len(argv):
            opts[a] = [s for s in argv[i + 1].split(",") if s]
    for a in ask(argv[0], opts["--connected"], opts["--declined"]):
        print(f"[{a['importance']}] {a['text']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
