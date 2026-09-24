'use strict';
// Buyer desk: the media buyer's daily screen. Morning brief, blended return guardrail, budget moves,
// relaunch kit, audience and placement cuts, creative coverage, ad check-up and the festive plan.
// Read-only: every section says what to change; the team makes the change in Ads Manager.
// Uses VIEW, ENGINE, DATA (app/engine), SL, loadSales, metaDayMap, adCat (sales.js), rpDay (report.js),
// healthGroup, thumbHtml, openSide (app.js), sparkSvg, compact (overview.js), roasTxt (studio.js).

const BD = { guard: null, relaunchAll: false, covFmt: 'all', catalog: null };
const BD_SECTIONS = [['bd-brief', 'Morning brief'], ['bd-guard', 'Blended return'], ['bd-budget', 'Budget moves'], ['bd-relaunch', 'Relaunch kit'],
  ['bd-audience', 'Audience cuts'], ['bd-coverage', 'Creative coverage'], ['bd-checkup', 'Ad check-up'], ['bd-festive', 'Festive plan']];
// Festival dates (IST). Sources: devaastha.com and divinehindu.in festival calendars, read 24 Sep 2026.
const BD_FEST = {
  2025: [['2025-10-10', 'Karwa Chauth'], ['2025-10-18', 'Dhanteras'], ['2025-10-20', 'Diwali']],
  2026: [['2026-10-29', 'Karwa Chauth'], ['2026-11-06', 'Dhanteras'], ['2026-11-08', 'Diwali']],
};
const bdPct = (v) => (v === null || !Number.isFinite(v) ? '–' : Math.round(v * 100) + '%');
const bdX = (v) => (v === null || v === undefined || !Number.isFinite(v) ? 'no sales' : '₹' + v.toFixed(2));
const bdDay = (iso) => new Date(iso + 'T00:00:00Z').toLocaleDateString('en-IN', { weekday: 'short', day: 'numeric', month: 'short', timeZone: 'UTC' });

// ---------- shared numbers ----------
// Account totals per day index, from every ad (exclusions in the filter bar apply).
function bdAccountDays() {
  const inc = ENGINE.included(VIEW.exclusions.keywords, VIEW.exclusions.campaign_ids), out = {};
  for (const id of inc) for (const r of DATA.daily[id] || []) {
    const o = out[r[0]] || (out[r[0]] = { spend: 0, purch: 0, value: 0, seen: false, impr: 0, clicks: 0 });
    o.spend += r[1] || 0; o.purch += r[2] || 0; o.impr += r[4] || 0; o.clicks += r[5] || 0;
    if (r[3] !== null && r[3] !== undefined) { o.value += r[3]; o.seen = true; }
  }
  return out;
}
function bdSum(days, a, b) {
  const s = { spend: 0, purch: 0, value: 0, seen: false, impr: 0, clicks: 0, n: 0 };
  for (let d = a; d <= b; d++) { const o = days[d]; s.n += 1; if (!o) continue; s.spend += o.spend; s.purch += o.purch; s.impr += o.impr; s.clicks += o.clicks; if (o.seen) { s.value += o.value; s.seen = true; } }
  s.roas = s.spend && s.seen ? s.value / s.spend : null; s.cpa = s.purch ? s.spend / s.purch : null;
  return s;
}
// The last complete day: the capture day is partial, so step back 1 day when the capture is on the last day.
function bdLastFull() {
  const until = DATA.meta.window.until, cap = String(DATA.meta.captured_at || '').slice(0, 10);
  return cap >= until ? addDays(until, -1) : until;
}
function bdAdSums(id, a, b) { return ENGINE.sums(id, a, b); }
const bdLive = () => Object.keys(DATA.ads).filter((id) => DATA.ads[id].effective_status === 'ACTIVE');
function bdTarget() { return VIEW.targets.roas || VIEW.totals.roas || 0; }
function bdCpa() { return VIEW.targets.cpa || VIEW.totals.cpa || 0; }

