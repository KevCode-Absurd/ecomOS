// Read Google Analytics numbers from Metabase dashboard 26 (E-Commerce Analytics), for traffic.json and geo.json.
//
// Run inside a signed-in tab on https://analyze.gehnaindia.com (console, or Claude with the browser's
// JavaScript tool). It only reads: each card query is a POST, but nothing is saved or changed in Metabase.
//
//   gaPull.start('2026-09-24')      // 12 weeks ending that day, plus cities for 90 and 28 days
//   gaPull.status()                 // "done" when finished (about 1 minute)
//   gaPull.text()                   // the JSON to save
//
// Cards: 725 top landing pages by source/medium, 731 purchases by source/medium, 751 new vs return users,
// 730 users by city. Meta spend by state comes from the Meta connector (region breakdown), not from here.
(() => {
  const DASH = 26, FROM = '8f0eb729';
  let dash = null;
  const st = { status: 'idle', out: null };
  async function q(dcId, from, to) {
    dash = dash || await (await fetch(`/api/dashboard/${DASH}`)).json();
    const dc = dash.dashcards.find((c) => c.id === dcId);
    const params = (dc.parameter_mappings || []).map((m) => ({ id: m.parameter_id, type: 'date/single', value: m.parameter_id === FROM ? from : to, target: m.target }));
    const r = await fetch(`/api/dashboard/${DASH}/dashcard/${dcId}/card/${dc.card_id}/query`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ parameters: params }) });
    const j = await r.json();
    if (j.error) throw new Error(`card ${dcId}: ${j.error}`);
    return j.data.rows || [];
  }
  const iso = (d) => d.toISOString().slice(0, 10);
  const back = (s, n) => { const d = new Date(s + 'T00:00:00Z'); d.setUTCDate(d.getUTCDate() - n); return iso(d); };
  async function run(end) {
    const out = { pulled_at: new Date().toISOString(), source: 'Metabase dashboard 26, E-Commerce Analytics (Google Analytics 4)', weeks: [], cities: {} };
    for (let w = 0; w < 12; w++) {
      const b = back(end, 7 * w), a = back(b, 6);
      const [land, conv, nr] = await Promise.all([q(725, a, b), q(731, a, b), q(751, a, b)]);
      const src = {};
      for (const r of land) src[r[0]] = (src[r[0]] || 0) + r[2];
      out.weeks.push({ since: a, until: b, landings: src, purchases: Object.fromEntries(conv.map((r) => [r[0], r[1]])), users: Object.fromEntries(nr.map((r) => [r[0], r[1]])) });
    }
    for (const [k, a, b] of [['d90', back(end, 89), end], ['d28', back(end, 27), end], ['p28', back(end, 55), back(end, 28)]]) {
      const rows = await q(730, a, b);
      out.cities[k] = { since: a, until: b, rows: rows.filter((r) => r[1] >= 20).slice(0, 120), total: rows.reduce((t, r) => t + r[1], 0) };
    }
    st.out = out;
  }
  window.gaPull = {
    start(end) { st.status = 'running'; run(end).then(() => { st.status = 'done'; }, (e) => { st.status = 'error: ' + e.message; }); return 'started'; },
    status: () => st.status,
    text: () => JSON.stringify(st.out),
  };
})();
