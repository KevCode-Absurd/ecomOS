"""Frozen conversational-copy revision and matched, blinded editorial test."""
import copy,json,random,html,statistics,argparse,re
from pathlib import Path
import optimise_ad_copy as o
from build_library import read,write
from calibration_client import ROOT
from benchmark_copy_playbook import COMMON

OUT=ROOT/'data/ad-copy-bridge-v1'
PACK=ROOT/'playbooks/ad-copy-v1.3'
ARMS=('generic','v1.2','v1.3')
REPORT_STEM='AD_COPY_BRIDGE'
PROMPT='''Write finished ecommerce ad copy in simple, natural English. Aim below a 10th-grade reading level: familiar words, short clear sentences, one thought at a time. Read it as something a person would say, not a marketing presentation. Do not sacrifice accuracy or necessary policy terms to a reading-level target.
For the supplied avatar, identify a specific unwanted situation, a realistic desired improvement, and the supported product feature that connects them. Show that connection naturally. The product is a practical bridge, not the hero of a grand transformation. The before can be a small frustration or hesitation; the after can be a modest useful gain. Never manufacture anxiety or promise total safety, effortless parenting or guaranteed results. Aspirations must fit what this product can actually help with.
Choose a genuinely different angle for each variant. Use one concrete everyday detail and one main benefit per ad. Explain how a relevant feature helps this person, instead of listing everything in the box. Let an informed shopper's question determine whether to lead with the feature, benefit or objection. Do not force a before/after template, labels, dramatic story or question opening into every ad.
Make the headline clear beside the supplied visual. The body adds a useful reason to care; the CTA is the natural next step. Use warm direct language without jargon, slogans, filler, forced rhyme or vague phrases such as unlock, elevate, game-changer, ultimate solution or peace of mind without a concrete explanation. Simple does not mean childish. Preserve the brand voice when supported examples exist.
Use only supplied product facts. Cards provide writing methods, never product proof. Never invent quantities, fit, setup time, tools, ease, testimonials, certifications, urgency, savings or safety outcomes. Keep policy eligibility intact. Hypothetical customer moments are scenarios, not research findings. Missing information belongs in internal_notes, not invented customer-facing claims. State necessary qualifications once, naturally.
Before delivering, check avatar fit, the credible problem-to-benefit connection, plain language, specific details, distinct angles and factual support. Make one editing pass if needed. Deliver the requested JSON with finished copy and separate internal_notes. Do not expose drafting instructions or planning. Do not browse or publish.'''
RUBRIC={
 'natural_language':{'weight':20,'good':'Sounds like a person talking to this shopper; plain familiar words, easy first read, approximately below grade 10.','bad':'Jargon, brochure voice, tangled sentences, childish or robotic simplification.'},
 'avatar_fit':{'weight':15,'good':'Speaks to the specific brief and plausible concern without invented customer research.','bad':'Generic parent copy or a scenario inconsistent with the brief.'},
 'credible_bridge':{'weight':20,'good':'Makes a realistic unwanted situation, desired improvement and supported product mechanism connect naturally, even implicitly.','bad':'Grand transformation, empty reassurance, missing mechanism, forced Before/After labels or unsupported outcome.'},
 'benefit':{'weight':15,'good':'Gives a practical reason this feature matters to this person.','bad':'Inventory dump or vague aspiration without useful gain.'},
 'visual_specificity':{'weight':10,'good':'A concrete object or action makes the message easy to picture.','bad':'Abstractions, overwriting or fabricated evidence.'},
 'crispness':{'weight':10,'good':'Every sentence earns its place, clear headline and natural CTA.','bad':'Padding, repeated disclaimers or stock marketing language.'},
 'distinctiveness':{'weight':10,'good':'Three genuinely different useful angles.','bad':'Repeated idea with different opening synonyms.'}}
