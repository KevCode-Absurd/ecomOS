# Page Speed Guide for Ecommerce Store Operators: Diagnosis and Actions

source_id: 1kUl-y-7RoB9HQ9CkAmrhdUXHmTkCe_QS  |  folder: /08-SPD-speed  |  cards: 9  |  words: 1815  |  type: article
credibility: Written from Shopware's point of view (the article closes with a section on "automatic page speed optimization in Shopware" and names Shopware 6 features). Shopware sells an ecommerce platform, so the platform section is vendor content. Evidence: benchmark figures without named studies (7% per second, 3x, 66% of revenue on mobile, 30% to 50% smaller images, >50% of load time from scripts, >60% of data from images). No case studies.
date signals: States INP replaced FID in March 2024. Recommends PHP 8.2+ and HTTP/3. Example change log date "March 15". Likely written 2024 to 2026.

## 1. What this source is for

Use it as a short, non-technical 4-step order of work for a store operator: baseline, images, extension audit, then the server foundation. It is the source that says when to call the host (only after steps 1 to 3), what to ask them (PHP version, Redis or Varnish full-page cache, HTTP/3), and what "intelligent cache invalidation" means for prices and stock.

## 2. Principles

1. **Speed links technical performance and buying psychology.** Faster loads mean higher conversion, lower bounce and better Google rankings. A 1-second delay can cut conversion by up to 7%. Stores under 1 second convert up to 3x better than stores at 5 seconds. No study named. [f8bdb58727f9]
2. **Slow pages waste ad spend.** You pay per click; a visitor who leaves before the page loads never sees the offer. [f8bdb58727f9]
3. **Mobile first.** 66% of online revenue comes from smartphones and tablets (no study named). [f8bdb58727f9]
4. **Core Web Vitals are official ranking factors;** a slow store "will rank lower... even if its content or products are excellent". Note source 04 and 05 frame CWV as a tie-breaker; keep the conflict. [f8bdb58727f9]
5. **The core shop system is often not the problem; add-ons are.** Oversized images, scripts and plugins added later slow stores. [3d795cd17d4b]
6. **Every plugin and script must earn its place.** Ask of each: "How does this plugin currently contribute to revenue?" [753859e92e44]
7. **Remove unused plugins completely; do not just deactivate them.** [753859e92e44]
8. **Fix content before calling the host.** Contact your provider only after steps 1 to 3, "otherwise support will simply point to unoptimized content". [0709d6cdeb98]
9. **Poor TTFB means slow hosting or an overloaded database; front-end work can only do so much on a weak base.** TTFB under 800 ms is "often harder to achieve in ecommerce due to dynamic carts". [a10a7445f2a3]
10. **Full-page caching serves pre-rendered HTML** instead of querying databases, calculating prices and building layouts on every click. [3d795cd17d4b] [0709d6cdeb98]
11. **Clear only the pages that changed.** Intelligent cache invalidation detects price or stock changes and clears only affected pages, so the store stays fast without showing old prices or stock. [ee4655c50df6]
12. **Measure each change on its own.** Keep a dated change log. [6012d71fccb6]

## 3. Procedures

### 3.1 The 4-step roadmap
1. **Baseline.** Run Google PageSpeed Insights on your URL for mobile and desktop. Screenshot results or note LCP and the overall score. Start a dated change log, for example "March 15: image compression enabled". The card extends this to each key template: homepage, key category pages, best-selling PDPs, cart and checkout. [6012d71fccb6] [verify UI]
2. **Images.** Use WebP instead of JPEG (AVIF also named elsewhere in the text). Convert a few images by hand with free browser tools; at scale, use platform automation (Shopware converts automatically). Re-measure LCP on the hero and main product image. [baaf2f6aee4e]
3. **Extension audit.** In the admin panel, read the plugin list top to bottom. Ask the revenue question for each. Disable uncertain plugins in a staging environment and measure again. Marketing pixels and unused design effects often block rendering. Remove unused plugins completely. Repeat for third-party scripts (pixels, chat widgets, review platforms, social embeds). [753859e92e44]
4. **Technical foundation.** Talk to your in-house IT admin or the host's support, only after steps 1 to 3. Ask: which PHP version (want 8.2+)? Is server-side caching (Redis or Varnish) active? Is full-page caching serving pre-rendered HTML? Is HTTP/3 on? In SaaS and cloud setups many settings are already tuned, but read the documentation anyway. Re-measure TTFB and LCP after changes. [0709d6cdeb98] [d2e8efefa7f2]

### 3.2 Shopware 6 native features (vendor section)
1. WebP generation: uploaded source images are converted to WebP automatically.
2. Thumbnail sets: several sizes per product, served by device.
3. Integrated HTTP cache: stores fully rendered pages; repeat visits get ready HTML without database queries or PHP.
4. Intelligent cache invalidation: price or stock changes clear only affected pages.
5. CSS and JavaScript bundled and optimized.
6. On other platforms, look for equivalents: automatic image conversion, responsive thumbnails, selective cache purge (card). [ee4655c50df6] [verify UI]

## 4. Rules, thresholds and numbers

