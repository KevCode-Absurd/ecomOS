'use strict';
// Client report: the whole business (website sales from Metabase) and Meta ads, in plain English,
// with charts, a clear plan and what we need from the owner. Replaces reportHtml from app.js.
// Uses: VIEW, ENGINE, DATA (app.js/engine.js), SL, metaDayMap, gaMap, typeCat, CATS, CAT_COLOR, baseCode, cleanName, inAds (sales.js),
// sparkSvg, compact (overview.js), buildTests (testlab.js), topProducts (prodads.js), TESTS (lab.js).

const RP = { team: false };
const RP_PERIODS = [['30', 'Last 30 days'], ['60', 'Last 60 days'], ['90', 'Last 90 days'], ['this_month', 'This month'], ['last_month', 'Last month']];

// ---------- numbers ----------
function rpDay(d) {
  // A day with no orders comes back with no sales row: that is a real zero, not missing data.
  const zero = (sales, orders) => (sales === null && orders === 0 ? 0 : sales);
  const x = SL.data.daily && SL.data.daily[d];
  if (x) return { sales: zero(x.sales, x.orders), orders: x.orders, items: x.items, refund: x.refund, types: x.types, skus: x.skus, full: true };
  const t = SL.data.daily_totals && SL.data.daily_totals[d];
  if (t) return { sales: zero(t[0], t[1]), orders: t[1], items: t[2], refund: t[3], types: null, skus: (SL.data.sku_daily || {})[d] || null, full: false };
  return null;
}
function rpLastSalesDay() {
  const k = Object.keys(SL.data.daily || {}).sort();
  return k[k.length - 1];
}
// Website numbers for since..until. Days with no data are counted, so coverage can be shown.
function rpBrand(since, until) {
  const ga = gaMap(), md = metaDayMap(), days = [];
  for (let d = since; d <= until; d = addDays(d, 1)) {
    const x = rpDay(d), g = ga[d], m = md[d];
    days.push({ d, x, visits: g ? g.visits : null, spend: m ? m.spend : 0, claimed: m && m.valueSeen ? m.value : null, purchases: m ? m.purchases : 0 });
  }
  const got = days.filter((r) => r.x && r.x.sales !== null);
  const sum = (f) => got.reduce((t, r) => t + (f(r) || 0), 0);
  const withVisits = got.filter((r) => r.visits !== null);
  const sales = sum((r) => r.x.sales), orders = sum((r) => r.x.orders);
  // Sales by type from the product list of each day (names say ring, chain...). Covers every day with product data.
  const typeDays = got.filter((r) => r.x.skus);
  const types = {};
  for (const r of typeDays) for (const row of r.x.skus) { const name = row.length === 5 ? row[2] : ''; const v = row.length === 5 ? row[3] : row[2]; const c = typeCat(name); types[c] = (types[c] || 0) + (v || 0); }
  const skus = {};
  for (const r of got) for (const row of r.x.skus || []) {
    const [metal, code, name, v, n] = row.length === 5 ? row : [row[0], row[1], '', row[2], row[3]];
    const b = baseCode(code), o = skus[b] || (skus[b] = { code: b, name: cleanName(name), v: 0, n: 0 });
    o.v += v || 0; o.n += n || 0;
    if (!o.name && name) o.name = cleanName(name);
  }
  const refundDays = got.filter((r) => r.x.refund !== null && r.x.refund !== undefined);
  return {
    since, until, days, n: days.length, covered: got.length,
    sales: got.length ? sales : null, orders: got.length ? orders : null, items: got.length ? sum((r) => r.x.items) : null,
    aov: orders ? sales / orders : null, refund: refundDays.length ? refundDays.reduce((t, r) => t + r.x.refund, 0) : null,
    visits: withVisits.length === got.length && got.length ? withVisits.reduce((t, r) => t + r.visits, 0) : null,
    conv: withVisits.length === got.length && got.length ? orders / withVisits.reduce((t, r) => t + r.visits, 0) : null,
    types: got.length && typeDays.length >= got.length * 0.8 ? types : null, typeDays: typeDays.length,
    skus: Object.values(skus).filter((o) => o.v > 0).sort((a, b) => b.v - a.v),
    spend: days.reduce((t, r) => t + r.spend, 0),
  };
}
function rpPeriods() {
  const last = rpLastSalesDay(), r = VIEW.range;
  const until = r.until > last ? last : r.until, since = r.since;
  const len = Math.round((Date.parse(until) - Date.parse(since)) / 864e5) + 1;
  const pu = addDays(since, -1), ps = addDays(since, -len);
  const cur = rpBrand(since, until), prev = rpBrand(ps, pu);
  // Compare only when both periods have every day, so a gap never looks like a drop.
  const ok = cur.covered === cur.n && prev.covered === prev.n;
  return { cur, prev: ok ? prev : { ...prev, sales: null, orders: null, aov: null, visits: null, conv: null, refund: null, partial: true }, prevRaw: prev, cut: until < r.until, ok };
}

// ---------- words ----------
const rpPct = (v) => (v === null || !Number.isFinite(v) ? null : Math.round(v * 100));
function rpChange(cur, prev, good = 1) {
  if (cur === null || prev === null || prev === undefined || !prev) return { txt: 'no full earlier period to compare', tone: 'flat', ch: null };
  const ch = (cur - prev) / Math.abs(prev), p = Math.abs(Math.round(ch * 100));
  if (p === 0) return { txt: 'about the same as before', tone: 'flat', ch };
  const up = ch > 0;
  return { txt: `${up ? 'up' : 'down'} ${p}% from before`, tone: (up ? good : -good) > 0 ? 'good' : 'bad', ch };
}
function rpDelta(cur, prev, good = 1) {
  const c = rpChange(cur, prev, good);
  const icon = c.ch === null || c.tone === 'flat' ? '•' : c.ch > 0 ? '▲' : '▼';
  return `<span class="rp-delta ${c.tone}"><span aria-hidden="true">${icon}</span> ${esc(c.txt)}</span>`;
}
const rpMoney = (v) => (v === null || v === undefined ? '<span class="na">Not available</span>' : esc(compact(v)));
const rpX = (v) => (v === null || v === undefined ? '<span class="na">Not available</span>' : '₹' + v.toFixed(2));

