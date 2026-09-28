"""Where we meet them off Meta: our marketplace listings against our own site, and what we know of theirs.

Ours: the brain's `marketplaces` records (Amazon listings: title, price, stars, review count, seller).
Per style (ankle, no show, crew, from the title) the median Amazon price per pair where the title states
the pack size, against our site's net price per pair for the same style's biggest pack (simulated).
Theirs: competitor marketplace listings are not in the brain and read unavailable.

Rule COMP-R18: a style with MIN_LISTINGS (2) or more Amazon listings whose median price per pair sits
UNDERCUT (15 percent) or more below our site's net price per pair. A shopper who compares finds us cheaper
on Amazon, and a reseller may be behind it (seller is null in the capture). Answer: a listing and price
check (PROD-C46, agent does it). Site prices are simulated, so confidence is low.
"""
from __future__ import annotations

import statistics

MIN_LISTINGS, UNDERCUT = 2, 0.15
STYLE_KEYS = [("no show", ["no show", "no-show"]), ("ankle", ["ankle", "low cut"]), ("crew", ["crew"]), ("merino", ["merino"]),
              ("compression", ["compression"])]


def style_of_title(title: str) -> str | None:
    t = str(title or "").lower()
    for style, keys in STYLE_KEYS:
        if any(k in t for k in keys):
            return style
    return None


def build(m: dict, brain, pairs_in_title) -> dict:
    listings = []
    for r in brain.records("marketplaces"):
        v = r.get("value") if isinstance(r.get("value"), dict) else {}
        if not v.get("channel"):
            continue
        n = pairs_in_title(v.get("title"))
        price = v.get("price_usd") if isinstance(v.get("price_usd"), (int, float)) else None
        listings.append({"channel": v["channel"], "asin": v.get("asin"), "title": v.get("title"), "style": style_of_title(v.get("title")),
                         "pairs": n, "price": round(price, 2) if price is not None else None,
                         "per_pair": round(price / n, 2) if price is not None and n else None,
                         "stars": v.get("stars"), "reviews": v.get("reviews_count"), "seller": v.get("seller")})
    site = {}
    for lad in (m.get("ladder") or {}).get("ladders") or []:
        base = lad["style"].split("'s ")[-1]
        site.setdefault(base, []).append(lad["biggest"])
    styles = []
    for style, _ in STYLE_KEYS:
        rows = [x for x in listings if x["style"] == style and x["per_pair"] is not None]
        if not rows:
            continue
        amz = round(statistics.median(x["per_pair"] for x in rows), 2)
        ours = round(min(site[style]), 2) if style in site else None
        gap = round(1 - amz / ours, 3) if ours else None
        styles.append({"style": style, "listings": len(rows), "amazon_per_pair": amz, "site_per_pair": ours, "gap": gap,
                       "undercut": gap is not None and gap >= UNDERCUT and len(rows) >= MIN_LISTINGS,
                       "unknown_sellers": sum(1 for x in rows if not x["seller"])})
    stars = [x["stars"] for x in listings if isinstance(x["stars"], (int, float))]
    reviews = [x["reviews"] for x in listings if isinstance(x["reviews"], int)]
    return {"listings": len(listings) or None, "priced": sum(1 for x in listings if x["per_pair"] is not None) if listings else None,
            "median_stars": round(statistics.median(stars), 2) if stars else None, "reviews": sum(reviews) if reviews else None,
            "styles": styles, "top": sorted(listings, key=lambda x: -(x["reviews"] or 0))[:5],
            "theirs": None, "theirs_reason": "competitor marketplace listings are not captured; an Amazon search by brand would fill it",
            "rule": f"Undercut: a style with {MIN_LISTINGS} or more Amazon listings whose median price per pair is "
                    f"{round(UNDERCUT * 100)} percent or more below our site's net price per pair (simulated)."}


def draft(s: dict, brand: str) -> str:
    return "\n".join([f"Listing and price check: {s['style']} on Amazon.",
                      f"Amazon median {s['amazon_per_pair']:.2f} dollars a pair across {s['listings']} listings; our site nets "
                      f"{s['site_per_pair']:.2f} a pair (simulated). Gap {round(s['gap'] * 100)} percent.",
                      f"Sellers unknown on {s['unknown_sellers']} listings: check which are {brand} and which are resellers.",
                      "If a reseller: log it for the MAP and brand registry team. If ours: align the pack price or the pack size.",
                      "Report back with each listing's seller, price per pair and action."])
