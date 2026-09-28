/* Products and research, round 0. Reads /api/01-market-research/overview and composes kit components.
   No numbers are computed here; the server sends every value, rule and sentence. */
(function () {
  'use strict';
  const SLUG = '01-market-research';
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
      ': simulated data. Sales, units and list prices are generated from a public profile. Nothing here is a ' + name +
      ' result. Review counts, ratings and competitor prices are public and come from the brand brain.');
  }

  function freshness(t) {
    const src = (t.sources || []).map((s) => s.table).join(', ');
    return t.freshness ? (fmt.date(t.freshness) + (src ? ' from ' + src : '')) : null;
  }

  function tile(t, extra) {
    return UI.tile(Object.assign({}, t, { freshness: freshness(t) }, extra || {}));
  }

  function chip(text, tone) { return el('span', { class: 'chip ' + (tone || ''), text }); }

  function points(v) { return v == null ? 'unavailable' : (v > 0 ? '+' : '') + v.toFixed(1) + ' pt'; }

  function demandTable(rows, w) {
    return el('div', null,
      el('p', { class: 'th', text: 'Units in ' + w.months.join(' to ') + ' against ' + w.year_ago.join(' to ') +
        '. "vs store" is the line\'s growth minus the whole store\'s, in points. Reviews are the brand site\'s public totals.' }),
      el('div', { class: 'card scroll' }, UI.table({
        columns: [
          { key: 'line', label: 'Line' },
          { key: 'skus', label: 'SKUs', unit: 'n' },
          { key: 'units', label: 'Units 3 mo', unit: 'n' },
          { key: 'growth', label: 'vs last year', unit: '%' },
          { key: 'gap_points', label: 'vs store', align: 'right', format: points },
          { key: 'net_sales', label: 'Net sales 3 mo', unit: '$' },
          { key: 'rating', label: 'Stars', align: 'right', format: (v) => v == null ? 'no record' : v.toFixed(2) },
          { key: 'reviews', label: 'Reviews', align: 'right', format: (v) => v == null ? 'no record' : fmt.int(v) },
          { key: 'low_star_share', label: '1 and 2 star', align: 'right', format: (v) => v == null ? 'no record' : fmt.pct(v) },
          { key: 'status', label: 'Trend', format: (v) => v },
        ],
        rows, sort: { key: 'units', dir: 'desc' },
      })));
  }

  function priceTable(p) {
    if (p.unavailable) return UI.emptyState({ screen: SLUG, title: 'No catalog', text: p.reason, missing: [p.fix] });
    const comps = (p.competitors || []).map((c) => c.name + ' ' + (c.median != null ? fmt.money(c.median) : 'no median')).join(', ');
    return el('div', null,
      el('p', { class: 'th', text: 'Per pair: ' + p.basis + '. Competitor medians: ' + comps + '.' }),
      el('div', { class: 'card scroll' }, UI.table({
        columns: [
          { key: 'line', label: 'Line' },
          { key: 'category', label: 'Category' },
          { key: 'packs', label: 'Packs', unit: 'n' },
          { key: 'per_pair_low', label: 'Per pair, low', unit: '$' },
          { key: 'per_pair_high', label: 'Per pair, high', unit: '$' },
          { key: 'band', label: 'Competitor band', align: 'right',
            format: (v, r) => r.band_low == null ? 'no competitor on file' : fmt.money(r.band_low) + ' to ' + fmt.money(r.band_high) },
          { key: 'position', label: 'Position', format: (v) => v || 'not compared' },
        ],
        rows: p.rows.map((r) => Object.assign({ band: r.band_low }, r)), sort: false,
      })));
  }

  function list(items) { return el('ul', null, (items.length ? items : ['none on file']).map((t) => el('li', { text: t }))); }

  function reviewTiles(rows) {
    if (!rows.length) return UI.emptyState({ screen: SLUG, title: 'No reviews on file', text: 'The brand brain has no review totals per line yet.', missing: ['reviews'] });
    return el('div', { class: 'reviews' }, rows.map((r) => el('div', { class: 'card review' },
      el('h4', { text: r.line }),
      el('div', { class: 'stat', text: (r.rating != null ? r.rating.toFixed(2) + ' stars, ' : '') + fmt.int(r.reviews) +
        ' reviews, ' + fmt.pct(r.low_star_share) + ' are 1 or 2 stars' }),
      el('div', { class: 'lbl good', text: 'What works' }), list(r.works),
      el('div', { class: 'lbl bad', text: 'What fails' }), list(r.fails),
      r.ladders.length ? el('div', { class: 'lbl', text: 'Objection ladders built from these reviews' }) : null,
      r.ladders.map((l) => el('div', { class: 'rung', text: l.theme.replace(/_/g, ' ') + ': ' +
        l.rungs.map((g) => 'rung ' + g.level + ', "' + g.doubt + '", ' + g.one_star + ' one-star').join('; ') })))));
  }

  function pipeline(p) {
    const floor = p.floor_pct != null ? 'The brand floor is ' + p.floor_pct + ' percent, from ' + p.floor_source + '.'
      : 'No floor on file: enter a target contribution margin on the setup screen.';
    return el('div', null,
      el('p', { class: 'gate', text: 'Margin gate: ' + p.gate_rule + ' ' + floor }),
      el('div', { class: 'card scroll' }, UI.table({
        columns: p.columns.map((c) => ({ key: c, label: c.replace(/_/g, ' ') })), rows: p.rows, sort: false,
        empty: 'No candidates yet. The pipeline fills when the first idea is screened.' })),
      UI.decisionRow({ capability: 'PROD-C01', autonomy: 'agent', screen: SLUG,
        stub: 'Screen 3 next-SKU ideas for the top line against demand, competition and store fit, then add them to this ' +
          'pipeline with a time box. Nothing is bought or listed; your choice is logged.' }));
  }

  function chart(c) {
    if (c.unavailable) return UI.emptyState({ screen: SLUG, title: 'No monthly product sales', text: c.reason, missing: [c.fix] });
    return el('div', { class: 'card' }, Charts.bar({
      labels: c.labels, series: c.series, stacked: true, unit: 'n', title: 'Units by line, ' + c.window,
      note: 'Top 5 lines by units; the rest are grouped. Whole months only.' }));
  }

  function findingsList(fs) {
    if (!fs.length) return el('p', { text: 'No findings this run.' });
    return el('div', { class: 'card' }, fs.map((f) => el('div', { class: 'finding' },
      el('div', { class: 'tags' },
        chip(f.severity, f.severity === 'critical' || f.severity === 'high' ? 'bad' : 'warn'),
        chip(f.rule_id, 'mono'), chip(f.capability.id, 'mono'),
        f.status === 'unavailable' ? chip('unavailable') : null,
        f.confidence < 0.3 ? chip('weak evidence') : null),
      el('div', { text: f.sentence }),
      f.money_at_stake ? el('div', { class: 'money', text: fmt.money(f.money_at_stake.usd) + ' at stake = ' + f.money_at_stake.formula +
        ' (' + Object.entries(f.money_at_stake.inputs).map(([k, v]) => k + ' ' + v).join(', ') + '), ' + f.money_at_stake.window })
        : el('div', { class: 'money', text: 'Money at stake unavailable: ' + (f.money_reason || 'no baseline') }),
      f.brain_refs.length ? el('div', { class: 'money', text: 'Brain: ' + f.brain_refs.join(', ') }) : null)));
  }

  function render(d) {
    const b = d.brand || {};
    const t = d.tiles || {};
    const w = (d.window || {}).trend;
    const parts = [
      el('header', { class: 'screen-head' }, el('h1', { text: 'Products and research' }),
        el('p', { text: 'Which lines are growing, where prices sit against competitors, what reviews say, and what to launch next. Through ' + fmt.date(b.as_of) + '.' })),
      simBanner(b),
      section('Demand', el('div', { class: 'grid tiles three' },
        tile(t.units), tile(t.losing), tile(t.rating))),
      section('What the rules say', el('div', { class: 'grid two' }, (d.insights || []).map((i) =>
        UI.insight({ sentence: i.sentence, rule: i.rule, severity: i.severity, capability: i.capability,
          autonomy: AUTONOMY_KIT[i.autonomy] || i.autonomy, screen: SLUG })))),
      section('Units by line, 12 months', chart(d.chart)),
    ];
    if (w) parts.push(section('Demand by line', demandTable(d.demand || [], w)));
    parts.push(section('Price bands against competitors', priceTable(d.price_bands || {})));
    parts.push(section('Review mining by line', reviewTiles(d.reviews || [])));
    parts.push(section('Candidate pipeline', pipeline(d.pipeline)));
    parts.push(section('Audit findings', findingsList(d.findings || [])));
    UI.mount('#app', ...parts);
  }

  UI.api('/api/' + SLUG + '/overview?brand=' + encodeURIComponent(brand))
    .then(render)
    .catch((e) => UI.mount('#app', el('header', { class: 'screen-head' }, el('h1', { text: 'Products and research' })),
      UI.emptyState({ screen: SLUG, title: 'Could not load', text: String(e.message || e) })));
})();
