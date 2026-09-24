"""Refresh the gallery data with a fresh re-pull of recent days.

Two parts, both local file work only (no network calls here):

  meta   Merge a Meta re-pull (days since..until) into a copy of the newest raw capture.
         The inputs are the saved results of read-only ads_get_ad_entities calls
         (Meta Ads MCP connector in Claude):
           --daily     level=ad, time_increment=1, fields id,name,amount_spent,omni_purchase,
                       omni_purchase_values,impressions,link_click
           --age / --gender / --platform
                       level=ad, breakdowns=[dim], time_increment=all_days (range inside one
                       calendar month) or monthly, fields id,name,amount_spent,omni_purchase,
                       omni_purchase_values
           --video     level=ad, object_ids=video ads, time_increment=1, the video fields in the capture
         --account-total is ad_account amount_spent for the whole capture window.
         Writes data/meta-gallery/raw/mcp_capture_<today>_1y.json. The old capture is not touched.
         Then run: python -m meta_gallery.snapshot

  sales  Apply a Metabase pull (JSON from meta_gallery/metabase_pull.js) to sales.json.
         Replaces the pulled days, moves each month total by the change in its days, checks the
         result against Metabase's own month cards, and updates the traffic rows (ga).

Re-pull at least the last 7 days: Meta keeps adding purchases for 7-day click attribution,
and the last day of an earlier pull is often a part day.
"""
import argparse
import json
import shutil
from collections import defaultdict
from datetime import date, datetime, timezone
from pathlib import Path

from .snapshot import DATA, newest_capture, rows

MONEY = ('amount_spent', 'omni_purchase_values')
COUNTS = ('omni_purchase', 'impressions', 'link_click')
DIMS = ('age', 'gender', 'publisher_platform')


def val(x):
    if x is None:
        return None
    return float(x['value']) if isinstance(x, dict) else float(x)


def in_range(r, since, until):
    return since <= r['date_start'] <= until


def merge_meta(capture, since, until, daily, breakdowns=None, video=None, account_total=None, now=None):
    """Return (new capture, checks). `breakdowns` maps age/gender/publisher_platform to rows."""
    if capture.get('version') != 2:
        raise ValueError('Needs a version 2 capture.')
    if any(not in_range(r, since, until) for r in daily):
        raise ValueError(f'Daily rows fall outside {since} to {until}.')
    cap = json.loads(json.dumps(capture))
    ads = {a['id']: a for a in cap['ads']}
    new_ids = sorted({r['id'] for r in daily} - set(ads))
    if new_ids:
        raise ValueError(f'New ads need ad and creative details in the capture first: {new_ids}')

    # Per-ad totals move by (new rows - old rows) for the re-pulled days.
    old_daily = [r for r in cap['daily'] if in_range(r, since, until)]
    delta = defaultdict(lambda: defaultdict(float))
    for sign, block in ((-1, old_daily), (1, daily)):
        for r in block:
            for k in MONEY + COUNTS:
                v = val(r.get(k))
                if v is not None:
                    delta[r['id']][k] += sign * v
    for ad_id, d in delta.items():
        a = ads[ad_id]
        for k, dv in d.items():
            if abs(dv) < 1e-9:
                continue
            nv = round((val(a.get(k)) or 0.0) + dv, 2)
            a[k] = {'value': f'{nv:.2f}', 'unit': 'INR'} if k in MONEY else str(int(round(nv)))

    cap['daily'] = [r for r in cap['daily'] if not in_range(r, since, until)] + list(daily)

    for dim, got in (breakdowns or {}).items():
        fresh = []
        for r in got:
            start, stop = r.get('date_start'), r.get('date_stop')
            if not start:
                if since[:7] != until[:7] or since[8:] != '01':
                    raise ValueError(f'{dim}: rows without dates need a range that starts on the 1st of one month.')
                start, stop = since, until
            fresh.append({'date_start': start, 'date_stop': stop, dim: r.get(dim),
                          'amount_spent': r.get('amount_spent'), 'omni_purchase': r.get('omni_purchase'),
                          'omni_purchase_values': r.get('omni_purchase_values'), 'id': r['id'], 'name': r.get('name')})
        starts = {r['date_start'] for r in fresh}
        cap['monthly'][dim] = [r for r in cap['monthly'].get(dim, []) if r['date_start'] not in starts] + fresh

    if video is not None:
        keys = list(cap['video_daily'][0].keys()) if cap.get('video_daily') else None
        fresh = [{k: r.get(k) for k in keys} if keys else r for r in video]
        cap['video_daily'] = [r for r in cap.get('video_daily', []) if not in_range(r, since, until)] + fresh

    if until > cap['window']['until']:
        cap['window']['until'] = until
    now = now or datetime.now(timezone.utc)
    cap['captured_at'] = now.strftime('%Y-%m-%dT%H:%M:%SZ')
    cap['source'] += f'; {since} to {until} re-pulled on {now.date().isoformat()}'
    if account_total is not None:
        cap['account_spend_check'] = {'account_total_spend': account_total,
                                      'note': f'Account amount_spent for the whole window, read {now.date().isoformat()}.'}

    spend = lambda block: round(sum(val(r.get('amount_spent')) or 0 for r in block), 2)
    checks = {'daily_spend_window': spend(cap['daily']), 'account_total': account_total,
              'range_spend_before': spend(old_daily), 'range_spend_after': spend(daily)}
    for dim, got in (breakdowns or {}).items():
        checks[f'{dim}_spend'] = spend(got)
    return cap, checks


