# Speed — draft playbook

**Status:** source-linked draft; not owner-approved or outcome-tested.

Read [the operating contract](../OPERATING_CONTRACT.md) before using a workflow.

## Inputs
- Important URLs/templates
- device mix
- field/lab measurements
- app/script inventory

## Measures
- Field loading/responsiveness/stability metrics
- checkout regression

## Foundation candidates
Inferred principle labels do not establish universal applicability. Retain source conditions; empty means no matched labelled principle, not absence of foundational knowledge.

- **Setting Speed Targets by Page and Store Type** (`b147e14a22ec3685cbfc7fe3`): Practical performance targets for ecommerce pages, combining load-time goals, PageSpeed scores and Core Web Vitals thresholds.
  Applies when: You are defining acceptance criteria for a store build, theme change or app install and need concrete speed targets to test against.
  Condition: The three-second and two-second load targets and 90+ score band are source heuristics; 'two seconds or less' is described as a competitive-performance aspiration rather than a threshold with measured lift.
  Condition: PageSpeed scores fluctuate with lab conditions, so use CWV metrics as the more stable signal.

- **Two Root Causes of Slow Shopify Stores: Layout Stability and Apps** (`7678b95c31ff1fdbee1c0019`): Prioritize speed work around CLS/LCP layout stability and third-party app scripts that load with your theme.
  Applies when: Diagnosing slow mobile load times or deciding where to spend speed-optimization effort on a Shopify store.
  Condition: App lazy-loading may break apps that genuinely need to run immediately; verify each app after changing its loading.

- **Prioritize speed fixes by financial impact and conversion benchmarks** (`b36e60f619f77cc137537723`): Maps ecommerce speed benchmarks and revenue math to help operators justify and sequence performance work.
  Applies when: Deciding whether to invest engineering time in site speed, or building a business case for a performance sprint before a peak sales period.
  Condition: Conversion and financial figures are cited from third-party studies and vendor examples; they are illustrative, not guarantees for your store.
  Condition: Some cited statistics appear contradictory (e.g. 'millisecond improvement' vs '0.1 second improvement' at 8.4%), so treat the direction of the effect as the takeaway, not the exact number.
  Condition: Benchmark numbers should never be treated as a universal rule; measure your own baseline before and after changes.

## Diagnose storefront speed problems
Workflow ID: `speed.diagnose-speed`

**Deliverable:** Speed diagnosis and ranked fixes

### Proposed decision sequence
1. Select important templates and separate mobile from desktop
2. Distinguish field experience from lab diagnostics
3. Prioritise observed bottlenecks rather than assumed revenue lifts

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Map LCP, FCP, TTI and TBT to What Shoppers Actually Experience
Card: `0e11008fda404dbea1997411` · Source: Page Speed Optimization_ How to Improve the Loading Time of Your Online Shop.docx · Section: 0

Translate the four Core Web Vitals-adjacent metrics into shopper-visible moments so speed work targets the metric that blocks browsing and buying.

Applies when: Interpreting a speed report and choosing whether to fix first paint, interactivity or main-content load on category and product pages.

- Read First Contentful Paint (FCP) as when the first visible element — a heading, a product image — appears.
- Read Time to Interactive (TTI) as when the page becomes usable, i.e. the shopper can actually click and buy.
- Read Total Blocking Time (TBT) as the elapsed time between FCP and TTI — in practice the window where the page looks ready but ignores taps on filters, variants or add-to-cart.
- Read Largest Contentful Paint (LCP) as when the main content is fully loaded from the user's point of view, which on a PDP is typically the hero product image.
- Combine: a fast FCP with a long FCP-to-TTI gap tells you scripts are blocking interaction, whereas a slow LCP points at the heavyweight primary image or hero asset.
- **Condition:** TBT as 'time between FCP and TTI' is the source's definition; some tooling calculates TBT from long tasks, so confirm the definition used in your current report before quoting a number.

#### Follow the Speed Work Order: Defer, Lazy-Load Apps, Fix CLS, Fix LCP
Card: `dca8734ae894714e539b5fcb` · Source: Page speed.docx · Section: 5

Apply speed fixes in the order the source demonstrates: add defer where needed, lazy-load app scripts, resolve layout shift, then correct eager/lazy image loading.

Applies when: Working a Shopify mobile speed score up systematically toward and past 50.

- Start by adding defer to render-blocking scripts in theme.liquid where apps tolerate it.
- Then lazy-load app scripts via the content_for_header override and per-app embed technique.
- Then hunt and fix CLS by throttled inspection and correcting offending inline CSS.
- Then fix LCP by making first in-view images eager while keeping others lazy.
- Retest three times after each stage and average, allowing a couple of minutes for changes to propagate.
- Source's documented progression on a real store: about 33 to over 50 mobile; app-script lazy-loading alone was credited with roughly 10-15% improvement when apps were the bottleneck.
- Use the outcome as directional — the same sequence won't produce identical numbers on a different store.
- **Condition:** Results are a single-account case study, not a guaranteed benchmark.
- **Condition:** If apps aren't your bottleneck, the lazy-load step may be far less effective, as the source itself cautions.

