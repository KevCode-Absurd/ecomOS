'use strict';
// Printable client report. Reads the same local API as the gallery. No credentials here.
let R_META = null;
let R_VIEW = null;
let R_SET = null;
const q = new URLSearchParams(location.search);
const R_FILTER = {
  since: q.get('since'), until: q.get('until'),
  kw: parseKw(q.get('kw')), camp: (q.get('camp') || '').split(',').filter((x) => /^\d{5,25}$/.test(x)),
};
const COMPARE = q.get('nocompare') !== '1';

async function boot() {
  try {
    R_META = await getJSON('/api/meta');
    R_SET = R_META.settings;
    setCurrency(R_META.meta.currency);
    if (!R_FILTER.since || !R_FILTER.until) { R_FILTER.until = R_META.meta.window.until; R_FILTER.since = addDays(R_FILTER.until, -29); }
    R_VIEW = await getJSON('/api/view?' + filterQuery(R_FILTER));
  } catch (e) {
    $('doc').innerHTML = `<p class="note">${esc(e.message)}</p>`;
    return;
  }
  $('agency').value = R_SET.branding.agency;
  $('client').value = R_SET.branding.client;
  $('note').value = R_SET.branding.note;
  for (const id of ['agency', 'client', 'note']) $(id).addEventListener('input', render);
  $('saveBrand').addEventListener('click', async () => {
    try {
      R_SET = await saveSettings({ ...R_SET, branding: { agency: $('agency').value, client: $('client').value, note: $('note').value } });
      $('msg').textContent = 'Branding saved.';
    } catch (e) { $('msg').textContent = 'Could not save: ' + e.message; }
  });
  $('print').addEventListener('click', () => window.print());
  render();
}

function kpiTile(label, cur, prev, kind, good) {
  const show = COMPARE && R_VIEW.previous.complete;
  return `<div class="kpi"><div class="k-label">${esc(label)}</div><div class="k-val">${fmt(cur, kind)}</div>` +
    (show ? `<div class="k-prev">${delta(cur, prev, good)} <span class="muted">prev ${fmt(prev, kind)}</span></div>` : '') + '</div>';
}

function adTile(ad) {
  const v = ad.view;
  const m = v.metrics;
  const p = COMPARE ? v.prev_metrics : null;
  const c = ad.creative;
  return `<div class="r-ad"><div class="thumb${c.display_quality !== 'full' ? ' low' : ''}"><span class="rank">#${v.rank_by_spend}</span>
      <img src="/img/${esc(ad.id)}" alt="" onerror="this.replaceWith(Object.assign(document.createElement('div'),{className:'noimg',textContent:'Image unavailable'}))"></div>
    <div class="body"><div class="name" title="${esc(ad.name)}">${esc(ad.name)}</div>
      <div class="chips">${verdictChip(v.verdict)}${fatigueChip(v.fatigue)}<span class="chip fmt">${esc(c.type_label)}</span></div>
      <div>Spend ${fmt(m.spend, 'money')} ${p ? delta(m.spend, p.spend, 0) : ''}</div>
      <div>ROAS ${fmt(m.roas, 'x')} ${p ? delta(m.roas, p.roas, 1) : ''} · CPA ${fmt(m.cpa, 'money')}</div>
      <div class="muted">${esc(ad.campaign_name)}</div></div></div>`;
}

