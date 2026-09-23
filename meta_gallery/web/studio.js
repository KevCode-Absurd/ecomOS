'use strict';
// Action plan, Creative studio (brand kit, playbook, test tracker), format x audience,
// and "Build this for Gehna" on the Competitors tab. Uses helpers from app.js, overview.js and lab.js.
const AGE_KEYS = ['18-24', '25-34', '35-44', '45-54', '55-64', '65+'];
const STUDIO = { busy: {}, comp: {}, refRole: 'layout', hint: '' };

function doneKey(kind, id) { return `gallery-done:${VIEW ? VIEW.range.until : ''}:${kind}:${id}`; }
function isDone(kind, id) { try { return localStorage.getItem(doneKey(kind, id)) === '1'; } catch (e) { return false; } }
function setDone(kind, id, on) { try { if (on) localStorage.setItem(doneKey(kind, id), '1'); else localStorage.removeItem(doneKey(kind, id)); } catch (e) { /* storage unavailable */ } }
const roasTxt = (v) => (v === null || v === undefined ? 'no sales' : v.toFixed(2) + 'x');

// ---------- format x audience heatmap ----------
function heatCell(c, max) {
  if (!c || c.spend <= 0) return '<td class="heat na-cell">·</td>';
  if (c.roas === null) return `<td class="heat" data-tip="${esc(`No sales reported|Spend|${money(c.spend)}`)}"><b>0 sales</b><span>${compact(c.spend)}</span></td>`;
  const t = Math.max(0, Math.min(1, c.roas / max));
  return `<td class="heat" style="background:color-mix(in srgb, var(--gold) ${Math.round(8 + t * 80)}%, var(--surface))" data-tip="${esc(`ROAS|${c.roas.toFixed(2)}x|Spend|${money(c.spend)}|Purchases|${c.purchases ?? 0}`)}"><b>${c.roas.toFixed(1)}x</b><span>${compact(c.spend)}</span></td>`;
}
function heatTable(fa, dim, keys) {
  const rows = Object.entries(fa[dim]).map(([f, cells]) => ({ f, cells, spend: Object.values(cells).reduce((s, c) => s + c.spend, 0) })).filter((r) => r.spend > 0).sort((a, b) => b.spend - a.spend);
  const cols = keys.filter((k) => rows.some((r) => r.cells[k] && r.cells[k].spend > 0));
  const max = Math.max(...rows.flatMap((r) => cols.map((k) => (r.cells[k] && r.cells[k].roas) || 0)), 1);
  return `<div class="scroll"><table class="heatmap"><tr><th>Format</th>${cols.map((k) => `<th class="n">${esc(k)}</th>`).join('')}</tr>${rows.map((r) => `<tr><td>${esc(DATA.meta.format_labels[r.f] || r.f)}</td>${cols.map((k) => heatCell(r.cells[k], max)).join('')}</tr>`).join('')}</table></div>`;
}
function formatAudienceSection() {
  const fa = ENGINE.formatAudience(VIEW);
  return `<section class="panel-box" id="ins-fa"><h2>Format by age and gender</h2>
    <p class="lead">ROAS for each format and audience. Darker gold means higher ROAS. The small number is spend. ${esc(bucketNote(fa.buckets, VIEW.demographics_exact, VIEW.range))}</p>
    <div class="two"><div><h3>Age</h3>${heatTable(fa, 'age', AGE_KEYS)}</div><div><h3>Gender</h3>${heatTable(fa, 'gender', ['female', 'male', 'unknown'])}</div></div>
    <p class="small muted">A split of the same spend. Small cells can swing a lot, so check spend before acting.</p></section>`;
}
const baseRenderInsights = window.renderInsights;
window.renderInsights = function () {
  baseRenderInsights();
  const nav = document.querySelector('#insightsView .ins-nav');
  if (nav && !nav.querySelector('[href="#ins-fa"]')) nav.insertAdjacentHTML('beforeend', '<a href="#ins-fa">Format by audience</a>');
  const weekly = $('ins-weekly');
  if (weekly) weekly.insertAdjacentHTML('afterend', formatAudienceSection());
};

