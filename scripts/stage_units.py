"""Persist V2 candidates after checking evidence against local source snapshots.

No candidate becomes approved or executable here. Raw results remain immutable.
"""
import hashlib
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from intelligence.units import validate_output


def main():
    dest=ROOT/'data/calibration-v2'
    rows=json.loads((dest/'summary-staging.json').read_text(encoding='utf-8'))
    output_dir=ROOT/'data/units'; output_dir.mkdir(parents=True,exist_ok=True)
    records=[]; diagnostics=[]; sources={}
    for row in rows:
        raw=json.loads((dest/(row['request_id']+'.json')).read_text(encoding='utf-8'))
        source=raw['input']; key=(source['source_id'],source['source_sha256'])
        if key not in sources:
            path=ROOT/'data/snapshots'/key[0]/key[1]
            if hashlib.sha256(path.read_bytes()).hexdigest()!=key[1]: raise ValueError('Source snapshot hash mismatch')
            parsed=json.loads(path.with_name(path.name+'.parsed.json').read_text(encoding='utf-8'))
            sources[key]={b['locator']:b['text'] for b in parsed['blocks']}
        text=sources[key][source['locator']]
        if text[source['start']:source['start']+len(source['text'])]!=source['text']:
            raise ValueError('Excerpt does not match snapshot text')
        checked=validate_output(raw['output'],source)
        diagnostics.append({'case_index':row['case_index'],'request_id':row['request_id'],
                            'complete':row['complete'],'errors':checked['errors'],'held':checked['held'],
                            'candidates':len(checked['candidates']),'more_units':checked.get('more_units')})
        for candidate in checked['candidates']:
            for evidence in candidate['evidence']:
                if text[evidence['start']:evidence['end']]!=evidence['quote']:
                    raise ValueError('Bound evidence does not match immutable snapshot')
            record={**candidate,'extraction_request':row['request_id'],'case_index':row['case_index'],
                    'status':'held' if checked['errors'] or not row['complete'] else 'candidate',
                    'publication_allowed':False,'schema_version':2}
            path=output_dir/(candidate['id']+'.json')
            encoded=json.dumps(record,ensure_ascii=False,sort_keys=True,indent=2)
            if path.exists() and path.read_text(encoding='utf-8')!=encoded:
                raise ValueError('Existing staged unit differs; explicit version migration required')
            if not path.exists(): path.write_text(encoded,encoding='utf-8')
            records.append({'id':candidate['id'],'status':record['status'],'case_index':row['case_index']})
    result={'source_cases':len(rows),'units':records,'published':0,'diagnostics':diagnostics,
            'validator_sha256':hashlib.sha256((ROOT/'intelligence/units.py').read_bytes()).hexdigest()}
    (dest/'staging-report.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({'source_cases':len(rows),'staged_units':len(records),'published':0,
                      'held_unit_count':sum(r['status']=='held' for r in records)}))


if __name__=='__main__': main()
