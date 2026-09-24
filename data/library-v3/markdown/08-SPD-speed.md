## Build the Business Case for Speed with Conversion and Bounce Benchmarks
Use when: You need to prioritize a speed initiative against other roadmap items and must translate load time into revenue impact for merchandising, PDP or category page work.
- Anchor the case on source-cited conversion effects: a 1-second reduction in load time correlates with roughly a 5.6% conversion increase and nearly a 12% bounce-rate decrease. Mobile-specific figures are slightly different (1-second improvement associated with ~5.9% conversion lift and ~9% bounce reduction), so use the mobile set when the business is mobile-heavy.
- Frame the failure thresholds shoppers abandon at: 40% leave after 3 seconds, 63% bounce past 4 seconds, and roughly two-thirds leave at 6 seconds. For page views, 2-second pages average 8.9 pages per session versus 3.3 pages at 8 seconds.
- Illustrate with concrete own-store arithmetic rather than generic percentages: daily sessions x conversion rate x AOV gives current daily revenue; recompute with the improved conversion rate to size the annualized gain.
- Note that the source's $1.8M/$5.5M example assumes 50,000 daily visitors, 3.5% conversion and $50 AOV with a 6-second average load; treat it as a worked example, not a forecast, and re-run with your own traffic and margin.
- Pair revenue upside with ranking and loyalty effects (fast sites appear higher in results; 65% trust a business less after a problem) so the case isn't purely conversion-based.
Caveat: Conversion lift figures are observed correlations across studies, not guaranteed causal outcomes for every store; your mileage will vary by traffic quality, device mix and catalog.
Caveat: Do not present the source's hypothetical revenue scenario as your store's expected result.

Tags: speed, measurement, conversion-optimization, product-page, analytics, business-case
Source: 93 powerful statistics that show why your ecommerce site speed matters in 2026.docx

---

## Adopt Google Core Web Vitals Thresholds as Speed Targets
Use when: You are setting performance budgets or audit criteria for PDP, category and landing page templates and need concrete numbers.
- Use Google's recommended thresholds as the pass line: TTFB under 800ms, FID under 100ms, and FCP under 1.8 seconds.
- Compare against reported averages to see how much room exists: average TTFB is about 1.286s desktop and 2.594s mobile; average FID is ~12.73ms desktop and ~59.73ms mobile.
- Recognize that 'fully loaded' is a different, much larger figure than FCP: average full load is 10.3 seconds desktop and 27.3 seconds mobile, so don't confuse interactive/usable states with paint times.
- Check scores with Google's PageSpeed Insights (verify current interface), as the source did, which brought one homepage's FCP to 0.8 seconds.
- Route fixes to the right owner: perceived-speed and benchmark work here, technical implementation (minification, image compression, lazy loading) to the technical execution workstream.
Caveat: FID has been superseded in Google's current Core Web Vitals program (INP now captures interaction responsiveness); verify the current metric set before committing targets.
Caveat: These are Google recommendation thresholds, not store-specific targets; derive your own from template and device-mix data.

Tags: speed, core-web-vitals, measurement, performance-budget, technical-seo, product-page
Source: 93 powerful statistics that show why your ecommerce site speed matters in 2026.docx

---

## Prioritize the Product and Category Templates Most Shopper Time Spends On
Use when: You must decide which templates to make faster first with limited engineering capacity.
- Focus first on PDP and category templates because they account for 72% of page views in the shopper journey, maximizing the speed benefit per fix.
- Set a concrete target using the source comparison: unoptimized PDPs average 6.1 seconds, optimized ones average 4.1 seconds — a full 2 seconds faster.
- Quantify the journey-level time saved: with retail's high 5.01 pages per session on desktop, optimized sites save about 23 seconds per shopper journey. That compounds across the funnel.
- Treat mobile PDPs as the highest-value target since mobile is ~59% of traffic and pages load 87.8% longer on mobile than desktop on average.
- Track pages per session and bounce as secondary KPIs alongside conversion so you capture engagement, not just orders.
Caveat: Figures are industry averages reported in the source; benchmark your own templates before assuming the same gap.
Caveat: Time-saved estimates depend on your pages-per-session figure, which varies by catalog and traffic source.

Tags: speed, product-page, merchandising, prioritization, mobile, measurement
Source: 93 powerful statistics that show why your ecommerce site speed matters in 2026.docx

---

## Diagnose and Prepare for IT Brownouts During High-Traffic Sales
Use when: You are planning a flash sale, Black Friday event or product drop and need to protect cart, checkout and login reliability.
- Understand brownouts: traffic-induced slowdowns or errors in dynamic areas like add-to-cart, site search and login — not a full outage. They show up as laggy or broken funnel steps during spikes.
- Use the Pet Smart Black Friday case as a pattern to plan against: load speed nearly doubled from 7.7s to 13.84s under peak traffic. Test your own peak-load behavior before the event, not during it.
- Expect brownouts to be common: 50% of ecommerce consumers report slowdowns during high-traffic occasions, and 82% of those couldn't access the target site at all.
- Deploy virtual waiting rooms for limited-inventory events: the source cites 87% of consumers preferring a short queue over a slow/buggy site, 84% preferring a queue to a crash page, and willingness to wait an average of 53 minutes for limited-inventory sales.
- Map high-risk funnel steps (cart, checkout, login, search) and define degradation behavior — queue, throttle or static fallback — before traffic hits.
- Account for business cost: organizations with frequent outages/brownouts face up to 16x higher costs, and 31% of IT professionals report brand damage and 30% report stock-price impact from these events.
Caveat: Queueing trades immediate access for reliability; it is best suited to genuinely high-demand events or limited inventory, not everyday traffic.
Caveat: The willingness-to-wait and preference percentages are survey opinions from the source, useful for planning rationale but not guarantees of shopper behavior.
Caveat: Server architecture and load-balancer work belongs with the infrastructure owner, not this playbook.

Tags: speed, checkout, cart, high-traffic, brownout, queueing, conversion-optimization
Source: 93 powerful statistics that show why your ecommerce site speed matters in 2026.docx

---

## Set Mobile-Specific Speed Standards Separate from Desktop
Use when: You are auditing storefront performance or setting pass/fail thresholds for a mobile-first audience.
- Treat mobile as the primary performance surface: ~59% of web traffic is mobile, and pages take 87.8% longer to load on mobile on average.
- Set abandonment-aware thresholds: 53% of mobile visitors leave past 3 seconds, 64% expect under 4 seconds, and 74% abandon past 5 seconds.
- Compare mobile against desktop honestly: mobile bounce averages 56.8% versus 50% on desktop, and mobile users' top complaint (46%) is waiting for pages to load.
- Account for the perception gap: 85% of mobile users expect pages to load as fast or faster than desktop, which almost never happens, so perceived mobile speed is a loyalty lever (95% of mobile users return to a fast site vs. 62% for a slow one).
- Use mobile-specific conversion figures (1-second mobile improvement ~5.9% conversion lift) when valuing mobile work.
- Watch the source's caveat that mobile sites average much worse load times, so desktop-only testing understates the real shopper experience.
Caveat: Average mobile load times cited (up to ~15 seconds for some measures, 27.3s full load) are industry averages and will differ substantially by storefront.
Caveat: Do not apply desktop benchmarks to mobile passes; use separate mobile targets.

Tags: speed, mobile, benchmarks, bounce-rate, conversion-optimization, measurement
Source: 93 powerful statistics that show why your ecommerce site speed matters in 2026.docx

---

## Reduce Page Weight and Third-Party Script Load to Cut Load Time
Use when: You are deciding whether to prune scripts or compress media as part of a speed budget for PDPs and landing pages.
- Count third-party scripts and treat each as a cost: every third-party script adds an average of 34.1 milliseconds to load time, so removing or deferring a handful compounds.
- Target compression of images and text: 25% of pages could save more than 250kb, and 10% could save more than 1mb from this alone.
- Note that large pages take 318% longer to visually load than small pages, making page weight a first-order lever for visual speed.
- Recognize the trade-off shoppers accept: half of users would give up animation and video for faster loads, so heavy hero media is a candidate for trimming.
- Connect speed to revenue: the source cites Yahoo gaining 9% traffic from a 0.4-second speedup and the BBC losing ~10% of users per extra second, as directional evidence that even small gains matter.
Caveat: Method details for the page-weight and third-party-script figures are not given in the source; use them as planning approximations.
Caveat: The Yahoo and BBC results are single-company anecdotes, not generalizable benchmarks.

Tags: speed, page-weight, third-party-scripts, image-optimization, landing-page, product-page
Source: 93 powerful statistics that show why your ecommerce site speed matters in 2026.docx

---

## Convert Speed Work from Low Priority into an Urgent Initiative
Use when: You are trying to get engineering time approved for speed work against feature and animation projects on the roadmap.
- Lead with the awareness gap: 81% of marketers know speed impacts conversions but do not prioritize optimization, and only 3% name faster speed as a top priority, while 73% call it somewhat or very urgent.
- Frame speed as a conversion, loyalty and ranking lever, not a vanity engineering metric; slow sites waste marketing spend by sending paid and organic traffic to pages that bounce.
- Counter the common anti-pattern that changes to ecommerce sites usually add animations and features that make pages slower, not faster, so new features should carry a performance review.
- Pick a small set of fixes with clear ownership — for example 57% of marketers cited image/media optimization, 43% backend fixes like caching, and 14% CDN usage — and set measurable load-time targets.
- Re-measure after changes using a tool like PageSpeed Insights (verify current interface) and tie results back to conversion and bounce.
Caveat: The 81%/3%/73% figures are survey opinions from the source, not operational benchmarks.
Caveat: Prioritization is an organizational decision; these numbers support the argument but don't guarantee budget.

Tags: speed, prioritization, stakeholder-communication, conversion-optimization, measurement, roadmap
Source: 93 powerful statistics that show why your ecommerce site speed matters in 2026.docx

---

## Model Load-Time Revenue Impact Before and After Speed Fixes
Use when: You need a defensible number to decide whether speed work is worth the engineering investment for your funnel.
- Gather your baselines: daily sessions, current conversion rate, average order value, and average load time.
- Compute current daily revenue = sessions x conversion rate x AOV, matching the source's method (its example used 50,000 visitors at 3.5% conversion and $50 AOV, yielding 1,750 orders and $87,500/day).
- Apply the source's directional lift: a 1-second improvement is associated with conversion moving from 3.5% to 3.7%, roughly 100 added orders per day on those volumes in the example.
- Annualize carefully and label assumptions — the source's $1.8M/year and $5.5M/year figures are illustrative, hypothetical math at 50,000 daily visitors and should not be presented as a forecast.
- Add secondary value the example excludes: better Google rankings, loyalty, and word-of-mouth, plus the fact that conversion rates are highest (~3.05%) on 1-2 second pages.
Caveat: The source itself flags the $1.8M-$5.5M scenario as arbitrary hypothetical math tied to 50,000 daily visitors; use your own inputs.
Caveat: Conversion lift is an observed correlation across studies, not a guaranteed causal effect of your specific change.

Tags: speed, measurement, revenue-modeling, conversion-optimization, business-case, analytics
Source: 93 powerful statistics that show why your ecommerce site speed matters in 2026.docx

---

## Use Load-Time Tiers to Predict Bounce and Browsing Depth
Use when: You are setting load-time SLAs or diagnosing why bounce and session depth move, and need reference bands.
- Use the cited bands as planning heuristics: going from 1 to 3 seconds raises bounce chance by ~32%, 1 to 5 seconds by ~90%, and 1 to 10 seconds by ~123%.
- Pair with absolute averages: pages under 2 seconds average ~9% bounce, while pages at 5 seconds average ~38%.
- Expect browsing depth to fall with load time: 8.9 pages per session at 2 seconds versus 3.3 pages at 8 seconds.
- Connect the bands back to revenue levers: deeper sessions mean more PDP and category views, which the source shows account for 72% of shopper-journey page views.
- Set an internal SLA inside Google's 3-second mobile recommendation with headroom, since shoppers increasingly expect faster and fast pages are where the highest conversion rates cluster.
Caveat: The band figures are aggregate averages across many sites, not targets for any specific storefront.
Caveat: Bounce and pages-per-session are also affected by traffic source, price and catalog depth, so speed is one factor, not the sole driver.

Tags: speed, bounce-rate, benchmarks, measurement, product-page, conversion-optimization
Source: 93 powerful statistics that show why your ecommerce site speed matters in 2026.docx

---

## Translate a Slow Site's Behavioral Damage into Retention and Word-of-Mouth Risk
Use when: You are making the retention and brand case for speed to leadership, beyond single-session conversion.
- Use the source's post-slowdown behavior shares: 45.4% of shoppers are less likely to make a purchase, 36.8% are less likely to return, and 11.9% are likely to tell a friend — framing speed as a retention and acquisition issue.
- Incorporate abandonment behavior during a slow load: about 50% refresh once, 22% close the tab, and 14% visit a competitor.
- Reinforce trust stakes: 65% of consumers trust a business less after a problem, 64% shop elsewhere after a poor experience, and 1 in 3 leave a brand they love after one bad experience.
- Set a first-page-speed target as a ranking and discoverability lever, since first-page Google results average 1.96 seconds to load (directionally: faster may rank better).
- Connect to loyalty value: 95% of mobile users return to a fast site versus 62% for a slow site, making speed a repeat-purchase input.
Caveat: These are survey percentages around hypothetical or recalled experiences, not store-observed churn rates.
Caveat: The ranking claim is inferential in the source (slow sites rank lower) and not a confirmed algorithm rule.

Tags: speed, retention, bounce-rate, trust, mobile, conversion-optimization
Source: 93 powerful statistics that show why your ecommerce site speed matters in 2026.docx

---

## Speed Fix Priority Ladder: Images, Scripts, Hosting
Use when: You are deciding where to spend limited dev or app budget on store speed and need the highest-impact fixes first.
- Start with images: compress and convert product photos, category banners and promo graphics to WebP. The source claims this single change often cuts page weight by 40-60% with minimal technical effort, so it is the best return before touching code.
- Second, audit third-party scripts: review every installed app, plugin, chat widget, review tool and analytics tag and remove ones not actively used. Each script runs on every page load and competes for browser resources.
- Third, address infrastructure: if you are on shared hosting with meaningful traffic, move to a VPS or cloud hosting, and add a CDN if you serve customers across multiple regions.
- Only after these three foundations are handled should you spend effort on JavaScript minification, code splitting or fine-tuning cache headers — the source treats those as later-order work.
- Note that the source ties the whole ladder to conversion: a 0.1-second load-time improvement can increase retail conversions by up to 8.4% (Google/NitroPack), so frame speed work as revenue work, not just a technical score.
Caveat: The 40-60% page-weight reduction and 8.4% conversion lift are source-cited research figures, not guarantees for your store; measure your own before/after.
Caveat: Hosting upgrade thresholds and budget tradeoffs depend on order volume — see the hosting-by-store-size card.

Tags: speed, performance, image-optimization, third-party-scripts, hosting, cdn, conversion-optimization
Source: Ecommerce Site Speed Optimization_ Complete Guide for 2026.docx

---

## Core Web Vitals Thresholds and What Each Metric Means for Your Store
Use when: You are diagnosing why a product, category or homepage scores poorly and need to know which CWV metric each page element is hurting.
- LCP (Largest Contentful Paint) measures how fast the largest visible element loads — usually the main product image on a PDP or the hero banner/first product grid on a category page. Target is under 2.5 seconds; over 4 seconds is rated 'poor'. Fix via image optimization and faster server response.
- INP (Interaction to Next Paint) replaced First Input Delay and measures responsiveness to clicks, taps and filters. Target is under 200 milliseconds. Ecommerce sites fail INP because of heavy JavaScript from apps, plugins and tracking scripts — the classic symptom is a customer clicking Add to Cart and nothing happening for half a second.
- CLS (Cumulative Layout Shift) measures visual stability; target is under 0.1. Common ecommerce causes are late-loading images without defined dimensions, dynamically injected content like cookie banners, and font loading that reflows text. Reserve space and set explicit dimensions.
- Diagnose per page type: PDP main image drives LCP, review/variant/BNPL JavaScript drives INP, and the hero image or rotating carousel drives homepage LCP.
- Prioritize fixes on the pages with the most traffic times the most revenue impact — a smaller gain on a high-traffic page beats a bigger gain on a rarely visited page.
Caveat: Google uses Core Web Vitals as a ranking tie-breaker; content relevance remains the primary factor, so speed alone will not outrank better content.
Caveat: Approximately 50% of mobile sites fail the CWV assessment per HTTP Archive cited in the source — passing is a competitive advantage, not the norm.

Tags: speed, performance, core-web-vitals, lcp, inp, cls, product-page, landing-page
Source: Ecommerce Site Speed Optimization_ Complete Guide for 2026.docx

---

## Lighthouse vs PageSpeed Insights: Which Lab Test to Trust
Use when: You are interpreting a speed report and need to know whether a score reflects simulated conditions or actual customer experience.
- Know the shared engine: both Lighthouse (Chrome DevTools or CLI) and PageSpeed Insights run the same Lighthouse engine with throttled CPU and network, so the underlying test methodology is identical.
- The difference is data source: Lighthouse is simulated only, while PageSpeed Insights adds real-user metrics from the Chrome User Experience Report (CrUX) covering the past 28 days.
- For store decisions, prefer PageSpeed Insights because it shows how actual visitors experienced the site, not how a controlled test machine did — use it as your baseline for both mobile and desktop.
- Use raw Lighthouse (or Lighthouse CI in your deploy pipeline) when you need a repeatable lab measurement to compare before/after a specific code change.
- Interpret PageSpeed Insights scores with the source's rough bands: 90+ is good, 50-89 needs improvement, below 50 signals serious problems. Pay most attention to the Core Web Vitals metrics and the priority-ordered recommendations section.
Caveat: CrUX data is a 28-day rolling window, so recent fixes take weeks to show up in the real-user portion of the report.
Caveat: Neither tool captures the full checkout experience — test checkout flows separately.

Tags: speed, performance, measurement, page-speed-insights, lighthouse, core-web-vitals, testing
Source: Ecommerce Site Speed Optimization_ Complete Guide for 2026.docx

---

## Image Optimization That Actually Moves LCP
Use when: You are preparing product imagery, category banners or a homepage hero and need file-size, format and loading rules that protect LCP.
- Convert to WebP: it is roughly 25-35% smaller than JPEG at equivalent quality and is supported by all modern browsers, so make it the default web format. AVIF compresses even better but has narrower browser support — keep it as an optional enhancement.
- Keep originals in JPEG or PNG and let build tools or a CDN (Cloudflare, Imgix, Cloudinary) auto-convert and serve the modern format with fallbacks for older browsers.
- Hit size targets: under 100KB for product images and under 200KB for hero banners. For product photography, 80% JPEG quality typically balances file size and appearance.
- Never compress the same image multiple times — quality degrades each pass. Compress once from the original.
- Lazy-load below-the-fold images (native loading="lazy"), but never lazy-load above-the-fold assets — lazy-loading the hero image or first visible products artificially inflates LCP. Shopify and WooCommerce usually handle product-grid lazy loading automatically.
- For stores with thousands of SKUs, use CDN-based image optimization to auto-resize by device and convert formats rather than doing it manually — the source argues the small monthly cost typically pays for itself in improved conversions.
- Watch the common mistake: uploading a 4000x3000 camera image at full quality can exceed 5MB. Resize to actual display dimensions before upload.
Caveat: CDN auto-optimization is a paid feature on most providers (often bundled with free tiers); verify current plan terms.
Caveat: The 25-35% WebP savings is a source-cited average — exact savings vary by image content.

Tags: speed, performance, image-optimization, webp, lazy-loading, cdp, cdp, lcp, product-page
Source: Ecommerce Site Speed Optimization_ Complete Guide for 2026.docx

---

## Cut Third-Party App and Script Bloat Without Losing Functionality
Use when: You are reviewing your installed apps and plugins, or deciding whether to install a new one, and need a repeatable audit that protects mobile performance.
- Quantify the problem: in the source's Shopify Speed Benchmark (1,533 stores), correlation between third-party service count and performance score was r = -0.66, the dataset's strongest signal. Stores with 0-5 services scored a median 74 on mobile; stores with 21-30 dropped to 44.
- Audit regularly: list every app, plugin, chat widget, review tool, upsell popup and analytics tag, then remove tools you no longer actively use. Each adds JavaScript running on every page load.
- Before installing anything new: check reviews for speed complaints. After installing: run a speed test to measure impact. Remove apps that degrade performance without delivering proportional value.
- For scripts you must keep, defer or async-load those that don't affect initial rendering so they download after main content — this improves INP by reducing JS execution during page load.
- Account for industry stack weight when setting expectations: source cites beauty stores loading a median 31 third-party services per page (worst of 9 Shopify industries for mobile speed) and automotive parts stores a median of 15 (best), with fashion/apparel in between due to sizing charts and shipping insurance.
- Guard against gradual degradation: performance declines silently as products, apps and tracking scripts accumulate, so schedule the audit rather than waiting for complaints or a conversion drop.
Caveat: The median-score and correlation figures come from the source's own benchmark dataset of Shopify stores; treat them as directional, not as targets your store must match.
Caveat: Removing apps can drop functionality customers expect — weight each removal against its feature value, not just its byte cost.

Tags: speed, performance, third-party-scripts, app-audit, shopify, mobile, inp
Source: Ecommerce Site Speed Optimization_ Complete Guide for 2026.docx

---

## Caching Layers: What to Cache, What Never to Cache
Use when: You are configuring cache headers or a CDN and need to set safe durations and exclusion rules for user-specific ecommerce pages.
- Browser caching: instruct visitor browsers to store static assets (CSS, JS, images) locally. Set long expiration dates — the source suggests up to a year for static assets since filenames change when content updates. HTML pages need shorter durations so visitors see current content.
- CDN edge caching: store content on globally distributed servers so a visitor in Tokyo is served from an Asian edge instead of a US origin. The source cites 200-800ms latency reduction for geographically distant visitors.
- Server-side caching: store generated HTML or database query results so the server doesn't rebuild pages per visitor. WooCommerce options include WP Rocket, W3 Total Cache and Redis Object Cache; Shopify manages this automatically with limited control.
- Never cache cart pages, checkout flows or account pages — they contain visitor-specific data and caching them causes serious errors.
- Handle session cookies carefully: the source cites Salesforce guidance to defer session creation until the visitor actually needs it (first add-to-cart or login), which keeps anonymous browsing cacheable.
- Handle volatile data like prices and stock status: either cache the page and update those elements dynamically via JavaScript, or use short cache durations with rapid invalidation when data changes.
- Audit cache headers after changes to confirm updated content appears correctly while static assets stay cached — misconfiguration causes either stale prices or missed optimization.
Caveat: Shopify gives limited control over server-side caching, so some layers may not apply on that platform.
Caveat: Aggressive asset caching requires a cache-busting filename strategy (e.g., hashed filenames) or visitors will see stale CSS/JS.

Tags: speed, performance, caching, cdn, checkout, woocommerce, shopify
Source: Ecommerce Site Speed Optimization_ Complete Guide for 2026.docx

---

## CDN Setup and Configuration for Ecommerce
Use when: You are selecting or configuring a CDN for your store and need concrete setup choices that avoid cache fragmentation and stale content.
- Understand the mechanism: a visitor request routes to the nearest edge server, which returns cached content instantly or fetches from origin. The first visitor from each region sees normal load time; subsequent visitors get cached content with much lower latency.
- Start caching static assets — images, CSS, JavaScript and fonts — since these change infrequently and benefit most. Configure aggressive caching for static assets and shorter TTLs for pages with dynamic content like prices or stock levels.
- Choose a provider based on traffic geography: single-region stores get by with a basic CDN; global stores benefit from extensive edge networks. Options cited include Cloudflare (DDoS protection, image optimization), Fastly (edge computing), Akamai, AWS CloudFront and BunnyCDN (competitive pricing for high-bandwidth stores). Most offer free tiers or affordable entry plans.
- Configure cache keys carefully: include query parameters that affect content (like page numbers) but exclude tracking parameters, which create unnecessary cache fragmentation.
- Set up automatic cache invalidation so updated product images or new code clear immediately — most CDNs offer API-based purging or URL-based invalidation.
- Monitor cache hit rate: a well-configured CDN should serve 80%+ of requests from cache. Low hit rates indicate misconfiguration or excessive dynamic content.
Caveat: The 80%+ hit-rate figure is the source's target, not a guaranteed baseline — what's achievable depends on how dynamic your storefront is.
Caveat: Provider features and plan terms change; verify current offerings before committing.

Tags: speed, performance, cdn, caching, infrastructure, measurement
Source: Ecommerce Site Speed Optimization_ Complete Guide for 2026.docx

---

## Hosting Architecture: Shared vs VPS vs Cloud by Order Volume
Use when: You are deciding whether your store needs to move off shared hosting or add a VPS/cloud plan, often triggered by traffic spikes or slow pages.
- Know the shared-hosting limit: shared hosting places multiple sites on one server sharing CPU, memory and bandwidth, so a neighbor's traffic spike slows your store. It costs roughly $1-15/month and suits brand-new stores only — the source cites BlueHost noting resource limits make it unsuitable for meaningful traffic.
- VPS as middle ground: a Virtual Private Server guarantees CPU and memory within a shared physical server, starting around $20-50/month for managed options. It fits growing stores that outgrew shared hosting but don't need dedicated hardware. Managed VPS handles administration; unmanaged requires technical skill.
- Cloud hosting for scale: distributes the site across multiple servers with automatic scaling, absorbing traffic spikes without manual upgrades. Options include AWS, Google Cloud, DigitalOcean, Shopify's infrastructure and managed WooCommerce hosts like Kinsta.
- Use the source's rough threshold: stores processing 100+ orders monthly should use VPS or cloud hosting, since improved reliability and speed pay for themselves in reduced cart abandonment.
- For high-volume stores, choose auto-scaling cloud infrastructure so peak traffic during sales and promotions is handled without pre-provisioning extra capacity.
- If you serve international customers, combine the hosting upgrade with a CDN rather than relying on the origin server alone.
Caveat: The 100+ monthly orders threshold is a source heuristic, not a calculated break-even — model your own cart abandonment rate and average order value to judge ROI.
Caveat: Managed hosting prices and feature sets change frequently; verify current plans.

Tags: speed, performance, hosting, infrastructure, vps, cloud-hosting, shopify, woocommerce
Source: Ecommerce Site Speed Optimization_ Complete Guide for 2026.docx

---

## Speed Testing Toolchain: From Quick Score to Root Cause
Use when: You are investigating store speed problems and need to pick the right tool for a quick check versus deep root-cause analysis.
- Start with PageSpeed Insights for mobile and desktop scores plus real-user CrUX metrics and priority-ordered recommendations — the source's default starting point for most store owners.
- Use GTmetrix for a deeper dive than PSI: its waterfall chart shows exactly which resources load when and how long each takes. Create a free account to test from different locations and connection speeds, useful for seeing how international or mobile customers experience the site. Check the 'Top Issues' section first for highest-impact changes.
- Use WebPageTest when you need the most detailed diagnosis: run from specific locations, device types and connection speeds. The filmstrip view shows visual progress at each load stage; the connection view reveals server response times and resource sequences. It requires more interpretation and suits diagnosing specific issues rather than routine monitoring.
- Test mobile separately from desktop, and on real devices rather than only browser emulation — what feels fine on a dev machine frustrates customers on mid-range phones.
- Don't rely on one test: performance varies with server load, network conditions and cached state. One test is a snapshot, not a trend.
Caveat: PageSpeed Insights' real-user data lags 28 days, so fresh fixes won't appear immediately.
Caveat: Ecomhint's paid audit is a promotional context in the source; the free Google tools cover the core diagnostics.

Tags: speed, performance, measurement, testing, page-speed-insights, gtmetrix, webpagetest, mobile
Source: Ecommerce Site Speed Optimization_ Complete Guide for 2026.docx

---

## Continuous Performance Monitoring and Budgets
Use when: You are setting store speed governance — deciding test cadence, alerting and limits on page weight or third-party scripts.
- Adopt a monitoring cadence: test at minimum monthly to catch gradual degradation, and test immediately after installing apps, changing themes or making site-wide updates.
- Before major sales events, run speed audits to confirm the site can handle increased traffic smoothly.
- Set up automated monitoring rather than manual tests: free options include PageSpeed Insights API with scheduled runs, GTmetrix monitoring (with account) and Lighthouse CI for automated testing during deployments. Paid services like DebugBear, SpeedCurve and Calibre add tracking, alerting and historical analysis.
- Define a performance budget as a guardrail: maximum page weight, minimum speed scores and maximum third-party script count. Review any change that exceeds the limits before approving it — without defined limits, performance degrades gradually.
- Run targeted tests after app installs specifically, since each app runs code on every page and cumulative additions are the main cause of silent slowdown.
Caveat: Paid monitoring tools are a cost that the source argues pays off for revenue-critical stores, but ROI depends on store scale.
Caveat: Performance budgets are only useful if enforcement is built into the release or approval process, not just documented.

Tags: speed, performance, measurement, monitoring, performance-budget, testing, process
Source: Ecommerce Site Speed Optimization_ Complete Guide for 2026.docx

---

## Prioritizing Speed Work by Page Type and Traffic
Use when: You are allocating limited speed-optimization effort across homepage, PDPs, category pages and checkout and need to know what matters on each.
- Homepage: LCP is critical because it's often the entry point for brand and direct traffic. Watch large hero images, rotating carousels and promo banners. A slow homepage loses customers before they see a product.
- Product pages: the main product image drives LCP, while review widgets, related products and variant selectors add JavaScript that hurts INP. Keep the PDP lean by loading secondary content only after the primary image and buy button render. PDPs are especially affected on Shopify because they load variant selectors, review widgets and BNPL calculators that other page types don't need.
- Category pages: many thumbnails load at once, filters must respond fast and pagination must be smooth. Lazy-load below-the-fold product images and serve responsive thumbnails rather than full-resolution photos. Filter responsiveness is an INP concern.
- Checkout: slow checkout directly causes abandoned carts. Payment gateway integrations, address verification and fraud detection scripts add load time, and cart calculations must feel instant. Test checkout flows separately because overall site speed scores don't capture the full checkout experience.
- Allocate by impact: prioritize the highest-traffic pages first — the source notes a 0.5-second improvement on a page with 10,000 monthly visitors matters more than a 2-second improvement on a page with 100 visitors.
Caveat: The source's page-priority framing assumes overall site speed scores are inadequate for checkout; validate checkout timing with dedicated testing.
Caveat: The traffic-weighting heuristic is directional; weight by revenue per page, not visits alone, where data allows.

Tags: speed, performance, product-page, landing-page, checkout, prioritization, measurement
Source: Ecommerce Site Speed Optimization_ Complete Guide for 2026.docx

---

## JavaScript and CSS Optimization: Minify, Split, Inline Critical
Use when: You have already optimized images and trimmed apps, and now need to reduce JS/CSS blocking so LCP and INP improve.
- Minify first: strip whitespace, comments and long variable names. The source cites up to 80% JavaScript file-size reduction via minification. Use Terser for JS and CSSNano for CSS; most modern build tools (Webpack, Vite, Parcel) minify automatically in production. On Shopify, minification typically needs an app like Hyperspeed or TinyIMG; WooCommerce stores can use Autoptimize or WP Rocket.
- Then code-split by page type: break bundles into chunks that load on demand so visitors only download what they need. Product page code shouldn't load on category pages, and category pages don't need product zoom functionality. Modern frameworks (Next.js, Nuxt, Gatsby) handle this automatically; traditional themes need manual Webpack dynamic imports.
- Finally, implement Critical CSS: extract the styles needed for above-the-fold content and inline them directly in the HTML, eliminating the render-blocking external stylesheet request. Load the rest of the CSS asynchronously after initial render. Tools like Critical and PurgeCSS automate this; WP Rocket and similar WordPress caching plugins can generate critical CSS.
- Apply these after the priority ladder — the source places code work behind image optimization, script auditing and hosting/CDN changes.
- Verify with before/after measurements using a consistent lab test (Lighthouse or Lighthouse CI) so you can attribute the improvement to the code change.
Caveat: The 80% minification figure is a source-cited maximum for JS file size, not a typical result across all assets.
Caveat: Code splitting and Critical CSS require build tooling or platform-specific apps; hand-rolled implementations can break themes, so test thoroughly.

