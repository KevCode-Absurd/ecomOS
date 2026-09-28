import json
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.brain.extract import stack  # noqa: E402
from app.brain import validate  # noqa: E402

FIXTURE = ROOT / "app" / "brain" / "extract" / "fixtures" / "stack" / "bombas"

# field -> a substring of the vendor name S1.3a found by hand in the 10 Bombas stack records
HAND_FOUND = {
    "platform": "Shopify",
    "theme": "custom React storefront theme",
    "reviews_app": "Yotpo",
    "upsell_app": "Rebuy",
    "tag_manager": "Google Tag Manager",
    "cookie_consent": "OneTrust",
    "ab_testing": "Optimizely",
    "performance_vendor": "Yottaa",
    "form_security": "hCaptcha",
    "agent_commerce_endpoint": "UCP/MCP",
}


class ExtractStackTests(unittest.TestCase):
    def test_signatures_file_has_no_duplicate_ids(self):
        sigs = stack.load_signatures()
        ids = Counter(s["id"] for s in sigs)
        dupes = [i for i, n in ids.items() if n > 1]
        self.assertEqual(dupes, [], f"duplicate signature ids: {dupes}")

    def test_bombas_fixture_reproduces_at_least_8_of_10_hand_found_records(self):
        docs = stack.read_pages(FIXTURE, "https://shop.bombas.com")
        records = stack.run("bombas", docs, "2026-09-28")
        by_field = {r["field"]: r for r in records}
        matched = 0
        for field, expect in HAND_FOUND.items():
            rec = by_field.get(field)
            if rec and expect.lower() in str(rec["value"]).lower():
                matched += 1
        self.assertGreaterEqual(matched, 8, f"only matched {matched} of 10: {sorted(by_field)}")

    def test_every_record_validates(self):
        docs = stack.read_pages(FIXTURE, "https://shop.bombas.com")
        records = stack.run("bombas", docs, "2026-09-28")
        self.assertTrue(records)
        for rec in records:
            errs = validate.check_record(rec, expect_section="stack")
            self.assertEqual(errs, [], f"{rec['id']}: {errs}")

    def test_empty_page_yields_zero_records_and_no_error(self):
        docs = [{"url": "https://example.com/", "text": "<html><body>hello</body></html>", "headers": {}, "cookies": []}]
        records = stack.run("example", docs, "2026-09-28")
        self.assertEqual(records, [])

    def test_no_pages_yields_zero_records_and_no_error(self):
        self.assertEqual(stack.run("example", [], "2026-09-28"), [])

    def test_path_for_file_round_trips_the_url_encoding(self):
        self.assertEqual(stack._path_for_file("index.html"), "/")
        self.assertEqual(stack._path_for_file("collections__mens-socks.html"), "/collections/mens-socks")
        self.assertEqual(stack._path_for_file("robots.txt"), "/robots.txt")

    def test_multi_field_collects_every_distinct_vendor(self):
        text = ("shop-pay-button here, apple-pay-button there, "
                "klarna.com placement, myshopify.com host")
        docs = [{"url": "https://example.com/", "text": text, "headers": {}, "cookies": []}]
        records = stack.run("example", docs, "2026-09-28")
        wallets = next(r for r in records if r["field"] == "payment_wallets")
        self.assertIsInstance(wallets["value"], list)
        self.assertGreaterEqual(len(wallets["value"]), 2)


if __name__ == "__main__":
    unittest.main()
