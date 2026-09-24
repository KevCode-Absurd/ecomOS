'use strict';
// Creative lab: "Why it worked" breakdowns and image variants for image ads.
// Shared page: the breakdown runs on Claude through the page's `sample` capability (viewer's own Claude).
// Local app: both run on the local server, which keeps API keys in its own settings (never in this file).
let BREAKDOWNS = {};
const LABST = { status: null, sample: undefined, busy: {}, variants: {}, loaded: false };

// One shared promise, so every caller waits for the same boot (a second caller used to return early).
function labBoot() {
  if (!LABST.bootP) LABST.bootP = labBootOnce();
  return LABST.bootP;
}
async function labBootOnce() {
  LABST.loaded = true;
  try { const r = await fetch('breakdowns.json'); if (r.ok) { const d = await r.json(); if (d && typeof d === 'object') BREAKDOWNS = d; } } catch (e) { /* none yet */ }
  if (IS_CLAUDE) {
    try { LABST.sample = await window.claude.use('sample'); } catch (e) { LABST.sample = null; }
  } else {
    try { const r = await fetch('/api/ai-status'); LABST.status = r.ok ? await r.json() : null; } catch (e) { LABST.status = null; }
  }
}

// The facts both back ends see. Keep the wording of the prompt in sync with meta_gallery/ai.py.
function adFacts(id) {
  const ad = ENGINE.adDetail(id, state.since, state.until, { roas: VIEW.targets.roas, cpa: VIEW.targets.cpa });
  const m = ad.detail.metrics, t = VIEW.totals, c = ad.creative, r2x = (v) => (v === null || v === undefined ? null : Math.round(v * 100) / 100);
  const lc = ENGINE.lifecycle(id, (VIEW.targets.cpa || 5000) / 2);
  let domain = null;
  try { domain = c.link_url ? new URL(c.link_url).hostname : null; } catch (e) { domain = null; }
  return {
    ad_name: ad.name, campaign: ad.campaign_name, format: c.type_label, headline: c.headline || null,
    primary_text: (c.primary_text || '').slice(0, 1200) || null, call_to_action: c.cta || null, landing_domain: domain,
    tags: ad.tags ? { angle: ad.tags.angle.label, product: ad.tags.product.label, opening_line: ad.tags.hook.label } : null,
    dates: `${VIEW.range.since} to ${VIEW.range.until}`,
    this_ad: { spend_inr: r2x(m.spend), purchases: m.purchases, purchase_value_inr: r2x(m.purchase_value), roas: r2x(m.roas), cpa_inr: r2x(m.cpa), link_ctr_pct: r2x(m.link_ctr), impressions: m.impressions, days_with_spend: m.days_active, rank_by_spend: VIEW.ads[id] ? VIEW.ads[id].view.rank_by_spend : null },
    account_average: { roas: r2x(t.roas), cpa_inr: r2x(t.cpa), link_ctr_pct: r2x(t.link_ctr), ads: t.ads },
    verdict: ad.detail.verdict ? ad.detail.verdict.label : null, fatigue: ad.detail.fatigue ? ad.detail.fatigue.label : null,
    lifetime: lc ? { spend_inr: r2x(lc.lifetime.spend), roas: r2x(lc.lifetime.roas), first_day: lc.first_day, last_day: lc.last_day } : null,
  };
}
const BREAKDOWN_SHAPE = `{
  "verdict": "worked" | "mixed" | "did_not_work",
  "summary": "one sentence, plain words",
  "why": [{"point": "short reason", "evidence": "what in the image, copy or numbers shows it"}],
  "structure": {"hook": "", "layout": "", "product": "", "text_on_image": "", "offer": "", "proof": "", "cta": "", "look": ""},
  "keep": ["element to keep in new versions"],
  "test_next": ["one idea per line for a new version"],
  "watch_out": ["risk or weak spot"]
}`;
function breakdownPrompt(facts) {
  return 'You are a senior performance creative strategist for Meta ads. Study this image ad from Gehna, '
    + 'an Indian fine jewellery brand, and explain why it performed the way it did.\n\n'
    + `Ad data (JSON):\n${JSON.stringify(facts)}\n\n`
    + 'Rules:\n- Use the image, the copy and the numbers. Compare the ad\'s ROAS, CPA and link CTR with the account '
    + 'averages given. If the numbers are weak, say so honestly and set verdict accordingly.\n'
    + '- Plain, short sentences. No jargon. Use digits. No em dashes.\n'
    + '- 3 to 5 items in why. 3 to 6 items in keep and test_next. 1 to 3 in watch_out.\n'
    + '- structure: describe what is actually in the image. Use "none" when a part is missing.\n\n'
    + `Reply with only this JSON:\n${BREAKDOWN_SHAPE}`;
}
function cleanBd(d) {
  const s = (v, n) => String(v ?? '').replace(/[\u0000-\u001f\u007f]/g, ' ').trim().slice(0, n);
  const list = (v, n, m) => (Array.isArray(v) ? v : []).slice(0, n).map((x) => s(x, m)).filter(Boolean);
  const st = d && typeof d.structure === 'object' && d.structure ? d.structure : {};
  return {
    verdict: ['worked', 'mixed', 'did_not_work'].includes(d.verdict) ? d.verdict : 'mixed',
    summary: s(d.summary, 400),
    why: (Array.isArray(d.why) ? d.why : []).slice(0, 6).map((w) => (typeof w === 'string' ? { point: s(w, 200), evidence: '' } : { point: s(w && w.point, 200), evidence: s(w && w.evidence, 400) })).filter((w) => w.point),
    structure: Object.fromEntries(['hook', 'layout', 'product', 'text_on_image', 'offer', 'proof', 'cta', 'look'].map((k) => [k, s(st[k], 300)])),
    keep: list(d.keep, 8, 200), test_next: list(d.test_next, 8, 240), watch_out: list(d.watch_out, 4, 240),
    model: s(d.model, 60), provider: s(d.provider, 20), date: s(d.date, 20),
  };
}
function thumbBlob(id) {
  const src = thumbSrc(id);
  if (!src || !src.startsWith('data:')) return null;
  const [head, b64] = src.split(',');
  const bin = atob(b64), arr = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) arr[i] = bin.charCodeAt(i);
  return new Blob([arr], { type: head.slice(5, head.indexOf(';')) || 'image/jpeg' });
}

