'use strict';
// Brand tools on the Overview: client orders, month pacing, brand alerts, new vs repeat buyers,
// ad-to-sale delay and a weekly budget plan. Uses SL, gaMap, addDays, weekday (sales.js), rpDay, rpBrand,
// rpBigMeta, rpLastSalesDay (report.js), metaDayMap (sales.js), compact, sparkSvg, ARROW (overview.js),
// saveDoc, copyBtn (lab.js), VIEW, ENGINE, esc, money, shortDate (app.js).

// ---------- client orders ----------
// A large order from 1 client (a bulk or trade order) is real revenue, but it hides how ads and the site
// do on a normal day. The team marks it once; Overview, the client report and the Buyer desk then leave
// that amount out. Brand sales keeps Metabase's own numbers.
const CO = { data: { marks: [] }, loaded: false, on: true, open: null, msg: '' };
try { CO.on = localStorage.getItem('client-orders-on') !== '0'; } catch (e) { /* storage unavailable */ }
async function coBoot() {
  if (CO.loaded) return;
  CO.loaded = true;
  try {
    const r = await fetch('client_orders.json');
    const j = r.ok ? await r.json() : null;
    if (j && Array.isArray(j.marks)) CO.data = { marks: j.marks.filter((m) => /^\d{4}-\d{2}-\d{2}$/.test(m.d) && m.amount > 0) };
  } catch (e) { /* no file yet */ }
}
function coMarks(d) { return CO.data.marks.filter((m) => m.d === d); }
// Called by rpDay: take marked client orders out of that day's sales and orders.
function coAdjust(d, x) {
  if (!CO.on || !x || x.sales === null) return x;
  const ms = coMarks(d);
  if (!ms.length) return x;
  const amt = Math.min(x.sales, ms.reduce((t, m) => t + m.amount, 0)), n = Math.min(x.orders || 0, ms.reduce((t, m) => t + (m.orders || 1), 0));
  return { ...x, sales: x.sales - amt, orders: (x.orders || 0) - n, client: amt, client_orders: n, raw_sales: x.sales };
}
async function coSave() {
  CO.msg = await saveDoc('client_orders.json', { marks: CO.data.marks, updated: new Date().toISOString().slice(0, 10) });
}
function coTile(B) {
  const c = B.cur, sc = ovDays(B).sc;
  const inRange = CO.data.marks.filter((m) => m.d >= c.since && m.d <= c.until).sort((a, b) => (a.d < b.d ? 1 : -1));
  // Days worth checking: big website days, and days where Meta counted 1 or 2 very large sales.
  const raw = (d) => { const x = rpDayRaw(d); return x ? x.sales : null; };
  const sug = [];
  for (const r of c.days) { const s = raw(r.d); if (sc && s !== null && s > sc.cap && !coMarks(r.d).length) sug.push({ d: r.d, why: `${compact(s)} in website sales, ${(s / sc.med).toFixed(0)}x a normal day`, amount: Math.round(s - sc.med) }); }
  for (const m of rpBigMeta(c.since, c.until)) if (!coMarks(m.d).length && !sug.some((x) => x.d === m.d)) sug.push({ d: m.d, why: `Meta counted ${m.purchases} sale${m.purchases > 1 ? 's' : ''} worth ${compact(m.value)} on "${m.name}"`, amount: Math.round(m.value) });
  sug.sort((a, b) => (a.d < b.d ? 1 : -1));
  const bigs = c.days.filter((r) => { const s = raw(r.d); return sc && s !== null && s > sc.cap; }), bigSum = bigs.reduce((t, r) => t + raw(r.d), 0), rawAll = c.days.reduce((t, r) => t + (raw(r.d) || 0), 0);
  const bigLine = bigs.length ? `<p class="small" style="margin:0">${bigs.length} big day${bigs.length > 1 ? 's' : ''} made ${esc(compact(bigSum))}, ${rawAll ? (bigSum / rawAll * 100).toFixed(0) : '–'}% of website sales here. If 1 client made a large order, mark it so it does not skew the numbers.</p>` : '';
  const left = inRange.reduce((t, m) => t + m.amount, 0);
  const form = (d, amount, why) => `<form class="co-form" data-coform="${esc(d)}"><div class="small muted">${esc(why)}</div>
      <label>Amount to leave out <input type="number" name="amount" min="1" step="1" value="${amount}" required></label>
      <label>Orders <input type="number" name="orders" min="1" step="1" value="1" required></label>
      <label class="wide">Note <input type="text" name="note" maxlength="80" placeholder="Client name or order number"></label>
      <div class="act-btns"><button class="btn small-btn" type="submit">Leave it out</button><button class="btn ghost small-btn" type="button" data-coclose>Cancel</button></div></form>`;
  return `<section class="tile c-4" aria-label="Client orders">
    <div class="tile-head"><div><h2>Big days and client orders</h2><div class="sub">${sc ? `A normal day is about ${esc(compact(sc.med))}. Big means over ${esc(compact(sc.cap))}.` : 'Needs 7 or more days of sales.'}</div></div></div>
    ${bigLine}
    <label class="co-toggle"><input type="checkbox" data-coon ${CO.on ? 'checked' : ''}> Leave client orders out${left ? ` · ${esc(compact(left))} left out here` : ''}</label>
    ${inRange.length ? `<div>${inRange.map((m) => `<div class="mixrow"><i style="background:var(--ink)"></i><span>${esc(weekday(m.d))} ${esc(shortDate(m.d))} <span class="muted small">${esc(m.note || '')}</span></span><span class="v">${esc(compact(m.amount))}</span><button class="linkbtn" type="button" data-counmark="${esc(m.id)}">Undo</button></div>`).join('')}</div>` : '<p class="muted small" style="margin:0">None marked in these dates.</p>'}
    ${sug.length ? `<div class="small" style="font-weight:600">Worth a check</div><div class="co-sug">${sug.slice(0, 5).map((x) => CO.open === x.d ? form(x.d, x.amount, x.why) : `<div class="co-row"><span><b>${esc(weekday(x.d))} ${esc(shortDate(x.d))}</b> <span class="muted small">${esc(x.why)}</span></span><button class="btn ghost small-btn" type="button" data-coopen="${esc(x.d)}">Client order?</button></div>`).join('')}</div>` : ''}
    <p class="small muted" style="margin:0">${esc(CO.msg || 'Brand sales keeps Metabase\'s own totals. Marks are saved for the team.')}</p>
  </section>`;
}
document.addEventListener('click', async (e) => {
  const v = $('overviewView');
  if (!v || !v.contains(e.target)) return;
  const o = e.target.closest('[data-coopen]');
  if (o) { CO.open = o.dataset.coopen; window.renderOverview(); return; }
  if (e.target.closest('[data-coclose]')) { CO.open = null; window.renderOverview(); return; }
  const u = e.target.closest('[data-counmark]');
  if (u) { CO.data.marks = CO.data.marks.filter((m) => m.id !== u.dataset.counmark); await coSave(); window.renderOverview(); }
});
document.addEventListener('change', (e) => {
  if (!e.target.matches || !e.target.matches('[data-coon]')) return;
  CO.on = e.target.checked;
  try { localStorage.setItem('client-orders-on', CO.on ? '1' : '0'); } catch (er) { /* storage unavailable */ }
  window.renderOverview();
});
document.addEventListener('submit', async (e) => {
  const f = e.target.closest && e.target.closest('[data-coform]');
  if (!f) return;
  e.preventDefault();
  const amount = Math.round(Number(f.amount.value)), orders = Math.max(1, Math.round(Number(f.orders.value) || 1));
  if (!(amount > 0)) return;
  CO.data.marks.push({ id: 'c' + Date.now().toString(36), d: f.dataset.coform, amount, orders, note: String(f.note.value || '').slice(0, 80), added: new Date().toISOString().slice(0, 10) });
  CO.open = null;
  await coSave();
  window.renderOverview();
});

