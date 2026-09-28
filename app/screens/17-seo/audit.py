"""Audit for 17-seo: where unpaid search is leaking visits and money, with proof.

Findings follow app/contracts/audit.md. Sessions, AOV and conversion come from app/metrics.py
(session_funnel, aov). Search Console rows have no metric in metrics.md yet, so they are read from
the brand's data layer (`search_console`, the same data.sqlite metrics.py reads) with one GROUP BY
here; a contract session can lift ctr_by_query_group into metrics.py later. Brand facts come from
app/brain/<brand>/ through store.Brain. No connector, no model, no wall clock: the same tables,
brain and window give the same findings. Every rule below is owned by 17-seo.

Rules (one per insight in the room spec's JTBD table, room "SEO", agent ORG)
  SEO-R01  Unexplained organic drop. Organic Search sessions (session_funnel channel=Organic Search)
           in the last 7 days against the 7 days before. Fires at a fall of DROP_WOW or more. No
           algorithm update or cause log is connected, so every drop counts as unexplained. Stake =
           lost sessions x organic conversion rate x AOV. Capability ORG-C32.
  SEO-R02  CTR mismatch. Search Console rows in the window by page and query. A query row in the
           top 20 percent by impressions fires when its CTR sits CTR_GAP or more below the CTR curve
           for its position (CTR_CURVE, branded curve for queries holding the brand name). Stake =
           (curve CTR - CTR) x impressions x the page's organic conversion rate x AOV. Windows
           agreeing: the same test on each earlier window Search Console covers. Capability ORG-C21.
  SEO-R03  Keyword cannibalization. 2 or more pages with impressions on one query, average
           positions within CANNIBAL_SPREAD. Capability ORG-C27.
  SEO-R04  Orphan money page. Needs crawl_snapshot internal_inlinks and keyword_question_map.
           Capability ORG-C27.
  SEO-R05  Stale high value page. Needs organic revenue by page from ga4_orders_join and a page
           last-updated date. Capability ORG-C26.
  SEO-R06  Broken schema on a money page. Needs schema_validation_log. Capability ORG-C23.
  SEO-R07  Long redirect chain (3 or more hops). Needs crawl_snapshot redirect_hops. Capability ORG-C20.
  SEO-R08  Discontinued page 404ing. Needs product_feed_status. Capability ORG-C26.
  SEO-R09  Outreach not landing links (60 pitches in 60 days, 0 new domains). Needs backlink_index
           and an outreach log. Capability ORG-C28.
  SEO-R10  Unanswered Google Business Profile reviews over 7 days. Needs gbp_reviews. Capability ORG-C29.
  SEO-R11  Tag stopped firing. Daily GA4 counts of sessions, add to cart and purchase for the window
           (session_funnel, one call per day). Fires when an event reads 0 on 2 or more days in a
           row. The ga4_tag_audit table (expected counts) is not written; this checks GA4's own
           totals only. Capability MONEY-C20.
  SEO-R12  AI crawler blocked on a money page. Needs robots_txt_snapshot by user agent. The brain's
           site_map.crawl_access summary names no agent rules, so it cannot decide. Capability ORG-C20.
  SEO-R13  Vendor claim does not hold up. Needs a vendor_claims record (the pitch numbers). Capability ORG-C33.

Severity: critical when stake is over 5 percent of net revenue in the window, high over 1 percent or
when 2 or more windows agree, else medium. Net revenue here is GA4 purchases x AOV so both sides
share one data scale. A rule whose inputs are not written emits one unavailable finding.
"""
import importlib.util
import math
import statistics
import sys
from datetime import date, timedelta
from pathlib import Path

APP = Path(__file__).resolve().parents[2]
SCREEN = '17-seo'
ORGANIC = 'Organic Search'
FRESHNESS_DAYS = 1
DROP_WOW = 0.15
CTR_GAP = 0.30
TOP_SHARE = 0.20
CANNIBAL_SPREAD = 5.0
ZERO_DAYS = 2

# CTR by position, positions 1 to 10, then 0.01 to 20. Non-branded follows the room spec benchmark
# (25 to 35 percent at position 1) and the public click curves; branded queries get twice the rate
# (a searcher who types the brand is looking for the site).
CTR_CURVE = (0.28, 0.155, 0.11, 0.08, 0.06, 0.045, 0.035, 0.028, 0.023, 0.02)
BRANDED_FACTOR = 2.0
BRAND_TERMS = {'bombas': ('bombas',)}

