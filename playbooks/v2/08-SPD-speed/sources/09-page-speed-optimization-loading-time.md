# Page Speed Optimization: How to Improve the Loading Time of Your Online Shop

source_id: 1S-GQ3bEp-JK5GQ1HOKSMUk90q2A0--UN  |  folder: /08-SPD-speed  |  cards: 10  |  words: 1770  |  type: article
credibility: Blog post from an ecommerce platform vendor. The vendor is not named in the text; it says "a shop system that supports optimized page speeds isn't just nice to have" and pushes a downloadable guide, "Marketing ROI: How to Increase Your Profit Return by Five". British spelling and a mention of Ecosia suggest a European vendor. Evidence: 1 named study (Akamai) plus uncited survey figures. No case studies, no own tests.
date signals: No year. Uses Time to Interactive (TTI), a metric Lighthouse has since dropped, and defines TBT as the time between FCP and TTI. Does not mention INP or CLS. Likely older content (roughly 2020 to 2023).

## 1. What this source is for

Use it for the architecture-level levers a platform or developer team controls: server-side rendering vs client-side rendering (and a hybrid), CDN for static files, browser and server caching, and fast, well-structured APIs that return only the data a page needs. It also gives a short list of first steps: measure mobile and desktop, compress and size images per device, lite embeds for video, and load third-party integrations after the main content.

## 2. Principles

1. **Speed affects sales, return visits and SEO.** Slow shops lose buyers to faster shops. High bounce "sends negative feedback" to Google and other engines (Ecosia named); speed is "not the only ranking factor... but it is an important one". [af5fd5b1745b]
2. **Measure first, on both mobile and desktop.** Results "differ significantly" between the 2. If most customers shop on mobile, fix mobile first. [b35da7f37105] [needs brand data: mobile share of sessions and revenue]
3. **Cross-check with more than 1 tool.** "Don't just rely on Google"; also use GTmetrix or Pingdom's Website Test. [b35da7f37105]
4. **Stable, fast hosting is a basic.** No detail given. [3d5cfd45530c]
5. **Never send an XXL image to a small phone.** Compress images and serve different sizes by page, usage and device. [3d5cfd45530c]
6. **Load video players only on click.** Lite embeds load a thumbnail; the player loads when the user clicks. The same idea applies to other third-party integrations. [0021f744e1e0]
7. **Question every third-party integration.** Remove unnecessary ones. Load the rest only after the main page (product images and product information) has loaded. [dc6cd41ae52d]
8. **Server-side rendering is more reliable than client-side rendering.** Client-side rendering depends heavily on the visitor's connection; SSR needs more server power but displays the page directly and faster. "Often a combination of both is the best choice": server does complex tasks, browser does the rest and reduces server load. [171da560af89]
9. **CDNs serve content from the server closest to the user.** [6e2d4fa52ebe]
10. **Caching can live in the browser and on the server.** It stores product data and other content so it is available faster. [9973ef4b38a5]
11. **Fast, well-structured APIs reduce the need for caching.** A clear structure lets you select exactly which data to load, which cuts response and loading times. [34052dbf559b]

## 3. Procedures

The source is light on steps. What it gives:

### 3.1 Measure
1. Open Google PageSpeed Insights (free). Run it for desktop and mobile. [verify UI]
2. Read the good / mediocre / poor classification for each metric.
3. Read the recommendations and the estimated time each would save. Card: order work by saving vs effort.
4. Check the same page in GTmetrix or Pingdom Website Test. [verify UI] [b35da7f37105]

### 3.2 First fixes
1. Compress images.
2. Create different image sizes by page, usage and device.
3. Replace video embeds with lite embeds.
4. List third-party integrations; remove the unneeded ones.
5. Load the remaining integrations after product images and information have loaded. Card caveat: some (payments, fraud) may need to load earlier; check analytics still fire after deferring. [3d5cfd45530c] [0021f744e1e0] [dc6cd41ae52d]

### 3.3 Further setup (platform or developer level)
1. Rendering: move heavy rendering to the server (SSR) or use a hybrid split.
2. Put static content (images, files) on a CDN.
3. Cache product data and content in the browser and on the server.
4. Make APIs fast and structured so each page requests only the fields it needs.
5. Card: re-test FCP, TTI and LCP after a rendering change; size server capacity for SSR first. [171da560af89] [6e2d4fa52ebe] [9973ef4b38a5] [34052dbf559b]

## 4. Rules, thresholds and numbers

