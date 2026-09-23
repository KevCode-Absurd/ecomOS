"""Nine frozen Luna comparisons. Same facts, three briefs, three instruction conditions."""
import argparse,hashlib,html,json,random,time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import peach_visual as v
from build_library import read,write
from calibration_client import ROOT,Budget

OUT=ROOT/'data/ad-copy-playbook-test-v1'
MODEL='gpt-6-luna'
COMMON='Use only supplied brand facts. Do not invent testimonials, certifications, scarcity, safety guarantees, product quantities or compatibility. Keep the offer fixed. Audience motivations are hypotheses, not observed customer research. No browsing or live actions. Return JSON with variants (each: concept, primary_text, headline, cta), and internal_notes. Write exactly three variants, each primary text 40-90 words; these are test-specific length constraints.'
TASKS=[
 ('installation','Write three static Meta ad copy variants for a parent considering childproofing but unsure how to get started with installation. Use the available support claim without inventing ease, tools, compatibility or installation time.', ['4fb56bc1019fff1c2b939750','8e6c32baa35ff2f2aa1ef544']),
 ('value','Write three static Meta ad copy variants helping a product-aware shopper understand what the six-part kit offers at the listed price. Keep the offer unchanged; no invented savings versus competitors or individual component prices.', ['d5db0dddac4ab42c3d5640c1','40638b840ce1e28ea89b4b19']),
 ('reassurance','Write three static Meta ad copy variants for parents who want practical reassurance before buying. We have no approved reviews or certifications to quote. Use available product information and support without implying the home becomes child-safe.', ['a9db8de6d903f43da80e956e','3f95809c1b82aca30df46509'])]

def prepare():
 pack=read(ROOT/'playbooks/ad-copy-v1.1/ad-copy-deployment/playbook.json')
 old=read(ROOT/'data/peach-web-benchmark/brand.json')
 facts={k:old[k] for k in ('name','market','currency','product_url')}
 facts['observations']={k:old['website_observations'][k] for k in ('observed_on','status','kit','listed_price','voice','offer_claims')}
 facts['constraints']='Availability unknown: no scarcity. Policy eligibility details not supplied; do not expand policies. Adult supervision remains necessary. These are saved website observations, not a fresh website check.'
 facts['visual_brief']='Same assumed creative for every condition: product-kit photograph on a plain cream background. No image is supplied to the model; do not claim to inspect a photograph.'
 cards={c['id']:c for c in read(ROOT/'data/library-v3/cards.json')['cards']}
 jobs=[]
 for tid,brief,ids in TASKS:
  started=time.perf_counter()
  selected=[cards[cid] for cid in ids]
  retrieval_ms=(time.perf_counter()-started)*1000
  knowledge=[{k:c[k] for k in ('id','title','use_when','steps','caveats')} for c in selected]
  for arm in ('generic','playbook','playbook_cards'):
   user=dict(brand=facts,brief=brief,response_format='Return a JSON object using the requested schema.')
   system='You are an ecommerce ad copywriter. Write clear persuasive copy.'
   if arm!='generic':
    system=pack['system_prompt']
    user['playbook']={'version':pack['version'],'principles':pack['editorial_principles'],
                     'workflow_steps':pack['workflows'][0]['steps']}
   if arm=='playbook_cards':user['supporting_cards']=knowledge
   payload={'model':MODEL,'instructions':system+'\n'+COMMON,'input':[{'role':'user','content':json.dumps(user,ensure_ascii=False)}],
            'reasoning':{'effort':'medium'},'store':False,'max_output_tokens':4000,'text':{'format':{'type':'json_object'}}}
   jobs.append(dict(id=tid+'-'+arm,task=tid,arm=arm,payload=payload,
      card_ids=ids if arm=='playbook_cards' else [],retrieval_ms=retrieval_ms if arm=='playbook_cards' else 0,
      selection='Editorially selected ID lookup; no keyword or semantic search. Timing excludes catalog loading and human curation.'))
 manifest=dict(model=MODEL,reasoning='medium',jobs=jobs,source_fact_date=facts['observations']['observed_on'],
   limitations=['One sample per brief/condition; no statistical performance claim.',
     'Tests selected context, not automatic search relevance or full website-to-copy workflow.',
     'No web, images, external actions or automated taste judge.',
     'Costs are conservative estimates using input $0.125/M and output $0.50/M; no cache discounts.'],
   rate_source='https://developers.openai.com/api/docs/models/gpt-6-luna',maximum_new_commitment_usd=1)
 path=OUT/'manifest-corrected.json'
 if path.exists():return read(path)
 write(path,manifest);return manifest

def run():
 manifest=prepare();v.setup()
 # Existing visual/global ledgers remain enforced; add a stricter cap for this round.
 def one(job):
  path=OUT/'runs'/(job['id']+'.json')
  if path.exists():return
  cap=Budget(OUT/'spend.sqlite',1,1)
  rid=hashlib.sha256(json.dumps(job['payload'],sort_keys=True).encode()).hexdigest()
  try:
   cap.reserve(rid,'openai-responses',0.02)
   response=v.api.response(job['payload'])
   cap.settle(rid,response['cost_upper_estimate_usd'])
   raw='\n'.join(z['text'] for x in response['body'].get('output',[]) if x.get('type')=='message' for z in x.get('content',[]) if z.get('type')=='output_text')
   try:output=json.loads(raw)
   except ValueError:output={'raw_output':raw}
   write(path,{'job':job,'response':response,'output':output})
   print(json.dumps({'completed':job['id'],'status':response['body'].get('status'),'cost_upper_usd':response['cost_upper_estimate_usd']}),flush=True)
  finally:cap.close()
 jobs=manifest['jobs'].copy();random.Random(913).shuffle(jobs)
 with ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(one,jobs))

