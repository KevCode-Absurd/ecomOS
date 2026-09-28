/* Brand brain, round 1 top section (depth contract). Reads /api/05-brand-brain/master, profile, documents,
   overview, records and audit. Writes only through the api: a profile edit (approved founder record), a
   document in, a founder answer, accept or ignore on a proposed record, and decisions on the master list. */
(function () {
  'use strict';
  const { el, mount, fmt } = UI;
  const BASE = '/api/05-brand-brain/';
  // the brand comes from the url (?brand=<slug>); every call to this screen's api and to the shared api carries it
  const BRAND = (new URLSearchParams(location.search).get('brand') || '').replace(/[^a-z0-9_-]/g, '');
  const withBrand = (url) => (BRAND && url.startsWith('/api/') ? url + (url.includes('?') ? '&' : '?') + 'brand=' + encodeURIComponent(BRAND) : url);
  const api = (url, opts) => UI.api(withBrand(url), opts);
  const SCREEN = '05-brand-brain';
  const NA = 'unavailable';
  const pretty = (s) => String(s || '').replace(/_/g, ' ');
  const TIER_TONE = { approved: 'good', site_backed: 'accent', forbidden: 'bad', unverified: 'warn', inferred: 'warn', evidence: '', reported: '' };

  function tierChip(t) { return el('span', { class: 'chip ' + (TIER_TONE[t] || ''), text: pretty(t) }); }

  function sourceLink(src) {
    if (!src) return el('span', { text: 'no source' });
    if (src.link) return el('a', { href: src.link, target: '_blank', rel: 'noopener', text: pretty(src.type) + ': ' + src.link.replace(/^https?:\/\//, '') });
    return el('span', { text: pretty(src.type) + (src.ref ? ': ' + src.ref : '') });
  }

  // ---------- 1. the plan: master list ----------
  function orient(m, prof) {
    const c = m.counts || {};
    return [
      { label: 'to approve', value: (m.top || []).length, unit: 'n', title: 'open actions in the top 10' },
      { label: 'open across screens', value: c.open, unit: 'n' },
      { label: 'need a connector', value: c.unavailable, unit: 'n', tone: c.unavailable ? 'bad' : null },
      { label: 'stake known', value: m.stake_usd, unit: '$', title: 'sum of money at stake where a formula exists' },
      { label: 'profile approved', value: prof ? prof.approved_share : null, unit: '%' },
      { label: 'brain', value: null, unit: 'n', unavailable_label: (m.brain_version || '').slice(0, 7) || NA, title: 'brain version' },
    ];
  }
  async function loadPlan(prof) {
    let m;
    try { m = await api(BASE + 'master'); } catch (e) { mount('#plan', el('p', { class: 'muted', text: 'Master list unavailable: ' + e.message })); return; }
    const win = m.window || {};
    const decided = (a) => a.decision && (a.decision.choice === 'agent' || a.decision.choice === 'person');
    const inProgress = (m.actions || []).filter((a) => a.status !== 'unavailable' && decided(a));
    const toApprove = (m.actions || []).filter((a) => a.status !== 'unavailable' && !decided(a)).slice(0, 10);
    m.top = toApprove;
    mount('#plan', UI.planBoard({
      title: 'The plan: top 10 to approve', sub: win.days + ' days to ' + fmt.date(win.ends_on) + ', ' + (m.screens || []).length + ' screens ranked' + (inProgress.length ? ', ' + inProgress.length + ' in progress' : ''),
      orient: orient(m, prof), actions: toApprove, limit: 10, screen: SCREEN, showScreen: true, onDecision: () => loadPlan(prof),
      tools: [el('button', { class: 'btn sm', type: 'button', text: 'Export CSV', onclick: () => UI.csv((m.actions || []).map((a) => ({ rank: (m.actions || []).indexOf(a) + 1, screen: a.screen, title: a.title, owner: a.owner, severity: a.severity, status: a.status, total: a.rubric && a.rubric.total, stake_usd: a.money_at_stake && a.money_at_stake.usd, why: a.why })), null, 'master-list.csv') })],
      foot: el('div', { class: 'row', style: { gap: '14px' } }, UI.rubricLegend(), el('span', { class: 'micro faint', text: 'Ranking: critical first by stake, then rubric total, severity, stake, days open. Approvals log to the decisions table; "Not now" snoozes 14 days.' })),
      empty: 'No open action across the 28 audits for this window.',
    }));
    const pw = document.getElementById('progress-wrap');
    if (inProgress.length) {
      pw.hidden = false;
      mount('#progress', el('div', { class: 'sec-head' }, el('h2', { text: 'In progress: ' + inProgress.length + ' approved' }), el('span', { class: 'sub', text: 'Approved on this screen. Agent items run when the agent layer is live; person items wait on the person named. Each shows its decision and date.' })),
        el('div', { class: 'grid' }, ...inProgress.slice(0, 10).map((a) => UI.actionCard(a, { compact: true, screen: SCREEN, showScreen: true, onDecision: () => loadPlan(prof) }))));
    } else pw.hidden = true;
    loadDecisions(m);
    loadChanges();
    loadReport();
    loadUnlocks();
    loadLadderProof(m.actions || []);
    loadSelfAudit(m.actions || []);
    loadPeaks(m.actions || []);
    loadVisual(m.actions || []);
    const con = m.connect || [];
    const cw = document.getElementById('connect-wrap');
    if (con.length) {
      cw.hidden = false;
      const list = el('div', { class: 'grid', hidden: true });
      const btn = el('button', { class: 'btn sm', type: 'button', text: 'Show ' + Math.min(con.length, 10) });
      btn.addEventListener('click', () => { list.hidden = !list.hidden; btn.textContent = list.hidden ? 'Show ' + Math.min(con.length, 10) : 'Hide'; if (!list.hidden && !list.children.length) mount(list, ...con.slice(0, 10).map((a) => UI.actionCard(a, { compact: true, screen: SCREEN, showScreen: true }))); });
      mount('#connect', el('div', { class: 'card flat connect' },
        el('div', { class: 'sec-head' }, el('h2', { text: 'Connect first: ' + (m.counts ? m.counts.unavailable : con.length) + ' rules wait on a source' }), el('div', { class: 'tools' }, btn),
          el('span', { class: 'sub', text: 'Each is a person task in Setup, read-only keys only. They never crowd out work that can start today.' })), list));
    } else cw.hidden = true;
    mount('#bottlenecks', UI.verdictTable({
      columns: [{ key: 'screen', label: 'Screen' }, { key: 'open', label: 'Open', unit: 'n' }, { key: 'unavailable', label: 'Need connector', unit: 'n' }, { key: 'critical', label: 'Critical', unit: 'n' }, { key: 'stake_usd', label: 'Stake', unit: '$' }, { key: 'score', label: 'Score', unit: 'n' }],
      rows: (m.bottlenecks || []).map((b) => Object.assign({}, b, { top_title: b.top ? b.top.title : '', top_owner: b.top ? b.top.owner : '' })),
      verdict: { at: 1, kind: (r) => r.critical ? 'stop' : r.open >= 8 ? 'fix' : r.open ? 'watch' : (r.unavailable ? 'wait' : 'keep'), text: (r) => r.critical ? 'Critical' : r.open >= 8 ? 'Busy' : r.open ? 'Open' : (r.unavailable ? 'Connect' : 'Clear'), reason: (r) => r.open + ' open, ' + r.unavailable + ' waiting on a source' },
      reason: { key: 'top_title', label: 'Top action', text: (r) => r.top_title ? r.top_title + (r.top_owner ? ' (' + pretty(r.top_owner) + ')' : '') : 'nothing open' },
      actions: { label: 'Open', onClick: (r) => { if (window.parent && window.parent !== window) window.parent.location.hash = '#/' + r.screen; else window.open('/screens/' + r.screen + '/', '_blank'); } },
      sort: { key: 'score', dir: 'desc' }, maxRows: 28,
    }));
  }

  // ---------- 0. ask the brain ----------
  function mountAsk() {
    const input = el('input', { class: 'text', placeholder: 'Ask the brain: what is our returns window? can we say the socks last a year? who is our 3PL?', 'aria-label': 'Ask the brain', style: { flex: '1 1 420px' } });
    const btn = el('button', { class: 'btn primary sm', type: 'button', text: 'Ask' });
    const out = el('div', { class: 'stack ask-out' });
    const run = async () => {
      const q = input.value.trim(); if (!q) return;
      btn.disabled = true;
      try {
        const r = await api(BASE + 'ask?q=' + encodeURIComponent(q));
        const items = [];
        if (r.can_we_say) items.push(el('div', { class: 'card ' + (r.can_we_say.verdict === 'yes' ? 'flat' : 'sunken') }, UI.verdict(r.can_we_say.verdict === 'yes' ? 'keep' : r.can_we_say.verdict === 'never' ? 'stop' : 'watch', pretty(r.can_we_say.verdict), ''), ' ', r.can_we_say.text, r.can_we_say.record ? el('span', { class: 'chip mono', text: r.can_we_say.record }) : null));
        if (r.answers.length) items.push(UI.table({ columns: [{ key: 'text', label: 'Answer' }, { key: 'tier', label: 'Tier', format: pretty }, { key: 'date', label: 'Date', format: (v) => v ? fmt.date(v) : 'undated' }, { key: 'src', label: 'Source', format: (v, row) => row.source.link ? row.source.link.replace(/^https?:\/\//, '').slice(0, 50) : (row.source.type || 'none') }, { key: 'id', label: 'Record' }], rows: r.answers, sort: false, onRow: (row) => { if (row.source.link) window.open(row.source.link, '_blank', 'noopener'); } }));
        else items.push(el('p', { class: 'muted small', text: 'Nothing on file matches.' }));
        const save = el('button', { class: 'btn sm', type: 'button', text: 'Save as an open question' });
        const st = el('span', { class: 'micro muted' });
        save.addEventListener('click', async () => { save.disabled = true; try { const res = await api(BASE + 'ask/open', { method: 'POST', body: { q } }); st.textContent = 'Saved ' + res.record + '. It shows under what the system needs from you.'; loadQuestions(); } catch (e) { save.disabled = false; st.textContent = 'Could not save: ' + e.message; } });
        items.push(el('div', { class: 'row' }, el('span', { class: 'micro faint', text: r.count + ' records match. ' + (r.note || '') }), save, st));
        mount(out, ...items);
      } catch (e) { mount(out, el('p', { class: 'muted', text: 'Could not ask: ' + e.message })); }
      btn.disabled = false;
    };
    btn.addEventListener('click', run);
    input.addEventListener('keydown', (e) => { if (e.key === 'Enter') run(); });
    mount('#ask', el('div', { class: 'card flat ask' }, el('div', { class: 'row' }, input, btn), out));
  }

  // ---------- 5e2. assumptions register ----------
  function assumptionPanel(a, byAct, reload) {
    const body = el('div', { class: 'stack' });
    body.append(el('div', { class: 'row' }, UI.verdict(a.verdict.kind, a.verdict.text, ''), el('span', { class: 'chip', text: a.unit || 'no unit' }), a.as_of ? el('span', { class: 'chip', text: 'as of ' + a.as_of }) : null, ...a.rooms.map((r) => el('span', { class: 'chip mono', text: pretty(r) }))));
    body.append(el('div', null, el('b', { text: 'Value: ' }), a.summary));
    if (a.reasoning) body.append(el('div', { class: 'small muted', text: a.reasoning }));
    if (a.source_refs.length) body.append(el('div', { class: 'small' }, el('b', { text: 'Sources: ' }), a.source_refs.map((r) => r.slice(0, 90)).join('; ')));
    body.append(el('div', { class: 'small' }, el('b', { text: 'Writes to: ' }), a.target || NA));
    const input = el('input', { class: 'text sm', placeholder: 'The real number or value', style: { flex: '1 1 200px' } });
    const status = el('span', { class: 'micro muted' });
    const go = (bodyReq) => async () => { try { const r = await api(BASE + 'assumptions/' + a.field, { method: 'POST', body: bodyReq }); status.textContent = 'Saved ' + r.record + '. Read by ' + (r.rooms || []).map(pretty).join(', ') + '.'; reload(); } catch (e) { status.textContent = 'Could not save: ' + e.message; } };
    body.append(el('div', { class: 'row' }, el('button', { class: 'btn primary sm', type: 'button', text: 'Confirm as is', onclick: go({ choice: 'confirm' }) }), input, el('button', { class: 'btn sm', type: 'button', text: 'Correct it', onclick: () => go({ value: input.value })() }), status));
    const act = byAct['assumption_' + a.field];
    if (act) body.append(UI.actionCard(act, { screen: SCREEN, expanded: false }));
    UI.panel({ title: a.label, body });
  }
  async function loadAssumptions() {
    let ar, actions = [];
    try { ar = await api(BASE + 'assumptions'); } catch (e) { mount('#assumptions', el('p', { class: 'muted', text: 'Assumptions unavailable: ' + e.message })); return; }
    try { const r = await api(BASE + 'rank'); actions = (r.actions || []).filter((a) => a.rule_id === 'BRN-R21'); } catch (e) { actions = []; }
    const byAct = {}; for (const a of actions) if (a.entity && a.entity.id) byAct[a.entity.id] = a;
    mount('#assumptions-tools', UI.orientation([{ label: 'yours', value: ar.counts.founder, unit: 'n', tone: 'good' }, { label: 'sourced', value: ar.counts.sourced, unit: 'n' }, { label: 'modelled', value: ar.counts.modelled, unit: 'n', tone: ar.counts.modelled ? 'bad' : null }, { label: 'derived', value: ar.counts.derived, unit: 'n' }]));
    mount('#assumptions', UI.verdictTable({
      columns: [{ key: 'label', label: 'Assumption' }, { key: 'summary', label: 'Value' }, { key: 'unit', label: 'Unit', format: (v) => v || '' }, { key: 'as_of', label: 'As of', format: (v) => v || NA }, { key: 'rooms_text', label: 'Read by' }],
      verdict: { at: 1, kind: (r) => r.verdict.kind, text: (r) => r.verdict.text, reason: (r) => r.verdict.reason },
      actions: { label: (r) => r.status === 'founder' ? 'Open' : 'Confirm or correct', onClick: (r) => assumptionPanel(r, byAct, loadAssumptions) },
      rows: ar.assumptions.map((a) => Object.assign({}, a, { rooms_text: a.rooms.slice(0, 4).map(pretty).join(', ') + (a.rooms.length > 4 ? ' +' + (a.rooms.length - 4) : '') })), sort: false, maxRows: 30,
    }), el('div', { class: 'micro faint', text: ar.note }));
  }

  // ---------- 5f. permissions and export ----------
  function permPanel(sec, pm, reload) {
    const selects = {};
    const body = el('div', { class: 'stack' }, el('div', { class: 'small muted', text: sec.records + ' records, ' + (sec.private_share == null ? 'no records' : Math.round(sec.private_share * 100) + ' percent private') + '. The founder always has full access.' }));
    for (const role of pm.roles) {
      if (role === 'founder') continue;
      const sel = el('select', { class: 'text sm' }, ...pm.levels.map((lv) => el('option', { value: lv, text: lv, selected: sec.levels[role] === lv })));
      selects[role] = sel;
      body.append(el('div', { class: 'row' }, el('span', { style: { minWidth: '160px' }, text: pretty(role) }), sel));
    }
    const status = el('span', { class: 'micro muted' });
    const go = el('button', { class: 'btn primary sm', type: 'button', text: 'Save for ' + pretty(sec.key) });
    const panel = UI.panel({ title: 'Who sees ' + pretty(sec.key), body: [body, el('div', { class: 'row' }, go, status)] });
    go.addEventListener('click', async () => { go.disabled = true; const roles = {}; for (const [r, s] of Object.entries(selects)) roles[r] = s.value; try { await api(BASE + 'permissions/' + sec.key, { method: 'POST', body: { roles } }); panel.close(); reload(); } catch (e) { go.disabled = false; status.textContent = 'Could not save: ' + e.message; } });
  }
  async function loadPermissions() {
    let pm;
    try { pm = await api(BASE + 'permissions'); } catch (e) { mount('#perm', el('p', { class: 'muted', text: 'Permissions unavailable: ' + e.message })); return; }
    const bySec = {}; for (const s of pm.sections) bySec[s.key] = s;
    mount('#perm-tools', UI.orientation([{ label: 'sections set', value: pm.counts.explicit, unit: 'n', title: 'of ' + pm.counts.sections }, { label: 'default, restricted', value: pm.counts.unset, unit: 'n' }, { label: 'coverage', value: pm.counts.coverage_pct, unit: '%' }]));
    const matrix = UI.coverageMatrix({ rows: pm.rows, cols: pm.cols, cells: pm.cells, unit: 'n', single: true, max: 2, corner: 'Section by role',
      gapRule: (cell, row, col) => (cell && cell.label === 'none' && col.key !== 'founder' && !bySec[row.key].explicit ? '' : ''), onCell: (cell, row) => permPanel(bySec[row.key], pm, loadPermissions), note: pm.note + ' Click a row to set it. 2 = full, 1 = read, 0 = none.' });
    const exp = el('button', { class: 'btn sm', type: 'button', text: 'Export the whole brain (JSON)' });
    const st = el('span', { class: 'micro muted' });
    exp.addEventListener('click', async () => { exp.disabled = true; try { const b = await api(BASE + 'export'); const blob = new Blob([JSON.stringify(b, null, 1)], { type: 'application/json' }); const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = b.brand + '-brain-' + b.exported_at + '.json'; a.click(); st.textContent = b.counts.records + ' records, ' + b.counts.documents + ' documents, ' + b.counts.conflicts + ' conflicts. ' + b.note; } catch (e) { st.textContent = 'Could not export: ' + e.message; } exp.disabled = false; });
    mount('#perm', matrix, el('div', { class: 'row', style: { marginTop: '10px' } }, exp, UI.decisionRow({ capability: 'LOOP-C22', autonomy: 'founder_gate', owner: 'agent_drafts', screen: SCREEN, compact: true, stub: 'Offboarding: export the brain and the registry as a handoff package, list every connector to revoke in Setup, and confirm no external write access stays open. You approve each revoke.' }), st));
  }

  // ---------- 5b0. does it look like us ----------
  function swatch(c) {
    return el('div', { class: 'swatch', title: c.record + ', ' + pretty(c.tier) }, el('i', { style: { background: c.hex } }), el('div', null, el('b', { text: c.name }), ' ', el('span', { class: 'micro faint', text: pretty(c.role) }), el('small', { text: c.hex })));
  }
  function foundChip(r) {
    return el('span', { class: 'chip ' + (r.on_palette ? 'good' : 'bad'), title: r.nearest ? 'nearest ' + pretty(r.nearest) + ' ' + r.nearest_hex + ', distance ' + r.distance : 'no palette' }, el('i', { style: { background: r.hex } }), r.hex + (r.share != null ? ' ' + Math.round(r.share * 100) + '%' : (r.times > 1 ? ' x' + r.times : '')) + (r.on_palette ? '' : ' (nearest ' + pretty(r.nearest || 'none') + ')'));
  }
  async function loadVisual(actions) {
    let v;
    try { v = await api(BASE + 'visual'); } catch (e) { mount('#visual', el('p', { class: 'muted', text: 'Visual unavailable: ' + e.message })); return; }
    const act = (actions || []).find((a) => a.rule_id === 'BRN-R27');
    mount('#visual-tools', UI.orientation([{ label: 'colours', value: v.counts.colours, unit: 'n' }, { label: 'fonts', value: v.counts.fonts, unit: 'n' }, { label: 'contrast pairs failing', value: v.counts.aa_fail, unit: 'n', tone: v.counts.aa_fail ? 'bad' : 'good' }, { label: 'logo rules', value: v.logo_rules.available ? 1 : null, unit: 'n', unavailable_label: 'not set' }]));
    const status = el('span', { class: 'micro muted' });
    const out = el('div', { class: 'stack' });
    // the palette
    const paletteBody = el('div', { class: 'stack' });
    if (!v.available) paletteBody.append(el('p', { class: 'muted', text: 'Palette unavailable: ' + v.reason + '.' }));
    else {
      paletteBody.append(el('div', { class: 'swatches' }, ...v.colours.map(swatch)));
      paletteBody.append(el('div', { class: 'small' }, el('b', { text: 'Fonts: ' }), v.fonts.length ? v.fonts.map((f) => f.name + ' (' + f.role + ')').join(', ') : NA));
      paletteBody.append(UI.verdictTable({ columns: [{ key: 'text', label: 'Text' }, { key: 'background', label: 'On' }, { key: 'ratio', label: 'Ratio', num: true, format: (x) => (x == null ? NA : x.toFixed(1) + ':1') }, { key: 'use', label: 'Use' }],
        verdict: { at: 1, kind: (r) => r.aa ? 'keep' : (r.aa_large ? 'watch' : 'stop'), text: (r) => r.aa ? 'AA' : (r.aa_large ? 'Large only' : 'Fails'), reason: (r) => '4.5 passes for body text, 3 for large text and accents' },
        rows: v.pairs.map((p) => ({ text: pretty(p.text.replace('color_', '')), background: pretty(p.background.replace('color_', '')), ratio: p.ratio, aa: p.aa, aa_large: p.aa_large, use: p.accent ? 'accent, large text or buttons' : 'body text' })), sort: false, empty: 'No text and background pair to check.' }));
    }
    // logo rules
    const logoBody = el('div', { class: 'stack' });
    const lr = v.logo_rules;
    if (lr.available) logoBody.append(el('div', { class: 'small' }, el('b', { text: 'On file: ' }), (lr.value.min_size_px ? 'minimum ' + lr.value.min_size_px + ' px wide. ' : '') + (lr.value.clear_space ? 'Clear space ' + lr.value.clear_space + '. ' : '') + (lr.value.never.length ? 'Never ' + lr.value.never.join('; ') + '. ' : '') + (lr.value.backgrounds.length ? 'On ' + lr.value.backgrounds.join(', ') + '.' : '')));
    else logoBody.append(el('div', { class: 'small muted', text: 'Unavailable: ' + lr.reason + '.' }));
    const minPx = el('input', { class: 'text sm', type: 'number', placeholder: 'min width px', style: { maxWidth: '130px' }, value: lr.value && lr.value.min_size_px ? lr.value.min_size_px : '' });
    const clear = el('input', { class: 'text sm', placeholder: 'clear space, like: the height of the mark on every side', style: { flex: '1 1 260px' }, value: lr.value && lr.value.clear_space ? lr.value.clear_space : '' });
    const never = el('input', { class: 'text sm', placeholder: 'never, separated by ; like: stretch it; recolour it; put it on a busy photo', style: { flex: '1 1 300px' }, value: lr.value && lr.value.never ? lr.value.never.join('; ') : '' });
    const bgs = el('input', { class: 'text sm', placeholder: 'allowed backgrounds, like: white, offwhite, black', style: { flex: '1 1 220px' }, value: lr.value && lr.value.backgrounds ? lr.value.backgrounds.join(', ') : '' });
    const save = el('button', { class: 'btn primary sm', type: 'button', text: lr.available ? 'Update the logo rules' : 'Set the logo rules' });
    save.addEventListener('click', async () => { save.disabled = true; try { const r = await api(BASE + 'visual/logo', { method: 'POST', body: { min_size_px: minPx.value, clear_space: clear.value, never: never.value, backgrounds: bgs.value } }); status.textContent = r.text; loadVisual(actions); loadPlan(); } catch (e) { save.disabled = false; status.textContent = 'Could not save: ' + e.message; } });
    logoBody.append(el('div', { class: 'row' }, minPx, clear), el('div', { class: 'row' }, never, bgs, save));
    // the checker
    const checkBody = el('div', { class: 'stack' });
    const ta = el('textarea', { class: 'text', placeholder: 'Paste CSS, HTML, an email template or a list of hex codes. Every colour and font-family is matched to the palette.' });
    const go = el('button', { class: 'btn primary sm', type: 'button', text: 'Check it' });
    function renderCheck(r) {
      const kids = [el('div', { class: 'row' }, UI.verdict(r.verdict === 'pass' ? 'keep' : r.verdict === 'warn' ? 'watch' : r.verdict === 'fail' ? 'stop' : 'na', r.verdict === 'unavailable' ? 'Unavailable' : r.verdict.toUpperCase()), el('span', { class: 'small', text: r.summary + (r.name ? ' (' + r.name + ')' : '') + (r.width ? ', ' + r.width + 'x' + r.height : '') }))];
      if (r.colours.length) kids.push(el('div', { class: 'found' }, ...r.colours.map(foundChip)));
      if (r.fonts && r.fonts.length) kids.push(el('div', { class: 'found' }, ...r.fonts.map((f) => el('span', { class: 'chip ' + (f.brand ? 'good' : 'bad'), text: f.name + (f.brand ? '' : ' (not a brand font)') }))));
      if (r.note) kids.push(el('div', { class: 'micro faint', text: r.note }));
      mount(out, ...kids);
    }
    go.addEventListener('click', async () => { if (!ta.value.trim()) return; go.disabled = true; try { renderCheck(await api(BASE + 'visual/check', { method: 'POST', body: { text: ta.value } })); } catch (e) { mount(out, el('p', { class: 'muted', text: 'Could not check: ' + e.message })); } go.disabled = false; });
    const zone = UI.dropZone({ accept: 'image/png', hint: 'A PNG of a generated creative, a banner or an email screenshot. Its dominant colours are matched to the palette. JPEG cannot be read here; export a PNG.',
      onFiles: async (files) => { for (const f of files) { mount(out, el('p', { class: 'muted small', text: 'Reading ' + f.name })); try { renderCheck(await api(BASE + 'visual/check', { method: 'POST', body: { name: f.name, content_base64: await readAsBase64(f) } })); } catch (e) { mount(out, el('p', { class: 'muted', text: 'Could not read ' + f.name + ': ' + e.message })); } } } });
    checkBody.append(ta, el('div', { class: 'row' }, go, el('span', { class: 'micro faint', text: 'Tolerance: a colour within ' + (v.available ? '40' : '40') + ' RGB units of a token counts as on the palette.' })), zone, out);
    mount('#visual', el('div', { class: 'row' }, act ? UI.decisionRow({ capability: 'CREA-C12', autonomy: 'agent_does', owner: act.owner, screen: SCREEN, compact: true, finding_id: act.id, current: act.decision, stub: act.title + '. ' + act.artefact.label + '.' }) : null, status),
      UI.tabs({ items: [{ key: 'palette', label: 'Palette and contrast', n: v.counts.colours, panel: paletteBody }, { key: 'check', label: 'Check a draft or a PNG', panel: checkBody }, { key: 'logo', label: 'Logo rules', panel: logoBody }] }),
      el('p', { class: 'micro faint', text: v.note }));
  }

  // ---------- 5b1. peak readiness ----------
  function peakPanel(p, action, reload) {
    const body = el('div', { class: 'stack' });
    body.append(el('div', { class: 'row' }, UI.verdict(p.verdict.kind, p.verdict.text), el('span', { class: 'chip', text: p.date ? fmt.date(p.date) + (p.days_to != null ? ', ' + p.days_to + ' days' : '') : (p.window || 'date unavailable') }), el('span', { class: 'chip', text: pretty(p.kind) }), el('span', { class: 'chip', text: p.surfaces })));
    body.append(el('div', { class: 'small', text: p.why }));
    if (p.derived) body.append(el('div', { class: 'small warn', text: 'Derived: ' + p.derivation + '. Confirm it below.' }));
    const checks = el('div', { class: 'checks' });
    for (const c of p.checks) {
      checks.append(el('div', { class: 'row' }, el('span', { class: 'chip ' + (c.status === 'ok' ? 'good' : c.status === 'gap' ? 'bad' : ''), text: c.status === 'ok' ? 'ok' : c.status === 'gap' ? 'decide' : 'unavailable' }), el('b', { text: c.label + ': ' }), el('span', { text: c.evidence + (c.fix ? ' ' + c.fix : '') + (c.note ? ' (' + c.note + ')' : '') }), c.who ? el('span', { class: 'micro faint', text: pretty(c.who) }) : null));
    }
    body.append(checks);
    const status = el('span', { class: 'micro muted' });
    if (p.kind !== 'event' || true) {
      const offer = el('input', { class: 'text', placeholder: p.kind === 'mission' ? 'The plan, like: match every order with a second donation, no discount' : 'The offer, like: 25 percent off sitewide, code BF25, no stacking with COMFORT20', style: { flex: '1 1 360px' } });
      const note = el('input', { class: 'text', placeholder: 'Note (optional)', style: { flex: '1 1 200px' } });
      const cutoff = p.key.indexOf('holiday_orderby') === 0 || p.key.indexOf('christmas') === 0 ? el('input', { class: 'text', type: 'date', value: p.key.indexOf('holiday_orderby') === 0 && p.date ? p.date : '', title: 'Holiday shipping cutoff' }) : null;
      const go = el('button', { class: 'btn primary sm', type: 'button', text: 'Decide it' });
      go.addEventListener('click', async () => { if (!offer.value.trim()) { status.textContent = 'Type the offer or the plan first.'; return; } go.disabled = true; try { const r = await api(BASE + 'peaks/plan', { method: 'POST', body: { peak: p.key, offer: offer.value.trim(), note: note.value.trim(), cutoff: cutoff ? cutoff.value : null } }); status.textContent = r.next + (r.warns.length ? ' Scanner warned on: ' + r.warns.join(', ') + '.' : ''); panel.close(); reload(); loadPlan(); } catch (e) { go.disabled = false; status.textContent = 'Could not save: ' + e.message; } });
      body.append(el('div', { class: 'row' }, offer, note, cutoff, go));
    }
    body.append(el('div', { class: 'row' }, status));
    if (action) body.append(UI.decisionRow({ capability: 'BRN-C07', autonomy: 'founder_gate', owner: action.owner, screen: SCREEN, compact: true, finding_id: action.id, current: action.decision, stub: action.title + '. ' + action.artefact.label + '.' }));
    const panel = UI.panel({ title: p.label + (p.date ? ', ' + fmt.date(p.date) : ''), body });
  }
  async function loadPeaks(actions) {
    let r;
    try { r = await api(BASE + 'peaks'); } catch (e) { mount('#peaks', el('p', { class: 'muted', text: 'Peaks unavailable: ' + e.message })); return; }
    const byAct = {}; for (const a of actions || []) if (a.rule_id === 'BRN-R26' && a.entity) byAct[a.entity.id] = a;
    mount('#peaks-tools', UI.orientation([{ label: 'peaks in 90 days', value: r.counts.peaks, unit: 'n' }, { label: 'ready', value: r.counts.ready, unit: 'n', tone: r.counts.ready === r.counts.peaks ? 'good' : null }, { label: 'decisions waiting', value: r.counts.gaps, unit: 'n', tone: r.counts.gaps ? 'bad' : 'good' }, { label: 'checks waiting on a source', value: r.counts.unavailable, unit: 'n' }]));
    const months = el('div', { class: 'months' });
    if (r.heavy_months.available) { months.append(el('span', { class: 'small', text: 'Seasonality index (' + pretty(r.heavy_months.status || 'modelled') + '): ' })); for (const m of r.heavy_months.months) months.append(el('span', { class: 'chip' + (m.heavy ? ' heavy warn' : ''), text: m.label + ' ' + m.index.toFixed(2) + (m.heavy ? ', heavy' : '') })); }
    else months.append(el('span', { class: 'small muted', text: 'Seasonality index unavailable: ' + r.heavy_months.reason + '.' }));
    const table = UI.verdictTable({
      columns: [{ key: 'label', label: 'Peak' }, { key: 'when', label: 'When' }, { key: 'days', label: 'Days', num: true }, { key: 'ready', label: 'Ready', num: true, unit: '%' }, { key: 'decide', label: 'To decide' }, { key: 'waiting', label: 'Waiting on a source', num: true }],
      verdict: { at: 1, kind: (x) => x.verdict.kind, text: (x) => x.verdict.text, reason: (x) => x.why },
      rows: r.peaks.map((p) => ({ key: p.key, label: p.label + (p.own ? ' (yours)' : ''), when: p.date ? fmt.date(p.date) + (p.derived ? ', derived' : '') : (p.window || NA), days: p.days_to, ready: p.readiness_pct == null ? null : p.readiness_pct / 100, decide: p.checks.filter((c) => c.status === 'gap').map((c) => c.label.toLowerCase()).join(', ') || 'nothing', waiting: p.checks.filter((c) => c.status === 'unavailable').length, verdict: p.verdict, why: p.why })),
      sort: false, empty: 'No peak in the next 90 days.', onRow: (x) => { const p = r.peaks.find((q) => q.key === x.key); if (p) peakPanel(p, byAct['peak_' + p.key], () => loadPeaks(actions)); },
      actions: { label: 'Open', onClick: (x) => { const p = r.peaks.find((q) => q.key === x.key); if (p) peakPanel(p, byAct['peak_' + p.key], () => loadPeaks(actions)); } },
    });
    mount('#peaks', months, table, el('p', { class: 'micro faint', text: r.note }));
  }

  // ---------- 5b2. the brain audits itself ----------
  async function loadSelfAudit(actions) {
    let sa;
    try { sa = await api(BASE + 'selfaudit'); } catch (e) { mount('#selfaudit', el('p', { class: 'muted', text: 'Self audit unavailable: ' + e.message })); return; }
    const c = sa.counts;
    const byAct = {}; for (const a of actions || []) if ((a.rule_id === 'BRN-R24' || a.rule_id === 'BRN-R25') && a.entity) byAct[a.entity.id] = a;
    mount('#selfaudit-tools', UI.orientation([{ label: 'lines', value: c.total, unit: 'n' }, { label: 'router rows to fix', value: sa.proposals.filter((p) => p.kind === 'drifted' || p.kind === 'broken_link').length, unit: 'n', tone: sa.router.ok ? 'good' : 'bad' }, { label: 'duplicates', value: c.duplicates, unit: 'n' }, { label: 'sections nobody reads', value: c.unread_sections, unit: 'n' }]));
    const status = el('span', { class: 'micro muted' });
    const regen = el('button', { class: 'btn sm' + (sa.router.ok ? '' : ' primary'), type: 'button', text: 'Regenerate BRAIN.md' });
    regen.addEventListener('click', async () => { regen.disabled = true; try { const r = await api(BASE + 'selfaudit/regenerate', { method: 'POST' }); status.textContent = 'Rebuilt: ' + r.drift_before + ' drifted rows before, ' + r.drift_after + ' after, ' + r.tokens + ' tokens.'; loadSelfAudit(actions); } catch (e) { regen.disabled = false; status.textContent = 'Could not regenerate: ' + e.message; } });
    const table = UI.verdictTable({
      columns: [{ key: 'kind', label: 'Check' }, { key: 'target', label: 'Where' }, { key: 'after', label: 'Fix' }, { key: 'who', label: 'Who' }],
      verdict: { at: 1, kind: (r) => ({ drifted: 'fix', broken_link: 'fix', stale: 'watch', conflict: 'fix', empty: 'new', unread: 'new' })[r.kindKey] || 'watch', text: (r) => ({ drifted: 'Drifted', broken_link: 'Broken', stale: 'Expired', conflict: 'Conflict', empty: 'Empty', unread: 'Unread' })[r.kindKey] || r.kind, reason: (r) => r.reason + '. Now: ' + r.before },
      rows: sa.proposals.map((p) => ({ kind: pretty(p.kind), kindKey: p.kind, target: p.target, before: String(p.before).slice(0, 140), after: p.after, who: pretty(p.fix.who), reason: p.reason })),
      sort: false, empty: 'Nothing past expiry, no open conflict, no empty section a room needs, no unread file, the router matches the records and every link resolves.',
    });
    const dupWrap = el('div', { class: 'stack' });
    if (sa.duplicates.length) {
      dupWrap.append(el('div', null, el('b', { text: sa.duplicates.length + ' duplicate pair' + (sa.duplicates.length === 1 ? '' : 's') + ': ' }), 'the stronger record is kept; retiring the twin keeps it in history.'));
      for (const d of sa.duplicates.slice(0, 20)) {
        const b = el('button', { class: 'btn sm', type: 'button', text: 'Retire the twin' });
        b.addEventListener('click', async () => { b.disabled = true; try { const r = await api(BASE + 'selfaudit/retire', { method: 'POST', body: { retire: d.retire, keep: d.keep } }); status.textContent = 'Retired ' + r.retired + ', kept ' + r.kept + '. ' + r.left + ' pairs left.'; loadSelfAudit(actions); } catch (e) { b.disabled = false; status.textContent = 'Could not retire: ' + e.message; } });
        dupWrap.append(el('div', { class: 'row card flat' }, el('span', { class: 'chip', text: pretty(d.section) }), el('span', { class: 'chip mono good', text: 'keep ' + d.keep + ' (' + pretty(d.keep_tier) + ')' }), el('span', { class: 'chip mono warn', text: 'retire ' + d.retire + ' (' + pretty(d.retire_tier) + ')' }), el('span', { class: 'small', text: d.match + ': ' + d.text }), b));
      }
    } else dupWrap.append(el('div', { class: 'muted small', text: 'No two active records say the same thing.' }));
    const reads = el('div', { class: 'stack' });
    if (!sa.reads.available) reads.append(el('div', { class: 'muted small', text: 'Read coverage unavailable: ' + sa.reads.reason + '.' }));
    else {
      reads.append(el('div', null, el('b', { text: sa.reads.total_reads + ' reads logged. ' }), (sa.reads.unread.length ? 'Held but never read: ' + sa.reads.unread.map((r) => pretty(r.section) + ' (' + r.records + ')').join(', ') + '. ' : 'Every section with records has been read. ') + (sa.reads.hot_thin.length ? 'Read often and thin: ' + sa.reads.hot_thin.map((r) => pretty(r.section) + ' (' + r.reads + ' reads, ' + r.records + ' records)').join(', ') + '. A pull there pays.' : '')));
      reads.append(UI.verdictTable({ columns: [{ key: 'section', label: 'Section' }, { key: 'records', label: 'Records', num: true }, { key: 'reads', label: 'Reads', num: true }, { key: 'readers', label: 'Readers' }, { key: 'last_read', label: 'Last read' }],
        rows: sa.reads.sections.filter((r) => r.reads || r.records).map((r) => ({ section: pretty(r.section), records: r.records, reads: r.reads, readers: r.readers.join(', ') || NA, last_read: r.last_read ? fmt.date(r.last_read.slice(0, 10)) : NA })), sort: false, empty: 'No section has records or reads.' }));
    }
    const files = sa.missing_files.length ? el('div', { class: 'warn small' }, el('b', { text: 'Files missing on disk: ' }), sa.missing_files.map((f) => f.file).join(', ') + '. Put the file back under documents/, or remove the manifest row.') : null;
    const act = byAct.router || byAct.duplicates;
    mount('#selfaudit', el('div', { class: 'row' }, regen, act ? UI.decisionRow({ capability: 'BRN-C12', autonomy: 'agent_does', owner: 'agent', screen: SCREEN, compact: true, finding_id: act.id, current: act.decision, stub: act.title + '. ' + act.artefact.label + '.' }) : null, status),
      UI.tabs({ items: [{ key: 'checks', label: 'Checks', n: sa.proposals.length, panel: table }, { key: 'dups', label: 'Duplicates', n: sa.duplicates.length, panel: dupWrap }, { key: 'reads', label: 'Read coverage', n: sa.reads.available ? sa.reads.total_reads : null, panel: reads }] }),
      files, el('p', { class: 'micro faint', text: sa.note }));
  }

  // ---------- 5c3b. ladder proof matrix: rungs by surface ----------
  function proofPanel(g, action, reload) {
    const body = el('div', { class: 'stack' });
    body.append(el('div', { class: 'row' }, el('span', { class: 'chip bad', text: g.status === 'forbidden' ? 'proof is forbidden' : 'no proof on file' }),
      el('span', { class: 'chip', text: (g.one_star == null ? NA : g.one_star) + ' one-star' }), ...g.uses.map((u) => el('span', { class: 'chip', text: pretty(u) }))));
    if (g.lost_ids && g.lost_ids.length) body.append(el('div', { class: 'small warn', text: 'Proof ids the brain no longer holds: ' + g.lost_ids.join(', ') }));
    body.append(el('pre', { class: 'card sunken brief', text: g.brief }));
    const status = el('span', { class: 'micro muted' });
    const cand = el('div', { class: 'cand' });
    if (g.candidates.length) {
      cand.append(el('div', { class: 'small' }, el('b', { text: 'On file already, ranked by overlap with the doubt:' })));
      for (const c of g.candidates) {
        const use = el('button', { class: 'btn sm' + (c.usable ? ' primary' : ''), type: 'button', text: c.usable ? 'Use as proof' : 'Attach (needs approval)' });
        use.addEventListener('click', async () => { use.disabled = true; try { const r = await api(BASE + 'ladders/proof', { method: 'POST', body: { theme: g.theme, level: g.level, record_id: c.id } }); status.textContent = r.next; panel.close(); reload(); } catch (e) { use.disabled = false; status.textContent = 'Could not attach: ' + e.message; } });
        cand.append(el('div', { class: 'row' }, el('span', { class: 'chip mono', text: c.id }), el('span', { class: 'chip ' + (c.usable ? 'good' : 'warn'), text: pretty(c.tier) }), el('span', { class: 'small', text: c.text }), use));
      }
    } else cand.append(el('div', { class: 'small muted', text: 'Nothing on file names this doubt. The brief asks the agent to draft the fact; you approve it in the review queue.' }));
    body.append(cand);
    const other = el('input', { class: 'text', placeholder: 'or type a record id, like bombas.policies.happiness_guarantee' });
    const go = el('button', { class: 'btn sm', type: 'button', text: 'Attach this id' });
    go.addEventListener('click', async () => { if (!other.value.trim()) return; go.disabled = true; try { const r = await api(BASE + 'ladders/proof', { method: 'POST', body: { theme: g.theme, level: g.level, record_id: other.value.trim() } }); status.textContent = r.next; panel.close(); reload(); } catch (e) { go.disabled = false; status.textContent = 'Could not attach: ' + e.message; } });
    body.append(el('div', { class: 'row' }, other, go, status));
    body.append(el('div', { class: 'row' }, UI.copyButton({ label: 'Copy the proof brief', text: () => g.brief }),
      UI.decisionRow({ capability: 'BRN-C03', autonomy: 'agent_does', owner: 'agent_drafts', screen: SCREEN, compact: true,
        finding_id: action ? action.id : ('05-brand-brain.BRN-R23.rung_' + g.theme + '_' + g.level), current: action ? action.decision : null,
        stub: 'The brain agent drafts the proof line for this rung from the records on file (or the missing fact to source), and puts it in the review queue. You approve it; the rung reads it on ' + g.uses.map(pretty).join(', ') + '.' })));
    const panel = UI.panel({ title: 'Brief the proof: ' + pretty(g.theme) + ' rung ' + g.level, body });
  }
  function rungPanel(r) {
    const body = el('div', { class: 'stack' });
    body.append(el('div', { class: 'row' }, el('span', { class: 'chip ' + (r.status === 'proved' ? 'good' : 'warn'), text: r.status + (r.tier ? ', ' + pretty(r.tier) : '') }), ...r.uses.map((u) => el('span', { class: 'chip', text: pretty(u) }))));
    body.append(el('div', { text: 'Doubt: ' + r.doubt }));
    if (r.proof) body.append(el('div', { class: 'small' }, el('b', { text: 'Proof: ' }), r.proof));
    body.append(el('div', { class: 'small muted', text: 'Records: ' + (r.proof_ids.length ? r.proof_ids.join(', ') : 'none') + (r.status === 'weak' ? '. Approve the record in the claims desk and the rung is proved.' : '') }));
    UI.panel({ title: pretty(r.theme) + ' rung ' + r.level, body });
  }
  async function loadLadderProof(actions) {
    let m;
    try { m = await api(BASE + 'ladders/proof'); } catch (e) { mount('#ladderproof', el('p', { class: 'muted', text: 'Ladder proof unavailable: ' + e.message })); return; }
    if (m.unavailable_reason) { mount('#ladderproof-tools'); mount('#ladderproof', el('p', { class: 'muted', text: 'Unavailable: ' + m.unavailable_reason + '.' })); return; }
    const byKey = {}; for (const r of m.rungs) byKey[r.key] = r;
    const byAct = {}; for (const a of actions || []) if (a.rule_id === 'BRN-R23' && a.entity && a.entity.id) byAct[a.entity.id] = a;
    const c = m.counts;
    mount('#ladderproof-tools', UI.orientation([{ label: 'rungs', value: c.rungs, unit: 'n' }, { label: 'proved', value: c.proved, unit: 'n' }, { label: 'weak', value: c.weak, unit: 'n' }, { label: 'no proof', value: c.missing, unit: 'n', title: c.one_star_unproved + ' of ' + c.one_star_total + ' one-star lines sit behind unproved rungs' }, { label: 'blocked cells', value: c.blocked, unit: 'n' }]));
    const matrix = UI.coverageMatrix({
      rows: m.rows, cols: m.cols, cells: m.cells, unit: 'n', single: true, max: 2, corner: 'Rung by surface',
      gapRule: (cell) => (cell && (cell.status === 'missing' || cell.status === 'forbidden')) ? 'gap' : ((cell && (cell.status === 'weak' || cell.status === 'blocked')) ? 'lead' : ''),
      action: { label: 'Brief the proof', onClick: (cell, row) => { const r = byKey[row.key]; if (r && r.brief) proofPanel(r, byAct['rung_' + r.theme + '_' + r.level], () => { loadLadderProof(actions); loadDesk(); }); else if (r) rungPanel(r); } },
      onCell: (cell, row) => { const r = byKey[row.key]; if (!r) return; if (r.brief) proofPanel(r, byAct['rung_' + r.theme + '_' + r.level], () => { loadLadderProof(actions); loadDesk(); }); else rungPanel(r); },
      note: m.note,
    });
    const lines = el('div', { class: 'stack cov-lines' });
    if (m.gaps.length) lines.append(el('div', null, el('b', { text: 'No proof: ' }), m.gaps.map((g) => pretty(g.theme) + ' ' + g.level + ' (' + (g.one_star == null ? NA : g.one_star) + ' one-star, ' + g.uses.length + ' surfaces)').join('; ') + '. Each carries a proof brief and is on the master list.'));
    if (m.weak.length) lines.append(el('div', null, el('b', { text: 'Weak: ' }), m.weak.map((w) => pretty(w.theme) + ' ' + w.level + ' (' + pretty(w.tier) + ')').join('; ') + '. Approve the record and the rung is proved.'));
    if (m.blocked.length) lines.append(el('div', null, el('b', { text: 'Blocked by a surface rule: ' }), m.blocked.map((b) => pretty(b.rung) + ' on the ' + b.surface_label.toLowerCase() + ' (' + b.reason + ')').join('; ') + '. Use a different proof there or fix the wording.'));
    if (!m.gaps.length && !m.weak.length && !m.blocked.length) lines.append(el('div', { class: 'muted', text: 'Every rung is proved on every surface it is used on.' }));
    mount('#ladderproof', matrix, lines);
  }

  // ---------- 5c4. battlecards ----------
  function cardPanel(c) {
    const body = el('div', { class: 'stack' });
    body.append(el('div', { class: 'row' }, UI.verdict(c.verdict.kind, c.verdict.text, c.verdict.reason), c.captured_at ? el('span', { class: 'chip', text: 'read ' + fmt.date(c.captured_at) }) : null, ...c.flags.map((f) => el('span', { class: 'chip warn', text: f.text }))));
    body.append(el('pre', { class: 'card sunken brief', text: c.text }));
    const wins = el('div', { class: 'grid' }, ...c.how_we_win.map((w) => el('div', { class: 'card flat rec' }, el('div', { class: 'meta' }, el('span', { class: 'chip ' + (w.line ? 'good' : 'bad'), text: w.label }), w.claim ? el('span', { class: 'chip mono', text: w.claim }) : null), el('div', { text: w.line || w.status }))));
    body.append(wins);
    body.append(el('div', { class: 'row' }, UI.copyButton({ label: 'Copy the battlecard', text: () => c.text }), c.ad_library_url ? el('a', { class: 'btn sm', href: c.ad_library_url, target: '_blank', rel: 'noopener', text: 'Their ads (read only)' }) : null,
      UI.decisionRow({ capability: 'BRAND-C57', autonomy: 'agent_does', owner: 'agent_drafts', screen: SCREEN, compact: true, stub: 'The brand agent turns this card into a CX macro and 3 copy first lines from the approved claims and puts them in the review queue. You approve before anything ships.' })));
    UI.panel({ title: 'Against ' + c.competitor, body });
  }
  function cardsTable(bc) {
    const rows = bc.cards.map((c) => Object.assign({}, c, { theirs: c.their_angles.map((a) => a.label.toLowerCase()).join(', '), win: c.they_win.map((a) => a.label.toLowerCase()).join(', ') || 'none', gaps: c.proof_gaps.map((g) => g.toLowerCase()).join(', ') || 'none', rec: c.recommended_instead ? c.recommended_instead.threads + ' threads' : '0' }));
    return UI.verdictTable({
      columns: [{ key: 'competitor', label: 'Competitor' }, { key: 'price_band', label: 'Their price', format: (v) => v || NA }, { key: 'theirs', label: 'Their angles' }, { key: 'win', label: 'They run, we do not' }, { key: 'gaps', label: 'Our proof gaps' }, { key: 'rec', label: 'Recommended instead' }, { key: 'long_runner_share', label: 'Their 30 d+ ads', unit: '%', align: 'right' }],
      verdict: { at: 1, kind: (r) => r.verdict.kind, text: (r) => r.verdict.text, reason: (r) => r.verdict.reason },
      actions: { label: 'Open card', onClick: (r) => cardPanel(r) }, rows, sort: false, maxRows: 20, empty: 'No competitor page with angles read yet.',
    });
  }
  async function loadBattlecards() {
    let bc;
    try { bc = await api(BASE + 'battlecards'); } catch (e) { mount('#battlecards', el('p', { class: 'muted', text: 'Battlecards unavailable: ' + e.message })); return; }
    mount('#battlecards-tools', UI.orientation([{ label: 'cards', value: bc.counts.cards, unit: 'n' }, { label: 'with a proof gap', value: bc.counts.with_gaps, unit: 'n', tone: bc.counts.with_gaps ? 'bad' : 'good' }, { label: 'recommended instead', value: bc.counts.recommended_instead, unit: 'n' }]));
    mount('#battlecards', cardsTable(bc), el('div', { class: 'micro faint', text: bc.note }));
  }

  // ---------- 1b. decisions log ----------
  const CHOICE_TEXT = { agent: 'Agent does it', person: 'Sent to a person', not_now: 'Not now, snoozed', undo: 'Undone, back on the list' };
  let decisionsFilter = 'all';
  async function loadDecisions(m) {
    let d;
    try { d = await api(BASE + 'decisions'); } catch (e) { mount('#decisions', el('p', { class: 'muted', text: 'Decisions unavailable: ' + e.message })); return; }
    const byId = {}; for (const a of (m && m.actions) || []) byId[a.id] = a;
    const status = el('span', { class: 'micro muted' });
    const undo = (it) => { const b = el('button', { class: 'btn xs soft', type: 'button', text: it.choice === 'not_now' ? 'Undo the snooze' : 'Undo' }); b.addEventListener('click', async () => { b.disabled = true; try { const r = await api(BASE + 'decisions/undo', { method: 'POST', body: { finding_id: it.finding_id } }); status.textContent = r.next; loadPlan(); } catch (e) { b.disabled = false; status.textContent = 'Could not undo: ' + e.message; } }); return b; };
    const pick = (it) => {
      if (decisionsFilter === 'all') return true;
      if (it.kind === 'brain') return decisionsFilter === 'brain';
      if (decisionsFilter === 'snoozed') return it.current && it.choice === 'not_now' && !it.expired;
      if (decisionsFilter === 'expired') return it.current && it.choice === 'not_now' && it.expired;
      if (decisionsFilter === 'approved') return it.current && (it.choice === 'agent' || it.choice === 'person');
      return true;
    };
    const items = d.items.filter(pick).map((it) => {
      if (it.kind === 'action') {
        const a = byId[it.finding_id];
        const tone = it.superseded ? null : (it.choice === 'not_now' ? (it.expired ? 'bad' : 'warn') : (it.choice === 'undo' ? 'info' : 'good'));
        const title = (it.superseded ? 'Superseded: ' : '') + (CHOICE_TEXT[it.choice] || it.choice) + (it.choice === 'not_now' && it.expires_on ? (it.expired ? ', expired ' + fmt.date(it.expires_on) + ', back on the list' : ' until ' + fmt.date(it.expires_on) + ' (' + it.days_left + ' day' + (it.days_left === 1 ? '' : 's') + ' left)') : '');
        const text = (a ? a.title : (it.finding_id || it.capability)) + (it.reason ? '. ' + it.reason : '') + (it.screen ? ' (' + it.screen + ')' : '');
        return { when: it.time, who: 'you', tone, title, text, extra: it.current && it.finding_id && (it.choice === 'not_now' || it.choice === 'agent' || it.choice === 'person') && !it.expired ? undo(it) : null };
      }
      return { when: it.date, who: it.who || 'founder', tone: 'accent', title: it.title, text: it.text };
    });
    const c = d.counts;
    mount('#decisions-tools', UI.orientation([{ label: 'approvals', value: c.action, unit: 'n' }, { label: 'snoozed', value: c.snoozed, unit: 'n' }, { label: 'expiring in 3 days', value: c.expiring, unit: 'n', tone: c.expiring ? 'warn' : null }, { label: 'expired, back on the list', value: c.expired, unit: 'n', tone: c.expired ? 'bad' : null }, { label: 'brain decisions', value: c.brain, unit: 'n' }, { label: 'last', value: null, unit: 'n', unavailable_label: d.last ? fmt.date(d.last) : 'none yet' }]));
    const filters = el('div', { class: 'row' }, ...[['all', 'All'], ['approved', 'Approved'], ['snoozed', 'Snoozed'], ['expired', 'Expired'], ['brain', 'Brain decisions']].map(([k, label]) => el('button', { class: 'btn xs' + (decisionsFilter === k ? ' primary' : ' soft'), type: 'button', text: label, onclick: () => { decisionsFilter = k; loadDecisions(m); } })), status);
    const tl = UI.timeline(items.slice(0, 30));
    // attach the undo buttons after the kit renders the rows
    Array.from(tl.querySelectorAll('.tl')).forEach((row, i) => { const it = items[i]; if (it && it.extra) row.lastChild.append(el('div', { style: { marginTop: '4px' } }, it.extra)); });
    mount('#decisions', filters, tl, items.length > 30 ? el('div', { class: 'micro faint', text: (items.length - 30) + ' older entries not shown.' }) : null, el('p', { class: 'micro faint', text: d.note }));
  }

  // ---------- 1a. bottlenecks and unlocks ----------
  function ideaRow(i, b, reload) {
    return Object.assign({}, i, { effect: (i.metric || '') + ' ' + (i.direction || '') + (i.size ? ', ' + i.size : ''), ecr: (i.effort || '') + ' / ' + (i.cost || '') + ' / ' + (i.risk || ''), actions: [{ label: 'Pick it', cls: 'primary', onClick: async () => {
      try { const r = await api(BASE + 'bottlenecks/pick', { method: 'POST', body: { idea_id: i.id, bottleneck: b.key } }); alert(r.next); reload(); loadPlan(); } catch (e) { alert('Could not pick: ' + e.message); }
    } }, { label: 'Steps', onClick: () => UI.panel({ title: i.id + ': ' + i.title, body: el('div', { class: 'stack' }, el('div', null, el('b', { text: 'If: ' }), i.hypothesis || ''), el('div', null, el('b', { text: 'Check first: ' }), i.signal || ''), el('ol', { class: 'a-steps' }, ...(i.steps || []).map((st) => el('li', { text: st }))), el('div', { class: 'micro faint', text: 'Bank score ' + i.score + ', confidence ' + (i.confidence || NA) + ', basis ' + (i.basis || NA) + '. Referenced by id; the bank is the source.' })) }) }] });
  }
  function bottleneckCard(b, u, reload) {
    const card = el('article', { class: 'card bottleneck' });
    card.append(el('div', { class: 'row' }, el('span', { class: 'rank num', text: String(b.rank) }), el('h4', { text: pretty(b.theme) }), ...b.codes.map((c) => el('span', { class: 'chip mono', text: pretty(c) })), ...Object.entries(b.numbers).slice(0, 3).map(([k, v]) => el('span', { class: 'chip', text: pretty(k) + ' ' + v })), (b.where || []).length ? el('span', { class: 'micro faint', text: 'seen on ' + b.where.map(pretty).join(', ') }) : null));
    card.append(el('div', { class: 'small', text: b.text || '' }));
    const onList = b.on_list.length ? UI.table({ columns: [{ key: 'title', label: 'On the master list' }, { key: 'screen', label: 'Screen' }, { key: 'owner', label: 'Owner', format: pretty }, { key: 'total', label: 'Score', unit: 'n', align: 'right' }, { key: 'decided', label: 'Decision', format: (v, r) => r.decision ? pretty(r.decision.choice) : 'open' }], rows: b.on_list.slice(0, 6), sort: false })
      : el('p', { class: 'muted small', text: 'Nothing on the master list names this bottleneck yet. The unlocks below fill the gap.' });
    const ideas = b.ideas.length ? UI.verdictTable({ columns: [{ key: 'id', label: 'Idea' }, { key: 'title', label: 'Unlock' }, { key: 'effect', label: 'Expected effect' }, { key: 'ecr', label: 'Effort / cost / risk' }, { key: 'signal', label: 'Check first' }],
      verdict: { at: 1, kind: (r) => r.theme_hits >= 3 ? 'scale' : (r.theme_hits ? 'keep' : 'watch'), text: (r) => r.theme_hits >= 3 ? 'Names it' : (r.theme_hits ? 'Fits' : 'Nearby'), reason: (r) => 'bank score ' + r.score },
      rows: b.ideas.map((i) => ideaRow(i, b, reload)), actions: { label: 'Do' }, sort: false })
      : el('p', { class: 'muted small', text: u.bank.available ? 'No idea in the bank fits this bottleneck and store.' : 'The idea bank is not loadable here.' });
    card.append(el('div', { class: 'grid two' }, el('div', { class: 'stack' }, el('span', { class: 'kicker', text: 'On the list now' }), onList), el('div', { class: 'stack' }, el('span', { class: 'kicker', text: 'Unlocks from the idea bank' }), ideas)));
    if (b.picked.length) card.append(el('div', { class: 'small' }, el('b', { text: 'Picked: ' }), b.picked.map((p) => p.idea_id + ' (' + (p.status || 'picked') + ')').join(', ') + '. Each is a test brief on the master list.'));
    return card;
  }
  async function loadUnlocks() {
    let u;
    try { u = await api(BASE + 'bottlenecks'); } catch (e) { mount('#unlocks', el('p', { class: 'muted', text: 'Bottlenecks unavailable: ' + e.message })); return; }
    mount('#unlocks-tools', UI.orientation([{ label: 'bottlenecks', value: u.bottlenecks.length, unit: 'n' }, { label: 'on the list', value: u.bottlenecks.reduce((a, b) => a + b.on_list.length, 0), unit: 'n' }, { label: 'unlocks offered', value: u.bottlenecks.reduce((a, b) => a + b.ideas.length, 0), unit: 'n' }, { label: 'picked', value: u.picked, unit: 'n' }, { label: 'bank', value: u.bank.ideas, unit: 'n' }]));
    const d = u.diagnosis;
    const items = [];
    if (d.summary) items.push(el('div', { class: 'card flat' }, el('b', { text: 'Diagnosis: ' }), d.summary, ' ', el('span', { class: 'micro faint', text: (d.basis || '') + (d.as_of ? ' As of ' + d.as_of + '.' : '') })));
    items.push(...u.bottlenecks.map((b) => bottleneckCard(b, u, loadUnlocks)));
    if (d.strengths.length) items.push(el('div', { class: 'small' }, el('b', { text: 'Strengths to lead with: ' }), d.strengths.map((s) => pretty(s.theme) + ' (' + Object.entries(s.numbers).slice(0, 2).map(([k, v]) => pretty(k) + ' ' + v).join(', ') + ')').join('; ') + '.'));
    if (d.test_queue.length) items.push(el('div', { class: 'small' }, el('b', { text: 'The diagnosis test queue: ' }), el('ol', { class: 'a-steps' }, ...d.test_queue.map((t) => el('li', { text: t })))));
    items.push(el('div', { class: 'micro faint', text: u.note + ' Store tags: ' + u.store_tags.map(pretty).join(', ') + '.' }));
    mount('#unlocks', ...items);
  }

  // ---------- 1b2. weekly report and founder digest ----------
  async function loadReport() {
    const wrap = el('div', { class: 'stack' });
    mount('#report', wrap);
    const [rp, dg] = await Promise.all([api(BASE + 'report?days=7').catch((e) => ({ error: e.message })), api(BASE + 'digest').catch((e) => ({ error: e.message }))]);
    if (rp.error) { mount(wrap, el('p', { class: 'muted', text: 'Report unavailable: ' + rp.error })); return; }
    mount('#report-tools', UI.orientation([{ label: 'changes', value: rp.counts.changes, unit: 'n' }, { label: 'approved', value: rp.counts.approved, unit: 'n' }, { label: 'questions open', value: rp.counts.questions_open, unit: 'n' }, { label: 'site changes open', value: rp.counts.site_open, unit: 'n' }, { label: 'weak sections', value: rp.counts.weak_sections, unit: 'n' }]));
    const printBtn = el('button', { class: 'btn sm', type: 'button', text: 'Print the report' });
    printBtn.addEventListener('click', () => { document.body.classList.add('print-report'); window.print(); setTimeout(() => document.body.classList.remove('print-report'), 500); });
    mount(wrap, UI.tabs({ items: [
      { key: 'report', label: 'Weekly report', panel: () => el('div', { class: 'stack' }, el('div', { class: 'row' }, UI.copyButton({ label: 'Copy the report', text: () => rp.text }), printBtn, el('span', { class: 'micro faint', text: rp.note })), el('pre', { class: 'card sunken brief report-text', text: rp.text })) },
      { key: 'digest', label: 'Founder round', n: dg.questions, panel: () => dg.error ? el('p', { class: 'muted', text: 'Digest unavailable: ' + dg.error }) : el('div', { class: 'stack' }, el('div', { class: 'row' }, UI.copyButton({ label: 'Copy the digest', text: () => dg.text }), el('span', { class: 'chip', text: 'Slack: ' + (dg.delivery.slack || NA) }), el('span', { class: 'chip', text: 'email: ' + (dg.delivery.email || NA) }), el('span', { class: 'micro faint', text: dg.delivery.reason + '. ' + dg.note })), el('pre', { class: 'card sunken brief', text: dg.text })) },
    ] }));
  }

  // ---------- 1c. what changed this week ----------
  const KIND_TONE = { site: 'warn', founder_edit: 'good', answer: 'good', approve: 'good', forbid: 'bad', conflict: 'accent', document: 'info', proposed: 'info', accepted: 'good', ignored: null, snapshot: 'info' };
  async function loadChanges() {
    let ch;
    try { ch = await api(BASE + 'changes'); } catch (e) { mount('#changes', el('p', { class: 'muted', text: 'Changes unavailable: ' + e.message })); return; }
    const c = ch.counts;
    mount('#changes-tools', UI.orientation([{ label: 'this week', value: c.week, unit: 'n' }, { label: 'site changes', value: c.by_kind.site || 0, unit: 'n', tone: c.by_kind.site ? 'bad' : null }, { label: 'your edits', value: (c.by_kind.founder_edit || 0) + (c.by_kind.answer || 0) + (c.by_kind.approve || 0), unit: 'n' }, { label: 'all time', value: c.total, unit: 'n' }, { label: 'versions', value: ch.versions.length, unit: 'n', title: 'version steps logged' }]));
    const items = ch.week.length ? ch.week : ch.changes.slice(0, 20);
    mount('#changes', ch.changes.length ? UI.timeline(items.map((x) => ({ when: x.date, who: x.source, tone: KIND_TONE[x.kind] || null, title: x.label, text: x.what + (x.before != null && x.after != null ? ' (before: ' + x.before + ')' : '') })))
      : el('p', { class: 'muted', text: 'No change logged yet. Every edit, answer, approval, file and site snapshot lands here.' }),
      !ch.week.length && ch.changes.length ? el('div', { class: 'micro faint', text: 'Nothing in the last ' + ch.days + ' days; showing the latest 20.' }) : null);
  }
  function tracePanel(rid) {
    const body = el('div', { class: 'stack' }, el('p', { class: 'muted small', text: 'Loading.' }));
    const panel = UI.panel({ title: 'Where ' + rid + ' is used', body });
    api(BASE + 'dependents?record=' + encodeURIComponent(rid)).then((d) => {
      mount(body, el('div', null, el('b', { text: d.summary + '. ' }), 'Value: ' + (d.value || NA)),
        d.dependents.length ? UI.table({ columns: [{ key: 'kind', label: 'Kind' }, { key: 'label', label: 'What' }, { key: 'why', label: 'Why' }, { key: 'surf', label: 'Surfaces', format: (v, r) => (r.surfaces || []).map(pretty).join(', ') }, { key: 'id', label: 'Record' }], rows: d.dependents, sort: false }) : null,
        el('div', { class: 'micro faint', text: d.note }));
    }).catch((e) => mount(body, el('p', { class: 'muted', text: 'Could not trace: ' + e.message })));
    return panel;
  }

  function historyPanel(rid, reload) {
    const body = el('div', { class: 'stack' }, el('p', { class: 'muted small', text: 'Loading.' }));
    const panel = UI.panel({ title: 'History of ' + rid, body });
    api(BASE + 'history?record=' + encodeURIComponent(rid)).then((h) => {
      const status = el('span', { class: 'micro muted' });
      const cur = h.current;
      const rows = h.items.map((it) => {
        if (it.kind === 'value') {
          const b = el('button', { class: 'btn xs' + (it.restorable ? ' primary' : ''), type: 'button', text: it.restorable ? 'Restore this' : 'Same as now', disabled: !it.restorable });
          b.addEventListener('click', async () => { b.disabled = true; try { const r = await api(BASE + 'history/restore', { method: 'POST', body: { record: rid, index: it.index } }); status.textContent = r.next; panel.close(); if (reload) reload(); loadProfile(); loadChanges(); } catch (e) { b.disabled = false; status.textContent = 'Could not restore: ' + e.message; } });
          return el('div', { class: 'tl' }, el('span', { class: 'dot' }), el('div', null, el('div', { class: 'when', text: (it.when ? fmt.date(it.when) : 'undated') + (it.source_type || it.source_ref ? ', from ' + (it.source_type ? pretty(it.source_type) + ' ' : '') + (it.source_ref || '') : '') + (it.tier ? ', ' + pretty(it.tier) : '') }), el('div', { class: 'row' }, el('span', { class: 'mono small', text: it.value_text }), b), it.reason ? el('div', { class: 'micro faint', text: it.reason }) : null));
        }
        return el('div', { class: 'tl' }, el('span', { class: 'dot', style: { background: 'var(--info)' } }), el('div', null, el('div', { class: 'when', text: (it.when ? fmt.date(it.when) : '') + ', ' + pretty(it.change_kind || 'change') + (it.source ? ' by ' + it.source : '') }), el('div', { class: 'small', text: it.what || '' })));
      });
      rows.push(el('div', { class: 'tl' }, el('span', { class: 'dot', style: { background: 'var(--good)' } }), el('div', null, el('div', { class: 'when', text: 'Now' + (cur.when ? ', ' + fmt.date(cur.when) : '') + ', ' + pretty(cur.tier) + (cur.source_type ? ', from ' + pretty(cur.source_type) : '') + (cur.restored_from ? ', restored from ' + (cur.restored_from.changed_at || 'an earlier value') : '') }), el('div', { class: 'mono small', text: cur.value_text }))));
      mount(body, el('div', { class: 'row' }, el('span', { class: 'chip', text: h.counts.values + ' earlier value' + (h.counts.values === 1 ? '' : 's') }), el('span', { class: 'chip', text: h.counts.changes + ' logged change' + (h.counts.changes === 1 ? '' : 's') }), status),
        el('div', { class: 'timeline' }, ...rows), el('div', { class: 'micro faint', text: h.note }));
    }).catch((e) => mount(body, el('p', { class: 'muted', text: 'Could not load the history: ' + e.message })));
    return panel;
  }

  // ---------- 2. the profile, editable ----------
  function profileSection(sec) {
    const wrap = el('div', { class: 'profile-sec' });
    wrap.append(el('div', { class: 'row between' },
      el('span', { class: 'small muted', text: sec.records + ' records, ' + sec.approved + ' approved. Flows to ' + sec.flows_to + '.' })));
    for (const f of sec.fields) {
      wrap.append(UI.field({
        key: f.key, name: pretty(f.key), sub: f.variants > 1 ? f.variants + ' records, best shown' : null,
        text: f.text, tier: f.tier, source: f.source, date: f.date, confidence: f.confidence, multiline: true,
        placeholder: 'unavailable. Add it and every screen gets it.',
        onSave: async (text) => api(BASE + 'profile/' + sec.section + '/' + encodeURIComponent(f.key), { method: 'POST', body: { text } }),
      }));
    }
    const withRecord = sec.fields.filter((f) => f.record_id);
    if (withRecord.length) wrap.append(el('div', { class: 'row trace' }, el('span', { class: 'micro faint', text: 'Where is it used?' }), ...withRecord.map((f) => el('button', { class: 'btn xs soft', type: 'button', text: pretty(f.key), onclick: () => tracePanel(f.record_id) }))));
    if (withRecord.length) wrap.append(el('div', { class: 'row trace' }, el('span', { class: 'micro faint', text: 'History and restore:' }), ...withRecord.map((f) => el('button', { class: 'btn xs soft', type: 'button', text: pretty(f.key), onclick: () => historyPanel(f.record_id) }))));
    const addKey = el('input', { class: 'text sm', placeholder: 'new field, like target_customer', style: { maxWidth: '240px' } });
    const addVal = el('input', { class: 'text sm', placeholder: 'value', style: { flex: '1 1 200px' } });
    const addBtn = el('button', { class: 'btn sm', type: 'button', text: 'Add field' });
    const status = el('span', { class: 'micro muted' });
    addBtn.addEventListener('click', async () => {
      const k = addKey.value.trim().toLowerCase().replace(/[^a-z0-9_]+/g, '_').replace(/^_+|_+$/g, '');
      if (!k || !addVal.value.trim()) { status.textContent = 'Give the field a name and a value.'; return; }
      try { await api(BASE + 'profile/' + sec.section + '/' + k, { method: 'POST', body: { text: addVal.value.trim() } }); status.textContent = 'Saved as approved. Reload to see it in place.'; addKey.value = ''; addVal.value = ''; }
      catch (e) { status.textContent = 'Could not save: ' + e.message; }
    });
    wrap.append(el('div', { class: 'row add-field' }, addKey, addVal, addBtn, status));
    return wrap;
  }
  async function loadProfile() {
    let p;
    try { p = await api(BASE + 'profile'); } catch (e) { mount('#profile', el('p', { class: 'muted', text: 'Profile unavailable: ' + e.message })); return null; }
    mount('#profile-tools', UI.orientation([
      { label: 'fields', value: p.fields, unit: 'n' }, { label: 'approved by you', value: p.approved, unit: 'n', tone: 'good' },
      { label: 'approved share', value: p.approved_share, unit: '%' }]));
    mount('#profile', UI.tabs({ items: p.sections.map((s) => ({ key: s.section, label: s.label, n: s.fields.filter((f) => f.text).length, panel: () => profileSection(s) })) }));
    return p;
  }

  // ---------- 2b. where an edit goes: flow proof ----------
  async function loadFlows() {
    let fl;
    try { fl = await api(BASE + 'flows'); } catch (e) { mount('#flows', el('p', { class: 'muted small', text: 'Flow proof unavailable: ' + e.message })); return; }
    const rows = fl.sections.map((s) => Object.assign({}, s, { readers: s.read_by.join(', ') || 'none directly', t0: s.read_by_t0.length ? s.read_by_t0.join(', ') : 'none', logged: (s.read_by_log || []).join(', ') || 'none yet', last_read_text: s.last_read ? fmt.date(s.last_read) + (s.last_reader ? ' by ' + s.last_reader : '') : NA + ' (' + s.last_read_reason + ')' }));
    const table = UI.table({
      columns: [
        { key: 'label', label: 'Profile section' },
        { key: 'approved', label: 'Approved by you', unit: 'n', align: 'right' },
        { key: 'last_founder_edit', label: 'Last edit', format: (v) => v ? fmt.date(v) : 'none yet' },
        { key: 'readers', label: 'Read by (code scan)' },
        { key: 't0', label: 'Read through the T0 card' },
        { key: 'logged', label: 'Read log' },
        { key: 'reach', label: 'Screens reached', unit: 'n', align: 'right' },
        { key: 'last_read_text', label: 'Last read' },
        { key: 'flows_to', label: 'Flows to (contract)' },
      ], rows, sort: false,
    });
    mount('#flows', el('div', { class: 'flows' }, el('div', { class: 'sec-head' }, el('h3', { text: 'Where an edit goes' }), el('span', { class: 'sub', text: fl.note + ' ' + fl.screens_scanned + ' screens scanned.' })), table));
  }

  // ---------- 3. files in ----------
  function docsTable(d) {
    return UI.table({
      columns: [
        { key: 'name', label: 'File' },
        { key: 'added_at', label: 'Added', format: (v) => v ? fmt.date(v) : NA },
        { key: 'added_by', label: 'By', format: (v) => v || 'unknown' },
        { key: 'proposed', label: 'Waiting', unit: 'n', align: 'right' },
        { key: 'accepted', label: 'Accepted', unit: 'n', align: 'right' },
        { key: 'sections_changed', label: 'Sections', format: (v) => (v || []).map(pretty).join(', ') || '' },
        { key: 'what_changed', label: 'What it changed' },
        { key: 'note', label: 'Note', format: (v) => v || '' },
      ], rows: d.documents, sort: false, empty: 'No files yet. Drop a brand book, a deck, past tests, anything.',
      onRow: (r) => { if (r.readable && !r.extracted) reReadDoc(r.name); },
    });
  }
  async function reReadDoc(name) {
    try { const res = await api(BASE + 'documents/extract', { method: 'POST', body: { name } }); loadDocs(); loadDesk(); return res; }
    catch (e) { return null; }
  }
  async function loadDocs() {
    try { mount('#documents', docsTable(await api(BASE + 'documents'))); }
    catch (e) { mount('#documents', el('p', { class: 'muted', text: 'Documents unavailable: ' + e.message })); }
  }
  function readAsBase64(file) {
    return new Promise((resolve, reject) => { const r = new FileReader(); r.onload = () => resolve(String(r.result).split(',')[1] || ''); r.onerror = reject; r.readAsDataURL(file); });
  }
  function mountDrop() {
    const status = el('div', { class: 'small muted', 'aria-live': 'polite' });
    const zone = UI.dropZone({
      hint: 'Up to 5 MB each. It is stored as it is. A text or markdown file is also read into proposed records: headings, key: value lines, bullets, things you tried, things we must never say. You accept them in the review queue.',
      onFiles: async (files) => {
        for (const f of files) {
          status.textContent = 'Adding ' + f.name;
          try {
            const res = await api(BASE + 'documents', { method: 'POST', body: { name: f.name, content_base64: await readAsBase64(f) } });
            status.textContent = 'Added ' + res.document.name + ' (' + fmt.compact(res.document.bytes) + ' bytes). ' + res.next;
            if (res.records_changed_count) loadDesk();
          } catch (e) { status.textContent = 'Could not add ' + f.name + ': ' + e.message; }
        }
        loadDocs();
      },
      onUrl: async (url) => {
        status.textContent = 'Adding url';
        try { const res = await api(BASE + 'documents', { method: 'POST', body: { url } }); status.textContent = 'Added ' + res.document.name + '. ' + res.next; loadDocs(); }
        catch (e) { status.textContent = 'Could not add: ' + e.message; }
      },
    });
    mount('#drop', zone, status);
  }

  // ---------- 4. competitors and market ----------
  const pct = (v) => v == null ? NA : Math.round(v * 100) + '%';
  function marketOrient(d) {
    const us = d.us || {};
    const med = d.medians || {};
    return [
      { label: 'pages pulled', value: d.competitors_pulled, unit: 'n', title: d.competitors_configured + ' configured' },
      { label: 'our ads seen', value: us.ads_seen, unit: 'n' },
      { label: 'ours 30 days+', value: us.long_runner_share, unit: '%', title: 'share of our ads that have run 30 days or more' },
      { label: 'their median 30 days+', value: med.long_runner_share, unit: '%' },
      { label: 'snapshot age', value: d.snapshot_age_days, unit: 'days', tone: d.snapshot_age_days > d.stale_after_days ? 'bad' : null },
      { label: 'gaps', value: (d.gaps || []).length, unit: 'n', tone: (d.gaps || []).length ? 'bad' : 'good' },
    ];
  }
  function pagesTable(d) {
    const rows = d.pages.map((p) => Object.assign({}, p, {
      video: p.format_share ? p.format_share.video : null, image: p.format_share ? p.format_share.image : null,
      dco: p.format_share ? p.format_share.dco : null, dpa: p.format_share ? p.format_share.dpa : null,
      question: p.hook_share ? p.hook_share.question : null, first_person: p.hook_share ? p.hook_share.first_person : null,
      offers: (p.offers_seen || []).join(', ') || (p.pulled ? 'none seen' : ''), flags_text: (p.flags || []).map((f) => f.text).join('; '),
      page_label: p.name + (p.role === 'self' ? ' (us)' : ''),
    }));
    return UI.verdictTable({
      columns: [
        { key: 'page_label', label: 'Page' },
        { key: 'ads_seen', label: 'Ads seen', unit: 'n', align: 'right' },
        { key: 'video', label: 'Video', unit: '%', align: 'right' },
        { key: 'image', label: 'Image', unit: '%', align: 'right' },
        { key: 'dco', label: 'Dynamic', unit: '%', align: 'right' },
        { key: 'dpa', label: 'Catalog', unit: '%', align: 'right' },
        { key: 'question', label: 'Question hooks', unit: '%', align: 'right' },
        { key: 'first_person', label: 'First person', unit: '%', align: 'right' },
        { key: 'long_runner_share', label: '30 days+', unit: '%', align: 'right' },
        { key: 'median_run_days', label: 'Median run', unit: 'days', align: 'right' },
        { key: 'offers', label: 'Offers seen' },
        { key: 'flags_text', label: 'Signals' },
      ],
      verdict: { at: 1, kind: (r) => r.verdict.kind, text: (r) => r.verdict.text, reason: (r) => r.verdict.reason },
      reason: { key: 'why', label: 'Why', text: (r) => r.verdict.reason },
      actions: { label: 'Open Ad Library', onClick: (r) => { if (r.ad_library_url) window.open(r.ad_library_url, '_blank', 'noopener'); } },
      rows, sort: false, maxRows: 20, empty: 'No Ad Library pages configured for this brand.',
      onRow: (r) => openPage(r, d),
    });
  }
  function openPage(p, d) {
    const med = d.medians || {};
    const body = el('div', { class: 'stack' });
    body.append(el('div', { class: 'row' }, el('span', { class: 'chip ' + (p.role === 'self' ? 'accent' : '') , text: p.role === 'self' ? 'us' : 'competitor' }),
      p.captured_at ? el('span', { class: 'chip', text: 'captured ' + fmt.date(p.captured_at) }) : el('span', { class: 'chip warn', text: 'not pulled' }),
      ...(p.flags || []).map((f) => el('span', { class: 'chip warn', text: f.text }))));
    if (p.positioning) body.append(el('div', null, el('b', { text: 'Positioning: ' }), p.positioning));
    if (p.price_band) body.append(el('div', null, el('b', { text: 'Price band: ' }), p.price_band));
    if (p.what_they_push) body.append(el('div', null, el('b', { text: 'Pushes now: ' }), p.what_they_push));
    if ((p.angles || []).length) body.append(el('div', null, el('b', { text: 'Angles seen: ' }), p.angles.join(', ')));
    if (p.format_share) {
      body.append(Charts.bar({ title: 'Format mix against the competitor median', labels: d.formats.map((f) => f.label),
        series: [{ name: p.name, values: d.formats.map((f) => p.format_share[f.key] == null ? null : Math.round(p.format_share[f.key] * 100)) },
                 { name: 'competitor median', values: d.formats.map((f) => med.format_share && med.format_share[f.key] != null ? Math.round(med.format_share[f.key] * 100) : null) }],
        unit: '%', height: 200, note: 'Share of ads seen on the page. Median across ' + (med.n || 0) + ' competitor pages with 20 or more ads.' }));
      body.append(Charts.bar({ title: 'Hook form mix', labels: d.hooks.map((h) => h.label),
        series: [{ name: p.name, values: d.hooks.map((h) => p.hook_share[h.key] == null ? null : Math.round(p.hook_share[h.key] * 100)) },
                 { name: 'competitor median', values: d.hooks.map((h) => med.hook_share && med.hook_share[h.key] != null ? Math.round(med.hook_share[h.key] * 100) : null) }],
        unit: '%', height: 200, note: 'Hook form is how the first line opens, not what it says. Angles are in the coverage matrix.' }));
    }
    body.append(el('div', { class: 'small muted', text: 'Records: ' + (p.record_ids || []).join(', ') }));
    body.append(el('p', { class: 'micro faint', text: d.note }));
    UI.panel({ title: p.name, body, tools: p.ad_library_url ? [el('a', { class: 'btn sm', href: p.ad_library_url, target: '_blank', rel: 'noopener', text: 'Open in the Ad Library' })] : null });
  }
  function mixChart(d, kind) {
    const keys = kind === 'format' ? d.formats : d.hooks;
    const pages = d.pages.filter((p) => p.pulled);
    const share = (p, k) => (kind === 'format' ? p.format_share : p.hook_share);
    return Charts.bar({
      title: kind === 'format' ? 'Format mix by page, us first' : 'Hook form mix by page, us first',
      labels: pages.map((p) => p.role === 'self' ? p.name + ' (us)' : p.name), stacked: true, unit: '%', height: 260,
      series: keys.map((k) => ({ name: k.label, values: pages.map((p) => { const s = share(p, k.key); return s && s[k.key] != null ? Math.round(s[k.key] * 100) : null; }) })),
      note: kind === 'format' ? 'Share of ads seen per page. Dynamic and catalog are auto-built from the feed; video and image are made by hand.' : 'Statement hooks dominate every page. The rare forms (question, first person, number, offer) are where a test can stand out.',
    });
  }
  function gapCards(d, actions) {
    const byKey = {};
    for (const a of actions || []) if (a.entity && a.entity.id) byKey[a.entity.id] = a;
    const wrap = el('div', { class: 'grid' });
    for (const g of d.gaps || []) {
      const a = byKey[g.kind + '_' + g.key];
      if (a) { a.finding_ids = a.finding_ids || [a.id]; }
      if (a) { wrap.append(UI.actionCard(a, { screen: SCREEN, expanded: false })); continue; }
      wrap.append(el('div', { class: 'card flat' }, el('b', { text: g.label }), el('div', { class: 'small muted', text: 'us ' + pct(g.us) + ', competitor median ' + pct(g.them) + '. Leaders: ' + g.leaders.map((l) => l.name + ' ' + pct(l.share)).join(', ') })));
    }
    if (!(d.gaps || []).length) wrap.append(el('p', { class: 'muted', text: 'No format or hook-form gap against the competitor median. Check the coverage matrix for angle gaps.' }));
    return wrap;
  }
  function repullStrip(d) {
    const r = d.repull || {};
    const stale = d.snapshot_age_days != null && d.snapshot_age_days > d.stale_after_days;
    const cost = r.estimate_usd != null ? fmt.unit(r.estimate_usd, '$') : NA + (r.estimate_reason ? ' (' + r.estimate_reason + ')' : '');
    const line = el('div', { class: 'row between' },
      el('div', null, el('b', { text: (stale ? 'Snapshot is stale. ' : 'Snapshot is fresh. ') }),
        'A fresh pull of ' + r.pages + ' pages by page id, up to ' + fmt.compact(r.items_max || 0) + ' ads, costs about ' + cost + '. Caps: ' + (r.cap_per_run_usd != null ? fmt.unit(r.cap_per_run_usd, '$') : NA) + ' a run, ' + (r.cap_per_week_usd != null ? fmt.unit(r.cap_per_week_usd, '$') : NA) + ' a week. Spent this week: ' + (r.week_spent_usd != null ? fmt.unit(r.week_spent_usd, '$') : NA) + '.'),
      UI.decisionRow({ capability: 'BRN-C11', autonomy: 'agent_does', owner: 'agent', screen: SCREEN, compact: true,
        stub: 'Queues one Ad Library pull of the ' + r.pages + ' configured pages by page id through app/connectors/apify.py. Estimated ' + cost + '. The connector checks the per-run and weekly caps and refuses over either. Never a search term. Records land in the review queue.' }));
    const notPulled = (d.not_pulled || []).length ? el('div', { class: 'small muted', text: 'Not pulled: ' + d.not_pulled.join(', ') + ' (no page id, or no ads in the market).' }) : null;
    return el('div', { class: 'card flat repull' + (stale ? ' stale' : '') }, line, notPulled, el('div', { class: 'micro faint', text: r.note || '' }));
  }
  // ---------- 4b. coverage matrix: angles by page ----------
  function briefPanel(g, action) {
    const body = el('div', { class: 'stack' });
    body.append(el('div', { class: 'row' }, el('span', { class: 'chip bad', text: 'gap' }), ...g.competitors.map((n) => el('span', { class: 'chip', text: n }))));
    body.append(el('pre', { class: 'card sunken brief', text: g.brief }));
    const proof = g.proof || { claims: [], rungs: [] };
    if (proof.claims.length) body.append(el('div', { class: 'small' }, el('b', { text: 'Claims in the brain for this angle: ' }), proof.claims.map((c) => c.id + ' (' + pretty(c.tier) + ')').join(', ')));
    if (proof.rungs.length) body.append(el('div', { class: 'small' }, el('b', { text: 'Doubts on the ladder: ' }), proof.rungs.map((r) => r.doubt + (r.has_proof ? '' : ' (no proof)')).join('; ')));
    body.append(el('div', { class: 'row' }, UI.copyButton({ label: 'Copy brief', text: () => g.brief }),
      UI.decisionRow({ capability: 'CREA-C06', autonomy: 'agent_does', owner: 'agent', screen: SCREEN, compact: true,
        finding_id: action ? action.id : ('05-brand-brain.BRN-R08.angle_' + g.angle), current: action ? action.decision : null,
        stub: 'The creative agent writes 3 concepts on the ' + g.label.toLowerCase() + ' angle from this brief and puts them in the review queue. Nothing runs before you approve.' })));
    UI.panel({ title: 'Brief it: ' + g.label, body });
  }
  async function loadCoverage(actions) {
    let c;
    try { c = await api(BASE + 'coverage'); } catch (e) { mount('#coverage', el('p', { class: 'muted', text: 'Coverage unavailable: ' + e.message })); return; }
    const byGap = {}; for (const g of c.gaps || []) byGap[g.angle] = g;
    const byAct = {}; for (const a of actions || []) if (a.entity && a.entity.id) byAct[a.entity.id] = a;
    const maxUs = Math.max(1, ...Object.values(c.cells).map((r) => (r.us && r.us.us) || 0));
    const matrix = UI.coverageMatrix({
      rows: c.rows, cols: c.cols, cells: c.cells, unit: 'n', single: true, max: maxUs, corner: 'Angle',
      gapRule: (cell, row, col) => col.key === 'us' ? (byGap[row.key] ? 'gap' : (c.leads.some((l) => l.angle === row.key) ? 'lead' : '')) : '',
      action: { label: 'Brief it', onClick: (cell, row) => { const g = byGap[row.key]; if (g) briefPanel(g, byAct['angle_' + g.angle]); } },
      onCell: (cell, row, col) => { if (col.key === 'us' && byGap[row.key]) briefPanel(byGap[row.key], byAct['angle_' + row.key]); },
      note: c.note,
    });
    const lines = el('div', { class: 'stack cov-lines' });
    if ((c.gaps || []).length) lines.append(el('div', null, el('b', { text: 'Gaps: ' }), c.gaps.map((g) => g.label.toLowerCase() + ' (' + g.competitors.length + ')').join(', ') + '. Each carries a drafted brief.'));
    if ((c.unused_own || []).length) lines.append(el('div', null, el('b', { text: 'Own ground unused: ' }), c.unused_own.map((u) => u.label.toLowerCase()).join(', ') + '. The brain names it as who we are and no ad leads with it.'));
    if ((c.leads || []).length) lines.append(el('div', null, el('b', { text: 'Only us: ' }), c.leads.map((l) => l.label.toLowerCase() + ' (' + l.us_n + ' ads)').join(', ') + '. Keep it, and watch for a competitor entering.'));
    if ((c.contested || []).length) lines.append(el('div', null, el('b', { text: 'Contested: ' }), c.contested.map((x) => x.label.toLowerCase() + ' (' + x.us_n + ' ads, ' + x.competitors.length + ' competitors)').join(', ') + '. Proof and format decide these, not the angle.'));
    if ((c.unmapped.us || []).length) lines.append(el('div', { class: 'micro faint', text: 'Our hooks not mapped to an angle: ' + c.unmapped.us.join(', ') + '.' }));
    mount('#coverage', matrix, lines);
  }

  // ---------- 4c. market signals: recommended instead, frames, competitor sets ----------
  function answerPanel(r, action) {
    const body = el('div', { class: 'stack' });
    const lad = r.ladder || {};
    const db = lad.deal_breaker || {};
    body.append(el('div', { class: 'row' }, el('span', { class: 'chip bad', text: r.threads + ' threads, ' + (r.upvotes == null ? NA : r.upvotes) + ' upvotes' }), ...r.subreddits.map((x) => el('span', { class: 'chip', text: 'r/' + x }))));
    body.append(el('div', null, el('b', { text: 'The doubt behind it: ' }), r.doubt_label.toLowerCase() + '. ' + (lad.theme ? 'Our ' + pretty(lad.theme) + ' ladder: ' + lad.rungs + ' rungs, ' + lad.no_proof + ' without proof.' : 'No ladder for it yet.')));
    if (db.doubt) body.append(el('div', { class: 'card sunken' }, el('b', { text: 'Deal-breaker rung ' + db.level + ': ' }), db.doubt, ' ', el('span', { class: 'chip ' + (db.has_proof ? 'good' : 'bad'), text: db.has_proof ? 'proof on file' : 'no proof' }), db.one_star != null ? el('span', { class: 'chip', text: db.one_star + ' one-star mentions' }) : null));
    body.append(el('div', null, el('b', { text: 'Where the answer goes: ' }), r.where.join(', ') + '.'));
    body.append(el('div', { class: 'small muted', text: r.never }));
    if (action) body.append(UI.actionCard(action, { screen: SCREEN, expanded: true }));
    else body.append(UI.decisionRow({ capability: 'BRAND-C57', autonomy: 'agent_does', owner: 'agent', screen: SCREEN, compact: true, finding_id: '05-brand-brain.BRN-R09.recommended_' + r.slug }));
    UI.panel({ title: 'Answer ' + r.competitor, body });
  }
  function recommendedTable(sg, byAct) {
    const rows = sg.recommended.map((r) => Object.assign({}, r, { subs: r.subreddits.map((x) => 'r/' + x).join(', '), where_text: r.where.join(', '), tracked: r.page_tracked ? 'yes' : (r.page_id_on_file ? 'pull pending' : 'no page id') }));
    return UI.verdictTable({
      columns: [
        { key: 'competitor', label: 'Recommended instead' },
        { key: 'threads', label: 'Threads', unit: 'n', align: 'right' },
        { key: 'upvotes', label: 'Upvotes', unit: 'n', align: 'right' },
        { key: 'subs', label: 'Where said' },
        { key: 'doubt_label', label: 'The doubt behind it' },
        { key: 'where_text', label: 'Answer goes to' },
        { key: 'tracked', label: 'Ads tracked' },
      ],
      verdict: { at: 1, kind: (r) => r.proof_status === 'proof on file' ? 'keep' : (r.threads >= 3 ? 'stop' : 'fix'), text: (r) => r.proof_status === 'proof on file' ? 'Proof on file' : (r.proof_status === 'no ladder' ? 'No ladder' : 'No proof'), reason: (r) => r.proof_status },
      reason: { key: 'why', label: 'Our proof', text: (r) => r.proof_status + (r.ladder && r.ladder.deal_breaker && !r.ladder.deal_breaker.has_proof ? ': "' + r.ladder.deal_breaker.doubt + '"' : '') },
      actions: { label: 'Answer it', onClick: (r) => answerPanel(r, byAct['recommended_' + r.slug]) },
      rows, sort: false, empty: 'No public thread recommends a competitor instead. Good, and check the pull is fresh.',
    });
  }
  function framesBlock(sg) {
    const fr = sg.frames || [];
    const wrap = el('div', { class: 'stack' });
    wrap.append(Charts.bar({ title: 'How buyers frame the category, mentions', labels: fr.map((f) => f.label), series: [{ name: 'mentions', values: fr.map((f) => f.mentions) }], unit: 'n', height: 180, values: true,
      note: 'From public threads. A frame with no line in our positioning is a gap the positioning screen fills; the brain owns the frame text.' }));
    const lines = el('div', { class: 'stack cov-lines' });
    for (const f of fr) lines.append(el('div', null, el('span', { class: 'chip ' + (f.covered_by_our_frame === false ? 'bad' : f.covered_by_our_frame ? 'good' : ''), text: f.covered_by_our_frame === false ? 'not in our frame' : f.covered_by_our_frame ? 'in our frame' : 'no angle' }), ' ', el('b', { text: f.label }), ' ' + f.mentions + ' mentions'));
    if (sg.our_frame) lines.append(el('div', { class: 'small muted' }, el('b', { text: 'Our frame (' + pretty(sg.our_frame.tier) + '): ' }), sg.our_frame.text));
    if (sg.mission_vs_marketing) lines.append(el('div', { class: 'small' }, el('b', { text: 'Mission read: ' }), 'marketing brand ' + sg.mission_vs_marketing.marketing + ', giving brand ' + sg.mission_vs_marketing.mission + '. ' + (sg.mission_vs_marketing.text || '')));
    wrap.append(lines);
    return wrap;
  }
  function setsBlock(sg, reload) {
    const wrap = el('div', { class: 'stack' });
    if (sg.competitor_frame) wrap.append(el('div', { class: 'small' }, el('span', { class: 'chip good', text: pretty(sg.competitor_frame.tier) }), ' ', el('b', { text: 'Competitor frame: ' }), sg.competitor_frame.text));
    for (const [k, names] of Object.entries(sg.sets || {})) {
      wrap.append(el('div', { class: 'row' }, el('span', { class: 'kicker', text: pretty(k) }), ...names.map((n) => el('span', { class: 'chip ' + (n.tracked ? 'accent' : ''), text: n.name + (n.tracked ? '' : ' (not tracked)') }))));
    }
    for (const p of sg.proposed || []) {
      const input = el('input', { class: 'text sm', placeholder: 'Meta page id (digits)', 'aria-label': 'Page id for ' + p.name, style: { maxWidth: '200px' } });
      const btn = el('button', { class: 'btn sm primary', type: 'button', text: 'Add ' + p.name });
      const status = el('span', { class: 'micro muted' });
      btn.addEventListener('click', async () => {
        btn.disabled = true;
        try { const res = await api(BASE + 'competitors/page-id', { method: 'POST', body: { name: p.name, page_id: input.value.trim() } }); status.textContent = 'Saved ' + res.record + '. Flows to ' + res.flows_to + '.'; if (reload) reload(); }
        catch (e) { btn.disabled = false; status.textContent = 'Could not save: ' + e.message; }
      });
      wrap.append(el('div', { class: 'card flat proposed' }, el('div', null, el('b', { text: 'Proposed: ' + p.name }), ' score ' + p.score + '. ' + p.reasons.join(' ') + ' A person pastes the page id; the next pull reads it by id.'),
        el('div', { class: 'row' }, input, btn, status)));
    }
    return wrap;
  }
  async function loadSignals(actions, reload) {
    let sg;
    try { sg = await api(BASE + 'signals'); } catch (e) { mount('#signals', el('p', { class: 'muted', text: 'Signals unavailable: ' + e.message })); return; }
    const byAct = {}; for (const a of actions || []) if (a.entity && a.entity.id) byAct[a.entity.id] = a;
    mount('#signals', UI.tabs({ items: [
      { key: 'rec', label: 'Recommended instead', n: sg.recommended.length, panel: () => el('div', { class: 'stack' }, recommendedTable(sg, byAct), el('div', { class: 'micro faint', text: sg.note })) },
      { key: 'frames', label: 'Category frames', n: sg.frames.length, panel: () => framesBlock(sg) },
      { key: 'sets', label: 'Competitor sets', n: Object.values(sg.sets || {}).reduce((a, b) => a + b.length, 0), panel: () => setsBlock(sg, reload) },
    ] }));
  }

  async function loadMarket() {
    let d, actions = [];
    try { d = await api(BASE + 'competitors'); } catch (e) { mount('#market', el('p', { class: 'muted', text: 'Competitors unavailable: ' + e.message })); return null; }
    try { const r = await api(BASE + 'rank'); actions = (r.actions || []).filter((a) => /BRN-R(0[5-9]|10)/.test(a.rule_id || '')); } catch (e) { actions = []; }
    mount('#market-tools', UI.orientation(marketOrient(d)));
    const gapsN = (d.gaps || []).length;
    loadCoverage(actions);
    loadSignals(actions, loadMarket);
    mount('#market', UI.tabs({ items: [
      { key: 'gaps', label: 'Gaps to brief', n: gapsN, panel: () => gapCards(d, actions) },
      { key: 'pages', label: 'Pages', n: d.pages.length, panel: () => el('div', { class: 'stack' }, pagesTable(d), el('div', { class: 'micro faint', text: d.note + ' Click a row for the page detail.' })) },
      { key: 'formats', label: 'Format mix', panel: () => mixChart(d, 'format') },
      { key: 'hooks', label: 'Hook mix', panel: () => mixChart(d, 'hook') },
    ], current: gapsN ? 'gaps' : 'pages' }), repullStrip(d));
    return d;
  }

  // ---------- 5. health: freshness by confidence ----------
  const KIND_VERDICT = { connect: 'stop', ask: 'fix', recrawl: 'watch', ok: 'keep' };
  function cellPanel(sec, tier) {
    const body = el('div', { class: 'stack' });
    const list = el('div', { class: 'grid' });
    body.append(el('div', { class: 'small muted', text: 'Approve makes it an approved founder record that wins the merge; forbid marks it as a thing we never say. Both keep the old tier in history.' }), list);
    UI.panel({ title: pretty(sec) + ': ' + pretty(tier) + ' records', body });
    api(BASE + 'health/cell?section=' + encodeURIComponent(sec) + '&tier=' + encodeURIComponent(tier)).then((d) => {
      if (!d.records.length) { list.append(el('p', { class: 'muted', text: 'No records in this cell.' })); return; }
      for (const r of d.records) {
        const card = el('article', { class: 'card flat rec' });
        card.append(el('div', { class: 'meta' }, tierChip(r.tier), el('span', { class: 'chip mono', text: r.id }), el('span', { text: r.date ? fmt.date(r.date) : 'undated' }), el('span', { text: 'confidence ' + (r.confidence == null ? NA : r.confidence) })));
        card.append(el('div', { text: r.text || '' }), el('div', { class: 'meta' }, sourceLink({ type: r.source.type, ref: r.source.ref, link: /^https?:/.test(r.source.ref) ? r.source.ref : null })));
        const status = el('span', { class: 'micro muted' });
        const act = (choice) => async (e) => {
          e.target.disabled = true;
          try { const res = await api(BASE + 'approve/' + encodeURIComponent(r.id), { method: 'POST', body: { choice } }); status.textContent = 'Now ' + res.tier + ' (was ' + res.was + ').'; card.classList.add('settled'); }
          catch (err) { e.target.disabled = false; status.textContent = 'Could not save: ' + err.message; }
        };
        if (r.tier !== 'approved') card.append(el('div', { class: 'row' }, el('button', { class: 'btn primary sm', type: 'button', text: 'Approve as is', onclick: act('approve') }), el('button', { class: 'btn danger sm', type: 'button', text: 'Forbid', onclick: act('forbid') }), status));
        list.append(card);
      }
    }).catch((e) => list.append(el('p', { class: 'muted', text: 'Could not load: ' + e.message })));
  }
  function sectionPanel(s, action) {
    const v = s.verdict;
    const body = el('div', { class: 'stack' });
    body.append(el('div', { class: 'row' }, UI.verdict(KIND_VERDICT[v.kind], v.text, v.reason), el('span', { class: 'chip', text: s.records + ' records' }), s.age_days != null ? el('span', { class: 'chip', text: s.age_days + ' d old, shelf ' + (s.shelf_days == null ? 'none' : s.shelf_days + ' d') }) : null, s.confidence != null ? el('span', { class: 'chip', text: 'confidence ' + s.confidence }) : null));
    body.append(el('div', null, el('b', { text: 'Why: ' }), v.reason + '.'));
    if (s.rooms.length) body.append(el('div', null, el('b', { text: 'Rooms that read it: ' }), s.rooms.map(pretty).join(', ') + '.'));
    if (s.empty_fields.length) body.append(el('div', null, el('b', { text: 'Fields the rooms need and do not have: ' }), s.empty_fields.map((f) => pretty(f.split('.').slice(1).join('.'))).join(', ') + '.'));
    if (s.sources.length) body.append(el('div', null, el('b', { text: 'Sources that fill it: ' }), s.sources.map((x) => x.name + (x.access === 'public' && !/public/i.test(x.name) ? ' (public)' : '')).join(', ') + '.'));
    body.append(el('div', { class: 'row' }, ...Object.entries(s.counts).filter(([, n]) => n).map(([t, n]) => el('button', { class: 'btn xs soft', type: 'button', text: pretty(t) + ' ' + n, onclick: () => cellPanel(s.section, t) }))));
    if (action) body.append(UI.actionCard(action, { screen: SCREEN, expanded: true }));
    else if (v.kind !== 'ok') body.append(UI.actionCard({ id: '05-brand-brain.health.' + s.section, title: v.text + ': ' + pretty(s.section), why: v.reason + '.', severity: 'medium', owner: v.owner, capability: { id: v.capability }, artefact: { kind: v.artefact, label: v.artefact === 'connector_setup' ? 'a source connected, read-only' : 'approved brain records' }, steps: v.steps, finding_ids: [] }, { screen: SCREEN, expanded: true }));
    body.append(el('button', { class: 'btn sm', type: 'button', text: 'Browse all records', onclick: () => openSection(s.section) }));
    UI.panel({ title: pretty(s.section), body });
  }
  function healthTable(h, byAct) {
    const rows = h.sections.map((s) => Object.assign({}, s, { strong_pct: s.strong_share, rooms_n: s.rooms.length, rooms_text: s.rooms.slice(0, 4).map(pretty).join(', ') + (s.rooms.length > 4 ? ' +' + (s.rooms.length - 4) : ''), age: s.records ? s.age_days : null }));
    return UI.verdictTable({
      columns: [
        { key: 'label', label: 'Section' },
        { key: 'records', label: 'Records', unit: 'n', align: 'right', format: (v) => v ? String(v) : 'no records' },
        { key: 'age', label: 'Newest', unit: 'days', align: 'right' },
        { key: 'shelf_days', label: 'Shelf', unit: 'days', align: 'right', format: (v) => v == null ? 'none' : v + ' d' },
        { key: 'strong_pct', label: 'Approved or backed', unit: '%', align: 'right' },
        { key: 'confidence', label: 'Confidence', align: 'right', format: (v) => v == null ? NA : v.toFixed(2) },
        { key: 'rooms_text', label: 'Rooms that read it' },
      ],
      verdict: { at: 1, kind: (r) => KIND_VERDICT[r.verdict.kind], text: (r) => r.verdict.text, reason: (r) => r.verdict.reason },
      actions: { label: (r) => r.verdict.kind === 'ok' ? 'Open' : 'Do it', onClick: (r) => sectionPanel(r, byAct[r.section]) },
      rows, sort: false, maxRows: 40,
    });
  }
  // ---------- 5c. connectors ----------
  function connectPanel(c) {
    const body = el('div', { class: 'stack' });
    body.append(el('div', { class: 'row' }, UI.verdict(c.verdict.kind, c.verdict.text, c.verdict.reason), el('span', { class: 'chip', text: c.sources + ' options' }), c.last_pull ? el('span', { class: 'chip', text: 'last pull ' + fmt.date(c.last_pull) }) : null));
    body.append(el('div', null, el('b', { text: 'Fills: ' }), c.fills_sections.map(pretty).join(', ') + '.'));
    body.append(el('div', null, el('b', { text: 'Unblocks: ' }), (c.unblocks_rooms.map(pretty).join(', ') || 'no room yet') + '.'));
    body.append(el('div', null, el('b', { text: 'Options: ' }), c.alternatives.map((a) => a.name).join(', ') + '.'));
    if (c.steps.length) body.append(UI.actionCard({ id: '05-brand-brain.connect.' + c.category, title: 'Connect a ' + pretty(c.category) + ' source', why: c.verdict.reason + '.', severity: c.verdict.kind === 'stop' ? 'high' : 'medium', owner: 'person', capability: { id: 'BRN-C02', autonomy: 'human_assist' }, artefact: { kind: 'connector_setup', label: 'one ' + pretty(c.category) + ' source connected, read-only' }, steps: c.steps, finding_ids: [], time_to_ship_hours: 1 }, { screen: SCREEN, expanded: true }));
    else body.append(el('div', { class: 'small muted', text: 'Connected via ' + c.via.join(', ') + '. Pull details are in the sources tab.' }));
    UI.panel({ title: pretty(c.category) + ' connectors', body });
  }
  function connectorsTable(cn) {
    const rows = cn.categories.map((c) => Object.assign({}, c, { via_text: (c.via.slice(0, 2).map((v) => v.replace(/\s*\(.*\)\s*/g, '')).join(', ') + (c.via.length > 2 ? ' +' + (c.via.length - 2) : '')) || (c.alternatives.every((a) => a.access === 'public') ? 'not pulled' : 'none'), fills_text: c.fills_sections.slice(0, 4).map(pretty).join(', ') + (c.fills_sections.length > 4 ? ' +' + (c.fills_sections.length - 4) : ''), rooms_n: c.unblocks_rooms.length, age: c.connected ? c.age_days : null }));
    return UI.verdictTable({
      columns: [
        { key: 'label', label: 'Category' },
        { key: 'via_text', label: 'Connected via' },
        { key: 'sources', label: 'Options', unit: 'n', align: 'right' },
        { key: 'fills_text', label: 'Fills' },
        { key: 'rooms_n', label: 'Rooms it unblocks', unit: 'n', align: 'right' },
        { key: 'age', label: 'Last pull', unit: 'days', align: 'right' },
      ],
      verdict: { at: 1, kind: (r) => r.verdict.kind, text: (r) => r.verdict.text, reason: (r) => r.verdict.reason },
      actions: { label: (r) => r.connected ? 'Open' : 'Connect', onClick: (r) => connectPanel(r) },
      rows, sort: false, maxRows: 30,
    });
  }
  function sourcesTable(cn) {
    return UI.verdictTable({
      columns: [
        { key: 'name', label: 'Source' }, { key: 'category', label: 'Category', format: pretty }, { key: 'access', label: 'Access', format: pretty },
        { key: 'pulls', label: 'Pulls', unit: 'n', align: 'right' }, { key: 'failed', label: 'Failed', unit: 'n', align: 'right' },
        { key: 'health', label: 'Health', unit: '%', align: 'right' }, { key: 'age_days', label: 'Last pull', unit: 'days', align: 'right' },
        { key: 'fills', label: 'Fills', format: (v, r) => r.fills_sections.slice(0, 3).map(pretty).join(', ') + (r.fills_sections.length > 3 ? ' +' + (r.fills_sections.length - 3) : '') },
      ],
      verdict: { at: 1, kind: (r) => r.verdict.kind, text: (r) => r.verdict.text, reason: (r) => r.verdict.reason },
      rows: cn.sources, sort: false, maxRows: 100,
    });
  }

  async function loadHealth() {
    let h, actions = [];
    try { h = await api(BASE + 'health'); } catch (e) { mount('#health', el('p', { class: 'muted', text: 'Health unavailable: ' + e.message })); return null; }
    try { const r = await api(BASE + 'rank'); actions = r.actions || []; } catch (e) { actions = []; }
    const byAct = {};
    for (const a of actions) if (a.entity && /^section_/.test(a.entity.id) && /BRN-R(01|02|11)/.test(a.rule_id || '')) { const k = a.entity.id.replace(/^section_/, ''); if (!byAct[k] || a.rule_id === 'BRN-R11') byAct[k] = a; }
    const emptyRows = new Set(h.sections.filter((s) => !s.records && s.verdict.kind !== 'ok').map((s) => s.section));
    mount('#health-tools', UI.orientation([
      { label: 'sections', value: h.counts.sections, unit: 'n' }, { label: 'need an action', value: h.counts.weak, unit: 'n', tone: h.counts.weak ? 'bad' : 'good' },
      { label: 'connect', value: h.counts.by_kind.connect, unit: 'n' }, { label: 'ask', value: h.counts.by_kind.ask, unit: 'n' }, { label: 're-crawl', value: h.counts.by_kind.recrawl, unit: 'n' },
      { label: 'records', value: h.records, unit: 'n' }, { label: 'approved or backed', value: h.strong_share, unit: '%' }]));
    const matrix = UI.coverageMatrix({
      rows: h.rows, cols: h.cols, cells: h.cells, unit: 'n', single: true, max: Math.min(h.max, 60), corner: 'Section by tier',
      gapRule: (cell, row, col) => (!cell && col.key === 'approved' && emptyRows.has(row.key) ? 'gap' : (cell && (col.key === 'inferred' || col.key === 'unverified') && cell.us > 0 ? 'over' : (col.key === 'forbidden' && cell && cell.us ? 'gap' : ''))),
      action: { label: 'Review', onClick: (cell, row, col) => { if (cell) cellPanel(row.key, col.key); else { const s = h.sections.find((x) => x.section === row.key); if (s) sectionPanel(s, byAct[row.key]); } } },
      onCell: (cell, row, col) => { if (cell) cellPanel(row.key, col.key); },
      note: h.note + ' Amber cells are inferred or unverified records a founder can settle. Colour scale caps at 60 so the language bank does not wash out the rest.',
    });
    const cn = h.connectors || { categories: [], sources: [], counts: {} };
    mount('#health', UI.tabs({ items: [
      { key: 'actions', label: 'Sections and actions', n: h.counts.weak, panel: () => healthTable(h, byAct) },
      { key: 'heat', label: 'Heatmap by tier', panel: () => matrix },
      { key: 'connectors', label: 'Connectors', n: cn.counts.connected, panel: () => el('div', { class: 'stack' },
        UI.orientation([{ label: 'connected', value: cn.counts.connected, unit: 'n' }, { label: 'categories live', value: cn.counts.categories_with_a_connection, unit: 'n', title: 'of ' + cn.categories.length }, { label: 'pull health', value: cn.health_pct, unit: '%', title: 'successful pulls over all pulls, public sources' }, { label: 'sources on offer', value: cn.counts.sources, unit: 'n' }]),
        connectorsTable(cn), el('div', { class: 'micro faint', text: cn.note })) },
      { key: 'sources', label: 'All sources', n: cn.counts.sources, panel: () => sourcesTable(cn) },
    ], current: h.counts.weak ? 'actions' : 'heat' }));
    return h;
  }

  // ---------- 5b. the desk (round 0 blocks, restyled) ----------
  function recordCard(r) {
    const card = el('article', { class: 'card flat rec' });
    card.append(el('div', { class: 'meta' }, tierChip(r.tier), el('span', { class: 'chip mono', text: r.id }),
      el('span', { text: r.date === 'undated' ? 'undated' : fmt.date(r.date) }),
      el('span', { text: 'confidence ' + (r.confidence == null ? NA : r.confidence) }),
      r.status !== 'active' ? el('span', { class: 'chip warn', text: r.status }) : null));
    card.append(el('div', { text: r.text || '' }));
    card.append(el('div', { class: 'meta' }, sourceLink(r.source), el('button', { class: 'btn xs soft', type: 'button', text: 'History', onclick: () => historyPanel(r.id, () => openSection(r.id.split('.')[1])) }), el('button', { class: 'btn xs soft', type: 'button', text: 'Where used', onclick: () => tracePanel(r.id) })));
    for (const e of (r.evidence || []).slice(0, 3)) card.append(el('blockquote', { text: '"' + e.quote + '"' }));
    return card;
  }

  async function openSection(name) {
    const wrap = document.getElementById('browser-wrap');
    wrap.hidden = false;
    document.getElementById('browser-title').textContent = 'Records in ' + pretty(name);
    mount('#browser', el('p', { class: 'muted', text: 'Loading.' }));
    try {
      const d = await api(BASE + 'records?section=' + encodeURIComponent(name));
      mount('#browser', ...(d.records.length ? d.records.map(recordCard) : [el('p', { class: 'muted', text: 'No records in this section yet.' })]));
    } catch (e) { mount('#browser', el('p', { class: 'muted', text: 'Could not load: ' + e.message })); }
    wrap.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function sectionsTable(rows) {
    return UI.verdictTable({
      columns: [
        { key: 'section', label: 'Section', format: (v, r) => pretty(v) + (r.meta ? ' (system)' : '') },
        { key: 'records', label: 'Records', align: 'right' },
        { key: 'freshness_days', label: 'Days since update', align: 'right', format: (v, r) => v == null ? (r.records ? 'undated' : 'no records') : String(v) },
        { key: 'stale', label: 'Stale', align: 'right' },
        { key: 'confidence', label: 'Confidence', align: 'right', format: (v) => v == null ? NA : v.toFixed(2) },
      ],
      verdict: { at: 1, kind: (r) => !r.records ? 'na' : r.stale ? 'fix' : (r.freshness_days != null && r.freshness_days > 90) ? 'watch' : 'keep', text: (r) => !r.records ? 'Empty' : r.stale ? 'Stale' : (r.freshness_days != null && r.freshness_days > 90) ? 'Ageing' : 'Fresh', reason: (r) => r.stale + ' stale of ' + r.records },
      rows, sort: { key: 'records', dir: 'desc' }, onRow: (r) => openSection(r.section),
    });
  }

  function ladderCard(l) {
    const card = el('article', { class: 'card ladder' });
    card.append(el('div', { class: 'row' }, el('b', { text: pretty(l.theme) }), el('span', { class: 'chip mono', text: l.id })));
    const rungs = el('div', { class: 'rungs' });
    for (const r of l.rungs) {
      const noProof = !r.proof_ids.length;
      const c = r.counts || {};
      const box = el('div', { class: 'rung' + (noProof ? ' noproof' : '') });
      box.append(el('div', { class: 'doubt', text: 'Rung ' + r.level + ': ' + r.doubt }));
      box.append(el('div', { class: 'meta' },
        el('span', { text: (c.one_star == null ? NA : c.one_star) + ' one-star' }),
        el('span', { text: (c.five_star == null ? NA : c.five_star) + ' five-star' }),
        ...r.uses.map((u) => el('span', { class: 'chip', text: pretty(u) }))));
      for (const q of r.one_star) box.append(el('blockquote', { text: '"' + q + '"' }));
      box.append(el('div', { class: 'meta' }, el('span', { class: 'chip ' + (noProof ? 'bad' : 'good'), text: noProof ? 'no proof' : 'proof' }),
        el('span', { text: r.proof || '' })));
      rungs.append(box);
    }
    card.append(rungs);
    return card;
  }

  // ---------- 5e. open questions, ranked ----------
  function questionCard(q, reload) {
    const card = el('article', { class: 'card flat rec question' + (q.answered_on ? ' settled' : '') });
    card.append(el('div', { class: 'meta' }, el('span', { class: 'chip ' + (q.weight >= 8 ? 'bad' : ''), text: 'weight ' + q.weight }),
      el('span', { class: 'chip accent', text: 'unblocks ' + q.rooms.length + ' rooms' }), el('span', { class: 'chip mono', text: q.fills[0] }),
      q.kind === 'bank' && q.connect.length ? el('span', { class: 'chip', text: 'pull first' }) : null,
      q.answered_on ? el('span', { class: 'chip good', text: 'answered ' + fmt.date(q.answered_on) }) : null));
    card.append(el('div', { class: 'q' , text: q.question }));
    if (q.why) card.append(el('div', { class: 'muted small', text: q.why[0].toUpperCase() + q.why.slice(1) + '.' }));
    card.append(el('div', { class: 'small', text: q.hint }));
    card.append(el('div', { class: 'row rooms' }, el('span', { class: 'micro faint', text: 'Unblocks:' }), ...q.screens.map((sc) => el('a', { class: 'chip mono', href: '/screens/' + sc + '/', target: '_blank', rel: 'noopener', text: sc }))));
    if (q.answered_on) { card.append(el('div', { class: 'muted small', text: 'Saved as ' + q.answer_record })); return card; }
    const input = el('input', { type: 'text', placeholder: 'Your answer in a line', 'aria-label': 'Answer: ' + q.question });
    const btn = el('button', { class: 'btn primary sm', type: 'button', text: 'Save answer' });
    const status = el('span', { class: 'muted small' });
    btn.addEventListener('click', async () => {
      if (!input.value.trim()) { status.textContent = 'Type an answer first.'; return; }
      btn.disabled = true;
      try {
        const url = q.kind === 'bank' ? BASE + 'questions/bank/' + encodeURIComponent(q.id) : BASE + 'questions/' + encodeURIComponent(q.field);
        const res = await api(url, { method: 'POST', body: { answer: input.value } });
        status.textContent = 'Saved as ' + res.record + (res.unblocks ? '. Unblocks ' + res.unblocks.map(pretty).join(', ') : '') + '.';
        reload();
      } catch (e) { btn.disabled = false; status.textContent = 'Could not save: ' + e.message; }
    });
    card.append(el('div', { class: 'answer' }, input, btn), status);
    return card;
  }
  async function loadQuestions() {
    let qv;
    try { qv = await api(BASE + 'questions'); } catch (e) { mount('#questions', el('p', { class: 'muted', text: 'Questions unavailable: ' + e.message })); return; }
    mount('#questions-tools', UI.orientation([
      { label: 'open', value: qv.counts.open, unit: 'n', tone: qv.counts.round_due ? 'bad' : null, title: 'a founder round is due at ' + qv.round_at },
      { label: 'answer by connecting', value: qv.counts.connect_first, unit: 'n' }, { label: 'rooms blocked', value: qv.counts.rooms_blocked, unit: 'n' }, { label: 'answered', value: qv.counts.answered, unit: 'n', tone: 'good' }]));
    const open = qv.questions.filter((q) => !q.answered_on);
    const done = qv.questions.filter((q) => q.answered_on);
    const items = open.slice(0, 5).map((q) => questionCard(q, loadQuestions));
    if (!open.length) items.push(el('p', { class: 'muted', text: 'Nothing waits on you. The next pull or audit may add a question.' }));
    if (open.length > 5) {
      const more = el('div', { class: 'grid', hidden: true });
      const btn = el('button', { class: 'btn sm', type: 'button', text: 'Show ' + (open.length - 5) + ' more' });
      btn.addEventListener('click', () => { more.hidden = !more.hidden; btn.textContent = more.hidden ? 'Show ' + (open.length - 5) + ' more' : 'Show the top 5 only'; if (!more.hidden && !more.children.length) mount(more, ...open.slice(5).map((q) => questionCard(q, loadQuestions))); });
      items.push(el('div', { class: 'row' }, btn), more);
    }
    if (done.length) {
      const list = el('div', { class: 'grid', hidden: true });
      const btn = el('button', { class: 'btn sm', type: 'button', text: 'Show ' + done.length + ' answered' });
      btn.addEventListener('click', () => { list.hidden = !list.hidden; btn.textContent = list.hidden ? 'Show ' + done.length + ' answered' : 'Hide answered'; if (!list.hidden && !list.children.length) mount(list, ...done.map((q) => questionCard(q, loadQuestions))); });
      items.push(el('div', { class: 'row' }, btn), list);
    }
    mount('#questions', ...items);
  }

  function reviewCard(r, reload) {
    const card = recordCard(r);
    const status = el('span', { class: 'muted small' });
    const act = (choice) => async () => {
      try { await api(BASE + 'review/' + encodeURIComponent(r.id), { method: 'POST', body: { choice } }); reload(); }
      catch (e) { status.textContent = 'Could not save: ' + e.message; }
    };
    const ok = el('button', { class: 'btn primary sm', type: 'button', text: 'Accept' });
    const no = el('button', { class: 'btn sm', type: 'button', text: 'Ignore' });
    ok.addEventListener('click', act('accept'));
    no.addEventListener('click', act('ignore'));
    card.append(el('div', { class: 'row' }, ok, no, status));
    return card;
  }

  // ---------- 5h. review queue with before and after, grouped, bulk ----------
  function proposalCard(r, reload) {
    const card = el('article', { class: 'card flat rec proposal' });
    card.append(el('div', { class: 'meta' }, el('span', { class: 'chip ' + (r.change === 'replaces' ? 'warn' : r.change === 'same value' ? '' : 'accent'), text: r.change }), el('span', { class: 'chip', text: pretty(r.section) }), tierChip(r.tier), el('span', { class: 'chip mono', text: r.id })));
    const vs = el('div', { class: 'vs' },
      el('div', null, el('div', { class: 'meta' }, el('span', { class: 'chip', text: 'before' }), r.before ? tierChip(r.before.tier) : null, r.before && r.before.date ? el('span', { text: fmt.date(r.before.date) }) : null), el('div', { text: r.before ? r.before.text : 'no record on this field yet' })),
      el('div', { class: 'kept' }, el('div', { class: 'meta' }, el('span', { class: 'chip accent', text: 'proposed' }), r.date ? el('span', { text: fmt.date(r.date) }) : null), el('div', { text: r.text || '' }), (r.evidence || []).length ? el('blockquote', { text: '"' + r.evidence[0].quote + '"' }) : null));
    card.append(vs);
    const status = el('span', { class: 'muted small' });
    const act = (choice) => async () => { try { await api(BASE + 'review/' + encodeURIComponent(r.id), { method: 'POST', body: { choice } }); reload(); } catch (e) { status.textContent = 'Could not save: ' + e.message; } };
    card.append(el('div', { class: 'row' }, el('button', { class: 'btn primary sm', type: 'button', text: 'Accept', onclick: act('accept') }), el('button', { class: 'btn sm', type: 'button', text: 'Ignore', onclick: act('ignore') }), status));
    return card;
  }
  async function loadReview() {
    let rv;
    try { rv = await api(BASE + 'review'); } catch (e) { mount('#review', el('p', { class: 'muted', text: 'Review queue unavailable: ' + e.message })); return; }
    mount('#review-tools', UI.orientation([{ label: 'proposed', value: rv.counts.proposed, unit: 'n', tone: rv.counts.proposed ? 'bad' : 'good' }, { label: 'sources', value: rv.counts.groups, unit: 'n' }, { label: 'new fields', value: rv.counts.new_fields, unit: 'n' }, { label: 'replacing', value: rv.counts.replacing, unit: 'n' }, { label: 'same value', value: rv.counts.duplicates, unit: 'n' }]));
    if (!rv.groups.length) { mount('#review', el('p', { class: 'muted', text: 'Nothing proposed. Agent updates and file extractions land here before they reach the brain.' })); return; }
    const groups = rv.groups.map((g) => {
      const status = el('span', { class: 'micro muted' });
      const bulk = (choice, ids) => async () => { try { const r = await api(BASE + 'review/bulk', { method: 'POST', body: { choice, ids } }); status.textContent = r.done.length + ' ' + choice + 'ed' + (r.failed.length ? ', ' + r.failed.length + ' failed' : '') + '.'; loadReview(); loadDesk(); loadDocs(); } catch (e) { status.textContent = 'Could not save: ' + e.message; } };
      const adds = g.records.filter((r) => r.change !== 'same value').map((r) => r.id);
      const dupes = g.records.filter((r) => r.change === 'same value').map((r) => r.id);
      const head = el('div', { class: 'sec-head' }, el('h4', { text: 'From ' + g.source + ' (' + pretty(g.type) + ')' }), el('div', { class: 'tools' },
        adds.length ? el('button', { class: 'btn sm primary', type: 'button', text: 'Accept ' + adds.length + ' that add something', onclick: bulk('accept', adds) }) : null,
        dupes.length ? el('button', { class: 'btn sm', type: 'button', text: 'Ignore ' + dupes.length + ' same value', onclick: bulk('ignore', dupes) }) : null,
        el('button', { class: 'btn sm quiet', type: 'button', text: 'Ignore all', onclick: bulk('ignore', g.records.map((r) => r.id)) }), status),
        el('span', { class: 'sub', text: g.records.length + ' proposed' + (g.date ? ', ' + fmt.date(g.date) : '') }));
      return el('div', { class: 'card tight review-group' }, head, el('div', { class: 'grid' }, ...g.records.map((r) => proposalCard(r, loadReview))));
    });
    mount('#review', ...groups, el('div', { class: 'micro faint', text: rv.note }));
  }

  // ---------- 5b1. contracts ----------
  function contractForm(cr, reload, preset) {
    const vendor = el('input', { class: 'text sm', placeholder: 'Vendor', value: preset ? preset.vendor : '', style: { maxWidth: '160px' } });
    const type = el('select', { class: 'text sm' }, ...cr.types.map((t) => el('option', { value: t, text: pretty(t), selected: preset && preset.type === t })));
    const date = el('input', { class: 'text sm', type: 'date', 'aria-label': 'Renewal date' });
    const notice = el('input', { class: 'text sm', type: 'number', placeholder: 'Notice days', style: { maxWidth: '110px' } });
    const rate = el('input', { class: 'text sm', placeholder: 'Rate card or last terms', style: { flex: '1 1 200px' } });
    const go = el('button', { class: 'btn sm primary', type: 'button', text: preset ? 'Save ' + preset.vendor : 'Add contract' });
    const status = el('span', { class: 'micro muted' });
    go.addEventListener('click', async () => {
      go.disabled = true;
      try { const r = await api(BASE + 'contracts', { method: 'POST', body: { vendor: vendor.value, type: type.value, renewal_date: date.value, notice_days: notice.value, rate_card: rate.value } }); status.textContent = 'Saved ' + r.record + '. Alert window ' + r.window_days + ' days.'; reload(); }
      catch (e) { go.disabled = false; status.textContent = 'Could not save: ' + e.message; }
    });
    return el('div', { class: 'row add-field' }, vendor, type, date, notice, rate, go, status);
  }
  function contractsTable(cr, byAct, reload) {
    const rows = cr.contracts.map((c) => Object.assign({}, c, { type_text: pretty(c.type), known: c.on_file ? 'on file' : 'from ' + (c.how || 'the brain') }));
    return UI.verdictTable({
      columns: [
        { key: 'vendor', label: 'Vendor' }, { key: 'type_text', label: 'Type' }, { key: 'renewal_date', label: 'Renews', format: (v) => v ? fmt.date(v) : NA },
        { key: 'days_left', label: 'Days left', unit: 'days', align: 'right' }, { key: 'window_days', label: 'Window', unit: 'days', align: 'right' }, { key: 'notice_days', label: 'Notice', unit: 'days', align: 'right' },
        { key: 'rate_card', label: 'Last terms', format: (v) => v || NA }, { key: 'known', label: 'Known from' },
      ],
      verdict: { at: 1, kind: (r) => r.verdict.kind, text: (r) => r.verdict.text, reason: (r) => r.verdict.reason },
      actions: { label: (r) => r.on_file && r.verdict.kind !== 'fix' ? 'Open' : 'Add', onClick: (r) => {
        const a = byAct['contract_' + r.slug] || (r.on_file ? null : byAct.contracts_missing);
        const body = el('div', { class: 'stack' }, el('div', { class: 'small muted', text: r.verdict.reason }), contractForm(cr, () => { reload(); }, r));
        if (a) body.append(UI.actionCard(a, { screen: SCREEN, expanded: true }));
        UI.panel({ title: r.vendor, body });
      } },
      rows, sort: false, maxRows: 40, empty: 'No vendors known yet. Add a contract below.',
    });
  }
  async function loadContracts() {
    let cr, actions = [];
    try { cr = await api(BASE + 'contracts'); } catch (e) { mount('#contracts', el('p', { class: 'muted', text: 'Contracts unavailable: ' + e.message })); return; }
    try { const r = await api(BASE + 'rank'); actions = (r.actions || []).filter((a) => /BRN-R1[78]/.test(a.rule_id || '')); } catch (e) { actions = []; }
    const byAct = {}; for (const a of actions) if (a.entity && a.entity.id) byAct[a.entity.id] = a;
    mount('#contracts-tools', UI.orientation([{ label: 'on file', value: cr.counts.on_file, unit: 'n' }, { label: 'inside the window', value: cr.counts.inside_window, unit: 'n', tone: cr.counts.inside_window ? 'bad' : 'good' }, { label: 'no date', value: cr.counts.no_date, unit: 'n' }, { label: 'known, no contract', value: cr.counts.known_without_contract, unit: 'n', tone: cr.counts.known_without_contract ? 'bad' : null },
      { label: 'next renewal', value: null, unit: 'n', unavailable_label: cr.next ? cr.next.vendor + ' in ' + cr.next.days_left + ' d' : 'none on file' }]));
    const cal = cr.calendar.length ? UI.table({ columns: [{ key: 'vendor', label: 'Vendor' }, { key: 'date', label: 'Renews', format: (v) => fmt.date(v) }, { key: 'days_left', label: 'Days left', unit: 'days', align: 'right' }, { key: 'window_days', label: 'Alert window', unit: 'days', align: 'right' }, { key: 'type', label: 'Type', format: pretty }], rows: cr.calendar, sort: false })
      : el('p', { class: 'muted small', text: 'No renewal within 12 months on file.' });
    mount('#contracts', UI.tabs({ items: [
      { key: 'register', label: 'Register', n: cr.contracts.length, panel: () => el('div', { class: 'stack' }, contractsTable(cr, byAct, loadContracts), contractForm(cr, loadContracts), el('div', { class: 'micro faint', text: cr.note })) },
      { key: 'calendar', label: 'Next 12 months', n: cr.calendar.length, panel: () => cal },
    ] }));
  }

  // ---------- 5b2. legal gate ----------
  function legalTable(lg, byAct) {
    const S = { pass: 'keep', fail: 'stop', unavailable: 'wait', na: 'na' };
    const T = { pass: 'Pass', fail: 'Fails', unavailable: 'Unavailable', na: 'Not applicable' };
    return UI.verdictTable({
      columns: [{ key: 'label', label: 'Check' }, { key: 'law', label: 'Rule family' }, { key: 'surface', label: 'Surface' }, { key: 'why', label: 'Evidence' }],
      verdict: { at: 1, kind: (r) => S[r.status], text: (r) => T[r.status], reason: (r) => r.why },
      rows: lg.checks.map((c) => Object.assign({}, c, { actions: c.status === 'fail' ? [{ label: 'Fix', cls: 'primary', onClick: () => { const a = byAct[c.key]; UI.panel({ title: c.label, body: a ? UI.actionCard(a, { screen: SCREEN, expanded: true }) : el('p', { text: c.action.title }) }); } }] : (c.evidence.length && /^https?:/.test(c.evidence[c.evidence.length - 1]) ? [{ label: 'Open page', onClick: () => window.open(c.evidence[c.evidence.length - 1], '_blank', 'noopener') }] : []) })),
      actions: { label: 'Do' }, sort: false, maxRows: 20,
    });
  }
  function gateBox(lg) {
    const kind = el('select', { class: 'text sm' }, ...lg.kinds.map((k) => el('option', { value: k, text: k === 'pdp' ? 'Product page' : pretty(k) })));
    const ta = el('textarea', { class: 'text', rows: 5, placeholder: 'Paste the email, ad, product page, policy or subscription terms.' });
    const out = el('div', { class: 'stack' });
    const btn = el('button', { class: 'btn primary sm', type: 'button', text: 'Run the gate' });
    btn.addEventListener('click', async () => {
      if (!ta.value.trim()) { mount(out, el('p', { class: 'muted small', text: 'Paste a draft first.' })); return; }
      btn.disabled = true;
      try {
        const r = await api(BASE + 'legal/gate', { method: 'POST', body: { kind: kind.value, text: ta.value } });
        const head = el('div', { class: 'row' }, UI.verdict(r.verdict === 'pass' ? 'keep' : r.verdict === 'warn' ? 'watch' : 'stop', r.verdict === 'pass' ? 'Can ship' : r.verdict === 'warn' ? 'Check first' : 'Blocked', r.blocking + ' blocking'));
        const rows = r.missing.map((m) => ({ level: 'blocks', what: 'missing ' + m.label, fix: m.fix })).concat(((r.claims && r.claims.hits) || []).map((h) => ({ level: h.severity === 'fail' ? 'blocks' : 'warning', what: pretty(h.kind) + ': ' + h.match, fix: h.fix })));
        mount(out, head, rows.length ? UI.table({ columns: [{ key: 'level', label: 'Level' }, { key: 'what', label: 'What' }, { key: 'fix', label: 'Fix' }], rows, sort: false }) : el('p', { class: 'muted small', text: 'Nothing missing for this kind. ' + r.present.map((p) => p.label).join('; ') + '.' }));
      } catch (e) { mount(out, el('p', { class: 'muted', text: 'Could not check: ' + e.message })); }
      btn.disabled = false;
    });
    return el('div', { class: 'stack scanner' }, el('div', { class: 'row' }, el('span', { class: 'small muted', text: 'Kind:' }), kind), ta, el('div', { class: 'row' }, btn, el('span', { class: 'micro faint', text: 'Rules only, not legal advice. The claims scanner runs on the same text.' })), out);
  }
  async function loadLegal() {
    let lg, actions = [];
    try { lg = await api(BASE + 'legal'); } catch (e) { mount('#legal', el('p', { class: 'muted', text: 'Legal checks unavailable: ' + e.message })); return; }
    try { const r = await api(BASE + 'rank'); actions = (r.actions || []).filter((a) => a.rule_id === 'BRN-R19'); } catch (e) { actions = []; }
    const byAct = {}; for (const a of actions) if (a.entity && a.entity.id) byAct[a.entity.id] = a;
    mount('#legal-tools', UI.orientation([{ label: 'pass', value: lg.counts.pass, unit: 'n', tone: 'good' }, { label: 'fail', value: lg.counts.fail, unit: 'n', tone: lg.counts.fail ? 'bad' : null }, { label: 'unavailable', value: lg.counts.unavailable, unit: 'n' }, { label: 'pass rate', value: lg.pass_rate, unit: '%', title: 'of the checks the brain can read' }]));
    mount('#legal', UI.tabs({ items: [
      { key: 'checks', label: 'Site checks', n: lg.checked, panel: () => el('div', { class: 'stack' }, legalTable(lg, byAct), el('div', { class: 'micro faint', text: lg.note })) },
      { key: 'gate', label: 'Gate a draft', panel: () => gateBox(lg) },
    ] }));
  }

  // ---------- 5c0. marketplace parity ----------
  function parityInputs(pv, reload) {
    const map = el('input', { class: 'text sm', placeholder: pv.map_usd_per_pair != null ? '$' + pv.map_usd_per_pair + ' a pair' : 'MAP per pair, like 12.50', style: { maxWidth: '180px' } });
    const sellers = el('input', { class: 'text sm', placeholder: pv.our_sellers ? pv.our_sellers.join(', ') : 'Your seller names, comma separated', style: { flex: '1 1 260px' } });
    const status = el('span', { class: 'micro muted' });
    const save = (what, body) => async () => { try { const r = await api(BASE + 'parity/' + what, { method: 'POST', body }); status.textContent = 'Saved ' + r.record + '.'; reload(); } catch (e) { status.textContent = 'Could not save: ' + e.message; } };
    return el('div', { class: 'row add-field' }, map, el('button', { class: 'btn sm primary', type: 'button', text: 'Set MAP', onclick: () => save('map', { usd: map.value })() }),
      sellers, el('button', { class: 'btn sm', type: 'button', text: 'Set seller names', onclick: () => save('sellers', { names: sellers.value })() }), status);
  }
  function parityTable(pv, byAct) {
    const rows = pv.listings.map((l) => Object.assign({}, l, { flags_text: l.flags.map((f) => f.text).join('; '), title_short: l.title.length > 60 ? l.title.slice(0, 57) + '...' : l.title }));
    return UI.verdictTable({
      columns: [
        { key: 'title_short', label: 'Listing' }, { key: 'asin', label: 'ASIN' }, { key: 'line', label: 'Line', format: (v) => v ? pretty(v) : NA }, { key: 'pack', label: 'Pack', unit: 'n', align: 'right' },
        { key: 'price_usd', label: 'Price', unit: '$', align: 'right' }, { key: 'per_pair_usd', label: 'Per pair', unit: '$', align: 'right' }, { key: 'site_floor_usd', label: 'Site floor', unit: '$', align: 'right' },
        { key: 'gap_pct', label: 'Gap', unit: '%', align: 'right', format: (v) => v == null ? NA : (v > 0 ? '+' : '') + v + '%' }, { key: 'seller', label: 'Seller', format: (v) => v || NA }, { key: 'stars', label: 'Stars', align: 'right' }, { key: 'reviews', label: 'Reviews', unit: 'n', align: 'right' },
      ],
      verdict: { at: 1, kind: (r) => r.verdict.kind, text: (r) => r.verdict.text, reason: (r) => r.verdict.reason },
      actions: { label: (r) => byAct[r.asin] ? 'Act' : 'Open', onClick: (r) => { const a = byAct[r.asin]; if (a) UI.panel({ title: r.title, body: UI.actionCard(a, { screen: SCREEN, expanded: true }) }); else window.open(r.url, '_blank', 'noopener'); } },
      rows, sort: false, maxRows: 60, empty: 'No marketplace listings in the brain yet.',
    });
  }
  async function loadParity() {
    let pv, actions = [];
    try { pv = await api(BASE + 'parity'); } catch (e) { mount('#parity', el('p', { class: 'muted', text: 'Parity unavailable: ' + e.message })); return; }
    try { const r = await api(BASE + 'rank'); actions = (r.actions || []).filter((a) => /BRN-R1[56]/.test(a.rule_id || '')); } catch (e) { actions = []; }
    const byAct = {}; for (const a of actions) if (a.entity && a.entity.type === 'sku') byAct[a.entity.id] = a;
    const c = pv.counts;
    mount('#parity-tools', UI.orientation([{ label: 'listings', value: c.listings, unit: 'n' }, { label: 'under the site', value: c.under_site, unit: 'n', tone: c.under_site ? 'bad' : 'good' }, { label: 'below MAP', value: c.below_map, unit: 'n' }, { label: 'seller unknown', value: c.seller_unknown, unit: 'n' }, { label: 'unrecognised seller', value: c.unrecognised, unit: 'n' }, { label: 'MAP', value: pv.map_usd_per_pair, unit: '$' }]));
    const connect = actions.filter((a) => a.status === 'unavailable').map((a) => UI.actionCard(a, { screen: SCREEN, compact: true }));
    mount('#parity', parityTable(pv, byAct), parityInputs(pv, loadParity), ...connect, el('div', { class: 'micro faint', text: pv.note }));
  }

  // ---------- 5c1. site diff between crawls ----------
  function changeCard(c, reload, byAct) {
    const a = byAct['change_' + c.section + '_' + (c.field || 'x')];
    const card = el('article', { class: 'card flat rec change' + (c.reviewed ? ' settled' : '') });
    card.append(el('div', { class: 'meta' }, UI.sevChip(c.severity), el('span', { class: 'chip mono', text: c.section + '.' + (c.field || '') }), el('span', { class: 'chip', text: c.change }),
      el('span', { text: c.captured_at ? 'seen ' + fmt.date(c.captured_at) : '' }), c.reviewed ? el('span', { class: 'chip good', text: 'reviewed ' + fmt.date(c.reviewed.at) }) : el('span', { class: 'chip warn', text: 'open' })));
    const vs = el('div', { class: 'vs' }, el('div', null, el('div', { class: 'meta' }, el('span', { class: 'chip', text: 'before' })), el('b', { text: c.old_text == null ? 'not on the site' : c.old_text })),
      el('div', { class: 'kept' }, el('div', { class: 'meta' }, el('span', { class: 'chip accent', text: 'now' })), el('b', { text: c.new_text == null ? 'gone' : c.new_text })));
    card.append(vs);
    if (c.ref) card.append(el('div', { class: 'meta' }, el('a', { href: c.ref, target: '_blank', rel: 'noopener', text: c.ref.replace(/^https?:\/\//, '') })));
    if (a) card.append(UI.actionCard(a, { screen: SCREEN, compact: true }));
    else card.append(el('div', { class: 'small' }, el('b', { text: c.action.title + '. ' }), 'Owner: ' + pretty(c.action.owner) + '. ' + c.action.steps.map((st) => st.n + '. ' + st.text).join(' ')));
    if (!c.reviewed) {
      const btn = el('button', { class: 'btn sm', type: 'button', text: 'Mark reviewed' });
      const status = el('span', { class: 'micro muted' });
      btn.addEventListener('click', async () => { btn.disabled = true; try { await api(BASE + 'site/reviewed', { method: 'POST', body: { ids: [c.id] } }); reload(); } catch (e) { btn.disabled = false; status.textContent = 'Could not save: ' + e.message; } });
      card.append(el('div', { class: 'row' }, btn, status));
    }
    return card;
  }
  async function loadSite() {
    let sd, actions = [];
    try { sd = await api(BASE + 'site/diff'); } catch (e) { mount('#site', el('p', { class: 'muted', text: 'Site diff unavailable: ' + e.message })); return; }
    try { const r = await api(BASE + 'rank'); actions = (r.actions || []).filter((a) => a.rule_id === 'BRN-R14'); } catch (e) { actions = []; }
    const byAct = {}; for (const a of actions) if (a.entity && a.entity.id) byAct[a.entity.id] = a;
    const last = sd.snapshots.length ? sd.snapshots[sd.snapshots.length - 1] : null;
    mount('#site-tools', UI.orientation([{ label: 'snapshots', value: sd.snapshots.length, unit: 'n' }, { label: 'last crawl', value: null, unit: 'n', unavailable_label: last ? fmt.date(last.date) : 'none' },
      { label: 'changes', value: sd.counts.changes, unit: 'n' }, { label: 'open', value: sd.counts.open, unit: 'n', tone: sd.counts.open ? 'bad' : (sd.counts.open === 0 ? 'good' : null) }, { label: 'high', value: sd.counts.high, unit: 'n' }]));
    const snapBtn = el('button', { class: 'btn sm', type: 'button', text: 'Snapshot the crawl on file' });
    const status = el('span', { class: 'micro muted' });
    snapBtn.addEventListener('click', async () => { snapBtn.disabled = true; try { const r = await api(BASE + 'site/snapshot', { method: 'POST', body: {} }); status.textContent = 'Snapshot ' + r.date + ', ' + r.records + ' records.'; loadSite(); } catch (e) { snapBtn.disabled = false; status.textContent = 'Could not snapshot: ' + e.message; } });
    const crawl = UI.decisionRow({ capability: 'BRN-C01', autonomy: 'agent_does', owner: 'agent', screen: SCREEN, compact: true, stub: 'Runs the site extractor read-only (1 request a second, robots honoured, 20 pages), writes raw/a-site, then a dated snapshot. The diff against the last snapshot appears here.' });
    const tools = el('div', { class: 'row' }, snapBtn, status, el('span', { class: 'micro faint', text: 'Re-crawl:' }), crawl);
    const items = [];
    if (sd.unavailable_reason) items.push(el('p', { class: 'muted', text: NA + ': ' + sd.unavailable_reason }));
    else {
      items.push(el('div', { class: 'small muted', text: 'Comparing ' + fmt.date(sd.old) + ' with ' + fmt.date(sd.new) + '. ' + Object.entries(sd.counts.by_section || {}).map(([k, v]) => pretty(k) + ' ' + v).join(', ') + '.' }));
      const open = sd.changes.filter((c) => !c.reviewed), done = sd.changes.filter((c) => c.reviewed);
      items.push(el('div', { class: 'grid' }, ...open.map((c) => changeCard(c, loadSite, byAct))));
      if (!open.length) items.push(el('p', { class: 'muted', text: 'Every change is reviewed.' }));
      if (done.length) { const list = el('div', { class: 'grid', hidden: true }); const btn = el('button', { class: 'btn sm', type: 'button', text: 'Show ' + done.length + ' reviewed' }); btn.addEventListener('click', () => { list.hidden = !list.hidden; btn.textContent = list.hidden ? 'Show ' + done.length + ' reviewed' : 'Hide reviewed'; if (!list.hidden && !list.children.length) mount(list, ...done.map((c) => changeCard(c, loadSite, byAct))); }); items.push(el('div', { class: 'row' }, btn), list); }
    }
    items.push(tools, el('div', { class: 'micro faint', text: sd.note }));
    mount('#site', ...items);
  }

  // ---------- 5g. what an agent reads ----------
  function packageBox() {
    const input = el('input', { class: 'text sm', placeholder: 'Capability id, like CREA-C06', value: 'CREA-C06', style: { maxWidth: '200px' } });
    const btn = el('button', { class: 'btn sm primary', type: 'button', text: 'Show the package' });
    const out = el('div', { class: 'stack' });
    btn.addEventListener('click', async () => {
      btn.disabled = true;
      try {
        const p = await api(BASE + 'package?capability=' + encodeURIComponent(input.value.trim().toUpperCase()));
        mount(out, el('div', { class: 'row' }, el('b', { text: p.capability + (p.name ? ': ' + p.name : '') }), el('span', { class: 'chip ' + (p.share > 0.9 ? 'warn' : ''), text: p.tokens + ' of ' + p.budget + ' tokens' }), p.public_facing ? el('span', { class: 'chip', text: 'public facing: private records left out' }) : null, el('span', { class: 'chip', text: p.records + ' T2 records' }), UI.copyButton({ label: 'Copy the package', text: () => p.text })),
          UI.table({ columns: [{ key: 'tier', label: 'Tier' }, { key: 'section', label: 'Section', format: (v) => v ? pretty(v) : 'brand card' }, { key: 'tokens', label: 'Tokens', unit: 'n', align: 'right' }, { key: 'text', label: 'Text', format: (v) => v.length > 160 ? v.slice(0, 157) + '...' : v }], rows: p.parts, sort: false }),
          el('pre', { class: 'card sunken brief', text: p.text }));
      } catch (e) { mount(out, el('p', { class: 'muted', text: 'Could not build: ' + e.message })); }
      btn.disabled = false;
    });
    return el('div', { class: 'stack' }, el('div', { class: 'row' }, input, btn, el('span', { class: 'micro faint', text: 'Any capability id from the catalogue with brain sections in the overlay.' })), out);
  }
  async function loadPackage() {
    let sm;
    try { sm = await api(BASE + 'summaries'); } catch (e) { mount('#package', el('p', { class: 'muted', text: 'Summaries unavailable: ' + e.message })); return; }
    mount('#package-tools', UI.orientation([{ label: 'brand card', value: sm.t0_tokens, unit: 'n', title: 'tokens' }, { label: 'summaries', value: sm.sections.length, unit: 'n' }, { label: 'all summaries', value: sm.total_tokens, unit: 'n', title: 'tokens if every section were loaded' }]));
    mount('#package', UI.tabs({ items: [
      { key: 'summaries', label: 'Summary per section', n: sm.sections.length, panel: () => UI.table({ columns: [{ key: 'label', label: 'Section' }, { key: 'records', label: 'Records', unit: 'n', align: 'right' }, { key: 'tokens', label: 'Tokens', unit: 'n', align: 'right' }, { key: 'text', label: 'What an agent reads', format: (v) => v.replace(/\nCites:.*$/s, '').replace(/^## /, '') }], rows: sm.sections, sort: false, maxRows: 40 }) },
      { key: 'package', label: 'Package for a capability', panel: packageBox },
    ] }), el('div', { class: 'micro faint', text: sm.note }));
  }

  // ---------- 5c2b. store facts for AI shopping agents ----------
  function factPanel(r, reload) {
    const q = el('input', { class: 'text sm', value: r.question, 'aria-label': 'Question' });
    const ta = el('textarea', { class: 'text', rows: 3 }); ta.value = r.approved || r.generated || '';
    const status = el('span', { class: 'micro muted' });
    const go = el('button', { class: 'btn primary sm', type: 'button', text: 'Approve this answer' });
    const body = el('div', { class: 'stack' }, r.status === 'stale' ? el('div', { class: 'card sunken small' }, el('b', { text: 'Stale: ' }), r.reason + '. Built from the records now: ' + r.generated) : el('div', { class: 'small muted', text: r.reason + (r.records.length ? '. Built from ' + r.records.join(', ') : '') }), q, ta, el('div', { class: 'row' }, go, status));
    const panel = UI.panel({ title: 'Store fact: ' + pretty(r.key), body });
    go.addEventListener('click', async () => { go.disabled = true; try { await api(BASE + 'facts/' + r.key, { method: 'POST', body: { question: q.value.trim(), answer: ta.value.trim() } }); panel.close(); reload(); } catch (e) { go.disabled = false; status.textContent = 'Could not save: ' + e.message; } });
  }
  async function loadFacts() {
    let fp;
    try { fp = await api(BASE + 'facts'); } catch (e) { mount('#facts', el('p', { class: 'muted', text: 'Store facts unavailable: ' + e.message })); return; }
    const S = { approved: 'keep', proposed: 'watch', stale: 'stop', unavailable: 'wait' };
    const T = { approved: 'Approved', proposed: 'Proposed', stale: 'Stale', unavailable: 'Unavailable' };
    mount('#facts-tools', UI.orientation([{ label: 'approved', value: fp.counts.approved, unit: 'n', tone: 'good' }, { label: 'proposed', value: fp.counts.proposed, unit: 'n' }, { label: 'stale', value: fp.counts.stale, unit: 'n', tone: fp.counts.stale ? 'bad' : null }, { label: 'unanswered', value: fp.counts.unavailable, unit: 'n' }]));
    const exp = el('button', { class: 'btn sm', type: 'button', text: 'Copy FAQ JSON-LD' });
    const expT = el('button', { class: 'btn sm', type: 'button', text: 'Copy as text' });
    const st = el('span', { class: 'micro muted' });
    const doExport = (kind) => async () => { try { const e = await api(BASE + 'facts/export'); const text = kind === 'json' ? JSON.stringify(e.jsonld, null, 1) : e.text; await navigator.clipboard.writeText(text); st.textContent = e.count + ' approved pairs copied. ' + e.note; } catch (err) { st.textContent = 'Could not export: ' + err.message; } };
    exp.addEventListener('click', doExport('json')); expT.addEventListener('click', doExport('text'));
    mount('#facts', UI.verdictTable({
      columns: [{ key: 'question', label: 'Question' }, { key: 'answer', label: 'Answer', format: (v) => v || NA }, { key: 'recs', label: 'Built from', format: (v, r) => r.records.length + (r.records.length === 1 ? ' record' : ' records') }],
      verdict: { at: 1, kind: (r) => S[r.status], text: (r) => T[r.status], reason: (r) => r.reason },
      actions: { label: (r) => r.status === 'approved' ? 'Edit' : (r.status === 'unavailable' ? 'Answer it' : 'Approve'), onClick: (r) => factPanel(r, loadFacts) },
      rows: fp.pairs, sort: false, maxRows: 20,
    }), el('div', { class: 'row', style: { marginTop: '8px' } }, exp, expT, UI.decisionRow({ capability: 'LOOP-C38', autonomy: 'agent_does', owner: 'agent', screen: SCREEN, compact: true, stub: 'The agent asks 3 public AI shopping assistants the same questions about the brand and compares their answers with these approved facts and the claims tiers. Differences land here as findings.' }), st), el('div', { class: 'micro faint', text: fp.note }));
  }

  // ---------- 5c3. how we write: voice sheet and snippets ----------
  function voiceFields(vs, reload) {
    const wrap = el('div', { class: 'profile-sec' });
    for (const f of vs.fields) {
      wrap.append(UI.field({ key: f.key, name: f.label, sub: f.text ? null : 'for example: ' + f.example, text: f.text, tier: f.tier, source: f.record ? f.record : null, date: f.date, multiline: f.key.endsWith('_list') || f.key === 'tone_by_context',
        placeholder: 'unavailable. Add it and every writing agent reads it.',
        onSave: async (text) => api(BASE + 'profile/voice/' + encodeURIComponent(f.key), { method: 'POST', body: { text } }), onSaved: reload }));
    }
    return wrap;
  }
  function exampleBox(kind, vs, reload) {
    const list = el('div', { class: 'grid' }, ...vs.examples[kind].map((e) => el('div', { class: 'card flat rec' }, el('div', { text: e.text }), el('div', { class: 'meta' }, e.why ? el('span', { text: 'why: ' + e.why }) : null, el('span', { class: 'chip mono', text: e.id }), e.date ? el('span', { text: fmt.date(e.date) }) : null))));
    const ta = el('textarea', { class: 'text', rows: 2, placeholder: kind === 'liked' ? 'Paste copy you love' : 'Paste copy you would never run' });
    const why = el('input', { class: 'text sm', placeholder: 'Why, in a few words', style: { flex: '1 1 200px' } });
    const btn = el('button', { class: 'btn sm ' + (kind === 'liked' ? 'primary' : 'danger'), type: 'button', text: kind === 'liked' ? 'Add as liked' : 'Add as disliked' });
    const status = el('span', { class: 'micro muted' });
    btn.addEventListener('click', async () => { if (!ta.value.trim()) { status.textContent = 'Paste it first.'; return; } btn.disabled = true; try { const r = await api(BASE + 'voice/example', { method: 'POST', body: { kind, text: ta.value.trim(), why: why.value.trim() } }); status.textContent = 'Saved ' + r.record + '.'; reload(); } catch (e) { btn.disabled = false; status.textContent = 'Could not save: ' + e.message; } });
    return el('div', { class: 'stack' }, el('h4', { text: (kind === 'liked' ? 'Copy we like' : 'Copy we do not like') + ' (' + vs.examples[kind].length + (kind === 'liked' ? ' of ' + vs.examples_needed + ' needed' : '') + ')' }), list, ta, el('div', { class: 'row' }, why, btn, status));
  }
  function snippetsTable(sn, reload) {
    const S = { locked: 'keep', proposed: 'watch', stale: 'stop', unavailable: 'na' };
    const T = { locked: 'Locked', proposed: 'Proposed', stale: 'Stale', unavailable: 'Unavailable' };
    return UI.verdictTable({
      columns: [{ key: 'label', label: 'Snippet' }, { key: 'use', label: 'Paste this, word for word', format: (v) => v || NA }, { key: 'generated', label: 'Built from the records', format: (v) => v || '' }, { key: 'records', label: 'Depends on', format: (v) => (v || []).join(', ') }],
      verdict: { at: 1, kind: (r) => S[r.status], text: (r) => T[r.status], reason: (r) => r.reason },
      rows: sn.snippets.map((r) => Object.assign({}, r, { actions: r.status === 'unavailable' ? [] : [{ label: r.status === 'locked' ? 'Edit' : 'Lock wording', cls: r.status === 'stale' ? 'primary' : 'soft', onClick: () => {
        const ta = el('textarea', { class: 'text', rows: 3 }); ta.value = r.locked || r.generated || '';
        const status = el('span', { class: 'micro muted' });
        const go = el('button', { class: 'btn primary sm', type: 'button', text: 'Lock this wording' });
        const body = el('div', { class: 'stack' }, r.status === 'stale' ? el('div', { class: 'card sunken small' }, el('b', { text: 'Stale: ' }), r.reason + '. Built from the records now: ' + r.generated) : null, ta, el('div', { class: 'row' }, go, UI.copyButton({ label: 'Copy', text: () => ta.value }), status),
          r.action ? el('div', { class: 'small' }, el('b', { text: r.action.title + '. ' }), r.action.steps.map((st) => st.n + '. ' + st.text).join(' ')) : null);
        const panel = UI.panel({ title: r.label, body });
        go.addEventListener('click', async () => { go.disabled = true; try { await api(BASE + 'voice/snippet/' + r.key, { method: 'POST', body: { text: ta.value.trim() } }); panel.close(); reload(); } catch (e) { go.disabled = false; status.textContent = 'Could not save: ' + e.message; } });
      } }] })),
      actions: { label: 'Do' }, sort: false, maxRows: 10,
    });
  }
  function learnBox(reload) {
    const out = el('div', { class: 'stack' }, el('p', { class: 'muted small', text: 'Loading.' }));
    api(BASE + 'learn').then((lv) => {
      const items = [el('div', { class: 'small muted', text: lv.counts.edits + ' edits with a value before. Avoid: ' + lv.rules.avoid + '. Use: ' + lv.rules.use + '.' })];
      const list = (kind, rows) => {
        if (!rows.length) return el('p', { class: 'muted small', text: 'No ' + (kind === 'avoided' ? 'word to avoid' : 'word to use') + ' learned yet. Edit a few fields and come back.' });
        const boxes = rows.map((p) => el('label', { class: 'chip', style: { cursor: 'pointer' } }, el('input', { type: 'checkbox', value: p.word, checked: true }), ' ' + p.word + ' (' + p.times + ')' + (p.hype ? ' hype' : '')));
        const st = el('span', { class: 'micro muted' });
        const btn = el('button', { class: 'btn sm primary', type: 'button', text: kind === 'avoided' ? 'Add to words we avoid' : 'Add to words we use' });
        btn.addEventListener('click', async () => { const words = boxes.map((b) => b.querySelector('input')).filter((i) => i.checked).map((i) => i.value); if (!words.length) { st.textContent = 'Tick a word first.'; return; } btn.disabled = true; try { const r = await api(BASE + 'learn/apply', { method: 'POST', body: { kind, words } }); st.textContent = 'Saved ' + r.record + ': ' + r.words.join(', '); reload(); } catch (e) { btn.disabled = false; st.textContent = 'Could not save: ' + e.message; } });
        const ev = el('div', { class: 'micro faint', text: rows.slice(0, 3).map((p) => p.word + ': "' + (p.evidence[0] || {}).before + '" became "' + (p.evidence[0] || {}).after + '"').join(' | ') });
        return el('div', { class: 'stack' }, el('div', { class: 'row' }, ...boxes), el('div', { class: 'row' }, btn, st), ev);
      };
      items.push(el('h4', { text: 'Words you cut' }), list('avoided', lv.avoid), el('h4', { text: 'Words you added' }), list('used', lv.use), el('div', { class: 'micro faint', text: lv.note }));
      mount(out, ...items);
    }).catch((e) => mount(out, el('p', { class: 'muted', text: 'Could not learn: ' + e.message })));
    return out;
  }
  async function loadVoice() {
    let vs;
    try { vs = await api(BASE + 'voice'); } catch (e) { mount('#voice', el('p', { class: 'muted', text: 'Voice unavailable: ' + e.message })); return; }
    const sn = vs.snippets;
    mount('#voice-tools', UI.orientation([{ label: 'fields filled', value: vs.filled, unit: 'n', title: 'of ' + vs.of }, { label: 'liked examples', value: vs.examples.liked.length, unit: 'n', tone: vs.examples.liked.length >= vs.examples_needed ? 'good' : 'bad' }, { label: 'disliked', value: vs.examples.disliked.length, unit: 'n' },
      { label: 'sheet ready', value: null, unit: 'n', unavailable_label: vs.ready ? 'yes' : 'not yet' }, { label: 'snippets locked', value: sn.counts.locked, unit: 'n', title: 'of ' + sn.snippets.length }, { label: 'stale', value: sn.counts.stale, unit: 'n', tone: sn.counts.stale ? 'bad' : null }]));
    mount('#voice', UI.tabs({ items: [
      { key: 'sheet', label: 'Voice sheet', n: vs.filled, panel: () => el('div', { class: 'stack' }, voiceFields(vs, loadVoice), vs.site_lines.length ? el('div', { class: 'small' }, el('b', { text: 'Lines from our own pages: ' }), vs.site_lines.map((l) => '"' + l.quote + '"').join(' ')) : null,
        el('div', { class: 'row' }, UI.copyButton({ label: 'Copy the sheet for an agent', text: () => vs.sheet_text }), el('span', { class: 'micro faint', text: 'Read by ' + vs.readers.join(', ') + '. ' + vs.note })), el('pre', { class: 'card sunken brief', text: vs.sheet_text })) },
      { key: 'examples', label: 'Examples', n: vs.examples.liked.length + vs.examples.disliked.length, panel: () => el('div', { class: 'grid two' }, exampleBox('liked', vs, loadVoice), exampleBox('disliked', vs, loadVoice)) },
      { key: 'snippets', label: 'Snippets', n: sn.snippets.length, panel: () => el('div', { class: 'stack' }, snippetsTable(sn, loadVoice), el('div', { class: 'row' }, UI.copyButton({ label: 'Copy all snippets', text: () => sn.all_text }), el('span', { class: 'micro faint', text: sn.note }))) },
      { key: 'learn', label: 'Learned from your edits', panel: () => learnBox(loadVoice) },
    ] }));
  }

  // ---------- 5c2. claims desk and the draft scanner ----------
  function claimsTable(cd, reload) {
    const rows = cd.claims.map((c) => Object.assign({}, c, { src: c.source.ref ? c.source.ref.replace(/^https?:\/\//, '').slice(0, 40) : (c.source.type || 'none'), used: c.used_by.length ? c.used_by.map((u) => pretty(u.theme) + ' ' + u.level).join(', ') : 'nothing yet', surf: c.surfaces.map(pretty).join(', ') || '' }));
    const act = (r, choice) => async () => {
      try { await api(BASE + 'approve/' + encodeURIComponent(r.id), { method: 'POST', body: { choice } }); reload(); } catch (e) { alert('Could not save: ' + e.message); }
    };
    return UI.verdictTable({
      columns: [
        { key: 'text', label: 'Claim' }, { key: 'tier', label: 'Tier', format: pretty }, { key: 'category', label: 'Kind', format: (v) => v || '' },
        { key: 'used', label: 'Used by ladder rungs' }, { key: 'surf', label: 'Surfaces' }, { key: 'age_days', label: 'Age', unit: 'days', align: 'right' }, { key: 'src', label: 'Source' },
      ],
      verdict: { at: 1, kind: (r) => r.verdict.kind, text: (r) => r.verdict.text, reason: (r) => r.verdict.reason },
      rows: rows.map((r) => Object.assign(r, { actions: r.tier === 'forbidden' ? [{ label: 'Allow again', onClick: act(r, 'approve') }] : r.tier === 'approved' ? [{ label: 'Forbid', cls: 'danger', onClick: act(r, 'forbid') }] : [{ label: 'Approve', cls: 'primary', onClick: act(r, 'approve') }, { label: 'Forbid', cls: 'danger', onClick: act(r, 'forbid') }] })),
      actions: { label: 'Do' }, sort: false, maxRows: 60, empty: 'No claims yet. Add the first one below.',
    });
  }
  function claimsAdd(reload) {
    const input = el('input', { class: 'text sm', placeholder: 'A claim we can back, or a phrase we must never say', style: { flex: '1 1 320px' } });
    const status = el('span', { class: 'micro muted' });
    const go = (tier) => async () => {
      if (!input.value.trim()) { status.textContent = 'Type it first.'; return; }
      try { const res = await api(BASE + 'claims', { method: 'POST', body: { text: input.value.trim(), tier } }); status.textContent = 'Saved ' + res.record + ' as ' + tier + '. Flows to ' + res.flows_to + '.'; input.value = ''; reload(); }
      catch (e) { status.textContent = 'Could not save: ' + e.message; }
    };
    return el('div', { class: 'row add-field' }, input, el('button', { class: 'btn sm primary', type: 'button', text: 'Add as approved', onclick: go('approved') }), el('button', { class: 'btn sm danger', type: 'button', text: 'Forbid this phrase', onclick: go('forbidden') }), status);
  }
  function tierBar(cd) {
    const keys = Object.keys(cd.counts);
    return Charts.bar({ title: 'Claims by tier', labels: keys.map(pretty), series: [{ name: 'claims', values: keys.map((k) => cd.counts[k]) }], unit: 'n', height: 170, values: true,
      note: 'Usable in copy: approved and site backed. Untiered claims should reach 0 within ' + cd.untiered_days + ' days of appearing.' });
  }
  function scanner() {
    const ta = el('textarea', { class: 'text', rows: 6, placeholder: 'Paste an ad, an email, a page section. The scanner checks it against the brain: forbidden phrases, unproven absolutes, stale numbers, unapproved claims, the avoid list, reading grade. Pick a channel to add its rules.' });
    const channel = el('select', { class: 'text sm' }, el('option', { value: '', text: 'No channel rules' }), ...['amazon', 'meta', 'google', 'email', 'sms'].map((c) => el('option', { value: c, text: pretty(c) + ' rules' })));
    const out = el('div', { class: 'stack' });
    const btn = el('button', { class: 'btn primary sm', type: 'button', text: 'Check the draft' });
    btn.addEventListener('click', async () => {
      if (!ta.value.trim()) { mount(out, el('p', { class: 'muted small', text: 'Paste a draft first.' })); return; }
      btn.disabled = true;
      try {
        const r = await api(BASE + 'scan', { method: 'POST', body: { text: ta.value, channel: channel.value || undefined } });
        const head = el('div', { class: 'row' }, UI.verdict(r.verdict === 'pass' ? 'keep' : r.verdict === 'warn' ? 'watch' : 'stop', r.verdict === 'pass' ? 'Ships' : r.verdict === 'warn' ? 'Check first' : 'Blocked', r.fails + ' blocking, ' + r.warns + ' warnings'),
          el('span', { class: 'chip', text: r.words + ' words, ' + r.sentences + ' sentences' }), el('span', { class: 'chip ' + (r.reading_grade != null && r.reading_grade > 10 ? 'warn' : ''), text: 'reading grade ' + (r.reading_grade == null ? NA : r.reading_grade) }),
          el('span', { class: 'micro faint', text: 'Checked ' + r.checked.forbidden_phrases + ' forbidden phrases, ' + r.checked.facts + ' brain numbers, ' + r.checked.weak_claims + ' unapproved claims.' }));
        const list = r.hits.length ? UI.table({ columns: [{ key: 'severity', label: 'Level', format: (v) => v === 'fail' ? 'blocks' : 'warning' }, { key: 'kind', label: 'Rule', format: pretty }, { key: 'match', label: 'In the draft' }, { key: 'fix', label: 'Fix' }, { key: 'record', label: 'Record', format: (v) => v || '' }], rows: r.hits, sort: false })
          : el('p', { class: 'muted small', text: 'No hit. Every number matches the brain and no forbidden phrase appears.' });
        mount(out, head, list);
      } catch (e) { mount(out, el('p', { class: 'muted', text: 'Could not check: ' + e.message })); }
      btn.disabled = false;
    });
    return el('div', { class: 'stack scanner' }, ta, el('div', { class: 'row' }, el('span', { class: 'small muted', text: 'Channel:' }), channel, btn, el('span', { class: 'micro faint', text: 'Rules only, no model. A blocking hit is a forbidden phrase, a number the brain contradicts, or a channel rule.' })), out);
  }
  async function loadClaims() {
    let cd;
    try { cd = await api(BASE + 'claims'); } catch (e) { mount('#claims', el('p', { class: 'muted', text: 'Claims unavailable: ' + e.message })); return; }
    mount('#claims-tools', UI.orientation([{ label: 'claims', value: cd.total, unit: 'n' }, { label: 'usable', value: cd.usable, unit: 'n', tone: 'good' }, { label: 'need your call', value: cd.needs_call, unit: 'n', tone: cd.needs_call ? 'bad' : null }, { label: 'forbidden', value: cd.forbidden, unit: 'n' }]));
    mount('#claims', UI.tabs({ items: [
      { key: 'claims', label: 'Claims', n: cd.total, panel: () => el('div', { class: 'stack' }, claimsTable(cd, loadClaims), claimsAdd(loadClaims), el('div', { class: 'micro faint', text: cd.note })) },
      { key: 'tiers', label: 'By tier', panel: () => tierBar(cd) },
      { key: 'scan', label: 'Check a draft', panel: scanner },
    ], current: cd.needs_call ? 'claims' : 'claims' }));
  }

  // ---------- 5d. conflicts: which source wins ----------
  function conflictCard(c, reload) {
    const card = el('article', { class: 'card flat rec conflict' + (c.status === 'open' ? '' : ' settled') });
    card.append(el('div', { class: 'meta' }, el('span', { class: 'chip mono', text: c.section + '.' + c.field }),
      el('span', { text: 'raised ' + fmt.date(c.raised_at) }), c.status === 'open' ? (c.needs_founder ? el('span', { class: 'chip bad', text: 'needs you' }) : el('span', { class: 'chip warn', text: 'open' })) : el('span', { class: 'chip good', text: 'settled by you ' + (c.resolved_at ? fmt.date(c.resolved_at) : '') }),
      c.reads_by && c.reads_by.length ? el('span', { text: 'read by ' + c.reads_by.join(', ') }) : null));
    const vs = el('div', { class: 'vs' });
    const status = el('span', { class: 'muted small' });
    (c.values || []).forEach((v, i) => {
      const kept = v.record_id === c.kept && i === (c.values || []).findIndex((x) => x.record_id === c.kept);
      const isDefault = c.status === 'open' && v.record_id === c.default_record && i === (c.values || []).findIndex((x) => x.record_id === c.default_record);
      const box = el('div', { class: kept ? 'kept' : '' },
        el('div', { class: 'meta' }, kept ? el('span', { class: 'chip accent', text: c.status === 'open' ? 'kept for now' : 'kept' }) : null, isDefault && !kept ? el('span', { class: 'chip', text: 'default' }) : null, el('span', { class: 'chip', text: pretty(v.source_type) }), el('span', { text: 'confidence ' + (v.confidence == null ? NA : v.confidence) })),
        el('b', { text: String(v.value) }), el('div', { class: 'muted small', text: v.text || '' }),
        el('div', { class: 'meta' }, sourceLink({ type: v.source_type, ref: v.source_ref, link: /^https?:/.test(v.source_ref || '') ? v.source_ref : null })));
      if (c.status === 'open') {
        const btn = el('button', { class: 'btn sm ' + (kept ? '' : 'primary'), type: 'button', text: kept ? 'Keep this' : 'Use this instead' });
        btn.addEventListener('click', async () => {
          btn.disabled = true; status.textContent = 'Saving';
          try { const res = await api(BASE + 'conflicts/' + encodeURIComponent(c.id), { method: 'POST', body: { record_id: v.record_id, index: i } }); status.textContent = 'Saved as ' + res.record + '. Flows to ' + res.flows_to + '. Logged as ' + res.decision + '.'; if (reload) reload(); }
          catch (e) { btn.disabled = false; status.textContent = 'Could not save: ' + e.message; }
        });
        box.append(el('div', { class: 'row' }, btn));
      }
      vs.append(box);
    });
    card.append(vs, el('div', { class: 'muted small', text: 'Rule: ' + (c.rule || NA) }));
    if (c.status === 'open') {
      const input = el('input', { type: 'text', placeholder: 'Or type the right value', 'aria-label': 'Right value for ' + c.field });
      const why = el('input', { type: 'text', placeholder: 'Reason (optional)', 'aria-label': 'Reason' });
      const go = el('button', { class: 'btn sm', type: 'button', text: 'Save my value' });
      go.addEventListener('click', async () => {
        if (!input.value.trim()) { status.textContent = 'Type a value first.'; return; }
        go.disabled = true;
        try { const res = await api(BASE + 'conflicts/' + encodeURIComponent(c.id), { method: 'POST', body: { text: input.value.trim(), reason: why.value.trim() } }); status.textContent = 'Saved as ' + res.record + '.'; if (reload) reload(); }
        catch (e) { go.disabled = false; status.textContent = 'Could not save: ' + e.message; }
      });
      card.append(el('div', { class: 'answer' }, input, why, go), status);
    }
    return card;
  }
  async function loadConflicts() {
    let cv;
    try { cv = await api(BASE + 'conflicts'); } catch (e) { mount('#conflicts', el('p', { class: 'muted', text: 'Conflicts unavailable: ' + e.message })); return; }
    mount('#conflicts-tools', UI.orientation([{ label: 'open', value: cv.counts.open, unit: 'n', tone: cv.counts.open ? 'bad' : 'good' }, { label: 'need you', value: cv.counts.needs_founder, unit: 'n' }, { label: 'settled', value: cv.counts.settled, unit: 'n' }]));
    const items = cv.open.map((c) => conflictCard(c, loadConflicts));
    if (!cv.open.length) items.push(el('p', { class: 'muted', text: 'No open conflict. ' + cv.rule }));
    if (cv.settled.length) {
      const list = el('div', { class: 'grid', hidden: true });
      const btn = el('button', { class: 'btn sm', type: 'button', text: 'Show ' + cv.settled.length + ' settled' });
      btn.addEventListener('click', () => { list.hidden = !list.hidden; btn.textContent = list.hidden ? 'Show ' + cv.settled.length + ' settled' : 'Hide settled'; if (!list.hidden && !list.children.length) mount(list, ...cv.settled.map((c) => conflictCard(c))); });
      items.push(el('div', { class: 'row' }, btn), list);
    }
    mount('#conflicts', ...items);
  }

  function auditTable(findings) {
    return UI.table({
      columns: [
        { key: 'severity', label: 'Severity' },
        { key: 'rule_id', label: 'Rule' },
        { key: 'what', label: 'What' },
        { key: 'sentence', label: 'Finding' },
        { key: 'cap', label: 'Capability' },
      ],
      rows: findings.map((f) => ({ severity: f.severity, rule_id: f.rule_id, what: pretty(f.entity.label), sentence: f.sentence,
        cap: f.capability.id + ', ' + pretty(f.capability.autonomy) })), sort: false, empty: 'No findings. The brain has what the rooms need.',
    });
  }

  async function loadDesk() {
    let d;
    try { d = await api(BASE + 'overview'); } catch (e) {
      mount('#badge', 'Could not load the brain: ' + e.message); return;
    }
    mount('#badge', el('span', null, el('b', { text: 'Simulated data. ' }), d.simulated_note + ' Brain version ' + d.version + '.' + (BRAND ? ' Brand: ' + BRAND + '.' : '')));
    const t0 = document.getElementById('t0');
    t0.textContent = d.t0;
    mount('#t0-tools', el('span', { class: 'small muted', text: 'The compact brand card every agent reads first.' }),
      el('button', { class: 'btn sm', type: 'button', text: 'Show', onclick: (e) => { t0.hidden = !t0.hidden; e.target.textContent = t0.hidden ? 'Show' : 'Hide'; } }),
      UI.copyButton({ label: 'Copy T0 card', text: () => d.t0 }));
    mount('#insights', ...(d.insights.length ? d.insights.map((i) => UI.insight(Object.assign({ screen: SCREEN }, i)))
      : [el('p', { class: 'muted', text: 'No rule fired today.' })]));
    mount('#ladders', ...d.ladders.map(ladderCard));
    loadReview();
    try {
      const a = await api(BASE + 'audit');
      mount('#audit', el('p', { class: 'muted small', text: a.findings.length + ' findings from ' + a.rules.length + ' rules.' }), auditTable(a.findings));
    } catch (e) { mount('#audit', el('p', { class: 'muted', text: 'Audit unavailable: ' + e.message })); }
  }

  async function load() {
    mountAsk();
    mountDrop();
    loadDocs();
    loadFlows();
    loadMarket();
    loadHealth();
    loadConflicts();
    loadQuestions();
    loadClaims();
    loadSite();
    loadParity();
    loadContracts();
    loadLegal();
    loadVoice();
    loadBattlecards();
    loadPermissions();
    loadAssumptions();
    loadFacts();
    loadPackage();
    const [prof] = await Promise.all([loadProfile(), loadDesk()]);
    await loadPlan(prof);
  }

  load();
})();
