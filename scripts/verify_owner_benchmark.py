import hashlib,json
from benchmark_v3 import OUT,TASKS,MODELS,METHODS,BRAND
from build_library import read,write
import calibration_client as c

def main():
 assert len(list((OUT/'runs').glob('*.json')))==81
 for t in TASKS:
  p=read(OUT/'packets'/f"{t['id']}.json")
  assert set(p['selected_ids'])<=set(p['raw_ids'])
  for model in MODELS:
   for method in METHODS:
    r=read(OUT/'runs'/f"{t['id']}-{model}-{method}.json")
    for stage in ['first','final']:
     call=r[stage];assert call['finish_reason']=='stop'
     assert isinstance(call['output'].get('answer_markdown'),str) and call['output']['answer_markdown'].strip()
     assert call['input']['brand']==BRAND
     assert call['input']['reference_guidance']==(p[method] if method!='none' else '')
     assert set(call['output'].get('applied_card_ids',[]))<=set(r['card_ids'])
     assert call['model']==model
    if t['id'] in ['E1','E3']:assert r['validation_protocol']=='semantic-v2' and r['superseded_final']
  for lens in ['business-owner','agency-owner']:
   r=read(OUT/'reviews'/f"{t['id']}-{lens}.json");assert r['valid']
   assert len(r['result']['output']['reviews'])==9
  a=read(OUT/'retrieval-audits'/f"{t['id']}.json")
  assert a['result']['finish_reason']=='stop'
  assert {x['id'] for x in a['result']['output']['cards']}==set(a['union_ids'])
 assert hashlib.sha256((c.ROOT/'data/library-v3/cards.json').read_bytes()).hexdigest()==read(OUT/'library-fingerprint.json')['cards_sha256']
 summary=read(OUT/'summary.json');assert summary['round_committed_total_usd']<25
 assert summary['budgets'][OUT.name]['pending_requests']==0
 write(OUT/'verification.json',{'status':'passed','runs':81,'owner_reviews':18,'retrieval_audits':9,'identical_brand_and_packets_verified':True,'library_unchanged':True,'budget_below_25':True,'note':'Protocol integrity, not a claim of answer correctness or business lift.'})
 print('PASS: 81 outputs, 18 reviews, 9 audits, exact context parity, library unchanged, budget below $25.')
if __name__=='__main__':main()
