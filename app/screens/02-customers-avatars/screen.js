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
    const m = a.meta || {};
    const chips = [];
    if (m.focus_rank) chips.push(el('span', { class: 'chip ' + (m.focus_rank === 1 ? 'accent' : ''), text: 'build rank ' + m.focus_rank + ' of ' + m.focus_of }));
    if (m.ads) chips.push(el('span', { class: 'chip ' + (m.ads === 'silent' || m.ads === 'under' ? 'bad' : ''), text: 'ads: ' + m.ads }));
    if (m.returns != null) chips.push(el('span', { class: 'chip ' + (m.returns >= 1.25 ? 'bad' : ''), text: 'returns ' + m.returns + 'x median' }));
    if (m.speaks) chips.push(el('span', { class: 'chip', text: m.speaks === 'marketplace' ? 'speaks on Amazon' : 'speaks on our site' }));
    if (m.split && m.split !== 'focused') chips.push(el('span', { class: 'chip warn', text: m.split === 'split' ? 'may be two buyers' : 'broad' }));
    card.append(el('div', { class: 'chans' }, ...chips));
    card.append(el('div', { class: 'small ' + (m.unknown && m.unknown.length ? 'unknown' : 'muted') },
      m.unknown && m.unknown.length ? el('span', null, el('b', { text: 'We do not know yet: ' }), m.unknown.join(', ').toLowerCase() + '.') : 'Every evidence check passes.'));
    const quotes = a.quotes.filter((q) => q.source !== 'Reddit').slice(0, 2);
    for (const q of quotes) card.append(el('blockquote', null, '"' + q.quote + '" ', link(q.ref, q.source || undefined)));
    if (!a.quotes.length) card.append(el('p', { class: 'muted small', text: 'No customer quotes. This avatar is a guess until customers say it.' }));
    const op = el('button', { class: 'btn quiet xs', type: 'button', text: 'One page to take away' });
    op.addEventListener('click', () => openAvatarPage(a.key, op));
    card.append(op, nextBuild(a.next));
    return card;
  }

  // ---------- keyboard: j and k move between plan items and actions, Enter opens the steps, ? lists the keys; Esc closes panels (kit)
  const KEY_ITEMS = '#plan .plan-item, #actions article.action';
  const KEYS = [['j', 'next plan item or action'], ['k', 'previous one'], ['Enter', 'open or close how it gets done'], ['Esc', 'close a panel'], ['?', 'this list']];
  function keyItems() { return Array.from(document.querySelectorAll(KEY_ITEMS)).filter((n) => n.offsetParent !== null); }
  function focusItem(n) {
    keyItems().forEach((x) => { x.tabIndex = -1; });
    n.tabIndex = 0; n.focus(); n.scrollIntoView({ block: 'nearest' });
  }
  document.addEventListener('keydown', (e) => {
    if (e.defaultPrevented || e.metaKey || e.ctrlKey || e.altKey) return;
    const t = e.target;
    if (t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT|BUTTON|A)$/.test(t.tagName))) return;
    if (document.querySelector('.panel-backdrop')) return;
    if (e.key === '?') {
      e.preventDefault();
      UI.panel({ title: 'Keys', body: el('ul', null, ...KEYS.map(([k, what]) => el('li', null, el('b', { text: k }), ' ' + what))) });
      return;
    }
    const items = keyItems();
    if (!items.length) return;
    const cur = items.indexOf(t && t.closest ? t.closest(KEY_ITEMS) : null);
    if (e.key === 'j' || e.key === 'k') {
      e.preventDefault();
      focusItem(items[e.key === 'j' ? Math.min(items.length - 1, cur + 1) : Math.max(0, cur - 1)]);
    } else if (e.key === 'Enter' && cur >= 0) {
      const b = Array.from(items[cur].querySelectorAll('button')).find((x) => /steps|How it gets done|^Hide$/.test(x.textContent));
      if (b) { e.preventDefault(); b.click(); }
    }
  });

  // one avatar, one page: Copy gives plain text, Print prints only the page
  async function openAvatarPage(key, btn) {
    let r;
    try { r = await api(BASE + 'avatar/' + encodeURIComponent(key) + '/brief'); } catch (e) { if (btn) btn.textContent = 'Could not load: ' + e.message; return; }
    const body = el('div', { class: 'report' }, el('p', { class: 'small muted print-head', text: r.header }),
      ...r.sections.map((s) => el('section', null, el('h3', { text: s.title }), el('ul', null, ...s.lines.map((l) => el('li', { text: l }))))));
    UI.panel({ title: r.title, body,
      tools: [UI.copyButton({ label: 'Copy', text: () => r.title + '\n\n' + r.text }),
        el('button', { class: 'btn sm', type: 'button', text: 'Print', onclick: () => { document.body.classList.add('print-report'); window.print(); document.body.classList.remove('print-report'); } })],
      onClose: () => document.body.classList.remove('print-report') });
  }

  // ---------- desk: avatar by channel ----------
  function briefPanel(b) {
    const sized = [b.size ? 'Size: ' + b.size.text : null, b.stop_rule ? 'Stop if: ' + b.stop_rule : null, b.check_on ? 'Check on: ' + fmt.date(b.check_on) : null].filter(Boolean);
    const brief = [b.title, '', 'Owner: ' + pretty(b.owner)].concat(sized, ['', 'Steps:'], b.steps.map((s) => s.n + '. ' + s.text + ' (' + s.who + ')'), ['', b.draft]).join('\n');
    UI.panel({
      title: b.title,
      tools: [UI.copyButton({ label: 'Copy brief', text: () => brief })],
      body: el('div', { class: 'stack' },
        el('div', { class: 'row' }, UI.ownerChip(b.owner), el('span', { class: 'chip', text: 'makes ' + (KIND_LABEL[b.kind] || pretty(b.kind)) }), el('span', { class: 'chip mono', text: b.capability.id })),
        sized.length ? el('p', { class: 'small', text: sized.join('. ') + '.' }) : null,
        el('pre', { class: 'draft', text: b.draft }),
        el('ol', { class: 'a-steps' }, ...b.steps.map((s) => el('li', null, s.text, el('span', { class: 'who', text: ' (' + s.who + ')' })))),
        UI.decisionRow({ capability: b.capability, owner: b.owner, screen: SLUG, finding_id: b.id })),
    });
  }
  function cellPanel(cell, row, col) {
    if (!cell || !cell.rungs || !cell.rungs.length) {
      UI.panel({ title: row.label + ' in ' + col.label, body: el('p', { class: 'muted', text: 'No doubt of this avatar needs an answer in ' + col.label.toLowerCase() + '.' }) });
      return;
    }
    UI.panel({ title: row.label + ' in ' + col.label, tools: cell.brief ? [el('button', { class: 'btn soft sm', type: 'button', text: 'Brief the open ones', onclick: () => briefPanel(cell.brief) })] : [],
      body: el('div', { class: 'stack' }, el('p', { class: 'small muted', text: cell.us + ' of ' + cell.them + ' doubts answered with proof here.' }),
        ...cell.rungs.map((r) => el('div', { class: 'card flat' }, el('div', { class: 'row between' }, el('b', { text: '"' + r.doubt + '"' }),
          el('span', { class: 'chip ' + (r.proof ? 'good' : 'bad'), text: r.proof ? 'answered' : 'open' })),
          el('div', { class: 'small', text: r.one_star + ' one-star, ' + r.five_star + ' five-star' }),
          el('div', { class: 'small muted', text: r.proof ? 'Proof: ' + r.proof : 'No proof on file yet.' })))) });
  }
  function renderCoverage(c, f) {
    document.getElementById('cover-sub').textContent = 'Each cell: doubts answered with proof | doubts that channel must answer, from the objection ladders. ' + c.line;
    mount('#cover', UI.coverageMatrix({
      rows: c.rows, cols: c.cols, cells: c.cells, unit: 'n', corner: 'Avatar',
      gapRule: (cell) => !cell || cell.them == null ? '' : cell.open ? 'gap' : 'lead',
      action: { label: 'Brief it', onClick: (cell) => cell && cell.brief && briefPanel(cell.brief) },
      onCell: (cell, row, col) => cellPanel(cell, row, col),
      note: 'Red: a doubt with no answer there, click Brief it. Green: every doubt answered. n/a: no doubt needs that channel. Click any cell to see the doubts behind it.' +
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
  function rungPanel(r) {
    const src = Object.entries(r.sources || {}).filter(([, n]) => n).map(([k, n]) => pretty(k) + ' ' + n).join(', ') || NA;
    const list = (label, qs, tone) => el('div', { class: 'stack' }, el('span', { class: 'kicker', text: label }),
      ...(qs.length ? qs.map((q) => el('blockquote', { class: 'q ' + tone, text: '"' + q + '"' })) : [el('span', { class: 'na', text: 'none on file' })]));
    UI.panel({ title: '"' + r.doubt + '"', tools: r.action ? [el('button', { class: 'btn soft sm', type: 'button', text: 'Brief it', onclick: () => briefPanel(r.action) })] : [],
      body: el('div', { class: 'stack' },
        el('div', { class: 'small' }, pretty(r.theme) + ', rung ' + r.level + '. ' + r.one_star + ' one-star, ' + r.five_star + ' five-star. Mentions by source: ' + src + '. Reddit counts as language only.'),
        el('div', { class: 'small' }, el('b', { text: 'Proof: ' }), r.proof || 'none on file'),
        el('div', { class: 'small' }, el('b', { text: 'Avatars: ' }), r.avatar_names.join(', ') || 'none named'),
        el('div', { class: 'grid two' }, list('One-star lines', r.one_star_quotes, 'bad'), list('Five-star lines', r.five_star_quotes, 'good'))) });
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
        actions: { label: 'Do' }, sort: false, maxRows: 40, empty: 'No rung names this avatar yet.', onRow: (r) => rungPanel(r),
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

  // ---------- desk: brand health ----------
  function renderHealth(x) {
    document.getElementById('health-sub').textContent = 'Monthly lines from our own store data, 12 full months, simulated. Rules: repeat in months 1 to 3 down 3 points over the last 3 cohorts; tickets per 1,000 orders up 20 percent over 3 months. ' + (x.line || x.reason || '');
    if (!x.available) { mount('#health', UI.emptyState({ screen: SLUG, title: 'Health line unavailable', text: x.reason })); }
    else mount('#health', Charts.trendStrip({ rows: x.rows, title: 'Brand health, ' + x.months[0] + ' to ' + x.months[x.months.length - 1] }),
      el('p', { class: 'micro faint', text: 'A gap in a line is a month with no full cohort yet, not a zero.' }));
    const connect = x.missing.map(([label, src, fix]) => UI.actionCard({ id: SLUG + '.health.connect.' + label.replace(/\W+/g, '_'), title: 'Connect ' + src + ' for the ' + label + ' line',
      why: 'The ' + label + ' line is unavailable until ' + src + ' is connected.', severity: 'low', status: 'unavailable', owner: 'person',
      steps: [{ n: 1, who: 'person', text: fix }, { n: 2, who: 'agent', text: 'Backfill 12 months and add the line here.' }],
      artefact: { kind: 'connector_setup', label: src + ' connected, read-only' } }, { compact: true, screen: SLUG }));
    mount('#health-moves', ...x.moves.map((m) => UI.actionCard({ id: m.id, title: m.title, why: m.why, severity: 'medium', owner: m.owner, capability: m.capability, steps: m.steps,
      artefact: { kind: m.kind, label: 'a cause review', draft: m.draft } }, { compact: true, screen: SLUG })), ...connect);
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

  // ---------- desk: doubt timing ----------
  function renderTiming(x) {
    document.getElementById('timing-sub').textContent = '1 and 2 star reviews behind each ladder theme, by month of year, Reddit left out. A season: the theme\'s share of all complaints in 3 months is 1.5x its share over the year, with 4 or more. Share of all complaints corrects for months the review pull over-samples. ' + x.line;
    mount('#timing', UI.coverageMatrix({ rows: x.rows, cols: x.cols, cells: x.cells, single: true, max: x.max, unit: 'n', corner: 'Theme',
      note: 'A public review sample: read seasons as direction, and re-check when the reviews app is connected.' }));
    mount('#timing-moves', ...x.moves.map((m) => UI.actionCard({ id: m.id, title: m.title, why: m.why + (m.late ? ' The season has started: ship now.' : ' Live by ' + m.ship_by + '.'),
      severity: m.late ? 'high' : 'medium', owner: m.owner, capability: m.capability, steps: m.steps, check_on: m.ship_by,
      artefact: { kind: m.kind, label: 'a seasonal answer on the page, in email and in support', draft: m.draft } }, { compact: true, screen: SLUG })));
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

  // ---------- how strong is each read ----------
  function renderStrength(rows) {
    const thin = rows.filter((r) => r.verdict === 'thin');
    document.getElementById('strength-sum').textContent = 'How strong is each read? ' + (thin.length ? thin.length + ' thin: ' + thin.map((r) => r.block).join(', ') + '.' : 'Every block rests on a fair sample.');
    const widen = { id: SLUG + '.strength.widen', title: 'Widen the thin reads', kind: 'research_note', owner: 'agent_drafts', severity: 'low',
      capability: { id: 'BRAND-C01', autonomy: 'agent_does' }, why: thin.map((r) => r.block + ': ' + r.n + ' ' + r.basis + ', under ' + r.thin_at).join('. '),
      steps: [{ n: 1, who: 'agent', text: 'Plan the extra review and ad pulls, by page id, inside the weekly cap.' },
        { n: 2, who: 'person', text: 'Approve the spend before any pull runs.' }, { n: 3, who: 'agent', text: 'Run the pulls and re-read the thin blocks.' }],
      artefact: { kind: 'research_note', label: 'a pull plan with its cost', draft: 'DRAFT pull plan\n' + thin.map((r) => '- ' + r.block + ': from ' + r.n + ' to ' + (r.thin_at * 2) + ' ' + r.basis).join('\n') } };
    mount('#strength', UI.table({ columns: [{ key: 'block', label: 'Block' }, { key: 'tab', label: 'Tab' }, { key: 'n', label: 'Sample', unit: 'n' }, { key: 'basis', label: 'Of what' },
      { key: 'verdict', label: 'Read', format: (v, r) => v === 'thin' ? 'thin, under ' + r.thin_at : v } ], rows, sort: false }),
      thin.length ? UI.actionCard(widen, { compact: true, screen: SLUG }) : null);
  }

  // ---------- desk: price doubts ----------
  function renderPrice(x) {
    const f = x.facts || {};
    document.getElementById('price-sub').textContent = 'Share of each avatar\'s one-star mentions that sit on price rungs. Price-led: 30 percent or more. Facts from the brain offers and products; per-pair price by pack is unavailable until pack prices are in the brain. ' + x.line;
    mount('#price-tools', UI.orientation([
      { label: 'free shipping from', value: f.free_shipping_at, unit: '$' }, { label: 'lowest single pair', value: f.lowest_single, unit: '$' },
      { label: 'shipping on one pair', value: f.shipping_on_one_pair, unit: '%' }, { label: 'pairs to free shipping', value: f.pairs_to_free_shipping, unit: 'n' }]));
    mount('#price', UI.verdictTable({
      columns: [{ key: 'name', label: 'Avatar' }, { key: 'price_share', label: 'Price share of one-star', unit: '%' }, { key: 'price_one_star', label: 'Price one-star', unit: 'n' }, { key: 'one_star', label: 'All one-star', unit: 'n' }],
      rows: x.rows.map((r) => Object.assign({}, r, { actions: r.action ? [{ label: 'Brief it', onClick: () => briefPanel(r.action) }] : [{ label: 'Not price-led', cls: 'quiet', onClick: () => {} }] })),
      verdict: { at: 1, kind: (r) => r.verdict === 'price_led' ? 'fix' : 'keep', text: (r) => r.verdict === 'price_led' ? 'Price-led' : 'Other' }, actions: { label: 'Do' }, sort: false,
    }));
  }

  // ---------- desk: re-check calendar ----------
  function renderRechecks(x) {
    document.getElementById('recheck-sub').textContent = 'Each avatar and ladder record stops being trusted on its expiry date. Due: within 30 days. ' + x.line +
      (x.no_date ? ' ' + x.no_date + ' records carry no expiry; they are re-checked on each review pull.' : '');
    const S = { expired: ['bad', 'expired'], due: ['warn', 'due'], ok: ['good', 'ok'], no_date: ['', 'no date'] };
    mount('#recheck', UI.table({ columns: [{ key: 'label', label: 'Record' }, { key: 'kind', label: 'Kind' }, { key: 'expires', label: 'Expires', format: (v) => v ? fmt.date(v) : 'no date' },
      { key: 'days_left', label: 'Days left', unit: 'n' }, { key: 'status', label: 'Status', format: (v) => S[v][1] }], rows: x.rows, sort: false, maxRows: 30 }));
    mount('#recheck-act', ...(x.action ? [UI.actionCard(Object.assign({}, x.action, { why: x.line, severity: 'low', artefact: { kind: x.action.kind, label: 'record updates proposed to the review queue', draft: x.action.draft } }), { compact: true, screen: SLUG })] : []));
  }

  // ---------- desk: marketplace voice ----------
  function renderMarket(x) {
    document.getElementById('market-sub').textContent = 'Where each avatar\'s reviews come from: its quotes plus the rated reviews behind its doubts, Reddit left out. Marketplace-led: half or more on Amazon; those get a listing fix for 20-marketplaces. The review pull samples Amazon heavily, so read shares as direction. ' + x.line;
    mount('#market', UI.verdictTable({
      columns: [{ key: 'name', label: 'Avatar' }, { key: 'amazon_share', label: 'On Amazon', unit: '%' }, { key: 'reviews', label: 'Reviews', unit: 'n' },
        { key: 'src_t', label: 'Sources' }, { key: 'doubt_t', label: 'Top Amazon doubts' }],
      rows: x.rows.map((r) => Object.assign({}, r, { src_t: Object.entries(r.sources).slice(0, 4).map(([k, n]) => k + ' ' + n).join(', '),
        doubt_t: r.amazon_doubts.map((d) => d.doubt + ' (' + d.n + ')').join('; ') || 'none',
        actions: r.action ? [{ label: 'Fix the listing', onClick: () => briefPanel(r.action) }] : [{ label: 'Site-led', cls: 'quiet', onClick: () => {} }] })),
      verdict: { at: 1, kind: (r) => r.verdict === 'marketplace' ? 'watch' : 'keep', text: (r) => r.verdict === 'marketplace' ? 'Marketplace' : 'Site' },
      actions: { label: 'Do' }, sort: false,
    }));
  }

  // ---------- desk: support replies ----------
  function renderMacros(x) {
    document.getElementById('macros-sub').textContent = 'A reply for every doubt the ladders send to support, from the proof on file, or from a policy a person checks. It never promises what is not on file. ' + x.line;
    mount('#macros-tools', UI.copyButton({ label: 'Copy all replies', text: () => x.rows.map((m) => m.draft).join('\n\n') }));
    const S = { ready: ['good', 'ready'], check: ['warn', 'check the policy'], person: ['bad', 'a person writes it'] };
    mount('#macros', ...x.rows.map((m) => el('article', { class: 'card flat macro' },
      el('div', { class: 'row between' }, el('b', { text: '"' + m.doubt + '"' }), el('span', { class: 'chip ' + S[m.status][0], text: S[m.status][1] })),
      el('pre', { class: 'draft', text: m.draft.split('\n').slice(2).join('\n') }),
      el('div', { class: 'row' }, UI.copyButton({ label: 'Copy', cls: 'quiet xs', text: () => m.draft }),
        UI.decisionRow({ capability: m.action.capability, owner: m.action.owner, screen: SLUG, compact: true, finding_id: m.action.id })))));
  }

  // ---------- desk: return risk ----------
  function renderReturns(x) {
    document.getElementById('returns-sub').textContent = 'Return risk per avatar: the lines it buys, weighted by how often, times each line\'s 1 and 2 star share and the share of its top complaints that are fit or wear. High: 1.25x the median avatar. A proxy from public reviews until ticket and return reasons are aggregated. ' + (x.line || '');
    mount('#returns-tools', UI.orientation([{ label: 'refunds, last 3 months', value: x.refund_share_3m, unit: '%', title: 'refunds on orders over net sales, simulated' }]));
    mount('#returns', UI.verdictTable({
      columns: [{ key: 'name', label: 'Avatar' }, { key: 'ratio', label: 'x median', unit: 'x' }, { key: 'driver_t', label: 'Driven by' }, { key: 'lines_t', label: 'Lines it buys' }],
      rows: (x.rows || []).map((r) => Object.assign({}, r, { driver_t: pretty(r.driver) + (r.driver_issue ? ': ' + r.driver_issue : ''),
        lines_t: Object.entries(r.lines).map(([k, n]) => pretty(k) + ' ' + n).join(', '),
        actions: r.action ? [{ label: 'Brief it', onClick: () => briefPanel(r.action) }] : [{ label: 'Watch', cls: 'quiet', onClick: () => {} }] })),
      verdict: { at: 1, kind: (r) => r.verdict === 'high' ? 'fix' : 'keep', text: (r) => r.verdict === 'high' ? 'High' : 'Normal' }, actions: { label: 'Do' }, sort: false,
    }));
    const t = x.tickets || {};
    mount('#returns-side', UI.actionCard({ id: SLUG + '.returns.connect', title: 'Aggregate tickets and returns by reason and line', severity: 'medium', status: 'unavailable', owner: 'person',
      why: 'Unavailable: ' + (t.reason || 'no aggregate') + '. With it, this table reads real return reasons per avatar instead of review complaints.',
      steps: [{ n: 1, who: 'person', text: t.fix || 'Ask the data session for the aggregate.' }, { n: 2, who: 'agent', text: 'Swap the proxy for real reasons and re-rank.' }],
      artefact: { kind: 'connector_setup', label: 'a tickets and returns aggregate, read-only' } }, { compact: true, screen: SLUG }));
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

  // ---------- desk: compare two avatars ----------
  function renderCompare(c) {
    const keys = Object.keys(c.rows);
    if (keys.length < 2) { mount('#compare', el('p', { class: 'muted small', text: 'Two avatars are needed to compare.' })); return; }
    const pick = (i) => { const s = el('select', { 'aria-label': 'Avatar ' + (i + 1) }, ...keys.map((k) => el('option', { value: k, text: c.rows[k].name }))); s.value = keys[i]; return s; };
    const a = pick(0), b = pick(1);
    const show = (v, u) => v == null ? NA : u === '%' ? Math.round(v * 1000) / 10 + ' percent' : u === 'x' ? v + 'x' : String(v);
    const draw = () => {
      const A = c.rows[a.value], B = c.rows[b.value];
      const rows = c.fields.map((f) => ({ label: f.label, a: show(A[f.key], f.unit), b: show(B[f.key], f.unit) }));
      const diff = rows.filter((r) => r.a !== r.b);
      const pageA = el('button', { class: 'btn soft sm', type: 'button', text: 'Page for ' + A.name });
      const pageB = el('button', { class: 'btn soft sm', type: 'button', text: 'Page for ' + B.name });
      pageA.addEventListener('click', () => openAvatarPage(a.value, pageA));
      pageB.addEventListener('click', () => openAvatarPage(b.value, pageB));
      const differences = () => [A.name + ' against ' + B.name + ': where they differ', ''].concat(diff.map((r) => r.label + ': ' + r.a + ' | ' + r.b)).join('\n');
      mount('#compare', UI.table({ columns: [{ key: 'label', label: '' }, { key: 'a', label: A.name }, { key: 'b', label: B.name }], rows, sort: false }),
        el('div', { class: 'row compare-do' }, pageA, pageB, UI.copyButton({ label: 'Copy the ' + diff.length + ' differences', text: differences })));
      document.querySelectorAll('#compare tbody tr').forEach((tr) => { if (tr.children[1] && tr.children[1].textContent !== tr.children[2].textContent) tr.classList.add('diff'); });
    };
    a.addEventListener('change', draw); b.addEventListener('change', draw);
    mount('#compare-tools', a, el('span', { class: 'muted small', text: 'against' }), b);
    draw();
  }

  // ---------- desk: focus ----------
  function renderFocus(x) {
    const w = x.weights;
    document.getElementById('focus-sub').textContent = 'Score out of 100: share of buyers ' + Math.round(w.share * 100) + ', how poorly we serve them ' + Math.round(w.unserved * 100) +
      ', how little our ads speak to them ' + Math.round(w.ad_gap * 100) + ', share of their doubts still open ' + Math.round(w.open_doubts * 100) + '. Share is from reviews; marked "sales" where reviews give none and the share of sales by line stands in. ' + x.line;
    mount('#focus', UI.verdictTable({
      columns: [{ key: 'name', label: 'Avatar' }, { key: 'score', label: 'Score', unit: 'n' }, { key: 'share', label: 'Buyers', unit: '%' },
        { key: 'served', label: 'Served', unit: '%' }, { key: 'open_doubts', label: 'Open doubts', unit: 'n' }, { key: 'next_t', label: 'Next build' }],
      rows: x.rows.map((r, i) => Object.assign({}, r, { rank: i, next_t: r.next.title, name: r.share_source === 'sales' ? r.name + ' (share from sales)' : r.name,
        actions: [{ label: 'Brief it', onClick: () => briefPanel(r.next) }] })),
      verdict: { at: 1, kind: (r) => r.rank === 0 ? 'scale' : r.score >= 60 ? 'fix' : 'keep', text: (r) => r.rank === 0 ? 'Next' : r.score >= 60 ? 'Soon' : 'Later' },
      actions: { label: 'Do' }, sort: false,
    }));
  }

  // ---------- desk: who our ads speak to ----------
  function renderAdVoice(x) {
    if (!x.available) { mount('#voiceads', UI.emptyState({ screen: SLUG, title: 'Ad read unavailable', text: x.reason })); return; }
    document.getElementById('voiceads-sub').textContent = 'Our live ads by hook, from the Ad Library read in the brain, matched to the avatar whose name the hook speaks to, against each avatar\'s share of buyers. Under: less than half its share. ' + x.line;
    const V = { silent: ['stop', 'Silent'], under: ['fix', 'Under'], fair: ['keep', 'Fair'], over: ['watch', 'Heavy'] };
    const rows = x.rows.map((r) => Object.assign({}, r, { bar: '', actions: r.action ? [{ label: 'Brief it', onClick: () => briefPanel(r.action) }] : [{ label: 'Keep', cls: 'quiet', onClick: () => {} }] }));
    const t = UI.verdictTable({
      columns: [{ key: 'name', label: 'Avatar' }, { key: 'buyer_share', label: 'Buyers', unit: '%' }, { key: 'ad_share', label: 'Live ads', unit: '%' }, { key: 'bar', label: 'Buyers | ads' }],
      rows, verdict: { at: 1, kind: (r) => V[r.verdict][0], text: (r) => V[r.verdict][1] }, actions: { label: 'Do' }, sort: false });
    t.querySelectorAll('tbody tr').forEach((tr, i) => { const r = rows[i]; if (r && tr.children[4]) tr.children[4].replaceChildren(el('span', { class: 'pair' },
      el('i', { class: 'b', style: 'width:' + Math.round(200 * (r.buyer_share || 0)) + 'px' }), el('i', { class: 'a', style: 'width:' + Math.round(200 * Math.min(1, r.ad_share || 0)) + 'px' }))); });
    mount('#voiceads', t, el('p', { class: 'small', text: 'Ads that name no avatar: ' + x.unmatched.map((u) => u.hook + ' (' + u.ads + ')').join(', ') + '.' }),
      el('p', { class: 'micro faint', text: 'Hooks come from a read of our Ad Library page, signals only. Tag ads with the naming convention and this reads exact.' }));
  }

  // ---------- desk: split check ----------
  function renderSplit(x) {
    document.getElementById('split-sub').textContent = 'Product lines behind each avatar (its own reviews count 3 times a review linked through a doubt) and its doubt themes. Split: 2 lines each hold 30 percent or more and draw different complaints. Broad: 3 or more doubt themes, none at half. ' + x.line;
    const V = { split: ['fix', 'Two buyers'], broad: ['watch', 'Broad'], focused: ['keep', 'One buyer'] };
    mount('#split', UI.verdictTable({
      columns: [{ key: 'name', label: 'Avatar' }, { key: 'lines_t', label: 'Lines behind it' }, { key: 'themes_t', label: 'Doubt themes' }],
      rows: x.rows.map((r) => Object.assign({}, r, { lines_t: Object.entries(r.lines).slice(0, 4).map(([k, n]) => pretty(k) + ' ' + n).join(', ') || 'none linked',
        themes_t: Object.keys(r.themes).map(pretty).join(', ') || 'none',
        actions: r.action ? [{ label: r.verdict === 'split' ? 'Split it' : 'Check it', onClick: () => briefPanel(r.action) }] : [{ label: 'Keep', cls: 'quiet', onClick: () => {} }] })),
      verdict: { at: 1, kind: (r) => V[r.verdict][0], text: (r) => V[r.verdict][1] }, actions: { label: 'Do' }, sort: false,
    }));
  }

  // ---------- desk: do reviews and sales agree on who buys ----------
  function renderSalesShare(x) {
    document.getElementById('salesshare-sub').textContent = 'Each line\'s store sales over 12 full months, split across avatars by their share of that line\'s linked reviews, against each avatar\'s share from reviews. Differ: 1.5x either way. ' + (x.line || x.reason || '');
    if (!x.available) { mount('#salesshare', el('p', { class: 'muted', text: 'Unavailable: ' + x.reason + '.' })); return; }
    const V = { agree: ['keep', 'Agree'], sales_higher: ['watch', 'Sales higher'], reviews_higher: ['fix', 'Reviews higher'], sales_only: ['watch', 'Sales only'], unavailable: ['wait', 'Unavailable'] };
    const pct = (v) => v == null ? 'unavailable' : Math.round(v * 1000) / 10 + ' percent';
    mount('#salesshare', UI.verdictTable({
      columns: [{ key: 'name', label: 'Avatar' }, { key: 'rev_t', label: 'From reviews' }, { key: 'sales_t', label: 'Of sales' }, { key: 'usd_t', label: 'Sales, 12 months' }],
      rows: x.rows.map((r) => Object.assign({}, r, { rev_t: pct(r.review_share), sales_t: pct(r.sales_share), usd_t: r.sales_usd == null ? 'unavailable' : fmt.money(r.sales_usd),
        actions: r.action ? [{ label: 'Settle it', onClick: () => briefPanel(r.action) }] : [{ label: 'Keep', cls: 'quiet', onClick: () => {} }] })),
      verdict: { at: 1, kind: (r) => V[r.verdict][0], text: (r) => V[r.verdict][1] }, actions: { label: 'Do' }, sort: false,
    }));
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
    const btn = el('button', { class: 'btn primary sm', type: 'button', text: h.approved ? 'Approved' : !h.available ? 'Nothing to approve yet' : 'Approve as our messaging hierarchy', disabled: h.approved || !h.available });
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

  function renderNaming(n) {
    mount('#naming', el('div', { class: 'row between' }, el('b', { text: 'Name ads so this matrix can count them' }),
      el('div', { class: 'row' }, UI.copyButton({ label: 'Copy the convention', text: () => n.spec }), el('button', { class: 'btn soft sm', type: 'button', text: 'Steps', onclick: () => briefPanel(n.action) }))),
      el('p', { class: 'small', text: 'Tags in any ad name: AV-<avatar>, ANG-<doubt theme>, FMT-<format>, HK-<hook>. Example: ' + (n.example || NA) }),
      el('p', { class: 'micro faint', text: 'Keys come from the brain: ' + n.avatars.length + ' avatars, ' + n.angles.length + ' doubt themes. Once live ads carry them, the ads column of this matrix fills with no other change.' }));
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

  function checkBox() {
    const card = el('article', { class: 'card vo' });
    const text = el('textarea', { placeholder: 'Paste a headline, ad line or email opener to check', maxlength: 600, 'aria-label': 'Line to check' });
    const out = el('div', { class: 'checks', 'aria-live': 'polite' });
    const V = { pass: 'good', warn: 'warn', fail: 'bad' };
    const run = async () => {
      if (!text.value.trim()) { out.textContent = 'Paste a line first.'; return; }
      try {
        const r = await api(BASE + 'voice/check', { method: 'POST', body: { text: text.value } });
        mount(out, el('div', { class: 'row' }, el('b', { text: 'Verdict: ' }), el('span', { class: 'chip ' + V[r.verdict], text: r.verdict })),
          el('ul', null, ...r.checks.map((c) => el('li', null, el('span', { class: 'chip ' + V[c.status], text: c.status }), ' ', c.why))));
      } catch (e) { out.textContent = 'Could not check: ' + e.message; }
    };
    card.append(el('b', { text: 'Does this line sound like us?' }),
      el('p', { class: 'muted small', text: 'Checks sentence length, reading grade, em dashes, inflated words, unproven claim words, forbidden claims, lines marked not us, and whether it uses buyer words. Nothing is saved.' }),
      el('div', { class: 'examples' }, text, el('button', { class: 'btn primary sm', type: 'button', text: 'Check it', onclick: run })), out);
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
    return [sheet, exampleBox(v, reload), checkBox()];
  }

  // ---------- 1. the plan ----------
  const isOpen = (a) => a.status !== 'unavailable';
  function exportCsv(actions) {
    UI.csv(actions.map((a, i) => ({ rank: i + 1, title: a.title, owner: a.owner, severity: a.severity, status: a.status,
      total: a.rubric && a.rubric.total, artefact: a.artefact && a.artefact.kind, why: a.why })), null, 'customers-avatars-plan.csv');
  }
  let planJob = 'all';
  function renderPlan(d, r) {
    const acts = r.actions || [];
    const open = acts.filter(isOpen).filter((a) => planJob === 'all' || a.job === planJob);
    const win = r.window || {};
    const counts = {}; for (const a of acts.filter(isOpen)) counts[a.job] = (counts[a.job] || 0) + 1;
    const pills = UI.pills({ items: [{ key: 'all', label: 'All jobs', n: acts.filter(isOpen).length }].concat(DESK.map((t) => ({ key: t.key, label: t.label, n: counts[t.key] || 0 }))),
      current: planJob, onChange: (k) => { planJob = k; renderPlan(d, r); } });
    const openTab = planJob === 'all' ? null : el('button', { class: 'btn quiet sm', type: 'button', text: 'Open the ' + DESK.find((t) => t.key === planJob).label + ' desk',
      onclick: () => { if (deskTabs) { deskTabs.show(planJob); document.getElementById('desk-wrap').scrollIntoView({ behavior: 'smooth' }); } } });
    mount('#plan', UI.planBoard({
      title: 'Next moves for our customers', sub: 'Brain as of ' + fmt.date(d.today) + '. Sales numbers ' + (win.days || 28) + ' days to ' + fmt.date(win.ends_on) + '.',
      orient: d.orientation, actions: open, limit: 10, screen: SLUG,
      tools: [pills, openTab, el('button', { class: 'btn sm', type: 'button', text: 'Export CSV', onclick: () => exportCsv(acts) })].filter(Boolean),
      foot: el('div', { class: 'row', style: { gap: '14px' } }, UI.rubricLegend(),
        el('span', { class: 'micro faint', text: 'Ranked by the shared rubric. "Not now" snoozes 14 days. Approved items go to the master list on the brand brain.' })),
      empty: planJob === 'all' ? 'No open move. Every avatar is grounded and every top doubt has proof.' : 'No open move in this job.',
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
    const cards = acts.map((a, i) => UI.actionCard(a, { expanded: i === 0, screen: SLUG, onDecision: () => load() }));
    const LIMIT = 6;
    const list = document.getElementById('actions');
    mount(list, ...cards.slice(0, LIMIT));
    if (cards.length > LIMIT) {
      const more = el('button', { class: 'btn sm', type: 'button', text: 'Show all ' + cards.length });
      more.addEventListener('click', () => { mount(list, ...cards); more.remove(); });
      mount('#actions-tools', more);
    }
    renderSnoozed(r.snoozed || []);
  }

  // ---------- depth rule 14: what the founder put off, with the date and the day it comes back
  function renderSnoozed(rows) {
    const box = document.getElementById('snoozed');
    if (!rows.length) { mount(box); box.hidden = true; return; }
    box.hidden = false;
    mount(box, el('details', null,
      el('summary', { text: rows.length + ' put off with "Not now". Each comes back after 14 days.' }),
      el('ul', { class: 'snoozed-list' }, ...rows.map((a) => el('li', null,
        el('b', { text: a.title }), ' ',
        el('span', { class: 'muted', text: 'Not now on ' + fmt.date(a.decision.time) + '. Back on ' + fmt.date(a.decision.back_on) + '.' + (a.decision.reason ? ' ' + a.decision.reason : '') }))))));
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

  // ---------- since your last visit (this browser only) ----------
  function renderSince(d, r) {
    const key = 'ecomos.' + SLUG + '.' + d.brand + '.seen';
    const now = { version: d.version, at: d.today, ids: (r.actions || []).filter(isOpen).map((a) => a.id) };
    let before = null;
    try { before = JSON.parse(localStorage.getItem(key) || 'null'); } catch (e) { before = null; }
    try { localStorage.setItem(key, JSON.stringify(now)); } catch (e) { /* storage blocked: the strip just stays hidden */ }
    const box = document.getElementById('since');
    if (!before || !Array.isArray(before.ids)) { box.hidden = true; return; }
    const was = new Set(before.ids), is = new Set(now.ids);
    const added = (r.actions || []).filter((a) => isOpen(a) && !was.has(a.id));
    const gone = before.ids.filter((id) => !is.has(id)).length;
    if (!added.length && !gone && before.version === now.version) { box.hidden = true; return; }
    box.hidden = false;
    mount(box, el('b', { text: 'Since your last visit' + (before.at ? ' on ' + fmt.date(before.at) : '') + ': ' }),
      el('span', { text: added.length + ' new move' + (added.length === 1 ? '' : 's') + ', ' + gone + ' resolved or merged' + (before.version !== now.version ? ', the brain changed.' : '.') }),
      ...added.slice(0, 3).map((a) => el('span', { class: 'chip accent', text: a.title.length > 60 ? a.title.slice(0, 57) + '...' : a.title })));
  }

  // ---------- the monthly report ----------
  async function openReport() {
    let r;
    try { r = await api(BASE + 'report'); } catch (e) { UI.panel({ title: 'Report unavailable', body: el('p', { text: e.message }) }); return; }
    const body = el('div', { class: 'report' }, el('p', { class: 'small muted print-head', text: r.header }),
      ...r.sections.map((s) => el('section', null, el('h3', { text: s.title }), el('ul', null, ...s.lines.map((l) => el('li', { text: l }))))));
    const pnl = UI.panel({ title: r.title, body,
      tools: [UI.copyButton({ label: 'Copy', text: () => r.title + '\n' + r.header + '\n\n' + r.text }),
        el('button', { class: 'btn sm', type: 'button', text: 'Print', onclick: () => { document.body.classList.add('print-report'); window.print(); document.body.classList.remove('print-report'); } })],
      onClose: () => document.body.classList.remove('print-report') });
    return pnl;
  }
  document.getElementById('report-btn').addEventListener('click', openReport);

  // ---------- the next 30 days ----------
  async function renderAgenda() {
    let x;
    try { x = await api(BASE + 'agenda'); } catch (e) { mount('#agenda', el('p', { class: 'muted', text: 'Agenda unavailable: ' + e.message })); return; }
    document.getElementById('agenda-sub').textContent = 'Ads-live and email dates for avatar moments, seasonal ship-by dates, record re-checks, dated checks and test starts. ' + x.line;
    mount('#agenda', UI.verdictTable({
      columns: [{ key: 'date', label: 'Date', format: (v) => fmt.date(v) }, { key: 'days_t', label: 'When' }, { key: 'kind', label: 'Kind' }, { key: 'what', label: 'What' }, { key: 'owner_t', label: 'Who' }],
      rows: x.items.map((i) => Object.assign({}, i, { days_t: i.overdue ? Math.abs(i.days) + ' days late' : i.days === 0 ? 'today' : 'in ' + i.days + ' days',
        owner_t: i.owner === 'person' ? 'a person' : i.owner === 'agent' ? 'agent' : 'agent drafts, you approve' })),
      verdict: { at: 1, kind: (r) => r.overdue ? 'stop' : r.days <= 7 ? 'fix' : 'wait', text: (r) => r.overdue ? 'Overdue' : r.days <= 7 ? 'This week' : 'Coming' },
      sort: false, empty: 'Nothing dated in the next 30 days.',
    }));
  }

  // ---------- tests proposed to 25-experiments ----------
  async function renderTests() {
    let t;
    try { t = await api(BASE + 'tests'); } catch (e) { mount('#tests', el('p', { class: 'muted', text: 'Tests unavailable: ' + e.message })); return; }
    document.getElementById('tests-sub').textContent = t.rows.length + ' tests in the experiment registry shape, status proposed. ' + t.note;
    mount('#tests-tools', UI.copyButton({ label: 'Copy as JSON', text: () => JSON.stringify(t.rows, null, 1) }));
    mount('#tests', UI.verdictTable({
      columns: [{ key: 'hypothesis', label: 'Hypothesis' }, { key: 'metric_t', label: 'Metric' }, { key: 'days', label: 'Days', unit: 'n' },
        { key: 'audience_t', label: 'Audience' }, { key: 'read_point', label: 'Read on', format: (v) => fmt.date(v) }],
      rows: t.rows.map((r) => Object.assign({}, r, { metric_t: r.metric.name.replace(/_/g, ' ') + ', ' + r.metric.direction, days: r.metric.min_days, audience_t: r.audience.join(', '),
        actions: [{ label: 'Copy row', onClick: () => UI.copy(JSON.stringify(r, null, 1)) }] })),
      verdict: { at: 0, kind: () => 'new', text: () => 'Proposed' }, actions: { label: 'Do' }, sort: false,
    }));
  }

  // ---------- decisions taken on this screen ----------
  const CHOICE = { agent: ['Agent does it', 'good'], person: ['Sent to a person', 'accent'], not_now: ['Not now', 'warn'] };
  async function renderDecided(actions) {
    let rows = [];
    try { const r = await api('/api/decisions?screen=' + SLUG); rows = Array.isArray(r) ? r : (r.decisions || r.rows || []); }
    catch (e) { mount('#decided', el('p', { class: 'muted small', text: 'Decisions log unavailable: ' + e.message })); return; }
    const byId = {}; for (const a of actions) byId[a.id] = a;
    rows = rows.filter((d) => d.screen === SLUG).slice().reverse();
    const counts = rows.reduce((o, d) => { o[d.choice] = (o[d.choice] || 0) + 1; return o; }, {});
    document.getElementById('decided-sub').textContent = rows.length ? rows.length + ' decisions: ' + Object.entries(counts).map(([k, n]) => n + ' ' + (CHOICE[k] ? CHOICE[k][0].toLowerCase() : k)).join(', ') + '. "Not now" comes back after 14 days.'
      : 'No decision yet. Approve, send or snooze any move above and it lands here with its check date.';
    if (!rows.length) { mount('#decided', el('p', { class: 'muted small', text: 'Nothing decided on this screen yet.' })); return; }
    mount('#decided', UI.timeline(rows.slice(0, 20).map((d) => {
      const a = byId[d.finding_id] || null;
      const back = d.choice === 'not_now' ? new Date(new Date(d.time).getTime() + 14 * 864e5) : null;
      return { when: fmt.date(d.time), who: (CHOICE[d.choice] || [d.choice])[0], tone: (CHOICE[d.choice] || [null, null])[1] === 'warn' ? 'warn' : 'good',
        title: a ? a.title : (d.finding_id || d.capability), text: back ? 'Back on the plan ' + fmt.date(back) : (a && a.check_on ? 'Check on ' + fmt.date(a.check_on) : (d.reason || '')) };
    })));
  }

  // ---------- hand-off packs ----------
  async function renderHandoff() {
    let h;
    try { h = await api(BASE + 'handoff'); } catch (e) { mount('#handoff', el('p', { class: 'muted', text: 'Hand-offs unavailable: ' + e.message })); return; }
    document.getElementById('handoff-sub').textContent = 'Ready artefacts for the screens that read avatars, the language bank and the objection map (events.md). ' + h.note;
    mount('#handoff', ...h.packs.map((p) => {
      const text = () => [p.label.toUpperCase() + ' PACK, brain ' + String(h.brain_version).slice(0, 7), ''].concat(p.items.map((i, n) => (n + 1) + '. ' + i.title + '\n' + i.draft)).join('\n\n');
      return el('article', { class: 'card flat pack' },
        el('div', { class: 'row between' }, el('b', { text: p.label }), el('span', { class: 'chip mono', text: p.screen })),
        el('div', { class: 'small', text: p.items.length + ' ready: ' + Object.entries(p.items.reduce((o, i) => { o[i.kind] = (o[i.kind] || 0) + 1; return o; }, {})).map(([k, n]) => n + ' ' + pretty(k)).join(', ') }),
        el('ul', { class: 'small' }, ...p.items.slice(0, 4).map((i) => el('li', { text: i.title }))),
        el('div', { class: 'row' }, UI.copyButton({ label: 'Copy the pack', text }), el('a', { class: 'btn quiet sm', href: '/screens/' + p.screen + '/', target: '_blank', rel: 'noopener', text: 'Open ' + p.label })));
    }));
  }

  // ---------- the desk, grouped into tabs by job ----------
  const DESK = [
    { key: 'avatars', label: 'Avatars', ids: ['focus-wrap', 'avatars-wrap', 'compare-wrap', 'salesshare-wrap', 'voiceads-wrap', 'split-wrap', 'gate-wrap', 'recheck-wrap', 'forces-wrap', 'survey-wrap', 'served-wrap', 'market-wrap', 'returns-wrap', 'misread-wrap'] },
    { key: 'doubts', label: 'Doubts and words', ids: ['ladders-wrap', 'cover-wrap', 'themes-wrap', 'words-wrap', 'hooks-wrap', 'gap-wrap', 'macros-wrap'] },
    { key: 'offers', label: 'Offers and claims', ids: ['offers-wrap', 'price-wrap', 'claims-wrap', 'timing-wrap'] },
    { key: 'retention', label: 'Retention', ids: ['paths-wrap', 'cohort-wrap', 'mix-wrap', 'moments-wrap', 'health-wrap'] },
    { key: 'brand', label: 'Brand and voice', ids: ['perc-wrap', 'hier-wrap', 'look-wrap', 'voice-wrap'] },
  ];
  let deskTabs = null;
  function buildDesk(actions) {
    const open = {};
    for (const t of DESK) {
      const box = document.getElementById('desk-' + t.key) || el('div', { id: 'desk-' + t.key, class: 'desk-panel' });
      for (const id of t.ids) { const sec = document.getElementById(id); if (sec) box.append(sec); }
      t.box = box;
      open[t.key] = 0;
    }
    const wanted = (location.hash.match(/tab=([a-z]+)/) || [])[1];
    deskTabs = UI.tabs({ items: DESK.map((t) => ({ key: t.key, label: t.label, n: t.ids.length, panel: t.box })),
      current: DESK.some((t) => t.key === wanted) ? wanted : 'avatars',
      onChange: (k) => { try { history.replaceState(null, '', '#tab=' + k); } catch (e) { /* no history in a sandbox */ } } });
    mount('#desk', deskTabs);
  }
  window.addEventListener('hashchange', () => { const k = (location.hash.match(/tab=([a-z]+)/) || [])[1]; if (deskTabs && DESK.some((t) => t.key === k)) deskTabs.show(k); });

  // ---------- window, gap and caveat on every desk block (depth rules 9 and 10)
  function renderBlocks(blocks) {
    for (const [id, b] of Object.entries(blocks || {})) {
      const sec = document.getElementById(id);
      if (!sec) continue;
      sec.querySelectorAll(':scope > .block-window, :scope > .sec-head > .block-window, :scope > .block-caveat, :scope > .block-gap').forEach((n) => n.remove());
      const head = sec.querySelector(':scope > .sec-head');
      const h2 = head && head.querySelector('h2');
      if (h2) h2.after(el('span', { class: 'block-window', text: b.window }));
      if (head && b.gap) head.after(el('p', { class: 'block-gap gap-' + b.gap.kind }, el('b', { text: 'Gap, ' + b.gap.label + ': ' }), b.gap.text));
      sec.append(el('p', { class: 'block-caveat', text: 'Caveat: ' + b.caveat }));
    }
  }

  async function load() {
    let d, r, a;
    try {
      [d, r, a] = await Promise.all([api(BASE + 'overview'), api(BASE + 'rank'), api(BASE + 'audit')]);
    } catch (e) {
      mount('#badge', 'Could not load customers: ' + e.message); return;
    }
    mount('#badge', el('span', null, el('b', { text: 'Simulated data. ' }), d.simulated_note));
    r.snoozed = (r.actions || []).filter((x) => x.status === 'snoozed');
    r.actions = (r.actions || []).filter((x) => x.status !== 'snoozed');
    renderPlan(d, r);
    renderSince(d, r);
    renderWrong(a, r);
    renderActions(r);
    renderOffers(d.offer_map);
    renderPrice(d.price);
    renderFocus(d.focus);
    renderCompare(d.compare);
    renderAdVoice(d.ad_voice);
    renderSalesShare(d.sales_share);
    renderSplit(d.split);
    renderGate(d.gate);
    renderStrength(d.strength);
    renderRechecks(d.rechecks);
    renderForces(d.forces);
    renderSurvey(d.survey);
    renderCoverage(d.coverage, d.formats);
    renderNaming(d.naming);
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
    renderReturns(d.returns);
    renderMarket(d.marketplace);
    renderMacros(d.macros);
    renderClaims(d.claims_fire);
    renderLookalikes(d.lookalikes);
    renderTiming(d.timing);
    renderMoments(d.moments);
    renderPaths(d.paths);
    renderCohorts(d.cohorts);
    renderHealth(d.health);
    renderMix(d.mix);
    mount('#avatars', ...(d.avatars.length ? d.avatars.map(avatarCard) : [el('p', { class: 'muted', text: 'No avatar records yet.' })]));
    document.getElementById('obj-note').textContent = 'Avatars come from the objection ladders. Ad coverage: ' +
      (d.angles.available ? 'counted from the ad table.' : d.angles.reason + '.') + ' Page coverage needs a live page scan.';
    mount('#objections', objectionTable(d.objections));
    mount('#language', ...d.language.themes.map(themeCard));
    mount('#voice', ...voiceCards(d.voice, load));
    renderBlocks(d.blocks);
    if (!deskTabs) buildDesk(r.actions || []);
    renderAgenda();
    renderTests();
    renderDecided((r.actions || []).concat(r.snoozed || []));
    renderHandoff();
    document.getElementById('audit-sub').textContent = a.findings.length + ' findings from ' + a.rules.length + ' rules. Brain version ' + String(a.brain_version || '').slice(0, 7) + '.';
    mount('#audit', auditTable(a.findings));
    mount('#rules', el('h4', { text: 'Rules' }), rulesTable(a.rules, a.findings));
  }

  load();
})();