Tags: speed, performance, javascript, css, critical-css, code-splitting, minification, shopify, woocommerce
Source: Ecommerce Site Speed Optimization_ Complete Guide for 2026.docx

---

## Common Speed Mistakes and How to Prevent Them
Use when: You are auditing store speed hygiene or building a process to stop new speed regressions from being introduced.
- Never upload unoptimized images: resize to actual display dimensions and compress before upload. A 4000x3000 photo at full quality can exceed 5MB, longer than some customers will wait.
- Never install an app without a speed check: check reviews for speed complaints before installing, and test page speed after to measure impact. Remove apps that degrade performance without proportional value.
- Never assume desktop tests reflect mobile: mobile devices have less processing power and often slower connections. Test mobile specifically and prioritize mobile optimizations — the majority of ecommerce visits are mobile.
- Avoid caching misconfiguration: too-aggressive caching serves stale prices or stock status; too-conservative caching forfeits the benefit. Audit cache headers after changes.
- Optimize fonts: host fonts locally or use font-display: swap to show fallback text while custom fonts load, and subset fonts to include only the characters you use.
- Clean the database on database-driven platforms: old revisions, expired transients and orphaned metadata bloat WooCommerce and similar platforms. Schedule regular cleanup with plugins like WP-Optimize.
- Test more than once: performance varies by server load, network and cache state, so a single test is a snapshot, not a trend.
Caveat: This is a prevention checklist, not a diagnostic ranking — the priority ladder (images, scripts, hosting) still governs fix order.
Caveat: Database cleanup tools differ by platform; Shopify stores have far less database access than WooCommerce, so this step applies mainly to self-hosted platforms.

Tags: speed, performance, image-optimization, app-audit, mobile, caching, fonts, woocommerce
Source: Ecommerce Site Speed Optimization_ Complete Guide for 2026.docx

---

## Quantifying the Conversion Cost of Slow Load Times
Use when: You need to justify speed optimization investment to a store owner or stakeholder using conversion and abandonment impact.
- Use the headline figure carefully: a 0.1-second improvement in load time can increase retail conversions by up to 8.4% (Google/NitroPack). Frame this as directional evidence, since it's an upper-bound claim from cited research.
- Use the delay figures: a one-second delay is associated with roughly 7% fewer conversions (Cloudflare), and stores can lose around 4% of conversions for every 2 seconds of load time (Cloudflare). A one-second site converts roughly 5x more visitors than a ten-second site (Queue-it).
- Use the abandonment threshold: approximately 53% of mobile visitors abandon sites taking longer than three seconds (Google/NitroPack). On mobile, with the majority of ecommerce traffic, the three-second threshold becomes even more critical.
- Use the four-second cliff: around 63% of shoppers leave if an ecommerce site takes more than four seconds to load (Queue-it), and these visitors rarely return — they find a faster competitor.
- Bring in case evidence cautiously: Vodafone's A/B test found 31% LCP improvement led to 15% better lead-to-visit rate and 8% more sales; Rakuten 24 reported 33% higher conversion rate and 53% more revenue per visitor after CWV optimization. Present these as examples, not promises.
- Also cite the demand-side stat: roughly 70% of consumers say page speed affects their decision to buy (Unbounce).
Caveat: These figures are source-cited research averages and case-study results, not guarantees — treat them as directional. Case study results are examples, not promises.
Caveat: Lead-to-visit rate (Vodafone) is a lead metric, not a purchase conversion metric; don't conflate it with sales conversion figures like Rakuten's.

Tags: speed, performance, benchmarks, conversion-optimization, mobile, abandonment, business-case
Source: Ecommerce Site Speed Optimization_ Complete Guide for 2026.docx

---

## Speed as an SEO Tie-Breaker Under Mobile-First Indexing
Use when: You are deciding whether to invest in speed partly for organic search, and setting expectations on how much ranking lift it can produce.
- Position speed correctly: content relevance remains the primary ranking factor, and Core Web Vitals serve as a tie-breaker between pages with similar quality — so speed optimization is a genuine advantage for competitive keywords where content quality is comparable.
- Prioritize mobile: Google uses mobile-first indexing, so your mobile speed determines ranking potential. Approximately 50% of mobile sites fail the Core Web Vitals assessment (HTTP Archive cited in source), meaning passing is a differentiator.
- Diagnose mobile separately with PageSpeed Insights' real-user mobile data, and test on actual devices rather than only browser emulation.
- Pair speed work with on-page SEO checks — the source treats speed as one ranking signal and suggests reviewing indexability, meta tags and structured data alongside Core Web Vitals.
- Expect the biggest SEO effect on competitive, content-comparable keyword sets rather than as a universal ranking fix.
Caveat: The 50% pass rate and tie-breaker framing are source-cited; actual ranking impact varies by query competitiveness and content quality.
Caveat: Speed cannot compensate for thin or irrelevant content.

Tags: speed, performance, seo, core-web-vitals, mobile, measurement
Source: Ecommerce Site Speed Optimization_ Complete Guide for 2026.docx

---

## Setting Speed Targets by Page and Store Type
Use when: You are defining acceptance criteria for a store build, theme change or app install and need concrete speed targets to test against.
- Set the headline load target: aim for pages loading under three seconds, with two seconds or less as the competitive-performance target for stores competing on experience.
- Set Core Web Vitals thresholds as pass/fail gates: LCP under 2.5 seconds, INP under 200 milliseconds, CLS under 0.1.
- Use PageSpeed Insights scores as a coarse health check: 90+ is good, 50-89 needs improvement, below 50 signals serious problems requiring immediate attention.
- Apply page-specific expectations: PDP main image drives LCP; PDP secondary content should load after the primary image and buy button render; category thumbnails should be lazy-loaded below the fold with responsive sizing; checkout needs separate testing since overall scores miss it.
- Tailor targets to platform: on Shopify the main controllable levers are app count and images, since the platform handles hosting and basic optimization; on WooCommerce, hosting, caching, database bloat and plugin count dominate, so set tighter infrastructure requirements.
- Define a performance budget as a guardrail — maximum page weight, minimum score, maximum third-party scripts — and review changes that exceed it before approval.
Caveat: The three-second and two-second load targets and 90+ score band are source heuristics; 'two seconds or less' is described as a competitive-performance aspiration rather than a threshold with measured lift.
Caveat: PageSpeed scores fluctuate with lab conditions, so use CWV metrics as the more stable signal.

Tags: speed, performance, benchmarks, core-web-vitals, performance-budget, product-page, checkout, shopify, woocommerce
Source: Ecommerce Site Speed Optimization_ Complete Guide for 2026.docx

---

## Diagnosing 'Why Is My Store Slow?' by Category
Use when: You are starting a speed investigation and need to map symptoms to likely causes before testing.
- Suspect images first: unoptimized images cause more speed problems than anything else — product photos, category banners and promo graphics uploaded at full resolution. A single uncompressed hero image can exceed 2MB.
- Suspect app/plugin accumulation second: a store with 30 apps may have 30 separate scripts competing for resources. Review upsell popups, analytics tools and other add-ons, since each adds JavaScript running on every page load.
- Suspect code bloat third: themes, page builders and customizations leave unminified JS/CSS full of comments, whitespace and formatting the browser doesn't need.
- Check platform-specific patterns: Shopify stores slow from app overload and PDP-specific functionality (variant selectors, review widgets, BNPL calculators); WooCommerce sites face shared hosting, unoptimized databases and plugin conflicts where every feature requires another plugin.
- Recognize that problems appear gradually, not suddenly — more products, apps and tracking scripts accumulate without monitoring until customers complain or conversions drop.
- Diagnose with PageSpeed Insights before fixing: often a single problem (a 3MB hero image or a dozen unused apps) causes most of the slowdown, so fix the biggest issue first rather than optimizing everything at once.
Caveat: This is a likely-cause ordering, not a substitute for measurement — confirm with PageSpeed Insights, GTmetrix or WebPageTest before major changes.
Caveat: Platform-specific causes differ enough that generic advice can mislead; diagnose within your platform's context.

Tags: speed, performance, diagnostics, image-optimization, app-audit, hosting, shopify, woocommerce
Source: Ecommerce Site Speed Optimization_ Complete Guide for 2026.docx

---

## Read PageSpeed Insights: Field Data (CrUX) vs Lab Data (Lighthouse)
Use when: Interpreting a PageSpeed Insights report for a product page, category page, or homepage and deciding which numbers to trust when setting speed work priorities.
- Open pagespeed.web.dev (verify the current interface) and enter the URL of the store page you want to assess.
- Keep the toggle on Mobile. The source's focus is always mobile because most web browsing happens on phones, not because mobile is harder.
- Read the top section as field data: anonymized Chrome UX Report (CrUX) data aggregated over the past 28 days from real Chrome users on that URL. This is what real shoppers experienced.
- Read the second section as lab data (Lighthouse): a simulation of a mid-tier device on a mobile network, run once, used for immediate diagnostic feedback.
- Expect the two sections to disagree — the source shows LCP of 1.6s in field data vs 1.1s FCP in lab data on the same page. That does not mean one is wrong.
- Prioritize fixing lab data issues, because improvements there eventually surface in field data, but expect a roughly 28-day lag before the field numbers reflect your work.
- If you are failing Core Web Vitals but lab looks clean, the cause is real-user conditions (device mix, network, third-party scripts), not a reporting error.
Caveat: Field data needs enough Chrome traffic in the 28-day window; low-traffic pages show no URL data at all.
Caveat: Lab data measures Total Blocking Time, not First Input Delay — FID only exists in field data because it requires real interactions.

Tags: speed, core-web-vitals, pagespeed-insights, measurement, diagnostics, product-page
Source: Google PageSpeed Insights_ Step-by-Step tutorial to Boost Site Speed.docx

---

## Use the Origin vs URL toggle to read low-traffic page speed
Use when: Auditing speed on a new product page, a low-traffic landing page, or a niche category page and wondering why the field data does not match what you expect for that page.
- Look at the URL/Origin toggle in the field data section after running the test.
- Notice whether the URL option is greyed out — if it is, the specific page did not receive enough Chrome traffic in the past 28 days.
- Accept the Origin figure as the site-wide average across all pages, and read it as a general health signal, not a diagnosis of that page.
- Use lab data for that page instead: it runs on every URL regardless of traffic and gives you page-specific issues to fix.
- If the whole site lacks traffic for 28 days, no field data will appear at all — work entirely from lab data until volume builds.
- Track the Origin trend over weeks as a proxy for site-wide speed health on lower-traffic stores.
Caveat: Origin data blends your fastest and slowest pages, so a single broken template can hide inside a healthy average.
Caveat: The 28-day window means recent fixes will not show up immediately.

Tags: speed, core-web-vitals, pagespeed-insights, measurement, landing-page, diagnostics
Source: Google PageSpeed Insights_ Step-by-Step tutorial to Boost Site Speed.docx

---

## Fix LCP by identifying the largest element and optimizing it
Use when: Improving page speed on a product page or homepage where the hero image, banner, or headline is the first thing shoppers see.
- Treat LCP under 2.5s as good (green), 2.5–4.0s as needs improvement (orange), and over 4.0s as poor (red) — these are the thresholds the source states.
- Find the LCP element: in lab data, expand Diagnostics and open 'Largest Contentful Paint element' to see exactly what it is (image, video, or text block).
- If it is an image: resize to the dimensions actually rendered, compress the file below roughly 250KB, and serve in a modern format such as WebP or AVIF.
- If it is a video: compress the file to reduce its size.
- If it is text: leave it. The source's opinion is that a text LCP is the fastest-loading option, so prefer a text-led hero when design allows.
- Remember that a slow LCP is usually not a web server problem — the source attributes it mainly to your theme, plugins, and the page elements you placed.
Caveat: The 250KB image guidance and text-LCP preference are the source's recommendations, not vendor-published requirements.
Caveat: The 1,200px recommended image width mentioned in the source is tied to Google Discover eligibility, not LCP itself.

Tags: speed, core-web-vitals, lcp, image-optimization, product-page, landing-page, resource-optimization
Source: Google PageSpeed Insights_ Step-by-Step tutorial to Boost Site Speed.docx

---

## Fix CLS on checkout and product pages with reserved space and image dimensions
Use when: Diagnosing layout jumps on a cart, checkout, or product page where shoppers mis-tap quantities, variants, or the place-order button.
- Read the score as: 0.1 or less good, 0.1–0.25 needs improvement, above 0.25 poor — the thresholds the source states.
- Remember the source's illustration: a shopper on the checkout page who casually selects 56 items by accident is the result of a layout shift moving the control under their finger.
- Audit the page for dynamically injected content — ads, embeds, iframes — that loads after the initial render and pushes content down.
- For each such element, reserve a dedicated placeholder with fixed space, regardless of the final shape or dimensions the element will take. The source flags this as technical work worth involving a designer on.
- Add explicit width and height attributes to every image so the browser reserves space before the file arrives. Wrapping image tags in fixed-ratio containers is the equivalent modern technique.
- If you run WP Rocket, enable its 'Add missing width and height attributes' image setting to apply this broadly with a single checkbox.
- Re-test after each change; a single attribute fix on a large template can move the CLS score substantially.
Caveat: Placeholder layout for third-party ads and embeds is genuinely technical and often needs developer or designer time.
Caveat: Fix CLS before chasing other metrics on checkout — the revenue risk from mis-taps is direct.

Tags: speed, core-web-vitals, cls, checkout, product-page, image-optimization, resource-optimization
Source: Google PageSpeed Insights_ Step-by-Step tutorial to Boost Site Speed.docx

---

## Reduce TBT by unblocking the main thread with JS minify, defer, and delay
Use when: A product or checkout page feels unresponsive on mobile — taps on add-to-cart, variant selectors, or nav menus lag — and lab data flags Total Blocking Time.
- Understand the mechanism: the main thread parses HTML, renders content, and processes user input. Any task running longer than 50ms is a 'long task' and blocks everything else while it runs.
- TBT is the accumulated blocking from those long tasks; the source describes a failing TBT as a sign your page runs a lot of complex JavaScript.
- The fastest fix per the source is to minify JavaScript files and defer or delay JavaScript execution so non-critical scripts stop occupying the main thread during load.
- In WP Rocket, go to the File Optimization tab (verify current interface) and enable JS minification alone first. The plugin warns it can break things.
- Save, clear the cache, and re-test the live site in an incognito window, clicking through a few pages to confirm every element renders and works.
- If nothing breaks, keep it on, then repeat the same activate-save-clear-test cycle for combining JS files.
- If something breaks, uncheck that single setting — the failure tells you which optimization is unsafe for your site.
- Then enable deferred JS loading and delay JS execution, using the exclusion list to keep specific scripts loading first, and optionally defer plugin and theme scripts.
- Re-run PageSpeed Insights to confirm TBT and the overall performance score moved.
Caveat: Never enable minify/combine/defer/delay in bulk without clearing cache and testing incognito — the source's protocol exists precisely because each can break UI.
Caveat: Delay JS can break interactive elements like add-to-cart or sliders if you delay scripts the page needs at first paint; exclude those.
Caveat: A cached copy of the page will produce stale lab results, so clear cache before every re-test.

Tags: speed, tbt, javascript-optimization, wp-rocket, core-web-vitals, resource-optimization, product-page
Source: Google PageSpeed Insights_ Step-by-Step tutorial to Boost Site Speed.docx

---

## Cache-bust your speed tests with an above-the-fold indicator
Use when: Re-testing speed after editing a product page, template, or plugin setting and you need confidence the reported score reflects the new version.
- Before you re-run PageSpeed Insights, add a small, obvious text or element to the page — for example a temporary line reading 'test build 2' — and keep it above the fold.
- Run the assessment on the live URL.
- Look at the above-the-fold screenshot PageSpeed Insights renders next to the performance score.
- If your indicator element appears in the snapshot, the crawl captured your latest changes and the metrics are trustworthy.
- If it does not appear, your test hit a cached or stale version — clear the cache and re-run before interpreting any number.
- Remove the indicator once you have confirmed the build and before you consider the page finished.
- Do this on every iteration of a speed project; it prevents hours spent reacting to stale metrics.
Caveat: The indicator must be above the fold or it will not appear in the rendered snapshot.
Caveat: This confirms freshness of the crawl, not that the crawl matches what a real shopper's device will render.

Tags: speed, measurement, pagespeed-insights, experiment-design, diagnostics, product-page
Source: Google PageSpeed Insights_ Step-by-Step tutorial to Boost Site Speed.docx

---

## Use the performance score's hover hint to pick your highest-impact fix
Use when: You have a long list of speed issues on a store page and limited time before a launch or campaign, and need to sequence the work.
- Read the overall performance score: green at 90 or above, orange from 50 to 89, red below 50 — the bands the source states.
- Hover over the score indicator circle to reveal which metric would create the most impact on the score for that page.
- Scroll to the optimization opportunities section, which PageSpeed Insights groups by the metric each fix affects.
- Open the group matching the flagged metric first — in the source's walkthrough, TBT was the flagged area, so the TBT opportunities were the ones to work.
- Work those opportunities top-down, re-testing after each change, rather than working through the whole checklist in list order.
- Use the recommendations inside each opportunity as a starting point: the source notes the 'serve images in next-gen formats' item recommends converting images to WebP via a performance plugin or WP Rocket's Image Optimization tab.
- Expect the score to move in jumps, not gradually — the source's example shows a WP Rocket configuration pass taking a page from 69 to 99 with nothing visibly broken.
Caveat: Score movement like 69-to-99 is one demonstration on one page, not a guaranteed result for your store.
Caveat: The source explicitly warns against chasing a 100 or a CrUX pass for its own sake; content depth and serving the audience are what ultimately drive rankings.
Caveat: Verify the current PageSpeed Insights hover behavior and recommendation links before relying on them.

Tags: speed, pagespeed-insights, prioritization, core-web-vitals, measurement, landing-page
Source: Google PageSpeed Insights_ Step-by-Step tutorial to Boost Site Speed.docx

---

## Sequence metrics: TTFB, FCP, FID, INP and what each one actually measures
Use when: Translating a PageSpeed report into a decision about whether to change hosting, theme, plugin stack, or front-end code on a store.
- Time to First Byte (TTFB): time from the browser's request to the server returning the first byte. Good is below 0.8s and it should not exceed 1.8s, per the source.
- First Contentful Paint (FCP): time until the first object renders, signaling to the shopper that the page is loading. Good is under 1.8s, 1.8–3.0s needs improvement, above 3.0s is poor.
- FID is a historical responsiveness metric, replaced by INP in 2024. Do not use it as the current Core Web Vitals target.
- INP measures interaction responsiveness through the next paint; it does not necessarily include completion of an asynchronous cart request. Track cart completion separately.
- When FCP is poor, the source argues the cause is usually your theme, plugins, and page elements rather than the web server — so audit the front end before buying new hosting.
- Only the top three field metrics are Core Web Vitals in the current report; the rest are 'notable' or experimental, so treat them as context rather than pass/fail gates.
- Verify the current report layout, as Google has shifted which metrics are labeled Core Web Vitals.
Caveat: The source describes INP and FID together, but FID is field-only while INP is the broader interaction metric — do not treat them as identical.
Caveat: These score bands are the source's stated thresholds; confirm against current Google documentation, since metric definitions and thresholds change.
Caveat: Current Core Web Vitals are LCP, INP and CLS; FCP and TTFB remain diagnostic. https://web.dev/articles/vitals

Tags: speed, core-web-vitals, ttfb, first-contentful-paint, inp, measurement, diagnostics
Source: Google PageSpeed Insights_ Step-by-Step tutorial to Boost Site Speed.docx

---

## Speed Index and the remaining Lighthouse audits beyond performance
Use when: Running a full Lighthouse review on a product page or checkout before launch and deciding which audit failures actually matter to the store.
- Interpret Speed Index as how fast the above-the-fold content visually fills in. The source's view is that if the other metrics are healthy, Speed Index generally follows — so fix the underlying metrics rather than targeting Speed Index directly.
- Read above-the-fold as everything visible on first load; everything else is below the fold.
- Use the Accessibility audit to catch missing descriptive labels on buttons (needed by screen-reader users) and insufficient contrast between background and foreground colors — both affect real shoppers.
- Use the Best Practices audit as a check on modern development standards for speed, security, and overall user experience.
- Use the SEO audit to confirm structured data is valid, the page is not blocked from indexing, and a title and meta description exist — factors that help search engines index product pages.
- Treat the SEO audit as a shallow check; the source notes a thorough on-page SEO checklist covers more than Lighthouse does.
Caveat: The accessibility audit is a subset of real accessibility work; passing it does not make a store accessible.
Caveat: The SEO audit does not assess content quality or commercial intent.

Tags: speed, lighthouse, accessibility, seo, product-page, diagnostics, measurement
Source: Google PageSpeed Insights_ Step-by-Step tutorial to Boost Site Speed.docx

---

## Share a frozen PageSpeed report with your developer or agency
Use when: You need a web developer or consultant to fix speed problems on a product template or checkout and want them working from the same evidence you saw.
- Run the assessment on the exact URL and device (mobile) you want fixed.
- Click the copy-link control in the report interface (verify the current control and label).
- Send the link with a short note naming the metric to fix — for example, 'TBT on the mobile product page' — rather than sending the whole report unexplained.
- Instruct the recipient to open the link, which reproduces the same report rather than re-running the test on a possibly changed page.
- Ask them to confirm the indicator or snapshot matches before starting, so you know they are looking at your build.
- Keep the link as a record of the before state so you can compare it to the after state once fixes ship.
Caveat: A stored report reflects the page at test time; if the site changes, it is a historical artifact, not a live view.
Caveat: Lab data in a shared report is simulated, so do not present it to stakeholders as actual customer experience.

Tags: speed, pagespeed-insights, measurement, workflow, diagnostics, core-web-vitals
Source: Google PageSpeed Insights_ Step-by-Step tutorial to Boost Site Speed.docx

---

## Diagnose Shop Speed With PageSpeed Insights Before Optimizing
Use when: Deciding which speed fixes to tackle first on a product listing or product detail page that feels slow or is losing mobile conversions.
- Before changing anything, measure the current shop on Google PageSpeed Insights (free) for both desktop and mobile — the source notes results often differ significantly between the two.
- If most of your traffic or revenue comes from mobile shoppers, prioritize the mobile score first.
- Use the tool's good / mediocre / poor classification rather than the raw number alone to decide whether you have a project or a tune-up.
- Read the improvement recommendations and the estimated time savings each fix should deliver, and sequence work by projected saving versus effort.
- Cross-check with a second tool (the source names GTmetrix or Pingdom) so you are not optimizing to one tool's quirks; verify current tool interfaces and scoring before relying on them.
Caveat: Scores are tool-specific and can change with scoring-version updates — treat them as a comparative baseline for your own site over time, not an absolute grade.
Caveat: Do not stop at diagnosis: the source warns against generic 'use GTmetrix' advice with no mechanical fix behind it.

Tags: speed, core-web-vitals, measurement, page-speed-insights, mobile, conversion-optimization, audit
Source: Page Speed Optimization_ How to Improve the Loading Time of Your Online Shop.docx

---

## Map LCP, FCP, TTI and TBT to What Shoppers Actually Experience
Use when: Interpreting a speed report and choosing whether to fix first paint, interactivity or main-content load on category and product pages.
- Read First Contentful Paint (FCP) as when the first visible element — a heading, a product image — appears.
- Read Time to Interactive (TTI) as when the page becomes usable, i.e. the shopper can actually click and buy.
- Read Total Blocking Time (TBT) as the elapsed time between FCP and TTI — in practice the window where the page looks ready but ignores taps on filters, variants or add-to-cart.
- Read Largest Contentful Paint (LCP) as when the main content is fully loaded from the user's point of view, which on a PDP is typically the hero product image.
- Combine: a fast FCP with a long FCP-to-TTI gap tells you scripts are blocking interaction, whereas a slow LCP points at the heavyweight primary image or hero asset.
Caveat: TBT as 'time between FCP and TTI' is the source's definition; some tooling calculates TBT from long tasks, so confirm the definition used in your current report before quoting a number.

Tags: speed, core-web-vitals, measurement, product-page, mobile, technical-seo
Source: Page Speed Optimization_ How to Improve the Loading Time of Your Online Shop.docx

---

## Run Image Compression and Device-Specific Sizing as the First Speed Fix
Use when: Improving load time on image-heavy category pages or product detail pages where high-quality product photography is slowing first render.
- Compress product and lifestyle images while keeping them presentable — the source treats compression as a basic time-saving step, not an optional refinement.
- Serve dimensions matched to the loading device; an XXL desktop image delivered to a small smartphone is wasted bytes.
- Generate different image sizes for different pages, usages and devices rather than one master asset for all placements.
- Combine with a CDN so the correctly sized image is fetched from a server geographically near the shopper.
Caveat: High-quality imagery is a conversion asset for shops, so balance compression against visible quality loss rather than maximizing compression.
Caveat: Do not ship a single downsized master everywhere; the source specifically recommends per-device and per-placement variants.

Tags: speed, resource-optimization, images, product-page, cdn, mobile
Source: Page Speed Optimization_ How to Improve the Loading Time of Your Online Shop.docx

---

## Use Lite Embeds to Stop Video From Killing Page Speed
Use when: A product detail page or landing page embeds demo or how-to videos and the video player code is delaying the rest of the page.
- Identify every video embed on the page and check whether the full player loads on page load.
- Replace the default embed with a lite embed: only the thumbnail image loads initially.
- Fetch and initialize the actual video player code only after a user interaction — a click on the thumbnail.
- Apply the same deferral thinking to non-video embeds and integrations that exist purely to add 'additional content and code'.
Caveat: The shopper must click before video plays, so make the thumbnail look clearly interactive and relevant to the product.
Caveat: Confirm your current video platform's lite/facade embed option or a lightweight wrapper before implementing, as player APIs change.

Tags: speed, resource-optimization, video, lite-embeds, product-page, third-party-scripts
Source: Page Speed Optimization_ How to Improve the Loading Time of Your Online Shop.docx

---

## Audit Third-Party Scripts and Defer the Survivors
Use when: Trimming tag-manager, review-widget, chat, tracking or retargeting scripts that are delaying product images and product information from appearing.
- Inventory every third-party integration loaded on PDP, category and checkout pages.
- For each, ask whether it is really necessary on that page; remove the ones that are not.
- Load the remaining integrations only after the main page — product images and product info — has fully loaded, so the merchandising content wins the race.
- Re-measure after removing and deferring to confirm the main content actually paints earlier, not just that total page weight fell.
Caveat: Some integrations (payments, fraud, personalization) may need to load earlier than others; the source's rule is about deferring the rest, not removing essential functionality.
Caveat: Deferring a script can change how analytics or attribution fire — check reporting accuracy afterward.

Tags: speed, third-party-scripts, resource-optimization, product-page, measurement
Source: Page Speed Optimization_ How to Improve the Loading Time of Your Online Shop.docx

---

## Choose SSR or Hybrid Rendering for Faster First Display
Use when: Evaluating rendering architecture for a shop whose JavaScript-heavy pages feel slow on mobile connections even after resource fixes.
- Recognize the two options: client-side rendering, where the visitor's browser does the main work and performance depends heavily on their internet connection; and server-side rendering (SSR), where the server does that work and the page displays directly and faster.
- Accept the trade-off: SSR demands more power from the server but is more reliable for the shopper.
- Adopt a hybrid approach — the server handles complex, heavy processing; the browser handles lighter, immediate interactions — to reduce server load while keeping responsiveness.
- Re-test FCP, TTI and LCP after switching rendering mode, since the metric that improves may not be the one you assumed.
Caveat: SSR is a fundamental architectural change, not a quick tweak — the source frames it alongside other longer-term adjustments.
Caveat: Server capacity and cost must be sized for the added rendering load before committing.

Tags: speed, rendering, ssr, architecture, mobile, technical-seo
Source: Page Speed Optimization_ How to Improve the Loading Time of Your Online Shop.docx

---

## Serve Static Assets From a CDN Close to the Shopper
Use when: Serving shoppers across regions or countries where a single-origin host makes image and file delivery slow for distant customers.
- Identify static assets — images and files in particular — that are currently served only from your origin.
- Put a content delivery network in front so that content is temporarily stored on globally distributed servers.
- Ensure each shopper is served from the server geographically closest to them.
- Pair the CDN with the device-specific image sizing from your image work so the nearest server is also sending the right-sized file.
Caveat: A CDN improves delivery of cached static content; it does not fix server-side rendering or API logic problems.
Caveat: Cache invalidation for frequently changing product images and pricing needs a plan.

Tags: speed, cdn, resource-optimization, images, infrastructure, global
Source: Page Speed Optimization_ How to Improve the Loading Time of Your Online Shop.docx

---

## Layer Caching in Browser and on Server Without Over-Relying On It
Use when: Repeatedly serving the same product data across category listings and product pages where re-fetching is adding latency.
- Cache product data and other content so it is available more quickly, both in the user's browser and on the server.
- Treat caching as one layer, not the answer: the source notes that fast, well-structured APIs reduce the amount of caching needed to deliver the same content.
- Measure before and after caching changes to confirm the shopper-visible paint actually moved.
- Review cache lifetimes against how often product data — stock, price, promotions — actually changes.
Caveat: Caching stale product data risks showing wrong prices or availability; set lifetimes against your actual data volatility.

Tags: speed, caching, api, infrastructure, product-data
Source: Page Speed Optimization_ How to Improve the Loading Time of Your Online Shop.docx

---

## Structure APIs for Precise Data Selection and Smaller Payloads
Use when: Optimizing the data layer behind category grids, search results or product pages that return more fields per product than the page renders.
- Make interfaces quick and efficient first — slow APIs force more caching to compensate.
- Design a clear structure that lets the caller select exactly which data should be loaded for a given page or component.
- Request only the fields a view actually renders, rather than pulling the full product object for a listing tile.
- Track the resulting reduction in response payload and loading time, and expect less caching to be needed once the payload is lean.
Caveat: Field selection requires agreement between front-end views and API contracts; uncoordinated changes can break pages.
Caveat: The source presents this as a contributor to page speed, not a standalone fix for a fundamentally slow server.

Tags: speed, api, architecture, resource-optimization, product-data
Source: Page Speed Optimization_ How to Improve the Loading Time of Your Online Shop.docx

---

## Prioritize Speed Work With the Latency and Abandonment Evidence
Use when: Justifying a speed optimization budget to stakeholders or deciding how aggressively to invest in performance before other store projects.
- Lead with the revenue link: per Akamai, a delay of just 100 milliseconds in loading time can reduce the conversion rate by about 7%.
- Present the three-second abandonment threshold: 53% of mobile visitors leave a page immediately if it takes more than three seconds to load.
- Use expectation data to set targets: 47% of online shoppers expect page load in two seconds or less.
- Factor in retention risk: 79% said they would be less likely to shop again on a page they thought was too slow.
- Add the SEO angle — slow shops invite high bounce rates that send negative signals to Google and other search engines, hurting organic ranking, while fast loaders are rated positively.
Caveat: These figures are third-party study statistics (Akamai and survey data) cited by the source, not measured outcomes for any specific store; treat them as direction, not a guaranteed conversion lift.
Caveat: Page speed is one ranking factor among many, not the sole determinant of search position.

Tags: speed, benchmarks, conversion-optimization, business-case, retention, technical-seo
Source: Page Speed Optimization_ How to Improve the Loading Time of Your Online Shop.docx

---

