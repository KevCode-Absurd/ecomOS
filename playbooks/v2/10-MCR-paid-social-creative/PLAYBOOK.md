# 10-MCR-paid-social-creative playbook

version: 2.0-draft  |  date: 24 Sep 2026  |  sources: 19 (17 in domain, 2 live-selling sources in Appendix A)  |  cards: 319  |  built from: sources/*.md

## 0. How to use this playbook

**Who runs it.** The paid social creative agent: the creative strategist plus production role that turns brand research into concepts, statics, video scripts, hooks, founder and UGC briefs, VSLs, variant plans and test plans for Meta and TikTok, then reads results and decides what to make next. A designer, editor or reviewer worker can run any checklist in section 5 alone. Account structure, budgets, bidding and campaign settings hand off to 24-DEP-ad-deployment. Ad copy fields (primary text, headline, description) hand off to 11-ADC-ad-copy-deployment. Landing pages hand off to 07-LPG.

**Which sections to load for which task.**

| task | load |
|---|---|
| Define a concept (persona, angle, offer, format) | 3.1, 3.2, P1 to P4, checklist 5.3 |
| Plan the portfolio by awareness stage | 3.3, 3.10, P3, P12, section 6 |
| Brief or review a static ad | 3.4, P5, P6, checklist 5.1 |
| Write or review a video script | 3.5, 3.6, P7, P8, checklist 5.2 |
| Write and test hooks | 3.6, 3.7, P8, P18, section 6 |
| Founder ad or UGC brief | 3.8, P9, P11, deliverables 9.4 |
| VSL | 3.9, P10 |
| Size monthly volume and production budget | 3.10, P12, section 6 |
| Build a test pack and set the read | 3.11, 3.12, P13, P14, P15 |
| Read results and pick winners | 3.12, P15, P16, checklist 5.5 |
| Iterate a winner or revive a fatigued ad | 3.13, P17, P18 |
| Decide iteration vs new concept under Andromeda | 3.13, section 7 (C2) |
| Compliance check before launch | 3.16, P19, checklist 5.4 |
| Use AI in the pipeline | 3.15, P20 |
| TikTok native formats | 3.8 (R117 to R121), P24 |
| Any point where sources disagree | section 7 |
| What to hand back | section 9 |
| Live-selling (Whatnot) questions | Appendix A only, then route to the folder named there |

**Fetch before acting.**

- From brand data: persona list and customer research (reviews, support tickets, post-purchase surveys, ad comments), substantiated claims list, product facts and real product photos, offers the brand can run, live ads tagged by concept, stage, format and source, per-ad spend, purchases, CPA or ROAS, hook rate, hold rate, CTR, link CTR, frequency, hit rate, mean spend per ad, revenue per ad, production cost per asset, monthly spend and target CPA, landing pages available (PDP, advertorial, listicle, quiz), creator rights and usage terms, founder availability and true origin story, brand voice rules. Full list in section 2 and section 10.
- From the data layer: the Meta Ads read tools (read only), the gallery data in `data/meta-gallery/` for Gehna, the retention curves and video metrics the account exposes, the experiment or test log if one exists.
- From the web: current Meta advertising standards for the brand's category (health, personal attributes, before-and-after, branded content disclosure), current Meta statements on Andromeda and creative similarity, current TikTok ad policy for the market, current tool names and prices where a procedure names one. List in section 10, cadence in section 11.

**ecomOS rules that override any source.** Several sources tell the reader to copy competitor ads, invent a statistic, "sneak" before-and-afters past review, script a fake review, run a brand-owned review site as if independent, or stage a problem that is not real. Those instructions are recorded in section 7 and section 12 as what the source said and are not rules here. The rules below win every time:

1. Competitor and third-party ads are signals for layout, structure and mood only. Never copy their text, logos, products, claims or faces. "Recreate this exact ad for every product" (17), "clone any ad" (05), "steal these" (18) and "inspired by" outputs (15) are rewritten in the brand's own words with the brand's own assets, or not used.
2. No invented statistics, studies, percentages, customer counts, prevalence lines or health claims. A number goes in an ad only when the brand can show the study, test or order data behind it. Health, weight, body-image, fertility and appearance claims need a policy check for the market before launch.
3. Generated or AI-edited images keep the real product photo where accuracy matters (jewellery, apparel detail, packaging, labels). AI may build the scene, the layout, the illustration of a problem or the B-roll. It may not redraw the product.
4. No fake interviews, fake whistleblowers, scripted reviews presented as real, fake individuals' pages, undisclosed paid partnerships, or brand-owned "review" sites presented as independent.
5. Competitor ads are never "proven winners". Run time and likes in the Ad Library are weak proxies. Only the brand's own account data proves anything.
6. Meta is read only. Nothing in this playbook publishes, pauses or changes budgets. Section 3.11 and section 4 describe test structures so the creative agent can hand a complete test plan to 24-DEP; the deployment agent executes it.
7. Writing on pages and in copy follows the house rules: short sentences, simple words, digits, no em dashes, no inflated words, no invented claims, concrete before-to-after benefits.

**Source notes to keep in mind while reading.**

- 17 of the 19 mini playbooks are agency or tool sales videos. Every case number is one presenter's example, usually with no spend, sample size or control. No rule here is a promise. Section 12 rates each source.
- Several sources share a presenter or an agency. 01, 02, 03, 04 and 19 read as the same Australian agency (Blue Sense Digital; "Nathan" names himself in 04 and 19). 09, 11 and 13 are also Australian agency teardowns with the same vocabulary and may be the same channel. 08 and 17 are the same agency (Moonlighters). 05 and 15 are a US agency with a paid community and may be the same presenter. When this playbook says "3 sources agree", check section 12 for whether they are independent.
- Mini playbooks 06 and 14 are about live auction selling on Whatnot by thrift resellers. They are not paid social creative. They sit in Appendix A with a routing note and do not shape any rule in section 3.
- Some mini playbooks carry curator header notes or card text that is not in the spoken transcript (07: awareness stages and the PDP claim; 13: "cut every 3 seconds", "wait 30 seconds", the GLP-1 and sauna hooks; 16: a stray 06-MEA header on A/B testing math). This playbook credits those items to the source that actually said them.
- Tags: `[verify UI]` for platform steps that change, `[needs brand data: what]` for anything that depends on the brand's numbers, `[web check: what]` for anything to confirm live.

## 1. Scope and outcomes

**This folder covers.**

- Concept definition: persona (avatar, segment), angle (the argument), offer (product plus value framing), format (the delivery vehicle), mechanism, copy blocks.
- Persona and angle research inputs: reviews, comments, tickets, surveys, calls, Reddit, competitor reviews, the brand's own ad history.
- Awareness stages (unaware, problem aware, solution aware, product aware, most aware) and which formats and messages fit each.
- Static ad rules: clarity vs curiosity, visual hierarchy, headline and image pairing, primary text weight, text density, design faults that cost trust, destination match.
- Video script structures: hook, bridge, mechanism or education, product, proof, objection handling, risk reversal, CTA; product timing; edit pace; native vs studio look.
- Hook craft: the 3 layers, the grading order, hook types, templates, specificity, curiosity with relevance; hook testing and variation levers.
- Founder ads: the argument structure, story elements, involvement spectrum, script roles, batch shooting, refresh. UGC: briefs, creator vetting, creator seeding, usage rights, native TikTok formats.
- VSLs: when to use one, the 7-part structure, modular testing, matching landers.
- Creative volume and production budget by spend tier; portfolio thinking; the quality bar.
- Testing loops as the creative agent hands them to deployment: packs, ads per pack, minimum days to read, forced delivery options, hypothesis per test.
- Reading results: attention, click, post-click, incremental; winner definitions; what public signals cannot tell you.
- Iteration vs new concepts under Andromeda; fatigue causes and fixes; reviving a fatigued winner.
- Winner analysis (creative DNA), the brief, the pipeline, AI in the pipeline.
- Compliance risks in creative: health claims, before-and-after, invented numbers, fake interviews and reviews, competitor copying and callouts, disclosure, personal attributes, likeness rights, image rights.

**This folder does not cover (neighbour folder).**

- Campaign and ad set structure, CBO vs ABO, budgets, bids, cost caps, exclusions, attribution settings, ad set spending limits, incremental attribution columns, DPAs: 24-DEP-ad-deployment. Sections 3.11 and 3.12 keep only what the creative agent needs to write a test plan and read a result. Where a rule is deployment, it says "(deployment, 24-DEP)".
- Primary text, headline and description writing, ad copy iteration: 11-ADC-ad-copy-deployment. Section 3.4 keeps the rule that primary text carries the education on native statics, because it changes how the static is built.
- Landing pages, advertorials, listicles, quiz funnels as deliverables: 07-LPG. This playbook keeps the rule that the destination must match the ad's stage and promise.
- Persona research method as a discipline: 02-AVT. This playbook keeps the persona rules that decide creative.
- Offer construction: 03-OFF. This playbook keeps offer as a concept variable and the bundle rule for low-ticket items.
- Organic content, trial reels as a channel, creator community management: 13-ORG. This playbook keeps trial reels as a creative validation step.
- Measurement, attribution models, MER: 06-MEA. This playbook keeps the rule that top-of-funnel creative must not be judged on last click.
- Live auction selling: no folder yet. See Appendix A.

**Business measures this domain moves.** New customer revenue and new customer CAC at a given spend; the share of spend held by the top 1 to 3 ads (portfolio health); creative hit rate; mean spend per ad and revenue per ad; cold frequency; production cost per winning ad; time from brief to launch; the count of live concepts and formats per awareness stage. None of the 17 in-domain sources shows a controlled result. The most reliable evidence is a brand's own account history.

## 2. Inputs the agent needs

| input | from where | required or optional | why |
|---|---|---|---|
| Persona or avatar list with problems, desires, buying triggers, language, proof needed | brand record (02-AVT), user | required | Concept = persona + angle + offer (R1). Broad demographics make forgettable creative (R11). |
| Customer language: reviews, support tickets, post-purchase surveys, ad comments, call recordings, Reddit and forum threads, competitor reviews and competitor ad comments | brand record, data layer, web | required | Angles, hooks and objection handling come from repeated customer statements (R13, R14, R59). |
| Substantiated claims list: every number, study, test, certificate, customer count the brand can prove | brand record, user | required | ecomOS override 2. No number or health claim without proof (R43, R170). |
| Product facts: ingredients or materials, mechanism or reason to believe, specs, price, bundles, guarantees | brand record | required | Mechanism and proof sections (R57, R63); offer variable (R8). |
| Real product photos and footage | brand record | required | ecomOS override 3. AI may not redraw the product (R166). |
| Offers the brand can actually run and margin room | brand record (03-OFF), user | required | Offer is a concept variable and a hook lever (R8, R94). |
| Live ads tagged by concept, persona, angle, offer, format, awareness stage, source (in-house, UGC, AI) | data layer, brand record | required | Portfolio coverage, gap finding, similarity check (R20, R28, R158). `[needs brand data]` |
| Per-ad spend, purchases, CPA or ROAS (7-day click), incremental ROAS where available, hook rate, hold rate, CTR, link CTR, frequency, live days | data layer (Meta read tools, gallery data) | required for any read | Winner definitions and diagnostics (3.12). `[needs brand data]` |
| Hit rate, mean spend per ad, average revenue per ad, winner churn per month | data layer, computed in code | required for volume sizing | Volume formulas (R123). `[needs brand data]` |
| Monthly spend, target CPA, breakeven incremental ROAS, daily budget | brand record (20-FIN, 24-DEP) | required | Tier rules, pack sizing, 7-day minimum arithmetic (R124, R133). |
| Production cost per asset by source (creator, designer, editor, AI) | brand record | optional, required above $100K/month | Gross profit per ad by format (R25, R125). |
| Landing pages available: PDP, advertorial, listicle, quiz, long-form page, and their conversion rates | brand record (07-LPG) | required | Destination match decides clarity vs curiosity (R30, R33). |
| Founder availability, true origin story, lab or supplier proof, founder handle content | brand record, user | required for founder ads | Founder story must be true and viewer-first (R101 to R105). |
| Creator roster, accents and markets, usage rights, affiliate terms | brand record | required for UGC | Native accent per market (R110); rights before paid use (R112). |
| Inventory position and cash conversion cycle | brand record (20-FIN, 18-COG) | optional | Squeeze or breathe a winner (R155). |
| Category, market and currency | brand record | required | Compliance category (3.16); AUD vs USD in tier numbers. |
| Competitor ad references (Ad Library, saved swipes) | web, inspiration store | optional | Layout and mood signals only (override 1). |
| Brand voice rules and category norms | brand record (04-BRD) | required | Health-style DR formats may not fit a jewellery or gifting brand (R107, section 12). |
| Current Meta and TikTok policy for the category | web | required before launch | Compliance check (P19). `[web check]` |

## 3. Decision rules

Every rule states the rule, when it applies, the mini playbooks that support it (by number), any conflict (by section 7 code), and card ids. Where only 1 source supports a rule, the rule says so. Where sources disagree, the strictest condition is kept here and the disagreement is written out in section 7. Rules that are deployment rather than creative are marked "(deployment, 24-DEP)" and are here only so the creative agent can write a complete test plan.

### 3.1 Concept definition: persona, angle, offer, format

**R1. A concept is 1 persona plus 1 angle plus 1 offer. Format is a 4th, weaker lever.** A new concept changes at least 1 of persona, angle or offer. Same persona, angle and offer in a new format gives some new reach with heavy overlap. 08 says the same as "avatar x angle = package". 12 splits the "what" further into concept (core idea), angle (how it is presented) and mechanism (why it works). 15 says "avatar + template = ad concept". Condition: every brief, every test hypothesis, every tag on a live ad. Sources: 01, 03, 08, 12, 15; 19 uses the same 4 levers for hooks. Conflict: C14 (how much format counts). Cards: [939b4100ac4f] [f18d8afedb58] [ab5dac71c1dc] [8c915d03411c] [72f6438afa3a] [1b2a2554a0c8] [8cfd832f085a] [15769b01529d] [ec923b82af65].

**R2. A new design, colour, pose, background or model is not a new concept and is not worth testing on its own.** 03: the effect might be 1% to 2%, unmeasurable without enormous budgets, and under Andromeda near-identical ads are grouped and served to the same people. 05: the "old way" of variants of 1 winner ends with all spend in 1 to 4 creatives and a collapse when they fatigue. 15 and 17: an iteration must be "a decent swing", what "old-school Facebook" would have called a new ad. Condition: any variation plan. Only run a variation if it is measurable, worth the spend and would change what the team makes next. Sources: 01, 03, 05, 15, 17, 19. Conflict: C2. Cards: [d6f4dfaaf4c4] [8c915d03411c] [1e5ab3cbe70b] [80dbff5fec17] [fa341581e505] [f8f574a45327] [a15bb69c9b3a] [59cf922e4996].

**R3. Decide what the ad must say before choosing the format.** "Should we make UGC or a static?" is the wrong first question. 01's 5 format questions start with "what is the concept". 03: do not start in Canva; about 80% of the time goes to research and concepting. Condition: every new round. Sources: 01, 03, 10. Cards: [bc432cb2ccf7] [789c10faf325] [d797d2ae775b] [e36ec3e6809d].

**R4. Write the angle as 1 sentence for 1 persona: who, the product, why it solves their problem, the proof.** Then every line in the ad must support that sentence. Packing 10 selling points into 1 cold ad turns it into "an infomercial when someone was just watching a cat video". 1 product with 10 reasons to buy is 10 angles, not 1 ad. Condition: cold-traffic ads. Sources: 01, 10. Cards: [087eee279056] [f18d8afedb58] [13fa07bab746] [01183c908919].

**R5. Build the angle from components, not from features.** 01's list: problem agitation (skip if the viewer is not problem aware), contrarian truth, social proof (stack toward the back), domain authority (a runner for a running product, not a lab coat everywhere), curiosity gap (open early, close late), comparison or objection handling, transformation. Proof must match the persona's age and gender. 12's copy-block checklist runs beside it: pain, promise, proof, curiosity, constraints, conditions; more and stronger blocks "typically" make a better ad. Condition: writing any script or long-copy static. Sources: 01, 12. Cards: [087eee279056] [bacba7a80164].

**R6. Separate the mechanism into 2 parts: why the viewer has the problem, and why this product fixes it.** Best mechanisms are simple, intuitive and new, usually 1 problem cause and 1 solution cause. The mechanism gets stronger when it forms 1 story with the founder, the creation story, unique ingredients or features, and a moment in time. In supplements the mechanism is the ingredient; in other categories it is craft, material, fit or care. Condition: any ad that must educate (problem aware or colder). Source: 12; 11 and 13 agree that every claim needs its "why". Cards: [8cfd832f085a] [2f0b793e3ea7] [2370029af17b] [4e1cb65d14b8].

**R7. When creative stops working, test in this order: angle, then offer, then persona, then format.** 01's reasoning: past buyers prove the persona buys, so when a persona stops buying the angle or offer is wrong; the offer may matter most but has the least room to change; persona adds breadth once the offer is fixed; format is last. Most teams run the order backwards. 02 ranks the difficulty of changing a founder ad: offer easiest, angle hard, persona hardest. Condition: diagnosis of a failing concept, not a claim about which variable matters most. Source: 01 only for the order; 02 for founder ads. Cards: [4a3ce680ae23] [73f8f945b93b].

**R8. Treat the offer as a concept variable, not a discount.** Offer change = a different product, a different value framing (bundle, gift with purchase, tiered discount on 2 or 3 units, subscription), or different packaging. Avoid deep discounting as the only lever (01: do not eat 40% of margin). When the unit price is too low to carry ad cost, sell 3, 5 and 6 packs so AOV reaches about $25 to $30 (18's inference, not observed data). A strong offer can close a sale on its own (16, 1 personal anecdote). Condition: any concept board; offer construction itself is 03-OFF. Sources: 01, 03, 16, 18, 19. Cards: [4a3ce680ae23] [8c915d03411c] [5aaabe53c66f] [220538bd0247] [ec923b82af65].

**R9. Every product solves a problem, functional or emotional.** A clothing brand "makes people feel good about themselves, feel cool, feel part of something". Light products (golf accessories, a dip cup) lean on fast attention and connection, often humour; heavy private problems (fertility, appearance) lean on curiosity and emotion and route to a quiz or education page. Condition: brands that think they have no problem to agitate. Sources: 08, 16. Cards: [7d806738414a] [8bf081bed714] [84a55aede410].

**R10. Aim for self-recognition, not cleverness.** "This solves my exact problem" beats "the world's most cinematic ad that appeals to everybody". An ad built for 1 ICP should fail with other ICPs, and that is expected. Condition: cold hooks and scripts. Sources: 10, 16. Cards: [3921589ed44c] [84a55aede410] [9d1bbe5069da].

### 3.2 Personas and research

**R11. Build personas from problems, desires and buying triggers, not demographics.** "Women 25 to 45", "busy professional", "health-conscious parent" make forgettable creative. "A mom who has tried 6 supplements because her toddler won't eat vegetables" tells you the script, the talent, the language and the proof. 12's segment grammar: outcome x demographic x facet (a state, event or condition such as runner, GLP-1 user, on finasteride). 08: the avatar is the ICP and every problem the avatar has is an angle. Condition: always below mid 8 figures; broad unaware ads for a whole population need very high skill (01 gives 2 different thresholds, "mid 8 figures" and "$50M plus"). Sources: 01, 08, 12. Cards: [53ee81550f45] [939b4100ac4f] [e671f82f98b0] [0682f4fbff61] [72f6438afa3a].

**R12. Build the persona list by hand first, then use an LLM to expand it.** 01: spend about 20 minutes on avatars, list 2 to 4 core personas, drill into problem variants (acne at 20 to 25, 30 to 35, 40 to 45 are 3 personas), aim for 20 to 40 by hand, then give the full list plus wide business context to an LLM and ask for 20 to 30 more; keep 4 to 5 good ones, feed them back, ask for 10 to 20 more; roughly double the list. Do not start from 3 personas and a website URL: you get the average answer everyone gets. Condition: any persona expansion. Source: 01 only for the method; 03 and 16 agree LLM-only concepting gives everyone the same ideas. `[needs brand data: existing persona list]`. Cards: [bf65df9beea1] [53ee81550f45] [7a115c9bb3e2] [d59ecd84945b].

**R13. Research the customer before anyone opens Canva or a camera.** The research menu across sources: existing reviews, comments on the brand's ads and posts, support tickets, sales-call or support-call recordings, post-purchase surveys, Reddit and forum threads, Amazon reviews, competitor reviews and comments under competitor ads, calls to checkout abandoners, the brand's own top and bottom ads. 16: block 3 to 4 days of manual reading for a new niche and build 1 research document of raw quotes and screenshots. 03: about 80% of time on research and concepting. Condition: every new round, and before a new product's first ads. Sources: 03, 08, 10, 11, 12, 16. Conflict: C15 (AI research vs manual). `[needs brand data: review exports, tickets, surveys, ad comments]`. Cards: [e36ec3e6809d] [d59ecd84945b] [789c10faf325] [d797d2ae775b] [4fb56bc1019f] [8e3f775ece26] [36945e14679a] [1daabb35866f].

**R14. Extract 3 things from research: what the customer wants, what stops them, what they already tried.** Each strong, repeated statement is an ad idea. Repeated use cases across reviews (a blackout blind used in a nursery, an RV and a truck cab) are separate angles; one-off mentions are not. Condition: turning research into angles. Sources: 10; 11 uses the same 3 buckets for objection handling. Cards: [e36ec3e6809d] [320d499e601c] [4fb56bc1019f].

**R15. Use the ICP's own words and in-group signals.** Niche terms ("ascend" for looksmaxing), the customer's phrasing from reviews, jokes the group would repeat. AI will not write niche humour for you (16). Condition: hooks, headlines and body copy for a specific persona. Sources: 10, 16. Cards: [3921589ed44c] [84a55aede410] [d59ecd84945b].

**R16. Do not position below the real market, and keep benefit pillars broad enough to scale.** 13: a creatine brand that says "not for the everyday sedentary crowd, this is for your serious athlete" cuts the market so far it "will never be a hundred million business"; sell benefits that apply without the core activity. 09: "energy, focus, recovery" scales; "helps me at the gym, helps me running" narrows to 1 avatar. Reconcile with R4 (1 ad, 1 persona): each ad is specific; the portfolio stays broad through many personas. Condition: brand-level positioning and pillar wording. Sources: 09, 13. Cards: [df555261a040] [ef1959f490cb] [51a88883a763].

**R17. When 1 avatar is maxed out, open new avatars (personification) and new facets (horizontal scaling).** 05: for brands at thousands to $10,000+ a day after a plateau of months, list other problems the same product truly solves (sleep gummy: cannot fall asleep; sleep but wake groggy; wake through the night), each a different person, plus identities and use cases. 12: most of the biggest gains come from new outcomes, sub-outcomes and multiplied facets. Condition: a plateau on the main avatar, or a planned expansion; only claim benefits the product really has. Sources: 05, 12. `[needs brand data: spend, frequency and CPA trend for the main avatar]`. Cards: [4db4b950e221] [0682f4fbff61] [d3000970b47e].

**R18. Diversify idea sources; never source only from competitors, your own head or proven templates.** 12's STORMING list: swipes, templates, organic research, the segment x format matrix, internal patterns in your own account, new styles, gambits (low hit rate, occasionally big). 17: study competitors 1 to 2 steps above you, not giants or brands too small to be selling; skip Ad Library ads marked "low impression count". Under ecomOS override 1, competitor ads give layout, structure and mood only. Condition: building the idea pipeline for a batch. Sources: 12, 17, 13, 03. Cards: [36945e14679a] [1daabb35866f] [5790ccbc3904] [8ef182c6518e] [a0ce2d2f7363].

### 3.3 Awareness stages and matching formats

**R19. Map every creative to 1 awareness stage before it is built.** The 5 stages as the sources use them: unaware (does not know the problem exists), problem aware (knows the problem, not that a solution exists), solution aware (knows the general solution, not your product; 03: "where we start getting cold audiences"), product aware (knows your product, has not bought), most aware (knows the brand, probably visited). Classify by how much the ad explains, not by what the brief intended. Condition: every brief and every live-ad tag. Sources: 01, 02, 03, 05, 08, 13. Cards: [c218585e29e4] [af4c74b18af1] [322374ef1b12] [2e9ac19f8685] [1a178c0c2400] [86dcadbf0b6b] [7d806738414a] [4e1cb65d14b8].

**R20. Weight the portfolio toward the less aware stages.** 01: 70% to 90% of assets for the less-aware stages, about 20% middle, 5% to 10% bottom (his split does not sum to 100). 02: most creative in stages 1 to 3, about 20% in stages 4 and 5. 03: 90% of statics people make are product aware, which is why they "fail to scale". 05: 5 top, 5 middle, 5 bottom in a 15-ad batch. 08: build only for the extremes, nothing for the middle. Strictest reconciled rule: at least 70% of new assets serve unaware, problem aware or solution aware viewers; never build a library that is all testimonials, offers and hero product shots. Condition: any brand whose live library is mostly product aware. Sources: 01, 02, 03, 05, 08. Conflict: C4. `[needs brand data: live ads tagged by stage]`. Cards: [a23b0e4bcf1c] [af4c74b18af1] [cf1973e97542] [2e9ac19f8685] [7ef548d9c0df] [7d806738414a].

**R21. The hook, the body, the image and the copy must sit at the same stage.** A curiosity hook followed by a feature and ingredient tour "makes no sense" (13). A product-aware image with solution-aware copy fails (03's VPA creatine example). Condition: every static and video review. Sources: 03, 13. Cards: [cb664cb20762] [5ca4fa6b39ad] [541bb0ca2a17].

**R22. Less aware viewers need longer educational formats; product and most aware viewers can take images, offers and catalog ads.** 01's 5 questions before choosing a format: what is the concept; does it need education (if yes, VSL, long video or long-copy static); can the value fit in 1 frame (if yes, lean to images or carousels); does the product need a demo; what stage. 10: if the value must be seen (something folding open, real use), a static cannot show it. 03's static map: top of funnel = problem agitation, native, PR and advertorial, founder statics; middle = comparison, before and after, listicle, feature call-outs; bottom = offer call-outs, reviews, hero product shots. 05's map by stage: unaware = educational or statistic-led problem naming, founder story, downside of something they already use; problem aware = before and after, feature call-outs, "3 reasons why"; solution aware = us vs them, social proof, long-term testimonial UGC; product aware = limited offers, bundles, more testimonials; most aware = direct offer and cart reminder. Condition: format choice after the concept is set. Sources: 01, 03, 05, 10. Cards: [bc432cb2ccf7] [1190d2930cfd] [65acf3feb958] [d2e3d5f918af] [86dcadbf0b6b] [e36ec3e6809d].

**R23. Statics are not only bottom of funnel.** 01: "images are bottom of funnel, video is top of funnel" is "a skill issue"; statics have reached $500,000 lifetime spend. 03: statics have the lowest CPMs, cost about 4x less than video, and are the fastest way to test angles, concepts and offers; problem-agitation, native and advertorial statics serve cold traffic. 07: a single static (the mocha protein ad, run 2.5 years) can show uniqueness, mechanism and proof. Condition: any plan that puts statics only in retargeting. Sources: 01, 03, 07. Conflict: C3. `[needs brand data: CPM, CTR and CPA by creative type in the brand's account]`. Cards: [aa8f85929d1f] [bc432cb2ccf7] [00c2e103130f] [b0132ad73a68] [08f49b8491b0].

**R24. Compare formats on expected gross profit per ad, not on ROAS alone.** Expected gross profit per ad = average revenue per ad minus average spend per ad minus production cost per ad. 03's worked example at $1,000 revenue per ad: at 10x, a $20 static returns $880 and a $200 video $700 (20.5% less); at 2x, $480 vs $300 (37.5% less). 01: images at $50 cost returning $300 beat videos at $500 returning $400 even though the videos "perform better". Condition: production mix decisions; requires per-ad economics. Sources: 01, 03. `[needs brand data: revenue, spend and production cost per ad by format]`. Cards: [602ee9ba7290] [b0132ad73a68] [aa8f85929d1f] [0c485f7f58f5].

**R25. Product-aware creative cannot educate an unaware viewer. Do not put large cold budget behind it.** 02's example: a face-oil ad that rolls through testimonials is fine at the bottom of the funnel and "not a good ad for spending a quarter million dollars behind" on cold. A whole library built at the bottom (taste, value, "cheaper than the pills") will not scale on cold. Condition: budget allocation across creative. Source: 02; 03 agrees for statics. Cards: [af4c74b18af1] [cf1973e97542] [2e9ac19f8685].

**R26. Bottom-of-funnel creative handles objections, 1 objection and 1 proof point per ad.** 01: at a 5% site conversion rate 95% did not buy; map why (his illustrative split: price, trust, quality doubt, not ready, 20% each) and make 1 ad per objection: cost per use and value anchoring for price; customer and review counts and UGC for trust; product in use, before and afters, demos for quality doubt; educational or lifestyle content for not ready. 08: write every objection down, call checkout abandoners, and make each bottom ad carry 1 objection and 1 proof (a lifetime warranty against 1-year rivals; 1 clinical claim). Condition: retargeting and product-aware ads. Sources: 01, 08, 09. `[needs brand data: objection mix from surveys, tickets and abandoner calls]`. Cards: [0cd3c4f726de] [8e3f775ece26] [cac9faff0225].

**R27. Run several distinct formats at once because delivery shows different formats to different people.** 01: Meta serves people the formats they engage with (the presenter says he never sees UGC or DPAs), so format variety reaches people a single format never will. 05: 10 to 15 distinct formats and angles at once, so 1 fatiguing does not tank the account. Condition: portfolio planning; format still ranks below persona, angle and offer (R1). Sources: 01, 05. Cards: [1d9173fc3207] [80dbff5fec17] [c3b5ba2b7356].

**R28. Format innovation gives a temporary edge; copying a format gives little edge unless you are first.** Native formats people do not read as ads (tweet screenshot, notepad, text message, paparazzi photo) stop the scroll until the feed gets used to them. Condition: choosing formats; check the category's Ad Library for saturation. Sources: 03, 07, 12, 15. `[web check: Ad Library scan of the category for the format]`. Cards: [a0ce2d2f7363] [dbda4aba2928] [10b56ec55756] [15769b01529d].

**R29. Shift large retailers from desire-led toward pain-led creative.** Brands built on campaign shoots run about 90/10 desire to pain; move toward 60/40, and the best brands sit near 70/30 with pain-led performance creative as the larger share. Condition: brands whose library is mostly lifestyle and product beauty shots. Source: 01 only. Cards: [fb43b02e6f51].

**R30. Decide the ad's job from the page behind it.** If a quiz, listicle, advertorial or strong landing page finishes the sell, the ad only needs to earn the right click. If nothing behind the ad sells, the ad must do the selling (a long prospecting VSL). Condition: every brief states the destination and its job. Sources: 03, 11, 16. `[needs brand data: which pages exist and their conversion rates]`. Cards: [8bf081bed714] [2e9ac19f8685] [1567d2668c63] [9d1aae2f4dcb].

### 3.4 Static ad rules

**R31. A static has 3 jobs: stop the scroll, communicate the message, drive action.** Stop the scroll either by looking native (people do not realise it is an ad) or by being a deliberate non-native pattern interrupt. Communicate the angle, the offer and who it is for in few words; if the image stays native and light on information, the primary text carries the message. Drive action either by hinting at an article behind the click (advertorial) or through long-form copy that walks the reader through the stages. Condition: every static brief. Source: 03; 07 and 16 give the same 3 jobs in other words. Cards: [a0ce2d2f7363] [84a55aede410] [08f49b8491b0].

**R32. Pick one end of the clarity vs curiosity spectrum. Never sit in the middle.** Clarity end: a viewer looking for 3 to 4 seconds knows what is sold, the angle, who it is for and the offer. Curiosity end: the viewer cannot tell what is sold or that it is an ad, and is pulled into the primary text or the click. The middle ("Guaranteed energy in just 5 minutes", "We don't stop improving. Neither should you.") is "slop creative" that scoops up attribution as a middle-funnel ad and never drives growth. Condition: every static, decided before build. Sources: 03, 07. Cards: [102cc3ec8112] [033a793e7d07] [60f8424e2b37] [8eb2a2b5a787] [17bfe69f2476] [1f32e05c1042].

**R33. A curiosity gap works only if the target buyer wants it closed for their own benefit.** "We don't stop improving" opens a gap nobody has a stake in. "Symptoms of vitamin deficiency" opens one the reader cares about. Condition: the curiosity end. Source: 07; 13 says the same for video (the knife hook). Cards: [17bfe69f2476] [8e0335ccf918].

**R34. Send curiosity, native and advertorial clicks to an educational page, not a product page.** 03: this is where "most people fall apart" and conclude statics do not scale; for the curiosity direction "you don't even want to sell them on the landing page". 04: curiosity-gap statics win click-through "by far" but bring junk clicks, so send them to a listicle or long educational page that names the product only at the end. 07's presenter says only that clickbait works when the landing page and retargeting do the teaching; the PDP claim in 07 is a curator header. Clear-offer statics for product and most aware buyers can go to a PDP. Condition: any static on the curiosity end or aimed at unaware or problem aware viewers. Sources: 03, 04, 07 (in part), 11 for VSLs. Conflict: C8. `[needs brand data: which educational pages exist]`. Cards: [4a4cc4147dbc] [f5fe1d2b059b] [f4d743d1a127] [9197d49f4af4] [369b559b9fb2] [9d1aae2f4dcb].

**R35. Design the eye path: the first thing the eye lands on must be the highest-awareness message, not the product category.** If the biggest element reads "protein powder", the ad is a bottom-of-funnel pitch at first glance. Replace it with the problem, the persona call-out or "new technology". Plan 3 to 4 eye stops that pull the viewer through the stages (03's mocha read: product image creates desire, bold centre claim confirms, top call-outs add detail, review adds trust). Control the path with 3 levers: size (the eye goes to the biggest element), contrast (the eye goes to what differs), whitespace (steers the eye off empty space onto what matters). Condition: every static build and review. Sources: 03, 07. Cards: [f8a4e5a25281] [19abb79c0e64] [08f49b8491b0].

**R36. Pair the image and the headline like a YouTube thumbnail and title.** Each adds context the other lacks; neither carries the message alone. 07's substitution test: swap in a generic image in your head (a plain tub of powder); if the headline no longer makes sense ("wait, what's the simple switch?"), the pair is too loose. Generic category shots fail twice: saturated market and no link to the headline. Condition: every static. Sources: 03, 07. Cards: [541bb0ca2a17] [2022d1907c7a].

**R37. Give primary text and headline equal weight to the image on a static.** People read them on statics far more than on video. Native statics and advertorials give little away in the image and "force people to read the primary text", which is "where we sell". Put the product name and offer in the primary text, not the image, on a native static (07's IM8 read). Condition: statics, especially native and curiosity-end; copy writing itself is 11-ADC. Sources: 03, 07. `[verify UI: truncation by placement]`. Cards: [541bb0ca2a17] [9a2fc128c78d] [37c10bda4253].

**R38. Clarity beats design, but layout faults cost trust.** 03: under Andromeda "the design of a static ad really doesn't matter", some of the best examples look ugly and have spent a quarter million. The same source and 07 then list faults that "lose authority": poor spacing, a product pushed off to one side, a jump from lowercase to uppercase, an unneeded logo, a graph nobody can read in 2 seconds, sub-headlines too small to read on a phone (07: make them about 30% bigger and move them up). Reconciled rule: design is not the performance lever; layout, hierarchy, spacing and legibility must not break clarity or trust. Condition: every static review. Sources: 03, 07. Conflict: C16. Cards: [f8a4e5a25281] [3db510f74584] [1f32e05c1042] [9f262dc7beaa] [08f49b8491b0].

**R39. Lead with the plain benefit; put the mechanism after it, in brackets or smaller type.** "Feel less hungry (lowers ghrelin)" beats "lowers ghrelin, improves mitochondrial efficiency". Reorder, do not delete the science. 09's video version: tie every feature to a benefit and say the benefit first, because the retention curve only goes down. 16's blanket "nobody cares about ingredients or GSM" is read as: specs alone are not an ad for cold scrollers; specs still build trust for product-aware buyers and expert personas. Condition: cold statics and scripts. Sources: 07, 09, 16. Conflict: C17. Cards: [9f262dc7beaa] [cac9faff0225] [220538bd0247].

**R40. On a clean product-shot static, keep the headline to about 5 to 6 words and make it answer "why this instead of what they use now?"** "Guaranteed energy in 5 minutes" fails because coffee already gives that. Angle types 07 gives: a specific moment ("Avoid the 1pm crash"), money ("Save $6 per day"), persona plus problem. Reuse the same clean layout for each angle and change only the headline. Condition: product-forward statics. Source: 07 only for the word count. `[needs brand data: real unit price and substitute price before any savings line]`. Cards: [4f26d77793fa] [369b559b9fb2].

**R41. Name a persona and a problem in as few words as possible, or list 2 to 3 related problems to widen the market.** "GLP1 hair loss hits hard" self-selects the right reader and raises a fear in readers who do not have the problem yet. A symptom list tied to ingredients (IM8's tweet) reads as relevant to a large share of people while pulling in only those who care. 13's video version: "IBS, leaky gut, or bloating" names 3 personas; "leaky gut" alone loses most viewers. Condition: problem-aware statics and hooks; health lists carry claim risk (3.16). Sources: 07, 13, 03. Cards: [6afdcae5d6b5] [37c10bda4253] [51a88883a763] [f4d743d1a127].

**R42. Social proof must be recognisable as proof, and the product shot must look like what arrives at home.** An unattributed review line reads as confusion; it needs stars, a name or a face. A true-to-life product shot at the end closes the sale (07's "McDonald's photo shoot" point); 03 adds that a plain product shot can add useful friction so buyers are not surprised on site. Condition: any static with a review or a product image. Sources: 03, 07. Cards: [f520a0111397] [08f49b8491b0] [ae9948825d17].

**R43. Specific numbers read as authority. Use only numbers the brand can prove.** 07's presenter says a bold percentage works "even if you've just made it up" and 03's presenter praises a percentage that suggests a study "even if there wasn't". Under ecomOS override 2 neither is allowed. 04 and 10 agree on the true version: "found the same 2 problems" beats "some problems"; if the brand has data, show the number; if not, it is an unsupported claim, so do not show it. Condition: every number in any creative. Sources: 04, 07, 10, 13 (true version). Conflict: C18. `[needs brand data: substantiation behind every number]`. Cards: [385b3e7e17c3] [0ac3b2659983] [306f74067bdf] [ee8baa9c8041] [3db510f74584].

**R44. Never serve a white-background product shot or a plain "at home treadmill" image to cold traffic.** It "will hit no one" except most-aware buyers and shows "the metal rectangle", not the reason to buy. Exception: high-intent buyers choosing who to buy from. Condition: cold statics. Sources: 03, 10. Cards: [1a178c0c2400] [2e9ac19f8685] [13fa07bab746].

**R45. An unaware or problem-aware static needs long primary text or an educational page, because a static is consumed in about 4 seconds.** Long-copy story statics work on Facebook feeds for 50+ audiences (01, 03): open with a persona or problem call-out ("Read this if you're always bloated by 3 p.m."), first-person story, why the problem happens, the solution, proof and timelines, product revealed late, custom lander per angle. Condition: cold statics that must educate. Sources: 01, 03. Cards: [2e9ac19f8685] [9a2fc128c78d] [4101de6af476] [e10005e1b904].

**R46. Use an illustration for problems that are hard or unpleasant to photograph.** A cartoon of hair loss shows the problem cleanly and avoids a graphic image that 07's presenter guesses could hurt delivery (his guess, not policy). Condition: sensitive health or body topics; still needs a policy check. Source: 07 only. Cards: [5bfda2bed53d] [6afdcae5d6b5].

**R47. Scale a working static format by keeping the format and messaging and swapping 1 concept element.** A problem-agitation static that works for greens powder is rerun for protein powder; a women 30 to 40 static is rerun for men; weight loss becomes longevity. Do not keep iterating the format itself. Build the template once and swap only the words and the picture. Condition: after a static format has proven itself in the account. Sources: 03, 07. Cards: [6480746607a0] [d6f4dfaaf4c4] [4f26d77793fa] [6afdcae5d6b5].

**R48. Drop the logo from the image when the page name already shows the brand, unless the logo is part of how a native static reveals itself.** 03 and 07 both remove an unknown brand's corner logo as "not relevant". 03's Venroy read is the exception: the light logo is how the viewer discovers the paparazzi image is an ad. Condition: statics for cold traffic. Sources: 03, 07. Cards: [3db510f74584] [1f32e05c1042] [784187eac526] [0e29070e9b20].

**R49. Do not judge top-of-funnel statics by last-click ROAS.** They drive cheap clicks that get retargeted elsewhere in the account, and the retargeting ad takes the attribution; bottom-of-funnel statics may show 7x while a proper top-of-funnel static will not. Judge on account-level financial KPIs, new customer volume and the halo around launches. Condition: any static read. Sources: 03, 01. `[needs brand data: blended revenue, new customer count and MER around launches]`. Cards: [b3058b60c97e] [57ca8c633830] [9d506de16067].

**R50. A convincing static may not need a CTA in the image; test it, do not assume it.** 07's presenter runs strong organic posts as ads with no CTA added ("people will naturally try to take the next step"); Meta still shows its button. Condition: a hypothesis to test on native statics only. Source: 07 only. Cards: [4e47f314df0c].

**R51. A big brand's weak static may be carried by its logo; a small brand has no such shield.** Judge a competitor format on its own merit, and expect that a new, unsaturated category lets mediocre ads win until rivals arrive. Condition: reading competitor statics. Source: 03 only. Cards: [0e29070e9b20].

### 3.5 Video ad script structure

**R52. A cold video ad runs hook, bridge, education or problem agitation, mechanism, product, proof, objection handling, CTA.** The sources give the same skeleton in different words. 13: hook, bridge, body education, product plus proof. 09: hook, bridge, education or agitation, objections, features tied to benefits, proof, CTA. 04: hook, failed common approaches, discovery as education, alternatives rejected, product, outcome, offer. 11 (VSL): hook, problem, mechanism, objections, bridge to product, proof, risk reversal, CTA. 02 (founder): claim, proof, mechanism, proof, CTA plus social proof. 18 (TikTok): hook, raw story or demo, product and CTA at the back. Condition: any video for unaware, problem aware or solution aware viewers; the order flexes (R58), the parts do not. Sources: 02, 04, 09, 11, 13, 18. Cards: [a48f56ddf075] [66dd24ac26be] [46035a697541] [583ab7df2aaf] [c57792ab090f] [03820985a569] [c218585e29e4].

**R53. Do not name and pitch the product right after the hook.** The bridge is where most ads break. Weak: "The solution is our product, here are the benefits." Strong: "The solution to this is simple", a brief glimpse at most, then why the problem happens. 04: bridge into education the viewer values, not into the product; "this is the biggest mistake that people make". 13: FU2's bridge "how do you know who to trust? That's why I started taking FU2" is "too early, too aggressively"; add a research or supplier story first. 11: bridging to the product right after the intro is "where most people mess up VSLs". Condition: every cold video; the ad-level fix when hold rate is low (R99). Sources: 01, 04, 09, 11, 13. Cards: [c218585e29e4] [b7e6d1e3ad02] [09fddf695faa] [2370029af17b] [94e95729b482].

**R54. Keep product awareness near 0 through the hook and let it rise slowly to a peak at the CTA.** 04's curve: no product name, no product on screen, no sign of an ad in the hook; a small bump in the body followed by more teaching is acceptable; do not "stepstone" up at each section. 01: introduce the product as late as possible in top-of-funnel video; later introduction gives fewer but more qualified viewers and, per 01, more total purchases; a low-testosterone ad reveals at about 1.5 minutes. 13: product off screen, out of the first words and out of the top of the primary text for top-of-funnel hooks. 18: hook first, product and CTA in the middle to back. Exceptions the sources give: a product-first opener is fine as a partnership ad on the influencer's own page (09); a demo format can show the product working in the first 3 seconds (02's dishwashing example); product-aware and retargeting ads can lead with the product (13). Condition: cold video; test early vs late in the brand's own account before making it a law. Sources: 01, 02, 04, 09, 11, 13, 18. Conflict: C1. `[needs brand data: hook rate, hold rate and CPA for product-early vs product-late variants]`. Cards: [3ae52427e9c8] [0efe34c9febc] [cb664cb20762] [03820985a569] [2a76fe7e97e3] [c75046cd85fd] [7c2ba984d570] [a9237fc18657].

**R55. Explain the mechanism, the "why", before naming the product, at the depth the target stage needs.** Problem-aware viewers need what the mechanism is, why it fails and why that causes their problem; solution-aware viewers already know it and need reinforcement, difference and offer. An ad that asserts a cause ("NAD levels dropping") without the why is a solution-aware ad, not a problem-aware one. Every ingredient or feature gets a reason it matters. Condition: education-led video and VSLs. Sources: 11, 12, 13. Cards: [4e1cb65d14b8] [2370029af17b] [dda332d2d5b2] [8cfd832f085a] [2656d0241771].

**R56. After naming a condition or term, prove the viewer likely has it and explain it.** "This is dysbiosis. 40% of people have it. Most of them don't even know" grows the perceived market and makes the viewer self-identify; a clinical word dropped and left makes viewers think "I definitely don't have that". The prevalence line must be a true, sourced figure (override 2). Condition: any script that names a condition, mechanism or technical term. Source: 13 only. `[needs brand data: sourced prevalence figure]`. Cards: [2656d0241771] [4f6f2e7601e9].

**R57. Make the claim, then show the proof immediately.** 02's analysis of its top 15 founder ads: none worked on a claim alone. 09: "$50,000 of testing" and "7 times the toxins" with no results on screen are just assertions; overlay the actual test results or cut the claim. 10: for every claim in the script, write the shot that proves it (compact: show the room still has space; quiet: film a call and zoom out; a number: show the real number). Condition: every claim in voiceover, copy or overlay. Sources: 02, 09, 10. Cards: [acb7fe437e41] [c57792ab090f] [d3ac75d0d660] [306f74067bdf].

**R58. The 7-part order is a starting point. Move sections and test.** 11's 2 example VSLs both break the order (mechanism before problem; objections before mechanism) and still ran. Modular edits 11 names: mechanism before problem, objections earlier, problem agitation pulled forward (from about 15 to 20 seconds), a faster mechanism section (from about 30 seconds). 13 would add 4 to 6 seconds of mechanism before the product in an ad it calls "incredible". Condition: any long-form script iteration. Sources: 11, 13. Cards: [053dc07009fa] [c5a32b550f4d] [94e95729b482].

**R59. Handle at least 1 real objection inside the script before the CTA, from customer data, not guesses.** Sources of objections: reviews, tickets, surveys, call recordings, abandoner calls (R13, R26). Forms the sources praise: "it's not a hair mask, it's not a magic pill"; taste as reason 3 in a numbered list; the self-image objection said out loud in the creator's voice ("I don't want to look like a gamer boy") then repositioned ("luxury without losing functionality") with a reason (Japanese design); what they already tried and why it failed (squeezing, salt water, tongue scrapers). A very specific objection story narrows the audience; use it when that group is large enough. Condition: every cold video. Sources: 09, 11, 13, 02. Cards: [cac9faff0225] [dc0bcc2c4ae1] [4fb56bc1019f] [10c228fa0ec1] [ef1959f490cb].

**R60. Say the benefit first and the feature second, and move fast through table-stakes features.** "I can even lie down and have a 30-minute nap because the armrests go down" beats "the armrests go down". Dairy-free, gluten-free, plant-based get 1 quick line, not the whole ad; keep any compliance-required statement. Condition: any script that names features. Sources: 09, 13. Cards: [cac9faff0225] [10c228fa0ec1].

**R61. Stack proof after the product and keep the proof consistent with the viewer.** 13's IM8 close: 12-week trial percentages, then "92 nutrients". 11: UGC, influencers, testimonials, customer count ("80,000 plus customers"); weak or buried proof is "a really common and easy way to fix an underperforming VSL". 01: proof must fit the persona's age and gender. 02: product experience is not a founder moat; carry it with customers who look like the viewer. Condition: after the product reveal in any long-form script. Sources: 01, 02, 11, 13. Cards: [a48f56ddf075] [dda332d2d5b2] [087eee279056] [b27bfdea1a9c].

**R62. Give the viewer a reason to move from learning to buying, then a clear CTA with a risk reversal, and never leave a curiosity loop open.** 04: a strong ad "flops a lot of the time" because it jumps from education to the offer with no reason. 13: FU2 "bridged very aggressively and then just ended"; keep going into benefits, proof and offer. 02: a CTA that opens a new loop ("forget everything you know about pea protein") bridges nowhere. 11: "Skeptical? Good. With every single order, you get 90 days to test it yourself." then "Get yours in the link below"; keep the CTA on a first VSL. Condition: the last third of every script. Sources: 02, 04, 11, 13. Cards: [b7e6d1e3ad02] [89a475819a6d] [69e259507ec7] [b8868a83a786] [dda332d2d5b2].

**R63. Match the CTA's intensity to the tone and to the work the ad has already done.** 09: after heavy education and objection handling, a soft close ("Your halo is waiting for you"; "invest in a comfortable working experience") fits, and a hard pitch bolted onto a soft creator ad "would be very odd"; on a weak script a soft CTA only adds friction. 11: keep the CTA simple and clear. 07: a convincing native static may carry no CTA in the image (R50). Scarcity only when it is true (09's "before stock runs out" ran 20 weeks). Condition: writing the close. Sources: 07, 09, 11. Conflict: C6. Cards: [129eda6e1e3a] [dda332d2d5b2] [4e47f314df0c].

**R64. The first half decides the ad. Fix the opening first and keep a usable back half.** 09: "probably only 15% of people even get to the second half"; a good first half carries an average second half, the reverse does not. 13: diagnose hook, bridge and body apart, name 1 weakest segment, keep the strong ones, build a variant that changes only that segment. Condition: any underperforming video. Sources: 09, 13. `[needs brand data: retention curve per ad]`. Cards: [66dd24ac26be] [2a76fe7e97e3] [09fddf695faa] [89a475819a6d].

**R65. A good script still fails with no motion. Add cuts, overlays, B-roll and camera moves; the cut rate depends on the format.** 09: cut at least every 3 seconds, stressed for Instagram; a talking-head back half with no cuts and no social proof reads "very salesy". 13: a static, unmoving talking head through a long script "drops people"; at minimum add overlays, a few cuts and handheld push-pull; the "every 3 seconds" line in 13 is a header note, not the presenter. 02: never run an unedited talking head; use 2 cameras and motion; the exception is a famous founder. 18: native TikTok videos are raw storytelling and demos that do not look like ads. 13 and 18: a native setting (a car, a home) reads as content; a visible studio rig reads as an ad. Reconciled rule: every video needs visible motion and change; a polished ad format cuts every 3 seconds or faster, a lo-fi native UGC format keeps fewer cuts but still moves (props, handheld, B-roll, on-screen text) and never sits still for a long script. Condition: every edit review. Sources: 02, 09, 13, 18. Conflict: C7. Cards: [66dd24ac26be] [82b6f200aecd] [bb2386f4df37] [03820985a569] [2ef96388e6ab] [b7e6d1e3ad02].

**R66. Low-fi opening footage does not damage a premium brand if the product is not shown in it.** Show the product later in high-end shots so the contrast reads as intent, not cheapness. Condition: premium brands using raw founder or problem footage. Source: 02 only. Cards: [a9237fc18657].

**R67. Sell the category when the category has a strong story, and borrow authority when the brand has no famous face.** Category history ("invented thousands of years ago in central Europe"), licensed brands, design origin ("designed in Japan") all work for a category-defining or unfamiliar product; they do little for a commodity that looks like its rivals, and origin-as-premium depends on era and culture. Condition: unfamiliar or category-defining products. Source: 09 only. Cards: [09fddf695faa] [e17eff7e3b5c].

**R68. An ad must reach past the founder's or creator's organic reach.** If the ad only converts people who already trust the face ("if you change the avatar to someone else, this ad would 100% not work"), post it organically instead. Swap-the-face test: would it still work with a different person? Condition: founder and influencer ads on cold audiences. Source: 09; 02 disagrees on founder ads' value. Conflict: C11. Cards: [d3ac75d0d660].

**R69. Remove AI-script tells, above all contrast negation.** "Your gut isn't broken, it's starving" and "not a single soldier, a complete military operation" are giveaways of an AI-written script. Add the standing line "do not use contrast negation" to every AI script request and search drafts for "isn't ... it's" and stock war analogies. Condition: every script draft, AI-assisted or not. Sources: 01, 13. Cards: [ba72533dddbc] [156808a7c843].

**R70. Match word precision to the audience's expertise.** "Three simple ingredients: electrolytes, magnesium, and creatine" fails with athletes because magnesium is an electrolyte. The more expert the persona, the less forgiving the copy; have a category expert read expert-facing scripts. Condition: expert or enthusiast personas. Source: 13 only. Cards: [4f6f2e7601e9].

**R71. Click the live ad. The destination must load and hold what the ad promised.** 09's Blueprint ad pointed to a 404 for the lab results it promised. 11: a VSL "won't work if you're just dropping to a product page that has no continuity"; each VSL gets a page that continues its mechanism and story. 03: the lander's offer must be "directly congruent" with the ad ("less shedding in 26 days or less"). Condition: before launch and on a schedule after. Sources: 03, 09, 11. Cards: [8cce5e9474f5] [9d1aae2f4dcb] [4a4cc4147dbc].

**R72. Use a numbered-reasons body for routine or consumable products.** Curiosity hook that promises an answer; answer it within seconds; "here are 3 reasons": reason 1 a felt benefit, reason 2 the table-stakes value props fast, reason 3 the main objection; CTA to the bundle. Condition: consumables with a wide market. Source: 09 only; 05 lists "3 reasons why" as a problem-aware format. Cards: [ef1959f490cb] [d2e3d5f918af].

### 3.6 Hook craft

**R73. The hook is a promise of relevance with 2 jobs in order: make the right viewer stop, then keep them past the first seconds.** Most sources put 80% of viewers (19: 80% to 90%) dropping at the hook; none measures it. Whoever is in the hook must be the target buyer and the hook must relate to what follows. Bait (memes, a knife stabbed into the product, a hammer on a table) wins attention from the wrong people and loses the right ones. Condition: every paid hook, video or static. Sources: 01, 04, 09, 11, 13, 19. `[needs brand data: hook rate and drop-off curve per ad]`. Cards: [6ce954d6297e] [aaacbb3da60f] [b3dd2d5c796e] [8e0335ccf918] [556ea817b608] [2e9838db8377].

**R74. An irrelevant hook teaches delivery to find the wrong people.** 04: Meta optimises toward soft signals "to a degree"; if off-topic viewers hold, Meta serves more of them. 08: unqualified clicks that bounce still train the pixel. 13 (card wording): bad hooks feed bad data. 04's paid vs organic economics: a broad off-topic reel is fine organically because reach is free; buying 2 to 10 million views costs about $500,000, so 10 leads is a disaster. Condition: paid delivery; the mechanism is the presenters' belief, not Meta documentation. Sources: 04, 08, 13. `[web check: how Meta weights engagement signals after the learning phase]`. Cards: [aaacbb3da60f] [a932cc43b8da] [8e0335ccf918].

**R75. A hook has 3 layers: audio (what is said), copy (text on the creative, and the primary text above it), visual (what is shown).** Most people only think about the visual. A hook that is "doing okay" can double by fixing 1 weak layer (04's anecdote: adding the overlay "this transformed my life" doubled hook rate). A written hook handed to production without a visual plan can fail and get wrongly blamed. Condition: writing, briefing and diagnosing hooks. Sources: 01, 04. Cards: [6ce954d6297e] [98385b907b9b] [a535c8449dc1] [227f69979a61].

**R76. Grade every hook in this order: clarity, relevance, novelty, then specificity and credibility.** Clarity: a stranger understands what it is within 3 seconds. Relevance: the pain is obvious and the viewer can relate the product to themselves. Novelty: has this been done a million times? Specificity: numbers, names, outcomes. Credibility: proof or a reason to believe, hard to fit in 3 to 4 seconds, cheapest through who delivers the hook (a doctor for supplements, a runner for running gear). A couple done well is enough; low clarity plus low relevance fails whatever the novelty. Condition: every hook before launch. Sources: 01, 04; 09's cards repeat the list. Cards: [f994209714f5] [6d6308f42500].

**R77. Pick from a hook-type menu, avoid the overused types, and know which fit ecommerce.** 01's 9: problem agitation (problem-aware viewers only), contrarian truth (works across stages), specific proof ("I lost 12 kilos in 90 days without giving up pasta"), curiosity gap, truth bomb on price or ingredients (premium products where price is the objection), psychological confrontation, sensory or ASMR (2 to 3 seconds, no words; strong in fashion), founder's letter with real stakes, social proof ("90% of customers saw results in 30 days", substantiated). 04's 7: contrarian truth, specific proof, common mistakes (overused, "lost its weighting"), high-stakes warning (he uses it "a lot in ecom"), curiosity gap, tactical promise ("doesn't really translate into ecom"), mythbusting objection. 09: high-stakes warning and curiosity question that open a gap and answer it; if you cannot name the hook type, there is no hook. Condition: hook ideation; about 7 of 01's 9 fit most brands. Sources: 01, 04, 09. Cards: [10686d689660] [9197d49f4af4] [b3dd2d5c796e] [2a76fe7e97e3] [20656fe8bb82].

**R78. A working first-draft template: Persona + Problem + Pattern interrupt + Promise.** "If you're [persona] and you have [pain], you're probably doing [common approach]. That's why you're getting [bad outcome]. Here's the better method." Agitate the pain within about 2 seconds; the interrupt keeps viewers who sense an ad coming; the speaker must plausibly be the persona (no 50-year-old mom addressing 20-year-old guys). Frameworks are a start, not the end state; move to writing from scratch and to white space once you can tell a good hook from a bad one. Condition: teams learning hooks, and volume generation with an LLM. Source: 04; 01 agrees on frameworks vs novelty. Cards: [21dee8ebaffe] [20656fe8bb82] [10686d689660].

**R79. Agitate the viewer's problem rather than calling out their demographic, but a problem call-out that names who has it is fine.** 01: persona call-outs are "super overrated"; people skip "agency owners who need X, listen up" and watch a hook about their exact problem. 04, 08 and 13: open with who it is for ("if you're using protein powder, you're slowly destroying your gut"; "you have IBS, leaky gut, or bloating"), because whoever the ad talks about is who delivery finds. The reconciled rule: the call-out must carry the problem; a naked demographic label without a pain does not qualify anyone. Condition: hook writing. Sources: 01, 04, 08, 13. Conflict: C9. Cards: [f994209714f5] [d8253f20d2a9] [21dee8ebaffe] [72f6438afa3a] [51a88883a763].

**R80. Specific beats vague, and the specific must be true.** "Found the same 2 problems" beats "found the same problems"; "3-second label check" beats "quick check". Condition: any concrete figure in a hook (R43). Sources: 04, 01. Cards: [0ac3b2659983] [f994209714f5].

**R81. Do not sell in the hook.** No product name, no product on screen, no offer in the first line of a cold ad; open an educational payoff. Condition: cold video; product-aware ads are exempt (R54). Sources: 04, 13. Cards: [a535c8449dc1] [46035a697541] [cb664cb20762].

**R82. Curiosity is allowed only when it is qualified by relevance.** 13 rejects the knife hook and praises "the heat used in manufacturing destroys the creatine inside" and a famous face with "NAD+" and "peptides" on screen: both open a gap and name the viewer's world. 18: curiosity, controversy and mystery engage more, and teasing the result without showing it drives views for transformation products; 18 also admits the same format works when the before and after is shown. 16: light products can use humour and in-group jokes as the curiosity. Condition: hook writing; for statics the destination page absorbs junk clicks (R34). Sources: 09, 13, 16, 18. Cards: [8e0335ccf918] [2ef96388e6ab] [91a9091b2a20] [84a55aede410].

**R83. Write hooks in 4 steps: isolate the idea, commit to it, deep fry it (contrast, surprise, novelty, nuance, stakes), make it bang (trigger words, simple language, best information first, open loops).** 12's example turns "magnesium cream absorbs through the skin" into "naked magnesium". Any claim inside the hook ("fixed her back pain in 2 weeks") still needs proof. Condition: hook drafting when the mechanism is known. Source: 12 only. Cards: [85ea7dc45ab8].

**R84. Assume the viewer decides in well under 3 seconds.** 16: about 0.5 seconds on the feed, "a lot of the data says 3 seconds, I would 100% disagree". 01, 04, 09 and 19 work to a 3-second or 3-to-5-second window. Reconciled: the first frame and first words must give the target buyer a reason to stop; the 3-second hook rate is a reporting window, not a licence to warm up. Condition: every hook. Sources: 01, 04, 09, 16, 19. `[web check: Meta's current hook-timing guidance]`. Cards: [84a55aede410] [aaacbb3da60f] [6ce954d6297e] [c8317f1a2291].

**R85. Novelty is what lets an ad hold very large spend.** Standard hook types can build an 8-figure brand; an ad that holds $500,000 usually needs something novel up front, and competitors then copy it. "Purple ocean": adjacent to proven demand but different in look. Condition: when planning hooks meant to scale, not first tests. Source: 01 only. Cards: [f994209714f5] [10686d689660].

**R86. A famous face or trending term in the hook adds credibility, but clear the rights first.** 13's presenter is "not sure" of the legal risk and notes brands "seem to get away with it". Under ecomOS override 4 and 5, no likeness without permission. Condition: authority hooks. Sources: 04, 13. `[web check: right-of-publicity and Meta policy on public figures in the market]`. Cards: [2ef96388e6ab] [6d6308f42500].

**R87. Add a visual hook (on-screen text such as a POV line) as well as the spoken hook.** 09 praises "POV, you finally find a chair that meets all your sitting needs" and notes the other 2 good ads had no visual hook. Condition: video hooks. Source: 09; 01 and 04 count on-screen copy as a hook layer. Cards: [dc0bcc2c4ae1] [129eda6e1e3a] [98385b907b9b].

### 3.7 Hook testing and variation

**R88. Hook testing still works under Andromeda when the hooks are truly different.** 01: a new hook gets its own creative ID and reaches some new audience; 50 new hooks on ads that had spent $50K to $100K spent another $100K at the same efficiency. 02: hook variations and reused scripts with new scenes work "even under Andromeda". 19: 1 case revived with new hooks from a different person now holds the top 2 spots. 03's counter-view: slight variants are grouped and wasted. The condition that reconciles them: each hook must change angle, offer, avatar or format (19's levers), or the visual layer, not just wording. Condition: any hook test plan. Sources: 01, 02, 19. Conflict: C2. `[web check: Meta's current statements on creative similarity grouping]`. Cards: [2f44cbccd498] [d0761aaedfd8] [2d5a90d21b0d] [d6f4dfaaf4c4] [ec923b82af65].

**R89. Put production time into hooks over bodies, once the body script is good.** 01: 2 bodies x 15 hooks beats 2 hooks x 5 bodies in the same hour, because the performance gap sits in the hook; if scripting is weak, 1 lucky body distorts the learning. 19: 10 versions of a 3-to-5-second hook cost about as much as 1 body of a 75-second video. 11: build body and CTA once, then test hooks. Condition: video production planning. Sources: 01, 11, 19. Cards: [dd35cdd74a75] [59cf922e4996] [556ea817b608].

**R90. Shoot many hooks, launch them in waves sized to the budget.** Shoot: 01 records each hook about 6 times; 02 shoots 10 hooks x 3 bodies (30 ads) in 4 to 5 minutes of camera time; 19 targets 10 per body. Launch: 02 launches 2 to 4 hooks per body, up to 8, because $1,000 a day across 3 variants tests better than across 20 to 40; 11 runs 3 to 6; 19 says 3 is usually too few. Strictest reconciled rule: never launch more hooks per body than the ad set's budget can take to a read; 02's 2 to 4 (max 8) per body per wave; keep the rest for the next wave or the revival (R150). Condition: every hook test. Sources: 01, 02, 11, 19. Conflict: C10. `[needs brand data: daily budget per ad set and target CPA]`. Cards: [2f44cbccd498] [29d159fbe711] [d0761aaedfd8] [556ea817b608] [59cf922e4996].

**R91. Vary hooks on 4 levers: angle, offer, avatar, format.** Angle: the messaging or context (seasonal framing). Offer: often lives in primary text and headline (bundle, sale). Avatar: who delivers it, a clearly different profile. Format: a 3-second static or motion-graphic intro before the video. Change 1, 2 or all 4; pair any combination with volume. Wording changes bring some viewers in; visual changes are needed to reach the rest. Condition: planning hook variants for a proven body. Source: 19; 04's visual, copy, audio layers overlap. Cards: [ec923b82af65] [876d09a8a01a] [227f69979a61].

**R92. Turn 1 strong audio line into 20 to 30 variants by changing the visual, the on-screen copy and the audio separately.** 04's example: the same line "we taste tested the bestselling jerkys and found the same 2 problems" as a plain talking head, then with a supermarket sweep cut at about 1 second and a whiteboard reveal; overlay headlines at different severities for different pools (checked against claim rules). Condition: volume from 1 concept. Source: 04 only. Cards: [227f69979a61] [98385b907b9b].

**R93. Every hook must bridge naturally into the body it sits on.** "10 years ago this happened to me" cut to an unrelated body is "a big issue". Write only as many hooks as can bridge. Condition: hook-by-body matrices. Sources: 02, 04. Cards: [bb2386f4df37] [d0761aaedfd8] [b7e6d1e3ad02].

**R94. Do not spend test budget on CTA variants unless a volume target demands it.** Average watch time means almost nobody reaches the CTA. Condition: video tests. Source: 02 only. Cards: [29d159fbe711].

**R95. Read hook rate and hold rate as diagnostics, not as winners.** Hook rate (viewers past 3 seconds) low against the account average: swap the hook and see if the body works. Hold rate (viewers past 15 seconds, 1 of several definitions) low: viewers drop at the bridge; redo that section. Neither correlates with conversions. 09: high 3-second views with poor hold and poor conversion point to a confusing hook. Condition: any video read. Sources: 01, 09, 04. `[verify UI: Meta video metric names]` `[needs brand data: account average hook and hold rate]`. Cards: [8d71a067a46c] [f4aee117fef5] [b7e6d1e3ad02].

**R96. Validate hooks and rough cuts as trial reels before paid, where the brand has the page.** 01 (as of April 2026): cut the CTA, post as a trial reel on the page the ad will run through, read reach and the retention graph, feed into the V2 edit within 24 hours; post about 20 hook variants, keep the best, launch about 5 as ads. Condition: brands with an active Instagram presence; organic mechanics live in 13-ORG. Source: 01 only. `[verify UI: trial reels availability]`. Cards: [514bd1dc3fea] [4346adb6eca1].

**R97. A quick hook test can move a strong line from mid-ad to the start, if it still makes clear what the ad is about.** 09's roofing ad did this and lost relevance. Condition: cheap tests on existing footage. Source: 09 only. Cards: [f4aee117fef5].

### 3.8 Founder ads, UGC and native short-form formats

**R98. A founder ad presents the founder's argument. It is not a video of the founder talking.** Raw iPhone footage of the founder chatting is the common failure; "authenticity, authority, trust" is the format's gift but "if this is all you take away, it's over". 99% of the work is scripting and ideation; filming 30 ads takes 4 to 5 minutes. Condition: every founder ad. Source: 02 only for the framing; 09 and 13 apply the same script tests. Cards: [bd02cb579cd7] [59b1c68249c2] [29d159fbe711].

**R99. Use the top-performing founder structure: claim (usually adversarial, doubles as the hook), proof of the claim at once, unique mechanism tied to the founder story, proof of the mechanism, CTA plus social proof.** 02's basis: the most common structure in its agency's top 15 founder ads by spend; none of them worked on a claim alone. Put hooks in front of this body; do not rewrite the body per hook. Condition: founder video bodies. Source: 02 only (1 agency's ranking, KPIs undefined). Cards: [c57792ab090f] [acb7fe437e41].

**R100. Build the founder story from the 3 things only a founder or expert can own: origin, mechanism, adversarial angle.** Product experience is not a founder moat; carry it with customers who match the viewer. Split the story into static parts (origin, personal problem) that must stay consistent, and renewable parts (reviews, emails, supplier news, 1-star reviews, complaints) that feed new scripts every week. Condition: founder ad planning. Source: 02 only. `[needs brand data: true origin facts, lab or supplier proof, review and inbox feed]`. Cards: [bd02cb579cd7] [b27bfdea1a9c] [fb523fb2f4cd].

**R101. Tell the story through the viewer's eyes. Nobody cares about the founder.** Open on a problem the viewer has lived, agitate, open a curiosity gap that the founder solved it, walk through the mechanism, close the gap. Founder-only stories "sometimes work, but majority of the time people don't care". Condition: the first 1 to 2 minutes of any founder ad. Source: 02; 09 adds the swap-the-face test (R68). Cards: [59b1c68249c2] [6db074412846] [d3ac75d0d660].

**R102. Never invent or alter a founder story, and never present a scripted review or email as real.** 02 calls invented stories "black hat" and says they hurt exit value; the same source's "we're scripting the 1-star review in a way, or it's a real review" is rejected under override 4. Use only real reviews and emails, with permission. Condition: always. Source: 02. `[web check: fake review and testimonial rules in the market]`. Cards: [59b1c68249c2] [fb523fb2f4cd] [289897a2c363] [4098dd29a9fa].

**R103. The founder's face is the strongest sameness signal in the account. Diversify concept and format around it.** Format levers, cheap to expensive: reshoot the same script in a new scene (02's case: gym to outside the gym gave another $40,000 of spend), new formats (tier list, store-aisle walk), move down the involvement spectrum (protagonist, voice over B-roll or animation, evidence such as lab photos, proxy such as a dietitian or supplier, absent such as animation or claymation), change the script role (protagonist "I built this", witness "a customer emailed me", interviewer "I asked our lab why", reader "I just got a 1-star review"). Concept levers: offer (easiest), angle, persona (hardest; only with true stories). Condition: founder ad refresh and volume. Source: 02 only. Cards: [73f8f845b93b] [713723220d75] [51c9b7fece1b] [289897a2c363] [e52028da9a2d].

**R104. Batch-shoot founder ads as a hook-by-body matrix and run a monthly collection pipeline.** 3 bodies that tell materially different stories x 10 hooks = 30 ads; 2 endings for 60 only to hit volume; shoot general content monthly and the founder about quarterly in about 1 hour; pipe reviews and the support inbox into a database and pull ad-relevant items weekly. Condition: any brand running founder ads at volume. Source: 02 only. `[needs brand data: current creative volume and mix]`. Cards: [29d159fbe711] [254ef036ab38] [d0b9623db467].

**R105. Founder production rules: fast dynamic editing, 2 cameras for talking heads, move around during the shoot, let a weak teleprompter reader talk off a sentence outline, expect the first 10 hours on camera to sound robotic.** Do not conclude "founder ads don't work for us" from robotic first takes. Condition: founder shoots. Source: 02 only. Cards: [bb2386f4df37].

**R106. Run founder ads through the founder's handle as a partnership ad only when that page posts often and relevantly; otherwise use the company page.** 02: expected lift 5% to 30%, not 10x; he has "almost never seen" the company page beat the founder partnership ad when the page qualifies, and defaults many brands to the company page. 01: partnership ads use both handles' audience data, feel less like ads, reached 40% of spend in some accounts, and the edge is "probably coming towards its end". 07: partnership ads work as statics too. 09: product-first openers and soft CTAs fit partnership ads. Condition: founder or creator content; disclosure rules apply (3.16). Sources: 01, 02, 07, 09. `[verify UI: partnership ad setup]` `[web check: partnership ad performance and disclosure rules]`. Cards: [7c9fa26551de] [6560e7ff8a96] [646aacb0f2a9] [37c10bda4253] [7c1f89cbddee] [129eda6e1e3a].

**R107. Founder ads are optional but human presence is a counter to AI creative.** 02: a $200M fashion brand does not need the founder to reach $300M, but good founder content "will perform better", and a real person is "particularly missing with all of the AI creative that's flooding" accounts. 05: run in-house founder and behind-the-scenes content as the trust pillar; "a lot of people say you shouldn't make founder story ads, I totally disagree". 09: founder-reliant ads cap at the founder's organic reach. Condition: brand and founder fit, checked against brand voice; 2 of 3 sources are opinion. Sources: 02, 05, 09. Conflict: C11. Cards: [b27572e198f4] [ec40d606be63] [e7ff1f72cfb2] [d3ac75d0d660].

**R108. "UGC" is not a concept. The script, persona, angle and offer inside it are.** 01: "UGC as a concept doesn't work"; teams that test format first learn nothing. 05: the UGC pillar gives volume and authenticity that AI cannot, and cannot give warehouse, behind-the-scenes or founder content. Condition: every UGC brief carries a concept (R1). Sources: 01, 05. Cards: [4a3ce680ae23] [f06f1f445e76] [7ef548d9c0df].

**R109. Brief creators in detail by default, allow 2 takes, and vet them by the briefs behind their past work.** 01: ask for past work and the brief behind each piece; a great result from a thin brief means broad strokes are fine, a detailed brief behind it means you must match that depth; 1 take held to the script and 1 natural. 05's 2 brief types: wide (product only, let the creator tell it) for discovery, specific (show the top ads with their numbers, "go make ads like these") to multiply winners. Condition: every creator brief. Sources: 01, 05. `[needs brand data: which ads are top performers, with spend and ROAS]`. Cards: [f94a2801c0ad] [58ba8efa52c9].

**R110. Use native-accent creators for each market.** Same script, local creator: an Australian accent into the US does poorly, UK to Australia translates "decently", native always wins (01's observation). Condition: multi-market brands. Source: 01 only. Cards: [f94a2801c0ad].

**R111. Source creative from 3 pillars and blend their speeds: in-house (trust, control, about 30 minutes to a few hours per asset, least scalable), UGC creators (volume and authenticity, 1 to 4 weeks lead time), AI (angle tests in minutes for a few dollars, weak on trust).** 05's 33% split is a starting heuristic, not a measured optimum. Winners from 1 pillar feed the other 2 (the flywheel): a UGC angle wins, tell the creators, derive statics, make in-house and AI versions. Condition: planning supply for a monthly batch. Source: 05 only for the split; 15 and 17 describe the same flywheel. Cards: [7ef548d9c0df] [c7a8123193e9] [9e6943f760aa] [e7ff1f72cfb2] [9395469a9874].

**R112. Build a standing creator army rather than a few creators, and secure usage rights before any paid use.** 05: mass invites to TikTok creators across ages and niches, ship samples (about 7 days), ask for 2 to 3 videos per sample, expect 1 to 4 weeks and some who never post, run a creator community that learns what wins, reuse the army for every launch; 1 case reached 6,000 creators and about 5,800 videos from 100,000 invites in 60 days (under 1 video per creator). 18: 1 video runs as organic, affiliate and paid, which needs rights and affiliate terms the source never covers. Condition: brands whose category and margin support seeding. Sources: 05, 18. `[web check: seeding tools, TikTok and Meta rules on creator content in paid]` `[needs brand data: creator rights, affiliate terms]`. Cards: [f06f1f445e76] [c7a8123193e9] [03820985a569] [e897b3068f2a].

**R113. Split an ad into an EGC hook and a CGC body when reviving a testimonial.** A brand-side person films a new 3-to-5-second opening that talks about the testimonial, then cuts into the unchanged customer testimonial. Condition: fatigued testimonial bodies (R150). Source: 19 only. Cards: [8fa61a97ae26] [c8317f1a2291].

**R114. Leaving the founder or influencer out of an ad can open a new demographic.** A creatine static without the male influencer, showing a woman holding the gummies, opens the product to women. Condition: influencer-led brands whose ads skew to the influencer's audience. Source: 07 only. Cards: [7c1f89cbddee].

**R115. Native short-form video should not look like an ad and should be relatable in the first line.** Raw storytelling and demos, a creator or founder talking to camera, the buyer's own habit or annoyance in the opening ("I'm a foodie"; "if you see a lot of dust"). Condition: TikTok and Reels creator formats. Sources: 18, 13, 02. Cards: [03820985a569] [e897b3068f2a] [2ef96388e6ab] [bb2386f4df37].

**R116. Pick a native format from the 7 by product trait.** Strong sensation or visible change on first use: reaction (only when the response is "a magnitude higher" than normal; skip otherwise). Buyers use a flawed rival: problem/solution comparison (show a generic "old way" failing, not a named rival, under 3.16). Aspirational result that takes time: transformation teaser (tease or show the result; 18 allows both). A category full of wrong beliefs: misconception with a credible source (check the source before citing). A consumable tied to a recurring annoyance: free tip or secret narrative. Something surprising in use: comment-reply demo. A product that restricts a desire: "don't do this if you like this". Condition: format selection for creator briefs; the map is a card synthesis, not the presenter's rule. Source: 18 only. Cards: [2eae62f9a017] [01058f4f2412] [c7c5b8ef2ed7] [91a9091b2a20] [de0b0ea997a3] [bea60e1a6e4a] [52eb399debbc] [e897b3068f2a].

**R117. Views are not sales. Demonstration quality drives sales.** 18's own example: 34.5 million views for 13,000 units; the highest-view video had the lowest units per view. Judge a creator video on purchases per view, not reach. Condition: any TikTok or Reels read. Source: 18. `[needs brand data: views, orders and revenue per video]`. Cards: [c7c5b8ef2ed7].

**R118. Turn comment questions and disbelief into the next video.** Reply on video to a comment with many likes ("what is this sorcery"), demonstrate visually, link the product, then run the reply as an ad. Condition: videos that draw questions. Source: 18 only. `[verify UI: TikTok comment-reply distribution]`. Cards: [52eb399debbc] [de0b0ea997a3].

**R119. Use format innovation on the video side too, and keep the visual style consistent inside 1 ad.** 12: formats trend (whistleblower, timeline, personification, "Wall Street Journal style"); 02: animation and claymation are "kind of a new format" and let the founder be absent; 11: mixing AI UGC, real UGC and animation in 1 VSL "comes across a little bit scammy", so lean UGC or lean animation. Pretend formats (fake interview, fake whistleblower) are excluded under override 4. Condition: choosing video conceits. Sources: 02, 11, 12. Cards: [10b56ec55756] [713723220d75] [8e86c45ad8e2] [765ed4cbcc9c].

### 3.9 VSLs and advertorial funnels

**R120. Make a VSL only when the buyer needs education to convert.** 11's 3 cases: a complicated product, a low-trust category, a new category or ingredient; a 4th signal is top-of-funnel conversion capped because buyers do not understand the product. 01: VSLs for education-heavy products; 2 of the top single-ad revenue buckets 02 has seen are VSLs and founder ads. Condition: format decision; do not make a VSL because it worked for a supplement brand. Sources: 01, 02, 11. Cards: [1567d2668c63] [156808a7c843] [684258aed19c].

**R121. Script the VSL in 7 parts: hook, problem in the customer's words, mechanism, objection handling, bridge to product, proof, risk reversal, CTA.** The hook calls out who has the problem and is never a brand story; the problem section uses educational agitation and does not name the product; each ingredient or feature gets its why; objections come from customer data. 13's model for the first 30 to 40 seconds: persona call-out on 2 to 3 related conditions, curiosity line, agitation through failed fixes, reframe the cause, name the condition and prove prevalence, attack past solutions, then 4 to 6 more seconds of mechanism before the product. Condition: any VSL draft; the order flexes (R58). Sources: 11, 13. Cards: [583ab7df2aaf] [556ea817b608] [2370029af17b] [4fb56bc1019f] [a48f56ddf075] [2656d0241771].

**R122. Length is not the lever. Start short, then go longer, and cut lengths as extra variations.** Good VSLs run from about 90 seconds to 20 minutes (13: normally 3 to 4 minutes); a 6-to-10-minute master cuts to a 2-to-3-minute and a 45-second version. Do not start with a 60-minute script. Condition: VSL production. Source: 11 only; 13 gives the 3-to-4-minute norm. Cards: [583ab7df2aaf] [c5a32b550f4d] [1567d2668c63] [a48f56ddf075].

**R123. Judge VSL economics on repeat purchase, and design for older viewers.** 11's account runs about 2.5 to 3 ROAS on new customers with "pretty much all of the money on second, third purchase" and a 150% profit lift after year 1; VSLs "perform better with older age demographics", so text must be large and pacing quick. Condition: brands with strong repeat purchase; a 1-purchase product may not survive 2.5x. Source: 11 only. `[needs brand data: repeat rate, 12-month value, break-even ROAS]`. Cards: [9d1aae2f4dcb] [23116e553dcf] [dda332d2d5b2].

**R124. A no-CTA VSL (pure top of funnel, retarget viewers past 25%, or push to Amazon search) is not for a first VSL.** Keep the CTA on the asset and the retargeting simple. Condition: first VSLs. Source: 11 only. `[verify UI: video-view custom audiences]`. Cards: [b8868a83a786].

**R125. Advertorial and listicle funnels work only with an education-based page or heavy education in primary text.** 01 and 03 both admire a hair-growth "best products of 2025" roundup run from a dermatologist page to a brand-owned ranking site. Under override 4 the brand-owned site must not present itself as independent, rivals must not be shown with fake ticks and crosses, and paid relationships must be disclosed. What transfers: the static plus long copy plus a real educational page plus a quiz. Condition: cold curiosity statics. Sources: 01, 03, 04. `[web check: native advertising, endorsement and review-site rules in the market]`. Cards: [95a5ffb79c86] [1620b9b6a2e3] [9197d49f4af4].

### 3.10 Creative volume, portfolio and production budget

**R126. Run a portfolio, never 1 to 3 hero ads.** Every creative fatigues and has a maximum spend threshold. 01: 8 to 10 clients arrived 40% down year on year after building 8-figure businesses on 3 creatives holding $1M; that needed fixing 6 to 8 months earlier. 02: brands rode 1 founder ad plus hook swaps to $20M to $30M and then decayed. 05: variants of 1 winner end with all spend in 1 to 4 creatives and a collapse. 17: run every profitable concept because each adds profit; a 2.2x on $50,000 adds more than a 10x on $500. Condition: always; check the top 1 to 3 ads' spend share monthly. Sources: 01, 02, 05, 17. `[needs brand data: spend share by ad by month]`. Cards: [5db051a99754] [07ea7f1c6fd7] [db5e1836d487] [684258aed19c] [80dbff5fec17] [1defb5a33424].

**R127. Volume counts only above a quality bar.** 01: hierarchy is volume, concept quality, hook strength, editing quality, UGC talent, storytelling; define a 7 out of 10 ad and maximise volume above it; 2 accounts launching 2,000+ ads a month on about $4M a month were unprofitable. 08: total ads "literally means nothing", only winners count, and low-quality volume mis-trains the pixel. 15: 50 ads in an afternoon "and nothing is working"; expect about half of even context-rich AI output to be usable. 17: 1,000 ads an hour, fake UGC and many creators give a "very low" win rate. 09: "above a 7 out of 10 goes straight in the account". Condition: any volume target. Sources: 01, 08, 09, 15, 17. Cards: [fa5fa8da1288] [ca0232a9ea6e] [689d4746686a] [681541ae0981] [a932cc43b8da] [f4b2fe395205] [924a2df7bd2f] [a15bb69c9b3a] [66dd24ac26be].

**R128. Size monthly volume from the account's own hit rate and economics, with 1 new ad per $1,000 of monthly spend as the fallback.** 01's simple rule: $30K a month = 30 ads; his back-propagation: mean spend per ad = spend / ads launched; expected revenue per ad = mean spend x return (7-day click ROAS or aMER); ads needed = new customer revenue target / expected revenue per ad (his example: 100 a month). 03's churn model: winners to replace per month / hit rate (2 churned winners at a 5% hit rate = 40 ads); hit rate 5% to 15%, 5% "pretty normal". 08: 5% is "really solid, fairly normal"; a winner = spent more than 5% of the campaign budget and hit target CPA. Do the arithmetic in code with the brand's data. Condition: monthly planning. Sources: 01, 03, 08. `[needs brand data: ads launched, spend, revenue per ad, winners and churn over 12 months]`. Cards: [43ade564407b] [a667b506d058] [5482737fbbe4] [70512842dc08] [681541ae0981].

**R129. Set the production budget by spend tier.** 01's tiers (AUD, roughly USD): $4K to $30K a month: production is founder time, 60% to 80% of budget on testing, 3 active concepts. $30K to $100K: about 25% of media on production, 30 to 100 new creatives a month, 5 to 6 concepts, 2 to 3 UGC creators. Above $100K: production falls toward about 10% of media (about 2.5% of revenue at a 25% MER), at least 100 creatives a month, 8 to 10 concepts, 4 to 6 creators, and a model of cost per asset by source and profit per ad. Condition: brands without their own per-ad economics; replace with R24 once the data exists. Source: 01 only. Cards: [9ade7e9cbc82] [7e5d74c74710] [3b1d58c1f2c4] [7959f56e5471] [0c485f7f58f5].

**R130. Split production effort across replication of winners, iteration and net-new concepts.** 01: replication 50% to 60%, iteration 20% to 30%, net new 20% to 30%, never 0% net new. 12: default bets build on winning ideas (new formats, facets, styles on winners) and most people drop a winning idea before the market does. 05 warns that replication alone (variants of 1 winner) is the old way. Condition: batch planning. Sources: 01, 05, 12. Conflict: C2. Cards: [9ebeaefa9a83] [250bd27148f4] [d3000970b47e] [80dbff5fec17].

**R131. Treat creative as the revenue driver and production as media, not as a cost centre.** 01's case: a $350K-a-month account with 15 live ads; reworking old winners to about 60 ads cut CAC about 20% to 30% and raised new customer revenue about 28%; the founder refused production spend, the 60 ads fatigued, the account slid back. Condition: any budget conversation. Source: 01 only, reported by the agency that ran it. Cards: [54ba7f2f938e] [ca0232a9ea6e].

**R132. Work in pipelines and loops, not single ads.** Collect material all month, script in bulk, shoot rarely (02); let each test write the next brief: a winning angle gets more creatives, a winning hook gets 3 new bodies, a losing format is dropped for the one that won, competitor-review weaknesses become objection ads (10); review the account, competitors and the market several times a week and expect most ads to fail (12). Condition: the standing operating rhythm. Sources: 02, 10, 12, 17. Cards: [d0b9623db467] [01183c908919] [6d03d8961586] [be42d3427124].

**R133. Above about $50,000 a month, balance spend across ads and products against inventory and cash, not only ROAS.** Squeeze a winner (high budget, faster fatigue) when there is stock to clear; let it breathe ($100 a day for 6 months rather than 6 weeks) when stock or cash is tight; make creative for slow stock even at lower efficiency. Condition: mid-size and larger brands; finance inputs from 20-FIN and 18-COG. Source: 01 only. `[needs brand data: stock by SKU, cash conversion cycle]`. Cards: [6255e96b9dce] [2856ec36e1a9].

### 3.11 Testing loops: packs, ad set minimums, reads (creative side; execution is 24-DEP)

**R134. Every test starts with a hypothesis that names the concept and the 1 variable under test.** State expected spend, expected conversions and expected return before launch, then compare. Only run tests that are measurable, worth the spend and would change what the team makes next. Condition: every pack. Sources: 01, 03, 10. Cards: [70512842dc08] [d6f4dfaaf4c4] [1c4808b43997].

**R135. One ad set holds 1 concept, and new ads always go into a new ad set, never into a winning one.** 01: 1 ad set = 1 concept, so results can be read per concept and cross-ad-set spill is limited; adding ads to a winning ad set resets learning in part and breaks sequencing. 08: 1 avatar plus 1 angle per "pack" named by both. 15 and 17: "new ads, new pack; new concept, new pack", 1 avatar per pack. 05 is the outlier: all awareness stages in 1 ad set and let Meta pick. Condition: every launch plan handed to 24-DEP. Sources: 01, 08, 15, 17. Conflict: C4b. (deployment, 24-DEP) `[verify UI]`. Cards: [c66780271b6f] [044de7406ebb] [68bf58e8538f] [0519aa2b0cc3] [a8e061b0c56f] [ecb0d8423c9a] [08ed4f654c83] [14533d4ab993].

**R136. Put 4 to 8 ads in a pack, at least 3, and plan 10 or more ads per concept across packs.** 15 and 17: 2 to 10 per pack, 4 to 8 the sweet spot. 01: minimum 3 per ad set, 10+ ads per concept, about 20 at a 5% hit rate to expect 1 winner. 02: 2 to 4 hooks per body per launch, up to 8, because more spreads the budget too thin. 10: 13 ads at $30 a day needed an impression cap to get any read at all. Strictest reconciled rule: never more ads in a pack than the daily budget can take to a read in the window; 4 to 8 by default. Condition: every pack. Sources: 01, 02, 10, 15, 17. Conflict: C10. `[needs brand data: daily budget per pack, target CPA]`. Cards: [ecb0d8423c9a] [08ed4f654c83] [c66780271b6f] [70512842dc08] [d0761aaedfd8] [d13b3e03307b].

**R137. Give a new pack guaranteed delivery for a fixed window, then let it run free.** 15 and 17: an ad set daily minimum of 1x target CPA (capped at 20% of budget when 1x CPA is a large share), removed on day 7, never longer; winners keep spending above the floor, losers fade. 10: a per-ad impression cap (1,000, lowered to 800 at $50 to $70 CPM) so 13 ads got "apples-to-apples" visibility. 01: do not touch an ad set that is hitting KPI; if it misses, change anything. 05: "levelled" spend across creatives is the sign the structure is right (with no threshold). Common practice lets Meta allocate and reads the ads it favours. Condition: the test plan says which option is used and why; the deployment agent executes. Sources: 01, 05, 10, 15, 17. Conflict: C5. (deployment, 24-DEP) `[verify UI: ad set spending limits, impression caps]`. Cards: [757303dd5a4c] [663713e886d2] [d13b3e03307b] [cae81d0649c4] [d875376938d0] [5e88d4de1c4e].

**R138. Read a pack after at least 7 days, and expect winners inside 1 to 2 weeks.** 15 and 17: the 7-day minimum defines the first read. 10: aim to find winners in the first 1 to 2 weeks. 17's analysis example uses the last 14 days. 08 gives no window. Reads before day 7 are directional only. Condition: every pack. Sources: 10, 15, 17. Cards: [757303dd5a4c] [663713e886d2] [d13b3e03307b] [2497f72f8deb].

**R139. Change 1 meaningful variable per test, and make it big enough to measure.** 10: if hook, angle, audience, page, offer and campaign all change at once, "what did we test? Nothing." 03: change 1 concept element, not the pixel. 15: an iteration is "a decent swing". 12's own rotation example changes several parts at once for speed; treat that as iteration, not attribution. Condition: any test meant to teach something. Sources: 03, 10, 15. Conflict: C19. Cards: [1c4808b43997] [d6f4dfaaf4c4] [f8f574a45327] [b7618be5460c].

**R140. If most ads in a batch never got delivery, record the test as inconclusive, not as failures.** Re-run fewer creatives with enough delivery. Brands that launch 30 ads on a small budget and call them failures after 2 days learn nothing. Condition: small budgets. Source: 10 only (card wording for "inconclusive"). Cards: [d13b3e03307b] [cae81d0649c4].

**R141. Test new creative on cold audiences with existing customers excluded, and keep a winner where it is when it works.** 01: exclude existing customers from testing and scaling so those stay purely cold; scale a winner by raising its budget and by launching more ads for its concept in a new ad set, never by turning it off to relaunch it elsewhere ("rookie mistake"). 08 and 15: exclude 180-day purchasers from prospecting; test only in prospecting. Condition: test and scale plans. Sources: 01, 08, 15, 17. (deployment, 24-DEP) `[verify UI]`. Cards: [044de7406ebb] [c66780271b6f] [a8e061b0c56f] [ecb0d8423c9a].

### 3.12 Reading results: attention, click, post-click, incremental

**R142. Read the whole chain: did the right people stop, did they click, what happened after the click, did the ad cause sales the business would not otherwise have had.** 10: attention (hook or visual), click (CTR vs link CTR), post-click (conversion rate, add to cart, checkout, page speed, offer, price, shipping); if quality clicks do not buy, check the page before blaming the creative. 01: hook and hold rates as diagnostics, CPC and CTR as leading signals, ROAS or CPA on 7-day click or incremental as the outcome. 18: views are not sales. Condition: every read. Sources: 01, 09, 10, 18. `[needs brand data: per-ad metrics down to on-site funnel]`. Cards: [f6fbbab529e7] [03cf444bb483] [8d71a067a46c] [c7c5b8ef2ed7] [8cce5e9474f5].

**R143. High CTR can be empty attention. Read CTR next to link CTR and post-click behaviour.** 10's pair: a visually stimulating ad at 10.9% CTR with a drop of "over 3%" to link CTR and little buying; a routine and before-and-after ad at 6.3% CTR with a drop under 2% that led to buying. Whether the drop is points or relative is unclear in the source. Condition: any ad that wins clicks. Source: 10 only (1 pair of ads). `[verify UI: CTR (all) vs link CTR columns]`. Cards: [03cf444bb483] [cae81d0649c4].

**R144. Amount spent is a signal to rank by, not proof of a winner.** 01: rank ads by amount spent first, because an ad at 1.7x with double the spend of an ad at 2.2x is the stronger one and likely an opener causing sales elsewhere. 17: sort by spend under incremental attribution and flag high spend above threshold. 10: the ad with the most spend drives the most sales because it was "out in the market more"; the platform snowballs onto strong early engagement, so watch the ad and understand why it spends. Reconciled rule: sort by spend, then require the ad to clear the outcome threshold and to make sense as a concept before calling it a winner. Condition: every ranking. Sources: 01, 10, 17. Conflict: C12. Cards: [2af6392d4a31] [57ca8c633830] [8d71a067a46c] [2497f72f8deb] [cae81d0649c4].

**R145. Judge on incremental or 7-day-click results at ad set or campaign level, with existing customers excluded, not on ad-level last click.** 01: ad-level ROAS is "close to meaningless" because Meta optimises a sequence and last click credits the closer; campaign level on 7-day click with existing customers excluded is close to the P&L. 15 and 17: rank by incremental revenue and incremental ROAS (17's example: 1.42 reported vs 1.23 incremental on the same $97,000). 03: top-of-funnel statics show ROAS below bottom-of-funnel ones and are wrongly killed. Condition: every winner call; the column setup is deployment. Sources: 01, 03, 15, 17. (deployment, 24-DEP) `[verify UI: incremental attribution availability]` `[web check: how Meta computes incremental attribution]`. Cards: [9d506de16067] [b7fe20be2d09] [d304b260b888] [f8f574a45327] [2497f72f8deb] [b3058b60c97e].

**R146. Define a winner before launch and leave ads that sit at the threshold alone.** 08: spent more than 5% of the campaign budget and at or under target CPA. 17: high spend, above the brand's incremental ROAS threshold (1 brand's bar is about 1.1 on new customers), with outsized results on that spend; 1.13 and 1.16 against 1.1 are left untouched. 15: top ads by incremental revenue. 10: also ask whether it can hold spend at a larger budget; a great CPA at $30 a day may be a retargeting ad. Condition: every test plan states its definition. Sources: 08, 10, 15, 17. `[needs brand data: target CPA, breakeven incremental ROAS]`. Cards: [681541ae0981] [2497f72f8deb] [f8f574a45327] [cae81d0649c4] [64b12f085516].

**R147. Care about total profit across concepts, not the single best ROAS.** Run every concept that is profitable at its own spend level; a 2x that spends $50,000 profitably adds more than a 10x that can spend $500. 01 agrees from the portfolio side: every ad has a spend capacity. Condition: winner selection and scaling. Sources: 01, 17. `[needs brand data: contribution margin per order]`. Cards: [1defb5a33424] [2856ec36e1a9].

**R148. Public signals (likes, run time, "low impression count", Ad Library position) are weak proxies for anyone's results.** 07 and 13 read likes and run time; 11 guesses spend from likes and launch age; 17 ranks competitors by run time. All 4 note the limits. Use them to pick what to study, never to declare a winner. Condition: competitor research and public teardowns. Sources: 07, 11, 13, 17. Cards: [1f32e05c1042] [23116e553dcf] [8ef182c6518e] [5790ccbc3904].

**R149. A weak ad in a valid funnel slot may stay, but only if the brand's numbers say so.** 05: "you're not turning off necessarily the bad ads" because each holds a stage slot, with no kill rule. 10: cut the weakest option after each test, "even if it's 5 cents cost per click". 15: losers "fade and scale down" after the minimum comes off. 01: do not touch a winning ad set at all. Reconciled rule: never keep an ad on stage coverage alone; keep it only when spend, purchases and margin across several windows justify it, and never cut an ad inside an ad set that is hitting KPI. Condition: pruning decisions. Sources: 01, 05, 10, 15. Conflict: C13. `[needs brand data: per-ad spend, purchases, margin over several windows]`. Cards: [fa341581e505] [5e88d4de1c4e] [1c4808b43997] [757303dd5a4c] [d875376938d0].

**R150. Assign each surviving ad a funnel role from its combined metrics, not from what the brief intended.** 08: top packs spend more with lower ROAS, bottom packs convert better and spend less, "exactly what you want"; a pack that behaves unlike its label shows where the ad really sits. 10: a strong CPA that only holds at low spend may be a retargeting ad. Condition: after a test produces several usable ads. Sources: 08, 10. Cards: [a8e061b0c56f] [64b12f085516].

### 3.13 Iteration vs new concepts under Andromeda; fatigue

**R151. Diagnose fatigue before fixing it: is the ad stale, or is the audience too small for the spend?** 01: cold frequency above 2 at ad level over 30 or 60 days is the red flag; a small persona churns (marathon trainees), so hold spend at its capacity and rotate creative; a stale ad has hit its lifetime capacity, so iterate or replace. 05's pattern: ROAS falls as spend rises, recovers briefly after new variants, then drops again. Ask a Meta rep for the Creative Similarity Score (higher is worse); without it, rising frequency, falling reach and falling ROAS together point to sameness. Condition: any performance decline on a winner. Sources: 01, 05. `[needs brand data: frequency, reach, ROAS trend per ad]` `[web check: Creative Similarity Score availability]`. Cards: [e671f82f98b0] [70e1681410fa] [1e5ab3cbe70b] [c3b5ba2b7356].

**R152. Revive a fatigued winner with new hooks before you scrap it for new concepts, and shoot the hooks as new footage with a different person.** 19: replace only the first 3 to 5 seconds; do not re-cut hooks from the old footage, because the market saw and rejected that opening; change angle, offer, avatar or format; run more than 3 hooks (target 10); the case matched its old level at the same daily spend. 01: hooks on old winners are nearly free; 50 hooks bought another $100K. 02: a scene change on the same script bought another $40,000. 05 and 03 say the opposite: variants of a winner are the old way and near-identical ads are grouped. Condition: a proven body that ran months and stopped; a first test of the revival before any new concept spend. Sources: 01, 02, 19. Conflict: C2. Cards: [c8317f1a2291] [876d09a8a01a] [ec923b82af65] [59cf922e4996] [2f44cbccd498] [764735dc658b] [73f8f845b93b].

**R153. Iterate winners with decent swings and rotate 1 element to scale a format; make net-new concepts too, never 0%.** 15: keep the winning angle, change the execution a lot. 03: keep a winning static format and swap persona, offer or angle. 12: guess which part of the winner is active (concept, actor, or both), keep it and rotate the rest; brief the editor with the winning reference plus the changed part; do not drop an idea earlier than the market does. 17: merge 2 proven concepts into a 3rd; treat your own winners like competitor concepts. 01: 20% to 30% of effort on net-new. Condition: every batch after the first winner. Sources: 01, 03, 12, 15, 17. Cards: [f8f574a45327] [6480746607a0] [b7618be5460c] [765ed4cbcc9c] [d3000970b47e] [be42d3427124] [9ebeaefa9a83].

**R154. Rotate format when an ad fatigues: video to image, VSL to UGC, image to a long-copy static, founder protagonist to voice or animation.** 01's 4 tactical responses: new hooks; a cost-cap campaign for a short spend push (fatigues it faster); move the post ID to a scaling campaign ("won't save the account"); rotate format. Duplicating ad sets is "too tacky". A fatigued ad cannot be saved for long; the fix is other working ads. Condition: after R152. Sources: 01, 02. Cards: [764735dc658b] [713723220d75] [2856ec36e1a9].

**R155. Shape the fatigue curve by inventory and cash, not ROAS alone.** Squeeze or breathe (R133). Agencies that squeeze winners for a 30-to-90-day case study cause stockouts and short account life. Condition: scaling a winner. Source: 01 only. Cards: [2856ec36e1a9] [6255e96b9dce].

**R156. Under Andromeda, aim for diversity that delivery can tell apart: persona, angle, offer, format, and truly different hooks.** 01: similar creatives get bundled to one pool, so frequency rises and reach falls; identical creative to the same user helps up to 2 impressions, then purchase probability collapses. 03: Andromeda groups near-identical ads "as the same ad ID" (relayed from reps). 12: make winners with enough diversity that the algorithm serves them separately. 19: diversity was always good; the error is jumping from "diversity matters" to "stop hook testing". Condition: portfolio planning. Sources: 01, 03, 12, 19. `[web check: Meta documentation on Andromeda and creative grouping]`. Cards: [1e5ab3cbe70b] [70e1681410fa] [d6f4dfaaf4c4] [d3000970b47e] [2d5a90d21b0d].

### 3.14 Winner analysis

**R157. Break every winner and every loser into the same parts, then write the hypothesis of what drove it.** 12's DNA sheet: segment (outcome x demographic x facet), concept in 1 sentence, angle, mechanism (problem cause, solution cause), the 6 copy blocks marked strong, weak or missing, the hook quoted, the format; for video, CAST (conceit, actor, style, terrain, setup). Then ask: if this works, is it 1 element or the combination? 13: split hook, bridge and body and grade each. 10: watch the ad to explain the numbers; ask whether the reason it performs relates to the product's value. Condition: every winner and the worst loser in each batch. Sources: 10, 12, 13. Cards: [1b2a2554a0c8] [765ed4cbcc9c] [2f0b793e3ea7] [b6e4c6832826] [89a475819a6d] [cae81d0649c4].

**R158. Tag the live library and look for gaps in a segment x format matrix.** Mark which cells you have run and which competitors run; a competitor format you never tried, or a segment buried in your ad comments and reviews, is a gap for the next batch. 05: label each live ad by stage and by pillar; a stage or pillar with no ads is a gap. Condition: monthly planning. Sources: 05, 12. `[needs brand data: ad history tagged by segment, format, style, stage, source]`. Cards: [1daabb35866f] [b6e4c6832826] [86dcadbf0b6b] [7ef548d9c0df].

**R159. Run a frame-by-frame teardown on live video before deciding what to fix.** 09's order: hook type and what the viewer knows after 3 to 5 seconds; bridge; where education starts and when the value proposition first appears; features tied to benefits; objections answered; proof on screen for every claim; cut count; CTA fit and true scarcity; swap-the-face test; click the destination. Condition: any video review, own or competitor. Sources: 09, 13. Cards: [66dd24ac26be] [2a76fe7e97e3] [89a475819a6d].

**R160. Watch the ad libraries of brands that ship strong creative, and study structure, not their claims.** Condition: swipe research. Sources: 13, 17, 12. Cards: [8ef182c6518e] [5790ccbc3904] [36945e14679a].

### 3.15 Briefs, pipeline and AI

**R161. Run the pipeline in this order and weight: research, concept, build, variations, internal feedback, launch.** Each step means nothing without the one above it; variations are "just to squeeze a little bit more spend through the concept". Condition: every batch. Sources: 03, 10, 12. Cards: [d797d2ae775b] [789c10faf325] [3fb8f0a02cc8] [01183c908919].

**R162. Every brief carries the concept fields and names the creative type so the set stays diverse.** 16's 6 fields: concept, creative type (curiosity static, us vs them, USP call-out, social proof), angle (including who it is for), headline, CTA, visual direction. 03's brief: persona, angle, offer, format, key message. This playbook's brief (section 9) adds awareness stage, destination, emotion, proof available, claims cleared, and the hypothesis. "Always write down your creative type because you don't want to make a hundred of the exact same ad." Condition: every asset. Sources: 03, 16. Cards: [377393f355c6] [789c10faf325] [ab5dac71c1dc].

**R163. Use AI in the middle of the pipeline, not at the ends.** 01: ideation and analysis stay human (LLMs "output the mean" and misread account context); briefing, scripting and production use AI heavily; a brand-specific Claude skill that asks about 20 questions gets a script "99% of the way there". 03: 3 patterns real clients use, all with a human at concepting or feedback; full automation gives "slop". 15: AI is an accelerant on a strategy, deep brand context separates good output from slop, expect about 50% of output to be usable and review every piece. 16: research must be manual; AI will not write niche humour. Condition: any AI use. Sources: 01, 03, 15, 16. Conflict: C15. Cards: [c17baa93a884] [bf65df9beea1] [7a115c9bb3e2] [f4b2fe395205] [924a2df7bd2f] [d59ecd84945b].

**R164. Load the AI with the brand book, product facts, allowed claims, personas and the brand's own winners before generating, and keep a shared prompt library.** 15: brand URL, products, competitor set, things to say and not say; add more over time; connect account data read-only so research ranks by real KPIs. 01: a brand skill. Condition: any AI generation. Sources: 01, 15. `[needs brand data: brand book, claims list, winners]`. Cards: [f4b2fe395205] [924a2df7bd2f] [c17baa93a884].

**R165. AI may reproduce the brand's own winners and layout ideas. It may not clone competitor ads.** 05, 15 and 17 tell the reader to "copy and replicate any static ad", "clone any ad", "recreate this exact ad for every product" from other brands. Under override 1 those are rewritten as: take the layout or structure, rebuild with the brand's own persona, angle, offer, words and assets. Condition: any AI or manual production from a reference. Sources: 05, 15, 17 (as what they said). Cards: [9395469a9874] [924a2df7bd2f] [cba1f889934b].

**R166. Generated images keep the real product photo where accuracy matters.** AI builds the scene, the illustration of the problem, the B-roll, the format shell; the product itself is the real photo or footage, so buyers get what they saw (R42). Condition: every AI-assisted static or video. Sources: ecomOS rule; 07 and 03 on true-to-life product shots; 15's card. Cards: [08f49b8491b0] [ae9948825d17] [924a2df7bd2f].

**R167. Write the hook first, then let AI draft the rest, then hand-edit the mechanism and copy blocks, then send video to a human editor with a winning reference.** Condition: production workflow. Source: 12; 01's brief-first approach agrees. Cards: [3fb8f0a02cc8] [c17baa93a884].

**R168. Tag every asset by concept, persona, angle, offer, format, stage, source pillar and idea source.** Without tags, patterns and gaps stay invisible (R158) and the sourcing split (R111) cannot be checked. Condition: from the first batch. Sources: 05, 12 (card wording). Cards: [7ef548d9c0df] [36945e14679a] [1b2a2554a0c8].

### 3.16 Compliance risks in creative

**R169. Treat every health, weight, body-image, fertility, appearance and medical-condition claim as high risk: substantiate it and check policy before launch.** The sources' examples include GLP-1 side effects, "detox for worms", vitamin deficiency from symptoms, "fixed her back pain in 2 weeks", "bring back your jawline", appetite suppression, blood pressure, dysbiosis prevalence, "Alzheimer's" (13's presenter doubts it himself). None of the presenters checks. Condition: any such claim. Sources: 02, 03, 04, 05, 07, 11, 12, 13, 16, 18 (as risks the mini playbooks flag). `[web check: Meta and TikTok health, personal attributes and body-image policies; local rules such as ASCI in India, TGA in Australia, FTC in the US]`. Cards: [46035a697541] [c23189aedfc7] [6afdcae5d6b5] [f970fc3788a8] [df555261a040] [de0b0ea997a3] [8bf081bed714].

**R170. Never invent a statistic, study, customer count or prevalence figure.** 07 and 03 say a made-up percentage still builds authority; 04's model script invents a sodium-imbalance claim; 05's "74% of people suffer from gut issues" is unsourced. All rejected under override 2. Condition: every number (R43). Sources: 03, 04, 05, 07, 10, 13. Cards: [385b3e7e17c3] [3db510f74584] [46035a697541] [86dcadbf0b6b] [306f74067bdf] [ee8baa9c8041].

**R171. Before-and-after imagery is a policy risk. Never "sneak" it past review.** 01's presenter calls before-and-afters the best-performing angle component and says to sneak them past Meta; that is not a rule here. 07's illustration route and 05's "here's what life could look like" framing are the compliant directions to test. Condition: transformation content in health, beauty and body categories. Sources: 01, 05, 07. `[web check: Meta policy on before-and-after images]`. Cards: [087eee279056] [5bfda2bed53d] [d2e3d5f918af].

**R172. No fake interviews, fake whistleblowers, pretend news formats, invented characters presented as real, or scripted reviews.** 12's confessional whistleblower with a high-end escort actor and "Wall Street Journal style" conceits, and 02's scripted 1-star review, raise authenticity and disclosure problems. Formats that imitate media are allowed only when the content is clearly the brand's and no real person or outlet is impersonated. Condition: pretend-format conceits. Sources: 02, 12. `[web check: Meta misleading-format rules]`. Cards: [10b56ec55756] [289897a2c363] [4098dd29a9fa].

**R173. Disclose paid partnerships and never run a brand-owned review site as if independent.** 01 and 03 praise an IM8 static run from a doctor's profile "not as a partnership ad" so "you don't know this is an ad", and a brand-owned "Dermatologist Reviews" ranking site with affiliate links on rivals. Under override 4: use the partnership label, disclose the relationship, and present any brand-owned education page as the brand's. Condition: whitelisting, creator handles, advertorials. Sources: 01, 03. `[web check: branded content and endorsement rules in the market]`. Cards: [646aacb0f2a9] [c23189aedfc7] [95a5ffb79c86] [1620b9b6a2e3].

**R174. Competitor comparisons: show a generic "old way" failing, with true claims, rather than naming or showing a rival, and never stage a problem that is not real.** 18 praises an "over exaggerated" dust demo and rivals shown breaking; 08 allows a competitor comparison "if you are very competitive"; 02 says founders take adversarial risks agencies avoid. 03's presenter would blur a rival's trademark heavier and remove the name. Condition: comparison and adversarial angles. Sources: 02, 03, 08, 18. `[web check: comparative advertising law and platform rules in the market]`. Cards: [c7c5b8ef2ed7] [8e3f775ece26] [b27bfdea1a9c] [acb7fe437e41].

**R175. Copy that implies a personal attribute (race, health condition, sexual function, fertility, body shape) needs a policy check.** 12's segments ("all black men struggling with erections", "diabetic men with ED"), 16's fertility and looksmaxing copy, and 07's GLP-1 hair-loss line all sit near Meta's personal-attributes policy. Condition: any persona call-out that names an attribute. Sources: 07, 12, 16. `[web check: Meta personal attributes policy]`. Cards: [0682f4fbff61] [84a55aede410] [6afdcae5d6b5].

**R176. Clear likeness and image rights: no public figures without permission, no "found on Google images" B-roll.** Sources: 11, 13. `[web check: image licensing and right of publicity]`. Cards: [8e86c45ad8e2] [2ef96388e6ab].

**R177. Scarcity, offers and prices in the creative must match the live store on the day it runs.** "Before stock runs out" that runs for 20 weeks and "up to 16% off today" are checked against checkout and dates. Condition: every offer line. Sources: 09, 13. `[needs brand data: current offer and dates]`. Cards: [129eda6e1e3a] [ee8baa9c8041].

**R178. Consent and legality for research calls to checkout abandoners.** 08's method needs contact consent and staff time. Condition: objection research by phone. Source: 08. `[web check: consent rules for calling customers in the market]`. Cards: [8e3f775ece26].

## 4. Procedures (implementation)

Each procedure names its goal, preconditions, steps, checks, and rollback. Steps that touch a platform UI carry `[verify UI]`. Sources are given by mini playbook number after the title. Nothing here writes to an ad account; where a step is executed in Ads Manager, the creative agent writes the instruction into the test plan (section 9.6) and 24-DEP executes it.

### P1. Research sprint: from customer language to an angle list (03, 08, 10, 11, 12, 16)

Goal: a research document and a ranked list of angles in the customer's words.
Preconditions: access to reviews, support tickets, post-purchase surveys, ad comments; the product list; competitor names.
1. Block time in proportion to how unfamiliar the niche is; 16 uses 3 to 4 days in a row for a new niche. `[needs brand data: all review, ticket, survey and comment exports]`
2. Read in this order and paste raw quotes with screenshots into 1 document: the brand's reviews (all star levels, 1-star included), support tickets, post-purchase survey answers, comments on the brand's ads and posts, Reddit and forum threads, Amazon reviews for the category, competitor reviews and comments under competitor ads. `[web check: competitor reviews and ad comments]`
3. Sort every statement into 3 buckets: what they want, what stops them, what they already tried.
4. Cluster by repetition. A use case or complaint that repeats across many customers is an angle; a one-off is not. Count occurrences per cluster and record the count.
5. From competitor reviews, list what rivals do badly. Each is an objection to counter (R26, R59) and a reason to differ, expressed as a generic "old way", not a named rival (R174).
6. For each cluster write the angle in 1 sentence for 1 persona: who, the product, why it solves their problem, the proof (R4). Keep the customer's wording.
7. Mark next to each angle: the awareness stage it serves (R19), the proof the brand actually has (R57), and any claim that needs a compliance check (P19).
8. Rank by count, by proof available and by fit with the portfolio gaps (P25).
Checks: every angle traces to at least 2 quotes; every number in an angle has a source; no angle is the team's own feature list dressed up.
Rollback: if the document is only an AI summary with no raw quotes, redo step 2 by hand (16). If clusters are thin, widen to competitor reviews and forums before writing angles.

### P2. Build and expand the persona list (01, 12)

Goal: 20 to 40 sharp personas defined by problems, desires and triggers.
Preconditions: P1 document; any existing persona work from 02-AVT.
1. Spend about 20 minutes listing who buys and what problems the product solves for each.
2. List 2 to 4 core personas, then drill each into problem variants (acne at 20 to 25, hormonal acne at 30 to 35, 40 to 45 are 3 personas). Write each as outcome x demographic x facet where facets are states, events or conditions (12).
3. For each persona write pain points, language, and the proof they need (age- and gender-matched studies or reviews).
4. Aim for 20 to 40 by hand.
5. Give the full list plus wide business and customer context (not 3 personas and a URL) to an LLM. Ask for 20 to 30 more. Keep only the 4 to 5 good ones. Feed those back as "these were good" and ask for 10 to 20 more. Stop when the list has roughly doubled.
6. Flag any persona defined by a personal attribute that needs a policy check before it appears in copy (R175).
Checks: no persona reads as a demographic label alone; each persona could tell a writer the script, the talent and the proof.
Rollback: if the LLM returns generic archetypes ("busy professional"), the context was thin; add P1 quotes and rerun.

### P3. Build the concept board (01, 02, 03, 08, 12, 15)

Goal: a board of concepts (persona x angle x offer, plus format and stage) sized to the volume target.
Preconditions: P1, P2, the offers the brand can run, the volume target from P12.
1. For each candidate concept fill the row: persona, angle (1 sentence), mechanism (problem cause, solution cause), offer (product plus value framing), awareness stage, proof available, destination page, candidate formats, creative type, hypothesis.
2. Check each row against R1: at least 1 of persona, angle or offer differs from every other row. Rows that differ only in format or design are variants of a parent concept, not concepts; mark them as such.
3. Weight the board to the less aware stages: at least 70% of rows serve unaware, problem aware or solution aware viewers (R20). Fill bottom-of-funnel rows only with 1-objection ads (R26).
4. Add rows from the gap matrix (P25): a segment that repeats in comments but has no ad, a format competitors run that the brand never tested.
5. For a founder brand, add 02's matrix variables: proof type and founder role (protagonist, witness, interviewer, reader), changing 1 variable per new row.
6. Order the board by the testing priority when a concept has already failed: angle, then offer, then persona, then format (R7). For a new brand, start with the angles that have the most quotes and the strongest proof.
7. Write the offer test as a static first when possible (R23): statics test angles and offers fastest and cheapest.
Checks: run checklist 5.3.
Rollback: if fewer than 10 ads can be made for the lead concept (R136), either the concept is too narrow or the budget is; cut the board, do not thin the ads per concept.

### P4. Choose the format for a concept (01, 03, 10)

Goal: the cheapest format that can carry the concept to its stage.
Preconditions: a concept row from P3; per-format economics if they exist.
1. Ask 01's 5 questions: what is the concept; does it need education (yes: VSL, long video or long-copy static); can the value fit in 1 frame (yes: static or carousel); does the product need a demo (yes: video); what stage (less aware: longer, educational; product or most aware: images, offers, catalog).
2. Ask 10's question: must the value be seen moving or in real use? If yes, video.
3. Where per-ad economics exist, compare expected gross profit per ad by format (R24) and lean to the format that returns more profit per ad, not the one that "performs better".
4. Produce a static whenever the concept allows, and plan to turn a winning static angle into video later (R23).
5. Record the format and the reason on the concept row.
Checks: the format is chosen after the concept, not before (R3).
Rollback: if a static fails on an angle that needs a demo, do not conclude the angle failed; retest in video.

### P5. Build a static ad (03, 07)

Goal: a static that sits at one end of the clarity vs curiosity spectrum, reads in the right order and matches its destination.
Preconditions: a concept row; real product photos; the destination page; claims cleared.
1. Decide the end. Clarity: a 3-to-4-second look tells product, angle, who and offer. Curiosity: the viewer cannot tell what is sold or that it is an ad; withhold or blur the product; 1 open loop. Write the choice on the brief.
2. Decide the destination from the end (R34): curiosity, native and advertorial statics to an educational page (advertorial, listicle, quiz, long-form); clear offer statics for product or most aware buyers to a PDP.
3. Write the headline and choose the image as 1 unit (R36). Run the substitution test: with a generic image, does the headline still make sense? If yes, the pair is too loose.
4. Set the first eye stop to the highest-awareness message (problem, persona call-out, "new technology"), never the product category (R35).
5. Plan 3 to 4 eye stops: hook element, the bold line that answers the question it raised, 1 or 2 short supporting facts, proof (legible review with stars or name, or a true-to-life product shot).
6. Use size, contrast and whitespace to enforce the order. Fix spacing, alignment and case. Drop the corner logo when the page name shows the brand (R48).
7. Benefit first, mechanism in brackets or smaller type. Cut call-outs that repeat the headline. Sub-headlines readable on a phone; if not, enlarge about 30% and move up (R38, R39).
8. On a clean product-shot static, keep the headline to about 5 to 6 words and make it answer "why this instead of what they use now" (R40).
9. For an unaware or problem-aware static, write the long primary text (R45; wording is 11-ADC) and the persona or problem call-out in the first line.
10. If the topic is sensitive, use an illustration instead of a graphic photo (R46) and run P19.
11. Keep the real product photo; AI may build the scene only (R166).
12. Build the template so the next angle swaps only the words and the picture (R47).
Checks: run checklist 5.1 with someone outside the team.
Rollback: an ad that lands in the middle of the spectrum is pushed to one end or dropped; do not add spend to a confusing static (07).

### P6. Write the primary text structure and the destination match for a native or curiosity static (03, 04, 07)

Goal: a text block and a page that finish what the image started. (Word-level copy is 11-ADC; page build is 07-LPG.)
1. First line: persona or problem call-out ("Read this if you're always bloated by 3 p.m.").
2. First-person story that the persona has lived; disqualify others on purpose.
3. Move through the stages: why the problem happens, how it happened to the narrator, the solution.
4. Social proof and timelines, only true ones.
5. Reveal the product late ("here's where I actually got it from"), name the offer, and put the product name and code here rather than in the image on a native static.
6. Destination: a custom page that continues the angle and states an offer congruent with the ad ("less shedding in 26 days or less"). Do not sell hard on the page for the curiosity direction.
7. Click the live ad after launch and confirm the page loads and holds the promise (R71).
Checks: image stage and copy stage match (R21); primary text carries the education the image withheld.
Rollback: if a curiosity static underperforms on a PDP, test the educational page before concluding statics do not work (03).

### P7. Write a cold video script (04, 09, 11, 13)

Goal: a script whose hook filters, whose bridge educates, whose product arrives late and whose close gives a reason to buy.
Preconditions: concept row with mechanism and proof; objections from P1; the stage the ad serves.
1. Set the stage the whole ad serves and hold hook and body to it (R21).
2. Hook (first seconds): name the viewer's problem, persona or a known industry narrative; no product name, no product on screen, no offer (R81). Write 2 to 4 hooks per body for the first wave (P8).
3. Bridge: state a solution exists, then teach why the problem happens. No product pitch here (R53). Keep a visual cue moving (a prop, B-roll) through the bridge.
4. Problem and mechanism: in the customer's words; the biological, material or design cause; each term explained and, where true, a sourced prevalence line (R55, R56).
5. Failed alternatives: what they tried and why it did not work, from customer data (R59).
6. Product reveal, blended in as the thing that combines the mechanism; a research or supplier story before the name if the bridge feels abrupt (13).
7. Benefits before features, table-stakes features in 1 line, expert terms exact (R60, R70).
8. Proof stack: tests, customer count, testimonials from people who look like the viewer (R61). Every claim has a shot that proves it (R57).
9. Objection handled out loud, then a reason to move from learning to buying, risk reversal, clear CTA at the intensity the ad earned (R62, R63). No open loops in the CTA.
10. Script QA: search for "isn't ... it's" and stock analogies; check every number, every offer date, every health term (R69, R177).
11. Mark shot-level motion: cuts, overlays, B-roll, handheld moves; native setting over studio rig (R65).
Checks: run checklist 5.2 and P19.
Rollback: if the retention curve later drops right after the hook or right before the CTA, the bridge is the fault (R95); rewrite that segment only (R64).

### P8. Write, grade and multiply hooks (01, 04, 12, 19)

Goal: a graded set of hooks per body, shot at volume and launched in waves.
Preconditions: the body script; the persona; the speaker options.
1. Decide the hook's job: which viewer must stop, and what they must know by the end of the hook.
2. Draft with 2 methods: the template (Persona + Problem + Pattern interrupt + Promise) for volume, and 12's 4 steps (isolate the idea, commit, deep fry with contrast, surprise, novelty, nuance, stakes, make it bang with trigger words, simple language, best information first, open loops) for novelty.
3. Pick hook types from R77; avoid "the number 1 mistake" style; skip "tactical promise" for ecommerce.
4. Plan all 3 layers for each hook: audio line, on-screen copy (a bold headline, not just captions), visual (B-roll, props, a supermarket sweep, a whiteboard reveal, a 3-second static or motion intro).
5. Grade each hook: clarity, relevance, novelty, then specificity and credibility (R76). Drop any with low clarity and low relevance. Fix the weakest layer on the rest.
6. Cast a speaker who plausibly is the persona; for authority, a person the persona trusts (a runner, a doctor), with rights cleared (R86).
7. Spread hooks across 19's levers (angle, offer, avatar, format) so they are not near-duplicates (R91).
8. Check every hook bridges naturally into its body (R93); cut the ones that do not.
9. Shoot: record each hook about 6 times; 10 hooks per body is a normal shoot (R90). Shoot a 3-second static or GIF intro version too.
10. Launch in waves of 2 to 4 hooks per body (up to 8), sized to the budget (R90); hold the rest for wave 2 and for revival (P18).
11. Optional before paid: post about 20 hook variants as trial reels, keep the best, launch about 5 (P21).
Checks: checklist 5.6.
Rollback: if hook rate is low against the account average, swap the hook and keep the body; if hold rate is low, the bridge is at fault (R95).

### P9. Founder ad: story, structure, batch shoot (02)

Goal: a batch of founder ads built as arguments, shot in one short session.
Preconditions: a founder willing to appear (or a chosen involvement level); true origin facts; lab, supplier or test proof; the review and inbox feed.
1. Write the founder story's 3 owned elements: origin (why the business started, true), mechanism (why the product works, said by the founder or a credentialed expert), adversarial angle (what the category does wrong, with proof). Legal check on every adversarial or health claim (P19).
2. Check the story through the viewer's eyes: which problem or desire in it does the buyer already have? If none, rework (R101).
3. Split story elements into static (must stay consistent) and renewable (reviews, emails, supplier news, complaints).
4. Write 3 bodies with materially different stories using the top structure: claim (adversarial, doubles as hook), proof at once, mechanism tied to the story, proof of mechanism, CTA plus social proof (R99).
5. Write 10 hooks per body that bridge naturally; launch 2 to 4 per body per wave (R90).
6. Pick the involvement level per variant: protagonist, voice over B-roll or animation, evidence (lab photos, certificates), proxy (dietitian, supplier), absent (animation). Pick the script role per variant: protagonist, witness (real customer email, with permission), interviewer (cut to the lab or team), reader (a real review, never scripted) (R102, R103).
7. Shoot-day rules: teleprompter or memorised script while walking; a sentence outline for weak readers; 2 cameras for talking heads; move locations during the session; expect robotic takes in the first about 10 hours on camera. About 4 to 5 minutes of camera time covers 30 ads once scripts exist.
8. Edit: fast, dynamic, overlays and B-roll; low-fi opening is fine for a premium brand if the product appears only in high-end shots (R66); hold the product to about 20 seconds in story formats unless it is a demo format (R54).
9. Decide the page: founder handle as a partnership ad only if it posts often and relevantly; otherwise the company page (R106). `[verify UI: partnership ads]`
10. Set the monthly founder target inside the wider mix and the collection pipeline: reviews to a database, inbox to a weekly pull, supplier calls noted; shoot the founder about quarterly (R104).
Checks: checklist 5.2 plus the founder rows in 02's diagnostics: argument not monologue; viewer-first; claim proved; hook fits body; story true; curiosity loops closed.
Rollback: if founder ads fatigue, change scene first (cheap), then move down the involvement spectrum, then change offer, angle, persona in that order; if the concept is fatigued, stop making variants and move budget to other formats (R103).

### P10. VSL: decide, script, test, destination (11, 13)

Goal: a VSL only where needed, with a matched page and a hook test plan.
1. Decide: does the buyer need education to convert (complicated product, low-trust category, new category or ingredient, cold conversion capped by misunderstanding)? If no, stop; do not make a VSL (R120).
2. Decide where education lives: ad, page, or both (both preferred).
3. Script the 7 parts (R121) at a short length first; 13's first-30-to-40-seconds model for the opening; large on-screen text and quick pacing for an older skew (R123).
4. Pull objection handling from customer data (P1); include risk reversal and a clear CTA on the first VSL (R124).
5. Visuals: mix real UGC, AI B-roll and animation but lean one way; no found images without rights (R119, R176).
6. Finish body and CTA, then produce 3 to 6 hooks (R89, R90).
7. Plan modular variants: mechanism before problem, objections earlier, agitation pulled forward, a faster mechanism section; cut a 2-to-3-minute and a 45-second version as extra variants (R58, R122).
8. Build a custom page per VSL that continues the mechanism and story; never a bare PDP (R71).
9. Read economics on repeat purchase where the brand has it, not first-order ROAS alone (R123). `[needs brand data: repeat rate, 12-month value]`
Checks: 11's VSL review table (hook not a brand story; bridge after mechanism; every claim has a why; objections present; proof visible; risk reversal; clear offer; pacing and text; visual consistency; page continuity).
Rollback: if the VSL underperforms, fix proof placement first ("a really common and easy way to fix an underperforming VSL"), then the bridge, then hooks.

### P11. UGC brief, creator vetting and creator seeding (01, 05, 18)

Goal: creator content that carries a concept, from creators who match the persona and the market, with rights secured.
1. Vet: ask each creator for past work and the brief behind each piece; match your brief's depth to what produced their best work; default to the most detailed brief you can write (R109).
2. Cast native-accent creators per market and creators who plausibly are the persona (R110, R78).
3. Write the brief (section 9.4): concept row, awareness stage, hook options, body beats, claims allowed and forbidden, proof to show, the real product footage to include, format from R116 where TikTok-native, 2 takes (1 to script, 1 natural), deliverables and rights.
4. Choose brief width: wide for discovery (product only, creator's own story), specific to multiply winners (show the top ads with their real numbers).
5. Seeding at volume (05): mass invites, approve, ship samples (about 7 days), ask for 2 to 3 videos per sample, expect 1 to 4 weeks and non-posters; run a creator community that learns what wins; reuse the army for each launch. `[web check: seeding tools, platform rules]`
6. Secure usage rights and affiliate terms before any organic-to-paid move (R112). `[needs brand data: rights per asset]`
7. When a creator angle wins, tell the community, derive statics, and make in-house and AI versions (R111).
Checks: every UGC brief has a concept (R108); every asset has rights on file; claims in creator scripts pass P19.
Rollback: a review-style UGC that loses to a product demonstration means more demonstrations next round, not more review UGC (10).

### P12. Size monthly volume and production budget (01, 03, 08)

Goal: a monthly ad count, concept count and production budget in code, from the brand's own numbers.
1. Pull 12 months: ads launched, spend, new customer revenue, winners (by the account's definition, R146), winners that churned this month. `[needs brand data]`
2. Compute mean spend per ad, average return per ad (7-day click ROAS or aMER), expected revenue per ad, hit rate (winners / ads launched), churn (churned winners / live winners).
3. Ads needed, method A: new customer revenue target / expected revenue per ad. Method B: churned winners to replace / hit rate. Report both. Flex with the revenue forecast.
4. Fallback with no history: 1 new ad per $1,000 of monthly spend.
5. Set tier defaults from R129 (active concepts 3, 5 to 6, 8 to 10; production 25% then about 10% of media; testing 60% to 80% of budget at small spend). Replace with R24 economics once per-ad production costs exist.
6. Split effort: replication 50% to 60%, iteration 20% to 30%, net new 20% to 30% (R130).
7. Split supply: in-house, UGC, AI, near 1/3 each as a starting point (R111), adjusted by what wins.
8. Apply the quality bar: define the 7-out-of-10 ad for this brand and count only ads above it toward the target (R127).
Checks: the count is achievable at 4 to 8 ads per pack and 10+ ads per concept (R136).
Rollback: if hit rate falls as volume rises, quality is diluting; cut volume and raise the bar (08).

### P13. Build the test plan and the pack (01, 08, 10, 15, 17)

Goal: a complete test plan that 24-DEP can execute without questions.
1. Hypothesis: the concept, the 1 variable under test, expected spend, conversions and return (R134).
2. Pack contents: 4 to 8 ads, 1 concept (1 persona plus 1 angle), 2 to 4 hooks per body for video (R136). New ads never join a winning ad set (R135).
3. Naming: pack number, persona, angle, stage label ("problem + solution" or "bottom of funnel"), so the concept is filterable. `[verify UI: naming only]`
4. Audience: cold, existing customers excluded (R141). Placements open. (deployment, 24-DEP)
5. Delivery guarantee: state the option and the reason. Default in this playbook: an ad set daily minimum of 1x target CPA, capped at 20% of the campaign daily budget, removed on day 7 (15, 17). Alternative at very small budgets: a per-ad impression cap so every ad gets equal visibility (10). Alternative: no floor, let Meta allocate, and read the ads it favours (common practice; 05). Check that the number of packs with floors x floor fits inside the daily budget. `[needs brand data: target CPA, daily budget]` `[verify UI: ad set spending limits]`
6. Winner definition before launch (R146): spend share, CPA or incremental ROAS threshold, minimum days.
7. Read date: day 7 first read; day 14 decision (R138).
8. Destination per ad, checked live (R71).
9. Compliance sign-off attached (P19).
Checks: every ad in the pack calls out the same persona and angle (08); no near-duplicates (R2); claims cleared.
Rollback: if the budget cannot fund the floors, cut packs, not ads per pack below 4.

### P14. Run the 7-day read (10, 15, 17)

Goal: a first read that separates winners, losers and inconclusive ads.
1. On day 7, confirm the floor was removed (deployment) and note spend per ad.
2. Ads with little or no delivery: inconclusive, not failures (R140). Plan a smaller rerun.
3. Ads that spent: compare with the winner definition (R146). Mark winner, at threshold (leave alone), loser.
4. Pull diagnostics for each: hook rate and hold rate vs account average, CTR vs link CTR gap, on-site conversion and add-to-cart by ad (R142, R143, R95).
5. Watch every winner and the worst loser and write why (R157).
6. Decide by day 14: scale (raise budget, more ads for the concept in a new pack), iterate (P17), or drop.
Checks: no decision rests on ad-level last-click ROAS alone (R145); no ad inside a KPI-hitting ad set is cut (R149).
Rollback: if the read window had a promo, stock-out or tracking fault, extend the window rather than call winners.

### P15. Read results across the chain and pick winners (01, 08, 10, 17)

Goal: winners chosen on outcome plus concept sense, and each ad placed in the funnel.
1. Sort ads by amount spent (R144).
2. Switch the read to incremental attribution where available, 7-day click otherwise, at ad set or campaign level, existing customers excluded (R145). (deployment, 24-DEP) `[verify UI]`
3. Flag high spend plus above the brand's threshold plus outsized results. Leave at-threshold ads alone. Group by product or category where that matters.
4. For each flagged ad: does the reason it performs relate to the product's value (10)? Can it hold spend at a larger budget?
5. Assign a funnel role from combined metrics: high spend, lower ROAS, holds scale = opener; converts well, spends less = closer or retargeting (R150).
6. Judge top-of-funnel statics and openers on account-level new customer revenue and MER, not their own ROAS (R49). `[needs brand data: blended and new customer metrics]`
7. Record the winner in the DNA sheet (P16) and hand it to iteration (P17).
Checks: portfolio profit, not top ROAS, drives the scale list (R147).
Rollback: if incremental and reported results disagree sharply, hold the scale decision and check the attribution setup with 24-DEP and 06-MEA.

### P16. Winner analysis: the DNA sheet (09, 10, 12, 13)

Goal: a written hypothesis of what drove each winner and the worst loser, in a shared grammar.
1. Fill for each ad: segment (outcome x demographic x facet), concept in 1 sentence, angle, mechanism (problem cause, solution cause), the 6 copy blocks (pain, promise, proof, curiosity, constraints, conditions) marked strong, weak or missing, the hook quoted, the format, and for video CAST (conceit or none, actor, style, terrain, setup).
2. For video, split hook, bridge, body and grade each; note where the product first appears and the cut pace.
3. Compare winners with losers on the same fields. Write the hypothesis: 1 element, or a combination?
4. Feed the hypothesis into the iteration plan (P17) and the next brief (P13).
5. Add the ad to the tagged library (R168) and update the gap matrix (P25).
Checks: checklist 5.5.
Rollback: "it just works" is not a hypothesis; if none can be written, iterate on 2 candidate elements in separate packs.

### P17. Iterate a winner and decide iteration vs new concept (01, 03, 12, 15, 17)

Goal: the next batch built mostly on winners, with real swings, plus a net-new share.
1. From the DNA hypothesis, keep the active element (concept, actor, format) and rotate the rest: new hooks on the body (P8), a new persona or facet, a new offer, a new format or conceit (podcast, street interview, slice of life), a new style.
2. Make each iteration a decent swing (R2, R139): what old-school Facebook would call a new ad. No 1-word headline changes, no background colours.
3. For a winning static format, keep the format and messaging and swap 1 concept element (R47).
4. Merge 2 proven concepts into a 3rd (17).
5. Keep net-new concepts at 20% to 30% of the batch (R130); pull them from the gap matrix and STORMING sources (R18).
6. Launch iterations as a new pack (P13); never into the winning ad set.
7. Do not drop a winning idea before the market does (12); watch frequency and reach (R151) to see when it has.
Checks: no 2 ads in the batch are near-identical (R156).
Rollback: if iterations of 1 winner start taking all spend (05's pattern), shift the next batch to distinct formats and new concepts.

### P18. Revive a fatigued winner (01, 02, 19)

Goal: another run of spend from a proven body before new concept spend.
1. Confirm fatigue: months of running, most of the spend, results falling at steady spend, cold frequency above 2 (R151). `[needs brand data: ad-level trend]`
2. Keep the proven body. Do not start with new testimonials or a full rework.
3. Shoot new hooks as new footage with a different person (an employee or brand-side presenter on a customer testimonial body: EGC hook, CGC body). Do not re-cut hooks from the old footage.
4. Vary hooks on angle (seasonal or contextual), offer (in primary text and headline), avatar, format (a 3-second static or motion intro). Change 2 levers at least.
5. Produce more than 3 hooks; target 10; launch in budget-sized waves (R90).
6. Cheap add-on: reshoot the same script in a new scene with the same edit (02's $40,000 case).
7. Judge against the ad's pre-fatigue level: same daily spend, same or better CPA. `[needs brand data: pre-fatigue baseline]`
8. If the first set fails, raise volume and move more levers before concluding the body is dead; then rotate format (R154).
Checks: hooks differ on at least 1 lever from each other and from the old hook.
Rollback: if the revival holds only briefly, accept the body has reached capacity and move budget to other concepts (portfolio, R126).

### P19. Compliance check before launch (all sources' risks; ecomOS overrides)

Goal: a signed record that the asset carries no invented, unprovable or disallowed claim and no impersonation.
1. List every claim, number, study, customer count, prevalence line and offer in the asset (copy, overlay, voiceover, primary text, headline, page).
2. For each: the source document or data behind it. No source, no claim (R43, R170).
3. Category flags: health, weight, body image, fertility, appearance, medical condition, supplement, nicotine-adjacent. If flagged, check the platform policy and the market's rules. `[web check: Meta and TikTok policies; ASCI, TGA, FTC as relevant]`
4. Before-and-after imagery: policy check; prefer illustration or "what life could look like" framing (R171).
5. Personal attributes implied in copy (race, condition, sexual function): rewrite or clear (R175).
6. Format honesty: no fake interview, whistleblower, news style, invented person, scripted review presented as real (R172). Founder story facts confirmed true (R102).
7. Disclosure: partnership label on creator or founder handles; any brand-owned education page presented as the brand's (R173).
8. Competitors: no rival names, logos, packaging, faces or text; generic "old way" only; no staged problems (R174, override 1).
9. Rights: every face, image and clip licensed; no found images; no public figure without permission (R176).
10. Product accuracy: the product in every frame is the real photo or footage (R166).
11. Offer, price, dates and scarcity match the live store on launch day (R177).
12. Record pass, fix or reject per item; attach to the test plan.
Rollback: a fix that removes the ad's core claim means the concept lacked proof; return it to P1 for a provable angle.

### P20. Use AI in the pipeline (01, 03, 15, 16)

Goal: faster briefs, scripts and production without slop or copied competitors.
1. Keep ideation and analysis human (01). Use AI for research aggregation only with a human reading raw quotes (16, 03).
2. Load context before any generation: brand book, products, allowed and forbidden claims, personas, the brand's own winners, brand voice; connect account data read-only if the tool supports it (R164). `[needs brand data]`
3. Generate briefs and scripts from a brand-specific skill or prompt library; add the standing line "do not use contrast negation" (R69).
4. Review every output: angle named, avatar fit, claims true, product accurate, not a competitor clone; expect about half to be usable (R163, R165).
5. For images: AI builds scene, illustration and layout; the real product photo is composited in (R166).
6. For video: AI B-roll and animation with a consistent style (R119); human editor finishes with a winning reference (R167).
7. Never treat AI as the strategy or as a reason to stop producing the brand's own creative (15).
Checks: P19 on every AI asset; tag the asset's source pillar as AI (R168).
Rollback: if AI batches are all slop, the context was thin; rebuild the brand book and the winners file before generating again.

### P21. Validate creative with trial reels before paid (01) `[verify UI]`

Goal: a cheap read on reach and retention before spend.
1. Cut the CTA off the ad.
2. Post it as a trial reel on the page the ad will run through (business or personal).
3. Read reach against other posts and the retention graph: weak hook, bridge or body?
4. Feed the read into the V2 edit within 24 hours.
5. For hooks: post about 20 variants, keep the best, launch about 5 as ads.
Checks: the page has enough baseline posts to compare against. Organic mechanics live in 13-ORG.
Rollback: if the page has no history, skip this step; read in paid with a small pack instead.

### P22. Build bottom-of-funnel objection ads (01, 08, 09)

Goal: 1 ad per objection with 1 proof point, for product-aware and retargeting audiences.
1. List objections from surveys, tickets, reviews, and (with consent) calls to checkout abandoners (R178). Estimate the mix; 01's illustrative split is 20% each for price, trust, quality doubt, not ready.
2. Price: value anchoring, cost per use ("half the price of a coffee"), a true bundle. Trust: customer and review counts, UGC testimonials. Quality doubt: the product in use, demos, compliant before-and-afters. Not ready: educational or lifestyle content. Warranty or lifespan: the guarantee. Efficacy: 1 substantiated claim.
3. 1 objection and 1 proof per ad; no benefit lists (08).
4. Load into a bottom-of-funnel pack, separate from top packs; expect it to convert well and spend less (R150).
Checks: each proof is true and current; the ad would make no sense to a cold viewer (that is fine).
Rollback: a bottom ad that spends like a top ad is mislabelled; move it.

### P23. Frame-by-frame teardown of a live video ad (09, 13)

Goal: a ranked fix list for an own or competitor video (competitor: structure only).
1. Watch once, then step through in 3-second chunks.
2. Hook: name the type; what does the viewer know after 3 to 5 seconds; is there a visual hook; would only the target buyer stop?
3. Bridge: does it say a solution exists and teach, or name the product and list benefits?
4. Body: when does education start; when does the value proposition appear (7 to 10 seconds in is late); features tied to benefits, benefit first; table-stakes passed fast.
5. Objections: at least 1 answered before the CTA.
6. Proof: every claim backed on screen; subjective superlatives flagged.
7. Pace and look: any stretch over 3 seconds with no visual change in a polished format; long talking head with no overlays; studio rig vs native setting.
8. CTA: soft or hard, fits the tone; scarcity true; loops closed.
9. Swap-the-face test for founder or creator ads.
10. Click the destination.
11. Score against the brand's 7-out-of-10 bar; rank fixes; do not predict ROAS from the review.
Rollback: none; this is a read.

### P24. Brief a native short-form format for TikTok or Reels (18)

Goal: a creator brief for 1 of the 7 native formats, chosen by product trait.
1. Pick the format from R116 by product trait; skip reaction if the product gives no strong first-use response.
2. Write the relatable first line in the buyer's words (habit, annoyance, restriction).
3. Structure: hook first, raw story or demo in the middle, product and CTA at the back.
4. For comparisons: a generic "old way" shown failing honestly; no rival brands; no exaggerated staging (R174).
5. For misconception videos: cite only a source the team has checked (R56, R170).
6. For transformation teasers: tease or show the result; body-image claims cleared (P19).
7. Plan comment-reply follow-ups for the questions the video draws (R118).
8. Rights: organic, affiliate and paid use written into the agreement (R112).
9. Judge on purchases per view, not views (R117). `[needs brand data: views, orders per video]`
Rollback: high views and low sales means the demonstration is weak; improve the demo, not the reach.

### P25. Portfolio and gap audit (01, 02, 05, 12)

Goal: a monthly view of coverage, concentration and sameness.
1. Tag every live ad: concept, persona, angle, offer, format, stage, source pillar, creative type (R168).
2. Concentration: spend share of the top 1 to 3 ads this month and the trend (R126). Bad: a few ads hold most spend with no new winners behind them.
3. Stage coverage: share of assets and spend by stage; bad: mostly product aware (R20).
4. Format and pillar coverage: any pillar or format family with nothing live (R27, R111).
5. Sameness: cold frequency above 2 at ad level over 30 and 60 days; ask for the Creative Similarity Score (R151). `[verify UI]`
6. Desire vs pain tag on each ad; target 60/40 to 70/30 pain-led for shoot-heavy brands (R29).
7. Gap matrix: segments in comments and reviews with no ad; formats and styles competitors run that the brand has not tested (R158).
8. Output: the gaps and concentration risks feed the next concept board (P3) and volume plan (P12).
Rollback: none; this is a read. Act 6 to 8 months before a hero-ad decline would bite (01).

## 5. Diagnostic checklists

Written so a worker can run them without the sources. Each row: what to check, how, good, bad, fix, source.

### 5.1 Static ad review

| check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| Spectrum end | Ask "clear enough to sell, or curious enough to pull a click?" | Clearly one end | Middle ("Guaranteed energy in 5 minutes", a brand slogan) | Push to one end or drop | 03, 07 |
| Gap the reader cares about | If curiosity: would the target buyer want this answered for their own benefit? | Yes ("Symptoms of vitamin deficiency") | No ("We don't stop improving") | Rewrite around the buyer's problem | 07 |
| Stage of the image | What must the viewer already know to get it? | Cold ads lead with problem, persona or "new" | Plain product shot to cold | Rebuild at a higher stage | 03, 10 |
| Image and copy stage match | Classify image stage, then copy stage | Same | Product-aware image, solution-aware copy | Change one so both match | 03 |
| First eye stop | Glance for 1 second, name what you saw | Problem, persona call-out or highest-awareness message | Category name, brand-centred line, no-context tagline | Resize and recontrast | 03, 07 |
| Eye path | Follow the eye 3 to 4 stops | Each stop answers the last one's question | Reader hunts for what the product is | Add 1 bold line saying what it is | 03, 07 |
| Image-headline fit | Substitution test with a generic image | Headline only makes sense with this image | Headline still fine, or now meaningless | Rewrite as 1 unit | 07, 03 |
| Headline job | Product-shot static: 5 to 6 words answering "why this instead?" | Specific moment, money, persona plus problem | Generic promise a substitute gives too | New angle | 07 |
| Benefit order | Read each claim as a non-expert | Plain outcome first, mechanism in brackets | Jargon first | Flip order | 07, 09 |
| Text density and legibility | View at phone size | All lines readable; no repeats of the headline | Small sub-heads, redundant call-outs, unreadable graph | Enlarge about 30%, cut repeats, remove graph | 07, 03 |
| Layout craft | Spacing, alignment, case, product placement | Clean | Product off to one side, random caps, awkward gaps | Fix layout | 03, 07 |
| Logo | Is the brand shown by the page name? | Logo absent, or a deliberate reveal on a native static | Unknown logo in the corner | Remove | 03, 07 |
| Proof | Is there a review with stars or name, a true number, a real product shot? | Present and legible | Unattributed line, staged product | Add credibility markers, real shot | 03, 07 |
| Numbers | Trace each to a source | All sourced | Any invented or unsourced figure | Remove | 07, 10, 13 |
| Primary text | Does it carry the education the image withheld? | Persona call-out, story, late reveal | Empty, or repeats the image | Write it (11-ADC) | 03, 07 |
| Destination | Click it | Curiosity to an educational page; clear offer to PDP; offer congruent | Curiosity to PDP; 404; generic page | Build or switch page | 03, 04, 09 |
| Concept or variant | Did persona, angle or offer change vs live ads? | At least 1 changed | Only design, colour, pose | Count as a variant or drop | 03, 05 |
| Product accuracy | Compare product in image with the real photo | Real product | AI redraw | Composite the real photo | ecomOS |
| Competitor trace | Compare with any reference ad | Layout or mood only | Their text, product, face, logo | Rewrite | ecomOS |
| Compliance | Run checklist 5.4 | Pass | Any flag open | Fix before launch | all |

### 5.2 Video script review

| check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| Hook type | Name it | Nameable and about the buyer's problem | "These are my vital packs"; a prop with no link to the problem | Rewrite hook | 09, 13 |
| Who stops | Would only the target buyer have a reason to stop? | Yes | Anyone curious (meme, mystery food, knife) | Add persona or problem | 01, 04, 13 |
| Hook layers | Audio, on-screen copy, visual each planned | All 3 working | Captions only; static frame; product named | Fix the weakest layer | 01, 04 |
| Grade | Clarity, relevance, novelty, specificity, credibility | 2 or more strong, clarity and relevance not both low | Low clarity and low relevance | Rewrite | 01, 04 |
| Hook-body stage | Classify both | Same stage | Curiosity hook into a feature tour | Change one | 13 |
| Speaker fits persona | Look at who says it | Plausibly the persona or a trusted expert | Mismatch | Recast | 04 |
| Product in hook | First words, first frames, top of primary text | Absent for cold; allowed for product-aware, demo or partnership formats | Product on screen and named by word 3 in a cold ad | Move product later | 04, 13 |
| Bridge | Read the line after the hook | "A solution exists", then why the problem happens | "The solution is our product" plus benefits | Rewrite bridge | 04, 09, 11, 13 |
| Mechanism | For each claim, ask "why does it work?" | Each ingredient or feature has its why; terms explained; prevalence proven and sourced | Claims only; clinical word dropped | Add the why | 11, 12, 13 |
| Awareness curve | Second by second: does the viewer know it is an ad for a product yet? | Near 0 through hook, slow rise, peak at CTA | Stepstones up at each section | Pull back and teach | 04 |
| Benefits vs features | List features | Each tied to a benefit, benefit first; table-stakes in 1 line | Feature list; whole ad on table-stakes | Flip and cut | 09, 13 |
| Objections | List the buyer's doubts | At least 1 answered before the CTA, from customer data | None | Add a line or numbered reason | 09, 11, 13 |
| Proof | For each claim, what is on screen? | Tests, labels, certificates, counts, matched testimonials | "Best in the world", "trust me" | Overlay proof or cut the claim | 02, 09, 10 |
| Close | Read the last 20% | Reason to buy, risk reversal, clear CTA at the right intensity, loops closed | Jump from education to offer; hard pitch on a soft creator ad; new loop in CTA; abrupt end | Rewrite close | 02, 04, 09, 11, 13 |
| Scarcity and offer | Check store and dates | True and live | Invented urgency; stale discount | Remove or fix | 09, 13 |
| Motion | Scrub the timeline | Cuts, overlays, B-roll, camera moves throughout; polished formats cut every 3 seconds or faster | Static talking head through a long script | Re-edit | 02, 09, 13 |
| Setting | Look at the frame | Native (car, home, store) or deliberate | Visible studio rig on a founder or creator ad | Reshoot native | 13, 18 |
| Low-fi and product | Is the product in low-fi footage? | Product only in high-end shots | Yes | Re-edit | 02 |
| AI tells | Search "isn't ... it's", stock analogies | None | Contrast negation, "single soldier" | Rewrite plainly | 01, 13 |
| Expert precision | Have a category expert read it | No overlaps or errors | "Electrolytes, magnesium" | Fix terms | 13 |
| Market width | Compare persona with real buyer mix | Covers the main market or is a deliberate persona slice | Positions a mass product to an elite niche | Re-angle | 13, 09 |
| Swap-the-face | Would it work with a different presenter? | Yes | Only for the founder's fans | Add problem, mechanism, proof, or run organically | 09 |
| Destination | Click it | Loads and holds the promise, continues the story | 404, generic PDP | Fix | 09, 11 |
| Compliance | Run checklist 5.4 | Pass | Any flag | Fix | all |

### 5.3 Concept board review

| check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| Real concepts | For each row, did persona, angle or offer change vs the others? | Yes | Rows differ only in format or design | Mark as variants of a parent | 01, 03 |
| Angle written | 1 sentence: who, product, why, proof | Present, in customer words | Feature list, or team's idea with no quotes | Return to P1 | 01, 10 |
| Persona sharp | Problems, desires, triggers | Specific ("mom who tried 6 supplements") | Demographic label | Rework (P2) | 01, 12 |
| Mechanism | Problem cause and solution cause | Both, simple, new | Missing or vague | Add | 12 |
| Offer | Named value framing, margin checked | Bundle, GWP, tiered, subscription, or single with reason | "Discount" only | Rework with 03-OFF | 01 |
| Stage weight | Count rows by stage | At least 70% unaware, problem or solution aware | Mostly product aware | Add cold rows | 01, 02, 03 |
| Bottom rows | 1 objection, 1 proof each | Yes | Benefit lists | Split | 08 |
| Proof available | Column filled per row | Real, dated proof | "We'll find something" | Drop or research | 02, 10 |
| Destination | Page per row | Matches stage and spectrum end | All rows to PDP | Plan pages with 07-LPG | 03, 11 |
| Format after concept | Format column filled last | Chosen by the 5 questions and economics | "UGC" as the concept | Rework (P4) | 01, 10 |
| Ads per concept | Count planned ads | 10+ for lead concepts, 4 to 8 per pack | 1 to 3 | Add or cut concepts | 01, 15 |
| Diversity | Creative type and format across rows | Several types | 100 of the same ad | Add types | 16, 05 |
| Idea sources | STORMING letter per row | Several sources | All swipes or all own head | Pull from research, matrix, new styles | 12 |
| Hypothesis | 1 variable per row | Stated | "Test it" | Write it | 01, 10 |
| Brand fit | Voice and category norms | Fits | Health-DR tone on a gifting jewellery brand | Adjust | 12, 16 |
| Compliance flags | Any health, attribute, competitor, before-and-after row flagged | Flagged for P19 | Unflagged | Flag | all |

### 5.4 Compliance check

| check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| Every number sourced | List numbers; find the document behind each | All traceable | Made-up or "even if there wasn't" | Remove | 03, 07, 10, 13 |
| Health or body claim | Flag appetite, weight, hair, skin, gut, BP, fertility, jawline, disease | Substantiated and policy-checked | Unchecked | Check policy `[web check]`, then keep or cut | 02 to 18 |
| Before-and-after | Any transformation imagery | Illustrated or framed within policy | "Sneak it past review" | Reframe | 01, 07 |
| Personal attribute | Copy implies race, condition, sexual function, body shape | Cleared or rewritten | "All black men struggling with erections" | Rewrite | 12, 16 |
| Fake formats | Interview, whistleblower, news style, invented person | Clearly the brand's own content, no impersonation | Fake interview or actor presented as real | Cut | 12 |
| Reviews and stories | Every review, email, founder fact | Real, with permission, consistent | Scripted review as real; altered story | Cut | 02 |
| Disclosure | Creator or founder handle, brand-owned pages | Partnership label; page presented as the brand's | Undisclosed whitelisting; "independent" review site | Label and disclose | 01, 03 |
| Competitors | Names, logos, packaging, faces, text | Generic "old way" only | Rival shown or copied; staged failure | Rewrite | 08, 18, ecomOS |
| Likeness and image rights | Every face and image | Licensed | Public figure without consent; found image | Replace | 11, 13 |
| Product accuracy | AI images | Real product composited | Redrawn product | Replace | ecomOS |
| Offer and scarcity | Compare with live store and dates | Match | "Before stock runs out" for 20 weeks; stale discount | Fix or remove | 09, 13 |
| Research consent | Abandoner calls, comments used | Consent on file | None | Stop | 08 |
| Record | Pass, fix, reject per line, attached to the test plan | Filed | Missing | File | this playbook |

### 5.5 Winner analysis

| check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| Is it a winner by the pre-set definition? | Spend share, CPA or incremental ROAS threshold, days | Clears it with outsized results | At threshold, or only high ROAS on tiny spend | Leave alone, or mark "low-spend or retargeting candidate" | 08, 17, 10 |
| Read level | Ad set or campaign, 7-day click or incremental, existing customers excluded | Yes | Ad-level last click | Re-read | 01, 15, 17 |
| Spend artefact | Compare sales share with spend share | Wins on supporting metrics too | Wins only because it got the spend | Watch the ad; check chain | 10 |
| Chain | Hook rate, hold rate, CTR vs link CTR, on-site conversion | Consistent through to purchase | High CTR, big link-CTR gap, no buying | Not a winner; empty attention | 10, 01 |
| DNA filled | Segment, concept, angle, mechanism, copy blocks, hook, format, CAST | All fields | Blank fields | Complete | 12 |
| Hypothesis | 1 element or a combination named | Written | "It just works" | Test 2 candidates | 12, 13 |
| Segment grades | Hook, bridge, body each graded | Strong parts named | Only overall verdict | Grade each | 13 |
| Funnel role | Combined metrics | Opener, closer or retargeting assigned | Assumed from the brief | Assign | 08, 10 |
| Scale test | Metrics as budget rises | Holds | Falls apart above test budget | Low-spend role | 10 |
| Portfolio effect | Profit at its spend vs other concepts | Adds profit | Cutting a profitable 2x to feed a 10x on $500 | Keep both | 17 |
| Iteration plan | Levers to rotate, decent swings, new pack | Written | 1-word headline change; into the winning ad set | Rewrite plan | 15, 17, 01 |
| Tagged | Library and gap matrix updated | Yes | No | Update | 05, 12 |

### 5.6 Hook review (short form)

| check | good | bad | fix | source |
|---|---|---|---|---|
| Right viewer stops | Only the target buyer has a reason | Anyone curious | Persona or problem call-out | 01, 04, 13 |
| Clarity in 3 seconds | Stranger knows what it is about | Confusion | Add category or problem | 04, 09 |
| Relevance | Pain obvious | Demographic label without pain | Agitate the problem | 01, 04 |
| Novelty | Not done a million times | "Number 1 mistake..." | New type or format | 01, 04 |
| Specificity | True number or name | "Some problems" | Use the real figure | 04 |
| Credibility | Delivered by someone the persona trusts | None, or unlicensed famous face | Recast; clear rights | 01, 13 |
| Layers | Audio, copy, visual all planned | Visual only, or captions only | Plan all 3 | 01, 04 |
| Sells in hook | No product, no offer | Product named | Move product later | 04, 13 |
| Bridges | Natural into the body | Hook topic missing from body | Cut the hook | 02, 04 |
| Lever spread | Hooks differ on angle, offer, avatar or format | Wording-only variants | Add visual or avatar change | 19 |
| Count per wave | 2 to 4 per body (up to 8), budget-sized | 20 to 40 per body at $1,000 a day | Wave it | 02 |

### 5.7 Test read and pack health

| check | good | bad | fix | source |
|---|---|---|---|---|
| Pack purity | 1 persona and 1 angle | Mixed | Move ads | 01, 08, 15 |
| Pack size | 4 to 8 (min 3) | 1, or more than the budget can read | Split or merge | 01, 15, 17 |
| New ads placement | New pack | Added to a winning ad set | Move; note learning reset | 01, 08, 17 |
| Delivery guarantee | Stated in plan; floor removed on day 7 | Floor left on; or no plan for starvation | Fix in plan | 15, 17 |
| Floors vs budget | Packs with floors x floor fits inside daily budget | Exceeds | Cut packs | 17, computed |
| Read day | Day 7 first, day 14 decision | Day 2 kill | Wait | 10, 15, 17 |
| Delivery per ad | Every ad got spend | Most got none | Inconclusive; rerun smaller | 10 |
| Winner definition | Set before launch | Set after | Set now, apply next time | 08, 17 |
| Hypothesis answered | Expected vs actual written | Not recorded | Record | 01 |
| KPI-hitting ad set | Untouched | Ads cut or added inside it | Stop | 01 |
| Exclusions | Existing customers excluded from cold packs | Not excluded | Fix with 24-DEP | 01, 08 |

### 5.8 Portfolio health

| check | good | bad | fix | source |
|---|---|---|---|---|
| Hero dependence | Top 1 to 3 ads hold a falling or modest share; new winners behind them | A few ads hold most spend, nothing behind | Production now; 6 to 8 months of lead | 01, 02, 05 |
| Stage coverage | 70%+ of assets cold-stage | Mostly product aware | Cold rows in P3 | 01, 02, 03 |
| Format and pillar coverage | Several formats; all 3 pillars live | 1 format family or 1 pillar | Add | 01, 05 |
| Cold frequency | Under 2 at ad level, 30 and 60 days | Above 2 | More distinct concepts | 01 |
| Similarity | Score low (via rep), or reach steady as frequency holds | Frequency up, reach down, ROAS down together | Change persona, angle or offer, not just the shot | 01 |
| Desire vs pain | 60/40 to 70/30 pain-led for shoot-heavy brands | 90/10 desire | Add pain-led rows | 01 |
| Production vs media | Within tier (25% then about 10%) or justified by per-ad economics | 15 live ads on $350K a month | Fund production | 01 |
| Hit rate trend | Stable or rising with volume | Falling as volume rises | Cut volume, raise bar | 08 |
| Live ad count vs spend | About 1 new ad per $1,000 monthly spend, or the model's number | Far below | Volume plan (P12) | 01 |
| Inventory alignment | Winners squeezed or breathed by stock and cash | Stockouts from a squeezed winner; stock piling | Rebalance with 20-FIN | 01 |

## 6. Thresholds and benchmarks

One table for the folder. Confidence: how many independent sources agree (same-agency sources count once), and the evidence type. No figure here is measured with a control; all are practitioner rules or single cases.

| value | condition | source(s) | confidence |
|---|---|---|---|
| Viewers lost at the hook: about 80% (19: 80% to 90%) | video ads; premise, not data | 01, 04, 11, 19 | low (2 agencies, unsourced) |
| Viewers reaching the second half: about 15% | video; presenter estimate | 09 | low (1 source) |
| Hook window: first 3 seconds (hook rate = views past 3 s); 3 to 5 s in 09 and 19; 0.5 s to earn attention in 16 | every hook | 01, 04, 09, 16, 19 | medium that it is short; low on the exact number |
| Hold rate: views past 15 s (1 of several definitions) | video diagnostic | 01 | low |
| Hook and hold rates do not correlate with conversions | reading video | 01 | low (1 source) |
| Product first shown: not in the first 2 to 3 s of a story format; B-roll or product held to about 20 s; VSL reveals at about 1.5 min in 1 example; demo formats can show it in 3 s | cold video | 01, 02, 04, 13 | medium on "late" for education ads; conflict C1 |
| Cut pace: at least every 3 s in polished formats | video, Instagram stressed | 09 (13 header only) | low; conflict C7 |
| Extra mechanism before product: 4 to 6 s | education-led VSL | 13 | low |
| VSL length: about 90 s to 20 min; 3 to 4 min normal; cuts to 2 to 3 min and 45 s | VSLs | 11, 13 | low to medium |
| Hooks per body per launch wave: 2 to 4, up to 8 | video tests on modest budgets | 02 | low; conflict C10 |
| Hooks to test on a finished VSL body: 3 to 6 | VSL | 11 | low |
| Hooks per revival: more than 3, target 10 | fatigued proven body | 19 | low |
| Hooks recorded per shoot: about 6 takes each; 10 hooks x 3 bodies = 30 ads in 4 to 5 min camera time | shoot planning | 01, 02 | low (same agency) |
| Variants from 1 hook by layer swaps: 20 to 30 | volume from 1 concept | 04 | low |
| Effort: 2 bodies x 15 hooks beats 2 hooks x 5 bodies; 10 hooks ≈ 1 body | body scripts already good | 01, 19 | low (same agency) |
| Hook refresh case: 50 new hooks bought another $100K at same efficiency on ads that had spent $50K to $100K | 1 case | 01 | example only |
| Scene change case: +$40,000 spend, same script | 1 case | 02 | example only |
| Revival case: 2 bodies x 9 hooks at launch; 4 hooks x 2 bodies at revival; fatigue after 6 to 7 months; 5x better than the account | 1 case | 19 | example only |
| Static consumed in about 4 s; clarity end must land in 3 to 4 s | statics | 03 | low |
| Static headline: 5 to 6 words on a clean product-shot static | statics | 07 | low |
| Unreadable sub-heads: enlarge about 30% | statics | 07 | low |
| Minor variation effect: maybe 1% to 2%, unmeasurable | background, pose | 03 | low |
| Static vs video production: about 4 statics (3 great) per 60 to 90 s video; AI static about $1 or "a few dollars" | production planning | 03, 05, 15 | medium that statics are far cheaper; low on the figures |
| Expected GP per ad example: static $880 vs video $700 at 10x; $480 vs $300 at 2x ($1,000 revenue, $20 vs $200 production) | worked example | 03 | example only |
| Ads per concept: 10+; about 20 at a 5% hit rate | new concept | 01 | low |
| Ads per pack: 4 to 8 sweet spot; 2 to 10 seen; minimum 3 | packs | 01, 15, 17 | medium (2 agencies) |
| Hit rate: 5% normal; range 5% to 15% | large accounts | 01, 03, 08 | medium (2 agencies, no data shown) |
| Winner definition: spend > 5% of campaign budget AND at target CPA (08); high spend AND above incremental ROAS threshold (17); top incremental revenue (15) | pre-set per test | 08, 15, 17 | medium that a definition is needed; low on any one formula |
| Example incremental ROAS bar: about 1.1 on new customers; leave 1.13 and 1.16 alone | 1 brand | 17 | example only |
| Example incremental vs reported: 1.23 vs 1.42 on $97,000 | 1 brand | 17 | example only |
| Ad set daily minimum: 1x target CPA, capped at 20% of budget; remove on day 7 | new packs | 15, 17 | low (same agency); conflict C5 |
| Forced spend per pack at the floor: up to 7x target CPA over 7 days | computed from 15 and 17 | this playbook | arithmetic |
| Impression cap per ad: 1,000 then 800 at $50 to $70 CPM; 13 ads at $30 a day | very small budget | 10 | example only |
| Days to a first read: 7; winners within 1 to 2 weeks; 14-day analysis window | packs | 10, 15, 17 | medium |
| CTR vs link CTR: 10.9% CTR with a drop over 3% and little buying vs 6.3% with a drop under 2% and buying | 1 pair of ads | 10 | example only |
| Cold frequency ceiling: under 2 at ad level, 30 or 60 days | cold campaigns | 01 | low |
| Identical creative helps up to 2 impressions, then purchase probability collapses | paraphrased Meta article | 01 | low, `[web check]` |
| Mean spend per ad: about $700 to $1,500; revenue per ad about $2,000 | 1 agency's accounts | 01 | low |
| Creative volume: 1 new ad per $1,000 of monthly spend | fallback | 01 | low |
| Churn model example: 2 of 10 winners churn, 5% hit rate, 40 ads a month | forecast | 03 | example only |
| Production budget: founder time under $30K a month; 25% of media at $30K to $100K; about 10% above $100K | tiers, AUD | 01 | low |
| Testing budget share: 60% to 80% at $4K to $30K a month | small brands | 01 | low |
| Active concepts: 3 / 5 to 6 / 8 to 10 by tier; creators 2 to 3 / 4 to 6 | tiers | 01 | low |
| New creatives per month: 30 to 100 at $30K to $100K; 100+ above | tiers | 01 | low |
| Funnel weight: 70% to 90% TOF, about 20% MOF, 5% to 10% BOF (01); most in stages 1 to 3, about 20% in 4 and 5 (02); 5/5/5 (05); extremes only (08) | portfolio | 01, 02, 05, 08 | medium that cold dominates; conflict C4 |
| Sourcing split: 1/3 in-house, 1/3 UGC, 1/3 AI | starting heuristic | 05 | low |
| Distinct formats live: 10 to 15 | portfolio | 05 | low |
| Production effort: replication 50% to 60%, iteration 20% to 30%, net new 20% to 30% | batch planning | 01 | low |
| Desire vs pain: from 90/10 to 60/40; best about 70/30 pain-led | shoot-heavy brands | 01 | low |
| Partnership ad lift: 5% to 30%, not 10x; up to 40% of spend in some accounts | founder or creator handles | 02, 01 | low (same agency) |
| Founder camera ramp: first about 10 hours robotic | new founders | 02 | low |
| Content team volume: 200 to 400 ads a month with 1 to 2 people | systemised founder pipeline | 02 | example only |
| UGC lead time: 1 to 4 weeks; 2 to 3 videos per sample; seeding case 100,000 invites, 6,000 creators, about 5,800 videos in 60 days | creator army | 05 | example only |
| AI output usable: about 50% with deep context | AI statics | 15 | low (1 run) |
| Manual research: 3 to 4 days for a new niche; about 80% of time on research and concepting | before production | 16, 03 | low |
| Personas by hand: 20 to 40, then LLM roughly doubles | persona list | 01 | low |
| Hero-ad decay: 8 to 10 clients 40% down YoY after 3 creatives held $1M; fix 6 to 8 months earlier | 1 agency | 01 | example only |
| Junk volume: 2,000+ ads a month at about $4M a month, unprofitable | 2 accounts | 01 | example only |
| Quality bar: 7 out of 10 | before volume counts | 01, 09 | low |
| Pareto: 4% of ads hold about 64% of spend and revenue under CBO | account reads | 01 | low |
| VSL account: 2.5 to 3 ROAS on new customers, 150% profit lift after year 1, 1 VSL spent $360,000 | 1 account | 11 | example only |
| TikTok views vs sales: 34.5M views for 13,000 units; 78,000 views for 850 units | 7 public videos | 18 | example only |
| Bundle: about $4.99 unit to $25 to $30 AOV via 3, 5, 6 packs | low-ticket consumables | 18 | low (inferred) |
| Objection mix illustration: 20% each price, trust, quality doubt, not ready | BOF planning | 01 | illustration only |
