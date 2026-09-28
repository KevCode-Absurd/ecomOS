/* Reviews and reports: the weekly or monthly report on one page. 3 tiles, 2 rule insights,
   net revenue by period, what changed, the top 10 findings across screens with their decision
   status, what shipped, what the brain learned, open questions, this report's own audit and the
   brand card. Data from /api/26-reports/summary?period=week|month. Decisions go to
   /api/26-reports/decisions (app/data/brands/<brand>/decisions.json). */
(function () {
  const { el, mount, fmt } = UI;
  const API = '/api/26-reports/';
  let decisions = [];
  let period = 'week';

  function head(id) { return document.querySelector('#' + id + ' h3'); }
  function fill(id, ...nodes) { mount('#' + id, head(id), ...nodes); }
  const autonomy = (a) => UI.AUTONOMY[a === 'agent_does' ? 'agent' : a] || a || '';
  const signed = (v) => (typeof v === 'number' ? (v > 0 ? '+' : '') + (v * 100).toFixed(1) + '%' : 'unavailable');
  function show(v, unit) {
    if (typeof v !== 'number') return 'unavailable';
    if (unit === 'usd') return fmt.money(v);
    if (unit === 'count') return fmt.int(v);
    if (unit === 'ratio') return (v * 100).toFixed(1) + '%';
    if (unit === 'x') return v.toFixed(2) + 'x';
    return String(v);
  }

  /* The 3-button row, posting to this brand's log. */
  function decisionRow(p) {
    const node = el('div', { class: 'decision', dataset: { capability: p.capability } });
    const saved = el('div', { class: 'saved', 'aria-live': 'polite' });
    const buttons = el('div', { class: 'buttons' });
    const btn = {};
    const mark = (row) => {
      for (const k of Object.keys(btn)) btn[k].classList.toggle('sel', k === row.choice);
      saved.className = 'saved';
      saved.textContent = 'Saved: ' + UI.CHOICE_LABEL[row.choice] + ', ' + fmt.date(row.time) + (row.reason ? '. ' + row.reason : '');
    };
    for (const choice of ['agent', 'person', 'not_now']) {
      const b = el('button', { class: 'btn' + (choice === 'agent' ? ' primary' : choice === 'not_now' ? ' quiet' : ''), type: 'button', text: UI.CHOICE_LABEL[choice] });
      if (choice === 'agent' && p.autonomy === 'human_assist') { b.disabled = true; b.title = 'This capability needs a person.'; }
      b.addEventListener('click', () => openStub(p, choice, mark, (msg) => { saved.className = 'saved err'; saved.textContent = 'Could not save: ' + msg; }));
      btn[choice] = b;
      buttons.append(b);
    }
    node.append(buttons, saved, el('div', { class: 'cap' }, el('span', { class: 'chip mono', text: p.capability }), el('span', { text: autonomy(p.autonomy) })));
    const last = decisions.filter((d) => d.capability === p.capability && (!p.card || d.card === p.card)).pop();
    if (last) mark(last);
    return node;
  }

  function openStub(p, choice, onSaved, onError) {
    const what = choice === 'agent' ? 'The agent would run ' + p.capability + (p.autonomy === 'founder_gate' ? ', then stop for your approval before anything changes.' : ' and report back here.')
      : choice === 'person' ? 'A brief for ' + p.capability + ' would go to a person on your team with the evidence from this report.'
      : 'Nothing runs. ' + p.capability + ' stays in the report and comes back when the numbers change.';
    const reason = el('textarea', { class: 'text', placeholder: 'A short reason or note (optional)', maxlength: 300 });
    const status = el('div', { class: 'small muted', 'aria-live': 'polite' });
    const backdrop = el('div', { class: 'stub-backdrop', role: 'dialog', 'aria-modal': 'true', 'aria-label': UI.CHOICE_LABEL[choice] });
    const close = () => { backdrop.remove(); document.body.style.overflow = ''; };
    const confirm = el('button', { class: 'btn primary', type: 'button', text: 'Confirm: ' + UI.CHOICE_LABEL[choice] });
    confirm.addEventListener('click', async () => {
      confirm.disabled = true; status.textContent = 'Saving';
      try {
        const res = await UI.api(API + 'decisions', { method: 'POST', body: { capability: p.capability, autonomy: p.autonomy, card: p.card, choice, reason: reason.value.trim() } });
        decisions.push(res.decision); close(); onSaved(res.decision);
      } catch (e) { confirm.disabled = false; status.textContent = 'Could not save: ' + e.message; onError(e.message); }
    });
    backdrop.append(el('div', { class: 'stub' },
      el('h2', { text: UI.CHOICE_LABEL[choice] }),
      el('div', { class: 'row' }, el('span', { class: 'chip mono', text: p.capability }), el('span', { class: 'chip', text: autonomy(p.autonomy) })),
      el('div', { class: 'what' }, el('b', { text: 'What would happen' }), ' ', what),
      el('p', { class: 'small muted', text: 'The agent layer is not built yet. This logs your decision so the app can act on it later.' }),
      reason,
      el('div', { class: 'row' }, confirm, el('button', { class: 'btn', type: 'button', text: 'Cancel', onclick: close }), status)));
    backdrop.addEventListener('click', (e) => { if (e.target === backdrop) close(); });
    document.body.append(backdrop); document.body.style.overflow = 'hidden';
    reason.focus();
  }

  function tiles(d) {
    const label = d.period.kind === 'month' ? 'vs the month before' : 'vs the week before';
    fill('tiles', el('p', { class: 'small muted', text: d.period.label + ', ' + d.period.start + ' to ' + d.period.end + '. Compared with ' + d.period.prior_start + ' to ' + d.period.prior_end + '.' }),
      el('div', { class: 'grid tiles' }, d.tiles.map((t) => UI.tile(Object.assign({}, t, { delta_label: label })))));
  }

  function insights(d) {
    fill('insights', ...d.insights.map((i) => {
      if (!i.sentence) return UI.insight({ sentence: i.quiet, rule: i.rule, severity: 'info' });
      const node = UI.insight({ sentence: i.sentence, rule: i.rule, severity: i.severity, evidence: i.evidence });
      node.querySelector('.tags').append(el('span', { class: 'chip mono', text: i.capability }), el('span', { class: 'chip', text: autonomy(i.autonomy) }));
      node.append(decisionRow({ capability: i.capability, autonomy: i.autonomy, card: i.card }));
      return node;
    }));
  }

  function chart(d) {
    const c = d.chart;
    head('chart').textContent = c.kind === 'month' ? 'Net revenue by month, 13 closed months' : 'Net revenue by week, 13 weeks';
    if (c.unavailable) return fill('chart', UI.emptyState({ title: 'Net revenue is unavailable', text: 'No period in the chart has net revenue.' }));
    const labels = c.kind === 'month' ? c.labels : c.labels.map((iso) => new Date(iso + 'T12:00:00').toLocaleDateString('en-US', { month: 'short', day: 'numeric' }));
    fill('chart', el('div', { class: 'card' }, Charts.bar({
      labels, series: [{ name: 'Net revenue', values: c.values }], unit: '$', maxLabels: 13,
      note: 'Net revenue per ' + (c.kind === 'month' ? 'calendar month' : 'week ending on the date shown') + ': line subtotal minus discounts on paid orders, from the metric contract. The last bar is this report. Simulated.'
    })));
  }

  function changed(d) {
    const rows = d.what_changed.map((l) => ({
      label: l.label, now: show(l.value, l.unit), before: show(l.prior, l.unit),
      change: l.delta == null ? 'n/a' : signed(l.delta),
      source: l.metric ? 'contract: ' + l.metric : 'not in the contract',
    }));
    const mix = d.channel_mix;
    const mixNode = mix.unavailable ? el('p', { class: 'small muted', text: 'Channel mix unavailable: ' + mix.reason })
      : el('div', {}, el('h4', { text: 'Paid channel mix' }), UI.table({
        columns: [{ key: 'channel', label: 'Channel' }, { key: 'spend', label: 'Spend', unit: '$', format: (v) => fmt.money(v) },
          { key: 'share', label: 'Share', align: 'right', format: (v) => show(v, 'ratio') }, { key: 'prior_share', label: 'Share before', align: 'right', format: (v) => show(v, 'ratio') }],
        rows: mix.rows, sort: false }), el('p', { class: 'small muted', text: mix.note }));
    fill('changed', UI.table({
      columns: [{ key: 'label', label: 'Number' }, { key: 'now', label: 'This ' + d.period.noun, align: 'right' }, { key: 'before', label: 'The ' + d.period.noun + ' before', align: 'right' },
        { key: 'change', label: 'Change', align: 'right' }, { key: 'source', label: 'Source' }],
      rows, sort: false }), mixNode);
  }

  function top10(d) {
    if (!d.top10.length) return fill('top10', el('p', { class: 'muted', text: 'No open findings on any screen this period.' }));
    fill('top10', el('p', { class: 'small muted', text: 'From every screen\'s audit, ranked by money at stake. Findings with no money figure sort last. Status is the last decision logged for that finding.' }),
      UI.table({
        columns: [{ key: 'rank', label: '#' }, { key: 'screen', label: 'Screen' }, { key: 'severity', label: 'Severity' },
          { key: 'usd', label: 'At stake', unit: '$', format: (v) => (v == null ? 'none' : fmt.money(v)) },
          { key: 'sentence', label: 'What it says' }, { key: 'capability', label: 'Fix' }, { key: 'decision', label: 'Decision' }],
        rows: d.top10.map((t) => ({ rank: t.rank, screen: t.screen, severity: t.status === 'unavailable' ? 'unavailable' : t.severity, usd: t.usd,
          sentence: t.sentence, capability: (t.capability || {}).id || '', decision: t.decision.label })),
        sort: false
      }));
  }

  function list(items, render) { return el('ul', { class: 'report-list' }, items.map(render)); }

  function shipped(d) {
    const p = d.period;
    if (!d.shipped.length) return fill('shipped', el('p', { class: 'muted', text: 'No decision was logged from ' + p.log_start + ' to ' + p.log_end + '.' }));
    fill('shipped', el('p', { class: 'small muted', text: 'Decisions logged from ' + p.log_start + ' to ' + p.log_end + ', from the decisions log and the brain.' }),
      list(d.shipped, (s) => el('li', {}, el('div', { text: s.text }), el('div', { class: 'meta' },
        el('span', { text: s.date }), el('span', { class: 'chip', text: s.source }), s.ref ? el('span', { class: 'mono', text: s.ref }) : null))));
  }

  function brain(d) {
    const b = d.brain;
    if (b.unavailable) return fill('brain', UI.emptyState({ title: 'The brain is unavailable', text: b.reason }));
    if (!b.total) return fill('brain', el('p', { class: 'muted', text: 'No brain record was added or changed from ' + d.period.log_start + ' to ' + d.period.log_end + '.' }));
    const secs = Object.entries(b.by_section).sort((a, c) => c[1] - a[1]);
    fill('brain', el('p', { class: 'small muted', text: b.total + ' records added or changed. Brain version ' + b.version + '. A few per section below.' }),
      el('div', { class: 'chips' }, secs.map(([s, n]) => el('span', { class: 'chip', text: s.replace(/_/g, ' ') + ' ' + n }))),
      list(b.rows.slice(0, 12), (r) => el('li', {}, el('div', { text: r.text }), el('div', { class: 'meta' },
        el('span', { text: r.date }), el('span', { class: 'chip', text: r.tier || '' }), el('span', { class: 'mono', text: r.id })))));
  }

  function questions(d) {
    if (!d.open_questions.length) return fill('questions', el('p', { class: 'muted', text: 'No open questions.' }));
    fill('questions', list(d.open_questions.slice(0, 12), (q) => el('li', {}, el('div', { text: q.text }),
      el('div', { class: 'meta' }, el('span', { class: 'chip', text: q.kind === 'brain' ? 'brain question' : 'missing connector' }), q.who ? el('span', { text: 'Who can answer: ' + q.who }) : null))),
      d.open_questions.length > 12 ? el('p', { class: 'small muted', text: (d.open_questions.length - 12) + ' more.' }) : null);
  }

  function audit(d) {
    const bad = d.screens.filter((s) => s.status !== 'ok');
    const read = el('p', { class: 'small muted', text: 'Screens read: ' + (d.screens.length - bad.length) + ' of ' + d.screens.length + '.' + (bad.length ? ' Unavailable: ' + bad.map((s) => s.screen).join(', ') + '.' : '') });
    if (!d.findings.length) return fill('audit', read, el('p', { class: 'muted', text: 'Every claim cites a metric, every number matches the contract, and decisions were logged.' }));
    fill('audit', read, el('p', { class: 'small muted', text: 'What this screen\'s audit.py returns, in the shape Propose reads. Sorted by severity, then money.' }),
      UI.table({
        columns: [{ key: 'severity', label: 'Severity' }, { key: 'rule_id', label: 'Rule' },
          { key: 'usd', label: 'At stake', unit: '$', format: (v) => (v == null ? 'none' : fmt.money(v)) },
          { key: 'sentence', label: 'What it says' }, { key: 'capability', label: 'Fix' }],
        rows: d.findings.map((f) => ({ severity: f.status === 'unavailable' ? 'unavailable' : f.severity, rule_id: f.rule_id,
          usd: f.money_at_stake ? f.money_at_stake.usd : null, sentence: f.sentence, capability: f.capability.id })),
        sort: false
      }));
  }

  function card(d) {
    if (!d.t0_card) return fill('card', el('p', { class: 'muted', text: 'No brain folder for this brand yet.' }));
    fill('card', el('details', { class: 'card' }, el('summary', { text: 'Who this report is about (the brain\'s T0 card)' }), el('pre', { class: 'brand-card', text: d.t0_card })));
  }

  async function load() {
    document.querySelectorAll('.period-toggle .btn').forEach((b) => b.classList.toggle('sel', b.dataset.period === period));
    let d;
    try { d = await UI.api(API + 'summary?period=' + period); } catch (e) {
      return fill('tiles', UI.emptyState({ title: 'The report could not load', text: e.message }));
    }
    decisions = d.decisions || [];
    const b = d.brand || {};
    document.getElementById('simulated').textContent = (b.name || 'This brand') + ': simulated data, shaped from public information. Nothing here is a real ' + (b.name || '') + ' result. Last full day ' + fmt.date(b.as_of) + '.';
    tiles(d); insights(d); chart(d); changed(d); top10(d); shipped(d); brain(d); questions(d); audit(d); card(d);
  }

  document.querySelectorAll('.period-toggle .btn').forEach((b) => b.addEventListener('click', () => { period = b.dataset.period; load(); }));
  load();
})();
