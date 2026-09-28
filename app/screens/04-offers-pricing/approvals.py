"""Approvals for screen 04: a move saved to the brand brain as a plan record, and a proposed registry row for it.

The brain is written only through app/brain/store.py `Brain.put`, never by hand:
  mode 'proposed'  status proposed, tier inferred, source type agent with derived_from = the finding ids.
                   It lands in the brand brain review queue; the founder accepts or ignores it there.
  mode 'founder'   status active, tier approved, source type founder. The founder approved it on this screen.

The experiment registry has no shared table yet (app/contracts/events.md), so the proposed row goes to this
screen's outbox, `outbox/registry.<brand>.json`, in the events.md shape with status proposed. The experiments
screen owns ids, results and decisions; this screen only proposes. Contract ask in FEATURES.md.
"""
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parents[1]
SCREEN = '04-offers-pricing'
OUTBOX = HERE / 'outbox'
MODES = ('proposed', 'founder')
OFFER_KINDS = ('offer', 'price_change', 'landing_page')   # an approved move of these kinds is a new offer in the brain
TEST_KINDS = ('test_brief', 'price_change', 'ad_brief', 'page_section', 'offer', 'landing_page', 'flow', 'listing_fix')


def _store():
    path = str(APP / 'brain')
    if path not in sys.path:
        sys.path.insert(0, path)
    import store  # noqa: WPS433  (app/brain/store.py, the only writer of brain records)
    return store


def field_for(action):
    """A stable brain field name for a move: offer_ plus the rule and entity, a-z0-9_ only, short."""
    tail = action['id'].split('.', 1)[-1].lower()
    slug = re.sub(r'[^a-z0-9]+', '_', tail).strip('_')
    slug = slug[len('offer_'):] if slug.startswith('offer_') else slug
    if len(slug) > 48:
        slug = slug[:40] + '_' + hashlib.sha1(tail.encode()).hexdigest()[:6]
    return 'offer_' + slug


def plan_record(brand, action, mode, today):
    if mode not in MODES:
        raise ValueError('mode must be proposed or founder')
    field = field_for(action)
    ent = action.get('entity') or {}
    window = ent.get('id', '')[len('window_'):] if str(ent.get('id', '')).startswith('window_') else None
    value = {'screen': SCREEN, 'move_id': action['id'], 'rule_id': action.get('rule_id'), 'title': action['title'],
             'owner': action.get('owner'), 'artefact_kind': (action.get('artefact') or {}).get('kind'),
             'artefact_label': (action.get('artefact') or {}).get('label'), 'draft': (action.get('artefact') or {}).get('draft'),
             'steps': [s['text'] for s in action.get('steps') or []], 'win_rule': action.get('win_rule'),
             'stop_rule': action.get('stop_rule'), 'check_on': action.get('check_on'),
             'finding_ids': action.get('finding_ids') or [], 'approved_on': today.isoformat() if mode == 'founder' else None}
    if window:
        value['window'] = window   # OFFER-R11 reads plans by window
    rec = {'id': f'{brand}.plans.{field}', 'brand': brand, 'section': 'plans', 'field': field, 'value': value,
           'text': f'Planned move from Offers and pricing: {action["title"]}', 'added_by': SCREEN,
           'confidence': action.get('confidence') if isinstance(action.get('confidence'), (int, float)) else None}
    if rec['confidence'] is None:
        rec.pop('confidence')
    if mode == 'founder':
        rec.update(status='active', tier='approved',
                   source={'type': 'founder', 'ref': f'approved on {SCREEN}', 'captured_at': today.isoformat()})
    else:
        rec.update(status='proposed', tier='inferred',
                   source={'type': 'agent', 'ref': f'{SCREEN} rank', 'captured_at': today.isoformat(),
                           'derived_from': list(action.get('finding_ids') or []) + list(action.get('brain_refs') or [])[:6]})
    return rec


def registry_row(brand, action, rec, surfaces, today=None):
    """A proposed registry row in the events.md shape. The experiments screen assigns the EXP id later."""
    art = action.get('artefact') or {}
    today = today or dt.date.today()
    return {'id': 'PROP-04-' + hashlib.sha1(action['id'].encode()).hexdigest()[:8], 'brand': brand,
            'hypothesis': action['title'] + '. ' + (action.get('win_rule') or ''),
            'source': {'type': 'finding', 'ref': (action.get('finding_ids') or [action['id']])[0], 'index': None},
            'idea_id': None, 'owner': 'founder',
            # web pass 2 (Intelligems): judge offer, price and shipping tests on profit per visitor, not conversion or AOV
            'metric': {'name': 'profit_per_visitor', 'direction': 'up', 'min_days': 28, 'registered_on': today.isoformat(),
                       'reason': 'revenue minus promo cost, landed cost and shipping, over visitors, per arm'},
            'variant': {'control': 'today', 'treatment': art.get('label')}, 'audience': list(surfaces or []),
            'start': None, 'read_point': action.get('check_on'), 'end': None, 'status': 'proposed', 'result': None,
            'decision': None, 'learnings_ref': None, 'retro': None, 'park': None,
            'brain_refs': [rec['id']] + list(action.get('brain_refs') or [])[:6], 'proposed_by': SCREEN}


