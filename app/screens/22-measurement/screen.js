/* Measurement and data health, round 0. Reads /api/22-measurement/overview and composes kit components.
   No numbers are computed here; the server sends every value, rule and sentence. */
(function () {
  'use strict';
  const SLUG = '22-measurement';
  const { el, fmt } = UI;
  const brand = new URLSearchParams(location.search).get('brand') || 'bombas';
  const AUTONOMY_KIT = { agent_does: 'agent', founder_gate: 'founder_gate', human_assist: 'human_assist', agent: 'agent' };
  const TRUST_CHIP = { pass: 'good', warn: 'warn', fail: 'bad' };

  function section(title, ...children) {
    return el('section', { class: 'section' }, el('h3', { text: title }), ...children);
  }

  function simBanner(b) {
    const name = b.name || b.brand || 'This brand';
    if (!b.simulated) return el('div', { class: 'sim', role: 'note' }, el('b', { text: name }), ' live data. Read-only.');
    return el('div', { class: 'sim', role: 'note' }, el('b', { text: name }),
      ': simulated data. Every number on this page is generated from a public profile. Nothing here is a ' + name + ' result.');
  }

  function tile(t, extra) {
    const src = (t.sources || []).map((s) => s.table).join(', ');
    return UI.tile(Object.assign({}, t, { freshness: t.freshness ? fmt.date(t.freshness) + (src ? ' from ' + src : '') : null },
      extra || {}));
  }

  function reconciliation(r) {
    const table = UI.table({
      columns: [
        { key: 'source', label: 'Source' },
        { key: 'basis', label: 'Counts' },
        { key: 'orders', label: 'Orders claimed', unit: 'n' },
        { key: 'store_orders', label: 'Store orders', unit: 'n' },
        { key: 'gap', label: 'Gap', unit: '%' },
        { key: 'value', label: 'Value claimed', unit: '$' },
        { key: 'store_value', label: 'Store value', unit: '$' },
        { key: 'spend', label: 'Spend', unit: '$' },
        { key: 'roas', label: 'Platform ROAS', unit: 'x' },
      ],
      rows: r.rows, sort: false });
    const t = r.total;
    const note = t ? 'Meta and Google together: ' + fmt.num(t.claimed_orders) + ' orders and ' + fmt.money(t.claimed_value) +
      ' claimed on ' + fmt.money(t.spend) + ' spend, a period ROAS of ' + fmt.ratio(t.period_roas) +
      ' (total value over total spend). The store took ' + fmt.num(t.store_orders) + ' orders worth ' + fmt.money(t.store_net) + '.'
      : 'Totals unavailable: an ad platform is not connected.';
    return el('div', { class: 'card' },
      el('p', { class: 'th', text: 'Store orders for GA4 are all web orders. For Meta and Google they are store orders whose last click was that channel. GA4 value is as GA4 reports it; store value is net of discounts, before tax and shipping.' }),
      el('div', { class: 'table-wrap' }, table), el('p', { class: 'th', text: note }),
      UI.decisionRow({ capability: 'MONEY-C24', autonomy: 'agent', screen: SLUG,
        stub: 'Reconcile GA4, Meta and Google order counts against the store each day and flag any gap over 3 percent. Nothing changes in any account; your choice is logged.' }));
  }

  function trust(t) {
    return el('div', { class: 'card' },
      el('p', { text: 'Last full day, ' + fmt.date(t.day) + ': ' + t.status + '.' }),
      el('div', { class: 'trust' }, t.checks.map((c) => el('span', { class: 'chip ' + (TRUST_CHIP[c.status] || ''),
        title: c.detail, text: c.status + ': ' + c.check + ' (' + c.detail + ')' }))));
  }

  function incrementality(rows) {
    return el('div', { class: 'card' },
      el('p', { class: 'th', text: 'Lift is what a channel adds that would not have happened anyway. It reads unavailable until a test runs.' }),
      el('div', { class: 'table-wrap' }, UI.table({
        columns: [
          { key: 'platform', label: 'Platform' },
          { key: 'spend', label: 'Spend 28d', unit: '$' },
          { key: 'share', label: 'Share of paid', unit: '%' },
          { key: 'lift', label: 'Lift', unit: '%' },
          { key: 'test', label: 'Test to run', format: (v) => v },
        ], rows, sort: false })),
      UI.decisionRow({ capability: 'MONEY-C23', autonomy: 'agent', screen: SLUG,
        stub: 'Draft a holdout plan for the largest untested channel. No budget moves until you approve; your choice is logged.' }));
  }

  function chart(c) {
    if (c.unavailable) return UI.emptyState({ screen: SLUG, title: 'No store orders', text: c.reason, missing: [c.fix] });
    const labels = c.labels.map((d) => d.slice(5));
    return el('div', { class: 'card' },
      Charts.line({ labels, series: c.series, unit: 'n', title: 'Orders per day, ' + c.window + ': store against each platform',
        note: 'Store orders are the truth. ' + c.basis[0].toUpperCase() + c.basis.slice(1) + '.', maxLabels: 6 }));
  }

  function findingsList(fs) {
    if (!fs.length) return el('p', { text: 'No findings this run.' });
    return el('div', { class: 'card' }, fs.map((f) => el('div', { class: 'finding' },
      el('div', { class: 'tags' },
        el('span', { class: 'chip ' + (f.severity === 'critical' || f.severity === 'high' ? 'bad' : f.severity === 'medium' ? 'warn' : ''), text: f.severity }),
        el('span', { class: 'chip mono', text: f.rule_id }),
        el('span', { class: 'chip mono', text: f.capability.id }),
        f.status === 'unavailable' ? el('span', { class: 'chip', text: 'unavailable' }) : null,
        f.confidence < 0.3 && f.status !== 'unavailable' ? el('span', { class: 'chip', text: 'weak evidence' }) : null),
      el('div', { class: f.status === 'unavailable' ? 'unav' : null, text: f.sentence }),
      f.status === 'unavailable'
        ? el('div', { class: 'money', text: 'Needs ' + f.unavailable.inputs.join(', ') + '. ' + f.unavailable.fix })
        : f.money_at_stake
          ? el('div', { class: 'money', text: fmt.money(f.money_at_stake.usd) + ' at stake = ' + f.money_at_stake.formula +
            ' (' + Object.entries(f.money_at_stake.inputs).map(([k, v]) => k + ' ' + v).join(', ') + ')' })
          : el('div', { class: 'money', text: 'Money at stake unavailable: ' + (f.money_reason || 'no baseline') }))));
  }

  function render(d) {
    const b = d.brand || {};
    const t = d.tiles || {};
    const open = (d.findings || []).filter((f) => f.status === 'open');
    const unav = (d.findings || []).filter((f) => f.status === 'unavailable');
    UI.mount('#app',
      el('header', { class: 'screen-head' }, el('h1', { text: 'Measurement and data health' }),
        el('p', { text: 'Through ' + fmt.date(b.as_of) + '. Which numbers to trust: each platform against the store, the store as the truth.' })),
      simBanner(b),
      section('Can I trust the numbers',
        el('div', { class: 'grid tiles three' }, tile(t.mer, { delta_label: 'vs prior 28d' }),
          tile(t.overlap, { delta_label: 'vs prior 28d' }), tile(t.capture, { delta_label: 'vs prior 28d' }))),
      section('What the rules say', el('div', { class: 'grid two' }, (d.insights || []).map((i) =>
        UI.insight({ sentence: i.sentence, rule: i.rule, severity: i.severity, capability: i.capability,
          autonomy: AUTONOMY_KIT[i.autonomy] || i.autonomy, screen: SLUG })))),
      section('Orders: store against platforms', chart(d.chart)),
      section('Reconciliation, last 28 days', reconciliation(d.reconciliation)),
      section('Daily trust check', trust(d.trust)),
      section('Incrementality', incrementality(d.incrementality || [])),
      section('Audit findings (' + open.length + ' open, ' + unav.length + ' waiting on data)', findingsList(d.findings || [])));
  }

  UI.api('/api/' + SLUG + '/overview?brand=' + encodeURIComponent(brand))
    .then(render)
    .catch((e) => UI.mount('#app', el('header', { class: 'screen-head' }, el('h1', { text: 'Measurement and data health' })),
      UI.emptyState({ screen: SLUG, title: 'Could not load', text: String(e.message || e) })));
})();
