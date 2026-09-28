"""Tests for app/brain/extract/apify_reddit.py's plan(), press.py and jobs.py: all offline.

No network: fixture mode reads saved responses, and live fetching is patched to fail the
test if anything tries to reach out.
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "app" / "brain"))

import validate  # noqa: E402
from app.brain.extract import apify_reddit, jobs, press  # noqa: E402

PRESS_FIXTURE = ROOT / "app" / "brain" / "extract" / "fixtures" / "press" / "bombas"
JOBS_FIXTURE = ROOT / "app" / "brain" / "extract" / "fixtures" / "jobs" / "bombas"
BOMBAS_BRAIN = {"identity": {"category": "sock and apparel brand"},
                "products": {"lines": ["Socks", "Underwear", "T-Shirts", "Loungewear"]}}


def _no_network(*a, **k):
    raise AssertionError("fixture mode must not touch the network")


def _strings(v):
    if isinstance(v, str):
        yield v
    elif isinstance(v, list):
        for x in v:
            yield from _strings(x)
    elif isinstance(v, dict):
        for x in v.values():
            yield from _strings(x)


def _records(folder: Path):
    out = []
    for f in folder.glob("*.json"):
        if f.stem == "sources":
            continue
        out.extend(json.loads(f.read_text(encoding="utf-8")))
    return out


class RedditPlan(unittest.TestCase):
    def setUp(self):
        self.plan = apify_reddit.plan("bombas", BOMBAS_BRAIN, brand_name="Bombas")

    def test_buy_it_for_life_always_proposed(self):
        self.assertIn("BuyItForLife", self.plan["proposed_subreddits"])

    def test_at_least_five_queries(self):
        self.assertGreaterEqual(len(self.plan["searches"]), 5)

    def test_no_usernames_stored(self):
        blob = json.dumps(self.plan)
        self.assertNotIn("u/", blob)

    def test_queries_use_brand_and_category(self):
        self.assertTrue(any("Bombas" in q for q in self.plan["searches"]))
        self.assertTrue(any(self.plan["category_term"] in q for q in self.plan["searches"]))

    def test_write_plan_does_not_touch_confirmed_subreddits(self):
        with tempfile.TemporaryDirectory() as tmp:
            cfg_path = Path(tmp) / "bombas" / "config" / "apify.json"
            cfg_path.parent.mkdir(parents=True)
            cfg_path.write_text(json.dumps({"reddit": {"subreddits": ["BuyItForLife", "socks"], "actor": "x"}}), encoding="utf-8")
            result = apify_reddit.write_plan("bombas", brain_root=tmp, config_path=cfg_path)
            written = json.loads(cfg_path.read_text(encoding="utf-8"))
            self.assertEqual(written["reddit"]["subreddits"], ["BuyItForLife", "socks"])
            self.assertEqual(written["reddit"]["proposed_subreddits"], result["proposed_subreddits"])


class PressFixture(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out = Path(cls.tmp.name)
        with mock.patch("urllib.request.urlopen", _no_network):
            cls.result = press.run("bombas", {"press": {"brand_name": "Bombas", "site_url": "https://bombas.com"}},
                                   root=cls.out, captured_at="2026-09-28", fixture=PRESS_FIXTURE)
        cls.folder = cls.out / "bombas" / "raw" / "press"

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_produced_records(self):
        self.assertGreater(self.result["records"], 0)

    def test_valid_against_schema(self):
        self.assertEqual(validate.check_path(self.folder), [])

    def test_every_record_has_url_and_date(self):
        for r in _records(self.folder):
            self.assertTrue(r["source"]["ref"].startswith("http"), r["id"])
            self.assertRegex(r["source"]["captured_at"], r"^\d{4}-\d{2}-\d{2}$")
            self.assertTrue(r["value"].get("url", "").startswith("http"), r["id"])

    def test_no_text_over_300_chars(self):
        for r in _records(self.folder):
            for s in _strings(r):
                self.assertLessEqual(len(s), 300, r["id"])

    def test_tier_reported(self):
        for r in _records(self.folder):
            self.assertEqual(r["tier"], "reported")

    def test_own_domain_and_retailers_skipped(self):
        for r in _records(self.folder):
            self.assertNotIn("bombas.com", r["value"]["url"])
            self.assertNotIn("nordstrom.com", r["value"]["url"])


class JobsFixture(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out = Path(cls.tmp.name)
        with mock.patch("urllib.request.urlopen", _no_network):
            cls.result = jobs.run("bombas", {"jobs": {"brand_name": "Bombas", "site_url": "https://bombas.com"}},
                                  root=cls.out, captured_at="2026-09-28", fixture=JOBS_FIXTURE)
        cls.folder = cls.out / "bombas" / "raw" / "jobs"

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_produced_team_records(self):
        self.assertGreater(self.result["records"], 0)
        self.assertTrue((self.folder / "team.json").exists())

    def test_valid_against_schema(self):
        self.assertEqual(validate.check_path(self.folder), [])

    def test_every_record_has_url_and_date(self):
        for r in _records(self.folder):
            self.assertTrue(r["source"]["ref"].startswith("http"), r["id"])
            self.assertRegex(r["source"]["captured_at"], r"^\d{4}-\d{2}-\d{2}$")

    def test_no_text_over_300_chars(self):
        for r in _records(self.folder):
            for s in _strings(r):
                self.assertLessEqual(len(s), 300, r["id"])

    def test_roles_matched_to_brand_only(self):
        for r in _records(self.folder):
            if r["section"] == "team":
                self.assertIn("Bombas", r["text"])


class RedditWritesNothingIntoClaimsOrStoryBank(unittest.TestCase):
    def test_reddit_adapter_sections(self):
        from app.connectors import apify_adapters
        items = [{"dataType": "post", "title": "Are Bombas socks worth it?", "body": "I love mine, no holes after a year.",
                 "parsedCommunityName": "BuyItForLife", "upVotes": 42, "url": "https://reddit.com/r/BuyItForLife/1",
                 "createdAt": "2026-01-01T00:00:00Z", "parsedId": "abc123"}]
        records = apify_adapters.reddit(items, "bombas", run_id="test", captured_at="2026-09-28")
        sections = {r["section"] for r in records}
        self.assertNotIn("claims", sections)
        self.assertNotIn("story_bank", sections)
        for r in records:
            self.assertNotIn("u/abc123", json.dumps(r))


if __name__ == "__main__":
    unittest.main()
