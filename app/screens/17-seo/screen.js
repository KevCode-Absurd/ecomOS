/* SEO: 3 tiles, 2 insights, organic sessions and search clicks for 12 weeks, the query table against
   the CTR curve, organic landing pages and the findings (with what each missing connector blocks).
   Data from /api/17-seo/summary. Decisions go through the kit's /api/decisions. */
(function () {
  const { el, mount, fmt } = UI;
  const API = '/api/17-seo/';

  function head(id) { return document.querySelector('#' + id + ' h3'); }
  function fill(id, ...nodes) { mount('#' + id, head(id), ...nodes); }
  const pct = (v) => fmt.pct(v);
  const note = (text) => el('p', { class: 'small muted', text });
  const autonomy = (a) => (a === 'agent_does' ? 'agent' : a);
  const shortDay = (iso) => new Date(iso + 'T12:00:00').toLocaleDateString('en-US', { month: 'short', day: 'numeric' });

  function tiles(d) {
    fill('tiles', el('div', { class: 'grid tiles' }, d.tiles.map((t) => UI.tile(Object.assign({}, t, { delta_label: 'vs prior 28 days' })))));
  }

  function insights(d) {
    fill('insights', ...d.insights.map((i) => {
      if (!i.sentence) return UI.insight({ sentence: i.quiet, rule: i.rule, severity: 'info' });
      return UI.insight({ sentence: i.sentence, rule: i.rule, severity: i.severity, capability: i.capability, autonomy: autonomy(i.autonomy),
        evidence: (i.money != null ? fmt.money(i.money) + ' at stake in 28 days. ' : '') + 'Confidence ' + i.confidence.toFixed(1) + '. Finding ' + i.finding + '.' });
    }));
  }

  function chart(d) {
    const c = d.chart;
    if (c.unavailable) return fill('chart', UI.emptyState({ title: 'The weekly chart is unavailable', text: c.reason }));
    fill('chart', el('div', { class: 'card' }, Charts.line({ labels: c.labels.map(shortDay), series: c.series, unit: 'n',
      note: '7 days ending on each date. Weeks outside what Search Console covers read unavailable. Simulated.' })));
  }

  function queries(d) {
    const q = d.queries;
    if (q.unavailable) return fill('queries', UI.emptyState({ title: 'Search Console is not connected', text: q.reason, missing: [q.fix] }));
    fill('queries', UI.table({
      columns: [{ key: 'query', label: 'Query' }, { key: 'page', label: 'Page' }, { key: 'group', label: 'Type' },
        { key: 'impressions', label: 'Impressions', unit: 'n' }, { key: 'clicks', label: 'Clicks', unit: 'n' },
        { key: 'position', label: 'Position', align: 'right', format: (v) => v.toFixed(1) },
        { key: 'ctr', label: 'CTR', unit: '%' }, { key: 'expected_ctr', label: 'Curve CTR', unit: '%' },
        { key: 'gap', label: 'Gap', align: 'right', format: (v) => (v > 0 ? '+' : '') + Math.round(v * 100) + '%' }],
      rows: q.rows.map((r) => Object.assign({}, r, { group: r.branded ? 'branded' : 'non-branded' })), sort: { key: 'impressions', dir: 'desc' } }),
    note('Search Console, ' + fmt.date(q.start) + ' to ' + fmt.date(q.end) + '. Curve CTR is the click rate a page at that position usually gets; branded queries get twice the non-branded curve. A gap of minus 30% or worse on a top query fires SEO-R02.'));
  }

  function pages(d) {
    const p = d.landing_pages;
    if (p.unavailable) return fill('pages', UI.emptyState({ title: 'Organic landing pages are unavailable', text: p.reason }));
    fill('pages', UI.table({
      columns: [{ key: 'landing_page', label: 'Landing page' }, { key: 'sessions', label: 'Organic sessions', unit: 'n' },
        { key: 'add_to_cart_rate', label: 'Add to cart', unit: '%' }, { key: 'conversion_rate', label: 'Conversion', unit: '%' }],
      rows: p.rows, sort: { key: 'sessions', dir: 'desc' } }),
    note('GA4 sessions where the channel group is Organic Search, last 28 days. Conversion is GA4 purchases per session, not order-matched revenue.'));
  }

  function findings(d) {
    const open = d.findings.filter((f) => f.status !== 'unavailable');
    const missing = d.findings.filter((f) => f.status === 'unavailable');
    fill('findings', note('What audit.py returns, in the shape Propose will read. Sorted by severity, then money.'),
      UI.table({
        columns: [{ key: 'severity', label: 'Severity' }, { key: 'entity', label: 'On' }, { key: 'rule_id', label: 'Rule' },
          { key: 'usd', label: 'At stake', unit: '$', format: (v) => (v == null ? 'none' : fmt.money(v)) },
          { key: 'confidence', label: 'Confidence', align: 'right', format: (v) => v.toFixed(1) }, { key: 'capability', label: 'Fix' }, { key: 'sentence', label: 'What it says' }],
        rows: open.map((f) => ({ severity: f.severity, entity: f.entity.label, rule_id: f.rule_id, usd: f.money_at_stake ? f.money_at_stake.usd : null,
          confidence: f.confidence, capability: f.capability.id, sentence: f.sentence })),
        sort: false, empty: 'No open findings this window.' }),
      el('h4', { text: 'Rules waiting on data (' + missing.length + ')' }),
      UI.table({
        columns: [{ key: 'rule_id', label: 'Rule' }, { key: 'name', label: 'What it checks' }, { key: 'severity', label: 'Severity if it fires' },
          { key: 'connector', label: 'Needs' }, { key: 'capability', label: 'Fix' }],
        rows: missing.map((f) => ({ rule_id: f.rule_id, name: f.entity.label, severity: f.severity, connector: f.unavailable.connector, capability: f.capability.id })),
        sort: false }));
  }

  async function load() {
    let d;
    try { d = await UI.api(API + 'summary?window=28d'); } catch (e) {
      return fill('tiles', UI.emptyState({ title: 'SEO could not load', text: e.message }));
    }
    const b = d.brand || {};
    document.getElementById('simulated').textContent = (b.name || 'This brand') + ': simulated data, shaped from public information. Nothing here is a real ' +
      (b.name || '') + ' result. Last full day ' + fmt.date(b.as_of) + '.';
    for (const [fn, id] of [[tiles, 'tiles'], [insights, 'insights'], [chart, 'chart'], [queries, 'queries'], [pages, 'pages'], [findings, 'findings']]) {
      try { fn(d); } catch (e) { fill(id, UI.emptyState({ title: 'This block could not render', text: e.message })); }
    }
  }
  load();
})();
