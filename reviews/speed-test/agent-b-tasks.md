# Gehna site speed: execution plan (agent B, stage 2)

Date: 24 September 2026. Site: https://www.gehnaindia.com/. Stack: custom Next.js (pages router), React, Material UI, Apollo GraphQL, Cloudflare in front of CloudFront in front of the Next.js origin. Not Shopify.

Inputs: `playbooks/v2/08-SPD-speed/PLAYBOOK.md` (v2.0-draft), `reviews/speed-test/agent-b-audit.md` (the audit, 24 Sep 2026), raw runs in `reviews/speed-test/raw-b/` (`home-mobile-slow4g.json`, `collection-rings-mobile-slow4g.json`, `product-emerald-ring-mobile-slow4g.json`, `home-desktop-unthrottled.json`, `README.json`). No new measurements were taken for this plan; every number below is from those files or is arithmetic on them. The arithmetic was run in code (`spdB2-estimates.py`, reproduced in section 8).

Who does what: "Dev" = the developer who owns the Next.js repo. "CF" = whoever holds the Cloudflare and AWS logins. "Owner" = Kevin or the Gehna team. "Agent" = this system, for measurement and proof.

Where a playbook procedure is Shopify-only, the step given here is the Next.js equivalent and is marked **adaptation**.

## 0. How the ranking was made

Playbook rules used: R2 (biggest single cause first), R3 (pages by traffic and money; the ad landing page, usually the product page, first), R4 and conflict 7.4 (weight and content before code, code before caching and host), R23 (highest-impact item, not the first in the list), R91 (caching after fundamentals), R62 (bundle work after images and scripts), R26 (one change at a time), R102 (proof by averaged before and after runs).

What the raw data says the critical path is (medians of 3 runs, mobile Pixel 5 emulation, Slow 4G 1.6 Mbps, CPU 4x, cold cache; audit section 2.2 and 3.2):

| Step | Home | Collection /m/rings | Product (emerald ring) | Raw field |
|---|---|---|---|---|
| TTFB | 0.43 s | 0.13 s | 0.35 s | `nav.ttfb` |
| 2 big fonts (897 KB + 956 KB `.ttf`) finish | 19.2 s | 13.3 s | 14.2 s | `res` entries `14a3fceaeabbcb56-s.p.ttf`, `ae1a48c074c123e8-s.p.ttf` |
| All first-party JS before load finished | 10.1 s (443 KB, 30 files) | 7.5 s (461 KB, 33 files) | 9.0 s (599 KB, 38 files) | `res` `/_next/static/chunks/*.js`, `end` < `nav.load` |
| Load event | 19.3 s | 13.5 s | 14.3 s | `nav.load` |
| First heavy main-thread work (long tasks) | 19.2 s | 13.3 s | 14.25 s | `m.longtasks` |
| Product data requests (GraphQL) | 20.8 s | 15.0 s (tiles) | 16.7 to 18.5 s | `res` `graphql`, `/_next/image` product tiles |
| LCP | 7.9 s (hero PNG) | 6.6 s (spinner GIF); grid at 15.2 s | 18.3 s (main image, 25 KB AVIF, requested at 16.4 s) | `m.lcp`, `m.clsEntries` |
| CLS | 0.000 | 0.110 | 0.129 | `m.cls` |
| TBT est | 3.98 s | 2.64 s | 3.00 s | `summary.tbt_est` |
| Bytes before load | 3,544 KB | 2,420 KB | 2,558 KB | sum of `res.size` with `end` <= `nav.load` |

Two facts drive the ranking:

1. Fonts are 1,921 KB of every page (48% of the home page) and are `preload`ed, so they take the network from 0.3 s until 13 to 19 s. Effective throughput on the profile is 3,544 KB / (19.34 - 0.43) s = 187 KB/s on home and 2,558 KB / (14.31 - 0.35) s = 183 KB/s on product (nominal 200 KB/s). Removing 1,771 KB of font bytes frees 1,771 / 185 = 9.6 s of transfer on every template.
2. On all 3 templates, JavaScript execution (the long tasks) starts within 0.1 s of the load event, and the load event waits for the preloaded fonts, even though the JavaScript files finished downloading 4 to 9 s earlier (product: JS done at 9.0 s, first long task 14.25 s, fonts end 14.24 s, load 14.31 s). The product data is only requested 2.3 s after that. So on the product page the shopper waits: fonts, then hydration, then 6 GraphQL calls, then the image. This is the R81 case ("a script is hiding the image") and the R66 case (client-only rendering of the main content).

Ranked list (estimated gains are from the model in section 8, on the same slow 4G lab profile; they are model outputs, not promises, and each must be proven per P30):

| Rank | Task | Templates | Estimated gain (lab, slow 4G) | Effort | Owner | Depends on |
|---|---|---|---|---|---|---|
| 0 | Baseline with PageSpeed Insights and a re-run of the 3-run test | all | none (proof) | 2 h | Agent, Owner | PSI quota |
| 1 | Subset and convert the fonts to WOFF2 (1,921 KB to under 150 KB) | all | Home LCP 7.9 to about 3.2 s; product LCP 18.3 to about 9.4 s; collection grid 15.2 to about 9.2 s; page weight minus 1.77 MB | 4 to 8 h | Dev | none |
| 2 | Server-render the product buy box (image, name, price, Add to Cart) and preload the main image | product | Product LCP about 9.4 to about 2.0 to 2.5 s | 24 to 80 h | Dev | 1, 8 (image cache hit) |
| 3 | Server-render the first collection tiles, skeleton for the rest | collection | Collection LCP from spinner at 6.6 s (grid 15.2 s) to about 1.6 to 2.5 s | 16 to 40 h | Dev | 1, 5 |
| 4 | Home hero as AVIF under 100 KB with preload; 7 category icons at 10 KB; `priority` on 1 image only | home | Home LCP about 3.2 to about 2.2 s; minus 0.9 MB above the fold | 4 to 6 h | Dev | 1 |
| 5 | Reserve space for the grid and the reviews band | collection, product | CLS 0.110 to 0.05 and 0.129 to 0.05 (to about 0 with 2 and 3) | 3 to 4 h | Dev | none |
| 6 | Test Cloudflare Rocket Loader off; stop gating data fetches on the load event | all | Product LCP minus about 4.3 s if done alone; small after task 1; removes a hydration risk | 1 to 3 h | CF, Dev | none |
| 7 | JavaScript diet: bundle analysis, lazy sections, fewer tiles, no prefetch in grids | all | TBT est 2.6 to 4.0 s toward under 1 s; no measured basis for a seconds figure yet | 24 to 40 h | Dev | 1 to 3 measured first |
| 8 | Cache rules: resized images 30 days at CloudFront, decide the HTML rule | all | Removes 1.5 to 4.2 s image waits on CDN misses (measured on misses); needed for task 2's estimate | 3 to 4 h | Dev, CF | none |
| 9 | Clean-ups: dead Universal Analytics tag, CustomerLabs 403, duplicate gtag, GIF spinner and GIF logo, product video preload, 307 to 404 | all | minus 100 to 190 KB per page; fewer requests; correct 404s | 6 to 8 h | Dev | 6 for tracking tests |
| 10 | Monitoring and performance budget (Lighthouse CI in deploys, monthly 3-run test, 28-day field check) | all | protects the gains | 6 to 8 h | Dev, Agent | 0 |

Further items worth listing (section 1.11): API field selection, real-device and checkout tests, site-wide crawl on staging, peak readiness before the Diwali sale window, field INP.

## 1. Tasks

Each task: problem and evidence, playbook rules and procedures, estimated gain and its arithmetic, effort, owner, steps, verification per P30, risks and rollback, dependencies.

### Task 0. Baseline before the first change (R1, R15, R20, P1, P4)

Problem: the audit's baseline is from a local headless Chromium instrument, not from Google's PageSpeed Insights, because the PSI quota was exhausted on 24 Sep (audit 2.1). Google's own lab and field numbers are the ones the owner will see later, so record them before anything ships.