// ---------- month pacing ----------
function pacingTile() {
  const last = rpLastSalesDay(), part = String(SL.data.daily_pulled_at || '').slice(0, 10) === last;
  const end = part ? addDays(last, -1) : last, mk = end.slice(0, 7), first = mk + '-01';
  const dim = new Date(Date.UTC(+mk.slice(0, 4), +mk.slice(5), 0)).getUTCDate(), done = +end.slice(8), left = dim - done;
  const cur = rpBrand(first, end);
  const lm = addDays(first, -1).slice(0, 7), lmDim = new Date(Date.UTC(+lm.slice(0, 4), +lm.slice(5), 0)).getUTCDate();
  const lmSame = rpBrand(lm + '-01', `${lm}-${String(Math.min(done, lmDim)).padStart(2, '0')}`), lmAll = rpBrand(lm + '-01', `${lm}-${String(lmDim).padStart(2, '0')}`);
  const ly = rpBrand(`${+mk.slice(0, 4) - 1}${mk.slice(4)}-01`, `${+mk.slice(0, 4) - 1}${end.slice(4)}`);
  // A typical day: the average of the last 28 days with big days capped, so 1 huge day does not inflate the estimate.
  const recent = rpBrand(addDays(end, -27), end), vals = recent.days.filter((r) => r.x && r.x.sales !== null).map((r) => r.x.sales);
  const cap = ovCap(vals), typical = vals.length ? vals.reduce((t, v) => t + (cap ? Math.min(v, cap.cap) : v), 0) / vals.length : null;
  const proj = cur.sales !== null && typical !== null ? cur.sales + typical * left : null;
  const spend7 = rpBrand(addDays(end, -6), end).spend / 7, projSpend = cur.spend + spend7 * left;
  const pct = (a, b) => (a !== null && b ? `${a >= b ? '▲' : '▼'} ${Math.abs((a / b - 1) * 100).toFixed(0)}%` : 'Not available');
  const bar = proj && lmAll.sales ? Math.min(100, cur.sales / Math.max(proj, lmAll.sales) * 100) : 0;
  return `<section class="tile c-4" aria-label="Month pacing">
    <div class="tile-head"><div><h2>${esc(MONTHS[+mk.slice(5) - 1])} so far</h2><div class="sub">1 to ${done} ${esc(MONTHS[+mk.slice(5) - 1])}, ${left} day${left === 1 ? '' : 's'} to go</div></div></div>
    <div class="big-num">${cur.sales !== null ? esc(compact(cur.sales)) : 'Not available'}</div>
    <div class="meter"><div class="bar"><i style="width:${bar.toFixed(1)}%;background:var(--gold)"></i></div></div>
    <div class="pace-grid">
      <div><span>Same days last month</span><b>${lmSame.sales !== null ? esc(compact(lmSame.sales)) : 'Not available'}</b><em>${pct(cur.sales, lmSame.sales)}</em></div>
      <div><span>Same days last year</span><b>${ly.covered ? esc(compact(ly.sales)) : 'Not available'}</b><em>${ly.covered ? pct(cur.sales, ly.sales) : 'Data starts Mar 2026'}</em></div>
      <div><span>Month end at this pace</span><b>${proj !== null ? esc(compact(proj)) : 'Not available'}</b><em>Last month ${lmAll.sales !== null ? esc(compact(lmAll.sales)) : '–'}</em></div>
      <div><span>Meta spend by month end</span><b>${esc(compact(projSpend))}</b><em>${esc(compact(cur.spend))} so far</em></div>
    </div>
    <p class="small muted" style="margin:0">Pace uses a typical day from the last 28 days, with big days capped${CO.on && CO.data.marks.length ? ' and client orders left out' : ''}.</p>
  </section>`;
}

