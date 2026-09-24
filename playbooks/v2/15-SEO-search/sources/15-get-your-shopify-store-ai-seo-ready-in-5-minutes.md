# Get Your Shopify Store AI-SEO-Ready in 5 Minutes

source_id: 1gwkZ_tpNGT2btBydX0cvQFjwVGbcRUQM  |  folder: 15-SEO-search  |  cards: 6  |  words: 2,570  |  type: transcript (YouTube video, talking-head with screen references)

credibility: Presenter identifies himself only as "Jan," of "coding with jan.com." He states he "did a bit of research" last week and built a 3-stage framework from it; no client names, no before/after traffic or ranking data, no case study on his own store is given. Two example third-party apps (BrickFinder, a Tesla spare-parts finder) are shown as built by "members of my community," and the presenter explicitly discloses one of them pays an affiliate commission through his link. The whole framework ("Found, Matched, Chosen") is presented as the presenter's own mental model mapped from traditional SEO onto AI search, not a documented or externally validated ranking system. The video closes with a pitch for the presenter's own "AI developer bootcamp" — treat that as a sales pitch, not technical content, and it is excluded below per the source's own header instructions.

date signals: No explicit year stated in the transcript. References Shopify's "Sidekick" AI assistant, the Shopify "global product catalog," the "Agentyc storefront" requirement, ClaudeBot as a named crawler user-agent, and Gemini as an exception to the JS-rendering problem. All of these are current AI-platform and Shopify-feature names that move fast; every UI/feature reference below is tagged `[verify UI]` or `[web check]`.

## 1. What this source is for

Gives a fast, high-level 3-stage checklist (Found, Matched, Chosen) for making a Shopify store's products discoverable, matchable and recommendable by AI search tools and shopping agents (ChatGPT, Perplexity, and Shopify's own AI-fed catalog). It is a diagnostic mental model plus a handful of concrete spot-checks, not a full technical implementation guide.

## 2. Principles

