"""Organic and content API: /api/16-organic-content/...

  GET overview?brand=bombas   tiles, top posts, hook table, insights, chart, findings, rules
  GET findings?brand=bombas   the audit findings only (audit.py, contract shape)

Every number comes from `content_posts`, app/metrics.py and the brain through audit.Reader. Insights
are rules in `insights()`, each with the sentence it produces and the capability it maps to. Missing
is unavailable, never 0. Default brand is bombas (simulated). Read-only: nothing here writes anywhere.
"""
import importlib.util
import re
import statistics
from datetime import timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _audit():
    spec = importlib.util.spec_from_file_location('organic_audit', HERE / 'audit.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


audit = _audit()
DEFAULT_BRAND = 'bombas'
PW, HW, SW = audit.POST_WINDOW, audit.HOOK_WINDOW, audit.SESSION_WINDOW
CREATOR_WORDS = ('creator', 'review', 'testimonial', 'unboxing', 'ugc')


def _tile(name, plain, value, unit, window, as_of, table, reason=None, fix=None, **extra):
    out = {'name': name, 'plain': plain, 'unit': unit, 'value': value, 'window': window, 'freshness': as_of,
           'unavailable_reason': reason if value is None else None, 'fix': fix if value is None else None,
           'sources': [{'table': table}]}
    out.update(extra)
    return out


def _sum(posts, key):
    vals = [p[key] for p in posts if p.get(key) is not None]
    return sum(vals) if vals else None


def _delta(now, prev):
    return round(now / prev - 1, 4) if now is not None and prev else None


def tiles(rd):
    as_of = rd.ends_on.isoformat()
    now, prev = rd.posts(PW), rd.posts(PW, rd.ends_on - timedelta(days=PW))
    views, prev_views = _sum(now, 'views'), _sum(prev, 'views')
    posts = _tile('Posts published', 'Instagram and TikTok posts that went out in the last 30 days.', len(now), 'n',
                  f'{PW}d', as_of, 'content_posts', reason='no posts in the window', fix='platform insights',
                  delta=_delta(len(now), len(prev)), delta_label='vs prior 30d',
                  inputs={'posts': len(now), 'views': views, 'prior_posts': len(prev), 'prior_views': prev_views})
    orders, prev_orders = _sum(now, 'matched_orders'), _sum(prev, 'matched_orders')
    rate = audit.per_1k(orders, views) if orders is not None else None
    prev_rate = audit.per_1k(prev_orders, prev_views) if prev_orders is not None else None
    aov = rd.aov(PW)
    yield_ = _tile('Orders per 1,000 views', 'Orders matched to a post by its link or code, per 1,000 views, 30 days.',
                   rate, 'per 1k', f'{PW}d', as_of, 'content_posts', reason='posts carry no matched orders or no views',
                   fix='Tag post links with UTM content or a promo code.', delta=_delta(rate, prev_rate),
                   delta_label='vs prior 30d',
                   inputs={'matched_orders': orders, 'views': views, 'aov_30d': aov,
                           'matched_revenue_est': round(orders * aov, 2) if orders is not None and aov is not None else None})
    cur = rd.m('session_funnel', SW, channel='Organic Social')
    old = rd.m('session_funnel', SW, rd.ends_on - timedelta(days=SW), channel='Organic Social')
    sess = None if cur.get('unavailable') else cur['inputs']['sessions']
    prev_sess = None if old.get('unavailable') else old['inputs']['sessions']
    sessions = _tile('Organic social sessions', 'GA4 sessions from the Organic Social channel group, 28 days.', sess or None,
                     'n', f'{SW}d', as_of, 'sessions', reason=cur.get('reason') or 'no Organic Social sessions in the window',
                     fix=cur.get('fix') or 'ga4', delta=_delta(sess, prev_sess), delta_label='vs prior 28d',
                     inputs={'sessions': sess, 'conversion_rate': None if cur.get('unavailable') else cur['rates']['conversion_rate'],
                             'prior_sessions': prev_sess})
    return {'posts': posts, 'orders_per_1k': yield_, 'organic_sessions': sessions}


def hook_rows(rd):
    """One row per hook, 90 days: posts, views, matched orders, orders per 1,000 views, the same for the 90 days before."""
    now = audit.hook_rates(rd.posts(HW))
    prev = audit.hook_rates(rd.posts(HW, rd.ends_on - timedelta(days=HW)))
    rows = [{'hook': k, 'posts': v['posts'], 'views': v['views'], 'matched_orders': v['orders'], 'per_1k': v['per_1k'],
             'per_1k_prior': prev.get(k, {}).get('per_1k')} for k, v in sorted(now.items())]
    rows.sort(key=lambda r: (-(r['per_1k'] or 0), r['hook']))
    return rows


def top_posts(rd, n=8):
    rows = sorted((p for p in rd.posts(PW) if p.get('views') is not None), key=lambda p: (-p['views'], p['date'], p['platform']))
    return [{'date': p['date'], 'platform': p['platform'], 'format': p.get('format'), 'hook': p.get('hook'), 'views': p['views'],
             'saves': p.get('saves'), 'clicks': p.get('clicks'), 'matched_orders': p.get('matched_orders'),
             'per_1k': audit.per_1k(p['matched_orders'], p['views']) if p.get('matched_orders') is not None else None}
            for p in rows[:n]]


def insights(rows, records, findings, posts_90):
    """The rules behind the insight cards. Each returns the sentence it produces and its capability."""
    out = []
    ok = [r for r in rows if r['posts'] >= audit.HOOK_MIN_POSTS and r['per_1k'] is not None]
    rule = (f'Orders per 1,000 views by hook over 90 days, hooks with {audit.HOOK_MIN_POSTS} or more posts; flag a hook '
            f'under {audit.HOOK_RATE_X} x the median hook (ORG-R16)')
    if len(ok) >= 2:
        best, worst = ok[0], ok[-1]
        fired = [f for f in findings if f['rule_id'] == 'ORG-R16' and f['status'] == 'open']
        sentence = fired[0]['sentence'] if fired else (
            f'{best["hook"]} posts matched {best["per_1k"]:.2f} orders per 1,000 views over 90 days. '
            f'{worst["hook"]} matched {worst["per_1k"]:.2f}.')
        out.append({'id': 'hook_yield', 'severity': fired[0]['severity'] if fired else 'info', 'capability': 'ORG-C16',
                    'autonomy': 'agent_does', 'sentence': sentence, 'rule': rule})
    else:
        out.append({'id': 'hook_yield', 'severity': 'info', 'capability': None, 'autonomy': None,
                    'sentence': 'Fewer than 2 hooks have enough posts to compare.', 'rule': rule})
    comp = [r for r in records if isinstance(r.get('value'), dict) and r['value'].get('role') == 'competitor'
            and isinstance(r['value'].get('creator_style_ads'), (int, float))]
    rule = ('Creator-style ads competitors run in the Ad Library (brain content, signal only) against our posts '
            f'with a creator or review hook, {HW} days')
    if comp:
        ads = sum(r['value']['creator_style_ads'] for r in comp)
        ours = sum(1 for p in posts_90 if any(w in (p.get('hook') or '').lower() for w in CREATOR_WORDS))
        sentence = (f'{len(comp)} competitors run {ads} creator-style ads in the Ad Library. '
                    f'{ours} of our {len(posts_90)} posts in 90 days use a creator or review hook.')
        out.append({'id': 'creator_style', 'severity': 'low', 'capability': 'ORG-C07', 'autonomy': 'agent_does',
                    'sentence': sentence, 'rule': rule, 'brain_refs': [r['id'] for r in comp]})
    else:
        out.append({'id': 'creator_style', 'severity': 'info', 'capability': None, 'autonomy': None,
                    'sentence': 'No Ad Library pull is on file, so creator-style ads cannot be compared.', 'rule': rule})
    return out


def chart(rows):
    ok = [r for r in rows if r['per_1k'] is not None]
    med = statistics.median(r['per_1k'] for r in ok) if ok else None
    return {'labels': [r['hook'] for r in ok],
            'series': [{'name': 'Last 90 days', 'values': [r['per_1k'] for r in ok]},
                       {'name': '90 days before', 'values': [r['per_1k_prior'] for r in ok]}],
            'benchmark': round(med, 4) if med is not None else None, 'window': f'{HW}d',
            'basis': 'orders matched to a post by its link or code, per 1,000 views'}


def overview(data, brand):
    ends_on = audit.last_full_day(data, brand)
    rd = audit.Reader(data, brand, ends_on)
    b = rd.source.brand
    head = {'brand': b.get('brand'), 'name': b.get('name'), 'as_of': b.get('as_of'),
            'simulated': bool(b.get('simulated') or b.get('fictional')), 'market': b.get('market')}
    findings = audit.run(brand, {'ends_on': ends_on.isoformat()}, data=data)
    if rd.all_posts() is None:
        return {'brand': head, 'unavailable': True, 'reason': 'No post export is connected.',
                'fix': 'platform insights (Instagram, TikTok, YouTube)', 'findings': findings, 'rules': audit.RULES}
    rows = hook_rows(rd)
    records = audit.brain_records(brand, 'content', ends_on)
    return {'brand': head, 'unavailable': False, 'window': {'ends_on': ends_on.isoformat(), 'posts_days': PW, 'hook_days': HW},
            'tiles': tiles(rd), 'hooks': rows, 'top_posts': top_posts(rd),
            'insights': insights(rows, records, findings, rd.posts(HW)), 'chart': chart(rows),
            'findings': findings, 'rules': audit.RULES}


def _brand(req):
    brand = req.arg('brand', DEFAULT_BRAND)
    if brand in ('', 'sample'):
        return None
    if not re.fullmatch(r'[a-z0-9-]{1,40}', brand):
        raise ValueError('brand must be a folder name like bombas')
    return brand


def handle(req):
    if req.method != 'GET':
        return 405, {'error': 'read only'}
    try:
        brand = _brand(req)
        data = None if brand else req.data
        if brand:
            audit.brand_data(brand)  # ValueError for an unknown brand
        if req.path == ['overview']:
            return overview(data, brand)
        if req.path == ['findings']:
            return {'findings': audit.run(brand, None, data=data), 'rules': audit.RULES}
    except ValueError as exc:
        return 400, {'error': str(exc)}
    return 404, {'error': 'not found', 'routes': ['overview', 'findings']}