UNAVAILABLE = {  # rule: (severity if it fired, inputs, connector, fix, capability, autonomy, entity label)
    'SEO-R04': ('medium', ['crawl_snapshot.internal_inlinks', 'keyword_question_map'],
                'site crawler (JS-rendered, Screaming Frog style) plus the ORG-C18 keyword map',
                'Run a site crawl and save the keyword map, then this rule can list money pages with no internal links.',
                'ORG-C27', 'agent_does', 'Internal links to money pages'),
    'SEO-R05': ('high', ['ga4_orders_join', 'page last updated date'],
                'GA4 export joined to Shopify orders, plus Shopify page updated_at or sitemap lastmod',
                'Join GA4 sessions to store orders and read page update dates, then pages can be ranked by revenue at risk.',
                'ORG-C26', 'founder_gate', 'Refresh backlog by revenue at risk'),
    'SEO-R06': ('medium', ['schema_validation_log'], 'structured data validator run on product and collection pages',
                'Validate product and collection schema, then broken pages show here.',
                'ORG-C23', 'agent_does', 'Schema on money pages'),
    'SEO-R07': ('low', ['crawl_snapshot.redirect_hops'], 'site crawler (JS-rendered, Screaming Frog style)',
                'Run a site crawl, then URLs with 3 or more redirects show here.',
                'ORG-C20', 'agent_does', 'Redirect chains'),
    'SEO-R08': ('medium', ['product_feed_status'], 'merchant feed plus Shopify product export',
                'Connect the product feed with each page status, then discontinued pages that 404 show here.',
                'ORG-C26', 'agent_does', 'Discontinued product pages'),
    'SEO-R09': ('low', ['backlink_index', 'outreach log'], 'backlink index (Ahrefs or Semrush class tool)',
                'Connect a backlink index and log outreach pitches, then links per pitch show here.',
                'ORG-C28', 'human_assist', 'Outreach results'),
    'SEO-R10': ('low', ['gbp_reviews'], 'Google Business Profile',
                'Connect Google Business Profile for the retail stores, then unanswered reviews show here.',
                'ORG-C29', 'human_assist', 'Store reviews on Google'),
    'SEO-R12': ('medium', ['robots_txt_snapshot'], 'robots.txt fetch, read by user agent',
                'Fetch robots.txt on a schedule, then money pages closed to GPTBot, PerplexityBot or Google-Extended show here.',
                'ORG-C20', 'agent_does', 'AI crawler access'),
    'SEO-R13': ('low', ['vendor_claims'], 'none: the founder pastes the vendor pitch numbers',
                'Paste a vendor pitch, then its numbers are checked against our own analytics.',
                'ORG-C33', 'founder_gate', 'Vendor pitch check'),
}
NAMES = {
    'SEO-R01': 'Organic visits fell 15 percent or more week over week', 'SEO-R02': 'High impression query with a CTR well under its position',
    'SEO-R03': '2 or more pages compete for one query', 'SEO-R04': 'Money page with no internal links',
    'SEO-R05': 'High value page falling and not refreshed', 'SEO-R06': 'Broken schema on a money page',
    'SEO-R07': 'URL takes 3 or more redirects', 'SEO-R08': 'Discontinued product page returns 404',
    'SEO-R09': 'Outreach pitches with no new links', 'SEO-R10': 'Store review unanswered over a week',
    'SEO-R11': 'Key GA4 event stopped firing', 'SEO-R12': 'AI crawler blocked on a money page',
    'SEO-R13': 'Vendor claim differs from our analytics',
}
LIVE = {  # rules that read written tables: entity type, inputs, capability, autonomy
    'SEO-R01': ('brand', ['sessions', 'aggregates/daily'], 'ORG-C32', 'agent_does'),
    'SEO-R02': ('page', ['search_console', 'sessions', 'aggregates/daily'], 'ORG-C21', 'agent_does'),
    'SEO-R03': ('page', ['search_console'], 'ORG-C27', 'agent_does'),
    'SEO-R11': ('metric', ['sessions'], 'MONEY-C20', 'human_assist'),
}
RULES = [{'rule_id': r, 'name': NAMES[r],
          'entity_type': LIVE[r][0] if r in LIVE else ('brand' if r in ('SEO-R09', 'SEO-R10', 'SEO-R13') else 'page'),
          'inputs': LIVE[r][1] if r in LIVE else UNAVAILABLE[r][1],
          'capability': LIVE[r][2] if r in LIVE else UNAVAILABLE[r][4], 'owner_screen': SCREEN}
         for r in sorted(NAMES)]