#### Core Web Vitals Thresholds and What Each Metric Means for Your Store
Card: `2969a152a99dbaea19ffbc71` · Source: Ecommerce Site Speed Optimization_ Complete Guide for 2026.docx · Section: 0

Plain definitions and target thresholds for LCP, INP and CLS, mapped to the specific ecommerce elements (hero images, add-to-cart clicks, cookie banners) that drive each metric.

Applies when: You are diagnosing why a product, category or homepage scores poorly and need to know which CWV metric each page element is hurting.

- LCP (Largest Contentful Paint) measures how fast the largest visible element loads — usually the main product image on a PDP or the hero banner/first product grid on a category page. Target is under 2.5 seconds; over 4 seconds is rated 'poor'. Fix via image optimization and faster server response.
- INP (Interaction to Next Paint) replaced First Input Delay and measures responsiveness to clicks, taps and filters. Target is under 200 milliseconds. Ecommerce sites fail INP because of heavy JavaScript from apps, plugins and tracking scripts — the classic symptom is a customer clicking Add to Cart and nothing happening for half a second.
- CLS (Cumulative Layout Shift) measures visual stability; target is under 0.1. Common ecommerce causes are late-loading images without defined dimensions, dynamically injected content like cookie banners, and font loading that reflows text. Reserve space and set explicit dimensions.
- Diagnose per page type: PDP main image drives LCP, review/variant/BNPL JavaScript drives INP, and the hero image or rotating carousel drives homepage LCP.
- Prioritize fixes on the pages with the most traffic times the most revenue impact — a smaller gain on a high-traffic page beats a bigger gain on a rarely visited page.
- **Condition:** Google uses Core Web Vitals as a ranking tie-breaker; content relevance remains the primary factor, so speed alone will not outrank better content.
- **Condition:** Approximately 50% of mobile sites fail the CWV assessment per HTTP Archive cited in the source — passing is a competitive advantage, not the norm.

### Retrieval and applicability
Search: `mobile page speed core web vitals scripts images`
Related domains: store-setup, testing, measurement
Mixed-folder candidate IDs: 3412220fa6466ce136241e08, 48f063960d409da4e59978cf, bd778e96d24fbd03dc4967e6

- Does this advice fit the product lifecycle, market, audience and requested deliverable?
- Does it require proof, access, budget or assets the brand does not have?
- Does it change a fixed price, offer, policy or other explicit constraint?
- Are platform details or numerical claims current and substantiated?

### Output checks
- Deliver the specified artifact, not general advice about creating it.
- Use supplied brand facts; label hypotheses and missing inputs separately.
- Preserve relevant source conditions; do not copy another business’s proof or results.
- Include an owner, measurement and decision rule when proposing a test.
- Check the output against the requested constraints and owner feedback.

Stop after the requested artifact passes factual and brief checks; allow at most two revision passes, then report the unresolved issue.

## Plan a safe speed improvement
Workflow ID: `speed.plan-speed-fix`

**Deliverable:** Technical change brief and rollback checks

### Proposed decision sequence
1. Trace the costly asset or script and its business purpose
2. Specify the smallest reversible optimisation
3. Verify measurement plus cart, checkout and analytics regressions

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Reduce Page Weight and Third-Party Script Load to Cut Load Time
Card: `a62896aba3d86679456a34ef` · Source: 93 powerful statistics that show why your ecommerce site speed matters in 2026.docx · Section: 0

Compression and script discipline are constrained by known page-weight and script-cost figures you can plan against.

Applies when: You are deciding whether to prune scripts or compress media as part of a speed budget for PDPs and landing pages.

- Count third-party scripts and treat each as a cost: every third-party script adds an average of 34.1 milliseconds to load time, so removing or deferring a handful compounds.
- Target compression of images and text: 25% of pages could save more than 250kb, and 10% could save more than 1mb from this alone.
- Note that large pages take 318% longer to visually load than small pages, making page weight a first-order lever for visual speed.
- Recognize the trade-off shoppers accept: half of users would give up animation and video for faster loads, so heavy hero media is a candidate for trimming.
- Connect speed to revenue: the source cites Yahoo gaining 9% traffic from a 0.4-second speedup and the BBC losing ~10% of users per extra second, as directional evidence that even small gains matter.
- **Condition:** Method details for the page-weight and third-party-script figures are not given in the source; use them as planning approximations.
- **Condition:** The Yahoo and BBC results are single-company anecdotes, not generalizable benchmarks.