// ---------- brand alerts ----------
// Website problems ads cannot show: a very low day, no orders, fewer visits, fewer add to carts, refunds.
function brandAlerts(dayArg) {
  if (!SL.data) return [];
  const last = rpLastSalesDay(), part = String(SL.data.daily_pulled_at || '').slice(0, 10) === last;
  const d = dayArg && dayArg <= last ? dayArg : part ? addDays(last, -1) : last;
  const out = [], wd = weekday(d), same = [];
  for (let i = 1; i <= 8; i++) { const x = rpDay(addDays(d, -7 * i)); if (x && x.sales !== null) same.push(x.sales); }
  const x = rpDay(d);
  const med = same.length >= 4 ? same.slice().sort((a, b) => a - b)[Math.floor(same.length / 2)] : null;
  if (x && x.orders === 0) out.push({ sev: 3, text: `No website orders on ${wd} ${shortDate(d)}. Check the site, checkout and payments.` });
  else if (x && x.sales !== null && med && x.sales < med * 0.4) out.push({ sev: 2, text: `Website sales on ${wd} ${shortDate(d)} were ${compact(x.sales)}, ${Math.round((1 - x.sales / med) * 100)}% below a normal ${wd} (${compact(med)}).` });
  const ga = gaMap(), g = ga[d], gs = [];
  for (let i = 1; i <= 4; i++) { const v = ga[addDays(d, -7 * i)]; if (v && v.visits) gs.push(v); }
  if (g && g.visits && gs.length >= 3) {
    const mv = gs.map((v) => v.visits).sort((a, b) => a - b)[Math.floor(gs.length / 2)];
    const wk = (e) => { let t = 0; for (let i = 0; i < 7; i++) { const v = ga[addDays(e, -i)]; if (!v || !v.visits) return null; t += v.visits; } return t; };
    const now7 = wk(d), then7 = wk(addDays(d, -28));
    if (now7 && then7 && now7 < then7 * 0.75) out.push({ sev: 2, text: `Site visits are falling: ${fmt(now7, 'int')} in the last 7 days, ${Math.round((1 - now7 / then7) * 100)}% fewer than 4 weeks before. Check traffic sources, ad reach and tracking.` });
    else if (g.visits < mv * 0.6) out.push({ sev: 2, text: `Site visits on ${wd} were ${fmt(g.visits, 'int')}, ${Math.round((1 - g.visits / mv) * 100)}% below a normal ${wd}. Check tracking and traffic.` });
    const rate = (v) => (v.visits && v.carts !== null && v.carts !== undefined ? v.carts / v.visits : null);
    const mr = gs.map(rate).filter((v) => v !== null).sort((a, b) => a - b);
    if (rate(g) !== null && mr.length >= 3 && rate(g) < mr[Math.floor(mr.length / 2)] * 0.6) out.push({ sev: 2, text: `Add to cart rate on ${wd} was ${(rate(g) * 100).toFixed(1)}%, well under the usual ${(mr[Math.floor(mr.length / 2)] * 100).toFixed(1)}%. Check product pages, prices and stock.` });
  }
  const week = (end) => { let t = 0, n = 0; for (let i = 0; i < 7; i++) { const y = rpDay(addDays(end, -i)); if (y && y.refund !== null && y.refund !== undefined) { t += y.refund; n++; } } return n ? t : null; };
  const rw = week(d), past = [];
  for (let i = 1; i <= 8; i++) { const v = week(addDays(d, -7 * i)); if (v !== null) past.push(v); }
  const pm = past.length >= 4 ? past.slice().sort((a, b) => a - b)[Math.floor(past.length / 2)] : null;
  if (rw !== null && pm && rw > pm * 2 && rw > 50000) out.push({ sev: 2, text: `Refunds in the last 7 days are ${compact(rw)}, over 2 times a normal week (${compact(pm)}).` });
  if (x && x.sales !== null && med && x.sales > med * 3.5 && !coMarks(d).length) out.push({ sev: 1, text: `Big day on ${wd} ${shortDate(d)}: ${compact(x.sales)}. If 1 client made a large order, mark it on the Overview.` });
  return out;
}
function brandAlertsTile() {
  const list = brandAlerts();
  const last = rpLastSalesDay(), part = String(SL.data.daily_pulled_at || '').slice(0, 10) === last, d = part ? addDays(last, -1) : last;
  return `<section class="tile darklist c-4" aria-label="Brand alerts">
    <div class="tile-head"><h2>Brand alerts</h2><span class="count">${list.length}</span></div>
    <div class="sub" style="color:inherit;opacity:.75;font-size:12px">${esc(weekday(d))} ${esc(shortDate(d))}, the last full day. Compared with the same weekday in past weeks.</div>
    ${list.length ? list.map((a) => `<div class="dl-row"><span class="dot ${a.sev >= 3 ? 'down' : a.sev === 2 ? 'mix' : 'up'}"></span><span style="min-width:0"><div class="t" style="white-space:normal">${esc(a.text)}</div></span></div>`).join('') : '<p class="small" style="margin:0;opacity:.8">Nothing unusual. Sales, visits, add to carts and refunds look normal.</p>'}
  </section>`;
}

