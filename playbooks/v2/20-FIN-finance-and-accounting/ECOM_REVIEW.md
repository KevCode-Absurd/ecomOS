# Ecommerce review: 20-FIN Finance and accounting

Reviewed `PLAYBOOK.md` (1,732 lines, sections 0 to 12) against `TEMPLATE.md` and `sources/`.

## 1. Ecommerce specificity score: 4 out of 5

This playbook is built almost entirely from DTC operators and agencies, so its formulas and rules already speak in store terms: landed cost per SKU, CM1 to CM3, break-even CAC against first-order gross profit, cohort LTV, discount-plus-CAC as one pool, inventory days versus lead time, and platform (Shopify, Meta, Amazon) reconciliation. It loses a point because a handful of rules are stock accounting mechanics (3-statement reads, FCF sign convention, "show the numbers to everyone") with only light store framing, and because there is no ranked "do this first" view for an agent working a real store.

Section 3 has 142 numbered rules, R1 to R142 (F1 to F45, the formula register, is almost entirely ecom-specific and not counted here). Some calls are judgment; a different reviewer might shift a few rules by one category.

- (a) Store-specific: 122 rules (86%). Examples: R6 (CM2 ceiling on CAC), R53 (first-order gate), R58 (LTGP:CAC bands), R107 (days of inventory vs lead time), R130 (platform-to-books reconciliation).
- (b) Generic, correctly applied to a store: 14 rules (10%). Examples: R2 (exclude sales tax from revenue), R11 (statutory COGS "all in until it's in"), R19 (coupons reduce revenue), R31 (revenue is not profit), R94 (simple payroll models), R97 (FCF over net income).
- (c) Generic, no store framing: 6 rules (4%): R26 (interest below EBITDA), R32 (reconcile the model to itself), R39 (show the numbers to everyone), R99 (read the 3 statements in order), R100 (FCF for operations, net cash flow for solvency), R101 (cash cuts fast only on cash-equal lines).
- (d) Out of scope: 0 rules. No B2B, SaaS-only or publisher content in section 3. Section 6 keeps 2 comparison rows (SaaS and CPG gross margin) already labelled as not ecommerce, used only as sanity anchors.

## 2. Prioritisation check: missing. Draft below.

The routing table in section 0 ("which sections to load for which task") sorts by task, not by what matters most. No section ranks levers or changes order by store type (hero SKU vs catalogue, low vs high AOV, subscription vs one-off, marketplace-heavy, considered purchase, India vs US). Note: the playbook already uses "3.0" for the formula register, so insert this block as "0.1" right after "How to use this playbook," or renumber it "3.0a" ahead of the formulas.

**3.0 Ecommerce priority order**

1. Check cash before profit: 13-week forecast, lowest projected cash month. Many ecom stores fail on liquidity, not unit economics. R103, R97 to R102, P19, P20.
2. Get CM3 (post-marketing contribution) positive. Nothing below it fixes a business losing money after marketing. R7, F10.
3. Gate acquisition on CM2 per new order vs CAC (break-even). Default for every store; only cohort-proven repeat businesses spend above it. R6, R53, F15.
4. Split new vs returning revenue; manage to aMER, not MER, which hides new-customer efficiency. R37, F14.
5. Get landed cost and COD right per SKU; a wrong COGS number breaks every rule above it. R5, R11-18, F4.
6. Match ad spend to inventory position; do not buy CAC for a SKU about to stock out. R107, R108, R109.
7. For repeat or subscription stores: read LTGP:CAC in a fixed window and cohort payback before spending past break-even. Higher priority for subscription and considered-purchase; buy-once categories stay on rule 3. R57, R58, R60-62.
8. Treat any discount and CAC as one pool; recompute break-even at the discounted price before it goes public. R67, R68, R69.
9. Price new SKUs bottom-up from the waterfall, not keystone. Matters most for catalogue stores; less for a hero-SKU store repricing rarely. R77, R78.
10. Manage the cash conversion cycle and PO sizing; this, not ad efficiency, caps growth for stores carrying inventory. R115, R116, F34 to F36.
11. Reconcile platform numbers to the books monthly. More urgent for marketplace-heavy stores with more gaps to close. R129, R130.
12. For subscription stores only: run churn and prepaid as its own economics, separate from transactional CM. R134 to R142.

Store-type notes, marked `[general practice]` where the playbook gives no explicit condition: catalogue stores pull SKU-level contribution (P7, 9.2) into rule 6 sooner than a hero-SKU store, which instead watches one stockout risk closely `[general practice]`. Luxury or considered-purchase stores extend the LTV window toward 365 days or the plateau month (R55) and may miss the first-order gate at launch `[general practice]`. India stores keep the same order but swap every US or Australian rate for the local one, as section 0 already flags.

## 3. Rule rewrites (up to 15, store-specific wording, conditions and cards unchanged)

