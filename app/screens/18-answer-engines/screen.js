/* Answer engines, round 0. Reads /api/18-answer-engines/overview and composes kit components.
   No numbers are computed here; the server sends every value, rule and sentence. */
(function () {
  'use strict';
  const SLUG = '18-answer-engines';
  const { el, fmt } = UI;
  const brand = new URLSearchParams(location.search).get('brand') || 'bombas';
  const AUTONOMY_KIT = { agent_does: 'agent', founder_gate: 'founder_gate', human_assist: 'human_assist', agent: 'agent' };

  function section(title, ...children) {
    return el('section', { class: 'section' }, el('h3', { text: title }), ...children);
  }

  function simBanner(b) {
    const name = b.name || b.brand || 'This brand';
    if (!b.simulated) return el('div', { class: 'sim', role: 'note' }, el('b', { text: name }), ' live data. Read-only.');
    return el('div', { class: 'sim', role: 'note' }, el('b', { text: name }),
      ': simulated data. Store numbers are generated from a public profile. Facts, pages, reviews and Amazon listings come ' +
      'from the brand brain and are public. No answer engine has been asked anything yet, so engine numbers read unavailable. ' +
      'The buyer prompts are a written sample.');
  }

  function chip(text, tone) { return el('span', { class: 'chip ' + (tone || ''), text }); }

  function tile(t) {
    const extra = t.of != null ? { plain: t.plain + ' ' + fmt.int(t.value) + ' of ' + fmt.int(t.of) + '.' } : {};
    return UI.tile(Object.assign({}, t, extra));
  }

  function engineTable(rows) {
    const na = () => 'unavailable';
    return el('div', null,
      el('p', { class: 'th', text: 'Each rate needs the frozen prompt set run on that engine. Until then every cell reads unavailable, never 0.' }),
      el('div', { class: 'card scroll' }, UI.table({
        columns: [
          { key: 'engine', label: 'Engine' },
          { key: 'ai_mention_rate', label: 'Mentioned', align: 'right', format: na },
          { key: 'ai_recommend_rate', label: 'Recommended', align: 'right', format: na },
          { key: 'ai_share_of_voice', label: 'Share of voice', align: 'right', format: na },
          { key: 'citation_source_share', label: 'Cites our site', align: 'right', format: na },
          { key: 'last_run', label: 'Last run', format: (v) => v || 'never' },
        ],
        rows, sort: false,
      })),
      UI.decisionRow({ capability: 'ORG-C37', autonomy: 'agent', screen: SLUG,
        stub: 'Run the frozen prompt set on each engine and log mention, recommend, tone and cited sources per prompt. ' +
          'Nothing is published; your choice is logged.' }));
  }

  function factTable(rows) {
    if (!rows.length) return UI.emptyState({ screen: SLUG, title: 'No brand brain', text: 'Build the brand brain first.', missing: ['brain'] });
    return el('div', null,
      el('p', { class: 'th', text: 'Each fact an engine gets asked about, the brain records that hold it, and the page each came from.' }),
      el('div', { class: 'card scroll' }, UI.table({
        columns: [
          { key: 'fact', label: 'Fact' },
          { key: 'core', label: 'Core', format: (v) => v ? 'yes' : 'no' },
          { key: 'records', label: 'Records', unit: 'n' },
          { key: 'pages', label: 'Source pages', format: (v) => v.length ? v.map((u) => u.replace(/^https?:\/\/[^/]+/, '')).join(', ') : 'none' },
          { key: 'status', label: 'Status', format: (v) => v },
        ],
        rows, sort: false,
      })),
      UI.decisionRow({ capability: 'ORG-C35', autonomy: 'human_assist', screen: SLUG,
        stub: 'Draft one facts page with every core fact in plain answer form, for a person to check and publish. ' +
          'Nothing goes live without them; your choice is logged.' }));
  }

  function promptTable(p) {
    return el('div', null,
      el('p', { class: 'th', text: p.note }),
      el('div', { class: 'card scroll' }, UI.table({
        columns: [
          { key: 'prompt', label: 'Buyer prompt' },
          { key: 'needs', label: 'Needs', format: (v) => v.join(', ').replace(/_/g, ' ') },
          { key: 'missing', label: 'Missing in brain', format: (v) => v.length ? v.join(', ').replace(/_/g, ' ') : 'none' },
          { key: 'answerable', label: 'Brain can answer', format: (v) => v ? 'yes' : 'no' },
        ],
        rows: p.rows, sort: false,
      })));
  }

  function chart(c) {
    if (c.unavailable) return UI.emptyState({ screen: SLUG, title: 'No objection ladders', text: c.reason, missing: [c.fix] });
    return el('div', { class: 'card' }, Charts.bar({
      labels: c.labels, series: c.series, stacked: true, unit: 'n', title: 'One-star mentions by buyer doubt',
      note: 'Public reviews behind each objection ladder. A bar is marked missing when a sample prompt on that doubt needs a fact the brain does not hold.' }));
  }

  function findingsList(fs) {
    if (!fs.length) return el('p', { text: 'No findings this run.' });
    return el('div', { class: 'card' }, fs.map((f) => el('div', { class: 'finding' },
      el('div', { class: 'tags' },
        chip(f.severity, f.severity === 'critical' || f.severity === 'high' ? 'bad' : 'warn'),
        chip(f.rule_id, 'mono'), chip(f.capability.id, 'mono'),
        f.status === 'unavailable' ? chip('unavailable') : null,
        f.confidence < 0.3 ? chip('weak evidence') : null),
      el('div', { text: f.sentence }),
      f.money_at_stake ? el('div', { class: 'money', text: fmt.money(f.money_at_stake.usd) + ' at stake = ' + f.money_at_stake.formula +
        ' (' + Object.entries(f.money_at_stake.inputs).map(([k, v]) => k + ' ' + v).join(', ') + '), ' + f.money_at_stake.window })
        : el('div', { class: 'money', text: 'Money at stake unavailable: ' + (f.money_reason || 'no baseline') }),
      f.unavailable ? el('div', { class: 'money', text: 'Needs ' + f.unavailable.inputs.join(', ') + ' from ' + f.unavailable.connector + '. ' + f.unavailable.fix }) : null,
      f.brain_refs.length ? el('div', { class: 'money', text: 'Brain: ' + f.brain_refs.join(', ') }) : null)));
  }

  function render(d) {
    const b = d.brand || {};
    const t = d.tiles || {};
    UI.mount('#app',
      el('header', { class: 'screen-head' }, el('h1', { text: 'Answer engines' }),
        el('p', { text: 'What AI assistants can say about the brand, which facts they can cite, and where the gaps are. Through ' + fmt.date(b.as_of) + '.' })),
      simBanner(b),
      section('Readiness', el('div', { class: 'grid tiles three' }, tile(t.answered), tile(t.core), tile(t.ai_sessions))),
      section('What the rules say', el('div', { class: 'grid two' }, (d.insights || []).map((i) =>
        UI.insight({ sentence: i.sentence, rule: i.rule, severity: i.severity, capability: i.capability,
          autonomy: AUTONOMY_KIT[i.autonomy] || i.autonomy, screen: SLUG })))),
      section('Buyer doubts and whether the brain can answer them', chart(d.chart)),
      section('Engines', engineTable(d.engines || [])),
      section('Facts an engine can cite', factTable(d.facts || [])),
      section('Sample buyer prompts', promptTable(d.prompts || { rows: [] })),
      section('Audit findings', findingsList(d.findings || [])));
  }

  UI.api('/api/' + SLUG + '/overview?brand=' + encodeURIComponent(brand))
    .then(render)
    .catch((e) => UI.mount('#app', el('header', { class: 'screen-head' }, el('h1', { text: 'Answer engines' })),
      UI.emptyState({ screen: SLUG, title: 'Could not load', text: String(e.message || e) })));
})();
