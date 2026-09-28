"""Paid social audit (screen 11, round 0). Findings in the shape of app/contracts/audit.md.

Every number comes from app/metrics.py (ad-level Meta rows, `ad_rows`). No connector, no model call.
Same tables and window give the same findings, byte for byte.

Rules
  PAID-R01  Kill: an ad whose 7-day platform ROAS is under break-even, live all 7 days, with 7-day spend
            at or above the spend floor (3 x target CAC, the low end of the 3x to 5x read in MEDIA-C17).
            Break-even is the `break_even_roas` metric; when that needs order rows the data layer cannot
            give, it is 1 / target_gross_margin from finance_inputs (before fulfillment and fees, so the
            true line is higher and the list is short, not long). Money: spend_7d - purchase_value_7d /
            break_even, the spend not paid back at break-even. Capability MEDIA-C17 (founder gate).
            Owner: 11-paid-social.
  PAID-R03  Fatigue: an ad whose CTR fell 20 percent or more over 14 days (last 7 days against the 7
            before) while frequency rose, with 7-day spend at or above the floor. Money: spend_7d -
            purchases_7d x the ad's median CPA over its 4 trailing 7-day windows (null, "no baseline",
            when the ad has fewer than 4). Capability CREA-C15 (agent does). Owner: 11-paid-social;
            09-creative reads it from the findings table.

Scale is not a finding: an ad above target is not broken. The screen lists it next to the kills.
Verdicts in `verdict()` use the same thresholds so the list and the findings never disagree.
"""
import importlib.util
import json
import statistics
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parents[1]
SCREEN = '11-paid-social'

KILL_DAYS = 7
FATIGUE_CTR_DROP = 0.20
SCALE_MAX_FREQUENCY = 2.5
FLOOR_TIMES_CAC = 3
TRAILING = 4

RULES = [
    {'rule_id': 'PAID-R01', 'name': 'Ad under break-even for 7 days with spend above the floor', 'entity_type': 'ad',
     'inputs': ['ad_rows', 'finance_inputs.target_gross_margin', 'finance_inputs.target_cac'],
     'capability': 'MEDIA-C17', 'owner_screen': SCREEN},
    {'rule_id': 'PAID-R03', 'name': 'CTR down 20 percent over 14 days while frequency rises', 'entity_type': 'ad',
     'inputs': ['ad_rows'], 'capability': 'CREA-C15', 'owner_screen': SCREEN},
]
CAPABILITY = {'PAID-R01': {'id': 'MEDIA-C17', 'autonomy': 'founder_gate'},
              'PAID-R03': {'id': 'CREA-C15', 'autonomy': 'agent_does'}}
SEVERITY_ORDER = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_MODS = {}


def metrics():
    if 'metrics' not in _MODS:
        _MODS['metrics'] = _load('ecomos_metrics_paid', APP / 'metrics.py')
    return _MODS['metrics']


def brand_data(brand):
    if 'tables' not in _MODS:
        _MODS['tables'] = _load('ecomos_tables_paid', APP / 'data' / 'tables.py')
    return _MODS['tables'].brand_data(brand)


class Reader:
    """One brand, one window end. m(name, **kw) is metrics.compute with the brand and end filled in."""

    def __init__(self, data, brand, ends_on):
        self.data, self.brand, self.ends_on = data, brand, ends_on

    def m(self, name, days, end=None, **kw):
        q = {'window': f'{days}d', 'end': (end or self.ends_on).isoformat(), **kw}
        if self.brand:
            q['brand'] = self.brand
        return metrics().compute(name, self.data, **q)

    def ads(self, days=7, end=None):
        r = self.m('spend', days, end, channel='meta', by='ad')
        return r, ({g['ad']: g for g in r['groups']} if not r.get('unavailable') else {})

    def finance_rows(self):
        source = self.data if not self.brand else brand_data(self.brand)
        try:
            return source.table('finance_inputs')
        except (KeyError, ValueError):
            pass
        path = Path(getattr(source, 'folder', '') or '') / 'finance_inputs.json'
        if path.is_file():
            doc = json.loads(path.read_text(encoding='utf-8'))
            return doc.get('rows') if isinstance(doc, dict) else doc
        return None


