# Ecommerce specificity review: 22-AMZ-amazon-marketplace

Reviewer: Claude. Scope: PLAYBOOK.md against the TEMPLATE.md format and the ecomOS store-specificity bar.

## 1. Score and rule mix

**Score: 4 out of 5.** The playbook is built almost entirely around store economics: a 30% net margin gate, a fee stack in cents per unit, inventory cover in months, launch velocity tied to Amazon's ranking mechanics, and a hard wall between own-brand selling (in scope) and arbitrage or wholesale (out of scope, section 0 and conflict 1). Every rule states its condition and source, and section 7 keeps 14 real disagreements open instead of averaging them into a false consensus, which is directly useful to an agent working on real brand numbers. It loses a point because it has no ranked "what matters most, for what kind of store" block, and a handful of rules (trademark type, entity setup, NNN agreements) read as generic legal or business advice that would fit a SaaS company just as well.

**Section 3 rule mix (97 numbered rules, R1 to R97):**

- (a) Store-specific: 85 rules (about 88%). Examples: R35 (30% net margin gate), R52 (title keyword placement), R90 (3 to 6 months of cover), R84 (Amazon's own review-request path).
- (b) Generic but correctly applied to a store: 9 rules. R6 (don't delay launch), R7 (differentiate vs clone), R22 (NNN agreement, patents), R43 to R46 (ask capacity, get a sample, inspect before balance, reversible payment), R48 (air vs sea), R67 (keep the BOL). These are standard manufacturing, sourcing or business-psychology practice, tied here to an Amazon launch date, FBA check-in or reimbursement claim.
- (c) Generic with no store framing: 3 rules. R14 (EIN, seller's permit, separate business bank account), R18 (design mark vs word mark), R76 (recover a stalled launch, thin and generic).
- (d) Out of scope for a store: 0 rules inside section 3. The arbitrage and wholesale material (BSR under 100,000, 30% ROI, Buy Box repricing) is real in the sources but the playbook keeps it out of section 3 entirely and only names it in section 0's wall-off and section 6's two rows marked "out of scope." That is the right place for it, not a gap.

## 2. Prioritisation check

No, the playbook does not rank levers by store type. Section 0's "sections by task" table routes an agent to the right sections for a job, but it is a lookup table, not a ranked list of what matters most, and nothing in the playbook conditions the order by single SKU vs catalogue, low vs high AOV, subscription vs one-off, marketplace-heavy, luxury, or mobile-first India vs US. Draft block:

### 3.0 Ecommerce priority order

1. Net margin gate, 30% or more after landed cost and every fee (R35, R3). Nothing else matters if this fails.
2. Price at $25 or more and 3x unit cost (R24, R36, conflict 8). Sets whether PPC and referral fees leave any margin; matters most for a low-AOV SKU.
3. Real differentiation, not a generic clone (R7, R25 to R27, R30). Competes on a fixable gap in reviews, not on price.
4. Inventory sizing: cover enough to avoid a stockout without paying long-term storage (R90, R91, conflict 2). The sources' biggest reported losses; matters most for a single hero SKU with no backup stock.
5. Listing SEO: title, bullets, keyword buckets (R52 to R54). Cheapest acquisition channel once live, and it compounds; PPC does not.
6. Main and secondary images (R55, R56). Biggest conversion lever at the search grid; a bad image loses the click before copy is read.
7. Launch concentration: stock live, PPC on, audience ready the same week (R71, R72, R77, R78). Matters most for a single hero SKU launch; less for adding a SKU to a proven catalogue.
8. PPC discipline: negatives from day 1, judged on net profit not sales (R81, R82). Largest controllable variable cost after fees.
9. Brand Registry and trademark timing (R17, R19, R20). Unlocks A+, Vine, Sponsored Brands and hijacker protection; start early since approval lags months. `[general practice: ranked here for lead time]`
10. Ongoing fee-stack and storage modelling, including the long-term storage window (R37 to R39, R92). Protects the margin gate after launch.
11. Review compliance path (R84 to R86). A compliance floor, not a growth lever, but non-negotiable.
12. Account health monitoring (R88, R89). Losing the account erases every other lever. `[general practice: monitoring backstop, not ranked by any source]`

## 3. Rule rewrites (12 of the 15 allowed; the rest of section 3 already reads as store-specific)

- **R6.** Once the product clears the price, margin and differentiation gates (R23 to R35), set a launch date: every extra month of research after that is unrecovered fee-stack and carrying cost, not new information.
- **R7.** Reject a clone that cannot win a page-1 price or review fight against the top 10 Amazon listings (R25 to R27); if it cannot name one fixable gap from competitor 1 to 3 star reviews, do not list it.
- **R14.** Open the Amazon account under a business entity with its own EIN and bank account before the first sale, so a personal-account mismatch never blocks payout verification; route entity choice to 20-FIN.
- **R18.** Choose a design (logo) mark over a word mark when the brand name sits on the listing image and packaging, since a denied word mark stalls Brand Registry, A+, Sponsored Brands and hijacker protection on that ASIN, not just the trademark.
- **R22.** Before a production PO to an overseas factory for an Amazon-bound SKU, get a lawyer-reviewed NNN agreement, not a Western NDA, since it protects the SKU that will carry the brand's Amazon listing and reviews; put a provisional patent in the launch budget (P5), not aside.
- **R43.** Confirm the factory's maximum monthly output before setting a launch date, so a fast PPC ramp or rank jump does not outrun supply and trigger the stockout failure mode (R91).
- **R44.** Pay for the printed sample and approve it against the fixes in the product brief from review mining (P4 step G) before ordering the FBA-bound run; a defect that reaches FBA becomes a bad review, not a private return.
- **R45.** Run the third-party inspection, including a barcode scan of the FNSKU and UPC, before releasing the balance and before the stock ships to FBA; an uninspected defect becomes a review problem, not just a wasted purchase.
- **R46.** Pay new Amazon-bound suppliers by a reversible method until trust is established: a dispute over a bad FBA-bound run has no recourse once the goods are checked into Amazon's warehouse.
- **R48.** Choose air or sea freight against the launch date and the PPC budget already committed, not cost alone; a late sea shipment means a live, advertised listing burning cash with no stock.
- **R67.** Keep every carrier receipt and Bill of Lading before handover: it is the only proof Amazon accepts for shipped-vs-received reconciliation (P12) and reimbursement claims (R41).
- **R76.** Recover a stalled launch by reading sessions and unit session percentage (R95) and the search term report, then re-testing images and price; do not relaunch or edit the same ASIN blind.

## 4. Missing store levers (up to 8)

1. **Subscribe & Save mechanics and pricing.** Named once in a Brand Registry benefits list, no enrolment steps or discount rule. Source: `01-amazon-fba-12-hour-course-part2.md`, card area `049d4d03504b`. Goes in a new rule under 3C or 3E, next to Brand Referral Bonus.
2. **Storefront build.** Same one-line mention, no structure or use case, same source file. Goes in a new P3 sub-step, after A+ content.
3. **Coupons, Lightning Deals, Prime Day participation.** No source in this folder, `[general practice]`. Goes in 3I (launch) or a new 3N (promotions).
4. **Amazon DSP or Sponsored Display retargeting.** No source in this folder, `[general practice]`. Goes in 3J next to Sponsored Products, noting it needs separate access.
5. **Seller Fulfilled Prime as a real FBM alternative.** Only a card aside on R2 (`e94ff8c9c6e7`), never a rule. Goes in 3A next to the FBA vs FBM decision (R2).
6. **Price parity with the brand's own DTC store.** No source in this folder, `[general practice]`. Goes in 3E, since undercutting the brand's own site erodes both channels' margin.
7. **Packaging insert or QR code routing Amazon buyers to email or DTC.** No source in this folder, `[general practice]`. Goes in 3I next to the Attribution-link rule (R21), tied to 17-CXP for the insert itself.
8. **Catalogue growth after the first hero SKU.** R73 only says launch one SKU for the first listing; nothing on sequencing a second ASIN once it is proven. No source beyond R73, `[general practice]`. Goes in 3I or a new 3O (portfolio growth).

## 5. Demotions

- **R14** (EIN, seller's permit, separate business bank account): about 90 words in 3B, generic small-business hygiene that reads the same for any company. Keep only the Amazon consequence (a mismatch blocks verification); demote the rest, since entity choice already routes to 20-FIN.
- **R18** (design mark vs word mark): about 90 words in 3C, generic trademark strategy. Keep the Amazon consequence (a denied mark stalls Brand Registry); demote the "which mark type" discussion, since 04-BRD owns trademark strategy.
- **R22** (NNN vs NDA, patent figures): about 130 words in 3C, generic overseas-manufacturing legal advice for any importer, not Amazon mechanics. Demote to an appendix or 18-COG, keep a one-line pointer.
- **Section 7, conflict 11** (when to form an LLC): about 60 words, a generic entity-formation debate the playbook already routes to 20-FIN. Cut to one line.

Estimated total: roughly 350 words moved to a "General background" appendix.

## 6. Deliverables check

The 7 deliverables in section 9 are things an Amazon seller-ops person would actually produce: a channel decision memo, a product screen sheet, a fee and margin model spec, a listing brief, a launch plan, a PPC structure, and a monthly report. None reads as a generic "strategy document." No renames needed. One gap: P17 (replenishment) is a full procedure with a reorder trigger and order size, but section 9 has no standalone deliverable for it, only a mention inside 9.7. Add a short 9.8 replenishment plan (trigger date, order size, cash, lead time).

## 7. The single highest-value change

Add the ranked "3.0 Ecommerce priority order" block drafted in section 2, with store-type conditions filled in once real brand cases exist (a single hero SKU with no cash cushion behaves very differently from a wide catalogue with DTC traffic feeding Brand Referral Bonus). The playbook is a deep, well-sourced reference, but it does not say what to check first when a brand asks "should we add Amazon" or "our margin dropped." A ranked order turns 97 correct rules into a usable sequence, and is the one change that would most separate this from a generic "how Amazon FBA works" prompt.
