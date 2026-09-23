"""Owner-value evaluation: complete input/card/output traces, nine ecommerce workflows."""
import argparse,json,time,random,hashlib,shutil
from concurrent.futures import ThreadPoolExecutor,as_completed
import benchmark_v2 as v2
import calibration_client as c
from benchmark_case import BRAND
from build_library import read,write
STAGE='ecommerce-owner-benchmark-v3'
OUT=c.ROOT/'data'/STAGE
MODELS=['gpt-5.6-luna','gpt-5.6-terra','gpt-5.6-sol']
METHODS=['none','raw','selected']
TASKS=v2.TASKS+[
 {'id':'E5','title':'Agency creative production brief','request':'Create three distinct static Meta ad briefs for Daypack: one iteration of desk-to-trail, one laptop-fit objection concept and one fresh positioning hypothesis. Give actual headline/body/CTA, image composition, production instructions and a single-variable test plan. Allocate no more than 8 designer hours total. No competitor performance or testimonial is verified. These are production drafts; inventory is constrained. Return actions.concepts as a list and actions.designer_hours. Write for a designer and media buyer to use today.', 'queries':['ecommerce static ad creative brief visual hierarchy hook benefit proof','Meta ecommerce creative iteration testing concept angle single variable']},
 {'id':'E6','title':'Paid-traffic landing page build brief','request':'Build a landing-page wireframe and final copy for a Meta ad promising clarity about the Daypack laptop sleeve. Give hero, benefits, fit guidance, objection blocks, shipping/returns, CTA destinations and mobile acceptance checks. Unknown: actual internal sleeve dimensions and whether a 15-inch laptop fits. Give clearly marked placeholders for missing facts rather than inventing them. Preserve ad-to-page message match, prioritize what can ship, and provide a developer handoff within 4 developer hours. Return actions.section_order and actions.developer_hours.', 'queries':['ecommerce landing page message match paid ads hero product proof CTA','ecommerce landing page mobile wireframe objections shipping size fit']},
 {'id':'E7','title':'Accessory bundle profitability and offer copy','request':'Owner asks: should we offer a Daypack plus Cable pouch bundle for $90? For this scenario only, combined landed COGS $33, pick-pack $2.50, merchant shipping $8.50, payment fee 3%, expected new-order CAC $30. Single Daypack economics remain as in brand facts. Calculate bundle pre_ad_contribution and after_ad_contribution, compare with full-price Daypack, and draft offer copy. No additional discount or launch approved. Address cannibalization and limited Daypack stock; do not use unmeasured LTV to rescue the offer. Return actions.bundle_pre_ad_contribution, actions.bundle_after_ad_contribution and actions.launch_status.', 'queries':['ecommerce bundle offer contribution margin cannibalization AOV profitability','ecommerce offer value proposition bundle perceived value without discount']},
 {'id':'E8','title':'Post-purchase retention flow','request':'Create a practical post-purchase email flow for first-time Daypack buyers with three actual emails: useful onboarding, review request and optional accessory cross-sell. Include event/timing, eligibility, suppression, returns/refunds, delivery uncertainty and a small holdout measurement. Bags are durable goods, not replenishable subscriptions. Do not request a review before confirmed delivery or imply known repeat-purchase lift. Return actions.emails with subject/body/timing and actions.primary_metric. Make it ready for an agency CRM specialist to configure after verifying event fields.', 'queries':['ecommerce post purchase onboarding review request delivery cross sell flow','ecommerce retention durable goods repeat purchase holdout email measurement']},
 {'id':'E9','title':'Weekly client update and agency task handoff','request':'Write a client-facing weekly update using the supplied 30-day comparisons, explicitly saying these are 30-day data rather than inventing a weekly trend. Explain the conversion and Meta/Shopify discrepancy plainly. Give three priorities only, decisions needed from the owner, and an internal task board with owners, dependencies, acceptance checks and hours. Weekly limits: designer 8, developer 4, owner 4. Include an inventory-aware go/no-go rule. Do not claim a completed audit or promise revenue uplift. Return actions.priorities, actions.designer_hours, actions.developer_hours and actions.owner_hours.', 'queries':['ecommerce agency reporting actionable client priorities attribution profitability','ecommerce operating cadence team task prioritization inventory conversion']}
]
SYSTEM='''You are an ecommerce operator preparing a useful deliverable for a business owner or agency. The brand is fictional. Be clear, specific, crisp and directly useful; supply actual requested copy/configuration, not an essay about how to do it. Aim for 450-750 words, shorter if complete. Brand facts and task evidence govern. Cards, if supplied, are conditional expert guidance, not proof of results or current platform behavior. Apply only relevant advice. Never invent product facts, approval, measurements or customer quotes. Return JSON {"answer_markdown":"complete deliverable", "actions":{requested structured fields},"questions":[up to 3 material questions],"applied_card_ids":[IDs actually used],"rejected_guidance":[reasons if relevant]}. Numeric action fields must be numbers. Any launch_status must be draft or blocked. No live actions are possible. Do not mention model or test condition. All conditions receive the same instructions.'''

