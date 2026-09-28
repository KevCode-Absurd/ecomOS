"""Audit for screen 08-site-speed, in the shape of app/contracts/audit.md.

`build(data, brand)` computes everything the screen shows (api.py serves it); `run(brand, window)`
turns it into findings. Every speed number is a median from app/metrics.py (the Speed group) over the
`speed_runs` fixture; sessions, conversion and order value come from metrics.py too. No model call,
no connector, no live run: the same tables give the same output.

Fixture gap: the bombas `speed_runs` fixture puts the device in `variant` and has no run date. `SpeedData`
reads it as device = variant, variant = baseline, measured_at = the last full day, and the page says so.
Script weights come from `fixtures/script_log.json` (simulated, shaped like `speed_request_log`), joined to
the brain's stack records by id.

Rules (thresholds are rule constants, baseline_kind `threshold`):
  SPEED-R01  slow mobile pages. Fires when a measured page's median mobile LCP is over LCP_TARGET_MS
             (2,500 ms, Core Web Vitals "good"). Money: mobile sessions (28 days) x typical seconds over
             target (median of measured pages) x LOSS_PER_SECOND x cvr_overall x aov. Capability SITE-C26.
             Owner: this screen. Entity: device mobile (sessions by page are not in the data).
  SPEED-R02  heavy outside script. Fires per third-party script over SCRIPT_BUDGET_BYTES (100 KB).
             Money only when the script blocks rendering: the LCP time the fix chain gives it (transfer
             time on the lab's slow 4G, capped by what is left of the gap to target) priced like R01.
             Non-blocking scripts slow full load, not the main image, so money is null. Capability SITE-C23.
  SPEED-R03  image weight. Needs image rows in speed_request_log; the fixture holds scripts only, so it
             emits one unavailable finding until a lab run logs images. Capability SITE-C22.

LOSS_PER_SECOND is an assumption stated on the page, not a Bombas measurement: each second of LCP over
target loses that share of the orders those sessions would make. Replace it with the brand's own study.
"""
import importlib.util
import json
import re
import statistics
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parents[1]
ROOT = APP.parent
SCREEN = '08-site-speed'

LCP_TARGET_MS = 2500
TARGETS = {'fully_loaded_ms': 5000, 'lcp_ms': 2500, 'fcp_ms': 1800, 'bytes': 1_500_000, 'requests': 80}
SPEED_METRICS = ('fully_loaded_ms', 'lcp_ms', 'fcp_ms', 'bytes', 'requests')
DEVICES = ('mobile', 'desktop')
SCRIPT_BUDGET_BYTES = 100 * 1024
LAB_BYTES_PER_S = 200_000          # speed lab profile: slow 4G, 1.6 Mbps down
LOSS_PER_SECOND = 0.07             # assumption, see docstring
WINDOW = '28d'
SCRIPT_FIELDS = ('theme', 'ab_testing', 'cookie_consent', 'upsell_app', 'reviews_app', 'tag_manager',
                 'performance_vendor', 'form_security')
SEVERITY_ORDER = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
SAFE_BRAND = re.compile(r'^[a-z0-9-]{2,40}$')

RULES = [
    {'rule_id': 'SPEED-R01', 'name': 'Slow mobile pages', 'entity_type': 'device',
     'inputs': ['speed_runs', 'sessions', 'daily'], 'capability': 'SITE-C26', 'owner_screen': SCREEN},
    {'rule_id': 'SPEED-R02', 'name': 'Outside script over the weight budget', 'entity_type': 'metric',
     'inputs': ['speed_request_log', 'speed_runs', 'brain.stack'], 'capability': 'SITE-C23', 'owner_screen': SCREEN},
    {'rule_id': 'SPEED-R03', 'name': 'Images over their weight', 'entity_type': 'page',
     'inputs': ['speed_request_log'], 'capability': 'SITE-C22', 'owner_screen': SCREEN},
]

