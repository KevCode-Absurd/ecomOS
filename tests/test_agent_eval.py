import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from evaluate_agent_context import make_jobs,output_checks


class AgentEvalTests(unittest.TestCase):
    def test_expected_answer_never_leaks_to_executor(self):
        cases={'pairs':[{'id':'test','reference_case':0,'question':'What next?',
                        'common_facts':{'platform':'shop'},'variants':[{'id':'a','facts':{},'expected_difference':'SECRET_EXPECTATION'}],
                        'shared_requirements':['SECRET_RUBRIC']}]}
        passages=[{'source_sha256':'x','text':'source'}]
        packets={'0':{'review_status':'model_reviewed_for_evaluation_only','source_sha256':'x','context':[{'id':'u1','text':'advice'}]}}
        jobs=make_jobs(cases,passages,packets)
        self.assertEqual(len(jobs),3)
        self.assertNotIn('SECRET',str(jobs))
        self.assertEqual(next(j['input']['library'] for j in jobs if j['mode']=='none'),[])

    def test_baseline_cannot_invent_source_id(self):
        answer={'decision':'Wait','next_steps':[],'missing_inputs':[],'assumptions':[],
                'evidence_used':[{'id':'invented','supports':'a claim'}]}
        self.assertIn('invalid_evidence_id',output_checks(answer,[]))
