"""Social keyword pull for the research desk: public Instagram posts by hashtag through the Apify connector.

    python3 app/screens/01-market-research/social_pull.py --brand bombas --mode mock
    python3 app/screens/01-market-research/social_pull.py --brand bombas --mode live --per-tag 25

Reads the brand's hashtags from app/brain/<brand>/config/apify.json (brand name and category term from the
reddit lane) plus the lanes this desk follows, runs one hashtag actor under the brand's caps (per run and per
week, through the connector's ledger), and writes fixtures/social_pull.json: counts by theme, top co-hashtags
and short public quotes (at most 140 characters). Usernames, user ids and profile links are never read; the
item fields copied are a whitelist. Mock mode reads fixtures/apify~instagram-hashtag-scraper.json (invented
shape for tests) and costs nothing. The page says which mode filled the block.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from app.connectors import apify  # noqa: E402
from app.connectors.apify_adapters import THEMES, NEGATIVE, POSITIVE, has, themes_of  # noqa: E402

ACTOR = "apify~instagram-hashtag-scraper"
PRICE_PER_1000 = 2.30   # Apify Store, pay per result, seen 28 Sep 2026; contract ask: add to app/connectors/apify.py PRICES_PER_1000
QUOTE_MAX = 140
FIELDS = ("caption", "hashtags", "likesCount", "commentsCount", "timestamp", "url", "type", "hashtag")   # whitelist, no owner fields
LANE_TAGS = {"compression": "compressionsocks", "merino": "merinosocks", "performance": "runningsocks", "gifting": "sockgift",
             "guarantee": "buyitforlife", "style": "sockstyle"}


def hashtags_for(config: dict, lanes: list[str] | None = None) -> list[str]:
    reddit = config.get("reddit") or {}
    tags = []
    brand = (reddit.get("brand_name") or "").lower().replace(" ", "")
    if brand:
        tags.append(brand)
    cat = (reddit.get("category_term") or "").lower().replace(" ", "")
    if cat:
        tags.append(cat)
    for lane in lanes or []:
        t = LANE_TAGS.get(lane)
        if t and t not in tags:
            tags.append(t)
    return tags[:6]


def sentiment(text: str) -> str:
    neg, pos = has(text, NEGATIVE), has(text, POSITIVE)
    return "complaint" if neg and not pos else "praise" if pos and not neg else "mixed"


def clean(text: str, limit: int = QUOTE_MAX) -> str:
    t = re.sub(r"@\w+", "@user", str(text or ""))           # mask any handle in a caption
    t = t.replace("—", ",").replace("\n", " ")
    t = re.sub(r"\s+", " ", t).strip()
    return t[:limit]


def summarise(items: list[dict], tags: list[str], meta: dict) -> dict:
    themes: dict[str, dict] = {t: {"posts": 0, "likes": 0, "comments": 0, "praise": 0, "complaint": 0, "mixed": 0} for t in list(THEMES) + ["general"]}
    cotags: Counter = Counter()
    samples = []
    by_tag: Counter = Counter()
    for it in items:
        row = {k: it.get(k) for k in FIELDS}
        text = clean(row.get("caption") or "", 1000)
        ths = themes_of(text.lower()) or ["general"]
        sent = sentiment(text.lower())
        likes = int(row.get("likesCount") or 0)
        comments = int(row.get("commentsCount") or 0)
        by_tag[str(row.get("hashtag") or "").lower()] += 1
        for th in ths:
            g = themes[th]
            g["posts"] += 1
            g["likes"] += likes
            g["comments"] += comments
            g[sent] += 1
        for h in row.get("hashtags") or []:
            h = str(h).lower().lstrip("#")
            if h and h not in tags:
                cotags[h] += 1
        if text and len(samples) < 40:
            samples.append({"hashtag": row.get("hashtag"), "date": str(row.get("timestamp") or "")[:10], "likes": likes, "comments": comments,
                            "quote": clean(text), "themes": ths, "sentiment": sent, "url": row.get("url")})
    samples.sort(key=lambda s: -(s["likes"] + s["comments"]))
    return dict(meta, hashtags=tags, items=len(items), posts_by_tag=dict(by_tag),
                themes={k: v for k, v in themes.items() if v["posts"]}, co_hashtags=cotags.most_common(15),
                samples=samples[:20], note="Public posts by hashtag through Apify. Counts and short quotes only; no usernames are read or stored. Signals, not proof.")


def run(brand: str, mode: str, per_tag: int, lanes: list[str] | None = None, today: dt.date | None = None) -> dict:
    config = json.loads((ROOT / "app" / "brain" / brand / "config" / "apify.json").read_text(encoding="utf-8"))
    tags = hashtags_for(config, lanes)
    if not tags:
        raise apify.ApifyError("no hashtags: set reddit.brand_name and reddit.category_term in the brand's apify.json")
    apify.PRICES_PER_1000.setdefault(ACTOR, PRICE_PER_1000)
    client = apify.ApifyClient(mode=mode, brand=brand, budget=config.get("budget"), fixtures_dir=HERE / "fixtures", today=today)
    max_items = per_tag * len(tags)
    est = client.check_caps(ACTOR, max_items)
    items = client.run(ACTOR, {"hashtags": tags, "resultsLimit": per_tag, "resultsType": "posts"}, max_items, lane="social_keywords")
    last = client.last_run or {}
    out = summarise(items, tags, {"brand": brand, "captured_at": (today or dt.date.today()).isoformat(), "mode": mode, "actor": ACTOR,
                                  "run_id": last.get("run_id"), "usd": last.get("usd"), "estimate_usd": est, "per_tag": per_tag})
    (HERE / "fixtures" / "social_pull.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Instagram hashtag pull for the research desk, under the brand's Apify caps.")
    ap.add_argument("--brand", default="bombas")
    ap.add_argument("--mode", default="mock", choices=("mock", "live"))
    ap.add_argument("--per-tag", type=int, default=25)
    ap.add_argument("--lanes", nargs="*", default=["compression", "merino", "gifting"])
    ap.add_argument("--estimate-only", action="store_true")
    args = ap.parse_args(argv)
    config = json.loads((ROOT / "app" / "brain" / args.brand / "config" / "apify.json").read_text(encoding="utf-8"))
    tags = hashtags_for(config, args.lanes)
    apify.PRICES_PER_1000.setdefault(ACTOR, PRICE_PER_1000)
    est = apify.estimate_usd(ACTOR, args.per_tag * len(tags))
    print(f"hashtags {tags}, {args.per_tag} per tag, estimate ${est:.2f} against per run ${config['budget']['max_usd_per_run']} and week ${config['budget']['max_usd_per_week']}")
    if args.estimate_only:
        return 0
    try:
        out = run(args.brand, args.mode, args.per_tag, args.lanes)
    except apify.ApifyError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({k: out[k] for k in ("mode", "run_id", "usd", "items", "posts_by_tag", "themes")}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
