# Arm A results

Profile: Pixel 5, slow 4G (1.6 Mbps, 150 ms RTT), 4x CPU, cold cache. Medians of 3 runs from
`speed_lab/results/<label>.json`. Variants are cumulative. Scripts: `fixes/fNN.py` (rerunnable, each
rebuilds its variant from its parent).

Fidelity columns: "raw" is `speed_lab/check_fidelity.py` (run 1). "norm" is `tools/fidelity_norm.py`
over all 3 runs (same checks; replay-server 501 text collapsed; first party judged by host). The raw
check fails on every variant because of timestamped replay errors, and it also fails baseline runs 2
and 3 against baseline run 1 (4 "new" errors each). See report.md section 8.

| Variant | Fix added | LCP ms | FCP ms | DCL ms | Load ms | TBT ms | Wire B | 1st party B | 3rd party B | Requests | Fidelity raw | Fidelity norm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | none | 1,720 | 720 | 2,658 | 15,436 | 2,468 | 4,419,544 | 3,439,205 | 980,339 | 141 | PASS (self) | 3/3 |
| f01 | Rocket Loader off | 1,672 | 732 | 7,110 | 22,345 | 3,413 | 4,560,942 | 3,448,141 | 1,112,801 | 167 | FAIL | 3/3 |
| f02 | Nanum Latin WOFF2 | 1,576 | 712 | 5,254 | 13,838 | 3,519 | 2,425,750 | 1,312,949 | 1,112,801 | 165 | FAIL | 3/3 |
| f03 | tags lazyOnload | 1,572 | 728 | 5,260 | 6,304 | 2,590 | 2,420,823 | 1,312,197 | 1,108,626 | 142 | FAIL | 2/3 (1) |
| f04 | icons 256 px | 1,500 | 724 | 4,668 | 5,658 | 2,602 | 2,249,616 | 1,140,990 | 1,108,626 | 143 | FAIL | 3/3 |
| f05 | Lato Latin WOFF2 | 1,260 | 728 | 4,386 | 5,308 | 2,522 | 2,203,087 | 1,098,453 | 1,108,584 | 144 | FAIL | 3/3 |
| f06 | LCP image preload | 1,132 | 748 | 4,321 | 5,366 | 2,368 | 2,211,900 | 1,103,274 | 1,108,626 | 144 | FAIL | 3/3 |
| f07 | email-decode defer (reverted) | 1,148 | 748 | 4,299 | 5,321 | 2,503 | 2,203,270 | 1,094,644 | 1,108,626 | 144 | FAIL | 3/3 |
| f08 | inline CSS (on f06) | 1,228 | 520 | 4,383 | 5,317 | 2,572 | 2,204,191 | 1,095,565 | 1,108,626 | 139 | FAIL | 3/3 |
| f09 | drop dead UA tag | 1,224 | 516 | 4,407 | 5,455 | 2,619 | 2,053,307 | 1,098,891 | 954,416 | 141 | FAIL | 3/3 |
| x01 | fonts first (rejected) | 1,632 | 732 | 1,920 | 3,036 | 1,326 | 1,835,046 | 1,335,562 | 499,484 | 124 | FAIL | 0/3 (2) |

(1) f03 run 1: one GraphQL CORS preflight failed with no CORS header, the signature of the replay
server's unread-POST-body bug; all 3 GraphQL POSTs were served 200, page text was 9,963 chars (+0.4%).
An extra inspection load of f03 had page text identical to base.
(2) x01 failed on content: 8,815 vs 9,923 chars, 983 vs 1,836 DOM nodes (snapshot taken mid-hydration).
Its low TBT and 3rd-party bytes are because the app and tags had not run yet. Not a valid result.

Final variant: **arm-a-f09** (f01 to f06, f08, f09).

## Total change, baseline to f09 (medians)

| Metric | Baseline | f09 | Change |
|---|---|---|---|
| LCP | 1,720 ms | 1,224 ms | -496 ms (-29%) |
| FCP | 720 ms | 516 ms | -204 ms (-28%) |
| DOMContentLoaded | 2,658 ms | 4,407 ms | +1,749 ms (see note) |
| Load | 15,436 ms | 5,455 ms | -9,981 ms (-65%) |
| TBT | 2,468 ms | 2,619 ms | +151 ms (within run spread: f09 runs 2,290 to 2,677) |
| Wire bytes | 4,419,544 | 2,053,307 | -2,366,237 (-54%) |
| First-party bytes | 3,439,205 | 1,098,891 | -2,340,314 (-68%) |
| Third-party bytes | 980,339 | 954,416 | -25,923 |

Note on DCL: in the baseline, DCL at 2.7 s only meant "Rocket Loader ran"; the app itself ran after
15.4 s. In f09 the 31 app scripts are normal defer scripts, so DCL now includes downloading and running
them, and the app is hydrated at about 4.5 to 5 s instead of about 16 s.

Note on third-party bytes: f09 drops the UA tag (133 KB) but now also counts Google sign-in
(accounts.google.com, 101,394 B in run 1), which is a lazyOnload script the baseline never reached
inside its window. Every tag still loads in f09 (checked with a 15 s inspection load).

## Which fixes carried it

- Load: f02 fonts (-8.5 s after f01) and f03 tags after load (-7.5 s). Together with f01 they turn
  15.4 s into 6.3 s. f04 icons and f05 Lato added -1.0 s.
- LCP: f05 Lato WOFF2 (-240 ms) and f06 LCP preload (-128 ms) did most of it; f02 and f04 helped less.
- FCP: only f08 inline CSS (-228 ms).
- Bytes: f02 (-2.1 MB), f04 (-171 KB), f09 (-154 KB third party).
- f01 on its own was harmful (load +6.9 s, TBT +945 ms). It is needed so the app runs early once the
  fonts are fixed; without it the font fix fails fidelity (x01).

## Which fixes did nothing measurable

- f07 (defer email-decode): FCP unchanged at 748 ms. Reverted.
- f09 (drop UA tag): bytes only. No timing change beyond run noise.
- TBT: no fix moved it beyond run noise after f03. About 1.5 s of it is React hydration and render
  inside the app bundle (trace), the rest is Meta pixel and the Cloudflare bot script. Out of reach
  without a rebuild.
- f08 raised LCP by 96 ms while cutting FCP by 228 ms (HTTP/1.1 connection sharing; see report).

## What to ship first

1. Subset the fonts: `subsets: ['latin']` in next/font for Nanum Myeongjo and Lato. One config line,
   2.1 MB less per first visit.
2. Turn Rocket Loader off in Cloudflare, in the same release as step 1 (alone it makes load worse).
3. Move the tags in `_app` to `strategy="lazyOnload"` and add the dataLayer/gtag stub, after the
   marketing owner accepts the page-view risk for very short visits.
4. Set `width={128}` on the category icons and `priority` on the first hero slide.
5. Remove the Universal Analytics tag.
6. Then consider inline critical CSS (Next.js `optimizeCss`) and check LCP on real HTTP/2.
Beyond that, TBT needs app work: smaller hydration, lazy-hydrated carousels, static CSS instead of JSS.
