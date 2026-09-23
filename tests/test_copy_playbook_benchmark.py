import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from benchmark_copy_playbook import prepare

class CopyComparisonTests(unittest.TestCase):
 def test_matched_inputs_and_only_context_varies(self):
  manifest=prepare();self.assertEqual(len(manifest['jobs']),9)
  for task in ('installation','value','reassurance'):
   jobs={j['arm']:j for j in manifest['jobs'] if j['task']==task}
   bodies={k:json.loads(v['payload']['input'][0]['content']) for k,v in jobs.items()}
   for key in ('brand','brief','response_format'):
    self.assertEqual(bodies['generic'][key],bodies['playbook'][key])
    self.assertEqual(bodies['playbook'][key],bodies['playbook_cards'][key])
   self.assertNotIn('playbook',bodies['generic'])
   self.assertNotIn('supporting_cards',bodies['playbook'])
   extra=bodies['playbook_cards'].pop('supporting_cards')
   self.assertEqual(bodies['playbook'],bodies['playbook_cards'])
   self.assertEqual(len(extra),2)
   self.assertEqual(jobs['playbook']['payload']['instructions'],jobs['playbook_cards']['payload']['instructions'])
   for j in jobs.values():
    self.assertNotIn('tools',j['payload']);self.assertFalse(j['payload']['store'])
    self.assertEqual(j['payload']['model'],'gpt-6-luna')
    self.assertEqual(j['payload']['reasoning'],{'effort':'medium'})
    self.assertIn('JSON',j['payload']['input'][0]['content'])
 def test_no_private_performance_or_credentials_in_facts(self):
  for job in prepare()['jobs']:
   brand=json.loads(job['payload']['input'][0]['content'])['brand']
   self.assertEqual(set(brand),{'name','market','currency','product_url','observations','constraints','visual_brief'})

if __name__=='__main__':unittest.main()
