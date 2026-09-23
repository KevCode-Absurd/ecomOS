// Brand sales tab: website sales from the Metabase dashboard next to Meta ad data.
// sales.json holds monthly dashboard cards (website orders only), the same cards per day for recent days, and daily GA4 rows.
// Missing values stay unavailable, never zero.
'use strict';

const SL = { data: null, loading: null, month: null, err: null };

const CATS = ['Earrings', 'Chains', 'Bracelets', 'Pendants', 'Rings', 'Nosepins', 'Other'];
const CAT_COLOR = { Earrings: '#f2b92b', Chains: '#2a78d6', Bracelets: '#eb6834', Pendants: '#1baf7a', Rings: '#e87ba4', Nosepins: '#7a5200', Other: '#b9b5ab', Mixed: '#d9d6ce' };
const TYPE_CAT = [
  [/earring|jhumki|hook/i, 'Earrings'], [/chain|necklace/i, 'Chains'], [/bracelet|bangle|anklet/i, 'Bracelets'],
  [/pendant|charm/i, 'Pendants'], [/ring/i, 'Rings'], [/nose/i, 'Nosepins'],
];
const AD_CAT = [
  [/\b(earring|earrings|studs?|jhumk\w*|hoops?|danglers?)\b/i, 'Earrings'], [/\b(chains?|necklaces?|lariat|choker)\b/i, 'Chains'],
  [/\b(bracelets?|bangles?|tennis)\b/i, 'Bracelets'], [/\b(pendants?|charms?)\b/i, 'Pendants'], [/\b(rings?|eternity)\b/i, 'Rings'],
  [/\b(nose ?pins?|nosepins?)\b/i, 'Nosepins'],
];
const typeCat = (t) => { for (const [re, c] of TYPE_CAT) if (re.test(t)) return c; return 'Other'; };
const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
const mLabel = (k, yr = true) => MONTHS[+k.slice(5) - 1] + (yr ? ' ' + k.slice(2, 4) : '');
const pct = (v, d = 0) => (v === null || v === undefined || !Number.isFinite(v) ? '–' : (v * 100).toFixed(d) + '%');
const xx = (v) => (v === null || v === undefined || !Number.isFinite(v) ? '–' : v.toFixed(1) + 'x');
const baseCode = (c) => String(c || '').split('_')[0].trim();
const cleanName = (n) => String(n || '').replace(/\s*\((?:[^)]*)\)\s*/g, ' ').replace(/\s+(\d+)$/, '').replace(/\s+/g, ' ').trim();

async function loadSales() {
  if (SL.data) return SL.data;
  if (!SL.loading) {
    SL.loading = fetch('sales.json').then((r) => (r.ok ? r.json() : Promise.reject(new Error('sales.json not found'))))
      .then((d) => { SL.data = d; return d; })
      .catch((e) => { SL.err = e.message; return null; });
  }
  return SL.loading;
}

// ---------- numbers ----------
function monthStats(k) {
  const m = SL.data.months[k];
  if (!m) return null;
  const stock = m.ot.Stock || [0, 0], custom = m.ot['Custom Made'] || [0, 0];
  const sales = Object.values(m.ot).reduce((t, v) => t + (v[0] || 0), 0);
  const items = m.items;
  return { k, sales, items, aiv: items ? sales / items : null, stock: stock[0], custom: custom[0], customShare: sales ? custom[0] / sales : null,
    refund: m.refund, retItems: m.ret_items, refundRate: sales && m.refund !== null ? m.refund / sales : null };
}

let AD_TAGS = null;
function adCat(ad) {
  const c = ad.creative || {};
  for (const txt of [ad.name, c.headline, c.name, ad.adset_name, c.primary_text]) {
    if (!txt) continue;
    const hits = new Set();
    for (const [re, cat] of AD_CAT) if (re.test(txt)) hits.add(cat);
    if (hits.size === 1) return [...hits][0];
    if (hits.size > 1) return 'Mixed';
  }
  return 'Mixed';
}
function adTags() {
  if (!AD_TAGS) { AD_TAGS = {}; for (const [id, ad] of Object.entries(DATA.ads)) AD_TAGS[id] = adCat(ad); }
  return AD_TAGS;
}
// Daily ad rows are [day index, spend, purchases, value, impressions, clicks].
let ISO = null;
const dayIso = (i) => { if (!ISO) ISO = []; return ISO[i] || (ISO[i] = ENGINE.iso(i)); };
function metaMonth(k) {
  const tags = adTags();
  const out = { spend: 0, value: 0, valueSeen: false, purchases: 0, cat: {} };
  for (const [id, rows] of Object.entries(DATA.daily)) {
    for (const r of rows) {
      if (dayIso(r[0]).slice(0, 7) !== k) continue;
      out.spend += r[1] || 0; out.purchases += r[2] || 0;
      if (r[3] !== null && r[3] !== undefined) { out.value += r[3]; out.valueSeen = true; }
      const c = tags[id] || 'Mixed';
      out.cat[c] = (out.cat[c] || 0) + (r[1] || 0);
    }
  }
  const w = DATA.meta.window;
  out.partial = w.since.slice(0, 7) === k && w.since.slice(8) !== '01';
  out.covered = k >= w.since.slice(0, 7) && k <= w.until.slice(0, 7);
  return out;
}
function metaDaily() {
  const map = {};
  for (const rows of Object.values(DATA.daily)) for (const r of rows) {
    const d = dayIso(r[0]);
    const o = map[d] || (map[d] = { spend: 0, value: 0 });
    o.spend += r[1] || 0; o.value += r[3] || 0;
  }
  return map;
}
function catSales(k) {
  const out = {};
  for (const [, type, v, n] of monthObj(k).types) {
    const c = typeCat(type);
    const o = out[c] || (out[c] = { v: 0, n: 0 });
    o.v += v || 0; o.n += n || 0;
  }
  return out;
}
function skuRollup(keys) {
  const map = {};
  for (const k of keys) for (const [metal, code, name, v, n] of monthObj(k).skus) {
    const b = baseCode(code);
    const o = map[b] || (map[b] = { code: b, name: cleanName(name), metal, v: 0, n: 0, months: {} });
    o.v += v || 0; o.n += n || 0; o.months[k] = (o.months[k] || 0) + n;
    if (!/14K/.test(name) && o.name.includes('14K')) o.name = cleanName(name);
  }
  return Object.values(map);
}
let AD_TEXT = null;
function adText() {
  if (!AD_TEXT) AD_TEXT = Object.values(DATA.ads).map((a) => [a.name, a.creative && a.creative.headline, a.creative && a.creative.primary_text, a.creative && a.creative.name].join(' ')).join('\n').toLowerCase();
  return AD_TEXT;
}
const STOP = new Set(['18k', '14k', '22k', 'gold', 'yellow', 'rose', 'white', 'the', 'and', '&', 'with', 'without', 'chain', 'earrings', 'earring', 'bracelet', 'pendant', 'ring', 'stud', 'studs', 'dangle', 'drop', 'hook', 'inches', 'natural']);
function inAds(name) {
  const words = name.toLowerCase().replace(/[^a-z\s]/g, ' ').split(/\s+/).filter((w) => w.length > 2 && !STOP.has(w));
  const key = words.slice(0, 2);
  if (key.length < 2) return null;
  return adText().includes(key.join(' '));
}

