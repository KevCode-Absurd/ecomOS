'use strict';
// Read-only gallery UI. All data comes from the local server; no credentials here.
let META = null;       // /api/meta: account, window, campaigns, settings
let VIEW = null;       // /api/view for the current dates and exclusions
let SETTINGS = null;
const state = { since: null, until: null, kw: [], camp: [], preset: '' };

async function load() {
  try {
    META = await getJSON('/api/meta');
  } catch (e) {
    $('grid').textContent = e.message;
    return;
  }
  SETTINGS = META.settings;
  const m = META.meta;
  setCurrency(m.currency);
  $('account').textContent = `${m.account_name || ''} · act_${m.account_id} · ${m.currency} · ${m.timezone || 'timezone unavailable'}`;
  for (const id of ['since', 'until']) { $(id).min = m.window.since; $(id).max = m.window.until; }
  $('format').innerHTML = m.formats.map((f) => `<option value="${esc(f)}">${esc(m.format_labels[f])}</option>`).join('');
  $('footer').textContent = `Data window ${dateLabel(m.window.since)} to ${dateLabel(m.window.until)} · captured ${new Date(m.captured_at).toLocaleString('en-IN')} · cache built ${new Date(m.built_at).toLocaleString('en-IN')} · Source: ${m.source}. Browsing reads the local cache only.`;

  readUrl();
  fillPresets();
  fillCampaignList();
  fillTargets();

  $('preset').addEventListener('change', () => { applyPreset($('preset').value); refresh(); });
  for (const id of ['since', 'until']) $(id).addEventListener('change', () => { $('preset').value = 'custom'; state.since = $('since').value; state.until = $('until').value; refresh(); });
  $('compare').addEventListener('change', renderAll);
  $('kw').addEventListener('keydown', (e) => {
    if (e.key === ',' || e.key === 'Enter') { e.preventDefault(); addKeywords($('kw').value); }
    else if (e.key === 'Backspace' && !$('kw').value && state.kw.length) removeKeyword(state.kw[state.kw.length - 1]);
  });
  $('kw').addEventListener('input', () => { if ($('kw').value.includes(',')) addKeywords($('kw').value); });
  $('kw').addEventListener('blur', () => { if ($('kw').value.trim()) addKeywords($('kw').value); });
  $('kwBox').addEventListener('click', (e) => {
    const b = e.target.closest('button[data-kw], button[data-camp]');
    if (b && b.dataset.kw !== undefined) removeKeyword(b.dataset.kw);
    else if (b) removeCampaign(b.dataset.camp);
    else $('kw').focus();
  });
  $('campSearch').addEventListener('input', fillCampaignList);
  $('campList').addEventListener('change', (e) => {
    if (!e.target.matches('input[type=checkbox]')) return;
    const id = e.target.value;
    state.camp = e.target.checked ? [...new Set([...state.camp, id])] : state.camp.filter((x) => x !== id);
    state.preset = ''; $('presetSel').value = '';
    renderPills();
    refresh();
  });
  $('presetSel').addEventListener('change', () => {
    const p = SETTINGS.presets.find((x) => x.name === $('presetSel').value);
    state.preset = p ? p.name : '';
    state.kw = p ? [...p.keywords] : [];
    state.camp = p ? [...p.campaign_ids] : [];
    fillCampaignList();
    renderPills();
    refresh();
  });
  $('savePreset').addEventListener('click', savePreset);
  $('delPreset').addEventListener('click', deletePreset);
  $('saveTargets').addEventListener('click', saveTargets);
  $('reportBtn').addEventListener('click', () => window.open('/report?' + filterQuery(state) + ($('compare').checked ? '' : '&nocompare=1'), '_blank', 'noopener'));
  for (const id of ['sort', 'verdict', 'minSpend', 'minRoas', 'campaign', 'status']) $(id).addEventListener('input', renderGrid);
  $('format').addEventListener('change', () => { fillFilters(); renderGrid(); writeUrl(); });
  refresh();
}

