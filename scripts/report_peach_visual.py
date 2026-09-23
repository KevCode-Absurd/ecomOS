import json,html,csv,sqlite3
from pathlib import Path
from peach_visual import ROOT,OUT,MODELS
from build_library import read,write
def main():
 rows=[];sections=[]
 for model in MODELS:
  cols=[]
  for arm in ['none','cards']:
   key=f'{model}-{arm}';p=OUT/'runs'/f'{key}.json'
   if not p.exists():cols.append('<article>Pending</article>');continue
   r=read(p);o=r['output'];calls=r['calls'];ret=r['retrieval']
   row={'model':model,'retrieval':arm,'input_tokens':sum(c['body']['usage']['input_tokens'] for c in calls),'output_tokens':sum(c['body']['usage']['output_tokens'] for c in calls),'text_cost_upper_usd':sum(c['cost_upper_estimate_usd'] for c in calls),'model_seconds':sum(c['seconds'] for c in calls),'retrieval_ms':sum(x['result']['elapsed_ms'] for x in ret),'unique_cards':len({k for x in ret for k in x['result']['card_ids']}),'knowledge_tokens':sum(x['result']['knowledge_tokens'] for x in ret)};rows.append(row)
   def detail(title,obj):return '<details><summary>'+html.escape(title)+'</summary><pre>'+html.escape(json.dumps(obj,ensure_ascii=False,indent=2))+'</pre></details>'
   render_records={a:read(OUT/'deliverables'/key/(a+'-render.json')) for a in ['hero','ad'] if (OUT/'deliverables'/key/(a+'-render.json')).exists()}
   row['image_generation_seconds']=sum(x['seconds'] for x in render_records.values()) if len(render_records)==2 else None
   row['image_cost_usd']=None
   images=detail('Image render timings and provenance',render_records)
   review_path=OUT/'copy-review.json'
   if review_path.exists():
    review=read(review_path)
    if review['valid']:
     label=next(k for k,v in review['mapping'].items() if v=={'model':model,'arm':arm})
     grade=next(g for g in review['result']['output']['reviews'] if g['label']==label)
     row['simulated_copy_score']=grade['copy_score_0_to_4']
     images+=detail('Blinded simulated agency-owner review (copy only)',grade)
   for asset in ['hero','ad']:
    img=OUT/'deliverables'/key/(asset+'.png')
    if img.exists():images+='<h3>'+('Landing-page hero section' if asset=='hero' else 'Square static ad')+'</h3><a href="'+img.relative_to(ROOT).as_posix()+'"><img src="'+img.relative_to(ROOT).as_posix()+'"></a>'
    else:images+='<p>'+asset+': rendering pending</p>'
   cols.append('<article><h2>'+('With intelligence cards' if arm=='cards' else 'Without intelligence cards')+'</h2>'+detail('Tokens, text costs and retrieval',row)+images+'<h3>Ad copy</h3><pre>'+html.escape(o['ad']['primary_text'])+'</pre><p><b>'+html.escape(o['ad']['headline'])+'</b> · '+html.escape(o['ad']['cta'])+'</p><h3>Complete landing-page copy</h3><pre>'+html.escape(o['landing_page_markdown'])+'</pre>'+detail('Audience, offer and pre-launch checks',{k:o.get(k) for k in ['audience_and_offer','assumptions_and_prelaunch_checks','applied_card_ids']})+detail('Image prompts',{k:o[k]['image_prompt'] for k in ['hero','ad']})+detail('Queries, cards, exact retrieved text',ret)+detail('Exact API calls and responses',calls)+'</article>')
  sections.append('<section><h1>'+model+'</h1><div class="pair">'+''.join(cols)+'</div></section>')
 budget=sqlite3.connect(OUT/'spend.sqlite').execute('select status,count(*),sum(coalesce(actual,reserved))/1000000.0 from spend group by status').fetchall()
 page='''<!doctype html><meta charset="utf-8"><title>Peach Bucket visual A/B</title><style>body{font:16px system-ui;background:#f5f1ec;color:#243733;margin:28px}header{max-width:1000px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:24px}article{background:#fff;padding:22px;border-radius:12px;min-width:0}img{width:100%;height:auto}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:14px/1.55 system-ui}details pre{max-height:550px;overflow:auto;font:12px monospace}details{border:1px solid #ddd;padding:12px;margin:10px 0}summary{cursor:pointer}section{margin:45px 0}h1{font-size:28px}h3{margin-top:28px}@media(max-width:900px){.pair{display:block}article{margin-bottom:20px}}</style><header><h1>The Peach Bucket — visual comparison</h1><p>Three GPT-6 models × with/without retrieval. Same brand facts, planning step, public research and product references. Each output includes full landing-page copy, a complete hero section and one square ad with matching copy.</p><p>Images use the same built-in image-generation tool with each model's brief. This isolates the briefing workflow, not different image models. Image tools do not expose billable token/cost usage here; text API estimates below exclude unreported image cost. One sample per condition; visual quality is not conversion performance.</p><p>Customer copy is draft material. Review product representation, claims, policies and eligibility before launch. No assets have been published.</p></header>'''+''.join(sections)
 (ROOT/'PEACH_BUCKET_VISUAL_COMPARISON.html').write_text(page,encoding='utf-8')
 if rows:
  with (OUT/'metrics.csv').open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 write(OUT/'summary.json',{'metrics':rows,'text_budget':budget,'image_usage':'Built-in image tool; billing/token usage not exposed','image_count':len(list((OUT/'deliverables').glob('*/*.png')))})
 print(json.dumps({'rows':len(rows),'budget':budget,'images':len(list((OUT/'deliverables').glob('*/*.png')))},indent=2))
if __name__=='__main__':main()
