'use strict';
// Account health: 5 checks a media buyer runs every week.
//   Tracking   does Meta see every website order, and how well it matches buyers
//   Fatigue    which live ads are tiring, and when, with a backup queue
//   Changes    every change made in Ads Manager, with results 7 days before and after
//   Structure  live ad sets, learning status and ad sets that compete with each other
//   Creative DNA  what the best selling designs have in common
// Data files (all read-only pulls from Meta): tracking.json, freq.json, changes.json, structure.json,
// creativedna.json, metainsights.json. A file that is missing hides its section; nothing shows as zero.
// Uses: DATA, VIEW, ENGINE, esc, money, compact, shortDate, addDays, $, thumbHtml, copyBtn, isSaleAd,
// isSaleCampaign, SL, loadSales, bdLastFull (buyer.js).

const HL = { sec: 'tracking', files: null, chKind: 'all', chShow: 30, dnaSale: false };
try { const s = localStorage.getItem('health-sec'); if (s) HL.sec = s; } catch (e) { /* storage unavailable */ }
const HL_SECS = [['tracking', 'Tracking'], ['fatigue', 'Ad fatigue'], ['changes', 'Changes'], ['structure', 'Structure'], ['dna', 'Creative DNA']];
const hlX = (v) => (v === null || v === undefined || !Number.isFinite(v) ? 'no sales' : v.toFixed(2) + 'x');
const hlPct = (v, d = 0) => (v === null || v === undefined || !Number.isFinite(v) ? 'unavailable' : (v * 100).toFixed(d) + '%');
const hlNum = (v) => (v === null || v === undefined || !Number.isFinite(v) ? 'unavailable' : Number(v).toLocaleString('en-IN'));
const hlSales = (n) => `${n} sale${n === 1 ? '' : 's'}`;
const hlChip = (tone, text) => `<span class="hl-chip hl-${tone}">${esc(text)}</span>`;

async function hlBoot() {
  if (HL.files) return;
  const get = async (f) => { try { const r = await fetch(f); return r.ok ? await r.json() : null; } catch (e) { return null; } };
  const names = ['tracking', 'freq', 'changes', 'structure', 'creativedna', 'metainsights'];
  const got = await Promise.all(names.map((n) => get(n + '.json')));
  const F = {};
  names.forEach((n, i) => { F[n] = got[i]; });
  // shape guards: a server may answer {} for a file it does not have
  if (!(F.tracking && Array.isArray(F.tracking.purchase_days))) F.tracking = null;
  if (!(F.freq && F.freq.ads && Array.isArray(F.freq.weeks))) F.freq = null;
  if (!(F.changes && Array.isArray(F.changes.changes))) F.changes = null;
  if (!(F.structure && Array.isArray(F.structure.adsets))) F.structure = null;
  if (!(F.creativedna && F.creativedna.tags)) F.creativedna = null;
  if (!(F.metainsights && (F.metainsights.dataset || F.metainsights.opportunity))) F.metainsights = null;
  HL.files = F;
}

// ---------- ad groups from ids ----------
function hlAdsOf(level, id) {
  const out = [];
  for (const [aid, ad] of Object.entries(DATA.ads)) {
    if ((level === 'ad' && aid === id) || (level === 'adset' && ad.adset_id === id) || (level === 'campaign' && ad.campaign_id === id)) out.push(aid);
  }
  return out;
}
function hlSum(ids, a, b) {
  let spend = 0, purch = 0, value = 0, impr = 0, clicks = 0, hasV = false;
  for (const id of ids) {
    const m = ENGINE.sums(id, a, b);
    spend += m.spend; impr += m.impressions || 0; clicks += m.link_clicks || 0;
    purch += m.purchases || 0;
    if (m.purchase_value !== null) { value += m.purchase_value; hasV = true; }
  }
  return { spend, purch, value, impr, clicks, roas: spend && hasV ? value / spend : null, cpa: purch ? spend / purch : null, ctr: impr ? clicks / impr : null };
}