// ---------- action plan ----------
function actCard(kind, x, { title, why, action, numbers, extra = '' }) {
  const done = isDone(kind, x.id);
  return `<article class="act${done ? ' done' : ''}" data-kind="${kind}" data-id="${esc(x.id)}">
    <div class="act-th">${thumbHtml(x.id, x.name)}</div>
    <div class="act-body">
      <div class="act-top"><strong class="act-title">${esc(title)}</strong><label class="act-done"><input type="checkbox" data-done="${kind}|${esc(x.id)}"${done ? ' checked' : ''}> Done</label></div>
      <div class="act-name" title="${esc(x.name)}">${esc(x.name)} <span class="muted">· ${esc(x.format)}</span></div>
      <div class="small muted act-camp" title="${esc(x.campaign || '')}">${esc(x.campaign || '')}</div>
      <div class="act-nums">${numbers.map(([l, v]) => `<span><em>${esc(l)}</em>${v}</span>`).join('')}</div>
      <p class="act-why">${why}</p>
      <p class="act-do"><b>Do this:</b> ${action}</p>${extra}
      <div class="act-btns"><button class="btn" type="button" data-act-open="${esc(x.id)}">${x.type === 'static_image' ? 'Open and make variants' : 'Open ad'}</button><button class="btn ghost" type="button" data-act-test="${kind}|${esc(x.id)}">Add to tests</button></div>
    </div></article>`;
}
function actSection(id, title, sub, items) {
  if (!items.length) return '';
  return `<section class="act-sec" id="${id}"><div class="act-head"><h2>${title}</h2><span class="muted small">${sub}</span></div><div class="act-grid">${items.join('')}</div></section>`;
}
function planText(o) {
  const L = [`Gehna ads plan, ${shortDate(o.window[0])} to ${shortDate(o.window[1])}`];
  const add = (h, xs, f) => { if (xs.length) { L.push('', h); xs.forEach((x) => L.push('- ' + f(x))); } };
  add('Scale', o.scale, (x) => `${x.name}: ROAS ${roasTxt(x.m7.roas)} last 7 days. Raise budget about 20%.`);
  add('Hidden gems (own budget + variants)', o.gems, (x) => `${x.name}: ROAS ${roasTxt(x.m30.roas)} on only ${money(x.m30.spend)} in 30 days. Try ${money(x.suggest_daily)}/day in its own ad set.`);
  add('Pause or fix', o.pause, (x) => `${x.name}: ${money(x.m7.spend)} this week at ROAS ${roasTxt(x.m7.roas)}.`);
  add('Refresh', o.tired, (x) => `${x.name}: ${x.fatigue.reason}`);
  if (o.bet) L.push('', `Format to test more: ${o.bet.label}, ROAS ${roasTxt(o.bet.roas)} on ${(o.bet.share * 100).toFixed(0)}% of spend.`);
  return L.join('\n');
}
window.renderActions = function renderActions() {
  const o = ENGINE.opportunities(VIEW);
  const T = o.target_roas;
  const scaleDaily = o.scale.reduce((s, x) => s + x.daily, 0), weak = o.pause.reduce((s, x) => s + x.m7.spend, 0);
  const gems = o.gems.map((x) => {
    const stopped = x.m7.spend <= 0, sale = ENGINE.c.ads[x.id].tags && ENGINE.c.ads[x.id].tags.angle.code === 'offer';
    return actCard('gem', x, {
      title: stopped ? 'Hidden gem, not running now' : 'Hidden gem',
      numbers: [['30-day ROAS', `<b>${roasTxt(x.m30.roas)}</b>`], ['Spend', money(x.m30.spend)], ['Purchases', String(x.m30.purchases)], ['Account ROAS', roasTxt(T)]],
      why: `ROAS is ${(x.m30.roas / T).toFixed(1)}x the account's, but it got only ${money(x.daily)} a day. Meta has not given it a real chance.`,
      action: `${stopped ? 'Relaunch it' : 'Duplicate it'} into its own ad set or a scaling campaign at about <b>${money(x.suggest_daily)}/day</b>. Make 3 variants so it has fresh creative when it scales.`,
      extra: sale ? '<p class="act-note">This was a sale ad. Reuse the idea with a message that is true today.</p>' : '',
    });
  });
  const scale = o.scale.map((x) => actCard('scale', x, {
    title: 'Scale',
    numbers: [['7-day ROAS', `<b>${roasTxt(x.m7.roas)}</b>`], ['Spend a day', money(x.daily)], ['7-day value', money(x.m7.purchase_value || 0)]],
    why: `Above the ${roasTxt(T)} target with enough spend to trust it.`,
    action: `Raise its ad set budget about 20% to <b>${money(x.daily * 1.2)}/day</b>. Check again in 3 days.`,
  }));
  const pause = o.pause.map((x) => actCard('pause', x, {
    title: 'Pause or fix',
    numbers: [['7-day ROAS', `<b>${roasTxt(x.m7.roas)}</b>`], ['Spent this week', money(x.m7.spend)], ['Target', roasTxt(T)]],
    why: `It spent ${money(x.m7.spend)} this week and is more than 30% below target.`,
    action: 'Pause it, or swap in a fresh creative and give it 3 days.',
  }));
  const tired = o.tired.map((x) => actCard('tired', x, {
    title: 'Refresh this creative',
    numbers: [['30-day ROAS', roasTxt(x.m30.roas)], ['7-day ROAS', `<b>${roasTxt(x.m7.roas)}</b>`], ['Spend', money(x.m30.spend)]],
    why: esc(x.fatigue.reason),
    action: 'Make 3 variants from its breakdown and launch them in the same ad set.',
  }));
  const relaunch = o.relaunch.map((x) => actCard('relaunch', { ...x, m30: x.lifetime, format: x.format, type: ENGINE.c.ads[x.id].creative.type }, {
    title: 'Worth relaunching',
    numbers: [['Lifetime ROAS', `<b>${roasTxt(x.lifetime.roas)}</b>`], ['Lifetime spend', money(x.lifetime.spend)], ['Last ran', shortDate(x.last_day)]],
    why: 'Beat the account average by 20% or more, then stopped.',
    action: 'Relaunch in a new ad set, or use it as the base for new variants.',
  }));
  const b = o.bet;
  const bet = b ? `<section class="act-sec"><div class="act-head"><h2>Format to test more</h2><span class="muted small">Last 30 days</span></div>
    <div class="bet"><div class="bet-big">${esc(b.label)}</div><div class="bet-nums"><span><em>ROAS</em><b>${roasTxt(b.roas)}</b></span><span><em>Share of spend</em>${(b.share * 100).toFixed(0)}%</span>${b.runner_up ? `<span><em>Next best</em>${esc(b.runner_up.label)} ${roasTxt(b.runner_up.roas)}</span>` : ''}</div>
    <p><b>Do this:</b> move more budget and new creative into ${esc(b.label.toLowerCase())}${b.best_age || b.best_gender ? `, aimed at ${[b.best_gender && b.best_gender[0], b.best_age && b.best_age[0]].filter(Boolean).map(esc).join(' ')} first (${b.best_age ? `ROAS ${roasTxt(b.best_age[1].roas)} for ${esc(b.best_age[0])}` : ''}${b.best_gender ? `, ${roasTxt(b.best_gender[1].roas)} for ${esc(b.best_gender[0])}` : ''})` : ''}.</p>
    <button class="btn ghost" type="button" data-goto-ins="ins-fa">See format by age and gender</button></div></section>` : '';
  $('actionsView').innerHTML = `<div class="ins">
    <div class="act-hero"><div><h2>This week's plan</h2><p class="lead">Based on ${esc(dateLabel(o.window[0]))} to ${esc(dateLabel(o.window[1]))}. Tick items off as you go.</p></div>
      <div class="row"><button class="btn ghost" type="button" id="copyPlan">Copy plan</button></div></div>
    <div class="act-stats">
      <div><em>Ready to scale</em><b>${o.scale.length}</b><span>${money(scaleDaily)}/day now</span></div>
      <div class="gold"><em>Hidden gems</em><b>${o.gems.length}</b><span>High ROAS, little spend</span></div>
      <div><em>Weak spend this week</em><b>${money(weak)}</b><span>${o.pause.length} ads below target</span></div>
      <div><em>Tired creatives</em><b>${o.tired.length}</b><span>Need fresh versions</span></div>
    </div>
    ${actSection('act-gems', 'Hidden gems: give them their own budget', 'Low spend, high ROAS in the last 30 days', gems)}
    ${actSection('act-scale', 'Scale', 'Strong in the last 7 days', scale)}
    ${bet}
    ${actSection('act-pause', 'Pause or fix', 'Spending below target this week', pause)}
    ${actSection('act-tired', 'Refresh tired creatives', 'CTR or ROAS falling', tired)}
    ${actSection('act-relaunch', 'Worth relaunching', 'Past winners that stopped', relaunch)}
    ${!gems.length && !scale.length && !pause.length && !tired.length ? '<p class="muted">Nothing needs action for these dates.</p>' : ''}
    <p class="small muted">Suggestions from the numbers only. Budgets are rough starting points. This page never changes the ad account.</p></div>`;
  STUDIO.lastPlan = o;
};

