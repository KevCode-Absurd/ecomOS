# Website Speed Optimization Tips for Shopify Stores

source_id: 1XSgByl2dRVRm29K0fXOFIzVTwwHkPqYx  |  folder: /08-SPD-speed  |  cards: 15  |  words: 5767  |  type: article
credibility: Shopify (Shopify Plus) marketing blog. It sells Shopify Plus (the page carries a "$399 USD for one month" trial offer) and promotes Storefront Renderer, the Fastly CDN, Shop Pay and Plus Partners. Evidence is a mix of third-party studies (Deloitte, Portent), survey figures, Shopify-reported platform numbers, merchant case studies (Rhone, JB Hi-Fi, Merchology, Kotn) and quotes from agency owners (the49, GoGoChimp, Anatta, Loopex Digital, Eightvape). No own controlled tests.
date signals: Rhone adopted SFR in April 2020. Mobile commerce "projected to account for 10.4% of all ecommerce sales by 2025". Recommends AMP apps and "first meaningful paint", both older-era advice. Mentions Commerce Components by Shopify. Probably written or last updated around 2023 to 2024; no date printed.

## 1. What this source is for

Use it to plan speed work on a Shopify store and to make the money case for it. It lists 13 fixes with Shopify-specific mechanics: app scripts in `{{ content_for_header }}`, the `asset_url` filter for CDN versions, Liquid loop clean-up, Quick View cost on collection pages, lite video embeds, redirects, parser-blocking scripts, tag management, mobile video autoplay and Shop Pay for mobile checkout. It also names 3 test tools and what each reports.

## 2. Principles

1. **Speed costs money; do the math with your own numbers.** Condition: when building a business case. Source example: $60 AOV and 5,000 visitors a day, a 1-second delay "could be costing you $9,000 a day". The source does not show how it got $9,000. Recompute with real AOV and traffic. [b36e60f619f7] [needs brand data: AOV, daily sessions, conversion rate by load time]
2. **Target 2 seconds or less for an ecommerce page.** Condition: the source attributes this to Google. "The faster, the better." It also says a good speed for SEO is "below two seconds". [b36e60f619f7] [web check: current Google guidance; Core Web Vitals thresholds]
3. **The platform sets the ceiling.** Condition: if the platform does not prioritize speed, "the rest of the suggestions that follow won't make as big of a difference". Source is Shopify, so this claim serves its sales goal. [54e3673579e3]
4. **Plan hosting capacity for peak events.** Condition: before BFCM-type sales. Check memory and bandwidth limits and projected peak load; ask the platform provider to help prepare. [54e3673579e3]
5. **Every app has a speed cost.** Condition: most app script and CSS files are injected into `<head>` of `theme.liquid` through `{{ content_for_header }}`. Scripts added through the Script Tag API load async so page load is not halted; scripts put straight into `<head>` "often [have] an immediate impact on performance" (Jason Bowman, Shopify). Rule of thumb: more than 20 apps installed means you likely do not use them all. Ask before each install whether the value outweighs the slowdown. [efd7ec0cb6ce]
6. **A lean theme beats a feature-heavy one.** Condition: when choosing or rebuilding a theme. Quote: "You don't need a theme with all the bells and whistles." One agency saw "greater than 50% improvement in homepage bounce rate for new visitors" after switching to a streamlined theme (single observation). Anatta: "Quick speed hacks will not build the foundation... that starts with optimizing your underlying theme architecture." [a459458a1b47]
7. **Balance speed with the customer journey.** Condition: always. Tools guide decisions, but do not strip parts of the UI that help the journey just to win a score. [9bd3f7aed489] [b36e60f619f7]
8. **Images are the biggest weight.** Condition: most pages. Images are 50% to 75% of page weight; each image adds an HTTP request; the problem grows with catalog and blog size. [1c99225810ac]
9. **How JavaScript loads decides whether it blocks.** Condition: any `<script>` tag. "JavaScript itself does not block browsers." Add `defer` or `async`, then check the site still works. [e42f2f04f259]
10. **Checkout belongs in speed work.** Condition: mobile especially. Delay at checkout loses impulse shoppers and raises cart abandonment. [0bc2087de2a1]
11. **Remove Quick View rather than optimize it.** Condition: collection pages where Quick View pre-loads product data. AJAX-on-click or data attributes are "less ideal than removing" it. [6f05e9392e74]