function readUrl() {
  const p = new URLSearchParams(location.search);
  const w = META.meta.window;
  const ok = (d) => /^\d{4}-\d{2}-\d{2}$/.test(d || '') && d >= w.since && d <= w.until;
  if (ok(p.get('since')) && ok(p.get('until')) && p.get('since') <= p.get('until')) {
    state.since = p.get('since'); state.until = p.get('until');
    $('preset').value = p.get('preset') || 'custom';
  } else {
    applyPreset($('preset').value);
  }
  state.kw = parseKw(p.get('kw'));
  state.camp = (p.get('camp') || '').split(',').filter((x) => /^\d{5,25}$/.test(x));
  state.preset = p.get('xp') || '';
  if (p.get('fmt') && META.meta.formats.includes(p.get('fmt'))) $('format').value = p.get('fmt');
  renderPills();
  $('since').value = state.since; $('until').value = state.until;
}

function writeUrl() {
  const q = new URLSearchParams(filterQuery(state));
  q.set('preset', $('preset').value);
  if (state.preset) q.set('xp', state.preset);
  if ($('format').value !== 'all') q.set('fmt', $('format').value);
  history.replaceState(null, '', '?' + q.toString());
}

function applyPreset(v) {
  const end = META.meta.window.until;
  const start = META.meta.window.since;
  if (v === 'custom') return;
  if (v === 'this_month') { state.since = end.slice(0, 8) + '01'; state.until = end; }
  else if (v === 'last_month') {
    const lastEnd = addDays(end.slice(0, 8) + '01', -1);
    state.since = lastEnd.slice(0, 8) + '01'; state.until = lastEnd;
  } else { state.until = end; state.since = addDays(end, -(parseInt(v, 10) - 1)); }
  if (state.since < start) state.since = start;
  $('since').value = state.since; $('until').value = state.until;
}

async function refresh() {
  writeUrl();
  $('error').textContent = '';
  try {
    VIEW = await getJSON('/api/view?' + filterQuery(state));
  } catch (e) {
    $('error').textContent = e.message;
    return;
  }
  renderAll();
}

function renderAll() {
  const r = VIEW.range;
  const cmp = $('compare').checked;
  const pv = VIEW.previous;
  $('rangeLabel').innerHTML = `${esc(dateLabel(r.since))} to ${esc(dateLabel(r.until))} · ${r.days} days` +
    (cmp ? (pv.days_covered ? ` <span class="muted small">vs ${esc(dateLabel(pv.since))} to ${esc(dateLabel(pv.until))}${pv.complete ? '' : ` (only ${pv.days_covered} of ${pv.days} days are inside the stored year, so no change figures)`}</span>` :
      ' <span class="muted small">No earlier data stored to compare with.</span>') : '');
  renderExclusions();
  renderKpis();
  renderFormats();
  fillFilters();
  renderGrid();
}

function exclusionsChanged() {
  state.preset = '';
  $('presetSel').value = '';
  renderPills();
  fillCampaignList();
  refresh();
}
function addKeywords(text) {
  $('kw').value = '';
  const add = parseKw(text).filter((k) => !state.kw.includes(k));
  if (!add.length) return;
  state.kw = [...state.kw, ...add].slice(0, 20);
  exclusionsChanged();
}
function removeKeyword(k) {
  state.kw = state.kw.filter((x) => x !== k);
  exclusionsChanged();
  $('kw').focus();
}
function removeCampaign(id) {
  state.camp = state.camp.filter((x) => x !== id);
  exclusionsChanged();
}

// Pills show what is excluded right now. The count comes from the current view.
function renderPills() {
  const x = VIEW ? VIEW.exclusions : null;
  const hits = {};
  for (const c of (x ? x.campaigns : [])) {
    const h = hits[c.matched] || (hits[c.matched] = { n: 0, spend: 0 });
    h.n += 1;
    h.spend += c.spend;
  }
  const names = new Map(META.campaigns.map((c) => [c.id, c.name]));
  const kwPills = state.kw.map((k) => {
    const h = hits[k];
    const known = x && x.keywords.includes(k);  // false while the new view is still loading
    const info = !known ? '' : h ? `${h.n} campaign${h.n > 1 ? 's' : ''} · ${money(h.spend)}` : 'no campaign spent in these dates';
    return `<span class="pill${known && !h ? ' idle' : ''}" title="Campaigns whose name contains &quot;${esc(k)}&quot;${info ? ': ' + esc(info) : ''}">` +
      `<span class="pill-text">${esc(k)}</span>${info ? `<span class="pill-info">${esc(info)}</span>` : ''}` +
      `<button type="button" data-kw="${esc(k)}" aria-label="Stop excluding ${esc(k)}">×</button></span>`;
  });
  const campPills = state.camp.map((id) => `<span class="pill camp" title="${esc(names.get(id) || id)}"><span class="pill-text">${esc(names.get(id) || id)}</span>` +
    `<button type="button" data-camp="${esc(id)}" aria-label="Stop excluding this campaign">×</button></span>`);
  $('kwPills').innerHTML = kwPills.join('') + campPills.join('');
  $('kwBox').classList.toggle('active', state.kw.length + state.camp.length > 0);
  $('kw').placeholder = state.kw.length || state.camp.length ? 'Add another word' : 'Type a word in the campaign name, then press comma or Enter';
}