// ---------- charts ----------
function salesChart(keys) {
  const W = 900, H = 300, L = 60, R = 14, T = 16, B = 34;
  const rows = keys.map((k) => { const s = monthStats(k), m = metaMonth(k); return { k, s, m }; });
  const max = Math.max(...rows.map((r) => r.s.sales)) * 1.08 || 1;
  const slot = (W - L - R) / rows.length, bw = Math.min(46, slot * 0.62);
  const y = (v) => T + (H - T - B) * (1 - v / max);
  const ticks = [0, 0.25, 0.5, 0.75, 1].map((f) => max * f);
  let g = ticks.map((t) => `<line class="gl" x1="${L}" x2="${W - R}" y1="${y(t).toFixed(1)}" y2="${y(t).toFixed(1)}"/><text class="tl" x="${L - 8}" y="${(y(t) + 3).toFixed(1)}" text-anchor="end">${esc(compact(t))}</text>`).join('');
  const pts = [];
  rows.forEach((r, i) => {
    const cx = L + slot * i + slot / 2;
    const sales = r.s.sales, meta = r.m.covered && r.m.valueSeen ? Math.min(r.m.value, sales) : null;
    const tip = [`${mLabel(r.k)}${r.k === SL.data.last ? ' so far' : ''}`, 'Website sales', compact(sales), 'Meta spend', r.m.covered ? compact(r.m.spend) + (r.m.partial ? ' (partial)' : '') : 'Unavailable',
      'Meta says it drove', meta !== null ? compact(r.m.value) : 'Unavailable', 'Sales per ₹1 of ads', r.m.covered && r.m.spend && !r.m.partial ? xx(sales / r.m.spend) : 'Unavailable'].join('|');
    g += `<g data-tip="${esc(tip)}"><rect x="${(cx - slot / 2).toFixed(1)}" y="${T}" width="${slot.toFixed(1)}" height="${H - T - B}" style="fill:transparent"/>
      <rect x="${(cx - bw / 2).toFixed(1)}" y="${y(sales).toFixed(1)}" width="${bw.toFixed(1)}" height="${(y(0) - y(sales)).toFixed(1)}" rx="7" style="fill:${r.k === SL.month ? 'var(--gold)' : '#f6d985'}"/>
      ${meta !== null ? `<rect x="${(cx - bw / 2 + 6).toFixed(1)}" y="${y(meta).toFixed(1)}" width="${(bw - 12).toFixed(1)}" height="${(y(0) - y(meta)).toFixed(1)}" rx="4" style="fill:var(--ink);opacity:.82"/>` : ''}
      <text class="tl" x="${cx.toFixed(1)}" y="${H - 12}" text-anchor="middle">${esc(mLabel(r.k, r.k.endsWith('-01') || i === 0))}</text></g>`;
    if (r.m.covered && !r.m.partial) pts.push([cx, y(r.m.spend)]);
  });
  const line = pts.length > 1 ? `<path d="${pts.map((p, i) => (i ? 'L' : 'M') + p[0].toFixed(1) + ' ' + p[1].toFixed(1)).join(' ')}" style="fill:none;stroke:var(--spend);stroke-width:2.5"/>${pts.map((p) => `<circle cx="${p[0].toFixed(1)}" cy="${p[1].toFixed(1)}" r="3.5" style="fill:var(--spend)"/>`).join('')}` : '';
  return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Website sales, Meta claimed value and Meta spend by month">${g}${line}</svg>`;
}

function trafficChart(ga, md) {
  const W = 900, L = 60, R = 14, rowH = 64, gap = 14;
  const n = ga.length;
  if (!n) return '<p class="muted small">No traffic rows yet.</p>';
  const slot = (W - L - R) / n;
  const series = [
    { key: 'visits', label: 'Visits', color: '#c9c4b8', get: (r) => r[1], f: (v) => Math.round(v).toLocaleString('en-IN') },
    { key: 'spend', label: 'Meta spend', color: 'var(--spend)', get: (r) => (md[r[0]] ? md[r[0]].spend : null), f: compact },
    { key: 'orders', label: 'Orders', color: 'var(--gold)', get: (r) => r[4], f: (v) => String(v) },
    { key: 'conv', label: 'Conversion', color: 'var(--ink)', get: (r) => (r[4] !== null && r[1] ? r[4] / r[1] : null), f: (v) => (v * 100).toFixed(3) + '%' },
  ];
  let out = '';
  series.forEach((s, si) => {
    const top = si * (rowH + gap) + 6;
    const vals = ga.map(s.get);
    const max = Math.max(...vals.filter((v) => v !== null && v !== undefined)) || 1;
    out += `<text class="tl" x="0" y="${top + 12}" style="font-weight:700;fill:var(--ink)">${s.label}</text><text class="tl" x="0" y="${top + 26}">max ${esc(s.f(max))}</text>`;
    vals.forEach((v, i) => {
      if (v === null || v === undefined) { out += `<rect x="${(L + slot * i + slot * 0.15).toFixed(1)}" y="${top + rowH - 3}" width="${Math.max(1, slot * 0.7).toFixed(1)}" height="3" style="fill:var(--bad)"/>`; return; }
      const h = Math.max(1, (rowH - 4) * v / max);
      out += `<rect x="${(L + slot * i + slot * 0.15).toFixed(1)}" y="${(top + rowH - h).toFixed(1)}" width="${Math.max(1, slot * 0.7).toFixed(1)}" height="${h.toFixed(1)}" rx="1.5" style="fill:${s.color}"/>`;
    });
  });
  const totalH = series.length * (rowH + gap) + 16;
  ga.forEach((r, i) => {
    const m = md[r[0]];
    const tip = [dateLabel(r[0]), 'Visits', r[1].toLocaleString('en-IN'), 'Add to carts', String(r[2]), 'Orders', r[4] !== null ? String(r[4]) : 'Unavailable', 'Sales', r[3] !== null ? compact(r[3]) : 'Unavailable',
      'Conversion', r[4] !== null && r[1] ? (r[4] / r[1] * 100).toFixed(3) + '%' : 'Unavailable', 'Meta spend', m ? compact(m.spend) : 'Unavailable'].join('|');
    out += `<rect data-tip="${esc(tip)}" x="${(L + slot * i).toFixed(1)}" y="0" width="${slot.toFixed(1)}" height="${totalH - 16}" style="fill:transparent"/>`;
    if (r[0].endsWith('-01')) out += `<text class="tl" x="${(L + slot * i).toFixed(1)}" y="${totalH - 2}">${esc(mLabel(r[0].slice(0, 7)))}</text>`;
  });
  return `<svg viewBox="0 0 ${W} ${totalH}" role="img" aria-label="Daily visits, Meta spend, orders and conversion">${out}</svg>`;
}

function heatRows(keys) {
  const per = keys.map((k) => catSales(k));
  let max = 0;
  for (const p of per) for (const c of CATS) max = Math.max(max, (p[c] || {}).v || 0);
  const head = `<tr><th>Category</th>${keys.map((k) => `<th class="n">${esc(mLabel(k, k.endsWith('-01') || k === keys[0]))}</th>`).join('')}</tr>`;
  const body = CATS.map((c) => `<tr><th scope="row"><i class="cdot" style="background:${CAT_COLOR[c]}"></i>${c}</th>${per.map((p, i) => {
    const o = p[c]; if (!o || !o.v) return '<td class="heat na-cell">–</td>';
    const a = 0.08 + 0.8 * (o.v / max);
    return `<td class="heat" style="background:rgba(242,185,43,${a.toFixed(2)})" data-tip="${esc(`${c}, ${mLabel(keys[i])}|Sales|${compact(o.v)}|Items|${o.n}|Avg item|${compact(o.v / o.n)}`)}"><b>${esc(compact(o.v).replace('₹', ''))}</b><span>${o.n} sold</span></td>`;
  }).join('')}</tr>`).join('');
  return `<div class="scroll"><table class="heatmap sheat">${head}${body}</table></div>`;
}

