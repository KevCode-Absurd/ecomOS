"""Start a new brain: the intake that writes a brand folder from what the founder types, and an offline dry run of
the onboarding lanes.

`skeleton` creates `<root>/<slug>/` with what a second brand needs before any source connects: identity records for
the name, the store url, the category and the market as approved founder records; the Apify config the onboarding
runner starts with (nothing confirmed); an empty documents manifest; the opening questions from the keeper (at most
5, ranked by weight times rooms unblocked, none of them answerable by a connected source yet); and BRAIN.md from the
router. The screen then opens on `?brand=<slug>` with every block honest about what is missing. Nothing is crawled and
nothing is paid: the intake pre-fills only from the founder's own words.

`dryrun` runs `app/brain/onboard.py` in mock mode on saved fixtures, free lanes only, into the connectors' mock
folder (never a real brain), and returns each lane's status, records and the estimate a live run would cost. It makes
no network call. Capability BRN-C13 (onboarding ingestion) owns the live run; this screen owns the intake.
"""
from __future__ import annotations

import datetime as dt
import importlib.util
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BRAIN_DIR = HERE.parents[1] / "brain"
if str(BRAIN_DIR) not in sys.path:
    sys.path.insert(0, str(BRAIN_DIR))
import keeper  # noqa: E402
import router  # noqa: E402
from store import SECTIONS, Brain  # noqa: E402

_ospec = importlib.util.spec_from_file_location("brain_onboard", BRAIN_DIR / "onboard.py")
onboard = importlib.util.module_from_spec(_ospec)
_ospec.loader.exec_module(onboard)

SAFE_SLUG = re.compile(r"^[a-z0-9][a-z0-9_-]{1,39}$")
MARKETS = ("US", "UK", "EU", "CA", "AU", "IN", "other")
LANE_TEXT = {"site": "crawl the store: products, prices, policies, claims, scripts", "stack": "read the stack from the store's html", "adlib_pages": "propose Ad Library pages (own and competitors) for you to confirm",
             "adlibrary": "pull the confirmed pages from the Ad Library (page id only, never keyword)", "amazon_discover": "find the brand's ASINs from site links and the store page, search capped at $1",
             "amazon_reviews": "pull reviews on the found ASINs, 5 star and 1 star first", "reddit_plan": "propose subreddits and searches for you to confirm", "reddit": "pull the confirmed subreddits (never quoted as testimonials, no usernames)",
             "press": "one web search for press", "jobs": "the careers page and one job search", "merge": "merge every lane into records with the site as default", "ladders": "build the objection ladders from the language bank",
             "router": "write BRAIN.md", "calibrate": "the brand's own calibration, when it has one", "questions": "the 5 opening questions"}


def brains(root: Path) -> list[dict]:
    out = []
    for d in sorted(p for p in Path(root).iterdir() if p.is_dir() and not p.name.startswith(".")):
        if not (d / "BRAIN.md").exists() and not any((d / f"{sec}.json").exists() for sec in SECTIONS):
            continue  # a folder of fixtures or code is not a brain
        try:
            b = Brain(d.name, root)
            n = len(b.records())
        except Exception:  # noqa: BLE001
            n = None
        out.append({"slug": d.name, "records": n, "router": (d / "BRAIN.md").exists()})
    return out


def lanes() -> list[dict]:
    return [{"step": s, "kind": k, "folder": f, "what": LANE_TEXT.get(s, s)} for s, k, f in onboard.LANES]


def _rec(slug: str, field: str, value, text: str, today: str, visibility: str = "public") -> dict:
    return {"id": f"{slug}.identity.{field}", "brand": slug, "section": "identity", "field": field, "value": value, "text": text,
            "tier": "approved", "confidence": 1.0, "visibility": visibility, "source": {"type": "founder", "ref": "05-brand-brain new brain intake", "captured_at": today}}


