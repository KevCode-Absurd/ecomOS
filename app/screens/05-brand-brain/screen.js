/* Brand brain, round 1 top section (depth contract). Reads /api/05-brand-brain/master, profile, documents,
   overview, records and audit. Writes only through the api: a profile edit (approved founder record), a
   document in, a founder answer, accept or ignore on a proposed record, and decisions on the master list. */
(function () {
  'use strict';
  const { el, mount, api, fmt } = UI;
  const BASE = '/api/05-brand-brain/';
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
    mount('#plan', UI.planBoard({
      title: 'The plan: top 10 to approve', sub: win.days + ' days to ' + fmt.date(win.ends_on) + ', ' + (m.screens || []).length + ' screens ranked',
      orient: orient(m, prof), actions: m.top, limit: 10, screen: SCREEN, showScreen: true,
      tools: [el('button', { class: 'btn sm', type: 'button', text: 'Export CSV', onclick: () => UI.csv((m.actions || []).map((a) => ({ rank: (m.actions || []).indexOf(a) + 1, screen: a.screen, title: a.title, owner: a.owner, severity: a.severity, status: a.status, total: a.rubric && a.rubric.total, stake_usd: a.money_at_stake && a.money_at_stake.usd, why: a.why })), null, 'master-list.csv') })],
      foot: el('div', { class: 'row', style: { gap: '14px' } }, UI.rubricLegend(), el('span', { class: 'micro faint', text: 'Ranking: critical first by stake, then rubric total, severity, stake, days open. Approvals log to the decisions table; "Not now" snoozes 14 days.' })),
      empty: 'No open action across the 28 audits for this window.',
    }));
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

  // ---------- 3. files in ----------
  function docsTable(d) {
    return UI.table({
      columns: [
        { key: 'name', label: 'File' },
        { key: 'added_at', label: 'Added', format: (v) => v ? fmt.date(v) : NA },
        { key: 'added_by', label: 'By', format: (v) => v || 'unknown' },
        { key: 'records_changed_count', label: 'Records changed', unit: 'n' },
        { key: 'extracted', label: 'Read into records', format: (v) => v ? 'yes' : 'kept as a file' },
        { key: 'note', label: 'Note', format: (v) => v || '' },
      ], rows: d.documents, sort: false, empty: 'No files yet. Drop a brand book, a deck, past tests, anything.',
    });
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
      hint: 'Up to 5 MB each. It is stored as it is in the documents folder and listed here with the date.',
      onFiles: async (files) => {
        for (const f of files) {
          status.textContent = 'Adding ' + f.name;
          try {
            const res = await api(BASE + 'documents', { method: 'POST', body: { name: f.name, content_base64: await readAsBase64(f) } });
            status.textContent = 'Added ' + res.document.name + ' (' + fmt.compact(res.document.bytes) + ' bytes). ' + res.next;
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

  async function loadMarket() {
    let d, actions = [];
    try { d = await api(BASE + 'competitors'); } catch (e) { mount('#market', el('p', { class: 'muted', text: 'Competitors unavailable: ' + e.message })); return null; }
    try { const r = await api(BASE + 'rank'); actions = (r.actions || []).filter((a) => /BRN-R0[5678]/.test(a.rule_id || '')); } catch (e) { actions = []; }
    mount('#market-tools', UI.orientation(marketOrient(d)));
    const gapsN = (d.gaps || []).length;
    loadCoverage(actions);
    mount('#market', UI.tabs({ items: [
      { key: 'gaps', label: 'Gaps to brief', n: gapsN, panel: () => gapCards(d, actions) },
      { key: 'pages', label: 'Pages', n: d.pages.length, panel: () => el('div', { class: 'stack' }, pagesTable(d), el('div', { class: 'micro faint', text: d.note + ' Click a row for the page detail.' })) },
      { key: 'formats', label: 'Format mix', panel: () => mixChart(d, 'format') },
      { key: 'hooks', label: 'Hook mix', panel: () => mixChart(d, 'hook') },
    ], current: gapsN ? 'gaps' : 'pages' }), repullStrip(d));
    return d;
  }

  // ---------- 5. the desk (round 0 blocks, restyled) ----------
  function recordCard(r) {
    const card = el('article', { class: 'card flat rec' });
    card.append(el('div', { class: 'meta' }, tierChip(r.tier), el('span', { class: 'chip mono', text: r.id }),
      el('span', { text: r.date === 'undated' ? 'undated' : fmt.date(r.date) }),
      el('span', { text: 'confidence ' + (r.confidence == null ? NA : r.confidence) }),
      r.status !== 'active' ? el('span', { class: 'chip warn', text: r.status }) : null));
    card.append(el('div', { text: r.text || '' }));
    card.append(el('div', { class: 'meta' }, sourceLink(r.source)));
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

  function questionCard(q, reload) {
    const card = el('article', { class: 'card flat rec' });
    card.append(el('div', { class: 'meta' }, el('span', { class: 'chip mono', text: q.field }), el('span', { class: 'chip', text: pretty(q.section) }),
      el('span', { class: 'chip ' + (q.weight >= 8 ? 'bad' : ''), text: 'weight ' + q.weight }),
      q.answered_on ? el('span', { class: 'chip good', text: 'answered ' + fmt.date(q.answered_on) }) : null));
    card.append(el('div', { text: q.question }));
    if (q.why) card.append(el('div', { class: 'muted small', text: q.why }));
    if (q.who_can_answer) card.append(el('div', { class: 'muted small', text: 'Who can answer: ' + q.who_can_answer }));
    if (q.answered_on) { card.append(el('div', { class: 'muted small', text: 'Saved as ' + q.answer_record })); return card; }
    const input = el('input', { type: 'text', placeholder: 'Your answer in a line', 'aria-label': 'Answer: ' + q.question });
    const btn = el('button', { class: 'btn primary sm', type: 'button', text: 'Save answer' });
    const status = el('span', { class: 'muted small' });
    btn.addEventListener('click', async () => {
      if (!input.value.trim()) { status.textContent = 'Type an answer first.'; return; }
      btn.disabled = true;
      try {
        const res = await api(BASE + 'questions/' + encodeURIComponent(q.field), { method: 'POST', body: { answer: input.value } });
        status.textContent = 'Saved as ' + res.record + '.';
        reload();
      } catch (e) { btn.disabled = false; status.textContent = 'Could not save: ' + e.message; }
    });
    card.append(el('div', { class: 'answer' }, input, btn), status);
    return card;
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

  function conflictCard(c) {
    const card = el('article', { class: 'card flat rec' });
    card.append(el('div', { class: 'meta' }, el('span', { class: 'chip mono', text: c.section + '.' + c.field }),
      el('span', { text: 'raised ' + fmt.date(c.raised_at) }), c.needs_founder ? el('span', { class: 'chip warn', text: 'needs you' }) : null));
    const vs = el('div', { class: 'vs' });
    for (const v of c.values || []) {
      const kept = v.record_id === c.kept && v === (c.values || []).find((x) => x.record_id === c.kept);
      vs.append(el('div', { class: kept ? 'kept' : '' }, el('div', { class: 'meta' }, kept ? el('span', { class: 'chip accent', text: 'kept for now' }) : null,
        el('span', { text: 'confidence ' + v.confidence })), el('b', { text: String(v.value) }), el('div', { class: 'muted small', text: v.text }),
        el('div', { class: 'meta' }, sourceLink({ type: v.source_type, ref: v.source_ref, link: /^https?:/.test(v.source_ref) ? v.source_ref : null }))));
    }
    card.append(vs, el('div', { class: 'muted small', text: 'Rule: ' + (c.rule || NA) }));
    card.append(UI.decisionRow({ capability: 'BRN-C05', autonomy: 'agent', screen: SCREEN, compact: true }));
    return card;
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
    mount('#badge', el('span', null, el('b', { text: 'Simulated data. ' }), d.simulated_note + ' Brain version ' + d.version + '.'));
    const t0 = document.getElementById('t0');
    t0.textContent = d.t0;
    mount('#t0-tools', el('span', { class: 'small muted', text: 'The compact brand card every agent reads first.' }),
      el('button', { class: 'btn sm', type: 'button', text: 'Show', onclick: (e) => { t0.hidden = !t0.hidden; e.target.textContent = t0.hidden ? 'Show' : 'Hide'; } }),
      UI.copyButton({ label: 'Copy T0 card', text: () => d.t0 }));
    mount('#insights', ...(d.insights.length ? d.insights.map((i) => UI.insight(Object.assign({ screen: SCREEN }, i)))
      : [el('p', { class: 'muted', text: 'No rule fired today.' })]));
    mount('#sections', sectionsTable(d.sections));
    mount('#ladders', ...d.ladders.map(ladderCard));
    mount('#questions', ...(d.questions.length ? d.questions.map((q) => questionCard(q, loadDesk)) : [el('p', { class: 'muted', text: 'No open questions.' })]));
    mount('#review', ...(d.review.length ? d.review.map((r) => reviewCard(r, loadDesk)) : [el('p', { class: 'muted', text: 'Nothing proposed. Agent updates land here before they reach the brain.' })]));
    mount('#conflicts', ...(d.conflicts.length ? d.conflicts.map(conflictCard) : [el('p', { class: 'muted', text: 'No open conflicts.' })]));
    try {
      const a = await api(BASE + 'audit');
      mount('#audit', el('p', { class: 'muted small', text: a.findings.length + ' findings from ' + a.rules.length + ' rules.' }), auditTable(a.findings));
    } catch (e) { mount('#audit', el('p', { class: 'muted', text: 'Audit unavailable: ' + e.message })); }
  }

  async function load() {
    mountDrop();
    loadDocs();
    loadMarket();
    const [prof] = await Promise.all([loadProfile(), loadDesk()]);
    await loadPlan(prof);
  }

  load();
})();
