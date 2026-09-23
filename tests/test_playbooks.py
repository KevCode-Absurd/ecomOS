import hashlib
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from read_playbook import load_workflow

class PlaybookIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory=ROOT/'playbooks/v1'
        cls.catalog=json.loads((cls.directory/'catalog.json').read_text(encoding='utf-8'))
        cls.source=ROOT/'data/library-v3/cards.json'
        cls.cards={c['id']:c for c in json.loads(cls.source.read_text(encoding='utf-8'))['cards']}

    def test_source_snapshot_and_complete_inventory(self):
        self.assertEqual(hashlib.sha256(self.source.read_bytes()).hexdigest(),self.catalog['source_catalog_sha256'])
        inventory=[]
        for d in self.catalog['domains']:
            rows=json.loads((self.directory/d['domain']/'card-index.json').read_text(encoding='utf-8'))['cards']
            self.assertEqual(len(rows),d['card_count'])
            for c in rows:self.assertEqual(self.cards[c['id']]['domain'],d['domain'])
            inventory.extend(c['id'] for c in rows)
        mixed=json.loads((self.directory/'multi/routing.json').read_text(encoding='utf-8'))['cards']
        inventory.extend(c['id'] for c in mixed)
        self.assertEqual(len(inventory),len(set(inventory)))
        self.assertEqual(set(inventory),set(self.cards))

    def test_support_preserves_original_meaning_fields(self):
        workflows=[]
        for d in self.catalog['domains']:
            p=json.loads((self.directory/d['path']).read_text(encoding='utf-8'))
            self.assertEqual(p['status'],'draft')
            self.assertEqual(len(p['workflows']),3)
            for w in p['workflows']:
                workflows.append(w['id'])
                self.assertTrue(w['supporting_cards'])
                for c in w['supporting_cards']+p['foundation_candidates']:
                    for field,value in c.items():self.assertEqual(self.cards[c['id']][field],value)
                self.assertEqual([c['id'] for c in w['supporting_cards']],w['retrieval']['selected_card_ids'])
                for k in w['retrieval']['mixed_candidate_ids']:self.assertEqual(self.cards[k]['domain'],'multi')
        self.assertEqual(len(workflows),69)
        self.assertEqual(len(set(workflows)),69)

    def test_loader_is_scoped_and_selectable(self):
        wid='ad-copy-deployment.write-static-copy'
        packet=load_workflow(self.directory,wid)
        self.assertEqual(packet['workflow']['id'],wid)
        self.assertEqual(packet['foundation_candidates'],[])
        selected=packet['workflow']['supporting_cards'][0]['id']
        filtered=load_workflow(self.directory,wid,[selected])
        self.assertEqual([c['id'] for c in filtered['workflow']['supporting_cards']],[selected])
        self.assertIn('at most two revision passes',packet['workflow']['completion_rule'])

    def test_unknown_workflow_or_foreign_card_rejected(self):
        with self.assertRaises(ValueError):load_workflow(self.directory,'../../.env')
        with self.assertRaises(ValueError):load_workflow(self.directory,'ad-copy-deployment.write-static-copy',['nonexistent'])

    def test_mixed_links_resolve_and_unknowns_explicit(self):
        known={w['id'] for d in self.catalog['domains'] for w in d['workflows']}
        mixed=json.loads((self.directory/'multi/routing.json').read_text(encoding='utf-8'))['cards']
        for c in mixed:
            for route in c['candidate_routes']:self.assertIn(route['workflow'],known)
            if not c['candidate_routes']:self.assertEqual(c['status'],'unassigned-needs-task-search')

if __name__=='__main__':unittest.main()
