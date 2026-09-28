import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app" / "brain"))
import package  # noqa: E402
import validate  # noqa: E402

CATALOGUE = json.loads((ROOT / "agents" / "catalogue.json").read_text(encoding="utf-8"))
OVERLAY = json.loads((ROOT / "app" / "brain" / "capabilities.overlay.json").read_text(encoding="utf-8"))


class OverlayCoverageTests(unittest.TestCase):
    def test_every_capability_has_an_entry(self):
        missing = [c["id"] for c in CATALOGUE if c["id"] not in OVERLAY]
        self.assertEqual(missing, [], f"{len(missing)} capabilities missing from the overlay")

    def test_no_entry_for_an_unknown_capability(self):
        ids = {c["id"] for c in CATALOGUE}
        extra = [cid for cid in OVERLAY if cid not in ids]
        self.assertEqual(extra, [], f"overlay ids not in the catalogue: {extra}")

    def test_every_entry_has_sections_tiers_budget_and_public_facing(self):
        for cid, entry in OVERLAY.items():
            sections = entry.get("brain_sections")
            self.assertIsInstance(sections, dict, cid)
            self.assertTrue(sections, f"{cid} names no brain_sections")
            for sec, tier in sections.items():
                self.assertIn(tier, ("T1", "T2"), f"{cid}.{sec} has tier {tier!r}")
            self.assertIsInstance(entry.get("brain_budget"), int, cid)
            self.assertGreater(entry["brain_budget"], 0, cid)
            self.assertIsInstance(entry.get("public_facing"), bool, cid)

    def test_every_named_section_exists_in_the_schema(self):
        unknown = sorted({sec for entry in OVERLAY.values() for sec in entry["brain_sections"]
                           if sec not in validate.SECTIONS})
        self.assertEqual(unknown, [], f"overlay names sections the schema does not have: {unknown}")

    def test_package_resolve_returns_the_overlay_entry(self):
        for cid in ("CREA-C03", "MONEY-C04", "SITE-C39", "ORCH-C01"):
            resolved = package.resolve(cid)
            self.assertEqual(resolved["id"], cid)
            self.assertEqual(resolved["brain_sections"], OVERLAY[cid]["brain_sections"])
            self.assertEqual(resolved["brain_budget"], OVERLAY[cid]["brain_budget"])
            self.assertEqual(resolved["public_facing"], OVERLAY[cid]["public_facing"])

    def test_package_resolve_rejects_unknown_capability(self):
        with self.assertRaises(KeyError):
            package.resolve("NOPE-C99")


if __name__ == "__main__":
    unittest.main()
