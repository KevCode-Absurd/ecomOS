/* Creative, round 0. Reads /api/09-creative/overview and composes kit components.
   No numbers are computed here; the server sends every value, rule and sentence. */
(function () {
  'use strict';
  const SLUG = '09-creative';
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
      ': simulated data. Ad numbers are generated from a public profile. Competitor counts are public Ad Library signals, not proof. Nothing here is a ' + name + ' result.');
  }

  function tile(t, extra) {
    const src = (t.sources || []).map((s) => s.table).join(', ');
    const fresh = t.freshness ? fmt.date(t.freshness) + (src ? ' from ' + src : '') : null;
    return UI.tile(Object.assign({}, t, { freshness: fresh }, extra || {}));
  }

  function formats(rows) {
    return UI.table({
      columns: [
        { key: 'format', label: 'Format' },
        { key: 'ads', label: 'Ads', unit: 'n' },
        { key: 'spend', label: 'Spend 28d', unit: '$' },
        { key: 'share', label: 'Share', unit: '%' },
        { key: 'roas', label: 'ROAS', unit: 'x' },
        { key: 'roas_median_4w', label: 'Own median, 4 windows', unit: 'x' },
      ],
      rows, sort: { key: 'spend', dir: 'desc' },
    });
  }

  function chart(c) {
    return el('div', { class: 'card' }, Charts.bar({ labels: c.labels.map((d) => d.slice(5)), series: c.series, unit: 'x',
      title: 'Meta ROAS by format, ' + c.window, note: 'ROAS is ' + c.basis + '.' }));
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
        : el('div', { class: 'money', text: 'Money at stake unavailable: ' + (f.money_reason || 'no baseline') }),
      f.flags ? el('div', { class: 'money', text: f.flags.join('; ') }) : null)));
  }

  function render(d) {
    const b = d.brand || {};
    const parts = [
      el('header', { class: 'screen-head' }, el('h1', { text: 'Creative' }),
        el('p', { text: 'Meta, ad level, through ' + fmt.date(b.as_of) + '. Which formats win, what is starved, what is missing.' })),
      simBanner(b),
    ];
    if (d.unavailable) {
      parts.push(UI.emptyState({ screen: SLUG, title: 'Meta is not connected', text: d.reason, missing: [d.fix] }));
      parts.push(section('Audit findings', findingsList(d.findings || [])));
      return UI.mount('#app', ...parts);
    }
    const t = d.tiles || {};
    parts.push(section('Pipeline and signal',
      el('div', { class: 'grid tiles' }, tile(t.new_ads), tile(t.video_share), tile(t.hook_rate))));
    parts.push(section('What the rules say', el('div', { class: 'grid two' }, (d.insights || []).map((i) =>
      UI.insight({ sentence: i.sentence, rule: i.rule, severity: i.severity, capability: i.capability,
        autonomy: AUTONOMY_KIT[i.autonomy] || i.autonomy, screen: SLUG })))));
    parts.push(section('ROAS by format', chart(d.chart)));
    parts.push(section('Formats, last 28 days',
      el('p', { class: 'th', text: 'Account ROAS ' + (d.account_roas == null ? 'unavailable' : fmt.ratio(d.account_roas)) +
        '. Ads that share an image keep their own rows. Dynamic creatives are read as one ad.' }),
      formats(d.formats || [])));
    parts.push(section('Audit findings', findingsList(d.findings || [])));
    UI.mount('#app', ...parts);
  }

  UI.api('/api/' + SLUG + '/overview?brand=' + encodeURIComponent(brand))
    .then(render)
    .catch((e) => UI.mount('#app', el('header', { class: 'screen-head' }, el('h1', { text: 'Creative' })),
      UI.emptyState({ screen: SLUG, title: 'Could not load', text: String(e.message || e) })));
})();
