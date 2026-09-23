import json,html,csv,sqlite3
from peach_writing_v2 import OUT
from peach_visual import ROOT,MODELS
from build_library import read,write
def main():
 rows=[];sections=[];review=read(OUT/'review.json') if (OUT/'review.json').exists() else None
 for model in MODELS:
  cols=[]
  for arm in ['none','old','routed']:
   p=OUT/'runs'/f'{model}-{arm}.json'
   if not p.exists():continue
   r=read(p);c=r['call'];ret=r['retrieval'];o=r['output'];grade=None
   if review and review['valid']:
    label=next(k for k,v in review['mapping'].items() if v=={'model':model,'arm':arm})
    grade=next(g for g in review['result']['output']['reviews'] if g['label']==label)
   row={'model':model,'arm':arm,'input_tokens':c['body']['usage']['input_tokens'],'output_tokens':c['body']['usage']['output_tokens'],'cost_upper_usd':c['cost_upper_estimate_usd'],'model_seconds':c['seconds'],'knowledge_tokens':sum(x['result']['knowledge_tokens'] for x in ret),'retrieval_ms':sum(x['result']['elapsed_ms'] for x in ret),'unique_cards':len({k for x in ret for k in x['result']['card_ids']}),'copy_score':grade['copy_score_0_to_4'] if grade else None};rows.append(row)
   def detail(title,obj):return '<details><summary>'+html.escape(title)+'</summary><pre>'+html.escape(json.dumps(obj,ensure_ascii=False,indent=2))+'</pre></details>'
   cols.append('<article><h2>'+{'none':'No cards','old':'Previous retrieval','routed':'Routed + copy principles'}[arm]+'</h2>'+detail('Cost, tokens and speed',row)+detail('Blinded copy review',grade)+'<h3>Hero headline</h3><p>'+html.escape(o['hero']['headline'])+'</p><h3>Ad copy</h3><pre>'+html.escape(o['ad']['primary_text'])+'</pre><b>'+html.escape(o['ad']['headline'])+'</b><h3>Full page copy</h3><pre>'+html.escape(o['landing_page_markdown'])+'</pre>'+detail('Sources, queries and exact context',ret)+detail('Full output and visual briefs',o)+detail('Exact model request and response',c)+'</article>')
  sections.append('<h1>'+model+'</h1><div class="grid">'+''.join(cols)+'</div>')
 page='''<!doctype html><meta charset="utf-8"><title>Writing retrieval improvement</title><style>body{font:16px system-ui;color:#213a34;background:#f6f4ef;margin:24px}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}article{background:white;padding:20px;min-width:0}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:14px/1.5 system-ui}details{border:1px solid #ddd;padding:10px;margin:10px 0}details pre{max-height:450px;overflow:auto;font:12px monospace}summary{cursor:pointer}h1{margin-top:35px}@media(max-width:1000px){.grid{display:block}}</style><h1>Peach Bucket — writing and retrieval improvement</h1><p>Same revised writing prompt, brand facts, task and frozen model-specific plan in all three conditions. Only the retrieved context changes. This round tests copy and visual briefs; it does not regenerate images.</p><p>Scores are one blinded simulated agency-owner review of copy, not actual sales or owner satisfaction. Existing packets are reused in the old condition; retrieval times are original recorded timings, not a simultaneous speed race.</p>'''+''.join(sections)
 (ROOT/'PEACH_BUCKET_WRITING_V2.html').write_text(page,encoding='utf-8')
 if rows:
  with (OUT/'metrics.csv').open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 write(OUT/'summary.json',{'runs':len(rows),'metrics':rows,'generation_cost_usd':sum(r['cost_upper_usd'] for r in rows)})
 print(json.dumps({'runs':len(rows),'generation_cost':sum(r['cost_upper_usd'] for r in rows)},indent=2))
if __name__=='__main__':main()
