/* Wild bets and PR, round 0. Reads /api/27-wild-bets-pr/overview and composes kit components.
   No numbers are computed here; the server sends every value, rule and sentence. */
(function () {
  'use strict';
  const SLUG = '27-wild-bets-pr';
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
      ': simulated data. Visits, posts, ads, the bet queue and brief status are generated for this demo. Nothing here is a ' +
      name + ' plan or result. Stories, milestones, launches and Reddit frames are public and come from the brand brain.');
  }

  function chip(text, tone) { return el('span', { class: 'chip ' + (tone || ''), text }); }

  function tile(t) {
    const src = (t.sources || []).map((s) => s.table).join(', ');
    return UI.tile(Object.assign({}, t, { freshness: t.freshness ? fmt.date(t.freshness) + (src ? ' from ' + src : '') : null }));
  }

  function board(bets, stages, bound) {
    return el('div', null,
      el('p', { class: 'th', text: 'A bet needs all 8 bound fields (' + bound.map((f) => f.replace(/_/g, ' ')).join(', ') +
        ') before it can move to executing. Every claim must be tier approved or site_backed in the brain.' }),
      el('div', { class: 'board' }, stages.map((s) => {
        const here = bets.filter((b) => b.stage === s);
        return el('div', { class: 'col card' }, el('h4', { text: s + ' (' + here.length + ')' }),
          here.length ? here.map((b) => el('div', { class: 'bet' },
            el('b', { text: b.bet_id + ' ' + b.title }),
            el('div', { class: 'meta' + (b.overdue ? ' late' : ''), text: b.days_in_stage + ' days in stage, plan ' + b.planned_stage_days }),
            el('div', { class: 'meta', text: 'Bound ' + (b.bound_filled == null ? 'not started' : b.bound_filled + ' of ' + b.bound_total) +
              (b.budget_cap_usd != null ? ', cap ' + fmt.money(b.budget_cap_usd) : '') }),
            el('div', { class: 'meta', text: 'Moves ' + b.metric.replace(/_/g, ' ') }),
            el('div', { class: 'meta', text: 'Claims: ' + b.claims.map((c) => c.id.split('.').slice(1).join('.') + ' (' + (c.tier || 'missing') + ')').join(', ') }),
            b.ties_ok ? null : chip('claim not backed', 'bad'))) : el('div', { class: 'empty-col', text: 'none' }));
      })),
      UI.decisionRow({ capability: 'BRAND-C44', autonomy: 'agent', screen: SLUG,
        stub: 'Log 3 new wild bet ideas, each tied to a brain record and a room metric, with claims from approved or site-backed records only. Nothing launches; your choice is logged.' }));
  }

  function chart(c) {
    if (c.unavailable) return UI.emptyState({ screen: SLUG, title: 'No sessions', text: c.reason, missing: [c.fix] });
    return el('div', { class: 'card' }, Charts.line({ labels: c.labels, series: c.series, unit: 'n',
      title: 'Direct and referral visits by week, ' + c.window,
      note: c.note }));
  }

  function launchTable(rows) {
    return el('div', null,
      el('p', { class: 'th', text: 'Direct and referral visits as a share of all visits, 14 days after each launch against the median of the 4 windows before. Share, not count, so the fall ramp does not read as press. No press log is connected yet.' }),
      el('div', { class: 'card scroll' }, UI.table({
        columns: [
          { key: 'launch', label: 'Launch' },
          { key: 'date', label: 'Date' },
          { key: 'share_before', label: 'Share before', unit: '%' },
          { key: 'share_after', label: 'Share after', unit: '%' },
          { key: 'lift', label: 'Lift', align: 'right', format: (v) => v == null ? 'unavailable' : v.toFixed(2) + 'x' },
          { key: 'press_logged', label: 'Press logged', format: (v) => v == null ? 'no press log' : String(v) },
        ], rows, sort: false })));
  }

  function calendarTable(c) {
    const r = c.readiness;
    return el('div', null,
      el('p', { class: 'th', text: 'Briefs ready for ' + (r.value == null ? 'unavailable' : fmt.pct(r.value)) + ' of ' + r.moments +
        ' moments in the ' + r.window + '. Dates are public; relevance and brief status are simulated.' }),
      el('div', { class: 'card scroll' }, UI.table({
        columns: [
          { key: 'date', label: 'Date' },
          { key: 'moment', label: 'Moment' },
          { key: 'days_away', label: 'Days away', unit: 'n' },
          { key: 'relevance', label: 'Relevance' },
          { key: 'why', label: 'Why it matters' },
          { key: 'brief_id', label: 'Brief', format: (v) => v || 'not started' },
        ], rows: c.rows, sort: false })));
  }

  function storyTable(s) {
    if (s.unavailable) return UI.emptyState({ screen: SLUG, title: 'No brain', text: 'No story bank on file.', missing: ['brain'] });
    return el('div', null,
      el('p', { class: 'th', text: s.dated + ' of ' + s.total + ' stories carry a date of their own. The rest only carry the day they were read.' }),
      el('div', { class: 'card scroll stories' }, UI.table({
        columns: [
          { key: 'dated', label: 'Own date', format: (v) => v ? 'yes' : 'no' },
          { key: 'source_type', label: 'Source' },
          { key: 'tier', label: 'Tier' },
          { key: 'text', label: 'Story' },
        ], rows: s.rows, sort: false })));
  }

  function metricList(ms) {
    return el('div', { class: 'card scroll' }, UI.table({
      columns: [
        { key: 'plain', label: 'Metric' },
        { key: 'name', label: 'Id' },
        { key: 'value', label: 'Value', format: (v, r) => v == null ? 'unavailable: ' + r.unavailable_reason :
          Object.entries(v).filter(([, n]) => n !== 0).map(([k, n]) => k + ' ' + n).join(', ') },
        { key: 'source', label: 'Source' },
      ], rows: ms, sort: false }));
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
        ' (' + Object.entries(f.money_at_stake.inputs).map(([k, v]) => k + ' ' + v).join(', ') + ')' })
        : el('div', { class: 'money', text: 'Money at stake unavailable: ' + (f.money_reason || 'no baseline') }),
      f.status === 'unavailable' ? el('div', { class: 'money', text: 'Needs ' + f.unavailable.inputs.join(', ') + ' from ' + f.unavailable.connector + '. ' + f.unavailable.fix }) : null,
      f.brain_refs.length ? el('div', { class: 'money', text: 'Brain: ' + f.brain_refs.join(', ') }) : null)));
  }

  function render(d) {
    const b = d.brand || {};
    const t = d.tiles || {};
    UI.mount('#app',
      el('header', { class: 'screen-head' }, el('h1', { text: 'Wild bets and PR' }),
        el('p', { text: 'Bets with a bound and a read point, press, launches, and the dates that matter. Through ' + fmt.date(b.as_of) + '.' })),
      simBanner(b),
      section('Where things stand', el('div', { class: 'grid tiles three' }, tile(t.bets), tile(t.earned), tile(t.press))),
      section('What the rules say', el('div', { class: 'grid two' }, (d.insights || []).map((i) =>
        UI.insight({ sentence: i.sentence, rule: i.rule, severity: i.severity, capability: i.capability,
          autonomy: AUTONOMY_KIT[i.autonomy] || i.autonomy, screen: SLUG })))),
      section('Direct and referral visits, the PR proxy', chart(d.chart)),
      section('Wild bet pipeline', board(d.bets || [], d.stages || [], d.bound_fields || [])),
      section('Launches and press', launchTable(d.launches || [])),
      section('Moments in the next 90 days', calendarTable(d.calendar)),
      section('Story bank dating', storyTable(d.stories || {})),
      section('Room metrics and their sources', metricList(d.metrics || [])),
      section('Audit findings', findingsList(d.findings || [])),
      section('Actions', el('div', { class: 'actions' }, (d.actions || []).map((a) => el('div', { class: 'card' },
        el('b', { text: a.label }), UI.decisionRow({ capability: a.capability, autonomy: AUTONOMY_KIT[a.autonomy], screen: SLUG,
          stub: a.label + '. Nothing is sent or published; your choice is logged.' }))))));
  }

  UI.api('/api/' + SLUG + '/overview?brand=' + encodeURIComponent(brand))
    .then(render)
    .catch((e) => UI.mount('#app', el('header', { class: 'screen-head' }, el('h1', { text: 'Wild bets and PR' })),
      UI.emptyState({ screen: SLUG, title: 'Could not load', text: String(e.message || e) })));
})();
