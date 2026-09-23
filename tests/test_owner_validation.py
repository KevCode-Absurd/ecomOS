import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from owner_validation import validate
class Checks(unittest.TestCase):
 def test_alias_is_not_business_failure(self):
  x={'actions':{'proposed_daily_total_daypack_units_cap':5,'discount_percent':0,'launch_status':'draft'}}
  self.assertTrue(validate('E1',x)['all_pass']);self.assertNotIn('daily_total_daypack_units_cap',x['actions'])
 def test_negative_significance_variants(self):
  for v in [False,0,'not claimed']:
   self.assertTrue(validate('E3',{'actions':{'test_days':123,'designer_hours':6,'developer_hours':3,'qa_developer_hours':2,'claimed_statistical_significance':v,'launch_status':'draft'}})['all_pass'])
 def test_true_claim_still_fails(self):
  self.assertFalse(validate('E3',{'actions':{'test_days':123,'designer_hours':6,'developer_hours':5,'claimed_statistical_significance':True,'launch_status':'draft'}})['all_pass'])
 def test_zero_demand_cap_is_valid(self):
  self.assertTrue(validate('E1',{'actions':{'daily_total_daypack_units_cap':0,'discount_percent':0,'launch_status':'blocked'}})['all_pass'])
