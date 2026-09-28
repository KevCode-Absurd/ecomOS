"""Landing page tracking for the top threats: which of their pages to watch, what to diff, and what we know now.

Top threats: the pages with a threat verdict, highest points first, TOP (3). For each, the watch list is
built from public links in the brain (the price feed url's site, its products feed, the Ad Library page)
and the landing domains seen in an ad-level snapshot when one exists. What the agent diffs on each visit:
the hero headline, the offer banner, the guarantee line, price per pair on the best sellers, and new
collections. A page with no site capture reads "not tracked yet", never a blank. The crawl is a public read
by the site crawler (BRN-C01, agent does it), dated, one visit a week.

Rule COMP-R26: a top threat with no landing page capture becomes a "start tracking" research note (agent).
"""
from __future__ import annotations

import re

TOP = 3
WATCH = ["hero headline", "offer banner", "guarantee line", "price per pair on best sellers", "new collections"]


def _site(url: str | None) -> str | None:
    m = re.match(r"https?://(?:www\.)?([^/]+)", str(url or ""))
    return m.group(1) if m else None


def build(m: dict, snapshot: dict | None, captures: dict | None = None) -> dict:
    threats = [p for p in m["pages"] if (p.get("verdict") or {}).get("text") == "Threat"]
    threats.sort(key=lambda p: (-(p["verdict"]["points"]), -(p["active_ads"] or 0), p["name"]))
    comps = {c["name"]: c for c in m["competitors"]}
    rows = []
    for p in threats[:TOP]:
        c = next((v for k, v in comps.items() if k.lower()[:8] == p["name"].lower()[:8]), {})
        site = _site(c.get("price_ref"))
        urls = []
        if site:
            urls += [f"https://{site}/", f"https://{site}/products.json"]
        if p.get("ad_library_url"):
            urls.append(p["ad_library_url"])
        domains = sorted({r["link_domain"] for r in (snapshot or {}).get("ads") or []
                          if r.get("page_id") == p["page_id"] and r.get("link_domain")})
        cap = (captures or {}).get(p["key"])
        rows.append({"key": p["key"], "name": p["name"], "points": p["verdict"]["points"], "reason": p["verdict"]["short"],
                     "site": site, "urls": urls, "ad_domains": domains, "watch": WATCH,
                     "last_capture": cap.get("captured_at") if cap else None, "tracked": bool(cap)})
    return {"rows": rows, "top": TOP, "watch": WATCH,
            "rule": f"The top {TOP} threats by points. The agent visits each watch url once a week (public read) and diffs "
                    "the listed elements. No capture reads not tracked yet."}


def plan_text(rows: list[dict]) -> str:
    lines = ["Landing page tracking plan (weekly, public read, dated)."]
    for r in rows:
        lines.append(f"{r['name']}: " + (", ".join(r["urls"]) if r["urls"] else "no url in the brain; find the site first") + ".")
    lines += ["Diff on each visit: " + ", ".join(WATCH) + ".",
              "Alert when a headline, offer or guarantee changes, or a best seller's price per pair moves 15 percent.",
              "Keep text only as a 140-character quote with the date. Never copy their pages."]
    return "\n".join(lines)