# The fix chain in shipping order. Script rows are filled from the script log; the rest need a lab run.
LATER_FIXES = [
    ('SITE-C30', 'Split the theme bundle so the page needs less code to show',
     'how much of the theme bundle the first screen needs is not measured yet'),
    ('SITE-C22', 'Cut image weight', 'the request log fixture holds scripts only, no image rows'),
    ('SITE-C26', 'Preload the main image and drop lazy loading on it', 'no LCP element captured in a lab run yet'),
    ('SITE-C24', 'Fix font loading', 'no font rows in the request log fixture'),
    ('SITE-C28', 'Cache static files and serve them from the CDN', 'no response headers captured for images and fonts'),
]


def _load(name, path):
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def metrics():
    return _load('ecomos_metrics', APP / 'metrics.py')


def tables():
    return _load('ecomos_tables', APP / 'data' / 'tables.py')


def brain(brand):
    folder = APP / 'brain' / brand
    if not folder.is_dir():
        return None
    if str(APP / 'brain') not in sys.path:
        sys.path.insert(0, str(APP / 'brain'))  # store.py imports its sibling validate.py
    return _load('ecomos_brain_store', APP / 'brain' / 'store.py').Brain(brand)


def catalogue():
    try:
        caps = json.loads((ROOT / 'agents' / 'catalogue.json').read_text())
    except (OSError, ValueError):
        return {}
    caps = caps.get('capabilities', caps) if isinstance(caps, dict) else caps
    return {c['id']: c for c in caps if str(c.get('id', '')).startswith('SITE-')}


class SpeedData:
    """The data layer with the speed_runs fixture read in the metric contract's shape (see docstring)."""

    def __init__(self, base):
        self.base, self._runs, self.adapted = base, None, False

    @property
    def brand(self):
        return self.base.brand

    def meta(self, name):
        return self.base.meta(name)

    def table(self, name):
        if name != 'speed_runs':
            return self.base.table(name)
        if self._runs is None:
            rows = self.base.table(name)
            if rows and 'device' not in rows[0] and rows[0].get('variant') in DEVICES:
                day = (self.brand or {}).get('as_of')
                rows = [dict(r, device=r['variant'], variant='baseline', measured_at=day) for r in rows]
                self.adapted = True
            self._runs = rows
        return self._runs


def page_label(path):
    if path == '/':
        return 'Home'
    kind, _, slug = path.strip('/').partition('/')
    words = slug.replace('-', ' ').title().replace(' Pack', '-Pack')
    return {'collections': 'Collection: ', 'products': 'Product: '}.get(kind, '') + words


def speed_table(sd):
    """Median of runs per page and device for each speed metric, through metrics.py."""
    m = metrics()
    try:
        rows = sd.table('speed_runs')
    except (KeyError, ValueError):
        rows = []
    pages = sorted({r['page'] for r in rows if r.get('page')}) if rows else []
    out, meta = {}, {'unavailable': True, 'reason': 'the speed_runs table is not connected', 'fix': 'speed_lab'}
    for device in DEVICES:
        for name in SPEED_METRICS:
            here = [r['page'] for r in rows if r.get('device') == device]
            if not here:
                continue
            r = m.compute(name, sd, window=WINDOW, page=here[0], device=device)
            if r['unavailable']:
                meta = {'unavailable': True, 'reason': r['reason'], 'fix': r['fix']}
                continue
            meta = {'unavailable': False, 'window': r['window'], 'freshness': r['freshness']}
            for page, value in r['by_page'].items():
                out.setdefault((page, device), {})[name] = value
    table = []
    for page in pages:
        for device in DEVICES:
            vals = out.get((page, device))
            if vals is None:
                continue
            row = {'page': page, 'label': page_label(page), 'device': device}
            row.update({k: vals.get(k) for k in SPEED_METRICS})
            row['over_lcp_target'] = row['lcp_ms'] is not None and row['lcp_ms'] > LCP_TARGET_MS
            table.append(row)
    meta['adapted'] = sd.adapted
    return table, meta