// ---------- charts (SVG, 1 axis each, hover tips via data-tip) ----------
function rpBars({ labels, series, fmtY = compact, H = 220, tips, marks, ghost }) {
  const W = 900, L = 62, R = 12, T = 14, B = 34, n = labels.length;
  const vals = series.flatMap((s) => s.vals).filter((v) => v !== null && Number.isFinite(v));
  const max = Math.max(1, ...vals, ghost ? ghost.v : 0) * 1.08;
  const y = (v) => T + (H - T - B) * (1 - v / max);
  const slot = (W - L - R) / Math.max(1, n), gw = Math.min(slot * 0.72, 26 * series.length + 2 * (series.length - 1));
  const bw = (gw - 2 * (series.length - 1)) / series.length;
  const grid = [0, 0.5, 1].map((f) => `<line class="gl" x1="${L}" x2="${W - R}" y1="${y(max / 1.08 * f).toFixed(1)}" y2="${y(max / 1.08 * f).toFixed(1)}"/><text class="tl" x="${L - 8}" y="${(y(max / 1.08 * f) + 4).toFixed(1)}" text-anchor="end">${esc(fmtY(max / 1.08 * f))}</text>`).join('');
  const every = Math.ceil(n / 10);
  const body = labels.map((lab, i) => {
    const x0 = L + slot * i + (slot - gw) / 2;
    const bars = series.map((s, j) => {
      const v = s.vals[i];
      if (v === null || !Number.isFinite(v)) return '';
      const h = Math.max(v > 0 ? 2 : 0, y(0) - y(v)), x = x0 + j * (bw + 2);
      return `<path d="M${x.toFixed(1)},${y(0).toFixed(1)}v${(-h + Math.min(4, h)).toFixed(1)}q0,-${Math.min(4, h).toFixed(1)} ${Math.min(4, bw / 2).toFixed(1)},-${Math.min(4, h).toFixed(1)}h${(bw - 2 * Math.min(4, bw / 2)).toFixed(1)}q${Math.min(4, bw / 2).toFixed(1)},0 ${Math.min(4, bw / 2).toFixed(1)},${Math.min(4, h).toFixed(1)}v${(h - Math.min(4, h)).toFixed(1)}z" style="fill:${s.color}${s.faded && s.faded(i) ? ';opacity:.45' : ''}"/>`;
    }).join('');
    const mark = marks && marks[i] ? `<text class="tl" x="${(x0 + gw / 2).toFixed(1)}" y="${(y(Math.max(...series.map((s) => s.vals[i] || 0))) - 6).toFixed(1)}" text-anchor="middle" style="font-weight:700;fill:var(--ink)">${esc(marks[i])}</text>` : '';
    return `<g data-tip="${esc(tips ? tips(i) : [lab, ...series.flatMap((s) => [s.name, s.vals[i] === null ? 'Not available' : fmtY(s.vals[i])])].join('|'))}"><rect x="${(L + slot * i).toFixed(1)}" y="${T}" width="${slot.toFixed(1)}" height="${H - T - B}" fill="transparent"/>${bars}${mark}
      ${i === n - 1 || (i % every === 0 && n - 1 - i >= Math.max(2, every * 0.6)) ? `<text class="tl" x="${(x0 + gw / 2).toFixed(1)}" y="${H - 12}" text-anchor="middle">${esc(lab)}</text>` : ''}</g>`;
  }).join('');
  // ghost: a dashed outline from the bar top up to an estimate, on the same axis.
  let gh = '';
  if (ghost && series[0].vals[ghost.i] !== null && ghost.v > series[0].vals[ghost.i]) {
    const x0 = L + slot * ghost.i + (slot - gw) / 2;
    gh = `<rect x="${x0.toFixed(1)}" y="${y(ghost.v).toFixed(1)}" width="${bw.toFixed(1)}" height="${(y(series[0].vals[ghost.i]) - y(ghost.v)).toFixed(1)}" rx="4" style="fill:none;stroke:var(--gold-deep);stroke-dasharray:4 3;stroke-width:1.5" pointer-events="none"/>`;
  }
  return `<svg class="rp-chart" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(series.map((s) => s.name).join(' and '))}">${grid}<line x1="${L}" x2="${W - R}" y1="${y(0)}" y2="${y(0)}" style="stroke:var(--line)"/>${body}${gh}</svg>`;
}
function rpLegend(items) { return `<div class="rp-legend">${items.map(([c, l, faded]) => `<span><i style="background:${c}${faded ? ';opacity:.45' : ''}"></i>${esc(l)}</span>`).join('')}</div>`; }
// Group days into weeks when the period is long.
function rpBuckets(days) {
  if (days.length <= 45) return days.map((r) => ({ label: shortDate(r.d), from: r.d, to: r.d, rows: [r] }));
  const out = [];
  for (let i = 0; i < days.length; i += 7) { const rows = days.slice(i, i + 7); out.push({ label: shortDate(rows[0].d), from: rows[0].d, to: rows[rows.length - 1].d, rows }); }
  return out;
}
function rpHbar(rows, fmtV = compact) {
  const max = Math.max(1, ...rows.map((r) => Math.max(r.a || 0, r.b || 0)));
  return `<div class="rp-hbars">${rows.map((r) => `<div class="rp-hrow" data-tip="${esc(r.tip || '')}"><span class="rp-hl">${r.color ? `<i style="background:${r.color}"></i>` : ''}${esc(r.label)}</span>
    <span class="rp-htrack"><span style="width:${(100 * (r.a || 0) / max).toFixed(1)}%;background:${r.colorA || 'var(--gold)'}"></span>${r.b !== undefined ? `<span style="width:${(100 * (r.b || 0) / max).toFixed(1)}%;background:${r.colorB || 'var(--spend)'}"></span>` : ''}</span>
    <span class="rp-hv">${esc(r.valTxt || fmtV(r.a))}</span></div>`).join('')}</div>`;
}

