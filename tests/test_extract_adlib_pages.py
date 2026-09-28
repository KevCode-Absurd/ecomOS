import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.brain.extract import adlib_pages, apify_adlibrary  # noqa: E402

FIX = ROOT / "app" / "brain" / "extract" / "fixtures" / "adlib"
BRAIN = ROOT / "app" / "brain"
CONFIG = BRAIN / "bombas" / "config" / "apify.json"
BOMBAS_ID = "155577444523958"


def bombas_html():
    return [(FIX / "bombas-shop-header-footer.html").read_text(encoding="utf-8")]


class OwnPageTests(unittest.TestCase):
    def setUp(self):
        self.records = adlib_pages.load_brain("bombas", BRAIN)
        self.known = adlib_pages.load_known(None, self.records)

    def test_bombas_fixture_resolves_own_page_id(self):
        own = adlib_pages.find_own_page("Bombas", bombas_html(), self.known, adlib_pages.fixture_fetch())
        self.assertEqual(own["page_id"], BOMBAS_ID)
        # The saved shop host carries no Facebook link, so the id comes from the 28 Sep known ids.
        self.assertEqual(own["site_links"], [])
        self.assertTrue(own["found_by"].startswith("known ids"))

    def test_site_link_is_used_and_name_is_confirmed(self):
        html = [(FIX / "sample-site" / "index.html").read_text(encoding="utf-8")]
        links = adlib_pages.site_links(html)
        self.assertEqual(links[0]["where"], "json-ld sameAs")
        self.assertFalse(any("sharer" in l["url"] or "privacy" in l["url"] for l in links))
        own = adlib_pages.find_own_page("Trailhead Socks", html, self.known)
        self.assertEqual(own["page_id"], "123456789012345")
        self.assertTrue(own["found_by"].startswith("site"))
        # A link whose page name is another brand is not taken as the brand's own page.
        other = adlib_pages.find_own_page("Trailhead Outfitters", html, {"pages": [], "never": set()})
        self.assertIsNone(other["page_id"])

    def test_page_search_keeps_only_exact_name(self):
        fetch = adlib_pages.fixture_fetch()
        res = adlib_pages.search_page("Stance", fetch, {"pages": [], "never": set()})
        self.assertEqual(res["status"], "found")
        self.assertEqual(res["page_id"], "900000000000003")  # "STANCE " matches, case and spaces aside
        self.assertIn("Stance Auto", res["rejected"])
        text = json.dumps({"page_results": [{"page_id": "1", "name": "Stance Auto"}]})
        only_near = adlib_pages.search_page("Stance", lambda u, n: (200, text), {"pages": [], "never": set()})
        self.assertEqual(only_near["status"], "none")
        self.assertIsNone(only_near.get("page_id"))
        self.assertFalse(adlib_pages.exact("Stance Auto", "Stance"))
        self.assertFalse(adlib_pages.same_brand("Stance Auto", "Stance"))
        self.assertTrue(adlib_pages.same_brand("Darn Tough Vermont Socks", "Darn Tough"))

    def test_page_search_challenge_is_reported_unavailable(self):
        res = adlib_pages.search_page("Allbirds", adlib_pages.fixture_fetch(), {"pages": [], "never": set()})
        self.assertEqual(res["status"], "unavailable")
        self.assertIn("founder pastes", res["why"])


class ProposalTests(unittest.TestCase):
    def test_proposal_names_reasons_and_record_ids(self):
        records = adlib_pages.load_brain("bombas", BRAIN)
        ids = {r["id"] for r in records}
        props = adlib_pages.propose("Bombas", records)
        self.assertLessEqual(len(props), 15)
        by_key = {adlib_pages.key(p["name"]): p for p in props}
        for want in ("Darn Tough", "Stance", "Comrad"):
            p = by_key.get(adlib_pages.key(want))
            self.assertIsNotNone(p, want)
            self.assertTrue(p["reasons"])
            for r in p["reasons"]:
                self.assertIn(r["record"], ids)
        self.assertNotIn("bombas", by_key)
        self.assertFalse(any(p.get("page_id") == "109559148587404" for p in props))  # the lookalike page
        scores = [p["score"] for p in props]
        self.assertEqual(scores, sorted(scores, reverse=True))


class ConfigTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.cfg = self.tmp / "apify.json"
        shutil.copy(CONFIG, self.cfg)
        self.records = adlib_pages.load_brain("bombas", BRAIN)
        self.known = adlib_pages.load_known(None, self.records)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def write(self, confirm=None, own=None):
        props = adlib_pages.propose("Bombas", self.records)
        return adlib_pages.write_config(self.cfg, own, props, self.known, adlib_pages.fixture_fetch(), confirm)

    def test_write_is_idempotent(self):
        self.write()
        first = self.cfg.read_bytes()
        res = self.write()
        self.assertFalse(res["changed"])
        self.assertEqual(self.cfg.read_bytes(), first)

    def test_own_page_written_as_self_and_confirm_moves_proposals(self):
        cfg = json.loads(self.cfg.read_text())
        cfg["meta_ad_library"]["pages"] = [p for p in cfg["meta_ad_library"]["pages"] if p["name"] != "Bombas"]
        cfg["meta_ad_library"]["pages"] = cfg["meta_ad_library"]["pages"][:2]
        self.cfg.write_text(json.dumps(cfg))
        own = adlib_pages.find_own_page("Bombas", bombas_html(), self.known)
        self.write(own=own)
        mal = json.loads(self.cfg.read_text())["meta_ad_library"]
        self.assertEqual(mal["pages"][0], {"name": "Bombas", "role": "self", "page_id": BOMBAS_ID,
                                           "found_by": own["found_by"]})
        names = [p["name"] for p in mal["proposed_pages"]]
        self.assertIn("Comrad Socks", names)
        self.assertTrue(all(p["role"] == "proposed" for p in mal["proposed_pages"]))
        res = self.write(confirm=["Comrad", "Nobody Brand"])
        mal = json.loads(self.cfg.read_text())["meta_ad_library"]
        self.assertEqual(res["confirmed"], ["Comrad Socks"])
        self.assertEqual(res["not_found"], ["Nobody Brand"])
        comrad = next(p for p in mal["pages"] if p["name"] == "Comrad Socks")
        self.assertEqual((comrad["role"], comrad["page_id"]), ("competitor", "1156330774456653"))
        self.assertNotIn("Comrad Socks", [p["name"] for p in mal["proposed_pages"]])


class FakeClient:
    mode = "mock"

    def __init__(self):
        import datetime as dt
        self.today = dt.date(2026, 9, 28)
        self.input = None
        self.last_run = {"run_id": "fixture"}

    def run(self, actor, actor_input, max_items, lane=None):
        self.input = actor_input
        return []


class AdlibraryRunTests(unittest.TestCase):
    def test_mock_run_builds_page_id_urls_and_ignores_proposals(self):
        cfg = json.loads(CONFIG.read_text())
        cfg["meta_ad_library"]["proposed_pages"] = [{"name": "Kirkland", "role": "proposed", "page_id": "42"}]
        client = FakeClient()
        with tempfile.TemporaryDirectory() as tmp:
            apify_adlibrary.run("bombas", cfg, client=client, root=tmp, captured_at="2026-09-28")
        urls = [u["url"] for u in client.input["urls"]]
        for p in cfg["meta_ad_library"]["pages"]:
            if p.get("page_id"):
                self.assertTrue(any(f"view_all_page_id={p['page_id']}" in u for u in urls), p["name"])
        self.assertFalse(any("view_all_page_id=42" in u for u in urls))
        self.assertFalse(any("keyword" in u for u in urls))


if __name__ == "__main__":
    unittest.main()