// ---------- 1. Morning brief ----------
function bdBrief() {
  const days = bdAccountDays(), y = bdLastFull(), yi = ENGINE.idx(y);
  const d1 = bdSum(days, yi, yi), d7 = bdSum(days, yi - 7, yi - 1);
  const avg = (k) => (d7[k] !== undefined && d7.n ? d7[k] / d7.n : null);
  const site = rpDay(y), siteWeek = [];
  for (let i = 1; i <= 7; i++) { const x = rpDay(addDays(y, -i)); if (x && x.sales !== null) siteWeek.push(x); }
  const siteAvg = siteWeek.length ? siteWeek.reduce((t, x) => t + x.sales, 0) / siteWeek.length : null;
  const per = site && site.sales !== null && d1.spend ? site.sales / d1.spend : null;
  const perWeek = siteAvg !== null && avg('spend') ? siteAvg / avg('spend') : null;
  const T = bdTarget(), C = bdCpa(), alerts = [];
  // Live ads: spend with no sale, stopped delivering, cost per order jump.
  for (const id of bdLive()) {
    const ad = DATA.ads[id], m3 = bdAdSums(id, yi - 2, yi), m7 = bdAdSums(id, yi - 7, yi - 1), m1 = bdAdSums(id, yi, yi);
    if (C && m3.spend >= 2 * C && !m3.purchases) alerts.push({ sev: 3, id, text: `"${ad.name}" spent ${compact(m3.spend)} in 3 days with no sale. Pause it or change the creative.` });
    else if (m7.spend >= 7000 && m1.spend < m7.spend / 7 * 0.2) alerts.push({ sev: 2, id, text: `"${ad.name}" is on but almost stopped spending (${compact(m1.spend)} yesterday vs ${compact(m7.spend / 7)} a day before). Check the ad set budget, audience or a rejected ad.` });
    else if (m1.purchases && m7.purchases >= 2 && m1.spend / m1.purchases > 2 * (m7.spend / m7.purchases)) alerts.push({ sev: 1, id, text: `"${ad.name}" paid ${compact(m1.spend / m1.purchases)} for an order yesterday, over 2 times its week (${compact(m7.spend / m7.purchases)}).` });
  }
  if (avg('spend') && d1.spend > avg('spend') * 1.4) alerts.push({ sev: 2, text: `Account spend jumped to ${compact(d1.spend)}, ${Math.round((d1.spend / avg('spend') - 1) * 100)}% above the daily average. Check for a budget change or a new campaign.` });
  const g = bdGuardData();
  if (g && g.now !== null && g.now < g.floor) alerts.push({ sev: 3, text: `Website sales for every ₹1 of ads fell to ₹${g.now.toFixed(1)} over 7 days, under the floor of ₹${g.floor.toFixed(1)}. See Blended return.` });
  alerts.sort((a, b) => b.sev - a.sev);
  // Today's 3 things, from the action plan.
  const o = ENGINE.opportunities(VIEW), todo = [];
  if (o.pause[0]) todo.push(`Pause or fix "${o.pause[0].name}": ${compact(o.pause[0].m7.spend)} this week at ROAS ${roasTxt(o.pause[0].m7.roas)}.`);
  if (o.scale[0]) todo.push(`Raise "${o.scale[0].name}" by about 20%: ROAS ${roasTxt(o.scale[0].m7.roas)} this week.`);
  const rl = bdRelaunchList()[0];
  if (rl) todo.push(`Relaunch "${rl.ad.name}": ROAS ${bdX(rl.m.roas)} on ${rl.m.purchases} sales before it was switched off.`);
  if (todo.length < 3 && o.tired[0]) todo.push(`Refresh "${o.tired[0].name}": ${o.tired[0].fatigue.reason}`);
  const kpi = (label, v, ref, fmtv, good = 1) => {
    const ch = v !== null && ref ? (v - ref) / ref : null;
    const tone = ch === null || Math.abs(ch) < 0.05 ? 'flat' : (ch > 0) === (good > 0) ? 'good' : 'bad';
    return `<div class="bd-kpi"><span class="muted small">${esc(label)}</span><b>${v === null ? '<span class="na">Not available</span>' : esc(fmtv(v))}</b><span class="rp-delta ${tone}">${ch === null ? 'no 7-day average' : `${ch > 0 ? '▲' : '▼'} ${Math.abs(Math.round(ch * 100))}% vs 7-day average`}</span></div>`;
  };
  BD.briefText = [`Gehna ads, ${bdDay(y)}`, `Ad spend ${compact(d1.spend)} | Meta orders ${d1.purch} | Meta ROAS ${bdX(d1.roas)}`,
    `Website sales ${site && site.sales !== null ? compact(site.sales) : 'not available'} from ${site ? site.orders : '–'} orders | ₹${per ? per.toFixed(1) : '–'} for every ₹1 of ads`,
    '', 'Watch out:', ...(alerts.length ? alerts.slice(0, 6).map((a) => '- ' + a.text) : ['- Nothing unusual.']), '', 'Today:', ...todo.map((t, i) => `${i + 1}. ${t}`)].join('\n');
  return `<section class="panel-box bd-sec" id="bd-brief"><div class="bd-head"><div><h2>Morning brief</h2><p class="lead">${esc(bdDay(y))}, the last full day in the data. Compared with the 7 days before.</p></div>
      <button class="btn ghost small-btn" type="button" data-bdcopy="brief">Copy for WhatsApp</button></div>
    <div class="bd-kpis">${kpi('Ad spend', d1.spend, avg('spend'), compact, 0)}${kpi('Orders Meta counted', d1.purch, avg('purch'), (v) => String(v))}${kpi('Meta ROAS', d1.roas, d7.roas, bdX)}
      ${kpi('Website sales', site ? site.sales : null, siteAvg, compact)}${kpi('Website orders', site ? site.orders : null, siteWeek.length ? siteWeek.reduce((t, x) => t + x.orders, 0) / siteWeek.length : null, (v) => String(Math.round(v * 10) / 10))}
      ${kpi('Website sales per ₹1 of ads', per, perWeek, (v) => '₹' + v.toFixed(1))}</div>
    <div class="bd-two"><div><h3>Watch out (${alerts.length})</h3>${alerts.length ? `<ul class="bd-alerts">${alerts.slice(0, 8).map((a) => `<li class="sev${a.sev}">${a.id ? `<button class="linkbtn" type="button" data-bdopen="${esc(a.id)}">Open</button> ` : ''}${esc(a.text)}</li>`).join('')}</ul>` : '<p class="muted">Nothing unusual yesterday.</p>'}</div>
      <div><h3>Today's ${todo.length} things</h3><ol class="bd-todo">${todo.map((t) => `<li>${esc(t)}</li>`).join('')}</ol></div></div></section>`;
}

