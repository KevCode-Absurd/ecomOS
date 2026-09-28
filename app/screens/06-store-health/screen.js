/* Store health, round 0. Reads /api/06-store-health/overview and composes kit components.
   No numbers are computed here; the server sends every value, rule and sentence. */
(function () {
  'use strict';
  const SLUG = '06-store-health';
  const { el, fmt } = UI;
  const brand = new URLSearchParams(location.search).get('brand') || 'bombas';
  const AUTONOMY_KIT = { agent_does: 'agent', founder_gate: 'founder_gate', human_assist: 'human_assist', agent: 'agent' };
  const STATUS = { pass: 'good', fail: 'bad', unavailable: '' };
  const SOURCE = { site: 'Site', ad_library: 'Meta Ad Library', press: 'Press', review: 'Reviews', interview: 'Interview' };

  function section(title, ...children) {
    return el('section', { class: 'section' }, el('h3', { text: title }), ...children);
  }

  function simBanner(b) {
    const name = b.name || b.brand || 'This brand';
    if (!b.simulated) return el('div', { class: 'sim', role: 'note' }, el('b', { text: name }), ' live data. Read-only.');
    return el('div', { class: 'sim', role: 'note' }, el('b', { text: name }),
      ': simulated data. Stack, policies and site facts come from public pages; every order, return and chargeback is generated. Nothing here is a ' + name + ' result.');
  }

  function tile(t) {
    const src = (t.sources || []).map((s) => s.table).join(', ');
    return UI.tile(Object.assign({}, t, { freshness: t.freshness ? fmt.date(t.freshness) + (src ? ' from ' + src : '') : null }));
  }

  function pct(v, d) { return v == null ? 'unavailable' : (v * 100).toFixed(d == null ? 1 : d) + ' percent'; }
  function per1k(v) { return v == null ? 'unavailable' : v.toFixed(1) + ' per 1,000 orders'; }
  function kv(pairs) {
    return el('dl', { class: 'kv' }, pairs.filter(Boolean).flatMap(([k, v]) => [el('dt', { text: k }), el('dd', { text: v })]));
  }

  function srcText(s) {
    if (!s) return '';
    if (s.kind === 'brain') return 'Brain ' + s.ref + (s.type ? ', ' + (SOURCE[s.type] || s.type) : '') + (s.seen ? ', seen ' + s.seen : '');
    return 'Table ' + s.ref;
  }

  function checklist(items) {
    const groups = [];
    items.forEach((i) => { let g = groups.find((x) => x.name === i.group); if (!g) groups.push(g = { name: i.group, items: [] }); g.items.push(i); });
    return el('div', { class: 'card' }, groups.map((g) => el('div', null,
      el('div', { class: 'check-group', text: g.name }),
      g.items.map((i) => el('div', { class: 'check' },
        el('div', null, el('span', { class: 'chip ' + STATUS[i.status], text: i.status })),
        el('div', { class: 'body' },
          el('div', { class: 'label', text: i.label }),
          el('div', { class: 'detail', text: i.detail }),
          el('div', { class: 'src', text: srcText(i.source) + ' · ' + i.capability + (i.connector ? ' · needs ' + i.connector : '') })))))));
  }

  function legs(r) {
    const ret = r.returns, rts = r.return_to_sender, cb = r.chargebacks;
    const retCard = el('div', { class: 'card leg' }, el('h4', { text: 'Returns' }),
      ret.unavailable ? el('p', { class: 'th', text: 'Unavailable: ' + ret.reason + '.' }) : kv([
        ['Returns, 28 days', fmt.int(ret.returns)],
        ['Rate', per1k(ret.per_1000)],
        ['Own median', per1k(ret.median_per_1000)],
        ['Refunded', fmt.money(ret.refunded)],
        ['Top reason', ret.by_reason.length ? ret.by_reason[0].reason + ', ' + pct(ret.by_reason[0].share, 0) : 'none'],
      ]));
    const rtsCard = el('div', { class: 'card leg' }, el('h4', { text: 'Return to sender' }),
      rts.unavailable ? el('p', { class: 'th', text: 'Unavailable: ' + rts.reason + '.' }) : el('div', null, kv([
        ['Carrier returns, 28 days', fmt.int(rts.returned)],
        ['Rate', per1k(rts.per_1000)],
        r.cod_market ? ['Return to origin', pct(r.return_to_origin, 2)] : null,
      ]), el('p', { class: 'th', text: rts.basis + '.' })));
    const cbCard = el('div', { class: 'card leg' }, el('h4', { text: 'Chargebacks and disputes' }),
      cb.unavailable ? el('p', { class: 'th', text: 'Unavailable: ' + cb.reason + '.' }) : kv([
        ['Chargebacks, 30 days', fmt.int(cb.chargebacks) + ' (' + pct(cb.rate, 2) + ')'],
        ['Line', pct(cb.benchmark, 1) + (cb.own != null ? '; your 90 days before ' + pct(cb.own, 2) : '')],
        ['Disputed', cb.amount == null ? 'unavailable' : fmt.money(cb.amount)],
        ['Won, closed in 28 days', cb.win_rate == null ? 'unavailable' : pct(cb.win_rate, 0) + ' of ' + fmt.int(cb.closed)],
        ['Open now', cb.open == null ? 'unavailable' : fmt.int(cb.open) + ' (' + fmt.money(cb.open_amount) + '), ' + fmt.int(cb.inquiries_open) + ' of them inquiries'],
        ['Open ' + cb.dispute_days + '+ days', cb.aged == null ? 'unavailable' : fmt.int(cb.aged) + ' (' + fmt.money(cb.aged_amount) + ')'],
        cb.payouts ? ['Payouts, 28 days', 'adjustments ' + fmt.money(cb.payouts.adjustments_gross) + ', refunds ' + fmt.money(cb.payouts.refunds_gross)] : null,
      ]));
    return el('div', null,
      el('p', { class: 'th', text: 'Counted in the simulated order table, so the counts are a sample and the rates are the part to read.' + (r.cod_market ? '' : ' Cash on delivery legs are off for a US store.') }),
      el('div', { class: 'legs' }, retCard, rtsCard, cbCard));
  }

  function payments(p) {
    if (p.unavailable) return UI.emptyState({ screen: SLUG, title: 'No payment data', text: p.reason, missing: [p.fix] });
    return el('div', null,
      el('p', { class: 'th', text: fmt.int(p.orders) + ' paid orders, ' + p.window.start + ' to ' + p.window.end + '. Card ' + pct(p.groups.card) + ', wallets ' + pct(p.groups.wallet) +
        ', buy now pay later ' + (p.bnpl_offered ? pct(p.groups.bnpl) : 'none seen') + '.' }),
      UI.table({ columns: [
        { key: 'method', label: 'Method' },
        { key: 'group', label: 'Group' },
        { key: 'orders', label: 'Orders', unit: 'n' },
        { key: 'share', label: 'Share', unit: '%' },
      ], rows: p.rows, sort: false }));
  }

  function apps(a) {
    const w = a.weight || {};
    const weight = w.unavailable ? 'Page weight unavailable: ' + (w.reason || 'no runs') + '.' :
      w.note + ' ' + w.rows.filter((r) => r.device === 'mobile').map((r) => r.page + ' ' + (r.bytes / 1e6).toFixed(1) + ' MB, ' + Math.round(r.requests) + ' requests').join('; ') + ' (mobile, ' + (w.source || 'lab') + ').';
    return el('div', null,
      el('p', { class: 'th', text: a.onsite + ' tools seen on the storefront, ' + (a.rows.length - a.onsite) + ' named in press. Cost, revenue link and script weight per app: ' + a.cost_reason + '.' }),
      el('div', { class: 'wrap' }, UI.table({ columns: [
        { key: 'job', label: 'Job', format: (v) => v || 'other' },
        { key: 'tool', label: 'Tool', format: (v, r) => v || r.text },
        { key: 'seen', label: 'Seen' },
        { key: 'monthly_cost', label: 'Cost a month', format: () => 'unavailable' },
        { key: 'revenue_attributed', label: 'Revenue link', format: () => 'unavailable' },
        { key: 'date', label: 'Captured' },
      ], rows: a.rows, sort: false })),
      el('p', { class: 'th', text: weight }));
  }

  function uptime(u) {
    if (!u.unavailable) return el('p', { text: u.note });
    return UI.emptyState({ screen: SLUG, title: 'Uptime and checkout: unavailable', text: 'No synthetic monitor is connected, so nobody knows if the store is down until sales drop. ' + u.fix, missing: u.missing });
  }

  function chart(c) {
    if (c.unavailable) return UI.emptyState({ screen: SLUG, title: 'No reversed orders by month', text: c.reason, missing: [c.fix] });
    const labels = c.labels.map((m) => m.slice(2));
    const note = (c.partial.length ? c.partial.join(', ') + ' is a partial month. ' : '') + 'Per 1,000 paid orders placed in the month.';
    return el('div', { class: 'card chart-pair' },
      Charts.line({ labels, unit: 'n', title: 'Returns per 1,000 orders, ' + c.window, note, maxLabels: 6,
        series: [{ name: 'Returns', values: c.returns }, { name: 'Carrier returns', values: c.carrier_returns, color: 'var(--s3)' }] }),
      Charts.line({ labels, unit: 'n', title: 'Chargebacks per 1,000 orders, ' + c.window, note: note + ' The line is the ' + c.benchmark_per_1000 + ' per 1,000 benchmark.', maxLabels: 6,
        benchmark: c.benchmark_per_1000, series: [{ name: 'Chargebacks', values: c.chargebacks, color: 'var(--s2)' }, { name: 'Inquiries', values: c.inquiries, color: 'var(--s4)' }] }));
  }

  function findingsList(fs) {
    if (!fs.length) return el('p', { text: 'No findings this run.' });
    return el('div', { class: 'card' }, fs.map((f) => el('div', { class: 'finding' },
      el('div', { class: 'tags' },
        el('span', { class: 'chip ' + (f.severity === 'critical' || f.severity === 'high' ? 'bad' : 'warn'), text: f.severity }),
        el('span', { class: 'chip mono', text: f.rule_id }),
        el('span', { class: 'chip mono', text: f.capability.id }),
        f.status === 'unavailable' ? el('span', { class: 'chip', text: 'unavailable' }) : null,
        f.confidence < 0.3 && f.status !== 'unavailable' ? el('span', { class: 'chip', text: 'weak evidence' }) : null),
      el('div', { text: f.sentence }),
      f.money_at_stake ? el('div', { class: 'money', text: fmt.money(f.money_at_stake.usd) + ' at stake = ' + f.money_at_stake.formula + ' (' +
        Object.entries(f.money_at_stake.inputs).map(([k, v]) => k + ' ' + v).join(', ') + ')' + (f.money_at_stake.note ? '. ' + f.money_at_stake.note : '') })
        : el('div', { class: 'money', text: 'Money at stake unavailable: ' + (f.money_reason || 'no baseline') }),
      f.unavailable ? el('div', { class: 'money', text: 'Needs ' + f.unavailable.connector + '. ' + f.unavailable.fix }) : null,
      UI.decisionRow({ capability: f.capability.id, autonomy: AUTONOMY_KIT[f.capability.autonomy] || f.capability.autonomy, screen: SLUG }))));
  }

  function render(d) {
    const b = d.brand || {};
    const t = d.tiles || {};
    UI.mount('#app',
      el('header', { class: 'screen-head' }, el('h1', { text: 'Store health' }),
        el('p', { text: 'Through ' + fmt.date(b.as_of) + '. Is the store set up right, can people pay, and how many orders come back.' })),
      simBanner(b),
      section('At a glance', el('div', { class: 'grid tiles four' }, tile(t.checklist), tile(t.chargebacks), tile(t.returns), tile(t.uptime))),
      section('What the rules say', el('div', { class: 'grid two' }, (d.insights || []).map((i) =>
        UI.insight({ sentence: i.sentence, rule: i.rule, severity: i.severity, capability: i.capability,
          autonomy: AUTONOMY_KIT[i.autonomy] || i.autonomy, stub: i.stub, screen: SLUG })))),
      section('Audit findings', findingsList(d.findings || [])),
      section('Setup checklist', el('p', { class: 'th', text: 'Each item reads one source. Pass and fail are checked; unavailable means the data to check it is not connected yet.' }), checklist(d.checklist || [])),
      section('Reversed orders', legs(d.reversed), chart(d.chart)),
      section('Payment methods', payments(d.payments)),
      section('Apps and scripts', apps(d.apps)),
      section('Uptime and checkout', uptime(d.uptime)));
  }

  UI.api('/api/' + SLUG + '/overview?brand=' + encodeURIComponent(brand))
    .then(render)
    .catch((e) => UI.mount('#app', el('header', { class: 'screen-head' }, el('h1', { text: 'Store health' })),
      UI.emptyState({ screen: SLUG, title: 'Could not load', text: String(e.message || e) })));
})();
