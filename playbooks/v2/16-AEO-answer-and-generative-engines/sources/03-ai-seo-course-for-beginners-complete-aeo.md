# AI SEO Course for Beginners: Complete AEO Tutorial

source_id: 1Y-SLLJCddFSGRu_WwMBWFN4555wUygUa  |  folder: /16-AEO-answer-and-generative-engines  |  cards: 37  |  words: 15,583  |  type: course (transcript, one presenter, intro plus 4 modules, Ahrefs-branded)

credibility: One presenter (name given as "Sam Oh," auto-transcribed at points as "Samo" and "Ammo") delivering an official Ahrefs course. Every piece of hard evidence is either an Ahrefs-run aggregate study (75,000 brands; 174,000+ AI-Overview-cited pages; 140 million websites; Ahrefs' own site's AI mention counts and conversion data) or a named third-party anecdote (Vercel, Tally) relayed secondhand, plus one unnamed misinformation experiment Ahrefs says it ran. No methodology, sample window, or link is given for any study inside the transcript. Nearly every workflow routes through a paid Ahrefs product: Brand Radar, Site Explorer, Keywords Explorer, Content Explorer, Site Audit, Web Analytics, Bot Analytics. Treat this as vendor content sold alongside a tool suite, not independent research. `[web check: are the underlying Ahrefs studies published anywhere with methodology?]`
date signals: The presenter says "As of December 2025" for the AI-Overview click-through stat, so recording is at or after Dec 2025 (consistent with the Drive file's 20 Sep 2026 modification date). GPT-4 is named specifically for the YouTube-transcript training claim, which may already be superseded by newer models. The 76%-of-citations-from-Google-top-10 figure is given, then revised down to "closer to 38%... a more recent study" in the same breath, with no date attached to either figure. Every platform-specific number (market share, citation percentages, referral-passing behavior, crawler names, JS-rendering support, llms.txt adoption) is a snapshot that is very likely already stale; tag `[web check]` before using any of it in front of a client.

## 1. What this source is for

It gives an operator a full-funnel AEO/GEO program: how AI answer engines retrieve and cite content (training data vs. real-time retrieval, query fan-out), how the major platforms differ in what they cite, how to run a brand gap analysis, how to do AEO-specific keyword and prompt research (BID formula plus an "AI filter"), how to write and refresh content so AI can extract it, how to earn third-party mentions across three tiers, a YouTube-specific AEO workflow, six technical AEO checks, and three complementary ways to measure AI's effect on the business, ending in a one-week starter action plan. It is strongest on the mechanics of AI retrieval and on giving concrete, named report/filter workflows inside one vendor's tool. It is weakest on ecommerce-specific application (it never once uses a product-detail-page example itself; all ecommerce framing above the raw transcript was added by the card author), on citing sources for its platform-behavior claims, and on anything that needs a hard number for a decision (the "AI filter" and "quick win" prioritization are explicitly judgment calls).

## 2. Principles

1. **AEO builds on SEO; it does not replace it.** The presenter frames AI search as additive, not a zero-sum replacement (the "zero-sum bias" argument, using mobile apps vs. the web as the analogy). Condition: applies to allocating budget between the two, not to individual tactics. Evidence: SEO fundamentals (quality content, authority, technical health) still feed AI's real-time retrieval. (transcript; no dedicated card)
2. **AI answers come from two separate levers: training data and real-time retrieval (RAG).** Training data is static and updates on an unstated cadence ("maybe every 6 months or so," presenter's approximation); real-time retrieval kicks in for fresh or very specific questions. Condition: a brand-new product needs retrieval-side work (crawlable, accurate pages) since training data will not know about it yet. [d477a2718a07]
3. **Query fan-out means you must cover a whole topic, not one keyword.** A single prompt expands into many synthetic sub-queries run in parallel and merged into one answer. Evidence: research cited by the source finds an average prompt triggers 9-11 fan-out queries, some as high as 28, and one ChatGPT deep-research run used 420 searches for a single query. Condition: applies to category pages and buying guides, not to why a specific exact-match keyword page fails. [a227df367635]
4. **AI visibility is probabilistic, not a fixed rank.** The same prompt run five times can cite you a different number of times because of training patterns, retrieved-page signals, and a randomness ("temperature") setting. Condition: set KPIs as a share-of-voice/distribution metric, not a rank-tracking metric. [f85af788af43]
5. **Platforms barely overlap in what they cite (14% overlap across the top 50 domains on Google AI Overviews, ChatGPT and Perplexity).** Condition: pick 1-2 priority platforms based on market share and overlap with your existing SEO strengths, rather than optimizing generically for "AI search." [e8d6d277ebfb]
6. **AI visibility is a spectrum: cited+linked, mentioned-but-unlinked, or invisible.** Only ~28% of AI mentions carry a link on average (range 10.7% to 51.6% by platform), so most of the value of being mentioned is not click-through. Condition: match the goal to business type — retailers want category-query mentions with a path to purchase; publishers should value training-data presence as a long game. [dc9263a72730]
7. **Branded web mentions correlate with AI-Overview visibility more strongly than backlinks or domain rating.** Reported correlation: 0.664 across 75,000 brands; mentions specifically on highly-linked pages correlate even higher, at 0.7. Correlation, not proof of causation. [23ce7debe703] [dc9263a72730]
8. **Content length does not predict citation; freshness and format do.** Across 174,000+ AI-Overview-cited pages, word count correlated with citation at just 0.04. Cited content is reported ~25-25.7% fresher than what ranks organically, and 43.8% of ChatGPT citations are listicles/comparisons. Condition: stop lengthening pages to try to earn a citation; refresh and reformat instead. [9edf8483abdc]
9. **Write for extraction, not for a special "AI format."** The source is explicit there is no separate AI-optimized writing style — content that serves human readers (BLUF, atomic sections, entity-rich, declarative sentences) is what AI wants to cite, because it is trained on what humans find valuable. [08fd8b80c5a7]
10. **Screen keywords with BID before spending content budget, then apply an AI filter.** Business potential, Intent-match to the SERP, and Difficulty must all pass; then check whether an AI overview already fully answers the query — if so, redirect the effort toward an AEO mention or toward action/tool/transactional queries AI cannot satisfy. [caec8fa7e6e5] [f51f401ddf5f]
11. **Reddit and other UGC is heavily cited and used as LLM training data — earn it, never spam it.** The source is explicit that dropping a brand name into threads "will backfire fast"; the play is genuinely useful, on-topic answers. [7285d50f35a8] [3347a4baaad4]
12. **YouTube is a top-cited domain and a documented AI training source (GPT-4 was trained on over a million hours of YouTube transcripts, per the source).** Target "search hits" (sustained search demand) over "viral hits" (a view spike that dies once the algorithm's interested pool is exhausted). [926976b809be]
13. **Robots.txt is the most common accidental technical blocker, and Cloudflare's AI-bot setting is a common unintentional cause.** Cloudflare's "instruct AI bot traffic" feature is on by default and can auto-update a site's robots.txt to disallow AI crawlers without the owner's knowledge. Check this before any other technical AEO work. [bc44a7efd9f2] [75ea98447324]
14. **JavaScript rendering and page speed matter more for AI retrieval than assumed, because AI crawlers fetch, parse and chunk pages live.** A slow or JS-only page can be dropped before it is even scored. [d9728871b1a5]
15. **No single analytics source shows AI's full effect — combine three.** Referral traffic (what AI actively sends), bot analytics (what AI is paying attention to), and self-reported attribution (what is actually converting, including invisible zero-click influence) each cover a different blind spot. [e3fe0904f52d]
16. **Fill every information gap about your brand with specific, official facts, or AI will fill it with "specific fiction."** In the source's own misinformation test, AI platforms chose specific false claims over vague or absent official truth. [748700e7c99c]
17. **AI referral traffic is small today (~0.25% of total site traffic) but converts far above organic search, and the case for early investment rests on trajectory, not current volume.** [791c035b0f54]
18. **Use a six-dimension gap framework (visibility, narrative, topic, format, web mentions, demand) to decide whether to fix, build, or influence.** Most brands' gaps cluster in one or two of the six, which the source frames as a signal for where to build systems. [7ccc34f2e89e]
19. **Refresh "sleeper pages" (existing backlinks, declining traffic) before writing net-new content, since freshness plus prior authority is the fastest route to a new citation** — but only if the decline is a content problem, not a links problem. [4e6f7e7f1aa7]
20. **Brand your own original frameworks and repeat the branded name everywhere, or LLMs will flatten the idea into unattributed general knowledge.** [2fcdce4950af]
21. **Do not treat AEO as a one-time project.** Over 45% of AI-Overview citations change when the overview refreshes, which the source says happens roughly every two days; mention audits, gap analyses, and topic-coverage checks all need to repeat on a monthly/quarterly cadence. [35cbd98861df] [0d40ada60dfc]

## 3. Procedures

### A. Brand gap analysis
1. Map branded entities: main brand, sub-brands, product names, proprietary features or metrics, and any personal brands tied to the company. Each gets its own visibility profile and can be analyzed separately.
2. Attach the topics and attributes each entity should be associated with, using keyword research to find recurring adjectives/modifiers people already use alongside the brand or category.
3. Enter the domain into a site-metrics tool for a baseline (domain rating, referring domains, organic keywords/traffic/value), then open the AI-citation view for each platform. `[verify UI: Ahrefs Site Explorer -> Brand Radar]`
4. Record four metrics per platform: mentions, citations, impressions, AI share of voice.
5. Use the tool's filters to isolate: prompts naming your brand; responses that mention your brand but do not cite your site (missed-citation opportunities); a competitor added and filtered to "others only" (they are named, you are not); and specific topics to see who AI associates them with. `[verify UI]`
6. Classify every finding into one of six gaps: visibility, narrative, topic, format, web mentions, demand (definitions in section 5).
7. Prioritize by asking: how much demand could this drive, does it support brand credibility, does it improve citation odds. Label each item fix (optimize existing), build (create new), or influence (offsite mentions). Start with quick wins — a ranking page that just needs a topic update, or a major listicle competitors are on that outreach can win.
8. Repeat the identical audit on named competitors to surface gaps you overlooked.
[7ccc34f2e89e]

### B. AEO keyword and prompt research
1. Build a keyword list from seed terms (1-2 words, broad) plus modifiers (best, how-to, etc.). Shortcut: ask an AI assistant for 10 seed keywords and 5+ modifiers given a description of the site, revenue model and audience, specifying seeds and modifiers must not share words.
2. Paste seeds into a keyword tool's matching-terms report and add modifiers via an include filter to generate a candidate list. `[verify UI: Ahrefs Keywords Explorer]`
3. Vet with BID: Business potential (would ranking #1 actually help the business — "what is espresso" vs. "best espresso machine under $500"); Intent (search the term, check whether the ranking page type matches what you plan to build); Difficulty (check referring domains/DR of the top 10 — a few low-DR sites in the top 10 is a good sign).
4. Apply the AI filter: search the keyword, read the AI overview as the searcher would. If it fully answers the query, drop it as a traditional click target. Redirect that effort to (a) an AEO mention play for that query, or (b) action/tool queries AI cannot do yet (modifiers: calculator, checker, generator, tool, template, finder, planner, maker), or (c) transactional-intent-filtered queries.
5. Find AI-mention gaps: enter your domain in the brand-visibility tool, hover the target platform, click the "others only" filter, then layer keyword filters for best/top/versus/review/alternative. This is your AEO short list. `[verify UI: Ahrefs Brand Radar]` Repeat regularly — citations shift often (see rule table).
6. Do prompt research separately from keyword research: map the full chain of natural-language follow-up questions a real buyer might ask (chat queries are conversational, not term-based); do not try to target individual fan-out sub-queries since >95% have zero search volume and are inconsistent run to run.
[caec8fa7e6e5] [f51f401ddf5f] [35cbd98861df] [a227df367635]

### C. Content that gets cited
1. Open every section with the direct answer (BLUF), then support it with context — not the other way around.
2. Make each H2 section atomic: read it in isolation and rewrite if it depends on earlier paragraphs, since AI may chunk your page at any heading boundary and you cannot control where.
3. Write entity-rich: name the specific brand, product, or concept instead of a vague reference ("Ahrefs Keywords Explorer helps you find low-difficulty, high-traffic-potential keywords" instead of "this tool helps with SEO").
4. Keep sentences simple and declarative: one idea per sentence, clear subject-verb-object; if a sentence takes two reads, simplify it.
5. Choose the format that already gets cited for your target query — listicle, comparison, or original data/stats — rather than defaulting to a blog post.
6. Do not chase word count; write to the length the topic needs.
7. When refreshing, make substantive changes (new stats, examples, current information) — do not just change the publish date.
8. Find sleeper pages first: pull a top-pages report sorted by traffic decline, filter for pages that already have backlinks and a clear decline. Confirm the page had meaningful referring domains before assuming a rewrite will fix it. `[verify UI: Site Explorer]`
9. Brand any original framework you invent: name it with your brand prefix, define it explicitly on your own site, and distribute it with the name attached across blog, social, podcast and community channels.
[08fd8b80c5a7] [9edf8483abdc] [4e6f7e7f1aa7] [2fcdce4950af]

### D. Earning mentions, three tiers
**Tier 1 — editorial/listicles/comparisons:**
1. Open a cited-domains report for your brand's topics to see which sites AI already cites in your category. `[verify UI: Brand Radar]`
2. Use a content-research tool with a title:best or title:versus search plus a minus-operator on your own brand name to surface listicles/comparisons that omit you. `[verify UI: Content Explorer]`
3. Filter by referring domains to prioritize pages that already carry authority.
4. Pursue inclusion via outreach — do not wait for a page to already be cited; strong links plus topic relevance predict a future citation.
**Tier 2 — UGC/community:**
1. Check the cited-domains report for reddit.com and niche forums in your space. `[verify UI]`
2. Alternatively, run reddit.com through an organic-keywords report, filter to top-5 rankings, and add your niche terms, to find already-ranking threads. `[verify UI: Site Explorer]`
3. Contribute genuinely useful, on-topic answers only; never insert brand mentions into unrelated threads.
**Tier 3 — owned properties:**
1. Treat your YouTube channel, podcast, LinkedIn, and any secondary domains as additional citation sources; keep every one of them positive and topically relevant so AI has good training examples.
**Ongoing maintenance:**
1. Run a recurring brand-mention audit: track mention volume over time, investigate any drop, and check sentiment/accuracy of what AI says about you.
2. If you find misinformation, fix your own content first (publish the correct, specific facts), then request a correction from the third-party publisher. Move fast — the longer bad information sits, the more time AI has to learn it.
[23ce7debe703] [2037fd15a632] [7285d50f35a8] [3347a4baaad4] [de260c9bccd9] [445fa90e4caf]

### E. YouTube AEO
1. Find search-hit topics: run www.youtube.com/watch through an organic-keywords report, filter to top-3 rankings, and add your niche terms. `[verify UI: Site Explorer]`
2. Make the video rank: put the exact target keyword in the title (no clickbait — save cleverness for the thumbnail); write a real descriptive summary in the description with the keyword in the first couple of lines; add timestamps so they become chapters; say the keyword aloud in the video (the source attributes to Google's VP of Search the claim that Google understands audio content `[web check]`); match the format already ranking (tutorial vs. listicle).
3. Layer in AI visibility: open a topics report for a popular brand/channel in your space, filter to mentioned-domain = youtube.com, and see which queries are pulling YouTube videos into AI answers; create content for those topics. `[verify UI: Brand Radar]`
[926976b809be] [224d5f463421] [1af9f13ebe90]

### F. Six technical AEO checks
1. **Robots.txt.** Visit yourdomain.com/robots.txt; look for Disallow rules against GPTBot, OAI-SearchBot (OpenAI), ClaudeBot (Anthropic), or Google-Extended (Google). `[verify UI]` If the site runs on Cloudflare, separately check the "instruct AI bot traffic" setting — it is on by default and can auto-add these disallow rules. `[verify UI] [web check: current Cloudflare default]` A site-audit crawl can flag these automatically.
2. **llms.txt (low priority).** A proposed file at yourdomain.com/llms.txt summarizing the site for AI. At recording time, OpenAI does not use it, Anthropic publishes one but has not confirmed its crawlers read it, and Google has not adopted it. The source says it will not hurt but should not be prioritized. `[web check: current adoption]`
3. **JavaScript rendering.** Rendering support differs by crawler (source claims Gemini and Copilot can render JS, ChatGPT's crawler cannot `[web check]`). Test by disabling JavaScript in a browser and revisiting your own page; if content disappears, add server-side rendering or a pre-rendering solution.
4. **Page speed.** AI fetches, parses and chunks pages live and can drop a slow page before it is scored. Core Web Vitals work already done for SEO covers most of this.
5. **Clean HTML structure.** Proper heading hierarchy (H1 title, H2 sections, H3 subsections), each section self-contained, one idea per paragraph — since AI may chunk at any heading boundary.
6. **Schema markup.** Keep accurate schema you already use for SEO (Product/Offer, Organization, BreadcrumbList, Article, FAQ, HowTo as fits the page); there is no confirmed evidence it improves AI citation specifically, so do not over-invest in it for AEO alone.
7. **AI-hallucinated 404s.** Check analytics for sessions from AI referrers landing on 404 pages. If a hallucinated URL gets consistent traffic, redirect it to the closest real page instead of letting the journey end there.
[bc44a7efd9f2] [75ea98447324] [d9728871b1a5] [a4891c6c3426] [ccbc5be4692f] [64a695c65c71]

### G. Measurement setup
1. **GA4 AI-traffic channel.** Admin > Data Display > Channel Groups; copy the default group; add a channel named "AI traffic"; set the source to a regex matching AI referrer hostnames (source's example list: chatgpt.com/chat.openai.com, perplexity, gemini.google.com, copilot.microsoft.com, claude.ai, deepseek.com — verify current domains and escape dots/use hostname boundaries). `[verify UI] [web check: current AI referrer hostnames]` Then review under Reports > Acquisition > Traffic Acquisition. Note several platforms strip referral data (paid-account ChatGPT in-content links use no-referrer; Perplexity tracks on web but not its desktop app; Copilot tracks on web but not Windows; Grok passes no referral data at all per the source) — treat any referral count as an undercount. `[web check: current referrer-passing behavior]`
2. **Bot analytics.** Use server logs if available, or a bot-analytics tool with a Cloudflare integration that the source says works on Cloudflare's free plan. `[verify UI] [web check: pricing]` Separate training bots (GPTBot, Google-Extended) from search/citation bots (ChatGPT-User, OAI-SearchBot); repeated citation-bot visits to a page suggest it is being used as a source.
3. **Self-reported attribution.** Add a "How did you hear about us?" question to sign-up, checkout, or the post-purchase survey, with options such as AI assistant, ChatGPT, Perplexity, AI search (e.g., Google AI Overviews), organic search, social, and a friend/colleague, plus free text.
4. **Combine all three**, plus ongoing brand-visibility tracking across platforms, since no single source gives the complete picture.
5. **Cadence:** a monthly check of AI share of voice, cited domains, topic coverage, and mention sentiment; a deeper competitive audit quarterly.
[c2ae662a8e4f] [8f0d6e616976] [990877b3d70c] [e3fe0904f52d] [0d40ada60dfc]

### H. Starter action plan (week 1)
1. Check robots.txt for AI bot access (~5 minutes) — the most common technical blocker.
2. Set up AI analytics: build the GA4 AI channel or a web-analytics tool with a built-in AI channel, and add the "how did you hear about us" survey question so measurement starts from day one.
3. Update your top 5-10 most important pages for freshness with substantive changes (new stats, examples, current information).
4. Run the brand gap analysis (procedure A) to know your baseline before optimizing.
5. Identify your top 10 mention-earning targets using cited-domains and pages reports.
6. Then maintain the ongoing cadence: monthly brand-visibility check, quarterly competitive audit, repeat.
[bef60df0b856]

## 4. Rules, thresholds and numbers

| Rule / stat | Number or threshold | Condition | Source's basis | Card |
|---|---|---|---|---|
| AI Overview effect on #1 result's CTR | Reduces it by 58% | As of December 2025 | Ahrefs on-screen stat `[web check]` | transcript only |
| ChatGPT scale | 900 million weekly users; handles ~12% of Google's search volume | — | Cited stat `[web check]` | transcript only |
| AI traffic growth | Grown 9.7x in the past year | — | Ahrefs data `[web check]` | [791c035b0f54] |
| Ahrefs' own AI-vs-organic conversion | June 2025: AI search = 0.5% of Ahrefs' traffic but 12.1% of signups (23x higher conversion than organic) | Single-company example | Ahrefs example | transcript only |
| Ahrefs' organic AI mentions | 7,470 mentions across 2,309 pages, no deliberate AEO effort | Single-company example | Ahrefs example | transcript only |
| Query fan-out size | Average 9-11 sub-queries per prompt, up to 28; one case ran 420 searches | Per prompt | Seer Interactive & Nectaf research, cited by source `[web check]` | [a227df367635] |
| Fan-out queries with zero search volume | Over 95% | — | Ahrefs/Despina's guide | [a227df367635] |
| AI-Overview citations from Google top 10 | Was 76%, a "more recent study" puts it near 38% | Trend, not a fixed number | Ahrefs data | [e8d6d277ebfb] |
| AI-Overview citations not ranking in Google's top 100 at all | 14% | — | Ahrefs data | [e8d6d277ebfb] |
| Content freshness of AI-cited pages | ~25-25.7% fresher than organic SERP results | — | Ahrefs data | [9edf8483abdc] [f85af788af43] |
| Top-50 domain overlap (Google AI Overviews / ChatGPT / Perplexity) | 14% (7 of 50 shared) | — | Ahrefs data | [e8d6d277ebfb] |
| YouTube share of AI-Overview citations | 5.6% | — | Ahrefs data | [e8d6d277ebfb] |
| ChatGPT top-cited pages, median domain rating | 90 | — | Ahrefs data | [e8d6d277ebfb] |
| Perplexity citations from Google top 10 | 28.6% (vs. 8-10% for ChatGPT) | — | Ahrefs data | [e8d6d277ebfb] |
| Google AI Mode vs. AI Overviews citation overlap | 13.7%, despite 86% semantic similarity in answers | — | Ahrefs data | [e8d6d277ebfb] |
| AI Mode's Quora citation rate | 3.5x AI Overviews' rate | — | Ahrefs data | [e8d6d277ebfb] |
| Average link rate in AI mentions | ~28% overall; 51.6% Perplexity, 36.8% AI Mode, 26.9% ChatGPT, 10.7% AI Overviews | — | Ahrefs data | [dc9263a72730] |
| Link concentration by impression | Perplexity: links in 78% of impressions vs. 51% of mentions; Gemini: 71% of impressions vs. 16.8% of mentions | — | Ahrefs data | [dc9263a72730] |
| Branded mention correlation with AI-Overview visibility | 0.664 across 75,000 brands | Correlation, not causation | Ahrefs study | [23ce7debe703] [dc9263a72730] |
| Highly-linked-page mention correlation | 0.7 | Higher than general mentions | Ahrefs study | [23ce7debe703] |
| YouTube-mention correlation with ChatGPT visibility | 0.737, described as the strongest of all factors studied | — | Ahrefs study | transcript only |
| Word count vs. citation correlation | 0.04, across 174,000+ cited pages | — | Ahrefs study | [9edf8483abdc] |
| Cited pages under 1,000 words | 53.4% | — | Ahrefs study | [9edf8483abdc] |
| ChatGPT top-cited pages updated in 2025 | 89.7%; 76% refreshed in the last 30 days | — | Ahrefs study | [9edf8483abdc] |
| ChatGPT-cited pages that are listicles | 43.8% | — | Ahrefs study | [9edf8483abdc] [23ce7debe703] |
| AI Overviews appear on keywords | ~21% overall; ~58% of question queries; 46% of 7+-word queries; 99.9% of AI-Overview-triggering keywords are informational | — | Ahrefs data | [caec8fa7e6e5] |
| Websites blocking GPTBot | ~5.9% of 140 million sites checked | — | Ahrefs data `[web check]` | transcript only |
| AI-driven 404 rate vs. Google | AI sends visitors to 404s ~2.87x more often than Google; ChatGPT ~1% of clicked URLs lead to a 404 | — | Ahrefs data | [64a695c65c71] |
| AI referral share of total site traffic | ~0.25% average; Google sends ~210x more traffic than top AI platforms combined | — | Ahrefs data | [791c035b0f54] |
| Ahrefs AI-visitor conversion rate | 23x organic search rate | Single-company example | Ahrefs example | [791c035b0f54] |
| Vercel AI conversion rate | ~10% | Third-party example | Relayed by source `[web check]` | [791c035b0f54] |
| Tally AI impact | Largest acquisition channel; credited with +$1M ARR | Third-party example | Relayed by source `[web check]` | [791c035b0f54] |
| ChatGPT growth | +85% since January; source says it now sends more traffic than Reddit or LinkedIn | — | Ahrefs data `[web check]` | [791c035b0f54] |
| Misinformation resistance | Gemini/Perplexity repeated fake info in 37-39% of answers; ChatGPT under 7%, cited official FAQ 84% of the time | One planted-fake-brand test, 8 platforms, 3 contradicting sources | Ahrefs experiment | [748700e7c99c] |
| Ahrefs self-reported AI conversions | ~3% of conversions | Self-reported survey data, single company | Ahrefs example | [990877b3d70c] |
| AI-Overview citation churn | Over 45% of citations change on refresh | Refresh cadence roughly every 2 days | Ahrefs data | [35cbd98861df] |

## 5. Diagnostics and checks

| Check | How | Good | Bad | Next step | Card |
|---|---|---|---|---|---|
| Robots.txt AI-bot access | Visit /robots.txt; look for Disallow on GPTBot/OAI-SearchBot/ClaudeBot/Google-Extended `[verify UI]` | No disallow on target bots | Disallow present, often via a Cloudflare default | Remove/adjust the rule; recheck after any CDN or theme change | [bc44a7efd9f2] [75ea98447324] |
| JS rendering for AI crawlers | Disable JS in a browser and revisit your own page; compare raw vs. rendered HTML | Key content present in raw HTML | Page loads as an empty shell without JS | Add server-side rendering or pre-rendering | [d9728871b1a5] |
| Page speed for retrieval | Core Web Vitals audit | Fast load, clean HTML | Slow load | Apply standard SEO speed fixes; recheck AI bot fetch success | [d9728871b1a5] |
| Section self-containment (atomicity) | Read each H2 in isolation, out of page context | Makes complete sense alone | Depends on earlier paragraphs | Rewrite the section to stand alone | [08fd8b80c5a7] [a4891c6c3426] |
| Keyword AI-satisfaction | Search the keyword, read the AI overview as a shopper would | Overview leaves a reason to click (price, options, detail) | Overview fully answers the query | Drop as a click target; redirect to an AEO mention play or a tool/transactional query | [f51f401ddf5f] |
| Sleeper-page candidacy | Sort a top-pages report by traffic decline `[verify UI]` | Decent backlinks plus a clear decline | Decline but few backlinks to begin with | If links are thin, a content rewrite likely will not help — investigate other causes first | [4e6f7e7f1aa7] |
| AI-hallucinated 404s | Filter analytics for AI-referrer sessions landing on a 404 | No such sessions | Consistent AI-referred 404 traffic | Redirect the hallucinated URL to the closest real page | [64a695c65c71] |
| Brand mention trend | Mention-volume-over-time view `[verify UI]` | Stable or growing | Sudden drop | Investigate which page/source stopped mentioning you; consider re-outreach | [445fa90e4caf] |
| Brand mention accuracy/sentiment | Read AI responses that name your brand | Accurate and positive | Inaccurate, negative, or off-positioning | Publish the correct, specific content on your own site first, then request a publisher correction | [445fa90e4caf] [748700e7c99c] |
| AI share of voice trend | Monthly check vs. named competitors `[verify UI]` | Growing relative share | Flat while a competitor grows | Investigate which topics/pages the competitor is winning | [0d40ada60dfc] |
| Cited-domains trend | Monthly check for newly-citing domains `[verify UI]` | New domains appear | No new domains despite outreach | Revisit tier-1/tier-2 mention targets | [0d40ada60dfc] |
| Topic coverage | Compare current AI-topic associations to the last gap analysis | Prior gaps closed; new topics appearing | Gaps unchanged | Return to the content-creation procedure for that topic | [0d40ada60dfc] [7ccc34f2e89e] |
| AI bot visit pattern | Server logs or a bot-analytics tool `[verify UI]` | Repeated citation-bot visits to important pages | No bot visits to important pages | Check internal linking, access rules and log coverage before concluding there is a crawl problem | [8f0d6e616976] |

## 6. Tools, settings and named features

- **Ahrefs Brand Radar** `[verify UI]`: AI-visibility tracker. Reports used: AI responses (shows fan-out queries for ChatGPT/Perplexity prompts), cited domains, topics (filterable to a specific domain, e.g. youtube.com), and the mentions/citations/impressions/AI-share-of-voice dashboard, plus an "others only" competitor filter.
- **Ahrefs Site Explorer** `[verify UI]`: baseline SEO metrics (domain rating, referring domains, organic keywords/traffic/value); top-pages report sorted by traffic change (sleeper-page finding); organic-keywords report run against reddit.com and against www.youtube.com/watch to find already-ranking UGC threads and videos.
- **Ahrefs Keywords Explorer** `[verify UI]`: matching-terms report with include/exclude filters for seed-plus-modifier keyword research; an intent filter for transactional queries.
- **Ahrefs Content Explorer** `[verify UI]`: title:best / title:versus search operators combined with a minus-operator on your own brand name, to surface listicles/comparisons missing your brand.
- **Ahrefs Site Audit** `[verify UI]`: crawls a site and flags robots.txt rules that block AI crawlers.
- **Ahrefs Web Analytics** `[web check: current pricing/tier]` `[verify UI]`: alternative to GA4 with a built-in AI-search channel; separates "unknown" traffic from "direct," which GA4 does not.
- **Ahrefs Bot Analytics** `[web check: current pricing/tier]` `[verify UI]`: Cloudflare-integrated AI-bot tracker; the source says it works on Cloudflare's free plan.
- **GA4**: Admin > Data Display > Channel Groups `[verify UI]` for a custom "AI traffic" regex channel; Reports > Acquisition > Traffic Acquisition to view it.
- **Named AI crawlers**: GPTBot and OAI-SearchBot (OpenAI, training vs. search/citation respectively), ClaudeBot (Anthropic), Google-Extended (Google, training signal). `[web check: current crawler names and behavior — these change]`
- **Cloudflare**: "instruct AI bot traffic" robots.txt feature, on by default at recording time; auto-updates a site's robots.txt to signal against AI training use. `[verify UI] [web check: current default]`
- **llms.txt**: a proposed standard file at /llms.txt describing a site for AI systems; not confirmed as read by any major provider at recording time. `[web check: current adoption]`
- **AI platforms discussed**: Google AI Overviews, Google AI Mode, ChatGPT, Perplexity, Gemini, Copilot, Claude, DeepSeek, Grok — each with different citation behavior and referral-passing behavior. `[web check: all of the above change fast]`
- **A generic AI assistant** (e.g. ChatGPT): used to generate seed keywords/modifiers from a business description, and to turn a keyword list into natural-language questions.

## 7. Examples and case results

All are the presenter's/Ahrefs' own examples or relayed anecdotes; none is a promise.
- Ahrefs' own site: 7,470 organic AI mentions across 2,309 pages with no deliberate optimization, credited to existing SEO and content quality. (transcript)
- Ahrefs, June 2025: AI search was 0.5% of its traffic but drove 12.1% of sign-ups — a 23x higher conversion rate than organic search. [791c035b0f54]
- ChatGPT's deep-research mode ran 420 searches for a single query about buying a red phone case. [a227df367635]
- Fake-luxury-brand misinformation test: 3 contradicting sources planted across a blog, Reddit, and Medium, then queried across 8 AI platforms. Gemini and Perplexity repeated the fake founders/cities/pricing in 37-39% of answers; ChatGPT stayed under 7% and cited the brand's official FAQ 84% of the time. [748700e7c99c]
- Vercel: reported ~10% conversion rate from AI traffic (third-party example relayed by the source). [791c035b0f54] `[web check]`
- Tally: reported AI as its largest acquisition channel, credited with boosting ARR by $1 million (third-party example relayed by the source). [791c035b0f54] `[web check]`
- Ahrefs self-reported attribution: ~3% of conversions attributed to AI via post-purchase survey, with AI-attributed visitors converting at a much higher rate than organic-search visitors. [990877b3d70c]
- ChatGPT cited as growing 85% since January and, per the source, now sending more traffic than Reddit or LinkedIn. [791c035b0f54] `[web check]`

## 8. Mistakes the source warns about

- Writing a special "AI-optimized" format instead of writing well for humans — the source says there is no such separate format. [08fd8b80c5a7]
- Padding word count in hopes of earning a citation. [9edf8483abdc]
- "Refreshing" a page by only changing its publish date instead of making substantive content changes. [9edf8483abdc] [4e6f7e7f1aa7]
- Rewriting a page whose real problem is missing backlinks, not staleness. [4e6f7e7f1aa7]
- Spamming Reddit or forums with brand mentions instead of contributing genuinely — the source says this backfires fast. [7285d50f35a8] [3347a4baaad4]
- Leaving an original framework or concept unbranded, so AI flattens it into unattributed general knowledge. [2fcdce4950af]
- Assuming Google AI Mode mirrors Google AI Overviews just because both are Google products (only 13.7% citation overlap reported). [e8d6d277ebfb]
- Optimizing for one AI platform and assuming visibility transfers to the others (only 14% domain overlap across the top three). [e8d6d277ebfb]
- Ignoring the AI filter and chasing organic clicks on a keyword an AI overview already fully answers. [f51f401ddf5f]
- Building a keyword list out of fan-out sub-queries — the source says they are synthetic, inconsistent, and over 95% zero-volume. [a227df367635]
- Chasing a fixed "rank" for AI answers instead of tracking a probability/share-of-visibility metric. [f85af788af43]
- Over-investing in schema markup specifically for AEO, when the source says there is no confirmed evidence it improves AI citation. [ccbc5be4692f]
- Leaving AI-hallucinated URLs as dead-end 404s instead of redirecting them. [64a695c65c71]
- Not checking Cloudflare's default AI-bot-blocking setting, unknowingly cutting off AI crawlers. [bc44a7efd9f2] [75ea98447324]
- Relying on referral traffic alone to judge AI's impact, when several platforms strip referrer data and the visit shows up as "direct." [c2ae662a8e4f] [e3fe0904f52d]
- Skipping the "how did you hear about us" survey question, missing zero-click AI-driven brand awareness entirely. [3d817167591c] [990877b3d70c]
- Leaving your own brand's information gaps unfilled, letting AI default to specific (possibly false) third-party claims over an absent or vague official answer. [748700e7c99c]
- Trying to fix every gap-analysis finding at once instead of sequencing quick wins first. [7ccc34f2e89e]

## 9. Caveats, conflicts and what is missing

**Vendor content:** this is an Ahrefs-produced course and nearly every workflow routes through a paid Ahrefs product (Brand Radar, Site Explorer, Keywords Explorer, Content Explorer, Site Audit, Web Analytics, Bot Analytics). The headline statistics (75,000 brands; 174,000+ pages; 140 million websites) are Ahrefs' own studies, cited without links, dates, or methodology in the transcript. Treat every specific percentage as one vendor's snapshot, not an audited industry standard. `[web check: are these studies published anywhere with methodology?]`

**Near-duplicate cards:** [75ea98447324] ("Check CDN and robots rules...") and [bc44a7efd9f2] ("Audit search crawler access independently...") carry nearly identical text and appear to be duplicate extractions of the same passage — treat as one procedure, not two independent findings.

**Self-flagged internal revision:** the 76%-of-AI-Overview-citations-from-Google's-top-10 figure is stated, then immediately revised down to "closer to 38%... a more recent study" within the same lesson, with no date given for either number. Use the direction (weakening link between Google rank and AI citation) more than either specific figure. [e8d6d277ebfb]

**Fast-decaying platform claims, all flagged `[web check]`:**
- GPT-4 specifically (not a newer model) is named as the one trained on "over a million hours of YouTube transcripts" — verify what current frontier models' training data includes before repeating this.
- "ChatGPT's crawler cannot render JavaScript; Gemini and Copilot can" is asserted without citation and is exactly the kind of platform capability that changes without notice.
- llms.txt adoption status is explicitly time-boxed by the presenter ("right now") — re-check before recommending for or against building one.
- Referral-passing behavior per platform (Perplexity desktop vs. app, Copilot web vs. Windows, Grok not passing referral data at all, ChatGPT's no-referrer links on paid accounts) is a fast-changing technical detail tied only to the recording date.
- Named AI bots (GPTBot, OAI-SearchBot, ClaudeBot, Google-Extended) and Cloudflare's default AI-bot-blocking setting should both be reverified against current documentation.

**Numbers with no dedicated card** (transcript only — verify independently before quoting as current): the 58% AI-Overview CTR drop on the #1 result, ChatGPT's 900-million-weekly-user figure, Ahrefs' own 7,470-mentions/2,309-pages example, the 0.737 YouTube-to-ChatGPT-visibility correlation, the "~5.9% of 140 million sites block GPTBot" figure, and ChatGPT's "+85% since January" growth claim.

**Third-party anecdotes without methodology:** Vercel's ~10% AI-traffic conversion rate and Tally's "largest acquisition channel, +$1M ARR" claim are relayed by Ahrefs without a link or method — treat as marketing anecdotes, not case studies. `[web check]`

**What is thin or missing:**
- No treatment of paid placements inside AI answers — the source notes there is no ad product for chat questions yet and expects that to change, which would also change the "no volume truth set" problem in keyword/prompt research.
- No international or non-English AEO guidance.
- No quantitative scoring for the "AI filter" or "quick win" prioritization calls — both are explicit judgment calls in the source.
- The tier-2 (UGC) mention card itself notes the source "cuts off before detailing the full tier-two method," so that section is thinner than tiers 1 and 3. [7285d50f35a8]
- No disclosure/compliance guidance for paid or affiliated community commenters beyond "don't spam."
- The course is written for general websites/SaaS/publishers; it never uses a product-detail-page example itself. All ecommerce-specific framing in this playbook and its source cards (PDP long-tail Q&A, category-page topic coverage, buying-guide comparisons) is an application layer added by the card author, not something the source itself stated for ecommerce.
- `[needs brand data: branded entity list (sub-brands, product names, proprietary features/metrics, personal brands), current DR/referring-domains/organic-traffic baseline, current AI mention/citation/impression/share-of-voice numbers per platform, competitor domain list for the gap analysis, per-page backlink counts for sleeper-page triage, current robots.txt contents and CDN/Cloudflare AI-bot settings, current GA4 channel-group configuration, existing post-purchase survey platform and questions, YouTube channel history and top videos, target category keywords and modifiers]`

**Conflict with common ecommerce advice:** the source is broadly compatible with mainstream SEO/content practice (it frames AEO as additive to SEO, not a replacement), but two points cut against habits common in ecommerce content teams:
- "Content length does not predict citation" (0.04 correlation; 53.4% of cited pages under 1,000 words) runs against the common ecommerce habit of writing long buying guides purely for perceived topical authority. Reconcile by keeping guides comprehensive in topic *coverage* (per the query fan-out rule) without padding word count for its own sake.
- "Don't over-invest in schema for AEO" sits next to, but does not contradict, standard ecommerce SEO advice to maximize Product/Offer/Review schema for rich results — the source's point is narrower (no confirmed AEO-specific benefit), so schema should still be kept for its separately-proven SEO/rich-result value, just not expanded in the name of AEO alone.

## 10. Card index
- [caec8fa7e6e5] Keyword vetting with the BID formula
- [f51f401ddf5f] AI filter: avoid keywords AI already fully answers
- [35cbd98861df] Find competitor mention gaps with branded-query filters
- [08fd8b80c5a7] Content structure: BLUF, atomic sections, entities, declarative sentences
- [9edf8483abdc] Content length, freshness and format signals for AI citations
- [4e6f7e7f1aa7] Refresh sleeper pages to win citations fastest
- [2fcdce4950af] Brand the frameworks you invent to resist LLM flattening
- [23ce7debe703] Tier-one mentions: get listed on editorial listicles and comparison pages
- [7285d50f35a8] Tier-two mentions on community and UGC platforms, without spamming
- [a227df367635] Query fan-out and why topical coverage beats single-keyword pages
- [f85af788af43] AI visibility is probabilistic, not a ranking position
- [d477a2718a07] Two information sources: training data vs real-time retrieval
- [75ea98447324] Check CDN and robots rules for accidental search-crawler blocking
- [3d817167591c] Capture AI-driven demand with a post-purchase 'how did you hear about us?' survey
- [7ccc34f2e89e] Diagnose visibility gaps across six dimensions
- [e8d6d277ebfb] Platform-specific citation preferences: where to allocate AEO effort
- [dc9263a72730] Treat AI visibility as a spectrum: cited, mentioned, or invisible
- [2037fd15a632] Mining listicles and comparisons where your brand is absent
- [3347a4baaad4] Earning mentions in community and UGC platforms
- [de260c9bccd9] Using owned content properties as additional AI citation sources
- [445fa90e4caf] Running a regular brand mention audit
- [926976b809be] Targeting search-hit YouTube topics instead of viral hits
- [224d5f463421] YouTube video ranking checklist for product discovery
- [1af9f13ebe90] Finding YouTube topics AI is already citing for your niche
- [bc44a7efd9f2] Audit search crawler access independently from training permissions
- [d9728871b1a5] Handling JavaScript rendering and page speed for AI crawlers
- [a4891c6c3426] Structuring HTML for AI parsability
- [ccbc5be4692f] Using and limiting schema markup for AEO
- [64a695c65c71] Capturing traffic from AI-hallucinated 404 URLs
- [c2ae662a8e4f] Setting up an AI traffic channel group in GA4
- [8f0d6e616976] Tracking AI bot activity to identify citation candidates
- [990877b3d70c] Capturing AI impact through self-reported attribution
- [e3fe0904f52d] Combining three tracking pillars for AI visibility
- [791c035b0f54] Prioritizing and evaluating AI traffic volume vs. quality
- [748700e7c99c] Filling information gaps to resist AI misinformation
- [0d40ada60dfc] Completing a monthly and quarterly brand radar check
- [bef60df0b856] Executing a starter AEO action plan this week
