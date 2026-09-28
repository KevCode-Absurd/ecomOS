"""Amazon listing discovery for any brand on a fixed small budget: finds the ASINs, then the review lane runs.

Order, cheapest first, stopping once 10 or more ASINs with a ratings count are known:
  1. Amazon links on the brand's own site (the site crawler's saved pages, or files given with --site):
     /dp/, /gp/product/ and a /stores/ link. Free, but a link carries no ratings count.
  2. The brand store page (a /stores/ link from step 1, else config `store_url`, else
     amazon.com/stores/<Name>), one polite public fetch. A sign-in page, robot check or non-200 is
     recorded as unavailable with the reason and the next step runs.
  3. The axesso product search actor, capped at 50 results and a hard $1 through ApifyClient's caps.
     junglee~amazon-crawler is never used for search: it cost $8.64 for 160 results on 28 Sep.
Results are kept only when the brand matches (manufacturer or seller field, else the title starts with
the brand name), so another brand's socks named "better than Bombas" are dropped.

Writes `marketplaces` listing records to <out>/<brand>/raw/amazon-discover/ and ranks the config
`amazon_reviews.asins` by review_count: the top 10 stay in `asins`, the rest go to `asins_backlog`.
The review lane (apify_amazon.py) then runs unchanged.

    python3 -m app.brain.extract.amazon_discover --brand bombas --name "Bombas" [--site URL|DIR] \
        [--mode mock|live] [--max-usd 1.00]

Mock mode reads fixtures only (fixtures/amazon_discover/<brand>/), makes no network call and no ledger
entry, and writes under app/connectors/.mock unless --out is given, so invented counts never reorder a
real config.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html as htmllib
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.connectors import apify, apify_adapters  # noqa: E402

HERE = Path(__file__).resolve().parent
FIXTURES = HERE / "fixtures" / "amazon_discover"
SITE_FIXTURES = HERE / "fixtures" / "site"
SEARCH_ACTOR = "axesso_data~amazon-product-search-scraper"
NEVER_FOR_SEARCH = {"junglee~amazon-crawler"}
MAX_RESULTS = 50
HARD_MAX_USD = 1.00
ENOUGH = 10
KEEP_TOP = 10
UA = "Mozilla/5.0 (compatible; ecomOS brand setup; public pages only)"
# Not verified on the Store: an upper bound so the estimate stays safe. 50 results reserve $0.56.
apify.PRICES_PER_1000.setdefault(SEARCH_ACTOR, 5.00)

ASIN = r"([A-Z0-9]{10})"
DP_LINK = re.compile(r"amazon\.[a-z.]+/(?:[^\s\"'<>]*?/)?(?:dp|gp/product|gp/aw/d)/" + ASIN, re.I)
STORE_LINK = re.compile(r"https?://(?:www\.)?amazon\.[a-z.]+/(?:stores/[^\s\"'<>?#]+|s\?[^\s\"'<>#]*\bme=[A-Z0-9]+[^\s\"'<>#]*)", re.I)
SHORT_LINK = re.compile(r"https?://(?:amzn\.to|a\.co)/[A-Za-z0-9]+", re.I)
WALL = [("ap/signin", "sign-in page"), ("validatecaptcha", "robot check"), ("robot check", "robot check"),
        ("enter the characters you see", "robot check"), ("to discuss automated access", "robot check")]
LINES = [("no_show", ("no show", "no-show")), ("compression", ("compression",)), ("merino", ("merino",)),
         ("running", ("running", "performance")), ("slipper", ("slipper",)), ("ankle", ("ankle",)),
         ("quarter", ("quarter",)), ("calf", ("calf", "crew")), ("underwear", ("underwear", "boxer", "brief")),
         ("tshirt", ("t-shirt", "tee")), ("gift", ("gift box", "gift"))]


class DiscoverError(RuntimeError):
    pass


def norm(s) -> str:
    return " ".join(re.sub(r"[^a-z0-9]+", " ", str(s or "").lower()).split())


def line_of(title: str) -> str | None:
    t = f" {norm(title)} "
    for line, terms in LINES:
        if any(f" {norm(term)} " in t for term in terms):
            return line
    return None


def to_int(v) -> int | None:
    if isinstance(v, (int, float)):
        return int(v)
    m = re.search(r"\d[\d,]*", str(v or ""))
    return int(m.group(0).replace(",", "")) if m else None


def to_float(v) -> float | None:
    if isinstance(v, (int, float)):
        return float(v)
    m = re.search(r"\d+(?:\.\d+)?", str(v or ""))
    return float(m.group(0)) if m else None


# ---------- step 1: the brand's own site ----------

def site_pages(site: str | Path | None, brand: str) -> list[str]:
    """HTML of the saved site pages: a directory, one file, or the crawler's fixture for the brand."""
    path = Path(site) if site else SITE_FIXTURES / brand
    if not path.exists():
        return []
    files = [path] if path.is_file() else sorted(path.glob("*.html"))
    return [f.read_text(encoding="utf-8", errors="replace") for f in files]