// =============== 1. TRACKING ===============
function hlTracking() {
  const T = HL.files.tracking, MI = HL.files.metainsights;
  if (!T) return '<p class="muted">Tracking data is not available yet.</p>';
  const rows = T.purchase_days.map(([d, web, srv]) => {
    const x = SL.data && SL.data.daily ? SL.data.daily[d] : null;
    const orders = x && x.orders !== null && x.orders !== undefined ? x.orders : null;
    return { d, web, srv, meta: Math.max(web || 0, srv || 0), orders };
  });
  const both = rows.filter((r) => r.orders !== null);
  const sumO = both.reduce((t, r) => t + r.orders, 0), sumM = both.reduce((t, r) => t + r.meta, 0);
  const cover = sumO ? Math.min(1, sumM / sumO) : null;
  const sumW = rows.reduce((t, r) => t + (r.web || 0), 0), sumS = rows.reduce((t, r) => t + (r.srv || 0), 0);
  const ev = MI && MI.dataset ? MI.dataset.events || [] : [];
  const pur = ev.find((e) => e.event === 'Purchase'), vc = ev.find((e) => e.event === 'ViewContent');
  const noEmail = ev.length && ev.every((e) => !e.coverage || !e.coverage.email);
  const alerts = [];
  for (const r of both) {
    if (r.orders >= 5 && r.meta < r.orders * 0.5) alerts.push({ sev: 3, text: `${shortDate(r.d)}: ${r.orders} website orders, Meta saw ${r.meta}. Check for bulk or offline orders that day; if not, the purchase event missed them.` });
  }
  for (const r of rows) {
    if (r.web && r.srv < r.web) alerts.push({ sev: 2, text: `${shortDate(r.d)}: the server sent ${r.srv} purchases, the browser ${r.web}. The server copy should never be lower.` });
  }
  const F = T.funnel;
  let funnel = '';
  if (F) {
    const steps = [['PageView', 'Page views'], ['ViewContent', 'Product views'], ['AddToCart', 'Add to cart'], ['InitiateCheckout', 'Checkout started'], ['AddPaymentInfo', 'Payment details'], ['Purchase', 'Purchases']].filter(([k]) => F[k] !== undefined);
    const flags = [];
    if (F.ViewContent && F.PageView && F.ViewContent > F.PageView) flags.push(`Product views fire ${(F.ViewContent / F.PageView).toFixed(1)} times per page view. That is not possible for real views: the event likely fires on every product card or on scroll. It floods Meta with weak signals.`);
    if (F.AddPaymentInfo && F.Purchase && F.Purchase / F.AddPaymentInfo < 0.4) flags.push(`Only ${hlPct(F.Purchase / F.AddPaymentInfo)} of people who add payment details end with a purchase event. Check failed payments, and check the purchase event fires on the thank you page for every payment method.`);
    funnel = `<section class="panel-box hl-sec"><h3>Website funnel as Meta sees it <span class="muted small">${esc(F.window || '')}</span></h3>
      <div class="hl-funnel">${steps.map(([k, l], i) => { const prev = i ? F[steps[i - 1][0]] : null; return `<div><b>${hlNum(F[k])}</b><span>${esc(l)}</span>${prev ? `<em>${hlPct(F[k] / prev, F[k] / prev < 0.1 ? 1 : 0)} of the step before</em>` : ''}</div>`; }).join('')}</div>
      ${flags.map((f) => `<p class="hl-flag">${esc(f)}</p>`).join('')}</section>`;
  }
  // daily chart: orders (bars) and Meta purchases (dots)
  const W = 720, H = 180, L = 30, B = 22, max = Math.max(1, ...rows.map((r) => Math.max(r.orders || 0, r.meta))), n = rows.length, bw = (W - L - 8) / n;
  const y = (v) => H - B - (v / max) * (H - B - 10);
  const chart = `<svg class="rp-chart" viewBox="0 0 ${W} ${H}" role="img" aria-label="Website orders and Meta purchases per day">
    <line x1="${L}" y1="${H - B}" x2="${W}" y2="${H - B}" stroke="var(--line)"/>
    ${rows.map((r, i) => { const x = L + i * bw; const tip = esc([shortDate(r.d), 'Website orders', r.orders === null ? 'Not available' : r.orders, 'Meta purchases', r.meta, 'Browser', r.web, 'Server', r.srv].join('|'));
      return `${r.orders !== null ? `<rect x="${(x + bw * 0.15).toFixed(1)}" y="${y(r.orders).toFixed(1)}" width="${(bw * 0.7).toFixed(1)}" height="${(H - B - y(r.orders)).toFixed(1)}" rx="2" fill="var(--sunken)" stroke="var(--line)"/>` : ''}
        <circle cx="${(x + bw / 2).toFixed(1)}" cy="${y(r.meta).toFixed(1)}" r="4" fill="var(--accent, #d4a017)"/>
        <rect x="${x.toFixed(1)}" y="0" width="${bw.toFixed(1)}" height="${H}" fill="transparent" data-tip="${tip}"/>
        ${i % 4 === 0 ? `<text x="${(x + bw / 2).toFixed(1)}" y="${H - 6}" font-size="10" text-anchor="middle" fill="var(--muted)">${esc(shortDate(r.d))}</text>` : ''}`; }).join('')}
    <text x="4" y="14" font-size="10" fill="var(--muted)">${max}</text></svg>`;
  const fixes = [
    ...(cover !== null && cover < 0.9 ? ['Fire Purchase on the order confirmation page for every payment method, including cash on delivery and bank transfer.'] : []),
    ...(noEmail ? ['Send the shopper\'s email (hashed) with every event, from the browser and the server.'] : []),
    ...(pur && pur.coverage && pur.coverage.fbc < 60 ? [`Save the fbclid from the landing URL in a first party cookie and send it as fbc with server events (now ${pur.coverage.fbc}% of purchases have it).`] : []),
    ...(F && F.ViewContent > F.PageView ? ['Fire ViewContent once per product page load, not per product card.'] : []),
    'Use the same event_id in the browser and server event so Meta counts each order once.',
  ];
  const fixText = ['Tracking fixes for the web developer:', ...fixes.map((f, i) => `${i + 1}. ${f}`)].join('\n');
  const tone = cover === null ? 'grey' : cover >= 0.9 ? 'good' : cover >= 0.7 ? 'warn' : 'bad';
  return `<div class="hl-kpis">
      <div class="hl-kpi"><span>Orders Meta sees</span><b>${hlPct(cover)}</b><em>${sumM} of ${sumO} website orders, ${esc(shortDate(rows[0].d))} to ${esc(shortDate(rows[rows.length - 1].d))}</em>${hlChip(tone, tone === 'good' ? 'Good' : tone === 'warn' ? 'Watch' : tone === 'bad' ? 'Fix' : 'Unavailable')}</div>
      <div class="hl-kpi"><span>Server vs browser</span><b>${sumW ? hlPct(sumS / sumW) : 'unavailable'}</b><em>${sumS} server and ${sumW} browser purchase events</em>${hlChip(sumW && sumS >= sumW * 0.95 ? 'good' : 'warn', sumW && sumS >= sumW * 0.95 ? 'Both on' : 'Gaps')}</div>
      <div class="hl-kpi"><span>Purchase match quality</span><b>${pur ? pur.emq + ' of 10' : 'unavailable'}</b><em>Meta's score for tying a purchase to a person</em>${pur ? hlChip(pur.emq >= 8 ? 'good' : pur.emq >= 6 ? 'warn' : 'bad', pur.emq >= 8 ? 'Great' : pur.emq >= 6 ? 'OK' : 'Poor') : ''}</div>
      <div class="hl-kpi"><span>Click ID on purchases</span><b>${pur && pur.coverage ? pur.coverage.fbc + '%' : 'unavailable'}</b><em>Email sent: ${noEmail ? 'never' : 'yes'}${vc ? ` · product view match ${vc.emq} of 10` : ''}</em>${pur && pur.coverage ? hlChip(pur.coverage.fbc >= 60 ? 'good' : 'bad', pur.coverage.fbc >= 60 ? 'Good' : 'Fix') : ''}</div>
    </div>
    <section class="panel-box hl-sec"><h3>Website orders vs purchases Meta received</h3>${chart}
      ${rpLegendSafe([['var(--sunken)', 'Website orders'], ['var(--accent, #d4a017)', 'Purchases Meta received']])}
      <p class="small muted">Meta can never see every order: bulk, phone and store orders skip the website checkout. Below 70% on normal days means the event is missing real orders.</p></section>
    ${alerts.length ? `<section class="panel-box hl-sec"><h3>Days to check (${alerts.length})</h3><ul class="bd-alerts">${alerts.slice(0, 8).map((a) => `<li class="sev${a.sev}">${esc(a.text)}</li>`).join('')}</ul></section>` : ''}
    ${funnel}
    <section class="panel-box hl-sec"><div class="bd-head"><h3>Fix list for the web developer</h3>${copyBtn(fixText)}</div><ol class="mv-do">${fixes.map((f) => `<li>${esc(f)}</li>`).join('')}</ol>
      <p class="small muted">Pixel counts from Meta Events Manager, checked ${esc(shortDate(T.captured_at))}. Orders from website sales. Better tracking lowers cost per sale because Meta learns from more real buyers.</p></section>`;
}
function rpLegendSafe(items) { return typeof rpLegend === 'function' ? rpLegend(items) : `<p class="small">${items.map(([c, l]) => `<span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:${c};margin-right:4px"></span>${esc(l)}`).join(' &nbsp; ')}</p>`; }

// =============== 2. FATIGUE ===============
const HL_RETARGET = /\b(atc|mof|bof|retarget|visitors?|engagers?|cart|purchasers?)\b/i;
function hlFatigueRows() {
  const end = ENGINE.idx(bdLastFull()), FQ = HL.files.freq;
  const blocks = [0, 1, 2, 3].map((k) => [end - 27 + k * 7, end - 21 + k * 7]);
  const out = [];
  for (const [id, ad] of Object.entries(DATA.ads)) {
    if (ad.effective_status !== 'ACTIVE') continue;
    const m14 = ENGINE.sums(id, end - 13, end);
    if (m14.spend < 1500) continue;
    const bl = blocks.map(([a, b]) => ENGINE.sums(id, a, b));
    const ctrs = bl.map((m) => (m.impressions >= 2000 ? m.link_clicks / m.impressions : null));
    const valid = ctrs.filter((v) => v !== null);
    if (valid.length < 2) continue;
    const last = ctrs[3] !== null ? ctrs[3] : valid[valid.length - 1], peak = Math.max(...valid);
    const prev = ctrs[2] !== null && ctrs[3] !== null ? ctrs[2] : null;
    const wk = prev ? last / prev - 1 : null;
    const fr = FQ && FQ.ads[id] ? FQ.ads[id].map((x) => (x ? x[0] : null)) : null;
    const frLast = fr ? fr[fr.length - 1] : null, frPrev = fr ? fr[fr.length - 2] : null;
    const retarget = HL_RETARGET.test(ad.adset_name || '') || HL_RETARGET.test(ad.campaign_name || '');
    const frCap = retarget ? 6 : 3.5, drop = peak ? 1 - last / peak : 0;
    let days = null;
    if (drop >= 0.3 || (frLast !== null && frLast >= frCap)) days = 0;
    else {
      const cand = [];
      if (wk !== null && wk < -0.02) cand.push(Math.log((0.7 * peak) / last) / Math.log(1 + wk) * 7);
      if (frLast !== null && frPrev !== null && frLast > frPrev) cand.push((frCap - frLast) / (frLast - frPrev) * 7);
      days = cand.length ? Math.max(1, Math.round(Math.min(...cand))) : null;
    }
    const status = days === 0 ? 'Tired now' : days !== null && days <= 7 ? 'Tires this week' : days !== null && days <= 21 ? `About ${days} days left` : 'Healthy';
    out.push({ id, ad, m14, ctrs, last, peak, drop, wk, fr, frLast, retarget, days, status, sale: isSaleAd(ad) });
  }
  const order = (r) => (r.days === 0 ? 0 : r.days !== null && r.days <= 7 ? 1 : r.days !== null && r.days <= 21 ? 2 : 3);
  return out.sort((a, b) => order(a) - order(b) || b.m14.spend - a.m14.spend);
}
function hlFatigue() {
  const rows = hlFatigueRows();
  if (!rows.length) return '<p class="muted">No live ad spent enough in the last 14 days to judge.</p>';
  const tot = rows.reduce((t, r) => t + r.m14.spend, 0);
  const queue = rows.filter((r) => r.days !== null && r.days <= 14 && !r.sale).slice(0, REC_CAP);
  const tone = (r) => (r.days === 0 ? 'bad' : r.days !== null && r.days <= 7 ? 'bad' : r.days !== null && r.days <= 21 ? 'warn' : 'good');
  const spark = (v) => { const ok = v.filter((x) => x !== null); if (ok.length < 2) return ''; const mx = Math.max(...ok), mn = Math.min(...ok); return `<svg class="hl-spark" viewBox="0 0 60 18" aria-hidden="true"><polyline fill="none" stroke="currentColor" stroke-width="1.8" points="${v.map((x, i) => (x === null ? null : `${(i * 20).toFixed(0)},${(16 - ((x - mn) / ((mx - mn) || 1)) * 14).toFixed(1)}`)).filter(Boolean).join(' ')}"/></svg>`; };
  const brief = (r) => [`Backup for "${r.ad.name}" (ad ID ${r.id})`, `Why: ${r.status.toLowerCase()}. Click rate ${hlPct(r.last, 2)}, ${hlPct(r.drop)} below its best week.${r.frLast !== null ? ` People saw it ${r.frLast} times last week.` : ''}`,
    'Keep: the same product and the same offer.', 'Change: the first frame or image, and the first line of text.', 'Make 2 versions. Launch them in the same ad set at 10 to 15% of its budget.'].join('\n');
  return `<div class="hl-kpis">
      <div class="hl-kpi"><span>Tired now</span><b>${rows.filter((r) => r.days === 0).length}</b><em>of ${rows.length} live ads with real spend</em></div>
      <div class="hl-kpi"><span>Tire within 2 weeks</span><b>${rows.filter((r) => r.days && r.days <= 14).length}</b><em>build backups now</em></div>
      <div class="hl-kpi"><span>Spend on tired ads</span><b>${hlPct(rows.filter((r) => r.days === 0).reduce((t, r) => t + r.m14.spend, 0) / tot)}</b><em>of the last 14 days</em></div>
    </div>
    ${queue.length ? `<section class="panel-box hl-sec"><div class="bd-head"><h3>Backup queue for the creative team</h3>${copyBtn(queue.map(brief).join('\n\n'))}</div>
      <ol class="hl-queue">${queue.map((r) => `<li><button class="linkbtn" type="button" data-open="${esc(r.id)}">${esc(r.ad.name)}</button> ${hlChip(tone(r), r.status)} <span class="muted small">${compact(r.m14.spend)} in 14 days · ${esc(r.ad.creative.type_label || '')}</span> ${copyBtn(brief(r))}</li>`).join('')}</ol>
      <p class="small muted">Sale ads are left out: they stop with the sale.</p></section>` : ''}
    <section class="panel-box hl-sec"><h3>Every live ad with real spend</h3><div class="scroll"><table class="bd-table">
      <tr><th>Ad</th><th>Forecast</th><th class="n">Spend 14 days</th><th class="n">ROAS</th><th>Click rate, 4 weeks</th><th class="n">Now vs best</th><th class="n">Seen per person last week</th></tr>
      ${rows.map((r) => `<tr><td><button class="linkbtn" type="button" data-open="${esc(r.id)}">${esc(r.ad.name)}</button>${r.retarget ? ' <span class="muted small">past visitors</span>' : ''}${r.sale ? ' <span class="chip sale">Sale</span>' : ''}</td>
        <td>${hlChip(tone(r), r.status)}</td><td class="n">${compact(r.m14.spend)}</td><td class="n">${hlX(r.m14.roas)}</td><td>${spark(r.ctrs)} ${hlPct(r.last, 2)}</td>
        <td class="n">${r.drop > 0.005 ? '−' + hlPct(r.drop) : 'at best'}</td><td class="n">${r.frLast !== null ? r.frLast.toFixed(1) : 'unavailable'}</td></tr>`).join('')}
    </table></div>
    <p class="small muted">An ad counts as tired when its click rate is 30% below its best week, or people see it more than ${3.5} times a week (6 for past visitor ads). The forecast extends the last week's trend. Click rate needs 2,000 views a week to count.</p></section>`;
}

// =============== 3. CHANGES ===============
function hlChangeRows() {
  const C = HL.files.changes;
  if (!C) return [];
  const last = ENGINE.idx(DATA.meta.window.until), first = ENGINE.idx(DATA.meta.window.since);
  const campOf = {}, adsetOf = {};
  for (const ad of Object.values(DATA.ads)) { campOf[ad.campaign_id] = ad.campaign_name; adsetOf[ad.adset_id] = ad.campaign_id; }
  const adCamp = (id) => (DATA.ads[id] ? DATA.ads[id].campaign_id : null);
  // group many ad level events on the same day and campaign into 1 row
  const groups = new Map();
  for (const c of C.changes) {
    const camp = c.level === 'campaign' ? c.id : c.level === 'adset' ? adsetOf[c.id] : adCamp(c.id);
    const key = c.level === 'ad' ? [c.day, c.kind, c.text, camp || c.name].join('|') : [c.at, c.id, c.kind, c.text].join('|');
    const g = groups.get(key) || { ...c, ids: [], camp, n: 0 };
    g.ids.push(c.id); g.n += 1; groups.set(key, g);
  }
  const out = [];
  for (const g of groups.values()) {
    const ids = [...new Set(g.ids.flatMap((id) => hlAdsOf(g.level, id)))];
    const d = ENGINE.idx(g.day);
    let before = null, after = null, verdict = 'Not in the ads data', afterDays = 0;
    if (ids.length && d > first) {
      before = hlSum(ids, Math.max(first, d - 7), d - 1);
      afterDays = Math.max(0, Math.min(7, last - d));
      after = afterDays ? hlSum(ids, d + 1, d + afterDays) : null;
      if (afterDays < 3) verdict = 'Too early';
      else if (!before.spend && after && after.spend) verdict = 'New spend';
      else if (after && before.spend) {
        const rb = before.roas || 0, ra = after.roas || 0, perDayB = before.spend / 7, perDayA = after.spend / afterDays;
        if (g.kind === 'status' && /paused|inactive/i.test(g.text.split(' to ')[1] || '')) verdict = after.spend < before.spend * 0.2 ? 'Stopped as planned' : 'Still spending';
        else if (ra >= rb * 1.1 && (after.purch / afterDays) >= (before.purch / 7) * 0.9) verdict = 'Helped';
        else if (ra <= rb * 0.85 || (perDayA > perDayB * 1.1 && after.purch / afterDays < before.purch / 7)) verdict = 'Hurt';
        else verdict = 'No clear change';
      }
    }
    out.push({ ...g, campName: campOf[g.camp] || g.name, before, after, afterDays, verdict });
  }
  return out.sort((a, b) => (a.at < b.at ? 1 : -1));
}
function hlChanges() {
  const C = HL.files.changes;
  if (!C) return '<p class="muted">The change history is not available yet.</p>';
  const all = hlChangeRows();
  const kinds = [['all', 'All'], ['budget', 'Budget'], ['status', 'On and off'], ['targeting', 'Audience'], ['created', 'New']];
  const list = all.filter((r) => HL.chKind === 'all' || r.kind === HL.chKind);
  const tally = (k) => { const l = all.filter((r) => r.kind === k && r.by === 'Team'); return { n: l.length, help: l.filter((r) => r.verdict === 'Helped').length, hurt: l.filter((r) => r.verdict === 'Hurt').length }; };
  const bud = tally('budget'), raises = all.filter((r) => r.kind === 'budget' && r.new > r.old), cuts = all.filter((r) => r.kind === 'budget' && r.new < r.old);
  const vt = { Helped: 'good', Hurt: 'bad', 'No clear change': 'grey', 'Too early': 'grey', 'New spend': 'grey', 'Stopped as planned': 'good', 'Still spending': 'warn', 'Not in the ads data': 'grey' };
  const cell = (m) => (m ? `${compact(m.spend)} · ${hlSales(m.purch)}${m.purch ? ' · ' + hlX(m.roas) : ''}` : '–');
  const lesson = [];
  const rh = raises.filter((r) => r.verdict === 'Helped').length, rhu = raises.filter((r) => r.verdict === 'Hurt').length;
  if (raises.length >= 3) {
    const big = raises.filter((r) => r.old && r.new / r.old > 1.3), bigHurt = big.filter((r) => r.verdict === 'Hurt').length;
    lesson.push(`${raises.length} budget raises: ${rh} helped, ${rhu} hurt.${big.length ? ` Raises above 30% at once hurt ${bigHurt} of ${big.length} times.` : ''}`);
  }
  if (cuts.length) lesson.push(`${cuts.length} budget cuts: ${cuts.filter((r) => r.verdict === 'Helped').length} lifted ROAS.`);
  const tg = all.filter((r) => r.kind === 'targeting');
  if (tg.length) lesson.push(`${tg.length} audience edits. Each one restarts learning, so batch them.`);
  return `<div class="hl-kpis">
      <div class="hl-kpi"><span>Changes by the team</span><b>${all.filter((r) => r.by === 'Team').length}</b><em>${esc(shortDate(C.since))} to ${esc(shortDate(C.until))}</em></div>
      <div class="hl-kpi"><span>Budget moves</span><b>${bud.n}</b><em>${bud.help} helped, ${bud.hurt} hurt</em></div>
      <div class="hl-kpi"><span>Made by Meta</span><b>${all.filter((r) => r.by === 'Meta').length}</b><em>automatic changes</em></div>
    </div>
    ${lesson.length ? `<section class="panel-box hl-sec"><h3>What the history says</h3><ul>${lesson.map((l) => `<li>${esc(l)}</li>`).join('')}</ul></section>` : ''}
    <section class="panel-box hl-sec"><div class="bd-head"><h3>Change log</h3><div class="seg" role="group" aria-label="Kind">${kinds.map(([k, l]) => `<button type="button" data-hlkind="${k}" aria-pressed="${HL.chKind === k}">${esc(l)}</button>`).join('')}</div></div>
    <div class="scroll"><table class="bd-table"><tr><th>When</th><th>What</th><th>Where</th><th>7 days before</th><th>After</th><th>Result</th></tr>
      ${list.slice(0, HL.chShow).map((r) => `<tr><td class="small">${esc(shortDate(r.day))}${r.by === 'Meta' ? '<br><span class="muted">by Meta</span>' : ''}</td>
        <td>${esc(r.n > 1 ? `${r.n} ads: ${r.text}` : r.text)}</td><td class="small">${esc(r.level === 'campaign' ? r.name : `${r.name} (${r.campName || ''})`)}</td>
        <td class="small">${cell(r.before)}</td><td class="small">${r.after ? cell(r.after) + (r.afterDays < 7 ? ` <span class="muted">(${r.afterDays} days)</span>` : '') : '–'}</td><td>${hlChip(vt[r.verdict] || 'grey', r.verdict)}</td></tr>`).join('')}
    </table></div>
    ${list.length > HL.chShow ? `<button class="btn ghost" type="button" data-hlmore>Show ${Math.min(30, list.length - HL.chShow)} more</button>` : ''}
    <p class="small muted">From Ads Manager history. Results compare the 7 days before with up to 7 days after, for the ads under what changed. Other changes in the same days also move results, so read this as a hint, not proof. Status approvals by ad review are left out.</p></section>`;
}

// =============== 4. STRUCTURE ===============
function hlStructure() {
  const S = HL.files.structure;
  if (!S) return '<p class="muted">Ad set details are not available yet.</p>';
  const A = S.adsets, camps = new Map();
  for (const a of A) { const k = a.campaign || 'New campaign (not in the ads data yet)'; if (!camps.has(k)) camps.set(k, []); camps.get(k).push(a); }
  const lt = { 'Learning limited': 'bad', Learning: 'warn', 'Active (learned)': 'good', 'Not delivering yet': 'grey' };
  const limited = A.filter((a) => a.learning === 'Learning limited'), learning = A.filter((a) => a.learning === 'Learning'), learned = A.filter((a) => a.learning === 'Active (learned)');
  const findings = [];
  if (limited.length) findings.push({ tone: 'bad', text: `${limited.length} ad sets are learning limited: they get too few sales a week for Meta to learn (it needs about 50). Merge them so each gets more sales.`, who: limited.map((a) => a.name) });
  const split = [...camps.entries()].filter(([, l]) => l.length >= 3 && l.every((a) => a.advantage_audience));
  if (split.length) findings.push({ tone: 'warn', text: `${split.length} campaign${split.length > 1 ? 's split' : ' splits'} the same ads across ${split.map(([, l]) => l.length).join(', ')} audiences, all with Advantage+ audience on. Advantage+ already widens each audience, so they compete with each other. Merge into 1 broad ad set per campaign.`, who: split.map(([k]) => k) });
  const saleLive = A.filter((a) => a.campaign && isSaleCampaign(a.campaign));
  if (saleLive.length) findings.push({ tone: 'bad', text: `${saleLive.length} sale ad set${saleLive.length > 1 ? 's are' : ' is'} still on after the sale ended.`, who: saleLive.map((a) => `${a.name} (${a.campaign})`) });
  const retarget = A.filter((a) => a.audience === 'Past visitors'), rtNames = new Map();
  for (const a of retarget) for (const c of a.custom) rtNames.set(c, (rtNames.get(c) || 0) + 1);
  const dup = [...rtNames.entries()].filter(([, n]) => n > 1);
  if (dup.length) findings.push({ tone: 'warn', text: `The same past visitor audience runs in more than 1 ad set: ${dup.map(([c, n]) => `${c} (${n})`).join(', ')}. They bid against each other for the same people.`, who: [] });
  const goals = A.reduce((g, a) => { g[a.goal] = (g[a.goal] || 0) + 1; return g; }, {});
  if (goals['Most sales'] && goals['Most value']) findings.push({ tone: 'grey', text: `${goals['Most sales']} ad sets aim for most sales, ${goals['Most value']} for most value. Meta suggests most value for higher ROAS; value rules work with both.`, who: [] });
  const noExcl = A.filter((a) => a.audience !== 'Past visitors' && !a.excluded.length && a.spend > 0);
  if (noExcl.length >= 3) findings.push({ tone: 'grey', text: `${noExcl.length} prospecting ad sets do not exclude past buyers, so some spend goes to people who already bought.`, who: [] });
  const plan = ['Prospecting: 1 campaign, 1 broad ad set with Advantage+ audience, most value goal, value rules on. Put new winning ads here.',
    'Testing: 1 small campaign (10 to 15% of budget) where new ads prove themselves for 7 days before moving to prospecting.',
    'Past visitors: 1 campaign with 1 ad set (site visitors and add to cart, 180 days), past buyers excluded.',
    'Sales: a separate campaign that runs only during the sale, then goes off.'];
  const planText = ['Suggested account setup:', ...plan.map((p, i) => `${i + 1}. ${p}`), '', 'Findings:', ...findings.map((f) => '- ' + f.text)].join('\n');
  return `<div class="hl-kpis">
      <div class="hl-kpi"><span>Live ad sets</span><b>${A.length}</b><em>in ${camps.size} campaigns</em></div>
      <div class="hl-kpi"><span>Learned</span><b>${learned.length}</b><em>out of learning, stable</em></div>
      <div class="hl-kpi"><span>Still learning</span><b>${learning.length}</b><em>results jump around</em></div>
      <div class="hl-kpi"><span>Learning limited</span><b>${limited.length}</b><em>too few sales to learn</em>${limited.length ? hlChip('bad', 'Fix') : ''}</div>
    </div>
    ${findings.length ? `<section class="panel-box hl-sec"><h3>What to fix</h3><ul class="hl-find">${findings.map((f) => `<li>${hlChip(f.tone, f.tone === 'bad' ? 'Fix' : f.tone === 'warn' ? 'Watch' : 'Note')} ${esc(f.text)}${f.who.length ? `<br><span class="muted small">${esc(f.who.slice(0, 6).join('; '))}${f.who.length > 6 ? ' and more' : ''}</span>` : ''}</li>`).join('')}</ul></section>` : ''}
    <section class="panel-box hl-sec"><div class="bd-head"><h3>Suggested setup</h3>${copyBtn(planText)}</div><ol class="mv-do">${plan.map((p) => `<li>${esc(p)}</li>`).join('')}</ol></section>
    <section class="panel-box hl-sec"><h3>Live ad sets by campaign <span class="muted small">${esc(S.window || '')}</span></h3>
      ${[...camps.entries()].map(([k, l]) => `<div class="hl-camp"><h4>${esc(k)} ${isSaleCampaign(k) ? '<span class="chip sale">Sale</span>' : ''}</h4><div class="scroll"><table class="bd-table">
        <tr><th>Ad set</th><th>Who</th><th>Goal</th><th>Learning</th><th class="n">Spend</th><th class="n">Sales</th><th class="n">ROAS</th><th class="n">Seen per person</th></tr>
        ${l.map((a) => `<tr><td>${esc(a.name)}</td><td class="small">${esc(a.audience)}${a.gender !== 'All' ? ', ' + esc(a.gender.toLowerCase()) : ''}${a.advantage_audience ? ' · Advantage+' : ''}${a.interests.length ? `<br><span class="muted">${esc(a.interests.slice(0, 3).join(', '))}</span>` : ''}${a.custom.length ? `<br><span class="muted">${esc(a.custom[0])}</span>` : ''}</td>
          <td class="small">${esc(a.goal || '')}</td><td>${hlChip(lt[a.learning] || 'grey', a.learning)}${a.conversions !== null && a.conversions !== undefined ? ` <span class="muted small">${a.conversions} sales</span>` : ''}</td>
          <td class="n">${compact(a.spend)}</td><td class="n">${a.purchases}</td><td class="n">${hlX(a.spend && a.value ? a.value / a.spend : null)}</td><td class="n">${a.frequency ? a.frequency.toFixed(1) : 'unavailable'}</td></tr>`).join('')}
      </table></div></div>`).join('')}
      <p class="small muted">Live ad sets from Ads Manager, checked ${esc(shortDate(S.captured_at))}. Learning status is Meta's.</p></section>`;
}

// =============== 5. CREATIVE DNA ===============
function hlCreativeKey(c) { return c ? c.image_hash || 'creative_' + c.id : null; }
function hlDna() {
  const D = HL.files.creativedna;
  if (!D) return '<p class="muted">Creative tags are not available yet.</p>';
  const a = ENGINE.idx(VIEW.range.since), b = ENGINE.idx(VIEW.range.until);
  const tagged = [], untagged = { spend: 0 };
  let total = 0;
  for (const [id, ad] of Object.entries(DATA.ads)) {
    if (!HL.dnaSale && isSaleAd(ad)) continue;
    const m = ENGINE.sums(id, a, b);
    if (m.spend <= 0) continue;
    total += m.spend;
    const t = D.tags[hlCreativeKey(ad.creative)];
    if (t) tagged.push({ id, ad, m, t }); else untagged.spend += m.spend;
  }
  if (!tagged.length) return '<p class="muted">No tagged design spent in these dates. Try the last 365 days.</p>';
  const tagSpend = tagged.reduce((s, x) => s + x.m.spend, 0);
  const allM = tagged.reduce((s, x) => ({ spend: s.spend + x.m.spend, value: s.value + (x.m.purchase_value || 0), purch: s.purch + (x.m.purchases || 0) }), { spend: 0, value: 0, purch: 0 });
  const R = allM.spend ? allM.value / allM.spend : null;
  const dims = [['scene', 'What the image shows'], ['msg', 'Message on the image'], ['palette', 'Colours'], ['band', 'Trust strip']];
  const group = (fn) => {
    const g = {};
    for (const x of tagged) { const k = fn(x.t); const r = g[k] || (g[k] = { k, spend: 0, value: 0, purch: 0, n: 0, ads: [] }); r.spend += x.m.spend; r.value += x.m.purchase_value || 0; r.purch += x.m.purchases || 0; r.n += 1; r.ads.push(x); }
    return Object.values(g).map((r) => ({ ...r, roas: r.spend ? r.value / r.spend : null, share: r.spend / tagSpend })).sort((p, q) => (q.roas || 0) - (p.roas || 0));
  };
  const label = (dim, k) => (D.labels[dim] || {})[String(k)] || String(k);
  const winners = [];
  const tables = dims.map(([dim, title]) => {
    const rows = group((t) => t[dim]);
    const best = rows.filter((r) => r.purch >= 3 && r.share >= 0.05)[0];
    if (best && R && best.roas >= R * 1.15) winners.push({ dim, k: best.k, r: best });
    const mx = Math.max(...rows.map((r) => r.roas || 0), R || 0) || 1;
    return `<div class="hl-dna"><h4>${esc(title)}</h4>${rows.map((r) => `<div class="hl-dna-row${r.purch < 3 ? ' thin' : ''}"><span>${esc(label(dim, r.k))}</span>
      <span class="hl-bar"><i style="width:${(((r.roas || 0) / mx) * 100).toFixed(0)}%"></i>${R ? `<u style="left:${((R / mx) * 100).toFixed(0)}%"></u>` : ''}</span>
      <b>${r.purch ? hlX(r.roas) : 'no sales'}</b><em>${hlSales(r.purch)} · ${hlPct(r.share)} of spend</em></div>`).join('')}</div>`;
  }).join('');
  const combos = group((t) => t.scene + '|' + t.msg).filter((r) => r.purch >= 3).slice(0, 5);
  const lowCombos = group((t) => t.scene + '|' + t.msg).filter((r) => r.spend >= tagSpend * 0.05 && R && (r.roas || 0) < R * 0.7).slice(-3);
  const bestAds = (r) => { const seen = new Set(); return r.ads.slice().sort((p, q) => (q.m.purchase_value || 0) - (p.m.purchase_value || 0)).filter((x) => { const k = hlCreativeKey(x.ad.creative); if (seen.has(k)) return false; seen.add(k); return true; }).slice(0, 3); };
  const briefs = combos.slice(0, 3).map((c) => { const [s, m] = c.k.split('|'); return `${label('scene', s)} + ${label('msg', m).toLowerCase()}: ${hlX(c.roas)} on ${c.purch} sales. Model: "${bestAds(c)[0].ad.name}".`; });
  const briefText = ['Next 3 designs to brief (from Creative DNA):', ...briefs.map((x, i) => `${i + 1}. ${x}`), ...(winners.find((w) => w.dim === 'band' && w.k === true) ? ['Keep the trust strip (hallmark, returns) on every design.'] : [])].join('\n');
  return `<div class="hl-kpis">
      <div class="hl-kpi"><span>Designs tagged</span><b>${Object.keys(D.tags).length}</b><em>cover ${hlPct(tagSpend / (total || 1))} of spend in these dates</em></div>
      <div class="hl-kpi"><span>Tagged ROAS</span><b>${hlX(R)}</b><em>${allM.purch} sales on ${compact(allM.spend)}</em></div>
      ${winners.slice(0, 2).map((w) => `<div class="hl-kpi"><span>Wins: ${esc(dims.find((d) => d[0] === w.dim)[1].toLowerCase())}</span><b>${esc(label(w.dim, w.k))}</b><em>${hlX(w.r.roas)} vs ${hlX(R)}</em></div>`).join('')}
    </div>
    <section class="panel-box hl-sec"><div class="bd-head"><h3>What sells, by trait</h3>
      <label class="check small"><input type="checkbox" data-hldnasale ${HL.dnaSale ? 'checked' : ''}> Include sale ads</label></div>
      <div class="hl-dna-grid">${tables}</div>
      <p class="small muted">Bars show ROAS; the line marks the average of tagged designs. Faded rows have under 3 sales. Dates follow the picker at the top.</p></section>
    ${combos.length ? `<section class="panel-box hl-sec"><div class="bd-head"><h3>Best combinations</h3>${copyBtn(briefText)}</div>
      <div class="hl-combos">${combos.map((c) => { const [s, m] = c.k.split('|'); return `<div class="hl-combo"><div class="hl-thumbs">${bestAds(c).map((x) => `<button type="button" class="hl-th" data-open="${esc(x.id)}" title="${esc(x.ad.name)}">${thumbHtml(x.id, x.ad.name)}</button>`).join('')}</div>
        <b>${esc(label('scene', s))}</b><span>${esc(label('msg', m))}</span><em>${hlX(c.roas)} · ${hlSales(c.purch)} · ${c.n} ads</em></div>`; }).join('')}</div>
      ${lowCombos.length ? `<p class="small">Weak with real spend: ${esc(lowCombos.map((c) => { const [s, m] = c.k.split('|'); return `${label('scene', s).toLowerCase()} + ${label('msg', m).toLowerCase()} (${hlX(c.roas)})`; }).join('; '))}.</p>` : ''}</section>` : ''}
    <p class="small muted">${esc(D.method)} New designs need tags before they count here.</p>`;
}

// =============== page ===============
function hlStatus() {
  const F = HL.files, st = {};
  if (F.tracking && SL.data) {
    let o = 0, m = 0;
    for (const [d, w, s] of F.tracking.purchase_days) { const x = SL.data.daily[d]; if (x && x.orders !== null && x.orders !== undefined) { o += x.orders; m += Math.max(w || 0, s || 0); } }
    const c = o ? m / o : null;
    st.tracking = c === null ? ['grey', 'Unavailable'] : c >= 0.9 ? ['good', 'Good'] : c >= 0.7 ? ['warn', 'Watch'] : ['bad', `${Math.round(c * 100)}% of orders seen`];
  }
  try { const r = hlFatigueRows(), n = r.filter((x) => x.days === 0).length; st.fatigue = n ? ['bad', `${n} tired`] : r.some((x) => x.days && x.days <= 14) ? ['warn', 'Backups due'] : ['good', 'Fresh']; } catch (e) { st.fatigue = ['grey', 'Unavailable']; }
  if (F.changes) st.changes = ['grey', `${F.changes.changes.filter((c) => c.by === 'Team').length} changes`];
  if (F.structure) { const n = F.structure.adsets.filter((a) => a.learning === 'Learning limited').length; st.structure = n ? ['bad', `${n} limited`] : ['good', 'Clean']; }
  if (F.creativedna) st.dna = ['grey', `${Object.keys(F.creativedna.tags).length} tagged`];
  return st;
}
window.renderHealth = async function renderHealth() {
  const v = $('healthView');
  if (!v || !VIEW) return;
  if (!HL.files) v.innerHTML = '<p class="muted">Loading account health…</p>';
  await hlBoot();
  if (!SL.data && !SL.err) await loadSales();
  const st = hlStatus();
  const avail = HL_SECS.filter(([k]) => ({ tracking: HL.files.tracking, fatigue: true, changes: HL.files.changes, structure: HL.files.structure, dna: HL.files.creativedna })[k]);
  if (!avail.some(([k]) => k === HL.sec)) HL.sec = avail[0][0];
  let body = '';
  try {
    body = { tracking: hlTracking, fatigue: hlFatigue, changes: hlChanges, structure: hlStructure, dna: hlDna }[HL.sec]();
  } catch (e) { console.error(e); body = '<p class="muted">This check could not run on these dates. Try the last 90 days.</p>'; }
  v.innerHTML = `<div class="hl">
    <div class="mv-head"><div><h2>Account health</h2><p class="lead">5 checks for the media buyer: is tracking complete, which ads are tiring, what past changes did, is the setup clean, and what the best designs share.</p></div></div>
    <div class="hl-tiles" role="tablist">${avail.map(([k, l]) => { const s = st[k] || ['grey', '']; return `<button type="button" role="tab" data-hlsec="${k}" aria-selected="${HL.sec === k}"><span>${esc(l)}</span>${s[1] ? hlChip(s[0], s[1]) : ''}</button>`; }).join('')}</div>
    <div class="hl-body">${body}</div></div>`;
};
document.addEventListener('click', (e) => {
  const v = $('healthView');
  if (!v || !v.contains(e.target)) return;
  const s = e.target.closest('[data-hlsec]');
  if (s) { HL.sec = s.dataset.hlsec; try { localStorage.setItem('health-sec', HL.sec); } catch (er) { /* storage unavailable */ } window.renderHealth(); return; }
  const k = e.target.closest('[data-hlkind]');
  if (k) { HL.chKind = k.dataset.hlkind; HL.chShow = 30; window.renderHealth(); return; }
  if (e.target.closest('[data-hlmore]')) { HL.chShow += 30; window.renderHealth(); return; }
  const o = e.target.closest('[data-open]');
  if (o && typeof openSide === 'function') { e.preventDefault(); openSide(o.dataset.open); }
});
document.addEventListener('change', (e) => {
  if (e.target.matches && e.target.matches('[data-hldnasale]')) { HL.dnaSale = e.target.checked; window.renderHealth(); }
});
