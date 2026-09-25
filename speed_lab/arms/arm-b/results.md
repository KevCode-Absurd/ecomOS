# Arm B results: Gehna home page, cumulative fixes

Profile: Pixel 5, slow 4G (1.6 Mbps, 150 ms RTT), 4x CPU, cold cache. Every number is the median of 3 harness runs (`speed_lab/results/<label>.json`), built by `speed_lab/arms/arm-b/table.py`. KB = 1,024 bytes of wire (as served by the replay server). "App mount" is the start of the first `api.gehnaindia.com/graphql` call, which the app makes right after hydration.

| Variant | Fix added | LCP ms | FCP ms | DCL ms | Load ms | TBT ms | App mount ms | Wire KB | 1st-party KB | 3rd-party KB | Requests | Official check | Normalized check |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | none | 1,720 | 720 | 2,658 | 15,436 | 2,468 | 16,751 | 4,316 | 3,359 | 957 | 141 | PASS (itself) | PASS |
| arm-b-f01 | Nanum fonts subset to WOFF2 | 1,704 | 712 | 2,115 | 3,089 | 1,210 | not reached | 1,781 | 1,293 | 488 | 120 | FAIL | FAIL |
| arm-b-f02 | Rocket Loader off | 1,656 | 728 | 5,503 | 14,046 | 3,309 | 6,180 | 2,430 | 1,343 | 1,087 | 165 | FAIL* | PASS |
| arm-b-f03 | 3rd-party tags lazyOnload | 1,656 | 740 | 5,512 | 6,480 | 2,572 | 6,277 | 2,423 | 1,341 | 1,083 | 142 | FAIL* | FAIL** |
| arm-b-f04 | Category icons right-sized | 1,648 | 720 | 4,923 | 5,920 | 2,457 | 5,738 | 2,282 | 1,199 | 1,083 | 143 | FAIL* | PASS |
| arm-b-f05 | Hero preload first, no Nanum preload | 1,352 | 732 | 5,014 | 5,940 | 2,286 | 5,771 | 2,279 | 1,196 | 1,083 | 141 | FAIL* | PASS |
| arm-b-f06 | Lato as WOFF2 | 1,300 | 728 | 4,961 | 5,956 | 2,492 | 5,780 | 2,267 | 1,185 | 1,083 | 142 | FAIL* | PASS |
| arm-b-f07 | Dead UA tag removed | 1,292 | 716 | 4,910 | 5,872 | 2,366 | 5,648 | 2,113 | 1,180 | 932 | 144 | FAIL* | PASS |
| arm-b-f08 | email-decode made non-blocking | 1,288 | 736 | 4,877 | 5,830 | 2,463 | 5,646 | 2,117 | 1,185 | 932 | 143 | FAIL* | PASS |

\* The only official failure is "new console errors" of the form `501 (Unsupported method ('{"startTime":...,"pageloadId":"<random id>"...`. These come from the replay server, not the page. `serve.py` never reads a POST body, so a beacon body left on a keep-alive socket is parsed as the next request line and answered 501. The body holds a timestamp and a random id, so the text differs on every load. Proof: baseline runs 2 and 3 each have 4 such "new" errors against baseline run 1, so the unmodified page fails the official check too. `check_fidelity.py` compares exact strings, so no variant can pass it while Cloudflare RUM beacons fire. `speed_lab/arms/arm-b/check_norm.py` runs the same checks on all 3 runs and only replaces the random payload with a placeholder. Title, body text, images in view, first-party misses and every other error class are checked exactly as in the official script.

\*\* arm-b-f03 run 2 had a CORS preflight failure on `api.gehnaindia.com/graphql` (runs 1 and 3 passed, body text was complete in all 3). The app sends 3 GraphQL POSTs on the same host, so an OPTIONS preflight on a socket with an unread POST body hits the same replay defect. I believe it is an artifact, but I cannot prove it from the logs (the server does not log OPTIONS). It did not recur in the 15 runs of f04 to f08.

arm-b-f01 fails for a real reason: body text 8,724 vs 9,923 characters. With the fonts fixed, load fired at 3.1 s, but Rocket Loader was still fetching the 31 Next.js scripts one at a time. At load plus 6 s the app had not hydrated, so the product carousel (16 earrings with prices) was not on the page yet. The fix is sound; its partner is f02. Ship f01 and f02 together, never f01 alone. f02 is the repair, and it passes.

## Total change, baseline to arm-b-f08

