'use strict';
// Campaigns, Insights and Competitors tabs. Uses the helpers and state from app.js
// ($, esc, fmt, money, VIEW, ENGINE, state, ...), which are defined by the time these run.
const INS = { open: new Set(), share: 0.5, haircut: 0.7 };

function pctOf(part, total) { return total ? (part / total * 100).toFixed(1) + '%' : ''; }
function signed(ch) { return `${ch > 0 ? '+' : ''}${(ch * 100).toFixed(0)}%`; }
function openLink(id, text) { return `<a href="#" data-open="${esc(id)}">${esc(text)}</a>`; }

// ---------- campaigns ----------
function campaignRows() { return ENGINE.campaignRollup(VIEW); }
window.renderCampaigns = function renderCampaigns() {
  const list = campaignRows(), total = VIEW.totals.spend, cmp = $('compare').checked && VIEW.previous.complete;
  const line = (x, kind) => {
    const m = x.metrics, p = cmp ? x.prev_metrics : null;
    const isC = kind === 'c', open = isC && INS.open.has(x.id);
    const nAds = isC ? x.adsets.reduce((s, a) => s + a.ads.length, 0) : x.ads.length;
    return `<tr class="${isC ? 'camp-row' : 'adset-row'}"${isC ? ` data-camp="${esc(x.id)}" aria-expanded="${open}"` : ''}>
      <td>${isC ? `<span class="caret">${open ? '▾' : '▸'}</span>` : ''}${esc(x.name)}${isC ? ` <span class="small muted">(${x.adsets.length} ad set${x.adsets.length > 1 ? 's' : ''})</span>` : ''}</td>
      <td class="n">${nAds}</td><td class="n">${fmt(m.spend, 'money')}</td><td class="n">${pctOf(m.spend, total)}</td>
      <td class="n">${fmt(m.purchase_value, 'money')}</td><td class="n">${fmt(m.roas, 'x')}</td><td class="n">${fmt(m.purchases, 'int')}</td><td class="n">${fmt(m.cpa, 'money')}</td>
      ${cmp ? `<td class="n">${p ? delta(m.spend, p.spend, 0) : '<span class="small muted">New</span>'}</td><td class="n">${p ? delta(m.roas, p.roas, 1) : ''}</td>` : ''}
      <td>${verdictChip(x.verdict)}</td></tr>`;
  };
  const body = list.map((c) => line(c, 'c') + (INS.open.has(c.id) ? c.adsets.map((s) => line(s, 's')).join('') : '')).join('');
  const sumSpend = list.reduce((s, c) => s + c.metrics.spend, 0);
  $('campaignsView').innerHTML = `<div class="ins"><section class="panel-box">
    <div class="row" style="justify-content: space-between"><div><h2>Campaigns and ad sets</h2>
      <p class="lead">${esc(dateLabel(VIEW.range.since))} to ${esc(dateLabel(VIEW.range.until))} · ${list.length} campaigns spent ${money(sumSpend)}. Click a campaign to see its ad sets. Exclusions apply.</p></div>
      <div class="row"><button class="btn ghost" type="button" data-act="expand">Open all</button><button class="btn ghost" type="button" data-act="collapse">Close all</button><button class="btn ghost" type="button" data-act="csv-camp">Export CSV</button></div></div>
    <div class="scroll"><table><tr><th>Campaign / ad set</th><th class="n">Ads</th><th class="n">Spend</th><th class="n">Share</th><th class="n">Purchase value</th><th class="n">ROAS</th><th class="n">Purchases</th><th class="n">CPA</th>${cmp ? '<th class="n">Spend change</th><th class="n">ROAS change</th>' : ''}<th>Verdict</th></tr>
      ${body}<tr class="total"><td>All campaigns</td><td class="n">${VIEW.totals.ads}</td><td class="n">${fmt(VIEW.totals.spend, 'money')}</td><td class="n">100%</td><td class="n">${fmt(VIEW.totals.purchase_value, 'money')}</td><td class="n">${fmt(VIEW.totals.roas, 'x')}</td><td class="n">${fmt(VIEW.totals.purchases, 'int')}</td><td class="n">${fmt(VIEW.totals.cpa, 'money')}</td>${cmp ? '<td></td><td></td>' : ''}<td></td></tr></table></div>
    <p class="small muted">Verdicts use the same targets as the ads (ROAS ${VIEW.targets.roas ? VIEW.targets.roas.toFixed(2) + 'x' : 'not set'}, ${esc(VIEW.targets.roas_source)}). ROAS = purchase value ÷ spend for that row.</p></section></div>`;
};
function exportCampaignsCsv() {
  const head = ['Level', 'Campaign', 'Ad set', 'Campaign ID', 'Ad set ID', 'Ads', 'Spend', 'Purchase value', 'ROAS', 'Purchases', 'CPA', 'Link CTR %', 'Prev spend', 'Prev ROAS', 'Verdict'];
  const out = [];
  const r = (lvl, c, s, x) => [lvl, c.name, s ? s.name : '', c.id, s ? s.id : '', s ? s.ads.length : c.adsets.reduce((t, a) => t + a.ads.length, 0), r2(x.metrics.spend), r2(x.metrics.purchase_value), r2(x.metrics.roas), x.metrics.purchases, r2(x.metrics.cpa), r2(x.metrics.link_ctr),
    x.prev_metrics ? r2(x.prev_metrics.spend) : null, x.prev_metrics ? r2(x.prev_metrics.roas) : null, x.verdict ? x.verdict.label : ''];
  for (const c of campaignRows()) { out.push(r('Campaign', c, null, c)); for (const s of c.adsets) out.push(r('Ad set', c, s, s)); }
  return downloadFile(`Gehna campaigns ${fileStamp()}.csv`, csv([head, ...out]));
}

