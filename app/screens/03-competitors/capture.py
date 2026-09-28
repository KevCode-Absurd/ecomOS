"""Dated page-summary captures and their diffs: launch alerts that work before any ad-level snapshot.

A capture is `fixtures/captures/<brand>/<YYYY-MM-DD>.json`: per tracked page the summary the brain holds
that day (active ads, formats, offers seen, angle tags, median days live, longest ad start). Writing one
reads only the brain; nothing external, nothing paid. Run it after each brain refresh:

    python3 app/screens/03-competitors/capture.py --brand bombas

Diff rules between the latest two captures, per page (constants below):
  ads_up       active ads up SURGE (25 percent) or more and by MIN_ADS (10) or more: a push
  ads_down     active ads down SURGE or more: a pull back
  new_format   a format with MIN_FORMAT_SHARE (5 percent) of ads that was absent before
  new_offer    an offer seen that was not seen before
  dropped_offer an offer no longer seen
  new_angle    an angle tag not seen before
  new_channel  a placement (Instagram, Threads, WhatsApp, Audience Network) not seen before: the room's
               "competitor entered a new channel" rule
  new_flight   the longest running ad started after the previous capture: every ad is new
With an ad-level snapshot the same alerts come from snapshot.py rows instead (changes.diff).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FOLDER = HERE / "fixtures" / "captures"
SURGE, MIN_ADS, MIN_FORMAT_SHARE = 0.25, 10, 0.05
PRICE_MOVE = 0.15       # the room rule: a median price per pair moves 15 percent or more between captures


def summary(pages: list[dict]) -> dict:
    out = {}
    for p in pages:
        if p["source"] == "none":
            continue
        out[p["key"]] = {"name": p["name"], "role": p["role"], "frame": p["frame"], "active_ads": p["active_ads"],
                         "formats": p["formats"], "offers": sorted(p.get("offers_seen") or []),
                         "angles": sorted({a["tag"] for a in p.get("angles") or []}), "median_days": p.get("median_days"),
                         "longest_start": p.get("longest_start"), "price_text": p.get("price_text"),
                         "platforms": p.get("platforms") or [], "points": (p.get("verdict") or {}).get("points")}
    return out


def write(brand: str, pages: list[dict], day: dt.date, folder: Path | None = None) -> Path:
    path = (folder or FOLDER) / brand / f"{day.isoformat()}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"brand": brand, "captured_at": day.isoformat(), "source": "brain page summaries",
                                "pages": summary(pages)}, indent=1, sort_keys=True), encoding="utf-8")
    return path


def captures(brand: str, folder: Path | None = None) -> list[Path]:
    d = (folder or FOLDER) / brand
    return sorted(d.glob("????-??-??.json")) if d.is_dir() else []


def latest_two(brand: str, folder: Path | None = None) -> tuple[dict | None, dict | None]:
    ps = captures(brand, folder)
    load = lambda p: json.loads(p.read_text(encoding="utf-8"))  # noqa: E731
    return (load(ps[-2]) if len(ps) >= 2 else None), (load(ps[-1]) if ps else None)


def diff(prev: dict | None, cur: dict | None) -> list[dict]:
    if not prev or not cur:
        return []
    out = []
    when = cur["captured_at"]
    for key, b in cur["pages"].items():
        a = prev["pages"].get(key)
        if not a or b.get("role") == "self":
            continue
        name = b["name"]
        ev = lambda kind, text, value=None: out.append({"when": when, "page": name, "kind": kind, "text": text, "value": value,  # noqa: E731
                                                        "since": prev["captured_at"]})
        x, y = a.get("active_ads"), b.get("active_ads")
        if isinstance(x, int) and isinstance(y, int) and x:
            ch = (y - x) / x
            if ch >= SURGE and y - x >= MIN_ADS:
                ev("ads_up", f"active ads up {round(ch * 100)} percent, {x} to {y}", y - x)
            elif ch <= -SURGE:
                ev("ads_down", f"active ads down {round(-ch * 100)} percent, {x} to {y}", y - x)
        n = sum((b.get("formats") or {}).values())
        for f, c in sorted((b.get("formats") or {}).items()):
            if n and c / n >= MIN_FORMAT_SHARE and not (a.get("formats") or {}).get(f):
                ev("new_format", f"started running {f} ({c} ads)", f)
        for o in sorted(set(b.get("offers") or []) - set(a.get("offers") or [])):
            ev("new_offer", f"new offer seen: {o}", o)
        for o in sorted(set(a.get("offers") or []) - set(b.get("offers") or [])):
            ev("dropped_offer", f"offer no longer seen: {o}", o)
        if a.get("platforms"):   # an older capture without platforms cannot say what is new
            for pl in sorted(set(b.get("platforms") or []) - set(a.get("platforms") or [])):
                ev("new_channel", f"now running on {pl.replace('_', ' ')}", pl)
        for g in sorted(set(b.get("angles") or []) - set(a.get("angles") or [])):
            ev("new_angle", f"new angle: {g}", g)
        if b.get("longest_start") and b["longest_start"] > prev["captured_at"]:
            ev("new_flight", f"every ad is new since {prev['captured_at']}", b["longest_start"])
    return out


def history(brand: str, folder: Path | None = None, last: int = 12) -> dict:
    """Threat points and active ads per page across the dated captures, oldest first. A page missing from a capture reads None."""
    caps = [json.loads(p.read_text(encoding="utf-8")) for p in captures(brand, folder)[-last:]]
    dates = [c["captured_at"] for c in caps]
    keys = []
    for c in caps:
        for k, v in c["pages"].items():
            if v.get("role") != "self" and k not in keys:
                keys.append(k)
    rows = []
    for k in keys:
        name = next(c["pages"][k]["name"] for c in caps if k in c["pages"])
        rows.append({"key": k, "name": name, "points": [(c["pages"].get(k) or {}).get("points") for c in caps],
                     "active_ads": [(c["pages"].get(k) or {}).get("active_ads") for c in caps]})
    return {"dates": dates, "rows": rows}


def price_moves(prev: dict | None, cur: dict | None, parse) -> list[dict]:
    """Median price per pair per page between the latest two captures; a move of PRICE_MOVE or more is a price move."""
    if not prev or not cur:
        return []
    out = []
    for key, b in cur["pages"].items():
        a = prev["pages"].get(key)
        if not a or b.get("role") == "self":
            continue
        x, y = parse(a.get("price_text"))["median"], parse(b.get("price_text"))["median"]
        if x and y and abs(y - x) / x >= PRICE_MOVE:
            ch = (y - x) / x
            out.append({"page": b["name"], "frame": b.get("frame"), "from": x, "to": y, "change": round(ch, 3),
                        "kind": "cut" if ch < 0 else "raise", "since": prev["captured_at"], "when": cur["captured_at"]})
    return sorted(out, key=lambda r: r["change"])


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--brand", default="bombas")
    ap.add_argument("--date", help="capture date, default the brain's today")
    ns = ap.parse_args()
    sys.path.insert(0, str(HERE))
    import audit  # noqa: E402
    day = dt.date.fromisoformat(ns.date) if ns.date else dt.date.today()
    m = audit.market_full(ns.brand, day)
    print(write(ns.brand, m["pages"], day))
    print(audit.handmod.write_snapshot(m, audit.parse_band))   # the competitor_snapshot hand-off (events.md)
