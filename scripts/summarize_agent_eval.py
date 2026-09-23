"""Measured costs/context sizes, separated from qualitative decision review."""
import json
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]


def words(value):
    if isinstance(value,str): return len(value.split())
    if isinstance(value,dict): return sum(words(v) for v in value.values())
    if isinstance(value,list): return sum(words(v) for v in value)
    return 0


def main():
    dest=ROOT/'data/agent-ablation-v1'
    rows=json.loads((dest/'summary.json').read_text(encoding='utf-8'))
    groups=defaultdict(list); by_case=defaultdict(dict)
    for row in rows:
        obj=json.loads((dest/(row['request_id']+'.json')).read_text(encoding='utf-8'))
        row={**row,'output_words':words(obj['output'])}
        groups[row['mode']].append(row); by_case[row['case']][row['mode']]=row
    metrics={}
    for mode,items in groups.items():
        metrics[mode]={'requests':len(items),'complete':sum(r['complete'] for r in items),
                       'schema_id_passes':sum(not r['checks'] for r in items),
                       'over_350_words':sum(r['output_words']>350 for r in items),
                       'prompt_tokens':sum(r['prompt_tokens'] for r in items),
                       'completion_tokens':sum(r['completion_tokens'] for r in items),
                       'booked_cost_usd':round(sum(r['cost'] for r in items),6)}
    context_raw=sum(r['raw']['prompt_tokens']-r['none']['prompt_tokens'] for r in by_case.values())
    context_curated=sum(r['curated']['prompt_tokens']-r['none']['prompt_tokens'] for r in by_case.values())
    result={'modes':metrics,'library_prompt_token_estimate':{'raw':context_raw,'curated':context_curated},
            'total_prompt_reduction_curated_vs_raw_pct':round(100*(1-metrics['curated']['prompt_tokens']/metrics['raw']['prompt_tokens']),2),
            'context_reduction_curated_vs_raw_pct':round(100*(1-context_curated/context_raw),2),
            'cases':dict(by_case),'quality_claim':'No automated semantic or business-quality verdict.',
            'limitations':['Six development scenarios; preselected relevant sources, not retrieval benchmark.',
                          'One response per condition; no variance estimate or held-out evaluation.',
                          'Curated packets were model-reviewed with four logged corrections.',
                          'Extraction and executor use Terra for these packets; not model-independent validation.',
                          'Both condition and source familiarity may be inferable from citations despite masked labels.']}
    (dest/'metrics.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='cases'}))


if __name__=='__main__': main()
