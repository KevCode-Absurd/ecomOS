import argparse,hashlib,json,sys,time,random
from concurrent.futures import ThreadPoolExecutor,as_completed
import calibration_client as c
from bounded_process import run_bounded
from build_library import read,write
from peach_web_case import OUT,TASKS,SYSTEM,brand
MODELS=['gpt-5.6-luna','gpt-5.6-terra','gpt-5.6-sol']
RATES={'gpt-5.6-luna':(.25,1.2),'gpt-5.6-terra':(2.5,12),'gpt-5.6-sol':(5,20)}
KNOWLEDGE={'type':'function','name':'knowledge_search','description':'Search expert ecommerce guidance by task/subtask. Generates compact cards preserving applicability and caveats. Use separate focused queries for distinct needs; this is reference advice, not verified current brand evidence.','parameters':{'type':'object','properties':{'query':{'type':'string'},'purpose':{'type':'string'}},'required':['query','purpose'],'additionalProperties':False},'strict':True}

def response(payload):
 if (OUT/'HALT').exists():raise ValueError('Dispatch paused for integration check')
 rid=hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest();p=OUT/'responses'/f'{rid}.json'
 if p.exists():return read(p)
 local=c.Budget(OUT/'spend.sqlite',23,23);global_b=c.Budget(c.ROOT/'data/spend.sqlite',160,200)
 ir,orr=RATES[payload['model']];webcap=payload.get('max_tool_calls',0)
 # Conservatively reserve large default search-context allowance per built-in call.
 # Provider requests cannot be interrupted at a monetary amount; a bound overrun halts dispatch.
 bound=((len(json.dumps(payload).encode())+2048+128000*webcap)*ir*2+payload['max_output_tokens']*orr*1.5)/1e6+.01*webcap
 local.reserve(rid,'openai-responses',bound);global_b.reserve(rid,'openai-responses',bound)
 write(OUT/'attempts'/f'{rid}.json',{'model':payload['model'],'bound':bound,'status':'dispatched'})
 start=time.perf_counter()
 try:
  r=run_bounded([sys.executable,str(c.ROOT/'scripts/http_worker.py')],json.dumps({'provider':'openai-responses','payload':payload}),timeout=300)
  if r.returncode:raise ValueError('Transport error')
  env=json.loads(r.stdout)
  if env.get('status')!=200:
   write(OUT/'http-errors'/f'{rid}.json',env)
   raise ValueError('HTTP '+str(env.get('status'))+' param='+str(env.get('error_param'))+' code='+str(env.get('error_code')))
  body=env['body'];u=body.get('usage',{})
  if not all(type(u.get(k)) is int for k in ['input_tokens','output_tokens']):raise ValueError('Missing usage')
  nweb=sum(x.get('type')=='web_search_call' for x in body.get('output',[]));long=u['input_tokens']>272000
  cost=(u['input_tokens']*ir*(2 if long else 1)+u['output_tokens']*orr*(1.5 if long else 1))/1e6+.01*nweb
  global_b.settle(rid,cost);local.settle(rid,cost)
  out={'request_id':rid,'payload':payload,'body':body,'seconds':time.perf_counter()-start,'cost_upper_estimate_usd':cost,'web_calls':nweb,'web_tool_cost_usd':nweb*.01}
  write(p,out);write(OUT/'attempts'/f'{rid}.json',{'model':payload['model'],'bound':bound,'status':'complete','cost':cost})
  return out
 except Exception as e:
  write(OUT/'attempts'/f'{rid}.json',{'model':payload['model'],'bound':bound,'status':'uncertain_or_failed','error':str(e)});raise
 finally:local.close();global_b.close()

def prepare():
 b=brand();write(OUT/'brand.json',b)
 manifest={'brand':b,'tasks':TASKS,'system':SYSTEM,'models':MODELS,'arms':['web','web_cards'],'reasoning':'medium','max_response_output_tokens':12000,
 'max_model_turns':5,'max_built_in_tools_per_response':2,'max_knowledge_calls_per_workflow':8,'knowledge_budget_per_call':4000,
 'api_stage_cap_usd':23,'total_round_limit_usd':25,'notes':['One sample per cell; exploratory.','Web search available equally. Different chosen sources are part of workflow, not controlled identical evidence.','Model-authored queries and local tool loop; no live platform writes.','Owner reviews are simulated.','Conservative monetary reservations include tools; embeddings separately reserved globally.','Web token billing assumed represented in API usage; invoice reconciliation required.']}
 p=OUT/'manifest.json'
 if p.exists() and read(p)!=json.loads(json.dumps(manifest)):raise ValueError('Frozen manifest mismatch')
 write(p,manifest)

