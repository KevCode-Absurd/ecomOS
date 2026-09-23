"""Small same-model baseline comparison; saves outputs for human inspection."""
import json
import argparse
from concurrent.futures import ThreadPoolExecutor
from calibration_client import ROOT, run_call
from search_library import retrieve

CASES = [
    {'name':'low-traffic-testing','query':'Should we run an A/B test or use customer research to improve conversion?',
     'brand':'DTC skincare store; 1500 sessions and 20 purchases per month; no device breakdown yet.', 'complexity':'focused'},
    {'name':'mobile-checkout','query':'Build a prioritized investigation and action plan for mobile checkout abandonment using session recordings.',
     'brand':'Apparel store; 80% mobile traffic; desktop purchase conversion is 3%, mobile is 0.8%; no checkout-step data supplied.', 'complexity':'broad'},
    {'name':'popup-incrementality','query':'Our popup increased email signups. How do we decide whether to keep it?',
     'brand':'DTC coffee brand; email signups rose 40% after adding a discount popup; revenue impact and margin impact are unknown.', 'complexity':'focused'},
]


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--case',choices=[c['name'] for c in CASES]);args=parser.parse_args()
    destination=ROOT/'data/library-v3/evaluation';destination.mkdir(exist_ok=True)
    system='You are an ecommerce advisor. Return JSON with diagnosis, actions, missing_information, and caveats. Be specific and concise. Do not invent facts, expected uplifts or thresholds. Use supplied knowledge where applicable, and general knowledge where useful. Do not claim to have browsed or inspected unavailable data.'
    packets=[]
    for case in CASES:
        if args.case and case['name']!=args.case:continue
        packet=retrieve(case['query'],case['brand'],case['complexity'])
        packets.append((case,packet))
    def run(item):
        case,packet,variant=item
        user={'task':case['query'],'brand':case['brand'],'knowledge':packet['context'] if variant=='with_library' else ''}
        result=run_call('library-evaluation-v3','openai','low',system,user,limit=8192,stage_limit=5)
        if result['finish_reason']!='stop' or result['output'] is None:raise ValueError('Incomplete evaluation')
        row={'case':case,'variant':variant,'model':result['model'],'answer':result['output'],
             'usage':result['usage'],'estimated_cost_usd':result['booked_cost_usd'],
             'knowledge_tokens':packet['knowledge_tokens'] if variant=='with_library' else 0,
             'retrieved_titles':[c['title'] for c in packet['cards']] if variant=='with_library' else []}
        (destination/(case['name']+'-'+variant+'.json')).write_text(json.dumps(row,ensure_ascii=False,indent=2),encoding='utf-8')
        print(json.dumps({'case':case['name'],'variant':variant,'knowledge_tokens':row['knowledge_tokens'],'cost':row['estimated_cost_usd']}),flush=True)
    with ThreadPoolExecutor(max_workers=3) as pool:
        list(pool.map(run,[(case,packet,variant) for case,packet in packets for variant in ['baseline','with_library']]))


if __name__=='__main__':main()