// ---------- sections ----------
function rpHero(P) {
  const c = P.cur, p = P.prev;
  const tile = (label, val, cur, prev, good, spark, explain) => `<div class="rp-kpi"><div class="rp-kl">${esc(label)}</div><div class="rp-kv">${val}</div>${rpDelta(cur, prev, good)}
    ${spark ? `<div class="rp-spark">${spark}</div>` : ''}<div class="rp-kx">${esc(explain)}</div></div>`;
  const sv = (f) => c.days.map((r) => (r.x && r.x.sales !== null ? f(r) : null));
  return `<div class="rp-kpis">
    ${tile('Website sales', rpMoney(c.sales), c.sales, p.sales, 1, sparkSvg(sv((r) => r.x.sales), { color: 'var(--gold-deep)', H: 40 }), 'All orders on your website, from every source.')}
    ${tile('Orders', c.orders === null ? '<span class="na">Not available</span>' : String(c.orders), c.orders, p.orders, 1, sparkSvg(sv((r) => r.x.orders), { color: 'var(--ink)', H: 40 }), `About ${c.orders ? (c.orders / c.covered).toFixed(1) : '0'} orders a day.`)}
    ${tile('Average order', rpMoney(c.aov), c.aov, p.aov, 1, '', 'Money from 1 order, on average.')}
    ${tile('Website visits', c.visits === null ? '<span class="na">Not available</span>' : c.visits.toLocaleString('en-IN'), c.visits, p.visits, 1, sparkSvg(c.days.map((r) => r.visits), { color: 'var(--spend)', H: 40 }), 'People who came to the website.')}
    ${tile('Orders per 10,000 visits', c.conv === null ? '<span class="na">Not available</span>' : (c.conv * 10000).toFixed(1), c.conv, p.conv, 1, '', 'How many visits turn into an order.')}
    ${tile('Money refunded', rpMoney(c.refund), c.refund, p.refund, -1, '', 'Returns and refunds in these days.')}
  </div>`;
}
function rpSummary(P, t) {
  const c = P.cur, p = P.prev, s = rpChange(c.sales, p.sales), per = c.sales && c.spend ? c.sales / c.spend : null;
  const bits = [];
  if (c.sales !== null) bits.push(`You sold <b>${esc(compact(c.sales))}</b> on your website in these ${c.n} days${s.ch !== null ? `, <b>${esc(s.txt.replace(' from before', ''))}</b> from the ${c.n} days before` : ''}.`);
  if (t.spend) bits.push(`You spent <b>${esc(compact(t.spend))}</b> on Meta ads.`);
  if (per) bits.push(`For every ₹1 spent on ads, your website made <b>₹${per.toFixed(1)}</b> in sales.`);
  return bits.join(' ');
}
function rpSalesTrend(P) {
  const c = P.cur, p = P.prev;
  const bc = rpBuckets(c.days), bp = rpBuckets(p.days);
  const sumB = (b, f) => { const rows = b.rows.filter((r) => r.x && r.x.sales !== null); return rows.length ? rows.reduce((t, r) => t + (f(r) || 0), 0) : null; };
  const cur = bc.map((b) => sumB(b, (r) => r.x.sales)), prev = bc.map((b, i) => (bp[i] ? sumB(bp[i], (r) => r.x.sales) : null));
  const unit = c.days.length <= 45 ? 'day' : 'week';
  const best = c.days.filter((r) => r.x && r.x.sales !== null).sort((a, b) => b.x.sales - a.x.sales)[0];
  const byWd = {};
  for (const r of c.days) if (r.x && r.x.sales !== null) { const k = weekday(r.d); const o = byWd[k] || (byWd[k] = { s: 0, n: 0 }); o.s += r.x.sales; o.n += 1; }
  const wd = Object.entries(byWd).map(([k, o]) => [k, o.s / o.n]).sort((a, b) => b[1] - a[1]);
  const hasPrev = prev.some((v) => v !== null);
  return `<section class="rp-sec"><h2>How your sales moved</h2>
    <p class="rp-lead">Each bar is 1 ${unit} of website sales.${hasPrev ? ' The faded bar next to it is the same ' + unit + ' in the period before, so you can compare.' : ''}</p>
    ${rpLegend([['var(--gold)', `Website sales, this period`], ...(hasPrev ? [['var(--faint)', 'Same ' + unit + ', period before']] : [])])}
    ${rpBars({ labels: bc.map((b) => b.label), series: [{ name: 'This period', color: 'var(--gold)', vals: cur }, ...(hasPrev ? [{ name: 'Period before', color: 'var(--faint)', vals: prev }] : [])],
      tips: (i) => [`${unit === 'week' ? 'Week of ' : ''}${bc[i].label}`, 'Website sales', cur[i] === null ? 'Not available' : compact(cur[i]), ...(hasPrev ? ['Period before', prev[i] === null ? 'Not available' : compact(prev[i])] : [])].join('|') })}
    <div class="rp-facts">
      ${best ? `<div><span class="muted small">Best day</span><b>${esc(weekday(best.d))} ${esc(shortDate(best.d))}</b><span>${esc(compact(best.x.sales))} from ${best.x.orders} order${best.x.orders === 1 ? '' : 's'}</span></div>` : ''}
      ${wd.length >= 5 ? `<div><span class="muted small">Strongest weekday</span><b>${esc(wd[0][0])}</b><span>about ${esc(compact(wd[0][1]))} a day</span></div><div><span class="muted small">Slowest weekday</span><b>${esc(wd[wd.length - 1][0])}</b><span>about ${esc(compact(wd[wd.length - 1][1]))} a day</span></div>` : ''}
    </div></section>`;
}
function rpYear(P) {
  const keys = Object.keys(SL.data.months).sort().slice(-12);
  const last = rpLastSalesDay(), curKey = last.slice(0, 7);
  const dim = new Date(Date.UTC(+curKey.slice(0, 4), +curKey.slice(5), 0)).getUTCDate(), day = +last.slice(8);
  const mSales = (k) => { const m = SL.data.months[k]; return m && m.ot ? Object.values(m.ot).reduce((t, r) => t + (r[0] || 0), 0) : null; };
  const vals = keys.map(mSales);
  const est = day < dim && vals[vals.length - 1] !== null ? vals[vals.length - 1] / day * dim : null;
  const inPeriod = (k) => k >= P.cur.since.slice(0, 7) && k <= P.cur.until.slice(0, 7);
  const prior = vals.slice(-4, -1).filter((v) => v !== null), avg3 = prior.length ? prior.reduce((a, b) => a + b, 0) / prior.length : null;
  const lab = (k) => new Date(k + '-01T00:00:00Z').toLocaleDateString('en-IN', { month: 'short', timeZone: 'UTC' });
  const best = keys.map((k, i) => [k, vals[i]]).filter((x) => x[1] !== null && x[0] !== curKey).sort((a, b) => b[1] - a[1])[0];
  return `<section class="rp-sec"><h2>Where your business stands this year</h2>
    <p class="rp-lead">Website sales for each of the last 12 months. Months in this report are darker.${est ? ` The dashed part of ${esc(lab(curKey))} is an estimate if the month keeps its pace.` : ''}</p>
    ${rpBars({ labels: keys.map(lab), series: [{ name: 'Website sales', color: 'var(--gold)', vals, faded: (i) => !inPeriod(keys[i]) }], H: 200,
      tips: (i) => [new Date(keys[i] + '-01T00:00:00Z').toLocaleDateString('en-IN', { month: 'long', year: 'numeric', timeZone: 'UTC' }), 'Website sales', vals[i] === null ? 'Not available' : compact(vals[i]), ...(keys[i] === curKey && est ? ['So far', `${day} of ${dim} days`, 'Estimate for the month', compact(est)] : [])].join('|'), ghost: est ? { i: keys.length - 1, v: est } : null })}
    <div class="rp-facts">
      ${best ? `<div><span class="muted small">Best month</span><b>${esc(new Date(best[0] + '-01T00:00:00Z').toLocaleDateString('en-IN', { month: 'long', year: 'numeric', timeZone: 'UTC' }))}</b><span>${esc(compact(best[1]))}</span></div>` : ''}
      ${avg3 ? `<div><span class="muted small">Average of the 3 months before this one</span><b>${esc(compact(avg3))}</b><span>a month</span></div>` : ''}
      ${est ? `<div><span class="muted small">${esc(lab(curKey))} if the pace holds</span><b>about ${esc(compact(est))}</b><span>${avg3 ? `${est >= avg3 ? 'above' : 'below'} the 3-month average` : ''}</span></div>` : ''}
    </div></section>`;
}
function rpMeta(P) {
  const v = VIEW, t = v.totals, pt = v.previous_totals || {}, c = P.cur;
  const claimShare = c.sales && t.purchase_value !== null ? Math.min(1, t.purchase_value / c.sales) : null;
  // Same days on both sides: website sales and ad money for the days we have website data.
  const per = c.sales && c.spend ? c.sales / c.spend : null, perPrev = P.prev.sales && P.prev.spend ? P.prev.sales / P.prev.spend : null;
  const tile = (label, val, cur, prev, good, explain) => `<div class="rp-kpi"><div class="rp-kl">${esc(label)}</div><div class="rp-kv">${val}</div>${v.previous.complete ? rpDelta(cur, prev, good) : ''}<div class="rp-kx">${esc(explain)}</div></div>`;
  const b = rpBuckets(c.days);
  const spend = b.map((x) => x.rows.reduce((s, r) => s + r.spend, 0)), claimed = b.map((x) => { const r = x.rows.filter((q) => q.claimed !== null); return r.length ? r.reduce((s, q) => s + q.claimed, 0) : null; });
  const unit = c.days.length <= 45 ? 'day' : 'week';
  return `<section class="rp-sec"><h2>What your Meta ads did</h2>
    <div class="rp-kpis">
      ${tile('Money spent on ads', rpMoney(t.spend), t.spend, pt.spend, 0, 'Facebook and Instagram ads.')}
      ${tile('Sales Meta says came from ads', rpMoney(t.purchase_value), t.purchase_value, pt.purchase_value, 1, `${t.purchases || 0} orders, as Meta counts them.`)}
      ${tile('Return on ad money (ROAS)', t.roas === null ? '<span class="na">Not available</span>' : '₹' + t.roas.toFixed(2), t.roas, pt.roas, 1, 'Sales Meta counts for every ₹1 spent.')}
      ${tile('Website sales for every ₹1 of ads', per === null ? '<span class="na">Not available</span>' : '₹' + per.toFixed(1), per, perPrev, 1, 'All website sales divided by ad money. The simplest health check.')}
      ${tile('Cost for 1 order from ads', rpMoney(t.cpa), t.cpa, pt.cpa, -1, 'Ad money divided by the orders Meta counts.')}
      ${tile('Times your ads were seen', t.impressions === null || t.impressions === undefined ? '<span class="na">Not available</span>' : (t.impressions >= 1e7 ? (t.impressions / 1e7).toFixed(2) + ' crore' : t.impressions >= 1e5 ? (t.impressions / 1e5).toFixed(1) + ' lakh' : Number(t.impressions).toLocaleString('en-IN')), t.impressions, pt.impressions, 1, 'On Facebook and Instagram. 1 person can see an ad more than once.')}
    </div>
    <h3>Ad money and the sales Meta counted, by ${unit}</h3>
    ${rpLegend([['var(--spend)', 'Ad money spent'], ['var(--ink)', 'Sales Meta counted']])}
    ${rpBars({ labels: b.map((x) => x.label), series: [{ name: 'Ad money spent', color: 'var(--spend)', vals: spend }, { name: 'Sales Meta counted', color: 'var(--ink)', vals: claimed }], H: 200 })}
    ${claimShare !== null ? `<h3>How much of your website sales Meta takes credit for</h3>
      <div class="rp-split" role="img" aria-label="Meta counts ${rpPct(claimShare)}% of website sales"><span style="width:${(claimShare * 100).toFixed(1)}%;background:var(--ink)"><b>${rpPct(claimShare)}%</b></span><span style="width:${((1 - claimShare) * 100).toFixed(1)}%;background:var(--gold)"><b>${100 - rpPct(claimShare)}%</b></span></div>
      ${rpLegend([['var(--ink)', 'Meta says its ads brought these sales'], ['var(--gold)', 'The rest: repeat buyers, Google, word of mouth, store visits and sales Meta did not track']])}
      <p class="rp-note">Meta counts a sale if the buyer saw or clicked an ad before buying. Some of those people would have bought anyway, so the true share is usually lower.</p>` : ''}
  </section>`;
}
function rpAdCard(ad, why) {
  const m = ad.view.metrics;
  return `<div class="rp-ad">${thumbHtml(ad.id, ad.name).replace(' loading="lazy"', '')}<div><b>${esc(ad.name)}</b>
    <div class="rp-adm"><span>Spent ${esc(compact(m.spend))}</span><span>${m.purchases || 0} order${m.purchases === 1 ? '' : 's'}</span><span>${m.roas === null ? 'No sales counted' : `₹${m.roas.toFixed(2)} back for ₹1`}</span></div>
    <p class="small">${why}</p></div></div>`;
}
function rpAds() {
  const v = VIEW, pool = [...new Set([...(v.collections['roas2:all'] || { ad_ids: [] }).ad_ids, ...v.collections.all.ad_ids])].map((id) => v.ads[id]).filter(Boolean);
  const T = v.targets.roas || v.totals.roas || 0;
  const good = pool.filter((a) => a.view.metrics.roas !== null && a.view.metrics.purchases >= 2).sort((a, b) => b.view.metrics.roas - a.view.metrics.roas).slice(0, 4);
  const bad = v.collections.all.ad_ids.map((id) => v.ads[id]).filter((a) => a.view.verdict.code === 'cut').sort((a, b) => b.view.metrics.spend - a.view.metrics.spend).slice(0, 3);
  const tagWhy = (a) => { const tg = a.tags || {}; const bits = []; if (tg.angle && tg.angle.code !== 'other') bits.push(`the message is about ${tg.angle.label.toLowerCase()}`); if (tg.product && tg.product.label && !/mixed|other/i.test(tg.product.label)) bits.push(`it shows ${tg.product.label.toLowerCase()}`); return bits.length ? ' T' + bits.join(' and ').slice(1) + '.' : ''; };
  return `<section class="rp-sec"><h2>Ads that worked, and ads that did not</h2>
    <div class="rp-two"><div><h3 class="good">Worked best</h3>${good.map((a) => rpAdCard(a, `Made ₹${a.view.metrics.roas.toFixed(2)} for every ₹1${T ? `, ${(a.view.metrics.roas / T).toFixed(1)} times the account's usual` : ''}.${esc(tagWhy(a))}`)).join('') || '<p class="muted">No ad had 2 or more orders in these days.</p>'}</div>
    <div><h3 class="bad">Spent money, sold little</h3>${bad.map((a) => rpAdCard(a, `Spent ${esc(compact(a.view.metrics.spend))} ${a.view.metrics.purchases ? `for ${a.view.metrics.purchases} order${a.view.metrics.purchases === 1 ? '' : 's'}` : 'with no orders counted'}. We will stop or change it.`)).join('') || '<p class="muted">No big ad was losing money. Good.</p>'}</div></div></section>`;
}
function rpProducts(P) {
  const c = P.cur;
  const tot = c.types ? Object.values(c.types).reduce((a, b) => a + b, 0) : 0;
  const meta = metaRange(c.since, c.until), tagged = CATS.reduce((t, k) => t + (meta.cat[k] || 0), 0);
  const cats = c.types ? CATS.filter((k) => c.types[k]).map((k) => ({ k, s: c.types[k] / tot, a: tagged ? (meta.cat[k] || 0) / tagged : null })).sort((a, b) => b.s - a.s) : [];
  const skus = c.skus.slice(0, 6);
  return `<section class="rp-sec"><h2>What people bought</h2>
    <div class="rp-two">
      <div><h3>Top pieces by sales</h3>${skus.length ? rpHbar(skus.map((o) => ({ label: o.name || o.code, a: o.v, valTxt: `${compact(o.v)} · ${o.n} sold`, tip: [o.name, 'Sales', compact(o.v), 'Pieces sold', o.n, 'Code', o.code].join('|') }))) : '<p class="muted">Not available for these days.</p>'}
        ${skus.length ? `<p class="rp-note">${skus.filter((o) => inAds(o.name) === false).length} of these ${skus.length} pieces have no ad of their own yet.</p>` : ''}</div>
      <div><h3>Share of sales and share of ad money, by type</h3>${cats.length ? rpHbar(cats.map((x) => ({ label: x.k, color: CAT_COLOR[x.k], a: x.s, b: x.a ?? 0, colorA: 'var(--gold)', colorB: 'var(--spend)', valTxt: `${rpPct(x.s)}% of sales${x.a !== null ? ` · ${rpPct(x.a)}% of ad money` : ''}`,
          tip: [x.k, 'Share of website sales', rpPct(x.s) + '%', 'Share of product ad money', x.a === null ? 'Not available' : rpPct(x.a) + '%'].join('|') })), (v) => rpPct(v) + '%') + rpLegend([['var(--gold)', 'Share of website sales'], ['var(--spend)', 'Share of ad money']])
        : `<p class="muted">Sales by type are available from ${esc(dateLabel(Object.keys(SL.data.sku_daily || SL.data.daily).sort()[0]))}. Pick dates after that to see this.</p>`}${c.types && c.typeDays < c.covered ? `<p class="rp-note">Based on ${c.typeDays} of ${c.covered} days.</p>` : ''}</div>
    </div></section>`;
}
function rpPeople() {
  const d = VIEW.demographics_all || {};
  const rows = (dim, order) => Object.entries(d[dim] || {}).filter(([k, x]) => x.spend > 0 && !/unknown/i.test(k)).sort((a, b) => (order ? order.indexOf(a[0]) - order.indexOf(b[0]) : b[1].spend - a[1].spend));
  const age = rows('age'), gender = rows('gender');
  if (!age.length) return '';
  const tot = age.reduce((t, [, x]) => t + x.spend, 0);
  const best = age.filter(([, x]) => x.roas !== null && x.spend >= tot * 0.05).sort((a, b) => b[1].roas - a[1].roas)[0];
  const bar = (list) => rpHbar(list.map(([k, x]) => ({ label: k, a: x.roas || 0, valTxt: x.roas === null ? 'No sales counted' : `₹${x.roas.toFixed(2)} back for ₹1 · ${rpPct(x.spend / tot)}% of money`, colorA: 'var(--roas)', tip: [k, 'Ad money', compact(x.spend), 'Sales Meta counted', x.purchase_value === null ? 'Not available' : compact(x.purchase_value), 'Back for ₹1', x.roas === null ? 'Not available' : '₹' + x.roas.toFixed(2)].join('|') })), (v) => '₹' + v.toFixed(2));
  return `<section class="rp-sec"><h2>Who buys from your ads</h2>
    <p class="rp-lead">${best ? `People aged <b>${esc(best[0])}</b> gave the best return: <b>₹${best[1].roas.toFixed(2)}</b> for every ₹1.` : 'No age group had enough sales to compare.'}</p>
    <div class="rp-two"><div><h3>By age</h3>${bar(age)}</div><div><h3>By gender</h3>${bar(gender)}</div></div></section>`;
}