def config(model):
 rates={'gpt-5.6-luna':(.25,1.2),'gpt-5.6-terra':(2.5,12),'gpt-5.6-sol':(5,20)}
 c.PROVIDERS['openai']=(model,'https://api.openai.com/v1/chat/completions','OPENAI_API_KEY',*rates[model])

def call(system,payload,limit=12288):
 # $23 new stage + previous V2 holds/selection + embeddings remain below $25.
 return c.run_call(STAGE,'openai','medium',system,payload,limit=limit,stage_limit=23)

def prepare():
 OUT.mkdir(parents=True,exist_ok=True)
 manifest={'brand':BRAND,'tasks':TASKS,'models':MODELS,'methods':METHODS,'system':SYSTEM,'reasoning':'medium','max_completion_tokens':12288,
  'new_stage_budget':23,'overall_current_evaluation_cap':25,'protocol':'9 tasks x 3 models x 3 methods =81 drafts. First 4 tasks get one identical sandbox validation/revision opportunity =36 revisions. Owner and agency reviews on final drafts; first and final both retained. No live execution. No Astra or DeepSeek calls. One sample per cell. Raw and selected packets fixed across models. Selector notes never sent to generation. No claim of actual owner satisfaction, revenue, freshness, or exhaustive recall.'}
 if (OUT/'manifest.json').exists() and read(OUT/'manifest.json')!=manifest:raise ValueError('Frozen experiment mismatch')
 write(OUT/'manifest.json',manifest)
 # Preserve paid packets from interrupted predecessor without modifying them.
 for t in TASKS[:4]:
  dst=OUT/'packets'/f"{t['id']}.json";dst.parent.mkdir(exist_ok=True)
  if not dst.exists():shutil.copy2(v2.OUT/'packets'/dst.name,dst)
 from search_knowledge import engine
 e=engine()
 write(OUT/'library-fingerprint.json',{'cards_sha256':hashlib.sha256((e.directory/'cards.json').read_bytes()).hexdigest(),'cards':len(e.cards)})
 for t in TASKS[4:]:
  p=OUT/'packets'/f"{t['id']}.json"
  if p.exists():continue
  start=time.perf_counter();ids=[];results=[]
  for q in t['queries']:
   r=e.search(q,token_budget=5000,max_cards=12);results.append(r);ids.extend(k for k in r['card_ids'] if k not in ids)
  raw='\n\n'.join(e.get_card(k)['guidance'] for k in ids);search_ms=(time.perf_counter()-start)*1000
  config('gpt-5.6-luna')
  r=call('Select up to eight distinct, applicable cards for the brand and task. Return JSON {"selected_card_ids":[],"excluded":[{"id":"...","reason":"..."}],"applicability_notes":[]}. Exclude contradicted prerequisites, irrelevant platforms/business models and redundant advice. Preserve conditional guidance. Do not solve the task, rewrite cards or add tactics.',{'brand':BRAND,'task':t['request'],'candidate_cards':raw},4096)
  if r['finish_reason']!='stop' or not isinstance(r['output'],dict):raise ValueError('Bad selector')
  chosen=r['output'].get('selected_card_ids',[])
  if len(chosen)>8 or len(set(chosen))!=len(chosen) or any(k not in ids for k in chosen):raise ValueError('Bad selection IDs')
  selected='\n\n'.join(e.get_card(k)['guidance'] for k in chosen)
  write(p,{'raw':raw,'selected':selected,'raw_ids':ids,'selected_ids':chosen,'selection':r,'search_ms':search_ms,'raw_tokens':len(e.encoding.encode(raw)),'selected_tokens':len(e.encoding.encode(selected)),'searches':results})
  print({'prepared':t['id'],'raw_cards':len(ids),'selected_cards':len(chosen)},flush=True)
 # Exact original cards and inferred metadata for trace/freshness display.
 cards={k:{'card':e.cards[k],'metadata':e.metadata[k]} for p in (OUT/'packets').glob('*.json') for k in read(p)['raw_ids']}
 write(OUT/'card-catalog.json',cards)