def last_full_day(data, brand):
    source = brand_data(brand) if brand else data
    return date.fromisoformat(source.brand['as_of'])


def thresholds(rd):
    """Break-even ROAS, target ROAS and the spend floor, each with where it came from. None when unknown."""
    out = {'break_even': None, 'break_even_source': None, 'target_roas': None, 'target_source': None,
           'floor': None, 'floor_source': None, 'target_cac': None, 'margin_before_marketing': None}
    rows = rd.finance_rows()
    fin = metrics().finance.Finance(rows) if rows else None
    day = rd.ends_on.isoformat()
    be = rd.m('break_even_roas', 28)
    if not be.get('unavailable') and be.get('value'):
        out['break_even'] = be['value']
        out['margin_before_marketing'] = be.get('margin_before_marketing')
        out['break_even_source'] = 'break_even_roas: 1 over contribution margin before marketing, 28 days'
    elif fin and fin.value('target_gross_margin', day):
        gm = fin.value('target_gross_margin', day) / 100
        out['break_even'] = round(1 / gm, 4)
        out['margin_before_marketing'] = gm
        out['break_even_source'] = (f'1 over the target gross margin ({round(gm * 100)} percent). Full break-even '
                                    f'needs order-level costs: {be.get("reason")}')
    cm = fin.value('target_contribution_margin', day) if fin else None
    mbm = out['margin_before_marketing']
    if mbm and cm is not None and mbm - cm / 100 > 0:
        out['target_roas'] = round(1 / (mbm - cm / 100), 4)
        out['target_source'] = f'ROAS that still leaves the target contribution margin of {round(cm)} percent'
    cac = fin.value('target_cac', day) if fin else None
    if cac:
        out['target_cac'] = cac
        out['floor'] = round(FLOOR_TIMES_CAC * cac, 2)
        out['floor_source'] = f'{FLOOR_TIMES_CAC} x target CAC of ${cac:,.0f}'
    else:
        cpa = rd.m('cpa', 28, channel='meta')
        if not cpa.get('unavailable'):
            out['floor'] = round(FLOOR_TIMES_CAC * cpa['value'], 2)
            out['floor_source'] = f'{FLOOR_TIMES_CAC} x the 28-day Meta CPA (no target CAC on file)'
    return out


def ad_windows(rd, weeks=TRAILING + 1):
    """Ad groups for the current 7 days and the weeks before it, newest first."""
    out = []
    for k in range(weeks):
        _, ads = rd.ads(7, rd.ends_on - timedelta(days=7 * k))
        out.append(ads)
    return out


def live_days(ad, win_end, days=7):
    start = (win_end - timedelta(days=days - 1)).isoformat()
    return ad.get('first_day') <= start and ad.get('last_day') >= win_end.isoformat()


def verdict(ad, prev, th, ends_on):
    """kill, scale, watch, wait (under the spend floor) or off (no spend on the last day), with the reason. Same thresholds as the rules."""
    if th['floor'] is None or th['break_even'] is None:
        return 'unavailable', 'no break-even or spend floor on file'
    if ad.get('last_day') and ad['last_day'] < ends_on.isoformat():
        return 'off', f'no spend since {ad["last_day"]}'
    if ad['spend'] < th['floor']:
        return 'wait', f'spent under the ${th["floor"]:,.0f} floor'
    roas = ad['roas'] or 0
    if roas < th['break_even'] and live_days(ad, ends_on):
        return 'kill', f'{roas:.2f}x ROAS for 7 days, break-even is {th["break_even"]:.2f}x'
    freq = ad.get('frequency')
    if th['target_roas'] and roas >= th['target_roas'] and freq is not None and freq < SCALE_MAX_FREQUENCY:
        return 'scale', f'{roas:.2f}x ROAS over the {th["target_roas"]:.2f}x target at {freq:.1f} frequency'
    return 'watch', 'between break-even and target'


def fatigue(ad, prev):
    """(ctr_change, freq_change) when CTR fell 20 percent or more while frequency rose, else None."""
    if not prev or not ad.get('ctr') or not prev.get('ctr') or ad.get('frequency') is None or prev.get('frequency') is None:
        return None
    ctr_change = ad['ctr'] / prev['ctr'] - 1
    if ctr_change <= -FATIGUE_CTR_DROP and ad['frequency'] > prev['frequency']:
        return round(ctr_change, 4), round(ad['frequency'] - prev['frequency'], 4)
    return None


