import json,sys,unittest,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from refine_copy_bridge import OUT,PACK,RUBRIC

class BridgeControls(unittest.TestCase):
 def test_matched_inputs(self):
  m=json.loads((OUT/'manifest.json').read_text(encoding='utf-8'))
  self.assertEqual(len(m['jobs']),9)
  self.assertEqual(len(m['reused']),6)
  baseline=json.loads((ROOT/'data/ad-copy-playbook-test-v1/manifest-corrected.json').read_text(encoding='utf-8'))['jobs']
  for j in m['jobs']:
   p=j['payload'];base=next(b for b in baseline if b['arm']=='generic' and b['task']==(j['task'] if j['task'] in ('installation','value','reassurance') else 'value'))['payload']
   for k in ('model','reasoning','max_output_tokens','store','text'):self.assertEqual(p[k],base[k])
   user=json.loads(p['input'][0]['content'])
   self.assertEqual(user['brand'],json.loads(base['input'][0]['content'])['brand'])
   self.assertNotIn('tools',p)
  for task in {j['task'] for j in m['jobs']}:
   jobs=[j for j in m['jobs'] if j['task']==task]
   self.assertEqual(len({j['brief'] for j in jobs}),1)
 def test_cards_untouched_and_weights(self):
  p=json.loads((PACK/'ad-copy-deployment/playbook.json').read_text(encoding='utf-8'))
  self.assertEqual(hashlib.sha256((ROOT/'data/library-v3/cards.json').read_bytes()).hexdigest(),p['source_catalog_sha256'])
  self.assertEqual(sum(x['weight'] for x in RUBRIC.values()),100)
 def test_review_blinding(self):
  for p in (OUT/'calls').glob('review-*.json'):
   c=json.loads(p.read_text(encoding='utf-8'))
   candidates=json.loads(c['response']['payload']['input'][0]['content'])['candidates']
   self.assertEqual(len(candidates),15)
   for row in candidates:self.assertEqual(set(row),{'label','brief','brand_facts','copy'})

if __name__=='__main__':unittest.main()