function renderExclusions() {
  renderPills();
  const x = VIEW.exclusions;
  const n = state.camp.length;
  $('campCount').textContent = n ? `(${n} picked)` : '';
  $('delPreset').hidden = !state.preset;
  if (!x.keywords.length && !x.campaign_ids.length) { $('exclNote').innerHTML = 'No campaigns excluded. Totals, the top 30 and charts cover every campaign.'; return; }
  const list = x.campaigns.map((c) => `${esc(c.name)} (${money(c.spend)})`).join('\n');
  $('exclNote').innerHTML = x.campaigns.length
    ? `<strong>Left out of every number:</strong> ${x.campaigns.length} campaign${x.campaigns.length > 1 ? 's' : ''}, ${x.ads} ads, ${money(x.spend)} spend in these dates. <span class="linkish" title="${list}">Which campaigns?</span>`
    : 'The exclusion matches no campaign that spent in these dates.';
}

function kpi(label, cur, prev, kind, good, note) {
  const show = $('compare').checked && VIEW.previous.complete && prev !== undefined;
  return `<div class="kpi"><div class="k-label">${esc(label)}</div><div class="k-val">${fmt(cur, kind)}</div>` +
    (show ? `<div class="k-prev">${delta(cur, prev, good)} <span class="muted">prev ${fmt(prev, kind)}</span></div>` : '') +
    (note ? `<div class="k-note small muted">${note}</div>` : '') + '</div>';
}

function renderKpis() {
  const t = VIEW.totals;
  const p = VIEW.previous_totals || {};
  const tg = VIEW.targets;
  $('kpis').innerHTML = [
    kpi('Spend', t.spend, p.spend, 'money', 0),
    kpi('Purchase value', t.purchase_value, p.purchase_value, 'money', 1),
    kpi('ROAS', t.roas, p.roas, 'x', 1, `Target ${tg.roas ? tg.roas.toFixed(2) + 'x' : 'not set'} (${esc(tg.roas_source)})`),
    kpi('Purchases', t.purchases, p.purchases, 'int', 1),
    kpi('CPA', t.cpa, p.cpa, 'money', -1, `Target ${tg.cpa ? money(tg.cpa) : 'not set'} (${esc(tg.cpa_source)})`),
    kpi('Link CTR', t.link_ctr, p.link_ctr, 'pct', 1),
  ].join('') + `<p class="small muted kpi-foot">${t.ads} ads spent in these dates. ROAS = total purchase value ÷ total spend. ${t.ads_without_reported_value} ads had no reported purchase value; their spend still counts.</p>`;
}

function renderFormats() {
  const t = VIEW.totals;
  const rows = Object.values(VIEW.by_type).sort((a, b) => b.spend - a.spend);
  const fr = (label, x, strong) => `<tr${strong ? ' class="total"' : ''}><td>${esc(label)}</td><td class="n">${x.ads}</td><td class="n">${fmt(x.spend, 'money')}</td><td class="n">${t.spend ? (x.spend / t.spend * 100).toFixed(1) + '%' : NA}</td><td class="n">${fmt(x.purchase_value, 'money')}</td><td class="n">${fmt(x.roas, 'x')}</td><td class="n">${fmt(x.cpa, 'money')}</td></tr>`;
  $('formats').querySelector('summary').textContent = `Spend, purchase value and ROAS by format · all ${t.ads} ads that spent in these dates`;
  $('formats').querySelector('.body').innerHTML = '<table class="fmt-table"><tr><th>Format</th><th class="n">Ads</th><th class="n">Spend</th><th class="n">Share</th><th class="n">Purchase value</th><th class="n">ROAS</th><th class="n">CPA</th></tr>' +
    rows.map((x) => fr(x.label, x)).join('') + fr('All formats', t, true) + '</table>';
}

