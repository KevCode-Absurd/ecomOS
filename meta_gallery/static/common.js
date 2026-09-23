'use strict';
// Shared helpers for the gallery and the client report. No credentials here.
const $ = (id) => document.getElementById(id);
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const NA = '<span class="na" title="Meta returned no value for this metric in these dates. Meta omits purchase fields when none were attributed, so this is not shown as zero.">Unavailable</span>';

let money = (v) => String(v);
let money2 = money;
function setCurrency(cur) {
  const nf0 = new Intl.NumberFormat('en-IN', { style: 'currency', currency: cur || 'INR', maximumFractionDigits: 0 });
  const nf2 = new Intl.NumberFormat('en-IN', { style: 'currency', currency: cur || 'INR', maximumFractionDigits: 2 });
  money = (v) => nf0.format(v);
  money2 = (v) => nf2.format(v);
}
function fmt(v, kind) {
  if (v === null || v === undefined || Number.isNaN(v)) return NA;
  switch (kind) {
    case 'money': return money(v);
    case 'money2': return money2(v);
    case 'int': return Math.round(v).toLocaleString('en-IN');
    case 'x': return v.toFixed(2) + 'x';
    case 'pct': return v.toFixed(2) + '%';
    default: return esc(v);
  }
}
function dateLabel(iso) {
  return new Date(iso + 'T00:00:00Z').toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric', timeZone: 'UTC' });
}
function shortDate(iso) {
  return new Date(iso + 'T00:00:00Z').toLocaleDateString('en-IN', { day: 'numeric', month: 'short', timeZone: 'UTC' });
}
function addDays(iso, n) {
  const d = new Date(iso + 'T00:00:00Z');
  d.setUTCDate(d.getUTCDate() + n);
  return d.toISOString().slice(0, 10);
}
function statusLabel(s) { return (s || 'UNKNOWN').replace(/_/g, ' ').toLowerCase(); }
function secs(n) { return n ? `${Math.round(n)}s` : ''; }
const link = (url, text) => `<a href="${esc(url)}" target="_blank" rel="noopener noreferrer">${esc(text || url)}</a>`;

// Change vs previous period. good: +1 when up is good, -1 when up is bad, 0 neutral.
function delta(cur, prev, good) {
  if (cur === null || cur === undefined || prev === null || prev === undefined || prev === 0) return '';
  const ch = (cur - prev) / Math.abs(prev);
  if (!Number.isFinite(ch)) return '';
  const sign = ch > 0 ? '+' : '';
  const tone = Math.abs(ch) < 0.005 || !good ? 'flat' : (ch > 0) === (good > 0) ? 'good' : 'bad';
  return `<span class="delta ${tone}">${ch > 0 ? '▲' : ch < 0 ? '▼' : ''} ${sign}${(ch * 100).toFixed(1)}%</span>`;
}

function filterQuery(f) {
  const p = new URLSearchParams();
  p.set('since', f.since);
  p.set('until', f.until);
  if (f.kw && f.kw.length) p.set('kw', f.kw.join(','));
  if (f.camp && f.camp.length) p.set('camp', f.camp.join(','));
  return p.toString();
}
function parseKw(text) {
  return [...new Set(String(text || '').split(',').map((s) => s.trim().toLowerCase()).filter(Boolean))].slice(0, 20);
}

const VERDICT_CLASS = { scale: 'v-scale', watch: 'v-watch', cut: 'v-cut', not_enough_data: 'v-na', no_target: 'v-na' };
function verdictChip(v) {
  if (!v) return '';
  return `<span class="chip ${VERDICT_CLASS[v.code] || ''}" title="${esc(v.reason)}">${esc(v.label)}</span>`;
}
function fatigueChip(f) {
  if (!f || !['declining', 'ctr_down', 'roas_down'].includes(f.code)) return '';
  return `<span class="chip flag" title="${esc(f.reason)}">${esc(f.code === 'declining' ? 'Fatigue' : f.label)}</span>`;
}

const AGE_ORDER = ['13-17', '18-24', '25-34', '35-44', '45-54', '55-64', '65+', 'Unknown', 'unknown'];
const GENDER_ORDER = ['female', 'male', 'unknown'];
function aggregate(ads, dim) {
  const acc = {};
  for (const ad of ads) {
    const d = ((ad.view || {}).demographics || {})[dim] || {};
    for (const [k, b] of Object.entries(d)) {
      const a = acc[k] || (acc[k] = { spend: 0, value: 0, purchases: 0, reported: false });
      a.spend += b.spend;
      if (b.purchase_value !== null) { a.value += b.purchase_value; a.reported = true; }
      if (b.purchases !== null) a.purchases += b.purchases;
    }
  }
  const order = dim === 'age' ? AGE_ORDER : GENDER_ORDER;
  const pos = (k) => (order.indexOf(k) < 0 ? 99 : order.indexOf(k));
  return Object.entries(acc).filter(([, a]) => a.spend > 0).sort((x, y) => pos(x[0]) - pos(y[0]))
    .map(([k, a]) => ({ key: k, ...a, roas: a.reported ? a.value / a.spend : null }));
}

