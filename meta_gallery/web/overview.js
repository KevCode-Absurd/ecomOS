'use strict';
// Overview tab: a bento dashboard built from the same engine and view as the other tabs.
// Uses helpers from app.js ($, esc, fmt, money, VIEW, ENGINE, state, thumbSrc, openSide, setTab, ...).
const OV = { metric: 'spend' };
const FORMAT_COLOR = { static_image: 'var(--spend)', video: 'var(--roas)', carousel: 'var(--s3)', catalog_dynamic: 'var(--s4)', unconfirmed_mixed: 'var(--s5)' };
const ARROW = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17L17 7M9 7h8v8"/></svg>';
const compact = (v) => {
  if (v === null || v === undefined) return '–';
  const a = Math.abs(v);
  if (a >= 1e7) return '₹' + (v / 1e7).toFixed(2) + ' Cr';
  if (a >= 1e5) return '₹' + (v / 1e5).toFixed(2) + ' L';
  if (a >= 1e3) return '₹' + (v / 1e3).toFixed(1) + 'k';
  return '₹' + Math.round(v);
};

function dchip(cur, prev, good) {
  if (!($('compare').checked && VIEW.previous.complete) || cur === null || cur === undefined || !prev) return '';
  const ch = (cur - prev) / Math.abs(prev);
  if (!Number.isFinite(ch)) return '';
  const tone = Math.abs(ch) < 0.005 || !good ? 'flat' : (ch > 0) === (good > 0) ? '' : 'bad';
  return `<span class="dchip ${tone}" title="vs previous ${VIEW.range.days} days">${ch > 0 ? '▲' : ch < 0 ? '▼' : ''} ${Math.abs(ch * 100).toFixed(1)}%</span>`;
}

// Daily account series for the selected range (and the same-length period before it).
function rangeDays() {
  const [a, b] = ENGINE.resolveRange(VIEW.range.since, VIEW.range.until);
  const s = ENGINE.dailySeries(state.kw, state.camp);
  const row = (d) => (d < 0 ? null : { d, date: ENGINE.iso(d), spend: s.spend[d], value: s.reported[d] ? s.value[d] : null, purch: s.purch[d], reported: !!s.reported[d] });
  const cur = [], prev = [];
  for (let d = a; d <= b; d++) cur.push(row(d));
  const len = b - a + 1;
  for (let d = a - len; d < a; d++) prev.push(row(d));
  return { a, b, cur, prev: prev.every(Boolean) ? prev : null };
}
function rollAt(rows, i, fn) { return fn(rows.slice(Math.max(0, i - 6), i + 1)); }
const sumK = (rows, k) => rows.reduce((t, r) => t + (r[k] || 0), 0);
const roas7 = (rows) => { const sp = sumK(rows, 'spend'); return sp > 0 && rows.some((r) => r.reported) ? sumK(rows, 'value') / sp : null; };

// Smooth path through points (Catmull-Rom to Bezier). Breaks at nulls.
// A lone point becomes a tiny stroke, so with a round cap it shows as a dot instead of vanishing.
function smoothPath(pts) {
  let d = '', seg = [];
  const flush = () => {
    if (!seg.length) return;
    d += `M${seg[0][0].toFixed(1)},${seg[0][1].toFixed(1)}`;
    if (seg.length === 1) { d += 'l0.01,0'; seg = []; return; }
    for (let i = 0; i < seg.length - 1; i++) {
      const p0 = seg[i - 1] || seg[i], p1 = seg[i], p2 = seg[i + 1], p3 = seg[i + 2] || p2;
      const c1 = [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6], c2 = [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6];
      d += `C${c1[0].toFixed(1)},${c1[1].toFixed(1)} ${c2[0].toFixed(1)},${c2[1].toFixed(1)} ${p2[0].toFixed(1)},${p2[1].toFixed(1)}`;
    }
    seg = [];
  };
  for (const p of pts) { if (p === null) flush(); else seg.push(p); }
  flush();
  return d;
}
// Solid runs of points (no nulls), as [[x,y], ...] lists.
function segmentsOf(pts) {
  const out = [];
  let cur = [];
  for (const p of pts) { if (p === null) { if (cur.length) out.push(cur); cur = []; } else cur.push(p); }
  if (cur.length) out.push(cur);
  return out;
}
// Straight dotted links across gaps: last point before a gap to the first point after it.
function bridgePath(pts) {
  const segs = segmentsOf(pts);
  let d = '';
  for (let i = 0; i < segs.length - 1; i++) {
    const a = segs[i][segs[i].length - 1], b = segs[i + 1][0];
    d += `M${a[0].toFixed(1)},${a[1].toFixed(1)}L${b[0].toFixed(1)},${b[1].toFixed(1)}`;
  }
  return d;
}
// Area under each solid run, down to baseY.
function areaPath(pts, baseY) {
  return segmentsOf(pts).filter((s) => s.length > 1).map((s) => `${smoothPath(s)} L${s[s.length - 1][0].toFixed(1)},${baseY} L${s[0][0].toFixed(1)},${baseY} Z`).join(' ');
}

// Small area sparkline (no axes). vals: numbers or null.
function sparkSvg(vals, { color = 'var(--ink)', W = 240, H = 48, fill = true, id = '' } = {}) {
  const ok = vals.filter((v) => v !== null && Number.isFinite(v));
  if (ok.length < 2) return '<svg viewBox="0 0 240 48" aria-hidden="true"></svg>';
  const max = Math.max(...ok), min = Math.min(...ok, 0), n = vals.length;
  const x = (i) => 3 + i * (W - 6) / (n - 1), y = (v) => 4 + (H - 8) * (1 - (v - min) / ((max - min) || 1));
  const pts = vals.map((v, i) => (v === null || !Number.isFinite(v) ? null : [x(i), y(v)]));
  const line = smoothPath(pts), bridge = bridgePath(pts);
  const lastI = vals.map((v, i) => (v === null || !Number.isFinite(v) ? -1 : i)).filter((i) => i >= 0).pop();
  const area = fill ? `<path d="${areaPath(pts, H)}" style="fill:${color};opacity:.1"/>` : '';
  return `<svg viewBox="0 0 ${W} ${H}" preserveAspectRatio="none" aria-hidden="true"${id ? ` id="${id}"` : ''}>${area}${bridge ? `<path d="${bridge}" style="fill:none;stroke:${color};opacity:.45" stroke-width="1.5" stroke-dasharray="2 4" vector-effect="non-scaling-stroke"/>` : ''}<path d="${line}" style="fill:none;stroke:${color}" stroke-width="2" stroke-linecap="round" vector-effect="non-scaling-stroke"/><circle cx="${x(lastI).toFixed(1)}" cy="${y(vals[lastI]).toFixed(1)}" r="3.5" style="fill:${color}"/></svg>`;
}
// Group days into buckets for tile sparklines: 7-day buckets when the range is long.
function buckets(rows) {
  if (rows.length <= 21) return rows.map((r) => [r]);
  const out = [];
  for (let i = 0; i < rows.length; i += 7) out.push(rows.slice(i, i + 7));
  return out;
}

