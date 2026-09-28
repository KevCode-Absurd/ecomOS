"""Answer engines audit (screen 18, round 0). Findings in the shape of app/contracts/audit.md.

No engine is connected yet. There is no prompt-run log, no facts registry, no corrections log, no product
feed snapshot and no agentic listing check, so the rules that read them emit one `unavailable` finding
each, with the table and the connector named. What round 0 can read is readiness, from the brand brain
(app/brain/store.py): which facts an engine could cite, where they live, and whether they agree across the
surfaces the brain tracks. Sessions come from the data layer through app/metrics.py. No connector, no model
call. Same tables, same brain and same window give the same findings, byte for byte.

Rules (the room spec's insights are R01 to R11, in its order; R12 to R14 are the readiness reads)
  AEO-R01  Engine invents a fact: an answer states a number or claim not in the facts registry. Inputs
           ai_prompt_runs, facts_registry. Capability ORG-C36 (fix at the source, human assist).
  AEO-R02  Recommend gap: an engine mentions the brand but recommends a named competitor for the same
           prompt. Input ai_prompt_runs. Capability ORG-C34 (rewrite a page for citation, human assist).
  AEO-R03  Price drift across surfaces: for a sock line, the median per-pair price on marketplace
           listings the brain verified as the brand's (`marketplaces.amazon_asin_set_verified`, public
           capture) is 25 percent or more away from the median
           per-pair list price in the store catalog (`products`, simulated). Listings with no pack count
           in the title are left out, not guessed. An engine or a shopping assistant quotes whichever
           it reads. Money: null, no count of buyers who saw the wrong price. Capability ORG-C35
           (keep facts identical everywhere, human assist).
  AEO-R04  Correction did not land: a re-check after a shipped fix still returns the old fact. Input
           corrections_log. Capability ORG-C36.
  AEO-R05  No brand-owned citation: an engine cites zero brand-owned sources across the last audit.
           Input ai_prompt_runs.cited_sources. Capability ORG-C34.
  AEO-R06  Shopping agent gets it wrong: a spot-check returns a price or stock value that differs from
           the live feed. Inputs agentic_listing_checks, product_feed_snapshot. Capability PROD-C47
           (founder gate). Brain ref: the agent commerce endpoint record.
  AEO-R07  Sentiment slide: ai_sentiment_score for an engine falls on the prior month. Input
           ai_prompt_runs. Capability ORG-C37 (run the prompt set, agent does).
  AEO-R08  Competitor narrative shift: a named competitor's described strengths changed week on week.
           Input competitor_prompt_runs. Capability BRN-C11 (agent does).
  AEO-R09  Stale prompt set: the prompt set has not run on an engine in more than 35 days, or never.
           Input: the prompt-run log. With no log at all, every engine counts as never run, and the rule
           fires once for the brand. Capability ORG-C37 (agent does).
  AEO-R10  Rewrite backlog stalling: a priority page unrewritten for more than 4 weeks. Input
           page_rewrite_backlog. Capability ORG-C34.
  AEO-R11  Known but not recommended: mention rate over 60 percent and recommend rate under 20 percent
           for one engine. Input ai_prompt_runs. Capability ORG-C35.
  AEO-R12  Buyer prompt with no fact on file: a fact category that sample buyer prompts need
           (fixtures/prompts.json) has no brain record with a value. One finding per category. Evidence:
           the prompts that need it and the one-star counts of the objection ladders they come from.
           Money: null, no prompt run counts the lost answers. Capability ORG-C35 (publish the facts
           page, human assist).
  AEO-R13  Policy fact held only on a legal policy page: a returns, shipping, warranty or payment fact
           whose brain record comes from a /policies/ page that is not on the brand's facts page list
           (brain `site_map.facts_pages`). One finding per page. Money: null. Capability ORG-C34.
  AEO-R14  AI referrals below own median: sessions whose source is an AI engine, last 28 days, below
           the median of the 4 trailing 28-day windows. Money: (median - current) x GA4 conversion rate
           x aov, from app/metrics.py. Unavailable while the sessions table holds no AI engine source.
           Capability ORG-C37.

Owner of every rule: 18-answer-engines. Findings are sorted by severity, then stake, then id.
"""
import importlib.util
import json
import re
import sqlite3
import statistics
import sys
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parents[1]
SCREEN = '18-answer-engines'