| Metric | Baseline | arm-b-f08 | Change |
|---|---|---|---|
| LCP | 1,720 ms | 1,288 ms | -432 ms (-25.1%) |
| FCP | 720 ms | 736 ms | +16 ms (noise) |
| DOMContentLoaded | 2,658 ms | 4,877 ms | +2,219 ms (+83.5%), see below |
| Load event | 15,436 ms | 5,830 ms | -9,607 ms (-62.2%) |
| TBT (all long tasks to load + 6 s) | 2,468 ms | 2,463 ms | -5 ms (no change) |
| App mount (hydrated) | 16,751 ms | 5,646 ms | -11,105 ms (-66%) |
| Product carousel images done | 20,721 ms | 8,366 ms | -12,355 ms |
| Wire bytes | 4,419,544 | 2,167,793 | -2,251,751 (-50.9%) |
| First-party bytes | 3,439,205 | 1,213,377 | -2,225,828 (-64.7%) |
| Third-party bytes | 980,339 | 954,416 | -25,923 (-2.6%) |
| Requests | 141 | 143 | +2 |
| CLS | 0.0001 | 0.0001 | none |

Page text in a diag load of arm-b-f08 is 9,919 characters and line-by-line identical to a diag load of the baseline, including the decoded careers e-mail. The run 1 screenshots match: same header, search, 7 category icons, hero carousel and bottom bar. In f08 the carousel shows slide 2 at screenshot time, because the app hydrates 11 s earlier and autoplay has already advanced; slide 2 is fully loaded. Every third-party endpoint the baseline hit is still hit in all 3 runs (Meta pixel `/tr/`, GTM, GA4 and Ads gtag, `ccm/collect`, Clarity, Klaviyo, CustomerLabs), except `analytics.js` and the UA gtag, which f07 removes on purpose.

## Which fixes carried it

- **Load event and bytes: f01 (fonts).** -12,347 ms load and -2.60 MB wire against the baseline. It is almost the whole byte win.
- **Hydration: f02 plus f03 together.** The app now mounts at 5.6 s instead of 16.8 s, and products show at 8.4 s instead of 20.7 s. f02 alone made load worse (+10,958 ms against f01) and TBT worse (+2,099 ms), because the tags now ran before load; f03 took load from 14,046 to 6,480 ms.
- **LCP: f05.** -296 ms. The hero no longer queues behind font preloads. f06 added -52 ms.
- **DCL and load: f04.** -588 ms DCL and -560 ms load from 148 KB less image data.
- **Third-party bytes: f07.** -154 KB.

## Fixes that did nothing measurable

- **f08 (email-decode):** every metric moved within run-to-run noise (LCP -4 ms, load -42 ms, TBT +97 ms). Kept because it is harmless, but it is not worth a ticket on its own.
- **f06 (Lato WOFF2):** -52 ms LCP is at the edge of noise (runs 1,292 to 1,328 ms against 1,344 to 1,364 ms for f05). Bytes -12 KB.
- **TBT:** no fix moved it for good. Runs spread about 400 ms inside one variant (f08: 2,152 to 2,588 ms). Most of it is React hydration (764 ms and 632 ms tasks in framework.js), which needs the app.

## Two numbers that got worse, and why

- **DOMContentLoaded +2.2 s.** Rocket Loader let DOMContentLoaded fire before any app script ran; the scripts then ran after the load event. With plain defer scripts, the browser runs them before DOMContentLoaded, so DCL now waits for about 620 KB of first-party JS. The page is not slower: hydration moved 11.1 s earlier.
- **Blocking before load.** Long tasks before the load event add up to 316 ms of blocking in the baseline and 1,166 ms in f08, because hydration now happens before load instead of after it. The total is unchanged.

Third-party bytes also need care: the baseline's 6 s window after a 15.4 s load cut off some tags in some runs (Google One Tap `gsi/client`, 101 KB, loaded in 0 of 3 baseline runs and in 3 of 3 f08 runs; Clarity in 1 of 3 against 3 of 3). The -2.6% third-party change is therefore conservative.

## What to tell the developer to ship first

1. **Subset NanumMyeongjo to Latin WOFF2** (one build step, or `subsets: ['latin']`), and set `preload: false` on it. This alone cuts 2 MB and about 12 s off the load event.
2. **In the same release, turn Rocket Loader off and move the 7 `_app` tags to `lazyOnload`.** Never one without the other: Rocket Loader off alone pulls the tags before load. Test every tracking event with consent on and off, and accept that visitors who leave in the first 2 s after load are not tracked.
3. **Add `sizes="60px"` (or `width={60}`) to the category icons** and a hero image preload before the font preloads.
4. **Remove the UA-41818105-2 tag.**
5. Then profile hydration. That is where the remaining 2.4 s of blocking time is, and it needs code, not edge tweaks.

I stopped at f08. The next limiters (hydration cost, the 155 KB `_app` bundle, repeated GraphQL calls, carousel images marked priority) need a rebuild of the Next.js app.
