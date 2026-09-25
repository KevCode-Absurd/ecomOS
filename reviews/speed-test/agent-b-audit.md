# Gehna site speed audit (agent B)

Date: 24 September 2026. Site: https://www.gehnaindia.com/. Playbook: `playbooks/v2/08-SPD-speed/PLAYBOOK.md` version 2.0-draft. Raw data: `reviews/speed-test/raw-b/` (JSON per page, 1 file per page with all runs, plus screenshots).

Who this is for: the owner first, then the developer. Section 5 is the fix list. Every number in this report was measured by me today or comes from the repo's own Metabase export. Nothing is estimated unless it says "assumption".

## 1. Verdict

The site is slow on the phones most Gehna shoppers use, and the cause is not the server or the product photos. It is the way the site is built. Two things dominate. First, every page preloads 2 font files of about 950 KB and 900 KB each (the serif headline font in its full form, not trimmed to the letters the site uses). On a slow 4G connection these 2 files hold the network for 13 to 19 seconds, so everything else queues behind them. Second, the pages are built as a JavaScript app: the product grid on collection pages and the main product image and price on product pages are not in the HTML the server sends. They only appear after all the JavaScript has downloaded and run. On a slow 4G phone the home page hero appears at 7.9 s, the collection grid at about 15 s, and the main product image at 18.3 s. Google's "good" line for the largest element (LCP) is 2.5 s. Layout shift is also over the line on collection (0.11) and product pages (0.13) because content arrives late and pushes the page down. The good news: server response is fast (under 0.5 s), product photos are already small AVIF files, static files are cached for a year, and third-party scripts are already held back until after load. Fixing the fonts is a small developer job that removes about half of every page's weight. Rendering product content on the server is a bigger job but it is the only way to get product pages near 2.5 s.

## 2. What I measured, how, and the numbers (P1, P2, R1, R10, R15, R16, R19)

### 2.1 Method

- Tool: headless Chromium (Playwright) with a Pixel 5 phone profile (393 x 851 CSS px, device pixel ratio 2.75, mobile user agent, touch on).
- Network: Chrome's "Slow 4G" preset (1.6 Mbps down, 750 Kbps up, 150 ms round trip). CPU slowed 4x. Cache empty on every run (cold, first visit). This is close to what Lighthouse uses for its mobile lab test, but it is not Lighthouse, so no score out of 100 is given. Google PageSpeed Insights could not be used today (API quota exhausted).
- Runs: 3 per page, fresh browser profile each time, median reported (R15 says average 3; I use the median because it resists 1 odd run). Individual runs are listed so you can see the spread.
- Metrics captured in the browser: server response (TTFB), first paint of any content (FCP), largest element paint (LCP) and which element it was, layout shift (CLS) and which elements moved, long tasks over 50 ms and a blocking time estimate (TBT est = sum of long-task time over 50 ms; close to Lighthouse TBT but not identical), load event, request count, bytes by type, image natural vs rendered size, font faces, third-party hosts, response headers.
- Also 1 desktop run of the home page with no throttling (R10 says check desktop too) and 8 small `curl` fetches for headers (home, collection, product, cart, a fake URL, the hero image). Total page fetches: 20.
- Location: the test machine is in the USA and goes through a proxy. Indian shoppers hit Cloudflare and CloudFront edges in India, so their TTFB will differ. Everything after TTFB (bytes, order of loading, JavaScript work) is the same for them.
- Web checks in playbook section 10 (web.dev thresholds and so on) could not be fetched: web.dev is blocked on this network. I used the thresholds in playbook section 6 (LCP 2.5 s, INP 200 ms, CLS 0.1, TTFB 800 ms). [web check: not done today]
- INP (interaction delay) is a field metric and needs real users. Not measured. The lab stand-in is long tasks and TBT est.

### 2.2 Baseline table (mobile, slow 4G, cold cache, median of 3)

| Page | URL | TTFB | FCP | LCP | LCP element | CLS | Long tasks | TBT est | Load event | Requests | Bytes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Home | / | 429 ms | 1.10 s | **7.88 s** | Hero banner image `new-arrivals-mobile.png` (PNG, 279 KB) | 0.000 | 25 | 3.98 s | 19.3 s | 113 | 4.04 MB |
| Collection | /m/rings | 128 ms | 0.76 s | **6.58 s** | The loading spinner `loading.gif`. The real product grid appeared at about 15 s | **0.110** | 14 | 2.64 s | 13.4 s | 93 | 2.86 MB |
| Product | /verdant-whisper-emerald-18k-gold-ring | 345 ms | 0.87 s | **18.26 s** | Main product image (AVIF, 25 KB). Its request only started at 17.1 s | **0.129** | 18 | 3.00 s | 14.3 s | 90 | 2.88 MB |

Individual runs (TTFB ms, FCP ms, LCP ms, CLS, TBT est ms, load ms, requests, KB):

- Home: (483, 1220, 8016, 0.000, 4534, 19389, 118, 3942) (429, 1096, 7880, 0.000, 3981, 19339, 113, 3944) (204, 916, 7760, 0.000, 3552, 18960, 107, 3867)
- Collection: (117, 756, 2032, 0.109, 2837, 13374, 91, 2736) (128, 764, 6612, 0.110, 2638, 13516, 94, 2795) (135, 792, 6576, 0.110, 2565, 13356, 93, 2795)
- Product: (1262, 1852, 20128, 0.129, 2992, 15143, 94, 2823) (345, 872, 18112, 0.129, 3000, 14308, 90, 2814) (117, 732, 18264, 0.131, 3143, 14083, 89, 2814)

Spread is small (LCP within 0.3 s on home and product; collection run 1 recorded the spinner earlier at 2.0 s, runs 2 and 3 at 6.6 s). Page weight and request counts are stable, so the results are not noise (5.1 "score stability").

