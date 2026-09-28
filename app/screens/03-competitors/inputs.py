"""First-party records the team logs on this screen, so rules can read what no public signal holds.

One local file per brand, `fixtures/inputs/<brand>.json`, git-ignored and never sent anywhere. Each kind has a
validator; a record that fails is refused with the reason, never half saved. No free text about a person is kept:
an interview stores the outcome, the named competitor, one reason code and the date, never a name or a quote.

Kinds:
  interview   a win-loss interview (BRAND-C58): outcome win or loss, competitor from the names on file, reason code
"""
from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
FOLDER = HERE / "fixtures" / "inputs"
MAX_ROWS = 5000
REASON_CODES = ["price and value", "durability", "fit and sizing", "comfort and feel", "style", "availability", "trust", "other"]
SAFE_BRAND = re.compile(r"^[a-z0-9_-]+$")


def path(brand: str) -> Path:
    if not SAFE_BRAND.match(brand):
        raise ValueError("bad brand")
    return FOLDER / f"{brand}.json"


def read(brand: str, kind: str | None = None) -> list[dict]:
    try:
        rows = json.loads(path(brand).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        rows = []
    return [r for r in rows if isinstance(r, dict) and (kind is None or r.get("kind") == kind)]


def _date(v, today: dt.date) -> str | None:
    try:
        d = dt.date.fromisoformat(str(v))
    except ValueError:
        return None
    return d.isoformat() if d <= today else None


def _interview(body: dict, known: dict, today: dt.date) -> tuple[dict | None, str | None]:
    outcome, comp, reason = str(body.get("outcome") or ""), str(body.get("competitor") or ""), str(body.get("reason") or "")
    if outcome not in ("win", "loss"):
        return None, "outcome must be win or loss"
    names = known.get("competitors") or []
    match = next((n for n in names if n.lower() == comp.strip().lower()), None)
    if not match:
        return None, "competitor must be one of: " + ", ".join(names)
    if reason not in REASON_CODES:
        return None, "reason must be one of: " + ", ".join(REASON_CODES)
    day = _date(body.get("date") or today.isoformat(), today)
    if not day:
        return None, "date must be YYYY-MM-DD and not in the future"
    return {"outcome": outcome, "competitor": match, "reason": reason, "date": day}, None


VALIDATE = {"interview": _interview}


def add(brand: str, kind: str, body, known: dict, today: dt.date) -> tuple[int, dict]:
    if kind not in VALIDATE:
        return 400, {"error": "kind must be one of: " + ", ".join(VALIDATE)}
    if not isinstance(body, dict):
        return 400, {"error": "body must be an object"}
    rec, err = VALIDATE[kind](body, known, today)
    if err:
        return 400, {"error": err}
    rows = read(brand)
    if len(rows) >= MAX_ROWS:
        return 400, {"error": "the inputs file is full"}
    n = 1 + max((int(str(r.get("id", "x-0")).rsplit("-", 1)[-1]) for r in rows if str(r.get("id", "")).rsplit("-", 1)[-1].isdigit()), default=0)
    rec = {"id": f"{kind}-{n:04d}", "kind": kind, **rec, "by": str(body.get("by") or "team")[:40],
           "logged_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
    rows.append(rec)
    p = path(brand)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(rows, indent=1), encoding="utf-8")
    return 201, {"ok": True, "record": rec}


def win_loss(rows: list[dict], names: list[str], repeat_at: int = 3) -> dict:
    """Win rate by named competitor (wins / (wins + losses)) and loss reasons counted; a reason at repeat_at or more
    losses against one name is a repeat."""
    by = []
    for name in names:
        xs = [r for r in rows if r.get("competitor") == name]
        w, lo = sum(1 for r in xs if r["outcome"] == "win"), sum(1 for r in xs if r["outcome"] == "loss")
        reasons: dict[str, int] = {}
        for r in xs:
            if r["outcome"] == "loss":
                reasons[r["reason"]] = reasons.get(r["reason"], 0) + 1
        top = max(reasons.items(), key=lambda kv: (kv[1], kv[0])) if reasons else None
        by.append({"name": name, "wins": w, "losses": lo, "n": w + lo, "win_rate": round(w / (w + lo), 3) if w + lo else None,
                   "reasons": dict(sorted(reasons.items(), key=lambda kv: (-kv[1], kv[0]))),
                   "repeat": {"reason": top[0], "n": top[1]} if top and top[1] >= repeat_at else None})
    total = sum(x["n"] for x in by)
    wins = sum(x["wins"] for x in by)
    return {"rows": by, "n": total, "win_rate": round(wins / total, 3) if total else None, "repeat_at": repeat_at}
