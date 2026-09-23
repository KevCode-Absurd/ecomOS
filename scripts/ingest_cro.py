"""CRO-only approved folder ingestion; resumable requests and evidence checkpoints."""
import argparse, hashlib, json, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from calibration_client import ROOT, run_call
from calibrate_v2 import FORMAT
from intelligence.units import validate_output

STAGE='cro-folder-v1'

def assemble(batch):
    text=''; spans=[]
    for seg in batch['segments']:
        if text: text+='\n\n'
        start=len(text); text+=seg['text']
        spans.append((start,len(text),seg))
    return {'source_id':batch['source_id'],'source_sha256':batch['segments'][0]['source_sha256'],
            'locator':'batch','start':0,'text':text},spans

def validate(result,source,spans,max_units=16):
    checked=validate_output(result['output'],source,max_units=max_units)
    good=[]
    for candidate in checked['candidates']:
        mapped=[];valid=True
        for evidence in candidate['evidence']:
            pieces=[]
            for a,b,seg in spans:
                left=max(a,evidence['start']);right=min(b,evidence['end'])
                if left>=right:continue
                quote=source['text'][left:right]
                if not quote.strip():continue
                start=seg['start']+left-a
                if seg['text'][left-a:right-a]!=quote:
                    valid=False;break
                pieces.append({**evidence,'locator':seg['locator'],'start':start,
                               'end':start+len(quote),'quote':quote})
            if not pieces:valid=False
            mapped.extend(pieces)
        if valid:
            candidate['evidence']=mapped
            good.append(candidate)
        else:checked['held'].append({'unit_id':candidate['unit']['id'],'reason':'unmappable_source_quote'})
    checked['candidates']=good
    checked['publication_allowed']=False
    return checked

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--execute',action='store_true')
    parser.add_argument('--start-batch',type=int,default=0)
    parser.add_argument('--end-batch',type=int,default=52)
    parser.add_argument('--completion-limit',type=int,choices=[32768,65536],default=32768)
    parser.add_argument('--workers',type=int,choices=range(1,7),default=2)
    parser.add_argument('--max-rounds',type=int,choices=[1,2,3],default=3)
    args=parser.parse_args()
    if not 0<=args.start_batch<args.end_batch<=52:parser.error('Invalid batch range')
    path=ROOT/'data/cro-folder-proposal.json'
    auth=json.loads((ROOT/'data/cro-folder-authorization.json').read_text())
    if hashlib.sha256(path.read_bytes()).hexdigest()!=auth['manifest_sha256']:raise ValueError('Manifest changed')
    if auth['combined_cap_usd']!=10:raise ValueError('Unexpected authorization')
    manifest=json.loads(path.read_text(encoding='utf-8'))
    # Verify all excerpt offsets against local immutable parsed snapshots before dispatch.
    for batch in manifest['batches']:
        for seg in batch['segments']:
            p=ROOT/'data/snapshots'/seg['source_id']/(seg['source_sha256']+'.parsed.json')
            blocks=json.loads(p.read_text(encoding='utf-8'))['blocks']
            block=next(b for b in blocks if b['locator']==seg['locator'])
            if block['text'][seg['start']:seg['end']]!=seg['text']:raise ValueError('Snapshot mismatch')
    if not args.execute:print(json.dumps({'verified_batches':len(manifest['batches']),'cap':10}));return
    prompt=(ROOT/'prompts/extract-cro-v1.md').read_text(encoding='utf-8')
    dest=ROOT/'data'/STAGE;dest.mkdir(exist_ok=True)
    def job(index):
        source,spans=assemble(manifest['batches'][index]);previous=[]; rounds=[]
        for round_index in range(args.max_rounds):
            user={'source':source,'already_extracted_claims':previous,
                  'instruction':'Extract remaining distinct task-sized units. Do not repeat already extracted claims.'}
            result=run_call(STAGE,'deepseek','high',prompt,user,limit=args.completion_limit,stage_limit=10)
            checked=validate(result,source,spans)
            row={'batch':index,'round':round_index,'request_id':result['request_id'],
                 'finish_reason':result['finish_reason'],**checked}
            (dest/f'batch-{index:03d}-round-{round_index}.json').write_text(json.dumps(row,ensure_ascii=False,indent=2),encoding='utf-8')
            rounds.append(row)
            print(json.dumps({'batch':index,'round':round_index,'candidates':len(checked['candidates']),
                 'held':len(checked['held']),'errors':checked['errors'],'more':checked.get('more_units'),
                 'cost':result['booked_cost_usd']}),flush=True)
            if result['finish_reason']!='stop' or checked['errors'] or checked['held']:break
            if not checked.get('more_units'):break
            claims=[c['unit']['claim']['text'] for c in checked['candidates']]
            if not claims:break
            previous.extend(claims)
        return rounds
    # Bounded active group; any failure prevents scheduling the next group. Cached calls cost nothing.
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for start in range(args.start_batch,args.end_batch,args.workers):
            list(pool.map(job,range(start,min(start+args.workers,args.end_batch))))

if __name__=='__main__':
    try:main()
    except Exception as e:
        print(json.dumps({'stopped':True,'error_type':type(e).__name__,'note':'No automatic retry; inspect ledger.'}),flush=True)
        sys.exit(1)