def generate_one(t,method,round_id):
 model=c.PROVIDERS['openai'][0];p=OUT/'runs'/f"{t['id']}-{model}-{method}.json"
 if p.exists():return
 packet=read(OUT/'packets'/f"{t['id']}.json")
 payload={'experiment':'owner-v3','brand':BRAND,'task':{k:v for k,v in t.items() if k!='queries'},'reference_guidance':packet[method] if method!='none' else ''}
 if round_id:payload['transport_recovery_attempt']=round_id
 first=call(SYSTEM,payload)
 if first['finish_reason']!='stop' or not isinstance(first['output'],dict):
  write(OUT/'invalid'/p.name,first);raise ValueError('Invalid completion')
 check=v2.validate(t['id'],first['output']) if t['id'] in ['E1','E2','E3','E4'] else None
 final=first
 if check:
  final=call(SYSTEM,{**payload,'previous_draft':first['output'],'sandbox_feedback':check,'instruction':'Return the complete revised deliverable. Check prose as well as action fields; passing numeric checks does not establish practical correctness.'})
  if final['finish_reason']!='stop' or not isinstance(final['output'],dict):write(OUT/'invalid'/p.name,final);raise ValueError('Invalid revision')
 write(p,{'task':t['id'],'model':model,'method':method,'first':first,'final':final,'first_validation':check,
  'final_validation':v2.validate(t['id'],final['output']) if check else None,'knowledge_tokens':packet.get(method+'_tokens',0),
  'card_ids':packet[method+'_ids'] if method!='none' else [],'retrieval_ms':packet['search_ms'] if method!='none' else 0,
  'selector_seconds':packet['selection']['seconds'] if method=='selected' else 0,'selector_cost':packet['selection']['booked_cost_usd'] if method=='selected' else 0})
 print({'finished':p.stem,'checks':check['all_pass'] if check else 'editorial'},flush=True)

def generate(model,round_id=0,task_id=None):
 config(model);jobs=[(t,m,round_id) for t in TASKS if task_id is None or t['id']==task_id for m in METHODS];random.Random(63).shuffle(jobs)
 failures=[]
 with ThreadPoolExecutor(max_workers=3) as ex:
  fs={ex.submit(generate_one,*j):[j[0]['id'],j[1]] for j in jobs}
  for f in as_completed(fs):
   try:f.result()
   except Exception as err:failures.append({'job':fs[f],'error':str(err)});print({'failed':fs[f],'error':str(err)},flush=True)
 write(OUT/f'status-{model}-{round_id}.json',{'failures':failures})

RUBRIC={'usefulness':30,'brand_fit':20,'correctness':20,'clarity':15,'handoff_readiness':15}
def review_one(t,lens):
 p=OUT/'reviews'/f"{t['id']}-{lens}.json"
 if p.exists():return
 runs=[read(x) for x in sorted((OUT/'runs').glob(t['id']+'-*.json'))]
 if len(runs)!=9:raise ValueError('Need all nine candidates')
 if t['id'] in ['E1','E3'] and any(r.get('validation_protocol')!='semantic-v2' for r in runs):raise ValueError('Wait for corrected validation')
 random.Random(t['id']+lens).shuffle(runs)
 mapping={chr(65+i):{'model':r['model'],'method':r['method']} for i,r in enumerate(runs)}
 answers={chr(65+i):{k:v for k,v in r['final']['output'].items() if k not in ['applied_card_ids','rejected_guidance']} for i,r in enumerate(runs)}
 system='''You are simulating the perspective of a paying ecommerce BUSINESS OWNER or AGENCY OWNER, as specified. You are not an actual customer. Review anonymized drafts as work you would need to use today. Judge clear decisions, usable copy/configuration, brand fit, accuracy, realistic resources, and remaining editing burden. Do not reward jargon, academic completeness, verbosity, citations, or cards for their own sake. Short, complete answers can be excellent. Penalize invented facts, unsupported promises, unsafe launch recommendations, vague advice, contradictory fields/prose, missing requested artifacts and busywork. The source packet is optional reference material, not truth. Source-specific heuristics need appropriate conditions. Scores 0-4: 0 unusable,1 major rewrite,2 useful pieces but substantial editing,3 usable with small edits,4 ready as a draft with routine review. Return JSON {"reviews":[{"label":"A","scores":{"usefulness":0,"brand_fit":0,"correctness":0,"clarity":0,"handoff_readiness":0},"owner_verdict":"use|edit|reject","editing_burden":"none|minor|substantial|rewrite","specific_value":[],"critical_errors":[],"remaining_work":[],"evidence":"concrete supporting detail"}],"ranking":[],"summary":"..."}. Review all nine labels exactly once. Do not claim real satisfaction, revenue gain or willingness to pay. For E4, a union larger than store revenue is unresolved reconciliation, not real incremental sales. For E3, a negative test-feasibility conclusion can be good; a 14-day diagnostic cannot claim the supplied sample was reached.'''
 r=call(system,{'lens':lens,'brand':BRAND,'task':t,'rubric_weights':RUBRIC,'answers':answers,'optional_sources':read(OUT/'packets'/f"{t['id']}.json")['raw']},12288)
 out=r['output'];valid=r['finish_reason']=='stop' and isinstance(out,dict) and len(out.get('reviews',[]))==9 and {x.get('label') for x in out['reviews']}==set(mapping)
 if valid:valid=all(set(x.get('scores',{}))==set(RUBRIC) and all(type(v) in (int,float) and 0<=v<=4 for v in x['scores'].values()) for x in out['reviews'])
 write(p,{'valid':valid,'mapping':mapping,'lens':lens,'result':r});print({'reviewed':t['id'],'lens':lens,'valid':valid},flush=True)

