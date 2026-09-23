"""Build review-aware working revisions and actionable remaining work; no publishing."""
import collections,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def main():
    d=ROOT/'data/cro-folder-v1';cards=[];tasks=[]
    for i in range(52):
        oldreview=read(d/f'review-{i:03d}.json');oldverdicts={v['candidate_id']:v['verdict'] for v in oldreview['review']['reviews']}
        rp=d/f'repaired-{i:03d}.json';cp=d/f'recheck-{i:03d}.json'
        if not rp.exists():tasks.append({'batch':i,'task':'repair_first_pass'});continue
        repair=read(rp);checked=repair['checked']
        if checked['errors'] or checked['held']:tasks.append({'batch':i,'task':'repair_evidence_or_structure','errors':checked['errors'],'held':checked['held']})
        check=read(cp) if cp.exists() else None
        if not check:tasks.append({'batch':i,'task':'recheck_repaired_cards'})
        elif check['errors']:tasks.append({'batch':i,'task':'fix_review_validation','errors':check['errors']})
        if checked.get('unresolved'):tasks.append({'batch':i,'task':'resolve_source_context','questions':checked['unresolved']})
        review=check.get('review',{}) if check else {};review=review if isinstance(review,dict) else {}
        verdicts={v['candidate_id']:v['verdict'] for v in review.get('reviews',[]) if isinstance(v,dict) and 'candidate_id' in v and 'verdict' in v}
        inherited=check.get('unchanged_inheritance',{}) if check else {}
        ids={c['unit']['id']:c['id'] for c in checked['candidates']}
        for card in checked['candidates']:
            verdict=verdicts.get(card['id'],oldverdicts.get(inherited.get(card['id']),'unreviewed'))
            if verdict in ['revise','unsupported']:tasks.append({'batch':i,'task':'semantic_correction','candidate_id':card['id'],'verdict':verdict})
            if verdict=='unreviewed' and check and not check['errors']:tasks.append({'batch':i,'task':'missing_card_verdict','candidate_id':card['id']})
            cards.append({**card,'batch':i,'revision_request_id':repair['request_id'],'source_support_verdict':verdict,
                'review_output_valid':bool(check and not check['errors']),
                'batch_validation_errors':checked['errors'],'batch_held_units':len(checked['held']),
                'resolved_relations':[{'kind':r['kind'],'target':ids.get(r['target'])} for r in card['unit']['relations']],
                'source_limitations':review.get('source_limitations',[]),'publication_allowed':False})
        for omission in review.get('omissions',[]):tasks.append({'batch':i,'task':'extract_omitted_advice','detail':omission,'review_output_valid':not check['errors']})
    issues=d/'source-context-issues.json'
    if issues.exists():
        for issue in read(issues)['issues']:tasks.append({'task':'recover_original_source_context',**issue})
    tasks.extend([{'task':'cross_document_semantic_deduplication_and_conflict_review'}, {'task':'brand_scenario_retrieval_evaluation','note':'First-pass source review is not a retrieval or business-outcome benchmark.'}])
    report={'cards':cards,'publication_allowed':False,'note':'Working repair revisions only; original artifacts remain available, including failed and held outputs.'}
    (d/'revision-index.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    (d/'remaining-work.json').write_text(json.dumps({'tasks':tasks,'counts':dict(collections.Counter(t['task'] for t in tasks))},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'working_revision_cards':len(cards),'source_support_verdicts':dict(collections.Counter(c['source_support_verdict'] for c in cards)),'remaining_work_counts':dict(collections.Counter(t['task'] for t in tasks)),'published':0}))
if __name__=='__main__':main()
