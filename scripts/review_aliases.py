"""Keep opaque storage IDs out of model copying tasks."""
import copy

def encode(targets,context):
    rows=targets+context;ids=[r['candidate_id'] for r in rows]
    if len(ids)!=len(set(ids)):raise ValueError('Duplicate review identity')
    forward={uid:'c'+str(i+1) for i,uid in enumerate(ids)}
    def project(row):
        out=copy.deepcopy(row);out['candidate_id']=forward[row['candidate_id']];out['unit']['id']=out['candidate_id']
        for relation in out['unit']['relations']:relation['target']=forward.get(relation['target'],relation['target'])
        return out
    return [project(r) for r in targets],[project(r) for r in context],{a:b for b,a in forward.items()}

def decode(output,aliases):
    output=copy.deepcopy(output);errors=[]
    if isinstance(output,dict) and isinstance(output.get('reviews'),list):
        for row in output['reviews']:
            if not isinstance(row,dict):continue
            alias=row.get('candidate_id')
            if not isinstance(alias,str) or alias not in aliases:errors.append('unknown_review_alias')
            else:row['candidate_id']=aliases[alias]
    return output,errors
