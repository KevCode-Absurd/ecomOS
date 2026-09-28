/* Customers and avatars (depth contract). Reads /api/02-customers-avatars/overview, rank and audit.
   Order: the plan, what is wrong ranked, actions with steps, the desk, the audit.
   Writes only through the api: a founder-marked voice example, and decisions from the plan. */
(function () {
  'use strict';
  const { el, mount, api, fmt } = UI;
  const SLUG = '02-customers-avatars';
  const BASE = '/api/' + SLUG + '/';
  const NA = 'unavailable';
  const pretty = (s) => String(s || '').replace(/_/g, ' ');
  const GROUNDING = {
    grounded: ['good', 'grounded'],
    single_source: ['warn', 'one source'],
    inferred: ['bad', 'inferred'],
  };
  const rung = (id) => { const i = id.lastIndexOf('.'); return pretty(id.slice(0, i)) + ', rung ' + id.slice(i + 1); };
  const pctWhole = (v) => v == null ? NA : Math.round(v * 100) + '%';
  const short = (ref) => String(ref || '').replace(/^https?:\/\/(www\.)?/, '').replace(/\/$/, '');

  function link(ref, text) {
    if (!ref) return null;
    return el('a', { href: ref, target: '_blank', rel: 'noopener', text: text || short(ref) });
  }

  function avatarCard(a) {
    const [tone, label] = GROUNDING[a.grounding];
    const card = el('article', { class: 'card av' });
    card.append(el('div', { class: 'head' }, el('b', { text: a.name }), el('span', { class: 'chip ' + tone, text: label })));
    card.append(el('div', { class: 'meta' },
      el('span', { text: 'share ' + pctWhole(a.share_estimate) }),
      el('span', { text: 'intensity ' + (a.intensity || NA) }),
      el('span', { text: a.quote_count + ' quotes from ' + (a.sources.length ? a.sources.join(', ') : 'no source') })));
    card.append(el('div', { class: 'job' }, el('b', { text: 'Job: ' }), a.job || NA));
    for (const q of a.quotes.slice(0, 3)) {
      card.append(el('blockquote', null, '"' + q.quote + '" ', link(q.ref, q.source || undefined)));
    }
    if (!a.quotes.length) card.append(el('p', { class: 'muted small', text: 'No customer quotes. This avatar is inferred.' }));
    const t = a.top_objection;
    if (t) {
      card.append(el('div', { class: 'top' + (t.proof ? '' : ' open') },
        el('b', { text: 'Top doubt: ' }), t.doubt + ' (' + (t.one_star == null ? NA : t.one_star) + ' one-star). ',
        el('span', { class: 'chip ' + (t.proof ? 'good' : 'bad'), text: t.proof ? 'proof on file' : 'no proof' })));
    }
    return card;
  }

  function objectionTable(rows) {
    return UI.table({
      columns: [
        { key: 'objection', label: 'Objection' },
        { key: 'avatars', label: 'Avatars', format: (v) => !v.length ? 'none named' : v.slice(0, 3).map((a) => a.name).join(', ') + (v.length > 3 ? ' and ' + (v.length - 3) + ' more' : '') },
        { key: 'status', label: 'Proof or open question', format: (v, r) => v === 'open question'
          ? 'Open question on ' + r.open_rungs.map(rung).join('; ') : v === 'proof on file' ? 'Proof: ' + (r.proof_ids.join(', ') || r.proof) : v },
        { key: 'quotes', label: 'Quotes', align: 'right' },
        { key: 'ads', label: 'In ads', align: 'right', format: (v) => v.value == null ? NA : String(v.value) },
        { key: 'pages', label: 'On pages', align: 'right', format: (v) => v.value == null ? NA : String(v.value) },
      ],
      rows, sort: false, empty: 'The objection map is empty.',
    });
  }

  function barList(obj, total) {
    const bars = el('div', { class: 'bars' });
    for (const [k, n] of Object.entries(obj).sort((a, b) => b[1] - a[1])) {
      bars.append(el('div', { class: 'bar-row' }, el('span', { text: k }),
        el('div', { class: 'track' }, el('div', { class: 'fill', style: 'width:' + Math.round(100 * n / (total || 1)) + '%' })),
        el('span', { class: 'num', text: String(n) })));
    }
    return bars;
  }

  function themeCard(t) {
    const card = el('article', { class: 'card theme' });
    const srcTotal = Object.values(t.by_source).reduce((s, n) => s + n, 0);
    card.append(el('div', { class: 'row' }, el('b', { text: pretty(t.theme) }),
      el('span', { class: 'chip', text: t.phrases.length + ' phrases' }), el('span', { class: 'chip', text: t.mentions + ' mentions' })));
    card.append(el('div', { class: 'muted small', text: 'Mentions by source' }), barList(t.by_source, srcTotal));
    for (const p of t.phrases.slice(0, 5)) {
      card.append(el('div', { class: 'ph' },
        el('div', { class: 'meta' }, el('span', { class: 'phrase', text: '"' + p.phrase + '"' }), el('span', { text: (p.count == null ? NA : p.count) + ' mentions' })),
        p.quote ? el('blockquote', null, '"' + p.quote + '" ', link(p.ref, 'source')) : null));
    }
    if (t.phrases.length > 5) card.append(el('div', { class: 'muted small', text: (t.phrases.length - 5) + ' more phrases in this theme.' }));
    return card;
  }

  function exampleBox(v, reload) {
    const card = el('article', { class: 'card vo' });
    card.append(el('b', { text: 'Your examples' }),
      el('p', { class: 'muted small', text: 'Paste a line you like or dislike. It is saved to the brand brain as your record and guides every writer.' }));
    const text = el('textarea', { placeholder: 'A headline, ad line or email opener', maxlength: 600, 'aria-label': 'Example text' });
    const status = el('span', { class: 'small muted', 'aria-live': 'polite' });
    const send = (kind) => async () => {
      if (!text.value.trim()) { status.textContent = 'Paste an example first.'; return; }
      status.textContent = 'Saving';
      try { await api(BASE + 'voice/examples', { method: 'POST', body: { kind, text: text.value.trim() } }); reload(); }
      catch (e) { status.textContent = 'Could not save: ' + e.message; }
    };
    card.append(el('div', { class: 'examples' }, text,
      el('button', { class: 'btn primary sm', type: 'button', text: 'This sounds like us', onclick: send('liked') }),
      el('button', { class: 'btn sm', type: 'button', text: 'This is not us', onclick: send('disliked') }), status));
    for (const [label, rows] of [['Liked', v.liked], ['Disliked', v.disliked]]) {
      card.append(el('div', { class: 'muted small', text: label + ' (' + rows.length + ')' }));
      for (const r of rows.slice(0, 5)) card.append(el('blockquote', { text: '"' + r.text + '"' }));
    }
    return card;
  }

  function voiceCards(v, reload) {
    const sheet = el('article', { class: 'card vo' });
    sheet.append(el('b', { text: 'Do' }));
    sheet.append(el('ul', null, ...v.do.map((r) => el('li', null, r.rule + ' ', r.example ? el('blockquote', { text: '"' + r.example + '"' }) : null, link(r.source)))));
    sheet.append(el('b', { text: 'Do not' }));
    sheet.append(v.do_not.length ? el('ul', null, ...v.do_not.map((r) => el('li', null, r.rule + ' ', r.example ? el('blockquote', { text: '"' + r.example + '"' }) : null)))
      : el('p', { class: 'muted small', text: 'No do-not rules on file yet. Mark a line as not us to start one.' }));
    sheet.append(el('b', { text: 'Tone by context' }));
    sheet.append(el('ul', null, ...v.contexts.map((c) => el('li', null, el('b', { text: c.context + ': ' }), c.tone.join('; ') + ' ', ...c.refs.slice(0, 1).map((r) => link(r))))));
    return [sheet, exampleBox(v, reload)];
  }

  // ---------- 1. the plan ----------
  const isOpen = (a) => a.status !== 'unavailable';
  function exportCsv(actions) {
    UI.csv(actions.map((a, i) => ({ rank: i + 1, title: a.title, owner: a.owner, severity: a.severity, status: a.status,
      total: a.rubric && a.rubric.total, artefact: a.artefact && a.artefact.kind, why: a.why })), null, 'customers-avatars-plan.csv');
  }
  function renderPlan(d, r) {
    const acts = r.actions || [];
    const open = acts.filter(isOpen);
    const win = r.window || {};
    mount('#plan', UI.planBoard({
      title: 'Next moves for our customers', sub: 'Brain as of ' + fmt.date(d.today) + '. Sales numbers ' + (win.days || 28) + ' days to ' + fmt.date(win.ends_on) + '.',
      orient: d.orientation, actions: open, limit: 10, screen: SLUG,
      tools: [el('button', { class: 'btn sm', type: 'button', text: 'Export CSV', onclick: () => exportCsv(acts) })],
      foot: el('div', { class: 'row', style: { gap: '14px' } }, UI.rubricLegend(),
        el('span', { class: 'micro faint', text: 'Ranked by the shared rubric. "Not now" snoozes 14 days. Approved items go to the master list on the brand brain.' })),
      empty: 'No open move. Every avatar is grounded and every top doubt has proof.',
    }));
    const con = acts.filter((a) => !isOpen(a));
    const cw = document.getElementById('connect-wrap');
    cw.hidden = !con.length;
    if (con.length) {
      mount('#connect', el('div', { class: 'card flat connect' },
        el('div', { class: 'sec-head' }, el('h2', { text: 'Connect first: ' + con.length + (con.length === 1 ? ' rule waits' : ' rules wait') + ' on a source' }),
          el('span', { class: 'sub', text: 'A person sets these up in Setup, read-only. They never crowd out work that can start today.' })),
        el('div', { class: 'grid' }, ...con.map((a) => UI.actionCard(a, { compact: true, screen: SLUG })))));
    }
  }

  // ---------- 2. what is wrong, ranked ----------
  const SEV = { critical: 0, high: 1, medium: 2, low: 3 };
  function evidenceText(f) {
    if (f.status === 'unavailable') return 'Unavailable. ' + ((f.unavailable && f.unavailable.fix) || 'Connect the source.');
    return (f.evidence || []).map((e) => pretty(e.metric) + ' ' + (e.value == null ? NA : e.value) +
      (e.baseline != null ? ' vs ' + e.baseline + ' ' + (e.baseline_kind || '') : '')).join('; ') + '. ' + ((f.evidence[0] || {}).window || '');
  }
  function jumpTo(actionId) {
    const node = document.querySelector('#actions [data-id="' + CSS.escape(actionId) + '"]');
    if (!node) return;
    node.scrollIntoView({ behavior: 'smooth', block: 'center' });
    const btn = node.querySelector('.a-foot .btn.quiet');
    if (btn && btn.textContent === 'Show steps') btn.click();
    node.classList.add('flash'); setTimeout(() => node.classList.remove('flash'), 1600);
  }
  function renderWrong(a, r) {
    const byFinding = {};
    for (const act of r.actions || []) for (const fid of act.finding_ids || []) byFinding[fid] = act;
    const names = {}; for (const rule of a.rules) names[rule.rule_id] = rule.name;
    const groups = {};
    for (const f of a.findings) (groups[f.rule_id] = groups[f.rule_id] || []).push(f);
    const order = Object.keys(groups).sort((x, y) => Math.min(...groups[x].map((f) => SEV[f.severity])) - Math.min(...groups[y].map((f) => SEV[f.severity])) || groups[y].length - groups[x].length);
    document.getElementById('wrong-sub').textContent = a.findings.length + ' findings from ' + a.rules.length + ' rules, grouped by rule, severity first. Each links to the action that fixes it.';
    const out = [];
    for (const rid of order) {
      const fs = groups[rid].slice().sort((x, y) => SEV[x.severity] - SEV[y.severity] || x.id.localeCompare(y.id));
      out.push(el('div', { class: 'wrong-group' }, el('h4', null, rid + ': ' + (names[rid] || ''), el('span', { class: 'chip', text: fs.length + ' open' })),
        UI.verdictTable({
          columns: [{ key: 'label', label: 'What' }, { key: 'sentence', label: 'Finding' }, { key: 'confidence', label: 'Confidence', unit: '%' }],
          rows: fs.map((f) => { const act = byFinding[f.id]; return { id: f.id, label: f.entity.label, sentence: f.sentence, evidence: evidenceText(f), confidence: f.confidence, status: f.status, severity: f.severity,
            actions: act ? [{ label: 'Go to action', onClick: () => jumpTo(act.id) }] : [{ label: 'No action', cls: 'quiet', onClick: () => {} }] }; }),
          verdict: { at: 0, kind: (row) => row.status === 'unavailable' ? 'wait' : 'fix', text: (row) => row.status === 'unavailable' ? 'Connect' : row.severity, reason: (row) => row.evidence },
          reason: { key: 'evidence', label: 'Evidence', text: (row) => row.evidence },
          actions: { label: 'Action' },
          sort: false, maxRows: 40,
        })));
    }
    mount('#wrong', ...(out.length ? out : [el('p', { class: 'muted', text: 'No rule fired for this window.' })]));
  }

  // ---------- 3. actions ----------
  function renderActions(r) {
    const acts = r.actions || [];
    const cards = acts.map((a, i) => UI.actionCard(a, { expanded: i === 0, screen: SLUG }));
    const LIMIT = 6;
    const list = document.getElementById('actions');
    mount(list, ...cards.slice(0, LIMIT));
    if (cards.length > LIMIT) {
      const more = el('button', { class: 'btn sm', type: 'button', text: 'Show all ' + cards.length });
      more.addEventListener('click', () => { mount(list, ...cards); more.remove(); });
      mount('#actions-tools', more);
    }
  }

  // ---------- 6. the audit ----------
  function auditTable(findings) {
    return UI.table({
      columns: [
        { key: 'severity', label: 'Severity' },
        { key: 'rule_id', label: 'Rule' },
        { key: 'what', label: 'What' },
        { key: 'sentence', label: 'Finding' },
        { key: 'cap', label: 'Capability' },
      ],
      rows: findings.map((f) => ({ severity: f.status === 'unavailable' ? f.severity + ', unavailable' : f.severity, rule_id: f.rule_id,
        what: pretty(f.entity.label), sentence: f.sentence + (f.unavailable ? ' Fix: ' + f.unavailable.fix : ''),
        cap: f.capability.id + ', ' + pretty(f.capability.autonomy) })), sort: false, empty: 'No findings.',
    });
  }
  function rulesTable(rules, findings) {
    return UI.table({
      columns: [{ key: 'rule_id', label: 'Rule' }, { key: 'name', label: 'What it checks' }, { key: 'inputs', label: 'Reads' },
        { key: 'capability', label: 'Capability' }, { key: 'fired', label: 'Findings', unit: 'n' }],
      rows: rules.map((r) => ({ rule_id: r.rule_id, name: r.name, inputs: (r.inputs || []).join(', '), capability: r.capability,
        fired: findings.filter((f) => f.rule_id === r.rule_id).length })), sort: false,
    });
  }

  async function load() {
    let d, r, a;
    try {
      [d, r, a] = await Promise.all([api(BASE + 'overview'), api(BASE + 'rank'), api(BASE + 'audit')]);
    } catch (e) {
      mount('#badge', 'Could not load customers: ' + e.message); return;
    }
    mount('#badge', el('span', null, el('b', { text: 'Simulated data. ' }), d.simulated_note));
    renderPlan(d, r);
    renderWrong(a, r);
    renderActions(r);
    mount('#avatars', ...(d.avatars.length ? d.avatars.map(avatarCard) : [el('p', { class: 'muted', text: 'No avatar records yet.' })]));
    document.getElementById('obj-note').textContent = 'Avatars come from the objection ladders. Ad coverage: ' +
      (d.angles.available ? 'counted from the ad table.' : d.angles.reason + '.') + ' Page coverage needs a live page scan.';
    mount('#objections', objectionTable(d.objections));
    mount('#language', ...d.language.themes.map(themeCard));
    mount('#voice', ...voiceCards(d.voice, load));
    document.getElementById('audit-sub').textContent = a.findings.length + ' findings from ' + a.rules.length + ' rules. Brain version ' + String(a.brain_version || '').slice(0, 7) + '.';
    mount('#audit', auditTable(a.findings));
    mount('#rules', el('h4', { text: 'Rules' }), rulesTable(a.rules, a.findings));
  }

  load();
})();
