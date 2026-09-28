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
  function openAction(a) {
    UI.panel({ title: a.title, body: UI.actionCard(a, { expanded: true, screen: SLUG }) });
  }
  const state = { actions: [], byFinding: {} };
  function actionFor(findingId) { return state.byFinding[findingId] || null; }

  // ---------- 1. the plan ----------
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
  function loadWrong(o) {
    const groups = o.wrong || [];
    const n = groups.reduce((s, g) => s + g.findings.length, 0);
    document.getElementById('wrong-title').textContent = n ? 'What is wrong, ranked: ' + n + ' finding' + (n === 1 ? '' : 's') : 'Nothing is wrong on this desk today';
    if (!groups.length) { mount('#wrong', el('p', { class: 'muted', text: 'No rule fired for the window. The desk below still shows where the gaps are.' })); return; }
    mount('#wrong', ...groups.map((g) => el('div', { class: 'card flat wrong-group' },
      el('div', { class: 'g-head' }, el('h4', { text: g.name }), chip(g.rule_id, 'mono'), chip(g.severity, SEV_TONE[g.severity]), el('span', { class: 'micro muted', text: g.findings.length + ' finding' + (g.findings.length === 1 ? '' : 's') })),
      ...g.findings.map(findingCard))));
  }

  // ---------- 3 and 4. actions ----------
  function loadActions() {
    const list = state.actions.filter((a) => a.status !== 'unavailable');
    if (!list.length) { mount('#actions', el('p', { class: 'muted', text: 'No open action.' })); return; }
    mount('#actions', ...list.map((a, i) => UI.actionCard(a, { expanded: i === 0, screen: SLUG })));
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
  async function candidatePost(path, body) {
    try { await api(BASE + path + Q, { method: 'POST', body }); load(); }
    catch (e) { alert('Could not save: ' + e.message); }
  }
  function pipelineBlock(p) {
    const floor = p.floor_pct != null ? 'The brand floor is ' + p.floor_pct + ' percent, from ' + p.floor_source + '.' : 'No floor on file: enter a target contribution margin on the setup screen.';
    const rows = p.rows || [];
    const funnel = Charts.funnel({ title: 'Candidates by stage reached', stages: (p.funnel || []).map((f) => ({ label: f.stage, value: f.n })), unit: 'n',
      note: 'A candidate at a later stage counts at every stage before it. ' + (p.rule || '') + '.' });
    const stageNext = (r) => { const i = (p.stages || []).indexOf(r.stage); return i >= 0 && i < p.stages.length - 1 ? p.stages[i + 1] : null; };
    const vrows = rows.map((r) => { const acts = (r.finding_ids || []).map(actionFor).filter(Boolean); const nx = stageNext(r); return Object.assign({}, r, {
      stageText: r.stage + (r.closed ? '' : r.days_left != null ? (r.days_left < 0 ? ', ' + Math.abs(r.days_left) + ' d over the box' : ', ' + r.days_left + ' d left') : ''),
      checks: (p.checks || []).map((c) => pretty(c) + ' ' + ((r.screen_result || {})[c] || 'not run')).join(', '),
      angle: r.angle_text || 'no angle yet', price: r.planned_price, hours: r.hours_logged,
      actions: [].concat(acts.length ? [{ label: acts[0].rule_id === 'PROD-R15' ? 'Kill or fix' : 'Decide', onClick: () => openAction(acts[0]) }] : [],
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
    return el('div', { class: 'stack' }, orient,
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
      el('div', { class: 'grid two' }, el('div', { class: 'card' }, strip), el('div', { class: 'card scroll' }, el('h4', { text: 'Our mix against the market, 12 whole months to ' + (mix.last || NA) }), mixTable)),
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

  function loadDesk(o) {
    const d = o.desk || {};
    const w = (o.window || {}).trend;
    const parts = [];
    parts.push(section('desk-trends', 'Where is the category going, and which lane is under-advertised?', 'Public market sizes and growth from the web pass, a url and a date on every number, against our category mix over 12 whole months. Sales are simulated; markets are public.', trendsBlock(d.trends || { on_file: false }, d.mix || {})));
    parts.push(section('desk-lanes', 'Which lanes are competitors betting on, and what launched?', 'Competitor pages from the Ad Library pull in the brain, by lane: who pushes it, how long their ads have run, what launched in the last 24 months, and whether we sell and advertise it.', lanesBlock(d.lanes)));
    parts.push(section('desk-conversation', 'What are people talking about, and what goes unanswered?', 'Themes across reviews (site, Amazon, Trustpilot, retailers), Reddit and an Instagram hashtag pull: volume, complaint against praise, the top doubt, and whether the site and the active ads answer it.', conversationBlock(d.conversation)));
    parts.push(section('desk-preferences', 'Which preferences are shifting, and where do we stand on each?', 'Public survey numbers from the web pass against our own claims, our active ads, the competitors\' pitches and the category conversation.', preferencesBlock(d.preferences)));
    parts.push(section('desk-map', 'Where do we sit against the competitors, and which position is open?', 'Price per pair against the share of proof-led hooks, from the brain\'s competitor records and the Ad Library pull. Sized by active ads. The Reddit frames show how the category talks about itself.', mapBlock(d.map)));
    parts.push(section('desk-avatars', 'Which buyers do we serve, and which do competitors pitch to that we do not?', 'The brain\'s avatars by the lines we sell: our evidence against competitor pitches in every cell. Big segments on a complaint-led theme carry the repeat revenue at risk.', avatarBlock(d.avatars)));
    parts.push(section('desk-search', 'What do people search for around the brand and the category, and which searches have no page?', 'Brand, category, competitor and problem terms built from the brain, with Search Console and Google search-term demand where connected, against the pages in the site map.', searchBlock(d.search)));
    parts.push(section('desk-behind', 'Where is the brand falling behind on positioning and avatars?', 'Every positioning and avatar gap the audit found, ranked by money at stake where a formula exists, then reach, with the owner and the capability that closes it.', behindBlock(d.behind, d.map)));
    parts.push(section('desk-demand', 'Which lines are losing share, and which reviews say why?', 'Last 3 whole months against the same months a year earlier. A line fires when units fall or growth trails the store by 1 point or more.', demandBlock(d, w || { months: [], year_ago: [] })));
    parts.push(section('desk-price', 'Where do our prices sit against the competitor band?', 'Per-pair list price by line against the band of competitor median prices from the brain. Socks only; other categories have no competitor price on file.', priceBlock(d.price_bands || {})));
    parts.push(section('desk-reviews', 'What do reviews praise and fail, line by line?', 'Public site review totals per line, with the objection ladder rungs built from them.', reviewBlock(d.reviews || [])));
    parts.push(section('desk-margin', 'Does each candidate make money after real costs?', 'The margin gate per candidate: planned price stepping down through landed cost, the donated item, fulfilment and payment fees to contribution, every term from the finance inputs or the brain.', marginBlock(d.margin)));
    parts.push(section('desk-lane-map', 'Which lanes are growing with room left, and which are growing and already full?', 'Trend direction against competitive saturation per lane, read together as one go or no-go signal: market growth and launches from the web pass, sellers from the competitor pages in the brain.', laneMapBlock(d.lane_map)));
    parts.push(section('desk-pattern', 'Is each candidate evergreen, seasonal or a trend, and when does cash move?', 'The demand pattern from our own 12-month series by category and the web pass, with the cash timing it implies and the cash plan attached to each candidate.', patternBlock(d.pattern)));
    parts.push(section('desk-pipeline', 'What is in the next-SKU pipeline, and what is past its time box?', 'Candidates screened in from the gaps above or by hand, their stage, fast checks, time box and hours. Advance, log hours or kill from the card; every write lands in the pipeline log.', pipelineBlock(d.pipeline || { rows: [] })));
    mount('#desk', ...parts);
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