function collection() { return VIEW.collections[$('format').value]; }
function items() { return collection().ad_ids.map((id) => VIEW.ads[id]); }

function fillFilters() {
  const all = items();
  const keep = (sel, values) => {
    const prev = sel.value;
    sel.innerHTML = '<option value="">All</option>' + values.map(([v, l]) => `<option value="${esc(v)}">${esc(l)}</option>`).join('');
    sel.value = values.some(([v]) => v === prev) ? prev : '';
  };
  const camps = new Map(all.map((ad) => [ad.campaign_id, ad.campaign_name]));
  keep($('campaign'), [...camps].sort((a, b) => String(a[1]).localeCompare(String(b[1]))));
  keep($('status'), [...new Set(all.map((ad) => ad.effective_status))].sort().map((s) => [s, statusLabel(s)]));
}

function renderGrid() {
  const col = collection();
  const fmtKey = $('format').value;
  const sort = $('sort').value;
  const minSpend = parseFloat($('minSpend').value) || 0;
  const minRoas = parseFloat($('minRoas').value) || 0;
  const camp = $('campaign').value;
  const status = $('status').value;
  const verdict = $('verdict').value;
  let hiddenNoRoas = 0;
  const list = items().filter((ad) => {
    const m = ad.view.metrics;
    if ((m.spend || 0) < minSpend) return false;
    if (minRoas > 0 && m.roas === null) { hiddenNoRoas += 1; return false; }
    if (minRoas > 0 && m.roas < minRoas) return false;
    if (camp && ad.campaign_id !== camp) return false;
    if (status && ad.effective_status !== status) return false;
    if (verdict && ad.view.verdict.code !== verdict) return false;
    return true;
  });
  const chg = (ad) => { const p = ad.view.prev_metrics; return p && p.spend ? (ad.view.metrics.spend - p.spend) / p.spend : Infinity; };
  if (sort === 'roas') list.sort((a, b) => (b.view.metrics.roas ?? -1) - (a.view.metrics.roas ?? -1) || b.view.metrics.spend - a.view.metrics.spend);
  else if (sort === 'change') list.sort((a, b) => chg(b) - chg(a));
  else list.sort((a, b) => b.view.metrics.spend - a.view.metrics.spend);

  const scope = fmtKey === 'all' ? 'across all formats' : `${col.label.toLowerCase()} ads only`;
  $('collectionLabel').textContent = `Top 30 by spend, ${scope}` +
    (col.size < 30 ? ` · only ${col.size} ${col.label.toLowerCase()} ads spent in these dates` : '') + ` · showing ${list.length} of ${col.size}`;
  const notes = [];
  if (sort === 'roas') notes.push('Sorted by purchase ROAS within this top-30-by-spend set. It is not the account\'s top 30 by ROAS. Ads with unavailable ROAS are listed last.');
  if (sort === 'change') notes.push('Sorted by spend change vs the previous period. New ads (no spend before) are listed first.');
  if (hiddenNoRoas) notes.push(`${hiddenNoRoas} ads hidden by the ROAS filter because Meta reported no purchase value for them.`);
  $('sortNote').textContent = notes.join(' ');
  const t = col.totals;
  const vc = {};
  for (const ad of items()) vc[ad.view.verdict.code] = (vc[ad.view.verdict.code] || 0) + 1;
  $('totals').innerHTML = `This set (all ${col.size} ads, filters ignored): spend ${fmt(t.spend, 'money')} · purchase value ${fmt(t.purchase_value, 'money')} · ROAS ${fmt(t.roas, 'x')}` +
    (t.ads_without_reported_value ? ` · ${t.ads_without_reported_value} ads had no reported purchase value` : '') +
    ` · Verdicts: ${vc.scale || 0} scale, ${vc.watch || 0} watch, ${vc.cut || 0} cut, ${vc.not_enough_data || 0} not enough data`;

  $('demo').innerHTML = demoBlock(list, bucketNote(VIEW.demographics_buckets, VIEW.demographics_exact, VIEW.range) +
    ` Follows the format and filters: ${list.length} ads shown below.`);
  $('grid').innerHTML = list.map(card).join('');
  $('empty').hidden = list.length > 0;
  document.querySelectorAll('.more').forEach((b) => b.addEventListener('click', () => openPanel(b.dataset.id)));
}