def skeleton(root: Path, body: dict, today: dt.date) -> dict | tuple[int, dict]:
    slug = str(body.get("slug") or "").strip().lower()
    name = str(body.get("name") or "").strip()[:80]
    url = str(body.get("url") or "").strip()[:200]
    category = str(body.get("category") or "").strip()[:120]
    market = str(body.get("market") or "US").strip().upper()[:8] or "US"
    if not SAFE_SLUG.match(slug):
        return 400, {"error": "slug must be lowercase letters, digits, - or _, 2 to 40 characters"}
    if not name or not url:
        return 400, {"error": "name and url are required"}
    if "://" not in url:
        url = "https://" + url
    if not re.match(r"https?://[a-z0-9.-]+\.[a-z]{2,}", url, re.I):
        return 400, {"error": "url must be a store address like https://example.com"}
    if market not in MARKETS:
        return 400, {"error": "market must be one of " + ", ".join(MARKETS)}
    d = Path(root) / slug
    if d.exists():
        return 409, {"error": "a brain folder with that slug exists", "slug": slug}
    t = today.isoformat()
    d.mkdir(parents=True)
    (d / "documents").mkdir()
    (d / "documents" / "manifest.json").write_text("[]\n", encoding="utf-8")
    (d / "config").mkdir()
    (d / "config" / "apify.json").write_text(json.dumps(onboard.default_config(slug, name, url), indent=1) + "\n", encoding="utf-8")
    recs = [_rec(slug, "name", name, f"{name} is the brand name as customers write it.", t),
            _rec(slug, "site_url", url, f"The store is at {url}.", t)]
    if category:
        recs.append(_rec(slug, "category", category, f"{name} sells {category}.", t))
    recs.append(_rec(slug, "market", market, f"{name} sells in the {market} market" + ("; dollars, US holidays, US marketplaces and carriers by default." if market == "US" else "; market-only fields stay null until the data layer sets them."), t))
    brain = Brain(slug, root, today)
    errs = []
    for r in recs:
        errs += brain.put(r)
    if errs:
        return 400, {"error": "; ".join(errs)}
    asks = keeper.ask(brain, n=5)
    qrecs = [onboard.question_record(slug, a, t) for a in asks]
    (d / "open_questions.json").write_text(json.dumps(qrecs, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    router.write(slug, root, today)
    written = {sec: len(brain.records(sec)) for sec in SECTIONS if brain.records(sec)}
    return {"ok": True, "slug": slug, "name": name, "url": url, "market": market, "folder": str(d.relative_to(root.parent)) if str(d).startswith(str(root.parent)) else str(d),
            "records": sum(written.values()), "sections": written, "questions": [{"id": q.get("field"), "question": (q.get("value") or {}).get("question") or q.get("text"), "rooms": (q.get("value") or {}).get("rooms")} for q in qrecs],
            "files": ["BRAIN.md", "identity.json", "open_questions.json", "documents/manifest.json", "config/apify.json"],
            "next": f"Open the screen with ?brand={slug}: every block reads unavailable until a source connects or you answer. Connect the store first; the 5 questions shrink as sources connect."}


def dryrun(body: dict, out_root: Path, today: dt.date) -> dict | tuple[int, dict]:
    slug = str(body.get("slug") or "").strip().lower()
    name = str(body.get("name") or "").strip()[:80] or slug.replace("-", " ").title()
    url = str(body.get("url") or "").strip()[:200]
    if not SAFE_SLUG.match(slug):
        return 400, {"error": "slug must be lowercase letters, digits, - or _, 2 to 40 characters"}
    if not url:
        return 400, {"error": "url is required"}
    lines: list[str] = []
    try:
        r = onboard.Runner(slug, url, name, mode="mock", fixtures=True, free_only=True, out=out_root, brain_root=BRAIN_DIR, today=today.isoformat(), echo=lambda *a, **k: lines.append(" ".join(str(x) for x in a)))
        s = r.run(compare=False)
    except (ValueError, OSError) as e:
        return 400, {"error": f"dry run failed: {e}"}
    st = onboard.status(slug, out_root)
    return {"ok": True, "slug": slug, "mode": "mock, fixtures, free lanes only; no network call, nothing paid", "root": st["root"], "lanes": st["lanes"], "progress": st["progress"], "records": st["records"],
            "cost_usd": st["cost_usd"], "estimate_usd": st["estimate_usd"], "committed_usd": s.get("committed_usd"), "max_usd": s.get("max_usd"), "questions": st["questions"],
            "log": lines[-30:], "note": "A dry run on saved fixtures: it shows the lanes, their order and what a live run would estimate. Records here never land in a real brain. A live run needs the founder to confirm pages and subreddits, and stays under the Apify caps."}
