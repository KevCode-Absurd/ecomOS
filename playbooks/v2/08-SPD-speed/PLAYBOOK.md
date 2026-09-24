# Speed (08-SPD) playbook

version: 2.0-draft  |  date: 24 Sep 2026  |  sources: 9  |  cards: 226  |  built from: sources/*.md

## 0. How to use this playbook

**Who runs it.** The site speed agent. It audits a storefront's speed end to end, decides what to fix in which order, does the fixes it can do safely (or writes the brief for a developer or host), and proves each fix with before and after data. It works on Shopify first (6 of 9 sources), on WordPress and WooCommerce second (sources 02, 04, 05), and on any other platform for the architecture rules (sources 07, 08, 09).

**Which sections to load for which task.**

| Task | Load |
|---|---|
| First audit of a store | 0, 1, 2, 3 (groups A and B), 4 (P1 to P6), 5 (all), 6 |
| Business case for speed work | 3 (A9), 4 (P6), 6, 7 (conflicts 7.2, 7.3, 7.9) |
| Image audit and fixes | 3 (group C), 4 (P14 to P17), 5 (5.2), 6 |
| Apps, scripts and third parties (Shopify) | 3 (group D), 4 (P7 to P12), 5 (5.3), 7 (7.7, 7.12) |
| Plugins and assets (WordPress, WooCommerce) | 3 (group D, E), 4 (P7, P13), 5 (5.3, 5.4) |
| Theme code, CSS and JS | 3 (group E), 4 (P22, P23), 5 (5.4) |
| Fonts | 3 (group F), 4 (P21), 5 (5.5) |
| Layout shift (CLS) | 3 (group G), 4 (P19, P20), 5 (5.6) |
| Largest Contentful Paint (LCP) | 3 (group H), 4 (P18), 5 (5.7) |
| Interaction delay (INP, TBT) | 3 (group I), 4 (P13, P10), 5 (5.8) |
| Caching, CDN and hosting | 3 (groups J, K), 4 (P26 to P28), 5 (5.9, 5.10), 7 (7.4, 7.10) |
| Video, embeds, redirects, checkout | 3 (groups L, M, N), 4 (P24, P25), 5 (5.11, 5.12) |
| Prove a fix and report | 3 (group P), 4 (P30), 9 |
| Peak sale readiness | 3 (K94), 4 (P31), 5 (5.13) |
| Deciding to call the host or a developer | 3 (group O), 4 (P28), 9 |

**What the agent must fetch before acting.**

- From the brand record: platform and plan, theme name, version, who built it and when it was last customized; installed apps, plugins, app embeds and external scripts with the revenue role of each; which widgets must show at first paint; pixel and consent setup; mobile share of sessions and revenue; the pages ads land on; AOV, daily sessions, conversion rate, monthly orders, cart abandonment rate; whether shoppers use dynamic checkout (wallet) buttons; the store's own load time and speed history.
- From the data layer: sessions and revenue by template (home, collection, product, cart, checkout); scroll and click maps if they exist; Search Console Core Web Vitals report if connected.
- From the web: the current Core Web Vitals list and thresholds at web.dev/articles/vitals (sources are dated; 5 of 9 still name FID); current Shopify admin speed reporting; current Shopify image delivery behaviour (WebP and AVIF); current AVIF browser support; tool prices and plan limits (GTmetrix, WebPageTest, CDNs, hosting); whether named apps and plugins still exist. Section 10 lists every item.

**Hard rules for this agent.** Read-only until a baseline is recorded. Work on a duplicate theme or staging. Change 1 thing at a time. Never remove a script whose function is unknown. Never touch pixels or consent banners without the tests in P10 step 9 and P30. Never clear caches or purge a CDN on a live store without the owner's go-ahead. Do arithmetic in code, not in the model.

## 1. Scope and outcomes

**What this domain covers.** How fast a storefront loads and responds for real shoppers, and the score Google gives it. Concretely: images (size, format, delivery, lazy loading), scripts and apps (which to keep, how they load), theme code (Liquid, CSS, JS, critical CSS, loops, Quick View, sliders), fonts, third parties (pixels, chat, reviews, embeds), caching and CDN, hosting and server (TTFB, PHP, HTTP/3, database), layout shift, LCP, interaction delay, measurement method (lab vs field, tools, test protocol), order of work, when to call the host or a developer, and how to prove a fix.

**What it does not cover, and where it lives.**

- Keyword research, titles, descriptions, sitemaps, rich snippets, alt text as SEO: 15-SEO-search. Source 01 carries a long SEO video; only its speed parts are merged here.
- Product page layout, promo copy, gallery order, add-to-cart placement: 09-CRO-testing and 07-LPG-landing-pages.
- Pixel, Web Pixels API and CAPI setup and event testing: 06-MEA-measurement. This playbook only says when a speed change must be checked against tracking.
- Theme selection, media library setup, domains, headless and Commerce Components: 05-SET-store-setup. Theme choice appears here only where it changes speed.
- Load balancers, infrastructure sizing, virtual waiting room setup: 05-SET-store-setup. This playbook only flags peak-event risk.
- Google Ads landing page policy: 12-GAD.

**Business measures it moves.** Conversion rate (sources cite 5.6% to 8.4% per second or per 0.1 s; direction, not forecast), bounce rate (about 12% per second, source 06), pages per session (8.9 at 2 s vs 3.3 at 8 s, source 06), revenue per session, wasted paid clicks (a visitor who leaves before load never sees the offer, source 08), cart abandonment on mobile checkout (source 03), organic visibility (Core Web Vitals as tie-breaker per sources 04 and 05, as ranking factor per source 08; see 7.8), and return intent (source 06). All figures are third-party or vendor benchmarks. Recompute with brand data (P6).

## 2. Inputs the agent needs

| Input | From where | Required or optional | Why |
|---|---|---|---|
| Platform, plan, theme name and version, who built it, last customization date | Brand record | Required | Sets the levers (R12), tells whether responsive widths and lazy loading are likely missing (R28, R34), whether a rebuild beats optimizing (R13) |
| Installed apps, plugins, app embeds, external scripts, and the revenue role of each | Brand record, user | Required | App triage (R44) cannot run without it; the agent must not guess revenue roles |
| Widgets that must show at first paint (for example review stars above the fold) | Brand record, user | Required | Exceptions to delaying scripts (R48) |
| Pixel, tag manager and consent setup | Brand record, 06-MEA | Required | Delaying scripts can break events; consent banners have legal limits (R48, R76) |
| Mobile share of sessions and revenue | Data layer | Required | Decides mobile-first weighting (R10) and separate mobile targets |
| Sessions and revenue by template (home, collection, product, cart, checkout) | Data layer | Required | Page priority (R3) |
| Pages ads land on, and paid vs organic share | Brand record, data layer | Required | Ad landing page gets fixed first (R3); score weighting (R5) |
| AOV, daily sessions, conversion rate, margin, monthly orders, cart abandonment | Data layer | Required for business case; optional for a fix | Revenue model (P6), hosting tier (R91) |
| Baseline PSI averages per template, mobile and desktop, with dates | Agent produces in P1 | Required before any change | Proof of fix (R98) |
| Visitor connection and device mix | Data layer (analytics device and network reports), or user | Optional | Picks the throttling profile (P2) and the test device (R10) |
| Scroll and click heatmaps | Data layer (Hotjar or similar) | Optional | Quick View usage (R61), buy button reach (neighbour 09-CRO) |
| Search Console Core Web Vitals report | Data layer | Optional | Field confirmation of CLS and LCP fixes (R98) |
| Dynamic checkout button usage | Brand record, data layer | Optional | R56 |
| Current CWV thresholds, Shopify image delivery, AVIF support, tool prices | Web | Required once per audit | Sources are dated; see sections 10 and 11 |
| Staging or duplicate theme access, code editor access, host support contact | User | Required | Safe work and rollback (R14) |
| Consent rules that apply to the store's markets | User, legal | Required before touching a cookie banner | R76 |

## 3. Decision rules

Numbering runs across all groups. Each rule gives the rule, its condition, the mini playbooks that support it (by number), conflicts (pointing to section 7) and card ids. "Sources: 01" alone means 1 practitioner's view, not a law.

### Group A. Strategy, scope and order of work

**R1. Record a baseline before changing anything.** Condition: every audit, every template you will touch. Run PSI on mobile and desktop for home, a collection, a top product, cart and checkout; note the score, LCP, CLS, INP and TTFB; start a dated change log ("15 March: image compression enabled"). Without a baseline no fix can be proven. Sources: 08, 01, 05. Cards: [6012d71fccb6] [c33439a2c9b9] [d2e8efefa7f2].

**R2. Find the 1 biggest cause first; it is often most of the slowdown.** Condition: when the report shows many items. A 3 MB hero or a dozen unused apps usually explains more than the rest combined. On Shopify, source 01 ranks layout stability (CLS, LCP) and apps as the 2 root causes, CLS first. Use PSI's hover hint to see which metric would move the score most (R23). Sources: 04, 01, 05. Cards: [b4cb9fdf5db6] [7678b95c31ff] [693051f7daf7].

**R3. Prioritize pages by traffic and money, not by which page is easiest.** Condition: always. Product and category pages carry 72% of shopper page views (source 06). A 0.5 s gain on a page with 10,000 monthly visits beats a 2 s gain on a page with 100 (source 04). For paid traffic, fix the page ads land on first, usually the product page, which often has a poor LCP while the home page passes (source 01). Order: ad landing pages, top product pages, main collections, home, then cart and checkout. Sources: 04, 06, 01. Cards: [4b59118db903] [dd24469d1841] [1b9747314efd] [74187c8d7e19]. [needs brand data: sessions and revenue by template; ad landing pages]

**R4. Fix content before infrastructure: images, then scripts and apps, then hosting, CDN and caching; code work (minify, bundle, critical CSS) after those 3.** Condition: any platform. All 9 sources agree that images and third-party scripts come first. They disagree on where hosting and caching sit: source 04 puts hosting and CDN third and before code work; sources 02 and 08 put caching and server work last and call caching "a band-aid" if fundamentals are skipped; source 08 says a host contacted before content is fixed "will simply point to unoptimized content". Merged rule keeps the strictest condition: do not call the host or turn on caching layers until images and scripts are done and re-measured. See 7.4 for the Shopify-specific order (LCP and CLS vs apps first). Sources: 04, 02, 08, 01, 09. Cards: [c35b62b83860] [1b50d0611dc3] [0709d6cdeb98] [cce38d9369f2] [3d5cfd45530c].

**R5. How much the Google score matters depends on the traffic mix; the shopper experience case applies regardless.** Condition: deciding how far to push. If the store depends on organic traffic, the PSI score and Core Web Vitals matter and flagged items should be fixed. If nearly all traffic is paid, a low score matters less for ranking, but slow pages still lose ad clicks. Visits without sales make speed a candidate cause to test, not a proven one. Sources: 01, 04, 08. Conflict on ranking weight: see 7.8. Cards: [37d2f02ad647] [04439b080448] [f8bdb58727f9]. [needs brand data: paid vs organic share]

**R6. Do not chase 100, and do not game the score.** Condition: always. A perfect score on a marketing site is not a fair target for an image-heavy catalog; major sites average about 90 (source 07). Speed apps, caching scripts and "specialists" that raise the lab score while real shoppers still wait are not fixes (source 01). A plugin used only to inflate PSI is out of scope (source 02). Sources: 05, 02, 01, 07. Cards: [693051f7daf7] [1b50d0611dc3] [5f44ccb5ead1] [b906791efd1b].

**R7. Every app, plugin, embed and script must earn its place in revenue or shopper experience; remove the rest completely.** Condition: every installed item, including sales channel apps and scripts pasted by hand. Ask "how does this make money now?" and write the answer. No answer, or purely visual, or duplicate of a theme feature: remove. Deactivating is not removing (source 08). More than 20 apps is a warning sign (source 03). In a 1,533-store Shopify dataset the count of third-party services was the strongest predictor of score (r = -0.66): 0 to 5 services had a median mobile score of 74, 21 to 30 had 44 (source 04). Sources: 01, 03, 04, 08, 09, 06. Cards: [8dbbb42b9c2e] [474204ae609c] [efd7ec0cb6ce] [c09e2fd0f0d7] [753859e92e44] [dc6cd41ae52d] [a62896aba3d8]. [needs brand data: app list with revenue role of each]

**R8. Stores slow down over time; re-audit on a schedule and hold a performance budget.** Condition: ongoing. Source 01's illustration: a fresh store scores 60 to 80, drops to 40 with apps and to 20 or lower with customization. Test at least monthly, right after any app install, theme change or site-wide update, and before major sales (source 04). Write a budget: max page weight, minimum score, max third-party scripts. Any change that breaks it gets reviewed before approval. Most site changes add features that slow pages (source 06). Sources: 04, 01, 06. Cards: [9ffe9f981c57] [474204ae609c] [d56347d58c66] [689b4ce4442e].

**R9. Speed is revenue work; model it with the brand's own numbers and label the lift as an assumption.** Condition: when making the case or ranking work against other projects. Use the benchmarks in section 6 as direction only. Method: daily sessions x conversion rate x AOV today, then again with an assumed higher conversion rate, difference x 365. Never quote a source's example ($9,000 a day, $1.8 million a year) as a forecast. Sources: 03, 04, 06, 08, 09. Conflicts on the figures: 7.2, 7.3, 7.9. Cards: [b36e60f619f7] [41ce06260ce9] [77da7bd48ab8] [fa57997432c4] [f8bdb58727f9] [af5fd5b1745b]. [needs brand data: AOV, daily sessions, conversion rate, margin, current load time]

**R10. Mobile first, measured separately, on real mid-range devices where possible.** Condition: always; mandatory when mobile share is high or traffic comes from ads. Mobile pages load 87.8% longer than desktop on average and 59% of traffic is mobile (source 06); Google indexes mobile first (source 04); emulation on a developer machine hides problems (source 04). Still check the desktop tab: CLS can be 0 on mobile and large on desktop (source 01). Sources: 01, 04, 05, 06, 09, 08. Cards: [74187c8d7e19] [a4ded81551ca] [085b91000740] [2bb637e027c0] [b35da7f37105] [f00068c50316]. [needs brand data: mobile share of sessions and revenue]

**R11. Balance speed with the buying journey; never strip UI that helps shoppers buy just to win a score.** Condition: any removal decision. Reviews, chat, size charts and tracking have a revenue or operations role; check it before removing for speed. Tools guide, they do not decide. Sources: 03, 08 (card caveat), 01. Cards: [9bd3f7aed489] [b36e60f619f7] [3d795cd17d4b] [753859e92e44].

**R12. The platform sets the levers.** Condition: choosing where to spend effort. Shopify: hosting, CDN and basic caching are handled and largely locked; apps and images are the main levers; caching scripts add nothing. WooCommerce and other self-hosted PHP stores: shared hosting, database bloat and plugin conflicts dominate, and the server foundation (PHP version, Redis or Varnish, HTTP/3) is yours to fix. Shopware and similar platforms: check what the platform does natively (WebP, thumbnails, HTTP cache, selective invalidation) before adding tools. Sources: 04, 01, 08, 03. Cards: [b147e14a22ec] [b4cb9fdf5db6] [cdc61c33e699] [ee4655c50df6] [54e3673579e3].

**R13. A simpler theme beats a feature-rich one unless the features pay; theme architecture beats quick hacks.** Condition: new store, redesign, or an old custom theme on an established store. Premium themes ship libraries and effects you will not use. Optimizing an old theme can cost more than rebuilding on Dawn or Horizon; plan the rebuild with a redesign, not as a rush job. Sources: 01, 03. Cards: [637495534f7f] [02c570556e30] [a459458a1b47] [21280154cb29].

**R14. Work on a duplicate theme or staging, keep a backup, and make changes you can revert one by one.** Condition: every code, app or setting change. Shopify: duplicate the live theme and test on its preview link (preview runs a bit slower, so compare preview to preview). WordPress: staging, and 1 plugin setting at a time. Staging may not match production; confirm on live after. Sources: 01, 08, 05. Cards: [c33439a2c9b9] [58c5589c135f] [0709d6cdeb98] [8f0d567d9844].

### Group B. Measurement and testing method

**R15. Average 3 runs per page per device, wait 1 to 2 minutes after a change before retesting, and compare averages, not single readings.** Condition: every before and after comparison. Same page scored 48, 51 and 54 in a row (source 01). Test servers can serve a cached older version right after a change. Large swings usually mean many apps loading. Sources: 01, 02, 04. Cards: [079f8ea11444] [c33439a2c9b9] [9b3008487ad5] [21b1708d102a] [a4ded81551ca].

**R16. Test every template type, not only the home page; "Core Web Vitals passed" on home is not a pass.** Condition: every audit. Minimum: home, a collection, a product page (the 3 pages Shopify's admin score used). Add cart and checkout (source 08's card and source 04). Each template loads different apps; a store passed vitals on home while scoring 18 on home, 38 on collection and lower on product (source 01). Fix all templates of a page type, not only the one Shopify links to. Sources: 01, 08, 04, 03. Cards: [5e79bed9130e] [9b3008487ad5] [6012d71fccb6] [a4ded81551ca].

**R17. Read lab and field data as 2 different things; optimize against lab, confirm with field after about 28 days.** Condition: reading any PSI report. Field = Chrome UX Report, real Chrome users, 28-day window. Lab = Lighthouse on a simulated mid-tier phone and mobile network. URL toggle = this page; Origin = all pages averaged; a greyed URL toggle means too little traffic, so read Origin as a site-wide signal only. Field CLS in one case went 0.73, 0.66, 0.13, 0.1, 0 over about 28 days after the fix. Sources: 05, 04, 01. Cards: [085b91000740] [7d6d1e80db3c] [95c02555626f] [0d2d3621b19d] [80a761efcb18].

**R18. The Core Web Vitals are LCP, INP and CLS. FCP, TTFB, TBT and Speed Index are diagnostics. FID is retired.** Condition: any report, target or client deliverable. 5 of 9 sources still name FID or TTI; source 08 lists TTFB as a vital; source 03 describes vitals as "fully loaded, time to first byte, first meaningful paint". None of that is current. Use the thresholds in section 6 and verify them live. Sources: 05, 04, 08 (card correction), 06 (card), 07 (card), 09 (card). Cards: [dfde1d811af8] [2969a152a99d] [a10a7445f2a3] [4c4de77e3eae] [717cf5ec82fd] [0e11008fda40]. [web check: web.dev/articles/vitals for the current list and thresholds]

**R19. Run a slow-connection visual test alongside the scores.** Condition: every audit and every LCP or CLS investigation. DevTools Network, Disable cache, throttle to Slow 4G or 3G (pick the slowest common visitor connection), reload, and watch: time to first content, jumps, images revealing in chunks, the main image hidden behind a script. Source 02 ranks this above tool scores; source 05 says optimize against lab data; source 01 uses 3G and a 20 kbps custom profile to catch shifts. Merged: use both, and treat a page that looks bad on slow 4G as failing even with a good score. See 7.5. Sources: 02, 01, 05. Cards: [29d73beaf348] [d16d1fcdd349] [a5d2c3aee970] [74187c8d7e19] [085b91000740]. [needs brand data: visitor connection mix]

**R20. Make sure the test saw your latest version.** Condition: after every change. Put a small visible marker above the fold, rerun PSI, check the screenshot; marker missing means the test used a cached page, so clear cache and rerun; remove the marker after. Sources: 05, 01. Cards: [f1a837edbfbe] [079f8ea11444].

**R21. Cross-check with a second tool, and never compare scores across tools.** Condition: when Google's list runs out, or when 1 tool's result looks odd. GTmetrix (waterfall, Top Issues, other locations with a free account), WebPageTest (filmstrip and connection view, best for 1 specific problem), Pingdom (waterfall). Each tool picks its own "loaded" marker. Fix findings that 2 tools share first. Sources: 09, 03, 04, 01, 02. Cards: [b35da7f37105] [9bd3f7aed489] [a4ded81551ca] [9b3008487ad5] [701c087d0917]. [verify UI: tool plans and features]

**R22. Audit every page of a large catalog, not a sample; outlier slow pages hide.** Condition: hundreds of URLs or more. Run `npx unlighthouse --site <url>` against staging or with throttling (it can load a production server hard), find outliers, then confirm key pages with field data. Sources: 07. Cards: [08cf33a0563a]. [verify UI: Unlighthouse flags]

**R23. Pick the highest-impact fix from the report, not the first item in the list.** Condition: reading PSI lab results. Hover the score circle to see which metric would most improve the score; open that metric's opportunity group first; read estimated savings against effort; retest after each change. Sources: 05, 09. Cards: [693051f7daf7] [b35da7f37105].

**R24. Fix the Lighthouse list first, then PSI's list.** Condition: Shopify stores per source 01's practice. Lighthouse in DevTools shows fewer issues than PSI; clearing them first makes PSI's remaining list actionable. Expect new items to surface as old ones clear. Sources: 01. Cards: [ba43a0aaa747] [9b3008487ad5].

**R25. Test the checkout flow separately; site scores miss it.** Condition: every audit. Cart calculations should feel instant; slow payment, address and fraud scripts show only here. Sources: 04, 03. Cards: [a4ded81551ca] [0bc2087de2a1].

**R26. Change 1 setting or script at a time and browse the live site (incognito) before the next.** Condition: any JS minify, combine, defer or delay setting; any script removal. If something breaks you must know which change did it. Sources: 05, 01. Cards: [8f0d567d9844] [1dffb0dd47d1] [58c5589c135f].

**R27. Field data lags. Do not judge a fix by Search Console or the PSI history graph for at least 28 days.** Condition: after any fix. Search Console lagged "a couple of days" in one case and about 28 days in another (source 01); CrUX is a 28-day window (sources 04, 05). Shopify's admin score refreshed every 12 to 24 hours and needed traffic (source 01, older UI). Sources: 01, 04, 05. Cards: [ba43a0aaa747] [80a761efcb18] [95c02555626f] [9b3008487ad5]. [web check: whether Shopify admin still shows a composite speed score]

### Group C. Images

**R28. Check images first, and expect them to be the biggest weight.** Condition: always, and with priority when the theme is old, custom or agency-built, the catalog is large, mobile share is high, or the store is simple with few apps and still slow. Images are 50% to 75% of page weight (source 03), can be over 60% of data (source 08); a 4,000 x 3,000 camera photo can exceed 5 MB (source 04). Platform help (Shopify CDN, width variants, automatic WebP, light compression) is not enough: a 9.8 MB upload was delivered at 6.1 MB (source 01). Sources: 01, 03, 04, 08, 09. Cards: [21698bb77d52] [d84575512652] [1c99225810ac] [3d795cd17d4b] [74fc1378fc6a] [3d5cfd45530c].

**R29. Resize before upload. Long edge about 2,000 px for product and section images; 3,000 px is the ceiling and only for a full-bleed hero.** Condition: every upload. 2,000 px is enough for zoom and retina (source 01). A 1,920 x 1,920 JPEG at 46 KB looked fine as a zoomable product image. Never upload DSLR or design-tool originals (sources 01, 04). Sources: 01, 04. Cards: [cfa3fe76f953] [08bb3d69ec5b] [74fc1378fc6a].

**R30. Serve each image near its display size.** Condition: every rendered image. Three sources give 3 rules: box width plus 100 to 300 px (source 01, section images); 2x rendered size for retina (source 02, content images; cover backgrounds keep size and only change format); "resize to display dimensions" (source 04). Merged: export at 2x the rendered width, capped at 2,000 px, never below the box width (exact box size can look blurry), and never the master file. Flag any image whose intrinsic width is more than about 2x the box (example: 5,000 px in a 700 px box, 6 MB). See 7.13. Sources: 01, 02, 04, 09. Cards: [7558889b0856] [c9fcbc1b5513] [036e673a5a05] [b783c30c2217] [8883db1cfb1d] [3d5cfd45530c].

**R31. File size ceilings: target under 100 KB per product image and under 200 KB per hero; the LCP image under 250 KB; never above 500 KB for any image.** Condition: every image; the sources disagree and this merged rule keeps the strictest as target and the most common as the hard stop. Source 04: product under 100 KB, hero under 200 KB. Source 05: LCP image under 250 KB. Source 01, across videos: 500 KB max; 500 to 600 KB, prefer 100 to 200 KB; under 1 MB for section images; "full HD JPEG under 1 MB" for mobile-majority stores. Anything over 500 KB in Content > Files gets reduced. See 7.1. Sources: 04, 05, 01. Cards: [8883db1cfb1d] [eb9525bda54a] [21698bb77d52] [cfa3fe76f953] [0c4e0163aff8] [3a99be49f292] [cce38d9369f2].

**R32. Format by role: JPEG for photos, PNG only for transparency, never GIF (use MP4), and let the platform or CDN serve WebP or AVIF with fallbacks.** Condition: every image. WebP is 25% to 35% smaller than JPEG at equal quality (source 04); WebP or AVIF 30% to 50% smaller (source 08); AVIF compresses better still and source 02 prefers it at 50% quality, while source 04 calls its support narrower and makes WebP the default. Source 01 says do not hand-upload WebP to Shopify because Shopify converts automatically and non-supporting browsers could show nothing. A photo re-exported as PNG went from 2.7 MB to 8 MB (source 01). See 7.6. Sources: 01, 02, 04, 07, 08. Cards: [02dbd594ff18] [3dd6497a4d63] [cf9d029b70aa] [5148a60eef22] [f50e2bf2a5c4] [8883db1cfb1d] [baaf2f6aee4e] [cc2d433b9ede]. [web check: current AVIF support; whether Shopify still auto-serves WebP and AVIF and whether uploaded WebP is still a problem]

**R33. Compress once, from the original, with a visual preview, at JPEG quality about 70 to 80 (AVIF about 50).** Condition: every upload and every heavy image found later. Source 04: JPEG 80% "typically" balances size and look; repeat compression degrades quality. Source 01: Squoosh from default 75 down until artifacts show (40 gave 172 KB from 2.7 MB; 20 to 30 still acceptable to his eye); Photopea export at about 70%; a second pass on a compressed file saved only 8%. Source 02: AVIF at 50% was imperceptible in the presenter's tests. Keep originals. Sources: 04, 01, 02. Cards: [8883db1cfb1d] [cfa3fe76f953] [621e302f651f] [f50e2bf2a5c4].

**R34. The theme must serve responsive widths (srcset or width variants); a single `src` with the master URL fails.** Condition: every image-rendering section, especially in old, custom or agency themes, where sections added later often skip the pattern. Good pattern: several widths (example 1,600 default, 800 under 800 px, 1,200 under 1,200 px). Category grids use thumbnails, never full-size photos. Sources: 01, 04, 08, 09, 07. Cards: [c5fb935a9b7d] [d84575512652] [8883db1cfb1d] [baaf2f6aee4e] [3d5cfd45530c] [3932af95de46].

**R35. Lazy-load every image below the fold; never lazy-load anything in view.** Condition: hero, first slide, logo, main product image, first card of a grid and anything visible without scrolling stay eager. Lazy loading them "actually hurts LCP" (source 04) and source 01 says Google penalizes it. Slides 2 and on, footer logos, reviews, related products and social feeds are lazy. Browsers otherwise download every image at once (source 03). Sources: 01, 02, 03, 04. Cards: [51db910ccfc8] [0f413fcac223] [7a213481a9d2] [b093ed3b4d75] [eeb9c51fe0da] [4e8335051514] [8883db1cfb1d].

**R36. Set `loading="eager"` explicitly on in-view images, and remember the attribute only works on `<img>`, not CSS backgrounds.** Condition: any image a plugin or theme might lazy-load by default (a demo logo was lazy by default, source 02; a Dawn hero section lazy-loaded its first image, source 01). Background images that must cover a section: convert format, do not resize, do not lazy-load. Sources: 02, 01. Cards: [eeb9c51fe0da] [08e530e7d0b2] [51db910ccfc8].

**R37. Preload and set `fetchpriority="high"` on the LCP image only; set low priority on images far down; never preload many assets.** Condition: hero, first slide, main product image (with Liquid logic per product on PDPs), critical fonts. Too many preloads recreate the contention they were meant to fix. Check syntax against current browser support. Sources: 01, 07. Cards: [d56347d58c66] [b4735bb55b51] [958af3150188] [481d00497deb]. [web check: fetchpriority and preload support]

**R38. Every image and video in normal flow gets `width` and `height` attributes (numbers, no unit) or a CSS `aspect-ratio`.** Condition: all templates. This works only if CSS keeps the aspect ratio. For responsive images whose ratio changes by viewport, use `srcset`. Absolutely positioned images likely do not shift layout but get dimensions anyway. WordPress quick fix: WP Rocket "Add missing width and height attributes". Sources: 01, 02, 05, 07. Cards: [d16d1fcdd349] [f597983f8e66] [883371c7111c] [3932af95de46].

**R39. Large catalogs: automate compression, but measure before and after because the app adds its own scripts, and keep the manual pipeline for hero and launch images.** Condition: hundreds of images or more, or images already uploaded. Bulk apps often touch only product images, so still check Content > Files for section and home page images. CDN image services (Cloudflare, Imgix, Cloudinary) are the alternative at thousands of SKUs. Sources: 01, 04, 08. Cards: [3bbbee3c2099] [64042fc21a8b] [8883db1cfb1d] [baaf2f6aee4e] [3a99be49f292]. [web check: Tiny SEO, SEOAnt, TinyIMG, Hyperspeed still listed]

**R40. One media file per image, reused everywhere; use Replace to update; no empty `src`; combine small icons into a sprite.** Condition: Shopify media library and any theme. Uploading the same file twice makes a second URL and multiplies edits. `<img src=''>` still sends a request. Alt text goes in during the same pass (accessibility and image SEO, not speed; decorative images get empty alt; re-add alt after pasting builder settings). Sources: 01, 03, 02. Cards: [23917da7d97a] [1c99225810ac] [876fb6014fe1] [fe083ee96b08].

**R41. Sliders: 1 strong hero with a clear call to action beats a slider; if a slider is required, 2 to 3 static slides, slide 1 eager and the rest lazy.** Condition: home and collection banners. 4 to 5 auto-rotating slides are heavy (source 03). Sources: 03, 01. Cards: [a459458a1b47] [70af8654d12d] [7a213481a9d2].

**R42. Check non-product images in Content > Files (or the media library) for multi-MB files.** Condition: every Shopify audit. Bulk compressors often skip them. Reduce anything over the ceiling in R31 by download, compress, resize (Shopify's editor resizes but does not compress), compress again, re-upload. Sources: 01. Cards: [3a99be49f292] [0c4e0163aff8] [7558889b0856]. [verify UI: Content > Files]

### Group D. Scripts, apps and third parties

**R43. Inventory every way a script reaches the page before touching any.** Condition: Shopify. Three routes: the async load function inside `{{ content_for_header }}` (lists every app script Shopify injects; scripts via the Script Tag API load async), hardcoded `<script>` tags pasted into theme.liquid (often blocking), and App embeds toggled on in Customize (added straight to the head, so they load early). WordPress: the GTmetrix waterfall and PSI "Render-blocking requests" list everything. Sources: 01, 03, 02. Cards: [2a89f4e58923] [b7d4c6046a25] [b1f2c1da412b] [b711b4ded0ce] [efd7ec0cb6ce] [701c087d0917].

**R44. Uninstalling does not clean the theme; search for and remove residual code after every uninstall.** Condition: after any uninstall, trial, or removed tracking, on Shopify and WordPress alike. Leftover script tags, JS, CSS and rendered snippets keep calling external servers on every page view. Search the brand name and the App Store listing name (they differ: "Hexom" vs "free shipping bar"). Only remove code for apps you have actually uninstalled. Sources: 01, 03. Cards: [3c6bd0cce957] [68699dfd59de] [fde546149035] [10d064e032f8] [58c5589c135f] [efd7ec0cb6ce].

**R45. Before installing anything: check reviews for speed complaints, check the theme already lacks the feature, and run a speed test before and after.** Condition: every new app or plugin, for the life of the store. Sources: 01, 04, 03. Cards: [8dbbb42b9c2e] [c09e2fd0f0d7] [74fc1378fc6a] [efd7ec0cb6ce].

**R46. Add `defer` first; if the feature breaks try `async`; if both break, leave the script blocking. Never touch a script whose purpose you do not know.** Condition: every `<script>` without defer or async in theme.liquid or the WordPress head. Source 01 prefers defer ("more powerful": runs after the document loads; async downloads alongside without blocking); source 03 offers both without a rule; its card adds defer for scripts that need order, async for independent ones. Expect small gains per script (78 to 80 after one defer). Unknown speed or caching service scripts: test by commenting out; if speed is unchanged, leave them. Sources: 01, 03, 04, 05. Cards: [1dffb0dd47d1] [1d1dca3e3cfb] [07b358e531fb] [e42f2f04f259] [c09e2fd0f0d7] [8f0d567d9844] [cdc61c33e699]. See 7.11.

**R47. Delay scripts for widgets that are not in view and not part of the buying flow until the first user interaction.** Condition: loyalty, chat, cookie banner, social feed, SMS pop-up, review widgets below the fold, upsell drawers. Exceptions: widgets that must show at load (for example review stars above the fold; the brand record must say which), payments and fraud scripts (source 09's card), and tracking pixels (source 01 says never delay them; the cards say follow tested behaviour per integration; see 7.7 and R48). Source 01 claims 10 to 20% score gains when apps are the bottleneck, and says the delay helps little while CLS or LCP is large. Sources: 01, 04, 09, 05. Cards: [4e05290f17d5] [9714159dd4aa] [d1007a68a9e0] [56315833a352] [dc6cd41ae52d] [c09e2fd0f0d7] [8f0d567d9844]. [needs brand data: which widgets must show at first paint]

**R48. Tracking: never change how pixels load without testing page view, variant, add to cart and a test purchase for missing and duplicate events, with consent on and off.** Condition: any defer, delay, tag manager change or content_for_header override. Source 01's rule is to keep Facebook and Google pixels and Hotjar in the initial load; the card correction says use Shopify's supported pixel integration (Web Pixels API and standard events) and verify each integration. Duplicate injections are common (Facebook loaded twice: once by hand in theme.liquid, once by an app). Pixel setup itself is 06-MEA. Sources: 01, 03, 09. Cards: [15d23b16ff3c] [ef51a42e0e16] [20821a7ae674] [adc3ea59042a] [81ac749043da] [78f603581ed4] [dc6cd41ae52d]. [needs brand data: pixel and consent setup] [web check: current Shopify Web Pixels guidance]

**R49. Load an app's assets only on the templates that use its widget, and remove duplicate injections.** Condition: any script or stylesheet flagged as unused on a template where its widget is not visible (reviews and subscriptions only on collection and product pages; rewards only on the rewards page; a carousel library only where a carousel is in view at load). WordPress: unload per page with Asset CleanUp and write down what you unloaded, so a later mini cart gets its files back. Sources: 01, 02, 04, 08. Cards: [adc3ea59042a] [81ac749043da] [44c02380f01e] [c067983b290a] [3d795cd17d4b].

**R50. Remove jQuery and other libraries if unused; if you must keep one, self-host it from the theme assets instead of an outside CDN.** Condition: any theme loading a library from a third-party CDN. WordPress: dequeue jQuery only for logged-out front-end visitors (the admin bar needs it) and only if theme and plugins do not need it. Sources: 01, 02. Cards: [fdbc70a82f75] [0d00d9d01688] [81ac749043da].

**R51. Turn off every app embed you do not actively use, and re-check embeds after uninstalls.** Condition: Shopify, Customize > App embeds. An uninstalled app's embed should disappear; if it is still listed and unused, turn it off. Sources: 01. Cards: [d675d594782b] [4e05290f17d5]. [verify UI]

**R52. Never comment out `{{ content_for_header }}` on a live theme.** Condition: always. It is a diagnostic only (score went 80 to 100 on a demo) and breaks apps and platform features; the editor flags it as an error. The supported way to delay app scripts wraps or filters it (P10). Sources: 01. Cards: [b7d4c6046a25].

**R53. Non-essential integrations load after product images and product information; integrations that touch payment or fraud may need to load earlier.** Condition: any third-party on a product page. Check that analytics still fire after deferring (R48). Sources: 09, 01, 03. Cards: [dc6cd41ae52d] [ad877c2f348c] [4e8335051514].

**R54. A tag manager is for inventory and a kill switch, not for speed by itself; measure the waterfall.** Condition: stores with many tracking tags. The claim that a container "condenses all tags into one request" is wrong (card correction). Use it to remove a failing tag fast. Sources: 03. Cards: [78f603581ed4]. [verify UI: Shopify tag manager setup]

**R55. Be skeptical of speed apps and caching scripts; test them like any other change.** Condition: Shopify especially. Source 01: no magic app; speed apps "only work for returning users, if at all"; Shopify already caches, so caching scripts add nothing. Source 04 names Hyperspeed and TinyIMG for minification and source 05 uses WP Rocket on WordPress. Merged: on Shopify default to no speed app; on WordPress a cache and optimization plugin is normal but every setting is tested 1 at a time (R26). See 7.12. Sources: 01, 04, 05. Cards: [5f44ccb5ead1] [cdc61c33e699] [23a3f294b81c] [c067983b290a] [8f0d567d9844]. [web check: whether speed apps only help returning users]

**R56. Dynamic checkout (wallet) buttons: disable if shoppers do not use them; otherwise delay their script to interaction and accept that the buttons appear late.** Condition: Shopify product pages. Source 01 calls the script demanding. The trade-off is not measured. Sources: 01. Cards: [98a7bf9f5fb4]. [needs brand data: dynamic checkout button usage]

**R57. Count third-party services per page as a leading metric and hold it in the budget.** Condition: every audit and every app request. Each third-party script adds 34.1 ms on average (source 06); in many stores scripts are over 50% of load time (source 08); the count correlates with score at r = -0.66 (source 04). Beauty stores average 31 services per page, automotive 15 (source 04). Sources: 04, 06, 08. Cards: [c09e2fd0f0d7] [a62896aba3d8] [3d795cd17d4b].

**R58. Moving third-party scripts to a web worker (Partytown) is a developer task and needs per-tool testing.** Condition: rebuild or framework storefront; not every script is compatible. Sources: 07. Cards: [717cf5ec82fd].
