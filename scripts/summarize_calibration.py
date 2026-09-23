"""Read-only diagnostic report; never repairs or publishes candidate cards."""
import argparse
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def quote_status(quote, text):
    if not isinstance(quote,str): return 'invalid_type'
    if quote in text: return 'exact'
    # Diagnose formatting without silently fixing it or accepting the card.
    if len(quote)>2 and quote[0]==quote[-1]=='"' and quote[1:-1] in text:
        return 'added_quote_wrapper'
    return 'unmatched'


def summarize(directory):
    grouped=defaultdict(list)
    records=[]
    for path in sorted(directory.glob('*.json')):
        obj=json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(obj,dict) or 'summary' not in obj or 'evidence' not in obj: continue
        summary=obj['summary']
        output=obj.get('output') or {}
        cards=output.get('cards',[])
        counts=Counter(quote_status(q,obj['evidence']['text']) for c in cards
                       for q in c.get('evidence_quotes',[]))
        row={**summary,'quote_diagnostics':dict(counts),'more_candidates':output.get('more_candidates'),
             'artifact':path.name}
        records.append(row)
        grouped[summary['provider']].append(row)
    totals={}
    for provider,rows in grouped.items():
        quote_counts=Counter()
        for row in rows: quote_counts.update(row['quote_diagnostics'])
        totals[provider]={'requests':len(rows),'candidate_cards':sum(r['cards'] for r in rows),
                         'schema_and_exact_quote_passes':sum(not r['checks'] for r in rows),
                         'incomplete_outputs':sum('incomplete_output' in r['checks'] for r in rows),
                         'booked_cost_usd':round(sum(r['booked_cost_usd'] for r in rows),6),
                         'mean_seconds':round(statistics.mean(r['seconds'] for r in rows),2),
                         'continuation_flags':sum(r['more_candidates'] is True for r in rows),
                         'quote_diagnostics':dict(quote_counts)}
    return {'providers':totals,'records':records,
            'limitations':['Exact quotation is not semantic support or provenance verification.',
                          'Three-card cap prevents measuring complete extraction recall.',
                          'Different passages and completion caps prevent direct quality comparison with v1.',
                          'Added quotation wrappers are reported, not repaired or accepted.']}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--directory',default='data/calibration-body-high')
    args=parser.parse_args()
    dest=ROOT/args.directory
    result=summarize(dest)
    (dest/'diagnostics.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({'providers':result['providers'],'limitations':result['limitations']}))
