"""Lossless source-evidence compaction for future context packing; no approval grant."""
import copy

def compact_card(card):
    sources=[];source_ids={};evidence=[];evidence_ids={};fields={}
    for span in card['evidence']:
        source=(span['source_id'],span['source_sha256'])
        if source not in source_ids:
            sid='s'+str(len(sources)+1);source_ids[source]=sid
            sources.append({'id':sid,'source_id':source[0],'version':source[1]})
        key=(source,span['locator'],span['start'],span['end'],span['quote'])
        if key not in evidence_ids:
            eid='e'+str(len(evidence)+1);evidence_ids[key]=eid
            evidence.append({'id':eid,'source':source_ids[source],'locator':span['locator'],'start':span['start'],'end':span['end'],'quote':span['quote']})
        refs=fields.setdefault(span['field'],[])
        if evidence_ids[key] not in refs:refs.append(evidence_ids[key])
    def statement(value,path):
        if value is None:return None
        if set(value)=={'text','quote'}:
            if not fields.get(path):raise ValueError('Missing evidence for '+path)
            return {'text':value['text'],'evidence_refs':fields[path]}
        if set(value)=={'op','args'}:
            return {'op':value['op'],'args':[statement(v,path+'.'+str(i)) for i,v in enumerate(value['args'])]}
        raise ValueError('Unexpected statement structure')
    unit=copy.deepcopy(card['unit'])
    for field in ['claim','action','trigger','prerequisites','exclusions']:unit[field]=statement(unit[field],field)
    if 'resolved_relations' in card:unit['relations']=copy.deepcopy(card['resolved_relations'])
    unit['completion']=[statement(v,'completion.'+str(i)) for i,v in enumerate(unit['completion'])]
    return {'id':card['id'],'unit':unit,'sources':sources,'evidence':evidence,
        'source_support_verdict':card.get('source_support_verdict','unreviewed'),
        'review_output_valid':card.get('review_output_valid',False),
        'provenance':card.get('provenance','unverified'),
        'source_limitations':copy.deepcopy(card.get('source_limitations',[])),
        'batch_validation_errors':copy.deepcopy(card.get('batch_validation_errors',[])),
        'batch_held_units':card.get('batch_held_units',0),
        'evidence_role_hints':copy.deepcopy(card.get('evidence_role_hints',[])),
        'needs_primary_body_evidence':card.get('needs_primary_body_evidence',False),'publication_allowed':False}