// ---------- creative studio ----------
function brandHtml() {
  const b = BRAND || {};
  if (!b.name) return '<p class="muted">No brand kit yet.</p>';
  const list = (xs) => (xs || []).map((x) => `<li>${esc(x)}</li>`).join('');
  return `<div class="brand-kit">
    <p class="bk-one">${esc(b.one_liner)}</p>
    <div class="bk-colors">${(b.colors || []).map((c) => `<span><i style="background:${esc(c.hex)}"></i>${esc(c.name)}<em>${esc(c.hex)}</em></span>`).join('')}</div>
    <div class="two">
      <div><h3>Voice</h3><p>${esc(b.voice && b.voice.summary)}</p><div class="bd-keep">${((b.voice && b.voice.traits) || []).map((t) => `<span>${esc(t)}</span>`).join('')}</div>
        <h3 style="margin-top:12px">Do</h3><ul class="bd-list">${list(b.voice && b.voice.do)}</ul><h3 style="margin-top:12px">Don't</h3><ul class="bd-list warn">${list(b.voice && b.voice.dont)}</ul></div>
      <div><h3>Copy patterns that work</h3><ul class="bd-list">${list(b.copy_patterns)}</ul>
        <h3 style="margin-top:12px">Claims we can use</h3><div class="chips">${(b.approved_claims || []).map((c) => `<span class="chip tag">${esc(c)}</span>`).join('')}</div>
        <h3 style="margin-top:12px">Emojis</h3><p class="bk-emoji">${(b.emoji && b.emoji.favourites || []).map(esc).join(' ')}</p><p class="small muted">${esc(b.emoji && b.emoji.style)}</p>
        <h3 style="margin-top:12px">Photography</h3><ul class="bd-list">${list(b.photography)}</ul></div>
    </div>
    <p class="small muted">Built from ${esc((b.sources || []).join(' and '))} on ${esc(dateLabel(b.built))}. Every AI feature here writes and designs with it.</p></div>`;
}
function playbookPrompt() {
  const th = ENGINE.themes(VIEW), fa = ENGINE.formatAudience(VIEW);
  const top = VIEW.collections.all.ad_ids.slice(0, 15).map((id) => { const a = VIEW.ads[id]; return { name: a.name, format: a.creative.type_label, spend: Math.round(a.view.metrics.spend), roas: a.view.metrics.roas && +a.view.metrics.roas.toFixed(2), headline: a.creative.headline, angle: a.tags && a.tags.angle.label }; });
  const bds = Object.entries(BREAKDOWNS).slice(0, 20).map(([id, b]) => ({ ad: (ENGINE.c.ads[id] || {}).name, verdict: b.verdict, summary: b.summary, why: (b.why || []).map((w) => w.point), keep: b.keep }));
  const pick = (rows) => rows.slice(0, 8).map((r) => ({ label: r.label, spend: Math.round(r.spend), roas: r.roas && +r.roas.toFixed(2), ads: r.ads }));
  const faS = {};
  for (const dim of ['age', 'gender']) for (const [f, cells] of Object.entries(fa[dim])) for (const [k, c] of Object.entries(cells)) if (c.spend > 1000) (faS[dim] || (faS[dim] = [])).push({ format: DATA.meta.format_labels[f] || f, [dim]: k, spend: Math.round(c.spend), roas: c.roas && +c.roas.toFixed(2) });
  return 'You are the head of creative strategy for Gehna, an Indian fine jewellery brand. Write the creative playbook: what wins in their Meta ads and what to do next.\n\n'
    + `Brand kit (JSON):\n${JSON.stringify(BRAND || {}).slice(0, 4000)}\n\n`
    + `Dates: ${VIEW.range.since} to ${VIEW.range.until}. Account ROAS ${VIEW.totals.roas && VIEW.totals.roas.toFixed(2)}, CPA ${Math.round(VIEW.totals.cpa || 0)} INR.\n`
    + `Top ads by spend (JSON):\n${JSON.stringify(top)}\n\nBy creative angle:\n${JSON.stringify(pick(th.angle))}\nBy product:\n${JSON.stringify(pick(th.product))}\nBy opening line:\n${JSON.stringify(pick(th.hook))}\n\n`
    + `Format by audience (JSON):\n${JSON.stringify(faS).slice(0, 6000)}\n\nAd breakdowns so far (JSON):\n${JSON.stringify(bds).slice(0, 12000)}\n\n`
    + 'Rules: every point must come from the data above. Plain short sentences, digits, no em dashes. 3 to 5 items per list.\n'
    + 'Reply with only this JSON:\n{"headline": "one sentence: what wins for Gehna", "winning_patterns": [{"pattern": "", "evidence": ""}], "hooks": [""], "visuals": [""], "offers_and_proof": [""], "audiences": [""], "avoid": [""], "next_tests": [{"test": "", "why": ""}]}';
}
function playbookHtml() {
  const p = PLAYBOOK;
  if (!p) return '<p class="lab-lead">Turn every ad, breakdown and number into one page on what works for Gehna.</p>';
  const list = (xs) => (Array.isArray(xs) ? xs : []).map((x) => `<li>${esc(x)}</li>`).join('');
  return `<div class="bd"><div class="bd-top"><span class="small muted">Updated ${esc(dateLabel(p.date))}</span></div><p class="bd-sum">${esc(p.headline)}</p>
    <h3>What wins</h3><ul class="bd-why">${(p.winning_patterns || []).map((w) => `<li><strong>${esc(w.pattern)}</strong><span>${esc(w.evidence)}</span></li>`).join('')}</ul>
    <div class="two"><div><h3>Hooks</h3><ul class="bd-list">${list(p.hooks)}</ul><h3 style="margin-top:10px">Visuals</h3><ul class="bd-list">${list(p.visuals)}</ul></div>
    <div><h3>Offers and proof</h3><ul class="bd-list">${list(p.offers_and_proof)}</ul><h3 style="margin-top:10px">Audiences</h3><ul class="bd-list">${list(p.audiences)}</ul></div></div>
    <h3>Avoid</h3><ul class="bd-list warn">${list(p.avoid)}</ul>
    <h3>Test next</h3><div class="bd-grid">${(p.next_tests || []).map((t) => `<div><span>Test</span><p><b>${esc(t.test)}</b><br>${esc(t.why)}</p></div>`).join('')}</div></div>`;
}
const STATUS = [['idea', 'Idea'], ['launched', 'Launched'], ['winner', 'Winner'], ['loser', 'Loser'], ['dropped', 'Dropped']];
function testResult(t) {
  if (!t.new_ad_id || !ENGINE.c.ads[t.new_ad_id]) return '';
  const end = ENGINE.nDays - 1, start = t.launched_on ? Math.max(0, ENGINE.idx(t.launched_on)) : Math.max(0, end - 29);
  const m = ENGINE.sums(t.new_ad_id, start, end);
  const o = t.source_ad_id && ENGINE.c.ads[t.source_ad_id] ? ENGINE.sums(t.source_ad_id, Math.max(0, start - 30), Math.max(0, start - 1)) : null;
  return `${money(m.spend)} · ROAS ${roasTxt(m.roas)}${o && o.roas !== null ? ` vs original ${roasTxt(o.roas)}` : ''}`;
}
function testsHtml() {
  const items = TESTS.items;
  if (!items.length) return '<p class="muted small">No tests yet. Use "Track test" on a variant or "Add to tests" on the action plan.</p>';
  const counts = Object.fromEntries(STATUS.map(([k]) => [k, items.filter((t) => t.status === k).length]));
  return `<div class="test-stats">${STATUS.map(([k, l]) => `<span class="ts ts-${k}"><b>${counts[k]}</b>${l}</span>`).join('')}</div>
    <div class="scroll"><table class="tests"><tr><th>Test</th><th>From ad</th><th>Status</th><th>Launched</th><th>New ad ID</th><th>Result so far</th><th></th></tr>
    ${items.map((t) => `<tr data-test="${esc(t.id)}"><td>${t.file && t.source_ad_id && !IS_CLAUDE ? `<img class="test-img" src="/variants/${esc(t.source_ad_id)}/${esc(t.file)}" alt="">` : ''}<b>${esc(t.label)}</b>${t.idea ? `<br><span class="small muted">${esc(t.idea)}</span>` : ''}<br><span class="chip">${esc(t.kind)}</span></td>
      <td class="small">${esc(t.source_ad_name || '')}</td>
      <td><select data-tfield="status" aria-label="Status">${STATUS.map(([k, l]) => `<option value="${k}"${t.status === k ? ' selected' : ''}>${l}</option>`).join('')}</select></td>
      <td><input type="date" data-tfield="launched_on" value="${esc(t.launched_on || '')}" aria-label="Launched on"></td>
      <td><input type="text" data-tfield="new_ad_id" value="${esc(t.new_ad_id || '')}" placeholder="Paste ad ID" inputmode="numeric" aria-label="New ad ID" style="width:150px"></td>
      <td class="small">${testResult(t) || '<span class="muted">Add the new ad ID after launch</span>'}</td>
      <td><button class="icon" type="button" data-tdel="${esc(t.id)}" aria-label="Remove test">×</button></td></tr>`).join('')}</table></div>
    <p class="small muted" id="testMsg">Results fill in when the new ad appears in the data.</p>`;
}
window.renderStudio = async function renderStudio() {
  await labBoot(); await docsBoot();
  const busy = STUDIO.busy.playbook;
  $('studioView').innerHTML = `<div class="ins">
    ${toolHtml()}
    <section class="panel-box"><div class="row" style="justify-content:space-between;align-items:center"><h2>Creative playbook</h2>
      <button class="btn${PLAYBOOK ? ' ghost' : ''}" type="button" id="runPlaybook"${!aiReady() || busy ? ' disabled' : ''}>${busy ? 'Writing the playbook…' : PLAYBOOK ? 'Update playbook' : 'Build playbook'}</button></div>
      <p class="small muted" id="pbMsg">${aiReady() ? `Uses the ads, themes and ${Object.keys(BREAKDOWNS).length} breakdowns so far. Takes about 1 minute.` : IS_CLAUDE ? 'Sign in to Claude to build the playbook.' : 'AI is not set up on this computer yet.'}</p>
      ${playbookHtml()}</section>
    <section class="panel-box"><h2>Test tracker</h2><p class="lead">Every variant, copy and idea you launch, and how it did.</p>${testsHtml()}</section>
    <section class="panel-box"><h2>Brand kit</h2>${brandHtml()}</section></div>`;
};
async function runPlaybook() {
  STUDIO.busy.playbook = true; window.renderStudio();
  let msg = '';
  try {
    const out = await askAI(playbookPrompt());
    if (!out || !out.headline) throw { message: 'The playbook came back empty. Try again.' };
    PLAYBOOK = { ...out, date: new Date().toISOString().slice(0, 10) };
    msg = await saveDoc('playbook.json', PLAYBOOK);
  } catch (e) { msg = aiErr(e); }
  STUDIO.busy.playbook = false;
  await window.renderStudio();
  if ($('pbMsg')) $('pbMsg').textContent = msg;
}