Steps:
1. When the PSI quota resets, run PSI mobile and desktop, 3 times each, on `/`, `/m/rings` and `/verdant-whisper-emerald-18k-gold-ring`. Record score, LCP, CLS, TBT, FCP, TTFB, the LCP element, and whether field data (CrUX) exists for the URL or only the origin (P3 step 2). Save the report links.
2. Re-run the raw-b instrument (`reviews/speed-test/raw-b/measure-script.py`) once, 3 runs per page, to confirm the site has not changed since 24 Sep. Compare LCP, bytes and request counts with the audit table. Differences of a few percent are noise (R15).
3. Add the freshness marker rule to the developer's release checklist: after each deploy, a fresh incognito load, then `curl -sI` on the page to read `age` and `cf-cache-status`; if `age` is older than the deploy, purge that URL at Cloudflare before measuring (P4 adaptation; the site has no theme editor, the CDN cache plays that role).
4. Start the change log (section 6 template). Entry 1: the baseline.

Verification: baseline table complete for 3 templates x 2 devices. Rollback: none. Effort: 2 h. Owner: Agent runs the tests; Owner runs PSI if the agent's quota is still blocked.

### Task 1. Subset the fonts and ship WOFF2 (rank 1)

**Problem and evidence.** Four font files are preloaded on every page: `14a3fceaeabbcb56-s.p.ttf` 897 KB and `ae1a48c074c123e8-s.p.ttf` 956 KB (Nanum Myeongjo 400 and 700, full Korean glyph set, TrueType), plus `4291f48c2ea51320-s.p.ttf` 35 KB and `2c00c297d3cdabf8-s.p.ttf` 34 KB (Lato 400 and 700). Total 1,921 KB, 48% of home page bytes (audit 3.2, 5.5; raw `res` and `fonts` in all 3 mobile files). On slow 4G the 2 big files download from 0.3 to 0.6 s until 18.8 to 19.2 s (home), 13.0 to 13.3 s (collection), 13.9 to 14.2 s (product). The font family names in the DOM (`__nanumMyeongjo_a8aec9`, `__lato_e21d47`, `__variable_...` classes on `<body>`) show they are declared with `next/font`, and the `.p.ttf` extension shows `next/font/local` with TrueType sources (raw `fonts` list; `display: swap` is already set, `size-adjust` fallbacks exist). The load event waits for preloads, so these 2 files also hold back JavaScript execution on this site (section 0, fact 2).

**Rules and procedures.** R71 (about 3 variations, subset), R72 (self-host as WOFF2), R37 (preload only the LCP image and critical fonts; never many assets), R28 and R4 (weight first), R70 (keep swap). P21 steps 1, 3, 4, 5, 6 (adaptation: `next/font` config instead of a WordPress font plugin). Conflict 7.19 (page budget 2 MB; the fonts alone are 1.9 MB).

