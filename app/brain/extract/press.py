"""Press extractor: one free public search for the brand, into economics, story_bank and team.

Usage:
  python3 -m app.brain.extract.press --brand bombas --brand-name Bombas --site-url https://bombas.com
  python3 -m app.brain.extract.press --brand bombas --brand-name Bombas \
      --fixture app/brain/extract/fixtures/press/bombas --out /tmp/brain

Fetches one Bing web search results page for the brand name plus press-finding terms
(founder, interview, revenue, funding), reads its result cards (title, url, a snippet, a
date when the snippet carries one), and classifies each into economics (money and scale),
team (leadership and hires), or story_bank (a founder story, or a plain press mention when
no sharper signal is found). The brand's own domain and common marketplaces are skipped:
they are not press. Every record carries tier "reported", its source url and a capture
date.

Polite by design: one request, a descriptive user agent, a public page, no credentials.
--fixture reads a saved copy of the search page instead of the network. --save-fixture PATH
saves the live response for reuse. No third-party packages.
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import html
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

USER_AGENT = "ecomOS-press-extractor/0.1 (public brand onboarding search; 1 request per run)"
SEARCH_URL = "https://www.bing.com/search"
MAX_TEXT = 300
MAX_RESULTS = 10
EM_DASH = "—"

# Not press: the brand's own domain (passed in) plus common marketplaces and reference sites.
RETAIL_DOMAINS = {"nordstrom.com", "nordstromrack.com", "dsw.com", "walmart.com", "target.com",
                  "dillards.com", "amazon.com", "macys.com", "zappos.com", "kohls.com", "costco.com",
                  "backcountry.com", "rei.com", "wikipedia.org"}
ECONOMICS_KW = ["revenue", "funding", "raised", "valuation", "million", "billion", "profit", "ipo", "ebitda"]
TEAM_KW = ["chief executive", " ceo", "cfo", "cmo", "coo", "president", "appoints", "names ", "joins as", "hires", "hired"]
STORY_KW = ["founder", "co-founder", "cofounder", "interview", "shark tank", "story of", "journey",
            "how i built", "behind the brand"]
DATE_RE = re.compile(r"^([A-Z][a-z]{2}\s+\d{1,2},\s+\d{4})\b")


def clean(s: str) -> str:
    s = html.unescape(s or "").replace(EM_DASH, ", ")
    s = re.sub(r"…?\s*Read more\s*$", "", s)
    return re.sub(r"\s+", " ", s).strip()


def cap(s: str, n: int = MAX_TEXT) -> str:
    s = clean(s)
    return s if len(s) <= n else s[: n - 3].rstrip() + "..."


def slug(s: str, n: int = 50) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(s).lower()).strip("_")[:n] or "x"


def has(text: str, terms) -> bool:
    t = text.lower()
    return any(term in t for term in terms)


def domain_of(url: str) -> str:
    return urllib.parse.urlsplit(url).netloc.lower().removeprefix("www.")


def decode_bing_url(href: str) -> str | None:
    """Bing wraps result links in a redirect; the real url is base64 in its u= param (an a1 prefix)."""
    href = html.unescape(href)
    m = re.search(r"[?&]u=a1([A-Za-z0-9_-]+)", href)
    if not m:
        direct = urllib.parse.urlsplit(href)
        return href if direct.scheme and direct.netloc else None
    s = m.group(1) + "=" * (-len(m.group(1)) % 4)
    try:
        return base64.b64decode(s).decode("utf-8", "replace")
    except (ValueError, UnicodeDecodeError):
        return None


def parse_snippet_date(snippet: str) -> tuple[str | None, str]:
    """A leading "Mon D, YYYY" in the snippet is the article date; strip it from the text kept."""
    m = DATE_RE.match(snippet)
    if not m:
        return None, snippet
    try:
        day = dt.datetime.strptime(m.group(1), "%b %d, %Y").date().isoformat()
    except ValueError:
        return None, snippet
    rest = re.sub(r"^[\s·:-]+", "", snippet[m.end():])
    return day, rest


def parse_results(html_text: str) -> list[dict]:
    out = []
    for block in re.split(r'<li class="b_algo"', html_text)[1:]:
        mt = re.search(r'<h2[^>]*><a[^>]*>(.*?)</a></h2>', block, re.S)
        mh = re.search(r'<h2[^>]*><a[^>]*href="([^"]+)"', block, re.S)
        ms = re.search(r'<p class="b_lineclamp2"[^>]*>(.*?)</p>', block, re.S)
        if not (mt and mh):
            continue
        title = clean(re.sub(r"<[^>]+>", "", mt.group(1)))
        raw_snippet = clean(re.sub(r"<[^>]+>", "", ms.group(1))) if ms else ""
        date, snippet = parse_snippet_date(raw_snippet)
        url = decode_bing_url(mh.group(1))
        if not title or not url:
            continue
        out.append({"title": title, "url": url, "snippet": snippet, "date": date})
    return out[:MAX_RESULTS]


def classify(text: str) -> str:
    if has(text, ECONOMICS_KW):
        return "economics"
    if has(text, TEAM_KW):
        return "team"
    return "story_bank"  # a founder-story hit, or a plain press mention as the weakest signal


def record(brand: str, section: str, field: str, rid: str, value: dict, text: str, url: str, date: str) -> dict:
    return {"id": f"{brand}.{section}.{rid}", "brand": brand, "section": section, "field": field,
            "value": value, "text": cap(text),
            "source": {"type": "press", "ref": url, "captured_at": date},
            "tier": "reported", "visibility": "public"}


def _fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def run(brand: str, config: dict, *, root=None, captured_at: str | None = None,
        fixture: Path | str | None = None, save_fixture: Path | str | None = None) -> dict:
    cfg = config.get("press", {})
    brand_name = cfg.get("brand_name") or brand
    day = captured_at or dt.date.today().isoformat()
    site_domain = domain_of(cfg["site_url"]) if cfg.get("site_url") else None
    skip_domains = RETAIL_DOMAINS | ({site_domain} if site_domain else set())
    query = cfg.get("query") or f"{brand_name} founder interview revenue funding"
    url = f"{SEARCH_URL}?{urllib.parse.urlencode({'q': query})}"

    sources = []
    if fixture:
        raw = (Path(fixture) / "search.html").read_text(encoding="utf-8")
        sources.append({"url": url, "date": day, "status": 200, "note": "fixture, not fetched live"})
    else:
        try:
            raw = _fetch(url)
            sources.append({"url": url, "date": day, "status": 200})
            if save_fixture:
                out_fx = Path(save_fixture)
                out_fx.mkdir(parents=True, exist_ok=True)
                (out_fx / "search.html").write_text(raw, encoding="utf-8")
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            sources.append({"url": url, "date": day, "status": -1,
                           "note": f"fetch failed: {type(exc).__name__}; not used as evidence"})
            raw = ""

    results = parse_results(raw)
    records = []
    for r in results:
        dom = domain_of(r["url"])
        if not dom or dom == site_domain or any(dom == d or dom.endswith("." + d) for d in skip_domains):
            continue
        section = classify(f"{r['title']} {r['snippet']}")
        field = "press_signal" if section in ("economics", "team") else "press_mention"
        rid = f"{slug(dom)}_{slug(r['title'], 30)}"
        value = {"headline": cap(r["title"], 200), "snippet": cap(r["snippet"], 200), "url": r["url"],
                 "date": r["date"], "outlet": dom}
        label = {"economics": "touching money or scale", "team": "touching leadership",
                 "story_bank": "a mention"}[section]
        text = f"{brand_name} press result {label}: {r['title']}."
        records.append(record(brand, section, field, rid, value, text, r["url"], r["date"] or day))

    folder = (Path(root) if root else ROOT / "app" / "brain") / brand / "raw" / "press"
    folder.mkdir(parents=True, exist_ok=True)
    for old in folder.glob("*.json"):
        old.unlink()
    by_section: dict[str, list] = {}
    for rec in records:
        by_section.setdefault(rec["section"], []).append(rec)
    for section, recs in by_section.items():
        (folder / f"{section}.json").write_text(json.dumps(recs, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    (folder / "sources.json").write_text(json.dumps(sources, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return {"folder": str(folder), "results": len(results), "records": len(records)}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="One free public press search for a brand.")
    ap.add_argument("--brand", required=True)
    ap.add_argument("--brand-name")
    ap.add_argument("--site-url", help="the brand's own domain, skipped as not press")
    ap.add_argument("--query")
    ap.add_argument("--out", help="brain root to write <brand>/raw/press/ under; default app/brain")
    ap.add_argument("--fixture", help="read a saved search.html instead of the network")
    ap.add_argument("--save-fixture", help="save the live search page here for reuse offline")
    ap.add_argument("--date", help="capture date YYYY-MM-DD, default today")
    args = ap.parse_args(argv)
    config = {"press": {k: v for k, v in {"brand_name": args.brand_name, "site_url": args.site_url,
                                          "query": args.query}.items() if v}}
    result = run(args.brand, config, root=args.out, captured_at=args.date, fixture=args.fixture,
                save_fixture=args.save_fixture)
    print(json.dumps(result, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
