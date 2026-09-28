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


def registry_row(brand, action, rec, surfaces):
    """A proposed registry row in the events.md shape. The experiments screen assigns the EXP id later."""
    art = action.get('artefact') or {}
    return {'id': 'PROP-04-' + hashlib.sha1(action['id'].encode()).hexdigest()[:8], 'brand': brand,
            'hypothesis': action['title'] + '. ' + (action.get('win_rule') or ''),
            'source': {'type': 'finding', 'ref': (action.get('finding_ids') or [action['id']])[0], 'index': None},
            'idea_id': None, 'owner': 'founder', 'metric': None,
            'variant': {'control': 'today', 'treatment': art.get('label')}, 'audience': list(surfaces or []),
            'start': None, 'read_point': action.get('check_on'), 'end': None, 'status': 'proposed', 'result': None,
            'decision': None, 'learnings_ref': None, 'retro': None, 'park': None,
            'brain_refs': [rec['id']] + list(action.get('brain_refs') or [])[:6], 'proposed_by': SCREEN}


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
    row = None
    if (action.get('artefact') or {}).get('kind') in TEST_KINDS:
        row = registry_row(brand, action, rec, surfaces)
        rows = [r for r in outbox_rows(brand, outbox) if r.get('id') != row['id']] + [row]
        Path(outbox).mkdir(parents=True, exist_ok=True)
        (Path(outbox) / f'registry.{brand}.json').write_text(json.dumps(rows, indent=1), encoding='utf-8')
    return {'record': rec['id'], 'status': rec['status'], 'errors': [], 'registry': row['id'] if row else None}


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
