# Ecommerce Site Speed Optimization: Complete Guide for 2026

source_id: 1jotScp6YXxT1RXu1mdtsy3UrfcNnjUCu  |  folder: /08-SPD-speed  |  cards: 17  |  words: 5492  |  type: article
credibility: Jakub Rusniok, founder of Ecomhint. Ecomhint sells store speed and conversion audits ("1350+ stores audited", "Run Free Audit" boxes appear 3 times). Evidence: cited third-party research (Google, NitroPack, Cloudflare, Queue-it, Unbounce, HTTP Archive, web.dev case studies, Salesforce and BlueHost docs) plus Ecomhint's own "Shopify Speed Benchmark 2026" of 1,533 Shopify stores (correlation and median scores). No method detail for the benchmark in this text.
date signals: Published 25 March 2026. Uses INP (replaced FID). Cites "HTTP Archive 2025". Names 2026 tools and prices (shared hosting $1 to $15 a month, VPS $20 to $50).

## 1. What this source is for

Use it to set speed targets (load time, PSI score bands, Core Web Vitals), to decide the order of fixes (the "Speed Fix Priority Ladder": images, then third-party scripts, then hosting and CDN), and to plan caching, CDN, hosting tier, testing tools and ongoing monitoring for Shopify and WooCommerce stores. It is the most complete source in this batch on caching rules (what never to cache) and CDN setup.

## 2. Principles

1. **Fix in this order if you can do only 3 things: images, then third-party scripts, then hosting and CDN.** Condition: limited budget. Code work (JS bundles, cache headers) comes after these 3. Basis: images "often" cut page weight 40% to 60% with WebP; scripts compete for browser resources; shared hosting throttles. [c35b62b83860]
2. **Speed is revenue work.** Condition: use the research as direction, not a forecast. Figures: 0.1 s faster = up to 8.4% more retail conversions (Google/NitroPack); 1 s delay = about 7% fewer conversions (Cloudflare); about 4% lost per 2 s (Cloudflare); 1 s site converts about 5x a 10 s site; 53% of mobile visitors leave after 3 s; 63% leave after 4 s (Queue-it); 70% say speed affects purchase (Unbounce). [41ce06260ce9]
3. **Core Web Vitals are an SEO tie-breaker, not the main factor.** Condition: pages with similar content quality on competitive keywords. Google uses mobile-first indexing, so mobile speed decides ranking potential. About 50% of mobile sites pass CWV (HTTP Archive 2025). [04439b080448]
4. **Each CWV maps to specific store elements.** LCP: main product image on PDP, hero or first grid on category and home. INP: app, plugin and tracking JavaScript; the "Add to Cart does nothing for half a second" symptom; filters on category pages. CLS: images without dimensions, cookie banners and injected content, font reflow. [2969a152a99d]
5. **Third-party script count is the strongest predictor of Shopify speed in the author's data.** Condition: Shopify stores in Ecomhint's 1,533-store dataset. r = -0.66 between third-party service count and performance score. 0 to 5 services: median mobile score 74. 21 to 30 services: 44. [c09e2fd0f0d7]
6. **Industry stack weight matters.** Beauty: median 31 third-party services per page, last of 9 Shopify industries for mobile speed. Automotive parts: median 15, first. Fashion and apparel in between (sizing charts, shipping insurance add load). [c09e2fd0f0d7]
7. **Never lazy-load above-the-fold images.** Condition: hero and first visible products. Lazy-loading them "actually hurts LCP". [8883db1cfb1d]
8. **Never cache cart, checkout or account pages.** Condition: any page with visitor-specific data. [9490c0550ad4]
9. **Prioritize pages by traffic and conversion impact.** "A 0.5-second improvement on a page with 10,000 monthly visitors matters more than a 2-second improvement on a page with 100 visitors." Start with homepage, top product pages, main category pages, then checkout. [4b59118db903] [needs brand data: sessions and revenue by page]
10. **Stores slow down gradually.** More products, apps and tags accumulate. Monitor on a schedule and set a performance budget. [9ffe9f981c57] [c09e2fd0f0d7]
11. **Often 1 problem causes most of the slowdown.** Example: a 3 MB hero image or a dozen unused apps. Fix the biggest issue first. [b4cb9fdf5db6]
12. **Test mobile separately, on real mid-range devices.** Emulation on a dev machine hides problems. [a4ded81551ca]
13. **Platform shapes the levers.** Shopify: hosting and basic optimization are handled; apps bypass them; main levers are apps and images. WooCommerce: shared hosting, database bloat, plugin conflicts dominate. [b147e14a22ec] [b4cb9fdf5db6]

