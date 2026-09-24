# 16-AEO answer and generative engines playbook

version: 2.0-draft  |  date: 2026-09-24  |  sources: 9  |  cards: 173  |  built from: sources/*.md

## 0. How to use this playbook

**Who runs it.** The AI search visibility agent. Its job is to get a brand named, cited and described correctly inside AI answers (ChatGPT, Google AI Overviews and AI Mode, Perplexity, Gemini, Claude, Copilot), and to prove whether that work moved anything. The agent produces fix lists, rewrite briefs, mention target lists, prompt test sets and monthly visibility reports (section 9). It does not build the store, run paid media, write email flows or run the CRO program (section 1 points to those folders).

**What the sources are, and what they are not.** All 9 mini playbooks are vendor or practitioner content. 2 are Ahrefs courses (03, 07) that route every workflow through paid Ahrefs products and quote Ahrefs' own unpublished studies. 1 is a course by a presenter who sells his own tool, Data Wise, and a paid community (01). 1 is an agency CEO selling AEO services and building his own tracker (04). 1 is a presenter building a tool called Focal and a community (06). 1 is a hosting sponsor explainer with a discount code (08). 1 ends with a sponsor read for a tool called Py Rank (09). 1 is a podcast with a mid-roll ad for the host's course (02). 1 is the head of growth at a consumer SaaS company (05). None of them shows a measured ecommerce case. The only store examples are 1 fragrance category page title (02) and made-up illustrations (skincare, coffee, chocolates in 09; self-storage software in 06, whose title says "for ecommerce" but whose example is B2B software). The other evidence is B2B SaaS (Webflow in 04, Gamma in 05, Ahrefs itself in 03 and 07) or a fictional EV charger installer (01). Section 12 rates each source. Every rule below says which sources back it. Where a card added an ecommerce translation the source never gave, the rule says "(card adaptation)". Where a mini playbook reconstructed steps the source never listed, the rule says "(reconstructed)".

**ecomOS rules that override any source.** These win over anything a source recommends:
- No invented claims. Every fact, number, certification, award or "best" claim on a page or in a pitch must exist in the brand record. If the brand record does not hold it, the agent does not write it.
- No incentivised, scripted or fake reviews. Source 06 recommends paying staff $10 to $20 per review collected. That is prohibited.
- No gray-hat tactics. Prohibited: refreshing only a date with no content change to fake freshness (06); self-published "best of" listicles that hide competitors and put the brand first (06); paid placements presented as editorial or as an independent "industry report" (06, 02); buying links or bulk citations (01, 02); fake or undisclosed Reddit accounts (04, 05, 06); fabricated press releases (02's own test); hidden incentive text aimed at autonomous agents (05). Section 3.10 lists all of them with the source that raised each one.
- Claims match the brand record, in every channel: site, schema, directories, listicles, press, video, community posts.
- Reading level below tenth grade on every page and in every piece of copy the agent produces. Short sentences. Digits. No em dashes.
- Keep brands apart. Keep public web research separate from private business data.
- No paid or side-effect calls without checking the budget ledger first.

**Which sections to load for which task.**

| Task | Load | Run |
|---|---|---|
| First look at a brand's AI visibility | 0, 1, 2, 3.1, 3.2, 3.7 | Procedures P3, P4, P6 |
| Technical crawlability audit | 3.3 | P1, P2, checklist 5.1 |
| Rewrite a PDP, category page or buying guide for citation | 3.4, 3.5 | P8, P9, P10, checklist 5.2 |
| Build the question set and prompt test set | 3.5, 3.8 | P5, P6, checklist 5.4 |
| Earn mentions (listicles, Reddit, YouTube, reviews, press) | 3.6, 3.10 | P11 to P15, checklist 5.3 |
| Set up measurement | 3.8 | P16, checklist 5.5 |
| Monthly report | 3.8, 6, 9 | P17 |
| Test whether a tactic works | 3.8 | P7 |
| Vet a GEO agency or tool | 3.9, 3.10 | P18, checklist 5.6 |
| Decide whether a proposed tactic is allowed | 3.10, 7 | none; decide from the list |

**What to fetch before acting.**
- From the brand record: what the brand sells, its verified facts (founding year, materials, certifications, prices, shipping and returns policy), its competitor list, its voice rules, and which claims are approved. `[needs brand data: verified fact sheet]`
- From the data layer: current robots.txt and CDN settings, GA4 access, Search Console and Bing Webmaster access, post-purchase survey platform, review platform accounts, existing top pages by traffic and backlinks, any current AI referral traffic. `[needs brand data: analytics and platform access]`
- From the user: which AI platforms the brand's buyers use, budget ceiling for tools and placements, legal and PR review rules for public claims, and the time horizon (a 10-year brand and a 6-month test site get different tactics, section 3.2). `[needs brand data: buyer platform mix, budget, review process, horizon]`
- From the web: current AI crawler user-agent names, Cloudflare's current default AI-bot setting, current referrer-passing behaviour per platform, current tracker tools and prices, and the live citations for the brand's priority prompts. `[web check: all of these change monthly, section 11]`

## 1. Scope and outcomes

**What this domain covers.** How AI answer engines choose what to cite and name. Making a site retrievable by AI crawlers. Writing and structuring on-site pages so an engine can lift a clean answer. Earning third-party mentions that engines already read. Auditing what engines say about a brand and fixing wrong facts at the source. Measuring AI visibility with a fixed prompt set, referral data, bot logs and self-reported attribution. Vetting GEO vendors and tools. Deciding which tactics are allowed.

**What it does not cover.** Point the agent to the neighbour folder:
- Core SEO (keyword research at depth, backlink strategy, site architecture, technical SEO beyond crawler access). The sources route this to a "15-SEO" folder that does not exist in playbooks/v2 at this date. Use 13-ORG for organic content and 08-SPD for page speed until it does.
- Organic social and content calendars: 13-ORG.
- Landing page and PDP conversion design: 07-LPG, 09-CRO.
- Page speed engineering: 08-SPD.
- Measurement infrastructure, attribution models and dashboards beyond the AI-specific channel and survey: 06-MEA.
- Review collection flows and post-purchase surveys as a program: 17-CXP. This folder only says what the AEO agent needs from them.
- Brand positioning and the verified fact sheet: 04-BRD.
- Paid social creative and Google Ads: 10-MCR, 12-GAD. Paid-search "money terms" feed question research here (R60), nothing else crosses.

**Business measures it moves.**
- AI share of voice on a fixed prompt set (the share of runs where the brand is named, per platform).
- Mentions and citations of the brand, tracked separately (01, 03).
- Accuracy of what engines say about the brand (prompt audit pass rate).
- AI-referred sessions, their conversion rate and revenue (small in volume; every source that measured it reports higher conversion than organic, section 6).
- Self-reported "heard about us from an AI assistant" share at checkout or post-purchase.
- Retrievability: 0 blocked citation crawlers, key content present in raw HTML, 0 AI-referred 404s.

Do not promise a number. 01 says there is no fixed target for citation growth; judge month-over-month direction (R97).

## 2. Inputs the agent needs

| Input | From where | Required or optional | Why |
|---|---|---|---|
| Verified brand fact sheet (what it sells, founding year, materials, certifications, prices, policies, differentiators) | Brand record (04-BRD) | Required | Every page, schema, directory and pitch must match it (R48, R49). Engines fill gaps with fiction (R7). |
| Approved claims list and legal or PR review rules | Brand record, user | Required | Comparison pages and press releases carry legal exposure (R45, R75). |
| Competitor list (3 to 5 real competitors, plus who AI names for category prompts) | Brand record, prompt audit | Required | Gap analysis and "others only" filters need named competitors (R83). |
| Buyer segment and which AI platforms buyers use | Brand record, user, HDYHAU survey | Required | Platform priority flips by segment (R15). |
| Current robots.txt, CDN and firewall rules, hosting platform | Data layer | Required | Crawler access is the first check (R23 to R26). |
| GA4, Search Console, Bing Webmaster Tools access | Data layer | Required | Referral channel, indexing and Bing AI performance tab (R91, R97). |
| Post-purchase or checkout survey platform | Data layer (17-CXP) | Required | Self-reported attribution (R92). |
| Server logs or a bot-analytics integration | Data layer | Optional | Which pages citation bots fetch (R93). |
| Top pages by traffic, by traffic decline, and by referring domains | Data layer or SEO tool | Required | Sleeper page refresh triage (R55). |
| Paid-search money terms (own and competitor) | 12-GAD, SEO tool | Optional | Seed for question research (R60). |
| Sales call notes, support tickets, live chat logs | User, data layer | Optional | Tail questions nobody has answered (R61). |
| Review platform accounts and current ratings | Data layer | Required | Reviews feed consensus (R74). |
| YouTube channel, podcast, LinkedIn presence | Brand record | Optional | Tier-3 owned surfaces (R67, R73). |
| Existing product photos, original data (surveys, test results) | Brand record, inspiration | Optional | Citable evidence (R46, R47). |
| Budget ceiling for trackers, placements, creators | User | Required | Tool pricing is dislocated from the work (R105). |
| Time horizon for the brand | User | Required | Screens aggressive tactics (R20). |
| Live AI answers for the priority prompt set | Web | Required | Baseline before any change (P6). `[web check]` |
| Current AI crawler names, Cloudflare default, referrer behaviour | Web | Required | All 3 change without notice (section 11). `[web check]` |

## 3. Decision rules

Every rule states the rule, when it applies, the mini playbooks that support it (by number), any conflict (by section 7 code), and card ids. Where only 1 source says it, the rule says so. 03 and 07 are both Ahrefs material and share the same studies, so a rule backed only by 03 and 07 has 1 evidence base, not 2. Where sources disagree, the strictest condition is kept here and the disagreement is written out in section 7. Platform behaviour claims are snapshots; every one of them carries a `[web check]` in section 10.

### 3.1 How answer engines pick sources

**R1. Work the retrieval layer, not the model's memory.** AI answers come from 2 levers: what the model learned in training (static, updated on an unstated cadence) and what it fetches live from the web (retrieval, often called RAG). Retrieval is where a brand can act this month. Influencing training data is slow and only partly demonstrated: 02's single tracked case took about 2 years to move a stated fact from "9+ months" to "6 months", not to the intended "3 weeks", and 02 says it has never seen a verifiable case of anyone reliably getting new facts into training data. 04 calls training-side effects "possibly a year out". 05 cites an unnamed study saying ChatGPT searches the live web for about 60% of queries and answers from memory for about 40%; treat that split as unverified. Condition: applies when deciding where to spend effort. A brand-new product needs retrieval work first because training data cannot know it (03). Sources: 03, 04, 02, 05. Cards: [d477a2718a07] [d1f4e5dbbbbd] [6b58426c3650] [5f5e69e87c2f] [c156aac34f0f].

**R2. Cover the whole topic a prompt fans into, not the head keyword.** An assistant splits one prompt into parallel sub-queries and merges the results. 03 cites research (Seer Interactive and Nectaf, unlinked) finding 9 to 11 sub-queries per prompt on average, up to 28, and 1 deep-research run of 420 searches for a phone case query. 02 observes only 1 to 3 sub-queries per prompt in normal use. Both can be true for different modes; the operating rule is the same: a category page or buying guide must answer the comparisons, fit questions, objections and use cases a buyer prompt implies. Condition: category pages, buying guides and comparison content. Not a reason to build 1 page per sub-query (R56, C10). Sources: 03, 07, 02, 01. Conflict: C10 (fan-out phrasing as keyword targets). Cards: [a227df367635] [4b61146be572] [36e3c790fd2d] [22b29e78f3c4].

**R3. Ranking in Google or Bing gates eligibility for most citations.** Assistants run their background searches through search-engine indexes, so an unindexed or badly ranked page is rarely retrieved. 06 adds that ChatGPT leans on Bing, so Bing indexing matters more than its search share suggests. The size of the overlap is disputed: 07 says 76% of AI Overview citations come from Google's top 10; 03 gives the same 76% then revises it to "closer to 38%" from a newer study, and adds that 14% of AI Overview citations do not rank in Google's top 100 at all; 04's unnamed study puts ChatGPT-to-Google citation overlap near 35% and Perplexity-to-Google near 70%. Use the direction (classic ranking helps a lot, and helps most on Perplexity and Google surfaces), not any single figure. Condition: always; it is why R13 puts SEO first. Sources: 02, 06, 03, 07, 04, 08. Conflict: C11 (overlap magnitude). Cards: [36e3c790fd2d] [48ec50971ecd] [e8d6d277ebfb] [4b61146be572] [d92b32a284e9].

**R4. Optimise for share of voice, not rank 1.** A Google result has 1 winner. An AI answer summarises many citations and names the brand that appears most often across them, even when a competitor holds the top single citation. The same prompt run 5 times can name the brand a different number of times because of retrieval variance and the model's randomness setting. Condition: every KPI and every test design in this folder. Track the share of runs and platforms where the brand is named, never a "position". Sources: 04, 03. Cards: [fe9e277451de] [f85af788af43].

**R5. Platforms barely overlap, so pick 1 to 3 and plan per platform.** 03 reports 14% overlap across the top 50 cited domains on Google AI Overviews, ChatGPT and Perplexity, and only 13.7% citation overlap between Google AI Mode and AI Overviews despite 86% similar answers. 05 estimates 30% to 40% overlap in what works across engines and 60% platform-specific work. 04 says track about 3 surfaces, not 10, because nobody knows which will win. Condition: choose platforms by buyer segment (R15) and by the brand's existing SEO strength (Google surfaces and Perplexity reward classic ranking most, R3). Sources: 03, 05, 04. Cards: [e8d6d277ebfb] [dec3540c6b72] [f758425ed01b].

**R6. Treat visibility as 3 states: cited with a link, named without a link, invisible.** Only about 28% of AI mentions carry a link on average (03: 51.6% Perplexity, 36.8% AI Mode, 26.9% ChatGPT, 10.7% AI Overviews). A link without a name is not a win: 02's example is a company cited as a source inside a "best companies" answer that did not name it. 01 tracks mentions and citations as 2 KPIs and says a falling mention trend is a trigger to investigate. 02 adds that a bare logo or link under an AI answer, with no click, is still a brand impression comparable to a billboard, which matters now that top-of-funnel click-through has fallen. Condition: all reporting. Report mentions, citations and "named but unlinked" as separate lines. Sources: 03, 02, 01. Cards: [dc9263a72730] [96e957d20941] [707b3fae30ad] [311517f2c62e] [816ae1a10dd0].

**R7. Engines look for consensus, freshness and authority; consensus is the one the brand controls most.** An engine has no first-hand experience, so it repeats what many sources agree on. Conflicting facts across the site, schema, directories and reviews make it state wrong information. 03's own misinformation test found that engines pick a specific false claim over a vague or absent official one: Gemini and Perplexity repeated planted fakes in 37% to 39% of answers, ChatGPT under 7% and it cited the official FAQ 84% of the time. Condition: every fact about the brand, everywhere. Sources: 07, 06, 03. Cards: [4b61146be572] [2250abe5f1eb] [f91363a42603] [748700e7c99c].

**R8. Branded mentions on other sites correlate with AI visibility more than backlinks do.** 03 and 07 quote the same Ahrefs study of 75,000 brands: branded web mentions correlate at 0.664 with AI Overview visibility, mentions on highly linked pages at 0.7, both above backlinks, domain rating and referring domains. YouTube mentions correlate at 0.737 with ChatGPT visibility, called the strongest factor studied. Correlation only, 1 vendor, no methodology published. Condition: use it to rank off-site work (mentions first, links second), not to drop link building for SEO. Sources: 03, 07 (same study). Cards: [23ce7debe703] [aaf30f11b946] [2130f7b978ac].

**R9. AI referral traffic is small, converts high, and is undercounted.** 03: about 0.25% of site traffic on average, and Google sends about 210 times more traffic than the top AI platforms combined; Ahrefs' own AI traffic was 0.5% of visits and 12.1% of sign-ups in June 2025 (23 times the organic conversion rate). 04: Webflow saw 6 times the conversion rate and about 8% of sign-ups from LLM referrals. 05: ChatGPT referrals to Gamma grew about 8 times from under 1% of traffic, then click-through fell while self-reported AI attribution kept rising. 06 claims 4 to 10 times higher conversion with no source. All are single-company or unsourced; none is ecommerce. Condition: the case for early work rests on trend and conversion quality, not volume. Never present these numbers to a client as a forecast. Sources: 03, 04, 05, 06, 07. Cards: [791c035b0f54] [d3293f344c01] [e07344cb96f8] [64120ce92436] [98c8979b5728].

**R10. Citations churn, so nothing here is one-time.** 03: over 45% of AI Overview citations change when the overview refreshes, roughly every 2 days. 05 theorises a "citation half-life" but has no number and tracks it with a spreadsheet. 06 and 02 note cited sources vary run to run. Condition: every audit, prompt test and mention list repeats on a cadence (monthly check, quarterly deep audit, R88). Sources: 03, 05, 06, 02, 09. Cards: [35cbd98861df] [0d40ada60dfc] [b78f1ae27412] [dcb1c3495233] [d94670809e77].

**R11. Treat "memory compounds first-mover advantage" as a hypothesis, not a rule.** 05 suggests that a logged-in user's prior answers influence later ones, so early visibility could compound, and notes that trackers run prompts logged out while real buyers are logged in. The source calls this "a black box". Condition: do not build plans on it; do note logged-in versus logged-out mode when sampling prompts (P6). Source: 05 only. Cards: [c156aac34f0f].

**R12. AI search adds to Google search; do not defund SEO on "search is dying" headlines.** 04 cites past panic cycles (TikTok, Instagram, Facebook search) that each added a channel, and a Google statement that publisher referrals are flat to slightly up. 08 says "you still need SEO". 01 says classic SEO delivers about 80% of what GEO needs. 04 also expects search and chat to converge into 1 experience, which is 1 more reason to keep 1 program, not 2. Condition: budget allocation. Sources: 04, 08, 01, 03. Cards: [e9c9ed5464d2] [d92b32a284e9] [3fc1358227bb] [9b7b57a525d2].

### 3.2 Strategy, sequencing and platform choice

**R13. Put 70% to 80% of effort into sound SEO before AI-specific tactics.** 02 gives the 70% to 80% split. 01 says solid SEO is roughly 80% of GEO. 04 says traditional landing pages for high-volume terms "free-ride" into AI answers and calls "AEO is a separate discipline" partly a vendor sales line. 03 and 07 call SEO the foundation with 4 additive workstreams on top (content, mentions, YouTube, technical). Condition: any brand that does not already rank for its category terms. Sources: 02, 01, 04, 03, 07, 08, 09. Cards: [79bd30ddf57b] [3fc1358227bb] [276cdec15a35] [9ffb85f5c826] [d92b32a284e9] [9297d576fa76].

**R14. Run the work in this order: crawler check, measurement, gap analysis, then match the biggest gap to its fix.** 07's closing sequence and 03's week-1 plan agree: 30-second robots.txt check first (a blocked crawler wastes everything after it), then set up the AI referral channel and the "how did you hear about us" question so day-1 is measured, then the gap analysis, then fix 1 gap at a time. Gap-to-fix map (07): AI does not associate the brand with a topic it should own means a content problem, start by refreshing pages that used to rank; competitors get recommended and the brand does not means a mentions problem, pursue listicles, reviews and threads the brand is absent from; AI cites a format the brand does not produce (video) means a format problem, get on YouTube. Condition: any new engagement. Sources: 07, 03, 06. Cards: [9ffb85f5c826] [bef60df0b856] [64120ce92436] [c801b61f7e55].

**R15. Choose platforms from the brand's own buyer evidence, not a universal ranking.** 05's prosumer ranking is ChatGPT (over 90% of Gamma's AEO-driven new users), then Google AI Overviews, Perplexity, Claude; his enterprise guess flips to Claude, Copilot and Bing first. 03 says pick 1 to 2 platforms by market share and overlap with existing SEO strength. 06 says the same and gives no method. Condition: read the HDYHAU survey and referral data first; if neither exists yet, start with ChatGPT and Google AI surfaces and revisit after 1 quarter of data. `[needs brand data: which assistants the brand's buyers name in the survey]` Sources: 05, 03, 04, 06. Cards: [f467d7f0fff2] [dec3540c6b72] [e8d6d277ebfb] [f758425ed01b].

**R16. Prefer bottom-of-funnel pages (product, category, comparison, scenario) over broad "what is X" content.** 02: AI Overviews already answer broad informational questions, high-intent terms are the least competitive even at high CPC, and Google AI Mode increasingly links to homepages, category and product pages rather than listicles. 03's AI filter: if an AI Overview fully answers a query, drop it as a click target. 07: AI Overviews appear on about 21% of keywords but 58% of question queries, and 99.9% of triggering keywords are informational. Exception (02): a brand with real authority and audience can still win with opinionated top-of-funnel content that adds a new point of view. Condition: content budget allocation for a small or mid-size brand. Sources: 02, 03, 07. Conflict: C4 (broad informational content vs topical authority and intent breadth). Cards: [efa046d88d7c] [bff108ae1155] [60bd75ec7279] [f51f401ddf5f] [3a369bfc1c08].

**R17. When the broad query is owned by incumbents, niche the prompt down, win there, then widen.** 05's ladder: "best CRM" to "best CRM for SMB" to "best CRM for fintech". 04 says the chat tail is bigger than the search tail (about 25 words per chat query versus 6 for search, figures attributed to a third party) and much of it has never been asked before, so a brand-new company can be cited within days for a specific question nobody answered. Expect competitors to copy the niche once it works; keep moving. Condition: any category where 3 to 4 larger brands own the head prompt. `[needs brand data: which narrow use cases the catalog genuinely serves]` Sources: 05, 04. Cards: [1d269cb7fde5] [5440ba5b8b20] [efe70bd32711].

**R18. Do not assume domain authority blocks a small store from citations, and do not assume it is irrelevant.** 04 and 05 say the citation layer has no authority gate today: a Reddit thread, a video or a specific help article can get a new brand cited fast, and 05 calls it "a level playing field" that he expects to close. 03 reports the median domain rating of ChatGPT's top-cited pages is 90. Both are true at different ends: head prompts go to high-authority pages, tail prompts are open. Condition: small brands work the tail (R17) and mentions (R8); big brands defend the head. Sources: 04, 05, 03. Conflict: C2. Cards: [efe70bd32711] [dec3540c6b72] [e8d6d277ebfb].

**R19. Concentrate effort on the few pages that can win.** 04: about 1 in 20 landing pages drive about 85% of traffic. 03's week-1 plan refreshes the top 5 to 10 pages only. Condition: always; spreading a fixed budget thin across the catalog is the failure mode. Sources: 04, 03. Cards: [15d85f61b2c8] [bef60df0b856].

**R20. Screen every tactic by time horizon and by "does this give the searcher the best answer".** 02: a tactic that suits a churn-and-burn site is not acceptable for a business with a 10 to 15 year plan, because a Google penalty can suppress a domain for 2 to 3 years; tactics that fail the user test (self-serving listicles, scaled comparison pages) are the ones assistants already route around, for example by adding a `site:g2.com [brand]` search. Condition: any tactic in section 3.10 or any vendor proposal. Under ecomOS the answer to gray-hat is always no; this rule is the reasoning, not a loophole. Sources: 02. Cards: [7844505735de] [605820cb3efb] [96e957d20941].

**R21. Treat AI visibility as company-wide, not a marketing hire's job.** What an engine repeats depends on product quality, review-platform standing, PR messaging, founder reputation and affiliate relationships together. No listicle or Reddit work fixes a bad product or a 2-star review page. 02's example: a firm that moved its Glassdoor rating above 4 stars saw ChatGPT stop citing Glassdoor as its review source (1 anecdote). Condition: when the prompt audit shows negative or wrong answers driven by reviews. Source: 02 only. Cards: [304fb1f93013] [138fd5c7b44a].

**R22. Run on-site and off-site as 2 workstreams with different owners.** 04: keep on-site AEO with the SEO owner; hand video and community work to a community-minded marketer, because most SEO people are weak at it. Build a separate plan per citation group: own site, video, UGC (Reddit and Quora), tier-1 affiliates, tier-2 affiliates, blogs. Condition: any brand with more than 1 person on this. Source: 04 only. Cards: [77971a0d570d].

### 3.3 Technical foundations

**R23. Check robots.txt for AI crawler blocks before any other work.** Open `yourdomain.com/robots.txt` and look for Disallow rules against GPTBot and OAI-SearchBot (OpenAI), ClaudeBot (Anthropic), Google-Extended (Google), PerplexityBot (Perplexity). 03 and 07 call it the most common technical blocker (about 5.9% of 140 million sites blocked GPTBot in Ahrefs' scan). It takes 30 seconds. Condition: first step of every engagement and after every CDN, theme or platform change. `[web check: current crawler user-agent names per vendor; new ones appear]` Sources: 03, 07, 06, 04. Cards: [bc44a7efd9f2] [75ea98447324] [c801b61f7e55] [ac1b7d780e6a] [c722163c16a0]. (03's 2 cards are near-duplicate extractions of 1 passage; count as 1.)

**R24. Allow the retrieval and citation bots; decide on training bots separately.** OpenAI uses GPTBot for training and OAI-SearchBot and ChatGPT-User for search and citation; Google-Extended is a training signal, not the search crawler. Blocking everything forfeits the channel to competitors (04). A site can allow retrieval while opting out of training. Keep checkout and account paths protected as before. Condition: robots.txt policy decisions. 04 gives the principle but not the bot names; the names come from 03 and 07, and the OAI-SearchBot versus GPTBot distinction in 06 is a card addition the video did not make. `[web check: current training-versus-search bot split per vendor]` Sources: 04, 03, 07, 06 (card adaptation). Cards: [c722163c16a0] [bc44a7efd9f2] [8f0d6e616976] [ac1b7d780e6a].

**R25. If the site is behind Cloudflare, check its AI-bot setting separately.** Cloudflare's "instruct AI bot traffic with robots.txt" feature was on by default at recording time and can rewrite robots.txt to disallow AI crawlers without the owner knowing. Condition: any Cloudflare-hosted store. `[verify UI]` `[web check: current Cloudflare default and setting name]` Sources: 03, 07. Cards: [bc44a7efd9f2] [c801b61f7e55].

**R26. Confirm indexing in both Google and Bing, and submit the sitemap to both.** 06: ChatGPT draws on Bing, so Bing Webmaster Tools submission matters disproportionately. Spot-check with `site:yourdomain.com`. A SKU or collection page that is not indexed cannot be surfaced. 01: a launched site not submitted to Search Console is "wasted pixels". Condition: launch, every new collection, and whenever a page never appears in answers. `[verify UI]` Sources: 06, 01. Cards: [48ec50971ecd] [cb715d72eaf3].

**R27. Key content must be in the raw HTML, not only after JavaScript runs.** AI crawlers fetch, parse and chunk pages live; 03 claims ChatGPT's crawler does not render JavaScript while Gemini and Copilot do. Test by disabling JavaScript and reloading, or with a rendering checker; title, meta description, headings and body copy must show. Fix with server-side rendering or pre-rendering. Condition: any store whose theme or app injects product copy, specs, reviews or FAQ content client-side. `[web check: current JS rendering support per crawler]` Sources: 03, 06. Cards: [d9728871b1a5] [ac1b7d780e6a].

**R28. Keep pages fast; a slow page can be dropped before it is scored.** Core Web Vitals work done for SEO covers most of it. 01 pushes Lighthouse scores toward 100 and converts PNG to WEBP before upload. Condition: always; the engineering lives in 08-SPD. Sources: 03, 01. Cards: [d9728871b1a5] [1007ba5c92ec] [ba67965b3332].

**R29. Use a clean heading hierarchy with 1 H1 that states the offering.** H1 title, H2 sections, H3 subsections, each section self-contained, 1 idea per paragraph, because a chunk boundary can fall at any heading. 01 flags Shopify's Dawn theme using the logo as the homepage H1 by default. Condition: every page meant to be cited. `[verify UI: theme defaults]` Sources: 03, 01, 09. Cards: [a4891c6c3426] [24de1308655a] [4ddb9e4eaae6].

**R30. Keep accurate schema for its SEO value; validate it; do not expand it in the name of AEO alone.** 03: keep Product, Offer, Organization, BreadcrumbList, Article, FAQ and HowTo where they fit, but there is no confirmed evidence schema improves AI citation. 06 and 09 push Organization schema (founding date, description, social and YouTube profiles) and product schema as an AI signal without evidence. 04 notes that commerce answers with shoppable cards lean on rich-snippet data and review counts, which argues for accurate Product and review schema on commercial grounds. 01: never trust a plugin's schema without validating it. Condition: schema facts must match the fact sheet (R49). Sources: 03, 06, 09, 04, 01. Conflict: C12. Cards: [ccbc5be4692f] [618db29e2091] [4ddb9e4eaae6] [7a7c5e12d8bc] [24de1308655a].

**R31. Treat llms.txt as low priority, and a vendor that leads with it as a yellow flag.** 03: at recording time OpenAI did not use it, Anthropic published one but had not confirmed its crawlers read it, Google had not adopted it; it will not hurt but should not be prioritised. 02 uses "do you recommend llms.txt, an AI info page, or chunking all content" as grifter probes for vendors. 08 names it once without explaining it. Condition: do not spend engineering time on it until a major engine documents that it reads it. `[web check: current adoption]` Sources: 03, 02, 08. Conflict: C13. Cards: [ccbc5be4692f] [3be904342c0a].

**R32. Redirect AI-hallucinated URLs that receive traffic.** 03: AI sends visitors to 404 pages about 2.87 times more often than Google, and about 1% of ChatGPT-clicked URLs 404. Filter analytics for AI-referrer sessions landing on 404s; if a made-up URL gets consistent visits, 301 it to the closest real page. Condition: monthly, once the AI referral channel exists (R91). Source: 03 only. Cards: [64a695c65c71].

**R33. Put support and help content in a subdirectory and cross-link it into a cluster.** 04 says subdomains underperform for citation and help-centre articles are usually badly linked to each other. Source is B2B SaaS; for a store this means the FAQ, care guides, sizing and policy pages. Condition: when the brand has a help centre on a subdomain or a help-desk tool. `[verify UI: whether the help-desk platform supports subdirectory hosting]` Source: 04 only. Cards: [6ed9256ad5d8].

**R34. Link supporting content to the money page it supports, where it genuinely fits.** Internal links help crawling, navigation and pass authority deeper. Not on every mention. Condition: every guide, FAQ and comparison page. Source: 01 only. Cards: [bc9c4929973d].

**R35. Plan the site structure and build 1 page per distinct offering before writing anything.** 01 calls one page covering every product or service "the number 1 mistake". Only build a dedicated page where research shows independent demand for that variant. Use a consistent URL pattern. The ecommerce mapping (distinct products and useful collections) is a card adaptation of a service-business example. Condition: new stores and re-platforms. Sources: 01 (card adaptation). Cards: [60eade3cd695] [77a7370ed12c].

### 3.4 On-site content rules

**R36. Put the direct answer first, under a question-shaped heading, in a passage that stands alone.** This is the 1 rule every source agrees on, under different names: content capsule (01), BLUF (03, 07), answer-first (09), quotable passage (08), front-loaded TL;DR (06), question-led headings (05). Length guidance differs: 01 says 20 to 25 words per capsule, up to 50 if needed; 06 says a 2 to 4 sentence answer followed by a TL;DR block; 07 gives no length. Keep the strictest: 20 to 50 words of direct answer, then supporting detail. 06 adds that over 44% of AI citations come from the first third of a page (unsourced). Condition: every section of every page meant to be cited: PDP, category page, buying guide, comparison, FAQ. Sources: 01, 03, 07, 06, 08, 09, 05. Cards: [50fb70d1a21f] [08fd8b80c5a7] [5da2c2bb06ad] [10e99e650616] [cf7bae2b5009] [06e30e5bb046] [4959f5bec48f].

**R37. Make every H2 section atomic.** Read the section out of context; if it depends on "as mentioned above" or "this product", rewrite it, because the engine chunks at heading boundaries the writer cannot see. 07 notes this trades off narrative flow and gives no rule for balancing it; ecomOS keeps brand voice in the intro and story sections and makes the fact sections atomic. Condition: every page meant to be cited. Sources: 03, 07, 08. Cards: [08fd8b80c5a7] [79e59016f274] [cf7bae2b5009].

**R38. Write entity-rich, declarative sentences.** Name the product, material, model and competitor instead of "this item" or "many users". 1 idea per sentence, subject-verb-object. If a sentence takes 2 reads, simplify it. This matches the ecomOS reading-level rule. Condition: every page. Sources: 03, 07, 09. Cards: [08fd8b80c5a7] [79e59016f274] [06e30e5bb046].

**R39. Use the buyer's phrasing for headings, titles and opening lines.** 09 starts from conversational long-tail questions a shopper types into an assistant. 05 chooses titles and headings from the actual prompts people type, not clickbait, while keeping the page useful to a human. 02 goes further: read the literal sub-query phrasing the engine runs (P20) and place it in the title tag, URL slug, H1 and first sentence, because it usually differs from the user's original wording. 01: use the customer's word ("Tesla charger installation"), not the trade term. Condition: every rewrite brief. `[needs brand data: real buyer phrasing from support tickets, search queries, survey free text]` Sources: 09, 05, 02, 01. Conflict: C10. Cards: [9297d576fa76] [4959f5bec48f] [f587896fb244] [04b6ed95b92b].

**R40. Freshness beats length; refresh with substance, on a cadence.** 03 and 07 (same study): word count correlated with citation at 0.04 across 174,000+ cited pages, 53.4% of cited pages were under 1,000 words, cited content was about 25.7% fresher than organic results, 89.7% of ChatGPT's top-cited pages were updated in 2025 and 76% in the last 30 days. Cadence: 06 says every couple of months; 07 says content untouched for 6 months is at a disadvantage; 03 refreshes the top 5 to 10 pages in week 1. Keep the strictest: review high-intent pages every 2 months, and nothing sits untouched past 6 months. A refresh means new facts, prices, specs, examples or recommendations, and the visible date moves only when the content did. Condition: category pages, comparison pages, top buying guides first. Sources: 03, 07, 06. Conflicts: C3 (length), C14 (date-only refresh, prohibited). Cards: [9edf8483abdc] [e3c82eeb7e04] [984dbd1fc95a] [4e6f7e7f1aa7].

**R41. Refresh sleeper pages before writing new pages, but only when the decline is a content problem.** Find pages with existing backlinks and declining traffic; freshness plus prior authority is the fastest route to a citation. If the page never had meaningful referring domains, a rewrite will not fix it. Condition: the content-gap fix in R14. Sources: 03, 07. Cards: [4e6f7e7f1aa7] [e3c82eeb7e04].

**R42. Build the format that already gets cited for the target prompt.** 03: 43.8% of ChatGPT citations are listicles or comparisons. 04: look at what page type dominates the citations for a question set (listicle, category page, article, tool page) and build that type rather than inventing one. 06: put a comparison table near the top; tables lift cleanly into answers. 02: a plain product-grid category page titled "best fragrances for men" ranked for that bottom-of-funnel query with no listicle at all. Condition: check the live answer before choosing a format (P5 step 6). Sources: 03, 07, 04, 06, 02. Cards: [9edf8483abdc] [a082ffa8e1fc] [8c2682d22767] [bff108ae1155].

**R43. Write honest head-to-head comparison pages against 3 to 4 larger competitors.** 06: the engine already knows the big players; the comparison supplies its reasoning to recommend the brand. Give real pros and cons for both sides, keep prices and specs current, put the table near the top. 05 warns that naming a competitor can help that competitor's own visibility, so choose deliberately. ecomOS: every comparative claim must be verifiable in the brand record, and comparative advertising rules vary by market. `[needs brand data: approved competitor claims and legal review]` Condition: categories where buyers compare alternatives. Sources: 06, 05. Cards: [8c2682d22767] [9efc84d55e51] [1d269cb7fde5].

**R44. Replace vague claims with numbers, named quotes, original data and linked sources.** 06: at least 1 piece of original data per important page (a survey, an internal benchmark, a test result) and quotes from named team members with a public profile. 01: cite the source of any fact or number with a contextual link; a reader who leaves on a citation link was not held by the content anyway. 09: citations, expert quotes and statistics build trust with users and engines (asserted, no data). 08: the model passage cited the original research paper. Under ecomOS, only real, verifiable figures; nothing invented for the sake of "original data". Condition: buying guides, category guides, comparison pages, PDP spec sections. Sources: 06, 01, 09, 08. Cards: [c8d59fd79d48] [2b192a421dcf] [9da08c76878] [cf7bae2b5009].

**R45. Pass the information-gain and typicality test before publishing.** 04: ask "did this page say something nobody else said" and "how closely does it mirror the top competitor pages". 01: add first-hand experience the engine cannot invent; 1 documented result ("we tried X and got Y") counts. 05: go beyond a bare description into a reasoned angle (5 concrete benefits, why it beats the alternative). Condition: any page competing for a citation; scored-to-match content is what engines will learn to discount. Sources: 04, 01, 05. Cards: [b0dba8938d4e] [2b192a421dcf] [4959f5bec48f].

**R46. Fill every information gap about the brand with specific official facts, on the site.** 03's test showed engines choose specific fiction over vague truth (R7). 06: publish an About or Facts page listing what the brand sells, differentiators, years in business and credentials, and treat it as the canonical source for schema and directories. 02: publish pricing and useful product facts, or the model invents a number or scrapes one from Reddit or a review site. Condition: every brand; check the prompt audit (P4) for the gaps. `[needs brand data: verified fact sheet]` Sources: 03, 06, 02. Cards: [748700e7c99c] [b2f279ddb882] [5afb1c4861f4] [7d9bb64c3533].

**R47. Keep every fact identical everywhere.** Name, address, phone, founding year, product facts and claims must match across the About page, schema, Google Business Profile, directories, review platforms, listicles and video descriptions. 07: repeating the same entities across site, mentions and video builds the consensus signal. Condition: re-audit after any rebrand, move, price change or new certification. Sources: 06, 01, 07. Cards: [f91363a42603] [b2f279ddb882] [3514f3eb2279] [aaf30f11b946].

**R48. Cap the FAQ on a commercial page at about 5 questions; put the longer Q&A on a guide.** 01: no more than about 5 FAQ items on a money page, to protect transactional focus; route fuller question clusters to a buying guide or blog piece. 06: add an FAQ built from People Also Ask to the bottom of every important page and refresh it, with no cap. Keep 01's cap on PDP and category pages; 06's uncapped Q&A belongs on guides. Condition: PDP and category pages. Sources: 01, 06. Conflict: C18. Cards: [9c1581aeb2a1] [ea6702f063e4] [370b7ebbfabd] [ddeff4f4d862].

**R49. Commercial pages pass the 2-second test and carry 1 primary keyword.** Within 2 seconds, without scrolling, a visitor knows what the page sells, where (if location matters) and what to do next; plain headline, CTA above the fold, real photography over stock, specific prices, reviews that mention the product, a short "how it works". 1 primary keyword per page; secondary terms in subheadings. Condition: PDP, category and landing pages. Source: 01 only (service business; product mapping is a card adaptation). Cards: [71181984bc10] [ea6702f063e4] [60eade3cd695].

**R50. Cover intent breadth for a topic, but on the right page types.** 09: match content to informational through transactional intent so more entry points exist ("how to reduce plastic waste at home" plus "top 10 sustainable kitchen products"). Read with R16: for a small brand the transactional end comes first, and the informational piece only if the AI filter (R62) shows an Overview does not already answer it fully. Condition: topic cluster planning. Sources: 09, 02, 03. Conflict: C4. Cards: [04d9f9f38982] [efa046d88d7c] [f51f401ddf5f].

**R51. Brand any original framework, method or metric, and repeat the name everywhere.** Otherwise the engine flattens the idea into unattributed general knowledge. Define it on the site first, then use the branded name in video, social, community and press. Condition: any brand with a proprietary process, material or sizing method. Source: 03 only. Cards: [2fcdce4950af].

**R52. Aim for 60% to 70% of a buying guide in capsule form, the rest freer prose.** Source 01's heuristic, attributed to an unnamed "peer-reviewed study" that cannot be checked. Use it as a starting ratio, not a law. Condition: long guides only. Source: 01 only. Cards: [50fb70d1a21f].

**R53. AI-assisted, human-edited copy is fine; unassisted or scaled AI content is not.** 01: Google penalises thin content, not AI authorship, and the model used is not a ranking factor. 04's study: about 10% to 12% of cited or ranked content is AI-detected, about 90% is not (detector false-positive rate about 8%); 04 argues that if fully automated content worked it would collapse answers into 1 generic opinion. 02: sites that went from about 100 to 1,000+ posts in weeks spiked then declined ("rank and tank"), with 2 to 3 year recoveries; Google names it "scaled content abuse". 05: assuming AI-written content is automatically spam is a wrong assumption. Operating rule: use an assistant to draft, inject first-hand detail, edit by hand, verify every cited source, and never bulk-publish keyword-variant pages. Condition: all content production. Sources: 01, 04, 02, 05. Conflict: C9. Cards: [3fc1358227bb] [91dd48ff3974] [de7e91d4d30f] [d6f727b1e8c0] [4959f5bec48f].

**R54. Reuse a proven page as a structural template, never as copy.** Once 1 PDP or category page performs, replicate its framework across the catalog with fresh copy per page. Meta description under about 150 characters, title tag with the primary term. Condition: scaling across a catalog. Source: 01 only. Cards: [faf7cefdf38d] [a024bd850f13].

### 3.5 Question, keyword and prompt research

**R55. Start from the buyer's question, in the buyer's words, not from a keyword.** Chat queries are conversational and long; keyword tools do not hold them. 04: paste the brand's and competitors' paid-search money terms into an assistant and ask it to turn them into the questions people actually ask. 03: map the chain of follow-up questions a real buyer asks. 09: write the conversational phrases a shopper would type, then check how the engine structures its answer. Condition: the first step of any content or test-set work. Sources: 04, 03, 09, 01. Cards: [bf1d8a839388] [a227df367635] [9297d576fa76] [04b6ed95b92b].

**R56. Mine 5 question sources, then trim by hand.** (a) People Also Ask at depth (01's demo at depth 3 returned 143 questions for 1 term); (b) sales calls, support tickets and live chat, which hold tail questions with no search volume (04); (c) Reddit threads in the category (04); (d) the engine's own fan-out view (Perplexity shows it; ChatGPT needs P20) (02, 01); (e) the engine's stated buying criteria, "what do you look for when recommending [category]", run across several engines and merged (06). Every AI-generated list is noisy: 01's fan-out demo returned about 195 queries, many irrelevant. Review and cut by hand; never accept a list in bulk. Condition: every research run. Sources: 01, 04, 02, 06. Cards: [9c1581aeb2a1] [a43cf3acdd9f] [bf1d8a839388] [dd5f18c44b74] [22b29e78f3c4] [81e3b397ce06] [847055f1a547].

**R57. Do not build a keyword list out of fan-out sub-queries.** 03: over 95% have zero search volume and they change run to run. Use them to check topic coverage (R2) and to borrow phrasing (R39), not as page targets. Condition: keyword planning. Sources: 03. Conflict: C10 (02 and 01 use fan-out phrasing more directly). Cards: [a227df367635] [f587896fb244].

**R58. Split transactional from informational and route each to its page type.** Transactional feeds PDP and category pages. Informational feeds guides and FAQs. Short FAQ items (5 max) on the commercial page; full topics on a guide. Condition: every research export. Source: 01 only. Cards: [04b6ed95b92b] [370b7ebbfabd] [d644b9efe0f5].

**R59. Vet keywords with BID, then the AI filter.** Business potential (would ranking help sales), Intent (does the ranking page type match what you plan to build), Difficulty (a few low-authority sites in the top 10 is a good sign). Then search the term and read the AI Overview as a shopper: if it fully answers the query, drop it as a click target and retarget to (a) an unlinked mention inside the answer, (b) action or tool queries an engine cannot satisfy (calculator, checker, finder, planner), or (c) transactional queries. The judgment has no numeric cutoff. Condition: before spending content budget. Sources: 03, 07 (same course material). Cards: [caec8fa7e6e5] [f51f401ddf5f] [3a369bfc1c08].

**R60. Check which page type and which sources win the target prompt before writing.** Ask the prompt on 2 to 3 surfaces; note whether the cited pages are listicles, category pages, articles or videos, and which domains recur. If a big retailer or review site is consistently cited, prioritise a mention on that site over out-ranking it (02). Condition: every brief. `[web check: live answers]` Sources: 04, 02, 06, 09. Cards: [a082ffa8e1fc] [dd5f18c44b74] [61e62cdd75c6] [9297d576fa76].

**R61. Ask the engine its own buying criteria, and treat the answer as a hypothesis.** "What do you look for when recommending [category]?" across several engines gives a criteria list to test the page and directory descriptions against. Add only accurate, verifiable facts that match the list. Never invent a certification or claim to satisfy it. Condition: product copy and listing audits. Source: 06 only. Cards: [81e3b397ce06].

**R62. Use a persistent AI workspace with a brand brief for all research and drafting.** A single chat forgets earlier detail; a project holds the brief, keyword exports, competitor sitemaps and clusters. For a store, the brief covers catalog, categories, target buyer and fulfilment areas, not "services" (card adaptation). Condition: any multi-week content effort. Source: 01 only. `[verify UI: project features change by vendor and plan]` Cards: [852d326e7cca].

### 3.6 Off-site mentions

**R63. Earn mentions in 3 tiers: editorial, community, owned.** Tier 1 is editorial listicles, comparisons and review sites (hardest, most valuable; 07 names The Wirecutter and TechRadar as examples). Tier 2 is UGC: Reddit, Quora, niche forums. Tier 3 is owned: YouTube, podcast, LinkedIn, secondary domains, kept positive and on topic. 04 splits citations into 6 groups instead (own site, video, UGC, tier-1 affiliates such as Dotdash Meredith titles, tier-2 affiliates, blogs) and says each needs its own tactic. Condition: the "mentions problem" fix in R14. Sources: 03, 07, 04. Cards: [23ce7debe703] [7285d50f35a8] [de260c9bccd9] [aaf30f11b946] [77971a0d570d].

**R64. Get into the third-party listicles engines already cite, instead of building your own.** Find them 3 ways: the tracker's cited-domains or sources panel for the priority prompts (02, 03); a content search for `title:best` or `title:versus` in the category minus the brand name, filtered by referring domains (03); or run "best [category]" in AI Overviews and AI Mode and open every cited list (06). Skip listicles owned by direct competitors; 02 will not ask a competitor and ignores such requests himself. Prioritise pages that already carry links and topic relevance even if not yet cited (03). Outreach with a specific, credible case for inclusion, tracked in a spreadsheet (06). Condition: the mention target list (section 9). Sources: 02, 03, 07, 06. Cards: [07e818713c36] [2037fd15a632] [61e62cdd75c6] [aaf30f11b946].

**R65. Paid placements are allowed only when disclosed as sponsored or affiliate, never dressed as editorial.** 02 describes paying niche blogs $50 to $300 for inclusion, pursuing affiliate programs at large publishers, and observing paid "top rated" placements in newspaper sites, and says he does not condone the last one; disclosure rules vary by industry and jurisdiction. 06 treats paying for listicle inclusion as a normal cost. 04 calls paying a Forbes-style affiliate "expensive but easy and controllable". 01 says paid links must carry sponsored or nofollow attributes (a card addition; the transcript only says everybody buys links). ecomOS keeps the strictest line: a placement is acceptable when the publisher labels it sponsored or affiliate, the copy is true to the brand record, and nobody is asked to hide competitors. Buying editorial-looking coverage, and buying links for authority, are prohibited (R98, R99). `[needs brand data: legal review of any paid placement]` Condition: any paid mention. Sources: 02, 06, 04, 01. Conflicts: C7, C8. Cards: [07e818713c36] [61e62cdd75c6] [77971a0d570d] [d84b2be76cec].

**R66. Reddit: 1 real, disclosed person, 1 useful answer, in a thread that is already cited.** All 5 sources that cover Reddit agree on the shape and none allows spam. 04: find the thread that already appears in the answer to the target question, comment from a named account stating employer, give 1 genuinely useful point, no pitch; even 5 good comments "could be great"; fake accounts, auto-posting and self-upvotes are detected and deleted. 05: lead with an open-ecosystem angle (the brand works with what the community already uses) instead of "X beats Y"; choose subreddits from the buyer-persona angle and the problem angle; a smaller brand can treat small subreddits as fair game. 06: 5 to 10 relevant subreddits, build karma with value first, alert on category keywords with a tool such as F5Bot, and plan 1 to 2 years because the average cited post is over a year old (unsourced). 03: never insert the brand in unrelated threads. 02: before paying anyone for "Reddit mentions", pull the actual cited thread URLs and check thread age and whether the subreddit even allows brand mentions (his example cited thread was 8 years old and locked). Condition: tier-2 work on ChatGPT-heavy prompts (R67). `[web check: current subreddit self-promotion rules]` Sources: 04, 05, 06, 03, 02. Cards: [c3a578a68afc] [9efc84d55e51] [b78f1ae27412] [4e8ff5bc6f43] [7285d50f35a8] [3347a4baaad4] [28b9ca1fa247].

**R67. Expect Reddit to help mostly on ChatGPT, with a lag, in a few contested slots.** 05: Reddit's influence is concentrated almost entirely in ChatGPT; a new Reddit post took about 30 to 45 days to be cited by ChatGPT in 1 case, next day on Perplexity for an exact phrase; only about 4 to 5 Reddit references appear per answer, so it is a zero-sum contest with category competitors; comments shape sentiment, not which posts get cited, and a negative indexed comment persisted for months in a secondhand case. 02: Reddit temporarily dropped out of OpenAI's citations for a period, so never rely on 1 platform. 03 treats Reddit as heavily cited and as training data at once. Condition: budgeting Reddit effort. Sources: 05, 02, 03. Conflict: C5 (training-only vs most-cited; ChatGPT-only vs general). Cards: [dec3540c6b72] [b78f1ae27412] [1d269cb7fde5] [9efc84d55e51] [138fd5c7b44a] [7285d50f35a8].

**R68. YouTube: make or commission search-hit videos, not viral hits, and say the keyword out loud.** 03 and 07: YouTube is the most cited domain in AI Overviews (5.6% of citations) and YouTube mentions correlate at 0.737 with ChatGPT visibility; GPT-4 was trained on over a million hours of transcripts (claims to re-verify). Target topics with steady search demand; find them by checking which YouTube "watch" URLs rank top 3 for niche terms. Checklist: exact keyword in the title (save cleverness for the thumbnail), keyword in the first lines of the description, timestamps as chapters, the keyword spoken in the audio, match the format already ranking. 06 adds: keyword in the video and thumbnail file names, spoken in the first and last 10 seconds, a companion blog post per video, and hiring a creator to make a "best providers" video for the category. 04: video is comparatively easy because no community can veto it. 05: saw citations from an 18,000-view video and a 400,000-view video with no view-count pattern. Condition: the "format problem" fix in R14; sponsored creator videos must be disclosed. Sources: 03, 07, 06, 04, 05. Cards: [926976b809be] [224d5f463421] [1af9f13ebe90] [2130f7b978ac] [5f0da09a8820] [61e62cdd75c6] [2d4e6a109986].

**R69. Collect honest reviews on the platforms your buyers use and that appear in your category's answers; never incentivise them.** 02: engines draw on G2, Trustpilot, Yelp, Capterra, Reddit and Glassdoor unprompted, and which one matters shifts, so spread across platforms. 06: send a neutral post-purchase request about fit, quality and limitations, in the customer's own words; do not script outcomes or condition the request on satisfaction. 06's video also recommends $10 to $20 per review to staff and a QR review card at job completion; its own cards note Google prohibits incentivised reviews. 09: reviews and UGC add freshness and "diverse perspectives" (asserted). Under ecomOS, incentives and scripts are prohibited; the flow itself lives in 17-CXP. Condition: every brand. `[web check: current review-platform incentive policies]` Sources: 02, 06, 09. Conflict: C6. Cards: [138fd5c7b44a] [304fb1f93013] [77505b864e04] [f91363a42603] [98beae980f22].

**R70. Press releases: real announcements only, with the target phrase in the title, subheading and first sentence.** 02: a single ~$80 wire release with "best-selling SEO book" in the title, subhead and first line led to ChatGPT and AI Overviews citing that person for that phrase; the same source also built a fake company, bought a ~$5 release claiming a "near five-star" rating, and watched ChatGPT repeat it, which he framed as proof of the risk, not a template. 06 recommends titling a promotional ranking as an "industry report" and calls it the highest-ROI item on its list; its card adds guardrails the video never gave (describe only research actually performed, disclose method, sample, dates and sponsorship). ecomOS: releases carry real news (launches, sponsorships, awards actually won, research actually done with method disclosed) and nothing else. Condition: reputation, launches, local sponsorships. `[web check: wire service names, pricing and syndication partners]` Sources: 02, 06. Conflict: C15. Cards: [8a54ade0eeff] [5c9bc91bc0b2].

**R71. Use reporter-request platforms, podcasts and industry publications for expert mentions.** 01: create an account on a reporter-request platform (Connectivity, formerly Featured.com, formerly HARO-style), answer only the fits, expect review then selection then publication; his own hit rate was 5 published of 12 pitched on a free tier of about 3 answers a month (example, not a target). 06: at least 3 industry publications via guest posts, interviews or PR, prioritising outlets already cited in the category; pitch podcasts because transcripts are indexed; structure any long-form external piece like site content (answer in the first 2 to 4 sentences, TL;DR, tables). Condition: brands with a founder or expert who can speak with authority. `[web check: platform names, this category renames often]` Sources: 01, 06. Cards: [f6fee63ce69e] [2250abe5f1eb].

**R72. Claim free directory and business listings first, with identical NAP, and avoid bulk sellers.** 01: ask an assistant for free listing directories for the location and business type (Better Business Bureau, Foursquare, Nextdoor Business in the demo); if managing more than about 3 sites, use a citation service (Bright Local at about $3.20 per citation, about $2 at bulk, at recording time); never "300 citations for $5" on Fiverr. 06: Google Business Profile, Yelp, Trustpilot, Crunchbase and industry platforms, descriptions aligned with the AI-elicited criteria. Condition: all brands, before any paid mention work. `[web check: current pricing]` Sources: 01, 06. Cards: [3514f3eb2279] [f91363a42603].

**R73. Backlinks come last, quality over quantity, and buying them is prohibited.** 01: only after the site is built, content is published and indexing is confirmed, and only if still not competitive, consider links; even then, judge publisher relevance and real audience on a call. 01's transcript then normalises buying links ("everybody buys backlinks"); 02 says the same about paid listicles. ecomOS: no paid links. The SEO link strategy lives outside this folder. Condition: never a launch requirement. Sources: 01, 02. Conflict: C7. Cards: [d84b2be76cec] [3514f3eb2279] [07e818713c36].

**R74. Add LinkedIn long-form, Medium, Quora or Substack only if they already show up in sampled answers for the category.** 06: long-form LinkedIn articles (not short posts) are indexed and can be cited; structure them like site pages. 05: LinkedIn citation is "thin" and unpredictable; Medium and Quora showed activity once Reddit saturated; Substack is often paywalled; Discord not indexed; X never observed as a source. 05's rule: add a surface only if buyers use it or it turns up in real category answers. Condition: after tiers 1 and 2 are working. `[web check: which platforms are indexed now]` Sources: 06, 05. Cards: [6aaf743e7f1f] [b92cbebdb398] [2d4e6a109986].

**R75. Fix wrong brand facts at the source, own site first, then publisher, then repeat across channels, and expect it to be slow.** 03: publish the correct specific facts on the site, then request a correction from the third-party publisher; move fast because the longer it sits the more the engine learns it. 02: after the site, distribute the corrected claim through third-party articles, founder video and press, and update the platforms likely feeding the stale answer (G2, Reddit, Trustpilot, directories); re-run a fixed brand question set with model, date and cited evidence logged; a changed answer does not prove retraining. 06: open every cited source under "tell me what you know about [brand]" and correct or contest each. Condition: any inaccuracy found in the prompt audit. Sources: 03, 02, 06. Cards: [445fa90e4caf] [748700e7c99c] [6b58426c3650] [5f5e69e87c2f] [dcb1c3495233].

**R76. Coordinate with whoever runs affiliates, because tier-1 publishers are often affiliate relationships.** 02: durable, high-authority publishers in a vertical (Healthline, WebMD, Sleepopolis for mattresses, credit-card affiliates) are pursued through their affiliate programs, often at higher cost than wanted; run a link-intersection analysis on competitors to see which listicles and guest posts they appear in. Condition: brands with an affiliate program or budget. Source: 02 only. Cards: [07e818713c36].

**R77. An MCP or agent integration is a retention play, not acquisition, and mostly outside ecommerce today.** 05: building an MCP server and listing it in Claude's ecosystem drove usage from people already in Claude; Claude does not surface it unprompted; approval is slow. 04 raises preparing product data for agent purchasing without a method. Condition: note only; revisit when shopping-agent programs exist for the brand's platform. `[web check: current agentic commerce programs]` Sources: 05, 04. Cards: [dec3540c6b72] [ac75891ff0e4].

### 3.7 Brand gap analysis and prompt audits

**R78. Run a brand gap analysis before optimising anything.** 03's 6 gap types: visibility (not appearing), narrative (appearing with the wrong story), topic (not associated with a topic you should own), format (engines cite formats you do not make), web mentions (competitors named on sites you are absent from), demand (nobody asks yet). Label each finding fix (optimise existing), build (create new) or influence (off-site). 07 collapses it to 3 gaps (content, mention, format) mapped to fixes in R14. Repeat the identical audit on named competitors. 01 adds a 4-part SEO-side competitor analysis to run alongside it: pick 2 to 5 real competitors (from the search results and from who the assistant recommends), compare ranking keywords and traffic, inspect which URL types win for the leader (01's demo: blog posts plus location pages, not the homepage), categorise their sitemap by page type, and read their backlink profile; the output is the page types and rough page count the brand needs, with links held for later. Condition: start of engagement and quarterly. Sources: 03, 07, 01. Cards: [7ccc34f2e89e] [5ce00206b4bc] [0f0999fffc65].

**R79. Map branded entities first: brand, sub-brands, product names, proprietary features, founder names.** Each gets its own visibility profile. Attach the topics and attributes each entity should be associated with, using the adjectives and modifiers buyers already use. Condition: precondition for R78. Source: 03 only. `[needs brand data: entity list]` Cards: [7ccc34f2e89e].

**R80. Audit what engines believe about the brand by asking them, then open every cited source.** Prompt: "Search the internet and tell me what you know about [brand]." Read it as a buyer. Open every citation; those pages shape the answer. Run the same prompt for each competitor to see which sources drive their recommendations, and pursue mentions there. Repeat periodically; the source list is a snapshot. Condition: monthly, and after any PR event. `[web check: live answers]` Sources: 06, 02. Cards: [dcb1c3495233] [5f5e69e87c2f].

**R81. Check whether an answer came from a live search or from memory before acting on it.** 02: run the identical prompt in free ChatGPT, in an incognito tab, and in a logged-in paid account; compare citations; repeat a few times with varied wording. No citations or wildly inconsistent answers point to memory, which means fixing third-party sources, not only the site. 04 notes commerce answers increasingly render shoppable cards; note the answer format too. Condition: every prompt audit row. `[verify UI: session behaviour changes]` Sources: 02, 04. Cards: [5786137d7326] [536f2c6edb07].

**R82. Use tracker filters to find the 3 classic gaps.** "Mentioned but not cited" (brand named, site not linked: a missed citation); "others only" with a competitor added (they are named, you are not); topic view (who the engine associates a topic with). Then filter the "others only" list for best, top, versus, review and alternative terms to get the mention short list. Condition: when a tracker is in place; without one, do it by hand on the prompt set (P6). `[verify UI: Ahrefs Brand Radar filters]` Sources: 03, 07. Cards: [35cbd98861df] [5ce00206b4bc] [3a369bfc1c08].

**R83. Fix the single biggest gap first, with quick wins ahead of builds.** Quick wins: a ranking page that needs a topic refresh; a major listicle competitors are on that outreach can win. Do not try to close every gap at once. Condition: after every gap analysis. Sources: 03, 07. Cards: [7ccc34f2e89e] [9ffb85f5c826].

**R84. Repeat on a cadence: monthly share of voice, cited domains, topic coverage and sentiment; quarterly deep competitive audit.** Sources: 03, 09, 06. Cards: [0d40ada60dfc] [d94670809e77] [dcb1c3495233].

### 3.8 Measurement

**R85. Measure with 3 pillars together: AI referral traffic, AI bot activity, self-reported attribution.** No single one is complete. Referral shows what engines actively send; bot logs show what they read; the survey catches zero-click influence. 05: execute like SEO, measure like a view-through channel, because most AI-driven discovery never clicks. 04: for a commerce flow with clickable shoppable answers, last-touch referral is a fairer read than in B2B, but still add the survey. 08 makes the same point from the zero-click side: a dashboard that reports only rank and click-through misses the exposure engines now give. 04's habit for anything that looks unmeasurable is to find a proxy (the survey, branded search lift, share of voice) rather than declare it unmeasurable. Condition: set up before or alongside content work so day 1 is measured (R14). Sources: 03, 07, 05, 04, 08. Cards: [e3fe0904f52d] [98c8979b5728] [e07344cb96f8] [7a7c5e12d8bc] [f2a1a300d335] [621178a06132].

**R86. Build a GA4 "AI traffic" channel and treat its count as a floor.** Admin, Data Display, Channel Groups; copy the default group; add a channel matching AI referrer hostnames by regex (03's list: chatgpt.com, chat.openai.com, perplexity, gemini.google.com, copilot.microsoft.com, claude.ai, deepseek.com; escape dots, use hostname boundaries). Several platforms strip referrers: in-content links from paid ChatGPT use no-referrer, Perplexity's desktop app and Copilot on Windows do not pass it, Grok passes nothing (03). 04: AI users often open a new tab and search the brand, which lands in branded search or direct. Condition: every brand. `[verify UI: GA4 menu path]` `[web check: current referrer hostnames and behaviour]` Sources: 03, 07, 04. Cards: [c2ae662a8e4f] [98c8979b5728] [d3293f344c01].

**R87. Add "How did you hear about us?" at checkout or post-purchase, with AI options listed up front.** Options: AI assistant, ChatGPT, Perplexity, AI search such as Google AI Overviews, plus the usual channels and free text. 05: when Gamma moved AI options out of "Other", self-reported AI mentions rose sharply while click-through fell. 03: Ahrefs attributes about 3% of conversions to AI this way. Condition: every brand; the survey mechanics live in 17-CXP. `[verify UI: survey platform]` Sources: 03, 07, 05. Cards: [3d817167591c] [990877b3d70c] [e07344cb96f8].

**R88. Track which pages citation bots fetch, and separate them from training bots.** Server logs, or a bot-analytics tool with a Cloudflare integration (03 says it works on Cloudflare's free plan). Repeated visits from citation bots (ChatGPT-User, OAI-SearchBot) to a page suggest it is being used as a source; training bots (GPTBot, Google-Extended) are a different signal. No bot visits to key pages means check internal links, access rules and log coverage before assuming a crawl problem. Condition: when logs are available. `[verify UI]` `[web check: bot names]` Sources: 03, 07. Cards: [8f0d6e616976] [98c8979b5728].

**R89. Report share of voice on a fixed prompt set, run several times per platform, never a single run.** Because answers are probabilistic (R4), a prompt set of 100 to 200 questions run 3 or more times per platform on a schedule, logging model, date, mode (logged in or out, search on or off), whether the brand was named, cited, or both, and the cited URLs. 08's card 2b710976674c describes a per-query exposure log reviewed about quarterly; the mini playbook marks it as a card reconstruction of a checklist the video promised but never showed, so it supports the idea, not the cadence. Condition: baseline before any change, then monthly. Sources: 04, 03, 02, 05, 08 (card reconstruction). Cards: [f758425ed01b] [f85af788af43] [5786137d7326] [b78f1ae27412] [2b710976674c].

**R90. Prove a tactic with a test group and an untouched control group, then replicate.** 04's design: 200 questions split 100 test and 100 control; track for about 2 weeks before changing anything to see baseline variance; intervene on the test group with 1 tactic at a time (Reddit only, or a video only, or a placement only); wait about 2 weeks; compare the change in test against control; rerun or replicate on another set before adopting the tactic as a rule. 04 says most SEO and AEO "best practices" were never tested this way. Condition: any tactic the agent wants to recommend as proven. Source: 04 only. Cards: [0408383723f2].

**R91. Do not accept raw citation or mention counts as success.** 02: 1 URL can be cited across endless phrasing variants; trackers report "useless data" when the model never ran a search for the tracked prompt; a bare link with a competitor named as "best" is not a win. Ask which prompts, whether search fired, mention or citation, and whether revenue moved. Condition: every vendor report and every internal report. Sources: 02, 04. Cards: [28b2634c43eb] [96e957d20941] [56c995c391df].

**R92. Read Search Console and Bing Webmaster Tools monthly and judge direction, not an absolute.** GSC Performance: clicks, impressions, average position (impressions usually rise before clicks; expect lower CTR as answers absorb queries, 03 quotes a 58% CTR drop on the number 1 result as of December 2025). Bing Webmaster Tools "AI performance" tab: total citations, average pages cited, cited queries. No fixed growth target exists; judge month over month. Condition: every brand. `[verify UI: Bing tab name and availability]` Sources: 01, 03. Cards: [4df3dc92ffaf] [311517f2c62e].

**R93. Tie the channel to revenue: compare AI-referred conversion rate and revenue against organic.** 04's audit question for any case study: did the traffic produce more organic or LLM-referred revenue; if not, it is not a win regardless of the chart. Condition: monthly report. `[needs brand data: revenue by traffic source]` Sources: 04, 02, 03. Cards: [d3293f344c01] [7cbba7101a4d] [791c035b0f54].

**R94. Log every citation you find (query, platform, date, URL) and re-check the same queries to see persistence.** 05's manual spreadsheet is the only persistence method any source gives. Condition: alongside or instead of a paid tracker. Source: 05 only. Cards: [b78f1ae27412] [2d4e6a109986].

**R95. Track about 3 surfaces and buy the cheapest tracker that does the job.** 04: there are roughly 60 comparable trackers, functionally keyword trackers; nobody would pay $50,000 for keyword tracking, yet commodity tracking is sold at that price under the AEO label. 05 names Profound; 01 uses his own tool; 03 and 07 use Ahrefs Brand Radar. None is endorsed here. Condition: tool purchase. `[web check: current tracker landscape and pricing]` Sources: 04, 05, 01, 03. Cards: [f758425ed01b] [56c995c391df].

### 3.9 Vendor and tool vetting

**R96. Ask a GEO vendor 5 questions and 3 probes before hiring.** 02's questions: how is GEO different from SEO (vague hype is a signal); how long have you operated and when did you start in optimisation (post-ChatGPT births versus 2015 to 2017); show recent case studies and say how those clients perform now; what is your stance on off-site (affiliates, listicles, review sites) and do you have a video or social strategy; are you going to put up hundreds of blog posts (yes is a red flag). Then: explain your method in plain English (inability disqualifies); do you recommend llms.txt, an "AI info page", or "chunking" all content (enthusiastic yes leans red flag); does your platform have a built-in content generator. Run any confusing jargon through an assistant to see if it holds up. Condition: any agency or tool purchase. Source: 02 only. Cards: [5872777fb613] [3be904342c0a] [d6f727b1e8c0].

**R97. Audit a case study by keyword difficulty band and by "now", not by a blended chart.** Split the case study's keywords at a difficulty threshold (02 uses Ahrefs difficulty above 30); compare trends per band; harder, commercially valuable keywords declining under a rising total is early rank-and-tank; ask whether revenue moved; verify in your own tool rather than trusting a screenshot. Condition: every vendor case study, and the agent's own results. `[verify UI: difficulty metric]` Source: 02 only. Cards: [7cbba7101a4d].

**R98. Treat every vendor statistic as a snapshot from an interested party.** The big numbers in this folder (75,000 brands, 174,000 pages, 140 million sites, 0.664, 0.737, 43.8%, 25.7%, 89.7%) are Ahrefs studies quoted in Ahrefs courses without links or methodology; 04's 35% and 70% overlaps are an unnamed Graphite study; 06's 44%, 4 to 10 times and "10 documents" are unsourced; 05's 60/40 split is an unnamed study. Use direction, attribute the number to the source if quoted, and never present one to a client as an industry fact. Condition: all reporting. Sources: 03, 07, 04, 06, 05. Cards: [9edf8483abdc] [23ce7debe703] [10e99e650616] [c156aac34f0f].

### 3.10 Gray-hat and prohibited tactics

Each item below was recommended, described or raised by at least 1 source. Under ecomOS the agent does not run any of them, does not propose them, and flags them when a vendor or user proposes them. The source and card are listed so the agent can explain why.

**R99. Prohibited: scaled AI content.** Bulk keyword-variant pages or hundreds of templated posts to chase fan-out. 02: rank-and-tank, 2 to 3 year recovery, named by Google as scaled content abuse. 04: model collapse. Sources: 02, 04. Cards: [d6f727b1e8c0] [de7e91d4d30f] [61fbe7ae9c54].

**R100. Prohibited: fake, undisclosed or automated community accounts, self-upvoting, cold link drops.** 04, 05, 06, 03 all warn it is detected, deleted and banned. Cards: [c3a578a68afc] [9efc84d55e51] [4e8ff5bc6f43] [3347a4baaad4].

**R101. Prohibited: incentivised, scripted or conditional reviews.** 06 recommends $10 to $20 per review and a review card at job completion; its own cards note Google prohibits incentives. Sources: 06. Conflict: C6. Cards: [f91363a42603] [77505b864e04].

**R102. Prohibited: changing a visible date with no content change.** 06's presenter says to do it "really slightly so your competitors don't notice"; 03 says do not just change the publish date. Sources: 06 (recommends), 03 (forbids). Conflict: C14. Cards: [984dbd1fc95a] [9edf8483abdc].

**R103. Prohibited: self-published "best of" listicles that put the brand first and omit competitors, published on Medium, Substack, LinkedIn, Quora or owned sites to "poison" the model.** 06's gray-hat section, based on unnamed "10 documents" studies; 02 observes engines already route around self-serving listicles with `site:g2.com` style searches. Sources: 06 (recommends), 02 (warns). Conflict: C16. Cards: [5c9bc91bc0b2] [96e957d20941] [605820cb3efb].

**R104. Prohibited: paid placements presented as editorial, and promotional rankings relabelled as an "industry report".** 02 describes paid "top rated" placements in newspaper sites and does not condone them; 06 recommends the industry-report framing; 06's card adds disclosure guardrails the video never stated. Sources: 02, 06. Conflicts: C8, C15. Cards: [07e818713c36] [5c9bc91bc0b2].

**R105. Prohibited: buying links or bulk citations.** 01 normalises it in the transcript; 01's card adds a sponsored or nofollow requirement the presenter never said. Sources: 01. Conflict: C7. Cards: [d84b2be76cec] [3514f3eb2279].

**R106. Prohibited: fabricated press releases, fake ratings, invented claims or certifications to match an AI criteria list.** 02's fabricated-company test; 06's "do not invent certifications". Sources: 02, 06. Cards: [8a54ade0eeff] [81e3b397ce06] [c8d59fd79d48].

**R107. Prohibited: hidden incentive text aimed at autonomous agents ("agentic bribing").** 05 reports other growth people experimenting with reward text inside JSON schemas or install packages; legality and platform policy unaddressed. Source: 05. Cards: [c156aac34f0f].

**R108. Prohibited: emailing competitors to ask for inclusion in their listicles.** Not unethical, just documented as futile; 02 ignores such requests himself. Source: 02. Cards: [07e818713c36].

**R109. Allowed with disclosure: sponsored or affiliate listicle placement labelled as such; sponsored creator videos labelled as such; press releases for real news; paid directory or citation services that create real listings; a real employee posting under their own name and employer.** Sources: 02, 04, 06, 01. Cards: [07e818713c36] [77971a0d570d] [2250abe5f1eb] [3514f3eb2279] [c3a578a68afc].

## 4. Procedures (implementation)

Each procedure names its goal, preconditions, steps, the check after each step, and rollback. Steps that touch a platform screen carry `[verify UI]`. Where a source gave the idea but not the steps, the procedure says "(reconstructed)".

### P1. Technical crawlability audit

Goal: confirm AI citation crawlers can fetch, render and index the pages that matter. Preconditions: site URL, hosting and CDN details, Search Console and Bing access. Sources: 03, 07, 06, 01, 04.

1. Open `https://yourdomain.com/robots.txt` in a browser. List every `User-agent` block and its `Disallow` lines. Check: any rule against GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, Google-Extended, PerplexityBot, or a blanket `User-agent: *` with `Disallow: /`. `[web check: current crawler names]` [c801b61f7e55] [bc44a7efd9f2]
2. Decide the policy per bot (R24): allow search and citation bots; training bots per the brand's choice; checkout, cart, account and search-result paths stay disallowed as before. Record the decision.
3. If on Cloudflare, open the bot settings and find the AI-bot robots.txt feature; if it is on and the brand wants to be cited, turn off the auto-rewrite or edit the managed rules. `[verify UI]` `[web check: current default]` [c801b61f7e55]
4. Check firewall and WAF rules and any "block bots" app on the store platform for the same user agents. `[verify UI]`
5. Re-fetch robots.txt after every change and confirm the rule is gone. If a site audit tool is available, run its AI-crawler check. `[verify UI]` [bc44a7efd9f2]
6. Run a free bot-access checker on the homepage, 1 PDP, 1 category page and 1 guide (06 uses an unnamed tool). A spoofed user-agent test is not proof; confirm with server logs where possible. `[web check: current checker tool]` [ac1b7d780e6a]
7. Disable JavaScript in the browser and reload the same 4 pages. Check: title, meta description, H1, H2s, product copy, specs, price, FAQ and review text are present without JavaScript. If not, note which blocks are injected client-side. [d9728871b1a5] [ac1b7d780e6a]
8. Run Lighthouse (Chrome DevTools, Lighthouse tab) on the same 4 pages; record performance, accessibility, best practices, SEO. `[verify UI]` [1007ba5c92ec] [d9728871b1a5]
9. In Google Search Console, Indexing, Sitemaps: confirm the sitemap status is success and the discovered count is proportionate to the page count. Repeat in Bing Webmaster Tools. Spot-check `site:yourdomain.com` for PDPs and collections. `[verify UI]` [48ec50971ecd] [cb715d72eaf3]
10. In GA4, filter sessions from the AI channel (P16) landing on 404 pages; list any URL with repeat visits. [64a695c65c71]
11. Check heading hierarchy on the 4 pages: 1 H1 stating the offering; H2 sections; check the homepage H1 is not the logo (Shopify Dawn default). `[verify UI: theme]` [24de1308655a] [a4891c6c3426]
12. Validate schema on the 4 pages with a validator; confirm the facts match the fact sheet. [ccbc5be4692f] [618db29e2091]
13. Write the crawlability fix list (section 9) with owner and priority: blocked bots first, JS-hidden content second, indexing third, 404 redirects fourth, speed and schema last.

Rollback: keep a copy of the original robots.txt and Cloudflare settings before any edit; if a change exposes checkout or account paths, restore the copy.

### P2. Bot access policy (reconstructed from 04 and 03)

Goal: allow citation while honouring the brand's training choice. Preconditions: P1 step 1 done; brand's decision on training. Sources: 04, 03, 06 (card).

1. List each vendor's search bot and training bot from current documentation. `[web check]` [c722163c16a0]
2. Write robots.txt blocks: allow the search bots on public catalog and content paths; disallow training bots only if the brand chose that; keep the existing disallows for private paths.
3. If the store platform or CDN offers a toggle that separates indexing from training, prefer it over raw edits. `[verify UI]` `[web check: current tools]`
4. Deploy, re-fetch, re-run P1 step 6.
5. Never block everything as a defensive default; that forfeits the channel (R24).

Rollback: restore the saved robots.txt.

### P3. Brand gap analysis

Goal: a prioritised list of visibility, narrative, topic, format, mention and demand gaps. Preconditions: entity list, competitor list, prompt set (P6) or a tracker. Sources: 03, 07.

1. Write the entity list: brand, sub-brands, product lines, proprietary names, founder. Attach the topics and adjectives each should own. `[needs brand data]` [7ccc34f2e89e]
2. Record the SEO baseline: domain rating, referring domains, organic keywords and traffic, from whatever SEO tool is available. `[verify UI]`
3. Per priority platform, record mentions, citations, impressions and share of voice from the tracker, or from 3 runs of the prompt set by hand (P6). [5ce00206b4bc]
4. Apply the 3 filters: mentioned but not cited; competitor named and brand absent ("others only"); topic association. Without a tracker, tag each prompt-set row by hand with these 3 flags. `[verify UI]` [35cbd98861df]
5. Classify every finding into 1 of 6 gaps and label it fix, build or influence. [7ccc34f2e89e]
6. Score each by demand it could drive, credibility it supports, and citation odds. Pick quick wins first: a ranking page that needs a refresh; a listicle competitors are on. [9ffb85f5c826]
7. Repeat steps 3 to 5 for each named competitor to catch gaps missed.
8. Run 01's 4-part SEO competitor pass (R78): ranking keywords and traffic per competitor, winning URL types, sitemap categorised by page type, backlink profile. `[verify UI: SEO tool]` [0f0999fffc65]
9. Output the gap list; feed the content rows to P8 and P10, the mention rows to P11, the format rows to P13.

Check: every row has a gap type, a fix label and a source URL or prompt. Rollback: none; this is read-only.

### P4. Prompt audit and brand fact correction

Goal: know what engines say about the brand, and fix what is wrong at the source. Preconditions: fact sheet, priority platforms. Sources: 06, 02, 03.

1. On each priority platform, prompt: "Search the internet and tell me what you know about [brand]." Save the answer, the citations, the date, the model, and whether the session was logged in. [dcb1c3495233]
2. Run the same prompt in a logged-out or incognito session and in a logged-in session, 3 times each with varied wording; note whether citations appear at all. No citations means the answer may be from memory. `[verify UI]` [5786137d7326]
3. Mark every fact in the answer as correct, wrong, missing or competitor-favouring against the fact sheet. `[needs brand data]`
4. Open every cited source. For each: controlled by the brand (fix it now) or third party (log owner, find contact, request correction). [dcb1c3495233] [445fa90e4caf]
5. Publish the correct specific facts on the site first (About or Facts page, PDP, pricing, policies). [748700e7c99c] [b2f279ddb882]
6. Repeat the prompt for each competitor; list the sources driving their recommendations as mention targets for P11. [dcb1c3495233]
7. Ask each platform "what do you look for when recommending [category]?"; merge the lists into a criteria checklist; add only true, verifiable facts that match it to product copy and listings. [81e3b397ce06]
8. If a wrong fact persists after site and publisher fixes, run R75's wider distribution (founder video, third-party articles, review platforms, directories) and set the expectation that memory-based answers move slowly (02's 2-year example). [6b58426c3650]
9. Re-run monthly; log changes with model and date; a changed answer is evidence, not proof.

Rollback: none; corrections are additive. Never delete true but unflattering facts.

### P5. Question research and the AI filter

Goal: a trimmed list of buyer questions, each routed to a page type and a goal (click, mention, or transactional). Preconditions: catalog list, AI workspace with brand brief (P19). Sources: 04, 03, 07, 01, 06, 09.

1. Pull the brand's and competitors' paid-search terms; paste them into the assistant: "turn these into the questions people actually ask". [bf1d8a839388]
2. Add tail questions from sales calls, support tickets, chat logs and Reddit threads in the category. `[needs brand data]` [a43cf3acdd9f]
3. Run People Also Ask at depth for each core term; expand nested questions. `[verify UI: tool]` [9c1581aeb2a1]
4. Seed the keyword tool with 10 broad seeds and 5+ modifiers from the assistant (03's template: seeds and modifiers must not share words); run a matching-terms report. `[verify UI]` [caec8fa7e6e5]
5. Trim by hand: keep only questions a real buyer would ask about products the brand sells. [847055f1a547]
6. For each survivor, run it on 2 to 3 surfaces; note the cited page types and domains (R60). `[web check]` [a082ffa8e1fc]
7. Apply BID, then the AI filter: if the Overview fully answers it, mark the goal "mention" or move to a transactional or tool variant. [f51f401ddf5f] [3a369bfc1c08]
8. Route: transactional to PDP or category; short FAQ (5 max) to the commercial page; full topics to a guide; comparison prompts to a comparison page. [370b7ebbfabd] [04b6ed95b92b]
9. Export as CSV: question, source, intent, page type, goal, cited domains, owner.

Check: no row without an intent and a page type. Rollback: none.

### P6. Prompt test set and baseline

Goal: a fixed set of questions with a repeatable share-of-voice baseline per platform. Preconditions: P5 output, priority platforms. Sources: 04, 03, 02, 05.

1. Select 100 to 200 questions from P5 across intents: category "best X", comparison, fit and use case, brand questions, price and policy. Freeze the list. [0408383723f2] [f758425ed01b]
2. For each priority platform, run every question 3 times, in the mode buyers use (logged in where possible; note it). Record: date, platform, model, mode, brand named (yes/no), brand cited (yes/no), competitors named, cited URLs, answer format (text, list, table, shoppable card). `[verify UI]` [f85af788af43] [5786137d7326] [536f2c6edb07]
3. If a tracker is used, load the same list and export the same fields; note that trackers run logged out (05). [b78f1ae27412]
4. Compute per platform: share of runs naming the brand; share citing the brand; share naming each competitor; top cited domains. Do the arithmetic in code, not in the model.
5. Let it run 2 weeks before any intervention to see baseline variance. [0408383723f2]
6. Save as the baseline in the visibility report (section 9).

Check: every row has 3 runs per platform. Rollback: none.

### P7. Control-group experiment

Goal: prove 1 tactic moved share of voice. Preconditions: P6 baseline, 1 tactic ready. Source: 04.

1. Split the prompt set into test and control (04: 100 and 100), matched by intent. [0408383723f2]
2. Leave control untouched for the whole test.
3. Apply 1 tactic to the test group only (Reddit answers only, or 1 video only, or 1 disclosed placement only, or 1 page rewrite only).
4. Wait about 2 weeks; re-run P6 step 2 on both groups.
5. Compare the change in the test group's share of voice against the change in control over the same window.
6. Adopt the tactic as a rule only after the same result appears again on a rerun or a second matched set.
7. Record the design, dates, and both curves in the visibility report.

Rollback: if the tactic is a page change and the test group falls while control holds, revert the page from the saved copy.

### P8. Page rewrite for citation (PDP, category page, buying guide)

Goal: a page an engine can lift a correct answer from. Preconditions: fact sheet, P5 rows for this page, live-answer check (R60). Sources: 01, 03, 07, 06, 08, 09, 05, 04.

1. Confirm intent match: a transactional prompt gets a page where the product can be bought; a research prompt gets a guide. [ea6702f063e4]
2. Set 1 primary buyer phrase for the title tag, H1 and first sentence, in the buyer's words (R39). [04b6ed95b92b] [f587896fb244]
3. Write the first fold to pass the 2-second test: what it is, who it is for, what to do next; CTA above the fold; real product photo. [71181984bc10]
4. Open with the direct answer: 20 to 50 words under a question-shaped heading, then a TL;DR of key facts (materials, sizing, use case, price range, shipping) above any decorative section. [50fb70d1a21f] [10e99e650616] [5da2c2bb06ad]
5. Structure the body as atomic H2 sections, each opening with its answer, each readable alone, 1 idea per paragraph, named entities, declarative sentences. [08fd8b80c5a7] [79e59016f274] [cf7bae2b5009]
6. Category page: add a short comparison table of the products or options near the top, and cover the sub-questions the prompt fans into (who it suits, differences, care, price bands). [8c2682d22767] [a227df367635]
7. Buying guide: 60% to 70% capsules, the rest prose; 1 or 2 tables; original data or a first-hand result; linked sources for every external fact; FAQ at the end. [50fb70d1a21f] [c8d59fd79d48] [2b192a421dcf]
8. PDP: specs, materials, care, sizing, shipping and returns in plain fact blocks; FAQ of 5 max from P5; reviews that mention the product; schema facts equal to page facts. [ea6702f063e4] [ddeff4f4d862] [618db29e2091]
9. Run the information-gain test: name 1 thing on the page nobody else says. If none, add a first-hand detail or real data before publishing. [b0dba8938d4e] [2b192a421dcf]
10. Reading check: every sentence 1 idea; nothing needs 2 reads; below tenth grade; digits; no em dashes. Every claim traced to the fact sheet.
11. Internal links to the money page and from the money page to the guide. Meta description under 150 characters. [bc9c4929973d] [a024bd850f13]
12. Publish, request indexing, add to the refresh calendar (2 months), and add the page's prompts to the test set if not there.

Check: run the section 5.2 checklist; 01's rule of thumb is about 90% of items ticked before calling it ready. Rollback: keep the previous version; revert if conversion drops in 07-LPG or 09-CRO monitoring.

### P9. Comparison page

Goal: an honest head-to-head that gives the engine reasons to recommend the brand. Preconditions: approved competitor claims, legal review rule. Sources: 06, 05.

1. Pick 3 to 4 competitors larger than the brand that appear in the category's answers. [8c2682d22767]
2. Decide deliberately who to name; naming a competitor can lift them too (05). [9efc84d55e51]
3. Build the table first: features, materials, price, shipping, warranty, best for. Every cell verifiable. `[needs brand data]`
4. Write pros and cons for both sides; state plainly who each is better for.
5. Table near the top; answer-first summary above it; FAQ at the end.
6. Legal check on comparative claims for the market. `[needs brand data: review process]`
7. Refresh every 2 months; prices and specs drift fastest.

Rollback: unpublish if a claim cannot be verified on challenge.

### P10. Content refresh and sleeper pages

Goal: earn citations fastest by refreshing pages that already have authority. Preconditions: top-pages report with traffic change and referring domains. Sources: 03, 07, 06.

1. Sort top pages by traffic decline; keep pages with meaningful referring domains. `[verify UI]` [4e6f7e7f1aa7]
2. Drop pages whose real problem is thin links; a rewrite will not fix them.
3. For each keeper: update facts, prices, specs, examples, recommendations; add or update the answer-first opening; add a table if the format that wins is a comparison. [e3c82eeb7e04] [9edf8483abdc]
4. Move the visible "last updated" date only because the content changed. [984dbd1fc95a]
5. Request indexing; add the page's prompts to the test set.
6. Calendar: high-intent pages every 2 months; nothing past 6 months untouched.

Rollback: keep the previous version.

### P11. Mention target list and tier-1 outreach

Goal: a worked list of third-party pages that already feed the category's answers. Preconditions: P4 competitor sources, P6 cited domains. Sources: 02, 03, 06, 07.

1. Collect cited domains and URLs from P6 and the competitor prompts in P4. [dcb1c3495233]
2. Add listicles and comparisons that omit the brand: content search `title:best` or `title:versus` plus category terms minus the brand name; filter by referring domains. `[verify UI]` [2037fd15a632]
3. Add the listicles that show in "best [category]" on AI Overviews and AI Mode. [61e62cdd75c6]
4. Remove competitor-owned pages. [07e818713c36]
5. For each target: owner, contact (a contact-finding tool such as Hunter, `[web check: terms]`), placement type (editorial, affiliate, sponsored), cost if any, disclosure requirement, status. [61e62cdd75c6]
6. Pitch with a specific, true case for inclusion; offer product for testing where the publisher tests. Never ask to remove competitors.
7. Paid options go to legal and budget review; accept only labelled sponsored or affiliate placements (R65). `[needs brand data]`
8. Track responses; re-run P6 4 to 6 weeks after a placement lands.

Rollback: none.

### P12. Reddit and community participation

Goal: a few genuine, disclosed, useful answers in threads engines already cite. Preconditions: a real employee willing to post under their name; subreddit rules read. Sources: 04, 05, 06, 03, 02.

1. From P6, list Reddit and forum URLs that appear in answers for the priority prompts. Check thread age and whether it is locked. [28b9ca1fa247]
2. Pick 5 to 10 subreddits from 2 angles: where the buyer persona already reads, and where the product's problem is discussed. Read each one's self-promotion rules. `[web check]` [b78f1ae27412] [4e8ff5bc6f43]
3. Set keyword alerts for category terms (06 uses F5Bot). `[web check: tool]`
4. Build karma with helpful, non-brand answers first. [4e8ff5bc6f43]
5. When a thread fits, answer from a named account stating employer, with 1 useful point; lead with an open-ecosystem angle (how the product works with what the community already uses) rather than "we are better". No links unless asked. [c3a578a68afc] [9efc84d55e51]
6. Never use more than 1 account per person, never upvote yourself, never auto-post. [c3a578a68afc]
7. Watch cited threads for negative comments and respond early and honestly. [9efc84d55e51]
8. Expect 30 to 45 days before ChatGPT picks it up (05, 1 case); log any citation in the spreadsheet (R94).

Rollback: a moderator can delete anything; do not fight it.

### P13. YouTube search-hit videos

Goal: video that ranks for a steady search term and is cited. Preconditions: ability to make or commission video. Sources: 03, 07, 06.

1. Find search-hit topics: check which YouTube watch URLs rank in the top 3 for the brand's niche terms, or which category prompts already cite YouTube. `[verify UI]` [1af9f13ebe90] [2130f7b978ac]
2. Choose the format that already ranks (tutorial, review, "best of").
3. Title: exact keyword. Description: keyword in the first 2 lines, real summary. Chapters via timestamps. Say the keyword aloud in the first and last 10 seconds. Keyword in the video and thumbnail file names (06). [224d5f463421] [5f0da09a8820]
4. Information value over polish; real product on camera (ecomOS: real product photos and footage where accuracy matters).
5. Publish a companion page per video and link both ways; link the channel from the site and in Organization schema. [5f0da09a8820] [618db29e2091]
6. If commissioning a creator "best of" video, the sponsorship is disclosed on screen and in the description. [61e62cdd75c6]
7. Add the video's target prompts to the test set.

Rollback: none.

### P14. Reviews, directories and NAP

Goal: consistent facts and honest reviews on the platforms engines read. Preconditions: fact sheet, review platform access. Sources: 06, 01, 02.

1. Choose review platforms from P6's cited domains and from where buyers already post. [77505b864e04] [138fd5c7b44a]
2. Set up the neutral post-purchase request (17-CXP owns the flow): fit, quality, limitations, own words, no incentive, no condition. [77505b864e04]
3. Complete Google Business Profile and claim relevant directories; description aligned to the criteria list from P4 step 7, facts from the fact sheet. `[verify UI]` [f91363a42603]
4. Make NAP and key facts character-identical everywhere; re-audit after any change. [f91363a42603] [3514f3eb2279]
5. If managing many listings, a citation service is acceptable; bulk cheap sellers are not. `[web check: pricing]` [3514f3eb2279]
6. Respond to reviews; separate service fixes from any visibility effect. [77505b864e04]

Rollback: none.

### P15. Press release for real news

Goal: a syndicated, citable statement of a true fact. Preconditions: a real announcement; PR and legal sign-off. Sources: 02, 06 (card guardrails).

1. Confirm the news is real: launch, award actually won, sponsorship, original research with a described method. [8a54ade0eeff] [5c9bc91bc0b2]
2. Put the exact target phrase in the title, subheading and first sentence. [8a54ade0eeff]
3. If it reports research, state method, sample, dates and who paid. Never title a promotional ranking as an "industry report". [5c9bc91bc0b2]
4. Distribute via a wire service; record cost and syndication outlets. `[web check: service names and pricing]`
5. Re-run the relevant prompts after 4 weeks.

Rollback: issue a correction release if a fact was wrong.

### P16. Measurement setup

Goal: all 3 pillars live before content work starts. Preconditions: GA4 admin, survey platform, log or CDN access. Sources: 03, 07, 05, 04.

1. GA4: Admin, Data Display, Channel Groups; copy the default group; add "AI traffic" with a regex on AI referrer hostnames (current list from the web); place it above Referral in the order; verify in Reports, Acquisition, Traffic Acquisition. `[verify UI]` `[web check: hostnames]` [c2ae662a8e4f]
2. Note the undercount: no-referrer links on paid ChatGPT, desktop apps, Grok. Record the caveat in the report template. [c2ae662a8e4f]
3. Survey: add "How did you hear about us?" at checkout or post-purchase with AI assistant, ChatGPT, Perplexity, AI search (Google AI Overviews) as visible options, plus free text. `[verify UI]` [3d817167591c] [e07344cb96f8]
4. Bot logs: enable server log access or a bot-analytics integration; tag citation bots and training bots separately; list the top 20 pages fetched by citation bots monthly. `[verify UI]` [8f0d6e616976]
5. Search Console and Bing Webmaster Tools: confirm access; note the Bing AI performance tab. `[verify UI]` [4df3dc92ffaf]
6. Conversion: build a saved report comparing AI channel sessions, conversion rate and revenue against organic. Arithmetic in code. [d3293f344c01]
7. Citation log: the spreadsheet from R94 (query, platform, date, URL, named, cited).
8. Prompt set baseline: P6.

Check: each pillar returns data within 2 weeks. Rollback: channel group changes are non-destructive; remove the channel if it mis-buckets.

### P17. Monthly visibility report (reconstructed from 03, 01, 04, 02)

Goal: 1 page that shows direction, not vanity. Preconditions: P16 running, P6 baseline.

1. Re-run P6 (3 runs per prompt per platform). Compute share of voice, citation share, top competitors named, top cited domains, by platform. [0d40ada60dfc]
2. Report mentions and citations as separate lines; flag "named but unlinked". [dc9263a72730] [311517f2c62e]
3. Prompt audit accuracy: count of wrong facts open, closed, new. [dcb1c3495233]
4. GA4 AI channel: sessions, conversion rate, revenue, versus organic; state the undercount. [c2ae662a8e4f]
5. Survey: share of responses naming an AI assistant. [990877b3d70c]
6. Bot logs: top fetched pages by citation bots; new pages appearing. [8f0d6e616976]
7. GSC and Bing: impressions, clicks, citations, cited queries, month over month. [4df3dc92ffaf]
8. Crawlability: bots blocked (target 0), JS-hidden blocks (target 0), AI-referred 404s (target 0). [64a695c65c71]
9. Mention targets: landed, pending, declined. Experiments: test versus control results.
10. Next month's single biggest gap and its fix.

Never report a raw citation count as the headline (R91).

### P18. Vendor vetting

Goal: a hire or no-hire on a GEO agency or tool with evidence. Preconditions: the vendor's proposal and case studies. Source: 02, 04.

1. Ask the 5 questions and 3 probes in R96 on a call; record answers verbatim. [5872777fb613] [3be904342c0a]
2. Ask for the case-study keyword list; split at a difficulty threshold; chart both bands; ask how the client performs now and whether revenue moved. [7cbba7101a4d]
3. Ask whether the platform generates content and how many pages the plan publishes. Hundreds is a no. [d6f727b1e8c0]
4. Ask which of section 3.10's tactics they use. Any yes is a no-hire.
5. For a tracker: list the surfaces tracked, prompt limits, run frequency, logged-in support, export format, price; compare against 2 cheaper options. [56c995c391df]
6. Write the vetting sheet (section 5.6) and the decision.

### P19. AI-assisted drafting workflow

Goal: draft fast without inventing anything. Preconditions: brand brief, fact sheet, P5 rows. Sources: 01, 04.

1. Create a project in the assistant; add the brand brief and fact sheet as files; add every research export as it is produced. `[verify UI]` [852d326e7cca]
2. Prompt for the capsule structure with topic, audience and goal; cap the assistant's clarifying questions to what is useful. [100d6edb5ef3] [847055f1a547]
3. Review the proposed sources; reject anything not real or not relevant.
4. Inject first-hand detail the assistant cannot know before the draft. [2b192a421dcf]
5. Draft in an editable canvas; edit by hand; check every fact against the fact sheet; check every link works. [c500104bcbec]
6. Convert any generated illustration to WEBP; use real product photos wherever accuracy matters. [ba67965b3332]
7. Paste into the CMS; fix formatting; add real internal links; write the meta description. [a024bd850f13]

Rollback: discard the draft; never bulk-publish.

### P20. See the engine's own searches for a prompt

Goal: the literal sub-queries an engine ran, to check topic coverage and borrow phrasing. Preconditions: browser with developer tools. Source: 02. `[verify UI: undocumented technique, may break at any time]`

1. Perplexity: run the prompt; read the searches shown in the interface.
2. ChatGPT: send the prompt; wait for "searching the web"; open Inspect, Network tab; copy the conversation ID segment of the URL; paste into the Network filter; refresh; open the matching entry; open Response; search for "queries". [f587896fb244]
3. Record the sub-queries next to the prompt in P5. Use for coverage and phrasing (R2, R39), not as keyword targets (R57).
4. Repeat periodically; fan-out changes. [dd5f18c44b74]

## 5. Diagnostic checklists

Written so a worker can run each one without reading the sources. Each row: what to check, how, good, bad, fix, source.

### 5.1 Technical crawlability audit

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| robots.txt AI bot rules | Open /robots.txt; search for GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, Google-Extended, PerplexityBot `[web check: names]` | No Disallow on search or citation bots | Any Disallow on them, or `User-agent: *` with `Disallow: /` | Edit robots.txt per P2; re-fetch | 03, 07, 06 |
| Training vs search split | Compare each vendor's training bot with its search bot | Search bots allowed; training per brand choice | Both blocked together | Split the rules (P2) | 04, 03 |
| Cloudflare AI-bot feature | Cloudflare dashboard, bot settings `[verify UI]` | Off, or set to allow citation bots | On by default, rewriting robots.txt | Turn off or edit managed rules; re-fetch | 03, 07 |
| Firewall, WAF, bot-blocking apps | Review rules for the same user agents `[verify UI]` | No AI bot rules | Bot rule blocks them | Whitelist search and citation bots | 06 |
| Live bot access | Free bot-access checker on home, PDP, category, guide `[web check: tool]` | All pass | Any fail | Trace the failing layer (robots, CDN, WAF) | 06 |
| JavaScript-only content | Disable JS, reload the 4 pages | Title, H1, H2s, copy, specs, price, FAQ, reviews visible | Any of those missing | Server-side render or pre-render those blocks | 03, 06 |
| Page speed | Lighthouse on the 4 pages `[verify UI]` | Scores near 100; Core Web Vitals pass | Failing CWV | Hand to 08-SPD | 03, 01 |
| Heading hierarchy | View headings on the 4 pages | 1 H1 naming the offering; H2 sections; H3 subsections | Logo as H1; multiple H1s; no H2s | Fix theme template | 01, 03 |
| Google indexing | GSC Sitemaps status; `site:domain` `[verify UI]` | Success; discovered count proportionate; PDPs and collections indexed | Errors; low count; key pages missing | Fix sitemap, canonical, noindex; resubmit | 06, 01 |
| Bing indexing | Bing Webmaster Tools sitemap `[verify UI]` | Submitted, success | Not submitted | Submit | 06 |
| Schema validity and accuracy | Validator on the 4 pages | Valid; facts equal to page and fact sheet | Errors; plugin-invented facts | Fix and validate | 01, 03, 06 |
| AI-referred 404s | GA4 AI channel, landing page = 404 | None | Repeat visits to a made-up URL | 301 to closest real page | 03 |
| Help content location | Inspect URL of FAQ or help centre | Subdirectory, cross-linked | Subdomain, isolated articles | Move to a subdirectory and cross-link (R33) | 04 |
| Internal links | Crawl guides and FAQs | Each links to its money page and back | Orphan guides | Add links where they fit | 01 |
| llms.txt | /llms.txt | Absent or present; either is fine | Engineering hours spent on it | Deprioritise | 03, 02 |
| Re-test trigger | Change log | Audit re-run after every CDN, theme, app or platform change | No re-run | Add to the change checklist | 06 |

### 5.2 Page content audit (PDP, category page, buying guide)

Run per page. Rule of thumb from 01: about 90% ticked before the page is called ready.

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Intent match | Compare the target prompt with the page type | Transactional prompt lands on a buyable page; research prompt on a guide | Article for a buying prompt, or PDP for a research prompt | Change the page type or the target | 01, 03 |
| 1 primary buyer phrase | Title tag, H1, first sentence | Same phrase, buyer's words | Trade jargon, or 3 different phrasings | Rewrite title, H1, opener | 01, 02, 05 |
| 2-second first fold (PDP, category) | Load without scrolling | What, for whom, next action, CTA visible | Clever tagline, no CTA | Rewrite first fold | 01 |
| Answer first | Read the first 50 words | Direct 20 to 50 word answer under a question heading, then TL;DR facts | Marketing build-up first | Move the answer up | 01, 03, 06, 07, 08, 09 |
| Atomic sections | Read each H2 alone | Makes sense alone | "As mentioned above", "this item" | Rewrite the opener of each section | 03, 07 |
| Entity-rich, declarative | Sample 10 sentences | Named product, material, competitor; 1 idea each; no sentence needs 2 reads | "This tool", "many users", compound sentences | Simplify | 03, 07 |
| Reading level | Readability tool | Below tenth grade | Above | Shorten sentences and words | ecomOS |
| Format matches what wins | Compare with the live answer's cited pages | Same type (table, list, category grid) | Different type | Add a table or restructure | 04, 03, 06 |
| Topic coverage | List the prompt's sub-questions; tick which the page answers | All buyer sub-questions covered on this page or a linked page | Head keyword only | Add sections or a linked guide | 03, 07, 01 |
| Hard facts and evidence | Scan for numbers, quotes, data, linked sources | At least 1 real original data point; sources linked | Vague claims, no links | Add real data or a first-hand result | 06, 01, 09, 08 |
| Information gain | Ask "what does this say that no competitor page says" | At least 1 thing | Nothing | Add first-hand detail | 04, 01 |
| Claims vs fact sheet | Check every claim | All in the brand record | Any unverifiable claim | Remove it | ecomOS |
| FAQ (PDP, category) | Count questions | 5 or fewer, from real buyer questions | 10+ questions padding the page | Move extras to a guide | 01, 06 |
| Buying guide capsule share | Estimate share of sections in capsule form | 60% to 70% | Under half | Convert sections | 01 |
| Freshness | Last real content update | Within 2 months for high-intent pages; never past 6 months | Older | Refresh with substance (P10) | 07, 06, 03 |
| Date honesty | Compare date change with content diff | Date moved only when content changed | Date-only edits | Revert; prohibited | 03, ecomOS |
| Schema facts | Compare schema with visible copy | Equal | Different | Fix schema | 06, 01 |
| Real photos | View images | Real product photos; WEBP | Stock or generated product images where accuracy matters | Replace | 01, ecomOS |
| Internal links | Check in and out | Guide to money page and back | None | Add | 01 |
| Meta description | Count characters | Under about 150, has the phrase | Long or missing | Rewrite | 01 |
| AI-written check | Ask the writer | Human-edited, first-hand detail injected, sources verified | Unedited draft | Edit before publishing | 01, 04 |

### 5.3 Brand mention audit

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Cited domains for priority prompts | P6 export or tracker cited-domains view | Brand's site plus sites the brand is on | Only competitors' sources | Build the mention target list (P11) | 03, 06, 02 |
| Tier 1 presence | For each cited listicle or comparison: is the brand on it | Present, accurately described | Absent | Outreach; disclosed placement only | 03, 07, 06, 02 |
| Competitor-driving sources | P4 competitor prompts | Brand present on the same sources | Absent | Pursue mention there | 06 |
| Tier 2 presence | Cited Reddit or forum threads | Real, disclosed, helpful answer present | Absent, or a spammy one | P12; delete nothing you cannot stand behind | 04, 05, 06 |
| Thread viability | Thread age, locked, subreddit rules | Recent, open, brand mentions allowed | Old, locked, banned | Skip; find another | 02 |
| Sentiment in cited threads | Read them | Neutral or positive | Negative with traction | Respond early, honestly | 05 |
| Tier 3 owned | YouTube, podcast, LinkedIn | Present, on topic, facts consistent | Absent or stale | P13, R74 | 03, 07, 06 |
| YouTube in answers | Does the category prompt cite video | Brand's video appears | Competitor or creator videos only | Make or commission a search-hit video (disclosed) | 03, 07, 06 |
| Review platforms in answers | Which review sites the answers cite | Brand present with honest reviews | Absent or low rating | Honest collection (P14); fix the product problem | 02, 06 |
| Directory and NAP consistency | Compare all listings with the fact sheet | Identical | Any mismatch | Correct | 06, 01 |
| Wrong facts in third-party pages | P4 cited sources | None open | Open items | Correction request; log | 03, 02, 06 |
| Paid placement disclosure | Review every paid mention | Labelled sponsored or affiliate | Presented as editorial | Withdraw or relabel | ecomOS, 02 |
| Self-published listicles | Search Medium, Substack, LinkedIn, Quora for brand "best of" lists | None that hide competitors | Present | Remove; prohibited | ecomOS, 06 |
| Mention trend | Monthly mention count per platform | Stable or rising | Sudden drop | Find which page stopped mentioning; re-outreach | 03, 01 |

### 5.4 Prompt visibility test

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Prompt set frozen | 100 to 200 questions saved with intent tags | Yes | Ad hoc prompts | Freeze it (P6) | 04 |
| Runs per prompt | Count | 3 or more per platform per period | 1 | Re-run | 03, 04 |
| Mode logged | Each row has model, date, logged-in state, search on/off | Yes | Missing | Add fields | 02, 05 |
| Search actually fired | Citations present; incognito vs logged-in comparison | Consistent citations | None or wildly inconsistent | Mark as memory-based; fix third-party sources | 02 |
| Named vs cited | Separate columns | Both tracked | Only "cited" | Add "named" | 02, 03 |
| Competitor names | Column per competitor | Tracked | Missing | Add | 03 |
| Cited URLs | Column | Captured every run | Not captured | Add | 05 |
| Answer format | Text, list, table, shoppable card | Logged | Missing | Add | 04 |
| Arithmetic | Share of voice computed in code | Yes | Computed by the model | Recompute | ecomOS |
| Baseline period | 2 weeks before any change | Yes | Changes started early | Extend baseline | 04 |
| Control group | Untouched half for any experiment | Yes | None | Split (P7) | 04 |
| Replication | Result seen twice | Yes | Once | Rerun before adopting | 04 |
| Persistence | Same prompts re-run monthly, citation log | Citations hold | Citations decay | Refresh the page; log | 05 |

### 5.5 Measurement setup

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| GA4 AI channel | Channel group exists with current hostnames `[web check]` | Sessions appear | None, or AI in Referral | Fix regex and order | 03, 07 |
| Undercount noted | Report template | Caveat stated | Numbers presented as complete | Add caveat | 03, 04 |
| HDYHAU survey | Checkout or post-purchase | AI options visible up front; free text | Under "Other" or absent | Move up (P16) | 05, 03 |
| Bot logs | Server logs or integration | Citation bots and training bots separated; top pages listed | None | Enable | 03, 07 |
| GSC and Bing | Access confirmed; Bing AI performance tab read | Monthly read | Not read | Add to P17 | 01 |
| Conversion comparison | AI vs organic conversion and revenue | Report exists; arithmetic in code | None | Build | 04, 03 |
| Citation log | Spreadsheet | Maintained | None | Start | 05 |
| Prompt baseline | P6 done | Yes | No | Run | 04 |
| Direction not target | Report | Month-over-month trend | Fixed target promised | Remove the promise | 01 |

### 5.6 Vendor vetting

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| "How is GEO different from SEO" | Ask | Plain answer: mostly SEO plus mentions and format | Hype, "entirely new discipline" | Yellow flag | 02, 04 |
| Operating history | Ask when they started | Pre-2018 in optimisation | Founded after ChatGPT launch with no prior SEO | Yellow flag | 02 |
| Case studies then and now | Ask how those clients perform today | Held or grew; revenue shown | Only launch-time charts | Red flag | 02 |
| Keyword-band audit | Split their keywords at a difficulty threshold `[verify UI]` | Hard keywords hold | Hard keywords declining under a rising total | Red flag | 02 |
| Content volume | "Will you publish hundreds of posts?" | No | Yes | Red flag | 02 |
| Content generator | "Does your platform generate content?" | No | Yes | Red flag | 02 |
| Plain English | "Explain your method" | Clear | Cannot | Disqualify | 02 |
| Grifter probes | llms.txt, AI info page, chunking everything | Measured, low priority | Enthusiastic yes | Yellow flag | 02 |
| Off-site stance | Affiliates, listicles, reviews, video | Has a plan | None | Yellow flag | 02 |
| Prohibited tactics | Walk through section 3.10 | None used | Any used | No hire | ecomOS |
| Reporting | What KPIs | Share of voice, mentions vs citations, revenue | Raw citation counts | Change the contract or walk | 02 |
| Tool pricing | Compare with 2 cheaper trackers | Commodity price | Premium for "mystery" | Buy the cheaper one | 04 |

## 6. Thresholds and benchmarks

Confidence: "3 sources" means 3 independent evidence bases; 03 and 07 share Ahrefs' data and count as 1. "Vendor only" means the number comes from a vendor's unpublished study. "Unsourced" means the presenter gave no origin. "Example" means 1 company's result, never a target.

| Value | Condition | Source | Confidence |
|---|---|---|---|
| 70% to 80% of GEO effort on sound SEO | Program allocation | 02; 01 says about 80% | 2 sources, both opinion |
| Direct answer of 20 to 25 words, up to 50 | Capsule under a question heading | 01 | 1 source, unnamed study |
| Direct answer of 2 to 4 sentences plus TL;DR | Top of every important page | 06 | 1 source, opinion |
| 60% to 70% of a guide in capsule form | Long buying guide | 01 | 1 source, heuristic |
| Over 44% of AI citations from the first third of the page | Any page | 06 | Unsourced |
| FAQ on commercial page: 5 max | PDP, category | 01 | 1 source |
| Meta description under about 150 characters | Any page | 01 | 1 source |
| About 90% of page checklist ticked | Page ready | 01 | 1 source |
| Refresh high-intent pages every 2 months | Cadence | 06 | 1 source |
| Nothing untouched past 6 months | Cadence | 07 | Vendor only |
| Word count vs citation correlation 0.04; 53.4% of cited pages under 1,000 words | 174,000+ AI Overview citations | 03, 07 | Vendor only |
| Cited content about 25.7% fresher than organic | Same study | 03, 07 | Vendor only |
| 89.7% of ChatGPT top-cited pages updated in 2025; 76% in last 30 days | ChatGPT | 03, 07 | Vendor only |
| 43.8% of ChatGPT citations are listicles or comparisons | ChatGPT | 03, 07 | Vendor only |
| 9 to 11 fan-out sub-queries per prompt, up to 28; 420 in 1 deep-research run | Assistant search | 03, 07 (citing Seer, Nectaf) | Vendor relay, unlinked |
| 1 to 3 sub-queries per prompt | Assistant search, normal mode | 02 | 1 source, observation |
| Over 95% of fan-out sub-queries have zero search volume | Keyword planning | 03 | Vendor only |
| 76% of AI Overview citations from Google top 10; revised near 38%; 14% not in top 100 | Overlap | 03, 07 | Vendor only, self-revised |
| ChatGPT citations about 35% overlap with Google; Perplexity about 70% | Overlap | 04 | Vendor only, unnamed study |
| Perplexity citations from Google top 10: 28.6%; ChatGPT 8% to 10% | Overlap | 03 | Vendor only |
| 14% top-50 domain overlap across AI Overviews, ChatGPT, Perplexity | Platform choice | 03 | Vendor only |
| 13.7% citation overlap AI Mode vs AI Overviews | Platform choice | 03 | Vendor only |
| 30% to 40% cross-engine playbook overlap | Platform choice | 05 | 1 source, heuristic |
| Claude cites about 5 times less than ChatGPT | Platform choice | 05 (unnamed studies) | Unsourced |
| Over 90% of AEO-driven new users via ChatGPT | Prosumer SaaS | 05 | Example |
| About 28% of AI mentions carry a link (51.6% Perplexity, 36.8% AI Mode, 26.9% ChatGPT, 10.7% AI Overviews) | Reporting | 03 | Vendor only |
| Branded mention correlation 0.664; on highly linked pages 0.7 | 75,000 brands | 03, 07 | Vendor only |
| YouTube mention correlation 0.737 with ChatGPT visibility | Same study | 03, 07 | Vendor only |
| YouTube 5.6% of AI Overview citations | Format | 03 | Vendor only |
| Median domain rating 90 for ChatGPT top-cited pages | Authority | 03 | Vendor only |
| About 5.9% of 140 million sites block GPTBot | Crawlability | 03, 07 | Vendor only |
| AI sends visitors to 404s 2.87 times more than Google; about 1% of ChatGPT clicks 404 | Crawlability | 03 | Vendor only |
| Over 45% of AI Overview citations change on refresh, about every 2 days | Cadence | 03 | Vendor only |
| AI referral about 0.25% of site traffic; Google sends about 210 times more | Volume | 03 | Vendor only |
| AI traffic grew 9.7 times in a year; ChatGPT up 85% since January | Volume | 03, 07 | Vendor only, undated |
| Ahrefs: 0.5% of visits, 12.1% of sign-ups, 23 times organic conversion; about 3% of conversions self-reported | June 2025 | 03, 07 | Example |
| Webflow: 6 times conversion vs Google; about 8% of sign-ups from LLMs | B2B SaaS | 04 | Example |
| Gamma: ChatGPT referrals grew about 8 times from under 1% of traffic | Consumer SaaS | 05 | Example |
| Vercel about 10% AI conversion; Tally +$1M ARR | Relayed anecdotes | 03 | Unsourced |
| AI search traffic converts 4 to 10 times more | General | 06 | Unsourced |
| 58% CTR drop on the number 1 result under an AI Overview | December 2025 | 03 | Vendor only |
| 60% of Google searches end without a click | General | 08 | Unsourced |
| AI Overviews on about 21% of keywords, 58% of question queries; 99.9% informational | Keyword filter | 03, 07 | Vendor only |
| Gemini and Perplexity repeated planted fakes in 37% to 39% of answers; ChatGPT under 7%, cited official FAQ 84% | 1 planted-brand test | 03 | Vendor only, 1 test |
| About 1 in 20 pages drive about 85% of traffic | Budget concentration | 04 | Vendor only |
| Refresh top 5 to 10 pages in week 1 | Starter plan | 03 | 1 source |
| 10% to 12% of cited content AI-detected; 8% detector false positives | AI content | 04 | Vendor only, described method |
| About 100 to 1,000+ posts in weeks precedes rank-and-tank; 2 to 3 year recovery | Scaled content | 02 | 1 source, observation |
| Keyword difficulty above 30 as the "hard" band | Case-study audit | 02 | 1 source, tool-specific |
| Prompt test set 200, split 100 and 100; 2 weeks before and after | Experiment | 04 | 1 source, example |
| 3 runs per prompt per platform | Baseline | This playbook, from R4 | Reconstructed |
| Track about 3 surfaces; about 60 trackers exist | Tooling | 04 | 1 source |
| Reddit: as few as 5 genuine comments | Community | 04 | 1 source, anecdote |
| 5 to 10 subreddits | Community | 06 | 1 source |
| Average cited Reddit post over 1 year old; plan 1 to 2 years | Community | 06 | Unsourced |
| Reddit to ChatGPT citation lag 30 to 45 days; Perplexity next day | Community | 05 | 1 case |
| 4 to 5 Reddit references per answer | Community | 05 | 1 source, estimate |
| Reddit tactic "4 to 5 times visibility" | Community | 06 | Unsourced |
| Compare against 3 to 4 larger competitors | Comparison pages | 06 | 1 source |
| At least 3 industry publications | Mentions | 06 | 1 source |
| Niche listicle inclusion $50 to $300 | Paid placement, disclosed only | 02 | 1 source, anecdote |
| Press release about $80 single; about $6 each at bulk; "a couple hundred dollars" | Wire services | 02, 06 | 2 sources, stale prices |
| Local citations about $3.20 each, about $2 at bulk | Directory service | 01 | 1 source, stale |
| Reporter platform: 5 published of 12 pitched | Expert citations | 01 | Example |
| Training-data correction took about 2 years to move partway | Memory-based facts | 02 | 1 case |
| ChatGPT searches live for about 60% of queries | Retrieval vs memory | 05 (unnamed study) | Unsourced |
| "10 documents can poison an LLM" | Gray-hat basis | 06 | Unsourced; tactic prohibited |
| $10 to $20 per review to staff | Reviews | 06 | Prohibited |
| Lighthouse near 100 | Speed | 01 | 1 source, own site |
| Chat query about 25 words vs search about 6 | Tail size | 04 (third party) | Relayed |

## 7. Where sources disagree

Each conflict: what each side says, when each is right, what the agent should do. Nothing here is averaged into a rule the sources did not state.

**C1. Do AEO tactics work at all, or should a brand "just write good content"?**
Side A (platform line, relayed in 04): ChatGPT's head of product told the podcast host not to worry about AEO and to create quality content; the system will surface it. 02 is also skeptical of the whole vendor category's measurement claims and says most of GEO is plain SEO. 08 says the shift is gradual. Side B (04, 03, 05, 06, 01, 07): specific tactics move citations: mentions, format matching, freshness, Reddit answers, video, crawler access. 04 reads the platform line as "don't spam us", not "optimisation has no effect", and points to Webflow's results (SaaS). When each is right: quality content and crawlability are common ground, and both sides accept them. The disputed part is off-site and format tactics, and no source proves them with a control group except 04's method, which he describes but does not report results for. What the agent should do: run the common ground first (R13, R14, R36 to R47), treat every off-site tactic as a hypothesis, and only call it proven for this brand after a P7 test replicates. Never sell a client on the tactics as established.

**C2. Domain authority matters vs new sites can out-cite big ones.**
03: median domain rating of ChatGPT's top-cited pages is 90; most AI Overview citations already rank in Google's top 10. 04 and 05: the citation layer has no authority gate today; a new company can be cited within days via a thread, a video or a specific answer; 05 calls it a level playing field that will close. When each is right: head prompts ("best [category]") go to authority; tail and specific prompts are open. What the agent should do: a small brand works the tail (R17), mentions (R8) and specific unanswered questions (R55, R56); it does not budget to win the head prompt in month 1. Re-check quarterly whether the "open field" is closing (05's own prediction).

**C3. Length does not matter vs long buying guides.**
03 and 07: 0.04 correlation between word count and citation; 53.4% of cited pages under 1,000 words; stop lengthening pages. 05: go deep on comparative, reasoned angles, not thin copy. 01's capsule guide is long-form by nature; the common ecommerce habit is long guides for topical authority. When each is right: 03's finding is about being cited, not about ranking; 03 itself says coverage of the fan-out (R2) still matters. Depth of coverage and word count are different things. What the agent should do: write to the length the topic's sub-questions need, in capsules, and stop. Never add words for authority. If a page must be long to cover the topic, it is long; if not, it is not.

**C4. Broad informational content is wasted vs topical authority and intent breadth.**
02: "what is X" content is wasted for most small and mid brands because Overviews answer it, and Google AI Mode links to product and category pages more; exception for brands with real authority and a new point of view. 03's AI filter says the same for click targets but keeps the query as a mention play. 09: span informational through transactional to have more entry points. 06: FAQs on every important page and PAA-driven content. When each is right: 02 for a small brand's budget; 09 and 06 for a brand that can afford breadth and wants mentions inside Overviews. What the agent should do: transactional and comparison pages first (R16); informational pieces only after the AI filter (R59) shows the Overview leaves a reason to click, or as a deliberate mention play with no traffic expectation.

**C5. Reddit is training-only vs Reddit is the most-cited source; and Reddit helps only on ChatGPT vs in general.**
05 says in one place that Reddit interventions mostly become training data (clicks go to Reddit, not to the site) and in another that Reddit is the most-cited source for ChatGPT; his card flags the tension as unresolved. 05 also says Reddit's influence is concentrated almost entirely in ChatGPT. 03 and 06 treat Reddit as heavily cited in general and as training data at once. 02 saw Reddit drop out of OpenAI's citations for a period. What the agent should do: treat Reddit as both, with citation behaviour that varies by platform and month. Check which platforms cite Reddit for the brand's own prompts (P6 cited domains) before investing; expect the benefit mostly on ChatGPT until the data says otherwise; never rely on 1 platform.

**C6. Incentivised reviews.**
06's video recommends $10 to $20 per review to staff and a QR review card at job completion. 06's own cards and mainstream platform policy say Google prohibits incentivised reviews and that policies must be checked. ecomOS prohibits incentivised, scripted or conditional reviews. What the agent should do: never incentivise; run the neutral request (P14); flag any vendor that proposes incentives.

**C7. Buying backlinks and bulk citations.**
01's presenter says everybody buys links in competitive niches and names agencies he has used; 01's card adds a sponsored or nofollow requirement the presenter never stated. 02 says paid listicle placement is effective and that he does not condone the newspaper-site version. Google's guidelines and conservative SEO practice prohibit paid links, with manual-action risk. ecomOS prohibits buying links. What the agent should do: no paid links; paid citation services that create real directory listings are acceptable (R72); flag any vendor proposing link buying.

**C8. Paid listicle placements.**
02, 06 and 04 all describe paying for listicle or affiliate inclusion as effective and often necessary; 02 draws the line at undisclosed "top rated" placements in news sites and notes jurisdiction-specific disclosure rules. ecomOS: paid placements only when labelled sponsored or affiliate, copy true to the fact sheet, no competitor exclusion requested. What the agent should do: R65; route every paid option through legal review; record the disclosure on the mention target list.

**C9. AI-written content.**
04: about 90% of cited content is not AI-detected, fully automated content does not win, and if it did it would collapse answers; AI-assisted, human-edited is fine. 01: Google penalises thin content, not AI authorship; use an assistant to draft. 05: assuming AI-written content is spam is wrong; models can write deep content. 02: scaled AI content is the riskiest tactic in the field. When each is right: they agree more than they seem to. The dividing line is human editing, first-hand detail and volume. What the agent should do: R53 and P19; never bulk-publish; inject first-hand facts; edit by hand; verify sources.

**C10. Fan-out sub-queries: how many, and whether to target them.**
Count: 03 and 07 cite 9 to 11 per prompt (up to 28; 420 in deep research); 02 observes 1 to 3 in normal use. Use: 03 says do not build a keyword list from them (over 95% zero volume, inconsistent). 02 says read the literal phrasing and put it in the title, URL, H1 and opener. 01 routes fan-out questions into FAQs and guide subheadings after manual trimming. What the agent should do: use fan-out for coverage (R2) and phrasing (R39) on pages that exist for other reasons; never create a page per sub-query (R57); log the count seen for the brand's own prompts rather than assuming either figure.

**C11. How much Google ranking transfers to AI citations.**
76% (07), revised to about 38% (03), 14% of citations outside the top 100 (03), 35% for ChatGPT and 70% for Perplexity (04), 28.6% Perplexity and 8% to 10% ChatGPT from Google's top 10 (03). None is dated or linked. What the agent should do: assume classic ranking helps most on Google surfaces and Perplexity and least on ChatGPT; measure the brand's own overlap by comparing P6 cited URLs with GSC top-10 pages; do not quote any of these percentages as fact.

**C12. Schema's value for AEO.**
03: no confirmed evidence it improves AI citation; keep what SEO needs. 06 and 09: add Organization and product schema as an AI signal (no evidence). 04: shoppable answer cards lean on rich-snippet data and review counts in commerce. What the agent should do: R30; keep Product, Offer, Organization, review and breadcrumb schema accurate and validated for SEO and shopping surfaces; spend no extra hours on schema "for AI".

**C13. llms.txt.**
03: low priority, no major engine confirmed reading it, will not hurt. 02: a vendor leading with it is a grifter probe. 08: names it as an emerging standard. What the agent should do: R31; no engineering time until an engine documents support; re-check quarterly (section 11).

**C14. Date-only refresh.**
06's presenter: change the visible date slightly with no content change "so competitors don't notice", and claims it boosts ranking. 03: substantive changes only, never just the date. ecomOS prohibits it. What the agent should do: R40, R102.

**C15. Press releases and "industry reports".**
02: a cheap wire release with the phrase in the title, subhead and first line got a named person cited for that phrase; his fabricated-company test shows the same mechanism spreads false claims. 06: relabel a promotional ranking as an industry report and calls it the highest-ROI tactic; 06's card adds disclosure guardrails the video never said. ecomOS: real news only. What the agent should do: R70, P15; if a survey or test was actually run, publish it with method and sponsor disclosed; never call a self-ranking a report.

**C16. Self-published listicles and "source poisoning".**
06: publish 5 to 10 own "best of" lists on Medium, Substack, LinkedIn or Quora, brand first, competitors omitted, on the basis of unnamed "10 documents" studies. 02: assistants already route around self-serving listicles with review-site searches; scaled comparison pages fail the user test. ecomOS prohibits it. What the agent should do: R103; earn placement on lists the engines already trust (R64).

**C17. Citations as a KPI vs citations as vanity.**
01 and 03 track citations and mentions as headline KPIs; 06 reports "ranking in AI search". 02 calls citation-based visibility metrics "dangerous" and vendor-driven: 1 URL cited across endless phrasings, trackers reporting when no search ran, links without a name. 04 says pay commodity prices for tracking. What the agent should do: report share of voice on a frozen prompt set with named versus cited separated, plus revenue and survey attribution (R89, R91, P17); never headline a raw count.

**C18. FAQ count on commercial pages.**
01: 5 max on a money page. 06: a PAA-driven FAQ at the bottom of every important page, no cap. What the agent should do: cap at 5 on PDP and category pages; put the fuller Q&A on the guide and link both ways (R48).

**C19. Which platform to prioritise.**
05: ChatGPT first for consumers (over 90% of Gamma's AEO users), Google AI Overviews second for its SEO side benefit, then Perplexity, then Claude; Claude, Copilot and Bing first for enterprise (a guess). 03: pick 1 to 2 by market share and SEO overlap. 04: about 3 surfaces, nobody knows the winner. 06: gives no method. What the agent should do: R15; decide from the brand's survey and referral data after 1 quarter; until then ChatGPT plus Google AI surfaces for a consumer store.

## 8. Common mistakes

Merged from all 9 sources, deduplicated, each with the fix.

1. Blocking AI crawlers by accident through an old robots.txt template, a Cloudflare default or a bot-blocking app. Fix: P1 steps 1 to 6; re-run after every platform change. (03, 07, 06, 04)
2. Blocking everything as a defensive default and forfeiting the channel. Fix: P2; allow search bots, decide training separately. (04)
3. Product copy, specs, reviews or FAQ injected by JavaScript and invisible to crawlers. Fix: server-side render those blocks; test with JS off. (03, 06)
4. Launching or adding collections without Search Console and Bing submission. Fix: P1 step 9. (01, 06)
5. Trusting a plugin's schema without validation, or schema facts that differ from the page. Fix: validate; match the fact sheet. (01, 06)
6. Spending engineering hours on llms.txt, "AI info pages" or "chunking everything". Fix: R31; low priority. (03, 02)
7. Leaving hallucinated URLs as dead ends. Fix: 301 to the closest page. (03)
8. Burying the answer under marketing build-up. Fix: 20 to 50 word answer first, TL;DR facts above the fold. (06, 01, 03, 07, 08, 09)
9. Section openers that depend on earlier text ("as mentioned above"). Fix: atomic sections. (03, 07)
10. Generic references ("this product", "many users") and compound sentences. Fix: named entities, 1 idea per sentence, below tenth grade. (03, 07, 06)
11. Padding word count for authority. Fix: length the topic needs, in capsules. (03, 07, 09)
12. One page that covers every product or service. Fix: 1 page per offering with demand. (01)
13. Clever taglines in the first fold. Fix: what, for whom, next action. (01)
14. More than 5 FAQs on a money page, diluting intent. Fix: move extras to a guide. (01)
15. Writing "what is X" content the Overview already answers, expecting clicks. Fix: AI filter; retarget to mention or transactional. (03, 07, 02)
16. Building pages per fan-out sub-query. Fix: coverage and phrasing on existing pages. (03)
17. Optimising for a single head keyword instead of the whole topic. Fix: R2 coverage check. (03, 07)
18. Chasing a fixed "rank" in AI answers. Fix: share of voice on a frozen prompt set. (03, 04)
19. Assuming 1 platform's visibility transfers to the others, or that AI Mode mirrors AI Overviews. Fix: plan per platform. (03, 05)
20. Applying 1 Reddit playbook to every engine. Fix: check which platforms cite Reddit for the brand's prompts. (05)
21. Fake accounts, auto-posting, self-upvotes, cold link drops, brand mentions in unrelated threads. Fix: 1 disclosed person, 1 useful answer. (04, 05, 06, 03)
22. "We are better than X" posts. Fix: open-ecosystem angle. (05)
23. Paying for "Reddit mentions" without checking which threads are cited, their age, or subreddit rules. Fix: R66 checks first. (02)
24. Letting a negative indexed comment sit. Fix: respond early and honestly. (05)
25. Emailing competitors for inclusion in their listicles. Fix: skip them. (02)
26. Publishing self-serving listicles that hide competitors. Fix: prohibited; earn placement on trusted lists. (06 recommends; 02 warns)
27. Paid placements presented as editorial or as an "industry report". Fix: prohibited; disclosed placements only. (02, 06)
28. Buying links or bulk citations ("300 citations for $5"). Fix: prohibited; free listings and honest citation services. (01)
29. Incentivising, scripting or conditioning reviews. Fix: prohibited; neutral request. (06)
30. Changing only the date to fake freshness. Fix: prohibited; substantive refresh. (06 recommends; 03 forbids)
31. Rewriting a page whose problem is missing links, not staleness. Fix: check referring domains first. (03)
32. Scaling AI content to hundreds of posts. Fix: prohibited; human-edited, first-hand, verified. (02, 04)
33. Assuming Google penalises AI authorship, or that the model used is a ranking factor. Fix: judge thinness, not authorship. (01, 05)
34. Accepting AI-generated keyword, PAA or question lists in bulk. Fix: trim by hand. (01)
35. Inventing certifications, numbers, quotes or "original data" to satisfy an AI criteria list. Fix: prohibited; fact sheet only. (06)
36. Leaving brand information gaps for engines to fill with fiction. Fix: About or Facts page, pricing, product facts on site. (03, 06, 02)
37. Inconsistent NAP or facts across listings, schema and site. Fix: character-identical everywhere. (06, 01)
38. Relying on 1 review platform. Fix: spread across the platforms buyers use. (02)
39. Leaving an original framework unbranded. Fix: name it and repeat the name. (03)
40. Judging the channel by last-touch referral clicks only. Fix: 3 measurement pillars. (05, 04, 03, 07)
41. Burying AI options under "Other" in the survey. Fix: list them up front. (05)
42. Headlining raw citation counts, or trusting a tracker without asking whether a search fired. Fix: R91. (02)
43. Trusting a blended traffic chart or a launch-time case study. Fix: split by difficulty band; ask "how are they doing now". (02)
44. A single before-and-after with no control group. Fix: P7. (04)
45. Paying premium prices for commodity tracking. Fix: cheapest tool that does the job; about 3 surfaces. (04)
46. Defunding search because "SEO is dying". Fix: R12. (04, 08)
47. Treating GEO as a one-time project. Fix: monthly and quarterly cadence. (03, 09, 06, 05)
48. Trying to fix every gap at once. Fix: biggest gap first, quick wins first. (03, 07)
49. Treating an MCP listing or agent integration as self-marketing. Fix: it is a retention play; tell existing users. (05)
50. Reacting to the "level playing field" as permanent. Fix: re-check quarterly. (05)
51. Uploading PNG illustrations that slow the page. Fix: WEBP; real product photos where accuracy matters. (01)
52. Copying the same copy across product pages. Fix: template the structure, rewrite the copy. (01)
53. Skipping outbound source links for fear of losing the visitor. Fix: cite sources; hold the reader with content. (01)

## 9. Deliverables

**D1. Crawlability fix list.** Markdown table from P1: layer (robots, CDN, WAF, app, rendering, indexing, schema, 404, speed), finding, page or path, evidence (the exact rule or screenshot reference), fix, owner, priority (1 = blocked bot, 2 = hidden content, 3 = indexing, 4 = 404, 5 = speed and schema), status, re-test date. Header states the crawler names checked and the date. `[web check: names]`

**D2. Page rewrite brief.** One per page. Fields: page URL and type (PDP, category, guide, comparison); target prompt and buyer phrasing; goal (click, mention, transactional); the live-answer check (cited page types and domains, date); primary phrase for title, H1 and opener; answer-first passage (20 to 50 words) drafted; TL;DR fact list; H2 outline with the sub-questions from the fan-out check; table spec if the winning format is a comparison; original data or first-hand detail to include (from the brand record); source links to cite; FAQ (5 max on commercial pages); internal links in and out; schema facts to match; claims checklist against the fact sheet; reading-level target; refresh date. Written in plain English so a writer can execute it without this playbook.

**D3. Mention target list.** Spreadsheet from P11, P12, P13, P14: target URL, domain, tier (1 editorial, 2 community, 3 owned), why it is a target (cited for which prompt, or competitor-driving source), owner and contact, placement type (editorial, affiliate, sponsored, community answer, video, review platform, directory), disclosure required, cost, status, date landed, prompts to re-run after landing. Competitor-owned pages excluded. A second tab lists wrong facts found in the prompt audit with source, owner, request sent, resolved.

**D4. Prompt test set with baseline.** CSV: prompt id, prompt text, intent (category best, comparison, fit, brand, price and policy), page or entity targeted, group (test or control when used). Baseline sheet per platform: date, model, mode, run number, brand named, brand cited, competitors named, cited URLs, answer format. Summary computed in code: share of voice, citation share, competitor shares, top cited domains, per platform, with the run count. A note on which figures are a floor and why.

**D5. Monthly visibility report.** 1 page in this order: share of voice and citation share per platform versus last month and baseline; named-but-unlinked share; prompt audit accuracy (open, closed, new); AI channel sessions, conversion rate and revenue versus organic with the undercount caveat; survey share naming an AI assistant; top pages fetched by citation bots; GSC and Bing figures month over month; crawlability status (blocked bots, hidden content, AI-referred 404s); mention targets landed, pending, declined; experiments and their control comparison; the single biggest gap for next month and its fix. No raw citation count as a headline. No number from section 6 presented as an industry benchmark.

**D6. Gap list.** From P3: finding, gap type (visibility, narrative, topic, format, mentions, demand), label (fix, build, influence), evidence prompt or URL, score (demand, credibility, citation odds), quick win flag, assigned procedure.

**D7. Question research export.** From P5: question, source (paid terms, support, PAA, fan-out, criteria), intent, page type, goal, cited domains, owner.

**D8. Vendor vetting sheet.** From P18 and checklist 5.6: each question, the answer verbatim, the flag colour, the case-study band chart, the prohibited-tactics screen, the price comparison, the decision and reason.

**D9. Experiment record.** From P7: hypothesis, tactic, test and control prompt ids, dates, both curves, result, replication status, decision.

## 10. What needs live data or a web check

**`[needs brand data]`**
- Verified fact sheet: what the brand sells, founding year, materials, certifications, prices, shipping and returns, differentiators (R46, R47, P4, P8).
- Approved claims list, competitor claims allowed, legal and PR review process for comparison pages, press releases and paid placements (R43, R65, R70, P9, P15).
- Branded entity list: sub-brands, product lines, proprietary names, founder (R79, P3).
- Competitor list, 3 to 5 real plus who AI names (R78, P3, P4).
- Buyer segment and which assistants buyers name in the survey; platform mix (R15, C19).
- Real buyer phrasing from support tickets, chat, sales notes, survey free text (R39, R56, P5).
- Which narrow use cases the catalog genuinely serves (R17).
- Which keywords are informational versus commercial and which trigger Overviews (R59).
- Current robots.txt, CDN and WAF settings, hosting platform (P1).
- GA4, Search Console, Bing Webmaster access; current channel group config (P16).
- Survey platform and current questions (R87, P16).
- Server logs or bot analytics availability (R88).
- Top pages by traffic decline and referring domains (R41, P10).
- Revenue by traffic source; AI-referred conversion rate (R93, R97).
- Review platform accounts and ratings; where buyers already post (R69, P14).
- Subreddit sizes and rules relevant to the category; an employee willing to post under their name (R66, P12).
- Existing YouTube, podcast, LinkedIn presence and top videos (R68, R74).
- Original data the brand actually holds: tests, surveys, benchmarks (R44, R45).
- Budget ceiling for trackers, placements and creators; time horizon (R20, R95).
- Interoperability or open-ecosystem angle, if any, for community posts (R66).

**`[web check]`**
- Current AI crawler user-agent names per vendor and the training-versus-search split (R23, R24, P1, P2).
- Cloudflare's current AI-bot setting name and default (R25).
- JavaScript rendering support per crawler (R27).
- llms.txt adoption by any major engine (R31, C13).
- Current AI referrer hostnames and which platforms strip referrers (R86, P16).
- Live answers for the brand's prompt set, per platform, logged in and out (P4, P6).
- Cited domains and listicles for "best [category]" on AI Overviews and AI Mode (R64, P11).
- Which platforms cite Reddit, and subreddit self-promotion rules (R66, R67, C5).
- Which secondary platforms are indexed now (LinkedIn, Medium, Quora, Substack, X, Discord, Instagram) (R74).
- Current tracker tools, prompt limits, logged-in support, pricing (R95, P18).
- Free bot-access checker, JS-rendering checker, schema generator and validator tools (P1).
- Contact-finding tool availability and terms (P11).
- Reddit alert tool availability (P12).
- Reporter-request platform current name and tiers (R71).
- Wire service names, pricing and syndication partners (R70, P15).
- Citation service pricing (R72).
- Review platform incentive policies (R69, C6).
- Comparative advertising rules for the brand's markets (R43).
- Whether the Ahrefs, Graphite and other vendor studies are published with methodology; the origin of 06's 44%, 4 to 10 times and "10 documents" figures, and 05's 60/40 split (R98, section 6).
- Current Google statements on publisher referral traffic (R12).
- Agentic commerce programs for the brand's platform (R77).
- The ChatGPT network-tab technique still working (P20).
- Perplexity showing fan-out in its interface (P20).
- GA4 menu path; Bing AI performance tab name (P16, R92).

## 11. Freshness and stale-risk notes

This whole domain changes monthly. The sources themselves revise figures mid-lesson (03's 76% to 38%), rename platforms mid-sentence (01's HARO to Featured to Connectivity), and label their own claims as "right now". Re-verify on the cadence below, and date every figure in any client document.

**Re-verify monthly.**
- Crawler user-agent names and the training-versus-search split for OpenAI, Anthropic, Google, Perplexity, Microsoft. New bots appear; names change. (R23, R24, R88)
- Cloudflare's AI-bot default and setting name. (R25)
- Which platforms pass referrer data, and the hostnames to match. (R86)
- Which third-party platforms are being cited: Reddit's presence in OpenAI's citations changed at least once (02); LinkedIn, Quora, Medium, Substack, X, Discord and Instagram indexing (05). (R67, R74)
- Answer formats: shoppable cards, carousels, maps, and which categories get them (04). (R81)
- The brand's own cited domains and listicles (R10: over 45% churn per refresh).
- Prompt set share of voice (P6, P17).

**Re-verify quarterly.**
- llms.txt adoption. (R31)
- JavaScript rendering support per crawler. (R27)
- Tracker tool names, features, prompt limits, logged-in support and prices; 04 counted about 60 tools. (R95)
- Platform market share and which platform buyers use, from the survey. (R15, C19)
- Whether the "level playing field" for authority is closing (05's prediction). (R18, C2)
- Fan-out counts observed for the brand's prompts (9 to 11 vs 1 to 3). (C10)
- Wire service, citation service, reporter platform and creator pricing. (R70, R71, R72)
- Subreddit rules and sizes. (R66)
- Review platform incentive policies. (R69)
- MCP and agentic commerce programs. (R77)

**Re-verify before quoting to a client.**
- Every statistic in section 6 marked vendor only or unsourced. In particular: the 0.664 and 0.737 correlations, 43.8% listicles, 25.7% fresher, 89.7% and 76% freshness, 14% and 13.7% overlaps, 0.25% traffic share, 9.7 times growth, the 58% CTR drop, 5.9% blocking, 2.87 times 404s, 45% churn, the 37% to 39% misinformation rates, 04's 35% and 70% overlaps and 1-in-20 pages, 06's 44%, 4 to 10 times, "10 documents" and "4 to 5 times", 05's 60/40 split and 5 times Claude gap, 08's 60% zero-click and 15 million Perplexity users.
- Model names: 03 names GPT-4 for YouTube training; 05 names models and a "May 21st" Google update with no year; 02 states an "August 2025" cutoff. All superseded.
- Every UI path tagged `[verify UI]`: GA4 channel groups, GSC sitemaps, Bing AI performance tab, Cloudflare settings, Ahrefs Brand Radar filters, ChatGPT and Claude project features, the DevTools network technique, Perplexity's fan-out display, Lighthouse menu path.

**Rules least likely to go stale.** Answer first, atomic sections, entity-rich sentences (R36 to R38); consistent facts everywhere (R47); fill information gaps with official facts (R46); crawler access before anything (R23); share of voice with a control group (R89, R90); the 3 measurement pillars (R85); the prohibited list (section 3.10). These follow from how retrieval and summarisation work, not from any platform's current settings.

**Rules most likely to go stale.** Everything in section 3.3 that names a bot, a default or a rendering capability; every platform ranking in R15 and C19; every number in section 6; every tool name in sections 4 and 5; Reddit's platform-specific behaviour (R67); the 6-month and 2-month refresh thresholds, which come from 1 vendor study and 1 presenter.

**How to update this playbook.** Add a new mini playbook under sources/ and re-run the pass 2 merge. Brand exceptions go in `brands/<brand>/overlays/16-AEO.md`. Agent-specific additions go in `overlays/`. Never edit this file for a brand.

## 12. Source index

| No. | Title | Type | Credibility and bias | Contributed most |
|---|---|---|---|---|
| 01 | The Complete AI SEO Course 2026 | Course transcript, 1 presenter, 30 cards | Practitioner of 10+ years selling his own tool (Data Wise) and a paid community. Whole workflow demonstrated on a fictional EV charger installer, not a store; ecommerce mapping is card adaptation. One unnamed "peer-reviewed study" behind the capsule technique. Normalises buying links; the sponsored/nofollow requirement in card d84b2be76cec is a card addition. Bias: high (own tool, own community). Evidence: own practice. | Content capsule technique and lengths; 1 page per offering; 2-second first fold; FAQ cap; AI workspace and drafting workflow; GSC and Bing AI performance tracking; free directory citations; reporter-request platforms. |
| 02 | Generative Engine Optimization: Is It Safe and How To Do It the Right Way | Podcast interview, 26 cards | GEO consultant with unnamed client anecdotes; host's mid-roll course ad excluded. The most skeptical source on vendors and metrics. Describes gray tactics it does not condone and 1 fabricated-company test. Bias: medium (consultant; withholds names). Evidence: own observation, no studies. | Vendor vetting questions and probes; case-study difficulty-band audit; retrieval vs memory detection; fan-out network-tab technique; third-party listicles over own; bottom-of-funnel priority; time-horizon screen; citation metrics skepticism; press release mechanics and risks. |
| 03 | AI SEO Course for Beginners: Complete AEO Tutorial | Ahrefs course, 4 modules, 37 cards | Official Ahrefs course; every workflow routes through paid Ahrefs products; all statistics are Ahrefs' unpublished studies quoted without methodology; Vercel and Tally anecdotes relayed. Never uses a PDP example; ecommerce framing is card adaptation. 2 near-duplicate cards. Bias: high (vendor). Evidence: large-sample vendor studies, 1 own misinformation test. | Retrieval mechanics; fan-out figures; platform overlap; mention correlation; length vs freshness; BLUF and atomic writing; BID and AI filter; 6-gap analysis; 3-tier mentions; YouTube workflow; 6 technical checks; 3-pillar measurement; GA4 setup; week-1 plan. |
| 04 | The ultimate guide to AEO: How to get ChatGPT to recommend your product | Podcast interview, 28 cards | CEO of an SEO agency (Graphite), building his own tracker; 18 years in commerce SEO. Evidence: 1 named B2B client (Webflow), an internal AI-content study with described method, opinion. Relays the platform's "just write good content" line and disagrees with it openly. Bias: medium-high (sells services). | Share of voice over rank; control-group experiment design; RAG vs training model; information gain and typicality; authentic Reddit rules; index-yes train-separately policy; help centre subdirectory; tool pricing sanity check; "search is not dying". |
| 05 | The Head of Growth at a $100M Company Explains AEO | Podcast interview, 10 cards | Growth lead at a consumer SaaS company (Gamma). Entirely own observations, heavily hedged ("black box", "that's a theory"). No ecommerce. Procedures reconstructed by the mini playbook. Raises "agentic bribing" as something others do. Bias: low commercial, high anecdotal. | Measure like view-through; HDYHAU with AI options up front; platform priority by segment; Reddit open-ecosystem angle and lags; niche-down ladder; citation half-life spreadsheet; memory hypothesis; secondary surfaces; MCP as retention. |
| 06 | The Ultimate AI Visibility Checklist (AEO/GEO for ecommerce) | YouTube transcript, 20 cards | Unnamed presenter building a paid tool (Focal) and a community. Title says ecommerce; the only example is self-storage software. Several headline numbers unsourced. Recommends incentivised reviews, date-only refreshes, self-published listicles and "industry report" releases; its own cards add guardrails the video never gave. Bias: high (tool funnel; gray-hat). Evidence: 1 anecdotal client. | The 7-part checklist shape; About or Facts page; comparison pages with tables; PAA FAQs; refresh cadence; NAP and directories; listicle outreach steps; AI-elicited criteria; "what do you know about [brand]" audit; YouTube file-name details; the prohibited list's clearest examples. |
| 07 | Learn 80% of AEO in 19 Minutes | YouTube transcript, condensed course, 11 cards | Almost certainly Ahrefs-produced; teaser for a paid course; same studies as 03. Generic examples, no ecommerce. Bias: high (vendor). Evidence: same vendor studies. | The closing sequence (technical, measurement, biggest gap); gap-to-fix map; 6-month staleness threshold; the 30-second robots check; keyword-research prompt template. Counts as 1 evidence base with 03. |
| 08 | What Is GEO and Why It Is Important in 2025 | Short YouTube explainer, 4 cards | Hostinger-sponsored definitional video with a discount code; 2 unsourced numbers; 1 third-party blog held up as a model; promised checklist absent (card 2b710976674c is a reconstruction). Bias: medium (sponsor). Evidence: none. | SEO vs GEO framing (target, ranking factors, traffic type, scope); the quotable-passage pattern; "you still need SEO"; "don't rush". |
| 09 | 7 Essential Tactics for Mastering GEO | Short talking-head video, 7 cards | Self-identified SEO with illustrative industry examples only; ends with a sponsor read for Py Rank, not a tested tool. No data, no procedures with settings. Bias: medium (sponsor). Evidence: none. | Start from the conversational query; answer directly, no keyword-density fluff; structure and schema for parsing; intent breadth; reviews and UGC as freshness (asserted); ongoing loop. |

**Neighbour folders and what lives there.**
- 13-ORG organic and content: content calendars, social, organic video programs. AEO borrows the answer-first and entity rules; 13-ORG owns cadence and creative.
- 08-SPD speed: Core Web Vitals and rendering engineering behind R27 and R28.
- 07-LPG landing pages and 09-CRO testing: first-fold design, conversion tests; the 2-second rule overlaps with 07-LPG.
- 06-MEA measurement: attribution models, dashboards, ROAS; AEO adds only the AI channel, the survey option and the prompt set.
- 17-CXP post-purchase: the review request flow and the post-purchase survey mechanics.
- 04-BRD brand: the verified fact sheet and positioning every claim traces to.
- 12-GAD google ads: paid money terms used as question seeds.
- 10-MCR paid social creative and 11-ADC ad copy: no overlap beyond shared voice rules.
- Core SEO (keyword strategy, backlinks, site architecture): the sources point to "15-SEO", which does not exist in playbooks/v2 on 24 Sep 2026. Until it does, 13-ORG holds content SEO and this folder holds crawler access only.
