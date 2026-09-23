'use strict';
// Shared ad gallery. Data is a read-only snapshot shipped with the page (data.json).
// Team settings (targets, exclusion presets, report branding) live in settings.json and are
// saved by republishing that one file. People without edit access get a read-only page.
const $ = (id) => document.getElementById(id);
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const NA = '<span class="na" title="Meta reported no value for this metric in these dates. It is not counted as zero.">Unavailable</span>';
const DEFAULT_SETTINGS = { targets: { roas: null, cpa: null }, presets: [], branding: { agency: '', client: '', note: '' } };

let DATA = null, ENGINE = null, VIEW = null, CAMPAIGNS = [], THUMBS = null, NOTES = {}, COMPETITORS = null, COMP_MEDIA = {};
// Inside claude.ai the page saves by republishing its files; run locally it saves through the local server.
const IS_CLAUDE = !!(window.claude && window.claude.use);
const TABS = ['overview', 'actions', 'sales', 'gallery', 'campaigns', 'insights', 'studio', 'competitors', 'report'];
let SETTINGS = JSON.parse(JSON.stringify(DEFAULT_SETTINGS));
let CAN_SAVE = true;           // becomes false after the first refused save
const state = { since: null, until: null, kw: [], camp: [], preset: '', tab: 'overview', compare: [] };

// ---------- formatting ----------
const nf0 = new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 });
const nf2 = new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 2 });
const money = (v) => nf0.format(v);
function fmt(v, kind) {
  if (v === null || v === undefined || Number.isNaN(v)) return NA;
  if (kind === 'money') return money(v);
  if (kind === 'money2') return nf2.format(v);
  if (kind === 'int') return Math.round(v).toLocaleString('en-IN');
  if (kind === 'x') return v.toFixed(2) + 'x';
  if (kind === 'pct') return v.toFixed(2) + '%';
  return esc(v);
}
const dateLabel = (iso) => new Date(iso + 'T00:00:00Z').toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric', timeZone: 'UTC' });
const shortDate = (iso) => new Date(iso + 'T00:00:00Z').toLocaleDateString('en-IN', { day: 'numeric', month: 'short', timeZone: 'UTC' });
function addDays(iso, n) { const d = new Date(iso + 'T00:00:00Z'); d.setUTCDate(d.getUTCDate() + n); return d.toISOString().slice(0, 10); }
const statusLabel = (s) => (s || 'unknown').replace(/_/g, ' ').toLowerCase();
const secs = (n) => (n ? `${Math.round(n)}s` : '');
const link = (url, text) => `<a href="${esc(url)}" target="_blank" rel="noopener noreferrer">${esc(text || url)}</a>`;
const parseKw = (text) => cleanKeywords(String(text || '').split(','));
function delta(cur, prev, good) {
  if (cur === null || cur === undefined || prev === null || prev === undefined || prev === 0) return '';
  const ch = (cur - prev) / Math.abs(prev);
  if (!Number.isFinite(ch)) return '';
  const tone = Math.abs(ch) < 0.005 || !good ? 'flat' : (ch > 0) === (good > 0) ? 'good' : 'bad';
  return `<span class="delta ${tone}">${ch > 0 ? '▲' : ch < 0 ? '▼' : ''} ${ch > 0 ? '+' : ''}${(ch * 100).toFixed(1)}%</span>`;
}
const VCLASS = { scale: 'v-scale', watch: 'v-watch', cut: 'v-cut' };
const verdictChip = (v) => (v ? `<span class="chip ${VCLASS[v.code] || ''}" title="${esc(v.reason)}">${esc(v.label)}</span>` : '');
const FATIGUED = ['declining', 'ctr_down', 'roas_down'];
const fatigueChip = (f) => (f && FATIGUED.includes(f.code) ? `<span class="chip flag" title="${esc(f.reason)}">${esc(f.code === 'declining' ? 'Fatigue' : f.label)}</span>` : '');
function thumbSrc(adId) {
  if (!IS_CLAUDE && THUMBS && !Object.keys(THUMBS.ads).length) return '/img/' + encodeURIComponent(adId);
  if (!THUMBS) return null;
  const key = THUMBS.ads[adId];
  return key && THUMBS.images[key] ? 'data:image/jpeg;base64,' + THUMBS.images[key] : null;
}
function thumbHtml(adId, alt) {
  const src = thumbSrc(adId);
  return src ? `<img loading="lazy" src="${src}" alt="${esc(alt)}">` : `<div class="noimg">${THUMBS ? 'No preview' : 'Loading preview…'}</div>`;
}

// ---------- per-viewer memory (filters only) ----------
function remember() {
  try { localStorage.setItem('gallery-state', JSON.stringify({ since: state.since, until: state.until, kw: state.kw, camp: state.camp, xp: state.preset, preset: $('preset').value, fmt: $('format').value, compare: $('compare').checked })); } catch (e) { /* storage unavailable */ }
}
function recall() {
  try { return JSON.parse(localStorage.getItem('gallery-state') || 'null'); } catch (e) { return null; }
}

// Client facing name for where the numbers came from.
function sourceLabel() { return 'Meta Ads Manager, read-only'; }

// ---------- boot ----------
async function boot() {
  try {
    const opt = (name) => fetch(name).then((r) => (r.ok ? r.json() : null)).catch(() => null);
    const [d, s, n, comp, media] = await Promise.all([fetch('data.json').then((r) => r.json()), opt('settings.json'), opt('notes.json'), opt('competitors.json'), opt('comp_media.json')]);
    DATA = d;
    NOTES = n && typeof n === 'object' ? n : {};
    COMPETITORS = comp;
    COMP_MEDIA = media && typeof media === 'object' ? media : {};
    if (s) SETTINGS = { ...SETTINGS, ...s, targets: { ...SETTINGS.targets, ...(s.targets || {}) }, branding: { ...SETTINGS.branding, ...(s.branding || {}) } };
  } catch (e) {
    $('loading').textContent = 'Could not load the ad data. Reload the page to try again.';
    return;
  }
  ENGINE = new GalleryEngine(DATA);
  CAMPAIGNS = ENGINE.campaigns();
  const m = DATA.meta;
  $('acct').textContent = `${m.account_name || 'Meta ads'}`;
  $('navAcct').textContent = m.account_name || 'Meta ads';
  $('navSub').textContent = `act_${m.account_id} · ${m.currency}`;
  $('navFoot').textContent = `Captured ${dateLabel(String(m.captured_at).slice(0, 10))}. Nothing here can change the ad account.`;
  $('acctSub').textContent = `act_${m.account_id} · ${m.currency} · ${m.timezone || ''} · data ${dateLabel(m.window.since)} to ${dateLabel(m.window.until)}`;
  $('footer').textContent = `Snapshot captured ${new Date(m.captured_at).toLocaleString('en-IN')} from ${sourceLabel()}. It does not refresh on its own. Purchases and value are Meta's figures under each ad set's attribution setting.`;
  for (const id of ['since', 'until']) { $(id).min = m.window.since; $(id).max = m.window.until; }
  $('format').innerHTML = m.formats.map((f) => `<option value="${esc(f)}">${esc(m.format_labels[f])}</option>`).join('');

  const saved = recall();
  if (saved && saved.since >= m.window.since && saved.until <= m.window.until && saved.since <= saved.until) {
    Object.assign(state, { since: saved.since, until: saved.until, kw: cleanKeywords(saved.kw || []), camp: (saved.camp || []).filter((i) => /^\d{5,25}$/.test(i)) });
    $('preset').value = saved.preset && $('preset').querySelector(`option[value="${saved.preset}"]`) ? saved.preset : 'custom';
    if (saved.fmt && m.formats.includes(saved.fmt)) $('format').value = saved.fmt;
    $('compare').checked = saved.compare !== false;
    if (['7', '14', '30', '90', '180', '365', 'this_month', 'last_month'].includes($('preset').value)) applyPreset($('preset').value);
  } else {
    applyPreset($('preset').value);
  }
  state.preset = saved && saved.xp ? saved.xp : '';
  $('since').value = state.since; $('until').value = state.until;
  fillPresets(); fillTargets(); fillBranding(); fillCampaignList(); renderPills();
  wire();
  $('loading').hidden = true;
  refresh();
  const fromHash = (location.hash || '').slice(1);
  let savedTab = null;
  try { savedTab = localStorage.getItem('gallery-tab'); } catch (e) { /* storage unavailable */ }
  setTab(TABS.includes(fromHash) ? fromHash : TABS.includes(savedTab) ? savedTab : 'overview');
  fetch('thumbs.json').then((r) => (r.ok ? r.json() : Promise.reject())).then((t) => { THUMBS = t; renderGrid(); renderTab(); })
    .catch(() => { THUMBS = { ads: {}, images: {} }; renderGrid(); renderTab(); });
}

