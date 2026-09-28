/* Organic and content, round 0. Reads /api/16-organic-content/overview and composes kit components.
   No numbers are computed here; the server sends every value, rule and sentence. */
(function () {
  'use strict';
  const SLUG = '16-organic-content';
  const TITLE = 'Organic and content';
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
      ': simulated data. Posts, views and matched orders are generated from a public profile. Competitor counts are public Ad Library signals, not proof. Nothing here is a ' + name + ' result.');
  }

  function tile(t) {
    const src = (t.sources || []).map((s) => s.table).join(', ');
    const fresh = t.freshness ? fmt.date(t.freshness) + (src ? ' from ' + src : '') : null;
    return UI.tile(Object.assign({}, t, { freshness: fresh }));
  }

  function table(columns, rows, sortKey) {
    return el('div', { class: 'table-wrap' }, UI.table({ columns, rows, sort: { key: sortKey, dir: 'desc' } }));
  }

  function chart(c) {
    return el('div', { class: 'card' }, Charts.bar({ labels: c.labels, series: c.series, benchmark: c.benchmark, unit: 'per 1k',
      title: 'Orders per 1,000 views by hook, ' + c.window, note: 'Line is the median hook. Orders are ' + c.basis + '.' }));
  }

  function findingsList(fs) {
    if (!fs.length) return el('p', { text: 'No findings this run.' });
    return el('div', { class: 'card' }, fs.map((f) => el('div', { class: 'finding' },
      el('div', { class: 'tags' },
        el('span', { class: 'chip ' + (f.severity === 'critical' || f.severity === 'high' ? 'bad' : 'warn'), text: f.severity }),
        el('span', { class: 'chip mono', text: f.rule_id }),
        el('span', { class: 'chip mono', text: f.capability.id }),
        f.status === 'unavailable' ? el('span', { class: 'chip', text: 'unavailable' }) : null,
        f.status !== 'unavailable' && f.confidence < 0.3 ? el('span', { class: 'chip', text: 'weak evidence' }) : null),
      el('div', { text: f.sentence }),
      f.unavailable ? el('div', { class: 'money', text: 'Needs ' + f.unavailable.inputs.join(', ') + '. ' + f.unavailable.fix }) : null,
      f.money_at_stake ? el('div', { class: 'money', text: fmt.money(f.money_at_stake.usd) + ' at stake = ' + f.money_at_stake.formula +
        ' (' + Object.entries(f.money_at_stake.inputs).map(([k, v]) => k + ' ' + v).join(', ') + ')' })
        : el('div', { class: 'money', text: 'Money at stake unavailable: ' + (f.money_reason || 'no baseline') }))));
  }

  function render(d) {
    const b = d.brand || {};
    const parts = [
      el('header', { class: 'screen-head' }, el('h1', { text: TITLE }),
        el('p', { text: 'Instagram and TikTok posts through ' + fmt.date(b.as_of) + '. What went out, what sold, what is not tracked yet.' })),
      simBanner(b),
    ];
    if (d.unavailable) {
      parts.push(UI.emptyState({ screen: SLUG, title: 'No post export is connected', text: d.reason, missing: [d.fix] }));
      parts.push(section('Audit findings', findingsList(d.findings || [])));
      return UI.mount('#app', ...parts);
    }
    const t = d.tiles || {};
    parts.push(section('Posts and what they sold',
      el('div', { class: 'grid tiles' }, tile(t.posts), tile(t.orders_per_1k), tile(t.organic_sessions))));
    parts.push(section('What the rules say', el('div', { class: 'grid two' }, (d.insights || []).map((i) =>
      UI.insight({ sentence: i.sentence, rule: i.rule, severity: i.severity, capability: i.capability,
        autonomy: AUTONOMY_KIT[i.autonomy] || i.autonomy, screen: SLUG })))));
    parts.push(section('Which hooks sell', chart(d.chart)));
    parts.push(section('Hooks, last 90 days',
      el('p', { class: 'th', text: 'Matched orders come from the post\'s own link tag or promo code, not platform attribution.' }),
      table([
        { key: 'hook', label: 'Hook' },
        { key: 'posts', label: 'Posts', unit: 'n' },
        { key: 'views', label: 'Views', unit: 'n' },
        { key: 'matched_orders', label: 'Matched orders', unit: 'n' },
        { key: 'per_1k', label: 'Orders per 1,000 views', unit: 'per 1k' },
        { key: 'per_1k_prior', label: '90 days before', unit: 'per 1k' },
      ], d.hooks || [], 'per_1k')));
    parts.push(section('Top posts by views, last 30 days', table([
      { key: 'date', label: 'Date' },
      { key: 'platform', label: 'Platform' },
      { key: 'format', label: 'Format' },
      { key: 'hook', label: 'Hook' },
      { key: 'views', label: 'Views', unit: 'n' },
      { key: 'saves', label: 'Saves', unit: 'n' },
      { key: 'clicks', label: 'Clicks', unit: 'n' },
      { key: 'matched_orders', label: 'Orders', unit: 'n' },
    ], d.top_posts || [], 'views')));
    parts.push(section('Audit findings', findingsList(d.findings || [])));
    UI.mount('#app', ...parts);
  }

  UI.api('/api/' + SLUG + '/overview?brand=' + encodeURIComponent(brand))
    .then(render)
    .catch((e) => UI.mount('#app', el('header', { class: 'screen-head' }, el('h1', { text: TITLE })),
      UI.emptyState({ screen: SLUG, title: 'Could not load', text: String(e.message || e) })));
})();
