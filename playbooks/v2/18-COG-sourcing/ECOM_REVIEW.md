# Ecommerce review: 18-COG-sourcing playbook

Reviewed: `playbooks/v2/18-COG-sourcing/PLAYBOOK.md` (about 19,800 words) against `playbooks/v2/TEMPLATE.md`.

## 1. Ecommerce specificity score: 2 out of 5

The playbook is well built by the template's own rules: every rule traces to a source and card id, conflicts stay open in section 7, and the formulas match 20-FIN so 2 folders agree on 1 number. But it reads like a generic import and manufacturing guide for any physical-goods business, not one written for a store. Of 72 scored decision rules in section 3, only 3 tie their reasoning to what makes a business a store; the other 69 would print identically for a wholesaler, an Amazon-only reseller or a small retail chain.

Counts, out of 72 numbered rules (R1 to R73; R66 is a note, not a rule, and is excluded):

- (a) store-specific: 3 (4%). R20 (landed cost gates "every pricing, ad-spend, go or no-go" decision), R58 (3PL chosen on store-stack integration and Q4 surge history), R72 (COGS framed against CAC as the main lever).
- (b) generic but correctly applied to a store: 28 (39%). All of 3.1 spec/BOM (R1-R9), most of 3.3 quotes (R17-R19, R21, R22), most of 3.6 payment (R40-R42, R44), the QC rules (R48-R50), the reorder/PO rules (R60-R65, R67). Written with "SKU" and "brand", but the content is generic import discipline.
- (c) generic with no store framing: 41 (57%). All of 3.2 supplier vetting (R10-R16), all of 3.4 samples (R23-R29), all of 3.5 negotiation (R30-R39), most of 3.6 financing (R43, R45-R47), all of 3.8 freight (R52-R57), 3PL review cadence (R59), all of 3.11 risk (R68-R71), plus R51 and R73. None mentions a PDP, cart, checkout, offer, ad-driven demand or repeat purchase.
- (d) out of scope for a store: 0. The 1 real risk, 02's sourcing-agency-as-a-business content, is already excluded in section 1.

The 13 formulas follow the same split: F3, F4, F5 and F8 tie to store sales-velocity data; F1, F6, F7, F9-F13 are generic supply-chain and trade-finance math.

## 2. Prioritisation check: no priority block exists

Section 0's "which sections to load" table is task-based, not ranked, and gives no conditions by store type (hero SKU vs catalogue, low vs high AOV, subscription vs one-off, marketplace-heavy, luxury, mobile-first India vs US). No source ranks levers either. Every line below is my ranking, not a source's, so every line is `[general practice]`; rule ids carry the sourced content.

**3.0 Ecommerce priority order**

1. Landed cost before pricing or ad spend (F6, R20, R21): if this number is wrong, whether paid traffic can be profitable is wrong too. `[general practice]`
2. Exact spec and tech pack before factory contact (R1, R2): an open spec becomes an inconsistent PDP photo or a returned order. `[general practice]`
3. Production sample gate, no exception (R24): a mismatch that reaches bulk becomes a customer-facing defect. `[general practice]`
4. Margin gate before scaling a SKU (R22): a thin margin cannot fund the CAC that gets the SKU seen. `[general practice]`
5. Reorder point from real store sales velocity (F3-F5, R60): a stockout on an advertised SKU wastes committed ad spend. `[general practice]`
6. Pre-shipment QC gate before the balance is paid (R48): cheaper than the return, refund and support cost a defect causes later. `[general practice]`
7. Defect buffer from observed rate (F7, R49): keeps the reorder math honest. `[general practice]`
8. Freight mode set against the marketing or launch calendar (R52, R54): a late order forces air right when a launch needs its margin most. `[general practice]`
9. 3PL chosen on Q4 surge history and store-stack integration (R58): a 3PL failure at peak is a checkout failure too. `[general practice]`
10. Payment route matched to supplier proof level (R41, C1): protects deposit cash the store also needs for ads and the next PO. `[general practice]`
11. Supplier and country concentration tracked, backup mapped (F11, R67, R68): a shock in peak season is a stockout risk, not only a cost risk. `[general practice]`
12. Volume price breaks weighed against cash and cover, not unit price alone (R18, R19, F8): a deep discount that locks cash starves the next ad push. `[general practice]`

## 3. Rule rewrites (condition, sources and card ids unchanged)

