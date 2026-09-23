"""Create local follow-up tasks; never equate a capped extraction with coverage."""
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from intelligence.units import validate_output


def main():
    dest=ROOT/'data/calibration-v2'
    summary=dest/'summary-staging.json'
    if not summary.exists(): raise ValueError('Validated staging manifest is not ready')
    rows=json.loads(summary.read_text(encoding='utf-8'))
    tasks=[]
    for row in rows:
        request_id=row['request_id']
        raw=json.loads((dest/(request_id+'.json')).read_text(encoding='utf-8'))
        checked=validate_output(raw['output'],raw['input'])
        common={'case_index':row['case_index'],'request_id':request_id,
                'status':'pending','automatic_dispatch':False}
        if not row['complete'] or checked['errors']:
            tasks.append({**common,'kind':'output_or_schema_review','reason':checked['errors'] or ['incomplete_output']})
        for held in checked['held']:
            tasks.append({**common,'kind':'evidence_repair_review','unit_index':held['index'],'reason':held['reason']})
        if checked.get('more_units'):
            tasks.append({**common,'kind':'extract_remaining_units','covered_claims':[
                {'id':c['unit']['id'],'claim':c['unit']['claim']['text']} for c in checked['candidates']]})
        if checked.get('unresolved'):
            tasks.append({**common,'kind':'source_context_review','issues':checked['unresolved']})
        tasks.append({**common,'kind':'semantic_and_coverage_review',
                      'note':'Source support, completeness, provenance and operational applicability remain unverified.'})
    result={'source_cases':len(rows),'tasks':tasks,'published_units':0,
            'verified_complete_cases':0,'scope':'approved excerpts only, not full documents',
            'note':'Local plan only. Neighboring or new excerpts require separate transmission authorization where applicable.'}
    (dest/'continuation-queue.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'source_cases':len(rows),'pending_tasks':len(tasks),'verified_complete_cases':0}))


if __name__=='__main__': main()
