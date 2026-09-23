"""Frozen harder tasks, three context methods, deterministic sandbox validation."""
import argparse, json, time, random, hashlib, statistics, csv
from concurrent.futures import ThreadPoolExecutor, as_completed
import calibration_client as c
from benchmark_case import BRAND
from build_library import write, read
OUT=c.ROOT/'data/ecommerce-benchmark-v2'
STAGE='ecommerce-benchmark-v2'
TASKS=[
 {'id':'E1','title':'Inventory-aware acquisition and offer decision','request':'Use Shopify product economics, stock and Meta evidence to produce a 14-day acquisition decision and a usable campaign-change draft. Evaluate the proposed 20% Daypack discount at $30 CAC. Owner has not approved discounts. Reserve 30 Daypacks as an inventory buffer. Replenishment is 35 days away. Explain the distinction between ad CPA and total demand. Submit a proposed daily_total_daypack_units_cap, discount_percent and launch_status. Include actual ad copy, budget decision, dependencies and missing evidence.', 'queries':['ecommerce inventory constraints profitable acquisition contribution margin discount','Meta Ads creative testing budget scaling ecommerce']},
 {'id':'E2','title':'Build and test an abandonment audience','request':'Build a three-email checkout recovery draft and select exactly the eligible customer IDs from the event fixtures. Today is 2026-09-23T12:00:00Z. Eligibility: consent true; checkout at least 2 hours but no more than 48 hours ago; no subsequent purchase; not in welcome flow; no email in last 24h. No discount approved. Provide subjects, actual body copy, delays, purchase suppression, collision handling, and selected_customer_ids. Explain how Shopify events and Klaviyo eligibility interact. Draft only.', 'fixtures':[
 {'id':'c1','consent':True,'checkout_hours_ago':5,'purchased_after':False,'welcome_active':False,'last_email_hours_ago':50},
 {'id':'c2','consent':True,'checkout_hours_ago':8,'purchased_after':True,'welcome_active':False,'last_email_hours_ago':50},
 {'id':'c3','consent':False,'checkout_hours_ago':8,'purchased_after':False,'welcome_active':False,'last_email_hours_ago':50},
 {'id':'c4','consent':True,'checkout_hours_ago':8,'purchased_after':False,'welcome_active':True,'last_email_hours_ago':50},
 {'id':'c5','consent':True,'checkout_hours_ago':8,'purchased_after':False,'welcome_active':False,'last_email_hours_ago':12},
 {'id':'c6','consent':True,'checkout_hours_ago':1,'purchased_after':False,'welcome_active':False,'last_email_hours_ago':50},
 {'id':'c7','consent':True,'checkout_hours_ago':60,'purchased_after':False,'welcome_active':False,'last_email_hours_ago':50},
 {'id':'c8','consent':True,'checkout_hours_ago':48,'purchased_after':False,'welcome_active':False,'last_email_hours_ago':24}],
 'queries':['Klaviyo checkout abandonment purchase suppression flow filters consent','ecommerce abandoned checkout email copy sequence objections']},
 {'id':'E3','title':'Mobile PDP experiment with resource scheduling','request':'Produce implementation-ready mobile PDP copy, FAQ, section order, and an experiment configuration. Only 1200 eligible PDP sessions per week exist; baseline purchase rate 2%, minimum detectable absolute improvement 0.4 percentage points. Analyst supplied required sample 21000 sessions TOTAL; use it, do not recalculate a different test. Propose test_days, designer_hours, developer_hours, claimed_statistical_significance and launch_status. Build needs 6 designer and 3 developer hours; QA needs another 2 developer hours. Only 4 developer hours are available in week one, 4 in week two. Include schedule/dependencies and how you avoid false proof after a 14-day test. No verified 15-inch fit or speed data.', 'queries':['ecommerce mobile product page sizing shipping objections conversion','CRO experiment sample size low traffic prioritize qualitative testing']},
 {'id':'E4','title':'Cross-channel reconciliation and executable audit','request':'Create an order-level reconciliation table and a concrete next-week resource plan. Shopify net revenue 45000 includes a $1000 refund already deducted. Meta exported 400 orders totaling 48000; 80 Meta orders totaling 9600 are outside the Shopify reporting period. Klaviyo exported 120 orders totaling 14000, all in-period. Of in-period orders, 50 orders worth 6000 overlap Meta and Klaviyo. Compute in_period_meta_value, union_attributed_value and unassigned_shopify_value. These are attribution matches, not incremental sales. Build an audit task list with owner, acceptance test, dependency, hours and decision gates. Max analyst hours 6, developer 4, owner 2; do not double-subtract the refund or scale based on the blended attribution union.', 'queries':['ecommerce Shopify Meta Klaviyo attribution reconciliation revenue overlap','marketing measurement incrementality attribution ecommerce audit']}
]
SYSTEM='''Act as an ecommerce operator in a SIMULATED environment. Brand evidence and task fixtures govern; reference cards are conditional advice, never proof. Complete the requested artifacts, calculations and structured action proposal. Do not invent product claims, results, approvals or tool execution. Return JSON {"answer_markdown":"usable deliverable, 600-1000 words maximum", "actions":{...requested machine fields...},"questions":[at most 3 material questions],"applied_card_ids":[only actually useful card IDs],"rejected_guidance":[short reasons if any]}. Use numerical JSON values for numerical fields. All launch_status values must be draft or blocked. Do not omit action fields. You will receive sandbox validation feedback once and may correct your draft. No real changes are made.'''