FRESH={
 'exploring-cupboards':'Write three static Meta ad copy variants for a parent whose child is starting to explore cupboards. Help them consider the kit as part of preparing their home. This is a hypothetical audience scenario, not customer research. Do not imply any lock fits every cupboard or that the kit replaces supervision.',
 'grandparent-visits':'Write three static Meta ad copy variants for a grandparent preparing their home for visits from a young grandchild. Make the practical benefit relevant to visits without promising worry-free visits, universal compatibility or easy installation. This is a hypothetical audience scenario, not customer research.'}

def setup():
 o.OUT=OUT;o.v.setup();OUT.mkdir(parents=True,exist_ok=True)

def prepare():
 setup()
 if (OUT/'manifest.json').exists():return
 old=ROOT/'playbooks/ad-copy-v1.2'
 pack=read(old/'ad-copy-deployment/playbook.json')
 pack['version']='1.3.0-experimental';pack['system_prompt']=PROMPT
 pack['evidence_method']='Existing thirteen-card editorial synthesis plus explicitly user-requested plain-language and before/product/after criteria; not market-validated.'
 pack['editorial_principles'] += [{'id':'credible-before-after','guidance':'Connect this avatar\'s unwanted situation to a realistic improvement using a supported product mechanism. Do not force a transformation template.','source_card_ids':[],'origin':'User instruction; editorial hypothesis, not a claimed card quotation.'}]
 for w in pack['workflows']:
  w['steps'] += ['Identify the avatar, unwanted situation, realistic desired improvement and supported product mechanism for this brief.', 'Edit finished copy for conversational plain language, credible benefits and distinct angles; keep factual limits intact.']
  w['output_checks'] += ['A shopper can read this easily; aim below grade 10 without childish wording.', 'The desired improvement is credible and linked to a supplied feature.', 'Copy fits this avatar; no invented customer evidence.']
 write(PACK/'ad-copy-deployment/playbook.json',pack)
 for name in ('ad-copy-deployment/source-evidence.json','catalog.json','OPERATING_CONTRACT.md'):
  p=PACK/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text((old/name).read_text(encoding='utf-8'),encoding='utf-8')
 (PACK/'SYSTEM_PROMPT.md').write_text(PROMPT+'\n',encoding='utf-8')
 write(OUT/'rubric.json',{'criteria':RUBRIC,'scale':'0-5; 0 unusable, 1 major rewrite, 2 substantial edits, 3 usable with noticeable edits, 4 light edits, 5 exceptional.', 'limits':'AI editorial proxies; no measured reading grade, human preference or advertising performance. New rubric: old scores are not directly comparable.', 'stop':'One frozen revision; no rerolls to obtain a winning score.'})
 baseline=read(o.OLD/'manifest-corrected.json')['jobs'];jobs=[];reused=[]
 for j in baseline:
  if j['arm']!='generic':continue
  task=j['task'];u=json.loads(j['payload']['input'][0]['content'])
  for arm,path in [('generic',o.OLD/'runs'/f'{task}-generic.json'),('v1.2',ROOT/'data/ad-copy-optimisation-v1/runs'/f'v2-{task}-playbook.json')]:
   r=read(path);reused.append(dict(id=task+'-'+arm,task=task,arm=arm,facts=u['brand'],brief=u['brief'],output=r['output'],source=str(path)))
  jobs.append(make_job(j,task,'v1.3',u))
 base=next(j for j in baseline if j['task']=='value' and j['arm']=='generic')
 for task,brief in FRESH.items():
  for arm in ('generic','v1.2','v1.3'):
   u=json.loads(base['payload']['input'][0]['content']);u['brief']=brief;jobs.append(make_job(base,task,arm,u))
 write(OUT/'manifest.json',{'jobs':jobs,'reused':reused,'writer':'gpt-6-luna','design':'Five matched briefs, three arms. Six saved original outputs reused; nine new outputs. Two fresh same-brand briefs. No added cards; isolates compiled-playbook changes. Same facts, writer, reasoning and output constraints within each brief. Historical runs are not simultaneous repeats.','cap_usd':2})

