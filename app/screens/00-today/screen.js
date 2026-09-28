/* Today: the pipeline with the break marked, money at stake, 3 tiles, 2 insights, 1 chart,
   the top 10 stub and the findings. Data from /api/00-today/summary. Decisions go to
   /api/00-today/decisions (app/data/brands/<brand>/decisions.json). */
(function () {
  const { el, mount, fmt } = UI;
  const API = '/api/00-today/';
  let decisions = [];

  function head(id) { return document.querySelector('#' + id + ' h3'); }
  function fill(id, ...nodes) { mount('#' + id, head(id), ...nodes); }
  const pct = (v) => (typeof v === 'number' ? (v * 100).toFixed(1) + '%' : 'unavailable');
  // the catalogue writes agent_does; the kit's labels use agent
  const autonomy = (a) => UI.AUTONOMY[a === 'agent_does' ? 'agent' : a] || a || '';
  const shortDay = (iso) => new Date(iso + 'T12:00:00').toLocaleDateString('en-US', { month: 'short', day: 'numeric' });

  /* The 3-button row from the kit, posting to this brand's log instead of the shared one. */
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
      : choice === 'person' ? 'A brief for ' + p.capability + ' would go to a person on your team with the evidence from this screen.'
      : 'Nothing runs. ' + p.capability + ' stays in the list and comes back when the numbers change.';
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

  function pipeline(d) {
    const s = d.money_at_stake || {};
    if (!d.stages.length) {
      return fill('pipeline', UI.emptyState({ title: 'The pipeline is unavailable', text: s.reason || 'No stage could be read.', missing: [s.fix || 'ga4'] }));
    }
    const ends = (d.windows || []).map((w) => fmt.date(w.end));
    const cards = d.stages.map((st) => {
      const vals = st.windows.filter((v) => typeof v === 'number');
      const max = Math.max(1, ...vals);
      return el('div', { class: 'stage' + (st.is_break ? ' break' : '') },
        el('div', { class: 'label' }, el('span', { text: st.label }), st.is_break ? el('span', { class: 'chip bad', text: 'Break' }) : null),
        el('div', { class: 'count', text: fmt.int(st.value) }),
        st.from ? el('div', { class: 'rate' }, el('b', { text: pct(st.rate) }), ' of ' + d.stages.find((x) => x.stage === st.from).label.toLowerCase() + ', median ' + pct(st.median)) : el('div', { class: 'rate', text: 'Where the path starts' }),
        st.is_break ? el('div', { class: 'money', text: fmt.money(st.money) + ' at stake' }) : null,
        el('div', { class: 'bars', title: '4 windows of 28 days, oldest first' }, st.windows.map((v, i) => el('span', { class: i === st.windows.length - 1 ? 'now' : '', style: 'height:' + (typeof v === 'number' ? Math.max(4, (v / max) * 100) : 4) + '%', title: ends[i] + ': ' + fmt.int(v) }))),
        el('div', { class: 'bars-key' }, el('span', { text: ends[0] || '' }), el('span', { text: ends[ends.length - 1] || '' })));
    });
    const brk = d.stages.find((x) => x.is_break);
    const stake = el('div', { class: 'card stake' },
      el('div', { class: 'small muted', text: 'Money at stake this window' }),
      s.unavailable ? el('div', { class: 'muted', text: 'Unavailable: ' + s.reason })
        : el('div', { class: 'big', text: fmt.money(s.value) }),
      el('div', { class: 'small', text: brk ? 'From the ' + brk.label.toLowerCase() + ' step, the stage furthest below its own median. All 4 steps below median add up to ' + fmt.money(s.total) + '.' : 'No stage is below its own median.' }),
      el('div', { class: 'small muted', text: (s.notes || []).join(' ') + ' Stake = (median rate minus current rate) x shoppers entering the step x value per shopper downstream.' }));
    const pv = d.stages.find((x) => x.stage === 'product_view');
    const note = pv && pv.rate > 1 ? el('p', { class: 'small muted', text: 'Product view counts views, not sessions with a view, in this simulated set. So it can pass 100 percent of sessions.' }) : null;
    fill('pipeline', el('div', { class: 'stages' }, cards), note, stake);
  }

  function insights(d) {
    fill('insights', ...d.insights.map((i) => {
      if (!i.sentence) return UI.insight({ sentence: i.quiet, rule: i.rule, severity: 'info' });
      const node = UI.insight({ sentence: i.sentence, rule: i.rule, severity: i.severity, evidence: i.evidence });
      node.querySelector('.tags').append(el('span', { class: 'chip mono', text: i.capability }), el('span', { class: 'chip', text: autonomy(i.autonomy) }));
      node.append(decisionRow({ capability: i.capability, autonomy: i.autonomy, card: i.finding }));
      return node;
    }));
  }

  function chart(d) {
    const c = d.chart;
    if (c.unavailable) return fill('chart', UI.emptyState({ title: 'Daily revenue is unavailable', text: c.reason }));
    fill('chart', el('div', { class: 'card' }, Charts.line({
      labels: c.labels.map(shortDay), series: [{ name: 'Net revenue', values: c.values }], unit: 'usd',
      note: 'Net revenue per day: line subtotal minus discounts, all orders. From the daily aggregate. Simulated.'
    })));
  }

  function top10(d) {
    const t = d.top10;
    fill('top10', el('p', { class: 'small muted', text: t.note }), el('div', { class: 'cards' }, t.cards.map((c) => el('div', { class: 'card' },
      el('div', { class: 'row' }, el('span', { class: 'chip accent', text: '#' + c.rank }), el('span', { class: 'chip warn', text: 'stub' })),
      el('h4', { text: c.title }), el('p', { class: 'why', text: c.why }),
      decisionRow({ capability: c.capability, autonomy: c.autonomy, card: c.id })))));
  }

  function findings(d) {
    if (!d.findings.length) return fill('findings', el('p', { class: 'muted', text: 'No findings this window.' }));
    fill('findings', el('p', { class: 'small muted', text: 'What audit.py returns, in the shape Propose will read. Sorted by severity, then money.' }),
      UI.table({
        columns: [{ key: 'severity', label: 'Severity' }, { key: 'stage', label: 'Stage' }, { key: 'rule_id', label: 'Rule' },
          { key: 'usd', label: 'At stake', unit: '$', format: (v) => (v == null ? 'none' : fmt.money(v)) },
          { key: 'confidence', label: 'Confidence', align: 'right', format: (v) => v.toFixed(1) }, { key: 'capability', label: 'Fix' }, { key: 'sentence', label: 'What it says' }],
        rows: d.findings.map((f) => ({ severity: f.severity, stage: f.entity.label, rule_id: f.rule_id, usd: f.money_at_stake ? f.money_at_stake.usd : null,
          confidence: f.confidence, capability: f.capability.id, sentence: f.sentence })),
        sort: false
      }));
  }

  async function load() {
    let d;
    try { d = await UI.api(API + 'summary?window=28d'); } catch (e) {
      return fill('pipeline', UI.emptyState({ title: 'Today could not load', text: e.message }));
    }
    decisions = d.decisions || [];
    const b = d.brand || {};
    document.getElementById('simulated').textContent = (b.name || 'This brand') + ': simulated data, shaped from public information. Nothing here is a real ' + (b.name || '') + ' result. Last full day ' + fmt.date(b.as_of) + '.';
    pipeline(d);
    fill('tiles', el('div', { class: 'grid tiles' }, d.tiles.map((t) => UI.tile(Object.assign({}, t, { delta_label: 'vs prior 28 days' })))));
    insights(d);
    chart(d);
    top10(d);
    findings(d);
  }
  load();
})();
