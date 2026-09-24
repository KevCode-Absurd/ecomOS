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
