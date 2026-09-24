// Read Gehna's website sales from Metabase dashboard 6, day by day, for sales.json.
//
// Run inside a signed-in tab on https://analyze.gehnaindia.com (paste into the console, or
// Claude runs it with the browser's JavaScript tool). It only reads: each dashboard card query
// is a POST, but nothing is saved or changed in Metabase.
//
//   ecomPull.start('2026-09-17', '2026-09-23')         // starts in the background (~4 s a day)
//   ecomPull.status()                                   // "7/7 days, done"
//   ecomPull.chunks()                                   // number of 900-character pieces
//   ecomPull.chunk(0)                                   // read piece 0, 1, 2, ... and join them
//
// Pieces are 900 characters because the browser tool cuts replies off near 1,000.
//
// Save the joined text as a .json file, then: python -m meta_gallery.refresh sales FILE
//
// Output: {source, pulled_at, days: {date: entry}, month_totals: {YYYY-MM: summary}, ga: [...]}
// A day entry has the same shape as sales.json `daily`. month_totals come from the month cards
// (1st of the month to `until`) so the Python side can check its month figures against them.
// Traffic (ga) rows are [date, visits, add to carts, sales, orders] up to `until`.
(() => {
  const DASH = 6, RANGE_PARAM = 'a82b2b5d', TRAFFIC_CARD = 766;
  // dashcard id -> what it holds (checked against stored days on 24 Sep 2026)
  const C = { sales: 387, orders: 280, items: 281, ot: 289, refund: 386, retItems: 278, karat: 287,
    typesG: 290, typesS: 284, bandsG: 297, bandsS: 296, pay: 294, skusG: 277, skusS: 292, retG: 285, retS: 283 };
  const st = { dash: null, done: 0, total: 0, finished: false, error: null, out: null, text: '' };
  const t = (x) => x;  // keep values exactly as Metabase returns them (stored names can end in a space)

  async function dash() {
    if (!st.dash) st.dash = await (await fetch(`/api/dashboard/${DASH}`)).json();
    return st.dash;
  }
  async function q(dcId, range) {
    const dc = (await dash()).dashcards.find((c) => c.id === dcId);
    const m = (dc.parameter_mappings || []).find((p) => p.parameter_id === RANGE_PARAM);
    const body = { parameters: m && range ? [{ id: RANGE_PARAM, type: 'date/range', value: range, target: m.target }] : [] };
    const r = await fetch(`/api/dashboard/${DASH}/dashcard/${dcId}/card/${dc.card_id}/query`,
      { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
    const j = JSON.parse(await r.text());
    if (j.error) throw new Error(`card ${dcId}: ${j.error}`);
    return j.data.rows || [];
  }
  async function build(range, dayTotals) {
    const ids = Object.keys(C);
    const res = await Promise.all(ids.map((k) => q(C[k], range)));
    const R = Object.fromEntries(ids.map((k, i) => [k, res[i]]));
    const o = {};
    if (dayTotals) { o.sales = R.sales[0]?.[0] ?? null; o.orders = R.orders[0]?.[1] ?? 0; }
    o.items = R.items[0]?.[0] ?? 0;
    o.ot = Object.fromEntries(R.ot.map((r) => [t(r[0]), [r[1], r[3]]]));
    o.refund = R.refund[0]?.[0] ?? null;
    o.ret_items = R.retItems[0]?.[0] ?? 0;
    o.karat = R.karat.map((r) => [t(r[1]), r[0], r[2]]);
    o.types = [...R.typesG.map((r) => ['g', t(r[1]), r[0], r[3]]), ...R.typesS.map((r) => ['s', t(r[1]), r[0], r[3]])];
    o.bands = [...R.bandsG.map((r) => ['g', t(r[0]), r[1]]), ...R.bandsS.map((r) => ['s', t(r[0]), r[1]])];
    o.pay = R.pay.map((r) => [t(r[0]), r[1]]);
    o.ret = [...R.retG, ...R.retS].map((r) => [t(r[2]), t(r[3]), r[4], r[5]]);
    o.skus = [...R.skusG.map((r) => ['g', t(r[2]), t(r[3]), r[0], r[4]]), ...R.skusS.map((r) => ['s', t(r[2]), t(r[3]), r[0], r[4]])];
    return o;
  }
  const r2 = (x) => Math.round(x * 100) / 100;
  const sum = (rows, i) => r2(rows.reduce((a, r) => a + r[i], 0));
  function summary(m) {  // same shape as month_summary() in meta_gallery/refresh.py
    const otc = {}, otm = {};
    for (const k of Object.keys(m.ot).sort()) { otc[k] = m.ot[k][1]; otm[k] = r2(m.ot[k][0]); }
    return {
      counts: { items: m.items, ret_items: m.ret_items, ot: otc, karat: sum(m.karat, 2), types: sum(m.types, 3),
        bands: sum(m.bands, 2), pay: sum(m.pay, 1), skus: sum(m.skus, 4) },
      money: { refund: m.refund || 0, ot: otm, karat: sum(m.karat, 1), types: sum(m.types, 2), skus: sum(m.skus, 3) },
    };
  }
  function days(since, until) {
    const out = [];
    for (let d = new Date(since + 'T00:00:00Z'); d <= new Date(until + 'T00:00:00Z'); d.setUTCDate(d.getUTCDate() + 1)) out.push(d.toISOString().slice(0, 10));
    return out;
  }

  async function run(since, until) {
    const list = days(since, until);
    st.total = list.length; st.done = 0;
    const out = { source: 'Metabase dashboard 6, Online Website Sales Analytics (website orders only)',
      pulled_at: new Date().toISOString(), days: {}, month_totals: {}, ga: [] };
    for (const d of list) { out.days[d] = await build(`${d}~${d}`, true); st.done += 1; }
    for (const mk of [...new Set(list.map((d) => d.slice(0, 7)))]) {
      const [y, m] = mk.split('-').map(Number);
      const last = new Date(Date.UTC(y, m, 0)).toISOString().slice(0, 10);  // last day of that month
      out.month_totals[mk] = summary(await build(`${mk}-01~${until < last ? until : last}`, false));
    }
    out.ga = (await q(TRAFFIC_CARD, null)).map((r) => [r[0].slice(0, 10), r[1], r[2], r[3], r[4]])
      .filter((r) => r[0] >= since && r[0] <= until).sort((a, b) => (a[0] < b[0] ? -1 : 1));
    st.out = out; st.text = JSON.stringify(out); st.finished = true;
  }

  window.ecomPull = {
    start(since, until) {
      Object.assign(st, { finished: false, error: null, out: null, text: '' });
      run(since, until).catch((e) => { st.error = String(e); st.finished = true; });
      return 'started';
    },
    status: () => (st.error ? `error: ${st.error}` : `${st.done}/${st.total} days${st.finished ? ', done' : ''}`),
    chunks: (size = 900) => Math.ceil(st.text.length / size),
    chunk: (i, size = 900) => st.text.slice(i * size, (i + 1) * size),
    result: () => st.out,
  };
})();
