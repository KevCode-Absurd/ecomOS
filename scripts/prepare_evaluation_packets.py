"""Explicit model-reviewed development selections; not production approval.

Changes are logged against immutable raw extraction outputs. This deliberately
uses known relevant sources to isolate representation, not retrieval quality.
"""
import copy
import json
from calibration_client import ROOT
from intelligence.units import validate_output

SELECTIONS={2:['u1','u2','u9','u10'],8:['u7','u9','u12','u13','u14','u15'],
            19:['u1','u2','u4','u6','u13','u14','u15']}


def main():
    sources=json.loads((ROOT/'data/body-evaluation-proposal.json').read_text(encoding='utf-8'))['passages']
    rows=json.loads((ROOT/'data/calibration-v2/summary-controls.json').read_text(encoding='utf-8'))
    packets={}; audit=[]
    for index,ids in SELECTIONS.items():
        row=next(r for r in rows if r['case_index']==index and r['provider']=='openai' and r['effort']=='high')
        if not row['complete']: raise ValueError('Incomplete extraction')
        result=json.loads((ROOT/'data/calibration-v2'/(row['request_id']+'.json')).read_text(encoding='utf-8'))
        original={u['id']:u for u in result['output']['units']}
        chosen=[]
        for uid in ids:
            unit=copy.deepcopy(original[uid]); edits=[]
            if index==2 and uid=='u1':
                unit['exclusions']={'op':'any','args':[]}
                edits.append('Removed circular exclusion: the duplicate gift is the choice the action warns against, not a reason to hide the warning.')
            if index==2 and uid=='u9':
                unit['action']['quote']=unit['claim']['quote']
                edits.append('Bound the action to the specific product/stage quote already supplied for the claim.')
            if index==8 and uid=='u9':
                unit['kind']='principle'; unit['action']=None; unit['completion']=[]
                edits.append('Kept the attributed sample-size practice as a principle; removed a universal-looking command and completion threshold.')
            if index==19 and uid=='u2':
                unit['relations']=[]
                edits.append('Within-platform and cross-platform advice have different applicability; removed false conflict relation.')
            audit.append({'case_index':index,'unit_id':uid,'extraction_request':row['request_id'],
                          'review':'model_reviewed_for_evaluation_only','edits':edits,'original':original[uid],'reviewed':unit})
            chosen.append(unit)
        checked=validate_output({'units':chosen,'more_units':True,'unresolved':[]},sources[index])
        if checked['errors'] or checked['held']: raise ValueError('Selected unit failed evidence/relationship check')
        context=[]
        for candidate in checked['candidates']:
            unit=copy.deepcopy(candidate['unit']); unit['id']='case'+str(index)+'-'+unit['id']
            for r in unit['relations']: r['target']='case'+str(index)+'-'+r['target']
            # Only empty values are omitted; conditions and qualifications are never shortened.
            for key in ['trigger','prerequisites','exclusions']:
                if unit[key]=={'op':'all','args':[]} or unit[key]=={'op':'any','args':[]}: del unit[key]
            for key in ['completion','relations']:
                if not unit[key]: del unit[key]
            unit['provenance']='unverified_source; model-reviewed evaluation candidate'
            context.append(unit)
        packets[str(index)]={'review_status':'model_reviewed_for_evaluation_only',
                             'source_sha256':sources[index]['source_sha256'],'context':context,
                             'selection':'known relevant source; not automated retrieval',
                             'evidence_bindings':checked['candidates']}
    (ROOT/'data/evaluation-packets.json').write_text(json.dumps(packets,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'data/evaluation-packet-review.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'packets':len(packets),'selected_units':sum(len(v['context']) for v in packets.values()),
                      'review_edits':sum(len(a['edits']) for a in audit),'production_approved':False}))


if __name__=='__main__': main()