// ---------- 2. Blended return guardrail ----------
// Website sales (Metabase) for every ₹1 of Meta ad money, 7-day rolling. Floor = 80% of the 90-day level.
function bdGuardData() {
  if (!SL.data) return null;
  const days = bdAccountDays(), end = bdLastFull(), rows = [];
  for (let i = 179; i >= 0; i--) {
    const d = addDays(end, -i), x = rpDay(d), m = days[ENGINE.idx(d)];
    rows.push({ d, sales: x && x.sales !== null ? x.sales : null, spend: m ? m.spend : 0 });
  }
  const roll = rows.map((r, i) => {
    if (i < 6) return null;
    const w = rows.slice(i - 6, i + 1);
    if (w.some((x) => x.sales === null)) return null;
    const sp = w.reduce((t, x) => t + x.spend, 0);
    return sp ? w.reduce((t, x) => t + x.sales, 0) / sp : null;
  });
  const last90 = rows.slice(-90), sp90 = last90.reduce((t, x) => t + x.spend, 0), s90 = last90.filter((x) => x.sales !== null);
  const level = sp90 && s90.length === last90.length ? s90.reduce((t, x) => t + x.sales, 0) / sp90 : null;
  if (level === null) return null;
  return { rows, roll, level, floor: level * 0.8, good: level * 1.2, now: roll[roll.length - 1] };
}
function bdGuard() {
  const g = bdGuardData();
  if (!g) return `<section class="panel-box bd-sec" id="bd-guard"><h2>Blended return</h2><p class="muted">Needs website sales for the last 90 days.</p></section>`;
  const n = 90, rows = g.rows.slice(-n), roll = g.roll.slice(-n);
  const W = 900, H = 230, L = 54, R = 12, T = 12, B = 30;
  const vals = roll.filter((v) => v !== null), max = Math.max(g.good * 1.15, ...vals) * 1.05;
  const x = (i) => L + (W - L - R) * i / (n - 1), y = (v) => T + (H - T - B) * (1 - v / max);
  const pts = roll.map((v, i) => (v === null ? null : [x(i), y(v)]));
  const line = typeof smoothPath === 'function' ? smoothPath(pts) : '';
  const every = 15;
  const ticks = rows.map((r, i) => (i % every === 0 || i === n - 1 ? `<text class="tl" x="${x(i).toFixed(1)}" y="${H - 8}" text-anchor="${i === n - 1 ? 'end' : 'middle'}">${esc(shortDate(r.d))}</text>` : '')).join('');
  const hov = rows.map((r, i) => `<rect x="${(x(i) - (W - L - R) / n / 2).toFixed(1)}" y="${T}" width="${((W - L - R) / n).toFixed(1)}" height="${H - T - B}" fill="transparent" data-tip="${esc([bdDay(r.d), '7-day sales per ₹1', roll[i] === null ? 'Not available' : '₹' + roll[i].toFixed(1), 'Website sales that day', r.sales === null ? 'Not available' : compact(r.sales), 'Ad money that day', compact(r.spend)].join('|'))}"/>`).join('');
  const state = g.now === null ? ['flat', 'Not available'] : g.now < g.floor ? ['bad', 'Below the floor'] : g.now > g.good ? ['good', 'Above the good line'] : ['flat', 'Inside the normal band'];
  return `<section class="panel-box bd-sec" id="bd-guard"><div class="bd-head"><div><h2>Blended return guardrail</h2>
      <p class="lead">All website sales for every ₹1 of Meta ads, over the last 7 days. Meta's own numbers cannot show this, so it is the honest check.</p></div>
      <div class="bd-big ${state[0]}"><b>${g.now === null ? '–' : '₹' + g.now.toFixed(1)}</b><span>${state[1]}</span></div></div>
    <svg class="rp-chart" viewBox="0 0 ${W} ${H}" role="img" aria-label="7-day website sales per rupee of ads">
      <rect x="${L}" width="${W - L - R}" y="${y(g.good).toFixed(1)}" height="${(y(g.floor) - y(g.good)).toFixed(1)}" style="fill:var(--good-soft)"/>
      ${[g.floor, g.level, g.good].map((v, i) => `<line x1="${L}" x2="${W - R}" y1="${y(v).toFixed(1)}" y2="${y(v).toFixed(1)}" style="stroke:${i === 0 ? 'var(--bad)' : i === 2 ? 'var(--good)' : 'var(--muted)'};stroke-dasharray:4 4"/><text class="tl" x="${L - 6}" y="${(y(v) + 4).toFixed(1)}" text-anchor="end">₹${v.toFixed(1)}</text>`).join('')}
      <path d="${line}" style="fill:none;stroke:var(--ink)" stroke-width="2.2" stroke-linecap="round"/>${ticks}${hov}</svg>
    ${rpLegend([['var(--ink)', '7-day website sales per ₹1 of ads'], ['var(--bad)', `Floor ₹${g.floor.toFixed(1)} (80% of the 90-day level)`], ['var(--good)', `Good ₹${g.good.toFixed(1)} (120%)`]])}
    <p class="small muted">90-day level: ₹${g.level.toFixed(1)} of website sales for every ₹1 of ads. Below the floor for 3 days in a row: cut the weakest ads first, do not add budget. Above the good line: room to spend more. Big single orders lift a week, see the client report for those days.</p></section>`;
}