def money_inputs(base, brand):
    """Mobile sessions, cvr_overall, aov and net revenue for the window, all from metrics.py."""
    m = metrics()
    got, missing = {}, []
    for key, name, kw in (('mobile_sessions', 'sessions', {'device': 'mobile'}), ('cvr_overall', 'cvr_overall', {}),
                          ('aov', 'aov', {})):
        r = m.compute(name, base, window=WINDOW, **kw)
        if r['unavailable']:
            missing.append(f'{name}: {r["reason"]}')
            got[key] = None
        else:
            got[key] = r['value']
            if name == 'aov':
                got['net_revenue'] = (r.get('inputs') or {}).get('net_revenue')
            got['window'] = r['window']
    got['missing'] = missing
    return got


def stake(seconds, money, what):
    """Price seconds of LCP over target with the stated assumption. None when any input is missing."""
    if money['missing'] or seconds is None:
        return None
    inputs = {'mobile_sessions_28d': money['mobile_sessions'], 'seconds_over_target': round(seconds, 3),
              'loss_per_second_assumed': LOSS_PER_SECOND, 'cvr_overall': money['cvr_overall'], 'aov': money['aov']}
    usd = round(money['mobile_sessions'] * seconds * LOSS_PER_SECOND * money['cvr_overall'] * money['aov'], 2)
    return {'usd': usd, 'formula': f'mobile_sessions_28d x {what} x loss_per_second_assumed x cvr_overall x aov',
            'inputs': inputs, 'window': WINDOW}


def scripts(brand, sd_brand):
    """Script inventory: the brain's stack records joined to the script log fixture by record id."""
    b = brain(brand)
    records = [r for r in (b.records('stack') if b else []) if r.get('field') in SCRIPT_FIELDS]
    log = {}
    path = HERE / 'fixtures' / 'script_log.json'
    if path.is_file():
        f = json.loads(path.read_text())
        if f.get('brand') == brand:
            log = {r['brain_ref']: r for r in f['rows']}
    rows = []
    for rec in sorted(records, key=lambda r: SCRIPT_FIELDS.index(r['field'])):
        hit = log.get(rec['id'])
        size = hit['transfer_size'] if hit else None
        third = hit['party'] == 'third' if hit else rec['field'] != 'theme'
        rows.append({
            'name': str(rec.get('value') or rec.get('text'))[:60], 'role': rec['field'].replace('_', ' '),
            'party': 'first' if not third else 'third', 'route': hit['route'] if hit else None,
            'kb': round(size / 1024) if size is not None else None,
            'blocking': (hit['render_blocking_status'] == 'blocking') if hit else None,
            'cache': hit['cache_control'] if hit else None,
            'est_ms': round(size / LAB_BYTES_PER_S * 1000) if size is not None else None,
            'over_budget': (third and size > SCRIPT_BUDGET_BYTES) if size is not None else None,
            'revenue_link': None, 'brain_ref': rec['id'], 'tier': rec.get('tier'),
            'note': None if hit else 'not in the measured run',
        })
    return rows


