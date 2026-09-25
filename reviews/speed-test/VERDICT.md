# Verdict: playbook vs general prompt on the Gehna speed audit

Date: 24 September 2026. Orchestrator: the ecomOS session. Judges: 2 independent agents scoring blind. Arms: Report 1 is agent B (speed playbook, web, Metabase read access; 2 stages). Report 2 is agent A (general prompt, web only; 1 stage). Both on Fable 5.1, same browser instrument, same pages, same day.

## Scores

| | Report 1 (playbook) | Report 2 (general) | Judge's pick | Guessed the playbook arm |
|---|---|---|---|---|
| Judge 1 | 28 / 35 | 27 / 35 | Report 1 for the owner; Report 2 fix list for week 1 | Report 1 (correct) |
| Judge 2 | 28 / 35 | 29 / 35 | Report 2, by a narrow margin | Report 1 (correct) |

## Where the two reports agree

Same homepage LCP (7.9 s on slow 4G), same 2 root causes (a 1.9 MB Korean font set shipped as TTF on every page, and product and collection content rendered only in the browser), same secondary findings (40 below-fold images marked high priority, PNG hero and oversized category icons, layout shift from late content, 30-minute cache on resized images). Same first fix (subset the fonts to Latin WOFF2) with the same estimated gain (home LCP to about 3 s). Two independent runs of the same instrument landing on the same numbers is the strongest result of the test: the measurement layer is trustworthy.

## The 2 factual disputes, settled from the source

1. Does the product page HTML carry the product name and price? Report 1 said no. Report 2 said the title and price are present. I fetched the page: there is no `<h1>` and no visible price anywhere in the HTML; the price sits only inside the Next.js data block. Report 1 is right. Judge 2 docked Report 1 for this, so its accuracy gap is smaller than that score shows.
2. How much third-party script does the homepage load? Report 1 said about 110 KB. Report 2 said 1.05 MB. Both took the number from the browser's Resource Timing API, which reports 0 bytes for most cross-origin files, so both figures are unreliable. I fetched the 19 third-party scripts directly with compression: about 470 KB compressed (gtag 132 KB, Meta pixel 111 KB, Google Sign-In 100 KB, Clarity 26 KB, old Universal Analytics 21 KB, Klaviyo about 60 KB across 9 files). Report 1 undercounted by 4x; Report 2 overcounted by 2x, most likely by using uncompressed sizes. Neither report's fix for this changes, since both already list dropping Universal Analytics, merging the gtag loads and deferring Google Sign-In.

## What each report has that the other lacks

Report 1 (playbook): a pass threshold, a rollback and a dependency for every fix; a week-by-week sequence with the expected metric after each week; a performance budget; a monitoring setup; a business case in rupees from the brand's own 30-day sales; a full checklist audit (19 items, pass or fail with evidence) in the underlying audit file; skeleton grids sized to the real tile dimensions; the cold-resize cost on cache misses (1.5 to 4.2 s); the /cart 404 and the GIF spinner and logo.

Report 2 (general): hard evidence that Cloudflare Rocket Loader holds the site's own JavaScript (rewritten script types, chunk requests initiated by the loader), found first and ranked as fix 2 rather than a late test; the Cloudflare PNG cache-pinning explanation with the AVIF-accept test and 3 concrete cache-rule options; the Google Sign-In library on every page; 3 separate gtag loads; a sharper, shorter read.

## My pick

Report 1 for the owner and the developer, with Report 2's fix 2 (Rocket Loader and Email Obfuscation) moved up to the first week and its Cloudflare cache-rule options pasted into Report 1's fix 8. The reason is not depth of diagnosis, where the two are close and Report 2 is slightly better on the CDN layer. It is that Report 1 is a plan you can run: each fix says what to measure before and after, what number counts as done, what to do if it breaks, and what it depends on. That is what a developer needs on Monday, and it is what the playbook's procedures P1, P29 and P30 forced into the output.

## What the test says about the playbook

1. The playbook did not make the diagnosis better. Both arms found the same problems with the same instrument. On this task, a strong general model with a browser is already a good auditor.
2. The playbook made the output more operable. Verification gates, rollbacks, sequencing, budget, monitoring and a business case all came from playbook procedures, and the general arm produced none of them unprompted.
3. The playbook cost one finding. Report 1 spent effort on checklist coverage and treated Rocket Loader as a test, where Report 2 went straight to the evidence. A checklist can crowd out curiosity. The fix is a playbook line: when JavaScript waits for the load event, check the CDN's script rewriting first.
4. Judges can spot the playbook. Judge 2 guessed the arm from the structure. That is fine for an internal tool and irrelevant to the owner.
5. Both arms shared a measurement bug (Resource Timing zeros on cross-origin files). That belongs in the playbook's P1 as a rule: get third-party sizes from response headers or a direct fetch, never from Resource Timing.

## What to change before the next test

- Add to 08-SPD P1: third-party bytes from headers or direct fetch; and a Rocket Loader and CDN script-rewrite check in the scripts checklist.
- Give the general arm the same 2-stage structure next time, so the test isolates the playbook and not the pipeline.
- Run the same design on a domain where judgement matters more than measurement (offers or ad copy), where the playbook's decision rules should show a bigger gap.
