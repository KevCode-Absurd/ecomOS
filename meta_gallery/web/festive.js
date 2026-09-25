'use strict';
// Festive plan: this year's festival windows, what the same windows did last year (website sales and Meta),
// a day budget for each window, last year's festive winners to bring back, the festive creative pack,
// best sellers to feature, and what rivals run right now.
// Data: festive.json (dates), creativepack.json, compwatch.json, catalog.json; Meta and website sales already
// loaded by the page. Uses: DATA, ENGINE, SL, loadSales, rpDay, addDays, shortDate, compact, esc, $, copyBtn,
// thumbHtml, isSaleAd, bdLastFull, noAdSellers (testlab.js).

const FS = { files: null, show: 'festive' };
async function fsBoot() {
  if (FS.files) return;
  const get = async (f) => { try { const r = await fetch(f); return r.ok ? await r.json() : null; } catch (e) { return null; } };
  const [fe, cp, cw, cat] = await Promise.all(['festive.json', 'creativepack.json', 'compwatch.json', 'catalog.json'].map(get));
  FS.files = { fe: fe && Array.isArray(fe.windows) ? fe : null, cp: cp && Array.isArray(cp.items) ? cp : null, cw: cw && Array.isArray(cw.brands) ? cw : null, cat: cat && Array.isArray(cat.products) ? cat : null };
}
const fsX = (v) => (v === null || v === undefined || !Number.isFinite(v) ? 'no sales' : v.toFixed(2) + 'x');
const fsDays = (a, b) => { const out = []; for (let d = a; d <= b; d = addDays(d, 1)) out.push(d); return out; };

