"""Stack detector: reads a store's own HTML and writes app/brain stack records.

No BuiltWith or Wappalyzer call. Signatures in stack.signatures.json are matched
against the store's own pages: script hosts, meta tags, cookie names, CSS
classes, JSON keys and response headers. A signature can require several
patterns to match the same page (`all`); otherwise the first signature that
matches, in file order, wins its field, so a specific signature should sit
before a generic fallback for the same field. `multi: true` fields (payments,
analytics) keep every distinct vendor matched instead of only the first.

Input is either a directory of saved pages (`--pages`) or one live url fetched
once (`--url` alone). A saved page's file name encodes its path under the
brand's `--url`: `index.html` is `/`, and `__` stands for `/`, so
`collections__mens-socks.html` is `/collections/mens-socks`. A `robots.txt`
file in the pages directory is read the same way. An optional `headers.json`
in the pages directory maps a file name to `{"headers": {...}, "set_cookie":
[...]}` for header and cookie signatures; live fetches capture headers and
cookies from the one response.

CLI: python3 -m app.brain.extract.stack --brand <slug> --url <store> [--pages <dir>] [--out app/brain]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urljoin

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

USER_AGENT = "ecomOS-stack-detector/1.0 (+https://github.com/KevCode-Absurd/ecomOS)"

FIELD_LABELS = {
    "platform": "its ecommerce platform",
    "theme": "its storefront theme",
    "reviews_app": "its product reviews",
    "upsell_app": "cart upsells and bundles",
    "tag_manager": "tag management",
    "cookie_consent": "cookie and privacy consent",
    "ab_testing": "on site experimentation",
    "performance_vendor": "web performance and edge acceleration",
    "support_app": "chat and help desk support",
    "email_sms_app": "email and SMS marketing",
    "loyalty_app": "its loyalty program",
    "subscription_app": "subscriptions",
    "payment_wallets": "checkout payment options",
    "analytics_tags": "analytics and ad tracking",
    "search_app": "on site search",
    "form_security": "form and login protection",
    "agent_commerce_endpoint": "AI shopping agent access",
}


def load_signatures(path: Path | None = None) -> list[dict]:
    path = path or HERE / "stack.signatures.json"
    return json.loads(path.read_text(encoding="utf-8"))["signatures"]


def _path_for_file(name: str) -> str:
    stem = name.rsplit(".", 1)[0]
    if name == "robots.txt":
        return "/robots.txt"
    if stem == "index":
        return "/"
    return "/" + stem.replace("__", "/")


def read_pages(pages_dir: Path, base_url: str) -> list[dict]:
    """A directory of saved pages plus optional headers.json -> a list of docs, home first."""
    pages_dir = Path(pages_dir)
    extra = {}
    headers_file = pages_dir / "headers.json"
    if headers_file.exists():
        extra = json.loads(headers_file.read_text(encoding="utf-8"))
    docs = []
    files = list(pages_dir.glob("*.html"))
    robots = pages_dir / "robots.txt"
    if robots.exists():
        files.append(robots)
    for f in files:
        path = _path_for_file(f.name)
        meta = extra.get(f.name, {})
        docs.append({
            "url": urljoin(base_url.rstrip("/") + "/", path.lstrip("/")),
            "text": f.read_text(encoding="utf-8", errors="replace"),
            "headers": meta.get("headers", {}),
            "cookies": meta.get("set_cookie", []),
        })
    docs.sort(key=lambda d: len(d["url"]))
    return docs


def fetch_live(url: str, timeout: float = 15.0) -> list[dict]:
    """One polite GET of url. No retries, no crawling."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        text = resp.read().decode(resp.headers.get_content_charset() or "utf-8", errors="replace")
        headers = {k: v for k, v in resp.headers.items()}
        cookies = resp.headers.get_all("Set-Cookie") or []
    return [{"url": url, "text": text, "headers": headers, "cookies": cookies}]


def _doc_text(doc: dict, kind: str) -> str:
    if kind == "header":
        return "\n".join(f"{k}: {v}" for k, v in doc.get("headers", {}).items())
    if kind == "cookie":
        return "; ".join(doc.get("cookies", []))
    return doc.get("text", "")


