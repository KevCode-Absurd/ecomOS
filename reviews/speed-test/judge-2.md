# Judge 2 verdict: Gehna speed audit, blind comparison

Read order: report 2, then report 1. Judged on the 2 files only.

## Scores

| Criterion | Report 1 | Report 2 |
|---|---|---|
| 1. Accuracy | 3 | 4 |
| 2. Depth | 4 | 5 |
| 3. Actionability | 4 | 5 |
| 4. Ecommerce and stack specificity | 5 | 4 |
| 5. Credibility of impact estimates | 4 | 4 |
| 6. Readability for the owner | 5 | 3 |
| 7. Errors and invented claims | 3 | 4 |
| Total | 28 | 29 |

## Reasoning per score

### Report 2

1. Accuracy, 4. The core mechanisms are right: Rocket Loader rewrites script `type` and runs the chunks itself, Email Obfuscation can cause hydration mismatches, `priority` on 40 off-screen tiles starves the hero, a missing `sizes` prop makes Next.js request 640 px icons, and Cloudflare ignores `Vary: Accept` unless a Vary for Images rule exists. Two weak points: it says "neither CDN caches" product HTML from the header alone, yet its own repeat loads show 0.18 s first byte; and I cannot confirm that Vary for Images is on Pro rather than Enterprise only.
2. Depth, 5. It goes past symptoms to causes with evidence: chunk requests initiated by `rocket-loader.min.js`, a PNG returned to an AVIF-accepting request with a Cloudflare HIT, the 102 KB Google Sign-In library on every page, 3 separate gtag loads, 7 GraphQL calls after hydration, and the HTTP/1.1 proxy caveat.
3. Actionability, 5. A developer can execute almost every step as written: the `pyftsubset` command with the Latin range plus U+20B9, `next/font/google` with `subsets: ['latin']`, the Cloudflare dashboard path, `getStaticProps` with `revalidate`, the exact cache-control header, `sizes="60px"`.
4. Specificity, 4. Strong on the stack (Pages Router, Emotion, Tagalys, Indian CloudFront edges, rupee sign). Lighter on the business side: no revenue figures, no sale calendar, no analytics event checks after tag changes.
5. Estimates, 4. Gains are bytes divided by 200 KB per second with the sums shown, and the fonts-set-the-load-event argument is measured (fonts finish at 21.1 s, load at 21.2 s). One number has no basis: Fix 2 says first-party JS is "about 1.2 MB", while section P8 measured 664 KB in 42 chunks.
6. Readability, 3. The verdict and fix headings are plain, but sections 3 and 4 lean on unexplained terms (hydrate, Emotion, Vary, ISR) and long paragraphs.
7. Errors, 4. The 664 KB versus 1.2 MB contradiction, the "neither CDN caches" claim, and a product-page LCP of 1.8 s that the report itself admits is the spinner (report 1 records the real image at 18.3 s, which is the truer reading).

### Report 1

1. Accuracy, 3. Most findings hold, but 3 claims look wrong or shaky. The theory that the Next.js resizer "skips files narrower than the requested size" does not match how the optimiser works, and the report's own note that the desktop banner was a slow cache miss fits the cache-pinning explanation in report 2 better. Third-party weight of "about 110 KB" for GTM, GA4, Meta pixel, Klaviyo, Clarity and Google Sign-In is far too low; the Meta pixel and gtag alone exceed that. "Cloudflare is caching private pages anyway" is asserted without the header shown.
2. Depth, 4. It finds real items the other misses: 30-minute CDN cache on resized images, cold resizes costing up to 4.2 s, `/cart` landing on the 404 page, GIF spinner and logo, video autoplay with preload. But it only hedges on Rocket Loader where hard evidence was available, and it undercounts the tag load.
3. Actionability, 4. Every fix has effort, owner, pass criteria, risk, rollback and dependencies, which is excellent for managing the work. The steps themselves are in words rather than exact code: "switch to Google's font loader", "look for components loaded with no server rendering". A good developer can map them, with some guessing.
4. Specificity, 5. Rupees, lakh and crore, the Diwali window, ads landing on product pages, checking view item and purchase events fire once after tag changes, stale prices after a purge, Tagalys ordering, variant switching on a real phone, a speed budget with the first 12 tiles in the HTML.
5. Estimates, 4. Arithmetic is shown and chained (fix 1 first, then fix 2 on top), and the 185 KB per second figure is measured. The business case is honest about its limits, but the 0.045% conversion rate depends on an unconfirmed "visits" count.
6. Readability, 5. A one-line glossary, a "what the phone shows in words" narrative, a week-by-week plan, and the business case in the owner's currency. The fix paragraphs are dense but the words are plain.
7. Errors, 3. The resizer theory, the 110 KB tag figure, the unverified Cloudflare-caching-private claim, and "no product name, no price" in product HTML, which report 2 contradicts (title and price present). One of them is wrong; report 1 at least gives a check (no `<h1>`).

## Which report should the owner act on

Report 2, by a narrow margin. Its diagnosis is the more trustworthy one: it proved the Rocket Loader mechanism and the Cloudflare PNG pin with direct tests, where report 1 guessed. Its steps name the exact props, config keys, headers and commands for this Next.js and Cloudflare stack, so the developer will not have to translate. It also caught the 3 gtag loads and the Google Sign-In library, which report 1's undercount hid. Report 1 remains the better owner document; borrow its verification gates, rollback notes and sequencing. The 2 reports agree on the big picture, which raises confidence in both.

## What each has that the other lacks

Report 2 has:
1. Hard evidence for Rocket Loader (rewritten `type` attributes, chunk initiators) and Email Obfuscation as a hydration risk.
2. The Cloudflare cache-pinning explanation for the PNG banner, with the AVIF-accept test and 3 concrete fixes.
3. Tag detail: dead UA tag plus 2 extra gtag loads, Google Sign-In on every page, 7 GraphQL calls to merge.

Report 1 has:
1. Pass criteria, risk, rollback and dependencies on every fix, a week-by-week plan, and a speed budget for CI.
2. Findings the other missed: 30-minute image cache TTL and cold resizes, `/cart` and unknown URLs hitting the 404 page, GIF logo and spinner, video autoplay.
3. A rupee business case and the analytics-event checks that protect revenue when tags change.

## Fix list for a developer tomorrow

Report 2's list, in its order, with 4 additions from report 1: raise `images.minimumCacheTTL` (report 1 fix 8), check `/cart` and 404 behaviour, verify purchase events after any tag change, and use report 1's before-and-after 3-load test as the pass gate for each release.

## Guess on the playbook

Report 1 was written from a specialised written playbook, report 2 from general knowledge. Report 1's fixed per-fix fields (gain, basis, effort, owner, steps, risk, rollback, depends on), the speed budget, and the templated business case with stock per-second conversion figures read like a filled-in contract, while report 2 reads like an engineer following the evidence and citing vendor docs as it goes.
