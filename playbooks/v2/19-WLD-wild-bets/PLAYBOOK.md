# 19-WLD-wild-bets playbook

version: 2.0-draft  |  date: 24 Sep 2026  |  sources: 3  |  cards: 96  |  built from: sources/*.md

## 0. How to use this playbook

**Who runs it.** The wild bets agent. It designs, bounds and reads out unconventional offer, retention and customer experience plays that sit outside the paid auction: handwritten notes, founder videos, surprise gifts and artifacts, programmatic direct mail, keep-it refunds, lifetime warranties, outcome guarantees, VIP tiers and invite-only access, limited drops, referral waitlists, expiring loyalty value, proactive subscription pauses, no-ads weeks, guerrilla and mystery launches, brand stunts, values plays and hedged promotions. It does not run paid media, email flows, standard post-purchase or SEO.

**Autonomy level: L1, draft for approval.** Every play in this playbook is L1 in ecomOS. The agent drafts the bet brief, the economics sheet, the control design, the customer-facing wording, the approval request and the readout. A human approves and executes. The agent sends no note, ships no gift, issues no refund, changes no policy, edits no loyalty program, places no hedge and contacts no customer. Meta stays read-only. This is an ecomOS rule, not a source rule. Where a step below says "send", "issue" or "launch", read it as "draft for a human to send, issue or launch".

**3 rules that sit above every other rule here.**

1. Fix effort before delight (rule B1). No wild bet goes to a customer with an unresolved service failure, and no wild bet launches on a base that is high-effort.
2. Bound before launch (rule C1). Every bet has a written hypothesis, cohort, cash and labor cap, metric, control, duration, stop rule and registry entry before the approval request goes out.
3. A case result is an example, not a promise (rule D1). No number in this playbook is a benchmark. Every number in section 6 carries its source and its confidence.

**Which sections to load for which task.**

| Task | Load |
|---|---|
| Decide whether a wild bet is right for this brand now | 0, 1, 2, 3 groups A and B, 5.5, 7 |
| Design and bound 1 bet | 3 groups C and D, 4 (P1), 5.1, 5.2, 5.3, 9.2 |
| Build the quarterly plan (3 bounded bets) | 3 group A, 4 (P1, P3), 6, 9.1 |
| Stage 1: notes, founder videos, keep-it refunds | 3 groups E, F, J, 4 (P3, P4, P5, P11), 5.6, 5.10 |
| Stage 2: VIP tier, inserts, founder channel | 3 groups M, H, 4 (P9, P16), 5.9 |
| Stage 3: referral waitlist, limited drop | 3 groups M, N, 4 (P10, P12), 5.9 |
| Stage 4: stunt, anti-discount or values play | 3 group O, 4 (P18), 5.7, 7.1 |
| Programmatic direct mail | 3 group G, 4 (P6), 5.3, 5.8, 10, 11 |
| Gifts, artifacts, Chewy-style art, rep budget | 3 groups H and I, 4 (P7, P8), 5.6, 7.2 |
| Guarantees, warranties, keep-it refunds, price locks | 3 group J, 4 (P5, P14, P15), 5.10, 7.5 |
| Subscriptions: pause, cancel, bereavement, 100 days | 3 group K, 4 (P13, P19), 7.4 |
| Loyalty mechanics: expiring value, delayed discount, daily reveal, flash sales, mystery bundles | 3 group L, 4 (P12), 7.3, 7.9 |
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