ENGINES = ['ChatGPT', 'Gemini', 'Perplexity', 'Google AI Overviews', 'Amazon Rufus']
STALE_DAYS = 35
DRIFT_SHARE = 0.25
AI_SOURCES = ['chatgpt.com', 'chat.openai.com', 'perplexity.ai', 'gemini.google.com', 'copilot.microsoft.com',
              'claude.ai', 'meta.ai']
SEVERITY_ORDER = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}

# The core fact categories from the room spec (fact_gap_count) plus 3 the objection ladders ask for.
# Each maps to the brain records that answer it. A category with no record holding a value is a gap;
# `expected` names the record the fix would create.
CORE = ['price', 'materials', 'returns', 'shipping', 'payment_method', 'warranty']
FACTS = {
    'price': {'label': 'price', 'records': ['products.price_ladder_socks', 'products.price_ladder_underwear']},
    'materials': {'label': 'materials', 'records': ['products.materials', 'claims.ankle_socks_benefit',
                                                    'claims.calf_socks_benefit']},
    'returns': {'label': 'returns and exchanges', 'records': ['policies.returns_window_days', 'policies.refund_method',
                                                             'policies.exchanges']},
    'shipping': {'label': 'shipping cost and speed', 'records': ['policies.shipping_options']},
    'payment_method': {'label': 'payment methods', 'records': ['policies.payment_methods']},
    'warranty': {'label': 'guarantee', 'records': ['policies.happiness_guarantee', 'claims.guarantee_promise']},
    'sizing': {'label': 'the size chart', 'records': ['products.size_chart']},
    'durability': {'label': 'how long a pair lasts', 'records': ['products.wear_life']},
    'giving': {'label': 'the giving model', 'records': ['claims.donation_pledge']},
    'marketplace': {'label': 'where to buy the real product', 'records': ['marketplaces.authorized_sellers']},
}
POLICY_FACTS = ['returns', 'shipping', 'warranty', 'payment_method']

# Tables the room spec asks for. None exists in the data layer yet.
CONNECTOR = {
    'ai_prompt_runs': ('prompt-run script (ORG-C37)', 'Run the frozen prompt set on each engine once a month.'),
    'competitor_prompt_runs': ('prompt-run script, competitor slice (BRN-C11)', 'Add the weekly competitor slice.'),
    'facts_registry': ('facts registry (ORG-C35)', 'Build the facts registry: one row per fact per surface.'),
    'corrections_log': ('corrections log (ORG-C36)', 'Log each wrong fact, its fix dates and its re-checks.'),
    'product_feed_snapshot': ('merchant feed export', 'Connect the merchant feed (read only).'),
    'agentic_listing_checks': ('agentic spot-check script (PROD-C47)', 'Run the agentic listing check weekly.'),
    'page_rewrite_backlog': ('page rewrite list (ORG-C34)', 'Set the priority list of pages to rewrite.'),
}

TABLE_WORDS = {'ai_prompt_runs': 'no prompt run', 'competitor_prompt_runs': 'no competitor prompt run',
               'facts_registry': 'no facts registry', 'corrections_log': 'no corrections log',
               'product_feed_snapshot': 'no product feed', 'agentic_listing_checks': 'no agentic listing check',
               'page_rewrite_backlog': 'no page rewrite list'}

