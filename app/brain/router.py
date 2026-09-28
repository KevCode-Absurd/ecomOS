"""Write `app/brain/<brand>/BRAIN.md`: the router a person or agent reads first.

Usage: python3 app/brain/router.py example

Contract: app/contracts/brand-brain.md section 5.1. The file holds the T0 card,
a section index, a routing table, the founder notes block and links to the
documents manifest and open questions. It is regenerated from records on every
publish and stays under 1,500 tokens. It copies nothing from skills, agents or
the data layer; it names them by path or id. The founder notes block between
the two markers is kept word for word across regeneration.
"""
from __future__ import annotations

import sys
from pathlib import Path

from package import _fact, order, t0_card, tokens
from store import SECTIONS, Brain

NOTES_START = "<!-- founder-notes:start -->"
NOTES_END = "<!-- founder-notes:end -->"
DEFAULT_NOTES = "Write anything here. Regeneration keeps this block as it is."
MAX_TOKENS = 1500

ROUTES = [
    ("Writing ad copy", "`claims`, `voice`, `avatars`, `language_bank`, then skill `agents/skills/CREA/ad-copy/SKILL.md`"),
    ("Pricing a promo", "`offers`, `economics`, then `finance_inputs` in the data layer and capability MONEY-C04"),
    ("A creative brief", "`products`, `offers`, `avatars`, `objections`, `voice`, `learnings`, `competitors`"),
    ("Site or landing page work", "`site_map`, `policies`, `claims`, `visual`"),
    ("Email and retention", "`calendar`, `offers`, `voice`, `learnings`"),
    ("Anything numeric", "the metric contract at `/api/metrics`, never this file"),
    ("Answering an objection", "`objection_ladders`, then `claims`"),
    ("Checking a claim for copy", "records with tier `approved` or `site_backed` only; the QA gate enforces it"),
]


def read_notes(path: Path) -> str:
    if not path.exists():
        return DEFAULT_NOTES
    text = path.read_text(encoding="utf-8")
    if NOTES_START in text and NOTES_END in text:
        return text.split(NOTES_START, 1)[1].split(NOTES_END, 1)[0].strip("\n")
    return DEFAULT_NOTES


def render(brain: Brain, notes: str) -> str:
    stats = brain.section_stats()
    out = [t0_card(brain), "", "## Sections", "",
           "| Section | Records | Last update | Gist |", "|---|---|---|---|"]
    empty = []
    for sec in SECTIONS:
        s = stats[sec]
        if not s["count"]:
            empty.append(sec)
            continue
        gist = _fact(order(brain.records(sec))[0])
        if len(gist) > 70:
            gist = gist[:67].rsplit(" ", 1)[0] + "..."
        stale = f", {s['stale']} stale" if s["stale"] else ""
        out.append(f"| [{sec}]({sec}.json) | {s['count']}{stale} | {s['last_update'] or 'undated'} | {gist} |")
    if empty:
        out += ["", "No records yet: " + ", ".join(empty) + "."]
    out += ["", "## Routing", "", "| For this work | Read |", "|---|---|"]
    out += [f"| {work} | {read} |" for work, read in ROUTES]
    docs = brain.documents()
    oq = stats["open_questions"]["count"]
    out += ["", "## Links", "",
            f"- Documents: [documents/manifest.json](documents/manifest.json), {len(docs)} file{'' if len(docs) == 1 else 's'}",
            f"- Open questions: [open_questions.json](open_questions.json), {oq} open",
            f"- Brain version {brain.version()}. Generated from records; edit records, not this file.",
            "", "## Founder notes", "", NOTES_START, notes, NOTES_END, ""]
    return "\n".join(out)


def write(brand: str, root: Path | None = None, today=None) -> Path:
    brain = Brain(brand, root, today)
    path = brain.dir / "BRAIN.md"
    text = render(brain, read_notes(path))
    if tokens(text) > MAX_TOKENS:
        raise ValueError(f"BRAIN.md for {brand} is {tokens(text)} tokens, over {MAX_TOKENS}")
    path.write_text(text, encoding="utf-8")
    return path


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    path = write(argv[0])
    print(f"wrote {path} ({tokens(path.read_text(encoding='utf-8'))} tokens)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
