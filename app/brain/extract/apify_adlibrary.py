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
PAGE = "https://www.facebook.com/ads/library/?active_status={status}&ad_type=all&country={country}&view_all_page_id={page_id}&search_type=page"


def keep_configured_pages(items: list[dict], pages: list[dict]) -> list[dict]:
    """Drop advertisers a name search dragged in: keep items whose page id or exact page name is configured."""
    ids = {str(p["page_id"]) for p in pages if p.get("page_id")}
    names = {p["name"].strip().lower() for p in pages}
    return [it for it in items if str(it.get("page_id")) in ids or (it.get("page_name") or "").strip().lower() in names]


def run(brand: str, config: dict, *, client=None, root=None, captured_at=None) -> dict:
    cfg = config["meta_ad_library"]
    client = client or apify.ApifyClient(mode="mock", brand=brand, budget=config.get("budget"))
    day = captured_at or client.today.isoformat()
    actor = cfg["actor"]
    status, country = cfg.get("active_status", "active"), cfg.get("country", "US")
    pages = cfg.get("pages", [])
    # A page with a known id is read directly; a name search is a keyword search and pulls every advertiser
    # whose name contains the word (28 Sep: "Stance" returned car tuners), so items are filtered to the
    # configured pages afterwards and the name route is only a fallback until the id is known.
    urls = [PAGE.format(status=status, country=country, page_id=p["page_id"]) if p.get("page_id")
            else LIB.format(status=status, country=country, q=urllib.parse.quote(p["name"]), kind="page") for p in pages]
    urls += [LIB.format(status=status, country=country, q=urllib.parse.quote(t), kind="keyword_unordered")
             for t in cfg.get("search_terms", [])]
    per = cfg.get("limit_per_source", 100)
    actor_input = {"urls": [{"url": u} for u in urls], "scrapeAdDetails": bool(cfg.get("scrape_ad_details", False)),
                   "limitPerSource": per, "scrapePageAds.activeStatus": status, "scrapePageAds.countryCode": country}
    max_items = per * max(len(urls), 1)
    items = client.run(actor, actor_input, max_items, lane=LANE)
    run_id = client.last_run["run_id"]
    pulled = len(items)
    if not cfg.get("search_terms"):
        items = keep_configured_pages(items, pages)
    roles = {p["name"]: p.get("role", "competitor") for p in pages}
    for p in pages:  # the page's own display name can differ from the configured one ("Darn Tough Vermont Socks")
        for it in items:
            if p.get("page_id") and str(it.get("page_id")) == str(p["page_id"]) and it.get("page_name"):
                roles.setdefault(it["page_name"], p.get("role", "competitor"))
    # Items from keyword searches whose page is not in the config are competitors by default.
    records = apify_adapters.meta_ad_library(items, brand, roles, run_id=run_id, captured_at=day, actor=actor)
    if client.mode == "mock":
        for r in records:
            r["notes"] = "fixture data, not scraped"
    sources = [{"lane": LANE, "url": f"apify://{actor}/{run_id}", "accessed": day, "accessible": True,
                "mode": client.mode, "actor": actor, "run_id": run_id, "items": pulled, "kept": len(items), "records": len(records),
                "note": "fixture items, invented for tests" if client.mode == "mock" else "Apify actor run"}]
    folder = apify.write_raw(Path(root) if root else ROOT / "app" / "brain", brand, LANE, records, sources)
    return {"lane": LANE, "folder": str(folder), "items": len(items), "records": len(records), "run_id": run_id}