#### Where ecommerce stores lose speed: five common killers
Card: `3d795cd17d4b9c2f9133c28b` · Source: Page speed guide for ecommerce store operators_ diagnosis and actions.docx · Section: 0

The recurring causes of slow storefronts — images, third-party scripts, plugins, missing caching, and unused CSS/JS.

Applies when: Running a speed audit on a live store to decide which fix class will recover the most seconds.

- Unoptimized images: high-resolution product photos are needed for sales, but PNG/JPEG inflate page weight. Modern formats (WebP/AVIF) cut file size 30–50% at the same quality. Images can make up more than 60% of a page's total data volume, making them the biggest lever.
- Third-party scripts: tracking pixels, chat widgets, review platforms and social embeds each load their own JavaScript and block rendering. In many stores these external requests account for more than 50% of total load time.
- Plugins: every app or plugin loads its own stylesheets and scripts. Especially harmful are plugins that run complex database queries on every page load without caching results.
- Missing caching: without it, the server rebuilds each page on every click — querying databases, calculating prices, assembling layouts. Full-page caching instead serves a pre-rendered version, sharply cutting response times.
- Site-wide CSS/JS: many themes load functionality on every page even when only one subpage needs it, so mobile browsers download and process unused code.
- **Condition:** The >50% script share and >60% image data share are source-reported typical figures, not fixed proportions in every store; confirm with your own audit.
- **Condition:** Do not remove review, chat or tracking scripts purely on speed grounds without checking their revenue or operational role.

#### Speed Fix Priority Ladder: Images, Scripts, Hosting
Card: `c35b62b838606057963903bf` · Source: Ecommerce Site Speed Optimization_ Complete Guide for 2026.docx · Section: 0

A prioritized three-step order for ecommerce speed work: compress images to WebP, cut unused third-party apps/scripts, then upgrade hosting and add a CDN.

Applies when: You are deciding where to spend limited dev or app budget on store speed and need the highest-impact fixes first.

- Start with images: compress and convert product photos, category banners and promo graphics to WebP. The source claims this single change often cuts page weight by 40-60% with minimal technical effort, so it is the best return before touching code.
- Second, audit third-party scripts: review every installed app, plugin, chat widget, review tool and analytics tag and remove ones not actively used. Each script runs on every page load and competes for browser resources.
- Third, address infrastructure: if you are on shared hosting with meaningful traffic, move to a VPS or cloud hosting, and add a CDN if you serve customers across multiple regions.
- Only after these three foundations are handled should you spend effort on JavaScript minification, code splitting or fine-tuning cache headers — the source treats those as later-order work.
- Note that the source ties the whole ladder to conversion: a 0.1-second load-time improvement can increase retail conversions by up to 8.4% (Google/NitroPack), so frame speed work as revenue work, not just a technical score.
- **Condition:** The 40-60% page-weight reduction and 8.4% conversion lift are source-cited research figures, not guarantees for your store; measure your own before/after.
- **Condition:** Hosting upgrade thresholds and budget tradeoffs depend on order volume — see the hosting-by-store-size card.

### Retrieval and applicability
Search: `page weight third party script image loading performance`
Related domains: store-setup, testing, measurement
Mixed-folder candidate IDs: c049a4fab120c6557f696531, ba82a65b35b4274277febfee, 5de99742a3a07b09d36a6a7f

- Does this advice fit the product lifecycle, market, audience and requested deliverable?
- Does it require proof, access, budget or assets the brand does not have?
- Does it change a fixed price, offer, policy or other explicit constraint?
- Are platform details or numerical claims current and substantiated?

### Output checks
- Deliver the specified artifact, not general advice about creating it.
- Use supplied brand facts; label hypotheses and missing inputs separately.
- Preserve relevant source conditions; do not copy another business’s proof or results.
- Include an owner, measurement and decision rule when proposing a test.
- Check the output against the requested constraints and owner feedback.

Stop after the requested artifact passes factual and brief checks; allow at most two revision passes, then report the unresolved issue.

## Define a storefront performance budget
Workflow ID: `speed.monitor-speed`

**Deliverable:** Performance monitoring specification

### Proposed decision sequence
1. Record a representative baseline and measurement conditions
2. Set explicit owner-approved budgets and alert criteria
3. Compare after changes and investigate regressions

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Adopt Google Core Web Vitals Thresholds as Speed Targets
Card: `4c4de77e3eaedda872e4e9e8` · Source: 93 powerful statistics that show why your ecommerce site speed matters in 2026.docx · Section: 0

Set TTFB, FID and FCP targets from source-cited Google benchmarks and check current averages before optimizing.

