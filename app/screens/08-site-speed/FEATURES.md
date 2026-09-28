# Site and speed: features

Status: todo | doing | done | parked. One feature per commit. The first round is the skeleton; after that, features come in rounds of 10, stack-ranked by revenue impact, usefulness and how easy they are to build on dummy data.

## Round 0: skeleton

| # | Feature | Status |
|---|---|---|
| 0.1 | Page shell in the shared UI kit: simulated banner, founder note, sections, decision row (SITE-C21) | done |
| 0.2 | `api.py` (`overview`, `findings`) over `audit.build`, speed medians through `app/metrics.py`, unavailable states | done |
| 0.3 | 3 tiles (slowest mobile LCP, page weight, cost of slowness), 2 insights as rules (page over LCP target on mobile, outside script over 100 KB), 1 chart (LCP by page, to scale, target line) | done |
| 0.4 | Per-page table (median load, LCP, first paint, weight, requests by device), fix chain with expected ms saved and evidence run, developer brief stub per fix (SITE-C32), filmstrip on the slowest page (kit `UI.filmstrip`, frames drawn from timings), script inventory from brain stack records | done |
| 0.5 | `audit.py`: SPEED-R01 slow mobile pages, SPEED-R02 heavy outside script (money when blocking), SPEED-R03 image weight (unavailable) | done |

Round 0 notes (28 Sep 2026, S3.12):
- The bombas `speed_runs` fixture keeps the device in `variant` and has no `measured_at`, so `metrics.py` reads it as unavailable. `audit.SpeedData` reads it as device = variant, variant = baseline, measured_at = the last full day, and the page says so. A contract session should fix the fixture shape in `generate.py`.
- Script weights are a screen fixture (`fixtures/script_log.json`, simulated, shaped like `speed_request_log`); vendor names come from `bombas.stack.*` brain records.
- Cost of slowness uses an assumption stated on the page: 7 percent of orders lost per second of LCP over 2.5 s. It is not a Bombas measurement; `brand_economics.measured_conversion_loss_per_second` replaces it.
- The audit contract has no `script` entity type; SPEED-R02 uses `metric` with id `script_bytes.<field>`. Propose a `script` type in a contract session.
- Sessions by page are not in the data, so the money uses all mobile sessions and the median page gap.

## Jobs to be done (room "Site and speed")

| Job | Question | Capability |
|---|---|---|
| find why a page is slow and what it is costing in dollars | why is my page slow and what is it costing me | SITE-C21 |
| cut image weight without hurting quality | which images are too big and how do I fix them | SITE-C22 |
| defer or remove scripts that block the page | which scripts are slowing this page down and can they wait | SITE-C23 |
| fix font loading | why do fonts delay the page and how much do they weigh | SITE-C24 |
| stop the page jumping while it loads | what is causing layout shift and on which template | SITE-C25 |
| fix the largest paint element | what is the LCP element on each template and what fixes it | SITE-C26 |
| make add-to-cart, filters and search feel instant | which tap or click feels slow and why | SITE-C27 |
| confirm caching and CDN are actually working | are my pages cached and served from the CDN or not | SITE-C28 |
| get ready for a sale-day traffic spike | will the site hold up on Black Friday, Cyber Monday or another big sale day | SITE-C29 |
| cut and reorganize code weight | how much CSS and JS can be removed, split or inlined | SITE-C30 |
| speed-tune a headless or custom storefront | what is slow in our own framework code, not the platform's | SITE-C31 |
| hand a developer a brief they can execute without guessing | what exactly should the developer change, and how do we know it worked | SITE-C32 |
| catch a speed regression before it reaches customers | did the last deploy or app install make the site slower | SITE-C33 |
| pick a landing-page build method that will not wreck speed | will this new page-builder page load fast enough to run ads to | SITE-C61 |

## Candidates from the room spec (pick 10 per round)

### Questions this screen should answer