// ---------- competitors: build from a competitor ad ----------
// You pick one of your image ads (the product) and one competitor ad (the reference).
// Both images go to the AI. The competitor image is for layout, format and mood only.
function baseAds() {
  // Top 25 image ads by spend in these dates. The picker shows spend and ROAS for each.
  const col = VIEW.collections.static_image;
  return (col ? col.ad_ids : []).slice(0, 25);
}
function defaultBase(ids) {
  const sale = (id) => (VIEW.ads[id].tags && VIEW.ads[id].tags.angle.code === 'offer');
  const good = ids.filter((id) => VIEW.ads[id].view.metrics.roas !== null && VIEW.ads[id].view.metrics.purchases >= 2 && !sale(id));
  const any = ids.filter((id) => VIEW.ads[id].view.metrics.roas !== null && VIEW.ads[id].view.metrics.purchases >= 1);
  const byRoas = (list) => list.sort((a, b) => VIEW.ads[b].view.metrics.roas - VIEW.ads[a].view.metrics.roas)[0];
  return byRoas(good) || byRoas(any) || ids[0];
}
function basePickerHtml(ids) {
  return `<div class="base-pick" role="radiogroup" aria-label="Your ad to build from">${ids.map((id) => {
    const a = VIEW.ads[id], m = a.view.metrics, on = id === STUDIO.base;
    return `<button type="button" class="base-card${on ? ' on' : ''}" role="radio" aria-checked="${on}" data-base="${esc(id)}">
      <span class="bc-th">${thumbHtml(id, a.name)}<span class="bc-rank">#${a.view.rank_by_spend}</span></span>
      <span class="bc-name" title="${esc(a.name)}">${esc(a.name)}</span>
      <span class="bc-nums"><span>${compact(m.spend)}</span><b class="${m.roas !== null && m.roas >= (VIEW.targets.roas || 0) ? 'up' : ''}">${roasTxt(m.roas)}</b></span></button>`;
  }).join('')}</div>`;
}
function compRef() { return STUDIO.ref ? compItems().find((x) => x.key === STUDIO.ref) || null : null; }
function compFacts(it) {
  const meta = (it.md && it.md.meta) || {};
  return { ad_id: it.id, brand: it.brand, headline: meta.title || it.m.headline, body: (meta.body || '').slice(0, 800), cta: meta.cta || '',
    format: it.fmt.label, days_running: it.m.days_running, versions: it.m.variants, has_image: !!(it.md && it.md.img) };
}
function compIdeasPrompt(comp, baseId, withImages) {
  return 'You are a creative director for Meta ads at Gehna, an Indian fine jewellery brand. A competitor ad has run for '
    + `${comp.days_running} days with ${comp.versions} version(s) live, which usually means it works.\n`
    + `Competitor ad (JSON):\n${JSON.stringify(comp)}\n`
    + (withImages ? 'Image 1 is Gehna\'s own ad. Image 2 is the competitor ad.\n' : '')
    + 'Write 3 concepts for new Gehna image ads. Borrow only the layout, format, framing and mood of the competitor ad. '
    + 'Use Gehna\'s own product from Gehna\'s ad, Gehna\'s proof and Gehna\'s voice. Never copy their text, logo, product, models or faces, and never name them.\n'
    + `Gehna ad (JSON):\n${JSON.stringify(adFacts(baseId)).slice(0, 5000)}\n\nWhy it worked (JSON):\n${JSON.stringify(BREAKDOWNS[baseId] || {}).slice(0, 3000)}\n\nBrand kit (JSON):\n${JSON.stringify(BRAND || {}).slice(0, 4000)}\n\n`
    + 'Rules: never invent prices, discounts or claims. Plain short sentences, digits, no em dashes.\n'
    + 'Reply with only this JSON:\n{"concepts": [{"name": "", "principle": "what is borrowed from the competitor ad", "idea": "", "scene": "", "layout": "", "headline": "ad headline in Gehna voice", "primary_text": "3 to 5 short lines in Gehna voice"}]}';
}
function compResultHtml(key) {
  const r = STUDIO.comp[key];
  if (!r) return '';
  if (r.busy) return '<p class="small muted"><span class="lab-spin" style="display:inline-block;vertical-align:middle"></span> Building 3 versions for Gehna. About 1 to 2 minutes.</p>';
  if (r.error) return `<p class="small" style="color:var(--bad)">${esc(r.error)}</p>`;
  if (r.images) return `<div class="vgrid">${r.images.map((v) => v.error ? `<div class="vcard err"><strong>${esc(v.label)}</strong><span class="small">${esc(v.error)}</span></div>` : `<figure class="vcard"><img src="/variants/${esc(r.base)}/${esc(v.file)}" alt="${esc(v.label)}" loading="lazy"><figcaption><span class="vtag">${v.comp_brand ? `From ${esc(v.comp_brand)}` : 'From your reference'}</span><strong>${esc(v.label)}</strong><span class="small">${esc(v.principle || '')}</span><span class="vbtns"><a class="btn ghost small-btn" href="/variants/${esc(r.base)}/${esc(v.file)}" download>Download</a><button class="btn ghost small-btn" type="button" data-track="${esc(r.base)}|${esc(v.file)}">Track test</button></span></figcaption></figure>`).join('')}</div>`;
  return `<div class="bd-grid">${(r.concepts || []).map((c) => `<div><span>${esc(c.name)}</span><p><b>${esc(c.idea)}</b></p><p class="small muted">${esc(c.principle || '')}</p>${c.layout ? `<p class="small"><b>Layout:</b> ${esc(c.layout)}</p>` : ''}${c.headline ? `<p><b>${esc(c.headline)}</b></p>` : ''}${c.primary_text ? `<p class="pre small">${esc(c.primary_text)}</p>` : ''}</div>`).join('')}</div>`;
}
function compToolHtml(bases) {
  const cur = STUDIO.base && VIEW.ads[STUDIO.base], ref = compRef();
  const canImg = !IS_CLAUDE && LABST.status && LABST.status.variants;
  const rkey = cur && (REF.b64 || ref) ? `${REF.b64 ? 'paste:' + STUDIO.refRole + ':' + REF.b64.length + ':' + REF.b64.slice(-24) : ref.key}|${STUDIO.base}` : '';
  const busy = rkey && STUDIO.comp[rkey] && STUDIO.comp[rkey].busy;
  const pair = `<div class="cpair">
      <figure><figcaption class="small muted">${REF.b64 && STUDIO.refRole === 'product' ? 'Your winning ad (the layout)' : 'Your ad (the product)'}</figcaption>${cur ? `<div class="cpair-img">${thumbHtml(STUDIO.base, cur.name)}</div><span class="small"><b>${esc(cur.name)}</b><br>${money(cur.view.metrics.spend)} spend · ROAS ${roasTxt(cur.view.metrics.roas)}</span>` : '<div class="cpair-img cimg-none">Pick an ad below</div>'}</figure>
      <span class="cpair-plus" aria-hidden="true">+</span>
      <figure><figcaption class="small muted">${REF.b64 && STUDIO.refRole === 'product' ? 'Product to show' : 'Reference (layout and mood)'}</figcaption>${REF.b64 ? `<div class="cpair-img"><img src="data:image/jpeg;base64,${REF.b64}" alt="Pasted image"></div><span class="small"><b>Your pasted image</b></span>`
        : ref ? `<div class="cpair-img">${compImg(ref, 'cimg')}</div><span class="small"><b>${esc(ref.brand)}</b> · ${esc(ref.fmt.label)} · live ${ref.m.days_running} days<br>${esc(compTitle(ref))}<br><button class="linkbtn" type="button" data-crefclear>Clear</button></span>` : '<div class="cpair-img cimg-none">Paste an image below, or pick one on the Competitors tab</div>'}</figure>
    </div>
    <div class="lab-ref">${refSlotHtml(ref ? 'Pasted image. It replaces the competitor ad above.' : 'Pasted image')}<p class="small muted" data-refmsg>${esc(STUDIO.hint || '')}</p></div>
    <div class="seg" role="radiogroup" aria-label="What the pasted image is"><span class="small muted" style="align-self:center;margin-right:6px">The pasted image is</span><button type="button" data-refrole="layout" aria-pressed="${STUDIO.refRole !== 'product'}">A layout to borrow</button><button type="button" data-refrole="product" aria-pressed="${STUDIO.refRole === 'product'}">The product to show</button></div>`;
  return `<section class="panel-box comp-tool" id="comp-tool"><h2>Make variants from a reference</h2>
    <p class="lead">Pick your ad for the product. Add a reference: copy any ad image and paste it here, or pick one on the Competitors tab. The reference gives layout, framing and mood only. Its text, logo, product and faces are never copied.</p>
    ${pair}
    <div class="lab-actions"><button class="btn" type="button" id="compBuild"${!(ref || REF.b64) || !cur || !aiReady() || busy ? ' disabled' : ''}>${busy ? 'Building…' : canImg ? 'Make 3 images' : 'Write 3 ideas with copy'}</button>
      ${!aiReady() ? `<span class="small muted">${IS_CLAUDE ? 'Sign in to Claude to use this.' : 'AI is off for this copy.'}</span>` : ''}</div>
    <div id="compOut">${rkey ? compResultHtml(rkey) : ''}</div>
    <h3>Your top ${bases.length} image ads by spend, ${esc(shortDate(VIEW.range.since))} to ${esc(shortDate(VIEW.range.until))}</h3>
    ${bases.length ? basePickerHtml(bases) : '<p class="small muted">No image ads spent in these dates.</p>'}</section>`;
}
function toolHtml() {
  const bases = baseAds();
  if (!STUDIO.base || !bases.includes(STUDIO.base)) STUDIO.base = defaultBase(bases);
  return compToolHtml(bases);
}
function toolRerender() {
  if (state.tab === 'studio') window.renderStudio();
  else if (state.tab === 'competitors') window.renderCompetitors();
}
const baseRenderCompetitors = window.renderCompetitors;
window.renderCompetitors = function () {
  baseRenderCompetitors();
  const view = $('competitorsView');
  if (!COMPETITORS || !COMPETITORS.brands) return;
  view.querySelectorAll('[data-cref]').forEach((b) => { if (b.dataset.cref === STUDIO.ref) { b.textContent = 'Picked as reference'; b.classList.add('on'); } });
};
async function compAsk(prompt, baseId, it) {
  // Claude in the page: send both images when the viewer's Claude takes images. Local app: the server adds both.
  await labBoot();
  if (!IS_CLAUDE) return askAI(prompt, baseId, { comp: it.id });
  if (!LABST.sample) throw { code: 'unavailable', message: 'Sign in to Claude to use this.' };
  const caps = await LABST.sample.limits().catch(() => null);
  const imgs = caps && caps.images ? [thumbBlob(baseId), compBlob(it.id)].filter(Boolean) : [];
  return LABST.sample.json(prompt, { modelTier: 'default', cache: false, ...(imgs.length ? { images: imgs } : {}) });
}
function refIdeasPrompt(baseId) {
  const product = STUDIO.refRole === 'product';
  return 'You are a creative director for Meta ads at Gehna, an Indian fine jewellery brand. '
    + (product ? 'Image 1 is Gehna\'s winning ad. Image 2 is a Gehna product photo.\n'
      + 'Write 3 concepts for new Gehna image ads that feature the exact piece from image 2, using the layout, framing, text style and mood that made image 1 work. Use Gehna\'s proof and voice.\n'
      : 'Image 1 is Gehna\'s ad. Image 2 is a reference ad the team picked.\n'
      + 'Write 3 concepts for new Gehna image ads that use the reference\'s layout, framing, format and mood, with Gehna\'s product from image 1, Gehna\'s proof and Gehna\'s voice. '
      + 'Never copy the reference\'s text, logo, product, models or faces.\n')
    + `Gehna ad (JSON):\n${JSON.stringify(adFacts(baseId)).slice(0, 5000)}\n\nWhy it worked (JSON):\n${JSON.stringify(BREAKDOWNS[baseId] || {}).slice(0, 3000)}\n\nBrand kit (JSON):\n${JSON.stringify(BRAND || {}).slice(0, 4000)}\n\n`
    + 'Rules: never invent prices, discounts or claims. Plain short sentences, digits, no em dashes.\n'
    + 'Reply with only this JSON:\n{"concepts": [{"name": "", "principle": "what is taken from the reference", "idea": "", "scene": "", "layout": "", "headline": "ad headline in Gehna voice", "primary_text": "3 to 5 short lines in Gehna voice"}]}';
}
async function buildFromPaste(base) {
  const key = `paste:${STUDIO.refRole}:${REF.b64.length}:${REF.b64.slice(-24)}|${base}`;
  STUDIO.comp[key] = { busy: true };
  toolRerender();
  try {
    if (!IS_CLAUDE && LABST.status && LABST.status.variants) {
      const r = await fetch('/api/variants', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ ad_id: base, n: 3, size: 'square', quality: 'medium', ref_image: REF.b64, ref_role: STUDIO.refRole }) });
      const j = await r.json().catch(() => ({}));
      if (!r.ok) throw { message: j.error || 'Could not make images.' };
      STUDIO.comp[key] = { images: j.made, base };
    } else {
      const res = await askAI(refIdeasPrompt(base), base, { ref: true });
      STUDIO.comp[key] = { concepts: (res && Array.isArray(res.concepts) ? res.concepts : []).slice(0, 3) };
    }
  } catch (e) { STUDIO.comp[key] = { error: aiErr(e) }; }
  toolRerender();
}
async function buildComp() {
  const it = compRef(), base = STUDIO.base;
  if (base && REF.b64) return buildFromPaste(base);
  if (!it || !base) return;
  const key = `${it.key}|${base}`;
  STUDIO.comp[key] = { busy: true };
  const out = () => { const o = $('compOut'); if (o) o.innerHTML = compResultHtml(key); const bt = $('compBuild'); if (bt) { bt.disabled = !!STUDIO.comp[key].busy; } };
  out();
  const comp = compFacts(it);
  try {
    if (!IS_CLAUDE && LABST.status && LABST.status.variants) {
      const r = await fetch('/api/competitor-variants', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ base_ad_id: base, comp, facts: adFacts(base), n: 3 }) });
      const j = await r.json().catch(() => ({}));
      if (!r.ok) throw { message: j.error || 'Could not build this one.' };
      STUDIO.comp[key] = { images: j.made, base };
    } else {
      const res = await compAsk(compIdeasPrompt(comp, base, true), base, it);
      STUDIO.comp[key] = { concepts: (res && Array.isArray(res.concepts) ? res.concepts : []).slice(0, 3) };
    }
  } catch (e) { STUDIO.comp[key] = { error: aiErr(e) }; }
  toolRerender();
}