Applies when: You are setting performance budgets or audit criteria for PDP, category and landing page templates and need concrete numbers.

- Use Google's recommended thresholds as the pass line: TTFB under 800ms, FID under 100ms, and FCP under 1.8 seconds.
- Compare against reported averages to see how much room exists: average TTFB is about 1.286s desktop and 2.594s mobile; average FID is ~12.73ms desktop and ~59.73ms mobile.
- Recognize that 'fully loaded' is a different, much larger figure than FCP: average full load is 10.3 seconds desktop and 27.3 seconds mobile, so don't confuse interactive/usable states with paint times.
- Check scores with Google's PageSpeed Insights (verify current interface), as the source did, which brought one homepage's FCP to 0.8 seconds.
- Route fixes to the right owner: perceived-speed and benchmark work here, technical implementation (minification, image compression, lazy loading) to the technical execution workstream.
- **Condition:** FID has been superseded in Google's current Core Web Vitals program (INP now captures interaction responsiveness); verify the current metric set before committing targets.
- **Condition:** These are Google recommendation thresholds, not store-specific targets; derive your own from template and device-mix data.

#### Continuous Performance Monitoring and Budgets
Card: `9ffe9f981c5709c0f243cd4c` · Source: Ecommerce Site Speed Optimization_ Complete Guide for 2026.docx · Section: 0

Set up recurring speed monitoring and a performance budget so stores don't degrade silently as apps, products and tracking scripts accumulate.

Applies when: You are setting store speed governance — deciding test cadence, alerting and limits on page weight or third-party scripts.

- Adopt a monitoring cadence: test at minimum monthly to catch gradual degradation, and test immediately after installing apps, changing themes or making site-wide updates.
- Before major sales events, run speed audits to confirm the site can handle increased traffic smoothly.
- Set up automated monitoring rather than manual tests: free options include PageSpeed Insights API with scheduled runs, GTmetrix monitoring (with account) and Lighthouse CI for automated testing during deployments. Paid services like DebugBear, SpeedCurve and Calibre add tracking, alerting and historical analysis.
- Define a performance budget as a guardrail: maximum page weight, minimum speed scores and maximum third-party script count. Review any change that exceeds the limits before approving it — without defined limits, performance degrades gradually.
- Run targeted tests after app installs specifically, since each app runs code on every page and cumulative additions are the main cause of silent slowdown.
- **Condition:** Paid monitoring tools are a cost that the source argues pays off for revenue-critical stores, but ROI depends on store scale.
- **Condition:** Performance budgets are only useful if enforcement is built into the release or approval process, not just documented.

#### Baseline first: measuring speed before you change anything
Card: `6012d71fccb634a29e692e85` · Source: Page speed guide for ecommerce store operators_ diagnosis and actions.docx · Section: 0

Establish a documented before-state with PageSpeed Insights on mobile and desktop so each optimisation can be attributed.

Applies when: Starting any speed project on a store, or when you need evidence that a technical change actually helped.

- Run Google PageSpeed Insights for your URL on both mobile and desktop before touching anything, since mobile and desktop scores diverge and your mobile traffic is the larger revenue share.
- Record the LCP value (and other CWV values) plus the overall score for each template you care about — homepage, key category pages, best-selling PDPs, cart and checkout.
- Keep a dated change log in plain text, e.g. 'March 15 – image compression enabled', so you can tie observed metric shifts to specific actions instead of arguing about causes.
- Repeat the same measurements after each change class (images, plugins, caching) rather than bundling everything, so you can tell which lever produced which gain and roll back anything that regresses.
- Use the before/after numbers as the internal evidence for continuing or stopping further investment in speed work.
- **Condition:** PageSpeed Insights is Google's tool and its interface and scoring can change — verify current reports when you run it.
- **Condition:** Lab scores do not equal real-user field data; treat them as directional for prioritisation.

### Retrieval and applicability
Search: `performance budget monitoring mobile templates`
Related domains: store-setup, testing, measurement
Mixed-folder candidate IDs: 48f063960d409da4e59978cf, 50032f16a8cf75faea1b48cd, 1067951c3e42f2b344ca8de5

- Does this advice fit the product lifecycle, market, audience and requested deliverable?
- Does it require proof, access, budget or assets the brand does not have?
- Does it change a fixed price, offer, policy or other explicit constraint?
- Are platform details or numerical claims current and substantiated?

### Output checks
- Deliver the specified artifact, not general advice about creating it.
- Use supplied brand facts; label hypotheses and missing inputs separately.
- Preserve relevant source conditions; do not copy another business’s proof or results.
- Include an owner, measurement and decision rule when proposing a test.
- Check the output against the requested constraints and owner feedback.

Stop after the requested artifact passes factual and brief checks; allow at most two revision passes, then report the unresolved issue.
