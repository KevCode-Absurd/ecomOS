'use strict';
// Catalog tab: the Meta catalog for the top best sellers, a product set fix, 1-click premium photos
// for the catalog and a 5 to 15 image product story. Read-only on Meta: images are made and saved in the
// local gallery; the team uploads them. Uses catalog.json (a read-only copy of the Meta catalog for the top 100).

const CT = { data: null, made: {}, approved: {}, prompt: '', defPrompt: '', top: 50, quality: 'high', size: 'square', style: '', styles: null, storyN: 10, storySize: 'square', busy: {}, msg: {}, story: {}, open: {} };
// Same text as CATALOG_STYLES in ai.py (the local server sends its own copy).
const CT_STYLES = {
 "ivory": {
  "name": "Ivory studio",
  "prompt": "Premium studio photo of this jewellery piece for a luxury online catalog. Seamless warm ivory background with a very soft gradient, a touch lighter behind the piece. Large soft light from the top left and a gentle fill, so the gold glows with warm, true-to-life highlights and the stones catch small crisp sparkles. A soft natural contact shadow under the piece. Razor sharp focus across the whole piece, clean edges, no dust, no scratches, no colour cast. The piece is the clear hero, centred, filling about 65 to 70% of the frame, with even margins. No text, no logo, no hands, no model, no other jewellery, no watermark."
 },
 "silk": {
  "name": "Champagne silk",
  "prompt": "Luxury campaign photo of this jewellery piece resting on softly draped champagne silk with gentle folds. Warm low side light, so the gold glows and the stones sparkle. Shallow depth of field: the silk falls into a creamy blur behind the piece. Rich, warm and calm, like a high-end jewellery brand ad. Razor sharp focus across the whole piece, clean edges, no dust, no scratches, no colour cast. The piece is the clear hero, centred, filling about 65 to 70% of the frame, with even margins. No text, no logo, no hands, no model, no other jewellery, no watermark."
 },
 "stone": {
  "name": "Stone plinth",
  "prompt": "Editorial photo of this jewellery piece placed on a small honed ivory travertine block, with a warm beige plaster wall behind. Soft window light from one side and a long soft shadow. Calm, minimal and expensive, like a luxury brand's website. The block is simple and plain; the piece stays true to its real size. Razor sharp focus across the whole piece, clean edges, no dust, no scratches, no colour cast. The piece is the clear hero, centred, filling about 65 to 70% of the frame, with even margins. No text, no logo, no hands, no model, no other jewellery, no watermark."
 },
 "sunlit": {
  "name": "Sunlit shadows",
  "prompt": "Golden hour photo of this jewellery piece on a warm sand-coloured surface. Soft dappled sunlight with a blurred leaf shadow falling across the background, but the piece itself in clear, even light. Warm, fresh and natural, made to stop the scroll in a social feed. Razor sharp focus across the whole piece, clean edges, no dust, no scratches, no colour cast. The piece is the clear hero, centred, filling about 65 to 70% of the frame, with even margins. No text, no logo, no hands, no model, no other jewellery, no watermark."
 },
 "velvet": {
  "name": "Deep velvet",
  "prompt": "Dramatic luxury photo of this jewellery piece on deep emerald green velvet. Dark, rich background with a focused soft spotlight on the piece and a thin rim light, so the gold edges glow and the stones sparkle. High contrast but true colours for the metal and stones. Razor sharp focus across the whole piece, clean edges, no dust, no scratches, no colour cast. The piece is the clear hero, centred, filling about 65 to 70% of the frame, with even margins. No text, no logo, no hands, no model, no other jewellery, no watermark."
 }
};
const CT_DEFAULT_PROMPT = CT_STYLES.ivory.prompt;
const ctSlug = (p) => (p.url ? p.url.replace(/\/+$/, '').split('/').pop() : '');

