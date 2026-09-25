# Learn Everything About SEO & AI SEO in 50 Minutes!

source_id: 1dhIYF8yjdF6mOtPhDA64zWfXQS2bQ2vg  |  folder: /15-SEO-search  |  cards: 18  |  words: 8,552  |  type: transcript (YouTube course, single presenter)
credibility: Unnamed presenter who says he has "run dozens and dozens of SEO campaigns for clients." No client names, no case-study numbers beyond the worked examples below (which are framed as real client sites: Panda, Counterculture, Huntress — plus one openly fictional company, Stockpath). No controlled tests or before/after data. Evidence is anecdote, screenshots of real SERPs and one Ahrefs stat he cites secondhand. The video promotes Surfer (an SEO/content-optimization tool) throughout and ends with an explicit plug and affiliate-style link ("if you want to try Surfer, the link is in the description"). Treat every Surfer-attributed capability and every "pages that clear this threshold rank better" claim as a vendor claim carried by the presenter, not independent evidence. Screaming Frog and Source of Sources are recommended as free tools with no visible commercial tie to the presenter.
date signals: No explicit year stated. References ChatGPT, Gemini, Perplexity, Copilot, Claude, Grok and "Google AI mode" as live products, AI overviews on Google SERPs including commercial/transactional queries, Andromeda-era AI content volume implicitly, and "Claude Code and Codex" as vibe-coding tools — consistent with 2025-2026. Cites Google processing "over 5 trillion searches a year" and "190x more traffic than ChatGPT," both `[web check: current figures]`. All named tool capabilities (Surfer features, Screaming Frog free tier, Google SERP layout) can change; tagged `[verify UI]` throughout.

## 1. What this source is for

It is a single, opinionated walkthrough of SEO end to end — intent, keyword research, prioritization, content creation, on-page technical work, link building, basic technical SEO, and AI-search (GEO) visibility — built around three running example businesses: Panda (B2B SaaS, proposal software), Counterculture (specialty coffee ecommerce), and Huntress (managed cybersecurity). Its central argument is that AI search is not a separate discipline: ranking in Google/Bing is the prerequisite for showing up in AI answers, so the same fundamentals (intent match, topical authority, structured content, citations) serve both channels. It ends in a concrete 30-day action plan. It is strong on sequencing (what to build first, in what order) and weak on hard settings (no bid/budget/spend numbers apply here since this is organic, but also no keyword-difficulty score thresholds, no explicit crawl-budget or index-coverage numbers, and heavy reliance on a named paid tool for the "how").

## 2. Principles

### 2.1 SEO means showing up wherever people search, not just Google rankings
The presenter reframes SEO from "search engine optimization" to "search everywhere optimization" (credited to Ashley Liddell). Google search itself works in three steps: crawl (bots read pages by following links), index (Google stores what is found; if a page is not indexed it cannot appear in results), and rank (Google orders indexed pages by relevance, trust and usefulness for a given query). The modern SERP includes, in order seen: an AI overview at top, sponsored ads, organic results, People Also Ask boxes, video carousels, a local map pack (for location-based searches), and knowledge panels — "we've come a long way from 10 blue links." [7c2ebc1068d0]

### 2.2 Search intent is the single most important SEO concept
Every query has one of four intents: informational (wants to learn — e.g. "how to train your puppy"), commercial (comparing options, willing to spend but undecided — e.g. "best dog training classes"), transactional (ready to buy, knows the category — e.g. "dog training class near me sign up"), navigational/branded (using Google to reach a known brand — e.g. "petsmart dog training"). Your job is to match the page type to the intent Google has already inferred, not to fight it. [f32610667b5f]

### 2.3 The 30-second intent test: let the SERP tell you the intent
Google the exact target keyword and read the top 10 organic results. If they are comparison blogs and buying guides, intent is commercial. If they are product/pricing pages, intent is transactional. Also read the SERP features present (AI overview, PAA, video carousel, map pack, knowledge panel) — if videos dominate, you need a video to compete. Even commercial and transactional queries increasingly trigger AI overviews now, so Google may answer the comparison question before any click ("zero-click marketing"); your content must go deeper than the summary to earn the click. Condition: SERPs vary by location, personalization and time, so re-check intent when refreshing a page. [f32610667b5f] [245141abe8fc]

### 2.4 Shorter keywords are usually higher volume, more competitive and less useful
Rule of thumb, no fixed cutoff given: as keyword length drops, competition and ambiguity rise. Source's example: "coffee" gets roughly 650,000 US searches/month but the SERP is a mess (shops, definitions, news, every major site competing) — Google itself doesn't know what you want. "Best dark roast coffee beans for espresso" gets a few hundred searches/month but the SERP is uniformly comparison/buying-guide content — intent is crystal clear and competition is a fraction of the head term. Longtail keywords (longer, more specific phrases) have lower individual volume but focused intent, manageable competition, and in aggregate can carry a respectable amount of traffic. Newer sites should start on longtail terms and work up to head terms as authority grows. [f32610667b5f]

