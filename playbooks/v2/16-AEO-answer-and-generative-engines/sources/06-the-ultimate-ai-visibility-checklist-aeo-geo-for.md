# The Ultimate AI Visibility Checklist (AEO/GEO for ecommerce)

source_id: 1qLXwcwAMSA8vD1-WZKnN-CIyVODkJvWY  |  folder: /16-AEO-answer-and-generative-engines  |  cards: 20  |  words: 7,065  |  type: transcript (1 YouTube video, auto-captioned, no timestamps)

credibility: One unnamed presenter. He is building a paid tool called Focal (waitlist, "AI agents that will automatically do the things listed in this video") and runs a free/paid community called Futureproof ("AI visibility community... share our best practices and blueprints"). So the video is also a funnel for both. Evidence offered: 1 recurring anecdotal example, a "self storage software" business the presenter says he has ranked in AI search; no other named businesses, no controlled tests, no before/after visibility numbers with a stated measurement method. Several headline statistics ("4 to 10 times more likely to convert," "44% of AI citations... first onethird," "sample sizes of just 10 documents can poison LLMs") are stated as fact with no source, study name, or link given in the transcript `[web check: origin and current validity of each cited statistic]`. The presenter openly frames section 7 as "gray hat" and admits "some businesses may say this is unethical," which he leaves to the viewer.

date signals: No explicit year in the transcript (the file title says 2026). Named AI search engines: ChatGPT, Gemini, Perplexity, Google AI Overviews, Google AI mode. Named crawlers: GPTBot, PerplexityBot, an unnamed "AI overview search bot." Claims Microsoft owns "around 50%" of ChatGPT and that ChatGPT pulls from Bing. Tools named: an unnamed free robots.txt/bot checker, an unnamed free JavaScript-rendering checker, an unnamed schema generator site, Hunter (Chrome extension), Keywords Everywhere, Answer Socrates, F5Bot, Newswire, Gemini (used live in the video), Google Business Profile, Google Search Console, Bing Webmaster Tools. AI answer engines, their crawlers, their ranking signals and their market share change fast; every tool, bot name and platform step below should be re-checked before use `[web check: current AI crawler names, current free AEO tools, current AI search engine market share]`.

## 1. What this source is for

It gives an operator a 7-part checklist to increase "AI visibility," defined by the presenter as ranking and getting recommended by AI search engines (ChatGPT, Gemini, Perplexity, Google AI Overviews/AI mode) so target customers find and buy from the business. The 7 parts: (1) technical foundations (crawler access, indexing, an about/facts page), (2) structured data (schema), (3) content strategy (front-loaded answers, FAQs, comparison tables, hard data, freshness), (4) authority and brand signals (digital presence, NAP consistency, listicles, AI-elicited buying criteria, third-party mentions, reviews), (5) Reddit, LinkedIn and communities, (6) YouTube and video, and (7) gray-hat tactics (source poisoning, self-published listicles, industry-report press releases). It closes with a one-week quick-win sequence. It does not teach how to measure AI visibility itself or how to write the content beyond structural rules `[needs brand data: which AI engines the brand's actual customers use before prioritizing effort across ChatGPT, Gemini, Perplexity and Google AI mode]`.

## 2. Principles

1. **AI visibility is a distinct, high-intent traffic source.** Condition: any ecommerce brand not yet tracking it. Definition: ranking and getting recommended in AI search engines. The presenter's claim: AI-search traffic converts 4 to 10 times more than Google traffic because AI answers are personalized to a detailed prompt, so people who click through are already qualified. No study is cited. [64120ce92436] `[web check: any published data on AI-search traffic conversion rates]`
2. **Crawler access is a precondition, not a ranking factor.** Condition: before any other AEO work. If GPTBot, PerplexityBot, or Google's AI bots cannot reach the site, none of the content or authority work below matters, because the site is invisible to them. [ac1b7d780e6a]
3. **Traditional indexing gates AI visibility.** Condition: always, because the presenter says ChatGPT and similar engines lean on Google and Bing for fresh information. An unindexed page cannot be recommended in AI answers even if it is well written. [48ec50971ecd]
4. **AI has no first-hand experience, so it looks for consensus.** Condition: applies to every authority tactic in sections 4 to 7. Reviews, third-party mentions, directory listings and Reddit sentiment all function as substitutes for the personal experience an AI model does not have. [2250abe5f1eb] [77505b864e04] [4e8ff5bc6f43]
5. **Most AI citations come from the top of the page.** Condition: any page you want cited. The presenter's stated figure is over 44% of AI citations come from the first third of a page, so the direct answer and TL;DR must sit above the fold. [10e99e650616]
6. **Content must be citable, not just present.** Condition: any page competing for an AI citation. Hard numbers, named-expert quotes and original data make a page a better citation source than vague marketing language; AI models look for unique data they cannot get elsewhere. [c8d59fd79d48]
7. **Stale content loses to fresh competitors.** Condition: any evergreen page. Revisit every couple of months; freshness is a ranking factor for AI and traditional search alike. [984dbd1fc95a]
8. **Consistency across every listed source matters as much as any one source.** Condition: any business with directory, review or schema listings. Inconsistent name, address, phone or facts across sources causes AI to state wrong information and lowers recommendation odds. [f91363a42603]
9. **Listicles are a primary AI source, so placement in them is worth pursuing directly, including paying for it.** Condition: category queries that surface "best X" content. The presenter treats paid placement as a normal cost of AEO. [61e62cdd75c6]
10. **AI engines will tell you their own criteria if you ask.** Condition: any category. Prompting an AI engine with "what do you look for when recommending [category]" returns criteria to treat as hypotheses to test against, not as verified ranking factors. [81e3b397ce06]
11. **You can audit what AI already believes about your brand by asking it directly.** Condition: diagnosing wrong or missing AI answers about your brand. Ask an AI engine to search the internet and report what it knows about you, then open its cited sources and fix or contest each one. [dcb1c3495233]
12. **Video transcripts are a durable, separately indexable citation surface.** Condition: any brand willing to produce video. YouTube video transcripts are read and cited by AI engines independently of the video itself ranking. [5f0da09a8820] [2250abe5f1eb]
13. **Small sample sizes can shift what LLMs say.** Condition: gray-hat tactics only. The presenter cites unnamed studies claiming as few as 10 documents can "poison" an LLM's output on a topic, which is his stated basis for self-publishing listicles on trusted platforms. [5c9bc91bc0b2] `[web check: the actual studies referenced, their scope and current relevance]`

