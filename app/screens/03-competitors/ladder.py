"""Price ladder and pack ladder against the tracked pages.

Ours: net price per pair by style and pack from the simulated products_monthly table (audit.brand_packs),
grouped into a ladder per style (single, then each pack). Theirs: the public price band per pair from
each brain competitors record (low, median, high). Cross-source: our Amazon listing prices from the
brain's marketplaces records, per pair where the title states the pack size (public list prices, next
to our simulated site net prices).

Rules (constants below):
  shallow pack ladder (COMP-R09): the median per-pair saving from single to the biggest pack across our
      styles is under LADDER_MIN (10 percent) while a tracked page advertises a bundle saving of
      BUNDLE_MIN (15 percent) or more. Answer: a pack ladder offer (LIFE-C39).
  above with no proof (COMP-R10): a style's single pair sits above the median of the direct peers'
      medians and the brain holds no proof point for that style. Answer: a price proof section on the
      product page (CREA-C31).
"""
from __future__ import annotations

import re
import statistics

LADDER_MIN, BUNDLE_MIN = 0.10, 0.15
STYLE_WORDS = {"ANK": "ankle", "CRW": "crew", "NSH": "no show", "MER": "merino", "CMP": "compression",
               "ATH": "athletic", "GOLF": "golf", "KID": "kids", "GIFT": "gift box", "QTR": "quarter", "CLF": "calf",
               "RUN": "running"}
PROOF_STYLE = {"merino": ["merino", "wool"], "compression": ["compression", "support"], "ankle": ["arch", "blister", "seamless"],
               "crew": ["arch", "seamless"], "no show": ["blister", "grip", "stay"], "athletic": ["arch", "blister", "athletic"],
               "golf": ["arch", "blister"], "kids": ["seamless", "comfort"], "gift box": ["gift"]}


def _same(a: str, b: str) -> bool:
    x, y = (re.sub(r"[^a-z0-9]+", "_", str(v or "").lower()).strip("_") for v in (a, b))
    return bool(x and y) and (x == y or x.startswith(y) or y.startswith(x))


def style_of(sku: str) -> tuple[str, int] | None:
    parts = str(sku).split("-")
    try:
        pairs = int(parts[-1])
    except ValueError:
        return None
    code = parts[-2] if len(parts) >= 2 else ""
    gender = {"M": "men's ", "W": "women's "}.get(parts[-3], "") if len(parts) >= 4 else ""
    return gender + STYLE_WORDS.get(code, code.lower()), pairs


def pairs_in_title(title: str) -> int | None:
    t = str(title or "").lower()
    m = re.search(r"(\d+)\s*[- ]?\s*(pack|pairs?|pcs|pk)\b", t) or re.search(r"\((\d+)\s*(pack|pair)", t)
    return int(m.group(1)) if m else None


def build(m: dict, brain) -> dict:
    packs = m["packs"]
    styles: dict[str, list[dict]] = {}
    for p in packs.get("packs") or []:
        s = style_of(p["sku"])
        if s:
            styles.setdefault(s[0], []).append({"pairs": s[1], "per_pair": p["per_pair"], "per_pack": p["per_pack"],
                                                 "units": p["units"], "sku": p["sku"]})
    bands = []
    for p in m["pages"]:
        c = next((c for c in m["competitors"] if _same(c["name"], p["name"])), None)
        if not c or c["price"]["median"] is None:
            continue
        bands.append({"name": p["name"], "frame": p["frame"], "low": c["price"]["low"], "high": c["price"]["high"],
                      "median": c["price"]["median"], "rough": c["price"]["rough"], "text": c["price"]["text"], "ref": c.get("price_ref")})
    direct_meds = [b["median"] for b in bands if b["frame"] == "direct"]
    direct_median = round(statistics.median(direct_meds), 2) if direct_meds else None
    points = [str(x) for x in ((brain.get(f"{brain.brand}.positioning.proof_points") or {}).get("value") or [])]
    ladders = []
    for name, rows in sorted(styles.items()):
        rows.sort(key=lambda r: r["pairs"])
        single = next((r for r in rows if r["pairs"] == 1), None)
        big = rows[-1]
        saving = round(1 - big["per_pair"] / single["per_pair"], 3) if single and big["pairs"] > 1 else None
        base = name.split("'s ")[-1]
        proof = next((pt for pt in points if any(w in pt.lower() for w in PROOF_STYLE.get(base, [base]))), None)
        top = single or rows[0]
        pos = None if direct_median is None else ("above" if top["per_pair"] > direct_median else "below")
        ladders.append({"style": name, "steps": rows, "single": single["per_pair"] if single else None,
                        "biggest_pairs": big["pairs"], "biggest": big["per_pair"], "saving": saving,
                        "vs_direct_median": pos, "proof": proof})
    savings = [l["saving"] for l in ladders if l["saving"] is not None]
    median_saving = round(statistics.median(savings), 3) if savings else None
    bundle = bundle_offer(m)
    amazon = []
    for r in brain.records("marketplaces"):
        v = r.get("value") if isinstance(r.get("value"), dict) else {}
        n = pairs_in_title(v.get("title"))
        if v.get("channel") == "amazon" and isinstance(v.get("price_usd"), (int, float)) and n:
            amazon.append({"title": v.get("title"), "pairs": n, "price": round(v["price_usd"], 2),
                           "per_pair": round(v["price_usd"] / n, 2), "asin": v.get("asin")})
    amazon.sort(key=lambda a: a["per_pair"])
    return {"available": packs["available"], "reason": packs.get("reason"), "month": packs.get("month"),
            "ladders": ladders, "bands": bands, "direct_median": direct_median, "median_saving": median_saving,
            "bundle": bundle, "amazon": amazon, "ladder_min": LADDER_MIN, "bundle_min": BUNDLE_MIN,
            "shallow": median_saving is not None and median_saving < LADDER_MIN and bundle is not None
            and bundle["pct"] >= BUNDLE_MIN * 100,
            "above_no_proof": [l for l in ladders if l["vs_direct_median"] == "above" and not l["proof"]]}


def bundle_offer(m: dict) -> dict | None:
    """The deepest bundle saving a tracked page advertises: a bundle hook label plus a percent in its offers."""
    best = None
    for p in m["pages"]:
        if p["role"] == "self":
            continue
        has_bundle = any("bundle" in h.lower() for h in p.get("hook_labels") or []) or any(
            "bundle" in str(o).lower() for o in p.get("offers_seen") or [])
        if not has_bundle:
            continue
        for o in p.get("offers_seen") or []:
            mm = re.search(r"(\d{1,2})\s?%", str(o))
            if mm and (best is None or int(mm.group(1)) > best["pct"]):
                best = {"page": p["name"], "pct": int(mm.group(1)), "offer": o}
    return best
