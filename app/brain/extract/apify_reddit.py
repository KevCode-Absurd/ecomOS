"""Reddit through Apify (trudax~reddit-scraper-lite): run(brand, config) writes raw/reddit-apify/.

One actor run over the brand's searches and subreddits, capped by config max_items.
Records come from app/connectors/apify_adapters.reddit; every one carries the Reddit note.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.connectors import apify, apify_adapters  # noqa: E402

LANE = "reddit"


def run(brand: str, config: dict, *, client=None, root=None, captured_at=None) -> dict:
    cfg = config[LANE]
    client = client or apify.ApifyClient(mode="mock", brand=brand, budget=config.get("budget"))
    day = captured_at or client.today.isoformat()
    actor = cfg["actor"]
    import urllib.parse as _u
    brand_name = cfg.get("brand_name") or brand
    sort, time_ = cfg.get("sort", "top"), cfg.get("time", "year")
    urls = [f"https://www.reddit.com/search/?q={_u.quote(q)}&sort={sort}&t={time_}" for q in cfg.get("searches", [])]
    for sub in cfg.get("subreddits", []):
        for q in (brand_name, cfg.get("category_term", "socks")):
            urls.append(f"https://www.reddit.com/r/{sub}/search/?q={_u.quote(q)}&restrict_sr=1&sort={sort}&t={time_}")
    # Search result pages, not subreddit home pages: the home page yields one community record and nothing else.
    actor_input = {"startUrls": [{"url": u} for u in urls], "skipCommunity": True, "skipUserPosts": True,
                   "skipComments": False, "includeMediaLinks": True, "maxItems": cfg["max_items"],
                   "maxPostCount": cfg.get("max_posts_per_search", 15),
                   "maxComments": cfg.get("max_comments_per_post", 10)}
    items = client.run(actor, actor_input, cfg["max_items"], lane=LANE)
    run_id = client.last_run["run_id"]
    note = apify_adapters.REDDIT_NOTE + ("; fixture data, not scraped" if client.mode == "mock" else "")
    records = apify_adapters.reddit(items, brand, run_id=run_id, captured_at=day, actor=actor, notes=note)
    sources = [{"lane": LANE, "url": f"apify://{actor}/{run_id}", "accessed": day, "accessible": True,
                "mode": client.mode, "actor": actor, "run_id": run_id, "items": len(items), "records": len(records),
                "note": "fixture items, invented for tests" if client.mode == "mock" else "Apify actor run"}]
    folder = apify.write_raw(Path(root) if root else ROOT / "app" / "brain", brand, LANE, records, sources)
    return {"lane": LANE, "folder": str(folder), "items": len(items), "records": len(records), "run_id": run_id}
