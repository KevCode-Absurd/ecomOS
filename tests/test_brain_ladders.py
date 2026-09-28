"""Tests for app/brain/ladders.py: themes, rung order, counts by source, proof lookup, empty lanes."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app" / "brain"))

import ladders  # noqa: E402
import validate  # noqa: E402

TODAY = "2026-09-28"


def review(star, quote, source="own_site_yotpo", url="https://acme.com/products/sock"):
    return {"star": star, "quote": quote, "source": source, "url": url}


def rec(field, section, value, text="review record"):
    return {"id": f"acme.{section}.{field}", "brand": "acme", "section": section, "field": field, "value": value,
            "text": text, "source": {"type": "review", "ref": "https://acme.com/reviews", "captured_at": TODAY},
            "tier": "evidence"}


def lanes():
    return {"f-reviews": [
        rec("heel_holes", "objections", {"objection": "Socks wear out", "reviews": [
            review(1, "Hole in the heel after 2 wears."),
            review(1, "Started pilling after one day.", source="amazon_customers_say", url=None),
            review(5, "Two years and still no holes, so durable."),
        ]}),
        rec("stay_up", "language_bank", {"theme": "result", "phrase": "they stay in place", "reviews": [
            review(5, "They stay in place all day.", source="retailer", url="https://www.target.com/p/x"),
            review(None, "These slide down my heel constantly, disappointed.", source=None,
                   url="https://www.trustpilot.com/review/acme.com"),
        ]}),
    ], "d-public": [
        {"id": "acme.language_bank.price", "brand": "acme", "section": "language_bank", "field": "phrase",
         "value": {"theme": "complaint", "phrase": "not worth the price"}, "text": "not worth the price",
         "source": {"type": "review", "ref": "https://www.trustpilot.com/review/acme.com", "captured_at": TODAY},
         "evidence": [{"quote": "Not worth the price, cheaper socks at Walmart are fine.",
                       "ref": "https://www.trustpilot.com/review/acme.com"},
                      {"quote": "Pricey at $15 a pair.", "ref": "https://www.trustpilot.com/review/acme.com"},
                      {"quote": "Hole in the heel after 2 wears.", "ref": "https://acme.com/products/sock"}]},
    ]}


def sections():
    def site(section, field, text):
        return {"id": f"acme.{section}.{field}", "brand": "acme", "section": section, "field": field, "value": text,
                "text": text, "source": {"type": "site", "ref": "https://acme.com", "captured_at": TODAY}}
    return {"policies": [site("policies", "guarantee", "Acme replaces any pair under the Happiness Guarantee.")],
            "offers": [site("offers", "packs", "Packs carry a per pack price that discounts singles.")],
            "claims": [],
            "avatars": [{"id": "acme.avatars.let_down_loyalist", "brand": "acme", "section": "avatars", "field": "avatar",
                         "value": {"name": "Let down loyalist", "pains": ["holes in the heel", "pilling"]},
                         "text": "Loyal buyer let down by holes."}]}


def build(**kw):
    return ladders.build("acme", kw.get("lanes", lanes()), kw.get("empty", []), sections(), TODAY)


def by_theme(out):
    return {r["value"]["theme"]: r for r in out[0]}


class Ladders(unittest.TestCase):
    def test_theme_grouping(self):
        themes = by_theme(build())
        self.assertIn("durability", themes)
        self.assertIn("fit_and_sizing", themes)
        self.assertIn("price_and_value", themes)
        self.assertEqual(themes["durability"]["id"], "acme.objection_ladders.durability")

    def test_rungs_run_mild_to_deal_breaker(self):
        rungs = by_theme(build())["durability"]["value"]["rungs"]
        levels = [r["level"] for r in rungs]
        self.assertEqual(levels, sorted(levels))
        self.assertEqual(levels, [1, 3])
        self.assertIn("Started pilling after one day.", rungs[0]["one_star"])
        self.assertIn("Hole in the heel after 2 wears.", rungs[-1]["one_star"])
        self.assertIn("Two years and still no holes, so durable.", rungs[-1]["five_star"])

    def test_duplicate_quote_counted_once_with_both_records(self):
        top = by_theme(build())["durability"]["value"]["rungs"][-1]
        self.assertEqual(top["counts"]["one_star"], 1)
        self.assertIn("acme.objections.heel_holes", top["derived_from"])
        self.assertIn("acme.language_bank.price", top["derived_from"])

    def test_counts_by_star_and_source(self):
        dur = by_theme(build())["durability"]["value"]["counts"]
        self.assertEqual(set(ladders.SOURCES) <= set(dur["sources"]), True)
        self.assertEqual(dur["sources"]["own_site"], 2)
        self.assertEqual(dur["sources"]["amazon"], 1)
        self.assertEqual(dur["sources"]["reddit"], 0)
        self.assertEqual(dur["by_star"]["1"], 2)
        self.assertEqual(dur["by_star"]["5"], 1)
        fit = by_theme(build())["fit_and_sizing"]["value"]["counts"]
        self.assertEqual(fit["sources"]["trustpilot"], 1)
        self.assertEqual(fit["sources"]["retailer"], 1)

    def test_unstarred_quote_split_by_sentiment(self):
        fit = by_theme(build())["fit_and_sizing"]["value"]
        self.assertEqual(fit["counts"]["by_star"]["star_unknown"], 1)
        slip = [r for r in fit["rungs"] if r["level"] == 2][0]
        self.assertIn("These slide down my heel constantly, disappointed.", slip["one_star"])

    def test_proof_lookup_and_open_question(self):
        out = build()
        rungs = by_theme(out)["durability"]["value"]["rungs"]
        self.assertEqual(rungs[0]["proof_ids"], ["acme.policies.guarantee"])
        self.assertIn("pdp", rungs[0]["uses"])
        self.assertNotIn("proof_ids", rungs[-1])
        self.assertEqual(rungs[-1]["open_question"], "acme.open_questions.ladder_durability_3")
        self.assertIn("offer", rungs[-1]["uses"])
        self.assertIn("acme.open_questions.ladder_durability_3", [q["id"] for q in out[1]])
        price = by_theme(out)["price_and_value"]["value"]["rungs"]
        self.assertEqual([r["level"] for r in price], [1, 2])
        self.assertEqual(price[0]["proof_ids"], ["acme.offers.packs"])
        self.assertEqual(price[1]["proof_ids"], ["acme.policies.guarantee"])

    def test_avatars_and_amazon_use(self):
        rungs = by_theme(build())["durability"]["value"]["rungs"]
        self.assertIn("acme.avatars.let_down_loyalist", rungs[-1]["avatars"])
        self.assertIn("amazon_listing", rungs[0]["uses"])
        self.assertTrue(all(u in ladders.USES for r in rungs for u in r["uses"]))

    def test_records_validate(self):
        ladder, questions = build()
        for r in ladder + questions:
            self.assertEqual(validate.check_record(r), [], r["id"])
            if r["section"] == "objection_ladders":
                self.assertEqual(r["tier"], "inferred")
                self.assertEqual(r["source"]["type"], "agent")
                self.assertTrue(r["source"]["derived_from"])

    def test_empty_lane_tolerated(self):
        with tempfile.TemporaryDirectory() as tmp:
            brand = Path(tmp) / "acme"
            (brand / "raw" / "h-reddit").mkdir(parents=True)
            (brand / "raw" / "h-reddit" / "sources.json").write_text(
                json.dumps([{"url": "summary://h-reddit", "note": "Blocked at the edge."}]))
            (brand / "raw" / "f-reviews").mkdir()
            for name, recs in (("objections", lanes()["f-reviews"][:1]),):
                (brand / "raw" / "f-reviews" / f"{name}.json").write_text(json.dumps(recs))
            got, empty = ladders.load_lanes(brand)
            self.assertEqual(list(got), ["f-reviews"])
            self.assertEqual(empty, [{"lane": "h-reddit", "note": "Blocked at the edge."}])
            out = ladders.build("acme", got, empty, sections(), TODAY)
            counts = by_theme(out)["durability"]["value"]["counts"]
            self.assertEqual(counts["sources"]["reddit"], 0)
            self.assertEqual(counts["empty_lanes"][0]["lane"], "h-reddit")
        self.assertEqual(ladders.build("acme", {}, [], sections(), TODAY), ([], []))

    def test_no_raw_folder(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(ladders.load_lanes(Path(tmp)), ({}, []))


if __name__ == "__main__":
    unittest.main()
