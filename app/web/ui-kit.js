/* ecomOS UI kit. One global, `UI`, no build step.
   Every component returns a DOM element. Screens compose them:
     UI.mount('#tiles', UI.tile({...}), UI.tile({...}))
   v1 components: tile, insight, decisionRow, table, filmstrip, founderNote, emptyState, sampleBadge.
   v2 (depth contract, 28 Sep 2026): sectionHead, orientation, rubric, ownerChip, planBoard, actionCard,
   coverageMatrix, verdictTable, verdict, tabs, pills, panel, field, dropZone, timeline, copyButton, csv.
   Helpers: el, fmt, api, screen, mount, theme, copy. Charts live in charts.js. */
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
  const AUTONOMY = { agent: 'agent does', agent_does: 'agent does', founder_gate: 'founder gate', human_assist: 'human assist' };
  const CHOICE_LABEL = { agent: 'Agent does it', person: 'Send to a person', not_now: 'Not now' };
  const CHOICE_SAVED = { agent: 'the agent will do it', person: 'sent to a person', not_now: 'not now' };
  // owner: who ships the action. From the capability's autonomy unless the action says otherwise.
  const OWNER = { agent: 'Agent does it', agent_drafts: 'Agent drafts, you approve', person: 'A person does it' };
  const OWNER_SHORT = { agent: 'agent', agent_drafts: 'agent drafts', person: 'person' };
  const OWNER_CLASS = { agent: 'agent', agent_drafts: 'draft', person: 'person' };
  function ownerOf(p) {
    if (p.owner && OWNER[p.owner]) return p.owner;
    const a = p.autonomy || (p.capability && p.capability.autonomy);
    return a === 'human_assist' ? 'person' : a === 'founder_gate' ? 'agent_drafts' : 'agent';
  }

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
      el('span', { class: 'chip ' + (sev === 'high' || sev === 'critical' ? 'bad' : sev === 'medium' ? 'warn' : 'accent'), text: sev }),
      p.capability ? el('span', { class: 'chip mono', text: p.capability }) : null,
      p.autonomy ? el('span', { class: 'chip', text: AUTONOMY[p.autonomy] || p.autonomy }) : null));
    node.append(el('div', { class: 'sentence', text: p.sentence || '' }));
    if (p.rule) node.append(el('div', { class: 'rule' }, 'Rule: ', el('code', { text: p.rule })));
    if (p.evidence) node.append(el('div', { class: 'rule', text: p.evidence }));
    if (p.capability) node.append(decisionRow(p));
    return node;
  }

  /** decisionRow: capability, autonomy, owner (agent | agent_drafts | person), labels {agent, person, not_now},
      screen, stub (what would happen), current, onSaved, compact, finding_id.
      Three choices, logged to /api/decisions: agent, person, not_now. The agent button reads as
      "Agent does it" or "Agent drafts, you approve" from the owner; it is disabled when a person must do it. */
  function decisionRow(p) {
    p = p || {};
    const owner = ownerOf(p);
    const capId = typeof p.capability === 'object' && p.capability ? p.capability.id : p.capability;
    const autonomy = p.autonomy || (typeof p.capability === 'object' && p.capability ? p.capability.autonomy : null);
    const labels = Object.assign({}, CHOICE_LABEL, { agent: owner === 'agent_drafts' ? 'Agent drafts, I approve' : 'Agent does it' }, p.labels || {});
    const slug = p.screen || screen();
    const node = el('div', { class: 'decision' + (p.compact ? ' compact' : ''), dataset: { capability: capId || '', owner } });
    const buttons = el('div', { class: 'buttons' });
    const saved = el('div', { class: 'saved', 'aria-live': 'polite' });
    const btn = {};
    for (const choice of ['agent', 'person', 'not_now']) {
      const b = el('button', { class: 'btn' + (choice === 'agent' ? (owner === 'agent_drafts' ? ' owner-draft' : ' primary') : choice === 'not_now' ? ' quiet' : ''), type: 'button', text: labels[choice] });
      if (choice === 'agent' && owner === 'person') { b.disabled = true; b.title = 'This needs a person. Send it to one.'; }
      b.addEventListener('click', () => openStub(Object.assign({}, p, { capability: capId, autonomy, owner, screen: slug, choice, onSaved: (row) => {
        for (const k of Object.keys(btn)) btn[k].classList.toggle('sel', k === row.choice);
        saved.className = 'saved'; saved.textContent = 'Saved: ' + CHOICE_SAVED[row.choice] + ', ' + fmt.date(row.time) + (row.reason ? '. ' + row.reason : '');
        if (p.onSaved) p.onSaved(row);
      }, onError: (msg) => { saved.className = 'saved err'; saved.textContent = 'Could not save: ' + msg; } })));
      btn[choice] = b;
      buttons.append(b);
    }
    node.append(buttons, saved);
    if (capId) node.append(el('div', { class: 'cap' }, el('span', { class: 'chip mono', text: capId }), el('span', { text: OWNER[owner] })));
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
    const confirm = el('button', { class: 'btn primary', type: 'button', text: 'Confirm: ' + (p.choice === 'agent' ? OWNER[p.owner || 'agent'] : CHOICE_LABEL[p.choice]) });
    confirm.addEventListener('click', async () => {
      confirm.disabled = true; status.textContent = 'Saving';
      try {
        const body = { screen: p.screen, capability: p.capability, choice: p.choice, reason: reason.value.trim(), autonomy: p.autonomy === 'agent_does' ? 'agent' : p.autonomy };
        if (p.finding_id) body.finding_id = p.finding_id;
        const res = await api('/api/decisions', { method: 'POST', body });
        close(); if (p.onSaved) p.onSaved(res.decision);
      } catch (e) { confirm.disabled = false; status.textContent = 'Could not save: ' + e.message; if (p.onError) p.onError(e.message); }
    });
    const box = el('div', { class: 'stub' },
      el('h2', { text: p.title || (p.choice === 'agent' ? OWNER[p.owner || 'agent'] : CHOICE_LABEL[p.choice]) }),
      el('div', { class: 'row' }, el('span', { class: 'chip mono', text: p.capability || 'no capability id' }), el('span', { class: 'chip owner ' + (OWNER_CLASS[p.owner] || 'agent'), text: OWNER[p.owner] || AUTONOMY[p.autonomy] || 'owner unknown' }), el('span', { class: 'chip', text: p.screen || '' })),
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
    if (p.choice === 'agent') return 'The agent would run ' + cap + (p.owner === 'agent_drafts' || p.autonomy === 'founder_gate' ? ', then stop for your approval before anything ships.' : ' and report back here.');
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
      wrap.__rows = out;
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

  // ================= v2: execution-surface components (depth contract) =================

  function copyText(text) {
    try { return navigator.clipboard.writeText(text).then(() => true, () => false); }
    catch (e) { return Promise.resolve(false); }
  }
  /** copyButton: text or () => text, label. Copies to the clipboard and says "Copied" for 1.5 s. */
  function copyButton(p) {
    p = p || {};
    const b = el('button', { class: 'btn sm ' + (p.cls || ''), type: 'button', text: p.label || 'Copy' });
    b.addEventListener('click', async () => {
      const t = typeof p.text === 'function' ? p.text() : p.text;
      const ok = await copyText(String(t == null ? '' : t));
      const was = b.textContent; b.textContent = ok ? 'Copied' : 'Could not copy';
      setTimeout(() => { b.textContent = was; }, 1500);
    });
    return b;
  }
  /** csv: rows (objects) and columns [{key,label}] to a downloadable file. */
  function csv(rows, columns, filename) {
    const cols = columns || Object.keys(rows[0] || {}).map((k) => ({ key: k, label: k }));
    const esc = (v) => { const s = v == null ? '' : String(v); return /[",\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s; };
    const lines = [cols.map((c) => esc(c.label || c.key)).join(',')].concat(rows.map((r) => cols.map((c) => esc(r[c.key])).join(',')));
    const blob = new Blob([lines.join('\n')], { type: 'text/csv' });
    const a = el('a', { href: URL.createObjectURL(blob), download: filename || 'export.csv' });
    document.body.append(a); a.click(); a.remove();
  }

  /** sectionHead: title, sub (the window and the rule in numbers), orient (array for orientation()), tools (elements) */
  function sectionHead(p) {
    p = p || {};
    const node = el('div', { class: 'sec-head' });
    node.append(el('h2', { text: p.title || '' }));
    if (p.orient) node.append(orientation(p.orient));
    if (p.tools) node.append(el('div', { class: 'tools' }, p.tools));
    if (p.sub) node.append(el('div', { class: 'sub', text: p.sub }));
    return node;
  }

  /** orientation: items [{label, value, unit, delta, higher_is_better, tone, title}]. Small numbers beside a plan or a heading. */
  function orientation(items) {
    const node = el('div', { class: 'orient', role: 'list' });
    for (const it of items || []) {
      const na = !isNum(it.value);
      const o = el('span', { class: 'o' + (na ? ' na' : '') + (it.tone ? ' ' + it.tone : ''), role: 'listitem', title: it.title || '' });
      o.append(el('span', { text: it.label }), el('b', { text: na ? (it.unavailable_label || 'unavailable') : fmt.unit(it.value, it.unit, it.currency) + (it.suffix || '') }));
      if (!na && isNum(it.delta)) {
        const dir = it.delta > 0.0005 ? 'up' : it.delta < -0.0005 ? 'down' : 'flat';
        const good = it.higher_is_better === false ? dir === 'down' : dir === 'up';
        o.append(el('span', { class: 'd ' + (dir === 'flat' ? '' : good ? 'up' : 'down'), text: (it.delta > 0 ? '+' : '') + fmt.pct(it.delta) }));
      }
      node.append(o);
    }
    return node;
  }

  const RUBRIC_DIMS = [['revenue', 'Rev', 'Revenue impact'], ['profit', 'Prof', 'Profit impact'], ['reputation', 'Rep', 'Brand reputation'], ['satisfaction', 'Sat', 'Customer satisfaction'], ['ease', 'Ease', 'Ease to ship'], ['confidence', 'Conf', 'Confidence']];
  /** rubric: {revenue, profit, reputation, satisfaction, ease, confidence, total}. Six boxes 0..5 and the total /100. */
  function rubric(r, opts) {
    r = r || {}; opts = opts || {};
    const node = el('span', { class: 'rubric', title: RUBRIC_DIMS.map((d) => d[2] + ': ' + (isNum(r[d[0]]) ? r[d[0]] : 'n/a')).join('\n') });
    for (const [k, short] of RUBRIC_DIMS) {
      const v = r[k];
      node.append(el('span', { class: 'r' + (isNum(v) ? '' : ' na'), dataset: { lvl: isNum(v) ? String(Math.round(v)) : '' }, text: isNum(v) ? String(Math.round(v)) : 'n/a', 'aria-label': short }));
    }
    if (!opts.noTotal) node.append(el('span', { class: 'total' }, isNum(r.total) ? String(Math.round(r.total)) : 'n/a', el('small', { text: ' /100' })));
    return node;
  }
  function rubricLegend() {
    return el('div', { class: 'rubric-legend' }, RUBRIC_DIMS.map((d) => el('span', { text: d[1] + ' = ' + d[2] })), el('span', { text: '0 to 5 each, weighted to 100.' }));
  }
  /** ownerChip: owner (agent | agent_drafts | person) or an action */
  function ownerChip(o) {
    const owner = typeof o === 'string' ? o : ownerOf(o || {});
    return el('span', { class: 'chip owner ' + (OWNER_CLASS[owner] || 'agent'), text: OWNER[owner] || owner });
  }
  const SEV_CHIP = { critical: 'bad', high: 'bad', medium: 'warn', low: '' };
  function sevChip(sev) { return el('span', { class: 'chip ' + (SEV_CHIP[sev] || ''), text: sev || '' }); }
  function stakeText(a) {
    const m = a.money_at_stake;
    if (m && isNum(m.usd)) return fmt.money(m.usd) + ' at stake' + (m.window ? ', ' + m.window : '');
    if (a.size && a.size.text) return a.size.text;
    return 'stake unavailable';
  }
  function artefactIcon(kind) {
    const map = { ad_brief: 'AD', creative: 'IMG', copy: 'TXT', page_section: 'SEC', landing_page: 'LP', offer: 'OFR', price_change: '$', email: 'EML', flow: 'FLW', test_brief: 'TST', listing_fix: 'LST', feed_fix: 'FD', budget_move: 'BGT', bid_change: 'BID', connector_setup: 'CON', brain_record: 'BRN', policy: 'POL', research_note: 'RSH', ticket: 'TKT', report: 'RPT' };
    return map[kind] || 'OUT';
  }
  function stepsList(steps) {
    return el('ol', { class: 'a-steps' }, (steps || []).map((s) => el('li', null, s.text || String(s), s.who ? el('span', { class: 'who', text: ' (' + (OWNER_SHORT[s.who] || s.who) + ')' }) : null)));
  }
  function briefText(a) {
    const lines = [a.title, '', 'Why: ' + (a.why || ''), 'Owner: ' + (OWNER[ownerOf(a)] || ''), 'Artefact: ' + ((a.artefact && a.artefact.label) || (a.artefact && a.artefact.kind) || 'unavailable')];
    if (a.steps && a.steps.length) { lines.push('', 'Steps:'); a.steps.forEach((s, i) => lines.push((i + 1) + '. ' + (s.text || s) + (s.who ? ' (' + (OWNER_SHORT[s.who] || s.who) + ')' : ''))); }
    if (a.stop_rule) lines.push('', 'Stop if: ' + a.stop_rule);
    if (a.check_on) lines.push('Check on: ' + fmt.date(a.check_on));
    lines.push('Stake: ' + stakeText(a));
    if (a.rubric) lines.push('Score: ' + (a.rubric.total == null ? 'n/a' : Math.round(a.rubric.total)) + ' /100');
    return lines.join('\n');
  }

  /** implementation block: owner, steps with who, artefact, win and stop rule, check date. Used inside actionCard and planBoard. */
  function implementation(a) {
    const owner = ownerOf(a);
    const art = a.artefact || {};
    const grid = el('div', { class: 'a-grid' });
    grid.append(el('div', { class: 'a-block' }, el('span', { class: 'kicker', text: 'How it gets done' }),
      el('div', { class: 'row' }, ownerChip(owner), a.time_to_ship_hours != null ? el('span', { class: 'chip', text: 'about ' + a.time_to_ship_hours + ' h' }) : null, a.capability ? el('span', { class: 'chip mono', text: typeof a.capability === 'object' ? a.capability.id : a.capability }) : null),
      a.steps && a.steps.length ? stepsList(a.steps) : el('div', { class: 'na', text: 'steps unavailable' })));
    const right = el('div', { class: 'stack' });
    right.append(el('div', { class: 'a-block' }, el('span', { class: 'kicker', text: 'Artefact' }),
      el('div', { class: 'a-artefact' }, el('span', { class: 'ico', text: artefactIcon(art.kind) }), el('span', { text: art.label || art.kind || 'unavailable' })),
      art.draft ? el('div', { class: 'small', style: { whiteSpace: 'pre-wrap' }, text: art.draft }) : el('div', { class: 'micro faint', text: art.draft_note || 'Draft appears here once the agent runs.' })));
    if (a.win_rule || a.stop_rule || a.check_on) right.append(el('div', { class: 'a-block' }, el('span', { class: 'kicker', text: 'Rules' }),
      a.win_rule ? el('div', null, el('b', { text: 'Win if: ' }), a.win_rule) : null,
      a.stop_rule ? el('div', null, el('b', { text: 'Stop if: ' }), a.stop_rule) : null,
      a.check_on ? el('div', null, el('b', { text: 'Check on: ' }), fmt.date(a.check_on)) : null));
    grid.append(right);
    return grid;
  }

  /** actionCard: an action from /api/<slug>/rank plus {screen, expanded, onDecision, extra (elements)} */
  function actionCard(a, opts) {
    opts = opts || {};
    const node = el('article', { class: 'action' + (opts.compact ? ' compact' : ''), dataset: { id: a.id || '', owner: ownerOf(a) } });
    node.append(el('div', { class: 'a-head' }, el('span', { class: 'a-title', text: a.title || '' }), sevChip(a.severity), a.status === 'unavailable' ? el('span', { class: 'chip', text: 'needs a connector' }) : null, a.rubric ? rubric(a.rubric) : null));
    if (a.why) node.append(el('div', { class: 'a-why', html: escapeHtml(a.why).replace(/(\$[\d,\.]+|\d[\d,\.]*\s?(?:percent|%|x|days?|h))/g, '<b>$1</b>') }));
    const impl = implementation(a);
    if (!opts.expanded) impl.hidden = true;
    node.append(impl);
    if (opts.extra) node.append(opts.extra);
    const toggle = el('button', { class: 'btn quiet sm', type: 'button', text: opts.expanded ? 'Hide steps' : 'Show steps' });
    toggle.addEventListener('click', () => { impl.hidden = !impl.hidden; toggle.textContent = impl.hidden ? 'Show steps' : 'Hide steps'; });
    const foot = el('div', { class: 'a-foot' }, el('span', { class: 'stake' + (a.money_at_stake && isNum(a.money_at_stake.usd) ? '' : ' na') , text: stakeText(a) }),
      a.entity && a.entity.label ? el('span', { class: 'chip', text: a.entity.label }) : null,
      a.screen && opts.showScreen ? el('span', { class: 'chip mono', text: a.screen }) : null,
      toggle, copyButton({ label: 'Copy brief', text: () => briefText(a) }),
      opts.make ? el('button', { class: 'btn soft sm', type: 'button', text: opts.make.label || 'Make it', onclick: () => opts.make.onClick(a) }) : null,
      decisionRow({ capability: a.capability, owner: ownerOf(a), screen: opts.screen || a.screen, compact: true, current: a.decision, finding_id: a.id, stub: a.stub, onSaved: opts.onDecision }));
    node.append(foot);
    return node;
  }

  /** planBoard: title, sub, orient, actions (from rank or master), limit (default 10), screen, onDecision, empty, tools */
  function planBoard(p) {
    p = p || {};
    const node = el('section', { class: 'plan', 'aria-label': p.title || 'The plan' });
    const head = el('div', { class: 'plan-head' }, el('h2', { text: p.title || 'The plan' }));
    if (p.sub) head.append(el('span', { class: 'muted small', text: p.sub }));
    if (p.orient) head.append(orientation(p.orient));
    if (p.tools) head.append(el('div', { class: 'tools' }, p.tools));
    node.append(head);
    const list = el('div', { class: 'plan-list' });
    const actions = (p.actions || []).slice(0, p.limit || 10);
    if (!actions.length) list.append(el('div', { class: 'plan-empty', text: p.empty || 'Nothing to approve. The audits found no open finding for this window.' }));
    actions.forEach((a, i) => {
      const item = el('div', { class: 'plan-item' + (i < 3 ? ' top' : '') + ' sev-' + (a.severity || 'medium'), dataset: { id: a.id || '' } });
      item.append(el('div', { class: 'rank num', text: String(i + 1) }));
      item.append(el('div', { class: 'head' }, el('span', { class: 'title', text: a.title || '' }), ownerChip(a), sevChip(a.severity), a.screen && p.showScreen ? el('span', { class: 'chip mono', text: a.screen }) : null, a.status === 'unavailable' ? el('span', { class: 'chip', text: 'connect first' }) : null));
      if (a.why) item.append(el('div', { class: 'why', html: escapeHtml(a.why).replace(/(\$[\d,\.]+|\d[\d,\.]*\s?(?:percent|%|x))/g, '<b>$1</b>') }));
      const more = el('div', { class: 'more', hidden: true });
      const toggle = el('button', { class: 'toggle', type: 'button', text: 'How it gets done' });
      toggle.addEventListener('click', () => { if (more.hidden) { more.replaceChildren(implementation(a)); more.hidden = false; toggle.textContent = 'Hide'; } else { more.hidden = true; toggle.textContent = 'How it gets done'; } });
      item.append(el('div', { class: 'foot' }, el('span', { class: 'stake' + (a.money_at_stake && isNum(a.money_at_stake.usd) ? '' : ' na'), text: stakeText(a) }),
        a.rubric ? rubric(a.rubric) : null, toggle, copyButton({ label: 'Copy brief', cls: 'quiet xs', text: () => briefText(a) }),
        decisionRow({ capability: a.capability, owner: ownerOf(a), screen: p.screen || a.screen, compact: true, current: a.decision, finding_id: a.id, stub: a.stub, onSaved: p.onDecision })));
      item.append(more);
      list.append(item);
    });
    node.append(list);
    if (p.foot) node.append(el('div', { class: 'plan-head', style: { borderTop: '1px solid var(--line)', borderBottom: 0 } }, p.foot));
    return node;
  }

  /** coverageMatrix: rows [{key,label,sub}], cols [{key,label}], cells {rowKey: {colKey: {us, them, unit, n, label}}},
      unit ('n', '$', '%', 'x'), single (no them), gapRule (cell) => 'gap' | 'over' | 'lead' | '', onCell(cell, row, col),
      action {label, onClick(cell,row,col)} shown on gap cells, title, note, totals (bool). Us against them in every cell;
      an empty cell is a gap and carries the action. */
  function coverageMatrix(p) {
    p = p || {};
    const rows = p.rows || [], cols = p.cols || [], cells = p.cells || {};
    const wrap = el('div', { class: 'stack' });
    if (p.title) wrap.append(el('div', { class: 'row between' }, el('h4', { text: p.title }), p.tools || null));
    const scroll = el('div', { class: 'matrix-wrap' });
    const tbl = el('table', { class: 'matrix' });
    const thead = el('thead'), htr = el('tr');
    htr.append(el('th', { class: 'rowh', text: p.corner || '' }));
    for (const c of cols) htr.append(el('th', { text: c.label || c.key, title: c.title || '' }));
    if (p.totals) htr.append(el('th', { text: 'Total' }));
    thead.append(htr); tbl.append(thead);
    const tbody = el('tbody');
    const gapOf = p.gapRule || ((c) => {
      if (!c) return 'gap';
      if (p.single) return '';
      if (!isNum(c.us) && isNum(c.them) && c.them > 0) return 'gap';
      if (isNum(c.us) && isNum(c.them)) { if (c.them > 0 && c.us === 0) return 'gap'; if (c.us > c.them * 1.5 && c.us > 0) return 'over'; if (c.us > 0 && c.us >= c.them && c.them > 0) return 'lead'; }
      return '';
    });
    const vtxt = (v, unit) => isNum(v) ? fmt.unit(v, unit || p.unit) : 'n/a';
    const colTotals = {};
    for (const r of rows) {
      const tr = el('tr');
      const th = el('td', { class: 'rowh' }, r.label || r.key);
      if (r.sub) th.append(el('small', { text: r.sub }));
      tr.append(th);
      let rowTotal = null;
      for (const c of cols) {
        const cell = (cells[r.key] || {})[c.key] || null;
        const kind = gapOf(cell, r, c);
        const na = !cell || (!isNum(cell.us) && !isNum(cell.them));
        const box = el('div', { class: 'cell' + (p.single ? ' single' : '') + (kind ? ' ' + kind : '') + (na ? ' na' : ''), title: (r.label || r.key) + ' × ' + (c.label || c.key) + (cell ? '\nus: ' + vtxt(cell.us, cell.unit) + (p.single ? '' : '\nthem: ' + vtxt(cell.them, cell.unit)) + (cell.n != null ? '\nn: ' + cell.n : '') : '\nnot tried') });
        if (!p.single && cell && isNum(cell.share)) box.style.background = 'color-mix(in srgb, var(--heat-hi) ' + Math.round(Math.min(1, cell.share) * 60) + '%, var(--surface))';
        if (p.single && cell && isNum(cell.us) && isNum(p.max) && p.max > 0) box.style.background = 'color-mix(in srgb, var(--heat-hi) ' + Math.round(Math.min(1, cell.us / p.max) * 70) + '%, var(--heat-lo))';
        box.append(el('span', { class: 'us', text: cell ? vtxt(cell.us, cell.unit) : (p.single ? 'n/a' : 'not tried') }));
        if (!p.single) box.append(el('span', { class: 'them', text: cell ? vtxt(cell.them, cell.unit) : (cell === null ? 'n/a' : '') }));
        if (p.action && (kind === 'gap' || (cell && cell.act))) {
          const b = el('button', { class: 'act', type: 'button', text: p.action.label || 'Make it' });
          b.addEventListener('click', (e) => { e.stopPropagation(); p.action.onClick(cell, r, c); });
          (p.single ? box : box.lastChild).append(b);
        }
        const td = el('td', null, box);
        if (p.onCell) td.addEventListener('click', () => p.onCell(cell, r, c));
        tr.append(td);
        if (cell && isNum(cell.us)) { rowTotal = (rowTotal || 0) + cell.us; colTotals[c.key] = (colTotals[c.key] || 0) + cell.us; }
      }
      if (p.totals) tr.append(el('td', { class: 'total num', text: vtxt(rowTotal) }));
      tbody.append(tr);
    }
    tbl.append(tbody);
    if (p.totals) { const tf = el('tfoot'), tr = el('tr'); tr.append(el('td', { class: 'rowh', text: 'Total' })); for (const c of cols) tr.append(el('td', { class: 'total num', text: vtxt(colTotals[c.key]) })); tr.append(el('td', { class: 'total' })); tf.append(tr); tbl.append(tf); }
    scroll.append(tbl); wrap.append(scroll);
    const legend = el('div', { class: 'matrix-legend' });
    if (!p.single) legend.append(el('span', { text: 'Each cell: us | them' }), el('span', null, el('i', { class: 'gap' }), 'gap, they run it and we do not'), el('span', null, el('i', { class: 'lead' }), 'we lead'), el('span', null, el('i', { class: 'over' }), 'we are far ahead, check for waste'));
    if (p.note) legend.append(el('span', { text: p.note }));
    wrap.append(legend);
    return wrap;
  }

  /** verdict: kind (scale|watch|cut|keep|fix|stop|wait|new|na or good|warn|bad|info), text, reason (title) */
  function verdict(kind, text, reason) {
    return el('span', { class: 'verdict ' + (kind || 'na'), text: text || kind || '', title: reason || '' });
  }
  /** verdictTable: like table plus a verdict column {key, kinds: (row) => kind, reason: (row) => text} and an actions column
      {label or (row)=>label, onClick(row)} or per-row row.actions [{label,onClick}]. Rows carry entity data; the reason column is the rule in numbers. */
  function verdictTable(p) {
    p = p || {};
    const cols = (p.columns || []).slice();
    const v = p.verdict || { key: 'verdict' };
    const vcol = { key: v.key || 'verdict', label: v.label || 'Verdict', format: (val, r) => '' };
    cols.splice(v.at == null ? 1 : v.at, 0, vcol);
    if (p.reason) cols.push({ key: p.reason.key || 'reason', label: p.reason.label || 'Why', format: (val, r) => (p.reason.text ? p.reason.text(r) : val) || '' });
    if (p.actions) cols.push({ key: '__act', label: p.actions.label || 'Do', format: () => '' });
    const t = table(Object.assign({}, p, { columns: cols }));
    // post-render: swap verdict and action cells for real elements
    const decorate = () => {
      const body = t.querySelector('tbody'); if (!body) return;
      const shown = t.__rows || [];
      Array.from(body.querySelectorAll('tr')).forEach((tr, i) => {
        const r = shown[i]; if (!r) return;
        const tds = tr.children;
        const vi = cols.indexOf(vcol);
        const kind = v.kind ? v.kind(r) : r[vcol.key];
        if (tds[vi]) { tds[vi].replaceChildren(verdict(kind, v.text ? v.text(r) : (r[vcol.key + '_text'] || kind), v.reason ? v.reason(r) : r.reason)); tds[vi].className = ''; }
        if (p.reason) { const ri = cols.findIndex((c) => c.key === (p.reason.key || 'reason')); if (tds[ri]) tds[ri].classList.add('wrap'); }
        if (p.actions) {
          const ai = cols.length - 1;
          const acts = (r.actions || [p.actions]).filter(Boolean);
          tds[ai].replaceChildren(el('div', { class: 'row' }, acts.map((a) => el('button', { class: 'btn xs ' + (a.cls || 'soft'), type: 'button', text: typeof a.label === 'function' ? a.label(r) : a.label, onclick: (e) => { e.stopPropagation(); a.onClick(r); } }))));
          tds[ai].className = 'act';
        }
      });
    };
    // table() re-renders on sort; wrap its render by observing
    const mo = new MutationObserver(() => { mo.disconnect(); decorate(); mo.observe(t.querySelector('table'), { childList: true }); });
    decorate(); mo.observe(t.querySelector('table'), { childList: true });
    return t;
  }

  /** tabs: items [{key, label, n, panel (element or () => element)}], current, onChange. Jobs inside a section. */
  function tabs(p) {
    p = p || {};
    const items = p.items || [];
    const node = el('div', { class: 'tabs-wrap' });
    const bar = el('div', { class: 'tabs', role: 'tablist' });
    const panels = el('div', { class: 'tab-panels' });
    let cur = p.current || (items[0] && items[0].key);
    const btns = {};
    function show(key) {
      cur = key;
      for (const it of items) { btns[it.key].classList.toggle('sel', it.key === key); btns[it.key].setAttribute('aria-selected', it.key === key ? 'true' : 'false'); }
      const it = items.find((x) => x.key === key);
      const panel = it ? (typeof it.panel === 'function' ? it.panel() : it.panel) : null;
      panels.replaceChildren(el('div', { role: 'tabpanel' }, panel));
      if (p.onChange) p.onChange(key);
    }
    for (const it of items) {
      const b = el('button', { class: 'tab', type: 'button', role: 'tab', text: it.label });
      if (it.n != null) b.append(el('span', { class: 'n', text: String(it.n) }));
      b.addEventListener('click', () => show(it.key));
      btns[it.key] = b; bar.append(b);
    }
    node.append(bar, panels);
    if (cur) show(cur);
    node.show = show;
    return node;
  }

  /** pills: items [{key, label, n}], current (key or array when multi), multi, onChange(keys). Filters. */
  function pills(p) {
    p = p || {};
    const node = el('div', { class: 'pills', role: 'group' });
    let sel = new Set(Array.isArray(p.current) ? p.current : p.current ? [p.current] : []);
    const btns = {};
    const paint = () => { for (const k of Object.keys(btns)) btns[k].classList.toggle('sel', sel.has(k)); };
    for (const it of p.items || []) {
      const b = el('button', { class: 'pill', type: 'button', text: it.label });
      if (it.n != null) b.append(el('span', { class: 'n', text: String(it.n) }));
      b.addEventListener('click', () => {
        if (p.multi) { if (sel.has(it.key)) sel.delete(it.key); else sel.add(it.key); }
        else sel = new Set([it.key]);
        paint(); if (p.onChange) p.onChange(p.multi ? Array.from(sel) : it.key);
      });
      btns[it.key] = b; node.append(b);
    }
    paint();
    return node;
  }

  /** panel: title, body (element or array), tools (elements), onClose. A side drawer for one entity's detail and its actions. */
  function panel(p) {
    p = p || {};
    const backdrop = el('div', { class: 'panel-backdrop', role: 'dialog', 'aria-modal': 'true', 'aria-label': p.title || 'Detail' });
    const close = () => { backdrop.remove(); document.body.style.overflow = ''; document.removeEventListener('keydown', onKey); if (p.onClose) p.onClose(); };
    const onKey = (e) => { if (e.key === 'Escape') close(); };
    const box = el('div', { class: 'panel' },
      el('div', { class: 'p-head' }, el('h2', { text: p.title || '' }), p.tools ? el('div', { class: 'row' }, p.tools) : null, el('button', { class: 'btn quiet sm', type: 'button', text: 'Close', onclick: close })),
      el('div', { class: 'p-body' }, p.body));
    backdrop.append(box);
    backdrop.addEventListener('click', (e) => { if (e.target === backdrop) close(); });
    document.addEventListener('keydown', onKey);
    document.body.append(backdrop); document.body.style.overflow = 'hidden';
    backdrop.close = close;
    return backdrop;
  }

  /** field: an editable brain fact. {name, sub, value, text, tier, source, date, confidence, onSave(text) => Promise, placeholder, multiline}.
      Shows the value with its tier and source; Edit turns it into a textarea; Save calls onSave, which writes an approved founder record. */
  function field(p) {
    p = p || {};
    const na = p.text == null || p.text === '';
    const node = el('div', { class: 'field' + (p.tier === 'approved' ? ' approved' : ''), dataset: { field: p.key || '' } });
    const name = el('div', { class: 'f-name' }, p.name || p.key || '');
    if (p.sub) name.append(el('small', { text: p.sub }));
    const val = el('div', { class: 'f-val' });
    const text = el('div', { class: 'f-text' + (na ? ' na' : ''), text: na ? (p.placeholder || 'unavailable, add it') : p.text });
    const meta = el('div', { class: 'f-meta' });
    if (p.tier) meta.append(el('span', { class: 'chip ' + (p.tier === 'approved' ? 'good' : p.tier === 'site_backed' ? 'accent' : p.tier === 'forbidden' ? 'bad' : 'warn'), text: String(p.tier).replace(/_/g, ' ') }));
    if (p.source) meta.append(el('span', { text: p.source }));
    if (p.date) meta.append(el('span', { text: fmt.date(p.date) }));
    if (isNum(p.confidence)) meta.append(el('span', { text: 'confidence ' + p.confidence }));
    if (p.used_by) meta.append(el('span', { text: 'used by ' + p.used_by }));
    const editBtn = el('button', { class: 'btn xs quiet f-btn', type: 'button', text: na ? 'Add' : 'Edit' });
    meta.append(editBtn);
    const ta = el('textarea', { class: 'text', rows: p.multiline ? 3 : 1, 'aria-label': 'Edit ' + (p.name || p.key || '') });
    const save = el('button', { class: 'btn primary sm', type: 'button', text: 'Save as approved' });
    const cancel = el('button', { class: 'btn sm', type: 'button', text: 'Cancel' });
    const status = el('span', { class: 'small muted' });
    const edit = el('div', { class: 'f-edit' }, ta, save, cancel, status);
    editBtn.addEventListener('click', () => { ta.value = na ? '' : p.text; node.classList.add('editing'); ta.focus(); });
    cancel.addEventListener('click', () => { node.classList.remove('editing'); status.textContent = ''; });
    save.addEventListener('click', async () => {
      const v = ta.value.trim(); if (!v) { status.textContent = 'Type a value first.'; return; }
      save.disabled = true; status.textContent = 'Saving';
      try {
        const res = p.onSave ? await p.onSave(v) : null;
        text.textContent = v; text.classList.remove('na'); node.classList.remove('editing', 'unverified'); node.classList.add('approved');
        meta.replaceChildren(el('span', { class: 'chip good', text: 'approved' }), el('span', { text: 'you, ' + fmt.date(new Date()) }), res && res.flows_to ? el('span', { text: 'flows to ' + res.flows_to }) : null, editBtn);
        editBtn.textContent = 'Edit'; status.textContent = '';
        if (p.onSaved) p.onSaved(res);
      } catch (e) { status.textContent = 'Could not save: ' + e.message; }
      save.disabled = false;
    });
    val.append(text, meta, edit);
    node.append(name, val);
    return node;
  }

  /** dropZone: {accept, hint, onFiles(files), onUrl(url), urlPlaceholder}. Drop, choose or paste a url. */
  function dropZone(p) {
    p = p || {};
    const input = el('input', { type: 'file', multiple: true, accept: p.accept || '' });
    const node = el('div', { class: 'drop' });
    node.append(el('div', null, el('b', { text: 'Drop any file here' }), ' or ', el('a', { href: '#', text: 'choose one', onclick: (e) => { e.preventDefault(); input.click(); } }), '. ', p.hint || 'It lands in the documents manifest as it is. Nothing is blocked.'));
    input.addEventListener('change', () => { if (input.files.length && p.onFiles) p.onFiles(Array.from(input.files)); input.value = ''; });
    node.append(input);
    if (p.onUrl) {
      const url = el('input', { class: 'text sm', type: 'url', placeholder: p.urlPlaceholder || 'or paste a url (a page, a deck, a doc)' });
      const go = el('button', { class: 'btn sm', type: 'button', text: 'Add url' });
      go.addEventListener('click', () => { const u = url.value.trim(); if (u) { p.onUrl(u); url.value = ''; } });
      url.addEventListener('keydown', (e) => { if (e.key === 'Enter') go.click(); });
      node.append(el('div', { class: 'url' }, url, go));
    }
    ['dragenter', 'dragover'].forEach((ev) => node.addEventListener(ev, (e) => { e.preventDefault(); node.classList.add('over'); }));
    ['dragleave', 'drop'].forEach((ev) => node.addEventListener(ev, (e) => { e.preventDefault(); node.classList.remove('over'); }));
    node.addEventListener('drop', (e) => { const fs = Array.from((e.dataTransfer && e.dataTransfer.files) || []); if (fs.length && p.onFiles) p.onFiles(fs); });
    return node;
  }

  /** timeline: items [{when, title, text, tone}], most recent first. Decisions, changes, launches. */
  function timeline(items) {
    const node = el('div', { class: 'timeline' });
    for (const it of items || []) {
      node.append(el('div', { class: 'tl' }, el('span', { class: 'dot', style: it.tone ? { background: 'var(--' + it.tone + ')', boxShadow: '0 0 0 3px var(--' + it.tone + '-soft)' } : null }),
        el('div', null, el('div', { class: 'when', text: it.when ? fmt.date(it.when) + (it.who ? ', ' + it.who : '') : '' }), el('div', null, el('b', { text: it.title || '' }), it.text ? ' ' + it.text : ''))));
    }
    if (!(items || []).length) node.append(el('div', { class: 'muted small', text: 'Nothing yet.' }));
    return node;
  }

  function escapeHtml(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c])); }

  // ---------- export ----------
  window.UI = { el, append, mount, fmt, api, screen, loadBrand, theme, tile, insight, decisionRow, openStub, table, filmstrip, founderNote, emptyState, sampleBadge,
    sectionHead, orientation, rubric, rubricLegend, ownerChip, ownerOf, sevChip, planBoard, actionCard, implementation, coverageMatrix, verdict, verdictTable, tabs, pills, panel, field, dropZone, timeline, copyButton, copy: copyText, csv, briefText, escapeHtml,
    AUTONOMY, CHOICE_LABEL, OWNER, RUBRIC_DIMS, brand: null };
})();
