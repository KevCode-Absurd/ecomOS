"""Tests for app/brain/extract/site.py: both saved fixtures, offline.

No network: fixture mode reads saved responses, and live fetching is patched to fail the test.
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
from app.brain.extract import site  # noqa: E402

FIXTURES = ROOT / "app" / "brain" / "extract" / "fixtures" / "site"
HAND = ROOT / "app" / "brain" / "bombas" / "raw" / "a-site"
CHECKED = ["identity", "products", "offers", "policies", "claims"]


def _strings(v):
    if isinstance(v, str):
        yield v
    elif isinstance(v, list):
        for x in v:
            yield from _strings(x)
    elif isinstance(v, dict):
        for x in v.values():
            yield from _strings(x)


def _no_network(*a, **k):
    raise AssertionError("fixture mode must not touch the network")


class SiteFixtures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out = Path(cls.tmp.name)
        cls.runs = {}
        with mock.patch("urllib.request.urlopen", _no_network):
            for brand, url in (("bombas", "https://shop.bombas.com"), ("woo-sample", "https://woo-sample.example")):
                cls.runs[brand] = site.run(brand, url, cls.out, fixture=FIXTURES / brand)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def folder(self, brand):
        return self.out / brand / "raw" / "a-site"

    def test_files_written_and_valid(self):
        for brand in self.runs:
            for s in site.SECTIONS + ["sources"]:
                self.assertTrue((self.folder(brand) / f"{s}.json").exists(), f"{brand} {s}")
            self.assertEqual(validate.check_path(self.folder(brand)), [], brand)

    def test_every_record_has_url_date_tier(self):
        for brand, res in self.runs.items():
            n = 0
            for s in site.SECTIONS:
                for r in res[s]:
                    n += 1
                    self.assertTrue(r["source"]["ref"].startswith("https://"), r["id"])
                    self.assertRegex(r["source"]["captured_at"], r"^\d{4}-\d{2}-\d{2}$")
                    self.assertEqual((r["tier"], r["visibility"], r["section"]), ("site_backed", "public", s))
                    for e in r.get("evidence", []):
                        self.assertTrue(e["ref"].startswith("https://"), r["id"])
            self.assertGreater(n, 30 if brand == "bombas" else 20, brand)

    def test_no_text_over_300_chars(self):
        for brand, res in self.runs.items():
            for s in site.SECTIONS:
                for r in res[s]:
                    for text in _strings(r):
                        self.assertLessEqual(len(text), 300, f"{r['id']}: {text[:60]}")
                    for e in r.get("evidence", []):
                        self.assertLessEqual(len(e["quote"]), site.MAX_QUOTE, r["id"])

    def test_bombas_reproduces_hand_crawl(self):
        """At least 80 percent of the fields S1.3a wrote by hand, per section and overall."""
        total = hit = 0
        for s in CHECKED:
            hand = {r["field"] for r in json.loads((HAND / f"{s}.json").read_text(encoding="utf-8"))}
            got = {r["field"] for r in self.runs["bombas"][s]}
            total, hit = total + len(hand), hit + len(hand & got)
            self.assertGreaterEqual(len(hand & got) / len(hand), 0.8, f"{s}: missing {sorted(hand - got)}")
        self.assertGreaterEqual(hit / total, 0.8)

    def test_bombas_values_match_hand_crawl(self):
        hand = {r["id"]: r["value"] for s in CHECKED for r in json.loads((HAND / f"{s}.json").read_text(encoding="utf-8"))}
        got = {r["id"]: r["value"] for s in CHECKED for r in self.runs["bombas"][s]}
        for rid in ("bombas.offers.free_shipping_threshold_usd", "bombas.policies.returns_window_days",
                    "bombas.policies.privacy_effective_date", "bombas.policies.terms_effective_date",
                    "bombas.policies.terms_liability_cap", "bombas.identity.certification_bcorp",
                    "bombas.products.price_ladder_socks", "bombas.identity.category"):
            self.assertEqual(got[rid], hand[rid], rid)

    def test_quotes_are_verbatim(self):
        """Evidence quotes are short substrings of the page they cite, never rewritten copy."""
        pages = {}
        for brand in self.runs:
            idx = json.loads((FIXTURES / brand / "index.json").read_text(encoding="utf-8"))
            for url, hit in idx["responses"].items():
                if hit["kind"] == "page":
                    raw = (FIXTURES / brand / hit["file"]).read_text(encoding="utf-8")
                    pages[url] = site.Page(url, raw).text
        checked = 0
        for brand, res in self.runs.items():
            for s in site.SECTIONS:
                for r in res[s]:
                    for e in r.get("evidence", []):
                        if e["ref"] in pages and not e["quote"].startswith(("--", '"', "<")):
                            self.assertIn(site.clean(e["quote"]), pages[e["ref"]], r["id"])
                            checked += 1
        self.assertGreater(checked, 15)

    def test_woo_is_not_shopify(self):
        res = self.runs["woo-sample"]
        self.assertEqual(res["stack"][0]["value"], "woocommerce")
        fields = {s: {r["field"] for r in res[s]} for s in site.SECTIONS}
        self.assertIn("price_ladder_candles", fields["products"])
        self.assertEqual(next(r for r in res["products"] if r["field"] == "gift_card")["value"]["denominations_usd"], [25, 100])
        self.assertEqual(next(r for r in res["offers"] if r["field"] == "free_shipping_threshold_usd")["value"], 60)
        self.assertEqual(next(r for r in res["policies"] if r["field"] == "returns_window_days")["value"], 45)
        self.assertIn("glow_guarantee", fields["policies"])
        self.assertIn("cedar_porch_candle_benefit", fields["claims"])
        self.assertIn("logo_colors", fields["visual"])
        self.assertTrue({"sentence_length_avg", "reading_grade", "person", "recurring_words"} <= fields["voice"])
        self.assertFalse(any("my-account" in x["url"] for x in res["sources"]), "robots-disallowed page fetched")

    def test_sources_list_every_read(self):
        for brand, res in self.runs.items():
            urls = {x["url"] for x in res["sources"]}
            self.assertIn(site.Fetcher(res["sources"][0]["url"]).url("/robots.txt").replace("/robots.txt/robots.txt", "/robots.txt"), urls)
            for s in site.SECTIONS:
                for r in res[s]:
                    if r["source"]["ref"].split("?")[0].endswith((".png", ".svg", ".ico")):
                        continue
                    self.assertTrue(any(r["source"]["ref"].split("?")[0] == u.split("?")[0] or r["source"]["ref"] in u
                                        or r["source"]["ref"].startswith(u.rstrip("/")) for u in urls), r["id"])


class Politeness(unittest.TestCase):
    def test_robots_longest_match(self):
        rb = site.Robots("User-agent: *\nAllow: /\nDisallow: /cart/\nDisallow: /*/checkout\nAllow: /cart/share\n"
                         "Sitemap: https://x.example/sitemap.xml\n")
        self.assertTrue(rb.allowed("https://x.example/products/a"))
        self.assertFalse(rb.allowed("https://x.example/cart/1"))
        self.assertTrue(rb.allowed("https://x.example/cart/share"))
        self.assertFalse(rb.allowed("https://x.example/en/checkout"))
        self.assertEqual(rb.sitemaps, ["https://x.example/sitemap.xml"])

    def test_one_host_and_page_cap(self):
        f = site.Fetcher("https://x.example", max_pages=1)
        with mock.patch.object(site.Fetcher, "_fetch", return_value=(200, "text/html", b"<html></html>")):
            with self.assertRaises(site.Budget):
                f.get("https://other.example/", "page")
            f.get("/", "page")
            with self.assertRaises(site.Budget):
                f.get("/about", "page")
        self.assertIn("ecomOS", site.USER_AGENT)

    def test_fixture_size(self):
        size = sum(p.stat().st_size for p in (FIXTURES / "bombas").iterdir())
        self.assertLess(size, 3_000_000)


if __name__ == "__main__":
    unittest.main()
