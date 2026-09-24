# 19-WLD-wild-bets playbook

version: 2.0-draft  |  date: 24 Sep 2026  |  sources: 3  |  cards: 96  |  built from: sources/*.md

## 0. How to use this playbook

**Ecommerce first.** This playbook is for ecommerce stores, not general marketing or startup audiences. Section 3.0 is the priority order: a ranked list of the levers below by what matters most for a store right now. Load 3.0 first. Store-type conditions (single hero SKU vs catalogue, low vs high AOV, subscription vs one-off, marketplace-heavy, luxury or considered purchase, mobile-first India vs US) decide which rules in section 3 apply to the brand at hand.

**Who runs it.** The wild bets agent. It designs, bounds and reads out unconventional offer, retention and customer experience plays that sit outside the paid auction: handwritten notes, founder videos, surprise gifts and artifacts, programmatic direct mail, keep-it refunds, lifetime warranties, outcome guarantees, VIP tiers and invite-only access, limited drops, referral waitlists, expiring loyalty value, proactive subscription pauses, no-ads weeks, guerrilla and mystery launches, brand stunts, values plays and hedged promotions. It does not run paid media, email flows, standard post-purchase or SEO.

**Autonomy level: L1, draft for approval.** Every play in this playbook is L1 in ecomOS. The agent drafts the bet brief, the economics sheet, the control design, the customer-facing wording, the approval request and the readout. A human approves and executes. The agent sends no note, ships no gift, issues no refund, changes no policy, edits no loyalty program, places no hedge and contacts no customer. Meta stays read-only. This is an ecomOS rule, not a source rule. Where a step below says "send", "issue" or "launch", read it as "draft for a human to send, issue or launch".

**3 rules that sit above every other rule here.**

1. Fix effort before delight (rule B1). No wild bet goes to a customer with an unresolved service failure, and no wild bet launches on a base that is high-effort.
2. Bound before launch (rule C1). Every bet has a written hypothesis, cohort, cash and labor cap, metric, control, duration, stop rule and registry entry before the approval request goes out.
3. A case result is an example, not a promise (rule D1). No number in this playbook is a benchmark. Every number in section 6 carries its source and its confidence.

**Which sections to load for which task.**

| Task | Load |
|---|---|
| Decide whether a wild bet is right for this brand now | 0, 3.0, 1, 2, 3 groups A and B, 5.5, 7 |
| Design and bound 1 bet | 3 groups C and D, 4 (P1), 5.1, 5.2, 5.3, 9.2 |
| Build the quarterly plan (3 bounded bets) | 3 group A, 4 (P1, P3), 6, 9.1 |
| Stage 1: notes, founder videos, keep-it refunds | 3 groups E, F, J, 4 (P3, P4, P5, P11), 5.6, 5.10 |
| Stage 2: VIP tier, inserts, founder channel | 3 groups M, H, 4 (P9, P16), 5.9 |
| Stage 3: referral waitlist, limited drop | 3 groups M, N, 4 (P10, P12), 5.9 |
| Stage 4: stunt, anti-discount or values play | 3 group O, 4 (P18), 5.7, 7.1 |
| Programmatic direct mail | 3 group G, 4 (P6), 5.3, 5.8, 10, 11 |
| Gifts, artifacts, Chewy-style art, rep budget | 3 groups H and I, 4 (P7, P8), 5.6, 7.2 |
| Guarantees, warranties, keep-it refunds, price locks | 3 group J, 4 (P5, P14, P15, P19), 5.10, 7.5 |
| Subscriptions: pause, cancel, bereavement, 100 days | 3 group K, 4 (P14, P19), 7.4 |
| Loyalty mechanics: expiring value, delayed discount, daily reveal, flash sales, mystery bundles | 3 group L, 4 (P13, P23), 7.3, 7.9 |
| Hedged event promotion | 3 group P, 4 (P17), 5.2, 5.7 |
| No-ads week, founder's inbox, 20-customers exercise | 3 group Q, 4 (P20, P21) |
| Read out a finished bet and file it | 3 group D, 4 (P22), 5.4, 9.3, 9.4 |
| Any point where sources disagree | 7 |
| What cannot be known without brand data or the web | 10, 11 |

**Fetch before acting.**

- From brand data: customer list ranked by lifetime spend and order count; repeat-purchase rate and 90-day reorder rate by cohort; AOV; gross margin by SKU and per bundle; LTV distribution (top 1%, top 5%, top 50, top 200 shares of revenue); support metrics (Customer Effort Score, first-contact resolution, resolution time, transfers per ticket, contacts per order); returns data (cost per return, resale recovery, return reasons by SKU, keep-it claims per customer); subscription data (consumption per SKU, cadence, skip and pause history); loyalty data (earn and burn rates, points liability, share of signups through loyalty); organic vs paid revenue share; SMS and email consent status by customer; address data quality. Full list in section 2 and section 10.
- From the data layer: order history joined to customer id (Shopify or Metabase for Gehna); support tickets; loyalty and subscription tool exports; Meta spend and orders for the no-ads week baseline (read only).
- From the web: every `[web check]` in section 10 that touches the play at hand. All 3 sources are 2025 to 2026 compilations of second-hand cases; program terms, vendor features and consent law move.
- From the user: which brand (Gehna, Peach Bucket, TrailFold: keep them apart); brand voice (irreverent or serious); cash cap for the quarter; labor hours available for manual touches; risk appetite for public promises; whether a physical mail vendor, loyalty app or subscription tool is already in place.

**Neighbours.** Standard offers and discount design: 03-OFF. Email and SMS flows: 14-EML. Standard post-purchase, returns and support process: 17-CXP. Paid media, ROAS and incrementality tests: 24-DEP and 06-MEA. Creative for any stunt or ad: 10-MCR. SEO and AEO: 15-SEO, 16-AEO. Product research and channel expansion beyond a small test: 01-PRD, 22-AMZ.

## 1. Scope and outcomes

**Covers.** How to decide whether a wild bet fits a brand. The order of operations: fix effort, then run cheap and manual plays, then status plays, then demand plays, then 1 big swing. How to bound any play with a cap, a cohort, a control, a metric, a duration and a stop rule. A catalogue of about 30 plays, each with conditions, cost where a source gives one, the cohort it fits, the reported effect as an example, and a bounding template. How to read out a bet on relationship metrics, keep earned attention separate from incremental contribution, and file the result so the next bet learns from it.

**Does not cover.** Discount ladders, bundles as offer architecture, pricing tests (03-OFF; card 6812a43572e9 on bundles is recorded here because its source sits in this folder, but the offer design belongs there). Email and SMS flow build (14-EML; this playbook says when a physical or manual touch should fire on the same trigger). Returns process, support tooling and standard post-purchase sequences (17-CXP; this playbook only sets the "fix effort first" gate and the keep-it refund pilot). Paid media structure, ROAS and holdout tests on ad spend (24-DEP, 06-MEA; the no-ads week borrows their read). Creative production for stunts (10-MCR). Product development and marketplace expansion (01-PRD, 22-AMZ; group S records the sources' product and channel bets in brief and points there).

**Business measures it moves.** Repeat-purchase rate and 90-day reorder rate of treated cohorts vs control. Retention and AOV of VIP members vs non-members. Referral share of signups. Full-price sell-through of drops. Return cost per order and keep-it claim rate. Refund rate before and after a guarantee. Subscription pause-to-resume rate and early churn in the first 100 days. Customer Effort Score, first-contact resolution and resolution time on the operational base. Incremental contribution after all program costs. Earned media, UGC and referral volume, tracked separately as signals. Organic revenue share (the faucet test).

## 2. Inputs the agent needs

| Input | From where | Required or optional | Why |
|---|---|---|---|
| Customer list ranked by lifetime spend and by order count, with first and last order dates | Brand record, data layer | Required | Picks the top 10, top 50, top 200 and top 1% cohorts (rules E1, M1); source 03's "top 1% drive most revenue" is asserted, not shown, so the share must be measured |
| Repeat-purchase rate and 90-day reorder rate by cohort, with history | Data layer | Required | The Stage 1 pass mark and the keep-it readout (rules C2, J3) |
| AOV and gross margin by SKU, category and bundle | Brand record | Required | Sizes the rep budget, gift cost, keep-it threshold, warranty and price lock exposure (rules I1, J1, J4, J7) |
| Revenue share of top 1%, top 5%, top 50 and top 200 customers | Derived from the list | Required | Tests the top-1% claim before a VIP tier is built (rule E1) |
| Support metrics: CES, first-contact resolution, resolution time, transfers per ticket, contacts per order, repeat contacts | Support tool export | Required | The fix-effort-first gate (rules B1 to B4); source 02 gives no pass mark, so a baseline is needed |
| List of customers with an open or recently closed failure (late, broken, billing) | Support tool | Required | Exclusion list for every delight play (rule B2) |
| Returns: cost per return (shipping plus handling), resale recovery rate, return reasons by SKU, returns per customer | Brand record, 3PL | Required for keep-it and warranty plays | Break-even and abuse check (rules J1 to J4); source 03 gives no formula |
| Defect and failure rates by SKU | Brand record | Required for warranty plays | Picks durable SKUs and models claims (rule J4) |
| Subscription data: consumption per SKU, cadence, skip and pause history, cancel reasons | Subscription tool | Required for group K | Overstock flag and pause readout (rules K1 to K3); source 02 gives no threshold |
| Loyalty data: earn rate, burn rate, points liability, share of signups through loyalty | Loyalty app | Required for group L | Expiry fairness check and acquisition read (rules L1, L2) |
| Organic vs paid revenue share, by week, last 12 months | Data layer (Meta read only, Shopify or Metabase) | Required for the faucet test and no-ads week | Baseline for rule A2 and P20 |
| SMS and email consent status per customer; address data quality | ESP, loyalty app, brand record | Required for reminders, drops and mail | Consent gate (rules C7, L1, M5, G9) |
| Zero-party preferences and support notes that record life events or stated tastes | Support tool, quiz or pop-up data | Optional | Feeds artifact gifts and frontline gifts (rules H1, H7, I2) |
| Brand voice statement (irreverent or serious) and values that are backed by a program | Brand record, user | Required | Stunt and values-play fit (rules A6, A8, O1, O7) |
| Quarterly cash cap and labor hours for manual touches | User | Required | Bounds every bet (rule C1) |
| Vendor quotes: handwriting service, direct mail vendor, artists, waiting room tool | Web, user | Required where the play uses them | Cost per piece for the economics sheet; only source 03 gives cost ranges |
| Local rules: consumer protection, contest and promotion law, warranty law, SMS consent, privacy (GDPR, India DPDP), prediction market legality, gambling-style mechanics | Web | Required for groups J, L, O, P and for SMS and third-party data | Rule C7; no source gives legal steps |
| Existing tools: loyalty app, subscription platform, ESP, pop-up tool, mail vendor | Brand record | Required | `[verify UI]` steps depend on what is installed |

## 3. Decision rules

Numbering: letter is the group, number is the rule. "Sources" names the mini playbooks (01, 02, 03) that state the rule. Source 03 is a folder brief that repeats several cases from 01 and 02 (Paul Graham, Chewy, Eleven Madison Park, Cards Against Humanity, Liquid Death); where 03 only repeats a case, it counts as the same source, not as independent agreement. "Card addition" means the card writer added a step or caveat the source text does not state. "Playbook addition" means this document added it to make the rule runnable; it is marked so a reader can strip it.

### 3.0 Ecommerce priority order

1. Fix effort before delight (B1 to B4). Every store; no wild bet on a slow return process.
2. Run the faucet test (A2). Every store; shows whether the domain matters yet.
3. Handwritten note or founder video to the top 50 or top 10 (F1). Cheap entry point for hero-SKU and catalogue stores alike.
4. Keep-it refunds under a price threshold (J1 to J3). Best where return cost is real on low-value, perishable or hard-to-resell SKUs; skip for luxury catalogues with few returns.
5. VIP tier for the top 1% (M1, E1). Needs a repeat-purchase base; ranks higher for catalogue and subscription stores than a single hero SKU.
6. Subscription plays: proactive pause, price lock (K1, K2, J7). Fires only for subscription businesses. `[general practice]` on the ranking.
7. Loyalty mechanics: expiring value, non-purchase rewards (L1, L7). Needs an existing program; low priority for a single hero SKU or a rarely-repurchased item.
8. Programmatic direct mail (G1 to G14). Ranks higher for higher-AOV catalogues (home, jewelry, apparel); the vendor list is EU, UK and US only, so rank lower for India stores until confirmed `[web check: PDM vendors in India]`.
9. Limited drop with real scarcity (M3 to M9). Best for single hero SKU or narrow-catalogue, higher-AOV brands with an audience already built.
10. Tiered referral waitlist (N1). Fits a launch or drop moment for any store type.
11. Lifetime warranty or outcome guarantee (J4, J5). Best for durable, higher-AOV, considered-purchase SKUs.
12. Stunt or values play (O1 to O13, P1). Last, only after earlier stages pass. `[general practice]` that it sits last.

`[general practice]` covers the ranking order and store-type conditions above; the rule ids are the playbook's own. Load this block first; the groups below are the detail.

### Group A. What counts as a wild bet, and how to pick one

**A1. A wild bet is a deliberate break of a category norm, run outside the paid auction, that is cheap to run and hard to copy.** Condition: the brand can name the norm it breaks, the adjacent industry it borrows from, and the cash cap. Does not apply to standard tactics (10% off, BOGO, free-shipping thresholds, points programs, abandoned-cart emails); source 03 says skip them "unless there is a genuine twist", and none of the 3 sources says how to pick the twist. Norms the sources list as breakable: "you must spend on paid ads to grow", "never link off your site", "loyalty points should never expire", "discounts are the only way to drive urgency", "you can't sell big-ticket items online", "you need a physical store to build community". Sources: 01 [a7b8a9aa106c] [68c4bfa88afe]; 02 [b5a1ffc627e1] [ab3039ede71f]; 03 [24e7dd3a3012].

**A2. Run the faucet test before picking a bet.** Ask: if paid ads stop tomorrow, does revenue vanish? Measure organic vs paid revenue share, or run the bounded no-ads week (P20). Condition: source 01's framing (Last Crumb founder Derek Jaeger). Card caveat: a brand with strong paid economics may stay ad-led on purpose; the test sizes the dependence, it does not condemn it. Sources: 01 [9b43d5332e59] [56c8c219238a] [3043fc9b1846]. `[needs brand data: organic vs paid revenue share, by week]`

**A3. Fund 1 wild bet lever per quarter from the shared cash cap; do not split it across the discount ladder, the loyalty program and a drop at once.** Condition: 1 play per cohort per test window so the control stays clean (see C3). Sources: 01, as the card's reading of the cases, not a stated rule [9b43d5332e59]; 02, card addition [246d16432222]. Strictest condition kept: 1 play per cohort at a time.

**A4. Size the quarter's 3 bets so all 3 failing stays under a share of quarterly contribution margin, not revenue.** Source 01 says "limited downside, unlimited upside" and asks: what is the worst case, can I hedge it, can I test it on a small segment first? Card a7b8 rewrites this as: write a cash and labor cap and a stop condition, and limit the downside rather than assume it can be hedged. Condition: applies before every launch. The source does not say how to size a portfolio of small bets; the quarterly plan (9.1) uses 3 bets under 1 shared cash cap as a playbook addition. Sources: 01 [a7b8a9aa106c].

**A5. Borrow the model from an adjacent industry.** Luxury fashion (drops), gaming (FOMO, prop hunts), hospitality (Ritz-Carlton, Eleven Madison Park), live events, collectibles, financial markets (prediction market hedges). Condition: the model must survive the brand's margin and voice checks (A6, C1). Sources: 01 [a7b8a9aa106c] [f76f1da8af54]; 02 hospitality [22e369c1edc4]; 03 hospitality [ad5810cd8a68] [7ae163d5a82f].

**A6. The play must fit the brand voice.** Irreverent stunts for irreverent brands. Serious voice: skip punk stunts, lean on hospitality and status plays. "Copying the format without the voice usually flops." Absurdity that does not fit the persona confuses instead of building a cult. Condition: applies to stunts, anti-marketing, mystery hooks and absurdist products. Sources: 02 [0874da44648a]; 03 [f3d618345541] [24e7dd3a3012] (03 repeats the CAH and Liquid Death cases; the rule is stated twice, the case set once); 01 mystery and absurdism must fit voice [d1f0d1622744].

**A7. Prefer plays where the lasting value is a policy, not a one-off story, and document every winner.** A Joshie-style gesture fades unless an everyday rule (the Ritz-Carlton $2,000 Rule) stands behind it. Record what was done, why it worked, the numbers, so it can be repeated; treat bets as experiments, not stunts. Condition: every bet ends in a registry entry (P22), win or lose. Sources: 03 [7ae163d5a82f] [ad5810cd8a68]; 01 [a7b8a9aa106c].

**A8. Values and cultural plays only when the values are real and backed by a program, and the moment fits.** Patagonia's anti-consumption ad was backed by repair and resale. Faked values invite greenwashing accusations. Cultural or political alignment (Buy Canadian, Ramadan) only if customers would see it as authentic. Condition: the brand can point to the program behind the message before the message goes out. Sources: 03 [d2474fde6f0e]; 01 [4dc56ea887bf] [58e1755b645e].

**A9. Keep the human moments manual; automate only the rule-based work.** What does not scale cannot be copied cheaply. Recruit 1 by 1, over-deliver, ask for referrals in person, do by hand what will be automated later because manual work gives insight no dashboard gives. AI or automation may handle repetitive service replies and content so the founder has time for judgment calls; it must not replace personal follow-ups, referral asks and over-delivery. Condition: early stage, or a standing tier for high-LTV cohorts later. Graduate a play into a system once it outgrows manual effort; no source gives the trigger, the card on 02 says "once the manual motion repeatedly produces reorders and referrals". Sources: 01 [68c4bfa88afe] [7ccc9fc1a3f2]; 02 [f7bb6a108f71]; 03 [aa796ddf08a2]. Tension inside 01 (human touch vs "AI Gothpreneur"): card 7ccc reconciles it as above; the source does not.

**A10. Ignore the "numbers are too small" objection, but treat the compounding math as an illustration.** Condition: illustration only; no ecommerce brand in the sources sustained it. Moved to Appendix A: the 10%-a-week compounding math example. Sources: 02 [f7bb6a108f71].

**A11. Narrow on purpose.** The goal is not to please a million customers a little but to make a small group feel the purchase was one of their best choices. Condition: run manual acts as a founding-stage tactic or as a standing tier for the top cohort, not as a mass program. Sources: 02 [f7bb6a108f71]; 03 [8fc70ea68011] [2984f2673be5].

**A12. Prove the value hypothesis by hand before the growth hypothesis.** Prove the product and experience are exceptional with manual effort before spending on ads and automation. Applies to a new brand or to a new VIP segment. Sources: 02 [f7bb6a108f71] (Airbnb photos, Wufoo notes); 03 [aa796ddf08a2] (same Paul Graham cases plus Zappos); 01 [68c4bfa88afe] (same essay). All 3 cite the same 2013 essay, so this is 1 evidence base stated 3 times.

### Group B. Sequence: fix effort first, then delight

**B1. Give the customer the fastest refund, replacement or exchange before any gift; a wild bet on a slow return process will not move repeat-purchase rate.** In a failure (late shipment, broken item, billing error) the customer wants the easiest path to a fix. Exceeding expectations then (a free gift or discount after a long hold) gives "negligible" loyalty gain. Loyalty plateaus once expectations are met. High effort is 4 times more likely to create disloyalty than low effort is to create loyalty. Condition: applies to every operational failure, before and during any wild bet. Basis: Matthew Dixon's Effortless Experience study, 97,000+ service interactions, quoted through summaries; the only research-grade claim in the folder. Sources: 02 [9f47b7d4326c] [76193c44f7e8] [702bc45b5b83]. Conflict with source 03's "solve the problem, then add a surprise" and Chewy's bereavement gestures: see 7.2.

**B2. No delight play reaches a customer with an unresolved failure.** Check each week that nobody who had a failure last week is receiving a gift this week without the failure being fixed first. Condition: the exclusion list (section 2) is refreshed before every send. Sources: 02, card addition [76193c44f7e8]. Playbook addition: the exclusion list is a required attachment to every approval request (9.2).

**B3. Audit the base before any wild bet.** Can a customer get a return, cancellation or fix without channel switching, repeated explanations or long waits? If not, fix that first. Measure Customer Effort Score, first-contact resolution, resolution time, transfers per ticket, repeat contacts. Add "next issue avoidance": answer the likely follow-up question before it becomes a second ticket. Condition: source 02 gives no pass mark; the agent sets a baseline from brand data and the human sets the bar (5.5). A wild bet "fails catastrophically" on a high-effort base; the source's example is a custom pet portrait that cannot save a customer who spent 3 hours on hold last week (illustration, not data). Sources: 02 [702bc45b5b83] [aebda9584fe6] [9f47b7d4326c] [76193c44f7e8]. `[needs brand data: CES, FCR, resolution time, transfers per ticket, contacts per order]`

**B4. Perceived effort counts as much as actual effort.** A fast fix still feels high-effort if the customer repeated the problem to several transferred agents. Compare measured resolution time with customer-reported effort; a gap means handoffs or repeats are hurting. Sources: 02 [9f47b7d4326c] [aebda9584fe6].

**B5. Delight only customers in a neutral or positive state.** Failure state: fix fast, no gift. Neutral or positive: wild bet allowed. Exception: hardship the customer volunteers, handled under K3 (optional, welcomed, no delay to the customer's request). Sources: 02 [702bc45b5b83] [dee4592d0973]; 03's frontline rule [ad5810cd8a68] disagrees (7.2).

**B6. Split tickets into order/shipping problems (measure CES, first-contact resolution, resolution time) vs high-LTV relationship touches (measure repurchase rate, AOV, referral rate); a returns ticket is never a brand-elevation win.** Operational Support (routine questions, product failures, shipping, returns, billing): streamline, stop channel switching, first-contact resolution; measure CES, FCR, resolution time; do not try to delight. Brand Elevation (high-LTV cohorts, unexpected touchpoints, relationship building, life events): measure LTV, earned media value, NPS, repurchase rate. Raise the frontline "Control Quotient" so reps resolve without escalating. Sources: 02 [702bc45b5b83] [aebda9584fe6].

**B7. Follow the staged rollout and do not skip a stage.** Stage 1 (this month, low cost, low risk): notes or founder videos to the top 50, keep-it refunds under $20, a control group. Stage 2 (next 90 days): named invite-only VIP tier for the top 1%. Stage 3 (next 6 months): tiered referral waitlist and a limited drop. Stage 4 (ongoing): 1 big stunt or values play. Each stage has a pass mark before the next (P3). Condition: source 03's plan; the pass marks are its heuristics, card [24e7dd3a3012] says so. Source 02's rule B1 comes before Stage 1; neither source states the other's step, and they do not conflict, so this playbook runs B3 as "Stage 0" (playbook addition). Sources: 03 [24e7dd3a3012] [42d04b3223ba] [8fc70ea68011] [f58ea6021437] [f42a03d72af2] [f3d618345541].

**B8. Adjust the plan to margin, product and voice.** Thin margins: delay lifetime warranties, keep price locks narrow. Product does not win a head-to-head test: skip proof-in-the-box. Serious brand voice: skip punk stunts. Sources: 03 [24e7dd3a3012] [04f54549fb37] [36d5dbe4d17c] [574b9d94f465] [f3d618345541]. `[needs brand data: gross margin by SKU]`

**B9. Treat a high cash-on-delivery share and a high return-to-origin rate as a base-effort problem, not a wild bet target: size and fix them at Stage 0 before any delight play launches.** `[general practice]`. No library source; verify against brand data before use. Extends Stage 0 (P2) and 5.2.

### Group C. Bounding every bet

**C1. No launch without a written bound.** The bound has 8 fields: hypothesis, cohort (a segment from the customer order file, Shopify or Metabase), budget cap (cash and labor, checked against gross margin on that segment's orders), metric, control, duration with a review date, stop rule, registry entry. Condition: every play, including "free" ones like a founder video; labor is a cost. Basis: card additions to 01 (target segment, hypothesis, total cash and labor cap, duration, baseline or holdout, stop condition) and 03's control group and benchmark per stage. None of the 3 sources gives cohort sizes, budget ranges or durations for most plays; where a source gives one it is in section 6. Sources: 01 [a7b8a9aa106c] [49b0963cfe85]; 03 [24e7dd3a3012]; 02, card [89bcc55e9cc4]. `[needs brand data: margin, cash available, baseline conversion and repeat rate for the chosen segment]`

**C2. Hold out a control drawn from the same eligible cohort before the treatment list is final.** Source 01: an email-only control (Fressnapf design) and, as a card addition, a randomized no-mail holdout to test whether mail itself is incremental. Source 03: a control group at Stage 1, for keep-it refunds and for letters, but it does not say how to pick it or how big. Source 02: cards say "measure incrementality" with no method. Strictest version kept: randomized holdout from the same ranked list, drawn before anyone is treated, large enough that the pass-mark metric can move (5.3). Condition: a play with no control is filed as an "observation", not a test, and cannot pass a stage gate. Sources: 01 [70a71f09d8c2] [e890000fa7eb]; 03 [24e7dd3a3012] [42d04b3223ba] [1a706b82583a]; 02 [ab3039ede71f] [89bcc55e9cc4]. `[needs brand data: matched or randomized control of similar customers]`

**C3. One play per cohort per test window.** Source 03's Stage 1 bundles 2 plays (top-50 touch and keep-it refunds for all buyers under $20) under 1 benchmark (repeat rate of the top 50), which cannot isolate keep-it. Rule: run keep-it on its own cohort and control (P5) and the touch on its own (P4). Sources: 03 [24e7dd3a3012] (the gap is named in its section 9); playbook addition for the split.

**C4. Cap cohort size and frequency at what the team can sustain by hand.** If the team cannot keep it up, shrink the segment. Source 03: top 50 to 100 for notes, not the whole list, because cost scales with list size. Source 01: 1 mailing per customer per 30 days for programmatic mail (Magazine.co.uk). Sources: 02 [05b6ed77af75] [f7bb6a108f71]; 03 [42d04b3223ba]; 01 [a9e802c5098a].

**C5. Never count an unverified hedge, an earned-media estimate or expected virality as funding or return.** Fund the maximum liability in cash. Earned media value is an estimate and stays outside the incremental contribution line. One viral outcome is not proof. Sources: 01 [49b0963cfe85] [a7b8a9aa106c]; 02 [89bcc55e9cc4]; 03 [f3d618345541].

**C6. Write the stop rule before launch.** Source 01 says "double down or kill" with no definition of "doesn't work". Playbook addition, built from the sources' own diagnostics: stop when the cash or labor cap is hit; when the control shows no lift at the planned review; when keep-it or referral fraud signals appear (repeat claimers, fake signups); when refunds rise after a guarantee; when a stunt draws backlash; when customers start expecting or asking for the surprise; when drop frequency stops tracking repeat visits; when return rate rises after a keep-it pilot; when drop sell-through falls below full price; when checkout conversion falls during a stunt spike. Sources: 01 [a7b8a9aa106c]; 03 [1a706b82583a] [f58ea6021437] [3a74574fff82] [f3d618345541] [e29188eb0294] [b7edaaaeed23].

**C7. Legal, consent and platform review before any play that promises, refunds, mails, texts, uses third-party data, gates access, runs a contest or pays customers.** No source gives legal steps; the cards add warnings. Items: promotion terms and risk transfer for hedged refunds; GDPR and local privacy for address data; SMS consent for reminders and drop alerts; venue permits for guerrilla; gambling-style rules for mystery boxes and live auctions; warranty and consumer-protection law; contest and paid-internship rules; creator disclosure; platform DM and giveaway policy. Sources: 01 [49b0963cfe85] [49715f3b64de] [07497417cc0a] [8f0ac696045b] [85c5e90b4fff] [4c2cd1cec3bf]; 02 [147b7a92331e] [4b114e40b69d]; 03 [04f54549fb37] [3a74574fff82]. `[web check: consumer protection, contest, warranty, SMS consent, privacy and prediction market rules in the selling market]`

**C8. Judge at the planned review date, not at the first viral moment or the first quiet week.** Non-paid bets are a slower build (Huckberry's Ben O'Meara: "a slower build, but a more profitable business"). Set the review date in the bound; do not read a wild bet on a same-week or 30-day window unless the play is transactional by design (a flash sale, a drop). Sources: 01 [a7b8a9aa106c] [9b43d5332e59] [ce5b3f63afcc]; 02 [89bcc55e9cc4].

### Group D. Measurement

**D1. A reported repeat-purchase lift, ROAS or conversion lift from another brand is not a benchmark for this store's PDP, AOV or margin; it is an idea to test on this store's own cohort.** No case in the 3 sources gives sample size, duration, cost per piece, margin or how "ROI", "conversion" or "return rate" was defined. Vendor cases (optilyz, PebblePost, Paperplanes, Lob, Dotdigital, Experian, Webmart) are marketing and carry survivorship bias. Condition: a case number may be quoted in a brief only with its source and the words "reported, unaudited". Sources: 01 section 9; 02 section 9; 03 section 9 (all 3 mini playbooks say so).

**D2. Judge wild bets on relationship metrics, with incremental contribution after all program costs as the decision line.** Source metrics: unprompted word of mouth, LTV of engaged customers, referral rate, retention lift, repeat-purchase rate, 90-day reorder rate, NPS, incremental revenue. Card additions: incremental contribution after all program costs decides double down or kill; attention metrics are kept as separate signals; "not a licence to never measure". Condition: the readout (P22) reports both lines and never lets one stand in for the other. Sources: 01 [a7b8a9aa106c] [ce5b3f63afcc]; 02 [aebda9584fe6] [89bcc55e9cc4]; 03 [24e7dd3a3012] [f3d618345541]. Conflict with performance-marketing practice (engaged-customer LTV vs ROAS): 7.6.

**D3. Track earned media, UGC and shares separately from incremental sales and from campaign cost.** Earned media value is an estimate, not revenue. Stunts are budgeted as a marketing cost and judged on earned media; source 03 gives no method to value coverage or shares against spend. Sources: 02 [89bcc55e9cc4]; 03 [f3d618345541] [24e7dd3a3012]; 01 [a7b8a9aa106c]. `[needs brand data: method to value coverage and shares]`

**D4. Control for self-selection when comparing engaged vs non-engaged customers.** Huckberry's 3.5x LTV for content-engaged customers vs ad or affiliate customers is confounded: people who engage with content may buy more anyway. Compare after controlling for prior spend; if the gap disappears, do not claim the content caused it. Sources: 01 [ce5b3f63afcc].

**D5. Give operational touchpoints their own metrics.** CES, first-contact resolution, resolution time for support; LTV, earned media value, NPS, repurchase for Brand Elevation. Do not read a delight play on support metrics or a support fix on NPS alone. Sources: 02 [aebda9584fe6].

**D6. Judge a paid tier on spend and retention lift vs comparable non-members, not on enrollment; judge a new channel on contribution margin after platform fees.** Sources: 02, card additions [ab3039ede71f] [7d86ecac0ff5]. `[needs brand data: channel fees, margin]`

**D7. Put a response device on every physical piece.** QR code, unique URL, unique or private discount code, perforated tear-off referral insert. A piece with no device cannot be read. Sources: 01 [e890000fa7eb] [3790fdeac0c7]; 03 [42d04b3223ba] [9a0245f0095a].

**D8. Report the reported effect next to the measured one.** In every deliverable, the "expected effect" column carries the source's case figure with its label (vendor case, founder claim, blog, press) and the measured column carries the brand's own control comparison. Playbook addition that follows from D1 and D2.

### Group E. Cohort selection

**E1. Start at the top of the file by lifetime spend, with the smallest group the team can serve by hand, and widen only on a passed gate.** Source 01: top 10 customers from last quarter for the unscalable gift; top 10 for an insider event. Source 03: top 50 (or 50 to 100) for notes and founder videos, expand to top 200 when repeat or 90-day reorder beats control; top 1% for the VIP tier. Source 02: top 1% of repeat buyers for artifacts and Founder's Ink. Merged, strictest first: start at 10 to 50 by hand; 200 after a passed control read; 1% as a standing tier after Stage 2 passes. The claim that the top 1% "drive most of your revenue" is asserted, not shown; measure it. Sources: 01 [2d99a5dbeda9] [5eeef0648aad]; 03 [24e7dd3a3012] [42d04b3223ba] [8fc70ea68011]; 02 [0f05cded3cb1] [05b6ed77af75]. `[needs brand data: revenue share of top 1% and top 5%; customer list with lifetime spend]`

**E2. Costly touches go to repeat buyers with shown affinity, not first-time buyers.** Card adaptation on source 03: skip first-time buyers with no shown affinity for handwritten mail. Exceptions are different plays with their own bound: programmatic mail on welcome, cart abandonment and browse (G rules), the 100-day onboarding (K5) and surprise inserts on first orders (H10). Sources: 03 [42d04b3223ba] [9a0245f0095a]; 01 [fcef726cbd6f]; 02 [7615a4af9401]. See 7.10.

**E3. Emotional gifts need an emotional tie to the category.** Pet, home, car, baby, hobby item. A purely functional category has no hook and gets no shares. Sources: 03 [63f18883754c] [e29188eb0294].

**E4. Every delight cohort excludes customers in a failure state (B2, B5).** Sources: 02 [76193c44f7e8] [702bc45b5b83].

**E5. Programmatic mail segments: VIPs, repeat buyers, high-value cart abandoners, lapsed buyers, new club members, high-consideration browsers.** The lapsed window of 6 to 12 months and the second-purchase window of 30 to 60 days are the compiler's advice in source 01, not what any case did; Fressnapf's numbers come from a second-purchase campaign to 15,000 customers, not a reactivation. Find the brand's own repurchase interval. Sources: 01 [fcef726cbd6f] [70a71f09d8c2] [898e3d534adb] [a9e802c5098a]. `[needs brand data: repurchase interval, cart value distribution]`

**E6. Flash sales go only to loyalty segments, never the full list.** Targeting makes the sale read as a reward, not desperation; blanket discounts erode brand value. Needs clean segment data so the offer does not leak. Sources: 01 [184e447721a2].

**E7. Condition every cohort size and stage gate in this playbook on single-hero-SKU vs catalogue: a single-SKU store cannot build the top 50, top 200 or top 1% repeat-purchase cohorts the same way a catalogue business can, and needs a waitlist- or launch-based version of the same stages instead.** `[general practice]`. No library source; verify against brand data before use.

### Group F. Handwritten notes, founder videos, founder time

**F1. The first play is a handwritten note or a 60-second founder video to the top cohort, with a control.** Cost: about $1 to $3 per note plus time (source 03 estimate); a founder video costs time only. Track reorder and referral for recipients vs control. Source 01's version: top 10 customers from last quarter, handwritten note plus a small unexpected gift. Source 02's version: Wufoo wrote a handwritten thank-you to every new user "for as long as it was physically possible". Condition: repeat buyers (E2), neutral or positive state (B5). Sources: 03 [24e7dd3a3012] [42d04b3223ba] [aa796ddf08a2] [2984f2673be5]; 01 [2d99a5dbeda9]; 02 [f7bb6a108f71].

**F2. Founder's Ink: once a year, top 1% of repeat buyers, handwritten by the executive team, naming the buyer's past purchases, with no discount code.** Budget it as a fixed small activity, not a direct-response campaign; cap the segment at what the team can sustain. Condition: source 02's tactic; it conflicts with 02's own random-timing rule (H2) and with 03's annual letter that carries a private offer code (F3). See 7.8. Sources: 02 [05b6ed77af75]. `[needs brand data: top 1% by repeat orders]`

**F3. Annual or anniversary letter to repeat buyers with a VIP offer or club invite and a private code, measured against a control.** Cost $1 to $5 per piece (source 03, via LettrLabs). The private code or a perforated tear-off referral insert is the response device. Sources: 03 [42d04b3223ba]. Conflict with F2 on whether the letter carries a code: 7.8.

**F4. Never send printed notes made to look handwritten.** They feel fake. Source 03 says to use a handwriting service (LettrLabs or similar) only once volume grows, and to keep it genuine; it does not say how a robot-written note stays genuine, so treat the service as a scale option the human approves knowingly. Sources: 03 [42d04b3223ba] [9a0245f0095a].

**F5. Never send costly mail to the whole list.** Cost scales with list size; keep it to proven repeat buyers. Sources: 03 [42d04b3223ba].

**F6. Forward every post-purchase, shipping and return email to the founder for 1 month while volume is low, to map checkout and delivery pain before any wild bet.** Forward every service email to the founder, who replies personally. Source 01 claims you learn more in 30 days than in a year of surveys (claim, no data). Related: personally onboard or call first or best customers, fix their problems yourself, treat long untimed support as marketing spend (Zappos, 10-hour-43-minute call). Sources: 01 [2d99a5dbeda9]; 03 [aa796ddf08a2].

**F7. Map the path from ad or search to PDP to cart to checkout to repeat purchase for 20 real customers, and mark where a human touch fits.** "If you could only have 20 customers, what would you do to make each feel like the only customer?" Write every touchpoint from discovery to post-purchase and mark where a manual, human touch fits. Sources: 01 [2d99a5dbeda9].

**F8. Where a local messaging channel such as WhatsApp is how the customer base actually talks, use it for notes, drop alerts and reminders, instead of or alongside mail and email.** `[general practice]`. No library source; verify against brand data before use. Extends F1, G1, M5.

### Group G. Programmatic direct mail (PDM)

**G1. Trigger physical mail from the same behavioral signals as email, through an integration between the mail vendor and the email platform.** Bergzeit: optilyz plus Emarsys. Harlow Timber: Dotdigital plus ZAP~POST. Condition: the same event fires mail and email so the control (G6) can be an email-only group. Sources: 01 [fcef726cbd6f] [3790fdeac0c7]. `[verify UI: vendor and ESP integration]`

**G2. Start with high-value segments and high-consideration products.** VIPs, repeat buyers, high-value cart abandoners, lapsed buyers, new club members; home decor and similar categories that need several touchpoints (Lulu and Georgia). Source 01's reason for the cost: a letter cuts through inbox fatigue and mail from an ecommerce brand is itself a novelty; it gives no cost figures. Sources: 01 [fcef726cbd6f] [a9e802c5098a] [70a71f09d8c2].

**G3. Personalize per customer: show the exact abandoned or recommended products and tailor the offer by cohort.** Magazine.co.uk showed the exact magazines; Woolroom showed abandoned or recommended products with incentives; DukesHill personalized by cohort. Sources: 01 [a9e802c5098a] [fafb61f67162] [3790fdeac0c7].

**G4. Every piece carries a response device (D7).** QR code, unique URL or unique discount code. Sources: 01 [e890000fa7eb] [3790fdeac0c7].

**G5. Cap frequency at 1 mailing per customer per 30 days.** Magazine.co.uk's cap for abandoned basket cohorts. Condition: the only frequency number in the folder; 1 case. Sources: 01 [a9e802c5098a].

**G6. Run 2 controls: an email-only control and a randomized no-mail holdout.** The email-only control (Fressnapf design) shows mail's lift over email; the randomized holdout (card addition) shows whether mail itself is incremental. A creative A/B test compares 2 mail versions and answers a different question. Sources: 01 [70a71f09d8c2] [e890000fa7eb].

**G7. Timing: the sources' numbers are thin and mostly unsourced.** "About 48 hours after a high-value cart abandonment" appears only in source 01's header "Look for" list; no case in the body uses it. Lulu and Georgia's browse mail arrives "within days of browsing". "30 to 60 days after first order" for the second-purchase letter and "6 to 12 months since last order" for lapsed are the compiler's advice. Rule: find the brand's own repurchase interval and test timing as a variable (G12). Sources: 01 [fcef726cbd6f] [a9e802c5098a] [898e3d534adb] [70a71f09d8c2]. `[needs brand data: repurchase interval; abandonment volume by cart value]`

**G8. Mail format must match brand values.** Recycled paper for a sustainability brand (Woolroom); paper stock matters (source 01 credits GOLDNER's up to 13.6% conversion to personalization detail; claim, no test shown). Sources: 01 [fafb61f67162] [a7b8a9aa106c].

**G9. Third-party address or spend data: ask how segments and addresses were obtained and may be used; "anonymized insights" does not make address-based targeting anonymous; confirm GDPR and local privacy rules first.** HelloFresh used Experian Spend Insight to reach competitor meal-kit customers; no results given. Sources: 01, card addition [49715f3b64de]. `[web check: availability and privacy terms of spend-data partners per country; India DPDP rules on address data]`

**G10. Close the loop: mail engagement (QR scans, code use) triggers digital follow-ups and retargeting.** Harlow Timber's follow-up Black Friday email had an 88% open rate among 12,000 contacts (reported). Sources: 01 [3790fdeac0c7].

**G11. Named PDM vendors are EU, UK and US; India coverage is unknown.** Sources: 01 section 9. `[web check: PDM vendors and identity-match coverage in the brand's country; India options]`

**G12. Treat mail like a digital channel: A/B test offer, creative, timing and format; roll winners forward; re-test.** thredUP with Lob reported ROI up 128% from A/B-tested personalized mail (vendor case, ROI undefined). Sources: 01 [e890000fa7eb] [a9e802c5098a].

**G13.** Moved to Appendix A: the B2B, wholesale and corporate-gifting ABM rule (out of scope for a DTC store).

**G14. Physical welcome for new club or loyalty members: a personal note, a small gift, a clear list of member benefits; track reorder and referral.** GOLDNER: 3.4% to 13.6% conversion across 7 countries, a 4x spread (vendor case). Sources: 01 [898e3d534adb]; 03's surprise insert on VIP orders [2984f2673be5] [9a0245f0095a] is the low-cost version of the same idea.

### Group H. Gifts, artifacts, surprise and inserts

**H1. Artifact, not swag.** Logo items (t-shirts, pens, mugs, keychains) serve the sender and read as transactional. Send a high-quality, practical luxury item the recipient would be proud to own, with no company branding, matched to a stated preference. Adding a logo turns it back into swag. Ecommerce examples the source gives: premium cutlery or bespoke leather goods for the top 1% of repeat buyers. Condition: the preference is known (zero-party data, support notes); if not, do not guess. Sources: 02 [0f05cded3cb1]. `[needs brand data: zero-party preferences, support notes]`

**H2. Send gifts on a random date, not at Christmas, birthdays or purchase anniversaries.** Occasion gifts read as obligation and compete with other gifts. Spread sends across the calendar so none lands in a heavy gifting season (card addition). Condition: source 02's rule; no data on the effect. It conflicts with 02's own annual Founder's Ink, with 02's planned 100-day sequence and with source 01's Bergzeit birthday letters (about 7.5% redemption, vendor case). See 7.8. Sources: 02 [eb580823eb04]; 01 [fcef726cbd6f].

**H3. A surprise stays a surprise: unannounced, no purchase required, never a standard perk.** "The randomness is the point." It fades if routine or expected. Stop when customers start expecting or asking for it (C6). Chewy sends about 1,000 hand-painted pet portraits a week to selected customers, unannounced, since 2013 (press reports). Sources: 03 [e29188eb0294] [63f18883754c] [24e7dd3a3012]; 02 [ca8e2e37165b] (same Chewy case).

**H4. Emotional art or a personal physical gift: pick a personal artifact the product touches, choose a small weekly set of loyal repeat buyers, commission cheap custom art at $20 to $40 a piece (source 03 estimate), do not announce it.** Track whether recipients post, share or buy again vs non-recipients before scaling (card adaptation). Sources: 03 [e29188eb0294] [63f18883754c]. `[needs brand data: repeat rate of recipients vs non-recipients]`

**H5. Before scaling a gift-with-order program, secure enough vendor supply for expected weekly order volume, so gifts do not delay shipping.** Chewy uses hundreds of independent artists. Note: card dee4592d0973 wrongly attaches the 1,000-a-week figure to the bereavement play; portraits are a separate program. Sources: 02, card addition [ca8e2e37165b].

**H6. Expect negative direct ROI on a signature gift; judge on UGC, referrals, advocacy and repeat, tracked before scaling.** Sources: 02 [ca8e2e37165b] [89bcc55e9cc4]; 03 [e29188eb0294].

**H7. Inner-circle gifts (spouse, children, assistant) only where the buyer volunteered a relevant household preference, delivered through the buyer, optional, with no review, referral or purchase obligation.** Never infer family ties from unrelated data. Moved to Appendix A: the source's single B2B case behind this rule. Sources: 02, card adaptation, stricter than the text [4b114e40b69d].

**H8.** Moved to Appendix A: the Eleven Madison Park $2 hot dog story (a fine-dining anecdote, not an ecommerce result).

**H9. Budget gifts to the top 1% repeat-buyer cohort as a fixed quarterly cost against gross margin, not a per-order spend to optimize.** From Giftology (Ruhlin); opinion-grade. Sources: 02 [0f05cded3cb1] [05b6ed77af75].

**H10. Surprise inserts: a low-cost item (sticker, sample, small gift) in first orders or VIP orders, at cents to a few dollars, paired with a handwritten thank-you, personal not generic, tied to a tracked action (referral code, VIP invite, tracked reorder offer).** Generic filler adds cost without delight. Sources: 03 [9a0245f0095a] [2984f2673be5]; 01's GOLDNER welcome kit [898e3d534adb] is the fuller version.

**H11. Widen the relationship radius only with consent; keep gifts free of strings.** Sources: 02 [4b114e40b69d] [eb580823eb04].

**H12. For jewelry and other considered-purchase categories, the gift or artifact can be a considered-purchase feature: free engraving, a certification or appraisal guarantee, or a tie-in to a gifting occasion.** `[general practice]`. No library source; verify against brand data before use. Sits in J and H.

### Group I. Frontline discretionary budget

**I1. Give support and warehouse staff a standing no-approval budget per incident, sized to the brand's margin and AOV, not to the Ritz-Carlton figure.** Source 03 example: $50 to $200 per incident, scaled down from Ritz-Carlton's $2,000 per incident against about $250,000 guest LTV (0.8% of LTV per incident, derived). Source 02 gives no amount. Sources: 03 [7ae163d5a82f] [ad5810cd8a68]; 02 [22e369c1edc4] [246d16432222]. `[needs brand data: customer LTV, AOV, gross margin]`

**I2. Spend it on a specific item tied to something the customer said.** A customer mentions a hiking trip: a trail map or hiking socks. A vacation mentioned in chat: a small local treat in the order box. Capture cues in tickets, chats and calls. Sources: 02 [22e369c1edc4] [246d16432222]; 03 [ad5810cd8a68].

**I3. Set a per-incident cap, a per-rep monthly cap and a per-customer cap on frontline spend, sized to the order's gross margin, logged against the order id.** Logging of every spend, a per-rep monthly cap, a per-customer cap, a review of spend by cue, and an abuse check. Card 02 says "set guardrails to control abuse"; source 03 says it is thin on logging, limits and review. Playbook addition: the approval request names the caps and the log location. Sources: 02 [22e369c1edc4]; 03 [7ae163d5a82f].

**I4. Use the budget for customers in a neutral or positive state; in a failure, fix first.** Source 02 says delight after a failure adds negligible loyalty. Source 03 says "solve the problem, then add a surprise". What the agent should do is in 7.2: fix first, confirm the fix, and only then allow a small surprise that is not templated. Sources: 02 [702bc45b5b83] [9f47b7d4326c]; 03 [7ae163d5a82f] [ad5810cd8a68].

**I5. Write the frontline gesture into support macros as a standing rule, not a one-off, so every eligible order gets the same treatment.** Sources: 03 [7ae163d5a82f].

**I6. Raise the frontline Control Quotient: let reps resolve without escalating.** Named in source 02 without a method. Sources: 02 [702bc45b5b83].

### Group J. Guarantees, refunds, warranties, price locks, proof

**J1. Keep-it (returnless) refunds: case by case, under a price threshold, for damaged, perishable or hard-to-resell goods, and not advertised as the default.** Source 03's threshold example: under $20 (goTRG: most keep-it policies cover items up to $20). Reason not to advertise: about 9% of returns are fraudulent (NRF and Happy Returns, via source 03). Condition: product quality high, abuse monitored (repeat claimers). Sources: 03 [1a706b82583a] [24e7dd3a3012]. Conflict: O Positiv advertises a 30-day no-return money-back guarantee and credits it for scaling; Chewy tells bereaved owners to keep or donate; see 7.5.

**J2. Build the keep-it break-even from brand data; no source gives the formula.** Context from source 03: return processing costs 20% to 65% of COGS, sometimes up to 100% (UPS, via source). Playbook addition: keep-it pays when return shipping plus handling plus expected resale loss exceeds the item's refund cost, before fraud. Sources: 03 [1a706b82583a]. `[needs brand data: cost per return, resale recovery rate, return reasons by SKU]`

**J3. Raise the keep-it threshold only after repeat-purchase or 90-day reorder of keep-it recipients beats a control, and claims per customer stay rare.** Sources: 03 [1a706b82583a] [24e7dd3a3012].

**J4. Lifetime warranty or repair-for-life: durable SKUs only, repair-first, a clear claims page, claims modeled before promising, scope and exclusions defined, thin margins delay it.** LL Bean and Eddie Bauer pulled back generous guarantees; claims "will bury you" on products that do not last. Verify the current terms of cited brands (Osprey, Darn Tough) instead of copying "forever, any reason". Sources: 03 [04f54549fb37] [24e7dd3a3012]. `[needs brand data: defect and failure rates by SKU]` `[web check: current Osprey All Mighty Guarantee and Darn Tough terms; warranty rules in the selling market]`

**J5. Outcome guarantee: a specific, measurable outcome, a clear product-appropriate remedy for a substantiated claim, and refund-rate tracking before scaling.** Vague promises invite disputes. The "keep working until you get the result" form comes from services and must not become an unsupported physical-product guarantee (card adaptation). Hormozi's "about 30% more sales, refunds barely up" is a book-summary claim from a service context, not an ecommerce benchmark. Sources: 03 [3a74574fff82]. `[needs brand data: refund rate before and after]`

**J6. Risk reversal can convert and cut cost, but only where product quality is high and abuse is controlled.** Sources: 03 [04f54549fb37] [1a706b82583a].

**J7. Price lock for loyal subscribers: ring-fence who qualifies, market it as a loyalty benefit, model future cost increases before promising, test on an eligible cohort; keep it narrow on thin margins.** Alternative: hold prices during inflation and frame the hold as a promotion without a discount (Old Navy, Bark). BarkBox's 2012 price lock is historical context. Sources: 03 [36d5dbe4d17c] [7c689b80e439]. `[web check: whether BarkBox still honors the lock]` `[needs brand data: cost trend per unit]`

**J8. Proof in the box only if the product truly wins the test, the test is safe and readable by a customer, and the comparison is not selective.** Country Delight's milk-adulteration kit in the first order; its FY24 revenue does not show the kit caused growth. Measure conversion or repeat vs control before scaling. Sources: 03 [574b9d94f465].

**J9. Track damaged-in-transit reports and packaging quality as a return-cost driver next to the keep-it break-even (J2): a packaging fix can lower cost per return more cheaply than a keep-it or warranty policy.** `[general practice]`. No library source; verify against brand data before use. Sits next to J2 and H, P16.

**J10. For cross-border or diaspora buyers, offer a customs or duty transparency guarantee (landed cost shown at checkout, or a promise to cover surprise duties) as a trust lever alongside the other guarantees in this group.** `[general practice]`. No library source; verify against brand data before use. Sits near J and S4.

### Group K. Subscriptions, cancellation, first 100 days

**K1. Flexibility beats cancel friction: easy pause, credit rollover, cadence control.** ClassPass (pause and rollover, "massive retention gains", no number); Yankee Candle (custom cadence, 90% subscriber retention, via a blog with no method). Trust is the claimed payback, not a measured one. Sources: 02 [c58b965fe70a] [6812a43572e9]. `[verify UI: subscription tool supports pause, skip, rollover]`

**K2. Proactive Pause: flag subscribers receiving product faster than they use it and email them advising a pause "to save money", framed as protecting their wallet.** Source 02 names Recharge and gives no threshold. Track whether paused customers resume or cancel (card addition). Sources: 02 [c58b965fe70a]. `[needs brand data: consumption rate per SKU, order cadence, skip and pause history]` `[verify UI: whether the subscription tool exposes usage signals]`

**K3. Cancellation is the customer's choice and is never delayed.** Offer an optional reason field or a gentle support invite without delaying the cancellation. If hardship is volunteered, apply an approved remedy (pause or an eligible refund). Send a gesture (card, flowers) only when appropriate and welcomed. Do not turn the contact into an upsell or retention push. Train staff; avoid templated sympathy. Chewy's version (flag sudden cancellations of long-term auto-ships, agents "inquire gently", no-return refund, donate food, flowers, sometimes a custom doll) is the case; the card adaptation is stricter and is the rule. Sources: 02, card adaptation [dee4592d0973]; 03 [e29188eb0294] (same Chewy case). See 7.4 on pause vs hard cancel.

**K4. Bundles and subscription SKUs can carry the wild bet inside the offer: an unbranded artifact in the first shipment, a surprise upgrade or a discretionary treat, with cadence control, pause and rollover, and any paid tier about access, not only discount.** Check COGS impact of added items. Condition: this is the card writer's synthesis; source 02 has no bundle section. Offer architecture belongs to 03-OFF. Sources: 02, card synthesis [6812a43572e9]. `[needs brand data: margin per bundle]`

**K5. Treat days 0 to 100 after first purchase as the main churn window; do not jump to cross-sell or review requests; plan an emotional journey; measure repurchase and early churn.** Source 02 cites Joey Coleman's 8-phase model but does not list the phases. Options named: a customized welcome kit by expedited mail before the product arrives, sequential founder videos, surprise mailers, surprise digital upgrades. The matrix row says it keeps "dopamine high while waiting for the product", which is a confusion: 100 days is far longer than delivery. Sources: 02 [7615a4af9401].

**K6. Add a proactive post-delivery check-in (did it arrive, does it fit) timed to the expected delivery date, separate from the 100-day churn window.** `[general practice]`. No library source; verify against brand data before use. Extends K5.

### Group L. Loyalty mechanics and time-limited value

**L1. Expiring loyalty value can create a reason to return, if the expiry is disclosed before earning, the earn rate is meaningful, redemption is practical, reminders go on more than 1 channel with consent, and reminders are worded as loss of earned value ("you earned this, don't waste it").** Haus & Kinder: coins expire in 60 days, email and SMS reminders, "70X ROI" on retention tooling (ROI undefined), 12.4% of signups through the loyalty system. A low earn rate or hard redemption makes expiry feel punitive (card addition). Condition: an existing loyalty program in a repeat category. Sources: 01 [07497417cc0a]. Conflict: common advice treats expiry as a trust risk; sources 02 and 03 call points programs a commodity to skip; see 7.3.

**L2. Track loyalty as an acquisition surface: share of signups that come through it.** Sources: 01 [07497417cc0a].

**L3. Seasonal daily reveal: 12 days, 1 genuinely valuable offer per day behind a calendar, midnight expiry, a "missed" state that pushes tomorrow's visit, rules announced up front.** Filler days break the loop. Repeating daily urgency across the year trains discount dependency (card caveat). L'Occitane's "82% Return Rate" in the article title is never defined. Sources: 01 [67ba6fcee11e].

**L4. Delayed discount: no discount on the current order; a reward that unlocks on the next purchase, with an expiry; message the earned value; test the unlock threshold and expiry window against a no-reward control.** Too long kills urgency, too short feels punishing. Weak for one-time-purchase categories; creates an accounting liability (card). Sources: 01 [a03a3ab4e941].

**L5. Flash sales only to loyalty segments, personalized, occasional, with a high-visibility urgency cue (Bombas: bright yellow "Expires Tomorrow" banner), measured on conversion and brand perception together.** Sources: 01 [184e447721a2].

**L6. Paid loyalty: make the paid tier about exclusive access, not only discount, and measure spend and retention lift vs comparable non-members.** Source-reported McKinsey figure: paid members 60% more likely to increase spend after joining, twice the free-program rate; via a retention blog, no method. Sources: 02 [ab3039ede71f]. `[web check: McKinsey paid-loyalty study]`

**L7. Reward non-purchase actions (reviews, UGC) with gifts and event invites; tier by lifetime spend and let engagement move customers within tiers.** The Body Shop "Love Your Body". Sources: 03 [6cb0a48f51d6].

**L8. Mystery bundles and blind boxes: a stated minimum value ("at least $X value guaranteed"), products already profitable at the bundle discount, consistent and honest parameters, a small segment first, margin and repeat measured, gambling-style rules checked.** Elf: 6 bundles, 5 to 8 items, up to 50% off, early November (example). If buyers start waiting for bundles, run them less often. Sources: 01 [85c5e90b4fff]. Conflict with source 03's anti-discount stance: 7.9. `[web check: rules on mystery boxes, blind boxes and live auctions in the selling market]`

### Group M. Status, VIP, scarcity and drops

**M1. VIP tier: named, invite-only, top 1% by lifetime spend, with early access to drops, a direct founder channel and a surprise insert in every VIP order; formalize and add a second tier only when VIP retention and AOV beat non-VIP.** A 60-second founder video to new VIPs or after a big order. Sources: 03 [8fc70ea68011] [2984f2673be5] [11a4bf90d117] [6cb0a48f51d6]. `[needs brand data: retention and AOV by tier]`

**M2. Gate only when the reward inside is worth the friction, and keep benefits clearly tied to loyalty so they do not look unfair if they leak.** Gating shrinks the funnel. Harry's is the source's ecommerce case. Moved to Appendix A: the CRED (fintech app) example. Sources: 03 [11a4bf90d117] [8fc70ea68011].

**M3. Scarcity must be real: fixed inventory, fixed release time, numbered batches, no fake countdown timers, no restock promises you will not keep, full price.** Last Crumb: $120 per dozen, weekly drops, "sold out in seconds". L'Occitane: "true scarcity, not just a countdown timer". MSCHF: numbered drops by SMS on set Tuesdays, no paid ads. Sources: 01 [56c8c219238a] [67ba6fcee11e] [f76f1da8af54]; 03 [f42a03d72af2].

**M4. Build the brand and audience before the first drop.** Last Crumb spent 1 year on brand and tested 20 box designs before selling 1 box; Gully Labs spent 6 months building an audience before its first shoe. A drop with no pre-built audience may sell nothing (card caveat). Sources: 01 [56c8c219238a] [f76f1da8af54] [66b5d9fbb538].

**M5. Gate drop access with an invite-only waiting room, single-use links or a queue fast-pass so members, not bots or resellers, get in; tell insiders (VIP tier or SMS list) the day before.** SMS needs consent. Sources: 03 [f42a03d72af2] [11a4bf90d117]. `[verify UI: waiting room and single-use link setup in Queue-it or the store platform]` `[needs brand data: SMS list size and consent status]`

**M6. Do not set supply so low that real fans are shut out.** Raise batch size if fans complain and stock sells out at full price. Sources: 03 [f42a03d72af2].

**M7. Keep a drop cadence only while drop frequency tracks repeat visits or purchase frequency; a fast cadence needs a fast supply chain; otherwise make fewer, better drops.** Snitch: 15 to 20 days design to shelf, 200 to 250 styles a month (case). Source 01 does not address drop fatigue or restock policy at all. Sources: 03 [b7edaaaeed23]; 01 section 9. `[needs brand data: visit and purchase frequency by drop week]`

**M8. Packaging and the reveal are part of the product in a drop.** Sources: 01 [56c8c219238a] [f76f1da8af54].

**M9. Sell access, not price.** The feeling of having what others don't is the product (the Michelin reservation comparison). Sources: 01 [56c8c219238a].

**M10. Livestream selling works through compressed buy windows (timed listings, drops, auctions) with checkout in the stream, for products that reward demonstration, storytelling or collector appeal.** eBay Live Australia; Instagram, TikTok or YouTube Live as substitutes. Sources: 01 [72d41c0813d1]. `[verify UI: live shopping features per platform and country]`

**M11. For a catalogue store that never runs scheduled drops, give a genuine per-SKU low-stock indicator (a real remaining-count or low-stock flag) as the scarcity signal, distinct from M3's drop-specific scarcity.** `[general practice]`. No library source; verify against brand data before use. Sits next to M3.

### Group N. Referral, community, co-creation, content

**N1. Tiered referral waitlist: gate a launch or drop behind a waitlist, give each person a unique link, set escalating and reachable product rewards, show a live progress bar, use product or access rewards and never cash, filter fraud.** Harry's: 5 referrals = shave cream, 10 = razor; 100,000+ emails in 1 week, 85,000+ legitimate (85%), 77% from referrals, 200+ people made 50+ referrals each. Pass mark: referral signups above 30% of total (source 03 heuristic). No tool and no fraud steps given. Sources: 03 [f58ea6021437] [24e7dd3a3012]; 01 "ask for referrals personally, make it easy and rewarding" [68c4bfa88afe].

**N2. A named community with rituals, status markers and ongoing programming; a sticker and welcome note in every box; UGC contests; consistent voice; it cannot be faked.** boAt "boAtheads" (800,000 in 2018 to 3 million+ in 2020, reported); Harley HOG (members spend 30% more on clothing and events, brand-reported). Stores as community hubs and real people over paid influencers (Kotn, no numbers); events do not need to be elaborate (Bailey Books). Social is a hub, not a broadcast channel. Sources: 03 [e6ea8581c19b]; 01 [409a5642f1ed] [aa3400464439]; 02 [b5a1ffc627e1].

**N3. Co-creation: a submit-and-vote page seeded with the existing community or VIP tier, credit and a cut for winners, a public statement of what can and cannot ship, results fed into real product decisions.** LEGO Ideas: 10,000 supporters to be considered, about 1% royalty of net sales. Act on feedback visibly; feedback can skew to a vocal minority (card caveat). Sources: 03 [6fd8b0b7de34]; 01 [fcb3a9e4905f] [0c1287c76ea8] [66b5d9fbb538] [5eeef0648aad]. `[web check: current LEGO Ideas rules]`

**N4. Community before product: months of audience building and feedback before the next product.** Gully Labs: 6 months. Sources: 01 [66b5d9fbb538] [2d99a5dbeda9].

**N5. Start an insider program tiny.** Heaven Mayhem launched 20 one-of-a-kind necklaces and DMed every person who liked a post; source's adaptation: invite the top 10 customers to an event, ask for feedback, give early access; scale rituals as it grows (monthly calls, 150-person nights, office visits). Automate only after the manual pattern proves engagement. Sources: 01 [5eeef0648aad].

**N6. Content that makes deposits, not asks, including links off your site; measure engagement depth and engaged-customer LTV with the self-selection control (D4).** Huckberry's newsletter has linked off-site for about 15 years. Hokuoh Kurashi no Doguten: content first, commerce as an extension (no numbers). Test question: "What content would my customers consume even if I never sold them anything?" Sources: 01 [ce5b3f63afcc] [e5e13b0a3007]. `[needs brand data: customer-level engagement joined to order history]`

**N7. Creators: give freedom, seed product for unscripted reactions, do not over-script, follow disclosure rules, track creator-attributed revenue.** Natura and Swiss Arabian (no numbers). Sources: 01 [4c2cd1cec3bf]. `[web check: creator disclosure rules]`

### Group O. Stunts, anti-marketing, anti-discount, values, guerrilla, mystery

**O1. A stunt needs a strong, specific brand voice first, and a format that fits: content people would watch anyway (Liquid Death), a stunt that dramatizes the product benefit (Wakefit Sleep Internship), or an anti-promotional gesture on a retail holiday (Cards Against Humanity).** Scaled-down options from source 03: pay a few customers to test and document the product publicly; a deliberately anti-promotional gesture that fits the brand's humor. Sources: 03 [f3d618345541]; 02 [0874da44648a].

**O2. Anti-marketing fits a Millennial or Gen Z audience, or a commoditized category where the brand cannot outspend big retailers at peak events; design it as a filter and an inside joke, not for reach; make sure site and operations can take a viral spike.** Participants buy membership in something, not a product. Sources: 02 [0874da44648a].

**O3. Budget the stunt against the marketing line; compare earned media value to incremental orders and contribution margin, not site traffic alone, and pass only if that value is worth more than the spend.** No source gives a valuation method. Liquid Death's founder claims a $50,000 stunt can earn the reach of a $50 million TV buy (founder claim). Patagonia's "Don't Buy This Jacket" cost $57,000 and drew "tens of millions" in free publicity; 2012 sales up almost a third to $543 million (secondary, source says treat with mild caution). Sources: 03 [f3d618345541] [d2474fde6f0e] [24e7dd3a3012]; 02 [0874da44648a].

**O4. Stunt frequency: 1 or 2 a year, no more.** Source 03's text; its cards say "1 per season" (up to 4 a year). The agent follows the text unless the owner decides otherwise. See 7.1. Sources: 03 [f3d618345541] [24e7dd3a3012].

**O5. Legal, ethics and brand-risk review before any stunt; no source gives it.** Card additions only: offended audiences, when the joke backfires, contest and paid-internship rules, gambling-style mechanics. Sources: 02 section 9; 03 section 9. `[web check: contest and promotion rules in the selling market]`

**O6. Anti-discount stance: replace a planned sale with a gift-with-purchase, a bundle or a price hold; do not lead with an instant 10% pop-up; do not blanket-discount.** Basis: source 03 cites Ritson, Binet and Field and Ehrenberg-Bass via a blog and Kantar (heavy discounting disillusions loyal customers and raises price sensitivity); source 02 says an instant 10% pop-up devalues the brand and attracts bargain hunters (Common Thread Collective framework); source 01 says blanket discounts erode brand value. Condition (card adaptation): assumes premium positioning or a real quality story; commodity categories may need promotional pricing. The body of source 03 says "risk: none major"; the card disagrees. ZALORA's move from discount-led to culture-led positioning (bold visual identity, influencer-led storytelling, omnichannel) is source 01's case; its outcome is an award, not sales. Sources: 03 [7c689b80e439] [d2474fde6f0e]; 02 [daa23b9732b1]; 01 [184e447721a2] [e48936d74dc0]. Discount design itself belongs to 03-OFF.

**O7. Values play: pair a genuine sustainability or quality message with a repair or resale program (A8).** Sources: 03 [d2474fde6f0e].

**O8. Guerrilla launch: go where the exact target customers gather, bring something tangible and surprising or solve an attendee pain (mud, heat, lines), sell on the spot if possible, make the moment worth photographing, carry it to digital afterwards, get venue permissions first.** Benjie at Coachella sold out its full inventory within a week (size not given); Privalia's truck at Lollapalooza (no numbers). Attribution is weak; do not expect clean ROAS. Sources: 01 [8f0ac696045b] [f16baa315a9f].

**O9. Mystery-first launch: anonymous placement, then the real message, then full reveal with distribution ready; each phase has a next step; the payoff must be worth the curiosity. Confirm inventory and fulfillment capacity before the reveal date; a weak payoff risks a stockout the store cannot fill.** Future Farm "Mars Awaits": 395 clicks to Sainsbury's, 17,000 likes. Lazada "haunted CCTV". Weak payoffs annoy people and can draw platform penalties (card). Suits playful or daring brands only. Sources: 01 [3062c8c8c22a] [d1f0d1622744].

**O10.** Moved to Appendix A: the Mercado Livre in-game native-placement case (platform-scale budget, not transferable to a small store).

**O11. Own an avoided topic in the category, with authenticity and sensitivity, on the platform where that audience already talks; measure CPA against other channels.** Maxfem (feminine intimate health, Brazil, TikTok Shop): CPA 40% lower than other media, qualified leads up 42%, and a revenue figure that is ambiguous (see 6, "Maxfem"). Health-adjacent claims face platform policy limits (card). Sources: 01 [e4ec9650b8d9].

**O12. Turn a flat functional benefit into a jingle, a character or a cultural line, and test it against the functional version.** Carrefour app jingle (no numbers). Sources: 01 [8a6bb1bcc38c].

**O13. Absurdist products show personality but only for brands whose voice allows it.** The Odd Company's City Napper on April Fool's Day sold out (quantity not given); no card covers it. Sources: 01 principle 38 (source text only).

### Group P. Hedged, outcome-linked promotions

**P1. An event-linked refund or freebie promotion is an experiment with a funded maximum liability, never "free" because a hedge exists.** Steps the card sets: define eligibility, qualifying orders, the outcome and the refund formula; calculate maximum refund exposure, operating cost and cash needed if the event happens; cap the test scope; do not count an unverified hedge as funding; get review of promotion terms and any risk transfer, including settlement and timing gaps between the refund date and the market payout; judge on incremental contribution and downside alongside attention. Cases: Forme (World Cup refunds hedged on Kalshi via PlayAbly, no results); The Jeffrey bar staked $5,000 on Kalshi to receive $13,514 if the Knicks won (2.70x, about $0.37 per $1 of payout, derived). Source 01's text calls the risk "capped and hedged"; the card overrides it. Sources: 01 [49b0963cfe85]. `[web check: Kalshi and Polymarket availability, contract terms, and whether outcome-linked promotions are legal in the brand's country]` `[needs brand data: order volume forecast in the event window, AOV, margin]`

### Group Q. No-ads week and founder tests

**Q1. No-ads week: zero paid acquisition for 1 week; use the time to personally contact 20 lapsed customers, 10 potential partners and 5 micro-influencers; measure organic traffic and conversions during and after; set the maximum acceptable revenue loss first; account for disruption to established paid campaigns.** The source does not warn about paid delivery disruption; the card does. Playbook addition: coordinate the window and the read with the 24-DEP agent, and keep the Meta account read-only (the pause is a human action). Sources: 01 [3043fc9b1846] [2d99a5dbeda9]. `[needs brand data: weekly organic vs paid revenue, last 12 months]`

**Q2. Province of Canada ran no ads for its first 5 years while the founders kept day jobs; the revenue line in the source is garbled ("built months over $100,000 in revenue"), so quote no figure.** Sources: 01 [3043fc9b1846].

### Group R. Onboarding, pop-ups, consolation

**R1. Question-first pop-up: replace the instant 10% pop-up with a segment question (Mott & Bow: Men's, Women's or Both), then a relevant incentive; store the answer as zero-party data; or send cold traffic to a quiz page (Bambu Earth).** Presented as a framework, not a tested win. The pop-up itself belongs to 07-LPG and 03-OFF; recorded here because its source sits in this folder and because the zero-party answer feeds H1 and I2. Sources: 02 [daa23b9732b1]. `[verify UI: pop-up and quiz tool]`

**R2. Consolation offer for giveaway non-winners: decide the follow-up before the giveaway ends; message only where follow-up is permitted and expected; use accurate eligibility and expiry wording; do not call a code "secret" or "exclusive" unless it is; track conversion from the messages; watch for leaked codes eroding margin.** Chemical Guys DMed non-winners a discount (case). The card is stricter than the source and is the rule. Sources: 02 [147b7a92331e]. `[verify UI: Instagram DM limits and automation rules]` `[web check: platform giveaway and messaging policy]`

**R3. First 100 days (K5).**

### Group S. Product and channel bets (recorded, pointed to neighbours)

**S1. A wild bet can live in the product: fix the category's known failure point with an unglamorous premium component and cut features that market well but fail in use.** Mokobara: Hinomoto wheels, dropped USB ports, front pocket for laptop and power bank, reinforced shell; no unit economics. Belongs to 01-PRD for the build. Sources: 02 [618f30b6989d].

**S2. A wild bet can live in distribution: be the only premium brand in a micro-channel at the moment of need; judge on contribution margin after fees.** Mokobara on BlinkIt (neck pillows hours before flights) and the IndiGo 2kg baggage tie-in. Sources: 02 [7d86ecac0ff5]. `[web check: whether these partnerships still run]`

**S3. Question an accepted category assumption, and over-invest in the category's biggest trust barrier.** Kogan (big-ticket TVs online, own stack, direct to manufacturers; "$10 billion business", measure unclear). Miss Amara (premium rugs sight-unseen via education, photography, styling, transparent specs; $26 million business). Sources: 01 [53352d5eca9e] [fc9236aec38b]. `[web check: what the Kogan $10 billion figure measures]`

**S4. Test a new country through a platform before local infrastructure; verify eligibility, fulfillment, payments, fees and local obligations first; keep entry reversible.** MBX TikTok-first then Amazon ("Earn Abroad"). Belongs to 22-AMZ for the marketplace build. Sources: 01 [9f28fac6f291]. `[verify UI: TikTok Shop cross-border]`

**S5. Validate demand with crowdfunding or pre-orders before inventory, with an existing audience and stated delivery timelines.** GIZMART: ¥100 million GMV in 12 hours (case). Delivery risk (card). Sources: 01 [63777fd226ea].

**S6. Creator-first and affiliate-first discovery (N7).**

## 4. Procedures (implementation)

Every procedure is L1 in ecomOS: the agent drafts, a human approves and executes. Each play ends with a **Bound** block in the same 8 fields (hypothesis, cohort, budget cap, metric, control, duration, stop rule, registry entry). Where a source gives a number it is quoted with its source; where none does, the field says so and names the brand data needed. "Expected effect" is always the source's reported example, never a forecast.

### P1. Design and bound a wild bet (every play starts here)

Goal: a bet brief and an approval request that a human can approve, reject or edit in 1 pass.
Preconditions: Stage 0 audit (P2) done or scheduled; brand voice, cash cap and labor hours known (section 2).

1. Name the category norm the bet breaks (rule A1) and the adjacent-industry model it borrows (A5). Source 01's 7-step design: list the category's unwritten rules, pick the 1 that feels most constraining, study adjacent industries, design with a limited downside, execute with obsessive detail, measure on the right metrics, double down or kill, document. [a7b8a9aa106c]
2. Check fit: brand voice (A6), values backed by a program (A8), emotional hook if the play is a gift (E3), margin room (B8). If any fails, pick another play.
3. Check the base: no customer in a failure state in the cohort (B2); base-effort audit passed or the bet is a Stage 0 fix (B3).
4. Write the 8-field bound:
   - Hypothesis: "If we [play] for [cohort], then [metric] rises vs control by [amount the human sets] within [duration]." The sources give no minimum lift; the human sets it.
   - Cohort: who, how many, how ranked, exclusions (failure state, no consent, first-time buyers unless the play is for them).
   - Budget cap: cash (pieces x cost per piece plus vendor fees plus gifts plus refund exposure) and labor (hours x people). Cost sources: notes $1 to $3 (03), letters $1 to $5 (03), art $20 to $40 (03), inserts cents to a few dollars (03), rep budget $50 to $200 per incident (03). Everything else: `[needs brand data: vendor quote]`.
   - Metric: the relationship metric from D2 (repeat-purchase rate, 90-day reorder, retention, AOV, referral share, full-price sell-through, refund rate) plus incremental contribution after all costs. Earned media on a separate line (D3).
   - Control: randomized holdout from the same ranked list, drawn before treatment (C2, 5.3). For mail: email-only control plus no-mail holdout (G6).
   - Duration: start date, review date (C8). Source 03's stage windows: 1 month, 90 days, 6 months.
   - Stop rule: from C6, made specific to the play.
   - Registry entry: id and the fields in P22.
5. Legal and consent items (C7) listed with owner and status.
6. Draft the customer-facing wording (note text, email, terms, claims page) with the writing rules: short sentences, digits, no invented claims, no "secret" or "exclusive" unless true.
7. Assemble the approval request (9.2) and stop. Do not execute.

Checks: every field filled; no field says "TBD"; the exclusion list attached; the expected effect carries a source label.
Rollback: a rejected brief goes back to step 1 with the reviewer's reason recorded in the registry as "not run".

### P2. Stage 0: base-effort audit (fix effort first)

Goal: confirm the operational base is low-effort before any delight play. Source 02 gives the checks and no pass mark; the human sets the bar.
Preconditions: support tool export, order data.

1. List every customer touchpoint. Tag each Operational Support or Brand Elevation (B6). [702bc45b5b83]
2. Pull CES, first-contact resolution, resolution time, transfers per ticket, repeat contacts per issue, contacts per order. `[needs brand data]` [aebda9584fe6]
3. Walk the 3 paths as a customer: a return, a cancellation, a fix for a broken item. Record channel switches, repeated explanations, waits. [9f47b7d4326c]
4. Compare measured resolution time with customer-reported effort (B4). A gap points at handoffs.
5. List "next issue" follow-ups per ticket type and write the pre-emptive answer into the first reply (B3).
6. Write the fix list. Fixes go to 17-CXP. Wild bets wait until the human accepts the base.
7. Build the standing exclusion list: customers with a failure open or closed in the last 7 days (B2). Refresh weekly.

Checks: 1 contact, no channel switch, no repeated explanation on the 3 paths = good. Transfers, repeats, long holds = fix first.
Rollback: none; this is a read.
Bound: not a bet. Registry entry type "base audit", with the metrics and the bar the human set.

### P3. Staged rollout with pass marks (source 03's plan, with Stage 0 added)

Goal: run the sources' plays in the order that keeps cost and risk low, passing each gate before the next.
Preconditions: P2 done.

| Stage | Window (source 03) | Plays | Pass mark (source 03 heuristic unless marked) | Next |
|---|---|---|---|---|
| 0 | Before anything | Base-effort audit (P2) | Human accepts CES, FCR, resolution time baseline (playbook addition from source 02) | Stage 1 |
| 1a | This month | Handwritten note or 60-second founder video to top 50 (P4), with control | Repeat-purchase rate or 90-day reorder rate of treated top 50 beats control | Expand touch to top 200 |
| 1b | This month | Keep-it refunds under $20, case by case (P5), own control | Repeat or 90-day reorder of keep-it recipients beats control; claims per customer rare | Consider raising threshold |
| 2 | Next 90 days | Named invite-only VIP tier for top 1%: early access, founder channel, surprise insert (P9, P16) | VIP retention and AOV beat non-VIP | Formalize tier; add tier 2 below |
| 3 | Next 6 months | Tiered referral waitlist with product rewards (P12); limited drop to SMS list (P10) | Referral signups above 30% of total; drop sells through at full price | Make drops a regular cadence; formalize referral mechanic |
| 4 | Ongoing | 1 stunt or values play that fits the voice (P18) | Coverage or shares worth more than spend (no valuation method given) | 1 or 2 a year, no more |

Adjustments (B8): thin margins delay warranties and narrow price locks; product that does not win a test skips proof-in-the-box; serious voice skips punk stunts.
Sources: [24e7dd3a3012] [42d04b3223ba] [1a706b82583a] [8fc70ea68011] [2984f2673be5] [f58ea6021437] [f42a03d72af2] [f3d618345541]. The 1a/1b split is a playbook addition (C3).
Checks after each stage: readout filed (P22) before the next stage's approval request.
Rollback: a failed gate stops expansion; the play may continue at its current size only if the human accepts the cost.

### P4. Handwritten note or founder video to the top cohort (Stage 1a). L1.

Goal: test whether a personal touch lifts repeat behaviour in the top cohort.
Preconditions: customer list ranked by lifetime spend; exclusion list; a founder or team member with the hours.
Conditions: repeat buyers with shown affinity (E2); neutral or positive state (B5).
Cost: $1 to $3 per note plus time (source 03); founder video: time only. Sources: [24e7dd3a3012] [42d04b3223ba] [aa796ddf08a2] [2d99a5dbeda9] [f7bb6a108f71].

1. Rank customers by lifetime spend. Take the top 50 (source 03) or top 10 from last quarter (source 01) if hours are tight. Remove exclusions. `[needs brand data]`
2. Randomly hold out a control from the same ranked list before writing anything (5.3).
3. Choose the touch: handwritten note referencing a specific past purchase, or a 60-second Loom-style founder video. Source 01's version adds a small unexpected gift (H9, H10).
4. Write no discount code (source 02 Founder's Ink) or a private code as the response device (source 03). Pick 1; record the choice (7.8).
5. Draft each note or script. Human writes and sends. No printed notes styled as handwriting (F4).
6. Log recipients, send dates, control ids.
7. At the review date, compare repeat-purchase rate and 90-day reorder rate, treated vs control; log referrals and unprompted mentions separately.

Checks: every recipient is a repeat buyer not in a failure state; the control was drawn before sends; each note names a real purchase.
Rollback: none needed; a note cannot be recalled. Stop rule below.
Expected effect (example): source 03 says "if repeat-purchase rate rises vs control, expand"; no case gives the lift. Wufoo and Chewy claim loyalty; no numbers.
Bound: Hypothesis: personal touch lifts 90-day reorder of the top 50 vs control. Cohort: top 50 by lifetime spend, repeat buyers, exclusions applied; control drawn from ranks 1 to 100. Budget cap: 50 x $3 = $150 plus 50 x (minutes per note) labor; the human sets the labor cap. Metric: 90-day reorder rate and repeat-purchase rate, treated vs control; referrals logged. Control: randomized holdout, same list. Duration: sends within 2 weeks; review at 90 days. Stop rule: labor cap hit; any recipient found in a failure state (pause and fix). Registry entry: play "note-top50", stage 1a.

### P5. Keep-it refunds pilot (Stage 1b). L1.

Goal: test whether returnless refunds on low-value items cut return cost and lift repeat behaviour without abuse.
Preconditions: cost per return, resale recovery, return reasons by SKU; support macros. `[needs brand data]`
Conditions: damaged, perishable or hard-to-resell goods; case by case; not advertised (J1). Sources: [1a706b82583a] [24e7dd3a3012].

1. Set the threshold. Source 03 example: under $20. Playbook addition: set it where refund value is below return shipping plus handling plus expected resale loss (J2). `[needs brand data]`
2. Write the support rule: eligible reasons, eligible SKUs, max claims per customer per period (the source gives none; the human sets it), and what the agent says (no mention of a "policy").
3. Randomize: half of eligible return requests get keep-it, half follow the standard return (control). Draw by customer id before the request is handled.
4. Log every keep-it: customer, SKU, reason, value, prior claims.
5. Review at the stage window: repeat-purchase or 90-day reorder of keep-it recipients vs control; return cost per order; claims per customer.
6. Raise the threshold only on a pass (J3).

Checks: no public wording anywhere; claims per customer stay rare; fraud signals (repeat claimers, mismatched reasons) reviewed weekly.
Rollback: turn the rule off; standard returns resume; nothing owed.
Expected effect (example): source 03 context only: 59% of surveyed retailers ran keep-it in 2023, up from 26% (goTRG); about 9% of returns are fraudulent (NRF); O Positiv credits a no-return guarantee for scaling (brand claim). No lift figure.
Bound: Hypothesis: keep-it under the threshold lifts 90-day reorder vs standard returns and lowers cost per return. Cohort: customers requesting a return on eligible SKUs under the threshold. Budget cap: refund value forgone = expected claims x average item value; the human sets the cap. Metric: 90-day reorder rate, cost per return, claims per customer. Control: randomized standard-return group. Duration: 1 month (source 03 Stage 1), review at 90 days for reorder. Stop rule: claims per customer exceed the set cap; fraud signals; cap hit. Registry entry: play "keepit-under-20", stage 1b.

### P6. Programmatic direct mail program. L1.

Goal: add a triggered physical letter to 1 lifecycle moment and prove it is incremental over email.
Preconditions: a mail vendor available in the brand's country `[web check]`; ESP integration `[verify UI]`; address data quality; consent and privacy review (G9); cost per piece `[needs brand data: vendor quote]`. Sources: [fcef726cbd6f] [3790fdeac0c7] [a9e802c5098a] [e890000fa7eb] [70a71f09d8c2] [898e3d534adb] [fafb61f67162].

1. Map journeys: welcome, abandoned cart, browse, post-purchase, second purchase, birthday, win-back.
2. Pick 1 moment where a physical touch adds value for a high-value segment (G2). Start with the moment that has the most volume and the highest cart value.
3. Connect the vendor to the ESP so the same event fires mail and email. `[verify UI]`
4. Set timing as a test variable, not a constant: the 48-hour cart trigger is unsourced; "within days" (Lulu and Georgia), 30 to 60 days (compiler), 6 to 12 months (compiler). Use the brand's repurchase interval (G7).
5. Personalize: exact abandoned or recommended products; cohort-specific offer (G3). Paper stock and format match brand values (G8).
6. Add a response device to every piece: QR code, unique URL, unique code (G4).
7. Frequency cap: 1 mailing per customer per 30 days (G5).
8. Controls: split eligible customers 3 ways before send: mail plus email, email only, no contact (randomized holdout). (G6)
9. Feed scans and code use back to the ESP for follow-ups (G10).
10. A/B test offer, creative, timing and format in later waves (G12).

Checks: vendor identity match rate on the file (Lulu and Georgia case: 80%; low match limits results); every piece has a device; consent and privacy sign-off attached; no customer mailed twice in 30 days.
Rollback: turn off the trigger; pieces already printed are sunk.
Expected effect (examples, all vendor cases, metrics undefined): Bergzeit birthday letters about 7.5% redemption; Fressnapf second-purchase letters to 15,000 customers, "ROI of 6", conversion doubled vs control; GOLDNER welcome letters 3.4% to 13.6%; Lulu and Georgia 22x iROAS, 78.5% more incremental revenue; thredUP ROI up 128%; Magazine.co.uk 38.81% higher conversions; DukesHill 22% more conversions; Furn 514 letters, "40% return rate" undefined; Woolroom "tripled engagement" in a title with no body figure.
Bound: Hypothesis: a letter at [moment] lifts conversion of [segment] over email-only and over no contact by more than its cost. Cohort: [segment] with a valid address, consent where required, not in a failure state; source cohorts ranged from 514 to 15,000. Budget cap: pieces x cost per piece plus setup; the human sets it. Metric: conversion or redemption via device, incremental contribution after mail cost vs both controls. Control: email-only and no-contact holdouts, randomized. Duration: 1 wave plus the repurchase window; review date set. Stop rule: match rate too low to fill the cohort; no lift over email-only at review; cap hit; a privacy or consent issue. Registry entry: play "pdm-[moment]".

### P7. Artifact gift and emotional art. L1.

Goal: test whether an unbranded, personal gift to the top cohort produces repeat, referral and shares.
Preconditions: known preferences (zero-party data, support notes) for artifacts; an emotional category hook for art (E3); supply secured (H5). Sources: [0f05cded3cb1] [eb580823eb04] [4b114e40b69d] [e29188eb0294] [63f18883754c] [ca8e2e37165b] [89bcc55e9cc4].

1. Pick the form. Artifact: high-quality practical item, no logo, matched to a stated preference (top 1% of repeat buyers, source 02). Art: a custom piece of a personal artifact the product touches (pet, home, car, baby, hobby), $20 to $40 per piece (source 03), a small weekly set of loyal repeat buyers.
2. Rank and select the cohort; apply exclusions; draw the control first.
3. Pick a random date away from holidays, birthdays and purchase anniversaries; spread sends across the calendar (H2).
4. No announcement, no purchase required, no strings (H3). For inner-circle gifts, only with a volunteered preference, via the buyer (H7).
5. Secure artists or suppliers before the first send (H5).
6. Human orders and ships. Log recipient, item, cost, date.
7. Track posts, shares, referrals and repeat vs control; expect negative direct ROI (H6).

Checks: no logo on the item; the date is not an occasion; the recipient is not in a failure state; the category has an emotional hook (art).
Rollback: pause sends; nothing to recall.
Expected effect (examples): Chewy claims customer-for-life loyalty and heavy sharing from about 1,000 portraits a week (press, company claim). Ruhlin's Brooks Brothers showroom won "a lifelong advocate" (B2B anecdote).
Bound: Hypothesis: an unbranded personal gift lifts repeat and referral in the top cohort vs control. Cohort: top 1% of repeat buyers (artifact) or 10 to 20 loyal repeat buyers a week (art), exclusions applied. Budget cap: pieces x $20 to $40 (art) or pieces x item cost (artifact); the human sets the cap and the weekly count. Metric: repeat rate and referral rate vs control; posts and shares on a separate line. Control: randomized holdout from the same list. Duration: 8 to 12 weeks of sends; review at the repurchase interval. Stop rule: recipients start expecting or asking for gifts; no posts and no repeat lift at review; cap hit. Registry entry: play "artifact-top1pct" or "art-weekly".

### P8. Frontline no-approval budget. L1.

Goal: let reps act on cues with a small surprise, inside caps, without escalation.
Preconditions: Stage 0 passed; support tool can log spend; caps set by the human. Sources: [7ae163d5a82f] [ad5810cd8a68] [22e369c1edc4] [246d16432222] [702bc45b5b83].

1. Set the per-incident cap sized to margin and AOV. Source 03 example: $50 to $200; Ritz-Carlton's $2,000 is against about $250,000 guest LTV (0.8% per incident, derived). `[needs brand data: LTV, AOV, margin]`
2. Set the guardrails no source gives (I3): per-rep monthly cap, per-customer cap per period, mandatory log fields (customer, cue, item, cost, state of the customer), weekly review.
3. Write the rule: neutral or positive state gets a surprise on a cue; failure state gets the fix first, then only after the fix is confirmed a small non-templated gesture (7.2).
4. Train reps to catch cues (trip, event, milestone) and to pick a specific item (trail map, socks, local treat in the box).
5. Human approves the policy; reps run it; the agent reads the log.

Checks: every spend has a cue; no spend on an unresolved failure; per-rep spend within cap.
Rollback: suspend the budget; nothing owed.
Expected effect (examples): Ritz-Carlton and Eleven Madison Park anecdotes; no ecommerce numbers.
Bound: Hypothesis: cue-based surprises lift repeat and NPS among touched customers vs untouched similar customers. Cohort: customers who contact support and are not in a failure state. Budget cap: monthly total = reps x per-rep cap; the human sets it. Metric: repeat rate and NPS of touched vs a matched untouched group; log review for abuse. Control: matched customers with similar contact type not touched (a true randomization is possible by alternating eligible tickets; playbook addition). Duration: 90 days. Stop rule: spend without cues; per-rep cap breaches; touched customers show no lift at 90 days. Registry entry: play "rep-budget".

### P9. VIP tier and invite-only access (Stage 2). L1.

Goal: a named, invite-only tier for the top 1% with benefits that beat the friction of gating.
Preconditions: Stage 1a passed; revenue share of the top 1% measured (E1); loyalty or membership tool `[verify UI]`. Sources: [8fc70ea68011] [2984f2673be5] [11a4bf90d117] [6cb0a48f51d6] [9a0245f0095a].

1. Rank by lifetime spend; invite the top 1%. `[needs brand data]`
2. Name the tier. Benefits: first access to drops, exclusive products, events, a direct founder channel; a 60-second founder video on joining or after a big order; a surprise insert (sticker plus note) in every VIP order.
3. Reward non-purchase actions too (reviews, UGC) with gifts and invites; movement within tiers by engagement (L7).
4. Keep benefits tied to loyalty so a leak does not look unfair (M2).
5. Gate early access with a waiting room, single-use links or a fast-pass. `[verify UI: Queue-it or store platform]`
6. Human sends invites. Log members and join dates.
7. At 90 days compare VIP retention and AOV to non-VIP; add a second tier only on a pass.

Checks: benefits are worth the friction (M2); no benefit is a blanket discount (O6); the founder channel is staffed.
Rollback: the tier stays for existing members; stop inviting.
Expected effect (examples): CRED 13 million+ monthly actives (reported); HOG members spend 30% more on clothing and events (brand-reported). No ecommerce tier lift figure.
Bound: Hypothesis: VIP members retain and spend more than comparable non-members. Cohort: top 1% by lifetime spend. Budget cap: inserts x cost plus founder hours plus event costs; the human sets it. Metric: retention and AOV, VIP vs matched non-VIP (top 2% to 3% as the comparison group; playbook addition, since random exclusion from a VIP tier is hard to justify). Control: matched non-members; note the self-selection risk (D4). Duration: 90 days. Stop rule: retention and AOV flat at 90 days; benefit leaks causing complaints; founder channel unanswered. Registry entry: play "vip-top1pct", stage 2.

### P10. Limited drop (Stage 3). L1.

Goal: sell a small numbered batch at full price to insiders on a set schedule.
Preconditions: an audience already built (M4); a hero product developed and tested; an SMS list with consent (M5); a waiting room or single-use links `[verify UI]`. Sources: [56c8c219238a] [f76f1da8af54] [f42a03d72af2] [b7edaaaeed23] [11a4bf90d117].

1. Fix inventory, release time and cadence (Last Crumb: weekly; MSCHF: set Tuesdays). No fake timers, no restock promises (M3).
2. Tell insiders (VIP tier or SMS list) the day before.
3. Gate access so members, not bots or resellers, get in.
4. Price at full price. Design packaging and the reveal (M8).
5. Human launches. Log sell-through time, buyers, buyer overlap across drops, reseller listings.
6. Keep the cadence only if drop frequency tracks repeat visits or purchase frequency (M7).

Checks: real scarcity; fans not shut out (M6); resellers not capturing stock.
Rollback: pause the cadence; unsold stock returns to normal sale.
Expected effect (examples): Last Crumb "sold out in seconds" after 1 year of brand building; MSCHF drops "often sell out in minutes"; no sell-through rates given.
Bound: Hypothesis: numbered drops to insiders sell through at full price and lift repeat purchase across drops. Cohort: VIP tier or SMS list with consent. Budget cap: inventory at risk plus packaging plus gating tool fees; the human sets it. Metric: full-price sell-through, time to sell out, repeat buyers across drops, reseller capture. Control: no clean holdout for a public drop; compare full-price share and repeat rate vs the same product sold normally in a prior period (baseline comparison, weaker than a control; say so in the readout). Duration: 3 drops. Stop rule: any drop fails to sell through at full price; reseller capture; fan complaints about supply; ops strain. Registry entry: play "drop-[product]", stage 3.

### P11. Founder's Ink and the annual letter. L1.

Goal: a yearly handwritten letter to the top 1% of repeat buyers.
Preconditions: top 1% list; executive hours. Sources: [05b6ed77af75] [42d04b3223ba] [eb580823eb04].

1. Once a year, pull the top 1% of repeat buyers. Cap at what the executive team can handwrite (C4). `[needs brand data]`
2. Each letter names the buyer's specific past purchases.
3. Decide the code question and record it: source 02 says no discount code, gratitude only; source 03 says include a private offer code or a tear-off referral insert to measure response (7.8). If no code, measure by repeat rate vs control only.
4. Pick the send date: source 02's random-timing rule says avoid holidays and anniversaries even for this annual letter (7.8).
5. Draw the control before writing. Human writes and sends.
6. Budget as a fixed small activity, not direct response (H9).

Checks: handwritten by the executive team, not printed; each letter names a real purchase.
Rollback: none.
Expected effect: no case number in any source.
Bound: Hypothesis: the annual letter lifts repeat rate in the top 1% vs control. Cohort: top 1% by repeat orders, capped at writable count. Budget cap: letters x $1 to $5 (source 03) plus executive hours. Metric: repeat-purchase rate at the repurchase interval; code redemptions if a code is used. Control: randomized holdout within the top 1% (or top 2% if the tier is too small to split). Duration: 1 send; review at the repurchase interval. Stop rule: executive hours exceeded; letters drift to printed. Registry entry: play "founders-ink".

### P12. Tiered referral waitlist (Stage 3). L1.

Goal: fill a launch or drop waitlist through referrals with product rewards.
Preconditions: a launch or drop to gate; a waitlist page tool (no source names one) `[verify UI]`; fraud filter plan. Sources: [f58ea6021437] [24e7dd3a3012] [68c4bfa88afe].

1. Gate the launch behind a waitlist. Each signup gets a unique link.
2. Set escalating, reachable product or access rewards (Harry's: 5 referrals = shave cream, 10 = razor, and up). Never cash (N1).
3. Show a live progress bar toward the next reward.
4. Plan fraud filtering (Harry's counted 85,000+ of 100,000+ as legitimate; no steps given). Playbook addition: verify emails, cap rewards per IP or device, hold rewards until launch.
5. Human launches. Log signups, referral share, legitimate share.
6. Pass mark: referral signups above 30% of total (source 03 heuristic).

Checks: rewards are product or access; the progress bar is live; fraud filter on.
Rollback: close the waitlist; honor earned rewards.
Expected effect (examples): Harry's 100,000+ emails in 1 week, 77% from referrals; Dropbox 100,000 to 4 million users in 15 months (reported, different mechanic).
Bound: Hypothesis: referral rewards bring more than 30% of signups at a lower cost per signup than paid. Cohort: launch or drop waitlist. Budget cap: expected rewards x product cost plus tool fee; the human sets it. Metric: referral share of signups, legitimate share, cost per legitimate signup, later conversion. Control: none clean; compare cost per signup with the paid channel in the same window (say so in the readout). Duration: the pre-launch window. Stop rule: fake-signup share rises; referral share below 30% at midpoint with no fix; reward cost exceeds cap. Registry entry: play "referral-waitlist", stage 3.

### P13. Expiring loyalty value, delayed discount, daily reveal, targeted flash sale. L1.

Goal: add a time-limited value mechanic that gives customers a reason to return, without training discount dependency.
Preconditions: a loyalty app with expiry and reminder triggers `[verify UI]`; SMS and email consent; current points liability. Sources: [07497417cc0a] [a03a3ab4e941] [67ba6fcee11e] [184e447721a2].

Expiring coins (Haus & Kinder pattern):
1. Award coins on every purchase. Disclose the expiry and redemption terms before customers earn (L1).
2. Set a real expiry window (case: 60 days). Check that earn rate and redemption are meaningful first (5.6).
3. Reminders on email and SMS, worded as loss of earned value; SMS only with consent.
4. Track redemption, repeat rate vs a no-expiry control cohort, and share of signups through loyalty (L2).

Delayed discount:
1. No discount on the current order; the reward unlocks on the next purchase with an expiry.
2. Message the earned value ("you have $X waiting").
3. Test unlock threshold and expiry window vs a no-reward control. Skip for one-time-purchase categories. Record the accounting liability.

12-day daily reveal:
1. Seasonal window; 1 genuinely valuable offer per day planned in advance; no filler.
2. Calendar gate, midnight expiry, "missed" state, rules up front. Not year-round.

Targeted flash sale:
1. Loyalty segment only; personalized; high-visibility urgency cue; occasional. Track conversion and brand perception side by side; check for leakage.

Checks: terms disclosed before earning; consent for SMS; no evergreen countdown; redemption practical.
Rollback: extend or remove the expiry for affected customers (a human decision); pause reminders.
Expected effect (examples): Haus & Kinder "70X ROI" on tooling (undefined), 12.4% of signups via loyalty; L'Occitane "82% Return Rate" undefined; Bombas no numbers; Talon.One clients no numbers.
Bound: Hypothesis: expiring value (or the delayed reward) lifts repeat rate in the loyalty base vs a control with no expiry (or no reward). Cohort: loyalty members with consent, in a repeat category. Budget cap: incremental reward cost plus tool fees; the human sets it; points liability recorded. Metric: repeat-purchase rate, redemption rate, complaints per 1,000 reminders, share of signups via loyalty. Control: randomized no-expiry (or no-reward) cohort. Duration: 2 expiry cycles (120 days at a 60-day expiry). Stop rule: complaints rise; redemption is impractical; repeat rate no higher than control at review. Registry entry: play "expiring-coins", "delayed-discount", "daily-reveal" or "flash-loyalty".

### P14. Proactive pause, price lock, cancellation handling. L1.

Goal: keep subscribers by removing friction and protecting their wallet, and handle cancellations without delay.
Preconditions: subscription tool with pause, skip, rollover `[verify UI: Recharge or the brand's tool]`; consumption data. Sources: [c58b965fe70a] [6812a43572e9] [36d5dbe4d17c] [7c689b80e439] [dee4592d0973].

Proactive Pause:
1. Compare shipments received with consumption per SKU. Flag subscribers overstocked. The source gives no threshold; the human sets one. `[needs brand data]`
2. Email flagged subscribers advising a pause "to save money". Frame as protecting the wallet, not retention.
3. Allow easy pause and credit rollover.
4. Track resume vs cancel after pause, vs a flagged-but-not-emailed control.

Price lock:
1. Ring-fence who qualifies (for example current subscribers at launch). Model future unit cost trends before promising. `[needs brand data: cost trend per unit]`
2. Market it as a loyalty benefit. Keep it narrow on thin margins. Alternative: a price hold framed as a promotion during inflation.
3. Test on an eligible cohort; measure retention vs non-locked subscribers.

Cancellation:
1. Cancellation is never delayed (K3). Optional reason field; gentle support invite.
2. If hardship is volunteered: approved remedy (pause or eligible refund); gesture only when welcomed; no upsell; no templated sympathy.
3. Staff trained; no inference of grief or family ties from data.

Checks: pause is 1 click; no save-offer wall; cancellation completes on request.
Rollback: pause emails stop; price locks already granted are honored.
Expected effect (examples): ClassPass "massive retention gains" (no number); Yankee Candle 90% retention with custom cadence (blog, no method); BarkBox lock is historical; Chewy bereavement loyalty is a company claim.
Bound: Hypothesis: a proactive pause suggestion lowers cancellation among overstocked subscribers vs flagged subscribers not emailed. Cohort: flagged overstocked subscribers. Budget cap: revenue deferred by pauses; the human sets an acceptable amount. Metric: cancel rate at 90 days, resume rate after pause, LTV at 6 months. Control: randomized flagged-not-emailed group. Duration: 90 days. Stop rule: deferred revenue exceeds cap; cancel rate higher in the emailed group. Registry entry: play "proactive-pause" (price lock and cancellation as their own entries).

### P15. Lifetime warranty and outcome guarantee. L1.

Goal: remove the "will it last" or "will it work" objection with a promise the brand can fund.
Preconditions: defect and failure rates by SKU; refund rate baseline; legal review of warranty and guarantee terms (C7). Sources: [04f54549fb37] [3a74574fff82] [24e7dd3a3012].

Lifetime warranty or repair-for-life:
1. Most durable SKUs only. Model expected claims, repair logistics and cost before promising. `[needs brand data: failure rates]`
2. Repair-first, not replace-always. Define scope and exclusions.
3. Publish a clear, friendly claims page. `[web check: warranty law in the selling market; current Osprey and Darn Tough terms]`
4. Thin margins: delay.
5. Track claims rate and cost per claim by SKU.

Outcome guarantee:
1. Pick a specific, measurable outcome the product produces.
2. Promise it with a clear, product-appropriate remedy for a substantiated claim. No "keep working until" for physical products.
3. Track refund rate before and after; scale only if refunds barely move.

Checks: terms specific; claims page live; refund handling is low-effort (B1).
Rollback: close the guarantee to new orders; honor existing promises.
Expected effect (examples): Hormozi "about 30% more sales, refunds barely up" (services, book summary); LL Bean and Eddie Bauer pulled back generous guarantees (cost signal).
Bound: Hypothesis: the guarantee lifts conversion on the covered SKU more than its claim cost. Cohort: buyers of the covered SKU; the offer can be shown to half of traffic (A/B on the PDP; belongs to 09-CRO for setup). Budget cap: modeled claims x cost per claim over the window; the human sets it. Metric: conversion rate with vs without the promise, refund or claim rate, cost per claim. Control: PDP A/B split. Duration: 60 to 90 days plus the claim window. Stop rule: claims or refunds exceed the model; disputes; cap hit. Registry entry: play "warranty-[sku]" or "guarantee-[outcome]".

### P16. Surprise inserts and welcome kit. L1.

Goal: a low-cost surprise in first or VIP orders that ties to a tracked action.
Preconditions: packing process can add an item; response device (code or insert). Sources: [9a0245f0095a] [2984f2673be5] [898e3d534adb].

1. Pick the insert: sticker, sample, small gift; cents to a few dollars (source 03). Personal, not generic filler.
2. Pair it with a handwritten thank-you (not printed-as-handwriting).
3. Tie it to a tracked action: referral code, VIP invite, tracked reorder offer.
4. For club members, the fuller version is a welcome kit: personal note, small gift, benefits list (GOLDNER).
5. Randomize by order id: half of eligible orders get the insert.
6. Track reorder and referral vs control.

Checks: insert is personal; device works; cost per order within cap.
Rollback: stop adding; nothing to recall.
Expected effect (examples): GOLDNER welcome letters 3.4% to 13.6% conversion (vendor case); Grilla Grills and boAt no numbers.
Bound: Hypothesis: the insert lifts reorder or referral vs orders without it. Cohort: first orders or VIP orders. Budget cap: orders x insert cost; the human sets it. Metric: 90-day reorder rate, referral code use, vs control. Control: randomized by order id. Duration: 60 to 90 days. Stop rule: no lift at review; cost per order over cap. Registry entry: play "insert-[type]".

### P17. Hedged, outcome-linked promotion. L1.

Goal: a public promise tied to a binary event, with liability funded in cash and every term reviewed.
Preconditions: legal review of promotion terms and any risk transfer `[web check: legality in the brand's country; Kalshi and Polymarket access]`; order forecast for the event window `[needs brand data]`. Sources: [49b0963cfe85].

1. Pick an event customers care about with a binary outcome.
2. Define eligibility, qualifying orders, the outcome and the refund formula.
3. Calculate maximum refund exposure = forecast qualifying orders x refund per order, plus operating cost. Cap the scope (an order cap, a date window, a per-order cap) so the exposure fits cash on hand.
4. Fund the maximum liability in cash. A hedge is optional and never counted as funding until verified (C5). If a hedge is used, record stake, payout, settlement date and the gap to the refund date (The Jeffrey: $5,000 stake, $13,514 payout, 2.70x).
5. Get review of terms and risk transfer.
6. Human launches. Track qualifying orders daily against the cap.
7. Judge on incremental contribution and downside, with attention on a separate line.

Checks: exposure capped and funded; terms public and clear; daily order count vs cap.
Rollback: close the promotion to new orders at the cap; existing promises honored.
Expected effect (examples): Forme gave no results; The Jeffrey's hedge covered the tabs.
Bound: Hypothesis: the promise lifts qualifying orders in the window by more than the expected payout. Cohort: orders in the window on eligible SKUs. Budget cap: maximum refund exposure, funded. Metric: incremental orders vs the same window last year or a matched period (no clean control for a public promo; say so), expected payout, realized payout, contribution after payout. Control: none; baseline comparison. Duration: the event window plus settlement. Stop rule: order cap reached; a legal issue; cash for the liability not confirmed. Registry entry: play "hedged-promo-[event]".

### P18. Stunt, anti-discount swap or values play (Stage 4). L1.

Goal: 1 big swing a year (or 2 at most) that earns coverage worth more than it costs.
Preconditions: Stages 1 to 3 passed; a strong, specific voice (A6); legal, ethics and brand-risk review (O5); site and ops ready for a spike (O2). Sources: [f3d618345541] [0874da44648a] [7c689b80e439] [d2474fde6f0e] [24e7dd3a3012].

1. Pick the format by voice: entertaining content people would watch anyway; a stunt that dramatizes the product benefit; an anti-promotional gesture on a retail holiday; or, for a serious voice, an anti-discount swap (gift-with-purchase or bundle instead of a sale) or a values play backed by a real program.
2. Scaled-down options: pay a few customers to test and document the product publicly; a deliberately anti-promotional gesture in the brand's humor.
3. Budget it as a marketing cost. Write the earned-media valuation method before launch (no source gives one; the human approves the method).
4. Review legal, contest, paid-participation and platform rules. Review the failure case: who could be offended, what happens if the joke lands flat.
5. Confirm site capacity and stock for a viral spike (CAH 2018: 50,000 simultaneous page views, reported).
6. Human launches. Track coverage, shares, mentions, site traffic, sales in the window, refunds and complaints.
7. Pass mark: coverage or shares worth more than the spend. If passed, do 1 or 2 a year, no more (7.1).

Checks: voice fit confirmed by the owner; failure case written; capacity confirmed.
Rollback: a public stunt cannot be withdrawn; the stop rule is about not repeating.
Expected effect (examples): Patagonia $57,000 ad, "tens of millions" in publicity, 2012 sales up almost a third (secondary, mild caution); CAH 2014: 30,000 boxes of bull feces at $6 = $180,000 in 2 hours (checks); CAH 2015: 11,248 people paid "$5 for nothing", reported total $71,145 (source 02) or "over $70,000, outlets vary $50,000 to $70,000+" (source 03); 11,248 x $5 = $56,240, so either some paid more than $5 or a figure is off; quote as "$56,240 to $71,145, unaudited" `[web check: CAH 2015 totals]`; CAH 2016 hole: $100,573 over 50+ hours (source 03) vs "over $100,000" (source 02), consistent; Wakefit Sleep Internship: 170,000 applications, zero paid ads (reported); Liquid Death founder's $50,000 vs $50 million claim.
Bound: Hypothesis: the stunt earns coverage and shares valued above its cost by the agreed method, and does not raise complaints or refunds. Cohort: public. Budget cap: production plus media plus fulfilment of any giveaway plus a contingency for the spike; the human sets it. Metric: earned media by the agreed method, shares, mentions, site traffic, new customers in the window vs a matched window, complaints and refunds. Control: none; matched-window baseline. Duration: the campaign window plus 4 weeks. Stop rule: backlash; legal complaint; cap hit; do not repeat within the year if the pass mark fails. Registry entry: play "stunt-[name]", stage 4.

### P19. First 100 days onboarding and proof in the box. L1.

Goal: cut early churn by over-investing in the first 100 days, and let the customer prove the product.
Preconditions: repurchase interval and early churn baseline; for proof kits, a test the product wins safely. Sources: [7615a4af9401] [574b9d94f465].

100 days:
1. Treat days 0 to 100 after first purchase as the churn window. No cross-sell or review requests in it.
2. Plan the emotional journey (Coleman's 8 phases are named, not listed, in the source). Options: a welcome kit by expedited mail before the product arrives; sequential founder videos; surprise mailers; surprise digital upgrades.
3. Randomize new customers into the journey or the standard flow.
4. Measure repurchase rate and early churn at 100 days.

Proof in the box:
1. Pick 1 attribute the product can prove and that wins against rivals; run the test against rivals first.
2. Validate what the test measures, its limits and instructions; exclude unsafe or unreadable tests; do not present a selective comparison as full proof.
3. Put the test in the first box for half of first orders.
4. Measure conversion to second order vs control.

Checks: no review ask or cross-sell inside 100 days for the treated group; the proof test is safe and repeatable.
Rollback: revert to the standard flow.
Expected effect (examples): Country Delight's kit and FY24 revenue (about 1,380 crore) do not show causation; Coleman gives no numbers in the source.
Bound: Hypothesis: the 100-day journey (or the proof kit) lifts second-order rate vs the standard flow. Cohort: new customers. Budget cap: kits or mailers x cost plus video production; the human sets it. Metric: second-order rate at 100 days, early churn, support contacts per new customer. Control: randomized standard flow. Duration: 100 days plus enrollment window. Stop rule: cost per new customer over cap; no lift at 100 days. Registry entry: play "100-day" or "proof-in-box".

### P20. No-ads week. L1.

Goal: measure organic dependence and use the week for personal outreach.
Preconditions: 12 months of weekly organic vs paid revenue; a maximum acceptable revenue loss set by the human; the 24-DEP agent consulted on paid disruption; not a peak week. Sources: [3043fc9b1846] [2d99a5dbeda9] [9b43d5332e59].

1. Set the maximum acceptable revenue loss first (card addition).
2. Pick a week outside peak season. Record the paid baseline (Meta read only).
3. A human pauses paid acquisition for 7 days. The agent does not touch the account.
4. During the week: personally contact 20 lapsed customers, 10 potential partners, 5 micro-influencers.
5. Measure organic traffic, orders and revenue during and for 4 weeks after, against the prior 4 weeks and the same week last year.
6. Record any learning-phase or delivery disruption reported by 24-DEP after restart.

Checks: the loss cap agreed in writing; outreach list drawn from real customers with consent to be contacted.
Rollback: restart paid at any time if the loss cap is hit mid-week (human action).
Expected effect (examples): Province of Canada ran no ads for 5 years (garbled revenue figure, do not quote); Huckberry's slower build.
Bound: Hypothesis: organic revenue holds above [X]% of baseline without paid, and outreach produces [N] reactivations or partnerships. Cohort: whole store for the week; 35 named outreach contacts. Budget cap: the maximum acceptable revenue loss; outreach hours. Metric: organic revenue share vs baseline; reactivations from the 20 lapsed; partnerships opened; paid recovery time after restart. Control: prior 4 weeks and same week last year (baseline, not a control). Duration: 7 days plus 4 weeks of read. Stop rule: loss cap hit. Registry entry: play "no-ads-week".

### P21. Founder's inbox and the 20-customers exercise. L1.

Goal: founder insight from direct contact, before designing touch programs.
Sources: [2d99a5dbeda9] [aa796ddf08a2].

1. 20-customers exercise: write every touchpoint from discovery to post-purchase as if there were only 20 customers; mark where a manual human touch fits. Feeds P4, P7, P8, P16.
2. Founder's inbox: for 1 month, forward every service email to the founder to answer personally. Only while volume is low. Log themes weekly.
3. Founder calls to first or best customers; fix their problems personally.

Checks: volume low enough that replies stay within the service SLA (B1 still applies).
Bound: not a customer-facing bet. Registry entry type "founder read", with the themes found and the plays they suggest.

### P22. Readout and registry entry (every play ends here)

Goal: a readout the owner can act on and a registry entry the next bet can learn from.
ecomOS has no experiment registry yet. Until it exists, the entry lives in the quarterly plan deliverable (9.1) and in the brand record, in the format below, so it can be loaded into the registry later without rewriting.

1. Pull treated and control outcomes at the review date. Do the arithmetic in code (a script or spreadsheet), not by hand.
2. Report 2 lines: incremental contribution after all program costs (decision line) and attention signals (earned media, UGC, referrals, mentions) (signal line). Never merge them (D2, D3).
3. State the comparison quality: randomized control, matched group, or baseline only.
4. Decision: double down, keep at size, change 1 variable, or kill. Record why. One viral outcome is not proof (C8).
5. File the registry entry.

Registry entry fields: id; brand; play name and stage; hypothesis; cohort definition and size (treated, control); comparison type; start date; review date; cash cap and cash spent; labor cap and hours used; metric and result (treated, control, difference); attention signals; legal and consent items and status; stop rule and whether it fired; decision; approver; source rules and card ids used; what to change next time.

Checks: both lines present; comparison type stated; numbers computed in code; card ids listed.

### P23. Thin plays (source gives the idea, not the how). L1.

Each gets the same 8-field bound; the sources give no cost or cohort for any of them.

- **Mystery bundle or blind box** [85c5e90b4fff]: products profitable at the bundle discount; stated minimum value; consistent honest parameters; small segment first; margin and repeat measured; gambling-style rules checked `[web check]`. Elf: 6 bundles, 5 to 8 items, up to 50% off, early November (example). Bound: cohort = a loyalty segment; metric = margin at bundle price and full-price repeat after; control = segment not offered; stop = buyers start waiting for bundles.
- **Guerrilla event launch** [8f0ac696045b] [f16baa315a9f]: exact-customer events; tangible surprise or solve an attendee pain; sell on the spot; carry to digital; permissions first. Bound: cap = travel, stock, materials; metric = on-site sales, new customers with an event code, posts; control = none, baseline; stop = permit refused or cap hit.
- **Mystery-first phased reveal** [3062c8c8c22a] [d1f0d1622744]: anonymous placement, then the message, then the reveal with distribution ready. Future Farm: 395 clicks to Sainsbury's, 17,000 likes (example). Bound: cap = media cost; metric = reveal-day traffic and sales at the point of distribution; control = none; stop = platform penalty or weak engagement at phase 2.
- **Community co-creation and insider launch** [6fd8b0b7de34] [5eeef0648aad] [66b5d9fbb538] [fcb3a9e4905f] [0c1287c76ea8]: submit-and-vote with enough voters; credit and a cut; public rules on what can ship; start with 10 to 20 insiders; 6 months before a new product. Bound: cap = founder hours and event cost; metric = votes, launch sell-through to voters, repeat rate of insiders vs non-insiders; control = matched non-insiders; stop = vocal-minority skew or performative results.
- **Consolation offer after a giveaway** [147b7a92331e]: decided before the giveaway ends; permitted messaging only; accurate wording; tracked code. Bound: cap = code redemptions x discount; metric = conversion from messages, code leakage; control = non-winners not messaged; stop = leaked code.
- **Question-first pop-up or quiz** [daa23b9732b1]: setup in 07-LPG; the zero-party answer feeds gifts and rep cues here.
- **Livestream selling** [72d41c0813d1]: demonstration products; timed listings; in-stream checkout `[verify UI]`. Bound: metric = full-price sell-through in the stream vs the same SKU on site.
- **TikTok-first market test** [9f28fac6f291]: verify eligibility, fees, fulfilment, obligations; 1 market, small product set; reversible. Bound: metric = contribution margin after fees (D6). Marketplace build in 22-AMZ.
- **Crowdfunding or pre-order** [63777fd226ea]: existing audience; stated delivery timelines; delivery risk. Bound: metric = funded units vs target; stop = below target by the campaign midpoint.
- **Creator seeding with freedom** [4c2cd1cec3bf]: creators order independently and post unboxings; disclosure rules `[web check]`. Bound: metric = creator-attributed revenue vs product cost.
- **Anti-discount swap and price hold** [7c689b80e439] [d2474fde6f0e]: replace a planned sale with gift-with-purchase or a bundle; offer design in 03-OFF. Bound: metric = margin and units vs the same sale last year; stop = commodity category where units collapse (card caveat).
- **Product and channel bets** [618f30b6989d] [7d86ecac0ff5] [53352d5eca9e] [fc9236aec38b]: recorded in group S; built in 01-PRD and 22-AMZ.

## 5. Diagnostic checklists

Written so a worker can run each one. "Source" names the mini playbook and card.

### 5.1 Bet design review (before the approval request)

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Norm named | The brief names the category norm it breaks and the borrowed model | 1 norm, 1 model | "Do something viral" | Rewrite with A1, A5 | 01 [a7b8a9aa106c] |
| Voice fit | Owner confirms the play matches the brand voice | Confirmed in writing | Irreverent stunt for a serious brand | Switch to hospitality or status play | 02 [0874da44648a], 03 [f3d618345541] |
| Values backed | The program behind any values message exists today | Repair, resale or equivalent live | Message with no program | Drop the values play | 03 [d2474fde6f0e] |
| Standard tactic in disguise | Is it 10% off, BOGO, points or an abandoned-cart email with a new name? | A genuine twist | A standard tactic | Send to 03-OFF or 14-EML | 03 [24e7dd3a3012] |
| 1 play per cohort | No other play touches the same cohort in the window | Clean | 2 plays, 1 benchmark | Split (C3) | 03 [24e7dd3a3012], playbook |
| Cohort narrow enough | Team hours cover the cohort by hand | Yes | Cannot sustain | Shrink | 02 [05b6ed77af75] |
| Failure exclusions | Exclusion list attached and dated within 7 days | Attached | Missing | Attach (B2) | 02 [76193c44f7e8] |
| Emotional hook (gifts) | Category touches a pet, home, car, baby or hobby | Yes | Functional category | Pick a non-gift play | 03 [63f18883754c] |
| All 8 bound fields filled | Read the bound | No blanks | "TBD" | Fill or do not submit | 01 card, 03 [24e7dd3a3012] |
| Stop rule specific | The stop rule names a number or event | Specific | "If it doesn't work" | Use C6 | 01 [a7b8a9aa106c] |
| Expected effect labeled | Every quoted number carries its source and "reported, unaudited" | Labeled | Bare numbers | Label (D1) | all 3 |
| L1 stated | The request says a human executes | Stated | Implies the agent sends | Fix wording | ecomOS rule |

### 5.2 Economics check

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Cost per piece known | Vendor quote or source range on file | Quote | Guess | Get the quote; use 03's ranges only as placeholders | 03 [42d04b3223ba] [e29188eb0294] |
| Cash cap = pieces x cost + fees + gifts + refund exposure | Recompute in a sheet | Matches | Missing a line | Add it | 01 card [a7b8a9aa106c] |
| Labor counted | Hours x people in the cap | Counted | "Free" | Count it | 03 [24e7dd3a3012] |
| Margin room | Gift or refund cost vs gross margin on the cohort's orders | Cost well inside margin | Cost eats margin | Shrink cohort or item | 03 [7ae163d5a82f] card |
| Keep-it break-even | Refund value vs return shipping + handling + resale loss | Refund cheaper | Refund dearer | Lower the threshold | 03 [1a706b82583a], playbook |
| Warranty claims modeled | Failure rate x units x cost per claim | Modeled | Not modeled | Model or delay | 03 [04f54549fb37] |
| Guarantee refund exposure | Refund rate baseline x expected orders | Known | Unknown | Baseline first | 03 [3a74574fff82] |
| Hedged promo liability funded | Max exposure in cash on hand | Funded | Relies on a hedge | Cap scope until funded | 01 [49b0963cfe85] |
| Price lock modeled | Unit cost trend over the lock life | Modeled | Not modeled | Model | 03 [36d5dbe4d17c] |
| Points liability | Outstanding value with and without expiry | Recorded | Ignored | Record | 01 [a03a3ab4e941] |
| Rep budget caps | Per incident, per rep per month, per customer | All 3 set | Any missing | Set | 03 [7ae163d5a82f], 02 [22e369c1edc4] |
| Earned media outside the P&L line | Readout template has 2 lines | 2 lines | Earned media counted as revenue | Separate (D3) | 02 [89bcc55e9cc4] |
| Arithmetic in code | Sheet or script attached | Attached | Mental math | Attach | ecomOS rule |

### 5.3 Control group check

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Drawn before treatment | Timestamp of the holdout draw precedes the first send | Before | After | Redraw and restart | 01 [e890000fa7eb], 03 [24e7dd3a3012] |
| Same eligible pool | Control comes from the same ranked, filtered list | Same | Control from a different segment | Redraw | 01 [70a71f09d8c2] |
| Randomized | Random split, not "the ones we skipped" | Random | Convenience | Redraw | 01 card [e890000fa7eb] |
| Size can move the metric | Baseline rate x size gives enough events to see the human's minimum lift (compute in code; the sources give no sizes) | Enough events | A handful | Widen the pool or lengthen the window; the sources give no formula | playbook, `[needs brand data: baseline rates]` |
| Mail: 2 controls | Email-only and no-contact groups exist | Both | 1 or none | Add | 01 [70a71f09d8c2] [e890000fa7eb] |
| Not contaminated | Control not reached by the play (leaked codes, shared inserts, public wording) | Clean | Leaks | Tighten codes and segments | 01 [184e447721a2], 02 [147b7a92331e] |
| Self-selection handled | For engaged vs non-engaged reads, prior spend controlled | Handled | Raw comparison | Control for prior spend (D4) | 01 [ce5b3f63afcc] |
| Comparison type stated | Readout says randomized, matched or baseline | Stated | Implied | State | playbook |
| No control | The play is filed as an observation | Filed as observation | Filed as a test | Relabel | C2 |

### 5.4 Readout

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Review date honored | Readout at the planned date, not earlier on a viral spike or later on a quiet week | On date | Early or late | Wait or file now | 01 [a7b8a9aa106c] |
| Decision line | Incremental contribution after all program costs, treated vs control | Present | Missing | Compute | 01 card, 02 [89bcc55e9cc4] |
| Signal line | Earned media, UGC, referrals, mentions | Present, separate | Merged into revenue | Separate | 02 [89bcc55e9cc4], 03 [f3d618345541] |
| Window fits the play | Relationship plays read at the repurchase interval; transactional plays (drop, flash) read in the window | Fits | 30-day read on a slow play | Re-read at the interval | 01 [9b43d5332e59] [ce5b3f63afcc] |
| Stop rule status | Did it fire? | Stated | Unknown | State | C6 |
| Abuse signals | Keep-it repeat claimers, fake referrals, leaked codes, gift expectation | None | Present | Tighten or stop | 03 [1a706b82583a] [f58ea6021437] [e29188eb0294] |
| Decision recorded | Double down, keep, change 1 variable, kill, with reason | Recorded | Blank | Record | 01 [a7b8a9aa106c] |
| Registry entry filed | All fields in P22 | Filed | Partial | Complete | playbook |
| What changes next time | 1 to 3 lines | Present | Missing | Add | 01 [a7b8a9aa106c] |

### 5.5 Base-effort audit (Stage 0)

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Return without friction | Walk the return path | 1 contact, no switch | Transfers, repeats | Fix in 17-CXP first | 02 [702bc45b5b83] |
| Cancel without friction | Walk the cancel path | 1 click or 1 contact | Save-offer wall, delays | Remove friction | 02 [c58b965fe70a] [dee4592d0973] |
| Fix a broken item | Walk the path | Fast, no repeat explanation | Long hold, repeats | Fix | 02 [9f47b7d4326c] |
| CES, FCR, resolution time, transfers | Support export | Baseline accepted by the owner | No data | Instrument first | 02 [aebda9584fe6] |
| Perceived vs actual effort | Compare timer with customer-reported effort | Close | Gap | Cut handoffs | 02 [9f47b7d4326c] |
| Next-issue avoidance | First replies answer the likely follow-up | Yes | Second tickets common | Add to macros | 02 [9f47b7d4326c] |
| Failure exclusion list | Exists, refreshed weekly | Yes | No | Build (B2) | 02 [76193c44f7e8] |

### 5.6 Gift, surprise and expiry fairness

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Is it swag? | Logo present, or chosen for the brand's benefit | No logo, recipient benefit | Logo | Replace | 02 [0f05cded3cb1] |
| Is the date an occasion? | Holiday, birthday, anniversary | Random date | Occasion | Move | 02 [eb580823eb04] |
| Still a surprise? | Customers expect or ask for it | Unprompted thanks | Expected | Randomize, stop announcing | 03 [e29188eb0294] |
| Preference known? | Zero-party or support note on file | Known | Guessed | Do not send the artifact | 02 [0f05cded3cb1] |
| Inner circle consent | Buyer volunteered the preference | Yes | Inferred | Do not send | 02 [4b114e40b69d] |
| Supply secured | Artists or vendors under agreement | Yes | No | Secure first | 02 [ca8e2e37165b] |
| Expiry fair | Terms disclosed before earning; earn rate meaningful; redemption practical | All 3 | Any missing | Fix terms before adding expiry | 01 [07497417cc0a] |
| Daily loop health | Every day's offer worth a visit | Yes | Filler days | Replan | 01 [67ba6fcee11e] |
| Scarcity real | Fixed stock and time; no evergreen timer | Real | Fake | Remove | 01 [56c8c219238a] |

### 5.7 Legal, consent and platform

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| SMS consent | Consent flag per recipient | All consented | Any missing | Drop them | 01 [07497417cc0a], 03 [f42a03d72af2] |
| Address data source | How obtained, may it be used, GDPR or DPDP | Documented | "Anonymized" third-party | Legal review | 01 [49715f3b64de] |
| Promotion terms | Eligibility, outcome, remedy, expiry in writing | Reviewed | Vague | Review | 01 [49b0963cfe85], 03 [3a74574fff82] |
| Hedge legality | Prediction market access and promo legality in market | Confirmed | Unknown | `[web check]` | 01 [49b0963cfe85] |
| Gambling-style mechanics | Mystery boxes, blind boxes, live auctions | Allowed | Restricted | `[web check]` | 01 [85c5e90b4fff] |
| Venue permits | Guerrilla event permission | Obtained | Ambush | Obtain | 01 [8f0ac696045b] |
| Contest and paid-participation rules | Giveaways, paid internships | Reviewed | Not reviewed | `[web check]` | 02 [147b7a92331e], 03 [f3d618345541] |
| Creator disclosure | Rules per market | Followed | Not | `[web check]` | 01 [4c2cd1cec3bf] |
| Warranty law | Lifetime and outcome terms | Reviewed | Not | `[web check]` | 03 [04f54549fb37] |
| Platform DM and giveaway policy | Instagram DM limits, automation rules | Within | Outside | `[verify UI]` | 02 [147b7a92331e] |
| "Secret" or "exclusive" wording | True or not | True | Not true | Reword | 02 [147b7a92331e] |
| Health-adjacent claims | Platform policy | Compliant | Restricted | Reword | 01 [e4ec9650b8d9] |

### 5.8 Direct mail program

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Vendor in market | Coverage in the brand's country | Yes | EU, UK, US only | `[web check]` | 01 section 9 |
| Identity match | Vendor's match rate on the file | High (case: 80%) | Low | Fix address data; expect limited results | 01 [a9e802c5098a] |
| Response device | QR, unique URL or code on every piece | All | Any missing | Add | 01 [e890000fa7eb] |
| Frequency cap | 1 per customer per 30 days | Enforced | Not | Enforce | 01 [a9e802c5098a] |
| Trigger integration | Same event fires mail and email | Yes | Manual export | Integrate `[verify UI]` | 01 [fcef726cbd6f] |
| Timing sourced | Timing set from the brand's interval, tested | Yes | 48-hour default copied | Test it | 01 [fcef726cbd6f] |
| Format vs values | Paper and print match brand values | Match | Clash | Change stock | 01 [fafb61f67162] |
| 2 controls | Email-only and no-contact | Both | Missing | Add | 01 [70a71f09d8c2] [e890000fa7eb] |
| Loop closed | Scans trigger digital follow-up | Yes | No | Wire it | 01 [3790fdeac0c7] |

### 5.9 VIP, gating and drops

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Top 1% share measured | Revenue share of top 1% and 5% | Measured | Assumed | Measure | 03 [8fc70ea68011] |
| Reward beats friction | Signups or sales before vs after gating | Desire up | Funnel shrinks, no gain | Improve the reward | 03 [11a4bf90d117] |
| Benefits tied to loyalty | Would a leak look unfair? | No | Yes | Re-tie | 03 [8fc70ea68011] |
| Bots and resellers | Buyer overlap, reseller listings | Members first | Resellers win | Waiting room, single-use links | 03 [11a4bf90d117] [f42a03d72af2] |
| Supply | Sell-out speed and fan complaints | Sells out, fans served | Fans shut out | Raise batch | 03 [f42a03d72af2] |
| Cadence | Drop frequency vs repeat visits | Moves together | No link, ops strain | Fewer, better drops | 03 [b7edaaaeed23] |
| Audience built first | Audience size before drop 1 | Built | None | Build first | 01 [56c8c219238a] |
| VIP tier earning | Retention and AOV vs non-VIP | Both higher | Flat | No tier 2; improve reward | 03 [8fc70ea68011] |
| Founder channel staffed | Response time | Answered | Silent | Staff it | 03 [2984f2673be5] |

### 5.10 Guarantees, refunds and warranties

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Keep-it abuse | Claims per customer, fraud signals | Rare, spread | Repeat claimers | Tighten; stop advertising | 03 [1a706b82583a] |
| Keep-it public wording | Search site and macros | None | "Keep it, no return needed" as policy | Remove | 03 [1a706b82583a] |
| Warranty claims | Claims rate and cost by SKU | Low on durable SKUs | Claims "bury you" | Narrow, repair-first | 03 [04f54549fb37] |
| Guarantee refunds | Refund rate before vs after | Barely up | Up, disputes | Make terms specific | 03 [3a74574fff82] |
| Remedy is product-appropriate | Physical product remedy, not "keep working until" | Yes | Services-style promise | Rewrite | 03 [3a74574fff82] |
| Proof test wins | Run against rivals first | Clear, safe, repeatable | Mixed or unsafe | Skip | 03 [574b9d94f465] |
| Price lock scope | Who qualifies, for how long, cost modeled | Narrow, modeled | Broad on thin margin | Narrow | 03 [36d5dbe4d17c] |
| Refund handling effort | Low-effort path for claims | 1 contact | Friction | Fix (B1) | 02 [9f47b7d4326c] |

## 6. Thresholds and benchmarks

Confidence: "high" = 2 or more sources state it independently; "medium" = 1 source plus a card addition or a repeat in 03; "low" = 1 source, opinion or heuristic; "example" = a case result, never a target; "unsourced" = appears without a case or is the compiler's advice.

| Item | Value | Condition | Source | Confidence |
|---|---|---|---|---|
| First touch cohort | Top 50 by lifetime spend (03); top 10 from last quarter (01) | Stage 1, by hand | 03 [24e7dd3a3012] [42d04b3223ba]; 01 [2d99a5dbeda9] | medium (2 sources, different sizes) |
| Expand touch cohort | Top 200 | Only after repeat or 90-day reorder beats control | 03 [24e7dd3a3012] | low (heuristic) |
| VIP tier | Top 1% by lifetime spend | Stage 2 | 03 [8fc70ea68011]; 02 [0f05cded3cb1] [05b6ed77af75] | medium |
| "Top 1% drive most revenue" | Asserted, no data | Measure before building the tier | 03 [8fc70ea68011] | unsourced |
| Handwritten note cost | $1 to $3 plus time | Per note | 03 [42d04b3223ba] | low (estimate) |
| Letter cost | $1 to $5 per piece | Annual letter, handwriting service | 03 [42d04b3223ba] (LettrLabs) | low (vendor) |
| Custom art cost | $20 to $40 per piece | Emotional category | 03 [e29188eb0294] | low (estimate) |
| Insert cost | Cents to a few dollars | First or VIP orders | 03 [9a0245f0095a] | low |
| Founder video | 60 seconds | New VIPs, big orders | 03 [aa796ddf08a2] [2984f2673be5] | low |
| Founder's Ink | Top 1%, once a year, 0 codes | Executive handwritten | 02 [05b6ed77af75] | low (opinion) |
| Rep no-approval budget | $50 to $200 per incident | Scale to margin and AOV | 03 [7ae163d5a82f] | low (scaled from Ritz) |
| Ritz-Carlton rule | $2,000 per incident vs about $250,000 guest LTV (0.8%, derived) | Example, 1983 | 03 [ad5810cd8a68] | example |
| Delight after failure | "Negligible" loyalty gain | Service failures | 02 [9f47b7d4326c] (Dixon, 97,000+ interactions) | medium (1 source, research base) |
| Effort asymmetry | High effort 4x more likely to cause disloyalty than low effort causes loyalty | Service | 02 [9f47b7d4326c] | medium |
| Founder's inbox | 1 month | Low support volume | 01 [2d99a5dbeda9] | low |
| No-ads week | 1 week; 20 lapsed, 10 partners, 5 micro-influencers | Max loss set first (card) | 01 [3043fc9b1846] [2d99a5dbeda9] | low |
| Community before product | 6 months | New product line | 01 [66b5d9fbb538] [2d99a5dbeda9] | low (1 case) |
| Brand build before first drop | 1 year; 20 box designs | Premium drop | 01 [56c8c219238a] | example |
| Drop price | $120 per dozen, weekly | Last Crumb | 01 [f76f1da8af54] | example |
| Fast cadence | 15 to 20 days design to shelf; 200 to 250 styles a month | Needs fast supply chain | 03 [b7edaaaeed23] (Snitch) | example |
| Loyalty coin expiry | 60 days; reminders on 2 channels | Existing program, consent | 01 [07497417cc0a] | low (1 case) |
| Loyalty as acquisition | 12.4% of signups via loyalty | Haus & Kinder | 01 [07497417cc0a] | example |
| "70X ROI" on retention tooling | Undefined | Haus & Kinder | 01 [07497417cc0a] | example, undefined |
| Daily reveal | 12 days, midnight expiry | Seasonal | 01 [67ba6fcee11e] | low (1 case) |
| "82% Return Rate" | Undefined, title only | L'Occitane | 01 [67ba6fcee11e] | unsourced |
| Mystery bundle | 6 bundles, 5 to 8 items, up to 50% off; "at least $X value guaranteed" | Products profitable at discount | 01 [85c5e90b4fff] | example; the trust rule is compiler advice |
| Keep-it threshold | Under $20 | Damaged, perishable, hard to resell; case by case | 03 [1a706b82583a] (goTRG) | low |
| Keep-it adoption | 59% of surveyed retailers in 2023, from 26% | Context | 03 [1a706b82583a] | example `[web check: newer data]` |
| Return processing cost | 20% to 65% of COGS, up to 100% | Context | 03 [1a706b82583a] (UPS) | low |
| Return fraud | About 9% of returns | Reason not to advertise keep-it | 03 [1a706b82583a] (NRF) | low |
| Outcome guarantee lift | About 30% more sales, refunds barely up | Services, book summary | 03 [3a74574fff82] | unsourced for ecommerce |
| Referral pass mark | Referral signups above 30% of total | Stage 3 | 03 [f58ea6021437] [24e7dd3a3012] | low (heuristic) |
| Harry's waitlist | 100,000+ emails in 1 week; 85,000+ legitimate (85%); 77% from referrals; 5 = shave cream, 10 = razor | Example | 03 [f58ea6021437] | example |
| Drop pass mark | Sells through at full price | Stage 3 | 03 [f42a03d72af2] | low |
| Stunt frequency | 1 or 2 a year (text); 1 per season (cards) | After a pass | 03 [f3d618345541] [24e7dd3a3012] | low; internal conflict (7.1) |
| Stunt leverage | $50,000 stunt = reach of a $50 million TV buy | Founder claim | 03 [f3d618345541] | unsourced |
| Patagonia ad | $57,000; 2012 sales up almost a third to $543 million | Secondary | 03 [d2474fde6f0e] | example, mild caution |
| CAH 2013 | Price raised $5; sales spiked | Example | 02 [0874da44648a] | example |
| CAH 2014 | 30,000 boxes at $6 = $180,000 in 2 hours (checks) | Example | 02 [0874da44648a]; 03 [f3d618345541] | example (1 case, 2 sources) |
| CAH 2015 | 11,248 people paid "$5 for nothing"; reported $71,145 (02) or "over $70,000, outlets $50,000 to $70,000+" (03); 11,248 x $5 = $56,240 | Example | 02 [0874da44648a]; 03 [f3d618345541] | example, total unaudited `[web check]` |
| CAH 2016 | $100,573 over 50+ hours, about 3.6 million views in 3 days (03); "over $100,000" (02) | Example | 03 [f3d618345541]; 02 [0874da44648a] | example, consistent |
| CAH 2018 | 99% off real items; 50,000 simultaneous page views | Example | 02 [0874da44648a] | example |
| Wakefit Sleep Internship | 170,000 applications, 30 countries, 0 paid ads; 3 seasons, 1 million+ registrations, 51 interns paid about 63 lakh total; 2023 winner 9 lakh | Example | 03 [f3d618345541] | example, reported |
| Hedge example | $5,000 stake to receive $13,514 (2.70x; about $0.37 per $1 of payout, derived) | Binary outcome promo | 01 [49b0963cfe85] | example |
| Cart abandonment letter timing | About 48 hours | Header "Look for" only; no case | 01 [fcef726cbd6f] | unsourced |
| Browse mail timing | Within days of browsing | Lulu and Georgia | 01 [a9e802c5098a] | example |
| Second-purchase letter timing | 30 to 60 days after first order | Compiler advice | 01 [898e3d534adb] | unsourced |
| Lapsed window | 6 to 12 months | Compiler advice; Fressnapf did not do this | 01 [70a71f09d8c2] | unsourced |
| Mail frequency cap | 1 per customer per 30 days | Abandoned basket cohorts | 01 [a9e802c5098a] (Magazine.co.uk) | low (1 case) |
| Identity match | 80% | Lulu and Georgia with PebblePost | 01 [a9e802c5098a] | example |
| Bergzeit birthday letters | About 7.5% redemption; "strong ROAS" | Vendor case | 01 [fcef726cbd6f] | example |
| Fressnapf | 15,000 customers; "ROI of 6"; conversion doubled vs control | Second purchase, vendor case | 01 [70a71f09d8c2] [898e3d534adb] | example, ROI undefined |
| GOLDNER | 3.4% to 13.6% conversion (4x spread across 7 countries) | Welcome letters, vendor case | 01 [898e3d534adb] | example |
| Lulu and Georgia | 22x iROAS; 78.5% more incremental revenue | Vendor case | 01 [a9e802c5098a] | example |
| thredUP | ROI up 128% | A/B-tested mail, vendor case | 01 [e890000fa7eb] | example |
| Magazine.co.uk | 38.81% higher conversions | Vendor case | 01 [a9e802c5098a] | example |
| DukesHill | 22% more conversions | Vendor case | 01 [3790fdeac0c7] | example |
| Furn | 514 letters; "40% return rate" | Undefined | 01 [a9e802c5098a] | example, undefined |
| Harlow Timber | 88% open rate on the follow-up email, 12,000 contacts | Vendor case | 01 [3790fdeac0c7] | example |
| M&S Corporate Gifts | 3 personas, 100 prospects | ABM, B2B | 01 [f53e738ee3e7] | example |
| Huckberry | Content-engaged LTV 3.5x ad or affiliate customers | Self-selection not controlled | 01 [ce5b3f63afcc] | example, confounded |
| Chewy portraits | About 1,000 a week, hundreds of artists, since 2013 | Enterprise scale | 02 [ca8e2e37165b]; 03 [e29188eb0294] | example (1 case, 2 sources) `[web check: still running]` |
| Paid loyalty | 60% more likely to increase spend; 2x free programs | McKinsey via blog | 02 [ab3039ede71f] | unsourced method `[web check]` |
| Yankee Candle | 90% subscriber retention with custom cadence | Via blog | 02 [c58b965fe70a] | unsourced method `[web check]` |
| Churn window | First 100 days; 8 phases (not listed) | Post-purchase | 02 [7615a4af9401] (Coleman) | low |
| Compounding illustration | 10% a week: 100 to about 14,000 in 1 year (100 x 1.1^52 = 14,204) | Illustration | 02 [f7bb6a108f71] | illustration |
| LEGO Ideas | 10,000 supporters; about 1% royalty | Example | 03 [6fd8b0b7de34] | example `[web check]` |
| HOG | 1 million+ members; members spend 30% more on clothing and events | Brand-reported | 03 [e6ea8581c19b] | example |
| boAt community | 800,000 (2018) to 3 million+ (2020) | Reported | 03 [e6ea8581c19b] | example |
| CRED | Credit score 750+; 13 million+ MAU | Reported | 03 [11a4bf90d117] | example |
| Future Farm | 395 clicks to Sainsbury's; 17,000 likes | Example | 01 [3062c8c8c22a] | example |
| Maxfem | CPA 40% lower than other media; qualified leads up 42%; revenue "exceeded target by 170%" (source text, 2.7x) or "170% of target" (card caveat, 1.7x); card steps say "170% above target" | Ambiguous | 01 [e4ec9650b8d9] | example, ambiguous; quote only as "beat target, figure unclear" `[web check]` |
| GIZMART | ¥100 million GMV in 12 hours; over ¥300 million total | Crowdfunding | 01 [63777fd226ea] | example |
| Miss Amara | $26 million business | Trust-barrier content | 01 [fc9236aec38b] | example |
| Kogan | "$10 billion business" | Measure unclear | 01 [53352d5eca9e] | unsourced `[web check]` |
| Province of Canada | No ads for 5 years; revenue sentence garbled | Do not quote the figure | 01 [3043fc9b1846] | unsourced |
| Liquid Death | $1.4 billion valuation by 2025 | Reported | 03 [f3d618345541] | example `[web check]` |
| Indian D2C birthday-gifting ROI | Named in 03's caveats, never in its body | None | 03 section 9 | unsourced |

Two rows were moved to Appendix A because they are not ecommerce-specific: the Mercado Livre in-game placement case (also moved from O10) and the Zappos 10-hour-43-minute call with its $1.2 billion exit line.

## 7. Where sources disagree

**7.1 Stunts per year vs per season.** Source 03's text: "one or two a year, no more". Cards [24e7dd3a3012] and [f3d618345541] on the same source: "one big stunt or values play per season", which allows up to 4. What the agent should do: plan 1 a year in the quarterly plan; allow a second only if the first passed its earned-media mark; never draft a third without the owner's explicit choice. Record the choice in the registry.

**7.2 Gifts after a service failure or not.** Source 02 (Dixon): delight in a failure state adds negligible loyalty; fix effort instead; wild bets only for neutral or positive states [9f47b7d4326c] [702bc45b5b83]. Source 03 (Ritz-Carlton rule, scaled): "solve the problem, then add a surprise"; reps get a no-approval budget for problems and personal moments [7ae163d5a82f] [ad5810cd8a68]. Source 02 also praises Chewy's flowers and doll for grieving owners while its table puts "life events" under Brand Elevation and says delight is for neutral or positive states; it does not resolve this. When each is right: Dixon's finding is about the failure moment itself; Ritz's rule is about after the fix. What the agent should do: fix first; confirm the fix with the customer; only then allow a small, specific, non-templated gesture inside the rep cap; never a discount or gift as a substitute for the fix; for volunteered hardship, follow K3 (optional, welcomed, no delay). Log gestures after failures separately so the readout can test whether they add anything.

**7.3 Expiring points.** Source 01 uses expiry as the main return trigger (Haus & Kinder, 60 days) and frames it as loss of earned value [07497417cc0a]. Common ecommerce advice (recorded in 01's section 9) treats expiry as a trust risk. Sources 02 and 03 call points programs a commodity to skip or replace with status and non-purchase rewards [ab3039ede71f] [24e7dd3a3012] [6cb0a48f51d6]. When each is right: expiry works where the program already has meaningful earn rates and easy redemption in a repeat category; status plays fit where points are generic. What the agent should do: do not add expiry to a weak program; run 5.6's fairness checks first; test expiry against a no-expiry control with complaints per 1,000 reminders as a stop signal; consider L7's non-purchase rewards as the alternative bet in the same quarter, not the same cohort.

**7.4 Pause vs hard cancel.** Source 02's Proactive Pause suggests a pause to overstocked subscribers before they think of cancelling, and ClassPass-style pause and rollover instead of cancel friction [c58b965fe70a]. Card [dee4592d0973] on the same source says cancellation is the customer's choice and must not be delayed; a pause is offered only as an approved remedy when hardship is volunteered. Common cancel flows use save offers and friction; the source rejects them. What the agent should do: offer pause proactively and early (before cancel intent) as a wallet-protection message; at the cancel moment, complete the cancellation on request with at most an optional reason field and a 1-line pause option that does not block the cancel; never a save-offer wall. Measure resume-after-pause and cancel rate; if the pause option at cancel is used as friction, remove it.

**7.5 Keep-it refund thresholds and whether to advertise.** Source 03: keep-it under $20, case by case, not advertised because about 9% of returns are fraudulent [1a706b82583a]. The same source cites O Positiv, which advertises a 30-day money-back with no return required and credits it for scaling, and Chewy's "keep or donate" at bereavement; it does not reconcile these. Source 01 has no keep-it play. When each is right: case-by-case protects margin on hard-to-resell items; an advertised guarantee is a conversion offer with a modeled refund rate (J5) and belongs with the outcome guarantee, not the returns pilot. What the agent should do: run P5 unadvertised at the under-$20 threshold with fraud caps; if the owner wants an advertised no-return guarantee, treat it as a separate P15 bet with refund-rate tracking and a PDP A/B split; never raise the threshold without a control read.

**7.6 Judging by engaged-customer LTV vs ROAS.** Source 01: Huckberry's 3.5x LTV of content-engaged customers "is a better metric than ROAS"; measure word of mouth, engaged LTV, referral rate, retention lift [a7b8a9aa106c] [ce5b3f63afcc]. Source 02: return shows up in LTV, repurchase, NPS, earned media, referrals, not short-window attribution [aebda9584fe6] [89bcc55e9cc4]. Source 03: budget stunts as marketing cost and judge on earned media [f3d618345541]. Performance-marketing practice (24-DEP, 06-MEA) judges on ROAS and incrementality; the proposed metrics are weaker on causality, and the Huckberry figure is confounded by self-selection. Cards on 01 and 02 add: incremental contribution after all costs is the decision line; attention is a signal; "not a licence to never measure". What the agent should do: never read a wild bet on ROAS alone and never on engaged LTV alone; the readout carries incremental contribution after costs vs a control as the decision line, relationship metrics at the repurchase interval, and attention on a separate line; control for prior spend before claiming an LTV gap; if no control exists, file as an observation.

**7.7 Hedge as funding.** Source 01's text calls Forme's risk "capped and hedged" and presents the prediction market as "a safety net". Card [49b0963cfe85] says do not count an unverified hedge as funding, and review settlement and timing gaps. What the agent should do: fund maximum liability in cash; treat the hedge as optional upside; record stake, payout and settlement date; check legality per market.

**7.8 Random timing vs annual and occasion letters; code vs no code.** Source 02: gifts on a random date, never holidays, birthdays or anniversaries [eb580823eb04]; yet its Founder's Ink is annual [05b6ed77af75] and its 100-day onboarding is a planned sequence [7615a4af9401]. Source 01's Bergzeit case is a birthday letter with about 7.5% redemption (vendor case) [fcef726cbd6f]. Source 03's annual or anniversary letter carries a private offer code to measure response [42d04b3223ba]; source 02's Founder's Ink bans codes. When each is right: random timing is for surprise gifts (reciprocity); the annual letter is a gratitude ritual; birthday mail is a triggered lifecycle touch measured on redemption. What the agent should do: keep surprise gifts random; keep the annual letter annual but off holidays; if the owner wants response measurement on the letter, use a tear-off referral insert or a private code and say the letter is then a measured touch, not pure gratitude; run birthday mail as a P6 trigger with its own control; do not mix the 3 on 1 cohort in 1 quarter.

**7.9 Anti-discount stance vs discount-based mechanics in the same folder.** Source 03 says replace sales with gifts, bundles or price holds and skip 10% off and BOGO [7c689b80e439] [d2474fde6f0e]; source 02 bans the instant 10% pop-up and codes in Founder's Ink, yet its consolation offer and question-first pop-up end in a discount [daa23b9732b1] [147b7a92331e]; source 01 runs mystery bundles up to 50% off, loyalty flash sales, daily deals and delayed discounts [85c5e90b4fff] [184e447721a2] [67ba6fcee11e] [a03a3ab4e941]. Card on 03 adds that commodity categories may need promotional pricing. When each is right: the anti-discount stance is about brand-wide, public, repeated price cuts; the 01 mechanics are targeted, time-boxed and segment-only. What the agent should do: no public blanket discounts as a wild bet; targeted time-boxed mechanics only to loyalty segments with leak checks; record the brand's positioning (premium or commodity) in the brief; discount design goes to 03-OFF.

**7.10 First-time buyers: costly touches to repeat buyers only, or touches on the first order.** Card on 03: skip first-time buyers with no shown affinity for handwritten mail [42d04b3223ba]. Source 01's programmatic mail fires on welcome, cart abandonment and browse, before any repeat [fcef726cbd6f] [a9e802c5098a]; source 02's 100-day onboarding and source 03's first-order inserts target new customers [7615a4af9401] [9a0245f0095a]. When each is right: hand-written, expensive touches go to proven buyers; cheap or automated touches can go to new buyers with their own control. What the agent should do: cost per touch decides: above the insert range (cents to a few dollars), the recipient must be a repeat buyer; automated mail and inserts may target new customers under P6 or P16 with a control.

**7.11 Cohort size: top 10, top 50 or top 1%.** Source 01: top 10 (gift, insider event) [2d99a5dbeda9] [5eeef0648aad]; source 03: top 50, then 200, then 1% [24e7dd3a3012]; source 02: top 1% [0f05cded3cb1]. What the agent should do: the smallest that the team can serve by hand and that gives enough events to read (5.3); widen on a passed gate; treat top 1% as a tier, not a pilot size.

**7.12 Manual vs automation.** Source 01 pairs "doesn't scale" human touch with the "AI Gothpreneur" model of automating personalized outreach [68c4bfa88afe] [7ccc9fc1a3f2]; source 03 says graduate a play to a system when it outgrows manual effort without saying when [aa796ddf08a2]; source 02's card says once reorders and referrals repeat [f7bb6a108f71]. What the agent should do: automate the rule-based work (triggers, logging, reminders); keep the note, the call, the referral ask and the over-delivery human; propose graduation only after 2 passed reads.

**7.13 "Limited downside, unlimited upside" vs "most wild bets will fail".** Both in source 01 [a7b8a9aa106c], with no sizing method. What the agent should do: the quarterly plan holds 3 bets under 1 cash cap, each sized so that all 3 failing is affordable; no single bet takes more than half the cap (playbook addition, the owner can change it).

**7.14 Fast drop cadence vs scarce drops.** Source 03 records Snitch's 200 to 250 styles a month as a habit loop [b7edaaaeed23] and MSCHF's scarce numbered drops [f42a03d72af2]; source 01 records weekly Last Crumb drops with fixed inventory and does not address fatigue [56c8c219238a]. What the agent should do: pick 1 model per brand; keep a cadence only while frequency tracks repeat visits; a fast cadence needs the supply chain first.

**7.15 Stage 1 benchmark confounded.** Source 03's Stage 1 runs notes and keep-it under 1 benchmark [24e7dd3a3012]. What the agent should do: split into 1a and 1b with separate controls (C3, P3).

**7.16 Loyalty as acquisition vs loyalty as commodity.** Source 01: 12.4% of signups came through the loyalty system, so loyalty acquires [07497417cc0a]. Sources 02 and 03: points programs are table stakes [ab3039ede71f] [24e7dd3a3012]. What the agent should do: measure share of signups through loyalty before deciding; if it is material, treat the program as a surface for expiring value or status rewards; if not, do not build a wild bet on it.

**7.17 No-ads week vs paid delivery.** Source 01 presents the no-ads week with no warning; the card adds campaign disruption on established paid channels [3043fc9b1846]. What the agent should do: set the loss cap; consult 24-DEP; avoid peak weeks; record recovery time as a cost of the read.

## 8. Common mistakes

Merged from all 3 sources, deduplicated, with the fix.

- Calling a standard tactic a wild bet (10% off, BOGO, points, abandoned-cart email). Fix: name the norm broken or send it to 03-OFF or 14-EML. [24e7dd3a3012]
- Running a delight play on a high-effort base, or on a customer with an unresolved failure. Fix: Stage 0 audit; weekly exclusion list. [76193c44f7e8] [9f47b7d4326c]
- Trying to "delight" after a failure with a gift or discount instead of the easiest fix. Fix: fix first, gesture only after the fix is confirmed (7.2). [9f47b7d4326c]
- Making customers explain the issue across transfers. Fix: first-contact resolution, next-issue avoidance. [9f47b7d4326c]
- Launching with no bound: no cap, no control, no stop rule, no review date. Fix: P1. [a7b8a9aa106c] [24e7dd3a3012]
- Judging a wild bet on same-week ROAS, or never measuring because "it's about brand". Fix: 2-line readout (D2, D3). [a7b8a9aa106c] [89bcc55e9cc4]
- Treating a single viral result as repeatable, or a case number as a benchmark. Fix: D1, C8. [a7b8a9aa106c] [0874da44648a]
- Comparing engaged vs non-engaged customers without controlling for prior spend. Fix: D4. [ce5b3f63afcc]
- Counting an unverified hedge or an earned-media estimate as funding or revenue. Fix: C5. [49b0963cfe85] [89bcc55e9cc4]
- Uncapped refund liability on a public promise. Fix: P17. [49b0963cfe85]
- Fake scarcity: evergreen countdown timers, restock promises. Fix: M3. [56c8c219238a] [67ba6fcee11e]
- A drop with no audience built first. Fix: M4. [56c8c219238a]
- Supply so low it shuts out fans, or no gating so resellers win. Fix: M5, M6. [f42a03d72af2]
- A fast drop cadence without the supply chain. Fix: M7. [b7edaaaeed23]
- Expiry that feels manipulative: hidden terms, low earn rate, hard redemption. Fix: 5.6. [07497417cc0a]
- Filler days in a daily reveal; daily urgency all year. Fix: L3. [67ba6fcee11e]
- Blanket discounts and instant 10% pop-ups. Fix: O6, R1. [184e447721a2] [daa23b9732b1]
- Mystery bundles with no stated minimum value or on unprofitable products. Fix: L8. [85c5e90b4fff]
- Sending logo swag and calling it a gift. Fix: H1. [0f05cded3cb1]
- Gifts on holidays, birthdays or anniversaries when the play is a surprise. Fix: H2. [eb580823eb04]
- Announcing the surprise or making it a standard perk. Fix: H3. [e29188eb0294]
- Emotional art in a functional category. Fix: E3. [63f18883754c]
- Printed notes made to look handwritten. Fix: F4. [42d04b3223ba] [9a0245f0095a]
- Costly mail to the whole list. Fix: F5. [42d04b3223ba]
- Generic filler inserts. Fix: H10. [9a0245f0095a]
- One-off heroics with no standing policy. Fix: I5, A7. [7ae163d5a82f]
- An unguarded discretionary budget. Fix: I3. [22e369c1edc4]
- Inferring grief or family ties from data. Fix: K3, H7. [dee4592d0973] [4b114e40b69d]
- Delaying a cancellation with save offers. Fix: K3, 7.4. [dee4592d0973] [c58b965fe70a]
- Cross-sell or review asks inside the first 100 days. Fix: K5. [7615a4af9401]
- Lifetime guarantees on products that do not last; vague outcome guarantees; broad price locks on thin margins. Fix: J4, J5, J7. [04f54549fb37] [3a74574fff82] [36d5dbe4d17c]
- Advertising keep-it as the default policy. Fix: J1. [1a706b82583a]
- Proof-in-the-box when the product does not win, or with an unsafe test. Fix: J8. [574b9d94f465]
- Cash referral rewards. Fix: N1. [f58ea6021437]
- Gating without a reward worth the friction; VIP benefits that look arbitrary. Fix: M2. [11a4bf90d117] [8fc70ea68011]
- Co-creation with too few voters or promising designs will ship. Fix: N3. [6fd8b0b7de34]
- Forced community lingo; a community with no real investment; social as a broadcast channel. Fix: N2. [e6ea8581c19b] [b5a1ffc627e1]
- Copying a stunt format without the voice; more than 1 or 2 stunts a year; judging a stunt on direct sales. Fix: O1, O4, O3. [f3d618345541]
- Cultural or political alignment without authentic fit; faked values. Fix: A8. [4dc56ea887bf] [d2474fde6f0e]
- Absurdist or mystery stunts whose payoff is not worth the curiosity; distribution not ready at the reveal. Fix: O9. [d1f0d1622744] [3062c8c8c22a]
- Over-scripting creators; ignoring disclosure rules. Fix: N7. [4c2cd1cec3bf]
- Mail with no response device, no frequency cap, no control, or a format that contradicts brand values. Fix: G4, G5, G6, G8. [e890000fa7eb] [a9e802c5098a] [fafb61f67162]
- Third-party address data without knowing how it was obtained. Fix: G9. [49715f3b64de]
- SMS reminders or drop alerts without consent. Fix: C7. [07497417cc0a] [f42a03d72af2]
- Calling a code "secret" or "exclusive" when it is not; leaked consolation codes. Fix: R2. [147b7a92331e]
- Guerrilla without permits. Fix: O8. [8f0ac696045b]
- A no-ads week with no loss cap and no word to the paid team. Fix: Q1. [3043fc9b1846]
- Automating the human moments. Fix: A9. [7ccc9fc1a3f2]
- Dismissing manual outreach because the numbers look small. Fix: A10. [f7bb6a108f71]
- Running bets as one-off stunts without documenting. Fix: A7, P22. [a7b8a9aa106c]

## 9. Deliverables

All deliverables are drafts for a human to approve. None is sent, shipped, refunded or launched by the agent. Writing rules: short sentences, simple words, digits, no em dashes, no inflated words, no invented claims. Client-facing pages do not mention models or environment files.

### 9.1 Quarterly wild bets plan: 3 bounded bets with costed tests

Format: 1 page per bet plus a 1-page cover.

Cover:
- Brand. Quarter. Stage the brand is at (0 to 4) and the last passed gate.
- Faucet read: organic vs paid revenue share, last 12 months (A2). `[needs brand data]`
- Base-effort status: CES, FCR, resolution time baseline and whether the owner accepted it (P2).
- Shared cash cap for the quarter and labor hours; no single bet above half the cap (7.13).
- The 3 bets, 1 line each: play, cohort, cap, metric, review date.
- Why these 3: the norm each breaks, the stage each belongs to, and why not the runners-up.

Per bet (the bet brief):
1. Play name, stage, L1 statement.
2. Norm broken and borrowed model (A1, A5).
3. Fit: voice, values program, emotional hook, margin room (5.1).
4. The 8-field bound (P1): hypothesis, cohort with exclusions, budget cap (cash line by line: pieces x cost, fees, gifts, refund exposure; labor hours), metric (decision line and signal line), control (type and draw method), duration and review date, stop rule, registry id.
5. Costed test: a table of cost lines with the source of each cost (vendor quote, source 03 range, brand data) and the total against the cap.
6. Expected effect: the source case, labeled "reported, unaudited", next to the human's minimum lift.
7. Legal, consent and platform items with owner and status (5.7).
8. Customer-facing wording drafts (note, email, terms, claims page, SMS).
9. Rollback and what happens to promises already made.
10. Rules and card ids used.

Default first-quarter set when the brand is at Stage 0 or 1 (source 03's plan, split per C3): P4 note or founder video to the top 50; P5 keep-it refunds under $20; P16 surprise insert on VIP or first orders. Default second quarter after a pass: P9 VIP tier; P6 1 mail trigger; P13 1 loyalty mechanic. Third: P12 referral waitlist; P10 drop; P14 proactive pause. Fourth: P18 the 1 big swing. The owner reorders as needed.

### 9.2 Approval request (per bet)

Half a page. Play, cohort size, cash and labor cap, control, review date, stop rule, a link to the matching On-site and lifecycle copy pack (9.7) rather than the wording drafted inline, the exclusion list attached, legal items and status, what the human must do to execute (send, ship, switch on, pause paid), and the line "L1: nothing is executed by the agent".

### 9.3 Readout memo (per bet, at the review date)

1 page. What ran (play, cohort, dates, spend vs cap, hours vs cap). Comparison type (randomized, matched, baseline). Decision line: incremental contribution after all program costs, treated vs control, computed in code (attach the sheet or script). Relationship metrics at the repurchase interval. Signal line: earned media, UGC, referrals, mentions, kept separate. Stop rule status. Abuse or complaint signals. Decision: double down, keep, change 1 variable, kill, with reason. What changes next time. Card ids.

### 9.4 Registry entry (per bet)

The P22 fields, as a block the brand record can hold and the future experiment registry can import. ecomOS has no registry yet; keep the block in the quarterly plan and the brand record.

### 9.5 Play catalogue card (on request)

For any play in section 4: conditions, cost (source range or `[needs brand data]`), cohort, expected effect with source label, bound template, legal items, stage. Used when the owner asks "what would X look like for us".

### 9.6 Stage 0 audit report

The 5.5 table filled with brand numbers, the 3 walked paths with findings, the fix list for 17-CXP, and the exclusion list definition.

### 9.7 On-site and lifecycle copy pack (per bet, where customer-facing wording is used)

All customer-facing wording for the bet in one place: the note or founder-video script, emails, SMS, terms, and any claims-page copy. Written to the playbook's writing rules (short sentences, digits, no invented claims, no "secret" or "exclusive" unless true). Attached to the approval request (9.2) rather than drafted inside it.

### 9.8 Packing and fulfillment instruction sheet (per bet that adds a physical item to an order)

For any play that adds a gift, insert, welcome kit or artifact to an order (H, P7, P16 and similar): the item, the trigger that adds it, the cohort and exclusion list, and packing or shipping instructions, so the ops or packing team can run it without reading the full bet brief.

## 10. What needs live data or a web check

### 10.1 `[needs brand data]`

Cohorts and revenue concentration
- Customer list ranked by lifetime spend and order count; first and last order dates (E1, P4, P9, P11).
- Revenue share of top 1%, top 5%, top 50, top 200 (E1; the top-1% claim is asserted, not shown).
- Repeat-purchase rate and 90-day reorder rate by cohort, with history (P3 pass marks).
- Repurchase interval (G7, review dates).
- Baseline conversion and repeat rate for the chosen segment (C1, 5.3 sizing).

Margin and cost
- AOV, gross margin by SKU, category and bundle (B8, I1, J1, K4).
- Cash available and the quarterly cap; labor hours (C1).
- Vendor quotes: handwriting service, mail vendor cost per piece, artists, waiting room tool, waitlist tool (P1, P6, P7, P10, P12).
- Cost trend per unit for price locks (J7).
- Channel fees and margin for micro-channel bets (D6, S2).

Support and effort
- CES, first-contact resolution, resolution time, transfers per ticket, contacts per order, repeat contacts (B3, P2).
- Customers with a failure open or closed in the last 7 days (B2).
- Support transcripts or zero-party fields with life events and stated preferences (H1, I2).
- Customer LTV for sizing the rep budget (I1).

Returns and guarantees
- Cost per return (shipping plus handling), resale recovery rate, return reasons by SKU, returns per customer (J1, J2, P5).
- Defect and failure rates by SKU (J4, P15).
- Refund rate before a guarantee (J5, P15).

Subscriptions and loyalty
- Consumption rate per SKU, order cadence, skip and pause history, cancel reasons (K2, P14).
- Earn rate, burn rate, points liability, share of signups through loyalty (L1, L2, P13).
- Retention and AOV by tier (M1, P9).
- Visit and purchase frequency by drop week (M7, P10).
- SMS list size and consent status; email consent (M5, P13).

Measurement
- Organic vs paid revenue share by week, last 12 months (A2, P20).
- Customer-level engagement joined to order history (N6, D4).
- Repeat rate of gift recipients vs non-recipients (H4, P7).
- A method to value coverage and shares against spend, approved by the owner (D3, P18).
- Order volume forecast in an event window, AOV, margin (P1, P17).
- Matched or randomized control lists per play (C2, 5.3).

### 10.2 `[web check]`

Law, consent and platform policy
- Consumer protection, contest, promotion and paid-participation rules in the selling market (C7, O5, P18).
- Warranty and guarantee rules in the selling market (J4, P15).
- SMS consent rules; GDPR; India DPDP rules on address data and third-party targeting (G9, C7).
- Whether outcome-linked promotions are legal in the brand's country; Kalshi and Polymarket access and contract terms (P1, P17).
- Rules on mystery boxes, blind boxes and live auctions on the platform and in the market (L8).
- Creator disclosure rules (N7).
- Platform giveaway and DM policy; Instagram DM limits (R2).
- Health-adjacent claim policies on social platforms (O11).

Vendors and tools
- PDM vendors and identity-match coverage in the brand's country; India options (G11, P6).
- Availability and privacy terms of spend-data partners (Experian Spend Insight) per country (G9).
- LettrLabs and similar handwriting services: current pricing (F4).
- Queue-it or store-platform waiting rooms and single-use links (M5).
- Recharge or the brand's subscription tool: pause, skip, rollover, usage signals (K1, K2).
- Loyalty app: expiry and reminder triggers (L1).
- TikTok Shop cross-border and "Earn Abroad"; eBay Live; Instagram, TikTok, YouTube live shopping per country (M10, S4).

Cited programs and figures
- Chewy portrait program and current bereavement practice (H3, H5).
- Osprey All Mighty Guarantee and Darn Tough terms (J4).
- BarkBox price lock (J7).
- LEGO Ideas thresholds and royalty (N3).
- goTRG and NRF returns data, newer editions (J1).
- McKinsey paid-loyalty study; Yankee Candle retention figure (L6, K1).
- Cards Against Humanity 2015 totals (P18, section 6).
- Maxfem revenue figure (O11, section 6).
- Kogan $10 billion figure (S3).
- Liquid Death valuation; CRED MAU (section 6).
- Mokobara, BlinkIt and IndiGo partnerships (S2).

## 11. Freshness and stale-risk notes

All 3 sources are compilations of second-hand cases dated 2013 to 2026 and were last modified 20 Sep 2026. Nothing in them was tested by the author. Re-verify on the schedule below.

| Area | What can go stale | Rules affected | Re-verify |
|---|---|---|---|
| Direct mail vendors | Vendor names, country coverage, identity-match methods, cost per piece, ESP integrations (optilyz, PebblePost, Paperplanes, Lob, Dotdigital, ZAP~POST, Webmart, LettrLabs) | G1, G11, F4, P6 | Before each mail bet; quotes older than 90 days are stale |
| Loyalty app features | Expiry triggers, multi-channel reminders, tiering by spend with engagement movement, non-purchase rewards | L1, L7, M1, P13 | Before each loyalty bet `[verify UI]` |
| Subscription tools | Pause, skip, rollover, usage or stock-on-hand signals (Recharge named) | K1, K2, P14 | Before each subscription bet `[verify UI]` |
| Consent and privacy law | SMS consent rules, GDPR, India DPDP, third-party address and spend data, DM automation policy | C7, G9, L1, M5, R2 | Every quarter, and before any send to a new market |
| Consumer, contest and warranty law | Guarantees, lifetime warranties, price-lock promises, paid internships, giveaways | J4, J5, J7, O5, P15, P18 | Before each promise goes public |
| Prediction markets | Kalshi and Polymarket availability, contract terms, legality of outcome-linked promos | P1, P17 | Before each hedged promo; can change by country within months |
| Platform commerce features | TikTok Shop cross-border and "Earn Abroad", eBay Live, live shopping on Instagram, TikTok, YouTube, waiting rooms | M5, M10, S4 | Before use `[verify UI]` |
| Cited program terms | Chewy portraits and bereavement, Osprey and Darn Tough, BarkBox lock, LEGO Ideas, O Positiv guarantee | H3, J1, J4, J7, N3 | When quoted in a brief |
| Returns and fraud data | goTRG adoption, NRF fraud share, UPS processing cost | J1, J2 | Yearly |
| Case figures | Liquid Death valuation, CRED MAU, boAt community, Snitch and Country Delight revenue, Wakefit seasons | section 6 | When quoted; never as targets |
| Source 03's routing | It says paid media goes to 06-MEA; in ecomOS paid media is 24-DEP and measurement is 06-MEA | section 1 | Fixed here; do not copy the source's routing |
| Cost ranges | $1 to $3 notes, $1 to $5 letters, $20 to $40 art, $50 to $200 rep budget are 2025 to 2026 estimates in USD | F1, F3, H4, I1, section 6 | Convert and re-quote per brand and currency before each plan |

**Changelog.** 24 Sep 2026: ecommerce specificity pass applied from ECOM_REVIEW.md; priority block added, 15 rules reworded, 8 levers added, about 270 words moved to Appendix A.

## 12. Source index

**01. Wild bets (The Wild Bets Playbook: A Curated Research Document for E-commerce Founders, Global Edition).** source_id 15PcVPV3ufX8eVaTyXqlfry-_jTfPXTX3. Type: curated research digest, 11,679 words, 47 cards. Credibility: no named author; 55 short case entries retold from trade press, platform case pages and LinkedIn posts; 15 of 55 entries are direct mail and most of those come from vendor case studies (optilyz, PebblePost, Paperplanes, Lob, Dotdigital, Experian, Webmart), which publish their best results and define none of their metrics. No sample sizes, durations, costs or margins anywhere. Internal errors: Fressnapf filed under reactivation with second-purchase numbers; the 48-hour cart trigger appears only in the header; Maxfem's "170%" is ambiguous; Province of Canada's revenue line is garbled. Bias: vendor marketing, survivorship, and platform-scale cases (Mercado Livre, Lazada, Snap) that do not transfer to a small store. Contributed most: the 7-step bet design method, the faucet test, the 5 "doesn't scale" tests, the whole programmatic direct mail group, scarcity and expiring-value mechanics, the hedged promotion rules (via card 49b0), and the measurement stance (engaged LTV over ROAS, with the card's incremental-contribution correction).

**02. Unconventional E-Commerce Offer Strategies ("Strategic Unorthodoxy").** source_id 1jFVSQYe63LLx_GVXKRlbIwOUiJo-DZgN. Type: AI-style deep-research report, 6,091 words, 24 cards, numbered footnotes and about 60 works cited. Credibility: no named author; the title says "offer strategies" but the content is retention, gifting, hospitality and anti-marketing; evidence is book summaries (Giftology, The Effortless Experience, Never Lose a Customer Again), marketing blogs and YouTube breakdowns; the only research-grade claim is Dixon's 97,000-interaction effort study, quoted through summaries; McKinsey 60% and Yankee Candle 90% come through blogs with no method; CAH figures do not reconcile (11,248 x $5 vs $71,145). Bias: the report form makes second-hand claims read like findings; several cards were rewritten to be safer than the text (household gifts, bereavement, consolation offers, bundles) and those card versions are the rules here. Contributed most: the fix-effort-first sequence and the Operational Support vs Brand Elevation split, artifact-not-swag and random timing, the frontline "one size fits one" budget, proactive pause and no-delay cancellation, the 100-day window, the tactic-to-driver matrix, and the earned-attention-separate measurement rule.

**03. Wild bets folder: unconventional offer, retention and CX plays for e-commerce owners.** source_id 1qPsN1CMW45CVBBtXu__6Jllbm_heZV_e. Type: research compilation written as the folder brief, 4,643 words, 25 cards. Credibility: no named author, likely a research assistant writing for the library owner; sells nothing; evidence is news, trade press, brand-friendly blogs, vendor pages (Queue-it, LettrLabs, Antavo, Growave) and Wikipedia; the anti-discount stance cites Ritson, Binet and Field and Ehrenberg-Bass via a blog and Kantar; the source itself flags CRED, boAt and an Indian birthday-gifting claim as reported, not audited; case outcomes (Patagonia sales, Zappos exit, Liquid Death valuation) are correlations. Bias: it is a summary of this folder and repeats cases from 01 and 02 (Paul Graham, Chewy, Eleven Madison Park, CAH, Liquid Death), so overlaps count once; its benchmarks (top 50, top 200, 30% referral share, "beats control") are heuristics; its cards add rigor the text lacks. Internal conflict: 1 or 2 stunts a year (text) vs 1 per season (cards). Contributed most: the 4-stage rollout with pass marks, the only cost ranges in the folder, keep-it refunds, lifetime warranties, outcome guarantees, price locks, the rep budget figure, VIP tier and gating, referral waitlist, drops with gating, community rituals, co-creation, proof in the box, and the stunt frequency rule.

**Neighbour folders.**
- 03-OFF-offers: discount design, bundles as offer architecture, guarantees as offer components, pop-up incentives.
- 14-EML-email-lifecycle: the email and SMS flows that the physical touches here fire alongside; reminder cadence.
- 17-CXP-post-purchase: returns process, support tooling and macros, standard post-purchase sequences; receives the Stage 0 fix list.
- 24-DEP-ad-deployment and 06-MEA-measurement: paid media, ROAS, incrementality tests, the no-ads week baseline and recovery read.
- 10-MCR-paid-social-creative: creative production for any stunt or reveal.
- 09-CRO-testing and 07-LPG-landing-pages: PDP and pop-up A/B setups used by the guarantee and question-first plays.
- 13-ORG-organic-and-content: content programs behind the newsletter and content-as-store plays.
- 01-PRD-product-research and 22-AMZ-amazon-marketplace: product bets and marketplace or cross-border expansion recorded in group S.
- 15-SEO-search and 16-AEO-answer-and-generative-engines: out of scope per all 3 source headers.

## Appendix A. General background

Content moved here from the main body because it is not ecommerce-specific or not a DTC store result (ECOM_REVIEW.md, section 5, 24 Sep 2026). Moved, not deleted, so card ids and rule ids stay traceable. None of this is a ranked (3.0) or applied decision rule.

### A.1 H8: Eleven Madison Park's $2 hot dog (moved from Group H)

**H8. "One size fits one": the value is being heard, not the gift's price.** Eleven Madison Park's $2 street hot dog, plated by the chef, moved guests more than the tasting menu. A fine-dining anecdote, not an ecommerce result. Sources: 02 [22e369c1edc4]; 03 [ad5810cd8a68] (same case).

### A.2 H7's B2B case (moved from Group H, rule H7)

The source's evidence for H7 is 1 B2B relationship case (Ruhlin and a Brooks Brothers showroom in a hotel room). [4b114e40b69d]

### A.3 G13: B2B, wholesale and corporate gifting ABM (moved from Group G)

**G13. B2B, wholesale and corporate gifting: a small persona set and a short high-value list inside a multi-touch ABM sequence.** M&S Corporate Gifts: 3 personas, 100 prospects, HubSpot, personalized mail as 1 touch; "sales skyrocketing", no number. Sources: 01 [f53e738ee3e7]. `[verify UI: ABM sequencing in the CRM]`

### A.4 M2's CRED example (moved from Group M, rule M2)

CRED (credit score 750+, 13 million+ monthly actives, reported) was the source's other gating case, alongside Harry's. [11a4bf90d117]

### A.5 A10: compounding growth-math illustration (moved from Group A, rule A10)

Source 02: grow a truly loyal base 10% a week and 100 become about 14,000 in 1 year and about 2 million in 2 years (100 x 1.1^52 = 14,204; 100 x 1.1^104 = 2,017,619; the arithmetic checks). [f7bb6a108f71]

### A.6 O10: Mercado Livre in-game native placement (moved from Group O and section 6)

**O10. Native placements that hand out real value beat interruptions, but platform-scale budgets do not transfer to a small store.** Mercado Livre "Call of Discounts": 420+ products hidden in Call of Duty maps, over R$7 million in sales, 5.2 million views (agency case, Cannes Grand Prix). Sources: 01 [8f2e2350741b].

Section 6 benchmark row: Mercado Livre Call of Discounts, 420+ products, over R$7 million sales, 5.2 million views, platform scale, example, not transferable. [8f2e2350741b]

### A.7 Zappos call and exit figure (moved from section 6)

Zappos: 10 hour 43 minute call (June 2016); 365-day returns; $1.2 billion exit. Example, correlation, general startup lore, not a store metric. Sources: 03 [aa796ddf08a2].
