# Ecommerce specificity review: 17-CXP post-purchase

Reviewed: `PLAYBOOK.md` (1,463 lines, about 26,300 words) against `TEMPLATE.md` and the sources in `sources/`.

## 1. Ecommerce specificity score: 4 out of 5

The core of this playbook (retention economics, cohort formulas, WISMO, delivery estimate accuracy, returns and refunds, unboxing, replenishment, loyalty and win-back) is built from ecommerce numbers and store mechanics no generic prompt would produce, and every rule becomes a runnable procedure with brand-data and web-check tags. It loses a point because section 3.21 (CX strategy, ownership, maturity and voice of customer, 10 rules from source 02) is general corporate CX consulting content with almost no store mechanics, and a scatter of other rules (service recovery theory, brand-voice-for-AI, community, buy-vs-build governance) state the general principle first and the store application second or not at all. None of this is wrong, but it is not the store-specific edge the rest of the document has.

Counts for section 3 (150 rules, R1 to R150, plus 8 ecomOS override rules E1 to E8; the 25 formulas in 3.0 are definitions, not counted, and all 25 are store-specific):

| Category | Count | Share |
|---|---|---|
| (a) store-specific | 134 | 85% |
| (b) generic but correctly applied to a store | 11 | 7% |
| (c) generic with no store framing | 12 | 8% |
| (d) out of scope for a store | 1 | under 1% |
| Total | 158 | 100% |

The (c) and (d) rules cluster almost entirely in 3.21 (R134 to R143: 7 generic, 2 correctly applied, 1 explicitly B2B and out of scope), with the rest spread thin: R56 (feeling-first design, flagged by its own mini playbook as "no ecommerce data"), R106 and R108 (staffing and a webinar poll, source 02), R114 (AI budget to emotional value), and R128 (a journey-map truism). Everything in 3.9 to 3.20 and 3.24, where the domain's weight sits, is 85% or higher store-specific.

## 2. Prioritisation check: missing, draft below

The playbook has strong pieces of prioritisation (R23's hierarchy, R43's VIP threshold, R125's test order, R126's payoff-ordered roadmap) but no single ranked list across the whole domain with conditions by store type. Section 0.3 routes by task, not by what matters most first. Draft:

### 3.0 Ecommerce priority order

1. Fix product and portfolio before any CX spend. A broken reason to return outranks every touchpoint fix. R23, R24, R25.
2. Get delivery date accuracy and proactive tracking above 90%. Cheapest, most universal WISMO and trust fix. R69, R70, R126 step 1.
3. Fix returns and refunds friction. Weight highest for catalogue and apparel brands with high return rates, lower for single-SKU low-return consumables. R96, R97, R102.
4. Build the 3-message post-purchase sequence and cut WISMO under 5%. Universal, low cost, high leverage. R67, R68, R71.
5. Design the unboxing peak. Weight highest for single-hero-SKU DTC brands with a strong physical identity, lower for commodity or marketplace-heavy catalogues. `[general practice]` on the marketplace weighting; R80, R83.
6. Time replenishment and the second-purchase nudge to the usage cycle. High priority for consumable and subscription brands, low for durable one-off categories. R34, R92.
7. Track CAC payback day for subscription or CPG brands only; one-off and durable brands skip to first-order profitability. R7, R11.
8. Set the LTGP window and CAC ceiling by capital and category. Bootstrapped or sub-15 to 20 million brands default 30-day; funded or high-repeat brands go 90-day or further. R7, R8.
9. Build engaged-audience and RFM segmentation, only after steps 1 to 4 are healthy. R23, R37, R40, R41.
10. Choose the update channel by audience and geography: SMS for older or US bases, WhatsApp for opted-in Indian D2C. The clearest store-by-geography rule the playbook already has. R75.
11. Build loyalty and VIP tiers only once delivery, returns and support are reliable, and only where VIP revenue is the constraint, roughly above 10 to 20 million a year. R43, R115.
12. Spend on existing-customer ads only in the fashion or frequent-drop exception. Every other store type skips this lever. R49.

## 3. Rule rewrites (13)

Condition, sources and card ids unchanged; only the lead sentence changes to name the store mechanic first.