// ---------- shared AI helper (used by the lab, action plan, playbook and competitors) ----------
function aiReady() { return IS_CLAUDE ? !!LABST.sample : !!(LABST.status && LABST.status.breakdown); }
// A competitor ad image from the saved Ad Library snapshot, as a Blob for the AI.
function compBlob(compAdId) {
  const md = compAdId && typeof COMP_MEDIA === 'object' && COMP_MEDIA ? COMP_MEDIA[compAdId] : null;
  if (!md || !md.img) return null;
  const bin = atob(md.img), arr = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) arr[i] = bin.charCodeAt(i);
  return new Blob([arr], { type: 'image/jpeg' });
}
// opts: { comp: competitor ad id, ref: true to send the pasted reference image } as the second image.
async function askAI(prompt, imageAdId, opts = {}) {
  await labBoot();
  const useRef = !!(opts.ref && REF.b64);
  if (IS_CLAUDE) {
    if (!LABST.sample) throw { code: 'unavailable', message: 'Sign in to Claude to use this.' };
    const caps = await LABST.sample.limits().catch(() => null);
    const imgs = caps && caps.images ? [imageAdId ? thumbBlob(imageAdId) : null, useRef ? refBlob() : opts.comp ? compBlob(opts.comp) : null].filter(Boolean) : [];
    return LABST.sample.json(prompt, { modelTier: 'default', cache: false, ...(imgs.length ? { images: imgs.length === 1 ? imgs[0] : imgs } : {}) });
  }
  if (!aiReady()) throw { code: 'unavailable', message: 'AI is not set up on this computer yet.' };
  const r = await fetch('/api/ask', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ prompt, image_ad_id: imageAdId || null, comp_ad_id: (!useRef && opts.comp) || null, ref_image: useRef ? REF.b64 : null }) });
  const j = await r.json().catch(() => ({}));
  if (!r.ok) throw { code: 'server', message: j.error || 'Something went wrong. Try again.' };
  return j.json;
}
function aiErr(e) {
  const copy = { not_granted: 'Claude is not allowed for this page. Allow it when asked, or reload.', rate_limited: 'Too many requests just now. Wait a minute and try again.', invalid_json: 'The answer came back in the wrong shape. Try again.', refused: 'Claude declined this one.', session_expired: 'Sign in to Claude again.', cancelled: 'Stopped.' };
  return e && e.code in copy ? copy[e.code] : (e && e.message) || 'Something went wrong. Try again.';
}

