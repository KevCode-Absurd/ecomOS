/* Team and ops, round 0. Reads /api/23-team-ops/overview and composes kit components.
   No numbers are computed here; the server sends every value, rule and sentence. */
(function () {
  'use strict';
  const SLUG = '23-team-ops';
  const { el, fmt } = UI;
  const brand = new URLSearchParams(location.search).get('brand') || 'bombas';
  const AUTONOMY_KIT = { agent_does: 'agent', founder_gate: 'founder_gate', human_assist: 'human_assist', agent: 'agent' };
  const NA = 'unavailable';

  function section(title, ...children) {
    return el('section', { class: 'section' }, el('h3', { text: title }), ...children);
  }

  function simBanner(b) {
    const name = b.name || b.brand || 'This brand';
    if (!b.simulated) return el('div', { class: 'sim', role: 'note' }, el('b', { text: name }), ' live data. Read-only.');
    return el('div', { class: 'sim', role: 'note' }, el('b', { text: name }),
      ': simulated data. Open roles, 3PL and agency facts come from public job posts and press; every ticket, order, ad and cost line is generated. Nothing here is a ' + name + ' result.');
  }

  function tile(t) {
    const src = (t.sources || []).map((s) => s.table).join(', ');
    return UI.tile(Object.assign({}, t, { freshness: t.freshness ? fmt.date(t.freshness) + (src ? ' from ' + src : '') : null }));
  }

  function chart(c) {
    if (c.unavailable) return UI.emptyState({ screen: SLUG, title: 'No tickets by month', text: c.reason, missing: [c.fix] });
    return el('div', { class: 'card' }, Charts.line({ labels: c.labels.map((m) => m.slice(2)), unit: 'x',
      title: 'Tickets and orders by month, as a multiple of the median month, ' + c.window,
      note: 'Full months only. The dashed line is ' + c.benchmark + ' times, where a month counts as a peak for the team.',
      benchmark: c.benchmark, maxLabels: 12,
      series: c.series.map((s) => ({ name: s.name, values: s.values })) }));
  }

  function workload(w, cadence) {
    if (w.unavailable) return UI.emptyState({ screen: SLUG, title: 'No workload windows', text: w.reason, missing: [w.fix] });
    const byWin = {};
    for (const c of cadence || []) byWin[c.start + ' to ' + c.end] = c;
    const rows = w.rows.map((r) => Object.assign({}, r, { new_ads: (byWin[r.window] || {}).new_ads, posts: (byWin[r.window] || {}).posts }));
    return el('div', null,
      el('p', { class: 'th', text: '28-day windows, newest first. ' + w.note + ' New ads are Meta ads first seen in the window; posts are organic posts from platform exports.' }),
      el('div', { class: 'table-wrap' }, UI.table({ columns: [
        { key: 'window', label: 'Window' },
        { key: 'tickets', label: 'Tickets', unit: 'n' },
        { key: 'paid_orders', label: 'Paid orders', unit: 'n' },
        { key: 'per_100_orders', label: 'Tickets per 100 orders', format: (v) => v == null ? NA : v.toFixed(2) },
        { key: 'resolve_hours', label: 'Resolve, hours', format: (v) => v == null ? NA : v.toFixed(1) },
        { key: 'reply_min', label: 'First reply, min', format: (v) => v == null ? NA : Math.round(v).toString() },
        { key: 'new_ads', label: 'New ads', format: (v) => v == null ? NA : fmt.int(v) },
        { key: 'posts', label: 'Posts', format: (v) => v == null ? NA : fmt.int(v) },
      ], rows, sort: false })));
  }

  function team(t, costs) {
    const facts = t.team.concat(t.operations);
    const left = el('div', null,
      el('p', { class: 'th', text: t.open_roles + ' open roles from public job posts, ' + t.care_roles + ' in customer care. These are public facts from the brand brain, not simulated.' }),
      el('div', { class: 'table-wrap' }, UI.table({ columns: [
        { key: 'field', label: 'Kind', format: (v) => (v || '').replace(/_/g, ' ') },
        { key: 'text', label: 'Fact' },
      ], rows: facts, sort: false })));
    let right;
    if (costs.unavailable) right = UI.emptyState({ screen: SLUG, title: 'No cost lines', text: costs.reason, missing: [costs.fix] });
    else right = el('div', { class: 'card' }, el('h4', { text: 'Cost lines per month' }), el('dl', { class: 'kv' },
      el('dt', { text: 'Headcount' }), el('dd', { text: costs.headcount_per_month == null ? NA : fmt.money(costs.headcount_per_month) }),
      el('dt', { text: 'Agencies' }), el('dd', { text: costs.agency_per_month == null ? NA : fmt.money(costs.agency_per_month) }),
      el('dt', { text: 'Software' }), el('dd', { text: fmt.money(costs.tools_per_month) + ' across ' + costs.tools.length + ' tools' }),
      el('dt', { text: 'Software share' }), el('dd', { text: costs.share_of_net_revenue == null ? NA : (costs.share_of_net_revenue * 100).toFixed(2) + ' percent of net revenue, 28 days' }),
      el('dt', { text: 'Stage plan' }), el('dd', { text: costs.stage_plan == null ? NA + ': ' + costs.stage_plan_reason : String(costs.stage_plan) })),
      UI.table({ columns: [
        { key: 'tool', label: 'Tool', format: (v) => (v || '').replace(/_/g, ' ') },
        { key: 'usd_per_month', label: 'Per month', unit: '$' },
      ], rows: costs.tools, sort: false }),
      el('p', { class: 'th', text: costs.note }));
    return el('div', { class: 'pair' }, left, right);
  }

  function decisions(ds) {
    if (!ds.length) return el('p', { text: 'No founder decisions are in the brain yet.' });
    return el('div', { class: 'table-wrap' }, UI.table({ columns: [
      { key: 'date', label: 'Logged' },
      { key: 'text', label: 'Decision' },
      { key: 'owner', label: 'Owner', format: (v) => v || 'none' },
      { key: 'metric', label: 'Metric', format: (v) => v || 'none' },
      { key: 'review_date', label: 'Review date', format: (v) => v || 'none' },
    ], rows: ds, sort: false }));
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
      el('header', { class: 'screen-head' }, el('h1', { text: 'Team and ops' }),
        el('p', { text: 'Through ' + fmt.date(b.as_of) + '. How much work lands on the team, when it peaks, and whether decisions, SOPs and vendors are on paper.' })),
      simBanner(b),
      section('At a glance', el('div', { class: 'grid tiles four' }, tile(t.peak_load), tile(t.tickets_per_order), tile(t.sop_coverage), tile(t.decision_log))),
      section('What the rules say', el('div', { class: 'grid two' }, (d.insights || []).map((i) =>
        UI.insight({ sentence: i.sentence, rule: i.rule, severity: i.severity, capability: i.capability,
          autonomy: AUTONOMY_KIT[i.autonomy] || i.autonomy, stub: i.stub, screen: SLUG })))),
      section('Audit findings', findingsList(d.findings || [])),
      section('Workload by month', chart(d.chart)),
      section('Workload and output by window', workload(d.workload, d.cadence)),
      section('Decision log', decisions(d.decisions || [])),
      section('Team signals and cost lines', team(d.team, d.costs)));
  }

  UI.api('/api/' + SLUG + '/overview?brand=' + encodeURIComponent(brand))
    .then(render)
    .catch((e) => UI.mount('#app', el('header', { class: 'screen-head' }, el('h1', { text: 'Team and ops' })),
      UI.emptyState({ screen: SLUG, title: 'Could not load', text: String(e.message || e) })));
})();
