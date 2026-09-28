/* Offers and pricing (round 1). Reads /api/04-offers-pricing/overview and composes kit components in the depth
   order: plan, what is wrong, actions, the desk, the audit. No number is computed here; the server sends every
   value, rule and sentence. No brand fact is written here; everything comes from the brain through the api. */
(function () {
  'use strict';
  const SLUG = '04-offers-pricing';
  const { el, fmt, mount } = UI;
  const brand = new URLSearchParams(location.search).get('brand') || 'bombas';
  const NA = 'unavailable';
  const SOURCE = { site: 'Site', ad_library: 'Meta Ad Library', press: 'Press', review: 'Reviews', interview: 'Interview', founder: 'Founder' };
  const pretty = (s) => String(s || '').replace(/_/g, ' ');
  const pct = (v, d) => v == null ? NA : (v * 100).toFixed(d == null ? 1 : d) + ' percent';
  let ACTIONS = [];

  // ---------- helpers ----------
  function section(id, head, ...body) {
    const node = el('section', { class: 'section', id: id }, UI.sectionHead(head), ...body);
    // depth.md rule 9 and section 2: every desk block ends in a line with the next move, even when it is unavailable
    if (id.indexOf('desk-') === 0 && !node.querySelector('.act-line')) node.append(actionLine('This block waits on the source named above. The connect strip at the top lists it with its steps.', null));
    return node;
  }
  function kv(pairs) {
    return el('dl', { class: 'kv' }, pairs.flatMap(([k, v]) => [el('dt', { text: k }), el('dd', { text: v })]));
  }
  function findAction(fid) { return ACTIONS.find((a) => (a.finding_ids || []).includes(fid) || a.id === fid); }
  function openAction(a) {
    const card = document.querySelector('#actions [data-id="' + CSS.escape(a.id) + '"]');
    if (!card) return;
    card.scrollIntoView({ behavior: 'smooth', block: 'start' });
    card.classList.add('flash');
    setTimeout(() => card.classList.remove('flash'), 1600);
    const btn = Array.from(card.querySelectorAll('button')).find((b) => b.textContent === 'Show steps');
    if (btn) btn.click();
  }
  /** The line every desk block ends in: the gap in words and the action that closes it. */
  function actionLine(text, a) {
    const node = el('div', { class: 'act-line' }, el('span', { class: 'kicker', text: 'Next move' }), el('span', { text: text }));
    if (a) node.append(UI.ownerChip(a), el('button', { class: 'btn soft sm', type: 'button', text: 'Open the action', onclick: () => openAction(a) }));
    return node;
  }

  /** Per-row buttons for a verdict table: the kit reads row.actions; the column header stays a plain word. */
  function withActs(rows, fn) { return rows.map((r) => Object.assign({}, r, { actions: fn(r) })); }

  // ---------- 0. head ----------
  function badge(b) {
    const name = b.name || b.brand || 'This brand';
    mount('#badge', b.simulated
      ? el('span', null, el('b', { text: 'Simulated data. ' }), 'Offers, prices and reviews come from ' + name + ' public pages; every sales number is generated. Nothing here is a ' + name + ' result.')
      : el('span', null, el('b', { text: name }), ' live data. Read-only.'));
  }

  // ---------- 1. the plan ----------
  function plan(d) {
    const open = d.plan.filter((a) => a.status !== 'unavailable');
    const con = d.plan.filter((a) => a.status === 'unavailable');
    const w = d.window;
    mount('#plan', UI.planBoard({
      title: 'The plan: offer and price moves to approve',
      sub: w.days + ' days to ' + fmt.date(w.ends_on) + '. ' + open.length + ' moves, ranked by the rubric.',
      orient: d.orientation, actions: open, limit: 10, screen: SLUG,
      tools: [el('button', { class: 'btn sm', type: 'button', text: 'Export CSV', onclick: () => UI.csv(d.plan.map((a, i) => ({ rank: i + 1, title: a.title, owner: a.owner, severity: a.severity, status: a.status, artefact: a.artefact.kind, total: a.rubric.total, stake_usd: a.money_at_stake && a.money_at_stake.usd, why: a.why })), null, 'offers-plan.csv') })],
      foot: el('div', { class: 'row' }, UI.rubricLegend(), el('span', { class: 'micro faint', text: 'Ranking: critical first by stake, then rubric total, severity, stake. "Not now" snoozes 14 days.' })),
      empty: 'No open offer or price move for this window.',
    }));
    if ((d.planned || []).length) document.getElementById('plan').append(el('div', { class: 'card flat tight planned' }, el('span', { class: 'kicker', text: 'In the brain as plans' }),
      ...d.planned.map((x) => { const st = el('span', { class: 'micro muted' }); return el('div', { class: 'row' }, el('span', { class: 'small', text: x.title + ' (' + x.status + ')' }),
        x.can_launch ? el('button', { class: 'btn xs', type: 'button', text: 'Mark launched', onclick: async () => { try { const r = await UI.api('/api/' + SLUG + '/launched?brand=' + encodeURIComponent(brand), { method: 'POST', body: { id: x.id } }); st.textContent = 'Live from today: ' + r.record; } catch (e) { st.textContent = 'Could not mark: ' + e.message; } } }) : null, st); })));
    if ((d.snoozed || []).length) document.getElementById('plan').append(el('p', { class: 'micro faint', text: 'Not now: ' + d.snoozed.map((x) => x.title + (x.back_on ? ' (back ' + fmt.date(x.back_on) + ')' : '')).join('; ') + '.' }));
    const cw = document.getElementById('connect-wrap');
    cw.hidden = !con.length;
    if (con.length) mount('#connect', el('div', { class: 'card flat connect' },
      el('div', { class: 'sec-head' }, el('h2', { text: 'Connect first: ' + con.length + ' rules wait on a source' }),
        el('span', { class: 'sub', text: 'Each is a person task in Setup, read-only keys only. They never crowd out work that can start today.' })),
      el('div', { class: 'grid' }, con.map((a) => UI.actionCard(a, { compact: true, screen: SLUG })))));
  }

  // ---------- 2. what is wrong, ranked ----------
  function evidenceText(f) {
    return (f.evidence || []).slice(0, 4).map((e) => pretty(e.metric) + ' ' + fmtVal(e.value, e.unit) +
      (e.baseline != null ? ' vs ' + pretty(e.baseline_kind || 'baseline') + ' ' + fmtVal(e.baseline, e.unit) : '') + ' (' + e.window + ')').join('; ');
  }
  function fmtVal(v, unit) {
    if (v == null) return NA;
    if (unit === 'usd' || unit === 'usd_per_order') return fmt.money(v);
    if (unit === 'ratio') return pct(v);
    return fmt.num(v);
  }
  function wrong(d) {
    const fs = d.findings.filter((f) => f.status !== 'resolved');
    const rows = fs.map((f) => ({ f, rule: f.rule_id, what: f.entity.label, sentence: f.sentence, evidence: evidenceText(f) || 'no evidence rows: ' + (f.money_reason || NA), confidence: f.confidence, stake: f.money_at_stake ? f.money_at_stake.usd : null }));
    mount('#wrong', UI.sectionHead({ title: 'What is wrong, ranked', sub: fs.length + ' open findings from ' + d.rules.length + ' rules, severity first. Each links to the action that fixes it.' }),
      UI.verdictTable({
        columns: [{ key: 'what', label: 'Where' }, { key: 'sentence', label: 'Finding' }, { key: 'evidence', label: 'Evidence, window' }, { key: 'stake', label: 'Stake', unit: '$' }, { key: 'confidence', label: 'Conf.', format: (v) => v == null ? NA : v.toFixed(1) }],
        rows, verdict: { at: 0, kind: (r) => r.f.status === 'unavailable' ? 'wait' : r.f.severity === 'critical' || r.f.severity === 'high' ? 'fix' : 'watch', text: (r) => r.f.status === 'unavailable' ? 'Connect' : r.f.severity, reason: (r) => r.f.rule_id },
        actions: { label: 'Open action', onClick: (r) => { const a = findAction(r.f.id); if (a) openAction(a); } },
        sort: false,
      }));
  }

  /** Save a move to the brand brain as a plan record: proposed (review queue) or approved by the founder. */
  function saveRow(a) {
    const status = el('span', { class: 'micro muted' });
    const go = (mode) => async () => {
      status.textContent = 'Saving.';
      try {
        const r = await UI.api('/api/' + SLUG + '/approve?brand=' + encodeURIComponent(brand), { method: 'POST', body: { id: a.id, mode } });
        status.textContent = 'Saved as ' + r.record + ' (' + r.status + ')' + (r.offer ? ', offer ' + r.offer + ' planned' : '') + (r.registry ? ', test proposed as ' + r.registry : '') + '.';
      } catch (e) { status.textContent = 'Could not save: ' + e.message; }
    };
    return el('div', { class: 'row save-row' }, el('span', { class: 'kicker', text: 'Brand brain' }),
      el('button', { class: 'btn sm', type: 'button', text: 'Propose as a plan', onclick: go('proposed') }),
      el('button', { class: 'btn soft sm', type: 'button', text: 'I approve: save as a plan', onclick: go('founder') }), status);
  }

  // ---------- 3 and 4. actions ----------
  function actionsList(d) {
    const open = d.plan.filter((a) => a.status !== 'unavailable');
    mount('#actions', UI.sectionHead({ title: 'Actions: how each move gets done', sub: 'Owner, steps with who does each, the artefact it produces, the win and stop rules, the check date.' }),
      el('div', { class: 'grid' }, open.map((a, i) => UI.actionCard(a, { expanded: i === 0, screen: SLUG, extra: saveRow(a) }))));
  }

  // ---------- 5. the desk ----------
  function stackBlock(rows) {
    return section('desk-stack', { title: 'What does a shopper get from us today?', sub: 'The offer stack from the brand brain, in the order a shopper meets it. Each line keeps its source and the day it was seen.' },
      el('div', { class: 'card tight' }, UI.table({
        columns: [
          { key: 'item', label: 'Offer' },
          { key: 'text', label: 'What it is', format: (v, r) => v || r.unavailable_reason },
          { key: 'source', label: 'Source', format: (v, r) => v ? (SOURCE[v] || v) + (r.ref ? ', ' + r.ref.replace(/^https?:\/\//, '').split('?')[0] : '') : NA },
          { key: 'date', label: 'Seen', format: (v) => v ? fmt.date(v) : NA },
          { key: 'tier', label: 'Tier', format: (v) => pretty(v) || NA },
        ], rows, sort: false })),
      actionLine(rows.filter((r) => !r.id).length ? rows.filter((r) => !r.id).length + ' offer lines are missing from the brain. Add them on the brand brain screen so every rule can read them.'
        : 'Every offer line has a source and a date. Each move above reads from these records.', null));
  }

  function thresholdBlock(th) {
    const a = ACTIONS.find((x) => x.rule_id === 'OFFER-R01');
    const head = { title: 'Does the free shipping line pay for itself?', sub: 'Break-even = AOV + average label / gross margin. A line that works has more orders in the $' + (th.band || 10) + ' just over it than just under it.' };
    if (th.unavailable) return section('desk-threshold', head, UI.emptyState({ screen: SLUG, title: 'Threshold economics unavailable', text: th.reason, missing: [th.fix] }));
    const inp = th.break_even_inputs || {};
    const bins = th.bins || [];
    const i0 = bins.findIndex((g) => g.from === th.shade[0]);
    const dist = Charts.bar({
      labels: bins.map((g) => '$' + g.from), stacked: true, unit: '%', shade: i0 >= 0 ? [i0, i0 + Math.round((th.shade[1] - th.shade[0]) / 5) - 1] : null,
      series: [
        { name: 'Pays shipping', values: bins.map((g) => g.share_paid) },
        { name: 'Ships free', values: bins.map((g) => g.share_free) },
      ],
      maxLabels: 10, title: (th.fixture ? 'Fixture: ' : '') + 'share of orders by order value, $5 bins' + (th.fixture ? ' (shape only, not brand data)' : ', ' + th.window.label),
      note: th.fixture ? 'Order values are ' + NA + ': ' + th.distribution_unavailable + '. A labelled fixture is drawn so the layout can be checked. Shaded: the $' + th.band + ' just under the line.'
        : 'Shaded: the $' + th.band + ' just under the line. Order value is subtotal minus discounts, before tax and shipping. ' + fmt.int(th.orders_sample) + ' order rows.',
    });
    const trend = Charts.step({ labels: th.trend.map((r) => r.month.slice(2)), unit: '$',
      series: [{ name: 'Break-even', values: th.trend.map((r) => r.break_even) }, { name: 'Free shipping line', values: th.trend.map((r) => r.threshold) }],
      title: 'Break-even by month against the line', note: '28-day AOV at each month end, label in force that day, target gross margin. The gap is label money on every order in between.', maxLabels: 6 });
    const facts = [
      ['Line', fmt.money(th.threshold) + ' (' + (SOURCE[(th.threshold_source || {}).type] || 'brain') + ', ' + ((th.threshold_source || {}).captured_at || 'undated') + '), ' + pct(th.above_aov, 0) + ' above AOV'],
      ['Break-even', fmt.money(th.break_even) + ' = AOV ' + fmt.money(inp.aov) + ' + label ' + fmt.money(inp.label) + ' / margin ' + pct(inp.gross_margin, 0)],
      ['Gap', th.gap == null ? NA : fmt.money(th.gap) + (th.gap > 0 ? ' under break-even on every free order in between' : ' over break-even')],
      ['Shipping under the line', th.shipping_listed == null ? NA : fmt.money(th.shipping_listed) + ' listed rate'],
      ['Just under / just over', th.share_just_under == null ? NA + ' until order rows connect' : pct(th.share_just_under) + ' / ' + pct(th.share_just_over)],
    ];
    const scen = UI.verdictTable({
      columns: [
        { key: 'threshold', label: 'Line', format: (v) => fmt.money(v, null, 0) },
        { key: 'be', label: 'Covers break-even', format: (v, r) => r.covers_break_even ? 'yes' : 'no' },
        { key: 'band_orders_28d', label: 'Orders in band, 28 days', format: (v, r) => r.current ? '' : v == null ? NA : fmt.int(v) },
        { key: 'contribution_free', label: 'Contribution, band order', format: (v, r) => r.current ? '' : v == null ? NA : fmt.money(v) },
        { key: 'text', label: 'What must be true' },
      ],
      rows: withActs(th.scenarios.map((r) => Object.assign({ be: '' }, r)), (r) => [r.kind === 'raise' && r.covers_break_even && a
        ? { label: 'Open test brief', onClick: () => openAction(a) } : { label: 'Copy', cls: 'quiet', onClick: () => UI.copy('Free shipping at $' + r.threshold + ': ' + r.text) }]),
      verdict: { at: 1, kind: (r) => r.current ? 'keep' : r.kind === 'raise' && r.covers_break_even ? 'new' : r.kind === 'raise' ? 'watch' : 'wait',
        text: (r) => r.current ? 'Today' : r.kind === 'raise' && r.covers_break_even ? 'Test' : r.kind === 'raise' ? 'Partial' : 'Needs lift', reason: (r) => r.text },
      actions: { label: 'Do' },
      sort: false,
    });
    const line = th.suggested ? 'The line sits ' + fmt.money(th.gap) + ' under break-even. Test $' + th.suggested + ' against ' + fmt.money(th.threshold) + '.' : 'The line sits at or over break-even. Keep it; watch the orders just under it.';
    return section('desk-threshold', head,
      el('div', { class: 'grid two' }, el('div', { class: 'card' }, dist), el('div', { class: 'card' }, trend, kv(facts))),
      el('div', { class: 'card tight' }, el('h4', { text: 'What would a different line need to pay?' }), el('p', { class: 'micro faint', text: th.scenario_rule }), scen),
      actionLine(line, a));
  }

  function cartBlock(cl) {
    const head = { title: 'What does the cart reward past the free shipping line?', sub: 'A second tier one item past the line. The gift pays for itself once a shopper adds its cost over the contribution share, before media.' };
    if (!cl) return section('desk-cart', head, UI.emptyState({ screen: SLUG, title: 'Cart ladder unavailable', text: 'Needs a threshold, a gift item and contribution inputs.' }));
    const a = ACTIONS.find((x) => x.rule_id === 'OFFER-R20');
    const tiers = UI.verdictTable({ columns: [{ key: 'n', label: 'Tier' }, { key: 'at', label: 'Cart value', format: (v) => fmt.money(v, null, 0) }, { key: 'reward', label: 'Reward' }],
      rows: cl.tiers.map((t, i) => Object.assign({ n: String(i + 1), today: !i }, t)), verdict: { at: 1, kind: (r) => r.today ? 'keep' : 'new', text: (r) => r.today ? 'Today' : 'Proposed' }, sort: false });
    const facts = kv([
      ['Climb from tier 1', fmt.money(cl.climb, null, 0)],
      ['Gift cost with pick fee', fmt.money(cl.gift_cost)],
      ['Pays after', fmt.money(cl.pays_after) + ' added, so the climb covers it ' + cl.cover.toFixed(1) + ' times'],
      ['Orders already past tier 2', cl.leak_share == null ? NA + ': ' + cl.leak_reason : pct(cl.leak_share, 0)],
    ]);
    return section('desk-cart', head, el('div', { class: 'grid two' }, el('div', { class: 'card tight' }, tiers), el('div', { class: 'card' }, facts)),
      actionLine(a ? 'The cart has one reward. Add the gift tier at ' + fmt.money(cl.tier2, null, 0) + '.' : 'The cart already runs more than one reward.', a));
  }

  function discountBlock(d) {
    const c = d.chart, dd = d.discipline;
    const head = { title: 'Are we training buyers to wait for a discount?', sub: 'Discount share of gross by day and by month. A promo day runs at ' + (dd ? dd.promo_ratio : 1.5) + ' times the year\'s median share or more; the rest is always-on discounting.' };
    const a = ACTIONS.find((x) => (x.finding_ids || []).some((id) => id.indexOf('OFFER-R19') >= 0 || id.indexOf('OFFER-R18') >= 0));
    const parts = [];
    if (c.unavailable) parts.push(UI.emptyState({ screen: SLUG, title: 'No monthly sales', text: c.reason, missing: [c.fix] }));
    else {
      const note = c.partial.length ? c.partial.join(', ') + ' is a partial month. ' : '';
      parts.push(Charts.line({ labels: c.labels.map((m) => m.slice(2)), series: [{ name: 'Discount share of gross', values: c.discount_share }], unit: '%',
        title: 'Discounts as a share of gross sales, ' + c.window, note: note + 'Discounts over gross sales, all channels.', maxLabels: 8 }));
    }
    const ty = (dd || {}).this_year || {}, ly = (dd || {}).last_year || {};
    const score = UI.table({ columns: [{ key: 'k', label: 'Measure' }, { key: 'now', label: 'Last 365 days' }, { key: 'before', label: 'The 365 before' }], sort: false, rows: [
      { k: 'Median day, discount share', now: pct(ty.median_share), before: pct(ly.median_share) },
      { k: 'Promo days', now: ty.promo_days == null ? NA : String(ty.promo_days), before: ly.promo_days == null ? NA : String(ly.promo_days) },
      { k: 'Net sales on promo days', now: pct(ty.promo_net_share), before: pct(ly.promo_net_share) },
      { k: 'Discount dollars on ordinary days', now: pct(ty.always_on_share, 0), before: pct(ly.always_on_share, 0) },
      { k: 'Blended rate, last 90 days', now: pct(dd && dd.blended_90d), before: pct(dd && dd.blended_90d_last_year) },
    ] });
    const wins = (dd && dd.windows) || [];
    const winTable = wins.length ? UI.verdictTable({ columns: [{ key: 'name', label: 'Window' },
        { key: 'b', label: 'Time before', format: (v, r) => pct(r.before.depth) + ' (' + r.before.start.slice(0, 4) + ')' },
        { key: 'l', label: 'Last time', format: (v, r) => pct(r.last.depth) + ' (' + r.last.start.slice(0, 4) + ')' },
        { key: 'points', label: 'Change, points', format: (v) => (v > 0.05 ? '+' : '') + (Math.abs(v) < 0.05 ? '0.0' : v.toFixed(1)) },
        { key: 'excess_points', label: 'Deeper than the 28 days before, points', format: (v) => Math.abs(v) < 0.05 ? '0.0' : v.toFixed(1) }],
      rows: wins.map((w) => Object.assign({ b: '', l: '' }, w)), verdict: { at: 1, kind: (r) => r.points > dd.window_creep_points ? 'fix' : r.points > 0 ? 'watch' : 'keep', text: (r) => r.points > dd.window_creep_points ? 'Creeping' : r.points > 0 ? 'Deeper' : 'Held or cut' }, sort: false }) : null;
    const policy = dd && dd.policy ? el('div', null, el('h4', { text: 'Discount policy, drafted from the brand\'s history' }), el('pre', { class: 'spec', text: dd.policy }), UI.copyButton({ label: 'Copy policy', text: () => dd.policy })) : null;
    return section('desk-discount', head, el('div', { class: 'grid two' }, el('div', { class: 'card' }, ...parts), el('div', { class: 'card tight' }, score)),
      winTable ? el('div', { class: 'card tight' }, el('h4', { text: 'Is each promo window getting deeper year on year?' }), winTable) : null,
      el('div', { class: 'card' }, el('p', { class: 'small', text: (d.creep || {}).sentence || '' }), policy),
      actionLine(ty.always_on_share != null ? pct(ty.always_on_share, 0) + ' of discount dollars go out on ordinary days. The code is the discount program; test what replaces it.' : 'Discount history unavailable.', a));
  }

  function ladderBlock(l) {
    const head = { title: 'Does every pack size earn its place?', sub: 'Price per item after discounts, 12 full months. Singles over 30 percent of a line, or a pack saving under 10 percent per item, means the ladder is not moving shoppers up.' };
    if (l.unavailable) return section('desk-ladder', head, UI.emptyState({ screen: SLUG, title: 'No product sales', text: l.reason, missing: [l.fix] }));
    const moves = l.moves || [];
    const two = moves.filter((r) => r.single_sku && r.pack_sku);
    const chart = Charts.bar({ labels: two.map((r) => r.line.split('-').slice(-2).join('-')), unit: '$', values: false, width: 1100, height: 200,
      series: [{ name: 'Single, per item', values: two.map((r) => r.single_per_item) }, { name: 'Best-selling pack, per item', values: two.map((r) => r.pack_per_item) }],
      title: 'Price per item: single against the pack', note: 'Net sales over items sold, 12 full months, after discounts. Close bars mean the pack gives little reason to trade up.' });
    const V = { push: ['fix', 'Push'], deepen: ['new', 'Test price'], add: ['new', 'Add pack'], keep: ['keep', 'Keep'] };
    const act = (r) => ACTIONS.find((x) => x.id === SLUG + '.' + (r.verdict === 'add' ? 'OFFER-R09' : 'OFFER-R07') + '.' + r.verdict);
    const table = UI.verdictTable({
      columns: [
        { key: 'line', label: 'Line', format: (v, r) => v + ' (' + r.category + ', ' + (r.rungs || []).join('/') + ')' },
        { key: 'single_share', label: 'Singles', unit: '%' },
        { key: 'saving', label: 'Pack saving', unit: '%' },
        { key: 'gain_per_trade_up', label: 'Margin per trade-up', unit: '$' },
      ],
      rows: withActs(moves.filter((r) => r.verdict !== 'keep'), (r) => act(r) ? [{ label: 'Open action', onClick: () => openAction(act(r)) }] : []), maxRows: 30,
      verdict: { at: 1, kind: (r) => V[r.verdict][0], text: (r) => V[r.verdict][1],
        reason: (r) => r.verdict === 'push' ? 'A 15 percent pack price needs ' + pct(r.trade_up_needed, 0) + ' of single buyers to trade up' : r.verdict === 'deepen' ? 'Pays back at ' + pct(r.trade_up_needed, 0) + ' trade-up' : r.verdict === 'add' ? 'Proposed ' + r.new_pack + '-pack at ' + fmt.money(r.new_price) : 'Ladder works' },
      reason: { key: 'why', label: 'Why', text: (r) => r.verdict === 'push' ? 'Deeper price gives ' + fmt.money(r.give_away_12m) + ' a year to pack buyers; ' + pct(r.trade_up_needed, 0) + ' of singles must trade up.' :
        r.verdict === 'deepen' ? 'Test ' + fmt.money(r.test_price) + '; pays back at ' + pct(r.trade_up_needed, 0) + ' trade-up.' :
        r.verdict === 'add' ? r.new_pack + '-pack at ' + fmt.money(r.new_price) + ', margin ' + fmt.money(r.new_margin) + ' a pack.' : '' },
      actions: { label: 'Do' },
      sort: false,
    });
    const push = moves.filter((r) => r.verdict === 'push').length, add = moves.filter((r) => r.verdict === 'add').length;
    return section('desk-ladder', head,
      el('div', { class: 'card' }, chart), el('div', { class: 'card tight' }, table,
        el('p', { class: 'micro faint', text: moves.filter((r) => r.verdict === 'keep').length + ' more lines keep their ladder: a single pack size, or singles and saving inside the rule. ' + l.margin + '.' })),
      actionLine(push + ' lines need the pack preselected, not a lower price. ' + add + ' basics lines need a pack.', act({ verdict: 'push' }) || act({ verdict: 'add' })));
  }

  function firstOrderBlock(fo) {
    const head = { title: 'What should pay for a first order?', sub: 'Each offer at the average list-price order, 28 days: price paid, what it costs against full price, contribution before media, and payback on paid media per new customer.' };
    if (!fo || fo.unavailable) return section('desk-first', head, UI.emptyState({ screen: SLUG, title: 'First-order economics unavailable', text: (fo || {}).reason }));
    const a = ACTIONS.find((x) => x.rule_id === 'OFFER-R08');
    const best = fo.rows.find((r) => r.key === fo.best_key) || null;
    const isBest = (r) => best && r.key === best.key;
    const table = UI.verdictTable({
      columns: [
        { key: 'name', label: 'Offer' }, { key: 'terms', label: 'Terms', format: (v, r) => r.unavailable ? (v || '') + ' (' + r.reason + ')' : v },
        { key: 'price_paid', label: 'Price paid', unit: '$', format: (v, r) => v == null ? NA : fmt.money(v) + (r.under_line ? ' (under the line)' : '') },
        { key: 'cost', label: 'Cost vs full price', unit: '$' },
        { key: 'contribution', label: 'Contribution', unit: '$' },
        { key: 'payback', label: 'Payback', format: (v) => v == null ? NA : v.toFixed(2) + 'x' },
        { key: 'cvr_limit', label: 'Conversion it can lose', format: (v, r) => r.key === 'code' ? 'baseline' : v == null ? (r.unavailable ? NA : 'none') : pct(v, 0) },
      ],
      rows: withActs(fo.rows, (r) => isBest(r) && a ? [{ label: 'Open test brief', onClick: () => openAction(a) }] : []),
      verdict: { at: 1, kind: (r) => r.key === 'code' ? 'watch' : r.unavailable ? 'na' : isBest(r) ? 'new' : r.cvr_limit ? 'keep' : 'cut',
        text: (r) => r.key === 'code' ? 'Today' : r.unavailable ? 'Unavailable' : isBest(r) ? 'Test' : r.cvr_limit ? 'Option' : 'Worse', reason: (r) => r.answers },
      actions: { label: 'Do' }, sort: false,
    });
    const facts = kv([
      ['Average order', fmt.money(fo.gross_order) + ' at list price, ' + fmt.money(fo.net_order) + ' after discounts'],
      ['Full price keeps', fmt.money(fo.full_price.contribution) + ' before media, ' + fo.full_price.payback.toFixed(2) + 'x payback'],
      ['Paid media per new customer', fmt.money(fo.new_cac) + (fo.target_cac != null ? ' against a ' + fmt.money(fo.target_cac) + ' target' : '')],
      ['Discounts on new orders, 28 days', fmt.money(fo.new_discounts_28d) + ' (all discounts times the ' + pct(fo.new_share, 0) + ' new-customer share; orders do not carry the code yet)'],
    ]);
    const gifts = (fo.gifts || []).slice(0, 6);
    const giftTable = gifts.length ? UI.verdictTable({ columns: [{ key: 'sku', label: 'Single item' }, { key: 'category', label: 'Category' }, { key: 'value', label: 'Paid price', unit: '$' }, { key: 'cost', label: 'Landed cost', unit: '$' }, { key: 'ratio', label: 'Value over cost', format: (v) => v.toFixed(1) + 'x' }],
      rows: gifts, verdict: { at: 1, kind: (r) => r.sku === gifts[0].sku ? 'new' : r.qualifies ? 'keep' : 'watch', text: (r) => r.sku === gifts[0].sku ? 'Give this' : r.qualifies ? 'Also works' : 'Under the bar', reason: (r) => 'value over cost ' + r.ratio + 'x' }, sort: false }) : null;
    return section('desk-first', head, el('div', { class: 'card tight' }, table, el('p', { class: 'micro faint', text: fo.basis + '.' })),
      el('div', { class: 'grid two' }, el('div', { class: 'card' }, facts), giftTable ? el('div', { class: 'card tight' }, el('h4', { text: 'Which item to give?' }), giftTable,
        el('p', { class: 'micro faint', text: 'Ranked by paid price over landed cost. The bar is ' + fo.gift_bar + 'x; ' + (gifts[0].qualifies ? 'the top item clears it.' : 'no item clears it, so the test uses the best one and says so.') })) : null),
      actionLine(best ? 'Test ' + best.name.toLowerCase() + ' against the code. It keeps ' + fmt.money(fo.best_gain) + ' more per first order.' : 'No price-keeping offer beats the code today.', a));
  }

  function waterfallBlock(falls) {
    const head = { title: 'What does each offer keep, from price to contribution?', sub: 'One order per offer, 28 days. Costs from finance inputs, returns at the brain model rates, paid media per order or per new customer. A first order must pay its own media; any other order must keep the target contribution margin.' };
    if (!falls || !falls.length) return section('desk-waterfall', head, UI.emptyState({ screen: SLUG, title: 'Margin waterfall unavailable', text: 'Finance inputs or the daily aggregate are missing.' }));
    const chartBox = el('div', { class: 'card' });
    const draw = (key) => {
      const w = falls.find((x) => x.key === key) || falls[0];
      mount(chartBox, Charts.waterfall({ unit: '$', width: 900, height: 260, title: w.name + (w.status === 'proposed' ? ' (proposed)' : ''),
        steps: w.steps.map((st) => ({ label: st.label, value: st.value, kind: st.kind })),
        note: w.note + (w.missing.length ? ' Unavailable: ' + w.missing.join(', ') + '.' : '') + ' Red line: ' + w.red_line_kind + '.' }));
    };
    const pills = UI.pills({ items: falls.map((w) => ({ key: w.key, label: w.name })), current: falls[0].key, onChange: draw });
    draw(falls[0].key);
    const table = UI.verdictTable({
      columns: [
        { key: 'name', label: 'Offer' }, { key: 'status', label: 'Status' },
        { key: 'price_paid', label: 'Price paid', unit: '$' }, { key: 'before_media', label: 'Before media', unit: '$' },
        { key: 'contribution', label: 'After media', unit: '$' }, { key: 'contribution_share', label: 'Share of price', unit: '%' },
      ],
      rows: falls, verdict: { at: 1, kind: (r) => r.clears == null ? 'na' : r.clears ? 'keep' : 'stop', text: (r) => r.clears == null ? NA : r.clears ? 'Clears' : 'Under the line', reason: (r) => r.red_line_kind },
      reason: { key: 'rl', label: 'Red line', text: (r) => r.red_line == null ? NA : r.red_line_kind === 'target contribution margin' ? pct(r.red_line, 0) + ' of price' : fmt.money(r.red_line) + ' after media' },
      sort: false,
    });
    const under = falls.filter((w) => w.clears === false && w.status === 'live');
    const a = ACTIONS.find((x) => (x.finding_ids || []).some((id) => id.indexOf('OFFER-R10') >= 0));
    return section('desk-waterfall', head, pills, chartBox, el('div', { class: 'card tight' }, table),
      actionLine(under.length ? under.map((w) => w.name).join(', ') + ' is under the red line. A proposed offer under it cannot be approved.' : 'Every live offer clears its red line.', a));
  }

  function registryBlock(reg) {
    const head = { title: 'What is already being tested, and what does it block?', sub: 'The experiment registry, mapped to the surfaces this screen changes. A running test holds its surface until its read point; a finished one can be the proof a doubt needs.' };
    if (!reg || reg.unavailable) return section('desk-registry', head, UI.emptyState({ screen: SLUG, title: 'No experiment registry', text: (reg || {}).reason }));
    const covered = ACTIONS.filter((a) => a.registry && a.registry.relation === 'covered');
    const table = UI.verdictTable({
      columns: [{ key: 'id', label: 'Test' }, { key: 'hypothesis', label: 'Hypothesis' }, { key: 'surface', label: 'Holds', format: (v) => v || 'not an offer surface' },
        { key: 'until', label: 'Until', format: (v) => v ? fmt.date(v) : NA }, { key: 'result', label: 'Result', format: (v) => v && v.lift != null ? v.direction + ' ' + pct(Math.abs(v.lift), 0) + ' (' + fmt.date(v.read_on) + ')' : 'no read yet' }],
      rows: withActs(reg.entries, (e) => { const a = ACTIONS.find((x) => (x.registry && x.registry.id === e.id) || (x.brain_refs || []).indexOf(e.id) >= 0); return a ? [{ label: 'Open action', onClick: () => openAction(a) }] : []; }),
      verdict: { at: 1, kind: (r) => r.status === 'running' ? 'wait' : r.status === 'done' ? 'keep' : 'na', text: (r) => r.status, reason: (r) => r.metric || 'no metric' },
      actions: { label: 'Do' }, sort: false });
    return section('desk-registry', head, el('div', { class: 'card tight' }, table,
      el('p', { class: 'micro faint', text: 'Source: ' + reg.source + '. Price elasticity: ' + (reg.elasticity ? reg.elasticity.reads.map((x) => x.id + ' ' + pct(x.lift, 1)).join(', ') : NA + ', ' + reg.elasticity_reason) + '.' })),
      actionLine(covered.length ? covered.length + ' proposed moves are already running as tests: read them before building anything new. ' + (reg.elasticity ? '' : 'The cost pass-through price test would be the first price read.') : 'No proposed move duplicates a running test.', covered[0] || ACTIONS.find((a) => a.rule_id === 'OFFER-R22')));
  }

  function calendarBlock(cal) {
    const head = { title: 'Which promo windows need an offer, and by when?', sub: 'US retail windows by date rule. Each must be approved a set number of days before it starts. Last year is net sales per day in the window against the 28 days before it.' };
    if (!cal || !cal.length) return section('desk-calendar', head, UI.emptyState({ screen: SLUG, title: 'Calendar unavailable', text: 'No windows for this market.' }));
    const act = (w) => ACTIONS.find((x) => (x.finding_ids || []).some((id) => id.endsWith('.window_' + w.key)));
    const tl = UI.timeline(cal.slice(0, 6).map((w) => ({ when: fmt.date(w.start), who: w.due ? 'approve by ' + fmt.date(w.approve_by) : (w.plan ? 'planned' : 'in ' + w.days_to_start + ' days'),
      title: w.name, text: w.offer, tone: w.due ? 'bad' : w.plan ? 'good' : '' })));
    const table = UI.verdictTable({
      columns: [
        { key: 'name', label: 'Window' }, { key: 'start', label: 'Dates', format: (v, r) => fmt.date(r.start) + ' to ' + fmt.date(r.end) },
        { key: 'approve_by', label: 'Approve by', format: (v, r) => fmt.date(v) + ' (' + (r.days_to_approve >= 0 ? r.days_to_approve + ' days' : 'overdue') + ')' },
        { key: 'lift', label: 'Last year lift', format: (v, r) => r.last_year && r.last_year.lift != null ? pct(r.last_year.lift, 0) : NA },
        { key: 'depth', label: 'Last year depth', format: (v, r) => r.last_year && r.last_year.depth != null ? pct(r.last_year.depth) + ' vs ' + pct(r.last_year.baseline_depth) : NA },
      ],
      rows: withActs(cal.map((w) => Object.assign({ lift: '', depth: '' }, w)), (w) => act(w) ? [{ label: 'Open action', onClick: () => openAction(act(w)) }] : []),
      verdict: { at: 1, kind: (r) => r.plan ? 'keep' : r.due ? 'fix' : 'wait', text: (r) => r.plan ? 'Planned' : r.due ? 'Build now' : 'Later', reason: (r) => r.offer },
      actions: { label: 'Do' }, sort: false,
    });
    const due = cal.filter((w) => w.due);
    return section('desk-calendar', head, el('div', { class: 'grid side' }, el('div', { class: 'card' }, tl), el('div', { class: 'card tight' }, table)),
      actionLine(due.length ? due.length + ' windows need an approved offer in the next 30 days: ' + due.map((w) => w.name + ' by ' + fmt.date(w.approve_by)).join(', ') + '.' : 'No window is due in the next 30 days.', due.length ? act(due[0]) : null));
  }

  function depthBlock(dl) {
    const head = { title: 'How deep can each line go in a promo?', sub: 'The deepest tier each line\'s best-selling pack can take and still keep the target contribution margin after its share of paid media. Lines that clear no tier get a gift instead.' };
    if (!dl || dl.unavailable) return section('desk-depth', head, UI.emptyState({ screen: SLUG, title: 'Depth by line unavailable', text: (dl || {}).reason }));
    const a = ACTIONS.find((x) => x.entity && x.entity.id === 'window_bfcm');
    const table = UI.verdictTable({
      columns: [{ key: 'sku', label: 'Pack' }, { key: 'price', label: 'Paid price', unit: '$' }, { key: 'cogs', label: 'Landed cost', unit: '$' },
        { key: 'contribution_at_depth', label: 'Kept at that depth', format: (v) => v == null ? 'no tier clears' : fmt.money(v) },
        { key: 'share_at_depth', label: 'Share of price', format: (v) => v == null ? 'no tier clears' : pct(v) }],
      rows: dl.rows, maxRows: 30,
      verdict: { at: 1, kind: (r) => r.max_depth == null ? 'watch' : r.max_depth >= 0.2 ? 'scale' : 'keep', text: (r) => r.tier, reason: (r) => 'red line ' + pct(dl.target, 0) },
      sort: false });
    const gifts = dl.rows.filter((r) => r.max_depth == null).length;
    return section('desk-depth', head, el('div', { class: 'card tight' }, table, el('p', { class: 'micro faint', text: dl.basis + '. Paid media is ' + pct(dl.media_share, 0) + ' of net sales over 28 days.' })),
      actionLine('Build the promo as tiers by line, not one sitewide percent. ' + gifts + ' lines get a gift instead of a discount.', a));
  }

  function secondOrderBlock(cc) {
    const head = { title: 'When do first-time buyers stop coming back?', sub: 'Share of each month\'s new customers who order again in months 1 to ' + (cc && cc.curve ? cc.curve.length : 6) + ', weighted by cohort size. The offer goes out before the steepest drop.' };
    if (!cc || cc.unavailable) return section('desk-second', head, UI.emptyState({ screen: SLUG, title: 'Cohorts unavailable', text: (cc || {}).reason }));
    const a = ACTIONS.find((x) => x.rule_id === 'OFFER-R21');
    const chart = Charts.bar({ labels: cc.curve.map((_, i) => 'Month ' + (i + 1)), series: [{ name: 'Active share', values: cc.curve }], unit: '%', values: true, width: 900, height: 200,
      shade: [cc.drop_after_month - 1, cc.drop_after_month - 1], title: 'Share of new customers who order again, by month', note: cc.cohorts + ' cohorts, ' + fmt.int(cc.customers) + ' customers. Shaded: the month before the steepest drop.' });
    return section('desk-second', head, el('div', { class: 'card' }, chart),
      actionLine(a ? 'No offer speaks to the second order. Send first-time buyers the pack upgrade and the gift by day ' + cc.send_by_day + ', no percent off.' : 'A second-order offer is in the brain.', a));
  }

  function costBlock(cm) {
    const head = { title: 'Did prices follow our costs?', sub: 'Landed cost in force today against a year ago, and the paid price per pack over the last 3 full months against the same 3 a year before. The gap is margin that leaks on every pack.' };
    if (!cm || cm.unavailable) return section('desk-cost', head, UI.emptyState({ screen: SLUG, title: 'Cost history unavailable', text: (cm || {}).reason }));
    const a = ACTIONS.find((x) => x.rule_id === 'OFFER-R22');
    const table = UI.verdictTable({
      columns: [{ key: 'sku', label: 'Pack' }, { key: 'cost_move', label: 'Cost move', unit: '%' }, { key: 'price_move', label: 'Price move', unit: '%' },
        { key: 'leak_per_pack', label: 'Leak per pack', unit: '$' }, { key: 'leak_12m', label: 'Leak, 12 months', unit: '$' },
        { key: 'test_price', label: 'Test price', unit: '$' }, { key: 'cvr_limit', label: 'Conversion it can lose', unit: '%' }],
      rows: cm.rows.slice(0, 12), verdict: { at: 1, kind: (r) => r.fires ? 'fix' : 'keep', text: (r) => r.fires ? 'Leaking' : 'Covered', reason: (r) => 'cost ' + pct(r.cost_move, 0) + ', price ' + pct(r.price_move, 1) },
      sort: false });
    const n = cm.rows.filter((r) => r.fires).length;
    return section('desk-cost', head, el('div', { class: 'card tight' }, table, el('p', { class: 'micro faint', text: cm.basis + '. Showing the 12 biggest leaks of ' + cm.rows.length + ' packs.' })),
      actionLine(n ? n + ' packs leak ' + fmt.money(cm.leak_12m) + ' a year. Test passing the cost rise through on the biggest ones.' : 'Prices followed costs.', a));
  }

  function giftingBlock(g) {
    const head = { title: 'Do we sell gifts at the holidays?', sub: 'Holiday index = a line\'s November and December share of its 12 months over the store\'s own share. Gift-led lines sit at or above the bar.' };
    if (!g) return section('desk-gifting', head, UI.emptyState({ screen: SLUG, title: 'Gifting unavailable', text: 'No brand folder.' }));
    const a = ACTIONS.find((x) => x.entity && x.entity.id === 'window_holiday_gifting') || ACTIONS.find((x) => x.rule_id === 'OFFER-R12');
    const top = g.lines.slice(0, 12);
    const chart = Charts.bar({ labels: top.map((r) => r.line.split('-').slice(-2).join('-')), series: [{ name: 'Holiday index', values: top.map((r) => r.index) }],
      benchmark: g.ratio, benchmark_label: 'gift-led bar', unit: 'x', width: 900, height: 200,
      title: 'Holiday index by line, ' + g.months, note: 'Store November and December share: ' + pct(g.store_q4_share) + ' of the 12 months. 1.0x means the line follows the store.' });
    const card = g.gift_card || {};
    const ship = UI.table({ columns: [{ key: 'name', label: 'Shipping' }, { key: 'business_days', label: 'Business days' }, { key: 'order_by', label: 'Order by for ' + fmt.date(g.gift_day), format: (v) => v ? fmt.date(v) : NA }], rows: g.ship_by, sort: false });
    const facts = kv([
      ['Gift card', card.denominations_usd ? (card.name || 'gift card') + ', ' + card.denominations_usd.map((d) => '$' + d).join(', ') : NA],
      ['Gifting program', g.program || NA],
      ['Gift card liability', g.ledger.unavailable ? NA + ': ' + g.ledger.reason : 'see the ledger'],
    ]);
    const led = g.lines.filter((r) => r.gift_led).length;
    return section('desk-gifting', head, el('div', { class: 'card' }, chart),
      el('div', { class: 'grid two' }, el('div', { class: 'card' }, facts), el('div', { class: 'card tight' }, ship)),
      actionLine(led ? led + ' lines sell as gifts. Put them on the holiday page first.' : 'No line sells as a gift yet. Build the holiday page around the big packs, the gift card and the order-by dates.', a));
  }

  function guaranteeBlock(g, returns) {
    const head = { title: 'Is the guarantee working as an offer?', sub: 'The guarantee\'s terms from the brain, the page each term was found on, the doubts it answers, and claims against the brain\'s planned rates.' };
    if (!g || !g.terms.length) return section('desk-guarantee', head, UI.emptyState({ screen: SLUG, title: 'No guarantee in the brain', text: 'Add the guarantee to the brain offers section.' }));
    const a = ACTIONS.find((x) => x.rule_id === 'OFFER-R14');
    const terms = UI.verdictTable({
      columns: [{ key: 'text', label: 'Term' }, { key: 'source', label: 'Found on', format: (v) => v ? v.replace(/^https?:\/\//, '') : NA }],
      rows: g.terms, verdict: { at: 1, kind: (r) => r.selling ? 'keep' : 'fix', text: (r) => r.page_type, reason: (r) => r.id }, sort: false });
    const answers = UI.table({ columns: [{ key: 'theme', label: 'Objection' }, { key: 'doubt', label: 'Doubt it answers' }, { key: 'one_star', label: 'One-star', unit: 'n' }, { key: 'uses', label: 'Needed on', format: (v) => (v || []).map(pretty).join(', ') }], rows: g.answers, sort: false });
    const p = g.planned || {};
    const facts = kv([
      ['Planned refunds or replacements', p.refund_or_replace == null ? NA : pct(p.refund_or_replace) + ' of orders (' + p.source + ')'],
      ['Planned replacements', p.replacement == null ? NA : pct(p.replacement) + ' of orders'],
      ['Actual', returns && !returns.fixture ? 'see returns by reason above' : NA + ': ' + ((returns || {}).reason || 'returns are not connected')],
    ]);
    return section('desk-guarantee', head, el('div', { class: 'grid two' }, el('div', { class: 'card tight' }, terms), el('div', { class: 'card' }, facts)),
      el('div', { class: 'card tight' }, answers),
      actionLine(g.on_selling_page ? 'The guarantee is on a selling page. Keep it next to the price.' : 'The guarantee answers ' + g.one_star_answered + ' one-star doubts but lives on the ' + g.stated_on.join(', ') + '. Put it next to the price and in the cart.', a));
  }

  function positionBlock(cp, b) {
    const head = { title: 'Where do we sit on price and offer against the set?', sub: 'Median price per item from each competitor\'s price band in the brain, the discount their ads show in the Ad Library, and the proof their ads sell. Signals only; nothing is copied.' };
    if (!cp || !cp.us) return section('desk-position', head, UI.emptyState({ screen: SLUG, title: 'Position unavailable', text: 'No competitor price bands in the brain.' }));
    const a = ACTIONS.find((x) => x.rule_id === 'OFFER-R16');
    const byXY = {};
    for (const c of cp.competitors.filter((c) => c.price != null && c.discount_in_ads != null)) {
      const k = c.price + '|' + c.discount_in_ads;
      const short = c.name.split(' ')[0];
      if (byXY[k]) { byXY[k].label += ', ' + short; byXY[k].size = Math.max(byXY[k].size, c.proof_hooks.length ? 9 : 6); }
      else byXY[k] = { label: short, x: c.price, y: c.discount_in_ads, size: c.proof_hooks.length ? 9 : 6, note: c.proof_hooks.join(', ') || 'no proof hook' };
    }
    const pts = Object.values(byXY);
    pts.push({ label: b.name || cp.us.name, x: cp.us.price, y: cp.us.discount_in_ads || 0, us: true, size: 10 });
    const map = Charts.positioningMap({ x: { label: 'Price per item, $', min: 0, max: Math.max(...pts.map((p) => p.x)) + 5, lo: 'cheaper', hi: 'dearer' },
      y: { label: 'Discount in ads, percent', min: 0, max: 25 },
      points: pts, midX: cp.set_median_price, midY: 10, quadrants: ['cheap and discount-led', 'premium with a discount', 'cheap, no discount', 'premium, proof-led'],
      title: 'Price per item against discount in ads', note: cp.basis + '. Bigger dots sell proof in their ads.' });
    const table = UI.table({ columns: [
      { key: 'name', label: 'Competitor' }, { key: 'price', label: 'Median per item', unit: '$' },
      { key: 'discount_in_ads', label: 'Discount in ads', format: (v) => v == null ? NA : v ? v + ' percent' : 'none' },
      { key: 'proof_hooks', label: 'Proof they sell', format: (v) => (v || []).join(', ') || 'none' }], rows: cp.competitors, sort: false });
    return section('desk-position', head, el('div', { class: 'grid two' }, el('div', { class: 'card' }, map), el('div', { class: 'card tight' }, table)),
      actionLine(a ? 'We are the cheap, discount-led dot in a proof-led set. Lead 3 ads with proof instead of the code.' : 'Our price and offer position matches the set.', a));
  }

  function parityBlock(mp) {
    const head = { title: 'Is anyone selling us cheaper than our own site?', sub: 'Marketplace listings in the brain: price over the pack count in the title, against the site\'s paid price per item at the same pack size. More than ' + (mp ? pct(mp.gap, 0) : '10 percent') + ' under is an undercut.' };
    if (!mp || !mp.rows.length) return section('desk-parity', head, UI.emptyState({ screen: SLUG, title: 'No marketplace listings', text: 'Add marketplace listings to the brain.' }));
    const a = ACTIONS.find((x) => x.rule_id === 'OFFER-R17');
    const table = UI.verdictTable({
      columns: [
        { key: 'asin', label: 'Listing', format: (v, r) => r.channel + ' ' + v }, { key: 'title', label: 'Title' },
        { key: 'pack', label: 'Pack', format: (v) => v == null ? NA : String(v) }, { key: 'price', label: 'Price', unit: '$' },
        { key: 'per_item', label: 'Per item', unit: '$' }, { key: 'site_per_item', label: 'Site per item', unit: '$' },
        { key: 'gap', label: 'Gap', format: (v, r) => v == null ? r.reason : pct(v, 0) },
      ],
      rows: mp.rows.filter((r) => r.gap != null), maxRows: 40,
      verdict: { at: 1, kind: (r) => r.gap == null ? 'na' : r.undercut ? 'fix' : 'keep', text: (r) => r.gap == null ? 'Unmatched' : r.undercut ? 'Undercut' : 'In line', reason: (r) => 'seller ' + (r.seller || 'unknown') },
      sort: false,
    });
    const n = mp.rows.filter((r) => r.undercut).length;
    const scale = Object.entries(mp.channel_sales || {}).map(([k, v]) => k + ' ' + fmt.money(v)).join(', ');
    return section('desk-parity', head, el('div', { class: 'card tight' }, table,
      el('p', { class: 'micro faint', text: mp.basis + '. ' + (scale ? 'Channel sales in ' + mp.channel_month + ': ' + scale + '.' : '') + ' Site pack sizes compared: ' + Object.keys(mp.site_per_item_by_pack).join(', ') + '. ' + mp.rows.filter((r) => r.gap == null).length + ' more listings could not be matched: no price, no pack count in the title, or no site pack of that size.' })),
      actionLine(n ? n + ' listings undercut the site. Check each seller, then price or report.' : 'No listing undercuts the site.', a));
  }

  function testsBlock(tests) {
    const head = { title: 'Which moves can run together, and which must wait?', sub: 'Each move changes a surface for a set number of days. Two moves on one surface cannot run at once, and nothing runs inside a promo window. Earliest start is 7 days after today for approval.' };
    if (!tests || !tests.length) return section('desk-tests', head, UI.emptyState({ screen: SLUG, title: 'No moves to schedule', text: 'The plan has no open moves.' }));
    const short = (iso) => { const d = new Date(iso + 'T00:00:00'); return isNaN(d) ? NA : d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }); };
    const V = { ready: ['new', 'Starts first'], waits: ['wait', 'Waits'], after_freeze: ['watch', 'After the peak'] };
    const table = UI.verdictTable({
      columns: [{ key: 'title', label: 'Move' }, { key: 'start', label: 'Runs', format: (v, r) => short(r.start) + ' to ' + short(r.end) + ', ' + r.days + ' days' },
        { key: 'surfaces', label: 'Changes', format: (v) => v.join(', ') }, { key: 'waits_for', label: 'Waits for', format: (v) => v.length ? v.join('; ') : 'nothing' }],
      rows: withActs(tests, (r) => { const a = ACTIONS.find((x) => x.id === r.id); return a ? [{ label: 'Open action', onClick: () => openAction(a) }] : []; }),
      verdict: { at: 1, kind: (r) => V[r.status][0], text: (r) => V[r.status][1], reason: (r) => r.surfaces.join(', ') },
      actions: { label: 'Do' }, sort: false,
    });
    const ready = tests.filter((t) => t.status === 'ready');
    return section('desk-tests', head, el('div', { class: 'card tight' }, table,
      el('div', { class: 'row' }, el('button', { class: 'btn sm', type: 'button', text: 'Export calendar CSV', onclick: () => UI.csv(tests.map((t) => ({ move: t.title, start: t.start, end: t.end, days: t.days, changes: t.surfaces.join('; '), waits_for: t.waits_for.join('; ') })), null, 'offer-test-calendar.csv') }))),
      actionLine(ready.length + ' moves can start on ' + fmt.date(ready.length ? ready[0].start : null) + ' side by side. ' + (tests.length - ready.length) + ' wait for a shared surface or the peak.', null));
  }

  function buyersBlock(d) {
    const head = { title: 'What do we offer people who already buy?', sub: 'Referral and loyalty, priced in product at landed cost against paid media per new customer and gross margin.' };
    const ro = d.referral, lo = d.loyalty;
    const parts = [];
    const ra = ACTIONS.find((x) => x.rule_id === 'OFFER-R23'), la = ACTIONS.find((x) => x.rule_id === 'OFFER-R24');
    if (ro && !ro.unavailable) parts.push(el('div', { class: 'card' }, el('h4', { text: 'Referral: give one, get one' }), kv([
      ['Terms', ro.terms], ['Paid media per new customer', fmt.money(ro.paid_cac)], ['Cost per referred customer', fmt.money(ro.cost_per_referral) + ', ' + pct(ro.share_of_cac, 0) + ' of paid'],
      ['Cap (half of paid)', fmt.money(ro.cap)]]), el('p', { class: 'micro faint', text: ro.basis + '.' })));
    else parts.push(el('div', { class: 'card' }, el('h4', { text: 'Referral' }), el('p', { class: 'muted small', text: NA + ': ' + ((ro || {}).reason || 'no data') })));
    if (lo && !lo.unavailable) parts.push(el('div', { class: 'card' }, el('h4', { text: 'Loyalty: ' + pct(lo.earn, 0) + ' back' }), kv([
      ['Gross margin', pct(lo.gross_margin, 0)], ['Paid in cash', pct(lo.cash_share_of_margin, 1) + ' of gross margin'],
      ['Paid in product', pct(lo.product_share_of_margin, 1) + ' of gross margin'], ['Cap', pct(lo.cap, 0) + ' of gross margin (our own heuristic)']]),
      el('p', { class: 'micro faint', text: lo.basis + '.' })));
    const line = [ra ? 'No referral offer: launch give-one-get-one at ' + fmt.money(ro.cost_per_referral) + ' a customer.' : '', la ? 'No loyalty program: pay points in product.' : ''].filter(Boolean).join(' ') || 'Referral and loyalty offers are in place.';
    return section('desk-buyers', head, el('div', { class: 'grid two' }, ...parts), actionLine(line, ra || la));
  }

  function subscriptionBlock(sn) {
    const head = { title: 'Should we offer a subscription? Parked, with what would decide it', sub: 'Not built. The brand\'s own numbers that a subscription decision would start from, and the data it still needs.' };
    if (!sn) return section('desk-subscription', head, UI.emptyState({ screen: SLUG, title: 'No note', text: 'No brand folder.' }));
    const facts = kv([
      ['Status', 'Parked. ' + sn.reason],
      ['Buy again in month 1', pct(sn.month_1)], ['Still buying in month 6', pct(sn.month_6)],
      ['Deepest subscribe discount the top lines can fund', sn.funding.length ? sn.funding.map((f) => f.sku + ' ' + (f.max_depth == null ? 'none' : pct(f.max_depth, 0))).join(', ') : NA],
    ]);
    return section('desk-subscription', head, el('div', { class: 'card' }, facts, el('ul', { class: 'small' }, sn.questions.map((q) => el('li', { text: q })))),
      actionLine('Parked by the founder. Nothing to approve; the questions above are what the subscription product will answer first.', null));
  }

  function returnsChart(r) {
    if (!r || !r.groups || !r.groups.length) return el('p', { class: 'muted small', text: 'Returns by reason ' + NA + '.' });
    const rows = r.groups.slice().sort((a, b) => b.per_1000 - a.per_1000);
    return Charts.bar({ labels: rows.map((g) => g.reason), series: [{ name: 'Returns per 1,000 orders', values: rows.map((g) => g.per_1000) }], values: true,
      title: r.fixture ? 'Fixture: returns per 1,000 orders by reason (shape only, not brand data)' : 'Returns per 1,000 orders by reason, ' + r.window.label,
      note: r.fixture ? 'Returns by reason are ' + NA + ': ' + r.reason + '. The bars are a labelled fixture so the layout can be checked. The action reads the real metric once order rows connect.' : 'Returns opened in the window over paid orders placed in it. Carrier returns left out.' });
  }

  function objectionBlock(rows, returns) {
    const head = { title: 'Which deal-breaker doubt gets which offer?', sub: 'The top rung of each objection ladder in the brain. A rung with no proof gets an offer, a guarantee line or proof on the page, priced from finance inputs.' };
    const findA = (r) => ACTIONS.find((x) => x.rule_id === 'OFFER-R04' && x.entity && x.entity.id === r.theme_key + '.deal_breaker');
    const table = UI.verdictTable({
      columns: [
        { key: 'theme', label: 'Objection' },
        { key: 'doubt', label: 'Deal-breaker doubt' },
        { key: 'one_star', label: 'One-star', unit: 'n' },
        { key: 'offer', label: 'Offer or proof to launch' },
        { key: 'covered', label: 'Already in policy', format: (v, r) => r.covered_by.length ? r.covered_by.map((c) => c.id.split('.').slice(1).join('.')).join(', ') : 'nothing' },
        { key: 'cost_per_claim', label: 'Cost per claim', format: (v, r) => r.claim === 'none' ? 'none' : v == null ? NA : fmt.money(v) },
        { key: 'cost_per_1000_orders', label: 'Per 1,000 orders', format: (v, r) => r.claim === 'none' ? 'none' : v == null ? 'rate ' + NA : fmt.money(v) },
        { key: 'ret', label: 'Returns per 1,000', format: (v, r) => r.returns.per_1000 != null ? r.returns.per_1000.toFixed(1) : (r.returns.reasons.length ? NA : 'no reason maps') },
      ],
      rows: withActs(rows.map((r) => Object.assign({ covered: '', ret: '' }, r)), (r) => [findA(r) ? { label: 'Open action', onClick: () => openAction(findA(r)) } : { label: 'Copy spec', cls: 'quiet', onClick: () => UI.copy(r.spec) }]),
      verdict: { at: 1, kind: (r) => r.answered ? 'keep' : 'fix', text: (r) => r.answered ? 'Answered' : 'No proof', reason: (r) => 'rung ' + r.rung },
      actions: { label: 'Do' },
      sort: false,
    });
    const open = rows.filter((r) => !r.answered);
    const top = open.slice().sort((a, b) => b.one_star - a.one_star)[0];
    return section('desk-objections', head, el('div', { class: 'card tight' }, table),
      el('div', { class: 'grid two' }, el('div', { class: 'card' }, returnsChart(returns)),
        el('div', { class: 'card' }, el('h4', { text: top ? 'The spec for the biggest open doubt' : 'Every deal-breaker has proof' }),
          top ? el('pre', { class: 'spec', text: top.spec }) : null, top ? UI.copyButton({ label: 'Copy spec', text: () => top.spec }) : null)),
      actionLine(open.length + ' of ' + rows.length + ' deal-breaker doubts have no proof. Launch the offer for the biggest one first.', top ? findA(top) : null));
  }

  // ---------- 6. the audit ----------
  function auditBlock(d) {
    mount('#audit', UI.sectionHead({ title: 'The audit', sub: d.findings.length + ' findings from ' + d.rules.length + ' rules. Every rule reads brand records and tables; none calls a model.',
      tools: [el('button', { class: 'btn sm', type: 'button', text: 'Export findings CSV', onclick: () => UI.csv(d.findings.map((f) => ({ id: f.id, rule: f.rule_id, severity: f.severity, status: f.status, sentence: f.sentence, stake_usd: f.money_at_stake && f.money_at_stake.usd, money_reason: f.money_reason || '' })), null, 'offers-findings.csv') })] }),
      el('div', { class: 'card tight' }, UI.table({ columns: [
        { key: 'rule_id', label: 'Rule' }, { key: 'name', label: 'What it checks' }, { key: 'entity_type', label: 'On' },
        { key: 'inputs', label: 'Reads', format: (v) => (v || []).join(', ') }, { key: 'capability', label: 'Capability' },
        { key: 'fired', label: 'Fired', unit: 'n' },
      ], rows: d.rules.map((r) => Object.assign({}, r, { fired: d.findings.filter((f) => f.rule_id === r.rule_id).length })), sort: false })));
  }

  function render(d) {
    ACTIONS = d.plan || [];
    badge(d.brand || {});
    plan(d);
    wrong(d);
    actionsList(d);
    const TABS = [
      { key: 'launch', label: 'Launch next', rules: ['OFFER-R11', 'OFFER-R12', 'OFFER-R21'],
        blocks: () => [testsBlock(d.tests), registryBlock(d.registry), calendarBlock(d.calendar), depthBlock(d.depth), giftingBlock(d.gifting), secondOrderBlock(d.cohorts)] },
      { key: 'offers', label: 'Offers', rules: ['OFFER-R08', 'OFFER-R10', 'OFFER-R19', 'OFFER-R20', 'OFFER-R23', 'OFFER-R24', 'OFFER-R04', 'OFFER-R14', 'OFFER-R15'],
        blocks: () => [firstOrderBlock(d.first_order), cartBlock(d.cart), buyersBlock(d), objectionBlock(d.objections || [], d.returns), guaranteeBlock(d.guarantee, d.returns), subscriptionBlock(d.subscription), stackBlock(d.stack || [])] },
      { key: 'prices', label: 'Prices and packs', rules: ['OFFER-R22', 'OFFER-R16', 'OFFER-R17', 'OFFER-R07', 'OFFER-R09'],
        blocks: () => [costBlock(d.costs), positionBlock(d.position, d.brand || {}), parityBlock(d.parity), ladderBlock(d.ladder), waterfallBlock(d.waterfalls)] },
      { key: 'shipping', label: 'Shipping and discounts', rules: ['OFFER-R01', 'OFFER-R05', 'OFFER-R06', 'OFFER-R18', 'OFFER-R25'],
        blocks: () => [thresholdBlock(d.threshold), discountBlock(d)] },
    ];
    const openIn = (t) => ACTIONS.filter((a) => a.status === 'open' && (a.finding_ids || []).some((id) => t.rules.some((r) => id.indexOf('.' + r + '.') >= 0))).length;
    let saved = null;
    try { saved = localStorage.getItem('offers-desk-tab'); } catch (e) { saved = null; }
    mount('#desk', el('div', { class: 'desk-kicker' }, UI.sectionHead({ title: 'The desk', sub: 'The offer strategist\'s working tables, by job. Every block ends in the move it supports.' })),
      UI.tabs({ items: TABS.map((t) => ({ key: t.key, label: t.label, n: openIn(t), panel: () => el('div', null, ...t.blocks()) })),
        current: TABS.some((t) => t.key === saved) ? saved : 'launch',
        onChange: (k) => { try { localStorage.setItem('offers-desk-tab', k); } catch (e) { /* per-viewer convenience only */ } } }));
    auditBlock(d);
  }

  UI.api('/api/' + SLUG + '/overview?brand=' + encodeURIComponent(brand))
    .then(render)
    .catch((e) => mount('#plan', UI.emptyState({ screen: SLUG, title: 'Could not load', text: String(e.message || e) })));
})();
