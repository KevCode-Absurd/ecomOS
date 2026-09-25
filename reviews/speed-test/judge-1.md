# Judge 1: Gehna speed audit, blind comparison

Judged only the 2 blind reports. Site not fetched. Scores 1 to 5.

## Scores

| Criterion | Report 1 | Report 2 |
|---|---|---|
| 1. Accuracy | 3 | 4 |
| 2. Depth | 4 | 5 |
| 3. Actionability | 4 | 4 |
| 4. Ecommerce and stack specificity | 4 | 4 |
| 5. Credibility of impact estimates | 4 | 3 |
| 6. Readability for a non-technical owner | 5 | 3 |
| 7. Errors and invented claims | 4 | 4 |
| Total | 28 | 27 |

## Reasoning

**Accuracy.** Report 1 (3): the font, client-rendering and Rocket Loader mechanisms are right, but it sizes all third-party tags at about 110 KB and tells the owner to ignore them, which is implausible for GTM, GA4, a Google Ads gtag, the Meta pixel, Klaviyo, Clarity and Google Sign-In (Report 2 measured 1.05 MB, which matches known sizes); its theory that the resizer skips narrow files is a guess, since Next.js still converts format when it refuses to upscale. Report 2 (4): its Rocket Loader finding is backed by hard evidence (rewritten `type` attributes, chunks requested by rocket-loader.min.js) and its PNG-pinned-in-Cloudflare-cache theory fits its own test (PNG returned to an AVIF-accepting request with a cache HIT; Cloudflare ignores `Vary: Accept` by default), but it calls first-party JavaScript "about 1.2 MB" after measuring 664 KB, and I could not confirm that Vary for Images is on Pro plans rather than Enterprise only.

Two claims clash across the reports and need a view-source check: Report 1 says the product HTML has no name, price or `<h1>`, Report 2 says price and title are there; Report 1 says Cloudflare caches private product pages for up to an hour, Report 2 says neither CDN caches them and saw a 1.27 s first byte on a miss.

**Depth.** Report 1 (4): it traces the timeline through fonts, load event, hydration and API calls and finds real structural items (reviews band causing CLS, 6 product API calls, GIF spinner and logo, video preload, 404 redirects) but stops near the load event and misses the post-load tag weight. Report 2 (5): it reaches root causes with evidence, including the 2 CDNs in a row, the Email Obfuscation hydration risk, 3 hero banners downloading at once, MP4 range requests, the uncached product HTML, and 8.7 s of main-thread work between 22 and 40 s.

**Actionability.** Report 1 (4): each fix has steps, a pass test, a risk and a rollback, but some steps say "find why" rather than "do this". Report 2 (4): exact file names, a working `pyftsubset` command with the rupee sign, the Cloudflare menu path, the ISR config and header strings, but Fix 8 step 4 (limit Emotion CSS to above-the-fold components) is not really executable and there are no pass criteria or rollbacks.

**Specificity.** Report 1 (4): strong on the commerce side (rupee glyph, Diwali capacity check, sale freeze, purge on price or stock change, conversion events checked with consent on and off). Report 2 (4): strong on the stack side (Pages Router proof, ISR with `fallback: 'blocking'`, `next/font/local`, `next/dynamic`, Jio and Airtel, Mumbai and Chennai edges) but thinner on the business.

**Credibility of estimates.** Report 1 (4): every gain shows its arithmetic (1,771 KB at 185 KB per second is 9.6 s; 280 KB plus 0.35 s server time is about 2 s; CLS 0.110 minus 0.059) and the chain from fix to fix is explicit, with expected numbers per week. Report 2 (3): "line time" arithmetic is shown, but LCP outcomes are loose ("towards 2.5 to 3.5 s"), the Fix 2 hydrate estimate rests on the wrong 1.2 MB figure, and the table's product LCP of 1.8 s (the spinner) understates the problem even though the text explains it.

**Readability.** Report 1 (5): a 4-line glossary, one idea per sentence, a plain verdict, a ranked list, and a business case in rupees. Report 2 (3): the verdict is clear, but the body leans on hydration, GraphQL, Emotion, Brotli, curl, HTTP 206 and raw JSON API calls without explanation.

**Errors and invented claims.** Report 1 (4): the third-party undercount and the resizer guess; otherwise numbers tie out (91 to 201 hours, scenario arithmetic, conversion 0.045%) and it flags its own suspect visits figure. Report 2 (4): the 1.2 MB versus 664 KB slip, "640 px wide (natural 320 by 320)" is muddled, and the community and Medium links could not be checked; the measured numbers are consistent.

## Which report the owner should act on

The owner should act on Report 1 as the plan, with Report 2's diagnosis stapled to it. Report 1 is the one the owner can read, it says what to expect after each week, it puts a rupee value on the work with labelled scenarios, and its one-change-per-release rule with a before-and-after test is what stops the gains being undone. Report 2 is the better engineering: its causes are proven, not inferred, and its cache-pinning finding means Report 1's "re-export the banner as a JPEG" step may not fix the banner. Report 1's biggest miss is waving away 1 MB of tags; Report 2's is having no test plan, rollback, budget or business case. Alone, Report 1 is the one an owner can hold a developer to.

## What each has that the other lacks

Report 1:
1. A 3-week plan with expected numbers per week, a speed budget and Lighthouse CI so the gains stick.
2. A business case in the brand's own figures (₹96.8 lakh in 30 days, 285 orders) with cautious scenarios.
3. Per-fix pass criteria, rollback, risk, feature flags and analytics event checks.

Report 2:
1. Evidence for Rocket Loader (rewritten script types, chunk initiator) and the Email Obfuscation hydration risk, with a 15-minute fix.
2. The Cloudflare cache-pinning explanation for the PNG banner, tested with an AVIF Accept header, and 3 ways to fix it.
3. The true third-party weight (1.05 MB, including a dead Universal Analytics tag and a 102 KB Sign-In library on every page) and the 1.27 s uncached product first byte.

## Which fix list I would hand a developer tomorrow

Report 2's list, in its order, for week 1: fonts, Rocket Loader and Email Obfuscation off, AVIF via Option C, `priority` only on the hero, tag clean-up. Each is under a day and precisely specified. For server rendering, use Report 2's ISR steps with Report 1's verification list (image with high priority in source, 3 products tested, events fire once, layout shift under 0.05, flag and rollback). Add Report 1's skeleton grid, Fix 9 items (GIF spinner and logo, 404 status, /cart) and Fix 10 monitoring, which Report 2 lacks.

## Guess: playbook versus general knowledge

Report 1 was likely written from a specialised playbook, and Report 2 from general knowledge and tools. Report 1 fills the same template for every fix (gain, basis, effort, owner, steps, risk, rollback, depends on) and adds a speed budget, glossary, scenario table and sale-window rules, which read like a checklist being satisfied; Report 2 reasons from raw measurements and cites vendor documentation, which is how an engineer without a script would argue the case.