def review(lens,ready=False):
 config('gpt-5.6-sol' if lens=='business-owner' else 'gpt-5.6-terra')
 tasks=TASKS
 if ready:
  tasks=[]
  for t in TASKS:
   rs=[read(p) for p in (OUT/'runs').glob(t['id']+'-*.json')]
   if len(rs)==9 and (t['id'] not in ['E1','E3'] or all(r.get('validation_protocol')=='semantic-v2' for r in rs)):tasks.append(t)
 with ThreadPoolExecutor(max_workers=2) as ex:
  fs=[ex.submit(review_one,t,lens) for t in tasks]
  for f in as_completed(fs):f.result()

def audit():
 from search_knowledge import engine
 e=engine();config('gpt-5.6-terra')
 for t in TASKS:
  p=OUT/'retrieval-audits'/f"{t['id']}.json"
  if p.exists():continue
  packet=read(OUT/'packets'/f"{t['id']}.json");ids=[];start=time.perf_counter()
  for q in t['queries']:
   r=e.search(q,semantic=False,token_budget=5000,max_cards=12);ids.extend(k for k in r['card_ids'] if k not in ids)
  keyword_ms=(time.perf_counter()-start)*1000
  start=time.perf_counter()
  for q in t['queries']:e.search(q,token_budget=5000,max_cards=12)
  cache_ms=(time.perf_counter()-start)*1000
  # Audit evidence uses union so reviewer can compare selection and ranking misses.
  union=list(dict.fromkeys(packet['raw_ids']+ids))
  r=call('Audit retrieval from a practical ecommerce operator perspective. Return JSON {"cards":[{"id":"...","relevance":"direct|conditional|irrelevant","reason":"..."}],"coverage":[{"need":"task capability","raw_covered":true,"selected_covered":true,"keyword_covered":true,"supporting_ids":[]}],"missing_capabilities":[],"freshness_checks":[],"summary":"..."}. Review every supplied card exactly once. A keyword match is not enough: inspect applicability, brand, caveats and exact guidance. Missing facts from brand data are not a retrieval failure. Do not assert exhaustive recall: you see only the candidate union, not all 7611 cards. Do not label advice verified-current absent evidence. Separate source guidance from actual model output.',{'brand':BRAND,'task':t,'raw_ids':packet['raw_ids'],'selected_ids':packet['selected_ids'],'keyword_ids':ids,'cards':[{'id':k,'text':e.get_card(k)['guidance'],'metadata':e.metadata[k]} for k in union]},10000)
  write(p,{'keyword_ids':ids,'keyword_ms':keyword_ms,'cached_hybrid_ms':cache_ms,'union_ids':union,'result':r})
  print({'audited':t['id']},flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('phase',choices=['prepare','generate','review','audit']);p.add_argument('--model',choices=MODELS);p.add_argument('--lens',choices=['business-owner','agency-owner']);p.add_argument('--round',type=int,default=0);p.add_argument('--task');p.add_argument('--ready',action='store_true');a=p.parse_args()
 if a.phase=='prepare':prepare()
 elif a.phase=='generate':generate(a.model,a.round,a.task)
 elif a.phase=='audit':audit()
 else:review(a.lens,a.ready)
