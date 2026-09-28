"""Tests for the Apify connector (app/connectors/apify.py), its adapters and the three extractors.

No network: live-mode tests use a transport that fails the test if it is ever called.
"""
import datetime as dt
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "app" / "brain"))

import validate  # noqa: E402
from app.connectors import apify, apify_adapters  # noqa: E402
from app.brain.extract import apify_adlibrary, apify_amazon, apify_reddit  # noqa: E402
from intelligence.budget import Budget  # noqa: E402

CONFIG = json.loads((ROOT / "app" / "brain" / "bombas" / "sources.config.json").read_text())
FIXTURES = ROOT / "app" / "connectors" / "fixtures" / "apify"
TODAY = dt.date(2026, 9, 28)
EXTRACTORS = {"reddit": apify_reddit, "adlibrary": apify_adlibrary, "amazon": apify_amazon}


def no_network(*args, **kwargs):
    raise AssertionError("network called")


def usernames():
    names = set()
    for path in FIXTURES.glob("*.json"):
        for it in json.loads(path.read_text())["items"]:
            for key in ("userName", "username", "author"):
                if it.get(key):
                    names.add(it[key])
    return names


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def client(self, mode="mock", **kw):
        kw.setdefault("budget", CONFIG["budget"])
        kw.setdefault("log_path", self.dir / "runs.jsonl")
        kw.setdefault("today", TODAY)
        return apify.ApifyClient(mode=mode, brand="bombas", **kw)


class MockLanes(Base):
    def test_fixtures_hold_5_to_10_marked_items(self):
        for path in FIXTURES.glob("*.json"):
            data = json.loads(path.read_text())
            self.assertIn("INVENTED FIXTURE", data["_fixture"])
            self.assertTrue(5 <= len(data["items"]) <= 10, path.name)

    def test_all_three_lanes_write_valid_raw_folders(self):
        for lane, mod in EXTRACTORS.items():
            with self.subTest(lane=lane):
                result = mod.run("bombas", CONFIG, client=self.client(), root=self.dir, captured_at="2026-09-28")
                folder = self.dir / "bombas" / "raw" / f"{lane}-apify"
                self.assertEqual(Path(result["folder"]), folder)
                self.assertGreater(result["records"], 0)
                self.assertEqual(validate.check_path(folder), [])
                self.assertTrue((folder / "sources.json").exists())
                for rec in self._records(folder):
                    self.assertEqual(rec["tier"], "evidence")
                    self.assertEqual(rec["visibility"], "public")
                    self.assertTrue(rec["source"]["ref"].startswith("apify:"), rec["id"])
                    self.assertEqual(len(rec["source"]["ref"].split(":", 3)), 4)

    def test_sections_per_lane(self):
        want = {"reddit": {"language_bank", "objections", "avatars", "competitors", "positioning", "seo_facts", "content"},
                "adlibrary": {"competitors", "offers", "learnings", "content"},
                "amazon": {"language_bank", "objections", "products", "marketplaces"}}
        for lane, mod in EXTRACTORS.items():
            mod.run("bombas", CONFIG, client=self.client(), root=self.dir, captured_at="2026-09-28")
            got = {p.stem for p in (self.dir / "bombas" / "raw" / f"{lane}-apify").glob("*.json")} - {"sources"}
            self.assertEqual(got, want[lane], lane)

    def test_no_usernames_anywhere(self):
        names = usernames()
        self.assertGreaterEqual(len(names), 10)
        for mod in EXTRACTORS.values():
            mod.run("bombas", CONFIG, client=self.client(), root=self.dir, captured_at="2026-09-28")
        for path in (self.dir / "bombas" / "raw").rglob("*.json"):
            text = path.read_text()
            for name in names:
                self.assertNotIn(name, text, f"{name} in {path.name}")
            self.assertNotIn("example.invalid", text, "media url stored")

    def test_reddit_records_carry_the_note(self):
        apify_reddit.run("bombas", CONFIG, client=self.client(), root=self.dir, captured_at="2026-09-28")
        for rec in self._records(self.dir / "bombas" / "raw" / "reddit-apify"):
            self.assertTrue(rec["notes"].startswith("reddit language, not for testimonial use"), rec["id"])

    def test_amazon_quotes_trimmed_and_stars_kept(self):
        items = [{"asin": "A1", "reviewId": "R1", "rating": "1.0 out of 5 stars", "title": "Bad",
                  "text": "hole " * 200, "url": "https://www.amazon.com/r/R1", "userName": "someone_secret"}]
        recs = apify_adapters.amazon_reviews(items, "acme", "A1", None, run_id="run9", captured_at="2026-09-28")
        lb = [r for r in recs if r["section"] == "language_bank"][0]
        review = lb["value"]["reviews"][0]
        self.assertLessEqual(len(review["quote"]), 300)
        self.assertEqual(review["star"], 1)
        self.assertEqual(lb["source"]["ref"], "apify:axesso_data~amazon-reviews-scraper:run9:https://www.amazon.com/r/R1")
        self.assertNotIn("someone_secret", json.dumps(recs))

    def test_mock_output_defaults_outside_the_real_brain(self):
        self.assertNotEqual(apify.MOCK_OUT.resolve(), (ROOT / "app" / "brain").resolve())

    @staticmethod
    def _records(folder):
        for path in folder.glob("*.json"):
            if path.stem != "sources":
                yield from json.loads(path.read_text())


