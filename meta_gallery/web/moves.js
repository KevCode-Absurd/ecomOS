'use strict';
// Next moves: one tab that turns the data into jobs for 3 teams.
//   Strategy (founder), Creative (design and content team), Media buying (ads team).
// Every card says what the numbers show, what to do this week, who owns it, the likely effect and how sure
// we are. Nothing here is brand specific: it reads the same data files every brand gets (ads data,
// website sales, traffic), and a card that has no data is simply left out.
// Uses: DATA, VIEW, ENGINE, esc, money, fmt, shortDate (app.js), compact, ovCap (overview.js), SL, loadSales,
// adCat, typeCat, addDays, weekday (sales.js), rpBrand, rpLastSalesDay (report.js), BX, bxBoot (brandx.js),
// bdLastFull, bdRelaunchList (buyer.js), noAdSellers (testlab.js), addTest, docsBoot (lab.js).

const MV = { days: 30, level: 'all', done: {} };
try { MV.done = JSON.parse(localStorage.getItem('moves-done') || '{}') || {}; } catch (e) { MV.done = {}; }
const MV_LEVELS = [['strategy', 'Strategy', 'Founder'], ['creative', 'Creative', 'Creative team'], ['media', 'Media buying', 'Media buyer']];
const mvPct = (v, d = 0) => (v === null || v === undefined || !Number.isFinite(v) ? '–' : (v * 100).toFixed(d) + '%');
const mvX = (v) => (v === null || v === undefined || !Number.isFinite(v) ? 'no sales' : v.toFixed(2) + 'x');
const mvCh = (a, b) => (a !== null && b ? (a - b) / Math.abs(b) : null);
const mvChTxt = (c) => (c === null || !Number.isFinite(c) ? 'no earlier data' : `${c >= 0 ? 'up' : 'down'} ${Math.abs(Math.round(c * 100))}%`);

// ---------- the window: last N full days, and the N days before ----------
function mvWindow() {
  const end = bdLastFull(), N = MV.days;
  const b = ENGINE.idx(end), a = b - N + 1, pb = a - 1, pa = pb - N + 1;
  const first = ENGINE.idx(DATA.meta.window.since);
  return { N, end, since: addDays(end, -(N - 1)), a, b, pa: Math.max(pa, first), pb, prevFull: pa >= first };
}
function mvAds(W) {
  const inc = ENGINE.included(VIEW.exclusions.keywords, VIEW.exclusions.campaign_ids);
  const out = [];
  for (const id of inc) {
    const ad = DATA.ads[id], m = ENGINE.sums(id, W.a, W.b);
    if (m.spend <= 0) continue;
    out.push({ id, ad, m, p: ENGINE.sums(id, W.pa, W.pb), live: ad.effective_status === 'ACTIVE' });
  }
  return out;
}
const mvAdd = (list) => {
  const spend = list.reduce((t, x) => t + x.m.spend, 0), vals = list.filter((x) => x.m.purchase_value !== null);
  const value = vals.reduce((t, x) => t + x.m.purchase_value, 0), purch = list.reduce((t, x) => t + (x.m.purchases || 0), 0);
  const impr = list.reduce((t, x) => t + (x.m.impressions || 0), 0), clicks = list.reduce((t, x) => t + (x.m.link_clicks || 0), 0);
  return { spend, value, purch, impr, clicks, n: list.length, roas: spend && vals.length ? value / spend : null, cpa: purch ? spend / purch : null };
};
const mvConf = (purch, spend) => (purch >= 20 && spend >= 50000 ? 'High' : purch >= 6 ? 'Medium' : 'Low');

// ---------- value rules ----------
// valuerules.json: 90-day age x gender, placement and phone rows for the whole account ("all") and for
// sale campaigns ("sale"). The page uses all minus sale.
async function mvVrBoot() {
  if (MV.vrLoaded) return;
  MV.vrLoaded = true;
  const get = async (f) => { try { const r = await fetch(f); return r.ok ? await r.json() : null; } catch (e) { return null; } };
  const [v, m] = await Promise.all([get('valuerules.json'), get('metainsights.json')]);
  MV.vr = v && v.segments && v.segments.ag ? v : null;
  MV.meta = m && (m.opportunity || m.dataset || m.catalog || m.auction) ? m : null;
}