## 3. Procedures

### 3.1 Check AI crawler access `[verify UI]` `[web check: current tool]`

1. Open the presenter's linked free bot-validation tool (unnamed in the transcript, described as the "first link in the description") and enter your website URL. [ac1b7d780e6a]
2. Confirm the site passes for each bot the tool checks: GPTBot (ChatGPT), PerplexityBot, and an unnamed "AI overview search bot." Card adds the distinction that OAI-SearchBot governs ChatGPT search access while GPTBot separately governs training permission, so do not blanket-allow or blanket-block all bots together. [ac1b7d780e6a]
3. If any bot fails, inspect your robots.txt file and any CDN or firewall rules for that bot's user agent; unblock the search/answer bots you want while preserving any deliberate training opt-outs and protected checkout/account paths. [ac1b7d780e6a]
4. Separately test JavaScript rendering with a second free tool (also unnamed, "this free tool") by entering the URL; it shows what text is visible when JavaScript does not load. [ac1b7d780e6a]
5. Check that title, meta description, headings and the bulk of body copy appear in the non-JavaScript render. If they do not, that content is invisible to AI bots that do not execute JavaScript. Card frames this as comparing initial HTML to the fully rendered page. [ac1b7d780e6a]
6. Re-test after any CDN, theme, or platform migration, since these can silently reintroduce blocking. [ac1b7d780e6a]
7. Note: a spoofed user-agent test is not proof of real crawler access; verify with actual crawler logs where available. [ac1b7d780e6a]

### 3.2 Submit sitemaps and confirm indexing `[verify UI]`

1. Go to Google Search Console > Indexing > Sitemaps. [48ec50971ecd]
2. Enter your sitemap URL, typically `yoursite.com/sitemap.xml`, and press submit. The presenter's own example picked up 94 pages with a "successful" status. [48ec50971ecd]
3. Repeat the same submission in Bing Webmaster Tools. The presenter says this matters disproportionately because ChatGPT draws on Bing. [48ec50971ecd]
4. Spot-check indexation by typing `site:yourdomain.com` into Google search and reviewing which product, category and content pages actually appear. [48ec50971ecd]
5. Re-check whenever new product or collection pages fail to appear in AI answers, since an unindexed SKU page cannot be surfaced. [48ec50971ecd]

### 3.3 Publish or fix an About/Facts page

1. Add an About Us or Facts page if the store does not have one. [b2f279ddb882]
2. In plain factual language, list what you sell, your key differentiators, how long the business has operated, and any relevant credentials. [b2f279ddb882]
3. Keep every fact on this page identical to what appears in directories, review platforms and schema markup, since conflicting claims confuse AI's understanding of the brand. [b2f279ddb882] [f91363a42603]
4. Update the page whenever the business changes (new categories, certifications, milestones). [b2f279ddb882]
5. Treat this page as the canonical source you will later point schema and directory listings toward. [b2f279ddb882]

### 3.4 Add structured data (schema) `[verify UI]` `[web check: current schema generator]`

