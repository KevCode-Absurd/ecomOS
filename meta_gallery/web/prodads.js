'use strict';
// Top 5 sellers: test number 1 in "Tests to run this week", with an ad builder on each product.
// Sales come from Metabase (sales.json: daily, plus sku_daily for older days).
// Locally, the server loads the product's photos from gehnaindia.com and makes images and copy.
// On the shared page, Claude writes the copy and image briefs (no image making there).
// Uses sales.js (SL, baseCode, cleanName, typeCat, inAds, dailyDays, addDays, dateLabel), lab.js (askAI, REF, refSlotHtml, thumbBlob, aiErr) and studio.js (baseAds).

const PB = { days: 30, by: 'n', showHidden: {}, closed: {}, open: null, info: {}, opt: {}, busy: {}, res: {}, msg: {} };
const PB_SIZES = [['square', 'Square 1:1'], ['portrait', 'Portrait 4:5'], ['story', 'Story 9:16']];
const PB_Q = [['low', 'Low (fast)'], ['medium', 'Medium'], ['high', 'High']];
const PB_SITE = 'https://www.gehnaindia.com/';
const pbSlug = (name) => String(name || '').toLowerCase().replace(/&/g, ' ').replace(/\(.*?\)/g, ' ').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

// Days with product sales: daily entries first, then the older SKU-only days.
function pbSkuDays() {
  const out = {};
  for (const [d, rows] of Object.entries((SL.data && SL.data.sku_daily) || {})) out[d] = rows;
  for (const [d, x] of Object.entries((SL.data && SL.data.daily) || {})) out[d] = x.skus || [];
  return out;
}
function topProducts(days) {
  const all = pbSkuDays(), keys = Object.keys(all).sort();
  if (!keys.length) return null;
  const until = keys[keys.length - 1], want = addDays(until, -(days - 1)), since = want < keys[0] ? keys[0] : want;
  const map = {};
  let total = 0, n = 0;
  for (const d of keys) {
    if (d < since || d > until) continue;
    n += 1;
    for (const [metal, code, name, v, c] of all[d]) {
      const b = baseCode(code);
      const o = map[b] || (map[b] = { code: b, fullCode: code, name: cleanName(name), metal, v: 0, n: 0 });
      o.v += v || 0; o.n += c || 0; total += v || 0;
      if (!/14K/.test(name) && o.name.includes('14K')) { o.name = cleanName(name); o.fullCode = code; }
    }
  }
  const list = Object.values(map).filter((o) => o.v > 0).sort((a, b) => (PB.by === 'n' ? b.n - a.n || b.v - a.v : b.v - a.v || b.n - a.n)).slice(0, 5)
    .map((o) => ({ ...o, avg: o.n ? o.v / o.n : null, cat: typeCat(o.name), inAds: inAds(o.name), share: total ? o.v / total : null }));
  return { list, since, until, days: n, short: want < keys[0], total };
}
// Best image ads to borrow a style from: same category first, then the account's best by ROAS.
function pbRefAds(cat) {
  // Sale and countdown ads are left out: their look is the offer, not a style to reuse.
  const SALE = /\b(sale|eoss|% ?off|off on|discount|offer|coupon|hours left|days left|last \d+ (days|hours)|flat \d+)/i;
  const sale = (id) => { const a = ENGINE.c.ads[id] || DATA.ads[id] || {}, c = a.creative || {};
    return (VIEW.ads[id].tags && VIEW.ads[id].tags.angle.code === 'offer') || SALE.test([a.name, c.name, c.headline, c.primary_text].join(' ')); };
  const all = ((VIEW.collections.static_image || {}).ad_ids || []).filter((id) => VIEW.ads[id] && VIEW.ads[id].view.metrics.roas !== null && VIEW.ads[id].view.metrics.purchases >= 1);
  const ids = all.filter((id) => !sale(id)).length ? all.filter((id) => !sale(id)) : all;
  const by = (l) => l.sort((a, b) => VIEW.ads[b].view.metrics.roas - VIEW.ads[a].view.metrics.roas);
  const inCat = by(ids.filter((id) => adCat(ENGINE.c.ads[id] || DATA.ads[id]) === cat));
  const rest = by(ids.filter((id) => !inCat.includes(id)));
  return [...inCat, ...rest].slice(0, 4);
}
function pbOpt(p) {
  if (!PB.opt[p.code]) { const refs = pbRefAds(p.cat); PB.opt[p.code] = { n: 4, size: 'square', quality: 'medium', ref: refs.length ? 'ad' : 'none', refAd: refs[0] || null, picks: [1, 2], off: [], paste: '' }; }
  return PB.opt[p.code];
}
function pbFind(code) { const t = topProducts(PB.days); return t ? t.list.find((p) => p.code === code) : null; }
function soldLine(p) { return `${p.n} sold in the last ${PB.days} days on the website (${compact(p.v)}), number ${PB.top ? PB.top.list.findIndex((q) => q.code === p.code) + 1 : 1} by ${PB.by === 'n' ? 'pieces sold' : 'sales value'}`; }