1. **R11**: a dropped factory leaves the PDP "sold out" while ads keep spending on clicks that cannot convert; vet enough backups before setting a launch date against 1 supplier.
2. **R23**: do not shoot PDP or ad creative, or set a launch date, before a sample from the exact factory is in hand.
3. **R24**: a production sample that slips this gate becomes a customer return and a bad review that raises CAC on future ads for that SKU.
4. **R36**: sell-through is unknown until paid traffic runs against the SKU; pay for resize rights through the first campaigns before locking a volume discount.
5. **R48**: a defect that reaches a customer costs a refund, a return and a support ticket, more than the roughly $200 inspection that would have caught it.
6. **R52**: a scheduled campaign or launch date turns a late order into forced air freight right when the campaign's margin needs protecting.
7. **R53**: planning the next shipment the day the last lands keeps stock in place for promotions already on the marketing calendar.
8. **R41**: the deposit protected here is cash the store also needs for ads and the next reorder.
9. **R68**: a single-country shock during peak season is a stockout on the storefront, not only a cost increase.
10. **R29**: a failed supplier switch shows up as returns and lower ratings before it shows up as a saving; keep the incumbent live until the new rate is proven.
11. **R64**: demand units should reflect the channel plan already committed for that SKU, not only trailing velocity, so sourcing does not under-order into a planned spike.
12. **R10**: the best factory in the category matters most for a SKU carrying real ad spend; a filtered search is a fair floor only for a low-volume or test SKU.
13. **R22**: a SKU cannot fund paid acquisition on a thin margin; check before any bulk order assuming ad-driven volume.
14. **R58**: name the store platform in the ask (order sync, out-of-stock sync to the storefront), not just "confirm integration".
15. **R67**: a concentrated supplier failing during a scheduled promo does more damage than the same failure in a slow month; weigh against the marketing calendar, not only annual COGS share.

## 4. Missing store levers

1. **Backorder or "sold out" PDP handling when the reorder point is missed.** No coverage; would sit in 3.10 near R60/F4. Grep of `sources/`: no hits for "backorder" or "pre-order"; "sold out" appears only in 03's 1 stockout anecdote, already used for R61. `[general practice]`
2. **Subscription or recurring-replenishment cadence versus one-off purchase.** F3-F5 assume simple daily velocity. Grep: 0 hits for "subscri" in any source. `[general practice]`
3. **Hero SKU versus catalogue-wide sourcing investment.** No rule sets which SKUs get a full BOM or backup factory first. Grep: 0 hits for "hero sku" or "catalogue" as a prioritisation idea. `[general practice]`
4. **Seeding or gifting units for content and ad shoots as a demand-plan line.** Not in this folder, but the same source (01) carries influencer cards (for example `5f1f1ab07f4e`) already routed to 10-MCR and 07-LPG; note only, fix belongs at that interface.
5. **De minimis or small-parcel customs thresholds for cross-border direct lanes.** R52 covers mode choice, not the duty-threshold angle. Grep: 0 hits for "de minimis". `[general practice]`
6. **Customer-returned units re-entering the sourcing/QC loop**, distinct from supplier defects (F7) and supplier reclaim (R43). Grep: only 01's supplier-reclaim line touches "return". Thin on both sides of the 17-CXP interface. `[general practice]`
7. **AOV or bundle/kit assumptions feeding order quantity.** R64/P14 take units as given. Grep: 0 hits for "bundle" or "kit". `[general practice]`
8. **Store-type conditions on freight and payment** (luxury/considered-purchase tolerating slow sea freight vs low-AOV impulse needing fast fulfilment). R52 gives a mode rule with no store-type condition. Grep: 0 hits on purchase-consideration level. `[general practice]`

## 5. Demotions to an appendix "General background"

- **R57**, Hong Kong cost-of-living comparison (about 60 words): the playbook itself calls this "not a sourcing number."
- **R45**'s bank/insurer mechanics (Sinosure, Allianz, Bank of China, HSBC premiums and advance rates, about 100 words): keep the 1-line takeaway in 3.6, move the mechanism detail.
- **Conflict C5**, dividend vs reinvest (about 90 words): the playbook itself calls this "finance, not sourcing."
- **Conflict C11**, price-led agency selling (about 40 words): already marked agency-specific and out of scope.
- **R71**, the Bali aside (about 45 words): 1 anecdote about 1 location, not a transferable rule.
- The "personal turnaround" biography under 01 in section 12 (about 40 words): keep the bias disclosure, drop the narrative.

Roughly 350-400 of 19,800 words would move; the base document otherwise stays on-task.

## 6. Deliverables check (section 9)

The 6 deliverables (spec sheet, quote comparison, sample plan, landed cost table, reorder calendar, PO draft) are correctly scoped: sourcing does not produce a PDP brief, offer ladder or creative test plan, and section 1 already routes those to 03-OFF, 07-LPG and 10-MCR. This is not a generic-documents problem. What is missing is the connective tissue to the store-facing side:

- **9.5 Reorder calendar**: add a field flagging marketing or ad ops when a SKU's days of cover drops under its lead time, so spend can be throttled before a stockout. Rename to "Reorder calendar and ad-pacing flag."
- **9.6 PO draft**: add a field tying the required land date to a marketing calendar or launch date, not only the season calendar already in section 2's inputs.

## 7. The single highest-value change

Thread the store consequence through the 41 rules now in bucket (c), the way R20 and R72 already do for pricing and COGS, instead of confining that link to 2 or 3 places. The playbook proves that landed cost gates ad spend and a stockout costs sales, states it once, then reverts to generic import language for vetting, samples, negotiation, freight and diversification, the majority of the document. One sentence per rule tying the consequence to the storefront, a dropped factory means a "sold out" PDP burning ad spend, a failed sample means a return and a lower rating, a late shipment means a missed promo, plus the priority block above, would turn this from a correct general sourcing manual into one that earns its place for a store over a generic prompt.
