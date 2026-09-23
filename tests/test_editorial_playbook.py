import hashlib
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from read_playbook import load_workflow

class EditorialPlaybookTests(unittest.TestCase):
 def test_evidence_links_and_source_integrity(self):
  folder=ROOT/'playbooks/ad-copy-v1.1'
  pack=json.loads((folder/'ad-copy-deployment/playbook.json').read_text(encoding='utf-8'))
  evidence=json.loads((folder/'ad-copy-deployment/source-evidence.json').read_text(encoding='utf-8'))['cards']
  source=ROOT/'data/library-v3/cards.json'
  cards={c['id']:c for c in json.loads(source.read_text(encoding='utf-8'))['cards']}
  self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),pack['source_catalog_sha256'])
  for c in evidence:self.assertEqual(c,cards[c['id']])
  ids={c['id'] for c in evidence}
  self.assertEqual(ids,{k for r in pack['editorial_principles'] for k in r['source_card_ids']})

 def test_editorial_packet_excludes_bulk_evidence(self):
  folder=ROOT/'playbooks/ad-copy-v1.1'
  for slug in ('write-static-copy','revise-copy','objection-copy'):
   result=load_workflow(folder,'ad-copy-deployment.'+slug)
   self.assertEqual(result['status'],'editorial-draft')
   self.assertTrue(result['system_prompt'])
   self.assertEqual(len(result['editorial_principles']),8)
   self.assertEqual(result['workflow']['supporting_cards'],[])
   self.assertEqual(result['foundation_candidates'],[])
   self.assertNotIn('Sales-Page Template and Section Order',json.dumps(result))

if __name__=='__main__':unittest.main()