// ---------- batches and hidden ads ----------
// Each result carries a batch id and a key. New batches go on top; older ones stay below.
// Hidden ads are remembered in this browser only (they are not deleted).
const PB_HIDE_KEY = 'ecomos.pb.hidden';
let PB_HIDDEN = new Set();
try { PB_HIDDEN = new Set(JSON.parse(localStorage.getItem(PB_HIDE_KEY) || '[]')); } catch (e) { PB_HIDDEN = new Set(); }
function pbSaveHidden() { try { localStorage.setItem(PB_HIDE_KEY, JSON.stringify([...PB_HIDDEN].slice(-2000))); } catch (e) { /* private mode */ } }
function pbStamp() { const d = new Date(), z = (n) => String(n).padStart(2, '0'); return `${d.getFullYear()}${z(d.getMonth() + 1)}${z(d.getDate())}-${z(d.getHours())}${z(d.getMinutes())}${z(d.getSeconds())}`; }
function pbBatchLabel(id) {
  const m = /^(?:copy-)?(\d{4})(\d{2})(\d{2})-(\d{2})(\d{2})/.exec(id || '');
  if (!m) return 'Earlier';
  const d = new Date(Date.UTC(+m[1], +m[2] - 1, +m[3]));
  return `${d.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', timeZone: 'UTC' })}, ${m[4]}:${m[5]}`;
}
// Tag results with batch and key. Server images: batch = file name stamp, key = code + file.
function pbTag(p, list, batch) {
  return (list || []).map((c, i) => {
    const b = c.file ? c.file.split('_')[0] : batch;
    return { ...c, batch: b, key: `${p.code}|${c.file || `${b}_${i}`}` };
  });
}
function pbAdd(p, list) { PB.res[p.code] = [...list, ...(PB.res[p.code] || []).filter((c) => !list.some((n) => n.key === c.key))]; PB.closed[p.code] = false; }

// ---------- the card ----------
window.top5CardHtml = function top5CardHtml() {
  const t = topProducts(PB.days);
  PB.top = t;
  if (!t || !t.list.length) return '';
  const top = t.list, sum = top.reduce((a, p) => a + p.v, 0), noAd = top.filter((p) => p.inAds === false).length;
  const perDay = r100(Math.max(1000, (metaRange(t.since, t.until).spend / Math.max(1, t.days)) * 0.04));
  return `<article class="tcard pb" id="pb-card" data-test-id="top5">
    <div class="tc-head"><span class="tc-rank">1</span><div><div class="row" style="gap:6px"><span class="chip fmt">Product</span><span class="chip v-scale">Strong</span></div><h3>Build new ads for your 5 best sellers</h3></div></div>
    <div class="row pb-bar"><div class="seg" role="group" aria-label="Sales window">${[30, 60].map((d) => `<button type="button" data-pbdays="${d}" aria-pressed="${PB.days === d}">Last ${d} days</button>`).join('')}</div>
      <div class="seg" role="group" aria-label="Rank by">${[['n', 'Pieces sold'], ['v', 'Sales value']].map(([k, l]) => `<button type="button" data-pbby="${k}" aria-pressed="${PB.by === k}">${l}</button>`).join('')}</div>
      <span class="small muted">Website sales ${esc(dateLabel(t.since))} to ${esc(dateLabel(t.until))}${t.short ? `, ${t.days} days with data` : ''}.</span></div>
    <div class="tc-cols"><div><h4>Why</h4><ul><li>These 5 pieces made ${compact(sum)}, ${pc(t.total ? sum / t.total : null)} of product sales in this window.</li>
      <li>${noAd ? `${noAd} of them ${noAd === 1 ? 'has' : 'have'} no ad naming ${noAd === 1 ? 'it' : 'them'}. People buy them anyway.` : 'Each has at least 1 ad that names it. Fresh creative keeps them selling.'}</li>
      <li>Proven demand is the cheapest place to test new creative.</li></ul></div>
      <div><h4>The test</h4><ul><li>Pick a piece and press Build creative. Use its site photos and the style of your best image ad.</li><li>Launch 3 to 4 new ads per piece in 1 ad set, so they compete for the same budget.</li><li>Change nothing else in the account while it runs.</li></ul></div></div>
    <div class="pb-list">${top.map((p, i) => pbRowHtml(p, i)).join('')}</div>
    <dl class="tc-rules"><div><dt>Budget and time</dt><dd>${money(perDay)} a day per piece for 7 days.</dd></div>
      <div><dt>Win if</dt><dd>A new ad beats ROAS ${roasTxt(VIEW.targets.roas)}, or the piece sells faster than its usual pace.</dd></div>
      <div><dt>Stop if</dt><dd>An ad spends 2x your target cost per purchase with no sale.</dd></div></dl>
  </article>`;
};
function pbRowHtml(p, i) {
  const open = PB.open === p.code;
  return `<div class="pb-item${open ? ' open' : ''}" data-pbcode="${esc(p.code)}">
    <div class="pb-row"><span class="rankc">${i + 1}</span>
      <span class="pb-nm"><span class="nm">${esc(p.name)}</span><span class="mt">${esc(p.code)} · ${esc(p.cat)} · about ${compact(p.avg)} each · ${p.inAds === false ? '<b class="pb-noad">No ad names it</b>' : p.inAds ? 'Named in ads' : 'Ad match unclear'}</span></span>
      <span class="pb-num"><b>${p.n} sold</b><span class="mt">${compact(p.v)}</span></span>
      <button class="btn${open ? ' ghost' : ''} small-btn" type="button" data-pbopen="${esc(p.code)}" aria-expanded="${open}">${open ? 'Close' : 'Build creative'}</button></div>
    ${open ? `<div class="pb-build" id="pb-build">${pbBuildHtml(p)}</div>` : ''}
  </div>`;
}

