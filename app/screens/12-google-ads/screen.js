/* 12-google-ads round 0. Everything on the page comes from GET /api/12-google-ads/ (api.py and audit.py).
   The page does no arithmetic beyond formatting; null means unavailable. */
(async function () {
  'use strict';
  const SLUG = '12-google-ads';
  const { el, mount, fmt } = UI;
  const brand = new URLSearchParams(location.search).get('brand') || 'bombas';
  const AUTONOMY = { agent_does: 'agent', founder_gate: 'founder_gate', human_assist: 'human_assist' };
  const SEV = { critical: 'high', high: 'high', medium: 'medium', low: 'low' };
  const TAG = { brand: 'Brand', nonbrand: 'Non-brand' };

  let d;
  try {
    d = await UI.api('/api/' + SLUG + '/?brand=' + encodeURIComponent(brand));
  } catch (e) {
    mount('#tiles', UI.emptyState({ screen: SLUG, title: 'Google Ads data did not load', text: e.message, missing: ['google_ads'] }));
    return;
  }

  const name = brand.charAt(0).toUpperCase() + brand.slice(1);
  mount('#badge', el('div', { class: 'sample-badge', role: 'note' },
    el('span', null, el('b', { text: name }), d.simulated === false
      ? ' live data. Read-only.'
      : ' data on this page is simulated. Nothing here is a ' + name + ' result.')));

  if (d.unavailable) {
    mount('#tiles', UI.emptyState({ screen: SLUG, title: 'Google Ads is unavailable', text: d.reason, missing: [d.fix || 'google_ads'] }));
    return;
  }

  const w = d.window;
  const winLabel = 'last ' + w.days + ' days to ' + fmt.date(w.end);
  document.getElementById('head-sub').textContent = 'Brand and non-brand, search terms, impression share, Performance Max and tracking. ' +
    'Numbers are as Google reports them unless a line says store orders.';

  const findings = d.findings || [];
  const s = d.split;
  mount('#note', UI.founderNote([
    'Google says it made ' + fmt.money(s.total.value) + ' from ' + fmt.money(s.total.spend) + ' in the ' + winLabel + ', ' +
      fmt.unit(s.total.roas, 'x') + '. Your own name carries most of that: brand search returned ' + fmt.unit(s.brand.roas, 'x') +
      ' and everything else ' + fmt.unit(s.nonbrand.roas, 'x') + '.',
    findings.length ? findings.length + ' rules fired. The one with the most money at stake is first.' : 'No rule fired in this window.'
  ]));

  // ---- tiles
  mount('#tiles', ...d.tiles.map((t) => UI.tile(Object.assign({}, t, { window: winLabel, freshness: d.as_of, delta_label: 'vs prior ' + w.days + ' days' }))));

  // ---- the decision row: the top finding
  const top = findings[0];
  if (top) {
    mount('#decision', el('div', { class: 'card decision-card' },
      el('div', { class: 'tags' },
        el('span', { class: 'chip ' + (top.severity === 'medium' ? 'warn' : 'bad'), text: top.severity }),
        top.money_at_stake ? el('span', { class: 'chip', text: fmt.money(top.money_at_stake.usd) + ' at stake' }) : null,
        el('span', { class: 'chip mono', text: top.capability.id })),
      el('div', { class: 'sentence', text: top.sentence }),
      UI.decisionRow({ capability: top.capability.id, autonomy: AUTONOMY[top.capability.autonomy], screen: SLUG, stub: stub(top) })));
  } else {
    mount('#decision', el('p', { class: 'muted', text: 'Nothing to decide: no rule fired in this window.' }));
  }

  // ---- insights: every finding is a rule in audit.py
  mount('#insights', ...findings.map((f) => UI.insight({
    severity: SEV[f.severity], sentence: f.sentence, rule: f.rule_id + ' (see audit.py)',
    evidence: evidenceText(f), capability: f.capability.id, autonomy: AUTONOMY[f.capability.autonomy], screen: SLUG, stub: stub(f)
  })));

  // ---- brand vs non-brand
  const flag = s.brand.incrementality || {};
  document.getElementById('split-sub').textContent = 'Campaigns are tagged by name. Performance Max and Demand Gen count as non-brand; ' +
    'Performance Max can still show on searches for your name, and Google hides those terms.';
  mount('#split',
    UI.table({
      columns: [
        { key: 'label', label: 'Group' }, { key: 'spend', label: 'Spend', unit: '$' }, { key: 'conversions', label: 'Conversions', unit: 'n' },
        { key: 'value', label: 'Value', unit: '$' }, { key: 'roas', label: 'ROAS', unit: 'x' }, { key: 'cpa', label: 'Cost per conversion', unit: '$' },
        { key: 'share_of_spend', label: 'Share of spend', unit: '%' }, { key: 'campaigns', label: 'Campaigns', format: (v) => (v || []).join(', ') }
      ],
      rows: [Object.assign({ label: 'Brand' }, s.brand), Object.assign({ label: 'Non-brand' }, s.nonbrand), Object.assign({ label: 'All Google', share_of_spend: 1, cpa: s.total.conversions ? s.total.spend / s.total.conversions : null }, s.total)],
      sort: false
    }),
    el('div', { class: 'split-flag' },
      el('span', { class: 'chip ' + (flag.flagged ? 'warn' : 'good'), text: flag.flagged ? 'Brand incrementality: untested' : 'Brand incrementality: tested' }),
      ' ', flag.text || '', ' ', el('span', { class: 'muted small', text: 'Rule: ' + (flag.rule || '') })));

  // ---- chart: daily spend or conversions, brand and non-brand
  const c = d.chart;
  const labels = c.labels.map((x) => new Date(x + 'T12:00:00').toLocaleString('en-US', { month: 'short', day: 'numeric' }));
  const chartBox = el('div');
  const draw = (kind) => {
    const unit = kind === 'spend' ? '$' : 'n';
    chartBox.replaceChildren(Charts.line({
      title: (kind === 'spend' ? 'Spend' : 'Conversions') + ' per day, ' + fmt.date(c.window.start) + ' to ' + fmt.date(c.window.end),
      labels, unit, maxLabels: 7,
      series: [{ name: 'Brand', values: c['brand_' + kind] }, { name: 'Non-brand', values: c['nonbrand_' + kind] }],
      note: kind === 'spend' ? 'Google spend by day.' : 'Google conversions by click date. They are not store orders.'
    }));
    seg.querySelectorAll('button').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.kind === kind)));
  };
  const seg = el('div', { class: 'seg', role: 'group', 'aria-label': 'chart measure' },
    el('button', { class: 'btn sm quiet', dataset: { kind: 'spend' }, text: 'Spend', onclick: () => draw('spend') }),
    el('button', { class: 'btn sm quiet', dataset: { kind: 'conversions' }, text: 'Conversions', onclick: () => draw('conversions') }));
  mount('#chart', seg, chartBox);
  draw('spend');

  // ---- conversion tracking check, the gap stated either way
  const t = d.conversion_check;
  if (t.unavailable) {
    mount('#tracking', UI.emptyState({ screen: SLUG, title: 'Tracking check unavailable', text: t.reason, missing: [t.fix] }));
  } else {
    const month = new Date(t.window.end + 'T12:00:00').toLocaleString('en-US', { month: 'long', year: 'numeric' });
    const more = t.conversion_gap < 0 ? 'fewer' : 'more';
    mount('#tracking', el('div', { class: 'card' },
      el('p', { class: 'gap-line', text: 'In ' + month + ' Google counted ' + fmt.int(t.google_conversions) + ' conversions. The store got ' +
        fmt.int(t.store_orders) + ' orders from paid search. Google counted ' + fmt.pct(Math.abs(t.conversion_gap)) + ' ' + more + '.' }),
      el('p', { class: 'gap-line', text: 'Google valued a conversion at ' + fmt.money(t.google_value_per_conversion) + '. A paid search order was worth ' +
        fmt.money(t.store_aov) + ' net of discounts, before tax and shipping. Gap: ' + fmt.pct(t.value_per_conversion_gap) + '.' }),
      el('p', { class: 'small muted', text: t.basis + ' A gap of ' + fmt.pct(0.1) + ' or more on either line is a finding.' })));
  }

  // ---- impression share
  mount('#is', UI.table({
    columns: [
      { key: 'campaign', label: 'Campaign' }, { key: 'tag', label: 'Group', format: (v) => TAG[v] || 'unavailable' },
      { key: 'impression_share', label: 'Impression share', unit: '%' }, { key: 'lost_is_budget', label: 'Lost to budget', unit: '%' },
      { key: 'lost_is_rank', label: 'Lost to rank', unit: '%' }, { key: 'clipped_days', label: 'Days over 90%', unit: 'n' },
      { key: 'reason', label: 'Note', format: (v, r) => v || r.note || '' }
    ],
    rows: d.impression_share, sort: false
  }));

  // ---- search terms
  const ts = d.search_terms.summary;
  document.getElementById('terms-sub').textContent = ts.new_keywords + ' terms to add as keywords, ' + ts.negatives + ' to add as negatives. ' +
    'Negative: ' + ts.rules.negative + '. New keyword: ' + ts.rules['new keyword'] + '. ' + ts.note;
  const chip = (v) => el('span', { class: 'chip ' + (v === 'negative' ? 'bad' : v === 'new keyword' ? 'good' : ''), text: v });
  const termsTable = UI.table({
    columns: [
      { key: 'term', label: 'Search term' }, { key: 'campaign', label: 'Campaign' }, { key: 'status', label: 'Keyword', format: (v) => v === 'ADDED' ? 'yes' : 'no' },
      { key: 'spend', label: 'Spend', unit: '$' }, { key: 'clicks', label: 'Clicks', unit: 'n' }, { key: 'conversions', label: 'Conversions', unit: 'n' },
      { key: 'cpa', label: 'Cost per conversion', unit: '$' }, { key: 'campaign_cpa', label: 'Campaign cost per conversion', unit: '$' },
      { key: 'action', label: 'Rule says' }, { key: 'why', label: 'Why' }
    ],
    rows: d.search_terms.rows, sort: { key: 'spend', dir: 'desc' }
  });
  mount('#terms', termsTable);
  paintChips(termsTable, chip);

  // ---- Performance Max asset groups
  mount('#assets', UI.table({
    columns: [
      { key: 'asset_group', label: 'Asset group' }, { key: 'campaign', label: 'Campaign' }, { key: 'ad_strength', label: 'Ad strength today' },
      { key: 'strength_days', label: 'Days by strength', format: (v) => Object.entries(v || {}).map(([k, n]) => k.toLowerCase() + ' ' + n).join(', ') },
      { key: 'spend', label: 'Spend', unit: '$' }, { key: 'conversions', label: 'Conversions', unit: 'n' }, { key: 'reason', label: 'Note' }
    ],
    rows: d.asset_groups, sort: false, empty: 'No Performance Max asset groups in this window.'
  }));

  function evidenceText(f) {
    const m = f.money_at_stake;
    const money = m ? 'Money at stake ' + fmt.money(m.usd) + ': ' + m.formula + '.' + (m.note ? ' ' + m.note[0].toUpperCase() + m.note.slice(1) + '.' : '')
      : 'No money figure: ' + (f.money_reason || 'no baseline') + '.';
    const conf = 'Confidence ' + f.confidence + (f.confidence < 0.3 ? ', weak evidence' : '') + '. Open since ' + fmt.date(f.first_seen) + '.';
    return money + ' ' + conf;
  }

  function stub(f) {
    return 'A person working ' + f.capability.id + ' would pick this up with the evidence: ' + f.sentence;
  }

  // The kit table renders text cells; the rule column gets a chip after render and after each sort.
  function paintChips(wrap, make) {
    const col = [...wrap.querySelectorAll('thead th')].findIndex((th) => th.textContent.startsWith('Rule says'));
    const paint = () => wrap.querySelectorAll('tbody tr').forEach((tr) => {
      const td = tr.children[col];
      if (td && !td.querySelector('.chip')) { const v = td.textContent; td.replaceChildren(make(v)); }
    });
    paint();
    new MutationObserver(paint).observe(wrap, { childList: true, subtree: true });
  }
})();