// ---------- 3. Budget move planner ----------
function bdCampaigns() {
  const yi = ENGINE.idx(bdLastFull()), map = {};
  const inc = ENGINE.included(VIEW.exclusions.keywords, VIEW.exclusions.campaign_ids);
  for (const id of inc) {
    const ad = DATA.ads[id];
    const o = map[ad.campaign_id] || (map[ad.campaign_id] = { id: ad.campaign_id, name: ad.campaign_name, live: false, m7: [], m30: [] });
    if (ad.effective_status === 'ACTIVE') o.live = true;
    o.m7.push(ENGINE.sums(id, yi - 6, yi)); o.m30.push(ENGINE.sums(id, yi - 29, yi));
  }
  return Object.values(map).map((c) => ({ ...c, m7: ENGINE.constructor.addUp(c.m7), m30: ENGINE.constructor.addUp(c.m30) })).filter((c) => c.live && c.m7.spend > 0);
}
function bdBudget() {
  const T = bdTarget(), camps = bdCampaigns();
  for (const c of camps) {
    c.daily = c.m7.spend / 7;
    c.act = c.m7.roas !== null && c.m7.purchases >= 3 && c.m7.roas >= T * 1.2 ? 'grow' : (c.m7.roas === null || c.m7.roas < T * 0.6) && c.m7.spend >= Math.max(3000, bdCpa()) ? 'cut' : 'hold';
  }
  const cut = camps.filter((c) => c.act === 'cut'), grow = camps.filter((c) => c.act === 'grow').sort((a, b) => b.m7.roas - a.m7.roas);
  let pool = 0;
  for (const c of cut) { c.move = -Math.round(c.daily * 0.3 / 100) * 100; pool -= c.move; }
  // Give each winner up to +20% a day (Meta relearns after big jumps), best ROAS first.
  let left = pool;
  for (const c of grow) { const add = Math.min(left, Math.round(c.daily * 0.2 / 100) * 100); c.move = add; left -= add; }
  for (const c of camps) { c.move = c.move || 0; c.next = c.daily + c.move; }
  const total = camps.reduce((t, c) => t + c.daily, 0);
  const rows = [...grow, ...cut, ...camps.filter((c) => c.act === 'hold')];
  const why = (c) => (c.act === 'grow' ? `ROAS ${roasTxt(c.m7.roas)} this week on ${c.m7.purchases} orders, above target ${roasTxt(T)}.` : c.act === 'cut' ? `ROAS ${roasTxt(c.m7.roas)} this week, under 60% of target.` : 'Near target. Leave it.');
  BD.budgetText = ['Budget moves (per day, total stays the same):', ...rows.filter((c) => c.move).map((c) => `- ${c.name}: ${compact(c.daily)} → ${compact(c.next)} (${c.move > 0 ? '+' : '−'}${compact(Math.abs(c.move))}). ${why(c)}`), left > 0 ? `- Keep ${compact(left)} a day unspent or give it to the next best campaign.` : ''].filter(Boolean).join('\n');
  return `<section class="panel-box bd-sec" id="bd-budget"><div class="bd-head"><div><h2>Budget move planner</h2>
      <p class="lead">Live campaigns, last 7 days. Take 30% from campaigns far under target and give it to the best ones, at most +20% each, so Meta does not reset. Total spend stays the same.</p></div>
      <button class="btn ghost small-btn" type="button" data-bdcopy="budget">Copy moves</button></div>
    <div class="scroll"><table class="bd-table"><tr><th>Campaign</th><th class="n">Now a day</th><th class="n">Move</th><th class="n">New a day</th><th class="n">7-day ROAS</th><th class="n">Orders</th><th>Why</th></tr>
      ${rows.map((c) => `<tr class="bd-${c.act}"><td>${esc(c.name)}</td><td class="n">${compact(c.daily)}</td><td class="n"><b class="${c.move > 0 ? 'up' : c.move < 0 ? 'down' : ''}">${c.move ? (c.move > 0 ? '+' : '−') + compact(Math.abs(c.move)) : '–'}</b></td><td class="n">${compact(c.next)}</td><td class="n">${roasTxt(c.m7.roas)}</td><td class="n">${c.m7.purchases || 0}</td><td class="small">${esc(why(c))}</td></tr>`).join('')}
      <tr class="bd-total"><td>All live campaigns</td><td class="n">${compact(total)}</td><td class="n">${left > 0 ? `${compact(left)} not placed` : '0'}</td><td class="n">${compact(total - Math.max(0, left))}</td><td colspan="3"></td></tr></table></div>
    <p class="small muted">Set the change where the budget sits: the campaign budget if it uses Advantage campaign budget, otherwise its ad sets. Change once, then wait 3 days before the next move.</p></section>`;
}

// ---------- 4. Relaunch kit ----------
function bdRelaunchList() {
  const ids = (VIEW.collections.health || VIEW.collections.all).ad_ids;
  return ids.map((id) => VIEW.ads[id]).filter((a) => a && healthGroup(a) === 'relaunch')
    .map((a) => ({ ad: a, m: a.view.metrics, sale: bdSale(a), score: a.view.metrics.roas * Math.log(1 + a.view.metrics.purchases) }))
    .sort((x, y) => x.sale - y.sale || y.score - x.score);   // evergreen ads first, sale ads after
}
// Sale and countdown ads only make sense again when a sale is on.
function bdSale(ad) {
  const c = ad.creative || {};
  return /\b(eoss|sale|% ?off|hours left|days? left|days? to go|day to go|last \d+|countdown)\b/i.test([ad.name, ad.campaign_name, ad.adset_name, c.headline, c.primary_text].join(' '));
}
function bdRelaunch() {
  const list = bdRelaunchList(), C = bdCpa(), show = BD.relaunchAll ? list : list.slice(0, 8);
  if (!list.length) return `<section class="panel-box bd-sec" id="bd-relaunch"><h2>Relaunch kit</h2><p class="muted">No switched-off ad beat the target with 2 or more sales in these dates. Try the last 365 days.</p></section>`;
  const card = ({ ad, m, sale }) => {
    const lc = ENGINE.lifecycle(ad.id, (C || 5000) / 2), c = ad.creative;
    const daily = lc && lc.days_live ? Math.max(500, Math.round(lc.lifetime.spend / lc.days_live / 100) * 100) : 1000;
    const brief = [`Relaunch: ${ad.name} (${c.type_label}, ad ID ${ad.id})`, `Was in: ${ad.campaign_name} > ${ad.adset_name}`,
      `Result in these dates: ROAS ${bdX(m.roas)}, ${m.purchases} orders on ${compact(m.spend)}.`,
      lc ? `Life: ${lc.first_day} to ${lc.last_day}. Best week ${lc.peak_roas !== null ? `ROAS ${lc.peak_roas.toFixed(2)}x on ${lc.peak_day}` : 'not clear'}.${lc.fatigue_day ? ` It tired on ${lc.fatigue_day}.` : ''}` : '',
      `Do: duplicate the ad into a new ad set (same audience) at about ${compact(daily)} a day for 7 days. Add 2 fresh versions of the creative next to it.`,
      `Stop if: ${compact(2 * (C || 5000))} spent with no sale.`].filter(Boolean).join('\n');
    return `<article class="bd-rl">${thumbHtml(ad.id, ad.name)}<div><b>${esc(ad.name)}</b>${sale ? ' <span class="chip v-watch">Sale ad: bring back with a live offer</span>' : ''}<div class="rp-adm"><span>${esc(c.type_label)}</span><span>ROAS ${bdX(m.roas)}</span><span>${m.purchases} orders</span><span>spent ${compact(m.spend)}</span></div>
      <p class="small">${lc ? `Ran ${esc(shortDate(lc.first_day))} to ${esc(shortDate(lc.last_day))}. ${lc.fatigue_day ? `Tired on ${esc(shortDate(lc.fatigue_day))}, ${lc.days_to_fatigue} days after launch.` : 'Did not tire; it was switched off.'} ` : ''}Relaunch at about <b>${compact(daily)} a day</b>, with 2 fresh versions.</p>
      <p class="small muted">${esc(ad.campaign_name)} › ${esc(ad.adset_name)}</p>
      <div class="act-btns"><button class="btn ghost small-btn" type="button" data-bdcopytext="${esc(brief)}">Copy brief</button><button class="btn ghost small-btn" type="button" data-bdopen="${esc(ad.id)}">${c.type === 'static_image' ? 'Make fresh versions' : 'Open ad'}</button></div></div></article>`;
  };
  return `<section class="panel-box bd-sec" id="bd-relaunch"><div class="bd-head"><div><h2>Relaunch kit</h2>
      <p class="lead">${list.length} switched-off ads beat the ROAS target (${roasTxt(bdTarget())}) with 2 or more sales in these dates. Everyday ads first, then sale ads to keep for the next sale. Each has a ready brief.</p></div></div>
    <div class="bd-rls">${show.map(card).join('')}</div>
    ${list.length > show.length ? `<button class="btn ghost" type="button" data-bdrelaunchall>Show all ${list.length}</button>` : ''}</section>`;
}

