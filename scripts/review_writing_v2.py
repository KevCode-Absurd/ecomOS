import random,json
import calibration_client as c
from peach_writing_v2 import OUT
from peach_visual import facts
from review_peach_visual import SYSTEM
from build_library import read,write
def main():
 if (OUT/'review.json').exists():
  previous=read(OUT/'review.json')
  if previous.get('shared_research_provided'):return
  write(OUT/'review-incomplete-evidence.json',previous)
 runs=[read(p) for p in sorted((OUT/'runs').glob('*.json'))];assert len(runs)==9,'Wait for all candidates'
 random.Random(821).shuffle(runs);mapping={};candidates={}
 for i,r in enumerate(runs):
  label=chr(65+i);mapping[label]={'model':r['model'],'arm':r['arm']};o=r['output'];candidates[label]={'page':o['landing_page_markdown'],'ad':{k:v for k,v in o['ad'].items() if k!='image_prompt'}}
 c.PROVIDERS['openai']=('gpt-6-sol','https://api.openai.com/v1/chat/completions','OPENAI_API_KEY',2.5,10)
 research=json.loads(runs[0]['call']['payload']['input'][0]['content'])['shared_public_research']
 result=c.run_call('peach-visual-benchmark','openai','high',SYSTEM.replace('six anonymized','nine anonymized')+' The shared research memo was supplied to every writer. Treat its brand claims as supplied claims, not independent verification; do not call them invented merely because the shorter fact sheet omits them.',{'facts':facts(),'shared_public_research':research,'candidates':candidates},limit=6000,stage_limit=20)
 out=result.get('output',{});valid=result['finish_reason']=='stop' and len(out.get('reviews',[]))==9 and {x['label'] for x in out['reviews']}==set(mapping)
 write(OUT/'review.json',{'valid':valid,'mapping':mapping,'result':result,'shared_research_provided':True,'scope':'Blinded simulated agency-owner, copy only; same-family bias possible'})
 print({'valid':valid,'cost':result['booked_cost_usd']})
if __name__=='__main__':main()