function wire() {
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
    else if (b) { state.camp = state.camp.filter((x) => x !== b.dataset.camp); exclusionsChanged(); }
    else $('kw').focus();
  });
  $('campSearch').addEventListener('input', fillCampaignList);
  $('campList').addEventListener('change', (e) => {
    if (!e.target.matches('input[type=checkbox]')) return;
    const id = e.target.value;
    state.camp = e.target.checked ? [...new Set([...state.camp, id])] : state.camp.filter((x) => x !== id);
    state.preset = ''; $('presetSel').value = '';
    renderPills(); refresh();
  });
  $('presetSel').addEventListener('change', () => {
    const p = SETTINGS.presets.find((x) => x.name === $('presetSel').value);
    state.preset = p ? p.name : '';
    state.kw = p ? [...p.keywords] : [];
    state.camp = p ? [...p.campaign_ids] : [];
    fillCampaignList(); renderPills(); refresh();
  });
  $('savePreset').addEventListener('click', savePreset);
  $('delPreset').addEventListener('click', deletePreset);
  $('saveTargets').addEventListener('click', saveTargets);
  $('saveBrand').addEventListener('click', saveBranding);
  $('dlReport').addEventListener('click', downloadReport);
  for (const id of ['agency', 'client', 'note']) $(id).addEventListener('input', renderReport);
  for (const id of ['sort', 'verdict', 'minSpend', 'minRoas', 'campaign', 'adStatus']) $(id).addEventListener('input', renderGrid);
  $('format').addEventListener('change', () => { fillFilters(); renderGrid(); remember(); });
  for (const t of TABS) $('tab-' + t).addEventListener('click', () => { setTab(t); window.scrollTo(0, 0); });
  $('exportGrid').addEventListener('click', exportGridCsv);
  $('grid').addEventListener('change', (e) => { if (e.target.matches('input[data-compare]')) toggleCompare(e.target.dataset.compare, e.target.checked); });
  $('compareOpen').addEventListener('click', openCompare);
  $('compareClear').addEventListener('click', () => { state.compare = []; renderTray(); renderGrid(); });
  $('sideBody').addEventListener('submit', (e) => { if (e.target.id === 'noteForm') { e.preventDefault(); addNote(e.target); } });
  if (window.initInsights) window.initInsights();
  if (window.initStudio) window.initStudio();
  $('filterToggle').addEventListener('click', () => {
    const open = $('filterPanel').hidden;
    $('filterPanel').hidden = !open;
    $('filterToggle').setAttribute('aria-expanded', String(open));
    if (open) $('kw').focus();
  });
  $('close').addEventListener('click', closeSide);
  $('scrim').addEventListener('click', closeSide);
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeSide(); });
}

function setTab(tab) {
  state.tab = tab;
  try { localStorage.setItem('gallery-tab', tab); } catch (e) { /* storage unavailable */ }
  for (const t of TABS) {
    $('tab-' + t).setAttribute('aria-selected', String(t === tab));
    $(t + 'View').hidden = t !== tab;
  }
  renderTray();
  renderTab();
}
function renderTab() {
  if (!VIEW) return;
  if (state.tab === 'report') renderReport();
  if (state.tab === 'overview' && window.renderOverview) window.renderOverview();
  if (state.tab === 'actions' && window.renderActions) window.renderActions();
  if (state.tab === 'studio' && window.renderStudio) window.renderStudio();
  if (state.tab === 'sales' && window.renderSales) window.renderSales();
  if (state.tab === 'campaigns' && window.renderCampaigns) window.renderCampaigns();
  if (state.tab === 'insights' && window.renderInsights) window.renderInsights();
  if (state.tab === 'competitors' && window.renderCompetitors) window.renderCompetitors();
}

function applyPreset(v) {
  const end = DATA.meta.window.until, start = DATA.meta.window.since;
  if (v === 'custom') return;
  if (v === 'this_month') { state.since = end.slice(0, 8) + '01'; state.until = end; }
  else if (v === 'last_month') { const le = addDays(end.slice(0, 8) + '01', -1); state.since = le.slice(0, 8) + '01'; state.until = le; }
  else { state.until = end; state.since = addDays(end, -(parseInt(v, 10) - 1)); }
  if (state.since < start) state.since = start;
  $('since').value = state.since; $('until').value = state.until;
}

function refresh() {
  $('error').textContent = '';
  try {
    VIEW = ENGINE.view(state.since, state.until, state.kw, state.camp, SETTINGS.targets);
  } catch (e) {
    $('error').textContent = e.message;
    return;
  }
  remember();
  renderAll();
}

function renderAll() {
  const r = VIEW.range, pv = VIEW.previous, cmp = $('compare').checked;
  $('rangeLabel').innerHTML = `${esc(dateLabel(r.since))} to ${esc(dateLabel(r.until))} · ${r.days} days` +
    (cmp ? (pv.days_covered ? ` <span class="muted">vs ${esc(dateLabel(pv.since))} to ${esc(dateLabel(pv.until))}${pv.complete ? '' : ` (only ${pv.days_covered} of ${pv.days} days are in the data, so no change figures)`}</span>`
      : ' <span class="muted">No earlier data to compare with.</span>') : '');
  renderPills(); renderStatus(); renderKpis(); renderFormats(); fillFilters(); renderGrid(); renderTray();
  renderTab();
}

// ---------- exclusions ----------
function exclusionsChanged() { state.preset = ''; $('presetSel').value = ''; renderPills(); fillCampaignList(); refresh(); }
function addKeywords(text) {
  $('kw').value = '';
  const add = parseKw(text).filter((k) => !state.kw.includes(k));
  if (!add.length) return;
  state.kw = [...state.kw, ...add].slice(0, 20);
  exclusionsChanged();
}
function removeKeyword(k) { state.kw = state.kw.filter((x) => x !== k); exclusionsChanged(); $('kw').focus(); }

function renderPills() {
  const x = VIEW ? VIEW.exclusions : null;
  const hits = {};
  for (const c of (x ? x.campaigns : [])) {
    const h = hits[c.matched] || (hits[c.matched] = { n: 0, spend: 0 });
    h.n += 1; h.spend += c.spend;
  }
  const names = new Map(CAMPAIGNS.map((c) => [c.id, c.name]));
  const kw = state.kw.map((k) => {
    const known = x && x.keywords.includes(k), h = hits[k];
    const info = !known ? '' : h ? `${h.n} campaign${h.n > 1 ? 's' : ''} · ${money(h.spend)}` : 'no campaign spent in these dates';
    return `<span class="pill${known && !h ? ' idle' : ''}" title="Campaigns whose name contains &quot;${esc(k)}&quot;${info ? ': ' + esc(info) : ''}"><span class="pill-text">${esc(k)}</span>${info ? `<span class="pill-info">${esc(info)}</span>` : ''}<button type="button" data-kw="${esc(k)}" aria-label="Stop excluding ${esc(k)}">×</button></span>`;
  });
  const camp = state.camp.map((id) => `<span class="pill camp" title="${esc(names.get(id) || id)}"><span class="pill-text">${esc(names.get(id) || id)}</span><button type="button" data-camp="${esc(id)}" aria-label="Stop excluding this campaign">×</button></span>`);
  $('kwPills').innerHTML = kw.join('') + camp.join('');
  $('kwBox').classList.toggle('active', state.kw.length + state.camp.length > 0);
  $('kw').placeholder = state.kw.length || state.camp.length ? 'Add another word' : 'Type a word in the campaign name, then press comma or Enter';
  $('campCount').textContent = state.camp.length ? `(${state.camp.length} picked)` : '';
  $('filterCount').textContent = state.kw.length + state.camp.length ? String(state.kw.length + state.camp.length) : '';
  $('delPreset').hidden = !state.preset || !CAN_SAVE;
}