// ---------- 5. Audience and placement cuts ----------
function bdAudience() {
  const d = VIEW.demographics_all || {}, T = VIEW.totals.roas || 0, days = VIEW.range.days;
  const rows = [];
  const label = { age: 'Age', gender: 'Gender', publisher_platform: 'Platform' };
  for (const dim of ['age', 'gender', 'publisher_platform']) {
    const e = Object.entries(d[dim] || {}).filter(([k, x]) => x.spend > 0 && !/unknown/i.test(k));
    const tot = e.reduce((t, [, x]) => t + x.spend, 0);
    for (const [k0, x] of e) { const k = { facebook: 'Facebook', instagram: 'Instagram', audience_network: 'Audience Network', messenger: 'Messenger', whatsapp: 'WhatsApp', threads: 'Threads', male: 'Men', female: 'Women' }[k0] || k0; rows.push({ dim, k, spend: x.spend, share: tot ? x.spend / tot : 0, roas: x.roas, value: x.purchase_value }); }
  }
  const cuts = rows.filter((r) => r.share >= 0.05 && (r.roas === null || r.roas < T * 0.5)).sort((a, b) => b.spend - a.spend);
  const lean = rows.filter((r) => r.share >= 0.03 && r.roas !== null && r.roas >= T * 1.3).sort((a, b) => b.roas - a.roas);
  const perMonth = (s) => s / days * 30;
  const line = (r, kind) => `<li><b>${esc(label[r.dim])} ${esc(r.k)}</b>: ${bdPct(r.share)} of money, ${bdX(r.roas)} back for ₹1 (account ${bdX(T)}). ${kind === 'cut'
    ? `Exclude it, or cap it with a separate ad set. Frees about <b>${compact(perMonth(r.spend))} a month</b>.` : 'Give it its own ad set or more of the budget.'}</li>`;
  const bars = (dim) => rpHbar(rows.filter((r) => r.dim === dim).map((r) => ({ label: r.k, a: r.roas || 0, colorA: r.roas !== null && r.roas < T * 0.5 ? 'var(--bad)' : r.roas !== null && r.roas >= T * 1.3 ? 'var(--good)' : 'var(--roas)',
    valTxt: `${bdX(r.roas)} back · ${bdPct(r.share)} of money`, tip: [r.k, 'Ad money', compact(r.spend), 'Back for ₹1', bdX(r.roas)].join('|') })));
  return `<section class="panel-box bd-sec" id="bd-audience"><h2>Audience and placement cuts</h2>
    <p class="lead">Every ad in these dates, split by age, gender and platform. Red: under half the account return on 5% or more of the money. Green: 30% or more above it.</p>
    <div class="bd-two"><div><h3 class="bad">Cut or cap (${cuts.length})</h3>${cuts.length ? `<ul class="bd-list">${cuts.map((r) => line(r, 'cut')).join('')}</ul>` : '<p class="muted">No big leak.</p>'}</div>
      <div><h3 class="good">Lean in (${lean.length})</h3>${lean.length ? `<ul class="bd-list">${lean.map((r) => line(r, 'lean')).join('')}</ul>` : '<p class="muted">No group stands out.</p>'}</div></div>
    <div class="bd-three"><div><h3>Age</h3>${bars('age')}</div><div><h3>Gender</h3>${bars('gender')}</div><div><h3>Platform</h3>${bars('publisher_platform')}</div></div>
    <p class="small muted">Advantage+ audiences can ignore exclusions. Where that happens, cap the group in its own ad set instead. Meta's age data is by month, so short date ranges are close, not exact.</p></section>`;
}

