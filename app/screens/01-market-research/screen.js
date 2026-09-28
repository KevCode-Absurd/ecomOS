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
  function pipelineBlock(p) {
    const floor = p.floor_pct != null ? 'The brand floor is ' + p.floor_pct + ' percent, from ' + p.floor_source + '.' : 'No floor on file: enter a target contribution margin on the setup screen.';
    const heroes = state.actions.filter((a) => a.rule_id === 'PROD-R03');
    return el('div', null,
      el('p', { class: 'small muted', text: 'Margin gate: ' + p.gate_rule + ' ' + floor }),
      el('div', { class: 'card scroll' }, UI.table({ columns: p.columns.map((c) => ({ key: c, label: pretty(c) })), rows: p.rows, sort: false, empty: 'No candidates yet. The pipeline fills when the first idea is screened.' })),
      gapLine(p.rows.length ? p.rows.length + ' candidates open.' : (heroes.length ? 'The pipeline is empty while ' + heroes.length + ' hero line' + (heroes.length === 1 ? ' has' : 's have') + ' no next SKU planned.' : 'The pipeline is empty. Every category with a hero line will show a plan-the-next-SKU action here.'),
        heroes.length ? { label: 'Plan the next SKU', onClick: () => openAction(heroes[0]) } : null));
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

  function loadDesk(o) {
    const d = o.desk || {};
    const w = (o.window || {}).trend;
    const parts = [];
    parts.push(section('desk-trends', 'Where is the category going, and which lane is under-advertised?', 'Public market sizes and growth from the web pass, a url and a date on every number, against our category mix over 12 whole months. Sales are simulated; markets are public.', trendsBlock(d.trends || { on_file: false }, d.mix || {})));
    parts.push(section('desk-lanes', 'Which lanes are competitors betting on, and what launched?', 'Competitor pages from the Ad Library pull in the brain, by lane: who pushes it, how long their ads have run, what launched in the last 24 months, and whether we sell and advertise it.', lanesBlock(d.lanes)));
    parts.push(section('desk-conversation', 'What are people talking about, and what goes unanswered?', 'Themes across reviews (site, Amazon, Trustpilot, retailers), Reddit and an Instagram hashtag pull: volume, complaint against praise, the top doubt, and whether the site and the active ads answer it.', conversationBlock(d.conversation)));
    parts.push(section('desk-demand', 'Which lines are losing share, and which reviews say why?', 'Last 3 whole months against the same months a year earlier. A line fires when units fall or growth trails the store by 1 point or more.', demandBlock(d, w || { months: [], year_ago: [] })));
    parts.push(section('desk-price', 'Where do our prices sit against the competitor band?', 'Per-pair list price by line against the band of competitor median prices from the brain. Socks only; other categories have no competitor price on file.', priceBlock(d.price_bands || {})));
    parts.push(section('desk-reviews', 'What do reviews praise and fail, line by line?', 'Public site review totals per line, with the objection ladder rungs built from them.', reviewBlock(d.reviews || [])));
    parts.push(section('desk-pipeline', 'What is in the next-SKU pipeline?', 'Candidates, their stage, time box and the margin gate.', pipelineBlock(d.pipeline || { columns: [], rows: [] })));
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
