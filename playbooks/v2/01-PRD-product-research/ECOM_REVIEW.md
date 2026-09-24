# Ecommerce specificity review: 01-PRD-product-research

Scope: PLAYBOOK.md against TEMPLATE.md's Pass 2 format and this domain's job, finding and validating a product for a DTC store (PDP, checkout, ad-driven traffic, margin, inventory, seasonality).

## 1. Score and rule mix

**Score: 5 out of 5.** This playbook is built from store operators screening real ad and TikTok Shop data, so most rules already carry ecom mechanics (revenue bands, margin floors, competitor ad counts) instead of generic business advice. It also tags every rule that only holds for the dropshipping arbitrage model and rewrites it for a branded, inventory-holding store, and grades each source's commercial bias before using its numbers. What remains thin: no ranked priority order by store type, and no coverage of payment or marketplace realities outside the US Meta and TikTok Shop world.

Section 3 has 109 numbered rules, R1 to R109. The 6 ecomOS overrides (O1 to O6) are ecomOS's own governance layer, not source rules, so they sit outside this tally.

| Class | Count | Share | Meaning |
|---|---|---|---|
| (a) Store-specific | 81 | 74% | Names a store mechanic: PDP, ad platform, margin, MOQ, SKU, delivery window, ad count |
| (b) Generic, applied to a store | 22 | 20% | A general principle (trend risk, AI hygiene, procurement) scoped to an ecom step with an ecom example |
| (c) Generic, no store framing | 6 | 6% | Same for any business: R92, R95, R96, R106, R108, R109 |
| (d) Out of scope for a store | 0 | 0% | None found |

## 2. Prioritization check

No. Section 0 routes the agent to sections by task, and section 3 groups rules by subtopic in a fixed order, but nothing ranks the levers by what matters most, and nothing branches by store type (hero SKU vs catalogue, low vs high AOV, subscription vs one-off, marketplace-heavy, luxury or considered purchase, mobile-first India vs US). Section 7 comes closest (C1, C3, C5 to C7 resolve by store trait) but is not assembled into one list. Draft below, from the playbook's own rules and section 7.

### 3.0 Ecommerce priority order (draft)

1. **Margin and contribution gate (R76, P14, O4).** Nothing else matters if the product cannot pay for its own acquisition cost; the hard stop every source implies.
2. **Regulatory and IP clearance (R84, R86).** A miss voids the SKU after money is spent on samples or ads; the other no-override stop (R106).
3. **Owned difference named (O2, R60).** Proven demand with no angle is a cash test (R56), not a bet for a brand holding inventory and reputation.
4. **Demand read matched to the brand's own ad platform (R24, R44 to R49).** TikTok-Shop-heavy brands read video and live data directly (R15 to R21); Meta-only brands treat TikTok data as a lead, not proof.
5. **Competition ladder, exact-product and niche level (R53, R54).** Amber or red with no angle routes to P12 first; green goes straight to economics.
6. **Price band and margin floor from the store's own AOV (R75, R76, O4).** Impulse-price stores live or die on the dollar floor; a luxury or considered-purchase store should raise it and lean less on the 3x multiple `[general practice]`.
7. **SKU strategy by store type (R59, R87, C5).** A hero-SKU launch opens at 1 SKU with a secondary-product plan; a catalogue brand checks gaps in its existing range instead, since R87 assumes no catalogue yet `[general practice]`.
8. **Subscription or repeat fit from real usage (R72, R9).** Subscription stores gate on replenishment cadence; one-off or considered-purchase stores check LTV against AOV instead (06, 09; card 3b6e3ec9a71b).
9. **Sourcing model by channel (R93, R50).** A no-inventory store compares agent vs marketplace-direct cost (R93); a store also on a third-party marketplace reads that marketplace's own density and fees separately `[general practice]`.
10. **Logistics and durability priced before sourcing (R81 to R83, R85).** A shippability gate, not a differentiator, but it still kills candidates that passed 1 to 9.
11. **Supplier vetting and sample order (R89 to R92).** Only after the SKU clears 1 to 10, so cash and goodwill are not spent early.
12. **Launch sequencing and expansion order (R99, R100).** A mobile-first India-vs-US move must re-price duty, payment friction and delivery days per market first `[general practice, see section 4]`.

## 3. Rule rewrites (15 of the 28 rules in classes b and c)

Condition, sources and card ids stay as written; only the rule's wording changes.

