# Ecommerce specificity review: 19-WLD-wild-bets

## 1. Score and rule mix

Score: 4/5.

The procedures (section 4), the inputs table (section 2), and most cohort, mail, VIP, drop and subscription rules (groups E, F, G, K, L, M) run on store concepts: lifetime spend, AOV, 90-day reorder rate, contribution margin, cart abandonment, drop sell-through. That is real edge, not something a generic prompt would produce. But many numbered rules in section 3 are general startup, marketing or CX advice (Paul Graham essays, the Effortless Experience research, stunt theory) with a store example attached rather than a store-specific rule. A few passages are openly non-ecommerce and sit in the main body instead of an appendix.

I read all 143 numbered items in section 3, groups A to S, excluding pointers like R3, and classified each:

- (a) Store-specific: about 70 rules (49%). Groups E, F, G, J, K, L, M, plus D2, D6, B7, B8, O6, P1, Q1.
- (b) Generic but correctly applied to a store: about 38 rules (27%). Mostly group A, N, and rules in B, C, D, H, O where the idea (pilot small, voice fit, control groups) is general but the cohort is store-shaped.
- (c) Generic with no store framing: about 30 rules (21%). Concentrated in group C (bounding) and group O (stunts, guerrilla), plus B1, B4, B6, D1, D4, D5, D8, F6, F7, H5, H9, H11, I3, I5, I6. These read the same for a SaaS launch.
- (d) Out of scope for a DTC store: 3 rules. G13 (B2B corporate-gifting ABM), H7 (an inner-circle gift rule whose only evidence is 1 B2B case), H8 (Eleven Madison Park's $2 hot dog, which the playbook itself labels "not an ecommerce result").

These counts are a judgment call rule by rule. The closer a rule sits to a cohort, a cost or a stage gate, the more store-specific; the closer to "why wild bets work" or "how to run a stunt," the more generic.

## 2. Prioritisation check

No block ranks levers by what matters most for a store right now, conditioned on store type. What exists instead: a task-to-section lookup table (section 0), the 4-stage rollout with pass marks (B7, P3), and the default quarterly play sequence (9.1). These order plays by risk and cost, not store type. None adjusts for single hero SKU vs catalogue, low vs high AOV, subscription vs one-off, marketplace-heavy, luxury vs everyday, or mobile-first India vs US, except in passing (B8 mentions margin and product-test results; group K fires only for subscription brands by definition).

Draft block to add:

**3.0 Ecommerce priority order**

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

`[general practice]` covers the ranking order and store-type conditions above; the rule ids are the playbook's own.

## 3. Rule rewrites (up to 15, wording only, condition and sources unchanged)

1. B1: give the customer the fastest refund, replacement or exchange before any gift; a wild bet on a slow return process will not move repeat-purchase rate.
2. B6: split tickets into order/shipping problems (measure CES, first-contact resolution, resolution time) vs high-LTV relationship touches (measure repurchase rate, AOV, referral rate); a returns ticket is never a brand-elevation win.
3. C1: the bound's cohort is a segment from the customer order file (Shopify or Metabase); the budget cap is checked against gross margin on that segment's orders.
4. C6: add store triggers to the stop list: return rate rises after a keep-it pilot, refund rate rises after a guarantee, drop sell-through falls below full price, checkout conversion falls during a stunt spike.
5. D1: a reported repeat-purchase lift, ROAS or conversion lift from another brand is not a benchmark for this store's PDP, AOV or margin; it is an idea to test on this store's own cohort.
6. A3: fund 1 wild bet lever per quarter from the shared cash cap; do not split it across the discount ladder, the loyalty program and a drop at once.
7. A4: size the quarter's 3 bets so all 3 failing stays under a share of quarterly contribution margin, not revenue.
8. F6: forward every post-purchase, shipping and return email to the founder for 1 month while volume is low, to map checkout and delivery pain before any wild bet.
9. F7: map the path from ad or search to PDP to cart to checkout to repeat purchase for 20 real customers, and mark where a human touch fits.
10. H5: before scaling a gift-with-order program, secure enough vendor supply for expected weekly order volume, so gifts do not delay shipping.
11. H9: budget gifts to the top 1% repeat-buyer cohort as a fixed quarterly cost against gross margin, not a per-order spend to optimize.
12. I3: set a per-incident cap, a per-rep monthly cap and a per-customer cap on frontline spend, sized to the order's gross margin, logged against the order id.
13. I5: write the frontline gesture into support macros as a standing rule, not a one-off, so every eligible order gets the same treatment.
14. O3: budget the stunt against the marketing line; compare earned media value to incremental orders and contribution margin, not site traffic alone.
15. O9: confirm inventory and fulfillment capacity before the reveal date; a weak payoff risks a stockout the store cannot fill.

## 4. Missing store levers (up to 8)

1. WhatsApp or a local messaging channel for notes, drop alerts and reminders. No source (grepped, 0 hits). `[general practice]`. Extends F1, G1, M5.
2. Cash-on-delivery and return-to-origin risk as a base-effort gate. No source (grepped "COD", "RTO", 0 hits). `[general practice]`. Extends Stage 0 (P2) and 5.2.
3. Damaged-in-transit and packaging quality as a driver of return cost. No source (grepped, 0 hits). `[general practice]`. Sits next to J2 and H, P16.
4. A genuine per-SKU low-stock indicator for a catalogue that never runs drops (M3 only covers scarcity inside a scheduled drop). No source (grepped "low stock", 0 hits). `[general practice]`. Sits next to M3.
5. Considered-purchase artifacts for jewelry: engraving, a certification or appraisal guarantee, a gifting-occasion tie-in. No source (grepped "jewelry", "engraving", "certification", 0 hits). `[general practice]`. Sits in J and H.
6. A proactive post-delivery check-in (did it arrive, does it fit), distinct from the 100-day window. No source (grepped, 0 hits). `[general practice]`. Extends K5.
7. A customs or duty transparency guarantee for cross-border or diaspora buyers. No source (grepped "customs", "duty", 0 hits). `[general practice]`. Sits near J and S4.
8. A single-hero-SKU-vs-catalogue conditioning note: stage gates and cohort sizes (top 50, top 200, top 1%) assume a repeat-purchase catalogue business, which a single-SKU store cannot build the same way. No source addresses this split. `[general practice]`.

## 5. Demotions to a "General background" appendix

- H8, the Eleven Madison Park $2 hot dog story (about 70 words). The rule itself calls it "a fine-dining anecdote, not an ecommerce result."
- H7's Ruhlin and Brooks Brothers hotel-room case (about 70 words). Its only evidence is 1 B2B relationship, not a store case.
- G13, the whole rule on B2B, wholesale and corporate-gifting ABM (about 140 words with its checklist row). Explicitly B2B, not a DTC store play.
- The CRED example inside M2 (about 40 words). A fintech app's monthly actives, not an ecommerce case.
- A10's compounding-math illustration, 100 growing to about 14,000 in a year (about 60 words). The rule says "no ecommerce brand in the sources sustained it."
- The Zappos 10-hour-43-minute call and its $1.2 billion exit line in section 6 (about 50 words). General startup lore, not a store metric.
- O10, the Mercado Livre in-game placement case (about 80 words across rule and table). Already warns "platform-scale budgets do not transfer to a small store."

## 6. Deliverables check (section 9)

The 6 deliverables (quarterly plan, approval request, readout memo, registry entry, play catalogue card, Stage 0 audit report) are shaped like a general experiment program, though their content (cohorts, LTV, AOV, margin) is store-specific. A store team would recognize the plan and the readout memo, but 2 things are missing: customer-facing wording sits buried inside the approval request, and gift or insert plays (H, P7, P16) have no handoff document for the packing team.

Proposed changes: split customer-facing wording out of 9.2 into its own "On-site and lifecycle copy pack" (notes, emails, terms, claims-page copy, SMS). Add a 7th deliverable, a "Packing and fulfillment instruction sheet" for any play adding a physical item to an order, naming item, trigger, cohort and exclusion list, so ops can run it without the full bet brief.

## 7. The single highest-value change

Add the "3.0 Ecommerce priority order" block, conditioned by store type, and put it first in the "which sections to load" table. Right now an agent has to read 143 decision rules across 19 groups and infer what matters most for this brand, AOV and purchase frequency. A short, ranked, conditioned list at the front turns the playbook from a well-sourced reference into a decision tool: it tells the agent where to start for a single hero SKU versus a catalogue, subscription versus one-off, and high-AOV considered purchase versus low-AOV impulse buy. That is the difference between a strong research library and a playbook a store operator would run from on day 1.
