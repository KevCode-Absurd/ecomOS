# 24-DEP-ad-deployment: ecommerce specificity review

Reviewed `playbooks/v2/24-DEP-ad-deployment/PLAYBOOK.md` (10 sources, 213 cards, 107 decision rules R1 to R107) against `playbooks/v2/TEMPLATE.md`, read in 3 chunks with a rule-by-rule classification.

## 1. Ecommerce specificity score: 3 / 5

The playbook is written only for Meta and TikTok deployment on a store, and its strongest material (economics ceiling, GP to CAC bands, new-customer profitability checks, exclusion sizing, DPA and SKU-level scale checks, TikTok Shop and GMV Max) could not come from a generic prompt. But just over half the 107 rules are platform-mechanic rules (auction and delivery model, attribution windows, ad set hygiene, budget pacing, TikTok setup clicks) that would read the same for a lead-gen or SaaS advertiser on the same platforms, with no store framing added. The store-specific core is real and load-bearing, but it sits inside a large shell of generic paid-media knowledge a general model already has.

Rule-by-rule count (judgment calls noted where borderline; counted at rule level):

| Category | Count | Share |
|---|---|---|
| (a) Store-specific | 31 | 29% |
| (b) Generic, correctly applied to a store | 16 | 15% |
| (c) Generic, no store framing | 60 | 56% |
| (d) Out of scope for a store | 0 | 0% |

Nothing scored (d); every rule sits inside an ecommerce example even when the mechanic is generic. (c) concentrates in group J, algorithm mechanics (8 of 8), group D targeting (5 of 6), and groups G, I, O (TikTok setup clicks): a Meta or TikTok mechanic with no store consequence attached (SKU, AOV, margin, repeat purchase, season). (a) concentrates in groups B, H, L, P: spend-tier templates, GP to CAC, exclusion sizing, DPA, TikTok Shop and GMV Max.

## 2. Prioritisation check

No ranked lever list exists. Section 0's task router tells the agent which sections to load per task, and R1 gives 1 general sequence (data, then structure, then creative), but nothing ranks levers by store type (hero SKU vs catalogue, low vs high AOV, subscription vs one-off, marketplace-heavy, luxury or considered purchase, mobile-first India vs US). Draft block below, built only from the playbook's own rules and section 7 conflicts.

**3.0 Ecommerce priority order** (draft, insert after section 2)

