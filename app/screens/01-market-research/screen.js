/* Market and product research, round 1. Reads /api/01-market-research/rank (the plan) and overview (the rest).
   No brand fact and no number lives here; the server sends every value, rule, sentence and step. */
(function () {
  'use strict';
  const { el, mount, api, fmt } = UI;
  const SLUG = '01-market-research';
  const BASE = '/api/' + SLUG + '/';
  const brand = new URLSearchParams(location.search).get('brand') || 'bombas';
  const Q = '?brand=' + encodeURIComponent(brand);
  const NA = 'unavailable';
  const pretty = (s) => String(s || '').replace(/_/g, ' ');
  const SEV_TONE = { critical: 'bad', high: 'bad', medium: 'warn', low: '' };

  function chip(text, tone) { return el('span', { class: 'chip ' + (tone || ''), text }); }
  function section(id, title, sub, ...children) {
    const s = el('section', { class: 'section', id });
    s.append(el('div', { class: 'sec-head' }, el('h2', { text: title }), sub ? el('span', { class: 'sub', text: sub }) : null));
    s.append(...children.filter(Boolean));
    return s;
  }
  function gapLine(text, action) {
    const line = el('div', { class: 'gap-line' }, el('span', null, el('b', { text: 'Gap: ' }), text));
    if (action) line.append(el('button', { class: 'btn soft xs', type: 'button', text: action.label, onclick: action.onClick }));
    return line;
  }
  function coversList(a, compact) {
    const c = a.covers || [];
    if (!c.length || (compact && c.length < 2)) return null;
    const sev = (s) => s === 'critical' || s === 'high' ? 'fix' : s === 'low' ? 'na' : 'watch';
    return el('div', { class: 'card flat' + (compact ? ' covers' : ''), style: compact ? { marginTop: '-4px', marginBottom: '8px' } : null },
      el('div', { class: 'micro muted', text: 'This card covers ' + c.length + ' finding' + (c.length === 1 ? '' : 's') + '; each one closes on its own rule.' }),
      el('ul', { class: 'small', style: { margin: '4px 0 0', paddingLeft: '18px' } }, c.map((f) => el('li', null, UI.verdict(sev(f.severity), f.severity || ''), ' ', el('span', { class: 'mono micro faint', text: f.rule_id }), ' ', f.sentence || f.rule, f.stake_usd != null ? el('span', { class: 'muted', text: ' (' + fmt.money(f.stake_usd) + ')' }) : null))));
  }
  const CREATIVE_RULES = ['PROD-R07', 'PROD-R08', 'PROD-R09', 'PROD-R10', 'PROD-R11', 'PROD-R35'];
  async function openHandoff(a) {
    const fid = (a.finding_ids || [])[0];
    let h;
    try { h = await api(BASE + 'handoff/' + encodeURIComponent(fid) + Q); } catch (e) { alert('Hand-off unavailable: ' + e.message); return; }
    UI.panel({ title: 'Creative hand-off: ' + (h.title || a.title), tools: [UI.copyButton({ label: 'Copy hand-off', text: () => h.text })],
      body: el('div', { class: 'stack' }, el('p', { class: 'micro muted', text: 'The angle, the buyer, the doubt, the proof on file, what buyers say (reviews only, never Reddit), the words to use and the do-not list. Every line comes from the brain and this desk.' }),
        el('pre', { class: 'small', style: { whiteSpace: 'pre-wrap', margin: 0 }, text: h.text })) });
  }
  function openAction(a) {
    const tools = CREATIVE_RULES.includes(a.rule_id) ? [el('button', { class: 'btn sm', type: 'button', text: 'Creative hand-off', onclick: () => openHandoff(a) })] : null;
    UI.panel({ title: a.title, tools, body: el('div', { class: 'stack' }, UI.actionCard(a, { expanded: true, screen: SLUG }), coversList(a, false)) });
  }
  const state = { actions: [], byFinding: {} };
  function actionFor(findingId) { return state.byFinding[findingId] || null; }

  // ---------- 1. the plan ----------
  async function loadCalendar() {
    let c;
    try { c = await api(BASE + 'calendar' + Q); } catch (e) { return; }
    const host = document.getElementById('calendar');
    if (!host) return;
    host.innerHTML = '';
    const items = c.items || [];
    const byId = {}; for (const a of state.actions) byId[a.id] = a;
    const open = (it) => { const a = byId[it.action_id]; if (a) openAction(a); };
    const rows = items.map((it) => ({ when: fmt.date(it.when) + (it.days < 0 ? ' (' + (-it.days) + ' d ago)' : it.days === 0 ? ' (today)' : ' (in ' + it.days + ' d)'), kind: it.kind.replace('_', ' '), title: it.title, text: it.text, it,
      actions: [it.action_id ? { label: 'Open', onClick: () => open(it) } : { label: 'No card', cls: 'quiet', onClick: () => {} }] }));
    host.append(section('desk-calendar', 'What is due, and when?', 'Every dated thing on this desk in the next ' + c.horizon_days + ' days: time boxes, review dates, the check dates of the top actions, parked actions coming back, pulls due and the gift window. Each one opens its card.',
      el('div', { class: 'grid two' }, el('div', { class: 'card' }, UI.timeline(items.slice(0, 14).map((it) => ({ when: it.when, title: it.title, text: it.text, tone: it.tone })))),
        el('div', { class: 'card scroll' }, UI.verdictTable({ columns: [{ key: 'when', label: 'When' }, { key: 'title', label: 'What' }, { key: 'text', label: 'Detail' }], rows,
          verdict: { at: 1, kind: (r) => r.it.days < 0 ? 'fix' : r.it.days <= 7 ? 'watch' : 'keep', text: (r) => r.it.days < 0 ? 'Overdue' : r.it.days <= 7 ? 'This week' : r.it.kind.replace('_', ' '), reason: () => 'by date' },
          actions: { label: 'Do', onClick: () => {} }, sort: false }))),
      gapLine((c.overdue ? c.overdue + ' overdue' : 'nothing overdue') + ', ' + (c.this_week || 0) + ' due in the next 7 days, ' + items.length + ' in ' + c.horizon_days + ' days.', items.length && items[0].action_id ? { label: 'Open the first', onClick: () => open(items[0]) } : null)));
  }

  async function loadParked() {
    let r;
    try { r = await api(BASE + 'parked' + Q); } catch (e) { return; }
    const parked = r.parked || [];
    const host = document.getElementById('parked') || el('div', { id: 'parked' });
    host.innerHTML = '';
    document.getElementById('plan').append(host);
    if (!parked.length && !r.decided) return;
    const rows = parked.map((a) => ({ title: a.title, choice: 'not now', on: fmt.date(((a.decision || {}).time || '').slice(0, 10)), back: fmt.date(a.returns_on), reason: (a.decision || {}).reason || '', a }));
    host.append(el('div', { class: 'card flat', style: { marginTop: '10px' } },
      el('div', { class: 'sec-head' }, el('h2', { text: 'Decided: ' + (r.decided || 0) + ' on the plan, ' + parked.length + ' parked' }),
        el('span', { class: 'sub', text: 'A "not now" parks an action for ' + r.snooze_days + ' days and it leaves the plan; it comes back on its own or when you decide again here. Agent and person choices stay on their cards.' })),
      parked.length ? UI.table({ columns: [{ key: 'title', label: 'Parked action' }, { key: 'on', label: 'Parked on' }, { key: 'back', label: 'Back on the plan' }, { key: 'reason', label: 'Your note' }], rows }) : null,
      parked.length ? el('div', { class: 'stack', style: { marginTop: '8px' } }, parked.slice(0, 3).map((a) => UI.actionCard(a, { compact: true, screen: SLUG }))) : null));
  }

  async function loadPlan(o) {
    let r;
    try { r = await api(BASE + 'rank' + Q + '&window=28d'); }
    catch (e) { mount('#plan', el('p', { class: 'muted', text: 'Plan unavailable: ' + e.message })); return; }
    state.actions = r.actions || [];
    for (const a of state.actions) for (const id of a.finding_ids || []) state.byFinding[id] = a;
    const open = state.actions.filter((a) => a.status !== 'unavailable');
    const connect = state.actions.filter((a) => a.status === 'unavailable');
    const w = r.window || {};
    mount('#plan', UI.planBoard({
      title: 'The plan: what to build and do next', sub: w.days + ' days to ' + fmt.date(w.ends_on) + ', ' + open.length + ' open, ' + connect.length + ' waiting on a source',
      orient: o.orientation, actions: open, limit: 10, screen: SLUG,
      tools: [el('button', { class: 'btn sm', type: 'button', text: 'Export CSV', onclick: () => UI.csv(state.actions.map((a, i) => ({ rank: i + 1, title: a.title, owner: a.owner, severity: a.severity, status: a.status, total: a.rubric && a.rubric.total, stake_usd: a.money_at_stake && a.money_at_stake.usd, why: a.why })), null, 'research-plan.csv') })],
      foot: el('div', { class: 'row', style: { gap: '14px' } }, UI.rubricLegend(), el('span', { class: 'micro faint', text: 'Ranking: critical first by stake, then rubric total, severity, stake, days open. "Not now" snoozes 14 days.' })),
      empty: 'No open finding on this desk for the window. The desk below shows the gaps still worth a look.',
    }));
    loadParked();
    loadCalendar();
    if (connect.length) {
      document.getElementById('plan').append(el('div', { class: 'card flat', style: { marginTop: '10px' } },
        el('div', { class: 'sec-head' }, el('h2', { text: 'Connect first: ' + connect.length + ' rules wait on a source' }),
          el('span', { class: 'sub', text: 'Person tasks in Setup, read-only keys. They never crowd out work that can start today.' })),
        el('div', { class: 'stack' }, connect.map((a) => UI.actionCard(a, { compact: true, screen: SLUG })))));
    }
  }

  // ---------- 2. what is wrong ----------
  function evidenceLine(e) {
    const v = e.value == null ? NA : fmt.unit(e.value, e.unit === 'ratio' ? '%' : e.unit === 'usd' ? '$' : e.unit === 'count' ? 'n' : e.unit);
    const b = e.baseline == null ? '' : ' against ' + fmt.unit(e.baseline, e.unit === 'ratio' ? '%' : e.unit === 'usd' ? '$' : e.unit === 'count' ? 'n' : e.unit) + (e.baseline_kind ? ' (' + pretty(e.baseline_kind) + ')' : '');
    return el('span', null, pretty(e.metric) + ' ', el('b', { text: v }), b + ', ' + e.window);
  }
  function findingCard(f) {
    const a = actionFor(f.id);
    const card = el('div', { class: 'finding' });
    card.append(el('div', { class: 'tags' }, chip(f.severity, SEV_TONE[f.severity]), f.status === 'unavailable' ? chip('needs a source') : null,
      f.confidence != null && f.confidence < 0.3 ? chip('weak evidence', 'warn') : null, f.entity && f.entity.label ? chip(f.entity.label) : null));
    card.append(el('div', { text: f.sentence }));
    if (f.evidence && f.evidence.length) card.append(el('div', { class: 'ev' }, f.evidence.map(evidenceLine)));
    if (f.unavailable) card.append(el('div', { class: 'ev' }, el('span', { text: 'Needs: ' + (f.unavailable.inputs || []).join(', ') + '. ' + (f.unavailable.fix || '') })));
    card.append(el('div', { class: 'money', text: f.money_at_stake ? fmt.money(f.money_at_stake.usd) + ' at stake = ' + f.money_at_stake.formula + ' (' + Object.entries(f.money_at_stake.inputs || {}).map(([k, v]) => k + ' ' + v).join(', ') + '), ' + f.money_at_stake.window
      : 'money at stake unavailable: ' + (f.money_reason || 'no baseline') }));
    card.append(el('div', { class: 'row' }, a ? el('button', { class: 'btn soft xs', type: 'button', text: 'Fix: ' + a.title, onclick: () => openAction(a) }) : el('span', { class: 'micro na', text: 'no action mapped yet' })));
    return card;
  }
  const SHOW_PER_GROUP = 2;
  function loadWrong(o) {
    const groups = o.wrong || [];
    const n = groups.reduce((s, g) => s + g.findings.length, 0);
    document.getElementById('wrong-title').textContent = n ? 'What is wrong, ranked: ' + n + ' finding' + (n === 1 ? '' : 's') + ' across ' + groups.length + ' rules' : 'Nothing is wrong on this desk today';
    if (!groups.length) { mount('#wrong', el('p', { class: 'muted', text: 'No rule fired for the window. The desk below still shows where the gaps are.' })); return; }
    const counts = {};
    groups.forEach((g) => g.findings.forEach((f) => { const k = f.status === 'unavailable' ? 'unavailable' : f.severity; counts[k] = (counts[k] || 0) + 1; }));
    const list = el('div', { class: 'stack' });
    const render = (sev) => {
      mount(list, ...groups.map((g) => {
        const fs = g.findings.filter((f) => sev === 'all' || (sev === 'unavailable' ? f.status === 'unavailable' : f.severity === sev && f.status !== 'unavailable'));
        if (!fs.length) return null;
        const card = el('div', { class: 'card flat wrong-group' });
        card.append(el('div', { class: 'g-head' }, el('h4', { text: g.name }), chip(g.rule_id, 'mono'), chip(g.severity, SEV_TONE[g.severity]), el('span', { class: 'micro muted', text: fs.length + ' finding' + (fs.length === 1 ? '' : 's') })));
        fs.slice(0, SHOW_PER_GROUP).forEach((f) => card.append(findingCard(f)));
        if (fs.length > SHOW_PER_GROUP) {
          const more = el('div', { class: 'stack', hidden: true }, fs.slice(SHOW_PER_GROUP).map(findingCard));
          const btn = el('button', { class: 'btn quiet xs', type: 'button', text: 'Show ' + (fs.length - SHOW_PER_GROUP) + ' more' });
          btn.addEventListener('click', () => { more.hidden = !more.hidden; btn.textContent = more.hidden ? 'Show ' + (fs.length - SHOW_PER_GROUP) + ' more' : 'Show fewer'; });
          card.append(more, btn);
        }
        return card;
      }).filter(Boolean));
    };
    const pills = UI.pills({ items: [{ key: 'all', label: 'All', n }].concat(['critical', 'high', 'medium', 'low', 'unavailable'].filter((k) => counts[k]).map((k) => ({ key: k, label: k === 'unavailable' ? 'Needs a source' : k[0].toUpperCase() + k.slice(1), n: counts[k] }))), current: 'all', onChange: render });
    mount('#wrong', pills, list);
    render('all');
  }

  // ---------- 3 and 4. actions ----------
  const TOP_CARDS = 10;
  function loadActions() {
    const list = state.actions.filter((a) => a.status !== 'unavailable');
    if (!list.length) { mount('#actions', el('p', { class: 'muted', text: 'No open action.' })); return; }
    const top = list.slice(0, TOP_CARDS), rest = list.slice(TOP_CARDS);
    const parts = top.flatMap((a, i) => [UI.actionCard(a, { expanded: i === 0, screen: SLUG }), coversList(a, true)].filter(Boolean));
    if (rest.length) {
      parts.push(el('div', { class: 'card scroll' }, el('h4', { text: rest.length + ' more, below the top ' + TOP_CARDS }), UI.verdictTable({
        columns: [{ key: 'rank', label: '#', unit: 'n' }, { key: 'title', label: 'Action' }, { key: 'ownerText', label: 'Owner' }, { key: 'kind', label: 'Artefact' }, { key: 'total', label: 'Score', align: 'right', format: (v) => v == null ? NA : Math.round(v) + ' /100' }, { key: 'stake', label: 'Stake', align: 'right', format: (v) => v == null ? NA : fmt.money(v) }],
        rows: rest.map((a, i) => ({ rank: TOP_CARDS + i + 1, title: a.title, ownerText: { agent: 'agent does it', agent_drafts: 'agent drafts, you approve', person: 'a person does it' }[a.owner] || a.owner, kind: pretty((a.artefact || {}).kind), total: (a.rubric || {}).total, stake: (a.money_at_stake || {}).usd, severity: a.severity, rule_id: a.rule_id, actions: [{ label: 'Open', onClick: () => openAction(a) }] })),
        verdict: { at: 1, kind: (r) => r.severity === 'high' || r.severity === 'critical' ? 'fix' : r.severity === 'low' ? 'na' : 'watch', text: (r) => r.severity, reason: (r) => r.rule_id },
        actions: { label: 'Do', onClick: () => {} }, sort: false })));
    }
    mount('#actions', ...parts);
  }

  // ---------- 5. the desk ----------
  function points(v) { return v == null ? NA : (v > 0 ? '+' : '') + v.toFixed(1) + ' pt'; }
  function demandBlock(d, w) {
    if (d.demand_unavailable) return UI.emptyState({ screen: SLUG, title: 'No monthly product sales', text: d.demand_unavailable.reason, missing: [d.demand_unavailable.fix] });
    const rows = (d.demand || []).map((r) => {
      const key = r.line.toLowerCase().replace(/ /g, '-');
      const a = actionFor(SLUG + '.PROD-R01.' + key) || actionFor(SLUG + '.PROD-R02.' + key) || actionFor(SLUG + '.PROD-R03.' + key);
      return Object.assign({}, r, { actions: [a ? { label: 'Open action', onClick: () => openAction(a) } : { label: 'No action', cls: 'quiet', onClick: () => {} }] });
    });
    const losing = rows.filter((r) => r.status !== 'holding');
    const t = UI.verdictTable({
      columns: [
        { key: 'line', label: 'Line' }, { key: 'skus', label: 'SKUs', unit: 'n' }, { key: 'units', label: 'Units 3 mo', unit: 'n' },
        { key: 'growth', label: 'vs last year', unit: '%' }, { key: 'gap_points', label: 'vs store', align: 'right', format: points },
        { key: 'net_sales', label: 'Net sales 3 mo', unit: '$' },
        { key: 'rating', label: 'Stars', align: 'right', format: (v) => v == null ? 'no record' : v.toFixed(2) },
        { key: 'low_star_share', label: '1 and 2 star', align: 'right', format: (v) => v == null ? 'no record' : fmt.pct(v) }],
      rows,
      verdict: { at: 1, kind: (r) => r.status === 'down' ? 'stop' : r.status === 'losing share' ? 'fix' : (r.low_star_share != null && r.low_star_share >= 0.1) ? 'watch' : 'keep',
        text: (r) => r.status === 'holding' ? ((r.low_star_share != null && r.low_star_share >= 0.1) ? 'Reviews' : 'Holding') : r.status === 'down' ? 'Down' : 'Losing share',
        reason: (r) => 'growth ' + (r.growth == null ? NA : fmt.pct(r.growth)) + ', store ' + (d.store_growth == null ? NA : fmt.pct(d.store_growth)) },
      actions: { label: 'Do', onClick: () => {} },
      sort: { key: 'units', dir: 'desc' },
    });
    return el('div', null, el('p', { class: 'small muted', text: 'Units in ' + w.months.join(' to ') + ' against ' + w.year_ago.join(' to ') + '. "vs store" is the line\'s growth minus the whole store\'s, in points. Stars and low-star share are public site totals.' }),
      el('div', { class: 'card scroll' }, t),
      gapLine(losing.length ? losing.length + ' of ' + rows.length + ' lines sold less or grew slower than the store.' : 'Every line grows with the store. The gaps here are in reviews and in what is missing from the range, not in units.'));
  }
  function priceBlock(p) {
    if (p.unavailable) {
      const comps = (p.competitors || []).map((c) => c.name + ' ' + (c.median != null ? fmt.money(c.median) : 'no median')).join(', ');
      return el('div', null, UI.emptyState({ screen: SLUG, title: 'No catalog connected', text: p.reason + '. Competitor medians per pair are on file: ' + comps + '.', missing: [p.fix] }));
    }
    const comps = (p.competitors || []).map((c) => c.name + ' ' + (c.median != null ? fmt.money(c.median) : 'no median')).join(', ');
    const below = p.rows.filter((r) => r.position === 'below');
    return el('div', null,
      el('p', { class: 'small muted', text: 'Per pair: ' + p.basis + '. Competitor medians: ' + comps + '.' }),
      el('div', { class: 'card scroll' }, UI.verdictTable({
        columns: [{ key: 'line', label: 'Line' }, { key: 'category', label: 'Category' }, { key: 'packs', label: 'Packs', unit: 'n' },
          { key: 'per_pair_low', label: 'Per pair, low', unit: '$' }, { key: 'per_pair_high', label: 'Per pair, high', unit: '$' },
          { key: 'band', label: 'Competitor band', align: 'right', format: (v, r) => r.band_low == null ? 'no competitor on file' : fmt.money(r.band_low) + ' to ' + fmt.money(r.band_high) }],
        rows: p.rows.map((r) => Object.assign({ band: r.band_low }, r)),
        verdict: { at: 1, kind: (r) => r.position === 'below' ? 'fix' : r.position === 'above' ? 'watch' : r.position === 'inside' ? 'keep' : 'na', text: (r) => r.position ? r.position : 'not compared', reason: (r) => r.position ? 'per pair ' + fmt.money(r.per_pair_low) + ' to ' + fmt.money(r.per_pair_high) : 'no competitor band for this category' },
        sort: false })),
      gapLine(below.length ? below.length + ' sock lines sell under the lowest competitor median. Either the price frame is "worth more" and the proof is missing, or the packs hide the per-pair price.' : 'No sock line prices under the competitor band.'));
  }
  function list(items) { return el('ul', null, (items.length ? items : ['none on file']).map((t) => el('li', { text: t }))); }
  function reviewBlock(rows) {
    if (!rows.length) return UI.emptyState({ screen: SLUG, title: 'No reviews on file', text: 'The brand brain has no review totals per line yet.', missing: ['reviews'] });
    return el('div', null, el('div', { class: 'reviews' }, rows.map((r) => el('div', { class: 'card review' },
      el('h4', { text: r.line }),
      el('div', { class: 'stat', text: (r.rating != null ? r.rating.toFixed(2) + ' stars, ' : '') + fmt.int(r.reviews) + ' reviews, ' + fmt.pct(r.low_star_share) + ' are 1 or 2 stars' }),
      el('div', { class: 'kicker', text: 'What works' }), list(r.works),
      el('div', { class: 'kicker', text: 'What fails' }), list(r.fails),
      r.ladders.length ? el('div', { class: 'kicker', text: 'Objection ladder rungs from these reviews' }) : null,
      r.ladders.map((l) => el('div', { class: 'rung', text: pretty(l.theme) + ': ' + l.rungs.map((g) => 'rung ' + g.level + ', "' + g.doubt + '", ' + g.one_star + ' one-star' + (g.proof ? '' : ', no proof')).join('; ') })),
      (function () { const a = actionFor(SLUG + '.PROD-R02.' + r.line.toLowerCase().replace(/ /g, '-')); return a ? el('div', { class: 'row', style: { marginTop: '6px' } }, el('button', { class: 'btn soft xs', type: 'button', text: 'Fix the top complaint', onclick: () => openAction(a) })) : null; })()))),
      gapLine('Lines with a low-star share over 10 percent and 1.5 times the brand median carry a fix action. The rest are read for the next SKU\'s angle.'));
  }
  async function openBrief(cid) {
    let b;
    try { b = await api(BASE + 'candidates/' + encodeURIComponent(cid) + '/brief' + Q); } catch (e) { alert('Brief unavailable: ' + e.message); return; }
    UI.panel({ title: 'Brief: ' + b.name, tools: [UI.copyButton({ label: 'Copy brief', text: () => b.text })],
      body: el('div', { class: 'stack' }, el('p', { class: 'micro muted', text: 'One page from every block of the desk: the angle and proof for creative, the spec, margin and cash timing for sourcing. Numbers come from the blocks; nothing is written here.' }),
        el('pre', { class: 'small', style: { whiteSpace: 'pre-wrap', margin: 0 }, text: b.text })) });
  }

  async function candidatePost(path, body) {
    try { await api(BASE + path + Q, { method: 'POST', body }); load(); }
    catch (e) { alert('Could not save: ' + e.message); }
  }
  function pipelineBlock(p) {
    const floor = p.floor_pct != null ? 'The brand floor is ' + p.floor_pct + ' percent, from ' + p.floor_source + '.' : 'No floor on file: enter a target contribution margin on the setup screen.';
    const rows = p.rows || [];
    const ho = p.handoff || {};
    const handoffLine = el('p', { class: 'micro muted', text: 'Hand-off (events contract): ' + (ho.rows || 0) + ' candidates in ' + (ho.file || 'product_candidates') + ', ' + (ho.go || 0) + ' at go, ' + (ho.with_cost || 0) + ' with a landed cost estimate; read by ' + ((ho.read_by || []).join(' and ') || 'offers and supply') + '. ' + ((p.proposed_tests || []).length ? (p.proposed_tests || []).length + ' proposed test' + ((p.proposed_tests || []).length === 1 ? '' : 's') + ' for the experiment registry: ' + (p.proposed_tests || []).map((x) => x.name + ' (read ' + fmt.date(x.read_point) + ')').join(', ') + '.' : 'A go writes a proposed test for the experiment registry.') });
    const funnel = rows.length ? Charts.funnel({ title: 'Candidates by stage reached', stages: (p.funnel || []).map((f) => ({ label: f.stage, value: f.n })), unit: 'n',
      note: 'A candidate at a later stage counts at every stage before it. ' + (p.rule || '') + '.' })
      : el('div', null, el('h4', { text: 'Candidates by stage reached' }), el('p', { class: 'muted small', text: 'No candidate on file for this brand yet. Screen one in on the right; the funnel fills from there.' }));
    const stageNext = (r) => { const i = (p.stages || []).indexOf(r.stage); return i >= 0 && i < p.stages.length - 1 ? p.stages[i + 1] : null; };
    const vrows = rows.map((r) => { const acts = (r.finding_ids || []).map(actionFor).filter(Boolean); const nx = stageNext(r); return Object.assign({}, r, {
      stageText: r.stage + (r.closed ? '' : r.days_left != null ? (r.days_left < 0 ? ', ' + Math.abs(r.days_left) + ' d over the box' : ', ' + r.days_left + ' d left') : ''),
      checks: (p.checks || []).map((c) => pretty(c) + ' ' + ((r.screen_result || {})[c] || 'not run')).join(', '),
      angle: r.angle_text || 'no angle yet', price: r.planned_price, hours: r.hours_logged,
      actions: [].concat(acts.length ? [{ label: acts[0].rule_id === 'PROD-R15' ? 'Kill or fix' : 'Decide', onClick: () => openAction(acts[0]) }] : [],
        [{ label: 'Brief', cls: 'quiet', onClick: () => openBrief(r.candidate_id) }],
        !r.closed && nx ? [{ label: 'Advance to ' + nx, cls: 'quiet', onClick: () => candidatePost('candidates/' + r.candidate_id, { stage: nx, who: 'person' }) }] : [],
        !r.closed ? [{ label: 'Log 1 h', cls: 'quiet', onClick: () => candidatePost('candidates/' + r.candidate_id, { hours_add: 1, who: 'person' }) }, { label: 'Kill', cls: 'quiet', onClick: () => { if (confirm('Kill ' + r.name + '? It stays killed 90 days.')) candidatePost('candidates/' + r.candidate_id, { stage: 'killed', who: 'person' }); } }] : []) }); });
    const t = UI.verdictTable({
      columns: [{ key: 'name', label: 'Candidate' }, { key: 'category', label: 'Category' }, { key: 'stageText', label: 'Stage and box' }, { key: 'checks', label: 'Fast checks' }, { key: 'angle', label: 'Angle' },
        { key: 'price', label: 'Planned price', unit: '$' }, { key: 'hours', label: 'Hours', align: 'right', format: (v) => v == null ? NA : v.toFixed(1) }],
      rows: vrows,
      verdict: { at: 1, kind: (r) => r.closed ? (r.stage === 'go' ? 'scale' : 'na') : (r.failed_checks || []).length >= 2 ? 'stop' : r.over_box ? 'fix' : 'keep',
        text: (r) => r.closed ? (r.stage === 'go' ? 'Go' : 'Killed') : (r.failed_checks || []).length >= 2 ? 'Failed screen' : r.over_box ? 'Over the box' : 'In the box',
        reason: (r) => (r.failed_checks || []).length + ' checks failed, ' + (r.age_days == null ? NA : r.age_days + ' days since screen-in against a ' + r.time_box_days + '-day box') },
      actions: { label: 'Do', onClick: () => {} }, sort: false, empty: 'No candidates yet. Screen one from a gap above, or add one here.' });
    const name = el('input', { class: 'text sm', placeholder: 'candidate name', style: { flex: '1 1 220px' } });
    const cat = el('input', { class: 'text sm', placeholder: 'category, like socks', style: { maxWidth: '160px' } });
    const price = el('input', { class: 'text sm', placeholder: 'planned price', type: 'number', style: { maxWidth: '130px' } });
    const box = el('input', { class: 'text sm', placeholder: 'time box, days', type: 'number', value: '10', style: { maxWidth: '130px' } });
    const angle = el('input', { class: 'text sm', placeholder: 'angle in one line (optional)', style: { flex: '1 1 260px' } });
    const add = el('button', { class: 'btn primary sm', type: 'button', text: 'Screen it in', onclick: () => { if (!name.value.trim()) { alert('Give the candidate a name.'); return; } candidatePost('candidates', { name: name.value, category: cat.value || 'socks', planned_price: price.value || null, time_box_days: box.value || 10, angle_text: angle.value || null, who: 'person' }); } });
    const orient = UI.orientation([{ label: 'open', value: p.open, unit: 'n' }, { label: 'over the box', value: p.over_box, unit: 'n', tone: p.over_box ? 'bad' : 'good' }, { label: 'hours logged', value: p.hours, unit: 'n' }, { label: 'margin floor', value: p.floor_pct == null ? null : p.floor_pct / 100, unit: '%' }]);
    return el('div', { class: 'stack' }, orient, handoffLine,
      el('div', { class: 'grid two' }, el('div', { class: 'card' }, funnel), el('div', { class: 'card flat' }, el('h4', { text: 'Screen a candidate in' }), el('div', { class: 'row', style: { gap: '6px', flexWrap: 'wrap' } }, name, cat, price, box), el('div', { class: 'row', style: { gap: '6px', marginTop: '6px' } }, angle, add),
        el('p', { class: 'micro faint', text: 'It lands at screened with a time box. The 3 fast checks run when the agent screens it; you can set them from the card. Margin gate: ' + p.gate_rule + ' ' + floor }))),
      el('div', { class: 'card scroll' }, t),
      gapLine(p.over_box ? p.over_box + ' candidates are past their time box. Each carries a decide-or-kill action.' : (p.open ? 'Every open candidate is inside its box.' : 'The pipeline is empty. Every gap above with a screen action can fill it.'),
        rows.find((r) => r.finding_ids && r.finding_ids.length) ? { label: 'Decide the first', onClick: () => { const r = rows.find((x) => x.finding_ids && x.finding_ids.length); const a = actionFor(r.finding_ids[0]); if (a) openAction(a); } } : null));
  }

  function trendsBlock(t, mix) {
    if (!t.on_file) return UI.emptyState({ screen: SLUG, title: 'No web pass on file', text: 'Run the research web pass for this brand. Every number it keeps carries a url and a date.', missing: ['web_pass'] });
    const cite = (m) => (m.sources && m.sources[0]) ? (m.sources[0].publisher + ', ' + m.sources[0].date) : 'no source';
    const rows = t.markets.map((m) => ({
      label: m.label, sub: (m.size_usd != null ? fmt.money(m.size_usd) + (m.size_year ? ' in ' + m.size_year : '') : 'size unavailable') + (m.cagr_pct != null ? ', ' + m.cagr_pct + ' percent a year, ' + (m.cagr_window || '') : ', growth unavailable') + '. ' + cite(m),
      values: (m.series && m.series.length) ? m.series.map((p) => p.value_usd) : (m.size_usd != null ? [m.size_usd] : []), unit: '$', higher_is_better: true, delta_label: (m.series && m.series.length > 1) ? m.series[0].year + ' to ' + m.series[m.series.length - 1].year : '' }));
    const strip = Charts.trendStrip({ title: 'Public markets, ' + t.captured_at, rows, note: (t.note || '') + ' Two-point lines are a forecast from the size and the growth rate, not history.' });
    const byCat = {};
    for (const m of t.markets) if (m.our_category && (m.key.indexOf('_us') > 0 || m.key === 'basics_tshirts' || m.key === 'footwear_casual')) byCat[m.our_category] = byCat[m.our_category] || m;
    const pub = t.public_mix || [];
    const mixRows = (mix.rows || []).map((r) => {
      const m = byCat[r.category];
      const band = pub.find((p) => p.categories.indexOf(r.category) >= 0);
      const a = actionFor(SLUG + '.PROD-R04.' + r.category);
      return Object.assign({}, r, { market: m ? m.label : null, cagr: m ? m.cagr_pct : null, gap: (m && m.cagr_pct != null && r.growth != null) ? r.growth * 100 - m.cagr_pct : null,
        band: band ? fmt.pct(band.share) + ' with ' + band.categories.filter((c) => c !== r.category).join(', ') + ' (public, ' + (band.as_of || 'undated') + ')' : 'no public record',
        actions: [a ? { label: 'Close the gap', onClick: () => openAction(a) } : { label: 'No action', cls: 'quiet', onClick: () => {} }] });
    });
    const mixTable = mix.unavailable ? UI.emptyState({ screen: SLUG, title: 'No product sales by month', text: mix.reason, missing: [mix.fix] }) : UI.verdictTable({
      columns: [{ key: 'category', label: 'Our category' }, { key: 'net_share', label: 'Share of net sales, 12 mo', unit: '%' }, { key: 'growth', label: 'Unit growth, 12 mo', unit: '%' },
        { key: 'cagr', label: 'Market growth a year', align: 'right', format: (v) => v == null ? 'no market on file' : v + ' percent' }, { key: 'band', label: 'Public share record' }],
      rows: mixRows,
      verdict: { at: 1, kind: (r) => r.gap == null ? 'na' : r.gap < 0 ? 'fix' : r.gap > 10 ? 'scale' : 'keep', text: (r) => r.gap == null ? 'No market' : r.gap < 0 ? 'Behind market' : r.gap > 10 ? 'Outgrowing' : 'In line', reason: (r) => r.gap == null ? 'no public growth rate mapped to this category' : 'our growth minus market growth: ' + (r.gap > 0 ? '+' : '') + r.gap.toFixed(1) + ' points' },
      actions: { label: 'Do', onClick: () => {} }, sort: false });
    const subRows = t.markets.map((m) => { const a = actionFor(m.finding_id); return Object.assign({}, m, { size: m.size_usd, cite: cite(m), actions: [a ? { label: 'Brief it', onClick: () => openAction(a) } : { label: m.covered === false ? 'Screen it' : 'Covered', cls: 'quiet', onClick: () => { if (m.covered === false) UI.decisionRow({ capability: 'PROD-C01', screen: SLUG }); } }] }); });
    const subTable = UI.verdictTable({
      columns: [{ key: 'label', label: 'Market or lane' }, { key: 'size', label: 'Size', unit: '$' }, { key: 'cagr_pct', label: 'Growth a year', align: 'right', format: (v) => v == null ? NA : v + ' percent' },
        { key: 'covered', label: 'We sell it', format: (v) => v == null ? NA : v ? 'yes' : 'no' }, { key: 'advertised', label: 'In our active ads', format: (v) => v == null ? NA : v ? 'yes' : 'no' }, { key: 'cite', label: 'Source' }],
      rows: subRows,
      verdict: { at: 1, kind: (r) => r.covered === false && r.direction === 'up' ? 'new' : (r.covered && r.advertised === false && (r.cagr_pct >= 4 || r.key === 'gifting_socks')) ? 'fix' : r.covered && r.advertised ? 'keep' : 'watch',
        text: (r) => r.covered === false && r.direction === 'up' ? 'Not sold' : (r.covered && r.advertised === false && (r.cagr_pct >= 4 || r.key === 'gifting_socks')) ? 'Sold, not advertised' : r.covered && r.advertised ? 'Sold and advertised' : 'Watch',
        reason: (r) => 'direction ' + (r.direction || NA) + (r.drivers && r.drivers.length ? '; ' + r.drivers.slice(0, 2).join('; ') : '') },
      actions: { label: 'Do', onClick: () => {} }, sort: false });
    const gaps = subRows.filter((r) => r.covered && r.advertised === false && (r.cagr_pct >= 4 || r.key === 'gifting_socks'));
    return el('div', { class: 'stack' },
      el('div', { class: 'grid two' }, el('div', { class: 'card' }, strip), el('div', { class: 'card scroll' }, el('h4', { text: 'Our mix against the market, 12 whole months to ' + (mix.last || NA) }), (mix.basis && mix.basis !== 'products_monthly') || mix.growth_note ? el('p', { class: 'micro muted', text: (mix.basis && mix.basis !== 'products_monthly' ? 'Built from ' + mix.basis + '. ' : '') + (mix.growth_note ? mix.growth_note.charAt(0).toUpperCase() + mix.growth_note.slice(1) + '.' : '') }) : null, mixTable)),
      el('div', { class: 'card scroll' }, el('h4', { text: 'Lanes: sold, advertised, or neither' }), subTable),
      gapLine(gaps.length ? gaps.length + ' growing lanes are sold and not named in any active ad: ' + gaps.map((g) => g.label).join(', ') + '. Each carries an ad brief in the plan.' : 'Every growing lane the brand sells has an active ad naming it.',
        gaps.length ? { label: 'Brief the first', onClick: () => { const a = actionFor(gaps[0].finding_id); if (a) openAction(a); } } : null));
  }

  function lanesBlock(rows) {
    if (!rows || !rows.length) return UI.emptyState({ screen: SLUG, title: 'No competitor ad signals', text: 'The brain holds no Ad Library records for competitor pages yet.', missing: ['ad_library'] });
    const vrows = rows.map((r) => { const a = actionFor(r.finding_id); return Object.assign({}, r, {
      who: r.competitors.map((c) => c.name + ' (' + (c.active_ads == null ? '?' : c.active_ads) + ' ads, ' + (c.longest_run_days == null ? '?' : c.longest_run_days) + ' d)').join('; ') || 'none',
      launched: r.launches.length ? r.launches.map((l) => l.brand + ': ' + l.what + (l.date ? ' (' + l.date + (l.price_usd != null ? ', ' + fmt.money(l.price_usd) : '') + ')' : '')).join(' | ') : 'none in the web pass',
      soldText: r.sold == null ? NA : r.kind === 'proof' ? (r.sold ? 'proof on file' : 'no proof') : (r.sold ? 'yes' : 'no'),
      advText: r.advertised == null ? NA : r.advertised ? 'yes' : 'no',
      actions: [a ? { label: 'Brief it', onClick: () => openAction(a) } : { label: r.verdict === 'follow' ? 'Covered' : r.verdict === 'watch' ? 'Watch' : 'Ignore', cls: 'quiet', onClick: () => {} }] }); });
    const t = UI.verdictTable({
      columns: [{ key: 'label', label: 'Lane' }, { key: 'competitors_n', label: 'Competitors pushing it', unit: 'n' }, { key: 'ads_sum', label: 'Their active ads', unit: 'n' },
        { key: 'long_run_n', label: 'With an ad live 30 d+', unit: 'n' }, { key: 'who', label: 'Who' }, { key: 'launched', label: 'Launched, last 24 months' },
        { key: 'soldText', label: 'We sell it' }, { key: 'advText', label: 'In our active ads' }],
      rows: vrows,
      verdict: { at: 1, kind: (r) => r.verdict === 'follow' ? (r.advertised ? 'keep' : 'fix') : r.verdict === 'watch' ? 'watch' : 'na',
        text: (r) => r.verdict === 'follow' ? (r.advertised ? 'Follow, covered' : 'Follow') : r.verdict === 'watch' ? 'Watch' : 'Ignore',
        reason: (r) => r.competitors_n + ' pushing, ' + r.long_run_n + ' with a long runner; follow needs 2 and 1' },
      actions: { label: 'Do', onClick: () => {} }, sort: false });
    const gaps = rows.filter((r) => r.verdict === 'follow' && !r.advertised);
    return el('div', null, el('div', { class: 'card scroll' }, t),
      el('p', { class: 'micro faint', text: 'Rule: follow when 2 or more competitor pages push the lane and one has an ad live 30 days or more; ignore when every ad on it is under 14 days old and nothing launched; else watch. Competitor ads are signals, never copied. Launches come from the public web pass with a url per row.' }),
      gapLine(gaps.length ? gaps.length + ' lanes to follow have no active ad of ours: ' + gaps.map((g) => g.label.toLowerCase()).join(', ') + '.' : 'Every lane worth following has an active ad of ours.',
        gaps.length ? { label: 'Brief the first', onClick: () => { const a = actionFor(gaps[0].finding_id); if (a) openAction(a); } } : null));
  }

  function conversationBlock(c) {
    const rows = (c && c.rows) || [];
    if (!rows.length) return UI.emptyState({ screen: SLUG, title: 'No conversation on file', text: 'The brain holds no objection ladders or Reddit language yet.', missing: ['reviews', 'reddit'] });
    const vrows = rows.map((r) => { const a = actionFor(r.finding_id); return Object.assign({}, r, {
      reviews: r.review_complaints + r.review_praise ? r.review_complaints + ' vs ' + r.review_praise : 'none',
      sources: Object.keys(r.by_source).length ? Object.entries(r.by_source).filter(([k, v]) => v).sort((a, b) => b[1] - a[1]).map(([k, v]) => pretty(k) + ' ' + v).join(', ') : 'reviews not split',
      reddit: r.reddit_mentions ? r.reddit_mentions + ' (' + fmt.int(r.reddit_upvotes) + ' upvotes)' : 'none',
      social: r.social_posts == null ? NA : r.social_posts + ' posts, ' + fmt.int(r.social_engagement || 0) + ' likes and comments',
      site: r.answered_on_site == null ? NA : r.answered_on_site ? 'yes' : 'no', ads: r.answered_in_ads == null ? NA : r.answered_in_ads ? 'yes' : 'no',
      doubt: r.top_rung ? '"' + r.top_rung.doubt + '" (' + r.top_rung.one_star + ' one-star' + (r.top_rung.proof ? '' : ', no proof') + ')' : '',
      actions: [a ? { label: 'Answer it', onClick: () => openAction(a) } : { label: r.verdict === 'strength' ? 'Lead with it' : 'Watch', cls: 'quiet', onClick: () => {} }] }); });
    const t = UI.verdictTable({
      columns: [{ key: 'label', label: 'Theme' }, { key: 'reviews', label: 'Complaint vs praise quotes' }, { key: 'praise_share', label: 'Praise share', unit: '%' },
        { key: 'sources', label: 'Review sources' }, { key: 'reddit', label: 'Reddit' }, { key: 'social', label: 'Instagram pull' }, { key: 'doubt', label: 'Top doubt' },
        { key: 'site', label: 'Site answers it' }, { key: 'ads', label: 'Active ad answers it' }],
      rows: vrows,
      verdict: { at: 1, kind: (r) => r.verdict === 'gap' ? 'fix' : r.verdict === 'strength' ? 'scale' : r.verdict === 'answered' ? 'keep' : 'watch',
        text: (r) => r.verdict === 'gap' ? 'Unanswered' : r.verdict === 'strength' ? 'Strength' : r.verdict === 'answered' ? 'Answered' : 'Watch',
        reason: (r) => 'volume ' + r.volume + '; a gap needs 10 quotes, more complaints than praise, and no ad answer' },
      actions: { label: 'Do', onClick: () => {} }, sort: false });
    const gaps = rows.filter((r) => r.verdict === 'gap');
    const soc = c.social;
    const socialCard = el('div', { class: 'card flat' });
    if (!soc) socialCard.append(el('h4', { text: 'Instagram keyword pull' }), el('p', { class: 'muted small', text: 'No pull on file. Run social_pull.py for this brand; it stays under the brand\'s Apify caps and stores no usernames.' }));
    else {
      socialCard.append(el('h4', { text: 'Instagram keyword pull, ' + soc.captured_at }),
        el('div', { class: 'row', style: { gap: '6px' } }, (soc.hashtags || []).map((h) => chip('#' + h)), chip(soc.mode === 'live' ? 'live run' : 'mock run, invented sample', soc.mode === 'live' ? 'good' : 'warn'), chip((soc.items || 0) + ' posts'), chip(soc.usd != null ? fmt.money(soc.usd) + ' spent' : 'cost unavailable')),
        el('p', { class: 'micro muted', text: soc.note + (soc.mode !== 'live' ? ' This block was filled by the mock run because the live pull could not be authorised from this session. The numbers in it are a sample shape, not the market.' : '') }),
        soc.co_hashtags && soc.co_hashtags.length ? el('div', { class: 'small' }, el('b', { text: 'Tags that travel with ours: ' }), soc.co_hashtags.slice(0, 10).map((x) => '#' + x[0] + ' ' + x[1]).join(', ')) : null,
        el('ul', { class: 'small', style: { margin: '6px 0 0', paddingLeft: '18px' } }, (soc.samples || []).slice(0, 6).map((sm) => el('li', null, el('span', { class: 'muted', text: '#' + sm.hashtag + ', ' + fmt.int(sm.likes) + ' likes: ' }), '"' + sm.quote + '"'))));
    }
    return el('div', { class: 'stack' }, el('div', { class: 'card scroll' }, t), socialCard,
      el('p', { class: 'micro faint', text: 'Review quotes are the objection ladders built from the brand site, Amazon, Trustpilot, retailers and Reddit. Reddit language shapes hooks and is never quoted as a testimonial. Usernames are never stored.' }),
      gapLine(gaps.length ? gaps.length + ' themes are complaint-led and no active ad answers them: ' + gaps.map((g) => g.label.toLowerCase()).join(', ') + '. Each has an ad brief and a page section in the plan.' : 'Every complaint-led theme has an active ad answering it.',
        gaps.length ? { label: 'Answer the first', onClick: () => { const a = actionFor(gaps[0].finding_id); if (a) openAction(a); } } : null));
  }

  function preferencesBlock(rows) {
    if (!rows || !rows.length) return UI.emptyState({ screen: SLUG, title: 'No preference survey on file', text: 'The web pass keeps public survey numbers on shifting preferences. Run it for this brand.', missing: ['web_pass'] });
    const vrows = rows.map((r) => {
      const a = actionFor(r.finding_id);
      const ads5 = actionFor(SLUG + '.PROD-R05.' + { sustainability: 'sustainable_apparel', gifting: 'gifting_socks' }[r.key]) || null;
      const ads6 = actionFor(SLUG + '.PROD-R06.' + { durability: 'guarantee', natural_fibres: 'merino', gifting: 'gifting' }[r.key]) || null;
      const ads7 = actionFor(SLUG + '.PROD-R07.' + { durability: 'durability' }[r.key]) || null;
      const prove = ads6 || ads7 || ads5;
      return Object.assign({}, r, { dir: r.direction === 'up' ? 'rising' : r.direction === 'down' ? 'falling' : r.direction === 'flat' ? 'holding' : NA,
        site: r.on_site == null ? NA : r.on_site ? 'yes' : 'no', ads: r.in_ads == null ? NA : r.in_ads ? 'yes' : 'no',
        rivals: r.competitors.length ? r.competitors.join(', ') : 'none seen',
        talk: r.conversation ? r.conversation.complaints + ' complaints, ' + r.conversation.praise + ' praise, ' + r.conversation.reddit + ' Reddit' : 'no theme mapped',
        actions: [a ? { label: 'Decide our position', onClick: () => openAction(a) } : prove ? { label: 'Prove it in an ad', onClick: () => openAction(prove) } : { label: r.verdict === 'lead' ? 'Leading' : 'Watch', cls: 'quiet', onClick: () => {} }] });
    });
    const t = UI.verdictTable({
      columns: [{ key: 'label', label: 'Preference' }, { key: 'dir', label: 'Direction' }, { key: 'evidence', label: 'What the public numbers say' }, { key: 'cite', label: 'Source' },
        { key: 'site', label: 'Our records claim it' }, { key: 'ads', label: 'Our active ads say it' }, { key: 'rivals', label: 'Competitors claiming it' }, { key: 'talk', label: 'Category conversation' }],
      rows: vrows,
      verdict: { at: 1, kind: (r) => r.verdict === 'gap' ? 'fix' : r.verdict === 'prove' ? 'watch' : r.verdict === 'lead' ? 'keep' : 'na',
        text: (r) => r.verdict === 'gap' ? 'Gap' : r.verdict === 'prove' ? 'Prove it' : r.verdict === 'lead' ? 'Leading' : 'Watch',
        reason: (r) => r.verdict === 'gap' ? 'competitors claim it, we hold no record' : r.verdict === 'prove' ? 'we hold the proof and no ad says it' : r.verdict === 'lead' ? 'claimed on site and in ads' : 'not rising, or nobody claims it' },
      actions: { label: 'Do', onClick: () => {} }, sort: false });
    const gaps = rows.filter((r) => r.verdict === 'gap'), prove = rows.filter((r) => r.verdict === 'prove');
    return el('div', null, el('div', { class: 'card scroll' }, t),
      el('p', { class: 'micro faint', text: 'Rule: leading when our records and our active ads carry it; prove it when we hold the proof and no ad says it; gap when a competitor claims it and we hold no record; else watch. A claim is never invented: the gap action decides claim, counter or leave.' }),
      gapLine((gaps.length ? gaps.length + ' preference' + (gaps.length === 1 ? '' : 's') + ' competitors claim and we do not: ' + gaps.map((g) => g.label.toLowerCase()).join(', ') + '. ' : '') + (prove.length ? prove.length + ' we hold the proof for and never say in an ad: ' + prove.map((g) => g.label.toLowerCase()).join(', ') + '.' : ''),
        gaps.length ? { label: 'Decide the first', onClick: () => { const a = actionFor(gaps[0].finding_id); if (a) openAction(a); } } : null));
  }

  function mapBlock(m) {
    if (!m || !m.enough) return UI.emptyState({ screen: SLUG, title: 'Not enough priced competitor pages', text: 'The map needs 3 pages with a price band and hook types in the brain.', missing: ['ad_library'] });
    const a9 = actionFor(SLUG + '.PROD-R09.brand');
    const pts = m.points.map((p) => ({ label: p.label, x: p.x, y: p.y, us: p.us, size: p.size, note: (p.hooks || []).slice(0, 4).join(', ') + (p.price_basis ? '. Price: ' + p.price_basis : '') }));
    const q = m.quadrants || {};
    const chart = Charts.positioningMap({
      title: 'Price against proof, ' + m.points.length + ' pages sized by active ads',
      x: { label: (m.x || {}).label || 'price per pair', lo: 'cheaper per pair', hi: 'dearer per pair', unit: '$' },
      y: { label: (m.y || {}).label || 'proof share', lo: 'sells on feel', hi: 'sells on proof', unit: '%' },
      points: pts, midX: m.mid_x, midY: m.mid_y, quadrants: [q.tl, q.tr, q.bl, q.br], usLabel: (m.ours || {}).label || 'us', themLabel: 'competitor pages',
      note: 'Proof share is the share of a page\'s hook types that carry a guarantee, a lab or review claim, a testimonial or made in USA. Price is the median per pair from each brand\'s public catalog; ours is ' + ((m.ours || {}).price_basis || NA) + '. Ad counts are Ad Library signals, not spend.' });
    const ourQ = Object.entries(m.members || {}).find(([k, v]) => v.indexOf((m.ours || {}).label) >= 0);
    const empty = (m.empty || []).map((k) => q[k]);
    const frames = (m.frames || []).map((f) => pretty(f.frame) + ' ' + f.mentions + (f.mentions_brand ? ' (brand named ' + f.mentions_brand + ')' : ' (brand never named)')).join(', ');
    const instead = (m.instead || []).map((f) => f.competitor + ' ' + f.n + ' (' + f.upvotes + ' upvotes)').join(', ');
    const unpriced = m.unpriced || [];
    const utable = unpriced.length ? UI.table({ columns: [{ key: 'label', label: 'Page' }, { key: 'size', label: 'Active ads', unit: 'n' }, { key: 'longest_run_days', label: 'Longest run', unit: 'd' }, { key: 'why', label: 'Not on the map because' }],
      rows: unpriced.map((p) => ({ label: p.label, size: p.size, longest_run_days: p.longest_run_days, why: p.x == null ? 'no price band in the brain' : 'no hook types read yet' })), sort: false }) : null;
    return el('div', { class: 'stack' },
      el('div', { class: 'grid two' }, el('div', { class: 'card' }, chart),
        el('div', { class: 'card flat stack' },
          el('h4', { text: 'How the category talks about itself' }),
          el('div', { class: 'small' }, el('b', { text: 'Reddit frames: ' }), frames || 'none on file'),
          el('div', { class: 'small' }, el('b', { text: 'Recommended instead: ' }), instead || 'none on file'),
          el('div', { class: 'small' }, el('b', { text: 'We sit in: ' }), ourQ ? q[ourQ[0]] + ' with ' + (ourQ[1].filter((n) => n !== (m.ours || {}).label).join(', ') || 'nobody else') : NA),
          el('div', { class: 'small' }, el('b', { text: 'Empty quadrants: ' }), empty.length ? empty.join(', ') : 'none, every quadrant has a page'),
          utable ? el('div', null, el('h4', { text: 'Pages off the map' }), utable) : null)),
      gapLine(a9 ? 'The category frames itself on proof and we sell on feel. ' + a9.why : (empty.length ? 'No page sits in ' + empty.join(' or ') + '. That is the open position.' : 'Our proof share is at or above the competitor median.'),
        a9 ? { label: 'Take the position', onClick: () => openAction(a9) } : null));
  }

  function avatarBlock(c) {
    if (!c || !c.rows || !c.rows.length) return UI.emptyState({ screen: SLUG, title: 'No avatars in the brain', text: 'The brain holds no avatar records yet. Reviews, tickets and Reddit build them.', missing: ['reviews'] });
    const rows = c.rows.map((r) => ({ key: r.key, label: r.label, sub: (r.share != null ? Math.round(r.share * 100) + ' percent' : 'share unavailable') + (r.intensity ? ', ' + r.intensity : '') }));
    const matrix = UI.coverageMatrix({
      rows, cols: c.cols, cells: c.cells, unit: 'n', corner: 'avatar x line',
      gapRule: (cell) => !cell ? '' : (cell.them > 0 && !cell.us) ? 'gap' : (cell.us > 0 && cell.them > 0 && cell.us >= cell.them) ? 'lead' : (cell.us > 0 && !cell.them) ? 'lead' : '',
      note: c.note + '. An empty cell is not tried on either side; a red cell is a competitor pitch with nothing of ours.',
      action: { label: 'Research it', onClick: (cell, row) => { const r = c.rows.find((x) => x.key === row.key); const a = r && actionFor(r.finding_id); if (a) openAction(a); else UI.panel({ title: row.label, body: el('div', { class: 'stack' }, el('p', { text: (r && r.job) || '' }), el('p', { class: 'muted small', text: 'No rule fired for this cell yet. The avatar has line evidence elsewhere; the competitor pitch here is a signal to watch.' }), UI.decisionRow({ capability: 'PROD-C01', screen: SLUG, finding_id: SLUG + '.avatar.' + row.key })) }); } },
      onCell: (cell, row) => { const r = c.rows.find((x) => x.key === row.key); if (!r) return; UI.panel({ title: r.label, body: el('div', { class: 'stack' }, el('p', { text: r.job || '' }), el('div', { class: 'small muted', text: 'Words matched: ' + (r.words || []).join(', ') }), el('div', { class: 'small', text: 'Competitor pages pitching to them: ' + (r.served_by.length ? r.served_by.join(', ') : 'none seen') }), actionFor(r.finding_id) ? UI.actionCard(actionFor(r.finding_id), { expanded: true, screen: SLUG }) : el('p', { class: 'muted small', text: 'No finding on this avatar.' })) }); },
    });
    const vrows = c.rows.map((r) => { const a = actionFor(r.finding_id); return Object.assign({}, r, {
      shareText: r.share == null ? NA : fmt.pct(r.share), themeText: r.theme ? pretty(r.theme) + (r.complaint_share != null ? ', ' + fmt.pct(r.complaint_share) + ' complaints' : '') : 'no theme read',
      served: r.served_by.length ? r.served_by.join(', ') : 'none seen', ads: r.in_ads == null ? NA : r.in_ads ? 'yes' : 'no',
      verdict: r.not_served ? 'not_served' : a ? 'under' : r.theme_verdict === 'strength' ? 'strength' : 'served',
      actions: [a ? { label: r.not_served ? 'Screen it' : 'Win them back', onClick: () => openAction(a) } : { label: r.not_served ? 'No line' : 'Served', cls: 'quiet', onClick: () => {} }] }); });
    const t = UI.verdictTable({
      columns: [{ key: 'label', label: 'Avatar' }, { key: 'shareText', label: 'Share of buyers' }, { key: 'intensity', label: 'Intensity', format: (v) => v || NA }, { key: 'lines_us', label: 'Lines with our evidence', unit: 'n' },
        { key: 'themeText', label: 'Their theme' }, { key: 'served', label: 'Competitors pitching to them' }, { key: 'ads', label: 'In our active ads' }],
      rows: vrows,
      verdict: { at: 1, kind: (r) => r.verdict === 'not_served' ? 'new' : r.verdict === 'under' ? 'fix' : r.verdict === 'strength' ? 'scale' : 'keep',
        text: (r) => r.verdict === 'not_served' ? 'Not served' : r.verdict === 'under' ? 'Under-served' : r.verdict === 'strength' ? 'Strength' : 'Served',
        reason: (r) => r.verdict === 'under' ? 'big segment on a complaint-led theme no ad answers' : r.verdict === 'not_served' ? 'no record ties them to a line we sell' : 'line evidence on file' },
      actions: { label: 'Do', onClick: () => {} }, sort: false });
    const under = c.rows.filter((r) => r.finding_id && !r.not_served), ns = c.rows.filter((r) => r.not_served);
    return el('div', { class: 'stack' }, el('div', { class: 'card' }, matrix), el('div', { class: 'card scroll' }, t),
      gapLine((under.length ? under.length + ' big segments sit on a complaint-led theme no active ad answers: ' + under.map((r) => r.label).join(', ') + '. ' : '') + (ns.length ? ns.length + ' avatars have no line evidence: ' + ns.map((r) => r.label).join(', ') + '.' : 'Every avatar has line evidence on our side.'),
        under.length ? { label: 'Win back the first', onClick: () => { const a = actionFor(under[0].finding_id); if (a) openAction(a); } } : null));
  }

  function searchBlock(t) {
    if (!t || !t.groups || !t.groups.length) return UI.emptyState({ screen: SLUG, title: 'No term groups', text: 'The brain holds no identity, lines or ladders to build term groups from.', missing: ['brain'] });
    const av = t.available || {};
    const connect = actionFor(SLUG + '.PROD-R12.brand');
    const vrows = t.groups.map((g) => { const a = actionFor(g.finding_id); return Object.assign({}, g, {
      termsText: g.terms.slice(0, 6).join(', ') + (g.terms.length > 6 ? ' and ' + (g.terms.length - 6) + ' more' : ''),
      pagesText: g.pages.length ? g.pages.map((u) => u.replace(/^https?:\/\/[^/]+/, '')).join(', ') : 'none in the site map',
      topText: (g.top || []).length ? g.top.map((x) => x[0] + ' ' + fmt.int(x[1])).join(', ') : (av.organic ? 'no queries matched' : NA),
      actions: [a ? { label: 'Build the page', onClick: () => openAction(a) } : connect ? { label: 'Connect search', onClick: () => openAction(connect) } : { label: g.pages.length ? 'Answered' : 'No demand read', cls: 'quiet', onClick: () => {} }] }); });
    const table = UI.verdictTable({
      columns: [{ key: 'label', label: 'Group' }, { key: 'termsText', label: 'Terms from the brain' }, { key: 'impressions', label: 'Impressions, 28 d', unit: 'n' }, { key: 'clicks', label: 'Clicks', unit: 'n' },
        { key: 'position', label: 'Position', align: 'right', format: (v) => v == null ? NA : v.toFixed(1) }, { key: 'paid_spend', label: 'Paid spend', unit: '$' }, { key: 'paid_conversions', label: 'Paid conversions', unit: 'n' },
        { key: 'topText', label: 'Top queries' }, { key: 'pagesText', label: 'Pages that answer them' }],
      rows: vrows,
      verdict: { at: 1, kind: (r) => !av.organic ? 'wait' : (r.impressions > 0 && !r.pages.length) ? 'fix' : r.impressions > 0 ? 'keep' : 'watch',
        text: (r) => !av.organic ? 'Connect' : (r.impressions > 0 && !r.pages.length) ? 'No page' : r.impressions > 0 ? 'Answered' : 'No demand read',
        reason: (r) => av.organic ? r.queries + ' queries matched in 28 days' : 'Search Console not connected; demand reads unavailable, never 0' },
      actions: { label: 'Do', onClick: () => {} }, sort: false });
    const qs = (t.questions || []).map((q) => el('li', null, '"' + q.question + '"', el('span', { class: 'muted', text: ' (r/' + q.subreddit + ', ' + fmt.int(q.upvotes) + ' upvotes)' })));
    const noPage = t.groups.filter((g) => !g.pages.length);
    return el('div', { class: 'stack' }, el('div', { class: 'card scroll' }, table),
      el('div', { class: 'card flat' }, el('h4', { text: 'Questions people ask the category' }), qs.length ? el('ul', { class: 'small', style: { margin: 0, paddingLeft: '18px' } }, qs) : el('p', { class: 'muted small', text: 'No questions on file yet.' }),
        el('p', { class: 'micro faint', text: 'From the Reddit pull in the brain (seo_facts). A question page answers them in the brand\'s voice; Reddit is never quoted.' })),
      el('p', { class: 'micro faint', text: 'Organic demand: Search Console, 28 days, queries grouped by the brain\'s words. Paid: Google search-term rows in the same window. ' + (av.organic ? '' : 'Neither is connected for this brand yet, so every volume reads unavailable. ') + 'Pages: urls in the brain\'s site map (' + (t.pages_known || 0) + ' known) whose path carries the group\'s words.' }),
      gapLine((av.organic ? '' : 'Search demand cannot be read until Search Console connects. ') + (noPage.length ? noPage.map((g) => g.label.toLowerCase()).join(' and ') + ' have no answering page in the site map.' : 'Every group has a page in the site map.'),
        connect ? { label: 'Connect Search Console', onClick: () => openAction(connect) } : (noPage.length && actionFor(noPage[0].finding_id) ? { label: 'Build the page', onClick: () => openAction(actionFor(noPage[0].finding_id)) } : null)));
  }

  function behindBlock(b, mp) {
    const rows = (b && b.rows) || [];
    if (!rows.length) return el('div', null, el('p', { class: 'muted', text: 'No positioning or avatar gap fired. The map and the matrix above show where the next one would come from.' }));
    const vrows = rows.map((r) => { const a = actionFor(r.finding_id); return Object.assign({}, r, {
      stakeText: r.usd != null ? fmt.money(r.usd) : 'unavailable: ' + (r.money_reason || 'no formula'), reachText: r.reach || NA,
      owner: a ? a.owner : null, ownerText: a ? { agent: 'agent does it', agent_drafts: 'agent drafts, you approve', person: 'a person does it' }[a.owner] : NA,
      actions: [a ? { label: 'Open the action', onClick: () => openAction(a) } : { label: 'No action', cls: 'quiet', onClick: () => {} }] }); });
    const t = UI.verdictTable({
      columns: [{ key: 'label', label: 'Gap' }, { key: 'sentence', label: 'What the rule found' }, { key: 'stakeText', label: 'Money at stake', align: 'right' }, { key: 'reachText', label: 'Reach' },
        { key: 'ownerText', label: 'Owner' }, { key: 'capability', label: 'Capability' }, { key: 'rule_id', label: 'Rule' }],
      rows: vrows,
      verdict: { at: 1, kind: (r) => r.kind === 'avatar' ? 'fix' : 'watch', text: (r) => r.kind === 'avatar' ? 'Avatar' : 'Positioning', reason: (r) => r.severity + ', confidence ' + (r.confidence == null ? NA : r.confidence) },
      actions: { label: 'Do', onClick: () => {} }, sort: false });
    const orient = UI.orientation([
      { label: 'gaps', value: rows.length, unit: 'n' }, { label: 'positioning', value: b.counts.positioning, unit: 'n' }, { label: 'avatars', value: b.counts.avatar, unit: 'n' },
      { label: 'stake known', value: b.stake_usd, unit: '$', title: 'sum of money at stake where a formula exists' },
      { label: 'of 28-day net revenue', value: b.stake_share_of_net_28d, unit: '%' },
      { label: 'we sit in', value: null, unit: 'n', unavailable_label: b.quadrant && mp && mp.quadrants ? mp.quadrants[b.quadrant] : NA }]);
    return el('div', { class: 'stack' }, orient, el('div', { class: 'card scroll' }, t),
      el('p', { class: 'micro faint', text: 'Ranked by money at stake where a formula exists (avatar rows: share of buyers x 28-day net revenue x complaint share x repeat rate), then reach, then severity. Every row is also in the plan at the top, ranked by the rubric.' }),
      gapLine((b.prove && b.prove.length ? 'Proof we hold and never say in an ad: ' + b.prove.join(', ').toLowerCase() + '. ' : '') + 'The top row is the biggest known gap; approve it from the plan.',
        rows.length && actionFor(rows[0].finding_id) ? { label: 'Open the biggest gap', onClick: () => openAction(actionFor(rows[0].finding_id)) } : null));
  }

  function marginBlock(m) {
    const rows = (m && m.rows) || [];
    if (!rows.length) return el('p', { class: 'muted', text: 'No candidate to gate. Screen one in above.' });
    const open = rows.filter((r) => !r.closed);
    const wrap = el('div', { class: 'stack' });
    const chartHost = el('div', { class: 'card' });
    const draw = (key) => {
      const r = rows.find((x) => x.candidate_id === key); if (!r) return;
      const g = r.gate || {};
      const steps = (g.steps || []).map((s) => ({ label: s.label, value: s.value, kind: s.kind, sub: s.kind === 'down' && s.value != null && r.price ? Math.round(s.value / r.price * 100) + '%' : '' }));
      mount(chartHost, Charts.waterfall({ title: r.name + ': from planned price to contribution a unit', steps, unit: '$',
        note: g.unavailable ? 'Unavailable: ' + g.reason : (g.formula + '. Landed cost: ' + (g.cogs ? g.cogs.basis : NA) + '. Per-order costs are spread over ' + (m.units_per_order || 1) + ' units an order (last whole month).') }));
    };
    const pills = UI.pills({ items: rows.map((r) => ({ key: r.candidate_id, label: r.name.length > 34 ? r.name.slice(0, 32) + '..' : r.name })), current: (open[0] || rows[0]).candidate_id, onChange: draw });
    draw((open[0] || rows[0]).candidate_id);
    const vrows = rows.map((r) => { const g = r.gate || {}; const a = actionFor(r.finding_id); return Object.assign({}, r, {
      margin: g.margin_pct, contribution: g.contribution_usd, cogs: g.cogs ? g.cogs.value : null, cogsBasis: g.cogs ? (g.cogs.estimated ? 'estimated' : 'entered') : NA,
      multiple: g.multiple, bank: g.unavailable ? NA : (g.bank_rule_ok ? 'passes' : 'below'),
      actions: [a ? { label: 'Close the gap', onClick: () => openAction(a) } : { label: g.unavailable ? 'Add the inputs' : 'Passes', cls: 'quiet', onClick: () => {} }] }); });
    const t = UI.verdictTable({
      columns: [{ key: 'name', label: 'Candidate' }, { key: 'price', label: 'Planned price', unit: '$' }, { key: 'pack_units', label: 'Units in pack', unit: 'n' }, { key: 'cogs', label: 'Landed cost', unit: '$' }, { key: 'cogsBasis', label: 'Cost basis' },
        { key: 'contribution', label: 'Contribution a unit', unit: '$' }, { key: 'margin', label: 'Modelled margin', align: 'right', format: (v) => v == null ? NA : v.toFixed(1) + ' percent' },
        { key: 'multiple', label: 'Price over cost', align: 'right', format: (v) => v == null ? NA : v.toFixed(1) + 'x' }, { key: 'bank', label: 'Bank rule PRD-079' }],
      rows: vrows,
      verdict: { at: 1, kind: (r) => (r.gate || {}).unavailable ? 'na' : r.gate.passes_floor === false ? 'stop' : r.gate.passes_floor ? 'keep' : 'watch',
        text: (r) => (r.gate || {}).unavailable ? 'Inputs missing' : r.gate.passes_floor === false ? 'Below the floor' : r.gate.passes_floor ? 'Passes the gate' : 'No floor',
        reason: (r) => (r.gate || {}).unavailable ? r.gate.reason : 'floor ' + (m.floor_pct == null ? NA : m.floor_pct + ' percent') },
      actions: { label: 'Do', onClick: () => {} }, sort: false });
    const below = rows.filter((r) => !r.closed && r.gate && r.gate.passes_floor === false);
    const actual = m.actual_unavailable ? actionFor(m.actual_unavailable) : null;
    wrap.append(pills, el('div', { class: 'grid two' }, chartHost, el('div', { class: 'card flat stack' },
      el('h4', { text: 'The gate' }), el('div', { class: 'small', text: 'Contribution margin modelled = ' + m.formula + '.' }),
      el('div', { class: 'small', text: 'Brand floor: ' + (m.floor_pct == null ? 'unavailable, enter target_contribution_margin in finance inputs' : m.floor_pct + ' percent from ' + m.floor_source) + '.' }),
      el('div', { class: 'small muted', text: m.bank_rule + '.' }),
      el('div', { class: 'small' }, el('b', { text: 'Actual against model: ' }), actual ? 'unavailable until the store connects. ' : 'available.', actual ? el('button', { class: 'btn soft xs', type: 'button', text: 'Connect the store', onclick: () => openAction(actual) }) : null))),
      el('div', { class: 'card scroll' }, t),
      gapLine(below.length ? below.length + ' open candidate' + (below.length === 1 ? '' : 's') + ' below the floor: ' + below.map((r) => r.name).join(', ') + '. Nothing moves to sourcing spend below the floor.' : 'Every open candidate with a price passes the gate.',
        below.length && actionFor(below[0].finding_id) ? { label: 'Close the first gap', onClick: () => openAction(actionFor(below[0].finding_id)) } : null));
    return wrap;
  }

  function patternBlock(p) {
    if (!p || p.unavailable) return UI.emptyState({ screen: SLUG, title: 'No 12-month series', text: (p && p.unavailable) || 'products_monthly is not connected', missing: ['shopify'] });
    const rows = (p.candidates || []).concat(p.categories || []);
    const vrows = rows.map((r) => { const a = r.finding_id ? actionFor(r.finding_id) : null; return Object.assign({}, r, {
      label: r.kind === 'candidate' ? r.name : r.category + ' (category)',
      peak: r.peak_months ? r.peak_months.map((m) => ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][Number(m)]).join(' and ') : NA,
      cagr: r.market_cagr, cash: r.kind === 'candidate' ? (r.cash_plan ? 'attached: ' + r.cash_plan : 'none') : (r.cash_timing || NA),
      actions: [a ? { label: 'Draft the cash plan', onClick: () => openAction(a) } : r.kind === 'candidate' && !r.closed ? { label: r.cash_plan ? 'Edit cash plan' : 'Attach cash plan', cls: 'quiet', onClick: () => { const v = prompt('Cash plan for ' + r.name + ' (order-by month, units, cash out, cash in):', r.cash_plan || ''); if (v != null && v.trim()) candidatePost('candidates/' + r.candidate_id, { cash_plan: v, who: 'person' }); } } : { label: r.kind === 'category' ? 'Reference' : 'Closed', cls: 'quiet', onClick: () => {} }] }); });
    const t = UI.verdictTable({
      columns: [{ key: 'label', label: 'Candidate or category' }, { key: 'why', label: 'Why' }, { key: 'top2_share', label: 'Top 2 months', unit: '%' }, { key: 'peak', label: 'Peak' },
        { key: 'cagr', label: 'Market growth a year', align: 'right', format: (v) => v == null ? NA : v + ' percent' }, { key: 'launches_24m', label: 'Launches, 24 mo', unit: 'n' }, { key: 'cash', label: 'Cash timing or plan' }],
      rows: vrows,
      verdict: { at: 1, kind: (r) => r.tag === 'seasonal' ? (r.kind === 'candidate' && !r.cash_plan && !r.closed ? 'fix' : 'watch') : r.tag === 'trending' ? 'new' : r.tag ? 'keep' : 'na',
        text: (r) => r.tag ? r.tag[0].toUpperCase() + r.tag.slice(1) : 'No series', reason: (r) => r.why || '' },
      actions: { label: 'Do', onClick: () => {} }, sort: false });
    const missing = (p.candidates || []).filter((r) => r.tag === 'seasonal' && !r.cash_plan && !r.closed);
    return el('div', { class: 'stack' }, el('div', { class: 'card scroll' }, t), el('p', { class: 'micro faint', text: 'Rule: ' + p.rule + '. Series: our units by category over 12 whole months (simulated); growth and launches from the web pass.' }),
      gapLine(missing.length ? missing.length + ' seasonal candidate' + (missing.length === 1 ? ' has' : 's have') + ' no cash plan: ' + missing.map((r) => r.name).join(', ') + '. None can reach the shortlist without one.' : 'Every seasonal candidate carries a cash plan.',
        missing.length && actionFor(missing[0].finding_id) ? { label: 'Draft the first', onClick: () => openAction(actionFor(missing[0].finding_id)) } : null));
  }

  function laneMapBlock(m) {
    if (!m || !m.points || !m.points.length) return UI.emptyState({ screen: SLUG, title: 'No lanes to map', text: 'The map needs the competitor pages in the brain and the web pass.', missing: ['ad_library', 'web_pass'] });
    const q = m.quadrants || {};
    const chart = Charts.positioningMap({
      title: 'Trend against saturation, one point per lane, sized by competitor active ads',
      x: { label: 'sellers: competitor pages pushing it plus launches by others, 24 months', lo: 'open', hi: 'crowded', unit: 'n', min: 0, max: Math.max(10, Math.max.apply(null, m.points.map((p) => p.x || 0)) + 1) },
      y: { label: 'trend score from market growth and launches', lo: 'flat', hi: 'growing', unit: 'n', min: -1, max: 1 },
      points: m.points.filter((p) => p.y != null).map((p) => ({ label: p.label, x: p.x, y: p.y, us: !!p.sold && !!p.advertised, size: p.size, note: p.quadrant + '; ladder ' + p.grade })),
      midX: m.mid_x, midY: m.mid_y, quadrants: [q.tl, q.tr, q.bl, q.br], usLabel: 'we sell and advertise it', themLabel: 'lane',
      note: m.rule + '. Lanes with no market growth on file are listed below, not plotted.' });
    const vrows = m.points.map((p) => { const a = actionFor(p.finding_id); return Object.assign({}, p, {
      trendText: p.y == null ? NA : p.y.toFixed(2), cagr: p.market_cagr, sellers: p.x, sold: p.sold == null ? NA : p.sold ? 'yes' : 'no',
      actions: [a ? { label: 'Find the room', onClick: () => openAction(a) } : { label: p.quadrant, cls: 'quiet', onClick: () => {} }] }); });
    const t = UI.verdictTable({
      columns: [{ key: 'label', label: 'Lane' }, { key: 'trendText', label: 'Trend score', align: 'right' }, { key: 'cagr', label: 'Market growth a year', align: 'right', format: (v) => v == null ? NA : v + ' percent' },
        { key: 'sellers', label: 'Sellers', unit: 'n' }, { key: 'competitors_n', label: 'Pages advertising', unit: 'n' }, { key: 'launches_theirs', label: 'Launches by others', unit: 'n' }, { key: 'sold', label: 'We sell it' }],
      rows: vrows,
      verdict: { at: 1, kind: (r) => r.grade === 'green' ? 'keep' : r.grade === 'amber' ? 'watch' : 'stop', text: (r) => r.grade === 'green' ? 'Green, 0 to 1' : r.grade === 'amber' ? 'Amber, 2 to 4' : 'Red, 5 or more', reason: (r) => 'bank ladder PRD-052 on sellers: ' + r.x },
      actions: { label: 'Do', onClick: () => {} }, sort: false });
    const full = m.points.filter((p) => p.y != null && p.y >= m.mid_y && p.x >= m.mid_x + 0.5);
    const room = m.points.filter((p) => p.y != null && p.y >= m.mid_y && p.x < m.mid_x + 0.5);
    return el('div', { class: 'stack' }, el('div', { class: 'card' }, chart), el('div', { class: 'card scroll' }, t),
      gapLine((room.length ? 'Growing with room left: ' + room.map((p) => p.label.toLowerCase()).join(', ') + '. ' : '') + (full.length ? 'Growing but full: ' + full.map((p) => p.label.toLowerCase()).join(', ') + '. Only a named angle gets in.' : 'No growing lane is full.'),
        full.length && actionFor(full[0].finding_id) ? { label: 'Find the room', onClick: () => openAction(actionFor(full[0].finding_id)) } : null));
  }

  function spendBlock(sp) {
    const rows = (sp && sp.rows) || [];
    if (!rows.length) return UI.emptyState({ screen: SLUG, title: 'No competitor ad signals', text: 'The brain holds no Ad Library records yet.', missing: ['ad_library'] });
    const bands = sp.bands || [];
    const chart = Charts.bar({ title: 'Advertisers by longest run, per lane', labels: rows.map((r) => r.label.length > 18 ? r.label.slice(0, 16) + '..' : r.label), stacked: true, unit: 'n',
      series: bands.map((b) => ({ name: b, values: rows.map((r) => r.bands[b]) })),
      note: 'One count per competitor page, by the longest run of its active ads on the lane. A snapshot from the Ad Library pull in the brain, not a spend figure.' });
    const vrows = rows.map((r) => { const a = actionFor(r.finding_id); return Object.assign({}, r, {
      fundedText: r.funded.length ? r.funded.join(', ') : 'none', longestText: r.longest == null ? NA : r.longest + ' d', cand: r.candidates.length ? r.candidates.join(', ') : 'none',
      actions: [a ? { label: 'Screen it', onClick: () => openAction(a) } : { label: r.verdict === 'funded' ? (r.candidates.length ? 'Candidate open' : r.kind === 'proof' ? 'Proof lane' : 'Covered') : r.verdict === 'live' ? 'Live test' : 'Noise', cls: 'quiet', onClick: () => {} }] }); });
    const t = UI.verdictTable({
      columns: [{ key: 'label', label: 'Lane' }, { key: 'fundedText', label: 'Advertisers at 90 days or more' }, { key: 'longestText', label: 'Longest run', align: 'right' }, { key: 'long_runners_30d', label: 'Their ads live 30 d+', unit: 'n' }, { key: 'cand', label: 'Our open candidates on it' }],
      rows: vrows,
      verdict: { at: 1, kind: (r) => r.verdict === 'funded' ? 'scale' : r.verdict === 'live' ? 'watch' : 'na', text: (r) => r.verdict === 'funded' ? 'Funded test' : r.verdict === 'live' ? 'Live test' : r.verdict === 'noise' ? 'Noise' : 'No advertiser', reason: (r) => r.funded.length + ' at 90 days, ' + r.live.length + ' at 14 days' },
      actions: { label: 'Do', onClick: () => {} }, sort: false });
    const gaps = rows.filter((r) => r.verdict === 'funded' && r.kind !== 'proof' && !r.candidates.length);
    return el('div', { class: 'stack' }, el('div', { class: 'grid two' }, el('div', { class: 'card' }, chart), el('div', { class: 'card flat' }, el('h4', { text: 'How to read it' }), el('p', { class: 'small', text: sp.rule + '.' }), el('p', { class: 'small muted', text: 'A high concurrent ad count reads as budget and confidence, then the margin gate checks the money (bank idea PRD-024). Lanes with a candidate open are covered; proof lanes carry the brief from the lanes table above, not a candidate.' }))),
      el('div', { class: 'card scroll' }, t),
      gapLine(gaps.length ? gaps.length + ' funded lane' + (gaps.length === 1 ? ' has' : 's have') + ' no candidate: ' + gaps.map((g) => g.label.toLowerCase()).join(', ') + '.' : 'Every funded product lane has a candidate open.',
        gaps.length && actionFor(gaps[0].finding_id) ? { label: 'Screen the first', onClick: () => openAction(actionFor(gaps[0].finding_id)) } : null));
  }

  function priceSignalBlock(ps) {
    if (!ps || !ps.n) return UI.emptyState({ screen: SLUG, title: 'No price mentions in reviews', text: 'The language bank holds no review quote that names a per-pair price.', missing: ['reviews'] });
    const orient = UI.orientation([
      { label: 'reviewers say a pair is worth', value: ps.median_per_pair, unit: '$', title: 'median of per-pair price mentions' }, { label: 'mentions', value: ps.n, unit: 'n' },
      { label: 'range', value: null, unit: 'n', unavailable_label: ps.low != null ? fmt.money(ps.low) + ' to ' + fmt.money(ps.high) : NA },
      { label: 'competitor medians', value: null, unit: 'n', unavailable_label: ps.competitor_band ? fmt.money(ps.competitor_band[0]) + ' to ' + fmt.money(ps.competitor_band[1]) : NA },
      { label: 'our pair', value: ps.ours ? ps.ours.value : null, unit: '$', title: ps.ours ? ps.ours.basis : '' }]);
    const bars = Charts.bar({ title: 'Price mentions by source', labels: Object.keys(ps.by_source), series: [{ name: 'mentions', values: Object.values(ps.by_source) }], unit: 'n',
      note: ps.rule + '. Stars: ' + Object.entries(ps.by_star).map(([k, v]) => k + '-star ' + v).join(', ') + '.' });
    const quotes = el('ul', { class: 'small', style: { margin: 0, paddingLeft: '18px' } }, (ps.mentions || []).slice(0, 8).map((m) => el('li', null, el('b', { text: fmt.money(m.usd) + ' ' }), el('span', { class: 'muted', text: '(' + m.source + (m.star ? ', ' + m.star + '-star' : '') + ') ' }), '"' + m.quote + '"')));
    const vrows = (ps.candidates || []).map((c) => { const a = actionFor(c.finding_id); return Object.assign({}, c, { gapText: c.gap == null ? NA : (c.gap > 0 ? '+' : '') + Math.round(c.gap * 100) + ' percent',
      actions: [a ? { label: 'Recheck the price', onClick: () => openAction(a) } : { label: c.per_pair == null ? 'No price' : 'Inside the signal', cls: 'quiet', onClick: () => {} }] }); });
    const t = UI.verdictTable({
      columns: [{ key: 'name', label: 'Candidate' }, { key: 'category', label: 'Category' }, { key: 'per_pair', label: 'Planned per unit', unit: '$' }, { key: 'gapText', label: 'Against the review median' }],
      rows: vrows,
      verdict: { at: 1, kind: (r) => r.closed ? 'na' : r.gap == null ? 'na' : r.gap > ps.gap_rule ? 'fix' : r.gap < -ps.gap_rule ? 'watch' : 'keep', text: (r) => r.closed ? 'Closed' : r.gap == null ? 'No read' : r.gap > ps.gap_rule ? 'Above the signal' : r.gap < -ps.gap_rule ? 'Below the signal' : 'Inside', reason: (r) => 'gap rule ' + Math.round(ps.gap_rule * 100) + ' percent' },
      actions: { label: 'Do', onClick: () => {} }, sort: false, empty: 'No candidate with a planned price.' });
    const above = (ps.candidates || []).filter((c) => !c.closed && c.gap != null && c.gap > ps.gap_rule);
    return el('div', { class: 'stack' }, orient, el('div', { class: 'grid two' }, el('div', { class: 'card' }, bars), el('div', { class: 'card flat' }, el('h4', { text: 'What they say, in their words' }), quotes, el('p', { class: 'micro faint', text: 'Complaint quotes name the price they paid; the ceiling is what they say it should cost. Both feed the median. Never quoted in an ad.' }))),
      el('div', { class: 'card scroll' }, t),
      gapLine(above.length ? above.length + ' candidate' + (above.length === 1 ? ' is' : 's are') + ' planned above what reviewers say a pair is worth: ' + above.map((c) => c.name).join(', ') + '.' : 'Every priced candidate sits within the review price signal.',
        above.length && actionFor(above[0].finding_id) ? { label: 'Recheck the first', onClick: () => openAction(actionFor(above[0].finding_id)) } : null));
  }

  function complaintBlock(rows) {
    if (!rows || !rows.length) return UI.emptyState({ screen: SLUG, title: 'No mined listing reviews', text: 'The brain holds no Amazon issue and praise counts yet.', missing: ['amazon_reviews'] });
    const themes = Array.from(new Set(rows.flatMap((r) => Object.keys(r.issues)))).filter((t) => t !== 'general');
    const chart = Charts.bar({ title: 'Complaint themes per listing, share of mined reviews', labels: rows.map((r) => r.asin), stacked: true, unit: '%',
      series: themes.map((t) => ({ name: pretty(t), values: rows.map((r) => r.mined ? (r.issues[t] || 0) / r.mined : null) })), benchmark: 0.15, benchmark_label: '15 percent, one complaint',
      note: 'Each bar is one listing; segments are complaint themes as a share of the reviews mined on it (general is left out). The dashed line is the rule: one complaint over 15 percent is the gap to build on.' });
    const vrows = rows.map((r) => { const a = actionFor(r.finding_id); return Object.assign({}, r, {
      top: r.top_complaint ? pretty(r.top_complaint) + ' (' + r.top_count + ')' : 'none', label: r.title.length > 48 ? r.title.slice(0, 46) + '..' : r.title,
      actions: [a ? { label: 'Build the angle', onClick: () => openAction(a) } : { label: r.mined < 20 ? 'Too few mined' : 'Under 15 percent', cls: 'quiet', onClick: () => {} }] }); });
    const t = UI.verdictTable({
      columns: [{ key: 'label', label: 'Listing' }, { key: 'asin', label: 'ASIN' }, { key: 'stars', label: 'Stars', align: 'right', format: (v) => v == null ? NA : v.toFixed(1) }, { key: 'ratings', label: 'Ratings', unit: 'n' },
        { key: 'price_usd', label: 'Price', unit: '$' }, { key: 'mined', label: 'Reviews mined', unit: 'n' }, { key: 'top', label: 'Top complaint' }, { key: 'top_rate', label: 'Its share', unit: '%' }, { key: 'praise_share', label: 'Praise share', unit: '%' }],
      rows: vrows,
      verdict: { at: 1, kind: (r) => r.mined < 20 ? 'na' : (r.top_rate || 0) > 0.15 ? 'fix' : (r.praise_share || 0) >= 0.7 ? 'scale' : 'keep', text: (r) => r.mined < 20 ? 'Thin sample' : (r.top_rate || 0) > 0.15 ? 'Complaint over 15' : (r.praise_share || 0) >= 0.7 ? 'Praise led' : 'Mixed', reason: (r) => r.complaints + ' complaint, ' + r.praises + ' praise quotes mined' },
      actions: { label: 'Do', onClick: () => {} }, sort: false });
    const gaps = rows.filter((r) => r.mined >= 20 && (r.top_rate || 0) > 0.15);
    return el('div', { class: 'stack' }, el('div', { class: 'card' }, chart), el('div', { class: 'card scroll' }, t),
      el('p', { class: 'micro faint', text: 'Mined counts come from the Amazon review pull in the brain (public), by theme. Ratings and stars are the listing\'s public totals. Listing sales are not connected.' }),
      gapLine(gaps.length ? gaps.length + ' listing' + (gaps.length === 1 ? ' has' : 's have') + ' one complaint over 15 percent of mined reviews: ' + gaps.map((g) => g.asin + ' (' + pretty(g.top_complaint) + ')').join(', ') + '.' : 'No listing has a single complaint over 15 percent of its mined reviews.',
        gaps.length && actionFor(gaps[0].finding_id) ? { label: 'Build the first angle', onClick: () => openAction(actionFor(gaps[0].finding_id)) } : null));
  }

  function gatesBlock(g) {
    const rows = (g && g.rows) || [];
    if (!rows.length) return el('p', { class: 'muted', text: 'No candidate to gate.' });
    const cols = (g.gates || []).map((k) => ({ key: k, label: g.labels[k] }));
    const cells = {};
    rows.forEach((r) => { cells[r.candidate_id] = {}; (g.gates || []).forEach((k) => { const s = r.gates[k]; cells[r.candidate_id][k] = { us: s.status === 'pass' ? 1 : s.status === 'fail' ? 0 : null, unit: 'n', label: s.why }; }); });
    const matrix = UI.coverageMatrix({ rows: rows.map((r) => ({ key: r.candidate_id, label: r.name, sub: r.passed + ' of ' + r.of + ' passed, angle ' + r.angle.label + ', compliance ' + r.compliance })), cols, cells, single: true, max: 1, unit: 'n', corner: 'candidate x gate',
      note: '1 is pass, 0 is fail, n/a is not run. Hover a cell for the reason. ' + (g.rule || ''),
      onCell: (cell, row, col) => { const r = rows.find((x) => x.candidate_id === row.key); if (!r) return; const s = r.gates[col.key]; UI.panel({ title: r.name + ': ' + g.labels[col.key], body: el('div', { class: 'stack' }, el('p', null, el('b', { text: s.status + '. ' }), s.why), el('div', { class: 'small muted', text: 'Angle: ' + (r.angle_text || 'none') + (r.angle_source ? ' (source: ' + r.angle_source + ')' : '') }), r.angle.copied ? el('div', { class: 'small', text: 'Reads like ' + r.angle.copied.competitor + ': ' + r.angle.copied.words.join(', ') }) : null, (r.finding_ids || []).map(actionFor).filter(Boolean).map((a) => UI.actionCard(a, { expanded: true, screen: SLUG }))) }); } });
    const vrows = rows.map((r) => { const acts = (r.finding_ids || []).map(actionFor).filter(Boolean); return Object.assign({}, r, {
      angleText: r.angle.label + ' (' + r.angle.score + ' of 3)' + (r.angle.copied ? ', reads like ' + r.angle.copied.competitor : ''), gatesText: r.passed + ' of ' + r.of, comp: r.compliance,
      actions: [acts.length ? { label: acts[0].rule_id === 'PROD-R23' ? 'Write the angle' : 'Run compliance', onClick: () => openAction(acts[0]) } : { label: r.closed ? 'Closed' : r.passed === r.of && r.compliance === 'pass' ? 'Fundable' : 'Gates open', cls: 'quiet', onClick: () => {} }] }); });
    const t = UI.verdictTable({
      columns: [{ key: 'name', label: 'Candidate' }, { key: 'stage', label: 'Stage' }, { key: 'angleText', label: 'Angle confidence' }, { key: 'gatesText', label: 'Gates passed' }, { key: 'comp', label: 'Compliance' }],
      rows: vrows,
      verdict: { at: 1, kind: (r) => r.closed ? 'na' : (r.passed === r.of && r.compliance === 'pass') ? 'scale' : (r.finding_ids || []).length ? 'fix' : 'watch', text: (r) => r.closed ? 'Closed' : (r.passed === r.of && r.compliance === 'pass') ? 'Fundable' : (r.finding_ids || []).length ? 'Blocked' : 'In progress', reason: (r) => r.passed + ' of ' + r.of + ' gates, compliance ' + r.compliance },
      actions: { label: 'Do', onClick: () => {} }, sort: false });
    const blocked = rows.filter((r) => !r.closed && (r.finding_ids || []).length);
    return el('div', { class: 'stack' }, el('div', { class: 'card' }, matrix), el('div', { class: 'card scroll' }, t),
      gapLine(blocked.length ? blocked.length + ' candidate' + (blocked.length === 1 ? ' is' : 's are') + ' blocked on an angle or a compliance check: ' + blocked.map((r) => r.name).join(', ') + '.' : 'No candidate is blocked on an angle or compliance.',
        blocked.length ? { label: 'Unblock the first', onClick: () => { const a = actionFor(blocked[0].finding_ids[0]); if (a) openAction(a); } } : null));
  }

  function scorecardBlock(sc) {
    const rows = (sc && sc.rows) || [];
    if (!rows.length) return el('p', { class: 'muted', text: 'No candidate to score.' });
    const cols = (sc.criteria || []).map((k) => ({ key: k, label: sc.labels[k] + ' ' + sc.weights[k] + '%' }));
    const cells = {};
    rows.forEach((r) => { cells[r.candidate_id] = {}; (sc.criteria || []).forEach((k) => { cells[r.candidate_id][k] = { us: r.scores[k], unit: 'n' }; }); });
    const heat = UI.coverageMatrix({ rows: rows.map((r) => ({ key: r.candidate_id, label: '#' + r.rank + ' ' + r.name, sub: r.total + ' of 100, ' + r.verdict.replace(/_/g, ' ') })), cols, cells, single: true, max: 5, unit: 'n', corner: 'candidate x criterion',
      note: 'Each criterion 0 to 5 from the fast checks and the spend signal (demand), the margin gate (margin), the angle (differentiation), the compliance check, and the demand pattern with its cash plan (cash timing). n/a scores the neutral 2.5. Weights: ' + sc.weights_source + '.' });
    const openMemo = (r) => { const a = actionFor(r.finding_id); UI.panel({ title: r.name + ': go or no-go memo', body: el('div', { class: 'stack' }, el('pre', { class: 'card', style: { whiteSpace: 'pre-wrap', fontFamily: 'var(--mono)', fontSize: 'var(--fs-small)', margin: 0 }, text: r.memo }),
      el('div', { class: 'row' }, UI.copyButton({ label: 'Copy memo', text: () => r.memo }), el('button', { class: 'btn soft sm', type: 'button', text: 'Shortlist it', onclick: () => candidatePost('candidates/' + r.candidate_id, { stage: 'shortlisted', who: 'person' }) }), el('button', { class: 'btn soft sm', type: 'button', text: 'Go', onclick: () => candidatePost('candidates/' + r.candidate_id, { stage: 'go', who: 'person' }) }), el('button', { class: 'btn quiet sm', type: 'button', text: 'Kill', onclick: () => { if (confirm('Kill ' + r.name + '?')) candidatePost('candidates/' + r.candidate_id, { stage: 'killed', who: 'person' }); } })),
      a ? UI.actionCard(a, { expanded: true, screen: SLUG }) : UI.decisionRow({ capability: 'PROD-C11', screen: SLUG, finding_id: SLUG + '.scorecard.' + r.candidate_id, compact: true })) }); };
    const vrows = rows.map((r) => Object.assign({}, r, { na: r.unavailable.length ? r.unavailable.map(pretty).join(', ') : 'none',
      actions: [{ label: r.review_due ? 'Decide now' : 'Open the memo', onClick: () => openMemo(r) }] }));
    const t = UI.verdictTable({
      columns: [{ key: 'rank', label: '#', unit: 'n' }, { key: 'name', label: 'Candidate' }, { key: 'total', label: 'Score', align: 'right', format: (v) => v == null ? NA : v.toFixed(0) + ' /100' }, { key: 'stage', label: 'Stage' },
        { key: 'gates_passed', label: 'Gates', align: 'right', format: (v, r) => v + ' of ' + r.gates_of }, { key: 'compliance', label: 'Compliance' }, { key: 'review_date', label: 'Review date', format: (v) => v ? fmt.date(v) : NA }, { key: 'na', label: 'Criteria with no input' }],
      rows: vrows,
      verdict: { at: 2, kind: (r) => r.verdict === 'go' ? 'scale' : r.verdict === 'no_go' ? 'stop' : r.closed ? 'na' : r.review_due ? 'fix' : 'watch', text: (r) => r.verdict === 'go' ? 'Go' : r.verdict === 'no_go' ? 'No go' : r.closed ? r.stage : r.review_due ? 'Review due' : 'Hold', reason: (r) => sc.rule },
      actions: { label: 'Do', onClick: () => {} }, sort: false });
    const due = rows.filter((r) => r.review_due);
    return el('div', { class: 'stack' }, el('div', { class: 'card' }, heat), el('div', { class: 'card scroll' }, t), el('p', { class: 'micro faint', text: sc.rule + ' Weights are set once per brand in the brain (learnings.shortlist_weights); today: ' + sc.weights_source + '.' }),
      gapLine(due.length ? due.length + ' candidate' + (due.length === 1 ? ' is' : 's are') + ' due for a decision this week: ' + due.map((r) => r.name).join(', ') + '.' : 'No candidate is due for a decision this week. The top of the table is the one to fund next.',
        due.length ? { label: 'Decide the first', onClick: () => openMemo(due[0]) } : rows.length ? { label: 'Open the top memo', onClick: () => openMemo(rows[0]) } : null));
  }

  function videoBlock(v) {
    const rows = (v && v.rows) || [];
    if (!rows.length) return UI.emptyState({ screen: SLUG, title: 'No demand signals', text: 'No social pull, Reddit language or creator ads on file.', missing: ['reddit', 'social_pull'] });
    const vrows = rows.map((r) => { const a = actionFor(r.finding_id); return Object.assign({}, r, {
      ig: r.instagram_posts == null ? NA : r.instagram_posts + ' posts' + (r.instagram_mode === 'live' ? '' : ' (mock pull)'), rd: r.reddit_mentions ? r.reddit_mentions + ' (' + fmt.int(r.reddit_upvotes) + ' upvotes)' : 'none',
      cr: r.creator_pages.length ? r.creator_pages.join(', ') : 'none', own: r.own_creator_ads || 'none', plat: r.platforms.length ? r.platforms.join(', ') : 'none', cand: r.candidates.length ? r.candidates.join(', ') : 'none',
      actions: [a ? { label: 'Confirm on a second platform', onClick: () => openAction(a) } : { label: r.verdict === 'pattern' ? 'Pattern' : r.verdict === 'single' ? 'One source' : 'No signal', cls: 'quiet', onClick: () => {} }] }); });
    const t = UI.verdictTable({
      columns: [{ key: 'label', label: 'Lane' }, { key: 'ig', label: 'Instagram pull' }, { key: 'rd', label: 'Reddit' }, { key: 'cr', label: 'Competitor creator ads' }, { key: 'own', label: 'Our creator ads' }, { key: 'plat', label: 'Platforms above the floor' }, { key: 'cand', label: 'Our candidates' }],
      rows: vrows,
      verdict: { at: 1, kind: (r) => r.verdict === 'pattern' ? 'keep' : r.verdict === 'single' ? 'watch' : 'na', text: (r) => r.verdict === 'pattern' ? 'Real pattern' : r.verdict === 'single' ? 'Single source' : 'No signal', reason: (r) => r.platforms.length + ' platforms; ' + v.rule },
      actions: { label: 'Do', onClick: () => {} }, sort: false });
    const single = rows.filter((r) => r.verdict === 'single' && r.candidates.length);
    return el('div', { class: 'stack' }, el('div', { class: 'card scroll' }, t),
      el('p', { class: 'micro faint', text: 'Rule: ' + v.rule + '. ' + (v.social_mode === 'live' ? 'Instagram counts are from the live hashtag pull.' : 'Instagram counts come from the mock hashtag pull (a sample shape, not the market); the live pull needs a session that allows paid calls.') + ' One platform\'s demand is a lead for another platform, never proof (bank idea PRD-022).' }),
      gapLine(single.length ? single.length + ' candidate lane' + (single.length === 1 ? ' rests' : 's rest') + ' on one platform: ' + single.map((r) => r.label.toLowerCase()).join(', ') + '.' : 'Every candidate lane shows demand on 2 or more platforms, or none at all.',
        single.length && actionFor(single[0].finding_id) ? { label: 'Confirm the first', onClick: () => openAction(actionFor(single[0].finding_id)) } : null));
  }

  function techPackBlock(t) {
    const rows = (t && t.rows) || [];
    if (!rows.length) return el('p', { class: 'muted', text: 'No candidate to spec.' });
    const openSpec = (r) => {
      const tol = el('input', { class: 'text sm', placeholder: 'tolerances, like length plus or minus 5 mm, weight plus or minus 3 g', value: (r.pack && r.pack.tolerances) || '' });
      const bom = el('textarea', { class: 'text sm', rows: 4, placeholder: 'bill of materials, one line per material with share, like 62% cotton, 33% nylon, 5% spandex; cuff elastic; packaging card', style: { width: '100%' } });
      if (r.pack && r.pack.bom) bom.value = r.pack.bom;
      const cost = el('input', { class: 'text sm', type: 'number', step: '0.01', placeholder: 'packaging cost a unit, $', value: r.pack && r.pack.packaging_cost != null ? r.pack.packaging_cost : '' });
      const note = el('input', { class: 'text sm', placeholder: 'note (optional)' });
      const save = el('button', { class: 'btn primary sm', type: 'button', text: 'Save as the current version', onclick: () => candidatePost('candidates/' + r.candidate_id, { tech_pack: { tolerances: tol.value, bom: bom.value, packaging_cost: cost.value || null, note: note.value }, who: 'person' }) });
      UI.panel({ title: r.name + ': tech pack ' + (r.version ? '(current ' + r.version + ')' : '(none yet)'), body: el('div', { class: 'stack' }, el('div', { class: 'small muted', text: t.rule + '.' }), tol, bom, cost, note, el('div', { class: 'row' }, save), r.finding_id && actionFor(r.finding_id) ? UI.actionCard(actionFor(r.finding_id), { expanded: true, screen: SLUG }) : null) });
    };
    const vrows = rows.map((r) => Object.assign({}, r, { tol: r.pack && r.pack.tolerances ? 'yes' : 'missing', bomText: r.pack && r.pack.bom ? 'yes' : 'missing', pk: r.pack && r.pack.packaging_cost != null ? fmt.money(r.pack.packaging_cost) : 'missing',
      updated: r.pack && r.pack.updated_at ? fmt.date(r.pack.updated_at) : NA, versionText: r.version || 'none',
      actions: [{ label: r.status === 'current' ? 'New version' : 'Write the spec', onClick: () => openSpec(r) }] }));
    const tbl = UI.verdictTable({
      columns: [{ key: 'name', label: 'Candidate' }, { key: 'stage', label: 'Stage' }, { key: 'versionText', label: 'Version' }, { key: 'tol', label: 'Tolerances' }, { key: 'bomText', label: 'BOM' }, { key: 'pk', label: 'Packaging cost' }, { key: 'updated', label: 'Updated' }, { key: 'versions', label: 'Versions', unit: 'n' }],
      rows: vrows,
      verdict: { at: 1, kind: (r) => r.closed ? 'na' : r.status === 'current' ? 'keep' : r.needs_spec ? 'fix' : 'watch', text: (r) => r.closed ? 'Closed' : r.status === 'current' ? 'Ready to quote' : r.needs_spec ? 'Spec missing' : r.status === 'partial' ? 'Partial' : 'Not yet needed', reason: (r) => r.missing.length ? 'missing ' + r.missing.map(pretty).join(', ') : 'complete' },
      actions: { label: 'Do', onClick: () => {} }, sort: false });
    const gaps = rows.filter((r) => !r.closed && r.needs_spec && r.status !== 'current');
    return el('div', { class: 'stack' }, el('div', { class: 'card scroll' }, tbl), el('p', { class: 'micro faint', text: t.rule + '. Packaging cost here is the line sourcing quotes on; the margin gate above reads the finance inputs until a pack is priced.' }),
      gapLine(gaps.length ? gaps.length + ' candidate' + (gaps.length === 1 ? '' : 's') + ' past the gate with no current spec: ' + gaps.map((r) => r.name).join(', ') + '. Sourcing cannot quote them.' : 'Every candidate past the gate has a current spec.',
        gaps.length ? { label: 'Write the first', onClick: () => openSpec(gaps[0]) } : null));
  }

  function hoursBlock(h) {
    const rows = (h && h.rows) || [];
    if (!rows.length) return el('p', { class: 'muted', text: 'No candidate with hours logged.' });
    const bars = Charts.bar({ title: 'Hours logged against hours allowed through the stage', labels: rows.map((r) => r.name.length > 18 ? r.name.slice(0, 16) + '..' : r.name), unit: 'n',
      series: [{ name: 'hours logged', values: rows.map((r) => r.hours_logged) }, { name: 'hours allowed', values: rows.map((r) => r.hours_allowed) }],
      note: h.rule + '. Budget per stage: ' + (h.stages || []).map((s) => s + ' ' + h.budget[s]).join(', ') + ' (' + h.budget_source + ').' });
    const vrows = rows.map((r) => { const fid = (h.findings || {})[r.candidate_id]; const a = fid ? actionFor(fid) : null; return Object.assign({}, r, {
      allowed: r.hours_allowed == null ? NA : r.hours_allowed, share: r.used_share,
      actions: [a ? { label: 'Stop the clock', onClick: () => openAction(a) } : { label: r.closed ? 'Closed' : 'Log 1 h', cls: 'quiet', onClick: () => { if (!r.closed) candidatePost('candidates/' + r.candidate_id, { hours_add: 1, who: 'person' }); } }] }); });
    const t = UI.verdictTable({
      columns: [{ key: 'name', label: 'Candidate' }, { key: 'stage', label: 'Stage' }, { key: 'hours_logged', label: 'Hours logged', align: 'right', format: (v) => v == null ? NA : v.toFixed(1) }, { key: 'allowed', label: 'Allowed through the stage', align: 'right', format: (v) => v == null ? NA : v.toFixed(0) }, { key: 'share', label: 'Used', unit: '%' }],
      rows: vrows,
      verdict: { at: 1, kind: (r) => r.closed ? 'na' : r.over_by > 0 ? 'fix' : (r.used_share || 0) >= 0.75 ? 'watch' : 'keep', text: (r) => r.closed ? 'Closed' : r.over_by > 0 ? 'Over budget' : (r.used_share || 0) >= 0.75 ? 'Near the cap' : 'In budget', reason: (r) => r.over_by > 0 ? r.over_by + ' hours over' : '' },
      actions: { label: 'Do', onClick: () => {} }, sort: false });
    const over = rows.filter((r) => !r.closed && r.over_by > 0);
    return el('div', { class: 'stack' }, UI.orientation([{ label: 'hours logged across the pipeline', value: h.total_hours, unit: 'n' }, { label: 'over budget', value: over.length, unit: 'n', tone: over.length ? 'bad' : 'good' }]),
      el('div', { class: 'grid two' }, el('div', { class: 'card' }, bars), el('div', { class: 'card scroll' }, t)),
      gapLine(over.length ? over.length + ' candidate' + (over.length === 1 ? ' has' : 's have') + ' passed the hours budget: ' + over.map((r) => r.name).join(', ') + '. No more hours without a named question.' : 'Every open candidate is inside its hours budget.',
        over.length && (h.findings || {})[over[0].candidate_id] && actionFor(h.findings[over[0].candidate_id]) ? { label: 'Stop the first clock', onClick: () => openAction(actionFor(h.findings[over[0].candidate_id])) } : null));
  }

  function trendChecksBlock(t) {
    const rows = (t && t.rows) || [];
    if (!rows.length) return UI.emptyState({ screen: SLUG, title: 'No lanes', text: 'No web pass on file.', missing: ['web_pass'] });
    const pct = (v) => v == null ? NA : (v * 100).toFixed(1) + ' percent';
    const vrows = rows.map((r) => { const a = actionFor(r.finding_id); return Object.assign({}, r, {
      hist: r.history_points ? r.history_points + ' point' + (r.history_points === 1 ? '' : 's') + ', ' + r.history_years + ' year' + (r.history_years === 1 ? '' : 's') + (r.first_year ? ' (' + r.first_year + (r.last_year !== r.first_year ? ' to ' + r.last_year : '') + ')' : '') : 'none',
      shortText: pct(r.short_growth), longText: pct(r.long_growth), fc: r.forecast_growth == null ? NA : pct(r.forecast_growth) + ' (' + r.forecast_points + ' pt)', cand: r.candidates.length ? r.candidates.join(', ') : 'none',
      actions: [a ? { label: 'Run the multi-year check', onClick: () => openAction(a) } : { label: r.verdict === 'steady' ? 'Trusted' : r.candidates.length ? 'Fine' : 'No candidate', cls: 'quiet', onClick: () => {} }] }); });
    const tbl = UI.verdictTable({
      columns: [{ key: 'label', label: 'Lane' }, { key: 'market', label: 'Market series', format: (v) => v || 'none' }, { key: 'hist', label: 'History on file' }, { key: 'shortText', label: 'Last year' }, { key: 'longText', label: 'Multi-year a year' }, { key: 'fc', label: 'Forecast a year' }, { key: 'cand', label: 'Our candidates' }],
      rows: vrows,
      verdict: { at: 1, kind: (r) => r.verdict === 'steady' ? 'keep' : r.verdict === 'fad_risk' ? 'stop' : r.verdict === 'falling' ? 'cut' : 'watch', text: (r) => ({ steady: 'Steady trend', fad_risk: 'Spike, not trend', falling: 'Falling', forecast_only: 'Forecast only', no_series: 'No series' })[r.verdict], reason: (r) => t.rule },
      actions: { label: 'Do', onClick: () => {} }, sort: false });
    const gaps = rows.filter((r) => r.candidates.length && r.verdict !== 'steady');
    return el('div', { class: 'stack' }, el('div', { class: 'card scroll' }, tbl), el('p', { class: 'micro faint', text: 'Rule: ' + t.rule + '. Series come from the web pass with a url per market; today most hold one current point and a forecast, which is why the check is open.' }),
      gapLine(gaps.length ? gaps.length + ' candidate lane' + (gaps.length === 1 ? ' rests' : 's rest') + ' on a forecast or one year: ' + gaps.map((r) => r.label.toLowerCase()).join(', ') + '.' : 'Every candidate lane has 3 or more years of history behind its trend.',
        gaps.length && actionFor(gaps[0].finding_id) ? { label: 'Run the first check', onClick: () => openAction(actionFor(gaps[0].finding_id)) } : null));
  }

  function surfacesBlock(sf) {
    const rows = (sf && sf.rows) || [];
    if (!rows.length) return UI.emptyState({ screen: SLUG, title: 'No surfaces on file', text: 'The brain holds no Reddit language, review sources or channel records yet.', missing: ['reddit', 'reviews', 'channels'] });
    const kindText = { forum: 'Forum', reviews: 'Review source', social: 'Social' };
    const reach = (r) => r.status === 'not_pulled' ? 'not pulled yet' : r.status === 'no_pull' ? 'no pull for this surface' : r.kind === 'forum' ? r.quotes + ' quotes, ' + fmt.int(r.upvotes || 0) + ' upvotes' : r.kind === 'reviews' ? r.quotes + ' review quotes' : (r.posts == null ? NA : r.posts + ' posts' + (r.status === 'mock' ? ' (mock pull)' : ''));
    const pending = rows.filter((r) => r.verdict === 'not_pulled');
    const vrows = rows.filter((r) => r.verdict !== 'not_pulled').map((r) => { const a = actionFor(r.finding_id); return Object.assign({}, r, {
      kindText: kindText[r.kind] || r.kind, reachText: reach(r), theme: r.top_theme_label || (r.verdict === 'not_pulled' ? NA : 'none'),
      praise: r.praise_share == null ? NA : (r.praise_share * 100).toFixed(0) + ' percent praise', present: r.present == null ? NA : r.present ? 'yes' : 'no',
      answer: r.answered_on_site == null ? NA : r.answered_on_site ? 'yes' : 'no',
      actions: [a ? { label: r.kind === 'forum' ? 'Open the listening post' : r.kind === 'reviews' ? 'Claim the profile' : 'Open the account', onClick: () => openAction(a) } : { label: r.verdict === 'present' ? 'Present' : r.verdict === 'not_pulled' ? 'Plan a pull' : 'Watch', cls: 'quiet', onClick: () => {} }] }); });
    const tbl = UI.verdictTable({
      columns: [{ key: 'label', label: 'Surface' }, { key: 'kindText', label: 'Kind' }, { key: 'reachText', label: 'Reach on file' }, { key: 'praise', label: 'Tone' }, { key: 'theme', label: 'Loudest theme' }, { key: 'present', label: 'Brand present' }, { key: 'answer', label: 'Site answers the theme' }],
      rows: vrows,
      verdict: { at: 1, kind: (r) => r.verdict === 'gap' ? 'fix' : r.verdict === 'present' ? 'keep' : r.verdict === 'not_pulled' ? 'na' : 'watch', text: (r) => ({ gap: 'Reach, no presence', present: 'Present', watch: 'Below the floor', not_pulled: 'Not pulled' })[r.verdict], reason: (r) => sf.rule },
      actions: { label: 'Do', onClick: () => {} }, sort: false });
    const gaps = rows.filter((r) => r.verdict === 'gap');
    return el('div', { class: 'stack' }, el('div', { class: 'card scroll' }, tbl),
      el('p', { class: 'micro faint', text: 'Rule: ' + sf.rule + '. ' + (sf.note || '') + (pending.length ? ' Configured and not pulled yet (a pull is a paid call a person approves): ' + pending.map((r) => r.label).join(', ') + '.' : '') }),
      gapLine(gaps.length ? gaps.length + ' surface' + (gaps.length === 1 ? ' carries' : 's carry') + ' the category conversation with no record of the brand on ' + (gaps.length === 1 ? 'it' : 'them') + ': ' + gaps.map((r) => r.label).join(', ') + '.' : 'The brand is present on every surface with reach.',
        gaps.length && actionFor(gaps[0].finding_id) ? { label: 'Open the first', onClick: () => openAction(actionFor(gaps[0].finding_id)) } : null));
  }

  function marketplaceBlock(m) {
    if (!m || (!m.rows.length && !m.presence)) return UI.emptyState({ screen: SLUG, title: 'No marketplace read on file', text: 'The brain holds no Amazon listing or presence records for this brand yet.', missing: ['marketplaces'] });
    const p = m.presence, sm = m.summary || {}, site = m.site_per_pair || {};
    const stance = actionFor(SLUG + '.PROD-R31.amazon');
    const head = el('div', { class: 'card flat' });
    if (p) {
      head.append(el('h4', { text: 'Who sells the brand on Amazon' }),
        el('div', { class: 'row', style: { gap: '6px' } }, chip(p.brand_store ? 'brand store: yes' : 'brand store: none seen', p.brand_store ? 'good' : 'bad'), chip(p.sold_by_brand ? 'sold by the brand' : 'sold by the brand: no offer read', p.sold_by_brand ? 'good' : 'bad'), chip(p.aplus ? 'A+ content: yes' : 'A+ content: none seen', p.aplus ? 'good' : 'warn'), chip((p.in_stock == null ? NA : p.in_stock) + ' of ' + p.asins_read.length + ' listings read in stock'), chip('resellers seen: ' + (p.resellers.length ? p.resellers.join(', ') : 'none named'))),
        el('p', { class: 'small', text: p.text }),
        el('p', { class: 'micro muted', text: 'Read ' + (p.captured_at || 'undated') + '. ' + (p.lines_not_found.length ? 'Not found on Amazon: ' + p.lines_not_found.map((x) => x.replace('_', ' ')).join(', ') + '. ' : '') + sm.judged + ' listings judged, ' + fmt.int(sm.ratings || 0) + ' public ratings; ' + sm.unverified + ' thin rows read but not judged. Site price per pair: ' + (site.value == null ? NA : fmt.money(site.value)) + ' (' + (site.basis || '') + ').' }));
    } else head.append(el('p', { class: 'muted small', text: 'No presence record: whether the brand is the seller has not been read.' }));
    const pull = m.pull;
    head.append(el('div', { class: 'row', style: { gap: '6px', marginTop: '6px' } }, pull ? [chip('seller pull: ' + (pull.mode === 'live' ? 'live run ' + (pull.captured_at || '') : 'mock on file, sellers withheld'), pull.mode === 'live' ? 'good' : 'warn'), chip(pull.rows + ' rows'), chip(pull.usd != null ? fmt.money(pull.usd) + ' spent' : 'cost unavailable')] : chip('seller pull: not run', 'warn')));
    const vt = { price_spread: 'Off the site price', reseller: 'Reseller sells it', seller_not_read: 'Seller not read', brand_sells: 'Brand sells it', unverified: 'Thin read' };
    const vrows = m.rows.map((r) => { const a = actionFor(r.finding_id); return Object.assign({}, r, {
      pack: r.pack_units + (r.pack_units === 1 ? ' pair' : ' pairs'), priceText: r.price_usd == null ? NA : fmt.money(r.price_usd), ppText: r.per_pair == null ? NA : fmt.money(r.per_pair),
      spreadText: r.spread == null ? NA : (r.spread > 0 ? '+' : '') + (r.spread * 100).toFixed(0) + ' percent', starsText: r.stars == null ? NA : r.stars + ' (' + fmt.int(r.ratings || 0) + ')', sellerText: r.seller || 'not read',
      actions: [a ? { label: r.verdict === 'price_spread' ? 'Check the price' : 'Decide the stance', onClick: () => openAction(a) } : { label: r.verdict === 'unverified' ? 'Thin' : 'Watch', cls: 'quiet', onClick: () => {} }] }); });
    const tbl = UI.verdictTable({
      columns: [{ key: 'asin', label: 'ASIN' }, { key: 'title', label: 'Listing', format: (v) => (v || '').slice(0, 60) }, { key: 'pack', label: 'Pairs' }, { key: 'priceText', label: 'Price' }, { key: 'ppText', label: 'Per pair' }, { key: 'spreadText', label: 'Against the site' }, { key: 'starsText', label: 'Stars (ratings)' }, { key: 'sellerText', label: 'Seller' }],
      rows: vrows,
      verdict: { at: 2, kind: (r) => r.verdict === 'price_spread' ? 'fix' : r.verdict === 'reseller' ? 'watch' : r.verdict === 'brand_sells' ? 'keep' : 'na', text: (r) => vt[r.verdict], reason: (r) => m.rule },
      actions: { label: 'Do', onClick: () => {} }, sort: false });
    const spreads = m.rows.filter((r) => r.verdict === 'price_spread');
    return el('div', { class: 'stack' }, head, el('div', { class: 'card scroll' }, tbl),
      el('p', { class: 'micro faint', text: 'Rule: ' + m.rule + '. Pairs come from the listing title; a listing far under the site price with few ratings is checked as a possible copy, never assumed one. Listing records come from a public search pull; the seller of record comes from the listing pull (listing_pull.py), and only a live run fills it.' }),
      gapLine(p && p.sold_by_brand === false ? 'The brand is not the seller on its own Amazon listings' + (spreads.length ? ', and ' + spreads.length + ' listings are priced ' + (spreads.length === 1 ? '' : '25 percent or more ') + 'off the site price' : '') + '. One stance decision covers it.' : spreads.length ? spreads.length + ' listings are priced off the site price.' : 'The brand is the seller of record and the listing prices track the site.',
        stance ? { label: 'Decide the stance', onClick: () => openAction(stance) } : spreads.length && actionFor(spreads[0].finding_id) ? { label: 'Check the first', onClick: () => openAction(actionFor(spreads[0].finding_id)) } : null));
  }

  function cadenceBlock(c) {
    if (!c || !c.brands.length) return UI.emptyState({ screen: SLUG, title: 'No launches on file', text: 'The web pass keeps competitor launches with a url and a date. Run it for this brand.', missing: ['web_pass'] });
    const brands = c.brands;
    const chart = Charts.bar({ title: 'Launches per brand, last 12 and 24 months', labels: brands.map((b) => b.brand.length > 12 ? b.brand.slice(0, 11) + '.' : b.brand), unit: 'n',
      series: [{ name: 'last 12 months', values: brands.map((b) => b.n_12m) }, { name: 'last 24 months', values: brands.map((b) => b.n_24m) }],
      note: 'Public launches from the web pass, ' + (c.launches_read || 0) + ' read, a url and a date on each. Press-covered launches, not a full catalogue; small brands under-count.' });
    const ours = c.ours || {};
    const line = ours.n_12m != null ? 'Our cadence: ' + ours.n_12m + ' launch' + (ours.n_12m === 1 ? '' : 'es') + ' in 12 months' + (c.competitor_median_12m != null ? ' against a competitor median of ' + c.competitor_median_12m : '') + (ours.months_since_last != null ? ', last one ' + ours.months_since_last.toFixed(0) + ' months ago.' : '.') : 'Our cadence: unavailable.';
    const vt = { in_play: 'In play, none of ours', matched: 'Matched', watch: 'Watch', quiet: 'Quiet', proof: 'Proof lane', not_sold: 'Not sold' };
    const vrows = c.lanes.map((r) => { const a = actionFor(r.finding_id) || actionFor(SLUG + '.PROD-R06.' + r.key); return Object.assign({}, r, {
      theirs: r.theirs_24m ? r.theirs_12m + ' in 12 months, ' + r.theirs_24m + ' in 24 (' + r.brands_24m.join(', ') + ')' : 'none',
      newestText: r.newest ? r.newest.brand + ' ' + r.newest.date + ': ' + (r.newest.what || '').slice(0, 70) : 'none',
      oursText: r.our_last ? r.our_last.date + ': ' + (r.our_last.what || '').slice(0, 60) + (r.months_since_ours != null ? ' (' + r.months_since_ours.toFixed(0) + ' months ago)' : '') : 'none on file',
      soldText: r.sold == null ? NA : r.sold ? 'yes' : 'no',
      actions: [r.verdict === 'in_play' && a ? { label: 'Brief the next SKU', onClick: () => openAction(a) } : { label: r.verdict === 'matched' ? 'Holding' : r.verdict === 'not_sold' ? 'Not ours' : r.verdict === 'proof' ? 'Proof, not a SKU' : 'Watch', cls: 'quiet', onClick: () => {} }] }); });
    const tbl = UI.verdictTable({
      columns: [{ key: 'label', label: 'Lane' }, { key: 'theirs', label: 'Competitor launches' }, { key: 'newestText', label: 'Newest of theirs' }, { key: 'oursText', label: 'Our last launch there' }, { key: 'soldText', label: 'We sell it' }],
      rows: vrows,
      verdict: { at: 1, kind: (r) => r.verdict === 'in_play' ? 'fix' : r.verdict === 'matched' ? 'keep' : (r.verdict === 'not_sold' || r.verdict === 'proof') ? 'na' : 'watch', text: (r) => vt[r.verdict], reason: (r) => c.rule },
      actions: { label: 'Do', onClick: () => {} }, sort: false });
    const gaps = c.lanes.filter((r) => r.verdict === 'in_play');
    const first = gaps.length ? (actionFor(gaps[0].finding_id) || actionFor(SLUG + '.PROD-R06.' + gaps[0].key)) : null;
    return el('div', { class: 'stack' }, el('div', { class: 'grid two' }, el('div', { class: 'card' }, chart), el('div', { class: 'card flat scroll' }, el('h4', { text: 'Cadence by brand' }),
      el('table', { class: 'small' }, el('thead', null, el('tr', null, ['Brand', '12 m', '24 m', 'Last', 'Lanes', 'Median price'].map((h) => el('th', { text: h })))),
        el('tbody', null, brands.map((b) => el('tr', null, el('td', { text: b.brand + (b.self ? ' (us)' : '') }), el('td', { class: 'num', text: String(b.n_12m) }), el('td', { class: 'num', text: String(b.n_24m) }), el('td', { text: b.last + ' (' + b.months_since_last.toFixed(0) + ' mo)' }), el('td', { text: b.lanes.join(', ') }), el('td', { class: 'num', text: b.median_price == null ? NA : fmt.money(b.median_price) }))))),
      el('p', { class: 'small', text: line }))),
      el('div', { class: 'card scroll' }, tbl),
      el('p', { class: 'micro faint', text: 'Rule: ' + c.rule + '. Proof lanes (guarantee, creator) are claims, not SKUs, and never read as in play. A month reads as its 15th, a bare year as 1 July.' }),
      gapLine(gaps.length ? gaps.length + ' lane' + (gaps.length === 1 ? ' we sell is' : 's we sell are') + ' in play with nothing of ours launched there in 24 months: ' + gaps.map((r) => r.label.toLowerCase()).join(', ') + '.' : 'No lane we sell has competitor launches without one of ours.',
        first ? { label: 'Brief the first', onClick: () => openAction(first) } : null));
  }

  function returnsBlock(rr) {
    if (!rr || rr.unavailable) return UI.emptyState({ screen: SLUG, title: 'No return rates by line', text: (rr && rr.reason) || 'Orders and returns are not connected.', missing: [(rr && rr.fix) || 'shopify'] });
    const rows = rr.rows || [];
    if (!rows.length) return UI.emptyState({ screen: SLUG, title: 'No orders in the last 12 whole months', text: 'The orders table holds nothing in the window.', missing: ['orders'] });
    const pct = (v) => v == null ? NA : (v * 100).toFixed(1) + ' percent';
    const vt = { high: 'Returning high', normal: 'Normal', thin: 'Too few to judge' };
    const vrows = rows.map((r) => { const a = actionFor(r.finding_id); return Object.assign({}, r, {
      rateText: pct(r.rate) + (r.x_median != null ? ' (' + r.x_median + 'x median)' : ''), n: r.returns + ' of ' + fmt.int(r.units), reasonsText: r.reasons.length ? r.reasons.map((x) => x[0] + ' ' + x[1]).join(', ') : 'none',
      actions: [a ? { label: 'Cut the returns', onClick: () => openAction(a) } : { label: r.verdict === 'thin' ? 'Thin' : 'Fine', cls: 'quiet', onClick: () => {} }] }); });
    const tbl = UI.verdictTable({
      columns: [{ key: 'line', label: 'Line' }, { key: 'category', label: 'Category' }, { key: 'rateText', label: 'Return rate' }, { key: 'n', label: 'Returns of units' }, { key: 'reasonsText', label: 'Top reasons' }],
      rows: vrows,
      verdict: { at: 1, kind: (r) => r.verdict === 'high' ? 'fix' : r.verdict === 'thin' ? 'na' : 'keep', text: (r) => vt[r.verdict], reason: (r) => rr.rule },
      actions: { label: 'Do', onClick: () => {} }, sort: false });
    const high = rows.filter((r) => r.verdict === 'high');
    return el('div', { class: 'stack' }, el('div', { class: 'card scroll' }, tbl),
      el('p', { class: 'micro faint', text: 'Store: ' + pct(rr.store_rate) + ' of ' + fmt.int(rr.units) + ' units returned over ' + rr.first + ' to ' + rr.last + '; median line rate ' + pct(rr.median) + '. Rule: ' + rr.rule + '. Simulated orders.' }),
      gapLine(high.length ? high.length + ' line' + (high.length === 1 ? ' returns' : 's return') + ' at 1.5 times the store median or more: ' + high.map((r) => r.line).join(', ') + '.' : 'No line returns far above the store median.',
        high.length && actionFor(high[0].finding_id) ? { label: 'Cut the first', onClick: () => openAction(actionFor(high[0].finding_id)) } : null));
  }

  function questionsBlock(q) {
    const rows = (q && q.rows) || [];
    if (!rows.length) return UI.emptyState({ screen: SLUG, title: 'No open questions', text: 'The brain holds no open questions for the founder.', missing: ['brain'] });
    const vt = { overdue: 'Asked, no answer', never_asked: 'Never asked', asked: 'Asked, waiting', answered: 'Answered' };
    const vrows = rows.map((r) => { const a = actionFor(r.finding_id); return Object.assign({}, r, {
      q: r.doubt ? '"' + r.doubt + '"' : r.question.slice(0, 80), quotesText: r.quotes == null ? NA : String(r.quotes), theme: r.theme_label || NA,
      state: r.answered_on ? 'answered ' + fmt.date(r.answered_on) : r.asked_on ? 'asked ' + fmt.date(r.asked_on) + (r.days_open != null ? ' (' + r.days_open + ' d)' : '') : 'not asked yet',
      site: r.records_answer_theme == null ? NA : r.records_answer_theme ? 'the theme, yes; this doubt, no' : 'no',
      actions: [a ? { label: 'Ask the founder', onClick: () => openAction(a) } : { label: r.verdict === 'answered' ? 'Done' : 'Thin', cls: 'quiet', onClick: () => {} }] }); });
    const tbl = UI.verdictTable({
      columns: [{ key: 'q', label: 'The doubt' }, { key: 'theme', label: 'Theme' }, { key: 'quotesText', label: 'Complaint quotes' }, { key: 'who', label: 'Who can answer' }, { key: 'state', label: 'State' }, { key: 'site', label: 'Records answer it' }],
      rows: vrows,
      verdict: { at: 1, kind: (r) => r.verdict === 'overdue' ? 'fix' : r.verdict === 'never_asked' ? 'watch' : r.verdict === 'answered' ? 'keep' : 'na', text: (r) => vt[r.verdict], reason: (r) => q.rule },
      actions: { label: 'Do', onClick: () => {} }, sort: false });
    const open = rows.filter((r) => r.verdict === 'overdue' || r.verdict === 'never_asked');
    return el('div', { class: 'stack' }, el('div', { class: 'card scroll' }, tbl),
      el('p', { class: 'micro faint', text: 'Rule: ' + q.rule + '. A doubt with no proof is an offer, guarantee or product problem; copy alone cannot answer it. The answer becomes a claims, policies or offers record and the theme card reads it.' }),
      gapLine(open.length ? open.length + ' question' + (open.length === 1 ? ' waits' : 's wait') + ' on the founder: ' + open.map((r) => '"' + (r.doubt || r.question.slice(0, 40)) + '"').join(', ') + '.' : 'Every open question has been asked and answered.',
        open.length && actionFor(open[0].finding_id) ? { label: 'Ask the first', onClick: () => openAction(actionFor(open[0].finding_id)) } : null));
  }

  function pullsBlock(p) {
    const rows = (p && p.rows) || [];
    if (!rows.length) return UI.emptyState({ screen: SLUG, title: 'No pulls configured', text: 'This brand has no connector config (apify.json) and no fixtures.', missing: ['apify'] });
    const vt = { due: 'Due', never: 'Never run', mock: 'Mock stands in', unset: 'No actor set', fresh: 'Fresh' };
    const vrows = rows.map((r) => { const a = actionFor(r.finding_id); return Object.assign({}, r, {
      actorText: r.actor || (r.key === 'web_pass' ? 'session task' : 'not set'), last: r.captured_at ? fmt.date(r.captured_at) + (r.age_days != null ? ' (' + r.age_days + ' d)' : '') : 'never',
      win: r.window_days + ' d' + (r.next_due ? ', next ' + fmt.date(r.next_due) : ''), feedsText: (r.feeds || []).join(', '),
      est: r.estimate_usd == null ? (r.actor ? 'no price on file' : NA) : fmt.money(r.estimate_usd) + (r.over_run_cap ? ' (over the run cap)' : ''),
      actions: [a ? { label: r.verdict === 'unset' ? 'Set the actor' : r.verdict === 'due' ? 'Approve the refresh' : 'Approve the live run', onClick: () => openAction(a) } : { label: 'Fresh', cls: 'quiet', onClick: () => {} }] }); });
    const tbl = UI.verdictTable({
      columns: [{ key: 'label', label: 'Pull' }, { key: 'actorText', label: 'Actor' }, { key: 'last', label: 'Last capture' }, { key: 'win', label: 'Window' }, { key: 'feedsText', label: 'Feeds' }, { key: 'est', label: 'Estimate a run' }, { key: 'note', label: 'Note', format: (v) => v || '' }],
      rows: vrows,
      verdict: { at: 1, kind: (r) => r.verdict === 'due' ? 'fix' : r.verdict === 'fresh' ? 'keep' : r.verdict === 'unset' ? 'na' : 'watch', text: (r) => vt[r.verdict], reason: (r) => p.rule },
      actions: { label: 'Do', onClick: () => {} }, sort: false });
    const open = rows.filter((r) => r.verdict !== 'fresh');
    const caps = p.caps || {};
    return el('div', { class: 'stack' }, el('div', { class: 'card scroll' }, tbl),
      el('p', { class: 'micro faint', text: 'Caps: ' + (caps.per_run_usd != null ? fmt.money(caps.per_run_usd) + ' a run, ' + fmt.money(caps.per_week_usd) + ' a week' : 'none on file') + '. Estimates come from the connector price table at the configured size with its margin. Nothing on this page runs a pull; a person approves each one from the card. Rule: ' + p.rule + '.' }),
      gapLine(open.length ? open.length + ' pull' + (open.length === 1 ? ' is' : 's are') + ' not fresh: ' + open.map((r) => r.label.toLowerCase() + ' (' + vt[r.verdict].toLowerCase() + ')').join(', ') + '.' : 'Every pull is inside its window.',
        open.length && actionFor(open[0].finding_id) ? { label: 'Open the first', onClick: () => openAction(actionFor(open[0].finding_id)) } : null));
  }

  function firstRunsBlock(fr) {
    const rows = ((fr && fr.rows) || []).filter((r) => r.verdict !== 'closed');
    if (!rows.length) return UI.emptyState({ screen: SLUG, title: 'No candidates', text: 'Screen a candidate in; from gated on, its first run is sized here.', missing: ['pipeline'] });
    const vt = { full_moq_risk: 'Full MOQ, no option', no_plan: 'No first run on file', sized: 'Sized', not_yet: 'Before gated' };
    const size = (r) => { const units = prompt('First run for ' + r.name + ': units wanted for the first 90 days', r.units || ''); if (units == null) return;
      const format = prompt('Format of the first run (fully custom pack, stock blank with a sleeve, ...)', r.format || ''); if (format == null) return;
      const moq = prompt('MOQ of that format, in units', r.moq_units || ''); if (moq == null) return;
      const cash = prompt('Cash out for the first run, USD', r.cash_usd || ''); if (cash == null) return;
      const opt = prompt('Lower-MOQ alternative considered (format, MOQ, cash), or leave empty', r.lower_moq_option || ''); if (opt == null) return;
      candidatePost('candidates/' + r.candidate_id, { first_run: { units, format, moq_units: moq, cash_usd: cash, lower_moq_option: opt }, who: 'person' }); };
    const vrows = rows.map((r) => { const a = actionFor(r.finding_id); return Object.assign({}, r, {
      unitsText: r.units == null ? NA : fmt.int(r.units), moqText: r.moq_units == null ? NA : fmt.int(r.moq_units) + (r.moq_over_units ? ' (over the units wanted)' : ''), fmtText: r.format || NA,
      cashText: r.cash_usd == null ? NA : fmt.money(r.cash_usd) + (r.cash_share_28d != null ? ' (' + (r.cash_share_28d * 100).toFixed(0) + ' percent of 28-day net)' : ' (revenue unknown)'), optText: r.lower_moq_option || 'none noted',
      actions: [a ? { label: r.verdict === 'no_plan' ? 'Size the first run' : 'Cost a lower-MOQ format', onClick: () => openAction(a) } : null, r.verdict !== 'not_yet' ? { label: r.verdict === 'no_plan' ? 'Enter it' : 'Edit', cls: 'quiet', onClick: () => size(r) } : { label: 'Before gated', cls: 'quiet', onClick: () => {} }].filter(Boolean) }); });
    const tbl = UI.verdictTable({
      columns: [{ key: 'name', label: 'Candidate' }, { key: 'stage', label: 'Stage' }, { key: 'unitsText', label: 'Units wanted' }, { key: 'fmtText', label: 'Format' }, { key: 'moqText', label: 'MOQ' }, { key: 'cashText', label: 'Cash out' }, { key: 'optText', label: 'Lower-MOQ option' }],
      rows: vrows,
      verdict: { at: 1, kind: (r) => r.verdict === 'full_moq_risk' ? 'fix' : r.verdict === 'no_plan' ? 'watch' : r.verdict === 'sized' ? 'keep' : 'na', text: (r) => vt[r.verdict], reason: (r) => fr.rule },
      actions: { label: 'Do', onClick: () => {} }, sort: false });
    const open = rows.filter((r) => r.verdict === 'full_moq_risk' || r.verdict === 'no_plan');
    return el('div', { class: 'stack' }, el('div', { class: 'card scroll' }, tbl),
      el('p', { class: 'micro faint', text: 'Rule: ' + fr.rule + '. 28-day net revenue: ' + (fr.net_28d == null ? NA : fmt.money(fr.net_28d)) + ', simulated. The first run is written on the candidate; the cash plan and the brief read it.' }),
      gapLine(open.length ? open.length + ' candidate' + (open.length === 1 ? ' has' : 's have') + ' a first run to size or de-risk: ' + open.map((r) => r.name).join(', ') + '.' : 'Every candidate from gated on has a sized first run with a lower-MOQ option.',
        open.length && actionFor(open[0].finding_id) ? { label: 'Open the first', onClick: () => openAction(actionFor(open[0].finding_id)) } : null));
  }

  function loadDesk(o) {
    const d = o.desk || {};
    const w = (o.window || {}).trend;
    const parts = [];
    parts.push(section('desk-trends', 'Where is the category going, and which lane is under-advertised?', 'Public market sizes and growth from the web pass, a url and a date on every number, against our category mix over 12 whole months. Sales are simulated; markets are public.', trendsBlock(d.trends || { on_file: false }, d.mix || {})));
    parts.push(section('desk-lanes', 'Which lanes are competitors betting on, and what launched?', 'Competitor pages from the Ad Library pull in the brain, by lane: who pushes it, how long their ads have run, what launched in the last 24 months, and whether we sell and advertise it.', lanesBlock(d.lanes)));
    parts.push(section('desk-cadence', 'Who launches, how often, and where are we quiet?', 'Competitor launches from the web pass by brand and by lane over 12 and 24 months, against our own cadence; a lane we sell where they keep launching and we have not is in play.', cadenceBlock(d.cadence)));
    parts.push(section('desk-conversation', 'What are people talking about, and what goes unanswered?', 'Themes across reviews (site, Amazon, Trustpilot, retailers), Reddit and an Instagram hashtag pull: volume, complaint against praise, the top doubt, and whether the site and the active ads answer it.', conversationBlock(d.conversation)));
    parts.push(section('desk-surfaces', 'Where do buyers talk, and where are we absent?', 'Each subreddit in the Reddit pull, each review source in the ladders and each social surface the brand names: reach on file, tone, the loudest theme, and whether any brand record shows us there. Counts only; no usernames.', surfacesBlock(d.surfaces)));
    parts.push(section('desk-questions', 'What does the desk need the founder to answer?', 'The open questions the brain holds, each a doubt from the objection ladders with the complaint quotes behind it and no policy, offer or claim that covers it; who can answer, whether it was asked, and whether any record answers it yet.', questionsBlock(d.questions)));
    parts.push(section('desk-preferences', 'Which preferences are shifting, and where do we stand on each?', 'Public survey numbers from the web pass against our own claims, our active ads, the competitors\' pitches and the category conversation.', preferencesBlock(d.preferences)));
    parts.push(section('desk-map', 'Where do we sit against the competitors, and which position is open?', 'Price per pair against the share of proof-led hooks, from the brain\'s competitor records and the Ad Library pull. Sized by active ads. The Reddit frames show how the category talks about itself.', mapBlock(d.map)));
    parts.push(section('desk-avatars', 'Which buyers do we serve, and which do competitors pitch to that we do not?', 'The brain\'s avatars by the lines we sell: our evidence against competitor pitches in every cell. Big segments on a complaint-led theme carry the repeat revenue at risk.', avatarBlock(d.avatars)));
    parts.push(section('desk-search', 'What do people search for around the brand and the category, and which searches have no page?', 'Brand, category, competitor and problem terms built from the brain, with Search Console and Google search-term demand where connected, against the pages in the site map.', searchBlock(d.search)));
    parts.push(section('desk-behind', 'Where is the brand falling behind on positioning and avatars?', 'Every positioning and avatar gap the audit found, ranked by money at stake where a formula exists, then reach, with the owner and the capability that closes it.', behindBlock(d.behind, d.map)));
    parts.push(section('desk-demand', 'Which lines are losing share, and which reviews say why?', 'Last 3 whole months against the same months a year earlier. A line fires when units fall or growth trails the store by 1 point or more.', demandBlock(d, w || { months: [], year_ago: [] })));
    parts.push(section('desk-price', 'Where do our prices sit against the competitor band?', 'Per-pair list price by line against the band of competitor median prices from the brain. Socks only; other categories have no competitor price on file.', priceBlock(d.price_bands || {})));
    parts.push(section('desk-reviews', 'What do reviews praise and fail, line by line?', 'Public site review totals per line, with the objection ladder rungs built from them.', reviewBlock(d.reviews || [])));
    parts.push(section('desk-returns', 'Which lines come back, and why?', 'Return rate per line over the last 12 whole months from orders and the return leg of reversed orders, against the store median, with the reasons. Room metric sku_return_rate.', returnsBlock(d.returns)));
    parts.push(section('desk-margin', 'Does each candidate make money after real costs?', 'The margin gate per candidate: planned price stepping down through landed cost, the donated item, fulfilment and payment fees to contribution, every term from the finance inputs or the brain.', marginBlock(d.margin)));
    parts.push(section('desk-lane-map', 'Which lanes are growing with room left, and which are growing and already full?', 'Trend direction against competitive saturation per lane, read together as one go or no-go signal: market growth and launches from the web pass, sellers from the competitor pages in the brain.', laneMapBlock(d.lane_map)));
    parts.push(section('desk-spend', 'Who is actually funding which lane, not just posting about it?', 'Competitor pages by the longest run of their active ads per lane. Three or more advertisers at 90 days is a funded test; one at 14 days is a live test; the rest is noise.', spendBlock(d.spend)));
    parts.push(section('desk-price-signal', 'What would buyers actually pay for a pair?', 'Price mentions mined from review quotes across Amazon, the brand site, Trustpilot and retailers, as a median per pair, against the competitor band, our own pair and each candidate\'s planned price.', priceSignalBlock(d.price_signal)));
    parts.push(section('desk-complaints', 'What do buyers hate about what exists, listing by listing?', 'Complaint themes mined from the brand\'s own Amazon listings as a share of reviews mined, against praise, with the listing\'s public stars, ratings and price. One complaint over 15 percent is the angle to build on.', complaintBlock(d.complaints)));
    parts.push(section('desk-marketplace', 'Who sells us on Amazon, and at what price?', 'The brain\'s Amazon read: whether a brand store, A+ content or a brand-as-seller offer showed, the resellers seen, and every listing with its price per pair against the site. Public listing data, no order counts.', marketplaceBlock(d.marketplace)));
    parts.push(section('desk-gates', 'Is each candidate ready to fund: an owned angle and the 5 go-live gates?', 'Angle confidence (filled, sourced, not a competitor claim) and the gates per candidate: provable claim, owned difference, brand threshold, contribution margin, ad-cost ceiling, plus the compliance check.', gatesBlock(d.gates)));
    parts.push(section('desk-scorecard', 'Which candidates does the founder decide on this week?', 'The fixed scorecard with the brand\'s weights: demand, margin, differentiation, compliance and cash timing, each scored in code, ranked, with the go or no-go memo drafted from the numbers and the review date.', scorecardBlock(d.scorecard)));
    parts.push(section('desk-video', 'Is the demand one clip or a real pattern?', 'Independent platforms showing demand per lane: the Instagram hashtag pull, Reddit mentions and upvotes, competitor creator-style ads and our own, with the candidates that rest on each lane.', videoBlock(d.video)));
    parts.push(section('desk-tech-packs', 'Which candidates have a real, versioned spec ready for sourcing?', 'Tech pack versions per candidate: tolerances, the bill of materials and the packaging cost line. A pack saved from the card becomes the current version and supersedes the last.', techPackBlock(d.tech_packs)));
    parts.push(section('desk-first-run', 'How big is the first run, and does it have to be that big?', 'From gated on, the first production run per candidate: units wanted, the format and its MOQ, the cash it ties up as a share of 28-day net revenue, and the lower-MOQ alternative considered (bank idea BRD-249).', firstRunsBlock(d.first_runs)));
    parts.push(section('desk-hours', 'Has any candidate used up its research hours?', 'Hours logged per candidate against the hours allowed through its stage, from the brand\'s budget per stage. Research cannot sprawl past the box.', hoursBlock(d.hours)));
    parts.push(section('desk-trend-checks', 'Does each lane\'s trend rest on history, or on a forecast?', 'The 12-month rate against the multi-year rate per lane from the web pass series: a trend is trusted with 3 or more years of history on the exact term; a last year over twice the multi-year rate is a spike.', trendChecksBlock(d.trend_checks)));
    parts.push(section('desk-pattern', 'Is each candidate evergreen, seasonal or a trend, and when does cash move?', 'The demand pattern from our own 12-month series by category and the web pass, with the cash timing it implies and the cash plan attached to each candidate.', patternBlock(d.pattern)));
    parts.push(section('desk-pipeline', 'What is in the next-SKU pipeline, and what is past its time box?', 'Candidates screened in from the gaps above or by hand, their stage, fast checks, time box and hours. Advance, log hours or kill from the card; every write lands in the pipeline log.', pipelineBlock(d.pipeline || { rows: [] })));
    parts.push(section('desk-pulls', 'How fresh is what this desk reads, and what would a refresh cost?', 'Every pull the desk depends on: its last capture, age against its window, the blocks it feeds and the estimate for a run under the brand\'s caps. A person approves each paid call; nothing runs from here.', pullsBlock(d.pulls)));
    const jumps = UI.pills({ items: parts.map((p) => ({ key: p.id, label: p.querySelector('h2').textContent.replace(/\?.*$/, '?').split(',')[0].slice(0, 42) })), onChange: (key) => { const t = document.getElementById(key); if (t) t.scrollIntoView({ behavior: 'smooth', block: 'start' }); } });
    mount('#desk', el('section', { class: 'section' }, el('div', { class: 'sec-head' }, el('h2', { text: 'The desk: ' + parts.length + ' blocks' }), el('span', { class: 'sub', text: 'Each block ends in a gap line and an action. Jump to one:' })), jumps), ...parts);
  }

  // ---------- 6. the audit ----------
  function loadAudit(o) {
    const a = o.audit || { findings: [], rules: [] };
    document.getElementById('audit-sub').textContent = a.findings.length + ' finding' + (a.findings.length === 1 ? '' : 's') + ' from ' + a.rules.length + ' rules. Resolved findings stay 28 days.';
    mount('#audit',
      el('div', { class: 'card scroll' }, UI.table({
        columns: [{ key: 'severity', label: 'Severity' }, { key: 'rule_id', label: 'Rule' }, { key: 'what', label: 'Entity' }, { key: 'sentence', label: 'Finding' },
          { key: 'stake', label: 'Stake', align: 'right', format: (v) => v == null ? NA : fmt.money(v) }, { key: 'confidence', label: 'Confidence', align: 'right', format: (v) => v == null ? NA : v.toFixed(1) }, { key: 'status', label: 'Status' }],
        rows: a.findings.map((f) => ({ severity: f.severity, rule_id: f.rule_id, what: f.entity.label, sentence: f.sentence, stake: f.money_at_stake ? f.money_at_stake.usd : null, confidence: f.confidence, status: f.status })),
        sort: false, empty: 'No findings. Every rule read its inputs and found nothing to say.' })),
      el('h4', { text: 'The rules', style: { margin: '10px 0 4px' } }),
      el('div', { class: 'card scroll rules' }, UI.table({
        columns: [{ key: 'rule_id', label: 'Rule' }, { key: 'name', label: 'What it reads and when it fires' }, { key: 'inputs', label: 'Inputs', format: (v) => (v || []).join(', ') }, { key: 'capability', label: 'Capability' }],
        rows: a.rules, sort: false })));
    mount('#exports',
      el('button', { class: 'btn sm', type: 'button', text: 'Findings CSV', onclick: () => UI.csv(a.findings.map((f) => ({ id: f.id, severity: f.severity, status: f.status, sentence: f.sentence, stake_usd: f.money_at_stake ? f.money_at_stake.usd : null, confidence: f.confidence })), null, 'research-findings.csv') }),
      el('button', { class: 'btn sm', type: 'button', text: 'Print', onclick: () => window.print() }));
  }

  async function load() {
    let o;
    try { o = await api(BASE + 'overview' + Q); }
    catch (e) { mount('#badge', 'Could not load the desk: ' + e.message); return; }
    const b = o.brand || {};
    mount('#badge', b.simulated ? el('span', null, el('b', { text: 'Simulated data. ' }), b.simulated_note + (b.brain_version ? ' Brain version ' + b.brain_version.slice(0, 7) + '.' : ''))
      : el('span', null, el('b', { text: (b.name || b.brand) + ' live data. ' }), 'Read-only.'));
    await loadPlan(o);
    loadWrong(o);
    loadActions();
    loadDesk(o);
    loadAudit(o);
  }
  load();
})();