def _ev(metric, value, unit, ends_on, baseline=None, baseline_kind=None, window='7d', source='ad_rows'):
    return {'metric': metric, 'value': value, 'unit': unit, 'window': window, 'ends_on': ends_on.isoformat(),
            'freshness_days': 1, 'baseline': baseline, 'baseline_kind': baseline_kind, 'source': source, 'simulated': True}


def _confidence(windows_agree):
    return 0.9 if windows_agree >= 4 else 0.7 if windows_agree >= 2 else 0.5


def _severity(stake, net_28d, windows_agree):
    if stake is not None and net_28d and stake > 0.05 * net_28d:
        return 'critical'
    if windows_agree >= 2 or (stake is not None and net_28d and stake > 0.01 * net_28d):
        return 'high'
    return 'medium'


def _label(ad):
    return ad.get('ad_name') or f'{ad["ad"]} ({ad.get("format") or "ad"}, {ad.get("campaign_name") or ad.get("campaign_id")})'


def _flags(ad):
    out = []
    if ad.get('shared_creative'):
        out.append('shares its image or video with another ad; ad-level rows kept')
    if ad.get('dynamic_creative'):
        out.append('dynamic creative: mixed assets, read as one ad')
    return out


def _finding(rule_id, ad, ends_on, severity, evidence, sentence, stake, confidence, brain_refs=()):
    ad_id = ad['ad']
    out = {'id': f'{SCREEN}.{rule_id}.{ad_id}', 'screen': SCREEN, 'rule_id': rule_id, 'severity': severity,
           'entity': {'type': 'ad', 'id': ad_id, 'label': _label(ad)}, 'evidence': evidence, 'sentence': sentence,
           'capability': dict(CAPABILITY[rule_id]), 'money_at_stake': stake, 'confidence': confidence,
           'brain_refs': list(brain_refs), 'first_seen': ends_on.isoformat(), 'last_seen': ends_on.isoformat(),
           'status': 'open', 'unavailable': None}
    if stake is None:
        out['money_reason'] = 'no baseline'
    flags = _flags(ad)
    if flags:
        out['flags'] = flags
    return out


def _unavailable(rule_id, ends_on, reason, inputs, connector, fix):
    return {'id': f'{SCREEN}.{rule_id}.brand', 'screen': SCREEN, 'rule_id': rule_id, 'severity': 'high',
            'entity': {'type': 'brand', 'id': 'brand', 'label': 'Meta account'}, 'evidence': [],
            'sentence': reason, 'capability': dict(CAPABILITY[rule_id]), 'money_at_stake': None,
            'money_reason': 'inputs unavailable', 'confidence': 0.1, 'brain_refs': [],
            'first_seen': ends_on.isoformat(), 'last_seen': ends_on.isoformat(), 'status': 'unavailable',
            'unavailable': {'inputs': inputs, 'connector': connector, 'fix': fix}}


def kill_findings(windows, th, ends_on, net_28d):
    now, out = windows[0], []
    for ad in now.values():
        if verdict(ad, windows[1].get(ad['ad']), th, ends_on)[0] != 'kill':
            continue
        be = th['break_even']
        stake_usd = round(ad['spend'] - ad['purchase_value'] / be)
        agree = 1 + sum(1 for w in windows[1:] if ad['ad'] in w and (w[ad['ad']]['roas'] or 0) < be)
        stake = {'usd': stake_usd, 'formula': 'spend_7d - purchase_value_7d / break_even_roas',
                 'inputs': {'spend_7d': ad['spend'], 'purchase_value_7d': ad['purchase_value'], 'break_even_roas': be},
                 'window': '7d'}
        evidence = [_ev('platform_roas', ad['roas'], 'x', ends_on, be, 'threshold'),
                    _ev('spend', ad['spend'], 'usd', ends_on, th['floor'], 'threshold'),
                    _ev('purchases', ad['purchases'], 'count', ends_on),
                    _ev('windows_below_break_even', agree, 'count', ends_on, window=f'{7 * len(windows)}d')]
        sentence = (f'{ad["ad"]} returned {ad["roas"]:.2f}x on ${ad["spend"]:,.0f} this week. '
                    f'Break-even is {be:.2f}x, so ${stake_usd:,} did not pay back.')
        out.append(_finding('PAID-R01', ad, ends_on, _severity(stake_usd, net_28d, agree), evidence, sentence, stake,
                            _confidence(agree)))
    return out