// ---------- events ----------
window.initStudio = function initStudio() {
  labBoot().then(docsBoot);
  $('actionsView').addEventListener('click', async (e) => {
    const open = e.target.closest('[data-act-open]');
    if (open) { openSide(open.dataset.actOpen); setTimeout(() => { const l = $('lab'); if (l) l.scrollIntoView({ behavior: 'smooth', block: 'start' }); }, 250); return; }
    const t = e.target.closest('[data-act-test]');
    if (t) {
      const [kind, id] = t.dataset.actTest.split('|');
      const label = { gem: 'Own budget for hidden gem', scale: 'Scale +20%', pause: 'Pause or swap creative', tired: 'Refresh with variants', relaunch: 'Relaunch' }[kind] || kind;
      await docsBoot();
      t.disabled = true;
      const msg = await addTest({ kind: 'action', label, idea: '', source_ad_id: id, source_ad_name: (ENGINE.c.ads[id] || {}).name || '' });
      t.textContent = msg.startsWith('Saved') ? 'Added' : 'Added for you';
      return;
    }
    if (e.target.closest('#copyPlan')) {
      const b = $('copyPlan');
      try { await navigator.clipboard.writeText(planText(STUDIO.lastPlan)); b.textContent = 'Copied'; } catch (err) { b.textContent = 'Copy blocked here'; }
      setTimeout(() => { b.textContent = 'Copy plan'; }, 1800);
      return;
    }
    const g = e.target.closest('[data-goto-ins]');
    if (g) { setTab('insights'); setTimeout(() => { const s = $(g.dataset.gotoIns); if (s) s.scrollIntoView({ behavior: 'smooth' }); }, 150); }
  });
  $('actionsView').addEventListener('change', (e) => {
    const d = e.target.closest('[data-done]');
    if (!d) return;
    const [kind, id] = d.dataset.done.split('|');
    setDone(kind, id, d.checked);
    d.closest('.act').classList.toggle('done', d.checked);
  });
  $('studioView').addEventListener('click', async (e) => {
    if (e.target.closest('#runPlaybook')) { runPlaybook(); return; }
    if (e.target.closest('#compBuild')) { buildComp(); return; }
    if (e.target.closest('[data-crefclear]')) { STUDIO.ref = ''; window.renderStudio(); return; }
    const role = e.target.closest('[data-refrole]');
    if (role) { STUDIO.refRole = role.dataset.refrole; window.renderStudio(); return; }
    const pick = e.target.closest('[data-base]');
    if (pick) { STUDIO.base = pick.dataset.base; window.renderStudio(); return; }
    const del = e.target.closest('[data-tdel]');
    if (del) { TESTS = { items: TESTS.items.filter((t) => t.id !== del.dataset.tdel) }; const m = await saveDoc('tests.json', TESTS); await window.renderStudio(); if ($('testMsg')) $('testMsg').textContent = m; }
  });
  $('studioView').addEventListener('change', async (e) => {
    const f = e.target.closest('[data-tfield]');
    if (!f) return;
    const id = f.closest('[data-test]').dataset.test, field = f.dataset.tfield;
    let v = f.value.trim();
    if (field === 'new_ad_id') v = v.replace(/\D/g, '').slice(0, 25);
    TESTS = { items: TESTS.items.map((t) => (t.id === id ? { ...t, [field]: v, ...(field === 'status' && v === 'launched' && !t.launched_on ? { launched_on: new Date().toISOString().slice(0, 10) } : {}) } : t)) };
    const m = await saveDoc('tests.json', TESTS);
    await window.renderStudio();
    if ($('testMsg')) $('testMsg').textContent = m;
  });
  $('competitorsView').addEventListener('click', (e) => {
    const r = e.target.closest('[data-cref]');
    if (r) { STUDIO.ref = r.dataset.cref; setTab('studio'); setTimeout(() => { const t = $('comp-tool'); if (t) t.scrollIntoView({ behavior: 'smooth', block: 'start' }); }, 400); return; }
    const fb = e.target.closest('[data-cbrand]');
    if (fb) { COMPV.brand = fb.dataset.cbrand; window.renderCompetitors(); return; }
    const ff = e.target.closest('[data-cfmt]');
    if (ff) { COMPV.fmt = ff.dataset.cfmt; window.renderCompetitors(); }
  });
};
