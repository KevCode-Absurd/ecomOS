/* Experiments and memory, round 0. Reads /api/25-experiments/overview and composes kit components.
   No numbers are computed here; the server sends every value, rule and sentence. */
(function () {
  'use strict';
  const SLUG = '25-experiments';
  const { el, fmt } = UI;
  const brand = new URLSearchParams(location.search).get('brand') || 'bombas';
  const AUTONOMY_KIT = { agent_does: 'agent', founder_gate: 'founder_gate', human_assist: 'human_assist', agent: 'agent' };
  const STATUS = { running: 'Running', proposed: 'Proposed', parked: 'Parked', done: 'Done' };

  function section(title, ...children) {
    return el('section', { class: 'section' }, el('h3', { text: title }), ...children);
  }

  function simBanner(b) {
    const name = b.name || b.brand || 'This brand';
    if (!b.simulated) return el('div', { class: 'sim', role: 'note' }, el('b', { text: name }), ' live data. Read-only.');
    return el('div', { class: 'sim', role: 'note' }, el('b', { text: name }),
      ': simulated data. The tests come from the brain\'s test queue; every date, result and decision in the registry is made up, and every sales number is generated. Nothing here is a ' + name + ' result.');
  }

  function tile(t) { return UI.tile(Object.assign({}, t, { freshness: t.freshness ? fmt.date(t.freshness) + ' from registry' : null })); }

  function outcome(r) {
    if (r.outcome_unavailable) return 'unavailable: ' + r.outcome_unavailable;
    if (r.outcome_now == null) return 'unavailable';
    return (r.outcome_unit === 'usd' ? fmt.money(r.outcome_now) : r.outcome_unit === 'ratio' ? (r.outcome_now * 100).toFixed(2) + ' percent' : String(r.outcome_now)) +
      (r.outcome_label ? ' ' + r.outcome_label : '');
  }

  function registry(rows) {
    return el('div', { class: 'wrap' }, UI.table({ columns: [
      { key: 'id', label: 'Test' },
      { key: 'status', label: 'Status', format: (v) => STATUS[v] || v },
      { key: 'hypothesis', label: 'Hypothesis' },
      { key: 'metric', label: 'Metric', format: (v, r) => v ? v + (r.min_days ? ', ' + r.min_days + ' days minimum' : '') : 'none agreed' },
      { key: 'start', label: 'Start', format: (v) => v || 'not started' },
      { key: 'read_point', label: 'Read point', format: (v, r) => v ? v + (r.days_to_read < 0 ? ', ' + (-r.days_to_read) + ' days ago' : ', in ' + r.days_to_read + ' days') : (r.park ? 'parked: ' + r.park.reason : 'none') },
      { key: 'result', label: 'Result', format: (v, r) => v ? v + ' ' + (r.lift * 100).toFixed(0) + ' percent, read ' + r.read_on : 'no result' },
      { key: 'decision', label: 'Decision', format: (v) => v ? v.replace('_', ' ') : 'none' },
      { key: 'outcome_now', label: 'Metric now, 28 days', format: (v, r) => outcome(r) },
    ], rows, sort: false }));
  }

  function chart(c) {
    return el('div', { class: 'card' }, Charts.bar({
      labels: c.labels, unit: 'n', values: true, height: 200,
      series: [{ name: 'Days run', values: c.days_run }, { name: 'Minimum days', values: c.min_days, color: 'var(--s2)' }],
      title: 'Days run against the minimum each test needs',
      note: 'Simulated registry. ' + c.basis + '. A test with no agreed metric has no minimum (hatched).',
    }));
  }

  function findingsList(fs) {
    if (!fs.length) return el('p', { text: 'No findings this run.' });
    return el('div', { class: 'card' }, fs.map((f) => el('div', { class: 'finding' },
      el('div', { class: 'tags' },
        el('span', { class: 'chip ' + (f.severity === 'critical' || f.severity === 'high' ? 'bad' : 'warn'), text: f.severity }),
        el('span', { class: 'chip mono', text: f.rule_id }),
        el('span', { class: 'chip mono', text: f.capability.id }),
        f.status === 'unavailable' ? el('span', { class: 'chip', text: 'unavailable' }) : null),
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
      el('header', { class: 'screen-head' }, el('h1', { text: 'Experiments and memory' }),
        el('p', { text: 'Through ' + fmt.date(b.as_of) + '. What is running, which reads are late, what won, and what the brain has learned.' })),
      simBanner(b),
      section('The loop today', el('div', { class: 'grid tiles three' }, tile(t.running), tile(t.due), tile(t.stale))),
      section('What the rules say', el('div', { class: 'grid two' }, (d.insights || []).map((i) =>
        UI.insight({ sentence: i.sentence, rule: i.rule, severity: i.severity, capability: i.capability,
          autonomy: AUTONOMY_KIT[i.autonomy] || i.autonomy, stub: i.stub, screen: SLUG })))),
      section('Test length', chart(d.chart)),
      section('Registry', el('p', { class: 'th', text: 'Simulated entries seeded from the brain. Metric now comes from the metric contract; a metric with no formula reads unavailable.' }),
        registry(d.registry || [])),
      section('Audit findings', findingsList(d.findings || [])));
  }

  UI.api('/api/' + SLUG + '/overview?brand=' + encodeURIComponent(brand))
    .then(render)
    .catch((e) => UI.mount('#app', el('header', { class: 'screen-head' }, el('h1', { text: 'Experiments and memory' })),
      UI.emptyState({ screen: SLUG, title: 'Could not load', text: String(e.message || e) })));
})();