RULES = [
    {'rule_id': 'AEO-R01', 'name': 'Engine states a fact that is not in the facts registry', 'entity_type': 'brand',
     'inputs': ['ai_prompt_runs', 'facts_registry'], 'capability': 'ORG-C36', 'owner_screen': SCREEN},
    {'rule_id': 'AEO-R02', 'name': 'Engine mentions the brand but recommends a named competitor', 'entity_type': 'brand',
     'inputs': ['ai_prompt_runs'], 'capability': 'ORG-C34', 'owner_screen': SCREEN},
    {'rule_id': 'AEO-R03', 'name': 'Per-pair price on marketplace listings 25 percent or more away from the catalog',
     'entity_type': 'sku', 'inputs': ['brain.marketplaces', 'products'], 'capability': 'ORG-C35', 'owner_screen': SCREEN},
    {'rule_id': 'AEO-R04', 'name': 'Correction shipped, re-check still returns the old fact', 'entity_type': 'brand',
     'inputs': ['corrections_log'], 'capability': 'ORG-C36', 'owner_screen': SCREEN},
    {'rule_id': 'AEO-R05', 'name': 'Engine cites no brand-owned source', 'entity_type': 'brand',
     'inputs': ['ai_prompt_runs'], 'capability': 'ORG-C34', 'owner_screen': SCREEN},
    {'rule_id': 'AEO-R06', 'name': 'Shopping agent returns a price or stock value that differs from the feed',
     'entity_type': 'sku', 'inputs': ['agentic_listing_checks', 'product_feed_snapshot'], 'capability': 'PROD-C47',
     'owner_screen': SCREEN},
    {'rule_id': 'AEO-R07', 'name': 'Positive mentions fell on the prior month', 'entity_type': 'brand',
     'inputs': ['ai_prompt_runs'], 'capability': 'ORG-C37', 'owner_screen': SCREEN},
    {'rule_id': 'AEO-R08', 'name': 'A named competitor is described differently this week', 'entity_type': 'brand',
     'inputs': ['competitor_prompt_runs'], 'capability': 'BRN-C11', 'owner_screen': SCREEN},
    {'rule_id': 'AEO-R09', 'name': 'Prompt set not run on an engine in more than 35 days', 'entity_type': 'brand',
     'inputs': ['ai_prompt_runs'], 'capability': 'ORG-C37', 'owner_screen': SCREEN},
    {'rule_id': 'AEO-R10', 'name': 'Priority page not rewritten for citation after 4 weeks', 'entity_type': 'page',
     'inputs': ['page_rewrite_backlog'], 'capability': 'ORG-C34', 'owner_screen': SCREEN},
    {'rule_id': 'AEO-R11', 'name': 'Mentioned in over 60 percent of prompts, recommended in under 20 percent',
     'entity_type': 'brand', 'inputs': ['ai_prompt_runs'], 'capability': 'ORG-C35', 'owner_screen': SCREEN},
    {'rule_id': 'AEO-R12', 'name': 'A fact buyer prompts need has no record in the brand brain', 'entity_type': 'page',
     'inputs': ['fixtures/prompts.json', 'brain.policies', 'brain.products', 'brain.claims', 'brain.objection_ladders'],
     'capability': 'ORG-C35', 'owner_screen': SCREEN},
    {'rule_id': 'AEO-R13', 'name': 'A policy fact lives only on a legal policy page, not a facts page', 'entity_type': 'page',
     'inputs': ['brain.policies', 'brain.claims', 'brain.site_map'], 'capability': 'ORG-C34', 'owner_screen': SCREEN},
    {'rule_id': 'AEO-R14', 'name': 'AI engine referral sessions below the 4-window median', 'entity_type': 'metric',
     'inputs': ['sessions.session_source'], 'capability': 'ORG-C37', 'owner_screen': SCREEN},
]
CAPABILITY = {
    'AEO-R01': ('ORG-C36', 'human_assist'), 'AEO-R02': ('ORG-C34', 'human_assist'), 'AEO-R03': ('ORG-C35', 'human_assist'),
    'AEO-R04': ('ORG-C36', 'human_assist'), 'AEO-R05': ('ORG-C34', 'human_assist'), 'AEO-R06': ('PROD-C47', 'founder_gate'),
    'AEO-R07': ('ORG-C37', 'agent_does'), 'AEO-R08': ('BRN-C11', 'agent_does'), 'AEO-R09': ('ORG-C37', 'agent_does'),
    'AEO-R10': ('ORG-C34', 'human_assist'), 'AEO-R11': ('ORG-C35', 'human_assist'), 'AEO-R12': ('ORG-C35', 'human_assist'),
    'AEO-R13': ('ORG-C34', 'human_assist'), 'AEO-R14': ('ORG-C37', 'agent_does'),
}
# Severity each rule gives when it fires (and keeps when unavailable). Contract section 2: a gap with no
# money formula is medium; the room spec's "high" rules stay high because each is a wrong answer in front
# of a buyer now.
SEVERITY = {'AEO-R01': 'high', 'AEO-R02': 'high', 'AEO-R03': 'medium', 'AEO-R04': 'high', 'AEO-R05': 'medium',
            'AEO-R06': 'high', 'AEO-R07': 'medium', 'AEO-R08': 'medium', 'AEO-R09': 'medium', 'AEO-R10': 'low',
            'AEO-R11': 'medium', 'AEO-R12': 'medium', 'AEO-R13': 'medium', 'AEO-R14': 'medium'}
