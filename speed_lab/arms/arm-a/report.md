# Gehna homepage speed audit (arm A)

Page: https://www.gehnaindia.com/ (Next.js pages router behind Cloudflare), mirrored offline with 199 responses.
Profile: Pixel 5, slow 4G (1.6 Mbps, 150 ms RTT), 4x CPU slowdown, cold cache, 3 runs, median.
All numbers come from `speed_lab/results/*.json` (the harness) or from the store, computed in code.
Where I used my own diagnostic loads (`tools/trace.py`, `tools/inspect_load.py`), they only explain the
harness numbers; they are never reported as results.

## 1. Baseline in one table

| Metric | Median |
|---|---|
| FCP | 720 ms |
| LCP | 1,720 ms (hero banner image, `new-arrivals-mobile`, 40,309 B AVIF) |
| DOMContentLoaded | 2,658 ms |
| Load event | 15,436 ms |
| TBT (sum of long-task time over 50 ms, load + 6 s) | 2,468 ms |
| Wire bytes | 4,419,544 B |
| First party / third party | 3,439,205 B / 980,339 B |
| Requests served | 141 |

## 2. What loads, and in what order

1. HTML (209,142 B raw, 39,463 B wire). TTFB is 46 ms in the lab. The head holds 4 font preloads, 2
   stylesheets, 31 Next.js script tags and a 44 KB inline JSS style block. The body holds 110 KB of
   server-rendered markup and a 45 KB `__NEXT_DATA__` block.
2. At 180 ms the 4 font preloads and 2 stylesheets start. Two of the fonts are 3 MB TTF files.
3. At 222 ms the LCP banner starts (fetchpriority high). At 275 ms the parser-blocking Cloudflare
   `email-decode.min.js` starts. At 360 ms `rocket-loader.min.js` starts.
4. At 710 ms the 7 category icons and hero slides 2 and 3 start. FCP is 720 ms. LCP is 1,720 ms.
5. At 2,696 ms Rocket Loader has arrived and only now requests the 31 Next.js scripts (534 KB wire of
   first-party JS). They finish by 8,720 ms, but Rocket Loader does not run them yet.
6. The two big fonts finish at 14,950 ms and 15,356 ms. The load event fires at 15,431 ms.
7. Only now does the app run: `_app` evaluation at 15.6 s, React hydration (766 ms task) at 16.0 s.
   Then next/script injects the tag stack (GTM, gtag G- and AW-, UA gtag, Meta pixel, Klaviyo, Clarity,
   CustomerLabs), GraphQL loads the product carousels, and 24 product images arrive around 17.7 to 20.5 s.

So the site is visible early but is not interactive for about 16 s on this profile, and the reason is
a font file, not the app.

## 3. Where the bytes go (baseline run 1)

| Type | Requests | Wire bytes |
|---|---|---|
| Font | 4 | 2,236,653 |
| Script | 65 | 1,520,017 (534 KB first party, the rest tags) |
| Image | 39 | 594,653 (icons 228,928; hero 124,181; products 238,659) |
| Document | 2 | 39,463 |
| Stylesheet | 3 | 7,641 |

Top third-party hosts: www.googletagmanager.com 680,952 B (GTM, 2 gtag builds, UA gtag),
connect.facebook.net 199,183 B, static.klaviyo.com plus static-tracking.klaviyo.com 68,484 B,
scripts.clarity.ms 26,851 B.

Images are already AVIF from the Next.js optimizer, so format is not the problem. Size choice is.

## 4. Where the time goes

A Chrome trace of the baseline (`tools/trace.py base`) attributes the long tasks:

- React (framework.js): 766 ms hydration and 791 ms second render, plus about 250 ms of smaller renders.
- `_app` and page chunk evaluation: 154 ms and 182 ms.
- Cloudflare bot check (`/cdn-cgi/challenge-platform/.../main.js`): 242 ms, and again 203 ms.
- Meta `fbevents.js` evaluation: 321 ms.
- Early parse, style and layout tasks with no script: 140 ms and 63 ms.

About 1.5 s of the 2.5 s TBT is React work inside the app bundle. That part cannot change without a
rebuild. The rest is mostly third-party code, which can be moved but not removed.

## 5. Top 10 limiters, ranked by expected effect on LCP, load and blocking time

Each entry is also in `limiters.json`. "Measured" refers to the cumulative variant table in `results.md`.

### 1. Two full Korean Nanum Myeongjo TTF files, preloaded
- Evidence: `14a3fceaeabbcb56-s.p.ttf` (3,056,912 B raw, 1,043,710 B wire) and `ae1a48c074c123e8-s.p.ttf`
  (3,073,144 B raw, 1,120,642 B wire), 11,880 code points each. 49% of all wire bytes. They end 75 ms
  before the load event.