def offer_record(brand, action, plan_id, today, launched=False):
    """The offer as the brain's offers section will hold it. Proposed while planned, so no screen reads it as
    live; active from the day it launches (valid_from). The terms are the first lines of the drafted spec."""
    field = field_for(action).replace('offer_', 'planned_', 1)
    draft = (action.get('artefact') or {}).get('draft') or ''
    terms = ' '.join(draft.splitlines()[:3])[:400]
    rec = {'id': f'{brand}.offers.{field}', 'brand': brand, 'section': 'offers', 'field': field,
           'value': {'state': 'live' if launched else 'planned', 'plan': plan_id, 'kind': (action.get('artefact') or {}).get('kind'),
                     'label': (action.get('artefact') or {}).get('label'), 'terms': terms, 'stop_rule': action.get('stop_rule')},
           'text': ('Live offer: ' if launched else 'Planned offer: ') + (action.get('artefact') or {}).get('label', action['title']),
           'added_by': SCREEN, 'tier': 'approved',
           'source': {'type': 'founder', 'ref': f'approved on {SCREEN}', 'captured_at': today.isoformat()},
           'status': 'active' if launched else 'proposed'}
    if launched:
        rec['valid_from'] = today.isoformat()
    return rec


def launch(brand, action, brain_root=None, today=None):
    """Mark an approved offer live: the offers record turns active with valid_from today. Needs the founder plan."""
    today = today or dt.date.today()
    store = _store()
    brain = store.Brain(brand, brain_root, today) if brain_root else store.Brain(brand, today=today)
    plan_id = f'{brand}.plans.{field_for(action)}'
    plan = next((r for r in brain.raw('plans') if r['id'] == plan_id), None)
    if not plan or plan.get('status') != 'active':
        return {'record': None, 'errors': ['approve the move as the founder before it can launch']}
    rec = offer_record(brand, action, plan_id, today, launched=True)
    errs = brain.put(rec)
    return {'record': rec['id'], 'status': rec['status'], 'errors': errs}


def outbox_rows(brand, outbox=OUTBOX):
    path = Path(outbox) / f'registry.{brand}.json'
    if not path.is_file():
        return []
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except ValueError:
        return []


def save(brand, action, mode='proposed', surfaces=None, brain_root=None, outbox=OUTBOX, today=None):
    """Write the plan record through Brain.put and, for a testable move, the proposed registry row.
    Returns {record, errors, registry}. Nothing is written when the record fails validation."""
    today = today or dt.date.today()
    store = _store()
    brain = store.Brain(brand, brain_root, today) if brain_root else store.Brain(brand, today=today)
    rec = plan_record(brand, action, mode, today)
    errs = brain.put(rec)
    if errs:
        return {'record': rec['id'], 'errors': errs, 'registry': None}
    offer_id = None
    if mode == 'founder' and (action.get('artefact') or {}).get('kind') in OFFER_KINDS:
        orec = offer_record(brand, action, rec['id'], today)
        oerrs = brain.put(orec)
        if oerrs:
            return {'record': rec['id'], 'errors': oerrs, 'registry': None}
        offer_id = orec['id']
    row = None
    if (action.get('artefact') or {}).get('kind') in TEST_KINDS:
        row = registry_row(brand, action, rec, surfaces, today)
        rows = [r for r in outbox_rows(brand, outbox) if r.get('id') != row['id']] + [row]
        Path(outbox).mkdir(parents=True, exist_ok=True)
        (Path(outbox) / f'registry.{brand}.json').write_text(json.dumps(rows, indent=1), encoding='utf-8')
    return {'record': rec['id'], 'status': rec['status'], 'errors': [], 'registry': row['id'] if row else None, 'offer': offer_id}


def planned(rd):
    """Move ids that already have a plan record in the brain, with the record id and status."""
    out = {}
    brain = getattr(rd, '_brain', None)
    recs = brain.records('plans', include_retired=True) if brain else []
    for rec in recs:
        if rec.get('status') == 'retired':
            continue
        v = rec.get('value')
        if isinstance(v, dict) and v.get('move_id'):
            out[v['move_id']] = {'record': rec['id'], 'status': rec.get('status'), 'tier': rec.get('tier')}
    return out


# Who receives an approved brief on the shared hand-offs table (events.md), by artefact kind. A test goes to the
# experiments screen; store settings and offer terms go to the person who runs the store admin.
HANDOFF_TO = {'page_section': 'landing pages', 'landing_page': 'landing pages', 'ad_brief': 'creative', 'creative': 'creative',
              'copy': 'copy', 'email': 'email', 'flow': 'email', 'listing_fix': 'marketplaces', 'test_brief': '25-experiments',
              'report': '25-experiments', 'offer': 'store admin', 'price_change': 'store admin', 'policy': 'store admin',
              'research_note': 'founder'}


def file_text(pf):
    """A move's build file as a titled CSV block, or None."""
    if not pf or not pf.get('rows'):
        return None
    cols = list(pf['rows'][0])
    rows = [','.join(cols)] + [','.join(str(r.get(c, '')).replace(',', ' ') for c in cols) for r in pf['rows']]
    return f'File {pf["name"]} ({pf.get("note", "")}):\n' + '\n'.join(rows)


def handoff_row(action):
    """The hand-off row for an approved move, in the events.md shape; the page posts it to /api/handoffs once."""
    art = action.get('artefact') or {}
    to = HANDOFF_TO.get(art.get('kind'))
    if not to:
        return None
    draft = art.get('draft') or ''
    ft = file_text(action.get('price_file'))
    if ft:   # the build file travels with the brief, as CSV text
        draft = (draft + '\n\n' + ft)[:20000]
    return {'from_screen': SCREEN, 'to': to, 'kind': art['kind'], 'title': action['title'], 'why': action.get('why'),
            'draft': draft or None, 'win_rule': action.get('win_rule'), 'stop_rule': action.get('stop_rule'),
            'check_on': action.get('check_on'), 'capability': (action.get('capability') or {}).get('id'),
            'owner': action.get('owner'), 'finding_id': action['id'], 'status': 'decided'}
