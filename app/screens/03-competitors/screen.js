/* Competitors and market, round 0. Reads /api/03-competitors/overview and audit. No writes except
   decisions through the kit's decision row. Competitor facts are public signals; brand prices are simulated. */
(function () {
  'use strict';
  const { el, mount, api, fmt } = UI;
  const BASE = '/api/03-competitors/';
  const SCREEN = '03-competitors';
  const NA = 'unavailable';
  const NS = 'http://www.w3.org/2000/svg';
  const pretty = (s) => String(s || '').replace(/_/g, ' ');
  const usd = (v) => v == null ? NA : '$' + Number(v).toFixed(2);
  const chips = (list, cls) => el('div', { class: 'chips' }, ...(list || []).map((t) => el('span', { class: 'chip ' + (cls || ''), text: t })));

  function svg(tag, attrs, text) {
    const n = document.createElementNS(NS, tag);
    for (const k of Object.keys(attrs || {})) n.setAttribute(k, attrs[k]);
    if (text != null) n.textContent = text;
    return n;
  }

  function band(p) {
    if (p.low != null && p.high != null) return usd(p.low) + ' to ' + usd(p.high);
    if (p.low != null) return 'from ' + usd(p.low);
    return 'median only';
  }

  function compCard(c) {
    const card = el('article', { class: 'card comp' });
    card.append(el('div', { class: 'head' }, el('b', { text: c.name }),
      c.ad_library_url ? el('a', { href: c.ad_library_url, target: '_blank', rel: 'noopener', class: 'small', text: 'Ad Library' }) : null));
    card.append(el('div', { class: 'small', text: c.positioning || NA }));
    const dl = el('dl');
    const row = (k, v) => dl.append(el('dt', { text: k }), el('dd', { text: v }));
    row('Price per pair', (c.price.median == null ? NA : 'median ' + usd(c.price.median)) + ', ' + band(c.price) + (c.price.rough ? ' (rough)' : ''));
    row('Pushes', c.what_they_push || NA);
    row('Active ads', c.active_ads == null ? NA : fmt.num(c.active_ads));
    row('Longest run', c.longest_days == null ? NA : c.longest_days + ' days, since ' + fmt.date(c.longest_start));
    row('Claims', 'durability ' + c.durability + ' of 3, comfort ' + c.comfort + ' of 3');
    card.append(dl);
    if (c.gap_to_own && c.gap_to_own.length) card.append(el('div', { class: 'gap-own', text: 'Gap to own: ' + c.gap_to_own.join(', ') + '. They show none of it.' }));
    card.append(el('div', { class: 'muted small', text: 'Captured ' + (c.captured_at === 'undated' ? 'undated' : fmt.date(c.captured_at)) + (c.expired ? ', past its refresh date' : '') + '. Run length is a signal, not proof.' }));
    return card;
  }

  function drawMap(pos, axis) {
    const spec = pos.axes[axis];
    const q = pos.quadrants[axis];
    const W = 640, H = 380, pad = { l: 52, r: 20, t: 18, b: 44 };
    const iw = W - pad.l - pad.r, ih = H - pad.t - pad.b;
    const xs = pos.points.flatMap((p) => [p.x, p.high, p.low]).filter((v) => v != null);
    const xmax = Math.ceil(Math.max(...xs, 1) * 1.1 / 5) * 5;
    const ylo = -0.4, yhi = spec.max + 0.4;
    const X = (v) => pad.l + (v / xmax) * iw;
    const Y = (v) => pad.t + ih - ((v - ylo) / (yhi - ylo)) * ih;
    const s = svg('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': 'Positioning map: price per pair against ' + spec.label.toLowerCase() });
    if (pos.split_x != null) {
      const sx = X(pos.split_x), sy = Y(q.split_y);
      const rects = { 'false,true': [pad.l, pad.t, sx - pad.l, sy - pad.t], 'false,false': [pad.l, sy, sx - pad.l, pad.t + ih - sy],
        'true,true': [sx, pad.t, pad.l + iw - sx, sy - pad.t], 'true,false': [sx, sy, pad.l + iw - sx, pad.t + ih - sy] };
      for (const quad of q.quadrants) {
        const r = rects[quad.x_high + ',' + quad.y_high];
        if (!quad.competitors.length) s.append(svg('rect', { x: r[0], y: r[1], width: r[2], height: r[3], class: 'open' }));
        s.append(svg('text', { x: r[0] + 6, y: quad.y_high ? r[1] + 13 : r[1] + r[3] - 6, class: 'ql' }, quad.label + (quad.competitors.length ? '' : ' (open)')));
      }
    }
    for (let v = 0; v <= xmax; v += 5) {
      s.append(svg('line', { x1: X(v), x2: X(v), y1: pad.t, y2: pad.t + ih, class: 'grid-l' }));
      s.append(svg('text', { x: X(v), y: pad.t + ih + 16, 'text-anchor': 'middle' }, '$' + v));
    }
    for (let v = 0; v <= spec.max; v++) {
      s.append(svg('line', { x1: pad.l, x2: pad.l + iw, y1: Y(v), y2: Y(v), class: 'grid-l' }));
      s.append(svg('text', { x: pad.l - 8, y: Y(v) + 4, 'text-anchor': 'end' }, String(v)));
    }
    s.append(svg('line', { x1: pad.l, x2: pad.l + iw, y1: pad.t + ih, y2: pad.t + ih, class: 'axis' }));
    s.append(svg('line', { x1: pad.l, x2: pad.l, y1: pad.t, y2: pad.t + ih, class: 'axis' }));
    if (pos.split_x != null) {
      s.append(svg('line', { x1: X(pos.split_x), x2: X(pos.split_x), y1: pad.t, y2: pad.t + ih, class: 'split' }));
      s.append(svg('line', { x1: pad.l, x2: pad.l + iw, y1: Y(q.split_y), y2: Y(q.split_y), class: 'split' }));
    }
    s.append(svg('text', { x: pad.l + iw / 2, y: H - 6, 'text-anchor': 'middle' }, 'Median price per pair, US dollars (line: public price band)'));
    s.append(svg('text', { x: 14, y: pad.t + ih / 2, 'text-anchor': 'middle', transform: 'rotate(-90 14 ' + (pad.t + ih / 2) + ')' }, spec.label + ', 0 to ' + spec.max));
    const seen = {};
    for (const p of pos.points) {
      if (p.x == null) continue;
      const y = p[axis];
      const key = p.x + ',' + y;
      const nth = seen[key] = (seen[key] || 0) + 1;
      const cls = p.brand ? ' brand' : '';
      if (p.low != null && p.high != null) s.append(svg('line', { x1: X(p.low), x2: X(p.high), y1: Y(y), y2: Y(y), class: 'band' + cls }));
      const dot = svg('circle', { cx: X(p.x), cy: Y(y), r: p.brand ? 7 : 6, class: 'dot' + cls + (p.rough && !p.brand ? ' rough' : '') });
      dot.append(svg('title', null, p.name + ': ' + usd(p.x) + ' a pair, ' + spec.label.toLowerCase() + ' ' + y + (p.simulated ? ' (simulated price)' : '') + (p.rough ? ' (rough price)' : '')));
      s.append(dot);
      const ly = p.brand ? Y(y) + 22 : Y(y) - 8 - (nth - 1) * 14;
      s.append(svg('text', { x: p.brand ? X(p.x) - 8 : X(p.x) + 10, y: ly, class: 'pt' }, p.name + (p.brand ? ' (simulated price)' : '')));
    }
    return s;
  }

  function mapCard(pos) {
    let axis = 'durability';
    const box = el('div', { class: 'map-wrap' });
    const note = el('p', { class: 'muted small' });
    const tabs = el('div', { class: 'map-tabs', role: 'tablist' });
    const render = () => {
      box.replaceChildren(drawMap(pos, axis));
      const q = pos.quadrants[axis];
      note.textContent = pos.axes[axis].plain + '. Split lines: the tracked median price (' + usd(pos.split_x) + ') and the middle of the claim scale. Open quadrants: ' + (q.openness || NA) + '. Hollow dots are rough price reads.';
      for (const b of tabs.children) b.classList.toggle('sel', b.dataset.axis === axis);
    };
    for (const k of Object.keys(pos.axes)) {
      const b = el('button', { class: 'btn sm', type: 'button', text: 'Price vs ' + pos.axes[k].label.toLowerCase(), dataset: { axis: k } });
      b.addEventListener('click', () => { axis = k; render(); });
      tabs.append(b);
    }
    render();
    return [tabs, box, note];
  }

  function priceTable(pr) {
    if (!pr.available) return [el('p', { class: 'muted', text: 'Brand prices unavailable: ' + (pr.reason || 'no sales table') + '.' })];
    const cols = [
      { key: 'label', label: 'Brand pack' },
      { key: 'per_pack', label: 'Per pack', align: 'right', format: usd },
      { key: 'per_pair', label: 'Per pair', align: 'right', format: usd },
    ];
    for (const c of pr.competitors) {
      cols.push({ key: 'c_' + c.name, label: c.name + ' (' + usd(c.median) + ')', align: 'right',
        format: (v) => v ? (v.diff > 0 ? '+' : '') + usd(v.diff).replace('$-', '-$') + ' ' + v.position.replace(' median', '') : NA });
    }
    const rows = pr.rows.map((r) => {
      const o = { label: r.label, per_pack: r.per_pack, per_pair: r.per_pair };
      for (const c of pr.competitors) o['c_' + c.name] = r.cells[c.name];
      return o;
    });
    const bands = el('ul', { class: 'small muted' }, ...pr.competitors.map((c) => el('li', null, c.name + ': ' + c.band + '. ',
      c.ref ? el('a', { href: c.ref, target: '_blank', rel: 'noopener', text: 'source' }) : null)));
    return [el('p', { class: 'muted small', text: 'Brand price per pack is simulated net sales per unit sold in ' + pr.month + ', after discounts. Each cell is the brand price per pair minus the competitor median (in brackets), then below, inside or above their public band, or below or above the median when only a median is public.' }),
      UI.table({ columns: cols, rows, sort: { key: 'per_pair', dir: 'asc' } }), el('b', { class: 'small', text: 'Public price bands' }), bands];
  }

  function boardCard(b) {
    return el('article', { class: 'card' + (b.brand ? ' brand' : '') },
      el('div', { class: 'row' }, el('b', { text: b.name }), b.brand ? el('span', { class: 'chip accent', text: 'your brand' }) : null,
        el('span', { class: 'muted small', text: (b.active_ads == null ? NA : b.active_ads) + ' active ads' })),
      el('div', { class: 'muted small', text: 'Formats' }), chips(b.formats),
      el('div', { class: 'muted small', text: 'Hook types' }), chips(b.hooks, 'accent'));
  }

  function lookalikeBox(lk) {
    if (!lk) return [];
    return [el('div', { class: 'warnbox', role: 'alert' },
      el('b', { text: 'Lookalike page warning' }),
      el('div', { text: 'A ' + pretty(lk.verdict) + ' page (id ' + lk.page_id + ') ran ' + lk.ads_seen + ' ads on ' + fmt.date(lk.created) + ' that link to ' + lk.links_to + '. It is not the brand. Its ads are left out of every count on this page.' }),
      lk.ref ? el('a', { href: lk.ref, target: '_blank', rel: 'noopener', class: 'small', text: 'See it in the Ad Library' }) : null,
      UI.decisionRow({ capability: 'MONEY-C48', autonomy: 'human_assist', screen: SCREEN }))];
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

  async function load() {
    let d;
    try { d = await api(BASE + 'overview'); } catch (e) { mount('#badge', 'Could not load: ' + e.message); return; }
    mount('#badge', el('span', null, el('b', { text: 'Simulated data and public signals. ' }), d.simulated_note + ' Brain version ' + d.version + '.'));
    document.getElementById('signal-note').textContent = d.signal_note;
    mount('#lookalike', ...lookalikeBox(d.lookalike));
    mount('#tiles', ...d.tiles.map((t) => UI.tile(Object.assign({}, t, { freshness: d.today }))));
    mount('#insights', ...(d.insights.length ? d.insights.map((i) => UI.insight(Object.assign({ screen: SCREEN }, i)))
      : [el('p', { class: 'muted', text: 'No rule fired on this capture.' })]));
    mount('#cards', ...d.competitors.map(compCard));
    mount('#map', ...mapCard(d.positioning));
    mount('#prices', ...priceTable(d.prices));
    mount('#board', ...d.board.map(boardCard));
    const ch = d.chart;
    mount('#chart', Charts.bar({ labels: ch.labels, series: [{ name: 'active ads', values: ch.values }], unit: 'n', values: true,
      title: 'Active Meta ads seen per brand, latest capture',
      note: 'Public signal from the Ad Library. The last bar is the brand. More ads means more testing, not better results.' }));
    mount('#actions', ...d.actions.map((a) => el('article', { class: 'card' }, el('b', { text: a.label }),
      UI.decisionRow({ capability: a.capability, autonomy: a.autonomy, screen: SCREEN }))));
    try {
      const a = await api(BASE + 'audit');
      mount('#audit', el('p', { class: 'muted small', text: a.findings.length + ' findings from ' + a.rules.length + ' rules. Public signals, one capture.' }), auditTable(a.findings));
    } catch (e) { mount('#audit', el('p', { class: 'muted', text: 'Audit unavailable: ' + e.message })); }
  }

  load();
})();