## Ecommerce page speed: conversion, ranking and ad-spend impact
Use when: Deciding whether to prioritise speed work on the store roadmap, or building the business case for image, plugin and caching fixes.
- Frame speed as a revenue lever, not an IT chore: the source reports that even a one-second delay can reduce conversion rates by up to 7%, and that stores loading under one second can convert up to three times better than stores taking around five seconds. Treat these as source-cited benchmarks, not guarantees for your store.
- Connect speed to acquisition economics: with paid ads you pay per click, so a slow landing or product page burns budget on visitors who leave before seeing the offer — speed improvements raise the effective ROI of the same spend.
- Account for Google rankings: Core Web Vitals are official ranking factors, so a slow store can rank below competitors with weaker products or content.
- Prioritise mobile: the source states 66% of online revenue comes from smartphones and tablets, so measure and fix mobile experience first rather than desktop.
- Translate the case into a testable internal target (e.g. cut LCP or TTFB on the top-revenue templates) and re-measure conversion and bounce before/after.
Caveat: The 7% conversion drop and 3x conversion uplift are reported benchmark figures from the source, not measured outcomes for any specific store; your own traffic, device mix and baseline matter.
Caveat: Speed alone will not rescue bad merchandising, pricing or traffic quality — treat it as one input to conversion.

Tags: speed, conversion-optimization, core-web-vitals, acquisition, measurement, mobile, roi
Source: Page speed guide for ecommerce store operators_ diagnosis and actions.docx

---

## Track three Core Web Vitals plus diagnostic TTFB on store templates
Use when: Diagnosing which experience metric is hurting a homepage, category page, PDP or checkout, and setting fix priorities.
- LCP (Largest Contentful Paint) — time until the largest visible element loads, typically the homepage hero or the PDP product image. Target under 2.5 seconds. If it fails, shoppers may doubt the store's credibility or functionality before they even see the product.
- CLS (Cumulative Layout Shift) — visual stability of elements. Target under 0.1. High CLS causes misclicks when buttons or elements move just before a tap; the source notes the worst case is purchase abandonment from frustration with an unstable interface.
- INP (Interaction to Next Paint) — responsiveness to interactions such as clicking 'Add to cart'. INP replaced First Input Delay (FID) in March 2024. Target under 200 milliseconds. Delayed response in checkout makes users click repeatedly or abandon because they are unsure their input registered.
- TTFB (Time to First Byte) — server response time from request to first byte. Target under 800 milliseconds, which the source notes is often harder to achieve in ecommerce because of dynamic carts.
- Read TTFB as a foundation signal: poor TTFB points to slow hosting or an overloaded database, and frontend work can only do so much if the base is weak.
Caveat: Editorial correction: LCP, INP and CLS are the three Core Web Vitals; TTFB is diagnostic. Assess the 75th percentile separately for mobile and desktop. https://web.dev/articles/vitals

Tags: speed, core-web-vitals, lcp, cls, inp, ttfb, measurement, product-page, checkout
Source: Page speed guide for ecommerce store operators_ diagnosis and actions.docx

---

## Where ecommerce stores lose speed: five common killers
Use when: Running a speed audit on a live store to decide which fix class will recover the most seconds.
- Unoptimized images: high-resolution product photos are needed for sales, but PNG/JPEG inflate page weight. Modern formats (WebP/AVIF) cut file size 30–50% at the same quality. Images can make up more than 60% of a page's total data volume, making them the biggest lever.
- Third-party scripts: tracking pixels, chat widgets, review platforms and social embeds each load their own JavaScript and block rendering. In many stores these external requests account for more than 50% of total load time.
- Plugins: every app or plugin loads its own stylesheets and scripts. Especially harmful are plugins that run complex database queries on every page load without caching results.
- Missing caching: without it, the server rebuilds each page on every click — querying databases, calculating prices, assembling layouts. Full-page caching instead serves a pre-rendered version, sharply cutting response times.
- Site-wide CSS/JS: many themes load functionality on every page even when only one subpage needs it, so mobile browsers download and process unused code.
Caveat: The >50% script share and >60% image data share are source-reported typical figures, not fixed proportions in every store; confirm with your own audit.
Caveat: Do not remove review, chat or tracking scripts purely on speed grounds without checking their revenue or operational role.

Tags: speed, performance-audit, images, third-party-scripts, plugins, caching, mobile
Source: Page speed guide for ecommerce store operators_ diagnosis and actions.docx

---

## Baseline first: measuring speed before you change anything
Use when: Starting any speed project on a store, or when you need evidence that a technical change actually helped.
- Run Google PageSpeed Insights for your URL on both mobile and desktop before touching anything, since mobile and desktop scores diverge and your mobile traffic is the larger revenue share.
- Record the LCP value (and other CWV values) plus the overall score for each template you care about — homepage, key category pages, best-selling PDPs, cart and checkout.
- Keep a dated change log in plain text, e.g. 'March 15 – image compression enabled', so you can tie observed metric shifts to specific actions instead of arguing about causes.
- Repeat the same measurements after each change class (images, plugins, caching) rather than bundling everything, so you can tell which lever produced which gain and roll back anything that regresses.
- Use the before/after numbers as the internal evidence for continuing or stopping further investment in speed work.
Caveat: PageSpeed Insights is Google's tool and its interface and scoring can change — verify current reports when you run it.
Caveat: Lab scores do not equal real-user field data; treat them as directional for prioritisation.

Tags: speed, measurement, core-web-vitals, performance-audit, experiment-design, pagespeed-insights
Source: Page speed guide for ecommerce store operators_ diagnosis and actions.docx

---

## Optimise product images with WebP/AVIF and responsive sizes
Use when: Reducing PDP and category page weight while keeping product photography high-resolution enough to sell.
- Convert legacy PNG and JPEG assets to WebP or AVIF, which the source reports reduce file size by 30–50% at the same visual quality — the highest-leverage single fix when images are the bulk of page data.
- For a small number of images, convert them manually with free browser-based tools; for a catalogue-scale store, use platform automation instead of hand-editing.
- On Shopware 6, rely on automatic WebP generation for uploaded source images and automatic thumbnail sets that produce multiple sizes per product, so each device gets an appropriately sized file.
- Keep the original high-resolution source so you can regenerate renditions if your format or size strategy changes.
- Re-measure LCP on your hero image (homepage) and main product image (PDP) after conversion, since these are the elements LCP scores.
Caveat: Shopware automation details are platform-specific; other carts need equivalent plugins or CDN image services — verify your platform's current capabilities.
Caveat: Format support and compression results vary by image type; check visual quality on product close-ups before bulk converting.

Tags: speed, images, webp, avif, product-page, resource-optimization, shopware
Source: Page speed guide for ecommerce store operators_ diagnosis and actions.docx

---

## Plugin and script audit: earn each extension its place
Use when: Cleaning up accumulated plugins, apps and marketing pixels that slow rendering on store pages.
- Open your plugin list in the admin panel and review it from top to bottom, asking of each one: 'How does this plugin currently contribute to revenue?'
- Flag the usual offenders: marketing pixels, unused design effects, chat widgets and plugins that run uncached database queries on every page load.
- Disable uncertain plugins in a staging environment — not on live — then measure page speed again and compare against your baseline.
- Remove unused plugins completely rather than merely deactivating them, since leftover code and assets can still be loaded or interfere.
- Repeat the loop for third-party scripts: every tracking pixel, review widget, chat tool and social embed adds blocking JavaScript, so only keep those whose measured value justifies their cost.
Caveat: Never disable tracking or review scripts on live without confirming you are not breaking attribution, customer service or social proof.
Caveat: Staging environments may not replicate production traffic or caching, so confirm gains on live after a controlled rollout.

Tags: speed, plugins, third-party-scripts, performance-audit, staging, measurement
Source: Page speed guide for ecommerce store operators_ diagnosis and actions.docx

---

## Server-side foundation: caching, PHP and HTTP/3
Use when: Escalating to your host or IT team after content-level fixes, when TTFB or overall response time is still poor.
- Finish content and plugin work first: the source explicitly advises contacting your provider only after steps 1–3, otherwise support will simply point at your unoptimized images and scripts.
- Ask specifically whether server-side caching such as Redis or Varnish is active, and whether full-page caching delivers pre-rendered HTML instead of rebuilding pages (querying databases and recalculating prices) on every click.
- Ask for the current PHP version and whether your stack is on PHP 8.2+ and HTTP/3; these are the modern server technologies the source recommends as the foundation for all further optimisation.
- In SaaS or cloud environments, many settings may already be optimised — still review the documentation and confirm rather than assume.
- After infrastructure changes, re-run your baseline measurements for TTFB and LCP to verify the server improvement reached the storefront.
Caveat: These stack recommendations reflect the source's guidance and will age; verify current supported PHP and HTTP versions before requesting changes.
Caveat: Infrastructure changes can interact badly with checkout and cart logic — test transactional flows after any caching or protocol change.

Tags: speed, caching, redis, varnish, ttfb, hosting, infrastructure
Source: Page speed guide for ecommerce store operators_ diagnosis and actions.docx

---

## Platform-native caching and intelligent cache invalidation
Use when: Choosing or configuring an ecommerce platform's performance features, especially where price and stock updates must not serve stale pages.
- Use the platform's integrated HTTP cache so repeat visits are served pre-rendered HTML rather than re-executing PHP and querying the database.
- Rely on native WebP generation for uploaded images and automatic thumbnail sets so each device receives an appropriately sized file without a custom pipeline.
- Understand intelligent cache invalidation: the platform detects price or stock changes and clears only the affected pages rather than purging the entire site cache — keeping the store fast without displaying outdated prices or availability.
- Confirm your platform also bundles and optimises required CSS and JavaScript, avoiding site-wide loading of code needed on only one subpage.
- Where your platform lacks these features, look for equivalent automatic image conversion, responsive thumbnail generation and selective cache purging before building custom tooling.
Caveat: Shopware 6 is the source's example of a platform with these native features; other platforms differ, so verify current capabilities in your own admin and documentation.
Caveat: Selective invalidation depends on correct price/stock event wiring — test that price and availability changes actually propagate before trusting the cache.

Tags: speed, caching, shopware, images, webp, platform-configuration, inventory
Source: Page speed guide for ecommerce store operators_ diagnosis and actions.docx

---

## Prioritised speed roadmap for a store
Use when: Planning a multi-week speed programme and deciding what to do first with limited developer or agency time.
- Step 1 — Baseline: run PageSpeed Insights for mobile and desktop, log LCP and the overall score, and start a dated change log.
- Step 2 — Images: convert to WebP/AVIF and serve responsive sizes, since images are typically the largest share of page data and the cheapest early win.
- Step 3 — Extensions: review plugins top to bottom against revenue contribution, disable candidates in staging, measure, then delete unused ones completely and trim non-essential third-party scripts.
- Step 4 — Infrastructure: with content and scripts cleaned up, ask your host or IT about PHP version and Redis/Varnish server-side caching, and confirm PHP 8.2+ / HTTP/3.
- Throughout: use full-page caching with intelligent invalidation so price and stock changes clear only the affected pages, and re-measure after each stage so gains are attributable.
Caveat: The sequence is the source's recommended order, not a universal law — a severely underpowered server may justify infrastructure work earlier, but expect reduced credibility with support if content is still unoptimised.
Caveat: Each stage should be re-measured; bundling all changes makes it impossible to know which one helped.

Tags: speed, roadmap, performance-audit, images, plugins, caching, measurement
Source: Page speed guide for ecommerce store operators_ diagnosis and actions.docx

---

## Remove residual Shopify app code from theme files
Use when: Auditing loading performance on a Shopify store after installing, trialing or uninstalling speed or marketing apps, before concluding the theme itself is slow.
- Inventory apps you have installed or trialed, noting each app's brand name (for example 'loox') because leftover snippets usually contain the app name or its CDN domain.
- Search theme files for those names: theme.liquid, head.liquid and footer.liquid are the paths to check. A Chrome extension such as Shopify Theme File Search lets you grep across the theme instead of opening files one by one.
- Delete the lingering <script> tags you find. Uninstalling an app does not always remove its injected code, and any surviving tag keeps making requests to an external server on every page load.
- Re-test the storefront after each removal so you can attribute any change in load behavior to a specific deletion rather than a batch edit.
- Repeat this cleanup periodically, especially after trial installs, since each app adds independent risk of residual code.
Caveat: Only remove snippets tied to apps you have actually uninstalled; deleting code for an active app breaks its function.
Caveat: Keep a backup or version record of theme files before editing Liquid directly.

Tags: speed, shopify, theme-optimization, resource-optimization, liquid, technical-seo, site-audit
Source: Page speed.docx

---

## Format and size images and videos for faster load
Use when: Merchandising product images, hero banners or category tiles on a Shopify store, or diagnosing pages that load slowly because of large media assets.
- Keep image file sizes under 1MB as the working ceiling for storefront assets.
- Choose JPEG instead of PNG unless the image genuinely requires transparency; PNG files are usually much heavier for photographic content.
- Replace heavy animated GIFs with compressed MP4 video embedded via an HTML <video> tag, which delivers the same motion at far smaller file size.
- Apply video loading behavior deliberately: set preload="none" on videos so the browser does not eagerly fetch media the shopper has not reached yet.
- Apply loading="lazy" to off-screen images so they are only fetched as the shopper scrolls toward them.
- Do not lazy load above-the-fold assets such as the hero image; those should load immediately to keep LCP low.
Caveat: Lazy loading the hero image works against LCP rather than helping it.
Caveat: Transparency requirements and animation content determine whether the JPEG or GIF-replacement advice applies to a given asset.

Tags: speed, image-optimization, product-page, media-sizing, lazy-loading, core-web-vitals, shopify
Source: Page speed.docx

---

## Lazy load below-fold media, preload the hero
Use when: Structuring a product page, landing page or homepage where the hero image and other above-the-fold media compete with below-fold content for bandwidth.
- Identify the assets visible in the initial viewport, typically the hero image and any headline banner. These are the ones that determine LCP.
- For above-the-fold assets, do not apply loading="lazy". Instead add a preload link in the <head> so the browser fetches them at the earliest opportunity.
- For every image below the fold, add loading="lazy" so the request is deferred until the shopper scrolls near it.
- For embedded videos, set preload="none" to prevent the browser from downloading video data on page load.
- Re-check after restructuring that the hero still renders promptly and that below-fold content does not appear late or jumpy.
Caveat: Applying lazy loading indiscriminately to all images including the hero is the common failure mode this addresses.
Caveat: Which asset counts as above-the-fold changes by viewport size, so check mobile and desktop layouts separately.

Tags: speed, core-web-vitals, lazy-loading, landing-page, product-page, shopify, resource-optimization
Source: Page speed.docx

---

## Reduce storefront script blocking while preserving purchase tracking
Use when: Diagnosing render-blocking scripts on a Shopify storefront, or speeding up page rendering without breaking analytics and ad tracking during acquisition campaigns.
- Inventory theme and app scripts; remove confirmed unused integrations on a duplicate theme first.
- Choose defer or async only after checking execution order, DOM dependencies and the vendor integration requirements.
- Do not impose a blanket synchronous-pixel rule. Use the supported platform integration; Shopify provides a Web Pixels API and standard event subscriptions.
- Test consent behavior, page views, variant selection, add-to-cart and a test purchase after changes; check missing and duplicate events.
Caveat: Editorial correction: source advice that all pixels must remain synchronous is not a universal requirement. Verify the specific integration. https://shopify.dev/docs/api/pixels

Tags: speed, script-optimization, shopify, liquid, resource-optimization, acquisition, measurement
Source: Page speed.docx

---

## Load non-critical CSS asynchronously with the media=print trick
Use when: Cutting render-blocking CSS on product, category or landing pages where multiple stylesheets delay first paint.
- Identify stylesheets that are not required for the initial render, such as styles for modals, below-fold sections or secondary components.
- Rewrite those link tags as <link rel="stylesheet" href="..." media="print" onload="this.media='all'">. The browser treats the print stylesheet as non-render-blocking and downloads it without stalling paint.
- Leave critical above-the-fold CSS loaded normally, since it is needed for first render.
- Apply the same async pattern to any additional non-critical stylesheets you introduce later.
- Test the page visually after the change to confirm the deferral did not cause a flash of unstyled content in areas the shopper sees immediately.
Caveat: Moving critical CSS into this pattern can leave the visible page unstyled on first paint.
Caveat: This is a specific HTML attribute technique; verify the markup still behaves as expected in the current browser and theme context.

Tags: speed, css-optimization, resource-optimization, shopify, theme-optimization, core-web-vitals
Source: Page speed.docx

---

## Set font-display: swap to prevent invisible text
Use when: Fixing slow text rendering, low perceived speed or a flash of invisible text on product pages that use custom brand fonts.
- Open the stylesheet containing the store's @font-face declarations.
- Add font-display: swap to each @font-face rule. This tells the browser to render text in a fallback system font immediately and swap in the custom font once it loads.
- Without swap, the browser can leave text blank until the custom font finishes downloading, which reads as a broken or slow page to the shopper.
- Confirm the change covers all custom font declarations, including weights and italic variants loaded separately.
- Review the page after the change to ensure the swap does not introduce disruptive layout shift when the brand font replaces the fallback.
Caveat: Swap improves perceived speed but can cause a visible font switch; check that fallback and brand fonts have similar metrics to limit reflow.
Caveat: Custom font files should still be reasonably sized; font-display only changes how the wait is presented.

Tags: speed, fonts, perceived-performance, product-page, css-optimization, shopify
Source: Page speed.docx

---

## Approach speed work as rendering mechanics, not app shortcuts
Use when: Deciding how to allocate effort on a Shopify speed problem, choosing between installing a speed app and editing theme code, or setting a performance baseline for the storefront.
- Treat loading performance, browser rendering, perceived performance, resource optimization, Core Web Vitals, caching and file-size reduction as the core problem set.
- Work on the actual mechanisms: defer non-essential scripts, remove leftover app code from Liquid templates, size and format media correctly, and use CSS media attributes to load non-critical styles.
- Be skeptical of approaches aimed mainly at spoofing Lighthouse scores rather than improving real rendering and load behavior, and of general complaints about pushy apps or speed specialists that do not identify a concrete fix.
- Keep paid social creative formats and true incremental ROAS or pixel/CAPI setups in their own workstreams, since they are separate from loading performance.
- Establish a baseline measurement before editing so speed changes can be judged against it.
Caveat: The source's framing of speed work as theme-level mechanics is a stance; some stores may still need managed hosting or app-level solutions.
Caveat: Perceived-performance changes are not always captured by a single synthetic score.

Tags: speed, shopify, perceived-performance, resource-optimization, core-web-vitals, theme-optimization, site-audit
Source: Page speed.docx

---

## Shopify image pipeline audit: what Shopify does and doesn't optimize
Use when: Auditing product images or theme assets for page speed on a Shopify store
- Recognize the free wins already in place: Shopify serves images from a CDN (copies propagate to regional servers, so distant customers download locally) and lazily generates width variants from one upload via URL filters such as appending ?width=493, so the theme can request a smaller rendition instead of the master file.
- Verified behavior on a test store: a 9.8 MB upload was auto-reduced to roughly 6.1 MB on delivery, but the presenter recommends 500 KB as the practical ceiling — meaning out-of-the-box compression is real but conservative. Do not assume upload equals optimized.
- Shopify also serves WebP automatically to browsers that support it (a JPEG upload downloads as .webp). Do not pre-convert your catalog to WebP: if you serve only WebP and a browser doesn't support it, shoppers see no image. Upload JPEG/PNG and let Shopify handle format negotiation.
- Find the gaps: (1) large dimensions are not reduced enough, (2) the wrong source format (PNG/GIF where JPEG would do) cannot be repaired by Shopify, (3) whether a theme requests multiple widths is determined by the theme code, not Shopify.
- Prioritize images because they are among the heaviest assets and the part you can actually control, unlike apps and platform code.
Caveat: Shopify's internal dashboards and CDN behavior change over time — verify current upload sizes and filter parameters in the live admin before building a process around specifics.
Caveat: The 500-600 KB ceiling and the 6.1 MB observation are this presenter's test values, not Shopify-published benchmarks.

Tags: speed, image-optimization, shopify, cdn, webp, page-speed, technical-seo
Source: Page speed.docx

---

## Check whether your theme serves responsive image widths
Use when: Diagnosing slow mobile PDP or homepage load on a custom, agency-built or older Shopify theme
- Open Online Store → Themes → Edit code and open a section or snippet that renders an image (hero, image-with-text, product grid).
- A bad pattern looks like a single img src pointing at image.url or image | img_url: 'master'. That means every device — phone and 4K desktop alike — downloads the identical original file, so a 5,000px upload is delivered to a 400px screen.
- The desired pattern is a srcset (or equivalent srcset-style Liquid filter) offering several widths, e.g. a 1,600px default plus entries for 800px and 1,200px, so the browser fetches the smallest adequate file.
- If your theme is old, custom or agency-modified, audit all image-bearing sections rather than one: sections added later by developers often skip the responsive pattern even when the base theme uses it.
- Fix or have fixed the offending sections; the presenter calls this the first thing to check on a store, because the payoff is immediate and applies to all traffic, especially mobile.
Caveat: Newer Shopify themes generally follow this practice; old or heavily customized themes are the usual offenders.
Caveat: Verifying responsive behavior requires reading theme code or inspecting network requests per viewport, which many merchants cannot do alone.

Tags: speed, image-optimization, shopify-liquid, srcset, responsive-images, theme-development, mobile
Source: Page speed.docx

---

## Choose JPEG, PNG, WebP or MP4 by image role
Use when: Preparing product photos, banners, logos or animated promos before upload
- Default for photography and any rectangular image without transparency: JPEG. It supports lossy compression, which the human eye largely cannot detect at sensible settings, and Shopify converts it to WebP.
- Use PNG only when you need transparency or crisp flat graphics: cut-out product shots that must sit on a colored section, logos, and illustrations layered over other content. In the example store, a transparent cut-out product and a transparent logo justified PNG; the same product on a white background could have been a better-compressing JPEG.
- Avoid PNG for ordinary opaque photos. Demonstrated cost: the identical image re-exported as PNG with no edits went from 2.7 MB to 8 MB purely from the format.
- Avoid GIF for animation. Use MP4 video in an HTML video tag instead — it loads far better than an animated GIF.
- Lossless (PNG) preserves quality for further editing; lossy (JPEG) discards detail you mostly cannot see and is the format for delivery. You can still compress PNGs, so an oversized PNG is never necessary.
Caveat: Do not convert and upload WebP yourself; Shopify's automatic conversion is what keeps non-supporting browsers served.
Caveat: Format advice assumes normal ecommerce viewing; print or archival use has different requirements.

Tags: speed, image-optimization, file-formats, jpeg, png, webp, video, product-photography
Source: Page speed.docx

---

## Size and compress product images before upload
Use when: Preparing a photo shoot or supplier image drop for a product launch or catalog refresh
- Resize the long edge. The presenter's rule: never upload larger than 3,000px, and 3,000 is already overkill — 2,000px is enough for hero banners, zoom and retina on typical Full HD and 4K screens. Because screens downscale, an 8,000px image and a 2,000px image look effectively the same on a 3,000px-wide display.
- Size to the box, not the screen. A 600x600 grid tile should receive roughly a 600px-class image; feeding it 5,000px wastes bandwidth (a ~3 MB asset where ~60 KB would do). Only full-bleed elements like a hero justify near screen width.
- Compress with a visual preview. A tool with a live preview (the presenter uses Squoosh) lets you drag the quality slider and stop when artifacts appear: at quality 40 a 2.7 MB image landed at 172 KB with no difference the presenter could see, and quality 20-30 remained acceptable in his view.
- Ceiling guidance: stay under 500-600 KB, and preferably 100-200 KB. A real reference point from an example store: a 1,920x1,920 zoomable product image at 46 KB looked fine.
- Do image resizing and format conversion before upload. Shopify's built-in editor can resize and change aspect ratio, but offers no compression settings — so an oversized upload stays oversized in weight.
Caveat: Numbers are the presenter's working thresholds, not a universal standard; heavily textured images may need higher quality settings to avoid visible artifacts.
Caveat: Fine line art, small text in images and print use tolerate compression far less well.

Tags: speed, image-optimization, compression, product-photography, squoosh, page-speed, catalog-management
Source: Page speed.docx

---

## Batch resize in Preview, crop individually, then convert format
Use when: Processing a folder of photographer or supplier images before loading them into Shopify
- Keep a folder of same-orientation images, select them all, open in macOS Preview, then Edit → Select All and Tools → Adjust Size. Set the larger dimension (e.g. 4,000) down to 2,000 and apply — this resizes the whole batch in one pass.
- Do not batch crop. Product framing differs image to image, so a shared crop rectangle decapitates some products. Crop manually instead: in Preview use the selection tool, hold Shift to constrain to a square, position it, then click the crop icon.
- Export to JPEG or PNG: File → Export lets you change the format (e.g. iPhone HEIC to JPEG) and apply compression in one step, with a file-size readout.
- Understand the limitation of that export dialog: it shows resulting file size but not image quality, so you are accepting the setting blind. For control, do the compression step in a preview-based tool where you can see the result.
- This sequence (resize → crop → convert → compress → rename → alt text → upload) is the recommended order; doing it in another order creates rework.
Caveat: Bulk resizing assumes uniform orientation; mixing portrait and landscape in one batch will resize the wrong axis.
Caveat: Windows equivalents exist but the presenter only demonstrates the macOS Preview workflow.

Tags: speed, image-optimization, workflow, compression, product-photography, batch-editing
Source: Page speed.docx

---

## Automate image compression for large catalogs
Use when: Running a store with a large or already-loaded image catalog that needs compressing at scale
- Estimate the workload first: manual per-image compression with a preview tool works for a handful of hero or launch images, but for a large catalog — especially images already uploaded to Shopify — it is a lot of repetitive manual work.
- Install an image optimization app (the presenter uses Tiny SEO Speed and Image Optimizer) and enable automatic compression of images as they upload, so compression stops being a step you remember to do.
- Check the app's optimization report for per-image savings from actual runs. In the presenter's example, individual images lost more than 80% of their file size after optimization.
- Treat size reduction as a bandwidth and experience win for the shopper, not only a Lighthouse number.
- Keep the manual pipeline for launch hero images and for anything the app compresses too aggressively, since you control quality only in a preview tool.
Caveat: Installing an app adds its own scripts and can offset speed gains from compression — measure before and after.
Caveat: App results and features vary; verify current app capabilities in the Shopify App Store, as interfaces change.
Caveat: Some apps also alter SEO fields; review their settings rather than accepting defaults.

Tags: speed, image-optimization, apps, shopify, compression, automation, catalog-management
Source: Page speed.docx

---

## Fix messy product grids with Shopify's crop and resize tools
Use when: Product grid or collection page looks uneven because uploaded images have mixed aspect ratios
- Establish the grid's aspect ratio first. Commonly used online: square for general product grids, and 4:5 portrait for fashion, which fits a full-body model shot better.
- Fix already-uploaded images without re-uploading: open the image in the Shopify media editor, use crop and transform to pick the target ratio (square is offered as a preset), drag the crop frame to keep the whole product in view, then Apply.
- Resize dimensions in the same editor if the file is oversized; the presenter changed 3,000 to 1,920 for a square product image as a sufficient size for zoom.
- Save, then refresh the collection page to confirm the grid is aligned.
- Prevent the problem upstream: crop to the target ratio before upload, since a tall image added to a square grid renders visibly out of step with its neighbors.
Caveat: Shopify's in-admin editor resizes and crops but offers no compression settings, so its output can remain heavier than a properly compressed pre-upload file.
Caveat: Changing the main image's crop changes how the product appears in collection grids; check the storefront, not just the admin preview.

Tags: speed, image-optimization, merchandising, product-grid, aspect-ratio, shopify-admin, product-page
Source: Page speed.docx

---

## Plan a product image set: 3-5 images that each answer a question
Use when: Planning a product photo shoot or deciding which images to add to a PDP
- Start with the minimum that answers buying questions: three to five images. One is workable, two is better, three to five covers most stores.
- Cover the four functional slots: a main hero shot, an alternate angle (side, back or top depending on the product), a detail shot showing a feature, and a lifestyle shot of the product in use or held.
- Add more depth for higher-priced or more complex products, where extra angles, kit contents and multiple usage scenarios help the shopper imagine owning the item and justify the price. Reference examples show footwear/apparel and sporting goods running the four-slot pattern, plus video.
- Test a reordered gallery when the product is aspirational: the presenter suggests main image, alternate angle, lifestyle, then details, so the shopper imagines ownership first and resolves objections second.
- Stop adding when no image is answering a new question — filler images add page weight and make mobile scrolling excessive.
Caveat: The 3-5 figure is a practical heuristic, not a measured conversion threshold.
Caveat: Extra images are only affordable if they are correctly sized and lazy-loaded, otherwise they degrade mobile performance.

Tags: speed, merchandising, product-page, product-photography, conversion-optimization, mobile
Source: Page speed.docx

---

## Name image files with keyword-first descriptive filenames
Use when: Renaming a folder of product images before uploading them to Shopify
- Reject camera/supplier filenames (random strings, IMG_1234) — they give search engines nothing to categorize the image with, so you lose an SEO opportunity at upload time. For images already uploaded with bad names, replacing the file is the practical remedy.
- Use the formula: main keyword + product descriptor + unique detail + shot angle. Examples from the source: leather-wallet-men-brown-back, leather-wallet-men-stitched-detail.
- Generate these at scale by prompting ChatGPT with a template: supply the main keyword (sports backpack), the descriptor (men), and a comma-separated list of per-image details (black front, top detail, on the shoulder, back, front detail), and take the resulting filenames.
- Review the output — in the demonstration the model produced more filenames than images existed, so match names to files deliberately rather than pasting blindly.
- Do this before upload, alongside resizing and compression, so each file goes up once, correctly named.
Caveat: Filename is a categorization signal only; it is never shown to shoppers. Alt text carries the user-facing and semantic description.
Caveat: AI-generated names still need human review for accuracy of color, angle and product detail.

Tags: technical-seo, image-optimization, product-page, file-naming, keyword-research, shopify
Source: Page speed.docx

---

## Write alt text that describes the image, not a sales pitch
Use when: Adding or auditing alt text across product images, collection banners and blog images
- Write a plain description of what is in the frame, as a sighted shopper would describe it: 'men wearing a black sports backpack outdoors' or 'closeup of padded shoulder straps on a black sports backpack'.
- Use the filename for initial categorization and alt text for meaning — Google uses both, and alt text is also the text that displays when an image fails to load, so the page still communicates.
- Accessibility is a real functional reason, not a checkbox: visually impaired shoppers navigate the store through this text, and missing alt text shuts them out.
- Avoid promotional copy in alt text ('leather wallet man black buy cheap'). The presenter's position is that this is poor practice — though still better than no alt text at all, since the image at least stays indexed.
- Do it for every shot in the gallery, matching each alt text to that specific angle or detail rather than repeating the product name.
Caveat: The source treats ad-laden alt text as a mistake but explicitly ranks it above blank alt text; the trade-off is indexation versus quality.
Caveat: Alt text must not be used to stuff keywords — the examples are natural sentences.

Tags: technical-seo, accessibility, image-optimization, product-page, alt-text, content-quality
Source: Page speed.docx

---

## Upload product images and assign variant images so color swatches switch the gallery
Use when: Building a new product page or adding a new color variant with its own photography
- Know the entry points: images can be uploaded from Content → Files (the media library), directly on the product creation page (upload new or select existing), on collection pages for cover images, on blog posts, and through the theme customizer for section images. Everything lands in the same media library.
- On the product page, drag to set the order: main image first, then alternate angle, then lifestyle and details (or details before lifestyle if you prefer question-answering order). Save.
- For variants, assign per-option images. In the product editor, each variant row has a plus icon; click it to attach the matching image (e.g. the red backpack for the red variant). After saving, the variant icon shows the assigned thumbnail.
- Add new variant photography by uploading through the same plus flow, then click Done and Save so the swatch updates.
- Confirm on the storefront: clicking color swatches should swap the gallery image, and variant images should also appear further down the product page.
Caveat: Assign every variant a real image — an unassigned variant shows the generic placeholder and can confuse shoppers choosing a color.
Caveat: Gallery order and variant behavior are theme-dependent; verify in the live theme, not just the admin.

Tags: product-page, merchandising, variants, shopify-admin, image-optimization, product-media
Source: Page speed.docx

---