// ---------- the plan ----------
// Test briefs come from the action plan and use ad words. Turn them into plain English for the owner.
function rpPlain(t) {
  return String(t || '')
    .replace(/Meta ROAS beats ([\d.]+)x/g, 'the ad makes back more than ₹$1 for every ₹1')
    .replace(/ROAS ([\d.]+)x/g, '₹$1 back for every ₹1').replace(/\bROAS\b/g, 'return on ad money')
    .replace(/product ad spend/g, 'ad money on single products').replace(/\bad spend\b/g, 'ad money')
    .replace(/\bad sets?\b/g, (m) => (m.endsWith('s') ? 'ad groups' : 'ad group')).replace(/best broad audience/g, 'widest audience')
    .replace(/\bCTR\b/g, 'share of people who click').replace(/cost per purchase/g, 'cost for 1 order')
    .replace(/Catalog and mixed ads are left out\.?/g, '').replace(/Ads are tagged by product from their names and copy\.?/g, '')
    .replace(/\s+/g, ' ').trim();
}
function rpPlan() {
  const o = ENGINE.opportunities(VIEW), items = [];
  // 1 ad in 1 list only (pause first), and say the format when 2 ads share a name.
  const seen = new Set();
  for (const k of ['pause', 'scale', 'gems', 'tired']) o[k] = o[k].filter((x) => !seen.has(x.id) && seen.add(x.id));
  const all = ['pause', 'scale', 'gems', 'tired'].flatMap((k) => o[k]), count = {};
  for (const x of all) count[x.name] = (count[x.name] || 0) + 1;
  const names = (l, n = 3) => l.slice(0, n).map((x) => `"${x.name}"${count[x.name] > 1 ? ` (${String(x.format || '').toLowerCase()})` : ''}`).join(', ');
  let top = null;
  try { top = topProducts(30); } catch (e) { top = null; }
  if (top && top.list.length) {
    const noAd = top.list.filter((p) => p.inAds === false);
    items.push({ when: 'This week', title: 'Make new ads for your 5 best-selling pieces',
      what: `We will make 3 to 4 new image ads for each of these pieces: ${top.list.map((p) => p.name).join(', ')}. Each ad uses the real photo, the real price and 1 fact from your website, like the hallmark or the exchange promise.`,
      why: `These 5 pieces made ${compact(top.list.reduce((t, p) => t + p.v, 0))} in the last 30 days.${noAd.length ? ` ${noAd.length} of them have no ad of their own, but people still buy them.` : ''} Selling what already sells is the safest way to grow.`,
      you: 'Send 2 or 3 good photos of each piece if you have them, and tell us if any piece is low on stock.', result: 'Each piece sells faster than before, and new ads bring back at least as much as the account average.' });
  }
  if (o.pause.length) items.push({ when: 'This week', title: 'Stop or fix ads that spend but do not sell',
    what: `We will pause or change ${o.pause.length} ad${o.pause.length > 1 ? 's' : ''}: ${names(o.pause)}.`,
    why: `Together they spent ${compact(o.pause.reduce((t, x) => t + x.m7.spend, 0))} last week and brought back far less than your other ads.`,
    you: 'Nothing. We will do this.', result: `About ${compact(o.pause.reduce((t, x) => t + x.m7.spend, 0) * 4)} a month moves to ads that work.` });
  if (o.scale.length) items.push({ when: 'This week', title: 'Give a little more money to your best ads',
    what: `We will raise the daily budget by about 20% on ${names(o.scale)}. We raise it slowly so Meta does not reset what it has learned.`,
    why: 'These ads are bringing back more than your target right now.', you: `Please approve about ${compact(o.scale.reduce((t, x) => t + x.daily, 0) * 0.2)} more a day.`, result: 'More orders at about the same cost per order.' });
  if (o.gems.length) items.push({ when: 'Next week', title: 'Test ads that sold well on small money',
    what: `We will give ${names(o.gems)} their own budget of about ${compact(o.gems[0].suggest_daily)} a day each, with 3 fresh versions.`,
    why: 'They brought back much more than your average, but Meta gave them very little money, so we do not know their full power yet.', you: 'Nothing. We will do this.', result: 'At least 1 of them becomes a steady seller.' });
  if (o.tired.length) items.push({ when: 'Next week', title: 'Refresh ads people are tired of seeing',
    what: `We will make new versions of ${names(o.tired)}: same idea, new photo or new first line.`,
    why: 'Fewer people click these ads now than a few weeks ago. That happens when the same people see an ad many times.', you: 'Nothing, unless you have new photos or a new launch to show.', result: 'Clicks and sales come back to their earlier level.' });
  let tests = [];
  const inTop = new Set(top ? top.list.map((p) => p.code) : []);
  try { tests = buildTests().filter((t) => t.id !== 'pulse' && !(t.id.startsWith('sku-') && inTop.has(t.id.slice(4)))).slice(0, 2); } catch (e) { tests = []; }
  for (const t of tests) items.push({ when: 'Weeks 3 and 4', title: rpPlain(t.title.replace(/^Test /, 'Test: ')), what: rpPlain(t.setup.join(' ')), why: rpPlain(t.why.join(' ')),
    you: /emi|cod|custom|price/i.test(t.id) ? 'Confirm this offer is true for these pieces before we run it.' : 'Nothing. We will do this.', result: rpPlain(t.win) });
  if (o.bet) items.push({ when: 'Weeks 3 and 4', title: `Use more ${o.bet.label.toLowerCase()} ads`, what: `We will move a small part of the budget to ${o.bet.label.toLowerCase()} ads and make 2 new ones.`,
    why: `${o.bet.label} ads brought back ₹${o.bet.roas.toFixed(2)} for every ₹1 on ${Math.round(o.bet.share * 100)}% of the money.`, you: 'Nothing. We will do this.', result: 'The whole account brings back more for the same money.' });
  return items;
}
function rpPlanHtml() {
  const items = rpPlan();
  if (!items.length) return '';
  const groups = ['This week', 'Next week', 'Weeks 3 and 4'];
  const asks = items.filter((x) => !/^Nothing/.test(x.you));
  let n = 0;
  return `<section class="rp-sec"><h2>What we will do next</h2>
    <p class="rp-lead">${items.length} steps for the next 30 days, in order. Each one says what we will do, why, what we need from you, and how we will know it worked.</p>
    <ol class="rp-time">${groups.map((g) => { const list = items.filter((x) => x.when === g); return list.length ? `<li><span class="rp-when">${esc(g)}</span><span>${list.map((x) => esc(x.title)).join(' · ')}</span></li>` : ''; }).join('')}</ol>
    <div class="rp-plan">${groups.flatMap((g) => items.filter((x) => x.when === g)).map((x) => `<article class="rp-step"><div class="rp-sh"><span class="rp-num">${++n}</span><div><span class="chip">${esc(x.when)}</span><h3>${esc(x.title)}</h3></div></div>
      <dl><div><dt>What we will do</dt><dd>${esc(x.what)}</dd></div><div><dt>Why</dt><dd>${esc(x.why)}</dd></div><div><dt>What we need from you</dt><dd>${esc(x.you)}</dd></div><div><dt>How we will know it worked</dt><dd>${esc(x.result)}</dd></div></dl></article>`).join('')}</div>
    ${asks.length ? `<div class="rp-ask"><h3>Your to-do list</h3><ul>${asks.map((x) => `<li><span class="rp-box" aria-hidden="true"></span>${esc(x.you)} <span class="muted small">(${esc(x.title)})</span></li>`).join('')}</ul></div>` : ''}</section>`;
}
function rpWorked(P) {
  const list = (typeof TESTS !== 'undefined' && TESTS.items || []).filter((t) => t.created && t.created >= P.cur.since).slice(0, 8);
  if (!list.length) return '';
  const st = { idea: 'Planned', launched: 'Running', winner: 'Worked', loser: 'Did not work', dropped: 'Dropped' };
  return `<section class="rp-sec"><h2>What we worked on</h2><ul class="rp-work">${list.map((t) => `<li><span class="chip">${esc(st[t.status] || t.status || 'Planned')}</span>${esc(t.label || '')}${t.idea ? ` <span class="muted small">${esc(t.idea)}</span>` : ''}</li>`).join('')}</ul></section>`;
}
function rpWords() {
  return `<section class="rp-sec rp-words"><h2>Words in this report</h2><dl>
    <div><dt>Website sales</dt><dd>Every order on your website, whatever brought the buyer.</dd></div>
    <div><dt>ROAS</dt><dd>Return on ad spend. If ROAS is ₹4, Meta counted ₹4 of sales for every ₹1 of ads.</dd></div>
    <div><dt>Sales for every ₹1 of ads</dt><dd>All website sales divided by ad money. It does not depend on Meta's counting.</dd></div>
    <div><dt>Not available</dt><dd>We do not have this number for these days. It is not zero.</dd></div></dl></section>`;
}
function rpTeam(P) {
  if (!RP.team) return '';
  const v = VIEW, x = v.exclusions, c = P.cur;
  return `<section class="rp-sec rp-teamnotes"><h2>Team notes (not for the client)</h2><ul>
    <li>Website data: ${c.covered} of ${c.n} days have totals${c.typeDays < c.covered ? `, ${c.typeDays} have product types` : ''}.${P.cut ? ` Website sales end ${esc(dateLabel(c.until))}; Meta runs to ${esc(dateLabel(v.range.until))}.` : ''}</li>
    <li>Previous period for website numbers: ${esc(dateLabel(P.prevRaw.since))} to ${esc(dateLabel(P.prevRaw.until))}, ${P.prevRaw.covered} of ${P.prevRaw.n} days with data.${P.ok ? '' : ' Not full, so website changes are not shown.'}</li>
    <li>Targets: ROAS ${v.targets.roas ? v.targets.roas.toFixed(2) + 'x' : 'not set'} (${esc(v.targets.roas_source)}), CPA ${v.targets.cpa ? money(v.targets.cpa) : 'not set'}.</li>
    <li>${x.campaigns.length ? `Left out: ${x.campaigns.length} campaigns (${x.ads} ads, ${money(x.spend)}).` : 'No campaigns left out.'} ${v.totals.ads_without_reported_value} ads had spend but no reported value.</li>
    <li>Meta purchases use each ad set's attribution setting. Website sales come from Metabase (website orders only).</li></ul></section>`;
}

