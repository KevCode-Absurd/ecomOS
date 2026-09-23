"""Aggregate benchmark outputs without treating automated judgments as ground truth."""
import csv,html,json,statistics,sqlite3
from run_ecommerce_benchmark import OUT,ROOT,ARMS,TASKS,RUBRIC,read,write

def score(review):
 s=review['scores']
 if set(s)!=set(RUBRIC) or any(type(v) not in (int,float) or not 0<=v<=4 for v in s.values()):raise ValueError('Invalid score')
 return sum(s[k]*w/4 for k,w in RUBRIC.items())


def usage_price(model,usage):
 prompt=usage['prompt_tokens'];output=usage['completion_tokens'];details=usage.get('prompt_tokens_details',{})
 if model.startswith('deepseek'):
  hit=usage.get('prompt_cache_hit_tokens',details.get('cached_tokens',0));miss=prompt-hit
  return (hit*0.006+miss*0.3+output*1.2)/1e6
 hit=details.get('cached_tokens',0);writes=details.get('cache_write_tokens',0)
 if hit+writes>prompt:raise ValueError('Invalid cache accounting')
 return ((prompt-hit-writes)*10+hit*1+writes*12.5+output*50)/1e6

def main():
 rows=[];judgments={};judge_details={}
 for task in TASKS:
  for j in ['deepseek','openai']:
   p=OUT/'judges-v2'/f"{task['id']}-{j}.json"
   if not p.exists():continue
   d=read(p)
   if d['status']!='complete':continue
   for review in d['output']['reviews']:
    key=(task['id'],d['mapping'][review['label']]);judgments.setdefault(key,[]).append(score(review))
    judge_details.setdefault(key,[]).append({'judge':d['judge_model'],**review})
 for task in TASKS:
  for arm in ARMS:
   p=OUT/'runs'/f"{task['id']}-{arm}.json"
   if not p.exists():continue
   r=read(p);scores=judgments.get((task['id'],arm),[])
   row={k:r.get(k) for k in ['task_id','arm','requested_model','returned_model','effort','status','generation_seconds','retrieval_ms','retrieval_warm_ms','estimated_end_to_end_seconds','generation_cost_upper_estimate_usd','knowledge_tokens','finish_reason']}
   row['usage_priced_generation_estimate_usd']=usage_price(r['requested_model'],r['usage'])+(usage_price(r['requested_model'],r['initial_usage']) if r.get('recovery_attempted') else 0)
   row.update(final_attempt_generation_seconds=r.get('final_attempt_generation_seconds',r['generation_seconds']),format_repair=r.get('format_repair'),task_kind=task['kind'],task_title=task['title'],initial_failed=r.get('initial_status',r['status'])!='complete',
    recovery_attempted=r.get('recovery_attempted',False),quality_score=statistics.mean(scores) if scores else None,
    judge_count=len(scores),judge_spread=max(scores)-min(scores) if scores else None,
    prompt_tokens=r['usage'].get('prompt_tokens'),completion_tokens=r['usage'].get('completion_tokens'),
    initial_prompt_tokens=r.get('initial_usage',r['usage']).get('prompt_tokens'),initial_completion_tokens=r.get('initial_usage',r['usage']).get('completion_tokens'))
   rows.append(row)
 aggregates=[]
 for arm in ARMS:
  group=[r for r in rows if r['arm']==arm];quality=[r['quality_score'] for r in group if r['quality_score'] is not None]
  if not group:continue
  aggregates.append({'arm':arm,'runs':len(group),'first_pass_successes':sum(not r['initial_failed'] for r in group),
   'eventual_successes':sum(r['status']=='complete' for r in group),'mean_quality':statistics.mean(quality) if quality else None,
   'median_end_to_end_seconds':statistics.median(r['estimated_end_to_end_seconds'] for r in group),
   'median_final_attempt_generation_seconds':statistics.median(r['final_attempt_generation_seconds'] for r in group),
   'mean_cost_upper_estimate_usd':statistics.mean(r['generation_cost_upper_estimate_usd'] for r in group),
   'mean_knowledge_tokens':statistics.mean(r['knowledge_tokens'] for r in group),
   'first_pass_quality_with_failures_zero':statistics.mean(0 if r['initial_failed'] else (r['quality_score'] or 0) for r in group)})
 pairs=[]
 for task in TASKS:
  rr={r['arm']:r for r in rows if r['task_id']==task['id']}
  for model in ['cheap','frontier']:
   a=rr.get(model+'_without');b=rr.get(model+'_with')
   if a and b and a['quality_score'] is not None and b['quality_score'] is not None:
    pairs.append({'task':task['id'],'model':model,'quality_delta':b['quality_score']-a['quality_score'],
     'cost_delta_usd':b['generation_cost_upper_estimate_usd']-a['generation_cost_upper_estimate_usd'],
     'latency_delta_seconds':b['estimated_end_to_end_seconds']-a['estimated_end_to_end_seconds']})
 db=sqlite3.connect(OUT/'spend.sqlite');actual,pending=db.execute('select coalesce(sum(actual),0),coalesce(sum(case when actual is null then reserved else 0 end),0) from spend').fetchone();db.close()
 result={'rows':rows,'aggregates':aggregates,'paired_deltas':pairs,'stage_cost_upper_estimate_usd':actual/1e6,'unresolved_reservations_usd':pending/1e6}
 write(OUT/'summary.json',result)
 with (OUT/'metrics.csv').open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 with (OUT/'paired-deltas.csv').open('w',newline='',encoding='utf-8-sig') as f:
  if pairs:w=csv.DictWriter(f,fieldnames=list(pairs[0]));w.writeheader();w.writerows(pairs)
 # A self-contained read-only comparison viewer. No keys, network requests, dependencies or execution controls.
 data=[]
 for task in TASKS:
  item={'task':task,'runs':[],'retrieval':read(OUT/'retrieval'/f"{task['id']}.json")}
  for arm in ARMS:
   p=OUT/'runs'/f"{task['id']}-{arm}.json"
   if p.exists():
    r=read(p);item['runs'].append({'arm':arm,'output':r.get('output'),'raw':r.get('raw_output'),'metrics':next(x for x in rows if x['task_id']==task['id'] and x['arm']==arm),'reviews':judge_details.get((task['id'],arm),[]),'first_attempt':read(OUT/'first-attempts'/p.name) if (OUT/'first-attempts'/p.name).exists() else None})
  data.append(item)
  parts=['# '+task['id']+' - '+task['title'],'',task['request'],'']
  for run in item['runs']:
   parts += ['## '+run['arm'],'',json.dumps(run['metrics'],ensure_ascii=False),'',run['output'].get('answer_markdown','') if isinstance(run['output'],dict) else (run['raw'] or 'No usable answer.'),'','Questions: '+json.dumps((run['output'] or {}).get('questions',[]),ensure_ascii=False),'','Automated reviews: '+json.dumps(run['reviews'],ensure_ascii=False),'']
  target=ROOT/'benchmark-results';target.mkdir(exist_ok=True)
  (target/(task['id']+'.md')).write_text('\n'.join(parts),encoding='utf-8')
 payload=json.dumps({'tasks':data,'summary':result},ensure_ascii=False).replace('<','\\u003c')
 page='''<!doctype html><html><head><meta charset="utf-8"><title>Ecommerce intelligence benchmark</title><style>body{font:15px system-ui;margin:24px;color:#17212b;background:#fafafa}select,button{padding:8px;margin:4px}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}.card{background:white;border:1px solid #ddd;padding:18px;min-width:0}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:14px/1.5 system-ui}.muted{color:#555}summary{cursor:pointer}table{border-collapse:collapse}td,th{padding:8px;border:1px solid #ddd}@media(max-width:800px){.grid{grid-template-columns:1fr}}</style></head><body><h1>Ecommerce intelligence benchmark</h1><p>Fictional TrailFold brand · 10 tasks · 4 conditions · Read-only drafts, no deployments.</p><p class="muted">Quality scores are automated judgments from two models, not measured revenue impact. One sample per condition. Costs are conservative estimates. Retry time and cost are included.</p><div id="overview"></div><select id="task"></select><label><input type="checkbox" id="blind"> Hide model/condition labels</label><div id="request"></div><div class="grid" id="runs"></div><details><summary>Retrieved knowledge and selection</summary><pre id="knowledge"></pre></details><script>const DATA=PAYLOAD;const sel=document.getElementById('task');DATA.tasks.forEach((x,i)=>{const o=document.createElement('option');o.value=i;o.textContent=x.task.id+' — '+x.task.title;sel.append(o)});const overview=document.getElementById('overview');const t=document.createElement('table');let head=t.insertRow();['Condition','Quality /100','First-pass success','Median total seconds','Mean estimated $'].forEach(v=>{let c=document.createElement('th');c.textContent=v;head.append(c)});DATA.summary.aggregates.forEach(x=>{let r=t.insertRow();[x.arm,x.mean_quality?.toFixed(1)??'pending',x.first_pass_successes+'/'+x.runs,x.median_end_to_end_seconds.toFixed(2),x.mean_cost_upper_estimate_usd.toFixed(4)].forEach(v=>r.insertCell().textContent=v)});overview.append(t);function render(){let x=DATA.tasks[sel.value],blind=document.getElementById('blind').checked;document.getElementById('request').textContent=x.task.request;const root=document.getElementById('runs');root.replaceChildren();x.runs.forEach((r,i)=>{let el=document.createElement('section');el.className='card';let h=document.createElement('h2');h.textContent=blind?'Answer '+(i+1):r.arm+' · '+r.metrics.returned_model;el.append(h);let m=document.createElement('p');m.textContent=blind?'':`Quality ${r.metrics.quality_score?.toFixed(1)??'pending'}/100 · ${r.metrics.estimated_end_to_end_seconds.toFixed(2)}s · $${r.metrics.generation_cost_upper_estimate_usd.toFixed(4)} · retry: ${r.metrics.recovery_attempted}`;el.append(m);let p=document.createElement('pre');p.textContent=r.output?.answer_markdown??r.raw??'No answer';el.append(p);let q=document.createElement('pre');q.textContent='Questions: '+JSON.stringify(r.output?.questions??[])+'\\nAssumptions: '+JSON.stringify(r.output?.assumptions??[]);el.append(q);let d=document.createElement('details'),s=document.createElement('summary');s.textContent='Metrics and automated reviews';d.append(s);let j=document.createElement('pre');j.textContent=JSON.stringify({metrics:r.metrics,reviews:r.reviews,first_attempt:r.first_attempt},null,2);d.append(j);el.append(d);root.append(el)});document.getElementById('knowledge').textContent=JSON.stringify({titles:x.retrieval.titles,tokens:x.retrieval.knowledge_tokens,first_ms:x.retrieval.elapsed_ms,warm_ms:x.retrieval.warm_ms},null,2)+'\\n\\n'+x.retrieval.context}sel.onchange=render;document.getElementById('blind').onchange=render;render();</script></body></html>'''.replace('PAYLOAD',payload)
 (ROOT/'BENCHMARK_COMPARISON.html').write_text(page,encoding='utf-8')
 print(json.dumps({'aggregates':aggregates,'stage_cost_upper_estimate_usd':actual/1e6,'pending':pending/1e6}))
if __name__=='__main__':main()