def report():
 manifest=prepare();runs={p.stem:read(p) for p in (OUT/'runs').glob('*.json')}
 rows=[];panels=[];key={}
 for tid,brief,_ in TASKS:
  arms=['generic','playbook','playbook_cards'];random.Random(tid).shuffle(arms)
  cells=[]
  for label,arm in zip('ABC',arms):
   rid=tid+'-'+arm;key[tid+'-'+label]=arm
   if rid not in runs:cells.append('<article><h3>'+label+'</h3><p>Not completed</p></article>');continue
   run=runs[rid];r=run['response'];usage=r['body'].get('usage',{})
   rows.append(dict(task=tid,arm=arm,model=MODEL,input_tokens=usage.get('input_tokens'),output_tokens=usage.get('output_tokens'),
     cached_input_tokens=usage.get('input_tokens_details',{}).get('cached_tokens'),
     reasoning_tokens=usage.get('output_tokens_details',{}).get('reasoning_tokens'),
     generation_seconds=round(r['seconds'],2),retrieval_ms=run['job']['retrieval_ms'],cards=len(run['job']['card_ids']),
     cost_upper_usd=r['cost_upper_estimate_usd'],status=r['body'].get('status')))
   output=run['output'];body=''
   for i,ad in enumerate(output.get('variants',[]),1):
    body+='<h4>Variant '+str(i)+'</h4>'+''.join('<p><b>'+html.escape(k)+':</b> '+html.escape(str(ad.get(k,'')))+'</p>' for k in ('concept','primary_text','headline','cta'))
   if not body:body='<pre>'+html.escape(json.dumps(output,ensure_ascii=False,indent=2))+'</pre>'
   body+='<details><summary>Internal notes</summary><pre>'+html.escape(json.dumps(output.get('internal_notes',[]),ensure_ascii=False,indent=2))+'</pre></details>'
   cells.append('<article><h3>Option '+label+'</h3>'+body+'</article>')
  panels.append('<section><h2>'+html.escape(tid.title())+'</h2><p>'+html.escape(brief)+'</p><div class="grid">'+''.join(cells)+'</div></section>')
 write(OUT/'metrics.json',rows);write(OUT/'blind-key.json',key)
 total=sum(r['cost_upper_usd'] for r in rows)
 review='<h1>Peach Bucket: blind ad-copy comparison</h1><p>Nine Luna responses; three briefs × three conditions. Same facts and output constraints. Options are shuffled per brief. Judge usefulness before opening the key.</p><p>For each brief: choose A/B/C or tie, note what you would actually use, edits required, and any unsupported claims.</p>'
 trace='<h2>Audit and metrics</h2><details><summary>Reveal condition key</summary><pre>'+html.escape(json.dumps(key,indent=2))+'</pre></details><details><summary>Tokens, latency and cost</summary><pre>'+html.escape(json.dumps(rows,indent=2))+'</pre></details>'
 for job in manifest['jobs']:
  trace+='<details><summary>Exact input: '+html.escape(job['id'])+'</summary><pre>'+html.escape(json.dumps(job,ensure_ascii=False,indent=2))+'</pre></details>'
 doc='<!doctype html><meta charset="utf-8"><title>Ad copy playbook comparison</title><style>body{font:16px system-ui;margin:32px;color:#16242c;background:#f6f7f8}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}article{background:white;padding:22px;border:1px solid #ccd4d8;border-radius:10px}section{margin:36px 0}pre{white-space:pre-wrap;overflow-wrap:anywhere}h4{border-top:1px solid #ddd;padding-top:18px}details{margin:14px 0}@media(max-width:950px){.grid{grid-template-columns:1fr}}</style>'+review+''.join(panels)+trace
 (ROOT/'AD_COPY_PLAYBOOK_COMPARISON.html').write_text(doc,encoding='utf-8')
 (ROOT/'AD_COPY_PLAYBOOK_RESULTS.md').write_text('# Ad-copy playbook comparison\n\nCompleted responses: '+str(len(rows))+'/9. Conservative generation estimate: $'+format(total,'.6f')+'.\n\nNo quality winner has been assigned. Owner review is pending. One sample per cell; selected-ID retrieval is not an automatic retrieval benchmark. Facts were reused from the saved 2026-09-23 website snapshot, not freshly verified.\n\nExact inputs, outputs, usage and latency are in data/ad-copy-playbook-test-v1. The HTML shows shuffled options and a collapsible condition key.\n',encoding='utf-8')
 print(json.dumps({'responses':len(rows),'cost_upper_usd':total,'metrics':rows}))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('phase',choices=['prepare','run','report']);a=p.parse_args()
 {'prepare':prepare,'run':run,'report':report}[a.phase]()