- **R19**: "Do not stop at CSAT and NPS: track CLV by delight-touchpoint cohort, WISMO volume, unboxing UGC count, return-to-repurchase rate, tracking-page engagement and loyalty-redeemer repeat rate too, since CSAT and NPS only catch dissatisfaction, not a customer quietly drifting."
- **R56**: "Before writing a confirmation email, a tracking page or a return flow, decide the feeling you want the shopper to have there (reassured after checkout, informed during the wait, delighted at unboxing) and design copy and timing around it, not around urgency tactics like 'only 1 left.'"
- **R57**: "A delivery that lands exactly on the quoted date, or a refund that takes exactly as long as policy says, both leave the customer neutral and free to try a competitor next time. Beat the quoted date or refund window on cheap, visible steps to earn a small positive surprise instead."
- **R65**: "Never manufacture a stockout, a slow refund or a shipping delay to trigger a recovery moment. When a real failure happens (wrong item, late parcel, damaged box), over-recover it; do not treat failures as a marketing tactic."
- **R106**: "Build a staff checklist for the store's own edge cases before they happen: an order stuck in customs, a mis-shipped item, a stockout after the order confirms, a subscription payment failure. Do this during journey mapping, not live on a ticket."
- **R108**: "Shoppers rank 'helped me when something went wrong' above generic friendliness and close to ease of checkout; treat a bad return or refund experience as a bigger trust hit than slow live chat."
- **R112**: "Before turning on an order-status bot, a return-authorization flow or a WISMO auto-reply, write down the brand's tone, the words it never uses, and how it should sound different from a generic support bot."
- **R113**: "On handwritten notes, recovery emails and VIP messages, write in a human voice on purpose; do not let AI polish flatten the one moment meant to feel personal."
- **R114**: "Give AI budget to genuine post-purchase help (setup, troubleshooting, replenishment advice), not just ticket deflection, only in categories where the brand has real expertise to hand to the bot."
- **R120**: "Where the brand has a real shared activity (a run club, a restock alert group, a top-spender chat), build community around it as a retention channel AI cannot copy; do not launch a generic 'community' tab with no activity behind it."
- **R128**: "A journey map of the post-purchase funnel (confirmation, tracking, wait, delivery, unboxing, support, return, repeat) only earns its keep if it changes one of those touchpoints; if nothing ships, it was a workshop exercise, not CX work."
- **R144**: "Buy or use a Shopify-ecosystem app for search, ranking and merchandising unless the brand's edge genuinely is that engine; keep assortment, layout, supplier choice and merchandising judgment in-house."
- **R149**: "Treat any markdown or clearance pricing used to defend share as a costed decision against the discount-cohort penalty (F24), not a default reflex in a slow week."

## 4. Missing store levers (8)

| Lever | Where it would go | Source material in this folder |
|---|---|---|
| COD and RTO (return-to-origin) risk, central to India D2C economics | Near R71 and R96, a formula alongside F18 | No source in this folder, `[general practice]` |
| Self-service order edit or cancel before ship (address change, cancel window) | New procedure near P13 | No source in this folder, `[general practice]` |
| Gift-purchase experience: gift wrap, gift receipt, hidden price on the slip | New rule in 3.12 near R83 | No source in this folder, `[general practice]` |
| Subscription cancellation save flow (offer or pause shown at the cancel step) | Near R93 and R39's "cancelled" cohort | Sources only warn against a hard-to-cancel flow (05); no material on a proactive save offer, `[general practice]` |
| Chargebacks and payment disputes as their own cost line, separate from returns | Near R99 and F19 | One line only: source 05 lists cancellations and chargebacks as a mistake, no card id, no procedure. `[general practice]` for the rest |
| Cross-border duties, customs and landed-cost surprises at delivery | Near R69 and R76 | No source in this folder, `[general practice]` |
| Marketplace-channel post-purchase (Amazon or Flipkart-fulfilled orders the brand does not control) | New scope note in section 1 and 0.4 | No source in this folder (only an unrelated SAP Store mention in 03), `[general practice]` |
| Split or partial shipment communication for multi-item orders | New rule near R68 | No source in this folder, `[general practice]` |

## 5. Demotions

Move section 3.21 (R134 to R143, 10 rules, about 540 words) plus procedure P28 (about 150 words) and the section 6 rows "CX maturity split," "Consumer stats" and "Favourite-brand drivers" (about 50 words) to a new appendix, "General background: CX strategy theory (source 02)." This is a general corporate CX framework with almost no ecommerce mechanics; the playbook's own credibility note calls source 02 "general CX theory with no ecommerce content of her own." R141 (apply the same rules to B2B and wholesale) should move with it, since B2B is explicitly out of scope. About 740 words total.

## 6. Deliverables check (section 9): good, no renames needed

All 6 deliverables are things a retention or CX team would actually produce and use: a cohort readout with LTGP, CAC and repeat-rate tables (9.1); a ranked top-3 experience-fix brief with cost and expected effect (9.2); a retention test plan with a pre-registered decision rule (9.3); 8 support reply templates in brand voice (9.4); a filled-in journey audit with red or green flags (9.5); a delight payback model (9.6). None are generic documents; they are outputs a store's retention function would run each month. One gap: procedure P27 (roadmap in payoff order with exit gates) has no entry in section 9. Add a short 9.7, "Post-purchase roadmap with exit gates," so P27 produces a deliverable for leadership, not just an internal sequencing step.

## 7. The single highest-value change

Add the "3.0 Ecommerce priority order" block drafted in item 2. Right now an agent opening this playbook mid-task has excellent material but must assemble the "what matters most, in what order, for this kind of store" answer itself from R23, R43, R49, R75 and R126, scattered across 4 subsections written for 4 different sub-problems. A single ranked list, conditioned on subscription vs one-off, catalogue vs single SKU, and India vs US, turns 150 correct rules into a triage tool an agent can run in the first minute of a job, before it reaches a formula or a procedure.
