"""Offline complete trace and paired report. No paid calls."""
import json,csv,sqlite3,statistics,html,hashlib
from pathlib import Path
from peach_web_case import OUT,TASKS
from run_peach_web import MODELS
from review_peach_web import WEIGHTS
from build_library import read,write
ROOT=OUT.parent.parent
def main():
 reviews={p.stem:read(p) for p in (OUT/'reviews').glob('*.json')}
 rows=[];traces={}
 for p in sorted((OUT/'safe-runs').glob('*.json')):
  r=read(p)
  if r['status']!='complete':continue
  pub=read(Path(r['research_file']));calls=[pub['response']]+r['calls']
  assert all(not c['web_calls'] and all(t['type']=='function' for t in c['payload']['tools']) for c in r['calls'])
  public_input=json.loads(pub['response']['payload']['input'][0]['content'])
  assert set(public_input)=={'public_brand','owner_request'}
  ret=r['retrieval'];grades={}
  for lens in ['business-owner','agency-owner']:
   review=reviews.get(r['task_id']+'-'+lens)
   if review and review['valid']:
    label=next(k for k,v in review['mapping'].items() if v=={'model':r['model'],'arm':r['arm']})
    grades[lens]=next(g for g in review['result']['output']['reviews'] if g['label']==label)
  scores=[sum(g['scores'][k]*w/100 for k,w in WEIGHTS.items()) for g in grades.values()]
  row={'task':r['task_id'],'model':r['model'],'arm':r['arm'],'input_tokens':sum(c['body']['usage']['input_tokens'] for c in calls),'output_tokens':sum(c['body']['usage']['output_tokens'] for c in calls),
   'reasoning_tokens':sum(c['body']['usage'].get('output_tokens_details',{}).get('reasoning_tokens',0) for c in calls),'cached_tokens':sum(c['body']['usage'].get('input_tokens_details',{}).get('cached_tokens',0) for c in calls),
   'workflow_cost_upper_usd':sum(c['cost_upper_estimate_usd'] for c in calls),'workflow_seconds':pub['response']['seconds']+r['private_stage_seconds'],
   'research_seconds':pub['response']['seconds'],'private_seconds':r['private_stage_seconds'],'retrieval_ms':sum(x['result']['elapsed_ms'] for x in ret),
   'web_tool_items':pub['response']['web_calls'],'knowledge_calls':len(ret),'unique_cards':len({k for x in ret for k in x['result']['card_ids']}),'knowledge_tokens_returned':sum(x['result']['knowledge_tokens'] for x in ret),
   'owner_score':statistics.mean(scores) if scores else None,'review_count':len(scores)}
  rows.append(row);traces[p.stem]={'run':r,'public_research':pub,'metrics':row,'grades':grades}
 with (OUT/'safe-metrics.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 groups=[];pairs=[]
 for model in MODELS:
  for arm in ['web','web_cards']:
   rs=[r for r in rows if r['model']==model and r['arm']==arm]
   scored=[r['owner_score'] for r in rs if r['owner_score'] is not None]
   if rs:groups.append({'model':model,'arm':arm,'n':len(rs),'scored':len(scored),'score':statistics.mean(scored) if scored else None,'cost':statistics.mean(r['workflow_cost_upper_usd'] for r in rs),'seconds':statistics.median(r['workflow_seconds'] for r in rs),'input':statistics.mean(r['input_tokens'] for r in rs),'output':statistics.mean(r['output_tokens'] for r in rs),'cards':statistics.mean(r['unique_cards'] for r in rs)})
  for tid,_ in TASKS:
   rr={r['arm']:r for r in rows if r['task']==tid and r['model']==model}
   if len(rr)==2:
    a,b=rr['web'],rr['web_cards'];pairs.append({'task':tid,'model':model,'score_delta':b['owner_score']-a['owner_score'] if a['owner_score'] is not None and b['owner_score'] is not None else None,'cost_delta':b['workflow_cost_upper_usd']-a['workflow_cost_upper_usd'],'seconds_delta':b['workflow_seconds']-a['workflow_seconds']})
 db=sqlite3.connect(OUT/'spend.sqlite');budget={s:{'requests':n,'usd':v} for s,n,v in db.execute('select status,count(*),sum(coalesce(actual,reserved))/1000000.0 from spend group by status')};db.close()
 queries={rr['query'] for x in traces.values() for rr in x['run']['retrieval']}
 db=sqlite3.connect(ROOT/'data/spend.sqlite');embedding_total=0
 for q in queries:
  rid='embedding-'+hashlib.sha256(json.dumps({'model':'text-embedding-3-small','input':[q],'dimensions':512},sort_keys=True).encode()).hexdigest()
  row=db.execute('select coalesce(actual,reserved) from spend where request_id=?',(rid,)).fetchone()
  if row:embedding_total+=row[0]/1e6
 db.close();budget['query_embeddings_upper']={'queries':len(queries),'usd':embedding_total}
 data={'tasks':TASKS,'models':MODELS,'brand':read(OUT/'brand.json'),'protocol':read(OUT/'safe-protocol.json'),'groups':groups,'pairs':pairs,'budget':budget,'traces':traces,'reviews':reviews}
 write(OUT/'safe-summary.json',{k:v for k,v in data.items() if k not in ['traces','reviews','brand','protocol']})
 payload=json.dumps(data,ensure_ascii=False).replace('<','\\u003c')
 page='''<!doctype html><meta charset="utf-8"><title>Peach Bucket paired benchmark</title><style>body{font:16px system-ui;margin:28px;color:#172535;background:#f5f7fa}select{padding:8px;max-width:70%}.grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}section,details{background:white;padding:16px;margin:12px 0;border:1px solid #ccd4df;border-radius:8px}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:13px ui-monospace;max-height:650px;overflow:auto}h1{font-size:26px}summary{cursor:pointer}table{border-collapse:collapse}td,th{padding:8px;border:1px solid #ccc}@media(max-width:850px){.grid{display:block}}</style><h1>Peach Bucket: web vs web + intelligence</h1><p>Eight owner requests · medium reasoning · same research within each model/task · simulated owner reviews. Private business analysis has no web tool. Costs are conservative estimates, not invoices.</p><div id="totals"></div><select id="task"></select> <select id="model"></select><div id="common"></div><div class="grid" id="compare"></div><details><summary>Brand facts and complete protocol</summary><pre id="protocol"></pre></details><script id="data" type="application/json">PAYLOAD</script><script>
 const d=JSON.parse(document.getElementById('data').textContent),$=x=>document.getElementById(x),esc=x=>String(x).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;'),pretty=x=>esc(JSON.stringify(x,null,2)),detail=(name,x)=>'<details><summary>'+esc(name)+'</summary><pre>'+pretty(x)+'</pre></details>';
 $('task').innerHTML=d.tasks.map(t=>'<option value="'+t[0]+'">'+esc(t[0]+' — '+t[1])+'</option>').join('');$('model').innerHTML=d.models.map(m=>'<option>'+m+'</option>').join('');
 $('totals').innerHTML=detail('Aggregate results, paired changes and budget',{groups:d.groups,pairs:d.pairs,budget:d.budget});$('protocol').textContent=JSON.stringify({brand:d.brand,protocol:d.protocol},null,2);
 function draw(){const base=$('task').value+'-'+$('model').value,rs=['web','web_cards'].map(a=>d.traces[base+'-'+a]);$('common').innerHTML=rs[0]?detail('Shared public research: exact request, queries, sources, memo',rs[0].public_research):'';$('compare').innerHTML=rs.map((x,i)=>{if(!x)return '<section>Pending</section>';const r=x.run;return '<section><h2>'+(['Web + brand facts','Web + brand facts + cards'][i])+'</h2>'+detail('Cost, latency and tokens',x.metrics)+'<h3>Answer</h3><pre>'+esc(r.output.answer_markdown||JSON.stringify(r.output))+'</pre>'+detail('Usable artifacts, questions and assumptions',r.output)+detail('Simulated owner and agency reviews',x.grades)+detail('Every retrieval: query, purpose, card IDs, full cards and exact compact context',r.retrieval)+detail('Every private model call: exact inputs, tool results, outputs and usage',r.calls)+'</section>'}).join('')};$('task').onchange=draw;$('model').onchange=draw;draw();
 </script>'''.replace('PAYLOAD',payload)
 (ROOT/'PEACH_BUCKET_WEB_COMPARISON.html').write_text(page,encoding='utf-8')
 lines=['# Peach Bucket web-enabled benchmark','',f'{len(rows)}/48 completed answers; {sum(r["valid"] for r in reviews.values())}/16 valid simulated owner/agency reviews.','', '| Model | Context | N | Owner score /4 | Mean cost upper estimate | Median seconds | Mean input/output tokens |','|---|---|---:|---:|---:|---:|---:|']
 for g in groups:lines.append(f'| {g["model"]} | {g["arm"]} | {g["n"]} | {g["score"] if g["score"] is not None else "pending"} | ${g["cost"]:.4f} | {g["seconds"]:.1f} | {g["input"]:.0f} / {g["output"]:.0f} |')
 lines+=['','## Interpretation and limits','','Quality is primary. Scores are blinded simulated owner/agency judgments, not real customer satisfaction or measured sales lift. One answer per condition is exploratory; model-family judge bias and run variance remain.','Both arms receive identical public research for each model/task. Across models, research can differ. This tests cards after equal research; it does not establish fewer web searches or lower end-to-end cost from replacing research.','Every independent-request estimate includes full research cost, although that shared memo was billed once for the pair. All reasoning tokens are part of output totals. Cache discounts are not applied; billed cost may be lower. Web action items are conservatively counted at $0.01 each. Query embeddings are separate from these request estimates.','Exact API inputs, knowledge context and final outputs are recorded. Hosted search exposes sources/actions and aggregate usage, not all internal search snippets or page-by-page token allocation. Retrieval cannot prove all relevant cards were found; self-reported applied IDs cannot prove causal use.','Known facts: new store; sales reversals were test orders; 39 orders and 34 converted sessions are different metrics. Real customer order count is unknown. ₹2,233.02 at a ₹3,299 selling price is contribution before ads, RTO and other unconfirmed costs, not net profit.','Initial combined web/private run was stopped after automatic approval review rejected possible private-data leakage into search queries. The approved replacement structurally separates public research from private analysis. Old runs are excluded from quality results and retained in budget accounting.','','## Budget ledger','',json.dumps(budget,indent=2),'','Settled amounts are conservative usage estimates. Reserved amounts are unresolved or active requests, not proven charges; they remain counted toward the cap. Check provider billing to reconcile interrupted calls.','','Open PEACH_BUCKET_WEB_COMPARISON.html for A/B answers, artifacts, cards and exact traces. Machine-readable metrics are in data/peach-web-benchmark/safe-metrics.csv.']
 (ROOT/'PEACH_BUCKET_WEB_RESULTS.md').write_text('\n'.join(lines),encoding='utf-8');print(json.dumps({'runs':len(rows),'reviews':len(reviews),'budget':budget,'groups':groups},indent=2))
if __name__=='__main__':main()