def config(model):
 c.PROVIDERS['openai']=(model,'https://api.openai.com/v1/chat/completions','OPENAI_API_KEY',.25 if 'luna' in model else 2.5,1.2 if 'luna' in model else 12)

def validate(task,out):
 a=out.get('actions',{}) if isinstance(out,dict) else {}; checks={}
 def near(k,v):return type(a.get(k)) in (int,float) and abs(a[k]-v)<.02
 if task=='E1':
  checks={'inventory_buffer_respected':type(a.get('daily_total_daypack_units_cap')) in (int,float) and 0<a['daily_total_daypack_units_cap']<=180/35,
   'no_unapproved_discount':a.get('discount_percent')==0,'draft_only':a.get('launch_status') in ['draft','blocked']}
 elif task=='E2':checks={'audience_exact':sorted(a.get('selected_customer_ids',[]))==['c1','c8']}
 elif task=='E3':
  checks={'sample_duration':type(a.get('test_days')) in (int,float) and a['test_days']>=122.5,
   'build_and_qa_developer_hours':near('developer_hours',5),'designer_hours':near('designer_hours',6),
   'no_false_significance':a.get('claimed_statistical_significance') is False,'draft_only':a.get('launch_status') in ['draft','blocked']}
 else:checks={'meta_window':near('in_period_meta_value',38400),'deduplicated_union':near('union_attributed_value',46400),
   'negative_residual_preserved':near('unassigned_shopify_value',-1400)}
 return {'checks':checks,'passed':sum(checks.values()),'total':len(checks),'all_pass':all(checks.values()),'note':'Validates structured fields only; prose and business judgment require review. Negative reconciliation residual is a discrepancy, not negative real sales.'}

