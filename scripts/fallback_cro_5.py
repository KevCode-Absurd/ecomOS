"""Separate fallback for a confirmed truncated CRO result; never an unknown call."""
import json,hashlib
from calibration_client import ROOT,run_call
from ingest_cro import assemble,validate
p=ROOT/'data/cro-folder-proposal.json'
auth=json.loads((ROOT/'data/cro-folder-authorization.json').read_text())
assert hashlib.sha256(p.read_bytes()).hexdigest()==auth['manifest_sha256'] and auth['combined_cap_usd']==10
dest=ROOT/'data/cro-folder-v1'
old=json.loads((dest/'batch-005-round-0.json').read_text())
assert old['finish_reason']=='length'
manifest=json.loads(p.read_text(encoding='utf-8'));source,spans=assemble(manifest['batches'][5])
result=run_call('cro-folder-v1','openai','high',(ROOT/'prompts/extract-cro-v1.md').read_text(encoding='utf-8'),{'source':source,'instruction':'Extract task-sized units from this excerpt.'},limit=16384,stage_limit=10)
checked=validate(result,source,spans)
row={'batch':5,'round':1,'kind':'confirmed_truncation_fallback','request_id':result['request_id'],'finish_reason':result['finish_reason'],**checked}
(dest/'batch-005-round-1.json').write_text(json.dumps(row,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'batch':5,'fallback':'openai','candidates':len(checked['candidates']),'held':len(checked['held']),'errors':checked['errors'],'cost':result['booked_cost_usd']}))