function gapBars(k) {
  const cs = catSales(k), mm = isRange(k) ? metaRange(...rangeParts(k)) : metaMonth(k);
  const salesTot = Object.values(cs).reduce((t, o) => t + o.v, 0);
  const tagged = CATS.reduce((t, c) => t + (mm.cat[c] || 0), 0);
  const mixed = mm.cat.Mixed || 0;
  const rows = CATS.filter((c) => c !== 'Other').map((c) => ({ c, s: salesTot ? (cs[c] || { v: 0 }).v / salesTot : 0, a: tagged ? (mm.cat[c] || 0) / tagged : null, spend: mm.cat[c] || 0 }));
  const max = Math.max(...rows.map((r) => Math.max(r.s, r.a || 0))) || 1;
  const html = rows.map((r) => `<div class="gap-row" data-tip="${esc(`${r.c}|Share of website sales|${pct(r.s, 1)}|Share of product ad spend|${r.a === null ? 'Unavailable' : pct(r.a, 1)}|Ad spend|${compact(r.spend)}`)}">
    <span class="gl-name"><i class="cdot" style="background:${CAT_COLOR[r.c]}"></i>${r.c}</span>
    <span class="gl-bars"><span class="gb s" style="width:${(r.s / max * 100).toFixed(1)}%"></span><span class="gb a" style="width:${((r.a || 0) / max * 100).toFixed(1)}%"></span></span>
    <span class="gl-val"><b>${pct(r.s)}</b><em>${r.a === null ? '–' : pct(r.a)}</em></span></div>`).join('');
  return { html, rows, mixedShare: mm.spend ? mixed / mm.spend : null, covered: mm.covered };
}

function bandBars(k) {
  const m = monthObj(k);
  const order = ['0-10000', '10000-25000', '25000-40000', '40000-60000', '60000+'];
  const lab = { '0-10000': 'Under ₹10K', '10000-25000': '₹10K to 25K', '25000-40000': '₹25K to 40K', '40000-60000': '₹40K to 60K', '60000+': '₹60K+' };
  const g = Object.fromEntries(m.bands.filter((b) => b[0] === 'g').map((b) => [b[1], b[2]]));
  const tot = order.reduce((t, b) => t + (g[b] || 0), 0) || 1;
  const mx = Math.max(...order.map((b) => g[b] || 0)) || 1;
  return order.map((b) => `<div class="hbar" data-tip="${esc(`${lab[b]}|Gold items sold|${g[b] || 0}|Share|${pct((g[b] || 0) / tot, 1)}`)}"><span class="l">${lab[b]}</span><span class="t"><i style="width:${Math.max(2, (g[b] || 0) / mx * 100)}%"></i></span><span class="r">${g[b] || 0}</span></div>`).join('');
}
function mixList(rows, fmtV) {
  const tot = rows.reduce((t, r) => t + r[1], 0) || 1;
  const cols = ['var(--gold)', 'var(--spend)', 'var(--roas)', 'var(--s3)', 'var(--s5)', '#7a5200', '#b9b5ab'];
  return `<div class="stackbar">${rows.map((r, i) => `<span style="flex:${r[1]};background:${cols[i % cols.length]}" data-tip="${esc(`${r[0]}|Value|${fmtV(r[1])}|Share|${pct(r[1] / tot, 1)}`)}"></span>`).join('')}</div>
    ${rows.map((r, i) => `<div class="mixrow"><i style="background:${cols[i % cols.length]}"></i><span>${esc(r[0])}</span><span class="v">${esc(fmtV(r[1]))}</span><span class="r">${pct(r[1] / tot)}</span></div>`).join('')}`;
}