def run_one(model,task,arm):
 tid,request=task;p=OUT/'runs'/f'{tid}-{model}-{arm}.json'
 if p.exists():return
 history=[{'role':'user','content':json.dumps({'brand':read(OUT/'brand.json'),'owner_request':request},ensure_ascii=False)}]
 calls=[];retrieval=[];nknowledge=0;started=time.perf_counter()
 for step in range(5):
  tools=[{'type':'web_search','search_context_size':'medium'}]
  if arm=='web_cards' and nknowledge<8 and step<4:tools.append(KNOWLEDGE)
  payload={'model':model,'instructions':SYSTEM,'input':history,'tools':tools,'reasoning':{'effort':'medium'},'store':False,
   'include':['web_search_call.action.sources','reasoning.encrypted_content'],'max_output_tokens':12000,'max_tool_calls':2,'parallel_tool_calls':True}
  result=response(payload);calls.append(result);items=result['body'].get('output',[])
  functions=[x for x in items if x.get('type')=='function_call']
  if functions:
   history.extend(items)
   for f in functions:
    args=json.loads(f['arguments'])
    if f['name']!='knowledge_search' or nknowledge>=8:toolout={'error':'Unknown tool or knowledge-call allowance reached'}
    else:
     from search_knowledge import engine
     e=engine();ret=e.search(args['query'],token_budget=4000,max_cards=10);nknowledge+=1
     # Full audit saved; compact tool output goes to model.
     retrieval.append({'step':step,'query':args['query'],'purpose':args['purpose'],'result':ret,'cards':[e.cards[k] for k in ret['card_ids']]})
     toolout={k:ret[k] for k in ['context','card_ids','knowledge_tokens','needs_current_check','warnings','instruction']}
    history.append({'type':'function_call_output','call_id':f['call_id'],'output':json.dumps(toolout,ensure_ascii=False)})
   continue
  texts=[z['text'] for x in items if x.get('type')=='message' for z in x.get('content',[]) if z.get('type')=='output_text']
  text='\n'.join(texts)
  try:output=json.loads(text)
  except ValueError:output={'answer_markdown':text,'format_note':'Not JSON; raw text preserved.'}
  status='complete' if result['body'].get('status')=='completed' and text.strip() else 'incomplete'
  write(p,{'task_id':tid,'model':model,'arm':arm,'status':status,'output':output,'calls':calls,'retrieval':retrieval,'elapsed_seconds':time.perf_counter()-started})
  print({'run':p.stem,'status':status,'web_calls':sum(x['web_calls'] for x in calls),'knowledge_calls':nknowledge,'cost':sum(x['cost_upper_estimate_usd'] for x in calls)},flush=True);return
 write(p,{'task_id':tid,'model':model,'arm':arm,'status':'tool_loop_limit','calls':calls,'retrieval':retrieval,'output':{},'elapsed_seconds':time.perf_counter()-started})

def generate(model,tid):
 jobs=[(model,t,a) for t in TASKS if not tid or tid==t[0] for a in ['web','web_cards']];random.Random(model).shuffle(jobs)
 failures=[]
 with ThreadPoolExecutor(max_workers=2) as ex:
  fs={ex.submit(run_one,*j):[j[1][0],j[2]] for j in jobs}
  for f in as_completed(fs):
   try:f.result()
   except Exception as e:failures.append({'job':fs[f],'error':str(e)});print({'failed':fs[f],'error':str(e)},flush=True)
 write(OUT/f'status-{model}-{tid or "all"}.json',{'failures':failures})

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('phase',choices=['prepare','generate']);p.add_argument('--model',choices=MODELS);p.add_argument('--task');a=p.parse_args()
 if a.phase=='prepare':prepare()
 else:generate(a.model,a.task)
