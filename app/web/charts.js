/* ecomOS charts. One global, `Charts`. Plain SVG drawn to scale from plain arrays, theme-aware
   through the CSS tokens in ui-kit.css. Every function returns a DOM element (.chart).

   Charts.bar({ labels, series: [{name, values}], benchmark, unit, title, note, stacked })
   Charts.line({ labels, series: [{name, values}], benchmark, unit, title, note })
   Charts.step({ labels, series, benchmark, unit, title, note })        line with step interpolation
   Charts.funnel({ stages: [{label, value, rate}], breakAt, unit, title, note })
   Charts.cohort({ rows: [{label, values: [..]}], columns, unit, title, note })
   v2 (depth contract, 28 Sep 2026):
   Charts.positioningMap({ x: {label, min, max}, y: {label, min, max}, points: [{label, x, y, us, size, gap}], quadrants: [tl, tr, bl, br], title, note })
   Charts.trendStrip({ rows: [{label, sub, values, unit, higher_is_better, band: [lo, hi]}], title, note })
   Charts.waterfall({ steps: [{label, value, kind: 'total'|'up'|'down'|'sub'}], unit, title, note })
   bar and line take shade: [i0, i1] to shade a window of x positions (the selected dates).

   null in a values array means unavailable: the bar is hatched, the line breaks. Series colours
   come from --s1..--s6. Units: '$', '%', 'x', 'ms', 'n' (see UI.fmt.unit). */