// ---------- new vs repeat buyers ----------
function buyersTile() {
  return `<section class="tile c-4" aria-label="New and repeat buyers">
    <div class="tile-head"><div><h2>New vs repeat buyers</h2><div class="sub">Do ads bring new people, or the same buyers again?</div></div></div>
    <div class="na-box"><b>Not available yet</b><span>Metabase dashboard 6 has no customer card, and this login cannot read the orders table.</span></div>
    <p class="small" style="margin:0">Ask the Metabase admin for 1 card on dashboard 6: <b>orders by day, split into first order and repeat order</b> (count and sales, no names). It shows here after the next pull.</p>
  </section>`;
}

// ---------- ad-to-sale delay ----------
// Jewellery buyers often see an ad 1 to 2 weeks before they buy. This compares week-on-week changes in
// Meta spend with week-on-week changes in website sales some days later. Trends cancel out; what is left
// is whether a spend push is followed by a sales push, and how many days later.
function lagData(end) {
  const md = metaDayMap(), N = 150, start = addDays(end, -N + 1), days = [];
  for (let i = 0; i < N; i++) days.push(addDays(start, i));
  const sales = days.map((d) => { const x = rpDay(d); return x && x.sales !== null ? x.sales : null; });
  const cap = ovCap(sales), s = sales.map((v) => (v === null || !cap ? v : Math.min(v, cap.cap)));
  const sp = days.map((d) => (md[d] ? md[d].spend : null));
  const roll = (a, i) => { let t = 0; for (let k = 0; k < 7; k++) { const v = a[i - k]; if (v === null || v === undefined) return null; t += v; } return t; };
  const s7 = days.map((_, i) => (i >= 6 ? roll(s, i) : null)), p7 = days.map((_, i) => (i >= 6 ? roll(sp, i) : null));
  // Remove the slow trend: each 7-day total vs the average around it (42 days centred).
  const detr = (a) => a.map((v, i) => {
    if (v === null) return null;
    const w = a.slice(Math.max(0, i - 21), i + 22).filter((x) => x !== null);
    return w.length >= 34 ? v / (w.reduce((t, x) => t + x, 0) / w.length) - 1 : null;
  });
  const ds = detr(s7), dp = detr(p7);
  const corr = (L) => {
    const xs = [], ys = [];
    for (let i = L; i < N; i++) if (ds[i] !== null && dp[i - L] !== null) { xs.push(dp[i - L]); ys.push(ds[i]); }
    if (xs.length < 30) return null;
    const mx = xs.reduce((a, b) => a + b, 0) / xs.length, my = ys.reduce((a, b) => a + b, 0) / ys.length;
    let sxy = 0, sxx = 0, syy = 0;
    for (let k = 0; k < xs.length; k++) { sxy += (xs[k] - mx) * (ys[k] - my); sxx += (xs[k] - mx) ** 2; syy += (ys[k] - my) ** 2; }
    return sxx && syy ? { r: sxy / Math.sqrt(sxx * syy), n: xs.length } : null;
  };
  const lags = [];
  for (let L = 0; L <= 28; L++) lags.push({ L, ...(corr(L) || { r: null, n: 0 }) });
  const best = lags.filter((x) => x.r !== null).sort((a, b) => b.r - a.r)[0] || null;
  const band = lags.filter((x) => x.L >= 7 && x.L <= 14 && x.r !== null), bandAvg = band.length ? band.reduce((t, x) => t + x.r, 0) / band.length : null;
  // Sales per ₹1 counting the spend from 7 to 14 days earlier (the buying window the team sees).
  const win = (a, b) => { let t = 0; for (let i = a; i <= b; i++) { const v = sp[i]; if (v === null) return null; t += v; } return t; };
  let perLag = null, perSame = null;
  const i1 = N - 1, i0 = N - 28, sSum = s.slice(i0, i1 + 1).reduce((t, v) => t + (v || 0), 0);
  const sameSpend = win(i0, i1), lagSpend = (() => { let t = 0; for (let i = i0; i <= i1; i++) { let w = 0; for (let k = 7; k <= 14; k++) { const v = sp[i - k]; if (v === null || v === undefined) return null; w += v; } t += w / 8; } return t; })();
  if (sameSpend) perSame = sSum / sameSpend;
  if (lagSpend) perLag = sSum / lagSpend;
  return { lags, best, bandAvg, perLag, perSame, start, end };
}
function lagTile() {
  const last = rpLastSalesDay(), part = String(SL.data.daily_pulled_at || '').slice(0, 10) === last;
  const L = lagData(part ? addDays(last, -1) : last);
  const W = 640, H = 200, Lp = 38, R = 8, T = 16, Bt = 34, n = L.lags.length;
  const vals = L.lags.map((x) => x.r).filter((v) => v !== null), top = Math.max(0.2, ...vals.map(Math.abs));
  const max = Math.ceil(top * 10) / 10, y0 = T + (H - T - Bt) / 2, y = (v) => y0 - (H - T - Bt) / 2 * (v / max);
  const slot = (W - Lp - R) / n, bw = Math.max(4, slot * 0.66);
  const band = `<rect x="${(Lp + slot * 7).toFixed(1)}" y="${T}" width="${(slot * 8).toFixed(1)}" height="${H - T - Bt}" style="fill:var(--gold-soft)"/><text x="${(Lp + slot * 11).toFixed(1)}" y="${T + 12}" text-anchor="middle" style="fill:var(--gold-deep);font-size:11px;font-weight:600">7 to 14 days</text>`;
  const grid = [-max, 0, max].map((v) => `<line x1="${Lp}" x2="${W - R}" y1="${y(v).toFixed(1)}" y2="${y(v).toFixed(1)}" style="stroke:var(--line)"${v ? ' stroke-dasharray="3 4"' : ''}/><text x="${Lp - 6}" y="${(y(v) + 4).toFixed(1)}" text-anchor="end" style="fill:var(--muted);font-size:11px">${v.toFixed(1)}</text>`).join('');
  const bars = L.lags.map((x, i) => {
    const cx = Lp + slot * i + slot / 2, isBest = L.best && x.L === L.best.L;
    const tip = esc(`Spend ${x.L} day${x.L === 1 ? '' : 's'} earlier|Match|${x.r !== null ? x.r.toFixed(2) : 'Not available'}|Weeks compared|${x.n}`);
    const bar = x.r === null ? '' : `<rect x="${(cx - bw / 2).toFixed(1)}" y="${Math.min(y(x.r), y0).toFixed(1)}" width="${bw.toFixed(1)}" height="${Math.abs(y(x.r) - y0).toFixed(1)}" rx="2" style="fill:${isBest ? 'var(--gold)' : x.r > 0 ? '#bdb8ad' : '#e3dfd6'}"/>`;
    return `<g data-tip="${tip}"><rect x="${(cx - slot / 2).toFixed(1)}" y="${T}" width="${slot.toFixed(1)}" height="${H - T - Bt}" style="fill:transparent"/>${bar}${x.L % 7 === 0 ? `<text x="${cx}" y="${H - Bt + 16}" text-anchor="middle" style="fill:var(--muted);font-size:11px">${x.L}d</text>` : ''}</g>`;
  }).join('');
  const short = L.best && L.best.L <= 3;
  const msg = !L.best ? 'Not enough days with both sales and spend to compare.'
    : `The closest match is spend from <b>${L.best.L} day${L.best.L === 1 ? '' : 's'} earlier</b> (match ${L.best.r.toFixed(2)}).${L.bandAvg !== null ? ` The 7 to 14 day window averages ${L.bandAvg.toFixed(2)}.` : ''}${short ? ' Sales rise in the same weeks spend rises. Part of that is timing: budgets go up in sales and festivals, when people already buy. So this cannot confirm or rule out a 7 to 14 day delay.' : ''}${L.perLag && L.perSame ? ` Last 28 days: ₹${L.perSame.toFixed(1)} of sales per ₹1 spent the same days, ₹${L.perLag.toFixed(1)} per ₹1 spent 7 to 14 days before.` : ''}`;
  return `<section class="tile c-8" aria-label="Ad to sale delay">
    <div class="tile-head"><div><h2>How long ads take to turn into sales</h2><div class="sub">Meta spend above or below its trend vs website sales above or below trend, N days later. Last 150 days, big days capped.</div></div></div>
    <svg viewBox="0 0 ${W} ${H}" style="width:100%;height:auto;display:block" role="img" aria-label="Match between spend and later sales by days of delay">${band}${grid}${bars}<text x="${W - R}" y="${H - 4}" text-anchor="end" style="fill:var(--faint);font-size:10.5px">days between spend and sales</text></svg>
    <p class="ov-say">${msg}</p>
    <p class="small muted" style="margin:0">A match near 1 means spend above trend is followed by sales above trend that many days later. To measure the real delay, use the days to purchase report in Google Analytics, or a 2-week pause test in 1 region. Until then, judge ads on 7 to 14 day windows, not on the same day.</p>
  </section>`;
}

