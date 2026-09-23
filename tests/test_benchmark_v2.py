import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from benchmark_v2 import validate

class SandboxChecks(unittest.TestCase):
 def test_stock_buffer_and_discount(self):
  self.assertTrue(validate('E1',{'actions':{'daily_total_daypack_units_cap':5,'discount_percent':0,'launch_status':'draft'}})['all_pass'])
  self.assertFalse(validate('E1',{'actions':{'daily_total_daypack_units_cap':6,'discount_percent':20,'launch_status':'live'}})['all_pass'])
 def test_boundary_eligible_and_purchase_excluded(self):
  self.assertTrue(validate('E2',{'actions':{'selected_customer_ids':['c8','c1']}})['all_pass'])
  self.assertFalse(validate('E2',{'actions':{'selected_customer_ids':['c1','c2','c8']}})['all_pass'])
 def test_negative_residual_not_clamped(self):
  self.assertTrue(validate('E4',{'actions':{'in_period_meta_value':38400,'union_attributed_value':46400,'unassigned_shopify_value':-1400}})['all_pass'])
  self.assertFalse(validate('E4',{'actions':{'in_period_meta_value':38400,'union_attributed_value':46400,'unassigned_shopify_value':0}})['all_pass'])
 def test_short_test_cannot_claim_significance(self):
  self.assertFalse(validate('E3',{'actions':{'test_days':14,'developer_hours':3,'designer_hours':6,'claimed_statistical_significance':True,'launch_status':'draft'}})['all_pass'])

if __name__=='__main__':unittest.main()
