/* The shell: lists the 28 screens from /api/screens and renders the chosen one in an iframe.
   Route: #/<slug>. A screen without index.html shows the kit's empty state instead. */
(function () {
  'use strict';
  const PHASES = [
    ['Start here', ['setup']], ['A. Foundation', ['00']], ['B. Know the customer', ['01', '02', '03', '04', '05']], ['C. The store', ['06', '07', '08']],
    ['D. Acquisition', ['09', '10', '11', '12', '13']], ['E. Retention', ['14', '15']], ['F. Organic', ['16', '17', '18']],
    ['G. Operations', ['19', '20', '21', '22', '23', '24']], ['H. Memory', ['25', '26', '27']]];
  let screens = [], brand = null, current = null;
  const $ = (id) => document.getElementById(id);

  function slugFromHash() {
    const m = location.hash.match(/^#\/?([0-9]{2}-[a-z0-9-]+|setup)\b/);
    return m ? m[1] : null;
  }
  function phaseOf(slug) {
    const n = slug === 'setup' ? slug : slug.slice(0, 2);
    const p = PHASES.find((ph) => ph[1].includes(n));
    return p ? p[0] : '';
  }
  function renderNav() {
    const list = $('navlist');
    list.replaceChildren();
    let lastPhase = null;
    for (const s of screens) {
      const ph = phaseOf(s.slug);
      if (ph !== lastPhase) { list.append(UI.el('div', { class: 'phase', text: ph })); lastPhase = ph; }
      const a = UI.el('a', { href: '#/' + s.slug, class: (s.built ? 'built' : '') + (s.slug === current ? ' sel' : ''), title: s.purpose },
        UI.el('span', { class: 'n', text: s.slug === 'setup' ? '>' : s.slug.slice(0, 2) }), UI.el('span', { text: s.room }), UI.el('span', { class: 'dot', 'aria-hidden': 'true' }));
      list.append(a);
    }
    const sel = $('screen-select');
    sel.replaceChildren();
    for (const s of screens) sel.append(UI.el('option', { value: s.slug, text: (s.slug === 'setup' ? '>' : s.slug.slice(0, 2)) + '  ' + s.room + (s.built ? '' : ' (not built)') }));
    if (current) sel.value = current;
    const built = screens.filter((s) => s.built).length;
    $('built-count').textContent = built + ' of ' + screens.length + ' screens built';
  }
  function renderBrand() {
    const card = $('brandcard');
    card.replaceChildren();
    if (!brand) { card.append(UI.el('b', { text: 'Brand unavailable' })); return; }
    card.append(UI.el('b', { text: brand.brand }), UI.el('span', { text: (brand.fictional ? 'sample brand, simulated data' : 'live brand, read-only') + ', ' + (brand.market || 'US') }));
    const approve = UI.el('a', { class: 'approve', href: '#/05-brand-brain', text: 'To approve ' });
    const n = UI.el('span', { class: 'n', text: '…' });
    approve.append(n); card.append(approve);
    UI.api('/api/05-brand-brain/master').then((m) => { n.textContent = String((m.top || []).length); }).catch(() => { approve.remove(); });
    UI.mount('#sample-strip', UI.sampleBadge(brand));
  }
  function show(slug) {
    const s = screens.find((x) => x.slug === slug) || screens[0];
    if (!s) return;
    current = s.slug;
    document.title = s.room + ' · ecomOS';
    renderNav();
    const stage = $('stage');
    stage.replaceChildren();
    if (s.built) {
      stage.append(UI.el('iframe', { src: '/screens/' + s.slug + '/', title: s.room, loading: 'eager' }));
    } else {
      const wrap = UI.el('div', { class: 'empty' });
      wrap.append(UI.sampleBadge(brand));
      wrap.append(UI.emptyState({
        title: s.room + ' is not built yet',
        text: s.purpose + '. Round 0 for this screen is a shell, an api, 3 tiles, 2 insights and 1 chart.',
        missing: ['screens/' + s.slug + '/index.html'],
        action: { label: 'See the kit demo', href: '#/kit' }
      }));
      stage.append(wrap);
    }
  }
  function showKit() {
    current = null; renderNav(); document.title = 'UI kit · ecomOS';
    UI.mount('#stage', UI.el('iframe', { src: '/web/kit.html', title: 'UI kit demo' }));
  }
  function route() {
    if (location.hash === '#/kit') return showKit();
    const slug = slugFromHash();
    show(slug || (screens[0] && screens[0].slug));
  }
  function themeLabel() {
    const t = UI.theme.get();
    $('theme-btn').textContent = 'Theme: ' + t; $('theme-btn-m').textContent = t;
  }
  function cycleTheme() {
    const order = ['auto', 'light', 'dark'];
    UI.theme.set(order[(order.indexOf(UI.theme.get()) + 1) % order.length]);
    themeLabel();
    const frame = document.querySelector('#stage iframe');
    if (frame && frame.contentWindow && frame.contentWindow.UI) frame.contentWindow.UI.theme.set(UI.theme.get());
  }

  async function init() {
    try {
      const [sc, br] = await Promise.all([UI.api('/api/screens'), UI.api('/api/brand').catch(() => null)]);
      screens = sc.screens || []; brand = br; UI.brand = br;
    } catch (e) {
      UI.mount('#stage', UI.emptyState({ title: 'The server did not answer', text: 'Start it with: python app/server.py', missing: ['/api/screens'] }));
      return;
    }
    renderBrand();
    $('screen-select').addEventListener('change', (e) => { location.hash = '#/' + e.target.value; });
    const search = $('nav-search');
    if (search) search.addEventListener('input', () => {
      const q = search.value.trim().toLowerCase();
      for (const a of document.querySelectorAll('#navlist a')) a.hidden = !!q && !a.textContent.toLowerCase().includes(q);
      for (const ph of document.querySelectorAll('#navlist .phase')) ph.hidden = !!q;
    });
    $('theme-btn').addEventListener('click', cycleTheme);
    $('theme-btn-m').addEventListener('click', cycleTheme);
    themeLabel();
    window.addEventListener('hashchange', route);
    route();
  }
  init();
})();
