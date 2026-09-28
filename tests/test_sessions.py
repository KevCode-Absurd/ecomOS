import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SessionRegistryTests(unittest.TestCase):
    def setUp(self):
        self.sessions = json.loads((ROOT / "sessions" / "sessions.json").read_text(encoding="utf-8"))["sessions"]

    def test_ids_unique_and_needs_resolve(self):
        ids = [s["id"] for s in self.sessions]
        self.assertEqual(len(ids), len(set(ids)))
        for s in self.sessions:
            for n in s["needs"]:
                self.assertIn(n, ids, f"{s['id']} needs unknown {n}")

    def test_every_session_has_a_card(self):
        for s in self.sessions:
            for key in ("first_line", "reads", "writes", "done_when", "budget_tokens", "model"):
                self.assertTrue(s.get(key), f"{s['id']} missing {key}")
            self.assertLessEqual(len([r for r in s["reads"] if not r.startswith("scripts/")]), 5, s["id"])

    def test_no_session_reads_the_big_files_whole(self):
        for s in self.sessions:
            for r in s["reads"]:
                self.assertFalse(r.startswith("agents/catalogue.json") or r.startswith("agents/rooms/rooms.json"), f"{s['id']} reads {r}")

    def test_script_prints_a_card_under_budget(self):
        out = subprocess.run([sys.executable, "scripts/session.py", "S1.2a"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("first line:", out.stdout)
        total = int(out.stdout.split("total at start")[0].strip().split()[-1].replace(",", ""))
        self.assertLess(total, 22000)

    def test_md_and_json_agree_on_ids(self):
        md = (ROOT / "sessions" / "SESSIONS.md").read_text(encoding="utf-8")
        for s in self.sessions:
            self.assertIn(f"| {s['id']} |", md, s["id"])


if __name__ == "__main__":
    unittest.main()
