/* Setup: the onboarding flow. Website, documents, sources, brand numbers, first audit.
   All local and in mock mode. Data comes from /api/setup/* (api.py in this folder). */
(function () {
  'use strict';
  const el = UI.el;
  const BRAND = new URLSearchParams(location.search).get('brand') || 'bombas';
  const q = (path) => '/api/setup/' + path + (path.includes('?') ? '&' : '?') + 'brand=' + encodeURIComponent(BRAND);
  const CAT_NAMES = {
    store: 'Store platform', ads: 'Ad platforms', analytics: 'Analytics', email_sms: 'Email and SMS', reviews: 'Reviews',
    support: 'Customer support', fulfilment: 'Fulfilment and shipping', finance: 'Finance and accounting', payments: 'Payments',
    marketplaces: 'Marketplaces', documents: 'Documents and chat', social_organic: 'Organic social', seo_tools: 'SEO tools',
    affiliates_creators: 'Affiliates and creators', subscriptions: 'Subscriptions', content: 'Content', own: 'ecomOS tools',
    public: 'Public sources'
  };
  const CHOICE_LABEL = { connect: 'Connected (mock)', skip: 'Skipped for now', declined: 'Not comfortable' };
  const CHOICE_TONE = { connect: 'good', skip: '', declined: 'warn' };
  let S = null, auditResult = null, onb = null, onbTimer = null;
  const STATUS_TONE = { ok: 'good', mock: 'accent', waiting: 'warn', refused: 'bad', error: 'bad', skipped: '', pending: '' };
  const usd = (v) => (v === null || v === undefined) ? 'none' : '$' + Number(v).toFixed(2);

  const words = (s) => String(s || '').replace(/_/g, ' ');
  const chip = (text, tone) => el('span', { class: 'chip' + (tone ? ' ' + tone : ''), text });
  const msg = () => el('div', { class: 'msg', role: 'status' });
  function say(node, text, ok) { node.className = 'msg ' + (ok ? 'ok' : 'err'); node.textContent = text; }
  function head(n, title, done, text) {
    return [el('div', { class: 'step-head' }, el('span', { class: 'n', text: 'Step ' + n }), el('h3', { text: title }),
      done ? chip('done', 'good') : chip('to do')), text ? el('p', { class: 'muted', text }) : null];
  }
  function field(label, input, wide) { return el('label', { class: wide ? 'wide' : null }, label, input); }

  async function load() {
    try {
      S = await UI.api(q('state'));
    } catch (e) {
      UI.mount('#app', UI.emptyState({ title: 'Setup could not load', text: e.message, missing: ['/api/setup/state'] }));
      return;
    }
    render();
  }

  function stats() {
    const cats = S.categories.filter((c) => !c.public);
    const connected = cats.filter((c) => c.choice && c.choice.choice === 'connect').length;
    const answered = cats.filter((c) => c.choice).length;
    const fin = S.finance.fields.filter((f) => f.in_force).length;
    const mets = S.finance.metrics.filter((m) => m.available).length;
    const recs = S.sections.rows.reduce((a, r) => a + (r.records || 0), 0);
    return { cats, connected, answered, fin, mets, recs };
  }

  function render() {
    const st = stats();
    UI.mount('#badge', el('div', { class: 'sample-badge', role: 'note' }, el('span', null,
      el('b', { text: 'Bombas is the demo brand.' }),
      ' Facts come from public pages only. Every number on this page is simulated. Sources run in mock mode: nothing connects and nothing is sent.')));
    UI.mount('#note', UI.founderNote([
      'Start with your website. We read it and fill what we can. Then add documents, connect the tools you use, and enter the costs only you know.',
      'Nothing is required. A skipped step just means some numbers stay unavailable, and the page says which ones.'
    ]));
    UI.mount('#tiles',
      UI.tile({ name: 'Brain records', plain: 'facts found so far', value: st.recs, unit: 'n', window: 'all time' }),
      UI.tile({ name: 'Documents', plain: 'files added by you', value: S.documents.length, unit: 'n' }),
      UI.tile({ name: 'Sources connected', plain: 'of ' + st.cats.length + ' categories', value: st.connected, unit: 'n' }),
      UI.tile({ name: 'Brand numbers', plain: 'of ' + S.finance.fields.length + ' fields in force', value: st.fin, unit: 'n' }),
      UI.tile({ name: 'Money metrics', plain: 'of ' + S.finance.metrics.length + ' that can be computed', value: st.mets, unit: 'n' }));
    const done = [!!S.website, S.documents.length > 0, st.answered > 0, st.fin > 0, !!auditResult];
    UI.mount('#steps', ['Website', 'Documents', 'Sources', 'Brand numbers', 'First audit'].map((t, i) =>
      el('a', { href: '#step-' + (i + 1), class: 'chip' + (done[i] ? ' good' : ''), text: (i + 1) + '. ' + t })));
    renderWebsite(done[0]); renderOnboard(); renderDocs(done[1]); renderSources(done[2]); renderFinance(done[3]); renderAudit(done[4]);
  }

  // ---------- 1. website
  function renderWebsite(done) {
    const input = el('input', { class: 'text', type: 'text', value: (S.website && S.website.url) || 'bombas.com', 'aria-label': 'Website' });
    const out = msg();
    const btn = el('button', { class: 'btn primary', type: 'button', text: 'Read my site' });
    btn.addEventListener('click', async () => {
      btn.disabled = true;
      try {
        const r = await UI.api(q('crawl'), { method: 'POST', body: { url: input.value } });
        S.website = { url: r.url };
        say(out, r.matches_brand ? 'Read ' + r.url + ': ' + UI.fmt.int(r.records) + ' records across ' + r.sections.rows.length + ' sections.'
          : 'Mock mode reads no live site. Showing what the crawl found for the demo brand.', true);
        render();
      } catch (e) { say(out, e.message); } finally { btn.disabled = false; }
    });
    const rows = S.sections.rows.map((r) => ({ section: words(r.section), records: r.records, last_update: r.last_update, gist: r.gist }));
    UI.mount('#step-1', ...head(1, 'Enter your website', done, 'The crawler reads your pages, policies, products and ads, and fills the brain. Below is what it found.'),
      el('div', { class: 'form' }, field('Website', input), el('div', null, btn)), out,
      S.website ? UI.table({
        columns: [{ key: 'section', label: 'Section' }, { key: 'records', label: 'Records', unit: 'n', align: 'right' },
          { key: 'last_update', label: 'Last update' }, { key: 'gist', label: 'What it says' }],
        rows, sort: { key: 'records', dir: 'desc' }, maxRows: 30
      }) : null,
      S.website && S.sections.empty.length ? el('div', { class: 'chips' }, el('span', { class: 'muted small', text: 'Nothing found yet for:' }),
        S.sections.empty.map((s) => chip(words(s), 'warn'))) : null);
  }

  // ---------- 1b. onboarding run: every public lane, paid lanes in mock mode, then the 5 questions
  async function loadOnboard() {
    try { onb = await UI.api(q('onboard/status')); } catch (e) { onb = { error: e.message }; }
    renderOnboard();
    clearTimeout(onbTimer);
    if (onb && (onb.running || onb.thread_alive)) onbTimer = setTimeout(loadOnboard, 1500);
  }
  function renderOnboard() {
    if (!S) return;
    const url = el('input', { class: 'text', type: 'text', value: (S.website && S.website.url) || 'bombas.com', 'aria-label': 'Store url' });
    const name = el('input', { class: 'text', type: 'text', value: BRAND === 'bombas' ? 'Bombas' : '', 'aria-label': 'Brand name' });
    const fx = el('input', { type: 'checkbox', checked: BRAND === 'bombas' ? true : null });
    const out = msg();
    const running = onb && (onb.running || onb.thread_alive);
    const btn = el('button', { class: 'btn primary', type: 'button', text: running ? 'Running' : 'Run onboarding' });
    btn.disabled = !!running;
    btn.addEventListener('click', async () => {
      btn.disabled = true;
      try {
        await UI.api(q('onboard/start'), { method: 'POST', body: { url: url.value, name: name.value, fixtures: fx.checked } });
        say(out, 'Started. Paid lanes run in mock mode and cost nothing.', true);
        setTimeout(loadOnboard, 300);
      } catch (e) { say(out, e.message); btn.disabled = false; }
    });
    const body = [];
    if (onb && onb.error) body.push(el('div', { class: 'msg err', text: onb.error }));
    else if (onb && onb.started) {
      const p = onb.progress;
      body.push(el('div', { class: 'lanes' }, el('div', { class: 'small muted', text: p.finished + ' of ' + p.total + ' steps' + (onb.done ? ', done' : ', running') }),
        el('div', { class: 'bar' }, el('span', { style: 'width:' + Math.round(100 * p.finished / p.total) + '%' }))));
      body.push(el('div', { class: 'grid tiles' },
        UI.tile({ name: 'Records found', plain: 'across the lanes', value: onb.records, unit: 'n' }),
        UI.tile({ name: 'Paid lane estimates', plain: 'shown before each paid step', value: onb.estimate_usd, unit: 'usd' }),
        UI.tile({ name: 'Spent', plain: 'mock mode spends nothing', value: onb.cost_usd, unit: 'usd' })));
      body.push(UI.table({
        columns: [{ key: 'step', label: 'Lane' }, { key: 'kind', label: 'Kind' }, { key: 'status', label: 'Status' },
          { key: 'records', label: 'Records', unit: 'n', align: 'right' }, { key: 'estimate', label: 'Estimate', align: 'right' },
          { key: 'note', label: 'What happened' }],
        rows: onb.lanes.map((l) => ({ step: words(l.step), kind: l.kind, status: l.status, records: l.records,
          estimate: l.estimate_usd === null ? '' : usd(l.estimate_usd), note: l.note || '' })),
        sort: false, maxRows: 20
      }));
      if (onb.done) {
        body.push(el('h4', { text: onb.questions.length ? 'The ' + onb.questions.length + ' questions no source answered' : 'Nothing left to ask' }));
        body.push(el('div', { class: 'grid' }, onb.questions.map((a, i) => el('div', { class: 'card q' },
          el('div', { class: 'step-head' }, el('b', { text: (i + 1) + '. ' + a.asks }), el('span', { class: 'imp', text: 'importance ' + a.importance })),
          el('div', { class: 'small muted', text: 'Why: ' + a.why + '.' }),
          a.connect.length ? el('div', { class: 'chips' }, el('span', { class: 'muted small', text: 'Or connect:' }), a.connect.map((s) => chip(words(s), 'accent'))) : null,
          el('div', { class: 'chips' }, el('span', { class: 'muted small', text: 'Fills:' }), a.fills.map((f) => chip(words(f))))))));
        body.push(el('p', { class: 'small muted', text: 'Answer them in step 5. Paid lanes wait for you to confirm pages and subreddits; until then they show as waiting.' }));
      }
    }
    UI.mount('#onboard', el('div', { class: 'step-head' }, el('span', { class: 'n', text: 'Step 1b' }), el('h3', { text: 'Fill the brain from public sources' }),
      onb && onb.done ? chip('done', 'good') : chip(running ? 'running' : 'to do')),
      el('p', { class: 'muted', text: 'Reads your site, tech stack, Ad Library pages, Amazon, Reddit, press and job posts, then builds the brain and asks at most 5 questions. Each paid lane shows its cost first. Here they run in mock mode.' }),
      el('div', { class: 'form' }, field('Website', url), field('Brand name', name),
        el('label', { class: 'check' }, fx, 'Use saved pages (offline)'), el('div', null, btn)), out, ...body);
  }

  // ---------- 2. documents
  function renderDocs(done) {
    const file = el('input', { class: 'text', type: 'file', 'aria-label': 'File' });
    const note = el('textarea', { class: 'text', placeholder: 'What is this and why it matters' });
    const secs = el('select', { class: 'text', multiple: true, size: 4, 'aria-label': 'Sections it may inform' },
      S.section_names.map((s) => el('option', { value: s, text: words(s) })));
    const vis = el('select', { class: 'text' }, el('option', { value: 'private', text: 'Private' }), el('option', { value: 'public', text: 'Public' }));
    const out = msg();
    const btn = el('button', { class: 'btn primary', type: 'button', text: 'Add to the brain' });
    btn.addEventListener('click', async () => {
      const f = file.files && file.files[0];
      if (!f) return say(out, 'Pick a file first.');
      btn.disabled = true;
      try {
        await UI.api(q('documents'), { method: 'POST', body: { file: f.name, note: note.value,
          sections: Array.from(secs.selectedOptions).map((o) => o.value), visibility: vis.value } });
        S = await UI.api(q('state')); render();
      } catch (e) { say(out, e.message); btn.disabled = false; }
    });
    UI.mount('#step-2', ...head(2, 'Upload brand documents', done, 'Brand book, past decks, research. Each one is listed in the brain and read on the next pass. Local mode keeps a line in the manifest, not the file itself.'),
      el('div', { class: 'form' }, field('File', file), field('Visibility', vis), field('Sections it may inform (optional)', secs, true), field('Note', note, true),
        el('div', null, btn)), out,
      UI.table({
        columns: [{ key: 'file', label: 'File' }, { key: 'added_at', label: 'Added' }, { key: 'visibility', label: 'Visibility' },
          { key: 'sections', label: 'Sections', format: (v) => (v || []).map(words).join(', ') }, { key: 'note', label: 'Note' }],
        rows: S.documents, sort: false, empty: 'No documents yet.'
      }));
  }

  // ---------- 3. sources
  function catCard(c) {
    const sel = el('select', { class: 'text', 'aria-label': 'Source for ' + (CAT_NAMES[c.category] || c.category) },
      c.sources.map((s) => el('option', { value: s.id, text: s.name })));
    if (c.choice && c.choice.source) sel.value = c.choice.source;
    const out = msg();
    const detail = el('div', { class: 'small muted' });
    const showDetail = () => {
      const s = c.sources.find((x) => x.id === sel.value);
      detail.textContent = s ? 'Would pull: ' + (s.note || s.tables.map(words).join(', ') || 'records') + '. Mock mode, read-only.' : '';
    };
    sel.addEventListener('change', showDetail); showDetail();
    const send = async (choice) => {
      try {
        await UI.api(q('connect'), { method: 'POST', body: { category: c.category, choice, source: choice === 'connect' ? sel.value : null } });
        S = await UI.api(q('state')); auditResult = null; render();
      } catch (e) { say(out, e.message); }
    };
    const cur = c.choice && c.choice.choice;
    const b = (choice, label, cls) => el('button', { class: 'btn sm' + (cls ? ' ' + cls : '') + (cur === choice ? ' sel' : ''), type: 'button', text: label, onclick: () => send(choice) });
    return el('div', { class: 'card cat' },
      el('h4', null, el('span', { text: CAT_NAMES[c.category] || words(c.category) }), cur ? chip(CHOICE_LABEL[cur], CHOICE_TONE[cur]) : chip('not set')),
      c.sources.length > 1 ? sel : el('div', { class: 'small', text: c.sources[0].name }), detail,
      el('div', { class: 'chips' }, el('span', { class: 'muted small', text: 'Unlocks rooms:' }),
        c.rooms.length ? c.rooms.map((r) => chip(words(r), 'accent')) : chip('none yet')),
      el('div', { class: 'chips' }, el('span', { class: 'muted small', text: 'Fills:' }),
        c.sections.length ? c.sections.slice(0, 8).map((s) => chip(words(s))) : chip('data tables only'),
        c.sections.length > 8 ? chip('+' + (c.sections.length - 8)) : null),
      el('div', { class: 'btns' }, b('connect', 'Connect', 'primary'), b('skip', 'Skip', 'quiet'), b('declined', 'Not comfortable', 'quiet')), out);
  }
  function renderSources(done) {
    const pub = S.categories.filter((c) => c.public);
    UI.mount('#step-3', ...head(3, 'Connect your sources', done, 'Pick at most one tool per category. Each card says what it unlocks. Not comfortable means we ask you plainly instead and never nag about that tool again.'),
      el('div', { class: 'cats' }, S.categories.filter((c) => !c.public).map(catCard)),
      pub.length ? el('div', { class: 'card flat' }, el('b', { text: 'Public sources run for every brand' }),
        el('div', { class: 'chips' }, pub.flatMap((c) => c.sources).map((s) => chip(s.name)))) : null);
  }

  // ---------- 4. brand numbers
  function renderFinance(done) {
    const F = S.finance;
    const fsel = el('select', { class: 'text', 'aria-label': 'Field' }, F.fields.map((f) => el('option', { value: f.field, text: words(f.field) })));
    const scope = el('select', { class: 'text', 'aria-label': 'Scope' });
    const key = el('input', { class: 'text', type: 'text', placeholder: 'sku, carrier:zone, channel or vendor' });
    const value = el('input', { class: 'text', type: 'number', min: '0', step: 'any', inputmode: 'decimal' });
    const from = el('input', { class: 'text', type: 'date', value: S.today });
    const conf = el('select', { class: 'text' }, el('option', { value: 'estimate', text: 'My estimate' }), el('option', { value: 'invoice', text: 'From a bill' }));
    const note = el('input', { class: 'text', type: 'text', placeholder: 'invoice, contract or estimate' });
    const hint = el('div', { class: 'small muted wide' });
    const out = msg();
    const sync = () => {
      const f = F.fields.find((x) => x.field === fsel.value);
      scope.replaceChildren(...f.scope.map((s) => el('option', { value: s, text: words(s) })));
      key.disabled = scope.value === 'global';
      hint.textContent = f.what + ' Unit: ' + words(f.unit) + '.';
    };
    fsel.addEventListener('change', sync);
    scope.addEventListener('change', () => { key.disabled = scope.value === 'global'; });
    sync();
    const btn = el('button', { class: 'btn primary', type: 'button', text: 'Save number' });
    btn.addEventListener('click', async () => {
      btn.disabled = true;
      try {
        await UI.api(q('finance'), { method: 'POST', body: { field: fsel.value, scope: scope.value, scope_key: key.value,
          value: value.value === '' ? null : Number(value.value), effective_from: from.value, confidence: conf.value, note: note.value } });
        S = await UI.api(q('state')); render();
      } catch (e) { say(out, e.message); btn.disabled = false; }
    });
    const rows = F.fields.map((f) => ({ field: words(f.field), unit: words(f.unit), in_force: f.in_force || null,
      latest: f.latest ? f.latest.value : null, scope: f.latest ? words(f.latest.scope) : '', from: f.latest ? f.latest.effective_from : null,
      source: f.latest ? f.latest.confidence : null }));
    UI.mount('#step-4', ...head(4, 'Enter the numbers only you know', done, 'Product cost, shipping, fees, cash. The platforms do not have these. Each value has a start date, so past months do not move when a cost changes.'),
      el('div', { class: 'form' }, field('Field', fsel), field('Applies to', scope), field('Which one', key), field('Value', value),
        field('Starts on', from), field('Where from', conf), field('Note', note, true), hint, el('div', null, btn)), out,
      el('div', { class: 'metrics' }, F.metrics.map((m) => el('div', null, m.available ? chip('ready', 'good') : chip('unavailable', 'warn'),
        el('span', { text: words(m.metric) + (m.missing.length ? ': needs ' + m.missing.map(words).join(', ') : '') })))),
      UI.table({
        columns: [{ key: 'field', label: 'Field' }, { key: 'in_force', label: 'Rows in force', unit: 'n', align: 'right' },
          { key: 'latest', label: 'Value now', align: 'right', format: (v, r) => r.in_force > 1 ? 'varies by ' + r.scope : v == null ? 'unavailable' : UI.fmt.num(v) },
          { key: 'unit', label: 'Unit' }, { key: 'from', label: 'Since' }, { key: 'source', label: 'Source' }],
        rows, sort: false
      }));
  }

  // ---------- 5. first audit
  function questionCard(item) {
    const box = el('textarea', { class: 'text', placeholder: 'Answer in a line or two', 'aria-label': item.asks });
    const out = msg();
    const btn = el('button', { class: 'btn primary sm', type: 'button', text: 'Save answer' });
    btn.addEventListener('click', async () => {
      btn.disabled = true;
      try {
        const r = await UI.api(q('answer'), { method: 'POST', body: { question_id: item.id, answer: box.value } });
        say(out, 'Saved as ' + r.record.id + '. Founder records win over every other source.', true);
        setTimeout(runAudit, 900);
      } catch (e) { say(out, e.message); btn.disabled = false; }
    });
    return el('div', { class: 'card q' },
      el('div', { class: 'step-head' }, el('b', { text: item.asks }), el('span', { class: 'imp', text: 'importance ' + item.importance })),
      el('div', { class: 'small muted', text: 'Why: ' + item.why + '.' }),
      item.connect.length ? el('div', { class: 'chips' }, el('span', { class: 'muted small', text: 'Or connect:' }), item.connect.map((s) => chip(words(s), 'accent'))) : null,
      el('div', { class: 'chips' }, el('span', { class: 'muted small', text: 'Unblocks:' }), item.rooms.map((r) => chip(words(r)))),
      box, el('div', { class: 'btns' }, btn), out);
  }
  async function runAudit() {
    try { auditResult = await UI.api(q('audit')); render(); document.getElementById('step-5').scrollIntoView({ block: 'start' }); }
    catch (e) { auditResult = { error: e.message }; render(); }
  }
  function renderAudit(done) {
    const btn = el('button', { class: 'btn primary', type: 'button', text: auditResult ? 'Run it again' : 'Run the first audit', onclick: runAudit });
    const a = auditResult;
    const body = [];
    if (a && a.error) body.push(el('div', { class: 'msg err', text: a.error }));
    else if (a) {
      body.push(el('div', { class: 'grid tiles' },
        UI.tile({ name: 'Gaps in the brain', plain: 'still missing after the pull', value: a.gap_total, unit: 'n' }),
        UI.tile({ name: 'Empty fields', plain: 'a room needs these', value: a.gaps.empty || 0, unit: 'n' }),
        UI.tile({ name: 'Weak records', plain: 'low confidence', value: a.gaps.low_confidence || 0, unit: 'n' }),
        UI.tile({ name: 'Expired or in conflict', plain: 'need a fresh look', value: (a.gaps.expired || 0) + (a.gaps.conflict || 0), unit: 'n' })));
      body.push(a.questions.length ? el('div', { class: 'grid' }, a.questions.map(questionCard))
        : UI.emptyState({ title: 'Nothing to ask', text: 'Your sources and answers cover what the rooms need.' }));
      body.push(el('p', { class: 'small muted', text: 'Top 5 by importance: weight times rooms blocked. Questions a connected source can answer are dropped. Brain version ' + a.version + '.' }));
    }
    UI.mount('#step-5', ...head(5, 'Run the first audit', done, 'The keeper checks what is still missing and asks only the 5 questions that matter most. Your answers become founder records in the brain.'),
      el('div', null, btn), ...body);
  }

  load().then(loadOnboard);
})();