// ---------- pasted reference image (shared by the lab and the competitor builder) ----------
// Paste (Ctrl+V), drop or pick any ad image. It goes to the AI next to the brand image as a layout and mood reference.
const REF = { b64: '', w: 0, h: 0 };
function refSlotHtml(label) {
  if (REF.b64) {
    return `<div class="refslot has"><img src="data:image/jpeg;base64,${REF.b64}" alt="Pasted reference image">
      <span class="small"><b>${esc(label || 'Reference image')}</b><br><span class="muted">${REF.w} x ${REF.h}. Used for layout and mood only.</span></span>
      <button class="btn ghost small-btn" type="button" data-refclear>Remove</button></div>`;
  }
  return `<label class="refslot" tabindex="0" data-refdrop><span class="refslot-ic" aria-hidden="true">+</span>
    <span class="small"><b>Add a reference image</b><br><span class="muted">Copy any ad image and press Ctrl+V here, drop a file, or click to choose one.</span></span>
    <input type="file" accept="image/png,image/jpeg,image/webp" data-refpick hidden></label>`;
}
function refBlob() {
  if (!REF.b64) return null;
  const bin = atob(REF.b64), arr = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) arr[i] = bin.charCodeAt(i);
  return new Blob([arr], { type: 'image/jpeg' });
}
// Shrink to 1024px on the long side as JPEG, so it stays small enough to send.
function refLoad(file) {
  return new Promise((resolve, reject) => {
    if (!file || !/^image\/(png|jpeg|webp|gif)$/.test(file.type)) { reject(new Error('That is not a PNG, JPEG or WebP image.')); return; }
    const url = URL.createObjectURL(file), img = new Image();
    img.onload = () => {
      const k = Math.min(1, 1024 / Math.max(img.naturalWidth, img.naturalHeight));
      const c = document.createElement('canvas');
      c.width = Math.round(img.naturalWidth * k); c.height = Math.round(img.naturalHeight * k);
      const g = c.getContext('2d'); g.fillStyle = '#fff'; g.fillRect(0, 0, c.width, c.height); g.drawImage(img, 0, 0, c.width, c.height);
      URL.revokeObjectURL(url);
      REF.b64 = c.toDataURL('image/jpeg', 0.88).split(',')[1]; REF.w = c.width; REF.h = c.height;
      resolve();
    };
    img.onerror = () => { URL.revokeObjectURL(url); reject(new Error('Could not read that image.')); };
    img.src = url;
  });
}
function refRerender() {
  if (window.pbRerender) window.pbRerender();
  if (state.tab === 'studio' && window.renderStudio) window.renderStudio();
  const lab = $('lab');
  if (lab && lab.dataset.id && typeof labRender === 'function') labRender(lab.dataset.id);
}
async function refTake(file) {
  try { await refLoad(file); } catch (e) { alertRef(e.message); return; }
  refRerender();
}
function alertRef(msg) { const m = document.querySelector('[data-refmsg]'); if (m) m.textContent = msg; }
function refVisible() { return !!document.querySelector('[data-refdrop], .refslot.has'); }
document.addEventListener('paste', (e) => {
  if (!refVisible()) return;
  const t = e.target;
  if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA') && t.type !== 'file') return;
  const item = [...(e.clipboardData ? e.clipboardData.items : [])].find((i) => i.kind === 'file' && i.type.startsWith('image/'));
  if (!item) return;
  e.preventDefault();
  refTake(item.getAsFile());
});
document.addEventListener('change', (e) => { if (e.target.matches('[data-refpick]') && e.target.files[0]) refTake(e.target.files[0]); });
document.addEventListener('click', (e) => { if (e.target.closest('[data-refclear]')) { REF.b64 = ''; refRerender(); } });
document.addEventListener('dragover', (e) => { const z = e.target.closest && e.target.closest('[data-refdrop]'); if (z) { e.preventDefault(); z.classList.add('over'); } });
document.addEventListener('dragleave', (e) => { const z = e.target.closest && e.target.closest('[data-refdrop]'); if (z) z.classList.remove('over'); });
document.addEventListener('drop', (e) => {
  const z = e.target.closest && e.target.closest('[data-refdrop]');
  if (!z) return;
  e.preventDefault();
  const f = e.dataTransfer && e.dataTransfer.files[0];
  if (f) refTake(f);
});