// ---------- page ----------
function reportV2(forFile) {
  if (!SL.data) return '<p class="muted">Loading website sales…</p>';
  const v = VIEW, r = v.range, P = rpPeriods();
  const agency = $('agency').value.trim(), client = $('client').value.trim() || DATA.meta.account_name || 'Your brand', note = $('note').value.trim();
  return `<header class="rp-cover">${agency ? `<div class="r-agency">${esc(agency)}</div>` : ''}
      <div class="rp-title">${esc(client)}</div><div class="rp-sub">Business and Meta ads report</div>
      <div class="rp-dates">${esc(dateLabel(r.since))} to ${esc(dateLabel(r.until))} · ${r.days} days · compared with the ${r.days} days before</div>
      <p class="rp-summary">${rpSummary(P, v.totals)}</p></header>
    ${note ? `<div class="r-note"><b>Our note:</b> ${esc(note)}</div>` : ''}
    <section class="rp-sec"><h2>Your business at a glance</h2><p class="rp-lead">Your whole website, not only ads.${P.cut ? ` Website figures run to ${esc(dateLabel(P.cur.until))}, the latest day we have.` : ''}${String(SL.data.daily_pulled_at || '').slice(0, 10) === P.cur.until ? ` ${esc(shortDate(P.cur.until))} is today, so it shows sales up to ${esc(new Date(SL.data.daily_pulled_at).toLocaleTimeString('en-IN', { hour: 'numeric', minute: '2-digit' }))} only.` : ''}</p>${rpHero(P)}</section>
    ${rpSalesTrend(P)}${rpYear(P)}${rpMeta(P)}${rpAds()}${rpProducts(P)}${rpPeople()}${rpWorked(P)}${rpPlanHtml()}${rpWords()}${rpTeam(P)}
    <footer class="r-foot"><div>Website sales: Metabase, website orders only. Ads: ${esc(sourceLabel())}, captured ${esc(new Date(DATA.meta.captured_at).toLocaleString('en-IN'))}.${forFile ? '' : ' Read-only. Nothing in the ad account was changed.'}</div></footer>`;
}
window.reportHtml = reportV2;
// Report dates end on the last day with website sales, so both sides cover the same days.
async function rpSetPeriod(k) {
  await loadSales();
  const w = DATA.meta.window, lastSales = rpLastSalesDay();
  const end = lastSales && lastSales < w.until ? lastSales : w.until;
  let since, until = end;
  if (k === 'this_month') since = end.slice(0, 8) + '01';
  else if (k === 'last_month') { const d = new Date(end.slice(0, 8) + '01T00:00:00Z'); d.setUTCDate(0); until = d.toISOString().slice(0, 10); since = until.slice(0, 8) + '01'; }
  else since = addDays(end, -(Number(k) - 1));
  if (since < w.since) since = w.since;
  RP.period = k;
  state.since = since; state.until = until; $('since').value = since; $('until').value = until; $('preset').value = 'custom';
  refresh();
}
function rpToolsHtml() {
  const cur = RP.period && state.since === VIEW.range.since ? RP.period : '';
  return `<div class="rp-tools"><div class="seg" role="group" aria-label="Report dates">${RP_PERIODS.map(([v, l]) => `<button type="button" data-rpp="${v}" aria-pressed="${cur === v}">${l}</button>`).join('')}</div>
    <div class="seg" role="group" aria-label="Who is reading"><button type="button" data-rpteam="0" aria-pressed="${!RP.team}">Client view</button><button type="button" data-rpteam="1" aria-pressed="${RP.team}">Team view</button></div></div>`;
}
window.renderReport = async function renderReport() {
  if (!VIEW) return;
  const box = $('report');
  if (!$('rpTools')) { const t = document.createElement('div'); t.id = 'rpTools'; box.parentNode.insertBefore(t, box); }
  $('rpTools').innerHTML = rpToolsHtml();
  if (!SL.data) { box.innerHTML = reportV2(false); await loadSales(); await docsBoot(); }
  box.innerHTML = reportV2(false);
};
document.addEventListener('click', (e) => {
  const p = e.target.closest('[data-rpp]');
  if (p) { rpSetPeriod(p.dataset.rpp); return; }
  const t = e.target.closest('[data-rpteam]');
  if (t) { RP.team = t.dataset.rpteam === '1'; window.renderReport(); }
});
