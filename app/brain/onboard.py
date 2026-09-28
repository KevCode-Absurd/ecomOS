"""Onboarding runner: a store url in, a brand brain out, then at most 5 questions.

python3 -m app.brain.onboard --brand <slug> --url <store url> --name "<brand name>"
        [--mode mock|live] [--max-usd 10] [--fixtures] [--out DIR] [--date YYYY-MM-DD] [--free-only]

Steps, in order, each writing its raw folder and one line to <brand>/onboard.log.jsonl
(step, lane, started, finished, records, cost_usd, estimate_usd, status, note):

  site             site.py crawl                       raw/a-site            free
  stack            stack.py on the store's html         raw/a-site/stack.json free
  adlib_pages      own page id, competitor proposals   config/apify.json     free
  adlibrary        Ad Library pull, confirmed pages    raw/adlibrary-apify   paid
  amazon_discover  site links, store page, capped search raw/amazon-discover  free, search capped at $1
  amazon_reviews   review lane on the discovered ASINs  raw/amazon-apify      paid
  reddit_plan      proposed subreddits and searches    config/apify.json     free
  reddit           Reddit pull, confirmed subreddits   raw/reddit-apify      paid
  press            one web search                      raw/press             free
  jobs             careers page and one job search     raw/jobs              free

then merge.py, ladders.py, router.py (BRAIN.md), the brand's calibrate.py if it exists, and
keeper.ask for at most 5 questions, written to <brand>/open_questions.json and printed.

Paid steps print the estimate from app.connectors.apify.estimate_usd and the budget left before
they start, and are refused when the run would pass --max-usd. A refused or failed step is logged
and the run goes on: free steps never stop on a paid step. In mock mode the paid lanes use the
connector's fixtures and cost nothing; the estimate still counts against --max-usd so the cap
behaves the same in both modes.

--fixtures reads every free lane from app/brain/extract/fixtures/ and makes no network call. For a
brand whose brain already holds a saved paid pull (raw/<lane>-apify), mock mode replays that pull.
Mock runs write under app/connectors/.mock/onboard/ so fixture records never land in a real brain;
lanes this runner does not own (founder answers, documents, hand research) are copied from the real
brain first, so a re-onboard keeps them. --compare reports the record count per section against
the real brain (the dry run check: within 5 percent for the sections the run's lanes wrote).
"""
from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import json
import re
import shutil
import sys
import time
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
for p in (str(ROOT), str(HERE)):
    if p not in sys.path:
        sys.path.insert(0, p)

from app.connectors import apify  # noqa: E402

FIXTURES = HERE / "extract" / "fixtures"
MOCK_ROOT = apify.MOCK_OUT / "onboard"
LOG_NAME = "onboard.log.jsonl"
DEFAULT_MAX_USD = 10.0
TOLERANCE = 0.05
MAX_QUESTIONS = 5
SAFE_BRAND = re.compile(r"^[a-z0-9_-]{2,40}$")

# Raw folders this runner writes. Every other raw folder belongs to another lane and is kept.
OWNED = {"a-site", "adlibrary-apify", "amazon-discover", "amazon-apify", "reddit-apify", "press", "jobs"}
PAID = {"adlibrary": "adlibrary-apify", "amazon_reviews": "amazon-apify", "reddit": "reddit-apify"}
LANES = [
    ("site", "free", "a-site"),
    ("stack", "free", "a-site"),
    ("adlib_pages", "free", "config"),
    ("adlibrary", "paid", "adlibrary-apify"),
    ("amazon_discover", "capped", "amazon-discover"),
    ("amazon_reviews", "paid", "amazon-apify"),
    ("reddit_plan", "free", "config"),
    ("reddit", "paid", "reddit-apify"),
    ("press", "free", "press"),
    ("jobs", "free", "jobs"),
    ("merge", "build", None),
    ("ladders", "build", None),
    ("router", "build", None),
    ("calibrate", "build", None),
    ("questions", "build", None),
]
STEP_NAMES = [s for s, _, _ in LANES]
# Rebuilt from the whole brain on every run, so they are reported but never part of the check.
DERIVED = {"open_questions", "objection_ladders", "assumptions", "freshness"}


