"""Apify connector: read-only actor runs with spend caps. Spec: app/contracts/connectors/apify.md.

ApifyClient(mode="mock") reads app/connectors/fixtures/apify/<actor>.json and never
touches the network or the ledger. ApifyClient(mode="live") needs APIFY_TOKEN, estimates
each run from the actor's price per 1,000 results, refuses when the per-run or weekly cap
would be passed, reserves the estimate in intelligence/budget.py, runs the actor with
run-sync-get-dataset-items (async run plus polling on a 408), settles the real usage and
logs run id, item count and cost. The token goes in the Authorization header only; it is
never printed, logged, put in a url or kept in an error message.

CLI: python3 -m app.connectors.apify --brand bombas --lane reddit --mode mock
Mock output goes to app/connectors/.mock/<brand>/raw/<lane>-apify/ unless --out is given,
so fixture records never land in a real brain by accident.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import os
import sys
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "apify"
LOG_PATH = Path(__file__).resolve().parent / ".logs" / "apify_runs.jsonl"
MOCK_OUT = Path(__file__).resolve().parent / ".mock"
LEDGER = ROOT / "data" / "spend.sqlite"
API = "https://api.apify.com/v2"
SYNC_TIMEOUT_S = 300
MIN_RUN_USD = 0.50      # actors charge start and compute fees; an 8-item listing run cost $0.38
SYNC_MAX_ITEMS = 150    # above this, run async and poll, the sync endpoint disconnects on long runs
POLL_S = 10
POLL_MAX_S = 1800

# USD per 1,000 results, seen on the Apify Store on 28 Sep 2026 (contract table).
PRICES_PER_1000 = {
    "axesso_data~amazon-reviews-scraper": 0.90,
    "junglee~amazon-reviews-scraper": 3.00,
    "junglee~amazon-crawler": 54.00,  # observed 28 Sep 2026: $8.64 for 160 search results; listed $0.005 per result did not hold
    "curious_coder~facebook-ads-library-scraper": 0.75,
    "apify~facebook-ads-scraper": 3.40,
    "trudax~reddit-scraper-lite": 3.40,
    "apify~instagram-hashtag-scraper": 2.30,  # Apify Store, 28 Sep 2026; market research social pull
}
# Reservation is an upper bound: price x items, 50 percent margin for start and compute
# fees, plus a flat 5 cents. The ledger halts if a run settles above its reservation.
MARGIN = 1.5
FLAT_USD = 0.05


class ApifyError(RuntimeError):
    """Any connector failure. Messages never carry the token."""


class ApifyCapError(ApifyError):
    """A run was refused before it started because a cap would be passed."""


def estimate_usd(actor: str, max_items: int) -> float:
    if actor not in PRICES_PER_1000:
        raise ApifyError(f"no price on file for actor {actor}; add it to PRICES_PER_1000 before a live run")
    raw = max(PRICES_PER_1000[actor] * max_items / 1000 * MARGIN, MIN_RUN_USD) + FLAT_USD
    return math.ceil(raw * 100) / 100


def iso_week(day: dt.date) -> str:
    y, w, _ = day.isocalendar()
    return f"{y}-W{w:02d}"


def _urllib_transport(method: str, url: str, body: bytes | None, headers: dict, timeout: float):
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()


class ApifyClient:
    def __init__(self, token: str | None = None, mode: str = "live", *, brand: str = "default",
                 budget: dict | None = None, ledger_path: Path | str | None = None,
                 log_path: Path | str | None = None, fixtures_dir: Path | str | None = None,
                 transport=None, today: dt.date | None = None):
        if mode not in ("live", "mock"):
            raise ApifyError(f"mode must be live or mock, not {mode}")
        self.mode = mode
        self.brand = brand
        self.budget = dict(budget or {})
        self.ledger_path = Path(ledger_path) if ledger_path else (LEDGER if mode == "live" else None)
        self.log_path = Path(log_path) if log_path else LOG_PATH
        self.fixtures_dir = Path(fixtures_dir) if fixtures_dir else FIXTURES
        self.today = today or dt.date.today()
        self.last_run: dict | None = None
        self._transport = transport or _urllib_transport
        self.__token = token or os.environ.get("APIFY_TOKEN") or None
        if mode == "live" and not self.__token:
            raise ApifyError("APIFY_TOKEN is not set. Add it to .env locally or to the cloud environment's "
                             "settings, or use mode='mock'. No network call was made.")

    def __repr__(self) -> str:
        return f"ApifyClient(mode={self.mode!r}, brand={self.brand!r}, token={'set' if self.__token else 'missing'})"

    # ---- caps -----------------------------------------------------------------
    def _ledger(self):
        from intelligence.budget import Budget
        return Budget(self.ledger_path)

    def week_spent_usd(self) -> float:
        """Apify spend this ISO week in the ledger (settled, else reserved), for this brand."""
        if not self.ledger_path or not Path(self.ledger_path).exists():
            return 0.0
        b = self._ledger()
        try:
            prefix = f"apify:{self.brand}:{iso_week(self.today)}:%"
            row = b.db.execute("SELECT COALESCE(SUM(COALESCE(actual,reserved)),0) FROM spend WHERE request_id LIKE ?",
                               (prefix,)).fetchone()
            return row[0] / 1_000_000
        finally:
            b.close()

    def check_caps(self, actor: str, max_items: int, max_usd: float | None = None) -> float:
        """Return the reservation for this run, or raise ApifyCapError. Works in both modes."""
        est = estimate_usd(actor, max_items)
        per_run = max_usd if max_usd is not None else self.budget.get("max_usd_per_run")
        if per_run is None:
            raise ApifyCapError("no per-run cap given; set budget.max_usd_per_run in config/apify.json")
        if est > per_run:
            raise ApifyCapError(f"run refused: estimate ${est:.2f} for {max_items} items on {actor} "
                                f"is over the per-run cap ${per_run:.2f}")
        weekly = self.budget.get("max_usd_per_week")
        if weekly is not None:
            spent = self.week_spent_usd()
            if spent + est > weekly:
                raise ApifyCapError(f"run refused: ${spent:.2f} spent this week plus ${est:.2f} "
                                    f"is over the weekly cap ${weekly:.2f}")
        return est

    # ---- runs -----------------------------------------------------------------
    def run(self, actor: str, input: dict, max_items: int, max_usd: float | None = None, lane: str | None = None) -> list[dict]:
        est = self.check_caps(actor, max_items, max_usd)
        if self.mode == "mock":
            items = self._mock_items(actor)[:max_items]
            self._record(lane, actor, f"mock-{actor.replace('~', '-')}", len(items), 0.0)
            return items
        return self._live_run(actor, input, max_items, est, lane)

    def _mock_items(self, actor: str) -> list[dict]:
        path = self.fixtures_dir / f"{actor}.json"
        if not path.exists():
            raise ApifyError(f"no fixture for {actor} at {path}")
        data = json.loads(path.read_text(encoding="utf-8"))
        return list(data["items"] if isinstance(data, dict) else data)

    def _headers(self) -> dict:
        return {"Authorization": f"Bearer {self.__token}", "Content-Type": "application/json"}

    def _call(self, method: str, path: str, body: dict | None = None, timeout: float = 60):
        data = json.dumps(body).encode() if body is not None else None
        try:
            status, raw = self._transport(method, API + path, data, self._headers(), timeout)
        except Exception as exc:  # network errors: report the path only
            raise ApifyError(f"Apify request failed on {method} {path}: {type(exc).__name__}") from None
        return status, raw

    def _json(self, method: str, path: str, body: dict | None = None, timeout: float = 60):
        status, raw = self._call(method, path, body, timeout)
        if status >= 300:
            raise ApifyError(f"Apify HTTP {status} on {method} {path}")
        return json.loads(raw or b"null")

    def _live_run(self, actor: str, input: dict, max_items: int, est: float, lane: str | None) -> list[dict]:
        request_id = f"apify:{self.brand}:{iso_week(self.today)}:{actor}:{uuid.uuid4().hex[:10]}"
        ledger = self._ledger()
        try:
            try:
                ledger.reserve(request_id, "apify", est)
            except ValueError as exc:
                raise ApifyCapError(f"run refused by the budget ledger: {exc}") from None
            # From here an unknown outcome keeps its reservation, as the ledger requires.
            if max_items > SYNC_MAX_ITEMS:
                status, raw = 408, b""
            else:
                status, raw = self._call("POST", f"/acts/{actor}/run-sync-get-dataset-items?timeout={SYNC_TIMEOUT_S}"
                                         f"&maxItems={max_items}&clean=1", input, timeout=SYNC_TIMEOUT_S + 30)
            if status == 408:
                run_id, usd, items = self._async_run(actor, input, max_items)
            elif 400 <= status < 500:
                ledger.settle(request_id, 0.000001)
                raise ApifyError(f"Apify HTTP {status} on run-sync for {actor} (refused before running; nothing charged)")
            elif status >= 300:
                raise ApifyError(f"Apify HTTP {status} on run-sync for {actor}")
            else:
                items = json.loads(raw or b"[]")
                last = (self._json("GET", f"/acts/{actor}/runs/last") or {}).get("data") or {}
                run_id, usd = last.get("id") or "unknown", last.get("usageTotalUsd")
            items = list(items)[:max_items]
            actual = float(usd) if usd is not None else estimate_usd(actor, len(items)) - FLAT_USD
            try:
                ledger.settle(request_id, max(actual, 0.000001))
            except ValueError as exc:
                raise ApifyError(f"run {run_id} settled at ${actual:.2f}: {exc}") from None
        finally:
            ledger.close()
        self._record(lane, actor, run_id, len(items), actual)
        return items

    def _async_run(self, actor: str, input: dict, max_items: int):
        run = self._json("POST", f"/acts/{actor}/runs?maxItems={max_items}", input)["data"]
        run_id, waited = run["id"], 0
        while run.get("status") in ("READY", "RUNNING", "TIMING-OUT", "ABORTING"):
            if waited >= POLL_MAX_S:
                raise ApifyError(f"run {run_id} still running after {POLL_MAX_S} s; reservation kept")
            time.sleep(POLL_S)
            waited += POLL_S
            run = self._json("GET", f"/actor-runs/{run_id}")["data"]
        if run.get("status") not in ("SUCCEEDED", "TIMED-OUT"):
            raise ApifyError(f"run {run_id} ended {run.get('status')}; reservation kept")
        items = self._json("GET", f"/datasets/{run['defaultDatasetId']}/items?clean=1&limit={max_items}")
        return run_id, run.get("usageTotalUsd"), items

    def _record(self, lane, actor, run_id, n, usd):
        self.last_run = {"at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "mode": self.mode,
                         "brand": self.brand, "lane": lane, "actor": actor, "run_id": run_id, "items": n,
                         "usd": round(usd, 4)}
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        with self.log_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(self.last_run) + "\n")

    # ---- status ---------------------------------------------------------------
    def status(self, check_remote: bool = False) -> dict:
        last: dict = {}
        if self.log_path.exists():
            for line in self.log_path.read_text(encoding="utf-8").splitlines():
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if row.get("brand") == self.brand:
                    last[row.get("lane") or row.get("actor")] = row
        credit = None
        if check_remote and self.mode == "live":
            data = (self._json("GET", "/users/me/limits") or {}).get("data") or {}
            cap = (data.get("limits") or {}).get("maxMonthlyUsageUsd")
            used = (data.get("current") or {}).get("monthlyUsageUsd")
            if cap is not None and used is not None:
                credit = round(cap - used, 2)
        return {"mode": self.mode, "token_present": bool(self.__token), "plan_credit_usd": credit,
                "week_spent_usd": round(self.week_spent_usd(), 2), "last_run": last}


def write_raw(root: Path, brand: str, lane: str, records: list[dict], sources: list[dict]) -> Path:
    """Write <root>/<brand>/raw/<lane>-apify/<section>.json and sources.json. Returns the folder."""
    folder = Path(root) / brand / "raw" / f"{lane}-apify"
    folder.mkdir(parents=True, exist_ok=True)
    for old in folder.glob("*.json"):
        old.unlink()
    by_section: dict[str, list[dict]] = {}
    for rec in records:
        by_section.setdefault(rec["section"], []).append(rec)
    for section, recs in by_section.items():
        (folder / f"{section}.json").write_text(json.dumps(recs, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    (folder / "sources.json").write_text(json.dumps(sources, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return folder


LANES = {"amazon": "apify_amazon", "adlibrary": "apify_adlibrary", "reddit": "apify_reddit"}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Run one Apify lane for a brand and write its raw folder.")
    ap.add_argument("--brand", required=True)
    ap.add_argument("--lane", required=True, choices=sorted(LANES))
    ap.add_argument("--mode", default="mock", choices=("mock", "live"))
    ap.add_argument("--out", help="brain root to write <brand>/raw/ under; mock default app/connectors/.mock, live default app/brain")
    ap.add_argument("--date", help="capture date YYYY-MM-DD, default today")
    args = ap.parse_args(argv)
    import importlib
    config_path = ROOT / "app" / "brain" / args.brand / "config" / "apify.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    out = Path(args.out) if args.out else (MOCK_OUT if args.mode == "mock" else ROOT / "app" / "brain")
    if args.mode == "mock" and out.resolve() == (ROOT / "app" / "brain").resolve():
        print("warning: writing fixture records into a real brain folder; merge.py will read them", file=sys.stderr)
    today = dt.date.fromisoformat(args.date) if args.date else dt.date.today()
    try:
        client = ApifyClient(mode=args.mode, brand=args.brand, budget=config.get("budget"), today=today)
        mod = importlib.import_module(f"app.brain.extract.{LANES[args.lane]}")
        result = mod.run(args.brand, config, client=client, root=out, captured_at=today.isoformat())
    except ApifyError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