## Reuse one media-library file per image and use Replace to update everywhere
Use when: Maintaining a media library where product, collection, blog and theme images overlap
- Upload a given image once and select it from the media library wherever it is needed — product page, collection cover, blog, theme section — rather than uploading the file again.
- Understand the consequence of duplicates: uploading the same filename twice produces a second file with a modified, gibberish-suffixed URL. SEO suffers, and future edits multiply.
- Use Replace image in the media library when the asset changes. The URL is preserved and only the file is swapped, so every place the image appears — product pages, sections, collections — updates at once. This is the payoff for not having duplicates.
- With duplicates, this efficiency disappears: you must locate every copy and replace each individually.
- If your media library already has duplicates, consolidate to a single canonical file before a major image refresh.
Caveat: Replacing a file changes every usage, including hero images where the new crop may not fit — check each placement after replacing.
Caveat: Reusing one file across product and banner contexts may force one crop to serve two different aspect ratios.

Tags: image-optimization, shopify-admin, media-library, technical-seo, workflow, merchandising
Source: Page speed.docx

---

## Diagnose whether images are a plausible cause of your speed problem
Use when: Deciding where to start on a Shopify speed project or whether to invest in image cleanup
- If you run an older theme that doesn't receive updates, check images: old themes often don't follow current responsive-width practice, so a single large asset may be served to every device.
- If your theme was built or heavily modified by an agency or developer, audit the image tags in its sections — quality varies by builder. Large catalogs with many images per product compound the problem.
- If a large share of traffic is mobile, treat images as high priority: mobile devices neither need nor handle large assets well, and unstable connections make heavy downloads worse.
- If your store is simple with few apps and still slow, images are a likely culprit and an easy win — compress and re-upload and you may be done.
- The presenter's broader point: apps and some platform issues are outside your control, but image weight is controllable, so it is worth doing even when other causes exist.
Caveat: The presenter works from experience, not a measurement methodology. Confirm with your own performance data before attributing slowness to images.
Caveat: Image work is easy but not a substitute for addressing other bottlenecks if images are already optimized.

Tags: speed, image-optimization, diagnostics, mobile, shopify, page-speed, prioritization
Source: Page speed.docx

---

## Lazy-load images so catalog size doesn't dictate load weight
Use when: Deciding whether a media-heavy page or long PDP can carry more images without slowing the load
- Reject the assumption that more images means a slower site. The presenter's position: image count is not the problem, as long as the correct sizes are served and images below the fold are lazy-loaded.
- Implement lazy loading so an image is fetched only when a trigger fires — a scroll into view, or a defined interaction such as a click. Demonstrated: scrolling populated images that were not downloaded on initial page load, and a click loaded a specific image on demand.
- Apply it across long pages: content-heavy pages, long PDP galleries and landing pages with many sections can hold many images without the shopper downloading everything upfront.
- Pair lazy loading with correct dimensions. Lazy loading defers weight; it does not shrink oversized files, so both steps are needed.
Caveat: Lazy loading above-the-fold hero and LCP images can hurt perceived load — keep those eager.
Caveat: Theme implementation varies; verify in the live theme, not only in the customizer, and check current best practice before changing loading attributes.

Tags: speed, image-optimization, lazy-loading, page-speed, product-page, mobile
Source: Page speed.docx

---

## Reduce storefront script blocking while preserving purchase tracking
Use when: Reducing JavaScript render blocking in a Shopify theme's liquid files
- Inventory theme and app scripts; remove confirmed unused integrations on a duplicate theme first.
- Choose defer or async only after checking execution order, DOM dependencies and the vendor integration requirements.
- Do not impose a blanket synchronous-pixel rule. Use the supported platform integration; Shopify provides a Web Pixels API and standard event subscriptions.
- Test consent behavior, page views, variant selection, add-to-cart and a test purchase after changes; check missing and duplicate events.
Caveat: Editorial correction: source advice that all pixels must remain synchronous is not a universal requirement. Verify the specific integration. https://shopify.dev/docs/api/pixels

Tags: speed, javascript, shopify-liquid, page-speed, analytics, theme-development
Source: Page speed.docx

---

## Load non-critical CSS asynchronously
Use when: Reducing render-blocking CSS on a Shopify theme
- Identify non-critical stylesheets — anything not needed for the initially visible above-the-fold content.
- Load them with the pattern link rel=stylesheet href=... media=print onload="this.media='all'". It downloads the stylesheet in the print media context, which doesn't block rendering, then swaps it to all media once loaded.
- Keep the CSS that styles above-the-fold content in a normal blocking stylesheet so the first paint is correct.
- Verify the swap actually happens by checking the rendered page and the network panel; a failed onload leaves the stylesheet applied only to print.
- Apply the same critical/non-critical split when auditing app-injected CSS, which frequently loads render-blocking assets in the head.
Caveat: This is a known hack, not a standard API; behavior depends on browser support for the onload attribute on link elements.
Caveat: If the swap fails, above-the-fold styling can break, so test across browsers after implementing.

Tags: speed, css, render-blocking, shopify-liquid, page-speed, theme-development
Source: Page speed.docx

---

## Prevent invisible-text flash with font-display: swap
Use when: Custom web fonts on a Shopify theme cause text to be invisible during load
- Open the theme stylesheet where custom fonts are declared and locate the @font-face rule.
- Add font-display: swap inside that rule. This tells the browser to render text with a system fallback first and swap in the custom font when it arrives, eliminating the flash of invisible text.
- Note the trade-off inherent in swap: users may briefly see the fallback font and then a reflow when the custom font loads. The presenter treats this as preferable to invisible text, which delays content for every visitor.
- Check other font rules too — a theme may declare several faces, and one missing swap reintroduces the problem for that weight or style.
- Test on a slow connection to confirm text is visible during font load.
Caveat: Swap produces a visible font change on load; preloading the font is an alternative if you want to shorten the fallback window.
Caveat: Theme font implementation differs — verify where the @font-face rules live in your specific theme.

Tags: speed, fonts, css, shopify-liquid, page-speed, theme-development
Source: Page speed.docx

---

## Replace animated GIFs with MP4 video in a video tag
Use when: A product page, homepage section or ad creative uses an animated GIF for motion
- Identify the animated GIFs on your store — hero banners, how-it-works sections and product demos are common places.
- Convert the animation to MP4 and embed it in an HTML video tag. The presenter states this 'will load much better than a GIF file would', which is why GIF was left out of his recommended format list.
- When auditing theme files (theme.liquid, head.liquid, footer.liquid are the paths the presenter checks), look for GIF references that should become video tags.
- Keep the same presentation intent — convert first, then verify the section still looks right, since video tags need appropriate sizing and autoplay/mute settings to replace a GIF's visual behavior.
Caveat: The source states the speed advantage of MP4 but gives no measured comparison values; treat it as directional.
Caveat: Video embedding needs correct player attributes (mute, loop, playsinline) to mimic GIF behavior, which the source does not detail.

Tags: speed, video, image-optimization, page-speed, shopify-liquid, homepage
Source: Page speed.docx

---

## Write descriptive alt text that serves accessibility and image SEO
Use when: You are finalizing product or lifestyle images on a PDP, collection page or homepage and need to set alt text.
- Write alt text that describes exactly what is in the image in natural language, as a screen-reader user would need it: 'Men wearing a black sports backpack outdoors.'
- Include the product category plus visible attributes and the view/angle: 'Closeup of padded shoulder straps on a black sports backpack' or 'Side view of black sports backpack.'
- Avoid stuffing the field with ad copy or keyword strings like 'leather wallet man black buy cheap' — the source says this is the wrong way, though still better than an empty alt field.
- To scale across many images, draft a prompt for an AI tool that takes product name, visible characteristics and a list of angles, then generate one alt text per angle.
- Paste each result into the image's alt text field (in Shopify, open the image in the editor's alt text field, or edit from Content and Files / media library) and save.
- Verify in the live page source that the alt attribute is attached to the image element.
- Applying alt text to every image is optional best practice per the source, not a speed factor — prioritize it when accessibility and image search matter for your catalog.
Caveat: The source frames this as important for visually impaired users and for Google indexing, not as a page-speed win.
Caveat: AI-generated alt text must be checked against the actual image; inaccurate descriptions mislead screen-reader users.

Tags: speed, alt-text, image-seo, accessibility, product-page, shopify, image-optimization
Source: Page speed.docx

---

## Match alt text to image angle for multi-image product galleries
Use when: You have several images per product (front, back, detail, lifestyle) and are populating alt fields for a PDP gallery.
- List the angles you actually shoot for the product — for a backpack: front view, back view, front detail, top detail, lifestyle on shoulder.
- Supply product name, visible characteristics (color, water resistance) and that angle list to your AI alt-text prompt so each output maps to one image.
- Work through the gallery image by image, pasting the matching alt text into each image and saving.
- Use the same angle-first approach when reordering gallery images so the main image, alternate angle, detail shots and lifestyle shots each carry a suitably descriptive alt string.
- Re-open the live PDP and inspect each image element to confirm every image has its own alt text rather than a duplicated default.
Caveat: The source's angle list is an example for one backpack, not a fixed gallery structure; derive angles from what your own images show.
Caveat: Some platforms auto-fill alt text from the filename, so verify overrides actually saved.

Tags: speed, alt-text, product-page, image-optimization, shopify, merchandising
Source: Page speed.docx

---

## Resize images to just above their display box
Use when: You inspect a PDP, hero banner or content section and find the image's intrinsic size far exceeds the size it is displayed at.
- Right-click the image in the browser and choose Inspect to read its rendered/intrinsic dimensions against the box it occupies.
- Note the display box width — e.g. a section image shown in a 700px box.
- Set the new width to the box size plus 100–300px (e.g. ~1,000px for a 700px box) so the image is neither blurry nor oversized.
- In the theme customizer, open the section holding the image, click Edit on the uploaded asset, use the native editor's resize function, enter the new width and apply.
- Refresh the page and visually confirm the image looks the same as before.
- Use the same logic for hero banners: an image 5,712px wide shown in a site capped around 2,000–3,000px can be resized down with no visible change.
- Target no more than a few hundred KB per image where possible — resizing alone may still leave a 1MB file that needs compression.
Caveat: The native Shopify resize tool reduces dimensions but gives no compression control, so compressing with a separate tool afterward is still required.
Caveat: The 100–300px overshoot is the source's rule of thumb to avoid blur, not a tested universal threshold.

Tags: speed, image-optimization, product-page, shopify, landing-page, measurement
Source: Page speed.docx

---

## Compress images to keep files small, especially for mobile shoppers
Use when: Your product, banner or section images are still heavy after resizing, and you want faster downloads for mobile visitors.
- Audit image file weights in your media library or via page inspection; the source's practical threshold is to reduce any image larger than 500KB.
- Resize first if dimensions are oversized, then run the file through a compression tool — the source names Tiny SEO and Squash as examples.
- Re-upload the compressed version and confirm the visual result still looks acceptable on the live page.
- Check that the new file size dropped materially — the source's example went from ~1MB after resize to roughly 100KB when compressed.
- Treat image compression as user-experience work that can also support conversion rate, per the source, rather than only a technical chore.
Caveat: Compressing too aggressively can visibly degrade image quality; the source does not specify a quality setting.
Caveat: The source presents conversion-rate improvement as a possibility tied to better UX, not a measured benchmark.
Caveat: Compression tools and their interfaces change — verify current options before relying on named tools.

Tags: speed, image-optimization, compression, mobile, product-page, shopify, conversion-optimization
Source: Page speed.docx

---

## Pick the right image format and swap GIFs for MP4
Use when: You are preparing product, banner or content imagery for upload to a storefront.
- Upload stills as JPEG or PNG and let the platform (the source cites Shopify) handle conversion to modern formats like WebP.
- Replace animated GIFs with MP4 video, which the source says are better and load faster.
- Confirm what your platform auto-converts before doing extra format work yourself, since this reduces the value of manual conversion.
- Pair format choice with resizing and compression rather than treating format alone as the fix — the source warns that bad results follow if you upload without resizing or cropping.
Caveat: The source's WebP auto-conversion claim is a Shopify behavior that may not apply to other platforms; verify your own pipeline.
Caveat: Format choice will not rescue files that are still huge in dimension or weight.

Tags: speed, image-optimization, file-format, shopify, product-page, video
Source: Page speed.docx

---

## Name image files descriptively before upload
Use when: You are about to upload product or content images to your store and are naming the files on your computer.
- Rename files to describe what is in the image instead of keeping camera-generated or random names.
- Include the product/category and distinguishing attributes (e.g. color or view) so the filename communicates content.
- Upload only after renaming, since post-upload filename changes may not carry through cleanly.
- Pair descriptive filenames with descriptive alt text — the source lists naming, uploading, reordering, alt text and on-site verification as sequential steps.
Caveat: The source treats this as a straightforward SEO benefit without specifying keyword density or length limits.
Caveat: Filename alone does not replace alt text for accessibility.

Tags: speed, image-seo, image-optimization, product-page, shopify
Source: Page speed.docx

---

## Order gallery images to answer customer questions
Use when: You are uploading and reordering product images in a PDP gallery.
- Start with the main image that shows the product clearly.
- Follow with an alternate angle so the buyer can see what the main shot hides.
- Then add detailed shots covering specific features and materials buyers will ask about.
- Finish with lifestyle images showing the product in context — the source suggests generating lifestyle imagery with AI tools like Gemini if your supplier does not provide them.
- Reorder uploaded images so the sequence matches this question-answering flow rather than the order files were captured.
Caveat: The source presents this ordering as its usual convention, not a tested ordering that outperforms alternatives for every category.
Caveat: AI-generated lifestyle images should be checked for accuracy against the actual product.

Tags: speed, product-page, merchandising, image-optimization, creative-strategy, shopify
Source: Page speed.docx

---

## Run a final image checklist before finishing a store
Use when: You have finished uploading and editing a batch of store images and want to confirm nothing was missed.
- Confirm every image is a JPEG or PNG and that video content is MP4 rather than GIF.
- Confirm each image has been resized and cropped for its layout rather than uploaded straight from a camera.
- Confirm files over 500KB have been compressed through a tool such as Tiny SEO or Squash.
- Confirm filenames are descriptive, alt text has been written, and gallery order follows main → alternate → detail → lifestyle.
- Verify on the live store that images display at the right dimensions and that alt attributes are actually attached, by inspecting image elements.
- Re-check any oversized image found during verification, resize it in the customizer, and refresh the page to confirm it renders identically.
Caveat: This is a workflow checklist from the source, not a guarantee of specific performance gains.
Caveat: The 500KB figure is the source's practical threshold for flagging files, not a hard performance ceiling.

Tags: speed, image-optimization, quality-assurance, product-page, shopify, measurement
Source: Page speed.docx

---

## Inspect rendered image dimensions to find wasted bandwidth
Use when: Store pages feel slow or you suspect imagery is heavier than necessary, and you need evidence before optimizing.
- Right-click the suspect image on the live page and choose Inspect.
- In the inspector, read the intrinsic dimensions of the image file versus the dimensions of its container.
- Flag large gaps as waste — the source's example found a 5,000px-wide image displayed in a 700px box.
- Also note the file's total weight where visible; the source's example showed a 6MB section image.
- Use the gap to choose the resize target (box width + 100–300px) and then re-check after resizing to confirm the rendered look is unchanged.
- Apply the check beyond hero banners to section images and any repeated visual blocks across the store.
Caveat: Inspector interfaces vary by browser and change over time — verify the current dev tools layout.
Caveat: Resizing fixes dimension waste but not compression; a correctly sized file can still be too heavy.

Tags: speed, measurement, image-optimization, product-page, shopify, diagnostics
Source: Page speed.docx

---

## Decide whether an image is worth resizing, compressing, or both
Use when: You are triaging a catalog of store images and deciding which optimization each file needs.
- If dimensions exceed the display box by a wide margin, resize to roughly box size plus 100–300px.
- After resizing, check the file weight again — the source reduced a hero from 5,000px to 2,700px and still ended near 1MB, which it judged too much.
- If the file remains heavy, compress it; the source estimates the same visual result could come down to about 100KB.
- If a file is already correctly sized but still heavy, skip resizing and compress only.
- If an image is small and correctly sized, leave it and move on to other assets.
- Re-verify visually on the live page after each change so optimization does not degrade the customer's impression of the product.
Caveat: The 100KB estimate is the source's illustration, not a target that every image can or should hit.
Caveat: There is no single fix; the source explicitly pairs resizing with compression for the best result.

Tags: speed, image-optimization, compression, diagnostics, product-page, shopify
Source: Page speed.docx

---

## App Portfolio Triage: Only Keep Apps That Clearly Make Money
Use when: Auditing installed Shopify apps to decide which to keep, before running a page-speed test.
- List every installed app in the Shopify admin and write down the concrete revenue mechanism for each (e.g. sizing chart prevents non-purchase for sized products, review app supplies social proof, subscription app drives recurring orders).
- If you cannot state how an app makes money, treat it as a removal candidate — the source's rule is that apps must earn their place.
- Prefer apps with many reviews and good reviews, since volume signals the app actually works for other merchants.
- Before installing anything new, ask whether native theme features already cover it: announcement bars, discount codes in cart and similar simple elements should not come from an app.
- When uninstalling, do not assume cleanup happens: go to Online Store > Themes > Edit code, open theme.liquid, search the app's name and also search the app's store listing name (e.g. a 'free shipping bar' app whose brand is different), remove or comment out leftover script tags with Cmd/Ctrl + /.
- Check the customizer's app embeds panel and turn off any embed you are not actively using, then save.
Caveat: Apps can still inject assets via Shopify's own script tags, so removing all front-end mentions does not guarantee a specific loading behaviour outside of app embeds being off.
Caveat: Some apps cannot work defer/async and must stay blocking to keep functionality.

Tags: speed, app-audit, shopify, theme-code, technical-seo, performance-budget
Source: Page speed.docx

---

## Use the Restaurant Analogy to Prioritize Above-the-Fold Loading
Use when: Deciding which storefront assets to prioritize, defer or lazy load on a homepage, landing page or PDP.
- Identify everything visible without scrolling: hero banner, logo, main styling, headline copy, hero images, primary product imagery.
- Treat these as the 'drinks' — they must render immediately and must not wait for app assets, reward widgets or third-party scripts.
- Treat anything below the fold or non-essential (loyalty widgets, chat, extra marketing scripts) as later courses and lazy load or defer them.
- Never let a non-essential app asset block the hero: check whether widget assets download before main elements and deprioritize them.
- Apply the same priority logic per page type — on a PDP the product image and buy box are the 'drinks'.
Caveat: This is a prioritization heuristic, not a measurement; verify the effect with Lighthouse or PageSpeed Insights after changes.

Tags: speed, shopify, performance-budget, critical-rendering-path, lazy-loading, hero-banner
Source: Page speed.docx

---

## Defer Script Tags in theme.liquid, Then Fall Back to Async
Use when: Cutting render-blocking JavaScript found in a Shopify theme during a speed optimization pass.
- Run a Lighthouse audit (right-click > Inspect > Lighthouse tab) and scroll to the details section to find scripts listed under render-blocking resources.
- In Themes > Edit code, open theme.liquid — the file that holds most scripts — and locate script tags missing defer or async.
- Add defer so the document loads first and the script loads after; prefer defer over async (the source says defer is better).
- Save, load the store, and verify the specific functionality that script powers still works; if yes, keep defer.
- If the feature breaks, swap defer for async and re-test; if async also breaks it, leave the script as-is because that script genuinely must block.
- Re-run the Lighthouse test to confirm the render-blocking entry disappeared and the score moved (the source saw 78 to 80 after one defer, then 81 after removing a jQuery script).
Caveat: You must know what a script does before modifying it — blind defer/async can silently break store functionality.
Caveat: Score deltas from a single script are small; the source's 1-3 point gains are illustrative of one test, not a guarantee.

Tags: speed, shopify, theme-code, lazy-loading, javascript, lighthouse, technical-seo
Source: Page speed.docx

---

## Self-Host Third-Party Libraries in the Shopify Assets Folder
Use when: Adding or keeping a JavaScript library on a store, such as when legacy theme code depends on jQuery.
- Open the CDN link in a new browser tab and download the file to your computer.
- Upload the file into the theme's assets folder via the code editor.
- Reference it the way Shopify does in its own themes: copy an existing script line that uses the asset_url variable and replace only the file name.
- Hover the resulting link in the code editor — the tooltip should confirm the asset is served from the Shopify CDN for better performance.
- Avoid loading jQuery at all where possible; the source says it is old technology and vanilla JavaScript should replace it — removing a jQuery script raised his test score by one point.
Caveat: The source's one-point gain from removing jQuery is a single test observation, not a benchmark.
Caveat: Only remove a library if you can confirm nothing in the theme depends on it.

Tags: speed, shopify, theme-code, cdn, javascript, performance
Source: Page speed.docx

---

## Understand How Shopify Injects App Scripts via content_for_header
Use when: Diagnosing why a store's PageSpeed score plateaus despite a lean theme and no active app embeds.
- Test with app embeds all turned off in the customizer and still observe a gap between your score and 100 — this isolates Shopify-injected scripts as the cause.
- In theme.liquid, locate the content_for_header tag; this is what pulls Shopify's injected scripts into every page load.
- The source demonstrates commenting it out and re-running the speed test to confirm the impact (80% jumped to 100% with it disabled).
- Never do this on a live theme — the code editor flags it as an error and it will break app and platform functionality.
- Instead, if you want the benefit, use a lazy-loading approach for that tag's contents: the source supplies a snippet that defers the injected scripts until user interaction, and he measured 97% and an overall claim of 10-20% gain over the current score.
Caveat: The 10-20% claim is the presenter's own estimate; he also warns the technique has small impact if the store has larger underlying speed problems.
Caveat: This is a third-party snippet, not an official Shopify feature — verify current Shopify behaviour before relying on it.

Tags: speed, shopify, theme-code, app-scripts, technical-seo, measurement
Source: Page speed.docx

---

## Compress and Resize Product and Hero Images Before Upload
Use when: Preparing hero banners, category images and product photography for upload to a Shopify store.
- Check the file size of every image you plan to upload; the source found an 8 MB hero image on a student's store and treats 2-3 MB as the target for the entire store.
- Resize first: open the image in a tool like Photopea, go to Image > Size, and set the resolution to around 2,000 px, which the source treats as sufficient.
- Export as JPEG at roughly 70% quality (lower is acceptable if quality holds).
- Optionally run the result through a compressor like TinyPNG/TinyJPEG; the source's example only saved a further 8% after a good export, so the export step did most of the work.
- Do a visual side-by-side comparison — the source's compressed 234 KB file looked indistinguishable from the 8 MB original, and a 100 KB file matched a 400 KB one.
- If manual work per image is impractical, use a bulk image-compression app in Shopify instead.
Caveat: Some themes automatically re-serve smaller derivatives of large uploads, but you should still compress before uploading rather than relying on that.
Caveat: The source's file-size targets come from his own practice, not a published standard.

Tags: speed, images, shopify, asset-optimization, product-page, hero-banner
Source: Page speed.docx

---

## Set Image Upload Dimensions Slightly Above the Container Size
Use when: Configuring image width settings for a section or theme setting, such as a 700 px hero container.
- Find the actual rendered box width — the source's example box is 700 px.
- Set the image dimension to roughly 100-300 px above the box width (he used about 1000 px for a 700 px box) rather than uploading at exactly the box size.
- Uploading exactly matching dimensions risks a blurry rendering; uploading far larger wastes file size.
- Apply the setting, refresh the storefront and confirm the image still renders identically.
- Inspect the element to verify the served width reflects your setting.
- This setting is available in the theme editor and can be docked to the side while you work.
Caveat: The 100-300 px margin is the source's working rule of thumb, not a measured optimum; check the visual result.

Tags: speed, images, shopify, theme-settings, asset-optimization, hero-banner
Source: Page speed.docx

---

## Match Image Format to Use: JPEG Default, PNG for Transparency, MP4 Over GIF
Use when: Choosing file formats when preparing product images, logos and motion assets for a store.
- Default to JPEG and compress it for every photographic image.
- Use PNG only when you need something cropped out or transparent, such as a logo overlaid on a background.
- Never use GIFs — the source says they are huge; if you need motion or an animation, embed an MP4 inside an HTML video tag, which loads much faster.
- Apply the same compression discipline to video files as to images; oversized video is equally damaging.
- Treat 'media' decisions as a per-page-type choice: hero video, PDP gallery images and category thumbnails all follow the same format rules.
Caveat: Format choice does not substitute for compression — a large JPEG can still be worse than a reasonable PNG.

Tags: speed, images, video, shopify, asset-optimization, file-format
Source: Page speed.docx

---

## Preload Above-the-Fold Media and Lazy Load Everything Below
Use when: Setting loading behaviour on hero banners, above-the-fold product imagery and long-page sections.
- Mark every asset visible without scrolling as preloaded so the browser gives it priority.
- Lazy load everything underneath the fold so it downloads only when the customer scrolls to it.
- Do not use animations or transitions on the hero — an animation forces the browser to download an effects library before displaying the image, delaying the hero.
- If LCP readings are large, inspect the main image for fade-ins, slide-ins or similar effects and remove them.
- Lazy load app widgets that are not essential to the buying process, using lazy sizes or loading="lazy" attributes where appropriate, and keep essential buying-flow assets eager.
Caveat: Preload too many assets and you recreate the problem you are solving; apply it to above-the-fold only.
Caveat: The source notes that a slider's first image specifically must not be lazy loaded or animated.

Tags: speed, lazy-loading, lcp, images, shopify, hero-banner, performance-budget
Source: Page speed.docx

---

## Trim Custom Font Variations and Enable font-display: swap
Use when: Reviewing a designed Shopify theme that ships custom typography, or troubleshooting rendering delays on text.
- Inventory which font weights and styles actually appear on the storefront.
- Limit yourself to roughly three variations of a custom font; the source recommends no more than three and calls five or ten variations 'not a great idea'.
- In Themes > Edit code, search for the @font-face declarations that import your custom fonts.
- Ensure each imported font has the font-display: swap property so the browser shows fallback text and swaps the custom font in once downloaded.
- If the design does not genuinely require custom fonts, use the fonts built into Shopify themes instead — the source considers them good enough for most stores.
Caveat: The three-variation limit is the source's own recommendation, not a platform rule.
Caveat: font-display swap can cause a visible flash of fallback text; whether that trade-off is acceptable is a design judgement.

Tags: speed, fonts, shopify, theme-code, asset-optimization, technical-seo
Source: Page speed.docx

---

## Choose a Simpler Theme Over a Feature-Rich One Unless Features Pay
Use when: Selecting a theme for a new Shopify store or deciding whether to upgrade from a free theme.
- Default to a simple free theme; the source names Dawn and Horizon as the best starting points and warns against going for the most complex premium theme.
- Do not buy a premium theme for pop-ups or features on a hunch or because a video recommended it — require a clear reason it will make more money.
- If you genuinely expect to use specific features and expect them to drive revenue, a premium theme is justified.
- When evaluating, remember that the extra libraries and options you never use still load and cost performance.
- Note that effect-heavy designs delay display because effects libraries must load first.
- Choosing a free theme also saves roughly $300 versus a premium theme, according to the source.
Caveat: The $300 saving figure and the free-theme recommendation are the presenter's guidance for beginners and lean stores, not a rule for all businesses.

Tags: speed, shopify, theme-selection, positioning, performance-budget, cost
Source: Page speed.docx

---

## Weigh Migrating an Old Theme vs. Rebuilding on Dawn or Horizon
Use when: Deciding whether to keep optimizing a legacy Shopify theme or migrate the store.
- If the store is established and cannot change theme, implement the levers in order: app audit, script defer, image compression, font trimming — these are still possible on older themes.
- Accept that some fixes get technical on old themes because the technology is outdated and the theme was not built for speed.
- If you have the option and the theme is the bottleneck, build the site again on Dawn or Horizon; you must rebuild every section because structure differs, but a lighter newer theme loads fewer files.
- Compare the cost of repeatedly optimizing an ageing theme against the one-off cost of rebuilding — the source says optimizing an older theme can end up costing more.
- Plan migrations around other store changes (redesign, revamp) rather than as an isolated emergency project.
Caveat: A migration requires rebuilding sections, apps and customizations — budget for that disruption.
Caveat: The source gives no hard timeline for when a theme must be retired.

Tags: speed, shopify, theme-selection, migration, positioning, performance-budget
Source: Page speed.docx

---

## Recognize That Most Free Shopify Themes Are the Same Codebase
Use when: Choosing between free Shopify themes or deciding whether switching to a differently-styled free theme changes performance.
- In the theme store, filter for free themes and note the badges dividing Dawn-based from Horizon-based themes.
- Understand that picking among variants of the same base changes only styling, images, colours and settings — the codebase is identical.
- Check theme version numbers: all Dawn-based themes share one version (the source saw 1.5.3.0) and all Horizon-based themes share another (1.0.1).
- Conclusion for selection: do not expect a performance or capability change from switching between two themes built on the same base — choose on fit and design.
- If you want Horizon's structural capabilities, you must move to a Horizon-based theme, not a Dawn variant.
Caveat: Version numbers and store badges change over time — verify the current theme-store labelling.
Caveat: This applies to free themes at the time of the source, not necessarily to paid themes or future releases.

Tags: speed, shopify, theme-selection, shopify-themes, product-research, positioning
Source: Page speed.docx

---

## Understand Horizon's Global Blocks vs. Dawn's Section-Scoped Blocks
Use when: Designing a storefront layout and deciding how much free-form composition you need from the theme.
- On a Dawn-based theme, adding a section (e.g. image with text) shows only the blocks permitted for that section; blocks cannot move between sections.
- On a Horizon-based theme, sections that accept blocks accept global blocks; click Add block and see a much larger shared list (logo, accordion and more).
- Global blocks themselves can contain sub-blocks — an accordion added as a block gets its own nested block options.
- Check the theme's code editor: Horizon-based themes add a blocks folder alongside templates, holding the global blocks; Dawn has templates only.
- Use this as the deciding factor when choosing between simple versus composable layouts — more flexibility means more layout options but also more to configure.
Caveat: Block availability and nesting behaviour are theme-version dependent; verify in your own customizer.
Caveat: Customizer improvements such as copy-paste of sections and renaming apply to all themes, not just Horizon.

Tags: shopify, theme-selection, merchandising, shopify-themes, landing-page, site-design
Source: Page speed.docx

---

## Benchmark Theme Speed With an Apples-to-Apples Comparison
Use when: Justifying a theme migration decision or setting performance expectations before rebuilding a store.
- Set up the two themes on one store with identical customizations — the source used a hero banner and a few products only.
- Turn off all app embeds in the customizer for both themes so uninstalled/unused apps do not distort the comparison.
- Run PageSpeed Insights on both storefront URLs and record mobile and desktop scores plus LCP and blocking-time details.
- In the source's test, Horizon scored 71 mobile / 74 desktop and Dawn scored 56 mobile / 78 desktop — his conclusion was Horizon is somewhat better overall.
- Read the diagnostics rather than only the headline number: the LCP in his test came from an oversized hero image, so compression was the next fix for both.
Caveat: Single-run results are noisy and store-specific — treat these numbers as an example, not a benchmark you can expect to reproduce.
Caveat: The comparison held apps inactive; a real store's app mix will change the outcome.

Tags: speed, shopify, measurement, theme-selection, experiment-design, lighthouse
Source: Page speed.docx

---

## Keep Dawn for Now; Build New Stores on Horizon
Use when: Deciding whether to migrate an existing Shopify store to Horizon during a redesign or a new-build decision.
- For an existing Dawn store with significant work invested, keep Dawn — the source says there is no reason to rush and cites merchants still running the much older Debut theme successfully.
- Note that Shopify stopped releasing updates to Dawn earlier in the year, and the source does not expect Dawn to adopt the new structure.
- If you are building a new store, go with Horizon or a Horizon-based free theme.
- If you will redesign or revamp anyway, do it on Horizon at that point rather than as a standalone migration.
- Wait for maturity: the source observed Horizon already at version 1.0.1 with a patch pushed, and expects early bugs to be ironed out.
Caveat: This is the presenter's forward-looking opinion about theme roadmaps, not an official Shopify statement.
Caveat: He flagged that Dawn would likely be sunset eventually but explicitly not imminently.

Tags: speed, shopify, theme-selection, migration, shopify-themes, positioning
Source: Page speed.docx

---