def fatigue_findings(windows, th, ends_on, net_28d):
    now, prev, out = windows[0], windows[1], []
    for ad in now.values():
        p = prev.get(ad['ad'])
        hit = fatigue(ad, p)
        if not hit or th['floor'] is None or ad['spend'] < th['floor'] or ad['last_day'] < ends_on.isoformat():
            continue
        ctr_change, _ = hit
        past = [w[ad['ad']]['cpa'] for w in windows[1:] if ad['ad'] in w and w[ad['ad']].get('cpa')]
        stake = None
        if len(past) >= TRAILING:
            base = round(statistics.median(past), 2)
            usd = round(max(ad['spend'] - ad['purchases'] * base, 0))
            stake = {'usd': usd, 'formula': 'spend_7d - purchases_7d * cpa_median_4w',
                     'inputs': {'spend_7d': ad['spend'], 'purchases_7d': ad['purchases'], 'cpa_median_4w': base},
                     'window': '7d'}
        agree = 1 + (1 if len(windows) > 2 and fatigue(p, windows[2].get(ad['ad'])) else 0)
        evidence = [dict(_ev('ctr', ad['ctr'], 'ratio', ends_on, p['ctr'], 'own_median'), note='baseline is the 7 days before'),
                    dict(_ev('frequency', ad['frequency'], 'x', ends_on, p['frequency'], 'own_median'),
                         note='baseline is the 7 days before; reach summed from daily rows'),
                    _ev('spend', ad['spend'], 'usd', ends_on, th['floor'], 'threshold')]
        sentence = (f'{ad["ad"]} is shown {ad["frequency"]:.1f} times per person this week, up from {p["frequency"]:.1f}. '
                    f'Its click rate fell {abs(round(ctr_change * 100))} percent in 14 days.')
        usd = stake['usd'] if stake else None
        out.append(_finding('PAID-R03', ad, ends_on, _severity(usd, net_28d, agree), evidence, sentence, stake,
                            max(round(_confidence(agree) - 0.2, 2), 0.1)))  # frequency is from summed daily reach
    return out


def run(brand, window=None, data=None):
    """Findings for one brand and window ({ends_on, days, trailing}), sorted by severity then stake."""
    data = data if data is not None else (brand_data(brand) if brand else None)
    ends_on = date.fromisoformat(window['ends_on']) if window and window.get('ends_on') else last_full_day(data, brand)
    rd = Reader(data, brand, ends_on)
    first, _ = rd.ads(7)
    if first.get('unavailable'):
        return [_unavailable(r, ends_on, 'Meta ad rows are not connected, so kill and fatigue rules cannot run.',
                             ['ad_rows'], first.get('fix') or 'meta_ads', 'Connect the Meta ad account (read only).')
                for r in ('PAID-R01', 'PAID-R03')]
    th = thresholds(rd)
    windows = ad_windows(rd)
    mer = rd.m('mer', 28)
    net_28d = (mer.get('inputs') or {}).get('net_revenue') if not mer.get('unavailable') else None
    out = []
    if th['break_even'] is None or th['floor'] is None:
        out.append(_unavailable('PAID-R01', ends_on, 'Break-even ROAS is unknown, so no ad can be called a kill.',
                                ['finance_inputs.target_gross_margin', 'finance_inputs.target_cac'], 'finance_inputs',
                                'Enter gross margin and target CAC on the setup screen.'))
    else:
        out += kill_findings(windows, th, ends_on, net_28d)
    out += fatigue_findings(windows, th, ends_on, net_28d)
    out.sort(key=lambda f: (SEVERITY_ORDER[f['severity']], -((f['money_at_stake'] or {}).get('usd') or 0), f['id']))
    return out
