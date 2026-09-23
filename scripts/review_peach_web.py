import argparse,json,random
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import calibration_client as c
from peach_web_case import OUT,TASKS
from build_library import read,write
WEIGHTS={'usefulness':30,'personalization':20,'correctness':20,'clarity':15,'execution_readiness':15}
SYSTEM='''Simulate a paying ecommerce business owner or agency owner reviewing work you need to use today. This is a simulated perspective, not actual customer feedback. Review six anonymized answers to the same natural request. Judge clear decisions, actual usable artifacts/copy, real brand personalization, correct use of data, crispness and remaining operator effort. Do not reward length, sources/cards for their own sake, academic completeness, or needless blocking. Research memos/cards are evidence, not truth. Review source use honestly: citations alone do not verify a claim. Penalize fabricated research, unsupported product safety claims, invented business facts or completed actions, and impractical plans. Do not punish appropriate uncertainty. New store: zero past sales is not a meaningful growth comparison. Sales reversals were test orders; don't subtract twice or infer customer refund rates. 39 orders differs from 34 converted sessions; actual net customer order count is unknown. Reported funnel is 4452 sessions,112 cart,101 checkout,34 converted sessions. Product650/shipping350/payment2% are known; taxes, packaging, RTO reverse cost and stock are not. At listed3299,2233.02 contribution BEFORE ads/RTO/other costs is not net profit. Meta attribution is not incrementality. Return JSON {"reviews":[{"label":"A","scores":{"usefulness":0,"personalization":0,"correctness":0,"clarity":0,"execution_readiness":0},"verdict":"use|edit|reject","editing_burden":"minor|substantial|rewrite","strengths":[],"material_issues":[],"specific_evidence":"..."}],"summary":"..."}. Score 0-4:0unusable,1major rewrite,2useful pieces/substantial work,3minor editing,4usable draft with routine review. Every label exactly once. Explain actual business value; no invented revenue lift or willingness to pay.'''

def one(task,lens):
 tid,request=task;p=OUT/'reviews'/f'{tid}-{lens}.json'
 if p.exists():return
 runs=[read(x) for x in sorted((OUT/'safe-runs').glob(tid+'-*.json'))]
 if len(runs)!=6 or any(x['status']!='complete' for x in runs):raise ValueError('Incomplete candidates')
 random.Random(tid+lens).shuffle(runs);mapping={};answers={};evidence={}
 for i,r in enumerate(runs):
  label=chr(65+i);mapping[label]={'model':r['model'],'arm':r['arm']}
  answers[label]={k:v for k,v in r['output'].items() if k!='applied_card_ids'}
  research=read(Path(r['research_file']));cards={x['id']:x for rr in r['retrieval'] for x in rr['cards']}
  # Judge gets evidence without condition-specific grouping; avoid revealing arm labels.
  evidence[research['response']['request_id']]=research['memo']
  for k,v in cards.items():evidence[k]=v
 r=c.run_call(OUT.name,'openai','medium',SYSTEM,{'lens':lens,'brand':read(OUT/'brand.json'),'owner_request':request,'answers':answers,'available_evidence':list(evidence.values())},limit=11000,stage_limit=23)
 out=r.get('output');valid=r['finish_reason']=='stop' and isinstance(out,dict) and len(out.get('reviews',[]))==6 and {x['label'] for x in out['reviews']}==set(mapping)
 if valid:valid=all(set(x.get('scores',{}))==set(WEIGHTS) and all(type(v) in [int,float] and 0<=v<=4 for v in x['scores'].values()) for x in out['reviews'])
 write(p,{'valid':valid,'mapping':mapping,'lens':lens,'result':r});print({'reviewed':tid,'lens':lens,'valid':valid},flush=True)

def main(lens,ready=False):
 model='gpt-5.6-sol' if lens=='business-owner' else 'gpt-5.6-terra'
 c.PROVIDERS['openai']=(model,'https://api.openai.com/v1/chat/completions','OPENAI_API_KEY',5 if 'sol' in model else 2.5,20 if 'sol' in model else 12)
 tasks=TASKS if not ready else [t for t in TASKS if len(list((OUT/'safe-runs').glob(t[0]+'-*.json')))==6]
 with ThreadPoolExecutor(max_workers=1) as ex:
  for f in as_completed([ex.submit(one,t,lens) for t in tasks]):f.result()
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--lens',choices=['business-owner','agency-owner'],required=True);p.add_argument('--ready',action='store_true');a=p.parse_args();main(a.lens,a.ready)