# ---------- sales (Metabase) ----------

# Key columns, then value columns that add up. Products match on metal + name: Metabase's day and
# month cards can show different codes for the same piece (GHCSCH-8284 vs GHCSCH-8284_16).
SPEC = {'karat': ([0], [1, 2]), 'types': ([0, 1], [2, 3]), 'bands': ([0, 1], [2]), 'pay': ([0], [1]),
        'skus': ([0, 2], [3, 4]), 'ret': ([1], [2, 3])}
EMPTY_MONTH = {'items': 0, 'ot': {}, 'refund': None, 'ret_items': 0, **{k: [] for k in SPEC}}


def _shift(month_rows, day_rows, sign, keys, vals):
    key = lambda r: tuple(str(r[i]).strip() for i in keys)
    idx = {key(r): r for r in month_rows}
    for r in day_rows:
        k = key(r)
        if k not in idx:
            row = list(r)
            for v in vals:
                row[v] = 0
            month_rows.append(row)
            idx[k] = row
        for v in vals:
            idx[k][v] = round(idx[k][v] + sign * r[v], 2)
    month_rows[:] = [r for r in month_rows if any(abs(r[v]) > 1e-9 for v in vals)]


def shift_month(month, day, sign):
    """Add (sign=1) or remove (sign=-1) one day's figures from a month entry, in place."""
    for field, (keys, vals) in SPEC.items():
        _shift(month.setdefault(field, []), day.get(field) or [], sign, keys, vals)
    month['items'] = month.get('items', 0) + sign * (day.get('items') or 0)
    month['ret_items'] = month.get('ret_items', 0) + sign * (day.get('ret_items') or 0)
    if day.get('refund') is not None:
        month['refund'] = round((month.get('refund') or 0) + sign * day['refund'], 2) or None
    for k, (v, c) in (day.get('ot') or {}).items():
        a = month.setdefault('ot', {}).setdefault(k, [0, 0])
        month['ot'][k] = [round(a[0] + sign * v, 2), a[1] + sign * c]
    month['ot'] = {k: v for k, v in month['ot'].items() if v[1]}


def month_summary(m):
    """Counts and money totals of a month entry. Same shape as summary() in metabase_pull.js."""
    s = lambda rows, i: round(sum(r[i] for r in rows), 2)
    return {'counts': {'items': m['items'], 'ret_items': m.get('ret_items', 0),
                       'ot': {k: v[1] for k, v in sorted(m['ot'].items())},
                       'karat': s(m['karat'], 2), 'types': s(m['types'], 3), 'bands': s(m['bands'], 2),
                       'pay': s(m['pay'], 1), 'skus': s(m['skus'], 4)},
            'money': {'refund': m.get('refund') or 0,
                      'ot': {k: round(v[0], 2) for k, v in sorted(m['ot'].items())},
                      'karat': s(m['karat'], 1), 'types': s(m['types'], 2), 'skus': s(m['skus'], 3)}}


def _close(a, b, money):
    if isinstance(a, dict):
        return isinstance(b, dict) and a.keys() == b.keys() and all(_close(a[k], b[k], money) for k in a)
    if not money:
        return a == b
    # Earlier pulls stored month money in whole rupees, and day cards round a little differently
    # from month cards, so allow a few rupees (more on very large totals).
    return abs(a - b) <= max(10, 2e-6 * abs(b))


def _without_codes(entry):
    # The day card picks one of a product's codes each run (GHCSRG-6538 or GHCSRG-6538_17).
    e = dict(entry)
    e['skus'] = [[r[0], r[2], r[3], r[4]] for r in entry.get('skus') or []]
    return e


