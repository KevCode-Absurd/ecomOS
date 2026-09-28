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

  const KIND_LABEL = { ticket: 'a ticket', report: 'a report', flow: 'a flow', offer: 'an offer spec', page_section: 'a page section', research_note: 'a research note', ad_brief: 'an ad brief', email: 'an email draft', copy: 'copy', test_brief: 'a test brief' };
  function nextBuild(n) {
    const box = el('div', { class: 'next' });
    const draft = el('pre', { class: 'draft', hidden: true, text: n.draft });
    const toggle = el('button', { class: 'btn quiet xs', type: 'button', text: 'Show draft' });
    toggle.addEventListener('click', () => { draft.hidden = !draft.hidden; toggle.textContent = draft.hidden ? 'Show draft' : 'Hide draft'; });
    const brief = [n.title, '', 'Why: ' + n.why, 'Artefact: ' + (KIND_LABEL[n.kind] || n.kind), '', 'Steps:']
      .concat(n.steps.map((s) => s.n + '. ' + s.text + ' (' + s.who + ')'), ['', n.draft]).join('\n');
    box.append(el('span', { class: 'kicker', text: 'Next build' }),
      el('div', { class: 'row' }, el('b', { text: n.title })),
      el('div', { class: 'small muted', text: n.why }),
      el('div', { class: 'row' }, el('span', { class: 'chip', text: 'makes ' + (KIND_LABEL[n.kind] || n.kind) }),
        n.provisional ? el('span', { class: 'chip warn', text: 'provisional avatar', title: 'Quotes come from 1 source or none' }) : null),
      draft,
      el('div', { class: 'row' }, toggle, UI.copyButton({ label: 'Copy brief', cls: 'quiet xs', text: () => brief }),
        UI.decisionRow({ capability: n.capability, owner: n.owner, screen: SLUG, compact: true, finding_id: n.id })));
    return box;
  }

  function avatarCard(a) {
    const [tone, label] = GROUNDING[a.grounding];
    const card = el('article', { class: 'card av', dataset: { key: a.key } });
    card.append(el('div', { class: 'head' }, el('b', { text: a.name }), el('span', { class: 'chip ' + tone, text: label })));
    card.append(el('div', { class: 'meta' },
      el('span', { text: 'share ' + pctWhole(a.share_estimate) }),
      el('span', { text: 'intensity ' + (a.intensity || NA) }),
      el('span', { text: a.quote_count + ' quotes' })));
    const t = a.top_objection;
    const rows = [
      ['Job', a.job || NA],
      ['Moment', a.triggers.length ? a.triggers.slice(0, 3).join('; ') : NA],
      ['Pain', a.pains.length ? a.pains.slice(0, 2).join('; ') : NA],
      ['Top doubt', t ? el('span', null, t.doubt + ' ', el('span', { class: 'muted', text: '(' + (t.one_star == null ? NA : t.one_star) + ' one-star, ' + (t.five_star == null ? NA : t.five_star) + ' five-star)' })) : 'none named'],
      ['Proof', t ? el('span', null, el('span', { class: 'chip ' + (t.proof ? 'good' : 'bad'), text: t.proof ? 'on file' : 'none' }), ' ',
        t.proof_text ? t.proof_text : '', el('span', { class: 'muted', text: ' ' + a.rungs.proven + ' of ' + a.rungs.total + ' doubts answered' })) : NA],
      ['Where', a.channels.length ? el('span', { class: 'chans' }, ...a.channels.map((c) => el('span', { class: 'chip', text: c.channel + ' ' + c.n }))) : NA],
    ];
    card.append(el('dl', { class: 'facts' }, ...rows.flatMap(([k, v]) => [el('dt', { text: k }), el('dd', null, v)])));
    const quotes = a.quotes.filter((q) => q.source !== 'Reddit').slice(0, 2);
    for (const q of quotes) card.append(el('blockquote', null, '"' + q.quote + '" ', link(q.ref, q.source || undefined)));
    if (!a.quotes.length) card.append(el('p', { class: 'muted small', text: 'No customer quotes. This avatar is a guess until customers say it.' }));
    card.append(nextBuild(a.next));
    return card;
  }

  // ---------- desk: avatar by channel ----------
  function briefPanel(b) {
    const brief = [b.title, '', 'Owner: ' + pretty(b.owner), '', 'Steps:'].concat(b.steps.map((s) => s.n + '. ' + s.text + ' (' + s.who + ')'), ['', b.draft]).join('\n');
    UI.panel({
      title: b.title,
      tools: [UI.copyButton({ label: 'Copy brief', text: () => brief })],
      body: el('div', { class: 'stack' },
        el('div', { class: 'row' }, UI.ownerChip(b.owner), el('span', { class: 'chip', text: 'makes ' + (KIND_LABEL[b.kind] || pretty(b.kind)) }), el('span', { class: 'chip mono', text: b.capability.id })),
        el('pre', { class: 'draft', text: b.draft }),
        el('ol', { class: 'a-steps' }, ...b.steps.map((s) => el('li', null, s.text, el('span', { class: 'who', text: ' (' + s.who + ')' })))),
        UI.decisionRow({ capability: b.capability, owner: b.owner, screen: SLUG, finding_id: b.id })),
    });
  }
  function renderCoverage(c, f) {
    document.getElementById('cover-sub').textContent = 'Each cell: doubts answered with proof | doubts that channel must answer, from the objection ladders. ' + c.line;
    mount('#cover', UI.coverageMatrix({
      rows: c.rows, cols: c.cols, cells: c.cells, unit: 'n', corner: 'Avatar',
      gapRule: (cell) => !cell || cell.them == null ? '' : cell.open ? 'gap' : 'lead',
      action: { label: 'Brief it', onClick: (cell) => cell && cell.brief && briefPanel(cell.brief) },
      note: 'Red: a doubt with no answer there, click Brief it. Green: every doubt answered. n/a: no doubt needs that channel.' +
        (c.skipped.length ? ' Not shown, no doubts mapped yet: ' + c.skipped.join(', ') + '.' : ''),
    }));
    if (!f.available) { mount('#formats', UI.emptyState({ screen: SLUG, title: 'Format mix unavailable', text: f.reason })); return; }
    mount('#formats', el('h4', { text: 'Meta formats: us against the category' }),
      el('p', { class: 'small muted', text: 'Share of live ads. Us from our Ad Library page, them the median of ' + f.pages + ' category pages. Signals only, never proof a format wins.' }),
      UI.verdictTable({
        columns: [{ key: 'label', label: 'Format' }, { key: 'us', label: 'Us', unit: '%' }, { key: 'them', label: 'Category', unit: '%' }, { key: 'pages_running', label: 'Pages', unit: 'n' }],
        rows: f.rows.map((r) => Object.assign({}, r, { actions: r.brief ? [{ label: 'Brief it', onClick: () => briefPanel(r.brief) }] : [{ label: 'No gap', cls: 'quiet', onClick: () => {} }] })),
        verdict: { at: 1, kind: (r) => r.gap ? 'new' : r.us > r.them * 1.5 && r.us > 0.1 ? 'watch' : 'keep', text: (r) => r.gap ? 'Gap' : r.us > r.them * 1.5 && r.us > 0.1 ? 'Heavy' : 'Fine' },
        actions: { label: 'Do' }, sort: false,
      }),
      el('p', { class: 'small', text: f.line }));
  }

  // ---------- desk: ladders per avatar ----------
  const VERDICT = { answer: ['fix', 'No proof'], not_landing: ['watch', 'Not landing'], lead: ['scale', 'Lead with it'], keep: ['keep', 'Keep'] };
  function splitBar(one, five) {
    if (one == null || five == null) return el('span', { class: 'na', text: NA });
    const tot = one + five || 1;
    return el('span', { class: 'split', title: one + ' one-star, ' + five + ' five-star' },
      el('span', { class: 'sbar' }, el('i', { class: 'one', style: 'width:' + Math.round(100 * one / tot) + '%' }), el('i', { class: 'five', style: 'width:' + Math.round(100 * five / tot) + '%' })),
      el('span', { class: 'num small', text: one + ' | ' + five }));
  }
  function renderLadders(L, avatars) {
    document.getElementById('ladder-sub').textContent = 'Each rung: one-star against five-star mentions, proof on file, and the move. ' + L.line +
      ' Not landing means proof is on file and one-star is 2x five-star or more, with 10 or more.';
    const table = el('div');
    const show = (key) => {
      const rows = L.rows.filter((r) => key === 'all' || r.avatars.includes(key));
      mount(table, UI.verdictTable({
        columns: [{ key: 'rung', label: 'Rung' }, { key: 'doubt', label: 'Doubt' }, { key: 'counts', label: 'One-star | five-star' },
          { key: 'proof', label: 'Proof' }, { key: 'who', label: 'Avatars' }],
        rows: rows.map((r) => Object.assign({}, r, { rung: pretty(r.theme) + ', ' + r.level, counts: '', proof: r.proof || 'none on file', who: r.avatar_names.join(', ') || 'none named',
          actions: r.action ? [{ label: 'Brief it', onClick: () => briefPanel(r.action) }] : [{ label: 'Nothing to do', cls: 'quiet', onClick: () => {} }] })),
        verdict: { at: 1, kind: (r) => VERDICT[r.verdict][0], text: (r) => VERDICT[r.verdict][1] },
        actions: { label: 'Do' }, sort: false, maxRows: 40, empty: 'No rung names this avatar yet.',
      }));
      // the split bar is an element, so place it after render
      table.querySelectorAll('tbody tr').forEach((tr, i) => { const r = rows[i]; if (r && tr.children[3]) tr.children[3].replaceChildren(splitBar(r.one_star, r.five_star)); });
    };
    const open = (key) => L.rows.filter((r) => r.avatars.includes(key) && r.verdict === 'answer').length;
    mount('#ladder-pills', UI.pills({ items: [{ key: 'all', label: 'All avatars', n: L.counts.answer }].concat(avatars.filter((a) => L.rows.some((r) => r.avatars.includes(a.key))).map((a) => ({ key: a.key, label: a.name, n: open(a.key) }))),
      current: 'all', onChange: (k) => show(Array.isArray(k) ? k[0] : k) }));
    mount('#ladders', table);
    show('all');
  }

  // ---------- desk: language bank to copy ----------
  function wordList(label, items, picked) {
    const box = el('div', { class: 'wl' }, el('span', { class: 'kicker', text: label }));
    if (!items.length) box.append(el('div', { class: 'na small', text: 'none banked yet' }));
    for (const w of items) {
      const cb = el('input', { type: 'checkbox', checked: !w.language_only });
      if (!w.language_only) picked.add(w);
      cb.addEventListener('change', () => { if (cb.checked) picked.add(w); else picked.delete(w); });
      box.append(el('label', { class: 'w' }, cb, el('span', null, '"' + w.text + '" ',
        el('span', { class: 'chip' + (w.language_only ? ' warn' : ''), text: w.language_only ? 'language only' : (w.source + (w.star ? ', ' + w.star + ' star' : '')) }))));
    }
    return box;
  }
  function wordsCard(r) {
    const picked = new Set();
    const card = el('article', { class: 'card words', dataset: { rung: r.id } });
    card.append(el('div', { class: 'row between' }, el('b', { text: '"' + r.doubt + '"' }),
      el('span', { class: 'chip ' + (r.proof ? 'good' : 'bad'), text: r.proof ? 'proof on file' : 'no proof' })));
    card.append(el('div', { class: 'micro muted', text: pretty(r.theme) + ', rung ' + r.level }));
    card.append(el('div', { class: 'wcols' }, wordList('How they say the doubt', r.doubt_words, picked), wordList('How they say the win', r.win_words, picked)));
    const use = el('button', { class: 'btn soft sm', type: 'button', text: 'Use in brief' });
    use.addEventListener('click', () => {
      const ws = Array.from(picked);
      const lines = r.brief.head.concat(['', 'Doubt in their words:'], ws.filter((w) => r.doubt_words.includes(w)).map((w) => '- "' + w.text + '"' + (w.language_only ? ' (language only)' : '')),
        ['', 'Win in their words:'], ws.filter((w) => r.win_words.includes(w)).map((w) => '- "' + w.text + '"' + (w.language_only ? ' (language only)' : '')));
      briefPanel(Object.assign({}, r.brief, { draft: lines.join('\n') }));
    });
    card.append(el('div', { class: 'row' }, use, el('span', { class: 'micro faint', text: 'Ticked lines go into the brief.' })));
    return card;
  }
  function renderWords(W, avatars) {
    document.getElementById('words-sub').textContent = 'Their words per doubt, from reviews linked to each rung. ' + W.line + ' Reddit lines are language only, never a testimonial.';
    const show = (key) => mount('#words', ...W.rows.filter((r) => key === 'all' || r.avatars.includes(key)).map(wordsCard));
    mount('#words-pills', UI.pills({ items: [{ key: 'all', label: 'All avatars', n: W.rows.length }].concat(avatars.filter((a) => W.rows.some((r) => r.avatars.includes(a.key)))
      .map((a) => ({ key: a.key, label: a.name, n: W.rows.filter((r) => r.avatars.includes(a.key)).length }))), current: 'all', onChange: show }));
    show('all');
  }

  // ---------- desk: cohort grid and retention moves ----------
  function renderCohorts(c) {
    if (!c.available) { mount('#cohort', UI.emptyState({ screen: SLUG, title: 'Cohorts unavailable', text: c.reason })); return; }
    const cb = c.calendar_break, ab = c.age_break;
    document.getElementById('cohort-sub').textContent = 'Share of each first-order month active again, by months since the first order. A cell shows once that month has ended. ' +
      'Break rules: a month where half or more of cohorts fall 40 percent at once is the calendar; the largest fall after the peak, outside that month, is their age.';
    const full = c.rows.filter((r) => r.value_12m != null);
    mount('#cohort-orient', UI.orientation([
      { label: 'peak return month', value: c.peak_month, unit: 'n', title: 'month 1 to 3 with the highest median active share' },
      { label: 'repeat months 1 to 3, median', value: c.repeat_median, unit: '%' },
      { label: 'est. 12-month value', value: full.length ? full[full.length - 1].value_12m : null, unit: '$', title: 'latest full cohort; one order per active month times AOV, an estimate' },
    ]));
    mount('#cohort', Charts.cohort({ rows: c.rows.map((r) => ({ label: r.cohort, values: r.values })), columns: c.columns, unit: '%', cellW: 52, labelW: 70,
      title: 'Active again, by months since the first order',
      note: 'Simulated. From cohorts.json as of ' + fmt.date(c.as_of) + '. Grey is a month that has not ended. ' +
        (cb ? 'Calendar break: ' + cb.month + ', ' + Math.round(cb.share * 100) + ' percent of ' + cb.cohorts + ' cohorts fell together. ' : '') +
        (ab ? 'Age break: month ' + ab.month + ' to ' + (ab.month + 1) + ', down ' + Math.round(ab.drop * 100) + ' percent.' : '') }));
    mount('#cohort-moves', el('span', { class: 'kicker', text: 'Retention moves from the breaks' }),
      ...c.moves.map((m) => UI.actionCard(m, { compact: true, screen: SLUG })));
  }

  // ---------- desk: new against returning ----------
  function renderMix(x) {
    if (!x.available) { mount('#mix-line', UI.emptyState({ screen: SLUG, title: 'Mix unavailable', text: x.reason })); return; }
    document.getElementById('mix-sub').textContent = 'Returning share of orders by month, this year against last, and the channels behind the change in returning orders. ' +
      'Rules: share down 2 points or more against last year; a quarter or more of returning orders through paid ads; email and SMS growing 5 points slower than the rest.';
    mount('#mix-orient', UI.orientation([
      { label: 'returning share, ' + x.latest, value: x.share_now, unit: '%', delta: x.share_last_year ? x.share_now / x.share_last_year - 1 : null, higher_is_better: true },
      { label: 'returning via paid ads', value: x.paid_share_returning, unit: '%', tone: x.paid_share_returning >= 0.25 ? 'bad' : null },
      { label: 'email and SMS growth', value: x.owned_growth, unit: '%' },
    ]));
    mount('#mix-line', Charts.line({ labels: x.months, series: [{ name: 'this year', values: x.series.this_year }, { name: 'last year', values: x.series.last_year }], unit: '%',
      title: 'Returning share of orders', note: 'Simulated. Full months only, to ' + x.latest + '. Holiday months dip because new buyers flood in.' }));
    mount('#mix-wf', Charts.waterfall({ steps: x.waterfall, unit: 'n', title: 'Returning orders, ' + x.last_year_month + ' to ' + x.latest + ', by channel',
      note: 'Simulated. Returning orders are orders minus new-customer orders per channel. A channel absent last year counts in full.' }));
    mount('#mix-moves', el('span', { class: 'kicker', text: 'Moves from the mix' }),
      ...(x.moves.length ? x.moves.map((m) => UI.actionCard(m, { compact: true, screen: SLUG })) : [el('p', { class: 'muted small', text: 'No mix rule fired. Returning share is steady and owned channels keep pace.' })]));
  }

  // ---------- desk: served and not served ----------
  const QUAD = { core: ['keep', 'Core: grow it'], fix_first: ['fix', 'Fix first'], scale: ['scale', 'Scale it'], park: ['wait', 'Park'] };
  const SEG = { gap: ['new', 'Gap'], watch: ['watch', 'Watch'], hold: ['keep', 'Hold'], own: ['scale', 'We own it'] };
  function renderServed(x, avatars) {
    const byKey = {}; for (const a of avatars) byKey[a.key] = a;
    document.getElementById('served-sub').textContent = 'Left: each avatar by its share of buyers against how well we serve it (five-star share on its doubts). Lines at the median share and the all-doubt five-star share. ' +
      'Right: buying situations competitors push, against the avatars we hold. ' + x.line;
    mount('#served-map', Charts.positioningMap({
      x: { label: 'share of buyers', lo: 'fewer', hi: 'more', unit: '%', min: 0, max: Math.max(...x.points.map((q) => q.x), 0.01) * 1.4 },
      y: { label: 'served well', lo: 'poorly', hi: 'well', unit: '%', min: 0, max: 1 },
      points: x.points, midX: x.mid_x, midY: x.mid_y, width: 560, height: 360, sizeUnit: 'n', usLabel: 'our avatars', themLabel: 'category',
      quadrants: ['Small, served well: scale', 'Core: grow', 'Small, served poorly: park', 'Big, served poorly: fix first'],
      title: 'Avatars by reach and how well we serve them',
      note: 'Share is a rough estimate from public reviews. Not placed: ' + (x.unplaced.map((u) => u.name + ' (' + u.why + ')').join(', ') || 'none') + '.' }),
      UI.verdictTable({
        columns: [{ key: 'name', label: 'Avatar' }, { key: 'share', label: 'Share', unit: '%' }, { key: 'served', label: 'Served', unit: '%' }],
        rows: x.verdicts.map((v) => Object.assign({}, v, { actions: byKey[v.key] ? [{ label: 'Next build', onClick: () => briefPanel(Object.assign({ kind: byKey[v.key].next.kind }, byKey[v.key].next)) }] : [] })),
        verdict: { at: 1, kind: (r) => QUAD[r.quadrant][0], text: (r) => QUAD[r.quadrant][1] }, actions: { label: 'Do' }, sort: false,
      }));
    mount('#served-segs', el('h4', { text: 'Buying situations: us against the category' }),
      UI.verdictTable({
        columns: [{ key: 'segment', label: 'Situation' }, { key: 'ours_t', label: 'Our avatars' }, { key: 'theirs_t', label: 'Who pushes it' }],
        rows: x.segments.map((sg) => Object.assign({}, sg, { ours_t: sg.ours.join(', ') || 'none',
          theirs_t: (sg.theirs.join(', ') || 'no competitor') + (sg.reddit_mentions == null ? '' : '; Reddit ' + sg.reddit_mentions),
          actions: sg.action ? [{ label: 'Size it', onClick: () => briefPanel(sg.action) }] : [{ label: 'Nothing new', cls: 'quiet', onClick: () => {} }] })),
        verdict: { at: 1, kind: (r) => SEG[r.verdict][0], text: (r) => SEG[r.verdict][1] }, actions: { label: 'Do' }, sort: false,
      }),
      el('p', { class: 'micro faint', text: 'Gap: 2 or more competitors push it and we hold no avatar with quotes for it. Watch: 1 competitor or Reddit only. Competitor positioning is a signal, not proof the segment pays.' }));
  }

  function renderDrafts(drafts) {
    mount('#drafts', ...drafts.map((d) => {
      const status = el('span', { class: 'micro muted', 'aria-live': 'polite' });
      const add = el('button', { class: 'btn soft sm', type: 'button', text: d.exists ? 'In the brain' : 'Add as provisional avatar', disabled: d.exists });
      add.addEventListener('click', async () => {
        status.textContent = 'Saving';
        try { const r = await api(BASE + 'avatars/draft', { method: 'POST', body: { segment: d.segment } }); status.textContent = 'Added ' + r.record + '. Reload to see it.'; add.disabled = true; }
        catch (e) { status.textContent = 'Could not add: ' + e.message; }
      });
      const src = Object.entries(d.by_source).map(([k, n]) => k + ' ' + n).join(', ') || 'none';
      return el('article', { class: 'card flat draftav' },
        el('div', { class: 'row between' }, el('b', { text: 'Draft avatar: ' + d.record.value.name }), el('span', { class: 'chip warn', text: 'inferred' })),
        el('div', { class: 'small', text: d.mentions + ' mentions in the language bank (' + src + '). ' + d.quotes + ' quotes we may show. Served by ' + (d.record.value.competitors_serving.join(', ') || 'no competitor') + '.' }),
        el('div', { class: 'micro muted', text: 'Job, share and pains stay unavailable until buyers are asked. Adding it makes it a provisional avatar every screen can brief against.' }),
        el('div', { class: 'row' }, add, status));
    }));
  }

  // ---------- desk: order-level paths ----------
  function renderPaths(x) {
    document.getElementById('paths-sub').textContent = 'Gateway products, the second-order path, win-back timing from order gaps and value cells. Order-level rules; they read the customer_paths aggregate.';
    if (!x.available) {
      mount('#paths', el('div', { class: 'card flat connect' },
        el('b', { text: 'Unavailable: ' + x.reason + '.' }),
        el('p', { class: 'small', text: 'The rules are built and wait on the data. When the aggregate lands, this section fills with no change to the page.' }),
        el('ul', { class: 'small' }, ...x.rules.map((r) => el('li', { text: r }))),
        el('p', { class: 'micro faint', text: 'Shape asked of the data layer: ' + x.shape })));
      return;
    }
    const V = { gateway: ['scale', 'Gateway'], dead_end: ['cut', 'Dead end'], normal: ['keep', 'Normal'] };
    mount('#paths', el('div', { class: 'grid side-wide' },
      el('div', { class: 'card tight' }, UI.verdictTable({
        columns: [{ key: 'sku_group', label: 'First product' }, { key: 'first_buyers', label: 'First buyers', unit: 'n' }, { key: 'repeat_180d', label: 'Repeat 180d', unit: '%' },
          { key: 'ratio', label: 'x median', unit: 'x' }, { key: 'next_t', label: 'Next they buy' }],
        rows: x.products.map((p) => Object.assign({}, p, { next_t: p.next ? p.next.sku_group + ', ' + Math.round(p.next.share * 100) + ' percent, day ' + p.next.median_days : 'no clear path' })),
        verdict: { at: 1, kind: (r) => V[r.verdict][0], text: (r) => V[r.verdict][1] }, sort: false })),
      el('div', { class: 'stack' }, ...x.moves.map((m) => UI.actionCard({ id: m.id, title: m.title, severity: 'medium', owner: m.owner, capability: m.capability, steps: m.steps,
        why: m.draft.split('\n')[1] || '', artefact: { kind: m.kind, label: KIND_LABEL[m.kind] || m.kind, draft: m.draft } }, { compact: true, screen: SLUG })))));
  }

  // ---------- desk: claims under fire ----------
  function renderClaims(x) {
    document.getElementById('claims-sub').textContent = 'Every site-backed or approved claim in the brain against ' + x.complaints +
      ' one and two star reviews (Reddit left out). Under fire: 3 or more use the claim\'s own feature words, product names left out. ' + x.line;
    const V = { under_fire: ['stop', 'Under fire'], watch: ['watch', 'Watch'], clear: ['keep', 'Clear'] };
    mount('#claims', UI.verdictTable({
      columns: [{ key: 'claim', label: 'Claim' }, { key: 'hits', label: '1 and 2 star', unit: 'n' }, { key: 'words_t', label: 'Words they throw back' }, { key: 'example_t', label: 'Example' }],
      rows: x.rows.map((r) => Object.assign({}, r, { words_t: r.words.join(', ') || 'none', example_t: r.example ? '"' + r.example + '"' : '',
        actions: r.action ? [{ label: 'Fix the claim', onClick: () => briefPanel(r.action) }] : [{ label: 'Keep', cls: 'quiet', onClick: () => {} }] })),
      verdict: { at: 1, kind: (r) => V[r.verdict][0], text: (r) => V[r.verdict][1] }, actions: { label: 'Do' }, sort: false,
    }), el('p', { class: 'micro faint', text: 'Word matches, not a legal review. A person decides whether a claim changes.' }));
  }

  // ---------- desk: lookalike pages ----------
  function renderLookalikes(x) {
    document.getElementById('look-sub').textContent = 'Pages the Ad Library pull flags as likely impostors: our name, ads, links to another site. ' + x.line;
    if (!x.rows.length) { mount('#look', el('p', { class: 'muted small', text: x.line })); return; }
    mount('#look', ...x.rows.map((r) => UI.actionCard({ id: r.action.id, title: r.action.title, severity: 'high', owner: 'person',
      why: r.ads_seen + ' ads from page ' + r.page_id + ', first seen ' + r.created + ', linking to ' + r.links_to + '. ' + (r.note || ''),
      capability: r.action.capability, steps: r.action.steps, artefact: { kind: 'ticket', label: 'a Meta report, a support macro and a social note', draft: r.action.draft } },
      { compact: true, screen: SLUG, extra: r.ad_library ? el('a', { href: r.ad_library, target: '_blank', rel: 'noopener', class: 'small', text: 'Open in the Ad Library' }) : null })));
  }

  // ---------- desk: moments ----------
  function renderMoments(x) {
    document.getElementById('moments-sub').textContent = 'Moments named in avatar triggers, matched to US dates, 6 months ahead. Ads live 21 days before, emails 14 days before. Index: that month last year against the 12-month average, simulated. ' + x.line;
    if (!x.rows.length) { mount('#moments-tl', el('p', { class: 'muted small', text: x.line })); mount('#moments'); return; }
    const items = [];
    for (const r of x.rows) {
      items.push({ when: fmt.date(r.ad_by), who: 'agent drafts', title: 'Ads live for ' + r.label, text: r.avatars.join(', '), tone: r.late ? 'bad' : 'warn' });
      items.push({ when: fmt.date(r.email_by), who: 'agent drafts', title: 'Emails scheduled for ' + r.label, text: '2 emails' });
      items.push({ when: fmt.date(r.starts), who: 'moment', title: r.label + ' starts', text: r.sales_index_last_year ? 'Last year ' + r.sales_index_last_year + 'x the monthly average' : 'index unavailable', tone: 'good' });
    }
    items.sort((a, b) => new Date(a.when) - new Date(b.when));
    mount('#moments-tl', UI.timeline(items));
    mount('#moments', ...x.rows.map((r) => UI.actionCard({ id: r.action.id, title: r.action.title, severity: r.late ? 'high' : 'medium', owner: r.action.owner,
      why: r.label + ' starts ' + r.starts + '. Ads live by ' + r.ad_by + '.' + (r.sales_index_last_year ? ' Last year it sold at ' + r.sales_index_last_year + 'x the monthly average.' : ''),
      capability: r.action.capability, steps: r.action.steps, check_on: r.action.check_on,
      artefact: { kind: r.action.kind, label: 'a dated plan: ad briefs and 2 emails', draft: r.action.draft } }, { compact: true, screen: SLUG })));
  }

  // ---------- desk: misreads ----------
  const LINE_V = { problem: ['cut', 'Problem'], split: ['watch', 'Split'], fine: ['keep', 'Fine'] };
  function renderMisreads(x) {
    if (!x.available) { mount('#misread-lines', UI.emptyState({ screen: SLUG, title: 'Review themes unavailable', text: x.reason })); return; }
    document.getElementById('misread-sub').textContent = 'Review themes by product line against what each avatar hires us for. A misread: the avatar buys the line (2 or more linked reviews), ' +
      'a top complaint hits its own job or pains, and the line is at or above the median 1 and 2 star share (' + Math.round(x.median * 1000) / 10 + ' percent). ' + x.line;
    mount('#misread-lines', el('h4', { text: 'Product lines: complaints against the median' }), UI.verdictTable({
      columns: [{ key: 'line_t', label: 'Line' }, { key: 'neg_share', label: '1 and 2 star', unit: '%' }, { key: 'ratio', label: 'x median', unit: 'x' },
        { key: 'issues_t', label: 'Top complaints' }, { key: 'praise_t', label: 'Praise' }],
      rows: x.lines.map((l) => Object.assign({}, l, { line_t: pretty(l.line), issues_t: l.issues.join('; '), praise_t: l.praise.join('; '),
        actions: l.action ? [{ label: 'Brief it', onClick: () => briefPanel(l.action) }] : l.avatars.length ? [{ label: 'See misreads', cls: 'quiet', onClick: () => document.getElementById('misreads').scrollIntoView({ behavior: 'smooth' }) }] : [{ label: 'Nothing to do', cls: 'quiet', onClick: () => {} }] })),
      verdict: { at: 1, kind: (r) => LINE_V[r.verdict][0], text: (r) => LINE_V[r.verdict][1], reason: (r) => r.polar.length ? 'praised and blamed for: ' + r.polar.join(', ') : '' },
      actions: { label: 'Do' }, sort: false,
    }), el('p', { class: 'micro faint', text: 'Problem: 1.5x the median or more. Split: praise and complaints name the same trait, so set the expectation. From the review summaries in the brain, public reviews.' }));
    mount('#misreads', ...(x.rows.length ? x.rows.map((r) => el('article', { class: 'card misread' },
        el('div', { class: 'row between' }, el('b', { text: r.avatar }), el('span', { class: 'chip bad', text: pretty(r.line) + ' ' + Math.round(r.neg_share * 1000) / 10 + '%' })),
        el('div', { class: 'small', text: r.why }),
        el('div', { class: 'row' }, el('span', { class: 'chip', text: 'makes ' + (KIND_LABEL[r.action.kind] || pretty(r.action.kind)) }), UI.ownerChip(r.action.owner),
          el('button', { class: 'btn soft xs', type: 'button', text: 'Brief it', onclick: () => briefPanel(r.action) }))))
        : [el('p', { class: 'muted small', text: 'No misread found for this brain.' })]));
  }

  // ---------- desk: offer map ----------
  function renderOffers(x) {
    document.getElementById('offers-sub').textContent = 'Each cell: how many of the avatar\'s doubts that offer, policy or claim answers, from the ladder proof records. ' + x.line +
      (x.bare.length ? ' No offer or policy answers any doubt for: ' + x.bare.join(', ') + '.' : '');
    mount('#offers-tools', x.action ? el('button', { class: 'btn soft sm', type: 'button', text: 'Brief the offer test', onclick: () => briefPanel(x.action) }) : null);
    mount('#offers', UI.coverageMatrix({ rows: x.rows, cols: x.cols, cells: x.cells, unit: 'n', single: true, max: 3, corner: 'Avatar',
      note: 'Blank: this lever answers none of the avatar\'s doubts. Columns after the policies are offers no ladder uses yet.' }));
  }

  // ---------- desk: evidence gate ----------
  function renderGate(g) {
    document.getElementById('gate-sub').textContent = 'Each avatar against the checks a researcher runs before a launch. Core checks (bold) must all pass to leave provisional. Every red cell is a task. ' + g.line;
    const tbl = el('table', { class: 'gate' });
    tbl.append(el('thead', null, el('tr', null, el('th', { text: 'Avatar' }), el('th', { text: 'Status' }),
      ...g.checks.map((c) => el('th', { class: c.core ? 'core' : '', text: c.label })))));
    const body = el('tbody');
    for (const r of g.rows) {
      const tr = el('tr', null, el('td', { text: r.name }),
        el('td', null, UI.verdict(r.status === 'validated' ? 'keep' : 'wait', r.status === 'validated' ? 'Validated' : 'Provisional', r.passed + ' of ' + r.total + ' checks')));
      for (const c of g.checks) {
        const ok = r.checks[c.key];
        const task = r.tasks.find((t) => t.check === c.key);
        tr.append(el('td', { class: 'g ' + (ok ? 'ok' : 'no') }, ok ? el('span', { text: 'yes', 'aria-label': 'passes' })
          : el('button', { class: 'btn xs ' + (c.core ? 'soft' : 'quiet'), type: 'button', text: 'Fix', title: task ? task.title : '', onclick: () => task && briefPanel(task) })));
      }
      body.append(tr);
    }
    tbl.append(body);
    mount('#gate', el('div', { class: 'matrix-wrap' }, tbl), el('p', { class: 'micro faint', text: g.tasks + ' tasks in all. Checks read the avatar records and ladders in the brain only.' }));
  }

  // ---------- desk: four forces ----------
  function renderForces(x) {
    document.getElementById('forces-sub').textContent = 'Every line tied to an avatar (its quotes and the reviews behind its doubts, Reddit left out), coded by word patterns: push (the old way hurts), pull (what draws them), anxiety (what scares them), habit (what keeps them where they are, competitor names included). ' + x.line;
    const f = (k) => (r) => { const v = r.forces[k]; return v.n + (v.example ? '' : ''); };
    mount('#forces', UI.verdictTable({
      columns: [{ key: 'name', label: 'Avatar' }, { key: 'lines', label: 'Lines', unit: 'n' }, { key: 'push', label: 'Push', unit: 'n' }, { key: 'pull', label: 'Pull', unit: 'n' },
        { key: 'anxiety', label: 'Anxiety', unit: 'n' }, { key: 'habit', label: 'Habit', unit: 'n' }, { key: 'tension', label: 'Anxiety + habit', unit: '%' }],
      rows: x.rows.map((r) => Object.assign({}, r, { push: r.forces.push.n, pull: r.forces.pull.n, anxiety: r.forces.anxiety.n, habit: r.forces.habit.n,
        actions: r.action ? [{ label: 'Interview', onClick: () => briefPanel(r.action) }] : [{ label: 'Enough lines', cls: 'quiet', onClick: () => {} }] })),
      verdict: { at: 1, kind: (r) => r.under ? 'fix' : 'keep', text: (r) => r.under ? 'Under-researched' : 'Covered',
        reason: (r) => r.missing.length ? 'no lines for: ' + r.missing.join(', ') : '' },
      actions: { label: 'Do' }, sort: false,
    }), el('p', { class: 'micro faint', text: 'Under-researched: a force with no line, or anxiety plus habit under 15 percent of coded lines. Patterns are word lists, so read counts as direction, not a census.' }));
  }

  // ---------- desk: survey ----------
  function renderSurvey(x) {
    document.getElementById('survey-sub').textContent = 'A post-purchase survey where every question closes a gap named above. ' + x.line +
      ' Response rate is an assumption until the survey runs. Orders a day: ' + (x.orders_per_day == null ? NA : fmt.num(x.orders_per_day)) + ', simulated.';
    mount('#survey-tools', el('button', { class: 'btn soft sm', type: 'button', text: 'Open the survey draft', onclick: () => briefPanel(x.action) }));
    mount('#survey', el('ol', { class: 'survey' }, ...x.questions.map((q) => el('li', null, el('b', { text: q.q }), el('span', { class: 'chip', text: q.type }),
      el('div', { class: 'small muted', text: 'Closes: ' + q.closes + (q.gap_ids.length ? ' (' + q.gap_ids.length + ' gaps)' : '') }),
      q.options.length ? el('div', { class: 'micro', text: q.options.join(' | ') }) : null))));
  }

  // ---------- desk: copy gap ----------
  function renderGap(x) {
    if (!x.available) { mount('#gap', UI.emptyState({ screen: SLUG, title: 'Copy gap unavailable', text: x.reason })); return; }
    document.getElementById('gap-sub').textContent = 'Words in 3 or more praise reviews (4 and 5 star or praise themes, Reddit left out), checked against ' + x.our_records +
      ' site and founder records in the brain. Not a live crawl of every page. ' + x.line;
    mount('#gap-tools', x.action ? el('button', { class: 'btn soft sm', type: 'button', text: 'Brief the top ' + Math.min(5, x.missing), onclick: () => briefPanel(x.action) }) : null);
    mount('#gap', UI.verdictTable({
      columns: [{ key: 'word', label: 'Their word' }, { key: 'reviews', label: 'Praise reviews', unit: 'n' }, { key: 'ex', label: 'How they say it' }],
      rows: x.rows.map((r) => Object.assign({}, r, { ex: r.examples.map((e) => '"' + e + '"').join('  ') })),
      verdict: { at: 1, kind: (r) => r.verdict === 'missing' ? 'new' : 'keep', text: (r) => r.verdict === 'missing' ? 'We never say it' : 'We say it' },
      sort: false,
    }));
  }

  // ---------- desk: perception gap ----------
  function renderPerception(x) {
    if (!x.available) { mount('#perc-theirs', UI.emptyState({ screen: SLUG, title: 'Perception gap unavailable', text: x.reason })); return; }
    document.getElementById('perc-sub').textContent = 'Our positioning records (frame, category, price frame, proof points, pitch) against the words in ' + x.praise_reviews +
      ' praise reviews (4 and 5 star, Reddit left out). ' + x.line;
    mount('#perc-tools', UI.orientation([{ label: 'buyer words we share', value: x.score, unit: '%', tone: x.score < 0.5 ? 'bad' : null }]),
      el('button', { class: 'btn soft sm', type: 'button', text: 'Brief it', onclick: () => briefPanel(x.action) }));
    mount('#perc-theirs', el('h4', { text: 'Their top words, and whether we use them' }),
      el('div', { class: 'chips' }, ...x.theirs.map((t) => el('span', { class: 'chip ' + (t.in_positioning ? 'good' : 'bad'), text: t.word + ' ' + t.reviews }))),
      el('p', { class: 'micro faint', text: 'Green: our positioning uses it. Red: buyers say it, our positioning does not.' }));
    mount('#perc-ours', el('h4', { text: 'Our words buyers never echo' }),
      el('div', { class: 'chips' }, ...x.unechoed.map((w) => el('span', { class: 'chip', text: w }))),
      el('h4', { text: 'Our words buyers do echo' }),
      el('div', { class: 'chips' }, ...x.echoed.slice(0, 12).map((e) => el('span', { class: 'chip good', text: e.word + ' ' + e.reviews }))),
      el('p', { class: 'micro faint', text: 'Word stems, so read it as direction. Unechoed words can still be true; they belong in proof points, not the lead line.' }));
  }

  // ---------- desk: messaging hierarchy ----------
  function renderHierarchy(h) {
    document.getElementById('hier-sub').textContent = h.line + ' Approve it and it becomes a positioning record every screen reads.';
    const status = el('span', { class: 'micro muted', 'aria-live': 'polite' });
    const btn = el('button', { class: 'btn primary sm', type: 'button', text: h.approved ? 'Approved' : 'Approve as our messaging hierarchy', disabled: h.approved });
    btn.addEventListener('click', async () => {
      status.textContent = 'Saving';
      try { const r = await api(BASE + 'messaging/approve', { method: 'POST', body: {} }); status.textContent = 'Saved as ' + r.record + '.'; btn.disabled = true; btn.textContent = 'Approved'; }
      catch (e) { status.textContent = 'Could not save: ' + e.message; }
    });
    const text = ['MESSAGING HIERARCHY', '1. Lead: ' + h.lead, '   Now: ' + (h.frame || NA), '2. Proof points:']
      .concat(h.proofs.map((p, i) => '   ' + (i + 1) + ') ' + (p.text || p.id) + ' (' + p.five_star + ' five-star lines on the doubts it answers)'),
        ['3. Answer first: ' + (h.doubt ? h.doubt.doubt + ' (' + h.doubt.one_star + ' one-star)' : NA)]).join('\n');
    mount('#hier', el('div', { class: 'hier' },
      el('div', null, el('span', { class: 'kicker', text: '1. Lead' }), el('div', { class: 'lead', text: h.lead }), el('div', { class: 'small muted', text: 'Our frame now: ' + (h.frame || NA) })),
      el('div', null, el('span', { class: 'kicker', text: '2. Proof points, by five-star lines behind them' }),
        el('ol', null, ...h.proofs.map((p) => el('li', null, (p.text || p.id) + ' ', el('span', { class: 'chip good', text: p.five_star + ' five-star' }))))),
      el('div', null, el('span', { class: 'kicker', text: '3. Answer first' }),
        h.doubt ? el('div', null, '"' + h.doubt.doubt + '" ', el('span', { class: 'chip bad', text: h.doubt.one_star + ' one-star' })) : el('span', { class: 'na', text: NA }))),
      el('div', { class: 'row' }, btn, UI.copyButton({ label: 'Copy', text: () => text }), status));
  }

  // ---------- desk: hook bank ----------
  function renderHooks(h) {
    document.getElementById('hooks-sub').textContent = '2 to 4 word phrases in 3 or more distinct 4 and 5 star reviews, from ' + h.praise_reviews + ' praise reviews, Reddit left out. ' + h.line;
    const picked = new Set(h.rows.slice(0, 5));
    const grid = el('div', { class: 'hooks' }, ...h.rows.map((r) => {
      const cb = el('input', { type: 'checkbox', checked: picked.has(r) });
      cb.addEventListener('change', () => { if (cb.checked) picked.add(r); else picked.delete(r); });
      return el('label', { class: 'hook' }, cb, el('span', null, el('b', { text: '"' + r.hook + '"' }), ' ',
        el('span', { class: 'chip', text: r.reviews + ' reviews' }), el('span', { class: 'micro muted', text: ' ' + r.avatars.join(', ') })));
    }));
    mount('#hooks-tools', el('button', { class: 'btn soft sm', type: 'button', text: 'Brief the picked hooks', onclick: () => {
      const lines = h.brief.head.concat(['', 'Hooks:'], Array.from(picked).map((r) => '- "' + r.hook + '" (' + r.reviews + ' reviews; ' + r.avatars.join(', ') + ')'));
      briefPanel(Object.assign({}, h.brief, { draft: lines.join('\n') }));
    } }));
    mount('#hooks', grid);
  }

  // ---------- desk: theme impact ----------
  function divBar(v, max) {
    const w = Math.round(50 * Math.min(1, Math.abs(v) / (max || 1)));
    return el('span', { class: 'dbar', title: String(v) }, el('i', { class: v < 0 ? 'neg' : 'pos', style: (v < 0 ? 'right:50%;' : 'left:50%;') + 'width:' + w + '%' }));
  }
  function renderThemes(x) {
    if (!x.available) { mount('#themes', UI.emptyState({ screen: SLUG, title: 'Theme impact unavailable', text: x.reason })); return; }
    document.getElementById('themes-sub').textContent = 'Impact = share of rated reviews with the theme x (average stars with it minus without it), from ' + x.rated +
      ' rated public reviews in the brain. Rising: last 90 days share 1.5x the earlier share, with 5 or more reviews. ' + x.line;
    const max = Math.max(...x.rows.map((r) => Math.abs(r.impact)));
    const rows = x.rows.map((r) => Object.assign({}, r, { theme_t: pretty(r.theme), bar: '', gap_t: (r.star_gap > 0 ? '+' : '') + r.star_gap + ' stars',
      actions: r.action ? [{ label: r.impact < 0 ? 'Fix it' : 'Lead with it', onClick: () => briefPanel(r.action) }] : [{ label: 'No ladder', cls: 'quiet', onClick: () => {} }] }));
    const t = UI.verdictTable({
      columns: [{ key: 'theme_t', label: 'Theme' }, { key: 'bar', label: 'Impact on stars' }, { key: 'share', label: 'Share', unit: '%' },
        { key: 'avg_with', label: 'Avg with', align: 'right', format: (v) => v.toFixed(2) }, { key: 'avg_without', label: 'Avg without', align: 'right', format: (v) => v.toFixed(2) }, { key: 'gap_t', label: 'Gap' }, { key: 'reviews', label: 'Reviews', unit: 'n' }],
      rows, verdict: { at: 1, kind: (r) => r.impact < 0 ? (r.rising ? 'stop' : 'fix') : 'scale', text: (r) => r.impact < 0 ? (r.rising ? 'Rising cost' : 'Costs stars') : 'Earns stars' },
      actions: { label: 'Do' }, sort: false,
    });
    t.querySelectorAll('tbody tr').forEach((tr, i) => { if (tr.children[2]) tr.children[2].replaceChildren(divBar(rows[i].impact, max)); });
    mount('#themes', t, el('p', { class: 'micro faint', text: 'A public sample, skewed to unhappy buyers. Read it as a ranking of what to fix first, not a forecast of stars.' }));
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
    renderOffers(d.offer_map);
    renderGate(d.gate);
    renderForces(d.forces);
    renderSurvey(d.survey);
    renderCoverage(d.coverage, d.formats);
    renderLadders(d.ladders, d.avatars);
    renderGap(d.copy_gap);
    renderPerception(d.perception);
    renderHierarchy(d.hierarchy);
    renderHooks(d.hooks);
    renderThemes(d.themes);
    renderWords(d.words, d.avatars);
    renderServed(d.served, d.avatars);
    renderDrafts(d.drafts);
    renderMisreads(d.misreads);
    renderClaims(d.claims_fire);
    renderLookalikes(d.lookalikes);
    renderMoments(d.moments);
    renderPaths(d.paths);
    renderCohorts(d.cohorts);
    renderMix(d.mix);
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
