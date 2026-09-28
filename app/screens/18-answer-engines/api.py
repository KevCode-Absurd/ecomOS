"""Answer engines API: /api/18-answer-engines/...

  GET overview?brand=bombas   tiles, engines, facts, sample prompts, insights, chart, findings, rules
  GET findings?brand=bombas   the audit findings only (audit.py, contract shape)

No answer engine is connected, so mention, recommend and citation numbers read unavailable with the
source named. What round 0 reads is readiness, from the brand brain: which facts an engine could cite,
which sample buyer prompts the brain can answer, and where each fact lives. AI referral sessions read
from the sessions table and stay unavailable while it holds no AI engine source. Insights are rules in
`insights()`, each with the sentence it produces and its capability. Missing is unavailable, never 0.
Default brand is bombas (simulated store data, public brain). Read-only.
"""
import importlib.util
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _audit():
    spec = importlib.util.spec_from_file_location('answer_engines_audit', HERE / 'audit.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


audit = _audit()
DEFAULT_BRAND = 'bombas'
LOG_FIX = 'prompt-run script (ORG-C37)'
ENGINE_METRICS = ['ai_mention_rate', 'ai_recommend_rate', 'ai_share_of_voice', 'ai_sentiment_score',
                  'citation_source_share']


def _tile(name, plain, value, unit, **extra):
    out = {'name': name, 'plain': plain, 'unit': unit, 'value': value}
    out.update(extra)
    return out


def _unavail(name, plain, unit, reason, fix):
    return _tile(name, plain, None, unit, unavailable_reason=reason, fix=fix)


# ---------------------------------------------------------------- tiles

def tiles(br, cov, facts, sessions, ends_on):
    if br is None:
        answer = _unavail('Buyer prompts answered', 'Sample buyer prompts the brand brain holds every fact for.', 'n',
                          'the brand brain is not built', 'brain')
        core = _unavail('Core facts on a facts page', 'Of 6 core facts, how many sit on a page built for citation.', 'n',
                        'the brand brain is not built', 'brain')
    else:
        ok = [p for p in cov if p['answerable']]
        answer = _tile('Buyer prompts answered', f'Of {len(cov)} sample buyer prompts, how many the brand brain holds every '
                       f'fact for. The prompts are a sample, not a run on any engine.', len(ok), 'n', of=len(cov),
                       window='brain as of ' + ends_on.isoformat(), tone='bad' if len(ok) < len(cov) else 'good')
        pages = set(audit.facts_pages(br))
        on_page = [c for c in audit.CORE if any(r['page'] in pages for r in facts.get(c, []))]
        on_file = [c for c in audit.CORE if facts.get(c)]
        core = _tile('Core facts on a facts page', f'Of {len(audit.CORE)} core facts (price, materials, returns, shipping, '
                     f'payment methods, guarantee), {len(on_file)} are in the brain and {len(on_page)} sit on a facts page '
                     f'an engine can cite.', len(on_page), 'n', of=len(audit.CORE), window='brain as of ' + ends_on.isoformat(),
                     tone='bad' if len(on_page) < len(audit.CORE) else 'good')
    if sessions is None:
        ai = _unavail('AI referral sessions, 28 days', 'Sessions whose source is ChatGPT, Perplexity, Gemini, Copilot or '
                      'another AI engine.', 'n', 'the sessions table has no AI engine source yet', 'ga4')
    else:
        ai = _tile('AI referral sessions, 28 days', 'Sessions whose source is an AI engine, against the median of the 4 '
                   '28-day windows before.', sessions[0], 'n', window='28d to ' + ends_on.isoformat())
    return {'answered': answer, 'core': core, 'ai_sessions': ai}


# ---------------------------------------------------------------- tables

def engines():
    """One row per engine in the set. Every rate is unavailable until the prompt set runs."""
    return [{'engine': e, **{m: None for m in ENGINE_METRICS}, 'last_run': None,
             'unavailable_reason': 'the prompt set has not run on this engine', 'fix': LOG_FIX} for e in audit.ENGINES]


def fact_table(br, facts):
    """One row per fact category: records on file, the pages they come from, and whether a facts page holds them."""
    if br is None:
        return []
    pages = set(audit.facts_pages(br))
    out = []
    for cat, spec in audit.FACTS.items():
        recs = facts.get(cat, [])
        src = sorted({r['page'] for r in recs if r['page']})
        out.append({'fact': spec['label'], 'category': cat, 'core': cat in audit.CORE, 'records': len(recs),
                    'record_ids': [r['id'] for r in recs], 'pages': src,
                    'status': 'missing' if not recs else 'on a facts page' if any(p in pages for p in src)
                    else 'on file, not on a facts page'})
    return out


# ---------------------------------------------------------------- insights

def insights(br, cov, brand):
    """The rules behind the insight cards. Each returns the sentence it produces and its capability."""
    out = []
    rule = 'sample buyer prompts that need a fact category with no brain record holding a value'
    if br is None:
        out.append({'id': 'unanswered_prompts', 'severity': 'info', 'capability': None, 'autonomy': None,
                    'sentence': 'The brand brain is not built, so no buyer prompt can be checked.', 'rule': rule})
    else:
        miss = [p for p in cov if not p['answerable']]
        cats = []
        for p in miss:
            cats += [c for c in p['missing'] if c not in cats]
        if miss:
            out.append({'id': 'unanswered_prompts', 'severity': 'medium', 'capability': 'ORG-C35', 'autonomy': 'human_assist',
                        'sentence': f'{len(miss)} of {len(cov)} sample buyer prompts need a fact the brain does not hold: '
                                    f'{", ".join(audit.FACTS[c]["label"] for c in cats)}.', 'rule': rule})
        else:
            out.append({'id': 'unanswered_prompts', 'severity': 'info', 'capability': None, 'autonomy': None,
                        'sentence': f'The brain holds a fact for every one of the {len(cov)} sample prompts.', 'rule': rule})
    rule = 'the brain records an agent shopping endpoint, and no agentic listing check is on file'
    rec = br.get(f'{brand}.stack.agent_commerce_endpoint') if br else None
    if rec is None or rec.get('value') is None:
        out.append({'id': 'agent_endpoint_unchecked', 'severity': 'info', 'capability': None, 'autonomy': None,
                    'sentence': 'No agent shopping endpoint is on file for this brand.', 'rule': rule})
    else:
        out.append({'id': 'agent_endpoint_unchecked', 'severity': 'high', 'capability': 'PROD-C47', 'autonomy': 'founder_gate',
                    'sentence': 'The site publishes an endpoint for AI shopping agents. No check has confirmed the price, '
                                'stock and delivery date it gives a buyer.', 'rule': rule, 'brain_ref': rec['id']})
    return out


# ---------------------------------------------------------------- chart

def chart(br, cov):
    """One-star mentions per objection ladder theme, split by whether every linked sample prompt is answerable."""
    lads = audit.ladder_counts(br)
    if not lads:
        return {'unavailable': True, 'reason': 'no objection ladders in the brand brain', 'fix': 'brain'}
    labels, ok, gap = [], [], []
    for theme in sorted(lads, key=lambda t: -(lads[t]['one_star'] or 0)):
        linked = [p for p in cov if p['ladder'] == theme]
        n = lads[theme]['one_star']
        answered = bool(linked) and all(p['answerable'] for p in linked)
        labels.append(theme.split('_')[0])  # short axis label; the full theme is in `themes`
        ok.append(n if answered else None)
        gap.append(None if answered else n)
    return {'labels': labels, 'themes': sorted(lads, key=lambda t: -(lads[t]['one_star'] or 0)), 'series': [{'name': 'Brain can answer', 'values': ok},
                                         {'name': 'A fact is missing, or no prompt yet', 'values': gap}],
            'window': 'public reviews at ladder build', 'unit': 'n'}


# ---------------------------------------------------------------- overview

def overview(brand):
    data = audit.brand_data(brand)
    ends_on = audit.last_full_day(data)
    b = data.brand
    head = {'brand': b.get('brand'), 'name': b.get('name'), 'as_of': b.get('as_of'),
            'simulated': bool(b.get('simulated') or b.get('fictional')), 'market': b.get('market')}
    br = audit.brain(brand, today=ends_on)
    cov = audit.prompt_coverage(br) if br else []
    facts = audit.fact_records(br) if br else {}
    sessions = audit.ai_sessions(data, ends_on)
    findings = audit.run(brand, {'ends_on': ends_on.isoformat()}, data=data)
    fx = audit.prompts()
    return {'brand': head, 'window': {'ends_on': ends_on.isoformat()},
            'tiles': tiles(br, cov, facts, sessions, ends_on), 'engines': engines(), 'facts': fact_table(br, facts),
            'prompts': {'note': fx['note'], 'rows': cov}, 'insights': insights(br, cov, brand),
            'chart': chart(br, cov), 'findings': findings, 'rules': audit.RULES}


def _brand(req):
    brand = req.arg('brand', DEFAULT_BRAND) or DEFAULT_BRAND
    if not re.fullmatch(r'[a-z0-9-]{1,40}', brand):
        raise ValueError('brand must be a folder name like bombas')
    return brand


def handle(req):
    if req.method != 'GET':
        return 405, {'error': 'read only'}
    try:
        brand = _brand(req)
        audit.brand_data(brand)  # ValueError for an unknown brand
        if req.path == ['overview']:
            return overview(brand)
        if req.path == ['findings']:
            return {'findings': audit.run(brand), 'rules': audit.RULES}
    except ValueError as exc:
        return 400, {'error': str(exc)}
    return 404, {'error': 'not found', 'routes': ['overview', 'findings']}