function render() {
  const v = R_VIEW;
  const t = v.totals;
  const p = v.previous_totals || {};
  const r = v.range;
  const tg = v.targets;
  const agency = $('agency').value.trim();
  const client = $('client').value.trim() || R_META.meta.account_name || 'Meta ads';
  const note = $('note').value.trim();
  const top = v.collections.all.ad_ids.map((id) => v.ads[id]);
  const byCode = (code) => top.filter((a) => a.view.verdict.code === code);
  const fatigued = top.filter((a) => ['declining', 'ctr_down', 'roas_down'].includes(a.view.fatigue.code));
  const li = (a) => `<li>${esc(a.name)} <span class="muted">(${esc(a.creative.type_label)}, ${money(a.view.metrics.spend)}, ROAS ${a.view.metrics.roas !== null ? a.view.metrics.roas.toFixed(2) + 'x' : 'unavailable'})</span> ${esc(a.view.verdict.reason)}</li>`;
  const x = v.exclusions;
  const fmtRows = Object.values(v.by_type).sort((a, b) => b.spend - a.spend);
  const pv = v.previous;
  document.title = `${client} · Meta ads · ${r.since} to ${r.until}`;

  $('doc').innerHTML = `
    <header class="r-head"><div>
      ${agency ? `<div class="r-agency">${esc(agency)}</div>` : ''}
      <div class="r-title">${esc(client)} · Meta ads report</div>
      <div class="r-sub">${esc(dateLabel(r.since))} to ${esc(dateLabel(r.until))} (${r.days} days)${COMPARE && pv.complete ? ` · compared with ${esc(dateLabel(pv.since))} to ${esc(dateLabel(pv.until))}` : ''}</div>
      <div class="r-sub">Account ${esc(R_META.meta.account_name || '')} (act_${esc(R_META.meta.account_id)}) · ${esc(R_META.meta.currency)} · ${esc(R_META.meta.timezone || '')}</div>
    </div></header>
    ${note ? `<div class="r-note">${esc(note)}</div>` : ''}
    <section class="r-section"><h2>Results</h2><div class="kpis">
      ${kpiTile('Spend', t.spend, p.spend, 'money', 0)}
      ${kpiTile('Purchase value', t.purchase_value, p.purchase_value, 'money', 1)}
      ${kpiTile('ROAS', t.roas, p.roas, 'x', 1)}
      ${kpiTile('Purchases', t.purchases, p.purchases, 'int', 1)}
      ${kpiTile('CPA', t.cpa, p.cpa, 'money', -1)}
      ${kpiTile('Link CTR', t.link_ctr, p.link_ctr, 'pct', 1)}
    </div>
    <p class="small muted">${t.ads} ads spent in these dates. ROAS = total purchase value ÷ total spend. ${t.ads_without_reported_value} ads had no reported purchase value; their spend still counts.${COMPARE && !pv.complete ? ' No change figures: the previous period is not fully inside the stored year.' : ''}</p></section>
    <section class="r-section"><h2>By format</h2>
      <table class="fmt-table"><tr><th>Format</th><th class="n">Ads</th><th class="n">Spend</th><th class="n">Share</th><th class="n">Purchase value</th><th class="n">ROAS</th><th class="n">CPA</th></tr>
      ${fmtRows.map((f) => `<tr><td>${esc(f.label)}</td><td class="n">${f.ads}</td><td class="n">${fmt(f.spend, 'money')}</td><td class="n">${t.spend ? (f.spend / t.spend * 100).toFixed(1) + '%' : ''}</td><td class="n">${fmt(f.purchase_value, 'money')}</td><td class="n">${fmt(f.roas, 'x')}</td><td class="n">${fmt(f.cpa, 'money')}</td></tr>`).join('')}
      <tr class="total"><td>All formats</td><td class="n">${t.ads}</td><td class="n">${fmt(t.spend, 'money')}</td><td class="n">100%</td><td class="n">${fmt(t.purchase_value, 'money')}</td><td class="n">${fmt(t.roas, 'x')}</td><td class="n">${fmt(t.cpa, 'money')}</td></tr></table></section>
    <section class="demo r-section">${demoBlock([{ view: { demographics: v.demographics_all } }], bucketNote(v.demographics_buckets, v.demographics_exact, r) + ' Covers every ad in the report.')}</section>
    <section><h2>Top 12 ads by spend</h2><div class="r-ads">${top.slice(0, 12).map(adTile).join('')}</div></section>
    <section class="r-section"><h2>What to do next</h2>
      <p class="small muted">Verdicts compare each ad in the top 30 by spend with the targets: ROAS ${tg.roas ? tg.roas.toFixed(2) + 'x' : 'not set'} (${esc(tg.roas_source)}) and CPA ${tg.cpa ? money(tg.cpa) : 'not set'} (${esc(tg.cpa_source)}). Scale = ROAS at or above target. Watch = within 30% below target, or no purchases yet with spend under 2x target CPA. Cut = more than 30% below target, or no purchases after 2x target CPA. Not enough data = spent less than 1 target CPA.</p>
      <div class="r-two">
        <div><h3>Scale (${byCode('scale').length})</h3><ul class="r-list">${byCode('scale').slice(0, 8).map(li).join('') || '<li class="muted">None</li>'}</ul></div>
        <div><h3>Cut (${byCode('cut').length})</h3><ul class="r-list">${byCode('cut').slice(0, 8).map(li).join('') || '<li class="muted">None</li>'}</ul></div>
      </div>
      ${fatigued.length ? `<h3 style="margin-top:12px">Signs of fatigue (${fatigued.length})</h3><ul class="r-list">${fatigued.slice(0, 8).map((a) => `<li>${esc(a.name)}: ${esc(a.view.fatigue.reason)}</li>`).join('')}</ul>` : ''}
    </section>
    <footer class="r-foot">
      <div>${x.campaigns.length ? `Excluded from every figure: ${x.campaigns.length} campaign${x.campaigns.length > 1 ? 's' : ''} (${x.ads} ads, ${money(x.spend)})${x.keywords.length ? `, matched by name: ${esc(x.keywords.join(', '))}` : ''}.` : 'No campaigns excluded.'}</div>
      <div>Purchases and purchase value are Meta's reported figures under each ad set's attribution setting (mostly 7-day click and 1-day view). "Unavailable" means Meta reported none; it is not counted as zero.</div>
      <div>Source: ${esc(R_META.meta.source)}. Data captured ${esc(new Date(R_META.meta.captured_at).toLocaleString('en-IN'))}. Read-only; nothing in the account was changed.</div>
    </footer>`;
}
boot();
