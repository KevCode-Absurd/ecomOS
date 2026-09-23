"""Report blind AI scores with matched-task comparisons and preserved raw evidence."""
import html,json,re,statistics
from collections import defaultdict
from pathlib import Path
from optimise_ad_copy import OUT,OLD,ROOT,RUBRIC,REVIEWERS,candidates,summary
from build_library import read,write

def h(x):return html.escape(str(x))
def avg(xs):return round(statistics.mean(xs),2)

def main():
 scores=summary('final');rows={r['id']:r for r in candidates('final')}
 grouped=defaultdict(list);byid=defaultdict(list)
 for s in scores:
  byid[s['id']].append(s)
  if s['task']!='new-brief':grouped[(s['version'],s['arm'])].append(s)
 aggregates=[]
 for (version,arm),items in grouped.items():
  aggregates.append(dict(version=version,arm=arm,score=avg([x['score'] for x in items]),
    reviewer_scores={m:avg([x['score'] for x in items if x['reviewer']==m]) for m in REVIEWERS},
    criteria={k:avg([x['scores'][k]*20 for x in items]) for k in RUBRIC},
    material_flags=sum(sum(i['severity']=='material' for i in x['issues']) for x in items),
    ambiguity_flags=sum(sum(i['severity']=='ambiguity' for i in x['issues']) for x in items)))
 aggregates.sort(key=lambda x:(x['version'],x['arm']))
 write(OUT/'matched-aggregates.json',aggregates)
 metrics=[];checks=[]
 for cid,r in rows.items():
  if cid.startswith('v1-'):
   resp=read(OLD/'runs'/(cid[3:]+'.json'))['response']
  else:resp=read(OUT/r['call_path'])['response']
  u=resp['body']['usage']
  metrics.append(dict(id=cid,task=r['task'],arm=r['arm'],version=r['version'],model=resp['payload']['model'],
     input_tokens=u['input_tokens'],output_tokens=u['output_tokens'],reasoning_tokens=u.get('output_tokens_details',{}).get('reasoning_tokens'),
     seconds=resp['seconds'],cost_upper_usd=resp['cost_upper_estimate_usd']))
  ads=r['output']['variants'];texts=[a.get('primary_text','') for a in ads]
  checks.append(dict(id=cid,variants=len(ads),primary_word_counts=[len(re.findall(r"\b[\w’'-]+\b",t)) for t in texts],
     quantity_wording_hits=[t for t in texts if re.search(r'\bsix (?:items|pieces)\b',t,re.I)]))
  visible='\n'.join(str(a.get(k,'')) for a in ads for k in ('primary_text','headline','cta'))
  for s in byid[cid]:
   for issue in s['issues']:issue['quote_found_in_customer_copy']=issue['quote'] in visible
 write(OUT/'final-scores-audited.json',scores);write(OUT/'metrics.json',metrics);write(OUT/'mechanical-checks.json',checks)
 total=sum(read(p)['response']['cost_upper_estimate_usd'] for p in (OUT/'calls').glob('*.json'))
 columns=[('v1.1','generic'),('v1.1','playbook'),('v1.1','playbook_cards'),('v1.2','playbook'),('v1.2','playbook_cards')]
 table='| Condition | Score /100 | Sol | Luna |\n|---|---:|---:|---:|\n'
 for version,arm in columns:
  a=next(x for x in aggregates if (x['version'],x['arm'])==(version,arm))
  table+=f'| {version} {arm} | {a["score"]} | {a["reviewer_scores"]["gpt-6-sol"]} | {a["reviewer_scores"]["gpt-6-luna"]} |\n'
 notes='# Ad-copy optimisation results\n\n'+table+'\nThese are two blinded AI reviewers’ editorial scores, not owner approval or live ad performance. All five conditions were re-rated together in shuffled order under the same frozen rubric. The table uses only the original three matched briefs; the additional brief is reported separately.\n\n'
 notes+=f'New experiment cost estimate: ${total:.6f}, including initial reviews, nine new generations and final reviews. Earlier benchmark cost and reservations remain separate.\n\n'
 notes+='## Scope\n\nSix weighted criteria: clarity (20%), visual specificity (20%), pain relevance (15%), benefit (20%), crispness (15%), distinct variants (10%). Ratings 0–5 are converted to /100 by code. Factual issues are separate flags; unsupported claims cannot be justified by a high score. Reviewers receive original brand facts, brief, rubric/source summaries and anonymised customer copy, never writer prompts or condition labels.\n\n'
 notes+='The writer is Luna, medium reasoning, three variants per task. Brand facts, length requirements and original task-specific supplemental cards were held fixed. The v1.2 instruction package was frozen before generation. Existing generic outputs are reused, not independently regenerated for the matched briefs. A new same-brand brief received fresh generic/playbook/cards responses; it is a transfer check, not an independent-market holdout. Full-card retrieval is manually selected ID lookup, not a search benchmark.\n\n'
 notes+='## Additional brief\n\n'
 for cid,rs in byid.items():
  if rows[cid]['task']=='new-brief':notes+=f'- {rows[cid]["arm"]}: {avg([x["score"] for x in rs])}/100; individual scores '+', '.join(f'{x["reviewer"]}: {x["score"]}' for x in rs)+'.\n'
 notes+='\n## Limits and next decision\n\nOne brand, one generation per condition, same-family AI reviewers, subjective ordinal ratings and potential optimisation to the rubric. No statistics establish a general lift. Keep versions and failures, avoid repeated rerolls until a score improves, and assess new brands/real owner feedback before rollout. Exact generation and review prompts are in calls; mapping and reviews are retained. Original cards and v1.1 outputs are unchanged.\n'
 (ROOT/'AD_COPY_OPTIMISATION_RESULTS.md').write_text(notes,encoding='utf-8')
 markup='<h1>Ad-copy optimisation: scores and actual copy</h1><p>Two blinded AI reviewers. Scores are editorial proxies, not conversion results. Visual specificity means picturable language; no images were generated.</p><h2>Same three briefs: fair comparison</h2><table><tr><th>Condition</th><th>Score /100</th><th>Sol</th><th>Luna</th></tr>'
 for version,arm in columns:
  a=next(x for x in aggregates if (x['version'],x['arm'])==(version,arm))
  markup+='<tr><td>'+h(version+' '+arm)+'</td><td>'+h(a['score'])+'</td><td>'+h(a['reviewer_scores']['gpt-6-sol'])+'</td><td>'+h(a['reviewer_scores']['gpt-6-luna'])+'</td></tr>'
 markup+='</table><p>New experiment generation + reviews: $'+format(total,'.6f')+'. No winning-ad claim. Material factual issues override numerical ranking.</p><details><summary>Rubric and dimension scores</summary><pre>'+h(json.dumps({'rubric':RUBRIC,'scores':aggregates},indent=2))+'</pre></details>'
 for task in ('installation','value','reassurance','new-brief'):
  markup+='<h2>'+h(task)+'</h2><p>'+h(next(r['brief'] for r in rows.values() if r['task']==task))+'</p><div class="grid">'
  subset=[r for r in rows.values() if r['task']==task];subset.sort(key=lambda r:(r['version'],r['arm']))
  for r in subset:
   cid=r['id'];reviews=byid[cid]
   markup+='<article><h3>'+h(r['version']+' '+r['arm'])+'</h3><b>'+str(avg([s['score'] for s in reviews]))+'/100</b>'
   for i,a in enumerate(r['output']['variants'],1):
    markup+='<h4>Variant '+str(i)+': '+h(a.get('concept',''))+'</h4><p>'+h(a['primary_text'])+'</p><p><b>'+h(a['headline'])+'</b></p><p>'+h(a['cta'])+'</p>'
   markup+='<details><summary>Reviewer evidence and flags</summary><pre>'+h(json.dumps(reviews,ensure_ascii=False,indent=2))+'</pre></details>'
   markup+='<details><summary>Input/output tokens, latency and cost</summary><pre>'+h(json.dumps(next(m for m in metrics if m['id']==cid),indent=2))+'</pre></details></article>'
  markup+='</div>'
 markup+='<h2>Exact process and audit</h2><p>Read the results document for limitations. Calls below preserve full input context, full outputs, reviewer prompts and usage. No credentials are included.</p>'
 for p in sorted((OUT/'calls').glob('*.json')):
  markup+='<details><summary>'+h(p.stem)+'</summary><pre>'+h(json.dumps(read(p),ensure_ascii=False,indent=2))+'</pre></details>'
 doc='<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Copy optimisation results</title><style>body{font:16px system-ui;line-height:1.5;margin:28px;background:#f4f6f7;color:#15262d}table{border-collapse:collapse;background:white}td,th{padding:10px 18px;border:1px solid #ccd5d9;text-align:left}.grid{display:flex;gap:16px;overflow-x:auto;padding-bottom:18px}article{flex:0 0 350px;background:white;border:1px solid #ccd5d9;border-radius:12px;padding:20px}h4{border-top:1px solid #ddd;padding-top:16px}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:12px}details{margin:16px 0}h2{margin-top:36px}</style>'+markup
 (ROOT/'AD_COPY_OPTIMISATION_COMPARISON.html').write_text(doc,encoding='utf-8')
 print(json.dumps({'new_cost':total,'aggregates':aggregates,'new_brief':{cid:avg([s['score'] for s in rs]) for cid,rs in byid.items() if rows[cid]['task']=='new-brief'}},indent=2))

if __name__=='__main__':main()