def prepare():
 from search_knowledge import engine
 OUT.mkdir(parents=True,exist_ok=True);e=engine()
 manifest={'brand':BRAND,'tasks':TASKS,'system':SYSTEM,'models':['gpt-5.6-luna','gpt-5.6-terra'],'methods':['none','raw','selected'],
 'reasoning':'medium','completion_limit':16384,'stage_cap_usd':10,'library_hash':hashlib.sha256((e.directory/'cards.json').read_bytes()).hexdigest(),
 'protocol':'4 harder tasks x 2 models x 3 methods x draft then validation/revision. Same tools, feedback, fixtures and prompts per pair. No live execution. No new Astra calls. One sample per cell; exploratory. Selector cost shared for frozen packets, amortization reported separately.'}
 if (OUT/'manifest.json').exists() and read(OUT/'manifest.json')!=manifest:raise ValueError('Frozen manifest mismatch')
 write(OUT/'manifest.json',manifest)
 for t in TASKS:
  p=OUT/'packets'/f"{t['id']}.json"
  if p.exists():continue
  start=time.perf_counter();ids=[];results=[]
  for q in t['queries']:
   r=e.search(q,token_budget=5000,max_cards=12);results.append(r)
   ids.extend(k for k in r['card_ids'] if k not in ids)
  raw='\n\n'.join(e.get_card(k)['guidance'] for k in ids)
  search_ms=(time.perf_counter()-start)*1000
  config('gpt-5.6-luna')
  selection=c.run_call(STAGE,'openai','medium','Select applicable reference cards for the supplied ecommerce task and brand. Return JSON {"selected_card_ids":[up to 8 IDs],"excluded":[{"id":"...","reason":"..."}],"applicability_notes":[...]}. Prefer distinct coverage of task needs, preserve useful conditions. Do not solve the task or add new tactics. Unknown applicability is conditional, not proven. Exclude irrelevant business models, prerequisites contradicted by brand facts, redundant advice. Do not select merely because keywords match.',{'brand':BRAND,'task':t['request'],'candidate_cards':raw},limit=4096,stage_limit=10)
  if not isinstance(selection['output'],dict) or selection['finish_reason']!='stop':raise ValueError('Selection invalid')
  chosen=selection['output'].get('selected_card_ids',[])
  if not isinstance(chosen,list) or len(chosen)>8 or len(set(chosen))!=len(chosen) or any(k not in ids for k in chosen):raise ValueError('Unknown/duplicate selection')
  selected='\n\n'.join(e.get_card(k)['guidance'] for k in chosen)
  write(p,{'raw':raw,'selected':selected,'raw_ids':ids,'selected_ids':chosen,'selection':selection,'search_ms':search_ms,
   'raw_tokens':len(e.encoding.encode(raw)),'selected_tokens':len(e.encoding.encode(selected)),'searches':results})
  print({'prepared':t['id'],'raw_cards':len(ids),'selected_cards':len(chosen)},flush=True)

def run_one(t,method):
 model=c.PROVIDERS['openai'][0];p=OUT/'runs'/f"{t['id']}-{model}-{method}.json"
 if p.exists():return
 packet=read(OUT/'packets'/f"{t['id']}.json")
 payload={'brand':BRAND,'task':t,'reference_guidance':packet[method] if method!='none' else ''}
 first=c.run_call(STAGE,'openai','medium',SYSTEM,payload,limit=16384,stage_limit=10)
 check=validate(t['id'],first['output'])
 second=c.run_call(STAGE,'openai','medium',SYSTEM,{**payload,'previous_draft':first['output'] or first['raw_content'],
  'sandbox_feedback':check,'instruction':'Inspect the draft and sandbox feedback; return the complete corrected deliverable and actions. Do not merely repeat pass/fail. Even passing numerical fields do not establish that prose is correct.'},limit=16384,stage_limit=10)
 out={'task':t['id'],'model':model,'method':method,'first':first,'final':second,'first_validation':check,'final_validation':validate(t['id'],second['output']),
  'complete':second['finish_reason']=='stop' and isinstance(second['output'],dict),
  'knowledge_tokens':packet.get(method+'_tokens',0),'retrieval_ms':packet['search_ms'] if method!='none' else 0,
  'selector_seconds':packet['selection']['seconds'] if method=='selected' else 0,
  'selector_cost':packet['selection']['booked_cost_usd'] if method=='selected' else 0}
 write(p,out);print({'run':p.stem,'complete':out['complete'],'checks':out['final_validation']},flush=True)

def generate(model):
 config(model);jobs=[(t,m) for t in TASKS for m in ['none','raw','selected']];random.Random(42).shuffle(jobs)
 with ThreadPoolExecutor(max_workers=3) as ex:
  fs=[ex.submit(run_one,*j) for j in jobs]
  for f in as_completed(fs):f.result()

def judge():
 config('gpt-5.6-terra')
 for t in TASKS:
  p=OUT/'reviews'/f"{t['id']}.json"
  if p.exists():continue
  runs=[read(x) for x in sorted((OUT/'runs').glob(t['id']+'-*.json'))];random.Random(t['id']).shuffle(runs)
  mapping={chr(65+i):{'model':r['model'],'method':r['method']} for i,r in enumerate(runs)}
  answers={chr(65+i):r['final']['output'] for i,r in enumerate(runs)}
  r=c.run_call(STAGE,'openai','medium','Evaluate anonymized ecommerce drafts. Return JSON {"reviews":[{"label":"A", "usefulness_0_to_4":0,"ready_for_operator_review":false,"critical_errors":[],"specific_value":[],"remaining_work":[],"evidence":"concrete excerpt or calculation"}],"summary":"..."}. Review every label. 0 unusable,1 major rework,2 substantial editing,3 minor editing,4 immediately usable as a DRAFT. No reward for verbosity or source usage. Check arithmetic, actual copy, implementation dependencies, margin, inventory, eligibility, evidence, and resource feasibility. Cards are optional guidance, not ground truth. Especially flag contradictions between structured fields and prose. An apparent attribution union above store revenue is unresolved data mismatch, not proof of incremental sales. Mark ready only if usable with no material corrections. You are an advisory model grader, not a business outcome test.',{'brand':BRAND,'task':t,'answers':answers,'sources':read(OUT/'packets'/f"{t['id']}.json")['raw']},limit=12000,stage_limit=10)
  write(p,{'mapping':mapping,'review':r});print({'reviewed':t['id']},flush=True)