// ---------- the builder ----------
const PB_GROUPS = [['product', 'The piece'], ['price', 'Price and EMI'], ['delivery', 'Delivery'], ['proof', 'Proof'], ['trust', 'Promises on every page'], ['faq', 'FAQ on the page'], ['review', 'Customer words'], ['story', 'Story']];
function pbFacts(p) {
  const info = PB.info[p.code];
  return info && info.status === 'ok' ? info.product.facts || [] : [];
}
function pbChosenFacts(p) {
  const o = pbOpt(p);
  if (IS_CLAUDE) return o.paste.trim() ? [o.paste.trim().slice(0, 6000)] : [];
  return pbFacts(p).filter((f, i) => !o.off.includes(i)).map((f) => f.text);
}
function pbFactsHtml(p) {
  const o = pbOpt(p), url = PB_SITE + pbSlug(p.name);
  if (IS_CLAUDE) {
    return `<div class="pb-sec"><h4>Page facts</h4><p class="small muted">The shared page cannot read the website. Open <a href="${esc(url)}" target="_blank" rel="noopener">the product page</a>, select all (Ctrl+A), copy and paste it here. Claude uses only what you paste. The local gallery pulls this for you.</p>
      <textarea class="pb-paste" data-pbpaste rows="4" placeholder="Paste the product page text here">${esc(o.paste)}</textarea></div>`;
  }
  const facts = pbFacts(p);
  if (!facts.length) return '';
  const on = facts.length - o.off.length;
  return `<div class="pb-sec"><h4>Page facts <span class="muted small">${on} of ${facts.length} ticked. Untick anything you do not want in the ads. The AI builds each ad on different facts and may use only these.</span></h4>
    <div class="pb-facts">${PB_GROUPS.map(([g, label]) => {
      const rows = facts.map((f, i) => [f, i]).filter(([f]) => f.group === g);
      return rows.length ? `<div class="pb-fg"><span class="pb-fgl">${label}</span>${rows.map(([f, i]) => `<label class="pb-fact"><input type="checkbox" data-pbfact="${i}" ${o.off.includes(i) ? '' : 'checked'}><span>${esc(f.text)}</span></label>`).join('')}</div>` : '';
    }).join('')}</div>
    <div class="row" style="gap:8px"><button class="linkbtn" type="button" data-pbfacts="all">Tick all</button><button class="linkbtn" type="button" data-pbfacts="none">Untick all</button><button class="linkbtn" type="button" data-pbfacts="refresh">Pull again from the site</button></div></div>`;
}
function pbPhotosHtml(p) {
  const url = PB_SITE + pbSlug(p.name);
  if (IS_CLAUDE) {
    return `<div class="pb-sec"><h4>Product photos</h4><p class="small muted">The shared page cannot load photos from the website. Here Claude writes the copy and image briefs. Open the local gallery to make the images from the <a href="${esc(url)}" target="_blank" rel="noopener">site photos</a>.</p></div>`;
  }
  const info = PB.info[p.code];
  if (!info || info.status === 'loading') return `<div class="pb-sec"><h4>From the website</h4><p class="small muted">Pulling photos and facts from gehnaindia.com…</p></div>`;
  if (info.status === 'error') return `<div class="pb-sec"><h4>Product photos</h4><p class="small bad-text">${esc(info.error)}</p><p class="small muted">You can still write copy, or <a href="${esc(url)}" target="_blank" rel="noopener">check the page</a>.</p></div>`;
  const pr = info.product, o = pbOpt(p);
  return `<div class="pb-sec"><h4>Product photos <span class="muted small">from <a href="${esc(pr.url)}" target="_blank" rel="noopener">the product page</a>, pulled ${esc(pr.fetched || '')}. Pick up to 3.</span></h4>
    ${pr.code_match === false ? `<p class="small bad-text">The page shows code ${esc(pr.code)}, not ${esc(p.code)}. Check it is the same piece before you use these.</p>` : ''}
    <div class="pb-photos">${pr.photos.map((ph, i) => `<label class="pb-ph${o.picks.includes(i + 1) ? ' on' : ''}"><input type="checkbox" data-pbpick="${i + 1}" ${o.picks.includes(i + 1) ? 'checked' : ''}><img src="${esc(ph.src)}" alt="Site photo ${i + 1} of ${esc(pr.name)}"></label>`).join('') || '<span class="small muted">No photos on the page.</span>'}</div>
    </div>`;
}
function pbRefHtml(p) {
  const o = pbOpt(p), refs = pbRefAds(p.cat);
  const opt = (v, l) => `<button type="button" data-pbref="${v}" aria-pressed="${o.ref === v}">${l}</button>`;
  return `<div class="pb-sec"><h4>Style reference</h4>
    <div class="seg" role="group" aria-label="Style reference">${refs.length ? opt('ad', 'Your best image ad') : ''}${opt('paste', 'Paste an image')}${opt('none', 'None')}</div>
    ${o.ref === 'ad' ? `<div class="pb-refads">${refs.map((id) => { const a = VIEW.ads[id], m = a.view.metrics; return `<button type="button" class="base-card${id === o.refAd ? ' on' : ''}" data-pbrefad="${esc(id)}" aria-pressed="${id === o.refAd}"><span class="bc-th">${thumbHtml(id, a.name)}</span><span class="small"><b>ROAS ${roasTxt(m.roas)}</b> · ${m.purchases} sales</span><span class="mt small">${esc(adCat(ENGINE.c.ads[id] || DATA.ads[id]))}</span></button>`; }).join('')}</div><p class="small muted">Layout, framing and mood only. The piece always comes from the product. Picked from image ads with a sale in the dates above, sale ads left out.${refs.length < 3 ? ' Widen the dates to see more.' : ''}</p>` : ''}
    ${o.ref === 'paste' ? `${refSlotHtml('Style reference')}<p class="small muted" data-refmsg></p>` : ''}</div>`;
}
function pbBuildHtml(p) {
  const o = pbOpt(p), busy = PB.busy[p.code];
  const sel = (key, list) => `<select data-pbset="${key}">${list.map(([v, l]) => `<option value="${v}"${String(o[key]) === String(v) ? ' selected' : ''}>${l}</option>`).join('')}</select>`;
  const canImg = !IS_CLAUDE && LABST.status && LABST.status.variants;
  return `${pbPhotosHtml(p)}${pbFactsHtml(p)}${pbRefHtml(p)}
    <div class="pb-sec"><h4>Options</h4><div class="row pb-opts">
      <label>Number of ads ${sel('n', [[1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5']])}</label>
      <label>Format ${sel('size', PB_SIZES)}</label>
      ${IS_CLAUDE ? '' : `<label>Quality ${sel('quality', PB_Q)}</label>`}</div></div>
    <div class="act-btns">${canImg ? `<button class="btn" type="button" data-pbgo="images" ${busy ? 'disabled' : ''}>${busy === 'images' ? 'Making…' : `Make ${o.n} ad${o.n > 1 ? 's' : ''} with copy`}</button>` : ''}
      <button class="btn${canImg ? ' ghost' : ''}" type="button" data-pbgo="copy" ${busy ? 'disabled' : ''}>${busy === 'copy' ? 'Writing…' : canImg ? 'Write copy only' : 'Write copy and image briefs'}</button></div>
    ${!IS_CLAUDE && !canImg ? '<p class="small muted">Image making is off on this computer. Copy still works.</p>' : ''}
    <p class="small muted" id="pb-msg" aria-live="polite">${esc(PB.msg[p.code] || '')}</p>
    <div class="pb-res">${pbResultsHtml(p)}</div>`;
}
function pbCopyBlock(c) {
  const row = (label, v) => (v ? `<div class="pb-cp"><span class="muted small">${label}</span><p>${esc(v).replace(/\n/g, '<br>')}</p><button class="linkbtn" type="button" data-pbcopy="${esc(v)}">Copy</button></div>` : '');
  const alts = (label, l) => (Array.isArray(l) ? l : []).map((v, i) => row(`${label} option ${i + 2}`, v)).join('');
  return row('Primary text', c.primary_text) + alts('Primary text', c.primary_alt) + row('Headline', c.headline) + alts('Headline', c.headline_alt) + row('Description', c.description);
}
function pbResultsHtml(p) {
  const all = PB.res[p.code] || [];
  if (!all.length) return '';
  const hidden = all.filter((c) => PB_HIDDEN.has(c.key)).length, show = PB.showHidden[p.code];
  const list = all.filter((c) => show || !PB_HIDDEN.has(c.key));
  const batches = [...new Set(list.map((c) => c.batch))];
  const bar = `<div class="row pb-resbar"><b>${all.length - hidden} ad${all.length - hidden === 1 ? '' : 's'} for this piece</b>${batches.length > 1 ? `<span class="muted small">in ${batches.length} batches, newest first</span>` : ''}
    <button class="linkbtn" type="button" data-pbclose>${PB.closed[p.code] ? 'Show ads' : 'Close ads'}</button>
    ${hidden ? `<button class="linkbtn" type="button" data-pbshowhidden>${show ? 'Leave hidden ads out' : `Show ${hidden} hidden`}</button>` : ''}</div>`;
  if (PB.closed[p.code]) return bar;
  return bar + batches.map((bt) => {
    const items = list.map((c, i) => [c, all.indexOf(c)]).filter(([c]) => c.batch === bt);
    const open = items.filter(([c]) => !PB_HIDDEN.has(c.key));
    return `<section class="pb-batch"><div class="row pb-bhead"><span class="small"><b>${bt && bt.startsWith('copy-') ? 'Copy' : 'Batch'}</b> · ${esc(pbBatchLabel(bt))} · ${items.length} ad${items.length === 1 ? '' : 's'}</span>${open.length ? `<button class="linkbtn" type="button" data-pbhidebatch="${esc(bt)}">Hide this batch</button>` : ''}</div>
      <div class="pb-grid">${items.map(([c, i]) => pbAdHtml(c, i)).join('')}</div></section>`;
  }).join('') + '<p class="small muted">Check each image against the real piece before launch. Launch them yourself in Ads Manager. This page never changes the ad account. Hidden ads stay saved; they are only hidden in this browser.</p>';
}
function pbAdHtml(c, i) {
  const isHidden = PB_HIDDEN.has(c.key);
  const x = `<button class="pb-x" type="button" data-pbhide="${esc(c.key)}" aria-label="${isHidden ? 'Show this ad again' : 'Hide this ad'}" title="${isHidden ? 'Show again' : 'Hide'}">${isHidden ? '↺' : '×'}</button>`;
  return (() => {
    if (c.error && !c.headline) return `<figure class="vcard err pb-ad${isHidden ? ' is-hidden' : ''}">${x}<b>${esc(c.label || c.name || 'Ad ' + (i + 1))}</b><span>${esc(c.error)}</span></figure>`;
    const img = c.src ? `<a href="${esc(c.src)}" target="_blank" rel="noopener" download><img src="${esc(c.src)}" alt="${esc(c.label || c.name)}"></a>` : '';
    const all = [c.primary_text, ...(c.primary_alt || []).map((v, j) => `\nPrimary text ${j + 2}:\n${v}`), '', 'Headline: ' + (c.headline || ''),
      ...(c.headline_alt || []).map((v, j) => `Headline ${j + 2}: ${v}`), 'Description: ' + (c.description || '')].join('\n');
    return `<figure class="vcard pb-ad${isHidden ? ' is-hidden' : ''}">${x}${img}<figcaption><div class="row" style="gap:6px"><b>${esc(c.label || c.name || 'Ad ' + (i + 1))}</b>${c.angle ? `<span class="chip fmt">${esc(c.angle)}</span>` : ''}</div>
      ${c.error ? `<span class="small bad-text">Image failed: ${esc(c.error)}</span>` : ''}
      ${!c.src ? `<p class="small"><b>Image brief:</b> ${esc([c.idea, c.scene, c.layout].filter(Boolean).join(' '))}</p>` : `<p class="small muted">${esc(c.idea || '')}</p>`}
      ${c.text_on_image ? `<p class="small"><b>On the image:</b> ${esc(c.text_on_image)}</p>` : ''}
      ${Array.isArray(c.uses) && c.uses.length ? `<p class="small pb-uses"><b>Built on:</b> ${c.uses.map((u) => `<span class="chip">${esc(u)}</span>`).join(' ')}</p>` : ''}
      ${pbCopyBlock(c)}
      <div class="act-btns"><button class="btn ghost small-btn" type="button" data-pbcopy="${esc(all)}">Copy all</button><button class="btn ghost small-btn" type="button" data-pbtrack="${i}">Add to tests</button></div></figcaption></figure>`;
  })();
}

