import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.brain.extract import amazon_discover as ad  # noqa: E402
from app.connectors import apify  # noqa: E402

FIX = ROOT / "app" / "brain" / "extract" / "fixtures" / "amazon_discover"
CONFIG = ROOT / "app" / "brain" / "bombas" / "config" / "apify.json"
KNOWN = ["B08CS397JX", "B07PXFBWWG", "B0CVLKH8M2", "B0CW1N66K7", "B087VB376Y",
         "B087JLQF85", "B07SVGLWNY", "B0GZHN33K8", "B07GVF5SS3", "B0D9MSP1S3"]


def no_network(*a, **k):
    raise AssertionError("network call in mock mode")


class DiscoverTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.config = json.loads(CONFIG.read_text(encoding="utf-8"))
        self.log = self.tmp / "runs.jsonl"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def client(self, **kw):
        return apify.ApifyClient(mode="mock", brand="bombas", budget=self.config["budget"],
                                 fixtures_dir=FIX / "bombas", log_path=self.log, **kw)

    def run_bombas(self, **kw):
        with mock.patch("urllib.request.urlopen", no_network):
            return ad.run("bombas", "Bombas", self.config, mode="mock", out=self.tmp, client=self.client(),
                          captured_at="2026-09-28", **kw)

    def test_fixture_yields_known_asins_ranked_decoys_dropped(self):
        res = self.run_bombas()
        self.assertEqual(sorted(res["asins"]), sorted(KNOWN))
        recs = json.loads((self.tmp / "bombas" / "raw" / "amazon-discover" / "marketplaces.json").read_text())
        counts = {r["value"]["asin"]: r["value"]["review_count"] for r in recs}
        self.assertEqual(res["asins"], sorted(KNOWN, key=lambda a: -counts[a]))
        self.assertFalse(any(a.startswith("B0DECOY") for a in counts))
        search = res["steps"][-1]
        self.assertEqual((search["step"], search["found"], search["dropped"]), ("search_actor", 10, 5))
        rec = next(r for r in recs if r["value"]["asin"] == "B087VB376Y")
        self.assertEqual(rec["section"], "marketplaces")
        for key in ("asin", "title", "line", "rating", "review_count", "price", "availability", "seller"):
            self.assertIn(key, rec["value"])
        self.assertEqual(rec["value"]["line"], "no_show")
        self.assertEqual(rec["notes"], "fixture data, not scraped")

    def test_brand_filter_uses_field_then_title(self):
        self.assertFalse(ad.is_brand({"brand_field": "Hanes", "title": "Bombas style socks"}, "Bombas"))
        self.assertTrue(ad.is_brand({"brand_field": "BOMBAS", "title": "Crew socks"}, "Bombas"))
        self.assertFalse(ad.is_brand({"title": "Bomba Co Athletic Socks"}, "Bombas"))
        self.assertTrue(ad.is_brand({"title": "Bombas Men's Calf Socks"}, "Bombas"))

    def test_rank_keeps_top_and_backlog(self):
        found = {f"B00000000{i}": {"asin": f"B00000000{i}", "review_count": i * 10, "found_by": ["x"]} for i in range(3)}
        top, backlog = ad.rank(found, ["B0EXISTING"], keep=2)
        self.assertEqual(top, ["B000000002", "B000000001"])
        self.assertEqual(backlog, ["B000000000", "B0EXISTING"])

    def test_search_estimate_under_one_dollar_and_51st_refused(self):
        self.assertLess(apify.estimate_usd(ad.SEARCH_ACTOR, 50), 1.00)
        with self.assertRaises(apify.ApifyCapError):
            ad.search(self.client(), "Bombas", "com", results=51)
        # The dollar cap holds even when the caller asks for more.
        res = ad.search(self.client(), "Bombas", "com", results=50, max_usd=5.00)
        self.assertEqual(res["cap_usd"], 1.00)
        with self.assertRaises(ad.DiscoverError):
            ad.search(self.client(), "Bombas", "com", actor="junglee~amazon-crawler")

    def test_login_walled_store_page_is_unavailable_and_falls_through(self):
        res = self.run_bombas()
        store = next(s for s in res["steps"] if s["step"] == "store_page")
        self.assertEqual(store["status"], "unavailable")
        self.assertEqual(store["reason"], "sign-in page")
        self.assertEqual(res["steps"][-1]["step"], "search_actor")
        sources = json.loads((self.tmp / "bombas" / "raw" / "amazon-discover" / "sources.json").read_text())
        self.assertIn("sign-in page", [s.get("reason") for s in sources])

    def test_open_store_page_and_site_links_stop_before_the_actor(self):
        links = ad.site_links([(FIX / "sample" / "site-with-amazon.html").read_text()])
        self.assertEqual(links["asins"], ["B0SAMPLE01", "B0SAMPLE03"])
        self.assertTrue(links["store_urls"][0].startswith("https://www.amazon.com/stores/SampleBrand/"))
        self.assertEqual(links["short_links"], ["https://amzn.to/3xYzAbC"])
        page = (FIX / "sample" / "store-page-open.html").read_text()
        res = ad.store_page("https://www.amazon.com/stores/x", lambda url: {"status": 200, "final_url": url, "html": page})
        self.assertEqual(res["status"], "ok")
        self.assertEqual([(i["asin"], i["review_count"]) for i in res["items"]], [("B0SAMPLE01", 1234), ("B0SAMPLE02", 87)])
        cfg = {"budget": self.config["budget"], "amazon_reviews": {"asins": [], "discovery": {"enough": 2}}}
        client = self.client()
        with mock.patch("urllib.request.urlopen", no_network):
            out = ad.run("sample", "Sample Brand", cfg, mode="mock", site=FIX / "sample" / "site-with-amazon.html",
                         out=self.tmp, client=client, fetch=lambda url: {"status": 200, "final_url": url, "html": page},
                         captured_at="2026-09-28")
        self.assertEqual([s["step"] for s in out["steps"]], ["site", "store_page"])
        self.assertIsNone(client.last_run)
        self.assertEqual(out["asins"], ["B0SAMPLE01", "B0SAMPLE02", "B0SAMPLE03"])

    def test_config_write_is_idempotent(self):
        first = self.run_bombas()
        path = Path(first["config"])
        before = path.read_bytes()
        second = self.run_bombas()
        self.assertTrue(first["config_changed"])
        self.assertFalse(second["config_changed"])
        self.assertEqual(before, path.read_bytes())
        written = json.loads(before)["amazon_reviews"]
        self.assertEqual(written["asins_backlog"], [])
        self.assertEqual(written["stars_first"], [5, 1])

    def test_mock_mode_makes_no_network_call(self):
        with mock.patch("urllib.request.urlopen", no_network):
            res = ad.run("bombas", "Bombas", self.config, mode="mock", out=self.tmp, captured_at="2026-09-28",
                         client=self.client())
        self.assertEqual(len(res["asins"]), 10)
        with self.assertRaises(ad.DiscoverError):
            ad.run("bombas", "Bombas", self.config, mode="mock", site="https://shop.bombas.com", out=self.tmp)


if __name__ == "__main__":
    unittest.main()
