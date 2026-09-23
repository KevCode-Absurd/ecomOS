"""Bounded reusable experiment calls. Fixed endpoints; no automatic retries."""
import hashlib
import json
import sys
import time
import subprocess
import os
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'.runtime'),str(ROOT),str(ROOT/'scripts')]
from intelligence.budget import Budget
from bounded_process import run_bounded

PROVIDERS={
    'deepseek':('deepseek-flash','https://api.deepseek.com/chat/completions','DEEPSEEK_API_KEY',.3,1.2),
    'openai':('gpt-5.6-terra','https://api.openai.com/v1/chat/completions','OPENAI_API_KEY',2.5,12),
}


def run_call(stage,provider,effort,system,user,limit=16384,stage_limit=5,cached_only=False):
    from check_providers import settings
    model,url,key,input_rate,output_rate=PROVIDERS[provider]
    messages=[{'role':'system','content':system},{'role':'user','content':json.dumps(user,ensure_ascii=False)}]
    payload={'model':model,'messages':messages,'response_format':{'type':'json_object'}}
    if provider=='deepseek':
        payload.update(max_tokens=limit,thinking={'type':'disabled' if effort=='none' else 'enabled'})
        if effort!='none': payload['reasoning_effort']=effort
    else: payload.update(max_completion_tokens=limit,reasoning_effort=effort,store=False)
    request_id=hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()
    directory=ROOT/'data'/stage
    directory.mkdir(parents=True,exist_ok=True)
    path=directory/(request_id+'.json')
    if path.exists(): return json.loads(path.read_text(encoding='utf-8'))
    if cached_only:raise ValueError('Cached result missing; dispatch disabled')
    config=settings()
    if not config.get(key): raise ValueError('Missing provider credentials')
    local=Budget(directory/'spend.sqlite',stage_limit,stage_limit)
    global_budget=Budget(ROOT/'data/spend.sqlite',160,200)
    attempt_path=None
    attempt=None
    try:
        bound=((len(json.dumps(messages,ensure_ascii=False).encode())+2048)*input_rate+limit*output_rate)/1_000_000
        local.reserve(request_id,provider,bound)
        global_budget.reserve(request_id,provider,bound)
        started=time.monotonic()
        attempt_dir=directory/'attempts';attempt_dir.mkdir(exist_ok=True)
        attempt_path=attempt_dir/(request_id+'.json')
        attempt={'request_id':request_id,'provider':provider,'model':model,'started_at':datetime.now(timezone.utc).isoformat(),'reserved_usd':bound,'status':'dispatched','deadline_seconds':300}
        attempt_path.write_text(json.dumps(attempt,indent=2),encoding='utf-8')
        # Kill the isolated HTTP process at a total wall-clock deadline. Socket read
        # timeouts alone can be extended indefinitely by provider keep-alive bytes.
        response=run_bounded([sys.executable,str(ROOT/'scripts/http_worker.py')],
            json.dumps({'provider':provider,'payload':payload}),timeout=300)
        if response.returncode!=0: raise ValueError('Transport failed; reservation retained')
        envelope=json.loads(response.stdout)
        if envelope.get('status')!=200: raise ValueError('Provider HTTP failure; reservation retained')
        body=envelope['body']; usage=body.get('usage',{})
        if not all(type(usage.get(k)) is int and usage[k]>=0 for k in ['prompt_tokens','completion_tokens']):
            raise ValueError('Uncertain billing; reservation retained')
        cost=(usage['prompt_tokens']*input_rate+usage['completion_tokens']*output_rate)/1_000_000
        global_budget.settle(request_id,cost); local.settle(request_id,cost)
        choice=body['choices'][0]; content=choice['message'].get('content','')
        try: output=json.loads(content)
        except (ValueError,TypeError): output=None
        result={'request_id':request_id,'provider':provider,'model':body.get('model',model),'effort':effort,
                'completion_limit':limit,'usage':usage,'booked_cost_usd':cost,
                'seconds':round(time.monotonic()-started,2),'finish_reason':choice.get('finish_reason'),
                'output':output,'raw_content':content,'input':user,'system_prompt_sha256':hashlib.sha256(system.encode()).hexdigest()}
        path.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
        attempt.update(status='completed',finished_at=datetime.now(timezone.utc).isoformat())
        attempt_path.write_text(json.dumps(attempt,indent=2),encoding='utf-8')
        return result
    except Exception as error:
        if attempt_path is not None:
            attempt.update(status='no_usable_result',error_type=type(error).__name__,finished_at=datetime.now(timezone.utc).isoformat())
            attempt_path.write_text(json.dumps(attempt,indent=2),encoding='utf-8')
        raise
    finally:
        local.close(); global_budget.close()