# Plain words for the unavailable sentence of each prompt-log rule.
WAITING = {
    'AEO-R01': 'Wrong facts from engines cannot be caught',
    'AEO-R02': 'Prompts where an engine picks a competitor cannot be found',
    'AEO-R04': 'Whether a fix changed an engine\'s answer cannot be checked',
    'AEO-R05': 'Which sources engines cite cannot be read',
    'AEO-R06': 'What a shopping agent tells a buyer about price and stock cannot be checked',
    'AEO-R07': 'The tone of engine answers cannot be tracked',
    'AEO-R08': 'Changes in how engines describe competitors cannot be seen',
    'AEO-R10': 'Stalled page rewrites cannot be counted',
    'AEO-R11': 'Mention and recommend rates cannot be compared',
}

_MODS = {}


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def metrics():
    if 'metrics' not in _MODS:
        _MODS['metrics'] = _load('ecomos_metrics_answer_engines', APP / 'metrics.py')
    return _MODS['metrics']


def brand_data(brand):
    if 'tables' not in _MODS:
        _MODS['tables'] = _load('ecomos_tables_answer_engines', APP / 'data' / 'tables.py')
    return _MODS['tables'].brand_data(brand)


def brain(brand, today=None):
    """The brand's brain store, or None when the brand has no brain folder."""
    if str(APP / 'brain') not in sys.path:
        sys.path.insert(0, str(APP / 'brain'))
    import store
    if not brand or not (APP / 'brain' / str(brand)).is_dir():
        return None
    return store.Brain(brand, today=today)


def prompts():
    return json.loads((HERE / 'fixtures' / 'prompts.json').read_text(encoding='utf-8'))


def last_full_day(data):
    return date.fromisoformat(data.brand['as_of'])


def has_table(data, name):
    try:
        rows = data.table(name)
    except (KeyError, ValueError, AttributeError):
        return False
    return bool(rows)


def _age(captured_at, ends_on):
    if not captured_at:
        return None
    return max((ends_on - date.fromisoformat(str(captured_at)[:10])).days, 0)


# ---------------------------------------------------------------- brain reads

def fact_records(br):
    """Per fact category: the brain records that hold a value, with the page each came from."""
    out = {}
    for cat, spec in FACTS.items():
        found = []
        for short in spec['records']:
            rec = br.get(f'{br.brand}.{short}') if br else None
            if rec is None or rec.get('value') in (None, '', [], {}):
                continue
            src = rec.get('source') or {}
            found.append({'id': rec['id'], 'page': src.get('ref') if str(src.get('ref', '')).startswith('http') else None,
                          'captured_at': src.get('captured_at')})
        out[cat] = found
    return out


def facts_pages(br):
    rec = br.get(f'{br.brand}.site_map.facts_pages') if br else None
    return sorted({p['url'] for p in (rec or {}).get('value') or [] if isinstance(p, dict) and p.get('url')})


def ladder_counts(br):
    """One-star count per objection ladder theme, from the brain."""
    if br is None:
        return {}
    out = {}
    for rec in br.records('objection_ladders'):
        v = rec.get('value') or {}
        out[v.get('theme')] = {'id': rec['id'], 'one_star': (v.get('counts') or {}).get('one_star'),
                               'captured_at': (rec.get('source') or {}).get('captured_at')}
    return out


