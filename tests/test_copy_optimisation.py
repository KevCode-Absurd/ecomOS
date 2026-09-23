import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from optimise_ad_copy import RUBRIC,OUT,OLD

class OptimisationControls(unittest.TestCase):
 def test_equal_facts_cards_and_settings(self):
  old={j['id']:j for j in json.loads((OLD/'manifest-corrected.json').read_text())['jobs']}
  revision=json.loads((OUT/'revision-manifest.json').read_text())
  self.assertEqual(len(revision['jobs']),9)
  for j in revision['jobs']:
   if j['task']=='new-brief':continue
   before=old[j['id'].removeprefix('v2-')]['payload'];after=j['payload']
   for k in ('model','reasoning','max_output_tokens','store','text'):self.assertEqual(before[k],after[k])
   a=json.loads(before['input'][0]['content']);b=json.loads(after['input'][0]['content'])
   for k in ('brand','brief','response_format','supporting_cards'):self.assertEqual(a.get(k),b.get(k))
   self.assertNotIn('tools',after)
 def test_rubric_weight_and_blinding(self):
  self.assertEqual(sum(r['weight'] for r in RUBRIC.values()),100)
  for path in (OUT/'calls').glob('*review*.json'):
   call=json.loads(path.read_text(encoding='utf-8'))
   payload=json.loads(call['response']['payload']['input'][0]['content'])
   labels=[c['label'] for c in payload['candidates']]
   self.assertEqual(len(labels),len(set(labels)))
   for c in payload['candidates']:
    self.assertEqual(set(c),{'label','brief','brand_facts','copy'})
    self.assertNotIn('internal_notes',c)

if __name__=='__main__':unittest.main()
