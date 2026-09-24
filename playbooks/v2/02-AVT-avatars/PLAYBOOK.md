# 02-AVT customer avatars and market research playbook

version: 2.0-draft  |  date: 24 Sep 2026  |  sources: 9 mini playbooks (6 independent voices: 03, 04, 06 and 09 are one paid-social creator, see section 0)  |  cards: 216  |  built from: sources/*.md

## 0. How to use this playbook

**Who runs it.** The customer avatar and market research agent. Its job ends when a brand has a set of avatar records that are backed by quoted evidence, ranked by priority, and handed to the creative, copy, offer and landing page agents with an angle map. It does not write ads, pages or offers. It does not set ad targeting. It does not pick products.

**Ecommerce first.** This playbook is for stores, not for any business that happens to sell online. Section 3.0 is the ranking: it says what to check first and in what order for a store. Store-type conditions, hero SKU versus catalogue, low versus high AOV, subscription versus one-off, marketplace-heavy, luxury or considered purchase, mobile-first India versus US, decide which rules in the groups below actually apply to the brand in front of the agent.

**Which sections to load for which task.**

| Task | Load | Run |
|---|---|---|
| Build the first avatar set for a brand that has customers | 0, 1, 2, 3.1, 3.2, 3.4, 3.6, 3.7 | P1, P3, P4, P10, P11, P14, P16, P19, P25 |
| Build an avatar for a new product or new market with no customers | 3.3, 3.4, 3.5, 3.9 | P2, P5, P6, P7, P24, P21, P25 |
| One 60-minute research sprint before a copy round | 3.4, 3.6 | P1, then checklist 5.1 |
| Review-mining pass on Amazon or the brand's own reviews | 3.4 | P3, checklist 5.2 |
| Run customer interviews | 3.4 | P10, P11, P12, P13, checklist 5.3 |
| Write or QA an avatar record | 3.6 | P17, P18, P19, P20, checklist 5.4 |
| Turn an avatar into a creative or copy brief | 3.8 | P26, P27, checklist 5.5 |
| Find an untapped avatar to scale paid social | 3.3, 3.9 | P24, checklist 5.6 |
| Use AI research or an LLM persona | 3.5 | P21, P22, P23 |
| Decide how many avatars a brand needs | 3.7 | P25 |
| Feed the brand brain | 3.10 | P30 |
| Reconcile conflicting advice | 7 | none |

**What the agent fetches before acting.**

1. From the brand record: the product and its real mechanism, the current customer list with a value ranking, existing reviews, past interview notes, support ticket themes, return reasons, any post-purchase survey answers, past avatar records and which ones creative actually used, past test results per angle. Section 10 lists every `[needs brand data]` item. Brand record data wins over any figure a source gives about its own store or students.
2. From the data layer: repeat purchase rate per SKU (the "little hire" check), refund rate per SKU, which creative angles won or lost and for which stated audience. Do arithmetic in code, not in the model.
3. From the web: current state of every tool named here (SparkToro, Audience, Brand24, SimilarWeb, Google Ads Keyword Planner, Meta Ad Library, Amazon review filters, ChatGPT and Gemini deep research, Claude and ChatGPT projects, Shopify post-purchase survey apps), the current subreddits and forums for the category, current Meta policy on personal attributes and health claims. Section 10 lists every `[web check]`. Section 11 says how often to re-check.

**What the sources are.** 9 mini playbooks, 6 independent voices.

- 01 is Competing Against Luck (Christensen, Hall, Dillon, Duncan, 2016). An academic business book selling its own Jobs Theory, which the authors also sell as consulting (Innosight, Re-Wired Group). Evidence is named company cases, self-reported by executives. It has no ecommerce, DTC or paid-social case. Its mini playbook carries a section of ecommerce adaptations written by the card writer and pass 1, not the book. Those are marked `[adaptation]` wherever this playbook uses them.
- 02 (Adrienne Barnes, Best Buyer Persona) and 07 (HubSpot Media's Kyle Denhoff and Andrew Frost) are B2B persona sources. 02 works mostly with B2B SaaS and says so. 07 frames the ICP as a company profile with a buying committee and admits B2C needs an adaptation it does not give. Both sell something: 02 sells persona research, 07 plugs HubSpot's CRM and its persona QA feature.
- 03, 04, 06 and 09 are one paid-social creator ("Anthony" in 03 and 04; 06 and 09 are unnamed but the task brief and the shared method, vocabulary, worked examples and course pitch identify the same voice). He sells a course, a "School" community, an "evolve program", done-for-you ads for $200k+/month accounts and mentorship below that. Every result he states ($10k days, $30k days, $100k days, a student's $100k/month, a 5x day-one ROAS, a $3M agency sale) is self-reported and unverified. This playbook counts these 4 files as 1 voice when it says how many sources agree.
- 05 is an unnamed presenter for GrowthLab's "0 to Launch" course, dated January 2018. Self-reported "20+ successful products". Manual review and forum reading is his whole method.
- 08 is an unnamed presenter of a 2022 "Market Research 101" video that promotes his own marketing videos. It gives the 5W framework and the Google, Amazon and Ad Library method with no survey or interview method.

No source cites a dataset, a controlled test or audited numbers. The only cited studies are inside 01 (Kahneman and Tversky on loss aversion, a 2010 Bain reorg study, Nielsen innovation reports) and a twice-removed Nielsen claim in 02 (20 interviews cover about 97% of audience sentiment). Every count, time box and sample size in section 6 is a practitioner heuristic unless the table says otherwise.

**Adaptation tag.** Where the mini playbooks or this pass translate a source's idea into ecommerce terms the source never used, the rule carries `[adaptation]` and names who made it. Examples: big hire to first purchase and little hire to repeat purchase (pass 1 on source 01), workarounds to return reasons and support tickets (pass 1 on 01), B2B survey fields to consumer purchase-occasion fields (this pass on 02), win or loss interviews (this pass, from 02's churn interviews plus 07's call transcripts). The agent may use an adaptation. It may not cite it as the source's claim.

**ecomOS rules that override any source** (repeated in 3.11):

- No invented claims. An avatar record cannot state a fear, desire, belief or failed solution that no real review, post, ticket or interview showed.
- No invented quotes. Every quote in an avatar record traces to a real review, post, ticket, survey answer or interview in the brand's research evidence file, with the source URL or record id and the date collected. A quote an LLM wrote, summarized or "typical-ized" is not a quote.
- No sensitive-attribute claims that breach Meta policy. The record may hold what customers said about their own health, body, age, finances, religion or relationships as research. The creative brief may not assert or imply that a viewer has such an attribute. `[web check: current Meta advertising standards on personal attributes and personal health]`
- Brand record data wins over any source's self-reported figures. If a source says "the top 20% of customers" and the brand's data says the top 15% carry 60% of revenue, use the brand's cut.
- Competitor ads are signals, not proven winners. Use them for who is being spoken to, layout and mood only. Never copy text, logos, products or faces.
- Meta is read-only. Ad Library and read tools only.
- Keep brands apart. Keep public web research separate from private business data. Do not paste a brand's customer transcripts into a shared research doc with another brand's forum quotes.

## 1. Scope and outcomes

**Covers.** What a customer avatar is and is not (job, circumstance, forces, big and little hire). How to find avatar candidates (five job-hunting lenses, review identity markers, market fracturing, untapped avatars in a saturated category, failed-solution buyers). Every research source in the 9 mini playbooks and how to mine it: Amazon reviews by star rating, Reddit and niche forums, Quora, Google and Amazon autocomplete and Keyword Planner, competitor sites and headlines, Meta Ad Library, social content mapping, digital intelligence tools, social listening, customer interviews with scripts and counts, direct calls and DMs, post-purchase and verification surveys, churn and loss conversations, support and sales transcripts, AI deep research and LLM synthesis. The avatar record format (quoted evidence, trigger moment, job statement, miracles and miseries, failed solutions, beliefs, objections as anxieties, 5W fields, job spec). Validation rules for a job statement. Persona count, priority and the B2B ICP taxonomy. Avatar-to-creative and avatar-to-funnel mapping as far as the sources go. How avatars feed the brand brain.

**Does not cover.** Writing hooks, scripts, primary text or VSLs (10-MCR and 11-ADC; sources 03, 04, 06 and 09 all route it there). Landing page and pre-lander build (07-LPG). Offer construction, pricing and guarantees (03-OFF; source 09's "framing is part of the offer" is a handoff note only). Brand voice and positioning (04-BRD; 01's purpose brand idea is noted in 3.10 as a long-horizon goal only). Ad set structure, targeting settings and budgets (24-DEP and 11-ADC; source 06's broad-targeting practice is recorded in 3.8 as a constraint on the creative, not as a media rule). Product selection and mechanism engineering (01-PRD; source 04's "new mechanism or new avatar" fork is here only as far as it decides whether avatar work is the right lever). Email segmentation and RFM (14-EML; source 02's caveat says its JTBD segmentation is not a lifecycle segmentation method). Organizational design chapters of 01 (processes, metrics, mission statements) beyond the two ideas that port to a small brand: measure the customer's benefit and let the job settle disputes.

**Business measures this domain moves.** Share of creative tests that scale (sources 03, 06 and 09 claim stalled creative is usually an avatar gap, unverified). Editing effort on copy drafts (the ecomOS signal Kevin prefers). Hook and first-3-second retention on avatar-specific creative versus generic creative `[needs brand data: per-creative results]`. Conversion rate lift when the whole funnel names one avatar (source 06, no numbers). Repeat purchase rate as the little-hire check (01, adaptation). Return and 1-star review rate driven by wrong-fit buyers (01's "signal who it is not for"). Persona usage rate: the share of briefs that cite an avatar record (02's survey found 77% of marketers never use theirs).

## 2. Inputs the agent needs

| Input | From where | Required or optional | Why |
|---|---|---|---|
| Product, its real mechanism and whether it differs from competitors (visual, mechanical, functional) | brand record | required | Decides new-mechanism route vs new-avatar route (R24) and whether niching the avatar is the only lever left (R81) |
| Customer list with a value ranking (revenue, margin or repeat count; the brand picks the metric) | data layer | required for an existing brand | The top-customer cut that anchors the avatar (R17); the metric is not given by any source `[needs brand data: ranking metric]` |
| Brand's own reviews, all star ratings, with dates | brand record, review app | required for an existing brand | Identity markers and failed-solution buyers (R18, R27, R33) |
| Competitor listings and review pages (Amazon, marketplace, DTC site) | web | required | Review mining (P3), mainstream avatar map (P6) |
| Past interview transcripts, call notes, DM threads | brand record | optional but strongest input | The "why" behind behaviour (R50); every quote needs a source (R68) |
| Support ticket themes, return reasons, cancellation reasons | data layer, helpdesk | optional | Passive data on struggle and workarounds (R30, R60) `[adaptation]` |
| Post-purchase survey answers | brand record | optional | Trigger and situation at scale (R58) |
| Repeat purchase rate per SKU, refund rate per SKU | data layer | optional | Little-hire check (R13) and wrong-fit signal (R73) |
| Which creative angles won or lost, and the avatar each was written for | data layer, 10-MCR test log | optional | Angle map priority (P26) and research-gap diagnosis (R96) |
| Existing avatar records and whether creative used them | brand record | optional | Persona-use audit (R75, P28) |
| Category subreddits, forums, Quora topics, Facebook groups | web | required | Forum mining (R35) `[web check: current communities]` |
| Meta Ad Library results for the category keyword and named competitors | web, read-only | required | Mainstream avatar map (R25), long-running ad screen (R44) |
| Google and Amazon autocomplete, Keyword Planner volumes for the target country | web | optional | Say vs buy datasets (R42, R43) |
| Platform demographic data for the brand's countries | web | optional | The "Where" field (R47) `[web check]` |
| Current Meta policy text on personal attributes and health claims | web | required before any creative handoff | R77 |
| Which DM channel and platform the brand's buyers use | brand record | optional | Direct outreach channel (R56) `[needs brand data]` |
| Interview incentive budget and what the brand can offer (product, early access, donation) | user | optional | R54 |
| Target research depth: copy round, new product launch, or scale attempt | user | required | Sets sprint length vs full sequence (R31, P1 vs P2) |
| Business type: consumer, B2B, or a consumer brand with a B2B line | brand record | required | Decides whether the ICP taxonomy applies (R82) |

## 3. Decision rules

Each rule states the rule, the condition, the mini playbooks that support it (by number), conflicts, and card ids. "1 voice" means only the paid-social creator (03, 04, 06, 09) says it. Rules are merged where sources overlap and keep the strictest condition.

### 3.0 Ecommerce priority order

Run this block first, in order, for every avatar task. It ranks what matters most for a store and points to the rule that backs each step.

1. Anchor on the brand's own top customers if it has buyers. Anchor on competitor Ad Library data and reviews only if it has none (R19, R82). This decides every step after it.
2. Confirm scope: a consumer avatar, or a separate B2B, wholesale or gifting line (R84, R85). The wrong scope wastes the effort.
3. Run the mechanism audit before committing. No real product difference means avatar work is the main lever. A real difference routes to 01-PRD and 03-OFF (R24, C12).
4. Match research depth to the stake: a 60-minute sprint before a copy round, the full sequence before a launch or scale attempt (R32, P1, P2).
5. Single hero SKU: build one deep record. Multi-SKU catalogue: run the prioritise-and-count step per product line and cap it at one primary avatar per line this cycle (R81, R25, P25). `[general practice]` the catalogue framing itself; the sources speak to "product line," not to a large multi-SKU catalogue.
6. Mine the store's own passive data first (reviews by star band, tickets, returns, post-purchase survey) before public forums. It is cheaper and already store-specific (R30, R34, R59, R61).
7. Treat repeat purchase rate, or subscription retention where the brand sells on subscription, as the proof gate before an avatar counts as confirmed (R16). `[general practice]` naming subscription vs one-off as the condition; the source gives only the general little-hire rule.
8. Saturated or commodity catalogue: run the untapped-avatar pipeline instead of another angle for the same avatar (R96, R24).
9. Segment by consequence, cohort, and buyer versus user for gift-heavy or considered-purchase categories, where the buyer and the user are often different people (R28, R85). `[general practice]` flagging "considered purchase" and "gift-heavy" as the trigger; the rules exist but not this framing.
10. Push the record through the whole funnel for congruence before it reaches copy, and keep Meta targeting broad while the creative carries the avatar (R89, R90, R91, C6).
11. Route anxieties, failed solutions and the Why chain to the offer and page agents as flagged, not asserted, claims (R72, R92).
12. Re-run the dominant-avatar check and the persona-use audit every quarter. Downgrade any record with no new first-party evidence (R83, R76, R100).

Load this block first; the groups below are the detail.

### 3.1 What an avatar is, and what it is not

**R1. Define an avatar by the job, not by a demographic label.** An avatar is a specific person in a specific circumstance trying to make specific progress. "Women 45+ with cats" or "30+ year old woman with knee pain" is a demographic, not an avatar. Condition: applies to any avatar meant to guide copy, creative, offers or product decisions. It does not stop the agent recording age, gender, location or income as fields; it stops those fields being the definition. Sources: 01, 02, 03, 06, 09 (4 voices). Conflict: C1 (demographic targeting). [f2b99dd64bbd] [882242897d3b] [3f6f208703f1] [83486686c828] [6f03704d60e9] [0d27b0e8ba75] [f6f18000b06c] [ef0ecef3dfbb]

**R2. Every job has 3 dimensions: functional, emotional and social.** Record all 3. Most records over-index on the functional. Store example: a mattress. Functional is pressure relief. Emotional is "will I finally sleep." Social is "what will guests think of the guest room." Condition: any purchase with real functional, emotional or social weight; 01 says the theory does not apply where there is no struggle (R9). Sources: 01 only for the 3-way split; 03 and 09 supply the emotional dimension in their own terms (dominant emotion, what they vent about). [782e3f599df4] [74ac1061a1c9] [dae729a4f6bb] [f6f18000b06c]

**R3. The circumstance, not the person, drives the choice, so the same person can be 2 avatars.** 01's milkshake buyer is 1 avatar at 7am commuting and a different avatar at 5pm with a child. 09's 2 post-knee-surgery buyers are different avatars if one wants competitive running at 20 and one wants to run for fun at 50. Condition: whenever research shows the same product bought for different progress; split the record rather than average it (R80). Sources: 01, 09 (2 voices). [f2b99dd64bbd] [c8f28fdc6c65] [e04fb9d3213c] [9b44ebb5a6e9]

**R4. Needs and attributes are not jobs.** "Feel confident" is a need: generic, always present, untestable. "Premium" or "eco-friendly" is an attribute: an experience that might cause a hire, not the job. The job is "look sharp for a pitch without ironing a shirt at 7am." A job is specific to a circumstance and yields a testable hypothesis about what gets hired. Condition: applies when writing or reviewing a job statement. Source: 01 only. [98d43a545897] [b2121bd6e7ce]

**R5. Validate a job statement by 2 tests: verb plus noun, and cross-category alternatives.** (a) The statement must read as progress: verb plus noun ("get my kitchen counter clear before guests arrive"), never an adjective list. (b) List what could be hired for it. If every candidate is a SKU in the same category, go up 1 level of abstraction and repeat, until the alternatives span different categories (an organizer, a bigger bin, decluttering, doing nothing). 01 calls this iterative and "more art than science". Condition: run before the job statement enters an avatar record (P17). Source: 01 only. [b2121bd6e7ce] [4a291c65cf40]

**R6. Jobs are discovered, not created, and they outlast solutions.** The job of sharing information across distance ran from Pony Express to email. Condition: when a category shifts or a competitor launches, re-check whether the job moved or only the solution did. Do not rewrite the job statement because a competitor changed its product. Source: 01 only. [06f039bfa4ba]

**R7. Framing the job redraws the competitive set, and nonconsumption is in it.** Netflix competes with everything you do to relax; V8 competes with peeling carrots; a knee brace competes with physical therapy and with giving up ice skating. People who buy nothing rather than an imperfect solution are a market, often the largest one (01's Airbnb figure: about 40% of guests would not have travelled at all, self-reported by Airbnb). Condition: every avatar record lists the full competitive set, including "do nothing" and out-of-category options (R71). Sources: 01 for the rule; 09's failed-solution sequence shows the same idea in ecommerce terms (physical therapy as the fired alternative). [554e0cd99c6c] [2a7279282866] [a73e6aa41bc4] [35de9821d183] [113a77a88966] [c5a5b0969938] [873f2122bf91]

**R8. Demographics may be a reach layer, never the motivation.** 01 downgrades demographics as causal evidence but allows them as a targeting layer. 08 records demographics, geographics and psychographics as the "Who" fields. 06 keeps Meta targeting broad and lets the creative carry the avatar. 04 estimates competitor avatar age and gender from Ad Library videos as a map of who to avoid, not as a definition. Condition: record demographic fields as descriptive context and as a filter for the "Where" step; never write copy from them; never let them replace the job, trigger and quotes. Sources: 01, 04, 06, 08 (3 voices). Conflict: C1. [3f6f208703f1] [6e6df56de0a9] [229a47af9d51] [af1c969a5868] [b399ed19a017]

**R9. Apply jobs thinking only where a real struggle exists.** 01 bounds its own theory: it does not apply where the decision is purely rational or mathematical, where there is no struggle, or where the "job" is really an attribute or a same-category preference. Condition: a low-stakes, impulse or commodity repurchase may not carry a job worth a full record; say so in the record rather than inventing a struggle. Source: 01 only. [53d529b9c994] [a142b390da6f]

**R10. A real insight feels true on conception.** If the team has to argue itself into believing a job insight, treat it as unproven and gather more evidence. Condition: a soft check, used when 2 candidate job statements compete; it never overrides evidence. Source: 01 only, quoting Gerald Zaltman. [95dea7e97e72]

### 3.2 Forces, firing, big hire and little hire

**R11. Four forces decide a switch: push of the problem, pull of the new solution, habit of the present, anxiety of the new.** Push plus pull must outweigh habit plus anxiety. "Good enough" alone does not win. Record all 4 for every avatar. Condition: every avatar record; every interview probes for all 4 (P11). Source: 01 only, but 03's trigger moment (public humiliation over hair loss) and 09's "promises they are sick of hearing" map to push and anxiety respectively. [d60553248611] [188ed2166ca7] [69702437d033] [355b8d9aca5c]

**R12. Loss aversion is about 2x as strong as the pull of an equal gain.** So the anxiety side needs at least as much design work as the appeal side. Condition: applies when weighing objections against benefits in the record and the brief. Source: 01, citing Kahneman and Tversky (1979). This is the only externally cited number in the folder. [188ed2166ca7]

**R13. To hire something new, the customer fires something old. Record what was fired.** The fired thing is a product, a workaround, or the choice to do nothing. Companies rarely design for it. Condition: every avatar record names the fired alternative and what made it untenable. Sources: 01 for the rule; 03, 05, 09 for the ecommerce form (named failed solutions: minoxidil, Neograft, fountains and water bowls, physical therapy, multiple personal trainers). [4171f8999a97] [e8e9e127d973] [326d0318ebcc] [b08301158fb6] [2fd2d4d2c90b]

**R14. Habit of the present is a silent competitor.** The current routine, however bad, has no marketing budget and still wins by default. Condition: when a record shows a long-standing workaround (adding water to cat food, spreadsheets, a shoebox of receipts), log it as a competitor with a reason it persists. Source: 01 only. [058b163bd2ae]

**R15. Anxiety blocks purchases as much as weak appeal, and it can be designed against directly.** ING Direct's cafés, SNHU's real campus, health clubs dropping annual contracts. Condition: every objection in the record is written as an anxiety plus the thing that removed it in real purchases (a lenient return policy, a spouse touching the product, a specific proof). Source: 01 only; 09's "broken trust markers" from 1-star reviews are the ecommerce form. `[adaptation]` sizing fear, fit fear and return hassle as ecommerce negative jobs is pass 1's mapping, not the book's. [e9fd545cfc45] [2174f296edbe] [2fd2d4d2c90b]

**R16. Distinguish the big hire (the purchase) from the little hire (each moment of use). Only repeated little hires prove the job is solved.** Most data tracks only the sale. Condition: an avatar is not confirmed until the brand sees repeat use or repeat purchase for that avatar's job. `[adaptation]` Pass 1 mapped big hire to first purchase and little hire to repeat order or subscription retention; the book never discussed ecommerce. `[needs brand data: repeat purchase rate per SKU and per stated avatar]` Source: 01 only. [ec89bc0904f5] [16f58e3ab952] [e5b43e1bd5d6] [1f4f02b0b6ad]

**R17. Even B2B and gift purchases carry emotional and social weight.** Mercer's pension buyers feared looking unprepared to a board. Condition: a brand with a B2B line or a gift-giving avatar still records the emotional and social dimensions; do not write a "rational buyer" record. Source: 01 only. [488785e75dab]

**R109. Split the avatar into an acquisition record and a win-back or churn record when the brand sells on subscription.** The acquisition record proves itself on the little-hire signal (R16); the churn record comes from loss conversations with lapsed subscribers (R58) and looks for a fixable reason, the way 02's "Chicken Box" example found a live-chat gap. Condition: applies only when the brand sells on subscription; a one-off purchase brand does not need the split. `[general practice]` the 2-record split is this pass's lever; 02-adrienne-barnes-on-best-buyer-personas.md gives only the general little-hire rule and 1 churn example, not the split itself. [2dfaff611f9a]

### 3.3 Where avatar candidates come from

**R18. Mine 5 lenses for jobs a feature survey will not show: your own life, nonconsumption, workarounds, negative jobs, unusual uses.** Each lens is a separate pass, not one technique. Condition: run all 5 in a first discovery pass for a brand; for each candidate log a verbatim quote and the trigger circumstance, not an inferred need. `[adaptation]` Pass 1 mapped nonconsumption to cart abandoners and category non-buyers, workarounds to return reasons and support tickets, negative jobs to checkout dread, unusual uses to review and UGC mining. Source: 01 only. [9662bde03a61] [a08d84e7c35c] [99ef75b0fbb2] [d9081272b7dd] [817a338fa0e1] [7da672f7f3e9] [37d2beb5692b] [d6900a22a7ef] [1cd731e1d547] [304df7bf3bc7] [081951aa2322]

**R19. Existing market: anchor the avatar on the brand's top customers. New offer or new market: anchor on competitors' ads and who they target.** 08 says top 20% of customers, compared across demographics, geographics and psychographics; it gives no ranking metric. 06 detects the dominant avatar from what customers say unprompted (about 95% "ecom brand owner" in his community). 04 starts from competitor ads and strangers' reviews because his products have no customers yet. Condition: if the brand has buyers, own-customer data is the anchor and public data is the supplement. If it has none, competitor and public data are the only anchor, and the record is marked provisional until real buyers confirm it. Sources: 08, 06, 04 (2 voices), with 02, 05, 07 and 09 all saying own customers are the strongest input. Conflict: C5. `[needs brand data: customer ranking metric and the top cut]` [cef3f6a44c44] [16074c80a9e5] [bccb9c4b4dab] [b399ed19a017] [083c7052a4f0] [e2f0e8697fe7] [6f9531c5c473]

**R20. Scan reviews for identity markers: "I am a...", "As a...".** "As a nurse, I'm on my feet all day and these On Clouds are amazing." Pull from 3 places: the brand's own reviews, competitor reviews, and a generic marketplace listing (06 names AliExpress for a low-review product). Condition: a marker that repeats across independent reviews is an avatar candidate; 1 mention is not. Source: 06 (1 voice). [a724805d3534]

**R21. A segment becomes an avatar when it repeats and grows, not when it fits a definition.** 06 refuses to define "avatar" and uses recurrence (the same phrase again and again in reviews or calls) as the test. Once the pattern holds, go 1 level deeper (not "ecom owners" but "ecom owners doing $100k/month+"). 05 and 03 give the same test from the other side: a single dramatic quote is not proof; a pattern across many independent answers is. Condition: no candidate enters the priority list on 1 quote, 1 review or 1 call. The playbook sets no number because no source gives one (section 6 marks this gap). Sources: 03, 05, 06 (2 voices). [14590ac68739] [6e03505404f7] [e2f0e8697fe7] [3db1dccaa8da]

**R22. Markets fracture into sub-avatars as buyers get sophisticated.** Buyers move from "run my ads" to "have you done this before" to "I want someone who only does my type". Athletic apparel split into gym clothing (Gymshark), which split into entrepreneur lifters, women only, misfits, a bench crowd (06's own reading of Alphalete, Buff Bunny, Anaka Power, Young LA, unverified). Weight loss is splitting into perimenopausal and postmenopausal women. Condition: applies to a category where generic attempts have already failed on buyers; not to a market still in the "just sell it to me" stage. Use it as a scanning lens: mass layer, niche layer, sub-avatar layer, next unserved slice. Source: 06 (1 voice). `[web check: current positioning of any named brand before reusing the characterization]` [baea6f8c2d2c] [736937000034]

**R23. Check the niche is big enough before committing.** 06's illustration: 100M+ gym-goers leaves room for many sub-niches; a 20,000-person parent market leaves a sub-niche of 100 to 1,000, likely too small to promote into. 04's burden of proof asks "are there enough of them". Neither gives a method beyond Reddit thread volume and a rough parent-market estimate. Condition: before locking a very narrow avatar, estimate parent market and sub-niche size and log the basis. `[web check: keyword volume, subreddit membership, category ad spend for the candidate]` Sources: 04, 06 (1 voice). The quantified demand check (search volume, TAM) is a pass 1 caveat, not a source rule. [58497983a714] [70b5dd026992] [09f09782497e]

**R24. In a saturated commodity category, differentiate with a new mechanism or a new avatar. Decide which first.** A genuine mechanism needs a real product difference (visual, mechanical or functional). Most AliExpress-style products have none, so the avatar route is the practical one. 09 states the same fork: a superior product or a much more specific avatar, ideally both. Condition: check the brand's product first `[needs brand data: mechanism audit]`. If a real difference exists, route to 01-PRD and 03-OFF and use this folder for the avatar layer only. If none, this folder's untapped-avatar pipeline (3.9) is the main lever. Do not claim a mechanism the product does not have (ecomOS: no invented claims). Sources: 04, 09 (1 voice). [0934edc554c3] [60a58f44e42d] [f6f18000b06c]

**R25. Map the mainstream avatar in the Meta Ad Library before ideating a new one, so you know who to avoid.** Search the product keyword, find brands that look like they are scaling (many variations, repeated creatives, professional production), watch the videos for the visible person's rough age, gender and body type, note the desires and USPs the creative leans on and whether it assumes product awareness. Repeat until the picture is stable. Condition: any new-avatar work in a category with active advertisers; skip when few competitors advertise (08 found this in knitting). This is a read of competitors' creative choices, not measured audience data; 04 calls his age read a "spitball". Sources: 04, 08 (2 voices). Ad Library is read-only. [b399ed19a017] [146bbf72ccfa]

**R26. An untapped avatar must clear a heavy burden of proof on 3 counts: real struggle, enough people, desperate want for the product's outcome.** Isolation alone is not a gold mine; it can mean the segment is thin. Check on Reddit by turning the review's detail into a plain search ("post C-section weight gain Reddit") and judging thread volume and recency. Condition: no candidate enters deep research or a creative brief before all 3 checks are logged with evidence. Source: 04 (1 voice). [70b5dd026992] [09f09782497e]

**R27. Buyers who already paid for a failed solution are the best prospects.** They believe the problem is real and they are still hunting. Signal phrase: "I spent thousands and it didn't work." Found in 1-star and 5-star reviews (05), forum comments with prices ($6,500 plus $5,000 on Neograft in 03), and live interviews ("I already tried X and it didn't do Y", lean in and ask more). Condition: tag every such quote as high-intent evidence in the record; it drives the failed-solution field (R38) and the belief sequence (R86). Sources: 03, 05, 09 (2 voices). [b08301158fb6] [326d0318ebcc] [2fd2d4d2c90b]

**R28. Segment by consequence, cohort and prior insecurity, not only by condition.** "Can't do my job" and "can't play sports" are different avatars for the same knee. A man already carrying self-esteem issues who starts balding is a different avatar from a man whose life is "put together". A 20-year-old and a 50-year-old with the same diagnosis use different words on different platforms. Condition: when research shows the same problem with different consequences, motives or cohorts, split the record. Sources: 03, 09 (1 voice); 01's circumstance rule (R3) supports the split. [de6f52d00231] [9b44ebb5a6e9] [912d3aa3c168] [e04fb9d3213c]

**R29. For a brand-new idea, place it in the demand matrix (price x number of customers) before deep research.** High-end (high price, few), golden goose (high price, many), mass market (low price, many), labour of love (low price, few: discard). The same idea can sit in different quadrants depending on format. It is a napkin estimate, not a measurement. Condition: new product or new offer only; skip for an existing SKU. Source: 05 only. Routing note: this overlaps 01-PRD's validation gates; use it here only to decide whether avatar research is worth running. [d113ec3fa69f]

**R30. Prefer passive data (the context of struggle) over active data (sales, CRM fields, benchmarks).** Active data is easy to get and describes outcomes. Passive data (what they tried, what frustrated them, what they rigged up) is hard to get and describes causes. Growing companies let active data crowd out passive data. Condition: a record built only from order data, RFM fields or platform demographics fails review (checklist 5.4). `[adaptation]` Pass 1 mapped passive data to support tickets, return reasons and review text. Source: 01 only. [da14b9693dec] [241ce7605df0] [e95a35c04ebc] [6c8e591b96b4]

**R31. Be first to serve a newly forming avatar in an adjacent category, not the crowded core product.** 06's hypothetical: cornhole is going mainstream; do not make boards; be the first clothing, supplement or drink brand for cornhole players, using products that exist elsewhere. Condition: a visibly growing recreational or lifestyle trend; the source gives no launch it ran. Source: 06 (1 voice), hypothetical. Routing: product choice belongs to 01-PRD; this folder supplies the avatar. [1fa73b0ea73b] [2bcb37305e50]

**R110. Segment avatars by AOV or price tier when the brand sells across a price range.** A budget-tier buyer and a premium-tier buyer for the same category are often different avatars with different objections and proof needs; run the demand matrix (R29) per tier, not once for the whole catalogue. `[general practice]` No library source; verify against brand data before use.

**R111. A marketplace-only seller with no CRM or first-party customer list is a third branch beside R19's existing-versus-new split.** It has sales but no reachable buyers to interview or survey; anchor on marketplace reviews, Q&A and the Ad Library (R19's new-market path) until a first-party list exists, and mark every record provisional until it does. `[general practice]` No library source; verify against brand data before use.

### 3.4 Research sources and how to mine each

**R32. Research comes before copy, creative, offer or launch, and depth scales with the stake.** 05 spends 60 to 80% of new-product time on research (his practice). 03 says a $1k day needs an avatar and a $10k day needs deep avatar knowledge (his belief, no data). 08 puts research as step 1 but says it is worthless without a strategy to apply it. Two gates before writing: the 30-second riff test (03: can you talk for 30 seconds unprompted on who the avatar is, their hopes, situation, problem and snap-fingers wish) and the 3 questions (09: what do they vent to a friend about, what have they tried, what promises are they sick of hearing). Condition: fail either gate and run P1 before any copy. Sources: 03, 05, 08, 09 (3 voices). [0d27b0e8ba75] [5d6b9c23511a] [46a98b023ad3] [16074c80a9e5] [f6f18000b06c]

**R33. Use several sources; one forum or one review set is an unrepresentative slice.** 02's 4 prongs (conversations, surveys, digital intelligence, social listening) must all run before segmenting. 09 says research in as many places as possible. 05 says desk research is incomplete without a real conversation because you cannot verify who is honest online. Condition: a record must cite at least 2 source types, and a record for a brand with buyers must include at least 1 first-party source (interview, survey, ticket or own review). The "at least 2" and "at least 1 first-party" numbers are this playbook's floor drawn from the 3 sources' direction; no source states a count. Sources: 02, 05, 09 (3 voices). [6d0a453de28f] [912d3aa3c168] [e2f0e8697fe7]

**R34. Read Amazon reviews by star rating, each band for a different signal.** 5-star first for what buyers genuinely like (05) and for identity markers (06). 3-star, and the 2 to 4 band, for structural, recurring complaints ("good for beginners but oversimplified") rather than taste (05). 1-star for explicit failure points, physical friction, broken trust markers and claims worn out by overuse (09). 1-star and 5-star together for the failed-solution buyer (05). "Top reviews" sorted, with the images or video filter, for long life-story reviews that seed new avatars (04). Read across the top 5 to 10 products in the category, not 1 (05). Condition: every review-mining pass logs which band each quote came from. `[verify UI: Amazon review sort and filter options]` Sources: 04, 05, 06, 08, 09 (3 voices). [46eec728bb7e] [b08301158fb6] [2fd2d4d2c90b] [083c7052a4f0] [a724805d3534] [8a7237ef9555]

**R35. Skip short generic reviews; prioritize long narrative reviews.** "Works great" rarely carries anything usable. A review that narrates weight history, surgery, stress, age or physical limits is a "gold mine". Condition: applies to review mining for avatar discovery; short reviews still count for tallying identity markers (R20) and star-band sentiment. Source: 04 (1 voice). [083c7052a4f0]

**R36. Discount "keyboard warrior" reviews and single contradictory voices; act on repeated patterns only.** A "nothing new here" review from someone who did not apply the product is a pattern to recognize, not a gap. When 2 reviews contradict ("too technical" vs "not enough science"), log both, decide later, and consider that 1 reviewer is not the market. Where possible find a synthesis (simple main text, technical appendix). Condition: no change to an avatar or a brief on 1 review. Source: 05 only. [fcf1bd930a6c] [46eec728bb7e]

**R37. Search forums with the avatar's own words, through Google, and read the comments.** Adopt the avatar's mind state and type what they would type: "my cat won't drink water, please help, Reddit", "hair loss making me less attractive Reddit", "reddit why don't you go to the gym". Add identity qualifiers ("men", "over 30") to sharpen. Let vocabulary in one thread guide the next query. Read the comments, not only the post; confession communities such as r/offmychest carry the rawest material. Use condition-specific subreddits and niche groups, not general feeds. When there is no CRM and no transcripts, 07 uses Reddit, LinkedIn and Instagram as a temporary, lower-confidence layer. Condition: every forum pass. `[web check: current subreddits and forums for the category; Google's surfacing of Reddit threads has changed since 05 (2018) and 08 (2022)]` Sources: 03, 04, 05, 07, 09 (4 voices). [f1ca3f6fbc70] [70b5dd026992] [6e03505404f7] [912d3aa3c168] [e7cebf3b70d1]

**R38. Reddit for emotional mechanics, Quora for tactics, and verify per category.** 05 finds Reddit works like anonymous confession (fear, shame, identity) and Quora skews to long how-to answers that hide the emotional block. In store terms, name the category subreddit for feeling (r/SkincareAddiction for a skincare brand) and the how-to subreddit for tactics (r/MaleFashionAdvice for a menswear brand). He says this is his experience, not a platform rule. 04 notes his AI deep research pulled from Reddit, Facebook and Quora alike. Condition: when a Reddit thread is tactical or a Quora thread is emotional, follow the content, not the label. Source: 05 only. `[web check: both platforms have changed since 2018]` [6e03505404f7] [be3576be73a2]

**R39. Capture quotes verbatim, never paraphrased, and keep the harsh wording.** Copy whole posts and comments into a plain doc with spacing. Bold or underline emotional language, named failed solutions, situational detail and self-descriptions. Screenshots are fine when a post is dense. Keep "do you hate and feel like your balding is making you look uglier", not a softened version. Do not script, scrape or AI-summarize at this stage (05). Condition: every research entry; the research evidence file (section 9) is the only place quotes live, and every quote carries its URL or record id and date. Sources: 03, 05, 09 (2 voices). Conflict: C3 (manual vs AI extraction). [3db1dccaa8da] [46a98b023ad3] [2fd2d4d2c90b]

**R40. Name the exact failed solution, with cost and extent when given.** "Minoxidil", not "hair supplements or drugs". "Fountains and water bowls", not "hydration products". "$6,500 Neograft on the hairline, $5,000 on the crown 6 months later." "Physical therapy that didn't address the core problem." "Multiple personal trainers." Condition: every avatar record lists failed solutions by name; a blank or generic failed-solution field means the research is not done. Sources: 03, 05, 09 (2 voices); 01's "what was fired" is the same field (R13). [326d0318ebcc] [b08301158fb6] [873f2122bf91] [e8e9e127d973]

**R41. Log the avatar's dominant emotional mind state.** Frustration, fear, anxiety, depression, guilt, embarrassment or shame. A drop shipper who wasted money feels frustration; an empty nester afraid of losing a pet feels fear. The state sets the copy register (R85). Condition: 1 dominant state per avatar; if 2 states split the evidence, that may be 2 avatars (R28). Source: 03 (1 voice). [dae729a4f6bb]

**R42. Track repeated words and counterintuitive benefit links.** If "motivation" keeps recurring across threads, run a follow-up search on that word. Write down unexpected links (weight loss to being more focused and goal-oriented; feeling at ease talking to people; being treated with more respect) and tag which sub-avatar feels each. Condition: after each batch of forum reading. Source: 05 only. [0017b1b018a4]

**R43. Google autocomplete and Keyword Planner show what people say they want.** Type the niche keyword without pressing enter, record every relevant suggestion, then type a promising suggestion as a new stem for the next layer. Size the terms in Keyword Planner's "discover new keywords" flow for the target countries, reading volume, competition and seasonality. Volume is an input, not a mandate. Condition: useful for messaging language, including the PDP title, meta description and ad headline, and for niche sizing; not evidence of buying. `[verify UI: Keyword Planner menu path]` Source: 08 only. [8ef3a86a5137] [771e65508b21]

**R44. Amazon autocomplete, book titles and reviews show what people actually buy, and behavioral evidence weighs more than stated wants.** Amazon suggestions reflect shopping, not information seeking. Book titles and subtitles are pre-optimized headline language because a book takes longer to produce than a post; if the niche has no books, use the most optimized listings. Review counts are a rough proxy for relative sales, explicitly a guess. Cross-check the miracles and miseries list against what showed up in reviews. Condition: when Google interest is high and Amazon buying is thin (or the reverse), weight Amazon for offer and product decisions and Google for language. Source: 08 only. [bb02448d1007] [8a7237ef9555] [f33468b23555]

**R45. Meta Ad Library: read who competitors speak to and which ads run longest, as a screening signal only.** Path in 08: competitor page, Page Transparency, "see all", "go to ad library". Ads that recur across a scan and ads near the bottom of the feed (longest running) are more likely profitable, and 08 says outright "that's not always the case", so corroborate with reviews and keyword demand before adopting an angle. Adapt the angle; never copy text, images or offer. Condition: any competitor scan; ecomOS rule applies (signals, not proven winners; layout and mood only). `[verify UI: Page Transparency to Ad Library path]` Sources: 04, 08 (2 voices). [146bbf72ccfa] [0ea951a84570] [b399ed19a017]

**R46. Competitor sites reveal sub-markets through imagery, tone and headline, and read headlines for the constraint and reward they encode.** One fitness site speaks to aggressive testosterone buyers, another to "normal out-of-shape guys", a third to "nerds, misfits and mutants", a fourth calls out "skinny fat guys" and separates "us" from "regular guys". "An hour's worth of results in 25 minutes" encodes a time-poor buyer. Polished, profitable-looking competitors support the category; amateur competitors across the board are a category warning. Condition: early in a new-market pass, after natural-language Google searches for the problem. Source: 05 only. [c97ccae24606] [3e4fe752116b] [2ce06b2439fa]

**R47. Map sub-avatars through social content.** Search broad category terms on TikTok ("bodybuilding", "CrossFit", "gym clothing"), study the distinct groups posting, trace mass layer to niche to sub-avatar, and note how each brand marks identity: creative style, product design, language, who it uplifts (sponsors, features, sends to events). Pick a sub-avatar the brand can signal consistently across all of those at once. Condition: any category with visible social communities. Source: 06 (1 voice). [736937000034]

**R48. Confirm "Where" with platform demographic data and cohort-specific phrasing.** Search "social media demographics" and check the avatar's profile against each platform's skew before placing content or ads. Pull phrasing from where that cohort actually posts; TikTok phrasing aimed at a 50+ audience is 09's named mistake. 09's cohort-to-platform map (50+ on Facebook groups and Amazon, younger on TikTok) is his illustrative guess, not research. Condition: every record's Where field cites the data it used. `[web check: current platform demographics for the brand's countries]` `[needs brand data: actual platform use by cohort from the brand's own analytics]` Sources: 08, 09 (2 voices). [e6c10689be00] [9b44ebb5a6e9]

**R49. Digital intelligence and social listening show how the audience behaves at scale, never why.** 02's tools: SparkToro and "Audience" for which platforms the audience uses and which influencers shape it; IBM Watson-based data for buying mindset (fast vs slow decider, risk-taker vs conservative, self-serve vs wants support); Brand24 for social listening on the category's topics, pains and frustrations, not the brand's own mentions. Condition: run on the wider audience, separate from the interviewed sample; use it to fact-check whether interview themes match public conversation. The buying-mindset axis "needs a sales team vs self-serve" is B2B; `[adaptation]` this pass suggests "impulse vs considered, single item vs cart-building" but 02 does not say that. `[verify UI: SparkToro, Audience, Brand24, Watson-based data availability]` Source: 02 only. [5a83b6bd8cad] [bf1e76633e2e]

**R50. Cross-check what people say against what they do; a mismatch is signal, not noise.** Conversations give the why; digital data gives the how. Google gives stated want; Amazon gives purchase. Keep both in the record and note the gap. Condition: every record built from more than 1 source type. Sources: 02, 08 (2 voices). [2fac02da19a5] [f33468b23555]

**R51. Interviews are necessary because online answers cannot be verified, and depth beats breadth.** People give answers they think others want to hear, even anonymously (05). An online stranger cannot be confirmed as a paying customer; the store's own order data can filter interview invites to real buyers. A small number of rich interviews beats a large number of shallow data points for finding the causal job; quantitative follow-up confirms prevalence (01). 07 calls interviews the fastest high-value source once you start. Condition: any brand with reachable buyers runs interviews; a brand with none marks its records provisional (R19). Sources: 01, 02, 05, 07 (4 voices). [c4d6dd183e5b] [f13714393d43] [e2f0e8697fe7] [6f9531c5c473] [2534ec17bc50]

**R52. Interview counts: start with 5, aim for about 20, keep going forever.** 07: top 5 customers, 30 minutes each, as a fast start, not validation. 02: about 20 conversations of 30 minutes, citing a claim from "Deploy Empathy" attributed to Nielsen that 20 cover about 97% of audience sentiment `[web check: original claim]`. 05: at least 1 conversation a week, 1 hour blocked. 09 and 02: calls continue as a permanent practice, not a study. 01: cluster before acting; 1 interview is 1 data point. Condition: tie the count to the store's own purchase window (recent buyers, buyers past the return window, lapsed subscribers) rather than a generic sample size. 5 interviews may open a record; 20 is the bar before segmenting a market into several avatars; no number of interviews replaces the first-party review and ticket data. All counts are practitioner heuristics (section 6). Sources: 01, 02, 05, 07, 09 (5 voices, different numbers, not contradictory). [6f9531c5c473] [2534ec17bc50] [6d0a453de28f] [e2f0e8697fe7] [99043b84fe3d] [c4d6dd183e5b]

**R53. Frame every interview as exploratory, never as sales or support.** In the scheduling email and again at the start: you are not a product expert, you cannot solve their problem, this is not a demo or upsell, here is exactly how long it takes. Condition: every interview invite and opening. Source: 02 only for the explicit framing; 05's lateral questions and 07's "conversational, not a survey" agree. [2534ec17bc50] [e2f0e8697fe7] [6f9531c5c473]

**R54. Interview on the timeline and the struggle, not on product attributes.** Reconstruct the purchase timeline from the first thought of buying: when, where, with whom, what else was happening. Phrase it in store terms: first saw the ad, added to cart, abandoned, came back, checked out. Ask nothing about coils, colour, firmness or price. Probe when the little hire started failing, what was fired, and the 4 forces. Ask lateral questions ("Have you thought about X? How do you think about it? Who else do you know who did this? Why did they?"), never a pitch or a yes/no on the idea. Ask what surprised them. Ask about their full journey and emotions (02). Condition: every interview; the script is P11. Sources: 01, 02, 05, 07, 09 (5 voices). [da4191b7964a] [ab9f2f70e75c] [bd5e6104db6d] [d064d50c8bc4] [e2f0e8697fe7] [2534ec17bc50] [99043b84fe3d]

**R55. Match the incentive to the person.** Regular customers: a t-shirt, early or beta access (02's example: 3 months). Busy, senior or high-earning people: a charitable donation in their name ($30 for 30 minutes in 02's own validation), never cash, because cash turns the ask into a rate negotiation. Condition: every recruit; ecommerce brands can substitute product or store credit for the t-shirt `[adaptation]`. Source: 02 only. [70460b582ffd]

**R56. The booking rate is itself a signal.** Customers who love or hate a product want to talk. If very few book, the segment may lack strong feeling toward the product; reconsider the segment or the incentive rather than only the outreach copy. Fear that interviews cause churn is, in 02's experience, almost never founded (her recollection, not audited). Condition: track bookings per invite batch (checklist 5.3). Source: 02 only. [2534ec17bc50]

**R57. Direct calls and DMs to buyers run continuously, and ask what surprised them.** 09 cites an acquaintance's "nine-figure" team that still calls customers to ask how things are going (unverified). DM outreach is called underrated. 06 holds one-on-one and group calls and listens for unprompted self-description. 02's Triple Whale hosts put everyone on customer calls. Condition: a standing weekly slot, not a one-off study `[needs brand data: which DM channel buyers use]`. Sources: 02, 06, 09 (2 voices). [99043b84fe3d] [bccb9c4b4dab] [5d0d40c930ec]

**R58. Ask churned and lapsed customers why they left, directly.** Do not infer from usage or attribution data alone. 02's example: a subscription business learned customers left partly for lack of support access and added live chat. Condition: ongoing, tied to retention monitoring. `[adaptation]` This pass calls the ecommerce form a loss interview (lapsed subscribers, refund requesters, cart abandoners who answered an email); the win side (why did you choose us) comes from 07's call transcripts and 06's survey question "what specifically works for you". No source uses the phrase "win or loss". Source: 02 only. [2dfaff611f9a]

**R59. Surveys verify and scale what interviews found; they do not discover, and their wording is fragile.** 02: design the survey after analysing interview themes; use it to verify trends at scale and to collect structured facts (in B2B: role, tenure, company size, buying authority). 06: a free Google Form to existing buyers asking how they describe themselves (role, family role), what specifically works, what their situation is; look for identity plus mechanism pairs that repeat. 09: an automated Shopify post-purchase survey plus email follow-up asking about day-to-day friction and restricted activities, in the same categories as reviews and calls so results compare. 08: positive-to-negative rephrasing, leading questions, question order and the survey description all skew answers; "how awesome is our hard-working support team" is a leading question. Condition: a survey may confirm or count; it may not be the first or only source for a new avatar. `[adaptation]` consumer structured facts (household situation, purchase occasion, first vs repeat, who it was for) are this pass's suggestion; 02 gives no consumer list. `[verify UI: Shopify post-purchase survey apps; Google Forms limits]` Sources: 02, 06, 08, 09 (3 voices). Conflict: C2. [d7d12982e3e6] [d287ab9044c4] [99043b84fe3d] [42ca0e985030]

**R60. Do not run feature-request surveys or focus groups to find jobs.** They produce wishlists, not jobs, because they ask people to invent solutions (01: Intuit's 150-feature list; one focus group rejected American Girl). Focus groups are expensive, shallow and prone to moderator bias (08). Condition: applies to discovery, including a PDP feature-vote widget or a reviews-page poll, not only a room-based focus group. Neither source bans a well-built verification survey, and 07's "on-demand focus group" is an LLM query tool, not a room of people (R66). Sources: 01, 08 (2 voices). Conflict: C2. [d125c1d8df51] [b5a6783a503a] [42ca0e985030]

**R61. Mine sales and support transcripts, tickets and return reasons as passive data.** 07's data layer: call transcripts for recurring pains, company types and who seeks information; CRM fields; surveys; social. 01's workaround lens maps, per pass 1, to tickets describing jury-rigged use, reviews saying "I use this for X instead", and return reasons that reveal an unmet job `[adaptation]`. Condition: any brand with a helpdesk or returns log includes this pass; tag each theme with count and date. `[needs brand data: ticket themes, return reason codes, cancellation reasons]` Sources: 07 (rule), 01 (adaptation). [ff3969ab7ccb] [d9081272b7dd] [da14b9693dec]

**R62. Storyboard the struggle to reveal the forces.** Use "Once upon a time... Every day... One day... Because of that... Finally I did..." Map discrete emotional moments across the journey (Airbnb mapped 45 for hosts and guests before launch) including the first little hire (arrival at the home). For a store, map the journey as: ad or search, PDP visit, cart, checkout, unboxing, first use, repeat or subscribe. Condition: after interviews, before writing the record; the storyboard becomes the trigger-moment and forces fields. Source: 01 only. [63c8da8b3648] [df9261a8fe1b] [cb4347c65db1]

**R63. Record trigger moments as discrete, datable events, and cover life events plus daily schedule.** 01: capture the moment as a datable event, not a mood. 08's "When": life events (marriage, divorce, new child, new job, moving) shift buying; daily schedule (9-to-5, stay-at-home parent, home entrepreneur) shifts when and where they consume and buy. 03: the sharpest trigger in the hair-loss research was public exposure (a friend pointing it out in front of a room). Condition: every record has at least 1 quoted trigger event. Sources: 01, 03, 08 (3 voices). [e2bb9a4021c5] [826d0e12dcda] [dae729a4f6bb]

**R112. Check platform, language and payment habits for the brand's actual market before reusing any source's platform read.** Every named platform and forum in this folder (Reddit, Amazon, TikTok, the Ad Library) is treated as US and English-language; a mobile-first or India-facing brand should check WhatsApp, cash-on-delivery behaviour and regional platforms instead of assuming Reddit or a US demographic split applies (R48). `[general practice]` No library source; verify against brand data before use. `[web check: platform and payment habits for the brand's country]`

### 3.5 AI research and LLM personas

**R64. Do the manual reading first; use AI after, once you can judge its output.** 03: AI tools (Gemini, ChatGPT, Claude) have "unmatched efficiency" once you know what you are looking for, and are a crutch when you do not, because polished output is easy to mistake for understanding ("answering emails and thinking you're productive"). The crutch risk is AI research run before the operator has read this brand's own reviews and tickets, not research generally. 05: do not script, scrape or AI-summarize reviews and threads at this stage; it strips nuance and exact vocabulary. 04 and 07 run AI research and synthesis as core steps (R65, R66). Condition: an operator or agent that has not completed at least 1 manual sprint (P1) for this brand and category may not run AI deep research as the source of an avatar. After a manual sprint, AI may accelerate and extend, and the manual quotes are the check on it. Sources: 03, 05 for the rule (2 voices); 04, 07 against (2 voices). Conflicts: C3, C4. [4e2d70bdca59] [46a98b023ad3] [be3576be73a2] [ba49787189ec]

**R65. When running an AI deep-research report, fix the prompt, change only the avatar field, and click through every cited source.** 04's run: ChatGPT or Gemini deep research mode, one template prompt (linked in his video, not in the transcript `[web check]`), about 22 minutes, a 30-plus page report (39 exported) with claims tied to public sources (Reddit, Facebook, Quora). Read the report, then open the citations rather than trusting the summary. Gemini pulled more sources than ChatGPT in his 1 comparison (1 anecdote). Condition: the report's quotes may enter the research evidence file only after the agent has opened the cited page and confirmed the quote exists there; an uncited or unverifiable quote is discarded (ecomOS: no invented quotes). The bare-bones sketch from ads, reviews and Reddit is not an avatar; the report is the avatar's draft, and real buyers confirm it (R19). `[verify UI: deep research toggles]` Source: 04 (1 voice). [be3576be73a2] [208f632d3ddc]

**R66. An LLM may synthesize the brand's own transcripts, surveys and data into a draft record, and the draft is reviewed against the raw transcripts before it counts.** 07: upload 5 call transcripts, survey results, CRM fields, content performance and the brand's own product and pricing into a dedicated project (ChatGPT or Claude); ask who am I speaking to, what are their pains, what recurs; ask it to define the ICP. Review against sources; it compresses synthesis, it does not replace judgment. Condition: inputs are first-party or verified public quotes only; the model may not add "typical" quotes; the output cites the transcript id for every claim. `[verify UI: project and knowledge-base limits and sharing]` Source: 07 only. [ba49787189ec]

**R67. A live LLM persona is a QA tool for directional questions, built only from real data, and it does not replace customer contact.** 07 keeps the persona as a queryable project used on every campaign: would this resonate, would she hate it, how should I position, what words. Ask directional questions, not yes/no. Use it to align new hires. Condition: the persona project loads only the brand's avatar records and evidence file; every answer it gives is a hypothesis to check against quotes, never a new quote; the brand brain (3.10) is the ecomOS version. 03's crutch warning (R64) applies. Source: 07 only. Conflict: C4. [d7c43255dc6e]

**R68. Set content altitude per avatar from its actual experience level.** 101 for a novice, 301 for someone who already runs the thing. In store terms: PDP copy runs at 101, a retention email at 301, matched to the buyer's experience. Feed the model audience context plus content performance so the call is grounded. Covering both altitudes is fine; the mistake is not deciding. Condition: applies to content and email briefs more than to ads; record the avatar's experience level with the category as a field. Source: 07 only. [8cf79dbd3fd4]

### 3.6 The avatar record and its validation

**R69. Minimum record: quoted evidence, a trigger moment, a job statement.** All 4 sources that give a record standard agree on these 3. A draft that is demographic fields with no job is rejected. Condition: no record leaves this folder without all 3; checklist 5.4 enforces it. Sources: 01, 02, 03, 09 (4 voices). [294308de8309] [83486686c828] [ef0ecef3dfbb] [c5efc108c9c9]

**R70. Every quote traces to a real source, and reviewer identities are minimized.** ecomOS rule: each quote carries its URL or record id, date and source type. 04 raises the ethical line himself: log "Anna Z", not the reviewer's full name or identifying detail beyond what the profile needs. Condition: always. A brand's own interview quotes carry the interview id, consent status and whether the customer allowed quotation in marketing. `[needs brand data: consent terms for using interview quotes]` Sources: 04 for minimization (1 voice); the traceability rule is ecomOS. [083c7052a4f0] [294308de8309]

**R71. Full record fields, merged from 04, 08 and 01.** Identity and demographics (context only, R8). Avatar synopsis. Day-to-day struggles. How the problem makes them feel and the dominant emotional state (R41). Their own words for it (verbatim, R39). Failed past solutions by name and cost (R40). Limiting beliefs. Existing beliefs about solutions and competitors. Core identity beliefs, attitudes, hopes and dreams. The 5W: Who (top-customer patterns), What as 2 lists, miracles (wants, dreams, goals, desires) and miseries (fears, frustrations, pains, problems), When (life events and daily schedule), Where (online and offline, checked against platform data), Why (each benefit chained to personal motivation). The job spec: functional, emotional, social progress; tradeoffs the customer accepts; full competitive set including nonconsumption; obstacles and anxieties at purchase and at use (R72). The 4 forces. What was fired. Trigger event. Consequence segment and cohort (R28). Experience level (R68). Who it is not for (R73). Priority and evidence count. Condition: all fields present, and each field either cites evidence or says "no evidence yet". Sources: 01, 04, 08 (3 voices). [2b67b2edcb1a] [16074c80a9e5] [32ce1018d3e2] [826d0e12dcda] [e6c10689be00] [e35f8fec52f0] [e30632499b68] [fddf69615826] [88dec6a091ff]

**R72. Write objections as anxieties, each paired with what removed it in a real purchase.** The job spec lists obstacles at purchase and at use. 01's examples: a lenient return policy, a spouse touching the mattress, a real campus. 09's 1-star mining supplies broken trust markers and exhausted promises. Condition: an objection with no evidence of what removed it stays flagged for the offer agent (03-OFF) and landing page agent (07-LPG) to test, not for copy to assert. Sources: 01, 09 (2 voices). [2174f296edbe] [e9fd545cfc45] [b8edb10a0fa1] [2fd2d4d2c90b]

**R73. Say who the product is not for.** Reviews work as job-matching evidence: buyers look for reviewers with their job. A wrong-fit buyer leaves a lasting bad review, so product pages must let them self-select out. 06's version: someone outside the avatar who lands in the funnel should feel in the wrong place and leave. Condition: every record has a "not for" line and the brief carries it. `[adaptation]` PDP review curation by use case is pass 1's mapping of 01. Sources: 01, 06 (2 voices). [741dd2ac873a] [541818498033] [746f5e6fba38]

**R74. Miracles feed aspiration and promise; miseries feed problem agitation and objection handling. Keep them specific.** "Wants better quality" is generic; items drawn from review language are usable. Condition: both lists in every record, each item quoted. Source: 08 only for the split; 03 and 05 supply the specificity rule. [32ce1018d3e2] [3db1dccaa8da] [46a98b023ad3]

**R75. Chain each benefit to why it matters to this avatar, and check the avatar actually benefits from this offer, not the category.** Store example: "faster charging" leads to "less morning stress" leads to "not late for school drop-off." The chain (feature to benefit to personal motivation) decides which benefit leads (R93). Condition: the Why field of every record. Source: 08 only. [e35f8fec52f0]

**R76. A record that is not used is a failed record. Audit use.** 02's own survey (tool "Audience", no sample given): about 90% of marketers create personas, 77% never use them for a launch, campaign or copy. 07: a persona that lives in a slide deck nobody reopens is the named mistake. Condition: each quarter, list which PDP copy, ad briefs and email flows cited which avatar record by name; a record cited by nothing is reviewed or retired (P28). The label (persona, avatar, buyer insights) does not matter; adoption does. Sources: 02, 07 (2 voices). [6f03704d60e9] [d7c43255dc6e]

**R77. No sensitive-attribute assertions in anything handed to creative.** 03's method names baldness, terminal pet illness and self-esteem in hooks and never mentions Meta's rules on personal attributes and health. ecomOS rule: the record may hold what people said; the brief may not tell a viewer they have a condition, a body type, a financial state or a protected attribute. Write the situation ("post-op knees hurt" as a quoted forum line the creative may echo as a story), not an assertion about the viewer. Condition: always; the creative brief check (checklist 5.5) blocks the handoff. `[web check: current Meta advertising standards]` Source: 03's own caveat (1 voice); the rule is ecomOS.

**R78. The preliminary sketch is not an avatar.** The profile built from ads, reviews and Reddit alone is "very bare bones and surface level" (04). A record built from a first sprint (03) is enough to audit copy against, not enough to define a scale attempt (R32). Condition: mark every record "provisional" until it has first-party confirmation (R19) or, for a brand with no buyers, until the deep research report is verified (R65) and the first real buyers are interviewed. Sources: 03, 04 (1 voice). [208f632d3ddc] [5d6b9c23511a]

**R113. Write fit, size and return-reduction copy into the avatar record and the angle map.** R15 already names sizing and fit fear as an ecommerce negative job, but no source carries it through to a deliverable. Add a size-guide or fit-confidence angle to D5 wherever the record's anxieties include sizing or fit. `[general practice]` the deliverable step is this pass's lever; R15's fear-naming is the only source material. [2fd2d4d2c90b]

### 3.7 Persona count, priority and the ICP question

**R79. Inventory candidates before fixing the number of avatars.** 01: list every job candidate first. 09: the 3 required elements are universal, the number of avatars is not. 02: count varies by business and gives no rule. Condition: never start from "we need 3 personas"; start from the candidate list and let evidence decide. Sources: 01, 02, 09 (3 voices). [41ede02e56d1] [c5efc108c9c9] [f6f18000b06c]

**R80. Do not average conflicting jobs into 1 avatar.** The Air Force designed a cockpit for the average of 4,000 pilots and it fit none. SNHU's one-size recruiting failed both its jobs. The milkshake chain needed 2 fixes, not 1 averaged change. Condition: when evidence splits by circumstance, consequence, cohort or emotion, split the record (R3, R28). Sources: 01, 03, 09 (2 voices). [ba25422e25e4] [184aad3cbf8b] [e04fb9d3213c] [de6f52d00231] [9b44ebb5a6e9]

**R81. Narrow and deep beats broad and shallow, after the size check.** Going all in on 1 avatar lets creative, marketing and systems tune to it; spreading across many keeps everything generic. 06 states this as his preference, not a proven rule, and 06's own size check (R23) bounds it. Condition: a brand serves 1 primary avatar per product line at a time in creative and pages; further avatars are tested one at a time as untapped candidates (3.9). Source: 06 (1 voice). [baea6f8c2d2c] [58497983a714]

**R82. Priority order for an existing brand: dominant avatar first, then the highest-evidence untapped candidate. For a new or commodity product: the least-served candidate that clears the burden of proof.** 06 and 08 anchor on the brand's dominant or top customers. 04 ranks candidates by least existing paid competition, only after the 3 proof checks. Neither source gives a scoring formula. This playbook's priority record (section 9) therefore lists, per candidate: evidence count by source type, first-party confirmation yes or no, competition read from the Ad Library, size basis, and the 3 proof checks, and the agent ranks by those columns in that order. The column order is this pass's choice, drawn from R19, R26 and R33. Condition: any brand with more than 1 candidate. Sources: 04, 06, 08 (2 voices). Conflict: C5. [bccb9c4b4dab] [cef3f6a44c44] [09f09782497e]

**R83. Re-run the dominant-avatar check periodically; the mix shifts.** 06 re-checks who his community says they are and re-points content. 06 also warns that a dominant avatar in the existing base is not proof it is the largest available market. 09 calls one-off research a mistake. Condition: at least each quarter or after any major channel or product change; the cadence is this playbook's suggestion, no source gives one. Sources: 06, 09 (1 voice); 02's "keep asking" agrees. [bccb9c4b4dab] [99043b84fe3d] [5d0d40c930ec]

**R84. Use the TAM, ICP, persona taxonomy only for a B2B line.** Moved to Appendix A: the taxonomy detail (07's TAM, ICP and persona fields; 02's B2B survey fields). Condition: a consumer brand does not build an ICP layer; its "ICP" is the priority avatar (R82). A brand with wholesale, corporate gifting or B2B lines builds the ICP layer for that line only. Do not invent a consumer ICP schema and call it 07's method. Sources: 02, 07 (2 voices). Conflict: C7. [a1faffe60195] [834684cbb868] [d7d12982e3e6]

**R85. The "who" for a gift or a proxy purchase is 2 avatars: the buyer and the user.** `[adaptation]` This pass derives it from 01's rule that B2B and proxy decisions carry their own social weight (R17) and 01's childcare example; no source states a gift rule. Condition: when reviews or interviews show the buyer is not the user, record both jobs and mark which one the creative speaks to. Source: 01 (adaptation). [488785e75dab] [782e3f599df4]

**R114. Add research depth for a considered purchase or a long sales cycle.** 02 names "impulse versus considered, single item versus cart-building" as a gap it never fills [`bf1e76633e2e`]. For a considered-purchase store, extend the interview timeline (R54) to cover every research and comparison step before the cart, not only the moment of purchase. `[general practice]` extending the timeline is this pass's lever; 02-adrienne-barnes-on-best-buyer-personas.md names the gap but gives no method.

### 3.8 Avatar to creative and avatar to funnel

These rules end where 10-MCR, 11-ADC and 07-LPG begin. They say what the avatar hands over and what the receiving agent must keep congruent; they do not write the hook.

**R86. Copy reuses the buyer's own phrasing; the marketer does not brainstorm it.** "You don't reinvent the wheel." Carry exact phrases from reviews, threads and calls into the pre-lander, page and creative. Condition: the angle map (section 9) pairs every angle with the quotes it came from; a line with no source quote is flagged as invented. Sources: 03, 05, 09 (2 voices). [2fd2d4d2c90b] [9b44ebb5a6e9] [3db1dccaa8da] [46a98b023ad3]

**R87. The dominant emotion sets the copy register.** Frustration copy calls out wasted effort and broken promises. Fear copy speaks to loss, worst-case outcomes and protection. Writing one register to both is a mistake. Condition: the brief states the register with the quotes that justify it. Source: 03 (1 voice). [dae729a4f6bb]

**R88. A hook needs understanding before curiosity: name the exact situation first.** 03's rebuild: "Two women whose cats don't drink water. It seems innocent, but could be the reason you lose your last companion a few years too early." Parts: situational call-out, curiosity mechanic, deepest fear, identity phrasing ("last companion" signals empty nester without stating it). 09: open by naming the situation ("do you have a post-op knee?"), then the lived scenario, the named failed solution, briefly why it failed, then the mechanism, shown not asserted. Condition: the brief supplies situation, failed solution, why it failed and the fear, each with quotes; R77 applies to how the situation is phrased. Sources: 03, 09 (1 voice). [301d338a9f16] [873f2122bf91]

**R89. Avatar fit runs through the whole funnel, not only the hook.** Change the creative's setting (a roof, not an office), the page's proof (only that avatar's results), the product photos, every claim, the sales conversation. Keep the same named condition and journey across ad, pre-lander and page; naming a patellar tendon graft in the ad and arthritis on the page is a conversion killer (09, no numbers). Test: someone outside the avatar should feel in the wrong place and leave. Condition: the handoff to 07-LPG and 10-MCR includes a congruence line the receiving agent signs off (checklist 5.5). Sources: 06, 09 (1 voice). [746f5e6fba38] [873f2122bf91] [4af92fa26772]

**R90. Proof shown to an avatar comes only from that avatar.** No mixed or generic case studies or reviews on the avatar's page. Condition: the record lists which reviews and results belong to this avatar `[needs brand data: reviews tagged by avatar]`. Source: 06 (1 voice). [746f5e6fba38] [4af92fa26772]

**R91. The creative carries the avatar; targeting stays broad.** 06 keeps Meta targeting broad after niching and relies on the algorithm to find the audience from creative performance, so generic creative under broad targeting gives the algorithm nothing. 09's pass 1 note: the narrowing is about messaging, not ad-set targeting. Condition: this folder never prescribes an audience setting; it prescribes that the creative, not the targeting, must signal the avatar. Targeting decisions live in 24-DEP and 11-ADC. `[verify UI: Meta delivery behaviour]` Source: 06 (1 voice). Conflict: C6. [af1c969a5868]

**R92. Avatar framing is part of the offer.** Shifting "knee pain" to "enjoying your youth and running again" makes a generic product feel bespoke without changing it. Condition: the record's Why chain and miracles list go to 03-OFF as inputs; 03-OFF owns the promise. Source: 09 (1 voice). [a968d0d00a11]

**R93. The benefit that leads is the one whose Why chain is strongest for this avatar.** Condition: the angle map ranks benefits by the strength and count of quoted motivation behind each. Source: 08 only. [e35f8fec52f0] [0017b1b018a4]

**R94. Audit existing and AI-written copy against the research and cut what is off.** Expect lines that are not what the customer wants, not how they describe it, or the wrong emotion ("my product test failed" vs "I launched and got $200 CPMs"). The gaps become the next test list. Condition: after every sprint (P1 step 13). Source: 03 (1 voice). [4e2d70bdca59]

**R95. Stalled creative testing is usually a research gap, not an execution gap.** Test after test with nothing scaling ("in copium") means restart at review, forum and call mining before more variants. 03 opens by dismissing ad-set counts and cost caps as the wrong question. Condition: a diagnosis to raise with 10-MCR and 24-DEP, not a certainty; check the brand's test log first `[needs brand data: test history]`. Sources: 03, 09 (1 voice). [f6f18000b06c] [5d6b9c23511a] [0d27b0e8ba75]

**R115. Match an influencer or UGC creator to the avatar, not to reach alone.** 06 gives only background on Gymshark's creator sponsorships [`58497983a714`], with no matching method. Check a candidate creator's own audience and content against the avatar's job, trigger and register (R87) before a brief goes out. `[general practice]` the matching step is this pass's lever; 06-how-to-create-avatars-that-scale-facebook-ads.md gives no method to draw from.

**R116. Turn objections and failed solutions into support scripts or macros for the avatar.** 02's live-chat fix (R58) shows support content closing a gap the record found. Hand the record's objections (R72) and named failed solutions (R40) to 17-CXP as draft macros; support writes and owns the final wording. `[general practice]` the macro handoff is this pass's lever; 02's example is the only source material. [2dfaff611f9a]

### 3.9 Untapped avatar discovery for scaling paid social

**R96. Run the 4-step pipeline in order: Ad Library map, Amazon outlier reviews, Reddit validation, then deep research on 1 prioritized candidate.** Yield target: 3 to 4 candidates from reviews before deep-diving any one. Keep adjacent pockets found on the way as a backlog (04's undeveloped example: men around 65 with mobility limits). Condition: a saturated category with no real mechanism difference (R24). Each step's output is a section of the untapped avatar shortlist (section 9). Source: 04 (1 voice). [b399ed19a017] [083c7052a4f0] [70b5dd026992] [208f632d3ddc] [09f09782497e] [be3576be73a2]

**R97. Rework a proven mass-market play for 1 avatar, every layer.** Start from a product and angle other brands already prove, study their working ads, rewrite claim, creative concept, page structure, primary text, even the business name or framing for 1 avatar, and show only that avatar's results. 06's student example: a reported 5x day-one ROAS (1 anecdote, unverified). Condition: ecomOS competitor rule applies: study what the ads claim and show; never copy text, images, products or faces. Source: 06 (1 voice). [4af92fa26772] [2bcb37305e50]

**R98. Quantify demand before committing spend to a new avatar.** "A pretty decent amount" of Reddit threads is 04's only sizing. Pass 1 flagged that common practice wants keyword volume, category ad spend or a small paid test first. This is a pass 1 caveat, not a source rule. Condition: the shortlist carries a demand line (Keyword Planner volume from R43, subreddit size, competitor traffic from SimilarWeb in 04) and the media agent decides the test size. `[web check: SimilarWeb access]` Sources: 04's own gap; 08's Keyword Planner supplies the method. [70b5dd026992] [771e65508b21] [b399ed19a017]

### 3.10 How avatars feed the brand brain

**R99. The avatar record, evidence file and angle map are brand brain inputs, not a PDF.** 07's live persona project (R67) is the closest source: one place every brief queries. 02: one output serves marketing, product, sales and success. 01: a clear job statement is a "commander's intent" that lets people decide without asking (OnStar waiving fees in a hurricane, SNHU staff buying a student groceries). `[adaptation]` The ecomOS brand brain is not built yet; this rule defines what this folder will feed it. Condition: every record is stored with its evidence and its use log; the brain answers "which quotes support this line" not "what would the avatar say". Sources: 01, 02, 07 (3 voices). [d7c43255dc6e] [83486686c828] [51230f4f32c9] [2c9eb2206eeb] [583f1aa39218]

**R100. Push everyone into customer contact, and keep asking.** Talking to first customers and continuing to talk to them is permanent practice for a plumber, a farm, SaaS or DTC (02). For a store, lead with the roles that should join calls: support, fulfilment, retention or email. Condition: the brand brain logs who spoke to a customer and when; a quarter with no new first-party evidence downgrades every record's confidence. Sources: 02, 09 (2 voices). [5d0d40c930ec] [99043b84fe3d]

**R101.** Moved to Appendix A: organisational-design measurement examples (SNHU and the brain's 2 reported numbers).

**R102.** Moved to Appendix A: purpose-brand long-horizon theory (FedEx, IKEA, Volvo, V8).

### 3.11 ecomOS rules that override any source

**R103. No invented claims, no invented quotes, every quote traceable.** See section 0. A record or brief that fails this is rejected regardless of source. Basis: ecomOS; supported by 01 [294308de8309], 03 [ef0ecef3dfbb], 09 [c5efc108c9c9].

**R104. No sensitive-attribute claims that breach Meta policy in any handoff.** See R77.

**R105. Brand record and data layer win over any source figure.** The 20% cut, the 95% dominant share, the 5 or 20 interview counts, the 60-minute sprint, and every revenue claim in 03, 04, 06 and 09 yield to what the brand's own data shows. Where the brand has no data, the record says so.

**R106. Competitor ads and sites are signals, not proven winners.** Long-running is a screen (R45). Polished sites are a category read (R46). Use for who is spoken to, layout and mood. Never copy text, logos, products or faces.

**R107. Meta is read-only; research uses the Ad Library and read tools.** No custom audiences, no uploads, no targeting changes from this folder.

**R108. Keep brands apart and keep public research separate from private data.** One research evidence file per brand. Public forum quotes and private interview quotes are labelled by source type and never mixed into a cross-brand doc.

## 4. Procedures (implementation)

Each procedure: goal, preconditions, steps, checks, rollback. "Rollback" here means what to discard or re-mark when a check fails, since nothing in this folder touches an ad account.

### 4.1 Research sprints

**P1. The 60-minute manual research sprint (before a copy round).** Source: 03, with 05 and 09 on capture and star bands.
Goal: 1 provisional avatar record, or an update to an existing one, plus an audit list for current copy.
Preconditions: a product, a starting demographic or identity (from the brand's top customers per R19, or from a competitor's audience via SimilarWeb, a spy tool or a chatbot query if the brand has none `[needs brand data]` `[verify UI: SimilarWeb demographic report]`), a research evidence file for this brand (section 9 format).
Steps:
1. Open the brand's evidence file. Add a dated sprint header with product, candidate avatar, and who is running it.
2. Set a 60-minute block. If it cannot be done in 1 sitting, spread it over days but finish before writing copy (03).
3. Phase 1, forums, 30 minutes. Adopt the avatar's mind state. Type the avatar's own words into Google plus "reddit": "my cat won't drink water, please help, Reddit". Add identity qualifiers ("men", "over 30") as needed (R37).
4. Open threads. Read word for word. Read the comments, not only the post. Let one thread's vocabulary set the next query. Note confession communities such as r/offmychest.
5. Paste whole posts and comments verbatim into the evidence file, one entry per block, with URL and date. Bold emotional language, named failed solutions, situational detail, self-descriptions. Keep harsh wording (R39).
6. Phase 2, Amazon reviews, 30 minutes. On competing products, harvest the same 4 categories: fears, desired outcomes, emotional mind states, tried and failed solutions. Log the star band per quote (R34). Skip short generic reviews (R35).
7. After the block, write the dominant emotional state with the 2 or 3 quotes that show it (R41).
8. List named failed solutions with cost and extent where given (R40).
9. Write 1 trigger moment as a datable event with its quote (R63).
10. Draft the job statement as verb plus noun and run P17 on it.
11. Mark the record "provisional, sprint only".
12. Run the riff test and the 3 questions (R32). Fail either: schedule a second sprint on a different source type before copy.
13. Audit the current copy and any AI-drafted copy against the file: wrong want, wrong words, wrong emotion. Write the gap list for 10-MCR (R94).
Checks: at least 2 source types cited; every quote has a URL; failed-solution field not blank; register stated.
Rollback: if the sprint produced only generic material, change the query vocabulary and the subreddit, not the product; if the audience seems absent from Reddit, move to niche forums, Facebook groups or the brand's own reviews.

**P2. Full research sequence for a new product or new market.** Source: 05, with 08 for intent mining and 04 for the Ad Library.
Goal: a working list of sub-avatars with pains, hopes, obstacles and language for each, ready for P19 and P25.
Preconditions: a one-sentence idea with a specific avatar ("I help single men 25 to 35 who work 9-to-5 look better and feel more confident by showing them how to burn fat at the gym"); routing check that 01-PRD has not already killed the product.
Steps:
1. Place the idea in the demand matrix (R29). Discard a labour of love. Note which quadrant the chosen format sits in.
2. Google natural-language problem phrases ("how to burn fat and gain confidence for men"). Open every notable result. Log each competitor site.
3. For each site, read imagery, tone and headline; name the sub-market it speaks to; note distinctions the site itself draws; note format and price and its matrix quadrant (R46).
4. Read each headline for the constraint and reward it encodes (time-poor, challenge-seeking, identity).
5. Judge polish: do competitors look like real businesses? All amateur is a category warning.
6. Amazon: identify the top 5 to 10 books or products. Run P3 on them.
7. Google plus "reddit" searches for the emotional mechanics; barrier-specific searches ([niche] plus [fear]); Quora as a tactical check (R38). Run P4.
8. Track recurring words; run follow-up searches on each; log counterintuitive benefit links and tag the sub-avatar for each (R42).
9. Run the Google and Amazon intent pass (P5) for what they say vs what they buy.
10. Run the Ad Library map (P6).
11. Schedule at least 1 real conversation this week with someone who fits (P12). Listen live for the failed-solution phrase.
12. Compile sub-avatars: each with pains, hopes and benefits, obstacles, and the language for all 3, quoted.
Checks: every sub-avatar has quotes from at least 2 source types; contradictions logged, not resolved on the spot (R36).
Rollback: if no sub-market shows repeated language, the category may lack a struggle (R9); report that rather than inventing one.

### 4.2 Source-specific mining

**P3. Review-mining pass by star rating.** Sources: 04, 05, 06, 08, 09.
Goal: identity markers, failed-solution buyers, structural complaints, trust breaks and outlier life stories, each quoted and tagged.
Preconditions: the list of listings to mine: the brand's own reviews, the top 5 to 10 competitor or category products, and 1 high-review-count generic listing (AliExpress or the category's biggest Amazon listing).
Steps:
1. For each listing, sort by "Top reviews" and, where available, filter to reviews with images or video `[verify UI]`.
2. 5-star pass: log what buyers genuinely like (05) and every identity marker "I am a...", "As a..." (06). Tally markers across listings.
3. 3-star pass (and 2 to 4): log structural, recurring complaints; note contradictions between reviews side by side (05).
4. 1-star pass: log explicit failure points, physical friction ("couldn't get the brace off my knee fast enough"), broken trust markers, and claims that read as worn out (09). Flag any use case competitors do not target (post-surgery recovery).
5. 1-star and 5-star combined: search for the failed-solution phrase ("spent thousands", "tried everything", named products). Tag high-intent (R27).
6. Long-review pass: read the long narrative reviews for life-story context; log each distinct profile as a numbered candidate with a short identifier only ("Avatar 1: Anna Z"), never the full name (R70). Stop at 3 to 4 candidates for a new-avatar pass (R96).
7. Review-count proxy: note relative review counts across listings as a rough sales read, labelled as a guess (R44).
8. Cross-check the miracles and miseries list against what the reviews actually said (R74).
Checks: each quote has listing URL, star band, date; identity markers tallied with counts; no full reviewer names.
Rollback: a listing with fewer than a few dozen reviews gives tallies that mean little; add listings rather than reading deeper.

**P4. Forum mining and Reddit validation.** Sources: 03, 04, 05, 07, 09.
Goal: verbatim vocabulary, beliefs, failed solutions, emotional state, and a size-and-pain read for a candidate.
Preconditions: a candidate's specific detail (from P3 or an interview), the category's subreddits and niche forums `[web check]`.
Steps:
1. Turn the detail into a plain-language search: "post C-section weight gain Reddit" (04).
2. Open several threads. Judge volume and recency: many active recent threads is a common recurring problem; 1 old thread is not (R26).
3. Read for verbatim vocabulary ("C-section pooch", "patellar tendon graft"), existing beliefs ("only surgery fixes it"), failed solutions, emotional state ("so depressed over it").
4. Segment by consequence as you read: "can't do my job" vs "can't play sports" (R28).
5. Confirm the product's actual outcome matches the pain found; if it does not, drop the candidate.
6. Verify a specialized term is in common use in that community before it can anchor a hook (09).
7. Cross-reference against reviews, Google and social; 1 forum is not enough (R33).
8. Log the size-and-pain read with thread count, dates and 3 quotes.
Checks: 3 proof checks written (struggle, size, want); pattern seen across independent posters, not 1 user (R21).
Rollback: if Google no longer surfaces Reddit threads well for the category `[verify UI]`, use Reddit's own search and the subreddit's top posts; if the community is tactical rather than emotional, follow the content (R38).

**P5. Google and Amazon intent mining.** Source: 08.
Goal: 2 datasets, stated want and actual purchase, plus niche sizing.
Preconditions: the main niche keyword; Google Ads access for Keyword Planner (read only) `[verify UI]`; target countries.
Steps:
1. Google: type the keyword, do not press enter, record every relevant autocomplete suggestion.
2. Type each promising suggestion as a stem; record the next layer. Repeat 2 to 3 layers.
3. Keyword Planner: "discover new keywords", enter the seed, choose the countries, export ideas with volume, competition and seasonality. 08's sock-knitting example returned over 1,000 ideas.
4. Amazon: type the keyword, record autocomplete; press enter; read book titles and subtitles (or the most optimized listings) as pre-tested language.
5. Open listings and read reviews for likes and dislikes (feeds P3).
6. Compare the 2 datasets. Where they disagree, weight Amazon for offer and product decisions and Google for messaging (R44, R50).
Checks: volumes logged with country and date; no volume used as a mandate.
Rollback: a niche with no books and thin listings gives little purchase data; say so in the record.

**P6. Meta Ad Library competitor avatar map.** Sources: 04, 08. Read-only.
Goal: the mainstream avatar competitors already serve, their desires and USPs, and the longest-running angles, as signals.
Preconditions: product keyword and named competitors.
Steps:
1. Search the product keyword in the Ad Library `[verify UI]`. Also open each competitor page, Page Transparency, "see all", "go to ad library" (08's path) `[verify UI]`.
2. Mark brands that look like they are scaling: many variations, repeated creatives, professional production.
3. Play video ads. Note the visible person's rough age, gender, body type. Label it an estimate (04's "spitball"; his read was men early 40s to mid-60s for ab stimulators, matched by an outside data point of 47).
4. Note desires and USPs ("more defined abs", hands-free, "better than other ab stimulators" signals product awareness).
5. Note recurring ads and the ones lowest in the feed (longest running). Treat as a screen, not proof (R45).
6. Optional: SimilarWeb for a competitor's traffic and AOV (04's example: about 500,000 monthly visits, $149 AOV) `[web check]`. 04 also names a spy tool heard as "get hooked" [transcription unclear].
7. Repeat across competitors until the picture is stable. Write the mainstream avatar as a "who to avoid" profile.
Checks: every angle noted as a signal with the corroboration still needed; no ad text, image or offer copied.
Rollback: few advertisers (08's knitting case): skip this step and rely on reviews and forums.

**P7. Competitor site sub-market scan.** Source: 05. Steps are P2 steps 2 to 5. Output: a sub-market table (site, imagery, tone, headline constraint and reward, format, price, quadrant, polish read).

**P8. Social content sub-avatar map.** Source: 06.
Goal: the mass, niche and sub-avatar layers of the category and how each sub-avatar signals identity.
Steps:
1. Search broad terms on TikTok (and the brand's other platforms): "gym clothing", "CrossFit".
2. Note the distinct groups posting and what visibly separates them.
3. Trace the nesting: mass layer, niche layer, brand-claimed sub-avatars, the next unserved slice.
4. Log each brand's identity signals: creative style, product design, language and values, who it uplifts.
5. Pick a sub-avatar the brand could signal consistently across all of those.
Checks: characterizations of named brands marked as the agent's reading `[web check]`.

**P9. Digital intelligence and social listening.** Source: 02.
Goal: where the wider audience spends time, who influences it, and what the category (not the brand) complains about.
Steps:
1. SparkToro or Audience: platforms used, influencers followed `[verify UI]`.
2. Buying-mindset read if available (fast vs slow, risk vs conservative); note it is a B2B axis and mark any consumer adaptation as such (R49).
3. Brand24 or equivalent: track the category's topics, pains and frustrations in people's own words, not brand mentions `[verify UI]`.
4. Compare with interview themes; log matches and mismatches (R50).
Checks: run on the wider audience, not the interviewed sample.

### 4.3 Interviews, outreach and surveys

**P10. Recruit and frame a discovery interview.** Sources: 02, 07, 05.
Goal: 5 booked interviews to open a record; about 20 before segmenting a market (R52).
Preconditions: a customer list (07: the top 5 customers first), an incentive the brand can offer, consent wording for recording and quoting `[needs brand data]`.
Steps:
1. Draft the invite: purpose (learning about their experience), what it is not (no demo, no pitch, no support), exact time (30 minutes), the incentive, the recording and quote consent line.
2. Incentive: regular customers get product, store credit, early access or a t-shirt; senior or busy people get a charitable donation in their name, never cash (R55).
3. Send in batches. Track bookings per batch (R56).
4. At the start of the call, repeat the framing out loud before the first question.
5. With consent, record and auto-transcribe (07). Store the transcript in the evidence file with an interview id.
Checks: bookings fill within days in either direction (love or hate); if not, change the segment or incentive before changing the copy.
Rollback: a batch with near-zero response is logged as a signal about that segment's feeling toward the product.

**P11. Run the jobs-to-be-done interview (the script).** Sources: 01, 02, 05, 07, 09. The script below merges the sources' questions; the order is this playbook's.
Goal: 1 timeline, the 4 forces, the fired alternative, the trigger event, and verbatim language.
Steps:
1. Opening (02): "I'm not a product expert and I can't fix anything today. I just want to understand what happened. This takes 30 minutes."
2. Timeline start (01): "Take me back to the first time you thought about buying something like this. When was it? Where were you? Who was with you? What else was going on?"
3. The struggle (01, 02): "What wasn't working? What had you been doing about it before? How long had that been going on?"
4. Little hire failing (01): "Was there a moment your old way stopped being good enough? What happened that day?"
5. What was fired (01): "What did you stop doing or using when you bought this? What made that untenable?"
6. Push and pull (01): "What made the problem worse? What was the first thing about this option that pulled you in?"
7. Habit and anxiety (01): "What almost stopped you? What worried you about switching? What took that worry away at the last moment?"
8. Failed solutions (05, 03): "What had you already tried? What did it cost? What did it do and not do?" Lean in on "I tried X and it didn't Y".
9. Lateral questions (05): "Have you thought about X? How do you think about it? Who else do you know who did this? Why did they?"
10. Emotions and journey (02): "How did you find us? Why do you keep using it? How does it feel when it works? When it doesn't?"
11. Surprise (09): "What surprised you about the product or your situation?"
12. Day-to-day (09): "What can you do now that you couldn't? What still gets in the way?"
13. Never ask: about features, colours, price preferences, or "would you buy X" (01, 05).
14. Close: ask for 1 or 2 people they know with the same situation.
Checks after each interview: 1 data point, not a conclusion (01); log quotes with timestamps; write the storyboard (P18) while fresh.
Rollback: an interview that turned into support or a pitch is logged but its quotes are not used as evidence.

**P12. Lateral-question conversation by email or DM.** Sources: 05, 09.
Goal: a lightweight first conversation when a call is not possible.
Steps: reply to a real inbound email or DM; ask 2 or 3 lateral questions (P11 step 9) and "what surprised you"; probe day-to-day limits; log the thread verbatim with consent status. At least 1 such conversation per week (05).

**P13. Standing outreach: calls and DMs.** Sources: 09, 06, 02.
Goal: continuous first-party evidence.
Steps:
1. Book a weekly slot. Pull 3 to 5 recent buyers, 2 to 3 lapsed buyers.
2. Calls: "How are things going?" then P11 steps 8, 11, 12.
3. DMs on the channel buyers use `[needs brand data]`: ask concerns and what surprised them.
4. Listen for unprompted self-description (06's 95% "ecom brand owner"); tally it.
5. Log recurring frustrations, repeated phrases, broken trust markers in the same categories as reviews.
Checks: the tally of self-descriptions is re-read each quarter (R83).

**P14. Post-purchase survey and verification survey.** Sources: 09, 06, 02, 08.
Goal: count and confirm what interviews found; capture the situation at scale.
Preconditions: interview themes exist (02: survey after analysis, not before).
Steps:
1. Post-purchase survey (Shopify app or equivalent `[verify UI]`) fired after checkout, with email follow-up (09). Questions in the same categories as reviews and calls: what was going on when you bought, what had you tried, what activity do you want back, how would you describe yourself (06: role, family role), what specifically works for you.
2. Verification survey to the list (Google Forms is 06's free tool `[verify UI]`): the interview themes as closed questions plus structured facts. `[adaptation]` consumer facts: household situation, purchase occasion, first or repeat, bought for self or other.
3. Wording checks (08): no leading questions, no positive-only phrasing, randomize or reconsider order, keep the survey description neutral. Pilot on 5 people.
4. Aggregate. Recurring identity plus mechanism pairs become candidates; single aspirational answers do not (06).
Checks: the survey confirms or counts an existing theme; a brand-new theme from a survey goes back to interviews before it enters a record (R59).
Rollback: response counts too small to compare are logged as such; do not present percentages from a handful of answers.

**P15. Churn and loss conversations.** Source: 02; `[adaptation]` for the ecommerce forms.
Goal: the real reasons customers leave, and the fixable ones.
Steps:
1. Pull recent cancellations, refund requests, lapsed subscribers, and abandoners who replied to an email.
2. Ask directly why they left, with the P10 framing. Do not sell them back.
3. Log reasons verbatim; tag fixable ones (02's example: no support access, fixed with live chat).
4. Feed anxieties into the record's objections (R72) and fixes into 17-CXP and 14-EML.
Checks: reasons come from the customer, not inferred from dashboards.

**P16. Ticket, transcript and return-reason mining.** Sources: 07, 01 (adaptation).
Goal: passive data on struggle, workarounds and unmet jobs.
Steps:
1. Export support tickets, sales or support call transcripts, return reasons and cancellation reasons for the period `[needs brand data]`.
2. Read for: recurring pains, who is asking (proxy buyers, gift buyers), workarounds ("I use it for X instead"), and returns that describe a wrong job.
3. Tag each theme with count and dates; quote 2 or 3 tickets per theme by ticket id.
4. Feed workarounds into candidate jobs (R18), wrong-job returns into the "not for" line (R73).
Checks: counts done in code, not by eye.

### 4.4 Building and validating the record

**P17. Validate a job statement.** Source: 01.
Goal: a job statement that passes both tests (R5).
Steps:
1. Write the candidate as verb plus noun describing progress ("keep my third cat hydrated so I don't lose her early", "get back on the ice with my friends after knee surgery").
2. Reject any statement made of adjectives or attributes ("convenient", "premium", "trustworthy").
3. List everything that could be hired for it. If all are SKUs in the same category ("a different water fountain"), go up 1 level and rewrite ("keep my cat drinking": fountain, wet food, adding water, vet visit, doing nothing).
4. Stop when the alternatives span categories. Expect 2 or 3 passes.
5. Check the 3 dimensions are present or explicitly "no evidence" (R2).
6. Check a real struggle exists (R9). If not, note "low-stakes purchase; job statement optional" and keep the quotes.
Checks: the statement reads as progress in a circumstance and names no product.
Rollback: a statement that only fits 1 category is a preference; keep it as a tradeoff in the job spec, not as the job.

**P18. Storyboard the struggle.** Source: 01.
Steps:
1. From interview notes, write: Once upon a time (the situation). Every day (the routine and its workaround). One day (the trigger event, dated). Because of that (what they tried, what was fired). Because of this (push, pull, habit, anxiety). Finally I did (the purchase and what removed the last anxiety).
2. Mark each discrete emotional moment across the journey, including the first little hire (unboxing, first use).
3. Hand experiential moments to 17-CXP and 07-LPG; keep the trigger and forces in the record.
Checks: every beat has a quote or is marked inferred.

**P19. Assemble the avatar record.** Sources: 01, 03, 04, 08, 09.
Goal: a complete record in the section 9 format.
Preconditions: evidence file with at least 2 source types; a validated job statement (P17); for an existing brand, at least 1 first-party source.
Steps:
1. Fill every field in R71. For each field, attach quote ids or write "no evidence yet".
2. Write the 3 required elements at the top: quoted evidence (3 to 5 quotes minimum, this playbook's floor), trigger moment, job statement (R69).
3. Write the 4 forces with a quote each (R11). Write what was fired (R13).
4. Write failed solutions by name with cost (R40) and the dominant emotion (R41).
5. Write miracles and miseries as 2 specific lists (R74) and the Why chain per benefit (R75).
6. Write the job spec: tradeoffs, competitive set including do-nothing, obstacles and anxieties at purchase and at use, each anxiety paired with what removed it or "untested" (R71, R72).
7. Write consequence segment, cohort and platform habits (R28, R48), experience level (R68).
8. Write "not for" (R73).
9. Write demographics as context only, with the platform-demographics source (R8).
10. Set status: provisional (public data only), confirmed (first-party evidence), validated (repeat purchase or a scaled creative test for this avatar `[needs brand data]`).
11. Run checklist 5.4.
Checks: no field holds a claim without a quote id; no full reviewer names; no sensitive-attribute assertion phrased as fact about a viewer.
Rollback: a record that fails 5.4 goes back to P1 or P10, not to the copywriter.

**P20. Build the 5W layer.** Source: 08.
Steps: Who (existing market: top-customer cut compared across demographics, geographics, psychographics `[needs brand data: ranking metric]`; new market: competitor ads and targeting). What (miracles and miseries lists). When (life events; daily schedule type). Where (online and offline, then a "social media demographics" search to confirm `[web check]`). Why (benefit to personal motivation chain; check the avatar benefits from this offer, not the category). Attach to the record.

### 4.5 AI-assisted steps

**P21. Run an AI deep-research report on 1 prioritized candidate.** Source: 04.
Preconditions: at least 1 manual sprint done for this brand and category (R64); the candidate cleared the 3 proof checks (R26); the prompt template obtained and read `[web check: 04's prompt is only linked in his video]`.
Steps:
1. Open a fresh ChatGPT or Gemini session; enable deep research `[verify UI]`. 04 found a separate search toggle unnecessary.
2. Paste the fixed template. Change only the avatar field: identifier, preliminary profile (demographic band, problem in their words, desires and USPs, beliefs, failed solutions).
3. Confirm the prompt asks for: demographics and identity, synopsis, day-to-day struggles, feelings, own words, failed solutions, limiting beliefs, beliefs about solutions and competitors, core identity beliefs, attitudes, hopes and dreams.
4. Wait (04: about 22 minutes; 30-plus pages).
5. Read the whole report. Open every cited source. Copy into the evidence file only quotes you found on the cited page, with URL and date. Discard the rest.
6. Optional: run the same prompt in the other tool and compare source depth (04's 1 run favoured Gemini; anecdote).
7. Mark the resulting record "provisional, AI-assisted, verified quotes only".
Checks: zero quotes in the record without a verified URL.
Rollback: a report whose citations do not resolve is discarded and the candidate returns to P4.

**P22. LLM synthesis of the brand's own data.** Source: 07.
Preconditions: 5 or more transcripts, survey results, order data summary, product and pricing info, content performance; all first-party.
Steps:
1. Create a dedicated project or knowledge base in Claude or ChatGPT `[verify UI: limits and sharing]`. Load the inputs. Keep it to 1 brand.
2. Ask: who am I speaking to, what pains recur, what do they care about most, which themes repeat, what words do they use. Ask it to cite the transcript id for each claim.
3. Ask it to draft the record fields (R71) from the inputs only, marking any field it cannot support.
4. Review every claim against the raw transcripts. Remove anything unsupported. Replace any paraphrased "quote" with the verbatim line.
5. Save as a draft record; run P19 step 11.
Checks: every claim cites a transcript id; no quote absent from the transcripts.

**P23. Live LLM persona for QA.** Source: 07.
Preconditions: a confirmed record and its evidence file.
Steps:
1. Load only the record and evidence into a project. Instruct it to answer with quote ids and to say "no evidence" when there is none.
2. Before each brief or copy round, ask directional questions: would this resonate, what would she push back on, which words from the file fit, what proof is missing.
3. Treat answers as hypotheses. Any line that ends up in copy must trace to a quote (R86, R103).
4. Use the same project to brief new team members.
5. If the CMS or publishing tool has a persona QA feature (07 names HubSpot's), use it `[verify UI]`.
Checks: the project never invents quotes; if it does, tighten the instruction and re-run.

### 4.6 Untapped avatars, priority and creative handoff

**P24. Untapped avatar pipeline for a saturated category.** Source: 04, with 06 for the rework.
Preconditions: mechanism audit done (R24) and no real product difference found `[needs brand data]`.
Steps:
1. P6: map the mainstream avatar and write "who to avoid".
2. P3 steps 1 and 6: mine long Amazon reviews for 3 to 4 candidate profiles.
3. For each candidate, P4: Reddit size-and-pain read; log the 3 proof checks.
4. Assemble a preliminary sketch per candidate (demographic band, problem in their words, desires, beliefs, failed solutions). Mark "not an avatar yet" (R78).
5. Competitive isolation check: search the Ad Library for the candidate's likely angle and keywords. Little or no advertising is good; another advertiser owning it means re-run the proof checks.
6. Demand line (R98): keyword volume, subreddit size, any traffic read `[web check]`.
7. Rank: most isolated candidate that passes all 3 proof checks first (R82). Keep the others as a backlog.
8. P21 on the top candidate. Then P19 with status provisional.
9. Rework brief (R97): note the mass-market claim and creative concept competitors prove, and list every layer to rework (primary text, creative, page, proof, framing). Hand to 10-MCR and 07-LPG with the R106 reminder.
10. After the first buyers: P10 and P13 to confirm; upgrade status.
Checks: the shortlist (section 9) has every column filled per candidate.
Rollback: a candidate that fails size or want goes to the backlog with the reason; do not lower the bar because it is isolated.

**P25. Prioritize candidates and set the avatar count.** Sources: 01, 04, 06, 08, 09.
Steps:
1. List every candidate from P2, P3, P4, P13, P14 and P16 with its evidence counts by source type.
2. Merge candidates that share job, trigger, consequence and emotion. Split any that differ on those (R80).
3. Drop candidates with 1 quote, 1 review or 1 call (R21).
4. For an existing brand: rank the dominant avatar (unprompted self-description tally, top-customer patterns) first (R82).
5. Rank the rest by: first-party confirmation, evidence count, competition read, size basis, proof checks.
6. Pick 1 primary avatar per product line for the current creative cycle (R81). Everything else is a backlog with a next research step.
7. Record the count and the reason for it; no fixed number (R79).
8. Re-run each quarter (R83).
Checks: the priority list cites its evidence columns; nothing ranked on isolation or novelty alone.

**P26. Avatar-to-creative angle map.** Sources: 03, 08, 09, 06.
Goal: per avatar, a ranked list of angles with quotes, register, situation line, failed solution, anxiety and proof, for 10-MCR and 11-ADC.
Steps:
1. For each miracle and misery, write 1 angle. Attach the quote ids. An angle with no quote is dropped.
2. Rank benefits by the strength of the Why chain (R93) and the count of independent quotes.
3. State the register from the dominant emotion (R87).
4. Write the situation line in the avatar's words, phrased as a story or a quoted line, not as a claim about the viewer (R77, R88).
5. List the named failed solution and, in the avatar's words, why it failed (R88).
6. List the anxiety and the evidence of what removed it (R72).
7. List which reviews and results belong to this avatar for proof (R90) `[needs brand data]`.
8. Write the "not for" line and the congruence line: the condition and journey the ad, pre-lander and page must all name (R89).
9. Note cohort phrasing and platform (R48).
10. Note past test results for this avatar and angle `[needs brand data]`.
Checks: checklist 5.5.

**P27. Full-funnel congruence check.** Sources: 06, 09.
Steps: for a launched or drafted funnel, list the condition named in the ad, the pre-lander and the page; the setting shown; the proof shown; the offer framing. Any mismatch is sent back to the weaker asset before launch. Run the "wrong place" test: would a non-avatar viewer feel this is not for them?

**P28. Persona-use audit.** Sources: 02, 07.
Steps:
1. List the quarter's briefs, launches and copy rounds. For each, which avatar record was cited.
2. Records cited by nothing: interview the team on why (wrong fields, not findable, not trusted). Replace fluff fields with evidence fields (R76).
3. Keep whatever label the team uses.
4. Distribute the revised record to marketing, product, support and sales.
Checks: usage rate reported per record.

**P29. Demand matrix check.** Source: 05. Steps in P2 step 1. Output: quadrant, price band, rough customer count and basis.

**P30. Brand brain handoff.** Sources: 07, 02, 01 (adaptation for ecomOS).
Steps:
1. Store per brand: avatar records with status, the evidence file, the angle map, the untapped shortlist, the interview script as customized, the use log, and the little-hire metric per avatar.
2. Every record carries: date of last first-party evidence, next research step, and who owns the next call.
3. Expose 2 queries: "which quotes support this line" and "which avatar does this brief serve". Never "what would the avatar say" without quote ids.
4. Flag any record with no new first-party evidence in a quarter as decaying (R100).
Checks: no cross-brand mixing; public and private sources labelled.

## 5. Diagnostic checklists

Written so a worker can run each one without the sources.

### 5.1 Research sprint check (after P1)

| What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Time box complete | Sprint header shows 30 min forums plus 30 min reviews, or the spread over days | 60 min logged before any copy | Copy started mid-sprint | Finish the block first | 03 [d75e33882fdb] |
| Queries in the avatar's words | Read the query log | "my cat won't drink water please help" | "cat hydration supplement market" | Rewrite queries as the person would type them | 03 [f1ca3f6fbc70] |
| Comments read, not only posts | Entries include reply-level quotes | Reply quotes present | Only original posts | Reopen threads, read replies | 03 [f1ca3f6fbc70] |
| Verbatim capture | Spot-check 5 entries against their URLs | Exact text, harsh words kept, URL and date | Paraphrase, softened, no URL | Re-copy verbatim; drop entries with no URL | 03, 05 [3db1dccaa8da] [46a98b023ad3] |
| Star band logged | Each review quote shows 1, 3 or 5 star band | Bands present | Unlabelled | Re-tag | 05, 09 [46eec728bb7e] [2fd2d4d2c90b] |
| Dominant emotion stated | Record header | 1 state with 2 or 3 quotes | Blank or 3 states | Re-read quotes; if 2 states hold, consider 2 avatars | 03 [dae729a4f6bb] |
| Failed solutions named | Failed-solution field | Product or procedure names with cost | "Tried some things" or blank | Research not done; second sprint | 03, 05 [326d0318ebcc] [b08301158fb6] |
| Riff test and 3 questions | Operator answers unscripted | 30 seconds fluent; vent, tried, sick-of answers sourced | Defaults to a demographic | Second sprint on a different source type | 03, 09 [0d27b0e8ba75] [f6f18000b06c] |
| Copy audit done | Gap list exists | Lines flagged for wrong want, words or emotion | No audit | Run P1 step 13 | 03 [4e2d70bdca59] |
| Pattern, not 1 voice | Count independent posters per theme | Theme seen across several posters | 1 dramatic quote carries the theme | Keep collecting or downgrade the theme | 03, 05, 06 [6e03505404f7] [14590ac68739] |

### 5.2 Review-mining pass check (after P3)

| What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Listing set | Count listings | Own reviews plus top 5 to 10 category products plus 1 generic high-count listing | 1 listing | Add listings | 05, 06 [46eec728bb7e] [a724805d3534] |
| 5-star pass | Likes and identity markers logged with tallies | Markers tallied across listings | No tally | Re-run step 2 | 05, 06 |
| 3-star pass | Structural complaints listed; contradictions side by side | Repeated specific complaints | One-off taste complaints treated as gaps | Mark one-offs as noise | 05 [46eec728bb7e] [fcf1bd930a6c] |
| 1-star pass | Failure points, friction, trust breaks, worn claims | Verbatim lines per category | Summary only | Re-copy verbatim | 09 [2fd2d4d2c90b] |
| Failed-solution buyers | Search for "spent", "tried", product names in 1 and 5 star | Tagged high-intent quotes | None searched | Run step 5 | 05 [b08301158fb6] |
| Long-review candidates | Numbered candidates with short identifiers | 3 to 4 distinct profiles for a new-avatar pass | Full reviewer names stored; short reviews used | Strip identifiers; skip short reviews | 04 [083c7052a4f0] |
| Review-count proxy labelled | Note says "rough guess" | Labelled | Presented as sales | Relabel | 08 [8a7237ef9555] |
| Untargeted use case flagged | Any use competitors do not address | Flagged for P4 | Not looked for | Re-read 1-star and long reviews | 09 [2fd2d4d2c90b] |

### 5.3 Interview run check (after P10 and P11)

| What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Framing sent and repeated | Invite text and call opening | Not a sales or support call, exact time stated | Vague or pitch-like | Rewrite invite; restate at start | 02 [2534ec17bc50] |
| Incentive fit | Who was asked, what was offered | Product or access for regular buyers; donation for busy people; no cash to executives | Cash to a high earner | Change incentive | 02 [70460b582ffd] |
| Booking rate | Bookings per batch | Fills quickly, love or hate | Near zero | Treat as a segment signal; change segment or incentive | 02 [2534ec17bc50] |
| Count | Interviews logged | 5 to open a record; about 20 before segmenting | 1 or 2 used as proof | Keep going; mark provisional | 07, 02, 01 [6f9531c5c473] [c4d6dd183e5b] |
| Timeline reconstructed | Notes start at first thought of buying | Dated timeline | Starts at purchase day | Re-interview or mark thin | 01 [da4191b7964a] |
| No attribute questions | Read the transcript | No coil, colour, price, "would you buy" questions | Feature questions asked | Discard those answers | 01, 05 [ab9f2f70e75c] [e2f0e8697fe7] |
| 4 forces captured | Push, pull, habit, anxiety each have a line | All 4 | Only push and pull | Ask step 7 next time | 01 [d60553248611] |
| Fired alternative named | "What did you stop doing" answered | Named | Missing | Ask step 5 | 01 [4171f8999a97] |
| Failed-solution follow-up | "I tried X" was probed | Cost and outcome captured | Moved on | Train the interviewer to lean in | 05 [b08301158fb6] |
| Consent and storage | Transcript id, consent status | Both present | Missing | No quotes used until fixed | ecomOS |
| 1 data point rule | Conclusions drawn | Clustered across interviews | 1 interview rewrote the record | Revert; cluster first | 01 [c4d6dd183e5b] |

### 5.4 Avatar record review (before handoff)

| What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| 3 required elements | Top of record | Quotes, trigger, job all present | Any missing | Reject; back to P1 or P10 | 01, 02, 03, 09 [294308de8309] [ef0ecef3dfbb] [c5efc108c9c9] |
| Quote traceability | Spot-check every quote id against the evidence file | URL or record id and date for each | Any quote with no source | Remove the quote; if the field empties, mark "no evidence" | ecomOS, 01 |
| Job statement validated | P17 log | Verb plus noun; cross-category alternatives | Attribute list or same-category preference | Re-run P17 | 01 [b2121bd6e7ce] |
| Circumstance present | Read the synopsis | Situation, trigger, 3 dimensions | Age, gender, income only | Persona theater; rebuild from evidence | 01 [3f6f208703f1] |
| Passive data present | Evidence types listed | Struggle, workaround, fired alternative | Only sales or CRM fields | Add interviews, tickets or reviews | 01 [da14b9693dec] |
| Source-type floor | Count source types | 2 or more; 1 first-party for an existing brand | 1 forum only | Add a source type | 02, 05, 09 [6d0a453de28f] [912d3aa3c168] |
| Failed solutions and emotion | Fields | Named with cost; 1 dominant state | Generic or blank | Back to P3 or P4 | 03 [326d0318ebcc] [dae729a4f6bb] |
| Miracles and miseries specific | Read both lists | Quoted, concrete | "Wants better quality" | Rewrite from quotes | 08 [32ce1018d3e2] |
| Objections as anxieties | Job spec | Each paired with what removed it or "untested" | Objections listed with no evidence of removal | Mark untested; route to 03-OFF and 07-LPG | 01 [2174f296edbe] |
| Competitive set includes do-nothing | Job spec | Nonconsumption and out-of-category listed | Only competitor SKUs | Add | 01 [554e0cd99c6c] |
| Not-for line | Field | Present with a reason | Missing | Add from wrong-job returns or 1-star reviews | 01, 06 [741dd2ac873a] [746f5e6fba38] |
| Split or merged correctly | Compare with sibling records | Different job, trigger, consequence or emotion means separate | 2 emotions averaged into 1 | Split | 01, 03, 09 [ba25422e25e4] [de6f52d00231] |
| Status set | Header | Provisional, confirmed or validated with the reason | Unset | Set it | 03, 04 [208f632d3ddc] |
| Sensitive attributes | Read every line as if it were copy | Research statements only, quoted | A line asserts a viewer's condition or attribute | Rephrase as quoted situation; flag for 5.5 | ecomOS, 03 caveat |
| Reviewer identities | Search for full names | Short identifiers only | Full names or contact details | Strip | 04 [083c7052a4f0] |
| Demographics as context | Where the fields sit | Context block with platform-data source | Demographics lead the record | Move to context | 01, 08 [229a47af9d51] |
| Use log | Footer | Last cited brief and date | Never cited | P28 | 02, 07 [6f03704d60e9] |

### 5.5 Avatar-to-creative brief check (before handoff to 10-MCR, 11-ADC, 07-LPG)

| What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Every angle has quotes | Angle map columns | Quote ids per angle | An angle with none | Drop the angle | 03, 09 [2fd2d4d2c90b] [3db1dccaa8da] |
| Register stated | Brief header | Emotion plus quotes | Missing or 2 registers in 1 brief | Pick 1 or split the brief | 03 [dae729a4f6bb] |
| Situation before curiosity | Situation line | Names the exact situation in the avatar's words | Curiosity-only hook idea | Rewrite from situation and fear | 03 [301d338a9f16] |
| Failed solution named | Brief field | Exact product or procedure and why it failed, quoted | Category name | Replace with the named solution | 03, 09 [326d0318ebcc] [873f2122bf91] |
| Anxiety and remover | Brief field | Paired with evidence | Unpaired | Mark untested for 03-OFF | 01 [2174f296edbe] |
| Proof belongs to this avatar | Proof list | Only this avatar's reviews and results | Mixed | Filter | 06 [746f5e6fba38] |
| Congruence line | Brief field | 1 named condition and journey for ad, pre-lander, page | Missing | Add before handoff | 09, 06 [873f2122bf91] |
| Not-for line | Brief field | Present | Missing | Add | 01, 06 |
| Cohort phrasing and platform | Brief field | Quotes from where the cohort posts | TikTok phrasing for a 50+ avatar | Re-source | 09 [9b44ebb5a6e9] |
| Sensitive attributes | Read the situation line and every angle | Stories and quoted lines; no assertion about the viewer's health, body, age, money or protected status | "You have X" phrasing | Rephrase; if it cannot be rephrased, drop the angle | ecomOS `[web check: Meta policy]` |
| Competitor material | Search the brief for competitor text or images | Signals only: who is spoken to, layout, mood | Copied lines, logos, products, faces | Remove | ecomOS, 08 [0ea951a84570] |
| No invented claims | Every promise in the brief | Provable by the brand | Outcome the brand cannot prove | Remove | ecomOS |
| Creative carries the avatar | Brief notes | Setting, proof, language all avatar-specific | Avatar only in the hook | Rework the other layers | 06 [746f5e6fba38] |
| Past results attached | Test log | Wins and losses for this avatar and angle | None checked | Fetch `[needs brand data]` | ecomOS |

### 5.6 Untapped avatar scan check (after P24)

| What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Mechanism audit first | Brand record note | Real difference checked and documented | Skipped | Do it; if a real difference exists, route to 01-PRD and 03-OFF | 04, 09 [60a58f44e42d] |
| Mainstream avatar mapped | "Who to avoid" profile | Age band, desires, USPs, awareness level from several competitors | 1 competitor or none | Extend P6 | 04 [b399ed19a017] |
| Overlap check | Compare candidate with mainstream | Clearly different profile and desire | Same as a scaling brand | Back to review mining | 04 [0934edc554c3] |
| Candidate yield | Count | 3 to 4 from long reviews | 1 | Keep mining | 04 [083c7052a4f0] |
| 3 proof checks | Per candidate | Struggle, size, want each with thread counts and quotes | Any unchecked | Do not deep-research | 04 [70b5dd026992] [09f09782497e] |
| Isolation check | Ad Library search for the candidate's angle | Little or no advertising | Another advertiser owns it | Re-run proof checks; do not assume a gold mine | 04 [09f09782497e] |
| Demand line | Keyword volume, subreddit size, traffic read | Present with sources | "A lot of threads" only | Fill `[web check]` | pass 1 caveat, 08 [771e65508b21] |
| Sketch labelled | Preliminary profile | "Not an avatar yet" | Used to brief copy | Run P21 and P19 first | 04 [208f632d3ddc] |
| Deep research verified | Quote sources | Every quote found at its URL | Report pasted as is | Re-verify or discard | 04 [be3576be73a2] |
| Backlog kept | Shortlist | Adjacent pockets with reasons | Discarded | Restore | 04 [09f09782497e] |
| Niche size | Parent market and sub-niche estimate | Basis logged | 20,000-person parent market and a 100 to 1,000 sub-niche | Shallower cut or different parent | 06 [58497983a714] |
| Rework scope | Rework brief | Every layer listed | Hook only | Extend | 06 [4af92fa26772] |
| Competitor copying | Rework brief | Angle adapted, nothing copied | Text, image or offer copied | Remove | ecomOS |

## 6. Thresholds and benchmarks

Confidence: "1 voice" means only the paid-social creator or a single other source; "unsourced" means the number is this playbook's floor with no source count behind it. No number below is a measured result unless the basis column says so.

| Value | Condition | Source | Basis | Confidence |
|---|---|---|---|---|
| 60 minutes per research sprint, 30 forums plus 30 reviews | Before a copy round | 03 [d75e33882fdb] | Presenter's protocol | 1 voice; presenter also says 80/20 (C8) |
| 30-second riff test | Gate before writing copy | 03 [0d27b0e8ba75] | Presenter's heuristic | 1 voice |
| 3 questions (vent, tried, sick of hearing) | Gate before writing creative | 09 [f6f18000b06c] | Presenter's heuristic | 1 voice (same creator) |
| 60 to 80% of new-product time on research | New product development | 05 [46a98b023ad3] | Presenter's own practice | 1 source, self-reported |
| Top 5 to 10 products or books per category for review mining | Review pass | 05 [46eec728bb7e] | Presenter's step, no justification | 1 source |
| 3-star band most representative of structural complaints | Review pass | 05 [46eec728bb7e] | Presenter's read | 1 source |
| 1-star for failure and trust markers | Review pass | 09 [2fd2d4d2c90b] | Presenter's practice | 1 voice |
| 1-star and 5-star for failed-solution buyers | Review pass | 05 [b08301158fb6] | Presenter's pattern read | 1 source |
| 3 to 4 candidate avatars from long reviews before deep-diving | Untapped avatar pass | 04 [083c7052a4f0] | Presenter's target | 1 voice |
| 3 proof checks (struggle, size, want) | Before deep research on a candidate | 04 [70b5dd026992] [09f09782497e] | Presenter's gate | 1 voice |
| About 22 minutes and 30 to 39 pages per deep-research run | AI deep research | 04 [be3576be73a2] | 1 run | 1 voice, single run |
| 5 interviews, 30 minutes each, to start | Opening a record with thin data | 07 [6f9531c5c473] | Practitioner start point, not validation | 1 source |
| About 20 interviews, 30 minutes each | Before segmenting into personas | 02 [2534ec17bc50] [6d0a453de28f] | Cited from Deploy Empathy, attributed to Nielsen, from memory | 1 source, twice removed `[web check]` |
| 20 interviews cover about 97% of audience sentiment | Same | 02 [2534ec17bc50] | Same | 1 source, unverified |
| At least 1 real conversation per week, 1 hour blocked | Any brand | 05 [e2f0e8697fe7] | Presenter's suggestion | 1 source |
| Interviews continue permanently | Any brand | 02, 09 [5d0d40c930ec] [99043b84fe3d] | Practice and 1 unverified anecdote | 2 voices |
| Depth beats breadth: few rich interviews over many shallow data points | Finding the causal job | 01 [c4d6dd183e5b] | Book's argument, cases | 1 source, academic |
| $30 charitable donation for a 30-minute call | Busy or senior participants | 02 [70460b582ffd] | Her own validation practice | 1 source |
| 1 t-shirt or 3 months beta access | Regular participants | 02 [70460b582ffd] | Client examples | 1 source |
| Interview-caused cancellations "almost zero" out of "thousands" | Fear of outreach | 02 [2534ec17bc50] | Recollection, not audited | 1 source |
| About 90% of marketers create personas; 77% never use them | Persona adoption | 02 [6f03704d60e9] | Her own survey, no sample size | 1 source, self-run |
| 48% of 300+ marketers have a documented ICP | ICP adoption | 07 [ff3969ab7ccb] | HubSpot survey, no method given | 1 source, vendor |
| Top 20% of customers as the avatar base | Existing market | 08 [cef3f6a44c44] | Presenter's framing, no ranking metric | 1 source; brand data wins |
| About 95% self-identify as ecom owners | Dominant avatar detection | 06 [bccb9c4b4dab] | His own community | 1 voice, single case |
| 100M+ gym-goers; 20,000 parent market leaves 100 to 1,000 | Niche size check | 06 [58497983a714] | Illustrative estimates | 1 voice, illustrative |
| 45 emotional moments storyboarded (Airbnb) | Storyboarding | 01 [df9261a8fe1b] | Company's own account | 1 source, example |
| Loss aversion about 2x gain appeal | Weighing anxiety vs appeal | 01 [188ed2166ca7] | Kahneman and Tversky 1979 | External study, cited |
| About 40% of Airbnb guests would not have travelled | Nonconsumption size | 01 [35de9821d183] | Airbnb's own figure | 1 source, self-reported |
| Fewer than 1 in 3 of 57 reorgs improved results | Org design | 01 | Bain 2010 | External study; out of scope here |
| Up to 95% of consumers use reviews; 86% call them essential | Reviews as job evidence | 01 [541818498033] | PowerReviews, dated | External, dated `[web check]` |
| Long-running ads more likely profitable | Ad Library screen | 08 [0ea951a84570] | Heuristic, explicitly "not always" | 1 source, hedged |
| Review count as sales proxy | Amazon | 08 [8a7237ef9555] | Explicit guess | 1 source |
| Over 1,000 keyword ideas from 1 seed | Keyword Planner | 08 [771e65508b21] | Demo output | 1 source, example |
| About 500,000 monthly visits, $149 AOV (competitor) | Competitor scale read | 04 [b399ed19a017] | SimilarWeb lookup, 1 competitor | 1 voice, example |
| $6,500 plus $5,000 Neograft, reframed as about $300 a month | Failed-solution cost | 03 [326d0318ebcc] | 1 forum user | Example only |
| $60 for a 14-week DVD program; under $50 a week food budget | Price and budget reads | 05 [2ce06b2439fa] [46eec728bb7e] | 1 site, 1 review, 2018 | Example only |
| 5x ROAS day one (student) | Avatar rework | 06 [4af92fa26772] | Self-reported anecdote | Unverified; not a benchmark |
| At least 2 source types per record; 1 first-party for a brand with buyers | Record floor | this playbook (R33) | Direction from 02, 05, 09; no count given | Unsourced floor |
| 3 to 5 quotes minimum per record | Record floor | this playbook (P19) | No source gives a count | Unsourced floor |
| No candidate on 1 quote, 1 review or 1 call | Pattern rule | 03, 05, 06 | Direction, no count | 2 voices, no number |
| Quarterly re-check of dominant avatar and use log | Cadence | this playbook (R83, R76) | 06 and 09 say "periodically" and "ongoing" | Unsourced cadence |
| Pilot a survey on 5 people | Survey wording | this playbook (P14) | 08 warns on wording; gives no pilot size | Unsourced |

Moved to Appendix A: the unsourced vanity-numbers row (video framing dollar figures).

## 7. Where sources disagree

Each conflict: what each side says, when each is right, what the agent should do.

**C1. Demographics as noise vs demographic targeting.**
Side A: 01, 02, 03 and 09 say a demographic is not an avatar; 01 says demographics never explain causation (the "average pilot" cockpit fit nobody); 02 calls demographic personas fluff that cannot tell a copywriter what to write. Side B: 08 records demographics, geographics and psychographics as the Who fields and checks platform demographics for placement; 04 reads competitor avatar age and gender from Ad Library videos; 06 keeps Meta targeting broad but says the parent market's size matters; standard media buying still uses demographic and lookalike reach.
When each is right: Side A for the definition and for copy. Side B for reach, placement and for describing who competitors already speak to.
What the agent should do: keep demographics as a context block and a Where input (R8); never write copy from them; never let a record pass 5.4 on demographics alone; hand targeting questions to 24-DEP and 11-ADC. 01's own distinction (targeting layer, not motivation) is the resolution and comes from a source, not from averaging.

**C2. Surveys and focus groups: never vs core method.**
Side A: 01 says feature surveys and focus groups produce wishlists, not jobs (Intuit's 150 features; the focus group that rejected American Girl). 08 says focus groups are expensive, shallow and moderator-biased and surveys are fragile to wording, and prefers behavioral data (Google, Amazon, Ad Library). Side B: 02 runs a quantitative survey after interviews as one of 4 prongs; 06 uses a Google Form to existing buyers to name an avatar; 09 runs an automated post-purchase survey; 07 uses survey results as an LLM input.
When each is right: Side A for discovery and for any survey that asks people to invent solutions or rate features. Side B for verifying and counting themes interviews already found, and for capturing the purchase situation at scale.
What the agent should do: no survey or focus group as the first or only source of a new avatar (R59, R60). Surveys after interviews, worded per 08's warnings, used to count and confirm (P14). A post-purchase survey runs continuously because it captures situation, not feature wishes. A brand-new theme that only a survey shows goes back to interviews.

**C3. Manual review reading vs AI-assisted extraction.**
Side A: 05 says do the reading yourself; scripts and AI strip emotional nuance and exact vocabulary. 03 says manual first, AI is a crutch for anyone who cannot yet judge it. Side B: 04 runs a 22-minute AI deep research report as the step that turns a sketch into an avatar. 07 uploads transcripts and surveys and lets an LLM synthesize the ICP. Pass 1 notes that at-scale review summarization is common practice.
When each is right: Side A when the goal is vocabulary, register and quotes, and whenever the operator has not yet read the raw material for this category. Side B for volume (thousands of reviews or tickets), for synthesis of first-party transcripts the team has already read, and for finding public sources to then read by hand.
What the agent should do: manual sprint first for every new brand and category (R64). AI may then extend and synthesize (P21, P22) under 2 hard rules: every quote is verified at its source before it enters the evidence file, and the model cites ids for every claim. Counting and theme tallies are done in code. No quote from a model.

**C4. AI research personas as crutch vs method.**
Side A: 03 says blind AI deep research is busywork that feels productive and produces false confidence. Side B: 04 (same creator, later video) makes deep research the core step and calls the manual picture "very shallow". 07 keeps a live LLM persona as an "on-demand focus group" used on every project.
When each is right: 03 for a new operator or a new category; 04 and 07 once the operator can spot a wrong line because they read the forums and transcripts.
What the agent should do: treat the 2 videos from 1 creator as a sequence, not a contradiction: manual sprint, then deep research on a candidate that cleared proof, then a live persona for QA. The live persona answers with quote ids or "no evidence" (P23). It is never asked to generate customer language for copy. ecomOS's no-invented-quotes rule decides this.

**C5. Build from competitor and stranger data vs own customer data.**
Side A: 04 builds an avatar entirely from competitor ads, strangers' Amazon reviews, Reddit and AI, with no customer contact, because his products have no customers yet. 08 says a new offer starts from competitor targeting. 03's sprint uses Reddit and competitor reviews. Side B: 08 says an existing market starts from the top 20% of customers; 06 detects the dominant avatar from what customers say; 02, 05, 07 and 09 all say own interviews and calls are the strongest input and that online strangers cannot be verified as buyers.
When each is right: Side A when there are no customers, or for finding an untapped avatar the brand does not yet serve. Side B whenever buyers exist.
What the agent should do: R19 and R82. Own data anchors, public data supplements, and a record with no first-party evidence is marked provisional until real buyers confirm it. For an untapped avatar the provisional status is expected and the first buyers are interviewed immediately (P24 step 10).

**C6. Niche avatar messaging vs broad Meta targeting.**
Side A (apparent): 06 and 09 push very specific avatars; 06's 100-to-1,000-person sub-niche warning implies audience size matters. Side B: 06 says he keeps Meta targeting broad even after niching and lets the algorithm match the creative; 09's pass 1 note says the narrowing is about messaging, not ad sets; current Meta guidance favours broad delivery `[verify UI]`.
When each is right: both, because they are about different layers. Specific avatar in the creative; broad delivery in the account.
What the agent should do: this folder outputs avatar-specific creative inputs and never an audience setting (R91). The one real constraint it passes to media: under broad delivery, generic creative gives the algorithm nothing, so a hook-only avatar mention is not enough (R89). Targeting decisions stay in 24-DEP and 11-ADC.

**C7. B2B ICP taxonomy vs consumer avatars.**
Moved to Appendix A: the Side A and Side B taxonomy detail.
When each is right: 07 and 02 for a B2B or wholesale line. The consumer sources for shoppers.
What the agent should do: R84. No consumer ICP schema invented in 07's name. A consumer brand's "ICP" is its priority avatar. The buyer-and-user split for gifts and proxy purchases (R85) is this pass's adaptation and is labelled as such.

**C8. 80/20 Reddit and Amazon split vs the demonstrated 50/50.**
Side A: 03 says "probably about an 80/20", 80% of time on Reddit and forums. Side B: the same video's protocol is 30 minutes of forums then 30 minutes of Amazon reviews. 04 (same creator) leads with Amazon long reviews for candidate discovery and uses Reddit to validate. 05 reads Amazon first (top 5 to 10 products), then Reddit and Quora.
When each is right: 80/20 describes where 03 thinks the richer emotional material lives for his products; 50/50 is what he actually does in 60 minutes; 04 and 05 show the order can flip when the goal is candidate discovery (reviews carry life stories) rather than emotional register (forums carry confession).
What the agent should do: run 30 and 30 in P1 as demonstrated. Choose the order by goal: reviews first for new candidates and identity markers, forums first for register and vocabulary. Do not cite 80/20 as a rule.

**C9. Interview counts: 5, about 20, or ongoing with no number.**
07 says 5 to start; 02 says about 20 (a twice-removed Nielsen claim); 05 says 1 a week; 09 and 02 say never stop; 01 says depth over breadth with no count. These are not contradictory. Agent: 5 opens a record, 20 before segmenting a market, and the weekly slot never ends (R52). All numbers are practitioner heuristics and section 6 marks them so.

**C10. Reddit for emotion and Quora for tactics.**
Only 05 draws the split and says it is his experience. 04's deep research cites Quora quotes among emotional sources. Agent: use 05's split as a starting expectation and follow the content (R38). `[web check]` both platforms changed after 2018.

**C11. Ad duration as a profitability signal.**
08 uses it and hedges it. ecomOS goes further: competitor ads are signals, never proven winners. Agent: a screen to corroborate with reviews and demand, never a reason to adopt an angle on its own (R45).

**C12. New mechanism vs new avatar.**
04 says most commodity products have no real mechanism and the avatar is the lever; 09 says a superior product or a specific avatar, ideally both; 01's jobs win comes from experiences and processes, not a segment. Agent: audit the product first (R24); never claim a mechanism the product lacks; if a real difference exists, route to 01-PRD and 03-OFF and use this folder for the avatar layer.

**C13. Fixed record template vs LLM-drafted document.**
04 and 08 give fixed field lists; 07 prefers letting the model draft from data rather than filling a template. Agent: fixed fields (R71) because traceability needs them; the model may draft the content of those fields from first-party inputs (P22).

## 8. Common mistakes

Merged from all 9 sources, deduplicated, each with the fix.

1. Treating a demographic label as an avatar ("women 45+ with cats", "30+ woman with knee pain"). Fix: R1, R69; rebuild from quotes, trigger and job. (01, 02, 03, 09)
2. Persona theater: invented names, stock photos, favourite colours, lifestyle fluff. Fix: replace with concerns, jobs, objections, triggers (02, 01).
3. Averaging conflicting jobs into 1 record (the cockpit for the average pilot). Fix: split by circumstance, consequence, cohort, emotion (01, 03, 09).
4. Asking customers what features to add, or running a focus group to validate. Fix: timeline and struggle interviews; behavioral data (01, 08).
5. Skipping interviews because online research feels sufficient. Fix: 5 to start, then 20, then weekly (05, 02, 07).
6. Letting an interview drift into a sales, demo or support call. Fix: R53 framing, twice (02).
7. Paying cash to a high earner for an interview. Fix: donation in their name (02).
8. Avoiding outreach for fear of churn without checking. Fix: run a batch and log bookings and cancellations (02).
9. Treating 1 quote, 1 review, 1 forum or 1 interview as proof. Fix: R21; patterns across independent sources (01, 03, 05, 06, 09).
10. Reacting to every critical review and getting pulled in all directions. Fix: log contradictions, act on repeated patterns only (05).
11. Reading only original posts and skipping comments. Fix: P1 step 4 (03).
12. Reading short generic reviews for avatar insight. Fix: long narrative reviews; short ones only for tallies (04).
13. Paraphrasing, summarizing or softening customer language. Fix: verbatim capture, harsh words kept (03, 05).
14. Naming a solution category instead of the exact product tried. Fix: "minoxidil", not "hair drugs" (03, 09).
15. Writing the same register to a fear-driven and a frustration-driven avatar. Fix: R87 (03).
16. Building a hook on curiosity alone. Fix: situation and fear first (03, 09).
17. Putting the avatar only in the headline while creative setting, proof and page stay generic. Fix: R89 (06).
18. Mixing other avatars' or generic proof on the avatar's page. Fix: R90 (06).
19. Naming one condition in the ad and another on the page. Fix: congruence line (09).
20. Using one cohort's platform phrasing for another cohort. Fix: R48 (09).
21. Jumping to AI deep research before a manual pass, and pasting AI output into ads unread. Fix: R64, R65 (03, 04).
22. Treating the ads-reviews-Reddit sketch as a finished avatar. Fix: status provisional; deep research and first buyers (04).
23. Choosing an avatar for isolation or novelty without checking struggle, size and want. Fix: 3 proof checks (04).
24. Selling a commodity to the avatar a bigger competitor already owns, or claiming a mechanism the product lacks. Fix: R24 (04, 09).
25. Picking a sub-niche without checking the parent market is big enough. Fix: R23 (06).
26. Serving many avatars at once and staying generic. Fix: 1 primary per product line (06).
27. Competing in a trend's crowded core product instead of the adjacent category. Fix: R31 (06).
28. Building an avatar from assumptions instead of top customers (existing) or competitor targeting (new). Fix: R19 (08).
29. Treating search interest as the whole picture without purchase evidence. Fix: R44 (08).
30. Treating a long-running competitor ad as proof, or copying it. Fix: R45, R106 (08, ecomOS).
31. Writing generic miracles and miseries. Fix: quoted, specific items (08).
32. Guessing where the avatar spends time. Fix: platform demographics and cohort data (08, 09).
33. Skipping the Why chain and leading with the wrong benefit. Fix: R75, R93 (08).
34. Letting active data (sales, CRM) crowd out passive data (struggle, workarounds). Fix: R30 (01).
35. Confusing the first purchase with proof the job is solved. Fix: little-hire metric (01, adaptation).
36. Not saying who the product is not for, and collecting wrong-job 1-star reviews. Fix: R73 (01, 06).
37. Building a persona nobody uses (77% in 02's survey) or a static PDF nobody reopens. Fix: P28 use audit; live evidence file (02, 07).
38. Doing research once. Fix: weekly outreach, quarterly re-check (02, 06, 09).
39. Doing research with no strategy to apply it to. Fix: the angle map and handoff exist before the sprint ends (08).
40. Storing reviewers' full names or identifying detail. Fix: short identifiers (04).
41. Asserting a viewer's health, body, age or protected attribute in a brief. Fix: R77 (ecomOS; 03's caveat).
42. Inventing a consumer ICP schema and calling it the B2B source's method. Fix: R84 (07's own admission).
43. Believing a superior avatar rescues a product that fails the job. Fix: 09 only claims niching helps when the product is not superior; check the little hire (09, 01).
44. Fighting over what to call the deliverable. Fix: keep the team's label; judge the content (02).

## 9. Deliverables

All deliverables are per brand, stored in the brand record, and dated. Formats are this playbook's; no source gives a file format.

**D1. Avatar record** (1 file per avatar, `brands/<brand>/avatars/<slug>.md`).
Header: name (short, not a fictional person), product line, status (provisional, confirmed, validated), date of last first-party evidence, owner, priority rank.
Block 1, required: quoted evidence (3 to 5 quotes minimum, each with quote id), trigger moment (datable event with quote), job statement (verb plus noun, P17 log).
Block 2, forces: push, pull, habit, anxiety, each with quote; what was fired; little-hire evidence `[needs brand data]`.
Block 3, the person in the situation: synopsis; day-to-day struggles; dominant emotion; own words; failed solutions with cost; limiting beliefs; beliefs about solutions and competitors; identity, attitudes, hopes and dreams; consequence segment; cohort and platform habits; experience level.
Block 4, 5W: Who (context only, with source), What (miracles list, miseries list), When (life events, daily schedule), Where (with platform data source), Why (benefit chains).
Block 5, job spec: 3 dimensions; tradeoffs; competitive set including do-nothing; obstacles and anxieties at purchase and at use, each with its remover or "untested".
Block 6: not for; sensitive-attribute note (what may be quoted as story, what may not be asserted); consent status of interview quotes.
Footer: evidence counts by source type; use log (briefs that cited it); next research step.

**D2. Avatar priority and test queue** (`brands/<brand>/avatars/_priority.md`).
Table: avatar | status | evidence count by type (reviews, forums, interviews, tickets, surveys, AI-verified) | first-party confirmed | dominant-avatar tally | competition read (Ad Library) | size basis | 3 proof checks | little-hire metric | rank | reason | backlog next step. 1 primary per product line marked. Date of last re-rank.
Untapped avatar section (folds in the former D6, since both are ranked candidate lists for the same decision): mechanism audit result; mainstream avatar to avoid (age band estimate, desires, USPs, awareness level, competitors mapped, date); candidates, one block each: source review (short identifier, listing URL, star band), preliminary sketch, Reddit read (thread count, recency, 3 quotes), 3 proof checks, isolation check, demand line, rank, deep-research status, verified-quote count, rework brief scope, backlog reason if not chosen.

**D3. Research evidence file** (`brands/<brand>/avatars/evidence.md` or a table; 1 per brand, never shared across brands).
One row per quote: quote id | verbatim text | source type (own review, competitor review, forum, Quora, interview, DM, ticket, survey, AI-verified public) | URL or record id | star band if a review | date collected | consent status | avatar tags | field tags (trigger, failed solution, anxiety, miracle, misery, identity marker, belief, emotion) | bolded phrases. Sprint headers with date, product, operator, query log. Tallies (identity markers, self-descriptions, ticket themes) computed in code and stored with the date.

**D4. Interview script** (`brands/<brand>/avatars/interview-script.md`).
The P11 script customized: invite text with framing and consent line; incentive by participant type; opening statement; the 12 question groups; the "never ask" list; recording and storage instructions; a closing referral ask. Plus the P15 loss-conversation variant and the P13 DM variant.

**D5. Creative angle map per avatar** (`brands/<brand>/avatars/<slug>-angles.md`).
Header: avatar, status, register with quotes, situation line (story or quoted, policy-checked), not-for line, congruence line (condition and journey), cohort phrasing and platform, proof list belonging to this avatar.
Table: angle | miracle or misery it comes from | quote ids | benefit rank and Why chain strength | failed solution named and why it failed (quoted) | anxiety and remover | past test results `[needs brand data]` | policy flag | handoff target (10-MCR, 11-ADC, 07-LPG, 03-OFF). Add a size-guide or fit-confidence angle whenever the record's anxieties include sizing or fit (R113).

**D7. Sprint gap list** (appended to the angle map): lines in current or AI-drafted copy that fail the research (wrong want, wrong words, wrong emotion), each with the quote that contradicts it, for 10-MCR's next test round.

**D8. Persona-use audit note** (quarterly, appended to `_priority.md`): briefs per record, unused records and the decision (revise, merge, retire).
## 10. What needs live data or a web check

**`[needs brand data]`**

- Product mechanism audit: does the product differ visually, mechanically or functionally from competitors (R24, P24).
- Customer list with a value ranking and the chosen ranking metric for the top cut (R19, P20; 08 gives none).
- The brand's own reviews, all star bands, with dates (P3).
- Past interview transcripts, call notes, DM threads, with consent terms for quoting (R70, P10).
- Support ticket themes, return reason codes, cancellation reasons (R61, P16).
- Post-purchase survey answers and response counts (P14).
- Repeat purchase rate per SKU and per stated avatar: the little-hire metric (R16).
- Refund and 1-star rate by SKU as the wrong-fit signal (R73).
- Creative test history per avatar and angle, wins and losses (R95, P26).
- Reviews and results tagged by avatar for proof (R90).
- Which DM channel and platforms buyers actually use, by cohort (R48, R57).
- Interview incentive budget and what the brand can offer (R55).
- Existing avatar records and which briefs cited them (R76, P28).
- Business type: consumer, B2B line, wholesale, gifting share (R84, R85).
- Research depth target for this cycle: copy round, launch, or scale attempt (R32).
- Consumer structured facts the brand wants counted in a survey (household situation, occasion, first vs repeat, for self or other): this pass's adaptation of 02's B2B fields (R59).

**`[web check]`**

- Current subreddits, niche forums, Facebook groups and Quora topics for the category (R37, P4).
- Whether Google still surfaces Reddit and Quora threads for natural-language queries as 05 (2018) and 08 (2022) showed (R37, R38).
- Current Meta advertising standards on personal attributes and personal health, before any creative handoff (R77, checklist 5.5).
- Current Meta delivery and targeting behaviour under broad settings (R91, C6).
- Platform demographic data for the brand's countries (R48).
- Keyword volumes for the candidate's terms and the country (R43, R98).
- SimilarWeb or equivalent access and pricing for competitor traffic and demographic reads (P1, P6).
- The ad research tool 04 names, heard as "get hooked" [transcription unclear], and the competitor brand he names, heard as "Ap Born" or "Abornne" (P6).
- 04's deep-research prompt template, linked only in his video description (P21).
- The original Nielsen claim behind "20 interviews cover 97% of sentiment", cited from memory via Deploy Empathy (R52).
- The PowerReviews review-usage statistics 01 cites (dated).
- Current positioning of Gymshark, Alphalete, Buff Bunny, Anaka Power and Young LA before reusing 06's characterizations (R22).
- 05's presenter identity and any verification of "20+ successful products"; 08's presenter identity; 09's community claims. None changes a rule.
- Whether a competitor named by 03 ("Iris", 600,000 to 800,000 visitors, $500 to $1,000 AOV, transcript unclear) is relevant to any brand.
- Survey design best practice, since 08 warns on wording and gives no template (P14).

**`[verify UI]`**

- Amazon review sort ("Top reviews"), star filter and images or video filter (P3).
- Meta Ad Library search; Page Transparency to "see all" to "go to ad library" path (P6).
- Google Ads Keyword Planner "discover new keywords" location (P5).
- ChatGPT and Gemini deep research toggles; whether a separate search toggle is needed (P21).
- Claude and ChatGPT project or knowledge-base limits, file sizes and sharing (P22, P23).
- Shopify post-purchase survey apps and setup (P14).
- Google Forms free tier and question types (P14).
- SparkToro, "Audience", Brand24 and IBM Watson-based data availability and features (P9).
- Any CMS persona QA feature equivalent to HubSpot's "save your persona" (P23).
- TikTok search for category terms (P8).

## 11. Freshness and stale-risk notes

**Stable, re-verify yearly or when a source is added.** Jobs theory (R1 to R17), the 5 job-hunting lenses (R18), the record format (R69 to R75), interview technique and script (R51 to R56, P11), verbatim capture (R39), pattern-over-single-voice (R21, R36), the 4-step untapped pipeline's logic (R96). None depend on a UI. Source 01 is from 2016 and predates DTC and paid social; its theory is not dated but its examples are.

**Platform search behaviour, re-verify each quarter.** Google's surfacing of Reddit and Quora threads (05 is 2018, 08 is 2022; Reddit's search, API and indexing arrangements changed after both). Reddit's own search. Quora's answer mix (05's emotion-vs-tactics split may no longer hold). TikTok search. Amazon's review sort and filter options (04, 05, 08, 09 all assume them). These change what P1, P3, P4 and P8 return, not the rules.

**Tool UIs and availability, re-verify before each use.** Meta Ad Library and Page Transparency path (08's 2022 path). Google Ads Keyword Planner menu. ChatGPT and Gemini deep research (04 is Q1 2026; feature names, limits and output quality move). Claude and ChatGPT projects (07). Shopify post-purchase survey apps (09). Google Forms (06). SparkToro, "Audience", Brand24, IBM Watson-based personality data (02, recorded around 2021 to 2022; "Audience" may not be the same product and the Watson-based data may not be available). SimilarWeb access and demographic reports (03, 04). The spy tool in 04 [transcription unclear].

**Discontinued tools.** No source in this folder names Alexa (the Amazon web-traffic ranking service, closed in 2022) or any other tool known to be discontinued; the risk is generic: any third-party audience or traffic tool named here (SparkToro, Audience, Brand24, SimilarWeb, the unnamed spy tool, Watson-based data) can close or change pricing. When a tool is gone, keep the step's purpose (where the audience is, what the category complains about, how big a competitor is) and substitute, and log the substitution in the evidence file.

**AI research tools, re-verify each quarter and on every model change.** 04's runtime (22 minutes), length (30 to 39 pages) and the Gemini-vs-ChatGPT source depth are single runs on early-2026 models. The verification rule (every quote opened at its source) does not change; the yield and the failure modes do. 07's LLM synthesis depends on project features and file limits. 03's crutch warning gets more relevant, not less, as outputs get more polished.

**Meta policy, re-verify before every creative handoff.** Personal attributes and personal health standards decide how the situation line may be phrased (R77). 03's example hooks (baldness, terminal pet illness, self-esteem) were written without reference to any policy.

**Practitioner numbers, treat as dated to the video.** 60-minute sprint, 5 and 20 interviews, top 20%, 95% dominant share, 3 to 4 candidates, 100M gym-goers. None is measured; none goes stale in a way that can be checked, so section 6 marks confidence instead.

**Named-brand characterizations.** 06's readings of Gymshark, Alphalete, Buff Bunny, Anaka Power and Young LA, 05's 2018 fitness competitor sites and books, 04's ab-stimulator competitor, 03's "Iris" and cat-supplement examples: illustration only, re-check before reuse `[web check]`.

24 Sep 2026: ecommerce specificity pass applied from ECOM_REVIEW.md; priority block added, 15 rules reworded, 8 levers added, about 309 words moved to Appendix A.

## 12. Source index

| No. | Title | Type | Credibility and bias | Contributed most |
|---|---|---|---|---|
| 01 | Competing Against Luck (Christensen, Hall, Dillon, Duncan, 2016) | Book, 129 cards | Academic and consulting authors selling their own Jobs Theory (Innosight, Re-Wired Group). Evidence is named company cases, self-reported by executives, plus a few cited studies (Kahneman and Tversky, Bain 2010, Nielsen). Explicit about its own limits. No ecommerce, DTC or paid-social case. Rating: high on theory and interview method, low on ecommerce applicability; every ecommerce mapping in its mini playbook is a pass 1 adaptation, marked here. | Job definition and validation (R1 to R10), 4 forces and firing (R11 to R15), big and little hire (R16), 5 job-hunting lenses (R18), passive vs active data (R30), interview timeline method and script (R54, P11), storyboarding (R62, P18), job spec (R71, R72), not-for (R73), inventory before count (R79), no averaging (R80), commander's intent for the brand brain (R99, R101) |
| 02 | Adrienne Barnes on Best Buyer Personas (podcast, Triple Whale hosts) | Transcript, 12 cards | Persona researcher selling persona research; client base mostly B2B SaaS, some B2C. Evidence: her practice, one self-run survey with no sample size, and a twice-removed Nielsen claim. No named client results. Rating: medium on method (interview framing, incentives, 4 prongs), low on numbers; B2B survey fields do not map to consumers and are marked. | 4-prong method (R33), interview count and framing (R52, R53), incentives (R55), booking rate as signal (R56), survey after interviews (R59), digital intelligence and social listening (R49), say-do cross-check (R50), churn interviews (R58), persona-use audit (R76, P28), keep asking (R100) |
| 03 | How I Find Avatars That Scale Facebook Ads to $10k/day | Video transcript, 11 cards | Paid-social creator selling a course and "School" community; same voice as 04, 06, 09. Self-reported results only; the video is course marketing. Live Reddit demo is real but unverified. Rating: high on capture technique and register, zero on numbers; no policy awareness. | 60-minute sprint (P1), riff test (R32), query craft and comments (R37), verbatim and harsh wording (R39), named failed solutions (R40), emotional mind state (R41, R87), understanding before curiosity (R88), AI as crutch (R64), pre-existing insecurity split (R28), copy audit (R94), 80/20 vs 50/50 (C8) |
| 04 | How To Scale Facebook Creatives To $100k/mo With Untapped Avatars | Video transcript, 9 cards | Same creator; a student's $100k/month is the opener, unverified. Live demo "for the sake of this video", not a completed project. No customer contact anywhere in the method. Prompt not in the transcript. Rating: medium on pipeline logic, low on validation; its heavy burden of proof is its best rule. | Mechanism vs avatar fork (R24), Ad Library mainstream map (R25, P6), long-review candidates (R35), 3 proof checks (R26), preliminary sketch is not an avatar (R78), deep research protocol and verification (R65, P21), full record categories (R71), untapped pipeline (R96, P24), reviewer identity minimization (R70) |
| 05 | EXACTLY how I do market research for new products (GrowthLab, January 2018) | Video transcript, 11 cards | Unnamed presenter selling a "0 to Launch" course; "20+ successful products" unverified. Dated 2018; platform behaviour has changed. Rating: high on manual method and the reading discipline, low on numbers and freshness. | Demand matrix (R29), competitor site and headline reading (R46), star bands (R34), failed-solution buyers (R27), Reddit vs Quora (R38), repeated words and counterintuitive benefits (R42), pattern over single voice and contradictions (R36), manual not automated (R64), lateral questions (R54, P12), 60 to 80% time on research (R32) |
| 06 | How to create avatars that scale Facebook Ads to $30k days | Video transcript, 12 cards | Same creator, agency and mentorship pitch at the end ($200k+/month done-for-you; mentorship below). Anecdotes: a $3M agency sale, a 5x day-one ROAS, 95% of his community. Brand characterizations are his own reading. Rating: medium on discovery heuristics (identity markers, growth signal, fracturing), low on numbers; the broad-targeting note is practice, not data. | Identity markers in reviews (R20), avatar as growth signal (R21), market fracturing and nesting (R22, R47), niche size check (R23), dominant avatar from self-description (R19, R83), whole-funnel tailoring and the wrong-place test (R89, R90), broad targeting with creative carrying the avatar (R91, C6), rework a proven play (R97), emerging trend entry (R31), Google Form survey (R59) |
| 07 | How to Define Your Ideal Customer Profile (HubSpot Media, Fieldnotes) | Podcast transcript, 8 cards | Two HubSpot employees on HubSpot's show; plug HubSpot CRM and its persona QA feature; one HubSpot survey with no method. B2B framing with an admitted, unfilled B2C gap. Rating: medium on the LLM workflow and the 5-interview start, low on consumer fit; vendor bias on tools. | TAM, ICP, persona taxonomy and its limits (R84, C7), 5 interviews to start (R52), 3 data streams incl. transcripts (R61), no-CRM stopgap via communities (R37), LLM synthesis with review (R66, P22), live LLM persona for QA (R67, P23), content altitude (R68), persona as living tool (R76) |
| 08 | How To Do Market Research (Market Research 101, 2022) | Video transcript, 16 cards | Unnamed presenter promoting his own videos; "90% do it wrong" is unsupported; "10 years" of use unverifiable. No survey or interview method at all. Rating: medium on the 5W frame and the say-vs-buy split, high on staleness of tool paths (2022 UI). | 5W framework and miracles and miseries (R71, R74, P20), Who from top 20% or competitor ads (R19), When as life events and schedule (R63), Where via platform demographics (R48), Why chain (R75, R93), Google and Amazon intent mining (R43, R44, P5), Ad Library path and duration hedge (R45), survey wording warnings (R59), focus group critique (R60), research needs a strategy to apply it (mistake 39) |
| 09 | How I find Avatars that Scale Facebook Creatives to 100k/Day | Video transcript, 8 cards | Same creator; "evolve program" pitch; "300 plus brand owners", "100k days", a friend at "nine figures", all unverified. Defers the "exact ways" to the paid program; no counts, no script, no template. Rating: medium on the 3-question gate, 1-star mining and congruence, low on operational depth. | 3 questions gate (R32), record baseline and count-not-universal (R69, R79), 1-star mining for failure and trust (R34), condition-specific forums and clinical vocabulary (R37), consequence and cohort segmentation (R28, R48), calls, DMs and post-purchase survey (R57, R59), belief sequence and congruence (R88, R89), framing as offer (R92), stalled creative as research gap (R95) |

**Independent voices:** 6 (01; 02; 03 plus 04 plus 06 plus 09; 05; 07; 08). Where this playbook says "3 voices" it has counted the creator's 4 files as 1.

**Neighbour folders and what lives there.**
- 01-PRD product research: product selection, demand and competition gates, mechanism audit inputs, the demand matrix's product-side use.
- 03-OFF offers: promise, guarantee, bundle, price; receives the Why chain, miracles list and untested anxieties.
- 04-BRD brand: voice, positioning, purpose brand aim.
- 07-LPG landing pages: pre-lander and page build; receives the congruence line, proof list, not-for line, storyboard moments.
- 10-MCR paid-social creative and 11-ADC ad copy deployment: hooks, scripts, primary text; receive the angle map, register, situation line, sprint gap list.
- 24-DEP ad deployment: targeting, ad sets, budgets; receives only the note that creative must carry the avatar under broad delivery.
- 14-EML email lifecycle: RFM and lifecycle segmentation (02 says JTBD segmentation is not that).
- 17-CXP post-purchase: post-purchase survey placement, unboxing and first-use moments from the storyboard, churn fixes.
- 09-CRO testing: testing the anxiety removers on page.
- 06-MEA measurement: repeat purchase and refund metrics per avatar.

## Appendix A. General background

Moved here on 24 Sep 2026 during the ecommerce specificity pass. This is organisational-design case history and brand theory, not a store rule. It stays for context; no procedure, checklist or deliverable cites it.

**From R101 (moved from section 3.10).** Measure the customer's benefit, not internal activity, and let the job settle disputes. SNHU measured minutes to callback, not packages mailed. When teams argue tactics, nobody should be debating the job. The record's little-hire metric (R16) and its "not for" line are the 2 numbers the brain reports per avatar; organizational mechanisms in 01 (process owners, committees) are not sized for a small brand and are not adopted. Source: 01 only. [c79827d20a3f] [21955247a148] [336e01894bc3] [41516283a4bc]

**From R102 (moved from section 3.10).** Purpose brand is a long-horizon goal, not a campaign. A brand that owns 1 job in the buyer's mind (FedEx, IKEA) got there by being hired repeatedly for years, and lost it by chasing segments (Volvo under Ford, V8's flavour proliferation). Log it in 04-BRD as a positioning aim; this folder only supplies the job. Source: 01 only. [2b63dd9f725f] [1da34b764041] [4f376b72845a]

**From R84 and C7 (moved from section 3.7 and section 7).** The B2B ICP taxonomy detail. 07 splits audience into TAM (total market), ICP (target company: industry, size, location, seniority, department) and persona (the individual in the buying committee: daily tasks, career goals, pains, success vocabulary). 07 says B2C needs a different adaptation and does not give it. 02's survey fields (role, tenure, company size, buying authority) are B2B too. Side A (07, 02): builds this company-level taxonomy and admits the B2C gap. Side B (03, 04, 06, 08, 09): builds consumer avatars around a person's situation with no company layer; 01's jobs are individual circumstances. R84 and C7 keep the one-sentence scoping rule; a store agent never runs this taxonomy.

**From section 6 (moved from the thresholds and benchmarks table).** $10k, $30k, $100k days; $100k/month student; $3M agency sale; $200 CPM and $5 CPC. Video framing numbers from 03, 04, 06, 09, self-reported. Unverified; not used anywhere in this playbook.