// ---------- from Meta ----------
// metainsights.json: Meta's own read-outs (opportunity score, pixel match quality, catalog checks,
// ad rankings). Each becomes a card marked "From Meta".
const MI_DO = {
  value_optimization_goal: 'Move ad sets on the "most sales" goal to "most value of sales", 1 or 2 at a time. Meta expects about 7% higher ROAS. Value rules (above) work with both goals.',
  aplusc_standard_enhancements_bundle: 'Turn on Advantage+ creative enhancements for 2 or 3 ads first. Check every variation: touch-ups must keep the metal and stones true to life.',
  capi_event_coverage: 'Ask the web developer to send Purchase through Conversions API as well as the pixel, with the same event ID so Meta counts it once.',
  fragmentation: 'Merge ad sets that run the same ads to different audiences into 1 broad ad set, so it leaves learning faster.',
  advantage_plus_audience: 'Switch 1 older ad set to Advantage+ audience and compare cost per sale for 2 weeks.',
  advantage_plus_catalog_ads: 'Test 1 Advantage+ catalog campaign for past visitors, after the catalog fixes below.',
  messaging_events: 'If sales happen on WhatsApp, send those purchase events to Meta so they count.',
};
function mvMetaCards(push) {
  const M = MV.meta;
  if (!M) return;
  const when = M.captured_at ? `Checked ${shortDate(M.captured_at)}.` : '';
  const O = M.opportunity;
  if (O && O.recs && O.recs.length) {
    const recs = O.recs.slice(0, 6);
    push({ level: 'media', src: 'meta', key: 'x-opportunity', title: `Meta's opportunity score is ${O.score} of 100`,
      finding: `Meta scores how closely the account follows its own best practice. The biggest gains: ${recs.slice(0, 3).map((r) => `${r.title} (+${r.points} points)`).join('; ')}. ${when}`,
      actions: recs.map((r) => MI_DO[r.type] || r.title).slice(0, 5),
      thead: ['Suggestion', 'Points', 'Items'], table: recs.map((r) => [r.title, '+' + r.points, r.objects]),
      note: 'These are Meta\'s suggestions and lean toward more automation. Test each in 1 ad set before rolling out. Open Ads Manager > Opportunity score to apply them.',
      owner: 'Media buyer', impact: { value: 0, text: `Up to +${recs.reduce((t, r) => t + r.points, 0)} points` }, conf: 'Medium' });
  }
  const D = M.dataset && M.dataset.events;
  if (D && D.length) {
    const ev = (n) => D.find((e) => e.event === n), pur = ev('Purchase'), vc = ev('ViewContent');
    const noEmail = D.every((e) => !e.coverage.email), fbc = pur ? pur.coverage.fbc : null;
    const acts = [];
    if (noEmail) acts.push('Send the shopper\'s email (hashed) with every event. Today no event sends it, and email is the strongest match key.');
    if (fbc !== null && fbc < 60) acts.push(`Only ${fbc}% of purchases carry the Meta click ID. Save the fbclid from the landing page URL and send it with the purchase from the server.`);
    if (vc && vc.emq < 6) acts.push(`Product views match poorly (${vc.emq} of 10). Send the phone or customer ID for logged-in shoppers with ViewContent.`);
    if (acts.length) push({ level: 'strategy', src: 'meta', key: 'x-signals', title: `Help Meta match more buyers (purchase match ${pur ? pur.emq : '–'} of 10)`,
      finding: `Meta can only optimise for sales it can tie to a person. ${D.map((e) => `${e.event} ${e.emq}`).join(', ')} (match quality, out of 10). ${when}`,
      actions: [...acts, 'Recheck match quality in Events Manager 1 week after the change.'],
      owner: 'Founder + web developer', impact: { value: 0, text: 'Better matching lowers cost per sale over time' }, conf: 'High' });
  }
  const C = M.catalog && M.catalog.diagnostics;
  if (C && C.length) {
    const sum = (t) => C.filter((d) => d.type === t).reduce((a, d) => a + (d.items || 0), 0);
    const un = sum('UNMATCHED_EVENTS'), noid = sum('NO_CONTENT_ID'), img = sum('not_enough_images');
    const must = C.filter((d) => d.severity === 'must_fix');
    const acts = [...must.map((d) => `Must fix: ${d.title} (${d.items} items).`)];
    if (un) acts.push(`${un} product IDs sent by the website do not match the catalog. Make the pixel content_ids use the same ID as the catalog feed.`);
    if (noid) acts.push(`${noid} product views or cart adds arrived with no product ID. Add content_ids to ViewContent and AddToCart.`);
    if (img) acts.push(`Add a second photo for ${img} catalog items (worn shot or close up).`);
    if (acts.length) push({ level: 'creative', src: 'meta', key: 'x-catalog', title: 'Fix the catalog so product ads show the right piece',
      finding: `Meta's catalog check found ${C.length} issues${must.length ? `, ${must.length} must fix` : ', none blocking'}. When the website and catalog IDs differ, retargeting shows people the wrong pieces or none. ${when}`,
      actions: acts.slice(0, 5), owner: 'Web developer + catalog', impact: { value: 0, text: 'Product ads follow what each shopper viewed' }, conf: 'High', go: 'catalog' });
  }
  const A = M.auction && M.auction.ads;
  const low = (A || []).filter((a) => /below/i.test(a.conversion) || /below/i.test(a.quality) || /below/i.test(a.engagement));
  if (low.length) push({ level: 'media', src: 'meta', key: 'x-ranking', title: `${low.length} ad${low.length > 1 ? 's' : ''} rank low with Meta`,
    finding: `${Object.values(low.reduce((g, a) => { const k = [a.name, a.quality, a.engagement, a.conversion].join('|'); (g[k] = g[k] || { ...a, n: 0 }).n++; return g; }, {})).map((a) => `${a.n > 1 ? `${a.n} ads named ` : ''}"${a.name}": quality ${a.quality.toLowerCase()}, engagement ${a.engagement.toLowerCase()}, conversion rate ${a.conversion.toLowerCase()}`).join('; ')}. ${when}`,
    actions: [low.some((a) => /below/i.test(a.conversion)) ? 'People click but do not buy: check the product pages these ads open (price, photos, speed, stock).' : 'Refresh the image and first line.',
      'Test a single best seller or a collection ad next to the catalog ad.', 'Keep only in-stock pieces in the product set.'],
    owner: 'Media buyer', impact: { value: 0, text: 'Better ranking means cheaper reach' }, conf: 'Medium', go: 'insights' });
}
const VR_PLACE = { 'facebook|feed': 'Facebook feed', 'instagram|feed': 'Instagram feed', 'facebook|facebook_reels': 'Facebook reels', 'instagram|instagram_reels': 'Instagram reels', 'instagram|instagram_stories': 'Instagram stories', 'facebook|facebook_stories': 'Facebook stories', 'facebook|instream_video': 'Facebook in-stream video', 'threads|threads_feed': 'Threads', 'audience_network|an_classic': 'Audience Network', 'whatsapp|whatsapp_status': 'WhatsApp status', 'facebook|marketplace': 'Marketplace', 'instagram|instagram_explore_grid_home': 'Instagram explore' };
function mvValueRules() {
  const V = MV.vr;
  if (!V) return null;
  const net = (x) => { const a = x.all || [0, 0, 0], b = x.sale || [0, 0, 0]; return { s: Math.max(0, a[0] - b[0]), p: Math.max(0, a[1] - b[1]), v: Math.max(0, a[2] - b[2]) }; };
  const ag = Object.entries(V.segments.ag).map(([k, x]) => ({ k, ...net(x) }));
  const T = ag.reduce((t, r) => ({ s: t.s + r.s, p: t.p + r.p, v: t.v + r.v }), { s: 0, p: 0, v: 0 });
  if (!T.s || !T.p) return null;
  const aov = T.v / T.p, cpa = T.s / T.p, R = T.v / T.s, capPer = 3 * aov, M = 8, capped = [];
  const rate = (r, label) => {
    let v = r.v;
    if (r.p && v > r.p * capPer) { v = r.p * capPer; capped.push(label); }
    const shr = (v + M * aov) / (r.s + M * cpa);   // M make-believe sales at the account average
    let pct = Math.round((shr / R - 1) * 10) * 10;
    pct = Math.max(-50, Math.min(100, pct));
    return { ...r, label, roas: r.s ? v / r.s : null, pct, conf: r.p >= 30 ? 'High' : r.p >= 10 ? 'Medium' : 'Low' };
  };
  const out = [];
  for (const r of ag) {
    const [g, age] = r.k.split('|');
    if (g === 'unknown' || /unknown/i.test(age)) continue;
    const who = g === 'female' ? 'Women' : 'Men', ages = age === '65+' ? '65 and over' : age.replace('-', ' to ');
    out.push({ ...rate(r, `${who} ${ages}`), crit: [`Gender: ${who.toLowerCase()}`, `Age: ${ages}`], kind: 1 });
  }
  const os = {};
  for (const [k, x] of Object.entries(V.segments.dev || {})) {
    const n = net(x), key = /iphone|ipad/.test(k) ? 'iOS' : /android/.test(k) ? 'Android' : /desktop/.test(k) ? 'Desktop' : null;
    if (!key) continue;
    const o = os[key] || (os[key] = { s: 0, p: 0, v: 0 });
    o.s += n.s; o.p += n.p; o.v += n.v;
  }
  for (const [k, r] of Object.entries(os)) out.push({ ...rate(r, k === 'Desktop' ? 'Desktop' : `${k} phones`), crit: [k === 'Desktop' ? 'Device: desktop' : `Operating system: ${k}`], kind: 2 });
  for (const [k, x] of Object.entries(V.segments.pl || {})) {
    const label = VR_PLACE[k];
    if (label) out.push({ ...rate(net(x), label), crit: [`Placement: ${label}`], kind: 3 });
  }
  // Bid up only with 10 or more sales behind it (a couple of big orders is luck, not a pattern).
  // Bid down needs real spend: at least 3 times the cost of 1 sale.
  const ok = out.filter((r) => r.s >= T.s * 0.01 && Math.abs(r.pct) >= 10 && (r.pct > 0 ? r.p >= 10 : r.s >= 3 * cpa));
  const pick = (kind, n) => ok.filter((r) => r.kind === kind).sort((a, b) => Math.abs(b.pct) * Math.sqrt(b.s) - Math.abs(a.pct) * Math.sqrt(a.s)).slice(0, n);
  const other = [...pick(2, 2), ...pick(3, 3)].sort((a, b) => Math.abs(b.pct) * Math.sqrt(b.s) - Math.abs(a.pct) * Math.sqrt(a.s)).slice(0, 3);
  const rules = [...pick(1, 10 - other.length), ...other];
  const saleSpend = Object.values(V.segments.ag).reduce((t, x) => t + ((x.sale || [0])[0] || 0), 0);
  return { rules, R, until: V.window.until, saleSpend, capped: [...new Set(capped)].filter((l) => rules.some((r) => r.label === l)) };
}