def report():
 rows=[];texts=['# Ecommerce execution benchmark V2\n','Fictional cases; no production actions. One sample per task/condition. Automated usefulness is advisory. No new Astra calls.\n']
 for p in sorted((OUT/'runs').glob('*.json')):
  r=read(p);calls=[r['first'],r['final']];review=read(OUT/'reviews'/f"{r['task']}.json")
  label=next(k for k,v in review['mapping'].items() if v=={'model':r['model'],'method':r['method']})
  grade=next(x for x in review['review']['output']['reviews'] if x['label']==label)
  row={'task':r['task'],'model':r['model'],'method':r['method'],'input_tokens':sum(x['usage']['prompt_tokens'] for x in calls),
   'completion_tokens':sum(x['usage']['completion_tokens'] for x in calls),'reasoning_tokens':sum(x['usage'].get('completion_tokens_details',{}).get('reasoning_tokens',0) for x in calls),
   'knowledge_tokens':r['knowledge_tokens'],'generation_seconds':sum(x['seconds'] for x in calls),'retrieval_ms':r['retrieval_ms'],
   'selector_seconds':r['selector_seconds'],'generation_cost_usd':sum(x['booked_cost_usd'] for x in calls),'selector_cost_usd':r['selector_cost'],
   'first_all_checks':r['first_validation']['all_pass'],'final_all_checks':r['final_validation']['all_pass'],'usefulness':grade['usefulness_0_to_4'],'ready':grade['ready_for_operator_review']}
  rows.append(row)
  texts.extend([f"\n## {p.stem}\n",'Metrics: '+json.dumps(row)+'\n',r['final']['output'].get('answer_markdown',''), '\nActions:\n```json\n'+json.dumps(r['final']['output'].get('actions',{}),indent=2)+'\n```', '\nReview:\n```json\n'+json.dumps(grade,indent=2)+'\n```'])
 with (OUT/'metrics.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 summary=[]
 for model in ['gpt-5.6-luna','gpt-5.6-terra']:
  for method in ['none','raw','selected']:
   rr=[r for r in rows if r['model']==model and r['method']==method]
   summary.append({'model':model,'method':method,'mean_usefulness':statistics.mean(r['usefulness'] for r in rr),'ready_count':sum(r['ready'] for r in rr),
   'first_pass_count':sum(r['first_all_checks'] for r in rr),'final_pass_count':sum(r['final_all_checks'] for r in rr),
   'mean_input_tokens':statistics.mean(r['input_tokens'] for r in rr),'mean_completion_tokens':statistics.mean(r['completion_tokens'] for r in rr),
   'mean_cost_with_selection':statistics.mean(r['generation_cost_usd']+r['selector_cost_usd'] for r in rr),
   'median_seconds_with_selection':statistics.median(r['generation_seconds']+r['retrieval_ms']/1000+r['selector_seconds'] for r in rr)})
 b=c.Budget(OUT/'spend.sqlite',10,10);spend=b.summary();b.close()
 write(OUT/'summary.json',{'groups':summary,'spend':spend})
 (c.ROOT/'BENCHMARK_V2_OUTPUTS.md').write_text('\n'.join(texts),encoding='utf-8')
 print(json.dumps({'groups':summary,'spend':spend},indent=2))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('phase',choices=['prepare','generate','judge','report']);p.add_argument('--model',choices=['gpt-5.6-luna','gpt-5.6-terra']);a=p.parse_args()
 if a.phase=='generate':generate(a.model)
 else:globals()[a.phase]()
