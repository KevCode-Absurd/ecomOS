'use strict';
// Date-range engine. Same rules as meta_gallery/view.py:
// missing purchase values stay null (never zero), ROAS = value / spend,
// totals come from daily rows, breakdowns from monthly rows, kept apart.
(function (root) {
  const COLLECTION_SIZE = 30;
  const ROAS_SET_SIZE = 100, ROAS_FLOORS = [2, 1, 0];   // "Top 100 by ROAS" lists with a floor of 2, 1 or 0 purchases
  const WATCH_BAND = 0.7;
  const CUT_SPEND_MULTIPLE = 2.0;
  const RECENT = 7, BASE = 21, CTR_DROP = 0.25, ROAS_DROP = 0.30, MIN_RECENT_IMPR = 1000, MIN_BASE_IMPR = 3000;
  const FORMATS = ['static_image', 'video', 'carousel', 'catalog_dynamic', 'unconfirmed_mixed'];

  const ratio = (n, d, scale = 1) => (n === null || d === null || d === 0 ? null : (n / d) * scale);
  function derive(spend, purchases, value, impr, clicks) {
    return { spend, purchases, purchase_value: value, impressions: impr, link_clicks: clicks,
      roas: ratio(value, spend), cpa: ratio(spend, purchases), link_ctr: ratio(clicks, impr, 100), link_cpc: ratio(spend, clicks) };
  }
  function cleanKeywords(list) {
    const out = [];
    for (const v of list || []) {
      const k = String(v).trim().toLowerCase();
      if (k && k.length <= 60 && !out.includes(k)) out.push(k);
    }
    return out.slice(0, 20);
  }
  const DAY = 86400000;
  const toMs = (iso) => Date.UTC(+iso.slice(0, 4), +iso.slice(5, 7) - 1, +iso.slice(8, 10));

  class Engine {
    constructor(cache) {
      this.c = cache;
      this.start = toMs(cache.meta.window.since);
      this.nDays = (toMs(cache.meta.window.until) - this.start) / DAY + 1;
      this.labels = cache.meta.format_labels;
    }
    idx(iso) {
      if (!/^\d{4}-\d{2}-\d{2}$/.test(iso || '')) throw new Error(`Bad date: ${iso}`);
      return Math.round((toMs(iso) - this.start) / DAY);
    }
    iso(i) { return new Date(this.start + i * DAY).toISOString().slice(0, 10); }
    resolveRange(since, until) {
      const a = this.idx(since), b = this.idx(until);
      if (a > b) throw new Error('Start date is after end date.');
      if (b < 0 || a >= this.nDays) throw new Error(`Pick dates between ${this.iso(0)} and ${this.iso(this.nDays - 1)}.`);
      return [Math.max(a, 0), Math.min(b, this.nDays - 1)];
    }

    sums(adId, a, b) {
      let spend = 0, impr = 0, clicks = 0, purchases = null, value = null, days = 0, first = null, last = null;
      for (const [d, s, p, v, im, cl] of this.c.daily[adId] || []) {
        if (d < a) continue;
        if (d > b) break;
        spend += s; impr += im; clicks += cl;
        if (p !== null) purchases = (purchases || 0) + p;
        if (v !== null) value = (value || 0) + v;
        if (s > 0) { days += 1; if (first === null) first = d; last = d; }
      }
      const m = derive(spend, purchases, value, impr, clicks);
      m.days_active = days;
      m.first_day = first === null ? null : this.iso(first);
      m.last_day = last === null ? null : this.iso(last);
      return m;
    }
    static addUp(list) {
      const sum = (k) => list.reduce((t, m) => t + (m[k] || 0), 0);
      const vals = list.filter((m) => m.purchase_value !== null);
      const purch = list.filter((m) => m.purchases !== null);
      const out = derive(sum('spend'), purch.length ? purch.reduce((t, m) => t + m.purchases, 0) : null,
        vals.length ? vals.reduce((t, m) => t + m.purchase_value, 0) : null, sum('impressions'), sum('link_clicks'));
      out.ads = list.length;
      out.ads_without_reported_value = list.length - vals.length;
      return out;
    }
    excluded(ad, keywords, campIds) {
      if (campIds.has(ad.campaign_id)) return 'campaign';
      const name = (ad.campaign_name || '').toLowerCase();
      for (const k of keywords) if (name.includes(k)) return k;
      return null;
    }

    static verdict(m, T, C) {
      if (!T) return { code: 'no_target', label: 'No target', reason: 'Set a target ROAS to get verdicts.' };
      const spend = m.spend || 0;
      const inr = (v) => Math.round(v).toLocaleString('en-IN');
      if (C && spend < C) return { code: 'not_enough_data', label: 'Not enough data', reason: `Spent less than one target CPA (₹${inr(C)}).` };
      if (m.roas === null) {
        if (C && spend >= CUT_SPEND_MULTIPLE * C) return { code: 'cut', label: 'Cut', reason: `No purchases reported after spending ${(spend / C).toFixed(1)}x target CPA.` };
        return { code: 'watch', label: 'Watch', reason: 'No purchases reported yet, spend still below 2x target CPA.' };
      }
      if (m.roas >= T) return { code: 'scale', label: 'Scale', reason: `ROAS ${m.roas.toFixed(2)}x is at or above target ${T.toFixed(2)}x.` };
      if (m.roas >= WATCH_BAND * T) return { code: 'watch', label: 'Watch', reason: `ROAS ${m.roas.toFixed(2)}x is within 30% below target ${T.toFixed(2)}x.` };
      return { code: 'cut', label: 'Cut', reason: `ROAS ${m.roas.toFixed(2)}x is more than 30% below target ${T.toFixed(2)}x.` };
    }

    fatigue(adId, b) {
      const ra = b - RECENT + 1, ba = ra - BASE, bb = ra - 1;
      const recent = this.sums(adId, Math.max(ra, 0), b);
      if (recent.spend <= 0) return { code: 'not_running', label: 'Not running', reason: 'No spend in the last 7 days of the range.' };
      if (bb < 0) return { code: 'not_enough_data', label: 'Too new to judge', reason: 'No earlier data to compare with.' };
      const base = this.sums(adId, Math.max(ba, 0), bb);
      const pick = (m) => ({ spend: m.spend, roas: m.roas, link_ctr: m.link_ctr, impressions: m.impressions });
      const out = { recent: pick(recent), baseline: pick(base), recent_range: [this.iso(Math.max(ra, 0)), this.iso(b)], baseline_range: [this.iso(Math.max(ba, 0)), this.iso(bb)] };
      if (recent.impressions < MIN_RECENT_IMPR || base.impressions < MIN_BASE_IMPR) {
        return { ...out, code: 'not_enough_data', label: 'Too little data', reason: 'Needs 1,000 impressions in the last 7 days and 3,000 in the 21 days before.' };
      }
      const ctrDrop = base.link_ctr && recent.link_ctr !== null ? 1 - recent.link_ctr / base.link_ctr : null;
      let roasDrop = null, stopped = false;
      if (base.roas) { if (recent.roas !== null) roasDrop = 1 - recent.roas / base.roas; else stopped = true; }
      const ctrBad = ctrDrop !== null && ctrDrop >= CTR_DROP;
      const roasBad = stopped || (roasDrop !== null && roasDrop >= ROAS_DROP);
      const pct = (x) => Math.round(x * 100);
      if (ctrBad && roasBad) return { ...out, code: 'declining', label: 'Declining', reason: `Last 7 days vs the 21 days before: link CTR down ${pct(ctrDrop)}%, ${stopped ? 'purchases stopped' : `ROAS down ${pct(roasDrop)}%`}.` };
      if (ctrBad) return { ...out, code: 'ctr_down', label: 'CTR falling', reason: `Link CTR down ${pct(ctrDrop)}% (last 7 days vs the 21 days before). ROAS has not fallen 30%.` };
      if (roasBad) return { ...out, code: 'roas_down', label: 'ROAS falling', reason: `${stopped ? 'No purchases reported in the last 7 days' : `ROAS down ${pct(roasDrop)}%`}. Link CTR is holding.` };
      return { ...out, code: 'stable', label: 'Stable', reason: 'No large drop in link CTR or ROAS in the last 7 days.' };
    }

    bucketsFor(a, b) {
      const lo = this.iso(a), hi = this.iso(b);
      return (this.c.meta.breakdown_buckets || []).filter((bk) => bk[0] <= hi && bk[1] >= lo);
    }
    breakdown(adId, dim, buckets) {
      const keys = new Set(buckets.map((bk) => bk[0]));
      const acc = {};
      for (const [start, , key, s, p, v] of ((this.c.monthly[dim] || {})[adId] || [])) {
        if (!keys.has(start)) continue;
        const x = acc[key] || (acc[key] = { spend: 0, purchases: null, purchase_value: null });
        x.spend += s;
        if (p !== null) x.purchases = (x.purchases || 0) + p;
        if (v !== null) x.purchase_value = (x.purchase_value || 0) + v;
      }
      for (const x of Object.values(acc)) x.roas = ratio(x.purchase_value, x.spend);
      return acc;
    }

    view(since, until, keywords, campaignIds, targets) {
      const [a, b] = this.resolveRange(since, until);
      keywords = cleanKeywords(keywords);
      const campIds = new Set(campaignIds || []);
      const length = b - a + 1, pa = a - length, pb = a - 1;
      const prevCover = pb >= 0 ? Math.max(0, pb - Math.max(pa, 0) + 1) : 0;
      const ads = this.c.ads;
      const cands = [], prevList = [], prevOf = {}, excl = {};
      for (const [id, ad] of Object.entries(ads)) {
        const m = this.sums(id, a, b);
        const why = this.excluded(ad, keywords, campIds);
        if (why) {
          if (m.spend > 0) {
            const e = excl[ad.campaign_id] || (excl[ad.campaign_id] = { id: ad.campaign_id, name: ad.campaign_name, ads: 0, spend: 0, matched: why });
            e.ads += 1; e.spend += m.spend; e.matched = why;
          }
          continue;
        }
        if (prevCover) {
          const pm = this.sums(id, Math.max(pa, 0), pb);
          if (pm.spend > 0) prevList.push(pm);
          prevOf[id] = pm;
        }
        if (m.spend > 0) cands.push([id, m]);
      }
      cands.sort((x, y) => y[1].spend - x[1].spend);
      const total = Engine.addUp(cands.map((x) => x[1]));
      const prevTotal = prevCover ? Engine.addUp(prevList) : null;
      const t = targets || {};
      const T = t.roas || total.roas, C = t.cpa || total.cpa;
      const byType = {};
      for (const [id, m] of cands) (byType[ads[id].creative.type] || (byType[ads[id].creative.type] = [])).push(m);
      const byTypeOut = {};
      for (const [k, v] of Object.entries(byType)) byTypeOut[k] = { ...Engine.addUp(v), label: this.labels[k] || k };
      const picks = { all: cands.slice(0, COLLECTION_SIZE) };
      for (const f of FORMATS) picks[f] = cands.filter(([id]) => ads[id].creative.type === f).slice(0, COLLECTION_SIZE);
      // Second set of lists: the best ROAS, with a floor on purchases. Spend is the tie-break.
      // Ads with no reported value go last (unavailable, not zero). Keys look like roas2:static_image.
      const roasOrder = cands.slice().sort((x, y) => (y[1].roas ?? -1) - (x[1].roas ?? -1) || y[1].spend - x[1].spend);
      const roasPool = {};
      for (const fl of ROAS_FLOORS) {
        roasPool[fl] = fl ? roasOrder.filter(([, m]) => m.roas !== null && (m.purchases || 0) >= fl) : roasOrder;
        // All formats: the top 100, plus every single image ad with a reported ROAS even when it falls outside the 100.
        const top = roasPool[fl].slice(0, ROAS_SET_SIZE), inTop = new Set(top.map(([id]) => id));
        const extraImg = roasPool[fl].filter(([id, m]) => !inTop.has(id) && ads[id].creative.type === 'static_image' && m.roas !== null);
        picks[`roas${fl}:all`] = roasPool[fl].filter(([id]) => inTop.has(id) || extraImg.some(([x]) => x === id));
        roasPool['extra' + fl] = extraImg.length;
        for (const f of FORMATS) picks[`roas${fl}:${f}`] = roasPool[fl].filter(([id]) => ads[id].creative.type === f).slice(0, ROAS_SET_SIZE);
      }
      const rank = {};
      cands.forEach(([id], i) => { rank[id] = i + 1; });
      const media = {};
      for (const [id] of cands) {
        const c = ads[id].creative, key = c.image_hash || c.video_id;
        if (key) (media[key] || (media[key] = [])).push(id);
      }
      const buckets = this.bucketsFor(a, b);
      const candM = Object.fromEntries(cands);
      const selected = [...new Set(Object.values(picks).flat().map((x) => x[0]))];
      const outAds = {};
      for (const id of selected) {
        const ad = ads[id], m = candM[id], c = ad.creative, key = c.image_hash || c.video_id;
        const pm = prevCover === length ? prevOf[id] : null;
        outAds[id] = { ...ad, view: {
          rank_by_spend: rank[id], metrics: m, prev_metrics: pm && pm.spend > 0 ? pm : null,
          verdict: Engine.verdict(m, T, C), fatigue: this.fatigue(id, b),
          same_media_ads: key ? (media[key] || []).filter((x) => x !== id) : [],
          demographics: { age: this.breakdown(id, 'age', buckets), gender: this.breakdown(id, 'gender', buckets) },
        } };
      }
      const collections = {};
      for (const [key, grp] of Object.entries(picks)) {
        const rm = /^roas(\d):(.+)$/.exec(key), f = rm ? rm[2] : key, fl = rm ? Number(rm[1]) : 0;
        collections[key] = { label: this.labels[f] || f, ad_ids: grp.map((x) => x[0]), size: grp.length, by: rm ? 'roas' : 'spend',
          limit: rm ? ROAS_SET_SIZE : COLLECTION_SIZE, min_purchases: fl, extra_images: rm && f === 'all' ? roasPool['extra' + fl] : 0,
          available: rm ? (f === 'all' ? roasPool[fl].length : roasPool[fl].filter(([id]) => ads[id].creative.type === f).length) : f === 'all' ? cands.length : (byType[f] || []).length,
          totals: Engine.addUp(grp.map((x) => x[1])) };
      }
      const demoAll = {};
      for (const dim of ['age', 'gender', 'publisher_platform']) {
        const acc = {};
        for (const [id] of cands) {
          for (const [k, x] of Object.entries(this.breakdown(id, dim, buckets))) {
            const y = acc[k] || (acc[k] = { spend: 0, purchases: null, purchase_value: null });
            y.spend += x.spend;
            if (x.purchases !== null) y.purchases = (y.purchases || 0) + x.purchases;
            if (x.purchase_value !== null) y.purchase_value = (y.purchase_value || 0) + x.purchase_value;
          }
        }
        for (const y of Object.values(acc)) y.roas = ratio(y.purchase_value, y.spend);
        demoAll[dim] = acc;
      }
      const exclList = Object.values(excl).sort((x, y) => y.spend - x.spend);
      return {
        range: { since: this.iso(a), until: this.iso(b), days: length },
        previous: { since: prevCover ? this.iso(Math.max(pa, 0)) : null, until: prevCover ? this.iso(pb) : null, days_covered: prevCover, days: length, complete: prevCover === length },
        totals: total, previous_totals: prevTotal,
        targets: { roas: T, cpa: C, roas_source: t.roas ? 'saved' : 'average for these dates', cpa_source: t.cpa ? 'saved' : 'average for these dates' },
        exclusions: { keywords, campaign_ids: [...campIds].sort(), campaigns: exclList, ads: exclList.reduce((s, x) => s + x.ads, 0), spend: exclList.reduce((s, x) => s + x.spend, 0) },
        by_type: byTypeOut, collections, demographics_buckets: buckets, demographics_all: demoAll,
        demographics_exact: buckets.length > 0 && buckets[0][0] >= this.iso(a) && buckets[buckets.length - 1][1] <= this.iso(b),
        ads: outAds,
      };
    }

    campaigns() {
      const acc = {};
      for (const [id, ad] of Object.entries(this.c.ads)) {
        const x = acc[ad.campaign_id] || (acc[ad.campaign_id] = { id: ad.campaign_id, name: ad.campaign_name, spend: 0, first_day: null, last_day: null });
        const m = this.sums(id, 0, this.nDays - 1);
        x.spend += m.spend;
        if (m.first_day && (!x.first_day || m.first_day < x.first_day)) x.first_day = m.first_day;
        if (m.last_day && (!x.last_day || m.last_day > x.last_day)) x.last_day = m.last_day;
      }
      return Object.values(acc).sort((p, q) => q.spend - p.spend);
    }

    adDetail(adId, since, until, targets) {
      const ad = this.c.ads[adId];
      if (!ad) return null;
      const [a, b] = this.resolveRange(since, until);
      const m = this.sums(adId, a, b);
      const length = b - a + 1, pa = a - length, pb = a - 1;
      const prev = pa >= 0 ? this.sums(adId, pa, pb) : null;
      const buckets = this.bucketsFor(a, b);
      const lead = Math.max(a - 6, 0);
      const series = new Map((this.c.daily[adId] || []).filter((r) => r[0] >= lead && r[0] <= b).map((r) => [r[0], r]));
      const days = [];
      for (let d = lead; d <= b; d++) {
        const r = series.get(d) || [d, 0, null, null, 0, 0];
        days.push({ date: this.iso(d), in_range: d >= a, spend: r[1], purchases: r[2], purchase_value: r[3], impressions: r[4], link_clicks: r[5] });
      }
      return { ...ad, detail: {
        range: { since: this.iso(a), until: this.iso(b), days: length }, metrics: m,
        prev_metrics: prev && prev.spend > 0 ? prev : null, previous: pa >= 0 ? { since: this.iso(pa), until: this.iso(pb) } : null,
        verdict: m.spend > 0 ? Engine.verdict(m, targets.roas, targets.cpa) : null, targets,
        fatigue: this.fatigue(adId, b),
        breakdowns: Object.fromEntries(['age', 'gender', 'publisher_platform'].map((dim) => [dim, this.breakdown(adId, dim, buckets)])),
        breakdown_buckets: buckets, daily: days,
      } };
    }

    // ---------- insights ----------
    // Ads that pass the exclusions, as a Set of ids.
    included(keywords, campaignIds) {
      const kw = cleanKeywords(keywords), camp = new Set(campaignIds || []);
      return new Set(Object.entries(this.c.ads).filter(([, ad]) => !this.excluded(ad, kw, camp)).map(([id]) => id));
    }

    // Account totals per day for included ads, plus spend of excluded ads.
    dailySeries(keywords, campaignIds) {
      const inc = this.included(keywords, campaignIds);
      const n = this.nDays;
      const s = { spend: new Float64Array(n), value: new Float64Array(n), purch: new Float64Array(n), impr: new Float64Array(n), clicks: new Float64Array(n), excl: new Float64Array(n), reported: new Uint8Array(n) };
      for (const [id, rows] of Object.entries(this.c.daily)) {
        const inside = inc.has(id);
        for (const [d, sp, p, v, im, cl] of rows) {
          if (!inside) { s.excl[d] += sp; continue; }
          s.spend[d] += sp; s.impr[d] += im; s.clicks[d] += cl;
          if (v !== null) { s.value[d] += v; s.reported[d] = 1; }
          if (p !== null) s.purch[d] += p;
        }
      }
      return s;
    }

    // Weeks start on Monday. Covers the whole stored year.
    weekly(keywords, campaignIds) {
      const s = this.dailySeries(keywords, campaignIds);
      const weeks = [];
      let cur = null;
      for (let d = 0; d < this.nDays; d++) {
        const dow = new Date(this.start + d * DAY).getUTCDay();
        if (!cur || dow === 1) { cur = { start: this.iso(d), end: this.iso(d), a: d, b: d, spend: 0, value: 0, purch: 0, excl: 0, reported: false }; weeks.push(cur); }
        cur.end = this.iso(d); cur.b = d;
        cur.spend += s.spend[d]; cur.value += s.value[d]; cur.purch += s.purch[d]; cur.excl += s.excl[d];
        if (s.reported[d]) cur.reported = true;
      }
      for (const w of weeks) { w.roas = w.reported && w.spend ? w.value / w.spend : null; w.days = w.b - w.a + 1; }
      return weeks;
    }

    dayOfWeek(since, until, keywords, campaignIds) {
      const [a, b] = this.resolveRange(since, until);
      const s = this.dailySeries(keywords, campaignIds);
      const names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
      const out = names.map((n) => ({ key: n, days: 0, spend: 0, value: 0, purchases: 0, reported: false }));
      for (let d = a; d <= b; d++) {
        const o = out[new Date(this.start + d * DAY).getUTCDay()];
        o.days += 1; o.spend += s.spend[d]; o.value += s.value[d]; o.purchases += s.purch[d];
        if (s.reported[d]) o.reported = true;
      }
      for (const o of out) { o.roas = o.reported && o.spend ? o.value / o.spend : null; o.spend_per_day = o.days ? o.spend / o.days : 0; }
      return [...out.slice(1), out[0]];
    }

    // Platform split per stored month (breakdown rows), for included ads.
    platformByMonth(keywords, campaignIds) {
      const inc = this.included(keywords, campaignIds);
      const months = {};
      for (const [id, rows] of Object.entries(this.c.monthly.publisher_platform || {})) {
        if (!inc.has(id)) continue;
        for (const [start, stop, key, s, , v] of rows) {
          const m = months[start] || (months[start] = { start, stop, rows: {} });
          const x = m.rows[key] || (m.rows[key] = { spend: 0, value: 0, reported: false });
          x.spend += s;
          if (v !== null) { x.value += v; x.reported = true; }
        }
      }
      return Object.values(months).sort((p, q) => (p.start < q.start ? -1 : 1));
    }

    // Spend, value and ROAS by campaign and ad set for the range, plus the previous period.
    campaignRollup(view) {
      const out = {};
      const [a, b] = this.resolveRange(view.range.since, view.range.until);
      const len = b - a + 1, pa = a - len, pb = a - 1, prevOk = view.previous.complete;
      const inc = this.included(view.exclusions.keywords, view.exclusions.campaign_ids);
      for (const id of inc) {
        const ad = this.c.ads[id];
        const m = this.sums(id, a, b);
        const pm = prevOk ? this.sums(id, pa, pb) : null;
        if (m.spend <= 0 && !(pm && pm.spend > 0)) continue;
        const c = out[ad.campaign_id] || (out[ad.campaign_id] = { id: ad.campaign_id, name: ad.campaign_name, cur: [], prev: [], adsets: {} });
        const s = c.adsets[ad.adset_id] || (c.adsets[ad.adset_id] = { id: ad.adset_id, name: ad.adset_name, cur: [], prev: [], ads: [] });
        if (m.spend > 0) { c.cur.push(m); s.cur.push(m); s.ads.push(id); }
        if (pm && pm.spend > 0) { c.prev.push(pm); s.prev.push(pm); }
      }
      const T = view.targets.roas, C = view.targets.cpa;
      const fin = (x) => {
        x.metrics = Engine.addUp(x.cur);
        x.prev_metrics = prevOk && x.prev.length ? Engine.addUp(x.prev) : null;
        x.verdict = x.metrics.spend > 0 ? Engine.verdict(x.metrics, T, C) : null;
        delete x.cur; delete x.prev;
        return x;
      };
      return Object.values(out).map((c) => { fin(c); c.adsets = Object.values(c.adsets).map(fin).sort((p, q) => q.metrics.spend - p.metrics.spend); return c; })
        .filter((c) => c.metrics.spend > 0).sort((p, q) => q.metrics.spend - p.metrics.spend);
    }

    // Spend and ROAS by theme tag for every ad that spent in the range.
    themes(view) {
      const [a, b] = this.resolveRange(view.range.since, view.range.until);
      const inc = this.included(view.exclusions.keywords, view.exclusions.campaign_ids);
      const dims = { angle: {}, product: {}, hook: {} };
      for (const id of inc) {
        const ad = this.c.ads[id];
        const m = this.sums(id, a, b);
        if (m.spend <= 0 || !ad.tags) continue;
        for (const dim of Object.keys(dims)) {
          const t = ad.tags[dim];
          const g = dims[dim][t.code] || (dims[dim][t.code] = { code: t.code, label: t.label, list: [], top: null });
          g.list.push(m);
          if (!g.top || m.spend > g.top.spend) g.top = { id, name: ad.name, spend: m.spend, roas: m.roas };
        }
      }
      const res = {};
      for (const [dim, groups] of Object.entries(dims)) {
        res[dim] = Object.values(groups).map((g) => ({ code: g.code, label: g.label, top: g.top, ...Engine.addUp(g.list) })).sort((p, q) => q.spend - p.spend);
      }
      return res;
    }

    // Video metrics for one ad (or null when the ad has no video rows) over a day range.
    videoSums(adId, a, b) {
      const rows = (this.c.video || {})[adId];
      if (!rows) return null;
      let spend = 0, impr = 0, s3 = 0, s3ok = true, thru = 0, p25 = 0, p50 = 0, p75 = 0, p100 = 0, watch = 0, watchOk = true, starts = 0, days = 0;
      for (const [d, sp, im, v3, th, q1, q2, q3, q4, w, st] of rows) {
        if (d < a || d > b) continue;
        days += 1; spend += sp; impr += im; thru += th; p25 += q1; p50 += q2; p75 += q3; p100 += q4; starts += st;
        if (v3 === null) { if (sp > 0) s3ok = false; } else s3 += v3;
        if (w === null) watchOk = false; else watch += w;
      }
      if (!days) return null;
      const three = s3ok ? s3 : null;
      return { spend, impressions: impr, plays_3s: three, thruplays: thru, starts,
        hook_rate: ratio(three, impr, 100), hold_rate: ratio(thru, three, 100),
        avg_watch: watchOk ? ratio(watch, starts) : null,
        // Completion is measured against video starts. Starts ÷ impressions shows how often the video was
        // actually served; flexible creatives often show a still image instead.
        video_share: ratio(starts, impr, 100),
        p25: ratio(p25, starts, 100), p50: ratio(p50, starts, 100), p75: ratio(p75, starts, 100), p100: ratio(p100, starts, 100) };
    }

    videoTable(view) {
      const [a, b] = this.resolveRange(view.range.since, view.range.until);
      const inc = this.included(view.exclusions.keywords, view.exclusions.campaign_ids);
      const rows = [], all = { spend: 0, impr: 0, s3: 0, thru: 0 };
      for (const id of inc) {
        const v = this.videoSums(id, a, b);
        if (!v || v.spend <= 0) continue;
        const m = this.sums(id, a, b);
        v.mostly_image = v.video_share !== null && v.video_share < 20;
        rows.push({ id, name: this.c.ads[id].name, campaign: this.c.ads[id].campaign_name, video: v, metrics: m });
        if (!v.mostly_image && v.plays_3s !== null) { all.spend += v.spend; all.impr += v.impressions; all.thru += v.thruplays; all.s3 += v.plays_3s; }
      }
      rows.sort((p, q) => q.metrics.spend - p.metrics.spend);
      return { rows, avg: { hook_rate: ratio(all.s3, all.impr, 100), hold_rate: ratio(all.thru, all.s3, 100) } };
    }

    // Launch, peak and fatigue for one ad across the whole stored year.
    lifecycle(adId, minSpend7) {
      const rows = this.c.daily[adId] || [];
      if (!rows.length) return null;
      const byDay = new Map(rows.map((r) => [r[0], r]));
      const first = rows.find((r) => r[1] > 0), last = [...rows].reverse().find((r) => r[1] > 0);
      if (!first) return null;
      let peak = null, fatigue = null;
      const roll = [];
      for (let d = first[0]; d <= last[0]; d++) {
        let sp = 0, v = 0, rep = false;
        for (let k = d - 6; k <= d; k++) { const r = byDay.get(k); if (r) { sp += r[1]; if (r[3] !== null) { v += r[3]; rep = true; } } }
        const ro = sp >= minSpend7 ? (rep ? v / sp : 0) : null;
        roll.push([d, ro, sp]);
        if (ro !== null && (!peak || ro > peak.roas)) peak = { day: d, roas: ro };
      }
      if (peak) {
        for (const [d, ro] of roll) if (d > peak.day && ro !== null && ro < peak.roas * 0.5) { fatigue = { day: d, roas: ro }; break; }
      }
      const tot = this.sums(adId, 0, this.nDays - 1);
      return { first_day: this.iso(first[0]), last_day: this.iso(last[0]), days_live: tot.days_active,
        span_days: last[0] - first[0] + 1, still_running: last[0] >= this.nDays - 3,
        peak_day: peak ? this.iso(peak.day) : null, peak_roas: peak ? peak.roas : null, days_to_peak: peak ? peak.day - first[0] : null,
        fatigue_day: fatigue ? this.iso(fatigue.day) : null, days_to_fatigue: fatigue ? fatigue.day - first[0] : null,
        lifetime: tot, min_spend_7d: minSpend7 };
    }

    lifecycleSummary(view) {
      const inc = this.included(view.exclusions.keywords, view.exclusions.campaign_ids);
      const year = Engine.addUp([...inc].map((id) => this.sums(id, 0, this.nDays - 1)).filter((m) => m.spend > 0));
      const cpa = year.cpa || 5000;
      const minSpend7 = cpa / 2;
      const byFormat = {}, relaunch = [];
      for (const id of inc) {
        const lc = this.lifecycle(id, minSpend7);
        if (!lc || lc.lifetime.spend < cpa) continue;
        const f = this.c.ads[id].creative.type;
        const g = byFormat[f] || (byFormat[f] = { format: this.labels[f] || f, ads: 0, peak: [], fatigue: [], live: [] });
        g.ads += 1; g.live.push(lc.days_live);
        if (lc.days_to_peak !== null) g.peak.push(lc.days_to_peak);
        if (lc.days_to_fatigue !== null) g.fatigue.push(lc.days_to_fatigue);
        const l = lc.lifetime;
        if (!lc.still_running && l.roas !== null && year.roas && l.roas >= year.roas * 1.2 && l.spend >= 3 * cpa && this.nDays - 1 - this.idx(lc.last_day) >= 21) {
          relaunch.push({ id, name: this.c.ads[id].name, format: this.labels[f] || f, campaign: this.c.ads[id].campaign_name, ...lc });
        }
      }
      const med = (xs) => { if (!xs.length) return null; const s = [...xs].sort((p, q) => p - q); const m = Math.floor(s.length / 2); return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2; };
      return { year_roas: year.roas, cpa, min_spend_7d: minSpend7,
        formats: Object.values(byFormat).map((g) => ({ format: g.format, ads: g.ads, median_days_live: med(g.live), median_days_to_peak: med(g.peak), median_days_to_fatigue: med(g.fatigue), fatigued: g.fatigue.length })).sort((p, q) => q.ads - p.ads),
        relaunch: relaunch.sort((p, q) => q.lifetime.purchase_value - p.lifetime.purchase_value).slice(0, 12) };
    }

    // Days in the range where account spend or ROAS moved sharply against the 14 days before.
    anomalies(view) {
      const [a, b] = this.resolveRange(view.range.since, view.range.until);
      const kw = view.exclusions.keywords, camp = view.exclusions.campaign_ids;
      const s = this.dailySeries(kw, camp);
      const inc = this.included(kw, camp);
      const med = (xs) => { const t = xs.filter((x) => x !== null).sort((p, q) => p - q); if (!t.length) return null; const m = Math.floor(t.length / 2); return t.length % 2 ? t[m] : (t[m - 1] + t[m]) / 2; };
      const out = [];
      for (let d = Math.max(a, 14); d <= b; d++) {
        const prevSpend = [], prevRoas = [];
        for (let k = d - 14; k < d; k++) { prevSpend.push(s.spend[k]); prevRoas.push(s.reported[k] && s.spend[k] > 0 ? s.value[k] / s.spend[k] : null); }
        const ms = med(prevSpend), mr = med(prevRoas);
        const sp = s.spend[d], ro = s.reported[d] && sp > 0 ? s.value[d] / sp : null;
        const flags = [];
        if (ms && ms > 0) { const ch = (sp - ms) / ms; if (Math.abs(ch) >= 0.5) flags.push({ kind: 'spend', change: ch, now: sp, usual: ms }); }
        if (mr && ro !== null && sp >= (ms || 0) * 0.3) { const ch = (ro - mr) / mr; if (Math.abs(ch) >= 0.5) flags.push({ kind: 'roas', change: ch, now: ro, usual: mr }); }
        if (!flags.length) continue;
        const drivers = [];
        for (const id of inc) {
          const rows = this.c.daily[id];
          if (!rows) continue;
          let today = 0, base = 0;
          for (const r of rows) { if (r[0] === d) today = r[1]; else if (r[0] >= d - 14 && r[0] < d) base += r[1]; }
          const diff = today - base / 14;
          if (Math.abs(diff) > 0) drivers.push({ id, name: this.c.ads[id].name, today, usual: base / 14, diff });
        }
        drivers.sort((p, q) => Math.abs(q.diff) - Math.abs(p.diff));
        out.push({ date: this.iso(d), flags, drivers: drivers.slice(0, 3), size: Math.max(...flags.map((f) => Math.abs(f.change))) });
      }
      return out.sort((p, q) => q.size - p.size).slice(0, 12).sort((p, q) => (p.date < q.date ? 1 : -1));
    }

    // Move part of the running Cut ads' daily spend to running Scale ads.
    budgetShift(view, share, haircut) {
      const [, b] = this.resolveRange(view.range.since, view.range.until);
      const ra = Math.max(b - 6, 0);
      const cut = [], scale = [];
      for (const id of view.collections.all.ad_ids) {
        const ad = view.ads[id];
        const recent = this.sums(id, ra, b);
        if (recent.spend <= 0) continue;
        const row = { id, name: ad.name, daily: recent.spend / (b - ra + 1), roas: ad.view.metrics.roas, spend: ad.view.metrics.spend };
        if (ad.view.verdict.code === 'cut') cut.push(row);
        if (ad.view.verdict.code === 'scale') scale.push(row);
      }
      const cutDaily = cut.reduce((t, r) => t + r.daily, 0), scaleDaily = scale.reduce((t, r) => t + r.daily, 0);
      const cutValue = cut.reduce((t, r) => t + r.daily * (r.roas || 0), 0);
      const scaleValue = scale.reduce((t, r) => t + r.daily * (r.roas || 0), 0);
      const cutRoas = cutDaily ? cutValue / cutDaily : null, scaleRoas = scaleDaily ? scaleValue / scaleDaily : null;
      const moved = cutDaily * share;
      const gain = scaleRoas !== null && cutRoas !== null ? moved * (scaleRoas * haircut - cutRoas) : null;
      for (const r of cut) r.new_daily = r.daily * (1 - share);
      for (const r of scale) r.new_daily = r.daily + (scaleDaily ? moved * (r.daily / scaleDaily) : 0);
      return { cut, scale, cut_daily: cutDaily, scale_daily: scaleDaily, cut_roas: cutRoas, scale_roas: scaleRoas, moved_daily: moved, value_gain_daily: gain, value_gain_30d: gain === null ? null : gain * 30, share, haircut, window: [this.iso(ra), this.iso(b)] };
    }

    // Spend and ROAS by format x age and format x gender, from the monthly breakdown rows.
    formatAudience(view) {
      const [a, b] = this.resolveRange(view.range.since, view.range.until);
      const buckets = this.bucketsFor(a, b);
      const inc = this.included(view.exclusions.keywords, view.exclusions.campaign_ids);
      const out = { buckets, age: {}, gender: {} };
      for (const id of inc) {
        if (this.sums(id, a, b).spend <= 0) continue;
        const f = this.c.ads[id].creative.type;
        for (const dim of ['age', 'gender']) {
          for (const [k, x] of Object.entries(this.breakdown(id, dim, buckets))) {
            const row = out[dim][f] || (out[dim][f] = {});
            const c = row[k] || (row[k] = { spend: 0, value: null, purchases: null });
            c.spend += x.spend;
            if (x.purchase_value !== null) c.value = (c.value || 0) + x.purchase_value;
            if (x.purchases !== null) c.purchases = (c.purchases || 0) + x.purchases;
          }
        }
      }
      for (const dim of ['age', 'gender']) for (const row of Object.values(out[dim])) for (const c of Object.values(row)) c.roas = ratio(c.value, c.spend);
      return out;
    }

    // The weekly action plan: concrete moves with the numbers behind them.
    opportunities(view) {
      const [, b] = this.resolveRange(view.range.since, view.range.until);
      const a30 = Math.max(0, b - 29), a7 = Math.max(0, b - 6);
      const inc = this.included(view.exclusions.keywords, view.exclusions.campaign_ids);
      const rows = [];
      for (const id of inc) {
        const m30 = this.sums(id, a30, b);
        if (m30.spend <= 0) continue;
        rows.push({ id, m30, m7: this.sums(id, a7, b) });
      }
      const acct30 = Engine.addUp(rows.map((r) => r.m30)), acct7 = Engine.addUp(rows.map((r) => r.m7));
      const T = view.targets.roas || acct30.roas || 0, C = view.targets.cpa || acct30.cpa || 0;
      const ad = (id) => this.c.ads[id];
      const base = (r) => ({ id: r.id, name: ad(r.id).name, format: this.labels[ad(r.id).creative.type] || ad(r.id).creative.type, type: ad(r.id).creative.type, campaign: ad(r.id).campaign_name, m30: r.m30, m7: r.m7 });
      const running = (r) => r.m7.spend > 0 && r.m30.last_day >= this.iso(b - 2);
      const spendSorted = rows.map((r) => r.m30.spend).sort((p, q) => p - q);
      const median = spendSorted.length ? spendSorted[Math.floor(spendSorted.length / 2)] : 0;
      // 1. Hidden gems: little spend, strong ROAS, real purchases.
      const gems = rows.filter((r) => r.m30.roas !== null && r.m30.purchases >= 2 && r.m30.roas >= T * 1.3 && r.m30.spend <= Math.max(median, acct30.spend * 0.02))
        .map((r) => ({ ...base(r), daily: r.m30.spend / 30, suggest_daily: Math.max(500, Math.round(r.m30.spend / 30 * 2 / 100) * 100), score: r.m30.roas * Math.log(1 + r.m30.purchases) }))
        .sort((p, q) => q.score - p.score).slice(0, 6);
      // 2. Scale: running, strong last 7 days, enough data.
      const scale = rows.filter((r) => running(r) && r.m7.roas !== null && r.m7.roas >= T && C && r.m7.spend >= C && !gems.some((g) => g.id === r.id))
        .map((r) => ({ ...base(r), daily: r.m7.spend / 7 })).sort((p, q) => q.m7.purchase_value - p.m7.purchase_value).slice(0, 6);
      // 3. Pause or fix: running, spent at least 1 CPA this week, well below target.
      const pause = rows.filter((r) => running(r) && C && r.m7.spend >= C && (r.m7.roas === null || r.m7.roas < T * 0.7))
        .map((r) => ({ ...base(r), daily: r.m7.spend / 7, weekly_waste: r.m7.spend - (r.m7.purchase_value || 0) / (T || 1) })).sort((p, q) => q.m7.spend - p.m7.spend).slice(0, 6);
      // 4. Refresh: running ads with fatigue.
      const taken = new Set([...scale, ...pause].map((x) => x.id));
      const tired = rows.filter((r) => running(r) && !taken.has(r.id) && r.m30.spend >= (C || 0)).map((r) => ({ r, f: this.fatigue(r.id, b) }))
        .filter((x) => ['declining', 'ctr_down', 'roas_down'].includes(x.f.code)).map((x) => ({ ...base(x.r), fatigue: x.f })).sort((p, q) => q.m30.spend - p.m30.spend).slice(0, 6);
      // 5. Format bet from the breakdown rows.
      const fa = this.formatAudience(view);
      const fmt = {};
      for (const r of rows) { const t = ad(r.id).creative.type; (fmt[t] || (fmt[t] = [])).push(r.m30); }
      const formats = Object.entries(fmt).map(([t, list]) => ({ type: t, label: this.labels[t] || t, ...Engine.addUp(list) })).filter((f) => f.spend > 0);
      const bigEnough = formats.filter((f) => f.spend >= acct30.spend * 0.05 && f.roas !== null).sort((p, q) => q.roas - p.roas);
      let bet = null;
      if (bigEnough.length) {
        const f = bigEnough[0];
        const seg = (dim) => Object.entries(fa[dim][f.type] || {}).filter(([k, c]) => c.roas !== null && c.spend >= f.spend * 0.05 && k !== 'unknown').sort((p, q) => q[1].roas - p[1].roas)[0];
        bet = { ...f, share: f.spend / acct30.spend, best_age: seg('age'), best_gender: seg('gender'), runner_up: bigEnough[1] || null };
      }
      const relaunch = this.lifecycleSummary(view).relaunch.slice(0, 4);
      return { window: [this.iso(a30), this.iso(b)], acct30, acct7, target_roas: T, target_cpa: C, gems, scale, pause, tired, bet, formats, relaunch };
    }
  }
  root.GalleryEngine = Engine;
  root.cleanKeywords = cleanKeywords;
})(typeof window !== 'undefined' ? window : globalThis);