function barChart(title, rows, getV, fmtV, cls, total) {
  const max = Math.max(...rows.map((r) => getV(r) || 0), 0) || 1;
  return `<figure class="mini"><figcaption>${esc(title)}</figcaption>` + rows.map((r) => {
    const v = getV(r);
    const w = v ? Math.max(1.5, v / max * 100) : 0;
    const tip = `${r.key}: spend ${money(r.spend)}${total ? ` (${(r.spend / total * 100).toFixed(1)}%)` : ''} · purchase value ${r.reported ? money(r.value) : 'not reported'} · purchases ${r.reported ? Math.round(r.purchases) : 'not reported'} · ROAS ${r.roas !== null ? r.roas.toFixed(2) + 'x' : 'unavailable'}`;
    return `<div class="brow" title="${esc(tip)}"><span class="blabel">${esc(r.key)}</span><span class="btrack">${v !== null ? `<span class="bar ${cls}" style="width:${w}%"></span>` : ''}</span><span class="bval">${v !== null ? fmtV(v) : '<span class="na">No purchases reported</span>'}</span></div>`;
  }).join('') + '</figure>';
}

function demoBlock(ads, bucketNote) {
  const age = aggregate(ads, 'age');
  const gender = aggregate(ads, 'gender');
  const total = age.reduce((s, r) => s + r.spend, 0);
  if (!age.length) return '';
  const block = (name, rows) => `<div class="demo-block"><h3>By ${name}</h3><div class="demo-pair">
      ${barChart('Amount spent', rows, (r) => r.spend, (v) => `${money(v)} · ${(v / total * 100).toFixed(0)}%`, 'spend', total)}
      ${barChart('Purchase ROAS', rows, (r) => r.roas, (v) => v.toFixed(2) + 'x', 'roas', total)}
    </div></div>`;
  return `<div class="demo-head"><strong>Spend and ROAS by age and gender</strong>
      <span class="small muted">${bucketNote} Built from Meta's age and gender breakdown rows, summed per group. ROAS = purchase value ÷ spend for that group. A separate view of the same spend, not extra results.</span></div>
    <div class="demo-grid">${block('age', age)}${block('gender', gender)}</div>`;
}

function bucketNote(buckets, exact, range) {
  if (!buckets || !buckets.length) return 'No breakdown rows for these dates.';
  const span = `${dateLabel(buckets[0][0])} to ${dateLabel(buckets[buckets.length - 1][1])}`;
  if (exact) return `Covers ${span}, the same dates as above.`;
  return `Breakdowns are stored by calendar month, so these charts cover ${span} (every month that overlaps ${dateLabel(range.since)} to ${dateLabel(range.until)}), not exactly the dates above.`;
}

// Small single-series SVG line or bar chart. points: [{x: label, y: number|null}]
function sparkChart(points, { kind = 'line', color = '#2a78d6', fmtY = (v) => v.toFixed(2), height = 90, title = '' } = {}) {
  const W = 520, H = height, L = 44, R = 8, T = 8, B = 20;
  const ys = points.map((p) => p.y).filter((v) => v !== null && Number.isFinite(v));
  if (!ys.length) return `<figure class="spark"><figcaption>${esc(title)}</figcaption><p class="small muted">No data for these dates.</p></figure>`;
  const max = Math.max(...ys) || 1;
  const n = points.length;
  const x = (i) => L + (n === 1 ? (W - L - R) / 2 : i * (W - L - R) / (n - 1));
  const y = (v) => T + (H - T - B) * (1 - v / max);
  let body = '';
  if (kind === 'bar') {
    const bw = Math.max(1, (W - L - R) / n - 1);
    body = points.map((p, i) => p.y ? `<rect x="${(x(i) - bw / 2).toFixed(1)}" y="${y(p.y).toFixed(1)}" width="${bw.toFixed(1)}" height="${(H - B - y(p.y)).toFixed(1)}" fill="${color}"><title>${esc(p.x)}: ${esc(fmtY(p.y))}</title></rect>` : '').join('');
  } else {
    let d = '', pen = false;
    points.forEach((p, i) => {
      if (p.y === null || !Number.isFinite(p.y)) { pen = false; return; }
      d += `${pen ? 'L' : 'M'}${x(i).toFixed(1)},${y(p.y).toFixed(1)}`;
      pen = true;
    });
    body = `<path d="${d}" fill="none" stroke="${color}" stroke-width="2" stroke-linejoin="round"/>` +
      points.map((p, i) => (p.y === null ? '' : `<circle cx="${x(i).toFixed(1)}" cy="${y(p.y).toFixed(1)}" r="6" fill="transparent"><title>${esc(p.x)}: ${esc(fmtY(p.y))}</title></circle>`)).join('');
  }
  const grid = [0, 0.5, 1].map((f) => `<line x1="${L}" x2="${W - R}" y1="${y(max * f).toFixed(1)}" y2="${y(max * f).toFixed(1)}" class="gl"/><text x="${L - 4}" y="${(y(max * f) + 3).toFixed(1)}" text-anchor="end" class="tl">${esc(fmtY(max * f))}</text>`).join('');
  const xl = `<text x="${L}" y="${H - 4}" class="tl">${esc(points[0].x)}</text><text x="${W - R}" y="${H - 4}" text-anchor="end" class="tl">${esc(points[n - 1].x)}</text>`;
  return `<figure class="spark"><figcaption>${esc(title)}</figcaption><svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(title)}">${grid}${body}${xl}</svg></figure>`;
}

function attribution(s) {
  const map = {
    '1d_view_7d_click_1d_ev': '7-day click, 1-day view, 1-day engaged view',
    '1d_view_7d_click': '7-day click, 1-day view',
    '7d_click': '7-day click',
    '1d_click': '1-day click',
    'incrementality': 'Incremental attribution',
  };
  return s ? (map[s] ? `${map[s]} (${s})` : s) : 'Unavailable';
}

async function getJSON(url, opts) {
  const res = await fetch(url, opts);
  const body = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(body.error || `Request failed (${res.status})`);
  return body;
}
async function saveSettings(s) {
  return getJSON('/api/settings', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(s) });
}
