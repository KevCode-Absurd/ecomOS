# SEO Full Course 2026: SEO Tutorial For Beginners

source_id: 1IWFC4QSSWOZNNwhdkHBK2d6krCryMQml | folder: /15-SEO-search | cards: 114 | words: 62,552 | type: course transcript (YouTube, screen-share walkthrough)

credibility: Simplilearn training video. Presenter is an unnamed instructor with an Indian-English accent; the transcript is auto-generated speech-to-text and contains many mangled words ("onpage," "computer" for "competitor," "S3/S4" for H3/H4, "trafect," "period" for possibly "Domain Rating"). No credentials, agency name or personal results are given for the presenter. Evidence throughout is screen-share demonstrations on a handful of real small-business sites (an insurance-lead site "dancestudioinsurance.com," "martial arts school insurance," an unnamed skincare/haircare ecommerce site referred to as "Paul Labriq" or "paulabq.com," a power-cord ecommerce site "americancord.com") plus generic textbook-style claims with no citation ("Google uses more than 200 ranking factors," "70-80% of sales come from mobile," "50% of product searches start on Amazon"). The course opens with a sponsored pitch for a paid "AI-powered digital marketing certificate" from an affiliated school, offering free Meta/Google ad credits — this is a course upsell, not SEO content, and is excluded from the substance below. This is a generalist, beginner-level marketing course, not an ecommerce-specialist source; it borrows ecommerce examples (Shopify backend, GA4 ecommerce events, PDP structure) but most of its material (directories, YouTube SEO, ASO, generic content types) is channel-agnostic.

date signals: Presenter says "in 2026." Source file modified 20 Sep 2026. Some content is clearly outdated regardless of the stated year: the course still teaches Adobe Flash as a live concern (Flash was discontinued across all browsers in Dec 2020) and still teaches FID (First Input Delay) as a Core Web Vital (Google replaced FID with INP — Interaction to Next Paint — as an official Core Web Vital in March 2024). The course also still frames the `priority` attribute in XML sitemaps as meaningful, a signal Google has publicly said it mostly ignores. Treat any platform-UI step, tool screenshot, or "current" ranking-factor count as stale until re-checked — this is the single biggest freshness risk in this source.

## 1. What this source is for

This is a beginner's tour of the whole SEO discipline: how search engines work, on-page/off-page/technical SEO, keyword research, link building, local SEO, and — its strongest section by far — hands-on measurement setup (GA4, Google Search Console, Google Tag Manager) and a worked technical SEO audit (Ahrefs). Use it to onboard someone with zero SEO background, to get a checklist of on-page and technical factors to audit, and, especially, to get concrete, reusable step-by-step procedures for wiring up ecommerce tracking (add-to-cart/checkout/purchase events) and running a technical site audit without needing a developer for every fix. It is weak on: modern keyword-research nuance, current schema/rich-result rules, link-building ethics/risk (some described tactics are explicitly against Google's guidelines), and anything tied to a specific tool UI, all of which have moved on since this was recorded.

## 2. Principles

1. **Search is a three-stage pipeline: crawl, index, rank.** Crawlers (Googlebot, Bingbot, Yahoo's Slurp — verify current bot names) fetch pages; indexing stores them against relevant topics; ranking displays results by relevance and authority. A problem in an earlier stage blocks everything after it — a page that isn't crawled can't be indexed, and a page that isn't indexed can't rank. [4d7e19f8ea9d, 2a24068d5a43]
2. **SEO reduces paid-ad dependency but does not replace it.** The source frames SEO as free/organic versus paid ads as a separate lever; it explicitly allows for paid spend around demand spikes (its example: a Christmas seasonal push) even for a site with strong organic performance. [5437c6f5b94e]
3. **SEO has no guaranteed timeline.** Results depend on the site's starting authority, competitor activity and algorithm changes; the source refuses to promise a ranking date and instead frames progress as directional (month-over-month traffic deltas), using an illustrative jump from ~1,000 to ~12,000-15,000 sessions over roughly six months as an example, not a benchmark. [5437c6f5b94e]
4. **Only benchmark against competitors that outrank you, not the whole category.** The source's rule: identify core competitors selling the literal same product, then only study those actually ranking above you — competitors below you don't contain useful gaps. [30500e1bfd7e]
5. **Content is described as "king" repeatedly (5+ times) across the transcript.** No amount of technical setup compensates for weak, irrelevant or thin content; the source ties bounce rate, low traffic and poor rankings back to content quality more than to any other single cause. [42f6cdb74b3b, ece6a69ffd62]
6. **Reject black-hat tactics: keyword stuffing, cloaking, sneaky redirects, poor-quality content.** The source claims Google detects these within "one or two months" (unsourced) and penalizes the site's credibility. [cf1b90a9f8f8, 3f1fe6e32954]
7. **Grey-hat tactics (buying expired domains, buying relevant links, buying reviews) are treated as risky, not endorsed.** The presenter states a personal preference for white-hat only; buying reviews is explicitly called bad practice versus genuine reviews with real images. [cf1b90a9f8f8] Note: several of the link-building tactics later in the source (buying guest-post links, directory submission, incentivized/reciprocal links) sit closer to grey- or black-hat by current Google guidelines than the source itself admits — see Section 9.
8. **Algorithms and search behavior keep shifting; treat this as a standing constraint, not a one-time fix.** The smartphone-vs-keypad-phone and EV-vs-petrol-car analogies illustrate how entire product categories and the language people search with can move over years. [cd2dd5a72828]
9. **Split SEO into three workstreams: on-page, off-page, technical.** On-page = everything done directly on the page (titles, content, keywords, structure, speed); off-page = link building and third-party promotion; technical = sitemaps, schema, robots.txt, crawl/index infrastructure. [a5e95b5877f2]
10. **Good site architecture and UX are treated as ranking-adjacent, not just conversion-adjacent.** Clear navigation, consistent typography, one H1 per page, and internal linking are framed as helping both crawlers and shoppers. [ece6a69ffd62, b1cc7860ad7d]
11. **User-experience quality (eye-tracking / F-pattern scanning) should shape page layout.** Users scan horizontally in short bands rather than reading fully; the source's advice is to put product name, price, logo and the query's answer in the first visible band. [3ddb50cffb54, 6468710f6f02]
12. **Query intent has three buckets — informational, navigational, transactional — and page format should match intent.** A blog post ranking for a transactional term usually fails to convert; a bare product page ranking for an informational term usually bounces. [cdfba6f37765]
13. **Branded (navigational) search performance is reputation management, not a generic keyword problem.** A brand should hold the #1 organic slot for its own name; losing that slot to a third party is treated as a brand/reputation issue. [a7537cfd6597]
14. **Ecommerce-specific: search engines are also compared against Amazon as a rival "search engine" for product discovery.** The source states roughly 50% of product searches start on Amazon (unsourced) and that Amazon/Flipkart-style marketplaces take a large share of first-page ecommerce results — implying a realistic SEO strategy for most stores targets the tier below the dominant marketplaces, not head-to-head competition with them. [9456f3ecb153, 1bae7bf49f42, 2913525fbe2e] This is one of the source's few genuinely ecommerce-specific insights.
15. **Wrong-audience targeting shows up as one of three signals**: no traffic at all (topic/keyword misalignment), traffic that doesn't convert (visitors arrive but aren't real buyers), or traffic that bounces because the page doesn't match what the query implied (course example: content about an older product version ranking for a newer-version query). [161352fce48c]
16. **Original, current content is the stated defense against ranking decay**, especially where manufacturer-supplied descriptions are identical across competing sellers — write copy that adds information the manufacturer sheet doesn't have, and refresh year-specific titles ("Top SEO Tactics 2025" → "...2026") as time passes. [59f3b87a9465]
17. **AI-generated content used verbatim, without added value, is claimed to be recognized and devalued by Google.** The source's own advice: use ChatGPT/AI for reference or ideas, not as final published copy. [4c3f55273a76, 59f3b87a9465] This is a notable in-source caution given the course itself repeatedly uses ChatGPT to "fix" code and content live.
18. **Personalization and localization should shape store content and offers**: personalization uses a shopper's own captured details (name, address, prior behavior); localization delivers the right message/offer to the right region (near-me keywords, multilingual support, region-specific promotions). [9f38dfbf4f52]
19. **Mobile is the primary storefront design target, not an afterthought.** The source states 70-80% of sales come from mobile (its own estimate, unsourced) and that PageSpeed, responsiveness and UX should be designed and audited mobile-first. [684253d7bab8, 1d5f63c6c8b4]
20. **Pogo-sticking (clicking a result, not finding the answer, and returning to click a different result) is treated as a relevance signal Google reads against your page.** The fix is to answer the query's intent directly in the opening headline/above-fold copy, not several screens down. [6468710f6f02]
21. **Understand how search engines are described as evaluating ecommerce specifically**: response speed first, then cross-engine differences (Google/Bing/Yahoo can rank different retailers for the same query), then click/eye-tracking behavior (a clicked result that turns out broken gets pushed down over time), then brand strength (well-known brands get preferential first-page treatment). [9456f3ecb153]
22. **Directories, listings and citations should be judged by relevance, niche fit, cost/authority and geography** — not chased for volume. The source's own example: prefer Amazon/Flipkart-authorized listings over unknown cheap directories. [9fac54461fc4]