def site_links(pages: list[str]) -> dict:
    asins, stores, short = [], [], []
    for page in pages:
        text = htmllib.unescape(page)
        for a in DP_LINK.findall(text):
            if a.upper() not in asins:
                asins.append(a.upper())
        for s in STORE_LINK.findall(text):
            if s not in stores:
                stores.append(s)
        for s in SHORT_LINK.findall(text):
            if s not in short:
                short.append(s)
    return {"asins": asins, "store_urls": stores, "short_links": short}


# ---------- step 2: the brand store page ----------

def store_url_for(name: str, links: dict, cfg: dict) -> str:
    if links["store_urls"]:
        return links["store_urls"][0]
    if cfg.get("store_url"):
        return cfg["store_url"]
    return "https://www.amazon.com/stores/" + urllib.parse.quote(re.sub(r"\s+", "", name))


def live_fetch(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return {"status": resp.status, "final_url": resp.geturl(), "html": resp.read(2_000_000).decode("utf-8", "replace")}
    except urllib.error.HTTPError as exc:
        return {"status": exc.code, "final_url": url, "html": ""}
    except Exception as exc:  # noqa: BLE001  a network failure is a reason, not a crash
        return {"status": None, "final_url": url, "html": "", "error": type(exc).__name__}


def fixture_fetch(folder: Path):
    def fetch(url: str) -> dict:
        meta_path = folder / "store-page.json"
        if not meta_path.exists():
            return {"status": None, "final_url": url, "html": "", "error": "no saved store page"}
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        return {"status": meta.get("status"), "final_url": meta.get("final_url") or url,
                "html": (folder / meta["file"]).read_text(encoding="utf-8")}
    return fetch


def store_page(url: str, fetch) -> dict:
    resp = fetch(url)
    body, final = resp.get("html") or "", resp.get("final_url") or url
    probe = (final + " " + body[:20000]).lower()
    reason = None
    if resp.get("error"):
        reason = f"fetch failed: {resp['error']}"
    elif resp.get("status") != 200:
        reason = f"HTTP {resp.get('status')}"
    else:
        reason = next((why for cue, why in WALL if cue in probe), None)
    if reason:
        return {"step": "store_page", "url": url, "status": "unavailable", "reason": reason, "items": []}
    items = []
    for m in re.finditer(r'data-asin="([A-Z0-9]{10})"(.*?)(?=data-asin=|$)', body, re.S):
        chunk = m.group(2)
        title = re.search(r"<h2[^>]*>(.*?)</h2>", chunk, re.S)
        stars = re.search(r'aria-label="([\d.]+) out of 5 stars"', chunk)
        count = re.search(r'aria-label="([\d,]+) ratings?"', chunk)
        items.append({"asin": m.group(1), "title": htmllib.unescape(re.sub(r"<[^>]+>", "", title.group(1))).strip() if title else None,
                      "rating": to_float(stars.group(1)) if stars else None,
                      "review_count": to_int(count.group(1)) if count else None,
                      "price": None, "availability": None, "seller": None, "found_by": "store_page"})
    return {"step": "store_page", "url": url, "status": "ok", "reason": None, "items": items}


# ---------- step 3: the product search actor ----------

def search_input(name: str, domain: str, results: int) -> dict:
    # Input keys as pinned in fixtures/amazon_discover/bombas/<actor>.json; one page is about 48 results.
    return {"input": [{"keyword": name, "domainCode": domain, "sortBy": "relevanceblender",
                       "maxPages": max(1, -(-results // 48)), "category": "aps"}]}


def search(client, name: str, domain: str, results: int = MAX_RESULTS, max_usd: float = HARD_MAX_USD,
           actor: str = SEARCH_ACTOR) -> dict:
    if actor in NEVER_FOR_SEARCH:
        raise DiscoverError(f"{actor} is never used for search: it cost $8.64 for 160 results on 28 Sep")
    if results > MAX_RESULTS:
        raise apify.ApifyCapError(f"run refused: {results} results is over the discovery cap of {MAX_RESULTS}")
    cap = min(max_usd, HARD_MAX_USD)
    raw = client.run(actor, search_input(name, domain, results), results, max_usd=cap, lane="amazon-discover")
    items = []
    for it in raw[:results]:
        seller = it.get("soldBy") or it.get("seller")
        items.append({"asin": it.get("asin"), "title": it.get("productDescription") or it.get("title"),
                      "brand_field": it.get("manufacturer") or it.get("brand"),
                      "rating": to_float(it.get("productRating") or it.get("stars")),
                      "review_count": to_int(it.get("countReview") if it.get("countReview") is not None else it.get("reviewsCount")),
                      "price": it.get("price"), "availability": it.get("availability"),
                      "seller": seller.get("name") if isinstance(seller, dict) else seller, "found_by": "search_actor"})
    return {"step": "search_actor", "actor": actor, "status": "ok", "reason": None, "results": len(raw),
            "cap_usd": cap, "estimate_usd": apify.estimate_usd(actor, results), "run_id": (client.last_run or {}).get("run_id"),
            "items": items}


def is_brand(item: dict, name: str) -> bool:
    """Brand field decides when present; else the title must start with the brand name as whole words."""
    want = norm(name)
    field = item.get("brand_field") or None
    if field:
        return norm(field) == want
    title = norm(item.get("title"))
    return title == want or title.startswith(want + " ")


# ---------- ranking and writes ----------

def counted(found: dict) -> int:
    return sum(1 for it in found.values() if it.get("review_count") is not None)


def merge_items(found: dict, items: list[dict]) -> None:
    for it in items:
        asin = (it.get("asin") or "").upper()
        if not re.fullmatch(r"[A-Z0-9]{10}", asin):
            continue
        cur = found.setdefault(asin, {"asin": asin, "found_by": []})
        for k in ("title", "rating", "review_count", "price", "availability", "seller"):
            if cur.get(k) is None and it.get(k) is not None:
                cur[k] = it[k]
        if it["found_by"] not in cur["found_by"]:
            cur["found_by"].append(it["found_by"])


def rank(found: dict, existing: list[str], keep: int = KEEP_TOP) -> tuple[list[str], list[str]]:
    """Counted ASINs by review_count, highest first; then uncounted ones, config order first."""
    have = sorted((a for a, it in found.items() if it.get("review_count") is not None),
                  key=lambda a: (-found[a]["review_count"], a))
    rest = [a for a in existing if a not in have] + sorted(a for a in found if a not in have and a not in existing)
    order = have + rest
    return order[:keep], order[keep:]


def listing_records(brand: str, found: dict, day: str, mode: str, run_id: str | None) -> list[dict]:
    out = []
    for asin, it in sorted(found.items()):
        title = apify_adapters.clean(it.get("title"), 200) if it.get("title") else None
        value = {"channel": "amazon", "asin": asin, "title": title, "line": line_of(title or ""),
                 "rating": it.get("rating"), "review_count": it.get("review_count"), "price": it.get("price"),
                 "availability": it.get("availability"), "seller": it.get("seller"), "found_by": it["found_by"]}
        count = f"{value['review_count']:,} ratings" if value["review_count"] is not None else "ratings unavailable"
        stars = f"{value['rating']} stars" if value["rating"] is not None else "stars unavailable"
        by = it["found_by"][0]
        ref = (apify_adapters.ref(SEARCH_ACTOR, run_id or "unknown", f"https://www.amazon.com/dp/{asin}")
               if by == "search_actor" else f"https://www.amazon.com/dp/{asin}")
        rec = apify_adapters.record(brand, "marketplaces", f"amazon_{apify_adapters.slug(asin)}", value,
                                    f"Amazon listing {asin}: {stars}, {count}.", "site", ref, day)
        if mode == "mock":
            rec["notes"] = "fixture data, not scraped"
        out.append(rec)
    return out


def write_json(path: Path, data) -> bool:
    text = json.dumps(data, indent=1, ensure_ascii=False) + "\n"
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return True


def update_config(config: dict, top: list[str], backlog: list[str], steps: list[dict], day: str) -> dict:
    cfg = config.setdefault("amazon_reviews", {})
    cfg["asins"] = top
    cfg["asins_backlog"] = backlog
    disc = cfg.setdefault("discovery", {})
    disc["last_run"] = {"date": day, "steps": [{k: s.get(k) for k in ("step", "status", "reason", "found") if s.get(k) is not None}
                                               for s in steps]}
    return config


# ---------- the run ----------

def run(brand: str, name: str, config: dict, *, mode: str = "mock", site=None, out=None, max_usd: float = HARD_MAX_USD,
        client=None, fetch=None, captured_at: str | None = None, fixtures: Path | None = None) -> dict:
    day = captured_at or dt.date.today().isoformat()
    cfg = config.get("amazon_reviews") or {}
    disc_cfg = cfg.get("discovery") or {}
    domain = cfg.get("domain_code", "com")
    fixtures = Path(fixtures) if fixtures else FIXTURES / brand
    enough = disc_cfg.get("enough", ENOUGH)
    found: dict = {}
    steps: list[dict] = []

    # 1. the brand's own site
    pages = site_pages(site, brand) if not (isinstance(site, str) and site.startswith("http")) else []
    if isinstance(site, str) and site.startswith("http"):
        if mode == "mock":
            raise DiscoverError("mock mode reads saved pages only; pass a directory or file to --site")
        pages = [live_fetch(site).get("html") or ""]
    links = site_links(pages)
    merge_items(found, [{"asin": a, "found_by": "site"} for a in links["asins"]])
    steps.append({"step": "site", "status": "ok" if pages else "unavailable",
                  "reason": None if pages else "no saved site pages", "found": len(links["asins"]),
                  "store_urls": links["store_urls"], "short_links": links["short_links"]})

    # 2. the brand store page
    if counted(found) < enough:
        url = store_url_for(name, links, disc_cfg)
        fetch = fetch or (fixture_fetch(fixtures) if mode == "mock" else live_fetch)
        res = store_page(url, fetch)
        merge_items(found, res["items"])
        steps.append({"step": "store_page", "url": url, "status": res["status"], "reason": res["reason"],
                      "found": len(res["items"])})

    # 3. the search actor, capped
    run_id = None
    if counted(found) < enough:
        client = client or apify.ApifyClient(mode=mode, brand=brand, budget=config.get("budget"),
                                             fixtures_dir=fixtures if mode == "mock" else None)
        res = search(client, name, domain, min(disc_cfg.get("max_results", MAX_RESULTS), MAX_RESULTS),
                     min(max_usd, disc_cfg.get("max_usd", HARD_MAX_USD)), disc_cfg.get("search_actor", SEARCH_ACTOR))
        kept = [it for it in res["items"] if is_brand(it, name)]
        merge_items(found, kept)
        run_id = res["run_id"]
        steps.append({"step": "search_actor", "status": "ok", "reason": None, "found": len(kept),
                      "dropped": len(res["items"]) - len(kept), "results": res["results"],
                      "estimate_usd": res["estimate_usd"], "cap_usd": res["cap_usd"], "run_id": run_id})

    top, backlog = rank(found, list(cfg.get("asins") or []), disc_cfg.get("keep_top", KEEP_TOP))
    out_root = Path(out) if out else (apify.MOCK_OUT if mode == "mock" else ROOT / "app" / "brain")
    records = listing_records(brand, found, day, mode, run_id)
    raw = out_root / brand / "raw" / "amazon-discover"
    write_json(raw / "marketplaces.json", records)
    write_json(raw / "sources.json", [dict(s, accessed=day, mode=mode) for s in steps])
    config_path = out_root / brand / "config" / "apify.json"
    changed = write_json(config_path, update_config(json.loads(json.dumps(config)), top, backlog, steps, day))
    return {"brand": brand, "asins": top, "asins_backlog": backlog, "counted": counted(found), "steps": steps,
            "records": len(records), "raw": str(raw), "config": str(config_path), "config_changed": changed}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Find a brand's Amazon ASINs cheaply and rank them for the review lane.")
    ap.add_argument("--brand", required=True)
    ap.add_argument("--name", required=True, help="brand name as it appears on Amazon")
    ap.add_argument("--site", help="saved site pages (dir or file) or, in live mode, the store url")
    ap.add_argument("--mode", default="mock", choices=("mock", "live"))
    ap.add_argument("--max-usd", type=float, default=HARD_MAX_USD)
    ap.add_argument("--out", help="root for <brand>/raw and <brand>/config; mock default app/connectors/.mock, live default app/brain")
    ap.add_argument("--date", help="capture date YYYY-MM-DD, default today")
    args = ap.parse_args(argv)
    config = json.loads((ROOT / "app" / "brain" / args.brand / "config" / "apify.json").read_text(encoding="utf-8"))
    try:
        result = run(args.brand, args.name, config, mode=args.mode, site=args.site, out=args.out,
                     max_usd=args.max_usd, captured_at=args.date)
    except (apify.ApifyError, DiscoverError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
