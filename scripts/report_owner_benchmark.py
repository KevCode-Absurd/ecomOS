"""Offline, self-contained comparison document; no external scripts or services."""
import json,csv,statistics,html,hashlib,sqlite3
from benchmark_v3 import OUT,TASKS,MODELS,METHODS,RUBRIC,BRAND,SYSTEM
from build_library import read,write
import calibration_client as c

def metrics(r,grades):
 calls=[r['first']]+([r['final']] if r['final']['request_id']!=r['first']['request_id'] else [])
 def count(k):return sum(x['usage'].get(k,0) for x in calls)
 def detail(k,d):return sum(x['usage'].get(k,{}).get(d,0) for x in calls)
 row={'task':r['task'],'model':r['model'],'method':r['method'],'cards':len(r['card_ids']),'knowledge_tokens_once':r['knowledge_tokens'],
 'input_tokens_total':count('prompt_tokens'),'completion_tokens_total':count('completion_tokens'),
 'reasoning_tokens_total':detail('completion_tokens_details','reasoning_tokens'),'cached_input_tokens_total':detail('prompt_tokens_details','cached_tokens'),
 'first_input_tokens':r['first']['usage']['prompt_tokens'],'first_completion_tokens':r['first']['usage']['completion_tokens'],
 'first_seconds':r['first']['seconds'],'generation_seconds_total':sum(x['seconds'] for x in calls),'search_ms':r['retrieval_ms'],
 'selector_seconds':r['selector_seconds'],'generation_cost_usd':sum(x['booked_cost_usd'] for x in calls),'selector_cost_usd':r['selector_cost'],
 'cold_workflow_seconds':sum(x['seconds'] for x in calls)+r['retrieval_ms']/1000+r['selector_seconds'],
 'cold_workflow_cost_usd':sum(x['booked_cost_usd'] for x in calls)+r['selector_cost'],
 'first_checks_pass':r['first_validation']['all_pass'] if r['first_validation'] else '',
 'final_checks_pass':r['final_validation']['all_pass'] if r['final_validation'] else '',
 'superseded_revision_cost_usd':r.get('superseded_final',{}).get('booked_cost_usd',0),
 'superseded_revision_seconds':r.get('superseded_final',{}).get('seconds',0),
 'validation_protocol':r.get('validation_protocol','original')}
 for lens,g in grades.items():
  row[lens+'_score_0_to_4']=sum(g['scores'][k]*v/100 for k,v in RUBRIC.items())
  row[lens+'_verdict']=g['owner_verdict'];row[lens+'_editing']=g['editing_burden']
 row['mean_owner_score_0_to_4']=statistics.mean(row[l+'_score_0_to_4'] for l in grades)
 row['both_use']=all(g['owner_verdict']=='use' for g in grades.values())
 return row