**Estimated gain and basis.**
- Bytes: 1,921 KB today; target under 150 KB (4 Latin-subset WOFF2 files; Google's own Latin subsets are about 20 to 40 KB per weight). Saved: 1,771 KB.
- Transfer time freed on the profile: 1,771 KB / 185 KB/s = 9.6 s per page view (throughput derived in section 0).
- Home LCP: today the hero (279 KB PNG) shares the pipe with the fonts and downloads from 0.57 s to 7.83 s. Model after the fix: bytes that must arrive before the hero completes = HTML 36 + fonts 150 + hero 279 + CSS 30 = 495 KB; 495 / 185 = 2.7 s; plus TTFB 0.43 s and about 0.1 s render = **about 3.2 s** (from 7.9 s). With task 4 (AVIF hero of 100 KB) the same sum is 316 KB = 1.7 s + 0.5 = **about 2.2 s**.
- Product LCP: today JS finishes at 9.0 s while sharing the pipe with fonts; execution starts at load (14.3 s). Model after the fix: JS 602 KB alone from 1.13 s: 1.13 + 602 / 185 = 4.4 s; load about 4.5 s; then the measured main-thread work before the data requests (14.25 to 16.6 s = 2.3 s, CPU-bound, unchanged), then the GraphQL round (measured 0.8 to 1.8 s, use 1.2 s), then the image request (measured 16.45 to 17.97 s = 1.5 s): 4.4 + 2.3 + 1.2 + 1.5 = **about 9.4 s** (from 18.3 s). The rest needs task 2.
- Collection grid visible: 1.05 + 466 / 185 + 2.1 (work) + 1.5 (listing fetch) + 2.0 (tiles) = **about 9.2 s** (from 15.2 s). The rest needs task 3.

**Effort.** 4 to 8 h. **Owner.** Dev.

**Steps (Next.js pages router).**
1. Find the declaration: `grep -rn "nanumMyeongjo\|Nanum\|localFont(\|next/font" src pages components styles` (adjust to the repo layout). Expect a `localFont({ src: [...ttf] })` call for Nanum Myeongjo and one for Lato, exported with `variable`.
2. Decide the character set. The site is English with rupee prices. The subset must include Latin plus the rupee sign U+20B9 and the punctuation the site uses. Check for any Hindi text set in these fonts: `grep -rn "[ऀ-ॿ]" src` (or ask the content team). If none, Latin only.
3. Preferred route, `next/font/google` (Next downloads the font at build time and emits WOFF2 subsets; the build machine needs internet access to fonts.googleapis.com):
   ```ts
   // src/fonts.ts (or the existing fonts module)
   import { Lato, Nanum_Myeongjo } from 'next/font/google';
   export const lato = Lato({ weight: ['400', '700'], subsets: ['latin'], display: 'swap', variable: '--font-lato' });
   export const nanumMyeongjo = Nanum_Myeongjo({ weight: ['400', '700'], subsets: ['latin'], display: 'swap', variable: '--font-nanum', adjustFontFallback: true });
   ```
   Keep the same `variable` names the CSS already uses so nothing else changes.
4. If the build cannot reach Google, keep `next/font/local` but replace the `.ttf` sources with subset WOFF2 files you generate once:
   ```bash
   pip install fonttools brotli
   pyftsubset NanumMyeongjo-Regular.ttf --flavor=woff2 --layout-features='*' \
     --unicodes="U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+2074,U+20AC,U+20B9,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD" \
     --output-file=public/fonts/NanumMyeongjo-Regular.latin.woff2
   ```
   Repeat for the 700 weight and for both Lato weights. Then `localFont({ src: [{ path: '../public/fonts/NanumMyeongjo-Regular.latin.woff2', weight: '400', style: 'normal' }, ...], display: 'swap', variable: '--font-nanum' })`.
5. Check whether Nanum Myeongjo 700 is used at all: `grep -rn "fontWeight: *700\|font-weight: *700\|fontWeight: *'bold'\|<b>\|<strong>" src | grep -i -B2 -A2 "nanum\|serif"`. If no serif element is bold, drop the 700 file (R71). Same check for Lato 700.
6. Do not add manual `<link rel="preload">` tags for fonts; `next/font` adds one per file it emits. After the change there must be at most 4 (ideally 3) font preloads, all `.woff2`.
7. Build, deploy to staging, run the tests in "Verification".

**Verification (P30).**
- Before: the audit medians (home LCP 7.88 s, product 18.26 s, collection grid about 15.2 s; font bytes 1,921 KB).
- Freshness: `curl -s https://www.gehnaindia.com/ | grep -o '<link[^>]*as="font"[^>]*>'` lists only `.woff2` files; `curl -sI` on each shows `content-length` under 50 KB; total under 150 KB.
- After: 3 runs per page on the same slow 4G profile, medians. Pass: font bytes under 150 KB; home LCP under 4.0 s; product LCP under 11 s; load event on product under 6 s. (The task 1 model says 3.2 s, 9.4 s, 4.5 s; pass lines leave room for noise.)
- Visual: the hero headline and product names still render in the serif face; the rupee sign in prices renders in the same face as the digits (open DevTools > Elements > Computed > Rendered Fonts on a price). Test on throttled 3G that text shows in the fallback first, then swaps without a size jump (CLS stays under 0.01 on home).
- Function: no tracking change, so no event tests needed (R48 not triggered).

**Risks and rollback.** Risk: a glyph missing from the subset shows in the fallback font (most likely the rupee sign or a curly quote); fix by adding the code point to the subset. Risk: `next/font/google` build fails offline; use step 4. Rollback: revert the fonts module; the old `.ttf` files return on the next build.

**Dependencies.** None. Everything else measures better after this, so it ships first and alone (R26).

### Task 2. Server-render the product buy box and preload the main image (rank 2)

**Problem and evidence.** The product HTML (92 KB decoded, 25 KB compressed) has no `<h1>`, no price and no product `<img>`; the product data is inside `__NEXT_DATA__` (57 KB inline JSON, raw `scripts` list) but is rendered only in the browser after hydration. The main image request starts at 16.4 s (run 2), after the load event (14.3 s), after 2.3 s of main-thread work, and alongside 6 GraphQL calls (16.7 to 18.5 s). LCP 18.1 to 20.1 s across the 3 runs; the image itself is 25 KB AVIF and arrives 1.5 s after it is asked for (audit 3.2, 5.4, 5.16, Problem 2; raw `res`, `m.lcp`). The reviews band renders late and shifts the buy box down by 0.08 (raw `m.clsEntries`, text "Two Decades of Expertise, Glowing Review").

**Rules and procedures.** R66 (server-side or hybrid rendering beats a client-rendered app; render-blocking JS before the main image is the pattern to avoid "at all cost"), R81 (the script is hiding the image), R53 (product image and information before integrations), R80 and P18 steps 4 to 8 (un-lazy, de-animate, preload with high priority, cut what is ahead), R37 (preload the LCP image only), R100 (developer task), R3 (product pages are where ads land [needs brand data: landing pages by ad]).

**Estimated gain and basis.** With task 1 done and the image a CDN hit (task 8): the `<img>` is in the HTML, so the request starts right after the HTML arrives. Bytes before the image completes = HTML 25 + fonts 150 + CSS 80 + image 25 = 280 KB; 280 / 185 = 1.5 s; plus TTFB 0.35 s and 0.15 s render = **about 2.0 s**; allow up to 2.5 s for the preload competing with the first JS chunks. From about 9.4 s after task 1, so the task's own gain is about 7 s, and the combined gain from today is about 16 s. If the image is a CloudFront miss, add the origin resize wait: the desktop hero on a miss took 4.2 s for 78 KB (raw `home-desktop-unthrottled.json`, `new-arrivals-desktop.png` start 1,072 ms, end 5,272 ms), the product main image on a miss took 1.5 s for 25 KB. That is why task 8 is a dependency.

**Effort.** 24 to 80 h depending on how the page component is written. **Owner.** Dev.

**Steps.**
1. Confirm the gap: `curl -s https://www.gehnaindia.com/verdant-whisper-emerald-18k-gold-ring | grep -c "<h1"` returns 0 today. Save this output as the before state.
2. Find why the server skips the content. In `pages/[product].tsx` (the chunk name `pages/%5Bproduct%5D-*.js` confirms the route) and its components look for: `dynamic(() => import('...'), { ssr: false })` on the gallery, buy box or page body; `useQuery(..., { ssr: false })`; a `mounted` or `isClient` state that renders the spinner until `useEffect` runs; `if (typeof window === 'undefined') return <Loader />`; or a data fetch that waits for `window.load`. One of these is why the spinner (`loading.gif`, `MuiGrid-root jss28`) is the only content the server sends.
3. Move the product read to the server: the page already ships `initialApolloState` with the product, so `getServerSideProps` (or `getStaticProps` with `revalidate`) already runs the query. Pass the product as a prop to the buy box and render from the prop on the server and on the client. If the buy box uses `useQuery`, keep it but give it `fetchPolicy: 'cache-first'` so it reads the hydrated cache synchronously and never shows the spinner when the data is already present.
4. Main image: render slide 1 as a plain `next/image` outside any client-only carousel (P18 step 3), with `priority`, `sizes="100vw"`, real `width` and `height`. `priority` sets `fetchpriority="high"`, disables lazy loading and emits the `<link rel="preload" as="image" imagesrcset imagesizes>`. Check the rendered head has exactly 1 image preload; if the installed Next version does not emit it, add it in the page's `<Head>` by hand with the same `srcset` and `sizes`. Slides 2 and up stay lazy and can stay inside Swiper.
5. Render `<h1>` (product name), the price and the Add to Cart button on the server too. Price formatting must be identical on server and client (fixed `en-IN` formatting with a helper; do not rely on the runtime locale), or React will warn about a hydration mismatch and re-render.
6. Keep the reviews band, related products, recently viewed and any Klaviyo or Tagalys widgets client-rendered and below the buy box (R53). Give them fixed containers (task 5). Load them on mount, not on the load event.
7. The 6 GraphQL calls after load: list them (DevTools Network, filter `graphql`, read the operation names). Any that fetch data already in `__NEXT_DATA__` should be dropped; the rest should ask for only the fields the section renders (R69; see item 1.11.1).
8. Put the new rendering behind a flag (`NEXT_PUBLIC_PDP_SSR=1` or a query parameter on staging) so it can be compared on the same build.
9. HTML caching after this change: the HTML now carries price and stock. Keep `private, max-age=1800` from the app only if the Cloudflare rule that currently caches it (`cf-cache-status: HIT`, `age` 21 to 3,400 s on `private` pages, raw `doc_headers`) is reviewed in task 8. Either way, prices that change need a purge (task 8 step 5).

**Verification (P30).**
- Before: product LCP 18.26 s median; `<h1>` count 0; main image request at 16.4 s.
- Freshness: `curl -s <product url> | grep -o '<img[^>]*fetchpriority="high"[^>]*>' | head -1` shows the main image URL; `grep -o '<h1[^>]*>[^<]*<'` shows the name; the price string appears in the HTML. `grep -o 'rel="preload" as="image"[^>]*' ` shows exactly 1 image preload.
- After: 3 runs slow 4G. Pass: LCP element is the main product image (raw `m.lcp` `url` contains the product id), LCP under 3.0 s; image request start under 1.0 s; CLS under 0.05. Also 3 runs on 2 other products (a ring and a pendant) so the template, not 1 URL, is proven (R16).
- Function: variant switch, quantity, Add to Cart, cart drawer, Razorpay checkout start, on staging on a mid-range Android on mobile data (R99, P2 step 6). Tracking: view_item, add_to_cart and a test purchase fire once each with consent on and off (R48), because the render order of the tracking wrappers changes.
- Field: note the ship date; check PSI field LCP for the origin and Search Console 28 days later (R27).

**Risks and rollback.** Hydration mismatches (visible as console warnings and a flash) if server and client trees differ; fix formatting and conditional rendering. Origin load rises because the server now renders more HTML per request; TTFB is 0.35 s today and the HTML is cacheable, so watch TTFB in the after runs (R82: stay under 0.8 s). Rollback: flip the flag; no data migration.

**Dependencies.** Task 1 first (or the image still queues behind fonts). Task 8 for the CDN hit. Task 5 for the containers below.

### Task 3. Server-render the first collection tiles (rank 3)

**Problem and evidence.** `/m/rings` HTML (85 KB decoded) contains the logo and a tracking pixel image only (audit 5.4). The page shows `loading.gif` (26 KB GIF, LCP at 2.0 to 6.6 s) for about 14 s, then requests 20 tiles at 15.0 to 15.3 s and paints the "Rings (156 found)" grid at 15.2 s with a body shift of 0.059 (raw `m.clsEntries`, `res`). Product and category pages carry most shopper page views (R3, source 06's 72%). Search and filters are Tagalys (CSP allows `api-r1.tagalys.com`).

**Rules and procedures.** R66, R81, R35 and P17 step 4 (first cards eager, rest lazy), R75 (reserve space), R100, P18.

**Estimated gain and basis.** After task 1 the grid appears at about 9.2 s (task 1 model). With the first tiles in the HTML: the 4 tiles in the first viewport (2 per row at 167 px, rows at 259 px and 536 px, raw `imgs`) are about 13 KB each: HTML 18 + fonts 150 + CSS 27 + 4 x 13 = 247 KB; 247 / 185 = 1.3 s; plus TTFB 0.13 s and 0.15 s render = **about 1.6 s**; allow up to 2.5 s. Gain from today's "content seen" moment (15.2 s): about 13 s. The spinner stops being the LCP element.

**Effort.** 16 to 40 h. **Owner.** Dev.

**Steps.**
1. In `pages/m/[category].tsx` (or the route that renders `/m/rings`) add the page-1 listing call to `getServerSideProps`: default sort, no filters, first 12 to 16 products, calling the same Tagalys or GraphQL endpoint the client uses. If Tagalys is client-only by contract, use the GraphQL catalog for page 1 and let Tagalys take over on the first filter or sort.
2. Render the tiles with `next/image`, `sizes="(max-width: 600px) 50vw, 25vw"`, `width` and `height` set from the card ratio. `priority` on the first 4 tiles only (the 2 rows in view); `loading="lazy"` on the rest (P17 step 4 adaptation: `index < 4`).
3. Pass the page-1 result into the client list as initial state so it does not refetch on mount. Filters, sort and paging stay client-side.
4. Skeleton cards (task 5) for positions beyond the server-rendered ones while the client fetches page 2.
5. HTML caching: the tiles carry prices. Serve the category HTML with `Cache-Control: public, s-maxage=300, stale-while-revalidate=600` and purge category URLs on price or stock changes (task 8). If the team prefers no CDN cache for category HTML, keep it `private` and make sure Cloudflare respects it (task 8 step 4).
6. Replace `loading.gif` with the skeleton (task 9 item 4) so no GIF is ever the LCP candidate.

**Verification (P30).** Before: LCP element `loading.gif` at 6.58 s; grid at 15.2 s; CLS 0.110. Freshness: `curl -s https://www.gehnaindia.com/m/rings | grep -o '<a href="/[^"]*ring[^"]*"' | wc -l` returns 12 or more; the first `<img>` tags have `fetchpriority="high"`. After: 3 runs on `/m/rings` and 2 other categories. Pass: LCP element is a product tile `<img>`; LCP under 3.0 s; CLS under 0.05; filters and sort still work; the count "(156 found)" matches the Tagalys count. Tracking: view_item_list and select_item fire once (R48).

**Risks and rollback.** Two sources of truth for the listing (server page 1 vs Tagalys) can disagree on order after a Tagalys re-index; accept for page 1 or use Tagalys server-side. Origin CPU rises; watch TTFB. Rollback: flag.

**Dependencies.** Task 1; task 5 for the skeleton; task 8 for the HTML rule.

### Task 4. Home hero as AVIF, small category icons, `priority` on 1 image only (rank 4)

**Problem and evidence.**
- Hero: `/_next/image?url=/static/images/banner/new-arrivals-mobile.png&w=1200&q=75` returns `image/png`, 278.5 KB transfer, 650 x 1000 natural, in a 393 x 631 box; it is the LCP element at 7.9 s (raw `imgs`, `responses`, `m.lcp`). The desktop file of the same section (`new-arrivals-desktop.png`, `w=1920`) comes back as AVIF, 78 KB. The icons show the same pattern: mobile `w=640` requests on 320 px sources come back as PNG; desktop `w=256` requests on the same sources come back as AVIF (24 to 38 KB). Working hypothesis, to confirm in the code: when the requested width is larger than the source, the optimizer returns the original file untouched [verify UI].
- Category icons: `pendants.png` 234 KB, `nosepins.png` 203 KB, `earrings.png` 165 KB, `bracelets.png` 123 KB, `rings.png` 38 KB, plus 2 smaller, about 805 KB for 7 circles of 60 x 60 CSS px (165 device px), natural 320 x 320, requested at `w=640` (5.3x the box, R30 says flag over 2x). They download from 1.1 s to 16.3 s alongside the hero. All 7 are in view and marked `loading="lazy"` (raw `imgs`).
- 41 `<img>` tags carry `fetchpriority="high"` on home; 1 is in view (the hero at top 206 px), the other 40 sit at 1,052 px, 1,930 px and 2,802 px (raw `imgs` tops). No `<link rel="preload">` exists for the hero (audit 5.7).

**Rules and procedures.** R31 (LCP image under 250 KB, hero under 200 KB), R30 (2x the box, capped), R32 (photos as JPEG, let the resizer serve AVIF), R35 and R36 (in-view images eager, explicit), R37 (high priority on the LCP image only), R41 (slide 1 eager, 2 and 3 lazy: already true), P14, P16, P17, P18 step 7.

**Estimated gain and basis.** Icons: 805 KB to about 70 KB (7 x 10 KB AVIF at 256 px) saves 735 KB = 735 / 185 = 4.0 s of transfer that today overlaps the hero's download window (1.1 to 7.8 s). Hero: 279 KB to about 100 KB saves 179 KB = 1.0 s. Home LCP model after task 1 with these changes: **about 2.2 s** (section 8) versus 3.2 s with task 1 alone. The 40 carousel tiles marked high priority (raw: 40 requests of 10 to 30 KB) stop competing in the first seconds; their bytes move to scroll time.

**Effort.** 4 to 6 h. **Owner.** Dev (plus the designer for the hero export).

**Steps.**
1. Hero source: re-export the mobile banner as a JPEG at 1,080 px wide (2.75 x 393 = 1,081 device px; R30: 2x the box would be 786 px but the optimizer needs a source at least as wide as the `w` it picks, which is 1,200 on this device profile, so export at 1,200 px wide, quality 75 to 80, P14 step 4). The desktop version already converts, so the PNG is not needed for transparency. Target under 150 KB as JPEG so the AVIF output lands under 100 KB.
2. In the hero `<Image>`: `priority`, `sizes="100vw"`, `width={1200} height={1846}` (keep the 650:1000 ratio), no `loading` prop. Confirm the head now contains `<link rel="preload" as="image" imagesrcset="..." imagesizes="100vw" fetchpriority="high">`. If the Next version does not emit it, add it in `pages/index.tsx` `<Head>`.
3. Icons: in the category circle component set `sizes="60px"` (so the optimizer picks `w=128` or `w=256` from `imageSizes` instead of `w=640`) and `loading="eager"` without `priority` (in view, but not the LCP). Or replace the 7 PNGs with 160 px AVIF or SVG files under 10 KB each. Check the result is `image/avif` and under 10 KB.
4. Product tile component: remove `priority` unless a prop `aboveFold` is passed. On home pass nothing (all carousels are below 1,000 px). On collection pages pass `aboveFold={index < 4}`. On product pages the 5 thumbnails (23 px files) can keep `loading="eager"` but not `priority`.
5. Slides 2 and 3: keep `loading="lazy"` (R41). WhatsApp button (31 x 31 source asked at `w=2560`): set `sizes="50px"` or use an inline SVG.
6. Confirm why the PNG passed through unconverted (step 1 hypothesis) by reading the optimizer behaviour for the Next version in `package.json`, and note it in the change log so future uploads follow the rule "source at least as wide as the largest `w` the `sizes` attribute can pick".

**Verification (P30).** Before: hero `image/png` 278.5 KB; icons 805 KB; 41 `fetchpriority="high"`; home LCP 7.88 s. Freshness: `curl -sI "https://www.gehnaindia.com/_next/image?url=%2Fstatic%2Fimages%2Fbanner%2Fnew-arrivals-mobile.jpg&w=1200&q=75" -H "Accept: image/avif,image/webp,*/*"` shows `content-type: image/avif` and `content-length` under 102,400. `curl -s https://www.gehnaindia.com/ | grep -o 'fetchpriority="high"' | wc -l` returns 1. After: 3 runs. Pass: home LCP under 3.0 s with task 1 done; above-fold image bytes (hero + 7 icons + logo) under 250 KB; carousel tiles do not appear in the Network log until scroll. Visual check: icons crisp on a 3x screen (256 px source for a 165 px box is fine).

**Risks and rollback.** A JPEG hero loses transparency if the design relied on it (the desktop version does not, so unlikely). Icons at 256 px could look soft on a tablet where the box is larger; check the tablet breakpoint. Rollback: revert the component props and the image files.

**Dependencies.** Task 1 (the estimate assumes fonts are small). Independent of tasks 2 and 3.

### Task 5. Reserve space for late content (rank 5)

**Problem and evidence.** Collection: shift 0.025 on `DIV.MuiGrid-item jss70` at 13.6 s, then 0.059 on `BODY` at 15.2 s when the grid replaces the spinner; CLS 0.110 in all 3 runs. Product: 0.025 on `DIV.MuiGrid-item jss50` at 14.4 s, then 0.080 on `BODY` at 16.6 s when the "Two Decades of Expertise, Glowing Reviews" band renders and pushes the gallery down; CLS 0.129 to 0.131 (raw `m.clsEntries`; screenshot `raw-b/product-emerald-ring-mobile-slow4g-run2.png`). Identical across runs, so structural (R74). Home CLS 0.000, desktop home 0.004.

**Rules and procedures.** R74, R75 (reserve space for anything that arrives late), P19 step 6, P20 steps 2 and 4, R38 (images already have dimensions: pass).

**Estimated gain and basis.** Removing the two body-level shifts: collection 0.110 - 0.059 = **0.051**; product 0.129 - 0.080 = **0.049**. Both under the 0.1 "good" line; the remaining 0.025 grid-container shifts disappear when the content is server-rendered (tasks 2 and 3) or when the skeleton has the exact height.

**Effort.** 3 to 4 h. **Owner.** Dev.

**Steps.**
1. Measure the rendered heights at 393 px wide: the reviews band on the product page and the filter and sort bar plus grid header on the collection page (DevTools, Elements, hover the container; note height at 393 px and at 360 px and 414 px).
2. Reviews band: give its container `min-height` equal to the measured height on mobile (a media query for the desktop height) so its space exists before it renders. Better: render the band's static text ("Two Decades of Expertise", the 4.8/5 line) on the server (task 2 step 6) and only the dynamic count client-side.
3. Collection: replace the centered spinner with a skeleton grid: 2 columns of MUI `Skeleton variant="rectangular"` cards at the tile pitch measured from the raw data (rows at 259, 536, 813 px, so a 277 px pitch per row at 167 px width), 8 cards, plus a skeleton row for the sort and filter bar at its real height. The grid container gets the same `min-height` as 4 rows of tiles.
4. Product: the gallery box gets an `aspect-ratio` matching the product images (raw: slide box 361 px wide) so the spinner and the image occupy the same space.
5. Check each breakpoint you care about (360, 393, 414, 768 px); a fixed height can clip a responsive widget (P20 step 2).

**Verification (P30).** Before: CLS 0.110 and 0.129, `BODY` shifts at 15.2 s and 16.6 s. After: 3 runs each; pass when CLS is under 0.05 and no `clsEntries` source is `BODY`. Also check desktop CLS on collection and product (not measured in the audit; R10).

**Risks and rollback.** Over-reserved space leaves a gap when the band is shorter (for example when the review count is hidden). Rollback: remove the CSS rule.

**Dependencies.** None. Ship before tasks 2 and 3 so the skeleton is ready for them.

### Task 6. Test Rocket Loader off and stop gating data fetches on the load event (rank 6)

**Problem and evidence.** On all 3 templates the first heavy main-thread work starts within 0.1 s of the load event and the load event is held open by the 2 preloaded fonts: product run 2 fonts end 14.24 s, load 14.31 s, first long tasks 14.25 s (72, 148, 299, 350, 193, 1,094 ms), GraphQL calls at 16.66 s; collection fonts end 13.26 s, load 13.52 s, long tasks from 13.31 s; home fonts end 19.16 s, load 19.34 s, long tasks from 19.18 s (raw `m.longtasks`, `nav.load`, `res`). The JavaScript files had all arrived 4 to 9 s earlier (product `_app` chunk done 8.98 s). Cloudflare Rocket Loader is on (a 4 KB script that takes over script execution; audit 5.3) and it is the usual reason a page's own scripts run only after load. The third-party tags correctly start after load (that part should stay).

**Rules and procedures.** R55 (be skeptical of speed scripts; test them like any change), R26 (1 change at a time), R46 (defer first; never touch unknown scripts: here every script is known), R84 (INP: less JS on the main thread), P9 adaptation, P30.

**Estimated gain and basis.** Done alone (fonts still present): script execution could start when `_app` arrives (8.98 s) instead of at 14.3 s: 8.98 + 2.3 + 1.2 + 1.5 = **about 14.0 s** product LCP, a 4.3 s gain. After task 1 the load event moves to about 4.5 s, so the extra gain is small; the reason to still do it is that Rocket Loader reorders Next's own chunk execution, which is a hydration risk and cannot be controlled from the repo. This is a hypothesis test, not a promise (7.14 logic: promise no percentage).

**Effort.** 1 to 3 h. **Owner.** CF for the toggle, Dev for the code check.

**Steps.**
1. Cloudflare dashboard > Speed > Optimization > Content Optimization > Rocket Loader: off. (Also review "Auto Minify" and "Mirage"; leave them unless they show in the waterfall.) [verify UI]
2. Wait 2 minutes. Run 3 slow 4G loads of the product page and the home page. Compare `nav.load`, first long task time and the GraphQL start time with the audit values.
3. If long tasks still start only at load: search the code for `window.addEventListener('load'`, `document.readyState === 'complete'`, `onload` and `useEffect` hooks that wait for a "ready" flag before calling Apollo or Tagalys. Move product and listing fetches to run on mount (or, with tasks 2 and 3, not at all for the first paint). Keep GTM, Meta, Klaviyo and Clarity on `next/script` `strategy="lazyOnload"` or the existing after-load hook (R47: they are not part of the buying flow).
4. Confirm Rocket Loader stays off in the Cloudflare config and note it in the change log.

**Verification (P30).** Before: product first long task 14.25 s, GraphQL 16.66 s, load 14.31 s. After: first long task within 1 s of the last JS chunk's arrival; GraphQL start at least 4 s earlier than before; LCP lower. Function: full site click-through (menu, search, filters, variant, cart, checkout start) because script order changed; tracking events once each (R48).

**Risks and rollback.** Turning Rocket Loader off can make third-party scripts run earlier if any were only deferred by it; check that the after-load behaviour for GTM and Klaviyo survives (audit 3.3 says the app itself holds them until load, so it should). Rollback: toggle on again.

**Dependencies.** None; run in week 1 while task 1 is being built.

### Task 7. JavaScript diet (rank 7)

**Problem and evidence.** Long tasks total 5.8 s on home (25 tasks, max 876 to 911 ms), 3.2 to 3.6 s on collection (one 1,254 to 1,324 ms task), 3.9 s on product (max 915 to 1,094 ms); TBT est 2.6 to 4.0 s on a 4x slowed CPU. First-party JS before load: 443 KB in 30 files (home), 461 KB in 33 (collection), 599 KB in 38 (product); `_app` chunk 145 KB on every page; home DOM 3,128 nodes with 152 `<img>` tags, most in carousels (raw `res`, `m.longtasks`, `domNodes`, `imgs`). A `reactPlayerFilePlayer` chunk loads on the product page for 1 `<video autoplay preload="auto">` (raw `videos`). Collection and product pages prefetch each other's chunks (audit 5.3).

**Rules and procedures.** R83, R84 (INP maps to add to cart, variant pickers, filters), R62 (split code by page type; after images and scripts), R58 (Partytown at rebuild time only), R67 (no effects libraries on in-view elements), R26.

**Estimated gain and basis.** Main-thread time is CPU-bound and did not move in the task 1 model. No measured basis exists yet for a seconds figure; the target is set from the thresholds: TBT est under 1 s, no long task over 200 ms, DOM under 1,500 nodes on home. Each step is measured on its own (R26) and the change log records the gain.

**Effort.** 24 to 40 h over 2 to 3 weeks. **Owner.** Dev.

**Steps.**
1. `npm i -D @next/bundle-analyzer`, wrap `next.config.js`, run `ANALYZE=true npm run build`. Record what is in `_app` (145 KB): expect Material UI, Apollo, Swiper, tracking wrappers, possibly `react-player`, date or currency libraries.
2. Material UI: import from component paths (`@mui/material/Button`) or enable the SWC `modularizeImports` transform so only used components ship. Same for icons (`@mui/icons-material/X`).
3. Move page-only libraries out of `_app`: Swiper to the pages with a carousel; the video player to the product page and only when a video exists, using `next/dynamic`. Replace `react-player` with a native `<video preload="none" playsInline muted controls poster=...>` (R96; also task 9 item 5).
4. Home: render each below-fold carousel with `next/dynamic` and mount it when it enters the viewport (an `IntersectionObserver` wrapper), with 6 to 8 tiles on mobile instead of the full list; keep the server HTML for the first 2 sections. Goal: DOM under 1,500 nodes, `<img>` tags under 40 at load.
5. `<Link prefetch={false}>` on tiles inside grids and carousels; keep prefetch on the main navigation.
6. Product page: the 6 GraphQL calls after load: merge into 1 or 2, request only fields the sections render (R69, item 1.11.1).
7. After each step: build, 3 runs, record TBT est, long task count and max, bytes of JS before load.

**Verification (P30).** Before: TBT est 3.98 / 2.64 / 3.00 s; max long task 889 / 1,254 / 1,094 ms; home DOM 3,128. After each step: 3 runs; step passes if TBT est or max long task fell and nothing broke. Final pass: TBT est under 1.0 s on all 3 templates; no long task over 200 ms. Function tests after every step: carousels swipe, variant change, filters, Add to Cart, cart drawer, checkout start; tracking once (R48).

**Risks and rollback.** Dynamic imports can move content out of the server HTML (SEO and LCP risk) if `ssr: false` is used carelessly; use `ssr: true` for anything with product content. Rollback per step (git revert of that commit).

**Dependencies.** Measure after tasks 1 to 3 first, so the gains can be attributed (R102).

### Task 8. Cache rules for resized images and HTML (rank 8)

**Problem and evidence.**
- `/_next/image` responses for the static banners and icons carry `cache-control: max-age=1800, stale-while-revalidate` and were `x-cache: Miss from cloudfront` (hero, `earrings.png`); product images from `cdn-assets.gehnaindia.com` carry `max-age=86400` but were also CloudFront misses at test time (`jnrhmi8w...&w=1200` miss, `age` 19 to 21 s) (raw `responses`). Correction to the audit's Problem 7: the 30-minute rule applies to the `/static/images` banners and the GIFs; product photos already get 1 day, and they still missed. On a miss the origin resizes: the desktop hero (78 KB) took 4.2 s on an unthrottled line; the product main image (25 KB) took 1.5 s on slow 4G versus 0.4 to 0.5 s for hits of similar size.
- HTML: home `max-age=1800, s-maxage=86400, stale-while-revalidate`, CloudFront hit, `x-nextjs-cache: HIT`. Collection and product `private, max-age=1800, must-revalidate`, CloudFront miss, but Cloudflare `cf-cache-status: HIT` with `age` 21 to 3,420 s. So a Cloudflare rule caches pages the app marks private (R86 check).
- `/cart` answers 307 to `/404?pageType=product&slug=cart`, `cf-cache-status: BYPASS` (audit 5.9, 5.12).

**Rules and procedures.** R85 (verify from headers), R86 (never cache visitor-specific pages), R87 (static long TTL with versioned URLs; HTML brief; prices with fast invalidation), R90 (cache keys include content-changing parameters; 80%+ hit rate), P26 steps 1, 3, 4, 6, 9, P27 steps 3 to 5. R91: this comes after the fundamentals, which is why it is rank 8, but the image part is a config line and gates task 2's estimate, so it ships in week 1.

**Estimated gain and basis.** Per CDN miss avoided: 1.5 s (product main image, slow 4G) to 4.2 s (desktop hero). No site-wide figure without the CDN hit rate [needs brand data: Cloudflare and CloudFront cache analytics]. For the LCP image on a server-rendered product page (task 2) a miss would turn a 2.0 s LCP into 3.5 s.

**Effort.** 3 to 4 h. **Owner.** Dev (next.config.js) and CF (CloudFront behaviour, Cloudflare rules).

**Steps.**
1. `next.config.js`: `images: { minimumCacheTTL: 2592000 }` (30 days). The image URL already encodes the source file and width, and product image ids change when a photo changes, so long caching is safe (R87). Static banners: change the file name when the design changes.
2. CloudFront: on the behaviour for `/_next/image*`, cache policy must include the query string (all parameters) and the `Accept` header in the cache key (AVIF vs WebP vs PNG responses differ by `Accept`), and use origin `Cache-Control` for TTL with a default TTL of 30 days. Check the origin request policy forwards `Accept`. [verify UI]
3. Cloudflare: check the cache rule for `/_next/image*` (it should cache with the query string; Cloudflare respects origin headers by default). Confirm `cf-cache-status: HIT` on a second request.
4. HTML rule, decide 1 of 2 (R86, R87):
   - a) Cacheable at the edge: the app sends `public, s-maxage=300, stale-while-revalidate=600` for product and category HTML (no visitor-specific content in the HTML; cart and account are client state), and the catalog service purges the product URL and its category URLs on price or stock change via the Cloudflare purge API. Faster for the next shopper; needs the purge hook.
   - b) Not cacheable: keep `private` and remove the Cloudflare rule that overrides it; rely on the origin (TTFB 0.35 s today). Simpler; no purge needed.
   Do not leave the current state, where `private` HTML is served from Cloudflare for up to 57 minutes without a purge path (audit 5.9).
