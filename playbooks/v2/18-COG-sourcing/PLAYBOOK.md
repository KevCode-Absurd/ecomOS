# 18-COG Sourcing playbook

version: 2.0-draft  |  date: 24 Sep 2026  |  sources: 4 mini playbooks (4 independent presenters; mini playbook 04 also carries a second voice, a commenter)  |  cards: 82  |  built from: sources/*.md

## 0. How to use this playbook

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

