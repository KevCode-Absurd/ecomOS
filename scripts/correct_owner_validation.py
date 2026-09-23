"""Apply identical corrected feedback to E1/E3, retaining original revisions and costs."""
from concurrent.futures import ThreadPoolExecutor,as_completed
from benchmark_v3 import OUT,TASKS,MODELS,config,call,SYSTEM
from build_library import read,write
from owner_validation import validate
import argparse

def one(p):
 r=read(p)
 if r.get('validation_protocol')=='semantic-v2':return
 original=r['final'];first=r['first'];check=validate(r['task'],first['output'])
 final=call(SYSTEM,{**first['input'],'previous_draft':first['output'],'sandbox_feedback':check,
 'validation_protocol':'semantic-v2','instruction':'Return the complete revised deliverable. Check prose and schedule as well as fields. Equivalent field names and explicit negative values have been normalized in checks, not altered in your original draft. Passing these limited checks is not proof of full correctness.'})
 if final['finish_reason']!='stop' or not isinstance(final['output'],dict):raise ValueError('Invalid correction')
 r.update(superseded_final=original,superseded_first_validation=r['first_validation'],superseded_final_validation=r['final_validation'],
  final=final,first_validation=check,final_validation=validate(r['task'],final['output']),validation_protocol='semantic-v2')
 write(p,r);print({'corrected':p.stem},flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--model',choices=MODELS,required=True);a=p.parse_args();config(a.model)
 paths=[p for p in (OUT/'runs').glob('*-'+a.model+'-*.json') if p.name.startswith(('E1-','E3-'))]
 assert len(paths)==6
 with ThreadPoolExecutor(max_workers=3) as ex:
  fs=[ex.submit(one,p) for p in paths]
  for f in as_completed(fs):f.result()
