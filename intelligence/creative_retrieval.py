"""Explicit task routing for campaign writing. General search remains unchanged."""
import re
ROUTES={
 'avatar':({'avatars','ad-copy-deployment','brand'},r'avatar|customer.research|voice.of.customer|awareness|buyer|audience|pain.point|objection|motivation'),
 'landing_page':({'landing-pages','ad-copy-deployment','offers'},r'landing.page|product.page|pdp|hero|headline|copywriting|conversion|offer|objection'),
 'static_ad':({'ad-copy-deployment','paid-social-creative'},r'static|ad.creative|ad.copy|headline|hook|awareness|creative.strategy|copywriting'),
 'writing_principles':({'ad-copy-deployment'},r'copywriting|headline|readability|benefit|specific|clarity|persuasion|proof|desire|awareness')}
EXCLUDE=re.compile(r'permission|cybersecurity|prompt.injection|security.relevant|staffing|hiring|\bseo\b|subscription|whatsapp|surprise.and.delight',re.I)
def candidates(engine,purpose):
 if purpose not in ROUTES:raise ValueError('Unsupported creative subtask')
 domains,pattern=ROUTES[purpose]
 return {k for k,c in engine.cards.items() if c['domain'] in domains
   and re.search(pattern,c['title']+' '+' '.join(c['tags']),re.I)
   and not EXCLUDE.search(c['title']+' '+' '.join(c['tags']))}
def retrieve_campaign(engine,queries,semantic=True):
 """One shared packet with no repeated card IDs; preserve all conditions."""
 seen=set();results=[]
 expanded={'writing_principles':'Write clear specific persuasive ecommerce copy: customer awareness, benefits, proof, concrete language, one main promise, readability. '+queries.get('landing_page',''),**queries}
 for purpose in ['writing_principles','avatar','landing_page','static_ad']:
  query=expanded.get(purpose,'')
  if not query:continue
  eligible=candidates(engine,purpose)
  ret=engine.search(query,allowed_ids=eligible,exclude_ids=seen,semantic=semantic,
   token_budget=1700 if purpose=='writing_principles' else 2200,max_cards=4)
  seen.update(ret['card_ids'])
  results.append({'purpose':purpose,'query':query,'eligible_count':len(eligible),'result':ret,'cards':[engine.cards[k] for k in ret['card_ids']]})
 return results
