"""Setup screen api: the onboarding flow (PRODUCT-PLAN section 5.1).

Five steps, all local, all mock. No network, no paid calls, no external writes.

  GET  /api/setup/state?brand=bombas        everything the page needs in one call
  POST /api/setup/crawl      {url}          mock crawl: the BRAIN.md sections table
  POST /api/setup/documents  {file, note, sections, visibility}
                                            one line in app/brain/<brand>/documents/manifest.json
  POST /api/setup/connect    {category, choice, source}
                                            choice connect, skip or declined, saved to
                                            app/brain/<brand>/connections.json
  POST /api/setup/finance    {field, scope, scope_key, value, effective_from, note, confidence}
                                            one row in app/data/brands/<brand>/finance_inputs.json
  GET  /api/setup/audit                     keeper gaps plus the top 5 questions
  POST /api/setup/answer     {question_id, answer}
                                            the answer becomes a founder record via store.py

The brand comes from `?brand=` (default bombas) and must have a brain folder.
BRAIN_ROOT, DATA_ROOT and CONTRACTS are module constants so tests can point
them at a temporary copy.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import sys
import threading
from pathlib import Path
from urllib.parse import urlparse

APP = Path(__file__).resolve().parents[2]
BRAIN_ROOT = APP / 'brain'
DATA_ROOT = APP / 'data' / 'brands'
CONTRACTS = APP / 'contracts'
DEFAULT_BRAND = 'bombas'

if str(APP / 'brain') not in sys.path:
    sys.path.insert(0, str(APP / 'brain'))
import keeper  # noqa: E402
import store  # noqa: E402

SAFE_BRAND = re.compile(r'^[a-z0-9_-]{2,40}$')
SAFE_DOC = re.compile(r'^[A-Za-z0-9 _.()-]{1,120}$')
CHOICES = ('connect', 'skip', 'declined')
CONFIDENCE = ('invoice', 'estimate')
APPROVED_SECTIONS = ('claims', 'decisions')
_lock = threading.Lock()


def today() -> dt.date:
    return dt.date.today()


# ---------------------------------------------------------------- files

def _read_json(path: Path, default):
    if not path.is_file():
        return default
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return default


def _write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    tmp.replace(path)


def brand_of(req) -> str:
    brand = (req.arg('brand') if hasattr(req, 'arg') else None) or DEFAULT_BRAND
    if not SAFE_BRAND.match(brand) or not (BRAIN_ROOT / brand).is_dir():
        raise ValueError('no brain folder for that brand')
    return brand


# ---------------------------------------------------------------- 1. website

def sections_table(brand: str) -> dict:
    """Rows of the Sections table in BRAIN.md, plus the empty-section line."""
    path = BRAIN_ROOT / brand / 'BRAIN.md'
    out = {'rows': [], 'empty': [], 'brain_md': path.is_file()}
    if not path.is_file():
        return out
    in_table = False
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.startswith('## '):
            in_table = line.strip() == '## Sections'
            continue
        if not in_table:
            continue
        if line.startswith('No records yet:'):
            out['empty'] = [s.strip(' .') for s in line.split(':', 1)[1].split(',') if s.strip(' .')]
        if not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) < 4 or cells[0] == 'Section' or set(cells[0]) <= set('-: '):
            continue
        m = re.match(r'\[([a-z_]+)\]', cells[0])
        name = m.group(1) if m else cells[0]
        count = int(cells[1]) if cells[1].isdigit() else None
        last = cells[2] if re.match(r'\d{4}-\d{2}-\d{2}$', cells[2]) else None
        out['rows'].append({'section': name, 'records': count, 'last_update': last, 'gist': cells[3]})
    return out


def crawl(brand: str, url: str) -> dict:
    host = urlparse(url if '://' in url else 'https://' + url).hostname or ''
    if not host or '.' not in host:
        raise ValueError('enter a website like bombas.com')
    table = sections_table(brand)
    state = _read_json(BRAIN_ROOT / brand / 'connections.json', {})
    state.setdefault('brand', brand)
    state['website'] = {'url': host, 'entered_at': today().isoformat(), 'mode': 'mock'}
    _write_json(BRAIN_ROOT / brand / 'connections.json', state)
    return {'url': host, 'mode': 'mock', 'demo_brand': brand,
            'matches_brand': brand in host.replace('-', ''),
            'records': sum(r['records'] or 0 for r in table['rows']),
            'sections': table}


# ---------------------------------------------------------------- 2. documents

def manifest_path(brand: str) -> Path:
    return BRAIN_ROOT / brand / 'documents' / 'manifest.json'


def add_document(brand: str, body: dict) -> dict:
    name = str(body.get('file') or '').strip().split('/')[-1].split('\\')[-1]
    if not SAFE_DOC.match(name) or name.startswith('.'):
        raise ValueError('file name must be plain letters, digits, spaces, dots or dashes')
    line = {'file': 'documents/' + name, 'added_at': today().isoformat(), 'added_by': 'founder'}
    note = str(body.get('note') or '').strip()[:500]
    if note:
        line['note'] = note
    sections = [s for s in (body.get('sections') or []) if s in store.SECTIONS]
    if sections:
        line['sections'] = sections
    line['visibility'] = 'public' if body.get('visibility') == 'public' else 'private'
    line['extracted'] = False
    with _lock:
        rows = _read_json(manifest_path(brand), [])
        rows = rows if isinstance(rows, list) else []
        rows.append(line)
        _write_json(manifest_path(brand), rows)
    return line


# ---------------------------------------------------------------- 3. sources

def connections(brand: str) -> dict:
    state = _read_json(BRAIN_ROOT / brand / 'connections.json', {})
    state.setdefault('brand', brand)
    state.setdefault('mode', 'mock')
    state.setdefault('choices', {})
    return state


def connected_and_declined(brand: str, registry: dict) -> tuple[list[str], list[str]]:
    """Connected source ids, and every source id in a category marked not comfortable."""
    choices = connections(brand)['choices']
    connected = sorted(c['source'] for c in choices.values() if c.get('choice') == 'connect' and c.get('source'))
    declined_cats = {cat for cat, c in choices.items() if c.get('choice') == 'declined'}
    declined = sorted(s for s, v in registry.items() if v['category'] in declined_cats)
    return connected, declined


def source_categories(brand: str) -> list[dict]:
    """Registry grouped by category, with what each source unlocks and the saved choice."""
    registry = keeper.load_registry()
    bank = keeper.load_bank()
    rooms_by_source: dict[str, set] = {}
    for q in bank:
        for s in q['answerable_by']:
            rooms_by_source.setdefault(s, set()).update(q['unblocks_rooms'])
    choices = connections(brand)['choices']
    cats: dict[str, dict] = {}
    for sid, s in registry.items():
        cat = cats.setdefault(s['category'], {'category': s['category'], 'sources': [],
                                               'public': s['access'] == 'public'})
        cat['sources'].append({'id': sid, 'name': s['name'], 'note': s.get('note', ''),
                               'sections': s.get('fills_sections', []), 'tables': s.get('fills_tables', []),
                               'rooms': sorted(rooms_by_source.get(sid, ())), 'mock': bool(s.get('mock', True))})
    out = []
    for cat in cats.values():
        cat['sections'] = sorted({x for s in cat['sources'] for x in s['sections']})
        cat['rooms'] = sorted({x for s in cat['sources'] for x in s['rooms']})
        cat['choice'] = choices.get(cat['category'])
        out.append(cat)
    out.sort(key=lambda c: (c['public'], -len(c['rooms']), c['category']))
    return out


def set_connection(brand: str, body: dict) -> dict:
    registry = keeper.load_registry()
    category = str(body.get('category') or '')
    choice = str(body.get('choice') or '')
    source = body.get('source') or None
    cats = {s['category'] for s in registry.values() if s['access'] != 'public'}
    if category not in cats:
        raise ValueError('unknown or public category')
    if choice not in CHOICES:
        raise ValueError('choice must be connect, skip or declined')
    if choice == 'connect':
        if source not in registry or registry[source]['category'] != category:
            raise ValueError('pick a source from that category')
    else:
        source = None
    with _lock:
        state = connections(brand)
        state['choices'][category] = {'choice': choice, 'source': source, 'mode': 'mock',
                                      'at': today().isoformat()}
        state['updated_at'] = today().isoformat()
        _write_json(BRAIN_ROOT / brand / 'connections.json', state)
    return state['choices'][category]


# ---------------------------------------------------------------- 4. finance inputs

def _md_table(text: str, heading: str) -> list[list[str]]:
    rows, on = [], False
    for line in text.splitlines():
        if line.startswith('## '):
            on = line.strip() == heading
            continue
        if on and line.startswith('|'):
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if set(cells[0]) <= set('-: ') or cells[0] in ('Field', 'Metric'):
                continue
            rows.append(cells)
    return rows


def finance_contract() -> dict:
    text = (CONTRACTS / 'finance-inputs.md').read_text(encoding='utf-8')
    fields = [{'field': c[0], 'scope': [s.strip() for s in c[1].replace(' or ', ',').split(',') if s.strip()],
               'unit': c[2], 'what': c[3]} for c in _md_table(text, '## Fields') if len(c) >= 4]
    ids = {f['field'] for f in fields}
    metrics = []
    for c in _md_table(text, '## Metrics unlocked'):
        if len(c) < 3:
            continue
        needs = [t for t in re.findall(r'[a-z_]+', c[1]) if t in ids]
        if 'all of the above' in c[1]:
            # Marketplace fees only apply to marketplace orders, so they never block the total.
            prior = [n for m in metrics for n in m['needs'] if not n.startswith('marketplace_')]
            needs = list(dict.fromkeys(prior + needs))
        metrics.append({'metric': c[0], 'needs': needs, 'needs_text': c[1], 'how': c[2]})
    return {'fields': fields, 'metrics': metrics}


def finance_path(brand: str) -> Path:
    return DATA_ROOT / brand / 'finance_inputs.json'


def finance_rows(brand: str) -> tuple[dict, list[dict]]:
    doc = _read_json(finance_path(brand), None)
    if isinstance(doc, list):
        return {'table': 'finance_inputs', 'brand': brand}, doc
    if not isinstance(doc, dict):
        return {'table': 'finance_inputs', 'brand': brand}, []
    return doc, list(doc.get('rows') or [])


def finance_summary(brand: str) -> dict:
    contract = finance_contract()
    doc, rows = finance_rows(brand)
    on = today().isoformat()
    by_field: dict[str, dict] = {}
    for r in rows:
        f = by_field.setdefault(r.get('field'), {'rows': 0, 'in_force': 0, 'simulated': 0, 'latest': None})
        f['rows'] += 1
        if r.get('confidence') == 'simulated':
            f['simulated'] += 1
        if (r.get('effective_from') or '') <= on and (not r.get('effective_to') or r['effective_to'] >= on):
            f['in_force'] += 1
            if f['latest'] is None or (r.get('effective_from') or '') >= (f['latest'].get('effective_from') or ''):
                f['latest'] = {k: r.get(k) for k in ('value', 'unit', 'scope', 'scope_key', 'effective_from', 'confidence')}
    fields = [dict(f, **by_field.get(f['field'], {'rows': 0, 'in_force': 0, 'simulated': 0, 'latest': None}))
              for f in contract['fields']]
    have = {f['field'] for f in fields if f['in_force']}
    metrics = []
    for m in contract['metrics']:
        missing = [n for n in m['needs'] if n not in have]
        metrics.append(dict(m, missing=missing, available=bool(m['needs']) and not missing))
    return {'fields': fields, 'metrics': metrics, 'rows': len(rows),
            'note': doc.get('note'), 'confidence': doc.get('confidence')}


def add_finance_row(brand: str, body: dict) -> dict:
    contract = {f['field']: f for f in finance_contract()['fields']}
    field = str(body.get('field') or '')
    if field not in contract:
        raise ValueError('unknown field')
    spec = contract[field]
    scope = str(body.get('scope') or spec['scope'][0])
    if scope not in spec['scope']:
        raise ValueError('scope for ' + field + ' must be ' + ' or '.join(spec['scope']))
    scope_key = str(body.get('scope_key') or '').strip()[:80]
    if scope != 'global' and not scope_key:
        raise ValueError('name the ' + scope + ' this applies to')
    if scope == 'global':
        scope_key = ''
    try:
        value = float(body.get('value'))
    except (TypeError, ValueError):
        raise ValueError('value must be a number')
    if value != value or value < 0:
        raise ValueError('value must be zero or more')
    start = str(body.get('effective_from') or '')
    try:
        dt.date.fromisoformat(start)
    except ValueError:
        raise ValueError('effective_from must be a date like 2026-09-01')
    confidence = body.get('confidence') if body.get('confidence') in CONFIDENCE else 'estimate'
    row = {'field': field, 'scope': scope, 'scope_key': scope_key, 'value': value, 'unit': spec['unit'],
           'effective_from': start, 'effective_to': None, 'entered_by': 'founder',
           'entered_at': today().isoformat(), 'note': str(body.get('note') or '').strip()[:300],
           'confidence': confidence}
    with _lock:
        doc, rows = finance_rows(brand)
        same = [r for r in rows if r.get('field') == field and (r.get('scope_key') or '') == scope_key]
        if any((r.get('effective_from') or '') >= start for r in same):
            raise ValueError('a row for this field already starts on or after ' + start + '; pick a later date')
        # A change is a new row: the open row before it ends the day before, its value untouched.
        end = (dt.date.fromisoformat(start) - dt.timedelta(days=1)).isoformat()
        for r in same:
            if not r.get('effective_to') or r['effective_to'] >= start:
                r['effective_to'] = end
        rows.append(row)
        doc['rows'] = rows
        if 'rows_count' in doc:
            doc['rows_count'] = len(rows)
        _write_json(finance_path(brand), doc)
    return row


# ---------------------------------------------------------------- 5. first audit

def audit(brand: str) -> dict:
    brain = store.Brain(brand, root=BRAIN_ROOT, today=today())
    registry = keeper.load_registry()
    connected, declined = connected_and_declined(brand, registry)
    gap_list = keeper.gaps(brain)
    counts: dict[str, int] = {}
    for g in gap_list:
        counts[g['kind']] = counts.get(g['kind'], 0) + 1
    questions = keeper.ask(brain, connected, declined, n=5, registry=registry)
    return {'connected': connected, 'declined': declined, 'gaps': counts, 'gap_total': len(gap_list),
            'questions': questions, 'version': brain.version()}


def _slug(text: str) -> str:
    return re.sub(r'[^a-z0-9_]+', '_', text.lower()).strip('_')[:60] or 'answer'


def answer(brand: str, body: dict) -> dict:
    qid = str(body.get('question_id') or '')
    text = str(body.get('answer') or '').strip()
    if not text:
        raise ValueError('write an answer first')
    if len(text) > 2000:
        raise ValueError('keep the answer under 2,000 characters')
    q = next((q for q in keeper.load_bank() if q['id'] == qid), None)
    if q is None:
        raise ValueError('unknown question')
    brain = store.Brain(brand, root=BRAIN_ROOT, today=today())
    open_fields = [a['fills'] for a in keeper.ask(brain, n=100) if a['id'] == qid]
    target = (open_fields[0] if open_fields else q['fills'])[0]
    section, _, field = target.partition('.')
    field = field or 'founder_' + _slug(qid.split('.')[-1])
    rec = {'id': f'{brand}.{section}.{field}', 'brand': brand, 'section': section, 'field': field,
           'text': text, 'source': {'type': 'founder', 'ref': 'setup:' + qid, 'captured_at': today().isoformat()},
           'confidence': 1.0, 'status': 'active', 'visibility': 'private', 'added_by': 'founder',
           'notes': 'answered in setup: ' + q['asks']}
    if section in APPROVED_SECTIONS:
        rec['tier'] = 'approved'
    errs = brain.put(rec)
    if errs:
        raise ValueError('; '.join(errs[:3]))
    return {'record': rec, 'fills': q['fills']}


# ---------------------------------------------------------------- router

def state(brand: str) -> dict:
    conns = connections(brand)
    return {'brand': brand, 'mode': 'mock', 'simulated': True, 'today': today().isoformat(),
            'website': conns.get('website'), 'sections': sections_table(brand),
            'documents': _read_json(manifest_path(brand), []), 'section_names': store.SECTIONS,
            'categories': source_categories(brand), 'finance': finance_summary(brand)}


ROUTES = {
    ('GET', 'state'): lambda b, body: state(b),
    ('GET', 'audit'): lambda b, body: audit(b),
    ('POST', 'crawl'): lambda b, body: crawl(b, str(body.get('url') or '').strip()),
    ('POST', 'documents'): add_document,
    ('POST', 'connect'): set_connection,
    ('POST', 'finance'): add_finance_row,
    ('POST', 'answer'): answer,
}


def handle(req):
    name = req.path[0] if req.path else 'state'
    route = ROUTES.get((req.method, name))
    if route is None:
        return 404, {'error': 'not found', 'path': '/'.join(req.path)}
    try:
        brand = brand_of(req)
        body = req.body if isinstance(req.body, dict) else {}
        return route(brand, body)
    except ValueError as exc:
        return 400, {'error': str(exc)}