def make_job(base,task,arm,u):
 payload=copy.deepcopy(base['payload'])
 if arm!='generic':
  pack=read(ROOT/f'playbooks/ad-copy-{arm}/ad-copy-deployment/playbook.json')
  payload['instructions']=pack['system_prompt']+'\n'+COMMON
  u['playbook']={'version':pack['version'],'principles':pack['editorial_principles'],'workflow_steps':pack['workflows'][0]['steps']}
 payload['input'][0]['content']=json.dumps(u,ensure_ascii=False)
 return dict(id=task+'-'+arm,task=task,arm=arm,facts=u['brand'],brief=u['brief'],payload=payload)

def generate():
 setup();m=read(OUT/'manifest.json')
 for j in m['jobs']:
  p=OUT/'runs'/(j['id']+'.json')
  if p.exists():continue
  r=o.call(j['payload'],j['id'])
  if len(r['output'].get('variants',[]))!=3:raise ValueError('Invalid output retained; no reroll')
  write(p,{**{k:j[k] for k in ('id','task','arm','facts','brief')},'output':r['output']})
  print(j['id'],r['response']['cost_upper_estimate_usd'],flush=True)

def rows():return read(OUT/'manifest.json')['reused']+[read(p) for p in sorted((OUT/'runs').glob('*.json'))]

def readability(text):
 # Diagnostic only: spelling-based syllable estimates are noisy, especially for short ads.
 words=re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?",text)
 sentences=max(1,len(re.findall(r'[.!?]+(?:\s|$)',text)))
 def syllables(word):
  w=word.lower();n=len(re.findall('[aeiouy]+',w))
  if w.endswith('e') and not w.endswith(('le','ye')):n-=1
  return max(1,n)
 if not words:return {'words':0,'estimated_grade':None}
 return {'words':len(words),'sentences':sentences,'estimated_grade':round(.39*len(words)/sentences+11.8*sum(map(syllables,words))/len(words)-15.59,1),'method':'Approximate Flesch-Kincaid with heuristic syllables; English primary text only, noisy for short ads, not a compliance gate.'}

def response_for(row):
 if row.get('source'):
  p=Path(row['source']);r=read(p)
  if 'response' in r:return r['response']
  return read(p.parent.parent/r.get('call_path','calls/'+r['id']+'.json'))['response']
 return read(OUT/'calls'/(row['id']+'.json'))['response']

def review():
 setup();rs=rows()
 expected=len(read(OUT/'manifest.json')['jobs'])+len(read(OUT/'manifest.json')['reused'])
 if len(rs)!=expected:raise ValueError('Incomplete candidates')
 schema={k:0 for k in RUBRIC}
 for model in o.REVIEWERS:
  path=OUT/'reviews'/(model+'.json')
  if path.exists():continue
  shuffled=rs.copy();random.Random('bridge-'+model).shuffle(shuffled)
  mapping={f'C{i:02}':r['id'] for i,r in enumerate(shuffled)}
  instructions=o.JUDGE[:o.JUDGE.index('Return JSON only:')]+ 'Return JSON only with reviews, one per label. Each review has label, scores using exactly these keys: '+json.dumps(schema)+', strength, priority_fix, and issues (exact quote, severity material|ambiguity|style, reason). Use the supplied rubric and the anchored 0-5 scale. Do not claim to measure an exact reading grade. No numerical conversion predictions.'
  payload={'model':model,'instructions':instructions,'input':[{'role':'user','content':json.dumps({'format':'Return JSON.','rubric':RUBRIC,'candidates':[{'label':label,'brief':r['brief'],'brand_facts':r['facts'],'copy':r['output']['variants']} for label,r in zip(mapping,shuffled)]},ensure_ascii=False)}],'reasoning':{'effort':'medium'},'store':False,'max_output_tokens':12000,'text':{'format':{'type':'json_object'}}}
  result=o.call(payload,'review-'+model);rv=result['output'].get('reviews',[])
  valid=len(rv)==expected and {x.get('label') for x in rv}==set(mapping) and all(set(x.get('scores',{}))==set(RUBRIC) and all(type(n) in (int,float) and 0<=n<=5 for n in x['scores'].values()) for x in rv)
  write(path,{'valid':valid,'mapping':mapping,'output':result['output']})
  if not valid:raise ValueError('Invalid review retained')
  print('review',model,result['response']['cost_upper_estimate_usd'],flush=True)

