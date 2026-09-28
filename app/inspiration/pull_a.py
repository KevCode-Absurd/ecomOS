"""Inspiration puller A: Meta Ad Library pages -> creative and offers references.

Runs the Ad Library lane through the existing ApifyClient (same actor, caps and ledger as
app/brain/extract/apify_adlibrary.py) over the brand's config/apify.json pages, by page id
only. Every ad item becomes a creative reference, plus an offers reference when the ad
carries a promo. Tags (format, hook, layout, mood, topics) come from app/inspiration/tag.py,
relevance from app/inspiration/relevance.py over the brand's brain. Media is downloaded at
pull time into app/inspiration/media/<brand>/<origin>/ (git-ignored): own ads in full,
competitor ads as image plus video thumbnail, the video kept as a remote url with its expiry.

Mock mode reads the connector fixture (plus app/inspiration/fixtures/meta_ad_library_pages/
extra_items.json), makes no network call and downloads nothing: media reads kind none with
a note.

  python3 -m app.inspiration.pull_a --brand bombas [--mode mock|live] [--out app/inspiration]
  python3 -m app.inspiration.pull_a --purge "Comrad Socks" [--brand bombas]
"""
from __future__ import annotations

import argparse
import copy
import datetime as dt
import hashlib
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.brain.extract.apify_adlibrary import PAGE, keep_configured_pages  # noqa: E402
from app.connectors import apify  # noqa: E402
from app.inspiration import media as media_mod  # noqa: E402
from app.inspiration import relevance, tag  # noqa: E402

SOURCE = "meta_ad_library_pages"
OFFER_SOURCE = "competitor_promos"
EXTRA_FIXTURE = HERE / "fixtures" / SOURCE / "extra_items.json"
MOCK_NOTE = "fixture mode: media not downloaded"
ROLES = {"self": "own", "own": "own", "competitor": "competitor", "leader": "leader"}


def load_config(brand: str) -> dict:
    return json.loads((ROOT / "app" / "brain" / brand / "config" / "apify.json").read_text(encoding="utf-8"))


def build_input(cfg: dict) -> tuple[dict, int, list[dict], list[str]]:
    """Actor input over pages with a known page id. Name searches are never run here."""
    status, country = cfg.get("active_status", "active"), cfg.get("country", "US")
    pages = [p for p in cfg.get("pages", []) if p.get("page_id")]
    skipped = [p["name"] for p in cfg.get("pages", []) if not p.get("page_id")]
    urls = [PAGE.format(status=status, country=country, page_id=p["page_id"]) for p in pages]
    per = cfg.get("limit_per_source", 100)
    actor_input = {"urls": [{"url": u} for u in urls], "scrapeAdDetails": bool(cfg.get("scrape_ad_details", False)),
                   "limitPerSource": per, "scrapePageAds.activeStatus": status, "scrapePageAds.countryCode": country}
    return actor_input, per * max(len(urls), 1), pages, skipped


def role_of(item: dict, pages: list[dict]) -> tuple[str, str]:
    """(origin brand, contract role) for an item, by page id first, then by page name."""
    name = item.get("page_name") or ""
    for p in pages:
        if p.get("page_id") and str(p["page_id"]) == str(item.get("page_id")):
            return p["name"], ROLES.get(p.get("role", "competitor"), "competitor")
    for p in pages:
        if relevance._same_brand(p["name"], name):
            return p["name"], ROLES.get(p.get("role", "competitor"), "competitor")
    return name, "competitor"


def _rid(domain: str, source: str, key: str) -> str:
    return f"insp.{domain}.{source}.{hashlib.sha1(key.encode()).hexdigest()[:10]}"


def to_references(items: list[dict], brand: str, pages: list[dict], captured_at: str, facts: relevance.Facts,
                  dl: media_mod.Downloader | None, fixture: bool) -> tuple[list[dict], list[dict]]:
    creative, offers = [], []
    for item in items:
        key = str(item.get("ad_archive_id") or item.get("ad_id") or item.get("url"))
        origin_brand, role = role_of(item, pages)
        rights = "own_brand" if role == "own" else "reference_only"
        text = tag.ad_text(item)
        sig, tags = tag.signals(item, captured_at)
        origin = {"brand": origin_brand, "role": role, "url": item.get("url"),
                  "page_id": str(item["page_id"]) if item.get("page_id") else None}
        med = media_mod.collect(item, rights, brand, origin_brand, key, dl, MOCK_NOTE if dl is None else None)
        ref = {"id": _rid("creative", SOURCE, key), "domain": "creative", "source": SOURCE, "captured_at": captured_at,
               "origin": origin, "signals": sig, "quote": tag.quote(text), "media": med,
               "relevance": {"score": 0.0, "reasons": []}, "tags": tags}
        if fixture:
            ref["notes"] = "fixture data, not scraped"
        ref["relevance"] = relevance.score(ref, facts)
        creative.append(ref)
        if sig.get("offer_type"):
            osig = {k: sig.get(k) for k in ("offer_type", "discount_pct", "code", "threshold_usd", "price_usd",
                                            "promo", "start_date", "run_days", "active") if k in sig}
            off = {"id": _rid("offers", OFFER_SOURCE, key), "domain": "offers", "source": OFFER_SOURCE,
                   "captured_at": captured_at, "origin": dict(origin), "signals": osig,
                   "quote": tag.quote(sig.get("promo") or text), "media": copy.deepcopy(med),
                   "relevance": {"score": 0.0, "reasons": []}, "tags": tags + [f"offer:{sig['offer_type']}"],
                   "notes": ("fixture data, not scraped; " if fixture else "") + f"from creative reference {ref['id']}"}
            off["relevance"] = relevance.score(off, facts)
            offers.append(off)
    return creative, offers


