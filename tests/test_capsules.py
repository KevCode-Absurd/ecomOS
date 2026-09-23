import unittest
from intelligence.capsules import compact_card
class CapsuleTests(unittest.TestCase):
    def test_shared_evidence_and_nested_conditions_are_preserved(self):
        statement={'text':'Only if qualified','quote':'Evidence'}
        unit={'id':'u','kind':'action','title':'Task','claim':statement,'action':statement,
          'trigger':{'op':'all','args':[{'op':'any','args':[statement]}]},'prerequisites':{'op':'all','args':[]},'exclusions':{'op':'any','args':[]},'completion':[],'unknowns':['Brand facts missing'],'relations':[]}
        spans=[{'field':f,'source_id':'s','source_sha256':'v','locator':'p1','start':2,'end':10,'quote':'Evidence'} for f in ['claim','action','trigger.0.0']]
        out=compact_card({'id':'c','unit':unit,'evidence':spans,'source_limitations':['Source omits duration.'],'batch_validation_errors':['held_dependency']})
        self.assertEqual(len(out['evidence']),1)
        self.assertEqual(out['unit']['trigger']['args'][0]['op'],'any')
        self.assertEqual(out['unit']['unknowns'],['Brand facts missing'])
        self.assertEqual(out['unit']['action']['evidence_refs'],['e1'])
        self.assertFalse(out['publication_allowed'])
        self.assertEqual(out['source_limitations'],['Source omits duration.'])
        self.assertEqual(out['batch_validation_errors'],['held_dependency'])
        self.assertIn('quote',unit['action'])