## Diagnose CLS by Reading Google's Rendering Screenshots
Use when: Investigating a poor layout-stability score on a storefront that loads but shifts while users interact.
- Run PageSpeed Insights and open the rendering/screenshot sequence Google captured during load.
- Compare consecutive frames to spot elements that appear suddenly and push content down, around or larger.
- Note that GIF motion in the capture is expected if the store uses GIFs, but the real signal is an element appearing between frames.
- Note the suspect element's on-page ID, inspect it on the storefront and search the document to trace its source.
- Elements injected after load usually come from apps — the source identified a free-shipping-bar app (Hexom) creating CLS; he calls such simple announcement bars something themes already provide, so an app for it is unnecessary.
- Check the desktop tab too: the source found one site with zero CLS on mobile but a large desktop reading, and his free-shipping-bar example was worse on desktop.
Caveat: The source ranks CLS as the most impactful metric in his experience, ahead of LCP — this is his qualitative ranking, not a Google-published weight.
Caveat: Fixing LCP and CLS alone moved his illustrative store above 50, possibly 60 — a case observation, not a benchmark.

Tags: speed, cls, measurement, shopify, app-audit, technical-seo, layout-stability
Source: Page speed.docx

---

## Fix LCP by Un-lazy-loading and De-animating the Hero Image
Use when: Improving a poor LCP reading on a homepage, category page or any page where a large hero dominates.
- Identify the largest element — typically the hero banner image or the first slide of a slider.
- Remove loading="lazy" and any lazy-sizes classes or loading-lazy patterns from that image; the source says this should never be lazy loaded.
- Set loading="eager" instead, telling the browser the image is important and should load as fast as possible.
- Remove fade-in, slide-in or other entrance effects from that image, since effects force an effects library download before the image shows.
- Compress the image as much as you can once the loading behaviour is correct.
- In a slider, implement logic so the first image is never lazy loaded or animated while later slides can be; also check blocking time, which affects LCP too.
Caveat: In his example the image was lazy loaded and should have said eager — but LCP can also be driven by blocking time and effects, so check more than the loading attribute.

Tags: speed, lcp, images, lazy-loading, shopify, hero-banner, measurement
Source: Page speed.docx

---

## Decide Whether Your Store Actually Needs a Good Speed Score
Use when: Setting speed-optimization priorities and budget for a store before committing technical work.
- Assess your traffic mix: if you have a large ad budget and depend on paid traffic rather than organic, tight speed scores are less critical — the source notes big brands with lower scores still sell a lot.
- If you rely on or want organic traffic from Google, prioritise the PageSpeed Insights score and fix the flagged items, especially LCP and CLS.
- Separate the customer-experience case from the SEO case: the source's buying-impulse argument is that customers arrive from ads, hit a slow page and bounce within 2-3 seconds.
- If you have visits but no purchases, treat speed as a candidate explanation worth testing rather than assuming it is the only cause.
- Sequence your effort: fix LCP and CLS first, since the source says these two alone can move a poor score into the 50s-60s in his experience.
Caveat: The '2-3 second' expectation is the presenter's own behaviour as a shopper and his model of customer behaviour, not a measured threshold.
Caveat: The claim that optimized Shopify stores get more sales is his observation from years of client work, not a controlled study.

Tags: speed, measurement, acquisition, conversion-optimization, technical-seo, prioritization
Source: Page speed.docx

---

