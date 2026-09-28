"""Brand-supplied numbers: the finance_inputs table, resolved by effective date.

Contract: app/contracts/finance-inputs.md. Rows come from the table loader
(server.Data.table or app.data.tables.load_table), so this module never knows
where the file lives.

    fin = Finance(rows)
    fin.get('cogs_landed', '2026-09-01', 'BMB-SK-M-ANK-4')  # row in force, or None
    fin.monthly('headcount_cost', start, end)               # usd over the days, or None

Rules kept here:
  - A row is in force from effective_from to effective_to, both inclusive; a blank
    effective_to means still in force. The newest effective_from wins if two overlap
    (validate() reports the overlap).
  - No default fills a blank. A missing value is None and the caller says unavailable.
  - Monthly fields are spread evenly over the days of each month, then summed.
  - Shipping labels are keyed `<carrier>:<zone band>`, for example `usps:zones_1_4`.
    The band comes from the order's fulfilment.zone when it has one, else from the
    `states` list on the label row (the brand's zone map from its origin warehouse).
"""
from __future__ import annotations

import calendar
import json
import re
from datetime import date, timedelta
from pathlib import Path

FIELDS = {  # field: (scopes, units)
    'cogs_landed': (('sku',), ('usd_per_unit',)),
    'packaging': (('global', 'sku'), ('usd_per_order',)),
    'shipping_label': (('carrier_zone',), ('usd_per_order',)),
    'threepl_pick_pack': (('global',), ('usd_per_order', 'usd_per_unit')),
    'threepl_storage': (('global',), ('usd_per_month',)),
    'returns_processing': (('global',), ('usd_per_return',)),
    'payment_fee_percent': (('channel',), ('percent',)),
    'payment_fee_fixed': (('channel',), ('usd_per_order',)),
    'marketplace_fee_percent': (('marketplace',), ('percent',)),
    'marketplace_fee_fixed': (('marketplace',), ('usd_per_order',)),
    'app_fees': (('vendor',), ('usd_per_month',)),
    'agency_fees': (('vendor',), ('usd_per_month',)),
    'fixed_costs': (('global',), ('usd_per_month',)),
    'headcount_cost': (('global',), ('usd_per_month',)),
    'cash_balance': (('global',), ('usd',)),
    'credit_line_available': (('global',), ('usd',)),
    'target_cac': (('global', 'channel'), ('usd',)),
    'target_mer': (('global',), ('percent',)),
    'target_gross_margin': (('global',), ('percent',)),
    'target_contribution_margin': (('global',), ('percent',)),
    'target_inventory_cover': (('global', 'sku'), ('weeks',)),
    'pnl_actual': (('global',), ('usd_per_month',)),
}
MONTHLY = ('threepl_storage', 'app_fees', 'agency_fees', 'fixed_costs', 'headcount_cost')
CONFIDENCE = ('invoice', 'estimate', 'simulated')
REQUIRED = ('field', 'scope', 'value', 'unit', 'effective_from', 'confidence')


def _day(value):
    return str(value)[:10] if value else None


def _in_force(row, day):
    start, end = _day(row.get('effective_from')), _day(row.get('effective_to'))
    return start is not None and start <= day and (end is None or day <= end)


def carrier_key(carrier):
    """`USPS Ground Advantage` -> `usps`: the first word, lower case."""
    words = re.findall(r'[a-z0-9]+', str(carrier or '').lower())
    return words[0] if words else None


def band_has_zone(band, zone):
    m = re.fullmatch(r'zones?_(\d+)(?:_(\d+))?', band)
    if not m:
        return False
    lo = int(m.group(1))
    hi = int(m.group(2) or lo)
    return lo <= int(zone) <= hi