// ---------- 6. Creative coverage map ----------
function bdCoverage() {
  const [a, b] = ENGINE.resolveRange(VIEW.range.since, VIEW.range.until), T = bdTarget();
  const inc = ENGINE.included(VIEW.exclusions.keywords, VIEW.exclusions.campaign_ids), cells = {}, angles = {}, prods = {};
  const fmtOk = (ad) => BD.covFmt === 'all' || ad.creative.type === BD.covFmt;
  for (const id of inc) {
    const ad = DATA.ads[id];
    if (!fmtOk(ad) || !ad.tags) continue;
    const m = ENGINE.sums(id, a, b);
    if (m.spend <= 0) continue;
    const an = ad.tags.angle.label, pr = adCat(ENGINE.c.ads[id] || ad);
    angles[an] = (angles[an] || 0) + m.spend; prods[pr] = (prods[pr] || 0) + m.spend;
    const k = an + '|' + pr, c = cells[k] || (cells[k] = { ads: 0, list: [] });
    c.ads += 1; c.list.push(m);
  }
  const A = Object.keys(angles).sort((x, y) => angles[y] - angles[x]), P = [...CATS.filter((c) => c !== 'Other'), 'Mixed', 'Other'].filter((p) => prods[p] !== undefined || CATS.includes(p));
  const cellHtml = (an, pr) => {
    const c = cells[an + '|' + pr];
    if (!c) return `<td class="cov-empty" data-tip="${esc([an + ' × ' + pr, 'Status', 'Not tried'].join('|'))}">Not tried</td>`;
    const m = ENGINE.constructor.addUp(c.list), r = m.roas;
    const cls = r === null ? 'cov-none' : r >= T * 1.2 ? 'cov-win' : r >= T * 0.8 ? 'cov-ok' : 'cov-lose';
    return `<td class="${cls}" data-tip="${esc([an + ' × ' + pr, 'Ads', c.ads, 'Spend', compact(m.spend), 'ROAS', roasTxt(r), 'Orders', m.purchases].join('|'))}"><b>${roasTxt(r)}</b><span>${c.ads} ad${c.ads === 1 ? '' : 's'} · ${compact(m.spend)}</span></td>`;
  };
  const gaps = [];
  const winners = A.filter((an) => !/catalog/i.test(an)).map((an) => ({ an, m: ENGINE.constructor.addUp(Object.entries(cells).filter(([k]) => k.startsWith(an + '|')).flatMap(([, c]) => c.list)) }))
    .filter((x) => x.m.roas !== null && x.m.roas >= T).sort((x, y) => y.m.roas - x.m.roas).slice(0, 3);
  for (const { an } of winners) for (const pr of CATS.filter((p) => p !== 'Other')) if (!cells[an + '|' + pr]) gaps.push(`${an} on ${pr.toLowerCase()}`);
  const fmts = [['all', 'All formats'], ['static_image', 'Image'], ['video', 'Video'], ['carousel', 'Carousel'], ['catalog_dynamic', 'Catalog']];
  return `<section class="panel-box bd-sec" id="bd-coverage"><div class="bd-head"><div><h2>Creative coverage map</h2>
      <p class="lead">What each message has been tried on, by product type, in these dates. Gold: beats target. Grey: close. Red: loses. Dashed: never tried.</p></div>
      <div class="seg" role="group" aria-label="Format">${fmts.map(([k, l]) => `<button type="button" data-bdcov="${k}" aria-pressed="${BD.covFmt === k}">${l}</button>`).join('')}</div></div>
    <div class="scroll"><table class="bd-cov"><tr><th>Message</th>${P.map((p) => `<th>${esc(p)}</th>`).join('')}</tr>${A.map((an) => `<tr><th>${esc(an)}</th>${P.map((p) => cellHtml(an, p)).join('')}</tr>`).join('')}</table></div>
    ${gaps.length ? `<p class="small"><b>Next to try:</b> ${esc(gaps.slice(0, 8).join(', '))}. These are your best messages (beating target) on product types that never had them.</p>` : ''}
    <p class="small muted">Messages and products are tagged from ad names and copy, so a few can be wrong.</p></section>`;
}