def prompt_coverage(br):
    """Each sample prompt with the fact categories it needs and whether the brain holds each one."""
    facts = fact_records(br)
    rows = []
    for p in prompts()['prompts']:
        missing = [c for c in p['needs'] if not facts.get(c)]
        rows.append({'id': p['id'], 'prompt': p['prompt'], 'needs': p['needs'], 'ladder': p['ladder'],
                     'missing': missing, 'answerable': not missing,
                     'records': sorted({r['id'] for c in p['needs'] for r in facts.get(c, [])})})
    return rows


PACK = re.compile(r'(\d+)\s*-?\s*(?:pairs?|packs?|pk|pcs)\b', re.I)
LINES = [('no_show', re.compile(r'no[\s-]?show', re.I), 'No show socks'),
         ('ankle', re.compile(r'ankle', re.I), 'Ankle socks'),
         ('calf', re.compile(r'calf', re.I), 'Calf socks')]
SKIP = re.compile(r'merino|compression|running|golf|kids|gift|slipper', re.I)


def sock_line(title):
    if not title or SKIP.search(title):
        return None
    for key, rx, _ in LINES:
        if rx.search(title):
            return key
    return None


def price_surfaces(data, br):
    """Per sock line: per-pair prices in the store catalog and on marketplace listings with a pack count."""
    try:
        prods = data.table('products')
    except (KeyError, ValueError):
        prods = None
    if not prods or br is None:
        return None
    lines = {k: {'line': k, 'label': lbl, 'catalog': [], 'market': [], 'market_ids': [], 'skipped': 0, 'captured_at': None}
             for k, _, lbl in LINES}
    for p in prods:
        k = sock_line(p.get('title'))
        if k and p.get('price') is not None and p.get('items_per_unit'):
            lines[k]['catalog'].append(round(float(p['price']) / float(p['items_per_unit']), 2))
    verified = br.get(f'{br.brand}.marketplaces.amazon_asin_set_verified')
    verified = set((verified or {}).get('value') or [])
    for rec in br.records('marketplaces'):
        v = rec.get('value')
        if not isinstance(v, dict) or v.get('price_usd') is None or '_listing_' not in rec['id']:
            continue
        if v.get('asin') not in verified:
            continue
        k = sock_line(v.get('title'))
        if not k:
            continue
        m = PACK.search(v['title'])
        if not m or int(m.group(1)) < 1:
            lines[k]['skipped'] += 1
            continue
        lines[k]['market'].append(round(float(v['price_usd']) / int(m.group(1)), 2))
        lines[k]['market_ids'].append(rec['id'])
        lines[k]['captured_at'] = max(filter(None, [lines[k]['captured_at'], (rec.get('source') or {}).get('captured_at')]),
                                      default=None)
    out = []
    for g in lines.values():
        if not g['catalog'] or not g['market']:
            continue
        cat_med = round(statistics.median(g['catalog']), 2)
        mkt_med = round(statistics.median(g['market']), 2)
        g.update(catalog_median=cat_med, market_median=mkt_med, gap=round(mkt_med / cat_med - 1, 4),
                 market_ids=sorted(g['market_ids']))
        out.append(g)
    return out


# ---------------------------------------------------------------- sessions

def ai_sessions(data, ends_on):
    """AI engine referral sessions per 28-day window, newest first (5 windows), or None when the sessions
    table holds no AI engine source. Read-only GROUP BY on data.sqlite; a candidate for the metric contract."""
    path = getattr(data, 'sqlite', None)
    if not path or not Path(path).is_file():
        return None
    start = ends_on - timedelta(days=28 * 5 - 1)
    marks = ','.join('?' for _ in AI_SOURCES)
    con = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    try:
        rows = con.execute(f'SELECT date, SUM(sessions) FROM sessions WHERE session_source IN ({marks}) '
                           f'AND date BETWEEN ? AND ? GROUP BY date', [*AI_SOURCES, start.isoformat(),
                                                                       ends_on.isoformat()]).fetchall()
    finally:
        con.close()
    if not rows:
        return None
    windows = [0] * 5
    for d, n in rows:
        k = (ends_on - date.fromisoformat(str(d)[:10])).days // 28
        if 0 <= k < 5:
            windows[k] += int(n or 0)
    return windows


# ---------------------------------------------------------------- findings

