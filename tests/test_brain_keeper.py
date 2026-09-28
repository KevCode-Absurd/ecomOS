import datetime as dt
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app" / "brain"))
import audit  # noqa: E402
import keeper  # noqa: E402
import router  # noqa: E402
from store import Brain  # noqa: E402

EXAMPLE = ROOT / "app" / "brain" / "example"
TODAY = dt.date(2026, 9, 28)
TOP5 = ["q.economics.gross_margin", "q.claims.approved", "q.calendar.peaks",
        "q.learnings.tested", "q.products.hero"]


class KeeperTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        shutil.copytree(EXAMPLE, self.tmp / "example")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def brain(self, today=TODAY):
        return Brain("example", root=self.tmp, today=today)

    def bank(self):
        return {q["id"]: q for q in keeper.load_bank()}


class TestAsk(KeeperTestCase):
    def test_no_sources_top5_by_importance(self):
        asks = keeper.ask(self.brain())
        self.assertEqual([a["id"] for a in asks], TOP5)
        imps = [a["importance"] for a in asks]
        self.assertEqual(imps, sorted(imps, reverse=True))
        self.assertEqual(asks[0]["importance"], 50)

    def test_filled_section_is_asked_only_while_weak(self):
        # the example has 2 avatars; the_athlete is at 0.4 confidence, so the question stays open
        ids = [a["id"] for a in keeper.ask(self.brain(), n=100)]
        self.assertIn("q.avatars.who_buys", ids)
        path = self.tmp / "example" / "avatars.json"
        recs = json.loads(path.read_text())
        for r in recs:
            r["confidence"] = 0.8
        path.write_text(json.dumps(recs))
        ids = [a["id"] for a in keeper.ask(self.brain(), n=100)]
        self.assertNotIn("q.avatars.who_buys", ids)
        self.assertIn("q.team.approvals", ids)

    def test_never_more_than_n(self):
        self.assertEqual(len(keeper.ask(self.brain(), n=3)), 3)

    def test_connected_shopify_drops_its_questions(self):
        bank = self.bank()
        ids = [a["id"] for a in keeper.ask(self.brain(), connected_sources=["shopify"], n=100)]
        for qid, q in bank.items():
            if "shopify" in q["answerable_by"]:
                self.assertNotIn(qid, ids)
        self.assertIn("q.economics.gross_margin", ids)
        self.assertEqual(len(keeper.ask(self.brain(), connected_sources=["shopify"])), 5)

    def test_not_connected_source_becomes_connect_or_answer(self):
        hero = next(a for a in keeper.ask(self.brain()) if a["id"] == "q.products.hero")
        self.assertEqual(hero["kind"], "connect_or_answer")
        self.assertIn("shopify", hero["connect"])
        self.assertTrue(hero["text"].startswith("Connect "))
        self.assertIn("or answer this in a line", hero["text"])

    def test_founder_only_question_is_plain(self):
        claims = next(a for a in keeper.ask(self.brain()) if a["id"] == "q.claims.approved")
        self.assertEqual(claims["kind"], "plain")
        self.assertEqual(claims["connect"], [])

    def test_declined_source_turns_questions_plain(self):
        asks = {a["id"]: a for a in keeper.ask(self.brain(), declined_sources=["shopify"], n=100)}
        hero = asks["q.products.hero"]
        self.assertEqual(hero["kind"], "plain")
        self.assertEqual(hero["text"], self.bank()["q.products.hero"]["asks"])
        for a in asks.values():
            self.assertNotIn("shopify", a["connect"])
            self.assertNotIn("Shopify", a["text"].split(",")[0] if a["kind"] == "connect_or_answer" else "")
        # still asked, and other categories still offered
        self.assertEqual(asks["q.calendar.peaks"]["kind"], "connect_or_answer")
        self.assertIn("klaviyo", asks["q.calendar.peaks"]["connect"])

    def test_public_sources_are_never_offered(self):
        for a in keeper.ask(self.brain(), n=100):
            for s in ("site", "public_reviews", "meta_ad_library"):
                self.assertNotIn(s, a["connect"])


class TestGaps(KeeperTestCase):
    def test_kinds(self):
        brain = self.brain(today=dt.date(2026, 10, 5))
        g = keeper.gaps(brain)
        kinds = {x["kind"] for x in g}
        self.assertIn("expired", kinds)
        self.assertIn("empty", kinds)
        empty = {x["field"] for x in g if x["kind"] == "empty"}
        self.assertIn("economics.gross_margin_pct", empty)
        self.assertNotIn("avatars", empty)

    def test_conflict_and_low_confidence(self):
        path = self.tmp / "example" / "offers.json"
        recs = json.loads(path.read_text())
        dup = dict(recs[0], id="example.offers.free_shipping_threshold_usd_b", value=75, confidence=0.3)
        path.write_text(json.dumps(recs + [dup]))
        g = keeper.gaps(self.brain())
        conflicts = [x for x in g if x["kind"] == "conflict"]
        self.assertEqual(len(conflicts), 1)
        self.assertEqual(conflicts[0]["values"], [50, 75])
        self.assertIn("example.offers.free_shipping_threshold_usd_b",
                      [x["record"] for x in g if x["kind"] == "low_confidence"])


class TestAudit(KeeperTestCase):
    def test_findings(self):
        router.write("example", root=self.tmp, today=TODAY)
        brain = self.brain(today=dt.date(2026, 10, 5))
        found = audit.audit(brain)
        kinds = {p["kind"] for p in found}
        for k in ("stale", "empty", "drifted", "broken_link", "unread"):
            self.assertIn(k, kinds)
        for p in found:
            self.assertTrue(p["before"] and p["after"] and p["target"])

    def test_fresh_brain_md_has_no_drift(self):
        router.write("example", root=self.tmp, today=TODAY)
        self.assertEqual(audit.drift(self.brain()), [])

    def test_broken_link_named(self):
        router.write("example", root=self.tmp, today=TODAY)
        targets = [p["target"] for p in audit.broken_links(self.brain(), repo=ROOT)]
        self.assertIn("BRAIN.md -> open_questions.json", targets)
        self.assertNotIn("BRAIN.md -> offers.json", targets)
        self.assertNotIn("BRAIN.md -> documents/manifest.json", targets)


if __name__ == "__main__":
    unittest.main()