def fix_chain(page_row, script_rows, runs, cat):
    """Fixes in shipping order on the slowest mobile page, each with its expected saving or why not."""
    if not page_row:
        return []
    lcp = page_row['lcp_ms']
    left = max(0, lcp - LCP_TARGET_MS)
    heavy = [s for s in script_rows if s['over_budget']]
    heavy.sort(key=lambda s: (not s['blocking'], -s['kb']))
    variants = {r.get('variant') for r in runs}
    rows, after = [], lcp
    for s in heavy:
        lcp_saved = min(s['est_ms'], left) if s['blocking'] else None
        if lcp_saved is not None:
            left -= lcp_saved
            after -= lcp_saved
        rows.append({'capability': 'SITE-C23', 'fix': f'Defer or remove {s["name"]} ({s["kb"]} KB, '
                     + ('blocks the page' if s['blocking'] else 'loads after the page shows') + ')',
                     'expected_ms_saved': s['est_ms'], 'lcp_ms_saved': lcp_saved, 'lcp_after': after,
                     'basis': 'transfer time on slow 4G; LCP saving capped at the gap left to target' if s['blocking']
                     else 'transfer time on slow 4G; full load only, the main image does not wait for it',
                     'brain_ref': s['brain_ref']})
    for cap, fix, why in LATER_FIXES:
        rows.append({'capability': cap, 'fix': fix, 'expected_ms_saved': None, 'lcp_ms_saved': None,
                     'lcp_after': None, 'basis': why, 'brain_ref': None})
    for i, r in enumerate(rows, 1):
        r['step'] = i
        r['autonomy'] = (cat.get(r['capability']) or {}).get('autonomy')
        r['evidence_run'] = r['capability'] if r['capability'] in variants else None
        r['evidence_note'] = None if r['evidence_run'] else 'no measured run for this fix yet'
        target = r['lcp_after'] if r['lcp_after'] is not None else LCP_TARGET_MS
        r['brief'] = {'capability': 'SITE-C32', 'autonomy': (cat.get('SITE-C32') or {}).get('autonomy'),
                      'fix_capability': r['capability'], 'page': page_row['page'],
                      'pass': f'median mobile LCP on {page_row["label"]} at or under {target:,} ms over 3 lab runs, '
                              'and the fidelity check passes',
                      'rollback': 'revert the one theme or tag change, rerun the baseline, confirm LCP is back'}
    return rows