def _order(refs: list[dict]) -> list[dict]:
    return sorted(refs, key=lambda r: (-r["relevance"]["score"], r["origin"]["brand"], r["id"]))


def write_domain(out: Path, brand: str, domain: str, source: str, refs: list[dict]) -> Path:
    """Replace this source's records in <out>/<brand>/<domain>.json, keep other sources'."""
    path = Path(out) / brand / f"{domain}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    old = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    kept = [r for r in old if r.get("source") != source]
    path.write_text(json.dumps(_order(kept + refs), indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def pull(brand: str, mode: str = "mock", out: Path | str | None = None, *, client=None, downloader=None,
         captured_at: str | None = None, config: dict | None = None, facts: relevance.Facts | None = None) -> dict:
    config = config or load_config(brand)
    cfg = config["meta_ad_library"]
    day = captured_at or dt.date.today().isoformat()
    client = client or apify.ApifyClient(mode=mode, brand=brand, budget=config.get("budget"),
                                         today=dt.date.fromisoformat(day))
    actor_input, max_items, pages, skipped = build_input(cfg)
    items = client.run(cfg["actor"], actor_input, max_items, lane="adlibrary")
    if client.mode == "mock" and EXTRA_FIXTURE.exists():
        items = items + json.loads(EXTRA_FIXTURE.read_text(encoding="utf-8"))["items"]
    pulled = len(items)
    items = keep_configured_pages(items, cfg.get("pages", []))
    dl = None if client.mode == "mock" else (downloader or media_mod.Downloader())
    facts = facts or relevance.Facts(brand)
    creative, offers = to_references(items, brand, cfg.get("pages", []), day, facts, dl, client.mode == "mock")
    out = Path(out) if out else HERE
    write_domain(out, brand, "creative", SOURCE, creative)
    write_domain(out, brand, "offers", OFFER_SOURCE, offers)
    return {"brand": brand, "mode": client.mode, "run_id": (client.last_run or {}).get("run_id"), "items": pulled,
            "kept": len(items), "creative": len(creative), "offers": len(offers),
            "shown": sum(r["relevance"]["shown"] for r in creative + offers),
            "pages_skipped_no_id": skipped, "media_errors": (dl.errors if dl else [])}


def purge(origin: str, out: Path | str | None = None, brand: str | None = None, media_root: Path | str | None = None) -> dict:
    """Remove every reference whose origin brand is `origin`, and its media files, for a takedown."""
    out = Path(out) if out else HERE
    media_root = Path(media_root) if media_root else media_mod.MEDIA_ROOT
    target = relevance._norm(origin)
    brands = [brand] if brand else [d.name for d in out.iterdir()
                                    if d.is_dir() and d.name not in ("fixtures", "media", "__pycache__")]
    removed, files = 0, 0
    for b in brands:
        for path in sorted((out / b).glob("*.json")):
            refs = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(refs, list):
                continue
            keep = [r for r in refs if relevance._norm((r.get("origin") or {}).get("brand", "")) != target]
            for r in refs:
                if r not in keep:
                    for f in (r.get("media") or {}).get("files") or []:
                        p = ROOT / f if not Path(f).is_absolute() else Path(f)
                        if p.exists():
                            p.unlink()
                            files += 1
            if len(keep) != len(refs):
                removed += len(refs) - len(keep)
                path.write_text(json.dumps(keep, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        folder = media_root / media_mod.slug(b) / media_mod.slug(origin)
        if folder.is_dir():
            files += sum(1 for p in folder.rglob("*") if p.is_file())
            shutil.rmtree(folder)
    return {"origin": origin, "references_removed": removed, "media_files_removed": files, "brands": brands}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Pull Meta Ad Library references for a brand, or purge an origin brand.")
    ap.add_argument("--brand")
    ap.add_argument("--mode", default="mock", choices=("mock", "live"))
    ap.add_argument("--out", help="inspiration root, default app/inspiration")
    ap.add_argument("--date", help="capture date YYYY-MM-DD, default today")
    ap.add_argument("--purge", metavar="ORIGIN_BRAND", help="remove every reference and media file about this brand")
    args = ap.parse_args(argv)
    if args.purge:
        print(json.dumps(purge(args.purge, args.out, args.brand), indent=1))
        return 0
    if not args.brand:
        ap.error("--brand is required unless --purge is given")
    try:
        result = pull(args.brand, args.mode, args.out, captured_at=args.date)
    except apify.ApifyError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