function card(ad) {
  const v = ad.view;
  const m = v.metrics;
  const p = $('compare').checked ? v.prev_metrics : null;
  const c = ad.creative;
  const chips = [verdictChip(v.verdict), fatigueChip(v.fatigue), `<span class="chip fmt">${esc(c.type_label)}</span>`,
    `<span class="chip ${ad.effective_status === 'ACTIVE' ? 'active' : ''}">${esc(statusLabel(ad.effective_status))}</span>`];
  const n = (v.same_media_ads || []).length;
  if (n) chips.push(`<span class="chip" title="Metrics stay per ad">Same ${c.type === 'video' ? 'video' : 'image'} in ${n} other ad${n > 1 ? 's' : ''}</span>`);
  if (ad.flags.some((f) => f.startsWith('Ad set') || f.startsWith('Campaign'))) chips.push('<span class="chip flag">Check note</span>');
  if (!p && VIEW.previous.complete && $('compare').checked) chips.push('<span class="chip" title="No spend in the previous period">New</span>');
  const low = c.display_quality !== 'full' ? ' low' : '';
  const badge = c.type === 'video' ? `<span class="play">▶ ${secs(c.video && c.video.length)}</span>` :
    c.type === 'carousel' ? `<span class="play">${c.cards.length} cards</span>` : '';
  const d = (cur, prev, good) => (p ? delta(cur, prev, good) : '');
  return `<article class="card">
    <div class="thumb${low}"><span class="rank">#${v.rank_by_spend} by spend</span>${badge}
      <img loading="lazy" src="/img/${esc(ad.id)}" alt="${esc(c.headline || ad.name)}" onerror="this.replaceWith(Object.assign(document.createElement('div'),{className:'noimg',textContent:'Image unavailable. Run the image prefetch.'}))">
    </div>
    <div class="body">
      <div class="name" title="${esc(ad.name)}">${esc(ad.name)}</div>
      <div class="chips">${chips.join('')}</div>
      <dl class="stats">
        <div><dt>Spend</dt><dd>${fmt(m.spend, 'money')} ${d(m.spend, p && p.spend, 0)}</dd></div>
        <div><dt>Purchases</dt><dd>${fmt(m.purchases, 'int')}</dd></div>
        <div><dt>CPA</dt><dd>${fmt(m.cpa, 'money')} ${d(m.cpa, p && p.cpa, -1)}</dd></div>
        <div><dt>Purchase ROAS</dt><dd>${fmt(m.roas, 'x')} ${d(m.roas, p && p.roas, 1)}</dd></div>
      </dl>
      <button class="more" data-id="${esc(ad.id)}">View more</button>
    </div>
  </article>`;
}

function mediaSection(ad) {
  const c = ad.creative;
  const img = `<img src="/img/${esc(ad.id)}" alt="" onerror="this.replaceWith(Object.assign(document.createElement('div'),{className:'warnbox',textContent:'Image unavailable locally.'}))">`;
  if (c.type === 'carousel') {
    return `<section><h3>Carousel cards (${c.cards.length})</h3><div class="cards">` + c.cards.map((k, i) => `
      <div class="cardrow"><img src="/card/${esc(ad.id)}/${i}" alt="" onerror="this.style.visibility='hidden'">
        <div><strong>${esc(k.headline || '')}</strong>${k.description ? `<br><span class="small">${esc(k.description)}</span>` : ''}
        <br><span class="small">${k.link ? link(k.link) : NA}</span></div></div>`).join('') + '</div></section>';
  }
  const extra = [];
  if (c.type === 'video' && c.video) extra.push(`<p>${c.video.url ? link(c.video.url, 'Watch video on Facebook') : ''} ${c.video.length ? `· ${secs(c.video.length)}` : ''}</p>`);
  if (c.display_quality !== 'full') extra.push(`<p class="small muted">Small preview (${c.display_quality === 'thumbnail_160' ? '160px' : '64px'}) from Meta. Open the post for the full creative.</p>`);
  return img + extra.join('');
}

