import json,os,tempfile,unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/".runtime"))
from pathlib import Path
from intelligence.library import build_index
from intelligence.knowledge_metadata import build_metadata,classify,fingerprint
from intelligence.knowledge_search import KnowledgeEngine
ROOT=Path(__file__).resolve().parents[1]
os.environ['TIKTOKEN_CACHE_DIR']=str(ROOT/'data/tokenizer-cache')

def card(id,title,steps,caveats=None):
 return dict(id=id,title=title,summary=title,use_when='When shoppers abandon checkout',steps=steps,
 caveats=caveats or [],tags=['checkout'],domain='cro',source_name='test.docx',source_id='s',section=0)

class KnowledgeTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.p=Path(self.tmp.name)
  self.cards=[card('a','Remove checkout friction',['Offer guest checkout.'],['Measure completed orders, not clicks.']),
   card('b','Remove checkout friction',['Repeated advice.'],['Measure completed orders, not clicks.']),card('c','Review supplier terms',['Negotiate lead time.'])]
  self.save();self.calls=0
  def embed(text):self.calls+=1;return [1.,0.]
  self.e=KnowledgeEngine(self.p,embed)
 def save(self):
  (self.p/'cards.json').write_text(json.dumps({'cards':self.cards}),encoding='utf-8')
  (self.p/'metadata.json').write_text(json.dumps({'cards':build_metadata(self.cards)}),encoding='utf-8')
  (self.p/'vectors.json').write_text(json.dumps({'a':[1.,0.],'b':[1.,0.],'c':[0.,1.]}),encoding='utf-8')
  build_index(self.p/'search.sqlite',self.cards)
 def tearDown(self):self.tmp.cleanup()
 def test_packet_preserves_conditions_and_deduplicates(self):
  r=self.e.search('checkout friction',max_cards=2)
  self.assertIn('not clicks',r['context']);self.assertNotIn('cards',r)
  self.assertFalse({'a','b'}<=set(r['card_ids']));self.assertLessEqual(r['knowledge_tokens'],8000)
 def test_distinct_conditions_are_not_silently_dropped(self):
  self.cards[1]['caveats']=['Only for returning shoppers.'];self.save()
  r=self.e.search('checkout friction',max_cards=3)
  self.assertIn('not clicks',r['context']);self.assertIn('Only for returning',r['context'])
 def test_embedding_cached(self):
  self.e.search('checkout');self.e.search('checkout');self.assertEqual(self.calls,1)
 def test_empty_query_and_zero_limits_do_not_call_provider(self):
  for kw in [{'task':''},{'task':'checkout','token_budget':0},{'task':'checkout','max_cards':0}]:
   self.assertEqual(self.e.search(**kw)['card_ids'],[])
  self.assertEqual(self.calls,0)
 def test_unknown_query_keyword_abstains(self):
  self.assertEqual(self.e.search('quantum neutrino',semantic=False)['match_status'],'no-suitable-match')
 def test_tiny_budget_does_not_cut_instructions(self):
  self.assertEqual(self.e.search('checkout',token_budget=5,semantic=False)['context'],'')
 def test_explicit_filter(self):
  self.assertEqual(self.e.search('checkout',domain='finance')['card_ids'],[])
 def test_allowed_and_excluded_ids_apply_to_both_rankings(self):
  r=self.e.search('checkout',allowed_ids={'a','c'},exclude_ids={'a'})
  self.assertTrue(set(r['card_ids'])<={'c'})
  self.assertEqual(self.e.search('checkout',allowed_ids=set())['card_ids'],[])
 def test_provider_failure_falls_back(self):
  def fail(t):raise RuntimeError('secret must not leak')
  self.e=KnowledgeEngine(self.p,fail);r=self.e.search('checkout')
  self.assertEqual(r['method'],'keyword');self.assertTrue(r['warnings']);self.assertNotIn('secret',str(r))
 def test_reload_after_change_and_stale_metadata(self):
  self.cards[0]['steps']=['New checkout instruction.']
  (self.p/'cards.json').write_text(json.dumps({'cards':self.cards}),encoding='utf-8')
  self.assertIn('New checkout instruction',self.e.get_card('a')['guidance'])
  self.assertEqual(self.e.metadata['a']['content_hash'],fingerprint(self.cards[0]))
 def test_labels_never_invent_verification(self):
  m=classify(self.cards[0]);self.assertIsNone(m['last_verified_at']);self.assertIsNone(m['source_date'])
  self.assertEqual(m['classification_status'],'inferred')
 def test_override_requires_matching_content(self):
  o={'a':{'content_hash':'stale','fields':{'durability':'durable'}}}
  self.assertEqual(build_metadata(self.cards,o)['a']['durability'],'unknown')
if __name__=='__main__':unittest.main()