(function () {
  'use strict';
  const NS = 'http://www.w3.org/2000/svg';
  const isNum = (v) => typeof v === 'number' && Number.isFinite(v);
  const fmtv = (v, unit) => (window.UI ? UI.fmt.unit(v, unit) : String(v));
  const COLORS = ['var(--s1)', 'var(--s2)', 'var(--s3)', 'var(--s4)', 'var(--s5)', 'var(--s6)'];

  function svgEl(tag, attrs, ...children) {
    const node = document.createElementNS(NS, tag);
    if (attrs) for (const [k, v] of Object.entries(attrs)) if (v != null && v !== false) node.setAttribute(k, v);
    for (const c of children.flat(Infinity)) if (c != null) node.append(c instanceof Node ? c : document.createTextNode(String(c)));
    return node;
  }
  function wrap(p, svg, series) {
    const node = document.createElement('div');
    node.className = 'chart';
    if (p.title) { const t = document.createElement('div'); t.className = 'title'; t.textContent = p.title; node.append(t); }
    node.append(svg);
    if (series && series.length > 1) {
      const lg = document.createElement('div'); lg.className = 'legend';
      series.forEach((s, i) => { const item = document.createElement('span'); const dot = document.createElement('i'); dot.style.background = s.color || COLORS[i % COLORS.length]; item.append(dot, s.name || ('series ' + (i + 1))); lg.append(item); });
      node.append(lg);
    }
    if (p.note) { const n = document.createElement('div'); n.className = 'note'; n.textContent = p.note; node.append(n); }
    return node;
  }
  function hatchDefs() {
    const pat = svgEl('pattern', { id: 'kit-hatch', width: 6, height: 6, patternUnits: 'userSpaceOnUse', patternTransform: 'rotate(45)' });
    pat.append(svgEl('line', { x1: 0, y1: 0, x2: 0, y2: 6, stroke: 'var(--line-strong)', 'stroke-width': 2 }));
    return svgEl('defs', null, pat);
  }
  function niceMax(v) {
    if (!(v > 0)) return 1;
    const p = Math.pow(10, Math.floor(Math.log10(v)));
    const n = v / p;
    const m = n <= 1 ? 1 : n <= 2 ? 2 : n <= 2.5 ? 2.5 : n <= 5 ? 5 : 10;
    return m * p;
  }
  function ticks(max, count) {
    const out = [];
    for (let i = 0; i <= count; i++) out.push((max * i) / count);
    return out;
  }
  function tickLabel(v, unit) {
    if (unit === '%') return (v * 100).toFixed(v * 100 < 10 && v > 0 ? 1 : 0) + '%';
    if (unit === '$' || unit === 'money' || unit === 'usd') return '$' + (window.UI ? UI.fmt.compact(v) : v);
    if (unit === 'x' || unit === 'ratio') return v.toFixed(1) + 'x';
    if (unit === 'ms') return v >= 1000 ? (v / 1000).toFixed(1) + 's' : Math.round(v) + 'ms';
    return window.UI ? UI.fmt.compact(v) : String(v);
  }
  function frame(p, W, H, pad, max, unit) {
    const svg = svgEl('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': p.title || p.aria || 'chart' });
    svg.append(hatchDefs());
    const g = svgEl('g', { class: 'grid' });
    const ax = svgEl('g', { class: 'axis' });
    const innerH = H - pad.t - pad.b, innerW = W - pad.l - pad.r;
    for (const t of ticks(max, 4)) {
      const y = pad.t + innerH - (t / max) * innerH;
      g.append(svgEl('line', { x1: pad.l, x2: pad.l + innerW, y1: y, y2: y }));
      ax.append(svgEl('text', { x: pad.l - 6, y: y + 4, 'text-anchor': 'end' }, tickLabel(t, unit)));
    }
    svg.append(g, ax);
    return { svg, innerH, innerW, y: (v) => pad.t + innerH - (v / max) * innerH };
  }
  function benchLine(svg, y, x1, x2, label) {
    const g = svgEl('g', { class: 'bench' });
    g.append(svgEl('line', { x1, x2, y1: y, y2: y }));
    g.append(svgEl('text', { x: x2, y: y - 4, 'text-anchor': 'end' }, label));
    svg.append(g);
  }
  function xLabels(svg, labels, xAt, y, maxLabels) {
    const g = svgEl('g', { class: 'axis' });
    const n = labels.length, every = Math.max(1, Math.ceil(n / (maxLabels || 8)));
    labels.forEach((l, i) => { if (i % every === 0 || i === n - 1) g.append(svgEl('text', { x: xAt(i), y, 'text-anchor': 'middle' }, String(l))); });
    svg.append(g);
  }
  function seriesMax(series, stacked) {
    let m = 0;
    if (stacked) {
      const n = Math.max(...series.map((s) => s.values.length));
      for (let i = 0; i < n; i++) m = Math.max(m, series.reduce((a, s) => a + (isNum(s.values[i]) ? s.values[i] : 0), 0));
    } else for (const s of series) for (const v of s.values) if (isNum(v)) m = Math.max(m, v);
    return m;
  }

  /** bar: grouped (default) or stacked bars per label. */
  function bar(p) {
    const series = (p.series || []).map((s, i) => Object.assign({ color: COLORS[i % COLORS.length] }, s));
    const labels = p.labels || [];
    const W = p.width || 640, H = p.height || 260, pad = { t: 16, r: 12, b: 28, l: 48 };
    const max = niceMax(Math.max(seriesMax(series, p.stacked), isNum(p.benchmark) ? p.benchmark : 0) * 1.05 || 1);
    const { svg, innerW, y } = frame(p, W, H, pad, max, p.unit);
    const n = labels.length || Math.max(...series.map((s) => s.values.length));
    const slot = innerW / Math.max(n, 1), gap = Math.min(10, slot * 0.2);
    if (p.shade && p.shade.length === 2) svg.insertBefore(svgEl('rect', { class: 'shade', x: pad.l + p.shade[0] * slot, y: pad.t, width: (p.shade[1] - p.shade[0] + 1) * slot, height: H - pad.t - pad.b }), svg.children[1]);
    const bw = p.stacked ? slot - gap : (slot - gap) / Math.max(series.length, 1);
    const base = y(0);
    for (let i = 0; i < n; i++) {
      let stackTop = 0;
      series.forEach((s, si) => {
        const v = s.values[i];
        const x = pad.l + i * slot + gap / 2 + (p.stacked ? 0 : si * bw);
        if (!isNum(v)) {
          svg.append(svgEl('rect', { x, y: base - 22, width: Math.max(bw, 1), height: 22, class: 'hatch', rx: 2 }, svgEl('title', null, (s.name ? s.name + ': ' : '') + 'unavailable')));
          if (!p.stacked && series.length === 1) svg.append(svgEl('text', { x: x + bw / 2, y: base - 26, 'text-anchor': 'middle', class: 'na-mark' }, 'n/a'));
          return;
        }
        const top = p.stacked ? y(stackTop + v) : y(v);
        const h = (p.stacked ? y(stackTop) : base) - top;
        svg.append(svgEl('rect', { x, y: top, width: Math.max(bw, 1), height: Math.max(h, 0), fill: s.color, rx: 2 }, svgEl('title', null, (s.name ? s.name + ': ' : '') + fmtv(v, p.unit) + (labels[i] != null ? ' (' + labels[i] + ')' : ''))));
        if (p.values && !p.stacked && series.length === 1) svg.append(svgEl('text', { x: x + bw / 2, y: top - 4, 'text-anchor': 'middle', class: 'val' }, fmtv(v, p.unit)));
        stackTop += v;
      });
    }
    if (isNum(p.benchmark)) benchLine(svg, y(p.benchmark), pad.l, pad.l + innerW, (p.benchmark_label || 'benchmark') + ' ' + fmtv(p.benchmark, p.unit));
    xLabels(svg, labels, (i) => pad.l + i * slot + slot / 2, H - 8, p.maxLabels);
    return wrap(p, svg, series);
  }

  /** line: one polyline per series, gaps where a value is null. step=true draws a step line. */
  function line(p, step) {
    const series = (p.series || []).map((s, i) => Object.assign({ color: COLORS[i % COLORS.length] }, s));
    const labels = p.labels || [];
    const W = p.width || 640, H = p.height || 240, pad = { t: 16, r: 12, b: 28, l: 48 };
    const max = niceMax(Math.max(seriesMax(series), isNum(p.benchmark) ? p.benchmark : 0) * 1.05 || 1);
    const { svg, innerW, y } = frame(p, W, H, pad, max, p.unit);
    const n = labels.length || Math.max(...series.map((s) => s.values.length));
    const xAt = (i) => (n <= 1 ? pad.l + innerW / 2 : pad.l + (i / (n - 1)) * innerW);
    if (p.shade && p.shade.length === 2) svg.insertBefore(svgEl('rect', { class: 'shade', x: xAt(p.shade[0]), y: pad.t, width: Math.max(2, xAt(p.shade[1]) - xAt(p.shade[0])), height: H - pad.t - pad.b }), svg.children[1]);
    series.forEach((s) => {
      let d = '', prev = null;
      s.values.forEach((v, i) => {
        if (!isNum(v)) { prev = null; return; }
        const x = xAt(i), yy = y(v);
        if (prev == null) d += 'M' + x.toFixed(1) + ' ' + yy.toFixed(1);
        else if (step) d += ' H' + x.toFixed(1) + ' V' + yy.toFixed(1);
        else d += ' L' + x.toFixed(1) + ' ' + yy.toFixed(1);
        prev = v;
      });
      svg.append(svgEl('path', { d, fill: 'none', stroke: s.color, 'stroke-width': 2, 'stroke-linejoin': 'round', 'stroke-linecap': 'round' }));
      s.values.forEach((v, i) => {
        if (!isNum(v)) { svg.append(svgEl('text', { x: xAt(i), y: y(0) - 6, 'text-anchor': 'middle', class: 'na-mark' }, n <= 16 ? 'n/a' : '')); return; }
        const dot = svgEl('circle', { cx: xAt(i), cy: y(v), r: n > 40 ? 1.5 : 3, fill: s.color });
        dot.append(svgEl('title', null, (s.name ? s.name + ': ' : '') + fmtv(v, p.unit) + (labels[i] != null ? ' (' + labels[i] + ')' : '')));
        svg.append(dot);
      });
      if (p.values && series.length === 1) s.values.forEach((v, i) => { if (isNum(v) && (n <= 14 || i === n - 1)) svg.append(svgEl('text', { x: xAt(i), y: y(v) - 8, 'text-anchor': 'middle', class: 'val' }, fmtv(v, p.unit))); });
    });
    if (isNum(p.benchmark)) benchLine(svg, y(p.benchmark), pad.l, pad.l + innerW, (p.benchmark_label || 'benchmark') + ' ' + fmtv(p.benchmark, p.unit));
    xLabels(svg, labels, xAt, H - 8, p.maxLabels);
    return wrap(p, svg, series);
  }

  /** funnel: stages in order, each a count. Width to scale of the first stage. breakAt marks the stage index where the drop is worst. */
  function funnel(p) {
    const stages = p.stages || [];
    const W = p.width || 640, rowH = 42, gapH = 18, padL = 8, labelW = Math.min(200, W * 0.32);
    const H = stages.length * (rowH + gapH) + 8;
    const svg = svgEl('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': p.title || 'funnel', class: 'funnel' });
    svg.append(hatchDefs());
    const first = stages.find((s) => isNum(s.value));
    const max = first ? first.value : 1;
    const barW = W - labelW - padL - 8;
    let breakAt = p.breakAt;
    if (breakAt == null) {   // the worst stage-to-stage drop, by rate if given, else by ratio of counts
      let worst = null;
      for (let i = 1; i < stages.length; i++) {
        const r = isNum(stages[i].rate) ? stages[i].rate : (isNum(stages[i].value) && isNum(stages[i - 1].value) && stages[i - 1].value > 0 ? stages[i].value / stages[i - 1].value : null);
        const bench = isNum(stages[i].benchmark) ? stages[i].benchmark : null;
        const score = r == null ? null : bench != null ? r / bench : r;
        if (score != null && (worst == null || score < worst.score)) worst = { i, score };
      }
      breakAt = worst ? worst.i : null;
    }
    stages.forEach((s, i) => {
      const y = 4 + i * (rowH + gapH);
      const g = svgEl('g', { class: 'stage' + (i === breakAt ? ' break' : ''), transform: 'translate(0 ' + y + ')' });
      g.append(svgEl('text', { x: padL, y: rowH / 2 - 2, class: 'l' }, s.label || ('stage ' + (i + 1))));
      g.append(svgEl('text', { x: padL, y: rowH / 2 + 14, class: 'n' }, isNum(s.value) ? fmtv(s.value, p.unit || 'n') : 'unavailable'));
      if (isNum(s.value)) {
        const w = Math.max(2, (s.value / max) * barW);
        g.append(svgEl('rect', { x: labelW, y: 4, width: w, height: rowH - 8, fill: i === breakAt ? 'var(--bad-soft)' : 'var(--s1)', rx: 4 }, svgEl('title', null, (s.label || '') + ': ' + fmtv(s.value, p.unit || 'n'))));
      } else {
        g.append(svgEl('rect', { x: labelW, y: 4, width: barW * 0.3, height: rowH - 8, class: 'hatch', rx: 4 }));
      }
      if (i > 0) {
        const r = isNum(s.rate) ? s.rate : (isNum(s.value) && isNum(stages[i - 1].value) && stages[i - 1].value > 0 ? s.value / stages[i - 1].value : null);
        const txt = (r == null ? 'rate unavailable' : (r * 100).toFixed(1) + '% of ' + (stages[i - 1].label || 'previous')) + (isNum(s.benchmark) ? ', benchmark ' + (s.benchmark * 100).toFixed(1) + '%' : '') + (i === breakAt ? '. Break here' : '');
        g.append(svgEl('text', { x: labelW, y: -5, class: 'rate' }, txt));
      }
      svg.append(g);
    });
    return wrap(p, svg, null);
  }

  /** cohort: rows [{label, values}], columns ['m0','m1',...]. Cells are ratios or numbers; colour by value across the grid. */
  function cohort(p) {
    const rows = p.rows || [], cols = p.columns || [];
    const cellW = p.cellW || 58, cellH = 30, labelW = p.labelW || 92, headH = 24;
    const W = labelW + cols.length * cellW + 4, H = headH + rows.length * cellH + 4;
    const svg = svgEl('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': p.title || 'cohort grid', class: 'cohort', style: 'max-width:' + W + 'px' });
    svg.append(hatchDefs());
    let max = 0;
    for (const r of rows) for (const v of r.values) if (isNum(v)) max = Math.max(max, v);
    cols.forEach((c, j) => svg.append(svgEl('text', { x: labelW + j * cellW + cellW / 2, y: 16, 'text-anchor': 'middle', class: 'head' }, String(c))));
    rows.forEach((r, i) => {
      const y = headH + i * cellH;
      svg.append(svgEl('text', { x: labelW - 8, y: y + cellH / 2 + 4, 'text-anchor': 'end' }, String(r.label)));
      cols.forEach((c, j) => {
        const v = r.values[j], x = labelW + j * cellW;
        if (!isNum(v)) { svg.append(svgEl('rect', { x: x + 1, y: y + 1, width: cellW - 2, height: cellH - 2, fill: 'var(--sunken)', rx: 3 }, svgEl('title', null, 'unavailable'))); return; }
        const t = max > 0 ? v / max : 0;
        svg.append(svgEl('rect', { x: x + 1, y: y + 1, width: cellW - 2, height: cellH - 2, fill: 'color-mix(in srgb, var(--cohort-hi) ' + Math.round(t * 100) + '%, var(--cohort-lo))', rx: 3 }, svgEl('title', null, r.label + ' ' + c + ': ' + fmtv(v, p.unit))));
        svg.append(svgEl('text', { x: x + cellW / 2, y: y + cellH / 2 + 4, 'text-anchor': 'middle', class: t > 0.55 ? 'dark' : '' }, fmtv(v, p.unit)));
      });
    });
    const node = wrap(p, svg, null);
    node.style.overflowX = 'auto';
    return node;
  }

  /** positioningMap: two axes from the brain, points for us and them, empty quadrants named as gaps.
      p.points: [{label, x, y, us (bool), size, gap (bool), note}]; p.x / p.y: {label, min, max, lo, hi} where lo and hi
      are the words at each end ("Value" to "Premium"); p.quadrants: 4 labels [top-left, top-right, bottom-left, bottom-right]. */
  function positioningMap(p) {
    const W = p.width || 640, H = p.height || 420, pad = { t: 22, r: 22, b: 40, l: 44 };
    const pts = p.points || [];
    const ax = Object.assign({ min: 0, max: 1 }, p.x || {}), ay = Object.assign({ min: 0, max: 1 }, p.y || {});
    const xs = pts.map((q) => q.x).filter(isNum), ys = pts.map((q) => q.y).filter(isNum);
    if (p.x && p.x.min == null && xs.length) { ax.min = Math.min(...xs); ax.max = Math.max(...xs); }
    if (p.y && p.y.min == null && ys.length) { ay.min = Math.min(...ys); ay.max = Math.max(...ys); }
    const padX = (ax.max - ax.min) * 0.08 || 0.1, padY = (ay.max - ay.min) * 0.08 || 0.1;
    ax.min -= padX; ax.max += padX; ay.min -= padY; ay.max += padY;
    const innerW = W - pad.l - pad.r, innerH = H - pad.t - pad.b;
    const X = (v) => pad.l + ((v - ax.min) / (ax.max - ax.min)) * innerW;
    const Y = (v) => pad.t + innerH - ((v - ay.min) / (ay.max - ay.min)) * innerH;
    const svg = svgEl('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': p.title || 'positioning map', class: 'pmap' });
    svg.append(svgEl('rect', { x: pad.l, y: pad.t, width: innerW, height: innerH, fill: 'var(--sunken)', rx: 8 }));
    const midX = isNum(p.midX) ? X(p.midX) : pad.l + innerW / 2, midY = isNum(p.midY) ? Y(p.midY) : pad.t + innerH / 2;
    const q = svgEl('g', { class: 'quad' });
    q.append(svgEl('line', { x1: midX, x2: midX, y1: pad.t, y2: pad.t + innerH }), svgEl('line', { x1: pad.l, x2: pad.l + innerW, y1: midY, y2: midY }));
    const ql = p.quadrants || [];
    const qpos = [[pad.l + 8, pad.t + 14, 'start'], [pad.l + innerW - 8, pad.t + 14, 'end'], [pad.l + 8, pad.t + innerH - 6, 'start'], [pad.l + innerW - 8, pad.t + innerH - 6, 'end']];
    ql.forEach((t, i) => { if (t) q.append(svgEl('text', { x: qpos[i][0], y: qpos[i][1], 'text-anchor': qpos[i][2] }, t)); });
    svg.append(q);
    const axes = svgEl('g', { class: 'axis' });
    axes.append(svgEl('text', { x: pad.l + innerW / 2, y: H - 8, 'text-anchor': 'middle', class: 'axis-name' }, ax.label || 'x'));
    if (ax.lo) axes.append(svgEl('text', { x: pad.l, y: H - 8, 'text-anchor': 'start' }, ax.lo));
    if (ax.hi) axes.append(svgEl('text', { x: pad.l + innerW, y: H - 8, 'text-anchor': 'end' }, ax.hi));
    const yl = svgEl('text', { x: 14, y: pad.t + innerH / 2, 'text-anchor': 'middle', class: 'axis-name', transform: 'rotate(-90 14 ' + (pad.t + innerH / 2) + ')' }, ay.label || 'y');
    axes.append(yl);
    if (ay.lo) axes.append(svgEl('text', { x: pad.l - 4, y: pad.t + innerH, 'text-anchor': 'end' }, ay.lo));
    if (ay.hi) axes.append(svgEl('text', { x: pad.l - 4, y: pad.t + 10, 'text-anchor': 'end' }, ay.hi));
    svg.append(axes);
    const sizes = pts.map((q) => q.size).filter(isNum), maxS = sizes.length ? Math.max(...sizes) : 1;
    pts.slice().sort((a, b) => (a.us ? 1 : 0) - (b.us ? 1 : 0)).forEach((q) => {
      if (!isNum(q.x) || !isNum(q.y)) return;
      const r = isNum(q.size) ? 5 + 11 * Math.sqrt(q.size / maxS) : (q.us ? 9 : 6);
      const g = svgEl('g', { class: 'pt' + (q.us ? ' us' : ' them') + (q.gap ? ' gap' : '') });
      const c = svgEl('circle', { cx: X(q.x), cy: Y(q.y), r, fill: q.gap ? 'none' : q.us ? 'var(--us)' : 'var(--them)', 'fill-opacity': q.us ? 1 : .55, stroke: q.us ? 'var(--surface)' : 'none', 'stroke-width': 2 });
      c.append(svgEl('title', null, q.label + (q.note ? ': ' + q.note : '') + '\n' + (ax.label || 'x') + ' ' + fmtv(q.x, ax.unit) + ', ' + (ay.label || 'y') + ' ' + fmtv(q.y, ay.unit) + (isNum(q.size) ? '\nsize ' + fmtv(q.size, p.sizeUnit) : '')));
      g.append(c);
      g.append(svgEl('text', { x: X(q.x) + r + 4, y: Y(q.y) + 4 }, q.label));
      svg.append(g);
    });
    const node = wrap(p, svg, null);
    const lg = document.createElement('div'); lg.className = 'legend';
    const mk = (col, t) => { const s = document.createElement('span'); const i = document.createElement('i'); i.style.background = col; i.style.borderRadius = '50%'; s.append(i, t); return s; };
    lg.append(mk('var(--us)', p.usLabel || 'us'), mk('var(--them)', p.themLabel || 'them'));
    if (pts.some((q) => q.gap)) { const s = document.createElement('span'); const i = document.createElement('i'); i.style.border = '2px dashed var(--bad)'; i.style.borderRadius = '50%'; i.style.background = 'transparent'; s.append(i, 'gap: no one serves it'); lg.append(s); }
    node.insertBefore(lg, node.querySelector('.note'));
    return node;
  }

  /** trendStrip: rows of sparkline, last value and change. Orientation only.
      rows: [{label, sub, values, unit, higher_is_better, band: [lo, hi], tone}] */
  function trendStrip(p) {
    const node = document.createElement('div'); node.className = 'chart';
    if (p.title) { const t = document.createElement('div'); t.className = 'title'; t.textContent = p.title; node.append(t); }
    const grid = document.createElement('div'); grid.className = 'trend';
    const w = 96, h = 26;
    for (const r of p.rows || []) {
      const vals = (r.values || []);
      const nums = vals.filter(isNum);
      const last = nums.length ? nums[nums.length - 1] : null;
      const first = nums.length > 1 ? nums[0] : null;
      const delta = isNum(last) && isNum(first) && first !== 0 ? (last - first) / Math.abs(first) : null;
      const dir = delta == null ? null : delta > 0.0005 ? 'up' : delta < -0.0005 ? 'down' : 'flat';
      const good = dir == null || dir === 'flat' ? null : (r.higher_is_better === false ? dir === 'down' : dir === 'up');
      const tone = r.tone || (good == null ? '' : good ? 'good' : 'bad');
      const lab = document.createElement('div'); lab.className = 't-label'; lab.textContent = r.label || '';
      if (r.sub) { const s = document.createElement('small'); s.textContent = r.sub; lab.append(s); }
      const sp = document.createElement('div'); sp.className = 't-spark ' + tone;
      const svg = svgEl('svg', { viewBox: '0 0 ' + w + ' ' + h, role: 'img', 'aria-label': (r.label || '') + ' trend' });
      if (nums.length) {
        let lo = Math.min(...nums), hi = Math.max(...nums);
        if (r.band) { lo = Math.min(lo, r.band[0]); hi = Math.max(hi, r.band[1]); }
        if (hi === lo) { hi += 1; lo -= 1; }
        const n = vals.length, xAt = (i) => (n <= 1 ? w / 2 : 2 + (i / (n - 1)) * (w - 4)), yAt = (v) => 2 + (h - 4) - ((v - lo) / (hi - lo)) * (h - 4);
        if (r.band) svg.append(svgEl('rect', { class: 'band', x: 0, y: yAt(r.band[1]), width: w, height: Math.max(1, yAt(r.band[0]) - yAt(r.band[1])) }));
        let d = '', prev = null;
        vals.forEach((v, i) => { if (!isNum(v)) { prev = null; return; } d += (prev == null ? 'M' : 'L') + xAt(i).toFixed(1) + ' ' + yAt(v).toFixed(1); prev = v; });
        svg.append(svgEl('path', { d }));
        const li = vals.length - 1 - vals.slice().reverse().findIndex(isNum);
        svg.append(svgEl('circle', { class: 'last', cx: xAt(li), cy: yAt(last), r: 2.5 }));
      }
      sp.append(svg);
      const val = document.createElement('div'); val.className = 't-val' + (isNum(last) ? '' : ' na');
      val.textContent = isNum(last) ? fmtv(last, r.unit) : 'unavailable';
      if (delta != null) { const dd = document.createElement('span'); dd.className = 'd ' + (good == null ? '' : good ? 'up' : 'down'); dd.textContent = (delta > 0 ? '+' : '') + (delta * 100).toFixed(Math.abs(delta) < 0.1 ? 1 : 0) + '% ' + (r.delta_label || 'over the window'); val.append(dd); }
      grid.append(lab, sp, val);
    }
    node.append(grid);
    if (p.note) { const nn = document.createElement('div'); nn.className = 'note'; nn.textContent = p.note; node.append(nn); }
    return node;
  }

  /** waterfall: a total decomposed into steps. steps: [{label, value, kind}] where kind is total (absolute), up, down or sub (a subtotal). */
  function waterfall(p) {
    const steps = p.steps || [];
    const W = p.width || 640, H = p.height || 280, pad = { t: 18, r: 12, b: 44, l: 52 };
    let run = 0, lo = 0, hi = 0;
    const bars = steps.map((s) => {
      let start, end;
      if (s.kind === 'total' || s.kind === 'sub') { start = 0; end = s.kind === 'total' ? (isNum(s.value) ? s.value : run) : run; if (s.kind === 'total' && isNum(s.value)) run = s.value; }
      else { start = run; end = run + (isNum(s.value) ? (s.kind === 'down' ? -Math.abs(s.value) : s.value) : 0); run = end; }
      lo = Math.min(lo, start, end); hi = Math.max(hi, start, end);
      return { s, start, end };
    });
    const range = (hi - lo) || 1;
    const innerW = W - pad.l - pad.r, innerH = H - pad.t - pad.b;
    const y = (v) => pad.t + innerH - ((v - lo) / range) * innerH;
    const svg = svgEl('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': p.title || 'waterfall', class: 'wf' });
    svg.append(hatchDefs());
    const g = svgEl('g', { class: 'grid' }), ax = svgEl('g', { class: 'axis' });
    for (const t of ticks(hi - lo, 4)) { const v = lo + t; g.append(svgEl('line', { x1: pad.l, x2: pad.l + innerW, y1: y(v), y2: y(v) })); ax.append(svgEl('text', { x: pad.l - 6, y: y(v) + 4, 'text-anchor': 'end' }, tickLabel(v, p.unit))); }
    svg.append(g, ax);
    const slot = innerW / Math.max(bars.length, 1), bw = Math.min(64, slot * 0.66);
    bars.forEach((b, i) => {
      const x = pad.l + i * slot + (slot - bw) / 2;
      const top = Math.min(y(b.start), y(b.end)), hgt = Math.max(2, Math.abs(y(b.start) - y(b.end)));
      const kind = b.s.kind === 'total' ? 'total' : b.s.kind === 'sub' ? 'sub' : (b.end >= b.start ? 'up' : 'down');
      if (!isNum(b.s.value) && b.s.kind !== 'sub') svg.append(svgEl('rect', { x, y: y(b.start) - 20, width: bw, height: 20, class: 'hatch', rx: 3 }, svgEl('title', null, b.s.label + ': unavailable')));
      else svg.append(svgEl('rect', { x, y: top, width: bw, height: hgt, class: kind, rx: 3 }, svgEl('title', null, b.s.label + ': ' + fmtv(b.end - b.start, p.unit) + (b.s.kind === 'total' || b.s.kind === 'sub' ? '' : ' (running ' + fmtv(b.end, p.unit) + ')'))));
      svg.append(svgEl('text', { x: x + bw / 2, y: top - 5, 'text-anchor': 'middle' }, isNum(b.s.value) || b.s.kind === 'sub' ? fmtv(b.s.kind === 'sub' ? b.end : (b.s.kind === 'total' ? b.end : (kind === 'down' ? -Math.abs(b.s.value) : b.s.value)), p.unit) : 'n/a'));
      if (i < bars.length - 1) svg.append(svgEl('line', { class: 'connector', x1: x + bw, x2: pad.l + (i + 1) * slot + (slot - bw) / 2, y1: y(b.end), y2: y(b.end) }));
      const lab = String(b.s.label || '');
      svg.append(svgEl('text', { x: x + bw / 2, y: H - 26, 'text-anchor': 'middle' }, lab.length > 14 ? lab.slice(0, 13) + '.' : lab));
      if (b.s.sub) svg.append(svgEl('text', { x: x + bw / 2, y: H - 12, 'text-anchor': 'middle', style: 'font-size:10px' }, b.s.sub));
    });
    return wrap(p, svg, null);
  }

  window.Charts = { bar, line: (p) => line(p, false), step: (p) => line(p, true), funnel, cohort, positioningMap, trendStrip, waterfall, COLORS };
})();