Desktop, home page, no throttling, 1 run: TTFB 1,054 ms, FCP 1.49 s, LCP 5.34 s (desktop hero, AVIF 78 KB), CLS 0.004, 11 long tasks, TBT est 0.73 s, load 5.27 s, 154 requests, 3.28 MB. Even on a fast line the hero takes over 5 s because the 2 big fonts are fetched first.

Against the playbook thresholds (section 6): LCP is "poor" (over 4 s) on all 3 mobile templates. CLS is "needs improvement" on collection and product. TTFB is "good" on all pages. FCP is "good". Blocking time is high (Lighthouse flags anything over about 600 ms).

### 2.3 Slow-connection visual test (P2, R19), in words

- Home: white page for about 1 s, then header, search box and the row of category circles appear as empty grey circles. The category icons fill in over several seconds. The hero photo appears at about 8 s. Nothing jumps. Text is readable and the layout fits the screen (P2 step 7 pass).
- Collection: header appears under 1 s, then a spinner for about 14 s. The grid of 156 rings appears all at once at about 15 s and pushes the page (CLS 0.06 at that moment, on top of 0.025 from the grid container). Filters and sort bar appear with the grid.
- Product: header under 1 s, then a spinner. The product image, name, price and Add to Cart button appear together at about 17 s. The reviews section ("Two Decades of Expertise") lands at about 16.6 s and shifts the body (CLS 0.08). A shopper who taps an ad and lands here sees nothing to buy for 17 s on slow 4G.
- On all pages a thin progress bar at the top animates during load (Material UI LinearProgress). It is harmless for CLS but it tells the shopper the page is still working.

### 2.4 Change log

| Date | Change | Who |
|---|---|---|
| 24 Sep 2026 | Baseline recorded (this report). No changes made to the site. | Agent B |

## 3. How the site is built and where the time goes (R12, R66, 5.4)

### 3.1 Platform, from evidence

- Custom storefront built on Next.js (React), pages router. Evidence: `x-nextjs-cache: HIT` response header, `/_next/static/chunks/pages/_app-...js` and `pages/index-...js`, `__NEXT_DATA__` JSON in the HTML, build id `5HJHbNWyLaaiZsrRMyVjK`. UI library is Material UI (class names `MuiGrid-root`, `jss…`). Data comes from a GraphQL API at `api.gehnaindia.com/graphql` (Apollo client, `initialApolloState` in the page data). Product search and filters are Tagalys (allowed in the CSP header). No Shopify or WooCommerce signatures anywhere. The owner has confirmed custom build.
- Delivery chain: Cloudflare in front (`server: cloudflare`, `cf-cache-status`), then Amazon CloudFront (`x-cache: Hit from cloudfront`, `x-amz-cf-pop`), then the Next.js origin. Product images come from `cdn-assets.gehnaindia.com` and `cdn-images.gehnaindia.com` through Next's `/_next/image` resizer. Cloudflare adds Rocket Loader and an email-decode script to every page.
- Payments: Razorpay. Marketing scripts: Google Tag Manager (GTM-PK4C6HK), Google Analytics (a Universal Analytics tag `UA-41818105-2` and `analytics.js`, which is a retired product), Meta pixel, Klaviyo (11 script files), Microsoft Clarity, CustomerLabs (its script returned 403 in my tests), Google Sign-In, Cloudflare Insights.

Because the platform is custom, the Shopify-only procedures in the playbook (P8 residual code search in theme.liquid, P10 `content_for_header` delay, P12 asset_url, P23 Liquid loops, P32 theme choice) do not apply as written. Where a rule below is Shopify-only I say so and give the custom-code equivalent, marked "adaptation".

### 3.2 Where the time goes on a slow 4G phone (home page, run 1)

| From | To | What is happening |
|---|---|---|
| 0 | 0.48 s | Server response (HTML, 209 KB compressed with brotli, served from cache) |
| 0.6 s | 19.2 s | 4 font files download. 2 of them are 956 KB and 897 KB. They are `preload`ed, so the browser starts them first and they take most of the bandwidth the whole time |
| 0.6 s | 8.0 s | Hero image (PNG, 279 KB) downloads in parallel, slowly, because the fonts share the pipe. LCP fires at 8.0 s |
| 1.2 s | 16.3 s | Category circle icons (PNG 234 KB, 203 KB, 165 KB, 123 KB, 38 KB, 26 KB, 16 KB for 60 x 60 px circles) |
| 1.9 s | 11.7 s | 36 JavaScript chunks, about 480 KB. The main `_app` chunk alone is 145 KB and finishes at 11.7 s |
| about 12 s | 19 s | React hydrates, product carousels render, 25 long tasks (max 876 ms, total 5.8 s of main-thread time) |
| 19.3 s | | Load event. Only now do GTM, Meta pixel, Klaviyo, Clarity, Google Sign-In start (they are correctly held until after load) |
| 20.7 s | 25 s | Third-party scripts run: Meta `fbevents.js` 109 KB, GTM, Klaviyo, Clarity |

Page weight split (home, first visit): fonts 1,921 KB (48%), images 1,375 KB (34%), JavaScript 597 KB (15%), HTML 209 KB, CSS about 30 KB. The 2 big fonts alone are bigger than the playbook's whole-page budget of 2 MB (conflict 7.19).

Collection and product pages follow the same shape: fonts 0.3 s to 13 to 15 s, JavaScript 1 s to 7.6 s, load event at 13 to 14 s, then and only then the page asks the API for products (6 GraphQL calls at 17.3 to 19.1 s on the product page) and renders them. That is why the product image request does not even start until 17.1 s. The image itself is tiny (25 KB AVIF) and arrives 3 s later. R81 applies: "a poor LCP with a fast image download means a script is hiding the image; find the script, not the image".

### 3.3 What is already good