let BRAND = null, PACKS = {}, TESTS = { items: [] }, PLAYBOOK = null;
let DOCS_P = null;
function docsBoot() {
  if (!DOCS_P) DOCS_P = docsBootOnce();
  return DOCS_P;
}
async function docsBootOnce() {
  const get = (n) => fetch(n).then((r) => (r.ok ? r.json() : null)).catch(() => null);
  const [b, p, t, pb] = await Promise.all([get('brand.json'), get('packs.json'), get('tests.json'), get('playbook.json')]);
  BRAND = b && typeof b === 'object' ? b : {};
  PACKS = p && typeof p === 'object' ? p : {};
  TESTS = t && Array.isArray(t.items) ? t : { items: [] };
  PLAYBOOK = pb && pb.headline ? pb : null;
}
async function saveDoc(name, obj) {
  const r = await saveFile(name, obj);
  return r === 'saved' ? 'Saved for the team.' : r === 'local-only' ? 'Kept for you only. Saving for the team is off for you.' : r;
}
function copyBtn(text) { return `<button class="btn ghost small-btn" type="button" data-copy="${esc(text)}">Copy</button>`; }
document.addEventListener('click', (e) => {
  const b = e.target.closest('[data-copy]');
  if (!b) return;
  const t = b.dataset.copy;
  Promise.resolve().then(() => navigator.clipboard.writeText(t)).then(() => { b.textContent = 'Copied'; setTimeout(() => { b.textContent = 'Copy'; }, 1500); })
    .catch(() => { b.textContent = 'Select and copy'; });
});

// Tests: anything the team tries goes in one tracker.
function addTest(item) {
  const id = 't' + Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
  TESTS = { items: [{ id, created: new Date().toISOString().slice(0, 10), status: 'idea', ...item }, ...TESTS.items].slice(0, 500) };
  return saveDoc('tests.json', TESTS);
}

// ---------- launch packs (copy in the brand voice) ----------
function packPrompt(facts, bd, concepts) {
  return 'You write Meta ad copy for Gehna, an Indian fine jewellery brand. Write launch-ready copy in the brand voice below.\n\n'
    + `Brand kit (JSON):\n${JSON.stringify(BRAND || {}).slice(0, 5000)}\n\n`
    + `The ad these sets are for (JSON):\n${JSON.stringify(facts).slice(0, 5000)}\n\n`
    + `Why it worked (JSON):\n${JSON.stringify(bd || {}).slice(0, 4000)}\n\n`
    + `Write one copy set for each of these creatives (JSON):\n${JSON.stringify(concepts)}\n\n`
    + 'Rules:\n- Match the brand voice, emoji style and copy patterns closely. Emojis like the brand uses them.\n'
    + '- headline: at most 40 characters, 1 emoji at most.\n- primary_text: 3 to 6 short lines, a hook first, proof near the end, a clear last line. Use line breaks.\n'
    + '- description: at most 30 characters.\n- Use only approved claims that fit this product. Never invent prices, discounts or dates.\n- Digits, no em dashes.\n\n'
    + 'Reply with only this JSON:\n{"sets": [{"for": "creative name", "headline": "", "primary_text": "", "description": ""}], "cta": "SHOP_NOW"}';
}
function packConcepts(id) {
  const vs = (LABST.variants[id] || []).filter((v) => !v.error).slice(0, 5);
  if (vs.length) return vs.map((v) => ({ name: v.label, idea: v.idea || '', principle: v.principle || '' }));
  const b = BREAKDOWNS[id] ? cleanBd(BREAKDOWNS[id]) : null;
  return [{ name: 'Original ad', idea: 'the ad as it is' }, ...((b && b.test_next) || []).slice(0, 2).map((t, i) => ({ name: `New angle ${i + 1}`, idea: t }))];
}
function packHtml(id) {
  const p = PACKS[id];
  if (!p || !Array.isArray(p.sets)) return '';
  const s = (v) => String(v || '');
  return `<div class="packs">${p.sets.map((x) => `<div class="pack"><div class="pack-for">${esc(s(x.for))}</div>
    <div class="pack-row"><span>Headline</span><p>${esc(s(x.headline))}</p>${copyBtn(s(x.headline))}</div>
    <div class="pack-row"><span>Primary text</span><p class="pre">${esc(s(x.primary_text))}</p>${copyBtn(s(x.primary_text))}</div>
    ${x.description ? `<div class="pack-row"><span>Description</span><p>${esc(s(x.description))}</p>${copyBtn(s(x.description))}</div>` : ''}</div>`).join('')}
    <p class="small muted">Written in the Gehna voice${p.date ? ' on ' + esc(dateLabel(p.date)) : ''}. Call to action: ${esc(String(p.cta || 'SHOP_NOW').replace(/_/g, ' ').toLowerCase())}.</p></div>`;
}
async function labRunPack(id) {
  LABST.busy[id] = 'pack'; labRender(id);
  let msg = '';
  try {
    await docsBoot();
    const out = await askAI(packPrompt(adFacts(id), BREAKDOWNS[id], packConcepts(id)), id);
    const sets = (Array.isArray(out && out.sets) ? out.sets : []).slice(0, 6).map((x) => ({ for: String(x.for || '').slice(0, 80), headline: String(x.headline || '').slice(0, 120), primary_text: String(x.primary_text || '').slice(0, 1500), description: String(x.description || '').slice(0, 80) })).filter((x) => x.headline || x.primary_text);
    if (!sets.length) throw { message: 'No copy came back. Try again.' };
    PACKS = { ...PACKS, [id]: { date: new Date().toISOString().slice(0, 10), cta: String(out.cta || 'SHOP_NOW').slice(0, 30), sets } };
    msg = await saveDoc('packs.json', PACKS);
  } catch (e) { msg = aiErr(e); }
  delete LABST.busy[id];
  labRender(id);
  if ($('labMsg')) $('labMsg').textContent = msg;
}

