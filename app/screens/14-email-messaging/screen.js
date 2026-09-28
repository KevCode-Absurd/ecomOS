/* Email and messaging, round 0. Reads /api/14-email-messaging/overview and composes kit components.
   No numbers are computed here; the server sends every value, rule and sentence. */
(function () {
  'use strict';
  const SLUG = '14-email-messaging';
  const { el, fmt } = UI;
  const brand = new URLSearchParams(location.search).get('brand') || 'bombas';
  const AUTONOMY_KIT = { agent_does: 'agent', founder_gate: 'founder_gate', human_assist: 'human_assist', agent: 'agent' };
  const SEV_CHIP = { critical: 'bad', high: 'bad', medium: 'warn', low: '' };

  function section(title, ...children) {
    return el('section', { class: 'section' }, el('h3', { text: title }), ...children);
  }

  function simBanner(b) {
    const name = b.name || b.brand || 'This brand';
    if (!b.simulated) return el('div', { class: 'sim', role: 'note' }, el('b', { text: name }), ' live data. Read-only.');
    return el('div', { class: 'sim', role: 'note' }, el('b', { text: name }),
      ': simulated data. Every number on this page is generated from a public profile. Nothing here is a ' + name + ' result.');
  }

  function freshness(t) {
    const src = (t.sources || []).map((s) => s.table).join(', ');
    return t.freshness ? (fmt.date(t.freshness) + (src ? ' from ' + src : '')) : null;
  }

  function tile(t, extra) {
    return UI.tile(Object.assign({}, t, { freshness: freshness(t) }, extra || {}));
  }

  function chart(c) {
    if (c.unavailable) return UI.emptyState({ screen: SLUG, title: 'No flow sends', text: c.reason, missing: [c.fix] });
    return el('div', { class: 'card' }, Charts.bar({
      labels: c.labels,
      series: [{ name: 'Email platform', values: c.platform }, { name: 'Real orders', values: c.matched, color: 'var(--s2)' }],
      unit: '$', title: 'Flow revenue, platform against real orders, ' + c.window,
      note: 'The platform is the email tool\'s attributed revenue. Real orders are net revenue of orders matched to a send.' }));
  }

  function flowTable(rows) {
    return el('div', { class: 'table-wrap' }, UI.table({
      columns: [
        { key: 'flow', label: 'Flow' },
        { key: 'channels', label: 'Channels' },
        { key: 'messages', label: 'Messages', unit: 'n' },
        { key: 'sends', label: 'Sends', unit: 'n' },
        { key: 'open_rate', label: 'Open rate', unit: '%' },
        { key: 'click_rate', label: 'Click rate', unit: '%' },
        { key: 'unsubscribe_rate', label: 'Unsub rate', unit: '%' },
        { key: 'platform_revenue', label: 'Platform revenue', unit: '$' },
        { key: 'matched_revenue', label: 'Real-order revenue', unit: '$' },
        { key: 'gap', label: 'Gap', unit: '%' },
      ],
      rows, sort: { key: 'matched_revenue', dir: 'desc' },
    }));
  }

  function findingsList(fs) {
    if (!fs.length) return el('p', { text: 'No findings this run.' });
    const open = fs.filter((f) => f.status !== 'unavailable');
    const missing = fs.filter((f) => f.status === 'unavailable');
    const row = (f) => el('div', { class: 'finding' },
      el('div', { class: 'tags' },
        el('span', { class: 'chip ' + (f.status === 'unavailable' ? '' : SEV_CHIP[f.severity] || ''), text: f.status === 'unavailable' ? 'unavailable' : f.severity }),
        el('span', { class: 'chip mono', text: f.rule_id }),
        el('span', { class: 'chip mono', text: f.capability.id }),
        f.status !== 'unavailable' && f.confidence < 0.3 ? el('span', { class: 'chip', text: 'weak evidence' }) : null),
      el('div', { text: f.sentence }),
      f.status === 'unavailable'
        ? el('div', { class: 'money', text: 'Needs ' + f.unavailable.inputs.join(', ') + '. ' + f.unavailable.fix })
        : f.money_at_stake
          ? el('div', { class: 'money', text: fmt.money(f.money_at_stake.usd) + ' at stake = ' + f.money_at_stake.formula +
            ' (' + Object.entries(f.money_at_stake.inputs).map(([k, v]) => k + ' ' + v).join(', ') + ')' })
          : el('div', { class: 'money', text: 'Money at stake unavailable: ' + (f.money_reason || 'no baseline') }));
    return el('div', null,
      el('div', { class: 'card' }, open.length ? open.map(row) : el('p', { text: 'No rule fired on this data.' })),
      missing.length ? el('h4', { text: missing.length + ' rules cannot run yet' }) : null,
      missing.length ? el('div', { class: 'card' }, missing.map(row)) : null);
  }

  function render(d) {
    const b = d.brand || {};
    const parts = [
      el('header', { class: 'screen-head' }, el('h1', { text: 'Email and messaging' }),
        el('p', { text: 'Flows, campaigns and SMS through ' + fmt.date(b.as_of) + '. What the list earns in real orders, and where it leaks.' })),
      simBanner(b),
    ];
    const t = d.tiles || {};
    parts.push(section('Last 28 days',
      el('div', { class: 'grid tiles three' }, tile(t.flow_revenue, { delta_label: 'vs prior 28d' }),
        tile(t.list_growth, { delta_label: 'vs prior 28d' }), tile(t.unsubscribe_rate, { delta_label: 'vs prior 28d' }))));
    if (d.unavailable) {
      parts.push(UI.emptyState({ screen: SLUG, title: 'Email is not connected', text: d.reason, missing: [d.fix] }));
      parts.push(section('Audit findings', findingsList(d.findings || [])));
      return UI.mount('#app', ...parts);
    }
    parts.push(section('What the rules say', el('div', { class: 'grid two' }, (d.insights || []).map((i) =>
      UI.insight({ sentence: i.sentence, rule: i.rule, severity: i.severity, capability: i.capability,
        autonomy: AUTONOMY_KIT[i.autonomy] || i.autonomy, screen: SLUG })))));
    parts.push(section('Flow revenue check', chart(d.chart)));
    parts.push(section('Every flow, last 28 days',
      el('p', { class: 'th', text: 'Open rate is email only. Gap is the platform count over real orders, minus 1. An order matched to 2 flows counts in each.' }),
      flowTable(d.flows || [])));
    parts.push(section('Audit findings', findingsList(d.findings || [])));
    UI.mount('#app', ...parts);
  }

  UI.api('/api/' + SLUG + '/overview?brand=' + encodeURIComponent(brand))
    .then(render)
    .catch((e) => UI.mount('#app', el('header', { class: 'screen-head' }, el('h1', { text: 'Email and messaging' })),
      UI.emptyState({ screen: SLUG, title: 'Could not load', text: String(e.message || e) })));
})();