// ---------- 7. Ad check-up ----------
function bdCheckup() {
  const issues = [], cat = BD.catalog;
  const bySlug = {};
  if (cat) for (const p of cat.products) if (p.url) bySlug[p.url.split('/').pop()] = p;
  for (const id of bdLive()) {
    const ad = DATA.ads[id], c = ad.creative, add = (sev, what, fix) => issues.push({ id, ad, sev, what, fix });
    const txt = [c.primary_text, c.headline].filter(Boolean).join(' ');
    let url = null;
    try { url = c.link_url ? new URL(c.link_url) : null; } catch (e) { url = null; }
    if (c.type === 'static_image' || c.type === 'video') {
      if (url && !/gehnaindia\.com$/.test(url.hostname)) add(3, `Link goes to ${url.hostname}, not gehnaindia.com.`, 'Fix the link.');
      else if (url && (url.pathname === '/' || url.pathname === '')) add(1, 'Sends people to the home page, not a product or collection.', 'Point it at the product or a collection page. Home page traffic buys less.');
    }
    if (c.link_url && !/utm_/i.test(c.link_url)) add(1, 'No UTM tags on the link.', 'Add utm_source=facebook&utm_medium=paid&utm_campaign={{campaign.name}} so Google Analytics can see these visits.');
    if (/\b(copy|copy of|new ad|ad \d+|untitled)\b/i.test(ad.name)) add(1, `Unclear name: "${ad.name}".`, 'Rename it with product, message and format so reports make sense.');
    if (/\b(eoss|sale|% ?off|hours left|days left|last \d+)\b/i.test(txt + ' ' + ad.name)) add(2, 'Sale or countdown message is still live.', 'Check the offer is still true today. Old sale ads hurt trust.');
    const slug = url ? url.pathname.replace(/^\/+|\/+$/g, '') : '', p = bySlug[slug];
    if (p) {
      const prices = [...txt.matchAll(/(?:₹|rs\.?\s?)\s?([\d,]{4,})/gi)].map((m) => Number(m[1].replace(/,/g, '')));
      if (prices.length && p.price && !prices.some((v) => Math.abs(v - p.price) / p.price < 0.03)) add(3, `Copy says ${prices.map((v) => '₹' + v.toLocaleString('en-IN')).join(', ')}; the catalog price is ₹${p.price.toLocaleString('en-IN')}.`, 'Update the copy to the real price.');
      if (p.availability && p.availability !== 'in stock') add(3, 'The product in this ad is out of stock.', 'Pause the ad or point it at a similar piece.');
    }
  }
  // Catalog ads that use the old product set.
  if (cat) {
    const liveCat = bdLive().filter((id) => DATA.ads[id].creative.type === 'catalog_dynamic');
    const miss = cat.products.filter((p) => !p.in_ads_set).length;
    if (liveCat.length && miss) issues.push({ sev: 3, id: liveCat[0], ad: DATA.ads[liveCat[0]], what: `${liveCat.length} live catalog ads use "${cat.ads_set_name}", which is missing ${miss} of your top ${cat.products.length} sellers.`, fix: 'Add them to the set, or point the ads at a "Top sellers" set. See the Catalog tab.' });
  }
  // Price in the copy vs the catalog, matched on the product name.
  if (cat) for (const id of bdLive()) {
    const ad = DATA.ads[id], c = ad.creative, txt = [ad.name, c.headline, c.primary_text].filter(Boolean).join(' ').toLowerCase();
    const prices = [...txt.matchAll(/(?:₹|rs\.?\s?)\s?([\d,]{4,})/gi)].map((m) => Number(m[1].replace(/,/g, '')));
    if (!prices.length) continue;
    const p = cat.products.find((q) => { const w = q.name.toLowerCase().split(/\s+/).filter((x) => x.length > 3).slice(0, 2); return w.length === 2 && w.every((x) => txt.includes(x)); });
    if (p && p.price && !prices.some((v) => Math.abs(v - p.price) / p.price < 0.03)) issues.push({ id, ad, sev: 3, what: `Copy says ${prices.map((v) => '₹' + v.toLocaleString('en-IN')).join(', ')}; "${p.name}" is ₹${p.price.toLocaleString('en-IN')} in the catalog.`, fix: 'Update the copy to the real price.' });
  }
  // Tired live ads, and live ads running a long time.
  const yiC = ENGINE.idx(bdLastFull());
  for (const id of bdLive()) {
    const ad = DATA.ads[id], f = ENGINE.fatigue(id, yiC), lc = ENGINE.lifecycle(id, (bdCpa() || 5000) / 2);
    if (f && ['declining', 'ctr_down', 'roas_down'].includes(f.code)) issues.push({ id, ad, sev: 2, what: `Tired: ${f.reason}`, fix: 'Make 2 fresh versions (new photo or first line) and run them next to it.' });
    else if (lc && lc.days_live >= 90) issues.push({ id, ad, sev: 1, what: `Running for ${lc.days_live} days.`, fix: 'Plan a refresh before it tires.' });
  }
  if (cat) for (const p of cat.products) for (const r of p.missing_images || []) issues.push({ sev: 2, what: `Catalog item ${r} (${p.name}) has no image.`, fix: 'Add the image in the catalog, or catalog ads cannot show this size.' });
  issues.sort((a, b) => b.sev - a.sev);
  const sevTxt = { 3: 'Fix now', 2: 'Check', 1: 'Tidy' };
  return `<section class="panel-box bd-sec" id="bd-checkup"><h2>Ad check-up</h2>
    <p class="lead">${bdLive().length} live ads checked against their links, the catalog and the website. ${issues.length} thing${issues.length === 1 ? '' : 's'} to look at.</p>
    ${issues.length ? `<div class="scroll"><table class="bd-table"><tr><th></th><th>Ad</th><th>What is wrong</th><th>Fix</th></tr>${issues.slice(0, 60).map((x) => `<tr><td><span class="chip ${x.sev === 3 ? 'v-cut' : x.sev === 2 ? 'v-watch' : ''}">${sevTxt[x.sev]}</span></td><td>${x.ad ? `<button class="linkbtn" type="button" data-bdopen="${esc(x.id)}">${esc(x.ad.name)}</button>` : 'Catalog'}</td><td class="small">${esc(x.what)}</td><td class="small">${esc(x.fix)}</td></tr>`).join('')}</table></div>` : '<p class="muted">All clear.</p>'}
    <p class="small muted">Prices and stock come from the Meta catalog (read ${esc(cat ? cat.pulled_at : 'not yet')}). Links and UTM tags are checked when the ad data has a link. Most live ads keep their link inside the Facebook post, which the read-only data does not include, so check those by hand once.</p></section>`;
}

