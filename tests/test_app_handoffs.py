"""The shared hand-offs table (events.md): validation and append through server.Handoffs."""
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('ecomos_server_h', ROOT / 'app' / 'server.py')
server = importlib.util.module_from_spec(spec)
sys.modules['ecomos_server_h'] = server
spec.loader.exec_module(server)


class HandoffsTest(unittest.TestCase):
    def test_append_and_validate(self):
        with tempfile.TemporaryDirectory() as tmp:
            h = server.Handoffs(Path(tmp) / 'handoffs.json')
            row = h.append({'from_screen': '04-offers-pricing', 'to': 'creative', 'kind': 'ad_brief', 'title': 'Lead with proof, not the code',
                            'why': '91 percent of ads push a code.', 'draft': 'Hook: ...', 'win_rule': 'CTR up 15 percent', 'stop_rule': '3,000 impressions below control',
                            'check_on': '2026-10-12', 'capability': 'CREA-C06', 'owner': 'agent_drafts', 'finding_id': '04-offers-pricing.OFFER-R09.code'})
            self.assertTrue(row['id'].startswith('HO-'))
            self.assertEqual(row['status'], 'proposed')
            self.assertEqual(row['owner'], 'agent_drafts')
            self.assertEqual(json.loads((Path(tmp) / 'handoffs.json').read_text())[0]['title'], 'Lead with proof, not the code')
            for bad in ({'from_screen': 'x', 'to': 'creative', 'kind': 'ad_brief', 'title': 't'},
                        {'from_screen': '04-offers-pricing', 'to': '', 'kind': 'ad_brief', 'title': 't'},
                        {'from_screen': '04-offers-pricing', 'to': 'creative', 'kind': 'poem', 'title': 't'},
                        {'from_screen': '04-offers-pricing', 'to': 'creative', 'kind': 'ad_brief', 'title': ''}):
                with self.assertRaises(ValueError):
                    h.append(bad)

    def test_body_limit_fits_an_export(self):
        self.assertGreaterEqual(server.MAX_BODY, 2_000_000)


if __name__ == '__main__':
    unittest.main()
