"""Start a session small. Prints what one session reads, writes and must achieve,
and answers the spec queries a session needs instead of opening the big files.

  python3 scripts/session.py S1.2a                 the session card with token estimates
  python3 scripts/session.py --list [stage]        all sessions, or one stage
  python3 scripts/session.py --room "Paid social"  one room from agents/rooms/rooms.json, compact
  python3 scripts/session.py --capability MEDIA-C04
  python3 scripts/session.py --capabilities MEDIA  ids and names for one agent
  python3 scripts/session.py --contract 3,5        numbered sections of app/contracts/brand-brain.md
  python3 scripts/session.py --sample bombas offers [n]

catalogue.json is about 300k tokens and rooms.json about 180k. No session opens them.
"""
from __future__ import annotations

import json
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SESSIONS = ROOT / "sessions" / "sessions.json"


def tokens(path: Path) -> int:
    if path.is_dir():
        return sum(tokens(p) for p in path.rglob("*") if p.is_file())
    return path.stat().st_size // 4 if path.exists() else 0


def load_sessions():
    return json.loads(SESSIONS.read_text(encoding="utf-8"))["sessions"]


def card(sid: str) -> int:
    for s in load_sessions():
        if s["id"] == sid:
            break
    else:
        print(f"no session {sid}")
        return 1
    print(f"{s['id']}  {s['title']}  [stage {s['stage']}, {s['model']}, budget {s['budget_tokens']:,} tokens]")
    if s["needs"]:
        print(f"needs: {', '.join(s['needs'])}")
    print("\nfirst line:\n  " + s["first_line"])
    print("\nreads:")
    total = 0
    for r in s["reads"]:
        path = ROOT / r.split("#")[0].split(" ")[0]
        t = tokens(path) if path.exists() else 0
        if "#" in r and path.exists():
            secs = r.split("#")[1].split(",")
            t = sum(len(x) // 4 for x in contract_sections(secs).values())
        total += t
        print(f"  {t:>7,}  {r}")
    print(f"  {total:>7,}  total at start (target under {s['budget_tokens']:,})")
    print("\nwrites:")
    for w in s["writes"]:
        print(f"  {w}")
    print("\ndone when:\n  " + s["done_when"])
    return 0


def list_sessions(stage: str | None):
    for s in load_sessions():
        if stage and str(s["stage"]) != stage:
            continue
        par = f" (parallel {s['parallel_group']})" if s.get("parallel_group") else ""
        print(f"{s['id']:<6} {s['model']:<22} {s['budget_tokens']:>7,}  {s['title']}{par}")


def contract_sections(numbers, path: Path | None = None) -> dict:
    """Return {number: text} for '## N.' or '### N.M' sections of the brain contract."""
    path = path or ROOT / "app" / "contracts" / "brand-brain.md"
    text = path.read_text(encoding="utf-8")
    out = {}
    for n in numbers:
        n = n.strip()
        m = re.search(rf"^#{{2,3}} {re.escape(n)}\.? .*?(?=^#{{2,{2 if '.' not in n else 3}}} |\Z)", text, re.S | re.M)
        out[n] = m.group(0) if m else f"(section {n} not found)"
    return out


def room(name: str):
    rooms = json.loads((ROOT / "agents" / "rooms" / "rooms.json").read_text(encoding="utf-8"))
    for r in rooms:
        if r["room"].lower() == name.lower():
            compact = {k: r[k] for k in ("room", "agent", "who_uses", "jobs", "metrics", "insights", "actions", "data_needs") if k in r}
            print(json.dumps(compact, indent=1)[:12000])
            return 0
    print("rooms:", ", ".join(r["room"] for r in rooms))
    return 1


def capability(cid: str):
    for c in json.loads((ROOT / "agents" / "catalogue.json").read_text(encoding="utf-8")):
        if c.get("id") == cid:
            print(json.dumps(c, indent=1))
            return 0
    print(f"no capability {cid}")
    return 1


def capabilities(agent: str):
    cats = json.loads((ROOT / "agents" / "catalogue.json").read_text(encoding="utf-8"))
    rows = [c for c in cats if str(c.get("agent", c.get("id", ""))).upper().startswith(agent.upper()) or str(c.get("id", "")).startswith(agent.upper() + "-")]
    for c in rows:
        print(f"{c.get('id')}\t{c.get('name', '')[:90]}")
    print(f"{len(rows)} capabilities")


def sample(brand: str, section: str, n: int = 30):
    path = ROOT / "app" / "brain" / brand / f"{section}.json"
    recs = json.loads(path.read_text(encoding="utf-8"))
    random.seed(7)
    for r in random.sample(recs, min(n, len(recs))):
        src = r.get("source", {})
        print(f"- [{r.get('tier', 'unverified')}] {r.get('text') or r.get('value')}  ({src.get('type', 'no source')}, {src.get('captured_at', '')})")


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    a = argv[1]
    if a == "--list":
        return list_sessions(argv[2] if len(argv) > 2 else None)
    if a == "--room":
        return room(" ".join(argv[2:]))
    if a == "--capability":
        return capability(argv[2])
    if a == "--capabilities":
        return capabilities(argv[2])
    if a == "--contract":
        for n, t in contract_sections(argv[2].split(",")).items():
            print(t)
        return 0
    if a == "--sample":
        return sample(argv[2], argv[3], int(argv[4]) if len(argv) > 4 else 30)
    return card(a)


if __name__ == "__main__":
    sys.exit(main(sys.argv) or 0)
