"""Rebind saved evidence locally, preserving previous validations in history."""
import argparse,hashlib,json
from calibration_client import ROOT
from ingest_cro import assemble,validate
parser=argparse.ArgumentParser();parser.add_argument('batches',nargs='+',type=int);args=parser.parse_args()
manifest=json.loads((ROOT/'data/cro-folder-proposal.json').read_text(encoding='utf-8'))
dest=ROOT/'data/cro-folder-v1';history=dest/'validation-history';history.mkdir(exist_ok=True)
for i in args.batches:
    source,spans=assemble(manifest['batches'][i])
    for path in sorted(dest.glob(f'batch-{i:03d}-round-*.json')):
        old=path.read_bytes();row=json.loads(old)
        raw=json.loads((dest/(row['request_id']+'.json')).read_text(encoding='utf-8'))
        checked=validate(raw,source,spans)
        new={**row,**checked,'validation_revision':'multi-span-v1'}
        (history/(path.stem+'-'+hashlib.sha256(old).hexdigest()+'.json')).write_bytes(old)
        path.write_text(json.dumps(new,ensure_ascii=False,indent=2),encoding='utf-8')
        print(json.dumps({'batch':i,'round':row['round'],'candidates':len(checked['candidates']),'held':len(checked['held']),'errors':checked['errors']}))
