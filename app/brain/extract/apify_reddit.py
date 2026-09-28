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
    subs = [f"https://www.reddit.com/r/{s}/" for s in cfg.get("subreddits", [])]
    actor_input = {"searches": cfg.get("searches", []), "startUrls": [{"url": u} for u in subs],
                   "maxItems": cfg["max_items"], "maxComments": cfg.get("max_comments_per_post", 20),
                   "sort": cfg.get("sort", "top"), "time": cfg.get("time", "year"), "skipUserPosts": True}
    items = client.run(actor, actor_input, cfg["max_items"], lane=LANE)
    run_id = client.last_run["run_id"]
    note = apify_adapters.REDDIT_NOTE + ("; fixture data, not scraped" if client.mode == "mock" else "")
    records = apify_adapters.reddit(items, brand, run_id=run_id, captured_at=day, actor=actor, notes=note)
    sources = [{"lane": LANE, "url": f"apify://{actor}/{run_id}", "accessed": day, "accessible": True,
                "mode": client.mode, "actor": actor, "run_id": run_id, "items": len(items), "records": len(records),
                "note": "fixture items, invented for tests" if client.mode == "mock" else "Apify actor run"}]
    folder = apify.write_raw(Path(root) if root else ROOT / "app" / "brain", brand, LANE, records, sources)
    return {"lane": LANE, "folder": str(folder), "items": len(items), "records": len(records), "run_id": run_id}