// ---------- insights ----------
function weeklyChart(weeks, a, b) {
  const W = 1000, H = 190, L = 64, R = 10, T = 10, B = 24, n = weeks.length;
  const bw = (W - L - R) / n;
  const max = Math.max(...weeks.map((w) => w.spend + w.excl), 1);
  const y = (v) => T + (H - T - B) * (1 - v / max);
  const inRange = (w) => w.b >= a && w.a <= b;
  const band = weeks.map((w, i) => (inRange(w) ? `<rect class="band" x="${(L + i * bw).toFixed(1)}" y="${T}" width="${bw.toFixed(1)}" height="${H - T - B}"/>` : '')).join('');
  const bars = weeks.map((w, i) => {
    const x = (L + i * bw + 1).toFixed(1), wd = Math.max(1, bw - 2).toFixed(1);
    const tip = `Week of ${shortDate(w.start)}${w.days < 7 ? ` (${w.days} days)` : ''}: spend ${money(w.spend)}${w.excl ? `, excluded ${money(w.excl)}` : ''}, ROAS ${w.roas !== null ? w.roas.toFixed(2) + 'x' : 'unavailable'}`;
    return `<g><title>${esc(tip)}</title><rect x="${x}" y="${y(w.spend).toFixed(1)}" width="${wd}" height="${(H - B - y(w.spend)).toFixed(1)}" style="fill:var(--spend)"/>${w.excl ? `<rect x="${x}" y="${y(w.spend + w.excl).toFixed(1)}" width="${wd}" height="${(y(w.spend) - y(w.spend + w.excl)).toFixed(1)}" style="fill:var(--muted);opacity:.35"/>` : ''}</g>`;
  }).join('');
  const grid = [0, 0.5, 1].map((f) => `<line x1="${L}" x2="${W - R}" y1="${y(max * f).toFixed(1)}" y2="${y(max * f).toFixed(1)}" class="gl"/><text x="${L - 5}" y="${(y(max * f) + 3).toFixed(1)}" text-anchor="end" class="tl">${esc(money(max * f))}</text>`).join('');
  const ticks = weeks.map((w, i) => (i % 4 === 0 ? `<text x="${(L + i * bw).toFixed(1)}" y="${H - 6}" class="tl">${esc(shortDate(w.start))}</text>` : '')).join('');
  return `<figure class="wk"><svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Weekly spend">${band}${grid}${bars}${ticks}</svg></figure>`;
}
function weeklyRoasChart(weeks, a, b) {
  const W = 1000, H = 150, L = 64, R = 10, T = 10, B = 24, n = weeks.length;
  const bw = (W - L - R) / n;
  const vals = weeks.map((w) => w.roas).filter((v) => v !== null);
  const max = Math.max(...vals, 0.1);
  const y = (v) => T + (H - T - B) * (1 - v / max);
  const cx = (i) => L + i * bw + bw / 2;
  const band = weeks.map((w, i) => (w.b >= a && w.a <= b ? `<rect class="band" x="${(L + i * bw).toFixed(1)}" y="${T}" width="${bw.toFixed(1)}" height="${H - T - B}"/>` : '')).join('');
  const wpts = weeks.map((w, i) => (w.roas === null ? null : [cx(i), y(w.roas)]));
  const d = segmentsOf(wpts).map((s) => s.map((q, j) => `${j ? 'L' : 'M'}${q[0].toFixed(1)},${q[1].toFixed(1)}${s.length === 1 ? 'l0.01,0' : ''}`).join('')).join('') + bridgePath(wpts);
  const dots = weeks.map((w, i) => (w.roas === null ? '' : `<circle cx="${cx(i).toFixed(1)}" cy="${y(w.roas).toFixed(1)}" r="3" style="fill:var(--roas)"><title>Week of ${esc(shortDate(w.start))}: ${w.roas.toFixed(2)}x</title></circle>`)).join('');
  const grid = [0, 0.5, 1].map((f) => `<line x1="${L}" x2="${W - R}" y1="${y(max * f).toFixed(1)}" y2="${y(max * f).toFixed(1)}" class="gl"/><text x="${L - 5}" y="${(y(max * f) + 3).toFixed(1)}" text-anchor="end" class="tl">${(max * f).toFixed(1)}x</text>`).join('');
  const ticks = weeks.map((w, i) => (i % 4 === 0 ? `<text x="${(L + i * bw).toFixed(1)}" y="${H - 6}" class="tl">${esc(shortDate(w.start))}</text>` : '')).join('');
  return `<figure class="wk"><svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Weekly purchase ROAS">${band}${grid}<path d="${d}" style="fill:none;stroke:var(--roas)" stroke-width="2"/>${dots}${ticks}</svg></figure>`;
}

