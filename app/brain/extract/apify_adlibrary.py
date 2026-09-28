"""Meta Ad Library through Apify (curious_coder~facebook-ads-library-scraper): writes raw/adlibrary-apify/.

One run over the brand's pages (role self or competitor) and search terms, capped at
limit_per_source per source. Signals only: formats, hooks, run lengths, promos, a short quote.
"""
from __future__ import annotations

import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.connectors import apify, apify_adapters  # noqa: E402

LANE = "adlibrary"
LIB = "https://www.facebook.com/ads/library/?active_status={status}&ad_type=all&country={country}&q={q}&search_type={kind}"


def run(brand: str, config: dict, *, client=None, root=None, captured_at=None) -> dict:
    cfg = config["meta_ad_library"]
    client = client or apify.ApifyClient(mode="mock", brand=brand, budget=config.get("budget"))
    day = captured_at or client.today.isoformat()
    actor = cfg["actor"]
    status, country = cfg.get("active_status", "active"), cfg.get("country", "US")
    pages = cfg.get("pages", [])
    urls = [LIB.format(status=status, country=country, q=urllib.parse.quote(p["name"]), kind="page") for p in pages]
    urls += [LIB.format(status=status, country=country, q=urllib.parse.quote(t), kind="keyword_unordered")
             for t in cfg.get("search_terms", [])]
    per = cfg.get("limit_per_source", 100)
    actor_input = {"urls": [{"url": u} for u in urls], "scrapeAdDetails": bool(cfg.get("scrape_ad_details", False)),
                   "limitPerSource": per, "scrapePageAds.activeStatus": status, "scrapePageAds.countryCode": country}
    max_items = per * max(len(urls), 1)
    items = client.run(actor, actor_input, max_items, lane=LANE)
    run_id = client.last_run["run_id"]
    roles = {p["name"]: p.get("role", "competitor") for p in pages}
    # Items from keyword searches whose page is not in the config are competitors by default.
    records = apify_adapters.meta_ad_library(items, brand, roles, run_id=run_id, captured_at=day, actor=actor)
    if client.mode == "mock":
        for r in records:
            r["notes"] = "fixture data, not scraped"
    sources = [{"lane": LANE, "url": f"apify://{actor}/{run_id}", "accessed": day, "accessible": True,
                "mode": client.mode, "actor": actor, "run_id": run_id, "items": len(items), "records": len(records),
                "note": "fixture items, invented for tests" if client.mode == "mock" else "Apify actor run"}]
    folder = apify.write_raw(Path(root) if root else ROOT / "app" / "brain", brand, LANE, records, sources)
    return {"lane": LANE, "folder": str(folder), "items": len(items), "records": len(records), "run_id": run_id}
