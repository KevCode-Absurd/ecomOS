"""Jobs extractor: the brand's careers page plus one public job board search, into team and operations.

Usage:
  python3 -m app.brain.extract.jobs --brand bombas --brand-name Bombas --site-url https://bombas.com
  python3 -m app.brain.extract.jobs --brand bombas --brand-name Bombas \
      --fixture app/brain/extract/fixtures/jobs/bombas --out /tmp/brain

Two fetches: the brand's own careers page (default path /careers, overridable), then a
LinkedIn public job search filtered to postings whose listed company matches the brand
name. Open roles become team records (role, location, posted date); a role whose title
names a distribution, warehouse, fulfilment or logistics function also becomes an
operations record, and a careers page that names its hiring tool or a warehouse does too.
Tier reported, source url and a date on every record.

Polite by design: two requests total, a descriptive user agent, public pages only, no
credentials, no login. A blocked or non-200 careers page is logged and skipped, not
treated as a failure: many careers pages sit behind a bot check and that is expected.
--fixture DIR reads saved careers.html and jobs.html instead of the network. --save-fixture
DIR saves both live responses for reuse offline. No third-party packages.
"""
from __future__ import annotations

import argparse
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

USER_AGENT = "ecomOS-jobs-extractor/0.1 (public brand onboarding crawl; 2 requests per run)"
JOB_BOARD_URL = "https://www.linkedin.com/jobs/search"
MAX_TEXT = 300
MAX_JOBS = 25
EM_DASH = "—"

ATS_TOOLS = ["greenhouse", "lever", "workday", "icims", "smartrecruiters", "ashby", "breezy hr", "jobvite"]
OPS_MENTIONS = ["warehouse", "distribution center", "distribution centre", "fulfillment center",
                "fulfillment centre", "logistics hub"]
OPS_TITLE_KW = ["distribution", "warehouse", "fulfillment", "logistics", "supply chain", "operations"]


def clean(s: str) -> str:
    s = html.unescape(s or "").replace(EM_DASH, ", ")
    return re.sub(r"\s+", " ", s).strip()


def cap(s: str, n: int = MAX_TEXT) -> str:
    s = clean(s)
    return s if len(s) <= n else s[: n - 3].rstrip() + "..."


def strip_tags(s: str) -> str:
    return clean(re.sub(r"<[^>]+>", " ", s or ""))


def slug(s: str, n: int = 50) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(s).lower()).strip("_")[:n] or "x"


def has(text: str, terms) -> bool:
    t = text.lower()
    return any(term in t for term in terms)


def context(text: str, idx: int, kw_len: int, before: int = 40, after: int = 110) -> str:
    lo, hi = max(0, idx - before), min(len(text), idx + kw_len + after)
    return cap(text[lo:hi], 200)


def record(brand: str, section: str, field: str, rid: str, value: dict, text: str, url: str, date: str | None,
          day: str) -> dict:
    return {"id": f"{brand}.{section}.{rid}", "brand": brand, "section": section, "field": field,
            "value": value, "text": cap(text),
            "source": {"type": "press", "ref": url, "captured_at": date or day},
            "tier": "reported", "visibility": "public"}


def _fetch(url: str) -> tuple[int, str]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""


def _page(url: str, name: str, *, fixture_dir, save_dir, day) -> tuple[str, dict]:
    """One fetch (or fixture read): page text and its sources.json entry. Never raises."""
    if fixture_dir:
        path = Path(fixture_dir) / name
        if not path.exists():
            return "", {"url": url, "date": day, "status": -1, "note": "fixture missing; not used as evidence"}
        return path.read_text(encoding="utf-8"), {"url": url, "date": day, "status": 200, "note": "fixture, not fetched live"}
    try:
        status, raw = _fetch(url)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return "", {"url": url, "date": day, "status": -1, "note": f"fetch failed: {type(exc).__name__}; not used as evidence"}
    entry = {"url": url, "date": day, "status": status}
    if status != 200:
        entry["note"] = f"HTTP {status}; not used as evidence (common on a bot-checked careers page)"
        return "", entry
    if save_dir:
        out = Path(save_dir)
        out.mkdir(parents=True, exist_ok=True)
        (out / name).write_text(raw, encoding="utf-8")
    return raw, entry


def careers_records(brand: str, brand_name: str, raw_html: str, url: str, day: str) -> list[dict]:
    text = strip_tags(raw_html)
    low = text.lower()
    out = []
    for tool in ATS_TOOLS:
        i = low.find(tool)
        if i != -1:
            out.append(record(brand, "operations", "signal", f"careers_ats_{slug(tool)}",
                              {"tool": tool.title(), "context": context(text, i, len(tool))},
                              f"The {brand_name} careers page names {tool.title()} as its hiring tool.",
                              url, day, day))
            break
    for kw in OPS_MENTIONS:
        i = low.find(kw)
        if i != -1:
            out.append(record(brand, "operations", "signal", f"careers_{slug(kw)}",
                              {"mention": kw, "context": context(text, i, len(kw))},
                              f"The {brand_name} careers page mentions a {kw}.", url, day, day))
            break
    return out