def frames(fcp, lcp, load):
    """A frame strip drawn from 3 timings (not screenshots): blank, first paint, main image, ready."""
    def svg(stage):
        parts = ['<rect width="120" height="220" fill="#fff"/>']
        if stage >= 1:
            parts += ['<rect x="0" y="0" width="120" height="18" fill="#1f2a44"/>',
                      '<rect x="8" y="26" width="70" height="7" fill="#c9ced8"/>']
        if stage >= 2:
            parts += ['<rect x="8" y="40" width="104" height="96" fill="#e8a33d"/>',
                      '<rect x="8" y="144" width="80" height="8" fill="#1f2a44"/>']
        if stage >= 3:
            parts += ['<rect x="8" y="160" width="104" height="10" fill="#c9ced8"/>',
                      '<rect x="8" y="186" width="104" height="22" rx="4" fill="#2c6e49"/>']
        body = ''.join(parts)
        return 'data:image/svg+xml;utf8,' + body.join(
            ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 220">', '</svg>']).replace('#', '%23')
    return {'frames': [{'t': 0, 'src': svg(0)}, {'t': fcp / 1000, 'src': svg(1)}, {'t': lcp / 1000, 'src': svg(2)},
                       {'t': load / 1000, 'src': svg(3)}], 'loaded_at': round(load / 1000, 2)}


def build(data, brand):
    """Everything the screen shows for one brand. `data` is the base data layer (BrandData or server.Data)."""
    sd = SpeedData(data)
    table, speed_meta = speed_table(sd)
    try:
        runs = sd.table('speed_runs')
    except (KeyError, ValueError):
        runs = []
    mobile = [r for r in table if r['device'] == 'mobile' and r['lcp_ms'] is not None]
    slowest = max(mobile, key=lambda r: r['lcp_ms']) if mobile else None
    money = money_inputs(data, brand)
    gaps = [max(0, r['lcp_ms'] - LCP_TARGET_MS) for r in mobile]
    typical_gap_s = statistics.median(gaps) / 1000 if gaps else None
    cost = stake(typical_gap_s, money, 'seconds_over_target (median of measured mobile pages)')
    script_rows = scripts(brand, data.brand) if SAFE_BRAND.match(brand or '') else []
    cat = catalogue()
    chain = fix_chain(slowest, script_rows, runs, cat)
    film = None
    if slowest:
        target_lcp = min(slowest['lcp_ms'], LCP_TARGET_MS)
        cut = slowest['lcp_ms'] - target_lcp
        film = {'page': slowest['page'], 'label': slowest['label'],
                'before': frames(slowest['fcp_ms'], slowest['lcp_ms'], slowest['fully_loaded_ms']),
                'after': frames(min(slowest['fcp_ms'], TARGETS['fcp_ms']), target_lcp, slowest['fully_loaded_ms'] - cut)}
    try:
        captured = (data.meta('speed_runs') or {}).get('captured_at')
    except (KeyError, ValueError):
        captured = None
    return {'brand': data.brand, 'speed': {'rows': table, **speed_meta, 'captured_at': captured},
            'targets': TARGETS, 'slowest': slowest, 'money': money, 'typical_gap_s': typical_gap_s,
            'cost_of_slowness': cost, 'scripts': script_rows, 'chain': chain, 'film': film,
            'assumption': {'loss_per_second': LOSS_PER_SECOND, 'lab_bytes_per_s': LAB_BYTES_PER_S,
                           'script_budget_kb': SCRIPT_BUDGET_BYTES // 1024, 'lcp_target_ms': LCP_TARGET_MS}}


# ---------------------------------------------------------------- findings

def ev(metric, value, unit, ends_on, baseline=None, baseline_kind='threshold', source='speed_runs', freshness=1):
    return {'metric': metric, 'value': value, 'unit': unit, 'window': WINDOW, 'ends_on': ends_on,
            'freshness_days': freshness, 'baseline': baseline, 'baseline_kind': baseline_kind, 'source': source,
            'simulated': True}


def severity(money, net_revenue, fallback='medium'):
    if money and net_revenue:
        share = money['usd'] / net_revenue
        if share > 0.05:
            return 'critical'
        if share > 0.01:
            return 'high'
    return fallback


def finding(rule_id, sev, entity, evidence, sentence, cap, cat, money, ends_on, brain_refs, money_reason=None,
            status='open', unavailable=None, confidence=0.5):
    f = {'id': f'{SCREEN}.{rule_id}.{entity["id"]}', 'screen': SCREEN, 'rule_id': rule_id, 'severity': sev,
         'entity': entity, 'evidence': evidence, 'sentence': sentence,
         'capability': {'id': cap, 'autonomy': (cat.get(cap) or {}).get('autonomy', 'human_assist')},
         'money_at_stake': money, 'confidence': confidence, 'brain_refs': brain_refs, 'first_seen': ends_on,
         'last_seen': ends_on, 'status': status, 'unavailable': unavailable}
    if money is None:
        f['money_reason'] = money_reason or 'no baseline'
    return f


def seconds(ms):
    return f'{ms / 1000:.1f} s'


def run(brand='bombas', window=None, data=None):
    """Findings for one brand, sorted by severity then stake. `window` is accepted for the contract; the
    speed fixture is one capture, so the window is always the 28 days ending on the last full day."""
    if data is None:
        data = tables().brand_data(brand)
    s = build(data, brand)
    cat = catalogue()
    ends_on = (data.brand or {}).get('as_of')
    money, net = s['money'], s['money'].get('net_revenue')
    out = []
    mobile = [r for r in s['speed']['rows'] if r['device'] == 'mobile']
    if s['speed']['unavailable']:
        out.append(finding('SPEED-R01', 'high', {'type': 'device', 'id': 'mobile', 'label': 'Mobile pages'}, [],
                           'No speed run is on file, so page speed is unknown.', 'SITE-C26', cat, None, ends_on, [],
                           money_reason='inputs unavailable', status='unavailable',
                           unavailable={'inputs': ['speed_runs'], 'connector': 'speed_lab',
                                        'fix': 'Ask the agent to capture a speed baseline on the top pages.'}))
    else:
        over = [r for r in mobile if r['over_lcp_target']]
        if over:
            worst = s['slowest']
            evidence = [ev('lcp_ms', r['lcp_ms'], 'ms', ends_on, LCP_TARGET_MS) for r in over]
            m = s['cost_of_slowness']
            if m:
                evidence += [ev('sessions', money['mobile_sessions'], 'count', ends_on, None, 'threshold', 'sessions', 0),
                             ev('cvr_overall', money['cvr_overall'], 'ratio', ends_on, None, 'threshold', 'daily', 0),
                             ev('aov', money['aov'], 'usd', ends_on, None, 'threshold', 'daily', 0)]
            sentence = (f'On mobile, {len(over)} of {len(mobile)} measured pages show their main image after 2.5 s. '
                        f'The slowest is {worst["label"]} at {seconds(worst["lcp_ms"])}.')
            out.append(finding('SPEED-R01', severity(m, net), {'type': 'device', 'id': 'mobile', 'label': 'Mobile pages'},
                               evidence, sentence, 'SITE-C26', cat, m, ends_on, ['bombas.site_map.home'] if brand == 'bombas' else [],
                               money_reason=f'input unavailable: {"; ".join(money["missing"])}' if not m else None))
    by_ref = {c['brain_ref']: c for c in s['chain']}
    for sc in s['scripts']:
        if not sc['over_budget']:
            continue
        step = by_ref.get(sc['brain_ref']) or {}
        lcp_saved = step.get('lcp_ms_saved')
        # the script loads on every page, so its dollars are capped at the typical page's gap, like SPEED-R01
        priced = min(lcp_saved / 1000, s['typical_gap_s'] or 0) if sc['blocking'] and lcp_saved else 0
        m = stake(priced, money, 'lcp_seconds_this_fix_saves (capped at the typical gap)') if priced else None
        evidence = [ev('script_bytes', sc['kb'], 'KB', ends_on, SCRIPT_BUDGET_BYTES // 1024, source='speed_request_log'),
                    ev('est_transfer_ms', sc['est_ms'], 'ms', ends_on, None, source='speed_request_log')]
        if lcp_saved is not None:
            evidence.append(ev('lcp_ms_saved', lcp_saved, 'ms', ends_on, None))
        if sc['blocking']:
            sentence = (f'The {sc["name"]} script weighs {sc["kb"]} KB, over the 100 KB budget. '
                        f'It blocks the page and takes about {seconds(sc["est_ms"])} on slow 4G.')
            reason = 'the gap to the LCP target is already used by earlier fixes in the chain' if not m else None
        else:
            sentence = (f'The {sc["name"]} script weighs {sc["kb"]} KB, over the 100 KB budget. '
                        f'It loads after the page shows and adds about {seconds(sc["est_ms"])} to full load.')
            reason = 'not render blocking: it slows full load, not the main image, and no dollar link is measured'
        slug = sc['brain_ref'].rsplit('.', 1)[-1]
        out.append(finding('SPEED-R02', severity(m, net, 'medium' if sc['blocking'] else 'low'),
                           {'type': 'metric', 'id': f'script_bytes.{slug}', 'label': f'{sc["name"]} script weight'},
                           evidence, sentence, 'SITE-C23', cat, m, ends_on, [sc['brain_ref']], money_reason=reason))
    if not s['speed']['unavailable']:
        out.append(finding('SPEED-R03', 'medium', {'type': 'page', 'id': 'images', 'label': 'Images on measured pages'},
                           [], 'Image weight is unknown. The request log on file holds scripts only.', 'SITE-C22', cat,
                           None, ends_on, [], money_reason='inputs unavailable', status='unavailable',
                           unavailable={'inputs': ['speed_request_log (image rows)'], 'connector': 'speed_lab',
                                        'fix': 'Run the speed lab on the slowest page so every image is logged.'}))
    out.sort(key=lambda f: (SEVERITY_ORDER[f['severity']], -((f['money_at_stake'] or {}).get('usd') or 0)))
    return out
