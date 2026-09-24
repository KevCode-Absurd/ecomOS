# Beginners Guide to Shopify SEO - Full Course (4+ Hour Masterclass)

source_id: 1auRfTru5x54m8nlBa6w5kN4eomlWF7RE  |  folder: 15-SEO-search  |  cards: 76  |  words: 42,207  |  type: course (multi-video transcript, screen-recorded)

credibility: Two presenters from "607 Media," a Shopify SEO agency. Miko Martinez (co-founder) presents technical SEO, site speed, keyword research/topical maps, navigation/site structure, collection pages, product pages, and blog content. Chris Graham (co-founder, "in charge of off-page SEO") presents the link-building modules (overview, foundational links, guest posts/niche edits, HARO/Connectively). Both state "6+ years in SEO" and "200+ projects," with claims of scaling some clients to seven-figure annual revenue. Evidence offered is the agency's own client work: named case-study numbers (below) and named example brands (RighteousFel, MyProtein, Blinds Style, Chewy, REI, Brumate, Omnia Fishing, Soapery, Q for Quinn, Faets/Fera Pets, Half Priced Drapes) shown live on-screen, not independently audited. The course is also a sales funnel: every module ends with a pitch to book a call for the agency's paid "10x Shopify SEO Accelerator" program (stated goal: "at least $20,000 in monthly profit") and for a paid "Shopify SEO Mastermind" School community. No tool in the course is disclosed as a paid affiliate placement, but several named tools (Semrush, Keyword Cupid, Crush Pics, Sitebulb, Snov.io, Instantly, SEO Builder) are recommended repeatedly enough that an undisclosed commercial relationship cannot be ruled out — flagged per tool below.