def parse_linkedin(raw_html: str, brand_name: str) -> list[dict]:
    wanted = slug(brand_name)
    out, seen = [], set()
    for block in raw_html.split("base-search-card base-search-card--link job-search-card")[1:]:
        mt = re.search(r'base-search-card__title">\s*(.*?)\s*</h3>', block, re.S)
        mc = re.search(r'base-search-card__subtitle">.*?>\s*(.*?)\s*</a>', block, re.S)
        ml = re.search(r'job-search-card__location">\s*(.*?)\s*</span>', block, re.S)
        md = re.search(r'<time[^>]*datetime="([^"]+)"', block)
        mu = re.search(r'href="([^"?]+)', block)
        if not (mt and mc and mu):
            continue
        company = strip_tags(mc.group(1))
        if slug(company) != wanted:
            continue
        title, url = strip_tags(mt.group(1)), mu.group(1)
        if url in seen:
            continue
        seen.add(url)
        out.append({"title": title, "location": strip_tags(ml.group(1)) if ml else "",
                   "date": md.group(1) if md else None, "url": url})
        if len(out) >= MAX_JOBS:
            break
    return out


def job_board_records(brand: str, brand_name: str, jobs: list[dict], day: str) -> list[dict]:
    out = []
    for j in jobs:
        rid = f"{slug(j['title'], 35)}_{slug(j['location'], 20)}"
        where = f" in {j['location']}" if j["location"] else ""
        value = {"role": j["title"], "location": j["location"], "date": j["date"], "url": j["url"],
                 "board": "linkedin_jobs"}
        out.append(record(brand, "team", "open_role", rid, value,
                          f"{brand_name} is hiring a {j['title']}{where}.", j["url"], j["date"], day))
        if has(j["title"], OPS_TITLE_KW):
            out.append(record(brand, "operations", "signal", f"role_{rid}",
                              {"function": "distribution_or_logistics", "role": j["title"], "location": j["location"],
                               "url": j["url"]},
                              f"{brand_name} hiring signal for its distribution or logistics function: "
                              f"{j['title']}{where}.", j["url"], j["date"], day))
    return out


def run(brand: str, config: dict, *, root=None, captured_at: str | None = None,
        fixture: Path | str | None = None, save_fixture: Path | str | None = None) -> dict:
    cfg = config.get("jobs", {})
    brand_name = cfg.get("brand_name") or brand
    day = captured_at or dt.date.today().isoformat()
    site_url = (cfg.get("site_url") or "").rstrip("/")
    careers_path = cfg.get("careers_path", "/careers")
    careers_url = urllib.parse.urljoin(site_url + "/", careers_path.lstrip("/")) if site_url else ""
    board_url = f"{JOB_BOARD_URL}?{urllib.parse.urlencode({'keywords': brand_name})}"

    sources = []
    records = []
    if careers_url:
        careers_html, src = _page(careers_url, "careers.html", fixture_dir=fixture, save_dir=save_fixture, day=day)
        sources.append(src)
        if careers_html:
            records += careers_records(brand, brand_name, careers_html, careers_url, day)

    board_html, src = _page(board_url, "jobs.html", fixture_dir=fixture, save_dir=save_fixture, day=day)
    sources.append(src)
    jobs = parse_linkedin(board_html, brand_name) if board_html else []
    records += job_board_records(brand, brand_name, jobs, day)

    folder = (Path(root) if root else ROOT / "app" / "brain") / brand / "raw" / "jobs"
    folder.mkdir(parents=True, exist_ok=True)
    for old in folder.glob("*.json"):
        old.unlink()
    by_section: dict[str, list] = {}
    for rec in records:
        by_section.setdefault(rec["section"], []).append(rec)
    for section, recs in by_section.items():
        (folder / f"{section}.json").write_text(json.dumps(recs, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    (folder / "sources.json").write_text(json.dumps(sources, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return {"folder": str(folder), "jobs_matched": len(jobs), "records": len(records)}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="The brand's careers page plus one public job board search.")
    ap.add_argument("--brand", required=True)
    ap.add_argument("--brand-name")
    ap.add_argument("--site-url", help="the brand's own site, for its careers page")
    ap.add_argument("--careers-path", default="/careers")
    ap.add_argument("--out", help="brain root to write <brand>/raw/jobs/ under; default app/brain")
    ap.add_argument("--fixture", help="dir with saved careers.html and jobs.html instead of the network")
    ap.add_argument("--save-fixture", help="save both live responses here for reuse offline")
    ap.add_argument("--date", help="capture date YYYY-MM-DD, default today")
    args = ap.parse_args(argv)
    config = {"jobs": {k: v for k, v in {"brand_name": args.brand_name, "site_url": args.site_url,
                                         "careers_path": args.careers_path}.items() if v}}
    result = run(args.brand, config, root=args.out, captured_at=args.date, fixture=args.fixture,
                save_fixture=args.save_fixture)
    print(json.dumps(result, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
