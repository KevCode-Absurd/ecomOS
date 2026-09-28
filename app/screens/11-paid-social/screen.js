/* Paid social, round 0. Reads /api/11-paid-social/overview and composes kit components.
   No numbers are computed here; the server sends every value, rule and sentence. */
(function () {
  'use strict';
  const SLUG = '11-paid-social';
  const { el, fmt } = UI;
  const brand = new URLSearchParams(location.search).get('brand') || 'bombas';
  const AUTONOMY_KIT = { agent_does: 'agent', founder_gate: 'founder_gate', human_assist: 'human_assist', agent: 'agent' };
  const VERDICT_CHIP = { kill: 'bad', scale: 'good', watch: 'warn', wait: '', off: '', unavailable: '' };

  function section(title, ...children) {
    return el('section', { class: 'section' }, el('h3', { text: title }), ...children);
  }

  function simBanner(b) {
    const name = b.name || b.brand || 'This brand';
    if (!b.simulated) return el('div', { class: 'sim', role: 'note' }, el('b', { text: name }), ' live data. Read-only.');
    return el('div', { class: 'sim', role: 'note' }, el('b', { text: name }),
      ': simulated data. Every number on this page is generated from a public profile. Nothing here is a ' + name + ' result.');
  }

  function freshness(t) {
    const src = (t.sources || []).map((s) => s.table).join(', ');
    return t.freshness ? (fmt.date(t.freshness) + (src ? ' from ' + src : '')) : null;
  }

  function tile(t, extra) {
    return UI.tile(Object.assign({}, t, { freshness: freshness(t) }, extra || {}));
  }

  function verdictChip(v) { return el('span', { class: 'chip ' + (VERDICT_CHIP[v] || ''), text: v }); }

  function flags(r) {
    const out = [];
    if (r.shared_creative) out.push('shared image');
    if (r.dynamic_creative) out.push('dynamic');
    if (r.fatigue) out.push('fatigue');
    return out.join(', ') || '';
  }

  function killScale(ks, th) {
    const cols = [
      { key: 'ad', label: 'Ad' },
      { key: 'campaign', label: 'Campaign' },
      { key: 'spend', label: 'Spend 7d', unit: '$' },
      { key: 'roas', label: 'ROAS', unit: 'x' },
      { key: 'frequency', label: 'Freq', unit: 'x' },
    ];
    const kill = UI.table({
      columns: cols.concat([{ key: 'money_at_stake', label: 'Not paid back', align: 'right', format: (v) => v ? fmt.money(v.usd) : 'unavailable' }]),
      rows: ks.kill, sort: false, empty: 'No ad is under break-even with spend above the floor.' });
    const scale = UI.table({ columns: cols.concat([{ key: 'cpa', label: 'CPA', unit: '$' }]), rows: ks.scale, sort: false,
      empty: 'No ad is above target at a frequency under 2.5.' });
    const lines = [];
    if (th.break_even != null) lines.push('Break-even ' + fmt.ratio(th.break_even) + ': ' + th.break_even_source + '.');
    if (th.target_roas != null) lines.push('Target ' + fmt.ratio(th.target_roas) + ': ' + th.target_source + '.');
    if (th.floor != null) lines.push('Spend floor ' + fmt.money(th.floor) + ': ' + th.floor_source + '.');
    return el('div', null,
      el('p', { class: 'th', text: lines.join(' ') }),
      el('div', { class: 'ks' },
        el('div', { class: 'card' }, el('h4', { text: 'Kill (' + ks.kill.length + ')' }), kill),
        el('div', { class: 'card' }, el('h4', { text: 'Scale (' + ks.scale.length + ')' }), scale)),
      UI.decisionRow({ capability: 'MEDIA-C17', autonomy: 'founder_gate', screen: SLUG,
        stub: 'Pause the ' + ks.kill.length + ' ads under break-even and raise budget on the ' + ks.scale.length +
          ' ready to scale. Nothing changes in the ad account until the agent layer exists; your choice is logged.' }));
  }

  function creatives(rows) {
    return UI.table({
      columns: [
        { key: 'ad', label: 'Ad' },
        { key: 'format', label: 'Format' },
        { key: 'campaign', label: 'Campaign' },
        { key: 'spend', label: 'Spend 7d', unit: '$' },
        { key: 'purchases', label: 'Purchases', unit: 'n' },
        { key: 'roas', label: 'ROAS', unit: 'x' },
        { key: 'cpa', label: 'CPA', unit: '$' },
        { key: 'ctr', label: 'CTR', unit: '%' },
        { key: 'ctr_prev', label: 'CTR prior 7d', unit: '%' },
        { key: 'frequency', label: 'Freq', unit: 'x' },
        { key: 'verdict', label: 'Verdict', format: (v) => v },
        { key: 'flags', label: 'Flags', format: (v, r) => flags(r) },
      ],
      rows: rows.map((r) => Object.assign({ flags: flags(r) }, r)), sort: { key: 'spend', dir: 'desc' }, maxRows: 60,
    });
  }

  function chart(c) {
    if (c.unavailable) return UI.emptyState({ screen: SLUG, title: 'No daily ad rows', text: c.reason, missing: [c.fix] });
    const labels = c.labels.map((d) => d.slice(5));
    return el('div', { class: 'card chart-pair' },
      Charts.line({ labels, series: [{ name: 'Spend', values: c.spend }], unit: '$', title: 'Meta spend per day, ' + c.window, maxLabels: 5 }),
      Charts.line({ labels, series: [{ name: 'Purchases', values: c.purchases, color: 'var(--s2)' }], unit: 'n',
        title: 'Purchases per day, ' + c.window, note: 'Purchases are ' + c.basis + '.', maxLabels: 5 }));
  }

  function findingsList(fs) {
    if (!fs.length) return el('p', { text: 'No findings this run.' });
    return el('div', { class: 'card' }, fs.map((f) => el('div', { class: 'finding' },
      el('div', { class: 'tags' },
        el('span', { class: 'chip ' + (f.severity === 'critical' || f.severity === 'high' ? 'bad' : 'warn'), text: f.severity }),
        el('span', { class: 'chip mono', text: f.rule_id }),
        el('span', { class: 'chip mono', text: f.capability.id }),
        f.confidence < 0.3 ? el('span', { class: 'chip', text: 'weak evidence' }) : null),
      el('div', { text: f.sentence }),
      f.money_at_stake ? el('div', { class: 'money', text: fmt.money(f.money_at_stake.usd) + ' at stake = ' + f.money_at_stake.formula +
        ' (' + Object.entries(f.money_at_stake.inputs).map(([k, v]) => k + ' ' + v).join(', ') + ')' })
        : el('div', { class: 'money', text: 'Money at stake unavailable: ' + (f.money_reason || 'no baseline') }),
      f.flags ? el('div', { class: 'money', text: f.flags.join('; ') }) : null)));
  }

  function render(d) {
    const b = d.brand || {};
    const parts = [
      el('header', { class: 'screen-head' }, el('h1', { text: 'Paid social' }),
        el('p', { text: 'Meta, ad level, through ' + fmt.date(b.as_of) + '. Is spend on pace, what is working, what to cut.' })),
      simBanner(b),
    ];
    const t = d.tiles || {};
    parts.push(section('Pace and return',
      el('div', { class: 'grid tiles four' }, tile(t.pacing), tile(t.roas, { delta_label: 'vs prior 28d' }),
        tile(t.mer, { delta_label: 'vs prior 28d' }), tile(t.cpa, { delta_label: 'vs prior 28d' }))));
    if (d.unavailable) {
      parts.push(UI.emptyState({ screen: SLUG, title: 'Meta is not connected', text: d.reason, missing: [d.fix] }));
      parts.push(section('Audit findings', findingsList(d.findings || [])));
      return UI.mount('#app', ...parts);
    }
    parts.push(section('What the rules say', el('div', { class: 'grid two' }, (d.insights || []).map((i) =>
      UI.insight({ sentence: i.sentence, rule: i.rule, severity: i.severity, capability: i.capability,
        autonomy: AUTONOMY_KIT[i.autonomy] || i.autonomy, screen: SLUG })))));
    parts.push(section('Kill and scale, last 7 days', killScale(d.kill_scale, d.thresholds)));
    parts.push(section('Daily spend and purchases', chart(d.chart)));
    parts.push(section('Every ad, last 7 days',
      el('p', { class: 'th', text: 'One row per ad. Ads that share an image keep their own rows. Dynamic creatives are flagged, not split. Frequency is from daily reach, so it reads low.' }),
      creatives(d.creatives)));
    parts.push(section('Audit findings', findingsList(d.findings || [])));
    UI.mount('#app', ...parts);
  }

  UI.api('/api/' + SLUG + '/overview?brand=' + encodeURIComponent(brand))
    .then(render)
    .catch((e) => UI.mount('#app', el('header', { class: 'screen-head' }, el('h1', { text: 'Paid social' })),
      UI.emptyState({ screen: SLUG, title: 'Could not load', text: String(e.message || e) })));
})();
