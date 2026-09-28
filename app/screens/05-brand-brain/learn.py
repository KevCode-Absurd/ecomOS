"""Learn the voice from the founder's edits: what words they cut and what words they add, proposed to the voice sheet.

Every founder record that replaced an earlier value keeps that value in `history` (store.put). Comparing each
before and after, word by word, gives the words the founder removed and the words they added. A word removed in
2 or more edits (or once when it is on the generic hype list) is proposed for "words we avoid"; a word added in
2 or more edits is proposed for "words we use". Each proposal carries its evidence: the records and the before
and after snippets. Applying a proposal appends to the voice record; nothing is applied without the founder.
No model: a word diff and a count. Stop words and numbers are ignored.
"""
from __future__ import annotations

import re

STOP = set("the a an and or of to in on for with is are was were be it its this that these those you your we our us they them by as at from not no so if but than then there here can will just also very more most any all each every one two".split())
HYPE = {"premium", "elevate", "elevated", "leverage", "unlock", "unleash", "revolutionary", "game-changing", "ultimate", "luxurious", "cutting-edge", "seamless", "world-class", "best-in-class", "synergy", "curated", "bespoke", "innovative", "disruptive", "empower"}
MIN_REMOVED = 2
MIN_ADDED = 2


def _words(s) -> list[str]:
    if not isinstance(s, str):
        return []
    return [w for w in re.findall(r"[a-z][a-z'-]+", s.lower()) if w not in STOP and len(w) > 2]


def edits(brain) -> list[dict]:
    """Every founder edit that replaced a text value: before, after, the words cut and the words added."""
    out = []
    for r in brain.records():
        if (r.get("source") or {}).get("type") != "founder":
            continue
        after = r.get("text") if isinstance(r.get("text"), str) else (r.get("value") if isinstance(r.get("value"), str) else None)
        if not after:
            continue
        for h in r.get("history") or []:
            before = h.get("value") if isinstance(h.get("value"), str) else (h.get("text") if isinstance(h.get("text"), str) else None)
            if not before or before == after:
                continue
            bw, aw = set(_words(before)), set(_words(after))
            removed, added = sorted(bw - aw), sorted(aw - bw)
            if not removed and not added:
                continue
            out.append({"record": r["id"], "section": r["section"], "field": r.get("field"), "when": h.get("changed_at") or r["date"],
                        "before": before[:200], "after": after[:200], "removed": removed, "added": added})
    out.sort(key=lambda e: (e["when"] or "", e["record"]), reverse=True)
    return out


def proposals(brain, words_avoided: list[str], words_used: list[str]) -> dict:
    ed = edits(brain)
    removed: dict[str, list[dict]] = {}
    added: dict[str, list[dict]] = {}
    for e in ed:
        for w in e["removed"]:
            removed.setdefault(w, []).append(e)
        for w in e["added"]:
            added.setdefault(w, []).append(e)
    have_avoid, have_use = {w.lower() for w in words_avoided}, {w.lower() for w in words_used}
    avoid, use = [], []
    for w, evs in removed.items():
        if w in have_avoid:
            continue
        if len(evs) >= MIN_REMOVED or w in HYPE:
            avoid.append({"word": w, "times": len(evs), "hype": w in HYPE, "already": False,
                          "evidence": [{"record": e["record"], "before": e["before"][:120], "after": e["after"][:120]} for e in evs[:3]]})
    for w, evs in added.items():
        if w in have_use or w in HYPE:
            continue
        if len(evs) >= MIN_ADDED:
            use.append({"word": w, "times": len(evs), "already": False,
                        "evidence": [{"record": e["record"], "before": e["before"][:120], "after": e["after"][:120]} for e in evs[:3]]})
    avoid.sort(key=lambda p: (-p["times"], not p["hype"], p["word"]))
    use.sort(key=lambda p: (-p["times"], p["word"]))
    return {"edits": ed[:50], "counts": {"edits": len(ed), "avoid": len(avoid), "use": len(use)}, "avoid": avoid, "use": use,
            "rules": {"avoid": f"a word cut in {MIN_REMOVED} or more edits, or once when it is a hype word", "use": f"a word added in {MIN_ADDED} or more edits"},
            "note": "Learned from your edits only: the value before is in each record's history. Nothing reaches the voice sheet until you apply it."}
