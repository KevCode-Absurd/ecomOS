# Arm B audit: Gehna home page speed

Page: https://www.gehnaindia.com/ (custom Next.js pages-router store behind Cloudflare), offline mirror of 199 responses. Profile: Pixel 5, slow 4G (1.6 Mbps, 150 ms RTT), 4x CPU, cold cache, median of 3 runs. All numbers below come from `speed_lab/results/baseline.json`, the store, or my own diagnostic loads (`speed_lab/arms/arm-b/diag.py`, same profile, holds the measurement lock). Fix results are in `results.md`.

## 1. Baseline in one table

| Metric | Median |
|---|---|
| FCP | 720 ms |
| LCP | 1,720 ms (hero image `new-arrivals-mobile.png`, w=1200 AVIF, 40,309 B) |
| DOMContentLoaded | 2,658 ms |
| Load event | 15,436 ms |
| TBT (all long tasks until load + 6 s) | 2,468 ms |
| Wire bytes | 4,419,544 (first party 3,439,205; third party 980,339) |
| Requests served | 141 |
| CLS | 0.0001 |

The page paints fast (FCP 720 ms, LCP 1.7 s) because the HTML is server-rendered and the hero is in the HTML with `fetchpriority=high`. Everything after that is slow. The load event takes 15.4 s, and the app only becomes interactive after that.

## 2. What loads, and in what order (baseline run 1)

1. **0 to 100 ms.** HTML: 39,463 B on the wire (209,142 B raw). TTFB 46 ms. The HTML holds 31 `<script defer>` tags, all rewritten by Cloudflare Rocket Loader to `type="2ac945fd2ac69580976d0ac0-text/javascript"`, 53 inline Emotion `<style>` blocks, a JSS server style sheet, and a 44,926-character `__NEXT_DATA__`.
2. **180 to 460 ms.** 4 font preloads and 2 stylesheets start together. Lato 400 and 700 (36 KB each) finish at about 1.3 s. The two NanumMyeongjo files (1,043,710 B and 1,120,642 B) run until 14,950 and 15,356 ms.
3. **222 to 1,661 ms.** The hero image. It shares the link with the two big fonts.
4. **275 to 660 ms.** `email-decode.min.js`, a parser-blocking script in the body.
5. **360 to 2,684 ms.** `rocket-loader.min.js` (defer). Only when it runs, at about 2.7 s, do the 31 Next.js chunks start (2,696 ms). They finish between 3.1 and 8.7 s (`_app` 155,390 B ends at 8,720 ms), slowed by the fonts.
6. **710 to 7,547 ms.** 7 category icons and 2 more hero slides (lazy, but inside the lazy-load margin).
7. **15,436 ms.** Load event, set by the last Nanum font.
8. **15.4 to 16 s.** Rocket Loader runs the app. Hydration long tasks of 602 and 622 ms. The app mounts and calls GraphQL 3 times at 16.5 s.
9. **16.3 to 22 s.** `afterInteractive` tags: GTM (175,982 B), gtag for UA (133,440 B), GA4 (190,734 B) and Ads (180,796 B), Meta `fbevents.js` (111,400 B) and config (87,783 B), Klaviyo (12 requests, 68,527 B), Clarity (27 KB). Then 16 product carousel images (`fetchpriority=high`, preloaded by React) and 9 more lazy ones, ending at 20.7 s.

## 3. Where the bytes go (baseline run 1, wire, 4,425,667 B in total)

| Group | Requests | Bytes | Share |
|---|---|---|---|
| First-party fonts | 4 | 2,236,653 | 50.5% |
| Third-party scripts | 20 | 898,594 | 20.3% |
| First-party scripts | 45 | 621,423 | 14.0% |
| First-party images | 36 | 594,611 | 13.4% |
| HTML, CSS, API, beacons | 15 | 74,386 | 1.7% |

Two font files are 49% of all bytes. They hold 11,172 Hangul glyphs each. The page has no Korean text.

## 4. Where the time goes

- **Network, not CPU, sets the load event.** At 1.6 Mbps the link moves about 200 KB per second. 2.2 MB of fonts is about 11 s of transfer on its own.
- **Rocket Loader holds the app until after load.** In the baseline the chunks are downloaded by 8.7 s, but the app mounts at 16.8 s.
- **The main thread is busy for about 2.5 s in total.** A trace of the fixed page (arm-b-f03) splits it: React hydration and re-render in `framework.js` (tasks of 764 and 632 ms), `_app` evaluation (166 ms), the Cloudflare bot script `challenge-platform/.../jsd/main.js` (254 ms), Meta `fbevents.js` (255 ms), Klaviyo (95 ms), Google One Tap (73 ms).
- **The LCP image is small but waits for sockets.** The replay host speaks HTTP/1.1, so the browser opens 6 sockets per host. 4 font preloads and 2 stylesheets take all 6 first.

