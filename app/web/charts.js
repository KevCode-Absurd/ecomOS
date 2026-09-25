/* ecomOS charts. One global, `Charts`. Plain SVG drawn to scale from plain arrays, theme-aware
   through the CSS tokens in ui-kit.css. Every function returns a DOM element (.chart).

   Charts.bar({ labels, series: [{name, values}], benchmark, unit, title, note, stacked })
   Charts.line({ labels, series: [{name, values}], benchmark, unit, title, note })
   Charts.step({ labels, series, benchmark, unit, title, note })        line with step interpolation
   Charts.funnel({ stages: [{label, value, rate}], breakAt, unit, title, note })
   Charts.cohort({ rows: [{label, values: [..]}], columns, unit, title, note })

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
      svg.append(svgEl('path', { d, fill: 'none', stroke: s.color, 'stroke-width': 2.2, 'stroke-linejoin': 'round', 'stroke-linecap': 'round' }));
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

  window.Charts = { bar, line: (p) => line(p, false), step: (p) => line(p, true), funnel, cohort, COLORS };
})();
