# Gehna website speed audit (mobile)

Site: https://www.gehnaindia.com/
Date of test: 24 September 2026
Pages tested: homepage, the Rings collection (/m/rings), and one product page (/bold-emerald-18k-gold-ring)
Raw measurement files: `reviews/speed-test/raw-a/` (one JSON and one screenshot per test run, plus `summary.json` with the medians and `audit_script.py`, the script that ran the tests)

## 1. Verdict

On a slow 4G phone connection the Gehna site is slow to become usable, and the cause is clear. The homepage downloads 6.5 MB, which is about 3 to 4 times what a fast shop page should weigh. Almost 2 MB of that is 2 font files (a Korean serif font shipped with its full Korean character set, in an old file format), 1.6 MB is PNG banner and icon images that should be modern compressed images, and 1 MB is tracking scripts. Because the phone spends the first 20 seconds downloading fonts and images, the site's own JavaScript, which draws the product grid and the product page, does not finish running until 16 to 23 seconds in. On the collection and product pages the shopper sees a spinner until then. A Cloudflare setting called Rocket Loader makes this worse by holding the site's code until everything else has loaded. The hero banner on the homepage, the largest thing on screen, took a median 7.9 seconds to appear, against Google's target of 2.5 seconds. Layout is stable on the homepage but shifts on collection and product pages (0.12 to 0.14, above the 0.1 limit) because a bar is inserted at the top after the page has drawn. The good news: the server itself is fast (first byte in about 0.2 seconds when cached), the HTML is small, and every problem found is fixable by a developer without changing the design. The first 4 fixes below are small jobs and should remove roughly 3 MB and 10 or more seconds from a slow 4G load.

## 2. What was measured, how, and the numbers

How the test was run:

- A real headless Chromium browser (Playwright build 1194) driven by a script, on a phone-sized screen (412 by 823 pixels, 1.75 pixel density), with a Chrome on Android user agent and an India locale.
- Network throttled to the same profile Google's PageSpeed and Lighthouse use for mobile: 1.6 Mbps down, 750 Kbps up, 150 ms round trip, and the CPU slowed 4 times (source: Lighthouse throttling docs, https://github.com/GoogleChrome/lighthouse/blob/main/docs/throttling.md). At 1.6 Mbps the line moves about 200 KB per second, so every 1 MB costs about 5 seconds.
- Browser cache off, so every run is a first visit. Each page was loaded 3 times. The table shows the median (middle) run.
- The browser recorded: time to first byte, first paint, largest contentful paint (LCP, when the biggest thing on screen appears), layout shift (CLS, how much things jump), long tasks (JavaScript blocking the phone for over 50 ms), every request with its size, headers and timing, image natural size versus displayed size, fonts, and the DOM (page structure) size.
- Separate unthrottled checks with curl measured headers, redirects and server time.
- Google's PageSpeed Insights API was not available today, so there is no Lighthouse score and no real-user (CrUX) data in this report. All numbers below are from these lab runs.

Median of 3 throttled mobile runs:

| Measure | Homepage | Rings collection | Product page | Google target |
|---|---|---|---|---|
| Time to first byte | 0.23 s | 0.21 s | 0.18 s (1.27 s on the first, uncached load) | under 0.8 s |
| First paint of anything | 1.0 s | 0.8 s | 0.75 s | |
| LCP (largest thing on screen) | 7.9 s (hero banner) | 6.6 s (a loading spinner) | 1.8 s (a loading spinner; the product photo request only started at 16.3 s and finished at 17.9 s) | under 2.5 s |
| Layout shift (CLS) | 0.00 | 0.12 | 0.14 | under 0.1 |
| Page fully loaded (load event) | 21.2 s | 13.5 s | 14.1 s | |
| Site's own data calls start (page usable) | 22.7 s | about 15 s | 16.5 s | |
| Requests | 193 | 127 | 127 | |
| Total download | 6.52 MB | 3.10 MB | 3.50 MB | under 2 MB is good practice |
| Third-party download | 1.05 MB in 31 requests | 0.20 MB | 0.34 MB | |
| Long tasks (JavaScript blocking) | 62 tasks, 8.7 s total, worst 0.87 s | 9 tasks, 2.5 s total | 10 tasks, 2.5 s total | |
| Total blocking time | 5.2 s | 2.0 s | 2.0 s | under 0.2 s |
| Page structure (DOM nodes) | 3,134 | 1,294 | 1,131 | under 1,500 |

