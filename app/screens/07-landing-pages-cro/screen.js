/* Landing pages and CRO: funnel by device with the break per device, money at stake by device,
   conversion by device for 12 weeks, funnel by source, ad-to-page message match, the page registry,
   the PDP objection-proof map, the test registry, 3 tiles, 2 insights and the findings.
   Data from /api/07-landing-pages-cro/summary. Decisions go through the kit's /api/decisions. */
(function () {
  const { el, mount, fmt } = UI;
  const API = '/api/07-landing-pages-cro/';

  function head(id) { return document.querySelector('#' + id + ' h3'); }
  function fill(id, ...nodes) { mount('#' + id, head(id), ...nodes); }
  const pct = (v) => fmt.pct(v);
  const note = (text) => el('p', { class: 'small muted', text });
  const autonomy = (a) => (a === 'agent_does' ? 'agent' : a);
  const shortDay = (iso) => new Date(iso + 'T12:00:00').toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  const STATUS_TONE = { match: 'good', mismatch: 'bad', 'not checked': '', 'no proof': 'bad', 'on the PDP': 'good',
    'proof exists, PDP not captured': 'warn', 'proof exists, not on the PDP': 'warn' };
  const chip = (text, tone) => el('span', { class: 'chip' + (tone ? ' ' + tone : ''), text });

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

  function device(d) {
    const f = d.funnel_device;
    if (f.unavailable) return fill('device', UI.emptyState({ title: 'The funnel by device is unavailable', text: f.reason, missing: [f.fix || 'ga4'] }));
    const cards = f.rows.map((r) => {
      const brk = r.steps.find((s) => s.step === r.break_step);
      return el('div', { class: 'card dev' + (brk ? ' break' : '') },
        el('div', { class: 'row' }, el('b', { text: r.label }), brk ? chip('Break: ' + brk.label.toLowerCase(), 'bad') : chip('No break', 'good')),
        el('div', { class: 'small muted', text: fmt.int(r.sessions) + ' sessions, ' + pct(r.conversion_rate) + ' convert' }),
        el('div', { class: 'steps' }, r.steps.map((s) => el('div', { class: 'step' + (s.step === r.break_step ? ' is-break' : '') },
          el('span', { class: 'l', text: s.label }),
          el('span', { class: 'v', text: pct(s.current) }),
          el('span', { class: 'm', text: 'median ' + pct(s.median) })))),
        el('div', { class: 'money', text: brk ? fmt.money(brk.money) + ' at stake at the break' : 'Nothing at stake' }),
        r.money && brk && r.money > brk.money ? el('div', { class: 'small muted', text: fmt.money(r.money) + ' across every step below its median' }) : null);
    });
    fill('device', el('div', { class: 'devs' }, cards),
      note(f.basis + ' Stake = (median rate minus current rate) x shoppers entering the step x value per shopper downstream (later step rates x AOV ' + fmt.money(f.aov) + '). Rates are GA4 event counts.'));
  }

  function chart(d) {
    const c = d.chart;
    if (c.unavailable) return fill('chart', UI.emptyState({ title: 'The weekly chart is unavailable', text: c.reason }));
    fill('chart', el('div', { class: 'card' }, Charts.line({ labels: c.labels.map(shortDay), series: c.series, unit: '%',
      note: 'GA4 purchases per session, 7 days ending on each date. Simulated.' })));
  }

  function source(d) {
    const f = d.funnel_source;
    if (f.unavailable) return fill('source', UI.emptyState({ title: 'The funnel by source is unavailable', text: f.reason }));
    fill('source', UI.table({
      columns: [{ key: 'source', label: 'Source' }, { key: 'sessions', label: 'Sessions', unit: 'n' },
        { key: 'add_to_cart_rate', label: 'Add to cart', unit: '%' }, { key: 'checkout_rate', label: 'Cart to checkout', unit: '%' },
        { key: 'purchase_rate', label: 'Checkout to order', unit: '%' }, { key: 'conversion_rate', label: 'Conversion', unit: '%' }],
      rows: f.rows, sort: { key: 'sessions', dir: 'desc' } }), note('GA4 default channel groups, last 28 days. ' + (f.basis || '')));
  }

  function match(d) {
    const m = d.message_match;
    if (m.unavailable) return fill('match', UI.emptyState({ title: 'Message match is unavailable', text: m.reason }));
    fill('match', el('div', { class: 'cards' }, m.rows.map((r) => el('div', { class: 'card' },
      el('div', { class: 'row' }, el('b', { class: 'mono', text: r.page }),
        r.captured ? chip('Match ' + pct(r.score), r.score === 1 ? 'good' : 'bad') : chip('Page not captured', 'warn')),
      el('div', { class: 'small muted', text: fmt.int(r.sessions) + ' paid social sessions, ' + pct(r.conversion_rate) + ' convert, median ' + pct(r.median) }),
      el('ul', { class: 'elements' }, r.elements.map((e) => el('li', null,
        chip(e.status, STATUS_TONE[e.status]), ' ', el('b', { text: e.element + ': ' }), e.words,
        e.page_says ? el('div', { class: 'small muted', text: 'Page: ' + e.page_says }) : null,
        e.status === 'mismatch' ? el('div', { class: 'small muted', text: e.elsewhere ? 'Found elsewhere on the site: ' + e.elsewhere : 'No captured page on the site carries it.' }) : null)))))),
    note(m.rule + ' Ad side: the brain\'s Ad Library records. The ad table has no copy or landing URL, so the lander comes from GA4 paid social sessions.'));
  }

  function registry(d) {
    const r = d.registry;
    fill('registry', UI.table({
      columns: [{ key: 'page', label: 'Page' }, { key: 'type', label: 'Type' }, { key: 'type_from', label: 'Type from' },
        { key: 'captured', label: 'In brain', format: (v) => (v ? 'yes' : 'no') },
        { key: 'sessions', label: 'Sessions', unit: 'n' }, { key: 'add_to_cart_rate', label: 'Add to cart', unit: '%' },
        { key: 'conversion_rate', label: 'Conversion', unit: '%' }, { key: 'lcp_ms', label: 'Mobile LCP', unit: 'ms' }],
      rows: r.rows, sort: false }),
    note('Pages from the brain site map plus every landing page with sessions in 28 days. Funnel rates only where the page is a landing page.' +
      (r.speed_note ? ' Speed is unavailable: ' + r.speed_note + '.' : '')));
  }

  function proof(d) {
    const p = d.proof_map;
    const lead = 'PDP: ' + (p.pdp || 'none with sessions') + '. ' + p.with_proof + ' of ' + p.rungs + ' objection rungs have proof somewhere on the site. ' +
      (p.proof_placement_coverage == null ? 'Placement on the PDP is unknown: ' + p.coverage_reason + '.' : pct(p.proof_placement_coverage) + ' of rungs have proof on the PDP.');
    fill('proof', el('p', { text: lead }), UI.table({
      columns: [{ key: 'ladder', label: 'Objection' }, { key: 'level', label: 'Rung', align: 'right' }, { key: 'doubt', label: 'The doubt' },
        { key: 'one_star', label: '1-star mentions', unit: 'n' }, { key: 'status', label: 'Proof' },
        { key: 'proof_pages', label: 'Where the proof lives', format: (v) => (v && v.length ? v.join(', ') : 'none') }],
      rows: p.rows, sort: false }), note('From the brain objection ladders. A rung with "no public proof" counts as no proof.'));
  }

  function tests(d) {
    const t = d.tests;
    const ex = t.example;
    fill('tests', el('p', { class: 'small', text: t.note }),
      UI.table({ columns: t.fields.map((f) => ({ key: f.key, label: f.label })), rows: t.tests, sort: false, empty: 'No tests yet.' }),
      el('ul', { class: 'rules small' }, t.fields.filter((f) => f.rule).map((f) => el('li', null, el('b', { text: f.label + ': ' }), f.rule))),
      ex ? el('div', { class: 'card small' }, el('b', { text: 'Worked example. ' }),
        'To detect a ' + pct(ex.mde) + ' lift on ' + ex.metric + ' (now ' + pct(ex.baseline) + ') needs ' + fmt.int(ex.sample_per_arm) +
        ' sessions per arm. At ' + fmt.int(ex.daily_sessions) + ' mobile sessions a day that is ' + ex.days_to_sample + ' day' + (ex.days_to_sample === 1 ? '' : 's') +
        ', so the read date is ' + ex.read_after_days + ' days after launch.') : null);
  }

  function findings(d) {
    if (!d.findings.length) return fill('findings', el('p', { class: 'muted', text: 'No findings this window.' }));
    fill('findings', note('What audit.py returns, in the shape Propose will read. Sorted by severity, then money.'),
      UI.table({
        columns: [{ key: 'severity', label: 'Severity' }, { key: 'entity', label: 'On' }, { key: 'rule_id', label: 'Rule' }, { key: 'status', label: 'Status' },
          { key: 'usd', label: 'At stake', unit: '$', format: (v) => (v == null ? 'none' : fmt.money(v)) },
          { key: 'confidence', label: 'Confidence', align: 'right', format: (v) => v.toFixed(1) }, { key: 'capability', label: 'Fix' }, { key: 'sentence', label: 'What it says' }],
        rows: d.findings.map((f) => ({ severity: f.severity, entity: f.entity.label, rule_id: f.rule_id, status: f.status,
          usd: f.money_at_stake ? f.money_at_stake.usd : null, confidence: f.confidence, capability: f.capability.id, sentence: f.sentence })),
        sort: false }));
  }

  async function load() {
    let d;
    try { d = await UI.api(API + 'summary?window=28d'); } catch (e) {
      return fill('tiles', UI.emptyState({ title: 'Landing pages and CRO could not load', text: e.message }));
    }
    const b = d.brand || {};
    document.getElementById('simulated').textContent = (b.name || 'This brand') + ': simulated data, shaped from public information. Nothing here is a real ' +
      (b.name || '') + ' result. Last full day ' + fmt.date(b.as_of) + '.';
    for (const [fn, id] of [[tiles, 'tiles'], [insights, 'insights'], [device, 'device'], [chart, 'chart'], [source, 'source'], [match, 'match'],
      [registry, 'registry'], [proof, 'proof'], [tests, 'tests'], [findings, 'findings']]) {
      try { fn(d); } catch (e) { fill(id, UI.emptyState({ title: 'This block could not render', text: e.message })); }
    }
  }
  load();
})();