function anomalySection() {
  const list = ENGINE.anomalies(VIEW);
  const card = (x) => {
    const up = x.flags.every((f) => f.change > 0), down = x.flags.every((f) => f.change < 0);
    const txt = x.flags.map((f) => f.kind === 'spend' ? `Spend ${money(f.now)}, ${signed(f.change)} vs the usual ${money(f.usual)}` : `ROAS ${f.now.toFixed(2)}x, ${signed(f.change)} vs the usual ${f.usual.toFixed(2)}x`).join('. ');
    const drv = x.drivers.map((d) => `${openLink(d.id, d.name)} <span class="muted">${money(d.today)} vs ${money(d.usual)} a day</span>`).join('<br>');
    return `<div class="alert ${up ? 'up' : down ? 'down' : ''}"><strong>${esc(dateLabel(x.date))}</strong><span>${esc(txt)}.</span>${drv ? `<span class="small">Biggest spend moves:<br>${drv}</span>` : ''}</div>`;
  };
  return `<section class="panel-box" id="ins-alerts"><h2>Anomaly alerts</h2>
    <p class="lead">Days in the selected dates where account spend or ROAS moved 50% or more against the median of the 14 days before. Largest 12 shown, newest first.</p>
    ${list.length ? `<div class="alerts">${list.map(card).join('')}</div>` : '<p class="small muted">No sharp moves in these dates.</p>'}
    <p class="small muted">A spike can be a sale day or a new launch. Check it before acting. ROAS alerts are skipped on days with very low spend.</p></section>`;
}
function weeklySection() {
  const weeks = ENGINE.weekly(state.kw, state.camp);
  const [a, b] = ENGINE.resolveRange(VIEW.range.since, VIEW.range.until);
  const last = weeks[weeks.length - 1];
  return `<section class="panel-box" id="ins-weekly"><h2>Weekly trend</h2>
    <p class="lead">The whole year, one bar per week starting Monday. The shaded weeks overlap the dates you picked.${last && last.days < 7 ? ` The last week has only ${last.days} days.` : ''}</p>
    <div class="legend"><span><i style="background:var(--spend)"></i>Spend</span><span><i style="background:var(--muted);opacity:.35"></i>Excluded campaigns</span><span><i style="background:var(--accent-soft)"></i>Selected dates</span></div>
    ${weeklyChart(weeks, a, b)}
    <div class="legend"><span><i style="background:var(--roas)"></i>Purchase ROAS for the week (included campaigns)</span></div>
    ${weeklyRoasChart(weeks, a, b)}</section>`;
}
function budgetSection() {
  const r = ENGINE.budgetShift(VIEW, INS.share, INS.haircut);
  const opt = (vals, cur, lab) => vals.map((v) => `<option value="${v}"${v === cur ? ' selected' : ''}>${lab(v)}</option>`).join('');
  const rows = (list, kind) => list.sort((p, q) => q.daily - p.daily).map((x) => `<tr><td>${openLink(x.id, x.name)}</td><td class="n">${fmt(x.roas, 'x')}</td><td class="n">${money(x.daily)}</td><td class="n">${money(x.new_daily)}</td><td class="n">${kind === 'cut' ? '−' : '+'}${money(Math.abs(x.new_daily - x.daily))}</td></tr>`).join('');
  const head = '<tr><th>Ad</th><th class="n">ROAS (dates)</th><th class="n">Now a day</th><th class="n">Suggested</th><th class="n">Change</th></tr>';
  const enough = r.cut.length && r.scale.length;
  return `<section class="panel-box" id="ins-budget"><h2>Budget shift suggestions</h2>
    <p class="lead">Take part of the daily spend from running ads marked Cut and give it to running ads marked Scale, split by their current spend. Daily spend is the average of ${esc(shortDate(r.window[0]))} to ${esc(shortDate(r.window[1]))}.</p>
    <div class="ctl"><label class="field">Move this much of Cut spend <select id="bsShare">${opt([0.25, 0.5, 0.75, 1], INS.share, (v) => `${v * 100}%`)}</select></label>
      <label class="field">Assume Scale ads keep <select id="bsHair">${opt([0.5, 0.7, 0.9, 1], INS.haircut, (v) => `${v * 100}% of their ROAS`)}</select></label></div>
    ${enough ? `<div class="box"><strong>Move ${money(r.moved_daily)} a day</strong> from ${r.cut.length} Cut ad${r.cut.length > 1 ? 's' : ''} (ROAS ${fmt(r.cut_roas, 'x')}) to ${r.scale.length} Scale ad${r.scale.length > 1 ? 's' : ''} (ROAS ${fmt(r.scale_roas, 'x')}).
      ${r.value_gain_daily !== null ? `Rough extra purchase value: ${money(r.value_gain_daily)} a day, about ${money(r.value_gain_30d)} over 30 days.` : ''}</div>
      <div class="two" style="margin-top: 10px"><div><h3>Lower (${r.cut.length})</h3><div class="scroll"><table>${head}${rows(r.cut, 'cut')}</table></div></div>
      <div><h3>Raise (${r.scale.length})</h3><div class="scroll"><table>${head}${rows(r.scale, 'scale')}</table></div></div></div>`
    : '<p class="small muted">No shift to suggest. It needs at least 1 running Cut ad and 1 running Scale ad in the top 100.</p>'}
    <p class="small muted">A guide, not a forecast. Ads usually get less efficient as spend grows, which is why the Scale ROAS is reduced. Meta sets spend per ad set, not per ad, so make the change at ad set level. This page cannot change budgets.</p></section>`;
}
function themesSection() {
  const t = ENGINE.themes(VIEW);
  return `<section class="panel-box" id="ins-themes"><h2>Creative themes</h2>
    <p class="lead">Every ad that spent in these dates, grouped by tag. Tags come from the ad name, campaign name and copy, so they can be wrong. Open an ad to see why it got its tag.</p>
    <h3>Angle</h3><div class="scroll">${themeTable(t.angle, 'Angle')}</div>
    <h3 style="margin-top: 14px">Product</h3><div class="scroll">${themeTable(t.product, 'Product')}</div>
    <h3 style="margin-top: 14px">Opening line</h3><div class="scroll">${themeTable(t.hook, 'Opening line')}</div></section>`;
}
function videoInsSection() {
  const { rows, avg } = ENGINE.videoTable(VIEW);
  const shown = rows.slice(0, 30);
  const body = shown.map((r) => {
    const v = r.video;
    return `<tr><td>${openLink(r.id, r.name)}${v.mostly_image ? ' <span class="chip flag" title="The video played in under 20% of impressions">Mostly shown as image</span>' : ''}</td>
      <td class="n">${fmt(r.metrics.spend, 'money')}</td><td class="n">${fmt(v.video_share, 'pct')}</td><td class="n">${fmt(v.hook_rate, 'pct')}</td><td class="n">${fmt(v.hold_rate, 'pct')}</td>
      <td class="n">${v.avg_watch !== null ? v.avg_watch.toFixed(1) + 's' : NA}</td><td class="n">${fmt(v.p25, 'pct')}</td><td class="n">${fmt(v.p100, 'pct')}</td><td class="n">${fmt(r.metrics.roas, 'x')}</td></tr>`;
  }).join('');
  return `<section class="panel-box" id="ins-video"><div class="row" style="justify-content: space-between"><h2>Video metrics</h2><button class="btn ghost" type="button" data-act="csv-video">Export CSV</button></div>
    <p class="lead">${rows.length} ads with video spent in these dates${rows.length > 30 ? ', top 30 by spend shown' : ''}. Average hook rate ${fmt(avg.hook_rate, 'pct')}, hold rate ${fmt(avg.hold_rate, 'pct')} (ads mostly shown as image left out of the averages).</p>
    ${rows.length ? `<div class="scroll"><table><tr><th>Ad</th><th class="n">Spend</th><th class="n">Video played</th><th class="n">Hook rate</th><th class="n">Hold rate</th><th class="n">Avg watch</th><th class="n">Reached 25%</th><th class="n">Reached 100%</th><th class="n">ROAS</th></tr>${body}</table></div>` : '<p class="small muted">No video ads spent in these dates.</p>'}
    <p class="small muted">Hook rate = 3-second plays ÷ impressions. Hold rate = ThruPlays ÷ 3-second plays. Video played = video starts ÷ impressions; flexible ads often show a still image instead. Reached 25% and 100% are shares of video starts.</p></section>`;
}
function exportVideoCsv() {
  const { rows } = ENGINE.videoTable(VIEW);
  const head = ['Ad ID', 'Ad name', 'Campaign', 'Spend', 'Impressions', 'Video starts', 'Video played %', '3-second plays (derived)', 'ThruPlays', 'Hook rate %', 'Hold rate %', 'Avg watch s', 'Reached 25 %', 'Reached 50 %', 'Reached 75 %', 'Reached 100 %', 'ROAS', 'Mostly shown as image'];
  const out = rows.map((r) => { const v = r.video; return [r.id, r.name, r.campaign, r2(r.metrics.spend), v.impressions, v.starts, r2(v.video_share), r2(v.plays_3s), v.thruplays, r2(v.hook_rate), r2(v.hold_rate), r2(v.avg_watch), r2(v.p25), r2(v.p50), r2(v.p75), r2(v.p100), r2(r.metrics.roas), v.mostly_image ? 'yes' : 'no']; });
  return downloadFile(`Gehna video ${fileStamp()}.csv`, csv([head, ...out]));
}
function lifecycleInsSection() {
  const s = ENGINE.lifecycleSummary(VIEW);
  const d = (v) => (v === null ? NA : `${Math.round(v)} days`);
  return `<section class="panel-box" id="ins-life"><h2>Creative lifecycle</h2>
    <p class="lead">Across the whole year, for ads that spent at least ${money(s.cpa)} (1 year CPA). Peak = the best 7-day ROAS. Fatigue = the first day 7-day ROAS fell below half the peak.</p>
    <div class="scroll"><table><tr><th>Format</th><th class="n">Ads</th><th class="n">Median days with spend</th><th class="n">Median days to peak</th><th class="n">Median days to fatigue</th><th class="n">Ads that fatigued</th></tr>
      ${s.formats.map((f) => `<tr><td>${esc(f.format)}</td><td class="n">${f.ads}</td><td class="n">${d(f.median_days_live)}</td><td class="n">${d(f.median_days_to_peak)}</td><td class="n">${d(f.median_days_to_fatigue)}</td><td class="n">${f.fatigued}</td></tr>`).join('')}</table></div>
    <h3 style="margin-top: 14px">Worth relaunching (${s.relaunch.length})</h3>
    <p class="small muted">Stopped at least 21 days ago, spent at least 3x the year CPA, and had lifetime ROAS at least 20% above the year average (${fmt(s.year_roas, 'x')}).</p>
    ${s.relaunch.length ? `<div class="scroll"><table><tr><th>Ad</th><th>Format</th><th class="n">Lifetime spend</th><th class="n">Lifetime ROAS</th><th class="n">Days with spend</th><th>Last spend</th></tr>
      ${s.relaunch.map((r) => `<tr><td>${openLink(r.id, r.name)}</td><td>${esc(r.format)}</td><td class="n">${fmt(r.lifetime.spend, 'money')}</td><td class="n">${fmt(r.lifetime.roas, 'x')}</td><td class="n">${r.days_live}</td><td>${esc(dateLabel(r.last_day))}</td></tr>`).join('')}</table></div>` : '<p class="small muted">None found.</p>'}
    <p class="small muted">Lifecycle ignores the date picker but follows the exclusions.</p></section>`;
}
function dayPlatformSection() {
  const dow = ENGINE.dayOfWeek(VIEW.range.since, VIEW.range.until, state.kw, state.camp);
  const maxSpend = Math.max(...dow.map((x) => x.spend_per_day), 1), maxRoas = Math.max(...dow.map((x) => x.roas || 0), 0.01);
  const bar = (v, max, cls) => `<span class="btrack" style="display:block;min-width:60px">${v ? `<span class="bar-fill ${cls}" style="width:${Math.max(2, v / max * 100)}%"></span>` : ''}</span>`;
  const plat = VIEW.demographics_all.publisher_platform || {};
  const pRows = Object.entries(plat).map(([k, v]) => ({ key: k, ...v })).filter((r) => r.spend > 0).sort((p, q) => q.spend - p.spend);
  const pTotal = pRows.reduce((s, r) => s + r.spend, 0);
  const months = ENGINE.platformByMonth(state.kw, state.camp);
  const keys = pRows.map((r) => r.key);
  for (const m of months) for (const k of Object.keys(m.rows)) if (!keys.includes(k)) keys.push(k);
  const label = (k) => k.replace(/_/g, ' ');
  const mTable = months.map((m) => {
    const tot = Object.values(m.rows).reduce((s, x) => s + x.spend, 0);
    return `<tr><td>${esc(new Date(m.start + 'T00:00:00Z').toLocaleDateString('en-IN', { month: 'short', year: 'numeric', timeZone: 'UTC' }))}</td><td class="n">${money(tot)}</td>${keys.map((k) => { const x = m.rows[k]; return `<td class="n">${x && x.spend ? `${pctOf(x.spend, tot)}<br><span class="small muted">${x.reported ? (x.value / x.spend).toFixed(2) + 'x' : 'n/a'}</span>` : ''}</td>`; }).join('')}</tr>`;
  }).join('');
  return `<section class="panel-box" id="ins-day"><h2>Day of week and platform</h2>
    <div class="two"><div><h3>Day of week, selected dates</h3>
      <div class="scroll"><table><tr><th>Day</th><th class="n">Days</th><th class="n">Spend a day</th><th></th><th class="n">ROAS</th><th></th></tr>
      ${dow.map((x) => `<tr><td>${esc(x.key)}</td><td class="n">${x.days}</td><td class="n">${money(x.spend_per_day)}</td><td style="width:22%">${bar(x.spend_per_day, maxSpend, 'spend')}</td><td class="n">${fmt(x.roas, 'x')}</td><td style="width:22%">${bar(x.roas, maxRoas, 'roas')}</td></tr>`).join('')}</table></div>
      <p class="small muted">From daily totals of the included campaigns. Sale days can skew a weekday when the range is short.</p></div>
    <div><h3>Platform</h3>${breakdownTable(Object.fromEntries(pRows.map((r) => [r.key, r])), 'Platform', pTotal)}
      <p class="small muted">${esc(bucketNote(VIEW.demographics_buckets, VIEW.demographics_exact, VIEW.range))} A split of the same spend, not extra results.</p></div></div>
    <h3 style="margin-top: 14px">Platform share of spend by month (ROAS below)</h3>
    <div class="scroll"><table><tr><th>Month</th><th class="n">Spend</th>${keys.map((k) => `<th class="n">${esc(label(k))}</th>`).join('')}</tr>${mTable}</table></div></section>`;
}
window.renderInsights = function renderInsights() {
  $('insightsView').innerHTML = `<div class="ins">
    <nav class="ins-nav" aria-label="Insights sections"><a href="#ins-alerts">Alerts</a><a href="#ins-weekly">Weekly trend</a><a href="#ins-budget">Budget shift</a><a href="#ins-themes">Themes</a><a href="#ins-video">Video</a><a href="#ins-life">Lifecycle</a><a href="#ins-day">Day and platform</a></nav>
    ${anomalySection()}${weeklySection()}${budgetSection()}${themesSection()}${videoInsSection()}${lifecycleInsSection()}${dayPlatformSection()}</div>`;
};