// Keep in sync with product_prompt in meta_gallery/ai.py (shared page only; the local server builds its own).
const PB_SHAPE = `{"concepts": [
  {"name": "2 to 4 word concept name",
   "angle": "the selling angle in a few words, for example proof it sells, gifting, everyday wear, price, craft",
   "idea": "the ad idea in 1 sentence",
   "scene": "what the photo shows: setting, model or no model, props, light",
   "layout": "where product, text and proof sit",
   "text_on_image": "exact short text to print on the image, or empty",
   "uses": ["the page facts this ad is built on, copied short"],
   "primary_text": "Meta primary text: 2 to 4 short lines",
   "primary_alt": ["2 more primary texts that test other page facts"],
   "headline": "Meta headline, 40 characters or less",
   "headline_alt": ["2 more headlines, 40 characters or less"],
   "description": "Meta link description, 30 characters or less"}
]}`;
function pbPrompt(p, o, hasRef) {
  const facts = pbChosenFacts(p);
  const size = { square: '1024x1024', portrait: '1024x1280', story: '1024x1824' }[o.size];
  return 'You are a creative director and copywriter for Meta ads at Gehna, an Indian fine jewellery brand. '
    + `Write ${o.n} ad concepts for 1 best-selling piece, each with its own Meta copy.\n\n`
    + 'No product photo is attached; describe the piece only from the facts. '
    + (hasRef ? 'Image 1 is a style reference: borrow its layout, framing, text style and mood only. Never copy its product, text, logo, models or faces.\n' : '\n')
    + `Format: ${o.size} (${size}).\n\n`
    + `Product: ${p.name}\nCode: ${p.code}\nWebsite sales (context for you, not a claim for the ads): ${soldLine(p)}\n`
    + (p.avg ? `Average price paid: Rs ${Math.round(p.avg).toLocaleString('en-IN')}\n` : '')
    + (facts.length ? `Text pasted from the product page (the only claims you may use; ignore other products, menus and reviewer names on it):\n${facts.join('\n')}\n` : '')
    + '\nMake each concept test a different angle, and build each one on a different group of page facts: 1 close to a clean product ad, '
    + 'then for example craft and stones, trust (hallmark, exchange, returns), reviews and ratings, price and EMI, fast delivery, gifting '
    + 'or worn on the body. Pick the angles the facts support best. Quote customer words only without names.\n'
    + 'Rules: the piece shown is always this exact piece. Use only facts given here: never invent discounts, ratings, '
    + 'certifications, stock claims or delivery promises. A price may be used only as given. Copy: plain short sentences, '
    + 'digits for numbers, no em dashes, no hashtags, at most 1 emoji in primary text, and no words like elevate, timeless or stunning. '
    + 'Headlines and names in sentence case, never Title Case. Never claim a rank like number 1 or best seller unless a page fact says it.\n\n'
    + `Brand kit (JSON):\n${JSON.stringify(BRAND || {}).slice(0, 4000)}\n\n`
    + `Reply with only this JSON:\n${PB_SHAPE}`;
}
function pbClean(list, n) {
  const s = (v, m) => String(v ?? '').replace(/[\u0000-\u0009\u000b-\u001f\u007f]/g, ' ').trim().slice(0, m);
  return (Array.isArray(list) ? list : []).slice(0, n).filter((c) => c && s(c.idea, 400))
    .map((c) => ({ name: s(c.name, 80), angle: s(c.angle, 80), idea: s(c.idea, 400), scene: s(c.scene, 400), layout: s(c.layout, 400), text_on_image: s(c.text_on_image, 200),
      primary_text: s(c.primary_text, 700), headline: s(c.headline, 60), description: s(c.description, 60),
      primary_alt: (Array.isArray(c.primary_alt) ? c.primary_alt : []).slice(0, 2).map((x) => s(x, 700)).filter(Boolean),
      headline_alt: (Array.isArray(c.headline_alt) ? c.headline_alt : []).slice(0, 2).map((x) => s(x, 60)).filter(Boolean),
      uses: (Array.isArray(c.uses) ? c.uses : []).slice(0, 6).map((x) => s(x, 160)).filter(Boolean) }));
}