SEVERITY_ORDER = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}


def _load(name, path):
    mod = sys.modules.get(name)
    if mod is None:
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod
        spec.loader.exec_module(mod)
    return mod


def metrics_module():
    return _load('ecomos_metrics', APP / 'metrics.py')


def brain(brand, as_of):
    folder = str(APP / 'brain')
    if folder not in sys.path:
        sys.path.insert(0, folder)
    store = _load('ecomos_brain_store', APP / 'brain' / 'store.py')
    return store.Brain(brand, today=date.fromisoformat(as_of) + timedelta(days=1))


# ---------------------------------------------------------------- words

def usd(x):
    return f'${round(x):,}'


def pct(x):
    return f'{x * 100:.{1 if abs(x) < 0.1 else 0}f} percent'


def page_label(page):
    return 'home page' if page == '/' else page


def slug(page):
    return 'home' if page == '/' else page.strip('/').replace('/', '_')


# ---------------------------------------------------------------- numbers

def window_of(brand, window):
    data = metrics_module().resolve(None, {'brand': brand})
    w = dict(window or {})
    return {'ends_on': w.get('ends_on') or data.brand['as_of'], 'days': int(w.get('days') or 28),
            'trailing': int(w.get('trailing') or 4)}


def start_of(w, shift=0):
    end = date.fromisoformat(w['ends_on']) - timedelta(days=w['days'] * shift)
    return (end - timedelta(days=w['days'] - 1)).isoformat(), end.isoformat()


def funnel(brand, days, end, **filters):
    return metrics_module().compute('session_funnel', None, brand=brand, window=f'{days}d', end=end, **filters)


def aov(brand, w):
    return metrics_module().compute('aov', None, brand=brand, window=f"{w['days']}d", end=w['ends_on'])


def net_revenue_est(brand, w, a):
    """GA4 purchases x AOV for the window, on the same data scale as sessions and Search Console."""
    r = funnel(brand, w['days'], w['ends_on'])
    if r.get('unavailable') or a.get('unavailable'):
        return None
    return r['inputs']['purchase'] * a['value']


def branded(brand, query):
    return any(t in query.lower() for t in BRAND_TERMS.get(brand, (brand.lower(),)))


def curve_ctr(position, is_branded):
    """CTR the curve expects at a position, linear between whole positions."""
    p = max(1.0, float(position))
    if p >= 20:
        base = 0.01
    elif p >= 10:
        base = CTR_CURVE[-1] + (0.01 - CTR_CURVE[-1]) * (p - 10) / 10
    else:
        i = int(p) - 1
        nxt = CTR_CURVE[i + 1] if i + 1 < len(CTR_CURVE) else CTR_CURVE[-1]
        base = CTR_CURVE[i] + (nxt - CTR_CURVE[i]) * (p - int(p))
    return min(base * (BRANDED_FACTOR if is_branded else 1.0), 0.95)


def sc_span(brand):
    data = metrics_module().resolve(None, {'brand': brand})
    try:
        r = data._sql('SELECT MIN(date) AS first, MAX(date) AS last FROM search_console')[0]
    except Exception:
        return None
    return r if r['first'] else None


def sc_rows(brand, start, end):
    """Search Console totals by page and query for a date range; position is impression weighted."""
    data = metrics_module().resolve(None, {'brand': brand})
    rows = data._sql("SELECT page, query, SUM(clicks) AS clicks, SUM(impressions) AS impressions, "
                     "SUM(position * impressions) AS pos_x_imp FROM search_console "
                     f"WHERE date BETWEEN '{start}' AND '{end}' GROUP BY page, query ORDER BY page, query")
    out = []
    for r in rows:
        if not r['impressions']:
            continue
        out.append({'page': r['page'], 'query': r['query'], 'clicks': int(r['clicks']), 'impressions': int(r['impressions']),
                    'ctr': round(r['clicks'] / r['impressions'], 6), 'position': round(r['pos_x_imp'] / r['impressions'], 2),
                    'branded': branded(brand, r['query'])})
    return out


