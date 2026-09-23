'use strict';
// Tests to run: ranked test briefs built from website sales (Metabase) and Meta ad data together.
// Also adds a website sales line to each action plan card and a sales block to the ad side panel.
// Uses sales.js helpers (loadSales, rangeMonth, metaRange, dayRows, adCat, adText, inAds, skuRollup) and studio.js.

const TL = { list: null, key: '' };
const r100 = (v) => Math.max(500, Math.round(v / 100) * 100);
const share = (a, b) => (b ? a / b : null);
const pc = (v) => (v === null || !Number.isFinite(v) ? '–' : Math.round(v * 100) + '%');

function tlWindow() {
  const days = dailyDays();
  if (!days.length) return null;
  const until = days[days.length - 1], since = addDays(until, -29) < days[0] ? days[0] : addDays(until, -29);
  return { since, until, all: days };
}
// How many ads mention a pattern in their name, headline or text (spend-weighted share too).
function adsMention(re) {
  let n = 0, spend = 0, total = 0;
  const [a, b] = ENGINE.resolveRange(VIEW.range.since, VIEW.range.until);
  for (const [id, ad] of Object.entries(DATA.ads)) {
    const c = ad.creative || {};
    const txt = [ad.name, c.headline, c.primary_text, c.name].join(' ');
    const sp = ENGINE.sums(id, a, b).spend || 0;
    total += sp;
    if (re.test(txt)) { n += 1; spend += sp; }
  }
  return { n, spendShare: share(spend, total) };
}
function pearson(xs, ys) {
  const n = xs.length;
  if (n < 10) return null;
  const mx = xs.reduce((t, v) => t + v, 0) / n, my = ys.reduce((t, v) => t + v, 0) / n;
  let sxy = 0, sxx = 0, syy = 0;
  for (let i = 0; i < n; i++) { sxy += (xs[i] - mx) * (ys[i] - my); sxx += (xs[i] - mx) ** 2; syy += (ys[i] - my) ** 2; }
  return sxx && syy ? sxy / Math.sqrt(sxx * syy) : null;
}
function bestImageAd(cat) {
  const ids = baseAds();
  const ok = (id) => VIEW.ads[id].view.metrics.roas !== null && VIEW.ads[id].view.metrics.purchases >= 1;
  const inCat = cat ? ids.filter((id) => ok(id) && adCat(ENGINE.c.ads[id] || DATA.ads[id]) === cat) : [];
  const pick = (l) => l.sort((x, y) => VIEW.ads[y].view.metrics.roas - VIEW.ads[x].view.metrics.roas)[0];
  return pick(inCat) || pick(ids.filter(ok)) || ids[0] || null;
}