1. **Map AI search readiness onto 3 traditional-SEO-like stages: Found, Matched, Chosen.** Found = can AI discover and read the store (technical SEO analogue). Matched = does product data match a user's query (content/data layout). Chosen = does the store win the single final recommendation (reputation/social proof, the analogue of backlinks). Evidence: presenter's own framing from "a bit of research," not a published or cited model. [2a7d0c66c403]
2. **Work the stages in order.** A product that isn't found can't be matched, and a product that isn't matched can't be chosen — fix crawlability and data before investing in reputation building. Evidence: presenter's stated logic, not separately tested. [2a7d0c66c403]
3. **Being discoverable requires no extra setup beyond not blocking it.** Pages just get crawled like regular web pages; there is no AI-specific sitemap or "AI Search Console" step named. The only way to break this is blocking agents via robots.txt, or password-protecting pages. Evidence: presenter's stated claim about how Shopify stores are crawled by default. [9ccea10d00bf]
4. **Shopify auto-generates robots.txt and normally does not block AI agents**, unless a merchant or an installed app has modified it. Evidence: presenter's stated claim about Shopify's default behavior. [9ccea10d00bf]
5. **Most crawlers only see HTML present at page load; content injected later by JavaScript (e.g., review or FAQ widgets that render after the page appears) is invisible to them.** Gemini is called out as the one named exception. Evidence: presenter's stated technical claim, not independently tested per crawler in the source. [f8f8462498cb]
6. **Schema markup (structured product data — name, price, etc.) is not new** — it was already a good-SEO requirement, which is why AI-SEO and technical SEO overlap here. Evidence: presenter's stated claim. [29f83e9997d]
7. **The open web (page crawling) and Shopify's global product catalog are two separate distribution channels**, and a store should be checked on both. The catalog is back-end data only (title, description, price, some meta fields) — the crawler-visible product page content does not feed it. Evidence: presenter's stated architecture claim. [c0a13e75f012]
8. **AI builds a shortlist (the presenter's examples: top 5, top 10, or up to top 100) out of millions of indexed products before making a final recommendation; you can control landing in the shortlist (Matched) but full control ends there.** Getting to the single final "Chosen" answer is explicitly called a stage the store "can't fully control," since it depends on session context and per-user AI judgment. Evidence: presenter's stated model, not measured. [2a7d0c66c403]
9. **Explicit, factual product copy beats vague marketing copy for AI keyword matching**, because AI relies on exact data points (size, color, use case) to build the shortlist, the same as traditional SEO keyword matching. Evidence: presenter's worked example contrast (see section 7). [43284bf0e6dd]
10. **Final AI recommendation weight leans on off-page reputation and social proof** (external reviews, e.g. on Reddit) — described as the AI-search analogue of backlink authority in traditional SEO. Evidence: presenter's stated analogy, not a cited study. [2a7d0c66c403]
11. **Big brands still get recommended by default for broad queries** because they already have more trust and reputation, exactly as they already dominate broad traditional-SEO keywords; smaller stores should target longer, more specific queries and build reputation over time rather than compete on broad terms. Evidence: presenter's stated analogy to traditional SEO keyword competition (his own example: "shoes" vs. "vegan waterproof trail running shoes"). [2a7d0c66c403]

## 3. Procedures

### A. Check discoverability (robots.txt and crawler access)
1. Go to `yourdomain.com/robots.txt` in a browser to view the file. `[verify UI]`
2. Confirm Shopify's auto-generated file is not blocking common AI agents; check it has not been modified (manually or by an installed app).
3. Test directly by running a crawler-style fetch from the command line: `curl -A ClaudeBot yourwebsite.com` (the `-A` flag sets the user-agent string to impersonate the named bot) and read whether the site returns accessible content.
4. Alternatively, ask Claude or ChatGPT directly whether it can access the website (source does not specify exact prompt wording).
5. Make sure no page that should be publicly found is password-protected.
[card 9ccea10d00bf]

### B. Check readability (JavaScript-dependent content)
1. In your browser, disable JavaScript, then reload the target page (product page, or any page with review/FAQ widgets).
2. Compare what renders with JS off against the normal page. Anything missing (reviews, FAQs, specs) that is normally shown only after client-side JS runs is likely invisible to most AI crawlers — Gemini is the named exception.
3. Treat leftover placeholder/snippet stubs where content should be as the signal of a problem, not proof by itself that every engine misses it.
4. Fix by ensuring relevant information (reviews, FAQs, key specs) is rendered directly in the page, not injected later by a lazy-loaded app widget.
[card f8f8462498cb]

### C. Check and add schema markup
1. Confirm the page carries structured data (schema) describing the product: name, price, and other structured fields, rendered in the page markup.
2. Use a free schema validator app/tool (source does not name a specific one — "you can just Google for free validator apps, schema validators") to check what is working and what isn't. `[web check: which validator]`
[card 29f83e9997d]

### D. Check Shopify global product catalog eligibility
1. Confirm the "Agentyc storefront" requirement is enabled on the Shopify store — this is described as the eligibility gate for inclusion in the global product catalog, which independent AI shopping tools and chatbots can read. `[verify UI: exact setting name/location]`
2. To verify eligibility, ask Shopify's Sidekick AI assistant directly whether the store's products are eligible/showing in the global catalog. `[verify UI]`
3. Cross-check against Shopify's official published requirements (source paraphrases them, does not quote a canonical source): product must have a title, at least one image, and a non-zero price; store must comply with Shopify's terms of service. `[web check: current official requirements]`
4. Because the catalog is compiled purely from back-end data (title, description, price, meta fields — not full page content), review and clean these fields specifically. Watch for stray metafields left behind by uninstalled apps (source's example: outdated review apps leaving orphaned metafields) and remove/correct them.
[card c0a13e75f012]

### E. Rewrite product data for keyword matching ("Matched" stage)
1. Identify the explicit facts a shopper would search for: container/product size, exact color, exact use case, material, etc.
2. Replace vague marketing phrasing with these explicit facts in the product title, description, variant fields and metafields.
3. Keep titles, descriptions, variant fields and metafields internally consistent with each other.
4. Map a specific example shopper query to the product's on-page attributes and confirm each implied match is actually supported by real product data (not a marketing claim without a fact behind it).
[cards 43284bf0e6dd][29f83e9997d]

### F. Build reputation ("Chosen" stage)
1. Recognize this stage cannot be fully engineered — the source gives no step-by-step tactic beyond "get outside reputation."
2. Pursue reviews and good user stories/experiences across different platforms (Reddit named as one of the most important sources for this).
3. Aim for consistency of positive signal across platforms, since consistency is described as what makes the reputation signal trustworthy.
4. For a smaller/newer store, target longer, more specific ("niche") queries rather than competing on broad terms dominated by larger, already-trusted brands, and build reputation over time.
[card 2a7d0c66c403] — source gives no further procedural detail here; treat as thin on how.

## 4. Rules, thresholds and numbers

| Rule | Number / threshold | Condition | Source's basis | Card id |
|---|---|---|---|---|
| AI shortlist size (candidate pool before final pick) | top 5, top 10, or up to top 100 | Out of "millions" of indexed products, before AI narrows to one final recommendation | Presenter's stated model, not measured | 2a7d0c66c403 |
| Global catalog eligibility: title | must have a title | Product-level requirement for Shopify global product catalog | Presenter's paraphrase of Shopify's official requirements `[web check]` | c0a13e75f012 |
| Global catalog eligibility: image | at least one image | Product-level requirement for Shopify global product catalog | Presenter's paraphrase `[web check]` | c0a13e75f012 |
| Global catalog eligibility: price | price cannot be zero | Product-level requirement for Shopify global product catalog | Presenter's paraphrase `[web check]` | c0a13e75f012 |
| Global catalog eligibility: ToS | must comply with Shopify terms of service | Store-level requirement | Presenter's paraphrase `[web check]` | c0a13e75f012 |
| Crawler test command | `curl -A ClaudeBot yourwebsite.com` | Command-line check of whether an AI agent can access the site | Presenter's demonstrated command | 9ccea10d00bf |

No numeric SEO score, traffic figure, ranking position, or before/after result is given anywhere in this source — it is entirely a qualitative checklist with two named worked examples (see section 7) and no measured outcome for the presenter's own store or any client.

## 5. Diagnostics and checks

- **Robots.txt check**: visit `/robots.txt` on the domain; confirm no rule disallows major AI agents; re-check after installing any app, since apps can silently modify the auto-generated file. `[verify UI]` [9ccea10d00bf]
- **Crawler-access check**: run `curl -A ClaudeBot yourwebsite.com` (or ask an AI assistant directly) and read whether the response shows real content or a block. A spoofed user-agent fetch does not by itself prove a real crawler can access the site or that the page is indexed — treat it as a diagnostic signal, not final proof. [9ccea10d00bf]
- **JavaScript-off check**: disable JS in the browser, reload the page, and look for missing reviews/FAQs/specs or leftover placeholder stubs where content should be. Retest after any theme or app change, since rendering behavior can change. Gemini is named as the one exception that can still read JS-rendered content; other engines' current behavior should be verified rather than assumed constant. [f8f8462498cb]
- **Schema validator check**: run a free schema/structured-data validator against the product page; it reports what is and is not correctly structured. `[web check: which validator to use]` [29f83e9997d]
- **Global catalog eligibility check**: ask Shopify Sidekick whether the store is eligible/included; separately compare official Shopify catalog requirements against actual product data (title, image, price, ToS compliance). `[verify UI]` [c0a13e75f012]
- **Metafield audit**: review all product metafields for staleness, specifically checking for leftover fields from uninstalled apps (source's example: an old review app's metafields lingering after removal). [c0a13e75f012]
- **Query-to-attribute check**: take a specific realistic shopper query and confirm the product page's title/description/variants/metafields actually contain the matching facts the query would need (not just adjacent marketing language). [43284bf0e6dd]

## 6. Tools, settings and named features

| Tool / feature | Used for | Notes |
|---|---|---|
| Shopify auto-generated robots.txt | Controls whether AI agents/crawlers can access the store | Generated automatically unless manually modified; apps can also modify it. `[verify UI]` |
| `curl -A ClaudeBot <url>` | Command-line simulation of a named AI crawler fetching the site | Demonstrated command; ClaudeBot is the specific user-agent named. Other bots not tested in source. |
| Shopify Sidekick | Shopify's AI admin assistant | Used here specifically to ask whether a store is eligible for/showing in the global product catalog. `[verify UI]` |
| Shopify global product catalog | Back-end feed of all Shopify products, consumed by independent AI shopping tools/chatbots | Requires "Agentyc storefront" enabled to be eligible. `[verify UI: exact setting]` |
| "Agentyc storefront" | The named Shopify requirement/setting that gates inclusion in the global product catalog | Exact current name/location not given precisely enough to reproduce without checking Shopify's own docs/admin. `[verify UI]` |
| Free schema validator apps | Validate structured product data (schema markup) | Not a specific tool named — presenter says "Google for free validator apps." `[web check: which one]` |
| BrickFinder (third-party site) | Community-built example: finds specific LEGO bricks/packs across all Shopify stores via the global catalog | Presenter's community example, not evaluated for quality/traffic. |
| Tesla spare-parts finder (unnamed third-party site) | Community-built example: finds Tesla spare parts across Shopify stores via the global catalog | **Presenter explicitly discloses this one carries an affiliate commission through his link** — flag as promotional, not a neutral example. `[web check]` |
| ClaudeBot, ChatGPT, Perplexity, Gemini | Named AI agents/engines referenced as the crawlers/search surfaces being optimized for | Gemini specifically named as able to read JS-rendered content where others reportedly cannot; verify current per-engine crawling/rendering behavior before relying on this. `[web check]` |

## 7. Examples and case results

- Worked example (product copy rewrite, illustrative only, no store or outcome named): bad copy — "our best-selling water bottle, perfect for life on the go, in gorgeous colors" (vague, no color, size, or use case named). Better copy — explicit facts naming "insulated water bottle, green, cold drinks" so AI can match a query like "insulated water bottle, cold drinks, green" against real data points. No before/after ranking or recommendation outcome is given; this illustrates the method only. [43284bf0e6dd]
- Example: BrickFinder, a community-built tool using the Shopify global product catalog to find specific LEGO bricks/sets across every Shopify store. Presented as a working example of an app built on top of the catalog, not a measured business result. [c0a13e75f012]
- Example: an unnamed Tesla spare-parts finder site, also built on the global catalog, which the presenter discloses pays him an affiliate commission when visited through his link — treat this specific example as partly promotional. [c0a13e75f012]
- Traditional-SEO analogy example: a store cannot realistically rank for a broad keyword like "shoes" against dominant top brands, but can rank for a specific long-tail query like "vegan waterproof trail running shoes" with a specific size; the source applies this same logic to AI search recommendation odds for smaller vs. larger brands. Illustrative analogy, not tested on an actual AI search result. [2a7d0c66c403]

## 8. Mistakes the source warns about

- Blocking AI agents in robots.txt, whether done manually or introduced by an installed app, which breaks the "Found" stage entirely. [9ccea10d00bf]
- Leaving pages password-protected when they are meant to be publicly discoverable. [9ccea10d00bf]
- Relying on app-based review widgets, FAQ widgets or other content that only renders after page load via JavaScript, leaving critical content (reviews, FAQs, specs) invisible to most AI crawlers. [f8f8462498cb]
- Writing vague, "fluffy" marketing copy (the source's own example: "perfect for life on the go, in gorgeous colors") instead of explicit, matchable facts — this keeps a product out of the AI's shortlist even if it is otherwise a good product. [43284bf0e6dd]
- Leaving stale or orphaned metafields in place after uninstalling an app (source's example: leftover fields from an old review app), which pollutes the back-end data the global catalog is compiled from. [c0a13e75f012]
- Assuming the catalog reflects the same content a human visitor or open-web crawler sees — the source stresses the catalog is compiled purely from back-end fields (title, description, price, some meta fields), so front-end page fixes alone will not fix catalog data problems. [c0a13e75f012]

## 9. Caveats, conflicts and what is missing

- The entire "Found, Matched, Chosen" framework is explicitly the presenter's own simplification from a small, self-described research effort ("last week, I did a bit of research"). It has not been published, peer-reviewed, or validated as an actual AI ranking model — treat stage names and stage boundaries as a mental model/checklist, not a verified mechanism. [2a7d0c66c403]
- The "Chosen" (reputation) stage is explicitly called out by the presenter as something a store "can't fully control," and the source gives no concrete step-by-step tactic for building it beyond "get reviews and good experiences on different platforms" — this stage is thin on how compared to Found and Matched. [2a7d0c66c403]
- The Tesla spare-parts finder example carries an undisclosed-elsewhere but presenter-disclosed affiliate relationship; treat any traffic/success framing around it as partly promotional, not neutral evidence that the global catalog reliably drives business results. [c0a13e75f012]
- No numeric outcome (ranking position, AI-recommendation rate, traffic, or sales) is given anywhere for any of the source's own recommendations — every claim in this source is asserted from the presenter's reasoning or a single small demonstration, not measured.
- "Agentyc storefront" and the exact global-product-catalog admin path are named but not walked through step by step in the transcript (no menu path given) — this is a gap the source itself does not fill; verify the actual current Shopify setting name and location before acting. `[verify UI]`
- The claim that "Gemini is the only exception" to the JS-rendering-invisibility problem is a single, unqualified assertion with no test shown — verify current per-engine JS-rendering behavior before treating this as fixed. `[web check]`
- No conflict with other 15-SEO-search sources was identifiable from this document alone; this source's scope (AI/generative search readiness) is complementary to, not overlapping with, the traditional-Google-SEO sources already in this folder (keyword planning, on-page fields, page speed, sitemaps) — flag any conflict found later during the pass-2 merge, particularly around whether "technical SEO" steps (schema, page speed, crawlability) should be treated as one shared checklist across traditional and AI search or kept separate.
- The source explicitly excludes, and this playbook likewise excludes, the presenter's monetization pitch (technical/content/reputation "audits" as a paid service, and the "AI developer bootcamp") per the source header's own "skip" instruction.

## 10. Card index

- [2a7d0c66c403] Adapt the Found–Matched–Chosen framework to AI search
- [9ccea10d00bf] Check whether AI crawlers can actually access your store
- [f8f8462498cb] See your product page the way a JS-blind crawler sees it
- [43284bf0e6dd] Publish factual product attributes for specific shopper queries
- [c0a13e75f012] Audit Shopify catalog readiness alongside storefront SEO
- [29f83e9997d] Validate product structured data against visible store facts