def _ev(metric, value, unit, ends_on, window, baseline=None, baseline_kind=None, source='brain', simulated=False,
        freshness_days=0, **extra):
    out = {'metric': metric, 'value': value, 'unit': unit, 'window': window, 'ends_on': ends_on.isoformat(),
           'freshness_days': freshness_days, 'baseline': baseline, 'baseline_kind': baseline_kind, 'source': source,
           'simulated': simulated}
    out.update(extra)
    return out


def _finding(rule_id, entity, ends_on, evidence, sentence, confidence, brain_refs=(), stake=None, money_reason=None):
    cap, autonomy = CAPABILITY[rule_id]
    out = {'id': f'{SCREEN}.{rule_id}.{entity["id"]}', 'screen': SCREEN, 'rule_id': rule_id,
           'severity': SEVERITY[rule_id], 'entity': entity, 'evidence': evidence, 'sentence': sentence,
           'capability': {'id': cap, 'autonomy': autonomy}, 'money_at_stake': stake, 'confidence': confidence,
           'brain_refs': sorted(set(brain_refs)), 'first_seen': ends_on.isoformat(), 'last_seen': ends_on.isoformat(),
           'status': 'open', 'unavailable': None}
    if stake is None:
        out['money_reason'] = money_reason or 'no baseline'
    return out


def _unavailable(rule_id, ends_on, sentence, inputs, connector, fix, brain_refs=()):
    cap, autonomy = CAPABILITY[rule_id]
    return {'id': f'{SCREEN}.{rule_id}.brand', 'screen': SCREEN, 'rule_id': rule_id, 'severity': SEVERITY[rule_id],
            'entity': {'type': 'brand', 'id': 'brand', 'label': 'Answer engines'}, 'evidence': [],
            'sentence': sentence, 'capability': {'id': cap, 'autonomy': autonomy}, 'money_at_stake': None,
            'confidence': 0.1, 'brain_refs': sorted(set(brain_refs)),
            'first_seen': ends_on.isoformat(), 'last_seen': ends_on.isoformat(), 'status': 'unavailable',
            'unavailable': {'inputs': inputs, 'connector': connector, 'fix': fix}, 'money_reason': 'inputs unavailable'}


def log_rule_unavailable(rule_id, ends_on, data, brand):
    """The prompt-log rules: unavailable while any input table is missing."""
    inputs = next(r['inputs'] for r in RULES if r['rule_id'] == rule_id)
    missing = [t for t in inputs if not has_table(data, t)]
    if not missing:
        return None
    connector, fix = CONNECTOR[missing[0]]
    refs = [f'{brand}.stack.agent_commerce_endpoint'] if rule_id == 'AEO-R06' and brand else []
    return _unavailable(rule_id, ends_on, f'{WAITING[rule_id]}. Nothing is on file yet: {TABLE_WORDS[missing[0]]}.',
                        missing, connector, fix, refs)


def stale_findings(data, ends_on):
    if has_table(data, 'ai_prompt_runs'):
        return []  # per-engine staleness reads the log once it exists (feature round)
    ev = [_ev('days_since_last_run', None, 'days', ends_on, 'all time', STALE_DAYS, 'threshold',
              source='ai_prompt_runs', note='no run on file for any engine'),
          _ev('engines_in_set', len(ENGINES), 'count', ends_on, 'current', source='fixtures/prompts.json',
              simulated=True, engines=ENGINES)]
    return [_finding('AEO-R09', {'type': 'brand', 'id': 'brand', 'label': 'Prompt set, all engines'}, ends_on, ev,
                     f'The AI answer check has never run on any of the {len(ENGINES)} engines. '
                     f'No one has seen what they tell buyers about the brand.', 0.5,
                     money_reason='no prompt run, so no answer can be valued')]