| rule | number or threshold | condition | source's basis | card id |
|---|---|---|---|---|
| Conversion loss | up to -7% per 1 s delay | | unnamed benchmark | [f8bdb58727f9] |
| Fast vs slow | under 1 s converts up to 3x vs 5 s | | unnamed benchmark | [f8bdb58727f9] |
| Mobile revenue share | 66% | smartphones and tablets | unnamed | [f8bdb58727f9] |
| LCP | under 2.5 s | hero on home, product image on PDP | Google | [a10a7445f2a3] |
| CLS | under 0.1 | | Google | [a10a7445f2a3] |
| INP | under 200 ms | replaced FID March 2024 | Google | [a10a7445f2a3] |
| TTFB | under 800 ms | harder with dynamic carts; diagnostic, not a CWV (card correction) | Google | [a10a7445f2a3] |
| WebP/AVIF savings | 30% to 50% smaller than JPEG/PNG | same quality | unnamed | [baaf2f6aee4e] |
| Image share of data | more than 60% of page data | "can account for" | unnamed | [3d795cd17d4b] |
| Third-party script share | more than 50% of total load time | "in many stores" | unnamed | [3d795cd17d4b] |
| PHP version | 8.2+ | self-hosted PHP platforms | source's recommendation | [0709d6cdeb98] |
| Protocol | HTTP/3 (HTTP/2 also named once) | server | source's recommendation | [0709d6cdeb98] |
| Server cache | Redis or Varnish full-page cache | | source's recommendation | [0709d6cdeb98] |
| When to call host | after steps 1 to 3 | | source's rule | [0709d6cdeb98] |

## 5. Diagnostics and checks

| check | how | good | bad | next |
|---|---|---|---|---|
| Baseline recorded | PSI mobile and desktop; change log | dated values per template | no before numbers | record before changing anything |
| LCP element | PSI | product/hero image loads under 2.5 s | image appears late; shoppers doubt the store | step 2 |
| CLS | PSI | under 0.1 | buttons move before tap; misclicks | reserve space (source gives no steps) |
| INP | PSI field data | under 200 ms | repeated clicks in checkout, users unsure input registered | cut scripts |
| TTFB | PSI | under 800 ms | slow: hosting or overloaded database | step 4 |
| Plugins with heavy queries | ask developer; staging test | results cached | complex database queries on every page load, uncached | remove or cache |
| Site-wide CSS/JS | coverage check (method not given) | code loads only where used | theme loads all features on every page | remove or split (method not given) |
| Uncertain plugin | disable in staging, re-measure | no speed change: keep if useful | clear gain: remove fully | delete, not deactivate |
| Cache freshness | change a price or stock level; reload affected page | page updates, rest stays cached | old price shown, or full purge each time | intelligent invalidation |

## 6. Tools, settings and named features

- Google PageSpeed Insights (mobile and desktop). [verify UI]
- Free browser-based image converters (none named).
- Staging environment for plugin tests.
- Redis, Varnish (server-side full-page cache).
- PHP 8.2+, HTTP/3 (also HTTP/2 mentioned in the intro to the steps).
- Shopware 6: automatic WebP, thumbnail sets, integrated HTTP cache, intelligent cache invalidation, CSS/JS bundling. [verify UI]

## 7. Examples and case results

None. The source gives only benchmark figures and a sample change log line ("March 15: image compression enabled").

## 8. Mistakes the source warns about

- Calling the host before fixing images and plugins. [0709d6cdeb98]
- Deactivating instead of deleting unused plugins. [753859e92e44]
- Plugins that run complex database queries on every page load without caching. [3d795cd17d4b]
- Themes loading features site-wide that only 1 subpage needs. [3d795cd17d4b]
- No caching: the server rebuilds every page on every click. [3d795cd17d4b]
- Making changes without a baseline and a change log. [6012d71fccb6]

## 9. Caveats, conflicts and what is missing

- Vendor content for Shopware; the platform section is promotional.
- The source lists TTFB among the Core Web Vitals. The card corrects this: the 3 CWV are LCP, INP, CLS; TTFB is diagnostic; assess the 75th percentile separately for mobile and desktop. [a10a7445f2a3] [web check: web.dev/articles/vitals]
- HTTP/2 is named in 1 sentence and HTTP/3 in the rest.
- Conflict with source 04: under 1 s converts "up to 3x" vs 5 s here; source 03 says 2.5x (Portent); source 04 and 06 say 5x vs 10 s.
- Conflict on sequence: this source puts server work last (step 4) and says the host will blame unoptimized content; source 04 puts hosting and CDN third but before code work; source 02 puts caching last as a band-aid. Broadly agree: content first.
- Conflict on CWV weight: "official ranking factors" that make a slow store rank lower even with excellent content, vs "tie-breaker" in sources 04 and 05.
- Card caveats: do not remove review, chat or tracking scripts only for speed without checking their revenue or operations role; test checkout and cart after any cache or protocol change; staging may not match production. [3d795cd17d4b] [753859e92e44] [0709d6cdeb98]
- Thin on how: no steps for fixing CLS or INP, removing site-wide CSS/JS, or configuring Redis or Varnish.

## 10. Card index

- [f8bdb58727f9] Ecommerce page speed: conversion, ranking and ad-spend impact
- [a10a7445f2a3] Track three Core Web Vitals plus diagnostic TTFB on store templates
- [3d795cd17d4b] Where ecommerce stores lose speed: five common killers
- [6012d71fccb6] Baseline first: measuring speed before you change anything
- [baaf2f6aee4e] Optimise product images with WebP/AVIF and responsive sizes
- [753859e92e44] Plugin and script audit: earn each extension its place
- [0709d6cdeb98] Server-side foundation: caching, PHP and HTTP/3
- [ee4655c50df6] Platform-native caching and intelligent cache invalidation
- [d2e8efefa7f2] Prioritised speed roadmap for a store
