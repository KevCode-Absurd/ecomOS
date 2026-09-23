"""Explicit cross-provider fallback; retain original unknown reservations."""
import argparse,hashlib,json,sqlite3
from concurrent.futures import ThreadPoolExecutor
from calibration_client import ROOT,run_call
from ingest_cro import assemble,validate
parser=argparse.ArgumentParser();parser.add_argument('--execute',action='store_true');args=parser.parse_args()
p=ROOT/'data/cro-folder-proposal.json';auth=json.loads((ROOT/'data/cro-folder-authorization.json').read_text())
assert hashlib.sha256(p.read_bytes()).hexdigest()==auth['manifest_sha256'] and auth['combined_cap_usd']==10
manifest=json.loads(p.read_text(encoding='utf-8'));dest=ROOT/'data/cro-folder-v1';prompt=(ROOT/'prompts/extract-cro-v1.md').read_text(encoding='utf-8')
def job(i):
    source,spans=assemble(manifest['batches'][i])
    original_user={'source':source,'already_extracted_claims':[],'instruction':'Extract remaining distinct task-sized units. Do not repeat already extracted claims.'}
    payload={'model':'deepseek-flash','messages':[{'role':'system','content':prompt},{'role':'user','content':json.dumps(original_user,ensure_ascii=False)}],'response_format':{'type':'json_object'},'max_tokens':32768,'thinking':{'type':'enabled'},'reasoning_effort':'high'}
    original_id=hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()
    db=sqlite3.connect(dest/'spend.sqlite');record=db.execute('SELECT actual FROM spend WHERE request_id=?',(original_id,)).fetchone();db.close()
    if record!=(None,):raise ValueError('Expected existing uncertain original reservation')
    if not args.execute:return {'batch':i,'original_reservation_confirmed':True}
    result=run_call('cro-folder-v1','openai','high',prompt,{'source':source,'instruction':'Extract task-sized units from this excerpt. This is a separate cross-provider fallback.'},limit=16384,stage_limit=10)
    checked=validate(result,source,spans)
    row={'batch':i,'round':0,'kind':'separate_cross_provider_fallback','original_unknown_request_id':original_id,'request_id':result['request_id'],'finish_reason':result['finish_reason'],**checked}
    (dest/f'batch-{i:03d}-round-0.json').write_text(json.dumps(row,ensure_ascii=False,indent=2),encoding='utf-8')
    return {'batch':i,'candidates':len(checked['candidates']),'held':len(checked['held']),'errors':checked['errors'],'cost':result['booked_cost_usd']}
with ThreadPoolExecutor(max_workers=2) as pool:
    for result in pool.map(job,[2,3]):print(json.dumps(result),flush=True)