// ---------- day view: daily Metabase cards (sales.json "daily") next to daily Meta and GA ----------
// A day range is summed into the same shape as a month, stored under a key like "r:2026-09-01~2026-09-15".
const SD = { mode: 'months', since: null, until: null, sort: 'date' };
const isRange = (k) => typeof k === 'string' && k.startsWith('r:');
const rangeKey = (a, b) => `r:${a}~${b}`;
const rangeParts = (k) => k.slice(2).split('~');
function dailyDays() { return Object.keys((SL.data && SL.data.daily) || {}).sort(); }
function addDays(iso, n) { const t = new Date(iso + 'T00:00:00Z'); t.setUTCDate(t.getUTCDate() + n); return t.toISOString().slice(0, 10); }
function dayLabel(iso) { return new Date(iso + 'T00:00:00Z').toLocaleDateString('en-IN', { day: 'numeric', month: 'short', timeZone: 'UTC' }); }
function weekday(iso) { return new Date(iso + 'T00:00:00Z').toLocaleDateString('en-IN', { weekday: 'short', timeZone: 'UTC' }); }
// Sum daily entries into a month-shaped object. Lists are merged by their label columns.
function rangeMonth(since, until) {
  const days = dailyDays().filter((d) => d >= since && d <= until);
  if (!days.length) return null;
  const out = { items: 0, orders: 0, sales: 0, ot: {}, refund: null, ret_items: 0, karat: [], types: [], bands: [], pay: [], ret: [], skus: [], days: days.length };
  const merge = (list, row, nKey) => {
    const key = row.slice(0, nKey).join('\u0001');
    const f = list.find((r) => r.slice(0, nKey).join('\u0001') === key);
    if (f) { for (let i = nKey; i < row.length; i++) f[i] = (f[i] || 0) + (row[i] || 0); } else list.push(row.slice());
  };
  for (const d of days) {
    const x = SL.data.daily[d];
    out.items += x.items || 0; out.orders += x.orders || 0; out.sales += x.sales || 0; out.ret_items += x.ret_items || 0;
    if (x.refund !== null && x.refund !== undefined) out.refund = (out.refund || 0) + x.refund;
    for (const [t, v] of Object.entries(x.ot || {})) { const o = out.ot[t] || (out.ot[t] = [0, 0]); o[0] += v[0] || 0; o[1] += v[1] || 0; }
    x.karat.forEach((r) => merge(out.karat, r, 1));
    x.types.forEach((r) => merge(out.types, r, 2));
    x.bands.forEach((r) => merge(out.bands, r, 2));
    x.pay.forEach((r) => merge(out.pay, r, 1));
    x.ret.forEach((r) => merge(out.ret, r, 2));
    x.skus.forEach((r) => merge(out.skus, r, 3));
  }
  if (out.refund === null) out.refund = 0;
  return out;
}
function monthObj(k) {
  if (!isRange(k)) return SL.data.months[k];
  SL.ranges = SL.ranges || {};
  if (!(k in SL.ranges)) { const [a, b] = rangeParts(k); SL.ranges[k] = rangeMonth(a, b); }
  return SL.ranges[k];
}
function rangeLabel(k) {
  if (!isRange(k)) return mLabel(k);
  const [a, b] = rangeParts(k);
  return a === b ? dayLabel(a) : `${dayLabel(a)} to ${dayLabel(b)}`;
}
function metaDayMap() {
  if (SD.meta) return SD.meta;
  const tags = adTags(), map = {};
  for (const [id, rows] of Object.entries(DATA.daily)) for (const r of rows) {
    const d = dayIso(r[0]);
    const o = map[d] || (map[d] = { spend: 0, value: 0, valueSeen: false, purchases: 0, cat: {} });
    o.spend += r[1] || 0; o.purchases += r[2] || 0;
    if (r[3] !== null && r[3] !== undefined) { o.value += r[3]; o.valueSeen = true; }
    const c = tags[id] || 'Mixed';
    o.cat[c] = (o.cat[c] || 0) + (r[1] || 0);
  }
  return (SD.meta = map);
}
function metaRange(since, until) {
  const map = metaDayMap(), out = { spend: 0, value: 0, valueSeen: false, purchases: 0, cat: {}, partial: false };
  const w = DATA.meta.window;
  out.covered = since >= w.since && until <= w.until;
  for (let d = since; d <= until; d = addDays(d, 1)) {
    const o = map[d]; if (!o) continue;
    out.spend += o.spend; out.value += o.value; out.purchases += o.purchases; out.valueSeen = out.valueSeen || o.valueSeen;
    for (const [c, v] of Object.entries(o.cat)) out.cat[c] = (out.cat[c] || 0) + v;
  }
  return out;
}
function gaMap() {
  if (SD.ga) return SD.ga;
  const m = {};
  for (const r of SL.data.ga || []) m[r[0]] = { visits: r[1], carts: r[2], gaSales: r[3], gaOrders: r[4] };
  return (SD.ga = m);
}
// One row per day for the table and chart.
function dayRows(since, until) {
  const md = metaDayMap(), ga = gaMap(), out = [];
  for (const d of dailyDays().filter((x) => x >= since && x <= until)) {
    const x = SL.data.daily[d], m = md[d] || null, g = ga[d] || null;
    out.push({ d, sales: x.sales, orders: x.orders, items: x.items, aov: x.orders ? x.sales / x.orders : null, refund: x.refund,
      spend: m ? m.spend : null, claimed: m && m.valueSeen ? m.value : null, perRupee: m && m.spend ? x.sales / m.spend : null,
      visits: g ? g.visits : null, carts: g ? g.carts : null, conv: g && g.visits ? x.orders / g.visits : null });
  }
  return out;
}
function rangeStats(since, until) {
  const mo = rangeMonth(since, until);
  if (!mo) return null;
  const m = metaRange(since, until), rows = dayRows(since, until);
  const visits = rows.reduce((t, r) => t + (r.visits || 0), 0), vDays = rows.filter((r) => r.visits !== null).length;
  const ordersV = rows.filter((r) => r.visits !== null).reduce((t, r) => t + r.orders, 0);
  return { mo, m, rows, sales: mo.sales, orders: mo.orders, items: mo.items, aov: mo.orders ? mo.sales / mo.orders : null,
    refund: mo.refund, retItems: mo.ret_items, perRupee: m.spend ? mo.sales / m.spend : null, claim: m.valueSeen && mo.sales ? m.value / mo.sales : null,
    conv: vDays === rows.length && visits ? ordersV / visits : null, visits: vDays === rows.length ? visits : null, days: rows.length };
}
function dayChart(rows) {
  if (!rows.length) return '<p class="muted">No days in this range.</p>';
  const W = 900, H = 260, L = 56, R = 48, T = 16, B = 40;
  const maxS = Math.max(...rows.map((r) => Math.max(r.sales || 0, r.claimed || 0)), 1);
  const maxM = Math.max(...rows.map((r) => r.spend || 0), 1);
  const slot = (W - L - R) / rows.length, bw = Math.max(3, Math.min(22, slot * 0.62));
  const y = (v) => T + (H - T - B) * (1 - v / maxS), y2 = (v) => T + (H - T - B) * (1 - v / maxM);
  const ticks = [0, 0.5, 1].map((f) => `<line x1="${L}" x2="${W - R}" y1="${y(maxS * f).toFixed(1)}" y2="${y(maxS * f).toFixed(1)}" style="stroke:var(--line)"${f ? ' stroke-dasharray="3 4"' : ''}/><text x="${L - 6}" y="${(y(maxS * f) + 4).toFixed(1)}" text-anchor="end" style="fill:var(--muted);font-size:11px">${esc(compact(maxS * f))}</text><text x="${W - R + 6}" y="${(y2(maxM * f) + 4).toFixed(1)}" style="fill:var(--spend);font-size:11px">${esc(compact(maxM * f))}</text>`).join('');
  const every = Math.ceil(rows.length / 12);
  const bars = rows.map((r, i) => {
    const cx = L + slot * i + slot / 2;
    const tip = esc([`${weekday(r.d)} ${dayLabel(r.d)}`, 'Website sales', compact(r.sales), 'Orders', r.orders, 'Items', r.items, 'Meta spend', r.spend !== null ? compact(r.spend) : 'Unavailable', 'Meta claimed', r.claimed !== null ? compact(r.claimed) : 'Unavailable', 'Sales per ₹1 of Meta', r.perRupee !== null ? '₹' + r.perRupee.toFixed(1) : 'Unavailable', 'Visits', r.visits !== null ? r.visits.toLocaleString('en-IN') : 'Unavailable'].join('|'));
    return `<g class="hov" data-tip="${tip}"><rect x="${(cx - slot / 2).toFixed(1)}" y="${T}" width="${slot.toFixed(1)}" height="${H - T - B}" fill="transparent"/>
      <rect x="${(cx - bw / 2).toFixed(1)}" y="${y(r.sales || 0).toFixed(1)}" width="${bw.toFixed(1)}" height="${(H - B - y(r.sales || 0)).toFixed(1)}" rx="3" style="fill:var(--gold)"/>
      ${r.claimed !== null ? `<rect x="${(cx - bw / 4).toFixed(1)}" y="${y(r.claimed).toFixed(1)}" width="${(bw / 2).toFixed(1)}" height="${(H - B - y(r.claimed)).toFixed(1)}" rx="2" style="fill:var(--ink)"/>` : ''}
      ${i % every === 0 ? `<text x="${cx.toFixed(1)}" y="${H - B + 16}" text-anchor="middle" style="fill:var(--muted);font-size:11px">${esc(dayLabel(r.d))}</text>` : ''}</g>`;
  }).join('');
  const pts = rows.map((r, i) => (r.spend === null ? null : [L + slot * i + slot / 2, y2(r.spend)])).filter(Boolean);
  const line = pts.length > 1 ? `<path d="${pts.map((p, i) => `${i ? 'L' : 'M'}${p[0].toFixed(1)},${p[1].toFixed(1)}`).join(' ')}" style="fill:none;stroke:var(--spend);stroke-width:2"/>` : '';
  return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Website sales and Meta spend by day" class="daychart">${ticks}${bars}${line}</svg>`;
}
function dayInsights(st, prev) {
  const out = [], rows = st.rows;
  if (rows.length >= 2) {
    const best = rows.reduce((a, b) => (b.sales > a.sales ? b : a)), worst = rows.reduce((a, b) => (b.sales < a.sales ? b : a));
    out.push({ tone: 'up', title: `Best day: ${weekday(best.d)} ${dayLabel(best.d)}, ${compact(best.sales)}`, body: `${best.orders} order${best.orders === 1 ? '' : 's'}${best.spend !== null ? ` on ${compact(best.spend)} of Meta spend` : ''}. Worst day: ${dayLabel(worst.d)}, ${compact(worst.sales)} from ${worst.orders} order${worst.orders === 1 ? '' : 's'}.` });
    const zero = rows.filter((r) => !r.orders);
    if (zero.length) out.push({ tone: 'down', title: `${zero.length} day${zero.length > 1 ? 's' : ''} with no website orders`, body: zero.slice(0, 6).map((r) => `${dayLabel(r.d)}${r.spend !== null ? ` (${compact(r.spend)} Meta spend)` : ''}`).join(', ') + '.' });
  }
  if (rows.length >= 14) {
    const wd = {};
    rows.forEach((r) => { const k = weekday(r.d); const o = wd[k] || (wd[k] = { s: 0, n: 0 }); o.s += r.sales; o.n += 1; });
    const list = Object.entries(wd).map(([k, o]) => [k, o.s / o.n]).sort((a, b) => b[1] - a[1]);
    out.push({ tone: 'mix', title: `${list[0][0]} sells most, ${list[list.length - 1][0]} least`, body: `Average website sales: ${list.map(([k, v]) => `${k} ${compact(v)}`).join(', ')}.` });
  }
  if (prev && prev.sales && st.m.spend && prev.m.spend) {
    const ds = (st.sales - prev.sales) / prev.sales, dm = (st.m.spend - prev.m.spend) / prev.m.spend;
    out.push({ tone: ds >= dm ? 'up' : 'down', title: `Sales ${ds >= 0 ? 'up' : 'down'} ${Math.abs(ds * 100).toFixed(0)}%, Meta spend ${dm >= 0 ? 'up' : 'down'} ${Math.abs(dm * 100).toFixed(0)}%`, body: `Compared with the ${st.days} days before. ${ds >= dm ? 'Sales kept pace with spend.' : 'Spend grew faster than sales. Check which ads took the extra money.'}` });
  }
  const aovs = rows.filter((r) => r.orders).map((r) => r.aov);
  if (aovs.length >= 5 && st.aov) {
    const big = rows.filter((r) => r.orders && r.sales > 0.2 * st.sales);
    if (big.length) out.push({ tone: 'mix', title: `${big.length} day${big.length > 1 ? 's' : ''} made over 20% of sales`, body: `${big.map((r) => `${dayLabel(r.d)} (${compact(r.sales)}, ${r.orders} order${r.orders === 1 ? '' : 's'})`).join(', ')}. With high ticket orders, 1 big order moves the week. Judge ads on 7 days or more.` });
  }
  return out;
}
function daysCsv(rows) {
  const head = ['Date', 'Website sales', 'Orders', 'Items', 'Average order value', 'Refunds', 'Meta spend', 'Meta claimed value', 'Sales per 1 rupee of Meta', 'Visits', 'Add to carts', 'Conversion'];
  const cell = (v) => (v === null || v === undefined ? '' : typeof v === 'number' ? String(Math.round(v * 1000) / 1000) : `"${String(v).replace(/"/g, '""')}"`);
  return [head.join(','), ...rows.map((r) => [r.d, r.sales, r.orders, r.items, r.aov, r.refund, r.spend, r.claimed, r.perRupee, r.visits, r.carts, r.conv].map(cell).join(','))].join('\n');
}
function daysView() {
  const all = dailyDays();
  if (!all.length) return '<p class="muted">Daily sales are not loaded yet.</p>';
  const first = all[0], last = all[all.length - 1];
  if (!SD.until || SD.until > last || SD.until < first) SD.until = last;
  if (!SD.since || SD.since < first || SD.since > SD.until) SD.since = addDays(SD.until, -13) < first ? first : addDays(SD.until, -13);
  const st = rangeStats(SD.since, SD.until);
  const n = st.days, pSince = addDays(SD.since, -n), pUntil = addDays(SD.since, -1);
  const prev = pSince >= first ? rangeStats(pSince, pUntil) : null;
  const k = rangeKey(SD.since, SD.until);
  const top = skuRollup([k]).sort((a, b) => b.n - a.n || b.v - a.v).slice(0, 10);
  const gb = gapBars(k), ins = dayInsights(st, prev);
  const pay = monthObj(k).pay.slice().sort((a, b) => b[1] - a[1]);
  const presets = [['1', 'Yesterday'], ['7', '7 days'], ['14', '14 days'], ['30', '30 days'], ['mtd', 'This month'], ['lm', 'Last month']];
  const sorted = st.rows.slice().sort((a, b) => (SD.sort === 'date' ? b.d.localeCompare(a.d) : (b[SD.sort] ?? -1) - (a[SD.sort] ?? -1)));
  const th = (key, label) => `<th class="n"><button type="button" class="sortbtn${SD.sort === key ? ' on' : ''}" data-dsort="${key}">${label}</button></th>`;
  return `<div class="sd-bar">
      <div class="seg" role="group" aria-label="Quick ranges">${presets.map(([v, l]) => `<button type="button" data-dpreset="${v}">${l}</button>`).join('')}</div>
      <label class="field">From <input type="date" id="sdSince" min="${first}" max="${last}" value="${SD.since}"></label>
      <label class="field">To <input type="date" id="sdUntil" min="${first}" max="${last}" value="${SD.until}"></label>
      <span class="small muted">Daily data from ${esc(dayLabel(first))} to ${esc(dayLabel(last))}.</span></div>
  <div class="bento">
    <section class="tile hero c-4"><div class="label">Website sales · ${esc(rangeLabel(k))}</div><div class="big">${compact(st.sales)}</div>
      <div>${prev ? change(st.sales, prev.sales) + ` <span class="small">vs the ${n} day${n > 1 ? 's' : ''} before</span>` : ''}</div>
      <div class="spark-wrap">${sparkSvg(st.rows.map((r) => r.sales), { color: 'var(--on-gold)', W: 300, H: 64 })}</div></section>
    <div class="c-8 sl-kpis">
      ${kpi('Orders', st.orders, prev ? change(st.orders, prev.orders) + ' vs before' : `${n} day${n > 1 ? 's' : ''}`)}
      ${kpi('Average order value', compact(st.aov), prev ? change(st.aov, prev.aov) + ' vs before' : '')}
      ${kpi('Meta spend', st.m.covered ? compact(st.m.spend) : '–', st.m.covered ? (prev ? change(st.m.spend, prev.m.spend, -1) + ' vs before' : '') : 'No Meta data for these days')}
      ${kpi('Sales per ₹1 of Meta', st.perRupee !== null ? '₹' + st.perRupee.toFixed(1) : '–', prev && prev.perRupee !== null ? `₹${prev.perRupee.toFixed(1)} before` : 'All website sales ÷ Meta spend', 'gold')}
      ${kpi('Sales Meta claims', st.claim !== null ? pct(st.claim) : '–', prev && prev.claim !== null ? pct(prev.claim) + ' before' : 'Unavailable')}
      ${kpi('Conversion', st.conv !== null ? pct(st.conv, 3) : '–', st.visits !== null ? `${st.orders} orders from ${st.visits.toLocaleString('en-IN')} visits` : 'Visits unavailable for some days')}
    </div>
    <section class="tile c-12 sl-ins"><div class="tile-head"><div><h2>What stands out</h2><div class="sub">Built from these days</div></div></div>
      <div class="alerts">${ins.map((x) => `<div class="alert ${x.tone === 'up' ? 'up' : x.tone === 'down' ? 'down' : ''}"><b>${esc(x.title)}</b><span class="small">${esc(x.body)}</span></div>`).join('') || '<p class="muted">Pick at least 2 days.</p>'}</div></section>
    <section class="tile flow c-12"><div class="tile-head"><div><h2>Website sales vs Meta, by day</h2><div class="sub">Gold bars: website sales. Dark bars: sales Meta says it drove. Blue line: Meta spend (right scale). Hover a day.</div></div></div>
      ${dayChart(st.rows)}
      <div class="legend"><span><i style="background:var(--gold)"></i>Website sales</span><span><i style="background:var(--ink)"></i>Meta claimed</span><span><i style="background:var(--spend)"></i>Meta spend</span></div></section>
    <section class="tile c-12"><div class="tile-head"><div><h2>Day by day</h2><div class="sub">Click a column to sort. Visits come from Google Analytics.</div></div><button class="btn ghost small-btn" type="button" id="sdCsv">Export CSV</button></div>
      <div class="scroll"><table class="sdtable"><tr>${th('date', 'Date')}${th('sales', 'Sales')}${th('orders', 'Orders')}${th('items', 'Items')}${th('aov', 'Avg order')}${th('spend', 'Meta spend')}${th('claimed', 'Meta claimed')}${th('perRupee', 'Sales per ₹1')}${th('visits', 'Visits')}${th('conv', 'Conversion')}</tr>
      ${sorted.map((r) => `<tr><td>${esc(weekday(r.d))} ${esc(dayLabel(r.d))}</td><td class="n">${compact(r.sales)}</td><td class="n">${r.orders}</td><td class="n">${r.items}</td><td class="n">${r.aov !== null ? compact(r.aov) : '–'}</td><td class="n">${r.spend !== null ? compact(r.spend) : '–'}</td><td class="n">${r.claimed !== null ? compact(r.claimed) : '–'}</td><td class="n">${r.perRupee !== null ? '₹' + r.perRupee.toFixed(1) : '–'}</td><td class="n">${r.visits !== null ? r.visits.toLocaleString('en-IN') : '–'}</td><td class="n">${r.conv !== null ? pct(r.conv, 3) : '–'}</td></tr>`).join('')}
      <tr class="tot"><td>Total</td><td class="n">${compact(st.sales)}</td><td class="n">${st.orders}</td><td class="n">${st.items}</td><td class="n">${compact(st.aov)}</td><td class="n">${compact(st.m.spend)}</td><td class="n">${st.m.valueSeen ? compact(st.m.value) : '–'}</td><td class="n">${st.perRupee !== null ? '₹' + st.perRupee.toFixed(1) : '–'}</td><td class="n">${st.visits !== null ? st.visits.toLocaleString('en-IN') : '–'}</td><td class="n">${st.conv !== null ? pct(st.conv, 3) : '–'}</td></tr></table></div></section>
    <section class="tile c-7"><div class="tile-head"><div><h2>What sells vs what ads push</h2><div class="sub">${esc(rangeLabel(k))}. Gold: share of website sales. Blue: share of product ad spend.</div></div></div>
      ${gb.covered ? gb.html : '<p class="muted">No Meta data for these days.</p>'}</section>
    <section class="tile c-5"><div class="tile-head"><div><h2>Price bands</h2><div class="sub">Gold items sold, ${esc(rangeLabel(k))}</div></div></div>${bandBars(k)}
      <h3 style="margin-top:6px">Payment method</h3>${pay.length ? mixList(pay, (v) => v + ' orders') : '<p class="muted small">No orders.</p>'}</section>
    <section class="tile c-12"><div class="tile-head"><div><h2>Top products · ${esc(rangeLabel(k))}</h2><div class="sub">By items sold. "Not named in ads" means no ad name or copy mentions it.</div></div></div>
      <div class="adlist">${top.map((r, j) => `<div class="adrow sku"><span class="rankc">${j + 1}</span><span><span class="nm">${esc(r.name)}</span><span class="mt">${esc(r.code)} · ${r.metal === 's' ? 'Silver' : 'Gold'}${inAds(r.name) === false ? ' · <b class="noad">not named in ads</b>' : ''}</span></span><span class="rt"><b>${r.n} sold</b><span class="mt">${compact(r.v)}</span></span></div>`).join('') || '<p class="muted small">No products sold.</p>'}</div></section>
  </div>`;
}
function wireDays(view) {
  const all = dailyDays(), last = all[all.length - 1];
  view.querySelectorAll('[data-dpreset]').forEach((b) => b.addEventListener('click', () => {
    const v = b.dataset.dpreset;
    if (v === 'mtd') { SD.until = last; SD.since = last.slice(0, 8) + '01'; }
    else if (v === 'lm') { const f = new Date(last.slice(0, 8) + '01T00:00:00Z'); f.setUTCMonth(f.getUTCMonth() - 1); SD.since = f.toISOString().slice(0, 10); SD.until = addDays(last.slice(0, 8) + '01', -1); }
    else if (v === '1') { SD.since = SD.until = last; }
    else { SD.until = last; SD.since = addDays(last, -(Number(v) - 1)); }
    window.renderSales();
  }));
  const s = $('sdSince'), u = $('sdUntil');
  const upd = () => { if (s.value && u.value) { SD.since = s.value <= u.value ? s.value : u.value; SD.until = s.value <= u.value ? u.value : s.value; window.renderSales(); } };
  if (s) s.addEventListener('change', upd);
  if (u) u.addEventListener('change', upd);
  view.querySelectorAll('[data-dsort]').forEach((b) => b.addEventListener('click', () => { SD.sort = b.dataset.dsort; window.renderSales(); }));
  const c = $('sdCsv');
  if (c) c.addEventListener('click', async () => {
    c.textContent = await downloadFile(`gehna-daily-sales-${SD.since}-to-${SD.until}.csv`, '\ufeff' + daysCsv(dayRows(SD.since, SD.until)));
    setTimeout(() => { c.textContent = 'Export CSV'; }, 2500);
  });
}