def report():
 rs=rows();byid={r['id']:r for r in rs};scores=[]
 for model in o.REVIEWERS:
  rv=read(OUT/'reviews'/(model+'.json'))
  if not rv['valid']:raise ValueError('Invalid review')
  for x in rv['output']['reviews']:
   cid=rv['mapping'][x['label']];r=byid[cid]
   text=json.dumps(r['output']['variants'],ensure_ascii=False)
   for issue in x['issues']:
    quote=issue.get('quote',issue.get('exact_quote',''))
    issue['quote_verified']=bool(quote) and quote in text
   scores.append(dict(id=cid,task=r['task'],arm=r['arm'],reviewer=model,score=sum(x['scores'][k]*RUBRIC[k]['weight']/5 for k in RUBRIC),review=x))
 write(OUT/'scores.json',scores)
 calls=[read(p)['response'] for p in (OUT/'calls').glob('*.json')];cost=sum(c['cost_upper_estimate_usd'] for c in calls)
 decision=read(OUT/'decision.json') if (OUT/'decision.json').exists() else {}
 lines=['# Plain-language and credible-benefit experiment','',read(OUT/'manifest.json')['design'],'','AI editorial ratings, not market performance. Natural readability was judged; a separate heuristic reading-grade estimate is only a diagnostic. Scores use a new rubric and cannot be directly compared with earlier reports. No fresh website verification.','$'+f'{cost:.6f} estimated new API cost (conservative rates; no cache discount).','', '| Condition | All briefs /100 | Initial three | Additional briefs |','|---|---:|---:|---:|']
 for arm in ARMS:
  mean=lambda fresh:statistics.mean(s['score'] for s in scores if s['arm']==arm and (fresh is None or (s['task'] in FRESH)==fresh))
  lines.append(f'| {arm} | {mean(None):.1f} | {mean(False):.1f} | {mean(True):.1f} |')
 if decision:lines+=['',decision['summary'],'',decision['limitations']]
 diagnostics=[]
 for r in rs:
  response=response_for(r);usage=response['body'].get('usage',{})
  diagnostics.append({'id':r['id'],'arm':r['arm'],'seconds':response.get('seconds'),'cost_upper_estimate_usd':response['cost_upper_estimate_usd'],'usage':usage,'readability':[readability(x.get('primary_text','')) for x in r['output']['variants']]})
 write(OUT/'candidate-metrics.json',diagnostics)
 lines+=['','| Condition | Mean input tokens | Mean output tokens | Mean seconds | Mean cost/request | Approx. reading grade |','|---|---:|---:|---:|---:|---:|']
 for arm in ARMS:
  ds=[d for d in diagnostics if d['arm']==arm]
  avg=lambda k:statistics.mean(d['usage'].get(k,0) for d in ds)
  grades=[a['estimated_grade'] for d in ds for a in d['readability'] if a['estimated_grade'] is not None]
  seconds=[d['seconds'] for d in ds if d['seconds'] is not None]
  lines.append(f"| {arm} | {avg('input_tokens'):.0f} | {avg('output_tokens'):.0f} | {statistics.mean(seconds):.1f} | ${statistics.mean(d['cost_upper_estimate_usd'] for d in ds):.6f} | {statistics.mean(grades):.1f} |")
 lines+=['','Output tokens include provider-reported reasoning tokens. Latency is the saved response-call duration; reused runs happened earlier, so timing is descriptive, not a controlled speed benchmark. Grade uses a spelling-based syllable heuristic on primary text only; inspect the actual copy rather than using the number as a pass/fail rule.','', '## Exact outputs and reviewer comments','']
 esc=lambda s:html.escape(str(s))
 summary_html=[];in_table=False
 for line in lines:
  if line.startswith('|'):
   if not in_table:summary_html.append('<table>');in_table=True
   if set(line.replace('|','').replace(':','').replace(' ',''))=={'-'}:continue
   summary_html.append('<tr>'+''.join('<td>'+esc(cell.strip())+'</td>' for cell in line.strip('|').split('|'))+'</tr>')
  else:
   if in_table:summary_html.append('</table>');in_table=False
   if line and not line.startswith('#'):summary_html.append('<p>'+esc(line)+'</p>')
 if in_table:summary_html.append('</table>')
 page=['<!doctype html><meta charset="utf-8"><title>Ad copy: plain-language experiment</title><style>body{font:16px/1.5 system-ui;margin:30px;background:#f5f4f0;color:#212121}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}.arm{background:white;padding:22px;border-radius:12px}h1,h2{line-height:1.2}pre{white-space:pre-wrap;overflow-wrap:anywhere}summary{cursor:pointer}small{color:#555}table{border-collapse:collapse;background:white;margin:20px 0;width:100%}td{padding:10px;border-bottom:1px solid #ddd}tr:first-child{font-weight:bold;background:#e7ede8}@media(max-width:900px){.grid{grid-template-columns:1fr}}</style><h1>Plain language. Relevant benefits. A credible bridge.</h1>'+''.join(summary_html)]
 for task in sorted({r['task'] for r in rs}):
  page.append('<h2>'+esc(task)+'</h2><p>'+esc(next(r['brief'] for r in rs if r['task']==task))+'</p><div class="grid">')
  for arm in ARMS:
   r=next(r for r in rs if r['task']==task and r['arm']==arm);ss=[s for s in scores if s['id']==r['id']]
   page.append('<section class="arm"><h3>'+esc(arm)+f" · {statistics.mean(s['score'] for s in ss):.1f}/100</h3>")
   for variant in r['output']['variants']:
    page.append('<h4>'+esc(variant.get('headline',''))+'</h4><p>'+esc(variant.get('primary_text',''))+'</p><strong>'+esc(variant.get('cta',''))+'</strong><hr>')
   page.append('<details><summary>Exact review and flags</summary><pre>'+esc(json.dumps(ss,ensure_ascii=False,indent=2))+'</pre></details></section>')
   lines+=['### '+task+' / '+arm,'','```json',json.dumps(r['output'],ensure_ascii=False,indent=2),'```','',json.dumps(ss,ensure_ascii=False,indent=2),'']
  page.append('</div>')
 metrics=[]
 for p in sorted((OUT/'calls').glob('*.json')):
  r=read(p)['response'];metrics.append({'call':p.stem,'seconds':r.get('seconds'),'cost_upper_estimate_usd':r['cost_upper_estimate_usd'],'usage':r['body'].get('usage')})
 write(OUT/'metrics.json',metrics)
 page.append('<h2>New-call usage and latency</h2><pre>'+esc(json.dumps(metrics,indent=2))+'</pre><p>Exact prompts, responses, token usage, blinded labels and scores are saved under '+esc(OUT.relative_to(ROOT))+'. Reused outputs retain their previous run logs. Extra cards were not tested in this round.</p>')
 (ROOT/(REPORT_STEM+'_COMPARISON.html')).write_text('\n'.join(page),encoding='utf-8')
 (ROOT/(REPORT_STEM+'_RESULTS.md')).write_text('\n'.join(lines),encoding='utf-8')
 (PACK/'README.md').write_text('# '+PACK.name+' — experimental\n\nAdds the owner-requested plain-language, avatar and credible before/product/after checks to all three ad-copy workflows. The original thirteen supporting cards are preserved. No extra cards are injected by default.\n\nThis is an opt-in experimental revision. See '+REPORT_STEM+'_RESULTS.md at the project root for matched scores, limitations and exact outputs. AI ratings do not establish higher conversion or owner preference. Below-grade-10 is a writing target, not a measured guarantee. The other domain playbooks remain at their previous versions.\n',encoding='utf-8')
 if decision:
  with (PACK/'README.md').open('a',encoding='utf-8') as f:f.write('\n'+decision['summary']+'\n\n'+decision['limitations']+'\n\nSee [the complete decision](../../AD_COPY_ITERATION_DECISION.md).\n')
 print('\n'.join(lines[:12]))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('phase',choices=['prepare','generate','review','report']);a=p.parse_args();globals()[a.phase]()
