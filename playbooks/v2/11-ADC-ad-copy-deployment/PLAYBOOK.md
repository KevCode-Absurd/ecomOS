# 11-ADC ad copy playbook

version: 2.0-draft  |  date: 24 Sep 2026  |  sources: 9  |  cards: 402  |  built from: sources/*.md

After the 24 Sep 2026 split, folder 11 holds copywriting only. Meta, TikTok and account setup moved to 24-DEP. Google Ads moved to 12-GAD. This playbook covers the words: research before writing, the buying question and the one idea, headlines, hooks, body copy for ads, emails and pages, feature to benefit, specificity and proof, offers and deadlines in copy, objections, CTAs, editing, formats by placement, claim checking and variant planning.

## 0. How to use this playbook

**Who runs it.** The ad copy agent. It takes a brief and a brand record and returns finished copy: a static ad set, an email, page copy, a headline bank and a claim audit. It writes, edits and checks. It does not publish, pause or change budgets, and it does not contact customers. It can run inside the ad-copy v1.2 contract (`playbooks/ad-copy-v1.2/OPERATING_CONTRACT.md`): brief and brand facts govern; source cards are methods, not evidence; at most 2 revision passes.

**Ecommerce first.** This playbook is for stores, not for SaaS, coaching or B2B copy. Section 3.0 ranks the levers that move a store's numbers most; load it before the detail groups below. A rule's condition names the store type it applies to (hero SKU vs catalogue, low vs high AOV, subscription vs one-off, marketplace-heavy, luxury or considered purchase, mobile-first India vs US); that condition decides which rules apply to the brief in hand, not the group order.

**Which sections to load for which task.**

| Task | Load |
|---|---|
| New brand or product, first copy job | 0, 1, 2, 3 (groups A to C), 4 (P1, P2), 5.1, 10 |
| Static ad set (Meta or other feed) | 3 (groups C to H, K, N, P), 4 (P2, P3, P4, P5, P11, P12, P13), 5.2, 5.3, 5.5, 5.6 |
| Headline bank | 3 (group D), 4 (P3), 5.2, 6 |
| Hooks and first lines | 3 (group E), 4 (P4, P14), 5.2 |
| Email copy (single or sequence) | 3 (groups F, K, L, M, N), 4 (P6, P11), 5.4, 5.5 |
| Landing and sales page copy (hero, blocks, FAQ) | 3 (groups C, F, G, J, K), 4 (P7, P8), 5.3 |
| Product page copy (title, bullets, spec block) | 3 (groups G, H), 4 (P8), 9.8 |
| Feature to benefit work | 3 (group G), 4 (P8), 5.1 |
| Offer, guarantee or deadline wording | 3 (group I), 4 (P10), 5.5 |
| Claim audit before launch | 3 (groups H, O), 4 (P9), 5.5 |
| Editing an existing draft | 3 (group M), 4 (P11), 5.6 |
| Planning variants and tests | 3 (group P), 4 (P13), 6, 7 |
| Any point where sources disagree | 7 |
| What to hand back | 9 |

**Fetch before acting.**

- From the brand record: product facts with numbers (materials, counts, sizes, times, process steps, certifications), fixed prices and offers, approved claims and banned claims, guarantee and return policy with eligibility limits, voice samples (approved copy, packaging, support replies), avatar and segment notes, awareness of the traffic, past winning and losing copy with results.
- From the data layer: reviews (5-star and 1-star), support tickets and chat logs, top ads by cost per purchase and by CTR, email revenue by send, landing page conversion by traffic source.
- From the web: current character limits and truncation points for each placement, current ad policy for the claim types in play (health, income, before and after, body, urgency), current endorsement and review rules for the brand's market, current email client clipping limits. Section 10 lists every item.

**Hard rules for this agent (ecomOS rules that override any source).**

1. No invented statistics, studies, quotes, test counts, review counts, customer counts or savings figures. Several sources permit or model invention. Section 3 group O flags each.
2. No copying competitor text. Competitor ads are signals for layout and mood only.
3. Every claim must match the brand record or a checked source. Website assertions are not proof. Never infer piece counts from a kit or category count. Never invent setup time, ease, tools, compatibility, reviews, certifications, urgency or safety assurances.
4. Reading level below tenth grade. Short sentences. Digits. No em dashes. No inflated words. Concrete before to after benefits.
5. Keep brands apart. Keep public web research separate from private brand data.
6. Do arithmetic in code, not in the model (offer stacks, savings, percentages, reading scores).
7. Do not mention GPT or .env on client-facing pages.

**Era tags.** Every rule in section 3 carries a tag for where the idea comes from. The tag says what the evidence is, not whether it holds today.

- `[print 1920s]`: Claude Hopkins (sources 03 and 07) and the print readership studies Cashvertising cites (Starch, Rudolph, Caples, Ogilvy, 1912 to 1991). Evidence is keyed coupon returns and print readership scores. No digital channel exists in these texts. For a DTC brand today: the psychology (one buyer, specific claims, headline selects, cure over prevention, proof) transfers as a hypothesis to test. The mechanics (coupons, type size, print space, dealers, samples) do not. Length rules were measured on people who chose to read a print ad, not on a cold feed.
- `[DR book 2009]`: Drew Eric Whitman's own advice and the academic persuasion research he summarises (Cialdini, Petty and Cacioppo, Pratkanis and Aronson). Print and direct mail, early web. Uncited numbers are marked.
- `[SaaS 2011]`: Copy Hackers Book 1 (source 06). Written for software startups. The research method (segments, pains, motivations, feature and benefit table, competitor audit) transfers. The examples and tools do not. It never mentions reviews or product pages.
- `[course seller 2024]`: 8 Hour Copywriting (source 01). Clients are coaches and info products. Ecommerce appears in 3 places. Its email structures and edit checklist transfer; its funnel and VSL material is for coaching offers.
- `[coaching 2019]`: Copywriting 101 (source 05). Mostly courses and memberships, plus 1 hair-tool store (Head Candy). Its process rules (outline, read aloud, second person, congruency) transfer; its email numbers predate Apple Mail Privacy Protection.
- `[craft 2024]`: Harry Dry (source 04). Craft opinion on famous print ads. No data. The line-level tests transfer to any surface.
- `[organic video 2026]`: Sandcastles hook workflow (source 08). Organic creator videos ranked by views. The loop transfers; the paid-ad version is an inference, not shown.
- `[DR publishing]`: Rule of One (source 09), Masterson retold second hand.

**Where the sources are silent on ecommerce.** None of the 9 sources gives Meta character limits, product page rules, catalogue-scale copy, SMS, discount code strategy, or test sizes. No source shows a controlled test of its own advice on a store. This playbook says so where it matters and tags the gap `[needs brand data]` or `[web check]`.

## 1. Scope and outcomes

**What this domain covers.** The words in acquisition and retention copy: the research pack that precedes writing (feature and benefit table, customer language, competitor audit), the buying question and the one big idea, headline methods, hooks and first lines, body structures for static ads, emails and page sections, feature to benefit and abstract to concrete, specificity and proof, how offers, guarantees and deadlines are worded, objection handling, CTAs, editing passes, format rules per placement, claim checking and compliance, and how to plan copy variants for a test.

**What it does not cover, and where it lives.**

- Meta and TikTok account structure, budgets, bidding, scaling, algorithm behaviour, creative volume: 24-DEP.
- Google Ads: 12-GAD.
- Images, video, UGC, creative formats, competitor creative analysis: 10-MCR.
- Landing page layout, page build, CRO test design and statistics: 07-LPG and 09-CRO.
- Email flow build, ESP setup, deliverability, cadence, list hygiene: 14-EML. This playbook keeps the words in an email; the email sources here (01, 05) also give flow sketches, which are noted and pointed to 14-EML.
- Offer design and pricing strategy: 03-OFF. This playbook covers how to word an offer that already exists.
- Avatars and research method at depth: 02-AVT. Brand voice at depth: 04-BRD.

**Business measures it moves.** Purchase conversion rate of the ad, email or page. Cost per purchase and period ROAS (total value divided by total spend, kept separate from breakdowns). Email revenue per send and click to purchase rate. CTR only as a selection signal (did the right people click), never as the goal: 2 sources warn that mystery or teaser copy raises clicks and lowers purchases [5861e7fcfc77] [0cf0f5e70b0b]. The owner's own measure in ecomOS: would Kevin use the copy, and how much editing does it need.

## 2. Inputs the agent needs

| Input | From where | Required or optional | Why |
|---|---|---|---|
| Product facts with numbers: materials, counts, dimensions, weights, times, process steps, sourcing, certifications | Brand record | Required | Specific claims are believed; superlatives are discounted (03, 07, 02, 04). Every number in copy must trace here. `[needs brand data: verified product facts]` |
| Fixed price, offer, discount, bundle terms, eligibility limits | Brand record, user | Required | Copy must respect fixed prices and preserve eligibility limits (v1.2). Offer must be 1 concrete line (06). |
| Guarantee and return policy, exact terms | Brand record | Required if any risk reversal is written | Guarantee wording must match what operations honour (02, 01). `[needs brand data: return rate, refund cost]` |
| Approved claims list and banned claims list | Brand record | Required | Claim audit (P9). Platform policy risk (01, 02, 06). |
| Voice samples: approved copy, packaging, support replies, founder posts | Brand record | Required; if absent, use the brief's provisional tone and say so | Voice match (01, 03). Without samples, do not claim owner approval (v1.2). |
| Avatar, segment, awareness stage of the traffic | Brand record, user | Required | Lead, length and structure change by stage (05, 02, 06). |
| Reviews, 5-star and 1-star, plus support tickets and chat logs | Data layer | Required for any new product; optional for a variant on known copy | Customer language and sentiment matching (05, 06, 03). `[needs brand data: reviews and tickets]` |
| Past ads with copy and results (cost per purchase, CTR, spend) | Data layer | Optional, strongly preferred | Study own winners first (08, 09, 03). Decide refresh vs keep (07, 03). `[needs brand data: ad-level results with copy]` |
| Email results by send: opens, clicks, revenue, unsubscribes | Data layer | Optional | Subject and structure choices; goodwill balance (01, 05). |
| Landing page the ad points to, with its first screen | User, data layer | Required for ad copy | Ad to page congruency (05). |
| Placement and format: which platform, which slots, image or video brief | User | Required | Lengths and truncation `[verify UI]`; headline must read beside the image (04, v1.2). |
| Competitor ads and pages (public) | Web, Ads Library | Optional | Baseline and white noise (06), long runners as format signals (05). Never copy text. `[web check: competitor ads now running]` |
| Current platform character limits and policy pages | Web | Required for a launch-ready set | Sources are silent on limits. `[web check: Meta ad specs and advertising standards]` |
| Number of variants wanted and the variable to test | User | Required | Variant planning (P13). Default: 3 variants, 1 variable each. |
| Testimonials with written permission | Brand record | Optional | Proof that is not created by the brand (02). Permission rules `[web check]`. |

## 3. Decision rules

Each rule: the rule, its condition, supporting mini playbooks by number, conflicts, card ids, era tag. Rules are merged across sources; where sources set different thresholds the strictest is kept and the others are noted. Rules that rest on 1 source say "Source NN says".

### 3.0 Ecommerce priority order

Rank these levers before loading the groups below. Each points to the rule ids it draws on. Conditions vary by store type; follow the condition named, not the group order.

1. Claim and compliance audit before anything ships (R107 to R114, P9). An unsupported claim can get the ad account banned; this outranks every craft rule, for any store.
2. Match copy depth to where the traffic is (R16, R23, conflict 7.1). A cold feed gets the short argument before truncation; the list and the PDP get the fuller case. A catalogue brand sets this per collection, not once.
3. Pick 1 idea and 1 appeal per SKU or collection, not per store (R18 to R21). A hero-SKU brand can hold 1 idea across the account; a catalogue brand needs a different idea per hero product.
4. Size the proof to the purchase (R8, R61 to R64). Low-AOV, impulse SKUs need 1 clean image and 1 cue; high-AOV, subscription and considered-purchase SKUs need reviews, comparison and demonstration first. `[general practice: the AOV split itself is not sourced; R8 supports it]`
5. Offer and guarantee wording matches the real mechanism (R68 to R72, R114). Subscription brands frame value across the plan; one-off brands frame the single order. `[general practice: subscription vs one-off split is not sourced]`
6. Keep product identity consistent across every SKU's ad and PDP hero (R33, R34, R104, conflict 7.4). A catalogue brand needs 1 template that still says what is sold.
7. Ad-to-page congruency (R84, R105). Matters most where the brand controls the landing page; less where a marketplace-heavy seller does not. `[general practice: marketplace note]`
8. Write for the list's real knowledge (R16, R52, R78). A store's owned list already knows the product.
9. 1 variable per test, judged on cost per purchase (R116, R120 to R122). This is the store's real measure of a copy change.
10. Format to the live placement limits (R102, R103, P12). Execution-level, fetched fresh each launch.
11. Voice consistency across SKUs without boilerplate (R86, R89). Matters more for a founder-led DTC brand than a marketplace listing. `[general practice]`
12. Editing and readability pass (P11, R92 to R98). Real, but last-mile polish, not the decision that changes results.

Load this block first; the groups below are the detail.

### Group A. Foundations

**R1. Copy exists to make the sale or the next step toward it. Judge it by purchases, not applause or clicks.** Condition: every asset. Hopkins: the only purpose of advertising is to make sales; treat each ad as a salesman that must justify its cost [6ebd6afa8fcc]. Whitman: an ad that only informs is a salesperson who cannot close [329ff6de64b5] [0e09cddd6797]. Jamie: copywriting is sales in written form [f27d97c52312]. Founders: judge every ad question by the salesman's standard [250834566833]. Clicks are not the measure: mystery ads raised CTR 18% and lowered conversion (02, "one study", uncited) [5861e7fcfc77]; teaser emails with no mechanism get clicks and no buyers (01) [0cf0f5e70b0b]. Sources 01, 02, 03, 05, 07. `[print 1920s]` `[DR book 2009]` `[coaching 2019]`.

**R2. The salesman test: every line must be something you would say to 1 interested buyer face to face.** Condition: any line in any asset; use it as a filter, not a substitute for results. Cut slogans, clever conceits, big type, decoration, jokes about business or home. Sources 03 [6ebd6afa8fcc], 07 [250834566833] [e02bc47498e3]. `[print 1920s]`.

**R3. Write to 1 named shopper choosing between this SKU and the alternative in their cart, on the device named in the brief (phone feed, PDP, inbox).** Condition: always; the brief names the person and the moment before drafting. Hopkins: picture a typical buyer whose attention the headline already caught [6ebd6afa8fcc]; Founders: get down to the units [b60274dadf3c] [ad76051fec65]; Harry Dry: who you are talking to is piece 1 of 3 [6645e37e12f9]; Copy Hackers: write for the 20% to 35% of visitors who are your best segment, not 100% [52564e4cb23c]. Sources 03, 04, 06, 07. `[print 1920s]` `[craft 2024]` `[SaaS 2011]`.

**R4. Reader first: "you" language, a what's-in-it-for-me near the top, and no sentence that starts with I, we, our, the brand or the product.** Condition: all copy. Strictest form is Jamie's: never start a sentence with I, me, my, us, our, the company name or the product name; drop possessives from labels ("Story", not "Our Story") [a0589e4916be] [44549e0c9982]. Exceptions the sources allow: first person tied to the reader ("if you want my help with X") (05); "in my experience" to show conviction (01) [60835ecfe3d0]; the launch email "Introducing: [product]" names the product on purpose (05) [2ac1adf98a07]. Support: 01 WIIFM near the start, cut CTAs about the writer [51f77f32f63c] [a98bb10fd49f]; 02 Starch found more than half of readers ignored ads that bragged about the company, and Flesch's target of at least 14 people references per 100 words [40638b840ce1] [210eb332ef8f]; 07 boasts and selfish phrases kill ads [39699efcd305] [250834566833]. Sources 01, 02, 05, 07. `[coaching 2019]` `[course seller 2024]` `[print 1920s]`.

**R5. Write for a thumb scrolling a feed or a PDP on a phone; short sentences are a scanning aid, not a style choice.** Condition: all copy, including B2B and premium (01: "no downside to simplifying"). Targets the sources give: 01 says third grade or below [495714e45312] [474c5d2ad56a]; 02 gives Flesch: about 11 words per sentence, 70% to 80% one-syllable words, opening paragraph at most 11 words, Flesch Reading Ease 70 to 80 equals 7th grade [d2d7d23b7635] [a2f59bfd45f7] [17183d94160c]; 04: you cannot write simply, only rewrite simply [189a7e6d8231]; 05: people read in micro moments on a phone [f27d97c52312]. ecomOS floor: below tenth grade. Operating target for ads and emails: Flesch Reading Ease 70 or higher (7th grade or easier). Vary sentence length so it does not sound robotic (02) [3cc6113534e9]. Sources 01, 02, 04, 05. `[course seller 2024]` `[DR book 2009]` `[craft 2024]`.

**R6. Do not be clever, do not entertain by default, do not boast.** Condition: default for sales copy; humour is a minority tool. Hopkins: fine writing reveals the hook; people do not patronise a clown [6ebd6afa8fcc] [66ff32f28a57]; Whitman: "it's not clever to be clever" [0e09cddd6797]; Tyson: about 80% of his emails are plain benefit emails, gimmicks only after the emails work [99d753c33b55]; Founders: boasting is repulsive [39699efcd305]. Conflict: Harry Dry's model lines are witty by contrast, and the Founders host says entertain before you educate (his gloss, not Hopkins). See 7.14. Sources 01, 02, 03, 07. `[print 1920s]` `[DR book 2009]`.

**R7. Clarity before persuasion: 1 idea per sentence, 1 idea per asset, and a reader who understands can be persuaded.** Condition: all copy. Whitman: "If you don't understand what I'm saying, I can't persuade you" [b261e875d93b] [043af87cd47d]; Harry Dry: "and" is a red flag for scope; the strength of an idea is inversely proportional to its scope [867743b221ba]; Rule of One [491bae29b0be]. Sources 02, 04, 09. `[DR book 2009]` `[craft 2024]` `[DR publishing]`.

**R8. For a low-AOV or impulse SKU, lead on 1 image and 1 cue; for a high-AOV, subscription or considered-purchase SKU, add the spec table, reviews and comparison before the ask.** Condition: all copy; for costly or important purchases (central route) pour on facts, testimonials and evidence; for low-cost impulse buys (peripheral route) keep pleasant images and cues but still give basic data. Whitman via Young and Rubicam and the Elaboration Likelihood Model [a9db8de6d903] [42c77acaccca] [9ad90e7b96fa]; Tyson: persuasion is belief shifting, and people rarely lack knowledge [68cf28c41359]. Source 02 says central-route attitudes last longer `[web check: ELM findings]`. Sources 01, 02. `[DR book 2009]` `[course seller 2024]`.

### Group B. Research before writing

**R9. Messages come from customers, not from the maker or the writer's taste.** Condition: before any copy. Hopkins: the maker is the wrong judge; top cause of failure is selling what people do not want [76127c3b3070]; Founders: the maker is too close to his factory [ea531107827e]; Copy Hackers: never wordsmith your internal message; never ask customers to approve copy, only to inform it [dd20f7934ee1]; Jamie: you cannot sell with your logic, learn theirs [3786ef47e9f9] [44549e0c9982]. Sources 03, 05, 06, 07. `[print 1920s]` `[SaaS 2011]` `[coaching 2019]`.

**R10. Compile the brand's own material into 1 document before writing.** Condition: first job for a brand, then reused. Contents (01): the brand's common sayings, angles, how their posts and videos open, the offer including backend offers, their critique of alternatives, stories that show a belief shift, lines that prove they understand the audience, and how people got on the list [b88d5fdf5214] [b245a0ded890] [243af58d06bd] [3ce42487fd05]. "Steal the ideas, not the words" [42ebacbe34c3]. Source 01, supported by 06's messaging strategy paragraph [20fa6900506f]. `[course seller 2024]` `[SaaS 2011]`.

**R11. Mine 5-star and 1-star reviews and record the exact phrases people use for the problem, the result and the doubt.** Condition: own reviews first; if none, reviews of analogous products (05). Jamie's sentiment matching: position as "not like what you hate, like what you love" [fb6ca632b8da] [a438dd94bf69]; Copy Hackers: keywords people type are the customer's words and often the exact phrases they want to see [936e1b2b613f]; Hopkins interviewed hundreds and canvassed thousands before writing [76127c3b3070]; Copy Hackers cites Pain Killer Marketing: 12 to 15 one-on-one interviews surface about 80% of a segment's pains [0c27d9b3a340]. Note: 06 never mentions reviews; card [17b8f4f12a1d] adds them. Sources 03, 05, 06. `[coaching 2019]` `[SaaS 2011]` `[print 1920s]`. `[needs brand data: reviews, tickets, chat logs]`

**R12. Build 1 feature-and-benefit table per product line, not per SKU or variant, and flag rows that only apply to some sizes or colors.** Condition: every product; list every feature, including small ones; give each at least 1 express benefit or cut it; add rows for "how you do what you do" (sourcing, values, design); rank rows. Copy Hackers [7f5165a57e7a] [95690fe6cfee] [70aaf0b3735c]; Whitman's BIG DEAL drill ("You benefit by...") [dc660f4f168c]; Tyson's feature plus benefit bullets [c4995809f1dc]. Sources 01, 02, 06. `[SaaS 2011]` `[DR book 2009]`. `[needs brand data: full feature list with numbers; competitor feature list]`

**R13. Research until you find the keystone fact and the untold process facts.** Condition: any product with a making process, sourcing story or technical basis. Hopkins read for weeks to find 1 fact (caffeine acts 2 hours after drinking) and wrote up ordinary brewing steps nobody had told (bottles washed 4 times, wells 4,000 feet, 1,018 yeast experiments) [6959d40e0dc8] [975c891bc15a]; Founders: walk the process, ignore "everyone does this" [48f2e992c7ce] [a5c303a75054]; Whitman's extreme specificity inventory: "what is obvious to me that my market knows little about?" [9f88626f46bc]; Harry Dry: keep an arsenal of facts, find the fact with a story inside it [188f4fe29d32] [579d7f6fa475]. Sources 02, 03, 04, 07. `[print 1920s]` `[craft 2024]`. `[needs brand data: production, sourcing, QC and fulfilment steps with numbers]`

**R14. Audit what competitors say, to learn the baseline and the white noise. Never copy their text.** Condition: before positioning a new product or angle. Copy Hackers: top 3 organic and paid results per keyword are your competitors; audit at most 10 home pages, record 5 things each (value proposition, top messages, primary CTA, reasons to buy, standouts), tally messages; frequent messages are either white noise or an expected baseline, and the audit cannot tell which [a3ddc92dd001] [17b8f4f12a1d]; Hopkins: collect every rival's claims [7d36e2443edd]; Jamie: long-running ads in the Ads Library are a signal, valid only for brands spending enough that bad ads get cut in 24 to 48 hours [f27174953be4]; Sandcastles: reskin a format, never clone; cross-niche copying usually fails [721989c4c0ef] [a80ff986fd63]. ecomOS: competitor ads are signals, not proven winners; layout and mood only. Sources 03, 05, 06, 08. `[SaaS 2011]` `[print 1920s]` `[coaching 2019]` `[organic video 2026]`. `[web check: competitor ads and pages now live]`

**R15. Find the real rival: a habit or an old way, not only another brand.** Condition: category with low penetration or a home-made alternative. Hopkins's pork and beans canvass: 4% used canned, 96% baked at home, so "buy my brand" reached 4% [6959d40e0dc8]; Harry Dry: position by what you replace (Athletic Greens and the smaller cabinet) [c78fe9d7b47e]; Copy Hackers: piggyback on motivation others already built and remind rather than educate [17b8f4f12a1d]; Hopkins: do not pay alone to educate a habit ($20 to $25 per convert, 1920s) [50fbb6ee4040]. Sources 03, 04, 06. `[print 1920s]` `[craft 2024]` `[SaaS 2011]`.

**R16. Know the segment and its awareness stage before choosing the lead.** Condition: every brief. Copy Hackers: pick the segment that visits most and pays most; write for it [6c4ec380b27a] [7a372d0590a0]; Jamie's 5 stages (unaware, problem aware, solution aware, product aware, most aware) set story length [3912f9a679c0]; Whitman's Transtheoretical stages: one ad that covers all stages or a series that moves through them [f6643f8906df] [2723c7e5dcb7]; Tyson: know how people got on the list; an ecommerce list already knows the product [3ce42487fd05] [8a4864a0a123]. Sources 01, 02, 05, 06. `[SaaS 2011]` `[coaching 2019]` `[DR book 2009]`. `[needs brand data: share of traffic new vs returning vs repeat]`

**R17. Do not use research to validate what you already believe, and do not trust your own taste about demand.** Condition: reading research and judging drafts. Copy Hackers: highlight the surprising and the repeated findings [7a372d0590a0]; Hopkins: the appeals we like best rarely prove best [fe816803de4e]; Founders: never judge humanity by ourselves [9e96311d1944]. Sources 03, 06, 07. `[print 1920s]` `[SaaS 2011]`.

### Group C. The buying question and the one big idea

**R18. Anchor 1 idea per SKU or collection, never 1 idea for the whole store; a catalogue brand plans a different idea per hero product per cycle.** Condition: every sales message; if a strong point cannot serve the idea, cut it. Rule of One: 91 of Masterson's top 100 offers centred on 1 concept (second hand) [491bae29b0be] [b720ce9767c7] [1ee01d6bfef2]; Tyson: one email, one idea, one CTA [b1fc36d11cab] [cab8c603e36c]; Jamie: each asset gives value or sells, never both [c3c4e6142fe4]; Harry Dry: "and" is a red flag [867743b221ba]. Conflict with Hopkins's complete story: see 7.9 and R48. Sources 01, 04, 05, 09. `[DR publishing]` `[course seller 2024]` `[coaching 2019]` `[craft 2024]`.

**R19. Write the buying question before drafting: the reader's current belief and the belief the copy must move them to.** Condition: every brief. Harry Dry: current attitude is the starting line, desired attitude is the finish; you cannot start a race in the middle [6645e37e12f9]; Tyson: state the reader's current belief in their words before you try to move it [68cf28c41359]; Whitman: reinforce beliefs buyers hold, add new ones that do not conflict, never say "you're wrong" [dd9d7f53de83]; Jamie: bridge the perspective gap [3786ef47e9f9]. For an ecommerce list that already knows the product, the questions are "do these work, how, and why these rather than others" (01) [8a4864a0a123]. Sources 01, 02, 04, 05. `[craft 2024]` `[course seller 2024]` `[DR book 2009]`.

**R20. Pick 1 dominant appeal the product can credibly satisfy, and hold every variant to it before testing another.** Condition: every ad. Whitman: map results to the Life-Force 8 (survival, food, freedom from fear and pain, sexual companionship, comfort, superiority, care of loved ones, social approval) and the 9 learned wants; pick the one the product truly satisfies; the claim that LF8 drive more sales than all others combined is his view, uncited [5cfd138f2ca5] [012ce7b91762]; Copy Hackers: a message targets a pain or reflects a motivation; a discount is not a motivation [fb5fb47770a9]; Founders: state the appeal in 1 sentence before writing [ea531107827e] [6111749e4303]. Sources 02, 06, 07. `[DR book 2009]` `[SaaS 2011]` `[print 1920s]`. `[needs brand data: which desire buyers name in reviews and in past winning ads]`

**R21. Lead with the claim that appeals to the most buyers in your target segment; keep narrow claims in the body or in a minority of ads; do not let a narrow claim spoil a broad one.** Condition: choosing the headline claim. Hopkins: beauty over eczema; a claim that moves 1 in 4 buyers goes in some headlines and in every body [91b7cb943a89]; Tyson: do not narrow a hook to a slice of the list unless you segment [177dbbe025fd]. Reconciled with Copy Hackers' "write for 20% to 35%" [52564e4cb23c]: pick the segment first (R16), then the widest claim within it. Sources 01, 03, 06. `[print 1920s]` `[course seller 2024]` `[SaaS 2011]`.

**R22. Default to cure and reward over prevention.** Condition: choosing the appeal; exceptions are categories that sell on risk (card caveats name insurance and security; no source shows a store case). Hopkins: people do much to cure trouble and little to prevent it; the most successful toothpaste advertiser never featured tooth troubles [91b7cb943a89] [e9d818096148]; Founders: Pepsodent sold beauty, not decay prevention; never picture the afflicted [6111749e4303]. Sources 03, 07. `[print 1920s]`. See 7.5 for the negative-framing conflict.

**R23. Match depth to awareness: more story for problem-aware and solution-aware readers, short story plus many testimonials for product-aware readers, offer only for most-aware readers.** Condition: pages and emails; Jamie's default is stage 3 to 4, a medium to long story [3912f9a679c0]; Founders: length is for the reader who already showed interest [31dfb7e722f5]; Whitman's ELM (R8). Sources 02, 05, 07. `[coaching 2019]` `[print 1920s]` `[DR book 2009]`.

**R24. Create contrast with the old way or the category, never with a named rival, and never attack.** Condition: any comparison. Harry Dry: conflict drives memory; enemy types are a different approach, a belief, or a competitor; he does not take the third too seriously [a173f608eaa2] [e05c0ccdecf9] [988a4dabce09]; Whitman: two-sided messages beat one-sided only when you still argue your side, and comparison charts persuade peripheral thinkers [6fd2919611fb]; inoculation (warn, weak attack, strong defence) only with legitimate facts and a truly better product [d1717caa4ac6]; Hopkins: to attack a rival is never good advertising; "try our rivals' too" beat "beware of substitutes" [650b052b209a] [652fd908ec22]; Founders: "avoid imitations" is a selfish phrase that can kill an ad [250834566833]. ecomOS: no copying competitor text; claims about rivals need verified facts `[needs brand data]`. Sources 02, 03, 04, 07. `[craft 2024]` `[DR book 2009]` `[print 1920s]`.

**R25. Name the thing that makes the product different, and make sure it is true and ownable.** Condition: any product that risks price comparison. Tyson's unique mechanism: name the feature, say why it works and why alternatives fail (his examples are invented for teaching) [ecb28758fd66] [79bb35cef343] [384b4df664c6]; Whitman: a USP must be true; if it is not who you are yet, make it so [0463438d3951] [6468d5100e59] [902431ce25d6]; Harry Dry: never write a line a competitor could sign [954f8676cb20]; Rule of One: 1 USP, not 19 [b720ce9767c7]. Sources 01, 02, 04, 09. `[course seller 2024]` `[DR book 2009]` `[craft 2024]` `[DR publishing]`.

**R124. Build 1 reusable copy skeleton per product line (headline formula, bullet order, proof slot) so each SKU is filled in, not rewritten from scratch; keep the SKU-specific spec and image unique.** Condition: any brand selling more than a handful of SKUs. Source 01 names catalogue-scale copy as a gap it does not fill (01-8-hour-copywriting-course-for-beginners.md:391). `[general practice]` No library source; verify against brand data before use.

### Group D. Headlines

**R26. The headline's promise is also the PDP's first line and the collection hero; write it once and reuse it where the brand allows.** Condition: default for ads, emails and page heroes; see R54 and 7.2 for when a feature lead beats it. Whitman: biggest benefit in the headline "always, without exception"; he says 60% read only headlines (uncited) [56c0f6af65ab] [db040c273327]; Hopkins: the headline hails the people you can interest and only them, like calling "Hey there, Bill Jones" [c1863a8437f7]; Founders: headlines reveal or conceal an interest; spend most of your copy time here [e2b526314c8d] [1c9885b21bef]; Tyson's page stack: eyebrow calls out the reader, headline carries the big promise, deck raises ease or adds a guarantee [4b264d3e8066]. Sources 01, 02, 03, 07. `[print 1920s]` `[DR book 2009]` `[course seller 2024]`.

**R27. A reader who sees only the headline must be able to say what is sold and for whom. No blind, clever or pun headlines.** Condition: every headline; test it by showing the headline alone (02). Whitman's "what is sold?" test and cleverectomy [0e09cddd6797] [56c0f6af65ab]; Hopkins: a blind headline draws many readers but the wrong ones [c1863a8437f7]; Founders: headlines must not mislead [1c9885b21bef]; Harry Dry: the 2-second test ("One Mississippi, two Mississippi"), with his caveat that not everyone has to get it (7.15) [220e0eb8c1d5] [eb5614dd91ba]. Sources 02, 03, 04, 07. `[DR book 2009]` `[print 1920s]` `[craft 2024]`.

**R28. Put a true specific in the headline where one exists: a number, a time, a count, a price.** Condition: the figure is in the brand record. Whitman: add specifics (numbers, time, price, guarantee), all true [db040c273327] [581f8a1a98cd]; Hopkins: "3 1/3 times the light", "reduced 25 percent", "52 nations" [975c891bc15a]; Founders: "78-second shave", "net profit is 3%" [203ef216f7b2]; Harry Dry: you can only point [d6f95f2facce]; Tyson's headline formula: time frame plus discovery plus outcome plus ease, with the caveat that income claims are policed [3b6b0416a183]. Sources 01, 02, 03, 04, 07. `[print 1920s]` `[DR book 2009]` `[craft 2024]`.

**R29. Of 2 equally good headlines, choose the shorter; expect a drop above 12 words.** Condition: after the benefit is in; never shorten by cutting the benefit or the specific. Whitman's 2 rules and Rudolph's 1939 to 1940 data on 2,500 Saturday Evening Post ads (3 words or fewer read fully by 87.3%, 13 words or more by 77.9%) [87ab9b6867da]; Harry Dry: shorter is better "most of the time" [8e6c32baa35f]. Ogilvy's counter that longer headlines sell more is noted by 02. Sources 02, 04. `[print 1920s]` `[craft 2024]`.

**R30. Write many headlines, spend hours, discard scores, and change the headline first when an ad fails.** Condition: every ad set; a headline bank of at least 10 candidates before choosing 3. Hopkins keyed nearly 2,000 headlines on 1 product and saw 5 to 10 times swings [c1863a8437f7] [fe816803de4e]; Founders: hours on 1 headline [e2b526314c8d]; Whitman: headline first, then price, then offer (card [d7cbcd4ec542] reverses this; the book says headline first); Harry Dry: about 25 rewrites over 2 days for 1 ad [6e39a617d9e1]. Sources 02, 03, 04, 07. `[print 1920s]` `[DR book 2009]` `[craft 2024]`.

**R31. Use Caples' 4 qualities (self-interest, news, curiosity, quick easy way) and the 22 starters as generators, not templates.** Condition: building the headline bank. Whitman [935888c8c1f1] [2f196d76cd7a]; Tyson's attention formula: promise that is not spammy, intrigue that is not confusing, emotion that is not clickbait [ccb66d506164]. Whitman calls the starters "tested" with no data. Sources 01, 02. `[DR book 2009]` `[course seller 2024]`.

**R32. Use curiosity only with targeting and a payoff that matches.** Condition: any curiosity or mystery hook. Hopkins: curiosity is one of the strongest incentives (Puffed Wheat "shot from guns") [652fd908ec22]; Whitman: "SEX!" over patio furniture pulls the wrong eyeballs [935888c8c1f1]; Tyson: clickbait is a headline the content does not deliver [ccb66d506164]. Sources 01, 02, 03. `[print 1920s]` `[DR book 2009]` `[course seller 2024]`.

**R33. Write the headline in the final surface, beside the image, and judge it among other ads.** Condition: static ads and feeds. Harry Dry writes in Figma, drops placeholder images early, fixes line breaks by cutting words, and mocks a billboard among about 7 others [e93a8cf681bd] [220e0eb8c1d5]; v1.2: the headline must be understandable next to the supplied product photo brief. Whitman's print formatting (initial caps, all caps only at 4 to 5 words, break lines at phrase points, quotes "can boost reading 25%" uncited) is print era [388f0c750aad] [14dcce0a0c2a]. Sources 02, 04. `[craft 2024]` `[DR book 2009]`.

**R34. Product identity: enough that the ad stands alone, but the product name does not lead a long-form page hero unless the brand is a household name.** Condition: ads need product identity (v1.2; Whitman's "what is sold" test). Jamie: no product name in the hero of a sales page unless you are Mercedes or Apple [8ff8c1675824]. Conflict for product pages, where the product name is normally the H1: see 7.4. Sources 02, 05. `[coaching 2019]` `[DR book 2009]`.

### Group E. Hooks and first lines

**R35. Attention has 3 parts: a promise that is not spammy, intrigue that is not confusing, emotion that is not clickbait.** Condition: hooks, subjects, first lines. Source 01 [ccb66d506164] [f90f84d09846]. Spammy promises can push email to spam and risk a Meta account `[web check: current Meta advertising standards]`. `[course seller 2024]`.

**R36. Line 1's only job is to get line 2 read. Cut the lead. First sentence at most 14 words, ideally 7 to 10; opening paragraph at most 11 words.** Condition: emails, primary text, page copy. Tyson: "cut stuff in the beginning" is his first note on about 80% of critiques; no greetings, no "I hope", no "what if I told you" [610c9fac80ba] [f614c8ab3ac7] [0666118ff844] [f0259cdd1faf]; Whitman: the first sentence's only job is to get the second read; Ogilvy's 11-word opening paragraph [6d882bfcd851] [d2d7d23b7635]; Harry Dry via Sugarman [7272fafc80c7]; Sandcastles' shared pattern: avoid throat-clearing openers that delay the value [38a495e39205]. Sources 01, 02, 04, 08. `[course seller 2024]` `[DR book 2009]` `[craft 2024]` `[organic video 2026]`.

**R37. Front-load the payoff in a confident declarative. A question opener is allowed only when it names the buyer's exact situation; never a hedged question.** Condition: cold feed hooks and first lines. Sandcastles' model finding across 3 creator channels: "winners say things, losers ask questions" (1 run, organic, content creators) [38a495e39205]; Whitman: rhetorical-question research is split and Gayle, Preiss and Allen 1998 found no appreciable effect on persuasion; questions may aid memory [ecc5de375921]; against: Whitman's own letter opener "Do you want...?" [6d882bfcd851] and Tyson's perplexing question ("How come some people... while others...?") [f0259cdd1faf]. Conflict 7.8. Sources 01, 02, 08. `[organic video 2026]` `[DR book 2009]` `[course seller 2024]`. `[needs brand data: question vs declarative hook results in own ads]`

**R38. State, then amplify: sentence 1 makes the claim, sentence 2 adds a comparison or contrast.** Condition: hooks and primary text openers. Sandcastles: winners pair a stat with a second-sentence amplifier; losers state and stop [38a495e39205]; Harry Dry: contrast and juxtaposition make lines stick ("supermodels in London and dads in Ohio") [988a4dabce09]. Sources 04, 08. `[organic video 2026]` `[craft 2024]`.

**R39. Bridge headline to body with 1 device that flows from the headline.** Condition: body copy after a headline. Whitman's 12 lead-ins: continue the thought, ask a question, quote an authority, give a free taste, challenge them to prove it, story of skepticism, what others say, play reporter, get personal, dramatic story, super-detailed specs, very short first sentence [40367b3bec34]. Source 02. `[DR book 2009]`.

**R40. Keep the punchline for the end, but give a hint of the mechanism. Withholding everything gets clicks and no buyers.** Condition: emails and ads that lead to a page. Tyson: problem, agitate, "click to learn how" with no hint raises clicks and lowers purchases; close one loop with real value, open the next behind the CTA [0cf0f5e70b0b] [3e63ec1c1227]. Source 01. `[course seller 2024]`. `[needs brand data: click to purchase rate by email]`

**R41. Challenge a common belief only when the product can honestly justify the challenge.** Condition: CJN or contrarian hooks. Tyson's CJN (Challenge, Justify, Need) is taught with "is this true or not is beside the point"; the ecomOS rule bans that [8919626d89c1] [930c67d53174]; Whitman: never say "you're wrong"; change focus or importance instead [dd9d7f53de83]. Sources 01, 02. `[course seller 2024]` `[DR book 2009]`.

**R42. Ground any AI hook generation in the brand's own winners, reskin formats rather than clone them, strip any proof the model invents, and let a human pick.** Condition: whenever an LLM drafts hooks. Sandcastles: cold "write me hooks" prompts are generic; analyse your own backlog first, competitors separately; screen formats for topic fit; the model wrote "I studied 200 videos" as proof, which must never ship [a80ff986fd63] [14df3bb700a0] [fdd73f8bda1d] [721989c4c0ef] [e9f81c60dc73]; Tyson: write first, lift only lines that beat yours, strip AI tells [57ebdcf883f4] [5f65d6e25e3c]; Harry Dry: AI is a research tool; taste and conviction are yours [80c71cd2a847]. Sources 01, 04, 08. `[organic video 2026]` `[course seller 2024]` `[craft 2024]`.

### Group F. Body structures for ads, emails and pages

**R43. An ad body moves attention, interest, desire, proof, action, in that order; close the proof step with a store-owned signal, a star rating, a review count or a return-policy line, not a generic quality claim.** Condition: any ad long enough to have a body. Whitman's AIDA with proof added [043af87cd47d] [376eaacb3ff8]; Tyson's 4 jobs: attention, consumption, persuasion, action [583aa3b7fca0]. Sources 01, 02. `[DR book 2009]` `[course seller 2024]`.

**R44. The body adds a reason to care that the headline did not give: 1 recognisable situation, 1 relevant feature, the practical benefit that feature credibly provides.** Condition: static ad primary text. v1.2, supported by Harry Dry: copywriting is arguing and the conclusion is to buy [bf82611ee658], and Whitman's benefit of the benefit [012ce7b91762]. Do not repeat the component list in every variant (v1.2). Sources 02, 04. `[craft 2024]` `[DR book 2009]`.

**R45. Choose the email structure before writing, then fill it.** Condition: every email. Tyson's 3: PPAS (problem 3 to 4 lines, promise 2 to 3, agitate 7 to 8, solution and CTA about 7; never problem, agitate, then promise) [3e63ec1c1227] [a3f13080cb06]; CJN [930c67d53174]; HSO (hook, story with 2 beats, lesson, offer) [4a2f08fa92d1]; Jamie's outline block: goal (value or sell), subject, preview written by hand, story, "today I want to talk to you about X", content, CTA, P.S. pre-written [c3c4e6142fe4] [5a403376e7b5]. Sources 01, 05. `[course seller 2024]` `[coaching 2019]`.

**R46. Tell a story, not a chronology: a main character, a goal, adversity, a turn, and the lesson at the end. Relive 1 moment; do not retell a timeline.** Condition: story emails and founder or customer story blocks. Tyson [f6de27013260] [e8cdc6cbf78e] [a3f3d55f4e85] [adc834e923a1]; Harry Dry: find the "but" and build the turn naturally [a173f608eaa2]. Sources 01, 04. `[course seller 2024]` `[craft 2024]`.

**R47. Page order: hero (eyebrow, headline, deck, CTA) answering who is this for, why keep reading, what do I do next; then blocks; headers read alone must tell the story; CTA every 2 to 3 sections; FAQ at the bottom.** Condition: landing and sales pages; product pages follow 07-LPG. Tyson's blocks: what is X and why, meet the founder, relate to the reader, feature plus benefit bullets, testimonials, value stack, urgency, FAQ dropdowns [4b264d3e8066] [4f95db866881] [073d27caa4b0]; Jamie's 11-step template and header through-line [8ff8c1675824] [457ab3b6b02d] [caee8d24b0f0]; Copy Hackers: place messages where people look, not in rank order top to bottom [e374cf034894]; Whitman: end with a P.S. that restates the offer [1e562730b6b2]. Sources 01, 02, 05, 06. `[course seller 2024]` `[coaching 2019]` `[SaaS 2011]` `[DR book 2009]`.

**R48. Give the reader every proven claim needed to decide, all in service of the 1 idea. Do not serialise claims across ads. Do not pad.** Condition: pages, long emails, and any ad whose reader has shown interest. Hopkins: tell a reasonably complete story; omit a claim and some readers lose the fact that would convince; "the more you tell the more you sell" ("never failed in any test we know", no numbers); length follows the product, 1 sentence for chewing gum [8946e9e66b01] [243d845edcb1]; Founders: some of Hopkins's best ads were about 15,000 words, for an interested reader [84d9f8424c4b] [31dfb7e722f5]; Whitman: long copy wins "no qualifications" but must stay interesting; Sackheim: short copy only when there is little to say [bef86f46c5c6]; Copy Hackers: overwrite 2,000 words for 1,000, then cut [753e79e5c3d8]; Rule of One: every claim a sub-point of 1 idea [491bae29b0be]. Conflict with short feed copy: 7.1. Sources 02, 03, 06, 07, 09. `[print 1920s]` `[DR book 2009]` `[SaaS 2011]` `[DR publishing]`.

**R49. Pace the copy: mix short and long lines, add a short scroll-stopper line where a skimmer's eye should stop, and keep paragraphs short.** Condition: all body copy. Tyson: pace like an action movie; no wall of long lines, no all one-liners [a5360ff26b1f] [ce4adcb0c5bf]; Harry Dry: paragraphs of 2 lines or fewer (his habit, "idiosyncratic") [23276eda58ce]; Whitman: normal paragraphs about 4 or 5 short sentences; the short-short paragraph trick [d2d7d23b7635]; Jamie: 1-sentence paragraphs in social ads, 1 to 3 sentences at most [36b9e7b8a840]. Strictest for feed ads: 1 to 3 sentences per paragraph (05). Sources 01, 02, 04, 05. `[course seller 2024]` `[craft 2024]` `[DR book 2009]` `[coaching 2019]`.

**R50. Show many benefits as short bullets or numbers; long bullets defeat the purpose.** Condition: pages and long emails. Whitman's checklist [388f0c750aad]; Tyson: bullets are the fastest unit; keep them short; do not centre small text [c4995809f1dc] [28ee2e3aa4ff]. Sources 01, 02. `[DR book 2009]` `[course seller 2024]`.

**R51. In long copy, restate the main benefit from several angles (how they feel, how others see them, safety, savings), and break it with selling subheads and captions.** Condition: pages and sales letters. Whitman [bef86f46c5c6] [ea9e5fa0f35f] [6e8715d19594]. Source 02. `[DR book 2009]`.

**R52. Acquisition copy speaks to new buyers; list copy assumes the reader knows the product.** Condition: cold ads vs owned list. Hopkins: never waste a line on present users except in the headline (his letters to customers show he still marketed to them by mail) [8946e9e66b01]; Tyson: an ecommerce list is buyers plus discount sign-ups; do not open with "what is this?" [8a4864a0a123]. Sources 01, 03. `[print 1920s]` `[course seller 2024]`.

**R125. Write the product page in 3 blocks: a title that names the product and its key spec, a bullet block of specific features each tied to a benefit, and a spec block with the exact numbers a shopper filters or searches by.** Condition: any product detail page; page layout and build are 07-LPG's, this rule covers the words only. No source in this folder gives PDP guidance directly; the "PDP" language in cards from 02, 03 and 04 is the card writer's own translation, not the source text (02-cashvertising.md:596, 03-scientific-advertising.md:526, 04-learn-copywriting-in-76-minutes-harry-dry.md:291). `[general practice]` No library source; verify against brand data before use.

### Group G. Feature to benefit, abstract to concrete

**R53. Ladder every feature to the buyer's gain using the product's own spec-sheet units (denier, GSM, mAh, wash count), not a marketing adjective.** Condition: every feature that stays in copy. Whitman: react as the prospect ("BIG DEAL! What's in it for me?"), answer "You benefit by...", then ask "what's the benefit of that?" until you reach the end value; do not turn a benefit into a number the product data cannot support [dc660f4f168c] [012ce7b91762] [376eaacb3ff8]; Copy Hackers: a feature's purpose is still the feature; the benefit is what improves in the buyer's life, and it changes by segment (the gluten-free cake for a grandmother vs a teacher) [70aaf0b3735c]. Sources 02, 06. `[DR book 2009]` `[SaaS 2011]`.

**R54. There is no fixed rule to lead with the benefit. Lead with the feature when the buyer compares specs, distrusts soft language, or came for 1 feature they heard about. Whatever leads, pair it: every feature with a benefit, every benefit with a feature or a support point.** Condition: choosing the lead line per audience. Copy Hackers saw a feature headline beat a benefit headline [d5db0dddac4a]; Whitman's ELM: central-route buyers want facts [42c77acaccca]. Conflict with R26: see 7.2. Sources 02, 06. `[SaaS 2011]` `[DR book 2009]`.

**R55. Swap a vague quality word for the unit a shopper filters or searches by on the store (size, material, capacity, color, fit).** Condition: every vague line. Harry Dry: concrete words are things you can drop on your foot; run the abstract-to-concrete line ("regain fitness" to "Couch to 5K") [8e6c32baa35f] [eb5614dd91ba]; Whitman: build the mental movie (place, object, action, sense), swap bland phrases for powerful visual adjectives, run VAKOG [8998cd84ed0c] [b74a2213dcd8] [4366c3a8be93]; Tyson: hyper-specific beats "I had a lot of bills" [4a2f08fa92d1]. Sources 01, 02, 04. `[craft 2024]` `[DR book 2009]` `[course seller 2024]`.

**R56. Figurative swaps ("1,000 songs in your pocket") are allowed only where no reasonable reader takes them as a factual spec. Never on numbers, times, outcomes or safety.** Condition: metonymy in headlines. Harry Dry praises the iPod line and admits it is not literally true, which sits against his own "can I falsify it" test [fc16ebab7e1b]. ecomOS: claims must match the brand record. Source 04. `[craft 2024]`.

**R57. Cut a spec bullet that answers no filter, size guide or "will this work for me" search; keep it only if a shopper would search for it.** Condition: every asset. Copy Hackers [7f5165a57e7a]; v1.2: select the fact relevant to the angle; Harry Dry: 1 idea, not "jeans and t-shirts and socks and dressing rooms" [867743b221ba]. Sources 04, 06. `[SaaS 2011]` `[craft 2024]`.

**R58. Describe a big commitment by what changes, not by its label.** Condition: costly or effortful offers. Tyson: "a 12-week 1-to-1 program" sounds costly; describe sitting down with a professional and what changes [e9741d568a97]. Source 01. `[course seller 2024]`.

**R126. Word a bundle or kit as 1 line naming what is included, the saving versus buying separately (computed in code), and the 1 reason the pieces work together.** Condition: any multi-SKU offer. Only card-writer translations touch this in the folder's sources, and one is flagged as not traceable to its source text [b990935f853d]. `[general practice]` No library source; verify against brand data before use.

### Group H. Specificity and proof

**R59. Replace every superlative and adjective with a number, a name, a process fact or a checkable statement. A specific claim is either true or a lie; a generality is discounted.** Condition: every line; 6 of 9 sources agree. Hopkins: "best in the world" suggests a careless truth and makes readers discount everything [975c891bc15a]; Founders [203ef216f7b2]; Whitman: extreme specificity wins even when rivals do the same thing, because nobody else says it [9f88626f46bc] [581f8a1a98cd]; Harry Dry: you can't talk, you can only point [d6f95f2facce] [eb5614dd91ba]; Copy Hackers: specifics stick; do not summarise to fit a space [d5db0dddac4a]; Sandcastles: specificity beat abstraction on all 4 channels [38a495e39205]. Sources 02, 03, 04, 06, 07, 08. `[print 1920s]` `[DR book 2009]` `[craft 2024]` `[SaaS 2011]` `[organic video 2026]`.

**R60. Run the 3-question test on every line: can I visualise it, can I falsify it, can nobody else say this.** Condition: every sentence of an ad, hook, headline or hero line. 3 no answers means rewrite. Source 04 [eb5614dd91ba] [954f8676cb20]. `[craft 2024]`.

**R61. Rank proof: a demonstration first, then evidence not created by the brand (testimonials, reviews, third-party tests, seals), then cost narration and process facts, then analogy. A bare claim reads as "this dude is full of crap".** Condition: any claim of result. Founders: no argument compares with 1 dramatic demonstration [30ea811c01b3]; Whitman: evidence is "any factual statement, object or opinion not created by the source"; examples beat statistics, and the product sets the mix [a9db8de6d903] [7885a72eb3c6]; Tyson's 6 proof types (analogy, quote, statistic, cost narration, hypothetical, borrowed authority) and "be a stat shower" [574fd7aa2de4] [2b2ec22dc668] [792856b9a23c]; testimonial marketing is "the most safe yet effective form" [017ae2c141f9]. ecomOS override: a statistic or quote enters copy only from a checked source in the brand record; Tyson's "stats straight from Google" and "ask ChatGPT for stats" are not permitted (see R107). Sources 01, 02, 07. `[course seller 2024]` `[DR book 2009]` `[print 1920s]`.

**R62. Show conviction instead of telling the reader what to think; let design and the product prove what copy would otherwise assert.** Condition: results claims and quality claims. Tyson: "here's how mine went from this to this" beats "you can lose 20 lb", his heuristic is 90% of the time [60835ecfe3d0] [e9741d568a97]; Copy Hackers: let the product's own presentation prove the claim; for a store, that means a packaging or unboxing shot doing the showing, not a caption asserting quality (source's own example used a SaaS product's screen; moved to Appendix A) [61d04467e873] [e5294ffc5f69]. Sources 01, 06. `[course seller 2024]` `[SaaS 2011]`.

**R63. Where the brand has a review platform, quote the star rating and review count as proof, not a hand-picked testimonial alone.** Condition: any asset with room for proof. Whitman: volume signals strength (Length-Implies-Strength); collect with a release and quotable questions [952aca21b0fb] [5ae1f82d7e99]; Jamie: success emails work best when each testimonial answers an objection [0c6041550953]. `[web check: endorsement and review rules in the brand's market]`. Sources 02, 05. `[DR book 2009]` `[coaching 2019]`.

**R64. Small, believable claims beat big ones. A nearly unbelievable true claim needs examples on the same surface. An impossible claim never runs.** Condition: every promise. Harry Dry's course ad promises 1% to 2%, not millions [bf82611ee658]; Copy Hackers: never an impossible line; back a bold line with clear examples [6b829c0c6b03]; Tyson: promises must be attainable and hyper-specific; "an ounce of proof weighs the same as 100 lb of promise" [017ae2c141f9]. Conflict with bold hooks: 7.6. Sources 01, 04, 06. `[craft 2024]` `[SaaS 2011]` `[course seller 2024]`.

**R65. Back every factual claim with a source the agent has seen, and verify impressive claims before they run.** Condition: every number, study, count or comparison. Copy Hackers: support can be a link to the original article [19bf368e3817] [fb5fb47770a9]; Hopkins sent claims to a lab and turned "large food value" into 425 calories per pint; an untrue claim "may prove a boomerang" and bar the ad [6959d40e0dc8]. Sources 03, 06. `[SaaS 2011]` `[print 1920s]`.

**R66. Do not over-explain ordinary statements; defend only the bold ones.** Condition: editing. Copy Hackers: people accept ordinary claims because questioning is exhausting; bold claims still need proof [10a92744aa71]. Source 06. `[SaaS 2011]`.

**R67. Name who the product does not fit by size, skin type, use case or climate; this cuts returns as much as it raises trust.** Condition: where the brand can name a real non-fit. Whitman's takeaway raises credibility [5ba65827a517]; Tyson: speak to the right avatar, never "it works for everyone" [017ae2c141f9]. Sources 01, 02. `[DR book 2009]` `[course seller 2024]`.

### Group I. Offers, guarantees and deadlines in copy

**R68. Frame the offer as service and take the risk off the buyer.** Condition: every offer line. Hopkins: the best ads ask no one to buy; they offer information, a sample, a trial, goods on approval; people can be coaxed, not driven [dad9da2fb2e6]; Founders: ask a person to take a chance on you and you have a fight; offer to take a chance on him and the way is easy (no mechanism given) [5558b5dedefc] [30ea811c01b3]; Tyson's ecommerce blockers: risk (small pack sizes, a return guarantee), price, effectiveness [8a4864a0a123]. Sources 01, 03, 07. `[print 1920s]` `[course seller 2024]`.

**R69. State the offer as 1 concrete line: what is offered, the qualifying condition, and what it applies to.** Condition: any discount, threshold, bundle or fee offer. Whitman: say how to order step by step, "It's easy to order" [3d848b082e13]. Moved to Appendix A: Copy Hackers' Fidelity fee-rewrite case [690303793634]. Sources 02, 06. `[SaaS 2011]` `[DR book 2009]`.

**R70. Write the strongest guarantee operations can honour, in plain terms, and show it where the decision happens.** Condition: the brand record confirms the policy and its cost. Whitman: longest and strongest in the industry, long term over 30, 60 or 90 days, show it with a signature; "studies show" long guarantees cut returns (uncited) [83551014328e]; Hopkins: guarantees "have ceased to be impressive"; a local dealer's signed warrant and "pay in a week if you like them" beat money-back "many times" (1920s cases) [652fd908ec22] [abac911ba2b0]; Tyson's store example: "try it risk-free with a 30-day guarantee; if you don't love them, send them back" [8a4864a0a123]. Conflict: 7.16. Sources 01, 02, 03. `[DR book 2009]` `[print 1920s]` `[course seller 2024]`. `[needs brand data: return rate, refund cost, margin]`

**R71. Put a deadline or limit in copy only when it is real, state the time or units left in digits, and repeat the CTA.** Condition: promotions with a true end date or stock limit. Whitman: "always feature deadlines", hard ("Sale ends August 21st") or soft ("first 50 callers"), on every piece including the form [7181b1222823] [98e718ecef90]; his card adds the limit must be real and fake countdowns can break consumer law [61bd1ae6936b]; Tyson: only situational urgency keeps goodwill; fake scarcity on infinite goods makes no sense; deadline email states "only 48 hours left" and doubles the CTA [8f116e83a3f3] [073d27caa4b0] [3afc3ff48150]; Hopkins: pay for prompt action or tell what delay costs; many successful letters expire on a date [e48273314166]. ecomOS: never invent urgency. Conflict 7.7. Sources 01, 02, 03. `[DR book 2009]` `[course seller 2024]` `[print 1920s]`. `[web check: urgency and countdown rules in the brand's markets]`

**R72. Make believed value exceed price with real numbers: a value stack only with true component values, a cost comparison against the real alternative, and no cheapness appeal.** Condition: price positioning on pages and in sales emails. Tyson: nobody buys something for $100 that is worth $100; benefit bullets and compare and contrast raise perceived value [f5368da16a22] [29770c1882af]; Jamie: offer stack or apples-to-oranges (trainer plus chef plus nutritionist vs the course), plus the cost of inaction [c7a79cc9ee3e]; Whitman: WIIFM, and his 9 ways to convey value (amortise, tell what it is worth, why the price is low) [408a28943dcf] [a5e12a547cc8]; Hopkins: people want bargains, not cheapness; people judge largely by price, so a high price can be an inducement on lines judged by price [652fd908ec22] [4afe300cc039]. ecomOS: values in a stack must be real prices from the brand record; compute totals in code. Sources 01, 02, 03, 05. `[course seller 2024]` `[coaching 2019]` `[DR book 2009]` `[print 1920s]`. `[needs brand data: real component prices]`

**R73. An offer limited to a real group beats a general offer.** Condition: the buyer plausibly belongs to the group (veterans, members, past buyers, a profession). Hopkins [652fd908ec22]; Founders [2aab472f73cf]. Never fake a group. Sources 03, 07. `[print 1920s]`.

**R74. Trial wording: free on request beats part-price, and a free thing handed out unasked cheapens the product.** Condition: sample and trial offers. Hopkins: charging a dime or a stamp costs 40 cents to $1 extra per reply; "you buy one, we buy the other" does not pay; give samples only to people who asked after reading the story; a free full-size package given away failed while a maker-paid retail coupon succeeded (1920s cases) [0e72ef7fa48e] [dad9da2fb2e6]; Founders: "promiscuous sampling" is a very bad plan [04185b470730]. The sources are silent on percentage discount codes for first orders; see 7.16. Sources 03, 07. `[print 1920s]`.

**R75. A discount, a limited-time offer or the value proposition is not the motivation. Reflect the deeper reason to buy in its own line.** Condition: home pages and primary flow pages; also the first line of a promo email. Copy Hackers [fb5fb47770a9] [718d826f9fb7]. Source 06. `[SaaS 2011]`.

**R127. Word a discount or promo code as 1 concrete line: the percent or amount, what it applies to, and how to get it (a code, an email-signup gate, or automatic at checkout).** Condition: any promo beyond a flat storewide percent off. Source 05 names discount and promo wording beyond a flat percent off as a gap (05-copywriting-101-ecommerce-copywriting-course-for.md:334); 1 card covers gating a discount behind email capture [58af3dd961fe]. `[general practice]` beyond that card; verify against brand data before use.

**R128. Word subscription and repeat-purchase copy around the ongoing choice, not the first sale: what ships and when, how to pause or skip, how to cancel, and the saving versus a one-off order.** Condition: any subscribe-and-save or replenishment offer. No source in this folder covers subscription copy; "subscription" appears only as a business-model aside. `[general practice]` No library source; verify against brand data before use.

**R129. For a mobile-first, non-US market, state the real payment and delivery facts the buyer needs to trust the order: cash-on-delivery availability, the price in the local currency, and how order confirmation reaches them (for example WhatsApp).** Condition: a brand selling into a market where these are live concerns, for example Gehna in India. No source in this folder covers this; "WhatsApp" appears once as a card-writer analogy with no source text behind it (03-scientific-advertising.md:526). `[general practice]` No library source; verify against brand data before use.

### Group J. Objection handling

**R76. Shift a belief in 6 steps: name the belief in the reader's words, challenge it gently, sympathise, show the old belief's failure mode, prove the new belief, sell from the new belief. Run belief shifts against the store's actual blockers: shipping cost, return hassle, sizing risk and authenticity.** Condition: any objection that is a belief rather than a fact. Tyson [68cf28c41359]; Whitman: change the focus or the importance of a belief; reinforce what they already hold [dd9d7f53de83]; Jamie: sentiment matching gives the reader's words [fb6ca632b8da]. Sources 01, 02, 05. `[course seller 2024]` `[DR book 2009]` `[coaching 2019]`.

**R77. Preface an objection so a skimmer who fits does not leave, put the full FAQ at the bottom, and let testimonials answer objections one each.** Condition: pages and mid-sequence emails. Tyson: "Most people feel investing only works if you start early..." rather than stating the objection as fact; FAQ dropdowns at the very bottom for people who scroll straight down [073d27caa4b0] [3e3d5f0de011]; Jamie: FAQ email built from chat, email and page messages; success email with 1 long testimonial or several, each answering an objection [0c6041550953] [8ff8c1675824]. Sources 01, 05. `[course seller 2024]` `[coaching 2019]`.

**R78. For a store list, address the 3 blockers: risk, price, effectiveness (how and why it works, what it does differently).** Condition: emails to people who already know the product. Source 01's nose-strip critique [8a4864a0a123]. `[course seller 2024]`.

**R79. Do not handle every objection in 1 email; too much objection handling makes 288 words feel long.** Condition: emails. Source 01 [b1fc36d11cab]. `[course seller 2024]`.

**R80. Pre-empt a rival's pitch by telling the buyer what to look for, only with true information and a truly better product, and with a weak attack, never a strong one.** Condition: category with a known competing claim. Whitman's inoculation [d1717caa4ac6]. Source 02. `[DR book 2009]`. Combined with R24: no named rival.

### Group K. Calls to action

**R81. Label the single CTA with the store action it triggers (add to cart, shop now, get yours); a product grid counts as 1 action only when the email's whole job is "shop the range."** Condition: ads, emails, page sections. Tyson: action's biggest enemy is confusion; too many options means no click; the P.S. soft sell and the double CTA are the allowed repeats [b1fc36d11cab] [cab8c603e36c] [744657e341ac] [22a2130d998e] [3afc3ff48150]; Jamie: 1 function per asset [c3c4e6142fe4]; Whitman: the P.S. restates the offer and is often read first [1e562730b6b2]. Conflict with product grids and multi-link store emails: 7.3. Sources 01, 02, 05. `[course seller 2024]` `[coaching 2019]` `[DR book 2009]`.

**R82. Tell people what to do, positively and outright, and make the next step easy. Label buttons with what happens next.** Condition: every CTA. Whitman: make it easy, then ask ("Order now"); say how in numbered steps [d8e25cc5a2b0] [3d848b082e13]; Hopkins: "Send now for this sample", not "Why do you neglect this offer?"; assume people will do what you ask [650b052b209a]; Tyson's heatmap case: a bare "Start now" button nobody clicks because they do not know what is inside [22214793398e]. Sources 01, 02, 03. `[DR book 2009]` `[print 1920s]` `[course seller 2024]`.

**R83. The CTA says what to do, not how; the how is on the other side of the click, but the copy has already hinted at it.** Condition: emails and ads that lead to a page. Tyson [3e63ec1c1227] [0cf0f5e70b0b]. Source 01. `[course seller 2024]`.

**R84. The CTA and the page it opens must match the ad's promise in words, look and quality.** Condition: every paid click. Jamie: congruency is the biggest problem with paid ads; repeat the promise in new words like a reprise; a Spider-Man shirt ad must not land on the home page [dda3430eb956]; Hopkins: follow up along the line that created the interest, not a new argument [3cdc738f5682]. Sources 03, 05. `[coaching 2019]` `[print 1920s]`.

**R85. On a long page, place a CTA or price block every 2 or 3 content sections, and end with a P.S. or a final restated offer.** Condition: sales and landing pages. Jamie [8ff8c1675824]; Whitman [1e562730b6b2]. Sources 02, 05. `[coaching 2019]` `[DR book 2009]`.

### Group L. Voice, tone and framing

**R86. Keep voice consistent across every SKU and collection page without turning bullets into boilerplate; check 3 product pages side by side, not 1.** Condition: all copy; use the compile document's phrases. Tyson: a CPA does not talk like a business-opportunity coach; heavy emojis clash with a no-nonsense persona [3f95809c1b82] [88a07c18db1b] [134e00efad90]; Hopkins: give the advertiser a becoming style; never change a tone that won; appearing different every time never builds confidence [b5c60126fc0a]; Jamie: production quality and message must match what a warm audience already knows of the brand [dda3430eb956]. Sources 01, 03, 05. `[course seller 2024]` `[print 1920s]` `[coaching 2019]`. `[needs brand data: voice samples]`

**R87. Default to positive framing that shows the result and tells what to do. Negative framing is allowed when the product fully removes the weight and the framing is clear; hint at the negative otherwise. Never paint a vivid negative scene and attach the brand to it.** Condition: choosing the frame; test both when unsure. Hopkins: positive outpulled negative 4 to 1 in his tests; before and after are "follies"; show the face as it will appear [650b052b209a]; Founders: never picture the afflicted [6111749e4303]; Copy Hackers: negative is not banned; "Don't touch that" beats "Only touch this"; winners exist on both sides; do not attach the brand to a heavy negative image; rewrite negative copy only if the page converts poorly [19bf368e3817] [2c6f4cda6b12]; Whitman: fear works only with all 4 parts (threat, specific fix, proof the fix works, proof they can do it) and only if the product truly resolves it [23a92b334a3e] [724e63d042f4]; v1.2: avoid fear and exaggerated consequences. Conflict 7.5. Sources 02, 03, 06, 07. `[print 1920s]` `[SaaS 2011]` `[DR book 2009]`.

**R88. Put a real, named person behind the copy where the brand has one.** Condition: founder-led or expert-led brands; never an invented authority. Hopkins: a man is talking, not a soulless corporation; the motherly persona beat the bare offer [b5c60126fc0a] [abac911ba2b0]; Founders: personalities appeal, "Professor Anderson" had a real person behind it [762657ec71d8]; Whitman's authority position (headshot on everything) is for service and founder brands with no product-brand evidence [4036507c46bc]. Sources 02, 03, 07. `[print 1920s]` `[DR book 2009]`.

**R89. Write how you would say it to a friend. No jargon, no school-essay grammar, no AI tells.** Condition: all copy. Tyson's tells: "I hope this message finds you well", "take your business to the next level", "revolutionize", "don't miss out", magic-wand and cake analogies, the double dash [5f65d6e25e3c] [7de71d52b34a]; Whitman: no "constipated Harvard Law professor" writing [4960ce995f42]; Harry Dry: "yellow taxis, city that never sleeps" is secondhand filler; write from what you saw [a359f59b90c4]; Jamie: throw out SAT words [f27d97c52312]. Sources 01, 02, 04, 05. `[course seller 2024]` `[DR book 2009]` `[craft 2024]` `[coaching 2019]`.

**R90. Emojis: at most 1 or 2 in an email, more only in a social caption, and only if the persona uses them.** Condition: emails and captions. Tyson [d65a7b03c6a3] [134e00efad90]. Jamie's 2019 note that emojis and the waving hand pulled in ads is dated [36b9e7b8a840] `[web check: current norms]`. Sources 01, 05. `[course seller 2024]` `[coaching 2019]`.

**R91. Do not qualify the reader into a slice ("if you're 40ish") unless the send or the audience is segmented.** Condition: hooks and subject lines. Source 01 [177dbbe025fd]. `[course seller 2024]`. `[needs brand data: list and audience make-up]`

### Group M. Editing passes

**R92. Rest the draft, then read it aloud until you can read the whole piece without a stumble. Fix, then restart from the top.** Condition: every asset before delivery; 24 hours is the strictest rest (05), overnight (01), a walk (04). Jamie [e76793749fc7]; Tyson [28321b2f379b] [7fd437ffe114]; Harry Dry [f98be7ed26de]. Sources 01, 04, 05. `[coaching 2019]` `[course seller 2024]` `[craft 2024]`.

**R93. Cut every word that is not working: Kaplan's law, the burrito test, and the modifier sweep.** Condition: every draft. Harry Dry: words that are not working for you are working against you; pull 1 sentence out of a paragraph and if it still works the sentence should not have been there [23276eda58ce]; Tyson: cut "very", "really", "what if I told you", doubled words, repeated sentences; replace "almost" and "barely" with a real number [7de71d52b34a] [610c9fac80ba]; Whitman: cut "the aforementioned benefits" and its kin [4960ce995f42]. Sources 01, 02, 04. `[craft 2024]` `[course seller 2024]` `[DR book 2009]`.

**R94. Cut the lead and move the best line up.** Condition: every email and primary text. Tyson: about 80% of his critiques start here; if the body has a great line, move it into the subject or the first line [610c9fac80ba] [f614c8ab3ac7]. Source 01. `[course seller 2024]`.

**R95. Run the tossed salad audit: list every claim, flag any that is not a sub-point of the 1 idea, cut or rewrite it.** Condition: every asset; a stranger should be able to state the argument in 1 sentence (card's check). Source 09 [1ee01d6bfef2]. `[DR publishing]`.

**R96. Run the 3-question test line by line (R60) and the 2-second test on the whole ad.** Condition: ads and hero lines. Source 04 [eb5614dd91ba] [220e0eb8c1d5]. `[craft 2024]`.

**R97. Score readability and fix it by shortening words and sentences.** Condition: every asset; compute the score in code, not in the model. Whitman's Flesch pass and grade map [a2f59bfd45f7]; Tyson: Hemingway app, then read aloud [7de71d52b34a]. Sources 01, 02. `[DR book 2009]` `[course seller 2024]`. `[verify UI: readability tool]`

**R98. Overwrite, then cut. Make 4 or 5 versions of a key line, show a reviewer 3, get outside feedback once you have been on 1 ad for 2 to 3 hours, and ship only work you would rate 9 out of 10.** Condition: headlines and hooks; the whole ad for the feedback step. Copy Hackers: 10x the information, 2,000 words for 1,000 [753e79e5c3d8]; Harry Dry [189a7e6d8231] [6914df3c2bd8] [f98be7ed26de]; Tyson: review 3 pieces for every 1 you submit [7fd437ffe114]. Sources 01, 04, 06. `[SaaS 2011]` `[craft 2024]` `[course seller 2024]`.

**R99. Skim test: scroll without reading. The offer should rebuild from the bold and short lines; no wall of long lines, no centred small text, left-aligned body.** Condition: emails and pages. Source 01 [ce4adcb0c5bf] [28ee2e3aa4ff]. `[course seller 2024]`.

**R100. Subject line and preview text must match the email's angle; write the preview by hand; do not refer back to the subject inside the body.** Condition: every email. Tyson [134e00efad90] [0622a180b998]; Jamie [c3c4e6142fe4] [676688759b08]. Sources 01, 05. `[course seller 2024]` `[coaching 2019]`.

**R101. Write and check in the final surface so line wraps, truncation and the image are what the reader sees.** Condition: ads, emails, pages. Harry Dry [e93a8cf681bd] [220e0eb8c1d5]. Source 04. `[craft 2024]`. `[verify UI: preview tool for each placement]`

### Group N. Formats by placement

**R102. Meta primary text, headline and description: no source gives character limits or truncation points. Fetch them live before delivery and write to them.** Condition: every Meta ad set. `[verify UI: current Meta character limits and the "see more" truncation point for primary text, headline and description, per placement]` `[web check: Meta ad specs page]`. What the sources do support for the first visible lines: first sentence at most 14 words, ideally 7 to 10 (01) [f614c8ab3ac7]; 1-sentence paragraphs, 1 to 3 at most, in social ads (05) [36b9e7b8a840]; payoff in sentence 1, then amplify (08) [38a495e39205]; the headline must read next to the image and pass the 2-second test (04, v1.2) [220e0eb8c1d5]; a reader who sees only the headline knows what is sold (02) [0e09cddd6797]. Sources 01, 02, 04, 05, 08.

**R103. Email formats: subject at most 40 characters, no ambiguity, no period at the end; preview text written by hand; story and value emails 200 to 300 words; text-led with images only where they carry the message.** Condition: emails; the text-led rule conflicts with store practice, see 7.11. Tyson [0622a180b998] [134e00efad90] [a81371537582]; Jamie [676688759b08] [c3c4e6142fe4] [2bcad09a68e8]. Jamie's clipping figure ("about 2 MB") is her guess `[web check: current Gmail clipping limit]`. Sources 01, 05. `[course seller 2024]` `[coaching 2019]`.

**R104. Page hero: eyebrow (who it is for), headline (the promise), deck (ease, time frame or guarantee), 1 CTA; answer who, why keep reading, what next. Long-form sales pages omit the product name in the hero unless the brand is a household name; product pages keep it as the H1.** Condition: pages; see 7.4. Tyson [4b264d3e8066] [3e3d5f0de011]; Jamie [8ff8c1675824]. Sources 01, 05. `[course seller 2024]` `[coaching 2019]`.

**R105. Ad to page congruency: the first screen after the click repeats the promise in new words, in a similar look.** Condition: every paid click. Jamie [dda3430eb956]. Source 05. `[coaching 2019]`.

**R106. A static ad can be carried by 1 element (headline, or picture, or logo) when that element does the whole job; otherwise show product, promise and brand.** Condition: Harry Dry via Neil French (print) [7272fafc80c7] against v1.2's "enough product identity to stand alone" and Whitman's "show what you sell" [aa36dbcff998]. Treat the 1-element ad as a test, not a default. Sources 02, 04. `[craft 2024]` `[DR book 2009]`.

**R130. Write SMS as 1 short line: the offer or update, a clear action, and the opt-out or help instruction the carrier and law require.** Condition: any SMS send. Source 01 mentions SMS only as an automation action, with no copy rule, and names the gap directly (01-8-hour-copywriting-course-for-beginners.md:206, 391). `[general practice]` No library source; verify against brand data and current SMS compliance rules before use.

**R131. For a marketplace listing, front-load the title with the product, key spec and use case in the platform's expected order, and write bullets as short, keyword-led claims each sourced to the brand record.** Condition: any Amazon-style or marketplace listing. No source in this folder gives listing guidance; Amazon appears only as an example brand name in 01 and 05. `[general practice]` No library source; verify against brand data and the marketplace's current listing rules before use.

### Group O. Claim checking and compliance

**R107. No invented statistics, studies, quotes, test counts, review counts, customer counts, savings figures or "as seen in" claims. Every number traces to the brand record or a source the agent has opened.** Condition: absolute; ecomOS rule that overrides the sources. Sources that permit or model invention, which the agent must not follow: 01's proof types allow "statistics straight from Google" and prompts like "give me stats that prove X" and "give me quotes" [574fd7aa2de4] [2b2ec22dc668]; 01's CJN says truth is beside the point [930c67d53174]; 06's own example callouts carry unsourced stats ("over 30% of Americans spend $1,400 on coffee") despite its rule to back every claim [fb5fb47770a9]; 08's model wrote "I studied 200 of the most addictive videos" as proof [e9f81c60dc73]; 02 states uncited lifts ("quotes boost reading 25%", "Bill Me +50%") [037f584ed120] [3d848b082e13]; 05's offer stack puts a "75,000" value on a course [c7a79cc9ee3e]; 04's 22,000-hours line does not match its own inputs (4 x 300 x 30 = 36,000) [bf82611ee658]; 02's "Torpy's Tricky 200" shows how a long list of out-of-context quotes persuades [952aca21b0fb]. v1.2: never infer piece counts from a kit count; never invent setup time, ease, tools, compatibility, reviews, certifications, savings, urgency or safety assurances.

**R108. Verify impressive claims before they run; an untrue claim boomerangs and can bar the ad.** Condition: any claim of performance, purity, speed, count or comparison. Hopkins [6959d40e0dc8]; Copy Hackers [19bf368e3817]. Sources 03, 06. `[print 1920s]` `[SaaS 2011]`.

**R109. Check every claim type against current platform policy and consumer law: health, weight and body, income, before and after, safety, "free", urgency, comparative claims, personal attributes.** Condition: every launch-ready set. Tyson: anything that even looks like spam can get a Meta account shut down [f90f84d09846]; Whitman's fear, health and hygiene copy implies claims that need substantiation today [23a92b334a3e]; Copy Hackers' Teresa weight-loss example touches restricted copy [fb5fb47770a9]; Tyson's "$1,000 a day" opt-in headline is policed [3b6b0416a183]. `[web check: Meta advertising standards for each claim type; local consumer-protection rules on urgency and "free"]`. Sources 01, 02, 06.

**R110. Testimonials and reviews: real, permitted in writing, not edited to change meaning, with any incentive disclosed as the market requires.** Condition: any quoted customer. Whitman's release wording is lay legal advice from 2009 [5ae1f82d7e99]. `[web check: endorsement and review rules for the brand's country and each platform]`. Source 02.

**R111. Deadlines, stock limits and "selling fast" lines must be true at send time and expire when the fact expires.** Condition: any urgency. Whitman card [61bd1ae6936b]; Tyson [8f116e83a3f3]. Sources 01, 02.

**R112. No named-rival attacks and no competitor text. Comparison charts only with verified facts for both sides.** Condition: any comparative copy. Hopkins [650b052b209a]; Founders [250834566833]; Whitman [6fd2919611fb]. ecomOS rule. Sources 02, 03, 07. `[needs brand data: verified competitor facts]`

**R113. Figurative language passes only if no reasonable reader takes it as a spec, a time, a count or an outcome.** Condition: metonymy and hyperbole. Source 04 [fc16ebab7e1b]; ecomOS "no inflated words".

**R114. Guarantee and policy lines preserve eligibility limits exactly as the brand record states them.** Condition: any risk reversal. v1.2; Whitman: operations must honour it [83551014328e].

### Group P. Variant planning and testing

**R115. Each variant carries 1 genuinely different angle: a different supported benefit, customer moment, objection or execution. Different opening synonyms are not different angles.** Condition: every ad set; default 3 variants. v1.2; Hopkins: run many appeals, and use different ads across overlapping audiences [fe816803de4e]; Founders: framing levers are the group addressed, a price shown, a specific number, the headline [ab5eef4de74a] [55e663877849]; Whitman: redundancy (variations of the same message) extends an ad's life [17b39c491ef9] [c38941fe0dbc]. Sources 02, 03, 07. `[print 1920s]` `[DR book 2009]`.

**R116. Change 1 variable per test, and judge on cost per purchase or conversion, not on clicks or opens.** Condition: any test. Hopkins: cost per customer or per dollar of sale decides [2d66d3646e8c] [3607962859be]; Whitman's card: change 1 element at a time [8bb43df5a8b9]; Founders: measure purchase conversion for a sales goal, qualified clicks only if the headline's job is selection [55e663877849]; Tyson: track, change 1 variable, keep 1 method for at least 1 month as a control [07386e6caf36] [6649b7b1fce5]. Sources 01, 02, 03, 07. `[print 1920s]` `[DR book 2009]` `[course seller 2024]`.

**R117. When an ad fails, change the headline first, then check price against the market, then change the offer.** Condition: a launched ad with results. Whitman [d7cbcd4ec542] (the card reverses the order; the book says headline first); Hopkins: a headline change can multiply returns 5 to 10 times [c1863a8437f7]. Sources 02, 03. `[DR book 2009]` `[print 1920s]`.

**R118. Keep a proven winner running. Change it on a measured decline, not on team boredom, and when you change it keep the winning appeal, claim and offer and swap only the execution.** Condition: an ad with results; conflict with fast refresh at scale, 7.10. Hopkins: Mead would not change a word for $10,000; never change a tone that won [2ed6cf037222] [b5c60126fc0a]; Founders: "the way that won millions"; Ogilvy's moving parade [a122da70017c]; Whitman: agreement peaked at 3 exposures and fell at 5 in 1 study, not a cap; use redundancy [17b39c491ef9]; Jamie: brands spending tens to hundreds of thousands a month refresh creative every few days (2019 observation) [f27174953be4]. Sources 02, 03, 05, 07. `[print 1920s]` `[DR book 2009]` `[coaching 2019]`. `[needs brand data: ad-level results over time, frequency, reach]`

**R119. Weight the ad mix by proven pull; keep an appeal that pays even at half the best appeal's returns.** Condition: a brand with keyed results by appeal. Hopkins [fe816803de4e]. Source 03. `[print 1920s]`. `[needs brand data: results by appeal]`

**R120. No source gives a test size, duration or significance rule for copy tests. Size tests from the brand's own volume, or hand the design to 09-CRO.** Condition: any test plan. Only 02 gives a size (500 vs 500 letters) with no success rule [1557d7445b77]; 03 gives 25 letters x 1,000 prospects as a publisher's practice [c47b833d687e]. `[needs brand data: traffic and conversions per variant]`.

**R121. Study the brand's own winners first, then close competitors, each analysed on its own. Ask whether past winners were single-idea and specific.** Condition: before writing a new set for a brand with history. Sandcastles [14df3bb700a0] [fdd73f8bda1d] [ad297d96546e]; Rule of One [491bae29b0be]; Hopkins: record the headline beside every result [c1863a8437f7]. For paid ads, rank by cost per purchase or CTR at matched spend, not raw views; that substitution is not from source 08. Sources 03, 08, 09. `[organic video 2026]` `[DR publishing]` `[print 1920s]`. `[needs brand data: ad-level copy with spend and results]`

**R122. Record every delivered set: the brief, the idea, the angle per variant, the claims and their sources, the cards used, and later the result.** Condition: every job; needed for R118, R119 and R121. Hopkins: key everything [3607962859be]; v1.2 contract step 9. Sources 03.

### Group Q. AI use

**R123. AI drafts, researches and improves lines; it does not author the copy. Write first, lift only lines that beat yours, strip tells, verify every fact and quote it adds, and never let it supply statistics.** Condition: any use of an LLM in the workflow. Tyson [57ebdcf883f4] [5f65d6e25e3c]; Harry Dry [80c71cd2a847] [a359f59b90c4]; Sandcastles [a80ff986fd63] [e9f81c60dc73]. Sources 01, 04, 08. `[course seller 2024]` `[craft 2024]` `[organic video 2026]`.

## 4. Procedures (implementation)

Each procedure: goal, preconditions, steps, checks, rollback. `[verify UI]` where a tool or platform step can change.

### P1. Pre-writing research pack

Goal: 1 document per brand and product that every later procedure reads from. Preconditions: brand record access, reviews or tickets, the product itself or its documents.

1. Compile the brand's material (R10): common sayings, angles, how their posts open, the offer and backend offers, their critique of alternatives, stories with a belief shift, lines that prove they understand the buyer, how people join the list. Source: brand posts, emails, packaging, support replies. [b88d5fdf5214] [243af58d06bd]
2. Mine reviews (R11): read 5-star and 1-star reviews; record exact phrases for the problem, the result, the doubt, and the words used for the product. If the brand has none, use reviews of analogous products and mark them as such. Add support tickets and chat questions. [fb6ca632b8da] [a438dd94bf69] `[needs brand data]`
3. Interview if possible (R11): 12 to 15 one-on-one conversations with buyers surface most pains (06's citation); at least 12 before analysing (06). Highlight surprising and repeated findings; do not use them to confirm assumptions. [0c27d9b3a340] [7a372d0590a0]
4. Build the feature and benefit table (R12): Feature | Unique to us? | Customer pain solved | Benefit | Priority. Every feature, including small ones. For each, react "BIG DEAL, what's in it for me?" and write "You benefit by...". Then ask "what's the benefit of that?" until you reach the end value. Add rows for how the brand does what it does. Cut features with no benefit. Rank high, medium, low. Attach the number behind each benefit. [7f5165a57e7a] [dc660f4f168c] [012ce7b91762]
5. Hunt the keystone fact and the untold process facts (R13): walk the making process or read the product documents; record each step with its number (how often, how many, how deep, how long); ignore "everyone does this". Read technical material nobody wrote for marketing. [48f2e992c7ce] [6959d40e0dc8] [a5c303a75054]
6. Audit competitors (R14): find the top 3 organic and paid results per key phrase; audit at most 10 pages, 5 items each (value proposition, top messages, primary CTA, reasons to buy, standouts); tally messages in a table. Check the Ads Library for long runners `[verify UI: Meta Ad Library URL and filters]`. Record layout and mood only. Never save their text into the compile document. [a3ddc92dd001] [f27174953be4]
7. Find the real rival (R15): is the buyer's alternative another brand, a home-made fix, or doing nothing? Write it down. [6959d40e0dc8] [c78fe9d7b47e]
8. Write the segment and awareness line (R16): who visits most and pays most; which of the 5 stages the traffic is in; how list members joined. [6c4ec380b27a] [3912f9a679c0] [3ce42487fd05]
9. Write a 1-paragraph messaging strategy (06): the principles the copy follows and the tone. [20fa6900506f]
10. Pull past winners and losers with results (R121). Note whether winners were single-idea and specific. `[needs brand data]`

Checks: every benefit row has a number or a fact behind it; the customer-language list has at least 20 phrases; no competitor sentence is copied. Rollback: none; this is a document.

### P2. Choose the buying question and the one big idea

Goal: 1 sentence that says what the reader believes now and what they must believe to buy, and 1 idea the asset is built on. Preconditions: P1.

1. Write the current attitude and the desired attitude (R19). For a store list: "do these work, how, why these". [6645e37e12f9] [68cf28c41359] [8a4864a0a123]
2. List every candidate idea and selling point from the table (R18). [491bae29b0be]
3. Test each: easy to understand? easy to believe? interesting, unique or counterintuitive? Drop any that fails 1 test. [b720ce9767c7]
4. Map the survivors to an appeal (R20): which desire or pain they serve; whether they are cure or prevention (R22); how many buyers in the segment they move (R21). Pick the widest credible one. [5cfd138f2ca5] [91b7cb943a89]
5. Name the contrast (R24): the old way or the category, never a rival by name. [a173f608eaa2]
6. Name the mechanism or difference (R25) and confirm it is true and ownable: could a competitor sign it? [954f8676cb20]
7. Write the idea in 1 sentence. A stranger should be able to say it back.

Checks: the idea passes all 3 tests; the appeal is one the product truly satisfies; the contrast attacks no one. Rollback: return to step 2 with the next candidate.

### P3. Headline bank

Goal: at least 10 headline candidates, ranked, with the 3 strongest marked. Preconditions: P2.

1. Write the main promise in plain words (R26). Write who it selects (R3, R27). [56c0f6af65ab] [c1863a8437f7]
2. Generate: 1 version per Caples quality (self-interest, news, curiosity, quick easy way); versions from the 22 starters that fit; a specific-number version (R28); a time-frame plus outcome plus ease version (01); a contrast version (R38); a feature-led version for spec-comparing buyers (R54). [935888c8c1f1] [db040c273327] [3b6b0416a183] [d5db0dddac4a]
3. Run the 3-question test on each (R60) and the "what is sold?" test (R27). Cut any headline a competitor could sign. [eb5614dd91ba] [0e09cddd6797]
4. Prefer the shorter of 2 equal headlines; flag any over 12 words (R29). [87ab9b6867da]
5. Check every specific against the brand record (R107).
6. Put the top 3 beside the image in the real surface and count 2 seconds (R33, R96). `[verify UI]` [220e0eb8c1d5]
7. Rank and note the angle each carries.

Checks: 10 or more candidates; top 3 carry different angles; no superlatives; all numbers sourced. Rollback: if fewer than 3 survive, go back to P2 step 4 for a different appeal.

### P4. Hooks and first lines

Goal: a first line and a second line for each variant. Preconditions: P3.

1. Write the payoff of the ad in 1 declarative sentence of at most 14 words, ideally 7 to 10 (R36, R37). [f614c8ab3ac7] [38a495e39205]
2. Write the amplifier: a comparison, a contrast or the untold fact (R38). [988a4dabce09]
3. Write 1 question version only if it names the buyer's exact situation (R37). [f0259cdd1faf]
4. Check the promise, intrigue and emotion each line carries; none may be spammy, confusing or clickbait (R35). [ccb66d506164]
5. Check for throat-clearing: greetings, "I hope", "what if I told you", a run-on over 3 lines. Cut (R36). [610c9fac80ba]
6. If the line challenges a common belief, confirm the product can justify it (R41). [930c67d53174]
7. If an LLM is used, run P14 first (R42).

Checks: line 1 makes the reader want line 2; no hedged question; payoff in sentence 1. Rollback: reorder so the best line is first.

### P5. Static ad set (3 variants, 1 variable each)

Goal: 3 finished variants for 1 placement, each with primary text, headline, description if the placement has one, and a CTA, plus internal notes. Preconditions: P1 to P4, the image or video brief, the landing page, current character limits `[verify UI]`.

1. Assign each variant 1 angle before drafting (R115): a different supported benefit, customer moment, objection or execution. Write the angle list first. Do not force a testimonial or comparison when the evidence is missing (v1.2). [fe816803de4e] [ab5eef4de74a]
2. For each variant, pick 1 recognisable situation, 1 relevant feature, and the practical benefit that feature credibly provides (R44). Write that connection, not the component list. [012ce7b91762]
3. Headline: from the bank (P3), matched to the angle. It must read beside the image and say what is sold (R26, R27, R33).
4. Primary text: first line from P4; body in 1 to 3 sentence paragraphs (R49); attention, interest, desire, proof, action (R43); include product identity so it stands alone (R34); 1 specific from the table (R59); proof from the brand record only (R61); a hint of the mechanism (R40).
5. Description (if the placement has one): 1 concrete line for the offer, guarantee or the second benefit (R69).
6. CTA: 1 action, stated positively, matching the page's first screen (R81, R82, R84).
7. Offer, guarantee or deadline lines only from the brand record with eligibility limits intact (R70, R71, R114).
8. Run the editing pass P11 and the claim audit P9.
9. Fit to placement: write to the fetched limits; check what shows before "see more" `[verify UI]`; check the headline on mobile beside the image.
10. Write internal notes: assumptions, missing facts, the variable each variant tests. Do not show drafting instructions in the copy (v1.2).
11. Return the fields the brief asks for (default JSON per v1.2: primary text, headline, description, CTA, internal_notes per variant).

Checks (v1.2's private check): clear product and message; a picturable detail; a relevant buyer concern; a supported benefit; no padding; distinct variants; accurate claims. Revise once if it fails, then deliver (at most 2 passes under the contract). Rollback: if 2 variants collapse into the same angle, replace 1 with the next angle on the list.

### P6. Email copy

Goal: 1 finished email (or each email in a planned sequence) with subject, preview, body, CTA and P.S. Preconditions: P1, P2, the list's join source and the email's single goal.

1. Set the goal: value or sell, in 1 line (R18, R81). Decide the count and role of each email before writing any (05: 10 for a launch, 7 for a welcome, deviate on purpose). [c3c4e6142fe4] [70449eae6ade]
2. Pick the structure (R45): PPAS for a promo (problem 3 to 4 lines, promise 2 to 3, agitate 7 to 8, solution plus CTA about 7; never agitate before the promise); CJN for a belief shift the product can justify; HSO for a story; Jamie's block for anything. [a3f13080cb06] [930c67d53174] [4a2f08fa92d1]
3. Draft without editing. Leave weak lines marked and move on (05). [e20d746ada93]
4. Story rules if used (R46): main character, goal, adversity, turn, lesson at the end, relived not retold, opened on the question the email answers; then a loop back to the reader's next problem before the CTA. [f6de27013260] [ed8a53d10a41]
5. Store list rules (R52, R78): assume product knowledge; answer "do these work, how, why these"; address risk, price, effectiveness. [8a4864a0a123]
6. Subject: at most 40 characters, unambiguous, tied to the angle, no period; move the email's best line into it if it beats the draft (R100, R103). Preview by hand. [0622a180b998] [676688759b08]
7. WIIFM near the top; 1 CTA, optionally repeated once or in a P.S.; deadline emails state time left in digits and double the CTA if the deadline is real (R71, R81). [3afc3ff48150]
8. Length: 200 to 300 words for story and value emails (01); shorter is fine when the email has 1 job. [a81371537582]
9. Emojis: 1 or 2 at most, persona permitting (R90).
10. Run P11 and P9. Goodwill check: has this list had value sends since the last promo? (01's bank rule) [520f11f16e90] `[needs brand data: send history]`

Flow mechanics (welcome cadence, resends to unopens, triple close, revival windows) are 14-EML's. The sources' sketches are in section 6 for reference with their dates.

Checks: 1 idea, 1 CTA, subject matches body, no self-referential opening, reading grade under the floor. Rollback: if the email carries 2 ideas, split it into 2 emails.

### P7. Page section copy

Goal: hero and block copy for a landing or sales page (product page layout is 07-LPG's). Preconditions: P1, P2, awareness stage.

1. Hero: eyebrow (who it is for), headline (promise from P3), deck (ease, time frame or guarantee), 1 CTA. Answer who is this for, why keep reading, what next (R47, R104). [4b264d3e8066] [3e3d5f0de011]
2. Set story depth by stage (R23): more story for stages 2 and 3; short story plus testimonials for stage 4; offer only for stage 5. [3912f9a679c0]
3. Blocks in order (R47): what it is and why it is different; relate to the reader ("right for you if..."); feature plus benefit bullets (P8); testimonials each answering an objection; price positioning with real values (R72); guarantee (R70); urgency only if real (R71); FAQ dropdowns at the bottom (R77). [4f95db866881] [073d27caa4b0] [8ff8c1675824]
4. Place the messages the reader most needs near buttons and images, not in rank order top to bottom (06). [e374cf034894]
5. CTA every 2 or 3 sections; final restated offer or P.S. (R85). [1e562730b6b2]
6. Read only the headers: they must tell the story from problem to offer (R47). [457ab3b6b02d]
7. Scroll-stopper lines: short, bold, where a skimmer lands (R49, R99). [ce4adcb0c5bf]
8. Run P11 and P9.

Checks: headers alone tell the story; every block serves the 1 idea; no product name leads the hero of a long-form page unless the brand is known (R34). Rollback: cut blocks that introduce a second idea.

### P8. Feature to benefit and abstract to concrete

Goal: every feature in copy carries a benefit for this segment, and every vague word is replaced by something the reader can see. Preconditions: the table from P1.

1. For each feature row: "You benefit by..." then "what's the benefit of that?" to the end value (R53). Write the benefit for the segment named in the brief. [dc660f4f168c] [70aaf0b3735c]
2. Decide the lead per audience (R54): benefit lead by default; feature lead when the buyer compares specs or came for 1 feature. Pair whichever leads with the other. [d5db0dddac4a]
3. Zoom in (R55): draw a line, abstract at the top, concrete at the bottom; rewrite the vague phrase 1 step more concrete each time until you reach an object, person, place or action. [8e6c32baa35f]
4. Sensory pass where it fits (R55): what it looks like, sounds like, feels like, smells like, tastes like; skip senses that do not fit the product. [b74a2213dcd8]
5. Only-point rewrite (R59): for each adjective ask "why is it true?" and point at a number, a chart, a process step or a named thing. If nothing can be pointed at, cut the adjective. [d6f95f2facce]
6. Cut any feature that still has no benefit (R57).
7. Check that no benefit became a number the brand record cannot support (R107).

Checks: no adjective without a pointed fact; each line passes visualise and falsify. Rollback: restore the feature to a plain fact if the benefit overreached.

### P9. Claim and compliance audit

Goal: a claim list with a source per claim and a policy check per claim type. Preconditions: the draft, the brand record's approved and banned claim lists, current policy pages `[web check]`.

1. List every claim: numbers, comparisons, outcomes, times, counts, certifications, "free", guarantees, deadlines, quotes, testimonials, "best", "only", "#1". [975c891bc15a]
2. For each, write the source: brand record field, product document, lab result, a testimonial with permission, or a public source the agent opened. No source means cut or rewrite as a plain fact (R65, R107). [19bf368e3817]
3. Verify impressive claims with a document or a test before they run (R108). [6959d40e0dc8]
4. Check policy per claim type (R109): health, weight and body, income, before and after, safety, personal attributes, "free", urgency, comparative. `[web check: Meta advertising standards; local consumer-protection rules]`
5. Testimonials: permission on file, unedited meaning, incentives disclosed as required (R110). `[web check]`
6. Deadlines and stock lines true at send time, with an expiry noted (R111).
7. Competitor mentions: none by name; no copied text; comparison facts verified for both sides (R112).
8. Figurative lines: would a reasonable reader take it as a spec? If yes, rewrite (R113).
9. Guarantee and policy wording matches the record's eligibility limits (R114).
10. Numbers computed (savings, totals, percentages) were computed in code; attach the calculation.

Output: the claim audit table (section 9). Rollback: any claim without a source is removed before delivery; the removal is noted in internal notes.

### P10. Offer, guarantee and deadline lines

Goal: the exact wording for the offer, the risk reversal and any urgency. Preconditions: the brand record's offer terms.

1. Write the offer as 1 line with what, the condition and the scope (R69). [690303793634]
2. Frame it as service: what the buyer gets to try, keep or learn, before any "buy" (R68). [dad9da2fb2e6]
3. Guarantee (R70): term, what qualifies, how to claim, in plain words; show it next to the price and the CTA; the term is the longest operations can honour. [83551014328e] `[needs brand data]`
4. Urgency (R71): only if there is a real date, batch, restock, season or price change; state it in digits; give the reason; repeat the CTA. [8f116e83a3f3] [7181b1222823]
5. Value positioning (R72): a stack with real component prices totalled in code, or a cost comparison against the real alternative; no "priceless" filler, no invented values. [c7a79cc9ee3e] [29770c1882af]
6. Group-limited offer (R73) only for a group the buyer truly belongs to. [652fd908ec22]
7. Trial or sample lines (R74): free on request beats part-price in Hopkins's tests; the sources are silent on first-order percentage codes, so keep the brand's fixed offer as given.

Checks: the offer reads in 1 line; the guarantee matches policy; the deadline has a reason and an expiry. Rollback: remove urgency rather than soften a fake one.

### P11. Editing pass

Goal: a draft that reads aloud clean, carries 1 idea, and meets the reading floor. Preconditions: a complete draft.

1. Rest it: 24 hours if the schedule allows, else at least a walk away (R92). [e76793749fc7]
2. Structure first: 1 idea, 1 CTA; cut anything that is "a whole other email" (R18, R81). [b1fc36d11cab]
3. Tossed salad audit (R95): list claims; flag any not serving the idea; cut or rewrite. [1ee01d6bfef2]
4. Cut the lead; move the best line up; first sentence at most 14 words (R94, R36). [610c9fac80ba]
5. Pronoun pass: flip sentences that start with I, we, our, the brand or the product (R4). [a0589e4916be]
6. 3-question test line by line (R60): visualise, falsify, ownable. [eb5614dd91ba]
7. Modifier sweep (R93): cut very, really, almost, barely, doubled words, repeated sentences, AI tells (R89). [7de71d52b34a] [5f65d6e25e3c]
8. Burrito test per paragraph (R93): pull 1 sentence; if the paragraph still works, the sentence goes. [23276eda58ce]
9. Pacing and skim test (R49, R99): mix line lengths; add a scroll-stopper where the eye should stop; paragraphs of 1 to 3 sentences in ads. [ce4adcb0c5bf]
10. Readability score in code (R97): target Flesch 70 or higher for ads and emails; never above the ecomOS floor. Shorten words and sentences until it passes. [a2f59bfd45f7]
11. Read aloud until no stumble; fix and restart from the top (R92). [e76793749fc7]
12. Subject or headline vs body match (R100). [134e00efad90]
13. In the final surface: line wraps, truncation, image (R101). `[verify UI]` [e93a8cf681bd]
14. Ship bar (R98): if you cannot add or remove a word and make it better, it is done; if you would not rate it 9 of 10, keep cutting. [f98be7ed26de]

Checks: reading grade passes; no stumble; 1 idea. Rollback: keep the previous version; compare 3 versions side by side when a reviewer is available (04).

### P12. Format for placement

Goal: copy that fits the live limits and reads in the slot. Preconditions: fetched limits and a preview tool `[verify UI]`.

1. Fetch the current character limits and truncation points for the placement (R102). `[web check: Meta ad specs]`
2. Put the payoff before the truncation point; nothing important after "see more" unless the reader has already been won.
3. Headline beside the image on a phone: 2-second test (R33).
4. Email: subject at most 40 characters, preview by hand, body left-aligned, images only where they carry the message (R103). `[web check: clipping limit]`
5. Page hero: 3 elements plus 1 CTA (R104).
6. Ad to page: first screen repeats the promise in new words (R105).

Checks: nothing truncated mid-promise; headline legible at phone width. Rollback: shorten by cutting words, never by cutting the specific.

### P13. Variant plan and hand-off record

Goal: a test plan the deployment agent (24-DEP) can run, and a record for later learning. Preconditions: P5 or P6 delivered.

1. State the 1 variable per variant and the constant elements (R116). [8bb43df5a8b9]
2. State the success measure: cost per purchase or purchase conversion; CTR only as a selection check (R1, R116). [55e663877849]
3. If an existing winner is live, keep it as the control; do not replace it on a schedule (R118). [a122da70017c]
4. If the set is a rescue of a failed ad: headline first, then price, then offer (R117). [d7cbcd4ec542]
5. Test size and duration: not given by any source; take them from 09-CRO or the brand's volume (R120). `[needs brand data]`
6. Record (R122): brief, idea, angle per variant, claim audit, cards used, date; add results when they arrive. [3607962859be]

Checks: every variant maps to 1 variable; the control is named. Rollback: none; a record.

### P14. Grounded hook generation with an LLM (adapted from source 08)

Goal: hook candidates grounded in the brand's own winning copy, graded against a written rubric, then chosen by a human. Preconditions: past ads with copy and results. The source shows this on organic creator videos ranked by views; the paid-ad version below is an adaptation, not the source's demo.

1. Gather the brand's own ads with their text and results. Rank by cost per purchase (or CTR at matched spend), not by views or spend (R121). `[needs brand data]` [14df3bb700a0]
2. Split winners from losers at the natural break point in the ranked list; keep the line visible and adjustable. [ad297d96546e]
3. If close competitors' ads are studied, analyse each brand on its own, 1 per run; do not pool them (08's hunch is that pooling dilutes to the average). Record layout and structure only; never save their text as copy (R14). [fdd73f8bda1d]
4. Extract from winners in 4 buckets: psychology, trigger words and framing, grammar, non-obvious patterns; then note what appears in 2 or more sets. [38a495e39205]
5. Write the rubric: the folder's rules (R35 to R42, R59, R64) plus the brand-specific patterns, each tagged to the ad it came from. [e9f81c60dc73]
6. Screen formats for fit with the new topic before generating; reject mismatches rather than force them. [721989c4c0ef]
7. Generate up to 5 candidates per compatible format, reskinned not cloned, plus originals. [721989c4c0ef]
8. Grade each against the rubric; read the line-by-line critique, not only the grade. [e9f81c60dc73]
9. Strip any proof, number, credential or count the model added (R107). [e9f81c60dc73]
10. A human picks and edits for voice; reject high-graded lines that are off-voice or too long. [fdd73f8bda1d]
11. Rerun the rubric only when the data changes (more ads, a new product); reuse it otherwise. [728fcae3dec6]

Checks: every chosen hook passes P4's checks and P9. Rollback: if fewer than 3 formats fit, write hooks by hand from P4.

## 5. Diagnostic checklists

Written so a worker can run each one on a draft and mark pass or fail per line.

### 5.1 Pre-writing research checklist

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Compile document exists | Open it | Sayings, angles, hooks, offer, critique of alternatives, stories, proof lines, list join source | Writing from the brief alone | Run P1 steps 1 to 2 | 01 [b88d5fdf5214] |
| Customer language captured | Count phrases from 5-star and 1-star reviews | 20 or more exact phrases for problem, result, doubt | Writer's own words only | Mine reviews; if none, analogous products | 05 [fb6ca632b8da] [a438dd94bf69] |
| Feature and benefit table | Open the 5-column table | Every feature has a benefit or is cut; how-you-do-it rows present; ranked | Feature list with no benefits, or benefits with no feature | P1 step 4 | 06 [7f5165a57e7a] |
| Numbers behind benefits | Trace each benefit to a fact | A number, count, time or process fact per benefit | "premium", "quality", "better" | Keystone and process hunt (P1 step 5) | 03 [975c891bc15a] 07 [48f2e992c7ce] |
| Untold process facts | Ask "what do we do that we have never said?" | At least 3 process facts with numbers | "Everyone does this" and silence | Walk the process | 07 [48f2e992c7ce] |
| Competitor audit | Table of messages and CTAs, max 10 sites | Baseline and white noise identified; layout notes only | Competitor sentences saved as copy | Delete text; keep structure notes | 06 [a3ddc92dd001] ecomOS |
| Real rival named | 1 line | A habit, an old way or a brand, chosen from data | Assumed "other brands" | Canvass or review data | 03 [6959d40e0dc8] |
| Segment and stage | 1 line each | The segment that visits and pays most; 1 of 5 awareness stages; list join source | "Everyone" | P1 step 8 | 06 [6c4ec380b27a] 05 [3912f9a679c0] |
| Research read for surprises | Highlight pass | Surprising and repeated findings marked | Notes confirm what the team believed | Re-read for new information | 06 [7a372d0590a0] |
| Past winners studied | Copy with results | Winners ranked by cost per purchase; single-idea check done | No look at history | P14 steps 1 to 4 | 08 [14df3bb700a0] 09 [491bae29b0be] |
| Voice samples in hand | Count | 5 or more approved samples | None | Use provisional tone and say so | 01 [3f95809c1b82] v1.2 |

### 5.2 Headline review

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Main promise present | Underline the benefit | The reader's gain is in the line | Company news, cute line, question with no promise | Rewrite from the top benefit | 02 [56c0f6af65ab] 07 [e2b526314c8d] |
| Selects the audience | Ask who it is for | The target buyer would know it is for them | Could be for anything ("Brighten up your life") | Add the buyer or the need | 03 [c1863a8437f7] 02 [0e09cddd6797] |
| What is sold | Show the headline alone | Reader names the product type and benefit | A pun or riddle | Rewrite with product, benefit, for whom | 02 [0e09cddd6797] |
| Specific | Circle numbers and names | A true number, time, count or name | "Best", "fast", "quality" | Replace with a checked fact | 03 [975c891bc15a] 04 [d6f95f2facce] |
| Visualise, falsify, own | 3 questions | 3 yes | 3 no | Zoom in; point; find a brand-only fact | 04 [eb5614dd91ba] |
| Length | Count words | 12 or fewer, or every word earns its place | Over 12 with filler | Cut filler, keep the specific | 02 [87ab9b6867da] |
| Truthful | Compare with brand record | Every claim sourced | Inferred count, invented ease or time | Cut or source | ecomOS; v1.2 |
| Curiosity with payoff | Read headline then body | The body pays the curiosity off for the right buyer | Mystery that pulls the wrong reader | Add targeting or drop the tease | 02 [935888c8c1f1] 01 [ccb66d506164] |
| Reads beside the image | Mock it up on a phone | Understood in 2 seconds | Needs the body to make sense | Rewrite or change the image brief | 04 [220e0eb8c1d5] v1.2 |
| Distinct across variants | Compare the 3 | 3 different angles | Synonym swaps | Reassign angles | v1.2; 03 [fe816803de4e] |
| Not a competitor's line | Paste on a rival page | It becomes false for them | Still true for them | Find the brand-only fact | 04 [954f8676cb20] |
| Policy | Check claim type | No income, health, body or before-and-after claim without policy check | Any of those unchecked | P9 step 4 | 01 [f90f84d09846] `[web check]` |

### 5.3 Full ad copy review (static ad)

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| 1 idea | Say the argument in 1 sentence | A stranger can | 2 or more ideas | Tossed salad audit | 09 [1ee01d6bfef2] |
| Angle | Name the situation, feature and benefit | 1 of each, connected | Component list | Rewrite from the table | v1.2; 02 [012ce7b91762] |
| First line | Count words; look for throat-clearing | 14 words or fewer, payoff first | Greeting, "I hope", run-on | Cut the lead | 01 [f614c8ab3ac7] 08 [38a495e39205] |
| Second line amplifies | Read lines 1 and 2 | Contrast, comparison or the untold fact | Restates line 1 | Add the amplifier | 08 [38a495e39205] 04 [988a4dabce09] |
| Reader first | Scan sentence starts | "You" or the situation leads | I, we, our, brand, product | Flip syntax | 05 [a0589e4916be] |
| Salesman test | Read each line as said to 1 buyer | Every line helps a half-sold buyer | Cleverness, boast, decoration | Cut | 03 [6ebd6afa8fcc] 07 [250834566833] |
| Boast and selfish phrases | Scan | None | "We're the best", "insist on", "avoid imitations" | Turn into a buyer benefit or cut | 07 [39699efcd305] |
| Specific and picturable | Circle adjectives | Each replaced by a fact or object | Adjective trail | Only-point rewrite | 04 [d6f95f2facce] 02 [4366c3a8be93] |
| Proof present and sourced | List proof lines | Demonstration, testimonial with permission, or a brand-record fact | Bare claim, "studies show", model-written proof | Add sourced proof or cut | 02 [a9db8de6d903] 01 [792856b9a23c] ecomOS |
| Claim size | Would a buyer believe it? | Small and specific | "Life-changing", income or miracle claims | Shrink; add examples | 04 [bf82611ee658] 06 [6b829c0c6b03] |
| Frame | Positive or negative? | Positive result shown, or a negative the product fully removes | Vivid negative with the brand beside it; fear with no fix | Rewrite positive or hint | 03 [650b052b209a] 06 [2c6f4cda6b12] 02 [23a92b334a3e] |
| Mechanism hint | Is there a why? | 1 line on how it works | "Click to find out" with nothing | Add the hint | 01 [0cf0f5e70b0b] |
| Offer line | Read the offer | 1 concrete line: what, condition, scope | Vague amount or condition | Rewrite | 06 [690303793634] |
| Urgency | Is it real? | Real date or limit with a reason, or none | Evergreen countdown, "selling fast" with no fact | Remove | 01 [8f116e83a3f3] 02 [61bd1ae6936b] |
| CTA | Count asks | 1 action, positive, labelled with what happens | Several asks; "Start now" with no context | Cut to 1; label | 01 [b1fc36d11cab] 02 [d8e25cc5a2b0] |
| Page match | Click through | First screen repeats the promise | Home page or unrelated page | Change the destination or the copy | 05 [dda3430eb956] |
| Product identity | Cover the image | The ad still says what the product is | Could be any product | Add the identity | v1.2; 02 [0e09cddd6797] |
| Paragraphs | Count sentences | 1 to 3 per paragraph | Blocks | Break | 05 [36b9e7b8a840] |
| Reading grade | Score in code | Flesch 70 or higher; below the ecomOS floor | Above the floor | Shorten words and sentences | 02 [a2f59bfd45f7] ecomOS |
| Voice | Compare with samples | Matches the brand's phrases and persona | Hype in a calm brand; emojis for a serious persona | Use compile phrases | 01 [3f95809c1b82] |
| AI tells | Scan the list | None | "Revolutionize", "don't miss out", double dash | Cut | 01 [5f65d6e25e3c] |
| Fits placement | Preview `[verify UI]` | Payoff before truncation; headline legible on phone | Cut mid-promise | Shorten by cutting filler | R102 |
| Variants distinct | Compare 3 | 3 angles, 1 variable each | Synonyms | Reassign | v1.2 |
| Internal notes | Read | Assumptions and missing facts listed; no drafting text in copy | Planning text in the copy | Move to notes | v1.2 |

### 5.4 Email copy review

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| 1 goal | Read the goal line | Value or sell, with a specific action | Both, or several | Split | 05 [c3c4e6142fe4] |
| Structure chosen | Name it | PPAS, CJN, HSO or the outline block | Freeform | Rebuild on a structure | 01 [f95389e976bd] |
| PPAS order | Check the order | Problem, promise, agitate, solution | Agitate before the promise | Reorder | 01 [a3f13080cb06] |
| Subject | Count characters; read for ambiguity; check punctuation | 40 or fewer; tied to the angle; no period | Ambiguous, gives the email away, or over 40 | Rewrite; move the best line up | 01 [0622a180b998] [134e00efad90] 05 [676688759b08] |
| Preview | Check it is set | Written by hand, adds to the subject | Auto-filled | Write it | 05 [c3c4e6142fe4] |
| Lead | Count words in sentence 1 | 14 or fewer, ideally 7 to 10 | Greeting, "I hope", "what if I told you" | Cut | 01 [f614c8ab3ac7] |
| No reference back to subject | Scan body | None | "As I said in the subject" | Cut | 01 [134e00efad90] |
| WIIFM near top | Find it | Specific benefit in the first lines | Founder biography first | Add the WIIFM line | 01 [51f77f32f63c] |
| Reader first | Sentence starts | "You" leads | I, we, our | Flip | 05 [a0589e4916be] |
| Story test | If a story: goal, adversity, turn, lesson at end | All 4, relived | Timeline of numbers; lesson at the start | Rebuild the story | 01 [f6de27013260] |
| Show vs tell | Each results claim | First person demonstration or named customer, with proof | "You can lose 20 lb" | Rewrite as shown conviction | 01 [e9741d568a97] |
| Store list fit | Does it explain what the product is? | Assumes knowledge; answers work, how, why these | "What is X" opener to buyers | Rewrite | 01 [8a4864a0a123] |
| 3 blockers | Look for risk, price, effectiveness | Each addressed where relevant | Only a discount | Add mechanism and risk reversal | 01 [8a4864a0a123] |
| One idea, one CTA | Count | 1 idea; 1 CTA, repeated at most once or in a P.S. | Several asks; too much objection handling | Cut; move to another email | 01 [b1fc36d11cab] |
| Deadline email | If a deadline: is it real? time left in digits? CTA doubled? | Yes to all | Fake or vague deadline | Remove or fix | 01 [3afc3ff48150] [8f116e83a3f3] |
| Goodwill balance | Send history | Value sends since the last promo | Promo after promo | Add value emails first | 01 [520f11f16e90] `[needs brand data]` |
| Length | Word count | 200 to 300 for story or value emails; shorter if 1 job | 800 words of 3 ideas | Cut to 1 idea | 01 [a81371537582] |
| Pacing | Skim | Mixed line lengths, scroll-stopper lines | Wall of long lines or all one-liners | Add or merge lines | 01 [ce4adcb0c5bf] |
| Emojis | Count | 0 to 2, persona permitting | Many, or any in a serious persona | Cut | 01 [d65a7b03c6a3] |
| Format | Template and images | Text-led; images only where they carry the message | Heavy template with big images | Strip; see 7.11 for store grids | 05 [2bcad09a68e8] |
| Read aloud | After a rest | No stumble | Any trip | Fix, restart | 05 [e76793749fc7] |
| Claims | P9 | All sourced | Any unsourced | Cut | ecomOS |

### 5.5 Claim and compliance check

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Claim list complete | Extract every number, comparison, outcome, quote, guarantee, deadline | Nothing missed | A number in the copy not on the list | Re-extract | 03 [975c891bc15a] |
| Source per claim | Column filled | Brand record field, document, permitted testimonial, or a source the agent opened | "Google", "AI", "commonly known", a competitor's site | Cut or rewrite as plain fact | 06 [19bf368e3817] ecomOS |
| Impressive claims verified | Document or test on file | Yes | Owner's long-held belief | Verify or remove | 03 [6959d40e0dc8] |
| Inferred counts | Check kit or category counts | Exact count from the record | Pieces inferred from a set name | Remove the number | v1.2 |
| Invented ease, time, tools, compatibility | Scan | None, or from the record | "Sets up in 5 minutes" with no source | Cut | v1.2 |
| Reviews and counts | Scan "5-star", "10,000 customers" | From the data layer | Round-number guesses | Cut or source | ecomOS |
| Statistics | Scan "% of", "studies" | Only from a checked source in the record | From 01's "stats from Google" or an LLM | Cut | ecomOS overrides 01 [574fd7aa2de4] |
| Policy by claim type | Check current standards | Health, body, income, before-and-after, safety, personal attributes, "free", urgency, comparative each checked | Any unchecked | `[web check: Meta advertising standards]` | 01 [f90f84d09846] 02 [23a92b334a3e] |
| Testimonials | Permission file; meaning unchanged; incentive disclosed | All 3 | Any missing | Remove until fixed | 02 [5ae1f82d7e99] `[web check]` |
| Urgency | True at send time; expiry noted | Yes | Evergreen or vague | Remove | 02 [61bd1ae6936b] 01 [8f116e83a3f3] |
| Guarantee wording | Compare with policy | Term, eligibility and claim path match the record | Broader than the policy | Match the record | 02 [83551014328e] v1.2 |
| Comparative claims | Named rivals? Copied text? | None; charts with verified facts both sides | Named attack or borrowed sentence | Cut | 03 [650b052b209a] ecomOS |
| Figurative lines | Reasonable-reader test | Not readable as a spec or outcome | "1,000 X in your pocket" style on a real number | Rewrite | 04 [fc16ebab7e1b] |
| Arithmetic | Calculation attached | Computed in code | Mental math in copy | Recompute | ecomOS; 04's 22,000 error [bf82611ee658] |
| Client-page words | Scan | No mention of GPT or .env | Present | Cut | ecomOS |

### 5.6 Editing pass checklist

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Rested | Time since draft | 24 hours, or at least a walk | Edited the same minute | Wait | 05 [e76793749fc7] 04 [f98be7ed26de] |
| Read aloud | Whole piece | No stumble | Any trip | Fix, restart from the top | 05 [e76793749fc7] 01 [28321b2f379b] |
| Tossed salad | Claim list | All sub-points of 1 idea | Divergent claims | Cut or rewrite | 09 [1ee01d6bfef2] |
| 3 questions per line | Visualise, falsify, own | 3 yes | 3 no | Rewrite | 04 [eb5614dd91ba] |
| Lead cut | First 4 lines | Say something; best line first | Wind-up | Cut; move | 01 [610c9fac80ba] |
| Modifiers | Scan very, really, almost, barely | None; numbers instead | Present | Cut or replace | 01 [7de71d52b34a] |
| Doubles and repeats | Scan | None | "SMMA agency", repeated sentences | Cut | 01 [7de71d52b34a] |
| AI tells | Scan the list | None | Present | Cut | 01 [5f65d6e25e3c] |
| Burrito test | Pull 1 sentence per paragraph | Paragraph breaks | Still works | Cut the sentence | 04 [23276eda58ce] |
| Paragraph length | Count | 2 lines (04) or 4 to 5 short sentences (02); 1 to 3 sentences in ads (05) | Blocks | Break or cut | 04 [23276eda58ce] 02 [d2d7d23b7635] |
| Pronouns | Sentence starts | Reader leads | Writer leads | Flip | 05 [a0589e4916be] 02 [210eb332ef8f] |
| Readability | Score in code | Flesch 70 or higher; under the ecomOS floor | Lower | Shorten | 02 [a2f59bfd45f7] |
| Skim | Scroll without reading | Offer rebuilds from bold lines | Wall or all one-liners | Add stoppers; vary | 01 [ce4adcb0c5bf] |
| Subject or headline match | Compare with body | Same angle | Mismatch | Rewrite from the body's angle | 01 [134e00efad90] |
| Surface check | Preview in the tool | Wraps and truncation as intended | Line runs to 3 or 4 lines | Cut words | 04 [e93a8cf681bd] `[verify UI]` |
| Versions and feedback | Count versions; time on task | 3 shown to a reviewer; outside eyes after 2 to 3 hours | 1 version, 6 hours alone | Get feedback | 04 [189a7e6d8231] [6914df3c2bd8] |
| Done test | Add or remove a word | Nothing improves it; 9 of 10 | Words can go | Keep cutting | 04 [f98be7ed26de] |

## 6. Thresholds and benchmarks

One table for the folder. Confidence: how many mini playbooks state or support the value, and the evidence type. Dated values are marked. None is a promise; case results are examples.

| Value | Condition | Source | Confidence |
|---|---|---|---|
| Headline change swings returns 5 to 10 times | Same body, different headline, keyed print ads | 03 [c1863a8437f7], 07 [55e663877849] | 2 sources, both Hopkins, no data shown; `[print 1920s]` |
| Headline spread 19 to 1 | Ogilvy, as recalled by the host | 07 [55e663877849] | 1 source, recollection |
| 1 word changed in a headline gave up to 25% more conversions | Presenter's experience | 05 [f27d97c52312] | 1 source, anecdote |
| Nearly 2,000 headlines keyed on 1 product | Hopkins's records | 03 [c1863a8437f7] | 1 source |
| One claim vs another in the headline: up to 10 times results | Tested claims | 03 [91b7cb943a89] | 1 source, "proved by many disappointments" |
| 60% of readers read only the headline | Print ads | 02 [56c0f6af65ab] | 1 source, uncited `[web check]` |
| "80 or 90%" read the headline | Host's paraphrase of Ogilvy | 07 [e2b526314c8d] | 1 source `[web check]` |
| Longer headlines are read less fully; keep the headline short for a cold feed (operational takeaway; see also the row below and R29) | Word count | 02 [87ab9b6867da] | Moved to Appendix A: Rudolph 1939 to 1940 percentage breakdown |
| Drop above 12 words | Same study | 02 [87ab9b6867da] | 1 source |
| Headline in quotes "boosts reading 25%" | Checklist | 02 [037f584ed120] | 1 source, uncited; do not quote |
| ALL CAPS sparingly, at most 4 to 5 words (print packaging and inserts only, see R33 and section 11) | Print | 02 [388f0c750aad] [14dcce0a0c2a] | Moved to Appendix A: Paterson and Tinker 1956 all-caps reading-speed study |
| First sentence at most 14 words, ideally 7 to 10 | Email lead | 01 [f614c8ab3ac7] [0666118ff844] | 1 source, heuristic |
| Opening paragraph at most 11 words | Body copy | 02 [d2d7d23b7635] | 1 source, Ogilvy quote; agrees in spirit with 01 |
| About 11 words per sentence; 70% to 80% one-syllable words; 14 people references per 100 words | Body copy | 02 [d2d7d23b7635] [210eb332ef8f] | 1 source, Flesch |
| Flesch grade map: 90 to 100 5th grade; 80 to 90 6th; 70 to 80 7th; 60 to 70 8th to 9th; 50 to 60 10th to 12th; 30 to 50 college | English copy | 02 [a2f59bfd45f7] | 1 source, Flesch standard |
| Reading level: third grade or below | All copy | 01 [495714e45312] | 1 source, opinion; 02, 04, 05 agree "simple" without a grade |
| ecomOS floor: below tenth grade | All copy | ecomOS | Project rule |
| Paragraphs: 2 lines or fewer | Newsletters | 04 [23276eda58ce] | 1 source, "idiosyncratic" |
| Paragraphs: about 4 to 5 short sentences | Body copy | 02 [d2d7d23b7635] | 1 source |
| Ad paragraphs: 1 sentence; 1 to 3 at most | Social ads | 05 [36b9e7b8a840] | 1 source, 2019 observation |
| Bold lesson line about 7 to 8 words | Emails | 01 [0666118ff844] | 1 source, heuristic |
| Subject line 40 characters or fewer | Emails | 01 [0622a180b998] | 1 source, heuristic |
| No period at the end of a subject line | Emails | 05 [676688759b08] | 1 source, opinion |
| Story and value emails 200 to 300 words | Emails | 01 [a81371537582] | 1 source, practice norm from info products |
| PPAS proportions: problem 3 to 4 lines, promise 2 to 3, agitate 7 to 8, solution about 7 | Promo email | 01 [a3f13080cb06] | 1 source, heuristic |
| Emojis 1 to 2 per email | Emails | 01 [d65a7b03c6a3] | 1 source, opinion |
| Plain benefit emails about 80% of sends | An info-product list | 01 [99d753c33b55] | 1 source, own practice |
| Show rather than tell "90% of the time" | Results claims | 01 [e9741d568a97] | 1 source, heuristic |
| Write for 20% to 35% of visitors | Headlines and key pages | 06 [52564e4cb23c] | 1 source, heuristic |
| 12 to 15 interviews surface about 80% of pains | Segment research | 06 [0c27d9b3a340] | 1 source citing 1 book (Pain Killer Marketing, 2008) |
| At least 12 people surveyed before analysing | Segment research | 06 [7a372d0590a0] | 1 source, rule of thumb |
| Competitor audit: max 10 sites, 5 items each, top 3 results per phrase | Content audit | 06 [a3ddc92dd001] | 1 source, method |
| 91 of the top 100 offers centred on 1 idea | Masterson's review at 1 publisher | 09 [491bae29b0be] | 1 source, second hand |
| Small claim example: 1% to 2% conversion, "twice as many" | Harry Dry's course ad | 04 [bf82611ee658] | 1 source, positioning choice |
| 3-question test: 3 yes or 3 no | Every line | 04 [eb5614dd91ba] | 1 source, craft rule |
| 2-second comprehension | Glance contexts | 04 [220e0eb8c1d5] | 1 source, heuristic |
| About 25 rewrites over 2 days for 1 static ad | Harry Dry's own ad | 04 [6e39a617d9e1] | 1 source, own process |
| Lose judgement after 2 to 3 hours on 1 ad; then get outside feedback | Writing | 04 [6914df3c2bd8] | 1 source, experience |
| 4 to 5 versions of a line; show 3 to a reviewer | Editing | 04 [189a7e6d8231] | 1 source, habit |
| Ship bar 9 of 10 | All work | 04 [f98be7ed26de] | 1 source, standard |
| Review 3 pieces for every 1 you submit | Skill building | 01 [7fd437ffe114] | 1 source |
| Draft rest 24 hours | Before editing | 05 [e76793749fc7] | 1 source; 01 says overnight |
| Overwrite 2x (2,000 words for 1,000; 10x the information) | Drafting | 06 [753e79e5c3d8] | 1 source plus Caples quote |
| Positive outpulls negative 4 to 1 | Keyed print tests | 03 [650b052b209a] | 1 source, "if you have our experience"; 06 disputes a general rule |
| Repetition builds agreement; more exposure is not a guaranteed cap or floor (see R118) | Exposure count | 02 [17b39c491ef9] | Moved to Appendix A: Petty and Cacioppo 1979 college-student study |
| Reach cut on disliked ads in 24 to 48 hours; creative refresh every few days | Brands spending tens to hundreds of thousands a month, 2019 | 05 [f27174953be4] | 1 source, observation, dated `[web check]` |
| Ads Library check once a week or twice a month | Competitor watch | 05 [f27174953be4] | 1 source, practice |
| Screen out videos under about 2% engagement as paid | Organic creator channels | 08 [03d175f0d156] | 1 source, rule of thumb; no meaning for paid ads |
| Winner break point after video 4 or 5 of 10; ideal run about 100 own videos | Organic hook analysis | 08 [ad297d96546e] [14df3bb700a0] | 1 source, 1 demo |
| Episode branding without an outcome "sinks 50%"; audio-clip openers underperform "about 60%" | 1 channel each, 10 videos | 08 [38a495e39205] [cfa4e7c04581] | 1 source, model output, hypothesis |
| Long guarantee (6 months to lifetime) beats 30, 60, 90 days for sales and returns | Products | 02 [83551014328e] | 1 source, "studies show", uncited `[web check]` |
| Installments over $15 add 15% response; "Bill Me" adds 50% or more | Direct response | 02 [3d848b082e13] | 1 source, uncited; do not quote |
| BOGO beats 50% off | Offer framing | 02 [d7cbcd4ec542] | 1 source, "testing showed", no data `[web check]` |
| Moved to Appendix A: Fidelity bank-fee rewrite case (R69) | 1 offer rewrite | 06 [690303793634] | see appendix |
| Pay-in-a-week beat money-back "many times"; dealer's signed warrant "made a fortune" | 1920s mail order | 03 [652fd908ec22] [abac911ba2b0] | 1 source, cases |
| Free sample on request; charging a dime costs 40 cents to $1 more per reply; 3 in 4 refuse to pay before conversion | 1920s | 03 [0e72ef7fa48e] | 1 source, cases |
| Store pickup 4 times the mail response; 18 to 22 cents vs 70 cents per inquiry | 1920s | 03 [aa1335efee33] | 1 source, 1 line |
| Deadline email: "only 48 hours left", double CTA | Launch close | 01 [3afc3ff48150] | 1 source, example |
| Triple close: 3 sales emails on the last day; final day equalled all prior emails; third email added 15% to 25% of launch revenue | Info-product launches | 05 [8046e8352c3b] [8ccd32a8db57] | 1 source, anecdote; unsubscribes not measured; flow design is 14-EML's |
| "Introducing" email opens about 15% vs a normal 25% to 30% | Info-product lists, about 2019 | 05 [2ac1adf98a07] | 1 source, dated (pre Apple MPP) `[web check]` |
| "you up" subject about 32% opens on a 600,000 list | Late-night close, 2019 | 05 [ae22f03a0868] | 1 source, dated |
| Launch: 10 emails; welcome: 7 daily emails | Defaults | 05 [2ac1adf98a07] [dfb61fe7d4a8] | 1 source; 01 says 3, 5 or 8 welcome emails all work [e326516d4bdb]; flow design is 14-EML's |
| Revival trigger at 30 to 60 days of no opens | List hygiene | 01 [5e43074e0a7e] | 1 source, dated; opens unreliable since Apple MPP `[web check]` |
| Email vs social: 15% to 25% opens vs 2% to 4% reach; ROI $36, $42 or $44 per $1; "40 times" acquisition | Channel argument | 01 [fbb591f5fa80] [e8ba196b022f] | 1 source, inconsistent, undated third-party figures `[web check]`; do not quote to clients |
| Average email: 21.5% open, 2.5% click | Unnamed source | 01 | 1 source, no card, dated `[web check]` |
| 69% average open rate for opt-in B2B e-zines; HTML 200% better; 60% could receive HTML | Early 2000s | 02 [5861e7fcfc77] | 1 source, obsolete; do not use |
| Email clipping "about 2 MB" | Image-heavy HTML | 05 [2bcad09a68e8] | 1 source, guess `[web check: Gmail clip limit, usually cited as about 102 KB of HTML]` |
| Test size for a letter or mailer: 500 vs 500; 25 letters x 1,000 before 5 million | Direct mail | 02 [1557d7445b77], 03 [c47b833d687e] | 2 sources, no success rule; not a copy-test standard |
| Keep 1 method at least 1 month as a control | Any tracked process | 01 [07386e6caf36] | 1 source, opinion |
| Meta character limits and truncation points | Primary text, headline, description | None | No source; `[verify UI]` `[web check]` |

## 7. Where sources disagree

Each conflict: what each side says, when each is right, what the agent should do.

**7.1 Long copy vs short copy.** Hopkins: "the more you tell the more you sell", brief ads are never keyed, some winning ads ran 15,000 words [8946e9e66b01] [84d9f8424c4b]. Whitman: long outsells short "no qualifications, no disclaimers", with Sackheim's condition that short copy is for when there is little to say [bef86f46c5c6]. Copy Hackers: fact-packed messages work if interesting; write 2,000 then cut [753e79e5c3d8]. Against: Tyson's "TikTok brain", value per minute, 200 to 300 word emails [d65a7b03c6a3] [a81371537582]; Harry Dry's "shorter is better most of the time" and 2-line paragraphs [8e6c32baa35f] [23276eda58ce]; Jamie's 1 to 3 sentence paragraphs in ads [36b9e7b8a840]. When each is right: the long-copy evidence is from readers who chose to read a print ad or a page; the short-copy advice is for a cold feed and a phone. What the agent should do: in a feed ad, put the whole argument for the target buyer before the truncation point and let the page carry the complete story; on the page and in emails to interested readers, include every proven claim needed to decide (R48) and cut everything else (R93). Never pad to be long; never cut a claim to be short. Test length as a variable only with brand data `[needs brand data: results by copy length]`.

**7.2 Lead with the benefit vs not always.** Whitman: biggest benefit in the headline "always, without exception" [56c0f6af65ab]; Hopkins and Founders: the main promise in the headline [c1863a8437f7] [e2b526314c8d]. Copy Hackers: no fixed rule; a feature headline beat a benefit headline; spec-comparing and benefit-distrusting shoppers do not want a benefit lead [d5db0dddac4a]. When each is right: benefit lead for problem-aware and solution-aware traffic; feature or specific lead for product-aware buyers who compare, and for categories where soft language reads as hype. What the agent should do: default to the benefit lead (4 sources); write 1 feature-led variant when the brief says the buyer compares specs; always pair the lead with its other half (R54).

**7.3 One CTA vs many.** Tyson: 1 CTA, confusion kills action, double CTA or P.S. allowed [b1fc36d11cab]; Jamie: 1 function per asset [c3c4e6142fe4]; Whitman: 1 product at a time, except catalogue-style sellers [388f0c750aad]. Against: Tyson himself notes typical store emails are "20% off plus a product picture" with several links, and Jamie's Head Candy welcome email has a coupon plus a 3-column product grid with 3 buy links [60d5057bb3c2]. When each is right: 1 ask for any persuasive email or ad; a grid is fine when the email's single job is "shop the range" and every link serves that one job. What the agent should do: 1 kind of action per asset; a product grid counts as 1 action ("shop") only if the email has no other ask; never mix "read this", "follow us" and "buy" in one send.

**7.4 Product name in the hero vs not.** Jamie: no product name in the sales page hero unless the brand is Mercedes or Apple [8ff8c1675824]. v1.2 and Whitman: the ad must carry enough product identity to stand alone and pass "what is sold?" [0e09cddd6797]. Common product page practice makes the product name the H1 (not from a source). When each is right: Jamie's rule is for long-form sales pages and advertorials to cold traffic; ads and product pages need identity. What the agent should do: ads and product pages name the product; long-form landing pages lead with the reader's problem or goal and name the product after the promise; the brief decides which page type it is.

**7.5 Negative framing.** Hopkins: positive outpulled negative 4 to 1; before and after are follies; show the face as it will appear [650b052b209a]. Founders: never picture the afflicted; reward not prevention [6111749e4303]. v1.2: avoid fear. Copy Hackers: negative is not banned; people attend to "don't"; winners exist on both sides; do not attach the brand to a heavy negative picture; rewrite negative copy only if it converts poorly [19bf368e3817] [2c6f4cda6b12]. Whitman: fear works with all 4 parts and a product that truly resolves it [23a92b334a3e]. Tyson: PPAS agitates after the promise [a3f13080cb06]. When each is right: positive for cold ads and beauty, food, comfort categories; negative or problem-led when the buyer is already in pain and the product removes it fully. What the agent should do: positive by default; a problem-led variant is allowed as 1 of 3 when the product fully solves the problem, the frame is clear, and the brand is not placed inside the negative scene; no fear without a specific fix and proof; no before-and-after bodies or afflicted faces without a policy check `[web check]`.

**7.6 Small claims vs bold hooks.** Harry Dry: small believable claims ("1% to 2%") [bf82611ee658]; Copy Hackers: nearly unbelievable is fine with examples, impossible never [6b829c0c6b03]; Tyson: attainable and hyper-specific promises, proof over promise [017ae2c141f9]. Against: Whitman's headline rewrites ("Boost your tips by 512%... or your money back") and Tyson's own VSL examples ("$20,000 a month extra") model big claims [56c0f6af65ab] [6194d941ef49]. When each is right: a bold claim only when it is true, specific and backed on the same surface. What the agent should do: the claim size is set by the brand record, not by the hook's appetite; write the biggest claim the record supports and no bigger; add the example or proof beside any claim a stranger would doubt.

**7.7 Deadline on every ad.** Whitman: "always feature deadlines", most of the time one is appropriate [7181b1222823]. Hopkins: pay for prompt action; many successful letters expire on a date [e48273314166]. Tyson: only situational urgency; non-situational tactics only in promotions and sparingly; fake scarcity on infinite goods is absurd [8f116e83a3f3]. Whitman's own card: the limit must be real; fake countdowns can break consumer law [61bd1ae6936b]. When each is right: a real sale, batch, restock or season justifies a deadline; an evergreen ad has none. What the agent should do: no deadline unless the brand record has a real one; when it exists, state it in digits with its reason and repeat the CTA; never write "selling fast" or "limited" without a fact.

**7.8 Question vs declarative openers.** Sandcastles' model finding: winners say things, losers ask questions (3 organic creator channels, 1 run) [38a495e39205]. Whitman: rhetorical-question research is split; Gayle, Preiss and Allen 1998 found no appreciable persuasion effect; questions may help memory; yet his letter method opens with "Do you want...?" [ecc5de375921] [6d882bfcd851]. Tyson: replace throat-clearing with a perplexing question [f0259cdd1faf]; his HSO hook example is a question. When each is right: a question earns its place when it names the buyer's exact situation and cannot be answered "no" by the target; a hedged or generic question ("Want to save money?") is weaker than a declarative payoff. What the agent should do: default to a declarative first line for cold feed hooks; allow 1 question variant that names the situation precisely; never a hedged question; test on brand data `[needs brand data]`.

**7.9 One big idea vs the complete story.** Rule of One: 1 idea, everything else a sub-point; tossed salad copy weakens [491bae29b0be]; Tyson: 1 idea per email; Harry Dry: "and" is a red flag [867743b221ba]. Hopkins: tell a reasonably complete story; include every proven claim in every ad; no serials [8946e9e66b01]; Whitman: pile on benefits, restate from many angles [bef86f46c5c6]. When each is right: these agree more than they clash. The idea is 1; the claims that support it can be many. Hopkins's "all claims" refers to claims for 1 product to 1 buyer, not different ideas. What the agent should do: 1 idea per asset, chosen in P2; include every proven claim that serves that idea and the buyer's decision (more on a page, fewer in a feed ad); cut claims that pull toward a second idea; if a second idea is strong, it becomes a second variant, not a second paragraph.

**7.10 Refresh winners vs keep them.** Hopkins: Mead would not change a word for $10,000; never change a proven tone [2ed6cf037222] [b5c60126fc0a]; Founders: keep the ad that works, the moving parade [a122da70017c]; Whitman: repetition builds familiarity; use redundancy (variations) rather than stopping; the 3-exposure study is not a cap [17b39c491ef9]. Jamie: big spenders refresh creative every few days because reach on a disliked ad is cut in 24 to 48 hours (2019) [f27174953be4]. When each is right: Hopkins wrote for a stream of new readers who had not seen the ad; a small retargeting audience does tire. What the agent should do: keep a winner running until its own numbers decline; when they do, keep the appeal, claim and offer and change the execution (image, format, first line); plan new angles as additions, not replacements. Frequency and fatigue reads belong to 24-DEP `[needs brand data: results over time, frequency]`.

**7.11 Text-only emails vs store emails.** Jamie: all launch emails plain text; HTML templates land in Promotions and clip [2bcad09a68e8]; yet her own store welcome email 1 is a coupon plus a 3-column product image grid [60d5057bb3c2]. Tyson: typical store emails are a picture plus a discount, and he wants structured value emails instead [8a4864a0a123]. Whitman's HTML data is early 2000s and obsolete [5861e7fcfc77]. When each is right: text-led for story, belief-shift and launch emails; image-led when the product must be seen (a range, a colourway, a tutorial). What the agent should do: write every email so the words carry the message with images off; add images only where they carry meaning; the format decision and deliverability checks belong to 14-EML `[web check: current Gmail clipping and Promotions behaviour]`.

**7.12 Free trial vs paid trial vs discount code.** Hopkins: free sample on request beats part-price; a free full-size package handed out failed and a maker-paid retail coupon won; pay-later beat money-back [0e72ef7fa48e] [dad9da2fb2e6] [652fd908ec22]. Founders: never sample people who did not ask [04185b470730]; the host's Estee Lauder story praises unrequested sampling. Tyson and Jamie describe 10% off or "10 off" for an email as standard store practice [58af3dd961fe] [60d5057bb3c2]. When each is right: Hopkins's cases are 1920s foods and proprietaries; no source tests a modern first-order code. What the agent should do: word the brand's existing offer as given (03-OFF owns offer design); frame any trial as requested and earned rather than pushed; do not write "half price to try it" as if it were proven; keep this as an open question for the brand's own tests.

**7.13 Who writes: the maker or a writer, and the founder as the face.** Hopkins: no manufacturer should conduct his own advertising [ea531107827e]; Founders host: the founder should go direct and front the selling; Hopkins used a persona with a real person behind it [762657ec71d8]. Whitman: put your face on everything (service and founder brands) [4036507c46bc]. What the agent should do: the copy is written from the buyer's side (R9) whoever signs it; a real founder or expert can be the voice when the brand record has one; never an invented authority.

**7.14 Entertain or not.** Hopkins: never entertain, never joke about business or home [6ebd6afa8fcc] [66ff32f28a57]; Whitman: don't be clever [0e09cddd6797]; Tyson: gimmicks in a minority of sends, after the plain emails work [99d753c33b55]. Harry Dry's model lines are funny through contrast (New Balance) and he strips a mascot from a serious promise [988a4dabce09] [6e8d1ddacee4]; the Founders host says entertain before you educate (his gloss). What the agent should do: no compulsory cleverness, rhyme or drama (v1.2); wit is allowed only when it comes from a true contrast and the persona supports it; never at the expense of the 2-second test or the salesman test.

**7.15 Everyone must get it vs the in-crowd.** Harry Dry holds both the 2-second test and "if everyone gets it, you're possibly doing something wrong" [220e0eb8c1d5] [c78fe9d7b47e]. Hopkins: the headline should hail the right people only, so non-buyers not getting it is fine [c1863a8437f7]. What the agent should do: the target buyer must get it in 2 seconds; other people need not; decide who the target is before rejecting a line only they understand.

**7.16 Guarantee style: long money-back vs pay-later vs neighbour's warrant.** Whitman: longest money-back in the industry, shown everywhere [83551014328e]; Hopkins: money-back guarantees had "ceased to be impressive"; pay-after-trial and a local dealer's signed promise won [652fd908ec22] [abac911ba2b0]. What the agent should do: write the guarantee the brand record allows, in plain terms, with the eligibility limits; a pay-later or try-first framing is a wording option only if the brand has that mechanism (03-OFF); do not promise what operations cannot honour.

**7.17 Truth vs persuasion in the sources.** Tyson's CJN says the truth of the challenge is beside the point [930c67d53174]; Whitman says prospects "must remain unaware that you're attempting to influence them" and tells the Torpy's 200 story [952aca21b0fb]; Copy Hackers prints unsourced stats while telling you to back every claim [fb5fb47770a9]; Sandcastles' model invents proof [e9f81c60dc73]. ecomOS: no invented claims, ever. What the agent should do: use these sources' structures and drills, never their permission to invent.

**7.18 Awareness ads.** Jamie: skip brand awareness ads unless you are a monopoly; aim every ad at purchase [f27174953be4]. Hopkins: advertising is not "to keep your name before the people" [6ebd6afa8fcc]. Whitman: repetition and familiarity build trust over time [17b39c491ef9]. The modern full-funnel view is not in these sources. What the agent should do: this playbook writes copy that asks for the next step; campaign objectives are 24-DEP's decision.

**7.19 Sampling unrequested.** Hopkins and Founders: samples only to people who asked [0e72ef7fa48e] [04185b470730]; the Founders host praises Estee Lauder's street sampling; common seeding and PR boxes send unrequested product (not from a source). What the agent should do: when writing a sample or trial offer, make the buyer ask for it after reading the story; seeding strategy is not this folder's call.

## 8. Common mistakes

Merged from all 9 sources, deduplicated, with the fix.

1. Writing about the company (factory, history, awards, staff, "we") instead of the buyer's gain. Fix: BIG DEAL drill; flip sentence starts to "you". (01, 02, 03, 05, 07)
2. Listing features without benefits, or calling a feature's purpose its benefit. Fix: the 5-column table; "You benefit by...". (02, 06)
3. Blind, clever, punny or curiosity-only headlines that pull the wrong readers. Fix: the "what is sold?" test; main promise in the headline. (02, 03, 07)
4. Headlines that select no one ("Brighten up your life"). Fix: name the buyer or the need. (02, 06)
5. Superlatives and platitudes ("best", "premium", "quality", "lowest price"). Fix: replace with a checked number or process fact. (02, 03, 04, 07)
6. Abstract lines nobody can picture ("a better way", "seamless"). Fix: zoom in to an object, person, place or action. (04, 02)
7. Lines any competitor could sign. Fix: find the brand-only fact. (04, 02)
8. Invented or unsourced statistics, quotes, counts and "as seen in" claims; stats from Google or an LLM. Fix: source or cut; P9. (ecomOS; the failure is modelled in 01, 06, 08, 02)
9. Long leads that say nothing; greetings; "I hope this finds you well"; "what if I told you". Fix: cut the lead; first sentence 14 words or fewer. (01, 02, 08)
10. Giving the punchline too early, or withholding everything so clicks come without buyers. Fix: hint the mechanism; keep the reveal for the end. (01)
11. Telling instead of showing; "you can lose 20 lb" instead of a demonstrated case. Fix: shown conviction or a permitted testimonial. (01, 07, 06)
12. Correcting the reader ("wrong") or attacking a belief head on. Fix: understand first, change focus or importance. (01, 02)
13. Chronology instead of story; the lesson at the start. Fix: goal, adversity, turn, lesson last, relived. (01, 04)
14. Several CTAs, several ideas, or too much objection handling in 1 asset. Fix: 1 idea, 1 ask; move the rest to another asset. (01, 05, 09)
15. Tossed salad copy: every good point stacked in case one works. Fix: the audit; cut what does not serve the idea. (09, 04)
16. Vague promises ("3 key lessons") and vague offers ("reduced fees for a certain amount"). Fix: tangible specifics; 1 concrete offer line. (01, 06)
17. Fake urgency: evergreen countdowns, "sells out" on infinite goods, "always feature deadlines" taken literally. Fix: real dates and limits only, with the reason. (01, 02 card)
18. Fear with no fix, a new fear, or so much fear the reader freezes; picturing the afflicted; attaching the brand to a negative scene. Fix: positive default; 4-part fear only when the product truly resolves it. (02, 03, 06, 07)
19. Naming or attacking a rival; "avoid imitations"; copying competitor text. Fix: contrast with the old way; verified facts only; never copy. (03, 07, ecomOS)
20. Filler words (very, really, almost), doubled words, repeated sentences, long bullets, centred small text, reversed body type. Fix: modifier sweep; formatting rules. (01, 02)
21. AI tells and secondhand phrases ("revolutionize", "don't miss out", "yellow taxis"). Fix: strip; write from observed fact. (01, 04)
22. Pasting raw LLM copy; letting the model supply proof. Fix: write first; lift only better lines; strip invented proof. (01, 04, 08)
23. Ad clicks landing on the home page or a page that does not repeat the promise. Fix: congruency; first screen reprises the ad. (05, 03)
24. A bare button ("Start now") with no sense of what happens. Fix: label the outcome; headline gets the first look. (01, 02)
25. Judging by clicks, opens or applause instead of purchases. Fix: cost per purchase; conversion. (01, 02, 03, 07)
26. Judging demand or copy by the writer's or owner's taste. Fix: research; test; outside feedback. (03, 06, 07, 04)
27. Changing a working ad because the team is bored. Fix: change on measured decline; keep the core. (03, 07)
28. Endless identical repetition to a small audience without variations. Fix: redundancy; new executions of the same idea. (02, 05)
29. Voice mismatch with the brand; emojis and hype in a calm persona; gimmicks in every send. Fix: compile document phrases; persona check. (01, 03, 05)
30. Explaining the product to a list that already knows it. Fix: answer "do these work, how, why these"; the 3 blockers. (01)
31. Promo after promo to a list with no value deposits. Fix: goodwill balance (flow design in 14-EML). (01)
32. Subject lines that are ambiguous, give the email away, exceed 40 characters, or end in a period; referring back to the subject in the body; auto-filled preview text. Fix: subject from the body's angle; preview by hand. (01, 05)
33. Writing in a doc and pasting into the surface, so lines wrap badly and truncation cuts the promise. Fix: write in the surface; preview. (04)
34. Skipping research or using it to confirm assumptions; leaving small features off the list; never asking customers what they say. Fix: P1 in full. (03, 06, 07)
35. Copying a viral hook from a distant niche, or pooling many competitors into 1 analysis. Fix: own winners first; reskin formats; 1 competitor per run. (08)
36. Health, income, body or before-and-after claims without a policy check; "spammy" promises that risk the account. Fix: P9 step 4. (01, 02, 06)
37. Offer stacks with invented values; savings computed in the head. Fix: real prices; arithmetic in code. (05 example; ecomOS)
38. Guarantees written broader than the policy. Fix: match the brand record's eligibility limits. (02, v1.2)

## 9. Deliverables

What the agent produces for each task, and the format. Every deliverable carries an internal notes block with assumptions, missing facts and the cards used. Internal notes never appear in client-facing copy.

**9.1 Static ad copy set.** 3 variants for 1 placement, 1 variable each. Per variant: `angle` (1 line: the situation, feature and benefit), `primary_text`, `headline`, `description` (if the placement has one), `cta`, `internal_notes`. Plus a set-level block: the 1 idea (P2), the buying question, the variable each variant tests, the control if a winner is live, the placement limits used and their fetch date `[verify UI]`, and a link to the claim audit. Format: JSON per v1.2 when the caller asks; otherwise a Markdown table with the same fields.

**9.2 Email copy.** Per email: `goal` (value or sell, with the action), `structure` (PPAS, CJN, HSO or outline), `subject` (40 characters or fewer, character count shown), `preview`, `body` (word count shown), `cta`, `ps`, `internal_notes`. For a sequence: an outline block per email (number, goal, subject, preview, story, content, CTA, P.S.) before any body is written, and the sequence's single through-line. Flow timing, resends and segmentation go to 14-EML as notes, not decisions.

**9.3 Landing and sales page copy.** Hero: `eyebrow`, `headline`, `deck`, `cta`. Then each block with `block_name`, `header`, `body`, `proof_used`, `cta` (if any). Plus: the header-only read (headers listed in order, as the through-line test), the awareness stage the depth was set for, the FAQ list with sources for each answer, and the claim audit link. Layout and build go to 07-LPG.

**9.4 Headline bank.** At least 10 candidates. Per candidate: `headline`, `word_count`, `angle`, `caples_quality` (self-interest, news, curiosity, quick easy way), `specific_used` and its source, `3_question_result` (visualise, falsify, own: yes or no each), `what_is_sold_pass` (yes or no), `rank`, `note`. Top 3 marked with the variable they would test.

**9.5 Claim audit.** A table per asset: `claim` (exact wording), `type` (number, comparison, outcome, time, count, certification, free, guarantee, deadline, quote, testimonial, superlative, figurative), `source` (brand record field, document, testimonial permission id, or the public source opened), `verified` (yes, no, removed), `policy_check` (claim category and the standard checked, with date) `[web check]`, `arithmetic` (calculation attached if any), `action` (kept, rewritten, removed). Plus a 1-line verdict: ready, or blocked on named claims.

**9.6 Research pack (when P1 is the task).** The compile document, the customer-language list, the 5-column feature and benefit table, the process-fact list, the competitor message and CTA tables (structure only), the real-rival line, the segment and stage line, the 1-paragraph messaging strategy, and the past-winners note.

**9.7 Variant plan and hand-off record.** Variable per variant, constants, success measure, control, the sizing note (from 09-CRO or `[needs brand data]`), and the record fields: brief, idea, angles, claims and sources, cards used, date, result placeholder.

**9.8 Product page copy.** `title`, `bullet_block` (each bullet tied to a benefit and, where it exists, the filter or search term it answers), `spec_block` (exact numbers from the brand record), `size_or_fit_note` (who it does and does not fit, R67), `faq` (question and answer, each answer sourced to the brand record), and the claim audit link. Layout and build go to 07-LPG.

## 10. What needs live data or a web check

**Needs brand data.**

- Verified product facts with numbers: materials, counts, dimensions, times, process steps, sourcing, certifications (R12, R13, R28, R59).
- Fixed prices, offers, bundles, eligibility limits; real component prices for any value stack (R69, R72, R114).
- Guarantee and return policy; return rate, refund cost, margin (R70).
- Approved and banned claims list (P9).
- Voice samples: approved copy, packaging, support replies, founder posts (R86).
- Avatar, segment, awareness stage; share of traffic new vs returning vs repeat; list join source (R16, R21, R23).
- Reviews (5-star and 1-star), support tickets, chat logs (R11).
- Which desire or pain buyers name in reviews and in past winning ads (R20).
- Past ads with copy, spend and results; results by appeal, by copy length, by question vs declarative hook; results over time with frequency and reach (R118, R119, R121, 7.1, 7.8, 7.10).
- Email results by send: opens (unreliable since Apple MPP), clicks, revenue, unsubscribes, complaints; send history for the goodwill balance; click to purchase rate for teaser emails (R40, P6).
- Landing page for each ad and its first screen; page conversion, bounce and exit for framing decisions (R84, R87).
- Verified competitor facts for any comparison (R24, R112).
- Real segments for any group-limited offer (R73).
- Traffic and conversions per variant for test sizing (R120).
- Testimonials with written permission on file (R63, R110).

**Web check.**

- Current Meta character limits and truncation points for primary text, headline and description, per placement; Meta ad specs page (R102, P12) `[verify UI]`.
- Current Meta advertising standards for: health, weight and body, income, before and after, safety, personal attributes, "free", urgency, comparative claims (R109).
- Local consumer-protection rules on urgency, countdowns, "free" and "limited" (R71, R111).
- Endorsement and review rules for the brand's country and each platform (R63, R110).
- Current Gmail clipping limit and Promotions tab behaviour (R103, 7.11).
- Current guidance on open-rate reliability and sunset windows after Apple Mail Privacy Protection (section 6 email rows).
- Meta Ad Library URL and filters (P1 step 6) `[verify UI]`.
- Readability tool and Flesch formula coefficients (R97; 02 omits them).
- Every historical number before it is quoted to a client: Hopkins's and Whitman's case results, the 60% headline-only figure, Ogilvy's figures, the 25% quote-headline claim, BOGO vs 50% off, installment and "Bill Me" lifts, long-guarantee return claims, De Beers and Rolls-Royce figures, Masterson's 91 of 100, Sandcastles' tool details (section 6 and section 12).
- Publication years: Scientific Advertising (1923 per the brief), Great Leads.

## 11. Freshness and stale-risk notes

| Rule area | Depends on | Re-verify | Note |
|---|---|---|---|
| Meta primary text, headline, description lengths and truncation (R102, P12) | Platform UI and specs | Before every launch-ready set | No source gives them; fetch live `[verify UI]` |
| Claim policy by type (R109) | Meta advertising standards; national ad and consumer law | Before every launch-ready set; re-read the policy page monthly | Health, body, income and before-and-after rules move often |
| Urgency and "free" wording (R71, R74, R111) | Consumer-protection law | Quarterly, and per new market | Fake-countdown enforcement has grown since the sources were written |
| Testimonial and review rules (R63, R110) | Endorsement guidance per country; platform rules | Quarterly | Whitman's 2009 release wording is lay advice |
| Email client behaviour (R103, 7.11) | Gmail and Yahoo bulk-sender rules, clipping, Promotions tab, Apple MPP | Quarterly | 01 and 05 predate current rules; 02's email data is early 2000s and obsolete |
| Email benchmarks (section 6) | Client privacy changes | Do not use without a live check | All open-rate figures here are pre-MPP |
| Ads Library research (P1 step 6) | Meta Ad Library UI | Each use | URL and filters change |
| Readability scoring (R97) | Tool availability | Each use | Compute in code; do not trust the model's estimate |
| LLM hook workflow (P14) | Claude Desktop, Cowork, Sandcastles tiers, credits, MCP tools | Each use | All 2026 tool details can change; the paid-ad adaptation is untested |
| Creative refresh cadence (R118, 7.10) | Platform delivery behaviour | Per brand, from its own data | 05's 24 to 48 hour reach-cut claim is a 2019 observation |
| Print-era formatting (R33 note) | None | Not applicable to screens | Use only for packaging, inserts and print |
| Historical case numbers (sections 6, 12) | None | Before quoting to a client | Anecdotes, not benchmarks |

24 Sep 2026: ecommerce specificity pass applied from ECOM_REVIEW.md; priority block added, 15 rules reworded, 8 levers added, about 1,490 words moved to Appendix A.

## 12. Source index

| No. | Title | Type | Contributed most |
|---|---|---|---|
| 01 | 8 Hour Copywriting Course For Beginners (Tyson 4D, July 2024) | YouTube course transcript, 117,790 words, 115 cards | Email structures (PPAS, CJN, HSO), the edit checklist with dozens of worked cuts, attention formula, one CTA, situational urgency, story vs chronology, compile-first process, ecommerce list blockers, landing page block map, AI use rules |
| 02 | Cashvertising (Drew Eric Whitman, 2009) | Book, 65,196 words, 109 cards | LF8 and appeal choice, BIG DEAL drill, means-end chain, Flesch readability targets, headline rules and starters, 12 lead-ins, extreme specificity, VAKOG and PVAs, fear's 4 parts, inoculation and two-sided messages, guarantee and deadline wording, the 46-point checklist, make-it-easy rules |
| 03 | Scientific Advertising (Claude Hopkins, about 1923) | Book, 21,292 words, 45 cards | Salesman test, one buyer, headline selects, headline swings 5 to 10x, specific over superlative, untold process facts, cure over prevention, complete story, positive 4 to 1, never attack a rival, research before writing, keep proven winners, test before scale |
| 04 | Learn Copywriting in 76 Minutes (Harry Dry, mid 2024) | Podcast transcript, 15,516 words, 29 cards | The 3-question line test, abstract-to-concrete zoom, only point, competitor-signable check, 2-second test, write in the surface, small believable claims, contrast and the implicit "but", rewrite simply, 2-line paragraphs, versions and outside feedback, 9 of 10 bar |
| 05 | Copywriting 101: eCommerce copywriting course (Jamie Dorschuk, about 2019 to 2020) | Live talk transcript, 15,121 words, 34 cards | Second-person discipline, one function per asset, outline before drafting, 24-hour rest and read-aloud, ad-to-page congruency, sentiment matching from 5-star and 1-star reviews, awareness scale and story length, sales page template and header through-line, price positioning, subject-line punctuation |
| 06 | Copy Hackers Book 1 (Joanna Wiebe, 2011) | Ebook, 14,508 words, 28 cards | Messages from customers, messaging strategy, segment choice and 20% to 35% targeting, pain vs motivation, feature and benefit table (5 columns), no fixed rule to lead with the benefit, keyword language, competitor content audit, messaging hierarchy, simple offers, believable claims, negative framing not banned, overwrite then cut |
| 07 | How to Write Ads That Sell (Founders podcast on Hopkins, about Aug 2026) | Podcast transcript, 13,771 words, 29 cards | Service not sale, boasts kill, tell the pains you take (Schlitz), reward not prevention (Pepsodent), demonstration beats argument, requested samples, keystone fact, human personality, keep the ad that works, framing levers (group, price, number) |
| 08 | Claude + Sandcastles = Irresistible Hooks (Callaway, 2026) | YouTube walkthrough transcript, 7,190 words, 10 cards | Ground LLM hooks in own winners, winners vs losers, per-creator analysis, format-fit screen, reskin not clone, 4-bucket extraction, rubric then grade then rewrite, the observed patterns (specificity, 2-sentence amplifier, no throat-clearing, declaratives) |
| 09 | The Copy Rule I Learned From The Best Copywriter I Know (unnamed presenter on Masterson's Great Leads) | YouTube transcript, 1,305 words, 3 cards | Rule of One, the 3 tests (understand, believe, unique), tossed salad audit, one USP |

Moved to Appendix A: each source's credibility and bias paragraph, and the card-errors list (card text that differs from the source).

**Neighbour folders and what lives there.**

- 24-DEP ad deployment: Meta and TikTok account structure, budgets, bidding, scaling, algorithm, creative volume, frequency and fatigue reads, campaign objectives. This playbook hands it the variant plan (9.7).
- 12-GAD Google Ads: search and shopping copy rules, ad strength, keyword-to-ad match.
- 10-MCR paid social creative: images, video, UGC, formats, hook visuals, competitor creative analysis. The words in a video hook can follow group E here; the visual is 10-MCR's.
- 07-LPG landing pages: layout, page build, above-the-fold design, heatmaps, product page structure. This playbook hands it landing and sales page copy (9.3) and product page copy (9.8).
- 09-CRO testing: test design, sizing, validity, readouts. This playbook hands it the variable and the measure (R116, R120).
- 14-EML email lifecycle: flow design, cadence, resends, welcome and launch sequences, revival windows, deliverability, ESP choice. This playbook hands it finished email copy (9.2) and the sources' flow sketches as notes.
- 03-OFF offers: offer and price design, guarantees as mechanisms, trials, discount strategy. This playbook words what 03-OFF decides.
- 02-AVT avatars and 04-BRD brand: research depth and brand voice. This playbook's P1 is the copy-specific slice.

## Appendix A. General background

Moved here on 24 Sep 2026 by the ecommerce specificity pass. Useful for auditing the sources and cards, not for writing store copy. Nothing here is deleted; each item below carries a one-line note of where it came from in the main playbook.

### Source credibility and bias (moved from section 12's table)

- 01, 8 Hour Copywriting Course For Beginners: Freelance copywriter since 2022 who sells a mentorship; clients are coaches and info products; evidence is screenshots, student claims and "stats from Google" with no study design. Ecommerce appears in 3 places. About 40% is freelance client-getting. Bias: promotes his funnel; permits unverified stats and contestable "challenge" hooks.
- 02, Cashvertising: Direct-response copywriter and seminar seller; summarises academic persuasion research (years, no samples) and 1912 to 1991 print readership studies; shows no own test data; many uncited lifts. Bias: sells the seminar; "no qualifications" absolutism on long copy and deadlines.
- 03, Scientific Advertising: Senior agency man selling agency service; evidence is keyed coupon returns on "thousands" of ads with no tables; about 60 cases, many anonymous; overclaims that small tests "always hold". Bias: agency pitch; 1920s US print and mail order only.
- 04, Learn Copywriting in 76 Minutes: Runs Marketing Examples and sells a course; the worked ad is for that course; evidence is famous print ads and craft opinion; historical numbers from memory; an arithmetic error in his own ad (22,000 vs 36,000 hours). Bias: taste-led, no tests.
- 05, Copywriting 101: eCommerce copywriting course: Solo consultant; sells a free course and community; clients mostly courses and memberships; 1 store case (Head Candy) where CRO and automation ran together so copy's share is unknown; open-rate numbers pre-MPP. Bias: launch-sequence heavy; text-only rule contradicted by her own store email.
- 06, Copy Hackers Book 1: Professional copywriter selling a paid ebook series; written for software startups; evidence is practice plus a few cited claims and 2 single cases; her own example callouts carry unsourced stats. Bias: SaaS examples; dated tools.
- 07, How to Write Ads That Sell: Host reads his highlights of Hopkins's 2 books and adds Ogilvy, Estee Lauder and others; sells nothing but carries 3 sponsor reads; all numbers from memory; the file's header describes a different (Hormozi CRO) talk and must not be cited. Bias: hero-worship of Hopkins; host glosses ("painkillers not vitamins", "entertain before educate") are not Hopkins.
- 08, Claude + Sandcastles = Irresistible Hooks: Presenter sells the tool the workflow requires and wrote its rules; evidence is 1 demo on 4 organic creator channels (40 videos); model-generated findings unchecked; the model invented proof in a hook. Bias: product positioning; organic video, not paid ads.
- 09, The Copy Rule I Learned From The Best Copywriter I Know: Sells nothing; retells Masterson second hand; 91 of 100 is a historical review at 1 info publisher; no own data. Bias: none visible beyond enthusiasm.

### Card errors the mini playbooks found (moved from section 12)

Card text that differs from the source. Do not cite these cards for the wrong claim.

- 01: [b990935f853d] is not traceable to the transcript (a supplement-brand bundle that does not appear). [6ba3eae9a81e] names ActiveCampaign as the page builder shown; the transcript names no tool. [e326516d4bdb] says "3 to 8 emails"; the source says 3, 5 or 8 all work.
- 02: [d7cbcd4ec542] says change the offer before the headline; the book says headline, then price, then offer. [58e43cf450ab] misdescribes Editorial Energizers and Survey Power. [91a62eefd6d6] describes the "Ogilvy Principle" as studying Ogilvy's views; the book means the 2/3 photo, 1/3 copy layout. [2f196d76cd7a] puts grabbers before the headline; grabbers are objects attached to letters. [db10ac89cee2] says length is situational; the book says long copy wins with no qualifications. [037f584ed120] lists "social proof" where the book says "comparison". Many cards add ecommerce translations the book never gives.
- 03: [e9d818096148] says single-article mail-order sales cost "$2.50"; the text says $42.50. [3607962859be] inverts "five dollars to do what one dollar might do". [0e72ef7fa48e] says "price at full-size package rather than half-price" and "international circulation"; the text says give samples free rather than part-price, and "outside towns". [dad9da2fb2e6] adds "poorer-class buyers"; not in the text. [652fd908ec22] files the $1,000 Easter hat under cheapness; the text uses it for "people judge by price". [abac911ba2b0]'s title "Questionable Persona" has no basis in the text. Many cards add "For ecommerce" steps that are the card writers' analogies.
- 04: [867743b221ba] ties the New Balance line to Hiut Denim. [e05c0ccdecf9] makes the Volkswagen ad an enemy type C example; the source uses it for layout. [6e39a617d9e1] says "several days"; the source says about 2 days. [6645e37e12f9], [6e8d1ddacee4], [6914df3c2bd8] and [188f4fe29d32] add details the transcript does not give. [bf82611ee658] repeats the 22,000-hour figure without noting the inputs give 36,000.
- 05: [36b9e7b8a840] reads the "1, 1, 2, 1" rhythm as words; the transcript does not say. [2ac1adf98a07] says "at least one of each" format and a garbled revenue figure. [8ccd32a8db57] says closing emails are short; the transcript says "strong sales emails". [3912f9a679c0] mislabels stage 3 to 4. [60d5057bb3c2] says "$10 off"; the transcript says "10 off". [c7a79cc9ee3e] gives "$3.99"; likely $399. [ae22f03a0868] says write the subject last; not stated. [16254d1bf3e4] adds funnel steps the transcript does not list.
- 06: [17b8f4f12a1d] says reviews are a language source; the book never mentions reviews. [2c6f4cda6b12] says negative framings "often capture attention more sharply"; the book says negative "can be very powerful" and is not always better. [ab79ca8e0db3] adds a demand-capture note the book does not make. [19bf368e3817] adds shopper-type matching for framing. Several cards add ecommerce translations (shipping thresholds, bundles, checkout ideas).
- 07: the source file's header describes an Alex Hormozi CRO talk (07-LPG) with claims about above-the-fold views, weekly tests and an A/B calculator; none is in the body and no card covers them. Cards spell "Pepso dent" and "artisan wells". Many card steps (monthly re-audits, quizzes, UGC, prediction logs) are translations, not the source.
- 08: the cards' paid-ad application is an inference; the demo is organic. The 8 universal principles and most of the 11 custom principles are never stated in the source.
- 09: card [1ee01d6bfef2]'s "say it back in 1 sentence" check is the card's, not the presenter's; the presenter gives no research or tie-break method.

### Academic and historical studies (moved from section 6's threshold table)

The operational takeaway from each stays in the main section 6 table. This is the study detail behind it.

- Rudolph 1939 to 1940 headline-length readership study, cited by source 02: of 2,500 Saturday Evening Post ads, headlines of 3 words or fewer were read fully by 87.3%, 4 to 6 words by 86.3%, 7 to 9 words by 84%, 10 to 12 words by 82.5%, 13 words or more by 77.9% [87ab9b6867da]. `[print 1920s]` era; 1 source. Main-table takeaway: longer headlines are read less fully; keep the headline short for a cold feed (also cited in R29).
- Paterson and Tinker 1956, cited by source 02: all-caps text slows reading by about 11.8% compared with mixed case [388f0c750aad] [14dcce0a0c2a]. 1 source, print era. Main-table takeaway: use ALL CAPS sparingly, at most 4 to 5 words, and only for print packaging or inserts (R33 note; not applicable to screens per section 11).
- Petty and Cacioppo 1979, cited by source 02: in a study with 1 argument and college-student subjects, agreement with the argument peaked at 3 exposures and fell at 5 [17b39c491ef9]. 1 source, not a cap on repetition. Main-table takeaway: repetition builds agreement; more exposure is not a guaranteed cap or floor (R118 uses this to argue for redundancy, not a hard repetition limit).
- A "Listerine and Odorno 1919 headline story" was named in the ecommerce review as a study to move here, but no text matching that description was found anywhere in this playbook when the pass was applied; there is nothing to move. If it exists in an earlier draft or a mini playbook not covered here, it was not carried into this version.

### Case examples moved out of their rules

- From R69 (offers, guarantees and deadlines): Copy Hackers' Fidelity case. "No Fees If You Keep $400 In Your Savings Account" replaced "reduced fees for keeping a certain amount"; program customers quadrupled in 4 months (1 case, no baseline) [690303793634]. This is a financial-services example, not a store case. R69's rule wording now stands without it; the offer-wording rule itself is unchanged.
- From R62 (specificity and proof, show don't tell): Copy Hackers' Mint example. Mint (a SaaS budgeting product) shows clean design by having it; each copy chunk in its marketing gets a visual that proves or reinforces the claim, rather than a caption asserting it [61d04467e873] [e5294ffc5f69]. R62's main text now carries a store equivalent instead (a packaging or unboxing shot doing the showing, not a caption asserting quality), citing the same cards for the underlying principle.