- Fix (f02): Latin WOFF2 subset per weight, 19,220 B and 19,108 B, preloaded instead. A second
  `@font-face` per weight covers every other code point of the original with `unicode-range`, so a
  Korean or rare character still gets the right glyph. The browser only fetches that file if needed.
- Expected: load about 12 s earlier, about 2.1 MB fewer bytes. Basis: 2.16 MB at 200 KB/s is about 11 s.
- Effort: low (`subsets: ['latin']` in next/font). Risk: low.
- Measured: on top of f01, load 22,345 to 13,838 ms, wire 4.56 MB to 2.43 MB, LCP 1,672 to 1,576 ms.

### 2. Cloudflare Rocket Loader hides and delays all app scripts
- Evidence: 31 script tags have type `2ac945fd...-text/javascript`, so the preload scanner skips them.
  They start at 2,696 ms and run after the load event.
- Fix (f01): serve the tags as Next.js emits them and drop `rocket-loader.min.js`. In production this is
  one switch in the Cloudflare dashboard.
- Expected: scripts requested at about 0.2 s; hydration no longer waits for the load event.
- Effort: very low. Risk: low.
- Measured: alone it made things worse (load 15,436 to 22,345 ms, TBT 2,468 to 3,413 ms), because
  the app and its tags now start while the 2.16 MB of fonts still download, and all of it lands before
  the load event. It pays off only together with fix 1. See section 6 for why it went first.

### 3. Tag stack starts right after hydration and holds the load event
- Evidence: 986 KB of tag JS in run 1. In f02 the tag chain (GTM, then gtag, Clarity, Ads and
  Merchant Center hits) keeps the load event open to 13,838 ms. `fbevents.js` evaluation is a 321 to
  358 ms long task.
- Fix (f03): `strategy: "lazyOnload"` for the 6 next/script tags in `_app`. Next.js then injects them
  after the load event inside `requestIdleCallback`. A 2-line stub in `<head>` defines `dataLayer` and
  `gtag()` first, so `gtag('event', ...)` calls fired before GTM arrives are queued.
- Expected: load several seconds earlier. TBT stays, since the tags still run inside the 6 s window.
- Tracking risk: visitors who leave before load plus idle (about 5.5 s on this profile, less on real
  phones) are not recorded as page views by GA4, Google Ads, Meta, Klaviyo or Clarity. Events queue
  in `dataLayer`, so those are not lost. Meta and Klaviyo calls in the app check for the global first,
  so no errors.
- Measured: load 13,838 to 6,304 ms, TBT 3,519 to 2,590 ms. A 20 s inspection load confirms every tag
  still loads and sends its hits.

### 4. React hydration and re-render of a large tree (out of reach)
- Evidence: in the f04 trace, framework.js tasks of 811 ms and 688 ms, plus 383 ms for `_app` and page
  evaluation. 1,836 DOM nodes. 534 KB of first-party JS on the wire gates DOMContentLoaded.
- Fix: needs a rebuild. Split the home page, lazy-hydrate the below-the-fold carousels, move JSS to
  static CSS, trim the 155 KB `_app` bundle.
- Expected: the only lever that can cut TBT by more than a few hundred ms. Effort high, risk medium.
- Not applied.

### 5. Category icons fetched at 640 px for 60 px slots
- Evidence: 7 icons render at 60 x 60 CSS px (165 device px) but next/image has width 200, so the
  srcset is `w=256 1x, w=640 2x` and the phone takes the 640 px files: 228,928 B, starting at 0.7 s.
- Fix (f04): srcset `w=128 1x, w=256 2x` (what next/image emits for `width={128}`). The 256 px files
  are downscaled from the stored 640 px AVIFs at a quality calibrated to the site optimizer: 54,639 B.
- Expected: about 174 KB less early traffic. Effort and risk very low.
- Measured: DCL 5,260 to 4,668 ms, load 6,304 to 5,658 ms, LCP 1,572 to 1,500 ms.

### 6. Lato preloaded as TTF
- Evidence: 36,517 B and 35,784 B wire, high-priority preloads from 0.18 to 1.3 s, overlapping the LCP
  banner.
- Fix (f05): Latin WOFF2 subsets, 14,488 B and 14,620 B, plus unicode-range faces for the other 45
  code points.
- Expected: LCP 100 to 250 ms earlier. Measured: LCP 1,500 to 1,260 ms, load 5,658 to 5,308 ms.

### 7. LCP banner found late
- Evidence: requested at 222 ms, after the head's 31 script tags and 4 font preloads. It has
  `fetchPriority="high"` but no preload.
- Fix (f06): `<link rel="preload" as="image" fetchpriority="high" imagesrcset imagesizes>` placed before
  the font preloads (what next/image does with `priority`).
