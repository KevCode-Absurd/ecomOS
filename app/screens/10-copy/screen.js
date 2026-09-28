/* Copy, round 0. Reads /api/10-copy/overview, language and audit; POST check runs the claim
   checker on pasted copy. Nothing here writes except the decision row's log. */
(function () {
  'use strict';
  const { el, mount, api, fmt } = UI;
  const BASE = '/api/10-copy/';
  const NA = 'unavailable';
  const pretty = (s) => String(s == null ? '' : s).replace(/_/g, ' ');
  const TIER_TONE = { approved: 'good', site_backed: 'good', evidence: 'warn', reported: 'warn', inferred: 'warn', unverified: 'bad', forbidden: 'bad', missing: 'bad', none: 'bad' };
  const VERDICT = { flagged: ['bad', 'flagged'], allowed: ['good', 'allowed'], not_a_claim: ['', 'not a claim'] };
  let copyRows = [];

  const tierChip = (t) => el('span', { class: 'chip ' + (TIER_TONE[t] || ''), text: pretty(t) });
  const short = (u) => String(u || '').replace(/^https?:\/\//, '').replace(/\/$/, '');
  const money = (v) => (v == null ? NA : fmt.money(v));
  const n = (k, word, many) => k + ' ' + (k === 1 ? word : (many || word + 's'));

  /* A plain table whose cells can hold elements (links, chips). UI.table cells are text only. */
  function richTable(columns, rows, empty) {
    const wrap = el('div', { class: 'table-wrap' });
    const tbl = el('table', { class: 'kit' });
    tbl.append(el('thead', null, el('tr', null, ...columns.map((c) => el('th', { class: c.num ? 'num' : '', scope: 'col', text: c.label })))));
    const body = el('tbody');
    if (!rows.length) body.append(el('tr', null, el('td', { class: 'empty', colspan: columns.length, text: empty || 'No rows.' })));
    for (const r of rows) body.append(el('tr', null, ...columns.map((c) => { const v = c.cell(r); return el('td', { class: c.num ? 'num' : '' }, v == null ? NA : v); })));
    tbl.append(body);
    wrap.append(tbl);
    return wrap;
  }

  function sentenceCard(s) {
    const [tone, label] = VERDICT[s.verdict] || ['', s.verdict];
    const card = el('div', { class: 'sent ' + s.verdict });
    card.append(el('div', { text: s.text }));
    const meta = el('div', { class: 'meta' }, el('span', { class: 'chip ' + tone, text: label }));
    for (const m of s.matches) meta.append(el('span', { class: 'chip mono', text: m.id.split('.').slice(1).join('.') }), tierChip(m.tier));
    for (const r of s.risks) meta.append(el('span', { class: 'chip bad', text: pretty(r.id) }));
    if (s.never_testimonial) meta.append(el('span', { class: 'chip bad', text: 'never testimonial' }));
    card.append(meta);
    for (const why of s.reasons) card.append(el('div', { class: 'why', text: why }));
    if (s.testimonial) card.append(el('div', { class: 'small muted', text: 'Quote found in ' + s.testimonial.id + (s.testimonial.subreddit ? ' (r/' + s.testimonial.subreddit + ')' : '') }));
    return card;
  }

  function voiceSummary(v) {
    const ok = v.pass;
    return el('div', { class: 'voice-sum' }, el('span', { class: 'chip ' + (ok ? 'good' : 'bad'), text: ok ? 'voice rules pass' : 'voice rules broken' }), ' ',
      el('span', { class: 'muted', text: (v.grade == null ? 'grade not scored (under 12 words)' : 'grade ' + v.grade) + ', ' + v.words + ' words' + (v.breaks.length ? '. ' + v.breaks.join('; ') + '.' : '.') }));
  }

  function renderCheck(res) {
    const head = el('div', { class: 'row' },
      el('span', { class: 'chip ' + (res.flagged ? 'bad' : 'good'), text: res.flagged ? res.flagged + ' flagged' : 'no flagged claims' }),
      el('span', { class: 'chip', text: res.claims + ' claim-like lines' }),
      el('span', { class: 'chip good', text: res.allowed + ' allowed' }),
      res.never_testimonial ? el('span', { class: 'chip bad', text: 'Reddit quote used as a testimonial' }) : null);
    mount('#check-out', head, voiceSummary(res.voice), ...res.sentences.map(sentenceCard));
  }

  async function runCheck() {
    const text = document.getElementById('copy-text').value.trim();
    const status = document.getElementById('check-status');
    if (!text) { status.textContent = 'Paste or pick some copy first.'; return; }
    status.textContent = 'Checking.';
    try { renderCheck(await api(BASE + 'check', { method: 'POST', body: { text } })); status.textContent = ''; }
    catch (e) { status.textContent = 'Could not check: ' + e.message; }
  }

  function loadCopy(id) {
    const c = copyRows.find((x) => x.id === id);
    if (!c) return;
    document.getElementById('pick').value = id;
    document.getElementById('copy-text').value = c.headline + '\n' + c.primary_text;
    runCheck();
    document.getElementById('copy-text').scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

  function liveTable(rows) {
    return UI.table({
      columns: [
        { key: 'name', label: 'Copy set', format: (v, r) => r.id + ' ' + v },
        { key: 'headline', label: 'Headline' },
        { key: 'live_ads', label: 'Live ads', align: 'right', format: (v) => v == null ? NA : String(v) },
        { key: 'spend_7d', label: 'Spend, 7 days', align: 'right', format: (v) => money(v) },
        { key: 'flagged', label: 'Flagged lines', align: 'right' },
        { key: 'voice_text', label: 'Voice' },
      ],
      rows: rows.map((r) => Object.assign({ voice_text: r.voice_breaks.length ? r.voice_breaks.join('; ') : 'pass' }, r)), sort: { key: 'spend_7d', dir: 'desc' },
      onRow: (r) => loadCopy(r.id),
    });
  }

  function matchCard(m) {
    const card = el('article', { class: 'card flat fmt' });
    const score = m.score == null ? 'no promise to match' : m.score + ' percent matched';
    card.append(el('div', { class: 'row' }, el('b', { text: m.set_id + ' ' + m.name }),
      el('span', { class: 'chip ' + (m.score == null ? '' : m.score === 100 ? 'good' : 'bad'), text: score }),
      el('span', { class: 'chip', text: m.live_ads == null ? 'live ads ' + NA : n(m.live_ads, 'live ad') })));
    card.append(el('a', { class: 'url', href: m.destination_url, target: '_blank', rel: 'noopener', text: short(m.destination_url) }));
    const items = el('div', { class: 'items' });
    for (const i of m.items) items.append(el('span', { class: 'chip ' + (i.on_page ? 'good' : 'bad'), text: (i.on_page ? 'on page: ' : 'not on page: ') + i.label }));
    if (!m.items.length) items.append(el('span', { class: 'muted small', text: 'The ad names no claim or offer on file.' }));
    card.append(items);
    card.append(el('div', { class: 'small muted', text: m.page_captured ? n(m.page_claims.length, 'brain record') + ' captured from this page.' : 'No brain record was captured from this page yet.' }));
    return card;
  }

  function voiceCards(v) {
    const list = (items, fn) => el('ul', { class: 'rules' }, ...items.map(fn));
    const doCard = el('article', { class: 'card flat' }, el('b', { text: 'Do' }),
      list(v.brand_do, (x) => el('li', null, x.rule + ' ', tierChip(x.tier), ' ', el('span', { class: 'chip mono', text: x.ref.split('.').slice(1).join('.') }))),
      list(v.do, (x) => el('li', { text: x.rule + (x.checked ? ' (checked in code)' : ' (guidance, not checked)') })));
    const dontCard = el('article', { class: 'card flat' }, el('b', { text: 'Do not' }),
      list(v.do_not, (x) => el('li', { text: x.rule + (x.checked ? ' (checked in code)' : '') })),
      el('div', { class: 'small muted', text: 'Inflated words: ' + v.inflated_words.join(', ') + '.' }));
    return [doCard, dontCard];
  }

  function lineBox(l, blocked) {
    const box = el('div', { class: 'line' + (blocked ? ' blocked' : '') });
    box.append(el('div', { class: 'text', text: l.text }));
    box.append(el('div', { class: 'meta' }, blocked ? el('span', { class: 'chip', text: l.slot }) : null,
      el('span', { text: l.chars + ' of ' + l.limit + ' characters' }),
      ...Object.entries(l.tiers).map(([ref, t]) => el('span', { class: 'chip ' + (TIER_TONE[t] || ''), text: ref.split('.').pop().replace(/_/g, ' ') + ': ' + pretty(t) }))));
    if (blocked) box.append(el('div', { class: 'why', text: 'Blocked: ' + l.reasons.join('; ') }));
    return box;
  }

  function stubCard(f) {
    const card = el('article', { class: 'card fmt' });
    card.append(el('div', { class: 'row' }, el('b', { text: f.label }), el('span', { class: 'chip', text: 'headline up to ' + f.headline_max }),
      el('span', { class: 'chip', text: 'text up to ' + f.primary_max }), el('span', { class: 'chip mono', text: 'CTA ' + (f.cta || 'none') })));
    card.append(el('div', { class: 'small muted', text: 'Headlines' }), ...f.headlines.map((l) => lineBox(l, false)));
    card.append(el('div', { class: 'small muted', text: 'Primary text' }), ...(f.primary.length ? f.primary.map((l) => lineBox(l, false)) : [el('div', { class: 'muted small', text: 'No primary line passed the gate for this format.' })]));
    if (f.blocked.length) card.append(el('div', { class: 'small muted', text: 'Held back by the QA gate' }), ...f.blocked.map((l) => lineBox(l, true)));
    return card;
  }

  async function loadLanguage() {
    const theme = document.getElementById('theme').value, star = document.getElementById('star').value;
    try {
      const d = await api(BASE + 'language?theme=' + encodeURIComponent(theme) + '&star=' + encodeURIComponent(star));
      const sel = document.getElementById('theme');
      if (sel.options.length === 1) for (const t of d.themes) sel.append(el('option', { value: t, text: pretty(t) }));
      document.getElementById('lang-count').textContent = d.total + ' phrases, ' + d.never_testimonial + ' marked never testimonial.';
      mount('#language', richTable([
        { label: 'Phrase', cell: (r) => el('div', null, el('div', { text: r.phrase }), r.never_testimonial ? el('span', { class: 'chip bad', text: 'never testimonial' }) : r.copy_ready ? el('span', { class: 'chip good', text: 'copy ready' }) : null) },
        { label: 'Theme', cell: (r) => pretty(r.theme) },
        { label: 'Stars', cell: (r) => r.stars.length ? r.stars.join(', ') : 'none' },
        { label: 'Count', num: true, cell: (r) => r.upvotes != null ? r.upvotes + ' upvotes' : (r.count == null ? null : String(r.count)) },
        { label: 'Use', cell: (r) => r.use },
        { label: 'Source', cell: (r) => el('div', null, el('div', { class: 'small', text: r.subreddit ? 'r/' + r.subreddit : r.sources.map(pretty).join(', ') }),
          r.link ? el('a', { class: 'url', href: r.link, target: '_blank', rel: 'noopener', text: short(r.link).slice(0, 48) }) : null) },
      ], d.rows, 'No phrases for this filter.'));
    } catch (e) { mount('#language', el('p', { class: 'muted', text: 'Language bank unavailable: ' + e.message })); }
  }

  function claimsTable(rows) {
    return richTable([
      { label: 'Record', cell: (r) => el('span', { class: 'chip mono', text: r.id.split('.').slice(1).join('.') }) },
      { label: 'Tier', cell: (r) => el('div', null, tierChip(r.tier), ' ', el('span', { class: 'small muted', text: r.allowed ? 'usable in copy' : 'flagged if used' })) },
      { label: 'What it says', cell: (r) => r.text },
      { label: 'Source', cell: (r) => /^https?:/.test(r.source_ref || '') ? el('a', { class: 'url', href: r.source_ref, target: '_blank', rel: 'noopener', text: short(r.source_ref).slice(0, 48) }) : pretty(r.source_type) },
    ], rows);
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
      rows: findings.map((f) => ({ severity: f.severity + (f.status === 'unavailable' ? ' (unavailable)' : ''), rule_id: f.rule_id, what: f.entity.id + ' ' + f.entity.label,
        sentence: f.sentence, cap: f.capability.id + ', ' + pretty(f.capability.autonomy) })), sort: false, empty: 'No findings. Live copy clears the checks.',
    });
  }

  async function load() {
    let d;
    try { d = await api(BASE + 'overview'); } catch (e) { mount('#badge', 'Could not load copy checks: ' + e.message); return; }
    const inv = d.inventory;
    mount('#badge', el('span', null, el('b', { text: 'Simulated data. ' }), d.simulated_note + ' Brain version ' + d.brain_version + '.'
      + (inv.available ? ' ' + inv.live_ads + ' live ads on ' + fmt.date(inv.window.end) + '.' : ' Live ads unavailable: ' + inv.reason)));
    mount('#tiles', ...d.tiles.map((t) => UI.tile(Object.assign({}, t, { window: t.window || null }))));
    mount('#insights', ...(d.insights.length ? d.insights.map((i) => UI.insight(Object.assign({ screen: '10-copy' }, i)))
      : [el('p', { class: 'muted', text: inv.available ? 'No rule fired on live copy.' : 'Live ads are unavailable, so the live-copy rules did not run.' })]));
    const ch = d.chart;
    mount('#chart', Charts.bar({ labels: ch.labels, series: ch.series, stacked: true, unit: 'n', width: 1100, height: 240,
      title: 'Records a line of copy can cite, by tier', note: ch.allowed + ' of ' + ch.total + ' are approved or site backed and pass the QA gate. The rest are flagged if copy uses them.' }));
    copyRows = d.copy;
    const pick = document.getElementById('pick');
    pick.replaceChildren(el('option', { value: '', text: 'Choose a copy set' }), ...d.copy.map((c) => el('option', { value: c.id, text: c.id + ' ' + c.name + (c.flagged ? ' (' + c.flagged + ' flagged)' : '') })));
    pick.onchange = () => loadCopy(pick.value);
    mount('#live', liveTable(d.copy));
    mount('#match', el('div', { class: 'grid two' }, ...d.match.map(matchCard)));
    mount('#voice', ...voiceCards(d.voice));
    mount('#stub', ...d.stub.map(stubCard));
    mount('#claims', claimsTable(d.claims));
    const flaggedAds = d.tiles[0].value;
    mount('#decide', el('p', { text: (flaggedAds == null ? 'Live ads are unavailable.' : n(flaggedAds, 'live ad') + (flaggedAds === 1 ? ' carries' : ' carry') + ' a flagged line.') + ' The integrity gate would pull each flagged line, draft a replacement from approved claims and hold it for your yes.' }),
      UI.decisionRow({ capability: 'LOOP-C12', autonomy: 'agent', screen: '10-copy',
        stub: 'The agent would run the pre-delivery integrity gate on every live copy set, list each flagged line with its claim record and tier, and draft a replacement built only from approved or site backed claims. Nothing changes in the ad account.' }));
    const first = d.copy.find((c) => c.flagged) || d.copy[0];
    if (first) { pick.value = first.id; document.getElementById('copy-text').value = first.headline + '\n' + first.primary_text; runCheck(); }
    try {
      const a = await api(BASE + 'audit');
      mount('#audit', el('p', { class: 'muted small', text: a.findings.length + ' findings from ' + a.rules.length + ' rules.' }), auditTable(a.findings));
    } catch (e) { mount('#audit', el('p', { class: 'muted', text: 'Audit unavailable: ' + e.message })); }
  }

  document.getElementById('check-btn').addEventListener('click', runCheck);
  document.getElementById('theme').addEventListener('change', loadLanguage);
  document.getElementById('star').addEventListener('change', loadLanguage);
  load();
  loadLanguage();
})();