// Build the ranked list. Each test: { id, kind, title, conf, score, why[], setup[], budget, win, stop, base, cat }
function buildTests() {
  const w = tlWindow();
  if (!w) return [];
  const mo = rangeMonth(w.since, w.until), meta = metaRange(w.since, w.until), rows = dayRows(w.since, w.until);
  const allRows = dayRows(w.all[0], w.all[w.all.length - 1]);
  const days = rows.length, dailySpend = meta.spend / Math.max(1, days);
  const testBudget = r100(Math.max(1000, dailySpend * 0.07));
  const out = [];

  // 1. Best sellers with no ad of their own.
  const keys = Object.keys(SL.data.months).sort().slice(-3);
  const sold90 = skuRollup(keys).filter((r) => r.metal === 'g' && inAds(r.name) === false).sort((a, b) => b.n - a.n || b.v - a.v);
  const top = sold90.slice(0, 3);
  if (top.length && top[0].n >= 3) {
    const t = top[0], cat = typeCat(t.name), avg = t.v / t.n;
    out.push({ id: 'sku-' + t.code, kind: 'Product', title: `Give "${t.name}" its own ad`, conf: t.n >= 6 ? 'Strong' : 'Medium', score: 90 + Math.min(10, t.n),
      why: [`Sold ${t.n} times in the last 3 months (${compact(t.v)}, about ${compact(avg)} each) with no ad naming it.`,
        top.length > 1 ? `Next in line: ${top.slice(1).map((r) => `${r.name} (${r.n} sold)`).join(', ')}.` : '',
        'People already buy it without ads, so demand is proven. Catalog ads may still show it, but no ad sells it on purpose.'].filter(Boolean),
      setup: [`Make 1 image ad of this piece in the layout of your best ${cat.toLowerCase()} ad. Use the site photo, the real price and 1 line of proof.`,
        'Put it in its own ad set with your best broad audience, so it gets its own budget.', 'Keep everything else the same.'],
      budget: `${money(testBudget)} a day for 7 days (${money(testBudget * 7)} in total).`,
      win: `Website sales of this piece go above ${Math.max(1, Math.round(t.n / 90 * 7 * 2))} in 7 days (twice its usual pace), or Meta ROAS beats ${roasTxt(VIEW.targets.roas)}.`,
      stop: `No sale of it by day 5 and ROAS under half of target.`, base: bestImageAd(cat), cat, product: t.name });
  }

  // 2. Budget follows ads, sales follow product: the most under-funded category.
  const cs = {}, catTot = { s: 0, a: 0 };
  for (const [, type, v] of mo.types) { const c = typeCat(type); cs[c] = (cs[c] || 0) + (v || 0); catTot.s += v || 0; }
  const tagged = CATS.reduce((t, c) => t + (meta.cat[c] || 0), 0);
  const gaps = CATS.filter((c) => c !== 'Other').map((c) => ({ c, s: share(cs[c] || 0, catTot.s), a: share(meta.cat[c] || 0, tagged) })).filter((g) => g.s !== null && g.a !== null);
  const under = gaps.filter((g) => g.s - g.a > 0.1).sort((x, y) => (y.s - y.a) - (x.s - x.a))[0];
  const over = gaps.filter((g) => g.a - g.s > 0.1).sort((x, y) => (y.a - y.s) - (x.a - x.s))[0];
  if (under) {
    out.push({ id: 'cat-' + under.c, kind: 'Budget', title: `Fund ${under.c.toLowerCase()}: ${pc(under.s)} of sales, ${pc(under.a)} of product ad spend`, conf: under.s - under.a > 0.2 ? 'Strong' : 'Medium', score: 80 + Math.round((under.s - under.a) * 40),
      why: [`Last 30 days: ${under.c} made ${compact(cs[under.c] || 0)} of website sales (${pc(under.s)}) but got ${compact(meta.cat[under.c] || 0)} of product ad spend (${pc(under.a)}).`,
        over ? `${over.c} got ${pc(over.a)} of product ad spend for ${pc(over.s)} of sales.` : '',
        'Ads are tagged by product from their names and copy. Catalog and mixed ads are left out.'].filter(Boolean),
      setup: [`Launch a ${under.c.toLowerCase()} ad set with your 2 or 3 best ${under.c.toLowerCase()} creatives.`, over ? `Fund it by moving the same amount out of ${over.c.toLowerCase()} ad sets, so total spend stays flat.` : 'Fund it with new budget.'],
      budget: `${money(testBudget * 2)} a day for 10 days.`,
      win: `${under.c} website sales in the 10 days beat the 10 days before by 20% or more, with total sales flat or up.`,
      stop: 'Total website sales drop 20% or more for 4 days in a row.', base: bestImageAd(under.c), cat: under.c });
  }

  if (!under && over) {
    const to = gaps.filter((g) => g.c !== over.c).sort((x, y) => (y.s - y.a) - (x.s - x.a))[0];
    out.push({ id: 'cat-over-' + over.c, kind: 'Budget', title: `${over.c} get ${pc(over.a)} of product ad spend for ${pc(over.s)} of sales`, conf: over.a - over.s > 0.15 ? 'Medium' : 'Early signal', score: 75 + Math.round((over.a - over.s) * 30),
      why: [`Last 30 days: ${over.c} got ${compact(meta.cat[over.c] || 0)} of product ad spend (${pc(over.a)}) and made ${compact(cs[over.c] || 0)} of website sales (${pc(over.s)}).`,
        to ? `${to.c} made ${pc(to.s)} of sales on ${pc(to.a)} of product ad spend.` : '',
        'Ads are tagged by product from their names and copy. Catalog and mixed ads are left out.'].filter(Boolean),
      setup: [`Move 20% of ${over.c.toLowerCase()} ad set budgets${to ? ` into your best ${to.c.toLowerCase()} ad set` : ''}.`, 'Keep total spend the same, and change nothing else.'],
      budget: `About ${money((meta.cat[over.c] || 0) / Math.max(1, days) * 0.2)} a day moved, for 10 days.`,
      win: `Total website sales flat or up, and ${to ? to.c.toLowerCase() : 'other'} sales up 15% vs the 10 days before.`,
      stop: `${over.c} website sales fall 30% or more while total sales fall too.`, base: to ? bestImageAd(to.c) : null, cat: to ? to.c : null });
  }

  // 3. Does Meta spend move website sales? A simple on/off pulse to find the real effect.
  const sp = allRows.filter((r) => r.spend !== null);
  const rr = pearson(sp.map((r) => r.spend), sp.map((r) => r.sales || 0));
  const lag = pearson(sp.slice(0, -1).map((r) => r.spend), sp.slice(1).map((r) => r.sales || 0));
  const claim = meta.valueSeen && mo.sales ? meta.value / mo.sales : null;
  const link = (v) => (v === null ? 'unknown' : Math.abs(v) < 0.2 ? 'weak' : Math.abs(v) < 0.45 ? 'moderate' : 'strong');
  out.push({ id: 'pulse', kind: 'Measurement', title: 'Find out how much of your sales Meta really drives', conf: 'Strong', score: 85,
    why: [`Meta claims ${claim !== null ? pc(claim) : 'an unknown share'} of website sales in the last 30 days.`,
      `Across ${sp.length} days, the link between daily Meta spend and same-day website sales is ${link(rr)}${rr !== null ? ` (r = ${rr.toFixed(2)})` : ''}, and with next-day sales it is ${link(lag)}${lag !== null ? ` (r = ${lag.toFixed(2)})` : ''}. ${rr !== null && Math.abs(rr) >= 0.45 ? 'Sales rise and fall with spend, but both also follow paydays and sale events, so this does not prove cause.' : 'With 3 to 5 orders a day, noise hides the effect.'}`,
      'Meta\'s own attribution cannot answer this. A planned on/off test can.'],
    setup: ['Pick 2 fixed weekdays, for example Tuesday and Wednesday.', 'For 4 weeks, cut all prospecting budgets by 50% on those days only. Keep retargeting on.', 'Compare website sales on those days with the same weekdays in the 4 weeks before.'],
    budget: `Saves about ${money(dailySpend * 0.5 * 8 * 0.7)} over 4 weeks. No new spend.`,
    win: 'If sales on cut days hold within 10%, part of your spend is buying sales that would happen anyway. Move it to new-customer tests.',
    stop: 'Stop early if cut-day sales fall 30% or more in the first 2 weeks. That proves Meta drives sales, which is also a result.', base: null });

  // 4. Weekday budget.
  if (allRows.length >= 28) {
    const wd = {};
    allRows.forEach((r) => { const k = weekday(r.d); const o = wd[k] || (wd[k] = { s: 0, m: 0, n: 0 }); o.s += r.sales || 0; o.m += r.spend || 0; o.n += 1; });
    const list = Object.entries(wd).map(([k, o]) => ({ k, s: o.s / o.n, m: o.m / o.n, per: o.m ? o.s / o.m : null })).sort((a, b) => b.s - a.s);
    const best = list.slice(0, 2), worst = list.slice(-2);
    const spendFlat = Math.max(...list.map((x) => x.m)) / Math.max(1, Math.min(...list.map((x) => x.m))) < 1.4;
    if (best[1].s > 1.4 * worst[0].s && spendFlat) {
      out.push({ id: 'weekday', kind: 'Budget', title: `Spend more on ${best[0].k} and ${best[1].k}`, conf: allRows.length >= 50 ? 'Medium' : 'Early signal', score: 70,
        why: [`Average website sales: ${best.map((x) => `${x.k} ${compact(x.s)}`).join(', ')}, but ${worst.map((x) => `${x.k} ${compact(x.s)}`).join(', ')}.`,
          `Meta spend is almost flat across the week (${compact(Math.min(...list.map((x) => x.m)))} to ${compact(Math.max(...list.map((x) => x.m)))} a day).`,
          `Based on ${allRows.length} days, and 1 big order can move a day, so treat this as a test.`],
      setup: [`Raise your best ad sets 25% on the evening before ${best[0].k} and ${best[1].k}, and lower them 25% before ${worst[0].k} and ${worst[1].k}.`, 'Or use a lifetime budget with an ad schedule.', 'Total weekly spend stays the same.'],
      budget: 'No new spend. 3 weeks.',
      win: 'Weekly website sales up 10% or more on the same weekly spend.', stop: 'Weekly sales down 10% or more for 2 weeks.', base: null });
    }
  }

  // 5. Messages buyers already use but ads never say.
  const ordersPay = mo.pay.reduce((t, r) => t + r[1], 0);
  const payShare = (re) => share(mo.pay.filter((r) => re.test(r[0])).reduce((t, r) => t + r[1], 0), ordersPay);
  const custom = share((mo.ot['Custom Made'] || [0])[0], mo.sales);
  const msgs = [
    { id: 'msg-emi', s: payShare(/emi/i), min: 0.08, re: /\bemi\b|no.?cost/i, title: 'Test "Pay in easy EMIs" on pieces over ₹40K', what: 'of orders were paid by EMI', line: 'Put the EMI option in the headline and on the image of 2 pieces priced ₹40K or more.' },
    { id: 'msg-custom', s: custom, min: 0.25, re: /custom|made to order|made-to-order|bespoke|personali[sz]/i, title: 'Test "Made for you" custom jewellery ads', what: 'of website sales were custom made', line: 'Show a piece being made or sized, with the line "Made to order in your size and karat". Only if the site offers it for that piece.' },
    { id: 'msg-cod', s: payShare(/cash/i), min: 0.15, re: /\bcod\b|cash on delivery/i, title: 'Test "Cash on delivery" as a trust line', what: 'of orders were cash on delivery', line: 'Add "Cash on delivery available" under the price on 2 of your best image ads.' },
  ];
  for (const m of msgs) {
    if (m.s === null || m.s < m.min) continue;
    const ads = adsMention(m.re);
    if (ads.spendShare !== null && ads.spendShare > 0.15) continue;
    out.push({ id: m.id, kind: 'Message', title: m.title, conf: m.s >= m.min * 2 ? 'Medium' : 'Early signal', score: 60 + Math.round(m.s * 40),
      why: [`${pc(m.s)} ${m.what} in the last 30 days.`, `Only ${ads.n} ad${ads.n === 1 ? '' : 's'} mention it, with ${pc(ads.spendShare || 0)} of spend.`, 'Buyers already choose this. The ads do not tell new buyers it exists.'],
      setup: [m.line, 'Run it as a copy and image variant next to the original in the same ad set, so only the message changes.'],
      budget: `${money(testBudget)} a day for 7 days.`, win: 'Link CTR up 15% and cost per purchase down vs the original.', stop: 'CTR below the original after 3,000 impressions.', base: bestImageAd(null) });
  }

  // 6. Price point where people actually buy.
  const bands = Object.fromEntries(mo.bands.filter((b) => b[0] === 'g').map((b) => [b[1], b[2]]));
  const bandTot = Object.values(bands).reduce((t, v) => t + (v || 0), 0);
  const mid = share(bands['10000-25000'] || 0, bandTot);
  if (mid !== null && mid >= 0.4) {
    const ads = adsMention(/₹\s?\d|rs\.?\s?\d|under\s?₹?\s?\d|starting at|from ₹/i);
    out.push({ id: 'price', kind: 'Message', title: 'Test an "Under ₹25K" edit', conf: mid >= 0.5 ? 'Medium' : 'Early signal', score: 62 + Math.round(mid * 20),
      why: [`${pc(mid)} of gold pieces sold in the last 30 days cost ₹10K to ₹25K.`, ads.n ? `Only ${ads.n} ad${ads.n === 1 ? '' : 's'} show a price.` : 'No ad shows a price.', 'A clear price removes the biggest doubt for a first gold purchase.'],
      setup: ['Make a carousel of 5 best sellers priced ₹10K to ₹25K, each card with its real price.', 'Headline: the price range, not a discount.'],
      budget: `${money(testBudget)} a day for 7 days.`, win: 'Cost per purchase 20% below the account average.', stop: 'No purchase after 2x your target cost per purchase.', base: bestImageAd(null) });
  }
  return out.sort((a, b) => b.score - a.score);
}
function testBrief(t) {
  return [`Test: ${t.title}`, `Type: ${t.kind}. Confidence: ${t.conf}.`, '', 'Why:', ...t.why.map((x) => '- ' + x), '', 'Setup:', ...t.setup.map((x) => '- ' + x), '',
    `Budget and time: ${t.budget}`, `Win if: ${t.win}`, `Stop if: ${t.stop}`].join('\n');
}
function testCard(t, i) {
  const confCls = t.conf === 'Strong' ? 'v-scale' : t.conf === 'Medium' ? 'v-watch' : '';
  return `<article class="tcard" data-test-id="${esc(t.id)}">
    <div class="tc-head"><span class="tc-rank">${i + 1}</span><div><div class="row" style="gap:6px"><span class="chip fmt">${esc(t.kind)}</span><span class="chip ${confCls}">${esc(t.conf)}</span></div><h3>${esc(t.title)}</h3></div></div>
    <div class="tc-cols"><div><h4>Why</h4><ul>${t.why.map((x) => `<li>${esc(x)}</li>`).join('')}</ul></div>
      <div><h4>The test</h4><ul>${t.setup.map((x) => `<li>${esc(x)}</li>`).join('')}</ul></div></div>
    <dl class="tc-rules"><div><dt>Budget and time</dt><dd>${esc(t.budget)}</dd></div><div><dt>Win if</dt><dd>${esc(t.win)}</dd></div><div><dt>Stop if</dt><dd>${esc(t.stop)}</dd></div></dl>
    <div class="act-btns"><button class="btn ghost" type="button" data-tl-add="${esc(t.id)}">Add to tests</button><button class="btn ghost" type="button" data-tl-copy="${esc(t.id)}">Copy brief</button>${t.base ? `<button class="btn" type="button" data-tl-build="${esc(t.id)}">Make the creative</button>` : ''}</div>
  </article>`;
}
function noAdSellers() {
  const keys = Object.keys(SL.data.months).sort().slice(-3);
  return skuRollup(keys).filter((r) => inAds(r.name) === false).sort((a, b) => b.n - a.n || b.v - a.v).slice(0, 10);
}
function noAdHtml() {
  const list = noAdSellers();
  if (!list.length) return '';
  TL.noAd = list;
  return `<section class="act-sec" id="act-noad"><div class="act-head"><h2>Best sellers with no ad</h2><span class="muted small">Last 3 months of website sales. No ad name or copy mentions these pieces.</span></div>
    <div class="tile"><div class="adlist">${list.map((r, i) => `<div class="adrow sku"><span class="rankc">${i + 1}</span><span><span class="nm">${esc(r.name)}</span><span class="mt">${esc(r.code)} · ${r.metal === 's' ? 'Silver' : 'Gold'} · ${esc(typeCat(r.name))} · about ${compact(r.v / r.n)} each</span></span><span class="rt"><b>${r.n} sold</b><span class="mt">${compact(r.v)}</span><button class="btn ghost small-btn" type="button" data-noad="${i}">Make an ad</button></span></div>`).join('')}</div>
    <p class="small muted">Matched on the first 2 words of each product name, so check before acting. Catalog ads may still show these pieces.</p></div></section>`;
}
function testsSectionHtml() {
  const list = TL.list || [];
  if (!list.length) return '';
  const w = tlWindow();
  return `<section class="act-sec tl" id="act-tests"><div class="act-head"><h2>Tests to run this week</h2><span class="muted small">Ranked. Built from website sales ${esc(dateLabel(w.since))} to ${esc(dateLabel(w.until))} and Meta ads together.</span></div>
    <div class="tl-grid">${list.map(testCard).join('')}</div>
    <p class="small muted">Each test changes 1 thing and says up front what counts as a win. Budgets are starting points. The page never changes the ad account.</p></section>`;
}