- why is my page slow and what is it costing me  (SITE-C21)
- which images are too big and how do I fix them  (SITE-C22)
- which scripts are slowing this page down and can they wait  (SITE-C23)
- why do fonts delay the page and how much do they weigh  (SITE-C24)
- what is causing layout shift and on which template  (SITE-C25)
- what is the LCP element on each template and what fixes it  (SITE-C26)
- which tap or click feels slow and why  (SITE-C27)
- are my pages cached and served from the CDN or not  (SITE-C28)
- will the site hold up on Black Friday, Cyber Monday or another big sale day (or a festive sale day in India)  (SITE-C29)
- how much CSS and JS can be removed, split or inlined  (SITE-C30)
- what is slow in our own framework code, not the platform's  (SITE-C31)
- what exactly should the developer change, and how do we know it worked  (SITE-C32)
- did the last deploy or app install make the site slower  (SITE-C33)
- will this new page-builder page load fast enough to run ads to  (SITE-C61)

### Metrics specified

- `fully_loaded_mobile`: how long the page takes to be usable on a slow phone. median load_ms of 3 throttled runs (slow 4G, 4x CPU, Pixel 5 profile)
- `lcp_ms`: when the biggest visible thing on the page shows up. median LCP from the PerformanceObserver, largest-contentful-paint entry
- `fcp_ms`: when the first bit of the page appears. median first-contentful-paint entry across 3 runs
- `cls`: how much the page jumps while loading. sum of layout-shift entry values with no recent input, median of 3 runs
- `tbt_est_ms`: how long the page ignores taps and clicks while it loads. sum of (long task duration minus 50 ms) for long tasks over 50 ms, median of 3 runs
- `wire_bytes`: total data the page sends on one visit. sum of transferSize across every resource, median of 3 runs
- `first_party_vs_third_party_bytes`: how much weight is the brand's own code versus outside scripts. split wire_bytes by request host: brand domain and CDN of record versus everything else
- `requests_served`: how many separate files the page has to fetch. count of resource timing entries
- `console_errors_count`: how many script errors happen while the page loads. count of console error and page error events during the run
- `script_count_by_route`: how many scripts load from theme code, apps, tag manager and hardcoded tags. count distinct script src grouped by known route (theme bundle, app embed, GTM container, inline)
- `page_weight_budget_status`: pass or fail against the weight and script-count ceiling the brand agreed to. compare wire_bytes and requests_served on the latest run against the stored budget for that page type
- `cost_of_slowness_inr_per_month`: how much money the current load time is estimated to cost every month. (current LCP minus target LCP in seconds) x brand's own measured conversion-loss-per-second x monthly sessions on that page x average order value
- `regression_delta_pct`: how much slower or faster the site got since the last shipped baseline. (latest run load_ms minus last-shipped baseline load_ms) divided by baseline load_ms
- `days_since_last_speed_run`: how old the numbers on this page are. today minus the measured_at date of the latest run for that page

### Insights specified (rules in code)

