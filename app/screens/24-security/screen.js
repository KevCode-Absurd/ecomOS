/* Security, round 0. Reads /api/24-security/overview and composes kit components.
   No numbers are computed here; the server sends every value, rule and sentence. */
(function () {
  'use strict';
  const SLUG = '24-security';
  const { el, fmt } = UI;
  const brand = new URLSearchParams(location.search).get('brand') || 'bombas';
  const AUTONOMY_KIT = { agent_does: 'agent', founder_gate: 'founder_gate', human_assist: 'human_assist', agent: 'agent' };
  const STATE = { fired: 'bad', passed: 'good', unavailable: '' };

  function section(title, ...children) {
    return el('section', { class: 'section' }, el('h3', { text: title }), ...children);
  }

  function simBanner(b) {
    const name = b.name || b.brand || 'This brand';
    if (!b.simulated) return el('div', { class: 'sim', role: 'note' }, el('b', { text: name }), ' live data. Read-only.');
    return el('div', { class: 'sim', role: 'note' }, el('b', { text: name }),
      ': simulated data. Scripts, consent, captcha and policy dates come from public pages; every order, chargeback, dispute and payout is generated. Nothing here is a ' + name + ' result.');
  }

  function tile(t) {
    const src = (t.sources || []).map((s) => s.table).join(', ');
    return UI.tile(Object.assign({}, t, { freshness: t.freshness ? fmt.date(t.freshness) + (src ? ' from ' + src : '') : null }));
  }

  function pct(v, d) { return v == null ? 'unavailable' : (v * 100).toFixed(d == null ? 2 : d) + ' percent'; }
  function kv(pairs) {
    return el('dl', { class: 'kv' }, pairs.filter(Boolean).flatMap(([k, v]) => [el('dt', { text: k }), el('dd', { text: v })]));
  }

  function chart(c) {
    if (c.unavailable) return UI.emptyState({ screen: SLUG, title: 'No chargebacks by month', text: c.reason, missing: [c.fix] });
    const l = c.lines_per_1000;
    const note = (c.partial.length ? c.partial.join(', ') + ' is a partial month. ' : '') +
      'Per 1,000 paid orders placed in the month. The line is the ' + l.alert + ' per 1,000 alert. Card network lines sit at ' + l.early_warning + ' and ' + l.network + ' per 1,000.';
    return el('div', { class: 'card' }, Charts.line({ labels: c.labels.map((m) => m.slice(2)), unit: 'n',
      title: 'Chargebacks and inquiries per 1,000 orders, ' + c.window, note, maxLabels: 6, benchmark: l.alert,
      series: [{ name: 'Chargebacks', values: c.chargebacks, color: 'var(--s2)' }, { name: 'Inquiries', values: c.inquiries, color: 'var(--s4)' }] }));
  }

  function money(d) {
    const cb = d.chargebacks, w = d.win_rate, p = d.payouts;
    const left = el('div', { class: 'card' }, el('h4', { text: 'Chargebacks and disputes' }),
      cb.unavailable ? el('p', { class: 'th', text: 'Unavailable: ' + cb.reason + '.' }) : kv([
        ['Chargebacks, 30 days', fmt.int(cb.chargebacks) + ' of ' + fmt.int(cb.paid_orders) + ' paid orders (' + pct(cb.rate) + ')'],
        ['Disputed', cb.amount == null ? 'unavailable' : fmt.money(cb.amount)],
        ['Top reason', cb.by_reason.length ? cb.by_reason[0][0].replace(/_/g, ' ') + ' (' + cb.by_reason[0][1] + ')' : 'none'],
        ['Won, closed in 28 days', w.unavailable ? 'unavailable' : (w.closed ? pct(w.rate, 0) + ' (' + w.won + ' of ' + w.closed + ')' : 'none closed')],
        ['Open now', w.unavailable || w.open_now == null ? 'unavailable' : fmt.int(w.open_now)],
      ]));
    const right = el('div', { class: 'card' }, el('h4', { text: 'Payouts, 28 days' }),
      p.unavailable ? el('p', { class: 'th', text: 'Unavailable: ' + p.reason + '.' }) : el('div', null, kv([
        ['Payouts', fmt.int(p.payouts)],
        ['Charges', fmt.money(p.charges)],
        ['Dispute moves', fmt.money(p.adjustments)],
        ['Dispute moves, scaled to order totals', p.adjustments_scaled == null ? 'unavailable' : fmt.money(p.adjustments_scaled)],
        ['Refunds', fmt.money(p.refunds)],
        ['Held', 'unavailable'],
      ]), el('p', { class: 'th', text: 'Held: ' + p.holds_reason + '.' })));
    return el('div', null,
      el('p', { class: 'th', text: 'Counted in the simulated order table, so counts are a sample and rates are the part to read. Account takeover and promo abuse need connectors; see the rule list.' }),
      el('div', { class: 'pair' }, left, right));
  }

  function surface(sc, ctl) {
    const a = ctl.agent_endpoint, pv = ctl.privacy;
    return el('div', null,
      el('p', { class: 'th', text: sc.count + ' vendor scripts in the brand record, line ' + sc.max + '. Hosts named in the record: ' + (sc.hosts_named.join(', ') || 'none') + '. Other hosts: unavailable, ' + sc.unknown_reason + '.' }),
      el('div', { class: 'wrap' }, UI.table({ columns: [
        { key: 'field', label: 'Job', format: (v) => v.replace(/_/g, ' ') },
        { key: 'tool', label: 'Tool', format: (v, r) => v || r.text },
        { key: 'hosts', label: 'Hosts seen', format: (v) => (v && v.length ? v.join(', ') : 'none in the record') },
        { key: 'seen', label: 'Captured' },
      ], rows: sc.rows, sort: false })),
      el('div', { class: 'card' }, kv([
        ['Consent manager', ctl.consent.present ? ctl.consent.tool : 'not recorded'],
        ['Form captcha', ctl.captcha.present ? ctl.captcha.tool : 'not recorded'],
        ['Privacy policy', pv.effective ? 'effective ' + pv.effective + ', ' + pv.age_days + ' days ago (line ' + pv.max_days + ')' : 'unavailable'],
        ['AI agent endpoint', a.present ? a.value + ' (' + a.url + ')' : 'none recorded'],
      ])));
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
        Object.entries(f.money_at_stake.inputs).map(([k, v]) => k + ' ' + v).join(', ') + ')' })
        : el('div', { class: 'money', text: 'Money at stake unavailable: ' + (f.money_reason || 'no baseline') }),
      f.unavailable ? el('div', { class: 'money', text: 'Needs ' + f.unavailable.connector + '. ' + f.unavailable.fix }) : null,
      UI.decisionRow({ capability: f.capability.id, autonomy: AUTONOMY_KIT[f.capability.autonomy] || f.capability.autonomy, screen: SLUG }))));
  }

  function coverage(rows) {
    return el('div', { class: 'card' }, rows.map((r) => el('div', { class: 'rule' },
      el('span', { class: 'mono', text: r.rule_id + ' ' + r.capability }),
      el('span', null, el('span', { class: 'chip ' + STATE[r.state], text: r.state })),
      el('span', { class: 'name', text: r.name + (r.connector ? '. Needs ' + r.connector + '.' : '') }))));
  }

  function render(d) {
    const b = d.brand || {};
    const t = d.tiles || {};
    const open = (d.findings || []).filter((f) => f.status === 'open');
    const unavail = (d.findings || []).filter((f) => f.status === 'unavailable');
    UI.mount('#app',
      el('header', { class: 'screen-head' }, el('h1', { text: 'Security' }),
        el('p', { text: 'Through ' + fmt.date(b.as_of) + '. Fraud and disputes, what code runs on the store, and which checks cannot run yet.' })),
      simBanner(b),
      section('At a glance', el('div', { class: 'grid tiles three' }, tile(t.chargebacks), tile(t.win_rate), tile(t.scripts))),
      section('What the rules say', el('div', { class: 'grid two' }, (d.insights || []).map((i) =>
        UI.insight({ sentence: i.sentence, rule: i.rule, severity: i.severity, capability: i.capability,
          autonomy: AUTONOMY_KIT[i.autonomy] || i.autonomy, stub: i.stub, screen: SLUG })))),
      section('Chargebacks by month', chart(d.chart)),
      section('Audit findings', el('p', { class: 'th', text: open.length + ' open, ' + unavail.length + ' cannot be checked until a connector is added.' }), findingsList(d.findings || [])),
      section('Fraud and disputes', money(d)),
      section('Storefront surface', surface(d.scripts, d.controls)),
      section('Every rule', el('p', { class: 'th', text: 'Fired means the rule found an issue. Passed means it read its inputs and found none. Unavailable means the data is not connected.' }), coverage(d.coverage || [])));
  }

  UI.api('/api/' + SLUG + '/overview?brand=' + encodeURIComponent(brand))
    .then(render)
    .catch((e) => UI.mount('#app', el('header', { class: 'screen-head' }, el('h1', { text: 'Security' })),
      UI.emptyState({ screen: SLUG, title: 'Could not load', text: String(e.message || e) })));
})();
