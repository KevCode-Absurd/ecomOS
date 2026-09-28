/* Competitors and market, round 1. Reads /api/03-competitors/plan (ranked actions, findings, rules) and
   overview (the desk). No writes except decisions through the kit's decision row. Competitor facts are
   public signals; brand prices are simulated. Sections follow app/contracts/depth.md section 2. */
(function () {
  'use strict';
  const { el, mount, api, fmt } = UI;
  const BASE = '/api/03-competitors/';
  const SCREEN = '03-competitors';
  const NA = 'unavailable';
  let U = 'unit';   // the price unit from the brain (term.unit), set on load
  const NS = 'http://www.w3.org/2000/svg';
  const pretty = (s) => String(s || '').replace(/_/g, ' ');
  const usd = (v) => v == null ? NA : '$' + Number(v).toFixed(2);

  function svg(tag, attrs, text) {
    const n = document.createElementNS(NS, tag);
    for (const k of Object.keys(attrs || {})) n.setAttribute(k, attrs[k]);
    if (text != null) n.textContent = text;
    return n;
  }

  // ---------- 5f. positioning map ----------
  const MOVE = { hold: ['keep', 'Hold'], claim: ['new', 'Claim'], contest: ['watch', 'Contest'], skip: ['na', 'Skip'] };
  function mapCard(pos) {
    let axis = Object.keys(pos.kit)[0];
    const box = el('div');
    const render = () => {
      const k = pos.kit[axis];
      const chart = Charts.positioningMap({ x: k.x, y: k.y, points: k.points, quadrants: k.quadrants, midX: k.midX, midY: k.midY,
        usLabel: 'us (simulated price)', themLabel: 'tracked brands', sizeUnit: 'n', title: 'Price against ' + pos.axes[axis].label.toLowerCase() + ', sized by active ads',
        note: k.plain + '. Split lines: the tracked median price and the middle of the claim scale.' + (pos.not_placed.length ? ' Not placed, no price band in the brain: ' + pos.not_placed.join(', ') + '.' : '') });
      const moves = el('div', { class: 'grid two moves' }, ...k.moves.map((mv) => el('div', { class: 'card flat move' },
        el('div', { class: 'row' }, UI.verdict(MOVE[mv.kind][0], MOVE[mv.kind][1]), el('b', { text: mv.label })),
        el('div', { class: 'small', text: mv.text }),
        mv.kind === 'claim' || mv.kind === 'contest' ? UI.decisionRow({ capability: 'BRAND-C20', autonomy: 'agent_does', screen: SCREEN, compact: true, finding_id: SCREEN + '.map.' + axis + '.' + mv.label.replace(/[^a-z]+/gi, '_') }) : null)));
      box.replaceChildren(chart, moves);
    };
    const tabs = UI.pills({ items: Object.keys(pos.kit).map((key) => ({ key, label: 'Price vs ' + pos.axes[key].label.toLowerCase() })), current: axis, onChange: (key) => { axis = key; render(); } });
    render();
    return [tabs, box];
  }

  // ---------- 5e. price ladder and pack ladder ----------
  function bandChart(lad) {
    const rows = lad.bands.map((b) => ({ label: b.name, band: b, us: false })).concat(lad.ladders.filter((l) => l.steps.length).map((l) => ({ label: 'Us: ' + l.style, ladder: l, us: true })));
    const W = 720, rowH = 24, pad = { l: 170, r: 24, t: 14, b: 40 };
    const H = pad.t + rows.length * rowH + pad.b;
    const vals = lad.bands.flatMap((b) => [b.low, b.high, b.median].concat((b.seen || []).map((x) => x.per_unit))).concat(lad.ladders.flatMap((l) => l.steps.map((s) => s.per_pair))).filter((v) => v != null);
    const xmax = Math.ceil(Math.max(...vals, 10) * 1.1 / 5) * 5;
    const X = (v) => pad.l + (v / xmax) * (W - pad.l - pad.r);
    const s = svg('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': 'Price per ' + U + ': tracked bands against our pack ladders' });
    const meds = lad.bands.filter((b) => b.frame === 'direct').map((b) => b.median);
    if (meds.length) s.append(svg('rect', { x: X(Math.min(...meds)), y: pad.t, width: X(Math.max(...meds)) - X(Math.min(...meds)), height: rows.length * rowH, class: 'range' }));
    for (let v = 0; v <= xmax; v += 5) {
      s.append(svg('line', { x1: X(v), x2: X(v), y1: pad.t, y2: pad.t + rows.length * rowH, class: 'grid-l' }));
      s.append(svg('text', { x: X(v), y: pad.t + rows.length * rowH + 16, 'text-anchor': 'middle' }, '$' + v));
    }
    if (lad.direct_median != null) s.append(svg('line', { x1: X(lad.direct_median), x2: X(lad.direct_median), y1: pad.t, y2: pad.t + rows.length * rowH, class: 'split' }));
    rows.forEach((r, i) => {
      const y = pad.t + i * rowH + rowH / 2;
      s.append(svg('text', { x: pad.l - 8, y: y + 4, 'text-anchor': 'end', class: r.us ? 'pt us' : 'pt' }, r.label));
      if (r.band) {
        const b = r.band;
        if (b.low != null && b.high != null) s.append(svg('line', { x1: X(b.low), x2: X(b.high), y1: y, y2: y, class: 'band' }));
        else if (b.low != null) s.append(svg('line', { x1: X(b.low), x2: X(xmax), y1: y, y2: y, class: 'band open-end' }));
        const d = svg('circle', { cx: X(b.median), cy: y, r: 5, class: 'dot' + (b.rough ? ' rough' : '') });
        d.append(svg('title', null, b.name + ': ' + b.text));
        s.append(d);
        for (const x of b.seen || []) {   // prices the team logged from their site: squares, red when outside the band
          const q = svg('rect', { x: X(x.per_unit) - 4, y: y - 4, width: 8, height: 8, class: 'seen' + (x.in_band === false ? ' out' : '') });
          q.append(svg('title', null, x.product + ': ' + usd(x.per_unit) + ' a ' + U + ', seen ' + x.date + (x.in_band === false ? ', outside the band' : '')));
          s.append(q);
        }
      } else {
        const st = r.ladder.steps;
        if (st.length > 1) s.append(svg('line', { x1: X(Math.min(...st.map((x) => x.per_pair))), x2: X(Math.max(...st.map((x) => x.per_pair))), y1: y, y2: y, class: 'band brand' }));
        for (const x of st) {
          const d = svg('circle', { cx: X(x.per_pair), cy: y, r: 4 + Math.min(x.pairs, 12) / 3, class: 'dot brand' });
          d.append(svg('title', null, (x.pairs === 1 ? 'single' : x.pairs + '-pack') + ': ' + usd(x.per_pair) + ' a ' + U + ', ' + usd(x.per_pack) + ' a pack (simulated net)'));
          s.append(d);
        }
      }
    });
    s.append(svg('text', { x: pad.l + (W - pad.l - pad.r) / 2, y: H - 6, 'text-anchor': 'middle' }, 'Price per ' + U + ', US dollars. Shaded: range of direct peers\' medians. Dashed: their median.'));
    return el('div', { class: 'map-wrap' }, s);
  }
  function ladderSection(lad) {
    if (!lad.available) { mount('#prices', el('p', { class: 'na', text: 'Our prices are unavailable: ' + (lad.reason || 'no sales table') + '.' })); return; }
    const table = UI.verdictTable({
      columns: [
        { key: 'style', label: 'Style' },
        { key: 'single', label: 'Single, a ' + U, format: (v) => v == null ? 'not sold single' : usd(v) },
        { key: 'biggest', label: 'Biggest pack, a ' + U, format: (v, r) => usd(v) + ' (' + r.biggest_pairs + ' ' + U + 's)' },
        { key: 'saving', label: 'Saving a ' + U, format: (v) => v == null ? NA : Math.round(v * 100) + ' percent' },
        { key: 'proof', label: 'Proof on file', format: (v) => v ? 'yes' : 'none' }],
      rows: lad.ladders,
      verdict: { at: 1, kind: (r) => r.saving == null ? 'na' : r.saving < lad.ladder_min ? 'fix' : 'keep', text: (r) => r.saving == null ? 'No single' : r.saving < lad.ladder_min ? 'Shallow' : 'OK', reason: (r) => r.saving == null ? 'no single ' + U + ' to compare' : Math.round(r.saving * 100) + ' percent saving against a ' + Math.round(lad.ladder_min * 100) + ' percent rule' },
      reason: { key: 'why', label: 'Against direct peers', text: (r) => (r.vs_direct_median || NA) + ' their median of ' + usd(lad.direct_median) },
      sort: false });
    const b = lad.bundle;
    const amz = lad.amazon.length ? el('div', { class: 'small' }, el('b', { text: 'Cross-check, our Amazon listings (public list prices): ' }),
      lad.amazon.length + ' listings state a pack size; ' + usd(lad.amazon[0].per_pair) + ' to ' + usd(lad.amazon[lad.amazon.length - 1].per_pair) + ' a ' + U + ', median ' + usd(lad.amazon[Math.floor(lad.amazon.length / 2)].per_pair) + '. Site prices above are simulated net, so the gap is a check, not a finding.') : null;
    const pm = window.__priceMoves || { moves: [], captures: 0 };
    const moveTxt = (x) => x.source === 'logged'
      ? x.page + ' ' + (x.kind === 'cut' ? 'cut' : 'raised') + ' ' + x.product + ' ' + Math.round(Math.abs(x.change) * 100) + ' percent, ' + usd(x.to) + ' a ' + U + ' against its ' + pm.trail_days + '-day average of ' + usd(x.from) + ' (logged)'
      : x.page + ' ' + (x.kind === 'cut' ? 'cut' : 'raised') + ' ' + Math.round(Math.abs(x.change) * 100) + ' percent, ' + usd(x.from) + ' to ' + usd(x.to) + ' since ' + fmt.date(x.since);
    const moves = el('div', { class: 'small' }, el('b', { text: 'Price moves: ' }), pm.moves.length ? pm.moves.map(moveTxt).join('; ') + '.'
      : (pm.captures < 2 && !(pm.logged && pm.logged.with_baseline) ? 'start with the second dated capture (' + pm.captures + ' on file) or the second logged price for one product; a move of ' + Math.round((pm.threshold || 0.15) * 100) + ' percent or more is flagged.' : 'none of ' + Math.round((pm.threshold || 0.15) * 100) + ' percent or more.'));
    const seen = el('details', { class: 'card flat' }, el('summary', { class: 'small', text: 'Log a price seen on their site (' + ((pm.logged && pm.logged.records) || 0) + ' logged)' }),
      (pm.recent || []).length ? UI.table({ columns: [{ key: 'date', label: 'Date', format: (v) => fmt.date(v) }, { key: 'page', label: 'Page' }, { key: 'product', label: 'Product' },
        { key: 'price', label: 'Price', format: (v) => usd(v) }, { key: 'units', label: 'Units', unit: 'n' }, { key: 'per_unit', label: 'A ' + U, format: (v) => usd(v) }], rows: pm.recent, sort: false }) : null,
      inputForm('price_seen', [{ key: 'page', label: 'Page', options: pm.pages || [] }, { key: 'product', label: 'Product (short label)' },
        { key: 'price', label: 'Price in dollars', type: 'number', step: '0.01' }, { key: 'units', label: 'Units in the pack', type: 'number', value: '1' },
        { key: 'date', label: 'Date seen', type: 'date', value: new Date().toISOString().slice(0, 10) }, { key: 'url', label: 'Source link (https)' }], 'Log the price'),
      (pm.recheck || []).length ? el('p', { class: 'small' }, el('b', { text: 'Due a re-check: ' }), pm.recheck.map((x) => x.page + ' ' + x.product + ' (' + x.age_days + ' days)').join(', ') + '.') : null,
      el('p', { class: 'micro faint', text: 'Log the same product each week. A price ' + Math.round((pm.threshold || 0.15) * 100) + ' percent or more below its own ' + (pm.trail_days || 30) + '-day average goes on the plan. Public prices only.' }));
    mount('#prices', moves, seen, bandChart(lad), el('p', { class: 'micro faint', text: 'Our dots grow with pack size; hover for price per pack. Squares are prices the team logged from their sites; red is outside the band on file. Our prices are simulated net sales per unit for ' + lad.month + '. Hollow dots are rough public reads.' }),
      table, el('p', { class: 'small' }, el('b', { text: 'Pack ladder: ' }), 'our packs save a median ' + (lad.median_saving == null ? NA : Math.round(lad.median_saving * 100) + ' percent') + ' a ' + U + ' against a single' + (b ? '. ' + b.page + ' advertises ' + b.pct + ' percent off bundles.' : '.') + (lad.shallow ? ' The ladder offer is on the plan.' : '')), amz,
      el('ul', { class: 'small muted' }, ...lad.bands.map((x) => el('li', null, x.name + ': ' + x.text + '. ', x.ref ? el('a', { href: x.ref, target: '_blank', rel: 'noopener', text: 'source' }) : null))));
  }

  function auditTable(findings) {
    return UI.table({
      columns: [
        { key: 'severity', label: 'Severity' },
        { key: 'rule_id', label: 'Rule' },
        { key: 'what', label: 'What' },
        { key: 'sentence', label: 'Finding' },
        { key: 'conf', label: 'Confidence', align: 'right' },
        { key: 'cap', label: 'Capability' },
      ],
      rows: findings.map((f) => ({ severity: f.severity + (f.status === 'unavailable' ? ', unavailable' : ''), rule_id: f.rule_id,
        what: pretty(f.entity.label), sentence: f.sentence, conf: f.confidence < 0.3 ? f.confidence + ' (weak evidence)' : String(f.confidence),
        cap: f.capability.id + ', ' + pretty(f.capability.autonomy) })), sort: false, empty: 'No findings on this capture.',
    });
  }

  // ---------- 1. the plan ----------
  function planSection(p) {
    const w = p.window || {};
    mount('#plan', UI.planBoard({
      title: 'The plan: what we make because of them', sub: 'Capture to ' + fmt.date(w.ends_on) + (p.snapshot_age_days == null ? '' : ', ' + p.snapshot_age_days + ' days old') + ', ' + p.actions.length + ' actions from ' + p.rules.length + ' rules',
      orient: p.orient, actions: p.actions, limit: 10, screen: SCREEN,
      tools: [el('button', { class: 'btn sm', type: 'button', text: 'Export CSV', onclick: () => UI.csv(p.actions.map((a, i) => ({ rank: i + 1, title: a.title, owner: a.owner, artefact: a.artefact.kind, severity: a.severity, total: a.rubric.total, why: a.why, check_on: a.check_on })), null, 'competitor-actions.csv') })],
      foot: el('div', { class: 'row' }, UI.rubricLegend(), el('span', { class: 'micro faint', text: 'Ranking: rubric total, then severity. "Not now" snoozes 14 days.' + (p.snoozed ? ' ' + p.snoozed + ' snoozed.' : '') })),
      empty: 'No open action on this capture. Every tracked angle, offer and price sits inside its rule.',
    }));
    const q = p.queue || { items: [], total: 0 };
    mount('#queue', q.items.length ? el('div', { class: 'card flat stack queue' },
      UI.sectionHead({ title: 'Waiting on you: ' + q.total + ' call' + (q.total === 1 ? '' : 's'), sub: 'The top ' + q.items.length + ' by plan rank. Everything else the agent does or a person owns.' }),
      ...q.items.map((x) => el('div', { class: 'queue-item stack' },
        el('div', null, el('span', { class: 'chip' + (x.overdue ? ' warn' : ''), text: x.overdue ? 'overdue' : '#' + x.rank }), ' ', el('b', { text: x.question }), el('span', { class: 'muted', text: ' for "' + x.title + '"' })),
        el('div', { class: 'small' }, el('b', { text: 'Yes means: ' }), x.yes + (x.check_on ? ' Checked on ' + fmt.date(x.check_on) + '.' : '')),
        x.overdue ? null : UI.decisionRow({ capability: x.capability, autonomy: x.autonomy, owner: x.owner, screen: SCREEN, compact: true, finding_id: x.id }))),
      el('p', { class: 'micro faint', text: q.rule })) : el('p', { class: 'small muted', text: 'Nothing waits on you. Every open move is the agent\'s or a named person\'s.' }));
    if ((p.held || []).length) document.getElementById('queue').append(el('div', { class: 'card flat small' }, el('b', { text: 'Held after a lost result: ' }),
      p.held.map((h) => h.title + ' (lost ' + fmt.date(h.lost_on) + (h.reading ? ', ' + h.reading : '') + '; back on ' + fmt.date(h.back_on) + ')').join('; ') + '.',
      el('div', { class: 'micro faint', text: 'A move that lost stays off the plan for ' + p.hold_days + ' days, even while its rule still fires. Remove the outcome in the team log to bring it back sooner.' })));
    const cw = document.getElementById('connect-wrap');
    cw.hidden = !p.connect.length;
    if (p.connect.length) mount('#connect', el('div', { class: 'card flat' }, UI.sectionHead({ title: 'Connect first: ' + p.connect.length + ' rules wait on a source', sub: 'Person tasks in Setup, read-only. They never crowd out work that can start today.' }),
      ...p.connect.map((a) => UI.actionCard(a, { compact: true, screen: SCREEN }))));
  }

  // ---------- 2. what is wrong, ranked ----------
  const SEV = { critical: 0, high: 1, medium: 2, low: 3 };
  function evidenceLine(e) {
    const one = (x) => e.unit === 'usd' ? usd(x) : e.unit === '%' ? fmt.pct(x) : fmt.num(x);
    const v = e.value == null ? NA : one(e.value);
    const base = e.baseline == null ? '' : ' against ' + (Array.isArray(e.baseline) ? e.baseline.join(' to ') : one(e.baseline)) + ' (' + pretty(e.baseline_kind) + ')';
    return el('li', null, el('span', { class: 'mono micro', text: e.metric }), ' ', el('b', { class: 'num', text: v }), base, el('span', { class: 'faint', text: ', ' + e.window + (e.simulated ? ', simulated' : '') }));
  }
  // verdictTable prints actions.label as the column header, so per-row labels ride on row.actions
  function withActs(rows, label, onClick, cls) {
    return rows.map((r) => Object.assign({}, r, { actions: [{ label: label(r), onClick, cls: cls || 'soft' }] }));
  }
  function wrongList(findings, actionsById, p) {
    const open = findings.filter((f) => f.status !== 'resolved').sort((a, b) => (SEV[a.severity] - SEV[b.severity]) || (b.confidence - a.confidence));
    if (!open.length) return [el('p', { class: 'muted', text: 'Nothing open on this capture.' })];
    const card = (f) => {
      const a = actionsById[f.id];
      const go = a ? el('button', { class: 'btn soft xs', type: 'button', text: 'Go to the action', onclick: () => { const n = document.querySelector('#actions [data-id="' + CSS.escape(a.id) + '"]'); if (n) { n.scrollIntoView({ behavior: 'smooth', block: 'center' }); n.classList.add('flash'); setTimeout(() => n.classList.remove('flash'), 1600); } } }) : null;
      return el('article', { class: 'card flat finding' },
        el('div', { class: 'row' }, UI.sevChip(f.severity), el('span', { class: 'chip mono', text: f.rule_id }), el('b', { text: pretty(f.entity.label) }),
          el('span', { class: 'micro faint', text: 'confidence ' + f.confidence + (f.confidence < 0.3 ? ', weak evidence' : '') }), go),
        el('div', { text: f.sentence }),
        f.evidence.length ? el('ul', { class: 'ev small' }, ...f.evidence.map(evidenceLine)) : el('div', { class: 'na small', text: 'Inputs missing: ' + ((f.unavailable || {}).inputs || []).join(', ') }),
        a ? el('div', { class: 'small muted' }, 'Fix: ', el('b', { text: a.title }), ' ', UI.ownerChip(a)) : null);
    };
    return p.groups.map((g) => {
      const fs = open.filter((f) => (p.rule_group[f.rule_id] || 'watch') === g.key);
      if (!fs.length) return null;
      return el('div', { class: 'stack wrong-group' }, el('h4', { text: g.label + ' (' + fs.length + ')' }), ...fs.map(card));
    }).filter(Boolean);
  }

  // ---------- 5a. who are we up against: pills and the side-by-side table ----------
  const pctTxt = (v) => v == null ? NA : Math.round(v * 100) + ' percent';
  function mixText(mix, labels) {
    const top = Object.entries(mix || {}).sort((a, b) => b[1] - a[1]).slice(0, 2);
    return top.length ? top.map(([k, v]) => (labels[k] || k).toLowerCase() + ' ' + Math.round(v * 100) + '%').join(', ') : NA;
  }
  function angleChips(p) {
    return el('div', { class: 'chips' }, ...(p.angles || []).map((a) => el('span', { class: 'chip', title: 'set by "' + a.word + '" in the ' + a.where, text: a.label + (a.n != null ? ' ' + a.n : '') + ': "' + a.word + '"' })));
  }
  function notesBlock(entity) {
    const list = el('div', { class: 'stack small' });
    const input = el('textarea', { class: 'text', rows: 2, placeholder: 'A note for the team on this page', 'aria-label': 'Team note' });
    const status = el('span', { class: 'micro muted' });
    const load = async () => {
      try { const r = await api(BASE + 'notes?entity=' + encodeURIComponent(entity));
        list.replaceChildren(...(r.notes.length ? r.notes.map((n) => el('div', { class: 'card flat' }, el('span', { class: 'micro faint', text: fmt.date(n.time) + ', ' + n.by + ': ' }), n.text)) : [el('span', { class: 'muted', text: 'No notes yet.' })])); }
      catch (e) { list.replaceChildren(el('span', { class: 'na', text: 'Notes unavailable: ' + e.message })); }
    };
    const save = el('button', { class: 'btn sm', type: 'button', text: 'Save note' });
    save.addEventListener('click', async () => {
      if (!input.value.trim()) { status.textContent = 'Type a note first.'; return; }
      try { await api(BASE + 'notes', { method: 'POST', body: { entity, text: input.value } }); input.value = ''; status.textContent = 'Saved.'; load(); }
      catch (e) { status.textContent = 'Could not save: ' + e.message; }
    });
    load();
    return el('div', { class: 'stack' }, el('h4', { text: 'Team notes' }), list, input, el('div', { class: 'row' }, save, status));
  }
  function pagePanel(r, us, data) {
    const L = data.format_labels;
    const cmp = (label, a, b) => el('tr', null, el('th', { text: label }), el('td', { text: a }), el('td', { text: b }));
    const tbl = el('table', { class: 'kit dense vs-table' }, el('thead', null, el('tr', null, el('th'), el('th', { text: r.name }), el('th', { text: us.name }))),
      el('tbody', null,
        cmp('Active ads', r.active_ads == null ? NA : fmt.num(r.active_ads), us.active_ads == null ? NA : fmt.num(us.active_ads)),
        cmp('Format mix', mixText(r.format_mix, L), mixText(us.format_mix, L)),
        cmp('Median days live', r.median_days == null ? NA : String(r.median_days), us.median_days == null ? NA : String(us.median_days)),
        cmp('Ads live 30 days or more', r.long_runners_30d == null ? NA : String(r.long_runners_30d), us.long_runners_30d == null ? NA : String(us.long_runners_30d)),
        cmp('Share pushing an offer', pctTxt(r.offer_share), pctTxt(us.offer_share)),
        cmp('Offers seen', (r.offers_seen || []).join(', ') || 'none seen', (us.offers_seen || []).join(', ') || 'none seen'),
        cmp('Main call to action', r.main_cta || NA, us.main_cta || NA),
        cmp('New in 14 days', r.new_14d == null ? NA : String(r.new_14d), us.new_14d == null ? NA : String(us.new_14d))));
    const body = el('div', { class: 'stack' },
      el('div', { class: 'row' }, UI.verdict(r.verdict.kind, r.verdict.text, r.verdict.reason), el('span', { class: 'small', text: r.verdict.reason })),
      r.positioning ? el('div', { class: 'small', text: r.positioning }) : null,
      tbl,
      el('h4', { text: 'Angles they run, with the word that set each tag' }), r.angles.length ? angleChips(r) : el('div', { class: 'na small', text: 'No angle tagged from ' + (r.quoted_ads || 0) + ' quoted ads and the hook labels.' }),
      el('h4', { text: 'Battlecard draft' }), el('pre', { class: 'card sunken bc', text: r.battlecard }),
      el('div', { class: 'row' }, UI.copyButton({ label: 'Copy battlecard', text: () => r.battlecard }),
        r.ad_library_url ? el('a', { class: 'btn sm', href: r.ad_library_url, target: '_blank', rel: 'noopener', text: 'Open in the Ad Library' }) : null),
      el('div', { class: 'micro faint', text: 'Build the battlecard: the agent keeps it to verified differences and refreshes it each capture.' }),
      UI.decisionRow({ capability: 'BRAND-C57', autonomy: 'agent_does', screen: SCREEN, finding_id: SCREEN + '.page.' + r.key + '.battlecard' }),
      el('div', { class: 'micro faint', text: 'Watch this page weekly: alert only when a new angle, offer or format crosses the rule.' }),
      UI.decisionRow({ capability: 'BRN-C11', autonomy: 'agent_does', screen: SCREEN, finding_id: SCREEN + '.page.' + r.key + '.watch' }),
      notesBlock(r.key),
      el('div', { class: 'micro faint', text: 'Signals only. Run length shows what a page keeps live, not what works. Never copy their text, logos, products or faces.' }));
    UI.panel({ title: r.name + (r.frame === 'direct' ? ', direct competitor' : ', basics and apparel'), body });
  }
  function pagesSection(data) {
    const us = data.rows.find((r) => r.role === 'self');
    const comps = data.rows.filter((r) => r.role !== 'self');
    const L = data.format_labels;
    const cols = [
      { key: 'name', label: 'Page', format: (v, r) => v + (r.role === 'self' ? ' (us)' : r.frame === 'direct' ? '' : ' (basics)') },
      { key: 'active_ads', label: 'Active ads', unit: 'n' },
      { key: 'format_mix', label: 'Format mix', format: (v) => mixText(v, L) },
      { key: 'median_days', label: 'Median days live', unit: 'n' },
      { key: 'offer_share', label: 'Offer share', format: pctTxt },
      { key: 'main_cta', label: 'Main CTA', format: (v) => v || NA },
      { key: 'new_14d', label: 'New, 14 days', format: (v) => v == null ? NA : String(v) },
    ];
    const empty = cols.filter((c) => ['main_cta', 'new_14d'].includes(c.key) && data.rows.every((r) => r[c.key] == null));
    for (const c of empty) cols.splice(cols.indexOf(c), 1);
    const box = el('div');
    const draw = (key) => {
      const rows = comps.filter((r) => key === 'all' || (key === 'threat' ? r.verdict.text === 'Threat' : r.frame === key));
      box.replaceChildren(UI.verdictTable({
        columns: cols, rows: withActs(rows.concat([Object.assign({}, us, { verdict: { kind: 'new', text: 'Us', reason: 'our page, for the side by side' } })]),
          (r) => r.role === 'self' ? 'Ours' : r.verdict.text === 'Threat' ? 'Battlecard' : 'Open', (r) => { if (r.role !== 'self') pagePanel(r, us, data); }),
        verdict: { at: 1, kind: (r) => r.verdict.kind, text: (r) => r.verdict.text, reason: (r) => r.verdict.reason },
        reason: { key: 'why', label: 'Reason in numbers', text: (r) => r.role === 'self' ? 'the line we compare against' : r.verdict.short },
        actions: { label: 'Do', onClick: (r) => { if (r.role !== 'self') pagePanel(r, us, data); } },
        sort: false, onRow: (r) => { if (r.role !== 'self') pagePanel(r, us, data); },
      }));
    };
    const src = data.snapshot ? 'ad-level snapshot of ' + fmt.date(data.snapshot.captured_at) : 'the brain\'s page summaries (no ad-level snapshot yet, so offer share, CTA and new in 14 days read unavailable)';
    mount('#pages', UI.pills({ items: data.pills, current: 'all', onChange: draw }), box,
      el('p', { class: 'micro faint', text: data.rule + ' Source: ' + src + '. Format mix is from up to 150 ads a page.' + (empty.length ? ' Hidden until a snapshot fills them: ' + empty.map((c) => c.label.toLowerCase()).join(', ') + '.' : '') }));
    draw('all');
  }

  // ---------- 5b. the creative coverage matrix ----------
  function briefPanel(cell, row, col) {
    UI.panel({ title: 'Brief: ' + row.label.toLowerCase() + ' as ' + col.label.toLowerCase(), body: el('div', { class: 'stack' },
      el('pre', { class: 'card sunken bc', text: cell.brief }),
      el('div', { class: 'row' }, UI.copyButton({ label: 'Copy brief', text: () => cell.brief })),
      cell.proof ? null : el('div', { class: 'na small', text: 'No proof for this angle in the brain. Add it on the brand brain screen first.' }),
      el('div', { class: 'micro faint', text: 'The agent writes the brief; you approve before anything is made. This logs a creative decision.' }),
      UI.decisionRow({ capability: 'CREA-C06', owner: 'agent_drafts', screen: SCREEN, finding_id: SCREEN + '.' + cell.gap_id }),
      el('div', { class: 'micro faint', text: 'Pages that fill this cell: ' + (cell.pages.join(', ') || 'none') + '. Signals for layout and mood only.' })) });
  }
  function coverageSection(cov) {
    const box = el('div');
    const next = el('p', { class: 'small' });
    const draw = (key) => {
      const c = cov[key];
      box.replaceChildren(UI.coverageMatrix({
        rows: c.rows, cols: c.cols, cells: c.cells, unit: '%', corner: 'Angle, our ads',
        gapRule: (cell) => cell ? cell.kind : '', action: { label: 'Brief it', onClick: briefPanel },
        note: (c.estimated ? 'Estimated from page-level mixes: a page\'s format mix split over the angles it runs; ours from hook counts times our format mix. ' : 'Counted from the ad-level snapshot. ') + 'Them: ' + (c.their_ads == null ? NA : fmt.num(c.their_ads)) + ' ads on ' + c.pages.length + ' pages. Us: ' + (c.our_ads == null ? NA : fmt.num(c.our_ads)) + ' ads.',
      }));
      const g = c.gaps.slice(0, 4);
      next.replaceChildren(el('b', { text: 'Next to try: ' }), g.length ? g.map((x) => x.angle_label.toLowerCase() + ' in ' + x.format + ' (' + Math.round(x.them * 100) + '% of theirs' + (x.proof ? '' : ', proof missing') + ')').join('; ') + '.' : 'no cell passes the gap rule on this capture.');
    };
    const first = cov.all;
    document.getElementById('cov-sub').textContent = 'Cell: our share of ads | their share. A gap is a cell where they put ' + Math.round(first.gap_min * 100) + ' percent or more of their ads and we put none. Amber: we are ' + first.over_x + 'x ahead, check it is not waste.';
    mount('#coverage', UI.pills({ items: [{ key: 'all', label: 'All tracked pages', n: cov.all.pages.length }, { key: 'direct', label: 'Direct only', n: cov.direct.pages.length }], current: 'all', onChange: draw }), box, next);
    draw('all');
  }

  // ---------- 5c. hook and offer mix ----------
  const ANSWER = { copy: 'Copy brief', offer: 'Offer test' };
  function mixSection(mx, actionsById) {
    const rows = mx.rows.map((r) => ({ key: r.name, label: r.name + (r.role === 'self' ? ' (us)' : ''), sub: r.n ? r.n + ' ads read' : 'no ads read' }));
    const cells = {};
    for (const r of mx.rows) { cells[r.name] = {}; for (const k of mx.kinds) cells[r.name][k.key] = r.n ? { us: r.shares[k.key], unit: '%', n: r.n } : null; }
    const kinds = mx.kinds.filter((k) => mx.rows.some((r) => r.shares[k.key]));
    const heat = UI.coverageMatrix({ rows, cols: kinds, cells, unit: '%', single: true, max: 0.3, corner: 'Page', note: 'Share of each page\'s ads that open with each kind of first line. Darker is more.' });
    const offers = UI.table({ columns: [
      { key: 'name', label: 'Page', format: (v, r) => v + (r.role === 'self' ? ' (us)' : '') },
      { key: 'offers', label: 'Offer types seen', format: (v) => (v || []).map((k) => mx.offer_labels[k] || k).join(', ') || 'no offer seen' },
      { key: 'offer_share', label: 'Share of ads with an offer', format: (v) => v == null ? NA : Math.round(v * 100) + ' percent' }], rows: mx.rows, sort: false });
    const held = el('div', { class: 'small muted' }, el('b', { text: 'Held in our brain: ' }), Object.entries(mx.held).map(([k, h]) => (mx.offer_labels[k] || k) + ' (' + h.text + ')').join('; ') + '.');
    const answers = mx.gaps.map((g) => {
      const a = Object.values(actionsById).find((x) => x.entity && (x.entity.id === 'first_line_' + g.key || x.entity.id === 'offer_' + g.key || (g.kind === 'discount' && x.entity.id === 'discount_share')));
      return el('article', { class: 'card flat answer' },
        el('div', { class: 'row' }, el('span', { class: 'chip ' + (g.kind === 'first_line' ? 'accent' : 'warn'), text: ANSWER[g.answer] }), el('b', { text: g.label }), UI.ownerChip(g.owner), el('span', { class: 'micro faint', text: g.pages.length + ' pages: ' + g.pages.join(', ') })),
        el('pre', { class: 'card sunken bc', text: g.draft }),
        el('div', { class: 'row' }, UI.copyButton({ label: 'Copy', text: () => g.draft }),
          UI.decisionRow({ capability: g.capability, owner: g.owner, screen: SCREEN, compact: true, finding_id: a ? a.id : SCREEN + '.mix.' + g.key })));
    });
    mount('#mix', el('h4', { text: 'How their ads open' }), heat, el('h4', { text: 'What they offer' }), offers, held,
      el('h4', { text: 'The answer for each gap' }), ...(answers.length ? answers : [el('p', { class: 'muted', text: 'No gap passes the rules on this capture.' })]),
      el('p', { class: 'micro faint', text: mx.rules + ' Kinds and types only. Never their lines.' }));
  }

  // ---------- 5d. longest running ads as signals ----------
  function refPanel(r) {
    UI.panel({ title: 'Use as reference: ' + r.page, body: el('div', { class: 'stack' },
      el('div', { class: 'row' }, UI.verdict(r.verdict.kind, r.verdict.text), el('span', { class: 'chip', text: 'reference only' }), el('span', { class: 'small', text: 'relevance ' + r.score })),
      el('pre', { class: 'card sunken bc', text: r.brief }),
      el('div', { class: 'row' }, UI.copyButton({ label: 'Copy reference brief', text: () => r.brief }), r.url ? el('a', { class: 'btn sm', href: r.url, target: '_blank', rel: 'noopener', text: 'Open in the Ad Library' }) : null),
      el('div', { class: 'micro faint', text: 'File it in the reference library with its signals and the reason. It never becomes an asset in a brief or a generation call.' }),
      UI.decisionRow({ capability: 'SCT-C04', autonomy: 'agent_does', screen: SCREEN, finding_id: SCREEN + '.reference.' + r.key })) });
  }
  function refsSection(rf) {
    const ours = rf.ours.length ? el('div', { class: 'card flat ours' }, el('b', { text: 'Our longest runners: ' }),
      rf.ours.map((o) => o.days + ' days, ' + o.format + ', ' + o.hook).join('; ') + '. Our median ad lives ' + (rf.our_median == null ? NA : rf.our_median + ' days') + '.',
      el('div', { class: 'row' }, el('span', { class: 'micro faint', text: 'Tag and file our own winners by angle, format and mood so briefs start from them.' }),
        UI.decisionRow({ capability: 'SCT-C02', autonomy: 'agent_does', screen: SCREEN, compact: true, finding_id: SCREEN + '.reference.own_winners' }))) : null;
    const table = UI.verdictTable({
      columns: [
        { key: 'page', label: 'Page', format: (v, r) => v + (r.frame === 'direct' ? '' : ' (basics)') },
        { key: 'days', label: 'Longest, days live', unit: 'n' },
        { key: 'start', label: 'Since', format: (v) => v ? fmt.date(v) : NA },
        { key: 'keep_rate', label: 'Ads live 30 days+', format: (v, r) => v == null ? NA : Math.round(v * 100) + '% (' + r.long_runners + ')' },
        { key: 'score', label: 'Relevance', format: (v) => v == null ? NA : v.toFixed(1) }],
      rows: withActs(rf.refs, (r) => r.suggested ? 'Use as reference' : 'Open', refPanel), verdict: { at: 1, kind: (r) => r.verdict.kind, text: (r) => r.verdict.text, reason: (r) => r.reasons.join('; ') },
      reason: { key: 'why', label: 'Why it matters to us', text: (r) => r.reasons.join('; ') || 'no rule fired' },
      actions: { label: 'Do', onClick: refPanel }, sort: false, onRow: refPanel });
    mount('#refs', ours, table, el('p', { class: 'micro faint', text: rf.rule + ' Run length is a signal, not a result. Versions per ad need an ad-level snapshot.' }));
  }

  // ---------- 5g. launches and changes ----------
  const VKIND = { follow: 'stop', watch: 'watch', ignore: 'keep', ours: 'new' };
  const VTONE = { follow: 'bad', watch: 'warn', ignore: null, ours: 'accent' };
  function changesSection(ch) {
    const items = ch.events.map((e) => ({ when: e.when, who: e.page, title: e.page, text: e.text, tone: VTONE[e.verdict] }));
    const tl = UI.timeline(items);
    Array.from(tl.children).forEach((node, i) => {
      const e = ch.events[i]; if (!e) return;
      const body = node.lastChild;
      body.append(el('div', { class: 'row tl-act' }, UI.verdict(VKIND[e.verdict], e.verdict_text), e.action ? el('span', { class: 'small', text: e.action }) : null,
        e.verdict === 'follow' || e.verdict === 'watch' ? UI.decisionRow({ capability: 'BRN-C11', autonomy: 'agent_does', screen: SCREEN, compact: true, finding_id: SCREEN + '.change.' + e.kind + '.' + String(e.page).replace(/[^a-z0-9]+/gi, '_') }) : null,
        el('span', { class: 'micro faint', text: e.source })));
    });
    const c = ch.counts;
    mount('#changes', UI.orientation([{ label: 'follow', value: c.follow, unit: 'n', tone: c.follow ? 'bad' : null }, { label: 'watch', value: c.watch, unit: 'n' }, { label: 'ignore', value: c.ignore, unit: 'n' }, { label: 'ours', value: c.ours, unit: 'n' }]),
      tl, el('p', { class: 'micro faint', text: ch.rule + ' ' + (ch.captures < 2 ? 'Page-summary diffs start with the second dated capture (' + ch.captures + ' on file). ' : '') + (ch.snapshots < 2 ? 'Ad-level diffs start when a second snapshot lands.' : '') + (ch.older ? ' ' + ch.older + ' older events hidden.' : '') }));
  }

  // ---------- 5h. snapshot freshness and the re-pull ----------
  function freshSection(fr) {
    const table = UI.verdictTable({
      columns: [{ key: 'name', label: 'Page', format: (v, r) => v + (r.role === 'self' ? ' (us)' : '') },
        { key: 'page_id', label: 'Page id', format: (v) => v || 'none, cannot pull' },
        { key: 'captured_at', label: 'Last capture', format: (v) => v ? fmt.date(v) : NA },
        { key: 'age_days', label: 'Age, days', format: (v) => v == null ? NA : String(v) },
        { key: 'source', label: 'From', format: (v) => ({ snapshot: 'ad-level snapshot', brain: 'brain page summary', none: 'nothing captured' })[v] || v }],
      rows: fr.rows, verdict: { at: 1, kind: (r) => r.kind, text: (r) => r.text, reason: (r) => r.age_days == null ? 'no capture' : r.age_days + ' days old' },
      sort: false });
    const p = fr.plan;
    const planBox = el('div', { class: 'card sunken repull', hidden: true });
    if (p.error) planBox.append(el('div', { class: 'na', text: 'Re-pull unavailable: ' + p.error }));
    else planBox.append(
      el('div', null, el('b', { text: 'Re-pull plan: ' }), p.pages.length + ' pages by page id, up to ' + fmt.num(p.max_items) + ' ads (' + p.limit_per_page + ' a page) on ' + p.actor + '.'),
      el('div', null, el('b', { text: 'Estimate: ' }), usd(p.estimate_usd) + '. Caps: ' + usd(p.cap_per_run_usd) + ' a run, ' + usd(p.cap_week_usd) + ' a week, ' + (p.week_spent_usd == null ? 'week spend unavailable' : usd(p.week_spent_usd) + ' spent this week') + '. ' + (p.fits_caps ? 'Fits the caps.' : 'Over a cap: it will be refused.')),
      p.skipped.length ? el('div', { class: 'small' }, 'Skipped: ' + p.skipped.join(', ') + ' (' + p.skipped_reason + ').') : null,
      el('div', { class: 'small' }, p.token ? 'The Apify key is set on the server.' : 'No Apify key on the server: the pull cannot run until one is set in the environment.'),
      el('div', { class: 'row' }, UI.copyButton({ label: 'Copy the run command', text: () => fr.command }), el('span', { class: 'micro faint', text: 'The run logs to the spend ledger. This screen never spends on its own.' })),
      UI.decisionRow({ capability: 'BRN-C11', owner: 'person', screen: SCREEN, compact: true, finding_id: SCREEN + '.repull' }));
    const btn = el('button', { class: 'btn primary sm', type: 'button', text: 'Re-pull: show the estimate first' });
    btn.addEventListener('click', () => { planBox.hidden = !planBox.hidden; btn.textContent = planBox.hidden ? 'Re-pull: show the estimate first' : 'Hide the plan'; });
    const cp = fr.captures || { n: 0 };
    const capStatus = el('span', { class: 'micro muted' });
    const capBtn = el('button', { class: 'btn sm', type: 'button', text: 'Capture today from the brain (free)' });
    capBtn.addEventListener('click', async () => {
      capBtn.disabled = true;
      try { const r = await api(BASE + 'capture', { method: 'POST', body: {} });
        capStatus.textContent = r.already ? 'Already captured today.' : 'Captured ' + r.pages + ' pages; ' + (r.since ? r.changes + ' changes since ' + fmt.date(r.since) + '.' : 'the first capture, diffs start with the next.') + ' Reloading.';
        if (!r.already) setTimeout(() => location.reload(), 600); }
      catch (e) { capStatus.textContent = 'Not captured: ' + e.message; capBtn.disabled = false; }
    });
    const capRow = el('div', { class: 'row wrap' }, capBtn, el('span', { class: 'small muted', text: cp.n + ' dated captures, last ' + (cp.last ? fmt.date(cp.last) : NA) + '. The agent runs it weekly after each brain refresh; it reads only the brain and spends nothing.' }), capStatus);
    mount('#fresh', capRow, el('div', { class: 'row' }, btn, el('span', { class: 'small muted', text: fr.snapshot ? 'Latest ad-level snapshot: ' + fmt.date(fr.snapshot.captured_at) + '.' : 'No ad-level snapshot yet. The screen reads the brain\'s page summaries.' })),
      planBox, table, el('p', { class: 'micro faint', text: fr.rule }));
  }

  // ---------- 5i. who we lose to, by name ----------
  const THEME_KIND = { durability: 'stop', value: 'watch', style: 'watch', fit: 'watch', comfort: 'watch', availability: 'watch', trust: 'watch', unknown: 'na' };
  function lossPanel(r) {
    UI.panel({ title: 'Our answer to ' + r.name, body: el('div', { class: 'stack' },
      el('pre', { class: 'card sunken bc', text: r.answer }),
      el('div', { class: 'row' }, UI.copyButton({ label: 'Copy the answer', text: () => r.answer })),
      UI.decisionRow({ capability: 'BRAND-C57', owner: 'agent_drafts', screen: SCREEN, finding_id: SCREEN + '.COMP-R15.lost_' + r.key }),
      el('div', { class: 'micro faint', text: 'Win-loss interviews tell the real reason. A person books them; the agent writes the guide.' }),
      UI.decisionRow({ capability: 'BRAND-C58', autonomy: 'human_assist', screen: SCREEN, finding_id: SCREEN + '.winloss.' + r.key })) });
  }
  // a small form that logs one first-party record (inputs.py); the page reloads so every rule reads it
  function inputForm(kind, fields, label) {
    const ctl = {};
    const status = el('span', { class: 'micro muted', role: 'status', 'aria-live': 'polite' });
    const row = el('div', { class: 'row wrap input-form', role: 'group', 'aria-label': label });
    for (const f of fields) {
      if (f.hidden) { ctl[f.key] = el('input', { type: 'hidden', value: f.value }); row.append(ctl[f.key]); continue; }
      const c = f.options ? el('select', { class: 'text sm', 'aria-label': f.label }, ...f.options.map((o) => el('option', { value: o, text: o })))
        : el('input', { class: 'text sm', type: f.type || 'text', 'aria-label': f.label, placeholder: f.label, value: f.value || '', step: f.step || null });
      ctl[f.key] = c;
      row.append(el('label', { class: 'micro' }, el('span', { class: 'faint', text: f.label }), c));
    }
    const b = el('button', { class: 'btn sm', type: 'button', text: label });
    for (const c of Object.values(ctl)) if (c.tagName === 'INPUT') c.addEventListener('keydown', (e) => { if (e.key === 'Enter') { e.preventDefault(); b.click(); } });
    b.addEventListener('click', async () => {
      const body = { kind };
      for (const [k, c] of Object.entries(ctl)) body[k] = c.type === 'number' ? (c.value === '' ? null : Number(c.value)) : c.value;
      try { await api(BASE + 'inputs', { method: 'POST', body }); status.textContent = 'Saved. Reloading.'; setTimeout(() => location.reload(), 300); }
      catch (e) { status.textContent = 'Not saved: ' + e.message; const first = Object.values(ctl)[0]; if (first) first.focus(); }
    });
    row.append(b, status);
    return row;
  }
  // the win-loss reason breakdown (room visual): losses to one named brand by coded reason
  function lossReasons(rows, codes) {
    const lost = rows.filter((r) => r.losses);
    if (!lost.length) return null;
    const box = el('div');
    const pick = el('select', { class: 'text sm', 'aria-label': 'Named brand' }, ...lost.map((r) => el('option', { value: r.name, text: r.name })));
    const draw = () => {
      const r = lost.find((x) => x.name === pick.value) || lost[0];
      const used = codes.filter((c) => r.reasons[c]);
      box.replaceChildren(Charts.bar({ labels: used, series: [{ name: 'losses to ' + r.name, values: used.map((c) => r.reasons[c]) }], unit: 'n', height: 200,
        title: 'Losses to ' + r.name + ' by reason', benchmark: 3 }),
        el('p', { class: 'micro faint', text: r.repeat ? r.repeat.n + ' losses for ' + r.repeat.reason + ': on the plan (3 or more is a repeat).' : 'No reason repeats 3 or more times yet.' }));
    };
    pick.addEventListener('change', draw);
    draw();
    return el('div', { class: 'stack' }, el('div', { class: 'row' }, el('span', { class: 'small', text: 'Why we lose to' }), pick), box);
  }
  function winLossBlock(ls) {
    const wl = ls.win_loss || { rows: [], n: 0 };
    const rows = wl.rows.filter((r) => r.n);
    const rate = ls.win_rate == null ? NA + ', ' + ls.win_rate_reason : fmt.pct(ls.win_rate) + ' against ' + ls.win_rate_name;
    return el('div', { class: 'stack card flat' },
      el('h4', { text: 'Win-loss interviews logged: ' + wl.n }),
      el('p', { class: 'small' }, el('b', { text: 'Win rate against a named brand: ' }), rate + '.'),
      rows.length ? UI.table({ columns: [{ key: 'name', label: 'Against' }, { key: 'wins', label: 'Wins', unit: 'n' }, { key: 'losses', label: 'Losses', unit: 'n' },
        { key: 'win_rate', label: 'Win rate', format: (v) => v == null ? NA : fmt.pct(v) }], rows, sort: false }) : null,
      lossReasons(rows, ls.reason_codes || []),
      inputForm('interview', [{ key: 'outcome', label: 'Outcome', options: ['loss', 'win'] }, { key: 'competitor', label: 'Against', options: ls.names || [] },
        { key: 'reason', label: 'Reason code', options: ls.reason_codes || [] }, { key: 'date', label: 'Date', type: 'date', value: new Date().toISOString().slice(0, 10) }], 'Log the interview'),
      el('p', { class: 'micro faint', text: 'Kept in a local file for this brand, never sent anywhere. No names, no quotes: the outcome, the name, one reason and the date.' }));
  }
  function lossSection(ls) {
    const t = UI.verdictTable({
      columns: [{ key: 'name', label: 'Picked instead', format: (v, r) => v + (r.tracked ? '' : ' (not tracked)') },
        { key: 'times', label: 'Times', unit: 'n' }, { key: 'upvotes', label: 'Upvotes', unit: 'n' },
        { key: 'our_one_star', label: 'Our one-stars on it', format: (v) => v == null ? NA : fmt.num(v) }],
      rows: withActs(ls.rows, (r) => r.fires ? 'Answer' : 'Open', lossPanel), verdict: { at: 1, kind: (r) => THEME_KIND[r.theme], text: (r) => 'They ' + r.theme_label, reason: (r) => r.why },
      reason: { key: 'why', label: 'Why the rule says so', text: (r) => r.why + '; ' + (r.where || []).map((x) => 'r/' + x).join(', ') },
      actions: { label: 'Do', onClick: lossPanel }, sort: false, onRow: lossPanel });
    const fr = Object.entries(ls.frames || {}).map(([k, v]) => pretty(k) + ' ' + v).join(', ');
    const kit = el('pre', { class: 'card sunken bc', hidden: true, text: ls.kit });
    const kb = el('button', { class: 'btn sm', type: 'button', text: 'Show the win-loss kit' });
    kb.addEventListener('click', () => { kit.hidden = !kit.hidden; kb.textContent = kit.hidden ? 'Show the win-loss kit' : 'Hide the kit'; });
    mount('#losses', t, winLossBlock(ls),
      el('div', { class: 'row' }, kb, UI.copyButton({ label: 'Copy the kit', text: () => ls.kit }), UI.decisionRow({ capability: 'BRAND-C58', autonomy: 'human_assist', screen: SCREEN, compact: true, finding_id: SCREEN + '.COMP-R29.winloss' })), kit,
      fr ? el('p', { class: 'small muted', text: 'How Reddit frames the category (mentions): ' + fr + '.' }) : null,
      el('p', { class: 'micro faint', text: ls.rule }));
  }

  // ---------- 5j. the category ladder ----------
  function categorySection(c) {
    const box = el('div', { class: 'cat-ladder' });
    for (const r of c.rungs) {
      box.append(el('div', { class: 'rung-row card flat' + (r.ours ? ' ours' : '') },
        el('div', { class: 'row' }, el('b', { text: r.label }), r.ours ? el('span', { class: 'chip accent', text: 'we sit here' }) : null,
          el('span', { class: 'micro faint', text: r.signal_text })),
        el('div', { class: 'small muted', text: r.members.length ? r.members.join(', ') : 'nobody mapped yet' }),
        el('div', { class: 'row' }, el('span', { class: 'small' }, el('b', { text: 'Move: ' }), r.move),
          UI.decisionRow({ capability: r.capability, autonomy: r.autonomy, screen: SCREEN, compact: true, finding_id: SCREEN + '.rung.' + r.key }))));
    }
    mount('#category', box, el('p', { class: 'micro faint', text: c.rule + ' Our price ' + usd(c.our_price) + ' a ' + U + ' (simulated) against a split of ' + usd(c.split) + '. ' + c.coverage + ' of ' + c.rungs.length + ' rungs mapped. Demand trend by rung: unavailable, ' + c.trend_reason + '.' }));
  }

  // ---------- 5k. review themes against their claims ----------
  function reviewSection(rv) {
    const t = UI.verdictTable({
      columns: [{ key: 'label', label: 'Our review theme' }, { key: 'one_star', label: 'One-star', unit: 'n' }, { key: 'five_star', label: 'Five-star', unit: 'n' },
        { key: 'leaders', label: 'Pages leading with it', format: (v) => v.length ? v.length + ': ' + v.slice(0, 3).join(', ') + (v.length > 3 ? ' and more' : '') : 'none' }],
      rows: rv.rows,
      verdict: { at: 1, kind: (r) => rv.attack && r.theme === rv.attack.theme ? 'stop' : r.direct_leaders >= 2 ? 'watch' : 'keep', text: (r) => rv.attack && r.theme === rv.attack.theme ? 'Attacked' : r.direct_leaders >= 2 ? 'Contested' : 'Quiet', reason: (r) => r.direct_leaders + ' direct pages lead with it' },
      reason: { key: 'doubt', label: 'Top doubt', text: (r) => r.top_doubt || NA }, sort: false });
    mount('#reviews', t, el('p', { class: 'small' }, el('b', { text: 'Their review counts: ' }), 'unavailable, ' + rv.their_reviews_reason + '.'),
      el('p', { class: 'micro faint', text: rv.rule + (rv.attack ? ' The answer is on the plan.' : '') }));
  }

  // ---------- 5l. marketplace presence ----------
  function presenceSection(pr) {
    const t = UI.verdictTable({
      columns: [{ key: 'style', label: 'Style' }, { key: 'listings', label: 'Amazon listings', unit: 'n' },
        { key: 'amazon_per_pair', label: 'Amazon, a ' + U, format: (v) => usd(v) }, { key: 'site_per_pair', label: 'Our site, a ' + U, format: (v) => usd(v) },
        { key: 'unknown_sellers', label: 'Seller unknown', unit: 'n' }],
      rows: pr.styles, verdict: { at: 1, kind: (r) => r.undercut ? 'fix' : r.gap == null ? 'na' : 'keep', text: (r) => r.undercut ? 'Undercut' : r.gap == null ? 'No match' : 'In line', reason: (r) => r.gap == null ? 'no site price for the style' : Math.round(r.gap * 100) + ' percent below the site' },
      reason: { key: 'why', label: 'Gap', text: (r) => r.gap == null ? NA : Math.round(r.gap * 100) + ' percent below our site' }, sort: false });
    mount('#presence', UI.orientation([{ label: 'our listings', value: pr.listings, unit: 'n' }, { label: 'priced by ' + U, value: pr.priced, unit: 'n' },
      { label: 'median stars', value: pr.median_stars, unit: 'n' }, { label: 'reviews', value: pr.reviews, unit: 'n' }]), t,
      el('p', { class: 'small' }, el('b', { text: 'Their marketplace listings: ' }), 'unavailable, ' + pr.theirs_reason + '.'),
      el('p', { class: 'micro faint', text: pr.rule + ' Amazon prices are public list prices; ours are simulated net.' }));
  }

  // ---------- 5m. creative velocity and share of voice ----------
  function velocitySection(v) {
    const rows = v.rows.filter((r) => r.rate != null);
    const chart = Charts.bar({ labels: rows.map((r) => r.name + (r.role === 'self' ? ' (us)' : '')), series: [{ name: 'new ads a week, estimate', values: rows.map((r) => r.rate) }],
      benchmark: v.direct_median_rate, benchmark_label: 'direct median', unit: 'n', values: true,
      title: 'New ads a week per page, estimated from ad life', note: 'Active ads / median days live x 7. An estimate on a steady account, not a count. Our counted rate this month: ' + (v.our_counted_rate == null ? NA : v.our_counted_rate + ' a week (' + v.our_counted_note + ')') + '.' });
    const sov = UI.table({ columns: [{ key: 'name', label: 'Page', format: (x, r) => x + (r.role === 'self' ? ' (us)' : '') }, { key: 'active_ads', label: 'Active ads', unit: 'n' },
      { key: 'share', label: 'Share of voice', format: (x) => x == null ? NA : fmt.pct(x) }], rows: v.rows.filter((r) => r.share != null).sort((a, b) => b.share - a.share), sort: false });
    mount('#velocity', chart, el('p', { class: 'small' }, el('b', { text: v.slow ? 'We ship slower: ' : 'Pace: ' }),
      'about ' + v.our_rate + ' new ads a week against a direct median of ' + v.direct_median_rate + '.' + (v.slow ? ' The volume plan (' + v.target + ' a week) is on the plan.' : '')),
      el('h4', { text: 'Share of voice among direct pages, by ads live' }), sov, el('p', { class: 'micro faint', text: v.rule }));
  }

  // ---------- 5n. the weekly brief ----------
  async function digestSection() {
    try {
      const d = await api(BASE + 'digest');
      mount('#digest', el('pre', { class: 'card sunken bc', text: d.text }),
        el('div', { class: 'row' }, UI.copyButton({ label: 'Copy the brief', text: () => d.text }),
          el('span', { class: 'micro faint', text: 'The agent writes this every Monday from the plan and sends it to the team channel once you say so.' })),
        UI.decisionRow({ capability: 'BRN-C11', autonomy: 'agent_does', screen: SCREEN, compact: true, finding_id: SCREEN + '.weekly_brief' }));
    } catch (e) { mount('#digest', el('p', { class: 'na', text: 'Brief unavailable: ' + e.message })); }
  }

  // ---------- 5o. niche sizing against our bar ----------
  function nicheSection(n) {
    const b = n.bar;
    const bar = b ? el('div', { class: 'card flat' }, el('b', { text: 'The bar: ' }), fmt.num(b.buyers) + ' buyers a year to add ' + Math.round(b.share * 100) + ' percent of revenue (' + fmt.money(b.revenue) + '), at ' + usd(b.aov) + ' an order and ' + b.orders_per_buyer + ' orders a buyer. Contribution about ' + (b.contribution == null ? NA : fmt.money(b.contribution)) + '.')
      : el('div', { class: 'na', text: 'The bar is unavailable: the brain lacks AOV, repeat rate or revenue.' });
    const t = UI.table({ columns: [{ key: 'label', label: 'Candidate niche (angle)' }, { key: 'their_share', label: 'Their share of ads', format: (v) => fmt.pct(v) },
      { key: 'our_share', label: 'Ours', format: (v) => fmt.pct(v) }, { key: 'pages', label: 'Pages serving it', format: (v) => v.length + ': ' + v.slice(0, 3).join(', ') + (v.length > 3 ? ' and more' : '') },
      { key: 'demand', label: 'Search demand', format: () => NA }], rows: n.candidates, sort: false, empty: 'No angle passes the candidate rule.' });
    mount('#niche', bar, t, el('p', { class: 'micro faint', text: n.rule + ' Search demand: unavailable, ' + n.demand_reason + '.' + (n.candidates.length ? ' The top candidate has a sizing note on the plan.' : '') }));
  }

  // ---------- 5p. premium signals and discount depth ----------
  function premiumSection(pr) {
    const rows = pr.rows.map((r) => ({ key: r.name, label: r.name + (r.role === 'self' ? ' (us)' : ''), sub: 'score ' + (r.score == null ? NA : Math.round(r.score * 100) + '%') + ', discount ' + (r.depth == null ? NA : r.depth + '%') }));
    const cells = {};
    for (const r of pr.rows) { cells[r.name] = {}; for (const s of pr.signals) cells[r.name][s.key] = r.signals[s.key] == null ? null : { us: r.signals[s.key] ? 1 : 0, unit: 'n' }; }
    const heat = UI.coverageMatrix({ rows, cols: pr.signals, cells, single: true, max: 1, unit: 'n', corner: 'Page', note: '1 = the signal is present, 0 = not seen.' });
    mount('#premium', heat, el('p', { class: 'small' }, el('b', { text: 'Against the direct median: ' }),
      'our score ' + (pr.our_score == null ? NA : Math.round(pr.our_score * 100) + ' percent') + ' against ' + (pr.direct_median_score == null ? NA : Math.round(pr.direct_median_score * 100)) + '; our discount ' + (pr.our_depth == null ? NA : pr.our_depth + ' percent') + ' against ' + (pr.direct_median_depth == null ? NA : pr.direct_median_depth) + '.' + (pr.fires ? ' The code cap policy is on the plan.' : '')),
      el('p', { class: 'micro faint', text: pr.rule }));
  }

  // ---------- 5q. search seeds and overlap ----------
  const SKIND = { contested: ['stop', 'Contested'], gap: ['watch', 'Gap'], shared: ['keep', 'Ours too'] };
  function searchSection(s) {
    const t = UI.verdictTable({ columns: [{ key: 'term', label: 'Search term (seed)' }, { key: 'n', label: 'Pages', unit: 'n' }],
      rows: s.rows, verdict: { at: 1, kind: (r) => SKIND[r.kind][0], text: (r) => SKIND[r.kind][1], reason: (r) => r.pages.join(', ') },
      reason: { key: 'who', label: 'Who uses it', text: (r) => r.pages.join(', ') }, sort: false, maxRows: 20 });
    mount('#search', t, el('p', { class: 'small' }, el('b', { text: 'Only in our lines: ' }), (s.ours_only.join(', ') || 'none') + '.'),
      el('p', { class: 'small' }, el('b', { text: 'Rankings, bids and volume: ' }), 'unavailable, ' + s.overlap_reason + '. The connect step is in the plan\'s connect strip.'),
      el('p', { class: 'micro faint', text: s.rule }));
  }

  // ---------- 5r. landing page tracking for the top threats ----------
  function landingSection(ld) {
    const cards = ld.rows.map((r) => el('article', { class: 'card flat move' },
      el('div', { class: 'row' }, UI.verdict('stop', 'Threat'), el('b', { text: r.name }), el('span', { class: 'micro faint', text: r.reason })),
      el('div', { class: 'small' }, el('b', { text: 'Watch: ' }), r.urls.length ? r.urls.map((u) => /facebook\.com\/ads\/library/.test(u) ? 'Ad Library page' : u.replace(/^https?:\/\//, '')).join(' | ') : 'no url in the brain'),
      r.ad_domains.length ? el('div', { class: 'small' }, el('b', { text: 'Ad landing domains: ' }), r.ad_domains.join(', ')) : null,
      el('div', { class: 'small' }, el('b', { text: 'Last capture: ' }), r.last_capture ? fmt.date(r.last_capture) : 'not tracked yet')));
    mount('#landing', el('div', { class: 'grid three' }, ...cards), el('p', { class: 'small' }, el('b', { text: 'Diff each week: ' }), ld.watch.join(', ') + '.'),
      UI.decisionRow({ capability: 'BRN-C01', autonomy: 'agent_does', screen: SCREEN, compact: true, finding_id: SCREEN + '.COMP-R26.landing_tracking' }),
      el('p', { class: 'micro faint', text: ld.rule }));
  }

  // ---------- 5s. battlecards with freshness ----------
  function cardsSection(bc) {
    const t = UI.verdictTable({ columns: [{ key: 'name', label: 'Against' }, { key: 'verified_on', label: 'Facts checked', format: (v, r) => v ? fmt.date(v) + ', by ' + r.checked_by : NA },
      { key: 'age_days', label: 'Days old', format: (v) => v == null ? NA : String(v) }],
    rows: bc.rows, verdict: { at: 1, kind: (r) => r.stale ? 'fix' : 'keep', text: (r) => r.stale ? 'Stale' : 'Fresh', reason: (r) => (r.age_days == null ? NA : r.age_days) + ' days against ' + bc.stale_days },
    reason: { key: 'claims', label: 'What the card says', text: (r) => r.claims.slice(1, 3).join(' ') },
    actions: { label: 'Copy card', onClick: (r) => UI.copy(r.card) }, sort: false });
    mount('#cards', t, el('div', { class: 'row' }, UI.copyButton({ label: 'Copy all cards for support', text: () => bc.all_text }),
      UI.decisionRow({ capability: 'BRAND-C57', autonomy: 'agent_does', screen: SCREEN, compact: true, finding_id: SCREEN + '.battlecards' })),
      bc.rows.length ? el('details', { class: 'card flat' }, el('summary', { class: 'small', text: 'I checked a card against their site today' }),
        inputForm('card_check', [{ key: 'page', label: 'Card', options: bc.rows.map((r) => r.name) }, { key: 'dropped', label: 'Lines dropped as no longer true', type: 'number', value: '0' },
          { key: 'date', label: 'Date checked', type: 'date', value: new Date().toISOString().slice(0, 10) }], 'Mark checked'),
        el('p', { class: 'micro faint', text: 'Check every line against their site first. The card counts as fresh from this date.' })) : null,
      el('p', { class: 'micro faint', text: bc.rule + ' Verified differences only; never disparage.' }));
  }

  // ---------- 5t. positioning lines against shopper frames ----------
  function framesSection(fr) {
    const t = UI.table({ columns: [{ key: 'label', label: 'Shopper frame (Reddit)' }, { key: 'mentions', label: 'Mentions', unit: 'n' },
      { key: 'brand_named', label: 'We are named', format: (v) => v == null ? NA : String(v) }, { key: 'in_our_frame', label: 'In our line', format: (v) => v ? 'yes' : 'no' }],
    rows: fr.frames, sort: false });
    const lines = el('div', { class: 'stack' }, ...fr.lines.map((x) => el('div', { class: 'card flat' }, el('b', { text: x.key + '. ' }), x.line,
      el('div', { class: 'micro faint', text: 'Answers ' + x.answers + (x.proof ? '. Proof: ' + x.proof : x.key === 'B' ? '. No proof on file.' : '') }))));
    mount('#frames', el('p', { class: 'small' }, el('b', { text: 'Our line now: ' }), fr.our_frame || NA), t, el('h4', { text: 'Lines to test' }), lines,
      el('p', { class: 'small' }, el('b', { text: 'Test score: ' }), fr.score == null ? 'unavailable, no test on file.' : fr.score + ' points for line ' + fr.latest.line + ', ' + fr.latest.verdict + ' (' + fr.latest.why + ').'),
      (fr.tests || []).length ? UI.table({ columns: [{ key: 'date', label: 'Date', format: (v) => fmt.date(v) }, { key: 'line', label: 'Line' }, { key: 'asked', label: 'Asked', unit: 'n' },
        { key: 'prefer_new', label: 'Prefer it', unit: 'n' }, { key: 'prefer_current', label: 'Prefer ours', unit: 'n' }, { key: 'score', label: 'Points' }, { key: 'verdict', label: 'Verdict' }], rows: fr.tests, sort: false }) : null,
      fr.lines.length > 1 ? el('details', { class: 'card flat' }, el('summary', { class: 'small', text: 'Log a poll result' }),
        inputForm('frame_test', [{ key: 'line', label: 'Line tested against ours', options: fr.lines.filter((x) => x.key !== 'A').map((x) => x.key) },
          { key: 'asked', label: 'Shoppers asked', type: 'number' }, { key: 'prefer_new', label: 'Preferred the new line', type: 'number' },
          { key: 'prefer_current', label: 'Preferred ours', type: 'number' }, { key: 'date', label: 'Date', type: 'date', value: new Date().toISOString().slice(0, 10) }], 'Log the result'),
        el('p', { class: 'micro faint', text: 'Win at ' + fr.win_points + ' points or more with ' + fr.min_n + ' or more asked; under ' + fr.lose_points + ' points keeps our line.' })) : null,
      UI.decisionRow({ capability: 'BRAND-C20', autonomy: 'agent_does', owner: 'agent_drafts', screen: SCREEN, compact: true, finding_id: SCREEN + '.COMP-R28.positioning_test' }),
      el('p', { class: 'micro faint', text: fr.rule + ' Reddit is a signal; never quoted.' }));
  }

  // ---------- 5u. placements ----------
  function placementSection(pl) {
    const rows = pl.rows.map((r) => ({ key: r.name, label: r.name + (r.role === 'self' ? ' (us)' : ''), sub: r.platforms.length ? r.platforms.length + ' placements' : 'placements unavailable' }));
    const cells = {};
    for (const r of pl.rows) { cells[r.name] = {}; for (const p of pl.platforms) cells[r.name][p] = r.platforms.length ? { us: r.platforms.includes(p) ? 1 : 0, unit: 'n' } : null; }
    mount('#placements', UI.coverageMatrix({ rows, cols: pl.platforms.map((p) => ({ key: p, label: pretty(p) })), cells, single: true, max: 1, unit: 'n', corner: 'Page', note: '1 = runs ads there. n/a = not in the capture.' }),
      el('p', { class: 'small' }, el('b', { text: 'Gap: ' }), pl.ours_known ? (pl.gaps.length ? pl.gaps.map(pretty).join(', ') + ': most direct pages run there and we do not. Brief a test in the paid social screen.' : 'none; we run where most direct pages run.') : 'our placements are not in the brain yet; the ad-level pull fills them.'),
      el('p', { class: 'micro faint', text: pl.rule + ' A new placement on a rival page shows as a change once two captures exist.' }));
  }

  // ---------- 5v. threat score over time ----------
  function historySection(h) {
    const last = (r) => r.points[r.points.length - 1];
    const rows = h.rows.slice().sort((a, b) => (last(b) == null ? -1 : last(b)) - (last(a) == null ? -1 : last(a))).map((r) => ({ label: r.name, sub: r.active_ads[r.active_ads.length - 1] == null ? 'ads unavailable' : r.active_ads[r.active_ads.length - 1] + ' ads now', values: r.points, unit: 'n', higher_is_better: false,
      delta_label: r.points.length > 1 ? 'since ' + fmt.date(h.dates[0]) : 'one capture' }));
    const rising = h.rows.filter((r) => r.points.length > 1 && r.points[r.points.length - 1] != null && r.points[0] != null && r.points[r.points.length - 1] > r.points[0]).map((r) => r.name);
    mount('#history', Charts.trendStrip({ rows, title: 'Threat points per capture (0 to 6)' }),
      el('p', { class: 'micro faint', text: h.dates.length + ' dated captures (' + (h.dates.length ? h.dates.map(fmt.date).join(', ') : 'none') + '). A trend needs 2 or more; each new brain refresh adds one.' }),
      el('div', { class: 'gap-line row' + (rising.length ? '' : ' held') }, el('b', { text: rising.length ? 'Gap: ' : 'Holding: ' }), el('span', { text: rising.length ? 'Rising threat: ' + rising.join(', ') + '. Refresh their battlecards and read their new ads.' : (h.dates.length > 1 ? 'No page has gained threat points since the first capture.' : 'One capture on file; the trend starts with the next.') })));
  }

  // ---------- 5w. support answers ----------
  function macrosSection(mc) {
    const all = mc.rows.filter((x) => x.answer).map((x) => 'Q: ' + x.question + '\nA: ' + x.answer).join('\n\n');
    mount('#macros', el('div', { class: 'stack' }, ...mc.rows.map((x) => el('div', { class: 'card flat answer' },
      el('div', { class: 'row' }, el('b', { text: x.question }), el('span', { class: 'chip', text: pretty(x.theme) })),
      x.answer ? el('div', { class: 'small', text: x.answer }) : el('div', { class: 'na small', text: 'No answer until the proof is in the brain.' }),
      el('div', { class: 'row' }, x.answer ? UI.copyButton({ label: 'Copy', text: () => x.answer }) : null, el('span', { class: 'micro faint', text: 'Source: ' + x.source }))))),
      el('div', { class: 'row' }, UI.copyButton({ label: 'Copy all ' + mc.ready + ' answers', text: () => all }),
        UI.decisionRow({ capability: 'BRAND-C57', autonomy: 'agent_does', screen: SCREEN, compact: true, finding_id: SCREEN + '.macros' })),
      mc.missing.length ? el('p', { class: 'small' }, el('b', { text: 'Proof to add: ' }), mc.missing.join(', ') + '.') : null,
      el('p', { class: 'micro faint', text: mc.rule }));
  }

  // ---------- 5x. hand-offs to other screens ----------
  async function handoffSection() {
    // hold the node now: the desk tabs detach inactive panels before this fetch returns, so a lookup by id would miss it
    const box = document.getElementById('handoff');
    let snap, exp;
    try { [snap, exp] = await Promise.all([api(BASE + 'competitor_snapshot'), api(BASE + 'experiments')]); }
    catch (e) { mount(box, el('p', { class: 'na', text: 'Hand-offs unavailable: ' + e.message })); return; }
    mount(box, UI.table({ columns: [{ key: 't', label: 'Table' }, { key: 'n', label: 'Rows', unit: 'n' }, { key: 'to', label: 'Read by' }, { key: 'where', label: 'Where' }], sort: false,
      rows: [{ t: 'competitor_snapshot', n: snap.rows.length, to: 'customers and avatars, creative, offers and pricing', where: 'fixtures/competitor_snapshot_' + snap.brand + '.json' },
        { t: 'experiment registry (proposed)', n: exp.rows.length, to: 'experiments', where: 'drafted here; a row is proposed when you approve the test' }] }),
      el('div', { class: 'row' }, el('a', { class: 'btn sm', href: 'fixtures/competitor_snapshot_' + snap.brand + '.json', target: '_blank', rel: 'noopener', text: 'Open the snapshot' }),
        UI.copyButton({ label: 'Copy the proposed tests', text: () => JSON.stringify(exp.rows, null, 1) })),
      el('p', { class: 'micro faint', text: 'Other screens read these tables, never this screen\'s code. ' + exp.note }));
  }

  // ---------- 5y. the holiday season plan ----------
  const OWNER_TXT = { agent: 'Agent does it', agent_drafts: 'Agent drafts, you approve', person: 'A person does it' };
  function seasonSection(sn) {
    mount('#season', UI.orientation([{ label: 'days to Black Friday', value: sn.days_to_black_friday, unit: 'n' }, { label: 'Nov and Dec share of the year', value: sn.season_share_pct == null ? null : sn.season_share_pct / 100, unit: '%' },
      { label: 'our gifting ads', value: sn.our_gifting_ads, unit: 'n', unavailable_label: 'none seen' }]),
      UI.table({ columns: [{ key: 'phase', label: 'Phase' }, { key: 'from', label: 'From', format: (v) => fmt.date(v) }, { key: 'to', label: 'To', format: (v) => fmt.date(v) },
        { key: 'owner', label: 'Who', format: (v) => OWNER_TXT[v] || v }, { key: 'moves', label: 'Moves' }], rows: sn.phases, sort: false }),
      el('p', { class: 'small' }, el('b', { text: 'Dates: ' }), 'Black Friday ' + fmt.date(sn.black_friday) + ', Cyber Monday ' + fmt.date(sn.cyber_monday) + ', last day to order for gifts ' + fmt.date(sn.ship_cutoff) + '. Rivals with a gifting angle: ' + (sn.direct_gifting.join(', ') || 'none') + '.'),
      el('p', { class: 'micro faint', text: sn.rule }));
  }

  // ---------- 5aa. the quarterly positioning review ----------
  function quarterSection(rv) {
    mount('#review', el('pre', { class: 'card sunken bc', text: rv.text }),
      el('div', { class: 'row' }, UI.copyButton({ label: 'Copy the review', text: () => rv.text }),
        UI.decisionRow({ capability: 'BRAND-C19', autonomy: 'agent_does', screen: SCREEN, compact: true, finding_id: SCREEN + '.review.' + rv.quarter.replace(' ', '_') })),
      el('p', { class: 'micro faint', text: 'Built in code from the map, the threats, the shopper frames and the price model. The founder decides; the agent logs each decision to the brain.' }));
  }

  // ---------- 7. exports ----------
  function exportsSection(d) {
    const cov = [];
    for (const r of d.coverage.all.rows) for (const c of d.coverage.all.cols) { const x = d.coverage.all.cells[r.key][c.key]; cov.push({ angle: r.label, format: c.label, ours: x.us, theirs: x.them, pages: x.n, kind: x.kind }); }
    const sets = [
      ['pages', 'competitor-pages.csv', d.pages.rows.map((r) => ({ page: r.name, frame: r.frame, verdict: r.verdict ? r.verdict.text : 'us', points: r.verdict ? r.verdict.points : null, active_ads: r.active_ads, median_days: r.median_days, offers: (r.offers_seen || []).join('; ') }))],
      ['coverage', 'coverage-matrix.csv', cov],
      ['first lines and offers', 'hook-offer-mix.csv', d.mix.rows.map((r) => Object.assign({ page: r.name, ads: r.n, offers: r.offers.join('; ') }, r.shares))],
      ['references', 'references.csv', d.references.refs.map((r) => ({ page: r.page, days: r.days, since: r.start, keep_rate: r.keep_rate, relevance: r.score, url: r.url }))],
      ['pack ladder', 'pack-ladder.csv', d.ladder.ladders.map((r) => ({ style: r.style, single: r.single, biggest: r.biggest, biggest_units: r.biggest_pairs, saving: r.saving }))],
      ['search seeds', 'search-seeds.csv', d.search.rows.map((r) => ({ term: r.term, kind: r.kind, pages: r.pages.join('; ') }))],
      ['room metrics', 'room-metrics.csv', d.room_metrics.map((r) => ({ metric: r.key, value: r.value, formula: r.formula, unavailable: r.unavailable }))],
    ];
    mount('#exports', el('h4', { text: 'Exports' }), el('div', { class: 'row' }, ...sets.map(([label, file, rows]) => el('button', { class: 'btn sm', type: 'button', text: label + ' (' + rows.length + ')', onclick: () => UI.csv(rows, null, file) }))),
      el('p', { class: 'micro faint', text: 'CSV of each desk table as it stands on this capture. Unavailable cells export empty, never 0.' }));
  }

  // ---------- 5z. desk tabs: each job holds its sections ----------
  const DESK = [
    { key: 'rivals', label: 'Rivals', ids: ['pages', 'history', 'cards', 'macros', 'landing', 'losses', 'category', 'reviews'] },
    { key: 'creative', label: 'Ads', ids: ['season', 'coverage', 'velocity', 'mix', 'placements', 'refs', 'changes'] },
    { key: 'price', label: 'Price and position', ids: ['review', 'map', 'frames', 'premium', 'prices', 'presence'] },
    { key: 'market', label: 'Market and data', ids: ['niche', 'search', 'fresh', 'handoff'] },
  ];
  function gapLines(lines) {
    for (const [id, g] of Object.entries(lines || {})) {
      const node = document.getElementById(id);
      const sec = node && node.closest('.section');
      if (!sec || sec.querySelector('.gap-line')) continue;   // a block that writes its own live gap line keeps it
      const go = g.action_id ? el('button', { class: 'btn soft xs', type: 'button', text: g.status === 'unavailable' ? 'Go to the connect step' : 'Go to the action', onclick: () => {
        const n = document.querySelector('#actions [data-id="' + CSS.escape(g.action_id) + '"], #connect [data-id="' + CSS.escape(g.action_id) + '"]');
        if (n) { n.scrollIntoView({ behavior: 'smooth', block: 'center' }); n.classList.add('flash'); setTimeout(() => n.classList.remove('flash'), 1600); } } }) : null;
      sec.append(el('div', { class: 'gap-line row' + (g.action_id ? '' : ' held') }, el('b', { text: g.action_id ? 'Gap: ' : 'Holding: ' }), el('span', { text: g.text }),
        g.action_id ? el('span', { class: 'small muted', text: 'Move: ' + g.title + (g.more ? ' (+' + g.more + ' more)' : '') }) : null, g.owner ? UI.ownerChip(g.owner) : null, go));
    }
  }
  function deskTabs() {
    const src = document.getElementById('desk-src');
    const items = DESK.map((t) => {
      const box = el('div', { class: 'stack desk-panel' });
      for (const id of t.ids) { const n = document.getElementById(id); if (n && n.closest('.section')) box.append(n.closest('.section')); }
      return { key: t.key, label: t.label, n: box.children.length, panel: box };
    });
    mount('#desk', UI.tabs({ items }));
    if (src) src.remove();
  }

  // ---------- 7. the printable weekly report (?view=report): same page, print layout ----------
  const OWNER = { agent: 'Agent does it', agent_drafts: 'Agent drafts, you approve', person: 'A person does it' };
  async function loadReport() {
    let p, d, g;
    try { [p, d, g] = await Promise.all([api(BASE + 'plan'), api(BASE + 'overview'), api(BASE + 'digest')]); }
    catch (e) { mount('#r-badge', 'Could not load: ' + e.message); return; }
    U = (d.term && d.term.unit) || 'unit';
    mount('#r-badge', el('span', null, el('b', { text: 'Simulated data and public signals. ' }), d.simulated_note));
    document.getElementById('r-title').textContent = 'Competitor report, week of ' + fmt.date(g.week_of);
    document.getElementById('r-sub').textContent = p.actions.length + ' open moves from ' + p.rules.length + ' rules. Brain version ' + d.version + '.';
    mount('#r-moves', UI.table({ columns: [{ key: 'n', label: '#', unit: 'n' }, { key: 'title', label: 'Move' }, { key: 'owner', label: 'Who', format: (v) => OWNER[v] || v },
      { key: 'why', label: 'Why' }, { key: 'check_on', label: 'Check on', format: (v) => v ? fmt.date(v) : NA }],
    rows: p.actions.slice(0, 10).map((a, i) => ({ n: i + 1, title: a.title, owner: a.owner, why: a.why, check_on: a.check_on })), sort: false }));
    const q = p.queue || { items: [], total: 0 };
    mount('#r-queue', q.items.length ? el('div', null, el('p', { class: 'small', text: q.total + ' calls wait on you; the top ' + q.items.length + ':' }),
      el('ol', null, ...q.items.map((x) => el('li', null, el('b', { text: x.question }), ' (move #' + x.rank + '). Yes means: ' + x.yes))))
      : el('p', { class: 'muted', text: 'Nothing waits on you.' }));
    const lw = g.logged || { n: 0, lines: [] };
    mount('#r-logged', lw.n ? el('ul', null, ...lw.lines.map((t) => el('li', { text: t }))) : el('p', { class: 'muted', text: 'Nothing logged this week.' }));
    const ev = d.changes.events.filter((e) => e.verdict !== 'ours');
    mount('#r-changed', ev.length ? el('ul', null, ...ev.map((e) => el('li', null, el('b', { text: fmt.date(e.when) + ', ' + e.page + ': ' }), e.text + ' (' + e.verdict_text.toLowerCase() + ')')))
      : el('p', { class: 'muted', text: 'Nothing crossed a rule in the last 28 days.' }));
    mount('#r-threats', UI.table({ columns: [{ key: 'name', label: 'Page' }, { key: 'v', label: 'Verdict' }, { key: 'active_ads', label: 'Active ads', unit: 'n' }, { key: 'r', label: 'Reason' }],
      rows: d.pages.rows.filter((r) => r.role !== 'self').map((r) => ({ name: r.name, v: r.verdict.text, active_ads: r.active_ads, r: r.verdict.short })), sort: false }));
    const v = d.velocity, pr = d.premium;
    mount('#r-numbers', UI.table({ columns: [{ key: 'k', label: 'Number' }, { key: 'v', label: 'Now' }, { key: 'b', label: 'Against' }], sort: false, rows: [
      { k: 'Price index (100 = tracked median)', v: d.price_position_index == null ? NA : String(d.price_position_index), b: '85 to 115' },
      { k: 'New ads a week', v: v.our_counted_rate == null ? NA : v.our_counted_rate + ' (counted)', b: 'direct median ' + v.direct_median_rate + ' (estimate)' },
      { k: 'Discount depth', v: pr.our_depth == null ? NA : pr.our_depth + ' percent', b: 'direct median ' + pr.direct_median_depth + ' percent' },
      { k: 'Pack saving a ' + U, v: d.ladder.median_saving == null ? NA : Math.round(d.ladder.median_saving * 100) + ' percent', b: 'rule ' + Math.round(d.ladder.ladder_min * 100) + ' percent' },
      { k: 'Threat pages', v: String(d.pages.rows.filter((r) => r.verdict && r.verdict.text === 'Threat').length), b: 'of ' + (d.pages.rows.length - 1) + ' tracked' }] }));
    mount('#r-caveats', ...[
      'Competitor facts are public signals from the Ad Library, public product feeds and Reddit. Run length is a signal, not proof.',
      'Our prices and sales are simulated until the store connects.',
      d.coverage.all.estimated ? 'Angle and format shares are estimates from page summaries until an ad-level snapshot lands.' : 'Angle and format shares are counted from an ad-level snapshot.',
      'Never copy their text, logos, products or faces.'].map((t) => el('li', { text: t })));
  }

  // ---------- 3b. the brief pack: every draft, by the team that ships it ----------
  async function briefPack() {
    let b;
    try { b = await api(BASE + 'briefs'); } catch (e) { mount('#briefs', el('p', { class: 'na', text: 'Brief pack unavailable: ' + e.message })); return; }
    mount('#briefs', el('div', { class: 'row' }, el('b', { text: 'Brief pack: ' }), el('span', { class: 'small', text: b.total + ' moves, ' + b.drafted + ' with a draft, for ' + b.teams.length + ' teams.' }),
      ...b.teams.map((t) => UI.copyButton({ label: t.team + ' (' + t.n + ')', text: () => t.text })),
      UI.copyButton({ label: 'Copy as rows (JSON)', text: () => JSON.stringify(b.rows, null, 1) })),
      el('p', { class: 'micro faint', text: 'Copy one team\'s pack and paste it into that team\'s channel. Snoozed moves are left out.' }));
  }

  // ---------- 3. action lanes by owner, with the founder's decisions ----------
  const LANES = [{ key: 'due', label: 'Check due' }, { key: 'all', label: 'All' }, { key: 'agent', label: 'Agent does it' }, { key: 'agent_drafts', label: 'Agent drafts, you approve' }, { key: 'person', label: 'A person does it' }];
  async function actionLanes(p) {
    let dec = {};
    try { const r = await api('/api/decisions?screen=' + SCREEN); for (const x of (r.decisions || [])) if (x.finding_id) dec[x.finding_id] = x; } catch (e) { dec = {}; }
    const hours = (xs) => xs.reduce((t, a) => t + (a.time_to_ship_hours || 0), 0);
    const box = el('div', { class: 'stack' });
    const summary = el('div', { class: 'small muted' });
    const today = new Date().toISOString().slice(0, 10);
    const isDue = (a) => !a.outcome && !!(a.decision || dec[a.id]) && ((a.decision || dec[a.id]).choice !== 'not_now') && a.check_on && a.check_on <= today;
    const outcomeForm = (a) => el('div', { class: 'card flat stack' }, el('b', { class: 'small', text: 'What happened? Log it to close the move.' }),
      inputForm('outcome', [{ key: 'action_id', hidden: true, value: a.id }, { key: 'result', label: 'Result', options: ['won', 'lost', 'flat', 'not shipped'] },
        { key: 'reading', label: 'Reading (optional, short)' }, { key: 'date', label: 'Date read', type: 'date', value: today }], 'Log the outcome'));
    const card = (a, due) => { const c = UI.actionCard(Object.assign({}, a, { decision: a.decision || (dec[a.id] ? { choice: dec[a.id].choice, time: dec[a.id].time } : null) }), { screen: SCREEN });
      return due ? el('div', { class: 'stack' }, c, outcomeForm(a)) : a.outcome ? el('div', { class: 'stack' }, c, el('p', { class: 'small' }, el('b', { text: 'Outcome: ' }), a.outcome.result + (a.outcome.reading ? ', ' + a.outcome.reading : '') + ', read ' + fmt.date(a.outcome.date) + '.')) : c; };
    const draw = (key) => {
      const xs = p.actions.filter((a) => key === 'all' || (key === 'due' ? isDue(a) : a.owner === key));
      const decided = xs.filter((a) => dec[a.id]).length;
      summary.textContent = xs.length + ' actions, about ' + hours(xs) + ' hours of work; ' + decided + ' decided, ' + (xs.length - decided) + ' waiting on you.';
      if (key === 'due' && !xs.length) { box.replaceChildren(el('p', { class: 'muted', text: 'No decided move has reached its check date. Each card shows its date; this lane fills as dates arrive.' })); return; }
      box.replaceChildren(...(xs.length ? xs.map((a) => card(a, key === 'due')) : [el('p', { class: 'muted', text: 'Nothing in this lane.' })]));
    };
    const items = LANES.map((l) => ({ key: l.key, label: l.label, n: l.key === 'all' ? p.actions.length : l.key === 'due' ? p.actions.filter(isDue).length : p.actions.filter((a) => a.owner === l.key).length }));
    mount('#actions', UI.pills({ items, current: 'all', onChange: draw }), summary, box);
    draw('all');
  }

  // ---------- 6. the audit ----------
  function rulesTable(rules) {
    return UI.table({ columns: [{ key: 'rule_id', label: 'Rule' }, { key: 'name', label: 'What it checks' }, { key: 'inputs', label: 'Reads', format: (v) => (v || []).join(', ') }, { key: 'capability', label: 'Capability' }],
      rows: rules, sort: false });
  }

  // everything the team logged on this screen, newest first, with a way to take a mistake back
  const KIND_LABEL = { interview: 'Win-loss interview', price_seen: 'Price seen', card_check: 'Battlecard check', frame_test: 'Positioning poll', threshold: 'Threshold change', outcome: 'Outcome of a move' };
  async function inputsLog() {
    let r;
    try { r = await api(BASE + 'inputs'); } catch (e) { mount('#inputs', el('h4', { text: 'What the team logged' }), el('p', { class: 'na', text: 'Unavailable: ' + e.message })); return; }
    const rows = r.records.map((x) => Object.assign({}, x, { what: KIND_LABEL[x.kind] || pretty(x.kind), row_actions: [{ label: 'Remove', onClick: async () => {
      if (!window.confirm('Remove this record? Every rule reads the file again.')) return;
      try { await api(BASE + 'inputs/remove', { method: 'POST', body: { id: x.id } }); location.reload(); } catch (e) { window.alert('Not removed: ' + e.message); }
    } }] }));
    const tbl = rows.length ? el('table', { class: 'kit dense' }, el('thead', null, el('tr', null, ...['Logged', 'What', 'Record', 'By', ''].map((h) => el('th', { text: h })))),
      el('tbody', null, ...rows.map((x) => el('tr', null, el('td', { text: fmt.date(x.logged_at) }), el('td', { text: x.what }), el('td', { text: x.summary + (x.date ? ', ' + fmt.date(x.date) : '') }),
        el('td', { text: x.by }), el('td', null, el('button', { class: 'btn sm quiet', type: 'button', text: 'Remove', 'aria-label': 'Remove ' + x.what + ': ' + x.summary, onclick: x.row_actions[0].onClick })))))) : null;
    mount('#inputs', el('h4', { text: 'What the team logged (' + rows.length + ')' }), tbl ? el('div', { class: 'table-wrap' }, tbl) : el('p', { class: 'small muted', text: 'Nothing logged yet. Interviews, prices seen, card checks, polls and threshold changes show here.' }),
      el('p', { class: 'micro faint', text: r.note }));
  }

  async function load() {
    let d, p;
    try { [d, p] = await Promise.all([api(BASE + 'overview'), api(BASE + 'plan')]); } catch (e) { mount('#badge', 'Could not load: ' + e.message); return; }
    U = (d.term && d.term.unit) || 'unit';
    mount('#badge', el('span', null, el('b', { text: 'Simulated data and public signals. ' }), d.simulated_note + ' Brain version ' + d.version + '.'));
    planSection(p);
    const byId = {};
    for (const a of p.actions.concat(p.connect)) for (const id of a.finding_ids) byId[id] = a;
    document.getElementById('wrong-sub').textContent = p.findings.length + ' findings on the latest capture, severity first. Each links to the action that closes it.';
    mount('#wrong', ...wrongList(p.findings, byId, p));
    actionLanes(p);
    briefPack();
    document.getElementById('map-sub').textContent = 'Split at the tracked median price (' + usd(d.positioning.split_x) + ') and the middle of the claim scale. Each corner ends in a move: hold, contest, claim or skip.';
    mount('#map', ...mapCard(d.positioning));
    window.__priceMoves = d.price_moves;
    ladderSection(d.ladder);
    pagesSection(d.pages);
    coverageSection(d.coverage);
    mixSection(d.mix, byId);
    refsSection(d.references);
    changesSection(d.changes);
    freshSection(d.freshness);
    lossSection(d.losses);
    categorySection(d.category);
    reviewSection(d.reviews);
    presenceSection(d.presence);
    velocitySection(d.velocity);
    nicheSection(d.niche);
    premiumSection(d.premium);
    searchSection(d.search);
    digestSection();
    landingSection(d.landing);
    cardsSection(d.battlecards);
    framesSection(d.frames);
    placementSection(d.placements);
    historySection(d.history);
    seasonSection(d.season);
    quarterSection(d.review);
    macrosSection(d.macros);
    handoffSection();
    document.getElementById('audit-sub').textContent = p.findings.length + ' findings from ' + p.rules.length + ' rules. Public signals, one capture.';
    mount('#audit', auditTable(p.findings));
    gapLines(d.gap_lines);
    exportsSection(d);
    inputsLog();
    const sb = d.scoreboard || { rows: [] };
    mount('#scoreboard', el('h4', { text: 'What worked against them' }), sb.rows.length ? UI.table({ columns: [{ key: 'label', label: 'Kind of move' }, { key: 'won', label: 'Won', unit: 'n' },
      { key: 'lost', label: 'Lost', unit: 'n' }, { key: 'flat', label: 'Flat', unit: 'n' }, { key: 'not shipped', label: 'Not shipped', unit: 'n' },
      { key: 'win_share', label: 'Win share', format: (v) => v == null ? NA : fmt.pct(v) }], rows: sb.rows, sort: false })
      : el('p', { class: 'small muted', text: 'Unavailable until a move\'s outcome is logged on the check due lane.' }),
      sb.read ? el('p', { class: 'small', text: sb.read + ' moves read, win share ' + fmt.pct(sb.win_share) + (sb.not_shipped ? '; ' + sb.not_shipped + ' not shipped.' : '.') }) : null,
      el('p', { class: 'micro faint', text: sb.rule }));
    deskTabs();
    const fmtM = (r) => r.value == null ? NA : r.unit === '%' ? fmt.pct(r.value) : fmt.num(r.value) + (r.unit === 'days' ? ' days' : r.unit === 'points' ? ' points' : '');
    mount('#metrics', el('h4', { text: 'Room metrics' }), UI.table({ columns: [{ key: 'key', label: 'Metric', format: (v) => pretty(v) }, { key: 'v', label: 'Value' },
      { key: 'formula', label: 'Formula' }, { key: 'unavailable', label: 'Why unavailable', format: (v) => v || '' }], sort: false,
      rows: (d.room_metrics || []).map((r) => Object.assign({}, r, { v: fmtM(r) })) }));
    const th = p.thresholds || { values: {} };
    mount('#rules', el('h4', { text: 'Rules' }), rulesTable(p.rules), el('h4', { text: 'Thresholds in force' }),
      UI.table({ columns: [{ key: 'k', label: 'Threshold' }, { key: 'v', label: 'Value' }, { key: 'd', label: 'Default' }, { key: 's', label: 'From' }], sort: false,
        rows: Object.entries(th.values).map(([k, x]) => ({ k: pretty(k), v: String(x.value), d: String(x.default) + (x.range ? ' (range ' + x.range[0] + ' to ' + x.range[1] + ')' : ''),
          s: x.source === 'screen' ? 'changed here on ' + fmt.date(x.changed_on) : x.source === 'brain' ? 'the brain record' : 'default' })) }),
      el('details', { class: 'card flat' }, el('summary', { class: 'small', text: 'Change a threshold' }),
        inputForm('threshold', [{ key: 'name', label: 'Threshold', options: Object.keys(th.values) }, { key: 'value', label: 'New value', type: 'number', step: 'any' }], 'Save threshold'),
        el('p', { class: 'micro faint', text: 'Every rule reads the new value on the next load. Set it back to the default to undo. Ranges keep an alert from going silent or firing on noise.' })),
      el('p', { class: 'micro faint', text: 'A change made here wins over the brand brain record (plans, field competitor_thresholds' + (th.record ? ', in use: ' + th.record : '') + ').' }));
  }

  if (new URLSearchParams(location.search).get('view') === 'report') {
    document.querySelector('.screen').hidden = true;
    document.getElementById('report').hidden = false;
    document.getElementById('r-print').addEventListener('click', () => window.print());
    loadReport();
  } else load();
})();