| rule | number or threshold | condition | source's basis | card id |
|---|---|---|---|---|
| Latency cost | 100 ms delay > up to -7% conversion rate | | Akamai study | [af5fd5b1745b] |
| Mobile abandonment | 53% leave if over 3 s | mobile visitors | uncited | [af5fd5b1745b] |
| Shopper expectation | 47% expect 2 s or less | online shoppers | uncited | [af5fd5b1745b] |
| Return intent | 79% less likely to shop again on a slow page | | uncited | [af5fd5b1745b] |
| Image sizing | no XXL image on a small phone; sizes per page, usage, device | always | principle | [3d5cfd45530c] |
| Third-party timing | load after product images and info | non-essential integrations | principle | [dc6cd41ae52d] |

Metric definitions as given by this source (see caveats):

| metric | source's definition | card id |
|---|---|---|
| First Contentful Paint | time to the first element the user sees (text or image) | [0e11008fda40] |
| Time to Interactive | time until the site is usable | [0e11008fda40] |
| Total Blocking Time | time between FCP and TTI | [0e11008fda40] |
| Largest Contentful Paint | time until the page is loaded from the user's point of view | [0e11008fda40] |

## 5. Diagnostics and checks

| check | how | good | bad | next |
|---|---|---|---|---|
| Mobile vs desktop gap | PSI both tabs | similar | mobile far worse | fix mobile first if mobile-heavy |
| Tool agreement | PSI plus GTmetrix or Pingdom | same problems flagged | 1 tool's quirk | fix shared findings |
| Page looks ready but ignores taps | FCP fast, long gap to TTI (card reading) | short gap | long gap | scripts blocking; defer or remove |
| Main image slow | LCP | loads fast | heavy hero or product image | compress, size per device |
| Image size vs device | check file sent to a phone | phone-sized file | desktop XXL file | add size variants |
| Video embeds | network on page load | thumbnail only | player code loads before click | lite embed |
| Integration order | load order in waterfall | product content first | integrations before product images | defer integrations |
| API payload | inspect response for a listing tile | only fields shown | full product object | field selection |

## 6. Tools, settings and named features

- Google PageSpeed Insights: good/mediocre/poor ratings, recommendations with estimated time savings. [verify UI]
- GTmetrix, Pingdom Website Test: second opinions. [verify UI]
- Lite embeds (no library named).
- Server-side rendering, client-side rendering, hybrid rendering.
- CDN, browser cache, server cache.
- APIs with field selection (no technology named).

## 7. Examples and case results

None. The source gives only statistics.

## 8. Mistakes the source warns about

- Relying on Google's tool alone. [b35da7f37105]
- Sending large desktop images to phones. [3d5cfd45530c]
- Embedding many full video players. [0021f744e1e0]
- Keeping third-party integrations that are not needed, or loading them before product content. [dc6cd41ae52d]
- Relying on caching to hide slow or unstructured APIs. [34052dbf559b] [9973ef4b38a5]

## 9. Caveats, conflicts and what is missing

- Old metric model. TTI is no longer a Lighthouse metric, and TBT is defined elsewhere (source 05) as the sum of blocking time from long tasks over 50 ms, not "time between FCP and TTI". The card flags this. INP and CLS are not mentioned. [0e11008fda40] [web check: current Lighthouse metrics and CWV]
- The Akamai "100 ms = 7%" figure conflicts with source 04 ("1 s delay = about 7%", Cloudflare) and source 08 ("1 s delay = up to 7%"). Same 7%, 10x different delay. Do not quote either without checking the original. [web check: Akamai 2017 study wording]
- "Speed is an important ranking factor" is stated generally; other sources call CWV a tie-breaker.
- Very thin on how: no steps for SSR, CDN setup, cache rules, API design, or which integrations to defer. Card caveats add: SSR is a major change and needs server sizing; CDN does not fix rendering or API issues; cache lifetimes must match how often price and stock change; field selection needs coordinated API and front-end changes.
- Vendor content with a lead-magnet plug; the vendor is not named.

## 10. Card index

- [b35da7f37105] Diagnose Shop Speed With PageSpeed Insights Before Optimizing
- [0e11008fda40] Map LCP, FCP, TTI and TBT to What Shoppers Actually Experience
- [3d5cfd45530c] Run Image Compression and Device-Specific Sizing as the First Speed Fix
- [0021f744e1e0] Use Lite Embeds to Stop Video From Killing Page Speed
- [dc6cd41ae52d] Audit Third-Party Scripts and Defer the Survivors
- [171da560af89] Choose SSR or Hybrid Rendering for Faster First Display
- [6e2d4fa52ebe] Serve Static Assets From a CDN Close to the Shopper
- [9973ef4b38a5] Layer Caching in Browser and on Server Without Over-Relying On It
- [34052dbf559b] Structure APIs for Precise Data Selection and Smaller Payloads
- [af5fd5b1745b] Prioritize Speed Work With the Latency and Abandonment Evidence