function rolling(days, fn, win = 7) {
  return days.map((d, i) => {
    if (!d.in_range) return null;
    const slice = days.slice(Math.max(0, i - win + 1), i + 1);
    return { x: shortDate(d.date), y: fn(slice) };
  }).filter(Boolean);
}

function trendSection(det) {
  const days = det.daily;
  const sum = (s, k) => s.reduce((a, d) => a + (d[k] || 0), 0);
  const roas = rolling(days, (s) => {
    const sp = sum(s, 'spend');
    const reported = s.some((d) => d.purchase_value !== null);
    return sp > 0 && reported ? sum(s, 'purchase_value') / sp : null;
  });
  const ctr = rolling(days, (s) => { const im = sum(s, 'impressions'); return im > 0 ? sum(s, 'link_clicks') / im * 100 : null; });
  const spend = days.filter((d) => d.in_range).map((d) => ({ x: shortDate(d.date), y: d.spend }));
  const f = det.fatigue;
  const fbox = f ? `<div class="${['declining', 'ctr_down', 'roas_down'].includes(f.code) ? 'warnbox' : 'infobox'}"><strong>${esc(f.label)}.</strong> ${esc(f.reason)}` +
    (f.recent ? `<br><span class="small">Last 7 days (${esc(shortDate(f.recent_range[0]))} to ${esc(shortDate(f.recent_range[1]))}): link CTR ${fmt(f.recent.link_ctr, 'pct')}, ROAS ${fmt(f.recent.roas, 'x')}. The 21 days before: link CTR ${fmt(f.baseline.link_ctr, 'pct')}, ROAS ${fmt(f.baseline.roas, 'x')}.</span>` : '') + '</div>' : '';
  return `<section><h3>Trend and fatigue</h3>${fbox}
    ${sparkChart(spend, { kind: 'bar', color: '#2a78d6', fmtY: (v) => money(v), title: 'Daily spend' })}
    ${sparkChart(roas, { color: '#eb6834', fmtY: (v) => v.toFixed(2) + 'x', title: 'Purchase ROAS, rolling 7 days' })}
    ${sparkChart(ctr, { color: '#2a78d6', fmtY: (v) => v.toFixed(2) + '%', title: 'Link CTR, rolling 7 days' })}
    <p class="small muted">Rolling lines use the 7 days up to each date. A gap means no purchases were reported in that 7-day span.</p></section>`;
}

function breakdownTable(obj, head, total) {
  const rows = Object.entries(obj || {}).map(([k, v]) => ({ key: k, ...v })).sort((a, b) => b.spend - a.spend);
  if (!rows.length) return `<p>${NA}</p>`;
  return `<table><tr><th>${head}</th><th class="n">Spend</th><th class="n">Share</th><th class="n">Purch.</th><th class="n">Value</th><th class="n">ROAS</th></tr>` +
    rows.map((r) => `<tr><td>${esc(r.key.replace(/_/g, ' '))}</td><td class="n">${fmt(r.spend, 'money')}</td><td class="n">${total ? (r.spend / total * 100).toFixed(1) + '%' : NA}</td>
      <td class="n">${fmt(r.purchases, 'int')}</td><td class="n">${fmt(r.purchase_value, 'money')}</td><td class="n">${fmt(r.roas, 'x')}</td></tr>`).join('') + '</table>';
}

