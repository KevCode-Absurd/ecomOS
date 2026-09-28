/* Offers and pricing (round 1). Reads /api/04-offers-pricing/overview and composes kit components in the depth
   order: plan, what is wrong, actions, the desk, the audit. No number is computed here; the server sends every
   value, rule and sentence. No brand fact is written here; everything comes from the brain through the api. */
(function () {
  'use strict';
  const SLUG = '04-offers-pricing';
  const { el, fmt, mount } = UI;
  const brand = new URLSearchParams(location.search).get('brand') || 'bombas';
  const NA = 'unavailable';
  const SOURCE = { site: 'Site', ad_library: 'Meta Ad Library', press: 'Press', review: 'Reviews', interview: 'Interview', founder: 'Founder' };
  const pretty = (s) => String(s || '').replace(/_/g, ' ');
  const pct = (v, d) => v == null ? NA : (v * 100).toFixed(d == null ? 1 : d) + ' percent';
  let ACTIONS = [];

  // ---------- helpers ----------
  function section(id, head, ...body) {
    return el('section', { class: 'section', id: id }, UI.sectionHead(head), ...body);
  }
  function kv(pairs) {
    return el('dl', { class: 'kv' }, pairs.flatMap(([k, v]) => [el('dt', { text: k }), el('dd', { text: v })]));
  }
  function findAction(fid) { return ACTIONS.find((a) => (a.finding_ids || []).includes(fid) || a.id === fid); }
  function openAction(a) {
    const card = document.querySelector('#actions [data-id="' + CSS.escape(a.id) + '"]');
    if (!card) return;
    card.scrollIntoView({ behavior: 'smooth', block: 'start' });
    card.classList.add('flash');
    setTimeout(() => card.classList.remove('flash'), 1600);
    const btn = Array.from(card.querySelectorAll('button')).find((b) => b.textContent === 'Show steps');
    if (btn) btn.click();
  }
  /** The line every desk block ends in: the gap in words and the action that closes it. */
  function actionLine(text, a) {
    const node = el('div', { class: 'act-line' }, el('span', { class: 'kicker', text: 'Next move' }), el('span', { text: text }));
    if (a) node.append(UI.ownerChip(a), el('button', { class: 'btn soft sm', type: 'button', text: 'Open the action', onclick: () => openAction(a) }));
    return node;
  }

  // ---------- 0. head ----------
  function badge(b) {
    const name = b.name || b.brand || 'This brand';
    mount('#badge', b.simulated
      ? el('span', null, el('b', { text: 'Simulated data. ' }), 'Offers, prices and reviews come from ' + name + ' public pages; every sales number is generated. Nothing here is a ' + name + ' result.')
      : el('span', null, el('b', { text: name }), ' live data. Read-only.'));
  }

  // ---------- 1. the plan ----------
  function plan(d) {
    const open = d.plan.filter((a) => a.status !== 'unavailable');
    const con = d.plan.filter((a) => a.status === 'unavailable');
    const w = d.window;
    mount('#plan', UI.planBoard({
      title: 'The plan: offer and price moves to approve',
      sub: w.days + ' days to ' + fmt.date(w.ends_on) + '. ' + open.length + ' moves, ranked by the rubric.',
      orient: d.orientation, actions: open, limit: 10, screen: SLUG,
      tools: [el('button', { class: 'btn sm', type: 'button', text: 'Export CSV', onclick: () => UI.csv(d.plan.map((a, i) => ({ rank: i + 1, title: a.title, owner: a.owner, severity: a.severity, status: a.status, artefact: a.artefact.kind, total: a.rubric.total, stake_usd: a.money_at_stake && a.money_at_stake.usd, why: a.why })), null, 'offers-plan.csv') })],
      foot: el('div', { class: 'row' }, UI.rubricLegend(), el('span', { class: 'micro faint', text: 'Ranking: critical first by stake, then rubric total, severity, stake. "Not now" snoozes 14 days.' })),
      empty: 'No open offer or price move for this window.',
    }));
    const cw = document.getElementById('connect-wrap');
    cw.hidden = !con.length;
    if (con.length) mount('#connect', el('div', { class: 'card flat connect' },
      el('div', { class: 'sec-head' }, el('h2', { text: 'Connect first: ' + con.length + ' rules wait on a source' }),
        el('span', { class: 'sub', text: 'Each is a person task in Setup, read-only keys only. They never crowd out work that can start today.' })),
      el('div', { class: 'grid' }, con.map((a) => UI.actionCard(a, { compact: true, screen: SLUG })))));
  }

  // ---------- 2. what is wrong, ranked ----------
  function evidenceText(f) {
    return (f.evidence || []).slice(0, 4).map((e) => pretty(e.metric) + ' ' + fmtVal(e.value, e.unit) +
      (e.baseline != null ? ' vs ' + pretty(e.baseline_kind || 'baseline') + ' ' + fmtVal(e.baseline, e.unit) : '') + ' (' + e.window + ')').join('; ');
  }
  function fmtVal(v, unit) {
    if (v == null) return NA;
    if (unit === 'usd' || unit === 'usd_per_order') return fmt.money(v);
    if (unit === 'ratio') return pct(v);
    return fmt.num(v);
  }
  function wrong(d) {
    const fs = d.findings.filter((f) => f.status !== 'resolved');
    const rows = fs.map((f) => ({ f, rule: f.rule_id, what: f.entity.label, sentence: f.sentence, evidence: evidenceText(f) || 'no evidence rows: ' + (f.money_reason || NA), confidence: f.confidence, stake: f.money_at_stake ? f.money_at_stake.usd : null }));
    mount('#wrong', UI.sectionHead({ title: 'What is wrong, ranked', sub: fs.length + ' open findings from ' + d.rules.length + ' rules, severity first. Each links to the action that fixes it.' }),
      UI.verdictTable({
        columns: [{ key: 'what', label: 'Where' }, { key: 'sentence', label: 'Finding' }, { key: 'evidence', label: 'Evidence, window' }, { key: 'stake', label: 'Stake', unit: '$' }, { key: 'confidence', label: 'Conf.', format: (v) => v == null ? NA : v.toFixed(1) }],
        rows, verdict: { at: 0, kind: (r) => r.f.status === 'unavailable' ? 'wait' : r.f.severity === 'critical' || r.f.severity === 'high' ? 'fix' : 'watch', text: (r) => r.f.status === 'unavailable' ? 'Connect' : r.f.severity, reason: (r) => r.f.rule_id },
        actions: { label: 'Open action', onClick: (r) => { const a = findAction(r.f.id); if (a) openAction(a); } },
        sort: false,
      }));
  }

  // ---------- 3 and 4. actions ----------
  function actionsList(d) {
    const open = d.plan.filter((a) => a.status !== 'unavailable');
    mount('#actions', UI.sectionHead({ title: 'Actions: how each move gets done', sub: 'Owner, steps with who does each, the artefact it produces, the win and stop rules, the check date.' }),
      el('div', { class: 'grid' }, open.map((a, i) => UI.actionCard(a, { expanded: i === 0, screen: SLUG }))));
  }

  // ---------- 5. the desk ----------
  function stackBlock(rows) {
    return section('desk-stack', { title: 'What does a shopper get from us today?', sub: 'The offer stack from the brand brain, in the order a shopper meets it. Each line keeps its source and the day it was seen.' },
      el('div', { class: 'card tight' }, UI.table({
        columns: [
          { key: 'item', label: 'Offer' },
          { key: 'text', label: 'What it is', format: (v, r) => v || r.unavailable_reason },
          { key: 'source', label: 'Source', format: (v, r) => v ? (SOURCE[v] || v) + (r.ref ? ', ' + r.ref.replace(/^https?:\/\//, '').split('?')[0] : '') : NA },
          { key: 'date', label: 'Seen', format: (v) => v ? fmt.date(v) : NA },
          { key: 'tier', label: 'Tier', format: (v) => pretty(v) || NA },
        ], rows, sort: false })));
  }

  function thresholdBlock(th) {
    const a = ACTIONS.find((x) => x.rule_id === 'OFFER-R01');
    const head = { title: 'Does the free shipping line pay for itself?', sub: 'Break-even = AOV + average label / gross margin. A line that works has more orders in the $' + (th.band || 10) + ' just over it than just under it.' };
    if (th.unavailable) return section('desk-threshold', head, UI.emptyState({ screen: SLUG, title: 'Threshold economics unavailable', text: th.reason, missing: [th.fix] }));
    const inp = th.break_even_inputs || {};
    const bins = th.bins || [];
    const i0 = bins.findIndex((g) => g.from === th.shade[0]);
    const dist = Charts.bar({
      labels: bins.map((g) => '$' + g.from), stacked: true, unit: '%', shade: i0 >= 0 ? [i0, i0 + Math.round((th.shade[1] - th.shade[0]) / 5) - 1] : null,
      series: [
        { name: 'Pays shipping', values: bins.map((g) => g.orders ? g.share * g.paid_shipping_orders / g.orders : null) },
        { name: 'Ships free', values: bins.map((g) => g.orders ? g.share * (1 - g.paid_shipping_orders / g.orders) : null) },
      ],
      maxLabels: 10, title: (th.fixture ? 'Fixture: ' : '') + 'share of orders by order value, $5 bins' + (th.fixture ? ' (shape only, not brand data)' : ', ' + th.window.label),
      note: th.fixture ? 'Order values are ' + NA + ': ' + th.distribution_unavailable + '. A labelled fixture is drawn so the layout can be checked. Shaded: the $' + th.band + ' just under the line.'
        : 'Shaded: the $' + th.band + ' just under the line. Order value is subtotal minus discounts, before tax and shipping. ' + fmt.int(th.orders_sample) + ' order rows.',
    });
    const trend = Charts.step({ labels: th.trend.map((r) => r.month.slice(2)), unit: '$',
      series: [{ name: 'Break-even', values: th.trend.map((r) => r.break_even) }, { name: 'Free shipping line', values: th.trend.map((r) => r.threshold) }],
      title: 'Break-even by month against the line', note: '28-day AOV at each month end, label in force that day, target gross margin. The gap is label money on every order in between.', maxLabels: 6 });
    const facts = [
      ['Line', fmt.money(th.threshold) + ' (' + (SOURCE[(th.threshold_source || {}).type] || 'brain') + ', ' + ((th.threshold_source || {}).captured_at || 'undated') + '), ' + pct(th.above_aov, 0) + ' above AOV'],
      ['Break-even', fmt.money(th.break_even) + ' = AOV ' + fmt.money(inp.aov) + ' + label ' + fmt.money(inp.label) + ' / margin ' + pct(inp.gross_margin, 0)],
      ['Gap', th.gap == null ? NA : fmt.money(th.gap) + (th.gap > 0 ? ' under break-even on every free order in between' : ' over break-even')],
      ['Shipping under the line', th.shipping_listed == null ? NA : fmt.money(th.shipping_listed) + ' listed rate'],
      ['Just under / just over', th.share_just_under == null ? NA + ' until order rows connect' : pct(th.share_just_under) + ' / ' + pct(th.share_just_over)],
    ];
    const scen = UI.verdictTable({
      columns: [
        { key: 'threshold', label: 'Line', format: (v) => fmt.money(v, null, 0) },
        { key: 'be', label: 'Covers break-even', format: (v, r) => r.covers_break_even ? 'yes' : 'no' },
        { key: 'band_orders_28d', label: 'Orders in band, 28 days', format: (v, r) => r.current ? '' : v == null ? NA : fmt.int(v) },
        { key: 'contribution_free', label: 'Contribution, band order', format: (v, r) => r.current ? '' : v == null ? NA : fmt.money(v) },
        { key: 'text', label: 'What must be true' },
      ],
      rows: th.scenarios.map((r) => Object.assign({ be: '' }, r)),
      verdict: { at: 1, kind: (r) => r.current ? 'keep' : r.kind === 'raise' && r.covers_break_even ? 'new' : r.kind === 'raise' ? 'watch' : 'wait',
        text: (r) => r.current ? 'Today' : r.kind === 'raise' && r.covers_break_even ? 'Test' : r.kind === 'raise' ? 'Partial' : 'Needs lift', reason: (r) => r.text },
      actions: { label: (r) => r.kind === 'raise' && r.covers_break_even && a ? 'Open test brief' : 'Copy', onClick: (r) => { if (r.kind === 'raise' && r.covers_break_even && a) openAction(a); else UI.copy('Free shipping at $' + r.threshold + ': ' + r.text); } },
      sort: false,
    });
    const line = th.suggested ? 'The line sits ' + fmt.money(th.gap) + ' under break-even. Test $' + th.suggested + ' against ' + fmt.money(th.threshold) + '.' : 'The line sits at or over break-even. Keep it; watch the orders just under it.';
    return section('desk-threshold', head,
      el('div', { class: 'grid two' }, el('div', { class: 'card' }, dist), el('div', { class: 'card' }, trend, kv(facts))),
      el('div', { class: 'card tight' }, el('h4', { text: 'What would a different line need to pay?' }), el('p', { class: 'micro faint', text: th.scenario_rule }), scen),
      actionLine(line, a));
  }

  function discountBlock(d) {
    const c = d.chart, b = d.bfcm || {}, cr = d.creep || {};
    const head = { title: 'Are we training buyers to wait for a discount?', sub: cr.rule || '' };
    const parts = [];
    if (c.unavailable) parts.push(UI.emptyState({ screen: SLUG, title: 'No monthly sales', text: c.reason, missing: [c.fix] }));
    else {
      const note = c.partial.length ? c.partial.join(', ') + ' is a partial month. ' : '';
      parts.push(Charts.line({ labels: c.labels.map((m) => m.slice(2)), series: [{ name: 'Discount share of gross', values: c.discount_share }], unit: '%',
        title: 'Discounts as a share of gross sales, ' + c.window, note: note + 'Discounts over gross sales, all channels.', maxLabels: 8 }));
    }
    parts.push(kv([
      ['Creep rule', cr.sentence || NA],
      ['Last BFCM', b.unavailable ? NA + ': ' + b.reason : pct(b.depth) + ' of gross from ' + fmt.date(b.start) + ' to ' + fmt.date(b.end) + ', against ' + pct(b.baseline) + ' in the 28 days before (' + (b.points >= 0 ? '+' : '') + b.points.toFixed(1) + ' points, ' + fmt.int(b.orders) + ' orders).'],
    ]));
    return section('desk-discount', head, el('div', { class: 'card' }, ...parts),
      actionLine(cr.severity === 'high' ? 'Discount share is creeping. Cap code stacking and move the next promo to a gift.' : 'No creep this quarter. Hold the discount calendar as it is.', null));
  }

  function ladderBlock(l) {
    const head = { title: 'Does every pack size earn its place?', sub: 'Price per pair after discounts, 12 full months. A rung that saves the shopper nothing per pair gives no reason to trade up.' };
    if (l.unavailable) return section('desk-ladder', head, UI.emptyState({ screen: SLUG, title: 'No product sales', text: l.reason, missing: [l.fix] }));
    const rung = (v, r) => r.pack === 1 ? 'base' : v == null ? 'no single' : fmt.unit(v, '%');
    return section('desk-ladder', head, el('div', { class: 'card tight' },
      el('p', { class: 'micro faint', text: l.months + '. ' + l.basis + '.' }),
      UI.table({ columns: [
        { key: 'sku', label: 'SKU' },
        { key: 'category', label: 'Category' },
        { key: 'pack', label: 'Pack', unit: 'n' },
        { key: 'packs', label: 'Packs sold', unit: 'n' },
        { key: 'revenue', label: 'Revenue', unit: '$' },
        { key: 'price_per_item', label: 'Paid per pair', unit: '$' },
        { key: 'drop_vs_prev_rung', label: 'Drop vs rung below', unit: '%', format: (v, r) => rung(v, r) },
        { key: 'drop_vs_single', label: 'Drop vs single', unit: '%', format: (v, r) => rung(v, r) },
      ], rows: l.rows, sort: false, maxRows: 40 })));
  }

  function returnsChart(r) {
    if (!r || !r.groups || !r.groups.length) return el('p', { class: 'muted small', text: 'Returns by reason ' + NA + '.' });
    const rows = r.groups.slice().sort((a, b) => b.per_1000 - a.per_1000);
    return Charts.bar({ labels: rows.map((g) => g.reason), series: [{ name: 'Returns per 1,000 orders', values: rows.map((g) => g.per_1000) }], values: true,
      title: r.fixture ? 'Fixture: returns per 1,000 orders by reason (shape only, not brand data)' : 'Returns per 1,000 orders by reason, ' + r.window.label,
      note: r.fixture ? 'Returns by reason are ' + NA + ': ' + r.reason + '. The bars are a labelled fixture so the layout can be checked. The action reads the real metric once order rows connect.' : 'Returns opened in the window over paid orders placed in it. Carrier returns left out.' });
  }

  function objectionBlock(rows, returns) {
    const head = { title: 'Which deal-breaker doubt gets which offer?', sub: 'The top rung of each objection ladder in the brain. A rung with no proof gets an offer, a guarantee line or proof on the page, priced from finance inputs.' };
    const findA = (r) => ACTIONS.find((x) => x.rule_id === 'OFFER-R04' && x.entity && x.entity.id === r.theme_key + '.deal_breaker');
    const table = UI.verdictTable({
      columns: [
        { key: 'theme', label: 'Objection' },
        { key: 'doubt', label: 'Deal-breaker doubt' },
        { key: 'one_star', label: 'One-star', unit: 'n' },
        { key: 'offer', label: 'Offer or proof to launch' },
        { key: 'covered', label: 'Already in policy', format: (v, r) => r.covered_by.length ? r.covered_by.map((c) => c.id.split('.').slice(1).join('.')).join(', ') : 'nothing' },
        { key: 'cost_per_claim', label: 'Cost per claim', format: (v, r) => r.claim === 'none' ? 'none' : v == null ? NA : fmt.money(v) },
        { key: 'cost_per_1000_orders', label: 'Per 1,000 orders', format: (v, r) => r.claim === 'none' ? 'none' : v == null ? 'rate ' + NA : fmt.money(v) },
        { key: 'ret', label: 'Returns per 1,000', format: (v, r) => r.returns.per_1000 != null ? r.returns.per_1000.toFixed(1) : (r.returns.reasons.length ? NA : 'no reason maps') },
      ],
      rows: rows.map((r) => Object.assign({ covered: '', ret: '' }, r)),
      verdict: { at: 1, kind: (r) => r.answered ? 'keep' : 'fix', text: (r) => r.answered ? 'Answered' : 'No proof', reason: (r) => 'rung ' + r.rung },
      actions: { label: (r) => findA(r) ? 'Open action' : 'Copy spec', onClick: (r) => { const a = findA(r); if (a) openAction(a); else UI.copy(r.spec); } },
      sort: false,
    });
    const open = rows.filter((r) => !r.answered);
    const top = open.slice().sort((a, b) => b.one_star - a.one_star)[0];
    return section('desk-objections', head, el('div', { class: 'card tight' }, table),
      el('div', { class: 'grid two' }, el('div', { class: 'card' }, returnsChart(returns)),
        el('div', { class: 'card' }, el('h4', { text: top ? 'The spec for the biggest open doubt' : 'Every deal-breaker has proof' }),
          top ? el('pre', { class: 'spec', text: top.spec }) : null, top ? UI.copyButton({ label: 'Copy spec', text: () => top.spec }) : null)),
      actionLine(open.length + ' of ' + rows.length + ' deal-breaker doubts have no proof. Launch the offer for the biggest one first.', top ? findA(top) : null));
  }

  // ---------- 6. the audit ----------
  function auditBlock(d) {
    mount('#audit', UI.sectionHead({ title: 'The audit', sub: d.findings.length + ' findings from ' + d.rules.length + ' rules. Every rule reads brand records and tables; none calls a model.',
      tools: [el('button', { class: 'btn sm', type: 'button', text: 'Export findings CSV', onclick: () => UI.csv(d.findings.map((f) => ({ id: f.id, rule: f.rule_id, severity: f.severity, status: f.status, sentence: f.sentence, stake_usd: f.money_at_stake && f.money_at_stake.usd, money_reason: f.money_reason || '' })), null, 'offers-findings.csv') })] }),
      el('div', { class: 'card tight' }, UI.table({ columns: [
        { key: 'rule_id', label: 'Rule' }, { key: 'name', label: 'What it checks' }, { key: 'entity_type', label: 'On' },
        { key: 'inputs', label: 'Reads', format: (v) => (v || []).join(', ') }, { key: 'capability', label: 'Capability' },
        { key: 'fired', label: 'Fired', unit: 'n' },
      ], rows: d.rules.map((r) => Object.assign({}, r, { fired: d.findings.filter((f) => f.rule_id === r.rule_id).length })), sort: false })));
  }

  function render(d) {
    ACTIONS = d.plan || [];
    badge(d.brand || {});
    plan(d);
    wrong(d);
    actionsList(d);
    mount('#desk', el('div', { class: 'desk-kicker' }, el('h3', { text: 'The desk' })),
      stackBlock(d.stack || []), thresholdBlock(d.threshold), discountBlock(d), ladderBlock(d.ladder), objectionBlock(d.objections || [], d.returns));
    auditBlock(d);
  }

  UI.api('/api/' + SLUG + '/overview?brand=' + encodeURIComponent(brand))
    .then(render)
    .catch((e) => mount('#plan', UI.emptyState({ screen: SLUG, title: 'Could not load', text: String(e.message || e) })));
})();
