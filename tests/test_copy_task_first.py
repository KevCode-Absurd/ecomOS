import json,sys,unittest,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from refine_copy_task_first import OUT,PACK

def read(p):return json.loads(p.read_text(encoding='utf-8'))

class TaskFirstControls(unittest.TestCase):
 def test_complete_matched_design(self):
  m=read(OUT/'manifest.json');self.assertEqual(len(m['jobs']),8);self.assertEqual(len(m['reused']),10)
  rows=m['jobs']+m['reused'];self.assertEqual(len({r['id'] for r in rows}),18)
  for task in {r['task'] for r in rows}:
   group=[r for r in rows if r['task']==task]
   self.assertEqual({r['arm'] for r in group},{'generic','v1.2','v1.4'})
   self.assertEqual(len({json.dumps(r['facts'],sort_keys=True) for r in group}),1)
   self.assertEqual(len({r['brief'] for r in group}),1)
  self.assertNotIn('support-retargeting',{r['task'] for r in m['reused']})
  for j in m['jobs']:
   self.assertEqual(j['payload']['model'],'gpt-6-luna')
   self.assertNotIn('tools',j['payload'])
 def test_immutable_cards_and_blind_reviews(self):
  pack=read(PACK/'ad-copy-deployment/playbook.json')
  self.assertEqual(hashlib.sha256((ROOT/'data/library-v3/cards.json').read_bytes()).hexdigest(),pack['source_catalog_sha256'])
  for p in (OUT/'calls').glob('review-*.json'):
   candidates=json.loads(read(p)['response']['payload']['input'][0]['content'])['candidates']
   self.assertEqual(len(candidates),18)
   for r in candidates:self.assertEqual(set(r),{'label','brief','brand_facts','copy'})

if __name__=='__main__':unittest.main()