class Caps(Base):
    def test_per_run_cap_refuses(self):
        c = self.client(budget={"max_usd_per_run": 0.5, "max_usd_per_week": 15})
        with self.assertRaises(apify.ApifyCapError):
            c.run("trudax~reddit-scraper-lite", {}, 600)

    def test_explicit_max_usd_refuses(self):
        with self.assertRaises(apify.ApifyCapError):
            self.client().run("trudax~reddit-scraper-lite", {}, 600, max_usd=0.10)

    def test_weekly_cap_counts_the_ledger(self):
        ledger = self.dir / "spend.sqlite"
        b = Budget(ledger)
        b.reserve(f"apify:bombas:{apify.iso_week(TODAY)}:trudax~reddit-scraper-lite:x1", "apify", 14.0)
        b.close()
        c = self.client(ledger_path=ledger)
        self.assertAlmostEqual(c.week_spent_usd(), 14.0)
        with self.assertRaises(apify.ApifyCapError):
            c.run("trudax~reddit-scraper-lite", {}, 600)
        next_week = self.client(ledger_path=ledger, today=TODAY + dt.timedelta(days=7))
        self.assertEqual(len(next_week.run("trudax~reddit-scraper-lite", {}, 600)), 8)

    def test_live_over_cap_refuses_before_network_or_ledger(self):
        ledger = self.dir / "spend.sqlite"
        c = self.client("live", token="test-token-not-real", ledger_path=ledger, transport=no_network,
                        budget={"max_usd_per_run": 0.5, "max_usd_per_week": 15})
        with self.assertRaises(apify.ApifyCapError):
            c.run("trudax~reddit-scraper-lite", {}, 600)
        self.assertFalse(ledger.exists())

    def test_live_run_reserves_and_settles(self):
        ledger = self.dir / "spend.sqlite"
        items = json.loads((FIXTURES / "trudax~reddit-scraper-lite.json").read_text())["items"]
        calls = []

        def fake(method, url, body, headers, timeout):
            calls.append((method, url))
            self.assertNotIn("test-token", url)
            if "run-sync-get-dataset-items" in url:
                return 200, json.dumps(items).encode()
            return 200, json.dumps({"data": {"id": "RUN123", "usageTotalUsd": 0.03}}).encode()

        c = self.client("live", token="test-token-not-real", ledger_path=ledger, transport=fake)
        got = c.run("trudax~reddit-scraper-lite", {"searches": ["x"]}, 20, lane="reddit")
        self.assertEqual(len(got), len(items))
        self.assertEqual(c.last_run["run_id"], "RUN123")
        self.assertAlmostEqual(c.week_spent_usd(), 0.03)
        log = (self.dir / "runs.jsonl").read_text()
        self.assertIn("RUN123", log)
        self.assertNotIn("test-token", log)
        self.assertNotIn("test-token", repr(c))

    def test_live_408_falls_back_to_async_run(self):
        ledger = self.dir / "spend.sqlite"
        seen = []

        def fake(method, url, body, headers, timeout):
            seen.append(url.split("?")[0].rsplit("/v2", 1)[1])
            if "run-sync-get-dataset-items" in url:
                return 408, b""
            if url.endswith("/runs") or "/runs?" in url:
                return 201, json.dumps({"data": {"id": "RUNA", "status": "RUNNING"}}).encode()
            if "/actor-runs/RUNA" in url:
                return 200, json.dumps({"data": {"id": "RUNA", "status": "SUCCEEDED", "defaultDatasetId": "DS1",
                                                 "usageTotalUsd": 0.02}}).encode()
            if "/datasets/DS1/items" in url:
                return 200, json.dumps([{"id": 1}, {"id": 2}]).encode()
            raise AssertionError(url)

        c = self.client("live", token="test-token-not-real", ledger_path=ledger, transport=fake)
        with mock.patch.object(apify, "POLL_S", 0):
            got = c.run("trudax~reddit-scraper-lite", {}, 20, lane="reddit")
        self.assertEqual(len(got), 2)
        self.assertEqual(c.last_run["run_id"], "RUNA")
        self.assertIn("/actor-runs/RUNA", seen)


class LiveWithoutToken(Base):
    def test_clear_error_and_no_network(self):
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("APIFY_TOKEN", None)
            with mock.patch("urllib.request.urlopen", side_effect=AssertionError("network called")):
                with self.assertRaises(apify.ApifyError) as ctx:
                    self.client("live", transport=no_network)
        self.assertIn("APIFY_TOKEN", str(ctx.exception))

    def test_cli_live_without_token_exits_cleanly(self):
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("APIFY_TOKEN", None)
            with mock.patch("urllib.request.urlopen", side_effect=AssertionError("network called")):
                code = apify.main(["--brand", "bombas", "--lane", "reddit", "--mode", "live", "--out", str(self.dir)])
        self.assertEqual(code, 2)
        self.assertFalse((self.dir / "bombas").exists())

    def test_status_mock(self):
        c = self.client()
        c.run("trudax~reddit-scraper-lite", {}, 5, lane="reddit")
        s = c.status()
        self.assertEqual(s["mode"], "mock")
        self.assertIn("reddit", s["last_run"])
        self.assertIsNone(s["plan_credit_usd"])


if __name__ == "__main__":
    unittest.main()