// ---------- cards ----------
// Each returns null (no data or nothing to say) or:
// { level, key, title, finding, actions: [..], owner, impact: {value, text}, conf, go }
function mvCards(W, ads, adsAll) {
  const all = mvAdd(ads), cards = [];
  const tgt = VIEW.targets.roas || all.roas || 0, cpa = VIEW.targets.cpa || all.cpa || 0;
  const perMonth = (v) => v / W.N * 30;
  const push = (c) => { if (c) cards.push(c); };
  const brand = SL.data ? (() => {
    const last = rpLastSalesDay();
    if (!last) return null;
    const until = W.end > last ? last : W.end;
    return { cur: rpBrand(addDays(until, -(W.N - 1)), until), prev: rpBrand(addDays(until, -(2 * W.N - 1)), addDays(until, -W.N)) };
  })() : null;

  // ===== STRATEGY =====
  // S1. Total budget: raise, hold or pull back, from all website sales per ₹1 of ads.
  if (brand && brand.cur.sales !== null && brand.cur.spend) {
    const per = brand.cur.sales / brand.cur.spend, pper = brand.prev.sales !== null && brand.prev.spend ? brand.prev.sales / brand.prev.spend : null;
    const ch = mvCh(per, pper), up = ch !== null && ch >= 0.05 && (all.roas || 0) >= tgt * 0.95, down = ch !== null && ch <= -0.15;
    const extra = perMonth(brand.cur.spend) * 0.1;
    push({ level: 'strategy', key: 's-budget', title: up ? 'Raise the total ad budget by 10%' : down ? 'Hold the budget and fix creative first' : 'Keep the total budget steady',
      finding: `Every ₹1 on ads came with ₹${per.toFixed(1)} of website sales in the last ${W.N} days, ${mvChTxt(ch)} from the ${W.N} days before. Meta's own ROAS: ${mvX(all.roas)} (target ${mvX(tgt)}).`,
      actions: up ? [`Add about ${compact(extra)} a month, in steps of 10 to 20% every 3 to 4 days.`, 'Put the new money on the Scale ads in Media buying below, not on new tests.', 'Check this card again in 2 weeks. Stop adding if the return per ₹1 drops 10%.']
        : down ? ['Do not add budget this month.', 'Swap out tired ads first (see Creative).', 'Cut the ads in "Stop paying for these" below, then look again.']
          : ['Keep spend where it is.', 'Move money inside the account instead (see the cards below).'],
      owner: 'Founder', impact: up ? { value: extra * per * 0.6, text: `About ${compact(extra * per * 0.6)} more sales a month, if new money returns 60% of today's rate` } : { value: 0, text: 'Protects margin while creative is fixed' },
      conf: brand.cur.covered >= W.N * 0.9 && pper !== null ? 'High' : 'Medium', go: 'overview' });
  }
  // S2. How much sales depend on Meta.
  if (brand && brand.cur.sales) {
    const claimed = brand.cur.days.reduce((t, r) => t + (r.claimed || 0), 0), share = claimed / brand.cur.sales;
    if (claimed) push({ level: 'strategy', key: 's-share', title: share > 0.7 ? 'Too much rides on Meta: start a second channel' : share < 0.3 ? 'Most sales come without Meta: protect them' : 'Meta is 1 of several sales drivers',
      finding: `Meta counts ${compact(claimed)} of ${compact(brand.cur.sales)} website sales (${mvPct(share)}) in the last ${W.N} days. The rest comes from search, direct, repeat buyers and other channels.`,
      actions: share > 0.7 ? ['Start Google search ads on your brand and top product names.', 'Build an email and WhatsApp list from every order.', 'Keep Meta spend steady while the second channel grows.']
        : share < 0.3 ? ['Check that the Meta pixel and conversions API are sending every purchase.', 'Grow repeat buying: email and WhatsApp for past buyers.', 'Test a 2-week Meta pause in 1 region to see what Meta really adds.']
          : ['Keep a healthy mix. Review this every month.', 'Connect Google and email so each channel shows up here.'],
      owner: 'Founder', impact: { value: 0, text: 'Lowers risk if Meta costs rise' }, conf: 'Medium', go: 'overview' });
  }
  // S3. Category to push: share of website sales vs share of ad spend.
  if (brand && brand.cur.types) {
    const sales = brand.cur.types, st = Object.values(sales).reduce((t, v) => t + v, 0), sp = {};
    for (const x of ads) { const c = adCat(x.ad); if (c !== 'Mixed') sp[c] = (sp[c] || 0) + x.m.spend; }
    const spT = Object.values(sp).reduce((t, v) => t + v, 0);
    if (st && spT) {
      const rows = Object.keys({ ...sales, ...sp }).filter((c) => c !== 'Other' && c !== 'Mixed').map((c) => ({ c, s: (sales[c] || 0) / st, a: (sp[c] || 0) / spT, v: sales[c] || 0 })).map((r) => ({ ...r, gap: r.s - r.a }));
      const under = rows.filter((r) => r.s >= 0.08).sort((x, y) => y.gap - x.gap)[0], over = rows.sort((x, y) => x.gap - y.gap)[0];
      if (under && under.gap >= 0.08) push({ level: 'strategy', key: 's-cat', title: `Put more ad money on ${under.c.toLowerCase()}`,
        finding: `${under.c} is ${mvPct(under.s)} of website sales but gets ${mvPct(under.a)} of the ad spend you can tie to a category.${over && over.gap <= -0.08 ? ` ${over.c} is the opposite: ${mvPct(over.a)} of spend for ${mvPct(over.s)} of sales.` : ''}`,
        actions: [`Move about ${compact(perMonth(spT) * Math.min(0.15, under.gap / 2))} a month toward ${under.c.toLowerCase()} ads.`, `Brief 3 new ${under.c.toLowerCase()} ads with your best sellers (see Creative).`, ...(over && over.gap <= -0.08 ? [`Trim ${over.c.toLowerCase()} spend by the same amount.`] : [])],
        owner: 'Founder', impact: { value: perMonth(spT) * Math.min(0.15, under.gap / 2) * 0.5, text: 'Spend follows what buyers already want' }, conf: 'Medium', go: 'sales' });
    }
  }
  // S4. Price band buyers pick.
  if (brand) {
    const bands = {};
    for (const r of brand.cur.days) {
      const b = r.x && (r.x.bands || (SL.data.daily[r.d] || {}).bands);
      for (const row of b || []) { const k = row[1]; bands[k] = (bands[k] || 0) + (row[2] || 0); }
    }
    const tot = Object.values(bands).reduce((t, v) => t + v, 0), top = Object.entries(bands).sort((a, b) => b[1] - a[1])[0];
    const bandTxt = (k) => { const m = String(k).match(/^(\d+)\s*-\s*(\d+)$/); const f = (n) => '₹' + Number(n).toLocaleString('en-IN'); return m ? `${f(m[1])} to ${f(m[2])}` : /\+$/.test(k) ? `over ${f(parseInt(k, 10))}` : k; };
    if (tot >= 20 && top) push({ level: 'strategy', key: 's-band', title: `Lead with pieces priced ${bandTxt(top[0])}`,
      finding: `${mvPct(top[1] / tot)} of website orders in the last ${W.N} days were in the ${bandTxt(top[0])} band (${top[1]} of ${tot}).`,
      actions: ['Make sure at least half of live product ads show pieces in this band.', 'Show the price and EMI in the ad for pieces above it.', 'Use cheaper pieces as a first-order hook, not the main offer.'],
      owner: 'Founder', impact: { value: 0, text: 'Ads match what people actually pay' }, conf: tot >= 60 ? 'High' : 'Medium', go: 'sales' });
  }
  // S5. Big days make planning noisy.
  if (brand && brand.cur.sales) {
    const vals = brand.cur.days.filter((r) => r.x && r.x.sales !== null).map((r) => r.x.sales), cap = ovCap(vals);
    const big = cap ? vals.filter((v) => v > cap.cap) : [], bigSum = big.reduce((t, v) => t + v, 0);
    if (big.length && bigSum / brand.cur.sales >= 0.12) push({ level: 'strategy', key: 's-big', title: 'Plan on normal days, not big days',
      finding: `${big.length} big day${big.length > 1 ? 's' : ''} made ${compact(bigSum)}, ${mvPct(bigSum / brand.cur.sales)} of sales. A normal day is about ${compact(cap.med)}.`,
      actions: ['Mark client or bulk orders on the Overview so they stop skewing numbers.', `Set monthly targets from a normal day: about ${compact(cap.med * 30)} a month.`, 'Ask what caused each big day (a client, a sale, a festival) and write it down.'],
      owner: 'Founder', impact: { value: 0, text: 'Better targets and budgets' }, conf: 'High', go: 'overview' });
  }
  // S6. Visits falling.
  if (typeof BX !== 'undefined' && BX.traffic && typeof gaMap === 'function') {
    const ga = gaMap(), sum = (a, b) => { let t = 0, n = 0; for (let d = a; d <= b; d = addDays(d, 1)) if (ga[d] && ga[d].visits) { t += ga[d].visits; n++; } return n ? t : null; };
    const end = rpLastSalesDay(), v1 = sum(addDays(end, -27), end), v0 = sum(addDays(end, -55), addDays(end, -28));
    const acct = bdAccountDays(), c1 = bdSum(acct, ENGINE.idx(addDays(end, -27)), ENGINE.idx(end)).clicks, c0 = bdSum(acct, ENGINE.idx(addDays(end, -55)), ENGINE.idx(addDays(end, -28))).clicks;
    if (v1 && v0 && v1 < v0 * 0.85) push({ level: 'strategy', key: 's-visits', title: 'Win back lost site visits',
      finding: `Site visits fell ${Math.round((1 - v1 / v0) * 100)}% (last 4 weeks vs the 4 before). Meta link clicks moved ${mvChTxt(mvCh(c1, c0))}.`,
      actions: c0 && c1 < c0 * 0.8 ? ['Meta is sending fewer people: check reach, budgets and paused ad sets.', 'Add 2 to 3 broad prospecting ads with fresh creative.', 'Check links on live ads go to the right pages.'] : ['Meta clicks held, so look at search, direct and social.', 'Check Google Analytics tracking on every page.', 'Post more on Instagram and send a newsletter this week.'],
      owner: 'Founder', impact: { value: 0, text: 'More people at the top of the funnel' }, conf: 'Medium', go: 'overview' });
  }

  // ===== CREATIVE =====
  // C1. Format that wins vs where the money goes.
  const fmts = {};
  for (const x of ads) (fmts[x.ad.creative.type] || (fmts[x.ad.creative.type] = [])).push(x);
  const fr = Object.entries(fmts).map(([k, l]) => ({ k, label: (DATA.meta.format_labels || {})[k] || k, ...mvAdd(l), live: l.filter((x) => x.live).length })).map((r) => ({ ...r, share: all.spend ? r.spend / all.spend : 0 }));
  const fq = fr.filter((r) => r.roas !== null && (r.purch >= 8 || (r.share >= 0.1 && r.purch >= 3)));
  const small = fr.filter((r) => r.roas !== null && !fq.includes(r) && r.purch >= 2 && r.roas >= (all.roas || 0) * 1.2);
  if (fq.length >= 2) {
    const best = fq.slice().sort((a, b) => b.roas - a.roas)[0], worst = fq.filter((r) => r.share >= 0.1 && r.k !== best.k).sort((a, b) => a.roas - b.roas)[0];
    if (best && (!worst || best.roas > worst.roas * 1.2)) {
      const move = worst ? perMonth(worst.spend) * 0.15 : 0;
      push({ level: 'creative', key: 'c-format', title: `Make more ${best.label.toLowerCase()} ads`,
        finding: `${best.label} ads returned ${mvX(best.roas)} in the last ${W.N} days on ${mvPct(best.share)} of spend (${best.live} live).${worst ? ` ${worst.label} returned ${mvX(worst.roas)} on ${mvPct(worst.share)} of spend.` : ''}`,
        actions: [`Brief ${Math.max(3, Math.min(6, best.live + 2))} new ${best.label.toLowerCase()} ads this week, using the top ${best.label.toLowerCase()} ad as the model.`, ...(worst ? [`Media buyer: move about ${compact(move)} a month (15% of ${worst.label.toLowerCase()} spend) to ${best.label.toLowerCase()}.`] : []), 'Keep 1 new test of the weaker format a week, so you learn why it lags.', ...small.map((r) => `${r.label} shows ${mvX(r.roas)} but on only ${r.purch} sales: make 2 more to see if it holds.`)],
        owner: 'Creative team + media buyer', impact: { value: move * Math.max(0, best.roas - (worst ? worst.roas : 0)) * 0.5, text: worst ? `About ${compact(move * Math.max(0, best.roas - worst.roas) * 0.5)} more sales a month, at half the ROAS gap` : 'More of what works' },
        conf: mvConf(best.purch, best.spend), go: 'gallery', table: fr.sort((a, b) => b.spend - a.spend).map((r) => [r.label, compact(r.spend), mvPct(r.share), mvX(r.roas), r.purch]) });
    }
  }
  // C2 / C3. Angle and opening line to double down on, and one to stop.
  const exNS = VIEW.exclusions;
  const th = withoutSale(() => ENGINE.themes({ range: { since: W.since, until: W.end }, exclusions: exNS }));   // no sale ads
  for (const [dim, name, noun] of [['angle', 'angle', 'message'], ['hook', 'opening line', 'first line']]) {
    const rows = (th[dim] || []).filter((r) => r.spend > 0 && !/other|catalog|none|unknown/i.test(r.code)), tot = rows.reduce((t, r) => t + r.spend, 0);
    const q = rows.filter((r) => r.roas !== null && (r.purchases || 0) >= 3);
    const best = q.slice().sort((a, b) => b.roas - a.roas)[0], weak = q.filter((r) => r.spend / tot >= 0.1 && r !== best && r.roas < (all.roas || 0) * 0.7).sort((a, b) => a.roas - b.roas)[0];
    if (best && best.roas >= (all.roas || 0) * 1.15 && best.spend / tot < 0.35) push({ level: 'creative', key: 'c-' + dim, title: `Double down on the "${best.label}" ${name}`,
      finding: `Ads with the "${best.label}" ${noun} returned ${mvX(best.roas)} vs the account's ${mvX(all.roas)}, on only ${mvPct(best.spend / tot)} of spend.${weak ? ` "${weak.label}" returned ${mvX(weak.roas)} on ${mvPct(weak.spend / tot)}.` : ''}`,
      actions: [`Write 3 new ads with this ${noun}. Model: "${best.top ? best.top.name : ''}".`, 'Keep the same product and format, change only the words, so the test is clean.', ...(weak ? [`Stop briefing "${weak.label}" ${noun}s until a new version beats the account.`] : [])],
      owner: 'Creative team', impact: { value: perMonth(best.spend) * 0.3 * Math.max(0, best.roas - (all.roas || 0)), text: 'More spend on the message buyers answer' }, conf: mvConf(best.purchases || 0, best.spend), go: 'insights' });
  }
  // C4. Video hooks: the first 3 seconds.
  const vt = withoutSale(() => ENGINE.videoTable({ range: { since: W.since, until: W.end }, exclusions: exNS }));
  const avgHook = vt.avg.hook_rate, weakV = vt.rows.filter((r) => !r.video.mostly_image && r.video.hook_rate !== null && avgHook && r.video.hook_rate < avgHook * 0.7 && r.metrics.spend >= 3000).slice(0, 3);
  if (avgHook && weakV.length) push({ level: 'creative', key: 'c-hook', title: 'Recut the first 3 seconds of weak videos',
    finding: `Your videos stop ${avgHook.toFixed(1)}% of people in the first 3 seconds on average. ${weakV.length} video${weakV.length > 1 ? 's' : ''} with real spend sit well below that: ${weakV.map((r) => `"${r.name}" ${r.video.hook_rate.toFixed(1)}%`).join(', ')}.`,
    actions: ['Open on the piece being worn, close up, in the first second.', 'Put a short line of text on screen at 0 seconds (price, a claim or a question).', 'Cut any logo or slow intro at the start. Keep the rest of the video.'],
    owner: 'Creative team', impact: { value: weakV.reduce((t, r) => t + perMonth(r.metrics.spend), 0) * 0.1, text: 'Same spend, more people watching' }, conf: 'Medium', go: 'insights' });
  // C5. Refresh load: how many new ads a week.
  const live = ads.filter((x) => x.live), tired = live.filter((x) => { const f = ENGINE.fatigue(x.id, W.b); return f && ['declining', 'ctr_down', 'roas_down'].includes(f.code); });
  const fresh = ads.filter((x) => x.m.first_day && x.m.first_day >= W.since && ENGINE.sums(x.id, 0, W.a - 1).spend <= 0);
  const freshShare = all.spend ? fresh.reduce((t, x) => t + x.m.spend, 0) / all.spend : 0;
  if (live.length) {
    const need = Math.max(2, Math.ceil(tired.length / 2) + (freshShare < 0.2 ? 2 : 0));
    push({ level: 'creative', key: 'c-velocity', title: `Ship ${need} new ads a week`,
      finding: `${tired.length} of ${live.length} live ads show fatigue. New ads (launched in the last ${W.N} days) took ${mvPct(freshShare)} of spend; a healthy account keeps 20 to 30% on new ads.`,
      actions: [`Plan ${need} new ads every week: half new versions of winners, half new ideas.`, `Replace these tired ads first: ${tired.slice(0, 3).map((x) => `"${x.ad.name}"`).join(', ') || 'none right now'}.`, 'Keep a shared brief list in the Creative studio tab so nothing waits on a meeting.'],
      owner: 'Creative team', impact: { value: 0, text: 'Stops slow decline as ads tire' }, conf: live.length >= 10 ? 'High' : 'Medium', go: 'studio' });
  }
  // C6. Best sellers with no ad.
  if (SL.data && typeof noAdSellers === 'function') {
    let list = [];
    try { list = noAdSellers().slice(0, 5); } catch (e) { list = []; }
    if (list.length) push({ level: 'creative', key: 'c-products', title: `Make ads for ${list.length} best sellers that have none`,
      finding: `These sell on the website with no ad naming them: ${list.map((r) => `${r.name} (${r.n} sold)`).join(', ')}.`,
      actions: ['Make 2 statics and 1 short video for the top 2.', 'Use the product page photos and facts (Creative studio builds these).', 'Media buyer: test them in the best prospecting ad set with a small budget.'],
      owner: 'Creative team', impact: { value: 0, text: 'Ads for pieces people already buy' }, conf: 'Medium', go: 'actions' });
  }

  // ===== MEDIA BUYING =====
  // M1. Scale.
  const scale = ads.filter((x) => x.live && x.m.roas !== null && x.m.roas >= tgt * 1.3 && (x.m.purchases || 0) >= 3).sort((a, b) => b.m.roas - a.m.roas).slice(0, 5);
  if (scale.length) {
    const add = scale.reduce((t, x) => t + perMonth(x.m.spend) * 0.2, 0);
    push({ level: 'media', key: 'm-scale', title: `Raise budget on ${scale.length} winning ad${scale.length > 1 ? 's' : ''} by 20%`,
      finding: `${scale.map((x) => `"${x.ad.name}" ${mvX(x.m.roas)} on ${x.m.purchases} sales`).join('; ')}. Target ROAS is ${mvX(tgt)}.`,
      actions: ['Raise each ad set by 20%, then wait 3 to 4 days before the next step.', 'If ROAS falls under target after a raise, step back once.', 'Duplicate the best one into a new ad set with a broad audience.'],
      owner: 'Media buyer', impact: { value: add * scale.reduce((t, x) => t + x.m.roas, 0) / scale.length * 0.6, text: `About ${compact(add)} more spend a month at a lower but still good return` }, conf: mvConf(scale.reduce((t, x) => t + (x.m.purchases || 0), 0), scale.reduce((t, x) => t + x.m.spend, 0)), go: 'buyer' });
  }
  // M2. Stop paying for these.
  const cut = (adsAll || ads).filter((x) => x.live && ((cpa && x.m.spend >= 2 * cpa && !x.m.purchases) || (x.m.roas !== null && x.m.roas < tgt * 0.5 && x.m.spend >= 3 * (cpa || 3000)))).sort((a, b) => b.m.spend - a.m.spend).slice(0, 6);
  if (cut.length) {
    const save = cut.reduce((t, x) => t + perMonth(x.m.spend), 0);
    push({ level: 'media', key: 'm-cut', title: `Stop paying for ${cut.length} ad${cut.length > 1 ? 's' : ''}`,
      finding: `${cut.map((x) => `"${x.ad.name}" ${compact(x.m.spend)}, ${x.m.purchases ? mvX(x.m.roas) : 'no sales'}`).join('; ')}.`,
      actions: ['Pause them, or cut their budget in half if they are the only ad in an ad set.', 'Move the money to the Scale list above.', 'Tell the creative team which ones stopped, so they do not brief the same idea.'],
      owner: 'Media buyer', impact: { value: save * 0.6, text: `Frees about ${compact(save)} a month` }, conf: 'High', go: 'buyer' });
  }
  // M3. Relaunch.
  if (typeof bdRelaunchList === 'function') {
    const rl = bdRelaunchList().slice(0, 4);
    if (rl.length) push({ level: 'media', key: 'm-relaunch', title: `Turn ${rl.length} proven ad${rl.length > 1 ? 's' : ''} back on`,
      finding: `Off now, but they did well: ${rl.map((x) => `"${x.ad.name}" ${mvX(x.m.roas)} on ${x.m.purchases} sales`).join('; ')}.`,
      actions: ['Relaunch as new ads in a fresh ad set (the old learning is gone).', 'Start at the budget they had, not more.', 'Check prices and stock on the product first.'],
      owner: 'Media buyer', impact: { value: 0, text: 'Cheap wins: the creative is already proven' }, conf: 'Medium', go: 'buyer' });
  }
  // M4. Value rules: bid more for people who buy more, less for those who don't. Built from the last 90 days
  // of age, gender, placement and phone type, with sale campaigns taken out (they sold on the discount).
  const vr = mvValueRules();
  if (vr && vr.rules.length) {
    const up = vr.rules.filter((r) => r.pct > 0), down = vr.rules.filter((r) => r.pct < 0);
    push({ level: 'media', key: 'm-vrules', title: `Set ${vr.rules.length} value rules on your sales ad sets`,
      finding: `Some buyers are worth more than others. In the last 90 days (sale campaigns left out) ${up.slice(0, 2).map((r) => `${r.label} returned ${mvX(r.roas)}`).join(' and ') || 'no group stood out'}, while ${down.slice(0, 2).map((r) => `${r.label} returned ${mvX(r.roas)}`).join(' and ') || 'no group lagged'}. The account returned ${mvX(vr.R)}. Value rules tell Meta to bid more or less for these people, without cutting anyone out.`,
      actions: ['In Ads Manager, open a Sales ad set and find Value rules. Create 1 rule set with the rules below, in this order. Meta uses the first rule that matches a person.',
        'Use it only where the goal is most sales, most value or a cost per result goal. It does not work with a ROAS goal, a bid cap or Advantage+ catalog ads.',
        'Keep the audience broad. The rules steer spend, they do not exclude anyone.',
        'Start with the rules marked High or Medium. Add the Low ones after 2 weeks if the first ones help.',
        'Judge it on value and ROAS after 7 to 14 days, using the value rules breakdown in Ads Manager. Cost per sale may rise a little; that is expected.'],
      extra: ['Value rules to set (in order):', ...vr.rules.map((r, i) => `${i + 1}. ${r.crit.join(' + ')}: ${r.pct > 0 ? '+' : ''}${r.pct}% (${mvX(r.roas)} on ${r.p} sales, ${compact(r.s)} spent)`)],
      thead: ['#', 'Who', 'Bid change', 'ROAS', 'Sales', 'Spent', 'How sure'],
      table: vr.rules.map((r, i) => [i + 1, r.crit.join(' + '), `${r.pct > 0 ? '+' : ''}${r.pct}%`, mvX(r.roas), r.p, compact(r.s), r.conf]),
      note: `Numbers are Meta's, last 90 days to ${shortDate(vr.until)}. Left out: ${vr.saleSpend ? `${compact(vr.saleSpend)} of sale campaign spend` : 'no sale spend'}${vr.capped.length ? `; very large orders were capped for ${vr.capped.join(', ')}` : ''}. Small groups are pulled toward the account average, so the % is careful. Rules are capped at +100% and −50% to start; Meta allows +1000% to −90%.`,
      owner: 'Media buyer', impact: { value: down.reduce((t, r) => t + r.s / 3, 0) * Math.abs(down.length ? down[0].pct : 0) / 100 * vr.R * 0.3, text: 'More of the budget reaches the people who buy the most' },
      conf: vr.rules.some((r) => r.conf === 'High') ? 'Medium' : 'Low', go: 'buyer' });
  }
  // M5. Auction cost and click rate.
  const acc = bdAccountDays(), cur = bdSum(acc, W.a, W.b), prev = bdSum(acc, W.pa, W.pb);
  if (W.prevFull && prev.impr && cur.impr) {
    const cpm = cur.spend / cur.impr * 1000, pcpm = prev.spend / prev.impr * 1000, ctr = cur.clicks / cur.impr, pctr = prev.clicks / prev.impr;
    const dc = mvCh(cpm, pcpm), dt = mvCh(ctr, pctr);
    if (Math.abs(dc) >= 0.12 || Math.abs(dt) >= 0.12) push({ level: 'media', key: 'm-auction', title: dc > 0.12 && dt < -0.08 ? 'Ads are tiring: costs up, clicks down' : dc > 0.12 ? 'Reaching people got more expensive' : dt < -0.12 ? 'Fewer people click' : 'Cheaper reach: good time to test',
      finding: `Cost per 1,000 views ${money(cpm)} (${mvChTxt(dc)}). Link click rate ${(ctr * 100).toFixed(2)}% (${mvChTxt(dt)}). Last ${W.N} days vs the ${W.N} before.`,
      actions: dc > 0.12 && dt < -0.08 ? ['Launch fresh creative this week (see Creative).', 'Widen audiences on the tired ad sets.', 'Do not raise budgets until click rate recovers.']
        : dc > 0.12 ? ['Expect this before festivals: book creative early.', 'Lean on your best ads; pause tests with weak starts faster.', 'Check frequency on retargeting ad sets.']
          : dt < -0.12 ? ['Refresh the first line and the first image of top ads.', 'Check the offer is still clear in the ad.'] : ['Launch 2 to 3 new tests while costs are low.'],
      owner: 'Media buyer', impact: { value: 0, text: 'Early warning before ROAS drops' }, conf: 'High', go: 'insights' });
  }
  // M6. Too much on too few ads.
  const top3 = ads.slice().sort((a, b) => b.m.spend - a.m.spend).slice(0, 3), t3 = all.spend ? top3.reduce((t, x) => t + x.m.spend, 0) / all.spend : 0;
  if (t3 >= 0.6) push({ level: 'media', key: 'm-concentration', title: 'Spend sits on too few ads',
    finding: `The top 3 ads took ${mvPct(t3)} of spend: ${top3.map((x) => `"${x.ad.name}"`).join(', ')}. If one tires, results drop fast.`,
    actions: ['Build 2 backup versions of each top ad now.', 'Run them next to the originals at 10 to 15% of their budget.', 'Promote a backup as soon as it matches the original for 5 days.'],
    owner: 'Media buyer', impact: { value: 0, text: 'Less risk of a sudden drop' }, conf: 'High', go: 'gallery' });
  // M7. States with room.
  if (typeof BX !== 'undefined' && BX.geo) {
    const P = BX.geo.periods.d28 || BX.geo.periods.d90, ab = new Set(BX.geo.abroad || []), st = {};
    let u = 0, s = 0;
    for (const [c, n] of P.cities) { if (ab.has(c)) continue; const k = BX.geo.city_state[c]; if (!k) continue; (st[k] || (st[k] = { u: 0, s: 0 })).u += n; u += n; }
    for (const m of P.meta || []) { if (!st[m.region]) continue; st[m.region].s += m.spend; s += m.spend; }
    const room = Object.entries(st).map(([k, v]) => ({ k, us: v.u / u, ss: v.s / s })).filter((r) => r.us >= 0.03 && r.ss < r.us * 0.7).sort((a, b) => (b.us - b.ss) - (a.us - a.ss)).slice(0, 3);
    if (room.length) push({ level: 'media', key: 'm-geo', title: `Test more spend in ${room.map((r) => r.k).join(', ')}`,
      finding: room.map((r) => `${r.k}: ${mvPct(r.us)} of site visitors, ${mvPct(r.ss)} of Meta spend`).join('; ') + '.',
      actions: ['Duplicate your best prospecting ad set with only these states.', 'Give it 10 to 15% of prospecting budget for 2 weeks.', 'Keep it if cost per purchase is within 20% of the account.'],
      owner: 'Media buyer', impact: { value: 0, text: 'Reach buyers you are under-serving' }, conf: 'Low', go: 'overview' });
  }
  mvMetaCards(push);
  return cards;
}