## 3. Procedures

### 3.1 Build the business case
1. Use benchmarks as direction only: Google 2 seconds or less; Portent 1-second sites convert 2.5x vs 5-second sites; Deloitte 0.1 s faster = 8.4% more retail conversions and almost 10% more spend per session; conversion down 0.3% per extra second; 70% of consumers say slow sites hurt willingness to buy.
2. Plug in your own AOV and daily visitors. [needs brand data: AOV, daily sessions]
3. Measure your own baseline before and after; do not quote the example as a forecast.
4. Order work by likely payoff: images first (50% to 75% of weight), then async/defer, app removal, Liquid clean-up (order is the card's reading of the source). [b36e60f619f7]
5. If you lack in-house skill, the source points to a Shopify Plus Partner.

### 3.2 Audit and remove apps
1. List installed apps. Flag trials and unused apps. More than 20 is a warning sign.
2. Have a developer remove unneeded apps and any leftover code.
3. Re-test with GTmetrix, PageSpeed Insights, or Chrome DevTools > Network tab > reload. [verify UI]
4. Prefer apps whose scripts come through the Script Tag API (async) over code pasted into `<head>`.
5. Before each new install, ask whether its value beats its load cost. [efd7ec0cb6ce]

### 3.3 Use `asset_url` so the CDN serves the current file
1. Reference theme CSS and JS through the `asset_url` filter. Shopify adds a version to the URL, for example `?v=1384022871`, which tells the CDN to pull the new version. The card gives the Liquid form `{{ 'theme.css' | asset_url | stylesheet_tag }}` (the article itself does not print code).
2. Find URLs typed directly inside CSS. They are static and do not carry the version, so edits may not show.
3. Change that CSS to use the `asset_url` filter.
4. Check the Shopify Help Center list of URL filters. [verify UI] [5748b07d6cda]

### 3.4 Clean up Liquid loops
1. Review theme code for `for` loops that crawl all products in a collection to find a condition (price, tag).
2. Find loops run more than once for the same data. Common when several developers worked on the theme.
3. Remove the duplicates.
4. Where it fits, use the simpler `product.options_with_values` loop.
5. Loops are fine for outputting images or variants and on small collections; repetition is the problem. No gain figure given. [11d911ca0868]

### 3.5 Deal with Quick View on collection pages
1. Check if thumbnails show a Quick View button.
2. Use click maps (Hindsight, Hotjar) to see if shoppers use it. [verify UI]
3. Find the source: theme customizer toggle first; then check apps; if neither, it is in theme code and needs a developer or Plus Partner. [verify UI]
4. Preferred: remove it.
5. If it must stay: load product data by AJAX only when clicked, or store a small set of product data as data attributes on the grid item and build the pop-up with JavaScript. [6f05e9392e74]

### 3.6 Pop-ups and hero sliders
1. Pop-ups: set triggers that leave room between page load and pop-up load. The source names exit-intent and time-delay triggers. (The sentence in the article reads "Display immediately upon page load, such as exit intent or time delay"; the examples show the intent is to not show on load. The card repeats the garbled wording.)
2. Sliders: cut the number of slides or remove the slider. 4 to 5 slides is flagged as heavy.
3. Prefer 1 strong hero image with a clear call to action.
4. If a slider is required: 2 to 3 slides, static content sections instead of auto-rotating carousels, and `srcset` or lazy load. Example: Chubbies uses optimized images instead of a slider. [a459458a1b47]

### 3.7 Images
1. Compress losslessly (TinyJPG, TinyPNG). [verify UI]
2. Use Shopify's image size parameters to request the exact display size from the CDN. [verify UI: parameter syntax]
3. Remove empty image sources `<img src=''>`; they still send a request.
4. Combine small icons into a CSS sprite.
5. Stores adding many products or posts: build a review habit. Example: Loopex Digital client, images took 60% less space. [1c99225810ac]

### 3.8 Video
1. Replace standard YouTube embed code with a lite embed: only the thumbnail loads (about 15 KB); the player and its JavaScript load on click. Saves "almost a megabyte" per page.
2. Standard embeds also use a fixed-size `<iframe>` that does not adapt to screen size.
3. On mobile, turn off video autoplay. Show a static thumbnail and a play button. [badac5a4a278]

### 3.9 Redirects and broken links
1. Replace 302 (temporary) redirects that should be permanent. Use Shopify's built-in redirects in the Navigation panel (301 by default) or a "cacheable redirect". [verify UI]
2. Never redirect to a URL that itself redirects (no chains).
3. Find broken links to images, CSS and JS with a tool such as Broken Link Checker, and remove them.
4. Build a custom 404 page. Example: Gymshark sends 404 visitors to its 2 biggest categories (women's and men's). [2cd7ecfea589]

### 3.10 Lazy loading
1. Load above-fold content at once: on a product page, title, images, description.
2. Lazy-load supporting content: user-generated content, social carousels, reviews.
3. Reason: browsers download every image on a page at once, visible or not, unless lazy loading is used. [4e8335051514]
4. Check that first-view content is not delayed.

### 3.11 Parser-blocking scripts
1. Find `<script>` tags without `defer` or `async`.
2. Change `<script src="jquery.js"></script>` to `<script src="jquery.js" defer></script>` (or `async`).
3. Test that the site still works the same. [e42f2f04f259]

### 3.12 Tracking tags
1. Inventory tracking tags (analytics, conversions, goals, retargeting).
2. Manage them in a tag manager (Google Tag Manager). The article claims a TMS "condenses all your tags into one JavaScript request"; the card's editorial correction says a container does not make all vendor tags 1 request, so measure the waterfall.
3. Use the TMS to remove a failing tag fast if it breaks the site.
4. Setup: "one snippet of code" per the Shopify Plus Help Center. [verify UI] [78f603581ed4]

### 3.13 Mobile
1. Turn off video autoplay (3.8).
2. Include checkout in speed work. Turn on Shop Pay. [verify UI] [0bc2087de2a1]
3. The source also suggests AMP via Shopify apps (AMP, Fire AMP, The AMP App). [web check: whether AMP is still worth using and these apps still exist]

### 3.14 Run a speed test
1. Use PageSpeed Insights for Core Web Vitals status (Good, Needs Improvement, Poor) and tailored fixes. You can also test competitor mobile sites.
2. Use GTmetrix for an A to F grade, load speed, Web Vitals and Lighthouse data, opportunities, and page composition by requests and bytes.
3. Use Pingdom for a 0% to 100% score and a line-by-line waterfall.
4. Know the markers: fully loaded, time to first byte, first meaningful paint. Each tool picks its own "page load" marker, so scores do not compare across tools. [9bd3f7aed489] [verify UI]

## 4. Rules, thresholds and numbers

| rule | number or threshold | condition | source's basis | card id |
|---|---|---|---|---|
| Page load target | 2 seconds or less | ecommerce page; "faster is better" | attributed to Google | [b36e60f619f7] |
| Conversion vs load | 1 s converts 2.5x vs 5 s | ecommerce sites | Portent | [b36e60f619f7] |
| Chart in article | 3.05% at 1 s vs 1.68% at 2 s | chart caption | article chart | [b36e60f619f7] |
| Speed lift | 0.1 s faster = +8.4% retail conversions, almost +10% spend | retail | Deloitte | [b36e60f619f7] |
| Conversion loss | -0.3% per extra second | average ecommerce store | uncited | [b36e60f619f7] |
| Money example | $60 AOV x 5,000 visitors/day > $9,000/day for 1 s | example only | article arithmetic, not shown | [b36e60f619f7] |
| Shopper attitude | 70% say slow site hurts willingness to buy | survey | uncited | [b36e60f619f7] |
| Downtime cost | 81% say 60 min downtime costs > $300,000 | survey | "one survey" | [54e3673579e3] |
| App count warning | more than 20 apps | heuristic, weight matters more than count | opinion | [efd7ec0cb6ce] |
| Image share of weight | 50% to 75% | typical page | uncited | [1c99225810ac] |
| Hero slider | 2 to 3 slides max; 4 to 5 is heavy | only if a slider is required | UX best practice claim | [a459458a1b47] |
| Quick View cost | pre-loads data for 20 to 30 thumbnails | collection page | mechanism | [6f05e9392e74] |
| Lite embed | thumbnail about 15 KB; saves almost 1 MB | YouTube embeds | article | [badac5a4a278] |
| Core Web Vitals pass | users 24% less likely to abandon mid-load | sites meeting thresholds | uncited research | [9bd3f7aed489] |
| Shop Pay | 1.91x higher mobile checkout-to-order rate | vs regular checkout | Shopify-reported | [0bc2087de2a1] |
| SFR | 2.5x to 5x faster server-side | Shopify Storefront Renderer | Shopify-reported | [54e3673579e3] |
| Shopify Plus | 99.98% uptime; storefront 2.97x faster than other SaaS | vendor claim | Shopify | [54e3673579e3] |
| AMP | 2x time on page, +20% conversions | vs non-AMP pages | uncited | [0bc2087de2a1] |
| First impression | 94% design related; formed in 0.1 s | persuasion figure | "studies show" | [a459458a1b47] |
| Image vs text | brain processes images 60,000x faster | persuasion figure | uncited | [a459458a1b47] |
| Redirect type | use 301; avoid 302 for permanent moves; no chains | all redirects | SEO and request cost | [2cd7ecfea589] |

## 5. Diagnostics and checks

| check | how | good | bad | next |
|---|---|---|---|---|
| App load | count apps; read `<head>` output of `content_for_header`; waterfall | few apps, scripts async | 20+ apps, trials left on, scripts in `<head>` | remove (3.2) |
| Stale CSS/JS after edits | view page source for `?v=` on asset URLs; check URLs inside CSS | versioned URLs via `asset_url` | hardcoded URLs in CSS | 3.3 |
| Duplicate Liquid loops | code review of theme templates | each collection crawl once | same loop in several snippets | 3.4 |
| Quick View cost | network requests on a collection page load; click map | no product data pre-loaded | full product data for every tile | 3.5 |
| Slider weight | count slides and image sizes | 1 hero or 2 to 3 static slides | 4 to 5 auto-rotating large slides | 3.6 |
| Empty image src | search code for `src=''` | none | present | remove |
| Video embeds | network tab before clicking play | only thumbnail loaded | player JS loaded on page load | lite embed (3.8) |
| Redirects | crawl or redirect list | 301s, no chains | 302s, chains | 3.9 |
| Broken asset links | Broken Link Checker | none | 404 on images, CSS, JS | fix |
| Parser-blocking | PSI or waterfall; inspect `<script>` tags | `defer`/`async` set | plain `<script src>` in head | 3.11 |
| Tags | waterfall per vendor tag | each tag justified | many tracking scripts | 3.12 |
| Checkout speed on mobile | not specified by source | Shop Pay on | long forms on mobile | 3.13 |

## 6. Tools, settings and named features

- Google PageSpeed Insights: Core Web Vitals status, recommendations; can test competitors. [verify UI]
- GTmetrix: A to F grade; source says it merges YSlow and PageSpeed data. [verify UI] [web check: GTmetrix now uses Lighthouse; YSlow reference may be old]
- Pingdom: 0 to 100 score, waterfall analysis. [verify UI]
- Chrome DevTools Network tab: manual reload test. [verify UI]
- Shopify Storefront Renderer (SFR), Fastly CDN (free with Shopify), Commerce Components by Shopify.
- Liquid: `{{ content_for_header }}`, `asset_url` filter, `product.options_with_values`, Script Tag API. [verify UI: Shopify docs]
- Shopify image size parameters. [verify UI]
- Shopify redirects in Navigation (301 default). [verify UI]
- Theme customizer (Quick View toggle). [verify UI]
- Hindsight, Hotjar: click maps.
- TinyJPG, TinyPNG: lossless compression.
- Broken Link Checker.
- Google Tag Manager.
- Shop Pay.
- AMP apps: AMP, Fire AMP, The AMP App. [web check: still available]
- Lite embeds for YouTube (no library named).

## 7. Examples and case results

Examples only, mostly vendor-reported.
- Rhone Apparel, SFR from April 2020, vs prior month: revenue +15%, conversion +17%, average page load -12%, server response -37.95%, bounce -3%.
- JB Hi-Fi: down 2 hours in BFCM before moving; after Shopify Plus, record sales on nearly double traffic with no performance issues.
- Red Dress Boutique: about $100,000 a year saved on license, hosting and CDN.
- Merchology: mobile-first redesign, +40% mobile conversion rate 2 months after launch.
- Agency (the49): >50% better homepage bounce rate for new visitors after moving to a streamlined theme.
- Loopex Digital client: images 60% smaller after resize and compression.
- Anatta beauty client: Shopify APIs plus GTM clean-up "moved the needle more than anything else".
- Gymshark: 404 page links to women's and men's clothing.
- Kotn: Shop Pay removed the form step; "if they have to fill out a form, we've lost them".
- Chubbies: optimized category images instead of a hero slider.
- Lululemon, J.Crew, Lowe's named as retailers with sale-period crashes.

## 8. Mistakes the source warns about

- Keeping trial or unused apps installed. [efd7ec0cb6ce]
- Pasting scripts straight into `<head>`. [efd7ec0cb6ce]
- Hardcoding asset URLs inside CSS, so the CDN serves old files. [5748b07d6cda]
- Running the same Liquid loop several times. [11d911ca0868]
- Quick View that pre-loads every product on the grid; it also adds a step, gets clicked by accident, and is mistaken for a product page. [6f05e9392e74]
- Too many pop-ups and flashing graphics; 4 to 5 slide auto-rotating hero sliders. [a459458a1b47]
- Empty `src` attributes. [1c99225810ac]
- Standard YouTube embeds and mobile autoplay. [badac5a4a278]
- 302 redirects, redirect chains and broken asset links. [2cd7ecfea589]
- Leaving checkout out of speed work. [0bc2087de2a1]
- Picking a theme for "bells and whistles". [a459458a1b47]
- Relying on quick hacks instead of theme architecture. [a459458a1b47]

## 9. Caveats, conflicts and what is missing

- Vendor source. Platform claims (SFR, uptime, 2.97x, Shop Pay 1.91x) are Shopify's own numbers.
- Statistic conflicts inside the article: the 8.4% figure is tied to a "0.1 second" gain in one place and a "millisecond" gain in two others. The chart says 3.05% at 1 s vs 1.68% at 2 s, while the text says 2.5x is 1 s vs 5 s. Treat the direction as the finding, not the exact number. [b36e60f619f7]
- Heading "Enable quick view on category pages" contradicts its own body, which argues to remove Quick View. Follow the body.
- The pop-up trigger sentence is garbled (see 3.6).
- Core Web Vitals are described with "fully loaded", "time to first byte" and "first meaningful paint". These are not the Core Web Vitals (LCP, INP, CLS). Do not use this source for CWV definitions. [web check: current CWV metrics and thresholds]
- AMP advice and the "10.4% of ecommerce by 2025" mobile figure look dated.
- GTM claim of "one JavaScript request" is corrected by the card: measure the waterfall. [78f603581ed4]
- Thin on how: no code for lite embeds, AJAX Quick View, image size parameters or GTM setup; mostly points to a developer or Plus Partner.
- `defer` vs `async`: the article offers both as fixes and does not say which to use when. The card adds a rule (defer for ordered scripts, async for independent ones) that is not in the article text. [e42f2f04f259]
- Headless commerce and Commerce Components are mentioned but belong to 05-SET.

## 10. Card index

- [b36e60f619f7] Prioritize speed fixes by financial impact and conversion benchmarks
- [5748b07d6cda] Use asset_url to force Shopify CDN cache refresh
- [11d911ca0868] Deduplicate Liquid forloops to cut server execution time
- [efd7ec0cb6ce] Audit and remove third-party apps slowing your Shopify store
- [e42f2f04f259] Unblock HTML parsing with defer and async on script tags
- [1c99225810ac] Compress and resize images with correct Shopify size parameters
- [badac5a4a278] Replace standard YouTube embeds with lite embeds
- [6f05e9392e74] Remove or defer Quick View pop-ups on collection pages
- [a459458a1b47] Cut pop-ups and hero sliders that add page weight
- [2cd7ecfea589] Clean up redirects, broken links, and use 301s correctly
- [4e8335051514] Apply lazy loading to below-fold content
- [78f603581ed4] Consolidate tracking tags with a tag management system
- [9bd3f7aed489] Run and interpret website speed tests with the right expectations
- [0bc2087de2a1] Optimize mobile checkout with Shop Pay and mobile-first speed
- [54e3673579e3] Research hosting and platform capacity for peak traffic events
