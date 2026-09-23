"""Controlled text-only comparison: fixed revised prompt, none/old/routed retrieval."""
import argparse,json,time
import peach_visual as v
from build_library import read,write
from intelligence.creative_retrieval import retrieve_campaign
OUT=v.OUT/'writing-v2'
SYSTEM='''You are the brand's ecommerce copywriter and creative director. Write usable, persuasive customer-facing work in a direct, warm, concrete voice. Use supplied facts as the fact sheet; expert cards are methods, never new product facts. Choose one relevant customer situation and carry it through the page and ad. Explain the product and offer clearly with concrete benefits and credible reasons to buy. Write as the brand (we/our where natural), not a researcher describing "the brand advertises". Avoid abstractions, jargon, repeated cautions and commentary about writing. Keep internal assumptions and fact-check notes in the separate checks field. Include necessary compatibility, policy eligibility and adult-supervision qualifications concisely in sensible places, without repeating them in every section. Do not invent proof, reviews, certifications, component quantities, scarcity, extra services or safety guarantees. No external actions or browsing. Return valid JSON only.'''
def run(model):
 v.setup();v.SYSTEM=SYSTEM
 old=read(v.OUT/'runs'/f'{model}-cards.json');baseline=read(v.OUT/'runs'/f'{model}-none.json')
 # Fix the entire prior final task input; vary only expert_context and system prompt.
 user=json.loads(baseline['calls'][1]['payload']['input'][0]['content'])
 user.pop('expert_context',None)
 packets=OUT/'packets'/f'{model}.json'
 if packets.exists():new=read(packets)
 else:
  from search_knowledge import engine
  new=retrieve_campaign(engine(),old['plan']['queries']);write(packets,new)
 for arm,ret in [('none',[]),('old',old['retrieval']),('routed',new)]:
  p=OUT/'runs'/f'{model}-{arm}.json'
  if p.exists():continue
  payload={**user,'expert_context':[{'purpose':r['purpose'],'context':r['result']['context']} for r in ret]}
  result,out=v.call(model,payload,10500)
  write(p,{'model':model,'arm':arm,'output':out,'call':result,'retrieval':ret,'shared_plan':old['plan']})
  print({'done':p.stem,'cost':result['cost_upper_estimate_usd'],'cards':sum(len(r['cards']) for r in ret)},flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--model',choices=v.MODELS,required=True);a=p.parse_args();run(a.model)