def main():
 data={'brand':BRAND,'system':SYSTEM,'tasks':TASKS,'cards':read(OUT/'card-catalog.json'),'packets':{},'audits':{},'runs':{},'reviews':{}}
 rows=[]
 for t in TASKS:
  tid=t['id'];data['packets'][tid]=read(OUT/'packets'/f'{tid}.json')
  ap=OUT/'retrieval-audits'/f'{tid}.json'
  data['audits'][tid]=read(ap) if ap.exists() else None
  reviews={lens:read(OUT/'reviews'/f'{tid}-{lens}.json') for lens in ['business-owner','agency-owner']}
  assert all(r['valid'] for r in reviews.values())
  data['reviews'][tid]=reviews
  for model in MODELS:
   for method in METHODS:
    key=f'{tid}-{model}-{method}';r=read(OUT/'runs'/f'{key}.json');grades={}
    for lens,review in reviews.items():
     label=next(k for k,v in review['mapping'].items() if v=={'model':model,'method':method})
     grades[lens]=next(g for g in review['result']['output']['reviews'] if g['label']==label)
    row=metrics(r,grades);rows.append(row);data['runs'][key]={'trace':r,'metrics':row,'grades':grades}
 with (OUT/'metrics.csv').open('w',newline='',encoding='utf-8') as f:
  writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
 groups=[]
 for model in MODELS:
  for method in METHODS:
   rs=[r for r in rows if r['model']==model and r['method']==method]
   groups.append({'model':model,'method':method,'mean_owner_score':statistics.mean(r['mean_owner_score_0_to_4'] for r in rs),
    'both_use_count':sum(r['both_use'] for r in rs),'first_checks_pass_count':sum(r['first_checks_pass'] is True for r in rs),'final_checks_pass_count':sum(r['final_checks_pass'] is True for r in rs),
    'mean_input_tokens':statistics.mean(r['input_tokens_total'] for r in rs),'mean_completion_tokens':statistics.mean(r['completion_tokens_total'] for r in rs),
    'mean_cold_cost_usd':statistics.mean(r['cold_workflow_cost_usd'] for r in rs),'median_cold_seconds':statistics.median(r['cold_workflow_seconds'] for r in rs),
    'median_generation_seconds':statistics.median(r['generation_seconds_total'] for r in rs)})
 pairs=[]
 for model in MODELS:
  for t in TASKS:
   rr={r['method']:r for r in rows if r['task']==t['id'] and r['model']==model}
   pairs.append({'model':model,'task':t['id'],'raw_minus_none':rr['raw']['mean_owner_score_0_to_4']-rr['none']['mean_owner_score_0_to_4'],
    'selected_minus_none':rr['selected']['mean_owner_score_0_to_4']-rr['none']['mean_owner_score_0_to_4'],
    'selected_minus_raw':rr['selected']['mean_owner_score_0_to_4']-rr['raw']['mean_owner_score_0_to_4']})
 with (OUT/'paired-deltas.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(pairs[0]));w.writeheader();w.writerows(pairs)
 budgets={}
 for name in ['ecommerce-benchmark-v2',OUT.name]:
  b=c.Budget(c.ROOT/'data'/name/'spend.sqlite',23,23);budgets[name]=b.summary();b.close()
 db=sqlite3.connect(c.ROOT/'data/spend.sqlite');embedding_cost=0
 for q in {q for t in TASKS for q in t['queries']}:
  payload={'model':'text-embedding-3-small','input':[q],'dimensions':512}
  rid='embedding-'+hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()
  row=db.execute('SELECT COALESCE(actual,reserved) FROM spend WHERE request_id=?',(rid,)).fetchone()
  if row:embedding_cost+=row[0]/1_000_000
 db.close()
 retrieval_metrics=[]
 for t in TASKS:
  p=data['packets'][t['id']];a=data['audits'][t['id']];ratings={x['id']:x['relevance'] for x in a['result']['output']['cards']}
  retrieval_metrics.append({'task':t['id'],'raw_cards':len(p['raw_ids']),'selected_cards':len(p['selected_ids']),'raw_tokens':p['raw_tokens'],'selected_tokens':p['selected_tokens'],
   'raw_direct_fraction':sum(ratings.get(k)=='direct' for k in p['raw_ids'])/len(p['raw_ids']),
   'selected_direct_fraction':sum(ratings.get(k)=='direct' for k in p['selected_ids'])/len(p['selected_ids']),
   'search_ms':p['search_ms'],'keyword_ms':a['keyword_ms'],'cached_hybrid_ms':a['cached_hybrid_ms'],'selector_seconds':p['selection']['seconds']})
 summary={'groups':groups,'paired_deltas':pairs,'budgets':budgets,'round_committed_excluding_embeddings':sum(b['committed_usd'] for b in budgets.values()),
 'query_embedding_cost_usd':embedding_cost,'round_committed_total_usd':sum(b['committed_usd'] for b in budgets.values())+embedding_cost,'retrieval_metrics':retrieval_metrics,
 'limitations':['Single fictional brand and one sample per cell; no statistical or revenue proof.','Reviewers are models simulating owner perspectives, not actual owners. Reviewer models share family with candidates; rankings can be biased.','First four tasks have an extra revision, applied equally to every condition. Structured checks cover only limited fields, not the entire artifact.','E1/E3 original checks confused equivalent field names/types with decision errors. All 18 affected conditions were revised again from their INITIAL draft using corrected semantic checks. Original revisions are preserved. Per-workflow metrics show the active draft+corrected-revision path; discarded diagnostic revision costs/timing are separate and included in the budget ledger.','Queries were authored for the experiment and frozen across models. Autonomous query planning and live platform tool execution are not tested.','No exhaustive relevance labels over all 7611 cards: cannot claim full recall. Metadata and freshness labels are inferred, not independently verified.','Costs are conservative estimates, not invoices; every input token charged at cache-write allowance.','Concurrency influences observed latency. Cold workflow sums serial stages; cached packets can remove selection latency.','No new Astra comparison; earlier easier tasks cannot establish Terra beats Astra.','Different prompts from V1/V2 prevent direct historical score comparisons.']}
 write(OUT/'summary.json',summary);data['summary']=summary
 # Escaping prevents source text from creating HTML/script content.
 blob=json.dumps(data,ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
 template='''<!doctype html><html><head><meta charset="utf-8"><title>Ecommerce intelligence: owner-value comparison</title><style>
 body{font:15px system-ui,sans-serif;margin:24px;color:#15212e;background:#f6f8fa}h1{font-size:26px}select{font:inherit;padding:8px;max-width:100%}.toolbar{position:sticky;top:0;background:#f6f8fa;padding:12px 0;border-bottom:1px solid #bbc5ce;z-index:2}.grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}.panel{background:white;padding:18px;border:1px solid #ccd4dd;border-radius:8px;min-width:0}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:13px ui-monospace,monospace;line-height:1.5}details{margin:12px 0;border-top:1px solid #eee;padding-top:8px}summary{cursor:pointer;font-weight:600}.note{background:#fff0c7;padding:12px}table{border-collapse:collapse;width:100%;font-size:13px}td,th{padding:7px;border:1px solid #d0d8df;text-align:left}a{color:#165bac}.muted{color:#596775}@media(max-width:850px){.grid{grid-template-columns:1fr}}@media print{.toolbar{position:static}details{display:block}body{margin:0}.grid{display:block}}</style></head><body>
 <h1>Ecommerce intelligence: owner-value comparison</h1><p>9 workflows · Luna, Terra, Sol · no cards / broad cards / selected cards. All answers are fictional drafts. No campaigns, emails or pages were published.</p>
 <p class="note">Reviews simulate a business owner and an agency owner. They are not real customer ratings. The library is expert-sourced, but applicability and current accuracy are not guaranteed. Exact inputs, card text and outputs are below.</p>
 <details><summary>Experiment summary and limitations</summary><pre id="overview"></pre></details>
 <details><summary>Brand profile and common system instructions</summary><pre id="brand"></pre></details>
 <div class="toolbar"><label>Task <select id="task"></select></label> <label>Output stage <select id="stage"><option value="final">Final (after validation where applicable)</option><option value="first">Initial draft</option></select></label></div>
 <h2 id="tasktitle"></h2><pre id="taskrequest"></pre>
 <details><summary>Step 1–2: search queries, retrieved cards, applicability selection and relevance audit</summary><pre id="retrieval"></pre><div id="cardlist"></div></details>
 <div class="grid"><div class="panel"><select id="left"></select><div id="leftpanel"></div></div><div class="panel"><select id="right"></select><div id="rightpanel"></div></div></div>
 <script id="dataset" type="application/json">__DATA__</script><script>
 const D=JSON.parse(document.getElementById('dataset').textContent),$=id=>document.getElementById(id),models=['gpt-5.6-luna','gpt-5.6-terra','gpt-5.6-sol'],methods=['none','raw','selected'];
 function pre(text){let e=document.createElement('pre');e.textContent=typeof text==='string'?text:JSON.stringify(text,null,2);return e;}
 function detail(parent,title,value){let d=document.createElement('details'),s=document.createElement('summary');s.textContent=title;d.append(s,pre(value));parent.append(d);}
 D.tasks.forEach(t=>$('task').add(new Option(t.id+' — '+t.title,t.id)));
 for(const side of ['left','right'])for(const m of models)for(const method of methods)$(side).add(new Option(m+' / '+method,m+'|'+method));
 $('left').value='gpt-5.6-terra|none';$('right').value='gpt-5.6-terra|selected';
 $('overview').textContent=JSON.stringify(D.summary,null,2);$('brand').textContent=JSON.stringify({brand:D.brand,system:D.system},null,2);
 function render(){let tid=$('task').value,t=D.tasks.find(t=>t.id===tid),p=D.packets[tid];$('tasktitle').textContent=t.title;$('taskrequest').textContent=t.request;
 $('retrieval').textContent=JSON.stringify({queries:t.queries,raw_cards:p.raw_ids.length,selected_cards:p.selected_ids.length,raw_tokens:p.raw_tokens,selected_tokens:p.selected_tokens,search_ms:p.search_ms,selection_seconds:p.selection.seconds,selection:p.selection.output,audit:D.audits[tid]?.result?.output,keyword_ms:D.audits[tid]?.keyword_ms,cached_hybrid_ms:D.audits[tid]?.cached_hybrid_ms},null,2);
 $('cardlist').replaceChildren();for(const id of p.raw_ids){let x=D.cards[id];detail($('cardlist'),(p.selected_ids.includes(id)?'SELECTED · ':'EXCLUDED · ')+x.card.title+' ['+id+']',x);}
 for(const side of ['left','right']){let [model,method]=$(side).value.split('|'),r=D.runs[tid+'-'+model+'-'+method],box=$(side+'panel'),call=r.trace[$('stage').value];box.replaceChildren();
 detail(box,'Step 3: exact input sent to this model',{system:D.system,input:call.input});
 detail(box,'Metrics: tokens, costs, retrieval and total latency',r.metrics);
 detail(box,'Cards in this context ('+r.trace.card_ids.length+')',r.trace.card_ids.map(id=>({id,title:D.cards[id].card.title})));
 let h=document.createElement('h3');h.textContent='Step 4: complete '+$('stage').value+' output';box.append(h,pre(call.output?.answer_markdown||call.raw_content));
 detail(box,'Structured actions, questions and self-reported card use',call.output);
 detail(box,'Step 5: sandbox checks (limited field validation)',{first:r.trace.first_validation,final:r.trace.final_validation});
 detail(box,'Step 6: business-owner and agency-owner reviews of FINAL output',r.grades);
 detail(box,'Exact provider usage and request identifiers',{request_id:call.request_id,model:call.model,effort:call.effort,usage:call.usage,finish_reason:call.finish_reason});
 if(r.trace.superseded_final)detail(box,'Preserved superseded revision (original validator; excluded from quality comparison)',r.trace.superseded_final);}}
 ['task','stage','left','right'].forEach(id=>$(id).addEventListener('change',render));render();
 </script></body></html>'''
 (c.ROOT/'OWNER_BENCHMARK_COMPARISON.html').write_text(template.replace('__DATA__',blob),encoding='utf-8')
 lines=['# Ecommerce intelligence owner-value evaluation','', 'Nine workflows, three models, three retrieval methods. Complete side-by-side inputs, cards and outputs: [comparison document](OWNER_BENCHMARK_COMPARISON.html).','',
 '| Model | Context | Owner score /4 | Both reviewers: use /9 | Mean input tokens | Mean completion tokens | Mean cold cost | Median cold seconds |',
 '|---|---|---:|---:|---:|---:|---:|---:|']
 for g in groups:lines.append(f"| {g['model']} | {g['method']} | {g['mean_owner_score']:.2f} | {g['both_use_count']} | {g['mean_input_tokens']:.0f} | {g['mean_completion_tokens']:.0f} | ${g['mean_cold_cost_usd']:.4f} | {g['median_cold_seconds']:.1f} |")
 lines+=['','Scores are advisory model judgments. Completion tokens include reasoning. First four tasks include draft + revision; remaining five have one draft. Cold cost and latency include an unamortized selector for selected context. The selector was actually run once per task and reused.','',f"Current evaluation ledger including interrupted V2: ${summary['round_committed_excluding_embeddings']:.4f}, excluding tiny separately logged query embeddings.",'','## Process','',
 '1. Freeze the same fictional Shopify/Meta/Klaviyo brand and task for every condition.','2. Run two task-specific hybrid searches, merge duplicate IDs, and record all candidate cards.','3. Compare no cards, all broad candidates, and Luna-selected applicable cards. Selected text is copied intact with conditions; selection explanations never enter the answer prompt.','4. Generate each deliverable with Luna, Terra and Sol at medium reasoning. Save exact input, output, usage and timing.','5. For inventory, audience, experiment and reconciliation tasks, run deterministic field checks and allow exactly one revision for every condition. No platform writes occur.','6. Randomize candidate labels for two simulated owner reviews. Evaluate practical usefulness, brand fit, correctness, clarity and handoff readiness.','7. Audit keyword versus hybrid candidates, coverage, applicability and freshness gaps. These are judgments about retrieved candidates, not complete-library recall.','', '## Task-by-task retrieval trace','']
 for t in TASKS:
  p=data['packets'][t['id']];lines.extend([f"### {t['id']}: {t['title']}",'',t['request'],'',f"Broad: {len(p['raw_ids'])} cards / {p['raw_tokens']} tokens. Selected: {len(p['selected_ids'])} cards / {p['selected_tokens']} tokens.",'','Selected cards:',''])
  lines.extend('- '+data['cards'][k]['card']['title']+' (`'+k+'`)' for k in p['selected_ids'])
  lines.append('')
 lines+=['## Limits','']+['- '+x for x in summary['limitations']]
 lines+=['','Pricing references: [Luna](https://developers.openai.com/api/docs/models/gpt-5.6-luna), [Terra](https://developers.openai.com/api/docs/models/gpt-5.6-terra), [Sol](https://developers.openai.com/api/docs/models/gpt-5.6-sol). Exact billed cost must be reconciled with the provider invoice.']
 (c.ROOT/'OWNER_BENCHMARK_RESULTS.md').write_text('\n'.join(lines),encoding='utf-8')
 # Human rating template makes an actual owner review possible without rerunning models.
 with (OUT/'human-owner-review.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.writer(f);w.writerow(['task','model','method','would_use','editing_minutes','usefulness_0_to_4','why','critical_error'])
  for r in rows:w.writerow([r['task'],r['model'],r['method'],'','','','',''])
 print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
