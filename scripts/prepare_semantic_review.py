"""Bind model-reviewed audit criteria to immutable selected source spans.

This is a draft reference set, not independently certified ground truth or an
automated semantic judge. Labels must not be used to tune a held-out test set.
"""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]



def main():
    passages=json.loads((ROOT/'data/body-evaluation-proposal.json').read_text(encoding='utf-8'))['passages']
    cases=[]
    for index,specs in json.loads((ROOT/'data/semantic-review-specs.json').read_text(encoding='utf-8')).items():
        index=int(index)
        passage=passages[index]
        annotations=[]
        for key,requirement,quote in specs:
            local=passage['text'].find(quote)
            if local<0: raise ValueError('Annotation anchor absent: '+key)
            start=passage['start']+local
            annotations.append({'id':key,'requirement':requirement,'anchor':quote,
                                'source_start':start,'source_end':start+len(quote),
                                'review_status':'model_reviewed_pending_independent_review'})
        cases.append({'case_index':index,'document':passage['document'],
                      'source_identity':{k:passage[k] for k in ('source_id','source_sha256','locator') if k in passage},
                      'criteria':annotations})
    result={'purpose':'semantic coverage and qualification audit',
            'not_ground_truth':True,'independent_review_complete':False,
            'exhaustive_coverage_claimed':False,'cases':cases}
    (ROOT/'data/semantic-review-draft.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'cases':len(cases),'anchored_review_criteria':sum(len(c['criteria']) for c in cases),
                      'status':'draft_not_independently_verified'}))


if __name__=='__main__': main()