### 2.5 The Keyword Sweet Spot framework: score every candidate on 4 attributes
1) **Demand** — are people actually searching this? Thought-leadership topics can be worth publishing for credibility but won't drive meaningful organic traffic if nobody googles them. 2) **Fit** — where does it sit in the funnel, and is it relevant to your products/audience? 3) **Intent** — can your page format actually satisfy the searcher's want (a YouTube-video SERP needs a video; a calculator-SERP needs a calculator)? 4) **Difficulty** — can you realistically rank given your site's current authority (a brand-new site won't outrank Amazon for "running shoes" but might compete for a narrow longtail variant). Keywords scoring well on all four are rare "unicorns" — prioritize them when found, but most usable keywords score well on only some attributes and need a deliberate plan (see 2.6 for the top-funnel example). [03569978ba18]

### 2.6 A top-funnel keyword is fine if you have a conversion path behind it
Worked example (Panda, SaaS): "contract template" gets ~300,000 searches/month; almost nobody searching it is buying proposal software that day. Conventional wisdom says skip it, but Panda ranks highly for it and its template directory drives "hundreds of thousands of visits" monthly by running: free template download → email capture → nurture sequence → product signup. The keyword itself is not bad, it's a top-funnel keyword with a pipeline behind it. A keyword without a conversion path is vanity traffic; the same keyword with a path can be an automated acquisition channel. [03569978ba18] [28f51e6a77cb]

### 2.7 Different keyword-to-funnel-stage mapping needs different page types (ecommerce worked example)
Worked example (Counterculture, coffee ecommerce): "pour over coffee" (~34,000 searches/month) does not get targeted with a conversion page — the searcher likely wants a location or an explanation, not a purchase. Counterculture instead ranks it with an educational brew guide on their blog, and also ranks "pour over coffee ratio" (~10,000/month), "cold brew ratio" (~6,800/month) and "coffee brewing methods" (~5,200/month) with more educational content, building specialty-coffee authority and trust, with product sales following. [03569978ba18]

### 2.8 Money pages first: build what converts before you build what teaches — ecommerce-specific priority order
Money pages are the pages that directly convert: product pages, category pages, pricing pages, feature pages, subscription pages. Their keywords are typically transactional or commercial (source's examples: "buy espresso beans online," "coffee subscription," "cyber security assessment services," "proposal software for agencies"). Common failure pattern named: writing 10 informational articles first because they show volume or low competition, then finding nobody buys — because there is nowhere compelling for the traffic to convert. The presenter is explicit: you should not have an "SEO goal," you should have a business goal (more customers, revenue, leads); SEO is one route there. `[Ecommerce-specific: this money-pages-first order is stated as the correct order for any business, but is illustrated with product/category/subscription pages, which map directly onto a store's catalog structure.]` [28f51e6a77cb]

### 2.9 Build one topical cluster at a time, connected to a money page
Once money pages exist, pick one cluster that connects to a money page and build the full funnel for it, rather than scattering content across many topics. Structure, bottom to top: the money page itself (transactional — e.g. Counterculture's subscription page, which already ranked "coffee subscription" at 15,000 searches/month); one step up, commercial-intent comparison content (e.g. "best coffee subscription," "coffee subscription box comparison") that links back to the money page; at the top, educational content (Counterculture's "coffee basics" series: brewing ratios, brewing methods, grind size, tasting notes, single-origin coffee) that feeds everything below it and internally links sideways to related posts. This web of content is the "topic cluster." [28f51e6a77cb] [618a252af117]

### 2.10 Finish one cluster before starting the next
The presenter names his own earlier mistake: sorting one big keyword list by lowest competition and highest volume, then working straight down it. Worked counter-example (Panda): two blog posts on contract management, then a comparison page on e-signature tools, then jumping to an unrelated guide on sales forecasting — this spreads authority thin across unrelated clusters and prolongs time to results. Repeat cluster by cluster instead. [28f51e6a77cb] [618a252af117]

### 2.11 Topical authority: Google evaluates your whole site's coverage of a subject, not just one page
Mechanism as stated: when someone searches "how to prevent ransomware attacks," Google checks whether the site also covers "what is ransomware," "signs your network has been compromised," and "ransomware incident response checklist" — the same searcher at different stages of one problem. Full-journey coverage increases Google's trust in the whole subject, which makes every keyword in that cluster easier to rank, including the more competitive ones. Recommended cluster size: roughly 5-10 interconnected articles on one narrow topic (example: coffee brewing ratios) before moving to an entirely different subject (example: sales forecasting). Ecommerce application given directly in the card, not verbatim in the transcript: treat a category's buying journey as the cluster — definition/education content, comparison and buying guides, then the category or product page they all link to. This is a compounding strategy; the presenter says explicitly you probably won't see results in 30 days. [618a252af117]

### 2.12 Two-channel visibility: traditional SEO is the prerequisite for AI search visibility, not a competitor to it
Mechanism: ChatGPT uses Bing's index when it searches the web; Perplexity runs its own crawler but leans heavily on Bing's index underneath; even assistants building their own index are crawling pages that already rank in traditional search. If a site does not appear in Google or Bing, it is likely invisible to AI assistants too. The same signals help both channels: authoritative content, clear structure, schema markup, and third-party citations. Framing numbers given to argue against dropping SEO for a GEO-only program: Google sends roughly 190x more traffic to websites than ChatGPT, and Google search volume grew about 20% year over year. `[web check: current traffic-share and search-volume figures — these are the presenter's argument for 2025/2026, not a standing fact]` [7c2ebc1068d0]

### 2.13 AI assistants are a discovery channel now; check whether your brand shows up in them
People ask AI assistants for product/brand recommendations conversationally ("what's the best CRM for small businesses," "recommend a project management tool"), and the assistants answer with specific brand names. If your business is not showing up, you're invisible in this channel. Manual check: open a fresh incognito browser, ask an AI assistant a buying-journey question your target customer would plausibly ask, and note which brands are recommended — that is your AI competition. Use incognito specifically because assistants like ChatGPT can be "sneaky about recognizing your preferences" and skew answers toward what it thinks you want. Worked examples given as screenshots: "what's the best proposal software for agencies?" surfaced Panda; "best specialty coffee beans" surfaced Counterculture; "what companies can help me protect my network from ransomware?" surfaced Huntress. AI assistants synthesize information across the web into a conversational answer and cite sources based on authority, relevance, and how clearly the content answers the question. [7c2ebc1068d0] [46a784e2d55c]

### 2.14 AI search optimization is not a separate discipline from SEO
Restated as the source's closing thesis: everything that improves AI-search visibility — comprehensive structured content with clear subheadings and direct answers, topical-authority clusters, and third-party citations — is the same work that improves traditional rankings. "It's what happens when you do the fundamentals well and pay attention to where the channels are heading." [46a784e2d55c]

### 2.15 AI overviews now cover commercial and transactional queries, creating a zero-click risk
AI overviews used to skew informational; now Google's AI summarizes results across all query types, including product comparisons and ready-to-buy searches. Consumers can make entire buying decisions without clicking through to any site ("zero-click marketing"). Response: audit your target page against the live AI overview for its query — if your page only restates what the summary already covers, there is no reason to click. Add what the summary cannot: original data, hands-on experience, specific products/prices/dimensions, opinionated recommendations, and answers to the follow-up questions a buyer will have after reading the summary. Re-check periodically since which queries trigger an overview, and what the overview says, both change. [245141abe8fc]

## 3. Procedures

### 3.1 Run the 30-second intent test (before committing content budget to any keyword)
1. Search the exact target keyword in Google. `[verify UI: current SERP layout]`
2. Read the top 10 organic results and classify the dominant format: informational, commercial, transactional, or navigational/branded.
3. Note SERP features present: AI overview, sponsored ads, People Also Ask, video carousel, local map pack, knowledge panel.
4. Match your planned page type to the dominant format rather than fighting it (do not build a straight product page against an all-educational SERP, or vice versa).
5. If videos dominate the SERP, plan to produce a video, not just text. [f32610667b5f]

### 3.2 Keyword ideation (mine free sources before reaching for tools)
1. If Google Search Console is already set up, start there — it shows exactly what people searched to find your site, from Google's own data; it is the most accurate source available. `[verify UI]`
2. Type your topic into Google and record autocomplete suggestions.
3. Click through People Also Ask boxes — each click reveals more; mine a dozen ideas in minutes.
4. Scroll to the bottom of a results page and read the "People also search for" section.
5. Find subreddits where your customers discuss the topic; note their exact problem-phrasing, which often matches Google query phrasing.
6. Paste your sitemap into ChatGPT (or similar) and ask it to identify content gaps versus what a site like yours should cover. `[verify UI]`
7. Paste a competitor's sitemap in and ask what they cover that you don't. `[verify UI]`
8. Ask an AI assistant for "30 questions someone would ask before buying your product category" for a fast seed list.
9. Optional tool: Surfer's free "Keyword Surfer" Chrome extension shows search volume, CPC and related ideas inside Google search results directly. `[verify UI]` [note: Surfer is the source's sponsor — treat this step as a vendor recommendation, not a neutral one] [0648fb2c0ce2]

