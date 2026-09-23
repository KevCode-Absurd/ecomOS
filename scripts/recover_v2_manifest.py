"""Recover completed results without dispatching or retrying any provider call."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]


def main():
    dest=ROOT/'data/calibration-v2'
    sources=json.loads((ROOT/'data/body-evaluation-proposal.json').read_text(encoding='utf-8'))['passages']
    chosen={}
    for path in dest.glob('*.validation.json'):
        checked=json.loads(path.read_text(encoding='utf-8')); row=checked['summary']
        raw=json.loads((dest/(row['request_id']+'.json')).read_text(encoding='utf-8'))
        index=row['case_index']
        primary=raw['provider']=='deepseek' and raw['effort']=='high' and raw['completion_limit']==32768
        fallback=index==22 and raw['provider']=='openai' and raw['effort']=='high'
        if not (primary or fallback) or not row['complete']: continue
        source=sources[index]
        for field in ['source_id','source_sha256','locator','start','text']:
            if raw['input'][field]!=source[field]: raise ValueError('Experiment source mismatch')
        if index in chosen: raise ValueError('Ambiguous completed result; explicit selection needed')
        chosen[index]={**row,'selection':'separate_provider_fallback' if fallback else 'primary'}
    if set(chosen)!=set(range(24)):
        raise ValueError('Missing completed cases: '+str(sorted(set(range(24))-set(chosen))))
    (dest/'summary-staging.json').write_text(json.dumps([chosen[i] for i in range(24)],indent=2),encoding='utf-8')
    (dest/'recovery-note.json').write_text(json.dumps({
        'primary_experiment':'DeepSeek high, 32768 completion limit',
        'primary_completed_cases':23,'primary_unknown_outcome_cases':[22],
        'fallback':'Case 22 separately processed by Terra high; not a retry or successful DeepSeek result.',
        'pending_reservation_policy':'Retained until provider billing/outcome is reconciled; no automatic resend.',
        'staging_manifest':'24 completed source-case results from mixed providers; not a 24/24 DeepSeek success claim.'
    },indent=2),encoding='utf-8')
    print(json.dumps({'completed_source_cases':24,'primary_results':23,'fallback_results':1,'unknown_primary_outcomes':1}))


if __name__=='__main__': main()