## 5. Top 10 limiters

Ranked by expected marginal effect on LCP, load and blocking time with changes to what the browser receives. Full records, with the `source` field, are in `limiters.json`. "Measured" below means the harness delta when the fix was added on top of the previous variant.

### 1. Full Korean serif font files (source: SPD-073 plus audit)
- **Evidence:** 2,164,352 B wire, 49% of bytes; both preloaded at 182 ms and ending within 500 ms of the load event.
- **Fix:** subset to Latin plus the symbols the page uses (356 code points), WOFF2, 50.6 and 51.0 KB. Point `@font-face` and preloads at the new files.
- **Expected:** load down by about 10 s, bytes down 2 MB. Basis: the files end with the load event and 2 MB is about 10 s at 1.6 Mbps.
- **Measured (f01):** load 15,436 to 3,089 ms, wire -2.60 MB, TBT -1,258 ms. Fidelity failed: see limiter 2.
- **Effort:** S. **Risk:** low; checked that stars, bullets, curly quotes and hearts stay in the subset.

### 2. Rocket Loader serialises the app scripts (source: SPD-072 plus audit)
- **Evidence:** app mounts at 16,751 ms. With fonts fixed (f01), Rocket Loader fetched the 31 chunks one at a time; at load plus 6 s the product carousel (1,199 characters) was still missing.
- **Fix:** serve the plain `defer` tags Next.js emits; drop `rocket-loader.min.js`. On Cloudflare: one toggle.
- **Expected:** app mount near 6 s. DCL later, because native defer scripts run before it.
- **Measured (f02):** app mount 6,180 ms, fidelity back to PASS on the normalized check. But load rose to 14,046 ms and TBT to 3,309 ms, because the `afterInteractive` tags now ran before load. That led to limiter 3.
- **Effort:** S. **Risk:** low, if shipped with limiter 3.

### 3. Third-party tags on `afterInteractive` (source: audit; risk rule SPD-062)
- **Evidence:** 7 `next/script` tags in `_app`. In f02 they started at about 6 s and held the load event to 14 s.
- **Fix:** `strategy: "lazyOnload"` (load event, then browser idle). Nothing removed.
- **Expected:** load back near 6 s.
- **Measured (f03):** load 14,046 to 6,480 ms, TBT -737 ms.
- **Effort:** S. **Risk:** medium for tracking. Meta `fbevents.js` now starts at about 8.2 s (median, f08) instead of just after hydration. Visitors who leave in that gap are not counted by GA4, Ads, Meta, Klaviyo or Clarity. Any code that calls `gtag` or `fbq` early must guard for it. Every event needs a test with consent on and off.

### 4. Category icons 640 px for a 60 px slot (source: audit; card 8883db1cfb1d)
- **Evidence:** 7 icons, 228,928 B, all before load.
- **Fix:** w=128 and w=256 AVIF (81,052 B for the 7 files at w=256); srcset 1x/2x points at them.
- **Expected:** DCL and load about 0.5 to 0.7 s earlier.
- **Measured (f04):** DCL -588 ms, load -560 ms, wire -145 KB.
- **Effort:** S. **Risk:** low.

### 5. LCP image behind font preloads (source: SPD-043; card 958af3150188)
- **Evidence:** the hero ends at 1,603 ms although it is 40 KB and requested at 225 ms. No NanumMyeongjo text is in the first viewport (text walk in diag.py), yet both weights were preloaded.
- **Fix:** `<link rel=preload as=image fetchpriority=high imagesrcset imagesizes>` first in `<head>`; drop the 2 Nanum preloads.
- **Expected:** LCP about 0.3 s faster.
- **Measured (f05):** LCP 1,648 to 1,352 ms.
- **Effort:** S. **Risk:** low; CLS unchanged at 0.0001.

### 6. Lato as TTF (source: SPD-089 WOFF2 step; card 731928d47c17)
- **Evidence:** 72,301 B wire for the only above-the-fold web font.
- **Fix:** lossless WOFF2, 56,244 B.
- **Measured (f06):** LCP -52 ms (edge of noise), wire -12 KB.