def gap_findings(br, ends_on):
    cov = prompt_coverage(br)
    lads = ladder_counts(br)
    facts = fact_records(br)
    pages = facts_pages(br)
    out = []
    for cat, spec in FACTS.items():
        if facts.get(cat):
            continue
        need = [p for p in cov if cat in p['needs']]
        if not need:
            continue
        themes = sorted({p['ladder'] for p in need if p['ladder'] and p['ladder'] in lads})
        ev = [_ev('prompts_needing_fact', len(need), 'count', ends_on, 'sample prompt set', len(cov), 'threshold',
                  source='fixtures/prompts.json', simulated=True, prompts=[p['id'] for p in need]),
              _ev('fact_on_file', False, 'bool', ends_on, 'current', source='brain', expected_record=
                  f'{br.brand}.{spec["records"][0]}')]
        for t in themes:
            ev.append(_ev('ladder_one_star', lads[t]['one_star'], 'count', ends_on, 'at ladder build', source=lads[t]['id'],
                          freshness_days=_age(lads[t]['captured_at'], ends_on) or 0))
        page_hint = [u for u in pages if cat == 'sizing' and 'size' in u]
        one_star = sum(lads[t]['one_star'] or 0 for t in themes)
        verb = 'needs' if len(need) == 1 else 'need'
        sentence = (f'{len(need)} of {len(cov)} sample buyer prompts {verb} {spec["label"]}, and the brand brain holds '
                    f'no fact for it.')
        if page_hint:
            sentence += ' A size guide page exists, but no size values are on file.'
        elif one_star:
            sentence += f' The linked reviews carry {one_star} one-star mentions.'
        refs = [lads[t]['id'] for t in themes]
        out.append(_finding('AEO-R12', {'type': 'page', 'id': f'facts-{cat.replace("_", "-")}',
                                        'label': f'Facts page: {spec["label"]}'}, ends_on, ev, sentence, 0.5, refs,
                            money_reason='no prompt run, so lost answers cannot be counted'))
    return out


def policy_page_findings(br, ends_on):
    facts = fact_records(br)
    citable = set(facts_pages(br))
    by_page = {}
    for cat in POLICY_FACTS:
        for r in facts.get(cat, []):
            if r['page'] and '/policies/' in r['page'] and r['page'] not in citable:
                g = by_page.setdefault(r['page'], {'cats': set(), 'records': set(), 'captured_at': r['captured_at']})
                g['cats'].add(cat)
                g['records'].add(r['id'])
    out = []
    for page, g in sorted(by_page.items()):
        cats = [FACTS[c]['label'] for c in POLICY_FACTS if c in g['cats']]
        path = '/' + page.split('://', 1)[-1].split('/', 1)[-1]
        ev = [_ev('facts_on_page', len(g['records']), 'count', ends_on, 'current', source='brain', page=page,
                  freshness_days=_age(g['captured_at'], ends_on) or 0, categories=sorted(g['cats'])),
              _ev('facts_pages_listed', len(citable), 'count', ends_on, 'current', source=f'{br.brand}.site_map.facts_pages')]
        sentence = (f'The {", ".join(cats[:-1]) + " plus " + cats[-1] if len(cats) > 1 else cats[0]} facts live only '
                    f'on {path}, a legal policy page. '
                    f'None of the {len(citable)} facts pages carries them.')
        out.append(_finding('AEO-R13', {'type': 'page', 'id': path.strip('/').replace('/', '-'), 'label': path},
                            ends_on, ev, sentence, 0.5, sorted(g['records']) + [f'{br.brand}.site_map.facts_pages'],
                            money_reason='no prompt run, so lost answers cannot be counted'))
    return out


def drift_findings(lines, ends_on):
    out = []
    for g in lines:
        if abs(g['gap']) < DRIFT_SHARE:
            continue
        pct = round(abs(g['gap']) * 100)
        side = 'above' if g['gap'] > 0 else 'below'
        ev = [_ev('market_per_pair_median', g['market_median'], 'usd', ends_on, 'at capture', g['catalog_median'],
                  'threshold', source='brain.marketplaces', freshness_days=_age(g['captured_at'], ends_on) or 0,
                  listings=len(g['market']), listings_without_pack_count=g['skipped'],
                  note=f'the rule fires at {round(DRIFT_SHARE * 100)} percent from the catalog median'),
              _ev('catalog_per_pair_median', g['catalog_median'], 'usd', ends_on, 'current', source='products',
                  simulated=True, skus=len(g['catalog']))]
        sentence = (f'{g["label"]} sell for ${g["market_median"]:,.2f} a pair on Amazon listings and '
                    f'${g["catalog_median"]:,.2f} in the store catalog, {pct} percent {side}.')
        out.append(_finding('AEO-R03', {'type': 'sku', 'id': f'socks-{g["line"].replace("_", "-")}',
                                        'label': f'{g["label"]} (per pair)'}, ends_on, ev, sentence, 0.5, g['market_ids'],
                            money_reason='no count of buyers who saw the other price'))
    return out


