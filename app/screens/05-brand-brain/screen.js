/* Brand brain, round 0. Reads /api/05-brand-brain/overview, records and audit.
   Writes only through the api: a founder answer, and accept or ignore on a proposed record. */
(function () {
  'use strict';
  const { el, mount, api, fmt } = UI;
  const BASE = '/api/05-brand-brain/';
  const NA = 'unavailable';
  const pretty = (s) => String(s || '').replace(/_/g, ' ');
  const TIER_TONE = { approved: 'good', site_backed: 'accent', forbidden: 'bad', unverified: 'warn', inferred: 'warn' };

  function tierChip(t) { return el('span', { class: 'chip ' + (TIER_TONE[t] || ''), text: pretty(t) }); }

  function sourceLink(src) {
    if (!src) return el('span', { text: 'no source' });
    if (src.link) return el('a', { href: src.link, target: '_blank', rel: 'noopener', text: pretty(src.type) + ': ' + src.link.replace(/^https?:\/\//, '') });
    return el('span', { text: pretty(src.type) + (src.ref ? ': ' + src.ref : '') });
  }

  function recordCard(r) {
    const card = el('article', { class: 'card flat rec' });
    card.append(el('div', { class: 'meta' }, tierChip(r.tier), el('span', { class: 'chip mono', text: r.id }),
      el('span', { text: r.date === 'undated' ? 'undated' : fmt.date(r.date) }),
      el('span', { text: 'confidence ' + (r.confidence == null ? NA : r.confidence) }),
      r.status !== 'active' ? el('span', { class: 'chip warn', text: r.status }) : null));
    card.append(el('div', { text: r.text || '' }));
    card.append(el('div', { class: 'meta' }, sourceLink(r.source)));
    for (const e of (r.evidence || []).slice(0, 3)) card.append(el('blockquote', { text: '"' + e.quote + '"' }));
    return card;
  }

  async function openSection(name) {
    const wrap = document.getElementById('browser-wrap');
    wrap.hidden = false;
    document.getElementById('browser-title').textContent = 'Records in ' + pretty(name);
    mount('#browser', el('p', { class: 'muted', text: 'Loading.' }));
    try {
      const d = await api(BASE + 'records?section=' + encodeURIComponent(name));
      mount('#browser', ...(d.records.length ? d.records.map(recordCard) : [el('p', { class: 'muted', text: 'No records in this section yet.' })]));
    } catch (e) { mount('#browser', el('p', { class: 'muted', text: 'Could not load: ' + e.message })); }
    wrap.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function sectionsTable(rows) {
    return UI.table({
      columns: [
        { key: 'section', label: 'Section', format: (v, r) => pretty(v) + (r.meta ? ' (system)' : '') },
        { key: 'records', label: 'Records', align: 'right' },
        { key: 'freshness_days', label: 'Days since update', align: 'right', format: (v, r) => v == null ? (r.records ? 'undated' : 'no records') : String(v) },
        { key: 'stale', label: 'Stale', align: 'right' },
        { key: 'confidence', label: 'Confidence', align: 'right', format: (v) => v == null ? NA : v.toFixed(2) },
      ],
      rows, sort: { key: 'records', dir: 'desc' }, onRow: (r) => openSection(r.section),
    });
  }

  function ladderCard(l) {
    const card = el('article', { class: 'card ladder' });
    card.append(el('div', { class: 'row' }, el('b', { text: pretty(l.theme) }), el('span', { class: 'chip mono', text: l.id })));
    const rungs = el('div', { class: 'rungs' });
    for (const r of l.rungs) {
      const noProof = !r.proof_ids.length;
      const c = r.counts || {};
      const box = el('div', { class: 'rung' + (noProof ? ' noproof' : '') });
      box.append(el('div', { class: 'doubt', text: 'Rung ' + r.level + ': ' + r.doubt }));
      box.append(el('div', { class: 'meta' },
        el('span', { text: (c.one_star == null ? NA : c.one_star) + ' one-star' }),
        el('span', { text: (c.five_star == null ? NA : c.five_star) + ' five-star' }),
        ...r.uses.map((u) => el('span', { class: 'chip', text: pretty(u) }))));
      for (const q of r.one_star) box.append(el('blockquote', { text: '"' + q + '"' }));
      box.append(el('div', { class: 'meta' }, el('span', { class: 'chip ' + (noProof ? 'bad' : 'good'), text: noProof ? 'no proof' : 'proof' }),
        el('span', { text: r.proof || '' })));
      rungs.append(box);
    }
    card.append(rungs);
    return card;
  }

  function questionCard(q, reload) {
    const card = el('article', { class: 'card flat rec' });
    card.append(el('div', { class: 'meta' }, el('span', { class: 'chip mono', text: q.field }), el('span', { class: 'chip', text: pretty(q.section) }),
      el('span', { class: 'chip ' + (q.weight >= 8 ? 'bad' : ''), text: 'weight ' + q.weight }),
      q.answered_on ? el('span', { class: 'chip good', text: 'answered ' + fmt.date(q.answered_on) }) : null));
    card.append(el('div', { text: q.question }));
    if (q.why) card.append(el('div', { class: 'muted small', text: q.why }));
    if (q.who_can_answer) card.append(el('div', { class: 'muted small', text: 'Who can answer: ' + q.who_can_answer }));
    if (q.answered_on) { card.append(el('div', { class: 'muted small', text: 'Saved as ' + q.answer_record })); return card; }
    const input = el('input', { type: 'text', placeholder: 'Your answer in a line', 'aria-label': 'Answer: ' + q.question });
    const btn = el('button', { class: 'btn primary sm', type: 'button', text: 'Save answer' });
    const status = el('span', { class: 'muted small' });
    btn.addEventListener('click', async () => {
      if (!input.value.trim()) { status.textContent = 'Type an answer first.'; return; }
      btn.disabled = true;
      try {
        const res = await api(BASE + 'questions/' + encodeURIComponent(q.field), { method: 'POST', body: { answer: input.value } });
        status.textContent = 'Saved as ' + res.record + '.';
        reload();
      } catch (e) { btn.disabled = false; status.textContent = 'Could not save: ' + e.message; }
    });
    card.append(el('div', { class: 'answer' }, input, btn), status);
    return card;
  }

  function reviewCard(r, reload) {
    const card = recordCard(r);
    const status = el('span', { class: 'muted small' });
    const act = (choice) => async () => {
      try { await api(BASE + 'review/' + encodeURIComponent(r.id), { method: 'POST', body: { choice } }); reload(); }
      catch (e) { status.textContent = 'Could not save: ' + e.message; }
    };
    const ok = el('button', { class: 'btn primary sm', type: 'button', text: 'Accept' });
    const no = el('button', { class: 'btn sm', type: 'button', text: 'Ignore' });
    ok.addEventListener('click', act('accept'));
    no.addEventListener('click', act('ignore'));
    card.append(el('div', { class: 'row' }, ok, no, status));
    return card;
  }

  function conflictCard(c) {
    const card = el('article', { class: 'card flat rec' });
    card.append(el('div', { class: 'meta' }, el('span', { class: 'chip mono', text: c.section + '.' + c.field }),
      el('span', { text: 'raised ' + fmt.date(c.raised_at) }), c.needs_founder ? el('span', { class: 'chip warn', text: 'needs you' }) : null));
    const vs = el('div', { class: 'vs' });
    for (const v of c.values || []) {
      const kept = v.record_id === c.kept && v === (c.values || []).find((x) => x.record_id === c.kept);
      vs.append(el('div', { class: kept ? 'kept' : '' }, el('div', { class: 'meta' }, kept ? el('span', { class: 'chip accent', text: 'kept for now' }) : null,
        el('span', { text: 'confidence ' + v.confidence })), el('b', { text: String(v.value) }), el('div', { class: 'muted small', text: v.text }),
        el('div', { class: 'meta' }, sourceLink({ type: v.source_type, ref: v.source_ref, link: /^https?:/.test(v.source_ref) ? v.source_ref : null }))));
    }
    card.append(vs, el('div', { class: 'muted small', text: 'Rule: ' + (c.rule || NA) }));
    card.append(UI.decisionRow({ capability: 'BRN-C05', autonomy: 'agent', screen: '05-brand-brain' }));
    return card;
  }

  function auditTable(findings) {
    return UI.table({
      columns: [
        { key: 'severity', label: 'Severity' },
        { key: 'rule_id', label: 'Rule' },
        { key: 'what', label: 'What' },
        { key: 'sentence', label: 'Finding' },
        { key: 'cap', label: 'Capability' },
      ],
      rows: findings.map((f) => ({ severity: f.severity, rule_id: f.rule_id, what: pretty(f.entity.label), sentence: f.sentence,
        cap: f.capability.id + ', ' + pretty(f.capability.autonomy) })), sort: false, empty: 'No findings. The brain has what the rooms need.',
    });
  }

  async function load() {
    let d;
    try { d = await api(BASE + 'overview'); } catch (e) {
      mount('#badge', 'Could not load the brain: ' + e.message); return;
    }
    mount('#badge', el('span', null, el('b', { text: 'Simulated data. ' }), d.simulated_note + ' Brain version ' + d.version + '.'));
    document.getElementById('t0').textContent = d.t0;
    mount('#tiles', ...d.tiles.map((t) => UI.tile(Object.assign({}, t, { window: null, freshness: d.today }))));
    mount('#insights', ...(d.insights.length ? d.insights.map((i) => UI.insight(Object.assign({ screen: '05-brand-brain' }, i)))
      : [el('p', { class: 'muted', text: 'No rule fired today.' })]));
    const ch = d.chart;
    mount('#chart', Charts.bar({ labels: ch.labels.map((x, i) => (ch.labels.length - 1 - i) % 5 === 0 ? x.slice(5) : ''), series: [{ name: 'records', values: ch.values }], unit: 'n',
      title: 'Records by first known date, last ' + ch.labels.length + ' days',
      note: ch.earlier + ' records are dated earlier. ' + ch.undated + ' have no date.' }));
    mount('#sections', sectionsTable(d.sections));
    mount('#ladders', ...d.ladders.map(ladderCard));
    mount('#questions', ...(d.questions.length ? d.questions.map((q) => questionCard(q, load)) : [el('p', { class: 'muted', text: 'No open questions.' })]));
    mount('#review', ...(d.review.length ? d.review.map((r) => reviewCard(r, load)) : [el('p', { class: 'muted', text: 'Nothing proposed. Agent updates land here before they reach the brain.' })]));
    mount('#conflicts', ...(d.conflicts.length ? d.conflicts.map(conflictCard) : [el('p', { class: 'muted', text: 'No open conflicts.' })]));
    try {
      const a = await api(BASE + 'audit');
      mount('#audit', el('p', { class: 'muted small', text: a.findings.length + ' findings from ' + a.rules.length + ' rules.' }), auditTable(a.findings));
    } catch (e) { mount('#audit', el('p', { class: 'muted', text: 'Audit unavailable: ' + e.message })); }
  }

  load();
})();
