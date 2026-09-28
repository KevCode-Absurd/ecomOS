"""S4.2a: inspiration puller A (Meta Ad Library -> creative and offers references)."""
from __future__ import annotations

import datetime as dt
import json
import socket
import sys
import tempfile
import unittest
import urllib.request
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.connectors import apify  # noqa: E402
from app.inspiration import media, pull_a, relevance, rights, tag, validate  # noqa: E402

DAY = "2026-09-28"
FIXTURE = ROOT / "app" / "connectors" / "fixtures" / "apify" / "curious_coder~facebook-ads-library-scraper.json"


def _no_network(*a, **k):
    raise AssertionError("network call in mock mode")


class MockRun(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out = Path(cls.tmp.name) / "insp"
        cls.facts = relevance.Facts("bombas")
        client = apify.ApifyClient(mode="mock", brand="bombas", budget={"max_usd_per_run": 4.0},
                                   log_path=Path(cls.tmp.name) / "log.jsonl")
        with mock.patch.object(urllib.request, "urlopen", _no_network), \
                mock.patch.object(socket, "create_connection", _no_network):
            cls.result = pull_a.pull("bombas", "mock", cls.out, client=client, captured_at=DAY, facts=cls.facts)
        cls.creative = json.loads((cls.out / "bombas" / "creative.json").read_text())
        cls.offers = json.loads((cls.out / "bombas" / "offers.json").read_text())
        cls.all = cls.creative + cls.offers

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_references_validate(self):
        self.assertGreaterEqual(len(self.creative), 8)
        self.assertGreaterEqual(len(self.offers), 1)
        for ref in self.all:
            self.assertEqual(validate.errors(ref), [], ref["id"])

    def test_every_connector_fixture_ad_becomes_a_reference(self):
        items = json.loads(FIXTURE.read_text())["items"]
        ids = {r["origin"]["url"] for r in self.creative}
        for it in items:
            self.assertIn(it["url"], ids)

    def test_stray_page_is_filtered(self):
        self.assertNotIn("Sockscool Deals", {r["origin"]["brand"] for r in self.all})

    def test_rights_split(self):
        for ref in self.all:
            if ref["origin"]["brand"] == "Bombas":
                self.assertEqual(ref["origin"]["role"], "own")
                self.assertEqual(ref["media"]["rights"], "own_brand")
            else:
                self.assertEqual(ref["origin"]["role"], "competitor")
                self.assertEqual(ref["media"]["rights"], "reference_only")

    def test_quote_at_most_140(self):
        for ref in self.all:
            self.assertLessEqual(len(ref["quote"]), 140)
        comrad = next(r for r in self.creative if r["origin"]["brand"] == "Comrad Socks")
        full = json.loads(pull_a.EXTRA_FIXTURE.read_text())["items"][0]["snapshot"]["body"]["text"]
        self.assertGreater(len(full), 140)
        self.assertTrue(full.startswith(comrad["quote"]))
        self.assertNotIn(full, json.dumps(self.all))

    def test_mock_media_is_none_with_note(self):
        for ref in self.all:
            self.assertEqual(ref["media"]["kind"], "none")
            self.assertIsNone(ref["media"]["path"])
            self.assertEqual(ref["media"]["note"], pull_a.MOCK_NOTE)
        self.assertEqual(self.result["mode"], "mock")

    def test_tags_format_hook_layout_mood(self):
        for ref in self.creative:
            for k in ("format", "hook_type", "layout", "mood"):
                self.assertTrue(ref["signals"].get(k), (ref["id"], k))

    def test_reasons_cite_real_brain_fields(self):
        brain = self.facts.brain
        fired = 0
        for ref in self.all:
            for r in ref["relevance"]["reasons"]:
                if r["rule"] == "own_brand":
                    continue
                fired += 1
                rec = brain.get(r["record"])
                self.assertIsNotNone(rec, r)
                section = r["record"].split(".")[1]
                self.assertTrue(r["brain_field"].startswith(section), r)
                self.assertTrue(r["match"])
                self.assertTrue(r["sentence"])
                if r["rule"] in ("same_category", "competitor_in_frame", "same_offer_type"):
                    blob = json.dumps(rec["value"]).lower() + " " + rec["id"]
                    self.assertIn(r["match"].lower().rstrip("s"), blob, r)
        self.assertGreater(fired, 5)

    def test_comrad_scores_category_and_frame(self):
        comrad = next(r for r in self.creative if r["origin"]["brand"] == "Comrad Socks")
        rules = {r["rule"] for r in comrad["relevance"]["reasons"]}
        self.assertIn("same_category", rules)
        self.assertIn("competitor_in_frame", rules)
        self.assertGreaterEqual(comrad["relevance"]["score"], 0.4)
        self.assertTrue(comrad["relevance"]["shown"])

    def test_first_order_code_sentence(self):
        own = [r for r in self.all if r["signals"].get("offer_type") == "first_order_code"]
        sentences = [x["sentence"] for r in own for x in r["relevance"]["reasons"] if x["rule"] == "same_offer_type"]
        self.assertIn("Same offer type: a 20 percent first-order code, like COMFORT20", sentences)

    def test_score_capped_and_threshold(self):
        for ref in self.all:
            rel = ref["relevance"]
            self.assertLessEqual(rel["score"], 1.0)
            self.assertEqual(rel["shown"], rel["score"] >= 0.3)
            if ref["origin"]["role"] == "own":
                self.assertEqual(rel["score"], 1.0)
        low = [r for r in self.creative if not r["relevance"]["shown"]]
        self.assertTrue(low, "the new-prints Stance ad should be stored but not shown")


class Rights(unittest.TestCase):
    def ref(self, role):
        return {"id": f"insp.creative.x.{role}", "origin": {"brand": "B", "role": role},
                "media": {"rights": "own_brand" if role == "own" else "reference_only", "files": ["app/inspiration/media/b/x.jpg"],
                          "path": "app/inspiration/media/b/x.jpg", "thumbnail": None}}

    def test_refuses_competitor_accepts_own(self):
        with self.assertRaises(rights.RightsError):
            rights.assert_generation_input(self.ref("competitor"))
        with self.assertRaises(rights.RightsError):
            rights.generation_files(self.ref("leader"))
        self.assertEqual(rights.assert_generation_input(self.ref("own"))["origin"]["role"], "own")
        self.assertEqual(rights.generation_files(self.ref("own")), ["app/inspiration/media/b/x.jpg"])

    def test_mislabelled_rights_refused(self):
        bad = self.ref("competitor")
        bad["media"]["rights"] = "own_brand"
        with self.assertRaises(rights.RightsError):
            rights.assert_generation_input(bad)
        self.assertTrue(any("reference_only" in e for e in validate.errors(bad)))

    def test_path_boundary(self):
        refs = [self.ref("competitor")]
        with self.assertRaises(rights.RightsError):
            rights.assert_generation_path("app/inspiration/media/b/x.jpg", refs)
        with self.assertRaises(rights.RightsError):
            rights.assert_generation_path("app/inspiration/media/b/unknown.jpg", [self.ref("own")])
        self.assertTrue(rights.assert_generation_path("app/inspiration/media/b/x.jpg", [self.ref("own")]))


class LiveModeWithFakes(unittest.TestCase):
    """Live path through the real ApifyClient (caps, ledger) with a fake transport and fake downloads."""

    def test_live_downloads_split_by_rights(self):
        items = json.loads(FIXTURE.read_text())["items"] + json.loads(pull_a.EXTRA_FIXTURE.read_text())["items"]
        calls = []

        def transport(method, url, body, headers, timeout):
            calls.append(url)
            if "run-sync-get-dataset-items" in url:
                return 200, json.dumps(items).encode()
            if "/datasets/" in url:
                return 200, json.dumps(items).encode()
            return 200, json.dumps({"data": {"id": "run-fake", "status": "SUCCEEDED", "defaultDatasetId": "ds-fake",
                                             "usageTotalUsd": 0.12}}).encode()

        fetched = []

        def fetch(url, timeout):
            fetched.append(url)
            if "fixture-image-1" in url:
                raise OSError("expired")
            return ("video/mp4" if url.split("?")[0].endswith(".mp4") else "image/jpeg"), b"x" * 10

        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            client = apify.ApifyClient(token="fake", mode="live", brand="bombas",
                                       budget={"max_usd_per_run": 4.0, "max_usd_per_week": 30.0},
                                       ledger_path=tmp / "spend.sqlite", log_path=tmp / "log.jsonl",
                                       transport=transport, today=dt.date(2026, 9, 28))
            dl = media.Downloader(root=tmp / "media", fetch_fn=fetch, rel_to=tmp)
            res = pull_a.pull("bombas", "live", tmp / "insp", client=client, downloader=dl, captured_at=DAY)
            refs = json.loads((tmp / "insp" / "bombas" / "creative.json").read_text())
            self.assertEqual(res["run_id"], "run-fake")
            self.assertTrue(any("/acts/curious_coder~facebook-ads-library-scraper/" in c for c in calls))
            self.assertIn("apify:bombas", client._ledger().db.execute("SELECT request_id FROM spend").fetchone()[0])
            by = {r["origin"]["url"].split("=")[-1]: r for r in refs}
            own_video = by["900000000000002"]
            self.assertEqual(own_video["media"]["kind"], "video")
            self.assertTrue(own_video["media"]["path"].endswith(".mp4"))
            comp_video = by["900000000000101"]
            self.assertEqual(comp_video["media"]["kind"], "video")
            self.assertIsNone(comp_video["media"]["path"])
            self.assertTrue(comp_video["media"]["thumbnail"].endswith(".jpg"))
            self.assertIn("fixture-video-101.mp4", comp_video["media"]["remote_url"])
            self.assertEqual(comp_video["media"]["expires"], "2026-10-02")
            self.assertFalse(any("fixture-video-101.mp4" in u for u in fetched), "competitor video was downloaded")
            self.assertFalse(any("fixture-video-4.mp4" in u for u in fetched), "competitor video was downloaded")
            gone = by["900000000000001"]
            self.assertEqual(gone["media"]["kind"], "none")
            for r in refs:
                self.assertEqual(validate.errors(r), [], r["id"])
                for f in r["media"]["files"]:
                    self.assertTrue((tmp / f).exists(), f)
                if r["origin"]["role"] != "own":
                    with self.assertRaises(rights.RightsError):
                        rights.generation_files(r)


class Purge(unittest.TestCase):
    def test_purge_removes_origin_records_and_media(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            out, media_root = tmp / "insp", tmp / "media"
            client = apify.ApifyClient(mode="mock", brand="bombas", budget={"max_usd_per_run": 4.0},
                                       log_path=tmp / "log.jsonl")
            pull_a.pull("bombas", "mock", out, client=client, captured_at=DAY)
            folder = media_root / "bombas" / "comrad_socks"
            folder.mkdir(parents=True)
            (folder / "x.jpg").write_bytes(b"x")
            before = json.loads((out / "bombas" / "creative.json").read_text())
            self.assertTrue(any(r["origin"]["brand"] == "Comrad Socks" for r in before))
            res = pull_a.purge("comrad socks", out, media_root=media_root)
            self.assertEqual(res["references_removed"], 2)
            self.assertFalse(folder.exists())
            for d in ("creative", "offers"):
                refs = json.loads((out / "bombas" / f"{d}.json").read_text())
                self.assertFalse(any(r["origin"]["brand"] == "Comrad Socks" for r in refs))
                self.assertTrue(any(r["origin"]["brand"] == "Stance" for r in refs))


class Tagger(unittest.TestCase):
    def test_quote_cut_and_hooks(self):
        self.assertLessEqual(len(tag.quote("word " * 100)), 140)
        self.assertEqual(tag.hook_type("Why do your socks fall down? Ours stay."), "question")
        self.assertEqual(tag.hook_type("I wore these for a shift."), "first_person")
        o = tag.offer("Get 20% off your first order with code COMFORT20.")
        self.assertEqual((o["offer_type"], o["discount_pct"], o["code"]), ("first_order_code", 20.0, "COMFORT20"))
        self.assertEqual(media.url_expiry("https://x/y.jpg?oe=6ABEF400"), "2026-10-02")


if __name__ == "__main__":
    unittest.main()