- unused fonts: a font file is requested but 0 glyphs from it render on the page → "{n} font files nobody sees cost {kb} KB on every visit" (action SITE-C24)
- third-party scripts over budget: script_count_by_route for third-party routes exceeds the page's stored script budget → "{n} outside scripts add {ms} ms and {kb} KB, over your budget of {budget}" (action SITE-C23)
- speed regression since last ship: regression_delta_pct worse than 10 percent since the last recorded baseline → "the page got {pct}% slower since the last check on {date}, likely from {suspect_change}" (action SITE-C33)
- LCP element still un-lazied or animated: the element flagged as the LCP source has loading=lazy, an active CSS animation, or is not preloaded → "the {element} that decides how fast the page feels is still {problem}" (action SITE-C26)
- layout shift culprit: a single element accounts for over half of total CLS on a template → "{element} on the {template} page causes most of the jumping; it has no reserved space" (action SITE-C25)
- render-blocking code still present: a CSS or JS resource has renderBlockingStatus blocking and is not marked async or deferred → "{n} files still block the page from showing anything until they arrive" (action SITE-C30)
- dead analytics tag still firing: a request matches a known sunset tracking endpoint (for example old Universal Analytics) → "a tag that stopped working on {sunset_date} still loads and costs {kb} KB" (action SITE-C23)
- app adds weight with no clear revenue link: an app's script bytes rank in the top 5 by weight and the app inventory (SITE-C13) shows no attributed revenue → "{app} adds {kb} KB on every page and nothing in your sales data ties back to it" (action SITE-C13)
- font variation count too high: more than 2 weights or styles of the same font family are loaded → "{n} versions of {family} load when the page only uses {used}" (action SITE-C24)
- cache headers missing on static assets: a static asset (image, font, script, css) returns a cache-control max-age under 1 week or no cache-control header → "{n} static files are re-downloaded on every visit because caching is not set" (action SITE-C28)
- no CDN detected on a key page: response headers show no CDN-identifying header (for example cf-ray, x-served-by) on a page expected to run through one → "{page} is not being served through the CDN; every visit hits the origin" (action SITE-C28)
- dynamic step untested for peak load: a page depends on search, personalization or a live stock check and has no load-test result on file within 60 days of the next known sale date → "{feature} has never been tested under sale-day traffic and the next big sale is in {days} days" (action SITE-C29)
- main-thread block on a key interaction: a long task over 200 ms overlaps the time window of a tap test on add-to-cart, variant picker, filter or search → "tapping {interaction} freezes the page for about {ms} ms" (action SITE-C27)
- page-weight budget breached by latest deploy: page_weight_budget_status is fail on the most recent scheduled or pre-deploy check → "the last deploy pushed {page} to {kb} KB, over its {budget} KB budget" (action SITE-C33)
- new page-builder page is heavy before it ships: a page built with an app page-builder measures over the page-type budget on its own pre-launch run → "the new {page} page weighs {kb} KB before it even goes live, {pct}% over budget" (action SITE-C61)

### Visuals specified

- fix chain (step chart): load time after each fix, cumulative, in shipping order
- before and after filmstrip (frame strip): screenshots at fixed time steps, baseline versus the fixed page
- request waterfall by party (waterfall chart): every request, colored first-party versus third-party, ordered by start time
- page-weight budget trend (line chart with a budget line): page weight and script count at every deploy or scheduled check against the stored budget
- script inventory table (sortable table): every script, its route, weight, blocking status and whether revenue ties back to it
- cost of slowness bar (bar chart): estimated monthly dollars lost at current LCP versus at target LCP, for the pages that carry the most traffic
- sale-readiness checklist (step chart or checklist with pass/fail dots): each dynamic feature, its last load-test result and days left to the next sale

### Not in the usual tools

- measures a real before-and-after per fix on a mirrored copy of the live page, with a filmstrip
- one Lighthouse-style score is replaced with a fix-by-fix chain a founder can stop trusting or not, item by item
- cross-references every heavy script against the brand's own revenue attribution before calling it dead weight
- turns a diagnosed fix straight into a brief with a pass threshold and a rollback plan, ready for a developer
- prices slowness in the brand's own dollars per month, not a generic industry percentage
- regression checks point back to the exact fix chain and filmstrip already on file, so a regression names its own cause

### Data this screen needs

- `speed_runs`: brand, page, variant, run, load_ms, lcp_ms, fcp_ms, cls, tbt_est_ms, bytes (speed_lab.measure)
- `speed_request_log`: run_id, url, host, party, type, transfer_size, render_blocking_status, cache_control (speed_lab.measure)
- `app_inventory`: app_id, name, monthly_cost, revenue_attributed, script_bytes, install_date, owner (SITE-C13 app audit (manual entry until a platform API is connected))
- `page_weight_budgets`: page_type, max_bytes, max_requests, set_by, set_at (founder-set, stored by the regression monitor)
- `sale_calendar`: event_name, start_date, end_date, expected_traffic_multiple (manual entry from the brand's marketing calendar)
- `brand_economics`: page, sessions_30d, conversion_rate, average_order_value, measured_conversion_loss_per_second (Metabase pull plus a one-time speed-versus-conversion study per brand)

## Rounds

| Round | Features picked | Date | Notes |
|---|---|---|---|
| 0 | 0.1 to 0.5 | 2026-09-28 | Bombas simulated data, scale 0.1; screenshot `round0.png` |