class Finance:
    def __init__(self, rows):
        self.rows = [r for r in rows or () if isinstance(r, dict) and r.get('field')]
        self.by_field = {}
        for r in self.rows:
            self.by_field.setdefault(r['field'], []).append(r)
        for lst in self.by_field.values():
            lst.sort(key=lambda r: _day(r.get('effective_from')) or '', reverse=True)

    def has(self, field):
        return any(r.get('value') is not None for r in self.by_field.get(field, ()))

    def in_force(self, field, day):
        """Every row of `field` in force on `day`, one per scope key and unit (newest wins)."""
        day = _day(day)
        seen, out = set(), []
        for r in self.by_field.get(field, ()):
            key = (r.get('scope_key') or '', r.get('unit'))
            if key in seen or r.get('value') is None or not _in_force(r, day):
                continue
            seen.add(key)
            out.append(r)
        return out

    def get(self, field, day, key=None, unit=None):
        """The row in force on `day` for this scope key (None or '' for global), or None."""
        key = key or ''
        for r in self.in_force(field, day):
            if (r.get('scope_key') or '') == key and (unit is None or r.get('unit') == unit):
                return r
        return None

    def value(self, field, day, key=None, unit=None):
        r = self.get(field, day, key, unit)
        return None if r is None else r['value']

    def latest(self, field, day, key=None):
        """The newest row whose effective_from is on or before `day`: for balances as of a date."""
        day, key = _day(day), key or ''
        for r in self.by_field.get(field, ()):
            if (r.get('scope_key') or '') == key and r.get('value') is not None and _day(r['effective_from']) <= day:
                return r
        return None

    def label(self, day, carrier, zone=None, state=None):
        """The shipping_label row for an order: carrier plus zone band, by zone number or ship state."""
        ck = carrier_key(carrier)
        zone = None if zone in (None, '') else zone
        if not ck:
            return None
        for r in self.in_force('shipping_label', day):
            c, _, band = str(r.get('scope_key') or '').partition(':')
            if c != ck:
                continue
            if zone is not None and band_has_zone(band, zone):
                return r
            if zone is None and state and state in (r.get('states') or ()):
                return r
        return None

    def monthly(self, field, start, end):
        """Monthly rows spread over the days from start to end. None when any day has no row."""
        total, day = 0.0, start
        while day <= end:
            rows = self.in_force(field, day.isoformat())
            if not rows:
                return None
            days_in_month = calendar.monthrange(day.year, day.month)[1]
            total += sum(r['value'] for r in rows) / days_in_month
            day += timedelta(days=1)
        return total


def validate(rows):
    """Problems with a finance_inputs table, as plain sentences. Empty means it follows the contract."""
    problems, spans = [], {}
    for i, r in enumerate(rows):
        where = f'row {i} ({r.get("field")}:{r.get("scope_key") or "global"})'
        missing = [c for c in REQUIRED if r.get(c) in (None, '')]
        if missing:
            problems.append(f'{where} has no {", ".join(missing)}')
            continue
        spec = FIELDS.get(r['field'])
        if not spec:
            problems.append(f'{where} is not a contract field')
            continue
        if r['scope'] not in spec[0]:
            problems.append(f'{where} scope {r["scope"]} is not one of {spec[0]}')
        if r['unit'] not in spec[1]:
            problems.append(f'{where} unit {r["unit"]} is not one of {spec[1]}')
        if r['confidence'] not in CONFIDENCE:
            problems.append(f'{where} confidence {r["confidence"]} is not one of {CONFIDENCE}')
        if r['scope'] != 'global' and not r.get('scope_key'):
            problems.append(f'{where} needs a scope_key')
        if r.get('effective_to') and _day(r['effective_to']) < _day(r['effective_from']):
            problems.append(f'{where} ends before it starts')
        spans.setdefault((r['field'], r.get('scope_key') or '', r['unit']), []).append(
            (_day(r['effective_from']), _day(r.get('effective_to')) or '9999-12-31', i))
    for key, lst in spans.items():
        lst.sort()
        for (s1, e1, i1), (s2, e2, i2) in zip(lst, lst[1:]):
            if s2 <= e1:
                problems.append(f'rows {i1} and {i2} overlap for {key[0]}:{key[1] or "global"}')
    return problems


def load(path):
    """Rows from a finance_inputs.json file, for scripts and tests. Screens use the table loader."""
    doc = json.loads(Path(path).read_text(encoding='utf-8'))
    return doc['rows'] if isinstance(doc, dict) else doc