function renderStatus(msg) {
  const x = VIEW ? VIEW.exclusions : null;
  let line = 'No campaigns excluded. Totals, the top 30 and charts cover every campaign.';
  if (x && (x.keywords.length || x.campaign_ids.length)) {
    const list = x.campaigns.map((c) => `${c.name} (${money(c.spend)})`).join('\n');
    line = x.campaigns.length
      ? `<strong>Left out of every number:</strong> ${x.campaigns.length} campaign${x.campaigns.length > 1 ? 's' : ''}, ${x.ads} ads, ${money(x.spend)} spend in these dates. <span class="linkish" title="${esc(list)}">Which campaigns?</span>`
      : 'The exclusion matches no campaign that spent in these dates.';
  }
  const ro = CAN_SAVE ? '' : ' <span class="readonly">You can view and filter, but saving for the team is off for you. Ask the owner for edit access.</span>';
  $('status').innerHTML = (msg ? `<span class="saved">${esc(msg)}</span> ` : '') + line + ro;
}

function fillCampaignList() {
  const q = ($('campSearch').value || '').toLowerCase();
  const list = CAMPAIGNS.filter((c) => !q || (c.name || '').toLowerCase().includes(q));
  $('campList').innerHTML = list.map((c) => `<label class="camp"><input type="checkbox" value="${esc(c.id)}"${state.camp.includes(c.id) ? ' checked' : ''}><span>${esc(c.name)}<br><span class="small muted">${money(c.spend)} in the year · ${c.first_day ? esc(shortDate(c.first_day)) + ' to ' + esc(shortDate(c.last_day)) : ''}</span></span></label>`).join('') || '<p class="small muted">No campaign matches.</p>';
}
function fillPresets() {
  $('presetSel').innerHTML = '<option value="">None</option>' + SETTINGS.presets.map((p) => `<option value="${esc(p.name)}">${esc(p.name)}</option>`).join('');
  $('presetSel').value = state.preset && SETTINGS.presets.some((p) => p.name === state.preset) ? state.preset : '';
}
function fillTargets() { $('tRoas').value = SETTINGS.targets.roas ?? ''; $('tCpa').value = SETTINGS.targets.cpa ?? ''; }
function fillBranding() { $('agency').value = SETTINGS.branding.agency || ''; $('client').value = SETTINGS.branding.client || ''; $('note').value = SETTINGS.branding.note || ''; }

// ---------- saving team settings ----------
function cleanSettings(s) {
  const txt = (v, n) => String(v ?? '').replace(/[\u0000-\u001f\u007f]/g, ' ').trim().slice(0, n);
  const pos = (v) => { const f = parseFloat(v); return f > 0 && f < 1e9 ? f : null; };
  return {
    targets: { roas: pos(s.targets.roas), cpa: pos(s.targets.cpa) },
    presets: (s.presets || []).slice(0, 30).map((p) => ({ name: txt(p.name, 60), keywords: cleanKeywords(p.keywords), campaign_ids: (p.campaign_ids || []).filter((i) => /^\d{5,25}$/.test(i)).slice(0, 200) })).filter((p) => p.name),
    branding: { agency: txt(s.branding.agency, 80), client: txt(s.branding.client, 80), note: txt(s.branding.note, 400) },
  };
}
// Save one shared file (settings.json or notes.json). Returns 'saved', 'local-only' or an error message.
async function saveFile(name, obj) {
  if (!CAN_SAVE) return 'local-only';
  const body = JSON.stringify(obj, null, 1);
  if (!IS_CLAUDE) {
    try {
      const r = await fetch('/api/save/' + name, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body });
      if (r.ok) return 'saved';
      const j = await r.json().catch(() => ({}));
      if (r.status === 404 || r.status === 405 || r.status === 501) { CAN_SAVE = false; return 'local-only'; }
      return j.error || 'Could not save.';
    } catch (e) { return 'Could not reach the local server.'; }
  }
  const artifact = await window.claude.use('artifact');
  if (!artifact) { CAN_SAVE = false; return 'local-only'; }
  try {
    await artifact.publish({ [name]: { content: body, contentType: 'application/json' } });
    return 'saved';
  } catch (e) {
    const code = e && e.code;
    if (code === 'conflict') return 'Someone else saved first. The page is reloading with their version.';
    if (code === 'rate_limited') return 'Saving too often. Wait a minute and save again.';
    if (code === 'upstream_error') return 'Could not save just now. Try again in a moment.';
    CAN_SAVE = false;
    return 'local-only';
  }
}
async function persist(next, okMsg) {
  const clean = cleanSettings(next);
  SETTINGS = clean;   // applies for this viewer right away
  const r = await saveFile('settings.json', clean);
  renderStatus(r === 'saved' ? okMsg : r === 'local-only' ? 'Applied for you only.' : r);
  return r === 'saved';
}

