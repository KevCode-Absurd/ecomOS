import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from review_aliases import encode,decode
class ReviewAliasTests(unittest.TestCase):
    def test_links_and_verdicts_roundtrip_without_mutating_original(self):
        target={'candidate_id':'long-a','unit':{'id':'long-a','relations':[{'kind':'depends_on','target':'long-b'}]}}
        context={'candidate_id':'long-b','unit':{'id':'long-b','relations':[]}}
        a,b,m=encode([target],[context]);self.assertEqual(a[0]['unit']['relations'][0]['target'],'c2')
        out,errors=decode({'reviews':[{'candidate_id':'c1','verdict':'supported'}]},m)
        self.assertEqual(out['reviews'][0]['candidate_id'],'long-a');self.assertEqual(errors,[])
        self.assertEqual(target['candidate_id'],'long-a')
    def test_unknown_model_id_is_rejected(self):
        _,errors=decode({'reviews':[{'candidate_id':'invented'}]},{'c1':'known'})
        self.assertEqual(errors,['unknown_review_alias'])