// ---------- weekly budget plan ----------
// Keeps the weekly total the same and tilts it gently toward the days that bring more sales per ₹1.
// With a 7 to 14 day delay the day you spend is not the day people buy, so the tilt is capped at ±15%.
function budgetPlanTile(B) {
  const dow = ovWeekdays(B, 'cap'), ok = dow.filter((x) => x.per !== null && x.n >= 4);
  const last = rpLastSalesDay(), md = metaDayMap();
  let t14 = 0, n14 = 0;
  for (let i = 0; i < 14; i++) { const m = md[addDays(last, -i)]; if (m) { t14 += m.spend; n14++; } }
  const base = n14 ? t14 / n14 : null;
  if (!base || ok.length < 7) return `<section class="tile c-4" aria-label="Weekly budget plan"><div class="tile-head"><div><h2>Weekly budget plan</h2></div></div><p class="muted small">Needs 4 or more of each weekday with sales and spend. Pick 60 or 90 days.</p></section>`;
  const avg = ok.reduce((t, x) => t + x.sales, 0) / ok.reduce((t, x) => t + x.spend, 0);
  // Half-way toward the weekday's own return, then capped at ±15%.
  const raw = dow.map((x) => Math.max(0.85, Math.min(1.15, 1 + ((x.per / avg) - 1) * 0.5)));
  const k = 7 / raw.reduce((t, v) => t + v, 0), w = raw.map((v) => v * k);
  const rows = dow.map((x, i) => ({ key: x.key, amt: Math.round(base * w[i] / 100) * 100, ch: w[i] - 1 }));
  const text = ['Meta daily budget by weekday (weekly total unchanged):', ...rows.map((r) => `${r.key}: ${compact(r.amt)} (${r.ch >= 0 ? '+' : ''}${Math.round(r.ch * 100)}%)`)].join('\n');
  return `<section class="tile c-4" aria-label="Weekly budget plan">
    <div class="tile-head"><div><h2>Weekly budget plan</h2><div class="sub">Same weekly total (${esc(compact(base * 7))}), a gentle tilt by weekday</div></div>${copyBtn(text)}</div>
    <div>${rows.map((r) => `<div class="mixrow"><i style="background:${r.ch > 0.02 ? 'var(--good)' : r.ch < -0.02 ? 'var(--bad)' : 'var(--line)'}"></i><span>${esc(r.key)}</span><span class="v">${esc(compact(r.amt))}</span><span class="r">${r.ch >= 0 ? '+' : ''}${Math.round(r.ch * 100)}%</span></div>`).join('')}</div>
    <p class="small muted" style="margin:0">From the last 14 days of spend and the weekday return above (big days capped). Buyers take 1 to 2 weeks, so run it for 2 weeks and judge it on the 7 to 14 day window, not day by day. Use ad set dayparting or budget rules; this page cannot change budgets.</p>
  </section>`;
}

coBoot().then(() => { if (typeof state !== 'undefined' && ['overview', 'report', 'buyer'].includes(state.tab) && typeof renderTab === 'function') renderTab(); });