1. **R26**: interest on a PO loan or merchant cash advance stays below EBITDA, never OPEX, so the 4 buckets show fulfilment and acquisition health separate from how inventory was financed.
2. **R99**: read the 3 statements with the ecom lines in view: inventory on the balance sheet, marketplace payout lag in receivables, PO deposits in cash, before checking assets equal liabilities plus equity.
3. **R100**: for a store with inventory financing or a PO loan, judge the business itself on free cash flow and judge whether it survives its debt schedule (draws, PO financing, principal) on net cash flow.
4. **R101**: in a cash squeeze, cash comes back fast only from ad spend, payroll and 3PL or warehouse fees; cutting warehouse depreciation releases nothing, and cutting spend below break-even worsens the squeeze.
5. **R39**: put daily CM3, aMER and the inventory position in front of marketing, creative and ops, not only finance, since those teams move the numbers that move CM3.
6. **R32**: reconcile the SKU roll-up (9.2) and the cohort roll-up (P9) to the monthly ladder (P1) every close; a mismatch is a formula error, not rounding.
7. **R94**: build payroll in the store's own buckets (marketing and creative, warehouse and fulfilment, support, executive) plus on-costs, not a 700-row tab, so it matches how a store staffs for peak.
8. **R96**: one owner tracks daily CM3 and ad pacing; a second owns the marketing calendar and inventory plan months out, so a stockout or BFCM peak is not missed while someone is heads-down on today's spend.
9. **R121**: weigh a store's real borrowing options for a PO or peak-season buy (credit card float, a merchant cash advance, supplier terms) against these reference rates before deciding who carries the float.
10. **R11**: for every SKU in the catalogue, COGS is the purchase price, inbound freight, duty paid and product packaging to get that unit onto the shelf ready to sell; apply the same backup test per SKU.
11. **R19**: a promo code, automatic discount or BOGO reduction at checkout reduces net revenue; never book it as ad spend or COGS, even when marketing owns the discount-and-CAC pool (R67).
12. **R20**: Meta and Google spend, influencer fees and affiliate commissions are never COGS; a partner that ships or picks the product can be COGS, one that only markets it cannot.
13. **R29**: add the percent-of-revenue column to every ladder and 4-bucket line, so a rising marketing percent while scaling reads differently from a rising COD or OPEX percent, which should hold steady.
14. **R87**: when the owner wants a higher number than the model gives, name the store action that closes the gap (a launch, a promo, a new channel, more spend at a stated aMER), not a generic stretch target.
15. **R22**: post every inbound shipment to inventory by SKU and receive date; move it to COGS only when the unit sells, or a big-PO month will show a false loss.

## 4. Missing store levers (up to 8)

1. **Chargebacks and payment disputes, as a tracked cost and fraud flag.** In 3.5 or checklist 5.1. Mentioned once inside the net-revenue formula (03, `c9ccfa76430a`), never built into its own rule or threshold.
2. **Sales tax or GST nexus, registration thresholds, marketplace-facilitator remittance.** In section 10, tax sub-topic. No source in this folder, `[general practice]`.
3. **Gift cards issued and redeemed as deferred revenue, plus breakage.** In 3.1 next to R3. No source in this folder, `[general practice]`.
4. **Loyalty or rewards points as a balance-sheet liability, and their margin cost at redemption.** In 3.1 or 3.8. No source in this folder, `[general practice]`.
5. **Multi-currency revenue and FX exposure for cross-border sales**, beyond the landed-cost FX in F4. In 3.16 or a new 3.18. Partial source: 04 notes currency swings on supplier payments but not how to book them.
6. **Annual budget-setting and a budget-vs-actual cadence**, distinct from the close and the rolling forecast. In section 0 or a new 3.19. No source in this folder, `[general practice]`.
7. **Fraud, bot orders and duplicate accounts inflating the "new customer" count** that CAC (R44) and the cohort table depend on. In checklist 5.7. No source in this folder, `[general practice]`.
8. **Customer support or CX cost per order, classified in COD or OPEX.** In F6 and the P3 tree. Source exists but was dropped: mini playbook 06, card `332efa25ba89` ("classify ecommerce customer support costs consistently").

## 5. Demotions to an appendix "General background"

Move these to a short appendix, with a 1-line pointer where P1, P15 or P19 still cite them:
- R26 (interest below EBITDA), R32 (reconcile the model to itself), R39 (show the numbers to everyone), R99 (read the 3 statements in order), R100 (FCF vs net cash flow), R101 (cash cut fast only on cash-equal lines). About 275 words combined.
- The section 6 row "SaaS gross margin 70 to 90%... not ecommerce" (about 15 words), already labelled as a non-ecommerce comparison. Keep the CPG row as a sanity anchor for physical-product brands.

## 6. Deliverables check: yes, store-native

All 8 deliverables in section 9 are things a store team would use: a weekly profit memo (9.1), a SKU contribution table (9.2), a scenario answer for a spend decision (9.3), a standing alert list (9.4), a monthly close pack (9.5), a COGS and landed-cost table (9.6), a cash, inventory and PO sheet (9.7), and an offer or price go/no-go (9.8). None reads like a generic "financial report." No renames needed. The gap: 9.3 and 9.4 would read better pointing to the numbered priority order in section 2, not only to individual rules.

## 7. The single highest-value change

Add the "3.0 Ecommerce priority order" block. Everything else here is already deep, cited and store-specific: 142 decision rules, 45 formulas, 28 procedures, 7 checklists and 21 named conflicts. It lacks an entry point that tells an agent, for a specific store (hero SKU or catalogue, subscription or one-off, cash-constrained or not), which few of those 142 rules to act on first. Without it, the playbook reads like a reference book; with it, it reads like an operator who has already decided what matters this week.
