# 18-COG Sourcing playbook

version: 2.0-draft  |  date: 24 Sep 2026  |  sources: 4 mini playbooks (4 independent presenters; mini playbook 04 also carries a second voice, a commenter)  |  cards: 82  |  built from: sources/*.md

## 0. How to use this playbook

**Ecommerce first.** This playbook is for stores, not for a wholesaler, an Amazon-only reseller or a small retail chain. Section 3.0 is the ranking: it says which levers to work first and why, in store terms (a stockout that burns ad spend, a defect that raises CAC, a late shipment that misses a promo). Store-type conditions, hero SKU vs catalogue, low vs high AOV, subscription vs one-off, marketplace-heavy, luxury or considered purchase, mobile-first India vs US, decide which rules in the groups below apply and how strictly.

**Who runs it.** The sourcing and supply agent. It owns the product specification and bill of materials, the supplier shortlist and vetting record, the structured quote comparison, the sample plan and sign-off log, the negotiation brief and price-break schedule, the payment-terms and float model, the landed cost per unit, the freight plan, the pre-shipment QC brief, the 3PL evaluation, the reorder point and safety stock per SKU, the demand plan and the purchase order draft.

**The purchase itself stays a human or partner step.** In ecomOS the agent never places an order, sends a deposit, signs a manufacturing agreement, books freight or releases a payment. It produces the spec, the comparison, the plan and the purchase order draft, and hands them to the owner or the sourcing partner with the open decisions marked. Every deliverable in section 9 ends with a "decisions for the owner" block.

**All arithmetic is done in code, never by the model.** Every formula in section 3.0 is written with named variables and units so a developer can implement it. The agent fetches inputs, calls the calculation and reads the result. It never estimates a landed cost, a reorder point or a float in prose. If an input is missing, the output is "unavailable", not 0. Landed cost allocation across SKUs in a shipment follows 20-FIN formula F4 so that the sourcing view and the finance view of COGS agree.

**Which sections to load for which task.**

| task | load |
|---|---|
| Write or review a spec sheet or tech pack | 3.1, P1, checklist 5.1, deliverable 9.1 |
| Build or audit a bill of materials | 3.1, P2, checklist 5.1, 3.12 |
| Find, shortlist and vet suppliers or a sourcing agent | 3.2, P3, checklist 5.2 |
| Request and compare quotes, including volume tiers | 3.3, 3.5, P4, checklist 5.3, deliverable 9.2 |
| Plan and sign off samples | 3.4, P5, P6, checklist 5.4, deliverable 9.3 |
| Negotiate price, price breaks, terms | 3.5, 3.6, P7, P8, section 7 (C7, C8) |
| Payment route, deposit, float, consignment, financing | 3.6, P8, P18, section 7 (C1) |
| Landed cost per unit with duties and defects | 3.0 (F6, F7), 3.3, P9, checklist 5.6, deliverable 9.4 |
| Choose freight and plan lead time | 3.8, P10, section 7 (C2) |
| Pre-shipment QC and defect buffer | 3.7, P11, checklist 5.5, section 7 (C3) |
| Choose or review a 3PL | 3.9, P12 |
| Reorder point, safety stock, weekly forecast | 3.0 (F2 to F5), 3.10, P13, checklist 5.7, deliverable 9.5, section 7 (C4) |
| Demand plan and purchase order draft | 3.10, P14, checklist 5.8, deliverable 9.6 |
| Supplier concentration, country diversification, tariff shock | 3.11, P15, P16, P17 |
| Any point where sources disagree | section 7 |

**Fetch before acting.**

- From brand data: the current spec or tech pack per SKU and its version; the BOM per SKU if one exists; the supplier list with country, years active, certifications, payment terms, lead times and deposit splits; every quote received with date, quantity tier and terms; sample logs and approved reference samples; past inspection reports and defect counts per shipment; freight invoices per shipment with weight, volume and transit days; duty and tax paid per shipment; units sold per SKU per day; on-hand and on-order units per SKU; cash position and the owner's tolerance for cash tied in stock; the owner's stockout tolerance. Full list in section 2 and section 10.
- From the data layer: the store platform's order history for daily sales velocity (03 names Shopify; for Gehna use Metabase dashboard 6), the inventory system, the accounting system for landed cost (20-FIN P4), the spend ledger only if a paid call is involved.
- From the web: current duty and tariff rates for the brand's import lanes, current transit day ranges from a forwarder quote, the current status of ePacket and small-parcel options, the real names of the sourcing-agent platforms mini playbook 03 garbles, current credit-insurance providers and terms, current third-party inspection rates. List in section 10, cadence in section 11.

**Source notes to keep in mind while reading.**

- Every number in the 4 sources is one operator's self-reported figure or a worked example. No source cites a study, an audit or a cross-brand dataset. Every value in section 6 is a flag, not a target, until the brand's own data confirms it.
- Mini playbook 01 is a podcast interview with Roman Khan, who runs a solid-gold and lab-grown-diamond jewelry brand (Linear) and buys DTC brands. His numbers are jewelry-specific unless stated otherwise: factory margin bands, gold melt value enabling consignment, commodity monitoring cadence, financing rates. He discloses ties to products he recommends (a cross-border 3PL, a packaging venture). Marked "(01, jewelry)" wherever it matters.
- Mini playbook 02 is an interview with Isaac, a sourcing agency founder whose entry category is corporate swag (hats, bottles, shirts). His price gap and revenue figures are swag-specific. Marked "(02, corporate swag)" wherever it matters. His spec, sample, leverage and country rules are general.
- Mini playbook 03 is one presenter's video guide (blankets, dog beds) that plugs a paid coaching program. It gives the most complete procedure set: tech pack, Alibaba vetting, structured quotes, sample progression, landed cost lines, freight, QC, 3PL, reorder point. Its numbers are his own businesses or hypotheticals.
- Mini playbook 04 is an anonymous forum post by a US jewelry seller who moved from 500-unit weekly AliExpress batches to a 10,000-unit Alibaba order, plus one commenter who is a US sourcing agent and contract manufacturer. The two disagree on payment route. Marked "(04, jewelry)" and "(04, commenter)".
- Tags: `[verify UI]` for platform steps that change, `[needs brand data: what]` for anything that depends on the brand's own numbers, `[web check: what]` for anything to confirm live.
- Card ids from mini playbook 01 are cited as that file gives them (10 to 13 characters). All others are the first 12 characters of the card id.

## 1. Scope and outcomes

**This folder covers.**

- Product specification: the tech pack, exact measurements, the bill of materials (BOM) to component and sub-vendor level, packaging as a BOM line, reference samples, IP ownership of the spec.
- Supplier discovery, shortlist and vetting: Alibaba as a research tool, outreach volume, video calls, certifications, direct channels, sourcing agents, the curated shortlist per category, backup suppliers.
- Quotes: the structured quote request, volume tiers, comparison on identical terms, factory-direct vs domestic supplier gaps, negotiation of the opening quote.
- Samples: strike-off, pre-production, production sample, apparel grading, reference copies, the test batch for a new supplier.
- Negotiation: leverage from prepared redundancy, growth-partnership framing, volume price breaks as forward credits, sub-vendor pass-through, commodity monitoring, early-run flexibility, the limits of squeezing.
- Payment and float: terms minus lead time, deposit and balance splits, Trade Assurance vs direct transfer, consignment, hybrid cadence, credit insurance, invoice factoring, financing as a BOM line, partner-financed bulk buys.
- Quality: pre-shipment QC, inspection scope, defect buffers sized from observed rates, whether to return or absorb defects.
- Freight: air, sea, hybrid, ePacket, premium courier, forwarder choice, transit day planning, cross-border fulfilment.
- 3PL selection and management.
- Replenishment: daily velocity, total lead time, reorder point, safety stock, the weekly forecast rhythm, the demand plan before a PO, the PO draft.
- Supplier risk: concentration, country of origin, tariff and commodity shocks, country diversification, the supply chain audit on a takeover.

**This folder does not cover.**

- Landed cost allocation across SKUs, COGS recognition, cash conversion cycle, inventory grading and liquidation, the financial side of the demand plan (channel units, media dollars): 20-FIN, formulas F4, F5, F34 and procedures P4, P20 to P24. This playbook produces the inputs and points to those.
- Whether to distribute cash or reinvest it, free cash flow vs EBITDA, dividend recaps: 20-FIN. Mini playbook 01 raises it; section 7 (C5) notes it as finance, not sourcing.
- Hiring, team structure, daily reporting: 21-OPS. Mini playbook 01 carries 15 cards on this; they are listed in its section 9 and not used here.
- Product research and category choice: 01-PRD. Offer design and pricing: 03-OFF. Paid social: 10-MCR. Post-purchase and returns handling with customers: 17-CXP. Amazon-specific inventory and FBA: 22-AMZ.
- Starting a sourcing agency as a business (mini playbook 02, procedures A and F): out of scope for a brand agent, kept only where the tactic transfers to a brand.

**Business measures this domain moves.** Landed cost per unit and product margin (20-FIN CM1), defect rate per shipment and the cost of defects, float days and cash tied in inventory, stockout days and lost sales, supplier concentration share, tariff exposure by country, total lead time in days, freight cost per unit.

## 2. Inputs the agent needs

| input | from where | required or optional | why |
|---|---|---|---|
| Product spec or tech pack per SKU: drawings, materials, GSM, trims, measurements per size, Pantone codes, labels, packaging, care, name, version, date | brand record | required for any supplier contact | Without it the factory decides every open point, often wrongly [b760f0e0abc2] [4047ed4ac497] |
| Approved physical reference sample, its location and its owner | brand record, user | required for samples and QC | Sample and bulk are judged against it [3fe60e173a5f] [8254bc7180c2] |
| BOM per SKU: component, cost, sub-supplier, lead time, country of origin, payment terms, labor and overhead as separate lines, packaging line | brand record | required for negotiation, tariff and concentration work; optional for a first small order | Price breaks, terms and risk all hang off it [6c57759a7fd2] [615c598815] |
| Supplier list: name, country, years active, export markets, certifications (ISO, BSCI), direct contact channel, platform link, status (incumbent, backup, candidate) | brand record | required | Vetting, redundancy and leverage [f841770936e1] [3d269be19e27] [d923141a8806] |
| Every quote received: date, SKU, quantity tier, unit price, MOQ, production days, packaging, payment terms, incoterm, validity | brand record, user | required for comparison | Quotes are only comparable on identical terms [e929a7dceb46] [51903576b417] |
| Sample log: stage, date, supplier, result, deviations, who signed off | brand record | required before bulk | The production sample gate is a hard stop [8254bc7180c2] |
| Inspection reports and defect counts per past shipment | brand record | required for the defect buffer | Buffer is sized from observed quality, not a fixed surplus [bd4fa1a7ea61] |
| Freight invoices per shipment: mode, weight, volume, cost, transit days, forwarder | brand record | required for landed cost and lead time | Transit ranges in the sources are planning defaults only [6e280217d1d8] [e3609fde578c] |
| Duty and tax paid per shipment, HS codes, country of origin | brand record, accounting system | required for landed cost | Duty actually paid, not the tariff rate (20-FIN F4) [c52be45b5fec] |
| Insurance, warehousing, inbound handling, packaging cost per shipment or per unit | brand record, 3PL | required for landed cost | These are the lines that turned a 60% assumed margin into 20% in 03's example [c52be45b5fec] |
| Units sold per SKU per day, with a window long enough to see seasonality | data layer (store platform, Metabase for Gehna) | required for reorder | Daily sales velocity drives the reorder point [8bf409e6c3d5] |
| On-hand units, on-order units, expected receipt dates per SKU | inventory system | required for reorder and PO | Trigger and quantity depend on it [8bf409e6c3d5] |
| Owner's stockout tolerance and safety days per SKU | user | required for safety stock | No source gives a sizing formula [94c5d797f80b] |
| Cash position, acceptable cash tied in stock, deposit capacity | user, 20-FIN | required for PO sizing and terms | Volume discounts are weighed against cash lock-up [51903576b417] [b2b02a1e47e6] |
| Current payment terms and payment cadence per supplier | brand record | required for float | Float = terms minus lead time [520876950b] |
| Category, product weight and volume per unit, fragility | brand record | required for freight choice | Weight and urgency pick the mode [e3609fde578c] |
| Selling season calendar and launch dates | user, marketing calendar | required for freight and reorder timing | Late heavy orders force air cargo [e3609fde578c] |
| Competitor teardown samples and category factory-margin benchmarks | inspiration, web, user | optional, strengthens negotiation | Leverage is prepared before the talk [89a60c40d3] |
| Commodity spot prices for priced inputs (gold, diamonds, chipsets) | web | required only when the BOM has commodity inputs | Supplier markup on spot stays hidden otherwise [2d39c2fabf] |
| Tariff and duty rates by lane and HS code | web | required | Rates move; 01 lived through a roughly 50% India tariff period [b1afff921b] |
| Forwarder quotes with transit days for the lane | web, partner | required for a shipment plan | Sources' day ranges disagree (C2) |

## 3. Decision rules

Every rule states the rule, when it applies, the mini playbooks that support it (by number), any conflict (by section 7 code), and card ids. Where only 1 source supports a rule, the rule says so. Where sources disagree, the strictest condition is kept here and the disagreement is written out in section 7. Section 3.0 is the formula register; rules cite formulas by F number.

### 3.0 Ecommerce priority order

This is ecomOS's own ranking for a store, not a source's ranking. Rule ids and formulas carry the sourced content; every line here is `[general practice]` unless a rule id says otherwise.

1. Landed cost before pricing or ad spend (F6, R20, R21): if this number is wrong, whether paid traffic can be profitable is wrong too. `[general practice]`
2. Exact spec and tech pack before factory contact (R1, R2): an open spec becomes an inconsistent PDP photo or a returned order. `[general practice]`
3. Production sample gate, no exception (R24): a mismatch that reaches bulk becomes a customer-facing defect. `[general practice]`
4. Margin gate before scaling a SKU (R22): a thin margin cannot fund the CAC that gets the SKU seen. `[general practice]`
5. Reorder point from real store sales velocity (F3 to F5, R60): a stockout on an advertised SKU wastes committed ad spend. `[general practice]`
6. Pre-shipment QC gate before the balance is paid (R48): cheaper than the return, refund and support cost a defect causes later. `[general practice]`
7. Defect buffer from observed rate (F7, R49): keeps the reorder math honest. `[general practice]`
8. Freight mode set against the marketing or launch calendar (R52, R54): a late order forces air right when a launch needs its margin most. `[general practice]`
9. 3PL chosen on Q4 surge history and store-stack integration (R58): a 3PL failure at peak is a checkout failure too. `[general practice]`
10. Payment route matched to supplier proof level (R41, C1): protects deposit cash the store also needs for ads and the next PO. `[general practice]`
11. Supplier and country concentration tracked, backup mapped (F11, R67, R68): a shock in peak season is a stockout risk, not only a cost risk. `[general practice]`
12. Volume price breaks weighed against cash and cover, not unit price alone (R18, R19, F8): a deep discount that locks cash starves the next ad push. `[general practice]`

Load this block first; the groups below are the detail.

### 3.0b Formula register

Conventions for the developer. All money in the brand's reporting currency, tax exclusive. All percentages as decimals in code (0.10, not 10). Days are calendar days. Units are sellable units of 1 SKU unless stated. Missing inputs return "unavailable", never 0. Every output carries its input dates and the quote or invoice it came from.

**F1. Float.**
```
float_days = payment_terms_days - production_lead_time_days - float_buffer_days
```
`payment_terms_days` = days from invoice (or goods ready, as the contract states) to the date the brand must pay. `production_lead_time_days` = days from PO release to goods ready, plus logistics days if the contract clock starts before landing (01 uses "production/logistics lead time"). `float_buffer_days` = a brand-set allowance for ordering mistakes such as a wrong size mix, which consume float the nominal formula assumes you have; 01 gives no number `[needs brand data: float buffer]`. Worked example (01): 90-day terms minus 30-day lead time = 60-day float, before buffer. A negative result means the brand self-finances production. Source: 01 only. [520876950b]

**F2. Total lead time.**
```
total_lead_time_days = order_to_production_start_days
                     + production_days
                     + transit_days
                     + clearance_and_inbound_days
```
Clock runs from PO release or deposit paid to the day units are sellable at the warehouse or 3PL (03). `order_to_production_start_days` covers deposit clearance and material buying. `transit_days` comes from the forwarder quote for the chosen mode; the sources' planning defaults are in section 6 and conflict C2. Use actual measured values from the last 3 shipments when they exist `[needs brand data: measured lead time per supplier and lane]`. Source: 03. [8bf409e6c3d5] [6e280217d1d8]

**F3. Daily sales velocity.**
```
daily_sales_velocity[sku] = units_sold[sku, window] / window_days
```
`window_days` is a brand choice per SKU: long enough to smooth noise, short enough to show a trend; 03 says to read it weekly from order history and watch slow movers and seasonal spikes. Report the window with the number. Where a seasonal peak is ahead, compute a second velocity from the same weeks last year and show both; the sources give no seasonal formula `[needs brand data: seasonal index]`. Source: 03. [8bf409e6c3d5] [94c5d797f80b]

**F4. Reorder point.**
```
reorder_point[sku] = daily_sales_velocity[sku] x total_lead_time_days[sku] + safety_stock[sku]
```
Trigger: when `on_hand[sku] + on_order[sku] <= reorder_point[sku]`, the SKU goes on the reorder list for that week's review. Worked example (03): 50 units per day x 60 days + 500 safety stock = 3,500 units. The example inputs are illustrative, not benchmarks. Source: 03 only. [8bf409e6c3d5]

**F5. Safety stock.**
```
safety_stock[sku] = safety_days[sku] x daily_sales_velocity[sku]
```
No source gives a sizing formula. 03 calls it "your insurance buffer" sized to the brand's own spike and delay risk. The days-of-cover form above is an ecomOS convention so the input is 1 number the owner can set per SKU, not a source rule `[needs brand data: safety days per SKU, from stockout tolerance and observed lead-time variance]`. The owner may instead enter `safety_stock` directly in units, as 03's example does (500). Source: 03. [8bf409e6c3d5] [94c5d797f80b]

**F6. Landed cost per unit, and effective landed cost per sellable unit.**
```
landed_cost_unit[sku] = factory_unit_price[sku]
                      + freight_share[sku] / units_received[sku]
                      + duty_and_tax_share[sku] / units_received[sku]
                      + insurance_share[sku] / units_received[sku]
                      + inbound_handling_share[sku] / units_received[sku]
                      + product_packaging_unit[sku]
                      + inspection_share[sku] / units_received[sku]

effective_landed_cost_unit[sku] = landed_cost_unit[sku] x units_received[sku]
                                / (units_received[sku] - defective_units[sku])
                                = landed_cost_unit[sku] / (1 - defect_rate[sku])

defect_rate[sku] = defective_units[sku] / units_received[sku]
```
Shares are allocated across the SKUs in 1 shipment with 1 documented basis (weight, volume, value or units) exactly as 20-FIN F4 does, so both playbooks give the same number. `duty_and_tax_share` is duty actually paid, not the rate. `product_packaging_unit` is the retail box; the shipping carton sits in freight. The `inspection_share` line is the third-party QC fee (about $200 per inspection in 03 and 04) spread over the shipment. The effective cost line is what defects do to margin when the brand absorbs them instead of returning them, which is what 04's author chose (300 defective of 10,000, so defect_rate 0.03 and effective cost 1.031 x landed cost). Sources: 03 lists the lines (product cost, freight, duties and taxes, insurance, warehousing, packaging, fulfillment fees, platform fees, transaction fees, courier); 04 gives the defect case; 01 supplies the BOM view of `factory_unit_price`. [c52be45b5fec] [bd4fa1a7ea61] [6c57759a7fd2]

Keep 2 numbers apart. `landed_cost_unit` is the cost to get stock to the warehouse (inventory cost, 20-FIN F4). Warehousing rent, pick and pack, outbound shipping, payment and platform fees are per-order delivery costs (20-FIN F6) and belong in the delivered-order contribution, not in inventory cost [c52be45b5fec]. 03 lists both sets together as "hidden costs"; this playbook splits them so COGS matches the books.

**F7. Order quantity with a defect buffer.**
```
buffer_rate[sku]      = max(observed_defect_rate[sku], brand_floor_rate[sku])
observed_defect_rate  = sum(defective_units over last N inspected shipments)
                      / sum(units_received over the same shipments)
order_units[sku]      = ceil( demand_units[sku] / (1 - buffer_rate[sku]) )
```
`demand_units` is the planned sellable quantity from the demand plan (P14). `brand_floor_rate` is the owner's minimum buffer for a supplier with no inspection history `[needs brand data: floor rate per supplier]`. 04's author ordered 10% extra on a 10,000-unit jewelry order and saw about 3% defective; the card says to size the allowance from observed quality, not a fixed surplus. 10% is 1 operator's practice on 1 order, not a standard. Source: 04 only. [bd4fa1a7ea61]

**F8. Volume tier comparison and cash locked.**
```
for each tier t:
  unit_price[t], tier_units[t], deposit_share[t], terms_days[t]
  cash_at_deposit[t]     = tier_units[t] x unit_price[t] x deposit_share[t]
  cash_total[t]          = tier_units[t] x unit_price[t]
  days_of_cover[t]       = tier_units[t] x (1 - buffer_rate) / daily_sales_velocity
  landed_cost_unit[t]    = F6 with unit_price[t] and the freight quote for tier_units[t]
  saving_vs_base[t]      = (landed_cost_unit[base] - landed_cost_unit[t]) x tier_units[t]
```
Show every tier side by side with `days_of_cover` and `cash_total`, so the owner sees what the discount costs in cash and in months of stock. 04's author saw $7.80 at 500-unit weekly batches, $4 to $10 across bulk quotes, and $2.00 at 10,000 units (jewelry, 1 case); a $6.00 to $4.80 negotiation saved about $3,500 per order at their volume. Sources: 04, 01 (price breaks per BOM line). [51903576b417] [c7f05c514633] [2cb8e11885]

**F9. Price-break credit check on invoices.**
```
credit_due[line, period] = (cumulative_units[line, period] >= threshold_units[line])
                         ? credit_per_unit[line] x units_invoiced[line, period]
                         : 0
expected_invoice         = sum over lines ( units_invoiced x base_price - credit_due )
variance                 = actual_invoice - expected_invoice
```
Volume price breaks in 01 are forward credits that apply after a written threshold is hit, not retroactive discounts. A non-zero `variance` goes to the ops lead to reconcile line by line. Source: 01 only. [2cb8e11885]

**F10. Financing cost, expressed 3 ways.**
```
financing_cost_per_unit       = annual_financing_cost / annual_units
financing_cost_pct_of_cogs    = annual_financing_cost / annual_cogs
financing_cost_pct_of_revenue = annual_financing_cost / annual_revenue
brand_share_of_financing      = financing_cost_per_unit x brand_split_share
```
01's example: about 5 to 6% of financed COGS per year (about $600,000 on $12M spend), about $6 per unit at 100,000 units per year, projected $4 to $5 per unit at about 20M units; an 80% brand and 20% factory split in 1 negotiated case (01, jewelry, historical, not a quote). Compare `financing_cost_pct_of_revenue` against the brand's other working-capital options (20-FIN 3.14) before treating supplier credit as cheap. Source: 01 only. [8b29d3a119] [63dcc0f46e]

**F11. Supplier and country concentration.**
```
supplier_share[s] = sum(component_cost x annual_units for components bought from s) / annual_cogs
country_share[c]  = sum(component_cost x annual_units for components with origin c) / annual_cogs
```
Computed from the BOM's sub-supplier and country-of-origin columns. 01's own business had about 70% of COGS with 1 supplier that bundles gold and diamond procurement, which it treats as a risk to manage. No source gives a threshold `[needs brand data: concentration limit the owner accepts]`. Source: 01 only. [2d39c2fabf] [b1afff921b]

**F12. Country trade-off.**
```
for each candidate country c:
  lead_time_change_pct[c] = total_lead_time_days[c] / total_lead_time_days[current] - 1
  cost_change_pct[c]      = landed_cost_unit[c] / landed_cost_unit[current] - 1
```
Both inputs come from real quotes and forwarder transit days, with duty at the candidate's rate. 02's illustrative Egypt example: lead time about +30%, cost basis about -30%. The 4 qualitative factors (raw material origin, labor cost, overall taxes, development trajectory) are recorded alongside, not scored. Source: 02 only. [a0d9c84c5f13]

**F13. Factory-direct vs domestic supplier gap (02, corporate swag).**
```
gap_pct     = 1 - factory_direct_landed_unit / domestic_supplier_unit_price
resale_gap  = 1 - proposed_sell_price / domestic_supplier_unit_price
```
02's example: a hat at $12 from a domestic supplier, about $3 factory-direct on Alibaba, resold at about $7, about 30% under the domestic price. This is a swag-agency pricing example; for a brand it is only a sanity check on whether a domestic distributor's price carries a large markup. Source: 02 only. [f759ab73c73c]

### 3.1 Specification and bill of materials

**R1. Lock the spec before any supplier contact, and write every dimension, placement and colour as an exact number, never a descriptive word.** "Centered" becomes "4 inches from the top, 4 inches from the bottom, 2 inches from each side". Every open point in the spec is a decision the factory makes for you, and 03's own blanket shipment arrived in 3 shades of grey and 2 fabric weights because no spec was sent. Condition: every new product and every reorder that has shown inconsistency; applies to every measurement, imprint location and colour reference. Sources: 03, 02. [b760f0e0abc2] [aa2d7527a54d] [4047ed4ac497]

**R2. A tech pack contains: drawings or photos from every angle; exact materials and finishes including GSM, trims and hardware; measurements for every size and variant; colourways with Pantone codes; label, packaging and care instructions; product name, version and date.** Keep it as a living document (03 names Figma, Canva and Notion) so every reorder points at the same version. If nobody in-house can draw it, 03 says an experienced product designer on Upwork built one for about $200 `[web check: current tech pack design rates]`. Condition: any physical product. Source: 03 only for the contents list; 02 agrees on exactness. [b760f0e0abc2] [4047ed4ac497]

**R3. Build a bill of materials per SKU: every component with 6 data points (component cost, sub-supplier, lead time, country of origin, payment terms, labor and overhead as separate lines), plus packaging as its own line.** Do not accept "factory cost" as 1 lump line; it hides where the money and the negotiating room are. 01 says worth the effort at about $1M per year of COGS (about $100,000 per month to the supplier), and some businesses benefit from about $2.5M per year revenue; both are 1 operator's judgment (01, jewelry). 01 claims about 99 of 100 founders it met in acquisitions had no BOM (self-reported). Condition: any brand negotiating price, terms or tariff exposure; a first small test order can run on the tech pack alone. Source: 01 only. [6c57759a7fd2] [615c598815] [215ef9f95360b]

**R4. Verify the BOM physically: disassemble the product with the supplier, test material claims (is "organic cotton" organic), and map the sub-vendor layer beneath the factory (diamonds, gold, zippers, chipsets are bought in, not made).** Labor and overhead are the hardest lines to get; 01 says rapport over time makes the ask possible. Condition: when building or auditing a BOM. Source: 01 only. [6c57759a7fd2] [2d39c2fabf]

**R5. Use a physical reference sample to specify quality the brand already trusts, with the tech pack, and check IP exposure first if the reference is another brand's product.** Send the exact item plus written specs (materials, dimensions, tolerances) to the candidate factory to replicate. Condition: an authorised reference item exists; never copy a branded product's marks or protected design. Source: 02 only. [3fe60e173a5f]

**R6. Keep tech packs, artwork and source files on the brand's side, never only at the factory.** Once at volume, sign a manufacturing agreement and register trademarks. Condition: after a final supplier is chosen; strictest at volume. Source: 03 only. [a09ac2dd3ea0]

**R7. Use the BOM to rethink the product, not only to cut cost: a cheaper input tier, or a premium tier priced above its real cost delta.** Condition: after a component-level BOM exists. Source: 01 only. [31e1f32748]

**R8. Track packaging as its own BOM line and quote it like any component.** 01 says mentees cut packaging cost by more than 50% once it was a real line; his own premium tier packaging runs about $8 to $9 per unit against a $12 figure he calls a "dummy number"; 1 brand reportedly saw about 15% higher LTV after a packaging upgrade (01, jewelry, self-reported, and 01 runs a packaging venture). Condition: any product with retail packaging. Source: 01 only. [215ef9f95360b]

**R9. On a takeover or supply chain audit, ask for the BOM first; if none exists, building it is the first task, before any negotiation.** Then check the country-of-origin and supplier columns for concentration and tariff exposure (F11), and ask when COGS on the SKU last went down; "never" on a mature product means there is room. Condition: acquisitions, new client onboarding, first audit of an existing brand. Source: 01 only. [6c57759a7fd2] [294e057145]

### 3.2 Supplier search, shortlist and vetting

**R10. Treat Alibaba as a research and shortlisting tool, not a decision.** It is fine for pricing, materials and MOQ research. The best factory in the category matters most for a SKU carrying real ad spend; a filtered search is a fair floor only for a low-volume or test SKU. A filtered Alibaba search gets a decent factory, not the best one in the category; the best come from a curated shortlist built over years. Condition: sourcing a new product or category. Sources: 03, 02. [f841770936e1] [f759ab73c73c]

**R11. Message at least 10 to 15 factories, filter to verified suppliers and Trade Assurance, then video call the shortlist and ask to see the facility or sample products.** A dropped factory leaves the PDP "sold out" while ads keep spending on clicks that cannot convert; vet enough backups before setting a launch date against 1 supplier. Drop a candidate for vague answers, poor communication or signs of operating from a home. Verify years active and export markets, and request ISO or BSCI certificates; refusal is a red flag and the source does not proceed without one. Condition: any new supplier search `[verify UI: Alibaba verified supplier and Trade Assurance filters]`. Source: 03 only. [f841770936e1]

**R12. Keep a curated, vetted shortlist per product category, with at least 1 real backup factory per core product, vetted before it is needed.** A backup that exists only as a claim gives no leverage and carries relationship risk if the bluff is called. Condition: every core product; build before the negotiation, not during it. Sources: 02, 01 (redundancy prepared in advance). [f759ab73c73c] [3d269be19e27] [89a60c40d3]

**R13. Secure a direct channel (WhatsApp, WeChat, email) with every supplier at first contact, in addition to platform chat.** 04's author says suppliers go offline on Alibaba chat without notice. A refusal to give a direct contact is itself a diligence flag (04 does not say what to do; treat as a flag). Condition: from first contact. Source: 04 only. [d923141a8806]

**R14. Use a sourcing agent deliberately: when trading-company quotes look inflated, when customisation is needed, or when scaling and a platform that physically inspects factories is worth paying for. Vet the agent before trusting them.** 04 only says "use a better sourcing agent" with no criteria; 03 names 2 inspection platforms whose names are garbled in the transcript `[web check: real names of the sourcing-agent platforms 03 transcribes as "Quimma" and "Easy IMAX"]`. Minimum vetting the sources support: physical sample from the agent's factory (R18), a direct channel (R13), references from brands at similar volume `[needs brand data: agent references]`. Condition: as stated. Sources: 04, 03. [0b6b46366bee] [f841770936e1]

**R15. Do not buy into or open a factory unless there is a specific, unmet engineering or quality gap that off-the-shelf factories cannot fill, and someone is prepared to live on site.** 02 says most people he knows who did this on impulse "failed miserably". Condition: any factory-ownership idea. Source: 02 only. [f759ab73c73c]

**R16. Get quotes from 2 competing supplier channels where possible: factory-direct as well as any domestic distributor, and a manufacturer directly as well as a trading company.** 02's swag example: $12 domestic vs about $3 factory-direct for the same hat (02, corporate swag, F13). 04 says agents can reach the manufacturer and sometimes beat trading-company quotes. Condition: any product the brand buys through an intermediary today. Sources: 02, 04. [f759ab73c73c] [0b6b46366bee]

**R74. Give the hero SKU (the one carrying real ad spend) a full BOM and at least 1 vetted backup factory (R3, R12) before spending that effort on the rest of the catalogue.** No library source; verify against brand data before use. Condition: a catalogue with 1 or a few SKUs carrying most of paid spend. `[general practice]`

### 3.3 Quotes and comparison

**R17. Send the tech pack and request a structured quote: unit cost per SKU and variant, MOQ per SKU, production lead time in days, packaging details, payment terms. Compare suppliers only on identical specs, quantities and delivery terms.** "What's your price" alone gives non-comparable answers and no leverage. Condition: after the shortlist exists, before ordering samples. Source: 03 only. [e929a7dceb46]

**R18. Request quotes at several volume tiers (RFQ) and compare the whole curve, not 1 point; then weigh the lower unit cost against cash tied up and defect risk (F8).** 04's jewelry item: $7.80 at 500-unit batches, $4 to $10 across bulk quotes, $2.00 at 10,000 units. Condition: any bulk order `[verify UI: Alibaba RFQ posting flow]`. Sources: 04, 01 (per-line price breaks). [51903576b417] [2cb8e11885]

**R19. Treat the first quote as an opening position and negotiate before committing volume.** 04's author moved $6.00 to $4.80 per unit, about $3,500 saved per order at their volume (1 case). Condition: any bulk quote. Sources: 04, 02 (show competing quotes), 01 (prepared redundancy). Conflict C7 on tone. [c7f05c514633] [3d269be19e27] [89a60c40d3]

**R20. The decision number is landed cost per unit (F6), never the factory quote.** The ex-factory price covers physical production only. 03's dog bed margin looked like about 60% and was about 20% once freight, duties, insurance, warehousing and fulfillment were added; a hypothetical $40 cost against a $50 target price would need about a $200 price to work. Condition: every pricing, ad-spend, go or no-go and supplier decision. Sources: 03, 01 (BOM as foundation). [c52be45b5fec] [615c598815]

**R21. Run the landed cost and target-price math before manufacturing, not after.** 03 says even larger companies rush from design into production. Feed the result to 20-FIN P17 (waterfall price). Condition: before any PO for a new SKU. Source: 03 only. [c52be45b5fec]

**R22. Confirm the SKU already sells at a healthy margin before scaling it to a bulk order.** A SKU cannot fund paid acquisition on a thin margin; check before any bulk order assuming ad-driven volume. 04's baseline: $7.80 cost against $25.99 retail from 500-unit weekly batches before the 10,000-unit buy. A thin margin means the volume discount may not cover the cash lock-up and defect risk. Condition: any first bulk order on a SKU `[needs brand data: current margin per SKU]`. Source: 04 only. [51903576b417]

### 3.4 Samples

**R23. Never pitch, price or commit a launch date on a factory-made product before inspecting a physical sample from that exact factory, not a sister factory and not the same factory's other product.** Do not shoot PDP or ad creative, or set a launch date, before a sample from the exact factory is in hand. A factory's word on quality is not enough. Condition: any new factory or new product variation, even one similar to an approved SKU. Source: 02. 03 agrees (samples from every supplier still in consideration). [101cb1f841d9] [8254bc7180c2]

**R24. Run the sample progression in order: strike-off (approve materials and prints), pre-production sample (must match the tech pack exactly; the gold-standard reference for bulk), then a production sample built immediately before mass production. If the production sample does not match the pre-production standard, do not proceed to bulk. No exception.** A production sample that slips this gate becomes a customer return and a bad review that raises CAC on future ads for that SKU. For apparel, get multiple pre-production samples to confirm size grading. Condition: every new supplier and every new SKU; strictest gate is the production sample. Source: 03 only for the 3 stages; 02 for the sample-first gate. [8254bc7180c2] [101cb1f841d9]

**R25. Order samples from every supplier still in consideration and score communication and reliability, not only the sample: who follows instructions, who sends updates unprompted.** Condition: final candidate selection. Source: 03 only. [8254bc7180c2]

**R26. Keep 1 approved sample in-house and leave 1 at the factory as its reference copy.** Condition: after pre-production approval. Source: 03 only. [8254bc7180c2]

**R27. Compare the factory's sample directly against the approved reference sample on the attributes the brand cares about, side by side, and record the deviations.** Condition: every sample stage. Sources: 02, 03. [3fe60e173a5f] [8254bc7180c2]

**R28. A good sample is not a guarantee of bulk quality.** 02 flags the false sense of security; 04's test batch and 10,000-unit order both had defects after samples. The answer is the production sample gate (R24) plus pre-shipment QC (R48). Condition: always. Sources: 02, 04, 03. [101cb1f841d9] [bd4fa1a7ea61] [6356c16830fd]

**R29. Do not move volume to a cheaper supplier at once. Keep the incumbent active, place a small test order, inspect the full batch, and shift volume only once the new supplier's defect rate is proven comparable.** A failed supplier switch shows up as returns and lower ratings before it shows up as a saving; keep the incumbent live until the new rate is proven. 04's case: a competitor about 20% cheaper, a 500-unit test order, most units defective, incumbent kept. The 500 units and the 20% trigger are 1 jewelry seller's case, not thresholds. Condition: a competing supplier quotes materially lower. Source: 04 only. [28b7e903d4ef]

### 3.5 Negotiation and volume price breaks

**R30. Prepare leverage before the conversation: an alternate factory independently vetted, competitor samples bought and reverse-engineered, and the category's normal factory margin learned from people who ran procurement at larger comparable brands.** Leverage entered late is hard to recover. If the factory will not move and redundancy exists, be ready to switch; if it does not exist, build it before pushing hard. Condition: any cost-down or terms negotiation. Sources: 01, 02. [89a60c40d3] [3d269be19e27]

**R31. Tell the incumbent factory plainly that you are quoting competitors, and share the competing price where useful, framed as market reality.** Re-quote periodically even with happy long-term suppliers. 02 frames this as his opinion and notes relationship-first buyers disagree; overplaying it with a sole-source supplier you cannot replace is itself a risk. Condition: at least 1 vetted backup exists (R12). Source: 02 only. Conflict C7. [3d269be19e27]

**R32. Frame cost-downs as a shared-growth partnership: name the change ("new ownership, we plan to grow 5x"), say you want the supplier to win too, share the P&L only as percentages ("20% COGS, 40% marketing, 10% profit"), and translate the growth plan into units ("1M units now, 10M by [year]").** Factories respond to units, not marketing language. Offer to share a specific cost (for example financing, R46) to prove it is two-sided. Condition: an ongoing relationship the brand wants to keep. Source: 01 only. Conflict C7. [769835fae6]

**R33. Volume price breaks are forward credits tied to the supplier's fixed-cost utilisation (idle machine time, idle dedicated labor). They apply after an agreed threshold, not retroactively. Get the trigger written into the agreement and reconcile invoices line by line to confirm the credits appear (F9).** Ask the utilisation question per BOM line: how much of your dedicated equipment or labor is idle, and what volume would lower this cost? 01's jewelry example: about $42 per unit of setting, polishing and QC labor with about $2 to $3 per unit of credit possible at higher utilisation. Condition: any BOM line with a volume-sensitive cost. Source: 01 only. [2cb8e11885]

**R34. Ask whether the factory's own sub-vendors give it volume breaks, and negotiate for that saving to pass through.** 01's example: about $1 off per zipper at higher factory volume (garment example). Condition: any component the factory buys in. Source: 01 only. [2cb8e11885]

**R35. Review the BOM with the supplier at least yearly and ask, per line, what volume unlocks the next break. Ask when COGS last declined; "never" on a mature product means there is room.** Condition: every supplier relationship older than 1 year. Source: 01 only. [6c57759a7fd2] [294e057145]

**R36. In the first 1 to 2 production runs, accept a slightly higher unit cost in exchange for flexibility to test, pivot and resize orders. Use those runs to learn sell-through, quality consistency and where delays happen, then negotiate with that data.** Sell-through is unknown until paid traffic runs against the SKU; pay for resize rights through the first campaigns before locking a volume discount. 03's cautionary case: founders who saved about $2 per unit ended up with warehouses of unsold stock. Condition: a new product without sell-through history. Source: 03 only. Conflict C8 with 04's bulk-first path. [acd555dedcb7]

**R37. Do not squeeze a supplier to the point of retaliation: the saving comes back as cheaper materials, skipped QC or slower timelines.** 01's version: once the category margin band is known, offer the top of the band (9%, not 6%, in his jewelry example of a 5 to 9% factory EBITDA margin) while conditions are good, and expect reciprocity in a shock. Condition: any relationship the brand plans to keep. Sources: 03, 01. [acd555dedcb7] [89a60c40d3] [769835fae6]

**R38. Monitor commodity and market-priced inputs (gold, lab-grown diamonds, chipsets) on a cadence, and pull multiple sub-vendor quotes, so the supplier's markup on spot stays visible.** 01 pulls lab-grown diamond quotes from 6 to 7 sub-vendors monthly and uses trade fairs about twice a year to benchmark components (01, jewelry) `[web check: spot prices for the brand's commodity inputs]`. Condition: any BOM line with a public or fast-moving market price. Source: 01 only. [2d39c2fabf]

**R39. Consider buying a concentrated raw material directly and supplying the factory as an assembler only when volume justifies it and the brand can absorb the commodity price risk it takes on.** Condition: a component with a large COGS share (F11) and a public market. Source: 01 only. [2d39c2fabf]

### 3.6 Payment terms, float, payment route and financing

**R40. Evaluate payment terms as float (F1), not as a way to buy more stock. Push for longer terms as track record and volume grow.** 01's own path was net 7 to net 90 over years, with net 180 cited as an extreme others use (01, self-reported). Map the real dates: deposit, production start, ship, land, sellable, processor payout. The paper terms and the actual cash mechanism can differ. Condition: every supplier relationship; strictest for a new supplier, where the terms are whatever is negotiable from the brand's own cash needs (03). Sources: 01, 03. [520876950b] [acd555dedcb7]

**R41. Default payment route for a new or unproven supplier is the platform's protected order route (Alibaba Trade Assurance), with the specification, communication and payment all on-platform. Direct transfer (TT) for a platform discount is allowed only for a supplier the brand has already received compliant bulk from, and only with the owner's sign-off.** The deposit protected here is cash the store also needs for ads and the next reorder. 04's author calls Trade Assurance seamless with a good grievance system; 04's commenter, a sourcing professional, calls the grievance system "a joke" and prefers TT with a negotiated discount, but ties that to his own expertise and supplier confidence. The strictest condition is kept here. Condition: as stated `[verify UI: Trade Assurance order and payment flow]`. Sources: 04 (both voices), 03 (filter to Trade Assurance). Conflict C1. [626f4be665de] [f841770936e1]

**R42. Structure the deposit and balance so the balance is released only after the pre-shipment QC report passes.** 04's commenter cites 30% deposit and 70% before shipment as what clients "normally" pay (1 practitioner, not universal). Condition: every production order. Sources: 03 (release final payment after QC), 04 (split). [6356c16830fd] [b2b02a1e47e6]

**R43. Ask about consignment (pay only when you sell) where the product has reclaim or resale value to the supplier and the fulfilment geography lets the supplier take unsold stock back.** 01's case rests on gold's melt value and a Hong Kong hub for non-US orders (01, jewelry). It is the strongest supplier financing but not generally available, and it depends on an established payment and dispute record. Never present it as a simple ask for a new or small brand. Condition: category with residual value, established relationship. Source: 01 only. [520876950b]

**R44. If full consignment is not available, ask for a hybrid: standard net terms on the invoice, a smaller regular payment cadence in practice (01 pays weekly), and no penalty for the brand's own over-ordering mistakes. Add a buffer to the float assumption for those mistakes (F1).** Condition: established relationship. Source: 01 only. [520876950b]

**R45. Ask the supplier whether it uses export credit insurance (01 names Sinosure and Allianz) and invoice factoring (01 names Bank of China, Agricultural Bank of China, HSBC) to extend terms; understand the brand will be credit-graded A, B or C by an audit firm on management accounts, payment history and past disputes.** 01 was graded C once over an 8 to 9 year old unresolved supplier dispute. Keep books clean, resolve or disclose old disputes, pay on time. Moved to Appendix A: R45's bank and insurer mechanics (premium size, default trigger, advance rate) `[web check: current credit insurance and factoring providers and terms in the supplier's country]`. Condition: a supplier in a country with a credit-insurance ecosystem (01 says China's is especially developed); established relationship. Source: 01 only. [8b29d3a119]

**R46. Make financing cost an explicit, negotiable BOM line ("$6 per unit now, $5 if we double volume"), negotiate a specific split (01's case: 80% brand, 20% factory), and express the cost in currency over the financed period, as a percent of COGS and as a percent of revenue (F10) before calling it cheap. Compare it with other lenders; 01 warns that a growth-linked US inventory lender can run an effective 30 to 40% against a headline of about 10%** `[web check: the lender's name, garbled in the transcript, and its current rate structure]`. Condition: any supplier-financed terms. Source: 01 only. [8b29d3a119] [63dcc0f46e]

**R47. A replenishment SKU with a cash-flow ceiling can be structured as a partner-financed bulk buy: a partner adds capital to lift a recurring order to a full volume tier, the brand keeps paying its usual unit price (04's example: $10 landed) and pays only for units as they are consumed. It needs written inventory ownership and repayment terms.** This is 1 commenter's client example with no legal or accounting detail. Condition: recurring reorders, a trusted partner, documented terms `[needs brand data: partner and legal review]`. Source: 04 (commenter) only. [b2b02a1e47e6]

### 3.7 Quality control and defects

**R48. Book a third-party pre-shipment inspection before the container leaves the factory. Treat it as mandatory. The agent tests random units, checks measurements, packaging and labelling, checks carton weight and photographs everything, flagging small inconsistencies. Problems are fixed by the factory before departure; once goods are on the water they cannot be fixed. Approve or reject on the report; release the balance only on a pass.** A defect that reaches a customer costs a refund, a return and a support ticket, more than the roughly $200 inspection that would have caught it. About $200 per inspection in both 03 and 04 `[web check: current inspection rates]`; 03's $200 against up to $20,000 of problems is an illustration, not a ratio. Condition: every production shipment; the platform does not inspect for you (04: Alibaba is not Amazon). Sources: 03, 04. Conflict C3 on method. [6356c16830fd] [bd4fa1a7ea61]

**R49. Size the defect buffer from observed quality (F7), not a fixed surplus, and order that many extra units.** 04's author ordered 10% extra and saw about 3% defective (300 of 10,000, jewelry, 1 order). With no history, use the owner's floor rate and tighten it after the first inspected shipment. Condition: every bulk order. Source: 04 only. [bd4fa1a7ea61]

**R50. Decide case by case whether to return defective units or absorb them; record the decision and the effective landed cost (F6).** 04's author judged a return of 300 units not worth the time and absorbed the loss. Condition: after any inspection that finds defects above the buffer. Source: 04 only. [bd4fa1a7ea61]

**R51. Run a checklist-style production process before a run ships.** 02's agency runs about 80 checkpoints; only 2 are described (exact spec, sample approval), so the count is a signal that the process is long, not a list to copy. Checklists 5.1 to 5.8 are this playbook's version. Condition: every production run. Source: 02 only. [4047ed4ac497]

**R75. Route a customer-returned unit back through the QC loop as its own category, separate from a supplier defect (F7) or a supplier reclaim (R43): record what failed, whether it is a supplier fault or a fit or expectation problem, and feed a real supplier-fault return into the observed defect rate.** No library source; verify against brand data before use. Condition: any brand with a customer returns flow feeding back to sourcing; coordinate with 17-CXP on the customer-facing side. `[general practice]`

### 3.8 Freight and logistics

**R52. Pick the mode by weight, volume and urgency: air for small, light or urgent batches; sea for heavy or bulky items and scaled restocking; premium courier (FedEx, UPS) for large orders where a good relationship lets you ask for it; small-parcel post (ePacket where it still exists) only for dropship-scale batches.** A scheduled campaign or launch date turns a late order into forced air freight right when the campaign's margin needs protecting. Most brands in 03 hybridise: air a small first batch to start selling, then sea-restock. 04's case: a 1.2 kg stainless-steel item drew an air cargo quote of about $2,000, rejected with Q4 near, and went sea (about 1 month); a large order was upgraded from ePacket (10 to 14 days) to FedEx (4 to 5 days to California) after asking. Condition: every shipment `[web check: current status of ePacket and China to US small-parcel options; 04 says it ended around 2019 from memory]`. Sources: 03, 04. [6e280217d1d8] [e3609fde578c]

**R53. Plan backward from total lead time (F2) and start planning the next shipment the moment the current one lands.** Planning the next shipment the day the last lands keeps stock in place for promotions already on the marketing calendar. 03's planning defaults: sea 30 to 40 days door to door, air 7 to 10 days, production about 20 to 30 days, so about 50 to 70 days combined. 04's observed: sea about 1 month, ePacket 10 to 14 days, FedEx 4 to 5 days. 01 (self-interested): about 4.5 days Hong Kong to a US customer via his cross-border 3PL. Use the forwarder's quote for the lane and measured history over any of these. Condition: every reorder. Sources: 03, 04, 01. Conflict C2. [6e280217d1d8] [e3609fde578c] [1787e284ba5e]

**R54. Order heavy or bulky items well ahead of the selling season so sea freight is possible; a late order forces air cargo or a missed season.** Condition: any item where air cost per unit is material vs landed cost `[needs brand data: season calendar]`. Source: 04 only. [e3609fde578c]

**R55. Use a freight forwarder for container booking, customs and delivery coordination, and do not pick the cheapest quote by default: it may leave goods waiting at port to fill a container.** Condition: any sea shipment. Source: 03 only. [6e280217d1d8]

**R56. Cross-border fulfilment from a hub near the supplier can beat domestic fulfilment on cost and speed for light goods, but verify independently: 01 is an investor in the provider it names.** Condition: light goods, multi-country demand `[web check: independent rates and transit times]`. Source: 01 only. [1787e284ba5e] [ef4169a542a0]

Moved to Appendix A: R57, a near-supplier base and its cost-of-living comparison; the playbook itself calls it not a sourcing number.

**R76. Check the de minimis or small-parcel customs threshold for a cross-border direct-to-customer lane before choosing that lane over a bulk import; it changes the landed cost math and the paperwork, not only the transit day count in R52.** No library source; verify against brand data before use. Condition: any cross-border direct fulfilment lane `[web check: current de minimis thresholds for the brand's lanes]`. `[general practice]`

**R77. Set freight speed and payment cadence by store type: a luxury or considered-purchase SKU can tolerate slow sea freight and longer payment terms; a low-AOV impulse SKU needs fast fulfilment and cannot carry the cash lock-up of the deepest volume tier (F8).** No library source; verify against brand data before use. Condition: choosing a freight mode (R52) or a payment route (R41) for a SKU. `[general practice]`

### 3.9 3PL selection and management

**R58. Choose a 3PL on documented accuracy (order error rate), speed (peak processing and how), communication (a named direct contact) and scalability (documented prior Q4 surges for other brands), never on price or promises. Ask how they handle returns, damages and restocks and whether they flag issues proactively. Visit the warehouse in person; after 2 or 3 tours the real operators stand out. Name the store platform in the ask, order sync and out-of-stock sync to the storefront, not just "confirm integration."** 03's own 3PL collapsed in a Q4 with a $45M to $50M forecast, costing "tens of millions" and public complaints (self-reported). Condition: choosing, replacing or stress-testing a 3PL before a peak. Source: 03 only. [60146e443b29]

**R59. Once running: track inventory turnover weekly, keep a shared dashboard with the warehouse, and hold monthly reviews with the 3PL.** Condition: any 3PL relationship. Source: 03 only. [60146e443b29]

### 3.10 Reorder point, safety stock, forecasting and the purchase order

**R60. Set the reorder point per SKU from daily sales velocity, total lead time and safety stock (F3 to F5), and trigger the reorder when on hand plus on order falls to it.** 03's example: 50 per day x 60 days + 500 = 3,500 units. Condition: every stocked SKU. Source: 03 only. Conflict C4 on method. [8bf409e6c3d5]

**R61. Review velocity, lead time and stock position every week, as a discipline, whatever the team size, and put 1 person on operations and planning if at all possible.** 03's COVID case: sales of about $200,000 per day, sold out within a week with no forecasting, close to 2 months unable to fill orders; his retrospective estimate that the business "could have been 30 to 40% bigger" is his opinion. Condition: any sourced-product business. Source: 03 only. [94c5d797f80b]

**R62. Size safety stock from the brand's own spike and delay risk; no source gives a formula.** Record the days of cover chosen and the reason `[needs brand data: safety days per SKU]`. Condition: every SKU. Source: 03 only. [8bf409e6c3d5]

**R63. Tell suppliers the forecast and stock position before problems appear, not after.** Condition: weekly, or when the forecast moves materially. Source: 03 only. [94c5d797f80b]

**R64. Before any PO larger than a routine reorder, write a demand plan: the velocity and window used, the seasonal view, the days of cover the order buys, the cash it locks at deposit and in total (F8), the defect buffer (F7), the lead time assumed (F2) and the date the stock must land.** Demand units should reflect the channel plan already committed for that SKU, not only trailing velocity, so sourcing does not under-order into a planned spike. The channel split and media dollars behind the demand plan live in 20-FIN P22 and R110; this playbook consumes that plan and does not rebuild it. Condition: every non-routine PO. Sources: 04 (weigh cash and defect risk), 03 (velocity and lead time), 20-FIN (channel plan). [51903576b417] [8bf409e6c3d5]

**R65. The PO draft states: SKU and version of the tech pack, quantity including buffer, unit price and tier, price-break thresholds and credits, deposit and balance split with the QC-pass condition, incoterm and freight mode, production days and required ship date, packaging spec, inspection date and provider, payment route.** Anything not written is a decision left to the factory (R1). Condition: every PO. Sources: 03 (structured quote fields), 01 (written thresholds), 04 (payment route). [e929a7dceb46] [2cb8e11885] [626f4be665de]

**R66. 01 lists a card on moving procurement from weekly to daily purchase orders, but the mini playbook gives no method.** Not turned into a rule; noted so a later source can fill it. Source: 01 (card title only). [cf0394bf6e]

**R78. Give a SKU below its reorder point a "sold out" or "back in stock soon" PDP state instead of hiding it, and flag paid traffic pointing at it so spend can be throttled (see also the reorder calendar and ad-pacing flag, deliverable 9.5).** No library source; verify against brand data before use. Condition: on_hand plus on_order falls below the reorder point (F4) before the reorder is filled. `[general practice]`

**R79. For a subscription or recurring-replenishment SKU, size the reorder point and order quantity from the committed subscriber cadence, not only trailing daily sales velocity (F3 to F5); a one-off purchase SKU can use velocity alone.** No library source; verify against brand data before use. Condition: any SKU sold on a recurring or subscription cadence. `[general practice]`

**R80. Build the demand plan (R64) from the AOV, bundle and kit assumptions the SKU actually sells under, not from single-unit demand; a kit's component units follow the kit's sell-through, not each component's own history.** No library source; verify against brand data before use. Condition: any SKU sold mainly as part of a bundle or kit. `[general practice]`

### 3.11 Supplier risk, concentration, country diversification and shocks

**R67. Compute the share of COGS per supplier and per country from the BOM (F11) and treat a large single share as a risk to manage, by dual sourcing or by bringing the concentrated input in-house (R39).** A concentrated supplier failing during a scheduled promo does more damage than the same failure in a slow month; weigh against the marketing calendar, not only annual COGS share. 01's own case: about 70% of COGS with 1 supplier. No threshold is given. Condition: any brand with a BOM. Source: 01 only. [2d39c2fabf]

**R68. Build sourcing contingencies across more than 1 region so 1 country's disruption does not break the chain.** A single-country shock during peak season is a stockout on the storefront, not only a cost increase. 02 says brands asked for contingencies as standard after COVID. 03 says diversify outside China (Vietnam, India, Turkey) only once the business is "the right size", with no threshold `[needs brand data: order volume and maturity vs the owner's own threshold]`. Strictest kept: have at least 1 backup mapped (R12) in a second country before it is needed, even if volume there is 0. Condition: any single-country supply chain. Sources: 02, 03, 01. Conflict C9. [a0d9c84c5f13] [f841770936e1] [2d39c2fabf]

**R69. Assess a candidate country on 4 factors (raw material origin, labor cost, overall taxes, development trajectory) and run the lead-time vs cost trade-off with real quotes (F12).** 02's illustrative Egypt case: lead time about +30%, cost about -30%; 02 leans to cost but calls that his own call. Candidates named: Vietnam, Cambodia, Sri Lanka, Thailand, Egypt, Pakistan, Northern Africa (02); Vietnam, India, Turkey (03); Thailand (01 moved a line there). No country data beyond Egypt is given `[web check: labor cost, tax, duty and transit for each candidate]`. Condition: diversifying or relocating. Sources: 02, 03, 01. [a0d9c84c5f13] [f841770936e1] [b1afff921b]

**R70. When a tariff, duty or commodity move breaks unit economics: pull the country-of-origin column, decide explicitly to hold volume flat rather than push growth into broken margins, use the pause to ask for a temporary concession if the BOM shows an abnormal supplier margin, give some margin back when the shock eases, and evaluate relocation for the long term.** 01 paused growth about 1 year on an India-made business during a period it describes as roughly 50% tariffs, got a concession from a supplier running about 25 to 35% margin ("abnormal for textiles"), paid more again after, and moved production to Thailand (01, 1 case) `[web check: current tariff rates on the brand's lanes]`. Condition: as stated. Source: 01 only. [b1afff921b]

Moved to Appendix A: R71, the Bali (and similar boutique location) aside on testing vs scaled production.

### 3.12 Where sourcing meets finance

**R72. 01 says COGS, not marketing or overhead, is the biggest controllable lever in a mature physical-goods P&L, because a placed PO cannot be cancelled the way ad spend can, and overhead is sticky.** This is 1 operator's philosophy against mainstream advice that treats CAC as the main lever; the mini playbook says to state it as "the source says". What it means for this agent: the BOM and cost-down work in 3.1 and 3.5 is worth doing at the thresholds in R3. Condition: mature brand with a BOM. Source: 01 only. Conflict C6. [f79ca98129] [615c598815]

**R73. Distributions vs reinvestment, free cash flow vs EBITDA, and the monthly close are finance decisions and live in 20-FIN. This playbook only supplies the working-capital inputs: float days, cash locked in POs, financing cost.** Source: 01 raises it; routed. Conflict C5. [43a500ef77] [25c520ee87]

## 4. Procedures (implementation)

Each procedure names its goal, preconditions, steps with settings, checks, and rollback. The agent stops at every step marked "owner" and hands the deliverable over. It never places an order, pays or books freight.

### P1. Build or review the spec sheet and tech pack (03, 02)

Goal: a spec the factory cannot misread, versioned, owned by the brand.
Preconditions: product drawings or photos, the approved reference sample if one exists, packaging requirements, target materials.
Steps:
1. Create 1 document per SKU with the fields in R2: drawings or photos from every angle; materials and finishes with GSM, trims and hardware; measurements for every size and variant; colourways with Pantone codes; label, packaging and care; product name, version, date.
2. Scan every line for a descriptive word standing in for a number ("centered", "about", "similar to", "standard"). Replace each with an exact measurement, tolerance or code (R1).
3. Add tolerances the brand will accept per measurement `[needs brand data: tolerances]`; the sources say to write exact numbers and do not give tolerance bands.
4. If a reference sample exists, photograph it and reference it by an id in the spec; note its location and who holds it (R5). If the reference is another brand's product, record the IP check before sending it anywhere.
5. If nobody in-house can draw the pack, brief a product designer; 03's example rate is about $200 on Upwork `[web check: current rates]`.
6. Store the pack in the brand's own system (Figma, Canva or Notion in 03) and give it a version number. Every quote, sample and PO cites this version.
Checks: checklist 5.1 passes; the pack has 0 descriptive placement words; version and date are on every page.
Rollback: an inconsistent shipment (03's 3 shades of grey) means the pack was missing or unversioned; fix the pack before the next reorder, not after.

### P2. Build the bill of materials (01)

Goal: a component-level BOM per SKU with the 6 data points and a packaging line.
Preconditions: spec (P1), supplier willing to talk, R3's threshold met or the owner wants it anyway.
Steps:
1. List every physical component of the finished unit (01's ring: diamond, gold, labor, factory overhead, factory margin) plus retail packaging as its own line (R8).
2. For each line capture: component cost, sub-supplier or source, lead time, country of origin, payment terms, labor and overhead as separate lines (R3). Leave a line "unavailable" rather than guessing; note who to ask.
3. Disassemble a unit with the supplier and verify material claims (R4). Record test results.
4. Map the sub-vendor layer: for every bought-in component, who the factory buys it from, and whether that vendor gives the factory volume breaks (R34).
5. For commodity inputs, add a spot-price column and a cadence for re-pulling quotes (01: monthly, 6 to 7 sub-vendors) (R38) `[web check: spot prices]`.
6. Add a financing line if supplier credit is in use (R46) and a country-of-origin summary (F11).
7. Version the BOM with an effective date; review with the supplier at least yearly (R35).
Checks: sum of lines equals the factory quote within an explained variance; every line has a country; no line is a lump "factory cost".
Rollback: if the supplier refuses labor and overhead, keep them as 1 "unavailable" line and revisit as rapport grows (01); do not stop the rest.

### P3. Find, shortlist and vet suppliers (03, 02, 04)

Goal: a scored shortlist of 2 to 3 factories per SKU plus 1 vetted backup per core product.
Preconditions: spec (P1); target MOQ, target price band and quantity tiers; the brand's category and any certification needs.
Steps:
1. Check the brand's curated shortlist first (R12); a factory already vetted in the category skips to step 6.
2. Search Alibaba by exact product type; filter to verified suppliers and Trade Assurance `[verify UI]` (R10, R11). Record 10 to 15 candidates with years active, export markets and listed certifications.
3. Message all of them with the spec version and a structured quote request (P4). Score responsiveness, professionalism and prior similar products; expect drop-off.
4. Video call the responders. Ask to see the facility or sample products. Drop candidates with vague answers, poor communication or a home setup (R11).
5. Request ISO or BSCI certificates and check years active and export countries. No certificate, or refusal, is a drop (R11).
6. Get a direct channel (WhatsApp, WeChat, email) for every remaining candidate (R13). Record refusal as a flag.
7. Where a domestic distributor or trading company is the current source, get a factory-direct or manufacturer quote too (R16).
8. If scaling or the category is hard, consider a sourcing agent or an inspection platform; vet the agent with a sample from the agent's factory, a direct channel and references (R14) `[web check: platform names]`.
9. Write the shortlist record: for each candidate, the scores, the certificates, the channel, the quote, and a backup flag. Mark the incumbent's backup explicitly.
Checks: checklist 5.2 passes for each shortlisted factory; at least 1 backup exists per core product before any negotiation (R30).
Rollback: if fewer than 2 candidates pass, widen the search or add a second country (R68) rather than lowering the bar.

### P4. Request and compare structured quotes, including volume tiers (03, 04, 01, 02)

Goal: a quote comparison on identical terms across suppliers and tiers, with landed cost and cash locked per option.
Preconditions: spec version, shortlist, the quantity tiers the owner wants to see, forwarder quotes per tier, duty rate for the lane.
Steps:
1. Send every shortlisted factory the same spec version and ask, together: unit cost per SKU and variant, MOQ per SKU, production lead time in days, packaging details, payment terms, incoterm, quote validity (R17).
2. Ask each for the same 3 or more quantity tiers, or post an RFQ (R18) `[verify UI: RFQ]`. Record every quote with date and tier.
3. Normalise: same incoterm, same packaging, same tier. Where a supplier quoted a different basis, mark it and do not compare until fixed.
4. For each supplier and tier, compute landed cost per unit (F6) with the forwarder quote and duty rate, then cash at deposit, cash total, days of cover and saving vs base (F8). Arithmetic in code.
5. Add the swag-style sanity check where an intermediary is involved: the gap between the intermediary's price and factory-direct landed cost (F13) (02, corporate swag).
6. Treat the first quote as an opening position (R19). Prepare the negotiation brief (P7) before replying.
7. Present the comparison (deliverable 9.2) with the tier the numbers favour and the tier the cash and the defect risk favour, side by side.
Checks: checklist 5.3 passes; every option shows landed cost, not ex-factory price; every tier shows cash and cover.
Rollback: if the forwarder quote or duty rate is missing, publish landed cost as "unavailable" for that option and say what is missing; never fill it with the factory price.

### P5. Sample plan and sign-off (03, 02)

Goal: signed-off samples through 3 stages, with a reference copy on each side, before any bulk.
Preconditions: spec version, shortlist, the approved reference sample (if any), the brand's acceptance attributes.
Steps:
1. Order samples from every supplier still in consideration (R25). Log the date requested, promised and received, and every unprompted update.
2. Stage 1, strike-off: approve materials, colours and prints against the Pantone codes and material specs. Record deviations.
3. Stage 2, pre-production sample: must match the tech pack exactly. For apparel, order multiple sizes and check grading. Compare side by side with the reference sample (R27). Record every deviation with a photo and a measurement.
4. On approval, keep 1 sample in-house and leave 1 at the factory as its reference (R26). Log both ids and locations.
5. Select the final supplier on sample quality plus the reliability score from step 1.
6. Stage 3, production sample: built immediately before mass production, compared with the approved pre-production sample. Any mismatch is a stop; bulk does not proceed until a new production sample matches (R24). No exception in the source.
7. Hand the sign-off log to the owner with the go or no-go recommendation.
Checks: checklist 5.4 passes at each stage; the production sample matches the pre-production sample on every attribute in the acceptance list.
Rollback: a mismatch at stage 3 goes back to stage 2 with the factory, not forward to bulk. A mismatch discovered in bulk is a QC failure (P11) and a spec or gate failure to fix.

### P6. Test batch for a new or cheaper supplier (04)

Goal: prove a new supplier's defect rate before moving volume.
Preconditions: incumbent still active; the new supplier passed P3 and P5; a test quantity the owner accepts as a loss `[needs brand data: test quantity and acceptable loss]`.
Steps:
1. Keep the incumbent's order unchanged.
2. Place a small test order with the new supplier (04's case: 500 units).
3. Inspect the full test batch, not a sample (R29). Record the defect rate.
4. Compare with the incumbent's observed defect rate (F7 inputs).
5. Shift volume only if the new rate is comparable; otherwise keep the incumbent and record the result on the shortlist.
Checks: defect rate recorded; the comparison is between measured rates, not quotes.
Rollback: 04's case, most of 500 units defective, ends with the incumbent kept and the saving forgone.

### P7. Cost-down negotiation and price-break schedule (01, 02, 03, 04)

Goal: a negotiation brief, and after the talk a written price-break schedule and reconciliation rule.
Preconditions: BOM (P2), at least 1 vetted backup (P3), competitor teardown samples, a category margin benchmark if obtainable, the growth plan in units, the quote comparison (P4).
Steps:
1. Homework (R30): confirm the backup is real and current; list competitor teardown findings; record the category factory-margin band and its source (01's jewelry band: about 5 to 9% EBITDA; do not reuse it for other categories) `[web check: category benchmark]`.
2. Decide the posture with the owner (C7): partnership framing (R32) for a supplier the brand wants to keep; competing-quote framing (R31) where the relationship is transactional or the supplier has been complacent. Never bluff without a real backup.
3. Draft the opening: the change ("new ownership", "we plan to grow 5x"), the P&L in percentages only, the plan in units by year (R32).
4. Go through the BOM line by line. For each line ask what volume unlocks the next break and the utilisation question (R33). For bought-in components, ask about sub-vendor breaks and pass-through (R34).
5. For a new SKU in its first 1 to 2 runs, ask for flexibility (order resizing, pivot rights) rather than the lowest price (R36). For a proven SKU, negotiate the opening quote down (R19).
6. Offer a specific shared cost (for example the financing line, R46) to make it two-sided. Stop short of the point where the supplier would recover the cut through materials, QC or timelines (R37).
7. Write the result: base price per line, threshold units, credit per unit, effective date, forward-only, and the reconciliation rule (F9). Get it into the agreement.
8. Set the reconciliation task: the ops lead checks every invoice against F9 and chases any variance.
9. Diary a yearly BOM review with the supplier (R35).
Checks: every agreed break has a written threshold and a credit; the backup was not burned; the invoice reconciliation runs on the first invoice after the threshold.
Rollback: if the factory will not move and the backup is real, prepare the switch via P5 and P6; if the backup is not real, stop pushing and build it (R30).

### P8. Payment terms, float, payment route and financing (01, 04, 03)

Goal: a terms proposal with float days, a payment route decision, and a financing cost line.
Preconditions: the real date map for the last 2 orders (deposit, production start, ship, land, sellable, payout), current terms, the brand's cash needs from 20-FIN, supplier history.
Steps:
1. Map the dates and compute float (F1) for current and proposed terms, with the owner's buffer for ordering mistakes (R40, R44).
2. Pick the payment route (R41): new or unproven supplier, Trade Assurance with spec, chat and payment on-platform `[verify UI]`; proven supplier, TT for a discount only with owner sign-off and a written order. Record the choice and why (C1).
3. Propose the deposit and balance split with the balance tied to a passed QC report (R42). 04's commenter's 30/70 is 1 practice.
4. For an established supplier, ask about longer net terms (01's path: net 7 to net 90), consignment if the category has reclaim value and the geography allows (R43), and the hybrid weekly cadence (R44).
5. Ask whether the supplier uses credit insurance and factoring (R45). If yes, expect a credit grade; check the brand's books, payment history and open disputes before the audit `[needs brand data: payment history, open disputes]`.
6. Request the financing charge as a separate line, then express it 3 ways (F10) and compare with 20-FIN's financing options (R46). Propose a split.
7. If cash is the ceiling on a recurring SKU, draft the partner-financed structure with ownership and repayment terms for legal review (R47).
8. Hand the terms proposal to the owner. The owner negotiates and signs.
Checks: float is positive after buffer, or the negative float is stated as self-financed; the payment route matches the supplier's proof level; financing cost is shown as percent of revenue.
Rollback: never pay off-platform to unblock a shipment; never clear a payment condition tied to QC.

### P9. Landed cost per unit with duties and defects (03, 04, 01)

Goal: landed cost per unit and effective landed cost per sellable unit per SKU per shipment, tied to invoices, consistent with 20-FIN F4.
Preconditions: factory invoice, freight invoice or quote, duty and tax paid or the current rate and HS code `[web check: duty rate]`, insurance, inbound handling, inspection fee, packaging cost, units received and defective units from the QC report, the allocation basis from the accounting policy `[needs brand data: allocation basis]`.
Steps:
1. Collect every line for the shipment. Mark quoted vs invoiced values.
2. Allocate shipment-level costs to SKUs with the 1 documented basis (20-FIN F4).
3. Compute landed cost per unit (F6). Keep per-order delivery costs out; hand those to 20-FIN F6.
4. Compute defect rate and effective landed cost per sellable unit (F6, second block) once the QC report or the receiving count exists.
5. Compare with the factory quote and show the gap (03's dog bed: about 60% assumed margin to about 20% actual).
6. Feed the result to pricing (20-FIN P17) and to the quote comparison (P4).
7. Version the table with an effective date; recompute when price, freight, FX or duty changes.
Checks: checklist 5.6 passes; the sum of allocated shares equals the shipment invoices; the finance table and this table give the same number.
Rollback: a missing line returns "unavailable" for the SKU, with the missing line named.

### P10. Freight choice and lead-time plan (03, 04)

Goal: a freight recommendation per shipment and a dated lead-time plan.
Preconditions: unit weight and volume, quantity, required land date, forwarder quotes for air and sea with transit days `[web check: forwarder quotes]`, season calendar.
Steps:
1. Compute the shipment's chargeable weight and volume and the required land date from the reorder point or launch.
2. Get air, sea and, where applicable, courier and small-parcel quotes with transit days. Compute freight cost per unit for each.
3. Apply R52: light, small or urgent, air; heavy, bulky or scaled restock, sea; large order with a good relationship, ask for premium courier; hybrid for a launch (air a small first batch, sea the rest).
4. Compute total lead time per option (F2) and the latest PO date that still lands on time. If only air lands on time and its cost per unit is material, show the owner both the air cost and the missed-season cost.
5. Choose the forwarder on service and reliability, not the lowest quote (R55).
6. Diary the next shipment's planning start for the day this one lands (R53).
Checks: the plan shows a dated chain from PO to sellable stock; transit days come from the quote, not from the section 6 defaults, unless no quote exists (then the defaults are marked as such).
Rollback: if the required land date cannot be met by any mode, escalate to the owner with the reorder point that was missed (P13) rather than booking air silently.

### P11. Pre-shipment QC and defect handling (03, 04)

Goal: an inspection booked and a report-based approve or reject before the container leaves.
Preconditions: production complete or near complete, the approved pre-production sample and the spec version, an inspection provider and rate `[web check: current rates]`, the acceptance attributes.
Steps:
1. Book the third-party inspection for the date before container loading (R48). Cost in the sources: about $200.
2. Send the inspector the spec version, the acceptance attributes and photos of the approved sample.
3. Scope: random units tested, measurements, packaging and labelling, carton weight, photographs of everything, small inconsistencies flagged.
4. Read the report. Compute the sampled defect rate and compare with the buffer rate (F7).
5. Pass: approve the shipment and release the balance (R42). Fail: the factory fixes before departure, then re-inspects; never approve after loading.
6. On arrival, reconcile the receiving count and defects with the report; update the observed defect rate for the supplier (F7 inputs).
7. Decide with the owner whether to return or absorb any defects above buffer (R50) and record the effective landed cost (F6).
Checks: checklist 5.5 passes; balance release date is after the pass date.
Rollback: an inspection skipped is a process failure to log; 04's author absorbed 300 of 10,000 after the fact.

### P12. 3PL selection and review (03)

Goal: a scored 3PL evaluation and a running review cadence.
Preconditions: order volume and peak forecast, the store stack, candidate 3PLs.
Steps:
1. Ask each candidate for: order error rate, peak-volume processing speed and method, a named direct contact, documented prior Q4 surges for other brands, returns, damages and restock handling, proactive issue flagging, integration with the store (Shopify and warehouse tools in 03) (R58).
2. Visit 2 or 3 warehouses in person; the owner or a partner does the visit.
3. Score and recommend; the owner signs.
4. Once live: weekly inventory turnover check, a shared dashboard, a monthly review (R59).
Checks: every answer is documented, not promised; the visit confirmed the answers.
Rollback: a 3PL that cannot show surge history before a peak is replaced or backed up before the peak, not during it (03's Q4 case).

### P13. Reorder point, safety stock and the weekly forecast (03)

Goal: a reorder point per SKU, a weekly review, and a reorder calendar.
Preconditions: daily units sold per SKU from the data layer, on-hand and on-order per SKU, measured lead times per supplier and lane, the owner's safety days per SKU.
Steps:
1. Compute daily sales velocity per SKU (F3) with the chosen window; show the window and the same weeks last year if a season is ahead.
2. Compute total lead time per SKU (F2) from measured history; fall back to the section 6 defaults only when no history exists, and say so.
3. Compute safety stock (F5) from the owner's safety days, or take the owner's unit figure.
4. Compute the reorder point (F4) and the trigger state: on hand plus on order vs reorder point.
5. For each SKU, compute days until the trigger at current velocity and the PO date that keeps stock above safety; that is the reorder calendar (deliverable 9.5).
6. Run every week: refresh velocity, flag slow movers and spikes, update lead times from the last landed shipment, re-run F4, and send the supplier the forecast position (R63).
7. Recommend that 1 person owns this rhythm (R61).
Checks: checklist 5.7 passes; every reorder point shows its inputs and dates.
Rollback: a stockout with no trigger fired means an input was stale; fix the window or the lead time, then re-run.

### P14. Demand plan and purchase order draft (03, 04, 01, 20-FIN)

Goal: a demand plan and a PO draft the owner can approve, amend or reject.
Preconditions: the reorder calendar (P13), 20-FIN's demand plan by channel for a non-routine order (20-FIN P22), the quote comparison (P4), the sample sign-off (P5), the terms proposal (P8), the freight plan (P10), the defect buffer (F7).
Steps:
1. State demand units for the horizon: velocity x days of cover the owner wants, adjusted by the channel plan from 20-FIN for launches or pushes.
2. Compute order units with the defect buffer (F7). Round to the supplier's carton or MOQ multiple and show the rounding.
3. Show cash at deposit and total, days of cover and landed cost per unit for the chosen tier (F8), and the float (F1).
4. Check the margin gate (R22) with 20-FIN's contribution view.
5. Draft the PO with every field in R65. Cite the spec version and the approved sample ids.
6. Add the "decisions for the owner" block: tier choice, payment route, freight mode, inspection provider, any unavailable input.
7. Hand over. The owner or partner places the order.
Checks: checklist 5.8 passes; nothing in the PO is descriptive where a number is possible.
Rollback: an unavailable input blocks the PO draft; the agent says which, never fills it.

### P15. Country diversification assessment (02, 03, 01)

Goal: a scored comparison of candidate countries for a product line.
Preconditions: current landed cost and lead time, candidate list, quotes from at least 1 factory per candidate, forwarder transit days, duty rates per origin `[web check: all of these]`.
Steps:
1. List candidates (R69) and record the 4 factors per country: raw material origin, labor cost, overall taxes, development trajectory. If any factor is unknown, the estimate is not reliable yet (02).
2. Get real quotes and transit days; compute F12 per candidate.
3. State which matters more for this product, speed or cost, with the owner (02 leans cost, as his own call).
4. Recommend a contingency country even at 0 volume (R68) and a test order path (P6) for the chosen one.
Checks: every candidate has all 4 factors and both F12 numbers, or is marked incomplete.
Rollback: none; this is analysis.

### P16. Tariff, duty or commodity shock response (01)

Goal: a decision memo within days of a shock.
Preconditions: BOM with country-of-origin (P2), current rates `[web check]`, the P&L view from 20-FIN.
Steps:
1. Compute exposure: country share (F11) and the landed cost change per SKU (F6) at the new rate.
2. If unit economics break, recommend holding volume flat rather than growing into broken margins (R70).
3. Use the pause to ask for a temporary concession where the BOM shows an abnormal supplier margin for the category (01's textile example: about 25 to 35%).
4. Plan the give-back when the shock eases (01 did) and start P15 for relocation.
Checks: the memo shows exposure in currency per unit and per year.
Rollback: none; decisions are the owner's.

### P17. Supply chain audit on a takeover or new client (01)

Goal: a sourcing audit in the first week.
Steps: 1. Ask for the BOM; if none, P2 is the first task (R9). 2. Concentration and country shares (F11). 3. When did COGS last decline per SKU? 4. Terms, float and payment route per supplier (F1, R41). 5. Sample logs and inspection history. 6. Reorder method in use and last stockout. 7. Hand the gap list to the owner with the order of work.
Source: 01 only; marketing-lever checks from the same card belong to 10-MCR. [294e057145] [6c57759a7fd2]

### P18. Consignment or partner-financed bulk ask (01, 04 commenter)

Goal: a written proposal for consignment, hybrid cadence or a partner-financed year's supply.
Preconditions: established supplier, on-time payment history, a product with reclaim value (for consignment), a partner with capital (for the financed structure), legal review available.
Steps: 1. Confirm eligibility (R43, R47). 2. Draft terms: ownership of stock, reclaim rights and geography, payment cadence, repayment schedule, what happens to unsold units. 3. Compute float (F1) and financing cost (F10) under the proposal. 4. Hand to the owner and legal.
Checks: ownership and repayment are written; nothing is verbal.

## 5. Diagnostic checklists

Written so a worker can run them. Source column names the mini playbooks.

### 5.1 Spec and BOM review

| check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| Spec exists before any supplier contact | Look for the spec version on the first message to the factory | Version cited | Contact before spec | Stop outreach; P1 | 03, 02 |
| No descriptive placement or size words | Search the pack for "centered", "about", "similar", "standard", "approx" | 0 hits | Any hit | Replace with exact numbers | 02 |
| All R2 fields present | Tick drawings, materials with GSM, per-size measurements, Pantone, labels, packaging, care, name, version, date | All present | Any missing | Complete before sending | 03 |
| Reference sample identified | Sample id, location, holder recorded; IP check if another brand's product | Recorded | Missing or an unchecked branded item | Record; run the IP check | 02 |
| Version control | Same version cited on quote, sample log and PO | Same | Different or none | Reissue and re-cite | 03 |
| BOM has 6 data points per line and a packaging line | Read each line | Complete, or "unavailable" with an owner named | Lump "factory cost" | P2 | 01 |
| Country of origin per line | Column filled | Filled | Blank | Ask supplier; needed for F11 and tariffs | 01 |
| Commodity lines have a spot column and cadence | Check | Present | Absent | Add; monthly in 01 | 01 |
| Files owned by the brand | Where do the source files live | Brand's system | Only at the factory | Retrieve and store | 03 |

### 5.2 Supplier vetting

| check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| Outreach breadth | Count factories messaged | 10 to 15 or more | 1 to 3 | Widen | 03 |
| Platform filters | Verified supplier and Trade Assurance on `[verify UI]` | Both | Either off | Re-filter | 03 |
| Video call done | Facility or samples shown | Clear answers, professional setup, similar products made before | Vague, poor communication, home setup | Drop | 03 |
| Certificates | ISO or BSCI documents received | Received | Refused or absent | Drop | 03 |
| Years active and export markets | Asked and recorded | Recorded | Unknown | Ask | 03 |
| Direct channel | WhatsApp, WeChat or email obtained | Yes | Refused | Flag; weigh heavily | 04 |
| Physical sample from this exact factory | Sample log | Yes, matches reference | None, or from a sister factory | No pricing or launch commitment until yes | 02 |
| Backup exists per core product | Shortlist record | 1 or more vetted, current | None or a claim | Build before negotiating | 02, 01 |
| Sourcing agent vetted | Sample from the agent's factory, direct channel, references | All 3 | Any missing | Do not route volume through the agent yet | 04, 03 |
| Factory ownership idea | Is there a specific unmet quality gap and someone on site | Yes to both | No | Do not | 02 |

### 5.3 Quote comparison

| check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| Structured fields | Unit cost per SKU and variant, MOQ, production days, packaging, payment terms, incoterm, validity | All | "Price only" | Re-request | 03 |
| Identical basis | Same spec version, tier, incoterm, packaging across suppliers | Same | Differs | Normalise before comparing | 03 |
| Several tiers | 3 or more tiers per supplier | Yes | 1 point | RFQ for tiers | 04 |
| Landed cost computed | F6 per option with forwarder quote and duty | Present | Ex-factory price used | P9 | 03, 01 |
| Cash and cover shown | F8 per tier | Present | Missing | Compute | 04 |
| Intermediary gap | F13 where a distributor is the current source | Known | Unknown | Get factory-direct quote | 02 |
| First quote treated as opening | Negotiation brief exists | Yes | Accepted as is | P7 | 04 |
| Margin gate | Current margin per SKU healthy before bulk | Yes `[needs brand data]` | Thin | Do not scale | 04 |

### 5.4 Sample sign-off

| check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| Strike-off approved | Materials, colours, prints vs Pantone and material spec | Match | Deviation | Rework before PP sample | 03 |
| Pre-production sample matches tech pack exactly | Side-by-side with reference; measurements | Match on all acceptance attributes | Any deviation | Rework; do not select the supplier on it | 03, 02 |
| Apparel grading | Multiple sizes checked | Proportions hold | Off | Regrade | 03 |
| Reference copies | 1 in-house, 1 at factory, ids logged | Both | Either missing | Send or retrieve | 03 |
| Reliability score | Followed instructions, updates unprompted | High | Low | Weigh against sample quality | 03 |
| Production sample matches PP sample | Compared immediately before bulk | Match | Mismatch | Hard stop; no bulk | 03 |
| New cheaper supplier tested | Test batch fully inspected, defect rate vs incumbent | Comparable | Higher | Keep incumbent | 04 |

### 5.5 Pre-shipment QC

| check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| Inspection booked before loading | Date vs container date | Before | After or none | Book; hold loading | 03 |
| Scope complete | Random units, measurements, packaging, labels, carton weight, photos | All | Partial | Extend scope | 03 |
| Sampled defect rate vs buffer | F7 | At or below buffer | Above | Factory fixes before departure; re-inspect | 03, 04 |
| Balance release | Date of release vs pass date | After pass | Before, or on the water | Never release before pass | 03 |
| Receiving reconciliation | Count and defects on arrival vs report | Match | Gap | Update supplier's observed rate; raise with inspector | 04 |
| Return or absorb decision | Recorded with effective landed cost | Recorded | Unrecorded | Record | 04 |

### 5.6 Landed cost check

| check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| All F6 lines present | Factory price, freight, duty and tax paid, insurance, inbound handling, packaging, inspection | All | Any missing | "Unavailable", name the line | 03 |
| Duty is paid amount, not rate | Compare to customs invoice | Paid | Rate x value guessed | Use the invoice | 20-FIN |
| Allocation basis documented | Policy names weight, volume, value or units | 1 basis | None or mixed | Fix with finance | 20-FIN |
| Per-order costs excluded | Pick and pack, outbound shipping, fees not in landed cost | Excluded | Included | Move to 20-FIN F6 | 03 |
| Defect-adjusted cost | Effective landed cost computed when defects absorbed | Present | Missing | Compute | 04 |
| Matches finance table | Same number in 20-FIN P4 | Same | Differs | Reconcile | 20-FIN |
| Recomputed on change | Effective date vs last price, FX, freight, duty change | Current | Stale | Recompute | 03 |

### 5.7 Reorder check

| check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| Velocity window stated | F3 output shows window | Yes | Hidden | Show | 03 |
| Lead time measured | F2 from last 3 shipments | Measured | Section 6 default used | Mark as default; measure | 03 |
| Safety stock owner-set | Days or units recorded with reason | Yes | Guessed | Ask owner | 03 |
| Trigger evaluated | On hand + on order vs F4 | Evaluated weekly | Not run | Run | 03 |
| Weekly review happened | Log | Yes | Skipped | Assign 1 owner | 03 |
| Supplier told the forecast | Message log | Yes | No | Send | 03 |
| Season timing | Heavy items ordered early enough for sea | Yes | Air forced | Pull PO date forward | 04 |

### 5.8 PO draft review

| check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| Spec version and sample ids cited | On the PO | Yes | No | Add | 03 |
| Quantity includes buffer and rounding shown | F7 | Yes | Exact demand | Add buffer | 04 |
| Tier, price, thresholds, credits written | F9 fields | Yes | Verbal | Write | 01 |
| Deposit and balance with QC condition | Terms text | Yes | Balance unconditional | Add condition | 03, 04 |
| Payment route matches supplier proof level | R41 | Yes | TT to a new supplier | Trade Assurance | 04 |
| Freight mode, incoterm, required ship date | P10 | Present | Missing | Add | 03 |
| Inspection date and provider | P11 | Present | Missing | Add | 03 |
| Cash and float shown | F8, F1 | Present | Missing | Compute | 01, 04 |
| Demand plan attached | P14 step 1, 20-FIN P22 for non-routine | Attached | Missing | Attach | 20-FIN |
| Decisions for the owner listed | Block present | Yes | No | Add | ecomOS |

## 6. Thresholds and benchmarks

One table for the folder. Confidence: "1 source, example" means 1 operator's own case; "1 source, rule" means the source states it as a rule; "2 sources" means independent agreement. Category tags mark jewelry (01, 04) and corporate swag (02) figures. None of these is a target until the brand's data confirms it.

| item | value | condition | source | confidence |
|---|---|---|---|---|
| Supplier outreach | 10 to 15 factories messaged | New supplier search | 03 | 1 source, rule |
| Tech pack freelance cost | About $200 | Upwork designer `[web check]` | 03 | 1 source, example |
| BOM worth building | About $1M per year COGS (about $100,000 per month to supplier); some at about $2.5M revenue | Deciding on formal BOM work | 01 (jewelry, own judgment) | 1 source, opinion |
| Founders with no BOM | About 99 of 100 | 01's acquisition dealflow | 01 | 1 source, self-reported |
| Factory EBITDA margin band | About 5 to 9% | Jewelry factories only `[web check per category]` | 01 (jewelry) | 1 source, claim |
| Negotiation posture within band | Offer the top of the band while conditions are good | Ongoing relationship | 01 | 1 source, opinion |
| Labor price-break example | About $42 per unit labor; about $2 to $3 per unit credit at higher utilisation | Linear's BOM | 01 (jewelry) | 1 source, example |
| Sub-vendor pass-through | About $1 per zipper | Garment example | 01 | 1 source, example |
| Single-supplier concentration | About 70% of COGS | 01's own business, flagged as risk | 01 (jewelry) | 1 source, example |
| Commodity re-quote cadence | Monthly, 6 to 7 sub-vendors | Lab-grown diamonds | 01 (jewelry) | 1 source, practice |
| Trade fair cadence | About twice a year | Component benchmarking `[web check per category]` | 01 | 1 source, claim |
| Payment terms progression | Net 7 to net 90 over years; net 180 cited as extreme | Trust and volume built | 01 | 1 source, example |
| Float worked example | 90 day terms - 30 day lead time = 60 days | Illustration of F1 | 01 | 1 source, example |
| Factory financing cost | About 5 to 6% of financed COGS per year; about $6 per unit at 100,000 units per year; projected $4 to $5 at about 20M units | China factory, credit-insurance-backed factoring, historical | 01 (jewelry) | 1 source, example |
| Financing split | 80% brand, 20% factory | 1 negotiated deal | 01 | 1 source, example |
| Credit insurance premium | About $100,000 to $1M+ per year lump sum | Large factory, 100+ brand customers | 01 | 1 source, example |
| Insurer default trigger | Covers once more than 20% of the factory's customer base defaults | Illustrative mechanism | 01 | 1 source, example |
| Factoring advance | About 99 cents on the dollar | China banks named `[web check]` | 01 | 1 source, example |
| US inventory lender effective rate | 30 to 40% effective vs about 10% headline | Growth-linked lender, name garbled `[web check]` | 01 | 1 source, warning |
| Tariff shock | Roughly 50% tariffs; growth paused about 1 year | India-made line, period unspecified `[web check current rates]` | 01 | 1 source, example |
| Textile supplier margin | About 25 to 35% ("abnormal") | Leverage point during the shock | 01 | 1 source, claim |
| Packaging cost | About $8 to $9 per unit premium tier vs a $12 "dummy number"; mentees cut packaging more than 50% | Jewelry packaging | 01 (jewelry) | 1 source, example |
| Packaging LTV lift | About 15% | 1 brand after a packaging upgrade | 01 | 1 source, claim |
| Cross-border delivery | About 4.5 days Hong Kong to US | Light goods; 01 is an investor in the provider | 01 | 1 source, self-interested |
| Factory-direct vs domestic | Hat $12 domestic, about $3 factory-direct, resold about $7, about 30% under | Corporate swag | 02 (corporate swag) | 1 source, example |
| Corporate swag spend | About $100,000 to $200,000 per year per mid-size business | Agency prospecting | 02 (corporate swag) | 1 source, estimate |
| Production checklist length | About 80 checkpoints | 02's agency, not itemised | 02 | 1 source, count only |
| Country trade-off | Egypt: lead time about +30%, cost about -30% | Illustrative | 02 | 1 source, example |
| Pre-shipment inspection cost | About $200 | Third-party inspection `[web check]` | 03, 04 | 2 sources, example |
| QC value framing | $200 vs up to $20,000 of problems | Illustration | 03 | 1 source, illustration |
| Air transit | 7 to 10 days door to door | Small or urgent | 03 | 1 source, estimate (C2) |
| Sea transit | 30 to 40 days door to door (03); about 1 month (04) | Standard restock | 03, 04 | 2 sources, roughly agree (C2) |
| Production time | About 20 to 30 days | Added to transit | 03 | 1 source, estimate |
| Production plus transit | About 50 to 70 days | Justifies planning the next shipment on landing | 03 | 1 source, estimate |
| ePacket transit | 10 to 14 days | Small parcel, status uncertain `[web check]` | 04 | 1 source, example |
| Premium courier transit | 4 to 5 days to California | Large order, good relationship | 04 | 1 source, example |
| Air cargo quote | About $2,000 | 1.2 kg stainless item, rush near Q4 | 04 | 1 source, example |
| Reorder point example | 50 per day x 60 days + 500 = 3,500 units | Illustration of F4 | 03 | 1 source, example |
| Early-run price premium warning | About $2 per unit saved led to unsold stock | Cautionary, not an acceptable premium | 03 | 1 source, anecdote |
| Margin erosion | About 60% assumed to about 20% actual | Dog bed, after landed lines | 03 | 1 source, example |
| Price illustration | $40 cost vs $50 target needs about $200 price | Hypothetical | 03 | 1 source, illustration |
| Q4 3PL failure | $45M to $50M forecast; "tens of millions" lost | 03's own peak | 03 | 1 source, self-reported |
| COVID stockout | About $200,000 per day; sold out in a week; about 2 months short | 03's own | 03 | 1 source, self-reported |
| Ops planning upside | "30 to 40% bigger" | 03's opinion about his own business | 03 | 1 source, opinion |
| Small-batch baseline | $7.80 cost, $25.99 retail | 500-unit weekly AliExpress batches | 04 (jewelry) | 1 source, example |
| Volume price curve | $4 to $10 across tiers; $2.00 at 10,000 units | Alibaba RFQ, same item | 04 (jewelry) | 1 source, example |
| Negotiated drop | $6.00 to $4.80; about $3,500 saved per order | Direct negotiation | 04 (jewelry) | 1 source, example |
| Defect buffer | Order 10% extra | 04's practice on 1 order | 04 (jewelry) | 1 source, practice |
| Observed defect rate | About 300 of 10,000 (3%) | 1 bulk order | 04 (jewelry) | 1 source, example |
| Test batch | 500 units; triggered by about 20% lower quote; most defective | New supplier test | 04 (jewelry) | 1 source, example |
| Deposit and balance | 30% deposit, 70% before shipment | What the commenter's clients "normally" pay | 04 (commenter) | 1 source, practice |
| Partner-financed landed cost | About $10 per unit, several reorders per year | Commenter's client | 04 (commenter) | 1 source, example |

## 7. Where sources disagree

**C1. Trade Assurance vs direct transfer (TT).** 04's author: always pay through Alibaba's protected route; seamless, good grievance handling; never PayPal, WeChat or a direct wire. 04's commenter (a US sourcing agent and contract manufacturer): the grievance system "is a joke"; he pays by TT and negotiates the platform fee away, but says that rests on his expertise and confidence in the suppliers he picks. 03 filters to Trade Assurance suppliers at the shortlist stage but says nothing about paying. When each is right: the author's default fits a buyer without sourcing depth or supplier history; the commenter's fits a professional with proven suppliers and the capacity to absorb a loss. What the agent does: R41. Trade Assurance for any supplier without compliant bulk history; TT only for a proven supplier, only for a discount worth the risk, only with owner sign-off, and never as a workaround to speed a shipment. Record the route on every PO. [626f4be665de] [f841770936e1]

**C2. Freight day ranges.** 03: air 7 to 10 days door to door, sea 30 to 40, production 20 to 30, about 50 to 70 combined. 04: sea about 1 month, ePacket 10 to 14 days, FedEx 4 to 5 days to California, and ePacket possibly gone. 01: about 4.5 days Hong Kong to a US customer via a provider he invests in. The ranges are close on sea and differ on what "air" means (cargo vs courier vs post). None is a measurement across lanes. What the agent does: transit days come from the forwarder quote and from the brand's last 3 shipments (F2); the section 6 ranges are planning defaults used only when nothing else exists and are labelled as such in every output. [6e280217d1d8] [e3609fde578c] [1787e284ba5e]

**C3. QC method and cost.** 03: a third-party inspection of random units at the factory before the container leaves, about $200, with the balance released on a pass; once on the water nothing can be fixed. 04: the buyer must inspect because the platform does not; the author inspected after arrival, found 300 defects in 10,000, absorbed them, and cites about $200 for a third party "when self-inspection is impractical". Both put the cost at about $200, so the disagreement is on timing and method, not price: before departure by a third party (03) vs after arrival by the buyer (04). What the agent does: R48 keeps the strictest, a pre-shipment third-party inspection with the balance tied to it, and P11 step 6 adds 04's receiving reconciliation so the observed defect rate feeds the buffer. Self-inspection alone is acceptable only for a test batch (P6), where the whole batch is checked. [6356c16830fd] [bd4fa1a7ea61]

**C4. Reorder method.** 03: a computed reorder point (velocity x total lead time + safety stock), reviewed weekly. 04: the author ran small weekly batches, then a single 10,000-unit bulk buy sized by the volume discount, cash lock-up and defect risk, with heavy items ordered ahead of the season. 01: consignment or hybrid weekly payment that removes much of the reorder problem for an established supplier, and a card title on moving from weekly to daily POs with no method given. When each is right: 03's formula fits any stocked SKU with sales history; 04's cash-first sizing fits the first bulk buy and any cash-constrained brand; 01's fits an established relationship in a category with reclaim value. What the agent does: F4 is the trigger for every SKU; F8 sizes the quantity with cash and cover shown; consignment or hybrid cadence is proposed only where R43 and R44 apply. The daily-PO idea stays unimplemented until a source gives the method (R66). [8bf409e6c3d5] [51903576b417] [520876950b] [cf0394bf6e]

**C5.** Moved to Appendix A: the dividend-first vs reinvest conflict; the playbook itself calls it finance, not sourcing. What the agent does: nothing here; the sourcing agent supplies float days, cash locked and financing cost, and 20-FIN decides.

**C6. COGS as the biggest lever.** 01 says COGS and supplier terms are the largest controllable lever in a mature physical-goods P&L. Mainstream advice, and 03's framing, treat landed cost as the number to get right and marketing efficiency as the lever to work; 02 treats finding the best factory as the moat. No source measures it across brands. When each is right: 01's claim needs a mature brand with real volume (its own R3 thresholds) and a BOM; a small brand's biggest lever is usually elsewhere. What the agent does: state it as "01 says"; run the BOM and cost-down work at R3's thresholds; never claim a COGS saving that the reconciliation (F9) has not shown on an invoice. [f79ca98129] [615c598815] [c52be45b5fec] [f759ab73c73c]

**C7. How hard to push a supplier.** 02: tell the factory you are quoting competitors and show the price; silence is the risk. 01: frame as a shared-growth partnership, share the P&L in percentages, offer the top of the margin band in good times. 03: do not squeeze to the point of retaliation; the saving comes back as worse materials, skipped QC or delays. 02 itself notes relationship-first buyers disagree and that overplaying a sole-source supplier is a risk. When each is right: 02's for a transactional or complacent supplier with a real backup in hand; 01's for a strategic supplier the brand wants for years; 03's limit applies in both. What the agent does: P7 step 2 sets the posture with the owner; R30's redundancy is required either way; R37's limit is always on. [3d269be19e27] [769835fae6] [acd555dedcb7]

**C8. Early runs: flexibility vs bulk price.** 03: pay slightly more in the first 1 to 2 runs for the right to resize and pivot; founders who saved about $2 per unit ended with unsold stock. 04: negotiate the first quote down and, once margin is proven, take the 10,000-unit tier at $2.00. These are different stages: 04's author had 500-unit weekly batches selling at $25.99 before the bulk buy. What the agent does: a SKU with no sell-through history follows R36; a SKU with proven margin (R22) follows R18 and R19 with F8's cash and cover shown. Never take the deepest tier on an unproven SKU. [acd555dedcb7] [51903576b417] [c7f05c514633]

**C9. When to diversify country.** 02: build contingencies across regions as standard after COVID, and lean to cost over speed. 03: diversify outside China only at "the right size", undefined. 01: relocated a line to Thailand after a tariff shock, and treats concentration as a risk to manage. What the agent does: R68's strictest reading, a mapped backup in a second country before it is needed at any size; a real second-country production line only when the owner's volume threshold (unstated by 03) and F12 justify it. [a0d9c84c5f13] [f841770936e1] [b1afff921b]

**C10. Sourcing agent value.** 04: agents reach the manufacturer, arrange customisation and can beat trading-company quotes, but "use a better" one with no criteria. 02 (an agent): the scarce skill is knowing the best factory per category, built over years. 03: a platform that inspects factories is worth it when scaling. No source gives a vetting checklist. What the agent does: R14's minimum vetting, built from the sources' other rules, and a `[needs brand data: agent references]` tag; never route volume through an unvetted agent. [0b6b46366bee] [f759ab73c73c] [f841770936e1]

Moved to Appendix A: C11, the price-led-selling tension; already agency-specific and out of scope for a brand agent.

## 8. Common mistakes

Merged from all 4 sources, deduplicated, with the fix.

1. Contacting a factory before the spec is locked, or with descriptive words instead of numbers; the factory decides and often decides wrong (03, 02). Fix: P1, checklist 5.1.
2. No BOM, or "factory cost" as 1 line, so nobody knows where the money or the room is (01). Fix: P2.
3. Clicking the first professional-looking Alibaba listing instead of shortlisting 10 to 15 and vetting them (03); assuming a filtered search finds the best factory (02). Fix: P3.
4. Committing a price or a launch date before a physical sample from that exact factory (02); treating a good sample as a bulk guarantee (02, 04). Fix: P5, P11.
5. Switching the whole order to a cheaper supplier without a test batch (04). Fix: P6.
6. Using the ex-factory quote as the margin number; rushing from design into production without the landed math (03). Fix: P9, R21.
7. Chasing the lowest unit cost on early runs and trapping cash in unsold stock (03); taking the deepest tier before the SKU's margin is proven (04's own order of events). Fix: R36, R22, F8.
8. Squeezing a supplier until it recovers the cut in materials, QC or timing (03); bluffing about backups without one (02); entering without redundancy (01). Fix: P7 step 1 and 2, R37.
9. Agreeing price breaks verbally, so credits never appear on invoices (01). Fix: F9, P7 step 7 and 8.
10. Ignoring the sub-vendor layer and its volume breaks (01). Fix: P2 step 4, R34.
11. Confusing paper terms with real cash timing; ignoring the float that ordering mistakes eat (01). Fix: F1 with buffer, P8 step 1.
12. Taking a supplier financing rate at face value without expressing it as a percent of revenue and comparing lenders (01). Fix: F10, R46.
13. Paying off-platform to a new supplier for a discount (04 author's warning) or, the reverse, trusting the platform to inspect for you (04). Fix: R41, R48.
14. Ordering the exact quantity with no defect buffer, or a fixed buffer with no observed rate (04). Fix: F7.
15. Letting a container leave without inspection; approving once on the water; releasing the balance before the pass (03). Fix: P11.
16. Picking the cheapest forwarder and having goods sit at port (03); committing a heavy item late and being forced into air cargo (04). Fix: R55, R54, P10.
17. Choosing a 3PL on price or promises, no visit, no surge history (03). Fix: P12.
18. No forecasting rhythm and nobody owning stock levels; a stockout in the middle of a demand spike (03). Fix: P13, R61.
19. Relying only on platform chat and losing the supplier mid-order (04). Fix: R13.
20. Not tracking country of origin until a tariff hits; growing into broken margins (01). Fix: F11, P16.
21. Scaling production in a boutique location that was good for testing (02's Bali). Fix: R71.
22. Buying or opening a factory without a specific unmet gap (02). Fix: R15.
23. Letting the factory be the only holder of tech packs, artwork and source files (03). Fix: R6.
24. Reverse-engineering a branded reference sample without an IP check (02). Fix: R5.
25. Treating any figure in section 6 as a benchmark; every one is 1 operator's case. Fix: replace with the brand's own data as it arrives.

## 9. Deliverables

Every deliverable is produced by the agent, arithmetic in code, and ends with a "decisions for the owner" block and a list of unavailable inputs. The owner or partner acts; the agent does not order, pay or book.

**9.1 Spec sheet (tech pack).** 1 document per SKU: name, version, date; drawings or photos from every angle; materials and finishes with GSM, trims, hardware; measurements per size and variant with tolerances; Pantone colourways; label, packaging, care; reference sample id and location; IP check note. Format: the brand's living document (Figma, Canva, Notion) plus a PDF snapshot per version. Checklist 5.1 attached.

**9.2 Quote comparison.** One table: supplier, quote date, spec version, tier units, ex-factory unit price, MOQ, production days, packaging, payment terms, incoterm, validity, freight quote and mode, duty rate, landed cost per unit (F6), effective landed cost at the buffer rate, cash at deposit, cash total, days of cover, saving vs base (F8), vetting score, backup flag. Below it: the negotiation brief (P7 steps 1 to 3) and the tier the numbers favour vs the tier cash favours. Format: spreadsheet or JSON plus a 1-page summary. Checklist 5.3 attached.

**9.3 Sample plan.** Per supplier: the 3 stages with requested, promised and received dates; acceptance attributes; deviations with photos and measurements; reference copy ids and locations; reliability notes; sign-off names; the go or no-go recommendation. Format: log table plus photos. Checklist 5.4 attached.

**9.4 Landed cost per unit.** Per SKU per shipment: every F6 line with quoted vs invoiced values, allocation basis, units received, defective units, defect rate, landed cost, effective landed cost, gap to ex-factory price, effective date. Format: versioned table shared with 20-FIN P4. Checklist 5.6 attached.

**9.5 Reorder calendar and ad-pacing flag.** Per SKU: velocity and window, total lead time and its parts, safety days and units, reorder point, on hand, on order, days to trigger, latest PO date, required land date, recommended freight mode. A flag to marketing or ad ops when a SKU's days of cover drops under its total lead time, so spend can be throttled before a stockout. Refreshed weekly with the change log. Format: table plus a dated calendar view. Checklist 5.7 attached.

**9.6 Purchase order draft.** All R65 fields: supplier, spec version, approved sample ids, SKUs and variants, quantity with buffer and rounding, tier and unit price, price-break thresholds and credits, deposit and balance with the QC-pass condition, payment route, incoterm, freight mode, production days, required ship and land dates, packaging spec, inspection date and provider, cash at deposit and total, float days, and the required land date against the marketing calendar or launch date (not only the season calendar in section 2), flagged if the plan cannot meet it. Attached: the demand plan (P14 step 1 and 20-FIN P22 for non-routine orders). Format: PO document plus JSON. Checklist 5.8 attached. Status "draft, not placed" until the owner acts.

Also produced on request: supplier shortlist record (P3 step 9), negotiation brief and price-break schedule (P7), terms proposal (P8), freight plan (P10), QC brief and report reconciliation (P11), 3PL evaluation (P12), country comparison (P15), shock memo (P16), audit gap list (P17), consignment or partner-finance proposal (P18).

## 10. What needs live data or a web check

**Needs brand data.**

- Spec: tolerances per measurement; reference sample id, location and IP status (P1).
- BOM: component costs, sub-suppliers, lead times, countries, terms, labor and overhead; packaging cost; the allocation basis in the accounting policy (P2, P9).
- Suppliers: certifications, years active, export markets, direct channels, agent references (R11, R13, R14).
- Quotes: every quote with date and tier; the current margin per SKU before scaling (R22); the owner's cash ceiling and deposit capacity (F8).
- Samples: acceptance attributes; the test batch quantity and acceptable loss (P6).
- QC: inspection history and defect counts per shipment; the floor buffer rate per supplier (F7); the return-or-absorb decision (R50).
- Freight: unit weight and volume; measured transit and production days from the last 3 shipments per lane (F2); the season calendar (R54).
- Reorder: daily units sold per SKU and the window; on hand and on order; safety days per SKU or safety units; a seasonal index if used (F3 to F5).
- Terms: real date map per order; float buffer days; payment history and open disputes before a credit audit; partner and legal review for a financed structure (F1, R45, R47).
- Risk: the concentration share the owner accepts (F11); the owner's volume threshold for a second production country (R68).
- Thresholds: 03's "right size" for diversification, 04's 10% buffer and 500-unit test, 01's BOM thresholds all need the brand's own numbers before use.

**Web check.**

- Duty and tariff rates by lane and HS code; the current status of the India tariffs 01 describes (R70, P9).
- Forwarder quotes and transit days per lane and mode; the current status of ePacket and China to US small-parcel options (R52, R53).
- Third-party inspection rates (R48).
- Tech pack designer rates (R2).
- The real names of the sourcing-agent and inspection platforms 03 transcribes as "Quimma" and "Easy IMAX" (R14).
- Credit insurers and factoring banks and their current terms in the supplier's country; the name and rate structure of the US inventory lender 01's transcript garbles (R45, R46).
- Spot prices for commodity inputs in the BOM (R38).
- Category factory-margin benchmarks (R30); trade-fair calendar for the category (R38).
- Labor cost, taxes, duty and transit for each candidate country (R69).
- Independent rates and transit for any cross-border 3PL 01 recommends (R56).
- Alibaba UI: verified supplier and Trade Assurance filters, RFQ posting, Trade Assurance order and payment flow `[verify UI]` (R11, R18, R41).

## 11. Freshness and stale-risk notes

| item | why it goes stale | re-verify |
|---|---|---|
| Tariff and duty rates (R70, F6) | 01 describes a roughly 50% India tariff period that then ended; rates move with trade policy | Before every PO and every landed cost version; at least monthly for active lanes |
| Transit day ranges (R53, section 6) | Shipping routes, port congestion and carrier capacity change; the sources' ranges are 2024 to 2026 snapshots | Every shipment from the forwarder quote; refresh measured history quarterly |
| ePacket and small-parcel options (R52) | 04 says ePacket ended around 2019 from memory; carrier programs change | Before any small-parcel plan |
| Alibaba features: verified supplier, Trade Assurance, RFQ, payment flow (R11, R18, R41) | Platform UI and protections change; 04's dispute-handling claims are opinions from an unknown date | Each time the procedure runs `[verify UI]` |
| Insurer and bank names: Sinosure, Allianz, Bank of China, Agricultural Bank of China, HSBC (R45) | Providers, eligibility and terms change; 01's figures are historical | Before proposing supplier financing |
| Inventory lender rates (R46) | 01's 30 to 40% effective vs 10% headline is 1 warning with a garbled name | Before comparing with supplier credit |
| Inspection and tech pack rates (R48, R2) | $200 examples from 2 sources of unknown date | Before booking |
| Commodity prices (R38) | Gold moved from about $2,000 to $5,000 in 01's 18-month window | Monthly, or per 01's cadence for the input |
| Factory margin bands (R30, R37) | 01's 5 to 9% is jewelry and self-claimed | Per category, from a fresh benchmark |
| Country candidates (R69) | Labor cost, taxes and development trajectory move; 02's Egypt figures are illustrative | Per assessment |
| Sourcing-agent platforms (R14) | Names unconfirmed; services change | Before recommending one |
| Payment terms norms (R40, R42) | 01's net 7 to net 90 path and 04's 30/70 split are single cases | Per supplier, from the actual negotiation |
| Reorder inputs (F2 to F5) | Velocity and lead times drift weekly | Weekly (R61) |

**Revision log.** 24 Sep 2026: ecommerce specificity pass applied from ECOM_REVIEW.md; priority block added, 15 rules reworded, 7 levers added, about 220 words moved to Appendix A.

## 12. Source index

| no. | title | type | credibility and bias | contributed most |
|---|---|---|---|---|
| 01 | He Went From $3M In Debt To $13M In Cash Using This Playbook | Podcast interview, 37,786 words, 54 cards (about 15 used here; the rest belong to 20-FIN, 21-OPS, 07-LPG, 10-MCR) | Roman Khan, jewelry brand owner (Linear) and DTC acquirer; all figures self-reported and unaudited; discloses ties to a cross-border 3PL, a packaging venture and other sponsors; jewelry-specific on margins, consignment and financing. Strong on mechanism, weak on transferability | BOM to sub-vendor level (R3, R4, R8, R9), negotiation from redundancy and partnership (R30, R32), forward price-break credits and reconciliation (R33, F9), float (F1), consignment and hybrid cadence (R43, R44), credit insurance and factoring (R45, R46, F10), concentration and tariff response (F11, R67, R70) |
| 02 | How He Makes Millions Sourcing Products From China | Interview, 4,282 words, 6 cards | Isaac, sourcing agency founder; corporate swag entry point; all figures self-reported; secondhand anecdotes about other agents; sells sourcing services, so the "curated shortlist takes years" framing favours agencies | Exact measurements in specs (R1), reference sample with IP check (R5), sample-first gate (R23), backup quotes as leverage (R31), curated shortlist (R12), 4-factor country trade-off (R69, F12), factory-ownership warning (R15), Bali test-vs-scale (R71) |
| 03 | The Ultimate Guide To Product Sourcing In 2026 | Video guide transcript, 4,071 words, 13 cards | 1 presenter (blankets, dog beds); plugs a paid coaching program; numbers are his own businesses or hypotheticals; 2 platform names garbled by transcription; most complete procedure set in the folder | Tech pack contents (R2), Alibaba vetting steps (R10, R11), structured quote (R17), 3-stage sample progression with hard stop (R24 to R26), landed cost lines (R20, R21, F6), early-run flexibility (R36), freight hybrid and backward planning (R52, R53, R55), pre-shipment QC (R48), 3PL criteria (R58, R59), reorder point and weekly rhythm (F3 to F5, R60 to R63), IP ownership (R6) |
| 04 | What I learnt from sourcing e-commerce products from China | Forum post with comments, 1,671 words, 9 cards | Anonymous US jewelry seller, 1 bulk order's worth of data; a commenter who is a US sourcing agent and contract manufacturer adds a conflicting view; nothing verified; ePacket dating from memory | Volume tiers and cash weighing (R18, F8), negotiate the opening quote (R19), margin gate before bulk (R22), test batch before switching (R29), defect buffer from observed rate (R49, F7), direct channel (R13), weight and season freight choice (R52, R54), Trade Assurance vs TT conflict (R41, C1), 30/70 split and partner-financed bulk (R42, R47) |

**Card id note.** Mini playbook 01 cites ids of 10 to 13 characters as extracted; they are used as given. Mini playbook 03's body cites `f8417709361e` for the Alibaba vetting card; its index gives the full id `f841770936e122f42298d352`, confirmed in cards.json, so this playbook uses `f841770936e1`.

**Neighbour folders.**

- 20-FIN finance and accounting: landed cost allocation and COGS recognition (F4, F5), fulfillment cost per order (F6), cash conversion cycle and financing options (3.13, 3.14), inventory grading and liquidation (P21, P23), the demand plan by channel before a PO (P22, R110), pricing waterfall (P17), free cash flow and distributions (C5 here).
- 21-OPS team and management: hiring, daily reporting, the ops-owner role 03 recommends (R61) as a hire.
- 01-PRD product research: whether to make the product at all; this folder starts after that decision.
- 03-OFF offers: pricing and bundles that consume landed cost.
- 10-MCR paid social creative: the marketing lever 01 checks alongside the BOM in an acquisition.
- 17-CXP post-purchase: customer-facing returns and delivery experience; this folder covers supplier-side defects only.
- 22-AMZ Amazon marketplace: FBA inbound rules and marketplace inventory limits, not covered here.

## Appendix A. General background

Content moved here is not deleted, only demoted: it is background the source gave, not a store-facing sourcing rule. Each entry says where it came from in the base document.

**From R57 (3.8 Freight and logistics).** A near-supplier base (01: Hong Kong) builds terms and iteration speed; 01 gives a $5,000 per month apartment comparison as the cost of living there, not a sourcing number. Recorded as 1 operator's choice, not a rule. Source: 01 only. [18fe817181]

**From R45 (3.6 Payment terms, float, payment route and financing).** Illustrative mechanics from 01 on export credit insurance and factoring: the factory pays a lump premium ($100,000 to $1M+ per year for a large factory), the insurer covers the factory once more than 20% of its customer base defaults, the bank advances about 99 cents on the dollar. All 01, China example, historical.

**From Conflict C5 (section 7), Dividend-first vs reinvest.** 01 argues for taking distributions from free cash flow ahead of growth-at-all-costs, based on his own turnaround. Mainstream advice and the growth-stage brands in other folders reinvest. This is finance, not sourcing. What the agent does: nothing here; the sourcing agent supplies float days, cash locked and financing cost, and 20-FIN decides. [43a500ef77] [25c520ee87]

**From Conflict C11 (section 7), Price-led selling.** 02 says winning a first client on price is "the best way" to start a sourcing agency and also "isn't how I love to sell". Agency-specific, out of scope for a brand agent; noted so the tension is not averaged away. [f759ab73c73c]

**From R71 (3.11 Supplier risk, concentration, country diversification and shocks).** Bali (and places like it) is for testing fabrics and small runs, not for scaled production: slow, expensive, heavy holiday downtime, and most fabric still comes from China. Condition: any island or boutique manufacturing base. Source: 02 only. [a0d9c84c5f13]