def _try_match(sig: dict, text: str) -> dict | None:
    """All of the signature's patterns must search-match text. Returns merged named groups, or None."""
    match = sig["match"]
    patterns = match.get("all") or [match["pattern"]]
    groups: dict[str, str] = {}
    quotes = []
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if not m:
            return None
        groups.update({k: v for k, v in m.groupdict().items() if v is not None})
        quotes.append(m.group(0))
    groups["_quote"] = " | ".join(quotes)[:200]
    return groups


def detect(docs: list[dict], signatures: list[dict]) -> dict:
    """Signatures matched against docs (home first) -> field -> list of hits, each {vendor, quote, ref}."""
    field_hits: dict[str, list[dict]] = {}
    field_done: set[str] = set()
    for sig in signatures:
        field = sig["field"]
        if not sig.get("multi") and field in field_done:
            continue
        kind = sig["match"]["type"]
        for doc in docs:
            groups = _try_match(sig, _doc_text(doc, kind))
            if groups is None:
                continue
            vendor = sig["vendor"].format(**{k: v for k, v in groups.items() if k != "_quote"})
            hit = {"vendor": vendor, "quote": groups["_quote"], "ref": doc["url"]}
            existing = field_hits.setdefault(field, [])
            if not sig.get("multi"):
                existing.append(hit)
                field_done.add(field)
            elif not any(h["vendor"] == vendor for h in existing):
                existing.append(hit)
            break
    return field_hits


def _join_vendors(vendors: list[str]) -> str:
    if len(vendors) == 1:
        return vendors[0]
    return ", ".join(vendors[:-1]) + " and " + vendors[-1]


def build_records(brand: str, field_hits: dict, captured_at: str) -> list[dict]:
    records = []
    brand_title = brand.replace("-", " ").replace("_", " ").title()
    for field, hits in field_hits.items():
        multi = len(hits) > 1 and field in ("payment_wallets", "analytics_tags")
        value = [h["vendor"] for h in hits] if multi else hits[0]["vendor"]
        value_str = _join_vendors([h["vendor"] for h in hits]) if multi else hits[0]["vendor"]
        label = FIELD_LABELS.get(field, field.replace("_", " "))
        records.append({
            "id": f"{brand}.stack.{field}",
            "brand": brand,
            "section": "stack",
            "field": field,
            "value": value,
            "text": f"{brand_title} uses {value_str} for {label}.",
            "source": {"type": "site", "ref": hits[0]["ref"], "captured_at": captured_at},
            "confidence": 0.85,
            "tier": "site_backed",
            "visibility": "public",
            "evidence": [{"quote": h["quote"], "ref": h["ref"]} for h in hits],
        })
    records.sort(key=lambda r: r["field"])
    return records


def write_stack(out_root: Path, brand: str, records: list[dict], sources: list[dict]) -> Path:
    folder = Path(out_root) / brand / "raw" / "a-site"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "stack.json").write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    src_file = folder / "sources.json"
    existing = json.loads(src_file.read_text(encoding="utf-8")) if src_file.exists() else []
    known = {s["url"] for s in existing}
    for s in sources:
        if s["url"] not in known:
            existing.append(s)
            known.add(s["url"])
    src_file.write_text(json.dumps(existing, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return folder


def run(brand: str, docs: list[dict], captured_at: str, signatures: list[dict] | None = None) -> list[dict]:
    signatures = signatures or load_signatures()
    field_hits = detect(docs, signatures)
    return build_records(brand, field_hits, captured_at)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--brand", required=True)
    ap.add_argument("--url", required=True, help="the store's base url, e.g. https://shop.example.com")
    ap.add_argument("--pages", help="a directory of saved pages; omit to fetch --url live, once")
    ap.add_argument("--out", default="app/brain", help="brain root to write <brand>/raw/a-site/ under")
    ap.add_argument("--date", help="capture date YYYY-MM-DD, default today")
    args = ap.parse_args(argv)

    import datetime as dt
    captured_at = args.date or dt.date.today().isoformat()

    if args.pages:
        docs = read_pages(Path(args.pages), args.url)
    else:
        try:
            docs = fetch_live(args.url)
        except (urllib.error.URLError, TimeoutError) as exc:
            print(f"could not fetch {args.url}: {exc}", file=sys.stderr)
            return 1

    records = run(args.brand, docs, captured_at)
    sources = [{"url": d["url"], "date": captured_at} for d in docs]
    folder = write_stack(Path(args.out), args.brand, records, sources)
    print(f"{len(records)} stack records written to {folder / 'stack.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
