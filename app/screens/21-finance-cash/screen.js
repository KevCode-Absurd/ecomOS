/* Finance and cash, round 0. Reads /api/21-finance-cash/overview and composes kit components.
   No numbers are computed here; the server sends every value, rule and sentence. */
(function () {
  'use strict';
  const SLUG = '21-finance-cash';
  const { el, fmt } = UI;
  const brand = new URLSearchParams(location.search).get('brand') || 'bombas';
  const AUTONOMY_KIT = { agent_does: 'agent', founder_gate: 'founder_gate', human_assist: 'human_assist', agent: 'agent' };

  function section(title, ...children) {
    return el('section', { class: 'section' }, el('h3', { text: title }), ...children);
  }

  function simBanner(b) {
    const name = b.name || b.brand || 'This brand';
    if (!b.simulated) return el('div', { class: 'sim', role: 'note' }, el('b', { text: name }), ' live data. Read-only.');
    return el('div', { class: 'sim', role: 'note' }, el('b', { text: name }),
      ': simulated data. Costs, fees, cash and every sales number are generated. Nothing here is a ' + name + ' result.');
  }

  function tile(t) {
    const src = (t.sources || []).map((s) => s.table).join(', ');
    return UI.tile(Object.assign({}, t, { freshness: t.freshness ? fmt.date(t.freshness) + (src ? ' from ' + src : '') : null }));
  }

  function pct(v) { return v == null ? 'unavailable' : fmt.pct(v); }

  function kv(pairs) {
    return el('dl', { class: 'kv' }, pairs.flatMap(([k, v]) => [el('dt', { text: k }), el('dd', { text: v })]));
  }

  function chart(c) {
    if (c.unavailable) return UI.emptyState({ screen: SLUG, title: 'No monthly sales', text: c.reason, missing: [c.fix] });
    const labels = c.labels.map((m) => m.slice(2));
    const notes = [];
    if (c.unavailable_months.length) notes.push(c.unavailable_months[0] + ' to ' + c.unavailable_months[c.unavailable_months.length - 1] + ' read unavailable: no cost rows in force.');
    if (c.partial.length) notes.push(c.partial.join(', ') + ' is a partial month.');
    return el('div', { class: 'card' }, Charts.line({
      labels, unit: '%', maxLabels: 8, title: 'Margin ladder by month, ' + c.window,
      series: [
        { name: 'Gross margin', values: c.gross_margin },
        { name: 'Contribution after marketing', values: c.cm3_rate, color: 'var(--s2)' },
        { name: 'Paid media share', values: c.paid_share, color: 'var(--s3)' },
      ],
      note: notes.join(' ') + ' ' + c.basis,
    }));
  }

  function ladder(l) {
    if (l.unavailable) return UI.emptyState({ screen: SLUG, title: 'P&L ladder unavailable', text: l.reason });
    return el('div', { class: 'ladder' },
      el('p', { class: 'th', text: 'Online store, ' + l.label + '. ' + l.basis }),
      UI.table({ columns: [
        { key: 'line', label: 'Line' },
        { key: 'usd', label: 'Dollars', unit: '$' },
        { key: 'share', label: 'Share of net revenue', unit: '%' },
        { key: 'note', label: 'What it covers', format: (v) => v || '' },
      ], rows: l.rows, sort: false }));
  }

  function skus(s) {
    if (s.unavailable) return UI.emptyState({ screen: SLUG, title: 'Margin by SKU unavailable', text: s.reason });
    return el('div', null,
      el('p', { class: 'th', text: s.label + '. Per unit ops ' + fmt.money(s.per_unit_ops) + ', paid media per unit ' +
        fmt.money(s.paid_per_unit) + ', revenue costs ' + pct(s.revenue_cost_rate) + '. ' + s.basis }),
      el('div', { class: 'wrap' }, UI.table({ columns: [
        { key: 'sku', label: 'SKU' },
        { key: 'units', label: 'Units', unit: 'n' },
        { key: 'net_per_unit', label: 'Net per unit', unit: '$' },
        { key: 'unit_cost', label: 'Landed cost', unit: '$' },
        { key: 'gross_margin', label: 'Gross margin', unit: '%' },
        { key: 'cm3_per_unit', label: 'CM3 per unit', unit: '$' },
        { key: 'cm3', label: 'CM3', unit: '$' },
      ], rows: s.rows, sort: false, maxRows: 30 })));
  }

  function channels(rows) {
    return UI.table({ columns: [
      { key: 'line', label: 'Sales line' },
      { key: 'net_revenue', label: 'Net revenue', unit: '$' },
      { key: 'cm2_rate', label: 'CM2', unit: '%' },
      { key: 'cm3_rate', label: 'CM3', unit: '%' },
      { key: 'note', label: 'Note', format: (v) => v || '' },
    ], rows, sort: false });
  }

  function cash(c) {
    if (c.unavailable) return UI.emptyState({ screen: SLUG, title: 'No cash inputs', text: c.reason, missing: [c.fix] });
    const op = c.operating_costs || {};
    return el('div', { class: 'card' }, kv([
      ['Cash on hand', c.cash_balance == null ? 'unavailable' : fmt.money(c.cash_balance) + ' as of ' + fmt.date(c.cash_as_of)],
      ['Undrawn credit', c.credit_line_available == null ? 'unavailable' : fmt.money(c.credit_line_available)],
      ['Operating costs', op.total == null ? 'unavailable' : fmt.money(op.total) + ' in ' + op.month + ' (people, rent, apps, agency, storage)'],
      ['Runway', c.runway],
    ]));
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
      f.money_at_stake ? el('div', { class: 'money', text: fmt.money(f.money_at_stake.usd) + ' at stake = ' +
        f.money_at_stake.formula + ' (' + Object.entries(f.money_at_stake.inputs).map(([k, v]) => k + ' ' + v).join(', ') + ')' })
        : el('div', { class: 'money', text: 'Money at stake unavailable: ' + (f.money_reason || 'no baseline') }),
      f.unavailable ? el('div', { class: 'money', text: 'Fix: ' + f.unavailable.fix }) : null)));
  }

  function render(d) {
    const b = d.brand || {};
    const t = d.tiles || {};
    UI.mount('#app',
      el('header', { class: 'screen-head' }, el('h1', { text: 'Finance and cash' }),
        el('p', { text: 'Through ' + fmt.date(b.as_of) + '. What each order, SKU and sales line keeps after every real cost.' })),
      simBanner(b),
      section('Margin', el('div', { class: 'grid tiles three' }, tile(t.gross), tile(t.contribution), tile(t.mer))),
      section('What the rules say', el('div', { class: 'grid two' }, (d.insights || []).map((i) =>
        UI.insight({ sentence: i.sentence, rule: i.rule, severity: i.severity, capability: i.capability,
          autonomy: AUTONOMY_KIT[i.autonomy] || i.autonomy, stub: i.stub, screen: SLUG })))),
      section('Margin ladder by month', chart(d.chart)),
      section('P&L ladder', ladder(d.ladder)),
      section('Sales lines', channels(d.channels || [])),
      section('Margin by SKU, worst first', skus(d.skus)),
      section('Cash', cash(d.cash)),
      section('Audit findings', findingsList(d.findings || [])));
  }

  UI.api('/api/' + SLUG + '/overview?brand=' + encodeURIComponent(brand))
    .then(render)
    .catch((e) => UI.mount('#app', el('header', { class: 'screen-head' }, el('h1', { text: 'Finance and cash' })),
      UI.emptyState({ screen: SLUG, title: 'Could not load', text: String(e.message || e) })));
})();
