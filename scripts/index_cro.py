"""Build a private, review-gated CRO candidate index and explicit follow-up queue."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    directory=ROOT/'data/cro-folder-v1'
    manifest=json.loads((ROOT/'data/cro-folder-proposal.json').read_text(encoding='utf-8'))
    rows=[json.loads(p.read_text(encoding='utf-8')) for p in sorted(directory.glob('batch-*-round-*.json'))]
    latest={};by_batch={};tasks=[];cards={}
    for row in rows:
        i=row['batch'];latest[i]=row;by_batch.setdefault(i,[]).extend(row['candidates'])
        for held in row['held']:tasks.append({'batch':i,'kind':'evidence_repair','detail':held})
        if row['errors']:tasks.append({'batch':i,'kind':'response_repair','detail':row['errors']})
        local_ids={c['unit']['id']:c['id'] for c in row['candidates']}
        for card in row['candidates']:
            resolved=[{'kind':r['kind'],'target':local_ids.get(r['target']),'original_local_target':r['target']} for r in card['unit']['relations']]
            cards[card['id']]={**card,'batch':i,'request_id':row['request_id'],'response_validation_errors':row['errors'],'resolved_relations':resolved,'relationship_status':'held' if any(r['target'] is None for r in resolved) else 'resolved_within_response','publication_allowed':False,'review_status':'pending'}
    for i,batch in enumerate(manifest['batches']):
        if i not in latest:
            tasks.append({'batch':i,'kind':'missing_extraction','detail':'No usable result; inspect pending request ledger before any dispatch.'});continue
        row=latest[i]
        if row.get('more_units') or row.get('unresolved') or row.get('finish_reason')!='stop':
            tasks.append({'batch':i,'kind':'continuation_or_context','detail':row.get('unresolved',[])})
        reviewpath=directory/f'review-{i:03d}.json'
        if not reviewpath.exists():tasks.append({'batch':i,'kind':'semantic_and_coverage_review'});continue
        review=json.loads(reviewpath.read_text(encoding='utf-8'))
        if review['errors']:
            tasks.append({'batch':i,'kind':'review_repair','detail':review['errors']});continue
        seen=set()
        for verdict in review['review']['reviews']:
            uid=verdict['candidate_id'];seen.add(uid)
            if uid not in cards:continue
            cards[uid]['review_status']=verdict['verdict']
            cards[uid]['review_reasons']=verdict['reasons']
            if verdict['verdict']!='supported':tasks.append({'batch':i,'kind':'semantic_repair','candidate_id':uid,'detail':verdict['reasons']})
        missing={c['id'] for c in by_batch[i]}-seen
        if missing:tasks.append({'batch':i,'kind':'review_new_candidates','candidate_ids':sorted(missing)})
        for omission in review['review']['omissions']:tasks.append({'batch':i,'kind':'omitted_advice','detail':omission})
    # Exact-text duplicate hints only; no destructive merges or evidence deletion.
    groups={}
    for uid,card in cards.items():
        key=(card['unit']['kind'],' '.join(card['unit']['claim']['text'].lower().split()))
        groups.setdefault(key,[]).append(uid)
    duplicates=[v for v in groups.values() if len(v)>1]
    result={'cards':list(cards.values()),'exact_claim_duplicate_groups':duplicates,
            'publication_allowed':False,'note':'Source support is not source verification or execution authorization.'}
    (directory/'candidate-index.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    (directory/'followups.json').write_text(json.dumps({'tasks':tasks,'verified_complete_batches':0},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'indexed_candidates':len(cards),'followups':len(tasks),'duplicate_groups':len(duplicates),'published':0}))
if __name__=='__main__':main()