5. Make `/cart` either the cart route or a 301 to the right page; make unknown URLs return HTTP 404 (task 9 item 6).
6. After any change: cart drawer, Add to Cart and checkout start on a fresh device (P26 step 9).

**Verification (P30).** Before: headers as listed. After: `curl -sI -H "Accept: image/avif" "<product image url>"` twice, second shows `x-cache: Hit from cloudfront` and `cache-control` with `max-age=2592000`; a product page in a fresh incognito window shows the chosen HTML rule; a price change in admin shows on the product and category page within 5 minutes (P26 step 6). CDN dashboards: image hit rate over 80% after 1 week (R90) [needs brand data].

**Risks and rollback.** A stale price if option a) ships without the purge hook; test the hook before enabling. Rollback: revert the config and rules.

**Dependencies.** None for images (ship in week 1). The HTML rule waits for tasks 2 and 3 (that is when prices enter the HTML).

### Task 9. Clean-ups (rank 9)

**Problem and evidence.** Raw `scripts` on the product page: `www.google-analytics.com/analytics.js` (async) and `googletagmanager.com/gtag/js?id=UA-41818105-2` (Universal Analytics, which Google stopped processing) plus `gtag/js?id=G-FT109JXEC7` (GA4) plus `gtm.js?id=GTM-PK4C6HK` (which loads gtag again) plus `cdn.js.customerlabs.co/cl861926ufst6h.js` (HTTP 403 in the audit) plus Klaviyo (6 files) plus Cloudflare Insights plus Google Sign-In. `loading.gif` 25.6 KB (`image/gif`, `max-age=1800`, CloudFront miss) on every collection and product page; `gehnaMiniLogo.gif` 43.9 to 52.9 KB on the product page; a `<video autoplay preload="auto">` on the product page (raw `videos`; the audit's 5.11 said no video tags, the product raw file shows 1, below the fold, 0 KB transferred in the run because the range request was cut off); unknown URLs answer 307 to `/404?...` (audit 5.12); `swiper-icons` font declared and never loaded (raw `fonts`).

**Rules and procedures.** R44 (remove residual tracking after confirming what replaced it), R48 (event tests before and after any pixel change), R54 (tag manager as inventory and kill switch), R96 (never GIF; `preload="none"`; no autoplay on mobile), R97 (real 404s, no temporary redirects for missing pages), P8 adaptation (grep the repo and the GTM container instead of theme.liquid), P24, P25.

**Estimated gain and basis.** Bytes: UA tag and `analytics.js` plus `ec.js` (audit: about 20 to 40 KB, after load), `loading.gif` 26 KB and `gehnaMiniLogo.gif` 44 to 53 KB (before LCP on product), CustomerLabs request (403, 0 KB but a connection): about 100 to 190 KB and 4 to 6 requests per page view. Time: small on LCP after tasks 1 to 3; the GIF removals matter on the product page only until task 2 lands. The 404 fix stops soft 404s hitting the origin (`BYPASS`).

**Effort.** 6 to 8 h. **Owner.** Dev; Owner for the GA and CustomerLabs decisions.

**Steps.**
1. Universal Analytics: open the GTM container (GTM-PK4C6HK) and the app code; find where `UA-41818105-2` and `analytics.js` are loaded. Confirm GA4 `G-FT109JXEC7` carries view_item, add_to_cart, begin_checkout and purchase (GA4 DebugView on staging). Then remove the UA tag and `analytics.js` plus `ec.js`. [needs brand data: whether any report still reads UA]
2. Duplicate gtag: keep 1 loader (GTM), remove the direct `gtag/js?id=G-...` tag if GTM already loads it; verify each event fires once (R48 tests: page view, view_item, add_to_cart, purchase; consent accepted and refused).
3. CustomerLabs: ask the owner whether the account is live; if not, remove the script and its CSP entries. If it is, find out why the script returns 403 from a US proxy (geo-block is fine; an expired plan is not).
4. `loading.gif`: replace with the MUI skeleton (task 5) or a CSS spinner; delete the GIF request.
5. `gehnaMiniLogo.gif`: export as SVG or a 2x AVIF under 5 KB; `loading="lazy"` if below the fold.
6. Product video: `preload="none"`, `playsInline`, `muted`, a `poster` image, no `autoplay` on mobile (show a play button); lazy-mount the player (task 7 step 3).
7. 404: in the catch-all route return `res.statusCode = 404` (in `getServerSideProps` return `{ notFound: true }`) instead of a 307 redirect to `/404?...`. Keep the custom 404 page and add links to the top 2 categories (P25 step 4). Decide what `/cart` should do.
8. Remove the `swiper-icons` `@font-face` declaration.
9. Record each removal in the change log and re-test one at a time (R26).

**Verification (P30).** Before: script list as above; `curl -sI https://www.gehnaindia.com/this-does-not-exist` shows 307. After: no request to `UA-41818105-2`, `analytics.js`, `loading.gif`, `customerlabs` (if removed); `curl -sI` on a bad URL shows 404 and `cf-cache-status` not BYPASS; GA4 DebugView shows each event once; Meta Events Manager test events show once. 3 runs to confirm nothing regressed.

**Risks and rollback.** Losing an event if UA was the only carrier of a conversion; that is what step 1 checks. Rollback: restore the tag from the GTM version history (R54 kill switch).

**Dependencies.** Task 6 (script execution order settled before the event tests).

### Task 10. Monitoring and performance budget (rank 10)

**Problem.** Nothing in the deploy pipeline stops a 1 MB font or 40 `priority` images from coming back (R8: stores slow down over time).

**Rules and procedures.** R8, R57 (third-party count as a budget metric), P29, P30 step 5, R27.

**Steps.**
1. Lighthouse CI: `npm i -D @lhci/cli`; `lighthouserc.js` with `collect.url` = the 3 reference URLs on the staging deploy, `settings.preset = 'perf'`, mobile emulation, 3 runs; `assert.assertions` for `largest-contentful-paint` max 2,500 ms (warn) and 4,000 ms (error), `cumulative-layout-shift` max 0.1, `total-blocking-time` max 600 ms (warn), `resource-summary:font:size` max 153,600 bytes, `resource-summary:total:size` max 1,572,864 bytes, `resource-summary:third-party:count` max 10. Run on every pull request that touches `pages/`, `components/`, `next.config.js`, fonts or `public/`.
2. Monthly: the raw-b instrument (3 runs, same profile) on the 3 templates plus a cart drawer and a checkout start; store the JSON next to the baseline; compare medians.
3. PSI: once the quota allows, weekly PSI API runs on the 3 URLs into a sheet (free key); read lab and field.
4. Field: 28 days after each release, read PSI field data (origin and URL) and Search Console Core Web Vitals; log the values (R27).
5. Rules of the road for the team: any new third-party script, font, hero or carousel gets a before-and-after 3-run test and a change log entry before it goes live (R45); freeze changes for 2 weeks before a sale window (R8, P31 step 6).

**Verification.** A pull request that adds a 900 KB font fails the CI budget. **Effort.** 6 to 8 h. **Owner.** Dev sets up CI; Agent runs the monthly and 28-day checks.

### 1.11 Further items (not in the top 10)

1. **API field selection (R69).** The product page makes 6 GraphQL calls after load (raw `res`, 16.7 to 18.7 s). Inspect payloads; return only the fields each section renders; merge calls. Dev, 8 to 16 h, after task 2.
2. **Real device and checkout tests (R10, R25, R98, R99, P2 step 6).** Cart drawer, Add to Cart, variant switch, Razorpay checkout on a mid-range Android on mobile data; count form steps; time the payment step. Not measured in the audit (5.17, 5.18). Owner or Agent with a phone, 2 h, before and after each release.
3. **Site-wide crawl (P5).** `npx unlighthouse --site <staging url>` to find outlier templates (blog, static pages, lab-grown diamonds landing). Needs staging and the owner's go-ahead. Agent, 2 h.
4. **Peak readiness (P31, R94).** Before the Diwali sale window: capacity check for the GraphQL API (the product page's slowest step under load), load test Add to Cart, search and checkout, change freeze. Dev and CF, 1 day. [needs brand data: sale calendar]
5. **Field INP (R84).** Add a RUM source (Search Console CWV report, or `web-vitals` library posting to GA4) so INP is visible; the lab TBT numbers are a stand-in. Dev, 2 h.
6. **Desktop CLS on collection and product (R10).** Not measured; 1 run each with the instrument. Agent, 30 min.
7. **Tablet and 360 px checks** after tasks 4 and 5.

## 2. Dependencies

```
Task 0 (baseline) -> everything
Task 1 (fonts) -> 2, 3, 4 (their estimates assume small fonts)
Task 5 (reserve space) -> 2, 3 (skeleton and containers reused)
Task 8 images part -> 2 (LCP image must be a CDN hit)
Task 8 HTML part <- 2, 3 (prices enter the HTML)
Task 6 (Rocket Loader, load gating) -> 9 (tracking tests after script order settles)
Tasks 1, 2, 3 measured -> 7 (JS diet gains must be attributable)
Task 10 (CI) <- 0 (budget values from the baseline), should be live before task 7's many small commits
```

One change per release, 3 runs between releases (R26, R15). Tasks 1, 4, 5, 6, 8-images are each small enough to be 1 release; task 2 and task 3 are each 1 release behind a flag; task 7 is several releases; task 9 is 1 release per item that touches tracking.

## 3. Sequencing plan

**Week 1: weight and priority.**
- Day 1: Task 0 (baseline; PSI as soon as the quota allows). Task 6 Rocket Loader test (CF toggle, 3 runs, decision).
- Days 1 to 2: Task 1 fonts. Release, 3 runs.
- Day 3: Task 8 image cache (`minimumCacheTTL`, CloudFront cache key). Release, header checks.
- Days 3 to 4: Task 4 hero, icons, `priority` clean-up. Release, 3 runs.
- Day 5: Task 5 reserve space and skeletons. Release, 3 runs. Task 10 Lighthouse CI scaffolding started.
- Expected after week 1 (model, slow 4G lab): home LCP about 2.2 to 3.2 s (from 7.9), page weight about 1.3 MB (4,036 KB minus 1,771 fonts minus 735 icons minus 178 hero, before the lazy carousel tiles), product LCP about 9.4 s (from 18.3), collection grid about 9.2 s (from 15.2), CLS about 0.05 on both (from 0.11 and 0.13). Product and collection are still far from 2.5 s; that is week 2 and 3.

**Week 2: the product page.**
- Task 2 server-rendered buy box with the preloaded main image, behind a flag; task 9 items 4, 5, 6, 7, 8 (GIFs, video, 404, font declaration) in the same sprint as separate commits; task 10 CI live with the budget.
- Expected after week 2: product LCP about 2.0 to 2.5 s if task 2 ships on time (the 24 to 80 h range means it may slip into week 3); product CLS near 0; product page weight down a further 70 to 80 KB from the GIFs.

**Week 3: the collection page and JavaScript.**
- Task 3 server-rendered first tiles; task 8 HTML rule decision and purge hook; task 7 round 1 (bundle analysis, MUI imports, Swiper and video player out of `_app`, prefetch off in grids); task 9 items 1 to 3 (tracking) with the R48 event tests.
- Expected after week 3: all 3 templates LCP about 2.5 s or under on the slow 4G lab test; CLS under 0.05 everywhere; TBT est down but likely still over 1 s (JS diet continues); third-party hosts 7 to 8.

**Week 4 and after.** Task 7 rounds 2 and 3 (carousel virtualization, DOM under 1,500, API field selection); real-device and checkout tests; 28-day field checks for each release; peak readiness before the sale window; monthly instrument runs.

## 4. Performance budget (P29, R8, R31, R57; chosen values, not sourced, per conflict 7.19)

Per template, mobile, first visit, slow 4G lab profile (the raw-b instrument or Lighthouse mobile):

| Item | Budget | Today (home / collection / product) |
|---|---|---|
| Page weight before load | 1.5 MB | 3.54 / 2.42 / 2.56 MB |
| Fonts | 150 KB, WOFF2 only, 4 files max | 1,921 KB, 4 TTF |
| Largest image (LCP image) | 100 KB AVIF (hard stop 250 KB, R31) | 279 KB PNG / 26 KB GIF / 25 KB AVIF |
| Any image | 100 KB product, 200 KB hero; 500 KB hard stop | icons 123 to 234 KB |
| Images with `fetchpriority="high"` | 1 | 41 / 16 / 6 |
| In-view images marked lazy | 0 | 10 / 18 / 5 |
| LCP | 2.5 s (warn), 4.0 s (fail) | 7.9 / 6.6 (grid 15.2) / 18.3 s |
| CLS | 0.05 (warn), 0.1 (fail) | 0.000 / 0.110 / 0.129 |
| TBT est | 600 ms (warn), 1,000 ms (fail) | 3,981 / 2,638 / 3,000 ms |
| Longest task | 200 ms | 889 / 1,254 / 1,094 ms |
| First-party JS before load | 350 KB | 443 / 461 / 599 KB |
| Third-party hosts per page | 10 | 8 to 9 |
| DOM nodes | 1,500 | 3,128 / 1,297 / 1,299 |
| GIF files | 0 | 0 / 1 / 2 |
| TTFB | 800 ms | 429 / 128 / 345 ms |
| Content in server HTML | main image, h1, price, first 12 tiles | none on collection and product |

Cadence: every pull request (CI), monthly (instrument), after any change to fonts, `_app`, hero, carousels or third-party tags, 2 weeks before a sale, and 28 days after each release for field data.

## 5. Business case (P6, R9; arithmetic in section 8)

Private inputs from the audit's section 6.1 (Metabase dashboard 6 export in the repo, 25 Aug to 23 Sep 2026; keep out of anything public):
- Website sales ₹96,83,409; orders 285; AOV ₹33,977; visits 6,34,288 (GA "visits", definition unconfirmed [needs brand data]); add-to-carts 12,053.
- Daily: 21,143 visits x 0.045% x ₹33,977 = ₹3,22,780 a day; x 365 = ₹11.78 crore a year (last 30 days annualised, no seasonality).

Assumed lift scenarios (flat lift in conversion rate after the product and collection pages go from 15 to 18 s to about 2.5 s on slow mobile; the sources' per-second figures cannot be multiplied by a 15 s gain, so flat scenarios are used and every one is an assumption):

| Assumed lift | Extra sales per 30 days | Extra sales per year | Basis |
|---|---|---|---|
| +3% | ₹2.9 lakh | ₹35.3 lakh | conservative, below every source |
| +5.6% | ₹5.4 lakh | ₹66.0 lakh | source 06, "+5.6% per 1 s faster", uncited |
| +7% | ₹6.8 lakh | ₹82.5 lakh | source 04 citing Cloudflare, "about 7% per 1 s delay" |
| +10% | ₹9.7 lakh | ₹1.18 crore | assumption for a multi-second gain |

Cost side: developer effort in this plan is 4 to 8 (task 1) + 24 to 80 (2) + 16 to 40 (3) + 4 to 6 (4) + 3 to 4 (5) + 1 to 3 (6) + 24 to 40 (7) + 3 to 4 (8) + 6 to 8 (9) + 6 to 8 (10) = 91 to 201 hours, about 12 to 25 developer days. At [needs brand data: developer day rate] the cost is that many days times the rate. Even the +3% scenario (₹2.9 lakh per 30 days) pays for 25 developer days within a few months at typical Indian agency rates; the owner should put the real rate in.

Direction benchmarks (third-party, stated as such, at most 1 per point per conflict 7.9): Portent (source 03) found a site loading in 1 s converting about 2.5x one loading in 5 s; Google's mobile figure (sources 04, 06, 09) is that 53% of visitors leave a mobile page that takes over 3 s. Gehna's product page shows nothing to buy for 17 s on slow 4G today.

Ad-spend angle (P6 step 4): every paid click that lands on a product page and leaves before the image appears is a click paid for and never shown the product. [needs brand data: monthly Meta and Google spend, paid sessions, bounce rate on product landing pages, mobile share of sessions and revenue.] The Meta gallery data can give spend and landing URLs; it was not read for this plan.

What will count: Gehna's own before and after, same pages, same 3-run test, then conversion by device for the 28 days after each release (R102, P30). Nothing in the table above is a forecast.

## 6. Proof protocol and change log (P30, R102, R103, R104)

Change log row (one per release):

| Date | Page | Device and tool | Before (3-run median) | After (3-run median) | What changed | Other changes in the batch | Freshness confirmed | Function tests | Event tests (consent on / off) | Field check date (+28 d) | Owner |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 24 Sep 2026 | home, /m/rings, product | Pixel 5 emu, slow 4G, raw-b instrument | see audit 2.2 | | baseline | none | yes | n/a | n/a | 22 Oct 2026 | Agent B |

Per release: wait 2 minutes after deploy, purge the page URL at Cloudflare if `age` shows an old copy, confirm the marker (a new hash in the `_next/static` chunk names is the marker on this stack), run 3 loads per page, record medians, describe the slow 4G visual test in words, run the function tests listed in the task, run the tracking tests if the task touches scripts, share the PSI report link when PSI is available.

## 7. Notes and corrections to the audit found while checking the raw files

- Audit 3.2 says "36 JavaScript chunks, about 480 KB" on home; the raw file lists 44 first-party `.js` resources totalling 483 KB, of which 30 (443 KB) finish before the load event. Same conclusion.
- Audit Problem 7 says `/_next/image` responses cache for 30 minutes. That is true for the static banners and icons (`max-age=1800`); product photos from `cdn-assets` carry `max-age=86400` and were still CloudFront misses in the test. Task 8 covers both.
- Audit 5.11 says no video tags. The product page raw file has 1 `<video autoplay preload="auto">` (source `cdn-assets.gehnaindia.com/mjcl07kxuhwkfqf72l887wrcp3nv`, `video/mp4`) and a `reactPlayerFilePlayer` chunk. Task 9 item 6.
- New finding from the raw timing (not in the audit): script execution starts only at the load event on all 3 templates, and the load event is held by the preloaded fonts. This makes the font fix worth more than its bytes and is the basis of task 6.
- The 5 remaining `fetchpriority="high"` product thumbnails on the product page are 23 px files; harmless, cleaned up in task 4 step 4.

## 8. Arithmetic (run in code)

```
effective throughput KB/s: home 187.41 product 183.14 used 185.28 (nominal 1.6 Mbps = 200 KB/s)
fonts saved KB 1771.2 = transfer seconds at used throughput 9.56
home LCP model, PNG hero as today : bytes 494.5 -> 3.2 s (today 7.88 s)
home LCP model, AVIF hero 100 KB : bytes 316.0 -> 2.24 s (today 7.88 s)
product after Task 1 only: JS done 4.38 load~ 4.48 LCP~ 9.38 s (today 18.26 s) gain 8.88
product Rocket Loader off alone (hypothesis): LCP~ 13.98 gain 4.28
product after Tasks 1+2 (+8 cache hit): LCP~ 2.01 s; on a CloudFront miss add the origin resize wait (desktop hero miss took 4.2 s)
collection grid visible after Task 1 only: 9.17 s (today ~15.2 s)
collection after Tasks 1+3: LCP~ 1.61 s
collection CLS after Task 5: 0.110-0.059 = 0.05 ; product 0.129-0.080 = 0.05 ; after SSR both ~0
home category icons now KB 804.8 target 7 x 10 = 70; saved 734.8 KB = 3.97 s of transfer
AOV 33,977; CR 0.045%; daily 322,780; annual 117,814,810
lift 3.0%: +290,502 per 30 days, +3,534,444 per year
lift 5.6%: +542,271 per 30 days, +6,597,629 per year
lift 7.0%: +677,839 per 30 days, +8,247,037 per year
lift 10.0%: +968,341 per 30 days, +11,781,481 per year
```

Model inputs: bytes and times are run 2 medians from the raw files; throughput is bytes-before-load divided by (load minus TTFB); "work", "GraphQL" and "image" durations are the measured gaps on the product page run 2 (14.25 to 16.6 s, 16.66 to 17.9 s, 16.45 to 17.97 s). The model ignores request overhead and parallelism beyond the throughput cap, so it is a rough guide; the pass thresholds in each task leave room for that.

Total estimated LCP after all tasks, slow 4G lab: home about 2.2 s, product about 2.0 to 2.5 s, collection about 1.6 to 2.5 s. All three at or under the 2.5 s "good" line, subject to proof.
