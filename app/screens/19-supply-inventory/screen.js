/* Supply and inventory, round 0. Reads /api/19-supply-inventory/overview and composes kit components.
   No numbers are computed here; the server sends every value, rule and sentence. */
(function () {
  'use strict';
  const SLUG = '19-supply-inventory';
  const { el, fmt } = UI;
  const brand = new URLSearchParams(location.search).get('brand') || 'bombas';
  const AUTONOMY_KIT = { agent_does: 'agent', founder_gate: 'founder_gate', human_assist: 'human_assist', agent: 'agent' };

  function section(title, ...children) {
    return el('section', { class: 'section' }, el('h3', { text: title }), ...children);
  }

  function simBanner(b, scale) {
    const name = b.name || b.brand || 'This brand';
    if (!b.simulated) return el('div', { class: 'sim', role: 'note' }, el('b', { text: name }), ' live data. Read-only.');
    return el('div', { class: 'sim', role: 'note' }, el('b', { text: name }),
      ': simulated data. Stock, POs, sales and landed costs are generated. Nothing here is a ' + name + ' result.' +
      (scale && scale !== 1 ? ' Units and dollars are scaled from a sample to the full order totals.' : ''));
  }

  function tile(t) {
    const src = (t.sources || []).map((s) => s.table).join(', ');
    return UI.tile(Object.assign({}, t, { freshness: t.freshness ? fmt.date(t.freshness) + (src ? ' from ' + src : '') : null }));
  }

  function chart(c) {
    if (c.unavailable) return UI.emptyState({ screen: SLUG, title: 'No stock data', text: c.reason, missing: [c.fix] });
    return el('div', { class: 'card' },
      Charts.bar({ labels: c.labels, unit: 'days', maxLabels: c.labels.length, title: 'Days of stock against days until stock lands, ' + c.labels.length + ' SKUs with the least cover',
        note: c.note + ' Where days of stock is the shorter bar, the SKU sells out before stock lands. Labels are SKU codes without the BMB and line prefix.',
        series: [{ name: 'Days of stock', values: c.cover }, { name: 'Days until stock lands', values: c.lands, color: 'var(--s3)' }] }));
  }

  function skuTable(rows) {
    if (!rows.length) return el('p', { text: 'No SKUs.' });
    return el('div', { class: 'table-wrap' }, UI.table({ columns: [
      { key: 'title', label: 'SKU', format: (v, r) => v + (r.hero ? ' (top 5)' : '') },
      { key: 'on_hand', label: 'On hand', unit: 'n' },
      { key: 'per_day', label: 'Sold a day', unit: 'n' },
      { key: 'cover_days', label: 'Days of stock', format: (v) => v == null ? 'unavailable' : v.toFixed(0) },
      { key: 'next_eta', label: 'Next PO lands', format: (v, r) => v ? fmt.date(v) : 'none open, lead ' + (r.lead_days == null ? 'unavailable' : r.lead_days.toFixed(0) + ' days') },
      { key: 'gap_days', label: 'Days sold out', format: (v) => v == null ? 'unavailable' : v ? v.toFixed(0) : 'none' },
      { key: 'on_order', label: 'On order', unit: 'n' },
      { key: 'reorder_point', label: 'Reorder point', unit: 'n' },
      { key: 'recommended_po', label: 'Order now', unit: 'n' },
      { key: 'landed_cost', label: 'Landed cost', unit: '$' },
    ], rows, sort: false }));
  }

  function findingsList(fs) {
    const open = fs.filter((f) => f.status !== 'unavailable');
    const missing = fs.filter((f) => f.status === 'unavailable');
    const list = open.length ? el('div', { class: 'card' }, open.map((f) => el('div', { class: 'finding' },
      el('div', { class: 'tags' },
        el('span', { class: 'chip ' + (f.severity === 'critical' || f.severity === 'high' ? 'bad' : 'warn'), text: f.severity }),
        el('span', { class: 'chip mono', text: f.rule_id }),
        el('span', { class: 'chip mono', text: f.capability.id }),
        f.confidence < 0.3 ? el('span', { class: 'chip', text: 'weak evidence' }) : null),
      el('div', { text: f.sentence }),
      f.money_at_stake ? el('div', { class: 'money', text: fmt.money(f.money_at_stake.usd) + ' at stake = ' + f.money_at_stake.formula + ' (' +
        Object.entries(f.money_at_stake.inputs).map(([k, v]) => k + ' ' + v).join(', ') + ')' })
        : el('div', { class: 'money', text: 'Money at stake unavailable: ' + (f.money_reason || 'no baseline') }),
      UI.decisionRow({ capability: f.capability.id, autonomy: AUTONOMY_KIT[f.capability.autonomy] || f.capability.autonomy, screen: SLUG }))))
      : el('p', { text: 'No open findings this run.' });
    const miss = missing.length ? el('div', { class: 'card' },
      el('p', { class: 'th', text: missing.length + ' rules cannot run yet. Each names the data it needs.' }),
      el('div', { class: 'missing' }, missing.map((f) => el('div', { class: 'row' },
        el('div', null, el('b', { text: f.entity.label }), ' ', el('span', { class: 'chip mono', text: f.rule_id }), ' ', el('span', { class: 'chip', text: f.severity })),
        el('div', { class: 'muted', text: 'Needs ' + f.unavailable.connector + '. ' + f.unavailable.fix }))))) : null;
    return el('div', null, list, miss);
  }

  function render(d) {
    const b = d.brand || {};
    const t = d.tiles || {};
    UI.mount('#app',
      el('header', { class: 'screen-head' }, el('h1', { text: 'Supply and inventory' }),
        el('p', { text: 'Through ' + fmt.date(b.as_of) + '. Which SKUs run out first, what to order now, and what stock costs to land.' })),
      simBanner(b, d.scale),
      section('At a glance', el('div', { class: 'grid tiles three' }, tile(t.cover), tile(t.short), tile(t.value))),
      section('What the rules say', el('div', { class: 'grid two' }, (d.insights || []).map((i) =>
        UI.insight({ sentence: i.sentence, rule: i.rule, severity: i.severity, capability: i.capability,
          autonomy: AUTONOMY_KIT[i.autonomy] || i.autonomy, stub: i.stub, screen: SLUG })))),
      section('Stock against the next PO', chart(d.chart || { unavailable: true, reason: 'no data' })),
      section('Audit findings', findingsList(d.findings || [])),
      section('Reorder table', el('p', { class: 'th', text: 'Sorted by days of stock. Pace is the last ' + d.settings.velocity_days + ' days. Reorder point is pace times lead time plus safety stock (' + d.settings.service_z + ' times the daily spread times the root of lead time). Order now covers lead time plus ' + d.settings.review_days + ' days, less stock and open POs.' }),
        skuTable(d.skus || [])));
  }

  UI.api('/api/' + SLUG + '/overview?brand=' + encodeURIComponent(brand))
    .then(render)
    .catch((e) => UI.mount('#app', el('header', { class: 'screen-head' }, el('h1', { text: 'Supply and inventory' })),
      UI.emptyState({ screen: SLUG, title: 'Could not load', text: String(e.message || e) })));
})();
