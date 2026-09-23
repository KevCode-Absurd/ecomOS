import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from calibrate_extractors import validate

class CalibrationTests(unittest.TestCase):
    def test_valid_abstention(self):
        self.assertEqual(validate({'origin_assessment':'uncertain','cards':[],'more_candidates':False,'abstention_reason':'No action'},'source'),[])
    def test_fabricated_quote(self):
        card={'title':'x','claim':'x','action':'x','applies_when':[],'do_not_use_when':[],'unknowns':[],'evidence_quotes':['invented']}
        self.assertIn('quote_not_exact',validate({'origin_assessment':'uncertain','cards':[card],'more_candidates':False,'abstention_reason':''},'source'))