- TTFB under 500 ms on every page (R82 pass). HTML served from cache (`x-nextjs-cache: HIT`, `age` in the thousands of seconds).
- Static files (`/_next/static/...`) carry `cache-control: public, max-age=31536000, immutable` with hashed names and brotli compression, CloudFront hits (R87 pass, 5.9 pass).
- Product photos are served as AVIF through the Next image resizer at sensible widths (25 KB main image, 10 to 30 KB tiles). 57 of 62 image files on the home page were AVIF.
- Marketing and analytics scripts do not start until the load event. They are not the reason the pages are slow (R47 largely already in place).
- No render-blocking scripts in the head except Cloudflare's 1 KB email-decode. CSS is 2 small files.
- Fonts use `font-display: swap` (R70 pass). Text shows in a fallback font while the font loads.
- Layout fits the phone screen, no horizontal overflow, text readable.

## 4. Checklist results (section 5)

Pass, Fail or Partial, with the evidence. "n/a" means the row is for another platform or needs data I did not have.

### 5.1 Measurement setup

| Check | Result | Evidence |
|---|---|---|
| Baseline exists | Pass | Table in 2.2, 3 runs per page, dated |
| Test freshness (P4) | Pass | Fresh browser profile and cold cache per run; HTML `age` header shows a cached copy at the CDN, which is what shoppers get too |
| Field vs lab | n/a | No PSI field data today. All figures are lab. Field confirmation needed later [needs brand data: Search Console Core Web Vitals report] |
| Metric names | Pass | LCP, CLS, TTFB, FCP, TBT used. INP not measurable in lab |
| Score stability | Pass | LCP within 0.3 s on home and product across runs |
| Second tool | Fail | Only my own browser measurement. PSI quota was exhausted and GTmetrix and WebPageTest are not reachable from here. Re-run PSI when the quota resets (P1 step 3) |
| Slow-connection look | Fail | Spinner for 14 to 17 s on collection and product pages; hero at 8 s on home (2.3) |
| Outliers on big sites (P5) | n/a | Not run. Unlighthouse would hit production hard; needs owner go-ahead and a staging URL |

### 5.2 Images

| Check | Result | Evidence |
|---|---|---|
| File weight per image | Fail | Home hero `new-arrivals-mobile.png` 279 KB, served as PNG, over the 250 KB LCP-image cap (R31). Category icons: pendants 234 KB, nose pins 203 KB, earrings 165 KB, bracelets 123 KB, for 60 x 60 px circles. Nothing over 500 KB. Product photos all under 100 KB (pass) |
| Intrinsic vs rendered | Fail | Category icons natural 320 x 320 in a 60 x 60 box (5.3x, R30 says flag over 2x). Home hero: 650 x 1000 PNG shown at 393 x 631 CSS px, fine. Product slides 2 to 4 request `w=2560` for a 361 px box (7x, lazy so not urgent) |
| Responsive widths (srcset) | Pass | Next `srcset` with 640 to 3840 widths on all `next/image` tags |
| Format | Partial | AVIF for product photos (pass). Mobile hero served as PNG (`content-type: image/png`) while the desktop hero of the same section is AVIF 78 KB. The resizer seems to pass the mobile file through untouched, probably because the file (650 px wide) is narrower than the requested 1200 px. Developer to confirm [verify UI]. Category icons served as PNG. `loading.gif` spinner (27 KB GIF) on every collection and product page |
| In-view images lazy? | Fail | Home: 7 category circles, slides 2 and 3 and the WhatsApp button are in view and marked `loading="lazy"` (10 in-view images lazy). Product: gallery slides 2 to 4 in view and lazy (acceptable, only slide 1 must be eager; slide 1 is eager, pass for the LCP element) |
| Below-fold images eager? | Fail | Home: 41 `img` tags carry `fetchpriority="high"`; only 1 of them (the hero) is in view. The other 40 are product carousel tiles 1,000 to 1,900 px down the page. This fights the hero for bandwidth (R37: high priority on the LCP image only) |
| Dimensions set | Pass | All `img` tags have width and height or use `fill` with a sized box. CLS from images is 0 |
| Entrance effects | Partial | Hero is inside a Swiper slider (3 slides). No fade seen. Spinner placeholders on collection and product |
| Non-product images | Partial | Static images live in `/static/images/` in the app, not a media library. Sizes listed above |
| Duplicates, empty src | Pass | No empty `src`. Not checked in the media store [needs brand data] |
| Slider weight | Pass | 3 slides, slide 1 eager with `fetchpriority=high`, slides 2 and 3 lazy (R41 pass) |
| Bulk compressor, compression history | n/a | Custom pipeline. Product photos are already small |

### 5.3 Scripts, apps and third parties

| Check | Result | Evidence |
|---|---|---|
| App count and revenue roles | n/a | No app store on a custom build. Third-party inventory: GTM, GA (Universal Analytics tag, retired product), Meta pixel, Klaviyo, Clarity, CustomerLabs, Google Sign-In, Cloudflare Insights, Razorpay (checkout only), Tagalys (search API), Sentry (errors). Revenue role of each [needs brand data] (R7, P7) |
| Third-party service count | Pass | 8 to 9 third-party hosts per page, inside the 0 to 5 to 10 band the playbook likes best (R57). They cost about 120 KB and run after load |
| Scripts at load | Partial | First-party JavaScript 480 to 600 KB across 36 to 63 files at load. The `_app` chunk is 145 KB and every page needs it. The collection page also prefetches the product page chunk and vice versa (Next prefetch), which is more download on slow 4G |
| Residual code | Partial | A Universal Analytics tag (`gtag/js?id=UA-41818105-2` and `analytics.js` with `ec.js`) still loads. Google stopped processing UA data in 2023 and 2024. This is dead weight unless the developer knows otherwise [verify UI]. CustomerLabs script returned HTTP 403 here (blocked or removed?) [verify UI] |
| Bare script tags | Pass | No blocking `<script>` in the head besides Cloudflare email-decode (1 KB) |
| JS execution time | Fail | Long tasks total 5.8 s (home), 3.6 s (collection), 3.9 s (product) on a 4x slowed CPU. TBT est 2.6 to 4.0 s. Hydration of a large React tree is the cost (R83) |
| Unused JS and CSS | n/a | Needs Lighthouse coverage report. Not run |
| Delay snippet | Pass | Marketing scripts already start after the load event |
| Tracking intact | n/a | Not tested (read-only audit, no test purchase). Any change to script loading must go through R48 tests |
| Duplicate pixels | Partial | GA loads twice in different forms (gtag UA and analytics.js). GTM also loads gtag inside. Meta pixel once. Check inside GTM [verify UI] |
| Libraries from outside CDNs | Pass | All first-party JavaScript is self-hosted |
| Speed or caching scripts | Partial | Cloudflare Rocket Loader is on (4 KB script that rewrites how scripts load). On a Next.js app it can delay hydration or break scripts. Test with it off (R55, R26) |
| Dynamic checkout buttons | n/a | Razorpay loads at checkout only. Not seen on the product page |
| Tag manager | Partial | GTM present. Contents unknown [needs brand data: GTM container tags] |

