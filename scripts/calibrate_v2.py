"""Same approved excerpts; field-evidenced units and matched effort controls."""
import argparse
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor,as_completed
from calibration_client import ROOT,run_call
from intelligence.units import validate_output

FORMAT='''Return only JSON with exactly units (array, at most 16), more_units (boolean), unresolved (array of strings). Each unit has exactly: id (unique string), kind (action/principle/example/warning/unresolved_claim), title (string), claim (evidenced statement), action (evidenced statement only for action kind, otherwise null), trigger, prerequisites, exclusions (each an ALL/ANY group), completion (array of evidenced statements), unknowns (array of strings), relations (array of {kind: depends_on/alternative_to/conflicts_with, target: local unit id}). An evidenced statement is {"text":"attributed paraphrase","quote":"exact unique substring of source text"}. An ALL/ANY group is {"op":"all" or "any","args":[evidenced statements or nested groups]}; use empty args when unstated, not invented conditions. Example for input "Test one variable at a time.": {"units":[{"id":"u1","kind":"action","title":"Isolate the test variable","claim":{"text":"The source recommends changing one variable.","quote":"Test one variable at a time."},"action":{"text":"Test one variable at a time.","quote":"Test one variable at a time."},"trigger":{"op":"all","args":[]},"prerequisites":{"op":"all","args":[]},"exclusions":{"op":"any","args":[]},"completion":[],"unknowns":["No measurement method stated."],"relations":[]}],"more_units":false,"unresolved":[]}. Copy quote content WITHOUT adding literal quotation characters around it. Each unit has one atomic action at most. Do not invent conditions or execution steps. Source's examples, opinions and incomplete procedures retain that status. Extract all material distinct units up to the cap; explicitly flag omitted units. A task's unresolved problem is not an exclusion for the repair task.'''


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--execute',action='store_true')
    parser.add_argument('--all',action='store_true',help='DeepSeek high on all 24; otherwise 3 annotated cases with matched controls')
    parser.add_argument('--high-cap',action='store_true',help='Completed-outcome follow-up: DeepSeek high on 3 cases with 32768 completion tokens')
    parser.add_argument('--fallback-case',type=int,choices=range(24),help='Separate Terra-high fallback experiment on an approved case; never retries an uncertain DeepSeek request')
    args=parser.parse_args()
    source_path=ROOT/'data/body-evaluation-proposal.json'
    auth=json.loads((ROOT/'data/calibration-body-high/authorization.json').read_text(encoding='utf-8'))
    if hashlib.sha256(source_path.read_bytes()).hexdigest()!=auth['manifest_sha256']:
        raise ValueError('Approved source manifest changed')
    passages=json.loads(source_path.read_text(encoding='utf-8'))['passages']
    jobs=[(i,'deepseek','high') for i in range(24)] if args.all else [
        (i,p,e) for i in [2,8,19] for p,e in [('deepseek','high'),('deepseek','none'),('openai','high')]]
    if args.high_cap and not args.all: jobs=[(i,'deepseek','high') for i in [2,8,19]]
    if args.fallback_case is not None:
        if args.all or args.high_cap: parser.error('Fallback is a separate experiment')
        jobs=[(args.fallback_case,'openai','high')]
    prompt=(ROOT/'prompts/extract-v2.md').read_text(encoding='utf-8')+'\n\n'+FORMAT
    if not args.execute:
        print(json.dumps({'requests':len(jobs),'stage_ceiling_usd':5,'private_excerpt_set':'previously approved 24','bulk_publication':False})); return
    dest=ROOT/'data/calibration-v2'; dest.mkdir(parents=True,exist_ok=True)
    def job(index,provider,effort):
        source=passages[index]
        evidence={k:source[k] for k in ['source_id','source_sha256','locator','start','text']}
        evidence['provenance']='unverified'
        limit=32768 if args.high_cap else 16384
        result=run_call('calibration-v2',provider,effort,prompt,evidence,limit=limit)
        checked=validate_output(result['output'],source)
        row={'case_index':index,'provider':provider,'effort':effort,'request_id':result['request_id'],
             'complete':result['finish_reason']=='stop','completion_limit':limit,'units':len(checked['candidates']),
             'held':len(checked['held']),'errors':checked['errors'],'more_units':checked.get('more_units'),
             'cost':result['booked_cost_usd']}
        (dest/(result['request_id']+'.validation.json')).write_text(json.dumps({'summary':row,**checked},ensure_ascii=False,indent=2),encoding='utf-8')
        print(json.dumps(row),flush=True)
        return row
    rows=[]
    # Independent read-only provider requests; each worker has separate SQLite connections.
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures=[pool.submit(job,*j) for j in jobs]
        for future in as_completed(futures): rows.append(future.result())
    name='summary-all-high-cap.json' if args.all and args.high_cap else 'summary-high-cap.json' if args.high_cap else 'summary-all.json' if args.all else 'summary-controls.json'
    if args.fallback_case is not None: name='summary-fallback-'+str(args.fallback_case)+'.json'
    (dest/name).write_text(json.dumps(rows,indent=2),encoding='utf-8')


if __name__=='__main__':
    try: main()
    except Exception as error:
        print(json.dumps({'stopped':True,'error_type':type(error).__name__,'note':'No automatic retry; inspect pending reservations.'}),flush=True)
        raise SystemExit(1)