// Website sales line for each action card: how the ad's product category is selling.
function catSalesLine(id) {
  const w = tlWindow();
  if (!w) return '';
  const ad = ENGINE.c.ads[id] || DATA.ads[id];
  if (!ad) return '';
  const cat = adCat(ad);
  if (cat === 'Mixed' || cat === 'Other') return '<p class="act-sales">Sells a mix of products, so it cannot be matched to 1 category of website sales.</p>';
  const mo = rangeMonth(w.since, w.until), meta = metaRange(w.since, w.until);
  let s = 0, tot = 0;
  for (const [, type, v] of mo.types) { tot += v || 0; if (typeCat(type) === cat) s += v || 0; }
  const tagged = CATS.reduce((t, c) => t + (meta.cat[c] || 0), 0);
  const ss = share(s, tot), as = share(meta.cat[cat] || 0, tagged);
  if (ss === null || as === null) return '';
  const tone = ss - as > 0.08 ? 'up' : as - ss > 0.08 ? 'down' : '';
  const note = tone === 'up' ? 'Sales run ahead of ad spend. Good to push.' : tone === 'down' ? 'Ad spend runs ahead of sales. Check before adding budget.' : 'Spend and sales are in line.';
  return `<p class="act-sales ${tone}"><b>${esc(cat)} on the website:</b> ${pc(ss)} of sales vs ${pc(as)} of product ad spend, last 30 days. ${note}</p>`;
}