def default_config(brand: str, name: str, url: str) -> dict:
    """The Apify config a new brand starts with. Nothing is confirmed: pages and subreddits wait for the founder."""
    return {
        "version": dt.date.today().isoformat(),
        "note": "Written by onboarding. Pages and subreddits run only after the founder confirms them.",
        "budget": {"max_usd_per_run": 4.0, "max_usd_per_week": 30.0, "ledger": "intelligence/budget.py"},
        "amazon_reviews": {"actor": "axesso_data~amazon-reviews-scraper", "listing_actor": None, "domain_code": "com",
                           "asins": [], "asins_backlog": [],
                           "discovery": {"search_actor": "axesso_data~amazon-product-search-scraper",
                                         "max_results": 50, "max_usd": 1.0, "keep_top": 10, "enough": 10,
                                         "store_url": None},
                           "stars_first": [5, 1], "max_reviews_per_asin_per_star": 100, "max_pages": 10},
        "meta_ad_library": {"actor": "curious_coder~facebook-ads-library-scraper", "country": "US",
                            "active_status": "active", "pages": [], "limit_per_source": 100},
        "reddit": {"actor": "trudax~reddit-scraper-lite", "brand_name": name, "searches": [], "subreddits": [],
                   "max_items": 500, "max_comments_per_post": 8, "sort": "top", "time": "year"},
        "press": {"brand_name": name, "site_url": url},
        "jobs": {"brand_name": name, "site_url": url},
    }


# ---------------------------------------------------------------- files

