import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from benchmark_case import BRAND,TASKS,RUBRIC
from report_ecommerce_benchmark import score
class BenchmarkTests(unittest.TestCase):
 def test_known_answer_math(self):
  p=BRAND['products'][0]
  def contribution(price):return price-p['landed_cogs']-p['pick_pack']-p['merchant_shipping_cost']-price*p['payment_fee_percent']/100
  self.assertAlmostEqual(contribution(80),39.6);self.assertAlmostEqual(contribution(64),24.08)
  self.assertAlmostEqual(contribution(64)-30,-5.92)
  self.assertAlmostEqual(p['stock']/p['daily_units_sold'],26.25)
 def test_case_consistency(self):
  for period in ['previous_30_days','current_30_days']:
   s=BRAND['shopify'][period];self.assertEqual(s['mobile_orders']+s['desktop_orders'],s['orders']);self.assertEqual(s['mobile_sessions']+s['desktop_sessions'],s['sessions'])
   self.assertLessEqual(s['orders'],s['checkout_started_sessions']);self.assertLessEqual(s['checkout_started_sessions'],s['add_to_cart_sessions'])
  self.assertEqual(len({t['id'] for t in TASKS}),10);self.assertEqual(sum(t['kind']=='question' for t in TASKS),6)
 def test_weighting_and_invalid_judgments(self):
  self.assertEqual(score({'scores':{k:4 for k in RUBRIC}}),100)
  self.assertEqual(score({'scores':{k:2 for k in RUBRIC}}),50)
  with self.assertRaises(ValueError):score({'scores':{k:5 for k in RUBRIC}})
if __name__=='__main__':unittest.main()
