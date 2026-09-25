# Complete E-commerce Operations Guide

source_id: 1gkDP7vVRMnDRuuoJDvnTNfumOz3vN926  |  folder: /21-OPS-team-and-management  |  cards: 22  |  words: 15,070  |  type: transcript (YouTube video)

credibility: The speaker identifies himself as "Davey," founder of the weighted-blanket brand the Oodie (he says the business did "over $650 million in sales" lifetime, and grew from about $10 million in its first year to about $25 million by its second year, pre-COVID). He also runs a paid mentorship business, Daily Mentor, which he says has "over 57" seven-figure brands as members. The video is monetized content: he discloses affiliate links for Triple Whale, Inventory Planner, and his own vetted list of 10 3PLs ("they are Affiliates as well"), and closes with a pitch to join Daily Mentor with a 30-day refund guarantee. Evidence offered is entirely his own operating experience and anecdotes from Daily Mentor clients, not studies or named third-party sources. He also discloses, unprompted, that after a 3PL failure the BBC ran a story "saying that I was a scammer" — this is a self-reported reputational fact from the source itself, not verified here. `[web check: BBC report on Oodie/founder "scammer" story, and current standing of the brand]`. Treat the whole source as one experienced operator's playbook plus sales pitch, not an audited or academic source.

date signals: No calendar year is stated directly. Internal signals: the Oodie's COVID-era demand spike is described as its "second year" of business, pre-COVID, at ~$25M revenue — placing Oodie's founding a couple of years before COVID (per public knowledge the Oodie launched around 2018, so this places the anecdote around 2020) `[web check: Oodie founding year and COVID-era revenue, if this is used as a dated case]`. The speaker says CS is about to see "a huge disruption" from AI adoption, suggesting the recording sits before that disruption played out. Tool mentions (Zendesk, Gorgias, Triple Whale, Inventory Planner, NetSuite, Fulfil) and their described strengths/weaknesses may be stale; treat all named tools as `[verify UI]` / `[web check: current pricing and feature set]`.

## 1. What this source is for

It is a single operator's tour of e-commerce "operations" as he defines it: product development and sourcing, inbound supply chain (freight, 3PLs), demand forecasting and purchase ordering, and customer service — deliberately excluding paid acquisition (his stated specialty) and finance/bookkeeping. It is aimed at DTC/apparel-style physical-product founders who have built some traction through marketing but have not yet built process discipline, from solo founder up to brands doing tens of millions in revenue. Its core argument: operations is the "soft moat" that protects a brand once marketing has generated demand, and neglecting it (poor tech packs, poor forecasting, poor 3PL vetting, undocumented POs) is what causes stockouts, bad reviews and even existential cash crunches.

## 2. Principles