def sc_windows(brand, w):
    """(start, end) for the current window and each earlier one Search Console fully covers, newest first."""
    span = sc_span(brand)
    if not span:
        return []
    out = []
    for k in range(w['trailing']):
        s, e = start_of(w, k)
        if s >= span['first'] and e <= span['last']:
            out.append((s, e))
    return out


def ctr_by_group(brand, start, end):
    rows = sc_rows(brand, start, end)
    out = {}
    for g in (True, False):
        c = sum(r['clicks'] for r in rows if r['branded'] == g)
        i = sum(r['impressions'] for r in rows if r['branded'] == g)
        out['branded' if g else 'non_branded'] = {'clicks': c, 'impressions': i, 'ctr': round(c / i, 6) if i else None}
    return out


# ---------------------------------------------------------------- finding helpers

def ev(metric, value, unit, w, source, baseline=None, baseline_kind=None, window=None):
    return {'metric': metric, 'value': value, 'unit': unit, 'window': window or f"{w['days']}d", 'ends_on': w['ends_on'],
            'freshness_days': FRESHNESS_DAYS, 'baseline': baseline, 'baseline_kind': baseline_kind, 'source': source,
            'simulated': True}


def severity(stake, revenue, agree):
    if stake and revenue and stake > 0.05 * revenue:
        return 'critical'
    if (stake and revenue and stake > 0.01 * revenue) or agree >= 2:
        return 'high'
    return 'medium'


def confidence(agree, sampled=False):
    c = 0.9 if agree >= 4 else 0.7 if agree >= 2 else 0.5
    return round(max(0.1, c - (0.2 if sampled else 0)), 2)


def finding(rule, sev, entity, evidence, sentence, cap, autonomy, money, conf, w, brain_refs=(), status='open', unavailable=None,
            money_reason=None):
    f = {'id': f"{SCREEN}.{rule}.{entity['id']}", 'screen': SCREEN, 'rule_id': rule, 'severity': sev, 'entity': entity,
         'evidence': evidence, 'sentence': sentence, 'capability': {'id': cap, 'autonomy': autonomy},
         'money_at_stake': money, 'confidence': conf, 'brain_refs': list(brain_refs),
         'first_seen': w['ends_on'], 'last_seen': w['ends_on'], 'status': status, 'unavailable': unavailable}
    if money is None and money_reason:
        f['money_reason'] = money_reason
    return f


def unavailable_finding(rule, w, reason_inputs=None, connector=None, fix=None, brain_refs=()):
    sev, inputs, conn, fx, cap, autonomy, label = UNAVAILABLE.get(rule) or (None,) * 7
    if rule in LIVE:
        sev, cap, autonomy, label = 'medium', LIVE[rule][2], LIVE[rule][3], NAMES[rule]
    etype = next(r['entity_type'] for r in RULES if r['rule_id'] == rule)
    return finding(rule, sev, {'type': etype, 'id': 'all', 'label': label}, [],
                   f'{label} cannot be checked yet. The data it needs is not connected.', cap, autonomy, None, 0.1, w,
                   brain_refs, status='unavailable', money_reason='inputs not connected',
                   unavailable={'inputs': reason_inputs or inputs, 'connector': connector or conn, 'fix': fix or fx})


# ---------------------------------------------------------------- rules

def r01_drop(brand, w, ctx):
    now = funnel(brand, 7, w['ends_on'], channel=ORGANIC)
    prior_end = (date.fromisoformat(w['ends_on']) - timedelta(days=7)).isoformat()
    before = funnel(brand, 7, prior_end, channel=ORGANIC)
    if now.get('unavailable') or before.get('unavailable'):
        return [unavailable_finding('SEO-R01', w, ['sessions (Organic Search)'], 'ga4', 'Connect GA4 sessions by channel group.')]
    cur, prev = now['value'], before['value']
    drop = 1 - cur / prev if prev else 0
    if drop < DROP_WOW:
        return []
    cvr, a = ctx['organic_cvr'], ctx['aov']
    stake = (prev - cur) * cvr * a if cvr is not None and a is not None else None
    money = {'usd': round(stake), 'formula': '(sessions_prior_7d - sessions_7d) x organic_conversion_rate x aov',
             'inputs': {'sessions_prior_7d': prev, 'sessions_7d': cur, 'organic_conversion_rate': cvr, 'aov': a},
             'window': '7d'} if stake is not None else None
    sev = severity(stake, ctx['revenue_7d'], 1)
    return [finding('SEO-R01', sev, {'type': 'brand', 'id': brand, 'label': 'Organic search visits'},
                    [ev('organic_sessions', cur, 'count', w, 'sessions', prev, 'threshold', '7d')],
                    f'Organic visits fell {pct(drop)} this week, from {prev:,} to {cur:,}. No known cause is logged.',
                    'ORG-C32', 'agent_does', money, confidence(1), w, money_reason=None if money else 'no conversion rate')]


