/* 13-affiliate-marketplace-ads round 0. Everything on the page comes from GET /api/13-affiliate-marketplace-ads/
   (api.py and audit.py). The page does no arithmetic beyond formatting; null means unavailable. */
(async function () {
  'use strict';
  const SLUG = '13-affiliate-marketplace-ads';
  const { el, mount, fmt } = UI;
  const brand = new URLSearchParams(location.search).get('brand') || 'bombas';
  const AUTONOMY = { agent_does: 'agent', founder_gate: 'founder_gate', human_assist: 'human_assist' };
  const SEV = { critical: 'high', high: 'high', medium: 'medium', low: 'low' };

  let d;
  try {
    d = await UI.api('/api/' + SLUG + '/?brand=' + encodeURIComponent(brand));
  } catch (e) {
    mount('#tiles', UI.emptyState({ screen: SLUG, title: 'This screen did not load', text: e.message, missing: ['affiliate network'] }));
    return;
  }

  const name = brand.charAt(0).toUpperCase() + brand.slice(1);
  mount('#badge', el('div', { class: 'sample-badge', role: 'note' },
    el('span', null, el('b', { text: name }), d.simulated === false
      ? ' live data. Read-only.'
      : ' data on this page is simulated. Nothing here is a ' + name + ' result. The Amazon listings are a real public sample.')));

  if (d.unavailable) {
    mount('#tiles', UI.emptyState({ screen: SLUG, title: 'This screen is unavailable', text: d.reason, missing: [d.fix] }));
    return;
  }

  const w = d.window;
  const winLabel = 'last ' + w.days + ' days to ' + fmt.date(w.end);
  const findings = d.findings || [];
  const open = findings.filter((f) => f.status === 'open');
  const na = findings.filter((f) => f.status === 'unavailable');
  const a = d.amazon;
  mount('#note', UI.founderNote([
    'No affiliate network or Amazon Ads account is connected, so partner, fraud and ad numbers are unavailable, not zero.',
    'What we can see is public: ' + a.resold_in_stock + ' of ' + a.in_stock + ' in-stock Amazon listings in a sample of ' +
      a.asins_read + ' are sold by resellers, and no brand store showed.',
    open.length + ' rule' + (open.length === 1 ? '' : 's') + ' fired. ' + na.length + ' cannot run until a source is connected.'
  ]));

  // ---- tiles
  mount('#tiles', ...d.tiles.map((t) => UI.tile(Object.assign({}, t, {
    window: t.id === 'amazon_reseller_share' ? 'public sample' : winLabel, freshness: t.freshness || d.as_of
  }))));

  // ---- the decision row: the first open finding, else the first finding
  const top = open[0] || findings[0];
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

  // ---- insights: every finding is a rule in audit.py
  mount('#insights', ...findings.map((f) => UI.insight({
    severity: f.status === 'unavailable' ? 'info' : SEV[f.severity],
    sentence: f.sentence, rule: f.rule_id + ' (see audit.py)' + (f.status === 'unavailable' ? ', unavailable' : ''),
    evidence: f.status === 'unavailable' ? 'Fix: ' + f.unavailable.fix : evidenceText(f),
    capability: f.capability.id, autonomy: AUTONOMY[f.capability.autonomy], screen: SLUG, stub: stub(f)
  })));

  // ---- chart: affiliate orders by partner type, or the unavailable state drawn
  const c = d.chart;
  const months = c.labels.map((m) => new Date(m + '-15T12:00:00').toLocaleString('en-US', { month: 'short', year: '2-digit' }));
  mount('#chart', Charts.bar({
    title: 'Affiliate orders per month by partner type, ' + months[0] + ' to ' + months[months.length - 1],
    labels: months, unit: 'n', stacked: true, series: c.series,
    note: c.unavailable ? 'Unavailable: hatched bars mean no data, not zero. ' + c.unavailable.fix
      : 'Orders the network credits, by order month.' + (c.partial_last ? ' The last month is partial.' : '')
  }));

  // ---- affiliate partners
  const p = d.partners;
  document.getElementById('partners-sub').textContent = 'Fraud flags by rule. Fast: ' + p.rules.fast + '. No clicks: ' +
    p.rules.no_click + '. Code leak: ' + p.rules.leak + '.';
  if (p.unavailable) {
    mount('#partners', naCard('Partner table unavailable', 'Columns: partner, type, clicks, orders, sales, rate, commission, fraud flags.', p.unavailable));
  } else {
    mount('#partners', UI.table({
      columns: [
        { key: 'name', label: 'Partner' }, { key: 'partner_type', label: 'Type' }, { key: 'clicks', label: 'Clicks', unit: 'n' },
        { key: 'orders', label: 'Orders', unit: 'n' }, { key: 'sales', label: 'Sales', unit: '$' }, { key: 'cvr', label: 'Orders per click', unit: '%' },
        { key: 'rate', label: 'Rate', unit: '%' }, { key: 'commission', label: 'Commission', unit: '$' },
        { key: 'flags', label: 'Fraud flags', format: (v) => (v || []).join('; ') || 'none' }
      ],
      rows: p.rows, sort: { key: 'sales', dir: 'desc' }, empty: 'No affiliate activity in this window.'
    }));
  }

  // ---- commission tiers
  const t = d.commission_tiers;
  mount('#tiers',
    t.unavailable ? naCard('No commission tier record', 'The grid below is the shape. Every rate is unavailable until the record exists.', t.unavailable) : null,
    UI.table({
      columns: [
        { key: 'partner_type', label: 'Partner type' }, { key: 'new_rate', label: 'New customer rate', unit: '%' },
        { key: 'returning_rate', label: 'Returning customer rate', unit: '%' }, { key: 'partners', label: 'Partners', unit: 'n' }
      ],
      rows: t.rows, sort: false
    }));

  // ---- Amazon
  document.getElementById('amazon-sub').textContent = a.presence_text + ' Read ' + fmt.date(a.captured_at) + '. ' +
    'Lines not found: ' + (a.lines_not_found.join(', ') || 'none') + '.';
  mount('#amazon',
    a.ads.unavailable ? naCard('Sponsored Products unavailable', 'Spend, ad sales and ACoS per ASIN fill from the Amazon Ads report.', a.ads) : null,
    UI.table({
      columns: [
        { key: 'asin', label: 'ASIN' }, { key: 'title', label: 'Listing' }, { key: 'in_stock', label: 'In stock', format: (v) => v ? 'yes' : 'no' },
        { key: 'seller', label: 'Seller shown', format: (v, r) => v ? v + (r.sold_by === 'reseller' ? ' (reseller)' : '') : 'none shown' },
        { key: 'price', label: 'Price', unit: '$' },
        { key: 'rating', label: 'Rating', format: (v) => v == null ? 'unavailable' : v.toFixed(1) }, { key: 'ratings', label: 'Ratings', unit: 'n' },
        { key: 'spend', label: 'Ad spend', unit: '$' }, { key: 'ad_sales', label: 'Ad sales', unit: '$' }, { key: 'acos', label: 'ACoS', unit: '%' }
      ],
      rows: a.listings, sort: false
    }),
    el('p', { class: 'small muted', text: 'Source: ' + a.source }));

  // ---- retail media placeholder
  document.getElementById('retail-sub').textContent = d.retail_media.note;
  mount('#retail', UI.table({
    columns: [
      { key: 'platform', label: 'Platform' }, { key: 'network', label: 'Ads network' },
      { key: 'in_brain', label: 'Brain mentions the brand there', format: (v, r) => v ? 'yes (' + r.brain_refs.length + ' records)' : 'no' },
      { key: 'brief_status', label: 'Brief status', format: (v) => v || 'unavailable' },
      { key: 'reported_roas', label: 'Reported ROAS', unit: 'x' }, { key: 'reason', label: 'Why unavailable' }
    ],
    rows: d.retail_media.rows, sort: false
  }));

  // ---- billing reconciliation
  const b = d.billing;
  mount('#billing', UI.tile({
    name: 'Network invoice vs tracked orders', plain: 'what the network bills minus commission on orders we can see',
    value: b.unavailable ? null : b.gap, unit: '$',
    unavailable_reason: b.unavailable ? 'No invoice source yet. ' + (b.fix || '') : null,
    fix: b.unavailable ? b.connector : null, window: b.cycle || 'per payout cycle', freshness: d.as_of
  }));

  // ---- connectors
  mount('#connectors', ...d.connectors.map((x) => el('span', {
    class: 'chip ' + (x.connected ? 'good' : 'warn'), title: x.fix, text: x.table + ': ' + (x.connected ? 'connected' : 'needs ' + x.connector)
  })));

  function naCard(title, text, u) {
    return el('div', { class: 'card na-card' }, el('h4', { text: title }), el('p', { text: text }),
      el('p', { class: 'small muted', text: 'Needs ' + u.connector + '. ' + u.fix }));
  }

  function evidenceText(f) {
    const m = f.money_at_stake;
    const money = m ? 'Money at stake ' + fmt.money(m.usd) + ': ' + m.formula + '.' : 'No money figure: ' + (f.money_reason || 'no baseline') + '.';
    const conf = 'Confidence ' + f.confidence + (f.confidence < 0.3 ? ', weak evidence' : '') + '.' +
      (f.first_seen ? ' Open since ' + fmt.date(f.first_seen) + '.' : '');
    return money + ' ' + conf;
  }

  function stub(f) {
    if (f.status === 'unavailable') return 'A person would connect ' + f.unavailable.connector + ' so ' + f.rule_id + ' can run. ' + f.unavailable.fix;
    return 'A person working ' + f.capability.id + ' would pick this up with the evidence: ' + f.sentence;
  }
})();