1. **Operations = inputs → process → outputs, and the output is what the customer experiences.** Judge every operational change (automation, negotiation, headcount) by whether it improves the customer-facing result while cutting cost and process load, not by an internal metric alone. [0ff782611bef]
2. **Operations is a soft moat.** In e-commerce, brand and systems/operations are among the few defensible advantages against copycats and dropshippers; the source uses Amazon (heavy Opex/Capex into systems, eventually dominant) versus eBay (asset-light, margin-only) as its illustration of why investing in operations compounds. [0ff782611bef]
3. **Landed cost must be known before a product is priced or launched.** Sale price minus cost of product, freight, courier (pick/pack + outbound), storage, non-recoverable duties and payment fees gives the true contribution before marketing spend is subtracted — the source calls not tracking this "one of the main operational and financial mistakes" e-commerce founders make. [4cf8302e51b7]
4. **A tech pack is the primary defence against supplier quality drift and IP disputes.** Without one, disputes about "is this the same product" become unwinnable; with one, a founder can physically prove non-conformance (e.g., weighing fabric against a GSM spec). [24613aeb6cad]
5. **MOQ, price and lead time are one trade-off, not three separate negotiations.** A brand should deliberately choose whether it needs low MOQ (small budget), low price (margin), or low lead time (cash-flow turns), because a supplier will rarely offer all three. [48773124dba7]
6. **A critical path prevents missed seasonal windows.** Sequencing every product-development step with an owner and a date, and refusing to let suppliers edit it, is how the source says brands avoid missing Christmas trade and being stuck with January/February inventory. [2f17c3eca340]
7. **Forecast from the period you were actually in stock, not the raw calendar.** Including stockout days in a forecast base is, per the source, the top forecasting error and can drive 50% misses. [69512d4531fe]
8. **Both under- and over-ordering are existential, not just inefficient.** Zero stock means zero revenue against fixed costs; over-ordering locks all profit and cash into inventory, cutting off both marketing spend and tax payments. [48e4499ac999]
9. **A purchase order is a cross-functional document, not an invoice.** Finance, ops, marketing and customer service all need to see the same PO data (what's ordered, when it lands, what's been discontinued) or they will act on stale or wrong assumptions. [e50d8f082b51] [e252e690a92c]
10. **3PL selection should be run as a competitive RFP with facility visits, never a single-quote decision**, because 3PL failure is, in the source's telling, the single highest-consequence operational risk (see the $20M loss example in section 7). [875b2b81d78d] [25bacdb89696]
11. **Import duties and sales tax are not the same cost and must not be modelled together.** Duties are a sunk landed cost that varies by product/lane and is never recovered; sales tax is collected from the customer and remitted, and should be excluded from the profitability calculation. [05d7d9c866b8]
12. **A shared manual tracking sheet only works with a disciplined, dedicated owner.** The source's stated main failure mode across the whole video is "I'll update it later" — stale data then propagates into other teams' decisions. [5eb084517f52]
13. **Customer service quality is a lagging output metric for the rest of operations.** Slow freight, a missing tech pack, or an underperforming 3PL will surface as bad reviews and long resolution times before they show up anywhere else. [08a8a291428f]
14. **Do not assume offshore customer service is automatically cheaper.** The source argues local agents can be roughly twice as efficient as international ones, so true cost depends on training and ticket routing, not just wage rate. [d55c91623549]
15. **Below roughly $1M revenue, expect the founder to hold every operational role personally**, hiring freelancers for discrete tasks (e.g., a tech pack) rather than staff; dedicated roles (COO, forecaster, ops manager) come later as the business can afford them. [0ff782611bef] [87a5258c4926]

## 3. Procedures

**A. Build a tech pack before placing a large order** [24613aeb6cad] [9268b8dd340f]
1. Produce a complete drawing showing print placement, shape and approximate colours.
2. Document fabric specs: GSM (thickness/density), softness, and treatment instructions (e.g., acid wash). Collect physical strike-off samples and keep one set on file.
3. Record precise measurements for every size, especially for grading across S/M/L/XL.
4. Add graphics specs.
5. Add hardware specs (zips, pockets, closures).
6. Add label/swing-tag specs, including correct company-name placement (wrong or missing labelling can trigger regional fines) and packaging specs.
7. Keep reference photos of all samples produced.
8. If you cannot produce this yourself, commission a freelance tech-pack creator (the source used Upwork) with a defined deliverable; get a current quote rather than assuming the source's ~$200 anecdotal price. `[web check: current freelance tech-pack pricing]`
9. Use the finished tech pack to brief a second supplier for a comparative quote, and retain it (with the PO and supplier messages) as your evidence base for any quality dispute.