// ---------- competitors ----------
// Each competitor ad is shown in the page from the saved Ad Library snapshot (image, text, CTA).
const COMPV = { brand: '', fmt: '' };
function compId(url) { const m = /[?&]id=(\d+)/.exec(url || ''); return m ? m[1] : ''; }
function compMedia(id) { return (id && COMP_MEDIA && COMP_MEDIA[id]) || null; }
const isCatalog = (md) => /\{\{\s*product\./.test(`${md.meta.title || ''} ${md.meta.body || ''}`);
function compFormat(md) {
  if (!md || !md.meta) return { key: '', label: 'Format unknown' };
  if (isCatalog(md)) return { key: 'catalog', label: 'Catalog (Meta picks products)' };
  if (md.meta.video) return { key: 'video', label: 'Video' };
  if ((md.meta.cards || 0) > 1) return { key: 'carousel', label: `Carousel, ${md.meta.cards} cards` };
  return { key: 'image', label: 'Image' };
}
// Opportunity score: how proven the ad is (days live, capped at 180) and how hard they are pushing it (versions live).
function compScore(m) {
  const proof = Math.min(m.days_running || 0, 180) / 180, push = Math.min(m.variants || 1, 5) / 5;
  return Math.round(100 * (0.65 * proof + 0.35 * push));
}
function compWhy(m) {
  const out = [];
  if (m.days_running >= 90) out.push(`Live ${m.days_running} days. Ads kept this long usually pay back.`);
  else if (m.days_running >= 30) out.push(`Live ${m.days_running} days. Past the usual test window.`);
  else out.push(`Live ${m.days_running} days. Still new, so treat it as a test.`);
  if (m.variants >= 3) out.push(`${m.variants} versions running, so they are putting money behind it.`);
  else if (m.variants === 2) out.push('2 versions running.');
  return out;
}
// Every sampled competitor ad, flat, with a stable key used by the builder.
function compItems() {
  const c = COMPETITORS;
  if (!c || !c.brands) return [];
  const out = [];
  c.brands.forEach((b) => b.messages.forEach((m) => {
    const id = compId(m.url), md = compMedia(id), f = compFormat(md);
    out.push({ key: id || `${b.name}|${m.headline}|${m.started}`, id, brand: b.name, m, md, fmt: f, score: compScore(m) });
  }));
  return out;
}
function compTitle(it) {
  if (it.md && it.md.meta && isCatalog(it.md)) return 'Catalog ad. Meta fills in each product.';
  const t = it.md && it.md.meta && it.md.meta.title;
  const h = t || (it.m.headline !== '(no headline)' ? it.m.headline : '') || 'No headline';
  return h.length > 140 ? h.slice(0, 140) + '…' : h;
}
function compImg(it, cls) {
  return it.md && it.md.img ? `<img class="${cls}" src="data:image/jpeg;base64,${it.md.img}" alt="${esc(it.brand)} ad: ${esc(compTitle(it))}" loading="lazy">`
    : `<div class="${cls} cimg-none">Preview unavailable</div>`;
}
function compCard(it) {
  const md = it.md, meta = (md && md.meta) || {}, body = meta.body || '';
  return `<article class="ccard" data-ckey="${esc(it.key)}">
    ${compImg(it, 'cimg')}
    <div class="ccard-body">
      <div class="row" style="gap:6px"><span class="chip fmt">${esc(it.fmt.label)}</span>${meta.cta ? `<span class="chip tag">${esc(meta.cta)}</span>` : ''}<span class="chip">Score ${it.score}</span></div>
      <b class="ctitle">${esc(compTitle(it))}</b>
      ${body ? `<p class="cbody small">${esc(body)}</p>` : ''}
      <span class="small muted">Live ${it.m.days_running} days, since ${esc(dateLabel(it.m.started))} · ${it.m.variants} version${it.m.variants > 1 ? 's' : ''}</span>
      <div class="row" style="gap:8px;align-items:center"><button class="btn ghost small-btn" type="button" data-cref="${esc(it.key)}">Use as reference</button>${link(it.m.url, 'View in Ad Library')}</div>
    </div></article>`;
}
function compMix(items) {
  const n = (k) => items.filter((x) => x.fmt.key === k).length;
  const parts = [['image', 'image'], ['carousel', 'carousel'], ['catalog', 'catalog'], ['video', 'video']].map(([k, l]) => (n(k) ? `${n(k)} ${l}` : '')).filter(Boolean);
  const unk = items.filter((x) => !x.fmt.key).length;
  return parts.join(', ') + (unk ? `${parts.length ? ', ' : ''}${unk} without a preview` : '');
}
function compTopHtml(items, brand) {
  const top = [...items].sort((a, b) => b.score - a.score || b.m.days_running - a.m.days_running).slice(0, brand ? 5 : 8);
  if (!top.length) return '';
  return `<section class="panel-box" id="comp-top"><h2>Top ideas to borrow${brand ? ` from ${esc(brand)}` : ''}</h2>
    <p class="lead">Ranked by how long each ad has run and how many versions are live. Meta shows no spend or sales for competitor ads, so this is a signal, not proof.</p>
    <ol class="crank">${top.map((it, i) => `<li><span class="crank-n">${i + 1}</span>${compImg(it, 'crank-img')}<span class="crank-t"><b>${esc(it.brand)}</b><span class="small">${esc(compTitle(it))}</span><span class="small muted">${esc(it.fmt.label)} · ${compWhy(it.m).join(' ')}</span></span><span class="crank-s">${it.score}<span>score</span></span><button class="btn ghost small-btn" type="button" data-cref="${esc(it.key)}">Use as reference</button></li>`).join('')}</ol></section>`;
}
// One row of numbers per brand, so brands can be compared side by side.
const OFFER_RE = /\d+\s?%|\boff\b|making charges?|flat ₹|discount|sale\b|free\b/i;
function compProfile(b, mine) {
  const n = mine.length || 1, fk = (k) => mine.filter((x) => x.fmt.key === k).length / n;
  const days = mine.map((x) => x.m.days_running).sort((p, q) => p - q);
  const offers = mine.filter((x) => OFFER_RE.test(`${compTitle(x)} ${(x.md && x.md.meta && x.md.meta.body) || ''}`)).length / n;
  const ctas = {};
  mine.forEach((x) => { const c = x.md && x.md.meta && x.md.meta.cta; if (c) ctas[c] = (ctas[c] || 0) + 1; });
  const topCta = Object.entries(ctas).sort((p, q) => q[1] - p[1])[0];
  const newN = mine.filter((x) => x.m.days_running <= 14).length;
  return { name: b.name, active: b.active_ads_estimate, sampled: mine.length, img: fk('image'), car: fk('carousel'), cat: fk('catalog'), vid: fk('video'),
    median: days.length ? days[Math.floor(days.length / 2)] : null, longest: days.length ? days[days.length - 1] : null, offers, cta: topCta ? topCta[0] : '', newN };
}
const pct0 = (v) => Math.round(v * 100) + '%';
function compTableHtml(profiles) {
  return `<section class="panel-box"><h2>Brands side by side</h2><p class="lead">From the ads sampled for each brand. Click a brand to see only its ads.</p>
    <div class="scroll"><table class="sdtable"><tr><th>Brand</th><th class="n">Active ads</th><th class="n">Image</th><th class="n">Carousel</th><th class="n">Catalog</th><th class="n">Video</th><th class="n">Median days live</th><th class="n">Longest</th><th class="n">New in 14 days</th><th class="n">Push an offer</th><th>Main button</th></tr>
    ${profiles.map((p) => `<tr><td><button type="button" class="linkbtn" data-cbrand="${esc(p.name)}">${esc(p.name)}</button></td><td class="n">${p.active ?? '–'}</td><td class="n">${pct0(p.img)}</td><td class="n">${pct0(p.car)}</td><td class="n">${pct0(p.cat)}</td><td class="n">${pct0(p.vid)}</td><td class="n">${p.median ?? '–'}</td><td class="n">${p.longest ?? '–'}</td><td class="n">${p.newN} of ${p.sampled}</td><td class="n">${pct0(p.offers)}</td><td>${esc(p.cta || '–')}</td></tr>`).join('')}</table></div>
    <p class="small muted">Formats do not add to 100% when some ads have no preview. "Push an offer" means the headline or text mentions a percent, off, making charges, a discount, a sale or free. A brand whose ads are all new may be testing hard or may have restarted its ads.</p></section>`;
}
function compBrandHtml(p, b) {
  const tile = (label, v, sub) => `<div><em>${esc(label)}</em><b>${v}</b><span>${esc(sub)}</span></div>`;
  return `<section class="panel-box"><div class="row" style="justify-content: space-between"><h2>${esc(p.name)}</h2>${link(b.library_url, 'Open in Ad Library')}</div>
    <div class="act-stats">${tile('Active ads', p.active ?? '–', `${p.sampled} sampled here`)}${tile('Median days live', p.median ?? '–', `Longest ${p.longest ?? '–'} days`)}${tile('New in 14 days', p.newN, `of ${p.sampled} sampled`)}${tile('Push an offer', pct0(p.offers), 'of sampled ads')}</div>
    <p class="small">Formats: ${pct0(p.img)} image, ${pct0(p.car)} carousel, ${pct0(p.cat)} catalog, ${pct0(p.vid)} video. Main button: ${esc(p.cta || 'none')}.</p></section>`;
}
// Gap and festive watch: what rivals push now that Gehna does not (compwatch.json).
let COMPWATCH;
function compWatchHtml() {
  if (COMPWATCH === undefined) {
    COMPWATCH = null;
    fetch('compwatch.json').then((r) => (r.ok ? r.json() : null)).then((j) => { COMPWATCH = j && Array.isArray(j.gaps) ? j : null; if (COMPWATCH && state.tab === 'competitors') window.renderCompetitors(); }).catch(() => {});
    return '';
  }
  const w = COMPWATCH;
  if (!w) return '';
  const text = ['Competitor gap and festive watch', ...w.gaps.map((g) => `- ${g.title}: ${g.text}`), '', 'Offers live now:', ...w.brands.filter((b) => b.offers.length).map((b) => `- ${b.name}: ${b.offers.join('; ')}`)].join('\n');
  return `<section class="panel-box"><div class="row" style="justify-content: space-between"><h2>Gaps and festive watch</h2>${copyBtn(text)}</div>
    <p class="small muted">Active ads in India on ${esc(dateLabel(w.captured_at))}. Ad Library shows no spend or results.</p>
    <ul class="hl-find">${w.gaps.map((g) => `<li><b>${esc(g.title)}.</b> ${esc(g.text)}</li>`).join('')}</ul>
    <div class="scroll"><table class="bd-table"><tr><th>Brand</th><th class="n">Live ads</th><th>Offers now</th><th>Themes</th></tr>
    ${w.brands.map((b) => `<tr><td>${esc(b.name)}</td><td class="n">${b.active}</td><td class="small">${esc(b.offers.join('; ') || 'No offer')}</td><td class="small">${esc(b.themes.join('; '))}</td></tr>`).join('')}</table></div></section>`;
}
window.renderCompetitors = function renderCompetitors() {
  const c = COMPETITORS;
  if (!c || !c.brands) { $('competitorsView').innerHTML = '<p class="muted">No competitor snapshot loaded.</p>'; return; }
  const all = compItems();
  if (COMPV.brand && !c.brands.some((b) => b.name === COMPV.brand)) COMPV.brand = '';
  const keep = (it) => (!COMPV.brand || it.brand === COMPV.brand) && (!COMPV.fmt || it.fmt.key === COMPV.fmt);
  const brands = c.brands.filter((b) => !COMPV.brand || b.name === COMPV.brand);
  const profiles = c.brands.map((b) => compProfile(b, all.filter((x) => x.brand === b.name)));
  const brandSec = (b) => {
    const mine = all.filter((x) => x.brand === b.name), shown = mine.filter(keep).sort((p, q) => q.m.days_running - p.m.days_running);
    return `<section class="panel-box"><div class="row" style="justify-content: space-between"><h2>${esc(b.name)}</h2>${link(b.library_url, 'Open in Ad Library')}</div>
      <p class="lead">About ${b.active_ads_estimate} active ads. ${mine.length} different ads in the ${b.sampled} sampled: ${esc(compMix(mine))}. Longest running first.</p>
      ${shown.length ? `<div class="cgrid">${shown.map(compCard).join('')}</div>` : '<p class="small muted">No ads match this filter.</p>'}</section>`;
  };
  const chip = (attr, val, cur, label) => `<button type="button" class="fchip${cur === val ? ' on' : ''}" data-${attr}="${esc(val)}" aria-pressed="${cur === val}">${esc(label)}</button>`;
  const pill = (name, count) => `<button type="button" class="bpill${COMPV.brand === name ? ' on' : ''}" data-cbrand="${esc(name)}" aria-pressed="${COMPV.brand === name}">${name ? `<span class="monogram">${esc(name.replace(/^Mia by /, '').slice(0, 1))}</span>` : ''}<span>${esc(name || 'All brands')}</span><em>${count}</em></button>`;
  const cur = COMPV.brand ? c.brands.find((b) => b.name === COMPV.brand) : null;
  const items = all.filter((x) => !COMPV.brand || x.brand === COMPV.brand);
  $('competitorsView').innerHTML = `<div class="ins">
    <div class="bpills" role="group" aria-label="Pick a competitor">${pill('', c.brands.length)}${c.brands.map((b) => pill(b.name, b.active_ads_estimate ?? '–')).join('')}</div>
    <div class="note">${esc(c.note)} Snapshot of ${esc(c.status)} ads in ${esc(c.country)}, taken ${esc(dateLabel(c.captured_at))}.</div>
    ${compWatchHtml()}
    ${cur ? compBrandHtml(profiles.find((p) => p.name === cur.name), cur) : compTableHtml(profiles)}
    ${compTopHtml(items, cur ? cur.name : '')}
    <div class="cfilters" role="group" aria-label="Filter by format"><span class="small muted">Format</span>${chip('cfmt', '', COMPV.fmt, 'All')}${chip('cfmt', 'image', COMPV.fmt, 'Image')}${chip('cfmt', 'carousel', COMPV.fmt, 'Carousel')}${chip('cfmt', 'catalog', COMPV.fmt, 'Catalog')}${chip('cfmt', 'video', COMPV.fmt, 'Video')}</div>
    <div class="brands">${brands.map(brandSec).join('')}</div></div>`;
};

window.initInsights = function initInsights() {
  $('campaignsView').addEventListener('click', (e) => {
    const act = e.target.closest('[data-act]');
    if (act) {
      if (act.dataset.act === 'expand') campaignRows().forEach((c) => INS.open.add(c.id));
      if (act.dataset.act === 'collapse') INS.open.clear();
      if (act.dataset.act === 'csv-camp') { exportCampaignsCsv(); return; }
      window.renderCampaigns(); return;
    }
    const row = e.target.closest('tr.camp-row');
    if (row) { const id = row.dataset.camp; if (INS.open.has(id)) INS.open.delete(id); else INS.open.add(id); window.renderCampaigns(); }
  });
  $('insightsView').addEventListener('click', (e) => {
    const a = e.target.closest('[data-open]');
    if (a) { e.preventDefault(); openSide(a.dataset.open); return; }
    const act = e.target.closest('[data-act]');
    if (act && act.dataset.act === 'csv-video') exportVideoCsv();
    const nav = e.target.closest('.ins-nav a');
    if (nav) { e.preventDefault(); const t = document.querySelector(nav.getAttribute('href')); if (t) t.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
  });
  $('insightsView').addEventListener('change', (e) => {
    if (e.target.id === 'bsShare') INS.share = parseFloat(e.target.value);
    else if (e.target.id === 'bsHair') INS.haircut = parseFloat(e.target.value);
    else return;
    const sec = $('ins-budget');
    if (sec) sec.outerHTML = budgetSection();
  });
};
