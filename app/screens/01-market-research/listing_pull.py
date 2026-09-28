"""Amazon listing details for the research desk: seller of record, price, stars and ratings per ASIN through the Apify connector.

    python3 app/screens/01-market-research/listing_pull.py --brand bombas --mode mock
    python3 app/screens/01-market-research/listing_pull.py --brand bombas --mode live

Reads the brand's ASINs from app/brain/<brand>/config/apify.json (amazon_reviews.asins) and the listing actor from
amazon_reviews.listing_actor (junglee~amazon-crawler by default: the same actor the brain used for the search pull, priced
per result, so the run stays inside the per-run cap for a few dozen ASINs). Writes fixtures/amazon_listings.json: one row per
ASIN with the seller of record, whether it is a third party, the price and the ratings, plus the run's mode, cost and date.
Mock mode reads the connector's invented fixture and costs nothing; the marketplace read never takes a seller from a mock
row, it only says a mock is on file. The page says which mode filled the block.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from app.connectors import apify  # noqa: E402

DEFAULT_ACTOR = "junglee~amazon-crawler"
FIELDS = ("asin", "title", "url", "price", "stars", "reviewsCount", "brand", "seller")   # whitelist: no reviewer fields


def config_for(brand: str) -> dict:
    return json.loads((ROOT / "app" / "brain" / brand / "config" / "apify.json").read_text(encoding="utf-8"))


def actor_for(config: dict) -> str:
    return ((config.get("amazon_reviews") or {}).get("listing_actor")) or DEFAULT_ACTOR


def rows_from(items: list[dict], brand_name: str) -> list[dict]:
    out = []
    for it in items:
        row = {k: it.get(k) for k in FIELDS}
        seller = row.get("seller")
        seller = (seller.get("name") if isinstance(seller, dict) else seller) or None
        price = row.get("price")
        price = (price.get("value") if isinstance(price, dict) else price)
        third = None if not seller else seller.strip().lower() != brand_name.strip().lower()
        out.append({"asin": row.get("asin"), "title": row.get("title"), "url": row.get("url"), "price_usd": float(price) if price is not None else None,
                    "stars": row.get("stars"), "ratings": row.get("reviewsCount"), "brand_on_listing": row.get("brand"), "seller": seller, "third_party_seller": third})
    return out


def run(brand: str, mode: str, today: dt.date | None = None) -> dict:
    config = config_for(brand)
    asins = list((config.get("amazon_reviews") or {}).get("asins") or [])
    if not asins:
        raise apify.ApifyError("no ASINs: set amazon_reviews.asins in the brand's apify.json")
    actor = actor_for(config)
    brand_name = ((config.get("reddit") or {}).get("brand_name")) or brand
    client = apify.ApifyClient(mode=mode, brand=brand, budget=config.get("budget"), fixtures_dir=ROOT / "app" / "connectors" / "fixtures" / "apify", today=today)
    est = client.check_caps(actor, len(asins))
    items = client.run(actor, {"asins": asins, "domain_code": (config.get("amazon_reviews") or {}).get("domain_code") or "com"}, len(asins), lane="listing_seller")
    last = client.last_run or {}
    rows = rows_from(items, brand_name)
    out = {"brand": brand, "captured_at": (today or dt.date.today()).isoformat(), "mode": mode, "actor": actor, "run_id": last.get("run_id"), "usd": last.get("usd"),
           "estimate_usd": est, "asins": asins, "rows": rows,
           "note": "Seller of record per listing through Apify. Public listing data only. A mock run is an invented shape: its sellers are never read as fact."}
    (HERE / "fixtures" / "amazon_listings.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Amazon listing seller pull for the research desk, under the brand's Apify caps.")
    ap.add_argument("--brand", default="bombas")
    ap.add_argument("--mode", default="mock", choices=("mock", "live"))
    ap.add_argument("--estimate-only", action="store_true")
    args = ap.parse_args(argv)
    config = config_for(args.brand)
    asins = list((config.get("amazon_reviews") or {}).get("asins") or [])
    actor = actor_for(config)
    est = apify.estimate_usd(actor, len(asins))
    print(f"{actor} over {len(asins)} ASINs, estimate ${est:.2f} against per run ${config['budget']['max_usd_per_run']} and week ${config['budget']['max_usd_per_week']}")
    if args.estimate_only:
        return 0
    try:
        out = run(args.brand, args.mode)
    except apify.ApifyError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({k: out[k] for k in ("mode", "run_id", "usd", "actor")} | {"rows": len(out["rows"]), "third_party": sum(1 for r in out["rows"] if r["third_party_seller"])}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