1. Go to a schema generator website (unnamed in the transcript). [618db29e2091]
2. Select Organization schema for the homepage. Fill in founding date, description, and links to social profiles. [618db29e2091]
3. Copy the generated code and add it to the relevant page. [618db29e2091]
4. Apply the source's other recommended schema types to their matching page types (for example, product-related schema on product pages) rather than one schema block on one template; the exact list of other types sits in the presenter's separate checklist, not in this transcript. [618db29e2091]
5. Link your YouTube channel and social profiles from the site and include them in schema markup alongside other brand data. [618db29e2091] [5f0da09a8820]
6. Validate the markup after deployment so errors do not silently defeat the purpose. [618db29e2091]

### 3.5 Front-load pages with a direct answer and TL;DR

1. Open every important page (product, category, buying guide, comparison, landing page) with a direct 2 to 4 sentence answer to the core question, not a marketing build-up. [10e99e650616]
2. Follow immediately with a TL;DR block. [10e99e650616]
3. Move the key facts (materials, sizing, use case, who it's for) above the fold and above decorative sections, since the presenter states over 44% of AI citations come from the first third of the page. [10e99e650616]
4. Write in natural language, not keyword-stuffed phrasing, because AI engines parse and prefer natural-language queries and answers. [10e99e650616]
5. Keep updating the top section as facts change. [10e99e650616]

### 3.6 Build FAQs from "People Also Asked"

1. Search your topic on Google (presenter's example: "self storage software") and scroll to the "People Also Asked" box. [ddeff4f4d862]
2. Copy those exact questions and draft clear answers. [ddeff4f4d862]
3. Add the Q&A as an FAQ section at the bottom of every important page. [ddeff4f4d862]
4. Repeat per page type so category pages, product pages and guides each answer their own question cluster. [ddeff4f4d862]
5. Refresh FAQs periodically to reflect current pricing, specs and policy. [ddeff4f4d862]

### 3.7 Build comparison content

1. Pick 3 to 4 competitors bigger than you. [8c2682d22767]
2. Write head-to-head pages: you versus competitor A, B, C, D. [8c2682d22767]
3. Break down pros and cons of each honestly; explain why your product is better for the relevant buyer. Logic given: AI already knows the big players, so the comparison supplies AI's reasoning to recommend you instead. [8c2682d22767]
4. Put a comparison table near the top of the article, since tables are an easy structure for AI to lift directly into an answer. [8c2682d22767]
5. Extend the table format to your own category and product pages where buyers compare alternatives. [8c2682d22767]
6. Keep pricing, features and specs accurate; inaccurate comparison claims undercut credibility with buyers and AI alike. [8c2682d22767]

### 3.8 Upgrade content quality with hard numbers, quotes and original data

1. Audit copy for vague claims ("many users prefer") and replace with hard numbers and percentages wherever you have real evidence. [c8d59fd79d48]
2. Add direct quotes from named team members with a credible public presence (for example a strong LinkedIn profile). [c8d59fd79d48]
3. Include at least 1 piece of original data per important page (a survey, internal benchmark, or industry finding) that AI cannot get elsewhere. [c8d59fd79d48]
4. Consider an industry report or data roundup with original sourcing to position the brand as category leader. [c8d59fd79d48]
5. Apply the same rigor to glossary pages and statistics roundups, which the presenter names as citation-worthy content types. [c8d59fd79d48]
6. Only publish real, verifiable figures and quotes. [c8d59fd79d48]

### 3.9 Refresh content on a cadence

1. Revisit every important article every couple of months: add new statistics, update wording, reference recent case studies. [984dbd1fc95a]
2. Add a clearly visible "last updated" date to every article. [984dbd1fc95a]
3. Prioritize top-performing and high-commercial-intent pages first when time is limited (category pages, comparison pages, top buying guides). [984dbd1fc95a]
4. The presenter separately claims that updating only the visible date, with no content change, "will actually boost your ranking," and tells viewers to do it "really slightly so your competitors don't notice." Treat this as his own admitted manipulation tactic, not a content-quality practice. [984dbd1fc95a]

### 3.10 Fix digital presence and NAP consistency

1. Complete your Google Business Profile with accurate details: what you sell, USPs, years in operation. [f91363a42603]
2. Create and claim listings in relevant business directories and review platforms. The presenter names Yelp, Trustpilot, Crunchbase, and unspecified "industry platforms." [f91363a42603]
3. Make your business name, address and phone number character-for-character identical everywhere. [f91363a42603]
4. Encourage reviews on the most relevant platforms for your category and respond to them. [f91363a42603]
5. Align every listing description with the AI-elicited buying-criteria checklist (procedure 3.12). [f91363a42603]
6. Re-audit listings after any rebrand, move, or new location. [f91363a42603]

### 3.11 Get into "best of" listicles `[web check: current Hunter extension and terms]`

1. Search your category term (for example "best self storage software") in AI Overviews and AI mode and note which sources are cited; the presenter's example showed listicles dominating. [61e62cdd75c6]
2. Click into the listicle, identify who maintains it, and use the Hunter Chrome extension to find contact details for people at that site or business. [61e62cdd75c6]
3. Email and message on LinkedIn with a specific, credible case for inclusion, ideally near the top of the list. [61e62cdd75c6]
4. Expect some listings to require payment; the presenter treats this as often worth it because listicles are a primary AI source. [61e62cdd75c6]
5. Track every target site in a spreadsheet and work through it systematically. [61e62cdd75c6]
6. Consider hiring a YouTube creator to produce a "best of" video for your industry; video transcripts are also cited by AI. [61e62cdd75c6] [64120ce92436]

### 3.12 Elicit and apply AI's own buying criteria

1. Open an AI engine (the presenter demonstrates Gemini) and ask: "What do you look for when recommending [your product or service category]?" [81e3b397ce06]
2. Treat the returned list as a hypothesis about what matters, not as the engine's actual ranking algorithm. [81e3b397ce06]
3. Compare the criteria against verified product facts and real customer questions; add only accurate, relevant details to product copy and editable listings. Do not invent certifications or claims to satisfy the checklist. [81e3b397ce06]
4. Repeat the prompt across multiple AI engines and merge the results into one master checklist. [81e3b397ce06]
5. Use that master checklist as the input to procedure 3.13. [81e3b397ce06]

### 3.13 Run an AI brand audit and correct its sources

1. Prompt an AI engine: "Search the internet and tell me what you know about [brand]." Read the answer as a prospective buyer would. [dcb1c3495233]
2. Open every cited source under the answer; these are the pages shaping the AI's view of the business. [dcb1c3495233]
3. For sources you control, edit the description to include the criteria from procedure 3.12. For sources you do not control, use a contact-finding tool (for example Hunter) to reach the site owner and request a correction. [dcb1c3495233]
4. Run the identical prompt for each main competitor ("Search the internet and tell me what you know about competitor A/B/C/D") to see which sources drive their recommendations. [dcb1c3495233]
5. Pursue mentions, or better, listicle placement, on those same competitor-driving sources. [dcb1c3495233]
6. Repeat this audit periodically since AI answers and their sources shift over time. [dcb1c3495233]

### 3.14 Build third-party mentions, podcasts and video

1. Secure mentions in at least 3 industry publications via guest posts, interviews or PR, prioritizing outlets AI already cites in your category. [2250abe5f1eb]
2. Approach industry accreditation bodies and associations for sponsorship, contributed articles or partner listings; paying may be necessary. [2250abe5f1eb]
3. Pitch industry podcasts, since transcripts are frequently indexed and cited by AI engines. [2250abe5f1eb]
4. Work with influencers on YouTube videos about the brand. [2250abe5f1eb]
5. Structure any long-form external content (including LinkedIn) like your own site content: value in the first 2 to 4 sentences, a TL;DR, tables and bullets. [2250abe5f1eb]
6. Track target publications and appearances in a spreadsheet. [2250abe5f1eb]

### 3.15 Collect reviews `[web check: current platform incentive policies]`

1. Choose review destinations your shoppers actually use and that appear as sources in your category's AI answers. [77505b864e04]
2. Send a neutral post-purchase request about actual use, fit, quality and limitations; let customers use their own words. [77505b864e04]
3. Use a simple review link or QR code where appropriate to the purchase journey. [77505b864e04]
4. Do not script positive outcomes, fabricate numbers, or condition requests on satisfaction. [77505b864e04]
5. The presenter separately recommends a physical Google review card with a QR code and NFC tag, used at job completion, and incentivizing team members $10 to $20 per review collected. [f91363a42603] Card 77505b864e04 flags this as needing a platform-rules check before introducing any incentive, and card f91363a42603 explicitly notes Google prohibits incentivized reviews. This is a direct conflict inside the source's own cards, see section 9.
6. Monitor and respond to feedback; separate service fixes from any unproven AI-visibility effect. [77505b864e04]

### 3.16 Engage Reddit with F5Bot `[web check: current F5Bot availability and Reddit self-promotion rules]`

1. Identify 5 to 10 subreddits most relevant to your product category. [4e8ff5bc6f43]
2. Provide free value in existing threads first, building account karma before ever mentioning your brand, to reduce ban risk. [4e8ff5bc6f43]
3. Set up F5Bot alerts for your category's key keywords so you are notified whenever they are mentioned on Reddit. [4e8ff5bc6f43]
4. When relevant, recommend your product naturally inside a genuinely helpful answer rather than dropping a cold link. [4e8ff5bc6f43]
5. Expect a long runway: the presenter says the average Reddit post cited by AI is over a year old, so plan this as a 1 to 2 year compounding effort. [4e8ff5bc6f43]

### 3.17 Publish long-form LinkedIn articles

1. Write long-form articles, not short posts; the presenter says long-form LinkedIn articles are indexed by Google, making them eligible as AI sources. [6aaf743e7f1f]
2. Structure them like site content: value in the first 2 to 4 sentences, a TL;DR. [6aaf743e7f1f]
3. Add tables and bullet points for easy AI extraction. [6aaf743e7f1f]
4. Cover core category topics and include a natural product/service recommendation. [6aaf743e7f1f]
5. Keep facts consistent with your website and directory descriptions. [6aaf743e7f1f]
6. Publish on a schedule. [6aaf743e7f1f]

### 3.18 Build a YouTube presence for citation

1. Start a YouTube channel and publish an introductory video about the business, even at modest production value. [5f0da09a8820]
2. Pick a specific search term your target customers use across Google, YouTube and AI search engines. [5f0da09a8820]
3. Place that term in the video title, description, YouTube video filename, and thumbnail filename, and say it in the first and last 10 seconds of the video. [5f0da09a8820]
4. Prioritize information value over production polish. [5f0da09a8820]
5. Produce a companion blog post for every video, and a video for every blog post. [5f0da09a8820]
6. Link the YouTube channel from the website and include it in schema markup with social profiles. [5f0da09a8820] [618db29e2091]

### 3.19 Gray-hat: parasite SEO and source poisoning (presenter's own "gray hat" framing)

This entire procedure is presented by the source itself as ethically contested. See section 9 before using it.

1. **Self-published listicles.** Produce your own "best of" list that places you at the top and, ideally, omits competitors. Publish 5 to 10 of these on already-trusted platforms: Medium, Substack, LinkedIn, Quora, or any site you control. Basis given: unnamed studies claim as few as 10 documents can shift ("poison") what an LLM says on a topic. [5c9bc91bc0b2] `[web check: platform manipulation/spam policies for Medium, Substack, LinkedIn, Quora before doing this]`
2. **Target competitor-driving sources.** Ask AI "search the internet and tell me what you know about competitor A/B/C/D," identify the sources that drive their recommendations, and get those same sources to mention you, ideally in a listicle that excludes the competitor and puts you at the top. [dcb1c3495233] [5c9bc91bc0b2]
3. **Industry-report press release.** Title a release as an industry report (for example "Self Storage Industry Report: Top Leaders Ranked") instead of a plain "Top 10" article. Distribute via a press wire such as Newswire; the presenter says submissions cost "a couple hundred dollars" and calls this likely the highest-ROI activity in the checklist. [5c9bc91bc0b2] Card 5c9bc91bc0b2 adds the guardrail the video does not: describe only research actually performed, disclose method, sample, dates and sponsorship, and do not relabel a promotional ranking as independent research.

### 3.20 One-week quick-win sequence

The presenter's own prioritized starter list, in this order: [64120ce92436]
1. Check robots.txt with the free bot-access checker (3.1).
2. Register the site in Bing Webmaster Tools and Google Search Console; submit the sitemap (3.2).
3. Hire a YouTube creator to produce a best-providers list video for your industry and publish it.
4. Add Organization schema linking to LinkedIn, Crunchbase and other reputable brand mentions, including social profiles (3.4).
5. Rewrite business descriptions across all directories and review platforms using the AI-elicited criteria checklist (3.12).
6. Update your top 3 blog posts to add a TL;DR at the top and an FAQ section at the bottom (3.5, 3.6).
7. Ask AI what it knows about you, correct the cited sources, and create/refresh citations and review-platform entries (3.13).
8. Publish 1 long-form LinkedIn article recommending your product on a core category topic (3.17), and start outreach for "best X" placements via Hunter and LinkedIn (3.11).

## 4. Rules, thresholds and numbers

| Rule | Number or threshold | Condition | Source's basis | Card id |
|---|---|---|---|---|
| AI-search traffic converts better than Google traffic | 4 to 10 times more likely to convert | AI search traffic generally | Presenter's stated claim, no study named | 64120ce92436 |
| Share of AI citations from top of page | over 44% | Any page you want AI to cite | Presenter's cited statistic | 10e99e650616 |
| Competitors to compare against in head-to-head pages | 3 to 4, chosen bigger than you | Comparison content strategy | Presenter's rule | 8c2682d22767 |
| Industry publications for third-party mentions | at least 3 | Building authority signals | Presenter's rule | 2250abe5f1eb |
| Review incentive per review | $10 to $20 per team member | In-person service businesses collecting reviews | Presenter's recommendation; conflicts with platform rules, see section 9 | f91363a42603 |
| Subreddits to target | 5 to 10 | Reddit engagement strategy | Presenter's rule | 4e8ff5bc6f43 |
| Age of average AI-cited Reddit post | over 1 year | Judging Reddit as a long-game channel | Presenter's claim | 4e8ff5bc6f43 |
| Reported visibility uplift from Reddit tactic | 4 to 5x | Unnamed brands, presenter's anecdote | Presenter's claim, not independently verifiable | 4e8ff5bc6f43 |
| Microsoft's ownership share of ChatGPT | roughly 50% | Explaining why Bing indexing matters for ChatGPT | Presenter's claim | 48ec50971ecd |
| Example sitemap pickup | 94 pages, "successful" status | Presenter's own site, illustrative only | Presenter's screen recording | 48ec50971ecd |
| Content refresh cadence | every couple of months | Any evergreen/high-intent page | Presenter's rule | 984dbd1fc95a |
| Video keyword placement | title, description, filename, thumbnail filename, first and last 10 seconds | Any YouTube video meant to rank/be cited | Presenter's heuristic | 5f0da09a8820 |
| Document sample size claimed to shift LLM output | as few as 10 documents | Basis for gray-hat "source poisoning" tactic | Unnamed studies, not cited | 5c9bc91bc0b2 |
| Self-published listicle volume for gray-hat tactic | 5 to 10 articles | Publishing own "best of" lists on trusted platforms | Presenter's rule | 5c9bc91bc0b2 |
| Press release cost | "a couple hundred dollars" | Distributing an industry-report style release via a press wire (Newswire named) | Presenter's claim | 5c9bc91bc0b2 |

## 5. Diagnostics and checks

| Check | How | Good | Bad | Next step | Cards |
|---|---|---|---|---|---|
| Can AI bots reach the site? | Free bot-validation tool, enter URL `[web check: tool]` | Passes for GPTBot, PerplexityBot, AI overview bot | Any bot blocked | Fix robots.txt/CDN/firewall rule for that bot only | ac1b7d780e6a |
| Is important content hidden behind JavaScript? | Free JS-rendering checker, enter URL `[web check: tool]` | Title, meta description, headings, body copy visible without JS | Key content missing from non-JS render | Fix rendering or pre-render key content | ac1b7d780e6a |
| Is the site indexed? | `site:yourdomain.com` in Google | Product/category/content pages appear | Pages missing | Check sitemap submission and technical indexing issues | 48ec50971ecd |
| Is the sitemap accepted? | Google Search Console > Indexing > Sitemaps; Bing Webmaster Tools | Status "successful," expected page count picked up | Errors or low page count | Re-submit; investigate crawl/technical issues | 48ec50971ecd |
| Are facts consistent everywhere? | Compare About page, schema, directories, review platforms | Identical name, address, phone and key facts | Any mismatch | Correct the outdated source | b2f279ddb882, f91363a42603 |
| Does the page front-load the answer? | Read the first third of the page | Direct 2-4 sentence answer + TL;DR near the top | Marketing build-up before the answer | Rewrite the top section | 10e99e650616 |
| What does AI already believe about the brand? | Prompt: "Search the internet and tell me what you know about [brand]" | Accurate, complete description | Wrong, missing, or competitor-favoring answer | Open cited sources, correct or contest each one | dcb1c3495233 |
| What does AI think matters for this category? | Prompt: "What do you look for when recommending [category]?" across multiple engines | Criteria you already meet and can prove | Criteria you cannot honestly claim | Add only accurate, verifiable details; do not invent | 81e3b397ce06 |
| Which sources dominate a category's AI answer? | Search "best [category]" in AI Overviews/AI mode, note cited sources | Your brand appears | Only competitors and listicles appear | Pursue listicle placement (3.11) or mentions on those same sources | 61e62cdd75c6, dcb1c3495233 |
| Is content stale? | Check last-updated date and content age | Updated within a couple of months, current stats | Old stats, no visible update date | Refresh content and date genuinely | 984dbd1fc95a |

## 6. Tools, settings and named features

- **Free robots.txt / bot-access checker**: unnamed, "first link in the description." Tests GPTBot, PerplexityBot, and an unnamed AI overview bot. [ac1b7d780e6a] `[web check: name and URL]`
- **Free JavaScript-rendering checker**: unnamed. Shows text visible with JS disabled. [ac1b7d780e6a] `[web check: name and URL]`
- **Google Search Console**: Indexing > Sitemaps for submission; `site:domain.com` for a manual indexation check. [48ec50971ecd] `[verify UI]`
- **Bing Webmaster Tools**: parallel sitemap submission, called out as disproportionately important for ChatGPT-sourced answers. [48ec50971ecd] `[verify UI]`
- **Schema generator website**: unnamed, used to build Organization schema and other types. [618db29e2091] `[web check: name and URL]`
- **Hunter**: Chrome extension that surfaces contact details for people at a target website or business, used for listicle and source outreach. [61e62cdd75c6] [dcb1c3495233] `[web check: current extension name/availability and terms of use]`
- **Keywords Everywhere**: keyword research tool for finding low-competition keywords, mentioned once, no procedure given. `[web check: current tool]`
- **Answer Socrates**: question-research tool; input topic and country, returns questions to answer as articles, mentioned once, no procedure given. `[web check: current tool]`
- **F5Bot**: free alert tool that notifies when a chosen keyword is mentioned on Reddit (and elsewhere). [4e8ff5bc6f43] `[web check: current tool]`
- **Gemini**: used live in the video to demonstrate the "what do you look for when recommending X" prompt; the same prompt is meant to be run across multiple AI engines. [81e3b397ce06]
- **Newswire**: press-release distribution service named for the industry-report tactic. [5c9bc91bc0b2] `[web check: current service and pricing]`
- **Google Business Profile**: completed with product/USP/tenure details. [f91363a42603] `[verify UI]`
- **Review/directory platforms named**: Yelp, Trustpilot, Crunchbase, G2, Capterra (implied for software). [f91363a42603]
- **Focal**: the presenter's own in-development tool, described as AI agents to automate the checklist; waitlist only, not evaluated. [64120ce92436]
- **Futureproof**: the presenter's free AI-visibility community for best practices and schema questions; commercial/community funnel, not evaluated. (context, not cited to a specific card)

## 7. Examples and case results

All examples come from the presenter's single recurring case, a self-storage software business, or from his own unnamed community/client base. None are controlled or independently verifiable.
- The self-storage software business already ranks in AI search results the presenter shows on screen ("here, here, and also here"). [64120ce92436]
- The same business's website passed all crawler-access tests across GPTBot, PerplexityBot, and the AI overview search bot. [ac1b7d780e6a]
- The presenter's own Google Search Console example picked up 94 pages with a "successful" sitemap status. [48ec50971ecd]
- Searching "best self storage software" surfaced listicles as the dominant AI Overview/AI mode sources; the presenter's example business was already featured at the top of one. [61e62cdd75c6]
- A YouTube video the presenter made for the self-storage business ranks on page 1 of Google and is also used as an AI source; he says he currently holds 2 to 3 page-1 spots for a term he calls "chat GBT ads" [likely "ChatGPT ads," transcription artifact]. [5f0da09a8820]
- Reddit tactic: "we've seen brands... 4 to 5x their visibility" from consistent value-first Reddit engagement, unnamed brands, presented as a case result, not a benchmark. [4e8ff5bc6f43]
- Industry-report press releases: "from completing tests in clients and also with people in our community," these are "cited a lot more and are being trusted more" than plain listicle articles, an anecdotal claim with no numbers given. [5c9bc91bc0b2]

## 8. Mistakes the source warns about

1. Blocking AI crawlers unintentionally via robots.txt or CDN/firewall rules. [ac1b7d780e6a]
2. Letting excessive JavaScript hide title, meta description, headings or body copy from bots that do not render JS. [ac1b7d780e6a]
3. Leaving pages unindexed in Google/Bing while expecting AI recommendation. [48ec50971ecd]
4. Having no About/Facts page, so AI has no authoritative brand description to draw on. [b2f279ddb882]
5. Letting facts drift out of sync between the About page, schema, directories and reviews. [b2f279ddb882] [f91363a42603]
6. Burying the direct answer under marketing build-up instead of the top third of the page. [10e99e650616]
7. Using vague claims ("many users prefer") instead of numbers, quotes and original data. [c8d59fd79d48]
8. Letting content go stale with no visible last-updated date. [984dbd1fc95a]
9. Deceptively re-dating unchanged content "so your competitors don't notice" — the presenter's own tactic, flagged here as manipulation, not quality improvement. [984dbd1fc95a]
10. Inconsistent NAP (name, address, phone) across directories and platforms. [f91363a42603]
11. Incentivizing reviews without checking the platform's current rules; Google specifically prohibits incentivized reviews. [f91363a42603]
12. Treating AI-stated "buying criteria" as the actual ranking algorithm rather than a hypothesis to verify. [81e3b397ce06]
13. Inventing certifications or claims to match an AI-elicited checklist. [81e3b397ce06]
14. Posting on Reddit for promotion before building karma with genuine value, risking a ban. [4e8ff5bc6f43]
15. Publishing short posts instead of long-form articles on LinkedIn (short posts are not indexed the same way). [6aaf743e7f1f]
16. Fabricating figures, quotes, or "research" for the gray-hat listicle and press-release tactics. [c8d59fd79d48] [5c9bc91bc0b2]
17. Relabeling a self-serving promotional ranking as an independent industry report without disclosing method, sample and sponsorship. [5c9bc91bc0b2]

## 9. Caveats, conflicts and what is missing

**Inside the source and its cards**
- Direct conflict: procedure 3.15 recommends incentivizing reviews at $10 to $20 per review (source text, folded into card f91363a42603), while cards f91363a42603 and 77505b864e04 both flag that incentivized reviews violate the rules of at least 1 major platform (Google) and that current platform policy must be checked before offering any incentive. The video does not resolve this itself; it simply recommends the tactic. This is a live conflict with common ecommerce advice: mainstream guidance is to never incentivize or condition reviews on outcome, for legal and platform-policy reasons (FTC-type disclosure rules apply outside the transcript's scope too). `[web check: current Google, Yelp, Trustpilot, G2 and Capterra incentivized-review policies]`
- The "update only the date, not the content" freshness trick (section 3.9, step 4) is presented by the presenter as something to do "really slightly so your competitors don't notice" — an explicit admission of manipulating a freshness signal. This conflicts with standard SEO/content advice that ties freshness signals to real substantive updates.
- Section 7 (parasite SEO / source poisoning, self-published listicles, and the press-release-framed-as-industry-report tactic) is introduced by the presenter himself as "gray hat," and he explicitly says "some businesses may say this is unethical" and leaves the choice to the viewer. Card 5c9bc91bc0b2 adds guardrails (disclose method, do not relabel promotion as research) that the video itself does not state; treat those guardrails as the card writer's addition, not the source's own position.
- The "10 documents can poison an LLM" claim, the "44% of citations from the first third" figure, and the "4 to 10x conversion" figure are all stated without a named study, paper, or link in the transcript. Do not cite these numbers to a brand or client as established research; attribute them to this presenter if used at all. `[web check: origin of each figure]`
- Card dcb1c3495233 and card 5c9bc91bc0b2 both note that AI-cited sources vary run to run and across engines, so any "sources AI used" list from procedure 3.13 is a snapshot, not a stable target.

**Against common ecommerce advice**
- Incentivized reviews ($10 to $20 per review) conflict with platform rules most ecommerce operators are told to follow strictly (see above); this is the clearest conflict in the source.
- Deceptive "last updated" date changes without real content changes conflict with standard content-integrity practice and risk being read as manipulation if discovered by a customer, journalist, or platform.
- The entire gray-hat section (self-published "best of" listicles positioning yourself at the top while omitting competitors, and targeting competitors' own cited sources to add and favor you) sits outside normal ecommerce content-marketing ethics and may violate the terms of service of the platforms named for hosting it (Medium, Substack, LinkedIn, Quora) `[web check: current manipulation/spam policies on each named platform]`. It also risks being read as astroturfing if disclosed or discovered.
- Framing a promotional ranking as an "industry report" without disclosing sponsorship or method conflicts with standard PR and advertising-disclosure norms; card 5c9bc91bc0b2 flags this but the source text does not.

**Missing**
- No named tools for the robots.txt checker, the JavaScript-rendering checker, or the schema generator; an operator must find current equivalents before running procedures 3.1 and 3.4. `[web check: current free AEO crawler-access, rendering and schema tools]`
- No procedure for measuring "AI visibility" itself over time (this document's own scope note assigns AEO benchmark tracking to folder 06-MEA, and this source does not cover it).
- No guidance on prioritizing which AI engines to target first for a given brand or category `[needs brand data: which AI engines the brand's own customers actually use]`.
- No discussion of legal/compliance limits on comparative advertising claims used in the head-to-head pages beyond a general "keep it accurate" instruction (card 8c2682d22767 adds a caveat that legality varies by market, but gives no specifics).
- No guidance on how much AEO work an ecommerce brand of a given size should realistically expect to sustain (schema, comparison pages, third-party mentions, Reddit, LinkedIn, YouTube, and gray-hat outreach are each described as if in isolation, with no resourcing or sequencing trade-offs beyond the 1-week quick-win list).
- No discussion of how these tactics interact with existing brand reputation-management or legal review processes `[needs brand data: brand's existing PR/legal review process for public claims, press releases and incentivized outreach]`.

## 10. Card index

- ac1b7d780e6a Audit search crawler access independently from training permissions
- 48ec50971ecd Submit sitemaps and confirm indexation as an AI visibility prerequisite
- b2f279ddb882 Publish an About/Facts page as structured brand context for AI
- 618db29e2091 Validate structured product and brand facts alongside visible copy
- 10e99e650616 Front-load answers on product and category pages with a TL;DR
- ddeff4f4d862 Build FAQ sections from 'People Also Ask' to grow topical authority
- 8c2682d22767 Use comparison tables and head-to-head competitor pages to win AI recommendations
- c8d59fd79d48 Replace vague claims with hard numbers, expert quotes and original data
- 984dbd1fc95a Refresh evergreen content and surface a clear last-updated date
- f91363a42603 Fix NAP consistency and directory listings to stop AI misdescribing your store
- 61e62cdd75c6 Get into 'best of' listicles and roundup articles that AI cites
- 81e3b397ce06 Use AI-generated buying criteria as hypotheses for a product-content audit
- dcb1c3495233 Run an AI brand audit to find and correct the sources AI reads about you
- 2250abe5f1eb Earn third-party mentions, podcasts and video to build AI trust
- 77505b864e04 Collect honest product-experience reviews on relevant platforms
- 4e8ff5bc6f43 Engage Reddit communities with F5Bot monitoring to earn long-term AI citations
- 6aaf743e7f1f Publish long-form LinkedIn articles structured for AI extraction
- 5f0da09a8820 Use YouTube and video transcripts as a brand and AI citation channel
- 5c9bc91bc0b2 Publish transparent original product research through relevant press channels
- 64120ce92436 Execute a one-week AI visibility quick-win sequence