def r02_ctr(brand, w, ctx):
    wins = sc_windows(brand, w)
    if not wins:
        return [unavailable_finding('SEO-R02', w, ['search_console'], 'Google Search Console',
                                    'Connect Search Console, then pages with a low CTR for their position show here.')]
    per_window = [sc_rows(brand, s, e) for s, e in wins]

    def misses(rows):
        ranked = sorted(rows, key=lambda r: (-r['impressions'], r['page'], r['query']))
        top = ranked[:max(1, math.ceil(len(ranked) * TOP_SHARE))]
        out = {}
        for r in top:
            exp = curve_ctr(r['position'], r['branded'])
            if r['ctr'] <= exp * (1 - CTR_GAP):
                out[(r['page'], r['query'])] = dict(r, expected=round(exp, 4))
        return out

    hits = [misses(rows) for rows in per_window]
    out = []
    for key, r in sorted(hits[0].items()):
        agree = sum(1 for h in hits if key in h)
        page, query = key
        cvr = ctx['page_cvr'](page)
        a = ctx['aov']
        lost = (r['expected'] - r['ctr']) * r['impressions']
        stake = lost * cvr * a if cvr is not None and a is not None else None
        money = {'usd': round(stake), 'formula': '(curve_ctr - ctr) x impressions x organic_conversion_rate_on_page x aov',
                 'inputs': {'curve_ctr': r['expected'], 'ctr': r['ctr'], 'impressions': r['impressions'],
                            'organic_conversion_rate_on_page': cvr, 'aov': a},
                 'window': f"{w['days']}d"} if stake is not None else None
        group = 'branded' if r['branded'] else 'non-branded'
        sentence = (f"The {page_label(page)} gets {r['impressions']:,} impressions for '{query}' but a CTR of only "
                    f"{r['ctr'] * 100:.0f} percent. Pages at position {r['position']:.1f} get about {r['expected'] * 100:.0f} percent.")
        out.append(finding('SEO-R02', severity(stake, ctx['revenue'], agree), {'type': 'page', 'id': slug(page), 'label': f"{page_label(page)}, '{query}'"},
                           [ev('ctr', r['ctr'], 'ratio', w, 'search_console', r['expected'], 'threshold'),
                            ev('impressions', r['impressions'], 'count', w, 'search_console'),
                            ev('position', r['position'], 'rank', w, 'search_console'),
                            ev('query_group', group, 'label', w, 'search_console'),
                            ev('organic_conversion_rate_on_page', cvr, 'ratio', w, 'sessions'),
                            ev('aov', a, 'usd', w, 'aggregates/daily'),
                            ev('windows_agreeing', agree, 'count', w, 'search_console', len(wins), 'threshold')],
                           sentence, 'ORG-C21', 'agent_does', money, confidence(agree), w,
                           ctx['page_refs'](page), money_reason=None if money else 'no organic conversion rate for the page'))
    return out


def r03_cannibal(brand, w, ctx):
    wins = sc_windows(brand, w)
    if not wins:
        return [unavailable_finding('SEO-R03', w, ['search_console'], 'Google Search Console',
                                    'Connect Search Console, then pages that compete for one query show here.')]
    by_q = {}
    for r in sc_rows(brand, *wins[0]):
        by_q.setdefault(r['query'], []).append(r)
    out = []
    for q, rows in sorted(by_q.items()):
        if len(rows) < 2:
            continue
        pos = [r['position'] for r in rows]
        if max(pos) - min(pos) > CANNIBAL_SPREAD:
            continue
        out.append(finding('SEO-R03', 'medium', {'type': 'page', 'id': 'q_' + q.replace(' ', '_'), 'label': f"'{q}'"},
                           [ev('pages_ranking', len(rows), 'count', w, 'search_console', 1, 'threshold')]
                           + [ev('position', r['position'], 'rank', w, 'search_console') for r in rows],
                           f"{len(rows)} pages compete for '{q}', splitting the ranking signal.", 'ORG-C27', 'agent_does',
                           None, confidence(1), w, money_reason='no baseline'))
    return out


