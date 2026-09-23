"""Build auditable draft playbooks locally; never alter the source library or call APIs."""
import argparse
import collections
import hashlib
import json
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from playbooks.domain_specs import specs


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def evidence(card):
    return {k: card[k] for k in ('id','title','summary','use_when','steps','caveats','source_id','source_name','folder','domain','section')}


def build(destination):
    if destination.exists():
        raise ValueError('Output exists. Use a new version directory; do not overwrite reviewed playbooks.')
    source = ROOT/'data/library-v3/cards.json'
    initial_hash = digest(source)
    cards = json.loads(source.read_text(encoding='utf-8'))['cards']
    by_id = {c['id']: c for c in cards}
    if len(by_id) != len(cards):
        raise ValueError('Duplicate source card IDs')
    metadata = json.loads((source.parent/'metadata.json').read_text(encoding='utf-8'))['cards']
    domains = specs()
    observed = {c['domain'] for c in cards}
    if observed != set(domains)|{'multi'}:
        raise ValueError('Domain specification does not cover the current catalog')
    db = sqlite3.connect(':memory:')
    db.execute("CREATE VIRTUAL TABLE lookup USING fts5(id UNINDEXED,title,tags,summary,body,tokenize='porter unicode61')")
    for c in cards:
        db.execute('INSERT INTO lookup VALUES(?,?,?,?,?)',(c['id'],c['title'],' '.join(c['tags']),c['summary'],' '.join([c['use_when'],*c['steps'],*c['caveats']])))

    def rank(query, allowed):
        tokens = sorted(set(re.findall(r'[a-z0-9]+',query.lower())))
        match = ' OR '.join('"'+t+'"' for t in tokens)
        rows = db.execute('SELECT id,bm25(lookup,0,5,4,3,1) FROM lookup WHERE lookup MATCH ? ORDER BY 2,id',(match,)).fetchall()
        return [(k,-score) for k,score in rows if k in allowed]

    all_multi = {c['id'] for c in cards if c['domain']=='multi'}
    routes = collections.defaultdict(list)
    catalog = []
    for domain, spec in domains.items():
        own = {c['id'] for c in cards if c['domain']==domain}
        inventory = [dict(id=c['id'], title=c['title'],source_id=c['source_id']) for c in cards if c['id'] in own]
        pack = dict(schema_version=1,version='1.0.0-draft',status='draft',domain=domain,
                    source_catalog_sha256=initial_hash,required_inputs=spec['required_inputs'],
                    measures=spec['measures'],related_domains=spec['related_domains'],
                    evidence_method='Local BM25 candidate selection; authored workflow steps are proposals, not source quotations or verified synthesis.',
                    operating_contract='../OPERATING_CONTRACT.md',workflows=[])
        foundation = {k for k in own if 'foundation' in metadata.get(k,{}).get('roles',[]) or metadata.get(k,{}).get('knowledge_type')=='principle'}
        foundation_query = ' '.join(w['query'] for w in spec['workflows'])
        foundation_ranked = rank(foundation_query, foundation)
        pack['foundation_candidates'] = [evidence(by_id[k]) for k,_ in foundation_ranked[:3]]
        pack['foundation_note'] = 'Inferred principle labels do not establish universal applicability. Retain source conditions; empty means no matched labelled principle, not absence of foundational knowledge.'
        for w in spec['workflows']:
            ranked = rank(w['query'], own)
            selected=[]; used_sources=set()
            # Prefer independent source documents where lexical matches exist.
            for k,score in ranked:
                if by_id[k]['source_id'] not in used_sources:
                    selected.append((k,score));used_sources.add(by_id[k]['source_id'])
                if len(selected)==3:break
            for item in ranked:
                if len(selected)>=3:break
                if item[0] not in {k for k,_ in selected}:selected.append(item)
            if not selected:raise ValueError('No evidence candidate for '+w['id'])
            supplementary=rank(w['query'],all_multi)[:3]
            for k,score in supplementary:
                routes[k].append(dict(domain=domain,workflow=w['id'],lexical_score=round(score,6)))
            workflow={**w,'status':'draft','steps_origin':'authored orchestration draft',
              'retrieval':dict(primary_domain=domain,related_domains=spec['related_domains'],query=w['query'],
                   selected_card_ids=[k for k,_ in selected],mixed_candidate_ids=[k for k,_ in supplementary],
                   fallback='Search primary and related domains using the task and actual constraints; do not silently switch to a different workflow.',
                   selection_status='candidate-support-needs-applicability-review'),
              'supporting_cards':[evidence(by_id[k]) for k,_ in selected],
              'candidate_scores':[dict(card_id=k,score=round(score,6)) for k,score in selected],
              'applicability_checks':['Does this advice fit the product lifecycle, market, audience and requested deliverable?',
                'Does it require proof, access, budget or assets the brand does not have?',
                'Does it change a fixed price, offer, policy or other explicit constraint?',
                'Are platform details or numerical claims current and substantiated?'],
              'output_checks':['Deliver the specified artifact, not general advice about creating it.',
                'Use supplied brand facts; label hypotheses and missing inputs separately.',
                'Preserve relevant source conditions; do not copy another business’s proof or results.',
                'Include an owner, measurement and decision rule when proposing a test.',
                'Check the output against the requested constraints and owner feedback.'],
              'completion_rule':'Stop after the requested artifact passes factual and brief checks; allow at most two revision passes, then report the unresolved issue.',
              'action_boundary':'Prepare recommendations/artifacts only. Publication, spend changes, customer contact and production modifications require separate task authorization.'}
            pack['workflows'].append(workflow)
        write(destination/domain/'playbook.json',pack)
        write(destination/domain/'card-index.json',dict(domain=domain,cards=inventory))
        lines=[f'# {domain.replace("-"," ").title()} — draft playbook', '',
          '**Status:** source-linked draft; not owner-approved or outcome-tested.',
          '', 'Read [the operating contract](../OPERATING_CONTRACT.md) before using a workflow.',
          '', '## Inputs', *['- '+x for x in spec['required_inputs']], '',
          '## Measures', *['- '+x for x in spec['measures']], '',
          '## Foundation candidates',pack['foundation_note']]
        for c in pack['foundation_candidates']:
            lines += ['',f'- **{c["title"]}** (`{c["id"]}`): {c["summary"]}', '  Applies when: '+c['use_when']]
            lines += ['  Condition: '+s for s in c['caveats']]
        for w in pack['workflows']:
            lines += ['', '## '+w['title'],f'Workflow ID: `{w["id"]}`','',
              '**Deliverable:** '+w['deliverable'],'','### Proposed decision sequence']
            lines += [f'{i}. {s}' for i,s in enumerate(w['steps'],1)]
            lines += ['', '### Supporting knowledge candidates',
               'These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.']
            for c in w['supporting_cards']:
                lines += ['',f'#### {c["title"]}',f'Card: `{c["id"]}` · Source: {c["source_name"]} · Section: {c["section"]}',
                          '',c['summary'],'','Applies when: '+c['use_when'],'']
                lines += ['- '+s for s in c['steps']]
                lines += ['- **Condition:** '+s for s in c['caveats']]
            lines += ['', '### Retrieval and applicability',f'Search: `{w["query"]}`',
                     'Related domains: '+', '.join(spec['related_domains']),
                     'Mixed-folder candidate IDs: '+(', '.join(w['retrieval']['mixed_candidate_ids']) or 'None'),
                     '',*['- '+x for x in w['applicability_checks']], '', '### Output checks',
                     *['- '+x for x in w['output_checks']], '',w['completion_rule']]
        (destination/domain/'README.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
        catalog.append(dict(domain=domain,card_count=len(own),status='draft',path=domain+'/playbook.json',
                            workflows=[{k:w[k] for k in ('id','title','deliverable')} for w in pack['workflows']]))
    multi_records=[dict(id=k,title=by_id[k]['title'],candidate_routes=routes[k],
                        status='candidate-routes' if routes[k] else 'unassigned-needs-task-search') for k in sorted(all_multi)]
    write(destination/'multi/routing.json',dict(status='draft',method='Top three lexical matches per workflow; no claim of exhaustive semantic routing',cards=multi_records))
    (destination/'multi/README.md').write_text('# Mixed-source routing guide\n\nThe mixed folder is not an execution workflow. Use the target domain workflow and search this pool for supporting knowledge.\n\nAll '+str(len(all_multi))+' mixed card IDs are retained in routing.json. Candidate links are suggestions, not confirmed applicability. Unassigned cards remain searchable in the original library; they have not been discarded.\n',encoding='utf-8')
    write(destination/'catalog.json',dict(schema_version=1,status='draft',source_catalog_sha256=initial_hash,
             source_card_count=len(cards),domains=catalog,mixed_folder='multi/routing.json'))
    (destination/'OPERATING_CONTRACT.md').write_text((ROOT/'playbooks/OPERATING_CONTRACT.md').read_text(encoding='utf-8'),encoding='utf-8')
    index=['# Ecommerce playbook catalog — v1 draft','',
       '23 domain playbooks, 69 task workflows, and one mixed-source routing guide. All require applicability review and owner testing.',
       '', '| Domain | Source cards | Task workflows |','|---|---:|---|']
    for d in catalog:
        index.append('| ['+d['domain']+']('+d['domain']+'/README.md) | '+str(d['card_count'])+' | '+'; '.join(w['title'] for w in d['workflows'])+' |')
    index += ['', '[Mixed-source routing guide](multi/README.md)', '',
      '[Operating contract](OPERATING_CONTRACT.md) · [Build report](BUILD_REPORT.json)', '',
      'The full card catalog is unchanged. Domain indexes account for every original card; workflow support is deliberately selective.']
    (destination/'INDEX.md').write_text('\n'.join(index)+'\n',encoding='utf-8')
    write(destination/'BUILD_REPORT.json',dict(source_cards=len(cards),domain_playbooks=len(domains),
       task_workflows=sum(len(d['workflows']) for d in catalog),mixed_cards=len(all_multi),
       mixed_cards_with_candidate_routes=len([r for r in multi_records if r['candidate_routes']]),
       mixed_cards_unassigned=len([r for r in multi_records if not r['candidate_routes']]),
       source_hash_before=initial_hash,source_hash_after=digest(source),external_api_calls=0,
       limitations=['No semantic/LLM synthesis or conflict reconciliation performed.',
       'Evidence links are keyword-ranked candidates, not sentence-level verified support.',
       'All workflows need owner review and task testing before autonomous use.',
       'Mixed routing is deliberately partial and explicitly records all unassigned cards.']))
    if digest(source)!=initial_hash:raise ValueError('Source changed during build')
    db.close()
    return destination


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT/'playbooks/v1')
    args=parser.parse_args();print(build(args.output))