def apply_sales(sales, pull, now=None):
    """Return (new sales, report). Raises when a month does not match Metabase's month cards."""
    out = json.loads(json.dumps(sales))
    changed, codes_only = [], []
    for d, entry in sorted(pull['days'].items()):
        old = out['daily'].get(d)
        if old == entry:
            continue
        (codes_only if old and _without_codes(old) == _without_codes(entry) else changed).append(d)
        key = d[:7]
        month = out['months'].setdefault(key, json.loads(json.dumps(EMPTY_MONTH)))
        if old:
            shift_month(month, old, -1)
        shift_month(month, entry, 1)
        out['daily'][d] = entry
    out['daily'] = dict(sorted(out['daily'].items()))
    bad = {}
    for key, want in (pull.get('month_totals') or {}).items():
        got = month_summary(out['months'][key])
        if not (_close(got['counts'], want['counts'], False) and _close(got['money'], want['money'], True)):
            bad[key] = {'got': got, 'metabase': want}
    if bad:
        raise ValueError(f'Month totals do not match Metabase, nothing written: {json.dumps(bad)}')
    ga = {r[0]: r for r in out.get('ga', [])}
    ga_changed = [r[0] for r in pull.get('ga', []) if ga.get(r[0]) != r]
    for r in pull.get('ga', []):
        ga[r[0]] = r
    out['ga'] = [ga[k] for k in sorted(ga)]
    now = now or datetime.now(timezone.utc)
    out['pulled_at'] = now.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    out['daily_pulled_at'] = now.strftime('%Y-%m-%dT%H:%M:%SZ')
    return out, {'days_changed': changed, 'codes_only': codes_only, 'ga_changed': ga_changed,
                 'months_checked': sorted(pull.get('month_totals') or {})}


def _load_rows(path):
    return rows(json.loads(Path(path).read_text(encoding='utf-8')))


def main(argv=None):
    parser = argparse.ArgumentParser(description='Refresh gallery data from a re-pull of recent days.')
    sub = parser.add_subparsers(dest='cmd', required=True)
    m = sub.add_parser('meta', help='Merge a Meta re-pull into a new raw capture.')
    m.add_argument('--since', required=True)
    m.add_argument('--until', required=True)
    m.add_argument('--daily', required=True)
    m.add_argument('--age')
    m.add_argument('--gender')
    m.add_argument('--platform')
    m.add_argument('--video')
    m.add_argument('--account-total', type=float)
    m.add_argument('--capture', help='Base capture (default: newest version 2 raw capture)')
    m.add_argument('--out')
    s = sub.add_parser('sales', help='Apply a Metabase pull to sales.json.')
    s.add_argument('pull', help='JSON written from metabase_pull.js')
    s.add_argument('--sales', default=str(DATA / 'sales.json'))
    args = parser.parse_args(argv)

    if args.cmd == 'meta':
        base = Path(args.capture) if args.capture else newest_capture()
        dims = {'age': args.age, 'gender': args.gender, 'publisher_platform': args.platform}
        cap, checks = merge_meta(json.loads(base.read_text(encoding='utf-8')), args.since, args.until,
                                 _load_rows(args.daily),
                                 {k: _load_rows(v) for k, v in dims.items() if v},
                                 _load_rows(args.video) if args.video else None, args.account_total)
        out = Path(args.out) if args.out else DATA / 'raw' / f'mcp_capture_{date.today().isoformat()}_1y.json'
        if out.resolve() == base.resolve():
            raise SystemExit('Refusing to overwrite the base capture.')
        out.write_text(json.dumps(cap, ensure_ascii=False), encoding='utf-8')
        print(f'Base {base.name} -> {out.name}')
        for k, v in checks.items():
            print(f'  {k}: {v}')
        print('Next: python -m meta_gallery.snapshot')
    else:
        path = Path(args.sales)
        pull = json.loads(Path(args.pull).read_text(encoding='utf-8'))
        new, report = apply_sales(json.loads(path.read_text(encoding='utf-8')), pull)
        keep = DATA.parents[1] / 'backups' / f'sales_{datetime.now():%Y%m%d_%H%M%S}.json'  # backups/ is git-ignored
        keep.parent.mkdir(exist_ok=True)
        shutil.copy(path, keep)
        path.write_text(json.dumps(new, ensure_ascii=False), encoding='utf-8')
        print(f"Days changed: {', '.join(report['days_changed']) or 'none'}")
        if report['codes_only']:
            print(f"Only product codes differ (same pieces): {', '.join(report['codes_only'])}")
        print(f"Traffic rows changed: {', '.join(report['ga_changed']) or 'none'}")
        print(f"Month totals checked against Metabase: {', '.join(report['months_checked']) or 'none'}")
        print(f'Wrote {path} (previous copy: {keep})')


if __name__ == '__main__':
    main()