def r11_tags(brand, w, ctx):
    end = date.fromisoformat(w['ends_on'])
    days = [(end - timedelta(days=k)).isoformat() for k in range(w['days'] - 1, -1, -1)]
    counts = {'session_start': [], 'add_to_cart': [], 'purchase': []}
    for d in days:
        r = funnel(brand, 1, d)
        if r.get('unavailable'):
            for k in counts:
                counts[k].append(0 if 'no sessions match' in (r.get('reason') or '') else None)
            continue
        counts['session_start'].append(r['inputs']['sessions'])
        counts['add_to_cart'].append(r['inputs']['add_to_cart'])
        counts['purchase'].append(r['inputs']['purchase'])
    if all(v is None for v in counts['session_start']):
        return [unavailable_finding('SEO-R11', w, ['sessions'], 'ga4', 'Connect GA4 daily sessions.')]
    out = []
    for event, vals in counts.items():
        run, first = 0, None
        for d, v in zip(days, vals):
            run = run + 1 if v == 0 else 0
            if run == 1:
                first = d
            if run >= ZERO_DAYS:
                med = statistics.median([x for x in vals if x]) if any(vals) else None
                out.append(finding('SEO-R11', 'critical', {'type': 'metric', 'id': event, 'label': f'GA4 {event}'},
                                   [ev(f'{event}_daily', 0, 'count', w, 'sessions', med, 'own_median', '1d')],
                                   f'The {event} tag stopped firing on {first}.', 'MONEY-C20', 'human_assist', None,
                                   confidence(1), w, money_reason='tracking gap: sales still happen, only the count is lost'))
                break
    return out


# ---------------------------------------------------------------- context and run

def context(brand, w):
    a = aov(brand, w)
    av = None if a.get('unavailable') else a['value']
    org = funnel(brand, w['days'], w['ends_on'], channel=ORGANIC)
    by_page = funnel(brand, w['days'], w['ends_on'], channel=ORGANIC, by='landing_page')
    page_cvr = {g['landing_page']: g['conversion_rate'] for g in (by_page.get('groups') or [])}
    all7 = funnel(brand, 7, w['ends_on'])
    b = brain(brand, w['ends_on'])
    site = {}
    for rec in b.records('site_map'):
        v = rec.get('value')
        for it in ([v] if isinstance(v, dict) else v if isinstance(v, list) else []):
            if isinstance(it, dict) and it.get('url'):
                path = '/' + it['url'].split('://', 1)[-1].split('/', 1)[-1]
                site.setdefault(path.rstrip('/') or '/', rec['id'])
    return {
        'aov': av,
        'organic_cvr': None if org.get('unavailable') else org['rates']['conversion_rate'],
        'page_cvr': lambda p: page_cvr.get(p),
        'revenue': net_revenue_est(brand, w, a),
        'revenue_7d': all7['inputs']['purchase'] * av if av and not all7.get('unavailable') else None,
        'page_refs': lambda p: [site[p]] if p in site else [],
        'crawl_ref': next((r['id'] for r in b.records('site_map') if r.get('field') == 'crawl_access'), None),
    }


def run(brand, window=None):
    w = window_of(brand, window)
    ctx = context(brand, w)
    out = []
    out += r01_drop(brand, w, ctx)
    out += r02_ctr(brand, w, ctx)
    out += r03_cannibal(brand, w, ctx)
    out += r11_tags(brand, w, ctx)
    for rule in sorted(UNAVAILABLE):
        refs = [ctx['crawl_ref']] if rule == 'SEO-R12' and ctx['crawl_ref'] else []
        out.append(unavailable_finding(rule, w, brain_refs=refs))
    return sorted(out, key=lambda f: (SEVERITY_ORDER[f['severity']], f['status'] != 'open',
                                      -((f['money_at_stake'] or {}).get('usd') or 0), f['id']))
