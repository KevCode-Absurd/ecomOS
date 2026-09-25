/* ecomOS UI kit. One global, `UI`, no build step.
   Every component returns a DOM element. Screens compose them:
     UI.mount('#tiles', UI.tile({...}), UI.tile({...}))
   Components: tile, insight, decisionRow, table, filmstrip, founderNote, emptyState, sampleBadge.
   Helpers: el, fmt, api, screen, mount, theme. Charts live in charts.js. */
(function () {
  'use strict';

  // ---------- DOM ----------
  function el(tag, attrs, ...children) {
    const node = document.createElement(tag);
    if (attrs) for (const [k, v] of Object.entries(attrs)) {
      if (v == null || v === false) continue;
      if (k === 'class') node.className = v;
      else if (k === 'text') node.textContent = v;
      else if (k === 'html') node.innerHTML = v;
      else if (k.startsWith('on') && typeof v === 'function') node.addEventListener(k.slice(2), v);
      else if (k === 'style' && typeof v === 'object') Object.assign(node.style, v);
      else if (k === 'dataset') Object.assign(node.dataset, v);
      else node.setAttribute(k, v === true ? '' : v);
    }
    append(node, children);
    return node;
  }
  function append(node, children) {
    for (const c of children.flat(Infinity)) {
      if (c == null || c === false) continue;
      node.append(c instanceof Node ? c : document.createTextNode(String(c)));
    }
    return node;
  }
  function mount(target, ...children) {
    const node = typeof target === 'string' ? document.querySelector(target) : target;
    if (!node) return null;
    node.replaceChildren();
    return append(node, children);
  }

  // ---------- formatting ----------
  const NA = 'unavailable';
  const isNum = (v) => typeof v === 'number' && Number.isFinite(v);
  const fmt = {
    na: NA,
    num(v, digits) {
      if (!isNum(v)) return NA;
      if (digits == null) digits = Math.abs(v) >= 100 ? 0 : Math.abs(v) >= 10 ? 1 : 2;
      return v.toLocaleString('en-US', { maximumFractionDigits: digits, minimumFractionDigits: 0 });
    },
    int(v) { return isNum(v) ? Math.round(v).toLocaleString('en-US') : NA; },
    compact(v) {
      if (!isNum(v)) return NA;
      const a = Math.abs(v);
      if (a >= 1e6) return (v / 1e6).toFixed(a >= 1e7 ? 0 : 1) + 'M';
      if (a >= 1e4) return (v / 1e3).toFixed(0) + 'k';
      if (a >= 1e3) return (v / 1e3).toFixed(1) + 'k';
      return fmt.num(v);
    },
    money(v, currency, digits) {
      if (!isNum(v)) return NA;
      const cur = currency || (UI.brand && UI.brand.currency) || 'USD';
      if (digits == null) digits = Math.abs(v) >= 1000 ? 0 : 2;
      try { return v.toLocaleString('en-US', { style: 'currency', currency: cur, maximumFractionDigits: digits, minimumFractionDigits: digits }); }
      catch (e) { return cur + ' ' + fmt.num(v, digits); }
    },
    pct(v, digits) {   // v is a ratio 0..1
      if (!isNum(v)) return NA;
      const p = v * 100;
      if (digits == null) digits = Math.abs(p) >= 10 ? 1 : 2;
      return p.toFixed(digits) + '%';
    },
    ratio(v, digits) { return isNum(v) ? v.toFixed(digits == null ? 2 : digits) + 'x' : NA; },
    ms(v) { return isNum(v) ? (v >= 1000 ? (v / 1000).toFixed(1) + ' s' : Math.round(v) + ' ms') : NA; },
    date(v) {
      if (!v) return NA;
      const d = v instanceof Date ? v : new Date(v);
      return Number.isNaN(d.getTime()) ? String(v) : d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    },
    ago(v) {
      if (!v) return NA;
      const t = new Date(v).getTime();
      if (Number.isNaN(t)) return String(v);
      const m = Math.round((Date.now() - t) / 60000);
      if (m < 1) return 'just now';
      if (m < 60) return m + ' min ago';
      const h = Math.round(m / 60);
      if (h < 48) return h + ' h ago';
      return Math.round(h / 24) + ' days ago';
    },
    // unit-aware value for tiles: unit is one of '$', '%', 'x', 'ms', 'n' or a plain suffix
    unit(v, unit, currency) {
      if (!isNum(v)) return NA;
      switch (unit) {
        case '$': case 'usd': case 'money': return fmt.money(v, currency);
        case '%': case 'pct': return fmt.pct(v);
        case 'x': case 'ratio': return fmt.ratio(v);
        case 'ms': return fmt.ms(v);
        case 'n': case 'count': case undefined: case null: case '': return fmt.int(v);
        default: return fmt.num(v);
      }
    }
  };
  const AUTONOMY = { agent: 'agent does', founder_gate: 'founder gate', human_assist: 'human assist' };
  const CHOICE_LABEL = { agent: 'Let the agent do it', person: 'Send to a person', not_now: 'Not now' };
  const CHOICE_SAVED = { agent: 'the agent will do it', person: 'sent to a person', not_now: 'not now' };

  // ---------- network ----------
  async function api(path, opts) {
    const o = Object.assign({ method: 'GET' }, opts || {});
    const init = { method: o.method, headers: {} };
    if (o.body !== undefined) { init.headers['Content-Type'] = 'application/json'; init.body = JSON.stringify(o.body); }
    const res = await fetch(path, init);
    let data = null;
    try { data = await res.json(); } catch (e) { data = null; }
    if (!res.ok) {
      const err = new Error((data && data.error) || ('request failed: ' + res.status));
      err.status = res.status; err.data = data;
      throw err;
    }
    return data;
  }
  function screen() {
    const m = location.pathname.match(/\/screens\/([0-9]{2}-[a-z0-9-]+)/);
    if (m) return m[1];
    return document.body.dataset.screen || null;
  }
  async function loadBrand() {
    if (UI.brand) return UI.brand;
    try { UI.brand = await api('/api/brand'); } catch (e) { UI.brand = null; }
    return UI.brand;
  }

  // ---------- theme ----------
  const theme = {
    get() { return document.documentElement.dataset.theme || 'auto'; },
    set(mode) {
      if (mode === 'auto') delete document.documentElement.dataset.theme; else document.documentElement.dataset.theme = mode;
      try { localStorage.setItem('ecomos-theme', mode); } catch (e) { /* storage may be blocked */ }
    },
    init() { try { const m = localStorage.getItem('ecomos-theme'); if (m && m !== 'auto') document.documentElement.dataset.theme = m; } catch (e) { /* ignore */ } },
    isDark() { const t = theme.get(); return t === 'dark' || (t === 'auto' && matchMedia('(prefers-color-scheme: dark)').matches); }
  };
  theme.init();

  // ---------- components ----------

  /** tile: name, plain, value, unit, window, freshness, unavailable_reason, fix, delta, tone, currency */
  function tile(p) {
    p = p || {};
    const unavailable = !isNum(p.value);
    const node = el('div', { class: 'tile' + (unavailable ? ' unavailable' : '') + (p.tone ? ' ' + p.tone : ''), role: 'group', 'aria-label': p.name || '' });
    node.append(el('div', { class: 'name', text: p.name || '' }));
    if (p.plain) node.append(el('div', { class: 'plain', text: p.plain }));
    const value = el('div', { class: 'value num' });
    if (unavailable) {
      value.textContent = NA;
    } else {
      value.append(document.createTextNode(fmt.unit(p.value, p.unit, p.currency)));
      if (p.unit && !['$', 'usd', 'money', '%', 'pct', 'x', 'ratio', 'ms', 'n', 'count'].includes(p.unit)) value.append(el('span', { class: 'unit', text: p.unit }));
    }
    node.append(value);
    if (!unavailable && isNum(p.delta)) {
      const dir = p.delta > 0.0005 ? 'up' : p.delta < -0.0005 ? 'down' : 'flat';
      const good = p.higher_is_better === false ? dir === 'down' : dir === 'up';
      node.append(el('div', { class: 'delta ' + (dir === 'flat' ? 'flat' : good ? 'up' : 'down'), text: (p.delta > 0 ? '+' : '') + fmt.pct(p.delta) + (p.delta_label ? ' ' + p.delta_label : ' vs prior') }));
    }
    if (unavailable) {
      if (p.unavailable_reason) node.append(el('div', { class: 'plain', text: p.unavailable_reason }));
      if (p.fix) node.append(el('div', { class: 'fix', text: 'Connect: ' + p.fix }));
    }
    const meta = [];
    if (p.window) meta.push(el('span', { text: p.window }));
    if (p.freshness) meta.push(el('span', { text: 'as of ' + (String(p.freshness).match(/^\d{4}-\d{2}-\d{2}/) ? fmt.date(p.freshness) : p.freshness) }));
    if (meta.length) node.append(el('div', { class: 'meta' }, meta));
    return node;
  }

  /** insight: sentence, rule, severity (high|medium|low|info), capability, autonomy, screen, stub, evidence */
  function insight(p) {
    p = p || {};
    const sev = (p.severity || 'info').toLowerCase();
    const node = el('article', { class: 'insight sev-' + sev });
    node.append(el('div', { class: 'tags' },
      el('span', { class: 'chip ' + (sev === 'high' ? 'bad' : sev === 'medium' ? 'warn' : 'accent'), text: sev }),
      p.capability ? el('span', { class: 'chip mono', text: p.capability }) : null,
      p.autonomy ? el('span', { class: 'chip', text: AUTONOMY[p.autonomy] || p.autonomy }) : null));
    node.append(el('div', { class: 'sentence', text: p.sentence || '' }));
    if (p.rule) node.append(el('div', { class: 'rule' }, 'Rule: ', el('code', { text: p.rule })));
    if (p.evidence) node.append(el('div', { class: 'rule', text: p.evidence }));
    if (p.capability) node.append(decisionRow(p));
    return node;
  }

  /** decisionRow: capability, autonomy, labels {agent, person, not_now}, screen, stub (what would happen), onSaved */
  function decisionRow(p) {
    p = p || {};
    const labels = Object.assign({}, CHOICE_LABEL, p.labels || {});
    const slug = p.screen || screen();
    const node = el('div', { class: 'decision', dataset: { capability: p.capability || '' } });
    const buttons = el('div', { class: 'buttons' });
    const saved = el('div', { class: 'saved', 'aria-live': 'polite' });
    const btn = {};
    for (const choice of ['agent', 'person', 'not_now']) {
      const b = el('button', { class: 'btn' + (choice === 'agent' ? ' primary' : choice === 'not_now' ? ' quiet' : ''), type: 'button', text: labels[choice] });
      if (choice === 'agent' && p.autonomy === 'human_assist') { b.disabled = true; b.title = 'This capability needs a person.'; }
      b.addEventListener('click', () => openStub(Object.assign({}, p, { screen: slug, choice, onSaved: (row) => {
        for (const k of Object.keys(btn)) btn[k].classList.toggle('sel', k === row.choice);
        saved.className = 'saved'; saved.textContent = 'Saved: ' + CHOICE_SAVED[row.choice] + ', ' + fmt.date(row.time) + (row.reason ? '. ' + row.reason : '');
        if (p.onSaved) p.onSaved(row);
      }, onError: (msg) => { saved.className = 'saved err'; saved.textContent = 'Could not save: ' + msg; } })));
      btn[choice] = b;
      buttons.append(b);
    }
    node.append(buttons, saved);
    if (p.capability) node.append(el('div', { class: 'cap' }, el('span', { class: 'chip mono', text: p.capability }), p.autonomy ? el('span', { text: AUTONOMY[p.autonomy] || p.autonomy }) : null));
    if (p.current && btn[p.current.choice]) { btn[p.current.choice].classList.add('sel'); saved.textContent = 'Saved: ' + CHOICE_SAVED[p.current.choice] + ', ' + fmt.date(p.current.time); }
    return node;
  }

  /* The stub: until the agent layer exists, a button shows what would happen and logs the decision. */
  function openStub(p) {
    const what = p.stub || defaultStub(p);
    const reason = el('textarea', { class: 'text', placeholder: 'A short reason or note (optional)', maxlength: 300 });
    const status = el('div', { class: 'small muted', 'aria-live': 'polite' });
    const backdrop = el('div', { class: 'stub-backdrop', role: 'dialog', 'aria-modal': 'true', 'aria-label': CHOICE_LABEL[p.choice] });
    const close = () => { backdrop.remove(); document.body.style.overflow = ''; document.removeEventListener('keydown', onKey); };
    const onKey = (e) => { if (e.key === 'Escape') close(); };
    const confirm = el('button', { class: 'btn primary', type: 'button', text: 'Confirm: ' + CHOICE_LABEL[p.choice] });
    confirm.addEventListener('click', async () => {
      confirm.disabled = true; status.textContent = 'Saving';
      try {
        const res = await api('/api/decisions', { method: 'POST', body: { screen: p.screen, capability: p.capability, choice: p.choice, reason: reason.value.trim(), autonomy: p.autonomy } });
        close(); if (p.onSaved) p.onSaved(res.decision);
      } catch (e) { confirm.disabled = false; status.textContent = 'Could not save: ' + e.message; if (p.onError) p.onError(e.message); }
    });
    const box = el('div', { class: 'stub' },
      el('h2', { text: CHOICE_LABEL[p.choice] }),
      el('div', { class: 'row' }, el('span', { class: 'chip mono', text: p.capability || 'no capability id' }), el('span', { class: 'chip', text: AUTONOMY[p.autonomy] || 'autonomy unknown' }), el('span', { class: 'chip', text: p.screen || '' })),
      el('div', { class: 'what' }, el('b', { text: 'What would happen' }), what),
      el('p', { class: 'small muted', text: 'The agent layer is not built yet. This logs your decision to the decisions table so the app can act on it later.' }),
      reason,
      el('div', { class: 'row' }, confirm, el('button', { class: 'btn', type: 'button', text: 'Cancel', onclick: close }), status));
    backdrop.append(box);
    backdrop.addEventListener('click', (e) => { if (e.target === backdrop) close(); });
    document.addEventListener('keydown', onKey);
    document.body.append(backdrop); document.body.style.overflow = 'hidden';
    reason.focus();
  }
  function defaultStub(p) {
    const cap = p.capability || 'this capability';
    if (p.choice === 'agent') return 'The agent would run ' + cap + (p.autonomy === 'founder_gate' ? ', then stop for your approval before anything changes.' : ' and report back here.');
    if (p.choice === 'person') return 'A brief for ' + cap + ' would go to a person on your team with the evidence from this screen.';
    return 'Nothing runs. ' + cap + ' stays in the list and comes back when the numbers change.';
  }

  /** table: columns [{key, label, unit, align, format(fn)}], rows, sort {key, dir}, empty, maxRows */
  function table(p) {
    p = p || {};
    const cols = (p.columns || []).map((c) => typeof c === 'string' ? { key: c, label: c } : c);
    let rows = (p.rows || []).slice();
    const state = Object.assign({ key: null, dir: 'desc' }, p.sort || {});
    const wrap = el('div', { class: 'table-wrap' });
    const tbl = el('table', { class: 'kit' });
    wrap.append(tbl);
    const numeric = (c) => c.align === 'right' || c.unit || (rows.length && rows.every((r) => r[c.key] == null || isNum(r[c.key])) && rows.some((r) => isNum(r[c.key])));
    function render() {
      tbl.replaceChildren();
      const thead = el('thead');
      const tr = el('tr');
      for (const c of cols) {
        const isN = numeric(c);
        const th = el('th', { class: (isN ? 'num ' : '') + (p.sort === false ? '' : 'sortable'), scope: 'col', text: c.label || c.key });
        if (state.key === c.key) th.append(el('span', { class: 'arrow', text: state.dir === 'asc' ? '▲' : '▼' }));
        if (p.sort !== false) th.addEventListener('click', () => {
          if (state.key === c.key) state.dir = state.dir === 'asc' ? 'desc' : 'asc'; else { state.key = c.key; state.dir = isN ? 'desc' : 'asc'; }
          render();
        });
        tr.append(th);
      }
      thead.append(tr); tbl.append(thead);
      let out = rows;
      if (state.key) {
        const k = state.key, m = state.dir === 'asc' ? 1 : -1;
        out = rows.slice().sort((a, b) => {
          const x = a[k], y = b[k];
          if (x == null && y == null) return 0;
          if (x == null) return 1; if (y == null) return -1;
          return (isNum(x) && isNum(y) ? x - y : String(x).localeCompare(String(y))) * m;
        });
      }
      if (p.maxRows) out = out.slice(0, p.maxRows);
      const tbody = el('tbody');
      if (!out.length) tbody.append(el('tr', null, el('td', { class: 'empty', colspan: cols.length || 1, text: p.empty || 'No rows yet.' })));
      for (const r of out) {
        const trr = el('tr');
        for (const c of cols) {
          const v = r[c.key];
          const isN = numeric(c);
          let text;
          if (c.format) text = c.format(v, r);
          else if (v == null) text = NA;
          else if (isN && isNum(v)) text = fmt.unit(v, c.unit, p.currency);
          else text = String(v);
          const td = el('td', { class: (isN ? 'num' : '') + (v == null ? ' na' : ''), text: text });
          trr.append(td);
        }
        if (p.onRow) trr.addEventListener('click', () => p.onRow(r));
        tbody.append(trr);
      }
      tbl.append(tbody);
    }
    render();
    wrap.update = (newRows) => { rows = newRows.slice(); render(); };
    return wrap;
  }

  /** filmstrip: before {frames:[{t, src}], loaded_at}, after {...}, seconds, markers [{t, label}], caption
      Ported from speed_lab/build_founder_page.py: two columns, one clock, play, restart, scrub. */
  function filmstrip(p) {
    p = p || {};
    const sides = [['before', p.before, p.before_label || 'Before'], ['after', p.after, p.after_label || 'After']].filter((s) => s[1] && s[1].frames && s[1].frames.length);
    const seconds = p.seconds || Math.max(1, ...sides.map((s) => Math.max(s[1].loaded_at || 0, ...s[1].frames.map((f) => f.t))));
    const node = el('section', { class: 'film' });
    if (!sides.length) { node.append(el('div', { class: 'muted', text: 'No recording yet. Run the speed lab to capture a filmstrip.' })); return node; }
    let t = 0, playing = false, last = null;
    const clock = el('span', { class: 'clock num', text: '0.0 s' });
    const play = el('button', { class: 'btn primary', type: 'button', text: 'Play' });
    const restart = el('button', { class: 'btn', type: 'button', text: 'Restart' });
    const scrub = el('input', { type: 'range', min: 0, max: Math.round(seconds * 10), value: 0, 'aria-label': 'Time in tenths of a second' });
    const cols = el('div', { class: 'cols' });
    const imgs = {};
    for (const [key, side, name] of sides) {
      const img = el('img', { alt: name + ' loading' });
      const cap = el('figcaption', { text: name + ': loading' });
      imgs[key] = { img, cap, side, name };
      cols.append(el('figure', null, img, cap));
    }
    const frameAt = (frames, tt) => { let best = frames[0]; for (const f of frames) { if (f.t <= tt) best = f; else break; } return best; };
    function draw() {
      for (const k of Object.keys(imgs)) {
        const { img, cap, side, name } = imgs[k];
        const f = frameAt(side.frames, t);
        if (f && img.getAttribute('src') !== f.src) img.src = f.src;
        if (side.loaded_at != null && t >= side.loaded_at) { cap.textContent = name + ': ready to use at ' + side.loaded_at.toFixed(1) + ' s'; cap.className = 'done'; }
        else { cap.textContent = name + ': loading'; cap.className = ''; }
      }
      clock.textContent = t.toFixed(1) + ' s';
      scrub.value = Math.round(t * 10);
    }
    function tick(now) {
      if (!playing) return;
      if (last != null) t = Math.min(seconds, t + (now - last) / 1000);
      last = now; draw();
      if (t >= seconds) { playing = false; play.textContent = 'Play again'; return; }
      requestAnimationFrame(tick);
    }
    play.addEventListener('click', () => {
      if (playing) { playing = false; play.textContent = 'Play'; return; }
      if (t >= seconds) t = 0;
      playing = true; last = null; play.textContent = 'Pause'; requestAnimationFrame(tick);
    });
    restart.addEventListener('click', () => { t = 0; playing = false; last = null; play.textContent = 'Play'; draw(); });
    scrub.addEventListener('input', () => { t = parseInt(scrub.value, 10) / 10; playing = false; play.textContent = 'Play'; draw(); });
    node.append(el('div', { class: 'filmhead' }, p.caption ? el('div', { text: p.caption }) : null, el('div', { class: 'row' }, play, restart, clock)), scrub, cols);
    const markers = (p.markers || []).concat(sides.filter((s) => s[1].loaded_at != null).map((s) => ({ t: s[1].loaded_at, label: s[2] + ' ready' })));
    if (markers.length) node.append(el('div', { class: 'markers' }, markers.sort((a, b) => a.t - b.t).map((m) => el('span', { text: m.t.toFixed(1) + ' s: ' + m.label }))));
    draw();
    return node;
  }

  /** founderNote: text (string or array of paragraphs) */
  function founderNote(text) {
    const paras = Array.isArray(text) ? text : [text];
    return el('div', { class: 'founder-note' }, paras.map((t) => el('p', { text: t })));
  }

  /** emptyState: screen, title, text, missing (connector names), action {label, onClick or href} */
  function emptyState(p) {
    p = p || {};
    const node = el('div', { class: 'empty-state' });
    node.append(el('h2', { text: p.title || ((p.screen ? p.screen + ': ' : '') + 'nothing to show yet') }));
    if (p.text) node.append(el('p', { text: p.text }));
    if (p.missing && p.missing.length) node.append(el('div', { class: 'missing' }, el('span', { class: 'muted small', text: 'Needs:' }), p.missing.map((m) => el('span', { class: 'chip warn', text: m }))));
    if (p.action) node.append(p.action.href ? el('a', { class: 'btn primary', href: p.action.href, text: p.action.label }) : el('button', { class: 'btn primary', type: 'button', text: p.action.label, onclick: p.action.onClick }));
    return node;
  }

  /** sampleBadge: brand object from /api/brand (or nothing: it fetches) */
  function sampleBadge(brand) {
    const node = el('div', { class: 'sample-badge', role: 'note' });
    const fill = (b) => {
      if (!b) { node.textContent = 'Brand record unavailable.'; return; }
      node.replaceChildren();
      if (b.fictional) node.append(el('span', null, el('b', { text: b.brand }), ' is a fictional brand with generated data. Nothing here is a real company.'));
      else node.append(el('span', null, el('b', { text: b.brand }), ' live data. Read-only.'));
    };
    if (brand) fill(brand); else loadBrand().then(fill);
    return node;
  }

  // ---------- export ----------
  window.UI = { el, append, mount, fmt, api, screen, loadBrand, theme, tile, insight, decisionRow, openStub, table, filmstrip, founderNote, emptyState, sampleBadge, AUTONOMY, CHOICE_LABEL, brand: null };
})();