Homepage download by type (run 1 of the 3, the other 2 are within 3 KB):

| Type | Requests | Size |
|---|---|---|
| Images | 80 | 2.60 MB |
| Fonts | 4 | 1.98 MB |
| Scripts | 66 | 1.78 MB |
| HTML | 2 | 39 KB |
| CSS | 4 | 19 KB |
| Data and other | 41 | 0.10 MB |

Unthrottled checks (curl from the test machine, US East):

- https://www.gehnaindia.com/ answered in 0.53 s, HTTP 200, HTML 35 KB compressed (208 KB raw), served from cache (Cloudflare HIT, CloudFront HIT, age 2,875 s).
- https://gehnaindia.com/ (no www) redirects with a 301 to www in 0.41 s. That is 1 extra round trip for anyone who types the bare domain.
- The 2 large font files are 3.6 to 4 MB raw and 0.92 MB and 0.98 MB after Brotli compression. They are cached for 1 year (good) but the size is the problem.
- The hero banner PNG is 285 KB and comes back as PNG even when the browser says it accepts AVIF and WebP.

## 3. How the site is built and how it renders

Evidence-based, not assumed:

- Framework: a custom Next.js (React) app using the Pages Router. Proof: `/_next/static/chunks/pages/index-*.js`, `/_next/static/chunks/pages/_app-*.js`, a `__NEXT_DATA__` block (45 to 56 KB per page), the `x-nextjs-cache: HIT` header, and `/_next/image` for all pictures.
- UI kit: Material UI with Emotion styling (classes such as `MuiGrid-root`, `jss170`, 53 inline `data-emotion` style tags totalling 79 KB in the HTML). Carousels use Swiper.
- Data: the page talks to a GraphQL API at api.gehnaindia.com (Apollo client, `initialApolloState` in the page data). Search and collection listings use Tagalys (api-r1.tagalys.com in the security policy, and a Tagalys sitemap). Payments are Razorpay.
- Hosting and delivery: the Next.js server sits behind Amazon CloudFront (`x-amz-cf-pop`, `via: cloudfront`), and Cloudflare sits in front of CloudFront (`server: cloudflare`, `cf-cache-status`, `cf-ray`). So there are 2 CDNs in a row. Cloudflare features switched on: Rocket Loader, Email Address Obfuscation, a bot challenge script, and the Web Analytics beacon.
- Images: product photos come from cdn-assets.gehnaindia.com through the Next.js image optimiser, and arrive as AVIF (modern, small). Static banners and category icons are PNG files in the site's `/static/images/` folder and arrive as PNG.
- Fonts: 4 self-hosted TTF files via next/font: Lato 400 and 700 (38 KB each) and Nanum Myeongjo 400 and 700 (922 KB and 982 KB). Nanum Myeongjo is a Korean serif; the site uses it for headings and product names. The full Korean glyph set is shipped even though the site shows only Latin letters.
- Tags: Google Tag Manager (GTM-PK4C6HK), which loads 3 separate Google gtag scripts (GA4 G-FT109JXEC7, Google Ads AW-982480202, and the old Universal Analytics UA-41818105-2), the Meta pixel, Klaviyo, Microsoft Clarity, CustomerLabs, and the Google Sign-In library (accounts.google.com/gsi/client, 102 KB) on every page.

How a page renders, step by step, on slow 4G (homepage, from the median run):