date signals: Case-study screenshot dated "updated September 11, 2024" is the only explicit date in the transcript; treat the course itself as roughly 2024-era. Tools and their described behavior (Shopify admin paths, Semrush/Ahrefs features, HARO's rename to "Connectively," Google SERP feature availability) are all live products that change frequently — every UI- or feature-dependent step is tagged `[verify UI]` and every named third-party tool is tagged `[web check]` for current name, pricing, and feature set below. The FAQ rich-snippet guidance is explicitly self-aware that Google's display of that feature was already declining "less and less" at recording time — treat as further degraded now.

## 1. What this source is for

A soup-to-nuts Shopify SEO course, run as the agency's own service delivery playbook: technical SEO fixes specific to Shopify's default behavior (URL duplication, tag/vendor auto-pages, sitemap quirks), site speed, topical-map-based keyword research, site structure and navigation, on-page templates for collection and product pages, blog/content strategy tied to topical authority, and a long off-page/link-building sequence (foundational links, guest posts, niche edits, HARO/Connectively). It is meant for an operator building or auditing a Shopify store's organic-search program end to end, and it repeatedly frames each module as one piece of a larger sequence that only pays off "unlocking $20,000 in monthly profit" when run as a whole system, not cherry-picked.

## 2. Principles

1. Technical SEO is the mandatory first step because it lowers Google's "cost of retrieval" (crawl-budget efficiency); skipping it undermines content and backlink investment. Presenter's framing, not an external citation. [6b922910be56]
2. Shopify's default product URLs duplicate under every collection path a product is linked from, even though the canonical tag still points to the clean URL — this wastes crawl budget and must be fixed in the theme's product-grid snippet, not left alone. [d8681a26d74e]
3. Fixing that URL duplication breaks Shopify's URL-derived breadcrumbs, so breadcrumbs must be rebuilt manually via a metafield, not left broken. [97c5e148f639]
4. Auto-generated Shopify pages (product/blog tags, vendor pages, product-type pages, "all collections"/"all products"/"new products") are structurally unable to carry unique SEO elements and should be noindexed, not left indexable by default. [c45f3f4a4121]
5. A custom robots.txt is a useful second layer to block crawling of the same low-value page classes, but only after the URL-duplication fix is in place — applying it first can create crawl problems. [9098b567f595]
6. Product variants with no distinct search demand should be merged into one product (Shopify variant options); variants worth keeping separate should canonicalize to one primary product page. [4c936159bddb]
7. Deleted products must 301-redirect to a relevant replacement (product or collection), never straight to a 404, to preserve link equity and user experience. [abd78e24fb44]
8. Shopify does not auto-exclude noindexed/canonicalized pages from its sitemap the way WordPress does — sitemap exclusion is a separate, manual step, and the default "hidden" toggle also forces noindex,nofollow as an unwanted side effect. [9dc7ea365326]
9. Structured data (Product, Article, BreadcrumbList schema) is usually present by default in Shopify themes but must be verified, not assumed — errors are often trivial (a missing comma) but silently cost rich-snippet eligibility. [15208e629d08]
10. Shopify is fast out of the box; site-speed work is mostly about avoiding self-inflicted bloat (heavy themes, oversized images, unnecessary apps) rather than "optimizing" from a slow baseline. [6223d92e1e72]
11. Site speed is treated as both a conversion lever (bounce rate) and a modest, not primary, ranking signal — the source's own cited graphics describe the ranking effect as "slight." [6223d92e1e72]
12. Keyword research should map customer thought process and buying-journey stage, not just chase search volume. [6ebefab0aa29]
13. A topical map (a full roadmap of every collection/product/blog topic needed to be seen as a niche authority) is presented as superior to a flat keyword list — "keyword research on steroids," in the presenter's words. [7fe6a9f64adf]
14. Page type (collection, product, or blog post) should be decided by inspecting what already ranks in positions 1-3 for the target term, not by internal preference. [6f239699ac8d]
15. For Shopify stores specifically, bottom-of-funnel pages (collections, products) should be prioritized over blog content, because they convert directly and pay back SEO effort fastest. [40bc9625a691]
16. One topic per page, not one keyword per page: a page carries one primary keyword (H1, URL, title) plus many secondary/related keywords; splitting genuinely different topics (e.g., different colors of the same product) onto separate pages is still required. [69c5a2ad65bb]
17. Collection pages absorb broad/option-seeking transactional terms; product pages absorb only truly specific queries; the homepage absorbs one broad, high-level term that must not overlap any collection's target term. [6d5b32906d70]
18. Site structure and internal linking should be derived directly from the topical map (homepage -> collections -> subcollections by attribute), because a search query is treated as a "question" and a page as an "answer" — the tighter that match, the better the ranking odds (presenter's own analogy). [f1130887a71f]
19. Keyword cannibalization (two pages competing for one term) actively confuses ranking and must be fixed by enforcing one-page-per-topic, not by keyword repetition across pages. [e6d59dcb5f23]
20. Expanding a broad category into subcollections is good when each subcollection is genuinely distinct and has its own search demand; splitting into near-duplicate pages with no unique value is a mistake in the other direction. [607cf326f1ba]
21. Content and collections must stay inside the store's core topical map; branching into "shoulder niches" before fully dominating the core topic dilutes relevance and can cost rankings on the ORIGINAL topic too, not just fail to gain the new one — illustrated by the presenter's own agency's past mistake. [626394ae29f2]
22. Main-menu structure should scale with catalog size (simple menu for small catalogs, direct subcategory exposure or "shop by X" for large/varied catalogs), with the explicit goal of minimizing clicks to product for both users and crawlers. [5e99325d5f63]
23. The homepage should feature the highest-search-volume collections prominently, because the homepage usually holds the most backlinks and can pass that link equity into the pages you most want to rank. [1dfb2e52dbf9]
24. Shopify's default filter/facet URLs are parameter-based and not indexed; any filter combination worth ranking needs a real, dedicated collection page instead, since parameter pages cannot carry unique content. [6637fae5f44a]
25. Product grids should avoid JavaScript rendering (crawlers struggle with it), should show a healthy number of products per page with numbered pagination, and should surface enough on-grid detail that users don't always need to click through. [c463c6a96f1d]
26. For Shopify stores with 50+ products, collection pages are claimed to drive over 80% of organic revenue, because broad category terms carry far more search volume than specific product terms — the presenter's stated generalization, not a measured statistic for any given store. [c463c6a96f1d][45f79a195c33]
27. A bare collection page (H1 + grid) is not enough content for search engines to understand the page; more genuine, non-stuffed content increases perceived relevance and is framed as a competitive opening because large retailers (Amazon, Target) auto-generate thin category pages instead of building this out. [99f0bb9ef605]
28. Product pages should only be actively optimized/indexed when the specific product name or attribute combination has real search volume; otherwise, effort (and even indexing) should shift to the parent collection page. [496c62ba9cac]
29. Discontinued or out-of-stock product pages must never be deleted outright if they carry rankings or traffic — replace the purchase CTA (with "shop similar" or "notify me") and keep the URL live. [1fdc94e24437]
30. A Shopify store needs blog content mainly because it supports collection-page rankings via internal linking and topical authority, not primarily because blog posts themselves convert or rank best — this is stated as the "key thing" even though blog posts can also directly rank informational queries. [45f79a195c33]
31. Topical authority should be built one cluster at a time — fully cover one topic before branching to an adjacent one, using a bridging piece of content to connect clusters. [435ce96184bc]
32. Backlinks are treated as the presenter's most important ranking factor ("even more important... with the rise of AI content") — Chris Graham's stated opinion, not an externally cited ranking-factor study; flagged as contested, see section 9. [c26fdb13c1b0]
33. Off-page work should proceed in a deliberate sequence: foundational links first (safe, free, establishes "entity"), then guest posts/niche edits ("bread and butter"), then HARO/Connectively and linkable assets/digital PR for higher-authority editorial links. [4143ac10dcfc]
34. Link building toward your own pages should mostly target the root domain early (50-75% in the first 3 months) before shifting weight to specific "low-hanging fruit" collection pages, and should track your own link-gap versus competitors to set a monthly pace. [4143ac10dcfc][be35a345338047d5]
35. Backlink quality is judged on follow status, anchor-text naturalness, topical/page relevance, authority-score context (never in isolation), and whether your link volume to a page stays in a natural range relative to competitors. [d959e63d97697]
36. Anchor text should be diversified (mostly partial/URL/brand/topic anchors, few exact-match) and calibrated against top competitors' own anchor-profile ratios, to avoid looking artificially over-optimized. [fab6f93fabc4]

## 3. Procedures

### A. Technical SEO audit (three-step process)
1. Manually review the store for the known Shopify issue classes: product URL duplication, auto-generated tag/vendor/type pages, unredirected deleted products, variant duplication, missing/incomplete structured data. [6b922910be56]
2. Crawl the whole site with a tool such as Sitebulb: create a new project, use the Chrome (JavaScript-rendering) crawler, set a mobile device/user agent (Google uses mobile-first indexing), and turn on structured-data checking in the crawl settings. [verify UI] [6b922910be56]
3. Review the crawl results dashboard: issues are grouped critical/high/medium; fix critical and high first (crawl errors, broken links, orphan pages, schema errors, broken images, indexing issues, duplicate content, missing titles/meta descriptions/alt tags), then work down the list. [6b922910be56]
4. Open Google Search Console: check the Page Indexing report for 404s, "Crawled - currently not indexed," and robots.txt blocks; 301-redirect unintended 404s to the correct live page. [6b922910be56]
5. Check GSC's noindex pages: confirm each was intentionally set noindex; if not intended, remove noindex and, if the page should rank, ensure it isn't excluded from the sitemap. [6b922910be56]
6. Check GSC's Shopping/Enhancements structured-data report for schema errors (often a trivial fix, e.g., a missing comma). [6b922910be56][15208e629d08]

### B. Fix Shopify product URL duplication
1. Confirm the issue: open the same product from two different collections and note the URL changes (e.g., `/collections/healthy-beef-jerky/products/x` vs `/collections/jerky/products/x`), then view source to confirm the canonical tag still points to the clean `/products/x` URL. [d8681a26d74e]
2. Go to Shopify admin > Online Store > Edit code > Snippets, and find the product-grid file (commonly `main-collection-product-grid.liquid`, name varies by theme; search for "grid"). [verify UI]
3. Search that file for the string `within_collection` and delete every instance so product links resolve to the clean `/products/` URL. [verify UI]
4. Save. Some newer themes already omit this parameter by default — if you can't find it, no action is needed. [d8681a26d74e]

### C. Rebuild breadcrumbs after the URL fix (metafield method)
1. In Shopify admin, go to Content > Metaobjects > Manage definitions > Products, and create a new definition (e.g., "breadcrumb"). [verify UI]
2. Set the definition to Global, type = URL (avoid the "collection" type — the source says it "can create issues"). [verify UI]
3. For each product, store the URL of the collection it belongs to in this metafield.
4. Edit the theme's breadcrumb snippet to render the link from this metafield instead of the URL-derived default. [verify UI] [needs brand data: which products need which collection assigned in the metafield]

### D. Noindex auto-generated tag, vendor, type, and utility pages
1. Identify tag pages (product tags and blog tags), vendor pages, product-type pages, and utility pages ("all collections," "all products," "new products"). [c45f3f4a4121]
2. Add a `noindex, follow` code snippet to `theme.liquid` for each page class (tag pages, vendor pages, product-type pages, utility pages) — separate snippets per class, per the source. [verify UI]
3. For any tag topic you actually want to rank (e.g., "moisturizer for dry skin"), build a real, dedicated collection page instead of relying on the tag page, so you control H1/URL/title/content. [c45f3f4a4121]

### E. Custom robots.txt (defense in depth)
1. Check the current robots.txt at `yourdomain.com/robots.txt`.
2. In Shopify admin > Online Store > Edit code > Templates, add a new template and select the "robots.txt" template type. [verify UI]
3. Add rules blocking crawl of: all-products collection, vendor pages, product-type pages, product tag pages, blog tag pages, replacing any placeholder domain with your real one. [9098b567f595]
4. PREREQUISITE: only deploy this after the product-URL-duplication fix (step B) is live — doing it first "can create crawling issues," per the source's explicit warning. [9098b567f595]

### F. Manage product-variant duplication
1. Judge whether each variant (e.g., color, size) has meaningful independent search volume and would carry genuinely unique content if given its own page. [4c936159bddb]
2. If not: merge variants into one Shopify product using native variant options (one URL, one content set). [4c936159bddb]
3. If you want separate variant pages anyway: create them, then set a canonical-URL custom metafield on each secondary variant pointing to the primary product's URL, and update the theme to emit that canonical tag from the metafield. [verify UI] [4c936159bddb]

### G. Redirect deleted products
1. Before or immediately after deleting a product, go to Shopify admin > Online Store > Navigation > View URL redirects. [verify UI]
2. Add a redirect from the deleted product's URL to a relevant replacement product or collection page (not the homepage, unless nothing relevant exists). [abd78e24fb44]
3. Confirm in GSC that the old URL now returns a 301, not a 404.

### H. Exclude pages from the sitemap without forcing noindex
1. Recognize Shopify does not auto-remove canonicalized/noindexed pages from its sitemap (unlike WordPress) — this is always a manual step. [9dc7ea365326]
2. Use Shopify's hidden SEO field (via a special admin URL path) and set it to true to remove a URL from the sitemap. [verify UI]
3. CAUTION: that hidden toggle also sets the page to `noindex, nofollow` as a side effect — if you only want sitemap exclusion (e.g., for a canonicalized variant page), this is unwanted. [9dc7ea365326]
4. To avoid the side effect, edit `theme.liquid`, find the relevant sitemap-output section, and replace it with the provided code snippet so the page is excluded from the sitemap without the forced noindex/nofollow. [verify UI] [9dc7ea365326]
5. Test by requesting the sitemap again after the change.

### I. Verify structured data
1. Check theme output for Product schema (price, availability, ratings, shipping/returns where applicable) — most themes include a basic version by default, but verify it actually outputs and is complete. [15208e629d08]
2. Check Article/BlogPosting schema on blog templates the same way.
3. Check the theme's `breadcrumbs.liquid` snippet (under Snippets) for BreadcrumbList markup reflecting the real site hierarchy. [verify UI]
4. Use GSC's Shopping/Enhancements report plus a crawler's structured-data check to catch errors.

### J. Site speed: sequence of fixes (in the order the source presents them)
1. Baseline with Google PageSpeed Insights to see actual bottlenecks and third-party script impact before changing anything. [6223d92e1e72]
2. Choose/keep a lightweight theme: Dawn (free) or Palo Alto (paid) are the source's named picks; on an existing theme, replace sliders with a single static hero image and cut oversized carousels (source's example: from 64 items down to about 8). [verify UI] [1a7d18d205ed]
3. Set image formats by role: WebP or JPEG for product photos; WebP for hero/text graphics; PNG for lossless/critical clarity; SVG for logos/icons. Compress with an app (source uses "Crush Pics," ~50% file-size cut in its example). [web check: Crush Pics] [3472ce4f007f]
4. Resize images to actual display dimensions before upload; implement `srcset` so browsers load device-appropriate image sizes (mobile small, high-DPI large). [verify UI: requires theme code] [3472ce4f007f]
5. Implement lazy loading on offscreen images: add the `lazysizes.js` library to the theme's assets folder, include it via `theme.liquid`, then on each image tag replace `src` with `data-src` and add a `lazyload` class. Do NOT lazy-load the hero/LCP image. [verify UI] [00a2fbad5f22]
6. Audit and remove orphaned app code: uninstalling a Shopify app does not always remove its injected theme code; use PageSpeed Insights' "reduce the impact of third-party code" finding to spot leftover scripts from apps you no longer use. [959f69db4f65]
7. Conditionally load remaining app scripts by page type (e.g., product-review widgets and image-zoom scripts only on product templates; social-share scripts only on blog templates) using a Liquid `if` condition instead of loading sitewide via `theme.liquid`. [verify UI] [504893b96bd4]
8. Minify JS/CSS: no-code route is an app such as "File Optimizer"; manual JS route is "JSCompress"; Shopify's built-in CSS route is naming the file with a `.css.liquid`-style extension so Shopify auto-minifies it — verify current accepted extension against Shopify docs. [web check] [ac5223c74551][96f67f5ea6a7]
9. Add `async` or `defer` to non-essential third-party scripts (live chat, analytics/tracking) so they don't block rendering; have a developer implement and test cart/checkout/variant-picker behavior afterward. [5fe9759a8a5c]
10. Add resource hints in the `<head>`: `preload` for immediately-needed assets, `prefetch` for likely-next-page assets, `dns-prefetch`/`preconnect` for known third-party domains (analytics, social buttons). [verify UI] [edcb1a9b8cef]

### K. Keyword research and topical map build
1. Start from a seed product term and generate variations across material, room/use-case, question form, and buyer-vs-explorer phrasing (source's running example: "blackout curtains" -> "linen blackout curtains," "blackout curtains for bedroom," "do blackout curtains keep heat out"). [6ebefab0aa29]
2. Pull the full matching keyword list for the seed term from Semrush (source's example returned roughly 21,000 keywords containing "blackout curtain"). [web check: Semrush] [7fe6a9f64adf]
3. Cluster the list by search intent/SERP similarity — manually, or with "Keyword Cupid," which the source says clusters automatically based on SERP overlap so a single page can serve a full cluster. [web check: Keyword Cupid] [7fe6a9f64adf]
4. Prioritize by volume; move top clusters into a "keyword map" tab (keyword, volume, cluster).
5. In a second "topical map" tab, assign each cluster: page type (collection/product/blog), primary keyword, secondary keywords, URL, volume, current ranking, and publish status (published / needs refresh / apply quick wins / needs publishing). [dabcaf2093cb][7fe6a9f64adf]
6. Supplement with additional idea sources: Wikipedia, Google Trends, competitor sites, Exploding Topics. [7fe6a9f64adf]
7. For each cluster, decide page type by Googling the term and matching whatever occupies positions 1-3 (collection pages -> target with a collection; informational articles -> target with a blog post; mixed -> lean toward the dominant type and cross-check buyer intent). [6f239699ac8d]
8. Prioritize which pages to build/fix first: bottom-of-funnel (collection/product) pages before blog content; within those, sort Google Search Console by impressions to find pages ranking close to top-3 ("low-hanging fruit") and optimize those plus closely related pages first. [40bc9625a691]
9. Run a keyword-gap analysis (Semrush's "Keyword Gap" under Competitive Research: your domain + competitor domains) to find keywords competitors rank for that you don't — most winnable when your backlink profile is stronger than theirs. [40bc9625a691] [needs brand data: your own backlink-profile strength vs. named competitors]
10. Assign one primary keyword per page (H1/URL/title) plus secondary/related/misspelled variants; split genuinely different topics (e.g., different product colors) onto separate pages. [69c5a2ad65bb]
11. Build the site structure directly from the finished map: homepage -> primary collections -> subcollections by attribute (room, material, color); feature every subcollection from within its parent collection page. [f1130887a71f]

### L. Collection page build/optimization
1. Set the three core on-page elements: title tag (target keyword at the very start, up to ~60 characters, fill remaining space with modifiers/secondary keywords), H1 (exactly the target keyword), URL (as short as possible, mirroring the keyword). [d22a5b9d1e85]
2. Build the product grid: use Shopify's default Search & Discovery app rather than a JavaScript-rendered grid; show roughly 36-48 products per page (as many as possible without hurting speed); use numbered pagination, not only previous/next; surface product details (color, short spec, price) directly in the grid. [c463c6a96f1d]
3. Add faceted navigation once the collection has roughly 200+ SKUs; for any filter combination worth ranking, build it as its own dedicated collection page instead of relying on the (unindexed) parameter-filtered view. [6637fae5f44a][c463c6a96f1d]
4. Add the content stack, in order: (a) short description (max 2 lines) above the grid, below the H1; (b) detailed description (500-1,000 words) below the grid, including contextual internal links to relevant subcollections/blog posts; (c) FAQ accordion sourced from Google's "People also ask" for the target term; (d) 3 manually hand-picked featured reviews containing the target keyword, implemented in plain HTML/metafields, not a heavy review app. [ce1613cde42d][4d35e548f749][83dbf0409f3c]
5. To fit both a short and a long description in Shopify's single description field, either (a) edit the collection template's `collection.description` output with a split-marker code snippet so text above the marker renders above the grid and text below renders where a second snippet is placed below the grid, or (b) use a "read more" toggle (paste the provided code plus a small JS snippet). [verify UI: exact liquid not captured in transcript] [95c668e0b955]
6. Add subcollections for meaningful splits (e.g., stick/upright/handheld/robotic vacuums) and internally link them from the parent collection; reusing the same product across multiple collections is explicitly fine and not an SEO problem. [607cf326f1ba]

### M. Product page build/optimization
1. Set the three core elements: title tag (target keyword at start, ~60 characters, bulk-template for large catalogs), H1 (literal product name/target keyword), URL (short, keyword-matching). [c758a7b81cac]
2. Decide whether to even optimize/index the page: check if the specific product name/attribute combination has real search volume (Semrush or similar); if not, shift effort to the parent collection page and consider noindexing the product page; if yes, optimize it fully. [496c62ba9cac]
3. Build the content stack, in order: H1; short description (50-150 words, include the product name); features/benefits bullets; specifications in table format (weight, dimensions, size, material); detailed description (500-1,000 words: differentiators, ingredients/nutrition, suggested use); FAQ accordion (from "People also ask"); product reviews. [c758a7b81cac]
4. Optimize images: descriptive filenames (product name + what's happening in the shot), descriptive alt text, WebP/JPEG format, compress and resize, lazy-load, and list ALL product images (not just the primary) in the XML sitemap. [50cbdf6d8b19]
5. Collect reviews actively via post-purchase email (offer a discount on the next order in exchange), and implement Review/AggregateRating schema so star ratings render on the SERP — verify your review app actually outputs this markup. [55dc25234b47]
6. Implement all 4 recommended schema types: Product, Review, FAQPage, BreadcrumbList. [55dc25234b47]
7. Add breadcrumbs, tag-style category links, and a "frequently bought together"/related-products module. [43028e061152]
8. For discontinued products: keep the page live, replace the buy button with a "shop similar products" link. For out-of-stock: keep the page live, replace add-to-cart with a "notify me when available" stock alert. Never delete a page that had rankings/traffic. [1fdc94e24437]

### N. Blog content build
1. Source topic ideas from the completed topical map, not a random list. [869cf61bff5a]
2. Build the on-page basics: Shopify admin > Online Store > Blog posts > create; title tag (keyword at start, ~60 characters), H1 (the target keyword/topic), URL (matching), and use the "Edit website SEO" section at the bottom of the editor for page title/meta description/URL handle. [verify UI] [6731423ab54b]
3. Include the target keyword in the meta description for click-through (it does not directly affect rankings per the source, but the bolded keyword in the SERP snippet raises CTR). [6731423ab54b]
4. Before writing, inspect what currently ranks for the target term (structure, headings, subtopics covered) and match or exceed its depth and breadth. [869cf61bff5a]
5. Use visuals (images, video, infographics, tables, charts) to reduce bounce and increase time-on-page as an indirect SEO lever. [869cf61bff5a]
6. Embed direct product CTAs within or at the end of the post, matched to the post's topic. [84d4795d239e]
7. Build internal links from the post to relevant shopping pages and to other relevant posts; deliberately build backlinks to blog posts (not directly to shopping pages, which "looks unnatural"), then let internal links pass that authority to the shopping pages. [84d4795d239e]
8. Sequence topic production one cluster at a time: fully cover one topic (e.g., cold press juicers: how-to, health claims, comparisons) before starting an adjacent cluster; bridge with a comparison post (e.g., "cold press vs. masticating juicers") when you do expand. [435ce96184bc]

### O. Link building: foundational links (do this first)
1. Build the base layer: social profiles, business/local-directory citations, Web 2.0 profiles (examples: Medium, Behance). [9ef468a1aa73][d00b480b316f9]
2. Fill each profile out fully (business info, content, images) rather than dropping a bare URL — the source calls this "entity stacking," aimed at helping Google recognize the brand as a real entity. [d00b480b316f9]
3. For citations, prepare: business name, owner name, address, city, phone, website URL, business description, target (shopping-page) keywords, social links, logo; consider outsourcing citation building (source names "SEO Builder" as their outsourced vendor). [web check: SEO Builder] [d00b480b316f9]
4. Target at least 30 foundational links as a baseline (source's own internal, non-derived target). [d00b480b316f9]

### P. Link building: guest posts and niche edits
1. Target allocation for the first ~3 months: 50-75% of new links to the root domain, 25-50% to "low-hanging fruit" pages (collection pages ranking positions 4-10 in Semrush's Organic Research tool, picking about 3-5 per month depending on budget). [3cf4abf037ab]
2. Prospect for link sources: identify your true "SEO competition" (sites that rank for your target terms, which may differ from business competitors) via Semrush's Keyword Overview on a target term; pick mid-sized, niche-relevant competitors (explicitly skip giants like Amazon/Walmart/Target/Ikea) until you have at least 5 competitor domains. [931c46ea6362]
3. In Semrush Backlink Analytics, pull each competitor's backlinks filtered to: dofollow only, 1 link per referring domain, placement = "content," platform = "blog." Export. [web check: Semrush] [931c46ea6362]
4. Run the export through Semrush's Bulk Analysis (root domain), then filter to monthly visits > 1,000 and Authority Score >= 15 (raise the floor if your own profile is already strong). [931c46ea6362]
5. Widen prospecting to any topically relevant site, or adjacent-niche sites (e.g., interior design/home-improvement blogs for a curtain brand), while explicitly avoiding unnatural-feeling placements (e.g., an outdoor blog linking to a curtain brand). [931c46ea6362]
6. Find contacts: paid tools first (Snov.io, or Hunter.io) for a named person's email; manual fallback via each site's contact page/form or social profiles if not paying for tools. [web check: Snov.io, Hunter.io] [205cf1bbe674]
7. Write outreach: subject line must be both relevant and attention-grabbing (personalize with name/domain, use a question or light humor); body states your content specialty, willingness to pay a publishing fee if required, and that a dofollow link is the goal; personalize rather than sending the raw template. [ed27a5301c83]
8. Send at scale via a cold-outreach tool (source's top pick: Instantly; also named: Snov.io's outreach feature, Lemlist, GMass); warm up sending accounts first, start around 20 emails/day/account, ramp gradually; cap inboxes per domain and buy secondary look-alike domains for high-volume sending. [web check: all tools named] [6e04ce7fcb0e]
9. On any positive/clarifying reply: run final vetting (language, security, traffic, other quality metrics), negotiate price if paying (Semrush Authority Score used as a rough pricing-benchmark reference, case-by-case), then close. [cb6fea298ce4]
10. Write the guest post for the HOST site's actual audience, not your own customers; define the target page first, use AI (e.g., ChatGPT) to brainstorm titles/descriptions matching both the target keyword and the host's theme, then refine; 600-1,200 words unless the host specifies otherwise (note: the source's own slides briefly gave a conflicting 500-1,000-word range and self-corrected on camera). [d3cac352bc44]
11. Place the anchor naturally inside a relevant sentence near the top of the post, not isolated at the bottom; diversify anchor type (mostly partial/URL/brand/topic, very few exact-match) and calibrate the mix against your top 3 competitors' own anchor profiles. [cfd93f4f1fcb][fab6f93fabc4]
12. After publish: confirm the link is live, dofollow (or correctly qualified as sponsored/nofollow if paid), and contextual; review any host edits; repeat the whole loop. [3490d57698e0]
13. For niche edits/link inserts: instead of a new post, ask the host to add your link into an EXISTING, already-trafficked, topically relevant article; expect a fee; these are faster and often more powerful since the page is already indexed/aged; don't over-rely on inserts — balance with fresh guest posts. [3a7d9b1b9fd9]

### Q. Link building: HARO / Connectively
1. Sign up at Connectively (HARO's current platform name at time of recording — verify), verify email, select "subject matter expert." [web check] [verify UI] [e0058ce635d6]
2. Fill out your profile thoroughly, claiming expertise in your core niche AND closely related topics (e.g., a curtain brand also claims interior design/home improvement) to match more queries. [e0058ce635d6]
3. Start on the free/light plan to test fit for your niche before committing further. [e0058ce635d6]
4. Filter queries heavily by topic (don't over-filter by date/deadline — an older query can still be answered); for each candidate query, check the outlet's Domain Rating (Ahrefs free tool) or Authority Score (Semrush); skip very low-authority AND low-relevance queries, but still pitch highly relevant queries even from small or anonymous outlets. [e0058ce635d6]
5. Research each answer (Google first for orientation, then Quora/YouTube for genuine expert takes, then Reddit for real-world perspective) and emphasize a personal/experience-based "human touch," explicitly framed as a differentiator "especially with AI now." [493daec89c20]
6. Format for skimmability (bold key phrases, bullet points); keep a reusable 1-2 paragraph bio ready to paste; note that once submitted, a pitch's photos can no longer be edited, only viewed. [verify UI] [493daec89c20]
7. Track every query in a spreadsheet (query, outlet, authority, pitched y/n, outcome); watch the funnel rate (illustrative example given: 20 queries answered -> 2 positive replies -> 1 closed link) to decide whether to scale the effort. [7f70083e00d5]
8. Monitor email daily for journalist responses/follow-up requests; respond before any stated deadline. [7f70083e00d5]

## 4. Rules, thresholds and numbers

| Rule / setting | Number or threshold | Condition | Source's basis | Card id |
|---|---|---|---|---|
| Product grid item count | 36 to 48 products per page | Collection pages; "as much as possible without compromising site speed" | Presenter's recommendation | c463c6a96f1d |
| Faceted navigation trigger | ~200 SKUs | Add faceted nav once catalog crosses this size | Presenter's rule of thumb | c463c6a96f1d |
| Collection short description length | 2 lines max | Above the grid, below H1 (mobile UX) | Presenter's template | ce1613cde42d |
| Collection detailed description length | 500 to 1,000 words | Below the grid | Presenter's template | ce1613cde42d |
| Featured reviews on collection page | 3 reviews, manually picked | Bottom of collection page, keyword-containing | Presenter's template | 83dbf0409f3c |
| Product short description length | 50 to 150 words | Top of product page | Presenter's template | c758a7b81cac |
| Product detailed description length | 500 to 1,000 words | Below specs/features | Presenter's template | c758a7b81cac |
| Title tag length | up to ~60 characters | Collection, product, and blog titles | Presenter's rule of thumb, not a Google-enforced limit | d22a5b9d1e85, c758a7b81cac, 6731423ab54b |
| Meta description length | ~160 characters (product) | Affects CTR, not ranking per the source | Presenter's guidance (from sibling course notes; consistent with this source's product-page section) | c758a7b81cac |
| Product-page conversion rate from SEO traffic | 5% to 15% | Presenter's own observed range, no sample size given | Agency's own client data (unverified) | 496c62ba9cac |
| Collection-page conversion rate from SEO traffic | 2% to 5% | Same context as above | Agency's own client data (unverified) | 496c62ba9cac |
| Collection pages' share of organic revenue | over 80% | Stores with 50+ products | Presenter's stated generalization, not measured for any specific store | c463c6a96f1d, 45f79a195c33 |
| Foundational links target | at least 30 | Baseline for a new/growing store's base link layer | Agency's own internal target, described as "safe," not derived | d00b480b316f9 |
| Link allocation, first ~3 months | 50-75% to root domain, 25-50% to low-hanging-fruit pages | New/ramping link-building campaign | Agency's rule of thumb, adjusted after a few months | 4143ac10dcfc, 3cf4abf037ab |
| Low-hanging-fruit page selection | Semrush positions 4-10; pick 3-5 pages/month | Depends on link-building budget | Agency's method | 3cf4abf037ab |
| Backlink prospect filter: dofollow, links/domain | 1 link per referring domain, dofollow only, placement = content, platform = blog | Semrush Backlink Analytics export step | Agency's filter recipe | 931c46ea6362 |
| Backlink prospect filter: traffic | > 1,000 monthly visits | Site must clear this to be a reachable/healthy prospect | Agency's heuristic | 931c46ea6362, 102c5f4bc1f8 |
| Backlink prospect filter: authority | Authority Score >= 15 (raise if your profile is stronger) | Semrush Authority Score | Agency's heuristic | 931c46ea6362 |
| Link-gap analysis: quality floor | DR/DA >= 30, dofollow only | When counting your own vs. competitors' referring domains | Agency's heuristic | be35a345338047d5 |
| Link-gap worked example | You: 105 referring domains; competitor average: ~203; gap: ~98 | Illustrative example only, not a benchmark | Agency's own example numbers | be35a345338047d5 |
| Monthly link-building pace | ~4/month baseline (98 over 24 months); agency recommends 6-8/month | To close the gap above and keep pace with competitors still building links | Agency's recommendation | be35a345338047d5 |
| Cold email starting volume | ~20 emails/day/account, ramped gradually over a few weeks | After warm-up period | Agency's outreach practice | 6e04ce7fcb0e |
| Guest post word count | 600 to 1,200 words (source briefly, inconsistently also states 500-1,000 in one slide, self-corrected on camera) | Unless host specifies a different length | Agency's guidance | d3cac352bc44 |
| Anchor optimization timing | Lean on partial/URL/brand/topic anchors months 1-5; may start further optimizing around month 6-7 | Early vs. later link-building campaign | Agency's heuristic | fab6f93fabc4 |
| Image carousel/grid reduction example | From 64 items to ~8 | Site-speed cleanup example | Presenter's example, not a rule | 1a7d18d205ed |
| Image compression example | ~50% file-size reduction | Using the named "Crush Pics" app | Presenter's example | 3472ce4f007f |
| Search volume example (broad vs. specific) | "handheld vacuum cleaner" ~14,000/mo vs. "Shark WandVac handheld vacuum" ~490/mo | Illustrates why collection terms outrank product terms in volume | Presenter's tool-pulled example (tool/date unstated) | c463c6a96f1d |
| Keyword universe example | ~21,000 keywords found containing "blackout curtain" | Semrush pull for the topical-map worked example | Presenter's live demo | 7fe6a9f64adf |
| HARO/Connectively funnel example | 20 queries answered -> 2 positive replies -> 1 closed link | Illustrative benchmark for deciding whether to scale the tactic | Presenter's example ratio, not a guarantee | 7f70083e00d5 |

## 5. Diagnostics and checks

- **Is the product URL structure duplicating?** Open the same product from two different collections; if the URL path differs (contains `/collections/x/`) while the canonical tag (view source) still points to the clean `/products/` URL, the fix in Procedure B is needed. [d8681a26d74e]
- **Are tag/vendor/type pages indexed?** Search Google `site:yourdomain.com/collections/vendors` or check GSC's Page Indexing report for a spike of thin auto-generated URLs; if present, apply Procedure D. [c45f3f4a4121]
- **Is a robots.txt block causing crawl problems?** Check GSC's Page Indexing report for "blocked by robots.txt" errors on pages you actually want indexed; if the URL-duplication fix (B) isn't live yet, that is the likely cause — fix B before touching robots.txt. [9098b567f595]
- **Is a page correctly excluded from the sitemap without being wrongly noindexed?** Request the sitemap file after any hidden-SEO-toggle change and confirm the URL is absent; separately confirm in GSC that the page's index status matches your intent (indexed vs. noindexed). [9dc7ea365326]
- **Is structured data actually present and valid?** Run GSC's Shopping/Enhancements report and a crawler's structured-data check; look for common trivial errors like a missing comma. [15208e629d08]
- **Is the site actually slow, and why?** Run Google PageSpeed Insights; read the "reduce the impact of third-party code" section specifically to catch orphaned app scripts. [6223d92e1e72][959f69db4f65]
- **Is a keyword being cannibalized?** Check whether more than one page on the site targets the identical term (collection vs. product, or blog vs. collection); if GSC shows an unstable/switching ranking URL for one query, that is a cannibalization signal. [e6d59dcb5f23]
- **Should this product page be indexed at all?** Check the specific product name/attribute combination's search volume in a keyword tool; zero/negligible volume with a made-up or hyper-specific name (source's examples: fishing-lure names, ultra-specific fabric descriptions) means shift effort to the collection page instead. [496c62ba9cac]
- **Which pages should get link-building priority?** Sort Google Search Console impressions and Semrush ranking positions (4-10 = low-hanging fruit) to find pages closest to a top-3 breakthrough. [40bc9625a691][3cf4abf037ab]
- **Is a prospective linking site safe/worth pursuing?** Run the five-point checklist: (1) does it look like a real, coherent, single-topic site rather than a generic "about everything" link-selling blog; (2) check its domain history on the Wayback Machine for an unrelated past use (e.g., a former casino site now posing as an interior-design site); (3) is it topically relevant to your niche; (4) does it have at least ~1,000 monthly visitors, stable or growing, with no sudden traffic drop (possible penalty signal); (5) does the site's OWN backlink profile look clean/quality. [102c5f4bc1f8]
- **Is your off-page effort working?** Track a link-gap analysis periodically (own vs. competitor referring-domain counts, filtered to dofollow + DR/DA 30+) and a HARO/Connectively response-to-close ratio, to decide whether to scale or reallocate time. [be35a345338047d5][7f70083e00d5]

## 6. Tools, settings and named features

- **Sitebulb** - third-party site crawler used for the technical-SEO audit (Chrome/JS-rendering crawler, mobile device setting, structured-data check toggle). [verify UI] [web check: current pricing/features] [6b922910be56]
- **Google Search Console** - native/free; used throughout for Page Indexing, Enhancements/Shopping structured-data reports, and impression sorting for prioritization. [6b922910be56][40bc9625a691]
- **Shopify Search & Discovery app** - Shopify's own native app; recommended in place of JavaScript-rendered product grids. [c463c6a96f1d]
- **Google PageSpeed Insights** - free; baseline speed diagnostic and the source for "reduce the impact of third-party code" findings. [6223d92e1e72][959f69db4f65]
- **Crush Pics** - named Shopify image-compression app; one-click compression cited at ~50% file-size reduction in the source's example. [web check: current name/pricing, possible alternate spelling "Crush.pics"] [3472ce4f007f]
- **lazysizes.js** - open-source JS library used for lazy-loading offscreen images. [00a2fbad5f22]
- **File Optimizer** - named no-code Shopify app for auto-minifying JS/CSS. [web check] [ac5223c74551]
- **JSCompress** - named manual JS minification tool. [web check] [ac5223c74551]
- **Semrush** - paid SEO suite; used repeatedly for keyword research/topical maps (Keyword Overview, Organic Research for positions 4-10, Keyword Gap under Competitive Research, Backlink Analytics, Bulk Analysis, Authority Score). Named as the presenter's primary tool throughout; instructions "translatable" to Ahrefs per the source. [web check: current plans/pricing] [7fe6a9f64adf][40bc9625a691][931c46ea6362][be35a345338047d5]
- **Keyword Cupid** - named tool for automatic SERP-based keyword clustering. [web check: current name/pricing/availability] [7fe6a9f64adf]
- **Ahrefs** - named as Semrush's main alternative; its Domain Rating (DR) metric and a free DR-lookup tool are referenced for vetting HARO/Connectively query sources. [web check] [d959e63d97697][e0058ce635d6]
- **Google Trends, Wikipedia, Exploding Topics, competitor sites** - named supplementary keyword/topic discovery sources for topical-map building. [7fe6a9f64adf]
- **ChatGPT (general AI assistant)** - repeatedly recommended for: locating where to paste theme code, drafting guest-post titles/descriptions, and general troubleshooting. Treated as a drafting/troubleshooting aid, always to be refined by a human, per the source's own caveat ("you have to wrestle with AI sometimes"). [d3cac352bc44] and multiple technical-SEO cards
- **SEO Builder** - named vendor the agency outsources citation-building to. [web check: current name/pricing; possible undisclosed referral relationship] [d00b480b316f9]
- **Snov.io** - named paid email-finder (and outreach) tool, presenter's stated current preference. [web check] [205cf1bbe674]
- **Hunter.io** - named alternative email-finder tool. [web check] [205cf1bbe674]
- **Instantly** - named cold-email outreach platform, presenter's top pick ("best in the industry in our opinion"), paid with a free trial. [web check] [6e04ce7fcb0e]
- **Lemlist, GMass** - named alternative outreach tools, less strongly endorsed. [web check] [6e04ce7fcb0e]
- **HARO / Connectively** - journalist-sourcing platform; HARO rebranded to "Connectively" per the source; used for expert-quote backlinks. [web check: confirm current platform name/status] [e0058ce635d6]
- **Wayback Machine** - free tool used to check a prospective link source's domain history for red flags. [102c5f4bc1f8]
- **Dawn (theme)** - named free, lightweight Shopify theme recommendation. [verify UI: current Shopify theme catalog] [1a7d18d205ed]
- **Palo Alto (theme)** - named paid, lightweight Shopify theme recommendation (transcribed inconsistently as "Pao Alto" in places; verify actual theme name). [verify UI][web check] [1a7d18d205ed]
- **Metafields / Metaobjects (native Shopify feature)** - used repeatedly for breadcrumb rebuilding, canonical-tag management on variants, and custom collection-description splitting. [verify UI] [97c5e148f639][4c936159bddb]

## 7. Examples and case results

- Beauty brand: presenter's own client, stated to have grown from $1,000 to over $370,000 in monthly revenue with SEO. Example, not a promise; no timeframe, channel mix, or independent verification given. [source intro, not tied to a single card]
- Home improvement brand: presenter's own client, stated to have grown from $0 to over $140,000 in monthly revenue with SEO. Example only.
- Outdoors brand: stated to have doubled organic traffic in 3 months. Example only.
- Kids' hygiene brand: stated to have grown traffic 7x in 3 months. Example only.
- RighteousFel.com: used live on-screen to demonstrate the product-URL-duplication bug (same beef jerky product resolving to two different collection-prefixed URLs) and duplicate blog-tag pages. [d8681a26d74e][c45f3f4a4121]
- MyProtein: used as the example for direct subcategory access in the main menu (Bestsellers, Protein, Creatine, Amino Acids, Pre-workout, with Whey/Clear/Vegan/Blends sub-items) and for internal subcollection linking on its Whey Protein Powder collection page. [5e99325d5f63][f1130887a71f]
- Blinds Style: used as the example of a homepage mirroring the main menu ("shop by type," "shop by color," "most popular," "shop by room"). [1dfb2e52dbf9]
- Chewy: used as the example of faceted navigation (food texture, flavor, special diet, life stage) and image-based subcategory links on a cat-food collection page. [6637fae5f44a]
- REI: used as the example for out-of-stock/discontinued-product handling ("shop similar products" CTA) and for a simple product-spec table format. [1fdc94e24437]
- Brumate: used as the example of a "notify me when available" CTA on an out-of-stock color variant. [1fdc94e24437]
- Omnia Fishing: used as the example of tag-style category links on a product page (linking similar jigs by technique), and as an example of made-up product names with no search volume ("Finesse Bullet," "Hack Attack Flipping Jig," "ChatterBait Elite," "Dominator Tube") where the parent collection page should be optimized instead. [2b98fa10af38][496c62ba9cac]
- Soapery (essential oils brand): example where the collection page ranks #1 in the UK for "essential oils" AND individual product pages (rosemary, sandalwood, eucalyptus essential oil) also carry real search volume and should be individually optimized; also cited as a brand whose 200+ (stated "over 210") blog posts drive under 7% of site traffic directly but support collection-page rankings via internal linking/topical authority. [496c62ba9cac][45f79a195c33]
- Q for Quinn: example of a blog whose content drives over half the site's organic traffic, praised for depth, comprehensiveness, and heavy internal linking (example post: "types of women's underwear" with ~10 infographics). [869cf61bff5a]
- Faets / Fera Pets (name transcribed inconsistently): example of a small, newly relaunched site that published 1,100+ blog posts in a few months, already helping shopping-page rankings, but explicitly flagged by the presenter as imperfect (H1s stuffed with extra words, URLs too long) - presented as an early, in-progress case, not a finished result. [45f79a195c33]
- Half Priced Drapes and "Curtain Shop": used as the worked example of picking mid-sized, niche-relevant SEO competitors (vs. explicitly excluding Target/Walmart/Ikea) for backlink prospecting. [931c46ea6362]
- Fabric store example: product titles like "silk/spandex stretch crepe sheen blue" (vs. "navy") shown as too-specific/no-volume product pages, where effort should go to collection terms like "cotton woven fabrics," "quilting cotton fabrics," "eco-friendly fabrics" instead. [496c62ba9cac]
- Ikea vs. Wayfair vs. Walmart SERP comparison: used to argue that rich snippets (star rating, price range, return policy) increase perceived clickability versus a plain one-line listing - presenter's own visual/CTR opinion, not a controlled CTR test. [55dc25234b47]
- Healthline: used only as a scale example of dense internal linking across thousands of pages (not an ecommerce site). [84d4795d239e]

## 8. Mistakes the source warns about

1. Skipping technical SEO before content/link investment - "the strategy basically stands on shaky ground." [6b922910be56]
2. Leaving product URLs to duplicate under every collection path, wasting crawl budget. [d8681a26d74e]
3. Fixing the URL-duplication issue and leaving breadcrumbs broken as a result, without rebuilding them via a metafield. [97c5e148f639]
4. Letting Shopify's auto-generated tag/vendor/type/utility pages stay indexed as thin duplicate content. [c45f3f4a4121]
5. Deploying a custom robots.txt block before fixing product-URL duplication, creating new crawl problems. [9098b567f595]
6. Creating a separate product listing per low-demand variant instead of merging or canonicalizing. [4c936159bddb]
7. Letting a deleted product 404 instead of 301-redirecting it to a relevant page, losing traffic and link equity. [abd78e24fb44]
8. Using Shopify's default "hidden" SEO toggle to remove a page from the sitemap without realizing it also forces noindex,nofollow. [9dc7ea365326]
9. Assuming a theme's default schema is complete without verifying it in GSC/a crawler. [15208e629d08]
10. Adding apps, sliders, oversized carousels, and unnecessarily heavy images onto an otherwise fast Shopify baseline. [6223d92e1e72]
11. Leaving orphaned app code in the theme after uninstalling the app. [959f69db4f65]
12. Loading all app scripts sitewide via `theme.liquid` instead of conditionally by page type. [504893b96bd4]
13. Chasing keyword volume without considering search intent or buying-journey stage. [6ebefab0aa29]
14. Building a flat keyword list instead of a full topical map. [7fe6a9f64adf]
15. Targeting a page type (collection/product/blog) that contradicts what already ranks in positions 1-3 for that term. [6f239699ac8d]
16. Prioritizing blog content over bottom-of-funnel (collection/product) pages when SEO ROI is the goal. [40bc9625a691]
17. Keyword cannibalization: a collection page and a product page (or a blog post) targeting the identical keyword. [e6d59dcb5f23]
18. Overuse of the same keyword spread across many pages, believing it improves rankings when it actually confuses search engines. [e6d59dcb5f23]
19. Creating near-duplicate collection pages with no unique value (source's example: "top rated," "most popular," and "on sale" versions of the same category). [607cf326f1ba]
20. Branching into "shoulder niches" before the core topical map is fully covered - the presenter's own agency did this, ranked briefly, then lost rankings on the CORE topic too when Google recrawled and judged the site no longer focused. [626394ae29f2]
21. Homepage keyword overlapping with a collection page's target keyword. [6d5b32906d70]
22. Relying on Shopify's default parameter-based facet URLs to try to rank a specific filter combination (they aren't indexed). [6637fae5f44a]
23. Loading product grids via JavaScript, which crawlers struggle with. [c463c6a96f1d]
24. Using only "previous/next" pagination controls instead of numbered pages, forcing multiple clicks to reach deeper pages. [c463c6a96f1d]
25. Leaving a bare collection page (H1 + grid only) with no real content, making it hard for search engines to understand the page. [99f0bb9ef605]
26. Stuffing collection/product pages with obviously AI-generated or keyword-stuffed filler instead of genuinely useful content. [99f0bb9ef605][ce1613cde42d]
27. Optimizing a specific product page that has zero/negligible real search volume instead of the parent collection page. [496c62ba9cac]
28. Deleting a discontinued or out-of-stock product page outright instead of keeping it live with a replacement CTA. [1fdc94e24437]
29. Publishing blog content with no or poor internal linking to shopping pages - called out as a common mistake found in the agency's own audits of prior SEO vendors' work. [84d4795d239e]
30. Building backlinks directly and heavily to shopping/product pages, which "looks unnatural," instead of routing authority through well-linked blog content. [84d4795d239e]
31. Buying links from cheap marketplaces (source names Fiverr) or responding to unsolicited "we sell backlinks" outreach emails. [102c5f4bc1f8]
32. Building far more backlinks to one page than competitors have (source's example: competitors have ~10, you build 30) - "sticks out like a sore thumb" and risks a penalty. [d959e63d97697]
33. Using the same exact-match anchor text across most/all backlinks instead of diversifying anchor types. [fab6f93fabc4]
34. Sending cold outreach at full volume without warming up the sending account first, risking spam-filter flags. [6e04ce7fcb0e]
35. Using a generic, unmodified guest-post outreach template - the presenter says templates lose effectiveness once shared, and estimates personalized outreach beats roughly 70% of senders who use the raw template verbatim (presenter's own unverified estimate). [79c14ba1ded5]
36. Isolating a backlink anchor in an awkward standalone callout ("check out X here") instead of embedding it naturally in a relevant sentence near the top of the post. [cfd93f4f1fcb]
37. Over-filtering HARO/Connectively queries by deadline/date-posted instead of primarily by topic relevance. [e0058ce635d6]
38. Relying solely on a plain Google search to write a HARO/Connectively expert answer - journalists don't want an answer they could have Googled themselves. [493daec89c20]

## 9. Caveats, conflicts and what is missing

- **Sales-funnel framing throughout.** Every module ends with a pitch for the agency's paid "10x Shopify SEO Accelerator" program and a paid community; the course's own case-study numbers are the agency's unaudited client claims, not third-party-verified results. Treat all named revenue/traffic outcomes (beauty brand $370k/mo, home improvement $140k/mo, "doubled traffic in 3 months," "7x traffic in 3 months," "20K in monthly profit") as marketing claims, not benchmarks.
- **Direct conflict with Google's own stated policy on paid links.** The source's guest-posting module explicitly acknowledges that Google's guidelines treat manipulative link-buying as "link spam," then states the presenter's personal view that "everyone does it," that paid links "work really well provided you're doing it properly," and frames the agency's process as doing it "safely." This is a stated policy violation normalized as industry practice, not a compliant method - flag prominently before following the paid-link/outreach procedures (Procedure P), and note that a paid or sponsored placement should be qualified with `rel="sponsored"` or `rel="nofollow"`, not treated as a plain dofollow link, if you want to stay within Google's guidelines. [ed27a5301c83][cb6fea298ce4][3490d57698e0]
- **"Backlinks are the most important ranking factor" is Chris Graham's stated opinion**, not attributed to any external study in the transcript, and conflicts with the equally strong emphasis this same source places on technical SEO as "the mandatory first step" and on-page content/topical authority as what "allows you to outrank" competitors. The source does not reconcile which factor actually matters most; treat both technical foundation and off-page authority as necessary, not as a ranked hierarchy this source proves. [c26fdb13c1b0][6b922910be56]
- **FAQ rich-snippet guidance is self-aware but dated.** The source itself notes FAQ rich results were "appearing less and less" on Google's SERP at recording time (roughly 2024) - implement FAQ accordions for genuine UX/pre-purchase value, not on a promise of a rich-snippet payoff, and verify current Google search-feature support before promising this to a brand. [4d35e548f749][55dc25234b47]
- **Spec-table rich snippets are called out as declining too** - same caveat as FAQ snippets; keep the table for clarity/UX regardless. [c758a7b81cac]
- **Exact code snippets are not fully captured in the transcript.** Several procedures (description-splitting liquid code, sitemap-exclusion code, breadcrumb-metafield rendering code, robots.txt rule sets) reference on-screen code that is not verbally itemized - implementers must reconstruct or re-source the actual snippet, not assume the summary above is copy-pasteable. [95c668e0b955][9dc7ea365326][97c5e148f639]
- **Tool/vendor names carry an undisclosed-relationship risk.** Semrush, Keyword Cupid, Crush Pics, Sitebulb, SEO Builder, Snov.io, Instantly, and the specific theme names (Dawn, "Palo Alto") are recommended with unusual consistency and enthusiasm across an agency-run course; none is disclosed as a paid/affiliate placement in the transcript, but the pattern is consistent with undisclosed sponsorship - verify independently rather than treating any single named tool as the only valid option. [web check: all named tools]
- **No control group or independent measurement anywhere in the course.** Every numeric claim (conversion-rate ranges, the "80% of organic revenue from collections" figure, the link-gap worked example numbers, the HARO funnel-conversion example) is presented as the presenter's own experience or a single illustrative example, not as a study with a defined sample, methodology, or replication. Use these as directional heuristics, not as targets to report to a brand as guaranteed outcomes.
- **The "one page/product needs X search volume to deserve a page" framework is a judgment call the source itself hedges** ("this is another topic for discussion") - it gives worked examples on both sides (products with no volume that should be deindexed vs. Soapery's individual essential-oil products that DO have volume and should rank) but no formula for where the line sits for an arbitrary catalog. [496c62ba9cac]
- **Gap vs. common ecommerce SEO advice:** this course's emphasis on collection pages over product pages as the primary SEO revenue driver, and its instruction to potentially noindex low-volume product pages, runs counter to a common alternate ecommerce SEO position that every product page should be indexed by default for long-tail coverage; this source explicitly disagrees with that default-index approach for products with no measurable demand. Treat as a genuine strategy difference to make deliberately per catalog, not an error in either source.
- **What the source does not cover:** Google Ads/paid search interplay, GA4 or non-Search-Console measurement/reporting setup beyond crawl/index reports, international/multi-language SEO (hreflang), migration/replatforming SEO, mobile app deep-linking, and video/YouTube SEO are all outside this course's scope.

## 10. Card index

6b922910be5636aa4d47cbf5 - Technical SEO on Shopify: Audit Order and Purpose
d8681a26d74e3629e465eb8b - Fix Shopify Product URL Duplication (Within-Collection Paths)
97c5e148f6398997e725caf1 - Rebuild Shopify Breadcrumbs With a Meta Field After URL Fix
c45f3f4a4121a58752446fa7 - No-Index Auto-Generated Tag, Vendor, Type, and Utility Pages
9098b567f5957016219815d1 - Custom robots.txt on Shopify: Block Low-Value Pages
4c936159bddbfdbdbae0b3e8 - Manage Variant Duplication: Merge or Canonicalize
abd78e24fb447afb7e4139bb - Redirect Deleted Products to Preserve Redirect Path and Link Equity
9dc7ea365326d74c8304e2a7 - Remove Pages from Shopify Sitemaps Correctly (Avoid the Hidden SEO Trap)
15208e629d08181d341e5309 - Implement Product, Article, and Breadcrumb Structured Data
6223d92e1e72aa84b8671111 - Posture Site Speed: Avoid Bloat Rather Than Optimize
1a7d18d205edbff4bd672c43 - Choose Lightweight Themes and Cut Hero/Grid Bloat
3472ce4f007f429b8b04d715 - Optimize Image Format and Compression for Speed
00a2fbad5f22d9e312a180e2 - Lazy Load Offscreen Images on Collection Pages
959f69db4f65295b23d745a7 - Audit and Remove Unused App Code from Themes
504893b96bd4ec77ee263cef - Conditionally Load App Scripts by Page Type
ac5223c74551ca2115398b36 - Minify JavaScript and CSS to Reduce File Size
96f67f5ea6a721114ca83fc8 - Speed up a Shopify store by minifying CSS/JS
5fe9759a8a5c58945bfc97f1 - Async and defer non-essential scripts
edcb1a9b8cef89977068ffc5 - Use resource hints and preload to cut load times
6ebefab0aa297d379ef4a0c1 - Frame keyword research around customer thought process, not just volume
7fe6a9f64adfa67e0ed77ecf - Build a topical map instead of a flat keyword list
6f239699ac8dfc92a0619d9c - Decide page type by what ranks in positions 1-3
40bc9625a6913038aa5ba660 - Prioritise bottom-of-funnel pages first on Shopify
69c5a2ad65bbef2fb7b591d9 - One topic per page, many secondary keywords per page
6d5b32906d7069f1879434fe - Assign URL types: collections for options, products for specifics, homepage for breadth
f1130887a71fa3b6e62a4b9d - Derive site structure and internal links from the topical map
e6d59dcb5f233d8616f9c4a9 - Spot and fix keyword cannibalisation
607cf326f1ba5c4699764da1 - Expand broad topics into subcollections without creating redundancy
626394ae29f2b086bf43650e - Stick to your core topic and avoid diluting relevance
5e99325d5f635f7f3259a7df - Optimise the main menu for fewer clicks to product
1dfb2e52dbf99587e84e6812 - Make the homepage a hub for high-volume collections
6637fae5f44a5dc9e06deffe - Handle faceted navigation correctly on Shopify
c463c6a96f1d0dc3798edcc3 - Build product grids for both users and crawlers
2b98fa10af38cabf43b9a5f0 - Add breadcrumbs, tag-style links and related products to product pages
d22a5b9d1e858eb648b1636e - Optimise the three key on-page elements on collection pages
dabcaf2093cb596556d38119 - Decide what to do with a page: publish, refresh, or quick-win
ce1613cde42d81279b822692 - Shopify Collection Page Content Stack
95c668e0b9559e9753422a2d - Splitting One Shopify Description into Short and Detailed Sections
99f0bb9ef6050ba191cd8890 - Why Add Unique Content to Hundreds of Collection Pages
3896ccc0c89334e67c81f822 - Product Detail Info and Faceted Navigation on Collection Pages
4d35e548f749de33a058060e - FAQ Accordions on Collection and Product Pages
83dbf0409f3c2e103572b686 - Featured Reviews on Collection Pages
704b4171081de3383b87d889 - Deciding Whether to Rank a Product Page vs a Collection Page
496c62ba9cac375aa1c7f262 - Evaluating Search Volume Before Investing in Product Page SEO
1fdc94e244375acb7176da4a - Handling Discontinued and Out-of-Stock Product Pages
c758a7b81cac21ba6805c27f - Product Page Content Template for Shopify SEO
50cbdf6d8b19919bfcef9227 - Product Page Images, Alt Text, and XML Sitemap
55dc25234b4734355a448307 - Product Page Structured Data: Product, Review, FAQ, Breadcrumb
43028e061152821936b7db44 - Breadcrumbs, Tag-Style Category Links, and Related Product Modules
45f79a195c33a9a4f37d68f0 - When a Shopify Store Needs a Blog
6731423ab54b0d74aa8ce9ab - Optimizing Blog Post Titles, H1, URL, and Meta Description
869cf61bff5ab4f276eb64e6 - Writing Blog Content That Beats What Ranks
84d4795d239e115908e1755f - Embedding Product CTAs and Internal Links in Blog Posts
435ce96184bc1289a089644e - Building Topical Authority One Cluster at a Time
c26fdb13c1b0e4617d95fe95 - What Ecommerce Link Building Is and Why It Matters
9ef468a1aa73c1f2dd783787 - Foundational Links for a New Ecommerce Site
4143ac10dcfc827c8d06e0ce - Map the five link-building types to an ecommerce backlink mix
d959e63d97697c9f901f26ba - Judge a backlink's quality before pursuing it
be35a345338047d5fdee9aab - Run a link-gap analysis and set a monthly link target
102c5f4bc1f8a23733e7e34f - Screen spam links with a five-point checklist
d00b480b316f99d3ba90ba0d - Build foundational links and citations as the base layer
3cf4abf037ab228668508857 - Prioritize low-hanging-fruit collection pages for links
931c46ea636211cb5e2de4c9 - Prospect link targets by scraping competitors' guest-post backlinks
205cf1bbe6746b987146f1a7 - Find contact details for link prospects
ed27a5301c834b403728978a - Write outreach subject lines and bodies that get opened and answered
6e04ce7fcb0e6e992cca55cf - Warm Up Cold Outreach Sending Accounts Before Guest Post Pitching
79c14ba1ded5786ffb254117 - Make Guest Post Pitches Unique Instead of Reusing a Template
cb6fea298ce485870aff6c5c - Close and Negotiate the Guest Post Link, Then Run Final Vetting
d3cac352bc44bd7894ba1aaa - Write a Guest Post That Fits the Host Site's Audience
cfd93f4f1fcb55309e397afd - Place Guest Post Anchors Naturally and Near the Top
fab6f93fabc44c52b2854ec5 - Diversify Anchor Text and Mirror Competitor Backlink Profiles
3490d57698e058e5e7f59d3b - Run Final Checks After a Guest Post Goes Live
3a7d9b1b9fd92e369f5e2f03 - Evaluate relevant link inserts without assuming faster rankings
e0058ce635d65c8ac3973403 - Pitch ecommerce expertise to journalist sourcing requests (setup)
493daec89c204aebbbf182da - Pitch ecommerce expertise to journalist sourcing requests (writing answers)
7f70083e00d51f989d6300f7 - Pitch ecommerce expertise to journalist sourcing requests (tracking)