### 3.3 Keyword validation and clustering
1. For each idea generated in 3.2, assess search volume, difficulty, business fit, and intent (run 3.1 for intent).
2. Choose a validation route: DIY — connect an SEO data API to an AI coding tool to pull volume, difficulty and intent programmatically (cheapest if comfortable with technical setup, no specific API named); or managed — a tool such as Surfer returns volume, difficulty and intent from a pasted keyword list with no API setup. `[verify UI]`
3. Cluster validated keywords that are topically related or that Google treats as the same meaning.
4. Optional: some tools (Surfer named) automate clustering for an entire site from one seed topic. `[verify UI]`
5. Do not assume your funnel-stage ratio (how many top- vs bottom-funnel keywords) matches another business — the source's three examples (SaaS, coffee ecommerce, cybersecurity) all have different intent ratios. [fb8f4b373003]

### 3.4 Three-step prioritization plan
1. **Money pages first.** List every page that directly converts (product, category, pricing, feature, subscription pages) and build or optimize these before any top-funnel content. `[Ecommerce-specific: for a store this is your product and category pages.]`
2. **Pick one topical cluster connected to a money page and build it fully**: the money page (transactional) at the bottom, commercial comparison content linking back to it in the middle, educational content feeding everything below at the top. Internally link every piece down the funnel and sideways to related posts.
3. **Repeat cluster by cluster.** Finish one cluster (roughly 5-10 interconnected articles) before starting an unrelated one. [28f51e6a77cb] [618a252af117]