// Offer a generated file. Inside claude.ai this asks the viewer; locally it is a normal browser download.
async function downloadFile(filename, text) {
  if (!IS_CLAUDE) {
    const url = URL.createObjectURL(new Blob([text], { type: filename.endsWith('.csv') ? 'text/csv' : 'text/html' }));
    const a = Object.assign(document.createElement('a'), { href: url, download: filename });
    document.body.append(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 5000);
    return 'Saved to your downloads.';
  }
  const dl = await window.claude.use('downloads');
  if (!dl) return 'Downloads are not available in this view.';
  try { await dl.save({ filename, data: text }); return 'Saved.'; }
  catch (e) { const c = e && e.code; return c === 'declined' ? 'Download cancelled.' : c === 'rate_limited' ? 'A download prompt is already open.' : 'Downloads are not available in this view.'; }
}
function csv(rows) {
  const cell = (v) => { if (v === null || v === undefined) return ''; const t = String(v); return /[",\n]/.test(t) ? '"' + t.replace(/"/g, '""') + '"' : t; };
  return '\ufeff' + rows.map((r) => r.map(cell).join(',')).join('\r\n');
}
const r2 = (v) => (v === null || v === undefined ? null : Math.round(v * 100) / 100);
function fileStamp() { return `${VIEW.range.since} to ${VIEW.range.until}`; }
async function savePreset() {
  if ($('kw').value.trim()) addKeywords($('kw').value);
  if (!state.kw.length && !state.camp.length) { $('error').textContent = 'Add a word or pick a campaign first.'; return; }
  const name = ($('presetName').value || state.preset || state.kw.join(', ')).trim().slice(0, 60);
  const presets = SETTINGS.presets.filter((p) => p.name !== name).concat([{ name, keywords: state.kw, campaign_ids: state.camp }]);
  $('presetName').value = '';
  await persist({ ...SETTINGS, presets }, `Saved "${name}" for the team.`);
  state.preset = name; fillPresets(); renderPills(); remember();
}
async function deletePreset() {
  const name = state.preset;
  if (!name) return;
  await persist({ ...SETTINGS, presets: SETTINGS.presets.filter((p) => p.name !== name) }, `Deleted "${name}".`);
  state.preset = ''; fillPresets(); renderPills();
}
async function saveTargets() {
  await persist({ ...SETTINGS, targets: { roas: $('tRoas').value, cpa: $('tCpa').value } }, 'Targets saved for the team.');
  fillTargets(); refresh();
}
async function saveBranding() {
  const ok = await persist({ ...SETTINGS, branding: { agency: $('agency').value, client: $('client').value, note: $('note').value } }, 'Branding saved for the team.');
  $('dlMsg').textContent = ok ? 'Branding saved for the team.' : CAN_SAVE ? $('dlMsg').textContent : 'Branding applies for you only. Saving for the team is off for you.';
}

// ---------- summary ----------
function kpiSet(v, compare) {
  const t = v.totals, p = v.previous_totals || {}, tg = v.targets;
  const show = compare && v.previous.complete;
  const one = (label, cur, prev, kind, good, note) => `<div class="kpi"><div class="k-label">${esc(label)}</div><div class="k-val">${fmt(cur, kind)}</div>` +
    (show ? `<div class="k-prev">${delta(cur, prev, good)} <span class="muted">prev ${fmt(prev, kind)}</span></div>` : '') + (note ? `<div class="k-note muted">${note}</div>` : '') + '</div>';
  return [one('Spend', t.spend, p.spend, 'money', 0), one('Purchase value', t.purchase_value, p.purchase_value, 'money', 1),
    one('ROAS', t.roas, p.roas, 'x', 1, `Target ${tg.roas ? tg.roas.toFixed(2) + 'x' : 'not set'} (${esc(tg.roas_source)})`),
    one('Purchases', t.purchases, p.purchases, 'int', 1), one('CPA', t.cpa, p.cpa, 'money', -1, `Target ${tg.cpa ? money(tg.cpa) : 'not set'} (${esc(tg.cpa_source)})`),
    one('Link CTR', t.link_ctr, p.link_ctr, 'pct', 1)].join('');
}
function renderKpis() {
  const t = VIEW.totals;
  $('kpis').innerHTML = kpiSet(VIEW, $('compare').checked) + `<p class="small muted" style="grid-column: 1 / -1; margin: 0">${t.ads} ads spent in these dates. ROAS = total purchase value ÷ total spend. ${t.ads_without_reported_value} ads had no reported purchase value; their spend still counts.</p>`;
}
function formatTable(v) {
  const t = v.totals;
  const rows = Object.values(v.by_type).sort((a, b) => b.spend - a.spend);
  const fr = (label, x, strong) => `<tr${strong ? ' class="total"' : ''}><td>${esc(label)}</td><td class="n">${x.ads}</td><td class="n">${fmt(x.spend, 'money')}</td><td class="n">${t.spend ? (x.spend / t.spend * 100).toFixed(1) + '%' : ''}</td><td class="n">${fmt(x.purchase_value, 'money')}</td><td class="n">${fmt(x.roas, 'x')}</td><td class="n">${fmt(x.cpa, 'money')}</td></tr>`;
  return '<table><tr><th>Format</th><th class="n">Ads</th><th class="n">Spend</th><th class="n">Share</th><th class="n">Purchase value</th><th class="n">ROAS</th><th class="n">CPA</th></tr>' + rows.map((x) => fr(x.label, x)).join('') + fr('All formats', t, true) + '</table>';
}
function renderFormats() {
  $('formats').querySelector('summary').textContent = `Spend, purchase value and ROAS by format · all ${VIEW.totals.ads} ads that spent in these dates`;
  $('formats').querySelector('.scroll').innerHTML = formatTable(VIEW);
}

const AGE_ORDER = ['13-17', '18-24', '25-34', '35-44', '45-54', '55-64', '65+', 'Unknown', 'unknown'];
const GENDER_ORDER = ['female', 'male', 'unknown'];
function aggregate(demos, dim) {
  const acc = {};
  for (const d0 of demos) {
    for (const [k, b] of Object.entries((d0 || {})[dim] || {})) {
      const a = acc[k] || (acc[k] = { spend: 0, value: 0, purchases: 0, reported: false });
      a.spend += b.spend;
      if (b.purchase_value !== null) { a.value += b.purchase_value; a.reported = true; }
      if (b.purchases !== null) a.purchases += b.purchases;
    }
  }
  const order = dim === 'age' ? AGE_ORDER : GENDER_ORDER;
  const pos = (k) => (order.indexOf(k) < 0 ? 99 : order.indexOf(k));
  return Object.entries(acc).filter(([, a]) => a.spend > 0).sort((x, y) => pos(x[0]) - pos(y[0])).map(([k, a]) => ({ key: k, ...a, roas: a.reported ? a.value / a.spend : null }));
}
function barChart(title, rows, getV, fmtV, cls, total) {
  const max = Math.max(...rows.map((r) => getV(r) || 0), 0) || 1;
  return `<figure class="mini"><figcaption>${esc(title)}</figcaption>` + rows.map((r) => {
    const v = getV(r), w = v ? Math.max(1.5, v / max * 100) : 0;
    const tip = `${r.key}: spend ${money(r.spend)} (${(r.spend / total * 100).toFixed(1)}%) · purchase value ${r.reported ? money(r.value) : 'not reported'} · ROAS ${r.roas !== null ? r.roas.toFixed(2) + 'x' : 'unavailable'}`;
    return `<div class="brow" title="${esc(tip)}"><span class="blabel">${esc(r.key)}</span><span class="btrack">${v !== null ? `<span class="bar-fill ${cls}" style="width:${w}%"></span>` : ''}</span><span class="bval">${v !== null ? fmtV(v) : '<span class="na">No purchases reported</span>'}</span></div>`;
  }).join('') + '</figure>';
}
function bucketNote(buckets, exact, range) {
  if (!buckets || !buckets.length) return 'No breakdown rows for these dates.';
  const span = `${dateLabel(buckets[0][0])} to ${dateLabel(buckets[buckets.length - 1][1])}`;
  return exact ? `Covers ${span}, the same dates as above.` : `Breakdowns are stored by calendar month, so these charts cover ${span} (every month that overlaps the dates above).`;
}
function demoBlock(demos, note) {
  const age = aggregate(demos, 'age'), gender = aggregate(demos, 'gender');
  const total = age.reduce((s, r) => s + r.spend, 0);
  if (!age.length) return `<p class="muted small">No age or gender rows for these ads.</p>`;
  const block = (name, rows) => `<div><h3>By ${name}</h3><div class="demo-pair">${barChart('Amount spent', rows, (r) => r.spend, (v) => `${money(v)} · ${(v / total * 100).toFixed(0)}%`, 'spend', total)}${barChart('Purchase ROAS', rows, (r) => r.roas, (v) => v.toFixed(2) + 'x', 'roas', total)}</div></div>`;
  return `<div class="demo-head"><strong>Spend and ROAS by age and gender</strong><span class="small muted">${note} ROAS = purchase value ÷ spend for that group. A separate view of the same spend, not extra results.</span></div><div class="demo-grid">${block('age', age)}${block('gender', gender)}</div>`;
}

// ---------- grid ----------
const collection = () => VIEW.collections[$('format').value] || VIEW.collections.all;
const items = () => collection().ad_ids.map((id) => VIEW.ads[id]);
function fillFilters() {
  const all = items();
  const keep = (sel, values) => {
    const prev = sel.value;
    sel.innerHTML = '<option value="">All</option>' + values.map(([v, l]) => `<option value="${esc(v)}">${esc(l)}</option>`).join('');
    sel.value = values.some(([v]) => v === prev) ? prev : '';
  };
  keep($('campaign'), [...new Map(all.map((ad) => [ad.campaign_id, ad.campaign_name]))].sort((a, b) => String(a[1]).localeCompare(String(b[1]))));
  keep($('adStatus'), [...new Set(all.map((ad) => ad.effective_status))].sort().map((s) => [s, statusLabel(s)]));
}
function renderGrid() {
  if (!VIEW) return;
  const col = collection(), fmtKey = $('format').value, sort = $('sort').value;
  const minSpend = parseFloat($('minSpend').value) || 0, minRoas = parseFloat($('minRoas').value) || 0;
  const camp = $('campaign').value, status = $('adStatus').value, verdict = $('verdict').value;
  let hidden = 0;
  const list = items().filter((ad) => {
    const m = ad.view.metrics;
    if ((m.spend || 0) < minSpend) return false;
    if (minRoas > 0 && m.roas === null) { hidden += 1; return false; }
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
  $('collectionLabel').textContent = `Top 30 by spend, ${scope}` + (col.size < 30 ? ` · only ${col.size} spent in these dates` : '') + ` · showing ${list.length} of ${col.size}`;
  const notes = [];
  if (sort === 'roas') notes.push('Sorted by ROAS within this top-30-by-spend set, not the account\'s top 30 by ROAS. Ads with no reported value are last.');
  if (sort === 'change') notes.push('Sorted by spend change vs the previous period. New ads come first.');
  if (hidden) notes.push(`${hidden} ads hidden by the ROAS filter because Meta reported no purchase value for them.`);
  $('sortNote').textContent = notes.join(' ');
  const t = col.totals, vc = {};
  for (const ad of items()) vc[ad.view.verdict.code] = (vc[ad.view.verdict.code] || 0) + 1;
  $('totals').innerHTML = `This set (all ${col.size} ads, filters ignored): spend ${fmt(t.spend, 'money')} · purchase value ${fmt(t.purchase_value, 'money')} · ROAS ${fmt(t.roas, 'x')} · Verdicts: ${vc.scale || 0} scale, ${vc.watch || 0} watch, ${vc.cut || 0} cut, ${vc.not_enough_data || 0} not enough data`;
  $('demo').innerHTML = demoBlock(list.map((ad) => ad.view.demographics), bucketNote(VIEW.demographics_buckets, VIEW.demographics_exact, VIEW.range) + ` Follows the format and filters: ${list.length} ads shown below.`);
  $('grid').innerHTML = list.map(card).join('');
  $('empty').hidden = list.length > 0;
  CURRENT_LIST = list;
  document.querySelectorAll('.more').forEach((b) => b.addEventListener('click', () => openSide(b.dataset.id)));
}
let CURRENT_LIST = [];
function exportGridCsv() {
  const head = ['Rank by spend', 'Ad ID', 'Ad name', 'Campaign', 'Ad set', 'Format', 'Angle', 'Product', 'Hook', 'Status', 'Verdict', 'Fatigue',
    'Spend', 'Purchases', 'Purchase value', 'ROAS', 'CPA', 'Impressions', 'Link clicks', 'Link CTR %', 'Prev spend', 'Prev ROAS', 'Hook rate %', 'Hold rate %', 'Notes'];
  const [a, b] = ENGINE.resolveRange(VIEW.range.since, VIEW.range.until);
  const rows = CURRENT_LIST.map((ad) => {
    const v = ad.view, m = v.metrics, p = v.prev_metrics, vid = ENGINE.videoSums(ad.id, a, b), t = ad.tags || {};
    return [v.rank_by_spend, ad.id, ad.name, ad.campaign_name, ad.adset_name, ad.creative.type_label, t.angle && t.angle.label, t.product && t.product.label, t.hook && t.hook.label,
      statusLabel(ad.effective_status), v.verdict.label, v.fatigue.label, r2(m.spend), m.purchases, r2(m.purchase_value), r2(m.roas), r2(m.cpa), m.impressions, m.link_clicks, r2(m.link_ctr),
      p ? r2(p.spend) : null, p ? r2(p.roas) : null, vid ? r2(vid.hook_rate) : null, vid ? r2(vid.hold_rate) : null, (NOTES[ad.id] || []).map((x) => x.text).join(' | ')];
  });
  downloadFile(`Gehna ads ${fileStamp()}.csv`, csv([head, ...rows])).then((m) => { $('sortNote').textContent = m; });
}

// ---------- compare ----------
function toggleCompare(id, on) {
  if (on && !state.compare.includes(id)) {
    if (state.compare.length >= 4) { $('sortNote').textContent = 'Compare holds up to 4 ads. Untick one first.'; renderGrid(); return; }
    state.compare.push(id);
  }
  if (!on) state.compare = state.compare.filter((x) => x !== id);
  renderTray();
}
function renderTray() {
  const n = state.compare.length;
  $('tray').hidden = n === 0 || state.tab !== 'gallery';
  $('trayText').textContent = n === 1 ? '1 ad picked. Pick 1 to 3 more to compare.' : `${n} ads picked.`;
  $('compareOpen').disabled = n < 2;
}
function openCompare() {
  const ids = state.compare.filter((id) => ENGINE.c.ads[id]);
  const [a, b] = ENGINE.resolveRange(VIEW.range.since, VIEW.range.until);
  const tg = { roas: VIEW.targets.roas, cpa: VIEW.targets.cpa };
  const cols = ids.map((id) => {
    const ad = ENGINE.adDetail(id, state.since, state.until, tg);
    return { id, ad, det: ad.detail, vid: ENGINE.videoSums(id, a, b), life: ENGINE.lifecycle(id, (VIEW.targets.cpa || 5000) / 2) };
  });
  const best = (get, high = true) => { const vals = cols.map(get).filter((x) => x !== null && x !== undefined); if (vals.length < 2) return null; return high ? Math.max(...vals) : Math.min(...vals); };
  const row = (label, get, kind, high) => {
    const top = high === undefined ? null : best(get, high);
    return `<tr><th scope="row">${esc(label)}</th>${cols.map((c) => { const v = get(c); return `<td class="n${top !== null && v === top ? ' best' : ''}">${fmt(v, kind)}</td>`; }).join('')}</tr>`;
  };
  const sum = (s, k) => s.reduce((t, d) => t + (d[k] || 0), 0);
  const roasLine = (c) => rolling(c.det.daily, (s) => { const sp = sum(s, 'spend'); return sp > 0 && s.some((d) => d.purchase_value !== null) ? sum(s, 'purchase_value') / sp : null; });
  $('sideTitle').textContent = `Compare ${cols.length} ads`;
  $('side').classList.add('wide');
  $('sideBody').innerHTML = `<p class="small muted">${esc(dateLabel(VIEW.range.since))} to ${esc(dateLabel(VIEW.range.until))}. The best value in each row is marked. Hook and hold rates are left blank for ads that were mostly shown as an image.</p>
    <div class="scroll"><table class="cmp"><tr><th></th>${cols.map((c) => `<th><div class="cmp-thumb">${thumbHtml(c.id, c.ad.name)}</div><div class="name">${esc(c.ad.name)}</div><div class="small muted">${esc(c.ad.creative.type_label)} · ${esc(c.ad.campaign_name)}</div></th>`).join('')}</tr>
      <tr><th scope="row">Verdict</th>${cols.map((c) => `<td>${verdictChip(c.det.verdict)}</td>`).join('')}</tr>
      <tr><th scope="row">Theme</th>${cols.map((c) => `<td class="small">${c.ad.tags ? esc(c.ad.tags.angle.label + ' · ' + c.ad.tags.product.label) : ''}</td>`).join('')}</tr>
      ${row('Spend', (c) => c.det.metrics.spend, 'money')}
      ${row('Purchase value', (c) => c.det.metrics.purchase_value, 'money', true)}
      ${row('ROAS', (c) => c.det.metrics.roas, 'x', true)}
      ${row('Purchases', (c) => c.det.metrics.purchases, 'int', true)}
      ${row('CPA', (c) => c.det.metrics.cpa, 'money', false)}
      ${row('Link CTR', (c) => c.det.metrics.link_ctr, 'pct', true)}
      ${row('Link CPC', (c) => c.det.metrics.link_cpc, 'money2', false)}
      ${row('Hook rate', (c) => (c.vid && !(c.vid.video_share < 20) ? c.vid.hook_rate : null), 'pct', true)}
      ${row('Hold rate', (c) => (c.vid && !(c.vid.video_share < 20) ? c.vid.hold_rate : null), 'pct', true)}
      ${row('Days live (year)', (c) => (c.life ? c.life.days_live : null), 'int')}
      ${row('Days to peak ROAS', (c) => (c.life ? c.life.days_to_peak : null), 'int')}
      <tr><th scope="row">Fatigue</th>${cols.map((c) => `<td class="small">${esc(c.det.fatigue.label)}</td>`).join('')}</tr>
    </table></div>
    <section><h3>Purchase ROAS, rolling 7 days</h3>${cols.map((c) => sparkChart(roasLine(c), { color: 'var(--roas)', fmtY: (x) => x.toFixed(2) + 'x', title: c.ad.name })).join('')}</section>`;
  showSide();
}
function showSide() {
  $('side').classList.add('open');
  $('side').setAttribute('aria-hidden', 'false');
  $('scrim').hidden = false;
  $('close').focus();
}

// ---------- notes ----------
function notesHtml(id) {
  const list = NOTES[id] || [];
  let who = '';
  try { who = localStorage.getItem('gallery-note-name') || ''; } catch (e) { /* storage unavailable */ }
  return `<section><h3>Team notes (${list.length})</h3>
    ${list.length ? `<ul class="notes">${list.map((n) => `<li><div>${esc(n.text)}</div><div class="small muted">${esc(n.by || 'Someone')} · ${esc(n.date)}</div></li>`).join('')}</ul>` : '<p class="small muted">No notes yet.</p>'}
    <form id="noteForm" class="note-form" data-id="${esc(id)}">
      <label class="field">Note <textarea id="noteText" rows="2" maxlength="500" required placeholder="e.g. Tested a new hook on 12 Sep"></textarea></label>
      <div class="row"><label class="field">Your name <input id="noteBy" type="text" maxlength="40" value="${esc(who)}"></label><button class="btn ghost" type="submit">Add note</button></div>
      <p id="noteMsg" class="small muted"></p>
    </form></section>`;
}
async function addNote(form) {
  const id = form.dataset.id, text = $('noteText').value.trim().slice(0, 500), by = $('noteBy').value.trim().slice(0, 40);
  if (!text) return;
  try { localStorage.setItem('gallery-note-name', by); } catch (e) { /* storage unavailable */ }
  const next = JSON.parse(JSON.stringify(NOTES));
  (next[id] || (next[id] = [])).push({ text, by, date: new Date().toISOString().slice(0, 10) });
  NOTES = next;
  const r = await saveFile('notes.json', next);
  openSide(id);
  $('noteMsg').textContent = r === 'saved' ? 'Note saved for the team.' : r === 'local-only' ? 'Note kept for you only. Saving for the team is off for you.' : r;
  renderGrid();
}

function card(ad) {
  const v = ad.view, m = v.metrics, c = ad.creative;
  const p = $('compare').checked ? v.prev_metrics : null;
  const chips = [verdictChip(v.verdict), fatigueChip(v.fatigue), `<span class="chip fmt">${esc(c.type_label)}</span>`, `<span class="chip ${ad.effective_status === 'ACTIVE' ? 'active' : ''}">${esc(statusLabel(ad.effective_status))}</span>`];
  const n = (v.same_media_ads || []).length;
  if (n) chips.push(`<span class="chip" title="Metrics stay per ad">Same ${c.type === 'video' ? 'video' : 'image'} in ${n} other ad${n > 1 ? 's' : ''}</span>`);
  if (!p && VIEW.previous.complete && $('compare').checked) chips.push('<span class="chip" title="No spend in the previous period">New</span>');
  if (ad.tags) chips.push(`<span class="chip tag" title="Angle, from ${esc(ad.tags.angle.why)}">${esc(ad.tags.angle.label)}</span><span class="chip tag" title="Product, from ${esc(ad.tags.product.why)}">${esc(ad.tags.product.label)}</span>`);
  const nNotes = (NOTES[ad.id] || []).length;
  if (nNotes) chips.push(`<span class="chip note-chip">${nNotes} note${nNotes > 1 ? 's' : ''}</span>`);
  const [ra, rb] = ENGINE.resolveRange(VIEW.range.since, VIEW.range.until);
  const vid = c.type === 'video' ? ENGINE.videoSums(ad.id, ra, rb) : null;
  const vline = vid ? (vid.mostly_image || (vid.video_share !== null && vid.video_share < 20) ? '<div class="small muted">Video shown in few impressions</div>'
    : `<div class="small">Hook ${fmt(vid.hook_rate, 'pct')} · Hold ${fmt(vid.hold_rate, 'pct')}</div>`) : '';
  const picked = state.compare.includes(ad.id);
  const badge = c.type === 'video' ? `<span class="play">▶ ${secs(c.video && c.video.length)}</span>` : c.type === 'carousel' ? `<span class="play">${c.cards.length} cards</span>` : '';
  const d = (cur, prev, good) => (p ? delta(cur, prev, good) : '');
  return `<article class="card"><div class="thumb"><span class="rank">#${v.rank_by_spend} by spend</span>${badge}${thumbHtml(ad.id, c.headline || ad.name)}</div>
    <div class="body"><div class="name" title="${esc(ad.name)}">${esc(ad.name)}</div><div class="chips">${chips.join('')}</div>
      <dl class="stats"><div><dt>Spend</dt><dd>${fmt(m.spend, 'money')} ${d(m.spend, p && p.spend, 0)}</dd></div><div><dt>Purchases</dt><dd>${fmt(m.purchases, 'int')}</dd></div>
      <div><dt>CPA</dt><dd>${fmt(m.cpa, 'money')} ${d(m.cpa, p && p.cpa, -1)}</dd></div><div><dt>Purchase ROAS</dt><dd>${fmt(m.roas, 'x')} ${d(m.roas, p && p.roas, 1)}</dd></div></dl>
      ${vline}
      <div class="card-actions"><label class="pickbox"><input type="checkbox" data-compare="${esc(ad.id)}"${picked ? ' checked' : ''}> Compare</label><button class="more" type="button" data-id="${esc(ad.id)}">View more</button></div></div></article>`;
}

// ---------- side panel ----------
function sparkChart(points, { kind = 'line', color = 'var(--spend)', fmtY = (v) => v.toFixed(2), title = '' } = {}) {
  const W = 520, H = 92, L = 48, R = 8, T = 8, B = 20;
  const ys = points.map((p) => p.y).filter((v) => v !== null && Number.isFinite(v));
  if (!ys.length) return `<figure class="spark"><figcaption>${esc(title)}</figcaption><p class="small muted">No data for these dates.</p></figure>`;
  const max = Math.max(...ys) || 1, n = points.length;
  const x = (i) => L + (n === 1 ? (W - L - R) / 2 : i * (W - L - R) / (n - 1));
  const y = (v) => T + (H - T - B) * (1 - v / max);
  let body = '';
  if (kind === 'bar') {
    const bw = Math.max(1, (W - L - R) / n - 1);
    body = points.map((p, i) => (p.y ? `<rect x="${(x(i) - bw / 2).toFixed(1)}" y="${y(p.y).toFixed(1)}" width="${bw.toFixed(1)}" height="${(H - B - y(p.y)).toFixed(1)}" style="fill:${color}"><title>${esc(p.x)}: ${esc(fmtY(p.y))}</title></rect>` : '')).join('');
  } else {
    let d = '', pen = false;
    points.forEach((p, i) => { if (p.y === null || !Number.isFinite(p.y)) { pen = false; return; } d += `${pen ? 'L' : 'M'}${x(i).toFixed(1)},${y(p.y).toFixed(1)}`; pen = true; });
    body = `<path d="${d}" style="fill:none;stroke:${color}" stroke-width="2" stroke-linejoin="round"/>` + points.map((p, i) => (p.y === null ? '' : `<circle cx="${x(i).toFixed(1)}" cy="${y(p.y).toFixed(1)}" r="6" style="fill:transparent"><title>${esc(p.x)}: ${esc(fmtY(p.y))}</title></circle>`)).join('');
  }
  const grid = [0, 0.5, 1].map((f) => `<line x1="${L}" x2="${W - R}" y1="${y(max * f).toFixed(1)}" y2="${y(max * f).toFixed(1)}" class="gl"/><text x="${L - 4}" y="${(y(max * f) + 3).toFixed(1)}" text-anchor="end" class="tl">${esc(fmtY(max * f))}</text>`).join('');
  const xl = `<text x="${L}" y="${H - 4}" class="tl">${esc(points[0].x)}</text><text x="${W - R}" y="${H - 4}" text-anchor="end" class="tl">${esc(points[n - 1].x)}</text>`;
  return `<figure class="spark"><figcaption>${esc(title)}</figcaption><svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(title)}">${grid}${body}${xl}</svg></figure>`;
}
function rolling(days, fn) {
  return days.map((d, i) => (d.in_range ? { x: shortDate(d.date), y: fn(days.slice(Math.max(0, i - 6), i + 1)) } : null)).filter(Boolean);
}
function breakdownTable(obj, head, total) {
  const rows = Object.entries(obj || {}).map(([k, v]) => ({ key: k, ...v })).sort((a, b) => b.spend - a.spend);
  if (!rows.length) return `<p>${NA}</p>`;
  return `<div class="scroll"><table><tr><th>${head}</th><th class="n">Spend</th><th class="n">Share</th><th class="n">Purch.</th><th class="n">Value</th><th class="n">ROAS</th></tr>` + rows.map((r) => `<tr><td>${esc(r.key.replace(/_/g, ' '))}</td><td class="n">${fmt(r.spend, 'money')}</td><td class="n">${total ? (r.spend / total * 100).toFixed(1) + '%' : ''}</td><td class="n">${fmt(r.purchases, 'int')}</td><td class="n">${fmt(r.purchase_value, 'money')}</td><td class="n">${fmt(r.roas, 'x')}</td></tr>`).join('') + '</table></div>';
}
function attribution(s) {
  const map = { '1d_view_7d_click_1d_ev': '7-day click, 1-day view, 1-day engaged view', '1d_view_7d_click': '7-day click, 1-day view', '7d_click': '7-day click', '1d_click': '1-day click', incrementality: 'Incremental attribution' };
  return s ? (map[s] || s) : 'Unavailable';
}
function openSide(id) {
  const ad = ENGINE.adDetail(id, state.since, state.until, { roas: VIEW.targets.roas, cpa: VIEW.targets.cpa });
  if (!ad) return;
  $('side').classList.remove('wide');
  const det = ad.detail, m = det.metrics, c = ad.creative, r = det.range;
  const p = $('compare').checked ? det.prev_metrics : null;
  const view = VIEW.ads[id] ? VIEW.ads[id].view : null;
  const kv = (rows) => '<table class="kv">' + rows.map(([k, v]) => `<tr><td>${esc(k)}</td><td>${v}</td></tr>`).join('') + '</table>';
  const row = (label, key, kind, good) => [label, fmt(m[key], kind) + (p ? ` ${delta(m[key], p[key], good)} <span class="small muted">prev ${fmt(p[key], kind)}</span>` : '')];
  const sum = (s, k) => s.reduce((t, d) => t + (d[k] || 0), 0);
  const roas = rolling(det.daily, (s) => { const sp = sum(s, 'spend'); return sp > 0 && s.some((d) => d.purchase_value !== null) ? sum(s, 'purchase_value') / sp : null; });
  const ctr = rolling(det.daily, (s) => { const im = sum(s, 'impressions'); return im > 0 ? sum(s, 'link_clicks') / im * 100 : null; });
  const spend = det.daily.filter((d) => d.in_range).map((d) => ({ x: shortDate(d.date), y: d.spend }));
  const f = det.fatigue, v = det.verdict;
  const bdTotal = Object.values(det.breakdowns.age || {}).reduce((s, x) => s + x.spend, 0);
  const media = c.type === 'carousel'
    ? `<section><h3>Carousel cards (${c.cards.length})</h3>${c.cards.map((k) => `<div class="cardrow"><strong>${esc(k.headline || '')}</strong>${k.description ? `<span class="small">${esc(k.description)}</span>` : ''}<span class="small">${k.link ? link(k.link) : NA}</span></div>`).join('')}</section>`
    : '';
  $('sideTitle').textContent = ad.name;
  $('sideBody').innerHTML = `
    <div>${thumbHtml(id, c.headline || ad.name)}${c.type === 'video' && c.video && c.video.url ? `<p>${link(c.video.url, 'Watch video on Facebook')} ${c.video.length ? '· ' + secs(c.video.length) : ''}</p>` : ''}<p class="small muted">Preview image. ${c.post_url ? link(c.post_url, 'Open the post') + ' for the full creative.' : ''}</p></div>
    ${media}
    ${v ? `<div class="box ${VCLASS[v.code] || ''}"><strong>${esc(v.label)}.</strong> ${esc(v.reason)}</div>` : ''}
    ${(ad.flags || []).map((x) => `<div class="box warn">${esc(x)}</div>`).join('')}
    ${window.salesSideHtml ? window.salesSideHtml(id) : ''}
    ${c.type === 'static_image' && window.labSection ? window.labSection(id) : ''}
    <section><h3>Performance, ${esc(dateLabel(r.since))} to ${esc(dateLabel(r.until))}</h3>${kv([row('Spend', 'spend', 'money2', 0), row('Purchase value', 'purchase_value', 'money2', 1), row('Purchases', 'purchases', 'int', 1), row('Purchase ROAS', 'roas', 'x', 1), row('CPA', 'cpa', 'money2', -1), row('Impressions', 'impressions', 'int', 0), row('Link CTR', 'link_ctr', 'pct', 1), row('Link CPC', 'link_cpc', 'money2', -1),
      ['Days with spend', `${m.days_active} of ${r.days}`], ['Rank by spend', view ? `#${view.rank_by_spend} of ${VIEW.totals.ads}` : 'Not in the current view']])}
      ${p ? `<p class="small muted">Previous period: ${esc(dateLabel(det.previous.since))} to ${esc(dateLabel(det.previous.until))}.</p>` : ''}</section>
    <section><h3>Trend and fatigue</h3>
      ${f ? `<div class="box ${FATIGUED.includes(f.code) ? 'warn' : ''}"><strong>${esc(f.label)}.</strong> ${esc(f.reason)}${f.recent ? `<br><span class="small">Last 7 days: link CTR ${fmt(f.recent.link_ctr, 'pct')}, ROAS ${fmt(f.recent.roas, 'x')}. The 21 days before: link CTR ${fmt(f.baseline.link_ctr, 'pct')}, ROAS ${fmt(f.baseline.roas, 'x')}.</span>` : ''}</div>` : ''}
      ${sparkChart(spend, { kind: 'bar', color: 'var(--spend)', fmtY: (x) => money(x), title: 'Daily spend' })}
      ${sparkChart(roas, { color: 'var(--roas)', fmtY: (x) => x.toFixed(2) + 'x', title: 'Purchase ROAS, rolling 7 days' })}
      ${sparkChart(ctr, { color: 'var(--spend)', fmtY: (x) => x.toFixed(2) + '%', title: 'Link CTR, rolling 7 days' })}
      <p class="small muted">A gap in the ROAS line means no purchases were reported in that 7-day span.</p></section>
    ${videoSection(id)}
    ${lifecycleSection(id)}
    ${ad.tags ? `<section><h3>Theme tags</h3>${kv([['Angle', `${esc(ad.tags.angle.label)} <span class="small muted">(from ${esc(ad.tags.angle.why)})</span>`], ['Product', `${esc(ad.tags.product.label)} <span class="small muted">(from ${esc(ad.tags.product.why)})</span>`], ['Opening line', `${esc(ad.tags.hook.label)} <span class="small muted">(${esc(ad.tags.hook.why)})</span>`]])}<p class="small muted">Tags come from the ad name, campaign name and copy. They can be wrong.</p></section>` : ''}
    ${notesHtml(id)}
    <section><h3>Creative</h3>${kv([['Format', esc(c.type_label)], ['Headline', c.headline ? esc(c.headline) : NA], ['Call to action', c.cta ? esc(c.cta.replace(/_/g, ' ').toLowerCase()) : NA], ['Landing page', c.link_url ? link(c.link_url) : c.type === 'carousel' ? 'Per card, see above' : NA], ...(c.product_set_id ? [['Product set ID', esc(c.product_set_id)]] : [])])}
      <h3 style="margin-top: 10px">Primary text</h3><div class="copy">${c.primary_text ? esc(c.primary_text) : NA}</div></section>
    <section><h3>Structure</h3>${kv([['Campaign', esc(ad.campaign_name)], ['Ad set', esc(ad.adset_name)], ['Ad ID', esc(ad.id)], ['Delivery status', esc(statusLabel(ad.effective_status))], ['Attribution', esc(attribution(ad.attribution_setting))]])}</section>
    <section><h3>Breakdowns</h3><p class="small muted">${esc(bucketNote(det.breakdown_buckets, false, r))} Each table splits the same spend. Do not add them together.</p>
      <h3>Age</h3>${breakdownTable(det.breakdowns.age, 'Age', bdTotal)}<h3 style="margin-top: 10px">Gender</h3>${breakdownTable(det.breakdowns.gender, 'Gender', bdTotal)}<h3 style="margin-top: 10px">Platform</h3>${breakdownTable(det.breakdowns.publisher_platform, 'Platform', bdTotal)}</section>`;
  showSide();
  if (c.type === 'static_image' && window.initLab) window.initLab(id);
}
function videoSection(id) {
  const [a, b] = ENGINE.resolveRange(VIEW.range.since, VIEW.range.until);
  const v = ENGINE.videoSums(id, a, b);
  if (!v || v.spend <= 0) return '';
  const bar = (label, val) => `<div class="brow"><span class="blabel">${esc(label)}</span><span class="btrack">${val !== null ? `<span class="bar-fill spend" style="width:${Math.min(100, Math.max(1, val))}%"></span>` : ''}</span><span class="bval">${fmt(val, 'pct')}</span></div>`;
  return `<section><h3>Video</h3>
    ${v.video_share !== null && v.video_share < 20 ? `<div class="box warn">The video played in only ${fmt(v.video_share, 'pct')} of impressions. Meta mostly showed a still image, so these video numbers describe a small slice of the ad.</div>` : ''}
    <table class="kv"><tr><td>Hook rate (3-second plays ÷ impressions)</td><td>${fmt(v.hook_rate, 'pct')}</td></tr><tr><td>Hold rate (ThruPlays ÷ 3-second plays)</td><td>${fmt(v.hold_rate, 'pct')}</td></tr>
      <tr><td>Average watch time</td><td>${v.avg_watch !== null ? v.avg_watch.toFixed(1) + 's' : NA}</td></tr><tr><td>Video plays</td><td>${fmt(v.starts, 'int')}</td></tr></table>
    <figure class="mini" style="margin-top: 8px"><figcaption>Share of plays that reached each point</figcaption>${bar('25%', v.p25)}${bar('50%', v.p50)}${bar('75%', v.p75)}${bar('100%', v.p100)}</figure>
    <p class="small muted">3-second plays are worked out from Meta's cost per 3-second play, which Meta rounds, so the hook rate is close but not exact.</p></section>`;
}
function lifecycleSection(id) {
  const lc = ENGINE.lifecycle(id, (VIEW.targets.cpa || 5000) / 2);
  if (!lc) return '';
  return `<section><h3>Lifecycle (whole year)</h3><table class="kv">
    <tr><td>First and last spend</td><td>${esc(dateLabel(lc.first_day))} to ${esc(dateLabel(lc.last_day))}${lc.still_running ? ' (still running)' : ''}</td></tr>
    <tr><td>Days with spend</td><td>${lc.days_live}</td></tr>
    <tr><td>Peak 7-day ROAS</td><td>${lc.peak_roas !== null ? `${lc.peak_roas.toFixed(2)}x on ${esc(dateLabel(lc.peak_day))}, ${lc.days_to_peak} days after launch` : '<span class="na">Never spent enough in a week to judge</span>'}</td></tr>
    <tr><td>Fatigue</td><td>${lc.fatigue_day ? `7-day ROAS fell below half the peak on ${esc(dateLabel(lc.fatigue_day))}, ${lc.days_to_fatigue} days after launch` : 'Did not fall below half the peak'}</td></tr>
    <tr><td>Lifetime spend and ROAS</td><td>${fmt(lc.lifetime.spend, 'money')} · ${fmt(lc.lifetime.roas, 'x')}</td></tr></table>
    <p class="small muted">A week counts when it spent at least ${money(lc.min_spend_7d)} (half the account CPA for the year).</p></section>`;
}
function closeSide() { $('side').classList.remove('open', 'wide'); $('side').setAttribute('aria-hidden', 'true'); $('scrim').hidden = true; }

// ---------- client report ----------
function reportHtml(forFile) {
  const v = VIEW, t = v.totals, r = v.range, tg = v.targets, pv = v.previous, compare = $('compare').checked;
  const agency = $('agency').value.trim(), client = $('client').value.trim() || DATA.meta.account_name || 'Meta ads', note = $('note').value.trim();
  const top = v.collections.all.ad_ids.map((id) => v.ads[id]);
  const by = (code) => top.filter((a) => a.view.verdict.code === code);
  const tired = top.filter((a) => FATIGUED.includes(a.view.fatigue.code));
  const li = (a) => `<li>${esc(a.name)} <span class="muted">(${esc(a.creative.type_label)}, ${money(a.view.metrics.spend)}, ROAS ${a.view.metrics.roas !== null ? a.view.metrics.roas.toFixed(2) + 'x' : 'unavailable'})</span></li>`;
  const x = v.exclusions;
  const tile = (a) => {
    const m = a.view.metrics, p = compare ? a.view.prev_metrics : null;
    return `<div class="r-ad"><div class="thumb"><span class="rank">#${a.view.rank_by_spend}</span>${thumbHtml(a.id, a.name).replace(' loading="lazy"', '')}</div><div class="body"><div class="name" title="${esc(a.name)}">${esc(a.name)}</div><div class="chips">${verdictChip(a.view.verdict)}${fatigueChip(a.view.fatigue)}<span class="chip fmt">${esc(a.creative.type_label)}</span></div><div>Spend ${fmt(m.spend, 'money')} ${p ? delta(m.spend, p.spend, 0) : ''}</div><div>ROAS ${fmt(m.roas, 'x')} ${p ? delta(m.roas, p.roas, 1) : ''} · CPA ${fmt(m.cpa, 'money')}</div><div class="muted">${esc(a.campaign_name)}</div></div></div>`;
  };
  return `<header class="r-head">${agency ? `<div class="r-agency">${esc(agency)}</div>` : ''}<div class="r-title">${esc(client)} · Meta ads report</div>
      <div class="small muted">${esc(dateLabel(r.since))} to ${esc(dateLabel(r.until))} (${r.days} days)${compare && pv.complete ? ` · compared with ${esc(dateLabel(pv.since))} to ${esc(dateLabel(pv.until))}` : ''}</div></header>
    ${note ? `<div class="r-note">${esc(note)}</div>` : ''}
    <section><h2>Results</h2><div class="kpis">${kpiSet(v, compare)}</div><p class="small muted">${t.ads} ads spent in these dates. ROAS = total purchase value ÷ total spend. ${t.ads_without_reported_value} ads had no reported purchase value; their spend still counts.</p></section>
    <section><h2>By format</h2><div class="scroll">${formatTable(v)}</div></section>
    <section class="panel-box">${demoBlock([v.demographics_all], bucketNote(v.demographics_buckets, v.demographics_exact, r) + ' Covers every ad in the report.')}</section>
    <section><h2>What kind of ad worked</h2><div class="scroll">${themeTable(ENGINE.themes(v).angle, 'Angle')}</div><p class="small muted">Angles are tagged from ad names and copy, so treat them as a guide.</p></section>
    <section><h2>Top 12 ads by spend</h2><div class="r-ads">${top.slice(0, 12).map(tile).join('')}</div></section>
    <section><h2>What to do next</h2><p class="small muted">Verdicts compare each ad in the top 30 by spend with the targets: ROAS ${tg.roas ? tg.roas.toFixed(2) + 'x' : 'not set'} and CPA ${tg.cpa ? money(tg.cpa) : 'not set'} (${esc(tg.roas_source)}). Scale = at or above target ROAS. Watch = within 30% below, or no purchases yet under 2x target CPA. Cut = more than 30% below, or no purchases after 2x target CPA.</p>
      <div class="r-two"><div><h3>Scale (${by('scale').length})</h3><ul class="r-list">${by('scale').slice(0, 8).map(li).join('') || '<li class="muted">None</li>'}</ul></div><div><h3>Cut (${by('cut').length})</h3><ul class="r-list">${by('cut').slice(0, 8).map(li).join('') || '<li class="muted">None</li>'}</ul></div></div>
      ${tired.length ? `<h3 style="margin-top: 12px">Signs of fatigue (${tired.length})</h3><ul class="r-list">${tired.slice(0, 8).map((a) => `<li>${esc(a.name)}: ${esc(a.view.fatigue.reason)}</li>`).join('')}</ul>` : ''}</section>
    <footer class="r-foot"><div>${x.campaigns.length ? `Left out of every figure: ${x.campaigns.length} campaign${x.campaigns.length > 1 ? 's' : ''} (${x.ads} ads, ${money(x.spend)})${x.keywords.length ? `, matched by name: ${esc(x.keywords.join(', '))}` : ''}.` : 'No campaigns excluded.'}</div>
      <div>Purchases and purchase value are Meta's reported figures under each ad set's attribution setting. "Unavailable" means Meta reported none; it is not counted as zero.</div>
      <div>Source: ${esc(sourceLabel())}, captured ${esc(new Date(DATA.meta.captured_at).toLocaleString('en-IN'))}.${forFile ? '' : ' Read-only; nothing in the ad account was changed.'}</div></footer>`;
}
function renderReport() { if (VIEW) $('report').innerHTML = reportHtml(false); }

function themeTable(rows, head) {
  const total = rows.reduce((s, r) => s + r.spend, 0);
  return `<table><tr><th>${esc(head)}</th><th class="n">Ads</th><th class="n">Spend</th><th class="n">Share</th><th class="n">Purchase value</th><th class="n">ROAS</th><th class="n">CPA</th><th>Biggest ad</th></tr>` +
    rows.map((r) => `<tr><td>${esc(r.label)}</td><td class="n">${r.ads}</td><td class="n">${fmt(r.spend, 'money')}</td><td class="n">${total ? (r.spend / total * 100).toFixed(1) + '%' : ''}</td><td class="n">${fmt(r.purchase_value, 'money')}</td><td class="n">${fmt(r.roas, 'x')}</td><td class="n">${fmt(r.cpa, 'money')}</td><td class="small">${r.top ? esc(r.top.name) : ''}</td></tr>`).join('') + '</table>';
}
async function downloadReport() {
  const css = document.querySelector('style').textContent;
  const client = $('client').value.trim() || DATA.meta.account_name || 'Meta ads';
  const doc = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>${esc(client)} Meta ads report ${VIEW.range.since} to ${VIEW.range.until}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700&family=Instrument+Sans:wght@400;500;600;700&display=swap">
<style>${css}
body { padding: 24px 16px; } @page { size: A4; margin: 12mm; } @media print { body { padding: 0; background: #fff; } .report { border: 0; padding: 0; } .r-ad, .kpi, .panel-box { break-inside: avoid; } * { -webkit-print-color-adjust: exact; print-color-adjust: exact; } }</style></head>
<body><article class="report">${reportHtml(true)}</article></body></html>`;
  const msg = await downloadFile(`${client.replace(/[^\w -]+/g, '').trim() || 'report'} Meta ads ${VIEW.range.since} to ${VIEW.range.until}.html`, doc);
  $('dlMsg').textContent = msg.startsWith('Saved') ? msg + ' Open the file in a browser and use Print, Save as PDF to make a PDF.' : msg;
}

boot();