1. 0.0 to 0.23 s: HTML arrives from cache. Good.
2. 0.4 s: the browser starts downloading the hero banner (marked high priority, which is right), the 4 fonts (all preloaded), CSS, and 31 JavaScript chunks. But it also starts about 40 product thumbnails that the code marked `fetchpriority="high"` even though they sit 1,000 to 1,900 pixels below the fold. All of these share one 1.6 Mbps line.
3. 1.0 s: first paint (the header and text in fallback fonts).
4. 7.9 s: the hero banner finishes and becomes the LCP. It is 288 KB, so alone it would take 1.5 s on this line. It took 7.5 s because the fonts and thumbnails were competing.
5. 21.1 s: the 2 big fonts finish. 21.2 s: the load event fires.
6. 22.4 to 22.7 s: only now do the site's own JavaScript bundles run to completion, the React app "hydrates" (takes over the page), 7 GraphQL data calls fire, and the tag manager, Meta pixel, Klaviyo and Clarity load. Between 22 and 40 s the phone's main thread is busy for 8.7 s in 62 long tasks, so taps are sluggish.

Why the JavaScript runs so late: Cloudflare's Rocket Loader is on. It rewrites all 31 Next.js script tags in the HTML (they carry `type="…-text/javascript"` so the browser ignores them) and then fetches and runs them itself later. In the recorded runs 28 to 36 of the Next.js chunk requests were started by `rocket-loader.min.js`, not by the browser's normal loader. Rocket Loader is designed for simple sites and is a known source of trouble with React and Next.js apps (Cloudflare's own advice is to switch it off if you see JavaScript issues: https://developers.cloudflare.com/speed/optimization/content/rocket-loader/ and https://community.cloudflare.com/t/nextjs-and-rocket-loader/665577).

Collection and product pages render differently and worse. The server sends a shell: header, a progress bar and a spinner GIF (30 KB). The products, prices and the main photo are fetched by JavaScript after hydration. On slow 4G that is 15 to 17 s in. The browser records the spinner as the "largest content", which is why the LCP numbers for those pages look better than the experience is. On the product page the main photo request started at 16.3 s.

Where the time goes, in short: bandwidth. 6.5 MB at 200 KB per second is 32 s of pure transfer. Fonts (30 percent), PNG images (25 percent) and third-party scripts (16 percent) are the bulk, and none of them are needed to show a jewellery photo and a price.

## 4. Problems found, with evidence

### P1. 1.98 MB of fonts, 1.9 MB of it a Korean font shipped in full (critical)

- Files: `/_next/static/media/14a3fceaeabbcb56-s.p.ttf` (922 KB compressed) and `/_next/static/media/ae1a48c074c123e8-s.p.ttf` (982 KB compressed). Both are Nanum Myeongjo, weights 400 and 700, in TTF format (from the `@font-face` rules in `/_next/static/css/f45806cc85ed262f.css`).
- They are preloaded in the HTML `<head>`, so they compete with the hero image from the first moment.
- On the throttled line they finished at 21.1 s (home), 13.4 s (collection) and 14.0 s (product), and the load event fired within 0.1 to 0.7 s after them on every page. In other words the fonts alone set the "page loaded" time.
- The same font from Google Fonts, Latin characters only, in WOFF2 format, is 12.9 KB (400) and 12.8 KB (700). Measured today by fetching the Google Fonts CSS with a Chrome user agent and downloading the Latin file. Lato Latin WOFF2 is 14.0 KB and 14.2 KB, against 38 KB each as TTF now.
- `font-display: swap` is set, so text is readable early in Arial. Good. But the 2 MB still blocks everything else.

### P2. Cloudflare Rocket Loader delays the site's own code (critical)

- All 31 Next.js `<script>` tags in the HTML are rewritten to `type="e417ba1084750121c0fe6b0c-text/javascript"` and a `rocket-loader.min.js` script is injected with `data-cf-settings`. Counted in the raw HTML.
- In every run, most Next.js chunk requests were initiated by `rocket-loader.min.js` (28 of 42 on home, 31 of 32 on collection, 36 of 37 on product).
- The first GraphQL data call, which only happens after the React app has hydrated, came at 22.7 s on home and 16.5 s on the product page, both after the load event.
- A second Cloudflare feature, Email Address Obfuscation, is also active on the same pages (`email-decode.min.js` and `/cdn-cgi/l/email-protection` links in the footer). That feature rewrites page text with JavaScript, which can make React's server HTML and client HTML disagree (a hydration mismatch that forces a re-render). Reported by others with Cloudflare and React: https://medium.com/@Shivam010/cloudflare-pages-and-react-hydration-problems-only-on-custom-domain-957f5598ebe8

### P3. Hero banner and category icons are PNG, and the CDN may be locking in the PNG (high)

- Hero banner `/_next/image?url=/static/images/banner/new-arrivals-mobile.png&w=750&q=75`: 288 KB, `content-type: image/png`. This is the LCP element on the homepage. Two other banners in the same carousel: 326 KB and 216 KB, also PNG, and they download on first load even though only 1 is visible.
- With an `Accept: image/avif,image/webp` header the same URL still returned `image/png` with `cf-cache-status: HIT` and `age: 1502`, even though the response carries `vary: Accept`. Cloudflare only honours Vary on images on Pro, Business and Enterprise plans and only when a "Vary for Images" rule is set up (https://developers.cloudflare.com/cache/advanced-configuration/vary-for-images/, and the Next.js discussion https://github.com/vercel/next.js/discussions/39510). The likely story: one early request without AVIF support (a bot or old browser) got a PNG, Cloudflare cached it, and now everyone gets the PNG. Product photos, which were cache MISSes at Cloudflare, arrived as AVIF and were 11 to 33 KB each at 640 to 750 px wide. That is the size a banner should be.
- Category icons: 7 PNGs at 640 px wide (natural 320 by 320) shown in 60 by 60 px circles: pendants 243 KB, nosepins 211 KB, earrings 172 KB, bracelets 129 KB, rings 42 KB, chains 30 KB, best sellers under 26 KB. About 0.85 MB for 7 tiny icons. Cause: the `<Image>` has no `sizes` prop, so Next.js picks a width for a full-screen image, and again the files are PNG.

### P4. 40 below-the-fold thumbnails marked high priority (high)

- On the homepage, 40 product thumbnails in the product carousels carry `fetchpriority="high"` and no `loading="lazy"`, while sitting 1,024 to 1,903 px below the top of the screen. On the product page, 5 thumbnail strip images are marked high too. This is what the Next.js `priority` prop produces, and it should be reserved for the one LCP image (https://nextjs.org/docs/pages/api-reference/components/image).
- Effect: the hero banner (288 KB) took 7.5 s to download on a line that could deliver it in 1.5 s.

### P5. Collection and product pages are empty shells until JavaScript runs (high)

- Collection HTML contained 1 image (the logo) and a spinner. 60 product images appeared only after hydration. The largest element recorded by the browser was the `loading.gif` spinner (6.6 s median LCP).
- Product HTML: the price and title are in the HTML, but the main photo request started at 16.3 s (median) and the browser again recorded the spinner as the largest element. The 5 video thumbnails also start downloading MP4 data (HTTP 206 range requests) as soon as the page hydrates.
- Product HTML is sent with `cache-control: private, max-age=1800, must-revalidate`, so neither CDN caches it. The first, uncached product load had a 1.27 s time to first byte versus 0.15 to 0.18 s for the cached runs. Ads send shoppers to product pages that may not be cached.

### P6. Layout shifts on collection and product pages (medium)

- Collection CLS 0.12 in all 3 runs, product CLS 0.14. The single biggest shift on both is the whole `<body>` moving down by 50 px (collection) or 68 px (product) at 15 to 17 s, when JavaScript inserts a bar above the header. The header's right-hand icons also move 18 px left (0.03) when the search icon appears, and the indeterminate progress bar under the header adds many tiny shifts.
- Homepage CLS is 0.00. Good.

### P7. 1.05 MB of third-party scripts, including a dead one (medium)

- Google Tag Manager loads 3 separate gtag scripts: GA4 (192 KB), Google Ads (182 KB) and Universal Analytics UA-41818105-2 (136 KB). Universal Analytics stopped processing data in 2023 and the service was shut down on 1 July 2024 (https://blog.google/products/ads-commerce/upgrade-to-google-analytics-4-before-july-1/). That 136 KB does nothing.
- Meta pixel 207 KB (2 files), Google Sign-In library 102 KB on every page including product pages, Klaviyo 76 KB in 11 files, Clarity 27 KB, Cloudflare beacon 11 KB. CustomerLabs (`cdn.js.customerlabs.co/cl861926ufst6h.js`) returned 403 in every run; it may be blocked only from the test network, but it is worth checking.
- These do load after the site's own code, which is the right order. But they add 8.7 s of main-thread work on the homepage between 22 and 40 s, and each tag is a separate connection.

### P8. Heavy homepage: 3,134 DOM nodes, 114 product cards, 66 scripts (medium)

- The homepage renders 114 product cards across several carousels (152 images in total, from the image list in the raw data), plus 3 hero banners. The HTML is 208 KB raw with 79 KB of inline CSS, 45 KB of page data and 47 KB of inline scripts. After hydration the DOM is 578 KB of HTML. First-party JavaScript is 664 KB in 42 chunks on the homepage (`_app` chunk alone is 152 KB) and 7 GraphQL calls fire after hydration.
- Total blocking time of 5.2 s and 62 long tasks on the homepage. Each tap on a slow phone during that window waits.

### P9. Small things

- The bare domain gehnaindia.com sends a 301 to www (0.41 s). Fine, but any ads or links should use the www address directly.
- 2 CDNs in a row (Cloudflare then CloudFront) mean 2 caches to purge and 2 places where a stale PNG can stick.
- Fonts and JS are cached for 1 year with `immutable` (good). HTML on the homepage is cached for 30 minutes at the browser and 1 day at the CDN with stale-while-revalidate (good).
- The `email-decode` and bot challenge scripts add 3 to 4 small requests per page.

## 5. Top 10 fixes, ranked by impact

Gains are for the slow 4G test profile above. On fast Wi-Fi they will be smaller but still real. "Line time" means size divided by 200 KB per second, the throughput of the test line.

### Fix 1. Replace the 2 MB fonts with Latin-only WOFF2 files

- Gain: about 1.93 MB less per first visit, about 9.5 s of line time. Expect the load event to move from 21 s to roughly 10 to 12 s on the homepage, and everything after it (hydration, product grids) to move earlier by a similar amount. Basis: fonts finished at 21.1 s and the load event followed at 21.2 s; the Latin WOFF2 versions measured 12.9 KB and 12.8 KB (Nanum Myeongjo) and 14.0 and 14.2 KB (Lato).
- Effort: 1 to 2 hours. Who: developer.
- Steps:
  1. Download the Latin subset WOFF2 files for Nanum Myeongjo 400 and 700 and Lato 400 and 700. The simplest source is the Google Fonts CSS: request `https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@400;700&display=swap` with a Chrome user agent, take the `.woff2` URL under the `latin` block, and save the file. Or run `pyftsubset NanumMyeongjo-Regular.ttf --unicodes="U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+2074,U+20AC,U+20B9,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD" --flavor=woff2` (fonttools). Keep U+20B9, the rupee sign.
  2. Put the 4 files in the project's fonts folder and point the `next/font/local` declarations at the `.woff2` files instead of the `.ttf` files. Keep `display: 'swap'` and the `adjustFontFallback` metrics so text does not jump when the font arrives.
  3. Alternative with even less work: switch to `next/font/google` for both families with `subsets: ['latin']`. Next.js downloads and self-hosts them at build time.
  4. Build, then check in DevTools that the 4 font requests are each under 20 KB and that no `.ttf` is requested.

### Fix 2. Turn off Cloudflare Rocket Loader (and Email Obfuscation) for this site

- Gain: the site's JavaScript starts running as soon as it is downloaded instead of after the load event. Combined with Fix 1, the product page should hydrate around 6 to 8 s on slow 4G instead of 16.5 s (first-party JS is about 1.2 MB, about 6 s of line time). Also removes a known cause of React hydration errors. Basis: chunk requests initiated by rocket-loader.min.js in all runs; first data call at 16.5 to 22.7 s, after the load event; Cloudflare's own docs recommend disabling it when JavaScript misbehaves.
- Effort: 15 minutes. Who: whoever holds the Cloudflare login (developer or owner). No code change.
- Steps:
  1. Cloudflare dashboard, pick the gehnaindia.com zone, Speed, Optimization, Content Optimization. Set Rocket Loader to Off.
  2. Same page (or Scrape Shield), set Email Address Obfuscation to Off. Then write the 2 footer email addresses as plain text or as a small inline SVG if you worry about spam bots.
  3. Purge Everything in Cloudflare cache so the rewritten HTML is gone.
  4. Reload a product page and confirm the `<script>` tags in view-source have plain `type="text/javascript"` (or none) and there is no `rocket-loader.min.js`.
  5. Keep the site's existing pattern of loading tags after the page is interactive, which already exists in the code.

### Fix 3. Serve banners and icons as AVIF/WebP and stop the CDN pinning the PNG

- Gain: hero banner from 288 KB to roughly 40 to 80 KB; 7 category icons from about 0.85 MB to under 50 KB; other 2 banners from 542 KB to about 100 KB. Roughly 1.4 MB less on the homepage, about 7 s of line time. LCP should improve by 1 to 2 s on its own and by more together with Fix 4. Basis: product photos of the same width already arrive as AVIF at 11 to 33 KB; the banner was still PNG with an AVIF-accepting request and a Cloudflare cache HIT.
- Effort: 2 to 4 hours. Who: developer, plus the Cloudflare login.
- Steps:
  1. In `next.config.js` confirm `images.formats: ['image/avif', 'image/webp']`. Product images already come as AVIF, so this is probably set.
  2. Make the Cloudflare cache respect the browser's image preference. Two options. Option A, if the plan is Pro or higher: create a Vary for Images rule for the zone (POST `/zones/{zone_id}/cache/variants` with `{"value":{"png":["image/avif","image/webp"],"jpeg":["image/avif","image/webp"]}}`), and the optimised URL must end in an image extension for Cloudflare to apply it, so rewrite `/_next/image?url=...` responses through a small route such as `/img/[...].png` or use a custom `loader`. Option B, any plan: bypass Cloudflare cache for `/_next/image*` with a Cache Rule (Bypass cache) and let CloudFront, which sits behind it and does honour `Vary: Accept`, serve them. Option C, simplest: convert the static files in `/static/images/banner/` and `/static/images/browse-categories/` to AVIF and WebP at build time (Squoosh, `sharp`, or `cwebp`/`avifenc`), reference the `.avif` files directly with a `<picture>` fallback, and skip the optimiser for them.
  3. For the 7 category icons add `sizes="60px"` to the `<Image>` component so Next.js requests a 96 or 128 px file instead of 640 px.
  4. Give the 2 non-visible banners in the hero carousel `loading="lazy"` and no `priority`, so only the first banner downloads at start.
  5. Purge both caches (Cloudflare Purge Everything, and a CloudFront invalidation for `/_next/image*` and `/static/images/*`). Then request the banner URL with `Accept: image/avif` and confirm `content-type: image/avif`.

### Fix 4. Use `priority` only on the true LCP image

- Gain: the hero banner gets the line to itself for the first seconds. LCP on the homepage should fall from 7.9 s towards 2.5 to 3.5 s together with Fixes 1 and 3 (288 KB alone is 1.5 s of line time; as AVIF under 0.5 s). Basis: 40 below-the-fold thumbnails carried `fetchpriority="high"`; the banner took 7.5 s for 288 KB.
- Effort: 1 hour. Who: developer.
- Steps:
  1. Search the code for `priority` on `<Image>` inside the product card and carousel components (the cards render at 175 by 175 px). Remove it there. Leave `priority` on the first hero banner only.
  2. On the product page, remove `priority` from the thumbnail strip (the 46 px images). Keep it on the main product photo.
  3. Add `sizes` to product cards (`sizes="(max-width: 600px) 50vw, 25vw"` or the real column width) so the browser asks for the right width.
  4. Confirm in DevTools Network that only 1 image on the homepage has priority High at start, and that thumbnails below the fold show `loading="lazy"`.

### Fix 5. Render products on the server for collection and product pages

- Gain: the biggest change for shoppers coming from ads. The product photo and the product grid would appear with the HTML (about 1 to 2 s on slow 4G after Fixes 1 to 4) instead of at 15 to 17 s. Basis: HTML arrives at 0.2 to 1.3 s; the product photo request started at 16.3 s; the collection grid arrived after hydration at about 15 s.
- Effort: 2 to 5 days. Who: developer.
- Steps:
  1. Product page: move the product query (the GraphQL call for the product by slug) into `getServerSideProps` or, better, `getStaticProps` with `revalidate: 600` and `fallback: 'blocking'` (ISR). Pass the product into the page so the main `<Image>`, title, price and add-to-cart button are in the HTML. Keep only truly personal parts (wishlist state, cart count) as client fetches.
  2. Collection page: fetch the first page of Tagalys results on the server the same way, and render the grid in the HTML. Filters and pagination can stay client-side.
  3. Remove the spinner and the indeterminate progress bar from the server-rendered HTML for these pages, or render them only when a client-side navigation is in progress.
  4. Change the response header for product and collection HTML from `private, max-age=1800, must-revalidate` to `public, s-maxage=600, stale-while-revalidate=86400` (if the HTML has no per-user content). That lets both CDNs cache product pages, removing the 1.27 s first-byte time seen on an uncached product page.
  5. Set `preload="none"` on the product videos and only fetch MP4 data when the shopper taps a video thumbnail.

### Fix 6. Reserve space for the top bar and header icons (CLS)

- Gain: CLS on collection and product pages from 0.12 to 0.14 down to under 0.05, which passes Google's threshold. Basis: the largest shift is the `<body>` moving 50 to 68 px when a bar is inserted at the top after hydration; the header icons shift 18 px.
- Effort: 1 to 2 hours. Who: developer.
- Steps:
  1. Find the component that inserts the bar above the header after load (it appears at 15 to 17 s in the runs, 50 px tall on the collection page and 68 px on the product page). Either render it in the server HTML, or reserve its height with a fixed-height container (`min-height: 50px`) that is present from the first paint.
  2. Render the search icon slot in the header at its final width from the start, so the cart and menu icons do not move.
  3. Replace the `MuiLinearProgress` indeterminate bar with a fixed 4 px placeholder or make it `position: absolute` so it does not affect layout.
  4. Check with Chrome DevTools, Performance panel, Layout Shifts, that no shift over 0.01 remains.

### Fix 7. Clean up the tags: drop UA, merge gtag loads, defer Google Sign-In

- Gain: about 0.3 to 0.4 MB less per page and 1 to 2 s less main-thread work. Basis: UA-41818105-2 gtag is 136 KB and does nothing since July 2024; the second gtag file is 182 KB; Google Sign-In is 102 KB on every page.
- Effort: 1 to 2 hours. Who: whoever manages GTM, plus the developer for Sign-In.
- Steps:
  1. In Google Tag Manager, find the Universal Analytics tag (UA-41818105-2) and pause or delete it. Publish the container.
  2. Load Google Ads conversions through the same gtag instance as GA4: 1 Google tag (G-FT109JXEC7) with the Ads account configured as a linked destination, instead of separate `gtag/js?id=AW-…` and `gtag/js?id=G-…` scripts.
  3. Load the Google Sign-In script (`accounts.google.com/gsi/client`) only on the login, signup and checkout pages, or on first tap of the profile icon, with `next/script` `strategy="lazyOnload"`.
  4. Load Clarity and Klaviyo with `requestIdleCallback` or after the first user interaction. Keep the Meta pixel and GA4 after hydration as now.
  5. Check whether CustomerLabs is still needed; it returned 403 in every test run.

### Fix 8. Slim the homepage

- Gain: fewer requests and less main-thread work. Lowering the DOM from 3,134 nodes and the carousels from 114 cards should cut long tasks noticeably (they total 8.7 s today). Basis: 114 product cards and 3 hero images rendered on first load, 7 GraphQL calls after hydration.
- Effort: 1 to 2 days. Who: developer.
- Steps:
  1. Render at most the first 4 to 6 cards of each carousel in the HTML and fetch the rest when the carousel is scrolled or enters the viewport (an IntersectionObserver around each section).
  2. Combine the 7 GraphQL calls that fire at hydration into 1 or 2, or move their data into `getStaticProps` so no client calls are needed for the first view.
  3. Run `next build` with `@next/bundle-analyzer` and look at the 152 KB `_app` chunk. Move page-specific libraries (Swiper, Razorpay, Klaviyo form code) out of `_app` into the pages that use them with `next/dynamic`.
  4. Move the 79 KB of inline Emotion CSS out of the HTML where possible by using the MUI server style extraction only for above-the-fold components.

### Fix 9. Cache product and collection HTML at the CDN

- Gain: first-byte time on uncached product pages from about 1.3 s to about 0.2 s (measured 1,266 ms on a MISS versus 153 to 175 ms on a HIT). Basis: the `private, must-revalidate` header on these pages.
- Effort: 2 hours. Who: developer.
- Steps: covered in Fix 5 step 4. If personal content must stay in the HTML, split it: cache the page, fetch cart count and wishlist state client-side. Set a CloudFront cache policy that includes the `Accept` header only for `/_next/image*`.

### Fix 10. Small clean-ups

- Gain: fractions of a second each. Effort: under 1 hour total. Who: developer.
- Steps:
  1. Use the www address in all ads, Instagram bio and email links so no shopper pays for the 301 redirect.
  2. Add `<link rel="preconnect">` for `https://api.gehnaindia.com` and `https://cdn-assets.gehnaindia.com` (the HTML preconnects only to cdn-images today).
  3. Remove the `dns-prefetch` for facebook.com and googletagmanager.com if those tags stay deferred, and add them back as `preconnect` only right before they load.
  4. After all fixes, run PageSpeed Insights on the 3 pages and keep a monthly check.

Expected total after Fixes 1 to 4 and 7 (all under a day of work): homepage weight from 6.5 MB to roughly 2.5 to 3 MB, fonts from 2 MB to under 60 KB, load event from 21 s to about 8 to 10 s on slow 4G, LCP from 7.9 s to about 3 s. Fix 5 is the one that makes product pages feel instant and is worth scheduling as a project.

## 6. What could not be verified

- No Lighthouse score or real-user data (CrUX) today: the PageSpeed Insights API quota was used up. The numbers here are lab runs under a fixed throttle. Real Indian phones on Jio or Airtel 4G will differ, and a mid-range phone may be slower than the 4x CPU slowdown used here.
- Interaction to Next Paint (INP) needs real taps and was not measured. The 5.2 s of blocking time on the homepage suggests it will be poor until the JavaScript load is cut.
- The test machine is in the US East (CloudFront edge IAD55). Indian shoppers will hit Mumbai or Chennai edges, so their first-byte time will be different, probably lower for cached pages.
- The test browser went through a corporate proxy that forced HTTP/1.1. Real users get HTTP/2 or HTTP/3 (the site advertises `alt-svc: h3`), which loads many small files in parallel better. So the timings above may be a little pessimistic for the JavaScript chunks. Byte counts are unaffected.
- The Cloudflare plan level and settings could not be seen. The PNG-locked-in-cache explanation fits the evidence (PNG returned to an AVIF-accepting request with a cache HIT and `vary: Accept`) but the confirming test is to purge the cache and request the image again with AVIF accepted.
- The exact AVIF size of the hero banner is an estimate by analogy with the site's own 750 px product photos (33 KB); the real figure depends on the artwork.
- The CustomerLabs script's 403 may be caused by the test network, not the site.
- Checkout, cart, search and account pages were not tested. The homepage was fetched 4 times, the collection and product pages 3 times each, plus a handful of asset checks, all read-only.

Sources used: Core Web Vitals thresholds (https://web.dev/articles/vitals), Lighthouse throttling profile (https://github.com/GoogleChrome/lighthouse/blob/main/docs/throttling.md), Cloudflare Rocket Loader docs (https://developers.cloudflare.com/speed/optimization/content/rocket-loader/), Cloudflare Vary for Images (https://developers.cloudflare.com/cache/advanced-configuration/vary-for-images/), Next.js image `priority` docs (https://nextjs.org/docs/pages/api-reference/components/image), Next.js font docs recommending WOFF2 (https://nextjs.org/docs/pages/api-reference/components/font), Next.js discussion on Cloudflare and `/_next/image` (https://github.com/vercel/next.js/discussions/39510), Universal Analytics shutdown (https://blog.google/products/ads-commerce/upgrade-to-google-analytics-4-before-july-1/), Google Fonts Latin subset files for Nanum Myeongjo and Lato (sizes measured on 24 September 2026).