### 3.5 Content creation blueprint: research, structure, write, optimize
1. **Research.** Open the top 5 ranking pages for your target keyword and read all of them in full. Record: (a) topics every one of them covers — table stakes you must also cover; (b) what they missed — your gap/opportunity; (c) their average length as a comprehensiveness benchmark, not an exact word-count target; (d) any unique angle taken — room to differentiate. Do this manually for your first few pieces to understand what you're later automating. Optional tool: Surfer's content editor automates this analysis (topics, term frequency, needed depth) in about 60 seconds versus roughly 20 minutes manual. `[verify UI]` [5ff1064a03ea]
2. **Structure.** Build a full outline before writing — do not skip this step. Either feed your research notes into an AI assistant (Claude or ChatGPT named) and ask for a draft outline, or generate a one-click search-optimized outline from a tool such as Surfer. `[verify UI]` [5ff1064a03ea]
3. **Write.** Let AI handle scaffolding, basic definitions, research synthesis and sentence flow. Then manually add what AI cannot supply (see 3.6, the human content moat) before publishing. [5ff1064a03ea] [b7c89ca36202]
4. **Optimize.** Use a real-time content score (0-100, Surfer-specific in this source) that tracks topical coverage, term usage and depth for the target keyword, covering both traditional-search and AI-search topical coverage. Aim to beat the highest score already on the tool's dashboard for that keyword. `[verify UI]` [5ff1064a03ea]

### 3.6 Build the human content moat into every AI-assisted draft
1. Add your own experience: what actually happened when you tried the thing.
2. Add opinion deliberately: what you think is overrated, underrated, or plain wrong in your product category.
3. Add original data: your own experiment results, case studies, sales/usage numbers, or notes from customer conversations.
4. Add expert insight — this does not need to come from your own team; source quotes from podcasts, YouTube videos, books, or scholarly journals if your business lacks in-house expertise.
5. Add specific examples: real businesses, real numbers, real outcomes.
6. Find the moat that fits your business — worked examples: Panda (SaaS) uses customer stories, workflow screenshots and free downloadable assets; Counterculture (coffee ecommerce) uses roasting expertise and video content. `[needs brand data: what proprietary expertise, data or stories the brand can draw on]` [b7c89ca36202]

### 3.7 On-page checklist for any page (execute differently for money pages vs. content pages)
1. **Title tag**: include the target keyword, stay under 60 characters, make it clickworthy. Front-load the keyword on educational pages (example: "Ransomware Recovery Guide for Businesses"); make it benefit-driven on money pages (example: "Endpoint Detection and Response Built for Every Business"). `[verify UI: current SERP title truncation point]`
2. **Headers**: exactly one H1 per page, ideally mirroring the title tag. H2s for main sections, H3s for subsections, keywords used naturally throughout. Both Google and LLMs read this hierarchy to understand structure and depth; it also helps human readers skim.
3. **URL**: short, descriptive, keyword-bearing, categorized where sensible (examples: `/cybersecurity-101/ransomware-recovery-guide`, `/platform/managed-edr`). Avoid CMS-generated strings of random letters/numbers.
4. **Meta description**: 150-160 characters. Not a direct ranking factor, but affects click-through. Write it like ad copy: include the keyword, state clearly what the searcher will get.
5. **Internal linking**: add contextual links inside the body copy (not just nav/footer) to related content and to money pages. Worked example (Huntress ransomware guide) links to: a ransomware handbook, a blog post about a specific ransomware family (transcribed in the source as "Kawa Locker ransomware" — likely a mis-transcription of the actual ransomware name; verify before reuse `[web check: correct ransomware family name]`), a cybersecurity compliance solutions page, the managed EDR product page, and a security awareness training page. Optional tool: Surfer's "auto internal links" feature scans the site and inserts links automatically — treat as an assist, not a reason to skip manual review. `[verify UI]`
6. **Images**: descriptive file names, alt text that describes the image to someone who can't see it (screen-reader users depend on it), compressed file size, WebP format preferred. `[verify UI: current best-practice image formats]` [ce6536d71069] [91cc4c076fd9]

