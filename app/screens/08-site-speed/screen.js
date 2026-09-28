/* Screen 08-site-speed, round 0. Reads /api/08-site-speed/overview and composes kit components.
   Every number comes from the api (audit.build over app/metrics.py). Nothing is computed here but formatting. */
(function () {
  const { el, fmt } = UI;
  const SLUG = '08-site-speed';
  const AUTO = { agent_does: 'agent', founder_gate: 'founder_gate', human_assist: 'human_assist' };
  const brand = new URLSearchParams(location.search).get('brand') || 'bombas';
  const mb = (b) => (typeof b === 'number' ? (b / 1e6).toFixed(2) : null);
  const sec = (ms) => (typeof ms === 'number' ? (ms / 1000).toFixed(1) + ' s' : fmt.na);

  function section(title, ...kids) {
    return el('section', { class: 'section' }, el('h3', { text: title }), ...kids);
  }

  function banner(d) {
    const b = d.brand || {};
    const scale = b.scale != null && b.scale !== 1 ? ' Volumes are generated at ' + b.scale + ' scale.' : '';
    return el('div', { class: 'sample-badge', role: 'note' }, el('span', null,
      el('b', { text: b.name || b.brand || 'This brand' }),
      ' data here is simulated. Nothing is a real ' + (b.name || 'brand') + ' result.' + scale +
      ' The speed runs and script weights are fixtures until a real lab run replaces them. No live test was run on the store.'));
  }

  function tiles(d) {
    const t = d.tiles;
    const lcp = UI.tile(Object.assign({}, t.lcp, { name: t.lcp.name + (t.lcp.page ? ' (' + t.lcp.page + ')' : '') }));
    lcp.append(el('div', { class: 'plain', text: 'Target: 2.5 s or less' }));
    const w = UI.tile(Object.assign({}, t.weight, { value: t.weight.value == null ? null : +mb(t.weight.value), unit: ' MB' }));
    w.append(el('div', { class: 'plain', text: 'Target: ' + mb(t.weight.target) + ' MB or less' }));
    const cost = UI.tile(t.cost);
    cost.append(el('div', { class: 'plain', text: 'Uses the assumption below, not a Bombas measurement.' }));
    return el('div', { class: 'grid tiles' }, lcp, w, cost);
  }

  function assumption(d) {
    const a = d.assumption, m = d.cost_of_slowness;
    const lines = ['Assumption on this page: each second the main image takes past 2.5 s loses ' +
      Math.round(a.loss_per_second * 100) + ' percent of the orders those mobile sessions would make. It is a rule of thumb, not measured for this brand. A speed test on the store replaces it.'];
    if (m) {
      const i = m.inputs;
      lines.push('Cost of slowness = ' + fmt.int(i.mobile_sessions_28d) + ' mobile sessions x ' + i.seconds_over_target +
        ' s over target (median of the measured pages) x ' + i.loss_per_second_assumed + ' x ' +
        (i.cvr_overall * 100).toFixed(2) + ' percent conversion x ' + fmt.money(i.aov, null, 2) + ' order value = ' + fmt.money(m.usd) + ' in 28 days.');
    }
    return el('div', { class: 'card small' }, lines.map((t) => el('p', { text: t })));
  }

  function speedTable(d) {
    const s = d.speed, t = d.targets;
    if (s.unavailable) return UI.emptyState({ screen: SLUG, title: 'No speed run on file yet', text: s.reason, missing: [s.fix] });
    const rows = s.rows.map((r) => Object.assign({}, r, { mb: +mb(r.bytes), status: r.over_lcp_target ? 'over target' : 'within target' }));
    const note = 'Median of 3 runs per page and device, window ' + s.window.start + ' to ' + s.window.end + '. Targets: load 5.0 s, LCP 2.5 s, first paint 1.8 s, ' +
      mb(t.bytes) + ' MB, ' + t.requests + ' requests.' + (s.adapted ? ' The fixture has no run date and keeps the device in its variant column, so runs are read as baseline runs on ' + s.window.end + '.' : '');
    return el('div', null,
      UI.table({ columns: [
        { key: 'label', label: 'Page' }, { key: 'device', label: 'Device' },
        { key: 'fully_loaded_ms', label: 'Load (ms)', align: 'right', format: fmt.int },
        { key: 'lcp_ms', label: 'LCP (ms)', align: 'right', format: fmt.int },
        { key: 'fcp_ms', label: 'First paint (ms)', align: 'right', format: fmt.int },
        { key: 'mb', label: 'Weight (MB)', align: 'right', format: (v) => fmt.num(v, 2) },
        { key: 'requests', label: 'Requests', align: 'right', format: fmt.int },
        { key: 'status', label: 'LCP vs 2.5 s' }], rows, sort: false }),
      el('p', { class: 'muted small', text: note }));
  }

  function insights(d) {
    return el('div', { class: 'grid two' }, d.insights.map((i) => {
      const cap = i.capability ? (d.chain.find((c) => c.capability === i.capability) || {}).autonomy : null;
      return UI.insight({ sentence: i.sentence, rule: i.rule, severity: i.unavailable ? 'low' : i.severity,
        capability: i.capability, autonomy: AUTO[cap] || (i.capability === 'SITE-C21' ? 'agent' : 'human_assist'),
        evidence: i.evidence ? i.evidence.join('. ') : (i.unavailable ? 'unavailable' : null), screen: SLUG,
        stub: 'Opens a developer brief for ' + i.capability + '. Nothing changes on the store until a person ships it.' });
    }));
  }

  function chainTable(d) {
    if (!d.chain.length) return el('p', { class: 'muted', text: 'The fix chain appears once a mobile baseline run is on file.' });
    const rows = d.chain.map((c) => ({ step: c.step, fix: c.fix, capability: c.capability, autonomy: UI.AUTONOMY[AUTO[c.autonomy]] || c.autonomy,
      saved: c.expected_ms_saved, lcp_saved: c.lcp_ms_saved, lcp_after: c.lcp_after, basis: c.basis,
      evidence: c.evidence_run || c.evidence_note }));
    return el('div', null,
      el('p', { class: 'muted small', text: 'On ' + d.slowest.label + ', mobile, in shipping order. Expected savings are estimates from the fixture weights at the lab speed of 1.6 Mbps. None is measured yet: a fix counts only once its own lab run is on file.' }),
      UI.table({ columns: [
        { key: 'step', label: '#', align: 'right' }, { key: 'fix', label: 'Fix' }, { key: 'capability', label: 'Capability' },
        { key: 'autonomy', label: 'Who' },
        { key: 'saved', label: 'Expected ms saved', align: 'right', format: fmt.int },
        { key: 'lcp_saved', label: 'LCP ms saved', align: 'right', format: fmt.int },
        { key: 'lcp_after', label: 'LCP after (ms)', align: 'right', format: fmt.int },
        { key: 'basis', label: 'Basis or why unavailable' }, { key: 'evidence', label: 'Evidence run' }], rows, sort: false }));
  }

  function briefs(d) {
    return el('div', { class: 'briefs' }, d.chain.map((c) => el('details', { class: 'card small' },
      el('summary', { text: c.step + '. ' + c.fix }),
      el('p', null, 'Fix capability ', el('code', { text: c.capability }), ' (' + (UI.AUTONOMY[AUTO[c.autonomy]] || 'unavailable') + '). Brief ',
        el('code', { text: c.brief.capability }), ' (' + (UI.AUTONOMY[AUTO[c.brief.autonomy]] || 'unavailable') + ').'),
      el('p', { text: 'Pass: ' + c.brief.pass + '.' }),
      el('p', { text: 'Rollback: ' + c.brief.rollback + '.' }),
      el('p', { class: 'muted', text: 'Stub. The brief writer is not built yet.' }))));
  }

  function scripts(d) {
    const rows = d.scripts.map((s) => Object.assign({}, s, {
      blocking: s.blocking == null ? null : s.blocking ? 'blocks' : 'after paint',
      over: s.over_budget == null ? null : s.over_budget ? 'over' : s.party === 'first' ? 'own code' : 'within' }));
    return el('div', null, UI.table({ columns: [
      { key: 'name', label: 'Script' }, { key: 'role', label: 'Role' }, { key: 'party', label: 'Party' }, { key: 'route', label: 'Route' },
      { key: 'kb', label: 'KB', align: 'right', format: fmt.int }, { key: 'est_ms', label: 'ms on slow 4G', align: 'right', format: fmt.int },
      { key: 'blocking', label: 'Blocking' }, { key: 'over', label: d.assumption.script_budget_kb + ' KB budget' },
      { key: 'cache', label: 'Cache' }, { key: 'revenue_link', label: 'Revenue tie' }, { key: 'brain_ref', label: 'Brain record' }],
      rows, sort: { key: 'kb', dir: 'desc' } }),
      el('p', { class: 'muted small', text: 'Names come from the brand brain (public site reads). Weights, blocking and cache are fixture values. Revenue tie is unavailable until the app inventory is connected.' }));
  }

  function film(d) {
    if (!d.film) return el('p', { class: 'muted', text: 'No mobile run on file, so there is nothing to play.' });
    return el('div', null, UI.filmstrip({ before: d.film.before, after: d.film.after,
      before_label: 'Now (fixture median)', after_label: 'At the 2.5 s target (not measured)',
      caption: d.film.label + ' on mobile. Frames are drawn from the run timings, not screenshots: blank, first paint, main image, ready.' }));
  }

  async function main() {
    const root = document.getElementById('app');
    let d;
    try { d = await UI.api('/api/' + SLUG + '/overview?brand=' + encodeURIComponent(brand)); }
    catch (e) { UI.mount(root, el('p', { class: 'muted', text: 'Could not load this screen: ' + e.message })); return; }
    UI.brand = d.brand;
    UI.mount(root,
      el('div', { class: 'screen-head' }, el('h1', { text: 'Site and speed' }),
        el('p', { text: 'Why pages are slow, what it costs, and the fixes in order.' })),
      banner(d),
      UI.founderNote(d.slowest
        ? 'Mobile shoppers wait ' + sec(d.slowest.lcp_ms) + ' for the main image on ' + d.slowest.label + '. The target is 2.5 s. Outside scripts are the biggest known cause in the fixture. Image and font weights are not logged yet.'
        : 'No speed run is on file yet. Ask the agent to capture a baseline.'),
      tiles(d),
      assumption(d),
      section('Insights', insights(d)),
      section('Main image time (LCP) by page', Charts.bar(Object.assign({ title: 'LCP by page, median ms' }, d.chart))),
      section('Pages', speedTable(d)),
      section('Fix chain', chainTable(d)),
      section('Filmstrip, slowest page', film(d)),
      section('Scripts', scripts(d)),
      section('Developer briefs', briefs(d)),
      section('Decision', el('p', { class: 'muted small', text: 'Capture a real baseline on the top pages, then measure each fix on a mirror of the page.' }),
        UI.decisionRow({ capability: 'SITE-C21', autonomy: 'agent', screen: SLUG,
          stub: 'The agent records the top pages into the speed lab mirror and runs 3 throttled mobile runs per page. Nothing on the live store changes.' })));
  }

  main();
})();
