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