// ---------- 8. Festive plan ----------
function bdFestive() {
  const days = bdAccountDays(), fest25 = BD_FEST[2025], fest26 = BD_FEST[2026];
  const diwali25 = fest25[2][0];
  // Last year, week by week around Diwali (4 weeks before to 2 after), from Meta.
  const weeks = [];
  for (let w = -5; w <= 1; w++) {
    const start = addDays(diwali25, w * 7 - 3), end = addDays(start, 6), a = ENGINE.idx(start), b = ENGINE.idx(end);
    if (a < 0) continue;
    const s = bdSum(days, a, b);
    weeks.push({ start, end, s, w, fest: fest25.filter(([d]) => d >= start && d <= end).map(([, n]) => n) });
  }
  const base = weeks.slice(0, 2).map((x) => x.s.spend / 7), baseDaily = base.length ? base.reduce((t, v) => t + v, 0) / base.length : null;
  const peak = weeks.reduce((m, x) => (x.s.spend > (m ? m.s.spend : 0) ? x : m), null);
  const m25 = (k) => { const m = SL.data && SL.data.months[k]; return m && m.ot ? Object.values(m.ot).reduce((t, r) => t + (r[0] || 0), 0) : null; };
  const oct = m25('2025-10'), nov = m25('2025-11'), sep = m25('2025-09');
  const yi = ENGINE.idx(bdLastFull()), now = bdSum(days, yi - 13, yi), nowDaily = now.spend / 14;
  const ramp = baseDaily && peak ? Math.min(3, Math.max(1.2, peak.s.spend / 7 / baseDaily)) : 1.8;
  const coins = (BD.catalog ? BD.catalog.products : []).filter((p) => /coin/i.test(p.name)).slice(0, 2);
  const plan = [
    ['28 Sep to 11 Oct', 'Get ready', 1, 'Make the festive creative now: 3 to 4 ads each for the top 5 sellers, a gold and silver coin ad for Dhanteras, and a "gift for her" set for Karwa Chauth. Relaunch 2 or 3 of last year\'s festive winners.'],
    ['12 Oct to 25 Oct', 'Warm up', Math.round((1 + (ramp - 1) * 0.4) * 10) / 10, 'Test the new ads at small budgets. Keep the 2 best per product. Build retargeting lists from video views and site visits.'],
    ['26 Oct to 1 Nov', 'Karwa Chauth push', Math.round((1 + (ramp - 1) * 0.7) * 10) / 10, 'Karwa Chauth is on Thu 29 Oct. Gift angle for husbands: earrings and pendants under ₹25K, delivery before the day.'],
    ['2 Nov to 8 Nov', 'Dhanteras and Diwali peak', ramp, 'Dhanteras is Fri 6 Nov and Diwali Sun 8 Nov. Coins and gold pieces lead. Raise budgets on winners 20% a day, not all at once. Watch the blended return daily.'],
    ['9 Nov to 22 Nov', 'Wedding season', Math.round((1 + (ramp - 1) * 0.5) * 10) / 10, 'Move to bridal and gifting for weddings. Pull back to normal if the blended return drops under the floor.'],
  ];
  return `<section class="panel-box bd-sec" id="bd-festive"><h2>Festive season plan</h2>
    <p class="lead">Built from last year's Meta results around Diwali 2025 and this year's dates: Karwa Chauth Thu 29 Oct, Dhanteras Fri 6 Nov, Diwali Sun 8 Nov 2026.</p>
    <div class="bd-two"><div><h3>Last year, week by week (Meta)</h3>
      ${rpBars({ labels: weeks.map((x) => shortDate(x.start)), series: [{ name: 'Ad money a day', color: 'var(--spend)', vals: weeks.map((x) => x.s.spend / 7) }], H: 180, marks: weeks.map((x) => x.fest.join(', ')),
        tips: (i) => [`Week of ${bdDay(weeks[i].start)}`, 'Ad money a day', compact(weeks[i].s.spend / 7), 'Meta ROAS', bdX(weeks[i].s.roas), 'Orders Meta counted', weeks[i].s.purch, ...(weeks[i].fest.length ? ['Festival', weeks[i].fest.join(', ')] : [])].join('|') })}
      <p class="small muted">Diwali 2025 was on 20 Oct. Peak week spend was about ${ramp.toFixed(1)} times the calm weeks before it.</p></div>
      <div><h3>Last year, website sales by month</h3><div class="rp-facts">
        <div><span class="muted small">Sep 2025</span><b>${sep === null ? '–' : compact(sep)}</b></div><div><span class="muted small">Oct 2025</span><b>${oct === null ? '–' : compact(oct)}</b></div><div><span class="muted small">Nov 2025</span><b>${nov === null ? '–' : compact(nov)}</b></div></div>
        <p class="small muted">Now spending about ${compact(nowDaily)} a day (last 14 days).${coins.length ? ` Silver coins are in your top 100 sellers (${esc(coins.map((c) => c.name).join(', '))}), a natural Dhanteras ad.` : ''}</p></div></div>
    <div class="scroll"><table class="bd-table"><tr><th>Dates</th><th>Phase</th><th class="n">Budget a day</th><th>What to do</th></tr>
      ${plan.map(([d, ph, x, what]) => `<tr><td>${esc(d)}</td><td><b>${esc(ph)}</b></td><td class="n">${compact(nowDaily * x)}<span class="muted small"> (${x.toFixed(1)}x)</span></td><td class="small">${esc(what)}</td></tr>`).join('')}</table></div>
    <p class="small muted">Budgets are a guide based on last year's ramp. Only raise them while the blended return stays above the floor. Festival dates: devaastha.com and divinehindu.in calendars.</p></section>`;
}

// ---------- page ----------
window.renderBuyer = async function renderBuyer() {
  const v = $('buyerView');
  if (!SL.data) { v.innerHTML = '<p class="loading">Loading website sales…</p>'; await loadSales(); }
  if (!BD.catalog) { try { const r = await fetch('catalog.json'); BD.catalog = r.ok ? await r.json() : null; } catch (e) { BD.catalog = null; } }
  const safe = (f) => { try { return f(); } catch (e) { return `<section class="panel-box"><p class="bad-text small">This part could not be built: ${esc(e.message)}</p></section>`; } };
  v.innerHTML = `<div class="ins bd">
    <nav class="bd-nav" aria-label="Sections">${BD_SECTIONS.map(([id, l]) => `<a href="#${id}" data-bdjump="${id}">${l}</a>`).join('')}</nav>
    ${safe(bdBrief)}${safe(bdGuard)}${safe(bdBudget)}${safe(bdRelaunch)}${safe(bdAudience)}${safe(bdCoverage)}${safe(bdCheckup)}${safe(bdFestive)}
    <p class="small muted">Everything here is a suggestion from the data. This page never changes the ad account.</p></div>`;
};
document.addEventListener('click', async (e) => {
  const v = $('buyerView');
  if (!v || v.hidden || !v.contains(e.target)) return;
  const b = (s) => e.target.closest(s);
  let x;
  if ((x = b('[data-bdjump]'))) { e.preventDefault(); const el = $(x.dataset.bdjump); if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' }); return; }
  if ((x = b('[data-bdopen]'))) { openSide(x.dataset.bdopen); return; }
  if ((x = b('[data-bdrelaunchall]'))) { BD.relaunchAll = true; window.renderBuyer(); return; }
  if ((x = b('[data-bdcov]'))) { BD.covFmt = x.dataset.bdcov; const y = window.scrollY; await window.renderBuyer(); window.scrollTo(0, y); return; }
  const copy = async (text, btn) => { try { await navigator.clipboard.writeText(text); btn.textContent = 'Copied'; } catch (err) { btn.textContent = 'Copy blocked here'; } };
  if ((x = b('[data-bdcopy]'))) { copy(x.dataset.bdcopy === 'brief' ? BD.briefText : BD.budgetText, x); return; }
  if ((x = b('[data-bdcopytext]'))) copy(x.dataset.bdcopytext, x);
});