// ---------- rendering ----------
const STRUCT_LABELS = { hook: 'Hook', layout: 'Layout', product: 'Product', text_on_image: 'Text on image', offer: 'Offer', proof: 'Proof', cta: 'Call to action', look: 'Look and feel' };
const VERDICT_TXT = { worked: ['Worked', 'v-scale'], mixed: ['Mixed', 'v-watch'], did_not_work: ['Did not work', 'v-cut'] };
function bdHtml(b) {
  const [vt, vc] = VERDICT_TXT[b.verdict] || VERDICT_TXT.mixed;
  const li = (xs) => xs.map((x) => `<li>${esc(x)}</li>`).join('');
  return `<div class="bd">
    <div class="bd-top"><span class="chip ${vc}">${vt}</span>${b.date ? `<span class="small muted">Updated ${esc(dateLabel(b.date))}</span>` : ''}</div>
    ${b.summary ? `<p class="bd-sum">${esc(b.summary)}</p>` : ''}
    ${b.why.length ? `<h3>Why it performed this way</h3><ul class="bd-why">${b.why.map((w) => `<li><strong>${esc(w.point)}</strong>${w.evidence ? `<span>${esc(w.evidence)}</span>` : ''}</li>`).join('')}</ul>` : ''}
    <h3>Structure of the ad</h3>
    <div class="bd-grid">${Object.entries(STRUCT_LABELS).filter(([k]) => b.structure[k] && b.structure[k].toLowerCase() !== 'none').map(([k, l]) => `<div><span>${l}</span><p>${esc(b.structure[k])}</p></div>`).join('')}</div>
    ${b.keep.length ? `<h3>Keep in new versions</h3><div class="bd-keep">${b.keep.map((k) => `<span>${esc(k)}</span>`).join('')}</div>` : ''}
    ${b.test_next.length ? `<h3>Ideas to test next</h3><ul class="bd-list">${li(b.test_next)}</ul>` : ''}
    ${b.watch_out.length ? `<h3>Watch out</h3><ul class="bd-list warn">${li(b.watch_out)}</ul>` : ''}
    <p class="small muted">An AI reading of the ad and its numbers. Check it before acting on it.</p>
  </div>`;
}
function variantsHtml(id) {
  const list = LABST.variants[id] || [];
  if (!list.length) return '';
  return `<div class="vgrid">${list.map((v) => v.error ? `<div class="vcard err"><strong>${esc(v.label)}</strong><span class="small">${esc(v.error)}</span></div>`
    : `<figure class="vcard"><a href="/variants/${esc(id)}/${esc(v.file)}" target="_blank" rel="noopener"><img src="/variants/${esc(id)}/${esc(v.file)}" alt="${esc(v.label)}" loading="lazy"></a><figcaption><span class="vtag ${v.closeness === 'close' ? 'close' : ''}">${v.closeness === 'close' ? 'Close to original' : 'New idea'}</span><strong>${esc(v.label)}</strong>${v.principle ? `<span class="small">${esc(v.principle)}</span>` : ''}<span class="small muted">${esc(v.date || '')}</span><span class="vbtns"><a class="btn ghost small-btn" href="/variants/${esc(id)}/${esc(v.file)}" download="Gehna-${esc(id)}-${esc(v.file)}">Download</a><button class="btn ghost small-btn" type="button" data-track="${esc(id)}|${esc(v.file)}">Track test</button></span></figcaption></figure>`).join('')}</div>`;
}
window.labSection = function labSection(id) {
  return `<section id="lab" class="lab" data-id="${esc(id)}"><div class="lab-head"><h3 style="margin:0">Creative lab</h3><span class="small muted">Image ads only</span></div><div id="labBody"><p class="small muted">Loading…</p></div></section>`;
};
function labRender(id) {
  const box = $('labBody');
  if (!box || $('lab').dataset.id !== id) return;
  const b = BREAKDOWNS[id] ? cleanBd(BREAKDOWNS[id]) : null;
  const busy = LABST.busy[id];
  let canBd = false, note = '';
  if (IS_CLAUDE) {
    canBd = !!LABST.sample;
    note = canBd ? 'Takes about 30 to 60 seconds.' : 'Sign in to Claude to see why this ad worked.';
  } else if (LABST.status) {
    canBd = LABST.status.breakdown;
    note = canBd ? 'Takes about 30 to 60 seconds.' : 'AI is not set up on this computer yet.';
  } else note = 'AI is not available right now.';
  const canVar = !IS_CLAUDE && LABST.status && LABST.status.variants;
  const varCtl = canVar ? `<div class="lab-ctl">
      <label class="field">How many <select id="labN"><option value="2">2</option><option value="3" selected>3</option><option value="4">4</option><option value="5">5</option></select></label>
      <label class="field">Size <select id="labSize"><option value="square">Square 1:1</option><option value="portrait">Portrait 4:5</option><option value="story">Story 9:16</option></select></label>
      <label class="field">Quality <select id="labQ"><option value="medium" selected>Medium</option><option value="high">High</option><option value="low">Low (cheapest)</option></select></label>
      <button class="btn" type="button" data-lab="variants"${busy ? ' disabled' : ''}>${busy === 'variants' ? 'Making images…' : REF.b64 ? 'Make variants with reference' : 'Make image variants'}</button></div>
      <div class="lab-ref">${refSlotHtml('Reference image')}<p class="small muted" data-refmsg>Optional. With a reference, every version takes its layout and mood and keeps this ad's product.</p></div>
      <p class="small muted">Version 1 stays close to this ad. The rest are new ideas built on why it worked, each testing a different reason. About 1 to 2 minutes in total.</p>`
    : '';
  box.innerHTML = `${b ? bdHtml(b) : '<p class="lab-lead">Get a breakdown of why this ad worked and how it is built.</p>'}
    <div class="lab-actions"><button class="btn${b ? ' ghost' : ''}" type="button" data-lab="breakdown"${!canBd || busy ? ' disabled' : ''}>${busy === 'breakdown' ? 'Reading the ad…' : b ? 'Run again' : 'Why it worked'}</button>${busy ? '<span class="lab-spin" aria-hidden="true"></span>' : ''}</div>
    <p class="small muted" id="labMsg">${note}</p>
    ${b ? `<div class="lab-var"><h3>New versions of this ad</h3>${varCtl}<div id="labVariants">${variantsHtml(id)}</div></div>
    <div class="lab-var"><h3>Launch pack</h3><p class="small muted">Headlines and primary text in the Gehna voice, one set per new version.</p>
      <div class="lab-actions"><button class="btn${PACKS[id] ? ' ghost' : ''}" type="button" data-lab="pack"${!canBd || busy ? ' disabled' : ''}>${busy === 'pack' ? 'Writing…' : PACKS[id] ? 'Write again' : 'Write ad copy'}</button></div>
      ${packHtml(id)}</div>` : ''}`;
}
async function labRunBreakdown(id) {
  LABST.busy[id] = 'breakdown'; labRender(id);
  const facts = adFacts(id);
  let msg = '';
  try {
    let out;
    if (IS_CLAUDE) {
      const caps = await LABST.sample.limits().catch(() => null);
      const img = caps && caps.images ? thumbBlob(id) : null;
      const raw = await LABST.sample.json(breakdownPrompt(facts), { modelTier: 'default', cache: false, ...(img ? { images: img } : {}) });
      out = { ...cleanBd(raw), provider: 'claude', model: 'Claude', date: new Date().toISOString().slice(0, 10) };
      BREAKDOWNS = { ...BREAKDOWNS, [id]: out };
      const r = await saveFile('breakdowns.json', BREAKDOWNS);
      msg = r === 'saved' ? 'Saved for the team.' : r === 'local-only' ? 'Shown for you only. Saving for the team is off for you.' : r;
    } else {
      const r = await fetch('/api/breakdown', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ ad_id: id, facts }) });
      const j = await r.json().catch(() => ({}));
      if (!r.ok) throw { code: 'server', message: j.error || 'The breakdown failed.' };
      out = j;
      BREAKDOWNS = { ...BREAKDOWNS, [id]: out };
      msg = 'Saved.';
      loadVariants(id);
    }
  } catch (e) {
    const copy = { not_granted: 'Claude is not allowed for this page. Allow it when asked, or reload.', rate_limited: 'Too many requests just now. Wait a minute and try again.', invalid_json: 'The answer came back in the wrong shape. Try again.', refused: 'Claude declined this one.', session_expired: 'Sign in to Claude again.', cancelled: '' };
    msg = e && e.code in copy ? copy[e.code] : (e && e.message) || 'Something went wrong. Try again.';
  }
  delete LABST.busy[id];
  labRender(id);
  if ($('labMsg') && msg) $('labMsg').textContent = msg;
}
async function loadVariants(id) {
  if (IS_CLAUDE) return;
  try { const r = await fetch('/api/variants/' + encodeURIComponent(id)); if (r.ok) LABST.variants[id] = await r.json(); } catch (e) { /* none */ }
  if ($('labVariants')) $('labVariants').innerHTML = variantsHtml(id);
}
async function labRunVariants(id) {
  const n = $('labN').value, size = $('labSize').value, quality = $('labQ').value;
  LABST.busy[id] = 'variants'; labRender(id);
  if ($('labMsg')) $('labMsg').textContent = `Planning ${n} ideas, then making the images. About 1 to 2 minutes. You can keep browsing.`;
  let msg = '';
  try {
    const r = await fetch('/api/variants', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ ad_id: id, n: Number(n), size, quality, ref_image: REF.b64 || null }) });
    const j = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(j.error || 'Could not make images.');
    LABST.variants[id] = j.all;
    const bad = j.made.filter((m) => m.error);
    msg = bad.length ? `${j.made.length - bad.length} of ${j.made.length} made. ${bad[0].error}` : `${j.made.length} images made. Download the ones you like and launch them in Ads Manager.`;
  } catch (e) { msg = e.message; }
  delete LABST.busy[id];
  labRender(id);
  if ($('labMsg')) $('labMsg').textContent = msg;
}
window.initLab = async function initLab(id) {
  await labBoot();
  await docsBoot();
  labRender(id);
  loadVariants(id);
};
document.addEventListener('click', (e) => {
  const b = e.target.closest('[data-lab]');
  if (!b || !$('lab')) return;
  const id = $('lab').dataset.id;
  if (b.dataset.lab === 'breakdown') labRunBreakdown(id);
  if (b.dataset.lab === 'variants') labRunVariants(id);
  if (b.dataset.lab === 'pack') labRunPack(id);
});
document.addEventListener('click', async (e) => {
  const b = e.target.closest('[data-track]');
  if (!b) return;
  const [id, file] = b.dataset.track.split('|');
  const v = (LABST.variants[id] || []).find((x) => x.file === file) || {};
  const ad = ENGINE.c.ads[id];
  b.disabled = true;
  const msg = await addTest({ kind: v.source === 'competitor' ? 'competitor' : 'variant', label: v.label || 'Variant', idea: v.principle || v.idea || '', source_ad_id: id, source_ad_name: ad ? ad.name : '', file });
  b.textContent = msg.startsWith('Saved') ? 'Tracked' : 'Kept locally';
});
