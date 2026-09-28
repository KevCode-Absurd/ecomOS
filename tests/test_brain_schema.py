import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app" / "brain"))
import validate  # noqa: E402

EXAMPLE = ROOT / "app" / "brain" / "example"


def good():
    return json.loads((EXAMPLE / "offers.json").read_text(encoding="utf-8"))[0]


class BrainSchemaTests(unittest.TestCase):
    def test_example_folder_is_valid(self):
        self.assertEqual(validate.check_path(EXAMPLE), [])

    def test_missing_source_is_rejected(self):
        rec = good()
        del rec["source"]
        self.assertTrue(any("missing source" in e for e in validate.check_record(rec)))

    def test_missing_date_is_rejected(self):
        rec = good()
        rec["source"].pop("captured_at")
        self.assertTrue(any("captured_at" in e for e in validate.check_record(rec)))

    def test_em_dash_is_rejected(self):
        rec = good()
        rec["text"] = "Free shipping — over $50"
        self.assertTrue(any("em dash" in e for e in validate.check_record(rec)))

    def test_inferred_needs_derived_from(self):
        rec = good()
        rec["source"] = {"type": "inferred", "ref": "site copy", "captured_at": "2026-09-28"}
        rec["tier"] = "inferred"
        self.assertTrue(any("derived_from" in e for e in validate.check_record(rec)))

    def test_approved_needs_founder_source(self):
        rec = good()
        rec["tier"] = "approved"
        self.assertTrue(any("approved" in e for e in validate.check_record(rec)))

    def test_two_active_scalars_for_one_field_is_rejected(self):
        recs = [good(), copy.deepcopy(good())]
        recs[1]["id"] = "example.offers.free_shipping_threshold_usd.2"
        tmp = EXAMPLE.parent / "_tmp_offers"
        tmp.mkdir(exist_ok=True)
        p = tmp / "offers.json"
        p.write_text(json.dumps(recs), encoding="utf-8")
        try:
            errs = validate.check_path(tmp)
        finally:
            p.unlink()
            tmp.rmdir()
        self.assertTrue(any("2 active records" in e for e in errs))

    def test_section_file_name_must_match(self):
        rec = good()
        errs = validate.check_record(rec, expect_section="avatars")
        self.assertTrue(any("in file for avatars" in e for e in errs))


if __name__ == "__main__":
    unittest.main()
