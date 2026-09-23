"""Offline, explicit workflow loading; no model calls or automatic execution."""
import argparse
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def load_workflow(directory, workflow_id, card_ids=None, with_foundations=False):
    catalog=json.loads((directory/'catalog.json').read_text(encoding='utf-8'))
    match=next((d for d in catalog['domains'] if any(w['id']==workflow_id for w in d['workflows'])),None)
    if match is None:raise ValueError('Unknown workflow ID')
    pack=json.loads((directory/match['path']).read_text(encoding='utf-8'))
    workflow=next(w for w in pack['workflows'] if w['id']==workflow_id)
    if card_ids is not None:
        available={c['id'] for c in workflow['supporting_cards']}
        if set(card_ids)-available:raise ValueError('Requested card is not a supporting candidate for this workflow')
        workflow['supporting_cards']=[c for c in workflow['supporting_cards'] if c['id'] in card_ids]
    return dict(status=pack['status'],version=pack['version'],source_catalog_sha256=pack['source_catalog_sha256'],
                system_prompt=pack.get('system_prompt'),editorial_principles=pack.get('editorial_principles',[]),
                operating_contract=(directory/'OPERATING_CONTRACT.md').read_text(encoding='utf-8'),
                required_inputs=pack['required_inputs'],measures=pack['measures'],workflow=workflow,
                foundation_candidates=pack['foundation_candidates'] if with_foundations else [],
                note='Candidate support requires applicability review. This loader does not execute the workflow or verify current facts.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--directory',type=Path,default=ROOT/'playbooks/v1')
    group=p.add_mutually_exclusive_group(required=True);group.add_argument('--list',action='store_true');group.add_argument('--workflow')
    p.add_argument('--card-id',action='append');p.add_argument('--with-foundations',action='store_true');a=p.parse_args()
    if a.list:
        data=json.loads((a.directory/'catalog.json').read_text(encoding='utf-8'))
        result=[w for d in data['domains'] for w in d['workflows']]
    else:result=load_workflow(a.directory,a.workflow,a.card_id,a.with_foundations)
    print(json.dumps(result,ensure_ascii=False,indent=2))
