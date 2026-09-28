/* 20-marketplaces round 0. Everything on the page comes from GET /api/20-marketplaces/ (api.py and audit.py).
   The page does no arithmetic beyond formatting; null means unavailable. */
(async function () {
  'use strict';
  const SLUG = '20-marketplaces';
  const { el, mount, fmt } = UI;
  const brand = new URLSearchParams(location.search).get('brand') || 'bombas';
  const AUTONOMY = { agent_does: 'agent', founder_gate: 'founder_gate', human_assist: 'human_assist' };
  const SEV = { critical: 'high', high: 'high', medium: 'medium', low: 'low' };

  let d;
  try {
    d = await UI.api('/api/' + SLUG + '/?brand=' + encodeURIComponent(brand));
  } catch (e) {
    mount('#tiles', UI.emptyState({ screen: SLUG, title: 'This screen did not load', text: e.message, missing: ['marketplace sales'] }));
    return;
  }

  const name = brand.charAt(0).toUpperCase() + brand.slice(1);
  mount('#badge', el('div', { class: 'sample-badge', role: 'note' },
    el('span', null, el('b', { text: name }), d.simulated === false
      ? ' live data. Read-only.'
      : ' sales on this page are simulated. Nothing here is a ' + name + ' result. Amazon listings and ratings are a real public sample.')));

  if (d.unavailable) {
    mount('#tiles', UI.emptyState({ screen: SLUG, title: 'This screen is unavailable', text: d.reason, missing: [d.fix] }));
    return;
  }

  const findings = d.findings || [];
  const open = findings.filter((f) => f.status === 'open');
  const na = findings.filter((f) => f.status === 'unavailable');
  const L = d.listings;
  mount('#note', UI.founderNote([
    'Marketplace sales come from a monthly total. No seller portal, Buy Box tracker or settlement report is connected, so those checks are unavailable, not zero.',
    'From the public Amazon sample: ' + L.not_buyable + ' of ' + L.asins + ' ASINs cannot be bought right now.',
    open.length + ' finding' + (open.length === 1 ? '' : 's') + ' open. ' + na.length + ' checks wait on a source.'
  ]));

  // ---- tiles
  mount('#tiles', ...d.tiles.map((t) => UI.tile(Object.assign({}, t, { freshness: t.freshness || d.as_of }))));

  // ---- the decision row: the first open finding
  const top = open[0];
  if (top) {
    mount('#decision', el('div', { class: 'card decision-card' },
      el('div', { class: 'tags' },
        el('span', { class: 'chip ' + (top.severity === 'medium' ? 'warn' : 'bad'), text: top.severity }),
        top.money_at_stake ? el('span', { class: 'chip', text: fmt.money(top.money_at_stake.usd) + ' at stake' }) : null,
        el('span', { class: 'chip mono', text: top.capability.id }),
        top.confidence < 0.3 ? el('span', { class: 'chip', text: 'weak evidence' }) : null),
      el('div', { class: 'sentence', text: top.sentence }),
      el('p', { class: 'small muted', text: evidenceText(top) }),
      UI.decisionRow({ capability: top.capability.id, autonomy: AUTONOMY[top.capability.autonomy], screen: SLUG, stub: stub(top) })));
  } else {
    mount('#decision', el('p', { class: 'muted', text: 'Nothing to decide: no rule fired in this window.' }));
  }

  // ---- insights: open findings, each a rule in audit.py
  const firstPerRule = open.filter((f, i) => open.findIndex((g) => g.rule_id === f.rule_id) === i);
  mount('#insights', ...(firstPerRule.length ? firstPerRule : findings.slice(0, 2)).map((f) => UI.insight({
    severity: f.status === 'unavailable' ? 'info' : SEV[f.severity],
    sentence: f.sentence, rule: f.rule_id + ' (see audit.py)' + (open.filter((g) => g.rule_id === f.rule_id).length > 1 ? ', ' + open.filter((g) => g.rule_id === f.rule_id).length + ' findings' : ''),
    evidence: f.status === 'unavailable' ? 'Fix: ' + f.unavailable.fix : evidenceText(f),
    capability: f.capability.id, autonomy: AUTONOMY[f.capability.autonomy], screen: SLUG, stub: stub(f)
  })));

  // ---- chart: marketplace net sales per month, stacked by marketplace
  const c = d.chart;
  const months = c.labels.map((m) => new Date(m + '-15T12:00:00').toLocaleString('en-US', { month: 'short', year: '2-digit' }));
  mount('#chart', Charts.bar({
    title: 'Marketplace net sales per month, ' + months[0] + ' to ' + months[months.length - 1],
    labels: months, unit: '$', stacked: true, series: c.series,
    note: c.unavailable ? 'Unavailable: hatched bars mean no data, not zero. ' + c.unavailable.fix
      : 'Simulated. Net sales by month.' + (c.partial_last ? ' The last month is partial.' : '') +
        (c.not_connected && c.not_connected.length ? ' Not connected: ' + c.not_connected.join(', ') + '.' : '')
  }));

  // ---- Amazon listings
  document.getElementById('listings-sub').textContent = L.asins + ' ASINs from a public sample, not signed in. ' +
    'Amazon reviews in the reviews table: ' + (L.amazon_reviews_in_table == null ? 'unavailable' : L.amazon_reviews_in_table) + '.';
  mount('#listings', UI.table({
    columns: [
      { key: 'asin', label: 'ASIN' }, { key: 'title', label: 'Listing' },
      { key: 'stars', label: 'Stars', format: (v) => v == null ? 'unavailable' : Number(v).toFixed(1) },
      { key: 'ratings', label: 'Ratings', unit: 'n' }, { key: 'price', label: 'Price', unit: '$' },
      { key: 'seller', label: 'Seller shown', format: (v) => v || 'not read' },
      { key: 'problem', label: 'Can it be bought', format: (v, r) => v ? 'no: ' + v : r.buyable ? 'yes' : 'not read' }
    ],
    rows: L.rows, sort: false
  }), el('p', { class: 'small muted', text: 'Source: ' + L.source }));

  // ---- marketplace trust ladder
  const t = d.trust_ladder;
  mount('#trust', t ? el('div', { class: 'card' }, el('p', { text: t.text }),
    el('ul', { class: 'quotes' }, ...t.what_fails.map((q) => el('li', { text: '"' + q + '"' }))),
    el('p', { class: 'small muted', text: 'Brain record ' + t.id + '. Public Amazon reviews, not simulated.' }))
    : el('p', { class: 'muted', text: 'No marketplace trust ladder in the brain yet.' }));

  // ---- checks waiting on data
  mount('#waiting', UI.table({
    columns: [
      { key: 'rule', label: 'Rule' }, { key: 'name', label: 'Check' }, { key: 'severity', label: 'Severity if it fires' },
      { key: 'connector', label: 'Needs' }, { key: 'cap', label: 'Capability' }
    ],
    rows: na.map((f) => ({ rule: f.rule_id, name: f.entity.label, severity: f.severity, connector: f.unavailable.connector,
      cap: f.capability.id })),
    sort: false, empty: 'Every check has its data.'
  }));

  // ---- connectors
  mount('#connectors', ...d.connectors.map((x) => el('span', {
    class: 'chip ' + (x.connected ? 'good' : 'warn'), title: x.fix, text: x.table + ': ' + (x.connected ? 'connected' : 'needs ' + x.connector)
  })));

  function evidenceText(f) {
    const m = f.money_at_stake;
    const money = m ? 'Money at stake ' + fmt.money(m.usd) + ': ' + m.formula + '.' : 'No money figure: ' + (f.money_reason || 'no baseline') + '.';
    const conf = 'Confidence ' + f.confidence + (f.confidence < 0.3 ? ', weak evidence' : '') + '.' +
      (f.first_seen ? ' Open since ' + fmt.date(f.first_seen) + '.' : '');
    return money + ' ' + conf;
  }

  function stub(f) {
    if (f.status === 'unavailable') return 'A person would connect ' + f.unavailable.connector + ' so ' + f.rule_id + ' can run. ' + f.unavailable.fix;
    return 'Working ' + f.capability.id + ' would start from this evidence: ' + f.sentence;
  }
})();