## 3. Procedures

### 3.1 Priority ladder
1. Images: compress and convert to WebP. [c35b62b83860]
2. Third-party scripts: list every app, plugin, chat widget, review tool, analytics tag. Remove what you do not actively use.
3. Hosting and CDN: leave shared hosting if traffic is meaningful; add a CDN if customers are in several regions.
4. Only then: minify, code split, Critical CSS, cache header tuning.

### 3.2 Image pipeline
1. Keep originals as JPEG or PNG.
2. Serve WebP by default (25% to 35% smaller than JPEG at equal quality; all modern browsers). AVIF compresses better but the source says support is narrower; treat as optional.
3. Let build tools or a CDN (Cloudflare, Imgix, Cloudinary) auto-convert and serve modern formats with fallbacks.
4. Size targets: product images under 100 KB; hero banners under 200 KB.
5. Product photos: JPEG quality 80% "typically" balances size and look.
6. Compress once from the original. Repeat compression degrades quality.
7. Resize to display dimensions before upload. A 4000x3000 full-quality photo can exceed 5 MB.
8. Lazy-load below the fold with native `loading="lazy"`. Shopify and WooCommerce usually do this for product grids. Do not lazy-load hero or first visible products.
9. Category pages: responsive thumbnails, not full-size photos.
10. Thousands of SKUs: use CDN image optimization; "the slight monthly cost typically pays for itself" (author's claim). Tools for manual work: Squoosh, TinyPNG, ShortPixel. [8883db1cfb1d] [verify UI]

### 3.3 Third-party script audit
1. List all third-party services (apps, widgets, tags).
2. Remove unused ones.
3. Before installing an app: read reviews for speed complaints. After: run a speed test and compare.
4. Remove apps that slow the store without proportional value.
5. Defer or async-load needed scripts that do not affect first render. Source says this improves INP by cutting JS execution during load.
6. Schedule the audit; do not wait for complaints. [c09e2fd0f0d7] [74fc1378fc6a]

### 3.4 JavaScript and CSS
1. Minify: Terser (JS), CSSNano (CSS). Webpack, Vite, Parcel minify in production mode. Shopify: apps such as Hyperspeed or TinyIMG. WooCommerce: Autoptimize or WP Rocket. Up to 80% smaller JS. [verify UI]
2. Code split by page type: product pages do not need checkout code; category pages do not need product zoom. Next.js, Nuxt, Gatsby do it automatically; traditional themes use Webpack dynamic import.
3. Critical CSS: extract above-fold styles, inline them in the HTML, load the rest async. Tools: Critical, PurgeCSS; WP Rocket and similar plugins generate it.
4. On PDPs, load reviews, related products and other secondary content after the main image and buy button render. [c067983b290a] [4b59118db903]

### 3.5 Caching
1. Browser cache: static assets (images, CSS, JS) can cache for 1 year "since filenames change when content updates". HTML: shorter. Set via HTTP headers.
2. CDN edge cache: cache static assets aggressively; shorter TTL for pages with prices or stock.
3. Server-side cache: WooCommerce plugins WP Rocket, W3 Total Cache, Redis Object Cache. Shopify manages it automatically with limited control.
4. Exclude cart, checkout, account pages.
5. Defer session creation until first add-to-cart or login (Salesforce guidance) so anonymous browsing stays cacheable.
6. Prices and stock: cache the page and update those parts with JavaScript, or use short durations with fast invalidation.
7. After any change, audit cache headers: new content shows, static assets still cached. [9490c0550ad4] [74fc1378fc6a]

### 3.6 CDN setup
1. Pick by traffic geography. 1 region: basic CDN. Global: wide edge network. Providers: Cloudflare (DDoS protection, image optimization), Fastly (edge computing), Akamai, AWS CloudFront, BunnyCDN (low price for high bandwidth). Most have free or cheap entry plans. [web check: plans and prices]
2. Start with static assets: images, CSS, JS, fonts.
3. Cache keys: include query parameters that change content (page numbers); exclude tracking parameters (they fragment the cache).
4. Set automatic invalidation on image updates and deploys (API purge or URL invalidation).
5. Monitor cache hit rate. Target 80%+ of requests served from cache. Low hit rate = misconfiguration or too much dynamic content. [46127ea01ca7]

### 3.7 Hosting tier by store size
1. New store, little traffic: shared hosting ($1 to $15 a month) is acceptable for now; plan to upgrade within the first year.
2. 100+ orders a month: VPS (managed from about $20 to $50 a month) or cloud.
3. High volume: auto-scaling cloud (AWS, Google Cloud, DigitalOcean, Shopify infrastructure, managed WooCommerce hosts like Kinsta).
4. International customers: add a CDN on top.
5. ROI check: the author says $5 shared vs $30 quality hosting "often" is a meaningful speed gain; compute with your cart abandonment rate and AOV. [a063ce857916] [needs brand data: monthly orders, AOV, cart abandonment rate]

### 3.8 Testing toolchain
1. Quick check: PageSpeed Insights (lab plus CrUX field data, mobile and desktop, prioritized recommendations). The author also offers the Ecomhint store speed test (Lighthouse-based) as a starting point; promotional.
2. Deeper: GTmetrix waterfall; free account lets you test from other locations and connection speeds; read "Top Issues" first. [verify UI]
3. Deepest: WebPageTest with chosen location, device and connection; filmstrip view (visual progress) and connection view (server response and load order). Best for a specific problem, not routine monitoring. [verify UI]
4. Test mobile on real devices.
5. Test checkout flows separately; site scores miss them.
6. Repeat tests; 1 run is a snapshot. [a4ded81551ca] [95c02555626f]

### 3.9 Monitoring and budget
1. Test at least monthly.
2. Test right after installing apps, changing themes or site-wide updates.
3. Run a speed audit before major sales events.
4. Automate: free options are PSI API on a schedule, GTmetrix monitoring (account), Lighthouse CI in deploys. Paid: DebugBear, SpeedCurve, Calibre.
5. Write a performance budget: max page weight, min speed score, max third-party scripts. Review any change that breaks it before approval. [9ffe9f981c57]

### 3.10 Fonts and database
1. Host fonts locally or use `font-display: swap` so fallback text shows while fonts load.
2. Subset fonts to the characters you use.
3. WooCommerce and other database-driven platforms: clean old revisions, expired transients, orphaned metadata on a schedule (WP-Optimize). [74fc1378fc6a]

## 4. Rules, thresholds and numbers

| rule | number or threshold | condition | source's basis | card id |
|---|---|---|---|---|
| Page load target | under 3 s; 2 s or less for competitive stores | all pages | "industry research" | [b147e14a22ec] |
| LCP | under 2.5 s good; over 4 s poor | CWV | Google | [2969a152a99d] |
| INP | under 200 ms | CWV; replaced FID | Google | [2969a152a99d] |
| CLS | under 0.1 | CWV | Google | [2969a152a99d] |
| PSI score bands | 90+ good; 50 to 89 needs improvement; under 50 serious | lab score | source | [95c02555626f] |
| CrUX window | 28 days | PSI field data | Google | [95c02555626f] |
| CWV pass rate | about 50% of mobile sites | HTTP Archive 2025 | cited | [04439b080448] |
| WebP vs JPEG | 25% to 35% smaller | equal quality | cited | [8883db1cfb1d] |
| WebP conversion page weight | 40% to 60% less | "often" | author claim | [c35b62b83860] |
| Product image size | under 100 KB | product images | author target | [8883db1cfb1d] |
| Hero banner size | under 200 KB | hero | author target | [8883db1cfb1d] |
| JPEG quality | 80% | product photos | author | [8883db1cfb1d] |
| Uncompressed hero | can exceed 2 MB | full-res upload | example | [b4cb9fdf5db6] |
| Camera photo | 4000x3000 can exceed 5 MB | full quality | example | [74fc1378fc6a] |
| JS minification | up to 80% smaller | maximum, not typical | "research indicates" | [c067983b290a] |
| Static asset browser cache | up to 1 year | filenames change on update | author | [9490c0550ad4] |
| CDN latency cut | 200 to 800 ms | geographically distant visitors | Cloudflare | [9490c0550ad4] |
| CDN cache hit rate | 80%+ of requests | well-configured CDN | author target | [46127ea01ca7] |
| Hosting upgrade | 100+ orders a month > VPS or cloud | heuristic | author | [a063ce857916] |
| Shared hosting cost | $1 to $15 a month | 2026 | author | [a063ce857916] |
| Managed VPS cost | from $20 to $50 a month | 2026 | author | [a063ce857916] |
| Third-party services vs score | r = -0.66; 0 to 5 = median 74, 21 to 30 = median 44 (mobile) | Shopify, 1,533 stores | Ecomhint benchmark | [c09e2fd0f0d7] |
| Industry services | beauty median 31 (worst), auto parts median 15 (best) | 9 Shopify industries | Ecomhint | [c09e2fd0f0d7] |
| 0.1 s faster | up to +8.4% retail conversions | upper bound | Google/NitroPack | [41ce06260ce9] |
| 1 s delay | about -7% conversions | | Cloudflare | [41ce06260ce9] |
| Per 2 s | about -4% conversions | | Cloudflare | [41ce06260ce9] |
| 1 s vs 10 s | about 5x conversions | | Cloudflare (body) / Queue-it (summary) | [41ce06260ce9] |
| Mobile abandon | 53% after 3 s | mobile | Google/NitroPack | [41ce06260ce9] |
| Abandon | 63% after 4 s | ecommerce | Queue-it | [41ce06260ce9] |
| Page priority | 0.5 s on 10,000 visits beats 2 s on 100 | traffic weighting | author | [4b59118db903] |
| Test cadence | at least monthly; after app/theme changes; before big sales | | author | [9ffe9f981c57] |

## 5. Diagnostics and checks

| check | how | good | bad | next |
|---|---|---|---|---|
| Biggest cause | PSI first; likely order: images, apps, code bloat, hosting, database | 1 dominant issue found | scattered small fixes | fix biggest first [b4cb9fdf5db6] |
| LCP element | PSI; identify element per page type | under 2.5 s | over 4 s; hero lazy-loaded | image and server fixes |
| INP | PSI field data; click Add to Cart and filters | under 200 ms | half-second lag on clicks | cut, defer, async scripts |
| CLS | PSI | under 0.1 | images without dimensions, cookie banner push, font reflow | reserve space, set dimensions |
| Image weights | inspect file sizes | product < 100 KB, hero < 200 KB | 2 MB+ hero | 3.2 |
| Third-party count | list services on page | lean stack (0 to 5 had median 74) | 21 to 30 (median 44) | 3.3 |
| Cache safety | load cart/checkout/account; check headers | not cached | cached user data | exclude |
| Stale prices | compare page price with admin after a change | updates fast | old price shown | shorter TTL or JS update |
| CDN hit rate | CDN dashboard | 80%+ | low | review cache keys and dynamic content |
| Cache key fragmentation | CDN logs with tracking params | tracking params ignored | each UTM makes new cache entry | exclude tracking params |
| Mobile vs desktop | PSI mobile; real mid-range phone | mobile close to desktop | big gap | prioritize mobile |
| Checkout | separate test of checkout flow | cart calculations feel instant | slow payment, address, fraud scripts | review those scripts |
| Trend | scheduled monitoring | stable | creeping decline | enforce budget |

## 6. Tools, settings and named features

- Testing: PageSpeed Insights, Lighthouse (DevTools, CLI), Lighthouse CI, PSI API, GTmetrix (waterfall, Top Issues, locations with account), WebPageTest (filmstrip, connection view), Ecomhint store speed test (author's product). [verify UI]
- Monitoring (paid): DebugBear, SpeedCurve, Calibre.
- Images: Squoosh, TinyPNG, ShortPixel, Imagify; CDN image services Cloudflare, Imgix, Cloudinary.
- Code: Terser, CSSNano, Webpack, Vite, Parcel, Next.js, Nuxt, Gatsby, Critical, PurgeCSS.
- Shopify apps: Hyperspeed, TinyIMG. [web check: still listed]
- WordPress/WooCommerce: WP Rocket, W3 Total Cache, Autoptimize, Redis Object Cache, WP-Optimize, ShortPixel, Imagify.
- CDN: Cloudflare, Fastly, Akamai, AWS CloudFront, BunnyCDN.
- Hosting: BlueHost (cited), AWS, Google Cloud, DigitalOcean, Kinsta, Shopify infrastructure.
- CSS property: `font-display: swap`. HTML: `loading="lazy"`.

## 7. Examples and case results

Examples, not promises.
- Vodafone A/B test: LCP 31% better > lead-to-visit rate +15%, sales +8%. Lead-to-visit is not a purchase metric.
- Rakuten 24: after CWV work, conversion rate +33%, revenue per visitor +53% (web.dev).
- Ecomhint 1,533-store Shopify benchmark: see principle 5 and 6.

## 8. Mistakes the source warns about

- Uploading camera or design-tool originals. [74fc1378fc6a]
- Installing apps without a speed check before and after. [74fc1378fc6a]
- Judging mobile by desktop tests. [74fc1378fc6a]
- Caching too hard (stale prices, stock) or too little (no gain). [74fc1378fc6a]
- Ignoring fonts: not local, no `font-display: swap`, not subset. [74fc1378fc6a]
- Ignoring database bloat on WooCommerce. [74fc1378fc6a]
- No performance budget. [9ffe9f981c57]
- Testing only once. [74fc1378fc6a]
- Lazy-loading above-fold images. [8883db1cfb1d]
- Compressing the same image several times. [8883db1cfb1d]
- Caching cart, checkout, account pages. [9490c0550ad4]
- Tracking parameters in CDN cache keys. [46127ea01ca7]
- Doing JS bundle work before images, scripts and hosting. [c35b62b83860]

## 9. Caveats, conflicts and what is missing

- Vendor bias: the author sells audits; the Ecomhint benchmark method (how scores were measured, date, sample) is not given here.
- Internal number conflict: the "1 s converts about 5x a 10 s site" is credited to Cloudflare in the body and Queue-it in the summary. The WebP figures differ: 25% to 35% smaller per image vs 40% to 60% less page weight "often"; these measure different things.
- Conflict with source 02: this source says AVIF has "narrower browser support" and makes WebP the default; source 02 says AVIF has "really good browser support" and prefers it. [web check: current AVIF support]
- Conflict with source 02 on order: this source puts hosting and CDN third in the ladder but before code work; source 02 puts caching, compression and CDN last as a "band-aid".
- Browser cache "1 year" assumes filenames or versions change on update (card caveat: needs cache-busting file names).
- 100+ orders a month for VPS is a heuristic, not a break-even.
- PSI score bands are coarse; CWV metrics are more stable (card caveat).
- CrUX field data lags 28 days, so new fixes show slowly. [95c02555626f]
- "Defer or async improves INP" is stated without data.
- Thin on how for: CDN configuration screens, Critical CSS extraction steps, session deferral implementation, cache header values other than "a year".

## 10. Card index

- [c35b62b83860] Speed Fix Priority Ladder: Images, Scripts, Hosting
- [2969a152a99d] Core Web Vitals Thresholds and What Each Metric Means for Your Store
- [95c02555626f] Lighthouse vs PageSpeed Insights: Which Lab Test to Trust
- [8883db1cfb1d] Image Optimization That Actually Moves LCP
- [c09e2fd0f0d7] Cut Third-Party App and Script Bloat Without Losing Functionality
- [9490c0550ad4] Caching Layers: What to Cache, What Never to Cache
- [46127ea01ca7] CDN Setup and Configuration for Ecommerce
- [a063ce857916] Hosting Architecture: Shared vs VPS vs Cloud by Order Volume
- [a4ded81551ca] Speed Testing Toolchain: From Quick Score to Root Cause
- [9ffe9f981c57] Continuous Performance Monitoring and Budgets
- [4b59118db903] Prioritizing Speed Work by Page Type and Traffic
- [c067983b290a] JavaScript and CSS Optimization: Minify, Split, Inline Critical
- [74fc1378fc6a] Common Speed Mistakes and How to Prevent Them
- [41ce06260ce9] Quantifying the Conversion Cost of Slow Load Times
- [04439b080448] Speed as an SEO Tie-Breaker Under Mobile-First Indexing
- [b147e14a22ec] Setting Speed Targets by Page and Store Type
- [b4cb9fdf5db6] Diagnosing 'Why Is My Store Slow?' by Category
