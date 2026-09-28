/* Customers and CX, round 0. Reads /api/15-customers-cx/overview and composes kit components.
   No numbers are computed here; the server sends every value, rule and sentence. */
(function () {
  'use strict';
  const SLUG = '15-customers-cx';
  const { el, fmt } = UI;
  const brand = new URLSearchParams(location.search).get('brand') || 'bombas';
  const AUTONOMY_KIT = { agent_does: 'agent', founder_gate: 'founder_gate', human_assist: 'human_assist', agent: 'agent' };
  const THEME = (t) => (t || '').replace(/_/g, ' ');

  function section(title, ...children) {
    return el('section', { class: 'section' }, el('h3', { text: title }), ...children);
  }

  function simBanner(b) {
    const name = b.name || b.brand || 'This brand';
    if (!b.simulated) return el('div', { class: 'sim', role: 'note' }, el('b', { text: name }), ' live data. Read-only.');
    return el('div', { class: 'sim', role: 'note' }, el('b', { text: name }),
      ': simulated data. Policies and objection ladders come from public pages and reviews; every ticket, rating, order and repeat is generated. Nothing here is a ' + name + ' result.');
  }

  function tile(t) {
    const src = (t.sources || []).map((s) => s.table).join(', ');
    return UI.tile(Object.assign({}, t, { freshness: t.freshness ? fmt.date(t.freshness) + (src ? ' from ' + src : '') : null }));
  }

  function pct(v, d) { return v == null ? 'unavailable' : (v * 100).toFixed(d == null ? 1 : d) + ' percent'; }

  function chart(c) {
    if (c.unavailable) return UI.emptyState({ screen: SLUG, title: 'No tickets by month', text: c.reason, missing: [c.fix] });
    const note = (c.partial.length ? c.partial.join(', ') + ' is a partial month. ' : '') + 'Tickets opened in the month per 100 paid orders placed in the month.';
    return el('div', { class: 'card' }, Charts.bar({ labels: c.labels.map((m) => m.slice(2)), stacked: true, unit: 'n',
      title: 'Support tickets per 100 orders, by reason, ' + c.window, note, maxLabels: 12,
      series: c.series.map((s) => ({ name: s.name, values: s.values })) }));
  }

  function reasons(r) {
    if (r.unavailable) return UI.emptyState({ screen: SLUG, title: 'No ticket reasons', text: r.reason, missing: [r.fix] });
    return el('div', null,
      el('p', { class: 'th', text: fmt.int(r.tickets) + ' tickets and ' + fmt.int(r.paid_orders) + ' paid orders, ' + r.window.start + ' to ' + r.window.end +
        '. Counted in the simulated table, so counts are a sample and rates are the part to read. ' + r.note }),
      el('div', { class: 'stack' },
        UI.table({ columns: [
          { key: 'reason', label: 'Reason' },
          { key: 'tickets', label: 'Tickets', unit: 'n' },
          { key: 'share', label: 'Share', unit: '%' },
          { key: 'share_before', label: '28 days before', unit: '%' },
          { key: 'per_100_orders', label: 'Per 100 orders', format: (v) => v == null ? 'unavailable' : v.toFixed(2) },
          { key: 'csat', label: 'CSAT', unit: '%' },
        ], rows: r.rows, sort: false }),
        UI.table({ columns: [
          { key: 'channel', label: 'Channel' },
          { key: 'tickets', label: 'Tickets', unit: 'n' },
          { key: 'share', label: 'Share', unit: '%' },
          { key: 'first_reply_min', label: 'First reply, min', format: (v) => v == null ? 'unavailable' : Math.round(v).toString() },
          { key: 'target_min', label: 'Line, min', format: (v) => v == null ? 'none set' : fmt.int(v) },
        ], rows: r.channels, sort: false })));
  }

  function repeat(r) {
    if (r.unavailable) return UI.emptyState({ screen: SLUG, title: 'No repeat curve', text: 'The order table is not connected.' });
    return el('div', null,
      el('p', { class: 'th', text: 'First-time buyers by month of first order, and the share who ordered again within ' + r.days + ' days. A cohort shows once everyone in it has had the full ' + r.days + ' days.' }),
      UI.table({ columns: [
        { key: 'cohort', label: 'Cohort' },
        { key: 'customers', label: 'First-time buyers', unit: 'n' },
        { key: 'repeat', label: 'Ordered again', unit: 'n' },
        { key: 'rate', label: 'Repeat rate', unit: '%' },
      ], rows: r.cohorts.slice().reverse(), sort: false }));
  }

  function reviews(v, ladders, policy) {
    const left = v.unavailable ? UI.emptyState({ screen: SLUG, title: 'No reviews', text: v.reason, missing: [v.fix] }) :
      el('div', { class: 'card' }, el('h4', { text: 'Reviews, last 28 days' }), el('dl', { class: 'kv' },
        el('dt', { text: 'Reviews' }), el('dd', { text: fmt.int(v.reviews) + ' from ' + v.sources.join(', ') }),
        el('dt', { text: 'Average' }), el('dd', { text: v.average.toFixed(2) + ' stars' }),
        el('dt', { text: 'By star' }), el('dd', { text: ['5', '4', '3', '2', '1'].map((k) => k + ' star ' + fmt.int(v.by_star[k])).join(', ') }),
        el('dt', { text: '2 stars or below' }), el('dd', { text: pct(v.low_share) }),
        el('dt', { text: 'Replied to' }), el('dd', { text: 'unavailable: ' + v.replied_reason })),
        policy ? el('p', { class: 'th', text: policy.text + ' (' + policy.ref + ')' }) : null);
    const right = el('div', null,
      el('p', { class: 'th', text: 'Objection ladders from the brand brain: public complaint quotes by theme and the top rung. These are real public quotes, not simulated.' }),
      UI.table({ columns: [
        { key: 'theme', label: 'Theme', format: THEME },
        { key: 'complaints', label: 'Complaints', unit: 'n' },
        { key: 'top_doubt', label: 'Top rung' },
        { key: 'has_proof', label: 'Proof on file', format: (x) => x ? 'yes' : 'no' },
      ], rows: ladders, sort: false }));
    return el('div', { class: 'stack' }, left, right);
  }

  function findingRow(f) {
    return el('div', { class: 'finding' },
      el('div', { class: 'tags' },
        el('span', { class: 'chip ' + (f.severity === 'critical' || f.severity === 'high' ? 'bad' : 'warn'), text: f.severity }),
        el('span', { class: 'chip mono', text: f.rule_id }),
        el('span', { class: 'chip mono', text: f.capability.id }),
        f.status === 'unavailable' ? el('span', { class: 'chip', text: 'unavailable' }) : null,
        f.confidence < 0.3 && f.status !== 'unavailable' ? el('span', { class: 'chip', text: 'weak evidence' }) : null),
      el('div', { text: f.sentence }),
      f.money_at_stake ? el('div', { class: 'money', text: fmt.money(f.money_at_stake.usd) + ' at stake = ' + f.money_at_stake.formula + ' (' +
        Object.entries(f.money_at_stake.inputs).map(([k, v]) => k + ' ' + v).join(', ') + ')' })
        : el('div', { class: 'money', text: 'Money at stake unavailable: ' + (f.money_reason || 'no baseline') }),
      f.unavailable ? el('div', { class: 'money', text: 'Needs ' + f.unavailable.connector + '. ' + f.unavailable.fix }) : null,
      f.status === 'unavailable' ? null : UI.decisionRow({ capability: f.capability.id, autonomy: AUTONOMY_KIT[f.capability.autonomy] || f.capability.autonomy, screen: SLUG }));
  }

  function findingsList(fs) {
    if (!fs.length) return el('p', { text: 'No findings this run.' });
    const open = fs.filter((f) => f.status !== 'unavailable');
    const missing = fs.filter((f) => f.status === 'unavailable');
    return el('div', null,
      el('div', { class: 'card' }, open.length ? open.map(findingRow) : el('p', { text: 'No rule fired on the connected data.' })),
      missing.length ? el('details', { class: 'more' }, el('summary', { text: missing.length + ' rules cannot run yet: their data is not connected' }),
        el('div', { class: 'card' }, missing.map(findingRow))) : null);
  }

  function render(d) {
    const b = d.brand || {};
    const t = d.tiles || {};
    UI.mount('#app',
      el('header', { class: 'screen-head' }, el('h1', { text: 'Customers and CX' }),
        el('p', { text: 'Through ' + fmt.date(b.as_of) + '. What people contact us about, how fast and how well we answer, and who comes back.' })),
      simBanner(b),
      section('At a glance', el('div', { class: 'grid tiles four' }, tile(t.wismo), tile(t.csat), tile(t.first_reply), tile(t.repeat))),
      section('What the rules say', el('div', { class: 'grid two' }, (d.insights || []).map((i) =>
        UI.insight({ sentence: i.sentence, rule: i.rule, severity: i.severity, capability: i.capability,
          autonomy: AUTONOMY_KIT[i.autonomy] || i.autonomy, stub: i.stub, screen: SLUG })))),
      section('Audit findings', findingsList(d.findings || [])),
      section('Why people contact us', chart(d.chart), reasons(d.reasons)),
      section('Repeat by cohort', repeat(d.repeat)),
      section('Reviews and objections', reviews(d.reviews, d.ladders || [], d.policy)));
  }

  UI.api('/api/' + SLUG + '/overview?brand=' + encodeURIComponent(brand))
    .then(render)
    .catch((e) => UI.mount('#app', el('header', { class: 'screen-head' }, el('h1', { text: 'Customers and CX' })),
      UI.emptyState({ screen: SLUG, title: 'Could not load', text: String(e.message || e) })));
})();