// ---------- insights ----------
function insightsFor(k, keys) {
  const out = [];
  const i = keys.indexOf(k), prevK = keys[i - 1];
  const s = monthStats(k), m = metaMonth(k);
  const ps = prevK ? monthStats(prevK) : null, pm = prevK ? metaMonth(prevK) : null;
  const partial = k === SL.data.last;
  if (m.covered && m.spend && !m.partial) {
    const b = s.sales / m.spend;
    const pb = pm && pm.covered && pm.spend && !pm.partial ? ps.sales / pm.spend : null;
    out.push({ tone: pb && b < pb ? 'down' : 'up', title: `Every ₹1 on Meta came with ₹${b.toFixed(1)} of website sales`, body: pb ? `Last month it was ₹${pb.toFixed(1)}. This counts all website sales, not only the ones Meta claims.` : 'This counts all website sales, not only the ones Meta claims.' });
    if (m.valueSeen) {
      const sh = m.value / s.sales, psh = pm && pm.valueSeen && ps.sales ? pm.value / ps.sales : null;
      out.push({ tone: 'mix', title: `Meta claims ${pct(sh)} of website sales`, body: psh !== null ? `Last month it claimed ${pct(psh)}. ${sh < psh ? 'Sales are coming more from other sources. Check organic, email and repeat buyers before you cut Meta.' : 'Meta is taking more of the credit. Check the claimed sales against real orders.'}` : 'Compare this with other channels before you judge Meta alone.' });
    }
  }
  const gb = gapBars(k);
  if (gb.covered) {
    const withA = gb.rows.filter((r) => r.a !== null);
    const under = withA.filter((r) => r.s - r.a > 0.06).sort((a, b) => (b.s - b.a) - (a.s - a.a))[0];
    const over = withA.filter((r) => r.a - r.s > 0.06).sort((a, b) => (b.a - b.s) - (a.a - a.s))[0];
    if (under) out.push({ tone: 'up', title: `${under.c} sell more than ads push them`, body: `${under.c} made ${pct(under.s)} of website sales but got ${pct(under.a)} of product ad spend. Test more ${under.c.toLowerCase()} ads.` });
    if (over) out.push({ tone: 'down', title: `${over.c} get more ad money than sales`, body: `${over.c} took ${pct(over.a)} of product ad spend but made ${pct(over.s)} of website sales. Check if these ads earn their spend.` });
  }
  const recent = keys.slice(Math.max(0, i - 3), i);
  const now = skuRollup([k]).filter((r) => r.n >= 2);
  const before = Object.fromEntries(skuRollup(recent).map((r) => [r.code, r.n / Math.max(1, recent.length)]));
  const rising = now.filter((r) => r.n >= 2 * Math.max(0.5, before[r.code] || 0)).sort((a, b) => b.n - a.n).slice(0, 3);
  if (rising.length) out.push({ tone: 'up', title: 'Rising products', body: rising.map((r) => `${r.name} (${r.n} sold, ${before[r.code] ? before[r.code].toFixed(1) + ' a month before' : 'none in the 3 months before'})`).join('. ') + '. Make ads for these.' });
  const yearTop = skuRollup(keys).sort((a, b) => b.n - a.n).slice(0, 15).filter((r) => inAds(r.name) === false).slice(0, 3);
  if (yearTop.length) out.push({ tone: 'mix', title: 'Best sellers not named in any ad', body: yearTop.map((r) => `${r.name} (${r.n} sold in 12 months)`).join('. ') + '. No ad name or copy mentions them.' });
  const ga = SL.data.ga.filter((r) => r[4] !== null);
  if (ga.length > 30) {
    const conv = (rows) => rows.reduce((t, r) => t + r[4], 0) / rows.reduce((t, r) => t + r[1], 0);
    const last14 = ga.slice(-14), base = ga.slice(0, -14);
    const a = conv(last14), b = conv(base);
    if (Number.isFinite(a) && Number.isFinite(b)) out.push({ tone: a < b ? 'down' : 'up', title: `Site conversion is ${pct(a, 3)} in the last 14 days`, body: `It was ${pct(b, 3)} before that. ${a < b ? 'Traffic is landing but not buying. Check offers, landing pages and site speed.' : 'The site is converting better. Push more traffic now.'}` });
  }
  if (ps && !partial && ps.sales) {
    const ch = (s.sales - ps.sales) / ps.sales;
    out.unshift({ tone: ch < 0 ? 'down' : 'up', title: `Website sales ${ch < 0 ? 'fell' : 'rose'} ${pct(Math.abs(ch))} vs ${mLabel(prevK, false)}`, body: `${compact(s.sales)} from ${s.items} items. Last month was ${compact(ps.sales)} from ${ps.items} items.` });
  }
  return out;
}

