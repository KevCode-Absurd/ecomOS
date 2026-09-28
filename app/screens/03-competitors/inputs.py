"""First-party records the team logs on this screen, so rules can read what no public signal holds.

One local file per brand, `fixtures/inputs/<brand>.json`, git-ignored and never sent anywhere. Each kind has a
validator; a record that fails is refused with the reason, never half saved. No free text about a person is kept:
an interview stores the outcome, the named competitor, one reason code and the date, never a name or a quote.

Kinds:
  interview   a win-loss interview (BRAND-C58): outcome win or loss, competitor from the names on file, reason code
  price_seen  a rival price a person saw on their site (the price capture the room asks for): tracked page, product
              label, price in dollars, units in the pack, date, and an optional https source link
  card_check  a person checked every line of one direct page's battlecard against their site today: page, date, and how
              many lines were dropped as no longer true. The card's freshness counts from the latest check.
  frame_test  a positioning poll result: the challenger line (a key the frames block offers), shoppers asked, how many
              preferred it and how many preferred the current line
  threshold   a rule threshold tuned on the page: name (a tunable the audit lists) and value inside its range; the
              newest change per name wins over the brain's competitor_thresholds record
Price rule (the room's "competitor cut price sharply"): per page and product, the latest price per unit against the
mean of that product's earlier records in the trailing TRAIL_DAYS (30) days; a move of the price move threshold or
more is a cut or a raise. With no earlier record in the window there is no baseline, and no move.
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


SAFE_TEXT = re.compile(r"^[A-Za-z0-9 .,&'()/+-]{1,60}$")
TRAIL_DAYS = 30


def _price_seen(body: dict, known: dict, today: dt.date) -> tuple[dict | None, str | None]:
    pages = known.get("pages") or []
    page = next((n for n in pages if n.lower() == str(body.get("page") or "").strip().lower()), None)
    if not page:
        return None, "page must be one of the tracked pages: " + ", ".join(pages)
    product = str(body.get("product") or "").strip()
    if not SAFE_TEXT.match(product):
        return None, "product must be a short label (letters, digits, up to 60)"
    try:
        u = body.get("units")
        price, units = float(body.get("price")), int(1 if u in (None, "") else u)
    except (TypeError, ValueError):
        return None, "price must be a number and units a whole number"
    if not (0 < price < 10000) or not (1 <= units <= 100):
        return None, "price must be above 0 and under 10,000; units 1 to 100"
    day = _date(body.get("date") or today.isoformat(), today)
    if not day:
        return None, "date must be YYYY-MM-DD and not in the future"
    url = str(body.get("url") or "").strip()
    if url and not re.match(r"^https://[A-Za-z0-9.-]+(/[^\s]*)?$", url):
        return None, "source must be an https link"
    return {"page": page, "product": product, "price": round(price, 2), "units": units, "per_unit": round(price / units, 2),
            "date": day, "url": url[:300] or None}, None


def price_moves(rows: list[dict], threshold: float, frames: dict | None = None) -> dict:
    """Per page and product: the latest price per unit against the mean of the earlier records in the trailing window."""
    groups: dict[tuple, list[dict]] = {}
    for r in rows:
        groups.setdefault((r["page"], r["product"].lower()), []).append(r)
    moves, based = [], 0
    for (page, _), xs in sorted(groups.items()):
        xs.sort(key=lambda r: (r["date"], r["id"]))
        last = xs[-1]
        start = (dt.date.fromisoformat(last["date"]) - dt.timedelta(days=TRAIL_DAYS)).isoformat()
        prior = [r["per_unit"] for r in xs[:-1] if start <= r["date"] <= last["date"]]
        if not prior:
            continue
        based += 1
        avg = sum(prior) / len(prior)
        ch = (last["per_unit"] - avg) / avg
        if abs(ch) >= threshold:
            moves.append({"page": page, "product": last["product"], "frame": (frames or {}).get(page), "from": round(avg, 2),
                          "to": last["per_unit"], "change": round(ch, 3), "kind": "cut" if ch < 0 else "raise",
                          "since": min(r["date"] for r in xs[:-1] if start <= r["date"]), "when": last["date"],
                          "source": "logged", "records": len(prior) + 1, "url": last.get("url")})
    return {"moves": sorted(moves, key=lambda r: r["change"]), "with_baseline": based, "records": len(rows)}


def _card_check(body: dict, known: dict, today: dt.date) -> tuple[dict | None, str | None]:
    pages = known.get("direct") or []
    page = next((n for n in pages if n.lower() == str(body.get("page") or "").strip().lower()), None)
    if not page:
        return None, "page must be a direct page with a battlecard: " + ", ".join(pages)
    day = _date(body.get("date") or today.isoformat(), today)
    if not day:
        return None, "date must be YYYY-MM-DD and not in the future"
    try:
        dropped = int(body.get("dropped") or 0)
    except (TypeError, ValueError):
        return None, "dropped must be a whole number"
    if not 0 <= dropped <= 20:
        return None, "dropped must be 0 to 20"
    return {"page": page, "date": day, "dropped": dropped}, None


def card_checks(rows: list[dict]) -> dict:
    """The latest check per page: {page: record}."""
    out: dict[str, dict] = {}
    for r in sorted(rows, key=lambda r: (r["date"], r["id"])):
        out[r["page"]] = r
    return out


def _frame_test(body: dict, known: dict, today: dt.date) -> tuple[dict | None, str | None]:
    keys = known.get("lines") or []
    line = str(body.get("line") or "").strip().upper()
    if line not in keys:
        return None, "line must be one of: " + (", ".join(keys) or "no challenger line on file")
    try:
        asked, new, cur = (int(body.get(k)) for k in ("asked", "prefer_new", "prefer_current"))
    except (TypeError, ValueError):
        return None, "asked, prefer_new and prefer_current must be whole numbers"
    if not (20 <= asked <= 100000) or new < 0 or cur < 0 or new + cur > asked:
        return None, "asked must be 20 to 100,000, and the two preferences must add up to no more than asked"
    day = _date(body.get("date") or today.isoformat(), today)
    if not day:
        return None, "date must be YYYY-MM-DD and not in the future"
    return {"line": line, "asked": asked, "prefer_new": new, "prefer_current": cur, "date": day}, None


def _threshold(body: dict, known: dict, today: dt.date) -> tuple[dict | None, str | None]:
    ranges = known.get("tunable") or {}
    name = str(body.get("name") or "")
    if name not in ranges:
        return None, "name must be one of: " + ", ".join(ranges)
    try:
        value = float(body.get("value"))
    except (TypeError, ValueError):
        return None, "value must be a number"
    lo, hi = ranges[name]
    if not lo <= value <= hi:
        return None, f"{name} must be {lo:g} to {hi:g}"
    return {"name": name, "value": int(value) if value == int(value) and isinstance(lo, int) else value, "date": today.isoformat()}, None


def thresholds(rows: list[dict]) -> dict:
    """The newest change per threshold name."""
    out: dict[str, dict] = {}
    for r in sorted(rows, key=lambda r: (r.get("logged_at", ""), r["id"])):
        out[r["name"]] = r
    return out


VALIDATE = {"interview": _interview, "price_seen": _price_seen, "card_check": _card_check, "frame_test": _frame_test,
            "threshold": _threshold}


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


def remove(brand: str, rec_id: str) -> tuple[int, dict]:
    """Take back one record logged by mistake. The rules read the file again on the next load."""
    rows = read(brand)
    keep = [r for r in rows if r.get("id") != rec_id]
    if len(keep) == len(rows):
        return 404, {"error": "no record with that id"}
    path(brand).write_text(json.dumps(keep, indent=1), encoding="utf-8")
    return 200, {"ok": True, "removed": rec_id}


def summary(r: dict) -> str:
    k = r.get("kind")
    if k == "interview":
        return f"{r['outcome']} against {r['competitor']}: {r['reason']}"
    if k == "price_seen":
        return f"{r['page']} {r['product']}: ${r['price']:.2f} for {r['units']} (${r['per_unit']:.2f} each)"
    if k == "card_check":
        return f"{r['page']} battlecard checked, {r['dropped']} lines dropped"
    if k == "frame_test":
        return f"line {r['line']}: {r['prefer_new']} to {r['prefer_current']} of {r['asked']} asked"
    if k == "threshold":
        return f"{r['name'].replace('_', ' ')} set to {r['value']:g}"
    return k or "record"


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
