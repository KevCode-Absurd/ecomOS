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

  // ---------- 1b. decisions log ----------
  const CHOICE_TEXT = { agent: 'Agent does it', person: 'Sent to a person', not_now: 'Not now, snoozed 14 days' };
  async function loadDecisions(m) {
    let d;
    try { d = await api(BASE + 'decisions'); } catch (e) { mount('#decisions', el('p', { class: 'muted', text: 'Decisions unavailable: ' + e.message })); return; }
    const byId = {}; for (const a of (m && m.actions) || []) byId[a.id] = a;
    const items = d.items.map((it) => {
      if (it.kind === 'action') {
        const a = byId[it.finding_id];
        return { when: it.time, who: 'you', tone: it.choice === 'not_now' ? 'warn' : 'good', title: CHOICE_TEXT[it.choice] || it.choice, text: (a ? a.title : (it.finding_id || it.capability)) + (it.reason ? '. ' + it.reason : '') + (it.screen ? ' (' + it.screen + ')' : '') };
      }
      return { when: it.date, who: it.who || 'founder', tone: 'accent', title: it.title, text: it.text };
    });
    mount('#decisions-tools', UI.orientation([{ label: 'approvals', value: d.counts.action, unit: 'n' }, { label: 'snoozed', value: d.counts.snoozed, unit: 'n' }, { label: 'brain decisions', value: d.counts.brain, unit: 'n' }, { label: 'last', value: null, unit: 'n', unavailable_label: d.last ? fmt.date(d.last) : 'none yet' }]));
    mount('#decisions', UI.timeline(items.slice(0, 30)), items.length > 30 ? el('div', { class: 'micro faint', text: (items.length - 30) + ' older entries not shown.' }) : null);
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

  // ---------- 2b. where an edit goes: flow proof ----------
  async function loadFlows() {
    let fl;
    try { fl = await api(BASE + 'flows'); } catch (e) { mount('#flows', el('p', { class: 'muted small', text: 'Flow proof unavailable: ' + e.message })); return; }
    const rows = fl.sections.map((s) => Object.assign({}, s, { readers: s.read_by.join(', ') || 'none directly', t0: s.read_by_t0.length ? s.read_by_t0.join(', ') : 'none', last_read_text: s.last_read ? fmt.date(s.last_read) : NA + ' (' + s.last_read_reason + ')' }));
    const table = UI.table({
      columns: [
        { key: 'label', label: 'Profile section' },
        { key: 'approved', label: 'Approved by you', unit: 'n', align: 'right' },
        { key: 'last_founder_edit', label: 'Last edit', format: (v) => v ? fmt.date(v) : 'none yet' },
        { key: 'readers', label: 'Read by (code scan)' },
        { key: 't0', label: 'Read through the T0 card' },
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
    const ta = el('textarea', { class: 'text', rows: 6, placeholder: 'Paste an ad, an email, a page section. The scanner checks it against the brain: forbidden phrases, unproven absolutes, stale numbers, unapproved claims, reading grade.' });
    const out = el('div', { class: 'stack' });
    const btn = el('button', { class: 'btn primary sm', type: 'button', text: 'Check the draft' });
    btn.addEventListener('click', async () => {
      if (!ta.value.trim()) { mount(out, el('p', { class: 'muted small', text: 'Paste a draft first.' })); return; }
      btn.disabled = true;
      try {
        const r = await api(BASE + 'scan', { method: 'POST', body: { text: ta.value } });
        const head = el('div', { class: 'row' }, UI.verdict(r.verdict === 'pass' ? 'keep' : r.verdict === 'warn' ? 'watch' : 'stop', r.verdict === 'pass' ? 'Ships' : r.verdict === 'warn' ? 'Check first' : 'Blocked', r.fails + ' blocking, ' + r.warns + ' warnings'),
          el('span', { class: 'chip', text: r.words + ' words, ' + r.sentences + ' sentences' }), el('span', { class: 'chip ' + (r.reading_grade != null && r.reading_grade > 10 ? 'warn' : ''), text: 'reading grade ' + (r.reading_grade == null ? NA : r.reading_grade) }),
          el('span', { class: 'micro faint', text: 'Checked ' + r.checked.forbidden_phrases + ' forbidden phrases, ' + r.checked.facts + ' brain numbers, ' + r.checked.weak_claims + ' unapproved claims.' }));
        const list = r.hits.length ? UI.table({ columns: [{ key: 'severity', label: 'Level', format: (v) => v === 'fail' ? 'blocks' : 'warning' }, { key: 'kind', label: 'Rule', format: pretty }, { key: 'match', label: 'In the draft' }, { key: 'fix', label: 'Fix' }, { key: 'record', label: 'Record', format: (v) => v || '' }], rows: r.hits, sort: false })
          : el('p', { class: 'muted small', text: 'No hit. Every number matches the brain and no forbidden phrase appears.' });
        mount(out, head, list);
      } catch (e) { mount(out, el('p', { class: 'muted', text: 'Could not check: ' + e.message })); }
      btn.disabled = false;
    });
    return el('div', { class: 'stack scanner' }, ta, el('div', { class: 'row' }, btn, el('span', { class: 'micro faint', text: 'Rules only, no model. A blocking hit is a forbidden phrase or a number the brain contradicts.' })), out);
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
    mount('#badge', el('span', null, el('b', { text: 'Simulated data. ' }), d.simulated_note + ' Brain version ' + d.version + '.'));
    const t0 = document.getElementById('t0');
    t0.textContent = d.t0;
    mount('#t0-tools', el('span', { class: 'small muted', text: 'The compact brand card every agent reads first.' }),
      el('button', { class: 'btn sm', type: 'button', text: 'Show', onclick: (e) => { t0.hidden = !t0.hidden; e.target.textContent = t0.hidden ? 'Show' : 'Hide'; } }),
      UI.copyButton({ label: 'Copy T0 card', text: () => d.t0 }));
    mount('#insights', ...(d.insights.length ? d.insights.map((i) => UI.insight(Object.assign({ screen: SCREEN }, i)))
      : [el('p', { class: 'muted', text: 'No rule fired today.' })]));
    mount('#ladders', ...d.ladders.map(ladderCard));
    mount('#review', ...(d.review.length ? d.review.map((r) => reviewCard(r, loadDesk)) : [el('p', { class: 'muted', text: 'Nothing proposed. Agent updates land here before they reach the brain.' })]));
    try {
      const a = await api(BASE + 'audit');
      mount('#audit', el('p', { class: 'muted small', text: a.findings.length + ' findings from ' + a.rules.length + ' rules.' }), auditTable(a.findings));
    } catch (e) { mount('#audit', el('p', { class: 'muted', text: 'Audit unavailable: ' + e.message })); }
  }

  async function load() {
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
    const [prof] = await Promise.all([loadProfile(), loadDesk()]);
    await loadPlan(prof);
  }

  load();
})();