## Search a Downloaded Theme Folder for Residual App and Pixel Code
Use when: Deep-cleaning a storefront's code after uninstalling apps or removing tracking, beyond what theme.liquid search reveals.
- In the Shopify admin go to Themes > Download theme and send it to your email; save and unzip it locally.
- Install a code editor such as Cursor (free) and open the unzipped theme folder as a project.
- Use the editor's global search to query an app's brand name, and also its listing name — a two-part name means two searches.
- When a match appears (the source's example found a match inside a JSON file), open it and inspect the reference.
- Repeat for old pixels and libraries, e.g. searching a leftover analytics provider name shows every file that still references it.
- Checking file by file in the theme editor is slow, so use the global search as the efficient route.
Caveat: A downloaded copy is a snapshot — re-download if you have since changed the theme.
Caveat: Reading matches still requires judgement about whether removing them is safe.

Tags: speed, shopify, theme-code, app-audit, technical-seo, measurement
Source: Page speed.docx

---

## Audit Shopify theme files for leftover app code with a code editor
Use when: Store speed work is blocked or polluted by old app scripts you can no longer control from the Shopify admin, and you need to locate the exact theme file and line before deleting anything.
- Download your theme (Online Store > Themes > ... > Download theme file) and unzip it, or open it directly in a code editor such as Cursor (free; has AI assistance if you don't write code) using Open Folder.
- Use the editor's global search to find app keywords, e.g. 'hexom' for an uninstalled app, 'Google' for Google-related tags, or 'logs' for a reviews app. See which files contain them.
- When you open a match, note the file name and the approximate line number (e.g. a pixel at line 72 of a .json or .liquid file).
- Back in Shopify, go to Theme > Edit code, search the same file, jump to the nearby line, and remove only the target tag/code.
- Save and verify the store still works before doing the next removal; only remove code you have positively matched to an app you no longer use.
Caveat: Editing live theme code can break functionality or checkout; test after each change and keep a downloaded backup of the original theme.
Caveat: The source stresses confirming what a script does before altering it, because some apps require their scripts to load immediately.

Tags: speed, shopify, theme-code-cleanup, app-bloat, audit, liquid
Source: Page speed.docx

---

## Find and compress oversized non-product images in Shopify Files
Use when: Store images hurt page speed and app-based image compressors only touch product photos, leaving homepage/section banners heavy.
- In Shopify go to Content > Files and sort through the media library looking for large offenders (e.g. 3 MB, 5 MB). The presenter's working target: total page weight around 2–3 MB, and individual images under 1 MB, ideally a few hundred KB.
- Identify which theme sections use each heavy image, then download it.
- Resize large images (e.g. reduce width to ~1500px, keeping aspect ratio) if a compression pass alone still leaves them over budget; the presenter's example went from ~5 MB to ~1.6 MB after resize, then to ~400 KB after compression.
- Run the downloaded file through a free compression site (the demo used one that cut size by roughly 50–70%) and download the compressed output.
- Re-upload the compressed image to the same section/file so the reference is preserved, and replace the original wherever it appears.
Caveat: Compression targets are the presenter's heuristics, not Google thresholds; balance quality against weight for hero imagery.
Caveat: Always keep the original if you may need higher resolution later.

Tags: speed, shopify, image-optimization, media-library, lcp, compression
Source: Page speed.docx

---

## Choose JPEG vs PNG vs GIF for store imagery
Use when: Deciding export/upload format for product photos, section banners, or overlay graphics that affect page weight.
- For standard photos (product shots, lifestyle banners) export and upload as JPEG — the source says JPEGs compress much better and yield lower file sizes than PNGs.
- Use PNG only when you need transparency, e.g. decorative bubbles/graphics overlaid on a product or spanning sections where the background must show through.
- Never use GIF: the source calls GIFs bad for performance and unprofessional-looking, and notes big brands avoid them.
- For any looping background video, use an MP4 file set to autoplay/loop rather than an animated GIF.
Caveat: The 'never use GIF / big brands never do' claim is the presenter's opinion, stated as such; style choices may vary, but the performance point on GIF weight stands.
Caveat: Switching a transparent graphic to JPEG will lose the transparency effect.

Tags: speed, image-optimization, file-format, jpeg, png, gif, creative-assets
Source: Page speed.docx

---

## Lazy-load below-the-fold images but never the hero image
Use when: Setting theme image behavior or debugging slow perceived load / poor LCP on homepage banners and product grids.
- Leave the main hero image (the banner at the top) loading eagerly — do not lazy-load it, because in-view images are usually the Largest Contentful Paint element and lazy-loading them worsens LCP, which the source says Google dislikes.
- Apply lazy loading (loading="lazy") to everything below the fold: lower section images, secondary product images, and decorative overlays.
- If your theme's hero section lazy-loads its first image by default, add custom logic to exempt that first image so it renders immediately.
- Verify behavior in the browser/network panel: the in-view images should download right away, with further images downloading only as the user scrolls.
Caveat: The presenter cautions that if you already have serious LCP or CLS problems, lazy-loading fixes won't be enough — those issues need separate attention.
Caveat: Theme behavior differs by theme version; verify the current interface and default markup.

Tags: speed, lazy-loading, lcp, shopify, theme-code, image-optimization
Source: Page speed.docx

---

## Add font-display: swap to custom fonts to avoid render blocking
Use when: Custom store fonts create render-blocking delay and you want layout to paint immediately on slow connections.
- In your theme code (via the code editor), search for '@font-face' across all theme files — this is how fonts get imported.
- For each @font-face rule, check whether it has a font-display: swap property; if not, add it (e.g. just below the font-family declaration).
- Save and test: on a simulated slow connection (e.g. 3G in devtools) you should see a standard browser font render first, then swap to the custom font once it downloads.
- Accept the brief 'font swap' flash as the trade-off: the document no longer waits for the font before rendering, removing blocking time.
Caveat: Without swap, the whole document can be blocked until the font downloads, creating significant blocking time — this is the problem being fixed.
Caveat: On fast connections the swap may be invisible, so test under throttling to confirm it works.

Tags: speed, fonts, render-blocking, shopify, theme-code, font-display-swap
Source: Page speed.docx

---

## Add async or defer to third-party scripts after checking their purpose
Use when: Third-party scripts (jQuery, libraries, or app scripts) sit in theme.liquid and load synchronously, slowing first render.
- Open theme.liquid and scan for <script> tags, including ones you don't recognize (added by apps or a previous developer).
- Investigate what each script does and how it works before touching it — you must know its dependency on load order.
- Add 'async' to allow the script to download alongside the theme; add 'defer' to make it download only after the theme fully loads.
- Save and re-test; some solutions/apps specifically cannot use async or defer because they need their scripts immediately, so keep those untouched.
Caveat: The source says most (not all) theme scripts can take async/defer — verify app requirements, since loading a required script late can break functionality (e.g. consent, checkout widgets).
Caveat: Differentiating async vs defer matters for scripts that depend on DOM readiness.

Tags: speed, shopify, theme-code, async-defer, render-blocking, third-party-scripts
Source: Page speed.docx

---

## Defer all app scripts until user interaction to cut blocking time
Use when: Many installed apps load their scripts immediately and inflate blocking time; you want to prioritize first paint over third-party app JS.
- In devtools, inspect the <head> and find the 'async load' function that injects scripts for all installed apps — it runs concurrently with your theme.
- Comment out that async-load block in the theme's content file (the source uses comment tags around it).
- Paste the provided lazy-load snippet (in the video description) directly beneath the commented-out block; it defers injecting app scripts until the user starts interacting (scroll, click).
- Save and re-run a speed test after a short wait so the change propagates. In the demo the score moved from roughly 40–50 to ~85 after the change and reverted when removed.
- Also go to Customize > App embeds and turn off any app embeds you don't actively use before testing.
Caveat: The code is not as effective if you have high CLS or LCP — those issues take priority over blocking time.
Caveat: The demo's 40–50 → ~85 jump is a single case example, not a guarantee; results depend on your app mix and theme.
Caveat: Verify the current theme file name and interface before editing; theme markup changes over time.

Tags: speed, shopify, app-bloat, theme-code, blocking-time, lazy-loading
Source: Page speed.docx

---

## Prune unused apps and app embeds to reduce third-party load
Use when: Auditing store speed when many apps are installed, or deciding whether a low-value app is worth keeping.
- List installed apps and remove any you aren't currently using — the source's rule: if unsure, uninstall; you can reinstall later.
- Keep only apps that bring clear value to you or your customer, since app code lives on third-party servers and its quality can't be controlled.
- Go to theme Customize > App embeds and turn off any embeds that are enabled but not needed.
- Re-test speed after pruning to see the combined effect.
Caveat: Too many apps can make a store unusable, per the source — but some apps are load-bearing; confirm before removing.
Caveat: App embed locations and menus may change in the current Shopify admin; verify the interface.

Tags: speed, shopify, app-bloat, audit, cleanup
Source: Page speed.docx

---

## Plan a three-keyword SEO scheme per page with Google Keyword Planner
Use when: Beginning store SEO work — planning which keywords the homepage, product, and collection pages should target.
- Brainstorm keywords that represent your brand and products, then validate them in Google Keyword Planner (requires a Google Ads account; under Tools > Planning).
- Enter a seed term (e.g. 'homemade soap'), set country/language, and read results: monthly search volume, competition, and CPC (in the demo, 'homemade soap' showed 1k–10k searches and bids of $0.20–$1.54).
- Pick a sensible main keyword plus two supporting keywords per page, favoring ones with buying intent (e.g. 'homemade soap for sale') over purely informational ones (e.g. 'how to make homemade soap').
- Use the 'start with website' feature on a competitor's URL to see the keywords they rank for and borrow ideas.
- Cross-check volume/intent in free tools (Google Trends + Glimpse extension, or Google autocomplete predictions) and confirm in Keyword Planner before committing.
Caveat: Volume/competition/CPC figures are the source's tool examples, not universal benchmarks; niches differ.
Caveat: Paid tools (Ahrefs, Semrush) give extra intent/depth but aren't required — Keyword Planner is the free baseline.

Tags: speed, seo, keyword-research, keyword-planner, search-intent, shopify
Source: Page speed.docx

---

## Optimize the store-level SEO title and meta description
Use when: Configuring the global store-level search listing (Online Store > Preferences > Search engine listing) that represents your brand in search results.
- Go to Online Store > Preferences > Search engine listing.
- Put the chosen main keyword in the title field and supporting keywords (plus a call to action) in the description field.
- Keep the title within the character limit shown (the demo used 63 of 70 characters) and make sure the keywords genuinely represent your brand and niche — avoid too-broad or off-niche terms.
- Have ChatGPT draft title/description from your keywords, then refine for brand voice and save; verify the listing reflects your store before publishing.
Caveat: The source notes many Shopify owners neglect these fields, but avoid keyword stuffing terms that don't represent the store.
Caveat: Meta description length guidance here is the presenter's; search engines may rewrite snippets anyway.

Tags: speed, seo, meta-description, store-settings, shopify, brand-voice
Source: Page speed.docx

---

## Rename generic product titles into keyword-rich H1 titles
Use when: Product titles are vague (e.g. a cute name that says nothing to search engines) and need to become the page's explanatory H1.
- On a product page, the product title is the page's main H1 and explains to Google what the page is about; a name like 'sweet honey bomb' tells Google nothing — reinforce this by rewriting it.
- Copy the product's spec/description and ask ChatGPT for high-volume keyword candidates for that kind of product.
- Validate the promising candidates in Keyword Planner, keeping ones with good volume; discard the weak ones.
- Feed the validated keywords back to ChatGPT and have it generate several title options containing at least the main keyword; pick/tweak the best.
- Paste the new title into the product, save, and adjust theme title font size in the customizer if the longer title looks oversized.
Caveat: Ensure the title still accurately represents the product and the brand; don't force keywords that misdescribe the item.
Caveat: Keyword volumes are tool figures and change over time/region.

Tags: speed, seo, product-titles, h1, keyword-research, shopify, product-page
Source: Page speed.docx

---

## Write substantive 100–400 word product and collection descriptions
Use when: Product pages or collection pages have thin descriptions (just specs, or none) and need indexable, keyword-rich copy.
- Gather the product's specs/attributes and use ChatGPT to generate a description based on them, instructing it to include keywords found in Keyword Planner.
- Ensure the text sounds human and doesn't read as obviously AI-generated; format with bold, images, etc.
- Meet the length target: the source says at least 100 words, and 300–400 is ideal — copying only specs is a common mistake.
- For collection pages, add a description (100–400 words) with the right keywords; if you don't want it pushing products down, move it below the product grid.
- Save. Collection descriptions matter for ranking even when placed lower on the page.
Caveat: The 100-word minimum and 300–400 ideal are the presenter's guidance, not an official ranking rule.
Caveat: Long keyword-stuffed copy can look dull without images — balance readability against keyword coverage.

Tags: speed, seo, product-description, collection-page, content, keyword-research
Source: Page speed.docx

---

## Write alt text and rename image files for SEO and accessibility
Use when: Product images and site/section images have gibberish file names or no alt text and you want better indexing and accessibility.
- On a product image, write alt text that combines the target keyword, the actual product, key attributes, and the angle (e.g. '[keyword] bath bomb purple frontal').
- Rename the underlying file to match that descriptive alt text instead of a numeric/gibberish name.
- Repeat for all images in the product media gallery.
- For section images, go to Content > Files, open each media item, add descriptive alt text, and rename the file — most library files will be gibberish by default.
- Verify in the product listing (inspect the image) that the URL now reflects the descriptive name.
Caveat: The source notes this also aids visually impaired users and that Google rewards the practice.
Caveat: Doing this manually is impractical for very large catalogs — the source points to an automation app instead.

Tags: speed, seo, alt-text, image-optimization, accessibility, shopify
Source: Page speed.docx

---

## Set SEO-friendly URL handles with automatic redirects
Use when: Product or collection URLs are vague or non-descriptive and you're finalizing on-page SEO for those pages.
- In the product/collection's search engine listing section, replace the URL handle with the title (drop grammar/special characters — handles don't need them).
- Keep the automatic redirect option checked so the old URL forwards to the new one.
- Save; bookmarkers of the old link will be redirected instead of hitting a 404, protecting conversions.
- Apply the same handle cleanup to collections, whose handles are often wrong or generic.
Caveat: Only unchecked redirects cause lost traffic/404s — the source stresses leaving the redirect enabled whenever you change a handle.
Caveat: Changing handles has SEO implications; keep them stable once set.

Tags: speed, seo, url-handle, redirects, product-page, collection-page, shopify
Source: Page speed.docx

---

## Ensure each page has exactly one H1 tag
Use when: Auditing on-page SEO structure, especially after adding custom sections a developer built that may have introduced extra H1s.
- Inspect the page in devtools to confirm which element is the H1: on Shopify Dawn, the homepage H1 is the logo, a collection page's H1 is the collection title, and a product page's H1 is the product title.
- Scan custom sections for stray H1 tags — a developer-built or DIY section might use an H1 that competes with the real page H1.
- If two H1s describe different things, Google can't tell which is authoritative; demote the extra ones to H2/H3.
- Enforce one H1 per page across product, collection, and content pages.
Caveat: Confirmed for the Dawn theme by the presenter; other themes may structure H1s differently, so inspect rather than assume.
Caveat: Don't rely on visual size — the H1 may be the logo or a heading you didn't expect.

Tags: speed, seo, h1, on-page-seo, theme-code, shopify
Source: Page speed.docx

---

## Write 160-character meta descriptions for click-through
Use when: Finalizing a product or blog post's search engine listing meta description.
- At the bottom of the product/page editor, open the search engine listing and view the meta description (the product page can show an excerpt automatically).
- If the auto-excerpt reads well, you can leave it — especially for large catalogs where manual edits are impractical.
- Otherwise, take the product description and ask ChatGPT for a ~160-character meta description, then paste and save.
- Prioritize persuasion over keyword density here: the meta description's job is to make searchers click, more so than the page title/body copy.
Caveat: The source explicitly says you don't need keywords as heavily here as in the title/description — focus on click appeal.
Caveat: Search engines may override the description; the ~160-character figure is a guideline.

Tags: speed, seo, meta-description, ctr, product-page, shopify
Source: Page speed.docx

---

## Use internal linking to speed up crawling and discovery
Use when: Building blog content or benefit/education pages and planning how they connect to product and collection pages.
- Within blog posts and content pages, add links to the relevant products (e.g. a page describing a product's benefits should link to that product).
- Add links wherever you legitimately can across the site — from pages to products, blog posts to collections, etc.
- This helps Google discover more pages faster, because crawling one page reveals the next, which then gets crawled too.
Caveat: Link contextually and relevantly; the source frames it as helping discovery, not as a trick for arbitrary link volume.
Caveat: Blog posts each have their own title/content/search-listing fields that should also be optimized.

Tags: speed, seo, internal-linking, crawlability, content, blog, shopify
Source: Page speed.docx

---

## Verify mobile friendliness before treating SEO as complete
Use when: Pre-launch or SEO audit checklist step to confirm mobile rendering, which Google factors into authority/ranking.
- In Chrome, right-click > Inspect, then toggle the device toolbar and pick a device (e.g. iPhone 12 Pro) to preview the store.
- In Safari, use Develop > Enter Responsive Design to preview mobile rendering.
- Check that text stays within the viewport, images aren't shrunken/distorted, and everything is reachable.
- If it all renders well, you pass the mobile-friendliness check and can move to the next step (speed).
Caveat: Most modern Shopify themes are mobile-friendly out of the box, per the source, but verifying is still worthwhile.
Caveat: This is a visual/devtools check, not a formal Lighthouse category.

Tags: speed, seo, mobile-friendly, responsive-design, audit, shopify
Source: Page speed.docx

---

## Use PageSpeed Insights for a baseline and install speed snippets
Use when: Establishing a speed baseline or checking whether recent changes improved performance.
- Enter your URL on Google's PageSpeed Insights and click Analyze to get a page score plus field/historical data.
- Note that the historical graphs reflect the past 28 days, so a fix done today won't fully show in those graphs for ~28 days.
- Use the results to prioritize: loading speed is complex, and you need to fix most flagged issues to rank well.
- Apply speed-boost snippets (the source offers them) that the presenter claims can boost store speed by ~10–20%, per his own stores.
Caveat: The 10–20% snippet boost is the presenter's claim, not a guaranteed result.
Caveat: Field data lagging 28 days means you can't judge a fix from the field graphs immediately — use lab results in the meantime.

Tags: speed, pagespeed-insights, measurement, shopify, audit, loading-speed
Source: Page speed.docx

---

## Add rich snippets to earn larger search listings
Use when: Search result listings look plain and you want a bigger, richer presence (FAQ dropdowns, product ratings/prices) under your link.
- Determine the snippet type that fits a page: FAQ/Q&A for blog posts answering a question, product snippets for products, article snippets for posts.
- Add the corresponding structured data — this requires custom code or an app (the source links a guide and an app that does it).
- For product snippets, include description, rating, number of reviews, price, and availability so the listing shows these visually.
- Once rich snippets are live, your listing can occupy more vertical space (even multiple products), attracting more clicks than plain competitors.
Caveat: Requires custom code or an app; markup must match real page data (accurate prices/ratings) to be eligible.
Caveat: The source frames click advantage as the goal; it isn't a guarantee of ranking gains.

Tags: speed, seo, rich-snippets, structured-data, faq, product-page, shopify
Source: Page speed.docx

---

## Publish keyword-researched content at least twice a month
Use when: Planning an ongoing SEO content strategy to keep the store's pages fresh and discoverable.
- Plan at least two posts a month, ideally four (one per week).
- Research post topics using Keyword Planner and write about topics close to what you sell and that your customers want to learn about.
- For each post, set a title containing a main and secondary keyword, write valuable description/body text containing the keywords, and complete the search engine listing with an enticing ~160-character meta description.
- Give the post a URL handle containing the title's keywords so Google understands the page.
- Optionally connect the post with internal links to relevant products.
Caveat: The 2–4 posts/month cadence is the presenter's recommendation, not a rule Google enforces.
Caveat: Content still needs to be genuinely useful and relevant to the niche.

Tags: speed, seo, content, blog, keyword-research, publishing-cadence, shopify
Source: Page speed.docx

---

## Earn backlinks from authoritative sites and partners
Use when: Building off-page SEO and authority for a store competing for higher search placement.
- Identify authoritative websites, influencers, or friendly partners who can mention your store.
- Arrange for them to write about your store and include a link to it.
- Paying attention to partner authority matters: links from authoritative sites let your store gain some of that authority, increasing trustworthiness and ranking chances.
Caveat: The source frames backlinks as building trust/authority; link quality/authority matters more than volume.
Caveat: No specific quantity benchmark is given.

Tags: speed, seo, backlinks, authority, off-page-seo, shopify
Source: Page speed.docx

---

## Set a primary domain and submit your sitemap to Search Console
Use when: After on-page SEO is complete, kickstarting Google crawling and indexing of the store.
- In Settings > Domains, ensure a single primary domain is set (a premium/custom domain, not the myshopify one) so Google knows which URLs to crawl — do this before submitting the sitemap.
- Load your sitemap by appending /sitemap.xml to your store URL and copy that URL.
- Create/link your property in Google Search Console, then go to Indexing > Sitemaps and submit the sitemap URL.
- Google will begin crawling and indexing the store's pages.
Caveat: If you set the primary domain after submitting, you can submit a new sitemap; getting the primary domain right first avoids confusion.
Caveat: The exact Search Console menus can change; verify the current interface.

Tags: speed, seo, sitemap, search-console, indexing, primary-domain, shopify
Source: Page speed.docx

---

## Submit Sitemap and Set Primary Domain Before Google Indexing
Use when: Preparing a new or neglected Shopify store for organic search indexing before investing in on-page SEO or content.
- Link your store property to Google Search Console and open Indexing > Sitemaps.
- Paste your store's sitemap URL and hit Submit; Google will then start crawling and indexing store pages.
- Before submitting, go to Settings > Domains and confirm which domain should be primary. Stores with a custom domain often show multiple entries (the .myshopify.com plus the custom).
- Set the premium/custom domain as primary (not the myshopify URL). Do this first, then submit the sitemap so Google crawls the right URLs; if you already submitted, resubmit after switching.
- Also fill in brand information (logo, colors) under the brand tab — Search Console won't use it, but Facebook, Google and other sales channels pull it to represent you better when your products syndicate.
Caveat: Shopify admin menus and Search Console interface change; verify current panel names before following.

Tags: speed, seo, search-console, sitemap, shopify, indexing, brand-assets
Source: Page speed.docx

---

## Brand Asset Completeness for Sales Channel Syndication
Use when: Setting up or auditing a store that feeds products into Facebook, Google Shopping or other sales channels.
- Locate the brand settings tab (in the source, found via Shopify Sidekick because the menu position wasn't obvious).
- Upload logos and define brand colors there.
- This matters because external channels like Facebook and Google pull this information and use it when representing your products and store, so incomplete brand data means weaker, inconsistent presentation off-site.
- Treat this as a prerequisite feed-quality step alongside product data, not a design nicety.
Caveat: The source couldn't recall the exact menu path; use search/Sidekick or check current Shopify admin navigation.

Tags: speed, seo, shopify, brand-assets, product-feeds, sales-channels
Source: Page speed.docx

---

## Use an SEO App Dashboard to Drive Pages Toward 100% Score
Use when: Deciding whether to buy an SEO tool and how to systematize on-page optimization across many product and collection pages.
- Install an SEO app from the Shopify App Store (source demos 'SEOAnt' / AI SEO). It shows a store speed score and an SEO summary flagging issues such as uncompressed images.
- Work the flagged issues directly in the app dashboard instead of hunting them manually.
- Open a product page's breakdown and enter the target keywords you were aiming for; the score rises if you're actually targeting those keywords (source saw 80% after targeting two keywords).
- Fix the specific pointers: add an H2 in the description (source pasted the product title again and marked it H2, lifting 80% to 91), add 1-4 images inside the description, and include the target keyword in the meta description.
- Re-check score and iterate; source reached 94 with remaining issues (e.g. needing more images).
- Use the app's keyword research tool (keyword ideas, volume, trends) to pick keywords, its 'analyze my keywords' to see what you already rank for, and its competitor tracking to watch which keywords rivals rank for and how they change.
Caveat: Scores are app-specific heuristics, not Google rankings; source says 94 was 'good' without claiming rankings.
Caveat: Source appears to be affiliated with the app (offers a discount code); treat recommendations accordingly.
Caveat: Paid tiers gate some features; free tier may suffice for small stores.

Tags: speed, seo, shopify, seo-tools, keyword-research, product-page, on-page-seo
Source: Page speed.docx

---

## Automate Image Compression Instead of One-by-One Optimization
Use when: A speed or SEO audit flags uncompressed images on product and collection pages.
- Identify uncompressed images via the speed/SEO audit issue list.
- In the optimization app, choose to optimize published product images, collections, and similar asset groups.
- Trigger a bulk 'optimize all' so images compress in the background rather than exporting each image to a free compressor and re-uploading individually.
- Sequence the work: compress images first, then speed up the store, then do on-page SEO — the source presents this as the natural order.
Caveat: Only optimize published assets you actually serve; keep originals if you may need higher resolution later.

Tags: speed, seo, image-optimization, shopify, site-speed, apps
Source: Page speed.docx

---

## Reclaim Stale Keywords and Add Rich Snippets via an SEO App
Use when: Looking to grow organic traffic or improve search result presentation for existing pages and products.
- Run the app's 'analyze my keywords' to see the keywords your store already ranks for.
- Check whether any pages or blog posts rank for keywords with no search volume or that lead nowhere useful; adjust that content or page to target different, higher-value keywords.
- For rich results (FAQ snippets, product grids, top/bottom snippets, side image), use the app's search appearance section and simply turn each snippet type on — no code editing required.
- After enabling a snippet, run the app's test to confirm it's correctly added before assuming it will display.
- Use the app's broken-link finder to locate dead links (404s) and remove them; use its backlink tracking to build linking authority and support higher rankings.
Caveat: Snippet visibility is ultimately controlled by Google and may change; the app test confirms markup, not guaranteed display.

Tags: speed, seo, shopify, rich-snippets, keyword-research, backlinks, broken-links
Source: Page speed.docx

---

## Two Root Causes of Slow Shopify Stores: Layout Stability and Apps
Use when: Diagnosing slow mobile load times or deciding where to spend speed-optimization effort on a Shopify store.
- Separate issues into two buckets: layout stability (CLS, LCP) and app scripts loading from third-party servers.
- Recognize that even simple themes with little customization accumulate speed issues, and the source attributes most of them to apps rather than the theme.
- Don't remove apps wholesale — you need them to test and run the store; instead load their scripts later (after user interaction) to reduce their blocking impact.
- Frame the goal as loading the theme first and letting app functionality kick in afterward, rather than degrading app use.
Caveat: App lazy-loading may break apps that genuinely need to run immediately; verify each app after changing its loading.

Tags: speed, shopify, site-speed, core-web-vitals, apps, performance-audit
Source: Page speed.docx

---

## Find App Scripts Injected via the async Function in Your Theme Head
Use when: Investigating which apps are blocking your Shopify store load or adding layout shift.
- Right-click the live store and open Inspect, then expand the head tag.
- Scroll for empty/unnamed script tags and open them one by one; the app-injection function ('async' function) is usually in the last one but check all if unsure.
- Inside you'll see the links for every app script injected into the theme (e.g. Trustpilot widget scripts) and can see how many scripts each app contributes.
- Use this list to judge which apps load at the same time as the theme and are candidates to delay.
Caveat: Shopify theme internals and the injection mechanism may change; verify against your current theme.

Tags: speed, shopify, apps, theme-code, site-speed, diagnostics
Source: Page speed.docx

---

## Delay All App Scripts to Human Interaction via content_for_header
Use when: A simple Shopify theme still scores poorly because many app scripts load during initial render.
- In your theme's code editor, find the content_for_header tag — it's responsible for injecting all app scripts.
- Comment that tag out.
- Paste the lazy-load script (source provides one; you can also write your own delaying the async injection) directly underneath the commented tag and save.
- Wait a couple of minutes before retesting speed — testing immediately returns the old score.
- Verify: open the console, refresh, and hover/scroll on the page; you should see a confirmation message and the app widgets (e.g. Trustpilot badge) appear only after interaction.
- In the source's run, mobile speed moved from roughly 37-38 to 48-50, but significant blocking time from other apps remained.
Caveat: Requires editing theme.liquid; back up the theme first.
Caveat: Apps that must render immediately may not function correctly — test each app after applying.

Tags: speed, shopify, apps, theme-code, lazy-loading, site-speed, mobile-speed
Source: Page speed.docx

---

## Lazy-Load a Cookie Banner Script to Eliminate Its CLS and Blocking
Use when: A cookie consent banner loads with the theme and registers layout shift or blocking time in speed tests.
- Search theme.liquid for the cookie banner's script tag (the source found one already carrying a defer attribute).
- Confirm the banner is creating CLS by checking the layout shift report.
- Comment the original script tag out and add the script's URL to the lazy-load function's list, placing that function above the closing head tag.
- Save, reload the store: the banner should not appear until the user clicks, scrolls, touches, moves the mouse or presses a key — the function generates the script tag on that interaction.
- Verify in the console that the custom interaction message appears on mouse entry. In the source's run, CLS disappeared and mobile speed rose from around 48-50 to 57.
Caveat: Delaying a consent banner may have legal/compliance implications depending on your jurisdiction; confirm with your policy requirements.

Tags: speed, shopify, cookie-banner, cls, lazy-loading, theme-code, compliance
Source: Page speed.docx

---

## Lazy-Load App-Embed Widgets by Copying Their JS and CSS URLs
Use when: A theme customizer app embed (chat widget, review widget) renders immediately and you can accept loading it after interaction.
- In the theme customizer, go to App embeds and confirm which app is injecting (toggling off removes its script, toggling on adds scripts directly to the head rather than via the async function — that's why it loads early).
- Leave the toggle on temporarily, refresh the live store, open Elements in devtools and search for the app name (source searched 'vanchat').
- Find the app's JS element, right-click > Edit as HTML, copy the script URL, and add it to the lazy-load function's script list (add a comma if appending to an existing entry).
- Copy the accompanying CSS URL and paste it into the function's CSS area, then save.
- Now toggle the app embed OFF in the customizer and save — the function will inject its files on interaction instead.
- Verify the widget appears only after hover/scroll. Source's run: blocking time dropped sharply and the score moved from 57 to around 65, holding above 60 on retest.
Caveat: Only do this for apps that don't need to be on screen immediately.
Caveat: App URLs and DOM structure can change with app updates; re-verify after app upgrades.
Caveat: Test the app's full functionality after lazy-loading it.

Tags: speed, shopify, apps, app-embeds, lazy-loading, theme-code, chat-widget
Source: Page speed.docx

---

## Audit theme.liquid for Scripts Missing defer or async
Use when: Starting a Shopify speed audit or after the major app-script issues are addressed.
- Open theme.liquid and scan for script tags lacking a defer or async attribute; Shopify now flags these for you.
- For each, identify which app it belongs to (e.g. the source traced a script to an 'ILO Banner' cookie banner) and choose which attribute to apply.
- Prefer defer: async loads alongside the page, while defer waits until the site is downloaded and then fetches the script, producing less blocking time.
- Add it as either defer or defer="defer" — both work identically.
- Test whether the app still functions after adding defer; in the source's case the cookie banner still worked, meaning it didn't truly need to load immediately.
Caveat: Some apps break if their scripts are deferred and genuinely require immediate execution.
Caveat: Expect small gains from this alone — it's a cleanup step, not a headline fix.

Tags: speed, shopify, theme-code, script-loading, defer, async, performance-audit
Source: Page speed.docx

---

## Retest Speed Three Times and Average to Defeat Caching Lag
Use when: Verifying whether a speed change actually worked, or when results swing wildly between runs.
- After making a change, wait a couple of minutes before testing so files propagate.
- If you test immediately, the test may evaluate an older cached version and return essentially the same score, making you think your change did nothing.
- Run three tests and average the result rather than trusting a single run.
- Expect to spend most of your speed-audit time waiting for tests to complete — be patient.
- Note that apps loading on the store can make results swing a lot between runs.
Caveat: Source-specific practice, not a measured statistical method; use it as a practical heuristic to reduce false negatives.

Tags: speed, measurement, site-speed, testing, caching, performance-audit
Source: Page speed.docx

---

## Find Layout Shift Sources by Throttling Network to Slow 3G
Use when: Google reports a significant layout shift score but you can't tell what is moving or why.
- Open devtools Network tab, set throttling to 3G — the source found 3G still too fast to see movements clearly.
- Create a new custom throttling profile at a slower speed (source used ~20 kilobits per second) and refresh.
- If it still looks fast, switch to another profile and back to your custom one, then refresh — throttling sometimes doesn't apply directly.
- Watch elements populate slowly, then stop the page load when you spot the element in question so you can inspect its state mid-load.
- Optionally generate a loading GIF of your store via a third-party capture site to visually spot movement, though the source notes such tools may not register the same CLS that Google does.
Caveat: This is a manual diagnostic; you may need several attempts to catch the shift.
Caveat: A GIF capture tool may not show the same CLS measurement Google reports.

Tags: speed, cls, core-web-vitals, diagnostics, devtools, network-throttling, layout-shift
Source: Page speed.docx

---

## Fix Theme-Level Layout Shift Caused by Body and Inline Styles
Use when: A speed test reports a large layout shift, especially a jump involving the header or full page width.
- In the theme, check whether the body tag needs style display block — the source had historically added it to the Dawn theme to fix a jump.
- Look for inline styles that override base CSS loaded earlier: in the source, a 'page width 70%' style placed in the body tag shrank the page after it initially rendered full width, registering as CLS.
- Test removing that style to confirm it's the cause, then place the style sheet at the end of the head tag instead of in the body — the source found this both removed the CLS and loaded faster because the style no longer waited for everything to load.
- If the shrink was intentional on desktop, wrap the rule in a media query (source used min-width 767px) so mobile stays full width instead of showing shrunken text and white side bands.
- Where possible, use the theme's own layout width settings rather than hardcoded max-width to achieve the desired desktop width.
Caveat: Always confirm the intended design before removing styles the client wanted — source kept the 70% desktop width, only scoping it.
Caveat: Theme file structure differs across themes.

Tags: speed, cls, shopify, theme-code, inline-css, media-queries, layout-shift
Source: Page speed.docx

---

## Mark the First Visible Item Eager, Keep the Rest Lazy
Use when: A lazy-loaded image that is visible on initial mobile view is hurting the LCP in speed tests.
- Identify anything visible on first paint — logo, hero banner, and the first slide/card — and check whether it carries loading lazy; visible content should not be lazy-loaded.
- In the theme customizer, note the order of sections (source had a slideshow then a collection list) and open the relevant section's liquid code.
- In the collection list section's for-loop, assign a variable named lazy: set it false when the for-loop index equals 1 and true otherwise.
- Pass that variable into the card snippet by adding a line like lazy: lazy where the snippet is rendered.
- In the card collection snippet, replace the hardcoded loading lazy attribute with logic that outputs loading eager when lazy is false (first block) and loading lazy otherwise.
- Verify in the DOM that the first card renders loading eager and subsequent cards stay lazy, then retest. In the source's run this pushed mobile speed over 50.
Caveat: Only the first in-view items should be eager; making everything eager re-creates the original problem.
Caveat: Exact section/snippet names vary by theme; adapt the loop variable to your theme's structure.

Tags: speed, shopify, lcp, core-web-vitals, theme-code, lazy-loading, images
Source: Page speed.docx

---

## Verify Each Lazy-Loaded App Still Works After Changing Loading
Use when: Any time you defer, async, or lazy-load an app or theme script on a live store.
- After each change, load the storefront and exercise the app: open the chat widget, confirm the review badge renders, check the cookie banner appears on interaction.
- Use the console message from the interaction script to confirm scripts were actually injected.
- If the app breaks, restore the original script placement or re-enable the app embed — some apps' properties make them break when deferred.
- Decide per app whether it truly needs to be on screen immediately or can wait for interaction; only defer the ones that can wait.
- Keep a record of what you deferred so future app updates can be re-checked.
Caveat: An app may appear to work while a less-visible feature (e.g. form submission, tracking event) is broken; test the full flow, not just rendering.

Tags: speed, shopify, apps, lazy-loading, quality-assurance, testing, site-speed
Source: Page speed.docx

---

## Don't Trust Third-Party Caching Scripts on Shopify
Use when: Evaluating a speed tool or script that claims to speed up a Shopify store via caching.
- Identify scripts on your store belonging to unknown speed or caching services.
- Test the actual impact by commenting the script out and re-running speed tests; the source found speed remained essentially the same.
- Given Shopify handles caching automatically, don't add a caching service expecting gains, and don't remove a script you don't understand unless testing proves it's inert.
- If a mystery script's effect is unknown, leave it alone rather than risk breaking storefront behavior.
Caveat: Based on the source's informal testing of one such script, not a controlled study.

Tags: speed, shopify, caching, site-speed, apps, performance-audit
Source: Page speed.docx

---

## Follow the Speed Work Order: Defer, Lazy-Load Apps, Fix CLS, Fix LCP
Use when: Working a Shopify mobile speed score up systematically toward and past 50.
- Start by adding defer to render-blocking scripts in theme.liquid where apps tolerate it.
- Then lazy-load app scripts via the content_for_header override and per-app embed technique.
- Then hunt and fix CLS by throttled inspection and correcting offending inline CSS.
- Then fix LCP by making first in-view images eager while keeping others lazy.
- Retest three times after each stage and average, allowing a couple of minutes for changes to propagate.
- Source's documented progression on a real store: about 33 to over 50 mobile; app-script lazy-loading alone was credited with roughly 10-15% improvement when apps were the bottleneck.
- Use the outcome as directional — the same sequence won't produce identical numbers on a different store.
Caveat: Results are a single-account case study, not a guaranteed benchmark.
Caveat: If apps aren't your bottleneck, the lazy-load step may be far less effective, as the source itself cautions.

Tags: speed, shopify, site-speed, core-web-vitals, lazy-loading, cls, lcp, workflow
Source: Page speed.docx

---

## LCP diagnosis: the largest-in-viewport element and its delay source
Use when: Product or landing page speed audit where Google PageSpeed shows a poor LCP score and you need to decide what to fix first.
- Run the PageSpeed/Google test on the actual PDP or landing page you send paid traffic to, not the homepage. The source notes that even when the homepage scores fine, the page receiving ad traffic often has a huge LCP problem.
- Open Chrome DevTools, go to the Network tab, disable cache and set throttling to fast or slow 3G, then reload. Watch what actually renders. In the reviewed store the layout and secondary images appeared, but the main product image did not — the image file was already downloaded but not shown.
- Trace why it isn't shown. In the reviewed example the cause was a slideshow/carousel plugin: its JavaScript had to load before the first big image rendered, so the image sat hidden even after downloading.
- Fix the delay at its source: keep the main product image out of the lazy-loaded carousel path, use a plain img that renders immediately, and remove any preloader/placeholder that hides the in-view image.
- Add a preload link for that specific image in the head (see the preload card) and consider a more benefit-legible main image, since a confusing main image also hurts comprehension when the shopper lands from an ad.
- Re-test three times and average the results to confirm the change is constant rather than a one-off test.
Caveat: The source's affected store measured around 5 seconds LCP before and expected roughly 50-60 after a preload fix; treat these as that store's numbers, not benchmarks.
Caveat: Desktop often already scores acceptably; the source focuses mobile because that is where slow-connection shoppers experience the store.
Caveat: Editing theme.liquid requires a theme backup or duplicate before publishing.

Tags: speed, core-web-vitals, lcp, product-page, image-optimization, shopify, diagnostics
Source: Page speed.docx

---

## Handling loading="eager" vs "loading="lazy" in collection and card loops
Use when: Collection pages, homepage collection lists, or recommendation grids where you render many product images in loops and want above-the-fold images to load immediately.
- In the collection-list / grid section, add logic that tracks which card is first in render order. Assign that card's image loading="eager"; assign loading="lazy" to all subsequent cards.
- Push the same logic into the product card snippet so individual cards inherit the correct loading attribute rather than relying on a hardcoded value.
- Recognize the failure mode being fixed: when every image is lazy (including the first, in-view one), the browser delays the largest visible image; when everything is eager, non-visible images compete for bandwidth.
- Verify in the rendered page source that only the first in-view image has loading="eager" and the rest are lazy.
- Apply the same rule to hero banners, logos and slideshows — anything in the viewport should never be lazy loaded (see the above-the-fold card).
- Re-test the affected page three times and average before/after to confirm the change holds.
Caveat: The source reports this change contributed to a jump from 33 to 58 on mobile and desktop moving to 93, but it was one of several changes made together, so the improvement is not attributable to this step alone.
Caveat: Only the images genuinely in the first viewport should be eager; marking everything eager recreates the original contention problem.

Tags: speed, lazy-loading, image-optimization, collection-page, product-page, shopify, theme-code
Source: Page speed.docx

---

## Splitting above-the-fold assets from lazy-loaded assets
Use when: Deciding which images and assets in a theme's header, hero or product gallery should be lazy loaded and which should be preloaded.
- Inventory every image/video that renders in the initial viewport: logo, hero banner, main product image, first slider frame, first row of product cards.
- For those, do not add loading="lazy". Instead preload them: add link rel="preload" tags in the head listing the URLs of visible images, fonts and critical assets, and set fetch priority as high so the browser treats them as important.
- For everything below the fold, keep loading="lazy" on images and add preload="none" on videos so they don't interrupt more important downloads.
- Do not display a preloader bar or placeholder in place of an in-view image — the source describes that as an LCP generator because the image is already known to be needed and any delay showing it hurts LCP.
- Avoid transition/animation effects that delay in-view elements from appearing.
- Confirm the lazy/eager split visually under 3G throttling with cache disabled.
Caveat: The source states Google will penalize lazy-loading above-the-fold images — cited as the presenter's guidance rather than a stated numeric rule.
Caveat: Preload too many assets and you recreate contention; restrict preloads to genuinely in-view, business-critical assets.
Caveat: LCP and CLS can reappear as the store matures and new sections or apps are added, so this needs periodic re-checking.

Tags: speed, lcp, lazy-loading, preload, core-web-vitals, shopify, theme-code
Source: Page speed.docx

---

## CLS from images without dimensions: reserve space with width and height
Use when: Any PDP, homepage or landing page where content shifts as images load — the typical symptom is text pushed down after a hero or inline image appears.
- Understand the mechanism: the browser paints background, then text, and only later the images; when an inline image arrives its container expands to full image height and pushes everything below it down. This is one of the main CLS generators.
- Add width and height parameters to every image tag so the browser can reserve the correct box before the file arrives.
- Reproduce the shift to confirm the fix: open DevTools, Network tab, disable cache, set throttling to slow 3G or fast 3G — on fast Wi-Fi the shift may be too quick to see with the naked eye.
- Also run a Lighthouse test and open 'see original trace' to inspect the loading timeline and spot above-the-fold layout shifts.
- Treat non-user-initiated movement as the target; if the user clicks and the page then changes, that is not classified as CLS.
- Re-verify under the same throttle after the change.
Caveat: Setting width/height works only if the CSS respects the aspect ratio; conflicting CSS rules can still override the reserved box.
Caveat: CLS can also come from app widgets and font swaps, which need separate fixes.

Tags: speed, cls, core-web-vitals, image-optimization, diagnostics, shopify, layout-stability
Source: Page speed.docx

---

## Stopping app-widget CLS by reserving the widget container
Use when: A PDP or homepage uses a review, loyalty or upsell app widget that pops in after load and shifts the content below it.
- Identify the app-injecting element in the CLS report: the Google test outlines the shifting element. Copy its CSS classes, open your page, right-click > inspect, use Ctrl/Cmd+F to search the classes and locate the HTML tag.
- Diagnose why it moves: app widgets load after the theme's own assets, so their container has no reserved space and the whole page below drops when they render.
- Measure or approximate the widget's rendered width/height, then add a CSS rule fixing the width and height of that container so the space exists from first paint.
- Alternative diagnose: look for two contradicting CSS rules where one stylesheet sets a height and a later one changes it; remove the redundant rule instead of reserving space.
- Test the widget still functions correctly after the CSS change, on a duplicate theme first.
- Re-run the speed test and check Search Console > Core Web Vitals to see whether search performance was being affected by the shift.
Caveat: Fixing the container size can clip widget content if the widget is responsive or its size varies; verify on the real breakpoints you care about.
Caveat: The source states CLS issues shown by Google are real, not measurement errors, and that CLS affects search ranking — presenter's position, not a numeric guarantee.

Tags: speed, cls, core-web-vitals, apps, css, shopify, layout-stability
Source: Page speed.docx

---

## Matching fallback font metrics to the custom font to prevent font-swap CLS
Use when: A store uses custom or multiple brand fonts and you see text-size shifts during load, or CLS is attributed to font changes.
- Search the theme's CSS files for @font-face rules.
- If the rule lacks font-display: swap, add it — this shows a default browser font while the custom font downloads, improving perceived speed.
- Account for the side effect: default and custom fonts differ in size and line height, so at swap time the text changes size and shifts the layout.
- Add CSS that styles the fallback font to match the custom font's size as closely as possible, effectively reserving the same space the custom font will occupy.
- Verify under 3G throttling with cache disabled, since on fast connections the swap may be invisible.
- Consider consolidating the number of custom fonts, since the source notes font files slow the site down, especially with multiple fonts used for design flourish.
Caveat: Exact matching is hard; the goal is minimizing the shift, not eliminating it.
Caveat: Swap without metric matching trades a slight delay for a layout shift — decide per font whether the brand font is worth it.

Tags: speed, cls, fonts, core-web-vitals, css, shopify
Source: Page speed.docx

---

## Removing residual code from uninstalled apps and old tracking
Use when: Speed cleanup pass on any live theme, especially after removing apps, changing analytics, or when 'remove unused JavaScript' keeps appearing.
- Open theme.liquid and look for mentions of apps you have uninstalled (the source's example: a YOTPO script left after removing YOTPO). Remove them.
- Check whether a script belongs to an app: go to Apps in admin and confirm whether the app is installed. Some scripts belong to apps listed as sales channels, so check that list too.
- If you can't identify a script or app, ask whoever managed the store — it may belong to an external service not listed in Shopify's app store.
- Search all theme files, not just theme.liquid, for the script name. The source recommends the 'Shopify theme file search' Chrome extension for this, or a code editor.
- Also remove dead tracking pixels, scripts, custom fonts and other assets that no longer serve sales or conversion.
- Back up or duplicate the theme before editing so you can publish/revert safely.
Caveat: Some dependencies are JavaScript files, CSS files or rendered snippets, not just script tags.
Caveat: Removing a script that is still needed can silently break app functionality — verify apps on a duplicate theme before publishing.

Tags: speed, unused-javascript, apps, shopify, theme-code, maintenance, diagnostics
Source: Page speed.docx

---

## Deferring or lazy-loading app scripts so they don't block core content
Use when: PageSpeed reports unused JavaScript from app scripts and the store's core content should render before app widgets.
- Decide whether the app's widget genuinely needs to appear immediately at first paint. The source argues most apps don't; their scripts should be lazily loaded so core content loads first.
- If the script is visible in theme.liquid, add defer so it runs only after the document is downloaded. Then verify the app still functions — some apps break with defer.
- If defer breaks or the app stops loading, try async, which downloads alongside the document without blocking it. Verify again.
- If you can't find the script in theme.liquid, it is being injected automatically. Find the injection point: search for content_for_header in theme.liquid.
- Inspect the page head to find the injected inline script and the app's URL inside its async function. Capture content_for_header with Liquid, redefine it with that script removed, and turn the app's admin/customizer toggle off.
- Add your own small script that injects the app script on user interaction — click, scroll or other input — then verify app functionality and re-test.
Caveat: You must test app functionality after each change; a script that fails to inject may silently remove reviews, upsells or loyalty features from the storefront.
Caveat: Tracking pixels should not be deferred, per the source, because deferring them can corrupt collected data.
Caveat: Injecting scripts on interaction can delay widget display until the shopper engages — check whether the widget's value depends on being visible at load (e.g. review stars above the fold).

Tags: speed, unused-javascript, apps, theme-code, shopify, defer-async, performance
Source: Page speed.docx

---

## Lazy-loading Shopify's dynamic payment button script
Use when: Cart or PDP speed work where the dynamic checkout / payment button script is heavy and you aren't sure customers use those buttons.
- Check whether shoppers actually use the dynamic payment buttons (e.g. Shop Pay / wallet buttons) placed under the add-to-cart button.
- If they don't create value, disable the dynamic buttons entirely — the source describes this script as demanding and as slowing the store noticeably.
- If you keep them, locate the script to stop it loading: edit theme.liquid and add a line that removes it from content_for_header, using the same capture-and-modify Liquid approach used for app scripts.
- Add a case to your human-interaction injection script so the payment script loads when the user clicks, scrolls or otherwise interacts.
- Verify the payment buttons still appear and function after interaction on a duplicate theme, then re-test speed.
Caveat: Because the buttons appear only after interaction, evaluate whether hiding them until then could reduce wallet-button conversions — this is a trade-off the source does not quantify.
Caveat: Test on a copy theme before publishing so customers don't see errors.

Tags: speed, checkout, apps, theme-code, shopify, unused-javascript, payment
Source: Page speed.docx

---

## CSS that rewrites base styles from the body tag
Use when: A store shows horizontal layout problems or mobile content squished in a narrow column and you're auditing theme CSS load order.
- Inspect the DOM and identify any style block or CSS file loading at the end of the body tag that overrides rules already set in the theme's base CSS file.
- Understand the side effect: base CSS loads first with basic settings, then the late CSS rewrites them, producing layout problems (the source's case: horizontal issues on mobile).
- Move that style into the head, after the base stylesheet, so the cascade is predictable.
- If the rule should only apply on desktop, wrap it in a media query so it affects only screens above the relevant breakpoint. In the source's case a media query restricted it to screens over 767px, letting mobile content go full width instead of being squeezed into about 70% width.
- Check other symptoms of late-loading CSS: large blank gaps on a PDP are real estate to reclaim, since the source argues the add-to-cart area should sit high on the page.
- Re-verify mobile rendering at the widths your shoppers actually use (e.g. an iPhone-class viewport).
Caveat: The 767px breakpoint is the source's example, not a universal threshold — pick based on your theme's breakpoints.
Caveat: Moving CSS can change specificity outcomes elsewhere; check the affected pages, not just the one that prompted the change.

Tags: speed, css, theme-code, mobile, product-page, shopify, layout
Source: Page speed.docx

---

## Fixing layout shift from the body tag with display:block
Use when: A PDP or homepage hero visibly jumps upward as the page loads, or CLS is traced to the initial body/hero rendering.
- Reproduce the shift under slow 3G with cache disabled and watch the hero banner area specifically — the source observed the hero loading lower on the page and then being pushed up.
- Add display: block to the body tag in the theme's CSS. The source reports this resolved that particular shift.
- Combine with width and height on the hero image and any above-the-fold preloads, since body display alone won't fix image-induced shifts.
- Re-test with the Google speed test and confirm the CLS element no longer appears in the results.
- Run the test multiple times and average to avoid reading a single noisy result.
Caveat: This is one specific fix from one store review; if the shift persists, check contradicting CSS heights and app widgets as other causes.
Caveat: Some themes set body display via their own base CSS — verify your change isn't overridden.

Tags: speed, cls, css, theme-code, shopify, hero-banner, layout-stability
Source: Page speed.docx

---

## Cookie banner modification via a theme property
Use when: A store's cookie consent banner is identified as a speed blocker during a PageSpeed/theme audit.
- Confirm the cookie banner is contributing to blocking or delayed paint in the speed test or DevTools timeline.
- In the source's review, the fix was adding a different property to the cookie banner code rather than the mechanism it previously used.
- Make changes on a duplicate theme, then re-test three times and compare the average against the pre-change baseline, since the source performed this change alongside several others.
- Verify the banner still satisfies whatever consent requirement your store operates under — speed gains do not justify an invalid or missing consent flow.
- Re-check both mobile and desktop scores after the change; the source's desktop score, for instance, reached 93 while mobile just cleared 50 in its example.
Caveat: The source does not name the specific cookie banner or the exact property value, so treat this as a category of fix to investigate for your banner.
Caveat: Consent banners are frequently legally required; do not remove or obscure consent to gain speed.

Tags: speed, apps, theme-code, shopify, third-party-scripts, privacy
Source: Page speed.docx

---

## The seven-step Shopify speed framework and its order of operations
Use when: Planning a full speed optimization pass on a Shopify store before or during paid traffic campaigns.
- 1. Reduce apps. Every app means fetching assets from another server, and some load their assets as early as possible. If an app doesn't directly boost sales or improve the user experience, remove it, then clean residual code from theme files.
- 2. Remove residual code: dead scripts, old tracking pixels, unused custom fonts and other assets that don't serve sales or conversion.
- 3. Fix images: size to the devices shoppers use rather than uploading full-resolution camera files; JPEG under 1MB is the source's stated target for a full-HD-ish image covering any screen; use PNG only when transparency is needed; replace animated GIFs with compressed MP4 video in an HTML video tag; compress images and video (the source names compressjpeg.com as a free option, claiming 50-60%+ size reduction).
- 4. Fonts: add font-display: swap to @font-face rules and match fallback metrics to avoid CLS.
- 5. Prioritize scripts: defer non-essential app scripts; async for scripts that should load alongside without blocking; never defer tracking pixels.
- 6. CSS: defer non-visible CSS with the media onload print technique, but not CSS responsible for in-view elements.
- 7. Lazy load apps and their assets: load the store's core first, then inject app scripts on click or scroll.
Caveat: The listed 50-60% compression figure and the under-1MB JPEG guidance are the source's recommendations, not measured results for your store.
Caveat: The source ties speed to profitability but provides no conversion benchmark; do not treat speed score gains as guaranteed revenue gains.

Tags: speed, shopify, core-web-vitals, apps, image-optimization, fonts, performance
Source: Page speed.docx

---

## Choosing app and functionality by value to protect speed
Use when: App audit or cleanup decision on a store that has accumulated apps over time.
- List installed apps, sales-channel apps and any external scripts. For each, ask whether it creates real value that translates into more money for the store.
- Remove apps whose widget doesn't contribute — the source's framing is that most app widgets do not need to display at first paint.
- Check whether remaining apps' scripts can be deferred, made async or injected on interaction (see the app script cards).
- Watch for app side effects beyond scripts: widgets that inject HTML and shift layout, and CSS that conflicts with your base styles.
- Account for the fact that shops slow down over time: the source describes an initial 60-80% speed score dropping to 40, then to 20, 10 or lower as apps and customization are added — re-audit periodically rather than once.
- Check under throttled 3G with cache disabled after each change.
Caveat: The source's numbers about score decline are illustrative of typical patterns, not measurements of any specific store.
Caveat: Some apps genuinely need to render early (e.g. a reviews badge above the fold) — evaluate per app rather than blanket-deferring.

Tags: speed, apps, shopify, performance, maintenance, diagnostics, third-party-scripts
Source: Page speed.docx

---

## Testing protocol: three runs, averaged, on a duplicate theme
Use when: Any speed change you plan to make — establishing a before/after baseline so you don't chase noisy single-test results.
- Duplicate the live theme and use its preview link for testing. Note that the source acknowledges the preview link runs slightly slower than the live link, but still shows the difference between states.
- Pick a reference page: typically homepage, product page or collection page, depending on where traffic lands.
- Run the test three times on that page, allowing some time between runs, and record each result. Without gaps you tend to get the same result.
- Average the three results to establish your baseline.
- Implement one batch of changes, wait about a minute, then run three more tests and average again.
- Compare averages, not single readings, and verify app functionality on the duplicate theme before publishing.
Caveat: Preview-link results are inherently a bit slower than live, so compare like-for-like rather than against an absolute target.
Caveat: The source's example store was described as 'rather basic'; results on heavily customized themes will differ.
Caveat: Averaging three runs does not remove day-to-day variance in Google's test infrastructure — treat differences of a few points cautiously.

Tags: speed, measurement, experiment-design, shopify, testing, diagnostics, methodology
Source: Page speed.docx

---

## Simulating the real shopper's device and connection instead of your desk
Use when: Before deciding a store is 'fast enough', and when prioritizing which speed work actually matters to paid-traffic conversion.
- Test the store the way customers experience it: open it on mobile data away from strong Wi-Fi, or emulate a slow 3G connection in DevTools with cache disabled.
- Recognize that a store can look fine on your laptop while a customer on a 3G connection sees a blank or partially loaded layout — the source describes the customer's first impression being a blank page rather than the designed store.
- Note the source's stated context: shoppers on older devices and slower networks, and a general claim that many people shopping online use older mobile devices and don't always have fast internet.
- Prioritize mobile speed work over desktop; in the source's reviews desktop was often already acceptable while mobile was the problem.
- Focus on the page your ads point to — the source observes that ad traffic typically lands on the product page, so that page's LCP and mobile layout matter more than the homepage.
- Pay attention to a store scoring around 20% or lower on Google's speed score; the source treats that level as an indicator many customers will struggle or fail to load the store.
Caveat: The source references studies about average adult attention span around 8 seconds and claims customers leave after 3-4 seconds of an unloaded layout — these are presented as general claims, not store-specific measurements.
Caveat: If you don't send traffic to the homepage, the source advises not over-investing there, but still keeping the product-page-to-homepage experience cohesive.

Tags: speed, mobile, core-web-vitals, diagnostics, conversion-optimization, shopify, product-page
Source: Page speed.docx

---

## Product page mobile layout: get the add-to-cart within the visible band
Use when: Mobile PDP layout work where the buy button sits below a large header, logo, promo text or gallery.
- Pull a scroll heatmap (the source used Hotjar) for the product page. Read the percentages by depth: everyone in the source's example saw the header and first image, then dropped to 93, 91, 80 and so on, with only 20% of visitors reaching the add-to-cart button.
- Treat that drop-off as a layout problem: the buy button is effectively invisible to most mobile visitors.
- Shrink the mobile logo (the source tried values around 120, 110 and even 100px), reduce or single-line the header text, remove oversized gaps, and keep the mobile layout's horizontal real estate working hard.
- Move variants and quantity directly under the reviews, and try placing the benefit row below the buy button rather than above it — the source suggests testing both orders rather than assuming.
- Make the add-to-cart button slightly thinner and full page width, and test wording (the source suggests comparing 'add to bag' vs 'add to cart' depending on where your customers are).
- Make sure the review badge is present on mobile if it's on desktop; in the reviewed store it was missing on mobile.
- Re-project cost/conversion on a duplicate theme before publishing layout changes.
Caveat: The heatmap percentages are from one reviewed store and are an illustration of reading depth drop-off, not a benchmark.
Caveat: Recommendations such as exact logo pixel size or button thinness are the source's opinions from that review, not universal rules.
Caveat: Layout changes interact: verify the whole PDP after moving blocks.
Caveat: Move variants and quantity directly under the reviews, and try placing the benefit row below the buy button rather than above it — the source suggests testing both orders rather than assuming.

Tags: speed, product-page, mobile, conversion-optimization, heatmaps, merchandising, shopify
Source: Page speed.docx

---

## Clarifying the promo message so shoppers can act on it
Use when: PDP or cart promotion messaging, especially sitewide bars or badges combining several incentive types.
- Audit the promo copy on the product page. The source flags an example reading '20 to 50% off with free shipping today only'.
- Replace it with a single clear offer, e.g. '50% off with free shipping' or '20% off with free shipping'.
- Rationale given: people get confused easily, and an unclear offer weakens the page's message and its ability to convert paid traffic.
- Check for similar ambiguity elsewhere — separate offer claims in different page sections that appear to contradict each other.
- Keep promotion duration and terms consistent with what you can actually honor at checkout; a page promise that checkout can't fulfill creates friction.
Caveat: This is the presenter's guidance from a store review, not a tested A/B result.
Caveat: Discount messaging and margin trade-offs are store-specific; verify the promoted offer is sustainable.

Tags: speed, product-page, offer-design, messaging, conversion-optimization, shopify, pricing
Source: Page speed.docx

---

## Diagnose Shopify's Composite Speed Score
Use when: You need to make sense of the speed score in your Shopify admin versus a single-page Google/Lighthouse test, or you want to know which templates to optimize when improving store speed.
- Open the speed score in the Shopify admin and click through to see which pages Shopify says it measures — typically the home page, a collection page and a product page (the most-trafficked ones).
- Test those pages yourself multiple times (the source suggests running each 3–4 times and averaging) because a single run varies widely; the Shopify score is essentially an average of the three pages.
- Recognize that if you have multiple product or collection templates, fixing only the template Shopify links to gives partial improvement; editing all templates for a page type produces extra speed gain.
- After fixing images, scripts or assets, expect a delay before the dashboard score updates — the source's experience is roughly 12–24 hours, driven by store traffic rather than an instant refresh.
- Combine the Shopify score with Google PageSpeed Insights and Chrome Lighthouse, since Google surfaces only the top issues and others appear as you fix them.
Caveat: Score refresh timing (12–24h) is the presenter's field observation, not a documented SLA; verify against current Shopify reporting.

Tags: speed, measurement, shopify, performance-audit, core-web-vitals
Source: Page speed.docx

---

## Set a CLS Target and Find Shifts in Lighthouse Trace
Use when: Google Search Console flags CLS, a store's organic ranking drops, or you need to find which above-the-fold elements move during page load on your home or product pages.
- Run a Lighthouse test in Chrome, then choose 'View Original Trace' and watch the timeline: note the first paint and each point where new elements appear and push existing content down.
- In the source's example cases, the culprits were the top menu/header appearing late, the Afterpay widget injecting and pushing content down, and product thumbnails appearing at the bottom — all above the fold.
- For an element whose size is contradicted by two CSS rules (e.g. two stylesheets setting different heights), remove one conflicting rule.
- For an app that injects a widget (like reviews), determine the container size the widget needs and add CSS reserving that fixed width and height so the rest of the page doesn't move when the widget loads.
- Repeat across home, collection and product pages, since each has different apps and scripts loading.
Caveat: The source's target: keep CLS under 0.25, ideally near 0.1 or 0; the presenter's case dropped 0.73 → 0.13 → 0.1 → 0 over roughly 28 days, which is an example, not a promise.
Caveat: CLS data in Search Console lags real fixes by days/weeks.

Tags: speed, cls, layout-shift, core-web-vitals, shopify, debugging, product-page
Source: Page speed.docx

---

## Recompile Critical CSS for Lazy-Loaded Theme CSS
Use when: Your theme delays loading theme.css (or otherwise renders unstyled content briefly) and Lighthouse shows layout shift in the first second on home, collection or product templates.
- Confirm the pattern: theme.css downloads only after the rest of the DOM, so for the first second elements render unstyled and then jump into place when CSS loads — often invisible to the eye but captured by Google's test.
- Add inline critical CSS for the visible portion of each template so the page looks correct before theme.css arrives.
- In the source's example, the theme already had critical CSS for home, collection and product pages, but it was incomplete/miscompiled — the fix was recompiling a correct critical CSS file.
- Compile critical CSS with an online critical-CSS generator: feed the full theme CSS file plus the URL you want critical CSS for.
- Create separate critical CSS for visually different templates (e.g. a collection page with a banner vs one without).
- Insert the snippet that serves the critical CSS inline in theme.liquid, then test repeatedly with Lighthouse, zooming out to catch below-the-fold shifts too.
- For any element still moving (e.g. font-size changes), add a CSS rule reserving its final size so the change no longer displaces neighbors.
Caveat: Does not fully fix below-the-fold elements; the source admits Google weighs those less but says fixing them anyway is worthwhile.
Caveat: Lighthouse shows fewer issues than Google Speed Insights; address Lighthouse first, then move to Google's list.

Tags: speed, cls, critical-css, shopify, layout-shift, performance-audit, theme
Source: Page speed.docx

---

## Reserve Space for Widgets That Inject Late
Use when: A review app, payment widget or similar injected element visibly jumps into place and pushes other content during your store's load, on home, product or collection pages.
- Identify the injected widget by watching the Lighthouse original trace or reloading the page; note exactly which element appears and how far it pushes content.
- Determine the size the widget needs (inspect it after it renders, or check the app's documentation) then add a CSS rule fixing its container's width and height.
- If two CSS files conflict on the same element's height, remove one of the contradicting rules instead of stacking more overrides.
- Re-test with Lighthouse and confirm the shift is gone, both at normal zoom and zoomed out to surface below-the-fold shifts the source admits are lower priority.
- Cross-check in Google Speed Insights, which surfaces elements Lighthouse omits, and add CSS rules preventing those from shifting too.
Caveat: Ongoing Google Speed Insights may show green while Search Console lags by a couple of days.
Caveat: Presenter's position: most CLS he sees is a CSS issue or an app widget needing reserved space, but other causes exist.

Tags: speed, cls, shopify, widgets, layout-shift, css, conversion-optimization
Source: Page speed.docx

---

## Defer or Lazy-Trigger App Scripts to Shield Core Assets
Use when: Speed tests flag unused jQuery/app JavaScript that loads in the first second even though the app's widget is not visible, and you still need the app for later interaction (e.g. reviews, SMS).
- Screen every installed app against one question: does it directly impact conversion or user experience? If not, remove it; if yes, check whether it needs to load in the first second at all.
- On scripts you control (from theme.liquid), add defer or async so they load after core assets; test the app afterwards, as some break with these properties.
- For scripts injected by an app's async function, locate the injected script in the theme's head, copy its URL, modify content_for_header to exclude that URL, and list the modified content_for_header — this stops the automatic injection.
- Then create a snippet (e.g. lazy-scripts.liquid) containing vanilla JS that re-creates the script tag with that src, triggered on a click or scroll event; render it from theme.liquid.
- Re-run the speed test to confirm the delayed app still fires immediately when the user clicks or scrolls, and that the score improves.
Caveat: Scripts with pixels/tracking important for ad campaigns (e.g. Facebook, Google) should stay in the initial load and not be deferred.
Caveat: Delayed app loading is only safe when the widget is not needed above the fold; verify each app still functions.

Tags: speed, shopify, javascript, defer, lazy-loading, apps, user-interaction
Source: Page speed.docx

---

## Assess Whether Each Blocking Script Is Visible or Pixels
Use when: Google speed tests flag unused JavaScript / 'reduce unused JavaScript' on your home, collection or product page and you need to decide which scripts to keep, defer or remove.
- Read the flagged items: 'unused JavaScript' usually means unused during the test's window, not permanently — decide if each script is needed right away.
- Begin with an app inventory: remove apps that add no value, that are purely visual, or that you no longer use; uninstalling still leaves residual script tags you must search out and delete.
- For each remaining script, check whether its widget is actually visible at load. The source's example: Yotpo and Recharge widgets exist only on collection/product pages, so they don't need to run on the home page.
- Conditionally load app assets only on templates that use their widget; this also removes associated 'reduce unused CSS' warnings for that app.
- Keep pixels (Facebook, Google) and measurement tools in the initial load since they must track the user right away; keep Hotjar for interaction measurement.
- Investigate duplicate injections — e.g. a Facebook script added both manually in theme.liquid and via an app — and eliminate the duplicate.
Caveat: You may not be able to minify app-provided code; instead cut it from pages where it isn't needed.
Caveat: Some app assets (e.g. ones without compression) are outside your control unless you raise it with the app's support or drop the app.

Tags: speed, shopify, javascript, apps, conditional-loading, measurement, performance-audit
Source: Page speed.docx

---

## Clean Residual Scripts After Uninstalling Apps
Use when: You have removed or no longer use an app (or plugin) but its assets may still be loading and slowing your Shopify store.
- Open theme.liquid and search for the app's name (the source's example searches for 'yotpo' after uninstalling the Yotpo reviews app) and delete every script tag containing it.
- Do the same in head.liquid and footer.liquid, since injected assets may live in any of these theme files.
- Also audit scripts and style tags for plugins you stopped using — they often linger and keep loading.
- Review the full contents of theme.liquid, head.liquid and footer.liquid and judge each entry's relevance; remove any asset with no current function.
- Re-run speed tests to confirm the residual assets are gone and the store loads without them.
Caveat: Removing script tags can break an app you are still using — verify the specific app is truly uninstalled or unused first.

Tags: speed, shopify, apps, theme, cleanup, performance-audit
Source: Page speed.docx

---

## Right-Size Images and Pick the Correct Format
Use when: Speed tests show images are too large for mobile, or your store's pages load slowly because of oversized image assets.
- Convert large source images to a full-HD-size JPEG compressed under 1 MB — the source states this is sufficient for any screen size, especially for mobile-majority traffic.
- Use PNG only when the image needs a transparent background; avoid animated GIFs (unprofessional and heavy) and instead upload a compressed MP4 using an HTML video tag.
- For above-the-fold assets like the first hero or main product image, do not lazy-load them; they should load immediately.
- Use preload='none' on videos so they load without blocking other elements.
- Apply loading='lazy' to images not initially visible; for a carousel, lazy-load the second, third (etc.) images but not the first.
Caveat: 'Under 1 MB JPEG is sufficient for any screen' is the presenter's rule of thumb, not a measurement of your specific catalog.
Caveat: Lazy-loading the first visible image causes layout issues and hurts speed — the source calls this out as a common mistake.

Tags: speed, images, lazy-loading, mobile, product-page, shopify, hero-image
Source: Page speed.docx

---

## Use lazy-sizes for Bulletproof Image Lazy Loading
Use when: You want stronger lazy loading than the native loading='lazy' attribute gives, e.g. for a slide-out drawer or list of images below the fold.
- Install a lazy loading plugin like lazy-sizes on your theme.
- On each image to lazy-load, set src to an empty pixel, add data-src with the real image URL, and add the plugin's lazy-load class.
- Let lazy-sizes replace the src with the data-src URL once the image is needed, so the DOM downloads without being blocked by image requests.
- Verify behavior: in the source's example, the drawer's images show gray placeholders first, then the real files download.
- Never apply this to images in the initial viewport (hero, first carousel image, main product image).
Caveat: The presenter's opinion is that lazy-sizes does the job slightly better than the native property, but the native property works.
Caveat: Adding it to an image already visible at load defeats the purpose and creates the very layout issues you're avoiding.

Tags: speed, lazy-loading, images, shopify, plugins, product-page, drawer
Source: Page speed.docx

---

## Font Loading: Add font-display: swap
Use when: Your theme uses multiple custom fonts and speed tests show text-rendering delays or layout shifts caused by font loading.
- Locate the @font-face rules in your theme's CSS files.
- Add font-display: swap to each @font-face rule that lacks it, so a default font displays while the custom font downloads.
- This prevents text from being blocked and reduces perceived load time and shift from font-size changes.
- If a font-size change still shifts layout, add a CSS rule reserving the element's final size so neighbors don't move.
Caveat: Multiple custom fonts increase asset size; consolidating font files reduces the problem at the source.

Tags: speed, fonts, css, shopify, text-rendering, layout-shift
Source: Page speed.docx

---

## Defer and Async Scripts to Prioritize Core Assets
Use when: You control script tags in theme.liquid and want app/plugin scripts to stop delaying core asset loading.
- List the scripts in theme.liquid and ask, for each: does this need to load before or after the site is fully loaded?
- For scripts not needed immediately, add the defer attribute so they execute after core assets finish; add async to load them in parallel without blocking, when order doesn't matter.
- Common candidates for deferral: app scripts whose widgets aren't above the fold; tracking pixels (e.g. Facebook, Google) are the exception that should stay immediate.
- Test after altering each script — the source notes some apps stop working when defer or async is added.
- Go a step further (for a developer) by loading the entire store and core assets with no app scripts, then injecting those scripts on a click or scroll event.
Caveat: Some apps break with defer/async — verify functionality after each change.
Caveat: The interaction-triggered injection approach may require a specialist to tailor to your scenario.

Tags: speed, javascript, defer, async, shopify, conversion-optimization, apps
Source: Page speed.docx

---

## Delay Non-Visible CSS with media-onload-Print
Use when: Large CSS files reference elements below the fold and your store's CSS is blocking rendering.
- Identify CSS files that style elements not visible during initial page load.
- Apply the media='print' onload='this.media=all' technique so the stylesheet is fetched but only applied to the real view after load.
- Keep critical CSS (above-the-fold styles) in place so the visible view stays styled from the first paint.
- Re-test the page to confirm the CSS no longer blocks loading and the visible area remains correct.
Caveat: Confirm the delayed CSS genuinely styles only below-the-fold elements; misapplying it leaves visible content unstyled.

Tags: speed, css, shopify, render-blocking, critical-css, lazy-loading
Source: Page speed.docx

---

## Evaluate Speed-Apps and Optimization Vendors Skeptically
Use when: You are considering buying a speed-optimization app or hiring a speed specialist for your Shopify store.
- Treat 'speed-up' apps with caution: the source states they only work with returning users, if at all.
- When hiring a specialist, verify improvements with your own real-user-timing data, not just a Google score — the audience sees tricks that improve ratings while end-user load stays slow.
- Accept that there is no fast, one-action fix; expect a series of small changes across pages and templates.
- Prioritize serving what's needed for the current view first rather than loading the whole asset library in the first seconds — the source's restaurant analogy: serve the drink, appetizer, first course rather than cooking the entire menu at once.
- Work through fixes template by template: after fixing the main page-type templates, also run and fix secondary product/collection templates.
Caveat: The 'returning users only' claim is the presenter's experience, not a measured benchmark.

Tags: speed, shopify, apps, performance-audit, measurement, conversion-optimization
Source: Page speed.docx

---

## Check Page Vitals Before Trusting Them
Use when: Your home page shows 'all vitals passed' and you're deciding whether store speed is genuinely healthy, or you're auditing a store for the first time.
- Run speed tests on all three pages Shopify uses — home, a collection page and a product page — not just the home page.
- Do not equate passed vitals with a good score; the source's example store passed vitals yet scored 18 on home, 38 on collection and worse on product, combining to roughly 20.
- Aggregate a picture across pages: pages can carry different apps/scripts, so one page may be fine while another is broken.
- Fix the main issues (app load, JS blocking, image sizing, CSS), then expect new issues to surface in the test list as old ones are cleared.
- Re-run every page type and every unique template repeatedly until the score improves.
Caveat: The 18/38/≈20 figures are one audited store's example, not benchmarks for your store.

Tags: speed, measurement, core-web-vitals, shopify, performance-audit, product-page, collection-page
Source: Page speed.docx

---

## Reproduce the Original Page-Speed Audit Method
Use when: You're running a full speed audit of your own Shopify store for the first time and need a consistent sequence of steps.
- Install no new apps yet; first inventory existing apps and remove any that don't directly affect conversion or UX.
- Look at the JavaScript blocking delay (the source's example showed 2.7s from apps) and check for duplicates like Facebook pixel loaded twice (e.g. manual edit plus app).
- For each app script, ask whether it needs to load at page load: social widget, PostScript, etc. can often be loaded later or removed if unused. Keep pixels and heatmaps (Facebook, Google, Hotjar) since they must measure right away.
- Fix image sizing flagged as too large for mobile, and apply lazy loading to below-the-fold images only — not the first hero, first carousel slide or product image.
- Address blocking CSS — separate critical CSS from non-visible stylesheets — and fix any CSS delays from app widgets.
- Where app assets lack compression or minification, either contact the app's support or remove the app; then re-test home, collection and product pages.
Caveat: Some listed issues (app compression/minification) are outside your control if you keep the app.
Caveat: The presenter notes more advanced fixes exist beyond this main list.

Tags: speed, performance-audit, shopify, apps, images, css, javascript
Source: Page speed.docx

---

## Understand the Three Core Web Vitals and Their Thresholds
Use when: Setting performance targets for your storefront's key templates (homepage, category, PDP, checkout) before or during a speed optimization project.
- Treat LCP (Largest Contentful Paint) as your loading-performance metric: the time until the largest image or text block renders. Target under 2.5 seconds; the source treats anything over 4 seconds as bad and likely to hurt SEO.
- Treat FID (First Input Delay) as your interactivity metric: the time from a user's first click to the browser processing that event handler. Target under 100 ms; over 300 ms is bad. The source's framing: you don't want a page that renders while its controls don't work.
- Treat CLS (Cumulative Layout Shift) as your visual-stability metric: unexpected jumps/movement of elements. Fix it by reserving space so late-loading assets don't shove content around.
- Prioritize by element, not by metric: identify the largest above-the-fold element (often a hero image or headline) for LCP, and the elements that jump for CLS.
- Note the thresholds are the source's framing of Google's guidance; verify current thresholds against Google's live documentation since these bands can change.
- Because customers bounce when a slow page denies them instant gratification, the source argues page-load performance is directly tied to revenue—so don't deprioritize speed behind cosmetic redesigns.
Caveat: FID only captures delay on the first input; it says nothing about ongoing responsiveness after first interaction.
Caveat: The source presents 2.5s/4.0s, 100ms/300ms bands as the practical good/bad lines, not a fine-grained calculation.

Tags: speed, core-web-vitals, measurement, product-page, landing-page, conversion-optimization, bounce-rate
Source: The ultimate guide to web performance.docx

---

## Diagnose LCP Bottlenecks with the Network Waterfall
Use when: When your homepage, category page, or PDP loads slowly and you need to identify which specific asset is the LCP bottleneck.
- Open your store page and open the browser's Network tab, then look at the network waterfall.
- Scan for assets drawn as very wide bars; the source says these are your bottlenecks because they take the longest to load.
- Identify which asset is actually the largest rendered element (often the hero product image or headline) and check whether it's the one blocking LCP.
- Cross-check with the Web Vitals Chrome extension below—the waterfall narrows the timing, the extension names the exact DOM element.
- Once identified, attack the bottleneck with the LCP optimization card (compression, CDN, preload, avoid render-blocking JS).
Caveat: Waterfall view is browser- and device-environment dependent; what is slow on your connection may differ on mobile networks, which is where most storefront traffic often sits.
Caveat: The waterfall shows timing, not which element Google considers the LCP candidate—use the extension for that.

Tags: speed, core-web-vitals, lcp, chrome-devtools, diagnostics, product-page
Source: The ultimate guide to web performance.docx

---

## Optimize LCP: Compress, Serve via CDN, Unblock Rendering
Use when: After you've identified your LCP element and need concrete fixes for your hero image, category tiles, or above-the-fold content.
- Reduce resource load time: compress images and move to modern formats like WebP; reduce fonts to the bare minimum needed to render the page, since each font is a downloaded asset.
- Serve assets from a CDN. The source notes deploying to platforms like Firebase or Vercel handles CDN delivery automatically, so you don't manually manage edge caching.
- Eliminate render-blocking JavaScript above the fold. If scripts must execute before the hero image displays, they delay LCP. The source cites this as a reason server-side frameworks (e.g., Next.js) beat client-only single-page apps like plain React on initial load—SPAs must run a lot of JS before main content renders.
- Use preload links so important assets are discovered first by the browser, and set fetchpriority to high on critical above-the-fold images so low-priority below-fold images don't compete with them.
Caveat: Switching rendering architecture (SPA to SSR) is a major rebuild, not a quick tactical fix; only pursue it if the simpler levers are insufficient.
Caveat: The source's deployment-platform CDN behavior is a snapshot and vendor interfaces change—verify current behavior in your platform's docs.

Tags: speed, core-web-vitals, lcp, cdn, image-optimization, webp, javascript-optimization, product-page
Source: The ultimate guide to web performance.docx

---

## Make the LCP Element Explicit with Preload and Fetchpriority
Use when: When a hero product image or above-the-fold headline loads late because the browser is guessing wrong about priority.
- Identify your LCP candidate element first (via the Web Vitals extension), typically the main hero image on a homepage or the primary product image on a PDP.
- Add a preload link for that asset so the browser discovers it early rather than waiting on CSS/JS parsing.
- Set fetchpriority="high" (per the source's guidance) on the critical image; set low priority on below-the-fold images so they don't load ahead of the hero.
- Verify the change reduced LCP in a lab run (Lighthouse or the Web Vitals extension) or field data, rather than assuming the attribute alone fixed it.
- Do not over-apply: marking everything high-priority defeats the point and can re-create competition for bandwidth.
Caveat: Source states this as a general ability of modern browsers; exact syntax and behavior should be verified against current browser support before shipping.
Caveat: Preloading too many assets can worsen performance by forcing unnecessary early downloads.

Tags: speed, lcp, resource-priority, preload, product-page, landing-page, core-web-vitals
Source: The ultimate guide to web performance.docx

---

## Reduce product-page interaction delay by cutting JavaScript execution
Use when: When customers click add-to-cart, filters, or quantity controls and experience noticeable lag before the page responds.
- Measure INP and profile slow variant selectors, filters and add-to-cart controls in current browser performance tools; the source FID extension workflow is historical.
- The source says the primary optimization is reducing JavaScript execution time—you cannot simply delete all JS, so move or defer it instead.
- Move non-essential third-party scripts (analytics, chat, pixels) off the main thread using Web Workers; the source names Partytown as the tool for offloading third-party scripts to a worker.
- Use framework lazy loading (e.g., React lazy) to defer non-critical components until needed, keeping the main thread free at first interaction.
- Consider interactivity-focused frameworks like Qwik, which the source describes as using aggressive lazy loading to achieve instant interactivity—relevant if you're rebuilding.
Caveat: Third-party scripts (chat widgets, personalization, remarketing pixels) are common in ecommerce and are exactly the scripts worth offloading; test that the offloaded tool still functions.
Caveat: Framework-level changes are architectural and costly; treat tools like Qwik as rebuild-time options, not drop-in fixes.
Caveat: FID has been replaced by INP. Offloading requires integration compatibility; do not move every third-party script to a worker automatically. https://web.dev/articles/vitals

Tags: speed, core-web-vitals, fid, javascript-optimization, web-workers, partytown, lazy-loading, cart
Source: The ultimate guide to web performance.docx

---

## Prevent CLS with Explicit Image Dimensions and aspect-ratio
Use when: When category grids, PDP images, or ingredient/spec elements jump as they load, causing mis-taps or a broken-feeling storefront.
- Give every image explicit width and height attributes so the browser can reserve its space before the file loads.
- Alternatively, use the CSS aspect-ratio property to reserve space without hardcoding exact pixel dimensions—the source highlights this as the flexible way to avoid CLS.
- For responsive images that must change aspect ratio by viewport, use the srcset attribute to serve different images under different conditions rather than letting the layout shift.
- Audit known CLS generators in ecommerce: injected advertisements, promotional banners that push content down, and over-ambitious entrance animations. Reserve space for ad/banner slots even when empty.
- Verify with Lighthouse or the Web Vitals extension, which names the DOM elements causing shift so you can investigate each.
Caveat: Explicit dimensions alone don't fix dynamic content such as personalized banners or promo slots—those need reserved containers.
Caveat: The source treats animations as a contributor to bad CLS when they do too much; temper motion effects near interactive controls.

Tags: speed, core-web-vitals, cls, image-optimization, aspect-ratio, category-page, product-page, checkout
Source: The ultimate guide to web performance.docx

---

## Use the Web Vitals Chrome Extension to Name the Exact Problem Element
Use when: When Lighthouse gives you a numeric score but you need to know which actual element on your homepage or PDP to fix.
- Install the Web Vitals Chrome extension from the Chrome team, then open its settings and enable console logging.
- Open your storefront page and open the browser console; you will receive console logs for CLS and LCP as the page loads.
- For LCP, the log names exactly which element affects the metric—that's the element to optimize—and it breaks down subparts such as Time to First Byte and element render delay.
- For CLS, the log lists the DOM elements causing layout shift; investigate each and apply the aspect-ratio/dimensions fixes.
- Click something on the page to receive an FID log, plus additional measurement chances for interactions after the first.
Caveat: The source describes the extension as newly released at the time and says it was in personal use for only a couple of days—verify the current interface and available logs.
Caveat: Lab measurement on your machine won't equal field performance across your real customers' devices and networks.

Tags: speed, core-web-vitals, measurement, chrome-extension, lcp, cls, fid, diagnostics
Source: The ultimate guide to web performance.docx

---

## Run Site-Wide Audits in Parallel with Unlighthouse
Use when: When your store has hundreds or thousands of URLs (product, category, and content pages) and manual per-page auditing is impossible.
- Create a new directory for the audit work.
- Run the command `npx unlighthouse --site <url>` with your store's address; the tool runs Google Lighthouse reports on every page in parallel, so hundreds of pages take only a couple of minutes per the source.
- Watch the UI, which shows performance in real time as results come in.
- Review results to find outlier pages with very poor performance—the source's point is these are pages you would never have known were slow from spot-checking.
- Fix outliers and, since Unlighthouse has an SDK, consider integrating it into your continuous integration pipeline so new deploys can't silently regress page performance.
Caveat: Site-wide audits can hammer a production server; run against a staging environment or throttle where appropriate.
Caveat: The exact CLI flags may change over time—verify against the current Unlighthouse documentation before relying on the command.
Caveat: Parallel lab audits approximate performance; treat scores as triage, confirming important pages with field data.

Tags: speed, core-web-vitals, unlighthouse, auditing, lighthouse, ci-cd, measurement, diagnostics
Source: The ultimate guide to web performance.docx

---

## Use Lighthouse Scores to Triage, Not to Judge Vendors
Use when: When deciding which performance targets are realistic for your store, or when a stakeholder points at a competitor's high score.
- Treat audit scores as triage for finding slow pages, not as an absolute judgment of site quality. The source's sample of major sites (Amazon, Google, Reddit, Hub, Astro) averaged around 90, with Astro's framework homepage near perfect—these are examples, not benchmarks you must hit.
- Recognize that a complex commerce site can still perform well: the source expected Amazon to do poorly given heavy imagery but found it actually did quite well, while the Web Vitals extension still showed CLS issues on it.
- Prioritize the pages that actually drive revenue (homepage, top category pages, top PDPs, cart/checkout entry) rather than chasing a uniform score across every URL.
- Pair the aggregate score with element-level diagnosis (Web Vitals extension, network waterfall) so you fix real user-visible problems rather than optimizing for the audit tool.
- Set expectations: a perfect score on a marketing site (like the Astro homepage) is not a fair target for an image-heavy catalog.
Caveat: Scores vary by device profile, network throttling, and third-party scripts, so comparisons across different setups are not apples-to-apples.
Caveat: The source only observed these sites briefly in its own tests; do not treat its impressions as durable benchmark data.

Tags: speed, core-web-vitals, lighthouse, auditing, measurement, prioritization, conversion-optimization
Source: The ultimate guide to web performance.docx

---

## Prioritize speed fixes by financial impact and conversion benchmarks
Use when: Deciding whether to invest engineering time in site speed, or building a business case for a performance sprint before a peak sales period.
- Establish the source's benchmarks as reference points, not guarantees: Google recommends two seconds or less for ecommerce page load; Portent found sites loading within one second converted at roughly 2.5x the rate of sites loading within five seconds; Deloitte reported a 0.1 second speed improvement lifted retail conversions 8.4% and fast-session spend by nearly 10%; the source also cites conversion dropping about 0.3% per additional second and 70% of consumers saying slow loads affect willingness to buy.
- Translate speed into your own money using the source's arithmetic: with a $60 average order value and 5,000 daily visitors, the article estimates a one-second delay could cost about $9,000 per day. Recompute with your real AOV and traffic rather than quoting the example.
- Note the source's caveat that all speed-testing tools score differently and any single 'page load' figure picks one marker (e.g. time to first byte), so use scores to guide decisions rather than as absolute truth.
- Balance speed against the user journey: the article explicitly says you must weigh speed against a UI that optimizes the customer journey, so don't strip elements that drive conversion just to win a score.
- Sequence work by likely payoff: images are cited as 50-75% of page weight, so compression and resizing usually offers the largest early gain; then async/defer scripts, app removal, and Liquid deduplication.
- If in-house skills are missing, the source suggests engaging a Shopify Plus Partner for theme-level work.
- Verify current Core Web Vitals thresholds and tool interfaces before committing to targets, since Google's metrics and dashboards change.
Caveat: Conversion and financial figures are cited from third-party studies and vendor examples; they are illustrative, not guarantees for your store.
Caveat: Some cited statistics appear contradictory (e.g. 'millisecond improvement' vs '0.1 second improvement' at 8.4%), so treat the direction of the effect as the takeaway, not the exact number.
Caveat: Benchmark numbers should never be treated as a universal rule; measure your own baseline before and after changes.

Tags: speed, measurement, conversion-optimization, core-web-vitals, benchmarking, mobile, prioritization
Source: Website Speed Optimization Tips for Shopify Stores.docx

---

## Use asset_url to force Shopify CDN cache refresh
Use when: After editing theme CSS or JavaScript and finding browsers or the CDN still serve an old version of the asset.
- Understand the mechanism: Shopify tells its Fastly-powered CDN when assets (images, JS, CSS) change by appending a version number to generated URLs, e.g. ?v=1384022871. That version tells the CDN to pull the correct version.
- Use the asset_url filter (e.g. in Liquid: {{ 'theme.css' | asset_url | stylesheet_tag }}) for CSS and JS references so Shopify auto-appends the version number.
- Watch out for hardcoded URLs inside your CSS: the article warns that content referenced directly in CSS is static, won't carry Shopify's asset version, and may not update automatically.
- Convert CSS syntax to reference assets through the asset_url filter so updates propagate automatically rather than being pinned to stale URLs.
- Double-check the Shopify Help Center's current list of URL filters, as filter names and behavior can change with platform updates.
Caveat: This applies specifically to Shopify's asset pipeline; other platforms use different cache-busting conventions.
Caveat: Verify the current Liquid filter documentation, since Shopify's templating APIs can evolve.

Tags: speed, shopify, cdn, caching, liquid, resource-optimization
Source: Website Speed Optimization Tips for Shopify Stores.docx

---

## Deduplicate Liquid forloops to cut server execution time
Use when: Auditing a Shopify theme's performance or after multiple developers have worked on the same theme and page rendering feels heavy.
- Understand what forloop iteration means in Shopify's Liquid: the system loops (crawls or searches) all products in a collection to find a condition, such as a price or a tag.
- Accept that loops are sometimes necessary and beneficial, for example outputting images or product variants, and are less costly on collections with few products. The problem is repetition, not loops in principle.
- Review theme code to confirm you aren't running Liquid forloops multiple times looking for the same information, a common symptom when several developers work on one theme and duplicate or conflict with each other's code.
- Remove the duplicate iterations so the same data isn't fetched repeatedly during a single render.
- Where possible, replace heavy loops with a simpler loop such as product.options_with_values, which exposes option data without crawling the whole collection.
- Consult current Shopify Liquid documentation before refactoring, since templating language behavior can change.
Caveat: Deduplicating loops requires code access and comfort with Liquid; otherwise delegate to a developer or Shopify Plus Partner.
Caveat: The article does not specify measurable gains from this fix, so treat it as a structural improvement rather than a guaranteed result.

Tags: speed, shopify, liquid, resource-optimization, theme-development
Source: Website Speed Optimization Tips for Shopify Stores.docx

---

## Audit and remove third-party apps slowing your Shopify store
Use when: Reviewing a bloated app stack or evaluating whether to install one more app on a Shopify store.
- Recognize the mechanism: most script and CSS files for apps installed through Shopify Admin are injected into the <head> of theme.liquid through the {{ content_for_header }} object, and an app must be rendered before other code loads.
- Note the source's threshold: if you have more than 20 plugins installed, you likely aren't using them all, yet they still run in the background and can hurt performance.
- Enlist a developer to remove unnecessary apps, including forgotten trials.
- Re-test after removals using PageSpeed Insights, GTmetrix, or Chrome DevTools' Network tab (reload the page with the tab open) to see the effect.
- Before any new install, ask whether the app's added value outweighs the possible load-speed penalty.
- Understand the async nuance from Shopify's Jason Bowman: scripts added via the Script Tag API are async-loaded so page load isn't halted, but scripts added directly into the <head> often impact performance immediately. Prefer the API path where available.
Caveat: The 20-plugin figure is a heuristic, not a cutoff; an app's weight matters more than its count.
Caveat: Third-party app code isn't fully under your control, so removing apps may need developer support.
Caveat: Shopify's app-injection and Script Tag behaviors may change; verify against current documentation.

Tags: speed, shopify, third-party-apps, resource-optimization, audit
Source: Website Speed Optimization Tips for Shopify Stores.docx

---

## Unblock HTML parsing with defer and async on script tags
Use when: Diagnosing slow first render where the browser appears to stall before showing content on a Shopify or any site.
- Learn the definition: parser-blocking scripts force the browser to halt HTML parsing until the script is fully downloaded and executed, so nothing else can continue.
- Apply the specific fix: add defer or async to the script tag. Example from the source: parser blocking is <script src="jquery.js"></script>; not parser blocking is <script src="jquery.js" defer></script>.
- Remember the clarifying principle: JavaScript itself doesn't block the browser, how JavaScript is loaded determines whether it blocks.
- After changing attributes, retest to confirm the site still behaves as intended, since defer/async change execution order and timing assumptions.
- Use defer when scripts must run in order after parsing; use async when a script is independent and can run whenever it finishes downloading (the article presents both as valid fixes without prescribing which for which case).
- Re-run a speed test to verify the parser stall is resolved.
Caveat: Changing load behavior can break scripts that depend on execution order; the source explicitly advises checking the site still works.
Caveat: The article notes that scripts added directly into the <head> still often impact performance even with async handling elsewhere.

Tags: speed, javascript, parser-blocking, resource-optimization, shopify
Source: Website Speed Optimization Tips for Shopify Stores.docx

---

## Compress and resize images with correct Shopify size parameters
Use when: Optimizing page weight across product, collection, or landing pages where images dominate load time.
- Start with scale awareness: images account for roughly 50-75% of a web page's total weight, and each image creates its own HTTP request, so trimming them is high leverage.
- Apply lossless compression with tools like TinyJPG or TinyPNG to cut file size without visible quality loss.
- Use Shopify's built-in image size parameters to request the exact size displayed, which reduces the file downloaded from the CDN and cuts browser-side scaling work.
- Hunt for empty image sources such as <img src=' '>, which still send an extra request to your servers; remove them.
- Consolidate small UI images (icons) into CSS sprites to limit individual image requests.
- For assets that shouldn't render immediately, defer them with lazy loading or srcset as a catch-all (the article pairs this with hero-slider guidance).
- Set a review habit for stores publishing many products or blog posts, since images tend to be added without scrutiny over time; the source cites a client case where optimization cut image space by 60%.
Caveat: The 60% reduction is one agency's client example, not a benchmark.
Caveat: Shopify's image size parameter syntax should be verified against current documentation.

Tags: speed, images, shopify, resource-optimization, core-web-vitals, lazy-loading
Source: Website Speed Optimization Tips for Shopify Stores.docx

---

## Replace standard YouTube embeds with lite embeds
Use when: A product page, landing page, or homepage uses YouTube or similar video embeds and load time is a concern.
- Identify the problem: standard YouTube embed code downloads files even before a visitor clicks play and uses a fixed-size <iframe> that doesn't adapt to different screen sizes.
- Adopt lite embeds: on initial page load, only the thumbnail image is embedded; the video player and its JavaScript load when the user clicks inside the thumbnail.
- Use the size comparison as motivation: YouTube thumbnails are about 15 kilobytes, so lite embeds can reduce page weight by almost a megabyte compared with a full embed.
- Apply the mobile-specific rule: disable mobile video autoplay, because weak cellular connections must then download a large file; replace autoplay with a static thumbnail and a button that triggers the video.
- Verify the lite-embed library or approach still functions with current YouTube embedding policy, as embed APIs change.
Caveat: Lite embeds trade a tiny bit of click friction for large weight savings; test that the click-to-play experience still converts as intended.
Caveat: Implementation specifics vary by platform and embed library.

Tags: speed, video, mobile, resource-optimization, landing-page
Source: Website Speed Optimization Tips for Shopify Stores.docx

---

## Remove or defer Quick View pop-ups on collection pages
Use when: Reviewing a Shopify collection or category page that feels slow or bounce-prone, especially on mobile.
- Understand the cost: Quick View implementations (theme-built or app-based) sometimes pre-load entire product page data in case a visitor clicks the button. On a collection with 20-30 thumbnails, that's an enormous amount of data loaded up front.
- Weigh the customer experience downsides the source lists: Quick View adds an extra step to the journey, can be clicked by accident, and can be mistaken for a product page.
- Check whether shoppers even use it using click mapping tools such as Hindsight or Hotjar to see where users scroll and click.
- Locate the feature: check the theme customizer for an enable/disable option; if absent, check whether an app provides it; if neither, it's likely baked into the theme and needs a developer.
- The source's clear preference is removal. If it must stay, either use AJAX to fetch product information only on click, or store a limited set of product data as data attributes on the grid item and build the pop-up dynamically with JavaScript.
- Note the source's own qualification: both alternatives are less ideal than removing it, because product information still loads per product, though less than downloading all images and links.
Caveat: The article states even AJAX or data-attribute approaches are inferior to removing Quick View.
Caveat: Theme-level removal may require a Shopify Plus Service Partner.

Tags: speed, shopify, product-page, merchandising, mobile, resource-optimization
Source: Website Speed Optimization Tips for Shopify Stores.docx

---

## Cut pop-ups and hero sliders that add page weight
Use when: Merchandising a homepage or landing page where promo pop-ups and rotating hero carousels are slowing load.
- Set pop-up triggers that don't compete with initial page load: the source recommends displaying pop-ups immediately on load, or using exit-intent or time-delay triggers, so there's breathing room between page load and pop-up load. Too many flashing graphics hurt speed and distract from the content you optimized.
- Reduce or eliminate homepage hero sliders: the size and quality needed for a slider to look good increases load times, especially with four to five slides.
- Prefer a single high-quality hero image with a clear call to action; the source cites that the brain processes visual imagery about 60,000 times faster than text (attribution: source, not a conversion benchmark).
- If a slider is required, follow the article's UX rules: two to three slides maximum, render slides as static content sections rather than auto-rotating carousels, and use srcset or Lazy Load. It points to Chubbies using optimized images instead of a hero slider.
- Which one should you start with? Test whether a simplified theme alone helps: the source cites an agency's observation of greater than 50% improvement in homepage bounce rate for new visitors after switching to a streamlined theme, which is an example, not a promise.
Caveat: The 94%-design and 60,000x image-processing figures are cited research/opinion in the source; use them as persuasion, not measured KPIs.
Caveat: The 50% bounce-rate improvement is one practitioner's observation with no stated controls.

Tags: speed, landing-page, merchandising, homepage, mobile, resource-optimization
Source: Website Speed Optimization Tips for Shopify Stores.docx

---

## Clean up redirects, broken links, and use 301s correctly
Use when: Doing a technical SEO or speed audit of store navigation, collection URLs, or after replatforming or renaming products.
- Recognize the cost: too many redirects and broken links hurt performance and SEO rankings; 302 redirects (temporary moves) can hurt SEO and trigger additional HTTP requests and data transfer delays.
- Prefer cacheable redirects or Shopify's built-in redirects function within the Navigation panel, which are 301s by default.
- Follow the source's rule: never redirect URLs to pages that are themselves redirects, as this creates chains.
- Find and remove broken links for page elements like images, CSS, and JS files, which add HTTP requests and sting site speed; use a tool such as Broken Link Checker.
- Create custom 404 pages to help visitors who land on an incorrect URL; the source cites Gymshark directing 404s to its two biggest categories, demonstrating a merchandising recovery path from a broken link.
Caveat: Redirect cleanup is ongoing, not one-time, especially as products and collections are renamed.
Caveat: Shopify's built-in redirect behavior should be verified in current admin documentation.

Tags: speed, seo, redirects, shopify, resource-optimization
Source: Website Speed Optimization Tips for Shopify Stores.docx

---

## Apply lazy loading to below-fold content
Use when: Optimizing a product page, collection, or homepage that loads many images, reviews, or carousels up front.
- Understand the principle: lazy loading prevents all content from loading immediately; content only loads when users hit certain triggers.
- Apply it to product pages by letting above-the-fold content (title, imagery, description) load immediately while supporting content loads on scroll. User-generated content, social carousels, and customer reviews are cited explicitly as good lazy-load candidates.
- Remember the browser behavior this solves: a browser will simultaneously download every image on a page regardless of visibility; lazy load only downloads an image when it can be viewed in the browser.
- Use the cited agency example as an illustration of the pattern, not a promise: a client site with a staggering number of below-fold images was improved by lazy loading.
- In Shopify specifically, the source also recommends srcset or Lazy Load as a catch-all with hero/slider imagery.
- Verify interaction with above-the-fold content so first meaningful paint isn't harmed.
Caveat: The source does not quantify conversion impact from lazy loading; it describes the mechanism and one practitioner's experience.
Caveat: Implementing it incorrectly can hide content from crawlers or delay content users expect immediately.

Tags: speed, lazy-loading, product-page, resource-optimization, core-web-vitals
Source: Website Speed Optimization Tips for Shopify Stores.docx

---

## Consolidate tracking tags with a tag management system
Use when: A store loads multiple analytics, conversion, and retargeting tags and page speed is suffering, or you need to disable a failing tag quickly.
- Identify the culprit: JavaScript tracking tags for general analytics, conversions, goals, and behavioral retargeting are often to blame for slow performance.
- Use a tag manager to organize deployment, triggers and removal of tracking tags. Audit the requests and execution cost of each tag; one container does not make all vendor tags one network request.
- Note the operational benefit: if a tag failure takes your site down, a TMS lets you remove the tag quickly.
- Use the source's practitioner evidence as direction, not guarantee: Anatta's Nirav Sheth says that when optimizing a beauty client's speed, nothing moved the needle more than combining Shopify API leverage with cleaning up Google Tag Manager.
- Standard GTM container setup mechanics are outside this card's scope; follow the Shopify Plus Help Center guidelines for platform-specific configuration.
- Re-verify current GTM and Shopify integration interfaces before changing tag setup, as they change over time.
Caveat: The GTM 'needle mover' claim is a practitioner opinion from one agency's client project, not a controlled result.
Caveat: Poorly governed GTM containers can themselves accumulate tag bloat, so the consolidation only helps if it's maintained.
Caveat: Editorial correction: container consolidation alone does not establish a speed improvement. Measure the resulting store waterfall. https://developers.google.com/tag-platform/tag-manager/web

Tags: speed, measurement, google-tag-manager, third-party-apps, shopify
Source: Website Speed Optimization Tips for Shopify Stores.docx

---

## Run and interpret website speed tests with the right expectations
Use when: Establishing a speed baseline before optimization work, or verifying the impact of changes.
- Accept that each tool scores differently and any 'page load' timing picks one specific marker, such as time to first byte, so scores aren't directly comparable between tools.
- Use Google PageSpeed Insights for personalized recommendations and to identify elements like CSS and JavaScript slowing the page; it also scores Core Web Vitals as Good, Needs Improvement, or Poor. Note that on sites meeting Core Web Vitals thresholds, users were cited as 24% less likely to abandon mid-load.
- Use GTmetrix for an A-to-F grade merging YSlow and PageSpeed data, including page load speed, Web Vitals/Lighthouse analysis, optimization opportunities, and page composition by requests and total byte size.
- Use Pingdom for a 0-100 score and a waterfall analysis that helps identify problem areas line by line; it surfaces recommendations like reducing DNS lookups, fewer HTTP requests, and compression.
- Know the core metrics: fully loaded page, time to first byte, and first meaningful paint.
- You can also run tests on competitors' mobile sites to see what's wrong with theirs and avoid the same mistakes.
- Use results to guide decision-making but keep an open mind; balance speed against a UI that optimizes the customer journey.
Caveat: The 24% abandonment figure is cited from research and applies to sites meeting Core Web Vitals thresholds; it is not a universal prediction.
Caveat: These tools are third-party surfaces and their scoring methodology can change; verify current behavior before using scores as KPIs.

Tags: speed, measurement, core-web-vitals, page-speed-insights, gtmetrix, pingdom, benchmarking
Source: Website Speed Optimization Tips for Shopify Stores.docx

---

## Optimize mobile checkout with Shop Pay and mobile-first speed
Use when: Improving mobile conversion on the path from cart to order, where shoppers abandon due to checkout delays.
- Include checkout in every speed optimization effort: the source notes checkout is often forgotten while home, product, and category pages get attention, and failing to optimize it likely raises cart abandonment.
- Prioritize impulse shoppers: the article's reasoning is that people are confident enough to select items, but delays at checkout mean they have to really love the product to stick around.
- Enable Shop Pay for one-click mobile checkout. The source cites Shopify's figure that merchants using Shop Pay checkouts have a 1.91x higher mobile checkout-to-order rate than regular checkout. Note this is a platform-reported comparison and may involve differences in shopper mix.
- Support the pattern with Kotn's stated rationale: most customers discover products on mobile and if they have to fill out a form, they're lost; Shop Pay's million-merchant network even lets new customers check out in one click.
- Combine with other mobile speed fixes the source lists: disabling video autoplay, and considering AMP via a Shopify app (AMP, Fire AMP, or The AMP App) if you need it.
- Review current Shopify checkout documentation, since Shop Pay availability and third-party checkout rules vary by plan and region.
Caveat: The 1.91x checkout-to-order comparison is Shopify-reported and not a controlled independent study.
Caveat: AMP benefits cited (2x time on page, 20% conversion increase) come from the source and may not transfer; AMP app availability on Shopify should be verified.
Caveat: Checkout extensibility rules differ by Shopify plan.

Tags: speed, checkout, mobile, shopify, shop-pay, retention
Source: Website Speed Optimization Tips for Shopify Stores.docx

---

## Research hosting and platform capacity for peak traffic events
Use when: Preparing a store for a major sales event or choosing an ecommerce platform/hosting plan.
- Accept the source's precondition: if your commerce platform isn't committed to making speed a priority, the other optimizations make a smaller difference.
- When researching hosting requirements, check for memory or bandwidth limits for scaling during seasonal promotions, and estimate projected traffic and peak user load to avoid crashes from sudden spikes.
- Before any major sales event, ask your commerce platform provider to help you prepare for unexpected traffic spikes or an influx of orders.
- Weigh the source's evidence: one survey cited 81% of respondents saying 60 minutes of downtime costs their business more than $300,000 (a survey figure, not a guarantee); JB Hi-Fi's site went down two hours during BFCM, illustrating brand damage from outages.
- Consider rendering architecture as part of the picture: Shopify's Storefront Renderer (SFR) is cited as 2.5-5x faster for server-side requests, with the biggest gains on cache misses; Rhone Apparel reported a 15% revenue increase, 17% conversion increase, 12% lower average page load, 37.95% lower average server response time, and 3% lower bounce rate after adopting SFR. Treat these as vendor case-study figures.
Caveat: All figures here are vendor or survey-sourced case studies published by Shopify, not independent measurements.
Caveat: Headless commerce and other architectural changes are out of this card's scope and may add complexity rather than remove it.

Tags: speed, hosting, shopify, capacity-planning, bfcm, infrastructure
Source: Website Speed Optimization Tips for Shopify Stores.docx

---

## Measure Perceived Performance With Slow-4G Throttling
Use when: Evaluating whether your product or landing page actually loads acceptably for real shoppers before or after a speed optimization pass.
- Open Chrome DevTools and go to the Network tab.
- Set the throttling dropdown from 'No throttling' to 'Slow 4G' or '3G' — pick the one closest to your typical visitor's connection (the presenter uses Slow 4G).
- Check 'Disable Cache' so you don't fetch assets from memory and mask the real experience.
- Reload the page and watch: note time-to-first-content, layout jumps, and slow image reveal in chunks.
- Compare against a non-optimized copy of the same page to isolate the impact of your changes.
- Remember the presenter's point: third-party scores (PageSpeed Insights, GTmetrix, Gift of Speed) are not the best measure — perceived experience on slow connections is the primary metric.
Caveat: Disabled cache is a worst case; most real users benefit from cached assets, so also test with cache enabled to see the typical case.
Caveat: Presenter's opinion that scores are not the best way is source-specific; scores still correlate with real gains from fundamental fixes.

Tags: core-web-vitals, performance-testing, perceived-performance, chromedevtools, resource-optimization, landing-page
Source: WordPress Speed Optimization_ Improve Your Website Performance & Make It Faster (Step-By-Step).docx

---

## Set loading=eager Above the Fold and lazy Below
Use when: Optimizing image loading order on a homepage, PDP hero, or landing page where above-fold images must appear fast and off-screen images shouldn't block.
- Identify which images are visible on first paint: hero image, logo, above-fold banners.
- Set loading="eager" on those — even though it is the browser default, set it explicitly so a later optimization plugin doesn't accidentally lazy-load them.
- Set loading="lazy" on all images below the fold, including any repeated logo in the footer.
- Note you cannot lazy-load CSS background images with the loading attribute; optimize those files instead.
- In Oxygen, add the attribute under the element's Settings/Properties panel (attribute name 'loading', value 'eager' or 'lazy'), and use right-click 'Copy settings' / 'Paste settings' to apply across many images quickly.
- After pasting settings, re-add alt text you may have overwritten — decorative images get an empty alt attribute.
Caveat: Verify your builder's exact attribute panel, interface labels may differ by tool or version.
Caveat: Background images are not covered by the loading attribute.

Tags: core-web-vitals, lazy-loading, resource-optimization, performance-testing, wordpress, landing-page
Source: WordPress Speed Optimization_ Improve Your Website Performance & Make It Faster (Step-By-Step).docx

---

## Fix CLS With Explicit Width and Height Attributes
Use when: Fixing a red CLS score or content jumping on load on your homepage, PDP, or landing page.
- On the live front end, right-click the image and choose Inspect.
- Find the image tag and hover over the src (source URL) to read the rendered size — e.g. 398x597 px.
- In your builder, add a width attribute equal to the rendered width (no 'px' unit) and a height attribute equal to the rendered height.
- Repeat for every image; for non-absolutely-positioned images this matters most, but add to absolutely-positioned images as good practice too.
- Reuse settings via copy/paste for image sets that share identical rendered dimensions.
- Retest in PageSpeed Insights to confirm CLS moves into the green.
Caveat: Explicit dimensions reserve space but do not by themselves fix other shift sources (ads, injected content, web fonts).
Caveat: Presenter's example dropped CLS into the green after two simple changes — a case result, not a guarantee.

Tags: core-web-vitals, cls, resource-optimization, performance-testing, chromedevtools, landing-page, product-page
Source: WordPress Speed Optimization_ Improve Your Website Performance & Make It Faster (Step-By-Step).docx

---

## Convert and Resize Images With AVIF at 2x Rendered Size
Use when: Reducing image payload on image-heavy pages such as homepage heroes, product galleries, or landing pages.
- Inspect an image and hover the source URL to read both rendered size and intrinsic size plus current file size (e.g. rendered 398x597, intrinsic 1770x2560, 161KB).
- If intrinsic is far larger than rendered, there is waste to remove.
- Open the image in Photopea (free, browser-based, no login needed) or an equivalent editor.
- Export as AVIF (better compression than WebP/JPG/PNG while retaining quality and supporting transparency); WebP is an acceptable alternative with broad support.
- Resize to 2x the rendered size — e.g. 796x1194 for a 398x597 render — so high-density retina screens stay sharp without loading oversized originals.
- Keep the export quality slider around 50% (presenter finds the difference imperceptible) and confirm the file size drop.
- For background images that must cover a section, keep dimensions but still convert to AVIF.
- Swap optimized files into the page and add alt text to each while you work.
Caveat: Manual conversion is time-consuming; paid plugins like ShortPixel or Imagify can automate it.
Caveat: You can also resize via the WordPress media library, but that alone won't give the AVIF/WebP file-size savings.
Caveat: Presenter's 161KB→~10KB drop is a case example, not a benchmark.

Tags: resource-optimization, images, avif, webp, retina, landing-page, product-page
Source: WordPress Speed Optimization_ Improve Your Website Performance & Make It Faster (Step-By-Step).docx

---

## Audit Loaded Assets With a Waterfall Chart
Use when: Reducing render-blocking resources on a landing page or homepage before deeper optimization.
- In PageSpeed Insights, check the 'Render-blocking requests' section for its flagged items.
- For full detail, use the GTmetrix waterfall chart to see every request in load order.
- Scan for things you don't use on this page: jQuery (not needed by logged-out users), WooCommerce CSS/JS on a page with no cart or add-to-cart, unused block styles.
- Note which assets are global (needed everywhere) versus page-specific (can be unloaded here).
- Build a list of assets to remove, then unload them via theme/builder performance settings or a page-level plugin.
Caveat: PageSpeed Insights flags may not show every loaded asset; the waterfall gives the complete picture.
Caveat: Be conservative: unload only what this page truly doesn't use.

Tags: resource-optimization, performance-testing, waterfall, gtmetrix, javascript, landing-page
Source: WordPress Speed Optimization_ Improve Your Website Performance & Make It Faster (Step-By-Step).docx

---

## Dequeue jQuery for Logged-Out Front-End Users
Use when: Trimming render-blocking scripts on public pages where jQuery is confirmed unused but WordPress loads it by default.
- Confirm via the waterfall that jQuery (and jQuery Migrate) is loading on your public page.
- Create a code snippet (e.g. with WP Codebox) that hooks wp_enqueue_scripts and dequeues plus deregisters jQuery for the relevant scope.
- Add conditions so the snippet runs only when needed: front end (location) AND user not logged in — the WordPress admin bar needs jQuery for logged-in users.
- Enable the snippet and re-run the waterfall to confirm jQuery no longer loads for logged-out visitors.
- Only do this if your theme/plugins truly don't depend on jQuery on the front end, or you'll break scripts.
Caveat: Verify current hook and function names against WordPress docs, APIs change.
Caveat: Tool set (WP Codebox) and snippet UI may differ; confirm the current interface.

Tags: resource-optimization, javascript, jquery, wordpress, performance-testing, front-end
Source: WordPress Speed Optimization_ Improve Your Website Performance & Make It Faster (Step-By-Step).docx

---

## Unload Unused WooCommerce Assets Per Page With Asset CleanUp
Use when: A landing page or content page loads WooCommerce or other plugin assets it never uses, slowing first paint.
- Install the free Asset CleanUp plugin from the WordPress repository.
- Open the specific page in the editor; Asset CleanUp adds a metabox listing loaded files by source (e.g. WooCommerce category with 13 files).
- Expand the group and unload files not needed on this page: brand styles, source buster, add-to-cart, block styles CSS, jQuery block UI, etc.
- Review each before unloading — the presenter keeps a small 'coming soon' CSS file because its size is negligible.
- Save; the unloading applies only to that page, keeping assets elsewhere.
- Record what you unloaded — if you later add a WooCommerce feature like a mini cart to this page, you must re-enable those assets.
Caveat: Per-page unloading is page-specific; a new page with the same template needs its own setup.
Caveat: Verify plugin name and interface from current WordPress repo listing.

Tags: resource-optimization, woocommerce, css, javascript, wordpress, landing-page, page-speed
Source: WordPress Speed Optimization_ Improve Your Website Performance & Make It Faster (Step-By-Step).docx

---

## Unload Default WordPress Bloat for Logged-Out Users
Use when: Establishing a fast baseline on any WordPress storefront before page-specific fixes.
- Open your theme or builder's performance settings (e.g. Oxygen → Performance).
- Enable options that fit your site: disable Gutenberg block CSS (if not using Gutenberg), disable emojis, disable dashicons for logged-out users, remove/disable pingbacks.
- Skip any option tied to a feature you actually use — if you use Gutenberg blocks, keep block CSS.
- Save and re-check the waterfall to confirm the bloat is gone.
- Apply site-wide, since these defaults load everywhere.
Caveat: Settings locations differ by builder/theme; confirm current UI.
Caveat: Disabling a feature you rely on can break rendering — audit before enabling each toggle.

Tags: resource-optimization, wordpress, css, javascript, page-speed, baseline
Source: WordPress Speed Optimization_ Improve Your Website Performance & Make It Faster (Step-By-Step).docx

---

## Self-Host Google Fonts as WOFF2 to Cut External Requests
Use when: Reducing third-party font requests and render-blocking on your storefront, especially where fonts are used site-wide.
- Find your fonts on fonts.google.com and add them to your list (e.g. Inter, Libre Baskerville).
- Download the font files — you get TTF, which you must convert to WOFF2 web-font format.
- Convert using Google Web Fonts Helper (recommended; Font Squirrel's Webfont Generator also works but the presenter found it failed on some fonts, possibly variable ones).
- In your builder/theme, upload the WOFF2 files as custom fonts, specifying the font weight (e.g. 900) and style (italic/normal) for each.
- Name the local versions distinctly (e.g. 'Inter Local') so you can tell them apart in the font picker.
- Switch your font variables (body/heading) to the local versions; with variables, one change updates all usages.
- If your theme/builder has no custom-font upload, use a custom-font plugin from the WordPress repository.
- Re-run the waterfall to confirm Google font requests are gone.
Caveat: Conversion tool behavior varies by font; test variable fonts specifically.
Caveat: Exact custom-font UI differs by theme/builder — verify.

Tags: resource-optimization, fonts, woff2, wordpress, page-speed, third-party
Source: WordPress Speed Optimization_ Improve Your Website Performance & Make It Faster (Step-By-Step).docx

---

## Verify Caching and Compression via Response Headers
Use when: Checking whether your host's caching and compression are enabled, or verifying after you turn them on.
- Open DevTools, go to the Network tab, and enable 'Preserve log'.
- Reload the page (no throttling needed) and select the first/primary document request.
- Inspect the response headers.
- For caching enabled, look for a cache-related header such as x-cache: hit (not cache-control, which may say no-cache, must-revalidate).
- For compression enabled, look for content-encoding: gzip (or whatever encoding method your host uses).
- To re-verify caching/compression after enabling them, test in an incognito window with 'Disable cache' unchecked so you don't read from browser memory.
Caveat: Header names depend on the host/cache stack; x-cache is an example, not universal.
Caveat: Presenter calls caching/compression a band-aid if fundamentals aren't fixed first — do the content and asset work before relying on them.

Tags: caching, compression, performance-testing, chromedevtools, gzip, page-speed
Source: WordPress Speed Optimization_ Improve Your Website Performance & Make It Faster (Step-By-Step).docx

---

## Sequence WordPress Speed Work: Fundamentals Before Caching
Use when: Planning a speed project for a storefront or landing page and deciding what to prioritize.
- Start with image loading attributes: eager above the fold, lazy below.
- Add explicit width/height to above-fold images to kill CLS.
- Optimize and resize image files with AVIF or WebP.
- Unload unnecessary scripts/styles on the page, including jQuery if unused.
- Remove unneeded WordPress bloat (emojis, Gutenberg block CSS, etc.).
- Self-host Google Fonts as WOFF2.
- Only then enable caching and compression, and optionally add a CDN as a bonus.
- Re-test perceived performance on slow 4G after each stage so you can attribute improvements.
Caveat: Presenter states these fixes delivered strong gains with no compression, caching, or CDN enabled — a demonstrated case, not a promise for every site.
Caveat: 'Your mileage may vary depending on your site builder and hosting' — the source explicitly says this.

Tags: page-speed, resource-optimization, caching, compression, cdn, wordpress, prioritization
Source: WordPress Speed Optimization_ Improve Your Website Performance & Make It Faster (Step-By-Step).docx

---

## Interpret Waffling Speed Test Scores and Average Runs
Use when: Compiling speed data for a decision or report and deciding whether your score is trustworthy.
- Run the same test multiple times; scores can move up or down between runs even without changes.
- Average the results when gathering data for a report or comparison.
- Cross-reference across tools (PageSpeed Insights, GTmetrix, Gift of Speed) rather than relying on one.
- Weight real-user perceived experience (slow-4G DevTools test) above any single score.
- Expect lab tools to re-test in different conditions, so a single lower score after a change isn't necessarily a regression.
Caveat: Presenter notes scores are not the best performance measure; this is a source opinion.
Caveat: Tool interfaces and scoring change over time — verify current behavior.

Tags: performance-testing, measurement, core-web-vitals, pagespeed-insights, gtmetrix
Source: WordPress Speed Optimization_ Improve Your Website Performance & Make It Faster (Step-By-Step).docx

---

## Apply the WordPress Speed Optimization Checklist
Use when: Running a structured speed pass on any WordPress storefront or landing page.
- Set below-fold images to lazy loading and ensure above-fold images are not lazy loaded.
- Add fixed width and height to above-fold images to eliminate CLS.
- Optimize and resize images, converting to AVIF or another modern format like WebP.
- Unload unnecessary scripts and styles on the page, including jQuery if not needed.
- Remove as much unneeded WordPress bloat (emojis, Gutenberg block CSS) as possible.
- Load Google Fonts locally.
- Ensure caching and compression are enabled.
- Optionally add a CDN for further speed.
- Re-test with slow-4G throttling and cache disabled to confirm the perceived-experience gain.
Caveat: Results depend on builder and hosting; the source says to expect YMMV.
Caveat: Verify plugin names and interfaces against current versions.

Tags: page-speed, resource-optimization, checklist, core-web-vitals, wordpress, caching
Source: WordPress Speed Optimization_ Improve Your Website Performance & Make It Faster (Step-By-Step).docx

---

## Compare Optimized vs Unoptimized Page Under Throttling
Use when: Validating that a speed optimization effort actually changed the real loading experience, not just a lab score.
- Open an incognito window (so memory cache doesn't hide the effect) and set throttling to slow 4G.
- Load the unoptimized version first and note layout shifts and slow image reveal.
- Load the optimized version and compare how quickly content becomes usable and whether layout is stable.
- Note that global changes (local fonts, removing bloat) carry over to the non-optimized copy, so the comparison isolates page-specific work.
- Then uncheck 'Disable cache' and reload to see the more typical cached experience, which the presenter finds near-instant.
Caveat: Global optimizations persist across pages and can blur the before/after comparison.
Caveat: Cache-disabled testing is a worst case, not typical visitor experience.

Tags: performance-testing, perceived-performance, chromedevtools, core-web-vitals, measurement
Source: WordPress Speed Optimization_ Improve Your Website Performance & Make It Faster (Step-By-Step).docx

---

## Do Not Lazy-Load Background Images; Optimize Them Instead
Use when: Tuning a hero or section background image that must cover an area but is slowing the page.
- Recognize that the loading="lazy"/"eager" attribute only applies to <img> elements, not CSS background images.
- For background images that must cover a section, keep their large dimensions (do not shrink the intrinsic size).
- Still convert them to AVIF (or WebP) to gain file-size savings while retaining coverage.
- If measuring CLS, absolutely-positioned background images generally do not contribute, but the presenter still adds width/height as good practice.
- Re-test to confirm the background image no longer dominates load time.
Caveat: Background coverage constraints limit how much you can resize; format conversion is the main lever.
Caveat: Verify your builder exposes the format/lazy controls you need.

Tags: images, avif, background-images, resource-optimization, landing-page, hero
Source: WordPress Speed Optimization_ Improve Your Website Performance & Make It Faster (Step-By-Step).docx

---

## Resize Images to 2x Rendered Size for Retina
Use when: Selecting export dimensions when optimizing product photos, hero images, or gallery images for a storefront.
- Read the image's rendered size in DevTools (hover the source URL), e.g. 398x597 px.
- Multiply both dimensions by 2 to get the export target, e.g. 796x1194 px.
- Export at that size in AVIF, keeping the aspect ratio (editors auto-adjust height when you set width).
- Do not export at the raw rendered size — retina/high-density screens would look soft.
- Do not keep the original oversized intrinsic dimensions — that wastes bytes for no visible gain.
Caveat: Presenter's 2x rule is a practical heuristic, not a formal standard; higher-density displays may still benefit from more.
Caveat: Does not apply to background images that must cover a section.

Tags: images, retina, avif, resource-optimization, product-page, hero
Source: WordPress Speed Optimization_ Improve Your Website Performance & Make It Faster (Step-By-Step).docx

---

## Add Alt Text and Preserve It When Copying Image Settings
Use when: Standardizing image accessibility and SEO metadata while optimizing page images.
- While swapping in optimized images, add descriptive alt text for every meaningful image.
- Use an empty alt attribute for decorative images (e.g. a glow behind a hero).
- When using a builder's 'Copy settings'/'Paste settings' to apply loading and dimension attributes across many images, note that alt text can be overwritten.
- After pasting, re-add any alt text that was lost.
- Recognize that alt text supports accessibility and the presenter observes it also nudges PageSpeed scores, so it's a low-cost addition during the same pass.
Caveat: Keep decorative and meaningful images distinct — meaningful images need descriptive alt, decorative ones get empty alt.
Caveat: Copy/paste behavior is tool-specific; verify in your builder.

Tags: accessibility, alt-text, images, wordpress, resource-optimization, seo
Source: WordPress Speed Optimization_ Improve Your Website Performance & Make It Faster (Step-By-Step).docx