async function openPanel(id) {
  let ad;
  try { ad = await getJSON(`/api/ad/${encodeURIComponent(id)}?` + filterQuery(state)); } catch (e) { return; }
  const det = ad.detail;
  const m = det.metrics;
  const p = $('compare').checked ? det.prev_metrics : null;
  const c = ad.creative;
  const kv = (rows) => '<table class="kv">' + rows.map(([k, v]) => `<tr><td>${esc(k)}</td><td>${v}</td></tr>`).join('') + '</table>';
  const idl = (name, idv) => `${esc(name)}<br><span class="small muted">${esc(idv)}</span>`;
  const view = VIEW.ads[id] ? VIEW.ads[id].view : null;
  const same = (view ? view.same_media_ads : []).map((x) => esc(VIEW.ads[x]?.name || x) + ` <span class="small muted">(${esc(x)})</span>`).join('<br>');
  const landing = c.link_url ? link(c.link_url) : (c.type === 'carousel' ? 'Per card, see above' : NA);
  const bdTotal = Object.values(det.breakdowns.age || {}).reduce((s, r) => s + r.spend, 0);
  const cmpRow = (label, key, kind, good) => [label, fmt(m[key], kind) + (p ? ` ${delta(m[key], p[key], good)} <span class="small muted">prev ${fmt(p[key], kind)}</span>` : '')];
  const r = det.range;
  const v = det.verdict;

  $('panelTitle').textContent = ad.name;
  $('panelBody').innerHTML = `
    ${mediaSection(ad)}
    ${v ? `<div class="verdict-box ${VERDICT_CLASS[v.code] || ''}"><strong>${esc(v.label)}.</strong> ${esc(v.reason)}</div>` : ''}
    ${ad.flags.map((f) => `<div class="warnbox">${esc(f)}</div>`).join('')}
    <section><h3>Performance, whole ad, ${esc(dateLabel(r.since))} to ${esc(dateLabel(r.until))}</h3>${kv([
      cmpRow('Spend', 'spend', 'money2', 0),
      cmpRow('Attributed purchase value', 'purchase_value', 'money2', 1),
      cmpRow('Purchases', 'purchases', 'int', 1),
      cmpRow('Purchase ROAS', 'roas', 'x', 1),
      cmpRow('CPA', 'cpa', 'money2', -1),
      cmpRow('Impressions', 'impressions', 'int', 0),
      cmpRow('Link CTR', 'link_ctr', 'pct', 1),
      cmpRow('Link CPC', 'link_cpc', 'money2', -1),
      ['Days with spend', `${m.days_active} of ${r.days}` + (m.first_day ? ` <span class="small muted">(${esc(shortDate(m.first_day))} to ${esc(shortDate(m.last_day))})</span>` : '')],
      ['Rank by spend', view ? `#${view.rank_by_spend} of ${VIEW.totals.ads} ads that spent` : 'Not in the current view'],
    ])}${p ? `<p class="small muted">Previous period: ${esc(dateLabel(det.previous.since))} to ${esc(dateLabel(det.previous.until))}.</p>` : ''}</section>
    ${trendSection(det)}
    <section><h3>Creative</h3>${kv([
      ['Format', esc(c.type_label)],
      ['Headline', c.headline ? esc(c.headline) : NA],
      ['Call to action', c.cta ? esc(c.cta.replace(/_/g, ' ').toLowerCase()) : NA],
      ['Landing page', landing],
      ['Facebook post', c.post_url ? link(c.post_url, 'Open post') : NA],
      ...(c.product_set_id ? [['Product set ID', esc(c.product_set_id)]] : []),
      ['Creative ID', esc(c.id)],
    ])}
    <h3 style="margin-top:10px">Primary text</h3><div class="copy">${c.primary_text ? esc(c.primary_text) : NA}</div></section>
    <section><h3>Structure</h3>${kv([
      ['Campaign', idl(ad.campaign_name, ad.campaign_id)],
      ['Ad set', idl(ad.adset_name, ad.adset_id)],
      ['Ad', idl(ad.name, ad.id)],
      ['Delivery status', esc(statusLabel(ad.effective_status))],
      [`Same ${c.type === 'video' ? 'video' : 'image'} used by`, same || 'No other ad that spent in these dates'],
    ])}</section>
    <section><h3>Breakdowns</h3>
      <p class="small muted">${esc(bucketNote(det.breakdown_buckets, false, r).replace('these charts cover', 'these tables cover'))} Each table splits the same spend. Do not add the tables together.</p>
      <h3>Age</h3>${breakdownTable(det.breakdowns.age, 'Age', bdTotal)}
      <h3>Gender</h3>${breakdownTable(det.breakdowns.gender, 'Gender', bdTotal)}
      <h3>Platform</h3>${breakdownTable(det.breakdowns.publisher_platform, 'Platform', bdTotal)}</section>
    <section><h3>Report context</h3>${kv([
      ['Dates', `${dateLabel(r.since)} to ${dateLabel(r.until)} (${r.days} days)`],
      ['Currency', esc(META.meta.currency)],
      ['Account timezone', esc(META.meta.timezone || 'Unavailable')],
      ['Attribution setting', esc(attribution(ad.attribution_setting))],
      ['Targets used', `ROAS ${det.targets.roas ? det.targets.roas.toFixed(2) + 'x' : 'not set'} · CPA ${det.targets.cpa ? money(det.targets.cpa) : 'not set'}`],
      ['Data captured', esc(new Date(META.meta.captured_at).toLocaleString('en-IN'))],
      ['Source', esc(META.meta.source)],
    ])}<p class="small muted">${esc(META.meta.attribution_note)}</p></section>`;
  $('panel').classList.add('open');
  $('panel').setAttribute('aria-hidden', 'false');
  $('scrim').hidden = false;
}

// ---- exclusions, presets and targets --------------------------------------
function fillCampaignList() {
  const q = ($('campSearch').value || '').toLowerCase();
  const list = META.campaigns.filter((c) => !q || (c.name || '').toLowerCase().includes(q));
  $('campList').innerHTML = list.map((c) => `<label class="camp"><input type="checkbox" value="${esc(c.id)}"${state.camp.includes(c.id) ? ' checked' : ''}>
    <span>${esc(c.name)}<br><span class="small muted">${money(c.spend)} in the year · ${c.first_day ? esc(shortDate(c.first_day)) + ' to ' + esc(shortDate(c.last_day)) : ''}</span></span></label>`).join('') ||
    '<p class="small muted">No campaign matches.</p>';
}

function fillPresets() {
  $('presetSel').innerHTML = '<option value="">None</option>' + SETTINGS.presets.map((p) => `<option value="${esc(p.name)}">${esc(p.name)}</option>`).join('');
  $('presetSel').value = state.preset && SETTINGS.presets.some((p) => p.name === state.preset) ? state.preset : '';
}

function fillTargets() {
  $('tRoas').value = SETTINGS.targets.roas ?? '';
  $('tCpa').value = SETTINGS.targets.cpa ?? '';
  $('tRoas').placeholder = 'Average';
  $('tCpa').placeholder = 'Average';
}

async function persist(next, msg) {
  try {
    SETTINGS = await saveSettings(next);
    $('error').textContent = '';
    flash(msg);
  } catch (e) {
    $('error').textContent = 'Could not save: ' + e.message;
  }
}

function flash(msg) {
  $('exclNote').insertAdjacentHTML('afterbegin', `<strong class="saved">${esc(msg)} </strong>`);
}

async function savePreset() {
  if ($('kw').value.trim()) addKeywords($('kw').value);
  if (!state.kw.length && !state.camp.length) { $('error').textContent = 'Add a keyword or pick a campaign first.'; return; }
  const name = ($('presetName').value || state.preset || state.kw.join(', ')).trim().slice(0, 60);
  if (!name) { $('error').textContent = 'Type a preset name first.'; return; }
  $('presetName').value = '';
  const presets = SETTINGS.presets.filter((p) => p.name !== name).concat([{ name, keywords: state.kw, campaign_ids: state.camp }]);
  await persist({ ...SETTINGS, presets }, `Saved preset "${name}".`);
  state.preset = name;
  fillPresets();
  renderExclusions();
}

async function deletePreset() {
  if (!state.preset) return;
  const name = state.preset;
  await persist({ ...SETTINGS, presets: SETTINGS.presets.filter((p) => p.name !== name) }, `Deleted preset "${name}".`);
  state.preset = '';
  fillPresets();
  renderExclusions();
}

async function saveTargets() {
  const roas = parseFloat($('tRoas').value);
  const cpa = parseFloat($('tCpa').value);
  await persist({ ...SETTINGS, targets: { roas: roas > 0 ? roas : null, cpa: cpa > 0 ? cpa : null } }, 'Targets saved.');
  fillTargets();
  refresh();
}

function closePanel() {
  $('panel').classList.remove('open');
  $('panel').setAttribute('aria-hidden', 'true');
  $('scrim').hidden = true;
}
$('close').addEventListener('click', closePanel);
$('scrim').addEventListener('click', closePanel);
document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closePanel(); });
load();