// ---------- render ----------
function kpi(label, value, sub, cls = '') {
  return `<div class="tile kt ${cls}"><div class="kname">${label}</div><div class="kval">${value}</div><div class="kfoot">${sub}</div></div>`;
}
function change(cur, prev, good = 1) {
  if (cur === null || prev === null || prev === undefined || !prev) return '';
  const ch = (cur - prev) / Math.abs(prev);
  if (!Number.isFinite(ch)) return '';
  const tone = Math.abs(ch) < 0.005 ? 'flat' : (ch > 0) === (good > 0) ? '' : 'bad';
  return `<span class="dchip ${tone}">${ch > 0 ? '▲' : '▼'} ${Math.abs(ch * 100).toFixed(0)}%</span>`;
}

window.renderSales = async function renderSales() {
  const view = $('salesView');
  if (!SL.data) {
    view.innerHTML = '<p class="loading">Loading brand sales…</p>';
    await loadSales();
    if (!SL.data) { view.innerHTML = `<div class="panel-box"><h2>Brand sales</h2><p class="muted">Sales data is not available here${SL.err ? ` (${esc(SL.err)})` : ''}.</p></div>`; return; }
  }
  const keys = Object.keys(SL.data.months).sort();
  SL.data.last = keys[keys.length - 1];
  const hasDays = dailyDays().length > 0;
  const modeSeg = hasDays ? `<div class="seg" role="group" aria-label="View"><button type="button" data-smode="months" aria-pressed="${SD.mode === 'months'}">Months</button><button type="button" data-smode="days" aria-pressed="${SD.mode === 'days'}">Days</button></div>` : '';
  const wireMode = () => view.querySelectorAll('[data-smode]').forEach((b) => b.addEventListener('click', () => { SD.mode = b.dataset.smode; window.renderSales(); }));
  if (hasDays && SD.mode === 'days') {
    const dd = dailyDays();
    view.innerHTML = `<div class="sales"><div class="sl-head"><div><h2>Brand sales</h2><p class="muted small">Website orders from your Metabase dashboard, day by day, pulled ${esc(dateLabel((SL.data.daily_pulled_at || SL.data.pulled_at || '').slice(0, 10)))}. Meta numbers come from the ads data.</p></div>${modeSeg}</div>${daysView()}</div>`;
    wireMode(); wireDays(view);
    return;
  }
  if (!SL.month || !keys.includes(SL.month)) SL.month = SL.data.last;
  const k = SL.month, i = keys.indexOf(k), prevK = keys[i - 1];
  const s = monthStats(k), m = metaMonth(k), ps = prevK ? monthStats(prevK) : null, pm = prevK ? metaMonth(prevK) : null;
  const partial = k === SL.data.last;
  const pulled = (SL.data.pulled_at || '').slice(0, 10);
  const blended = m.covered && m.spend && !m.partial ? s.sales / m.spend : null;
  const pBlended = pm && pm.covered && pm.spend && !pm.partial ? ps.sales / pm.spend : null;
  const claim = m.covered && m.valueSeen && s.sales ? m.value / s.sales : null;
  const pClaim = pm && pm.covered && pm.valueSeen && ps.sales ? pm.value / ps.sales : null;
  const spark = sparkSvg(keys.map((x) => monthStats(x).sales), { color: 'var(--on-gold)', W: 300, H: 64 });
  const ins = insightsFor(k, keys);
  const gb = gapBars(k);
  const top = skuRollup([k]).sort((a, b) => b.n - a.n || b.v - a.v).slice(0, 12);
  const year = skuRollup(keys).sort((a, b) => b.n - a.n || b.v - a.v).slice(0, 12);
  const md = metaDaily();
  const ret = {};
  for (const x of keys) for (const [code, name, v, n] of SL.data.months[x].ret) { const b = baseCode(code); const o = ret[b] || (ret[b] = { name: cleanName(name), v: 0, n: 0 }); o.v += v || 0; o.n += n || 0; }
  const retTop = Object.values(ret).sort((a, b) => b.n - a.n || b.v - a.v).slice(0, 8);
  const karat = SL.data.months[k].karat.map((r) => [r[0].split(',')[0], r[1]]).reduce((acc, r) => { const f = acc.find((x) => x[0] === r[0]); if (f) f[1] += r[1]; else acc.push([r[0], r[1]]); return acc; }, []).sort((a, b) => b[1] - a[1]);
  const pay = SL.data.months[k].pay.slice().sort((a, b) => b[1] - a[1]);
  const skuRow = (r, i2, showMonths) => `<div class="adrow sku"><span class="rankc">${i2 + 1}</span><span><span class="nm">${esc(r.name)}</span><span class="mt">${esc(r.code)} · ${r.metal === 's' ? 'Silver' : 'Gold'}${showMonths ? ` · sold in ${Object.keys(r.months).length} of ${keys.length} months` : ''}${inAds(r.name) === false ? ' · <b class="noad">not named in ads</b>' : ''}</span></span><span class="rt"><b>${r.n} sold</b><span class="mt">${compact(r.v)}</span></span></div>`;

  view.innerHTML = `<div class="sales">
  <div class="sl-head">
    <div><h2>Brand sales</h2><p class="muted small">Website orders from your Metabase dashboard, pulled ${esc(pulled ? dateLabel(pulled) : '')}. Meta numbers come from the ads data. This tab uses its own month picker.</p></div>
    <div class="row" style="gap:8px">${modeSeg}<div class="seg sl-months" role="group" aria-label="Month">${keys.slice(-7).map((x) => `<button type="button" data-month="${x}" aria-pressed="${x === k}">${esc(mLabel(x, false))}${x === SL.data.last ? '*' : ''}</button>`).join('')}</div></div>
  </div>
  ${partial ? `<p class="note">* ${esc(mLabel(k))} is month to date, so compare it with care.</p>` : ''}
  <div class="bento">
    <section class="tile hero c-4"><div class="label">Website sales · ${esc(mLabel(k))}${partial ? ' so far' : ''}</div><div class="big">${compact(s.sales)}</div>
      <div>${partial ? '' : change(s.sales, ps && ps.sales)}</div>
      <div class="spark-wrap">${spark}</div><div class="spark-cap"><span>${esc(mLabel(keys[0]))}</span><span>${esc(mLabel(keys[keys.length - 1]))}</span></div></section>
    <div class="c-8 sl-kpis">
      ${kpi('Items sold', s.items ?? '–', partial ? 'Month to date' : change(s.items, ps && ps.items) + ' vs last month')}
      ${kpi('Average item value', compact(s.aiv), change(s.aiv, ps && ps.aiv) + ' vs last month')}
      ${kpi('Meta spend', m.covered ? compact(m.spend) : '–', m.covered ? (m.partial ? 'Partial month' : partial ? 'Month to date' : change(m.spend, pm && pm.spend, -1) + ' vs last month') : 'No Meta data for this month')}
      ${kpi('Sales per ₹1 of Meta', blended !== null ? '₹' + blended.toFixed(1) : '–', blended !== null ? `${pBlended !== null ? `₹${pBlended.toFixed(1)} last month` : ''}` : 'Unavailable', 'gold')}
      ${kpi('Sales Meta claims', claim !== null ? pct(claim) : '–', claim !== null ? `${pClaim !== null ? pct(pClaim) + ' last month' : ''}` : 'Unavailable')}
      ${kpi('Refunds', s.refund !== null ? compact(s.refund) : '–', s.refundRate !== null ? `${pct(s.refundRate, 1)} of sales · ${s.retItems} items` : 'Unavailable')}
    </div>
    <section class="tile c-12 sl-ins"><div class="tile-head"><div><h2>What to do</h2><div class="sub">Built from this month's sales and ad data</div></div><button class="btn ghost small-btn" type="button" id="slCopy">Copy</button></div>
      <div class="alerts">${ins.map((x) => `<div class="alert ${x.tone === 'up' ? 'up' : x.tone === 'down' ? 'down' : ''}"><b>${esc(x.title)}</b><span class="small">${esc(x.body)}</span></div>`).join('') || '<p class="muted">Nothing stands out this month.</p>'}</div></section>
    <section class="tile flow c-12"><div class="tile-head"><div><h2>Website sales vs Meta</h2><div class="sub">Gold bars: website sales. Dark bars: sales Meta says it drove. Blue line: Meta spend. Hover a month.</div></div></div>
      ${salesChart(keys)}
      <div class="legend"><span><i style="background:var(--gold)"></i>Website sales</span><span><i style="background:var(--ink)"></i>Meta claimed</span><span><i style="background:var(--spend)"></i>Meta spend</span></div></section>
    <section class="tile c-7"><div class="tile-head"><div><h2>What sells vs what ads push</h2><div class="sub">${esc(mLabel(k))}. Gold: share of website sales. Blue: share of product ad spend.</div></div></div>
      ${gb.covered ? gb.html : '<p class="muted">No Meta data for this month.</p>'}
      ${gb.mixedShare !== null ? `<p class="small muted">${pct(gb.mixedShare)} of ad spend went to catalog or mixed ads, so it is left out. Ads are tagged from their names and copy.</p>` : ''}</section>
    <section class="tile c-5"><div class="tile-head"><div><h2>Price bands</h2><div class="sub">Gold items sold, ${esc(mLabel(k))}</div></div></div>${bandBars(k)}
      <h3 style="margin-top:6px">Stock vs custom made</h3>${mixList([['Stock', s.stock], ['Custom made', s.custom]], compact)}</section>
    <section class="tile c-12"><div class="tile-head"><div><h2>Sales by category, month by month</h2><div class="sub">Darker cells mean more sales. Hover for items and average price.</div></div></div>${heatRows(keys)}</section>
    <section class="tile c-6"><div class="tile-head"><div><h2>Top products · ${esc(mLabel(k))}</h2><div class="sub">By items sold. "Not named in ads" means no ad name or copy mentions it.</div></div></div><div class="adlist">${top.map((r, j) => skuRow(r, j, false)).join('')}</div></section>
    <section class="tile c-6"><div class="tile-head"><div><h2>Best sellers · 12 months</h2><div class="sub">Sizes and karat versions grouped together</div></div></div><div class="adlist">${year.map((r, j) => skuRow(r, j, true)).join('')}</div></section>
    <section class="tile flow c-12"><div class="tile-head"><div><h2>Traffic, spend and orders by day</h2><div class="sub">Google Analytics from ${esc(dateLabel(SL.data.ga[0][0]))}. Red marks are days with no order data.</div></div></div>${trafficChart(SL.data.ga, md)}</section>
    <section class="tile c-4"><div class="tile-head"><h2>Metal and karat</h2></div>${mixList(karat, compact)}</section>
    <section class="tile c-4"><div class="tile-head"><h2>Payment method</h2></div>${mixList(pay, (v) => v + ' orders')}</section>
    <section class="tile c-4"><div class="tile-head"><div><h2>Most returned · 12 months</h2><div class="sub">By items returned</div></div></div><div class="adlist">${retTop.map((r) => `<div class="dl-row"><span class="dl-ic">${r.n}×</span><span><div class="t">${esc(r.name)}</div><div class="s">${compact(r.v)} refunded</div></span><span></span></div>`).join('')}</div></section>
  </div></div>`;

  view.querySelectorAll('[data-month]').forEach((b) => b.addEventListener('click', () => { SL.month = b.dataset.month; window.renderSales(); }));
  wireMode();
  const cp = $('slCopy');
  if (cp) cp.addEventListener('click', async () => {
    const text = `Brand sales, ${mLabel(k)}${partial ? ' so far' : ''}\n\n` + ins.map((x) => `- ${x.title}. ${x.body}`).join('\n');
    try { await navigator.clipboard.writeText(text); cp.textContent = 'Copied'; } catch (e) { cp.textContent = 'Copy failed'; }
    setTimeout(() => { cp.textContent = 'Copy'; }, 1600);
  });
};
