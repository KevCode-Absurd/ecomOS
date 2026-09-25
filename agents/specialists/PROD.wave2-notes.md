# PROD wave 2 notes

29 new capabilities (PROD-C48 to PROD-C76) plus 3 extensions of wave 1 records (PROD-C22, PROD-C44, PROD-C47).

## Sources by type

- Job descriptions / day-in-the-life: sourcing manager, ecommerce merchandiser, supply chain planner, fulfilment manager, Amazon/marketplace manager, catalogue executive (scmtalent, velvetjobs, clickpost, expertia, multiplymii).
- Agency service menus: third-party QC inspection pricing in China and India (QIMA, Tetra Inspection, TradeAider, AQI, V-Trust), quick commerce onboarding agencies (tech2globe, ecomsarthi).
- SaaS feature lists: Cin7, Katana, Netstock (inventory forecasting/reorder points); Sellercloud, ChannelAdvisor/Rithum (multichannel listing); Unicommerce, Increff (India WMS/OMS, live inventory pool, UPB serialization); Sales Layer, Salsify, Plytix (PIM); Zonos, DutyGlobal (landed cost calculators).
- Freelance marketplaces: Fiverr/Upwork gig categories for Amazon listing optimization ($75-800/SKU) and sourcing agents (Alibaba/AliExpress).
- AI agent products: Lyzr, Keelvar, Pactum, SupplyChainBrain on procurement agents (intake triage, RFQ drafting, three-way invoice matching, negotiation support, spend anomaly detection) : used to size what is common (advisory/drafting) versus what is still rare (an agent actually running the negotiation).
- India-specific (fed the India-market options in the affected capabilities; markets: IN): Shiprocket/Delhivery/Bluedart comparisons (aggregator vs direct, NDR panels, RTO reduction); confetti.design's day-by-day quick commerce guide (onboarding docs, ad credits, the MRP-vs-transaction ROAS distortion, contribution-margin gates); GST e-invoicing/HSN rules (vertexinc, incorpx, carajput); Legal Metrology and FSSAI labelling (taxtmi, diligencecertification, omgarudagroup).

14 web searches, 3 page fetches (confetti.design quick commerce guide, Lyzr procurement agents, Clickpost fulfilment manager).

Wave 5 (25 Sep 2026) made the brand default US-first: the rapid-delivery/quick-commerce capabilities now lead with Instacart, DoorDash and Gopuff, with Blinkit, Zepto and Instamart folded in as the India option; the tax/licensing capabilities now lead with US sales tax, FDA and state EPR, with GST/HSN, Legal Metrology, FSSAI and India's EPR rules folded in as the India option (markets: IN, reads null for a US brand). Coverage was not deleted, only re-centred; see PROD.json, PROD.wave2.json, PROD.skills.json and PROD.workflows.json for the resulting record shapes.

## What wave 1 missed most

Rapid-delivery/quick commerce (Instacart, DoorDash, Gopuff; India: Blinkit, Zepto, Instamart, markets: IN) was entirely absent despite being named in the brief: onboarding, the list/MRP-based ROAS distortion that inflates reported returns 30-50%, ad-credit management, dark-store fill rate, and the 90-day unit-economics validation window. Biggest single gap: 4 records (C48-C51).

Second: domestic operations mechanics below the strategic calls wave 1 covers. Wave 1 has 3PL/freight selection (C21) and reorder-point math (C22), not the daily layer underneath: WMS slotting and labor scheduling, returns grading, multi-carrier rate-shop and failover, carrier-exception outreach (India: NDR outreach, markets: IN), carrier billing reconciliation (India: COD remittance reconciliation, markets: IN), carrier scorecarding. Daily jobs of a fulfilment manager and shipping executive that no wave-1 record touches.

Third: US compliance beyond FTC/quality-marking (C45): sales-tax product-category validation against marketplace-facilitator filing errors, FDA/state-licence renewal tracking, state EPR packaging filing (India: HSN/SAC validation against e-invoice rejection, Legal Metrology and FSSAI licence-renewal tracking, India's EPR plastic-packaging filing; markets: IN). Concrete and recurring, done today by nobody or by the founder ad hoc.

Fourth: catalogue as a data-management discipline, not just an ads feed (C47) or one marketplace's listing (C34/C44): a real PIM layer with completeness scoring, per-channel formatting, cross-channel price/stock audits, image/video spec validation.

## Possible, not yet commonly sold

An agent that runs the actual multi-round supplier negotiation over email or a messaging channel (WhatsApp where the supplier region uses it) within founder-set guardrails (procurement agents today mostly prep the human, per Lyzr/Keelvar/Pactum, rather than negotiate themselves for small D2C import orders). A background watch on Alibaba/1688/Faire/Tundra/ThomasNet (India: IndiaMART, markets: IN) for a better-than-incumbent supplier against a held spec, alerting only, never contacting. A per-order carrier-exception stop/retry decision driven by the brand's own margin and return-to-sender cost (India: NDR stop/retry and RTO cost, markets: IN) instead of one blanket aggregator rule. A COD-to-prepaid conversion test run as a designed, read experiment rather than a policy nobody tests (India only; markets: IN, reads null for US brands). A state EPR compliance tracker (India: an EPR compliance tracker), since brands currently either ignore it or outsource it blind to a consultant.