// ---------- tiles ----------
function heroTile(R) {
  const t = VIEW.totals, p = VIEW.previous_totals || {};
  const spark = R.cur.map((r, i) => rollAt(R.cur, i, (s) => sumK(s, 'spend') / s.length));
  return `<section class="tile hero lite c-5" aria-label="Meta spend">
    <div class="label">Meta spend · ${esc(shortDate(VIEW.range.since))} to ${esc(shortDate(VIEW.range.until))} · ${VIEW.range.days} days</div>
    <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap"><div class="big">${money(t.spend)}</div>${dchip(t.spend, p.spend, 0)}</div>
    <div class="spark-wrap">${sparkSvg(spark, { color: '#16140f', W: 600, H: 96 })}<div class="spark-cap"><span>${esc(shortDate(VIEW.range.since))}</span><span>Spend a day, 7-day average</span><span>${esc(shortDate(VIEW.range.until))}</span></div></div>
    <div class="trio">
      <div><span>Purchase value</span><b>${t.purchase_value !== null ? compact(t.purchase_value) : 'Unavailable'}</b></div>
      <div><span>ROAS</span><b>${t.roas !== null ? t.roas.toFixed(2) + 'x' : 'Unavailable'}</b></div>
      <div><span>Ads live</span><b>${t.ads}</b></div>
    </div>
    <div class="actions"><button class="btn" type="button" data-goto="gallery">Open ad gallery</button><button class="btn ghost" type="button" data-goto="campaigns">Campaigns</button></div>
  </section>`;
}
function spotlightTile() {
  const top = VIEW.collections.all.ad_ids.map((id) => VIEW.ads[id]);
  const scale = top.filter((a) => a.view.verdict.code === 'scale').sort((x, y) => (y.view.metrics.purchase_value || 0) - (x.view.metrics.purchase_value || 0));
  const ad = scale[0] || top[0];
  if (!ad) return '<section class="tile c-3"><p class="muted">No ads spent in these dates.</p></section>';
  const m = ad.view.metrics, src = thumbSrc(ad.id);
  return `<button class="tile spot c-3" type="button" data-open="${esc(ad.id)}" aria-label="Open ${esc(ad.name)}">
    ${src ? `<img src="${src}" alt="">` : ''}<span class="shade"></span>
    <span class="top-chip">${scale[0] ? 'Top scaling ad' : 'Top ad by spend'}</span>
    <span class="roas-pill">${m.roas !== null ? m.roas.toFixed(2) + 'x' : 'No value'}</span>
    <span class="cap"><strong>${esc(ad.name)}</strong><span>${esc(ad.creative.type_label)} · ${money(m.spend)} spend · ${m.purchases ?? 0} purchases</span></span>
  </button>`;
}
function healthTile() {
  // Verdicts cover live ads only. Ads that are off show as Relaunch (did well) or Off.
  const every = (VIEW.collections.health || VIEW.collections.all).ad_ids.map((id) => VIEW.ads[id]);
  const top = every.filter((a) => a.effective_status === 'ACTIVE');
  const total = top.reduce((s, a) => s + a.view.metrics.spend, 0) || 1;
  const groups = [['scale', 'Scale', 'seg-scale'], ['cut', 'Cut', 'seg-cut'], ['watch', 'Watch', 'seg-watch'], ['not_enough_data', 'Too little spend', 'seg-ned']];
  const relaunch = every.filter((a) => healthGroup(a) === 'relaunch'), off = every.length - top.length - relaunch.length;
  const g = groups.map(([code, label, cls]) => {
    const list = top.filter((a) => a.view.verdict.code === code);
    return { code, label, cls, n: list.length, spend: list.reduce((s, a) => s + a.view.metrics.spend, 0) };
  });
  const scaleShare = g[0].spend / total * 100;
  const tired = top.filter((a) => FATIGUED.includes(a.view.fatigue.code)).length;
  const noted = top.filter((a) => (NOTES[a.id] || []).length).length;
  const tg = VIEW.targets;
  return `<section class="tile health c-4" aria-label="Ad health">
    <div class="tile-head"><div><h2>Live ads health, ${top.length} ads</h2><div class="sub">Share of live spend on ads beating ${tg.roas ? tg.roas.toFixed(2) + 'x' : 'the target'} ROAS</div></div><button class="go" type="button" data-health="all" aria-label="See every ad grouped by verdict">${ARROW}</button></div>
    <div class="big">${scaleShare.toFixed(0)}%</div>
    <div class="segbar" role="img" aria-label="Spend by verdict">${g.filter((x) => x.spend > 0).map((x) => `<span class="${x.cls}" style="flex:${x.spend}" data-health="${x.code}" data-tip="${esc(`${x.label}|Ads|${x.n}|Spend|${money(x.spend)}|Share|${(x.spend / total * 100).toFixed(1)}%`)}">${x.spend / total > 0.12 ? (x.spend / total * 100).toFixed(0) + '%' : ''}</span>`).join('')}</div>
    <div class="seg-legend">${g.map((x) => `<button type="button" data-health="${x.code}" aria-label="See the ${x.n} ${x.label} ads"><span><i class="${x.cls}"></i>${x.label}</span><b>${x.n} ads</b></button>`).join('')}</div>
    <button class="relaunch-row" type="button" data-health="relaunch"><span><b>${relaunch.length}</b> ads to relaunch</span><span class="muted small">Off now, did well in these dates · ${off} more are off</span></button>
    <div class="meter"><div style="display:flex;justify-content:space-between"><span>Showing fatigue</span><b>${tired} of ${top.length}</b></div><div class="bar"><i style="width:${top.length ? tired / top.length * 100 : 0}%"></i></div></div>
    <div class="meter"><div style="display:flex;justify-content:space-between"><span>With team notes</span><b>${noted} of ${top.length}</b></div><div class="bar"><i style="width:${top.length ? noted / top.length * 100 : 0}%"></i></div></div>
  </section>`;
}
function kpiTiles(R) {
  const t = VIEW.totals, p = VIEW.previous_totals || {};
  const B = buckets(R.cur);
  const series = {
    value: B.map((s) => (s.some((r) => r.reported) ? sumK(s, 'value') : null)),
    roas: B.map((s) => roas7(s)),
    purch: B.map((s) => sumK(s, 'purch')),
    cpa: B.map((s) => { const n = sumK(s, 'purch'); return n ? sumK(s, 'spend') / n : null; }),
  };
  const per = R.cur.length <= 21 ? 'day' : 'week';
  const tile = (cls, name, val, chip, vals, foot) => `<section class="tile kt ${cls} c-3"><div class="kname">${name}</div><div class="krow"><div class="kval">${val}</div>${chip}</div>${sparkSvg(vals, { color: 'var(--ink)' })}<div class="kfoot">${foot}</div></section>`;
  return tile('mint', 'Purchase value', t.purchase_value !== null ? compact(t.purchase_value) : NA, dchip(t.purchase_value, p.purchase_value, 1), series.value, `Per ${per}. Meta's reported value.`) +
    tile('sky', 'ROAS', t.roas !== null ? t.roas.toFixed(2) + 'x' : NA, dchip(t.roas, p.roas, 1), series.roas, `Value ÷ spend, per ${per}.`) +
    tile('lav', 'Purchases', fmt(t.purchases, 'int'), dchip(t.purchases, p.purchases, 1), series.purch, `Per ${per}.`) +
    tile('peach', 'Cost per purchase', t.cpa !== null ? money(t.cpa) : NA, dchip(t.cpa, p.cpa, -1), series.cpa, `Per ${per}. Lower is better.`);
}