## 3. Procedures

### 3.1 Install GA4 (full setup, step by step) [63d26551705b, 88f4ed4866f4]
1. Sign in to Google Analytics with a Google account; open Admin (gear icon, bottom left).
2. Account column > Create > name the account (e.g. matching the brand/store) > Next.
3. Property details: property name, reporting time zone, **currency — set this correctly now if the store is ecommerce**, since ecommerce revenue reporting depends on it. [verify UI]
4. Business details: industry category and business size (course notes "Marketing" wasn't an available category; picked the nearest fit — treat categories as cosmetic/formality).
5. Business objectives: select every objective that genuinely applies (generate leads, drive sales, understand traffic, engagement/retention) — the course warns some flows will silently uncheck others if you pick a mutually-exclusive option, so check carefully. [verify UI]
6. Accept Terms of Service; choose platform = **Web**; enter the website URL (must include https://) and a stream name; click Create and continue.
7. GA4 will show "No data received in past 48 hours" until the tag is installed — expected, not an error.
8. Open "View tag instructions" > choose **Install manually** (or the native CMS/website-builder option if supported) > copy the provided Google tag script.
9. Paste the script into the site's `<head>` section on every page template. **Do not install more than one GA4 tag per page** (duplicate tags cause double counting).
10. Verify: use the "Test" button in the setup wizard; check Reports > Realtime overview for your own visit; or view-source (Ctrl+U) and Ctrl+F for the measurement ID string to confirm the tag is actually live on the page. [verify UI]
- **Hard limitation to communicate to stakeholders**: GA4 cannot show data from before the tag was installed — there is no historical backfill. Plan measurement setup before a launch, not after. [88f4ed4866f4]

### 3.2 Install Google Search Console (GSC) for a store property [c0017f6a1d90, aab362a7a74277]
1. Sign in to GSC with the Google account that will keep managing the property.
2. Property dropdown > Add property. Choose between **Domain property** (covers all subdomains/protocols/www variants) and **URL-prefix property** (one exact URL). The source recommends URL-prefix with the exact https/www variant the site actually serves, calling GSC "sensitive" to URL mismatches (unlike GA4, which it calls more forgiving). **This is a debatable recommendation** — Domain properties are the more commonly recommended, comprehensive option in current Google guidance; verify current best practice before following the source's preference. [web check: Domain vs URL-prefix property recommendation]
3. Enter the exact URL, click Continue. If GA4 is already verified on the same account, GSC may auto-verify.
4. If not auto-verified: Settings > Ownership verification > HTML tag method — copy the one-line meta tag, paste into the site's `<head>` (before `</head>`), save, then click Verify in GSC. [verify UI]
5. Once verified: submit the XML sitemap (append `/sitemap.xml` to the domain and enter that path in GSC's Sitemaps section); confirm the "submitted successfully" message.

### 3.3 Install Google Tag Manager (GTM) and deploy GA4 through it [d0575f65e6d3]
1. Sign in to GTM, click Create Account; enter account name and country.
2. Container name = the bare domain (no `https://`, must not start with a dash — the course hit this error live); Target platform = **Web**; Create; accept terms.
3. GTM gives **two snippets**: one for `<head>` (as high as possible), one for immediately after the opening `<body>` tag. **Both must be installed** — this is different from GA4's single tag.
4. Paste both; watch for CMS-specific escaping issues (the course hit an `&` needing to be `&amp;` on Blogger — a similar issue can occur on other templating systems). [verify UI]
5. To fire GA4 through GTM instead of installing it directly: Variables > User-Defined Variables > New > type **Constant** > name it (e.g. "GA4 Measurement ID") > paste the GA4 Measurement ID (cross-check this against GA4 Admin > Data Streams to avoid a stale/mistyped ID) > Save.
6. Tags > New > name it > Tag Configuration > **Google Tag / GA4 Configuration** > Tag ID = reference the constant variable (via the variable picker, not typed manually) > Trigger = **All Pages – Page View** > Save.
7. **Submit > Publish** the container — nothing fires live until published; this is a step the course explicitly flags people forget.
8. Verify with **GTM Preview mode** (connect to the live URL, confirm the tag fires in the debug panel) — the course found the standalone "Tag Assistant" Chrome extension unreliable, so treat Preview mode plus view-source confirmation as the trustworthy verification path over the extension alone. [verify UI]
9. GSC still needs its own separate verification tag — GTM does not replace Search Console's verification. [cd191b374d2e]

### 3.4 Track Add-to-Cart / Checkout / Purchase button clicks via GTM, without touching site code [7234716f3e22, 59a0144c8001, ca8c688676278]
This is the source's single most concrete, most ecommerce-specific procedure — a code-free way to instrument a standard ecommerce funnel.
1. In GTM, open **Preview mode** on the target product page. Confirm the GA4 configuration tag is already firing.
2. Click the button you want to track (e.g. Add to Cart). In the debug panel's event log, open the resulting "Click" entry and inspect its **Variables** tab to find the exact **Click Text** value (e.g. literally "Add to Cart"). This is the identifier you'll match on.
3. Create a new Tag: Tag Configuration > **Google Analytics: GA4 Event**. Set the Measurement ID (verify against GA4 Admin > Data Streams). Set a GA event name, e.g. `add_to_cart`.
4. Create a matching Trigger: type **Click – All Elements** (or "Some Clicks"), condition **Click Text equals "Add to Cart"** (paste the exact text captured in step 2, no quotation marks).
5. Save; **Submit > Publish** the container.
6. Re-verify in Preview mode: click the button again, confirm the new tag fires; then confirm the event appears in GA4 (Realtime, then later in standard event reports).
7. **Repeat the same procedure for Checkout and Purchase/Submit buttons**, each with its own click-text trigger, to build a full add-to-cart → checkout → purchase funnel visible in GA4 purely through GTM.
- Caveats from the cards, worth carrying into execution: this tracks **clicks on visible button text**, so it breaks if the button label changes (localization, A/B tests, dynamic labels) — a unique element ID or CSS selector is more robust than text-matching long-term. It only confirms a click happened, not that the cart was actually updated server-side. Delete or disable old test tags before publishing to avoid double-counting. [59a0144c8001]

### 3.5 Read the add-to-cart → checkout → purchase funnel once instrumented [ca8c688676278, 7b56f452ec2a]
1. In GA4, Reports > Engagement > Events (or an Exploration/Funnel report), locate `add_to_cart`, `begin_checkout`, `purchase` (and `form_submit` for non-ecommerce actions).
2. Set the date range; enable Compare against the previous period or previous year.
3. Add a breakdown dimension "Session default channel group" to isolate Organic Search from other channels if you want SEO's contribution specifically.
4. Read the pattern, not single numbers. The source's own illustrative example: add-to-cart fell 25%, begin_checkout fell 27%, but purchase rose (152 → 395) — attributed in the source to a prior period's payment/technical failure rather than a genuine conversion gain. **Don't read one metric in isolation; investigate anomalies before concluding causation.**
5. Where a mid-funnel step collapses sharply relative to the step before it (the source's own funnel-reading example: 100 add-to-cart → 60 checkout → 10 purchase, illustrative numbers only, not a benchmark ratio), investigate payment options, form friction, shipping-cost surprises or forced account creation at that specific step before touching content or keywords.

### 3.6 Bounce-rate triage across a site (find and fix high-bounce pages) [9345e5130d85, 31b0c4a879ee]
1. GA4: Reports > Acquisition > Traffic acquisition. Add secondary dimension "Page path and screen class."
2. Sort by bounce rate descending.
3. **Exclude checkout/order-confirmation/gift-card pages from the review — 100% bounce there is normal** (single-visit endpoint pages) and not worth "optimizing."
4. Look past that noise for pages at 50%+ bounce. Audit each: is the content old/thin (the source's own example was a 2018 blog post with no FAQ), does it match competitor depth on the same query, does it answer the query it ranks for?
5. Export the full table to a spreadsheet; sort and filter systematically rather than eyeballing the live report.
6. Repeat without the organic-channel filter to catch pages also failing in paid/social traffic.
7. Re-check bounce rate on fixed pages after a defined rewrite window to confirm improvement.

### 3.7 Find declining pages via period-over-period export (traffic-drop detection) [1c1b6e9f3e7b, 5895232c1ead]
Applies identically in GA4 (Acquisition > Traffic acquisition, page dimension) and GSC (Performance report, Pages tab).
1. Pull the page-level metric table (Active Users in GA4; Clicks/Impressions in GSC) for the current period and a prior comparison period.
2. Export both to a spreadsheet; align rows by page path, current-period and prior-period columns side by side.
3. Add a difference column (e.g. `=C2-Z2`); sort descending/ascending on that column to surface the biggest gainers/losers.
4. Ignore non-commercial noise rows (account/login pages) that aren't real SEO or content targets.
5. In GSC specifically, do this one metric at a time (clicks, then impressions, then average CTR) rather than conflating them — the source's own example showed impressions and clicks both falling while average position simultaneously *improved* (17.8 → 12.7), illustrating that ranking-position quality and traffic volume can move in opposite directions at once.
6. Repeat monthly as a rolling log rather than a one-off audit.

### 3.8 Find and fix 404s and check indexing coverage in GSC [6387bf5f570f, 38ede763059698, 82c14d6403d3]
1. GSC > Indexing report. Read Indexed vs Not-indexed counts.
2. In "not indexed" reasons, distinguish **intentional exclusions** (dynamic/parameterized URLs with `?`/`=`, pages excluded by noindex — the source says these are typically fine to leave alone) from **genuine 404s** (need fixing).
3. Click into the 404 group, export the URL list.
4. **Redirect each to the nearest topically relevant page** — a specific product's successor model, or the closest collection/category page. Only fall back to the homepage if nothing relevant exists. Never redirect to an unrelated page (the source's explicit warning example: don't redirect an iPhone-model page to a perfume collection).
5. Hand the list to a developer for bulk redirect implementation.
6. Re-crawl / re-check the Indexing report after fixes to confirm the 404 count drops.

### 3.9 Find high-impression, low-click queries and fix them (CTR triage) [b243bdf156ec, 860428181c80]
1. GSC > Search results (Performance). Sort Queries or Pages by Impressions descending.
2. For each high-impression/low-click row, work through three possible causes: (a) the title/meta description isn't compelling relative to what's shown in the SERP — rewrite it; (b) the page ranks outside roughly the top 20, so it accumulates impressions without ever being seen/clicked — prioritize content/links, not just title copy, if position is poor; (c) the page ranks and gets clicked but loads slowly, drives bounce, and (per the source, unconfirmed by Google) gets demoted over time — check page speed.
3. Cross-reference average position for the query: page 2-3 positions → prioritize content/internal links; page 1 with weak CTR → prioritize title/meta and speed.
4. Re-measure the same query set after changes rather than judging impact immediately.

### 3.10 Create and validate schema (structured data) via a generator tool [fa6c5a7abc3d, c88b20d071878]
1. Pick the schema type matching the page: Article/BlogPosting for content, Product (with Offer/Review/AggregateRating) for PDPs, LocalBusiness for store-location pages.
2. Use a schema generator (course demoed **technicalseo.com**) [verify UI] rather than hand-writing JSON-LD. Fill fields from the live page: type, URL, headline, image URL, short description (~155-160 chars), author type/name/URL (leave URL blank if none, or link an About page), publisher name/logo URL, date published, date modified.
3. Paste the generated code into a rich-results/rich-snippet validator; fix any warnings (the course's recurring warning was an invalid date format, "fixed" by pasting the code into ChatGPT and asking it to correct the date field to ISO standard — **validate the AI's output, don't just trust it**).
4. Only after validation, install the code — either directly in the page `<head>` via a developer, or via GTM (see 3.11) if backend access isn't available.
5. Re-validate after any template change, since mismatched product data (price, availability) can break rich-result eligibility.

### 3.11 Deploy page-specific schema via GTM (no theme access needed) [639b2b41168f]
1. GTM > Tags > New > name it descriptively (e.g. "schema code – blog post X").
2. Tag Configuration > **Custom HTML** > paste the validated schema code.
3. Triggering > New > **Page View** trigger, narrowed to **Page Path equals [the specific URL path]** — schema is usually page-specific (a blog post's schema differs from a product page's), so don't fire it on All Pages.
4. Save; **Submit > Publish**.
5. Verify via GTM Preview connected to that specific page (confirm the tag fires), then re-run the schema through a Rich Results Test against the live URL to confirm it's detected. Note: a paused/unpublished tag may still show as "detected" in a validator until Google's next crawl — don't assume instant propagation.

### 3.12 Run a technical SEO site audit (Ahrefs-style, colour-prioritized) [86975c6c2e81, b6d9e2525ff1]
1. Create Project: import from a connected GSC account, or add the domain manually (works without Analytics/verification; sets a crawl frequency, e.g. weekly).
2. Optionally add target keywords and competitor domains to track.
3. Run the crawl; open the Health Score (0-100). **A high score does not mean a clean site** — the source's own example scored 96/100 ("excellent") yet still had fixable Errors.
4. **Work Errors (red) first, then Warnings (yellow):**
   - **404 pages** → redirect to nearest relevant page, or homepage if nothing relevant exists.
   - **Canonical points to redirect** (canonical tag points to a URL that itself redirects) → first check if the canonical target is genuinely broken; if so, correct the canonical tag to point to the actual live, correct URL.
   - **Orphan pages** (no internal links point to them) → add to a menu or interlink from a relevant blog/article.
   - **HTTPS page has an internal link to HTTP** → update the internal link to the direct https:// version, skip the redirect hop.
   - **Page has links to a broken page** → same fix class as 404 handling.
   - **Image file too large** → compress via developer.
   - **Nofollow pages** → some are benign/intentional (e.g. a redirecting internal offer link); don't blanket-fix every nofollow flag.
   - **Meta description too long/short** → target ~140-160 characters, 160 hard max; count characters, not words. Fix directly in the CMS (e.g. Shopify: Products > Collections, or Content > Blog posts).
   - **Title tag too long** → target **~60 characters max** (this is the figure that matches current standard practice; see Section 9 for the source's internal contradiction on title length).
   - **Missing alt text** → write concise (3-4 words max) descriptive alt text matching the image's actual subject; template-level images (footer/header) need a developer since they're global.
5. Hand the exported error/warning lists to a developer for the fixes that require backend access.

### 3.13 Keyword research workflow (volume + difficulty + intent + relevance) [017caafa9aba, 87e5562eb673, 16bdb59b661a, 010063066fd9]
1. Enter a seed keyword into a keyword tool (course demoed Ubersuggest, Google Keyword Planner, and Ahrefs) with your actual target location.
2. Sort/filter candidates by **volume descending, then apply a difficulty filter (course used KD 0-40 as a "first phase" range)** to surface realistically rankable terms for a new/lower-authority site.
3. Exclude terms outside your real service area or catalog fit (don't target "Miami SEO agency" if you don't serve Miami; don't chase a competitor's keyword for a product you don't sell).
4. Check each candidate's **intent label** (informational/navigational/transactional/commercial — some tools multi-tag) and match it to the page type you'll build. A "what is the best SEO software"-style query can be informational-phrased but carry commercial intent.
5. Before committing, inspect the actual SERP for the keyword: who ranks (high-DA sites, AI Overview, People Also Ask), whether the term is realistically winnable, and what page depth/format is already winning.
6. Mine the tool's **long-tail and question suggestions** ("skin cream for dry skin," "what face cream is best") to shape content headings/FAQ copy that genuinely answers real phrasing.
7. Re-run this after catalog or content changes, since volume/difficulty/rankings shift.

### 3.14 Keyword gap analysis against a competitor [44c8a0dfa87815, cf900456ba0ea]
1. Pull your own backlink/keyword profile and a chosen competitor's, in the same tool (numbers won't match across tools — see Section 9).
2. Read "common keywords" vs "competitor's total keywords"; the difference is the approximate gap of keywords they rank for and you don't.
3. **Hard filter: only pursue gap keywords that describe products/services you genuinely offer** — never chase a competitor's keyword just because they rank for it.
4. Drill into specific gap terms to see what the competitor's ranking page actually does (structure, depth, offers) before building your own version.

### 3.15 Backlink audit and spam/disavow decision [e592af67a06c, fe47b8b67efdab, ade5208b890b]
1. Sort the backlink report by Domain Rating (DR) ascending and descending. A DR-zero referring domain isn't automatically bad (could just be a new site) — use judgment, not an automatic removal rule.
2. Check each suspicious domain's spam score via a spam-score checker (course used Moz): **under 5/100 = fine; 10+ = starts to be risky; the course's own practical action threshold is roughly 10-30%+ = consider disavowing.**
3. Check geographic/audience relevance of the linking domain (a US store getting most links from an unrelated region is a weak-value signal, though not automatically toxic).
4. **Most sites do not need to disavow anything.** Per the cards' explicit correction to the source: investigate via GSC Manual Actions and link-scheme history first; third-party toxicity scores alone are not grounds for removal. Reserve disavow for considerable manipulative links tied to an actual or likely manual action, per Google's current instructions. [fe47b8b67efdab] — this is a stronger, more current caution than the raw transcript gives, and should be followed over the transcript's more casual "just disavow anything with a bad score" framing.
5. If disavowing: compile spam domains/URLs into a plain-text file (one per line) and submit via GSC's Disavow Links tool (requires GSC verified on the domain).

### 3.16 Off-page link building tactics (as the source describes them — see Section 9 for risk caveats) [f2d9c44191c1, 5ad59b6f29ec, a3d1dead77d7, b55f760c2d9e, 3ac30aa3629d]
1. **Broken-link building**: find broken external links relevant to your niche; ask the site admin to fix/replace with a link to your equivalent content.
2. **Resource-page / guest-post prospecting**: search operators like `[niche] + write for us` or `[niche] + guest post`; check submission guidelines (word count, format); note some placements charge a fee (course example: ~$50-60, treat as dated/illustrative). Write original, structured content with a contextual, relevant anchor-text link back.
3. **Directory submission**: pre-filter to a small number of high-authority, relevant directories; fill title/URL/description/category accurately; leave reciprocal-link fields blank unless genuinely reciprocal. The source itself calls mass submission poor practice.
4. **Content syndication**: republish/promote on platforms like Reddit, Medium, Flipboard, keeping the original canonical on one site and customizing the framing elsewhere to avoid duplicate-content risk (this directly conflicts with the source's own Panda-recovery advice against duplicate "content forms" — see Section 9).
5. **Incentive-based/reciprocal links**: only with partners of genuine relevant authority (good DA, low spam score, fast site); pair with an editorial-quality placement, not a bare swap. The source's own explicit warning: partners can delete the link later or start demanding payment, and this pattern is recognizable/riskier than it looks.
6. **Social promotion as a link vehicle**: short posts (2-3 lines) with the target keyword and the actual link (not just a brand mention) as a clear CTA; HD imagery; shortened URLs (Bitly).

### 3.17 Google Business Profile setup for local SEO [b9c13080c7d1]
1. Start a Google Business Profile; enter business category matching how customers search.
2. Indicate whether customers can visit a physical location (Yes/No); if yes, enter street/city/pincode/state, place the map pin, confirm.
3. Indicate delivery/in-person visit options; enter phone number.
4. Choose verification method (video, or "verify later" — profile is not visible until verified).
5. Add services offered; set business hours (or 24 hours); write an About/description; add photos (optional).
6. Once verified, the listing appears in the local pack/Maps/mobile search with NAP (Name, Address, Phone — must be consistent across every citation) and services.

### 3.18 Robots.txt configuration [f94ce42ad17a, 153492ce5eeb, 8c1e01fcf839]
1. Identify pages that must stay crawlable (product/service, category, blog, About) vs. paths to block (CMS admin, internal search results, low-value tag/category archives).
2. Configure via the CMS's native option where available (Yoast for WordPress; Magento has its own admin field) rather than hand-editing where a plugin exists.
3. Confirm the live file at `yourdomain.com/robots.txt`. Typical WordPress pattern: block `/wp-admin/` but allow `admin-ajax.php` (blocking that endpoint can break front-end functions).
4. **Reference the sitemap URL inside robots.txt** (a `Sitemap:` line) so crawlers can discover it from that file too.
5. Remember: robots.txt controls *crawling*, not *indexing* — a blocked URL can still appear in results if linked elsewhere; pair with a noindex tag where true removal from the index is the goal.

### 3.19 Sitemap creation and submission [3af48b4346f4, e1b09c7773f5, 0dc5d1a90cf4, d6f2fb640d55]
1. **Check whether one already exists** (append `/sitemap.xml`, or check the CMS's SEO plugin/app — modern CMS platforms like Shopify and WordPress with RankMath/Yoast generate sitemaps automatically; the actual URL can vary, e.g. RankMath serves `/sitemap_index.xml`, not literally `/sitemap.xml`). [verify UI]
2. Confirm it exposes the URL types you need indexed (product, collection, blog).
3. Only if genuinely absent, use a generator (e.g. sitemapgenerator.com) to produce an XML file (preferred format over HTML/RSS for search engines).
4. Submit the sitemap path in GSC; reference it in robots.txt.
5. **XML sitemap matters for SEO; HTML sitemap is optional** — it's for human navigation only and its absence is not an SEO problem.
6. Re-check after large catalog changes (bulk new products/categories), since new URLs aren't auto-submitted.

## 4. Rules, thresholds and numbers

| Rule / setting | Number or threshold | Condition | Source's basis | Card id |
|---|---|---|---|---|
| Meta description length | ~150-160 chars (best ~155-160), 160 hard max before truncation | All pages | Presenter's stated rule, repeated consistently | 28b89b50c0e9 |
| Title tag length (LATER, contradicts earlier claim) | ~60 characters max | On-page audit fix | Presenter's later stated rule (matches current industry norm) | 786a486134927 |
| Title tag length (EARLIER, conflicting claim) | 150-160 characters | Early on-page section | Presenter's earlier stated rule (does not match current norm) | 739d693029a4 (card corrects this to "no fixed limit; write for display") |
| Page load time target | ~1-2 seconds ideal; "under 3-4 sec" stated elsewhere as acceptable max | Technical SEO / bounce reduction | Presenter's guideline, restated 3+ different ways across the transcript (internally inconsistent — see Section 9) | 877d742162c1, 2aca699ba689, 1d5f63c6c8b4 |
| PageSpeed Insights score bands | 0-49 red/poor; 90-100 green/good | Reading a PageSpeed/CWV score | Tool's own color-coding, confirmed by presenter | 1d5f63c6c8b4 |
| Mobile post-click page load / bounce stat | ~22 sec typical load observed across 900K+ ads; >50% of visitors leave past 3 sec; each extra second loses more visitors | Cited as "Google researchers" study, not otherwise sourced in transcript | Unattributed citation in the course | 1d5f63c6c8b4 |
| Minimum keyword search volume floor | ~500 searches/month | Keyword selection (Ubersuggest demo) | Presenter's own heuristic — cards explicitly say do not impose this on every store; judge by commercial value | 017caafa9aba |
| Keyword difficulty "good" threshold | Under ~40/100 | Keyword selection (Ubersuggest/Ahrefs) | Presenter's own heuristic | 017caafa9aba, 87e5562eb673 |
| Domain Authority minimum for a "worthwhile" link | ~30-40 | Link-building decision | Presenter's own heuristic, not a Google metric | 6e87a52bb240 |
| Backlink spam score | Under 5/100 = fine; 10+ = risky; ~10-30+ = consider disavow | Backlink audit (Moz spam score) | Presenter's own bands, not a Google-published standard | e592af67a06c |
| Site-needs-a-sitemap page-count rule | "500+ pages" | Sitemap decision | Presenter's own arbitrary cutoff; cards note there's no supported general rule beyond this | e1b09c7773f5 |
| Alt text length | Max 3-4 words | Image alt text | Presenter's own style rule | 6cd7c100722a |
| Dwell time as a "good" signal | ~2-5 minutes | Reading engagement/behavior signals | Presenter's own informal rule of thumb, not an official Google metric | 01f36de58806 |
| Guest post pricing example | ~$50-60 per placement | Off-page link building | Presenter's one-time example, will vary by site/market | 5ad59b6f29ec |
| Referring domain traffic-by-location "healthy" example | 99.8% traffic from target region | Backlink geo-relevance check | One example the presenter showed, not a hard rule | ade5208b890b |
| Ahrefs Keyword Difficulty filter for a new/low-authority site | KD 0-40 | First-phase keyword targeting | Presenter's own demonstration range, tool-specific | 87e5562eb673, 010063066fd9 |
| Core Web Vitals CLS "poor" threshold | Cited as ">0.25" in one on-screen example | Reading a CWV report | Matches Google's actual published CLS threshold, though the source doesn't lay out the full good/needs-improvement/poor bands explicitly | 37ad8a642ccb |
| Google's stated ranking-factor count | "more than 200" | General SEO framing | Unsourced, widely repeated SEO folklore, not from an official Google statement in-transcript | (no dedicated card; appears in principles context) |

## 5. Diagnostics and checks

- **High impressions, low clicks (GSC).** What to check: sort Queries/Pages by impressions descending. What good looks like: impressions and clicks broadly proportional to position. What bad looks like: very high impressions with near-zero clicks (source examples: 74,000 impressions/175 clicks; 46,000 impressions/6 clicks). What to do next: check average position first (page 2-3 → work on content/links; page 1 → work on title/meta/speed); rewrite title and meta description to better match searcher phrasing and differentiate from competing SERP listings. [b243bdf156ec, 860428181c80]
- **High bounce rate by page (GA4).** What to check: Traffic acquisition + Page path secondary dimension, sorted by bounce rate descending. What good looks like: bounce roughly matching a page's normal type (checkout pages near 100% is fine and expected). What bad looks like: content pages at 50%+ that are old, thin, or lack an FAQ. What to do next: refresh/rewrite the flagged page; re-check after the rewrite window. [9345e5130d85]
- **Wrong-audience targeting.** What to check: (1) total traffic level, (2) visitor-to-customer conversion ratio, (3) landing-page bounce concentrated on pages targeting a mismatched query (e.g. content about an older product version ranking for a newer-version search). What good looks like: traffic converts at a rate consistent with the page's intent bucket. What bad looks like: any of the three signals present in isolation or combination. What to do next: narrow the keyword/content/channel targeting to match the audience that can actually buy; re-check keyword-to-page mapping after the fix. [161352fce48c]
- **Traffic-decline attribution to specific pages.** What to check: Top Pages report, comparing current traffic to a known peak period. What good looks like: traffic loss traceable to specific pages with specific lost/declined keywords. What bad looks like: a page that loads fine (not a 404) but shows zero current traffic despite a tracked ranking position — this typically indicates the page dropped out of a rankable position, not a technical break. What to do next: build a content/link-building fix list keyed to the specific lost keywords per page. [b36fc4bc173f, e3495a592539]
- **Core Web Vitals health (GSC).** What to check: CWV report split by mobile/desktop, drilling into red (Poor) URL groups by specific metric (CLS/LCP/FID — note FID is now superseded by INP, see Section 9). What good looks like: 0 Poor URLs, most URLs "Good." What bad looks like: a large share of URLs flagged Poor or Needs Improvement, especially on mobile. What to do next: pass the specific diagnostic (render-blocking requests, oversized CSS, unused JS, forced reflow) to a developer; re-run after fixes. [37ad8a642ccb]
- **Backlink quality/toxicity.** What to check: DR of each referring domain, spam score via a checker tool, follow/nofollow status, anchor-text relevance, geographic relevance. What good looks like: relevant anchor text, DR appropriate to age/niche, spam score under 5, region-matched traffic. What bad looks like: irrelevant anchor text, spam score 10-30+, dofollow links from clearly unrelated regions/niches. What to do next: investigate via GSC Manual Actions before disavowing anything; reserve disavow for confirmed manipulative-link situations, not just a low third-party score. [e592af67a06c, fe47b8b67efdab]
- **Indexing coverage health (GSC).** What to check: Indexed vs Not-indexed counts, and reasons for exclusion. What good looks like: exclusions are mostly intentional (noindex tags on filter/parameter URLs). What bad looks like: a meaningful count of genuine 404s among excluded URLs. What to do next: export, redirect each to the nearest relevant page, re-check the count drops. [38ede763059698]

## 6. Tools, settings and named features

- **Google Analytics 4 (GA4)** — free, core traffic/behavior/ecommerce-event tracking tool. [verify UI]
- **Google Search Console (GSC)** — free, crawl/index/query-performance tool; also hosts the Disavow Links tool. [verify UI]
- **Google Tag Manager (GTM)** — free, tag-deployment container; used here for GA4 delivery, schema injection and click-based event tracking. [verify UI]
- **Google PageSpeed Insights** — free, page-speed/Core Web Vitals lab-data tool. [verify UI]
- **Ubersuggest** — free-with-paid-tier keyword research tool (volume, difficulty 0-100, CPC, competitor domain overview). [verify UI]
- **Google Keyword Planner** — free, but requires a Google Ads account to access; built for paid campaigns but usable for SEO volume/competition data. [verify UI]
- **Google Trends** — free, relative search-interest-over-time and regional comparison tool. [verify UI]
- **Ahrefs ("HRF")** — paid, deep site-audit/backlink/keyword tool; used extensively in the walkthrough (Domain Rating, Site Audit health score, Keyword Explorer, Organic Keywords, Top Pages, Backlinks). No pricing given; **paid tool, not free**. [verify UI]
- **SEMrush** — paid, comparable all-in-one SEO tool; demoed only on a free/limited account, explicitly shallower than the Ahrefs walkthrough. Traffic/authority numbers differ from Ahrefs for the same site — **the source explicitly warns these tools use different methodologies and are not directly comparable.** [verify UI]
- **Moz / Moz Toolbar** — free browser extension; Domain Authority and spam-score checking. [verify UI]
- **Yoast SEO** (WordPress plugin) — meta tags, sitemap, robots.txt generation for WordPress. [verify UI]
- **RankMath** (WordPress plugin) — alternative SEO plugin; sitemap toggle demoed, serves at `/sitemap_index.xml`. [verify UI]
- **technicalseo.com** — free schema/structured-data code generator, demoed for Article and Product schema. [verify UI]
- **Rich Results Test / "rich snippet checker"** — schema validation tool (Google's own or a similar validator; exact tool name garbled in transcript). [verify UI]
- **sitemapgenerator.com** — free standalone XML/HTML sitemap generator for sites without a CMS-native option. [verify UI]
- **Google Tag Assistant** (Chrome extension) — GTM/tag verification; **the course found it unreliable during its own demo** — prefer GTM Preview mode plus view-source confirmation. [verify UI]
- **Bitly** — URL shortener, used in social-link-sharing tips.
- **Google Business Profile** — free local-listing/map-pack tool.
- **Blogger (blogspot.com)** — free website builder, demoed only as a beginner practice exercise, not a recommended real ecommerce platform.
- **WriteMaps, MindNode, Screaming Frog, Dynomapper** — visual sitemap/site-planning tools named as historically used; the presenter himself calls these largely unnecessary now that CMS platforms auto-generate structure/sitemaps. Treat as low-priority/legacy. [verify UI]
- **Sponsored/affiliate content flag**: the course's opening pitch for an "AI-powered digital marketing certificate" (with free Meta/Google ad credits) from an affiliated school is a paid promotional segment, not SEO instruction — excluded from all substantive sections above.

## 7. Examples and case results

All figures below are single-session illustrations from the presenter's own or client demo accounts, not benchmarks or proven outcomes.
- **GA4 ecommerce funnel example** (unnamed skincare/haircare site, organic channel, one 3-month window vs. prior 3 months): add_to_cart 751 vs. ~1,300 (-25%); form_submit 882 (+30%); begin_checkout 321 vs. 444 (-27%); purchase 395 vs. 152 (higher, attributed to a prior payment/technical issue depressing the earlier period). [7b56f452ec2a]
- **GSC period comparison example** (same or similar site): impressions ~3.39M → ~3M; clicks 19.2K → 15.4K; average position improved 17.8 → 12.7 — illustrating that visibility volume and position quality can move in opposite directions. [5895232c1ead]
- **High-impression/low-click example**: a branded term at ~2,416 impressions; "biologic research" product term at 74,000 impressions/175 clicks; "clarifying shampoo" at 46,000 impressions/6 clicks. [860428181c80]
- **Ahrefs Site Audit example**: Health Score 96/100 ("excellent") yet still carrying red errors (404s, canonical mismatches, orphan pages, oversized images) — illustrates that a high aggregate score does not mean a clean site. [86975c6c2e81]
- **Keyword decline example**: a site's total ranking keyword count fell from a March 2024 peak of ~14,000 to ~3,390 later; a specific page's traffic fell from 2,261 (peak month) to 174 (later). [e3495a592539, b36fc4bc173f]
- **Backlink comparison example**: own site 237 backlinks vs. a competitor's ~1,200 (~5x). [44c8a0dfa87815]
- **Keyword gap example**: 931 common keywords vs. a competitor's 2,953 total (~2,000-keyword gap), including a specific "red light therapy mask" term the competitor ranked for and the client's site did not. [cf900456ba0ea]
- **Funnel drop-off illustration**: 100 add-to-cart → 60 checkout → 10 purchase, used purely to demonstrate how to read a funnel, explicitly not a benchmark ratio. [ca8c688676278]
- **On-page fixes demoed live on real sites**: a meta description trimmed from 167 to 157/155 characters (Shopify backend); a blog post title trimmed from 73 to 54 characters (with a ChatGPT-suggested rewrite); missing alt text added to a footer shipping-badge icon ("fast free shipping") and a data-graphic image ("brand trust 81%"). [786a486134927, 6cd7c100722a]
- **Cross-tool discrepancy example**: the same site showed Ahrefs organic traffic ~4-5K vs. SEMrush ~9.8K, and Ahrefs DR 44 vs. SEMrush Authority Score 35 — presented by the source itself as proof that different tools use different methodologies and should never be compared head-to-head as if equivalent. [b6d9e2525ff1]

## 8. Mistakes the source warns about

- Keyword stuffing, cloaking, sneaky redirects, and thin/spammy content (black-hat basics). [cf1b90a9f8f8]
- Redirecting a 404'd or dead page to an unrelated destination instead of the nearest topically relevant page (explicit example: don't send an iPhone query to a perfume/unrelated collection). [6387bf5f570f]
- Buying reviews instead of collecting genuine ones with real images. [cf1b90a9f8f8]
- Using AI-generated content verbatim without adding real value — the source claims Google recognizes and devalues this. [4c3f55273a76]
- Riding one winning page/ad/keyword and neglecting variety (in content: republishing identical articles across many sites with just a source link — a duplicate-content risk the source itself later contradicts by recommending content syndication on Reddit/Medium/Flipboard; see Section 9). [933f7a1d51d8]
- Targeting a keyword you can't realistically fulfill, or that your product doesn't genuinely match (mismatched claims create bad reviews and lost trust). [30500e1bfd7e]
- Mass, low-quality directory submissions instead of a small number of relevant, authoritative ones. [a3d1dead77d7]
- Pursuing incentive-based/reciprocal link swaps as a primary tactic — the source flags that partners can delete links later or start demanding payment, and that Google explicitly targets paid-link schemes. [3ac30aa3629d]
- Treating a single third-party toxicity/spam score as sufficient grounds to disavow a backlink without checking GSC Manual Actions or actual link-scheme history first. [fe47b8b67efdab]
- Blocking pages you actually need indexed via robots.txt, or assuming robots.txt removes pages from the index (it only controls crawling). [153492ce5eeb]
- Confusing GA4's default ecommerce item-level percentage with the true transaction conversion rate — the source explicitly warns these are not the same metric. [31b0c4a879ee]
- Assuming a single high Site Audit health score means the site has no errors worth fixing. [86975c6c2e81]
- Comparing traffic/authority numbers across different SEO tools (Ahrefs vs. SEMrush) as if they were measuring the same thing. [b6d9e2525ff1]
- Leaving an old/duplicate GTM or GA4 tag active when adding a new one, causing double-counted events. [59a0144c8001]
- Relying on a button's literal text as the sole event-tracking trigger without accounting for future label changes (localization, A/B tests). [59a0144c8001]

## 9. Caveats, conflicts and what is missing

- **Internal contradiction on title tag length.** Early in the transcript, the presenter states title tags should be "150 to 160 characters." Much later, during the Ahrefs audit walkthrough, he fixes a "too long" title by cutting it from 73 to 54 characters and states the limit should be "maximum 60 or under 60 characters." These two claims directly conflict. The ~60-character figure matches current standard SEO practice (title display is pixel-width-limited, and Google may truncate or rewrite titles regardless of character count); the cards themselves correct this to "Google sets no fixed title-element character limit; display depends on available width." **Trust the later ~60-char framing and the cards' correction over the earlier 150-160 claim.** [739d693029a4, 786a486134927]
- **Internal inconsistency on page-speed targets.** Across the transcript the presenter states, at different points: "ideally load under 3 seconds or maximum under 4 seconds," "1-2 seconds," and "less than 1 second, maximum 2 seconds." These are not the same target. The cards consistently converge on "1-2 seconds" as the presenter's dominant framing, with the 3-4 second figure as an outlier — but there is no single number in the source you can cite as "the" target. [877d742162c1, 2aca699ba689, 1d5f63c6c8b4]
- **Outdated technology still taught as current.** The course teaches Adobe Flash as a live SEO concern (crawlers can't index it, it's heavy) — Flash has been fully discontinued across all browsers since December 2020, so this entire subsection is dead/irrelevant for any 2026 site. [e8655b6936971, 8c493a361720] The course also teaches **FID (First Input Delay)** as one of the three Core Web Vitals; Google officially replaced FID with **INP (Interaction to Next Paint)** in March 2024. Any Core Web Vitals guidance in this source should be re-verified against Google's current official metric set. [37ad8a642ccb] [web check: current Core Web Vitals set]
- **Sitemap `priority` attribute treated as meaningful.** The source demonstrates sitemap entries carrying a `priority` value (homepage 1.0, other pages 0.6-0.8) as though Google weighs it. Google has publicly stated for years that it mostly ignores this attribute. [web check: current relevance of sitemap priority/lastmod attributes] [0dc5d1a90cf4]
- **Domain vs. URL-prefix GSC property recommendation is debatable.** The source recommends the URL-prefix property type over Domain property, calling GSC "sensitive" to URL variants. Current common guidance more often favors Domain properties precisely because they cover all variants (http/https, www/non-www, subdomains) under one property. This is worth an explicit web check before standardizing on the source's preference. [c0017f6a1d90]
- **Internal conflict on content syndication vs. duplicate-content risk.** During Google Panda recovery advice, the source explicitly warns against "content forms" — i.e., republishing the same article across multiple sites with just a source-link reference. Later, in the off-page/link-building section, the source recommends content syndication on platforms like Reddit, Medium and Flipboard as a legitimate tactic. These two pieces of guidance are in direct tension; the cards partially resolve this by stressing the original should stay canonical on one site and syndicated copies should be customized/re-framed rather than verbatim — but the source itself does not reconcile the contradiction. [933f7a1d51d8, b55f760c2d9e]
- **Several link-building tactics sit closer to risky/grey-hat than the source's own framing admits.** Buying guest-post placements, incentive-based/reciprocal link exchanges, and mass directory submissions are all presented relatively casually, but current Google guidelines treat unqualified paid links and reciprocal link schemes as against the spirit (and often the letter) of their guidelines unless properly qualified with `rel="sponsored"` or `rel="nofollow"`. The cards add this qualification explicitly in several places; the raw transcript does not. **Follow the cards' qualification, not the transcript's more permissive framing, when actually building links.** [3ac30aa3629d, 5ad59b6f29ec, a3d1dead77d7]
- **Disavow guidance is more cautious in the cards than in the transcript.** The transcript treats spam-score thresholds fairly mechanically (e.g. "under 5 is fine, over 30 disavow"). The cards correctly add that most sites do not need to disavow anything at all, and that disavow should follow evidence of an actual or likely manual action — not just a third-party score. [fe47b8b67efdab]
- **No coverage of E-E-A-T, current Google helpful-content signals, or generative/AI Overview optimization in depth.** The source gestures at "AI is changing search" and shows Ahrefs' AI-citation tracking, but gives no concrete method for optimizing for AI Overviews or answer engines beyond writing to clear intent — this gap should be filled from folder 16-AEO sources, not from this one. [2e6780bee4135]
- **No coverage of international/multi-region technical SEO (hreflang), pagination/faceted-navigation handling for large catalogs, or Core Web Vitals field-data thresholds beyond the vague color bands shown on screen.** These are meaningful gaps for a mature ecommerce catalog and are simply not addressed in this source.
- **Most numeric thresholds throughout are the presenter's own heuristics, not documented Google standards** — the volume floor (500 searches/month), the DA minimum for a link (30-40), the spam-score bands, the dwell-time signal (2-5 minutes), and the "500+ pages needs a sitemap" rule are all presenter opinion presented with course-instructor confidence. Treat every specific number in Section 4 as directional, not authoritative, unless independently verified.
- **[needs brand data: what]** — nearly every procedure in Section 3 needs brand-specific inputs to execute for a real store: the actual GA4/GSC/GTM account and container IDs; the store's actual product catalog and URL structure (to decide what robots.txt should block and what the sitemap should expose); the store's actual top customer segments/niches (for any identity-trigger or personalization work); the store's real backlink profile and named competitors (for gap analysis and disavow decisions); and the store's actual CMS (Shopify/WooCommerce/custom), since every hands-on step in this source (meta edits, alt text, sitemap location, robots.txt syntax) is CMS-specific and was only demoed on WordPress, Blogger and Shopify examples.

## 10. Card index

1a35cd16217e — Track organic search performance with GA4, GSC and GTM
30500e1bfd7e — Prioritise rivals that outrank you, not the whole category
28b89b50c0e9 — Set 160-character meta descriptions with the key phrase
017caafa9aba — Choose keywords by search volume plus difficulty, not volume alone
877d742162c1 — Fix page speed before chasing rankings
883a5f7521dd — Make URLs readable and every page HTTPS
425291fc7791 — Use sitemaps to help crawlers discover store URLs
4d7e19f8ea9d — Understand the crawl-index-rank pipeline applied to your store
9fac54461fc4 — Judge directories and listings by relevance, niche and authority
a5e95b5877f2 — Split SEO work into on-page, off-page and technical buckets
ece6a69ffd62 — Build an engaging on-page experience, not just keywords
42f6cdb74b3b — Keep content on-topic and cite real sources
cf1b90a9f8f8 — Avoid black-hat tactics that risk store penalisation
5437c6f5b94e — Frame SEO as a long-term, measurable but unguaranteed investment
4c3f55273a76 — Use question data to improve content and product decisions
cd2dd5a72828 — Assume algorithms and search behaviour shift, and adapt
77a6f3560fde — Audit H1-H6 heading hierarchy on a product or category page
739d693029a4 — Write concise, descriptive titles for product and collection pages
3af48b4346f4 — Build and submit an XML sitemap to help Google discover sellable URLs
95ab0cd0f12e — Use canonical tags to prevent duplicate product and category pages from competing
2aca699ba689 — Speed up load times by compressing images and video
b06d74de8738 — Optimize URLs for clarity and crawlability
684253d7bab8 — Make the mobile experience the primary storefront design
b1cc7860ad7d — Design an SEO-friendly site architecture with navigation and interlinking
9d22914bec3a — Use Yoast (or an equivalent SEO plugin) for WordPress store page metadata and sitemaps
fa6c5a7abc3d — Implement schema markup to win rich results for products and reviews
153492ce5eeb — Set up robots.txt to guide crawlers away from cart, checkout and admin URLs
2a24068d5a43 — Understand crawl, index and rank mechanics to diagnose ranking problems
cb5f03373a82 — Choose keyword research tools by job: domain/catalog audit vs. traffic analysis
f2d9c44191c1 — Build link authority through third-party backlinks and guest posts
1b05d31a2f5c — Run local SEO with NAP-consistent business listings and near-me keywords
51be9ae93566 — Use YouTube SEO to drive store discovery and traffic
a6f04f0fcf2c — Write engaging content that keeps shoppers on the page and clicking
273f1ec32b07 — Audit technical SEO health: HTTPS, responsiveness, load time, sitemap, schema, citations
78c8dfa93009 — Keep technical SEO current as search algorithms change
f94ce42ad17a — Robots.txt: Block Admin and Cart Paths, Keep Product Pages Crawlable
ea2d1dfe6516 — Use Google Keyword Planner for Seed and Long-Tail Keyword Discovery
09c9050e0d04 — Use Google Trends to Time Content and Compare Keyword Demand
1d5f63c6c8b4 — Page Speed Thresholds and Mobile-First Priority
88f4ed4866f4 — Set Up Analytics and Understand Its Hard Start Date
82c14d6403d3 — Read Search Console Impressions, Clicks and CTR Without Panicking
6387bf5f570f — Fix 404s by Redirecting to the Nearest Relevant Page
02ce9701b980 — Site Settings: Name, URL, Favicon and Tagline in Your CMS
933f7a1d51d8 — Google Panda: Diagnose Thin and Duplicate Content Before It Suppresses Rankings
fe47b8b67efd — Investigate suspected manipulative backlinks before considering disavow
6e87a52bb240 — Judge a Link by Location, Anchor Text and Source Authority
5ad59b6f29ec — Land Guest Posts via 'Write For Us' and Resource-Page Prospecting
44c8a0dfa878 — Reverse-Engineer Competitor Backlinks Before Spending on Link Building
a3d1dead77d7 — Directory Submission Done Selectively and Correctly
b55f760c2d9e — Syndicate and Distribute Content Without Triggering Duplicate-Content Risk
b80a770d5913 — Use Social Posts as Link Vehicles with Clear CTAs
2c279628243e — Design UI/UX Around the Cart and Checkout Actions
1585b13af5cf — Use Customer Feedback to Feed Content and Keyword Selection
3ac30aa3629d — Incentive-Based Link Building: Discount Offers for Links, and Its Risks
ade5208b890b — Match Inbound Link Relevance to Your Target Market Region
9456f3ecb153 — Understand How Search Engines Evaluate Ecommerce Sites
cdfba6f37765 — Classify queries into informational, navigational and transactional buckets
64d0c1e22a94 — Build product pages that satisfy transactional intent end to end
161352fce48c — Diagnose wrong-audience targeting through three observable signals
7b56f452ec2a — Measure organic add-to-cart, checkout and purchase in GA4 to find funnel leaks
9345e5130d85 — Find and fix high-bounce pages by exporting first, prioritising second
860428181c80 — Use impressions vs clicks to find pages that rank but fail to attract
d6f2fb640d55 — Create and submit an XML sitemap as a bridge to search engines
37ad8a642ccb — Fix page speed and Core Web Vitals using Search Console's diagnostic drill-down
e8655b693697 — Limit flash and heavyweight elements so crawlers can index the page
6468710f6f02 — Pogo-sticking: use SERP returns to judge whether your page answers intent
a7537cfd6597 — Optimise for branded (navigational) searches you should already own
59f3b87a9465 — Compete on original, current content rather than copied product copy
3ddb50cffb54 — Use eye-tracking and click-tracking principles to shape UX that converts
66929e2b51f5 — Use social media as an adjacent channel that feeds brand search
3f1fe6e32954 — Avoid black hat SEO that produces short-lived rankings and penalties
2913525fbe2e — Choose the right keywords before worrying about traffic volume
1bae7bf49f42 — Teach yourself to read a live SERP before writing a page
8c493a361720 — Audit Flash and JavaScript bloat as page-experience obstacles
e1b09c7773f5 — Confirm your store already has an auto-generated XML sitemap instead of building one
0dc5d1a90cf4 — Match sitemap type to audience: XML for crawlers, HTML for shoppers
87e5562eb673 — Use Ahrefs keyword difficulty filters to find rankable store keywords
16bdb59b661a — Mine question keywords and filter by KD when planning store content
599c201a864f — Assess competitor authority and SERP features before choosing a keyword
1ec36409dfe1 — Choose a content format matched to the query and buyer stage
9f38dfbf4f52 — Apply personalization and localization to store content and offers
31b0c4a879ee — Read engagement, bounce and conversion metrics by page in GA4
1c1b6e9f3e7b — Spot declining pages by comparing active users period over period
63d26551705b — Install GA4 by adding the measurement tag to the site head
1cd8cac5630e — Size the SEO opportunity with GA4 channel comparison
b9c13080c7d1 — Create and verify a Google Business Profile for local store discovery
aab362a7a742 — Use Google Search Console for crawl issues and indexing health
01f36de58806 — Use engagement and conversion metrics to diagnose shopper fit
8c9e98850417 — Plan visually with mapping tools, but build strategy from competitor analysis
010063066fd9 — Prioritise low-difficulty, high-volume terms over vanity head keywords
8c1e01fcf839 — Reference the sitemap in robots.txt to control crawling and discovery
8b18558928513 — Treat canonical URLs as the single version of each store page
cd191b374d2e — Understand where SEO tracking tools fit before wiring them up
2e6780bee413 — Prepare store content for AI-assisted and voice search
e2547f7490bb — Edit permalinks to keep product and post URLs short and specific
be53a755c01a — Set follow/nofollow deliberately when building internal links
c0017f6a1d90 — Set Up Google Search Console for a Store Property
b243bdf156ec — Find High-Impression Low-Click Queries in Search Console
5895232c1ead — Compare Two Periods to Isolate Which Pages Lost Clicks
38ede7630596 — Audit Indexing Coverage and Fix 404s and No-Indexed Pages
d0575f65e6d3 — Install Google Tag Manager and Deploy Analytics Through It
c88b20d07187 — Create and Validate Articles/Blog Schema for Rich Snippets
639b2b41168f — Fire Page-Specific Schema from Google Tag Manager
b6d9e2525ff1 — Read an Ahrefs-Style Domain Rating and Backlink Profile
e3495a592539 — Compare Ranking Position Over Time to Find Lost and Declined Keywords
b36fc4bc173f — Attribute Traffic Loss to Specific Pages Using Peak-Period Comparison
e592af67a06c — Judge Backlink Quality with Referring Domains, DR and Spam Score
86975c6c2e81 — Run an Ahrefs Site Audit and Prioritise Errors by Colour
786a486134927 — Write Meta Titles and Descriptions Inside the CMS Within Length Limits
6cd7c100722a — Write and Place Alt Text for Store Images
cf900456ba0e — Use Semrush Keyword Gap to Find Competitor Terms You Are Missing
7234716f3e22 — Track Add-to-Cart and Button Click Events Without Back-End Code
59a0144c8001 — Set up Add-to-Cart event tracking with Google Tag Manager without touching site code
ca8c68867627 — Diagnose where shoppers drop off in the add-to-cart-to-purchase flow
