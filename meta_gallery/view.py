"""Date-range view engine.

Totals any date range inside the cached one-year window from stored daily
rows, applies campaign exclusions, compares with the previous period and adds
verdicts and fatigue flags. Pure functions over the cache dict. No network.

Rules kept from the first version:
  * Missing purchase values stay None (unavailable), never zero.
  * Period ROAS = total purchase value / total spend.
  * Aggregate totals (daily rows) are kept separate from breakdowns (monthly rows).
  * Each ad keeps its own metrics even when ads share an image or video.
"""
from collections import defaultdict
from datetime import date, timedelta

from .metrics import derive, ratio
from .snapshot import FORMATS, TYPE_LABELS

COLLECTION_SIZE = 30
WATCH_BAND = 0.7          # Watch when ROAS is between 70% of target and target
CUT_SPEND_MULTIPLE = 2.0  # Cut when no purchases after spending 2x target CPA
FATIGUE_RECENT_DAYS = 7
FATIGUE_BASE_DAYS = 21
FATIGUE_CTR_DROP = 0.25
FATIGUE_ROAS_DROP = 0.30
FATIGUE_MIN_RECENT_IMPR = 1000
FATIGUE_MIN_BASE_IMPR = 3000
MAX_KEYWORDS = 20


class ViewError(ValueError):
    pass


def clean_keywords(values):
    out = []
    for v in values or []:
        v = str(v).strip().lower()
        if v and len(v) <= 60 and v not in out:
            out.append(v)
    return out[:MAX_KEYWORDS]


