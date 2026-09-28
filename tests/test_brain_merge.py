"""Tests for app/brain/merge.py: site wins, losers kept in history, conflicts raised, list dedupe."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app" / "brain"))

import merge  # noqa: E402
import validate  # noqa: E402

TODAY = "2026-09-28"


def rec(rid, field, value, stype, conf=None, section="offers", text=None, ref=None):
    r = {"id": f"acme.{section}.{rid}", "brand": "acme", "section": section, "field": field, "value": value,
         "text": text or f"{field} is {value}.",
         "source": {"type": stype, "ref": ref or f"https://{stype}.example/{rid}", "captured_at": "2026-09-01"}}
    if conf is not None:
        r["confidence"] = conf
    return r


class MergeRules(unittest.TestCase):
    def test_site_wins_over_press_and_review(self):
        raw = [rec("threshold_press", "free_shipping_usd", 50, "press", 0.9),
               rec("threshold_site", "free_shipping_usd", 75, "site", 0.8),
               rec("threshold_review", "free_shipping_usd", 60, "review", 0.9)]
        merged, _ = merge.merge_records(raw, TODAY)
        active = [r for r in merged if r["field"] == "free_shipping_usd"]
        self.assertEqual(len(active), 1)
        self.assertEqual(active[0]["value"], 75)
        self.assertEqual(active[0]["id"], "acme.offers.threshold_site")

    def test_founder_wins_over_site(self):
        raw = [rec("a", "free_shipping_usd", 75, "site", 0.95), rec("b", "free_shipping_usd", 99, "founder")]
        merged, _ = merge.merge_records(raw, TODAY)
        self.assertEqual([r["value"] for r in merged], [99])
        self.assertEqual(merged[0]["confidence"], 1.0)

    def test_losers_kept_in_history(self):
        raw = [rec("press", "free_shipping_usd", 50, "press"), rec("site", "free_shipping_usd", 75, "site")]
        merged, _ = merge.merge_records(raw, TODAY)
        hist = merged[0]["history"]
        self.assertEqual(len(hist), 1)
        self.assertEqual(hist[0]["value"], 50)
        self.assertEqual(hist[0]["record_id"], "acme.offers.press")
        self.assertEqual(hist[0]["source_type"], "press")
        self.assertIn("changed_at", hist[0])

    def test_conflict_raised_with_both_values(self):
        raw = [rec("press", "free_shipping_usd", 50, "press"), rec("site", "free_shipping_usd", 75, "site")]
        merged, conflicts = merge.merge_records(raw, TODAY)
        self.assertEqual(len(conflicts), 1)
        c = conflicts[0]
        self.assertEqual((c["section"], c["field"], c["status"], c["kept"]),
                         ("offers", "free_shipping_usd", "open", "acme.offers.site"))
        self.assertEqual(sorted(v["value"] for v in c["values"]), [50, 75])
        self.assertIn("Conflict", merged[0]["notes"])

    def test_agreement_raises_confidence_and_no_conflict(self):
        raw = [rec("site", "free_shipping_usd", 75, "site", 0.8), rec("press", "free_shipping_usd", 75.0, "press", 0.6)]
        merged, conflicts = merge.merge_records(raw, TODAY)
        self.assertEqual(conflicts, [])
        self.assertEqual(merged[0]["confidence"], 0.85)
        self.assertEqual(merged[0]["history"][0]["reason"], "agrees")

    def test_conflict_lowers_confidence(self):
        raw = [rec("site", "free_shipping_usd", 75, "site", 0.8), rec("press", "free_shipping_usd", 50, "press")]
        merged, _ = merge.merge_records(raw, TODAY)
        self.assertEqual(merged[0]["confidence"], 0.7)

    def test_list_items_deduped_by_text(self):
        a = rec("heel_1", "issue", {"issue": "hole in the heel"}, "review", section="products",
                text="Socks get a hole in the heel within weeks.")
        b = rec("heel_2", "issue", {"issue": "hole in the heel"}, "press", section="products",
                text="Socks get a hole in the heel within a few weeks.")
        c = rec("slip", "issue", {"issue": "no show socks slip"}, "review", section="products",
                text="No show socks slip down into the shoe.")
        merged, conflicts = merge.merge_records([a, b, c], TODAY)
        self.assertEqual(conflicts, [])
        self.assertEqual(len(merged), 2)
        kept = next(r for r in merged if "heel" in r["id"])
        self.assertEqual(kept["id"], "acme.products.heel_2")  # press ranks above review
        self.assertEqual(kept["history"][0]["reason"], "near duplicate")

    def test_templated_items_with_different_values_stay_apart(self):
        a = rec("p1", "phrase", {"phrase": "hole in the heel"}, "review", section="language_bank",
                text="Customers use language like 'hole in the heel' when describing a complaint.")
        b = rec("p2", "phrase", {"phrase": "shedding and pilling"}, "review", section="language_bank",
                text="Customers use language like 'shedding and pilling' when describing a complaint.")
        merged, _ = merge.merge_records([a, b], TODAY)
        self.assertEqual(len(merged), 2)

    def test_inputs_not_changed(self):
        raw = [rec("press", "x", 1, "press"), rec("site", "x", 2, "site")]
        before = json.dumps(raw, sort_keys=True)
        merge.merge_records(raw, TODAY)
        self.assertEqual(json.dumps(raw, sort_keys=True), before)


class MergeRun(unittest.TestCase):
    def test_run_writes_valid_brain(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for folder, recs, srcs in [
                ("a-site", [rec("site", "free_shipping_usd", 75, "site")], [{"url": "https://s", "date": TODAY}]),
                ("c-press", [rec("press", "free_shipping_usd", 50, "press")],
                 [{"url": "https://s", "captured_at": TODAY, "source_type": "press"}, {"url": "https://p", "captured_at": TODAY}]),
            ]:
                d = root / "acme" / "raw" / folder
                d.mkdir(parents=True)
                (d / "offers.json").write_text(json.dumps(recs))
                (d / "sources.json").write_text(json.dumps(srcs))
            out = merge.run("acme", root, TODAY, publish=False)
            self.assertEqual(out["conflicts"], 1)
            brain = root / "acme"
            self.assertEqual(validate.check_path(brain), [])
            sources = json.loads((brain / "sources.json").read_text())
            self.assertEqual(len(sources), 2)
            self.assertEqual(sources[0]["extractors"], ["a-site", "c-press"])
            fresh = json.loads((brain / "freshness.json").read_text())
            self.assertEqual(fresh[0]["value"]["conflict_count"], 1)
            self.assertEqual(len(json.loads((brain / "review" / "conflicts.json").read_text())), 1)


class BombasBrain(unittest.TestCase):
    """The published Bombas brain holds its merge promises."""
    DIR = ROOT / "app" / "brain" / "bombas"

    def test_validates(self):
        self.assertEqual(validate.check_path(self.DIR), [])

    def test_calibration_fields_filled_or_open(self):
        fields = {a["field"]: a for a in json.loads((self.DIR / "assumptions.json").read_text())}
        for f in ("revenue_band", "aov_usd", "repeat_rate_12m", "channel_mix", "seasonality", "giving_units", "retail_partners"):
            self.assertIn(f, fields)
            self.assertIn(fields[f]["status"], ("sourced", "derived", "assumed"))
            self.assertTrue(fields[f]["reasoning"])
        open_q = {q["field"] for q in json.loads((self.DIR / "open_questions.json").read_text())}
        for f, a in fields.items():
            if a["status"] == "assumed":
                self.assertTrue(any(q in a["reasoning"] or q in f for q in open_q), f)


if __name__ == "__main__":
    unittest.main()
