import json,statistics
from pathlib import Path
from build_library import read,write
from peach_web_case import OUT,TASKS
from run_peach_web import MODELS
def main():
 runs={p.stem:read(p) for p in (OUT/'safe-runs').glob('*.json')};checks=[];missing=[]
 for m in MODELS:
  for tid,_ in TASKS:
   a=runs.get(f'{tid}-{m}-web');b=runs.get(f'{tid}-{m}-web_cards')
   for arm,r in [('web',a),('web_cards',b)]:
    if not r:missing.append(f'{tid}-{m}-{arm}')
   if a and b:
    assert a['public_research_request_id']==b['public_research_request_id']
    assert a['calls'][0]['payload']['input'][0]==b['calls'][0]['payload']['input'][0]
    checks.append(f'{tid}-{m}')
 library={c['id'] for c in read(OUT.parent/'library-v3/cards.json')['cards']}
 retrieval=[x for r in runs.values() for x in r['retrieval']]
 assert all(set(x['result']['card_ids'])<=library for x in retrieval)
 assert all(len(x['cards'])==len(x['result']['card_ids']) for x in retrieval)
 summary={'completed_answers':len(runs),'matched_pairs':len(checks),'missing':missing,'retrieval_calls':len(retrieval),'median_retrieval_ms':statistics.median(x['result']['elapsed_ms'] for x in retrieval),'max_retrieval_ms':max(x['result']['elapsed_ms'] for x in retrieval),'all_card_ids_exist':True,'brand_and_research_inputs_equal_in_pairs':True}
 write(OUT/'audit.json',summary)
 lines=['# Findings and next changes','','This is a partial exploratory benchmark. The raw A/B document preserves all completed outputs, including weak ones. No outputs were rewritten after scoring.','', '## Concrete review findings','']
 for p in sorted((OUT/'reviews').glob('*.json')):
  rev=read(p)
  if not rev['valid']:continue
  lines.append('### '+p.stem)
  for g in rev['result']['output']['reviews']:
   ident=rev['mapping'][g['label']];lines+=['',f'**{ident["model"]} / {ident["arm"]}: {g["verdict"]}**',g['specific_evidence'],'Issues: '+'; '.join(g['material_issues'])]
 lines+=['','## What to improve before autonomous execution','','1. Ground generated claims in a brand-fact whitelist. Card advice is not proof that this brand has a feature, offer, certification, or service.','2. Use a deterministic calculator for contribution, break-even CPA, and funnel rates; have the answer cite its input values. Retrieval does not prevent arithmetic errors.','3. Retrieve by subtask, then remove duplicate or weak matches before the drafting call. Measure useful-card precision; the present audit verifies IDs and payload delivery, not exhaustive recall.','4. Ask the model to distinguish observed audience evidence from testable segments. Reddit anecdotes do not establish prevalence or willingness to pay.','5. Make deliverables ready for an operator: finished copy, assets needed, acceptance criteria, and measurement. Keep unknown mandatory facts as explicit pre-publish checks.','6. Next cost experiment: let a public-only researcher consult the library first and browse only for evidence gaps. Keep private customer and financial data out of that stage. This round cannot prove reduced web cost.','','## Mechanical audit','',json.dumps(summary,indent=2)]
 (OUT.parent.parent/'PEACH_BUCKET_FINDINGS.md').write_text('\n'.join(lines),encoding='utf-8');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
