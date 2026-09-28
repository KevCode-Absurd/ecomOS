/* Offers and pricing, round 0. Reads /api/04-offers-pricing/overview and composes kit components.
   No numbers are computed here; the server sends every value, rule and sentence. */
(function () {
  'use strict';
  const SLUG = '04-offers-pricing';
  const { el, fmt } = UI;
  const brand = new URLSearchParams(location.search).get('brand') || 'bombas';
  const AUTONOMY_KIT = { agent_does: 'agent', founder_gate: 'founder_gate', human_assist: 'human_assist', agent: 'agent' };
  const SOURCE = { site: 'Site', ad_library: 'Meta Ad Library', press: 'Press', review: 'Reviews', interview: 'Interview' };

  function section(title, ...children) {
    return el('section', { class: 'section' }, el('h3', { text: title }), ...children);
  }

  function simBanner(b) {
    const name = b.name || b.brand || 'This brand';
    if (!b.simulated) return el('div', { class: 'sim', role: 'note' }, el('b', { text: name }), ' live data. Read-only.');
    return el('div', { class: 'sim', role: 'note' }, el('b', { text: name }),
      ': simulated data. Offers and reviews come from public pages; every sales number is generated. Nothing here is a ' + name + ' result.');
  }

  function tile(t) {
    const src = (t.sources || []).map((s) => s.table).join(', ');
    return UI.tile(Object.assign({}, t, { freshness: t.freshness ? fmt.date(t.freshness) + (src ? ' from ' + src : '') : null }));
  }

  function pct(v, d) { return v == null ? 'unavailable' : (v * 100).toFixed(d == null ? 1 : d) + ' percent'; }

  function kv(pairs) {
    return el('dl', { class: 'kv' }, pairs.flatMap(([k, v]) => [el('dt', { text: k }), el('dd', { text: v })]));
  }

  function stack(rows) {
    return UI.table({
      columns: [
        { key: 'item', label: 'Offer' },
        { key: 'text', label: 'What it is', format: (v, r) => v || r.unavailable_reason },
        { key: 'source', label: 'Source', format: (v, r) => v ? (SOURCE[v] || v) + (r.ref ? ', ' + r.ref.replace(/^https?:\/\//, '').split('?')[0] : '') : 'unavailable' },
        { key: 'date', label: 'Seen' },
        { key: 'tier', label: 'Tier' },
      ], rows, sort: false });
  }

  function threshold(th) {
    if (th.unavailable) return UI.emptyState({ screen: SLUG, title: 'Threshold economics unavailable', text: th.reason, missing: [th.fix] });
    const bins = th.bins;
    const chart = Charts.bar({
      labels: bins.map((g) => '$' + g.from), stacked: true, unit: '%',
      series: [
        { name: 'Pays shipping', values: bins.map((g) => g.orders ? g.share * g.paid_shipping_orders / g.orders : null) },
        { name: 'Ships free', values: bins.map((g) => g.orders ? g.share * (1 - g.paid_shipping_orders / g.orders) : null), color: 'var(--s2)' },
      ],
      maxLabels: 10, title: 'Share of orders by order value, $5 bins, ' + th.window.label,
      note: 'Order value is ' + th.basis.replace('paid orders; order value is ', '') + '. ' + fmt.int(th.orders_sample) + ' simulated order rows.',
    });
    const inp = th.break_even_inputs;
    const facts = [
      ['Threshold', fmt.money(th.threshold) + ' (' + (SOURCE[(th.threshold_source || {}).type] || 'brain') + ', ' + ((th.threshold_source || {}).captured_at || 'undated') + ')'],
      ['Just under ($' + th.band + ')', pct(th.share_just_under) + ' of orders'],
      ['Just over ($' + th.band + ')', pct(th.share_just_over) + ' of orders'],
      ['Ships free', pct(th.share_ship_free) + ' of orders'],
      ['Break-even', fmt.money(th.break_even) + ' = AOV ' + fmt.money(inp.aov) + ' + label ' + fmt.money(inp.label) + ' / margin ' + pct(inp.gross_margin, 0)],
      ['Margin used', th.margin_basis],
      ['Shipping charged', (th.shipping_paid_avg != null ? fmt.money(th.shipping_paid_avg) + ' average in simulated orders' : 'unavailable') +
        (th.shipping_listed != null ? '; the site lists ' + fmt.money(th.shipping_listed) : '')],
    ];
    if (th.suggested) facts.push(['Rule suggests', '$' + th.suggested + '. ' + pct(th.suggested_share_below_now, 0) + ' of orders sit below it today.']);
    return el('div', { class: 'card' }, chart, kv(facts), el('p', { class: 'th', text: 'Rule: ' + th.rule }));
  }

  function discount(d) {
    const parts = [];
    const b = d.bfcm || {};
    parts.push(el('p', { class: 'th', text: b.unavailable ? 'BFCM depth unavailable: ' + b.reason + '.' :
      'BFCM depth: discounts were ' + pct(b.depth) + ' of gross from ' + fmt.date(b.start) + ' to ' + fmt.date(b.end) +
      ', against ' + pct(b.baseline) + ' in the 28 days before (' + (b.points >= 0 ? '+' : '') + b.points.toFixed(1) + ' points, ' + fmt.int(b.orders) + ' orders).' }));
    const c = d.chart;
    if (c.unavailable) parts.push(UI.emptyState({ screen: SLUG, title: 'No monthly sales', text: c.reason, missing: [c.fix] }));
    else {
      const labels = c.labels.map((m) => m.slice(2));
      const note = c.partial.length ? c.partial.join(', ') + ' is a partial month. ' : '';
      parts.push(el('div', { class: 'card chart-pair' },
        Charts.line({ labels, series: [{ name: 'AOV', values: c.aov }], unit: '$', title: 'AOV by month, ' + c.window, note: note + 'Net sales over orders.', maxLabels: 6 }),
        Charts.line({ labels, series: [{ name: 'Discount share', values: c.discount_share, color: 'var(--s2)' }], unit: '%',
          title: 'Discounts as a share of gross, ' + c.window, note: note + 'Discounts over gross sales.', maxLabels: 6 })));
    }
    return el('div', null, ...parts);
  }

  function rung(v, r) { return r.pack === 1 ? 'base' : v == null ? 'no single' : fmt.unit(v, '%'); }

  function ladder(l) {
    if (l.unavailable) return UI.emptyState({ screen: SLUG, title: 'No product sales', text: l.reason, missing: [l.fix] });
    const sizes = UI.table({ columns: [
      { key: 'pack', label: 'Pack size', format: (v) => v == null ? 'unknown' : v === 1 ? 'single' : v + '-pack' },
      { key: 'packs', label: 'Packs sold', unit: 'n' },
      { key: 'revenue', label: 'Revenue', unit: '$' },
      { key: 'revenue_share', label: 'Share', unit: '%' },
    ], rows: l.by_size, sort: false });
    const rows = UI.table({ columns: [
      { key: 'sku', label: 'SKU' },
      { key: 'title', label: 'Product', format: (v, r) => v || r.category },
      { key: 'pack', label: 'Pack', unit: 'n' },
      { key: 'packs', label: 'Packs sold', unit: 'n' },
      { key: 'revenue', label: 'Revenue', unit: '$' },
      { key: 'price_per_item', label: 'Paid per pair', unit: '$' },
      { key: 'list_per_item', label: 'List per pair', unit: '$' },
      { key: 'drop_vs_prev_rung', label: 'Drop vs rung below', unit: '%', format: (v, r) => rung(v, r) },
      { key: 'drop_vs_single', label: 'Drop vs single', unit: '%', format: (v, r) => rung(v, r) },
    ], rows: l.rows, sort: false, maxRows: 40 });
    return el('div', null,
      el('p', { class: 'th', text: l.months + '. ' + l.basis + '. Margin per rung is ' + l.margin + '.' }),
      sizes, el('p'), rows);
  }

  function guarantee(rows) {
    return el('div', null,
      el('p', { class: 'th', text: 'The top rung of each objection ladder is the deal-breaker. Rungs with no proof are the ones the offer or guarantee has to answer.' }),
      el('div', { class: 'wrap' }, UI.table({ columns: [
        { key: 'theme', label: 'Objection' },
        { key: 'doubt', label: 'Deal-breaker doubt' },
        { key: 'one_star', label: 'One-star', unit: 'n' },
        { key: 'answered', label: 'Answered', format: (v) => v ? 'yes' : 'no proof' },
        { key: 'proof', label: 'Proof on file' },
        { key: 'returns_per_1000', label: 'Returns per 1,000 orders', format: (v, r) => !r.return_reason ? 'no reason maps' :
          (v == null ? 'unavailable' : v.toFixed(1)) + ' for ' + r.return_reason + (r.median_per_1000 != null ? ', median ' + r.median_per_1000.toFixed(1) : '') },
      ], rows, sort: false })));
  }

  function findingsList(fs) {
    if (!fs.length) return el('p', { text: 'No findings this run.' });
    return el('div', { class: 'card' }, fs.map((f) => el('div', { class: 'finding' },
      el('div', { class: 'tags' },
        el('span', { class: 'chip ' + (f.severity === 'critical' || f.severity === 'high' ? 'bad' : 'warn'), text: f.severity }),
        el('span', { class: 'chip mono', text: f.rule_id }),
        el('span', { class: 'chip mono', text: f.capability.id }),
        f.status === 'unavailable' ? el('span', { class: 'chip', text: 'unavailable' }) : null,
        f.confidence < 0.3 && f.status !== 'unavailable' ? el('span', { class: 'chip', text: 'weak evidence' }) : null),
      el('div', { text: f.sentence }),
      f.money_at_stake ? el('div', { class: 'money', text: fmt.money(f.money_at_stake.usd) + (f.money_at_stake.floor ? ' at stake, at least, = ' : ' at stake = ') +
        f.money_at_stake.formula + ' (' + Object.entries(f.money_at_stake.inputs).map(([k, v]) => k + ' ' + v).join(', ') + ')' })
        : el('div', { class: 'money', text: 'Money at stake unavailable: ' + (f.money_reason || 'no baseline') }),
      f.unavailable ? el('div', { class: 'money', text: 'Fix: ' + f.unavailable.fix }) : null)));
  }

  function render(d) {
    const b = d.brand || {};
    const t = d.tiles || {};
    UI.mount('#app',
      el('header', { class: 'screen-head' }, el('h1', { text: 'Offers and pricing' }),
        el('p', { text: 'Through ' + fmt.date(b.as_of) + '. What the offer is, what it costs, and which buyer doubts it leaves open.' })),
      simBanner(b),
      section('Offer economics', el('div', { class: 'grid tiles three' }, tile(t.threshold), tile(t.discount), tile(t.multipack))),
      section('What the rules say', el('div', { class: 'grid two' }, (d.insights || []).map((i) =>
        UI.insight({ sentence: i.sentence, rule: i.rule, severity: i.severity, capability: i.capability,
          autonomy: AUTONOMY_KIT[i.autonomy] || i.autonomy, stub: i.stub, screen: SLUG })))),
      section('The offer stack today', el('p', { class: 'th', text: 'From the brand brain. Each line keeps its public source and the day it was seen.' }),
        el('div', { class: 'wrap' }, stack(d.stack || []))),
      section('Free shipping threshold', threshold(d.threshold)),
      section('Discount policy', discount(d)),
      section('Pack ladder', ladder(d.ladder)),
      section('Guarantee against objections', guarantee(d.guarantee || [])),
      section('Audit findings', findingsList(d.findings || [])));
  }

  UI.api('/api/' + SLUG + '/overview?brand=' + encodeURIComponent(brand))
    .then(render)
    .catch((e) => UI.mount('#app', el('header', { class: 'screen-head' }, el('h1', { text: 'Offers and pricing' })),
      UI.emptyState({ screen: SLUG, title: 'Could not load', text: String(e.message || e) })));
})();
