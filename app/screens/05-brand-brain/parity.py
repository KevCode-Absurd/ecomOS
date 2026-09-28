"""Marketplace parity: is someone undercutting our price on Amazon, and is the listing ours?

Reads the brain only: marketplaces records the Amazon pull wrote (title, price, stars, reviews, seller), the
brand's own price ladders in products (min price per line is the single-pair floor), and two founder records
in offers: `map_usd_per_pair` (minimum advertised price per pair) and `marketplace_seller_names` (the seller
names that are ours). Both read unavailable until the founder sets them; nothing here guesses them.

Per listing, in code: pack count from the title, price per pair, the line it belongs to, and flags:
  under_site     price per pair under the site's single-pair floor by more than TOLERANCE;
  below_map      price per pair under the MAP (only when MAP is set);
  seller_unknown the pull carried no seller name (a listing actor with the seller field, or the Selling Partner
                 API, fills it);
  unrecognised   the seller is not in the founder's list (only when both are known).
Each flag ends in an action. Rules BRN-R15 (below MAP) and BRN-R16 (unrecognised seller) fire only when the
inputs exist; when they do not, one unavailable finding names the connector that fills them.
"""
from __future__ import annotations

import re

TOLERANCE = 0.35   # a site multi-pack sells for less per pair than a single; only a gap past this is a parity flag
PACK = re.compile(r"(\d+)\s*[- ]?\s*(?:pair|pack|pk|count|ct)\b", re.I)
LINES = [("socks", ["sock", "no show", "no-show", "ankle", "calf", "crew", "knee high"]), ("underwear", ["underwear", "boxer", "brief", "thong", "bikini"]),
         ("t_shirts", ["t-shirt", "tee", "shirt"]), ("slippers", ["slipper", "moccasin", "clog", "sandal"]), ("sleeves", ["sleeve"])]


def pack_count(title: str) -> int:
    m = PACK.search(title or "")
    if m:
        n = int(m.group(1))
        return n if 1 <= n <= 24 else 1
    return 1


def line_of(title: str) -> str | None:
    t = (title or "").lower()
    for key, words in LINES:
        if any(w in t for w in words):
            return key
    return None


def _founder(brain, field: str):
    r = next((x for x in brain.records("offers") if x.get("field") == field and x["tier"] == "approved"), None)
    return r


def floors(brain) -> dict:
    """Single-pair floor per line from the products price ladders (min price of the line's sample)."""
    out = {}
    for r in brain.records("products"):
        v = r.get("value")
        if (r.get("field") or "").startswith("price_ladder_") and isinstance(v, dict) and isinstance(v.get("min_usd"), (int, float)):
            out[(r["field"] or "").replace("price_ladder_", "")] = {"min_usd": float(v["min_usd"]), "max_usd": v.get("max_usd"), "n": v.get("sample_size"), "record": r["id"]}
    return out


def strip(brain) -> dict:
    fl = floors(brain)
    map_rec = _founder(brain, "map_usd_per_pair")
    map_usd = float(map_rec["value"]) if map_rec and isinstance(map_rec.get("value"), (int, float)) else None
    sellers_rec = _founder(brain, "marketplace_seller_names")
    ours = None
    if sellers_rec:
        v = sellers_rec.get("value")
        ours = [s.strip().lower() for s in (v if isinstance(v, list) else str(v).split(",")) if str(s).strip()]
    rows = []
    for r in brain.records("marketplaces"):
        v = r.get("value")
        if not (isinstance(v, dict) and v.get("asin")):
            continue
        title = v.get("title") or ""
        n = pack_count(title)
        price = v.get("price_usd") if isinstance(v.get("price_usd"), (int, float)) else None
        per = round(price / n, 2) if price else None
        line = line_of(title)
        floor = fl.get(line or "", {}).get("min_usd")
        seller = v.get("seller")
        flags = []
        if per is not None and floor is not None and per < floor * (1 - TOLERANCE):
            flags.append({"key": "under_site", "text": f"${per:,.2f} a pair is under the site floor of ${floor:,.2f}", "severity": "high"})
        if per is not None and map_usd is not None and per < map_usd:
            flags.append({"key": "below_map", "text": f"${per:,.2f} a pair is below your MAP of ${map_usd:,.2f}", "severity": "high"})
        if not seller:
            flags.append({"key": "seller_unknown", "text": "seller not in the pull", "severity": "low"})
        elif ours is not None and str(seller).strip().lower() not in ours:
            flags.append({"key": "unrecognised", "text": f"seller {seller} is not on your list", "severity": "high"})
        rows.append({"asin": v["asin"], "title": title, "line": line, "pack": n, "price_usd": price, "per_pair_usd": per, "site_floor_usd": floor,
                     "gap_pct": (round((per - floor) / floor * 100, 1) if per is not None and floor else None),
                     "stars": v.get("stars"), "reviews": v.get("reviews_count"), "seller": seller, "url": v.get("url") or f"https://www.amazon.com/dp/{v['asin']}",
                     "record": r["id"], "flags": flags, "verdict": _verdict(flags, per, floor)})
    order = {"stop": 0, "fix": 1, "wait": 2, "keep": 3}
    rows.sort(key=lambda x: (order.get(x["verdict"]["kind"], 9), x["gap_pct"] if x["gap_pct"] is not None else 999, x["asin"]))
    flagged = [x for x in rows if any(f["severity"] == "high" for f in x["flags"])]
    return {"listings": rows, "floors": fl, "map_usd_per_pair": map_usd, "map_record": map_rec["id"] if map_rec else None,
            "our_sellers": ours, "sellers_record": sellers_rec["id"] if sellers_rec else None,
            "counts": {"listings": len(rows), "flagged": len(flagged), "under_site": sum(1 for x in rows if any(f["key"] == "under_site" for f in x["flags"])),
                       "below_map": (sum(1 for x in rows if any(f["key"] == "below_map" for f in x["flags"])) if map_usd is not None else None),
                       "seller_unknown": sum(1 for x in rows if any(f["key"] == "seller_unknown" for f in x["flags"])),
                       "unrecognised": (sum(1 for x in rows if any(f["key"] == "unrecognised" for f in x["flags"])) if ours is not None else None)},
            "tolerance": TOLERANCE,
            "note": "Price per pair is the listing price over the pack count read from its title. The site floor is the lowest single price in the line's price ladder; a site multi-pack sells for less per pair than a single, so only a gap past 35 percent is flagged. MAP and your seller names are founder records; until set, those checks read unavailable."}


def _verdict(flags, per, floor) -> dict:
    keys = {f["key"] for f in flags}
    if "below_map" in keys or "unrecognised" in keys:
        return {"kind": "stop", "text": "Act", "reason": "; ".join(f["text"] for f in flags if f["severity"] == "high")}
    if "under_site" in keys:
        return {"kind": "fix", "text": "Under the site", "reason": next(f["text"] for f in flags if f["key"] == "under_site")}
    if per is None:
        return {"kind": "wait", "text": "No price", "reason": "the pull carried no price"}
    if "seller_unknown" in keys:
        return {"kind": "wait", "text": "Seller unknown", "reason": "parity holds on price; the seller needs a pull with the seller field"}
    return {"kind": "keep", "text": "In line", "reason": f"${per:,.2f} a pair against a ${floor:,.2f} floor" if floor else "no site floor for this line"}
