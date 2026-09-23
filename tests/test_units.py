import copy
import unittest
from intelligence.units import validate_output


class UnitTests(unittest.TestCase):
    def setUp(self):
        self.source={'source_id':'s','source_sha256':'abc','locator':'p1','start':100,'text':'Test one variable. Wait for data.'}
        self.unit={'id':'u1','kind':'action','title':'Test',
                   'claim':{'text':'One variable','quote':'Test one variable.'},
                   'action':{'text':'Test one variable','quote':'Test one variable.'},
                   'trigger':{'op':'all','args':[]},'prerequisites':{'op':'all','args':[]},
                   'exclusions':{'op':'any','args':[]},'completion':[],'unknowns':[],'relations':[]}

    def result(self,unit):
        return validate_output({'units':[unit],'more_units':False,'unresolved':[]},self.source)

    def test_binds_offsets_but_never_approves(self):
        candidate=self.result(self.unit)['candidates'][0]
        self.assertEqual(candidate['evidence'][0]['start'],100)
        self.assertEqual(candidate['status'],'candidate')
        self.assertEqual(candidate['semantic_review'],'required')

    def test_unquoted_condition_is_held(self):
        self.unit['prerequisites']['args']=[{'text':'Must have Shopify','quote':'Shopify'}]
        self.assertEqual(len(self.result(self.unit)['held']),1)

    def test_added_quote_wrapper_is_not_silently_fixed(self):
        self.unit['action']['quote']='"Test one variable."'
        self.assertEqual(len(self.result(self.unit)['held']),1)

    def test_principle_cannot_be_given_action(self):
        self.unit['kind']='principle'
        self.assertEqual(len(self.result(self.unit)['held']),1)
        self.unit['action']=None
        self.assertEqual(len(self.result(self.unit)['candidates']),1)

    def test_ambiguous_anchor_held(self):
        self.source['text']+=' Test one variable.'
        self.assertEqual(len(self.result(self.unit)['held']),1)

    def test_alternative_evidence_preserved(self):
        self.unit['prerequisites']={'op':'any','args':[{'text':'Testing','quote':'Test one variable.'},{'text':'Waiting','quote':'Wait for data.'}]}
        result=self.result(self.unit)
        self.assertEqual(len(result['candidates']),1)
        self.assertEqual(result['candidates'][0]['unit']['prerequisites']['op'],'any')

    def test_missing_relation_target(self):
        self.unit['relations']=[{'kind':'depends_on','target':'missing'}]
        self.assertIn('invalid_relation_target',self.result(self.unit)['errors'])

    def test_held_evidence_cannot_satisfy_dependency(self):
        other=copy.deepcopy(self.unit); other['id']='u2'; other['claim']['quote']='invented'
        self.unit['relations']=[{'kind':'depends_on','target':'u2'}]
        result=validate_output({'units':[self.unit,other],'more_units':False,'unresolved':[]},self.source)
        self.assertIn('invalid_relation_target',result['errors'])

    def test_dependency_cycle_is_reported(self):
        other=copy.deepcopy(self.unit); other['id']='u2'; other['relations']=[{'kind':'depends_on','target':'u1'}]
        self.unit['relations']=[{'kind':'depends_on','target':'u2'}]
        result=validate_output({'units':[self.unit,other],'more_units':False,'unresolved':[]},self.source)
        self.assertIn('dependency_cycle',result['errors'])

    def test_repair_merge_limit_is_explicit_and_bounded(self):
        units=[]
        for i in range(17):
            unit=copy.deepcopy(self.unit);unit['id']=str(i);units.append(unit)
        output={'units':units,'more_units':True,'unresolved':[]}
        self.assertEqual(validate_output(output,self.source)['errors'],['invalid_units'])
        self.assertEqual(len(validate_output(output,self.source,max_units=64)['candidates']),17)
        with self.assertRaises(ValueError):validate_output(output,self.source,max_units=65)