### 7. Dead Universal Analytics tag (source: audit plus web)
- **Evidence:** 133,440 B gtag plus 20,770 B `analytics.js`. Standard UA stopped processing hits on 1 July 2023 (web_log.md #1).
- **Fix:** remove the UA loader and config call; keep `window.gtag`, which the app uses for `user_data`.
- **Measured (f07):** third-party bytes -154 KB. Timing inside noise, as expected for a tag that runs after load.
- **Risk:** low; confirm in GA admin that nobody still reads the UA property.

### 8. Blocking email-decode script (source: SPD-056, SPD-072 step 3)
- **Evidence:** 656 B, blocking, 275 to 660 ms.
- **Fix:** `defer` in `<head>` before the Next.js scripts. The e-mail still decodes.
- **Measured (f08):** nothing outside noise. Kept because it is harmless.

### 9. Hydration and bundle cost (source: audit; out of reach)
- **Evidence:** 621 KB of first-party JS, `_app` 501 KB raw, hydration tasks of 764 and 632 ms, 1,840 DOM nodes, two CSS-in-JS systems (JSS and Emotion). TBT stays at about 2.4 s in every variant.
- **Fix:** needs the app: split `_app`, lazy-hydrate below-fold sections, drop one CSS-in-JS library. Not doable by changing responses alone.

### 10. Repeated post-hydration work (source: audit; SPD-146 fits part of it; out of reach)
- **Evidence:** 3 identical GraphQL POSTs (7,904 B each), 16 below-fold carousel images marked `fetchpriority=high` and preloaded, `/m/[category]` chunks downloaded twice.
- **Fix:** needs code. Bandwidth effect is after load, so the measured effect would be small.

## 6. How I used the idea bank and the cards

I did my own audit first from the harness data, then ran the bank for `site_speed` with the store tags and searched it for font, preload, third-party, defer, subset and rocket. I kept the ideas whose signal really fires here.

**Ideas that fired and carried a fix:** SPD-073 (the signal names almost this exact case: a framework store shipping a Korean serif font), SPD-072 (first-party JS runs after load behind Cloudflare), SPD-043 (preload only the LCP image and critical fonts), SPD-089 (WOFF2 part only), SPD-056 (defer a blocking script), SPD-062 (the tracking test rule behind the risk note on limiter 3).

**Cards cited:** 958af3150188 (preload and fetchpriority for the LCP element; do not preload too much), cc2d433b9ede (reduce fonts to the minimum), 8883db1cfb1d (resize images to display size; never lazy-load the hero), 731928d47c17 (serve fonts as WOFF2).

**Ideas I challenged:**
- **SPD-042, force eager loading on in-view lazy images.** The signal fires (7 in-view category icons carry `loading="lazy"`), but they are not the LCP element. On 6 HTTP/1.1 sockets, making them eager would add 7 requests at 190 ms next to the hero. After limiter 4 they are 81 KB and start at 720 ms, and the icons are not what users wait for. Not applied.
- **SPD-087, font-display: swap.** Does not fire: every `@font-face` already has `swap`.
- **SPD-036, LCP image under 250 KB.** Does not fire: the hero is 40 KB. Its problem was queueing, not size.
- **SPD-041, lazy-load below the fold.** Mostly does not fire: collection and store images are already lazy. The carousel images load anyway because they sit inside the lazy-load margin.
- **SPD-056, defer blocking scripts.** Fired, but the claimed effect was bigger than what I measured (f08: nothing outside noise).
- **SPD-146, fetchpriority=low on non-critical images.** The hero slides 2 and 3 already load at low priority as lazy images. Low expected effect; not applied.

**Where the winners came from:** the two largest wins (limiters 1 and 2) matched bank ideas, and my audit found them too. The LCP win came from a bank idea plus a card. Limiters 3, 4 and 7 came from the audit and one web check. The bank added no idea for limiters 3, 4 and 7.

**Web use:** one fetch (Google Analytics help, UA shutdown date), under 1 KB of text. Logged in `web_log.md`.

## 7. Assumptions and caveats

- **The official fidelity check cannot pass on this replay setup.** Cloudflare RUM and the bot script POST beacons. `serve.py` does not read POST bodies, so the leftover body is parsed as the next request and answered 501 with the body in the message. The message holds a random id, so it is "new" on every load. Baseline runs 2 and 3 fail against run 1 the same way. I added `check_norm.py`, which keeps every check but replaces that payload with a placeholder, and runs all 3 runs. I did not edit the official script.
- **Wire bytes are gzip level 6 from the replay server**, not Cloudflare's brotli. I kept my edited text files compressed the same way as the originals (the `Variant.put` helper drops the flag; `fixes/common.py` restores it).
- **TBT here** counts every long task until load plus 6 s, not only FCP to TTI. Fixes that make load earlier also shrink the window, so TBT deltas need care.
- **HTTP/1.1 replay.** Production Cloudflare serves HTTP/2 or 3, where 6-socket queueing matters less. The limiter 5 gain may be smaller in the field.
- **DCL got later on purpose.** Rocket Loader fired DOMContentLoaded early while the app waited.