1. Fix data access and new-vs-returning order data before any read. R1, R59, P9 step 1.
2. Confirm unit economics can support paid acquisition (AOV, margin, LTV) before sizing any test or scale plan. R3.
3. Pick the structure template for spend tier and business complexity. R7, R9 to R13. Catalogue or multi-persona stores need business-unit campaigns; single hero-SKU, low-AOV stores can consolidate (R9's 10% exception).
4. Set attribution to 7-day click everywhere and reconcile with acquisition MER before trusting any number. R55, R58, R59, P18.
5. Exclude existing customers from all cold spend, sized to the repurchase cycle. R27. Subscription or short-cycle stores need a tighter window than one-off or considered-purchase stores.
6. Hit the creative volume and concept-diversity band for the spend tier. R40, R41.
7. Confirm a "winner" is a real new-customer winner before briefing more of it. R46, P8. Matters most for high-AOV, low-volume or marketplace-heavy stores where 1 ad can carry the account.
8. Scale through equilibrium and a dedicated scaling campaign, not budget jumps. R49 to R51.
9. Choose a scale ceiling the owner has agreed to: GP to CAC band (default) or near-break-even with a cash check for cash-rich, high-repeat brands. R52, section 7.16. `[general practice: match to subscription vs one-off]`
10. Read frequency by segment monthly; existing-customer frequency is the first fatigue signal for repeat-purchase categories. R71, R77.
11. Cap retargeting and DPA as a support layer, not a growth line; DPA share is the fastest catalogue-store red flag. R75, R81.
12. Re-audit structure and creative bottleneck order on a cadence tied to spend tier and season. R87 to R91. `[general practice: tighten cadence going into peak season; no source gives a peak-season cadence]`

The playbook has no split for marketplace-heavy stores, or mobile-first India vs US beyond "convert to the brand's currency" and India-only DPDP notes. Flagged again in section 4.

## 3. Rule rewrites (15, wording only; condition, sources and card ids unchanged)

1. **R17.** Concept = the SKU or range, the buyer's stated pain or occasion, and the price or bundle offer on the PDP; changing any one is a new ad set.
2. **R18.** Load each concept ad set with enough ads that a shopper sees a matching hook 2 to 6 times before the PDP decides the sale, not just before the ad "learns".
3. **R24.** Go broad and let the product page, price and reviews qualify the buyer; do not pre-select by interest when the PDP and offer already do that work.
4. **R38.** Test ads that differ by product benefit, price point or persona, not just crop or colour, so a losing SKU angle and a losing hook are never confused.
5. **R42.** Judge and move budget at the ad set (SKU or concept) level; a single ad's ROAS says nothing about whether that product angle works.
6. **R55.** Read and pay on 7-day click because a shopper's path from ad to checkout, not a view, is what the store gets paid for.
7. **R63.** Every impression a shopper sees is scored and ranked first; a store wins impressions with strong buy signals (clicks that convert), not by fighting the auction with bid alone.
8. **R64.** A cheaper bid beats a pricier one when the ad's expected click and purchase rate is higher, so a sharper product hook or clearer price buys cheaper reach than raising the bid.
9. **R68.** Pass every order and its value cleanly from checkout to the pixel and CAPI; a store missing 30% of real orders is bidding blind on its actual best customers.
10. **R75.** Ask "where can cold spend grow" for new-customer campaigns and "where can this shrink" for cart-abandoner and past-buyer campaigns; retargeting supports the store, it does not grow it.
11. **R82.** Keep flexible or dynamic-crop ads off catalogue and product ads so a shopper never sees a cropped or mismatched product photo they did not order.
12. **R83.** Turn Advantage+ creative edits off on every product ad; an automatic overlay on a jewellery or apparel photo can misstate size, material or price.
13. **R88.** Start every audit at store revenue and new-customer revenue, not the ad platform, because platform numbers cannot see refunds, COGS or repeat buyers.
14. **R94.** Launch the first TikTok campaign as a website Sales campaign with the catalog off, so the pixel is credited for real checkouts, not browsing a synced catalogue.
15. **R107.** Build TikTok retargeting from site visitors and cart or product-page viewers, excluding recent buyers, so spend chases shoppers still deciding, not repeat buyers.

## 4. Missing store levers (up to 8)

| Lever | Where it would go | Source check |
|---|---|---|
| Peak-season (BFCM, festive/Diwali) budget and structure ramp | New item near 3.0.12 | Partial: source 02 gives CPM inflation "cyclical around Black Friday" [5b99bf6d671d] and Q4 CBO/Q1 ABO rotation [2f66cf4f65c6]. No procedure for pre-sale ramp, sale-price messaging, or wind-down. |
| Marketplace-heavy stores (ads driving Amazon/Flipkart sales, not the brand's own checkout) | Section 1 scope, group I | No source in this folder, `[general practice]`. Source 01 only covers syncing a feed to TikTok Shop, not attribution for outside marketplaces. |
| Cash-on-delivery and payment-friction effects on the purchase event | Group I, R55 to R59 | No source in this folder, `[general practice]`. No COD mention anywhere in `sources/`; relevant to India mobile-first stores like Gehna. |
| Stock-aware pacing (no added spend to an ad for a low or out-of-stock SKU) | P5 step 2, P9 | Partial: source 02 grades inventory A to D for margin segmentation [ebff07a9e6f2] but gives no live stock check before a scale step. |
| Repurchase-cycle-timed win-back ads (reminder near a customer's typical reorder date) | Group L, near R77 | No source in this folder, `[general practice]`. R77 gates existing-customer spend on repeat purchase being "expected" [3a48f7471999] but gives no reminder-timing rule. |
| Considered-purchase or luxury nurture (longer retarget window, financing/EMI messaging) for high-AOV categories like jewellery | Group L, near R80 | No source in this folder, `[general practice]`. R36 and R71 note longer windows and lower cold frequency for slow-cycle categories but no nurture ladder. |
| Cross-border, multi-currency ad and landing experience (duties, delivery time, currency display) | Group B, near R12 to R13 | Thin: R12 splits ad accounts by currency only [b8c4642d637c]; no rule on creative or targeting for cross-border buyers. |
| Return and exchange policy as a conversion or retargeting trust signal | Group L, near R80 | No source in this folder, `[general practice]`. All "return" hits in `sources/` are about ROAS or warehouse logistics, not shopper-facing return policy. |

## 5. Demotions

- **Group J, R63 to R70** (delivery, ranking, auction, Entity ID, EMQ mechanics; about 900 words). How Meta's system works for any advertiser on any vertical; nothing names a store metric. Move to appendix "General background: how Meta delivery works"; keep only the store-consequence lines (broad as probe, EMQ as plumbing) in the main rules.
- **Section 12 source credibility narratives** (about 2,000 words across 10 sources). Useful for provenance, not for running the domain. Keep 1 line per source in the index; move the full paragraphs to an appendix.
- **P11 steps 1 to 4** (TikTok Business Center admin: documents, card on file, 2-step auth; about 150 words). Standard onboarding for any TikTok advertiser, store or not. Low priority, short and needed once; note only.

## 6. Deliverables check (section 9)

The 5 deliverables are store-usable as written: the diagnosis memo carries CAC, GP to CAC and aMER; the budget JSON carries store currency and rule-id reasons; the kill-keep-scale list is per ad set with a creative brief line for 10-MCR; the test plan carries persona, angle and offer; the TikTok launch sheet is a pass/fail checklist. No renames needed. One addition worth considering once lever 1 above is added: a short "peak-season plan" deliverable (ramp dates, sale-price ad set, wind-down date), since none of the 5 current deliverables covers a sale event end to end.

## 7. Single highest-value change

Take every rule marked (c), mostly the algorithm, attribution and ad-hygiene rules in groups D, G, I and J, and add 1 line stating the store consequence: which SKU, margin, segment or season it changes the call for. Right now an agent could correctly explain the auction or set an attribution window without touching a business number. Adding the 3.0 priority order and forcing every generic rule onto a CAC, margin, repeat-purchase or peak-season consequence turns this from a well-organised paid-media manual into a document a generic model could not have produced for this brand.
