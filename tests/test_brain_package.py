import datetime as dt
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app" / "brain"))
import package  # noqa: E402
import router  # noqa: E402
from store import Brain  # noqa: E402

EXAMPLE = ROOT / "app" / "brain" / "example"
TODAY = dt.date(2026, 9, 28)
BRIEF = {"id": "TEST-BRIEF", "brain_sections": {"offers": "T1", "avatars": "T2", "learnings": "T2"},
         "brain_budget": 4000}


class BrainTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        shutil.copytree(EXAMPLE, self.tmp / "example")
        (self.tmp / "example" / "BRAIN.md").unlink(missing_ok=True)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def brain(self, today=TODAY):
        return Brain("example", self.tmp, today)


class StoreTests(BrainTestCase):
    def test_defaults_on_bare_note(self):
        note = self.brain().get("example.learnings.note_2026_09_28_1")
        self.assertEqual(note["tier"], "unverified")
        self.assertIsNone(note["confidence"])
        self.assertEqual(note["visibility"], "private")
        self.assertEqual(note["date"], "undated")

    def test_expired_record_reads_stale(self):
        rec = self.brain(dt.date(2026, 10, 3)).get("example.offers.guarantee")
        self.assertEqual(rec["status"], "stale")

    def test_put_keeps_history_and_retire_keeps_record(self):
        b = self.brain()
        rec = dict(b.raw("offers")[0], value=75, text="Free shipping on orders over $75.")
        self.assertEqual(b.put(rec), [])
        saved = b.raw("offers")[0]
        self.assertEqual(saved["value"], 75)
        self.assertEqual(saved["history"][-1]["value"], 50)
        self.assertTrue(b.retire(rec["id"]))
        self.assertEqual(b.raw("offers")[0]["status"], "retired")
        self.assertNotIn(rec["id"], [r["id"] for r in b.records("offers")])

    def test_put_rejects_invalid(self):
        b = self.brain()
        before = b.version()
        errs = b.put({"id": "example.offers.x", "brand": "example", "section": "offers", "text": "a — b"})
        self.assertTrue(errs)
        self.assertEqual(b.version(), before)


class PackageTests(BrainTestCase):
    def build(self, cap=BRIEF, budget=None, today=TODAY):
        return package.package("example", cap, budget, root=self.tmp, today=today, use_cache=False)

    def test_tiers_in_order_and_under_budget(self):
        pkg = self.build()
        self.assertEqual([p["tier"] for p in pkg["parts"]], ["T0", "T1", "T1", "T1", "T2"])
        self.assertLessEqual(pkg["tokens"], pkg["budget"])
        self.assertTrue(pkg["text"].startswith(pkg["parts"][0]["text"]))

    def test_every_record_has_date_and_tier(self):
        recs = self.build()["records"]
        self.assertEqual(len(recs), 4)
        for r in recs:
            self.assertTrue(r["date"])
            self.assertTrue(r["tier"])
            self.assertIn(f"[{r['tier']}, {r['date']}", r["text"])

    def test_tight_budget_drops_t2_first(self):
        full = self.build()
        t0_t1 = sum(package.tokens(p["text"]) for p in full["parts"] if p["tier"] != "T2")
        pkg = self.build(budget=t0_t1 + 40)
        self.assertLessEqual(pkg["tokens"], pkg["budget"])
        self.assertLess(len(pkg["records"]), 4)
        self.assertEqual(sum(p["tier"] == "T1" for p in pkg["parts"]), 3)

    def test_ordering_confidence_then_stale_last(self):
        ids = [r["id"] for r in self.build()["records"] if r["section"] == "avatars"]
        self.assertEqual(ids, ["example.avatars.the_gifter", "example.avatars.the_athlete"])

    def test_public_facing_excludes_private(self):
        pkg = self.build(dict(BRIEF, public_facing=True))
        ids = [r["id"] for r in pkg["records"]]
        self.assertNotIn("example.learnings.winning_ad_q2_hook", ids)
        self.assertNotIn("Dad socks UGC 03", pkg["text"])

    def test_t1_cites_record_ids(self):
        t1 = self.build()["parts"][1]["text"]
        self.assertIn("Cites: example.offers.", t1)

    def test_t0_shows_promo_and_freshness(self):
        t0 = package.t0_card(self.brain(dt.date(2026, 10, 3)))
        self.assertIn("buy 4 get 1 free", t0)
        self.assertIn("3 stale in offers", t0)

    def test_cache_by_version(self):
        a = package.package("example", BRIEF, root=self.tmp, today=TODAY)
        self.assertIs(package.package("example", BRIEF, root=self.tmp, today=TODAY), a)
        self.brain().put({"id": "example.learnings.n2", "brand": "example", "section": "learnings", "text": "New."})
        self.assertIsNot(package.package("example", BRIEF, root=self.tmp, today=TODAY), a)

    def test_unknown_capability_id_raises(self):
        with self.assertRaises(KeyError):
            package.resolve("NOPE-C99")


class RouterTests(BrainTestCase):
    def test_brain_md_under_limit_with_links(self):
        text = router.write("example", self.tmp, TODAY).read_text(encoding="utf-8")
        self.assertLessEqual(package.tokens(text), router.MAX_TOKENS)
        for piece in ("## Sections", "## Routing", "documents/manifest.json", "open_questions.json",
                      "[offers](offers.json)", router.NOTES_START):
            self.assertIn(piece, text)

    def test_founder_notes_survive_regeneration(self):
        path = router.write("example", self.tmp, TODAY)
        notes = "Never discount the hero pack.\n\nCall me before any price test."
        text = path.read_text(encoding="utf-8")
        default = f"{router.NOTES_START}\n{router.DEFAULT_NOTES}\n{router.NOTES_END}"
        path.write_text(text.replace(default, f"{router.NOTES_START}\n{notes}\n{router.NOTES_END}"),
                        encoding="utf-8")
        self.brain().put({"id": "example.learnings.n3", "brand": "example", "section": "learnings", "text": "More."})
        again = router.write("example", self.tmp, TODAY).read_text(encoding="utf-8")
        self.assertIn(f"{router.NOTES_START}\n{notes}\n{router.NOTES_END}", again)
        self.assertIn("| [learnings](learnings.json) | 3 |", again)

    def test_committed_example_brain_md_is_valid(self):
        text = (EXAMPLE / "BRAIN.md").read_text(encoding="utf-8")
        self.assertLessEqual(package.tokens(text), router.MAX_TOKENS)


if __name__ == "__main__":
    unittest.main()