### 5.4 Theme code, CSS and JS

| Check | Result | Evidence |
|---|---|---|
| Versioned asset URLs | Pass | Hashed file names, 1-year cache |
| Critical CSS | Pass | Styled from first paint; 2 CSS files, about 30 KB, no unstyled flash |
| Minified JS and CSS | Pass | Next production build |
| Code per page type | Partial | Shared `_app` chunk 145 KB on every page. Per-page chunks exist. Developer to check what sits in `_app` (Material UI, Apollo, Swiper, tracking wrappers) |
| Render-blocking JS before main image | Fail | The main product image and the collection grid do not exist until JavaScript runs. This is the R66 "avoid at all cost" pattern |
| Content in server HTML | **Fail** | Collection HTML: only the logo and the pixel image, no product tiles; product data is fetched after hydration. Product HTML: no `<h1>`, no price, no product `<img>`; the product data is in `__NEXT_DATA__` (58 KB) but is rendered only by the client. Home HTML: hero and category tiles are server-rendered (pass), product carousels are not |
| Late body styles | Pass | None seen |
| Pop-up on load | Pass | No pop-up fired in 25 s. Klaviyo forms load but did not show |
| API payload | Partial | 6 GraphQL calls on the product page after load. Payloads not inspected. R69: return only the fields the page needs |

### 5.5 Fonts

| Check | Result | Evidence |
|---|---|---|
| `font-display: swap` | Pass | Both families use swap |
| Variations count | Pass | 2 families x 2 weights (Lato 400 and 700, Nanum Myeongjo 400 and 700) plus a Swiper icon font that never loads |
| External font calls | Pass | Self-hosted under `/_next/static/media/` (R72 pass) |
| Subset and format | **Fail** | Nanum Myeongjo 400 = 897 KB and 700 = 956 KB as `.ttf`. That is a full Korean font shipped to render a few English headlines ("Good Things, No Waiting"). Lato is 35 KB and 34 KB, also `.ttf`. All 4 are `<link rel="preload">`, so they start before the hero image and JavaScript. Total 1,921 KB, 48% of the home page (R71, P21 step 4) |
| Font swap CLS | Pass | Next `size-adjust` fallback is present; CLS from text is near 0 |

### 5.6 Layout shift

| Check | Result | Evidence |
|---|---|---|
| CLS value | Fail on 2 of 3 | Home 0.000, collection 0.110, product 0.129 (target 0.1) |
| Shifting element | Found | Collection: grid container shift 0.025 at 13.6 s, then body shift 0.059 at 15.2 s when the "Rings (156 found)" grid replaces the spinner. Product: grid container 0.025 at 14.4 s, then body 0.08 at 16.6 s when the reviews section ("Two Decades of Expertise, Glowing Reviews") renders above the fold content and pushes it |
| Late widgets | Fail | Same as above; the spinner reserves less height than the content that replaces it (R75) |
| Cookie banner | Pass | None |
| Desktop CLS | Pass | 0.004 on home. Collection and product not measured on desktop |

### 5.7 LCP

