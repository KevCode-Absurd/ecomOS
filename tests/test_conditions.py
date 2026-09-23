import unittest
from intelligence.conditions import evaluate, excluded, validate
from intelligence.context import pack


class ConditionTests(unittest.TestCase):
    def test_alternative_audiences(self):
        rule={'op':'any','args':[{'awareness':'problem'},{'awareness':'solution'}]}
        self.assertTrue(evaluate(rule,{'awareness':'problem'}))
        self.assertTrue(evaluate(rule,{'awareness':'solution'}))
        self.assertFalse(evaluate(rule,{'awareness':'unaware'}))
        self.assertIsNone(evaluate(rule,{}))

    def test_known_alternative_can_resolve_missing_fact(self):
        rule={'op':'any','args':[{'platform':'Shopify'},{'custom_checkout':True}]}
        self.assertTrue(evaluate(rule,{'platform':'Shopify'}))
        self.assertIsNone(evaluate(rule,{'platform':'Other'}))

    def test_missing_exclusion_never_becomes_permission(self):
        self.assertIsNone(excluded({'inventory_blocked':True},{}))
        self.assertTrue(excluded({'inventory_blocked':True,'tracking_broken':True}, {'inventory_blocked':True}))
        self.assertFalse(excluded({},{}))

    def test_range_and_boolean_types(self):
        rule={'op':'gte','fact':'sessions','value':300000}
        self.assertTrue(evaluate(rule,{'sessions':300000}))
        self.assertFalse(evaluate(rule,{'sessions':299999}))
        self.assertIsNone(evaluate(rule,{'sessions':'300000'}))
        self.assertIsNone(evaluate(rule,{'sessions':True}))
        self.assertFalse(evaluate({'ready':True},{'ready':1}))

    def test_unknown_survives_negation(self):
        self.assertIsNone(evaluate({'op':'not','arg':{'ready':True}},{}))

    def test_invalid_expression_and_nonfinite(self):
        for rule in [{'op':'any'}, {'op':'any','args':[]},{'op':'gte','fact':'sessions','value':float('nan')}, {'op':'unknown','args':[]}]:
            with self.assertRaises(ValueError): validate(rule)

    def test_context_preserves_branch_and_rejects_wrong_audience(self):
        rule={'op':'any','args':[{'awareness':'problem'},{'awareness':'solution'}]}
        card={'id':'a','title':'Landing page','claim':'Explain offer','action':'Build page',
              'applies_when':rule,'do_not_use_when':{},'dependencies':[]}
        self.assertEqual(pack([card],'landing',{'awareness':'problem'})['selected_ids'],['a'])
        self.assertEqual(pack([card],'landing',{'awareness':'unaware'})['selected_ids'],[])
        self.assertIn('"any"',pack([card],'landing',{'awareness':'solution'})['context'])