async function ctBoot() {
  if (!CT.data) { try { const r = await fetch('catalog.json'); CT.data = r.ok ? await r.json() : null; } catch (e) { CT.data = null; } }
  if (!CT.prompt) {
    try { const r = await fetch('catalog_prompt.json'); const j = r.ok ? await r.json() : null; CT.prompt = (j && j.prompt) || ''; } catch (e) { CT.prompt = ''; }
  }
  if (!IS_CLAUDE) {
    await labBoot();
    try { const r = await fetch('/api/catalog-refresh'); if (r.ok) { const j = await r.json(); CT.made = j.made || {}; CT.approved = j.approved || {}; CT.defPrompt = j.default_prompt || ''; CT.styles = j.styles || null; } } catch (e) { /* offline */ }
  }
  CT.defPrompt = CT.defPrompt || CT_DEFAULT_PROMPT;
  CT.styles = CT.styles || CT_STYLES;
  if (!CT.prompt) CT.prompt = CT.defPrompt;
}
function ctCanMake() { return !IS_CLAUDE && LABST.status && LABST.status.variants; }

function ctSummary(d) {
  const ps = d.products, notSet = ps.filter((p) => !p.in_ads_set), noImg = ps.filter((p) => (p.missing_images || []).length);
  const catAds = (VIEW.collections.catalog_dynamic || { totals: {} }).totals;
  const ids = (list) => list.flatMap((p) => (p.variants && p.variants.length ? p.variants.map((v) => v.retailer_id) : [p.code]));
  CT.copyMissing = ids(notSet).join(', '); CT.copyAll = ids(ps).join(', ');
  return `<section class="panel-box"><h2>Catalog check for your best sellers</h2>
    <p class="lead">Your top ${ps.length} sellers on the website (pieces sold, last 12 months), checked against the Meta catalog "${esc(d.catalog_name)}" (${d.catalog_products.toLocaleString('en-IN')} items). Catalog ads use the product set "${esc(d.ads_set_name)}" (${d.ads_set_products.toLocaleString('en-IN')} items).</p>
    <div class="bd-kpis">
      <div class="bd-kpi"><span class="muted small">In the catalog</span><b>${ps.filter((p) => p.in_catalog).length} of ${ps.length}</b><span class="small muted">Some as size or karat versions</span></div>
      <div class="bd-kpi"><span class="muted small">In the set catalog ads use</span><b>${ps.length - notSet.length} of ${ps.length}</b><span class="rp-delta ${notSet.length ? 'bad' : 'good'}">${notSet.length} best sellers never shown by catalog ads</span></div>
      <div class="bd-kpi"><span class="muted small">Sizes with no image</span><b>${noImg.reduce((t, p) => t + p.missing_images.length, 0)}</b><span class="small muted">${esc(noImg.map((p) => p.missing_images.join(', ')).join('; ') || 'None')}</span></div>
      <div class="bd-kpi"><span class="muted small">Catalog ads in these dates</span><b>${catAds.spend ? compact(catAds.spend) : '–'}</b><span class="small muted">ROAS ${roasTxt(catAds.roas)}</span></div></div>
    ${notSet.length ? `<div class="rp-big"><b>Fix: add ${notSet.length} best sellers to the product set</b>
      <p>"${esc(d.ads_set_name)}" is a fixed list made in June 2024, so newer pieces never reach catalog ads. These sell well but are missing: ${esc(notSet.slice(0, 12).map((p) => p.name).join(', '))}${notSet.length > 12 ? ` and ${notSet.length - 12} more` : ''}.</p>
      <p>In Commerce Manager, open the set and add these IDs, or make a new set "Top 100 sellers" from all 100 and point catalog ads at it.</p>
      <div class="act-btns"><button class="btn small-btn" type="button" data-ctcopy="missing">Copy the missing IDs</button><button class="btn ghost small-btn" type="button" data-ctcopy="all">Copy all top ${ps.length} IDs</button></div></div>` : ''}
    <p class="small muted">${esc(d.source)} Catalog read ${esc(d.pulled_at)}. This page cannot change the catalog; the team makes the change.</p></section>`;
}
function ctPromptHtml() {
  const st = CT.styles || CT_STYLES, cur = CT.style || (Object.keys(st).find((k) => st[k].prompt === CT.prompt) || '');
  return `<section class="panel-box"><h2>Premium photo prompt</h2>
    <p class="lead">Used for every "Make premium photo". The piece itself is always kept exactly the same; this only changes the light, background and finish.</p>
    <div class="ct-styles" role="group" aria-label="Background style">${Object.entries(st).map(([k, v]) => `<button type="button" class="ct-st${cur === k ? ' on' : ''}" data-ctstyle="${esc(k)}">${esc(v.name)}</button>`).join('')}${cur ? '' : '<span class="ct-st on">Your own prompt</span>'}</div>
    <p class="small muted">Use Ivory studio for the main catalog photo. Use the other looks for feed ads and extra photos. Portrait 4:5 fills more of the feed.</p>
    <textarea class="pb-paste" data-ctprompt rows="4">${esc(CT.prompt)}</textarea>
    <div class="row" style="gap:10px;align-items:center;flex-wrap:wrap"><button class="btn ghost small-btn" type="button" data-ctsaveprompt>Save for the team</button><button class="linkbtn" type="button" data-ctresetprompt>Back to the default</button>
      <label class="small muted">Quality <select data-ctset="quality">${[['high', 'High'], ['medium', 'Medium'], ['low', 'Low']].map(([v, l]) => `<option value="${v}"${CT.quality === v ? ' selected' : ''}>${l}</option>`).join('')}</select></label>
      <label class="small muted">Photo size <select data-ctset="size">${[['square', 'Square 1:1'], ['portrait', 'Portrait 4:5']].map(([v, l]) => `<option value="${v}"${CT.size === v ? ' selected' : ''}>${l}</option>`).join('')}</select></label>
      <label class="small muted">Story images <select data-ctset="storyN">${[5, 10, 15].map((v) => `<option value="${v}"${CT.storyN === v ? ' selected' : ''}>${v}</option>`).join('')}</select></label>
      <label class="small muted">Story size <select data-ctset="storySize">${[['square', 'Square 1:1'], ['portrait', 'Portrait 4:5'], ['story', 'Story 9:16']].map(([v, l]) => `<option value="${v}"${CT.storySize === v ? ' selected' : ''}>${l}</option>`).join('')}</select></label>
      <span class="small muted" id="ctPromptMsg"></span></div></section>`;
}
function ctCard(p, i) {
  const made = CT.made[p.code] || [], appr = CT.approved[p.code], busy = CT.busy[p.code], can = ctCanMake();
  const cur = !IS_CLAUDE && p.image_url ? `<img src="/catalog-image/${encodeURIComponent(p.code)}" alt="Catalog photo of ${esc(p.name)}" loading="lazy">` : `<div class="noimg">${p.image_url ? 'Shown in the local gallery' : 'No catalog image'}</div>`;
  const last = made[0];
  const after = last ? `<a href="/catalog-refresh/${encodeURIComponent(p.code)}/${encodeURIComponent(last.file)}" target="_blank" rel="noopener" download><img src="/catalog-refresh/${encodeURIComponent(p.code)}/${encodeURIComponent(last.file)}" alt="Premium photo of ${esc(p.name)}"></a>` : `<div class="noimg">${busy === 'photo' ? 'Making…' : 'No new photo yet'}</div>`;
  // Newest run first; inside a run, in shot order (file names end in _1, _2, ...).
  const key = (m) => [String(m.file || '').split('_')[0], Number((String(m.file || '').match(/_(\d+)\.png$/) || [0, 0])[1])];
  const story = (CT.story[p.code] || []).slice().sort((x, y) => { const a = key(x), b = key(y); return a[0] === b[0] ? a[1] - b[1] : a[0] < b[0] ? 1 : -1; });
  return `<article class="ct-card" id="ct-${esc(p.code)}"><div class="ct-top"><span class="rankc">${i + 1}</span><div><b>${esc(p.name)}</b>
      <div class="rp-adm"><span>${esc(p.code)}</span><span>${p.sold_12m} sold in 12 months</span><span>${compact(p.sales_12m)}</span>${p.price ? `<span>₹${p.price.toLocaleString('en-IN')}</span>` : ''}</div>
      <div class="row" style="gap:6px;margin-top:4px">${p.in_ads_set ? '<span class="chip v-scale">In catalog ads</span>' : '<span class="chip v-cut">Not in catalog ads</span>'}${(p.missing_images || []).length ? `<span class="chip v-watch">${p.missing_images.length} size${p.missing_images.length > 1 ? 's' : ''} with no image</span>` : ''}${appr ? '<span class="chip good">New photo chosen</span>' : ''}</div></div></div>
    <div class="ct-pair"><figure>${cur}<figcaption>Now in the catalog</figcaption></figure><figure>${after}<figcaption>${last ? `Premium, ${esc(last.date || '')}` : 'Premium'}</figcaption></figure></div>
    <div class="act-btns">${can ? `<button class="btn small-btn" type="button" data-ctgo="photo" data-code="${esc(p.code)}" ${busy ? 'disabled' : ''}>${busy === 'photo' ? 'Making…' : last ? 'Make another' : 'Make premium photo'}</button>` : ''}
      ${last && can ? `<button class="btn ghost small-btn" type="button" data-ctapprove="${esc(p.code)}" data-file="${esc(last.file)}">${appr === last.file ? 'Chosen ✓' : 'Use this photo'}</button>` : ''}
      ${can ? `<button class="btn ghost small-btn" type="button" data-ctgo="story" data-code="${esc(p.code)}" ${busy ? 'disabled' : ''}>${busy === 'story' ? 'Making the story…' : `Make story (${CT.storyN})`}</button>` : ''}
      ${p.url ? `<a class="linkbtn" href="${esc(p.url)}" target="_blank" rel="noopener">Product page</a>` : ''}
      ${made.length > 1 ? `<button class="linkbtn" type="button" data-ctopen="${esc(p.code)}">${CT.open[p.code] ? 'Hide' : `All ${made.length} versions`}</button>` : ''}</div>
    ${!can ? `<p class="small muted">${IS_CLAUDE ? 'Photos are made in the local gallery.' : 'Image making is off on this computer.'}</p>` : ''}
    <p class="small muted" aria-live="polite">${esc(CT.msg[p.code] || '')}</p>
    ${CT.open[p.code] ? `<div class="ct-vers">${made.map((m) => `<button type="button" class="ct-ver${appr === m.file ? ' on' : ''}" data-ctapprove="${esc(p.code)}" data-file="${esc(m.file)}" title="Use this one"><img src="/catalog-refresh/${encodeURIComponent(p.code)}/${encodeURIComponent(m.file)}" alt="Version from ${esc(m.date || '')}"></button>`).join('')}</div>` : ''}
    ${story.length ? `<div class="ct-story"><h4>Product story, ${story.length} images</h4><div class="ct-sgrid">${story.map((m) => (m.error ? `<figure class="vcard err"><b>${esc(m.label)}</b><span>${esc(m.error)}</span></figure>` : `<figure><a href="/product-story/${esc(ctSlug(p))}/${esc(m.file)}" target="_blank" rel="noopener" download><img src="/product-story/${esc(ctSlug(p))}/${esc(m.file)}" alt="${esc(m.label)}" loading="lazy"></a><figcaption>${esc(m.label)}</figcaption></figure>`)).join('')}</div></div>` : ''}
  </article>`;
}
window.renderCatalog = async function renderCatalog() {
  const v = $('catalogView');
  if (!CT.data) v.innerHTML = '<p class="loading">Loading the catalog…</p>';
  await ctBoot();
  if (!CT.data) { v.innerHTML = '<p class="muted">catalog.json is missing. Pull the catalog first.</p>'; return; }
  const ps = CT.data.products.slice(0, CT.top);
  const chosen = Object.keys(CT.approved).length;
  v.innerHTML = `<div class="ins">${ctSummary(CT.data)}${ctPromptHtml()}
    <section class="panel-box"><div class="bd-head"><div><h2>Best sellers in the catalog</h2><p class="lead">Current catalog photo next to a premium version. Pick the one you like; the chosen photos go into a list you upload.</p></div>
      <div class="row" style="gap:8px;align-items:center"><div class="seg" role="group" aria-label="How many">${[25, 50, 100].map((n) => `<button type="button" data-cttop="${n}" aria-pressed="${CT.top === n}">Top ${n}</button>`).join('')}</div>
      ${!IS_CLAUDE ? `<a class="btn ghost small-btn" href="/api/catalog-export.csv" download="catalog-new-photos.csv">Download chosen (${chosen})</a>` : ''}</div></div>
      <div class="ct-grid">${ps.map(ctCard).join('')}</div>
      <p class="small muted">To use a new photo: host the file (for example on the Gehna CDN), then add it as the image link in a supplementary feed or in Commerce Manager. The list has each catalog ID and its new file.</p></section></div>`;
  if (!IS_CLAUDE) for (const p of ps) if (!CT.story[p.code] && p.url) loadStory(p);
};
async function loadStory(p) {
  try { const r = await fetch('/api/product-story/' + encodeURIComponent(ctSlug(p))); if (r.ok) { const j = await r.json(); if (j.length) { CT.story[p.code] = j; ctRerender(p.code); } } } catch (e) { /* none */ }
}
function ctRerender(code) {
  const el = $('ct-' + code), p = CT.data.products.find((x) => x.code === code);
  if (el && p) el.outerHTML = ctCard(p, CT.data.products.indexOf(p));
}
async function ctRun(code, what) {
  const p = CT.data.products.find((x) => x.code === code);
  CT.busy[code] = what; CT.msg[code] = what === 'photo' ? 'Making a premium photo. About 1 minute.' : `Making ${CT.storyN} story images from the website photos and facts. A few minutes; you can keep browsing.`;
  ctRerender(code);
  try {
    const url = what === 'photo' ? '/api/catalog-premium' : '/api/product-story';
    const body = what === 'photo' ? { code, prompt: CT.prompt, quality: CT.quality, size: CT.size } : { code, n: CT.storyN, size: CT.storySize, quality: CT.quality === 'high' ? 'medium' : CT.quality };
    const r = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
    const j = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(j.error || 'Something went wrong.');
    if (what === 'photo') { CT.made[code] = j.all; CT.msg[code] = j.made.error ? j.made.error : 'Done. Compare the two and pick one.'; }
    else { CT.story[code] = j.all; const bad = j.made.filter((m) => m.error); CT.msg[code] = bad.length ? `${j.made.length - bad.length} of ${j.made.length} made. ${bad[0].error}` : `${j.made.length} story images made. Click one to download.`; }
  } catch (e) { CT.msg[code] = e.message; }
  delete CT.busy[code];
  ctRerender(code);
}
document.addEventListener('click', async (e) => {
  const v = $('catalogView');
  if (!v || v.hidden || !v.contains(e.target)) return;
  const b = (s) => e.target.closest(s);
  let x;
  if ((x = b('[data-cttop]'))) { CT.top = Number(x.dataset.cttop); window.renderCatalog(); return; }
  if ((x = b('[data-ctgo]'))) { ctRun(x.dataset.code, x.dataset.ctgo); return; }
  if ((x = b('[data-ctopen]'))) { CT.open[x.dataset.ctopen] = !CT.open[x.dataset.ctopen]; ctRerender(x.dataset.ctopen); return; }
  if ((x = b('[data-ctapprove]'))) {
    const code = x.dataset.ctapprove, file = CT.approved[code] === x.dataset.file ? null : x.dataset.file;
    try { const r = await fetch('/api/catalog-approve', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ code, file }) }); const j = await r.json(); if (r.ok) CT.approved = j.approved; } catch (err) { /* offline */ }
    ctRerender(code); return;
  }
  if ((x = b('[data-ctcopy]'))) { try { await navigator.clipboard.writeText(x.dataset.ctcopy === 'all' ? CT.copyAll : CT.copyMissing); x.textContent = 'Copied'; } catch (err) { x.textContent = 'Copy blocked here'; } return; }
  const sb = b('[data-ctstyle]');
  if (sb) { const st = CT.styles || CT_STYLES, k = sb.dataset.ctstyle; if (st[k]) { CT.style = k; CT.prompt = st[k].prompt; renderCatalog(); } return; }
  if (b('[data-ctresetprompt]')) { CT.style = ''; CT.prompt = CT.defPrompt; const t = v.querySelector('[data-ctprompt]'); if (t) t.value = CT.prompt; return; }
  if (b('[data-ctsaveprompt]')) { await docsBoot(); const m = await saveDoc('catalog_prompt.json', { prompt: CT.prompt, updated: new Date().toISOString().slice(0, 10) }); const el = $('ctPromptMsg'); if (el) el.textContent = m; }
});
document.addEventListener('input', (e) => { if (e.target.matches && e.target.matches('[data-ctprompt]')) { CT.prompt = e.target.value.slice(0, 2000); CT.style = ''; } });
document.addEventListener('change', (e) => {
  const s = e.target.closest && e.target.closest('[data-ctset]');
  if (!s) return;
  CT[s.dataset.ctset] = s.dataset.ctset === 'storyN' ? Number(s.value) : s.value;
  window.renderCatalog();
});
