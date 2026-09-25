# SEO and search (15-SEO-search) playbook

version: 2.0-draft  |  date: 24 Sep 2026  |  sources: 16  |  cards: 420  |  built from: sources/*.md

## 0. How to use this playbook

**Ecommerce first.** This playbook is for an ecommerce store, not a generic website. Load section 3.0 first: it ranks the levers that matter most for a store (money pages, technical floor, branded search, catalog shape, and so on) before any group-level rule. Store-type conditions, such as catalog size, AOV, subscription vs one-off, marketplace exposure, physical location and region, decide which rules in the groups below actually apply to a given brand.

**Who runs it.** The SEO agent for an ecommerce store. It decides whether organic search is worth the store's time, builds the keyword map and site architecture, writes the page briefs for collection and product templates, runs the technical audit, plans blog content and links, reads Search Console every month, and reports organic revenue. It works on Shopify first (sources 02, 06, 07, 14, 15 are Shopify-specific), on any CMS for the general rules, and it hands depth on speed to 08-SPD and depth on AI answer engines to 16-AEO.

**What the sources are.** Almost every source is a vendor demo, an agency sales funnel or an affiliate video. Source 08 is a paid Semrush partnership. Sources 09, 10 and 11 are Surfer-sponsored. Source 07 carries an SEO Ant discount code. Source 04 is the Rankability founder demoing his own tool. Source 03 has affiliate links for DataForSEO, Machined AI and a link vendor. Source 12 promotes Arvo and a scheduler. Sources 02, 06, 13, 14 and 16 end with a pitch for an agency, a course, a mentorship program or a keyword product. Source 01 opens with a sponsored certificate. Source 05 gates its main template behind a community. Section 12 rates each one. Treat every tool recommendation as a lead to check, every case result as a story, and every threshold as a presenter heuristic unless section 6 says otherwise.

**Card-writer corrections.** Several rules in this playbook come from the card layer, not from the presenters. The most important: any paid or sponsored link placement must carry `rel="sponsored"` or `rel="nofollow"` (added on sources 01, 05, 09 and 13; no presenter said it), most sites never need to disavow anything (added on source 01), Google can render JavaScript so static generation is not a ranking requirement (added on source 05), Google does not read `llms.txt` (added on source 08), and templated near-duplicate pages carry doorway risk (added on source 03). Each is marked where it appears.

**Which sections to load for which task.**

| Task | Load |
|---|---|
| Decide if SEO is worth it for this store | 0, 1, 3 (group A), 6, 7 (7.1, 7.5), 9 |
| First audit of a store (technical) | 3 (groups I, J), 4 (P1, P2, P13, P14), 5 (5.1), 6 |
| Keyword map and topical map | 3 (groups B, C), 4 (P3, P4, P5), 5 (5.4), 7 (7.6, 7.20), 9 |
| Site architecture spec (Shopify) | 3 (group D), 4 (P2, P4, P12), 5 (5.1), 7 (7.7, 7.12) |
| Collection page brief | 3 (groups D, E), 4 (P6, P8), 5 (5.2), 7 (7.9, 7.10) |
| Product page brief | 3 (group F), 4 (P7, P8), 5 (5.3) |
| Blog and buying guides | 3 (groups G, H), 4 (P9, P10, P11), 5 (5.7), 7 (7.1, 7.9) |
| AI-assisted content production | 3 (group H), 4 (P10), 5 (5.7), 11 |
| Link plan and prospect screening | 3 (group L), 4 (P15 to P18), 5 (5.5), 7 (7.2, 7.3, 7.15) |
| Monthly Search Console read and report | 3 (group N), 4 (P19 to P21), 5 (5.6), 9 |
| Traffic drop or falling clicks | 4 (P20, P21), 5 (5.6), 7 (7.18) |
| AI search visibility (light pass) | 3 (group M), 4 (P22), then 16-AEO |
| Vetting an agency, freelancer or tool | 3 (group O), 4 (P23), 12 |
| 30-day or 90-day plan | 3 (group A), 4 (P24), 9 |

**What the agent must fetch before acting.**

- From the brand record: platform and theme, catalog size and structure (collections, subcollections, products, variants), margins and AOV, paid ad spend and channels, physical locations if any, the brand's voice document and banned words, real product photography, reviews and testimonials, existing keyword targets, who owns theme code, and whether Search Console, GA4 and any SEO tool are connected.
- From the data layer: Search Console clicks, impressions, CTR and position by page and query for 16 months; the Pages (indexing) report; GA4 organic sessions and purchase events by landing page; current rankings for money keywords; backlink profile and referring domains; competitor domains.
- From the web: the current Core Web Vitals set and thresholds (sources still name FID; INP replaced it in March 2024); current Google guidance on sponsored and nofollow attributes, doorway pages and site reputation; Search Console's current property types, quotas and generative AI report; whether each named tool still exists and what it costs; the live SERP for every keyword before a page is built. Section 10 lists every item.

**Hard rules for this agent (ecomOS overrides, they beat any source).** No invented claims on any page. No paid links, link swaps for discounts, private blog networks or any placement meant to pass ranking value; a sponsored placement is allowed only when disclosed and marked `rel="sponsored"`. No undisclosed promotion on Reddit, forums or communities, and no parasite pages on third-party domains that pose as editorial content. No incentivised reviews: no discount, gift or entry in exchange for a review. Reading level below tenth grade on every page. Real product photos where accuracy matters; no stock or generated images on product or collection pages. AI-generated copy passes a human quality gate before it reaches a client page. Do arithmetic in code, not in the model. Meta is read-only and paid search belongs to 12-GAD.

## 1. Scope and outcomes

**What this domain covers.** Organic search for an online store: how search engines crawl, index and rank; query intent and reading a SERP; keyword research (tools, volume and difficulty gates, clustering, money pages first, topical maps); site architecture (collections, subcollections, products, variants, filters, tags, URLs, Shopify duplicate paths, breadcrumbs, internal linking); on-page templates for collection and product pages (titles, metas, headings, copy, images, schema, FAQs, reviews); blog and buying-guide content (when it is worth it, formats, refresh); technical SEO (crawl, index, canonicals, redirects, sitemaps, robots.txt, JavaScript rendering, Search Console reports); link building and what Google forbids; the overlap with AI answer engines; measurement and monthly reporting; AI-assisted workflows with human gates; vetting vendors and agencies.

**What it does not cover.** Speed and Core Web Vitals in depth (08-SPD: this playbook keeps only the rules that decide when speed is an SEO problem). AI answer engines in depth (16-AEO: this playbook keeps the overlap and the routing rule). Paid search and Shopping (12-GAD). GA4 setup and attribution (06-MEA: this playbook keeps the organic reads). Landing page design (07-LPG). Blog and social content operations beyond SEO (13-ORG). Amazon (22-AMZ). Bot access and agent security (23-SEC). Store setup fields that are not search-facing (05-SET). Local SEO is covered only as a pointer: sources 01, 03 and 05 give Google Business Profile steps, but a pure online retailer has no listing to claim.

**Business measures it moves.** Organic search revenue (the KPI 3 sources put first). Non-branded organic clicks and impressions. Rankings for a shortlist of money keywords. Count of indexed money pages. Organic add-to-cart, checkout and purchase events. Share of AI answers that name or cite the brand (measured, not promised). Cost avoided: source 03's example values a keyword at CPC x clicks ($17.32 x 1,000 = $17,320 a month), an illustration, not a forecast.

## 2. Inputs the agent needs

| Input | From where | Required or optional | Why |
|---|---|---|---|
| Platform, theme, who edits theme code | brand record | required | Shopify fixes in P2 touch Liquid files; other platforms need different steps |
| Catalog tree: collections, subcollections, products, variants, SKU counts | brand record, data layer | required | decides collection vs product targets, facet rules, variant canonicals |
| Margin, AOV, paid spend, branded search volume | brand record, data layer | required | R1 (is SEO worth it), R10 (branded capture) |
| Search Console access (Domain property) | data layer | required | every read in group N; without it the agent is guessing |
| GA4 organic sessions and purchase events by landing page | data layer | required | organic revenue KPI, funnel leaks (R131) |
| Keyword tool access (Semrush, Ahrefs, DataForSEO, Keyword Planner) | user | required, any 1 | volume, difficulty, intent labels (R22, R23) |
| Crawler (Screaming Frog free tier up to 500 URLs, Sitebulb, Semrush Site Audit, Ahrefs) | user | required, any 1 | technical audit (P1, P13) |
| Backlink profile and competitor domains | data layer, user | required for link work | gap analysis, prospect screen, disavow decision |
| Brand voice document, banned words, reading level rule | brand record | required for any writing | AI drafts must match voice (group H) |
| Real product photography and specs | brand record | required for page briefs | ecomOS photo rule; specs feed the product template |
| Reviews and testimonials (unincentivised) | brand record | optional | featured reviews on collection pages, AggregateRating schema |
| Existing content inventory with URL, target keyword, status | data layer, user | required for refresh work | topical map status column (R28), refresh review (5.7) |
| Physical locations, if any | brand record | optional | Google Business Profile only applies with a location |
| Named competitors that outrank the store for money terms | data layer, web | required | R9: SEO competitors, not business competitors |
| Live SERP for each target keyword | web | required before any page brief | R16: page type follows what ranks |
| Current Google guidance on sponsored links, doorway pages, Core Web Vitals | web | required, re-check quarterly | section 11 staleness |
| Tool prices and plan limits | web | optional | section 6 marks vendor numbers; prices drift |
| Access to AI answer engines for manual checks | web | optional | R121 light check, then 16-AEO |

## 3. Decision rules

Numbering runs across all groups. Each rule gives the rule, its condition, the mini playbooks that support it (by number), conflicts (pointing to section 7) and card ids. "Sources: 13" alone means 1 practitioner's view, not a law. Where sources give different numbers, the rule keeps the strictest condition and section 7 keeps the disagreement.

### 3.0 Ecommerce priority order

Rank levers in this order for any store. Conditions by store type decide which ones apply.

1. **Money pages before anything else.** Collections and products convert; blogs do not. Every other lever waits. -> R4, R5, R67, conflict 7.1.
2. **Technical floor, once, sitewide.** Crawlable, indexed, no broken links, usable mobile UX. A blocked money page beats every content or link gain. -> R86, R87, R88.
3. **Protect branded search.** Any store running paid ads must hold position 1 for its own name and product names, or ad spend leaks to a competitor. -> R10.
4. **Catalog shape decides the template weight.** 50+ SKUs: collections likely carry most organic revenue, invest there first. Hero SKU or thin catalog: the product page and its cluster is the money page; do not force an empty collection layer. -> R58, R59, R37.
5. **Set the volume floor from AOV and catalog size, never a guru's number.** A niche or high-AOV, low-frequency ("considered purchase") store needs a lower floor and more patience than a low-AOV impulse category. -> R23. `[general practice]` on the considered-purchase half; the playbook gives only the catalog-size half.
6. **Marketplace-heavy categories change the target.** Where Amazon or another marketplace owns first-page or AI-citation slots, list there instead of fighting for a standalone page. -> R11.
7. **Concentrate on 1 category or cluster at a time, sized to the catalog.** A multi-category retailer picks 1 category per quarter; a hero-SKU or subscription store applies the same discipline to its 1 money page and cluster. -> R6, R68.
8. **Subscription and considered-purchase stores need the comparison and trust layer earlier.** These buyers read alternatives and reviews before converting; build that content sooner than a low-AOV, one-off store would. -> R65, R69, conflict 7.1. `[general practice]`.
9. **Local-only levers apply only with a physical location.** Google Business Profile, citations, NAP: skip for a pure online store. -> R138, R116.
10. **Mobile-first stores (most India-market and mobile-heavy US catalogs) should treat mobile UX as the primary check, not an equal-weight item.** `[general practice]`.
11. **AI answer-engine visibility rises for comparison-heavy, considered or subscription categories; matters less for one commodity SKU.** -> R118, R119, R120.
12. **Link building is last, sized to the catalog's link gap, not a fixed quota.** No source conditions it by store type beyond authority level. -> R104, R105, R111.

Load this block first; the groups below are the detail.

### Group A. Strategy, scope and order of work

**R1. Do SEO only where search demand already exists and margin can pay for it.** Condition: before any SEO budget. SEO captures existing demand; it does not create demand for a new product type (source 14). Check that the main category terms have real volume and commercial intent, and that AOV and margin can absorb months of content and link work. Source 14 gives no numeric floor for margin or AOV; source 09 adds that a keyword without a conversion path is vanity traffic. Sources: 14, 09, 06. Cards: [6d35da604075] [03569978ba18] [f8b0ca8237ae]. [needs brand data: AOV, margin, category search volume]

**R2. Never promise a launch, restock or seasonal-campaign date off an SEO timeline; a Q4 promotion planned around an unranked page is the most common way this rule gets broken.** Condition: every SEO proposal and report. Source 01 refuses to promise a timeline. Source 06's wine client saw momentum only after 12 to 13 months. Source 03 expects no link ROI for 3 to 6 months. Source 11 puts several months of work per cluster plus more months for results. Source 13 calls "6 to 12 months" a myth, but its own cases run from under 100 days to 11 months and are self-reported. Source 11: anyone who guarantees #1 is beyond a marketer's control. Sources: 01, 06, 03, 11, 13. Conflict on timelines: 7.17. Cards: [5437c6f5b94e] [f8b0ca8237ae] [691b416017c3] [1e7d8c5e6402] [41463bbdbca1].

**R3. The KPI is organic search revenue, then non-branded clicks and money-keyword rankings; traffic and rankings alone are vanity.** Condition: every report. Source 13's case: 2 agencies at about $5,000 a month each for 2 years, traffic and blog output looked fine, organic revenue never passed about $2,000 a month. Source 03 names over-celebrating rankings without conversions as his own past mistake. Source 09: have a business goal, not an SEO goal. Sources: 13, 09, 03, 10. Cards: [7cc511272fe0] [28f51e6a77cb] [fb7381a080bf] [dd8f0c00b989].

**R4. Money pages first: collections and products before any blog post.** Condition: any store, any stage. 7 sources say it in some form. Source 02: collections and products convert directly and pay back fastest. Source 09 names the failure pattern: 10 informational posts first, then nobody buys because there is nowhere to convert. Source 13's case: about 40 new collection pages in 3 to 4 months took organic revenue from about $2,000 to over $10,000 a month (self-reported). Source 06: collection page before the product page for a hero term. Sources: 02, 09, 13, 14, 16, 12, 06. Conflict on whether blogs matter at all: 7.1. Cards: [40bc9625a691] [28f51e6a77cb] [4ebd0ef27d61] [8512538fd23a] [00ce29e07738] [e879133cad0d].

**R5. Order of work: technical floor, then money pages, then 1 content cluster, then links.** Condition: a store starting or restarting SEO. Source 02 makes technical SEO the mandatory first step (crawl cost). Source 13 limits the technical floor to 4 items (crawlable and indexed key pages, no broken links, usable mobile and desktop, clear hierarchy). Source 09's 30-day plan: Search Console and keywords in week 1, the most important money page in week 2, the first cluster piece in week 3, outreach and monitoring in week 4. Source 09 and 11: no outreach until 10 to 15 good pieces exist. Source 08 runs the same as a loop: research, organize, fix the foundation, track. Sources: 02, 13, 09, 11, 08. Conflicts on how much technical work: 7.4. Cards: [6b922910be56] [6eb7236440e6] [63c02d6a7770] [1293de3e1c27] [e8139b1b3363].

**R6. Do sitewide hygiene once, then concentrate content and link effort on 1 category or cluster at a time.** Condition: growth-stage work after the technical floor. Source 04 attacks 1 category from the main menu for about 90 days (sometimes 1 to 2 quarters) and says spreading effort across every category gives "a centimeter in each direction". Sources 02 and 09 build 1 cluster fully before the next. Sources 01, 02 and 09 still expect baseline crawl, index and template hygiene across the whole site. Sources: 04, 02, 09, 11. Conflict on how far to concentrate: 7.5. Cards: [03e2459fa1f6] [618a252af117] [435ce96184bc] [1e7d8c5e6402].

**R7. Do not build content for a product category the store does not sell just because it clusters near a covered one; every page in the map must map to a real collection or product.** Condition: content and collection planning. Source 02's own agency branched early, ranked briefly, then lost rankings on the original topic when Google recrawled. Source 09: working down a volume-sorted list across unrelated topics spreads authority thin. Sources: 02, 09. Cards: [626394ae29f2] [435ce96184bc] [618a252af117].

**R8. Run the cycle against the catalog: validate keywords for the categories on sale or in season this month, update those pages first, then publish and get links.** Condition: ongoing operation after setup. Source 06's team runs it on a fixed calendar day; source 08's loop is the same 4 steps with tracking. Re-evaluate each tracked keyword: source 06 gives it about 6 months before adding support content or swapping it. Sources: 06, 08. Cards: [6c5f723270e6] [d0068f9ba972] [6d1a4ae6d1e0] [e8139b1b3363].

**R9. Benchmark only against SEO competitors that outrank you for your terms and sell what you sell; skip the giants.** Condition: competitor research and link prospecting. Source 01: rivals below you contain no useful gaps. Source 02: SEO competition differs from business competition, and Amazon, Walmart, Target and Ikea are excluded from prospecting. Source 14: if only a giant like Nike ranks, the term is too competitive. Sources: 01, 02, 14, 08. Cards: [30500e1bfd7e] [931c46ea6362] [0120e72eaf94] [e656b0848811].

**R10. Hold position 1 for your own brand name and product names; paid ads create branded searches that a competitor can capture.** Condition: any brand running paid ads, and every monthly read. Source 03: if you do not rank first for your brand, that is a real problem. Source 14: people see an ad, do not click, then Google the brand later. Source 10: branded position is almost always 1 and says nothing about competitive strength, so report it separately. Sources: 01, 03, 14, 10. Cards: [a7537cfd6597] [0e6da3acc1cc] [0363a4df755b] [dd8f0c00b989]. [needs brand data: Search Console brand queries and positions]

**R11. Treat marketplaces as search engines and as citation sources; list the product where the SERP or the AI answer already cites a marketplace.** Condition: categories where Amazon or another marketplace holds first-page or AI-citation slots. Source 01 says about half of product searches start on Amazon (unsourced). Source 04's example brand sold on Amazon but withheld its creatine line, a self-inflicted gap. Depth on Amazon lives in 22-AMZ. Sources: 01, 04. Cards: [9456f3ecb153] [1cdb6f4058e5] [6ea0882a8403].

**R12. Tool numbers are guides, not truth; never compare figures across tools; domain authority scores are vendor metrics.** Condition: every use of volume, difficulty, authority or traffic estimates. Source 01's example: the same site showed Ahrefs traffic of about 4,000 to 5,000 vs Semrush 9,800, and DR 44 vs Authority Score 35. Source 03: a tool showing 0 volume does not override niche knowledge, and DA is a vanity metric. Source 08: Authority Score is Semrush's own formula. Source 13: Keyword Planner gives ranges, and the 10K to 100K range is too wide to plan on. Sources: 01, 03, 08, 13. Cards: [b6d9e2525ff1] [b2ab9292f6ba] [fb7381a080bf] [3dd3ec99006f].

**R13. Knowing a tool is not knowing SEO, and no tool or vendor can promise a rank.** Condition: choosing tools, agencies and content platforms. Source 13's analogy: knowing Robinhood does not make a trader. Source 03: do not trust "our content will rank you number one". Source 11: prioritization, not execution, is the hard part. Sources: 13, 03, 11. Cards: [3dd3ec99006f] [b95c25b2d3c8] [41463bbdbca1].

**R147. List every eligible product in Google's free Shopping listings (the Merchant Center product feed) in addition to organic SEO; it is a second, no-cost slot on the same SERP.** Condition: any store on a platform that can generate a product feed. `[general practice]` No library source; verify against brand data before use.

**R148. Build and refresh the pages for a seasonal or promotional category ahead of the season it sells in, not after; tie the content calendar to the inventory calendar, not to a fixed publishing day alone.** Condition: any store with seasonal or promotional SKUs. Source 01 flags a seasonal push as a case for the fixed cycle (R8, R2); source 03's principle 7 makes the same point without a card. Sources: 01, 03. Cards: [5437c6f5b94e].

### Group B. How search works and query intent

Moved to Appendix A: R14, the crawl-index-rank diagnostic sequence (general search mechanics, section A.1).

**R15. Classify every query by intent and match the page type to it.** Condition: before any keyword is assigned to a page. Four classes: informational (learn), commercial (compare), transactional (buy), navigational (reach a brand). Source 03 says 2 buckets (transactional and informational) are enough to start. Informational queries go to blog or guide pages; transactional and commercial queries go to collection and product pages; a blog post ranking for a buy query rarely converts, and a bare product page ranking for a learn query bounces. Sources: 01, 09, 03, 05, 07, 06. Cards: [cdfba6f37765] [f32610667b5f] [b2ab9292f6ba] [4cf93efa0b3e] [6c1d36ed15c3] [33805e3f1916].

**R16. Read the live SERP before building any page; the page type follows what already ranks.** Condition: every target keyword, re-checked when a page is refreshed. Source 02 reads positions 1 to 3. Source 09 reads the top 10 organic results and their format. Source 11: if 5 or more of the top results share a format, build that format; if mixed, pick the format your authority can win. Source 14: if other collection pages rank, a collection can rank; if only giants rank, skip. Source 05: skip terms whose top results are other businesses or job seekers. Use an incognito window. Sources: 02, 09, 11, 14, 05, 01. Cards: [6f239699ac8d] [f32610667b5f] [8786029ccf04] [0120e72eaf94] [4cf93efa0b3e] [1bae7bf49f42].

Moved to Appendix A: R17, reading SERP features such as AI Overviews and video carousels (general search mechanics, section A.1).

Moved to Appendix A: R18, long-tail-to-head-term theory, kept store-specific in the R23 keyword gate and R58/R59 (section A.1).

**R19. Answer the query's intent in the first screen; a shopper who clicks back and picks another result is a signal against the page.** Condition: any page targeting a query. Source 01 calls this pogo-sticking and says to put product name, price and the answer in the first visible band. Source 03: one clear headline naming the offer and 1 primary call to action above the fold. Sources: 01, 03. Cards: [6468710f6f02] [3ddb50cffb54] [abc864090582].

**R20. When enterprise homepages own a commercial term, a roundup or comparison page can be the way in.** Condition: commercial keyword whose SERP is mixed and includes listicles. Source 11's example: GetAccept outranked DocuSign and PandaDoc homepages for "electronic signature software" with a tested, screenshot-backed roundup. Trade-off: some readers go to listed competitors. Sources: 11, 04. Cards: [be8eb0ae5390] [5346127695b9].

### Group C. Keyword research for stores

**R21. Score every candidate on demand, fit, intent and difficulty; keep the ones that pass all 4 and plan deliberately for the rest.** Condition: any keyword list. Source 09's Sweet Spot framework; source 01's version is volume plus difficulty plus intent plus relevance. Keywords that score on 1 attribute only are deprioritized or used as top-of-funnel with a conversion path (R34). Sources: 09, 01. Cards: [03569978ba18] [017caafa9aba].

**R22. Mine free sources before paying for a tool: Search Console queries, autocomplete, People Also Ask, "People also search for", Reddit phrasing, Google Keyword Planner and Trends.** Condition: every research pass; the paid tool comes after. Source 09 calls Search Console the most accurate source because it is Google's own data. Source 07's routine: Keyword Planner (needs a Google Ads account), Trends related queries, autocomplete, and a competitor URL in Keyword Planner's "start with website". Source 13's stack is Semrush, Keyword Planner and Screaming Frog only. Sources: 09, 07, 13, 01. Cards: [0648fb2c0ce2] [2fc78c801ced] [3dd3ec99006f] [ea2d1dfe6516] [09c9050e0d04].

**R23. Gate by difficulty relative to the store's authority, by intent fit, and by a volume floor set per catalog and margin; do not copy any presenter's single number.** Condition: filtering a keyword list. The sources give 6 different gates: source 01 KD under 40 and about 500 searches a month (the card says do not impose 500 on every store); source 05 KD 30 or under and at least 100 a month; source 06 commercial flag plus over 1,000 a month plus KD under 40 plus CPC over $1; source 08 KD 0 to 49 plus at least 5,000 a month; source 14 KD under 35 for collection variants; source 09 gives no numbers. Merged rule: for a new or low-authority store keep KD under 30 to 40 on whatever tool is used; require the intent to match the page type; set the volume floor from the catalog (a niche store with 50 products cannot demand 5,000 a month) and record the floor in the keyword map. Sources: 01, 05, 06, 08, 14, 09. Conflict: 7.20. Cards: [017caafa9aba] [e3f640eda70f] [33805e3f1916] [1449fb3da4a7] [0120e72eaf94] [010063066fd9].

**R24. Look for "gold nugget" terms with near-zero difficulty and real volume, then sanity check them.** Condition: reading a tool export. Source 03's example: "home equity agreement" at 14,800 a month and near-zero difficulty. A null-difficulty term that contains a real brand name is not easy. Source 08's example: "Is olive oil a seed oil?" at 14,800 a month and low KD. Sources: 03, 08. Cards: [d2b1c9b1538f] [1449fb3da4a7].

**R25. Use CPC as a commercial-intent signal and a competitiveness proxy, not as a filter on its own.** Condition: choosing money keywords, or when the tool has no difficulty score. Source 06 requires CPC over $1. Source 13 uses Keyword Planner's low-end bid as a proxy for organic competition when no KD exists. Source 05 sorts by CPC to surface service and city money terms but calls a $700 CPC "bad data" (typical range $3 to $20 in his niche). Source 03 values a keyword at CPC x estimated clicks. Sources: 06, 13, 05, 03. Cards: [33805e3f1916] [3dd3ec99006f] [ecfb3aa47dee] [d2b1c9b1538f].

**R26. Sweep the list by hand and remove competitor brand names, mascots, job-seeker queries and anything the store does not sell or ship.** Condition: after every tool export, before clustering. Source 05's rejected examples: "Hydrojet Plumbing", "Plumb Bob", "Zeke the Plumber". Source 01: never chase a competitor's keyword for a product you do not sell or a region you do not serve. Sources: 05, 01, 03. Cards: [4cf93efa0b3e] [30500e1bfd7e] [5f61c8804623].

**R27. One topic per page: 1 primary keyword in title, H1 and URL, plus a cluster of secondary terms in the copy.** Condition: every page. Source 02: 1 primary and many secondaries, with genuinely different topics (for example colours) on separate pages. Source 06: 3 to 5 cluster terms per hero keyword. Source 07: 1 main plus 2 supporting per page. Source 05: root keyword in the first 100 words plus variants. Source 08 clusters by SERP overlap so 1 page serves 1 cluster. Keyword stuffing of 1 term across pages is a mistake (source 06). Sources: 02, 06, 07, 05, 08. Cards: [69c5a2ad65bb] [88385c2e69c2] [2fc78c801ced] [ef4ca0c529fd] [041545a9412a].

**R28. Build a topical map, not a flat list: cluster, page type, primary keyword, secondaries, URL, volume, current rank, status.** Condition: any store with more than a handful of target terms. Source 02 calls it "keyword research on steroids" and derives site structure from it. Status values: published, needs refresh, quick win, needs publishing. Source 08's Keyword Strategy Builder does the clustering and hands the first 5 clusters to the month's calendar. Sources: 02, 08. Cards: [7fe6a9f64adf] [dabcaf2093cb] [041545a9412a].

**R29. Run a keyword gap against SEO competitors and pursue only gaps for products you sell; gaps are most winnable where your link profile is at least as strong.** Condition: after the own-site research. Source 08's Missing tab (they rank, you do not) and Weak tab (you rank far below). Source 01's example: 931 common keywords vs a competitor's 2,953, with a "red light therapy mask" term the client did not cover. Sources: 01, 02, 08, 03. Cards: [cf900456ba0e] [44c8a0dfa878] [40bc9625a691] [72620276fe27] [5f61c8804623]. [needs brand data: own vs competitor referring domains]

**R30. Start from a shortlist of business-driving terms, then expand each into its long-tail cluster; do not run down a volume-sorted list.** Condition: keyword roadmap. Source 11: pick a shortlist by tier (brand, product terms, geo terms if local). Sources 09 and 02: expand each money term into a cluster of long-tail and question terms. Sources: 11, 09, 02. Conflict on shortlist vs broad long tail: 7.6. Cards: [41463bbdbca1] [618a252af117] [7fe6a9f64adf].

**R31. AI models cannot supply keyword data; pull volume and difficulty from a tool, then use AI to organize the export.** Condition: any AI-assisted research. Source 05's bad example: "give me 20 keywords for plumbing" returns guesses. Source 03 feeds raw CSV exports into a chat with business context and asks for a money page, subpages and article ideas, then answers the model's clarifying questions. Sources: 05, 03, 09. Cards: [e3f640eda70f] [5b3f8191a572] [fb8f4b373003].

**R32. Mine questions for FAQs and guides: People Also Ask, question tools, and a Search Console regex on who, what, when, where, why, how, can, does.** Condition: building FAQ sections and content ideas. Source 10's rule: where no page answers a question the site already surfaces for, add an FAQ or a page. Source 03's example: 1 seed term produced 558 questions; pick 3 to 4 per cluster. Sources: 01, 02, 03, 10, 07. Cards: [16bdb59b661a] [4d35e548f749] [c88f9d623f64] [ad660f81d67a] [2fc78c801ced].

**R33. Re-run research after catalog changes and re-check tracked terms on a schedule.** Condition: ongoing. Volumes, difficulty and rankings shift (source 01); source 06 re-evaluates monthly and gives a keyword about 6 months before changing course. Sources: 01, 06. Cards: [017caafa9aba] [6d1a4ae6d1e0] [d0068f9ba972].

**R34. A top-of-funnel keyword is worth targeting only with a conversion path behind it.** Condition: informational terms with high volume. Source 09's example: "contract template" at about 300,000 a month feeds a template download, email capture and nurture. Source 05: adjacent higher-funnel topics for the same eventual buyer. Without a path it is vanity traffic. Sources: 09, 05. Cards: [03569978ba18] [a8ed94c10b20].

**R35. Audit what existing pages already rank for and fix wasted content.** Condition: any store with a content history. Source 07: flag pages ranking for zero-volume or irrelevant terms and re-aim them. Source 04: assign each existing URL consolidate, upgrade or delete from Search Console data, never from gut feel. Sources: 07, 04, 10. Cards: [f70db477cc54] [03e2459fa1f6] [96052232339a].

### Group D. Site architecture

**R36. Plan the architecture before building: home, collections, subcollections by attribute, products; every page has 1 parent and a planned link path.** Condition: new store, replatform, or a catalog restructure. Source 03: "measure twice, cut once"; no structure now means months of rework. Source 02 derives structure from the topical map. Source 01: clear navigation and interlinking help crawlers and shoppers. Sources: 03, 02, 01. Cards: [3a48ad90c5ed] [f1130887a71f] [b1cc7860ad7d].

**R37. Assign URL types by query breadth: collections take broad and option-seeking buy terms, products take specific terms, the homepage takes 1 broad term that no collection also targets.** Condition: mapping keywords to pages. Source 02's example: "handheld vacuum cleaner" at about 14,000 a month to a collection; "Shark WandVac handheld vacuum" at about 490 a month to a product. Sources: 02. Cards: [6d5b32906d70] [c463c6a96f1d].

**R38. Never let a product page and a collection page, or a blog post and a collection page, target the same keyword.** Condition: always. Source 14: cannibalization "will tank your results". Source 02: an unstable ranking URL for 1 query in Search Console is the signal. Fix by enforcing 1 page per topic, not by repeating the keyword on more pages. Sources: 02, 14. Cards: [e6d59dcb5f23] [0120e72eaf94].

**R39. Split a collection into subcollections only when each split has its own search demand and its own content; never build "top rated", "on sale" or modifier copies with no unique value.** Condition: expanding a category. Source 02's good split: stick, upright, handheld and robotic vacuums, each linked from the parent. Source 14 splits "hoodies" into men's, oversized, zip, running and under $50 pages that reuse the same products, gated by KD under 35 and commercial intent. Source 04: when a broader category page already covers a modifier query, publish a blog or listicle and link it in instead of a near-duplicate category page. Reusing the same product in several collections is fine (source 02). Sources: 02, 14, 04. Conflict on template reuse vs doorway risk: 7.7. Cards: [607cf326f1ba] [0120e72eaf94] [8a447e2a6302].

**R40. Shopify filter URLs are parameter-based and not indexed; any filter combination worth ranking gets a real collection page. Add faceted navigation at about 200 SKUs.** Condition: Shopify stores with large collections. Parameter pages cannot carry unique content. Sources: 02. Cards: [6637fae5f44a] [c463c6a96f1d] [3896ccc0c893].

**R41. Noindex Shopify's auto-generated tag, vendor, product-type and utility pages ("all collections", "all products", "new products"); build a real collection for any tag topic worth ranking.** Condition: Shopify. These pages cannot carry unique titles, H1s or copy. Use `noindex, follow` per page class in theme.liquid. Sources: 02. Cards: [c45f3f4a4121].

**R42. Fix Shopify's product URL duplication under collection paths, then rebuild breadcrumbs from a metafield.** Condition: Shopify themes that link products as `/collections/x/products/y`. The canonical still points to `/products/y`, but every collection path is crawled. Remove `within_collection` from the product grid snippet; newer themes may already omit it. The fix breaks URL-derived breadcrumbs, so store each product's parent collection URL in a metafield and render breadcrumbs from it. Sources: 02. Cards: [d8681a26d74e] [97c5e148f639].

**R43. Merge variants with no separate demand into 1 product; canonicalize any variant page you keep to the primary product.** Condition: colour, size or material variants. Source 02: judge whether the variant has its own volume and could carry unique content; if not, use native variant options. Source 01: 1 canonical version of every store page. Sources: 02, 01. Cards: [4c936159bddb] [95ab0cd0f12e] [8b1855892851].

**R44. Scale the main menu to the catalog and minimize clicks to product; feature the highest-volume collections on the homepage, because the homepage holds the most links.** Condition: navigation design. Source 02's examples: MyProtein exposes subcategories directly; Blinds Style mirrors the menu on the homepage by type, colour and room. Sources: 02. Cards: [5e99325d5f63] [1dfb2e52dbf9].

**R45. URLs are short, readable and keyword-bearing; every URL change gets a 301.** Condition: every page. Strip filler words from Shopify handles and confirm the "create a redirect" checkbox before saving (source 07). Avoid CMS-generated strings (source 09). Sources: 01, 07, 09. Cards: [883a5f7521dd] [b06d74de8738] [e2547f7490bb] [e7c0a899bee0] [ce6536d71069].

**R46. Internal links are hub and spoke: the collection page is the hub, every supporting page links to the hub and to at least 1 sibling, and the links sit in body copy, not only in menus.** Condition: every page, every new piece of content. Source 04: authority accumulates at the hub. Source 14: link to a money page within the first 100 to 200 words of a post, add 3 to 5 links to related posts, use 2 to 4 word descriptive anchors, never "click here" or the brand name. Source 05: 3 to 5 internal links and 2 to 3 external links per page. Source 10: find the most-linked pages in Search Console's Links report and point links from them at priority pages. Source 09 calls internal linking one of the best effort-to-value ratios in SEO. Sources: 04, 14, 09, 11, 05, 10, 12. Cards: [91d2b64f095d] [d0d5872a02aa] [91cc4c076fd9] [1293de3e1c27] [aeeccc51cf9d] [00909ce99f85] [d03002241ed3].

**R47. Every content page carries 2 kinds of links: an outbound citation for any factual claim and an internal link to the money page it supports; money pages link out to their best supporting posts.** Condition: every blog post, guide and comparison. Source 03: a post with no internal links is "a room without doors". Source 12 closes the loop in both directions. Sources: 03, 12, 02. Cards: [205809992aba] [d03002241ed3] [84d4795d239e].

**R48. Product pages carry breadcrumbs, tag-style category links and a related-products module.** Condition: every product template. Source 02's example: Omnia Fishing links similar jigs by technique. Sources: 02. Cards: [2b98fa10af38] [43028e061152].

**R49. No orphan pages: every page you want indexed has at least 1 internal link from a crawlable page.** Condition: after any crawl. Source 01: add orphan pages to a menu or link them from a relevant article. Source 10: "Discovered, currently not indexed" often clears with internal links from stronger pages. Sources: 01, 03, 10. Cards: [86975c6c2e81] [3a48ad90c5ed] [b90f727119e2].

**R50. Keep discontinued and out-of-stock product pages live if they have rankings or traffic; swap the buy button for "shop similar" or "notify me". Redirect deleted products to the nearest relevant product or collection, never to an unrelated page, and to the homepage only as a last resort.** Condition: catalog changes. Source 01's warning example: do not send an iPhone page to a perfume collection. Sources: 02, 01, 07. Cards: [1fdc94e24437] [abd78e24fb44] [6387bf5f570f] [e7c0a899bee0].

**R51. Reuse a page template across similar pages, but give each page its own demand, its own copy and a cap on the count.** Condition: variant collections, location pages, programmatic pages. Source 03: identical layouts are not duplication if the content differs (presenter opinion; the card flags doorway risk). Source 05: no objective cap, but avoid thousands and "probably" hundreds. Source 05: ramp releases rather than publishing a flood. Sources: 03, 05, 14. Conflict: 7.7. Cards: [c6d42d7d4d1f] [ecfb3aa47dee] [e400cd54ed6c] [0120e72eaf94]. [web check: current Google guidance on doorway pages]

**R149. When a batch of seasonal SKUs turns over at once, route the whole batch through the R50 decision (redirect or keep live with "shop similar") in 1 pass, and update the collection page and internal links at the same time, not product by product.** Condition: catalog-wide seasonal turnover, not a single SKU. `[general practice]` No library source beyond R50's own cards; verify against brand data before use.

### Group E. Collection page template

**R52. The 3 core elements: title tag with the keyword first and about 60 characters, H1 equal to the target keyword, short URL that mirrors it.** Condition: every collection page. Source 02 fills the remaining title space with modifiers. Source 06 sets the collection Title field to the hero keyword. Sources: 02, 06, 07. Conflict on title length limits: 7.10. Cards: [d22a5b9d1e85] [e879133cad0d] [04a11dea33db].

**R53. Content stack: a short description of up to 2 lines above the grid, a detailed description of 400 to 1,000 words below the grid with contextual links to subcollections and guides, then FAQs and reviews.** Condition: any collection competing for a real term. Source 02: 500 to 1,000 words below the grid; a bare H1 plus grid is not enough for Google to understand the page, and big retailers auto-generate thin category pages, which is the opening. Source 06: about 400 words or more. Source 07: 100 to 400 words, and move the description below the grid rather than deleting it. Merged rule keeps 400 as the floor for a competing term and 100 as the floor for any collection. Split the single Shopify description field with a marker snippet or a read-more toggle. Sources: 02, 06, 07. Conflict on length: 7.9. Cards: [ce1613cde42d] [99f0bb9ef605] [95c668e0b955] [e879133cad0d] [04a11dea33db].

**R54. The grid shows 36 to 48 products per page, uses numbered pagination, is not rendered by JavaScript, and shows colour, a short spec and price on the tile.** Condition: Shopify collection templates. Use the native Search and Discovery app rather than a JS grid. Sources: 02. Cards: [c463c6a96f1d] [3896ccc0c893].

**R55. Add an FAQ accordion built from real People Also Ask questions and 3 hand-picked reviews that mention the keyword, in plain HTML, for shoppers first; rich-result payoff is declining.** Condition: collection and product pages. Source 02 noted FAQ rich results appearing "less and less" at recording time. Source 07 adds FAQ schema through an app or code. Reviews must be genuine and unincentivised (ecomOS override, R63). Sources: 02, 07. Cards: [4d35e548f749] [83dbf0409f3c] [161c91717301]. [web check: current FAQ rich result eligibility]

**R56. Write the search engine listing for clicks: keyword plus a call to action or differentiator in the title, and a 150 to 160 character meta description that says what the shopper gets.** Condition: every indexable page. Source 06 contrasts "natural soap" with "buy natural soap online, fast delivery". Source 03 ends the description with a CTA. Sources 07, 09 and 13 agree the meta description does not rank (source 13: "not a ranking factor since 2014"); it moves click-through. Sources: 06, 07, 09, 03, 01, 13. Cards: [469605d28f73] [e9c397c88109] [ce6536d71069] [24d491f07b87] [28b89b50c0e9] [6eb7236440e6].

**R57. Exactly 1 H1 per page, sequential H2 and H3, keywords used naturally; a custom section can silently add a second H1.** Condition: every template. Source 07: on Dawn the homepage H1 is the logo; check custom sections. Source 03: an H1 that is a tagline instead of the keyword is a mistake, and skipping from H2 to H4 is a mistake. Source 06: use Shopify's heading formats in the description field. Sources: 07, 03, 01, 06, 05. Cards: [30ee2355cc6d] [329b823585e9] [77a6f3560fde] [21a9fd61d095] [aeeccc51cf9d].

**R58. Expect collections to carry most organic revenue on stores with 50 or more products, while product pages convert at a higher rate from search.** Condition: setting priorities between templates. Source 02 claims collections drive over 80% of organic revenue on such stores and gives conversion ranges of 5% to 15% for product pages vs 2% to 5% for collections, both agency claims without a sample. Sources: 02. Cards: [45f79a195c33] [496c62ba9cac] [c463c6a96f1d]. [needs brand data: organic revenue by template]

### Group F. Product page template

**R59. Optimize and index a product page only when its name or attribute combination has search volume; otherwise put the effort into the parent collection and consider noindexing the product.** Condition: every product. Source 02's examples: made-up lure names and "silk/spandex stretch crepe sheen blue" have no volume; Soapery's rosemary and eucalyptus essential oil products do. Source 02 hedges the line itself. Sources: 02. Conflict with the "index every product" default: 7.12. Cards: [496c62ba9cac] [704b4171081d].

**R60. Product title: the product name written as a shopper searches it, with the main keyword and 1 supporting term; the title is also the H1.** Condition: every product. Source 07's example: "Sweet Honey Bomb" tells Google nothing. Source 02 bulk-templates titles for large catalogs. Sources: 07, 02. Cards: [7b577e884e60] [c758a7b81cac].

**R61. Product content stack: short description of 50 to 150 words with the product name, feature and benefit bullets, a spec table, a detailed description of 300 to 1,000 words with differentiators, ingredients or materials and use, then FAQ and reviews; the copy states explicit facts (size, colour, material, use case) and is original, not the manufacturer's sheet.** Condition: every product page you choose to optimize. Source 02: 500 to 1,000 words detailed. Source 07: at least 100 words, 300 to 400 ideal. Source 15: "insulated water bottle, green, cold drinks" beats "perfect for life on the go, in gorgeous colours". Source 01: identical manufacturer copy across sellers decays; add what the sheet does not have. Sources: 02, 07, 15, 01. Cards: [c758a7b81cac] [7b577e884e60] [43284bf0e6dd] [59f3b87a9465] [64d0c1e22a94].

**R62. Images: descriptive file names, alt text that describes the image with the product name (keyword plus product plus visual descriptor), WebP or JPEG, compressed and resized, lazy-loaded except the main image, and every product image in the XML sitemap. Real product photos.** Condition: every product image. Source 01 caps alt at 3 to 4 words; source 07's pattern is "summer bath bomb purple front". Source 09: alt text serves screen readers, so describe the image and never repeat 1 phrase across many images. Sources: 02, 07, 09, 01, 03. Cards: [50cbdf6d8b19] [c9f57a4f6f3e] [91cc4c076fd9] [6cd7c100722a] [0332997e3c20].

**R63. Collect reviews by post-purchase email with no incentive, and emit Review and AggregateRating schema; verify the review app actually outputs the markup.** Condition: every product with reviews. Source 02 suggests a discount for the next order in exchange for a review; ecomOS forbids incentivised reviews, so the ask is a plain request. Source 01: buying reviews is bad practice; genuine reviews with real images. Sources: 02, 07, 01. Cards: [55dc25234b47] [161c91717301] [cf1b90a9f8f8].

**R64. Implement Product, Review or AggregateRating, FAQPage and BreadcrumbList schema on money pages; verify it, do not assume the theme's default is complete; cross-check 2 validators.** Condition: product, collection and homepage. Source 02: a missing comma silently costs rich results; check Search Console's Shopping and Enhancements reports. Source 03: apply schema to money pages, not About or Contact, and the browser extension and the Rich Results Test can disagree. Source 15: validate against visible facts. Source 01 generates schema in a tool and deploys through GTM when theme access is missing. Sources: 02, 03, 07, 01, 15. Cards: [55dc25234b47] [15208e629d08] [1da946decc85] [fa6c5a7abc3d] [29f83e9997d5] [639b2b41168f].

**R65. Show first-hand experience on money pages and guides: original photos, real screenshots or test notes, a named author, publish and updated dates, a consistent structure across compared items.** Condition: any page competing on a commercial or comparison term. Source 11 attributes the weight of "Experience" to unnamed SEO sources, not to Google. Source 09's moat list: experience, opinion, original data, expert quotes, specific examples. Sources: 11, 09. Cards: [1512b69d5402] [b7c89ca36202]. [web check: current Google E-E-A-T guidance]

**R66. Reviews, FAQs and specs must be in the HTML at load, not injected later by an app widget.** Condition: every product template. Source 15: most crawlers see only load-time HTML; Gemini is the named exception. Source 02: no JS-rendered grids. Source 05 overstates this as "you can't rank" with client-side rendering; the card corrects it (R95). Sources: 15, 02, 05. Cards: [f8f8462498cb] [c463c6a96f1d] [df678a626742].

**R150. Treat a subscription product as a third money-page template, next to collection and product: state cadence, pause and cancel terms, and price-per-delivery on the page itself, not only at checkout.** Condition: any store selling a subscription or recurring-delivery product. Source 09's Counterculture coffee-subscription example illustrates a money page but was not turned into a template rule. Sources: 09. Cards: [28f51e6a77cb].

**R151. Give a bundle or kit its own product page with its own keyword, price and spec table; do not fold it into a single component's page or rely on an upsell widget alone.** Condition: any store selling bundles, kits or sets. `[general practice]` No library source; verify against brand data before use.

### Group G. Blog and buying-guide content

**R67. A store blog earns its place by supporting collection rankings through internal links and topical authority, and by ranking buyer-intent formats; generic seasonal and lifestyle posts do not.** Condition: deciding whether and what to blog. Source 02's example: Soapery's 210 blog posts drive under 7% of traffic directly but support collection rankings; Q for Quinn's blog drives over half of organic traffic. Source 14's 4 formats: you vs competitor, alternatives to competitor, best X for use case, buying guide. Source 13 calls informational blog traffic near-worthless for conversion. Source 04 builds reviews, alternatives and head-to-head pages. Sources: 02, 14, 09, 13, 04. Conflict: 7.1. Cards: [45f79a195c33] [9dcbebf25933] [618a252af117] [4ebd0ef27d61] [5346127695b9].

**R68. Build 1 cluster of roughly 5 to 10 pieces around 1 money page before starting the next; bridge to the next cluster with a comparison post.** Condition: content sequencing. Source 09: 5 to 10 interconnected articles per narrow topic. Source 14: 10 to 15 well-targeted posts is a full system. Source 02: cover cold press juicers fully before masticating juicers, and bridge with "cold press vs masticating". Sources: 09, 14, 02, 11. Cards: [618a252af117] [9dcbebf25933] [435ce96184bc] [1e7d8c5e6402].

**R69. Comparison content is factual and never hostile; in an alternatives list put your brand first with claims you can support and list 7 to 10 competitors; name competitors directly.** Condition: writing vs, alternatives and roundup pages. Source 04: silence cedes the comparison to competitors and AI summaries. Source 14's example: a client ranked #3 for a competitor's brand name within about a week (self-reported). Sources: 04, 14. Cards: [5346127695b9] [9dcbebf25933].

**R70. Read what ranks for a collection or product term and add what a shopper needs to decide (specs, comparisons, real photos) that the top results skip; do not just lengthen the page.** Condition: every new page. Source 09 reads the top 5 in full and records table stakes, gaps, average length and unique angles; his bar is "at least 5x better" and he cites an Ahrefs study that over 96% of pages get no Google traffic. Source 05 averages the top 3 non-forum results. Source 11: Google rewards completeness, not length. Sources: 09, 05, 02, 11. Conflict on length: 7.9. Cards: [5ff1064a03ea] [5e49646f576c] [869cf61bff5a] [bd25b3cabfdf].

**R71. The store's own moat is its product testing notes, real customer photos, sizing and fit data, and return-rate-informed advice, not generic expert quotes.** Condition: every page, and non-negotiable for health, money or safety topics. Source 03's GEO principles from a Princeton paper (claimed 40% lift, unverified). Sources: 09, 03, 11. Cards: [b7c89ca36202] [205809992aba] [7e809a393a1d] [1512b69d5402]. [web check: the Princeton GEO paper and its 40% figure]

**R72. Go deeper than the AI Overview for the query: if the page only restates the summary there is no reason to click.** Condition: any query that triggers an AI Overview. Add original data, hands-on notes, specific products, prices and dimensions, and the follow-up questions a buyer has after the summary. Sources: 09, 10. Cards: [245141abe8fc] [cc309b3d5cf7].

**R73. Refresh before you write new: a page on page 2 or 3, or losing CTR at a stable position, is the fastest win; update year-stamped titles as time passes.** Condition: monthly content review. Source 09 and 10: updating a page 2 or 3 page beats a new page. Source 10's vendor heuristic flags positions 6 to 8 for refresh and a 7-day drop for alerts (Surfer settings, not Google rules). Source 06 gives a keyword about 6 months. No source gives a fixed refresh interval. Sources: 01, 09, 10, 06. Cards: [59f3b87a9465] [9bb24c359ea8] [7a8b4ae0cd5c] [d0068f9ba972] [96052232339a].

**R74. Publish on a steady cadence the team can review, and ramp bulk releases instead of flooding.** Condition: any publishing schedule. Source 07's minimum is 2 posts a month, ideally weekly (opinion). Source 06 feeds Google monthly. Source 05 ramps programmatic pages roughly doubling by day and warns that a thousand pages a day is "an easy way to get banned" (no Google citation). The ecomOS gate: no more pages than a human can check. Sources: 07, 06, 05. Cards: [1e1031d336d4] [f5fa218ed572] [e400cd54ed6c] [021e76f554cb].

**R75. Syndicate only as a rewritten variant with the original kept canonical on your site.** Condition: LinkedIn articles, Medium, partner sites. Source 01 both warns against republishing identical articles (Panda) and recommends syndication; the cards resolve it as "customize, keep canonical". Source 04 publishes a LinkedIn variant with the year in the title and has staff share it. Sources: 01, 04. Conflict: 7.14. Cards: [b55f760c2d9e] [933f7a1d51d8] [70d7dddf86e4].

**R76. Build 1 linkable asset per category when a simple gap exists: a calculator, a definitive guide, original data.** Condition: after money pages and the first cluster. Source 09's example: "coffee to water ratio calculator" at about 500 searches and KD 8, built with an AI coding tool in about 10 minutes. Source 13 warns that earning links purely from content is the slowest path and mostly works for DR 70 to 80 brands. Sources: 09, 13. Cards: [b7d9a9c621b3] [88997600260b] [248b6ed3e810].

**R154. For a low-frequency, high-AOV or considered purchase, build the comparison, trust and reassurance content (reviews, guarantees, sizing or fit guides, alternatives pages) earlier in the plan than a low-AOV, one-off store would; these buyers research longer before they buy.** Condition: luxury or considered-purchase catalogs. `[general practice]` No library source; verify against brand data before use.

### Group H. AI-assisted content with human gates

Moved to Appendix A: R77, AI text is not penalized, low quality is (general content-ops practice, section A.2).

**R78. Ground every product or collection draft in the actual catalog feed, real specs, and existing reviews for that SKU, not a generic brand voice document alone.** Condition: before any generation. Source 04 pastes the category page plus 5 product pages as sources and expects about 20% weak ideas. Source 03 builds a tone-of-voice document from the owner's own writing and a growing negative-word list, and the prompt asks clarifying questions first. Source 05 injects voice, stats and stories from transcripts and posts. Sources: 04, 03, 05, 06. Cards: [a539906b58c4] [0b71c176e2e3] [24994938e6b4] [d625e29f8820].

Moved to Appendix A: R79, human gates on AI-assisted drafts (general content-ops practice, section A.2).

Moved to Appendix A: R80, automation caution (general content-ops practice, section A.2).

Moved to Appendix A: R81, packaging a repeatable AI workflow (general content-ops practice, section A.2).

Moved to Appendix A: R82, using AI to read exports rather than invent data (general content-ops practice, section A.2).

**R83. Stock and generated images are allowed only on informational posts where the image is illustrative; product and collection pages use real product photos.** Condition: any image choice. Source 05 auto-pulls Pexels stock; source 06 generates a hero image with DALL-E; both are local-service or blog contexts. ecomOS override applies. Sources: 05, 06. Cards: [b5a63fb310d9] [d625e29f8820].

Moved to Appendix A: R84, reading-level target and its source (general content-ops practice, section A.2); enforced as the ecomOS override R143.

Moved to Appendix A: R85, parasite SEO and why it is refused (general content-ops practice, section A.2); enforced as the ecomOS override R141.

### Group I. Technical SEO: crawl, index, canonicals, redirects, sitemaps, robots, rendering

**R86. For a store, the floor is: every collection and product meant to sell is crawlable and indexed, no broken links to product pages, mobile checkout and PDP usable, and category hierarchy clear from home to product. On a modern CMS assume you are most of the way there; do not disappear into a technical rabbit hole before pages exist.** Condition: small and mid-sized stores on Shopify, WordPress or Webflow. Source 13: an audit that pushes far past these 4 is a sales tactic. Source 09: Shopify or WordPress puts you "roughly 90% of the way there"; beginners are held back by unpublished content, not technical debt. Source 02 adds the Shopify-specific issue classes (R41 to R43) to the floor. Sources: 13, 09, 02. Conflict on how much technical work matters: 7.4. Cards: [6eb7236440e6] [e9e95368a588] [6b922910be56].

**R87. Crawl the whole site with a crawler set to mobile and JavaScript rendering, then work errors first, warnings second, notices last; a high health score does not mean a clean site.** Condition: first audit and every quarter. Source 01's example: Ahrefs health 96 of 100 with 404s, canonical mismatches, orphan pages and oversized images still present. Source 08: reduce the count, do not chase 100. Source 02 uses Sitebulb with the Chrome crawler and structured-data checks on. Sources: 01, 02, 08, 09. Cards: [86975c6c2e81] [6b922910be56] [978afa7cbda6] [e9e95368a588].

**R88. "Not indexed" is not an error; apply the test "do I want people to find this page on Google?" and fix only unintended exclusions.** Condition: reading the Pages report. Intentional exclusions on a store: ad landing pages, thank-you and confirmation pages, internal search results, filtered category pages, staging, cart, account. Unintended: a money page under noindex or a robots.txt block. Sources: 10, 01. Cards: [2d733fe61543] [38ede7630596].

**R89. Read the URL Inspection reason before acting: "Discovered, currently not indexed" needs internal links and patience; "Crawled, currently not indexed" needs a stronger page, or on a small new site, sitewide authority.** Condition: a page that should rank but does not appear. Do not keep rewriting a page when the blocker is site authority. Sources: 10. Cards: [b90f727119e2].

**R90. Request indexing only after the fix, and expect a daily quota.** Condition: new or changed priority pages. Source 05 says about 10 requests a day and about 1 day to index (his figures). Source 10 says a quota exists without a number. Sources: 05, 10. Cards: [427d9666c474] [b90f727119e2]. [web check: current Request Indexing quota]

**R91. One canonical version of every page; a canonical that points to a redirect is a bug; variant pages canonicalize to the primary product.** Condition: every template. Source 01: fix the canonical to the live final URL. Source 02: canonical via a metafield on secondary variant pages. Sources: 01, 02. Cards: [8b1855892851] [95ab0cd0f12e] [4c936159bddb] [86975c6c2e81].

**R92. Redirect every dead URL to the nearest relevant page with a 301, update internal links to the final https URL instead of relying on the redirect, and confirm the old URL no longer returns 404.** Condition: after any URL change, product deletion or migration. Sources: 01, 02, 07. Cards: [6387bf5f570f] [abd78e24fb44] [e7c0a899bee0] [883a5f7521dd].

**R93. Sitemaps: confirm the CMS already generates one before building one; set the custom primary domain first; submit it in Search Console and reference it in robots.txt; include product images; on Shopify, exclude a page from the sitemap with theme code, not the hidden toggle that also forces noindex, nofollow; ignore the priority attribute.** Condition: every store. Source 01: XML matters, an HTML sitemap is for humans only; the "500 pages need a sitemap" cutoff is arbitrary. Source 07: submit again if the primary domain changes. Source 02: Shopify does not drop canonicalized or noindexed pages from the sitemap automatically. Sources: 01, 02, 07, 05. Cards: [e1b09c7773f5] [3af48b4346f4] [0dc5d1a90cf4] [9dc7ea365326] [b3744583a367] [dc2f8bf6bb36] [50cbdf6d8b19] [8c1e01fcf839].

**R94. Robots.txt blocks crawl of admin, cart, checkout, account, internal search and low-value tag and filter paths, carries a Sitemap line, and never blocks a page you want indexed; it controls crawling, not indexing, so pair it with noindex when removal is the goal. On Shopify, deploy a custom robots.txt only after the URL duplication fix. Do not block AI crawlers by accident; decide it deliberately.** Condition: every store, re-checked after any app install (apps can edit it). Source 15: test with `curl -A ClaudeBot yourdomain.com`. Source 08's audit flags pages "blocked from AI search". Source 04: CCBot's snapshot feeds model training. Sources: 01, 02, 15, 08, 04. Cards: [f94ce42ad17a] [153492ce5eeb] [8c1e01fcf839] [9098b567f595] [9ccea10d00bf] [8f6ede777b16] [87b0e16b4d08]. [web check: current AI crawler user agents]

**R95. Google can render JavaScript, so static generation is good practice, not a ranking requirement; still, put money-page content in the initial HTML and test with JavaScript off, because AI crawlers mostly do not render.** Condition: any theme or headless build. Source 05 says non-static sites "can't really rank"; the card corrects it. Source 15: disable JS, reload, and compare. Check the rendered HTML in URL Inspection. Sources: 05, 15, 02. Conflict: 7.13. Cards: [df678a626742] [b5a63fb310d9] [f8f8462498cb] [c463c6a96f1d].

**R96. A video gets video results only when it is the main content of its own page, above the fold; embeds mid-post rank as normal pages without video features.** Condition: stores with product or how-to video. Sources: 10. Cards: [5bde395c6a3b].

**R97. Use a Domain property so shop., checkout. and blog. subdomains and both http/https variants of the storefront are covered in one property; fall back to URL-prefix only when DNS access is impossible.** Condition: property setup or migration. Source 10: Domain covers shop., blog., checkout., www and non-www, http and https. Sources 01 and 05 use URL-prefix (source 01 calls GSC "sensitive" to variants; the card questions it). Sources: 10, 01, 05. Conflict: 7.8. Cards: [02f0df47b84c] [c0017f6a1d90] [4f3b94c692d3].

**R98. Refresh page code, not only visible copy: stale years in source, old asset names and leftover app code count against the page.** Condition: page-level audit. Source 04 spotted 2022 and 2023 timestamps in source; source 15 finds orphaned metafields from uninstalled review apps that pollute the Shopify catalog feed. Sources: 04, 15, 02. Cards: [29ea2467bb38] [c0a13e75f012] [959f69db4f65].

**R99. Gaps the sources do not cover: hreflang and multi-region, pagination beyond numbered pages, crawl budget on very large catalogs, migrations. Say so in the brief rather than invent steps.** Condition: any store that needs these. Sources: 01, 02, 07 (all state the gap). Cards: [273f1ec32b07].

**R152. Treat mobile as the primary storefront design target, not a speed footnote: check navigation, filters, checkout and the product page on a phone before a desktop screen.** Condition: mobile-first stores, including most India-market and mobile-heavy US catalogs; check the brand's own session and revenue split. Sources: 01. Cards: [684253d7bab8]. [needs brand data: mobile share of sessions and revenue]

**R153. For a store selling into more than 1 region or language, build region-specific pages (currency, shipping terms, near-me phrasing where relevant) with hreflang or a clear language switcher; do not run 1 generic page for India and US traffic.** Condition: any store selling into more than 1 country or language. Sources: 01. Cards: [9f38dfbf4f52]. [needs brand data: regions and languages served]

### Group J. Speed and Core Web Vitals (depth in 08-SPD)

**R100. Speed is a conversion lever first and a modest ranking signal second; treat it as an SEO blocker only when Search Console's Core Web Vitals report flags money-page URL groups as Poor or a page is clearly slow on a phone.** Condition: deciding whether speed work is SEO work. Source 02 calls the ranking effect "slight" and says Shopify is fast unless bloated. Source 01: fix speed before chasing rankings. Source 13: speed "can help but is absolutely not necessary" (opinion). Google's own guidance treats page experience as a ranking input. Sources: 02, 01, 03, 07, 13. Conflict: 7.4. Cards: [6223d92e1e72] [877d742162c1] [b75a8d6d1f40] [cc5014d16cd8] [6eb7236440e6] [37ad8a642ccb]. [web check: current Core Web Vitals thresholds]

**R101. Do not adopt any single speed target from these sources; log the store's own baseline and use 08-SPD's protocol.** Condition: always. The sources give 1 to 2 s, under 3 to 4 s, under 1.9 s, GTmetrix grade B, PageSpeed 80, Lighthouse 100, and source 01 still teaches FID, replaced by INP in March 2024. Sources: 01, 03, 05, 07. Conflict: 7.11. Cards: [1d5f63c6c8b4] [07eb3c368d7a] [67c0def66dd3] [37ad8a642ccb] [2aca699ba689].

**R102. Images are the first speed fix: WebP or JPEG for photos, resized to display size with srcset, compressed (source 07: under 2 MB each, about 2 MB per page), lazy-loaded except the LCP image.** Condition: every image upload. Sources: 02, 07, 03, 09. Cards: [3472ce4f007f] [00a2fbad5f22] [cc5014d16cd8] [0332997e3c20] [2aca699ba689].

**R103. Apps are the second speed fix: remove unused apps and their leftover theme code, load remaining app scripts only on the templates that use them, defer non-essential scripts.** Condition: Shopify. Source 02 finds leftovers in PageSpeed's third-party section. Sources: 02, 07. Cards: [959f69db4f65] [504893b96bd4] [5fe9759a8a5c] [cc5014d16cd8].

### Group L. Link building

Moved to Appendix A: R104, link volume and relevance (link-building doctrine, general to any website, section A.3).

Moved to Appendix A: R105, content-then-links sequencing (link-building doctrine, section A.3).

**R106. No paid links, no link swaps for discounts, no bulk packages; a disclosed sponsored placement carries `rel="sponsored"` and is bought for referral traffic, not rank.** Condition: always (ecomOS override plus Google policy). The sources say otherwise: source 02 says paid guest posts "work really well provided you're doing it properly" and treats dofollow as the goal; source 13 buys insertions at $100 to $400; source 03 uses vendors (with a disclosed affiliate tie); source 05 quotes $10 to $1,000 per placement; source 04 says paid and organic citations count equally. The `rel="sponsored"` qualifier was added by the card writers on sources 01, 05, 09 and 13; no presenter said it. Source 01 itself warns that link partners delete links or demand payment later. Sources: 02, 13, 03, 05, 04, 01. Conflict: 7.3. Cards: [ed27a5301c83] [cb6fea298ce4] [3490d57698e0] [6b66d770867b] [a4314277133f] [ed80a4bbd5e3] [ccdeae1f4dff] [3ac30aa3629d] [f32610667b5f].

Moved to Appendix A: R107, earning links (journalist queries, be-the-source, broken-link, guest posts) (link-building doctrine, section A.3).

**R108. Point earned links at educational pages and the root domain, then pass authority to money pages with internal links; direct heavy linking to product pages "looks unnatural".** Condition: choosing link targets. Source 02: 50% to 75% of new links to the root domain in the first 3 months, 25% to 50% to collection pages ranking 4 to 10, about 3 to 5 pages a month. Source 11: "I will die on this hill". Source 14: most links land on the homepage or blog anyway. Sources: 02, 11, 14. Conflict: 7.15. Cards: [84d4795d239e] [3cf4abf037ab] [1293de3e1c27] [d0d5872a02aa].

Moved to Appendix A: R109, anchor text mix (link-building doctrine, section A.3).

Moved to Appendix A: R110, the link-prospect screen (link-building doctrine, section A.3).

Moved to Appendix A: R111, monthly link pace from a competitor gap (link-building doctrine, section A.3).

Moved to Appendix A: R112, personalized outreach (link-building doctrine, section A.3).

Moved to Appendix A: R113, disavow caution (link-building doctrine, section A.3).

Moved to Appendix A: R114, reclaiming lost links (link-building doctrine, section A.3).

Moved to Appendix A: R115, digital PR cost and scale (link-building doctrine, section A.3).

**R116. Citations and directories: consistent name, address and phone, a small number of relevant directories, refreshed every 6 to 12 months; only for stores with a physical location.** Condition: local presence. Source 03's citation-service price of about $3.20 a listing is dated. Sources: 03, 01, 02. Cards: [f943f246de27] [1b05d31a2f5c] [d00b480b316f].

Moved to Appendix A: R117, vetting a link vendor (link-building doctrine, section A.3).

### Group M. AI search overlap (depth in 16-AEO)

**R118. AI answer engines retrieve from pages that already rank in Google or Bing, so traditional SEO is the prerequisite; do the fundamentals and then add the AEO layer.** Condition: any AI visibility work. Source 09: ChatGPT uses Bing's index, Perplexity leans on it, and Google sends about 190 times more traffic than ChatGPT (his figures). Source 03: AEO, GEO and LLM SEO are all still SEO. Source 05 treats "AI SEO" as a label. Source 08: keywords and prompts are the same intent on 2 platforms. Sources: 03, 09, 05, 08. Conflict on how separate AEO is: 7.18. Cards: [66b8ab8f9771] [7c2ebc1068d0] [b21ef0f9381d] [1449fb3da4a7] [46a784e2d55c]. [web check: current AI engine retrieval sources]

**R119. Pages that get cited are specific: product pages, comparisons, buying guides and best-of roundups with direct answers under clear headings.** Condition: choosing what to build for AI visibility. Source 14 cites a study of over 768,000 AI citations (unnamed) in which more than half came from product pages, comparison content and buying guides. Source 09: AI assistants favour best-of roundups. Source 04 pre-builds assets for the fan-out queries (alternatives, reviews, comparisons). Sources: 14, 09, 04, 12. Cards: [3fd8764bb3a6] [46a784e2d55c] [5346127695b9] [32d5cdf8c991] [10f5ad713679]. [web check: the 768,000-citation study]

**R120. Found, Matched, Chosen: allow the AI crawlers you want, state explicit product facts in the fields the AI reads, and build reputation on third-party platforms; on Shopify also check the global product catalog (title, at least 1 image, non-zero price, terms compliance, "agentic storefront" enabled) and clean stale metafields.** Condition: Shopify stores that want AI shopping visibility. Sources: 15, 04. Cards: [2a7d0c66c403] [9ccea10d00bf] [43284bf0e6dd] [c0a13e75f012] [87b0e16b4d08] [856538db1893]. [verify UI: Shopify catalog setting]

**R121. Measure AI visibility 3 ways and label each: a manual incognito check of buying questions, Search Console's generative AI report (impressions only at its June 2026 beta), and a tracker if the brand pays for one; a crawl hit in server logs is not a citation; set the region to the brand's main market.** Condition: monthly. Source 08's example: Brightland scored 50 of 100 in the US, mentioned by Google AI Overviews and rarely by ChatGPT. Sources: 09, 10, 08, 12. Cards: [46a784e2d55c] [178afbabc0bc] [05e68a491915] [7a78cc5341fe] [b099c3b28476]. [web check: current state of the generative AI report]

**R122. Do not present `llms.txt` as equal to robots.txt; Google does not use it, and adoption by other engines is unverified.** Condition: any AI crawl advice. Source 08 presents it as "the same job for AI tools"; the card corrects it. Sources: 08. Conflict: 7.19. Cards: [8f6ede777b16]. [web check: llms.txt adoption]

**R123. Everything beyond R118 to R122 (citation-blend research, fan-out modelling, brand sentiment in LLMs, agent readiness) routes to 16-AEO.** Condition: always. Source 04's citation blend sheet (5 queries, about 53 citations each) and source 08's Prompt Research and Brand Performance tools live there. Sources: 04, 08. Cards: [c65599bce8db] [cb73ca87f670] [9e06293fa0bb] [37ca9b962b23].

### Group N. Measurement and reporting

**R124. Search Console shows how Google sees the site; GA4 shows what visitors do; keep them separate and install both before launch, because GA4 has no backfill.** Condition: every store. Sources: 03, 01. Cards: [e247cdff3fb7] [88f4ed4866f4] [1a35cd16217e] [cd191b374d2e].

**R125. Report branded clicks (brand and product-name searches) separately from non-branded category and product-type searches; branded volume often moves with ad spend, not SEO work. Compare the last 3 months to the previous period, and export before data ages out of Search Console's 16-month window.** Condition: monthly report. Regex filter "doesn't match" with brand terms separated by `|`. Sources: 10. Cards: [ab49d7297c19] [f754914adaba] [dd8f0c00b989] [02f0df47b84c].

**R126. Read leading indicators before clicks: rising impressions, new queries you did not target, positions moving from page 5 toward page 3; ignore 2-position wobbles on 40-impression terms.** Condition: the first months of a program. Sources: 09, 10. Cards: [9bb24c359ea8] [0363a4df755b].

**R127. Low-hanging fruit is a page already ranking between positions 4 and 30 with impressions; push it with on-page work, internal links and a supporting piece before writing anything new.** Condition: monthly prioritization. Source 02 uses positions 4 to 10 for link targets; source 03 uses 9 to 30; source 10's vendor flags 6 to 8 for refresh. Sources: 02, 03, 10, 09. Cards: [3cf4abf037ab] [386891be5687] [7a8b4ae0cd5c] [40bc9625a691].

**R128. High impressions with low clicks: check position first; on page 2 or 3 the fix is content and links, on page 1 the fix is the title, the meta and speed, and a stable position with falling CTR means a stale snippet or an AI Overview above it.** Condition: CTR triage. Source 01's examples: 74,000 impressions to 175 clicks; 46,000 to 6. Sources: 01, 10. Cards: [b243bdf156ec] [860428181c80] [cc309b3d5cf7].

**R129. Find the pages behind a drop by sorting a 6-month comparison by click difference, then look for what the losers share: cluster, template, thin copy, cannibalization, or a SERP that changed.** Condition: any traffic decline. Source 01's period-over-period export shows that impressions and clicks can fall while average position improves. Sources: 10, 01. Cards: [c879262f60c4] [5895232c1ead] [b36fc4bc173f] [e3495a592539].

**R130. Retarget a page to the query that actually earns its clicks.** Condition: page-level review. Source 10's example: "is beeswax good for your skin" earned 3 clicks in 3 months; "benefits of beeswax for skin" earned 19. Sources: 10. Cards: [96052232339a].

**R131. Track organic add-to-cart, begin-checkout and purchase by landing page and investigate mid-funnel collapses before touching keywords; setup depth lives in 06-MEA.** Condition: organic revenue reporting. Source 01 tracks button clicks through Tag Manager and warns not to read 1 metric alone. Sources: 01. Cards: [7b56f452ec2a] [ca8c68867627] [7234716f3e22] [59a0144c8001].

**R132. Track 20 to 30 money keywords weekly, review Search Console and GA4 monthly, review device and country splits quarterly.** Condition: ongoing. Sources: 08, 03, 06. Cards: [db5cba249e82] [3f3f7fbd3c01] [411ebd9a5b1e] [d0068f9ba972].

**R133. The monthly report leads with organic revenue and non-branded clicks, then money-keyword positions, indexed money pages, links earned and AI mentions; no vanity totals.** Condition: every client report. Sources: 13, 03, 10. Cards: [7cc511272fe0] [fb7381a080bf] [dd8f0c00b989].

**R134. Do not build a dashboard until a free template or an export to a model stops being enough.** Condition: reporting setup. Sources: 03. Cards: [7a14782ab0f1].

**R135. Bounce triage excludes checkout, confirmation and gift-card pages, then looks at content pages over about 50% for thin or old copy.** Condition: GA4 page review. Sources: 01. Cards: [9345e5130d85] [31b0c4a879ee].

### Group O. Vendor, agency and tool vetting

**R136. Red flags: a guaranteed rank, an audit that lists dozens of critical fixes beyond the 4 essentials, a low retainer for blog posts only (source 13's example: $400 a month for 3 posts), cheap bulk links, "our content ranks #1" claims, tool advice from someone paid by the tool, and an audit or retainer that only proposes blog content and never touches collection or product page structure.** Condition: any pitch. Sources: 13, 11, 03, 05, 06. Cards: [6eb7236440e6] [41463bbdbca1] [b95c25b2d3c8] [0878cf8caa37] [7cc511272fe0].

**R137. Judge an agency on organic revenue after 3 to 6 months of money-page and link work, with the store's own before data recorded first.** Condition: any engagement. Sources: 13. Cards: [527f947f429c] [7cc511272fe0].

**R138. Google Business Profile, citations and local pages apply only to stores with a physical location; for those, claim and complete the profile, keep NAP consistent, post weekly, ask for reviews in person, and reply to every review.** Condition: physical presence. Source 03 targets 100 profile images (BrightLocal study, unverified). Source 05 calls the listing the lowest-hanging fruit. Sources: 09, 03, 01, 05. Cards: [e9e95368a588] [697ec7cc3648] [dbf8e0a7dc44] [b9c13080c7d1] [4b0b2abd2630].

### Group P. ecomOS overrides that beat any source

**R139.** No invented claims, statistics or testimonials on any page; every figure traces to a source or to brand data. **R140.** No paid or manipulative links (R106). **R141.** No undisclosed promotion on communities and no parasite pages (R85). **R142.** No incentivised reviews (R63). **R143.** Reading level below tenth grade (R84). **R144.** Real product photos where accuracy matters (R83). **R145.** AI-generated copy passes a human quality gate before it reaches a client page (R79). **R146.** Meta is read-only and no ad-account writes happen from this playbook. These have no source cards; they are house rules.

## 4. Procedures (implementation)

Each procedure gives the goal, preconditions, steps with settings, checks, rollback and `[verify UI]` tags. Steps that touch theme code run on a duplicate theme first.

### P1. Onboard a store and record the baseline

Goal: measurement in place and a dated baseline before any change. Preconditions: admin access to the store, a Google account that will keep owning the properties, registrar or DNS access.

1. Search Console: add a Domain property. Copy the TXT record into DNS at the registrar. If verification fails, click "verify later" and retry the next day. `[verify UI]` (R97, source 10)
2. If DNS is impossible, add a URL-prefix property for the exact https and www variant the store serves, verify with the HTML tag in `<head>`, and note the limitation in the brand record. (source 01, 05)
3. Confirm the custom domain is the primary domain (Shopify: Settings > Domains), then open `yourdomain.com/sitemap.xml` and submit that URL under Indexing > Sitemaps. `[verify UI]` (R93, source 07)
4. GA4: create the property with the store's currency set correctly, install 1 tag in `<head>` on every template (or through Tag Manager), verify in Realtime and by view-source for the measurement ID. Never install 2 GA4 tags. (source 01)
5. Record the baseline in the brand record: Search Console clicks, impressions, CTR and average position for the last 3 months, branded vs non-branded (P19 step 3), indexed vs not-indexed counts, GA4 organic sessions and purchases by landing page, current positions for the money keyword shortlist, referring domains.
6. Run a full crawl (P13 step 1) and store the export.
7. Checks: Search Console shows data within 2 to 3 days; GA4 Realtime shows your visit; the sitemap reports "success". Rollback: none needed; these are read-only setups.

### P2. Shopify technical fixes (in this order)

Goal: remove Shopify's default crawl waste and index only real pages. Preconditions: P1 done, duplicate theme created, theme editor access.

1. Confirm URL duplication: open the same product from 2 collections and compare URLs; view source and confirm the canonical points to `/products/handle`. (R42)
2. Online Store > Edit code > Snippets, find the product grid file (often `main-collection-product-grid.liquid`; search "grid"), delete every `within_collection` instance, save. If the string is absent, the theme already omits it. `[verify UI]`
3. Rebuild breadcrumbs: Content > Metaobjects and metafield definitions > Products, add a definition (type URL, not collection), store each product's parent collection URL, edit the breadcrumb snippet to render from it. `[verify UI]` [needs brand data: parent collection for every product]
4. Add `noindex, follow` snippets in theme.liquid for product tag pages, blog tag pages, vendor pages, product-type pages, and the all-collections, all-products and new-products utilities. (R41)
5. Only after step 2 is live: add a robots.txt.liquid template (Online Store > Edit code > Templates > Add > robots.txt) that disallows the same page classes plus cart, checkout, account and internal search, and keeps the Sitemap line. `[verify UI]` (R94)
6. Variants: for each product with separate variant pages, decide merge (native options) or keep and canonicalize with a metafield-driven canonical tag. (R43)
7. Deleted products: Online Store > Navigation > URL redirects, add a 301 to the nearest product or collection. (R50)
8. Sitemap exclusion for canonicalized pages: use the theme.liquid sitemap edit, not the hidden toggle that forces noindex, nofollow. (R93)
9. Verify structured data output on a product, a collection, a blog post and the breadcrumb snippet; fix trivial errors such as a missing comma. (R64)
10. Checks after each step: request the sitemap and confirm excluded URLs are absent; URL Inspection on 1 product and 1 tag page; Search Console Pages report a week later shows the tag and vendor pages moving to "excluded by noindex". Rollback: publish the previous theme version.

### P3. Keyword research and keyword map

Goal: a keyword map every page brief can be built from. Preconditions: access to 1 keyword tool and to Search Console; the catalog tree.

1. Seed list: 1 seed per collection and per major product type, in the shopper's words.
2. Free sources first (R22): export the last 16 months of Search Console queries; record autocomplete, People Also Ask and "People also search for" for each seed; note Reddit phrasing; run each seed through Keyword Planner with the target country.
3. Tool expansion: Keyword Magic Tool or equivalent for each seed (source 08's Brightland pull: filter KD 0 to 49; source 02's pull returned about 21,000 terms for "blackout curtain"). Pull questions separately. `[verify UI]`
4. Gate (R23): keep KD under the store's ceiling (30 to 40 for a new or low-authority store), intent transactional or commercial for money pages and informational for guides, volume above the floor written in the map. Use CPC as a secondary commercial signal (R25).
5. Hand sweep (R26): remove competitor brand names, mascots, job seekers, out-of-catalog and out-of-region terms.
6. Intent and SERP check on every kept term (P5).
7. Cluster: group terms that share a SERP or a meaning; 1 cluster equals 1 page (R27). Tools can cluster (Keyword Cupid, Keyword Strategy Builder); check the result by hand.
8. Gap analysis (R29): Keyword Gap with 3 to 4 SEO competitors; read Missing and Weak tabs; keep only gaps for products you sell.
9. Write the keyword map: cluster, primary keyword, secondaries, intent, volume, KD, CPC, page type, target URL (existing or new), current position, status.
10. Checks: no 2 rows share a primary keyword (R38); every money cluster maps to a collection or product; the volume floor is stated at the top of the sheet. Rollback: none; the map is a document.

### P4. Topical map and site architecture spec

Goal: a page tree that mirrors the keyword map. Preconditions: P3.

1. Order clusters by commercial value: money clusters first, then commercial comparison clusters, then informational clusters that support them (R4, R30).
2. Assign URL types (R37): collection for broad and option terms, subcollection for attribute splits with their own demand (R39), product for specific terms with volume (R59), homepage for 1 broad term nobody else targets, blog for informational and comparison formats.
3. Draw the tree: home, collections, subcollections by attribute (room, material, colour, use case), products. Every page has 1 parent.
4. Menu: expose subcategories directly for large catalogs; homepage features the highest-volume collections (R44).
5. Facets: for collections above about 200 SKUs, list the filter combinations with demand and give each a real collection page (R40).
6. Internal link plan (R46): for each collection hub, list the spokes that must link to it and to each other; for each product, the related-products rule and tag-style links (R48).
7. Cap and justify any set of templated pages (R51): count, unique content per page, demand per page.
8. Checks: no orphan pages in the plan; no keyword appears on 2 pages; every existing URL is mapped to keep, merge, redirect or noindex. Rollback: none; the spec is a document.

### P5. SERP intent check (30 seconds per keyword)

Goal: the page type for a keyword. Preconditions: an incognito browser set to the target country.

1. Search the exact keyword. Read organic results only; skip ads.
2. Classify the top 10 by format: product or collection pages, buying guides and comparisons, how-to articles, videos, forums, brand homepages.
3. Note features: AI Overview, People Also Ask, video carousel, shopping results, map pack.
4. Decide: 1 dominant format, build it; 5 or more of 1 format, build that; mixed, pick the format your authority can win (roundup for a commercial term owned by homepages, R20). Only giants ranking means skip (R16).
5. If an AI Overview appears, read it and list what your page must add beyond it (R72); mark the term as an AEO target (R17).
6. Record format, features and date in the keyword map. Re-check when the page is refreshed; SERPs drift.

### P6. Build or optimize a collection page

Goal: a collection page that can rank for its cluster and convert. Preconditions: keyword map row, real product photos, P2 done.

1. Title tag: keyword first, up to about 60 characters, modifiers after. H1: the keyword. Handle: short, keyword, filler removed; tick the redirect box if changed. (R52, R45)
2. Short description above the grid: up to 2 lines that answer what the collection is and for whom.
3. Grid: native app, 36 to 48 products, numbered pagination, colour, spec and price on tiles (R54).
4. Detailed description below the grid, 400 to 1,000 words when the term is contested (R53): what the products do, how to choose, differences between subcollections, contextual links to subcollections and guides, no stuffing. Use the split-marker snippet or read-more toggle. `[verify UI]`
5. Subcollection links from within the parent (R39).
6. FAQ accordion from People Also Ask and Search Console question queries (R55, R32), in HTML.
7. 3 featured reviews that mention the keyword, genuine and unincentivised, in plain HTML (R55, R63).
8. Search engine listing: title with a CTA or differentiator, 150 to 160 character meta description that sells the click (R56).
9. Headings: 1 H1, sequential H2 and H3 (R57). Images: alt text and file names (R62).
10. Schema: BreadcrumbList, FAQPage if FAQs exist; validate (R64).
11. Human quality gate (R79) on all copy: reading level, digits, short sentences, no em dashes, no invented claims.
12. Checks: view source shows content in HTML; the page has 1 H1; URL Inspection shows the live version; request indexing. Re-read position and CTR after 4 to 8 weeks. Rollback: restore the previous description text saved before the edit.

### P7. Build or optimize a product page

Goal: a product page for a product that has its own demand. Preconditions: R59 decision recorded; specs and real photos on hand.

1. Decide index vs noindex from volume (R59). For noindexed products, the collection carries the term.
2. Title from specs with the main and 1 supporting keyword (R60); the title is the H1.
3. Copy in order (R61): short description 50 to 150 words with the product name; feature and benefit bullets; spec table (weight, size, material, capacity); detailed description 300 to 1,000 words with explicit facts, differentiators, ingredients or materials, how to use; FAQ; reviews.
4. Images (R62): real product photos; descriptive file names; alt text with product name and what the image shows; WebP or JPEG; compressed; lazy-load all but the main image; all in the sitemap.
5. Reviews: unincentivised post-purchase request; app outputs Review and AggregateRating markup (R63).
6. Schema: Product with Offer, price and availability, AggregateRating, FAQPage, BreadcrumbList; validate in 2 tools (R64).
7. Breadcrumbs, tag-style category links, related products (R48).
8. Search engine listing: meta description about 160 characters written for the click; handle cleaned with redirect (R56, R45).
9. Out of stock: keep the page, swap the CTA to "notify me"; discontinued: "shop similar" (R50).
10. Human quality gate (R79).
11. Checks: JavaScript-off reload still shows reviews, FAQs and specs (R66); Rich Results Test shows Product eligible; 1 H1. Rollback: previous product copy saved before edit.

### P8. Implement and validate schema

Goal: valid, complete structured data on money pages. Preconditions: theme access or Tag Manager.

1. Inventory what the theme already emits on product, collection, article and breadcrumb templates (view source, search "application/ld+json").
2. Fill gaps: Product (name, image, description, sku, brand, offers with price, currency, availability), AggregateRating and Review from real reviews, FAQPage from the visible FAQ, BreadcrumbList from the real hierarchy, Article or BlogPosting on posts with author, dates and image.
3. Generate with a schema generator if hand-writing is risky; when a validator flags a date format, fix it and re-validate; do not trust an AI fix without re-running the validator. (source 01)
4. Deploy in the template. Without theme access, deploy per page through Tag Manager: Custom HTML tag, Page View trigger with Page Path equals the URL, publish, then Preview. (source 01) `[verify UI]`
5. Validate in Rich Results Test and a second validator; the 2 can disagree (source 03).
6. Watch Search Console's Shopping and Enhancements reports for errors after the next crawl.
7. Checks: the markup matches visible facts (price, availability, rating count). Rollback: remove the tag or revert the snippet.

### P9. Plan and produce a content cluster

Goal: 5 to 10 pieces that support 1 money page. Preconditions: the money page exists and is optimized (P6 or P7).

1. Pick the cluster from the topical map (R68). List every angle a buyer searches: definitions, how-to, comparisons, alternatives, best-for-use-case, buying guide (R67, R69).
2. For each piece run P5 and confirm a blog format ranks; if collections rank, build a collection instead (source 14).
3. Brief each piece (section 9, page brief): primary and secondary terms, the SERP's dominant structure, table stakes from the top 5, the gap you will fill, the money page it supports, sibling links, the human moat items (R71), cited sources, real images.
4. Produce with P10 or by hand.
5. Internal links before publishing: money page within the first 100 to 200 words, 3 to 5 sibling links, 2 to 4 word descriptive anchors (R46); add a link from the money page back to the best 1 or 2 posts (R47).
6. Publish on the review cadence, not faster (R74). Request indexing.
7. Bridge post when moving to the next cluster (R68).
8. Checks: every post has an outbound citation for each claim, an internal link to the money page and a byline with dates (R65). Rollback: unpublish; nothing else changes.

### P10. AI-assisted draft with human gates

Goal: a draft that passes the ecomOS quality gate. Preconditions: brand voice document, banned-word list, brand facts, real images, the page brief from P9.

1. Prepare the project folder with the voice document, banned words (start with em dashes and stock openers such as "in today's fast-paced world"), stories and stats, the brief, and the source pages (category page plus 3 to 5 product pages) (R78).
2. Prompt with a persona, the audience, the language variant and the goal; instruct the model to ask clarifying questions before writing (source 03, 06). Answer them.
3. Approve the outline first (gate 1). Reject any suggested section you cannot deliver (source 03's "calculator" example).
4. Generate the draft into a document, not the CMS.
5. Fact-check every number, claim and product detail against brand data; replace placeholders such as "contact for pricing"; expect 3 to 5 passes (R79, source 04).
6. Add the human moat by hand: first-hand notes, opinion, original data, a quote with a source (R71). Rewrite at least the weakest 10% to 20% by hand (source 06).
7. Run the on-page pass (title, meta, 1 H1, keyword in the first 100 words, 4 to 8 questions, 2 to 3 external and 3 to 5 internal links) with the instruction to keep the voice; then re-read for voice loss (source 05).
8. ecomOS quality gate: reading level below tenth grade, digits, short sentences, no em dashes, no inflated words, no invented claims, no GPT mentions on the page.
9. Images: real product photos on any product or collection page; illustrative stock or generated images only on informational posts, and never a redrawn product (R83).
10. Publish as a draft in the CMS; a person schedules it (gate 2).
11. Checks: the AI detector is optional and not a pass mark (source 06 uses one); the human read is the gate. Rollback: keep the previous version in the document history.

### P11. Content refresh

Goal: recover or lift an existing page. Preconditions: P19 output.

1. Candidates: pages ranking 4 to 30 with impressions; pages whose CTR fell at a stable position; pages that lost clicks in the 6-month comparison; year-stamped titles (R73, R127, R128).
2. Filter Search Console by the page URL, open Queries, and compare the target keyword with the click leader; retarget the title and H1 if they differ (R130).
3. Re-run P5 for the primary keyword; if the SERP format changed, change the page format.
4. Read the current top results; add missing subtopics, questions, data and first-hand notes; update dates and the year in the title; fix internal links to and from the page.
5. Rewrite title and meta if CTR was the problem; check whether an AI Overview now sits above the result and add what it lacks.
6. Request indexing; log the change with the date.
7. Checks: compare clicks, impressions, CTR and position for the page 4 to 8 weeks later against the pre-change window. Rollback: previous copy from the log.

### P12. Internal linking pass

Goal: authority flows to money pages. Preconditions: P4 spec.

1. Search Console > Links: list the most-linked pages (internal and external) (R46).
2. From each high-authority page, add contextual links to priority collections and new pages.
3. For the top 2 or 3 blog posts by traffic, add 1 clean link each to the bestselling collection or product (source 14).
4. For every collection hub, confirm each spoke links to the hub and to 1 sibling; add missing links in body copy with 2 to 4 word anchors.
5. Convert collection-to-subcollection links from general to specific.
6. Fix orphans found in the crawl (R49).
7. Checks: re-crawl and confirm no orphans and no links to redirecting or http URLs. Rollback: remove the added links.

### P13. Crawl, indexing diagnosis and fixes

Goal: every money page indexed, nothing else wasting crawl. Preconditions: crawler and Search Console.

1. Crawl with Screaming Frog (free to 500 URLs), Sitebulb or Semrush Site Audit, mobile user agent, JavaScript rendering on, structured-data checks on. `[verify UI]`
2. Work errors first: 404s and links to them (redirect to nearest relevant), canonicals pointing to redirects, orphan pages, https pages linking to http, missing or duplicate titles and descriptions, missing H1s, oversized images, schema errors (R87).
3. Search Console > Indexing > Pages: group not-indexed URLs by reason and apply the litmus test (R88). Fix money pages under noindex or robots blocks; leave cart, search, filters, thank-you and staging excluded.
4. URL Inspection on each priority page that is not indexed; act on the reason (R89); request indexing after the fix (R90).
5. robots.txt review (R94): allowed paths, Sitemap line, no accidental AI-crawler block; `curl -A ClaudeBot yourdomain.com` and a JavaScript-off reload of a product page (R95).
6. Video: for any video that should appear in video results, move it to its own watch page (R96).
7. Checks: the not-indexed count for money pages drops on the next report; 404 count drops after redirects. Rollback: redirects can be removed; noindex can be lifted.

### P14. Speed quick pass (then 08-SPD)

Goal: decide whether speed is an SEO blocker and fix the 2 easy causes. Preconditions: PageSpeed Insights.

1. Search Console > Experience > Core Web Vitals: count Poor URL groups on mobile for product and collection templates (R100).
2. PageSpeed Insights on the home, a top collection and a top product, mobile; note the field data lags about 28 days (source 07).
3. Images: compress, resize, WebP, srcset, lazy-load all but the LCP image (R102).
4. Apps: uninstall unused apps, remove leftover code found under "reduce the impact of third-party code", load app scripts by template (R103).
5. Re-test. If Poor groups remain, hand the report to 08-SPD.
6. Checks: no lazy attribute on the hero or main product image. Rollback: reinstall an app if a feature broke.

### P15. Link prospecting and screening

Goal: a vetted prospect list. Preconditions: 10 to 15 good pieces published (R105), a linkable asset or an expert available.

1. Identify 5 or more SEO competitors of similar size for your money terms (R9).
2. Pull each competitor's backlinks: dofollow only, 1 per referring domain, placement in content, platform blog; export (source 02). `[verify UI]`
3. Bulk-check prospects: monthly visits above about 1,000, Authority Score at least 15 (or 50 for a Backlink Gap pass, source 08), DR or DA 30 plus for gap counting (R110, R111).
4. Widen to topically adjacent sites (interior design blogs for a curtain brand); reject unnatural fits (an outdoor blog for curtains).
5. Screen each with the 5-point check (R110): real single-topic site, Wayback history, relevance, stable traffic, clean profile.
6. Reject anything selling links, Fiverr-style offers, or unsolicited sellers.
7. Record the target page on your site for each prospect (educational page or root domain first, R108) and the reason the host would link.
8. Checks: the list contains no site you would pay for a dofollow link; every row has a value offer. Rollback: none.

### P16. Journalist query outreach

Goal: earned editorial links and mentions. Preconditions: a named expert at the brand, a 1 to 2 paragraph bio, 15 minutes a day.

1. Sign up on Featured.com, Source of Sources, or Connectively; select subject-matter expert; claim the core niche and adjacent topics. `[verify UI]` [web check: current platforms]
2. Filter by topic, not by deadline; check the outlet's authority with a free checker but pitch highly relevant queries even from small outlets (source 02).
3. Research the answer beyond a plain Google search; answer from first-hand experience; bold key phrases; bullets; keep the bio ready.
4. Track in a sheet: query, outlet, authority, pitched, outcome. Expect about 1 hit per 100 (source 09) or 20 to 2 to 1 (source 02).
5. Reply to follow-ups before the deadline.
6. Checks: monthly count of placements and links. Rollback: none.

### P17. Guest posts and link inserts (compliant version)

Goal: editorial placements that pass Google policy and ecomOS rules. Preconditions: P15 list.

1. Pitch with a concrete offer: a tested, current replacement for an outdated page they link to, or a piece their readers need (R112). Personalize every email; warm up sending accounts; about 20 a day per account at the start (source 02).
2. If the host asks for a fee, treat the placement as sponsored: it must be disclosed and carry `rel="sponsored"` or `rel="nofollow"`, and it is bought for referral traffic only. If the host will not disclose, decline (R106).
3. Write for the host's audience, 600 to 1,200 words unless the host says otherwise; the link sits in a relevant sentence near the top; soft anchor (R109).
4. For an insert into an existing article, confirm the article already has traffic and topical fit (source 13's relevance check) and apply the same disclosure rule if money changes hands.
5. After publish: confirm the link is live, the rel attribute matches the deal, and host edits did not change your claims (source 02).
6. Checks: no more links to 1 page than competitors have (R104). Rollback: ask the host to remove a link that breaks policy.

### P18. Backlink audit and disavow decision

Goal: know the profile; disavow only when warranted. Preconditions: backlink tool export and Search Console.

1. Check Security and Manual Actions first (R113).
2. Sort referring domains by DR or DA and by spam score; low DR alone is not a problem.
3. Check anchor text mix (R109) and geography (a US store with most links from an unrelated region is weak, not toxic).
4. Lost and Vital: list high-authority lost links and reach out (R114).
5. Disavow only for manipulative links tied to an actual or likely manual action: text file, 1 domain or URL per line, upload in Search Console's disavow tool. Most stores skip this step.
6. Checks: the manual action clears on re-review. Rollback: a disavow file can be replaced.

### P19. Monthly Search Console read

Goal: the monthly report inputs. Preconditions: Domain property with 3 or more months of data.

1. Performance > Search results, last 3 months vs previous period; toggle clicks, impressions, CTR, position (R125).
2. Filter queries "doesn't match" regex `brand|brand name|brandname com`; record non-branded clicks and impressions; then the inverse for branded (R10, R125).
3. Pages tab sorted by click difference ascending: losers; ascending impressions with low clicks: CTR triage list (R128).
4. Queries tab: new non-targeted queries; positions 4 to 30 with impressions: low-hanging list (R127).
5. Question regex `who|what|when|where|why|how|can|does`: unanswered questions to FAQ or new pages (R32).
6. Indexing > Pages: not-indexed by reason; any money page in the wrong group (R88).
7. Experience > Core Web Vitals: Poor groups on mobile (R100). Shopping and Enhancements: schema errors.
8. Links: top linked pages and new referring sites.
9. Generative AI report if available: impressions by page, cross-checked against pages losing clicks (R121).
10. Export queries (up to 1,000 rows) and the not-indexed list for the record (R82).
11. Checks: every number is period-over-period and split branded vs non-branded. Output feeds section 9's monthly report.

### P20. Diagnose a traffic drop

Goal: name the cause before changing anything. Preconditions: P19.

1. Set the comparison to cover the drop (6 months vs previous). Sort pages by click difference ascending (R129).
2. Look for shared traits among the losers: 1 cluster, 1 template, thin copy, 2 pages on 1 keyword, a lost redirect, a noindex introduced by a theme or app change.
3. Check position: if position held and CTR fell, it is a snippet or an AI Overview (R128); if position fell across a cluster, it is content or links; if impressions fell to 0, it is indexing.
4. Check the date against known theme changes, app installs, migrations and Google updates.
5. Fix the largest losers first; log the fix.
6. Checks: clicks on the fixed pages recover in the next 2 monthly reads; if not, escalate to a content or link plan.

### P21. CTR triage

Goal: more clicks from existing impressions. Preconditions: P19 step 3.

1. For each high-impression low-click row, read the average position.
2. Page 2 or 3: content and internal links (P11, P12), not the title.
3. Page 1: rewrite the title (keyword plus benefit or CTA) and meta (150 to 160 characters, what the shopper gets); compare against the competing snippets on the SERP; check speed.
4. Stable position with falling CTR: check for an AI Overview; go deeper than it (R72).
5. Re-measure the same query set after 4 weeks.

### P22. AI search visibility, light pass

Goal: know whether the brand appears in AI answers; deeper work in 16-AEO.

1. In an incognito AI chat, ask 5 buying-journey questions a customer would ask; record which brands and pages are named (R121).
2. Search the main product type as a question in Google; if an AI Overview appears, note its cited pages and formats (source 14).
3. Read Search Console's generative AI report if present.
4. Run the crawler-access checks (P13 step 5) and the Shopify catalog check (R120).
5. List the specific pages (comparisons, best-for-use-case, product pages with explicit facts) the store lacks; feed them into the topical map.
6. Hand the rest to 16-AEO.

### P23. Vet an agency, freelancer or tool

Goal: avoid paying for vanity or risk. Preconditions: the pitch and the store's baseline.

1. Ask what the KPI is; if it is not organic revenue or non-branded clicks, push back (R3).
2. Ask for the link method in writing; any paid, swapped or bulk link is a refusal (R106).
3. Ask for 1 named past client site with campaign dates; check its traffic trend across the window (R117).
4. Read the audit: if it lists dozens of critical fixes beyond crawl, index, broken links, UX and hierarchy, it is a sales document (R136).
5. Ask whether recommended tools pay the recommender; treat sponsored tool advice as marketing (section 12).
6. Set a 3 to 6 month review on organic revenue with the baseline recorded first (R137).

### P24. 30-day and 90-day sequencing

Goal: a plan a small team can run. Preconditions: P1.

- Weeks 1 to 4 (source 09's plan): week 1 Search Console, tooling, 10 to 15 target keywords, intent tests on the top 5, money-page inventory; week 2 the single most important money page built or optimized; week 3 the first cluster piece linked to it; week 4 journalist queries 15 minutes a day, AI visibility check, first Search Console read.
- Days 1 to 90 (sources 04, 02, 13): technical fixes (P2, P13) in month 1 alongside the money pages of 1 category; 1 full cluster and internal linking in month 2; link outreach and refreshes in month 3; re-benchmark rankings, non-branded clicks and organic revenue at day 90 before choosing the next category (R6).
- Monthly thereafter: P19, P11, P12, P15 to P17, on a fixed day (R8).

## 5. Diagnostic checklists

Written so a worker can run them. Each row: what to check, how, good, bad, fix, source.

### 5.1 Technical audit

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Money pages indexed | Search Console > Pages; URL Inspection on top 20 collections and products | All indexed | Any under noindex, robots block or "crawled, not indexed" | R88, R89; P13 | 10, 13 |
| Not-indexed reasons are intentional | Pages report grouped by reason | Only cart, search, filters, thank-you, staging, tags | A money page in the excluded group | Remove the tag or rule, resubmit | 10 |
| Product URL duplication (Shopify) | Open 1 product from 2 collections; compare URL; view source canonical | Clean `/products/` URL everywhere | `/collections/x/products/y` paths | P2 step 2 | 02 |
| Tag, vendor, type, utility pages | `site:domain/collections/vendors`, Pages report | Noindexed | Indexed thin pages | P2 step 4 | 02 |
| robots.txt | Open `/robots.txt`; `curl -A ClaudeBot domain` | Blocks admin, cart, search, filters; Sitemap line; no money path blocked; AI bots allowed by decision | A wanted path blocked, or an app changed the file | R94 | 01, 02, 15, 08 |
| Sitemap | Open `/sitemap.xml`; Search Console Sitemaps | Submitted, success, includes products, collections, posts, images; excludes noindexed pages | Missing, errors, wrong domain, noindexed URLs listed | R93 | 01, 02, 07 |
| 404s and broken links | Crawler status codes; Pages report | 0 internal links to 404s | Dead product URLs, links to 404s | 301 to nearest relevant page | 01, 02, 13 |
| Redirect chains and http links | Crawler | Internal links go straight to final https URL | Chains, http targets | Update the links | 01 |
| Canonicals | Crawler canonical report | Self-referencing or to the primary variant; never to a redirect | Canonical to a redirect, missing, or pointing at a different collection path | R91 | 01, 02 |
| 1 H1 per template | Inspect element on home, collection, product, post | Exactly 1 | 0 or 2 plus (custom section) | Demote extra to H2 | 07, 03 |
| Titles and metas | Crawler | Unique per page; title about 60; meta 150 to 160 | Missing, duplicate, too long | P6, P7 step 8 | 01, 09 |
| Structured data | Rich Results Test on 1 product, collection, post; Search Console Enhancements | Product, Breadcrumb, Article valid | Errors (often a missing comma), missing types | P8 | 02, 03 |
| JavaScript-only content | Disable JS, reload a product page | Reviews, FAQs, specs still visible | Placeholders only | Render in HTML | 15 |
| Orphan pages | Crawler orphan report | 0 wanted pages orphaned | Pages with no internal links | P12 | 01, 03 |
| Image weight | Crawler or PageSpeed | Under 2 MB each; page about 2 MB | Camera uploads, PNG photos | R102 | 07, 02 |
| LCP lazy-loaded | View source of hero and main product image | No lazy attribute | `loading="lazy"` on the LCP image | Remove it | 07, 02 |
| Core Web Vitals | Search Console Experience | No Poor groups on money templates | Poor groups on mobile | P14 then 08-SPD | 01, 03 |
| Leftover app code and metafields | PageSpeed third-party section; product metafields | None from uninstalled apps | Scripts and fields from removed apps | Remove | 02, 15 |
| Health score reading | Crawler dashboard | Errors 0, warnings falling | High score but errors present | Work errors first; do not chase 100 | 01, 08 |
| Video pages | Search Console Videos report | Videos on watch pages | "Video isn't on a watch page" | R96 | 10 |
| Code freshness | View source for years and dates | Current | 2022 and 2023 timestamps | Refresh assets and markup | 04 |

### 5.2 Collection page audit

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| 1 target cluster, no cannibal | Keyword map; Search Console query filter shows 1 stable URL | 1 collection per keyword | A product or post also targets it | R38 | 02, 14 |
| Page type matches the SERP | P5 | Collections rank for the term | Guides or products rank | Change type or target | 02, 09 |
| Title tag | View source | Keyword first, about 60 chars, modifier after | Bare keyword, or over 60 | R52 | 02, 08 |
| H1 | Inspect | Equals the target keyword | Vague ("Bath") or 2 H1s | R52, R57 | 07 |
| URL | Address bar | Short, keyword, no filler | Long or generic | R45 with redirect | 07, 01 |
| Short description | Above the grid | Up to 2 lines, says what and for whom | Missing or a wall of text | R53 | 02 |
| Detailed description | Below the grid | 400 to 1,000 words for a contested term, at least 100 for any; links to subcollections and guides; no stuffing | Bare H1 plus grid; keyword-stuffed filler | R53 | 02, 06, 07 |
| Grid | Count and paginate | 36 to 48 items, numbered pages, tiles show colour, spec, price, HTML-rendered | Previous/next only; JS grid | R54 | 02 |
| Subcollections | Links inside the parent | Each has demand and unique copy | "Top rated", "on sale" clones | R39 | 02 |
| Facets | For 200 plus SKUs | Present; ranked combinations have real pages | Parameter URLs expected to rank | R40 | 02 |
| FAQ | Bottom of page | Real PAA and Search Console questions, in HTML | Missing or invented | R55, R32 | 02, 10 |
| Featured reviews | Bottom of page | 3 genuine reviews naming the keyword | Incentivised or none | R55, R63 | 02 |
| Search engine listing | Search the term in Google | Title with CTA or differentiator; meta 150 to 160 that sells | Bare keyword, truncated | R56 | 06, 07 |
| Schema | Rich Results Test | BreadcrumbList, FAQPage valid | Errors | P8 | 02 |
| Images | Alt and file names | Descriptive, keyword plus product plus descriptor | Numbers, repeated phrases | R62 | 07, 09 |
| Internal links out | Body copy | Links to subcollections, guides, sibling collections | None outside the menu | R46 | 04, 14 |
| Internal links in | Search Console Links; crawler | From homepage or parent and from cluster posts | Orphaned or menu-only | P12 | 10 |
| Reading level and claims | Human read | Below tenth grade, digits, no invented claims | Inflated words, unsupported claims | ecomOS gate | house |

### 5.3 Product page audit

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Should it be indexed | Volume for the product name or attribute | Volume exists | 0 volume, made-up name | Shift effort to collection; consider noindex | 02 |
| Title and H1 | Inspect | Product name as searched, main plus supporting keyword | "Sweet Honey Bomb" | R60 | 07 |
| Copy stack | Read the page | Short description 50 to 150 words; bullets; spec table; 300 to 1,000 words detailed; FAQ; reviews | Specs only, under 100 words, manufacturer copy | R61 | 02, 07, 01 |
| Explicit facts | Compare to a shopper query | Size, colour, material, use case stated | Vague marketing phrases | R61 | 15 |
| Images | Inspect | Real photos, descriptive names and alt, WebP or JPEG, compressed, main image not lazy, all in sitemap | Stock or generated product images; numeric names | R62, R83 | 02, 07, house |
| Reviews and schema | Rich Results Test | AggregateRating present from real reviews | Missing markup; incentivised reviews | R63 | 02 |
| Schema set | Rich Results Test and a second validator | Product with price and availability, Breadcrumb, FAQ | Missing or mismatched price | R64 | 02, 03 |
| Rendering | JS off | Reviews, FAQ, specs visible | Widget placeholders | R66 | 15 |
| Variants | URLs | Merged or canonicalized | Separate pages competing | R43 | 02 |
| Breadcrumbs and related | Page | Present and correct after the URL fix | Broken or missing | R48, R42 | 02 |
| Meta description | Search engine listing | About 160 chars, sells the click | Missing or keyword list | R56 | 07 |
| URL handle | Address bar | Short, descriptive; redirect exists for old handle | Filler words; no redirect | R45 | 07 |
| Out-of-stock handling | Page | Live with "notify me" or "shop similar" | Deleted or 404 | R50 | 02 |
| E-E-A-T signals | Page | Original photos, real usage notes, dates | Generic copy | R65 | 11, 09 |
| Reading level and claims | Human read | Below tenth grade, no invented claims | Otherwise | ecomOS gate | house |

### 5.4 Keyword map review

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Volume floor stated | Top of sheet | A number set per catalog and margin | Copied 500 or 5,000 from a video | R23 | 01, 08 |
| Difficulty ceiling | Sheet | Under 30 to 40 for a new store; raised as authority grows | Head terms owned by giants | R23, R18 | 05, 06, 14 |
| Intent per row | Column | Transactional or commercial to money pages; informational to guides | Informational term on a collection | R15 | 09, 07 |
| SERP check done | Date column | Every row checked in incognito with format noted | Blank | P5 | 11, 09 |
| No duplicate primaries | Sort by primary | 1 page per primary | 2 rows share a keyword | R38 | 02, 14 |
| Page type | Column | Collection for broad, product for specific, blog for learn and compare | Product page for a category term | R37 | 02 |
| Brand and mascot terms | Sweep | None | Competitor names kept | R26 | 05 |
| Clusters | Grouping | Each page has secondaries; clusters of 3 to 5 or more terms | Flat single-keyword rows | R27 | 06, 02 |
| Gaps mapped | Gap columns | Missing and Weak terms for products you sell | Gaps for products you do not sell | R29 | 08, 01 |
| Status and owner | Columns | Published, refresh, quick win, needs publishing, with owner | Blank | R28 | 02 |
| Shortlist first | Priority column | Money terms ranked before long tail | Volume-sorted list | R30 | 11 |
| TOFU with path | Note per informational term | Conversion path named | Vanity traffic | R34 | 09 |

### 5.5 Link prospect screen

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Real single-topic site | Read it | Coherent niche | "About everything" link farm | Reject | 02 |
| Domain history | Wayback Machine | Same topic over years | Former casino or unrelated past | Reject | 02 |
| Relevance | Compare topic to yours | Same or adjacent niche | Unrelated | Reject | 02, 03 |
| Traffic | Tool estimate | About 1,000 plus monthly visits, stable or growing | Sudden drop (penalty sign) | Reject | 02 |
| Authority | Authority Score or DR | 15 plus (raise as you grow); 30 plus for gap counting; 50 for a Backlink Gap pass | Below floor with no relevance | Deprioritize | 02, 08 |
| Own backlink profile | Tool | Clean, natural growth | Spikes, spam | Reject | 02, 03 |
| Payment asked | Host reply | None, or a disclosed sponsored placement with `rel="sponsored"` | Undisclosed paid dofollow | Decline (ecomOS) | house, 05, 09, 13 cards |
| Anchor and placement | Draft | Soft anchor in a relevant sentence near the top | Exact match, isolated callout | R109 | 02 |
| Target page | Plan | Educational page or root domain first | Heavy links to 1 product page | R108, R104 | 02, 11 |
| Vendor claims | Ask for a client site and dates | Traffic held or grew | Declined | Refuse | 05 |

### 5.6 Monthly Search Console read

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Non-branded clicks vs prior 3 months | Regex "doesn't match" brand terms; Compare | Up | Down | P20 | 10 |
| Branded position | Regex "matches" brand | Position 1 for brand and product names | Lost to a reseller or competitor | Homepage and brand page work; R10 | 10, 14 |
| Impressions trend | Compare | Rising even if clicks lag | Falling | P20 | 09 |
| Biggest losers | Pages by click difference ascending | None material | Cluster or template losing | P20 | 10 |
| High impression, low click | Pages and Queries by impressions | Proportional | 74,000 impressions to 175 clicks | P21 | 01 |
| Positions 4 to 30 with impressions | Queries filtered | List made | Ignored | P11, P12 | 02, 03 |
| New untargeted queries | Queries tab | Fed into the map | Ignored | R126 | 09 |
| Question queries unanswered | Regex question words | Each has a page | Passing mentions only | R32 | 10 |
| Not-indexed money pages | Pages report | 0 | Any | P13 | 10 |
| Core Web Vitals Poor groups | Experience | 0 on money templates | Any | P14 | 01 |
| Schema errors | Enhancements and Shopping | 0 | Any | P8 | 02 |
| New referring sites | Links | Logged | Spam spike | P18 | 10 |
| Generative AI impressions | Report if present | Logged by page | Overlap with click losses | R121 | 10 |
| Export saved | Download | Yes, dated | No | R125 | 10 |

### 5.7 Content refresh review

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Candidate list | Positions 4 to 30; CTR down at stable rank; click losers; year-stamped titles | List with owner and date | None | R73 | 09, 10, 01 |
| Click leader vs target | Page filter, Queries tab | Title and H1 match the click leader | They differ | R130 | 10 |
| SERP still matches format | P5 | Same format | Format changed | Change the page | 11 |
| Depth vs top 5 | Read them | Covers table stakes plus a gap | Restates the AI Overview | R70, R72 | 09 |
| Human moat present | Read | Experience, opinion, data, quotes, examples | Generic | R71 | 09, 03 |
| Citations | Count | Every claim linked to a source | Unsourced claims | R47 | 03 |
| Internal links | Count | Money page in first 100 to 200 words; 3 to 5 siblings; inbound from hub | Missing | R46 | 14 |
| Dates and byline | Page | Updated date and author present | Missing or stale year | R65, R73 | 11, 01 |
| Voice and reading level | Human read | Brand voice, below tenth grade, no em dashes | AI openers, inflated words | P10 step 8 | house, 05 |
| Cannibalization | Query filter | 1 URL per query | URL switches | R38 | 02 |
| Result logged | Log | Change date, then 4 to 8 week read | No log | P11 | 06 |

## 6. Thresholds and benchmarks

Confidence: "high" means 3 or more sources agree or it matches Google's public statements; "medium" means 2 sources; "presenter heuristic" means 1 practitioner's number; "vendor" means a tool's own score or a vendor's marketing figure. None of these is a promise.

| Item | Value | Condition | Source(s) | Confidence |
|---|---|---|---|---|
| Title tag length | about 60 characters; keyword first | any page | 01 (later), 02, 09, 08 | high (Google sets no character limit; display is pixel-based) |
| Title tag length, outliers | 150 to 160 (01 early, wrong); 45 to 61 (03); 70-character Shopify homepage field (07) | see 7.10 | 01, 03, 07 | presenter heuristic |
| Meta description length | 150 to 160 characters, about 155 | any page | 01, 03, 09, 07, 02 | high |
| Meta description as ranking factor | not a ranking factor; affects CTR | any page | 13, 07, 09, 02 | high |
| H1 count | exactly 1 | any page | 07, 03, 01, 05 | high |
| Keyword difficulty ceiling | under 30 (05), under 35 (14), under 40 (01, 06), 0 to 49 (08) | new or low-authority store | 05, 14, 01, 06, 08 | medium (range agreed, number not) |
| Volume floor | 100 (05), 500 (01), 1,000 (06), 5,000 (08) a month | keyword gate | 05, 01, 06, 08 | presenter heuristic, see 7.20 |
| CPC floor | over $1 | commercial keyword gate | 06 | presenter heuristic |
| Typical money-keyword CPC | $3 to $20 | local service niche | 05 | presenter heuristic |
| Keywords per page | 1 primary plus 2 to 5 secondaries | any page | 07, 06, 02 | medium |
| First keyword list size | 10 to 15 terms | starting out | 08, 09 | medium |
| Clusters per month | first 5 | content calendar | 08 | vendor workflow |
| Cluster size | 5 to 10 articles | 1 topic before the next | 09, 11 | medium |
| Blog system size | 10 to 15 posts in 4 buyer formats | Shopify store | 14 | presenter heuristic |
| Content before outreach | 10 to 15 good pieces | new site | 09 | presenter heuristic |
| Collection detailed description | 500 to 1,000 words (02); 400 plus (06); 100 to 400 (07) | competing collection | 02, 06, 07 | medium on "several hundred", see 7.9 |
| Collection short description | up to 2 lines | above the grid | 02 | presenter heuristic |
| Product short description | 50 to 150 words | top of product page | 02 | presenter heuristic |
| Product detailed description | 500 to 1,000 (02); 100 minimum, 300 to 400 ideal (07) | product page | 02, 07 | medium on "300 plus" |
| Grid size | 36 to 48 products per page | collection | 02 | presenter heuristic |
| Faceted navigation trigger | about 200 SKUs | collection | 02 | presenter heuristic |
| Featured reviews | 3 | collection page | 02 | presenter heuristic |
| Questions per post | 4 to 8 | blog post | 05 | presenter heuristic |
| Internal links per page | 3 to 5 to related pages; money page in the first 100 to 200 words | post | 05, 14 | medium |
| External citations per page | 2 to 3 | post | 05 | presenter heuristic |
| Anchor text length | 2 to 4 descriptive words | internal link | 14 | presenter heuristic |
| Alt text length | 3 to 4 words (01); descriptive sentence fragment (07, 09) | image | 01, 07, 09 | low; describe the image |
| Image file size | under 2 MB each; about 2 MB per page | uploads | 07 | presenter heuristic |
| Image compression example | about 50% reduction | 1 image | 02, 07 | example |
| Page load time | 1 to 2 s ideal (01); under 3 to 4 s (01); under 1.9 s good, over 3 s losing money (03) | speed | 01, 03 | presenter heuristic, see 7.11 |
| PageSpeed score | 0 to 49 poor, 90 to 100 good (tool bands); 80 plus target (03); Lighthouse 100 target (05) | speed | 01, 03, 05 | tool bands high; targets presenter heuristic |
| GTmetrix grade | below B fix now | speed | 03 | presenter heuristic |
| PageSpeed field data lag | about 28 days | reading after a fix | 07 | high (tool behaviour) |
| CLS poor | over 0.25 | Core Web Vitals | 01 | high (matches Google) |
| Core Web Vitals set | LCP, CLS, INP (FID replaced March 2024) | any | 01 card correction | high |
| Tool and platform prices | Screaming Frog, Semrush, Ahrefs, Featured.com tiers | tools | 08, 09, 13, 06, 03 | moved to Appendix A, section A.4 (vendor trivia, not store-specific) |
| Journalist query hit rate | about 1 per 100 (09); 20 to 2 to 1 (02) | links | 09, 02 | presenter heuristic |
| Journalist query time | 15 minutes a day | links | 09 | presenter heuristic |
| Foundational links | at least 30 profiles and citations | new store | 02 | presenter heuristic |
| Citation refresh | every 6 to 12 months | local | 03 | presenter heuristic |
| Citation service price | about $3.20 a listing | local | 03 | dated [web check] |
| Quality links needed | 10 to 20 relevant | "a lot of keywords" | 13 | presenter heuristic |
| Link pace | 4 a month baseline; 6 to 8 recommended | gap of about 98 domains | 02 | presenter heuristic |
| Link allocation first 3 months | 50 to 75% root domain, 25 to 50% collections ranking 4 to 10; 3 to 5 pages a month | new campaign | 02 | presenter heuristic |
| Prospect traffic floor | about 1,000 monthly visits | link prospect | 02 | presenter heuristic |
| Prospect authority floor | Authority Score 15 plus (02); 50 (08); DR or DA 30 plus (02 gap count, 01) | link prospect | 02, 08, 01 | vendor metrics, presenter floors |
| Guest post length | 600 to 1,200 words | host default | 02 | presenter heuristic |
| Cold email start | about 20 a day per account after warm-up | outreach | 02 | presenter heuristic |
| Link insertion price | $100 to $400 | paid (not allowed under ecomOS) | 13 | presenter spend |
| Insertion vs guest post cost | 20 to 30% cheaper | paid | 13 | presenter spend |
| Marketplace markup | 20 to 60% over direct outreach | paid | 13 | presenter spend |
| Paid placement range | $10 to $1,000 | paid | 05 | hedged guess |
| Digital PR service | about $5,000 a month | earned media | 13 | presenter estimate |
| DR needed to earn links at scale | 70 to 80 | organic link earning | 13 | presenter heuristic |
| Spam score bands | under 5 fine; 10 plus risky; 10 to 30 plus consider disavow (card: disavow only with manual action evidence) | backlink audit | 01 | presenter heuristic; card correction high |
| Link ROI timing | 3 to 6 months | links | 03 | presenter heuristic |
| SEO momentum timing | 12 to 13 months (06 client); "several months" per cluster (11); under 100 days to 11 months (13 cases) | expectations | 06, 11, 13 | examples, see 7.17 |
| Category focus period | about 90 days, sometimes 1 to 2 quarters | growth work | 04 | presenter heuristic |
| Assets for topic authority | "a couple hundred"; 250 to 500 across 5 channels | 1 category | 04 | presenter estimate |
| Weak ideas in AI topic lists | about 20% | AI planning | 04 | presenter estimate |
| Revision passes on AI drafts | 3 to 5 | AI content | 04 | presenter heuristic |
| Hand rewrite share | last 10 to 20% | AI content | 06 | presenter heuristic |
| Reading level | eighth grade (03); below tenth (ecomOS) | content | 03, house | medium |
| GEO content lift | about 40% AI Overview visibility | Princeton paper via 03 | 03 | unverified [web check] |
| AI citation source mix | over half from product pages, comparisons, buying guides (768,000 citations) | GEO | 14 | unverified [web check] |
| Publishing cadence | 2 a month minimum, weekly ideal (07); monthly cycle (06) | content | 07, 06 | presenter opinion |
| Publishing ramp | 1, 1, 2, 3, 4 posts over days 1 to 8 | programmatic release | 05 | presenter illustration |
| Templated page cap | avoid thousands, probably avoid hundreds | location or variant pages | 05 | presenter opinion |
| Request Indexing quota | about 10 a day (05); "a quota exists" (10) | indexing | 05, 10 | low [web check] |
| Indexing speed after request | about 1 day | indexing | 05 | presenter claim |
| Search Console retention | 16 months | reporting | 10 | high |
| Query export cap | 1,000 rows | reporting | 10 | high [verify UI] |
| Reporting comparison window | last 3 months vs previous; 6 months for a drop | reporting | 10 | presenter default |
| Low-volume noise | 2-position wobble on about 40 impressions | rank tracking | 10 | example |
| Low-hanging fruit positions | 4 to 10 (02); 9 to 30 (03); 6 to 8 refresh (10 vendor) | prioritization | 02, 03, 10 | merged 4 to 30, medium |
| Tracked keywords | 20 to 30, weekly | rank tracking | 08 | presenter heuristic |
| Collection share of organic revenue | over 80% for 50 plus products | Shopify | 02 | agency claim, unverified |
| Conversion from organic | 5 to 15% product pages; 2 to 5% collections | Shopify | 02 | agency claim, unverified |
| Site health benchmark | 92% "top 10% of sites"; AI search health 80% | Semrush Site Audit | 08 | vendor |
| Authority Score example | 47 "pretty good" | Semrush | 08 | vendor example |
| AI visibility example | 50 of 100 | Semrush | 08 | vendor example |
| Bounce triage floor | 50% plus on content pages | GA4 | 01 | presenter heuristic |
| Dwell time "good" | 2 to 5 minutes | GA4 | 01 | presenter heuristic |
| Alternatives list size | 7 to 10 competitors, brand first | comparison content | 04 | presenter heuristic |
| Competitors to compare against | 5 to 10 per category | comparison content | 04 | presenter heuristic |
| Core queries for a citation audit | at least 5 | AEO research | 04 | presenter heuristic |
| GBP images | 100 | local | 03 (BrightLocal) | unverified [web check] |
| GBP post length | under 1,450 characters | local | 03 | [verify UI] |
| Amazon share of product searches | about 50% | framing | 01 | unsourced |
| Google vs ChatGPT traffic | about 190x | framing | 09 | unsourced [web check] |
| Pages with 0 Google traffic | over 96% (Ahrefs, 14 billion pages) | framing | 09 | secondhand [web check] |

## 7. Where sources disagree

Each conflict: what each side says, when each is right, what the agent should do.

**7.1 Blog content is worthless vs blog content is core.** Source 13: informational blog traffic converts near 0% and blog-first agencies wasted $120,000 over 2 years; source 14: blog traffic and rankings alone are close to worthless in 2025; source 16: skip cold top-of-funnel articles. Against: source 02 says a Shopify store needs a blog to support collection rankings through internal links and topical authority (Q for Quinn's blog drives over half its organic traffic); sources 09 and 11 build clusters of 5 to 10 pieces around each money page; source 06 feeds Google monthly; source 07 posts at least twice a month. When each is right: the anti-blog side is right about generic, seasonal and lifestyle posts with no path to a money page, and for a store with no money pages built yet. The pro-blog side is right when the posts are buyer formats (comparisons, alternatives, best-for, buying guides), when the category is high-consideration, and when every post links into a hub. What the agent should do: build money pages first (R4); allow blog content only in the 4 buyer formats plus the educational pieces a cluster needs (R67, R68); require the internal link and citation rules (R46, R47); measure blog pages on assisted organic revenue, not traffic [needs brand data: assisted conversions by landing page].

**7.2 Backlinks are the top ranking factor vs content is.** Source 02's off-page presenter calls backlinks the most important factor "even more with the rise of AI content"; source 06 shows a weaker page with more authority outranking a better page; source 13 puts links in the 20% that drives 80% of revenue. Against: source 01 repeats "content is king"; source 05 does no off-page work at all and treats it as risky; source 11 builds the content cluster before any links; source 09 says publish 10 to 15 pieces before outreach. No source cites a ranking study. What the agent should do: treat both as necessary, not ranked (R5, R104); sequence content and technical work first, then links (R105); size the link effort from the competitor gap, not from a belief about weight (R111).

**7.3 Paid links "work" vs Google policy and ecomOS rules.** Source 02 acknowledges Google calls manipulative link buying spam, then says "everyone does it" and it works "provided you're doing it properly", and its process pays publishing fees for dofollow links. Source 13 buys insertions at $100 to $400. Source 03 recommends vendors (with a disclosed affiliate tie to 1). Source 05 quotes $10 to $1,000 for "quality" placements but does not do it himself. Source 04 says sponsored citations count as much as organic ones. Against: source 05 and 09 warn that bought links get penalized and $5-for-100 offers are PBNs; source 01 warns that partners delete links or demand more money; the card writers added `rel="sponsored"` or `rel="nofollow"` on sources 01, 05, 09 and 13, which no presenter said. What the agent should do: no paid or swapped links (R106). A sponsored placement is allowed only when disclosed, marked `rel="sponsored"`, and bought for referral traffic. Say this plainly to any vendor (P23). Any source procedure that includes "willingness to pay a publishing fee" is dropped from outreach (P17 step 2).

**7.4 Site speed is unnecessary vs page experience matters.** Source 13: speed "can help but is absolutely not necessary" and meta descriptions are noise; source 09: a modern CMS is 90% of the way there and beginners should not rabbit-hole. Against: source 01 fixes speed before chasing rankings; source 03 fixes anything below GTmetrix B immediately; source 07 lists speed under ranking checks; source 02 calls the ranking effect "slight" but the conversion effect real; Google's public guidance treats page experience as a ranking input. What the agent should do: keep the 4-item technical floor as the minimum (R86); treat speed as SEO work only when Search Console flags Poor URL groups on money templates (R100); do the 2 cheap fixes (images, apps) in P14; send everything else to 08-SPD; never sell speed work as a ranking guarantee.

**7.5 One category for a quarter vs sitewide work.** Source 04 concentrates almost all effort on 1 category for about 90 days and accepts that other categories wait; source 02 and 09 also build 1 cluster at a time. Against: sources 01, 02, 07 expect sitewide technical hygiene and template fixes across all pages; source 06 runs a monthly cycle across the store. What the agent should do: sitewide once (technical floor, templates, indexing), then concentrate content and links on 1 category or cluster per quarter (R6). No source says how much sitewide debt can be deferred; the agent reports the deferred list each month.

**7.6 Tight keyword shortlist vs broad long tail.** Source 11: pick a shortlist of business-driving terms and do not try to rank for everything; source 06: never chase every t-shirt variant at once. Against: source 09 tells new sites to start on long-tail terms and aggregate them; source 02 pulls about 21,000 terms for 1 seed and clusters them; source 14 splits 1 collection into many variant pages. When each is right: the shortlist is right for prioritization and for the first 90 days; the long tail is right as the cluster under each shortlisted term and as the entry point for a low-authority store. What the agent should do: shortlist the money terms, then expand each into its cluster (R30); never work a volume-sorted list top to bottom (R7).

**7.7 Template reuse across near-duplicate pages vs doorway risk.** Source 03: identical layouts across many location pages are not duplication if the on-page content differs (presenter experience only); source 14 multiplies 1 collection into many variant pages reusing the same products; source 05 zips services and cities into pages. Against: source 02 warns against "top rated", "most popular" and "on sale" copies with no unique value; source 04 uses a blog post instead of a near-duplicate category page when a broader page already covers the modifier; source 05 itself caps the count; the card on source 03 flags doorway risk. What the agent should do: a variant page needs its own demand, its own copy and a cap (R39, R51); reusing products across collections is fine, reusing copy is not; check Google's current doorway guidance before scaling past a few dozen pages [web check].

**7.8 Search Console Domain property vs URL-prefix property.** Source 10: Domain, because it covers shop., blog., checkout., www and non-www, http and https, at the cost of DNS verification. Sources 01 and 05: URL-prefix with the HTML tag; source 01 calls Search Console "sensitive" to variants (the card questions this). What the agent should do: Domain property by default (R97); URL-prefix only when DNS access is impossible, and then note that subdomains are not covered.

**7.9 Content length does not matter vs long guides and long descriptions.** Source 11: Google rewards completeness, not word count; source 09: match the average length of the top 5 as a benchmark, not a target. Against: source 02 prescribes 500 to 1,000 words on collections and products; source 06 wants 400 plus on collections; source 07 wants 300 to 400 on products; source 02 praises a post with about 10 infographics. What the agent should do: length follows the SERP and the topic (R70); use the source ranges as floors for a contested term, not as targets (R53, R61); never pad.

**7.10 Title length limits.** Source 01 says 150 to 160 characters early and about 60 later (its own audit cut a title from 73 to 54); source 03 says 45 to 61; source 08's tool flags over 60; sources 02 and 09 say about 60; source 07 shows a 70-character Shopify homepage field. The card on source 01 notes Google sets no character limit and display depends on pixel width. What the agent should do: keyword first, about 60 characters, and check the rendered SERP (R52); ignore 150 to 160.

**7.11 Speed targets.** Source 01 gives 1 to 2 s, under 3 to 4 s, and under 1 s max 2 s in different places; source 03 gives under 1.9 s good, over 3 s losing money, PageSpeed 80 plus, GTmetrix B; source 05 targets Lighthouse 100 on all 4 scores; source 01 still names FID. What the agent should do: no single target from these sources (R101); log the baseline and use 08-SPD's protocol and Google's current Core Web Vitals thresholds [web check].

**7.12 Index every product vs noindex low-demand products.** Source 02 noindexes products with no search volume and shifts effort to the collection; the common alternative (not in these sources, noted by source 02's card) indexes every product for long-tail coverage. What the agent should do: index products that have their own demand (R59); for the rest, keep them crawlable and linked from the collection, and decide noindex per catalog; record the decision in the architecture spec.

**7.13 Static rendering required vs Google renders JavaScript.** Source 05: without static generation "you can't really rank on Google whatsoever"; the card corrects it: Google can execute JavaScript and rendering support differs by crawler. Source 15: most AI crawlers see load-time HTML only, Gemini excepted. What the agent should do: money-page content in initial HTML, JavaScript-off test, URL Inspection rendered view (R95); static generation is a safety margin, not a gate.

**7.14 Syndication vs duplicate content.** Source 01 both warns against republishing identical articles across sites (Panda recovery) and recommends syndication on Reddit, Medium and Flipboard; source 04 publishes LinkedIn variants. What the agent should do: syndicate only rewritten variants with the original canonical on the store, on disclosed brand channels (R75); no community link drops (R85).

**7.15 Links to blog posts vs links to money pages.** Source 02 and 11: earn links on educational pages and the root domain, pass authority inward; linking heavily to shopping pages "looks unnatural". Source 13 points its bought insertions at the money pages themselves. What the agent should do: educational pages and root domain first, money pages through internal links (R108); the source 13 method is paid and excluded anyway.

**7.16 Disavow on a spam score vs disavow only with a manual action.** Source 01's transcript uses spam-score bands mechanically; its card says most sites never need to disavow and to check Manual Actions first. What the agent should do: follow the card (R113).

**7.17 Timelines.** Source 13 calls "6 to 12 months" a myth; source 06's client took 12 to 13 months; source 03 expects 3 to 6 months for links; source 11 expects several months per cluster plus more months for results; source 01 refuses a date. What the agent should do: promise no date (R2); report leading indicators from month 1 (R126) and organic revenue at 3 to 6 months (R137).

**7.18 AI search is the same as SEO vs a separate discipline.** Sources 03, 05, 09 and 08 say ranking in Google or Bing is the prerequisite and the same fundamentals carry over; source 04 and 15 build separate workflows (citation blends, agent readiness, Found-Matched-Chosen) on top. What the agent should do: fundamentals first (R118), then the specific-page formats (R119), then hand the separate workflows to 16-AEO (R123). Re-check how each engine sources answers; it changes [web check].

**7.19 llms.txt.** Source 08 presents it as the AI equivalent of robots.txt; the card notes Google does not use it and other engines' support is unverified. What the agent should do: do not sell it as a fix (R122); creating the file is harmless, promising results from it is not.

**7.20 Volume floors.** 100 (05), 500 (01), 1,000 (06), 5,000 (08) searches a month; source 03 says a tool's 0 does not override niche knowledge. What the agent should do: set the floor per catalog and margin and write it in the keyword map (R23); the 5,000 floor from the Semrush demo would empty most niche stores' maps.

## 8. Common mistakes

Merged from all sources and deduplicated, with the fix.

1. Doing SEO for a product nobody searches for. Fix: R1 demand check first.
2. Promising a rank or a date. Fix: R2; report leading indicators.
3. Reporting raw clicks or rankings as success. Fix: R3, R125; organic revenue and non-branded clicks.
4. Writing 10 blog posts before any money page exists. Fix: R4.
5. Chasing head terms owned by giants with a new store. Fix: R18, R16.
6. Building a product page for a term whose SERP is all guides, or a guide for a term whose SERP is all collections. Fix: P5.
7. Copying a presenter's volume floor or KD ceiling. Fix: R23.
8. Keeping competitor brand names, mascots and job-seeker queries in the map. Fix: R26.
9. A product page and a collection page on the same keyword. Fix: R38.
10. "Top rated", "on sale" and "most popular" clones of 1 category. Fix: R39.
11. Expecting Shopify filter URLs to rank. Fix: R40.
12. Leaving tag, vendor and type pages indexed. Fix: R41.
13. Leaving `/collections/x/products/y` duplicates in place, or fixing them and leaving breadcrumbs broken. Fix: R42.
14. Deploying a Shopify robots.txt before the URL fix. Fix: R94, P2 order.
15. Separate pages per colour variant with no demand. Fix: R43.
16. Deleting an out-of-stock or discontinued page that had rankings. Fix: R50.
17. Redirecting a dead page to an unrelated page or always to the homepage. Fix: R92.
18. Using the Shopify hidden toggle to drop a page from the sitemap (it forces noindex, nofollow). Fix: R93.
19. Submitting the sitemap before setting the primary domain. Fix: P1 step 3.
20. Blocking a wanted path in robots.txt, or assuming robots.txt removes a page from the index. Fix: R94.
21. Blocking AI crawlers by accident through an app's robots edit. Fix: R94, re-check after installs.
22. A bare collection page with an H1 and a grid. Fix: R53.
23. Deleting the collection description to keep the grid high. Fix: move it below the grid (R53).
24. Keyword-stuffed or obviously AI filler on collections and products. Fix: R77, R79.
25. Product titles that say nothing ("Sweet Honey Bomb"). Fix: R60.
26. Manufacturer copy reused across every seller. Fix: R61.
27. Vague marketing copy with no size, colour, material or use case. Fix: R61.
28. Image files named by number and alt text repeated across images. Fix: R62.
29. Stock or generated images standing in for the real product. Fix: R83.
30. Lazy-loading the hero or main product image. Fix: R102.
31. Reviews and FAQs injected by a widget after load. Fix: R66.
32. Assuming the theme's default schema is complete. Fix: R64, P8.
33. Trusting 1 validator; trusting an AI's schema fix without re-validating. Fix: P8.
34. Incentivised or bought reviews. Fix: R63.
35. 2 H1s from a custom section; an H1 that is a tagline. Fix: R57.
36. Bare-keyword search engine listings. Fix: R56.
37. Long, filler-word URL handles; changing a handle without the redirect box. Fix: R45.
38. Orphan pages; links only in header and footer. Fix: R46, R49.
39. "Click here" and brand-name anchors. Fix: R46.
40. Blog posts with no link to a money page and no citation. Fix: R47.
41. Branching into shoulder niches before the core is covered. Fix: R7.
42. Working a volume-sorted list top to bottom across unrelated topics. Fix: R30.
43. Publishing seasonal and lifestyle posts. Fix: R67.
44. Restating the AI Overview. Fix: R72.
45. Targeting word count instead of completeness. Fix: R70.
46. Publishing the first AI draft, or a spun draft. Fix: R79.
47. Running the SEO checklist pass and losing the voice. Fix: R81.
48. Auto-publishing from a pipeline; auto-replying to negative reviews. Fix: R80.
49. Automating before the fundamentals work. Fix: R80.
50. Bulk-publishing hundreds of pages at once. Fix: R74.
51. Parasite pages and community link drops. Fix: R85.
52. Buying links, swapping links for discounts, $5-for-100 offers, unsolicited link sellers. Fix: R106, R110.
53. Building far more links to 1 page than competitors have. Fix: R104.
54. Exact-match anchors everywhere. Fix: R109.
55. Sending outreach from a cold account at full volume with an unmodified template. Fix: R112.
56. Answering journalist queries with a plain Google search. Fix: P16.
57. Disavowing on a third-party spam score. Fix: R113.
58. Hiring a link vendor without a named client site and dates. Fix: R117.
59. Paying a low retainer for blog posts only. Fix: R136.
60. Accepting an audit with dozens of "critical" fixes beyond the 4 essentials. Fix: R136, R86.
61. Treating a crawler's health score as clean. Fix: R87.
62. Rewriting a page stuck at "crawled, not indexed" on a new site instead of building authority. Fix: R89.
63. Reacting to a 2-position wobble on 40 impressions. Fix: R126.
64. Reading branded position 1 as competitive strength. Fix: R10.
65. Judging a click drop as a ranking drop without checking CTR and the AI Overview. Fix: R128.
66. Comparing Ahrefs and Semrush numbers as if equal; treating DA as a KPI. Fix: R12.
67. Leaving old tags active and double-counting events; text-matching button clicks that later change label. Fix: P1, 06-MEA.
68. Reading a worldwide AI visibility score for a single-country brand. Fix: R121.
69. Treating an AI crawler's server hit as a citation. Fix: R121.
70. Selling llms.txt as a fix. Fix: R122.
71. Chasing a perfect audit score or a 10 out of 10 writing score. Fix: R87.
72. Ignoring code freshness and orphaned metafields. Fix: R98.
73. Reading the Semrush free-tier bypass or any dated price as current. Fix: section 11.

## 9. Deliverables

**9.1 Keyword map.** A sheet with 1 row per cluster: primary keyword, secondaries, intent, volume, KD, CPC, SERP format and features with the check date, page type, target URL, current position, status (published, refresh, quick win, needs publishing), owner, priority tier. Header lines state the volume floor, the KD ceiling and the tool used. Gap tab: Missing and Weak terms vs named SEO competitors. Question tab: PAA and Search Console questions mapped to pages.

**9.2 Site architecture spec.** The page tree (home, collections, subcollections, products, blog hubs) with 1 parent per page; URL patterns; the noindex list (tags, vendors, types, utilities, low-demand products); the facet rules and the list of filter combinations that get real pages; variant handling per product family; redirect map for merged or removed pages; the Shopify fix list (P2) in order; the internal link plan per hub (spokes, siblings, anchors); the menu spec; the templated-page cap with the justification per page.

**9.3 Page brief per template.** Named so an agent or a client can ask for one by name: the **PDP brief** (product template), the **collection brief** (collection template) and the **guide brief** (blog or buying-guide template), plus a filled brief per page being built. Each brief carries: primary and secondary terms; SERP format and features; title tag, H1, URL handle; short and detailed copy sections with word ranges; the facts that must appear (specs, sizes, materials, prices); FAQ questions with sources; review handling; image list with real photos, file names and alt text; schema types; internal links out (hub, siblings, money page in the first 100 to 200 words) and in; citations required; the human moat items; reading-level and claim rules; the human quality gate sign-off line.

**9.4 Technical fix list with priority.** One row per issue: URL or template, issue, evidence (crawler, Search Console, view source), priority (P1 money page not indexed or 404; P2 duplication, canonicals, robots, sitemap; P3 titles, metas, alt, schema warnings; P4 speed and notices), owner (agent, developer, host, app vendor), status, verification method, date fixed. The 4 essentials appear at the top; speed items carry a pointer to 08-SPD.

**9.5 Link plan.** Targets on your site (educational pages and root domain first); the gap number (own vs competitor referring domains at DR or DA 30 plus, dofollow); the monthly pace; the tactic mix (journalist queries, be-the-source assets, broken-link replacement, resource pages, editorial guest posts, disclosed sponsored placements for traffic only); the vetted prospect sheet (5-point screen, authority, traffic, contact, value offer, status); the compliance line stating no paid, swapped or bulk links and `rel="sponsored"` on any paid placement; the monthly log of placements with anchor, target and rel attribute.

**9.6 Monthly SEO report.** Organic revenue and organic purchases (GA4) vs prior period; non-branded and branded clicks and impressions vs prior 3 months (Search Console); positions for the 20 to 30 money keywords; indexed money pages and any exclusions found; pages gained and lost (click difference); CTR triage actions; refreshes and new pages published with links; links earned with source and rel; Core Web Vitals Poor groups; schema errors; AI visibility notes (manual check, generative AI report); the deferred list; next month's plan in the cycle order. Written below tenth grade, digits, no em dashes, no mention of GPT or .env on client pages.

## 10. What needs live data or a web check

**Needs brand data.**
- AOV, margin, paid spend, branded search volume (R1, R10).
- Catalog tree, SKU counts per collection, variant structure, parent collection per product for breadcrumbs (P2, P4).
- Organic revenue and assisted conversions by landing page and template (R3, R58, 7.1).
- Search Console history: brand queries, positions, not-indexed groups, question queries, links (group N).
- Own and competitor referring domains and backlink exports (R29, R111).
- Named SEO competitors that outrank the store for money terms (R9).
- Existing content inventory with URL, target keyword, status (R28, 5.7).
- Brand voice document, banned words, real facts, stories and stats for prompts (R78).
- Real product photography and specs (R61, R62, R83).
- Unincentivised reviews and testimonials (R63).
- Physical locations, if any (R138).
- App list and which apps edited robots.txt or left metafields (R94, R98).
- Who owns theme code and whether a duplicate theme exists (P2).
- Mobile share of sessions and revenue (P14).
- The actual setup prompt and Claude.md template from sources 05 and 12 if Kevin has them (they are gated and not reproduced).

**Web check.**
- Current Core Web Vitals set and thresholds; INP replaced FID in March 2024 (R100, R101).
- Current Google guidance on sponsored and nofollow attributes, paid links, doorway pages, site reputation, E-E-A-T (R106, R51, R65).
- Search Console: Domain property verification flow, Request Indexing quota, export cap, generative AI report status (June 2026 beta, impressions only), platform properties (announced July 2026), AI Overviews opt-out rollout (R90, R97, R121).
- Whether Google still ignores the sitemap priority attribute (R93).
- Current AI crawler user agents (ClaudeBot, CCBot, GPTBot and others) and each engine's rendering and retrieval behaviour; Gemini as the JS exception (R94, R95, R118).
- llms.txt adoption by any engine (R122).
- FAQ and spec-table rich result eligibility (R55).
- Tool names, prices and limits: Semrush One at $199 a month and the free-tier bypass; Ahrefs tiers and credit pricing; Screaming Frog 500-URL free tier and licence; Sitebulb; Keyword Cupid; Crush Pics; SEO Ant; Surfer features; Rankability; DataForSEO; Answer Socrates; Machined AI; Arvo; the scheduler in source 12 (name unclear); Napkin.ai; Snov.io, Hunter.io, Instantly; BrightLocal pricing (section 6).
- Journalist platforms: Featured.com free tier, Source of Sources, Connectively status (R107).
- Shopify: current admin paths for redirects, metafields, robots.txt.liquid, the sitemap exclusion method, the "agentic storefront" setting and global catalog requirements, Dawn and Palo Alto theme names (P2, R120).
- Studies cited secondhand: the Princeton GEO paper and its 40% figure; the 768,000-citation study; the BrightLocal 100-image study; Ahrefs' 96% zero-traffic figure; "190x" and "5 trillion searches" (section 6).
- Presenter identity and claims where attribution matters: source 13's $40 million, source 14's $800 million brand and the "Simbotanica" result, source 16's 5-hour ranking claim, source 05's $500,000.
- The mis-transcribed ransomware name in source 09's internal-link example before reusing it.
- The claude.ai domain authority figure and whether public artifacts are indexed (source 16; not to be used under R85 anyway).

## 11. Freshness and stale-risk notes

- **Tool UIs and pricing.** Every menu path in P1, P2, P3, P13 and P15 is a point-in-time screen. Semrush ($199 a month, 14-day trial by referral, the free-tier bypass), Ahrefs tiers, Screaming Frog limits, SEO Ant's discount code and score, Surfer's feature names, Rankability, DataForSEO's Sheets add-on and Machined AI's model names all drift within months. Re-verify before quoting a price or a click path to a client. Quarterly.
- **Google features.** Search Console's generative AI report (beta, June 2026, impressions only), platform properties (July 2026, gradual), the AI Overviews opt-out toggle (UK first), Request Indexing quotas, FAQ rich results (already declining at source 02's 2024 recording), the sitemap priority attribute. Re-check monthly during the monthly read.
- **Core Web Vitals.** Source 01 teaches FID and Flash; source 05 chases Lighthouse 100; INP replaced FID in March 2024. Use 08-SPD and web.dev for thresholds. Quarterly.
- **AI search behaviour.** Which engines use Bing's index, whether Gemini alone renders JavaScript, how citations are chosen, whether LinkedIn and Reddit remain heavily cited, the "60% of searches by agents" guess in source 04. Everything in group M can change in a quarter. Re-check quarterly and route depth to 16-AEO.
- **Dated course content.** Source 01 is stale on Flash, FID, sitemap priority and URL-prefix properties. Source 02 is 2024-era (HARO as Connectively). Source 06 is titled 2025 with a Semrush free-tier trick. Source 09 and 13 quote figures without dates. Source 16's whole tactic depends on a third-party platform's indexing behaviour. Treat named years in titles ("2026") as marketing.
- **Google policy.** Sponsored and nofollow rules, doorway and scaled-content policies, site reputation abuse. The card-writer corrections in this playbook assume the current policy; re-read it before any link or programmatic work. Quarterly.
- **Shopify admin.** Redirect UI, metafield and metaobject paths, robots.txt.liquid, theme file names (`main-collection-product-grid.liquid`), the hidden SEO toggle, Search and Discovery app, Sidekick, the agentic storefront and global catalog. Re-verify on every store.
- **Journalist platforms.** HARO became Connectively; Source of Sources and Featured.com are named as current; free-tier limits change. Before each outreach cycle.
- **Model names and prompts.** GPT-5 variants, Perplexity Sonar, OpenRouter credits, Claude Code skills and scheduling, the Antigravity workspace in source 05. The prompts in sources 03, 05 and 12 are mostly not reproduced; do not invent them. Re-check on each use.
- **24 Sep 2026: ecommerce specificity pass applied from ECOM_REVIEW.md; priority block added, 13 rules reworded, 8 levers added, about 1,850 words moved to Appendix A.**

## 12. Source index

| No. | Title | Type | Credibility and bias | Contributed most |
|---|---|---|---|---|
| 01 | SEO Full Course 2026 for Beginners (Simplilearn) | course transcript, auto-generated | Generalist, no presenter credentials, sponsored certificate pitch at the start, stale on Flash, FID, sitemap priority, title length (150 to 160 then 60) and URL-prefix; casual about paid and reciprocal links, corrected by its cards. Low to medium. | GA4, Search Console and Tag Manager setup; add-to-cart tracking; 404 and CTR triage; schema via generator and GTM; keyword and gap workflows; disavow caution (card). |
| 02 | Beginners Guide to Shopify SEO, 607 Media | 4-hour agency course | Shopify agency funnel ("10x Accelerator", $20,000 a month profit pitch); unaudited client numbers; undisclosed tool ties possible; states that paid links "work". Medium on Shopify mechanics, low on link ethics. | Shopify URL duplication, breadcrumbs, noindex classes, robots order, variants, sitemap trap; topical map; collection and product templates; prospect screen; anchor rules; link gap pacing. The backbone of groups D, E, F. |
| 03 | Complete SEO Course, Rank #1 AI Search | course transcript | Practitioner with a paid community; affiliate links (DataForSEO, Machined AI, Get Me Links with a personal tie); all examples local-service, none ecommerce; prompts referenced not reproduced. Medium. | AI content workflow with tone document and negative words; GEO principles; two-bucket intent; tool data as guide; automation after fundamentals; auto-reply only to 5-star. |
| 04 | Ecommerce SEO: The Definitive Guide (Rankability) | vendor demo | Founder demoing his own SaaS on a brand he has no data for; "99.9% of variables" and "60% agents" unsupported; endorses paid citations and aged-account Reddit posting without disclosure notes. Low on claims, medium on workflow. | One category per quarter; awareness-stage content plan; citation blend sheet; comparison content rules; hub-and-spoke; AI draft fact-check passes; CCBot and code freshness. |
| 05 | Claude Code + SEO Masterclass | video transcript | Self-reported $500,000 and 50,000 clicks with no company named; plumbing demo; gated Claude.md; overstates static rendering (corrected by card); Pexels stock images; off-page section theoretical. Low to medium. | Keyword filters (KD 30, volume 100); on-page checklist counts; Lighthouse loop; skill packaging; publishing ramp; vendor vetting by client site and dates. |
| 06 | Complete Shopify SEO Optimization Masterclass 2025 | webinar transcript | Sells a $99 course; Semrush bit.ly link and free-tier bypass; self-reported $1 million store; no speed, schema or link how-to. Medium on cadence and prompts. | Monthly cycle; C plus volume plus KD plus CPC filter; collection before product; CTA listings; persona prompts; 10 to 20% hand rewrite; 12 to 13 month client timeline. |
| 07 | Shopify SEO Optimization Guide for Beginners 2026 | screen-recorded walkthrough | SEO Ant affiliate code (35% off); demo store only, no outcomes; app scores presented as heuristics. Medium on Shopify field mechanics. | Keyword Planner and Trends routine; homepage, product, collection fields; single H1 audit; alt text pattern; handle redirects; image size and LCP rule; sitemap after primary domain. |
| 08 | Semrush Tutorial 2026, Semrush One | sponsored tutorial | Disclosed paid partnership; every step is a Semrush feature; single demo brand; Authority Score and Site Health benchmarks are vendor numbers; llms.txt overstated (corrected by card). Low as independent advice, useful as a tool map. | Keyword Magic filters; Keyword Gap Missing and Weak; clustering to a calendar; Site Audit order; Backlink Gap; Position Tracking cadence; AI visibility region rule. |
| 09 | Learn Everything About SEO and AI SEO in 50 Minutes | course transcript | Surfer promotion and affiliate link; client examples without data; secondhand Ahrefs stat; sponsored note added by card. Medium on strategy, low on tool claims. | 30-second intent test; Sweet Spot framework; money pages then 1 cluster; content blueprint and human moat; on-page checklist; be-the-source links; technical triage; 30-day plan; leading indicators. |
| 10 | Google Search Console Tutorial (2026) | tutorial transcript | Surfer Academy vehicle; 2 client examples; Google roadmap claims unverified; refresh bands are vendor settings. Medium to high on native Search Console mechanics. | Domain property; non-branded regex; not-indexed litmus test; URL Inspection reasons; traffic-drop method; retargeting; question regex; Links report; watch pages; generative AI report. |
| 11 | How to Rank #1 in Google in 2026: 3-Step Playbook | talk transcript | Surfer-sponsored; 1 SaaS case; E-E-A-T weight attributed to unnamed sources; no ecommerce examples in the transcript. Medium on prioritization. | Shortlist first; 5-plus majority SERP rule; roundup backdoor; completeness over word count; E-E-A-T audit; links to educational pages then inward. |
| 12 | Claude Code Full Content Automation | promotional talk | Affiliate for Arvo and a scheduler; prompt withheld as a lead magnet; no numbers at all; "hockey stick" charts unquantified. Low. | Human approval gates in a pipeline; bottom-of-funnel targeting; blog to money page loop; draft-first publishing; LLM brand monitoring as a category. |
| 13 | $40,000,000 Worth of Ecommerce SEO Advice in 11 Minutes | talk transcript | Agency lead-gen (discovery call); self-reported $40 million; buys link insertions; anti-blog framing suits its service; calls speed unnecessary. Low on ethics, medium on prioritization. | 4 technical essentials; organic revenue as the KPI; 10 to 20 links; 80/20; agency red flags; Keyword Planner CPC proxy; lean tool stack; digital PR costs. |
| 14 | Steal These Shopify SEO Hacks to Rank #1 Overnight | talk transcript | Daily Mentor funnel; $800 million and "1,000 founders" unverified; "overnight" unsupported by its own 6-month example; unnamed 768,000-citation study. Low on claims, medium on tactics. | Demand-and-margin filter; branded search from ads; collection splitting with KD 35; 4 blog formats; internal link placement and anchor rules; GEO citation formats. |
| 15 | Get Your Shopify Store AI-SEO-Ready in 5 Minutes | talking-head transcript | Self-described "a bit of research"; 1 affiliate example; bootcamp pitch; no outcomes. Low to medium; useful checks. | Found, Matched, Chosen; robots and curl check; JavaScript-off test; explicit product facts; Shopify global catalog eligibility; stale metafields. |
| 16 | Rank #1 on Google in 5 Hours with Claude Artifacts | podcast transcript | Secondhand claim, untested by the host at recording; pitches his own keyword product; parasite tactic with platform and disclosure risk. Very low; kept only to explain why R85 exists. | Bottom-of-funnel priority restated; the parasite tactic the agent must refuse. |

**Neighbour folders and what lives there.**
- 08-SPD-speed: measurement protocol, images, apps, theme code, fonts, CLS, LCP, INP, caching, hosting. This playbook only decides when speed is an SEO blocker (R100 to R103, P14).
- 16-AEO-answer-and-generative-engines: citation research, prompt research, fan-out modelling, brand sentiment in LLMs, agent readiness, CCBot policy, AI visibility trackers. This playbook keeps R118 to R123 and P22.
- 12-GAD-google-ads: paid search, Shopping, Keyword Planner as an ads tool, landing page tests with paid traffic (source 05's 20% conversion test lives there).
- 06-MEA-measurement: GA4 and Tag Manager setup, event tracking, attribution. This playbook keeps the organic reads (group N).
- 07-LPG-landing-pages: page layout and first-fold design (source 03's CRO screenshot critique).
- 13-ORG-organic-and-content: social repurposing, RSS to social, scheduling (source 12's bonus workflow), content operations beyond SEO.
- 22-AMZ-amazon-marketplace: marketplace listings that R11 points to.
- 23-SEC-bot-and-agent-security: which bots to allow or block for security reasons; this playbook only decides for search and AI visibility.
- 05-SET-store-setup: brand settings, domains, non-search store fields (source 07's brand information tab).
- 11-ADC-ad-copy-deployment and 24-DEP-ad-deployment: nothing from this folder; listed so the agent does not route SEO copy there.

## Appendix A. General background

Rules moved here on the 24 Sep 2026 ecommerce specificity pass. Each keeps its original rule id, condition, sources and card ids; only the location changed. They apply to any website, not only a store, and are kept for completeness and for the cross-references that still point to them from sections 3 to 10.

### A.1 How search works and query intent (from Group B, section 3)

**R14. On a store, the most common break is a money page (a collection or product) sitting behind noindex, a robots block, or a Shopify duplicate-URL path; check those before anything else.** Condition: diagnosing any ranking problem. Start at crawl (can the bot reach the page), then index (is it stored), then rank (is it competitive). Source 15 maps the same 3 stages onto AI search as Found, Matched, Chosen. Sources: 01, 09, 15. Cards: [4d7e19f8ea9d] [2a24068d5a43] [7c2ebc1068d0] [2a7d0c66c403].

**R17. Read the SERP features too: an AI Overview means the term is also an answer-engine target; a video carousel means a text page alone will not win.** Condition: the same SERP read as R16. Source 08 shows the AI Overview in the keyword tool's SERP panel. Source 09: AI Overviews now appear on commercial and transactional queries, so the page must add what the summary cannot. Sources: 08, 09, 10. Cards: [1449fb3da4a7] [f32610667b5f] [245141abe8fc].

**R18. A new or thin-catalog store should target its specific product and attribute combinations before its category head term; a full-catalog store can spread across both once its top categories rank.** Condition: any store that does not already rank for its category head term. Source 09's example: "coffee" at about 650,000 US searches a month has a mixed SERP; "best dark roast coffee beans for espresso" has a few hundred searches and a uniform buying-guide SERP. Source 15 applies the same logic to AI answers: "shoes" goes to big brands, "vegan waterproof trail running shoes" is winnable. Source 03: chase low-difficulty first, not shiny high-volume terms. Sources: 09, 15, 03, 05, 08. Cards: [f32610667b5f] [2a7d0c66c403] [d2b1c9b1538f] [1449fb3da4a7].

### A.2 AI-assisted content hygiene and automation caution (from Group H, section 3)

**R77. Product and collection copy generated from a spec sheet with no added detail reads as thin to Google the same way a scraped manufacturer description does; add what the manufacturer sheet does not have.** Condition: any AI use in content. Source 06's team published many AI posts, ranked, then lost value in a Google sweep. Source 01: verbatim AI without added value is recognized and devalued. Source 03: the source of a draft does not matter, the quality does. Sources: 03, 01, 06, 09. Cards: [0b71c176e2e3] [4c3f55273a76] [f6a17ed1177e] [5ff1064a03ea].

**R79. Human gates at every stage: approve the title and keyword list, review the draft, fact-check every number and claim, rewrite the weak 10% to 20% by hand, and publish only from a draft state; the ecomOS quality gate (reading level, digits, short sentences, no invented claims, no em dashes) runs last.** Condition: every AI-assisted page that reaches a client store. Source 12's own default is draft, then manual publish. Source 04 expects 3 to 5 revision passes and no "contact for pricing" placeholders. Source 06 rewrites the last 10% to 20% by hand and rejects spinning tools. Source 05 warns the SEO checklist pass often strips the voice. Sources: 12, 04, 06, 03, 05. Cards: [6e4f81398cf7] [17c5ce84a5ee] [f6a17ed1177e] [0b71c176e2e3] [aeeccc51cf9d].

**R80. Automate only after the fundamentals work, and let only low-risk, reversible actions run without a person.** Condition: any pipeline. Source 03 has seen "absolute horror cases" of automation on broken foundations; his automations auto-reply to 5-star reviews only. Source 12 keeps approval gates between research, generation and scheduling. Sources: 03, 12. Cards: [3b53ab90208b] [39455049b596] [3707612ddae8] [6e4f81398cf7].

**R81. Package a repeatable workflow as a reusable skill or prompt set in a local project folder that holds brand assets; re-run the voice check after any SEO checklist pass.** Condition: after 1 piece has been produced by hand end to end. Sources 05 and 12 build a "blog" skill; source 05 starts a fresh session for it to take effect. Sources: 05, 12. Cards: [cd866609b795] [7ad5eaa168b2] [09eb0afacdd2] [ab48255e465e] [aeeccc51cf9d].

**R82. Use AI to read exports, not to invent data: feed Search Console CSVs and the sitemap to a model for gap lists, then validate demand and difficulty before committing.** Condition: monthly analysis. Source 10 exports up to 1,000 query rows. Source 03 feeds the last 28 days into a custom GPT. Sources: 03, 10. Cards: [3f3f7fbd3c01] [d2808d386582] [7a14782ab0f1].

**R84. Write at or below an eighth-grade reading level for content and below tenth grade everywhere (ecomOS rule).** Condition: every page. Source 03 cites the GEO paper's eighth-grade target. Sources: 03. Cards: [7e809a393a1d]. Enforced in this playbook as the ecomOS override R143.

**R85. Do not run parasite SEO: no published AI articles on third-party domains posing as editorial content, no link drops in lightly moderated communities, no undisclosed brand mentions in Reddit threads.** Condition: always (ecomOS override). Source 16's Claude Artifact tactic is untested by its own presenter and depends on a domain you do not control. Source 04 describes aged-account Reddit posting as "commonly used" without flagging disclosure rules. Source 04's LinkedIn company-page variant is allowed because it is a disclosed brand channel. Sources: 16, 04. Cards: [3adc2f4b92d2] [d671d4362dd1] [e54f1c0e014f] [70d7dddf86e4]. Enforced in this playbook as the ecomOS override R141.

### A.3 Link-building doctrine (from Group L, section 3)

**R104. Links matter, relevance beats volume, and a modest number of good links is the goal: source 13 says 10 to 20 relevant links "for a lot of keywords".** Condition: any link plan. Source 03: 1 relevant link from a reputable site beats 100 spammy ones; check that the referring-domain curve grew naturally, not in spikes. Source 01 judges a link by placement, anchor and source authority (its DA 30 to 40 floor is a heuristic). Source 02: never build far more links to 1 page than competitors have (10 vs 30 "sticks out"). Sources: 13, 03, 08, 02, 01. Conflict on whether links are the top factor: 7.2. Cards: [8901669ff766] [691b416017c3] [c5e862cbcad9] [d959e63d9769] [6e87a52bb240].

**R105. Sequence: content first (10 to 15 good pieces), then foundational profiles and citations (about 30, filled out fully), then earned links.** Condition: a store starting link work. Source 09 and 11: no outreach before the content exists. Source 02's foundational layer: social profiles, directories, Web 2.0 profiles, "entity stacking". Source 01: directories judged by relevance and authority, never mass submission. Sources: 09, 11, 02, 01, 03. Cards: [88997600260b] [1293de3e1c27] [d00b480b316f] [9ef468a1aa73] [a3d1dead77d7] [9fac54461fc4] [f943f246de27].

**R107. Earn links from journalist queries, being the source, linkable assets, broken-link replacement, resource pages and unpaid editorial guest posts.** Condition: the link plan after R105. Journalist platforms: Featured.com (source 03: about 3 free answers a month), Source of Sources (source 09), Connectively (source 02, the HARO successor at recording); budget 15 minutes a day and expect about 1 hit per 100 submissions (source 09) or 20 answers to 2 replies to 1 link (source 02). Be the source: Counterculture's brew guide is cited by WikiHow, Gear Patrol and Breville. Broken-link swap: find 404s on niche hubs, offer your page. Guest posts: search `"[niche]" "write for us"`, write for the host's audience, 600 to 1,200 words, anchor in a relevant sentence near the top. Sources: 09, 02, 03, 05, 01. Cards: [88997600260b] [e0058ce635d6] [493daec89c20] [7f70083e00d5] [54ad628b63cd] [0d17f081b5be] [03b3bc6a6a34] [5ad59b6f29ec] [ee0764e85157] [d3cac352bc44] [cfd93f4f1fcb]. [web check: current names and status of Featured, Source of Sources, Connectively]

**R109. Anchor text is mostly partial, URL, brand and topic; exact match stays rare; calibrate against the top 3 competitors' anchor mix.** Condition: any placed link. Source 02 leans on soft anchors for months 1 to 5. Sources: 02. Cards: [fab6f93fabc4].

**R110. Screen every prospect: a real single-topic site, clean domain history on the Wayback Machine, topical relevance, at least about 1,000 monthly visits and no sudden drop, a clean backlink profile of its own; refuse Fiverr-style offers, "$5 for 100 links" and unsolicited link sellers.** Condition: before any outreach or acceptance. Source 02's 5-point check plus Authority Score 15 or more (raise it as your profile grows); source 08 filters Backlink Gap at Authority Score 50; source 02's gap analysis counts DR or DA 30 plus dofollow. Sources: 02, 08, 05, 03. Cards: [102c5f4bc1f8] [931c46ea6362] [c5e862cbcad9] [0878cf8caa37] [691b416017c3].

**R111. Set a monthly link pace from a gap analysis: your referring domains (DR or DA 30 plus, dofollow) vs the competitor average, closed over a set period.** Condition: link plan sizing. Source 02's example: 105 vs about 203, a gap of about 98, about 4 a month over 24 months, with 6 to 8 a month recommended. Sources: 02. Cards: [be35a3453380]. [needs brand data: own and competitor referring domains]

**R112. Outreach is personalized and offers something better: a current, tested replacement for an outdated page, a real expert answer, a resource the host's readers want; warm up sending accounts and start around 20 emails a day per account.** Condition: any outreach. Source 02 estimates personalized pitches beat about 70% of template senders. Sources: 02, 11. Cards: [ed27a5301c83] [79c14ba1ded5] [6e04ce7fcb0e] [1293de3e1c27].

**R113. Most sites never need to disavow; investigate Manual Actions and link-scheme history first and reserve disavow for manipulative links tied to an actual or likely manual action.** Condition: backlink audit. Source 01's transcript uses spam-score bands (under 5 fine, 10 plus risky, 10 to 30 plus consider disavow); the card corrects it to the cautious rule. A DR 0 referring domain is not automatically bad. Sources: 01. Cards: [fe47b8b67efd] [e592af67a06c] [ade5208b890b].

**R114. Reclaim lost links: check the Lost and Vital view for high-authority links that disappeared and ask whether it was a broken URL or a removal.** Condition: monthly. Sources: 08. Cards: [2b4bd20978c0].

**R115. Digital PR and organic earning at scale cost real money and time (source 13: about $5,000 a month for a PR service) and mostly work for brands already at DR 70 to 80; budget it as a later stage.** Condition: link plan for a small or mid brand. Sources: 13, 02. Cards: [248b6ed3e810] [4143ac10dcfc].

**R117. Vet a link vendor or agency by asking for 1 named past client site with campaign start and end dates, then checking that site's traffic trend across the window; a decline is a refusal.** Condition: any paid link help, which ecomOS only allows for disclosed sponsored placements. Source 05's "top 1%" Upwork vendor showed a declining line. Source 03 claims 99% of agencies buy links from vendors (his estimate). Sources: 05, 03. Cards: [2d1aea0b1ec7] [691b416017c3].

### A.4 Vendor and tool prices (from section 6)

Vendor trivia, already flagged `[web check]` in the original table; re-verify before quoting a price to a client.

| Item | Value | Condition | Source(s) | Confidence |
|---|---|---|---|---|
| Screaming Frog free tier | 500 URLs | crawl | 09, 13 | medium [web check] |
| Screaming Frog licence | about $500 a year | crawl | 13 | dated [web check] |
| Semrush starter plan | $199 a month (08); about $200 (06) | tools | 08, 06 | vendor [web check] |
| Ahrefs cheap tier | about $29 a month vs $129 | tools | 03 | dated [web check] |
| Featured.com free tier | about 3 answers a month | links | 03 | dated [web check] |