| Check | Result | Evidence |
|---|---|---|
| LCP value | Fail | 7.9 s, 6.6 s (spinner), 18.3 s |
| LCP element known | Pass | Home: hero image. Collection: the spinner, then the grid (the tiles are each smaller than the spinner so the browser keeps the spinner as LCP; the shopper's real "content seen" moment is about 15 s). Product: main product image |
| LCP element lazy or animated | Partial | Home hero is eager with `fetchpriority=high` (pass) but sits in a Swiper slider and competes with 40 other high-priority images and 1.9 MB of fonts. Product main image is eager once it exists, but it does not exist until 17 s |
| LCP image weight | Fail on home | Hero 279 KB PNG, over 250 KB. Product main image 25 KB (pass) |
| Preload and priority | Fail | No `<link rel="preload">` for the hero; 4 font preloads instead. 41 images with `fetchpriority=high` on home (R37) |
| Image downloaded but hidden | Fail (product) | The image request cannot start until React renders the gallery (R81) |
| Waterfall bottleneck | Found | The 2 font bars span 0.6 to 19 s on home |
| TTFB | Pass | 128 to 429 ms median |

### 5.8 Interaction delay

| Check | Result | Evidence |
|---|---|---|
| INP (field) | n/a | [needs brand data: Search Console or a RUM tool] |
| TBT (lab) | Fail | 2.6 to 4.0 s est with 4x CPU slowdown; 25 long tasks on home, longest 876 ms; 1.3 s single task on collection |
| Add to cart, filters, cart completion | n/a | Not tapped (read-only). Expect lag while hydration runs; test on a mid-range Android on mobile data (P2 step 6) [verify UI] |

### 5.9 Caching and CDN

| Check | Result | Evidence |
|---|---|---|
| Caching on | Pass | HTML: `x-nextjs-cache: HIT`, `cf-cache-status: HIT`, CloudFront hit on home. Collection and product HTML: `cache-control: private, max-age=1800, must-revalidate`, CloudFront "Miss" but Cloudflare "HIT" with `age` 3,400 s. So Cloudflare caches pages the app marks private. Developer to confirm this is intended and that nothing visitor-specific is in that HTML (R86) [verify UI] |
| Compression | Pass | brotli on HTML, JS, fonts |
| Cart, checkout, account not cached | Partial | `/cart` is not a page (307 to `/404?pageType=product&slug=cart`, `cf-cache-status: BYPASS`). Checkout not tested (read-only). [verify UI] |
| Static asset TTL | Pass | 1 year, immutable, hashed names |
| Resized images TTL | Fail | `/_next/image` responses: `cache-control: max-age=1800, stale-while-revalidate`, CloudFront "Miss" on the hero and on product images. 30 minutes is short for images whose URL already encodes the file and width; each CloudFront miss means the origin resizes again (R87) |
| CDN hit rate | n/a | [needs brand data: Cloudflare and CloudFront dashboards] |
| Cache key and UTM | n/a | Not testable from here |
| Session cookie on first hit | Pass | No `set-cookie` on the HTML response |

### 5.10 Hosting and server

| Check | Result | Evidence |
|---|---|---|
| TTFB per template | Pass | All under 800 ms at the median. Product run 1 was 1,262 ms and desktop home 1,054 ms, both single readings, likely a CloudFront miss |
| PHP, Redis, database | n/a | Not a PHP store. Origin stack unknown [needs brand data: hosting provider, Node runtime, where the GraphQL API runs] |
| Protocol | Partial | `curl` saw HTTP/2 and an `alt-svc: h3` header (HTTP/3 offered). The browser test went through a proxy, so protocol could not be confirmed in the browser |
| Peak capacity | n/a | [needs brand data] |

### 5.11 Video and embeds

Pass. No video tags, no YouTube iframes, no autoplay on the 3 pages. 1 empty-src iframe (GTM) only.

### 5.12 Redirects and links

| Check | Result | Evidence |
|---|---|---|
| Redirect types | Fail | Unknown URLs get a `307` (temporary) redirect to `/404?pageType=product&slug=...`. A missing page should answer `404` directly, not a temporary redirect to a page that likely returns 200 (R97, "soft 404"). This also hits the origin (`cf-cache-status: BYPASS`) |
| Chains | Pass | None seen on the tested URLs |
| http to https | n/a | Not testable from this network |
| Broken asset links | Partial | CustomerLabs script 403. Everything else 200 |
| 404 page | Partial | Custom 404 route exists; whether it links to top categories not checked [verify UI] |

### 5.13 Peak readiness

n/a. [needs brand data: sale calendar, capacity plan]. Note for later: the product page makes 6 API calls after load; under sale traffic the API is the step that will slow first (R94).

### 5.14 Home page

Hero: eager, high priority, but PNG 279 KB, in a slider, behind fonts, LCP 7.9 s (Fail). Section images: category icons 5x oversized PNG (Fail). Widgets at load: none before load (Pass). Announcement bar: none. Below-fold sections: 40 carousel tiles marked high priority (Fail). Traffic weight: [needs brand data: sessions by template].

### 5.15 Collection page

First card eager, rest lazy: the first 16 tiles carry `fetchpriority=high` (Partial). Thumbnails: 167 px boxes get 175 px AVIF files, right size (Pass). Quick View: none (Pass). Filters respond: not tested. Mixed aspect ratios: 1 ratio (Pass). Critical CSS: styled (Pass). Grid rendered client-side after load (Fail, R66).

### 5.16 Product page

Main image: not in server HTML, appears at 17 to 18 s (Fail, R81). Gallery thumbnails: 5 thumbnails marked high priority, 23 px files (fine). BNPL or payment widgets: none seen. Reviews and related products: render after the main image (Pass on order) but the reviews section shifts the layout (Fail, CLS 0.08). Add to cart response: not tested. Variant images: not tested. Video: none. Tracking events: not tested [verify UI].

### 5.17 and 5.18 Cart and checkout

Not measured. Cart is a drawer or a client route, not `/cart`. Checkout uses Razorpay. Read-only audit, no items added. [verify UI: run P1 on the cart drawer and the checkout on a phone after the fixes]

### 5.19 Mobile vs desktop

Both tested on home. Gap: LCP 7.9 s mobile slow 4G vs 5.3 s desktop fast line. Desktop CLS 0.004. Desktop-only styles: not inspected. Real device: not available [verify UI: repeat on a mid-range Android on mobile data].

## 5. Problems found, ranked (R2, R23, 7.4)

Ranked by how much of the measured time and weight each one explains, then by how easy it is. Owner column says who does it. Each item has an acceptance test so the developer can prove it (P30, R102).

### Problem 1. Two 900 KB font files are preloaded on every page

- Evidence: `/_next/static/media/ae1a48c074c123e8-s.p.ttf` 956 KB and `/_next/static/media/14a3fceaeabbcb56-s.p.ttf` 897 KB (Nanum Myeongjo 400 and 700, `font/ttf`). Both `<link rel="preload" as="font">` in the head via `next/font`. On slow 4G they download from 0.6 s to 19.2 s (home), 0.3 s to 13.3 s (collection), to 15 s (product). Fonts are 48% of home page bytes. The desktop run shows the same 2 files taking 1.07 to 1.55 s even on a fast line.
- Why it matters: preloaded fonts jump the queue. The hero image, the JavaScript and therefore the whole product render wait behind them. This one change moves LCP on every template.
- Rules: R71 (load only what a page needs, subset), R72 (self-host as WOFF2), R37 (preload only the LCP image and critical fonts, never many assets), R28 and R4 (weight first).
- Fix (developer, custom-code adaptation of P21): in the `next/font/google` or `next/font/local` config for Nanum Myeongjo, set `subsets: ['latin']` (and `latin-ext` only if needed) so Next builds a small WOFF2 subset. If the font is loaded from a local `.ttf`, replace it with a Latin-subset WOFF2 (Google's own subset files are about 20 to 40 KB per weight). Check whether weight 700 is used anywhere; if not, drop it. Do the same subset check for Lato. Keep `display: 'swap'`. If Nanum Myeongjo is only used for the hero headline, consider whether the headline could be baked into the hero image or use Lato; that removes the family entirely.
- Target: fonts under 150 KB in total, `.woff2`, at most 3 files.
- Acceptance test: Network panel shows no `.ttf`; total font bytes under 150 KB; hero LCP on the slow 4G test drops by several seconds; text still renders in the serif face on the hero.
- Rollback: revert the font config.

### Problem 2. Product and collection content is rendered only by JavaScript in the browser (R66, R81)

- Evidence: collection HTML has no product tiles (only the logo and the pixel image in the HTML, 84 KB, and `initialApolloState` holds filters only). Product HTML has no `<h1>`, no price, no product image tag; `__NEXT_DATA__` carries 58 KB of product data that the client renders. The product image request starts at 17.1 s, after the load event (14.3 s) and after 6 GraphQL calls (17.3 to 19.1 s). LCP 18.3 s. On collection the grid appears at about 15 s after a 14 s spinner.
- Why it matters: this sets the floor. Even with fonts fixed, the shopper waits for all JavaScript to download and run before seeing a product. Ad clicks land on product pages (R3). Google also sees an empty shell first.
- Rules: R66 (server-side or hybrid rendering beats client rendering; render-blocking JS before the main image is the pattern to avoid), R81 (script hiding the image), R53 (product image and information before integrations), R100 (developer task).
- Fix (developer, the big one): render the product's first image, name, price and Add to Cart in the server HTML (`getServerSideProps` or `getStaticProps` with ISR, using the data that is already in `initialApolloState`), so the `<img>` for the main image is in the HTML with `fetchpriority="high"` and a `<link rel="preload" as="image">` in the head (P18 step 7). Do the same for the first page of collection tiles: server-render the first 8 to 12 products with their AVIF tiles, then let Tagalys or GraphQL take over for filters and paging. The data is already fetched server-side for the product page (it is in the page JSON), so this is a rendering change, not a new data path. Keep the reviews, related products and carousels client-rendered and below the fold.
- Target: main product image visible before JavaScript runs; LCP under 2.5 s on the slow 4G test once fonts are fixed; collection first tiles in HTML.
- Acceptance test: `curl` the product URL and find the main image `<img>` and the price in the HTML; slow 4G test shows the image within 3 s; LCP element is the product image, not the spinner.
- Rollback: feature flag the server render per template.

### Problem 3. Forty below-fold images marked `fetchpriority="high"` on the home page

- Evidence: 41 `img` tags with `fetchpriority="high"`, 1 in view (the hero). The other 40 are product carousel tiles at 1,052 px and 1,931 px from the top. The collection page marks its first 16 tiles high, the product page its 5 thumbnails.
- Why it matters: high priority is meant to single out the LCP image. When 40 images share it, the hero loses the head start (R37: "too many preloads recreate the contention they were meant to fix").
- Rules: R37, R35 (lazy below the fold), R80 (LCP fix order: preload it, then cut what is ahead of it).
- Fix (developer): in the product tile component, only pass `priority` (which sets `fetchpriority=high` and removes lazy loading in `next/image`) for tiles that are above the fold on first paint: none on the home page carousels, the first 4 to 6 on a collection page. Everything else default (lazy). Same for the WhatsApp button and slides 2 and 3.
- Acceptance test: home page has exactly 1 `fetchpriority="high"` image (the hero); Network panel shows carousel tiles loading only on scroll.

### Problem 4. Home hero is a 279 KB PNG served without conversion; category icons are 5x oversized PNGs

- Evidence: `/_next/image?url=/static/images/banner/new-arrivals-mobile.png&w=1200&q=75` returns `image/png`, 284,910 bytes, 650 x 1000 px. The desktop hero of the same section returns AVIF at 78 KB. Category circles: `pendants.png` 234 KB, `nosepins.png` 203 KB, `earrings.png` 165 KB, `bracelets.png` 123 KB, each 320 x 320 natural for a 60 x 60 box. That is about 740 KB of icons above the fold, plus 7 lazy flags on in-view images.
- Why it matters: the hero is the LCP element and is over the 250 KB cap. The icons share bandwidth with it during the first 8 s.
- Rules: R31 (LCP image under 250 KB, hero under 200 KB), R30 (serve near display size, flag over 2x), R32 (JPEG for photos, let the resizer serve AVIF or WebP), R35 and R36 (in-view images eager), 5.14.
- Fix (developer, P14 and P16 adaptation): export the mobile hero as a JPEG at 2x the box width (about 800 px wide, quality 75 to 80) so the resizer converts it to AVIF like the desktop one; confirm why the PNG passed through (likely because the file is narrower than the `w=1200` slot; a `sizes` attribute of `100vw` on a 393 px screen at 2.75x asks for 1080 px) [verify UI]. Replace the category icons with 160 px AVIF or WebP files (2x the 60 px box, R30) and set `loading="eager"` on the 7 icons since they are in view. Add `<link rel="preload" as="image" imagesrcset=... fetchpriority="high">` for the hero (P18 step 7).
- Target: hero under 100 KB as AVIF, icons under 10 KB each.
- Acceptance test: `content-type: image/avif` on the hero; total above-fold image bytes on home under 250 KB.

### Problem 5. Layout shift on collection and product pages

- Evidence: collection CLS 0.110 (0.025 grid container at 13.6 s, 0.059 body at 15.2 s when the grid replaces the spinner). Product CLS 0.129 (0.025 at 14.4 s, 0.080 at 16.6 s when the reviews block renders and pushes content). Same values on all 3 runs, so it is structural, not random.
- Rules: R74 (a reported CLS is real), R75 (reserve space for anything that arrives late), P19 step 6 (late widgets), P20 step 2.
- Where it is: on the product page the "Two Decades of Expertise, Glowing Reviews, 4.8/5, 514 Google Reviews" band sits above the product gallery (see `raw-b/product-emerald-ring-mobile-slow4g-run2.png`). It renders late, so it pushes the gallery, price and Add to Cart down by its own height.
- Fix (developer): give the grid area and the product buy box a fixed minimum height while loading (skeleton tiles with the same aspect ratio as a product card, `min-height` on the reviews container equal to its rendered height on mobile, measured at 393 px). Problem 2 removes most of this on its own because the content is in the HTML from the start.
- Acceptance test: CLS under 0.05 on both templates in the slow 4G test; no body-level shift after 10 s.

### Problem 6. Too much JavaScript runs on the main thread

- Evidence: 25 long tasks on home (max 876 ms, 5.8 s in total on a 4x slowed CPU), 14 on collection (one 1.3 s task), 18 on product. First-party JS 480 to 600 KB, `_app` chunk 145 KB. 3,128 DOM nodes on home (152 `img` tags, most in carousels). TBT est 2.6 to 4.0 s.
- Rules: R83 (long tasks, TBT), R84 (INP maps to add to cart and filters), R62 (split code by page type, after images and scripts), R58 (worker for third parties is a rebuild-level task).
- Fix (developer, after 1 to 5): audit the `_app` bundle with `@next/bundle-analyzer`; move Swiper, Klaviyo and tracking wrappers out of `_app` into the pages that use them; lazy-import the carousels below the fold (`next/dynamic`) so the home page hydrates 3 sections instead of 152 tiles; render fewer tiles per carousel on mobile; check that Material UI is tree-shaken. Re-measure long tasks after each step (R26, one change at a time).
- Target: no long task over 200 ms; TBT est under 1 s on the slow test.

### Problem 7. Resized images and page HTML cache for only 30 minutes at the CDN

- Evidence: `/_next/image` responses `cache-control: max-age=1800, stale-while-revalidate`, `x-cache: Miss from cloudfront` on the hero and on product tiles. Collection and product HTML `cache-control: private, max-age=1800, must-revalidate`, CloudFront miss, Cloudflare HIT with `age` 3,400 s.
- Why it matters: every miss makes the origin resize the image again and adds latency for the next shopper. The private HTML being cached at Cloudflare is either a deliberate rule or a leak to check.
- Rules: R87 (static assets long TTL when versioned; HTML brief), R85 (verify from headers), R86 (never cache visitor-specific pages).
- Fix (developer and whoever owns Cloudflare, P26 adaptation): set `images.minimumCacheTTL` in `next.config.js` to at least 1 day (image URLs already include the width and quality, and product image ids change when the photo changes); confirm CloudFront caches `/_next/image` on the full query string. For product and collection HTML decide one rule: either `public, s-maxage=600, stale-while-revalidate` from the app (prices and stock update through the API anyway) or keep private and stop Cloudflare from caching it. Then load a product page in a fresh incognito window and read the headers (P26 step 1).
- Acceptance test: second request for the same product image is a CloudFront hit; HTML caching rule documented.

### Problem 8. Small clean-ups

- Universal Analytics tag still loads (`gtag/js?id=UA-41818105-2`, `analytics.js`, `ec.js`). Google stopped processing Universal Analytics data. Remove after confirming GA4 is set up in GTM (R44, residual tracking; R48 tests first) [verify UI].
- CustomerLabs script returns 403 from here. Either it is blocked for this network or the account lapsed. Check and remove if dead (R44) [verify UI].
- Cloudflare Rocket Loader is on. On a Next.js app it can delay hydration. Turn it off for 1 day and compare 3 runs (R55, R26).
- Unknown URLs answer `307` to `/404?...`. Return a real `404` status with the same page (R97). Also confirm `/cart` is meant to 307 to the 404 page; a shopper who types it gets a "not found" page instead of the cart.
- `loading.gif` spinner is a 27 KB GIF on every collection and product page. Replace with a CSS spinner or a skeleton (R96: never GIF).
- Swiper icon font is declared but never loads (`unloaded`). Harmless; remove the declaration.
- Next prefetches the product page chunk from collection pages and the collection chunk from product pages. On slow 4G this is more download before the page is usable. Set `prefetch={false}` on links inside carousels and grids; keep it for the main nav.

### Order of work (7.4 adaptation for a custom app)

1. Fonts (Problem 1). 1 developer day. Biggest weight cut, every template.
2. Hero and icon images, `fetchpriority` clean-up, hero preload (Problems 3 and 4). 1 day. Home LCP.
3. Reserve space for late content (Problem 5). Half a day. CLS.
4. Server-render product buy box and first collection tiles (Problem 2). 3 to 10 developer days depending on the codebase. This is the fix that gets product pages near 2.5 s.
5. JavaScript diet (Problem 6). Ongoing.
6. Cache rules and clean-ups (Problems 7 and 8). Half a day plus a Cloudflare setting.

Measure after each step with the same 3-run slow 4G test (P1 step 9), and run PSI mobile and desktop as soon as the quota resets so there is a Google baseline before the first change lands.

### Performance budget proposal (P29, R8; chosen values, not sourced)

Per template on mobile: page weight under 1.5 MB on first visit, fonts under 150 KB, at most 1 `fetchpriority="high"` image, LCP under 2.5 s on the slow 4G lab test, CLS under 0.05, no long task over 200 ms, third-party hosts at most 10, no `.ttf` or `.gif` files. Re-test monthly, after every deploy that touches `_app`, fonts or the product page, and 2 weeks before Diwali or any sale.

## 6. Business case (P6, R9)

### 6.1 Private brand data (from the repo's Metabase export, not from public web)

Source: `data/meta-gallery/sales.json`, pulled 24 Sep 2026 from Metabase dashboard 6 (Online Website Sales Analytics, website orders only) and its traffic card. This is Gehna's own data. Keep this section out of anything public.

- Live Metabase today: the MCP connector can only read the 2 staging Postgres databases. The BigQuery (Google Analytics) questions "Usage by Device Category", "Number of Users by Device", "E-Commerce Conversion Rates", "Bounce Rate by Traffic Source" and "Landing Page Performances" exist (ids 361, 364, 368, 356, 353) but all take parameters, and reading or running them returned "no permission". The staging database has 12 and 34 orders for June and July 2026, so it is not production data and I did not use it. Device split, bounce rate, conversion by device and top landing pages are therefore [needs brand data]. The owner can export those 5 questions from Metabase in a minute.
- What the repo export gives, last 30 days (25 Aug to 23 Sep 2026), arithmetic done in code:
  - Website sales: ₹96,83,409 (9,683,409). Orders: 285. AOV: ₹33,977. About 9.5 orders and ₹3.23 lakh a day.
  - Traffic card: 6,34,288 "visits" (21,143 a day), 12,053 add-to-carts, 173 orders as counted by Google Analytics (GA undercounts against Metabase's 285).
  - Conversion rate: 285 orders / 634,288 visits = 0.045%. Add-to-cart rate 1.9%. The "visits" definition (sessions, users or page views) is not documented in the export and changes this rate a lot [needs brand data: confirm the metric behind the traffic card].
  - Longer view, 1 Aug to 23 Sep (54 days): ₹1.44 crore, 446 orders, AOV ₹32,243. Monthly: June ₹62.1 lakh (184 orders), July ₹72.1 lakh (240), August ₹87.5 lakh (307).

### 6.2 The model

Today: 21,143 visits a day x 0.045% x ₹33,977 = about ₹3.23 lakh a day, ₹11.78 crore a year (the last 30 days annualised, no seasonality).

Assumed conversion lift from taking product-page LCP from 18 s to under 3 s on mobile. The playbook's sources give a range and none of them is Gehna's own result:

| Assumed lift in conversion rate | Extra sales per 30 days | Extra sales per year | Where the figure comes from |
|---|---|---|---|
| +3% | ₹2.9 lakh | ₹35.3 lakh | Conservative, below every source |
| +5.6% | ₹5.4 lakh | ₹66.0 lakh | Source 06, "+5.6% per second faster", uncited |
| +7% | ₹6.8 lakh | ₹82.5 lakh | Source 04 via Cloudflare, "about 7% per 1 s delay" |
| +10% | ₹9.7 lakh | ₹1.18 crore | Mid-range for a multi-second gain; assumption |

These are assumptions, not forecasts. The site is losing more than 1 s, so the per-second figures are a floor for direction only. Do not quote any of them as Gehna's own result. The only number that will count is Gehna's own before and after: same pages, same 3-run test, then conversion by device for the 28 days after each release (R102, P30).

Direction benchmarks, third-party, stated as such: Portent's study (source 03) found a site loading in 1 s converting about 2.5x a site loading in 5 s. Google's mobile figure (sources 04, 06, 09) is that 53% of mobile visitors leave a page that takes over 3 s. Gehna's product page takes 17 s to show anything to buy on slow 4G.

Ad-spend angle (P6 step 4): every paid click that lands on a product page and leaves before 17 s is a click paid for and never shown the product. With 12,053 add-to-carts a month but only 285 orders, the site already has a cart-to-order gap; speed at cart and checkout is part of that and was not measured here (5.17, 5.18).

## 7. What I could not verify

Playbook items marked for the owner, the developer or a later run.

[needs brand data]
- Mobile share of sessions and revenue; conversion rate by device; bounce rate; top landing pages; sessions by template (R3, R10, section 2). Metabase questions 361, 364, 368, 356, 353 hold this but are parameterised and not readable by the connector.
- Definition of "visits" in the Metabase traffic card (sessions, users or page views).
- Paid vs organic share and the exact pages ads land on (R3, R5). The Meta gallery data could answer the landing-page part; not read here (out of scope).
- Revenue role of each third-party script: GTM contents, Klaviyo, Clarity, CustomerLabs, Google Sign-In (R7, P7).
- Pixel and consent setup, and which events must keep firing (R48).
- Hosting provider and origin stack (where Next.js and the GraphQL API run), CDN hit rates from the Cloudflare and CloudFront dashboards (R90, P28).
- Search Console Core Web Vitals report for field LCP, INP and CLS (R17, R27).
- Sale calendar and capacity plan (R94).
- Margin, for a profit version of section 6.

[verify UI] (developer or owner checks in the real system)
- Why the mobile hero PNG passes through `/_next/image` unconverted while the desktop one becomes AVIF.
- Whether the Universal Analytics tag and the CustomerLabs script are still wanted.
- Whether Cloudflare caching `private` product HTML is intended, and the CloudFront behaviour for `/_next/image` query strings.
- Cart drawer, add to cart, variant switch and Razorpay checkout speed on a mid-range Android on mobile data (P2 step 6, R25, R98, R99). Not touched in this read-only audit.
- Whether `/cart` should answer 307 to the 404 page.
- Tracking events fire once after any script change (R48, R103).
- Rocket Loader on vs off, 3 runs each.

[web check] (blocked from this network today)
- Current Core Web Vitals thresholds at web.dev, `fetchpriority` and preload support, Next.js `images.minimumCacheTTL` and `next/font` subset docs. The developer should confirm the exact config names against the Next.js version in the repo before changing them.

Not run: PageSpeed Insights (quota), GTmetrix or WebPageTest cross-check (P1 step 10), Unlighthouse site-wide crawl (P5, needs owner go-ahead and staging), Lighthouse coverage report for unused JS and CSS.

Fetch count against the site today: 20 page or asset fetches (8 `curl`, 12 browser loads, of which 2 failed on a certificate before reaching the site).
