"""Reddit through Apify (trudax~reddit-scraper-lite): run(brand, config) writes raw/reddit-apify/.

One actor run over the brand's searches and subreddits, capped by config max_items.
Records come from app/connectors/apify_adapters.reddit; every one carries the Reddit note.

plan(brand, brain) builds queries and proposes subreddits from what the brain knows about
the brand (identity.category, products.lines), before any run and before any spend: the
founder confirms proposed_subreddits in config/apify.json (write_plan merges it in) and only
then does `run` above spend anything. Nothing here stores a Reddit username.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.connectors import apify, apify_adapters  # noqa: E402

LANE = "reddit"

# Category buckets: keyword hints to detect one from the brain, the subreddits it proposes
# (BuyItForLife is always proposed too), and a plain-language term for query building.
CATEGORY_KEYWORDS = {
    "socks_and_basics": ["sock", "socks", "underwear", "basics", "hosiery"],
    "apparel": ["apparel", "clothing", "fashion", "shirt", "loungewear", "activewear", "dress"],
    "beauty": ["beauty", "skincare", "makeup", "cosmetic"],
    "supplements": ["supplement", "vitamin", "protein powder", "nutrition"],
    "home": ["home", "furniture", "decor", "kitchen", "bedding"],
    "pets": ["pet", "dog", "cat", "treat"],
    "outdoor": ["outdoor", "camp", "hike", "hiking", "trail", "backpack"],
}
CATEGORY_SUBREDDITS = {
    "socks_and_basics": ["socks", "malefashionadvice", "femalefashionadvice"],
    "apparel": ["malefashionadvice", "femalefashionadvice", "frugalmalefashion"],
    "beauty": ["SkincareAddiction", "MakeupAddiction", "30PlusSkinCare"],
    "supplements": ["Supplements", "nutrition", "Fitness"],
    "home": ["HomeImprovement", "InteriorDesign", "Frugal"],
    "pets": ["dogs", "cats", "DogAdvice"],
    "outdoor": ["hiking", "CampingandHiking", "Ultralight"],
}
CATEGORY_TERM = {
    "socks_and_basics": "socks",
    "apparel": "clothing",
    "beauty": "skincare",
    "supplements": "supplements",
    "home": "home goods",
    "pets": "pet supplies",
    "outdoor": "outdoor gear",
}
DEFAULT_BUCKET = "apparel"


def _category_bucket(bits: list) -> str:
    blob = " ".join(str(b).lower() for b in bits if b)
    best, best_n = DEFAULT_BUCKET, 0
    for bucket, kws in CATEGORY_KEYWORDS.items():
        n = sum(1 for kw in kws if kw in blob)
        if n > best_n:
            best, best_n = bucket, n
    return best


def plan(brand: str, brain: dict, *, brand_name: str | None = None) -> dict:
    """Reddit queries and proposed subreddits, built from the brand's brain, not run.

    brain is {section: {field: value}}, e.g. from brain_from_files. Reads identity.category
    and products.lines only. Returns proposed_subreddits (BuyItForLife plus the category's
    own subs) and searches (at least 5), for the founder to confirm in config/apify.json
    before a paid run. Stores nothing from Reddit itself: this never touches the network.
    """
    identity = brain.get("identity") or {}
    products = brain.get("products") or {}
    name = brand_name or identity.get("name") or re.sub(r"[-_]+", " ", brand).strip().title()
    category_text = str(identity.get("category") or "")
    lines = products.get("lines") or []
    if isinstance(lines, str):
        lines = [lines]
    bucket = _category_bucket([category_text] + list(lines))
    terms = []
    for line in lines:
        t = re.sub(r"\s+", " ", str(line)).strip().lower()
        if t and t not in terms:
            terms.append(t)
    if not terms:
        terms = [CATEGORY_TERM[bucket]]
    primary = terms[0]
    subs, seen_s = [], set()
    for s in ["BuyItForLife"] + CATEGORY_SUBREDDITS.get(bucket, []):
        if s not in seen_s:
            seen_s.add(s)
            subs.append(s)
    candidates = [f"{name} review", f"{name} {primary}", f"best {primary}", f"{primary} worth it",
                  f"buy it for life {primary}"] + [f"best {t}" for t in terms[1:3]]
    searches, seen_q = [], set()
    for q in candidates:
        if q not in seen_q:
            seen_q.add(q)
            searches.append(q)
    return {"brand_name": name, "category_bucket": bucket, "category_term": primary,
            "category_terms": terms, "proposed_subreddits": subs, "searches": searches}


def _section_values(root: Path, brand: str, section: str) -> dict:
    path = Path(root) / brand / f"{section}.json"
    if not path.exists():
        return {}
    try:
        records = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    out = {}
    for r in records if isinstance(records, list) else []:
        if isinstance(r, dict) and r.get("field") and r.get("status", "active") == "active" and "value" in r:
            out[r["field"]] = r["value"]
    return out


def brain_from_files(brand: str, root=None) -> dict:
    """{"identity": {...}, "products": {...}} from a merged brain, if one exists yet. Missing files read as empty, never an error."""
    root = Path(root) if root else ROOT / "app" / "brain"
    return {"identity": _section_values(root, brand, "identity"), "products": _section_values(root, brand, "products")}


def write_plan(brand: str, *, brain_root=None, config_path=None) -> dict:
    """Compute the plan and merge proposed_subreddits/proposed_searches into config/apify.json's
    reddit lane. Never writes or touches `subreddits`: that list is the founder's confirmation."""
    cfg_path = Path(config_path) if config_path else ROOT / "app" / "brain" / brand / "config" / "apify.json"
    config = json.loads(cfg_path.read_text(encoding="utf-8")) if cfg_path.exists() else {}
    result = plan(brand, brain_from_files(brand, brain_root))
    reddit_cfg = config.setdefault(LANE, {})
    reddit_cfg["proposed_subreddits"] = result["proposed_subreddits"]
    reddit_cfg["proposed_searches"] = result["searches"]
    reddit_cfg["category_term"] = result["category_term"]
    reddit_cfg.setdefault("brand_name", result["brand_name"])
    cfg_path.parent.mkdir(parents=True, exist_ok=True)
    cfg_path.write_text(json.dumps(config, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return result


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


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="Propose Reddit subreddits and searches for a brand, from its brain. Never spends.")
    ap.add_argument("--brand", required=True)
    ap.add_argument("--write", action="store_true", help="merge the plan into the brand's config/apify.json")
    args = ap.parse_args(argv)
    result = write_plan(args.brand) if args.write else plan(args.brand, brain_from_files(args.brand))
    print(json.dumps(result, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