- **R4.** Watch for a shift in how people shop, pay or get delivery (buy-now-pay-later, TikTok Shop checkout, same-day delivery) that incumbents have not built for; it only counts once it changes what a buyer expects on a PDP or at checkout.
- **R8.** Ground a pain point in a review naming the product and a real complaint (a PDP review, a return reason, a support ticket), not a category-level post; confirm it is about the product, not the topic.
- **R11.** A founder's own taste is not a demand signal; run the demand check (P9) or the store's conversion and repeat-purchase data before funding a candidate on preference.
- **R14.** Trend tools are a source of SKU ideas only; every idea clears the same PDP-ready checks (platform demand, Ad Library count, landed-cost margin) as a product scouted from Meta or TikTok Shop before it reaches the shortlist.
- **R37.** The moment a scouted post shows a sellable product with a visible price and offer, stop scrolling and log it; more scrolling delays validating it, it does not improve the shortlist.
- **R42.** Search reviews for a buyer naming a price they would pay, a competitor price they found too high, or a pre-order pledge; the closest proxy to price-band fit (R75) before a live listing exists.
- **R44.** Keyword volume and social mentions size interest; they do not confirm anyone will check out at your price. Cross-check Google Trends and the Ad Library before shortlisting.
- **R47.** A rising trend can reverse before inventory sells through; do not commit an MOQ order to a hero SKU on trend data alone, plan a secondary evergreen SKU (R59) before ad spend starts.
- **R48.** A stable read, where search volume and unit sales hold together, supports a permanent catalog SKU; a spike with no matching sales is a signal for one limited batch, not an MOQ order or a built-out PDP.
- **R67.** Pull packaging and PDP imagery cues from an unrelated retail category, not a competitor's product photos, which O2 already forbids copying.
- **R80.** Before scaling ad spend on strong early signal, separate a fixable operational problem (weak copy, a mispriced offer) from a structural cost problem ad spend cannot beat; scale the first, stop the category on the second.
- **R86.** Before listing a fandom-adjacent or licensed-look product, check trademark exposure with the same rigor as the country regulatory check (R84); a takedown after launch costs the ad spend and the SKU.
- **R92.** Receive a sample through the store's own fulfillment chain, not only the factory, before committing to MOQ inventory or PDP photography; a sample that fails unboxing or shelf-life kills the SKU first.
- **R95.** Set a reminder to re-quote every supplier once a SKU's order volume crosses a threshold (500 or 1,000 units); do not assume the landed cost in the margin gate (R76) still holds as it scales.
- **R106.** The agent may override one amber-level ecom check per product if it names the overriding number in the log; it may never override a red on the margin gate, the regulatory check, or the owned-difference requirement (O2).

## 4. Missing store levers

Checked `sources/` for each topic with grep.

1. **COD, RTO and payment friction for a mobile-first, cash-on-delivery market.** Goes in section 2 and 3.12. No hits for "India", "COD", "RTO" `[general practice]`.
2. **Selling on a third-party marketplace (Amazon, Flipkart, Meesho, Myntra, Etsy) as a channel.** Goes in 3.1. Amazon appears only for ratings and search volume (07, cards d814f1dad676, 385b53666fdd), never as a channel with its own fees and competitors `[general practice]`.
3. **Category-specific certification beyond generic "regulations"** (jewelry hallmarking, BIS marks, per-country cosmetic rules). Sharpens R84 and P13 Q16. One example exists (07, GreenGuard Gold on cribs, card 48b21947926b) but no general method `[general practice]`.
4. **LTV as the repeat-purchase metric, not just AOV.** Goes in 3.10 and P14. Buried, not missing: 06 names LTV as "substantially higher than AOV" with no number (card 3b6e3ec9a71b), 09 covers usage frequency (cards 494c8db9f8ce, 480136acffdb), but no rule weights it like the margin gate.
5. **Influencer or creator seeding as a demand and content method**, distinct from burner scouting (P6). Only a one-line IP caution about influencer video exists (05) `[general practice]`.
6. **Gifting and occasion demand (festivals, wedding season)** beside Christmas and Black Friday. Goes in 3.9 next to R70. No hits for "gift" `[general practice]`.
7. **Payment-gateway friction as a margin input** (COD fee, failed-payment retry, prepaid-discount cost). Goes in P14. No source covers it `[general practice]`.
8. **Warranty or after-sales cost for considered-purchase categories** (electronics, jewelry, appliances). Goes in 3.14 and D3. No hits for "warranty" `[general practice]`.

## 5. Demotions

Two rules read as founder-psychology aphorisms with no ecom framing even where the example is ecom: **R108** ("if it is hard, it is probably wrong", about 90 words, with a 6-month founder story) and **R109** (one win is not a repeatable formula, about 70 words, tied to mistake 31). The "uphill phase before breakthrough" threshold row (about 15 words) belongs with it. Move these three, about 175 words, to an appendix "General background: founder psychology", leaving a one-line pointer from mistake 31 and C4.

## 6. Deliverables check

D1 to D4 are real store deliverables, not generic documents: a scored shortlist with margin and competitor-ladder columns, a validation memo, a supplier brief with MOQ and landed cost, a launch plan with duty and VAT per market. One gap: no standalone offer-ladder deliverable, even though R63 covers the content; it is folded into D2's angle brief. Propose **D5: Offer ladder**, one page from R63 and R76, so 05-WEB gets a page-ready pricing structure instead of extracting it from prose. No renames needed elsewhere.

## 7. Single highest-value change

Add section 3.0 and require the validation memo (D2) to open with the store's type against that order (hero SKU or catalogue, subscription or one-off, marketplace or DTC-only, considered-purchase or impulse). The playbook already carries excellent store-specific mechanics rule by rule, but it treats every store the same: a single-SKU launch and a 40-SKU catalogue brand read the same subtopic order and thresholds. Ranking the levers once, using conditions already scattered through section 7's conflicts, turns 109 correct rules into a decision path that changes with the store in front of it, which a generic prompt cannot do even knowing all 109 rules.