def _read(path: Path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def _dump(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def count_folder(folder: Path) -> int:
    n = 0
    for f in sorted(Path(folder).glob("*.json")):
        if f.stem != "sources":
            data = _read(f, [])
            n += len(data) if isinstance(data, list) else 0
    return n


def section_counts(brand_dir: Path) -> dict[str, int]:
    """Records per merged section file, as the brain screen counts them."""
    skip = {"sources", "freshness"}
    out = {}
    for f in sorted(Path(brand_dir).glob("*.json")):
        if f.stem in skip:
            continue
        data = _read(f, [])
        if isinstance(data, list):
            out[f.stem] = len(data)
    return out


def raw_sections(brand_dir: Path, lanes) -> set[str]:
    out = set()
    for lane in lanes:
        for f in (Path(brand_dir) / "raw" / lane).glob("*.json"):
            if f.stem != "sources" and _read(f, []):
                out.add(f.stem)
    return out


def read_log(brand_dir: Path) -> list[dict]:
    path = Path(brand_dir) / LOG_NAME
    if not path.is_file():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


# ---------------------------------------------------------------- runner

class Runner:
    def __init__(self, brand: str, url: str, name: str, *, mode: str = "mock", max_usd: float = DEFAULT_MAX_USD,
                 fixtures: bool = False, out: Path | None = None, brain_root: Path | None = None,
                 today: str | None = None, free_only: bool = False, echo=print):
        if not SAFE_BRAND.match(brand):
            raise ValueError("brand must be a lowercase slug")
        if mode not in ("mock", "live"):
            raise ValueError("mode must be mock or live")
        if fixtures and mode == "live":
            raise ValueError("--fixtures runs offline; use --mode mock")
        self.brand, self.name, self.mode, self.fixtures = brand, name, mode, fixtures
        self.url = (url if "://" in url else "https://" + url).rstrip("/")
        self.max_usd = float(max_usd)
        self.free_only = free_only
        self.brain_root = Path(brain_root or HERE)
        self.root = Path(out) if out else (MOCK_ROOT if mode == "mock" else self.brain_root)
        if mode == "mock" and self.root.resolve() == self.brain_root.resolve():
            raise ValueError("mock runs write under app/connectors/.mock, never into a real brain")
        self.dir = self.root / brand
        self.real_dir = self.brain_root / brand
        self.today = today or dt.date.today().isoformat()
        self.committed = 0.0   # estimates of paid steps that ran; counts against --max-usd in both modes
        self.spent = 0.0       # real dollars (live only)
        self.echo = echo
        self.results: dict[str, dict] = {}
        self.questions: list[dict] = []

    # ---- paths and config
    @property
    def config_path(self) -> Path:
        return self.dir / "config" / "apify.json"

    def config(self) -> dict:
        cfg = _read(self.config_path, None)
        if cfg is None:
            cfg = default_config(self.brand, self.name, self.url)
        cfg.setdefault("press", {}).update(brand_name=self.name, site_url=self.url)
        cfg.setdefault("jobs", {}).update(brand_name=self.name, site_url=self.url)
        cfg.setdefault("reddit", {}).setdefault("brand_name", self.name)
        return cfg

    def save_config(self, cfg: dict) -> None:
        _dump(self.config_path, cfg)

    def fixture(self, kind: str) -> Path | None:
        d = FIXTURES / kind / self.brand
        return d if d.is_dir() else None

    def site_url(self) -> str:
        """The crawl url: a site fixture keeps the host it was saved from (shop.bombas.com for Bombas)."""
        if self.fixtures:
            base = (_read((self.fixture("site") or Path("-")) / "index.json", {}) or {}).get("base")
            if base:
                return base.rstrip("/")
        return self.url

    def fixture_robots(self) -> list[dict]:
        """robots.txt from the saved crawl, so the stack detector sees what a live run would."""
        fx = self.fixture("site")
        index = (_read(fx / "index.json", {}) or {}) if fx else {}
        for url, meta in (index.get("responses") or {}).items():
            if meta.get("kind") == "robots" and (fx / meta["file"]).is_file():
                return [{"url": url, "text": (fx / meta["file"]).read_text(encoding="utf-8", errors="replace"),
                         "headers": {}, "cookies": []}]
        return []

    def left(self) -> float:
        return round(self.max_usd - self.committed, 2)

    # ---- log
    def log(self, row: dict) -> None:
        with (self.dir / LOG_NAME).open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    def step(self, name: str, fn) -> dict:
        kind, folder = next((k, f) for s, k, f in LANES if s == name)
        started = dt.datetime.now().isoformat(timespec="seconds")
        t0 = time.monotonic()
        row = {"step": name, "kind": kind, "folder": folder, "started": started, "mode": self.mode,
               "records": 0, "cost_usd": 0.0, "estimate_usd": None, "status": "ok", "note": None}
        try:
            out = fn() or {}
            row.update({k: v for k, v in out.items() if k in row or k in ("detail",)})
        except Exception as exc:  # a step failing is logged; the run goes on
            row.update(status="error", note=f"{type(exc).__name__}: {str(exc)[:300]}")
            if self.echo:
                traceback.print_exc(limit=2, file=sys.stderr)
        row["finished"] = dt.datetime.now().isoformat(timespec="seconds")
        row["seconds"] = round(time.monotonic() - t0, 2)
        self.results[name] = row
        self.log(row)
        if self.echo:
            est = f" est ${row['estimate_usd']:.2f}" if row.get("estimate_usd") is not None else ""
            self.echo(f"{name:16} {row['status']:9} {row['records']:5} records  ${row['cost_usd']:.2f}{est}"
                      + (f"  {row['note']}" if row["note"] else ""))
        return row

    # ---- paid gate
    def gate(self, lane: str, actor: str, max_items: int) -> tuple[float | None, str | None]:
        """Estimate, print it with the budget left, and refuse when it would pass --max-usd."""
        est = apify.estimate_usd(actor, max_items)
        if self.echo:
            self.echo(f"  {lane}: {actor}, up to {max_items} items, estimate ${est:.2f}; "
                      f"budget left ${self.left():.2f} of ${self.max_usd:.2f} ({self.mode})")
        if self.free_only:
            return est, "skipped: free steps only"
        if est > self.left():
            return est, f"refused: estimate ${est:.2f} is over the ${self.left():.2f} left of --max-usd ${self.max_usd:.2f}"
        return est, None

    def client(self, cfg: dict):
        return apify.ApifyClient(mode=self.mode, brand=self.brand, budget=cfg.get("budget"),
                                 today=dt.date.fromisoformat(self.today))

    def replay(self, folder: str) -> int | None:
        """Fixture runs replay the brand's saved paid pull, if the real brain has one."""
        src = self.real_dir / "raw" / folder
        if not (self.fixtures and src.is_dir() and src.resolve() != (self.dir / "raw" / folder).resolve()):
            return None
        dst = self.dir / "raw" / folder
        shutil.rmtree(dst, ignore_errors=True)
        shutil.copytree(src, dst)
        return count_folder(dst)

    def paid(self, lane: str, actor: str, max_items: int, run) -> dict:
        folder = PAID[lane]
        est, refused = self.gate(lane, actor, max_items)
        if refused:
            return {"status": "refused" if refused.startswith("refused") else "skipped", "estimate_usd": est,
                    "note": refused}
        self.committed += est
        if self.mode == "mock":
            n = self.replay(folder)
            if n is not None:
                return {"status": "mock", "estimate_usd": est, "records": n,
                        "note": f"replayed the saved pull in app/brain/{self.brand}/raw/{folder}"}
        res = run()
        cost = 0.0
        if self.mode == "live":
            cost = est  # the ledger settles the real figure; the log keeps the reservation
            self.spent += cost
        return {"status": "mock" if self.mode == "mock" else "ok", "estimate_usd": est,
                "records": res.get("records", 0), "cost_usd": cost,
                "note": "connector fixtures, invented" if self.mode == "mock" else f"run {res.get('run_id')}"}

    # ---- lanes
    def s_site(self) -> dict:
        from app.brain.extract import site
        fx = self.fixture("site") if self.fixtures else None
        if self.fixtures and not fx:
            return {"status": "skipped", "note": f"no site fixture for {self.brand}"}
        res = site.run(self.brand, self.site_url(), self.root, fx)
        return {"records": sum(len(v) for k, v in res.items() if k != "sources"),
                "note": f"fixture of {self.site_url()}" if fx else f"{len(res.get('sources', []))} urls read"}

    def s_stack(self) -> dict:
        from app.brain.extract import stack
        if self.fixtures:
            fx = self.fixture("stack") or self.fixture("site")
            if not fx:
                return {"status": "skipped", "note": f"no stack fixture for {self.brand}"}
            docs = stack.read_pages(fx, self.site_url())
            docs += self.fixture_robots()
        else:
            docs = stack.fetch_live(self.url)
        recs = stack.run(self.brand, docs, self.today)
        stack.write_stack(self.root, self.brand, recs, [{"url": d["url"], "date": self.today} for d in docs])
        return {"records": len(recs), "note": "fixture" if self.fixtures else None}

    def s_adlib_pages(self) -> dict:
        from app.brain.extract import adlib_pages
        self.save_config(self.config())
        site_dir = self.fixture("site") if self.fixtures else None
        live = not self.fixtures and self.mode == "live"
        site_arg = str(site_dir) if site_dir else (self.url if live else None)
        res = adlib_pages.run(self.brand, self.name, site=site_arg, root=self.root, config_path=self.config_path,
                              live=live)
        own = res["own"] or {}
        return {"records": res["proposed"],
                "note": f"own page {own.get('page_id') or 'unresolved'}; {res['proposed']} proposed, "
                        f"{res['pages']} confirmed"}

    def s_adlibrary(self) -> dict:
        from app.brain.extract import apify_adlibrary
        cfg = self.config()
        mal = cfg.get("meta_ad_library", {})
        pages = mal.get("pages", [])
        if not pages:
            return {"status": "waiting", "note": "no confirmed pages: the founder confirms competitors first"}
        n_urls = len(pages) + len(mal.get("search_terms", []))
        max_items = mal.get("limit_per_source", 100) * max(n_urls, 1)
        return self.paid("adlibrary", mal["actor"], max_items,
                         lambda: apify_adlibrary.run(self.brand, cfg, client=self.client(cfg), root=self.root,
                                                     captured_at=self.today))

    def s_amazon_discover(self) -> dict:
        from app.brain.extract import amazon_discover as ad
        cfg = self.config()
        disc = (cfg.get("amazon_reviews") or {}).get("discovery") or {}
        actor = disc.get("search_actor", ad.SEARCH_ACTOR)
        results = min(disc.get("max_results", ad.MAX_RESULTS), ad.MAX_RESULTS)
        est, refused = self.gate("amazon_discover search", actor, results)
        client = None
        fixtures = self.fixture("amazon_discover") or (FIXTURES / "amazon_discover" / "sample")
        if self.mode == "mock" and not refused and not (fixtures / f"{actor}.json").is_file():
            refused = "skipped: no mock output saved for the search actor"
        if refused:
            client = _NoSearch()
        site_arg = self.fixture("site") if self.fixtures else (self.url if self.mode == "live" else None)
        res = ad.run(self.brand, self.name, cfg, mode=self.mode, site=site_arg, out=self.root,
                     max_usd=min(ad.HARD_MAX_USD, max(self.left(), 0.0)), client=client, captured_at=self.today,
                     fixtures=fixtures)
        searched = any(s["step"] == "search_actor" for s in res["steps"]) and not refused
        cost = 0.0
        if searched:
            self.committed += est
            if self.mode == "live":
                cost = est
                self.spent += cost
        how = ", ".join(f"{s['step']} {s.get('found', 0)}" for s in res["steps"])
        note = f"{len(res['asins'])} ASINs kept ({how})"
        if refused and any(s["step"] == "search_actor" for s in res["steps"]):
            note += f"; search {refused}" if refused.startswith("refused") else f"; search {refused[len('skipped: '):]}"
        return {"records": res["records"], "estimate_usd": est, "cost_usd": cost, "note": note,
                "status": "ok" if not searched or self.mode == "live" else "mock"}

    def s_amazon_reviews(self) -> dict:
        from app.brain.extract import apify_amazon
        cfg = self.config()
        ar = cfg.get("amazon_reviews", {})
        asins = ar.get("asins") or []
        if not asins:
            return {"status": "waiting", "note": "no ASINs found; the review lane needs at least one"}
        max_items = ar.get("max_reviews_per_asin_per_star", 100) * len(asins) * len(ar.get("stars_first", [5, 1]))
        return self.paid("amazon_reviews", ar["actor"], max_items,
                         lambda: apify_amazon.run(self.brand, cfg, client=self.client(cfg), root=self.root,
                                                  captured_at=self.today))

    def s_reddit_plan(self) -> dict:
        from app.brain.extract import apify_reddit
        cfg = self.config()
        brain = {s: _values(self.dir, s) for s in ("identity", "products")}
        plan = apify_reddit.plan(self.brand, brain, brand_name=self.name)
        rc = cfg.setdefault("reddit", {})
        rc["proposed_subreddits"] = plan["proposed_subreddits"]
        rc["proposed_searches"] = plan["searches"]
        rc["category_term"] = plan["category_term"]
        rc.setdefault("brand_name", plan["brand_name"])
        self.save_config(cfg)
        return {"records": len(plan["proposed_subreddits"]),
                "note": f"{len(plan['proposed_subreddits'])} subreddits proposed, "
                        f"{len(rc.get('subreddits') or [])} confirmed"}

    def s_reddit(self) -> dict:
        from app.brain.extract import apify_reddit
        cfg = self.config()
        rc = cfg.get("reddit", {})
        if not rc.get("subreddits"):
            return {"status": "waiting", "note": "no confirmed subreddits: the founder confirms the proposals first"}
        return self.paid("reddit", rc["actor"], rc.get("max_items", 500),
                         lambda: apify_reddit.run(self.brand, cfg, client=self.client(cfg), root=self.root,
                                                  captured_at=self.today))

    def s_press(self) -> dict:
        from app.brain.extract import press
        fx = self.fixture("press") if self.fixtures else None
        if self.fixtures and not fx:
            return {"status": "skipped", "note": f"no press fixture for {self.brand}"}
        res = press.run(self.brand, self.config(), root=self.root, captured_at=self.today, fixture=fx)
        return {"records": res["records"], "note": f"{res['results']} search results"}

    def s_jobs(self) -> dict:
        from app.brain.extract import jobs
        fx = self.fixture("jobs") if self.fixtures else None
        if self.fixtures and not fx:
            return {"status": "skipped", "note": f"no jobs fixture for {self.brand}"}
        res = jobs.run(self.brand, self.config(), root=self.root, captured_at=self.today, fixture=fx)
        return {"records": res["records"], "note": f"{res['jobs_matched']} postings matched"}

    # ---- build
    def s_merge(self) -> dict:
        import merge
        (self.dir / "raw").mkdir(parents=True, exist_ok=True)
        res = merge.run(self.brand, self.root, self.today, publish=False)
        return {"records": res["records"], "note": f"{res['raw']} raw, {res['conflicts']} conflicts"}

    def s_ladders(self) -> dict:
        import ladders
        res = ladders.run(self.brand, self.root, self.today, remerge=False, publish=False)
        return {"records": res["ladders"], "note": f"{res['rungs']} rungs, {res['open_questions_added']} open questions"}

    def s_router(self) -> dict:
        import router
        path = router.write(self.brand, self.root, dt.date.fromisoformat(self.today))
        return {"records": 1, "note": str(path.relative_to(self.root))}

    def s_calibrate(self) -> dict:
        import merge
        import store
        path = self.dir / "calibrate.py"
        if not path.exists():
            path = self.real_dir / "calibrate.py"
        if not path.exists():
            return {"status": "skipped", "note": "no calibrate.py for this brand"}
        spec = importlib.util.spec_from_file_location(f"calibrate_{self.brand}_onboard", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        recs = store.Brain(self.brand, self.root, dt.date.fromisoformat(self.today)).records()
        assumptions, questions = mod.build(recs, self.today)
        merge._dump(self.dir / "assumptions.json", assumptions)
        oq = [q for q in _read(self.dir / "open_questions.json", []) if ".open_questions.ladder_" in q.get("id", "")]
        merge._dump(self.dir / "open_questions.json", questions + oq)
        return {"records": len(assumptions), "note": f"{len(questions)} calibration questions"}

    def s_questions(self) -> dict:
        import keeper
        import store
        brain = store.Brain(self.brand, self.root, dt.date.fromisoformat(self.today))
        conns = _read(self.dir / "connections.json", {}) or {}
        choices = conns.get("choices", {})
        connected = sorted(c["source"] for c in choices.values() if c.get("choice") == "connect" and c.get("source"))
        asks = keeper.ask(brain, connected, n=MAX_QUESTIONS)[:MAX_QUESTIONS]
        self.questions = asks
        path = self.dir / "open_questions.json"
        kept = [q for q in _read(path, []) if ".open_questions.keeper_" not in q.get("id", "")]
        recs = [question_record(self.brand, a, self.today) for a in asks]
        _dump(path, kept + recs)
        return {"records": len(asks), "detail": asks}

    # ---- run
    def seed(self) -> list[str]:
        """Copy the lanes this runner does not own, and the config, from the real brain into a mock root."""
        if self.root.resolve() == self.brain_root.resolve() or not (self.real_dir / "raw").is_dir():
            return []
        copied = []
        for src in sorted(p for p in (self.real_dir / "raw").iterdir() if p.is_dir()):
            if src.name in OWNED:
                continue
            dst = self.dir / "raw" / src.name
            shutil.rmtree(dst, ignore_errors=True)
            shutil.copytree(src, dst)
            copied.append(src.name)
        real_cfg = self.real_dir / "config" / "apify.json"
        if real_cfg.is_file() and not self.config_path.exists():
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(real_cfg, self.config_path)
        return copied

    def keep_prior(self) -> dict[str, int]:
        """A re-onboard never drops what the brain had: records an owned lane held before and the fresh
        run did not find go to raw/<lane>-kept/, so merge keeps them and the count says how many."""
        if self.root.resolve() == self.brain_root.resolve():
            return {}
        kept: dict[str, int] = {}
        for lane in sorted(OWNED):
            src, dst = self.real_dir / "raw" / lane, self.dir / "raw" / lane
            out = self.dir / "raw" / f"{lane}-kept"
            shutil.rmtree(out, ignore_errors=True)
            if not src.is_dir() or not dst.is_dir():
                continue
            fresh = {r.get("id") for f in dst.glob("*.json") if f.stem != "sources" for r in _read(f, []) or []}
            for f in sorted(src.glob("*.json")):
                if f.stem == "sources":
                    continue
                missing = [r for r in _read(f, []) or [] if r.get("id") not in fresh]
                if missing:
                    _dump(out / f.name, missing)
                    kept[f.stem] = kept.get(f.stem, 0) + len(missing)
            if out.is_dir():
                _dump(out / "sources.json", [{"lane": f"{lane}-kept", "note": f"records from app/brain/{self.brand}/raw/{lane} "
                                              "the fresh run did not find; kept, not deleted", "accessed": self.today}])
        return kept

    def run(self, compare: bool = False) -> dict:
        self.dir.mkdir(parents=True, exist_ok=True)
        (self.dir / LOG_NAME).write_text("", encoding="utf-8")
        self.log({"step": "start", "brand": self.brand, "url": self.url, "name": self.name, "mode": self.mode,
                  "fixtures": self.fixtures, "max_usd": self.max_usd, "started": dt.datetime.now().isoformat(timespec="seconds"),
                  "root": _rel(self.root)})
        seeded = self.seed()
        if seeded and self.echo:
            self.echo(f"kept prior lanes from the real brain: {', '.join(seeded)}")
        kept = {}
        for name in STEP_NAMES:
            if name == "merge":
                kept = self.keep_prior()
                if kept:
                    self.log({"step": "kept", "records": sum(kept.values()), "sections": kept,
                              "note": "prior records the fresh lanes did not find"})
                    if self.echo:
                        self.echo(f"kept {sum(kept.values())} prior records the fresh lanes did not find: "
                                  + ", ".join(f"{k} {v}" for k, v in kept.items()))
            self.step(name, getattr(self, "s_" + name))
        summary = {"brand": self.brand, "root": _rel(self.root), "mode": self.mode, "fixtures": self.fixtures,
                   "steps": {k: v["status"] for k, v in self.results.items()},
                   "committed_usd": round(self.committed, 2), "cost_usd": round(self.spent, 2),
                   "max_usd": self.max_usd, "seeded": seeded, "kept": kept, "questions": self.questions}
        if compare:
            summary["compare"] = compare_counts(self.dir, self.real_dir, raw_sections(self.dir, OWNED) - DERIVED)
        self.log({"step": "done", "finished": dt.datetime.now().isoformat(timespec="seconds"),
                  "committed_usd": summary["committed_usd"], "cost_usd": summary["cost_usd"],
                  **({"compare_ok": summary["compare"]["ok"]} if compare else {})})
        return summary


class _NoSearch:
    """Stands in for the Apify client when the search step is refused: returns nothing, spends nothing."""
    last_run = {"run_id": None}
    mode = "refused"

    def run(self, *a, **k):
        return []


def _values(brand_dir: Path, section: str) -> dict:
    """{field: value} for a section, from the merged file or, before merge, from raw a-site."""
    out = {}
    for path in (Path(brand_dir) / "raw" / "a-site" / f"{section}.json", Path(brand_dir) / f"{section}.json"):
        for r in _read(path, []) or []:
            if isinstance(r, dict) and r.get("field") and r.get("status", "active") == "active" and "value" in r:
                out[r["field"]] = r["value"]
    return out


def _rel(p: Path) -> str:
    try:
        return str(Path(p).resolve().relative_to(ROOT))
    except ValueError:
        return str(p)


def question_record(brand: str, ask: dict, today: str) -> dict:
    slug = re.sub(r"[^a-z0-9_]+", "_", ask["id"].lower()).strip("_")[:60]
    return {"id": f"{brand}.open_questions.keeper_{slug}", "brand": brand, "section": "open_questions",
            "field": f"keeper_{slug}",
            "value": {"question": ask["text"], "bank_id": ask["id"], "fills": ask["fills"], "rooms": ask["rooms"],
                      "importance": ask["importance"], "kind": ask["kind"], "connect": ask["connect"],
                      "why": ask["why"], "who_can_answer": "the founder", "asked_on": today, "answered_on": None},
            "text": ask["text"], "source": {"type": "agent", "ref": "keeper.ask via onboard", "captured_at": today},
            "visibility": "private"}


def _ids(path: Path) -> set:
    return {r.get("id") for r in _read(path, []) or [] if isinstance(r, dict)}


def compare_counts(brand_dir: Path, real_dir: Path, covered: set[str], tol: float = TOLERANCE) -> dict:
    """Record count per section, run vs the real brain, matched by record id.

    A covered section passes when the run keeps all but at most tol of today's records (lost / real).
    Records the run adds are reported as added, with the plain count difference, and do not fail it."""
    got, want = section_counts(brand_dir), section_counts(real_dir)
    rows, bad = [], []
    for s in sorted(set(got) | set(want)):
        g, w = got.get(s, 0), want.get(s, 0)
        a, b = _ids(real_dir / f"{s}.json"), _ids(brand_dir / f"{s}.json")
        lost, added = len(a - b), len(b - a)
        lost_pct = lost / w if w else 0.0
        inside = lost_pct <= tol + 1e-9
        rows.append({"section": s, "run": g, "real": w, "kept": len(a & b), "lost": lost, "added": added,
                     "lost_pct": round(lost_pct * 100, 1),
                     "diff_pct": round(((g - w) / w if w else (0.0 if not g else 1.0)) * 100, 1),
                     "covered": s in covered, "within": inside})
        if s in covered and not inside:
            bad.append(s)
    return {"ok": not bad, "outside": bad, "tolerance_pct": tol * 100, "rows": rows,
            "covered": sorted(covered), "run_total": sum(got.values()), "real_total": sum(want.values())}


# ---------------------------------------------------------------- status (read by the setup screen)

def status(brand: str, root: Path) -> dict:
    """Progress per lane, records, cost and the questions, from <root>/<brand>/onboard.log.jsonl."""
    brand_dir = Path(root) / brand
    rows = read_log(brand_dir)
    start = next((r for r in rows if r.get("step") == "start"), None)
    done = next((r for r in rows if r.get("step") == "done"), None)
    by_step = {r["step"]: r for r in rows if r.get("step") in STEP_NAMES}
    lanes = []
    for name, kind, folder in LANES:
        r = by_step.get(name)
        lanes.append({"step": name, "kind": kind, "folder": folder,
                      "status": r["status"] if r else ("pending" if start and not done else "not run"),
                      "records": r.get("records", 0) if r else 0, "cost_usd": r.get("cost_usd", 0.0) if r else 0.0,
                      "estimate_usd": r.get("estimate_usd") if r else None, "note": r.get("note") if r else None,
                      "started": r.get("started") if r else None, "finished": r.get("finished") if r else None})
    q = by_step.get("questions") or {}
    questions = q.get("detail") or []
    finished = sum(1 for lane in lanes if lane["started"])
    return {"brand": brand, "root": _rel(Path(root)), "started": bool(start), "running": bool(start) and not done,
            "done": bool(done), "run": start, "lanes": lanes, "progress": {"finished": finished, "total": len(LANES)},
            "records": sum(lane["records"] for lane in lanes if lane["kind"] not in ("build",)),
            "cost_usd": round(sum(lane["cost_usd"] or 0 for lane in lanes), 2),
            "estimate_usd": round(sum(lane["estimate_usd"] or 0 for lane in lanes), 2),
            "questions": questions[:MAX_QUESTIONS]}


# ---------------------------------------------------------------- cli

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--brand", required=True)
    ap.add_argument("--url", required=True, help="the store url, e.g. https://bombas.com")
    ap.add_argument("--name", help="the brand name as customers write it; default the slug in title case")
    ap.add_argument("--mode", default="mock", choices=("mock", "live"), help="mode for the paid Apify lanes")
    ap.add_argument("--max-usd", type=float, default=DEFAULT_MAX_USD, help="cap on the paid lanes for this run")
    ap.add_argument("--fixtures", action="store_true", help="read saved fixtures; no network call")
    ap.add_argument("--free-only", action="store_true", help="skip the paid lanes, still show their estimates")
    ap.add_argument("--out", help="brain root; mock default app/connectors/.mock/onboard, live default app/brain")
    ap.add_argument("--date", help="capture date YYYY-MM-DD, default today")
    ap.add_argument("--compare", action="store_true", help="report record counts per section against the real brain")
    a = ap.parse_args(argv)
    try:
        r = Runner(a.brand, a.url, a.name or a.brand.replace("-", " ").title(), mode=a.mode, max_usd=a.max_usd,
                   fixtures=a.fixtures, out=Path(a.out) if a.out else None, today=a.date, free_only=a.free_only)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    s = r.run(compare=a.compare or a.fixtures)
    print(f"\npaid lanes: ${s['committed_usd']:.2f} of estimates used, ${s['cost_usd']:.2f} spent, cap ${s['max_usd']:.2f}")
    print(f"brain written to {s['root']}/{a.brand}")
    if s.get("compare"):
        c = s["compare"]
        print(f"\nrecord count vs app/brain/{a.brand} (a covered section may lose at most {c['tolerance_pct']:.0f}% of today's records):")
        for row in c["rows"]:
            if row["run"] or row["real"]:
                mark = ("ok " if row["within"] else "OUT") if row["covered"] else " - "
                print(f"  {mark} {row['section']:18} run {row['run']:5}  real {row['real']:5}  lost {row['lost']:3}"
                      f"  added {row['added']:3}  count {row['diff_pct']:+6.1f}%")
        print(f"  total run {c['run_total']}, real {c['real_total']}: {'pass' if c['ok'] else 'outside: ' + ', '.join(c['outside'])}")
    print(f"\n{len(s['questions'])} questions for the founder:")
    for i, q in enumerate(s["questions"], 1):
        print(f"  {i}. [{q['importance']}] {q['text']}")
    return 0 if (not s.get("compare") or s["compare"]["ok"]) else 1


if __name__ == "__main__":
    sys.exit(main())
