"""The weekly audit: what in the brain and BRAIN.md should change, as proposals.

Usage: python3 app/brain/audit.py example

Contract: app/contracts/brand-brain.md section 7, clock 5. Each finding is a
proposal for the review queue with a kind, a target, a before, an after and a
reason. Nothing is written: the founder accepts or ignores each one. Kinds:

- stale: a record past its `expires_at`;
- conflict: two active records disagree on one field;
- empty: a section a room needs has no records;
- unread: a document in the manifest that was never extracted;
- drifted: a BRAIN.md section row or version line that no longer matches the records;
- broken_link: a link or path in BRAIN.md that points at a missing file.

No paid calls, no model calls.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import keeper
import router
from store import HERE, Brain

REPO = HERE.parents[1]
MD_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
CODE = re.compile(r"`([^`]+)`")


def _proposal(kind: str, target: str, before: str, after: str, reason: str) -> dict:
    return {"kind": kind, "target": target, "before": before, "after": after, "reason": reason}


def _rows(text: str) -> dict[str, str]:
    """Section table rows in BRAIN.md keyed by section name."""
    out = {}
    for ln in text.splitlines():
        m = re.match(r"\| \[([a-z_]+)\]\(", ln)
        if m:
            out[m.group(1)] = ln
    return out


def _version_line(text: str) -> str | None:
    return next((ln for ln in text.splitlines() if "Brain version" in ln), None)


def drift(brain: Brain) -> list[dict]:
    path = brain.dir / "BRAIN.md"
    if not path.exists():
        return [_proposal("drifted", "BRAIN.md", "missing", "regenerate with router.py",
                          "there is no BRAIN.md for this brand")]
    have = path.read_text(encoding="utf-8")
    want = router.render(brain, router.read_notes(path))
    out = []
    old, new = _rows(have), _rows(want)
    for sec in sorted(set(old) | set(new)):
        if old.get(sec) != new.get(sec):
            out.append(_proposal("drifted", f"BRAIN.md#{sec}", old.get(sec) or "no row",
                                 new.get(sec) or "no row", "the summary row no longer matches the records"))
    ov, nv = _version_line(have), _version_line(want)
    if ov != nv:
        out.append(_proposal("drifted", "BRAIN.md#version", ov or "no version line", nv,
                             "records changed since BRAIN.md was generated"))
    return out


def broken_links(brain: Brain, repo: Path = REPO) -> list[dict]:
    """Markdown links resolve from the brand folder; backticked paths from the repo root."""
    path = brain.dir / "BRAIN.md"
    if not path.exists():
        return []
    out, seen = [], set()
    for ln in path.read_text(encoding="utf-8").splitlines():
        targets = [(t, brain.dir / t) for t in MD_LINK.findall(ln) if "://" not in t]
        for t in CODE.findall(ln):
            t = t.strip()
            if not t.startswith("/") and ("/" in t or t.endswith((".json", ".md"))) and " " not in t:
                targets.append((t, repo / t))
        for t, p in targets:
            p = Path(str(p).split("#", 1)[0])
            if t in seen or p.exists():
                continue
            seen.add(t)
            out.append(_proposal("broken_link", f"BRAIN.md -> {t}", ln.strip(),
                                 f"create {t}, or point this row at a file that exists",
                                 "the link points at a missing file"))
    return out


def audit(brand, repo: Path = REPO) -> list[dict]:
    brain = brand if isinstance(brand, Brain) else Brain(brand)
    bank = keeper.load_bank()
    out = []
    for g in keeper.gaps(brain, bank):
        if g["kind"] == "expired":
            rec = brain.get(g["record"])
            out.append(_proposal("stale", g["record"], f"{rec.get('text') or rec.get('value')} "
                                 f"(expired {g['expires_at']})",
                                 "re-pull from its source or confirm it; retire it if no longer true",
                                 "the record is past its expiry date"))
        elif g["kind"] == "conflict":
            out.append(_proposal("conflict", g["field"], "; ".join(
                f"{rid} = {v}" for rid, v in zip(g["records"], g["values"])),
                "keep one value and retire the other", "two active records disagree"))
    stats = brain.section_stats()
    needs: dict[str, set] = {}
    for q in bank:
        for f in q["fills"]:
            needs.setdefault(f.split(".")[0], set()).update(q["unblocks_rooms"])
    for sec in sorted(needs):
        if sec in stats and not stats[sec]["count"]:
            out.append(_proposal("empty", sec, "no records",
                                 "fill from a connected source or the keeper's ask",
                                 "rooms need it: " + ", ".join(sorted(needs[sec]))))
    for d in brain.documents():
        if not d.get("extracted"):
            out.append(_proposal("unread", d["file"], "not extracted",
                                 "run the document extractor into " + ", ".join(d.get("sections") or []),
                                 "added but never read"))
    out += drift(brain)
    out += broken_links(brain, repo)
    return out


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    for p in audit(argv[0]):
        print(f"{p['kind']}: {p['target']}\n  before: {p['before']}\n  after:  {p['after']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
