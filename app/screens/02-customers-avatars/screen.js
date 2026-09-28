/* Customers and avatars, round 0. Reads /api/02-customers-avatars/overview and audit.
   The only write is a founder-marked voice example, through the api into the brain. */
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

  async function load() {
    let d;
    try { d = await api(BASE + 'overview'); } catch (e) {
      mount('#badge', 'Could not load customers: ' + e.message); return;
    }
    mount('#badge', el('span', null, el('b', { text: 'Simulated data. ' }), d.simulated_note));
    mount('#tiles', ...d.tiles.map((t) => UI.tile(Object.assign({ delta_label: 'vs prior cohort' }, t))));
    mount('#insights', ...(d.insights.length ? d.insights.map((i) => UI.insight(Object.assign({ screen: SLUG }, i)))
      : [el('p', { class: 'muted', text: 'No rule fired today.' })]));
    const ch = d.chart;
    mount('#chart', ch.unavailable ? UI.emptyState({ screen: SLUG, title: 'Repeat by cohort is unavailable', text: ch.reason, missing: ch.fix ? [ch.fix] : [] })
      : Charts.bar({ labels: ch.labels, series: [{ name: 'repeat within 3 months', values: ch.values }], unit: '%',
        title: 'Share of first-time buyers active again in months 1 to 3',
        note: 'Simulated. From cohorts.json as of ' + fmt.date(ch.as_of) + '. A buyer active in 2 of those months counts twice, so read it as an upper bound.' }));
    mount('#avatars', ...(d.avatars.length ? d.avatars.map(avatarCard) : [el('p', { class: 'muted', text: 'No avatar records yet.' })]));
    document.getElementById('obj-note').textContent = 'Avatars come from the objection ladders. Ad coverage: ' +
      (d.angles.available ? 'counted from the ad table.' : d.angles.reason + '.') + ' Page coverage needs a live page scan.';
    mount('#objections', objectionTable(d.objections));
    mount('#language', ...d.language.themes.map(themeCard));
    mount('#voice', ...voiceCards(d.voice, load));
    mount('#decision', el('p', { text: d.decision.label + '.' }), UI.decisionRow({ capability: d.decision.capability, autonomy: d.decision.autonomy, screen: SLUG }));
    try {
      const a = await api(BASE + 'audit');
      mount('#audit', el('p', { class: 'muted small', text: a.findings.length + ' findings from ' + a.rules.length + ' rules.' }), auditTable(a.findings));
    } catch (e) { mount('#audit', el('p', { class: 'muted', text: 'Audit unavailable: ' + e.message })); }
  }

  load();
})();