- Expected: LCP 50 to 150 ms earlier. Measured: LCP 1,260 to 1,132 ms.

### 8. Parser-blocking `email-decode.min.js` in the body
- Evidence: 956 B, marked render-blocking by Chrome, ends at 660 ms, just before FCP at 720 ms.
- Fix tried (f07): `defer`. Expected FCP up to 150 ms earlier.
- Measured: FCP 748 to 748 ms, LCP 1,132 to 1,148 ms. No gain. Reverted, since defer shows the
  "[email protected]" placeholder a little longer. The script was not the FCP gate; see limiter 9.

### 9. Two render-blocking stylesheets
- Evidence: 3,053 B and 4,621 B wire, done at 423 and 460 ms; the first paint task follows them.
- Fix (f08): inline both. The page sheet becomes `<style data-n-href="...">`, the element Next.js itself
  creates and toggles on client-side route changes, so later navigations keep correct styles. Next.js
  does not touch stylesheets on the first render (checked in `main.js`).
- Expected: FCP 150 to 250 ms earlier.
- Measured: FCP 748 to 520 ms. LCP went up 1,132 to 1,228 ms. With CSS inline, the 31 low-priority
  scripts start sooner and share the 6 HTTP/1.1 connections and 200 KB/s with the banner, whose download
  now ends at about 1,180 ms instead of 1,090 ms. Kept: net 228 ms earlier first paint for 96 ms later
  LCP, which is still 492 ms better than baseline. The replay server speaks HTTP/1.1; on Cloudflare's
  HTTP/2 or 3 with priorities this cost may shrink.

### 10. Dead Universal Analytics tag
- Evidence: `gtag/js?id=UA-41818105-2`, 133,440 B wire, 50 ms evaluation. Google's help page says
  standard UA properties stopped processing hits on 1 July 2023.
- Fix (f09): remove the UA loader element and its config line. Keep `dataLayer`, `gtag()` and
  `gtag('js')`. GA4 and Ads tags come from GTM and are untouched.
- Measured: third-party bytes 1,108,626 to 954,416 B. Timing metrics unchanged within noise.

## 6. Order of work, and one reverted attempt

My first f01 was the font fix (rank 1). Measured as `arm-a-x01-fonts-first`, load fell to 3,036 ms but
fidelity failed: page text 8,815 chars vs 9,923 and 983 DOM nodes vs 1,836. The cause: with the fonts
fast, the load event came at about 3 s, Rocket Loader cancelled its unfinished script preloads and then
re-fetched 20 scripts one at a time from 3.3 s to 8.9 s. Hydration started at 9.1 s, just as the harness
took its snapshot at load + 6 s. So the font fix could not pass on its own. I set it aside, applied the
Rocket Loader fix first (f01) and the font fix second (f02). Everything else follows the rank order.

## 7. Stopping point

After f09 the remaining limiters need the app rebuilt:
- React hydration and re-render, about 1.5 s of TBT (limiter 4).
- 534 KB of first-party JS that must arrive before DOMContentLoaded (4.4 s now).
- Hero slides 2 and 3 (84 KB) load early because the carousel keeps them near the viewport; changing
  that needs component code.
- 12 below-the-fold product images with `priority` set in a client component.
- `fbevents.js` (321 ms) and the Cloudflare bot script (about 240 ms) are third-party work that can
  be moved but not shrunk.

## 8. Harness issues found (affect both arms)

1. `check_fidelity.py` prints FAIL for every variant, including a re-run of the unchanged page. The
   replay server does not read POST bodies, so a Cloudflare RUM beacon body is read as the next request
   line and shows up as a 501 console error whose text includes a timestamp and a page-load UUID. That
   text never matches the baseline. Baseline runs 2 and 3 fail the same test.
2. The first-party miss test matches the substring `gehnaindia.com`, so Google tag URLs with
   `dl=www.gehnaindia.com` in the query count as first-party misses.
3. The same POST-body bug can break the next request on a connection. In f03 run 1 one GraphQL CORS
   preflight failed this way.

I did not change the shared harness. `tools/fidelity_norm.py` repeats every check but collapses the
501 text and judges first party by host. `results.md` reports both, for all 3 runs.

## 9. Assumptions

- The replay server is HTTP/1.1 with 6 connections per host, and latency is added per request. The
  production site uses HTTP/2 or 3, so absolute numbers differ; the direction of each fix should hold.
- Changing bytes under an existing hashed URL (CSS, `_app` JS) stands in for a rebuild with new hashes.
- The 128 and 256 px icons were made from the 640 px AVIFs because the source PNGs are not in the mirror.
- Screenshots differ only in carousel slide and the typing animation in the search box, because the
  snapshot happens at a different time after load. Page text in an inspection load is identical to base.