class Engine:
    def __init__(self, cache):
        self.c = cache
        w = cache['meta']['window']
        self.start = date.fromisoformat(w['since'])
        self.end = date.fromisoformat(w['until'])
        self.n_days = (self.end - self.start).days + 1

    # ---- dates -------------------------------------------------------
    def idx(self, iso):
        try:
            d = date.fromisoformat(iso)
        except (TypeError, ValueError):
            raise ViewError(f'Bad date: {iso!r}. Use YYYY-MM-DD.')
        return (d - self.start).days

    def iso(self, i):
        return (self.start + timedelta(days=i)).isoformat()

    def resolve_range(self, since, until):
        a = self.idx(since) if since else self.n_days - 90
        b = self.idx(until) if until else self.n_days - 1
        if a > b:
            raise ViewError('Start date is after end date.')
        if b < 0 or a >= self.n_days:
            raise ViewError(f'Dates must be inside {self.iso(0)} to {self.iso(self.n_days - 1)}.')
        clamped = a < 0 or b >= self.n_days
        return max(a, 0), min(b, self.n_days - 1), clamped

    # ---- totals ------------------------------------------------------
    def sums(self, ad_id, a, b):
        spend = impr = clicks = 0.0
        purchases = value = None
        days = 0
        first = last = None
        for d, s, p, v, im, cl in self.c['daily'].get(ad_id, ()):
            if d < a:
                continue
            if d > b:
                break
            spend += s
            impr += im
            clicks += cl
            if p is not None:
                purchases = (purchases or 0.0) + p
            if v is not None:
                value = (value or 0.0) + v
            if s > 0:
                days += 1
                first = d if first is None else first
                last = d
        m = derive(spend, purchases, value, impr, clicks)
        m['days_active'] = days
        m['first_day'] = self.iso(first) if first is not None else None
        m['last_day'] = self.iso(last) if last is not None else None
        return m

    @staticmethod
    def add_up(metric_list):
        spend = sum(m['spend'] or 0 for m in metric_list)
        impr = sum(m['impressions'] or 0 for m in metric_list)
        clicks = sum(m['link_clicks'] or 0 for m in metric_list)
        values = [m['purchase_value'] for m in metric_list if m['purchase_value'] is not None]
        purch = [m['purchases'] for m in metric_list if m['purchases'] is not None]
        out = derive(spend, sum(purch) if purch else None, sum(values) if values else None, impr, clicks)
        out['ads'] = len(metric_list)
        out['ads_without_reported_value'] = sum(1 for m in metric_list if m['purchase_value'] is None)
        return out

    def excluded(self, ad, keywords, campaign_ids):
        if ad.get('campaign_id') in campaign_ids:
            return 'campaign'
        name = (ad.get('campaign_name') or '').lower()
        for k in keywords:
            if k in name:
                return k
        return None

    # ---- verdicts and fatigue -----------------------------------------
    @staticmethod
    def verdict(m, target_roas, target_cpa):
        if target_roas is None:
            return {'code': 'no_target', 'label': 'No target', 'reason': 'Set a target ROAS to get verdicts.'}
        spend = m['spend'] or 0
        if target_cpa and spend < target_cpa:
            return {'code': 'not_enough_data', 'label': 'Not enough data',
                    'reason': f'Spent less than one target CPA ({target_cpa:,.0f}).'}
        if m['roas'] is None:
            if target_cpa and spend >= CUT_SPEND_MULTIPLE * target_cpa:
                return {'code': 'cut', 'label': 'Cut',
                        'reason': f'No purchases reported after spending {spend / target_cpa:.1f}x target CPA.'}
            return {'code': 'watch', 'label': 'Watch', 'reason': 'No purchases reported yet, spend still below 2x target CPA.'}
        if m['roas'] >= target_roas:
            return {'code': 'scale', 'label': 'Scale', 'reason': f"ROAS {m['roas']:.2f}x is at or above target {target_roas:.2f}x."}
        if m['roas'] >= WATCH_BAND * target_roas:
            return {'code': 'watch', 'label': 'Watch',
                    'reason': f"ROAS {m['roas']:.2f}x is within 30% below target {target_roas:.2f}x."}
        return {'code': 'cut', 'label': 'Cut', 'reason': f"ROAS {m['roas']:.2f}x is more than 30% below target {target_roas:.2f}x."}

    def fatigue(self, ad_id, b):
        r_a, r_b = b - FATIGUE_RECENT_DAYS + 1, b
        b_a, b_b = r_a - FATIGUE_BASE_DAYS, r_a - 1
        recent = self.sums(ad_id, max(r_a, 0), r_b)
        if recent['spend'] <= 0:
            return {'code': 'not_running', 'label': 'Not running', 'reason': 'No spend in the last 7 days of the range.'}
        if b_b < 0:
            return {'code': 'not_enough_data', 'label': 'Too new to judge', 'reason': 'No earlier data to compare with.'}
        base = self.sums(ad_id, max(b_a, 0), b_b)
        out = {'recent': {k: recent[k] for k in ('spend', 'roas', 'link_ctr', 'impressions')},
               'baseline': {k: base[k] for k in ('spend', 'roas', 'link_ctr', 'impressions')},
               'recent_range': [self.iso(max(r_a, 0)), self.iso(r_b)],
               'baseline_range': [self.iso(max(b_a, 0)), self.iso(b_b)]}
        if recent['impressions'] < FATIGUE_MIN_RECENT_IMPR or base['impressions'] < FATIGUE_MIN_BASE_IMPR:
            return dict(out, code='not_enough_data', label='Too little data',
                        reason='Needs 1,000 impressions in the last 7 days and 3,000 in the 21 days before.')
        ctr_drop = None
        if base['link_ctr'] and recent['link_ctr'] is not None:
            ctr_drop = 1 - recent['link_ctr'] / base['link_ctr']
        roas_drop = None
        stopped = False
        if base['roas']:
            if recent['roas'] is not None:
                roas_drop = 1 - recent['roas'] / base['roas']
            else:
                stopped = True
        out['ctr_change'] = -ctr_drop if ctr_drop is not None else None
        out['roas_change'] = -roas_drop if roas_drop is not None else None
        ctr_bad = ctr_drop is not None and ctr_drop >= FATIGUE_CTR_DROP
        roas_bad = stopped or (roas_drop is not None and roas_drop >= FATIGUE_ROAS_DROP)
        if ctr_bad and roas_bad:
            why = 'purchases stopped' if stopped else f'ROAS down {roas_drop * 100:.0f}%'
            return dict(out, code='declining', label='Declining',
                        reason=f'Last 7 days vs the 21 days before: link CTR down {ctr_drop * 100:.0f}%, {why}.')
        if ctr_bad:
            return dict(out, code='ctr_down', label='CTR falling',
                        reason=f'Link CTR down {ctr_drop * 100:.0f}% (last 7 days vs the 21 days before). ROAS has not fallen 30%.')
        if roas_bad:
            why = 'No purchases reported in the last 7 days' if stopped else f'ROAS down {roas_drop * 100:.0f}%'
            return dict(out, code='roas_down', label='ROAS falling', reason=f'{why}. Link CTR is holding.')
        return dict(out, code='stable', label='Stable', reason='No large drop in link CTR or ROAS in the last 7 days.')

    # ---- breakdowns ----------------------------------------------------
    def buckets_for(self, a, b):
        lo, hi = self.iso(a), self.iso(b)
        return [bk for bk in self.c['meta'].get('breakdown_buckets', []) if bk[0] <= hi and bk[1] >= lo]

    def breakdown(self, ad_id, dim, buckets):
        keys = {bk[0] for bk in buckets}
        acc = {}
        for start, _stop, key, s, p, v in self.c['monthly'].get(dim, {}).get(ad_id, ()):
            if start not in keys:
                continue
            x = acc.setdefault(key, {'spend': 0.0, 'purchases': None, 'purchase_value': None})
            x['spend'] += s
            if p is not None:
                x['purchases'] = (x['purchases'] or 0.0) + p
            if v is not None:
                x['purchase_value'] = (x['purchase_value'] or 0.0) + v
        for x in acc.values():
            x['roas'] = ratio(x['purchase_value'], x['spend'])
        return acc

    # ---- main view -----------------------------------------------------
    def view(self, since=None, until=None, keywords=(), campaign_ids=(), targets=None):
        a, b, clamped = self.resolve_range(since, until)
        keywords = clean_keywords(keywords)
        campaign_ids = set(campaign_ids or ())
        length = b - a + 1
        pa, pb = a - length, a - 1
        prev_cover = max(0, pb - max(pa, 0) + 1) if pb >= 0 else 0

        ads = self.c['ads']
        cands, prev_metrics, excl = [], [], defaultdict(lambda: {'ads': 0, 'spend': 0.0, 'matched': None})
        per_ad = {}
        for ad_id, ad in ads.items():
            m = self.sums(ad_id, a, b)
            why = self.excluded(ad, keywords, campaign_ids)
            if why:
                if m['spend'] > 0:
                    e = excl[ad['campaign_id']]
                    e['ads'] += 1
                    e['spend'] += m['spend']
                    e['name'] = ad['campaign_name']
                    e['matched'] = why
                continue
            if prev_cover:
                pm = self.sums(ad_id, max(pa, 0), pb)
                if pm['spend'] > 0:
                    prev_metrics.append(pm)
                per_ad[ad_id] = {'prev': pm}
            if m['spend'] > 0:
                cands.append((ad_id, m))

        cands.sort(key=lambda x: -x[1]['spend'])
        total = self.add_up([m for _, m in cands])
        prev_total = self.add_up(prev_metrics) if prev_cover else None

        t = targets or {}
        target_roas = t.get('roas') or total['roas']
        target_cpa = t.get('cpa') or total['cpa']
        target_info = {'roas': target_roas, 'cpa': target_cpa,
                       'roas_source': 'saved' if t.get('roas') else 'average for these dates',
                       'cpa_source': 'saved' if t.get('cpa') else 'average for these dates'}

        by_type = defaultdict(list)
        for ad_id, m in cands:
            by_type[ads[ad_id]['creative']['type']].append(m)
        by_type_out = {k: dict(self.add_up(v), label=TYPE_LABELS[k]) for k, v in by_type.items()}

        picks = {'all': cands[:COLLECTION_SIZE]}
        for fmt in FORMATS:
            picks[fmt] = [x for x in cands if ads[x[0]]['creative']['type'] == fmt][:COLLECTION_SIZE]
        rank = {ad_id: i for i, (ad_id, _) in enumerate(cands, 1)}

        media = defaultdict(list)
        for ad_id, _ in cands:
            c = ads[ad_id]['creative']
            key = c.get('image_hash') or c.get('video_id')
            if key:
                media[key].append(ad_id)

        buckets = self.buckets_for(a, b)
        selected = list(dict.fromkeys(ad_id for grp in picks.values() for ad_id, _ in grp))
        cand_m = dict(cands)
        out_ads = {}
        for ad_id in selected:
            ad = ads[ad_id]
            m = cand_m[ad_id]
            c = ad['creative']
            key = c.get('image_hash') or c.get('video_id')
            pm = per_ad.get(ad_id, {}).get('prev') if prev_cover == length else None
            out_ads[ad_id] = dict(ad, view={
                'rank_by_spend': rank[ad_id],
                'metrics': m,
                'prev_metrics': pm if pm and pm['spend'] > 0 else None,
                'verdict': self.verdict(m, target_roas, target_cpa),
                'fatigue': self.fatigue(ad_id, b),
                'same_media_ads': [x for x in media.get(key, []) if x != ad_id] if key else [],
                'demographics': {'age': self.breakdown(ad_id, 'age', buckets),
                                 'gender': self.breakdown(ad_id, 'gender', buckets)},
            })

        collections = {}
        for key, grp in picks.items():
            ids = [ad_id for ad_id, _ in grp]
            collections[key] = {'label': TYPE_LABELS[key], 'ad_ids': ids, 'size': len(ids),
                                'available': len(cands) if key == 'all' else len(by_type.get(key, [])),
                                'totals': self.add_up([m for _, m in grp])}

        demo_all = {}
        for dim in ('age', 'gender', 'publisher_platform'):
            acc = {}
            for ad_id, _ in cands:
                for k, x in self.breakdown(ad_id, dim, buckets).items():
                    y = acc.setdefault(k, {'spend': 0.0, 'purchases': None, 'purchase_value': None})
                    y['spend'] += x['spend']
                    if x['purchases'] is not None:
                        y['purchases'] = (y['purchases'] or 0.0) + x['purchases']
                    if x['purchase_value'] is not None:
                        y['purchase_value'] = (y['purchase_value'] or 0.0) + x['purchase_value']
            for y in acc.values():
                y['roas'] = ratio(y['purchase_value'], y['spend'])
            demo_all[dim] = acc

        verdict_counts = defaultdict(int)
        for ad_id in collections['all']['ad_ids']:
            verdict_counts[out_ads[ad_id]['view']['verdict']['code']] += 1

        return {
            'range': {'since': self.iso(a), 'until': self.iso(b), 'days': length, 'clamped': clamped},
            'previous': {'since': self.iso(max(pa, 0)) if prev_cover else None, 'until': self.iso(pb) if prev_cover else None,
                         'days_covered': prev_cover, 'days': length, 'complete': prev_cover == length},
            'totals': total,
            'previous_totals': prev_total,
            'targets': target_info,
            'exclusions': {'keywords': keywords, 'campaign_ids': sorted(campaign_ids),
                           'campaigns': sorted(({'id': k, **v} for k, v in excl.items()), key=lambda x: -x['spend']),
                           'ads': sum(v['ads'] for v in excl.values()),
                           'spend': sum(v['spend'] for v in excl.values())},
            'by_type': by_type_out,
            'collections': collections,
            'verdict_counts_top30': dict(verdict_counts),
            'demographics_buckets': buckets,
            'demographics_all': demo_all,
            'demographics_exact': bool(buckets) and buckets[0][0] >= self.iso(a) and buckets[-1][1] <= self.iso(b),
            'ads': out_ads,
        }

    def campaigns(self):
        acc = {}
        for ad_id, ad in self.c['ads'].items():
            x = acc.setdefault(ad['campaign_id'], {'id': ad['campaign_id'], 'name': ad['campaign_name'], 'spend': 0.0,
                                                   'first_day': None, 'last_day': None})
            m = self.sums(ad_id, 0, self.n_days - 1)
            x['spend'] += m['spend']
            for k, f in (('first_day', min), ('last_day', max)):
                if m[k]:
                    x[k] = m[k] if x[k] is None else f(x[k], m[k])
        return sorted(acc.values(), key=lambda x: -x['spend'])

    def ad_detail(self, ad_id, since=None, until=None, targets=None, keywords=(), campaign_ids=()):
        ad = self.c['ads'].get(ad_id)
        if not ad:
            return None
        a, b, _ = self.resolve_range(since, until)
        m = self.sums(ad_id, a, b)
        length = b - a + 1
        pa, pb = a - length, a - 1
        prev = self.sums(ad_id, pa, pb) if pa >= 0 else None
        buckets = self.buckets_for(a, b)
        lead = max(a - 6, 0)  # 6 days before the range so the 7-day line starts full
        series = {d: r for d, *r in self.c['daily'].get(ad_id, ()) if lead <= d <= b}
        days = []
        for d in range(lead, b + 1):
            s, p, v, im, cl = series.get(d, (0.0, None, None, 0.0, 0.0))
            days.append({'date': self.iso(d), 'in_range': d >= a, 'spend': s, 'purchases': p,
                         'purchase_value': v, 'impressions': im, 'link_clicks': cl})
        t = targets or {}
        total = None
        if not (t.get('roas') and t.get('cpa')):
            total = self.view(self.iso(a), self.iso(b), keywords, campaign_ids)['targets']
        target_roas = t.get('roas') or (total or {}).get('roas')
        target_cpa = t.get('cpa') or (total or {}).get('cpa')
        return dict(ad, detail={
            'range': {'since': self.iso(a), 'until': self.iso(b), 'days': length},
            'metrics': m,
            'prev_metrics': prev if prev and prev['spend'] > 0 else None,
            'previous': {'since': self.iso(pa), 'until': self.iso(pb)} if pa >= 0 else None,
            'verdict': self.verdict(m, target_roas, target_cpa) if m['spend'] > 0 else None,
            'targets': {'roas': target_roas, 'cpa': target_cpa},
            'fatigue': self.fatigue(ad_id, b),
            'breakdowns': {dim: self.breakdown(ad_id, dim, buckets) for dim in ('age', 'gender', 'publisher_platform')},
            'breakdown_buckets': buckets,
            'daily': days,
        })