### 3.8 Link building sequence
1. If you're new, don't start with outreach. First publish 10-15 great pieces of content.
2. Start with journalist-query platforms: sign up for **Source of Sources** (free, created by the original founder of HARO — Help a Reporter Out) or **Featured.com**. `[web check: current platform names/availability, since HARO itself has changed ownership/branding before]` Budget about 15 minutes a day monitoring and responding to queries with genuine quotes and insight; expect roughly 1 hit per 100 submissions and keep at it.
3. In parallel or after, be the source: identify original data, analysis or resources you can publish that journalists and bloggers will want to cite. Worked examples: Counterculture's pour-over brew guide, cited by WikiHow, Gear Patrol, Breville and dozens of coffee blogs because it is the most thorough guide on the topic; Huntress's ransomware/data-breach posts, cited by a cloud provider's threat-intelligence team and referenced on Wikipedia.
4. Consider building a linkable asset: identify a simple, interactive gap in your category (worked example: Counterculture already ranks #1 for "pour over coffee ratio" and "cold brew ratio" with blog guides; "coffee to water ratio calculator" gets about 500 searches/month at a keyword difficulty of 8 — a simple calculator could capture that traffic and earn links from every coffee blog that references their ratio guides). Build with an AI coding tool if you lack technical skills — the presenter vibe-coded a fictional inventory calculator ("Stockpath") in about 10 minutes using Claude Code with "nearly zero coding experience." [88997600260b] [b7d9a9c621b3]

### 3.9 Technical SEO triage
1. If running on Shopify, WordPress, Webflow or a similar CMS, assume you're already roughly 90% of the way there — genuinely messy technical SEO is mainly an enterprise-site problem.
2. Download Screaming Frog SEO Spider (free for up to 500 URLs), point it at your site, and let it crawl every page. `[verify UI/web check: current free-tier URL limit]`
3. Work down its prioritized issue list: broken links, missing title tags, duplicate content, redirect chains, images without alt text.
4. If the business has a physical location (store, office, restaurant), separately claim and fully complete the Google Business Profile, and gather and respond to reviews — this alone can help placement in the local map pack for "[category] near me" searches. `[Ecommerce-specific: only applies to stores with a physical location, not pure online retailers.]` [e9e95368a588]
5. As a beginner, do not go down a technical rabbit hole — the presenter's view is that most beginners are held back by not having published content yet, not by technical issues. [e9e95368a588]

### 3.10 AI-search (GEO) visibility procedure
1. Apply the content creation blueprint (3.5) and human content moat (3.6) — this is the same work, and LLMs pull from content they can parse easily (comprehensive, clearly subheaded, with direct answers to specific questions).
2. Build topical authority through clusters (3.4 step 2) covering a subject from every angle — definition, how-to, comparison, deep dive — so AI models are more likely to recognize the brand as an authority.
3. Earn citations from other authoritative sites (3.8) — AI models weight sources that other trusted sites reference; every backlink from a reputable site signals citability to AI systems too.
4. Specifically target "best of" roundup articles — the source says AI assistants especially favor them — either by getting placed in existing roundups or by writing your own.
5. Find citation gaps: optional tool, Surfer's "mention gap report," shows which queries competitors get cited in that you don't. Sort by highest mentions, filter for gaps, and use the list as a prioritized outreach target combined with the journalist-query tactic (3.8 step 2). `[verify UI]`
6. Monitor AI visibility regularly using the manual check in 2.13, or a tracking tool (Surfer's AI tracker named — runs queries across ChatGPT, Gemini and Perplexity, tracks which brands get recommended over time and where competitors show up and you don't). `[verify UI]` Note this tool reports visibility only, not traffic or conversions, since no one has access to what people type into AI assistants and Search Console cannot see AI-assistant referrals. [46a784e2d55c]

### 3.11 30-day SEO action plan
**Week 1 — Foundation.** Set up Google Search Console (free, essential) `[verify UI]`. Choose your keyword-research tooling and find 10-15 target keywords using the Keyword Sweet Spot framework (3.3). Run the 30-second intent test (3.1) on your top 5 keywords. Identify your money pages and note whether they exist yet.
**Week 2 — Most important money page.** Write and publish your single most important money page, or optimize the existing one, following the content creation blueprint (3.5) and the on-page checklist (3.7): title, meta, headers, internal links, images. Note: building additional money pages is an ongoing priority after this, not a one-week sprint.
**Week 3 — First funnel.** Pick one topical cluster connected to that money page. Publish a mid-funnel or top-funnel piece supporting it, and internally link it to the money page and other related pages. If content already exists and ranks on page 2 or 3, updating it can be faster than writing new content from scratch.
**Week 4 — Promote and monitor.** Spend about 15 minutes a day responding to journalist queries (Source of Sources or Featured.com). Check AI visibility manually (2.13) or with a tracker. Review Google Search Console for early signals (3.12). Then plan the next cluster — not the next random topic. [63c02d6a7770]

### 3.12 Reading early SEO signals in Search Console (before rankings/clicks mature)
1. Check for rising impressions even if clicks have not yet followed — treat this as progress, not failure; it means the page is being considered for relevant queries.
2. Check for new keywords appearing that you did not explicitly target — use these as raw material for the next cluster or for on-page refinement.
3. Check for position movement trending upward, e.g. from page 5 toward page 3.
4. When you see a page already on page 2 or 3, prioritize updating it over publishing something new — often faster to a result.
5. For AI channels, supplement Search Console with the manual or tool-based visibility check (2.13/3.10), since Search Console cannot register ChatGPT or Perplexity traffic. [9bb24c359ea8]

## 4. Rules, thresholds and numbers

| rule | number or threshold | condition | source's basis | card id |
|---|---|---|---|---|
| Google traffic advantage over ChatGPT | ~190x more traffic to websites | framing for "don't abandon SEO" | presenter's stated figure `[web check]` | 7c2ebc1068d0 |
| Google search volume growth | ~20% year over year | same framing | presenter's stated figure `[web check]` | 7c2ebc1068d0 |
| Google search volume | "over 5 trillion searches a year" | framing for AI-search chapter | presenter's stated figure `[web check]` | none (transcript only) |
| Title tag length | under 60 characters | any page | presenter's rule of thumb `[verify UI: current SERP truncation]` | ce6536d71069 |
| Meta description length | 150-160 characters | any page | presenter's rule of thumb `[verify UI]` | ce6536d71069 |
| Cluster size | roughly 5-10 interconnected articles | one narrow topic before moving on | presenter's rule of thumb | 618a252af117 |
| "Coffee" example volume/competition | ~650,000 US searches/month, messy/undefined SERP | head-term example | presenter's SERP read, single example | f32610667b5f |
| "Best dark roast coffee beans for espresso" example | a few hundred searches/month, uniform comparison SERP | longtail example | presenter's SERP read, single example | f32610667b5f |
| "Contract template" keyword | ~300,000 searches/month | top-funnel example (Panda) | presenter's claim about Panda's data, not verified | 03569978ba18 |
| "Pour over coffee" | ~34,000 searches/month | educational-intent example (Counterculture) | presenter's example | 03569978ba18 |
| "Coffee subscription" | ~15,000 searches/month | money-page keyword example (Counterculture) | presenter's example | 28f51e6a77cb |
| "Pour over coffee ratio" | ~10,000 searches/month | cluster example | presenter's example | 03569978ba18 |
| "Cold brew ratio" | ~6,800 searches/month | cluster example | presenter's example | 03569978ba18 |
| "Coffee brewing methods" | ~5,200 searches/month | cluster example | presenter's example | 03569978ba18 |
| "Coffee to water ratio calculator" | ~500 searches/month, keyword difficulty 8 | linkable-asset example | presenter's example, tool-scored difficulty `[verify UI: difficulty-score methodology]` | b7d9a9c621b3 |
| Content quality bar vs. existing top results | "at least 5x better" | new content vs. what already ranks | presenter's heuristic, not measured | 5ff1064a03ea |
| Share of web pages with zero Google traffic | over 96% | Ahrefs study of 14 billion pages, cited secondhand | Ahrefs data as relayed by presenter `[web check: primary Ahrefs source]` | 5ff1064a03ea |
| Journalist-query hit rate | roughly 1 hit per 100 submissions | Source of Sources / Featured.com outreach | presenter's estimate | 88997600260b |
| Time budget for journalist queries | ~15 minutes/day | ongoing link-building habit | presenter's recommendation | 88997600260b |
| Content pieces before starting outreach | 10-15 pieces | beginner sequencing | presenter's recommendation | 88997600260b |
| Screaming Frog free tier | up to 500 URLs | technical audit | presenter's stated figure `[web check: current free-tier limit]` | e9e95368a588 |
| Technical readiness on modern CMS | "~90% of the way there" | Shopify/WordPress/Webflow/custom CMS, small-mid business | presenter's estimate, not a measured audit | e9e95368a588 |
| Vibe-coded calculator build time | ~10 minutes, "nearly zero coding experience" | fictional Stockpath example, Claude Code | single anecdote | b7d9a9c621b3 |

## 5. Diagnostics and checks

| check | how | good | bad | next step | card |
|---|---|---|---|---|---|
| Is the target keyword's intent matched by my planned page? | Run the 30-second intent test (3.1) | Top 10 results are the same format as my planned page | Top 10 are a different format (e.g. blogs when I planned a product page) | Change page type, or retarget the keyword to a different page type in the funnel | f32610667b5f |
| Does this keyword score on the Sweet Spot framework? | Check demand, fit, intent, difficulty individually | Scores well on most/all four | Scores on 0-1 attributes, or difficulty is unrealistic for site authority | Deprioritize, or use as a top-funnel play only with a defined conversion path | 03569978ba18 |
| Do money pages exist yet? | List conversion pages against the catalog/service list | Every core product/category/pricing page exists and is optimized | Gaps exist, or blog content exists with nowhere for traffic to convert | Build the missing money page(s) before any new blog content `[needs brand data: current page/catalog inventory]` | 28f51e6a77cb |
| Is content spread thin across clusters? | Map published content to topical clusters | One cluster nearly complete (5-10 pieces) before starting next | Content scattered across many half-built clusters | Pause new clusters; finish the current one first | 618a252af117 |
| Does my page beat the AI overview for its query? | Search the query, read the live AI overview, compare to my draft | My page adds data/opinion/specifics the summary lacks | My page just restates the summary | Add original data, hands-on experience, specific numbers or opinionated recommendations | 245141abe8fc |
| Is my brand visible in AI assistant answers? | Ask a buying-journey question in a fresh incognito AI chat window | Brand is named / recommended | Brand does not appear; competitors do | Build topical authority + citations (3.10); re-check periodically since answers shift | 46a784e2d55c / 7c2ebc1068d0 |
| Is the on-page checklist complete? | Walk through title, H1/H2/H3, URL, meta description, internal links, image alt text for the page | All present and following the format rules in 3.7 | Missing elements, CMS-generated URL, repeated/generic alt text | Fix each element; treat as a floor, not a finish line — even the source's "well-optimized" example sites left items incomplete | ce6536d71069 / 91cc4c076fd9 |
| Is SEO progress showing in Search Console yet? | Review impressions, new keywords, position trend | Rising impressions, new query entries, upward position movement | No movement after a reasonable window, or judging on 1-2 days of data | Treat rising impressions with flat clicks as progress; use new keywords as content-planning input | 9bb24c359ea8 |
| Are technical issues blocking rankings? | Run Screaming Frog crawl | Few or no broken links/missing tags/duplicate content/redirect chains/missing alt text | Crawl surfaces a long prioritized issue list | Fix top-priority items first; don't treat this as the main blocker if the site is unpublished/thin on content instead | e9e95368a588 |

## 6. Tools, settings and named features

| tool or feature | use in the source | tag |
|---|---|---|
| Google Search Console | Best/most accurate source of real keyword ideas already driving traffic to your site; also used for weekly progress signals (impressions, new keywords, position) | `[verify UI]` free, essential per source |
| Surfer (content editor, keyword research, AI tracker, mention gap report, Keyword Surfer Chrome extension) | Named throughout for: keyword validation, keyword clustering, competitive content research/outline generation, real-time content score (0-100) and AI-search score, AI visibility tracking across ChatGPT/Gemini/Perplexity, auto internal-linking, mention-gap reporting for citation opportunities | `[verify UI]` **sponsored/affiliate — the video ends with an explicit Surfer promo and link; treat every Surfer capability claim as a vendor claim, not independent evidence** |
| Screaming Frog SEO Spider | Free technical crawler (up to 500 URLs stated); surfaces broken links, missing title tags, duplicate content, redirect chains, images without alt text | `[verify UI/web check: current free-tier limit and pricing]` — no visible sponsorship tie in this source |
| Source of Sources | Free journalist-query platform, created by the original founder of HARO; respond to reporter queries with quotes for backlinks | `[web check: current platform status]` |
| Featured.com | Alternate journalist-query platform named alongside Source of Sources | `[web check: current platform status]` |
| Google Business Profile | For businesses with a physical location: claim it, complete every field, gather and respond to reviews, to help local map-pack placement | `[verify UI]` |
| ChatGPT / Claude / an AI assistant (unspecified) | Used for: sitemap content-gap analysis, competitor sitemap analysis, generating buyer-question seed lists, drafting content outlines from research notes, drafting AI-assisted first drafts | `[verify UI]` |
| Claude Code / Codex | Named as "vibe coding" tools a non-technical marketer used to build a linkable-asset calculator in ~10 minutes | `[web check: current tool names/capabilities]` |
| WebP image format | Recommended image format for compression alongside descriptive names and alt text | `[verify UI: current best-practice format]` |

## 7. Examples and case results

All are the presenter's own client work or single anecdotes, not controlled tests or guarantees.
- Panda (SaaS, proposal software): ranks "contract template" (~300k/mo); template directory drives "hundreds of thousands of visits" via free download → email capture → nurture → signup. [03569978ba18]
- Counterculture (specialty coffee ecommerce): ranks "pour over coffee" (~34k/mo), "pour over coffee ratio" (~10k/mo), "cold brew ratio" (~6.8k/mo), "coffee brewing methods" (~5.2k/mo) with educational blog content, not conversion pages; subscription page already ranks "coffee subscription" (~15k/mo). [03569978ba18] [28f51e6a77cb]
- Counterculture's pour-over brew guide is cited by WikiHow, Gear Patrol, Breville and "dozens of coffee blogs" as the most thorough guide on the topic. [88997600260b]
- Huntress (managed cybersecurity): ransomware-recovery guide (educational) and managed-EDR page (money page) used to demonstrate the on-page checklist applied two ways; Huntress's ransomware/data-breach content is cited by a cloud provider's threat-intelligence team and referenced on Wikipedia. [ce6536d71069] [88997600260b]
- Huntress's managed-EDR page alt text ("malicious process behavior," "ransomware canaries") is called decent but not specific enough; its ransomware guide repeats "glitch effect" across most images, called a missed opportunity — "even well-optimized sites leave SEO on the table." [91cc4c076fd9]
- Fictional company "Stockpath": presenter vibe-coded an inventory calculator with Claude Code in about 10 minutes with "nearly zero coding experience," offered as proof that linkable-asset tools are now feasible for non-technical marketers. [b7d9a9c621b3]
- Manual AI-visibility check screenshots: "best proposal software for agencies" → Panda; "best specialty coffee beans" → Counterculture; "what companies can help me protect my network from ransomware?" → Huntress. [46a784e2d55c] [7c2ebc1068d0]
- Ahrefs study of 14 billion web pages (cited secondhand): over 96% get zero traffic from Google — used to argue that most content fails from sameness, not low quality. [5ff1064a03ea]

## 8. Mistakes the source warns about

1. Abandoning SEO for a GEO-only strategy because "SEO is dead" — the AI channels are built on top of traditional search indexes. [7c2ebc1068d0]
2. Fighting the SERP's established intent instead of matching your page type to it. [f32610667b5f]
3. Chasing high-volume head terms with a new/low-authority site instead of building up from longtail terms. [f32610667b5f]
4. Targeting a keyword purely for its volume with no plan for what happens after the click (vanity traffic). [03569978ba18]
5. Publishing informational blog content before money pages exist, leaving converting traffic nowhere to go. [28f51e6a77cb]
6. Spreading content across many topical clusters at once instead of finishing one before starting the next. [28f51e6a77cb] [618a252af117]
7. Believing search-volume research alone (sort by low competition/high volume, work down the list) is a sound content plan — it fragments topical authority. [28f51e6a77cb]
8. Publishing AI-drafted content with no added human differentiation ("AI slop") in a market where 96%+ of pages already get zero traffic. [5ff1064a03ea] [b7c89ca36202]
9. Skipping the outline/structure step before writing. [5ff1064a03ea]
10. Using CMS-generated random-string URLs instead of short, descriptive, keyword-bearing ones. [ce6536d71069]
11. Leaving generic or repeated alt text (e.g. reusing "glitch effect" across many images) instead of describing each image specifically. [91cc4c076fd9]
12. Skipping internal linking because it feels less urgent than publishing the next piece — called one of the best effort-to-value ratios in SEO. [91cc4c076fd9]
13. Buying links or taking outreach shortcuts that eventually get penalized. [88997600260b]
14. Obsessing over link building before you have 10-15 solid pieces of content published. [88997600260b]
15. Going down a full technical-SEO rabbit hole as a beginner when the actual bottleneck is not having published content yet. [e9e95368a588]
16. Assuming your AI-assistant answer once checked stays the same — AI recommendations shift over time and unmonitored brands lose visibility without noticing. [46a784e2d55c]
17. Letting a page merely restate the AI overview instead of going deeper than it. [245141abe8fc]
18. Copying another business's funnel/intent ratio instead of building your own, since SaaS, ecommerce and service businesses have very different mixes. [fb8f4b373003]

## 9. Caveats, conflicts and what is missing

- Sponsorship: the video promotes Surfer throughout — keyword validation, clustering, content research/outline generation, content scoring, internal-linking automation, AI tracking and mention-gap reporting are all shown as Surfer features, and the video closes with an explicit affiliate-style plug. None of Surfer's stated capabilities are independently verified in this source; treat as vendor claims carried by the presenter. Screaming Frog and Source of Sources/Featured.com appear to be genuine free-tool recommendations with no visible commercial tie in this source, but should still be `[web check]`ed for current pricing/availability.
- One card caveat (on the 30-second intent test) states an "editorial qualification" that paid placements must use sponsored/nofollow link attributes and that unqualified paid links should not be bought to manipulate rankings. This does not appear anywhere in the transcript text — it is a card addition, not something the presenter said. Treat it as a standard SEO compliance note added by the card author, not sourced to this video. [f32610667b5f]
- "Kawa Locker ransomware," named as an internal-link example on Huntress's ransomware guide, reads as a transcription artifact of a real ransomware family's name. Verify the actual name before reusing this example. `[web check]`
- The presenter gives no keyword-difficulty score thresholds, no explicit word-count targets (only "match the average length of the top 5, don't just hit a number"), and no fixed timeline for when a cluster should be considered "finished" beyond the loose 5-10 article guideline.
- No measurement method is given for AI-overview-caused lost clicks (2.15) — it is offered as a content-depth principle, not a trackable metric.
- No content-freshness or refresh-cadence guidance beyond "updating a page already on page 2-3 can be faster than starting over" — no specific refresh interval or trigger is given.
- Local SEO is explicitly flagged by the presenter as too large a topic for this video; the Google Business Profile advice is a starting point only, not a complete local-SEO program.
- Internal tension worth flagging: the presenter recommends both manual, first-principles work (read the top 5 results yourself; do keyword research by hand at first) and heavy reliance on one paid tool to automate nearly the same steps later. He frames the manual pass as pedagogical ("so you understand what you're automating"), not as an alternative once you have budget.
- Conflicts with general SEO advice: none flagged as explicit disagreements with other named sources in the folder — this source's core claims (intent-first targeting, topical authority via clusters, money-pages-before-content sequencing, E-E-A-T-style human differentiation, technical SEO as usually already "good enough" on modern platforms) align with mainstream SEO guidance rather than contradicting it. The one point that could read as counter to common advice is deprioritizing formal technical-SEO audits for beginners on modern CMS platforms — some sources put more weight on technical audits earlier; this source explicitly argues against that for small/mid sites.
- Scope: keyword-level rank tracking, GSC mechanics in more depth, and site-audit workflows belong to the companion Search Console source already filed in this folder; paid-search attribution, ROAS and ad-account tracking are explicitly out of scope per the folder header and route to 06-MEA; visual landing-page layout design routes to 07-LPG.

## 10. Card index

- 7c2ebc1068d0: Two-Channel Visibility: Traditional SEO as the Foundation for AI Search
- f32610667b5f: Run the 30-Second Intent Test Before Targeting Any Keyword
- 03569978ba18: The Keyword Sweet Spot Framework: Demand, Fit, Intent, Difficulty
- 28f51e6a77cb: Money Pages First: Build Conversion Pages Before Informational Content
- 618a252af117: Topical Authority Clusters: Why Google Evaluates Your Whole Site
- 0648fb2c0ce2: Keyword Ideation: Mine Google's Own Data Before Reaching for Tools
- fb8f4b373003: Keyword Validation and Clustering With AI
- 5ff1064a03ea: Content Creation Blueprint: Research, Structure, Write, Optimize
- b7c89ca36202: Build Human Content Moats into AI-Assisted Drafts
- ce6536d71069: On-Page Checklist Applied to Both Money Pages and Content Pages
- 91cc4c076fd9: Internal Linking as the Connective Tissue of Your Funnel
- 88997600260b: Link Building: Be the Source, Then Use Journalist Queries
- b7d9a9c621b3: Create Linkable Assets: Tools, Calculators and Templates as Backlink Magnets
- e9e95368a588: Technical SEO Triage: Audit With a Crawler Instead of a Rabbit Hole
- 46a784e2d55c: AI Search Optimization: Structured Content, Clusters and Third-Party Citations
- 245141abe8fc: Zero-Click Era: Make Content Deeper Than the AI Overview
- 63c02d6a7770: 30-Day SEO Action Plan for a Store
- 9bb24c359ea8: Track SEO Progress With Leading Indicators, Not Just Clicks