async function pbLoadInfo(p, refresh) {
  if (IS_CLAUDE || (!refresh && PB.info[p.code] && PB.info[p.code].status !== 'error')) return;
  PB.info[p.code] = { status: 'loading' };
  pbOpt(p).off = [];
  pbRerender();
  try {
    const r = await fetch(`/api/product?name=${encodeURIComponent(p.name)}&code=${encodeURIComponent(p.fullCode || p.code)}${refresh ? '&refresh=1' : ''}`);
    const j = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(j.error || 'Could not load the product page.');
    PB.info[p.code] = { status: 'ok', product: j.product };
    const o = pbOpt(p);
    o.picks = o.picks.filter((i) => i <= j.product.photos.length);
    if (!o.picks.length && j.product.photos.length) o.picks = [1];
    if (!PB.res[p.code] || !PB.res[p.code].length) PB.res[p.code] = pbTag(p, (j.ads || []).map((m) => ({ ...m, name: m.label, src: `/product-ads/${j.product.slug}/${m.file}` })));
  } catch (e) { PB.info[p.code] = { status: 'error', error: e.message }; }
  pbRerender();
}
async function pbRun(p, mode) {
  const o = pbOpt(p);
  PB.busy[p.code] = mode; PB.msg[p.code] = mode === 'images' ? `Planning ${o.n} ideas with copy, then making the images. About 1 to 3 minutes. You can keep browsing.` : 'Writing copy…';
  pbRerender();
  const refB64 = o.ref === 'paste' && REF.b64 ? REF.b64 : null, refAd = o.ref === 'ad' ? o.refAd : null;
  try {
    if (IS_CLAUDE) {
      await labBoot(); await docsBoot();
      if (!LABST.sample) throw { code: 'unavailable', message: 'Sign in to Claude to use this.' };
      const caps = await LABST.sample.limits().catch(() => null);
      const img = caps && caps.images ? (refB64 ? refBlob() : refAd ? thumbBlob(refAd) : null) : null;
      const out = await LABST.sample.json(pbPrompt(p, o, !!img), { modelTier: 'default', cache: false, ...(img ? { images: img } : {}) });
      const got = pbTag(p, pbClean(out && out.concepts, o.n), 'copy-' + pbStamp());
      pbAdd(p, got);
      PB.msg[p.code] = got.length ? `${got.length} ideas with copy added on top. Make the images in the local gallery, or brief a designer.` : 'No ideas came back. Try again.';
    } else {
      const body = { name: p.name, code: p.fullCode || p.code, picks: o.picks, facts: pbFacts(p).length ? pbChosenFacts(p) : null, n: o.n, size: o.size, quality: o.quality, ref_image: refB64, ref_ad_id: refAd, sold: soldLine(p), copy_only: mode === 'copy' };
      const r = await fetch('/api/product-ads', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
      const j = await r.json().catch(() => ({}));
      if (!r.ok) throw new Error(j.error || 'Something went wrong. Try again.');
      if (mode === 'copy') { pbAdd(p, pbTag(p, j.copy, 'copy-' + pbStamp())); PB.msg[p.code] = `${j.copy.length} ideas with copy added on top.`; }
      else {
        pbAdd(p, pbTag(p, j.made.map((m) => ({ ...m, name: m.label, src: m.file ? `/product-ads/${j.slug}/${m.file}` : '' })), pbStamp()));
        const bad = j.made.filter((m) => m.error);
        PB.msg[p.code] = bad.length ? `${j.made.length - bad.length} of ${j.made.length} images made. ${bad[0].error}` : `${j.made.length} ads made and added on top. Click an image to download it.`;
      }
    }
  } catch (e) { PB.msg[p.code] = aiErr(e); }
  delete PB.busy[p.code];
  pbRerender();
}
function pbRerender() {
  const card = $('pb-card');
  if (!card) return;
  const y = window.scrollY;
  card.outerHTML = window.top5CardHtml();
  window.scrollTo(0, y);
}
window.pbRerender = pbRerender;

document.addEventListener('click', async (e) => {
  if (!e.target.closest('#pb-card')) return;
  const b = (sel) => e.target.closest(sel);
  let x;
  if ((x = b('[data-pbdays]'))) { PB.days = Number(x.dataset.pbdays); PB.open = null; pbRerender(); return; }
  if ((x = b('[data-pbby]'))) { PB.by = x.dataset.pbby; PB.open = null; pbRerender(); return; }
  if ((x = b('[data-pbopen]'))) {
    const code = x.dataset.pbopen;
    PB.open = PB.open === code ? null : code;
    pbRerender();
    const p = PB.open && pbFind(PB.open);
    if (p) { if (!IS_CLAUDE) { await labBoot(); pbLoadInfo(p); } }
    return;
  }
  const p = PB.open && pbFind(PB.open);
  if (!p) return;
  const o = pbOpt(p);
  if ((x = b('[data-pbref]'))) { o.ref = x.dataset.pbref; pbRerender(); return; }
  if ((x = b('[data-pbrefad]'))) { o.refAd = x.dataset.pbrefad; pbRerender(); return; }
  if ((x = b('[data-pbgo]'))) { pbRun(p, x.dataset.pbgo); return; }
  if ((x = b('[data-pbhide]'))) { const k = x.dataset.pbhide; if (PB_HIDDEN.has(k)) PB_HIDDEN.delete(k); else PB_HIDDEN.add(k); pbSaveHidden(); pbRerender(); return; }
  if ((x = b('[data-pbhidebatch]'))) { (PB.res[p.code] || []).filter((c) => c.batch === x.dataset.pbhidebatch).forEach((c) => PB_HIDDEN.add(c.key)); pbSaveHidden(); pbRerender(); return; }
  if ((x = b('[data-pbshowhidden]'))) { PB.showHidden[p.code] = !PB.showHidden[p.code]; pbRerender(); return; }
  if (b('[data-pbclose]')) { PB.closed[p.code] = !PB.closed[p.code]; pbRerender(); return; }
  if ((x = b('[data-pbfacts]'))) {
    const how = x.dataset.pbfacts;
    if (how === 'refresh') { pbLoadInfo(p, true); return; }
    o.off = how === 'none' ? pbFacts(p).map((f, i) => i) : [];
    pbRerender(); return;
  }
  if ((x = b('[data-pbcopy]'))) {
    try { await navigator.clipboard.writeText(x.dataset.pbcopy); x.textContent = 'Copied'; } catch (err) { x.textContent = 'Copy blocked here'; }
    setTimeout(() => { x.textContent = x.classList.contains('linkbtn') ? 'Copy' : 'Copy all'; }, 1600);
    return;
  }
  if ((x = b('[data-pbtrack]'))) {
    const c = (PB.res[p.code] || [])[Number(x.dataset.pbtrack)];
    if (!c) return;
    await docsBoot(); x.disabled = true;
    const m = await addTest({ kind: 'product', label: `${p.name}: ${c.label || c.name}`, idea: c.headline || c.idea || '', source_ad_id: o.ref === 'ad' ? o.refAd || '' : '', source_ad_name: p.name, file: c.file || '' });
    x.textContent = String(m).startsWith('Saved') ? 'Added' : 'Added for you';
  }
});
document.addEventListener('change', (e) => {
  if (!e.target.closest('#pb-card')) return;
  const p = PB.open && pbFind(PB.open);
  if (!p) return;
  const o = pbOpt(p);
  const s = e.target.closest('[data-pbset]');
  if (s) { o[s.dataset.pbset] = s.dataset.pbset === 'n' ? Number(s.value) : s.value; pbRerender(); return; }
  const f = e.target.closest('[data-pbfact]');
  if (f) { const i = Number(f.dataset.pbfact); o.off = f.checked ? o.off.filter((v) => v !== i) : [...o.off, i]; pbRerender(); return; }
  const k = e.target.closest('[data-pbpick]');
  if (k) {
    const i = Number(k.dataset.pbpick);
    o.picks = k.checked ? [...new Set([...o.picks, i])].sort().slice(0, 3) : o.picks.filter((v) => v !== i);
    pbRerender();
  }
});
document.addEventListener('input', (e) => {
  const t = e.target.closest && e.target.closest('[data-pbpaste]');
  if (!t) return;
  const p = PB.open && pbFind(PB.open);
  if (p) pbOpt(p).paste = t.value.slice(0, 20000);
});