// Whole account per day, every ad (sale ads included: festive sales were real sales).
function fsAccount() {
  if (FS.acc) return FS.acc;
  const out = {};
  for (const rows of Object.values(DATA.daily)) for (const r of rows) {
    const o = out[r[0]] || (out[r[0]] = { spend: 0, value: 0, impr: 0, purch: 0 });
    o.spend += r[1] || 0; o.value += r[3] || 0; o.impr += r[4] || 0; o.purch += r[2] || 0;
  }
  FS.acc = out;
  return out;
}
function fsStats(a, b) {
  const acc = fsAccount(), first = DATA.meta.window.since;
  let sales = 0, sn = 0, orders = 0, spend = 0, value = 0, impr = 0, n = 0;
  for (const d of fsDays(a < first ? first : a, b)) {
    n += 1;
    const x = SL.data ? rpDay(d) : null;
    if (x && x.sales !== null && x.sales !== undefined) { sales += x.sales; sn += 1; orders += x.orders || 0; }
    const o = acc[ENGINE.idx(d)];
    if (o) { spend += o.spend; value += o.value; impr += o.impr; }
  }
  return { n, sales: sn ? sales / sn : null, orders: sn ? orders / sn : null, spend: n ? spend / n : 0, roas: spend ? value / spend : null, cpm: impr ? spend / impr * 1000 : null, per: spend && sn ? (sales / sn) / (spend / n) : null, covered: sn };
}
// A normal day last year: the median day outside every festive window.
function fsNormal(fe) {
  const acc = fsAccount(), inWin = new Set(fe.windows.flatMap((w) => fsDays(w.ly[0], w.ly[1])));
  const end = bdLastFull(), start = addDays(end, -364), sales = [], spend = [], cpm = [];
  for (const d of fsDays(start, end)) {
    if (inWin.has(d)) continue;
    const x = SL.data ? rpDay(d) : null, o = acc[ENGINE.idx(d)];
    if (x && x.sales !== null && x.sales !== undefined) sales.push(x.sales);
    if (o && o.spend) { spend.push(o.spend); if (o.impr) cpm.push(o.spend / o.impr * 1000); }
  }
  const med = (l) => { if (!l.length) return null; const s = l.slice().sort((p, q) => p - q); return s[Math.floor(s.length / 2)]; };
  const s = med(sales), sp = med(spend);
  return { sales: s, spend: sp, cpm: med(cpm), per: s && sp ? s / sp : null };
}
function fsPlan(fe) {
  const N = fsNormal(fe), end = bdLastFull();
  const acc = fsAccount();
  let now = 0;
  for (let i = 0; i < 14; i++) { const o = acc[ENGINE.idx(addDays(end, -i))]; now += o ? o.spend : 0; }
  now /= 14;
  const rows = fe.windows.map((w) => {
    const s = fsStats(w.ly[0], w.ly[1]);
    const lift = s.sales && N.sales ? s.sales / N.sales : null, eff = s.per && N.per ? s.per / N.per : null, cost = s.cpm && N.cpm ? s.cpm / N.cpm : null;
    // Budget: follow what each rupee returned last year, damped, and hold back where reach cost 2.5 times normal or more.
    let mult = eff === null ? 1 : Math.max(0.8, Math.min(1.6, 1 + (eff - 1) * 0.6));
    if (lift !== null && lift < 0.9) mult = Math.min(mult, 0.9);
    if (cost !== null && cost >= 2.5) mult = Math.min(mult, 1.3);
    mult = Math.round(mult * 20) / 20;
    return { ...w, s, lift, eff, cost, mult, day: Math.round(now * mult / 500) * 500 };
  });
  return { N, now, rows };
}
function fsLessons(P) {
  const L = [], r = (k) => P.rows.find((x) => x.key === k);
  const best = P.rows.filter((x) => x.lift !== null).sort((a, b) => b.lift - a.lift)[0];
  if (best) L.push(`Last year the biggest sales came in "${best.name}": ${compact(best.s.sales)} a day, ${best.lift.toFixed(1)} times a normal day.`);
  const dw = r('diwali'), ru = r('runup'), af = r('after');
  if (dw && ru && ru.lift && dw.lift && ru.lift > dw.lift) L.push('Sales peaked 2 to 3 weeks before Diwali, not in Diwali week. Push hardest from Dussehra to Karwa Chauth.');
  if (dw && dw.cost) L.push(`Reach cost ${dw.cost.toFixed(1)} times normal in the Dhanteras and Diwali window (${compact(dw.s.cpm)} per 1,000 views). Book creative early and lean on proven ads that week.`);
  if (af && af.lift && af.lift < 0.95) L.push(`Sales fell to ${compact(af.s.sales)} a day after Diwali. Cut budget the day after Bhai Dooj.`);
  const bf = r('bfcm');
  if (bf && bf.s.roas && bf.cost && bf.cost < 0.9) L.push(`Black Friday week was cheap to reach (${compact(bf.s.cpm)} per 1,000 views) and returned ${fsX(bf.s.roas)} on Meta. Plan a second push there.`);
  return L;
}
function fsWinners(fe) {
  const a = ENGINE.idx(fe.windows[0].ly[0] < DATA.meta.window.since ? DATA.meta.window.since : fe.windows[0].ly[0]), b = ENGINE.idx(fe.windows.find((w) => w.key === 'diwali').ly[1]);
  const rows = [];
  for (const [id, ad] of Object.entries(DATA.ads)) {
    const m = ENGINE.sums(id, a, b);
    if ((m.purchases || 0) < 5 || m.roas === null || ad.creative.type === 'catalog_dynamic') continue;
    rows.push({ id, ad, m, sale: isSaleAd(ad) });
  }
  return rows.sort((p, q) => (q.m.purchase_value || 0) - (p.m.purchase_value || 0)).slice(0, REC_CAP);
}
function fsCard(it) {
  const text = [`${it.headline}`, it.text, it.products.map((p) => `${p.name}${p.url ? ' ' + p.url : ''}`).join('\n'), `File: ${it.file} (${it.size})`].join('\n');
  return `<figure class="fs-cr"><img loading="lazy" src="${esc(it.preview)}" alt="${esc(it.headline)}">
    <figcaption><b>${esc(it.window || it.for || '')}</b><span>${esc(it.text)}</span><span class="act-btns">${copyBtn(text)}</span></figcaption></figure>`;
}
window.renderFestive = async function renderFestive() {
  const v = $('festiveView');
  if (!v || !VIEW) return;
  if (!FS.files) v.innerHTML = '<p class="muted">Loading the festive plan…</p>';
  await fsBoot();
  if (!SL.data && !SL.err) await loadSales();
  const { fe, cp, cw, cat } = FS.files;
  if (!fe) { v.innerHTML = '<p class="muted">Festival dates are not available yet.</p>'; return; }
  const today = bdLastFull();
  let P = null;
  try { P = SL.data ? fsPlan(fe) : null; } catch (e) { console.error(e); P = null; }
  const lessons = P ? fsLessons(P) : [];
  const next = fe.windows.find((w) => w.ty[1] >= today);
  const daysTo = next ? Math.max(0, Math.round((new Date(next.ty[0]) - new Date(today)) / 864e5)) : null;
  const planText = P ? ['Festive budget plan (Meta, per day):', `Prep ${shortDate(fe.prep[0])} to ${shortDate(fe.prep[1])}: ${compact(Math.round(P.now * 1.1 / 500) * 500)}. Test the festive designs at 10 to 15% of budget.`,
    ...P.rows.map((r) => `${r.name}, ${shortDate(r.ty[0])} to ${shortDate(r.ty[1])}: ${compact(r.day)} a day (${r.mult >= 1 ? '+' : ''}${Math.round((r.mult - 1) * 100)}% on today).`), '', ...lessons].join('\n') : '';
  const winners = fsWinners(fe);
  const pack = cp ? cp.items.filter((i) => i.group === 'festive') : [];
  let noAd = [];
  try { noAd = SL.data && typeof noAdSellers === 'function' ? noAdSellers().slice(0, 8) : []; } catch (e) { noAd = []; }
  const top = cat ? cat.products.slice(0, 12) : [];
  const inPack = new Set(cp ? cp.items.flatMap((i) => i.products.map((p) => p.code)) : []);
  v.innerHTML = `<div class="fs">
    <div class="mv-head"><div><h2>Festive plan</h2><p class="lead">Navratri to Diwali, then Black Friday and the wedding season. Built from last year's website sales and Meta results for the same windows.</p></div>
      ${planText ? copyBtn(planText) : ''}</div>
    ${next ? `<div class="fs-next"><b>${daysTo === 0 ? 'Now' : `${daysTo} days`}</b> to ${esc(next.name)} (${esc(shortDate(next.ty[0]))}). Prep window: ${esc(shortDate(fe.prep[0]))} to ${esc(shortDate(fe.prep[1]))}.</div>` : ''}
    <div class="fs-cal">${fe.windows.map((w) => `<div class="fs-win${next && w.key === next.key ? ' on' : ''}"><b>${esc(w.name)}</b><span>${esc(shortDate(w.ty[0]))} to ${esc(shortDate(w.ty[1]))}</span>${Object.entries(w.days || {}).map(([d, n]) => `<em>${esc(shortDate(d))}: ${esc(n)}</em>`).join('')}</div>`).join('')}</div>
    ${lessons.length ? `<section class="panel-box hl-sec"><h3>What last year says</h3><ul>${lessons.map((l) => `<li>${esc(l)}</li>`).join('')}</ul></section>` : ''}
    ${P ? `<section class="panel-box hl-sec"><h3>Budget plan and last year's numbers</h3><div class="scroll"><table class="bd-table">
      <tr><th>Window</th><th class="n">Sales a day, last year</th><th class="n">vs normal</th><th class="n">Ad spend a day</th><th class="n">Per 1,000 views</th><th class="n">Meta ROAS</th><th class="n">Budget a day, this year</th></tr>
      <tr class="bd-total"><td>Normal day last year</td><td class="n">${P.N.sales ? compact(P.N.sales) : 'unavailable'}</td><td class="n">1.0x</td><td class="n">${P.N.spend ? compact(P.N.spend) : '–'}</td><td class="n">${P.N.cpm ? compact(P.N.cpm) : '–'}</td><td class="n">–</td><td class="n">Today ${compact(P.now)}</td></tr>
      ${P.rows.map((r) => `<tr><td><b>${esc(r.name)}</b><br><span class="small">${esc(shortDate(r.ty[0]))} to ${esc(shortDate(r.ty[1]))}</span><br><span class="muted small">last year ${esc(shortDate(r.ly[0]))} to ${esc(shortDate(r.ly[1]))}${r.s.covered < r.s.n ? `, ${r.s.covered} of ${r.s.n} days of sales` : ''}</span></td>
        <td class="n">${r.s.sales !== null ? compact(r.s.sales) : 'unavailable'}</td><td class="n">${r.lift !== null ? r.lift.toFixed(1) + 'x' : '–'}</td>
        <td class="n">${compact(r.s.spend)}</td><td class="n${r.cost >= 2.5 ? ' bad' : ''}">${r.s.cpm ? compact(r.s.cpm) : '–'}</td><td class="n">${fsX(r.s.roas)}</td>
        <td class="n"><b>${compact(r.day)}</b><br><span class="muted small">${r.mult >= 1 ? '+' : ''}${Math.round((r.mult - 1) * 100)}%</span></td></tr>`).join('')}
    </table></div><p class="small muted">Budget follows how much website sales each ₹1 of ads brought in last year, damped so no window jumps more than 60%, and capped at +30% where reach cost 2.5 times normal or more. Raise in steps of 15 to 20% every 2 to 3 days, not in one jump.</p></section>` : '<p class="muted">Website sales are needed for the plan.</p>'}
    ${winners.length ? `<section class="panel-box hl-sec"><h3>Last year's festive winners</h3><p class="small">From Navratri to Bhai Dooj last year, 5 or more sales each. Bring back the everyday ones as new ads; sale ads only if you run the same offer.</p>
      <div class="scroll"><table class="bd-table"><tr><th>Ad</th><th>Format</th><th class="n">Spend</th><th class="n">Sales</th><th class="n">ROAS</th><th>Now</th></tr>
      ${winners.map((w) => `<tr><td><button class="linkbtn" type="button" data-open="${esc(w.id)}">${esc(w.ad.name)}</button>${w.sale ? ' <span class="chip sale">Sale</span>' : ''}<br><span class="muted small">${esc(w.ad.campaign_name)}</span></td><td class="small">${esc(w.ad.creative.type_label || '')}</td><td class="n">${compact(w.m.spend)}</td><td class="n">${w.m.purchases}</td><td class="n">${fsX(w.m.roas)}</td><td class="small">${w.ad.effective_status === 'ACTIVE' ? 'Live' : 'Off'}</td></tr>`).join('')}</table></div></section>` : ''}
    ${pack.length ? `<section class="panel-box hl-sec"><div class="bd-head"><h3>Festive creative pack (${pack.length} designs)</h3></div>
      <p class="small">Made from Gehna's own product photos with the winning formula: designed graphic, a question or festive hook, and the trust strip. Full size files (1080 x 1350) are in the creative_pack folder. Check price and stock before launch.</p>
      <div class="fs-grid">${pack.map(fsCard).join('')}</div></section>` : ''}
    <section class="panel-box hl-sec"><h3>Pieces to feature</h3><div class="fs-two">
      <div><h4>Top sellers, last 12 months</h4><ol class="fs-list">${top.map((p) => `<li>${esc(p.name)} <span class="muted small">${esc(p.sold_12m)} sold · ₹${Number(p.price).toLocaleString('en-IN')}${inPack.has(p.code) ? ' · in the pack' : ''}</span></li>`).join('') || '<li class="muted">Catalog not loaded.</li>'}</ol></div>
      <div><h4>Selling well with no ad</h4>${noAd.length ? `<ol class="fs-list">${noAd.map((r) => `<li>${esc(r.name)} <span class="muted small">${r.n} sold in 3 months</span></li>`).join('')}</ol><p class="small muted">Next: brief ads for these after the festive pack. Check stock first.</p>` : '<p class="muted small">Needs website sales by product.</p>'}</div></div></section>
    ${cw ? `<section class="panel-box hl-sec"><div class="bd-head"><h3>What rivals run right now</h3><button class="linkbtn" type="button" data-goto="competitors">Competitors tab</button></div>
      <ul class="hl-find">${cw.gaps.slice(0, 4).map((g) => `<li><b>${esc(g.title)}.</b> ${esc(g.text)}</li>`).join('')}</ul></section>` : ''}
    <p class="small muted">Festival dates: ${fe.sources.map((u) => `<a href="${esc(u)}" target="_blank" rel="noopener">${esc(u.replace(/^https?:\/\/(www\.)?/, '').split('/')[0])}</a>`).join(', ')}. Last year's windows are matched to the same festivals.</p>
  </div>`;
};
document.addEventListener('click', (e) => {
  const v = $('festiveView');
  if (!v || !v.contains(e.target)) return;
  const o = e.target.closest('[data-open]');
  if (o && typeof openSide === 'function') { e.preventDefault(); openSide(o.dataset.open); return; }
  const g = e.target.closest('[data-goto]');
  if (g && typeof setTab === 'function') { setTab(g.dataset.goto); window.scrollTo(0, 0); }
});