def referral_findings(data, ends_on, brand):
    w = ai_sessions(data, ends_on)
    if w is None:
        return [_unavailable('AEO-R14', ends_on, 'No session in the data came from an AI engine, so AI referrals '
                             'read unavailable, not zero.', ['sessions.session_source'], 'GA4 (read only)',
                             'Connect GA4. AI engine sources are read from the session source.')]
    cur, base = w[0], statistics.median(w[1:])
    if cur >= base:
        return []
    kw = {'window': '28d', 'end': ends_on.isoformat(), **({'brand': brand} if brand else {})}
    fun = metrics().compute('session_funnel', data, **kw)
    aov = metrics().compute('aov', data, **kw)
    stake = None
    if not fun.get('unavailable') and not aov.get('unavailable'):
        cvr = (fun.get('rates') or {}).get('conversion_rate')
        if cvr is not None and aov.get('value') is not None:
            stake = {'usd': max(round((base - cur) * cvr * aov['value']), 0),
                     'formula': '(ai_sessions_median_4w - ai_sessions_28d) * conversion_rate * aov',
                     'inputs': {'ai_sessions_median_4w': base, 'ai_sessions_28d': cur, 'conversion_rate': cvr,
                                'aov': aov['value']}, 'window': '28d'}
    agree = sum(1 for x in w[1:] if cur < x)
    ev = [_ev('ai_sessions', cur, 'count', ends_on, '28d', base, 'own_median', source='sessions', simulated=True,
              freshness_days=1)]
    pct = round((1 - cur / base) * 100) if base else None
    return [_finding('AEO-R14', {'type': 'metric', 'id': 'ai-sessions', 'label': 'AI engine referral sessions'}, ends_on,
                     ev, f'AI engines sent {cur:,} sessions in the last 28 days. The 4-window median is {base:,.0f}, '
                     f'so this is {pct} percent lower.', 0.9 if agree >= 4 else 0.7 if agree >= 2 else 0.5, [], stake)]


def run(brand, window=None, data=None):
    """Findings for one brand and window ({ends_on, days, trailing}), sorted by severity then stake."""
    data = data if data is not None else brand_data(brand)
    ends_on = date.fromisoformat(window['ends_on']) if window and window.get('ends_on') else last_full_day(data)
    br = brain(brand, today=ends_on)
    out = []
    for rid in ('AEO-R01', 'AEO-R02', 'AEO-R04', 'AEO-R05', 'AEO-R06', 'AEO-R07', 'AEO-R08', 'AEO-R10', 'AEO-R11'):
        f = log_rule_unavailable(rid, ends_on, data, brand)
        if f:
            out.append(f)
    out += stale_findings(data, ends_on)
    if br is None:
        for rid, what in (('AEO-R03', 'marketplace listings'), ('AEO-R12', 'facts'), ('AEO-R13', 'page sources')):
            out.append(_unavailable(rid, ends_on, f'The brand brain is not built, so {what} cannot be read.',
                                    ['brain'], 'brand brain', 'Build the brand brain from public sources.'))
    else:
        lines = price_surfaces(data, br)
        if lines is None:
            out.append(_unavailable('AEO-R03', ends_on, 'The store catalog is not connected, so prices cannot be compared.',
                                    ['products'], 'shopify', 'Connect the store (read only).'))
        else:
            out += drift_findings(lines, ends_on)
        out += gap_findings(br, ends_on)
        out += policy_page_findings(br, ends_on)
    out += referral_findings(data, ends_on, brand)
    out.sort(key=lambda f: (SEVERITY_ORDER[f['severity']], -((f['money_at_stake'] or {}).get('usd') or 0), f['id']))
    return out