**B. Negotiate and place the first purchase order** [48773124dba7] [9268b8dd340f]
1. Decide the product-development route: supplier co-development (cheaper, but the supplier may retain design ownership and anyone can copy it) versus an independent product/fashion designer or agency (more control, needs its own ownership/usage terms), then get comparable manufacturing quotes with the tech pack.
2. Get the supplier's actual MOQ, unit price and manufacturing lead time (lead time is manufacturing time only, not shipping time).
3. Choose which lever matters most for this SKU: lower MOQ (small budget) or lower lead time (faster cash-flow turns); the source notes Oodie sometimes paid more per unit specifically to get shorter lead times.
4. Compare 2+ factories and consider de-speccing the product to hit a viable landed cost; the source cites ~20% price improvement as achievable through comparison and negotiation (its own example, not a guaranteed figure).
5. Run the resulting landed cost against your intended retail price before committing — if it forces an unviable retail price, do not launch that variant (the source's inflatable-arm hoodie example: a landed cost that would force a $200 retail price kills demand for a product that would otherwise sell at $20-30).
6. Agree refund and quantity-tolerance terms, and ideally a signed contract, before wiring large sums, especially if the product is unique IP. The source says he has operated without contracts before but recommends them, and notes suppliers early on may resist a contract until trust is built.
7. Communicate through one channel — the source recommends keeping all supplier communication inside Alibaba (using Trade Assurance) so a dispute can be proven against message history, the tech pack and the PO.
8. Record the calculated landed cost in both the PO and Shopify's "Cost per item" field so downstream profit reporting is automated. `[verify UI: Shopify cost-per-item field location]`

**C. Run a critical path from sample to bulk production** [2f17c3eca340]
1. List every development step: strike-offs/prints, first sample, revised sample, production sample, QC, bulk production, freight, inbound to warehouse.
2. Sequence the steps in order in a project tool (the source names Monday.com, Asana, Notion, or Excel — pick one; `[verify UI]` on current features) or with a team member.
3. Assign a duration to each step (example given: a DHL sample from China takes about 5 days).
4. Set a target date per step, working backwards from a hard deadline (e.g., the Christmas shipping cut-off).
5. Assign one owner per step and monitor daily; use the tool's reminders for overdue tasks, and either push downstream dates or use built-in slack when a step slips.
6. Do not give suppliers edit access to the critical path — they can alter dates and the team loses visibility.
7. Book a QC agent (via Alibaba's inbuilt QC function or an external agency like SGS) for at least the first production run, and ideally the second and third; the agent weighs and measures the product against the tech pack and checks Pantone colour. `[verify UI: Alibaba QC feature]`

**D. Forecast demand and set the reorder point** [69512d4531fe] [87a5258c4926] [48e4499ac999]
1. Choose your forecast base period: exclude any days you were out of stock; if 15 of 30 days were in stock, extrapolate from those 15, not the raw 30.
2. If the business has under about a year of history or is growing fast, use month-on-month trend (example: 100 → 120 → 145 → 175 units suggests ~20% growth) and project the next month(s) linearly/slightly exponentially.
3. If seasonality dominates (the source says 90-95% of e-commerce businesses have meaningful seasonality from Black Friday and holiday gifting), build a month-by-month curve instead (example given: Jul 200, Aug 210, Sep 205, Oct 2,000, Nov 4,000, then a sharp drop after the Christmas shipping cut-off).
4. Check product-driven seasonality with Google Trends (example: "beach tent" spikes in northern-hemisphere summer) and remember northern/southern hemisphere seasons are reversed.
5. Apply a growth-rate assumption in your forecasting tool or a custom Excel sheet (the source names Inventory Planner as its own current choice, used for about 2 years at time of recording; also mentions NetSuite-class ERPs and Walmart-grade tools as alternatives it tested and moved away from). `[verify UI / web check: current Inventory Planner features and pricing]`
6. Enter supplier manufacturing lead time (example: 100 days) — longer lead time pushes the tool to recommend ordering earlier.
7. Set a target days-of-stock figure based on business volatility and available capital — typical range given is 4, 8 or 12 weeks.
8. Add 5-10 days of safety stock as a buffer, but only after lead time is already padded with an average (not best-case) figure; the source argues safety stock shouldn't be doing much work if lead time is padded properly.
9. Read the tool's two outputs: expected sell-out date and recommended replenishment quantity, then place the purchase order.
10. Review this on a weekly, fortnightly or monthly cadence; assign an owner (an operations manager is enough — it does not need to be a dedicated demand planner) once the business is profitable enough to pay one.

**E. Manage the purchase order across departments** [e50d8f082b51] [e252e690a92c]
1. Create a formal PO (product, price, quantities, ship-to, terms) rather than a bare Alibaba order line.
2. Keep the authoritative PO in accounting software (the source names Xero or MYOB) so it reconciles against supplier deposits and final payments.
3. Create a second, team-visible tracker (Google Sheets/Drive or Airtable) with SKU-level product, quantity and PO number that finance, ops, marketing and customer service can all view.
4. As freight details arrive, add them to the same sheet: estimated departure date, ETA, vessel number, bill of lading (or, for air freight, a tracking number and estimated dates).
5. Update the ETA whenever the vessel is pushed back, and notify affected teams via Slack/comments rather than letting them work off a stale date.
6. Keep the sheet internal-only — route any supplier-side change through one channel (e.g., Alibaba messaging) rather than letting suppliers edit the tracker directly.
7. Before discontinuing a product or issuing mass refunds, check the tracker for a PO about to land so you don't refund stock that is already in transit.
8. Once revenue passes roughly $30-50M, consider an ERP (see section 6) since the source says it can absorb about 90% of these coordination tasks; below that, the spreadsheet/accounting-software combination is the source's recommended stopgap. Add dedicated headcount to maintain the sheet once you cross roughly $5-10M revenue, since a single person can no longer keep it reliable past that point. [5eb084517f52] [b835681136c8]

**F. Select and manage a freight provider** [0bfbfacfd9fe]
1. Choose freight providers based in your own region (e.g., US-based if shipping from the US) so you can hold them locally accountable.
2. Engage 2-3 providers simultaneously and compare rates monthly; do not lock in with one provider indefinitely.
3. Once selected, hand them the PO or CC them into the supplier communication so they can coordinate collection directly with the factory.
4. Record what they return — estimated departure date, ETA, vessel number, bill of lading (or tracking number for air freight) — into the internal master sheet described in procedure E.
5. Re-shop freight rates on a monthly cadence rather than treating the first quote as fixed.

**G. Run a 3PL RFP and set up the SLA** [875b2b81d78d] [25bacdb89696] [30a460679b7f] [9b59cf172fa6]
1. Assemble a master RFP document: product dimensions, historical results, and — most important, per the source — your growth forecast, since a growing brand is what makes 3PLs compete for the account.
2. Send the identical document to multiple 3PLs (the source maintains its own vetted list of about 10) so quotes are comparable.
3. Visit the facility in person, or at minimum see interior footage; refusal to show the facility is a red flag (the source cites one prospective 3PL using stolen supermarket shopping trolleys to move stock internally).
4. Confirm they scan barcodes on both inbound and outbound — without this, missing stock becomes unresolvable finger-pointing.
5. Gauge whether you'll be a valued account: being the smallest (or, at the other extreme, sometimes the largest) customer on their book affects service quality; sales-team behaviour during the RFP is one signal.
6. Negotiate and record 3 price components separately: pick/pack, inbound (unloading), outbound (courier — this varies hugely by 3PL because each holds its own carrier account, e.g., UPS, Australia Post, Royal Mail), plus storage (usually minor unless the product is bulky).
7. Put picked-on-time and delivered-on-time guarantees, plus a minimum of two cycle counts a year, into a written SLA, with a stated consequence if pick-time is missed (the source suggests a discount on that pick or a free pick).
8. Send an advance shipping notice (ASN) ahead of inbound deliveries and follow the 3PL's booking requirements to reduce receiving delays; note an ASN does not itself guarantee no fees.
9. Audit the monthly 3PL invoice yourself: build a spreadsheet that estimates pick/pack, inbound, outbound and storage cost from your own Shopify order volume for the period, and compare it to what was billed; the source says roughly 30-40% of Daily Mentor clients it has seen were being overcharged in some cost area by simply accepting the invoice.
10. Track delivered-on-time yourself as an internal metric (3PLs won't put this in the SLA); if it drops under about 95%, investigate whether the cause is pick time or carrier lag before pursuing a discount or refund.
11. Give the 3PL forecasts you genuinely intend to hit — over-promising causes them to over-staff and can damage the relationship; the source frames this as a mutually profitable relationship, not a zero-sum one, and argues the cheapest 3PL is not automatically the best choice.

**H. Set up and run customer service** [d55c91623549] [08a8a291428f] [3f6fb0e7eecd]
1. Pick a helpdesk tool that consolidates email/tickets (the source tried Zendesk, found it "too clunky, slow," and moved to Gorgias; frames this as one operator's comparison, not a universal recommendation). `[web check: current CS tool comparison, since the source flags AI-driven disruption in this category]`
2. Decide the international-vs-local split: route simple, repeatable tickets to international agents (source mentions Philippines and Fiji); route nuanced/escalated tickets to local agents who sit closer to the internal team and source of truth. Use a blended model for larger businesses; either can work for smaller ones.
3. Do not assume international agents are automatically cheaper — build training and macros so their per-ticket efficiency approaches local agents' (source claims local can be roughly double as efficient without good training).
4. Use the sales forecast curve (not current ticket volume) to plan when to onboard and train extra agents, so new agents are productive before a peak rather than during it; lean on the international tier for fast ramp-up/ramp-down around peak season.
5. Define in advance what counts as a "complex" ticket so new or offshore agents are only routed tickets they can handle.
6. Track cost per service through the ramp-up to confirm headcount is tracking ticket volume rather than drifting.

## 4. Rules, thresholds and numbers

| Rule / number | Value | Condition | Source's basis | Card id |
|---|---|---|---|---|
| Freight forwarders to compare | 2-3, monthly | Any container/air freight lane | Operator experience | 0bfbfacfd9fe |
| Tech-pack freelance cost | "shouldn't cost more than 200 bucks" | Commissioning via Upwork | Anecdotal, source flags as such | 24613aeb6cad |
| Price improvement from supplier negotiation/comparison | ~20% | Comparing multiple factories, de-speccing | Source's own example, not a benchmark | 48773124dba7 |
| Container freight cost example | $11,000 / 1,000 units = $11/unit | Sea freight, identical units | Worked example; transcript itself misstates this as "$1" — treat $11 as correct | 4cf8302e51b7 |
| Two-brand landed-cost comparison | Freight $5 vs $6; product $10 vs $12; courier $5 vs $8; storage $1 vs $2 → landed $21 vs $28 | Illustrative only | Source's own example | 0ff782611bef |
| Extra margin from better ops (illustrative) | ~$7/unit, ~14% more profit on a $50 CAC | Same illustrative pair | Source's own example | 0ff782611bef |
| Manufacturing lead-time input example | 100 days | Forecast tool configuration | Example figure, not a target | 87a5258c4926 |
| Days-of-stock target | 4, 8, or 12 weeks | Depends on volatility and available capital | Source heuristic | 87a5258c4926 |
| Safety-stock buffer | 5-10 days | Only after lead time is padded with average, not best-case, figure | Source heuristic | 87a5258c4926 |
| Forecast miss, big-box retailer baseline | ~5% variance | Established, low-volatility retail | Cited industry baseline, not verified here | 48e4499ac999 |
| Forecast miss, growing e-commerce | ~50% | Fast-growing or high-volatility brand | Source's own estimate | 69512d4531fe / 48e4499ac999 |
| Sample shipping time (DHL, China) | ~5 days | Air-shipped physical sample | Example figure | 2f17c3eca340 |
| ERP adoption threshold | ~$30-50M revenue | Brand outgrowing spreadsheets/accounting software | Source heuristic | b835681136c8 / e252e690a92c |
| ERP cost | "over $200 grand," source's own implementation "upwards of half a million dollars" | Full ERP (e.g., NetSuite-class) implementation | Source's own reported spend; not a quote | b835681136c8 |
| Manual-sheet staffing threshold | ~$5-10M revenue | When one person can no longer keep the shared tracker reliable | Source heuristic | 5eb084517f52 |
| SLA pick-time commitment | 24-48 hours | Normal (non-peak) operation | Source-recommended SLA term | 30a460679b7f |
| Minimum cycle counts | 2 per year | 3PL inventory accuracy, written into SLA | Source recommendation | 30a460679b7f / 875b2b81d78d |
| Delivered-on-time investigation trigger | below ~95% | Internal CS/ops metric, not a contractual SLA term | Source-stated internal trigger | 30a460679b7f |
| Clients found overcharged by 3PL/courier | ~30-40% | Sample of Daily Mentor's own client base | Source's own client-sample claim, not independently verified | 9b59cf172fa6 |
| 3PL failure loss example | $20M+ lost revenue against a forecast $45-50M Oct/Nov peak | One historical incident at Oodie | Source's own case, not a benchmark | 875b2b81d78d |
| Founder holds all ops roles | below ~$1M revenue | Solo founder or early team | Source heuristic | 0ff782611bef |
| Missed growth from lacking an ops role | Oodie could have been "30-40% bigger" | COVID demand-surge period, ~$25M pre-COVID revenue | Source's own retrospective estimate | 48e4499ac999 |

## 5. Diagnostics and checks

- **Is our landed cost actually known?** Check whether Shopify's "Cost per item" field (or equivalent) is populated with true landed cost (product + freight + courier + storage + non-recoverable duties + payment fees), excluding sales tax. If not populated, daily profit reporting through tools like Triple Whale will be wrong. `[needs brand data: current landed cost per SKU]` [4cf8302e51b7]
- **Are we forecasting from a clean base period?** Check whether the trailing period used for a forecast included any stockout days. If yes, redo the forecast using only in-stock days. [69512d4531fe]
- **Is the 3PL invoice being audited?** Rebuild expected pick/pack, inbound, outbound and storage cost from your own Shopify order volume for the month and compare to the invoice; a gap flags likely overcharging (source claims this is common — 30-40% of one operator's client base). `[needs brand data: monthly 3PL invoice + Shopify order volume]` [9b59cf172fa6]
- **Is delivered-on-time tracked and healthy?** Pull this from your own CS/fulfilment data; if under ~95%, diagnose whether the cause is the 3PL's pick time or a carrier backlog before escalating for a discount. `[needs brand data: delivered-on-time %]` [30a460679b7f]
- **Is customer-service cost per ticket stable relative to sales swings?** Compute total CS expense (software + agents) ÷ ticket volume; if it is drifting up while sales/tickets rise, headcount or routing may be lagging the forecast. `[needs brand data: CS spend and ticket volume]` [08a8a291428f]
- **Why is resolution time or touch-points per ticket high?** Diagnose in order: (1) insufficient visible internal information, (2) slow agents or poor systems, (3) weak/missing macros forcing manual replies. [08a8a291428f]
- **Are reviews degrading?** Treat public reviews as a lagging output metric; trace backward through PO accuracy, freight negotiation and 3PL pick time rather than blaming support agents first. [08a8a291428f]
- **Is the PO visible to every department that needs it?** Confirm finance, ops, marketing and CS can all see current POs and their landing dates before a promotion is planned or a refund is issued; check specifically that a PO close to landing isn't being ignored when a product is about to be discontinued. [e50d8f082b51] [e252e690a92c]
- **Is the shared tracking sheet stale?** Check whether estimated vs. actual departure/arrival dates are both logged, and whether someone owns updating the sheet on a fixed cadence; stale data is the source's stated top cause of cross-team mistakes. [5eb084517f52]

## 6. Tools, settings and named features

| Tool | Used for | Notes |
|---|---|---|
| Alibaba (incl. Trade Assurance, inbuilt QC) | Sourcing, supplier messaging, dispute evidence, first-run QC booking | `[verify UI]` — Trade Assurance terms and QC feature availability may change |
| AliExpress | Early-stage sourcing comparison | Mentioned as an alternative to Alibaba for first outreach |
| SGS | Third-party QC/compliance inspection | Source says "quite expensive and big" but does compliance too |
| Monday.com, Asana, Notion, Excel | Critical-path / project management | Source uses Monday.com but says "pretty impartial" which one you use |
| Google Trends | Checking product-driven seasonality | Free tool; example search "beach tent" |
| Inventory Planner | Demand forecasting / replenishment app for Shopify | Source's own affiliate; used ~2 years at time of recording `[web check: current features/pricing]` |
| NetSuite | ERP | Source calls it "very very expensive"; cited only as an example, not tested in depth here |
| Fulfil (referred to as "fulfill.") | ERP | Source has "heard good things" via a client (Ridge Wallet) using it; not personally used |
| Xero, MYOB | Accounting software, authoritative PO record | `[verify UI]` |
| Google Drive / Google Sheets, Airtable | Shared, team-visible PO/freight tracker | Internal-only; suppliers should not have edit access |
| Slack | Notifying teams of tracker changes (e.g., ETA slips) | |
| Shopify "Cost per item" field | Storing landed unit cost for automated profit reporting | `[verify UI]` |
| Triple Whale | Automated daily profit/marketing reporting pulling from Shopify cost data | Source discloses an affiliate link |
| Looker | Custom reporting/dashboards as an alternative to Triple Whale | Mentioned once, not detailed |
| Zendesk | Helpdesk tool | Source tried and dropped it, calling it "too clunky, slow" |
| Gorgias (referred to as "gorgees") | Helpdesk tool, current choice | Source says other options exist; compare pricing for your business size |
| UPS, Australia Post, Royal Mail | Outbound courier accounts held by 3PLs | Rates vary hugely by 3PL's own account/volume |
| DHL | Sample shipping (used in the critical-path example) | |

## 7. Examples and case results

- **Oodie tech-pack fabric dispute (example).** After scaling weighted-blanket sales quickly (source says the category did about $10M in its first year, about $1M profit), customers complained the blankets were "too thin." Because a tech pack with a GSM spec existed, the team cut a standard-size fabric square, weighed it, proved the supplier had substituted thinner fabric, got the faulty units removed from sale, and had the supplier replace them. Presented as an example of what a tech pack enables, not a guaranteed outcome. [24613aeb6cad]
- **COVID demand-surge miss (example).** In Oodie's second year (~$25M revenue, pre-COVID), COVID hit right after launching YouTube ads; daily sales spiked (source cites a $200,000 day) but the business had nobody dedicated to operations/planning, so it did not reorder enough stock and sold out. Source's own retrospective estimate: the business could have been "30-40% bigger" with an ops/planning role in place at the time. [48e4499ac999] [0ff782611bef]
- **3PL failure during peak (example).** Forecasting a $45-50M October/November period, a contracted 3PL "completely couldn't ship any orders"; promotions had to be turned off, wrong products were shipped, and the source estimates over $20M in lost revenue. The source states the BBC then ran a story calling him a scammer. `[web check: verify this reporting independently before citing publicly]` [875b2b81d78d]
- **Illustrative two-brand cost comparison (not a real case).** Brand A: freight $5, product $10, courier $5, storage $1 → landed $21. Brand B: freight $6, product $12, courier $8, storage $2 → landed $28. The $7/unit gap is framed as extra headroom for marketing spend or profit (~14% more profit cited against a $50 CAC example). Explicitly a made-up illustration, not a client result. [0ff782611bef]
- **Unviable product design (example).** A hypothetical over-specced hoodie (inflatable arms, built-in speakers) that would sell at $20-30 unspecced actually costs $50-60 to land, forcing a $200 retail price and killing demand — used to argue unit economics must be checked before committing to a product spec. [48773124dba7]
- **3PL red flag (example).** A prospective 3PL competing for Oodie's account was found reusing stolen Woolworths shopping trolleys to move product internally — offered as a facility-visit red flag, not typical of the industry. [25bacdb89696]
- **Container freight math (worked example, contains an error).** "$11,000 container / 1,000 units" is spoken in the transcript as "$1 per unit," which is arithmetically wrong; the correct figure is $11/unit. Flagged here so it is not propagated as a lower cost than it is. [4cf8302e51b7]

## 8. Mistakes the source warns about

- Not tracking daily profit / true landed unit economics — called one of the most common operational and financial mistakes in e-commerce. [4cf8302e51b7]
- Confusing duties (a sunk, non-recoverable landed cost) with sales tax (collected and remitted) in the profit model. [05d7d9c866b8]
- Over-speccing a product without checking landed cost against a viable retail price before committing. [48773124dba7]
- Spreading supplier communication across multiple channels instead of centralizing in one auditable channel (source recommends Alibaba + Trade Assurance). [24613aeb6cad]
- Operating without any agreed terms on refunds, quantity tolerance and IP/ownership before wiring large payments to a supplier. [48773124dba7] [9268b8dd340f]
- Letting suppliers edit the internal critical-path or PO/freight tracker, which lets them manipulate dates the team can't independently verify. [2f17c3eca340] [e252e690a92c]
- Selecting the wrong date range for a forecast (including stockout days), which the source calls the top forecasting error. [69512d4531fe]
- Expanding SKUs (colours/sizes) without recognizing this multiplies forecast risk and capital requirement. [48e4499ac999]
- Fragmenting POs (e.g., only recorded as ad-hoc Alibaba orders) instead of routing one authoritative PO to finance, ops, marketing and CS. [e50d8f082b51]
- Accepting 3PL/courier invoices at face value instead of auditing them against your own order volume — source claims 30-40% of a client sample were overcharged somewhere. [9b59cf172fa6]
- Treating the 3PL relationship as zero-sum / always chasing the cheapest option, which the source argues backfires on service quality. [25bacdb89696]
- Under-forecasting your own 3PL's staffing needs for peak, causing pick time (and therefore delivery time) to blow out during Black Friday/Christmas. [30a460679b7f]
- Assuming offshore customer service agents are automatically cheaper without accounting for training and efficiency differences. [d55c91623549]
- Leaving a shared operational tracker unmaintained ("I'll do it later") — source's stated main failure mode for cross-team sheets. [5eb084517f52]
- Not incorporating sales tax handling correctly in the Shopify backend (missing the "charge tax" setting), which distorts the profit calculation. [05d7d9c866b8]

## 9. Caveats, conflicts and what is missing

- The source explicitly flags many of its own numbers as illustrative, not benchmarks: the 20% price-improvement figure, the $21/$28 two-brand example, the 14%-more-profit figure, the 30-40% overcharge claim, the 30-40% "could have been bigger" estimate, and the $200 tech-pack price. These are kept in this playbook as examples per the writing rules, not restated as targets.
- Internal arithmetic error: the transcript states a $11,000/1,000-unit container costs "$1 per unit," which is incorrect ($11/unit is correct). Card 4cf8302e51b7 already corrects this; anyone reading the raw transcript should not copy the "$1" figure.
- Named tools (Zendesk vs. Gorgias, Inventory Planner, NetSuite, Fulfil) reflect the source's personal experience and disclosed affiliate relationships (Triple Whale, Inventory Planner, its own 3PL list); it does not claim to have done an independent market comparison. Treat tool endorsements as one operator's preference, not a verified "best in class" ranking. `[web check: current CS/forecasting tool landscape before recommending to a brand]`
- The source discusses being the subject of a BBC story calling him a scammer, connected to the 3PL failure. This is self-reported and one-sided in the transcript; it is not independently verified here and should not be repeated as fact without a check. `[web check: BBC report and Oodie's public response]`
- Legal/IP statements (who owns product IP after co-development, what a contract should say) are given as operational advice from an operator, not as legal guidance; the source itself says contracts are "recommended" but that he has operated without them, which is a soft, hedged position rather than a hard rule.
- The source gives almost no detail on hiring process, job descriptions, interview practice or org-chart transition mechanics beyond naming CEO/CFO/CMO/COO and what the COO oversees (Product, Supply Chain, Fulfilment, Customer Service). Despite this file living in the "team and management" folder, the source is weighted heavily toward supply chain/inventory/3PL/CS process and cost mechanics, and is thin on people-management, hiring and SOP-writing practice specifically. That gap should be filled from other sources in this folder.
- No conflicts with other sources in this folder were found within this single-source read; conflicts (if any) should be resolved at the Pass 2 folder-playbook stage once multiple sources are compared.

## 10. Card index

- 4cf8302e51b7 — Build landed unit cost and contribution per ecommerce order
- 24613aeb6cad — Write a tech pack to control supplier quality and prove non-conformance
- 48773124dba7 — Negotiate MOQ, price and lead time as one trade-off set
- 0ff782611bef — Order against the outputs: operations as an input→process→output system
- 2f17c3eca340 — Build a critical path to hit launch and seasonal deadlines
- 69512d4531fe — Forecast demand on an in-stock window, not a raw calendar period
- 87a5258c4926 — Set lead time, days-of-stock and safety stock inputs in the forecast tool
- e50d8f082b51 — Use purchase orders as the single cross-functional source of truth
- 875b2b81d78d — Protect against 3PL failure with SLAs and multi-warehouse RFPs
- 05d7d9c866b8 — Keep import duties and collected sales taxes separate in the cost model
- 9268b8dd340f — Choose supplier co-development vs independent product design
- 48e4499ac999 — Run forecasting continuously to avoid the two existential inventory failures
- e252e690a92c — Purchase order visibility across departments
- 9b59cf172fa6 — Auditing 3PL invoices against actual order volume
- 25bacdb89696 — Running an RFP to select a 3PL
- 30a460679b7f — Writing an SLA with pick-time penalties for peak periods
- d55c91623549 — Designing the customer service tier split
- 08a8a291428f — Cost per ticket and resolution-time diagnostics
- 3f6fb0e7eecd — Forecast-driven support capacity planning
- b835681136c8 — Deciding when to buy an ERP
- 5eb084517f52 — Why manual operations sheets fail
- 0bfbfacfd9fe — Choosing a freight provider on competing quotes
