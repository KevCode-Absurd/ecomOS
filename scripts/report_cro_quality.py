"""Audit CRO revision gates without promoting or publishing any card."""
import collections,json,sqlite3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(path):return json.loads(path.read_text(encoding='utf-8'))
def main():
    d=ROOT/'data/cro-folder-v1';initial=collections.Counter();rows=[]
    for i in range(52):
        reviewpath=d/f'review-{i:03d}.json';row={'batch':i}
        old=read(reviewpath) if reviewpath.exists() else None
        old_verdicts={v['candidate_id']:v['verdict'] for v in old['review']['reviews']} if old and isinstance(old.get('review'),dict) else {}
        initial.update(old_verdicts.values())
        row['initial_review_errors']=old['errors'] if old else ['missing_review']
        rp=d/f'repaired-{i:03d}.json';cp=d/f'recheck-{i:03d}.json'
        row['repair_present']=rp.exists();row['recheck_present']=cp.exists();row['ready_for_next_evaluation']=False
        if rp.exists():
            repair=read(rp);checked=repair['checked'];row['repair_errors']=checked['errors'];row['repair_held']=len(checked['held']);row['repaired_candidates']=len(checked['candidates'])
            if cp.exists():
                check=read(cp);row['recheck_errors']=check['errors'];review=check.get('review') or {}
                verdicts={v['candidate_id']:v['verdict'] for v in review.get('reviews',[]) if isinstance(v,dict) and 'candidate_id' in v and 'verdict' in v}
                inherited=check.get('unchanged_inheritance',{})
                effective={c['id']:verdicts.get(c['id'],old_verdicts.get(inherited.get(c['id']),'unreviewed')) for c in checked['candidates']}
                row['effective_verdicts']=dict(collections.Counter(effective.values()))
                row['remaining_omissions']=len(review.get('omissions',[]));row['unresolved_source_questions']=len(checked.get('unresolved',[]))
                row['ready_for_next_evaluation']=bool(effective) and not checked['errors'] and not checked['held'] and not check['errors'] and not row['remaining_omissions'] and not row['unresolved_source_questions'] and all(v=='supported' for v in effective.values())
        rows.append(row)
    db=sqlite3.connect(d/'spend.sqlite');spend=[]
    for provider,actual,reserved,n in db.execute('SELECT provider,COALESCE(SUM(actual),0),COALESCE(SUM(CASE WHEN actual IS NULL THEN reserved ELSE 0 END),0),SUM(CASE WHEN actual IS NULL THEN 1 ELSE 0 END) FROM spend GROUP BY provider'):
        spend.append({'provider':provider,'recorded_usd':actual/1e6,'retained_or_active_usd':reserved/1e6,'pending_requests':n})
    db.close()
    summary={'first_pass_batches':52,'initial_review_verdicts':dict(initial),'repair_batches':sum(x['repair_present'] for x in rows),'rechecked_batches':sum(x['recheck_present'] for x in rows),'batches_passing_next_evaluation_gates':sum(x['ready_for_next_evaluation'] for x in rows),'published_cards':0,'spend':spend,'limitations':'Model source-support checks are not independent verification of truth, freshness, authorship, retrieval quality or brand outcomes. Passing these gates does not authorize publication or execution.'}
    (d/'quality-report.json').write_text(json.dumps({'summary':summary,'batches':rows},indent=2),encoding='utf-8');print(json.dumps(summary))
if __name__=='__main__':main()