const FLOW = { W: 900, H: 330, L: 56, R: 14, T: 14, B: 28 };
function flowData(R) {
  const pick = (rows) => rows.map((r, i) => (OV.metric === 'spend' ? r.spend : OV.metric === 'value' ? r.value : rollAt(rows, i, roas7)));
  return { cur: pick(R.cur), prev: R.prev && $('compare').checked ? pick(R.prev) : null };
}
function flowTile(R) {
  const { W, H, L, R: Rt, T, B } = FLOW;
  const { cur, prev } = flowData(R);
  const all = [...cur, ...(prev || [])].filter((v) => v !== null && Number.isFinite(v));
  const max = Math.max(...all, 0) * 1.08 || 1, n = cur.length;
  const x = (i) => L + (n === 1 ? (W - L - Rt) / 2 : i * (W - L - Rt) / (n - 1));
  const y = (v) => T + (H - T - B) * (1 - v / max);
  const f = OV.metric === 'roas' ? (v) => v.toFixed(1) + 'x' : compact;
  const grid = [0, 0.25, 0.5, 0.75, 1].map((k) => `<line x1="${L}" x2="${W - Rt}" y1="${y(max * k).toFixed(1)}" y2="${y(max * k).toFixed(1)}" class="gl"/><text x="${L - 8}" y="${(y(max * k) + 4).toFixed(1)}" text-anchor="end" class="tl">${esc(f(max * k))}</text>`).join('');
  const step = Math.max(1, Math.ceil(n / 7));
  const ticks = R.cur.map((r, i) => (i % step === 0 || i === n - 1 ? `<text x="${x(i).toFixed(1)}" y="${H - 8}" text-anchor="${i === 0 ? 'start' : i === n - 1 ? 'end' : 'middle'}" class="tl">${esc(shortDate(r.date))}</text>` : '')).join('');
  const ptsC = cur.map((v, i) => (v === null || !Number.isFinite(v) ? null : [x(i), y(v)]));
  const line = smoothPath(ptsC), bridge = bridgePath(ptsC);
  const area = `<path d="${areaPath(ptsC, H - B)}" style="fill:var(--ink);opacity:.06"/>`;
  const ptsP = prev ? prev.map((v, i) => (v === null || !Number.isFinite(v) ? null : [x(i), y(v)])) : null;
  const prevLine = prev ? `<path d="${smoothPath(ptsP)}${bridgePath(ptsP)}" style="fill:none;stroke:var(--faint)" stroke-width="2" stroke-dasharray="5 5" stroke-linecap="round"/>` : '';
  const gapNote = ptsC.some((p) => p === null) ? `<path d="${bridge}" style="fill:none;stroke:var(--ink);opacity:.35" stroke-width="1.5" stroke-dasharray="2 5"/>` : '';
  const label = { spend: 'Daily spend', value: 'Daily purchase value', roas: 'ROAS, rolling 7 days' }[OV.metric];
  return `<section class="tile flow c-8" aria-label="Money flow">
    <div class="tile-head"><div><h2>Money flow</h2><div class="sub">${label}${OV.metric !== 'spend' ? '. Dotted stretches are days with no reported value.' : ''}</div></div>
      <div class="seg" role="group" aria-label="Metric">${[['spend', 'Spend'], ['value', 'Value'], ['roas', 'ROAS']].map(([k, l]) => `<button type="button" data-metric="${k}" aria-pressed="${OV.metric === k}">${l}</button>`).join('')}</div></div>
    <div class="legend"><span><i style="background:var(--ink)"></i>This period</span>${prev ? '<span><i style="background:var(--faint)"></i>Previous period (dashed)</span>' : ''}</div>
    <svg id="flowSvg" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(label)} for the selected dates">${grid}${area}${prevLine}${gapNote}<path d="${line}" style="fill:none;stroke:var(--ink)" stroke-width="2.5" stroke-linecap="round"/>${ticks}
      <line id="flowX" x1="0" x2="0" y1="${T}" y2="${H - B}" style="stroke:var(--muted)" stroke-dasharray="3 3" visibility="hidden"/><circle id="flowDot" r="5" style="fill:var(--surface);stroke:var(--ink)" stroke-width="2.5" visibility="hidden"/>
      <rect x="${L}" y="${T}" width="${W - L - Rt}" height="${H - T - B}" style="fill:transparent" id="flowHit"/></svg>
  </section>`;
}
function wireFlow(R) {
  const svg = $('flowSvg');
  if (!svg) return;
  const { W, H, L, R: Rt, T, B } = FLOW;
  const { cur, prev } = flowData(R);
  const n = cur.length;
  const all = [...cur, ...(prev || [])].filter((v) => v !== null && Number.isFinite(v));
  const max = Math.max(...all, 0) * 1.08 || 1;
  const f = OV.metric === 'roas' ? (v) => v.toFixed(2) + 'x' : money;
  const move = (e) => {
    const box = svg.getBoundingClientRect();
    const px = (e.clientX - box.left) / box.width * W;
    const i = Math.max(0, Math.min(n - 1, Math.round((px - L) / ((W - L - Rt) / Math.max(1, n - 1)))));
    const cx = L + (n === 1 ? (W - L - Rt) / 2 : i * (W - L - Rt) / (n - 1));
    const v = cur[i];
    $('flowX').setAttribute('x1', cx); $('flowX').setAttribute('x2', cx); $('flowX').setAttribute('visibility', 'visible');
    if (v !== null && Number.isFinite(v)) { $('flowDot').setAttribute('cx', cx); $('flowDot').setAttribute('cy', T + (H - T - B) * (1 - v / max)); $('flowDot').setAttribute('visibility', 'visible'); } else $('flowDot').setAttribute('visibility', 'hidden');
    const r = R.cur[i];
    const rows = [['This period', v !== null && Number.isFinite(v) ? f(v) : 'Unavailable']];
    if (prev) rows.push([`Same day before (${shortDate(R.prev[i].date)})`, prev[i] !== null && Number.isFinite(prev[i]) ? f(prev[i]) : 'Unavailable']);
    if (OV.metric !== 'spend') rows.push(['Spend', money(r.spend)]);
    rows.push(['Purchases', String(Math.round(r.purch))]);
    showTip(e.clientX, e.clientY, new Date(r.date + 'T00:00:00Z').toLocaleDateString('en-IN', { weekday: 'short', day: 'numeric', month: 'short', timeZone: 'UTC' }), rows);
  };
  const hide = () => { $('flowX').setAttribute('visibility', 'hidden'); $('flowDot').setAttribute('visibility', 'hidden'); hideTip(); };
  svg.addEventListener('pointermove', move);
  svg.addEventListener('pointerleave', hide);
}
function topAdsTile() {
  const top = VIEW.collections.all.ad_ids.slice(0, 6).map((id) => VIEW.ads[id]);
  const vcls = { scale: 'v-scale', watch: 'v-watch', cut: 'v-cut' };
  return `<section class="tile c-4" aria-label="Top ads by spend">
    <div class="tile-head"><div><h2>Top ads</h2><div class="sub">By spend in these dates</div></div><button class="go" type="button" data-goto="gallery" aria-label="See all ads">${ARROW}</button></div>
    <div class="adlist">${top.map((a) => { const m = a.view.metrics, src = thumbSrc(a.id); return `<button class="adrow" type="button" data-open="${esc(a.id)}"><span class="th">${src ? `<img src="${src}" alt="" loading="lazy">` : ''}</span><span style="min-width:0"><div class="nm">${esc(a.name)}</div><div class="mt">${esc(a.creative.type_label)} · #${a.view.rank_by_spend}</div></span><span class="rt"><b>${compact(m.spend)}</b><span class="chip ${vcls[a.view.verdict.code] || ''}">${m.roas !== null ? m.roas.toFixed(2) + 'x' : 'No value'}</span></span></button>`; }).join('')}</div>
  </section>`;
}
function mixTile() {
  const t = VIEW.totals;
  const rows = Object.entries(VIEW.by_type).map(([k, x]) => ({ k, ...x })).sort((a, b) => b.spend - a.spend);
  return `<section class="tile c-4" aria-label="Spend by format">
    <div class="tile-head"><div><h2>Format mix</h2><div class="sub">Share of spend, with ROAS</div></div></div>
    <div class="stackbar" role="img" aria-label="Spend share by format">${rows.map((r) => `<span style="flex:${r.spend};background:${FORMAT_COLOR[r.k] || 'var(--faint)'}" data-tip="${esc(`${r.label}|Spend|${money(r.spend)}|Share|${(r.spend / t.spend * 100).toFixed(1)}%|ROAS|${r.roas !== null ? r.roas.toFixed(2) + 'x' : 'Unavailable'}`)}"></span>`).join('')}</div>
    <div>${rows.map((r) => `<div class="mixrow"><i style="background:${FORMAT_COLOR[r.k] || 'var(--faint)'}"></i><span>${esc(r.label)} <span class="muted small">${r.ads} ads</span></span><span class="v">${(r.spend / t.spend * 100).toFixed(1)}%</span><span class="r">${r.roas !== null ? r.roas.toFixed(2) + 'x' : '–'}</span></div>`).join('')}</div>
  </section>`;
}
function alertsTile() {
  const list = ENGINE.anomalies(VIEW).slice(0, 5);
  return `<section class="tile darklist c-4" aria-label="Alerts">
    <div class="tile-head"><h2>Alerts</h2><div style="display:flex;gap:10px;align-items:center"><span class="count">${ENGINE.anomalies(VIEW).length}</span><button class="go" type="button" data-goto="insights" aria-label="Open insights">${ARROW}</button></div></div>
    ${list.length ? list.map((x) => {
      const up = x.flags.every((f) => f.change > 0), down = x.flags.every((f) => f.change < 0);
      const f = x.flags[0];
      const txt = f.kind === 'spend' ? `Spend ${f.change > 0 ? '+' : ''}${(f.change * 100).toFixed(0)}% vs usual` : `ROAS ${f.change > 0 ? '+' : ''}${(f.change * 100).toFixed(0)}% vs usual`;
      const d = new Date(x.date + 'T00:00:00Z');
      return `<div class="dl-row"><span class="dl-ic">${d.getUTCDate()}<br>${d.toLocaleDateString('en-IN', { month: 'short', timeZone: 'UTC' })}</span><span style="min-width:0"><div class="t">${esc(txt)}${x.flags.length > 1 ? ' · ROAS too' : ''}</div><div class="s">${x.drivers[0] ? esc(x.drivers[0].name) : ''}</div></span><span class="dot ${up ? 'up' : down ? 'down' : 'mix'}" title="${up ? 'Up' : down ? 'Down' : 'Mixed'}"></span></div>`;
    }).join('') : '<p class="small" class="muted">No sharp moves in these dates.</p>'}
  </section>`;
}
function competitorTile() {
  const c = COMPETITORS;
  if (!c || !c.brands) return '';
  const maxN = Math.max(...c.brands.map((b) => b.active_ads_estimate || 0), 1);
  return `<section class="tile c-4" aria-label="Competitors">
    <div class="tile-head"><div><h2>Competitors</h2><div class="sub">Active ads in Meta Ad Library</div></div><button class="go" type="button" data-goto="competitors" aria-label="Open competitors">${ARROW}</button></div>
    <div>${c.brands.map((b) => { const longest = Math.max(...b.messages.map((m) => m.days_running)); return `<div class="brandrow"><span class="monogram">${esc(b.name.replace(/^Mia by /, '').slice(0, 1))}</span><span style="min-width:0"><div class="n">${esc(b.name)}</div><div class="s">Longest running ${longest} day${longest === 1 ? '' : 's'} · ${b.messages.length} headlines</div><div class="meter" style="margin-top:4px"><div class="bar"><i style="width:${(b.active_ads_estimate || 0) / maxN * 100}%;background:var(--gold)"></i></div></div></span><span class="c">${b.active_ads_estimate}<span>active</span></span></div>`; }).join('')}</div>
  </section>`;
}
function weekdayTile() {
  const dow = ENGINE.dayOfWeek(VIEW.range.since, VIEW.range.until, state.kw, state.camp);
  const best = dow.reduce((b, x) => (x.roas !== null && (!b || x.roas > b.roas) ? x : b), null);
  // Bar height = ROAS on one scale from 0, so the tallest bar is the best day.
  const W = 620, H = 230, L = 40, R = 8, T = 26, B = 44;
  const top = Math.max(...dow.map((x) => x.roas || 0), 0.5);
  const step = top > 4 ? 2 : top > 2 ? 1 : 0.5;
  const max = Math.ceil(top / step) * step;
  const y = (v) => T + (H - T - B) * (1 - v / max);
  const slot = (W - L - R) / dow.length, bw = Math.min(34, slot * 0.46);
  const ticks = [];
  for (let v = 0; v <= max + 1e-9; v += step) ticks.push(v);
  const grid = ticks.map((v) => `<line x1="${L}" x2="${W - R}" y1="${y(v).toFixed(1)}" y2="${y(v).toFixed(1)}" style="stroke:var(--line)"${v === 0 ? '' : ' stroke-dasharray="3 4"'}/><text x="${L - 8}" y="${(y(v) + 4).toFixed(1)}" text-anchor="end" style="fill:var(--muted);font-size:11px">${v % 1 ? v.toFixed(1) : v}x</text>`).join('');
  const bars = dow.map((x, i) => {
    const cx = L + slot * i + slot / 2, isBest = best && x.key === best.key;
    const v = x.roas, h = v === null ? 0 : H - B - y(v);
    const tip = esc(`${x.key}|ROAS|${v !== null ? v.toFixed(2) + 'x' : 'Unavailable'}|Spend a day|${money(x.spend_per_day)}|Days in range|${x.days}`);
    const bar = v === null ? `<text x="${cx}" y="${H - B - 6}" text-anchor="middle" style="fill:var(--faint);font-size:11px">n/a</text>`
      : `<path d="M${(cx - bw / 2).toFixed(1)},${(H - B).toFixed(1)} V${(y(v) + 6).toFixed(1)} Q${(cx - bw / 2).toFixed(1)},${y(v).toFixed(1)} ${(cx - bw / 2 + 6).toFixed(1)},${y(v).toFixed(1)} H${(cx + bw / 2 - 6).toFixed(1)} Q${(cx + bw / 2).toFixed(1)},${y(v).toFixed(1)} ${(cx + bw / 2).toFixed(1)},${(y(v) + 6).toFixed(1)} V${(H - B).toFixed(1)} Z" style="fill:${isBest ? 'var(--gold)' : '#dcd8cf'}"/>
        <text x="${cx}" y="${(y(v) - 7).toFixed(1)}" text-anchor="middle" style="fill:var(--ink);font:700 12px var(--display)">${v.toFixed(2)}x</text>`;
    return `<g data-tip="${tip}"><rect x="${(cx - slot / 2).toFixed(1)}" y="${T - 20}" width="${slot.toFixed(1)}" height="${H - T + 20}" style="fill:transparent"/>${bar}
      <text x="${cx}" y="${H - B + 17}" text-anchor="middle" style="fill:${isBest ? 'var(--ink)' : 'var(--muted)'};font-size:12px;font-weight:${isBest ? 700 : 500}">${x.key.slice(0, 3)}</text>
      <text x="${cx}" y="${H - B + 33}" text-anchor="middle" style="fill:var(--faint);font-size:10.5px">${esc(compact(x.spend_per_day))}/day</text></g>`;
  }).join('');
  return `<section class="tile c-6" aria-label="Day of week">
    <div class="tile-head"><div><h2>Meta ROAS by weekday</h2><div class="sub">Meta's own count, drawn from 0. Spend a day below each bar.${best ? ` Best: ${best.key}.` : ''}</div></div><button class="go" type="button" data-goto="insights" aria-label="Open insights">${ARROW}</button></div>
    <svg viewBox="0 0 ${W} ${H}" style="width:100%;height:auto;display:block" role="img" aria-label="ROAS by day of week">${grid}${bars}</svg>
  </section>`;
}
function anglesTile() {
  const rows = ENGINE.themes(VIEW).angle.slice(0, 6);
  const total = rows.reduce((s, r) => s + r.spend, 0) || 1;
  const max = Math.max(...rows.map((r) => r.spend), 1);
  return `<section class="tile c-6" aria-label="Creative angles">
    <div class="tile-head"><div><h2>What kind of ad works</h2><div class="sub">Bar: spend by creative angle. Number: ROAS.</div></div><button class="go" type="button" data-goto="insights" aria-label="Open insights">${ARROW}</button></div>
    <div>${rows.map((r) => `<div class="hbar" data-tip="${esc(`${r.label}|Ads|${r.ads}|Spend|${money(r.spend)}|Share|${(r.spend / total * 100).toFixed(1)}%|ROAS|${r.roas !== null ? r.roas.toFixed(2) + 'x' : 'Unavailable'}`)}"><span class="l">${esc(r.label)}</span><span class="t"><i style="width:${Math.max(2, r.spend / max * 100)}%"></i></span><span class="r">${r.roas !== null ? r.roas.toFixed(2) + 'x' : '–'}</span></div>`).join('')}</div>
    <p class="small muted" style="margin:0">Tagged from ad names and copy, so treat as a guide.</p>
  </section>`;
}

// ---------- brand (all channels) ----------
// The top of the overview is the whole brand: website sales from Metabase. Ad channels sit under it.
// Only Meta is connected today. Google and email are listed so the team sees they are not counted yet.
const OV_CHANNELS = [
  { key: 'meta', name: 'Meta ads', live: true },
  { key: 'google', name: 'Google ads', live: false },
  { key: 'email', name: 'Email and WhatsApp', live: false },
];
const OV_WD = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
OV.dayMode = OV.dayMode || 'cap';

function ovBrand() {
  if (!SL.data) return null;
  const last = rpLastSalesDay(), r = VIEW.range;
  const until = r.until > last ? last : r.until, since = r.since;
  if (!last || since > until) return null;
  const n = Math.round((new Date(until + 'T00:00:00Z') - new Date(since + 'T00:00:00Z')) / 864e5) + 1;
  const cur = rpBrand(since, until), prev = rpBrand(addDays(since, -n), addDays(since, -1));
  return { cur, prev, cut: until < r.until, until, n, full: cur.covered === cur.n && prev.covered === prev.n };
}
function ovChip(cur, prev, good, B) {
  if (!$('compare').checked || !B.full || cur === null || cur === undefined || !prev) return '';
  const ch = (cur - prev) / Math.abs(prev);
  if (!Number.isFinite(ch)) return '';
  const tone = Math.abs(ch) < 0.005 ? 'flat' : (ch > 0) === (good > 0) ? '' : 'bad';
  return `<span class="dchip ${tone}" title="vs the ${B.n} days before">${ch > 0 ? '▲' : ch < 0 ? '▼' : ''} ${Math.abs(ch * 100).toFixed(1)}%</span>`;
}
const ovQ = (s, q) => { if (!s.length) return null; const i = (s.length - 1) * q, lo = Math.floor(i), hi = Math.ceil(i); return s[lo] + (s[hi] - s[lo]) * (i - lo); };
// Big days: far above a normal day. Median + 3.5 robust spreads (MAD), and at least 2x the median.
function ovCap(vals) {
  const s = vals.filter((v) => v !== null && Number.isFinite(v)).sort((a, b) => a - b);
  if (s.length < 7) return null;
  const med = ovQ(s, 0.5), mad = ovQ(s.map((v) => Math.abs(v - med)).sort((a, b) => a - b), 0.5) * 1.4826;
  return { med, cap: Math.max(med + 3.5 * mad, 2 * med) };
}
function ovDays(B) {
  const rows = B.cur.days.filter((r) => r.x && r.x.sales !== null);
  const sc = ovCap(rows.map((r) => r.x.sales)), mc = ovCap(rows.map((r) => r.claimed));
  return { rows, sc, mc, big: sc ? rows.filter((r) => r.x.sales > sc.cap) : [] };
}

function brandHero(B) {
  const c = B.cur, p = B.prev;
  const per = c.sales !== null && c.spend ? c.sales / c.spend : null;
  const { rows, sc, big } = ovDays(B);
  const W = 640, H = 170, L = 6, R = 6, T = 10, Bt = 20, n = c.days.length;
  const slot = (W - L - R) / n, bw = Math.max(1.5, slot * 0.72);
  // Keep the scale for normal days; bars for big days reach the top with their value on them.
  const normalMax = Math.max(...rows.filter((r) => !sc || r.x.sales <= sc.cap).map((r) => r.x.sales), 1);
  const top = normalMax * 1.12, smax = Math.max(...c.days.map((r) => r.spend), 1) * 1.15;
  const y = (v) => T + (H - T - Bt) * (1 - Math.min(v, top) / top), ys = (v) => T + (H - T - Bt) * (1 - v / smax);
  const bigSet = new Set(big.map((r) => r.d));
  // Label the cut bars, biggest first, skipping any that would sit on top of a label already placed.
  const labelled = new Set(), placed = [];
  for (const r of big.slice().sort((a, b) => b.x.sales - a.x.sales)) {
    const i = c.days.findIndex((d) => d.d === r.d), cx = L + slot * i + slot / 2;
    if (r.x.sales > top && placed.every((px) => Math.abs(px - cx) > 58)) { placed.push(cx); labelled.add(r.d); }
  }
  const bars = c.days.map((r, i) => {
    const cx = L + slot * i + slot / 2;
    const tip = esc(`${new Date(r.d + 'T00:00:00Z').toLocaleDateString('en-IN', { weekday: 'short', day: 'numeric', month: 'short', timeZone: 'UTC' })}|Website sales|${r.x && r.x.sales !== null ? money(r.x.sales) : 'Not available'}|Orders|${r.x ? r.x.orders : 'Not available'}|Meta spend|${money(r.spend)}|Sales per ₹1 of ads|${r.x && r.x.sales !== null && r.spend ? '₹' + (r.x.sales / r.spend).toFixed(1) : 'Not available'}${bigSet.has(r.d) ? '|Note|Big day, bar cut at the top' : ''}`);
    const hit = `<rect x="${(cx - slot / 2).toFixed(1)}" y="${T}" width="${slot.toFixed(1)}" height="${H - T - Bt}" style="fill:transparent" data-tip="${tip}"/>`;
    if (!r.x || r.x.sales === null) return hit;
    const yy = y(r.x.sales), clip = r.x.sales > top;
    return `<rect x="${(cx - bw / 2).toFixed(1)}" y="${yy.toFixed(1)}" width="${bw.toFixed(1)}" height="${(H - Bt - yy).toFixed(1)}" rx="${Math.min(2, bw / 2)}" style="fill:rgba(22,20,15,${clip ? '.95' : '.62'})" pointer-events="none"/>${clip && labelled.has(r.d) ? `<text x="${cx.toFixed(1)}" y="${T + 11}" text-anchor="${i > n - 4 ? 'end' : i < 3 ? 'start' : 'middle'}" style="fill:#fff;font:700 10.5px var(--display);paint-order:stroke;stroke:#16140f;stroke-width:3px" pointer-events="none">${esc(compact(r.x.sales))}</text>` : ''}${hit}`;
  }).join('');
  const sp = c.days.map((r, i) => [L + slot * i + slot / 2, ys(r.spend)]);
  const spend = `<path d="${smoothPath(sp)}" style="fill:none;stroke:#fff" stroke-width="2.4" stroke-linecap="round" pointer-events="none"/>`;
  const ticks = [0, Math.floor((n - 1) / 2), n - 1].map((i, k) => `<text x="${(L + slot * i + slot / 2).toFixed(1)}" y="${H - 5}" text-anchor="${['start', 'middle', 'end'][k]}" style="fill:#5a4300;font-size:11px">${esc(shortDate(c.days[i].d))}</text>`).join('');
  return `<section class="tile hero c-8" aria-label="Website sales">
    <div class="label">Website sales · ${esc(shortDate(c.since))} to ${esc(shortDate(c.until))} · ${B.n} days${B.cut ? ' · website figures run to the last day we have' : ''}</div>
    <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap"><div class="big">${c.sales !== null ? compact(c.sales) : 'Not available'}</div>${ovChip(c.sales, p.sales, 1, B)}</div>
    <div class="ov-legend"><span><i class="sw-bar"></i>Website sales a day</span><span><i class="sw-line"></i>Meta spend a day (own scale)</span>${big.length ? `<span>${big.length} big day${big.length > 1 ? 's' : ''} cut at the top</span>` : ''}</div>
    <svg viewBox="0 0 ${W} ${H}" class="ov-combo" role="img" aria-label="Website sales a day with Meta spend on top">${bars}${spend}${ticks}</svg>
    <div class="trio">
      <div><span>Ad spend (Meta)</span><b>${compact(c.spend)}</b></div>
      <div><span>Website visits</span><b>${c.visits !== null ? fmt(c.visits, 'int') : 'Not available'}</b></div>
      <div><span>Orders per 10,000 visits</span><b>${c.conv !== null ? (c.conv * 1e4).toFixed(1) : 'Not available'}</b></div>
    </div>
    ${c.covered < c.n ? `<p class="small" style="margin:0;color:#5a4300">Website data is missing for ${c.n - c.covered} of ${c.n} days. Totals cover the days we have.</p>` : ''}
    <div class="actions"><button class="btn dark" type="button" data-goto="sales">Brand sales</button><button class="btn ghost" type="button" data-goto="report">Client report</button></div>
  </section>`;
}

function channelsTile(B) {
  const c = B.cur, seen = c.days.filter((r) => r.claimed !== null);
  const claimed = seen.length ? seen.reduce((t, r) => t + r.claimed, 0) : null;
  const share = claimed !== null && c.sales ? claimed / c.sales : null;
  const rest = claimed !== null && c.sales !== null ? Math.max(0, c.sales - claimed) : null;
  const row = (ch) => ch.key === 'meta'
    ? `<button class="chrow" type="button" data-goto-meta="1"><span class="chn"><i style="background:var(--spend)"></i>${esc(ch.name)}</span><span class="chv"><b>${compact(c.spend)}</b> spent</span><span class="chv"><b>${claimed !== null ? compact(claimed) : 'Not available'}</b> sales Meta counts${share !== null ? ` · ${(share * 100).toFixed(0)}%` : ''}</span></button>`
    : `<div class="chrow off"><span class="chn"><i></i>${esc(ch.name)}</span><span class="chv muted">Not connected yet</span></div>`;
  return `<section class="tile c-4" aria-label="Sales by channel">
    <div class="tile-head"><div><h2>Where sales come from</h2><div class="sub">Each channel's own count of website sales</div></div></div>
    ${share !== null ? `<div class="stackbar" role="img" aria-label="Share of website sales Meta counts"><span style="flex:${Math.min(claimed, c.sales)};background:var(--spend)" data-tip="${esc(`Meta ads|Sales Meta counts|${money(claimed)}|Share|${(share * 100).toFixed(1)}%`)}"></span><span style="flex:${rest};background:var(--faint)" data-tip="${esc(`Not counted by an ad channel|Sales|${money(rest)}|Share|${((1 - share) * 100).toFixed(1)}%`)}"></span></div>` : ''}
    <div class="chlist">${OV_CHANNELS.map(row).join('')}
      <div class="chrow"><span class="chn"><i style="background:var(--faint)"></i>Not counted by an ad channel</span><span class="chv"><b>${rest !== null ? compact(rest) : 'Not available'}</b> direct, search, repeat buyers and more</span></div>
      <div class="chrow off"><span class="chn"><i></i>New vs repeat buyers</span><span class="chv muted">Not available yet. Needs 1 Metabase card: orders by day, first order vs repeat.</span></div></div>
    <p class="small muted" style="margin:0">Meta counts a sale after a click or view, so its number can overlap with others. Google and email show here once connected.</p>
  </section>`;
}

function brandKpis(B) {
  const c = B.cur, p = B.prev, Bk = buckets(c.days);
  const got = (s) => s.filter((r) => r.x && r.x.sales !== null);
  const sumX = (s, k) => got(s).reduce((t, r) => t + (r.x[k] || 0), 0);
  const series = {
    orders: Bk.map((s) => (got(s).length ? sumX(s, 'orders') : null)),
    aov: Bk.map((s) => { const o = sumX(s, 'orders'); return o ? sumX(s, 'sales') / o : null; }),
    per: Bk.map((s) => { const sp = s.reduce((t, r) => t + r.spend, 0); return got(s).length && sp ? sumX(s, 'sales') / sp : null; }),
    refund: Bk.map((s) => (got(s).length ? sumX(s, 'refund') : null)),
  };
  const per = c.sales !== null && c.spend ? c.sales / c.spend : null, pper = p.sales !== null && p.spend ? p.sales / p.spend : null;
  const unit = c.days.length <= 21 ? 'day' : 'week';
  const tile = (cls, name, val, chip, vals, foot) => `<section class="tile kt ${cls} c-3"><div class="kname">${name}</div><div class="krow"><div class="kval">${val}</div>${chip}</div>${sparkSvg(vals, { color: 'var(--ink)' })}<div class="kfoot">${foot}</div></section>`;
  return tile('mint', 'Orders', c.orders !== null ? fmt(c.orders, 'int') : NA, ovChip(c.orders, p.orders, 1, B), series.orders, `Per ${unit}. About ${c.orders !== null && c.covered ? (c.orders / c.covered).toFixed(1) : '–'} a day.`) +
    tile('sky', 'Average order', c.aov !== null ? compact(c.aov) : NA, ovChip(c.aov, p.aov, 1, B), series.aov, `Per ${unit}. Big single orders lift this.`) +
    tile('lav', 'Sales per ₹1 of ads', per !== null ? '₹' + per.toFixed(1) : NA, ovChip(per, pper, 1, B), series.per, `Per ${unit}. All website sales ÷ ad spend.`) +
    tile('peach', 'Refunds', c.refund !== null ? compact(c.refund) : NA, ovChip(c.refund, p.refund, -1, B), series.refund, `Per ${unit}. ${c.refund !== null && c.sales ? (c.refund / c.sales * 100).toFixed(1) + '% of sales.' : ''} Lower is better.`);
}

// Best day to spend, from website sales (not only Meta's count), with big days handled.
function ovWeekdays(B, mode) {
  const { rows, sc, mc } = ovDays(B);
  const acc = Object.fromEntries(OV_WD.map((k) => [k, { key: k, n: 0, sales: 0, spend: 0, value: 0, valueN: 0 }]));
  for (const r of rows) {
    const bigS = sc && r.x.sales > sc.cap, bigM = mc && r.claimed !== null && r.claimed > mc.cap;
    if (mode === 'drop' && (bigS || bigM)) continue;
    const s = mode === 'cap' && bigS ? sc.cap : r.x.sales;
    const v = r.claimed === null ? null : mode === 'cap' && bigM ? mc.cap : r.claimed;
    const o = acc[weekday(r.d)];
    if (!o) continue;
    o.n += 1; o.sales += s; o.spend += r.spend;
    if (v !== null) { o.value += v; o.valueN += 1; }
  }
  return OV_WD.map((k) => {
    const o = acc[k];
    return { ...o, per: o.spend ? o.sales / o.spend : null, roas: o.spend && o.valueN ? o.value / o.spend : null, salesDay: o.n ? o.sales / o.n : null, spendDay: o.n ? o.spend / o.n : null };
  });
}
function bestDayTile(B) {
  const mode = OV.dayMode, dow = ovWeekdays(B, mode), raw = mode === 'raw' ? null : ovWeekdays(B, 'raw');
  const ok = dow.filter((x) => x.per !== null && x.n >= 4);
  const avg = ok.length ? ok.reduce((t, x) => t + x.sales, 0) / ok.reduce((t, x) => t + x.spend, 0) : null;
  const ranked = ok.slice().sort((a, b) => b.per - a.per), best = ranked[0], worst = ranked[ranked.length - 1];
  const clear = best && avg && best.per / avg >= 1.15;
  const W = 640, H = 240, L = 40, R = 8, T = 26, Bt = 52;
  const vals = [...dow, ...(raw || [])].map((x) => x.per || 0);
  const topv = Math.max(...vals, 1), step = topv > 20 ? 10 : topv > 8 ? 4 : topv > 4 ? 2 : 1, max = Math.ceil(topv / step) * step;
  const y = (v) => T + (H - T - Bt) * (1 - v / max);
  const slot = (W - L - R) / 7, bw = Math.min(40, slot * 0.5);
  const grid = [];
  for (let v = 0; v <= max + 1e-9; v += step) grid.push(`<line x1="${L}" x2="${W - R}" y1="${y(v).toFixed(1)}" y2="${y(v).toFixed(1)}" style="stroke:var(--line)"${v ? ' stroke-dasharray="3 4"' : ''}/><text x="${L - 8}" y="${(y(v) + 4).toFixed(1)}" text-anchor="end" style="fill:var(--muted);font-size:11px">₹${v}</text>`);
  const avgLine = avg ? `<line x1="${L}" x2="${W - R}" y1="${y(avg).toFixed(1)}" y2="${y(avg).toFixed(1)}" style="stroke:var(--ink)" stroke-width="1.2" stroke-dasharray="6 4"/><text x="${W - R}" y="${(y(avg) - 5).toFixed(1)}" text-anchor="end" style="fill:var(--ink);font-size:11px">Average ₹${avg.toFixed(1)}</text>` : '';
  const bars = dow.map((x, i) => {
    const cx = L + slot * i + slot / 2, isBest = clear && best && x.key === best.key, r0 = raw && raw[i];
    const tip = esc(`${x.key}|Sales per ₹1 of ads|${x.per !== null ? '₹' + x.per.toFixed(1) : 'Not available'}${r0 && r0.per !== null ? `|Before handling big days|₹${r0.per.toFixed(1)}` : ''}|Website sales a day|${x.salesDay !== null ? money(x.salesDay) : 'Not available'}|Meta spend a day|${x.spendDay !== null ? money(x.spendDay) : 'Not available'}|Meta ROAS|${x.roas !== null ? x.roas.toFixed(2) + 'x' : 'Not available'}|Days counted|${x.n}`);
    const ghost = r0 && r0.per !== null && Math.abs(r0.per - (x.per || 0)) > 0.05 ? `<rect x="${(cx - bw / 2).toFixed(1)}" y="${y(r0.per).toFixed(1)}" width="${bw.toFixed(1)}" height="${(H - Bt - y(r0.per)).toFixed(1)}" rx="6" style="fill:none;stroke:var(--faint)" stroke-dasharray="3 3"/>` : '';
    const bar = x.per === null ? `<text x="${cx}" y="${H - Bt - 6}" text-anchor="middle" style="fill:var(--faint);font-size:11px">n/a</text>`
      : `<rect x="${(cx - bw / 2).toFixed(1)}" y="${y(x.per).toFixed(1)}" width="${bw.toFixed(1)}" height="${(H - Bt - y(x.per)).toFixed(1)}" rx="6" style="fill:${isBest ? 'var(--gold)' : '#dcd8cf'}"/><text x="${cx}" y="${(y(Math.max(x.per, r0 && r0.per ? r0.per : 0)) - 7).toFixed(1)}" text-anchor="middle" style="fill:var(--ink);font:700 12px var(--display)">₹${x.per.toFixed(1)}</text>`;
    return `<g data-tip="${tip}"><rect x="${(cx - slot / 2).toFixed(1)}" y="${T - 20}" width="${slot.toFixed(1)}" height="${H - T + 20}" style="fill:transparent"/>${ghost}${bar}
      <text x="${cx}" y="${H - Bt + 17}" text-anchor="middle" style="fill:${isBest ? 'var(--ink)' : 'var(--muted)'};font-size:12px;font-weight:${isBest ? 700 : 500}">${x.key}</text>
      <text x="${cx}" y="${H - Bt + 32}" text-anchor="middle" style="fill:var(--faint);font-size:10.5px">${x.spendDay !== null ? esc(compact(x.spendDay)) : '–'} ads</text>
      <text x="${cx}" y="${H - Bt + 46}" text-anchor="middle" style="fill:var(--faint);font-size:10.5px">${x.n} days</text></g>`;
  }).join('');
  const modes = [['raw', 'As is'], ['cap', 'Cap big days'], ['drop', 'Drop big days']];
  const msg = !ok.length ? 'Not enough days with website sales in these dates.'
    : clear ? `<b>${best.key}</b> brings ₹${best.per.toFixed(1)} of website sales per ₹1 of ads, ${((best.per / avg - 1) * 100).toFixed(0)}% above the average day. <b>${worst.key}</b> is lowest at ₹${worst.per.toFixed(1)}. Try moving 10 to 15% of the ${esc(worst.key)} budget to ${esc(best.key)} for 2 weeks, then check again.`
      : `No day is clearly better: the best (${esc(best.key)}, ₹${best.per.toFixed(1)}) is within 15% of the average. Keep spend steady across the week.`;
  return `<section class="tile c-8" aria-label="Best day to spend">
    <div class="tile-head"><div><h2>Best day to spend</h2><div class="sub">All website sales per ₹1 of ads, by weekday. Dashed outline: before big days were handled.</div></div>
      <div class="seg" role="group" aria-label="Big days">${modes.map(([k, l]) => `<button type="button" data-daymode="${k}" aria-pressed="${mode === k}">${l}</button>`).join('')}</div></div>
    <svg viewBox="0 0 ${W} ${H}" style="width:100%;height:auto;display:block" role="img" aria-label="Sales per rupee of ads by weekday">${grid.join('')}${avgLine}${bars}</svg>
    <p class="ov-say">${msg}</p>
    <p class="small muted" style="margin:0">Buyers often take 7 to 14 days from first ad to purchase, so this shows the days people buy more than the days ads work best. Each weekday has about ${ok.length ? Math.round(ok.reduce((t, x) => t + x.n, 0) / ok.length) : 0} days here, so small gaps can be chance. Pick 90 days for a steadier read. "Cap" lowers big days to the normal top. "Drop" leaves them out.</p>
  </section>`;
}
function topPiecesTile(B) {
  const top = B.cur.skus.slice(0, 6);
  return `<section class="tile c-4" aria-label="Top pieces">
    <div class="tile-head"><div><h2>Top pieces</h2><div class="sub">By website sales in these dates</div></div><button class="go" type="button" data-goto="sales" aria-label="Open brand sales">${ARROW}</button></div>
    <div>${top.length ? top.map((s) => `<div class="mixrow"><i style="background:var(--s3)"></i><span style="min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${esc(s.name || s.code)}</span><span class="v">${esc(compact(s.v))}</span><span class="r">${s.n} sold</span></div>`).join('') : '<p class="muted small">No product data for these dates.</p>'}</div>
  </section>`;
}
function metaHeader() {
  return `<div class="ov-section ov-meta-h c-12"><div><h2>Meta ads</h2><p>1 of your ad channels. Google and email will sit next to it once connected.</p></div></div>`;
}
function brandBlock() {
  if (!SL.data) return `<section class="tile c-12"><p class="muted">${SL.err ? 'Website sales could not be loaded.' : 'Loading website sales…'}</p></section>`;
  const B = ovBrand();
  if (!B) return `<section class="tile c-12"><p class="muted">No website sales for these dates. Website data starts ${esc(shortDate(Object.keys(SL.data.daily_totals || SL.data.daily).sort()[0]))}.</p></section>`;
  return `<div class="ov-section c-12"><div><h2>Your brand</h2><p>Every website order, from every source.</p></div></div>
    ${brandHero(B)}${channelsTile(B)}${brandKpis(B)}
    ${pacingTile()}${brandAlertsTile()}${topPiecesTile(B)}
    ${bestDayTile(B)}${coTile(B)}
    ${lagTile()}${budgetPlanTile(B)}
    ${visitsTile()}${payTile()}
    ${geoTile()}`;
}

// ---------- tooltip ----------
function showTip(cx, cy, title, rows) {
  const tip = $('tip');
  tip.innerHTML = `<b>${esc(title)}</b>` + rows.map(([k, v]) => `<div class="r"><span>${esc(k)}</span><span>${esc(v)}</span></div>`).join('');
  tip.hidden = false;
  const w = tip.offsetWidth, h = tip.offsetHeight;
  let x = cx + 14, y = cy - h - 12;
  if (x + w > window.innerWidth - 8) x = cx - w - 14;
  if (y < 8) y = cy + 16;
  tip.style.left = Math.max(8, x) + 'px'; tip.style.top = y + 'px';
}
function hideTip() { $('tip').hidden = true; }
document.addEventListener('pointermove', (e) => {
  const el = e.target.closest && e.target.closest('[data-tip]');
  if (!el) { if (!e.target.closest || !e.target.closest('#flowSvg')) hideTip(); return; }
  const parts = el.dataset.tip.split('|');
  const rows = [];
  for (let i = 1; i + 1 < parts.length; i += 2) rows.push([parts[i], parts[i + 1]]);
  showTip(e.clientX, e.clientY, parts[0], rows);
});

window.renderOverview = function renderOverview() {
  if (!VIEW) return;
  const R = rangeDays();
  const excl = VIEW.exclusions.campaigns.length ? `<div class="note">${VIEW.exclusions.campaigns.length} campaign${VIEW.exclusions.campaigns.length > 1 ? 's' : ''} left out (${money(VIEW.exclusions.spend)}). Every tile below follows the filters.</div>` : '';
  if (!SL.data && !SL.err) loadSales().then(() => { if (state.tab === 'overview') window.renderOverview(); });
  if (!BX.loaded) bxBoot().then(() => { if (state.tab === 'overview') window.renderOverview(); });
  if (!CO.loaded) coBoot().then(() => { if (state.tab === 'overview') window.renderOverview(); });
  $('overviewView').innerHTML = `<div style="display:grid;gap:16px"><div class="bento">
    ${brandBlock()}
    ${metaHeader()}${excl ? `<div class="c-12">${excl}</div>` : ''}
    ${heroTile(R)}${spotlightTile()}${healthTile()}
    ${kpiTiles(R)}
    ${flowTile(R)}${topAdsTile()}
    ${mixTile()}${alertsTile()}${competitorTile()}
    ${weekdayTile()}${anglesTile()}
  </div></div>`;
  wireFlow(R);
};

document.addEventListener('click', (e) => {
  const view = $('overviewView');
  if (!view || view.hidden || !view.contains(e.target)) return;
  const hv = e.target.closest('[data-health]');
  if (hv) {
    // Open the gallery on every ad, grouped Scale, Cut, Watch, and jump to the group clicked.
    $('rankSet').value = 'health'; $('format').value = 'all'; $('sort').value = 'spend'; $('verdict').value = '';
    for (const id of ['minSpend', 'minRoas', 'campaign', 'adStatus', 'campStatus']) $(id).value = '';
    setTab('gallery'); fillFilters(); renderGrid(); remember();
    const code = hv.dataset.health;
    setTimeout(() => { const el = code === 'all' ? $('collectionLabel') : $('grp-' + code); if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' }); }, 250);
    return;
  }
  const go = e.target.closest('[data-goto]');
  if (go) { setTab(go.dataset.goto); window.scrollTo(0, 0); return; }
  const open = e.target.closest('[data-open]');
  if (open) { openSide(open.dataset.open); return; }
  const dm = e.target.closest('[data-daymode]');
  if (dm) { OV.dayMode = dm.dataset.daymode; window.renderOverview(); return; }
  if (e.target.closest('[data-goto-meta]')) { const h = document.querySelector('#overviewView .ov-meta-h'); if (h) h.scrollIntoView({ behavior: 'smooth', block: 'start' }); return; }
  const m = e.target.closest('[data-metric]');
  if (m) { OV.metric = m.dataset.metric; window.renderOverview(); }
});