// Ad side panel: this ad's spend next to website sales of its category, day by day.
window.salesSideHtml = function salesSideHtml(id) {
  setTimeout(() => fillAdSales(id), 0);
  return '<section id="adSales"><h3>Website sales on the days it ran</h3><p class="small muted">Loading…</p></section>';
};
async function fillAdSales(id) {
  await loadSales();
  const box = $('adSales');
  if (!box || !SL.data || !dailyDays().length) { if (box) box.remove(); return; }
  const w = tlWindow(), ad = ENGINE.c.ads[id] || DATA.ads[id], cat = adCat(ad);
  const i0 = ENGINE.idx(w.all[0]), i1 = ENGINE.idx(w.all[w.all.length - 1]);
  const spendBy = {};
  for (const r of DATA.daily[id] || []) if (r[0] >= i0 && r[0] <= i1) spendBy[dayIso(r[0])] = r[1] || 0;
  const rows = w.all.map((d) => {
    const x = SL.data.daily[d];
    const cs = cat === 'Mixed' ? null : x.types.filter((t) => typeCat(t[1]) === cat).reduce((t, v) => t + (v[2] || 0), 0);
    return { d, spend: spendBy[d] || 0, sales: x.sales || 0, cs };
  });
  const on = rows.filter((r) => r.spend > 0), off = rows.filter((r) => r.spend <= 0);
  if (!on.length) { box.innerHTML = `<h3>Website sales on the days it ran</h3><p class="small muted">This ad did not spend between ${esc(dateLabel(w.all[0]))} and ${esc(dateLabel(w.all[w.all.length - 1]))}, the days with daily sales data.</p>`; return; }
  const avg = (l, k) => (l.length ? l.reduce((t, r) => t + (r[k] || 0), 0) / l.length : null);
  const med = on.map((r) => r.spend).sort((a, b) => a - b)[Math.floor(on.length / 2)];
  const hi = on.filter((r) => r.spend >= med), lo = rows.filter((r) => r.spend < med);
  const line = (label, a, b) => `<tr><td>${esc(label)}</td><td>${a === null ? '–' : compact(a)}</td><td>${b === null ? '–' : compact(b)}</td></tr>`;
  box.innerHTML = `<h3>Website sales on the days it ran</h3>
    <p class="small muted">${esc(dateLabel(w.all[0]))} to ${esc(dateLabel(w.all[w.all.length - 1]))}. It spent on ${on.length} of ${rows.length} days. Average website sales a day:</p>
    <table class="kv"><tr><td></td><td><b>It spent ${compact(med)}+</b></td><td><b>Less or nothing</b></td></tr>
      ${line('All website sales', avg(hi, 'sales'), avg(lo, 'sales'))}
      ${cat !== 'Mixed' ? line(`${cat} sales`, avg(hi, 'cs'), avg(lo, 'cs')) : ''}</table>
    ${sparkChart(rows.map((r) => ({ x: dayLabel(r.d), y: r.spend })), { kind: 'bar', color: 'var(--spend)', fmtY: (x) => money(x), title: 'This ad, daily spend' })}
    ${cat !== 'Mixed' ? sparkChart(rows.map((r) => ({ x: dayLabel(r.d), y: r.cs })), { kind: 'bar', color: 'var(--gold)', fmtY: (x) => compact(x), title: `${cat}, website sales a day` }) : ''}
    <p class="small muted">Days side by side, not proof that the ad caused the sales. Many ads run on the same days${off.length ? `, and ${off.length} days had no spend from it` : ''}.</p>`;
}