// ---------- page ----------
function mvCard(c, i) {
  const [, lname] = MV_LEVELS.find((l) => l[0] === c.level);
  const done = !!MV.done[c.key];
  const text = [`${c.title} (${lname}, owner: ${c.owner})`, c.finding, ...c.actions.map((a, j) => `${j + 1}. ${a}`), ...(c.extra ? ['', ...c.extra] : []), `Effect: ${c.impact.text}. How sure: ${c.conf}.`].join('\n');
  return `<article class="mv-card${done ? ' done' : ''}" data-level="${c.level}">
    <div class="mv-top"><span class="mv-lvl mv-${c.level}">${esc(lname)}</span><span class="mv-owner">${esc(c.owner)}</span><span class="mv-conf mv-c${c.conf}">${esc(c.conf)} confidence</span>${c.src === 'meta' ? '<span class="mv-src">From Meta</span>' : ''}</div>
    <h3>${i !== null ? `<span class="mv-n">${i + 1}</span>` : ''}${esc(c.title)}</h3>
    <p class="mv-why">${esc(c.finding)}</p>
    ${c.table ? `<div class="scroll"><table class="bd-table"><tr>${(c.thead || ['Format', 'Spend', 'Share', 'ROAS', 'Sales']).map((h, j) => `<th class="${j && !/who/i.test(h) ? 'n' : ''}">${esc(h)}</th>`).join('')}</tr>${c.table.map((r) => `<tr>${r.map((v, j) => `<td class="${j && !(c.thead && /who/i.test(c.thead[j])) ? 'n' : ''}">${esc(String(v))}</td>`).join('')}</tr>`).join('')}</table></div>` : ''}
    ${c.note ? `<p class="small muted">${esc(c.note)}</p>` : ''}
    <ol class="mv-do">${c.actions.map((a) => `<li>${esc(a)}</li>`).join('')}</ol>
    <div class="mv-foot"><span class="mv-imp">${esc(c.impact.text)}</span>
      <span class="act-btns">${copyBtn(text)}<button class="btn ghost small-btn" type="button" data-mvtrack="${esc(c.key)}">Add to tracker</button><button class="btn ghost small-btn" type="button" data-mvdone="${esc(c.key)}">${done ? 'Done ✓' : 'Mark done'}</button>${c.go ? `<button class="linkbtn" type="button" data-goto="${esc(c.go)}">See the data</button>` : ''}</span></div>
  </article>`;
}
window.renderMoves = async function renderMoves() {
  const v = $('movesView');
  if (!v || !VIEW) return;
  if (!SL.data && !SL.err) { v.innerHTML = '<p class="muted">Loading website sales…</p>'; await loadSales(); }
  if (typeof BX !== 'undefined' && !BX.loaded) await bxBoot();
  await mvVrBoot();
  const W = mvWindow(), adsAll = mvAds(W), ads = noSale(adsAll, (x) => x.ad);
  const saleOut = adsAll.length - ads.length, saleSpend = adsAll.filter((x) => isSaleAd(x.ad)).reduce((t, x) => t + x.m.spend, 0);
  let cards = [];
  try { cards = mvCards(W, ads, adsAll); } catch (e) { cards = []; console.error(e); }
  MV.cards = cards;
  const top = cards.filter((c) => !MV.done[c.key]).slice().sort((a, b) => (b.impact.value || 0) - (a.impact.value || 0) || (b.conf === 'High') - (a.conf === 'High')).slice(0, 5);
  const brandName = (DATA.meta.account_name || 'Your brand').replace(/\s*-\s*\d+$/, '');
  const list = MV.level === 'all' ? cards : cards.filter((c) => c.level === MV.level);
  const allText = [`${brandName}: next moves, last ${W.N} days to ${shortDate(W.end)}`, ...MV_LEVELS.flatMap(([k, n, o]) => { const l = cards.filter((c) => c.level === k); return l.length ? ['', `${n.toUpperCase()} (${o})`, ...l.map((c) => `- ${c.title}: ${c.actions[0]}`)] : []; })].join('\n');
  v.innerHTML = `<div class="mv">
    <div class="mv-head"><div><h2>Next moves</h2><p class="lead">What to do this week, split by who does it. Built from the last ${W.N} full days (to ${esc(shortDate(W.end))}) compared with the ${W.N} days before.</p>${saleOut ? `<p class="small muted">${saleOut} sale ad${saleOut > 1 ? 's' : ''} (${compact(saleSpend)} spent) are left out of every suggestion. They sold on the discount, so copying them now would mislead. Lists name at most ${REC_CAP} ads.</p>` : ''}</div>
      <div class="row" style="gap:8px;flex-wrap:wrap;align-items:center"><div class="seg" role="group" aria-label="Days">${[30, 60, 90].map((d) => `<button type="button" data-mvdays="${d}" aria-pressed="${MV.days === d}">${d} days</button>`).join('')}</div>${copyBtn(allText)}</div></div>
    ${top.length ? `<section class="mv-top5"><h3>This week's top ${top.length}</h3><ol>${top.map((c) => `<li><b>${esc(c.title)}</b> <span class="muted small">${esc(c.owner)} · ${esc(c.impact.text)}</span></li>`).join('')}</ol></section>` : ''}
    <div class="mv-tabs" role="tablist">${[['all', 'All', cards.length], ...MV_LEVELS.map(([k, n]) => [k, n, cards.filter((c) => c.level === k).length])].map(([k, n, c]) => `<button type="button" role="tab" data-mvlevel="${k}" aria-selected="${MV.level === k}">${esc(n)} <b>${c}</b></button>`).join('')}</div>
    ${MV_LEVELS.filter(([k]) => MV.level === 'all' || MV.level === k).map(([k, n, o]) => { const l = list.filter((c) => c.level === k); return l.length ? `<h3 class="mv-sec">${esc(n)} <span class="muted small">for the ${esc(o.toLowerCase())}</span></h3><div class="mv-grid">${l.map((c) => mvCard(c, null)).join('')}</div>` : ''; }).join('')}
    ${cards.length ? '' : '<p class="muted">Not enough data in these days to suggest moves. Try 60 or 90 days.</p>'}
    <p class="small muted">How sure: High means 20 or more sales and real spend behind the numbers; Low means a guide to test, not a rule. Effects are rough monthly estimates. This page cannot change ads or budgets; the team makes each move.</p>
  </div>`;
};
document.addEventListener('click', async (e) => {
  const v = $('movesView');
  if (!v || !v.contains(e.target)) return;
  const d = e.target.closest('[data-mvdays]');
  if (d) { MV.days = Number(d.dataset.mvdays); window.renderMoves(); return; }
  const l = e.target.closest('[data-mvlevel]');
  if (l) { MV.level = l.dataset.mvlevel; window.renderMoves(); return; }
  const dn = e.target.closest('[data-mvdone]');
  if (dn) { const k = dn.dataset.mvdone; if (MV.done[k]) delete MV.done[k]; else MV.done[k] = new Date().toISOString().slice(0, 10); try { localStorage.setItem('moves-done', JSON.stringify(MV.done)); } catch (er) { /* storage unavailable */ } window.renderMoves(); return; }
  const t = e.target.closest('[data-mvtrack]');
  if (t) {
    const c = (MV.cards || []).find((x) => x.key === t.dataset.mvtrack);
    if (!c) return;
    t.disabled = true;
    await docsBoot();
    const m = await addTest({ kind: 'move', label: c.title, idea: c.actions[0] || '', source_ad_id: '', source_ad_name: c.owner });
    t.textContent = String(m).startsWith('Saved') ? 'Added' : 'Added for you';
  }
});
