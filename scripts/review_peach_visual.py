"""Blinded simulated owner review of copy only; images are reviewed separately."""
import random
import calibration_client as c
from peach_visual import OUT,facts
from build_library import read,write
SYSTEM='''Act as an ecommerce agency owner deciding which draft to hand to a designer and client. Review six anonymized campaign copy packages. You do not see rendered images: do not grade visual execution. Grade real usable copy, not academic completeness. Prioritize directness, audience specificity, believable persuasion, message consistency between page and ad, a clear offer and CTA, and little editing work. Penalize stilted phrases, repetitive disclaimers, researcher voice such as "the brand advertises" in customer copy, and unverified claims. Do not reward length or safety disclaimers for their own sake; concise necessary caveats are appropriate. No fabricated conversion lift or customer satisfaction. This is a simulated review, not actual owner validation. Return JSON {"reviews":[{"label":"A","copy_score_0_to_4":0,"verdict":"use_after_routine_review|edit|rewrite","strongest_line":"exact short quote","main_weakness":"specific example","change_before_launch":"..."}],"preferred_labels":[],"summary":"..."}. Score each label exactly once: 4 strong ready-to-build draft,3 useful with modest edits,2 substantial edits,1 largely rewrite,0 unusable. Judge only supplied copy and facts.'''
def main():
 p=OUT/'copy-review.json'
 if p.exists():return
 runs=[read(x) for x in sorted((OUT/'runs').glob('*.json'))];assert len(runs)==6
 random.Random(42).shuffle(runs);mapping={};candidates={}
 for i,r in enumerate(runs):
  label=chr(65+i);mapping[label]={'model':r['model'],'arm':r['arm']};o=r['output'];candidates[label]={'page':o['landing_page_markdown'],'ad':{k:v for k,v in o['ad'].items() if k!='image_prompt'}}
 c.PROVIDERS['openai']=('gpt-6-sol','https://api.openai.com/v1/chat/completions','OPENAI_API_KEY',2.5,10)
 result=c.run_call(OUT.name,'openai','high',SYSTEM,{'facts':facts(),'candidates':candidates},limit=4500,stage_limit=20)
 out=result.get('output',{});valid=result['finish_reason']=='stop' and len(out.get('reviews',[]))==6 and {x['label'] for x in out['reviews']}==set(mapping)
 write(p,{'valid':valid,'mapping':mapping,'result':result,'scope':'Copy only, simulated agency-owner lens; no image evaluation; same-model-family bias possible'});print({'valid':valid,'cost':result['booked_cost_usd']})
if __name__=='__main__':main()
