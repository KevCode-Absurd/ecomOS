"""Amazon reviews and listings through Apify: writes raw/amazon-apify/.

Two runs: junglee~amazon-reviews-scraper over every ASIN, 5-star and 1-star first
(config stars_first), capped at max_reviews_per_asin_per_star; then junglee~amazon-crawler
for title, bullets, stars, review count, price and seller per ASIN. The adapter runs per ASIN.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.connectors import apify, apify_adapters  # noqa: E402

LANE = "amazon"
STAR_FILTER = {1: "oneStar", 2: "twoStar", 3: "threeStar", 4: "fourStar", 5: "fiveStar"}
JUNGLEE = "junglee~amazon-reviews-scraper"


def _normalise(items):
    """junglee item keys to the adapter's keys (rating, title, text, date, verified, numberOfHelpful, reviewId, asin)."""
    out = []
    for it in items:
        if "ratingScore" in it or "reviewDescription" in it:
            when = str(it.get("reviewedIn") or it.get("date") or "")
            m = re.search(r"on (.+)$", when)
            helpful = re.search(r"(\d[\d,]*)", str(it.get("reviewReaction") or "0"))
            it = {"asin": it.get("productAsin") or it.get("asin"), "rating": it.get("ratingScore"),
                  "title": it.get("reviewTitle"), "text": it.get("reviewDescription"), "date": m.group(1) if m else when,
                  "verified": it.get("isVerified"), "numberOfHelpful": int(helpful.group(1).replace(",", "")) if helpful else 0,
                  "reviewId": (it.get("reviewUrl") or "").rstrip("/").split("/")[-1] or None, "reviewUrl": it.get("reviewUrl"),
                  "variant": it.get("variant")}
        out.append(it)
    return out


def run(brand: str, config: dict, *, client=None, root=None, captured_at=None, stars=None) -> dict:
    cfg = config["amazon_reviews"]
    client = client or apify.ApifyClient(mode="mock", brand=brand, budget=config.get("budget"))
    day = captured_at or client.today.isoformat()
    asins, domain = cfg["asins"], cfg.get("domain_code", "com")
    stars = stars or cfg.get("stars_first", [5, 1])
    per = cfg.get("max_reviews_per_asin_per_star", 100)
    if cfg["actor"] == JUNGLEE:
        review_input = {"productUrls": [{"url": f"https://www.amazon.{domain}/dp/{a}"} for a in asins],
                        "maxReviews": per, "filterByRatings": [STAR_FILTER[s] for s in stars], "sort": "recent",
                        "includeGdprSensitive": False, "scrapeProductDetails": False}
    else:
        review_input = {"input": [{"asin": a, "domainCode": domain, "sortBy": "recent", "maxPages": cfg.get("max_pages", 10),
                                   "filterByStar": STAR_FILTER[s].replace("Star", "_star").lower(), "reviewerType": "all_reviews"}
                                  for a in asins for s in stars]}
    reviews = _normalise(client.run(cfg["actor"], review_input, per * len(asins) * len(stars), lane=LANE))
    review_run = client.last_run["run_id"]
    listing_actor = cfg.get("listing_actor")
    listings, listing_run = {}, "none"
    if listing_actor:
        listing_input = {"categoryOrProductUrls": [{"url": f"https://www.amazon.{domain}/dp/{a}"} for a in asins],
                         "maxItemsPerStartUrl": 1, "scrapeProductDetails": True, "countryCode": "US" if domain == "com" else domain.upper()}
        for it in client.run(listing_actor, listing_input, len(asins), lane=f"{LANE}-listing"):
            if it.get("asin"):
                listings[it["asin"]] = it
        listing_run = client.last_run["run_id"]
    records = []
    for asin in asins:
        records += apify_adapters.amazon_reviews(reviews, brand, asin, listings.get(asin), run_id=review_run,
                                                 listing_run_id=listing_run, captured_at=day, actor=cfg["actor"],
                                                 listing_actor=listing_actor or apify_adapters.AMAZON_LISTING)
    if client.mode == "mock":
        for r in records:
            r["notes"] = "fixture data, not scraped"
    sources = [{"lane": LANE, "url": f"apify://{a}/{r}", "accessed": day, "accessible": True, "mode": client.mode,
                "actor": a, "run_id": r, "items": n,
                "note": "fixture items, invented for tests" if client.mode == "mock" else "Apify actor run"}
               for a, r, n in ((cfg["actor"], review_run, len(reviews)), (listing_actor, listing_run, len(listings))) if a]
    folder = apify.write_raw(Path(root) if root else ROOT / "app" / "brain", brand, LANE, records, sources)
    return {"lane": LANE, "folder": str(folder), "items": len(reviews) + len(listings), "records": len(records),
            "run_id": review_run}