// Hook into the action plan.
const baseRenderActionsTL = window.renderActions;
window.renderActions = function () {
  baseRenderActionsTL();
  loadSales().then(() => {
    if (!SL.data || !dailyDays().length || state.tab !== 'actions') return;
    const key = VIEW.range.since + VIEW.range.until;
    if (!TL.list || TL.key !== key) { try { TL.list = buildTests(); } catch (e) { TL.list = []; } TL.key = key; }
    const view = $('actionsView');
    if (!view.querySelector('#act-tests')) {
      const stats = view.querySelector('.act-stats');
      if (stats) stats.insertAdjacentHTML('afterend', testsSectionHtml() + noAdHtml());
    }
    view.querySelectorAll('article.act').forEach((el) => { if (!el.querySelector('.act-sales')) { const d = el.querySelector('.act-do'); if (d) d.insertAdjacentHTML('afterend', catSalesLine(el.dataset.id)); } });
  });
};
document.addEventListener('click', async (e) => {
  const na = e.target.closest('[data-noad]');
  if (na && TL.noAd) {
    const r = TL.noAd[Number(na.dataset.noad)];
    STUDIO.base = bestImageAd(typeCat(r.name)); STUDIO.ref = ''; STUDIO.refRole = 'product';
    STUDIO.hint = `Paste the site photo of "${r.name}". Your best ad gives the layout.`;
    setTab('studio'); setTimeout(() => { const el = $('comp-tool'); if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' }); }, 400);
    return;
  }
  const t = (attr) => { const b = e.target.closest(`[${attr}]`); return b ? [b, (TL.list || []).find((x) => x.id === b.getAttribute(attr))] : [null, null]; };
  let [b, x] = t('data-tl-copy');
  if (b && x) { try { await navigator.clipboard.writeText(testBrief(x)); b.textContent = 'Copied'; } catch (err) { b.textContent = 'Copy blocked here'; } setTimeout(() => { b.textContent = 'Copy brief'; }, 1800); return; }
  [b, x] = t('data-tl-add');
  if (b && x) { await docsBoot(); b.disabled = true; const m = await addTest({ kind: 'test', label: x.title, idea: x.win, source_ad_id: x.base || '', source_ad_name: x.base ? (ENGINE.c.ads[x.base] || {}).name || '' : '' }); b.textContent = String(m).startsWith('Saved') ? 'Added' : 'Added for you'; return; }
  [b, x] = t('data-tl-build');
  if (b && x) { STUDIO.base = x.base; STUDIO.ref = ''; STUDIO.refRole = x.product ? 'product' : 'layout';
    STUDIO.hint = x.product ? `Paste the site photo of "${x.product}". Your best ad gives the layout.` : 'Paste a reference image, or build from your ad alone.';
    setTab('studio'); setTimeout(() => { const el = $('comp-tool'); if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' }); }, 400); }
});
