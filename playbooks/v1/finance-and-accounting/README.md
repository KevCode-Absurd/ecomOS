# Finance And Accounting — draft playbook

**Status:** source-linked draft; not owner-approved or outcome-tested.

Read [the operating contract](../OPERATING_CONTRACT.md) before using a workflow.

## Inputs
- Orders/refunds
- COGS
- fulfilment/payment/ad costs
- cash balances
- liabilities
- dates

## Measures
- Contribution
- cash runway
- forecast error

## Foundation candidates
Inferred principle labels do not establish universal applicability. Retain source conditions; empty means no matched labelled principle, not absence of foundational knowledge.

- **Five core finance practices to run an ecommerce brand** (`8d570963a07c01bd206aac7f`): A closing checklist of five financial operating habits—margin literacy, live dashboards, new/returning separation, cash vs P&L plays, and constraint diagnosis.
  Applies when: Setting your store's monthly financial operating rhythm or auditing which finance disciplines your team is missing before scaling spend.
  Condition: The daily-vs-weekly ROAS preference is the presenter's opinion, not an established benchmark.
  Condition: The five-point list is a summary framework; it does not define numeric thresholds for any metric.

- **Why inventory purchases make a profitable store run out of cash** (`6a8332853dd6467236375330`): Buying stock in large lumps hits cash in the purchase month while the cost only reaches the P&L when goods sell, so profitable periods can coincide with cash shortages.
  Applies when: Planning inventory replenishment or a seasonal stock buy for an ecommerce store, or explaining why a high-revenue month did not improve the bank balance.
  Condition: The case study numbers are illustrative of one store's model, not benchmarks for expected inventory turns or margin levels.
  Condition: Inventory dynamics will differ by model — made-to-order, dropship or pre-order stores carry very different cash timing.

- **Balance Sheet to P&L Timing for Inventory Versus Services** (`a490586f1272b8c3e1a858c1`): CPG costs sit on the balance sheet as inventory until sale, while many SaaS costs like wages hit the P&L immediately.
  Applies when: Forecasting cash and monthly profitability, or explaining to a founder-investor why a stock build-up hurts cash before it hits COGS.
  Condition: The source notes most modern small companies rent rather than own servers; ownership changes the accounting treatment.
  Condition: Inventory costing methods (e.g. FIFO/weighted average) are not covered here.

## Calculate ecommerce unit economics
Workflow ID: `finance-and-accounting.unit-economics`

**Deliverable:** Unit-economics table with assumptions

### Proposed decision sequence
1. Define revenue net of relevant discounts and returns
2. Allocate product, fulfilment, payment and acquisition costs consistently
3. Show contribution and sensitivity to unknown inputs

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Turn a contribution-margin model into a pricing and negotiation checklist
Card: `2978d63684eab4dea71a22e7` · Source: Finance for eCommerce (1).docx · Section: 3

Because net margin per order is thin, identify each controllable line — freight, duties, pick and pack, packaging, 3PL, payment fees — and quantify what a dollar saved on each is worth at your order volume.

Applies when: Negotiating with a 3PL, carrier or supplier, evaluating a packaging change, or deciding where to spend optimization effort in an ecommerce P&L.

- Lay out the full net revenue to operating income waterfall per unit so every cost is visible on its own line: gross revenue, discounts, returns, shipping income, net revenue, product cost, import freight, duties and taxes, gross margin, pick and pack, packing materials, 3PL charges, shipping to customer, merchant fees, contribution margin, marketing, post-marketing contribution, opex, operating income.
- Track each line period over period as both a dollar per order and a percent of net revenue. In the source case, product COGS moved from 29% to 27% of net revenue, pick and pack declined month over month (possibly from a better warehouse system), and fulfillment totaled $31 then $35 per order.
- Watch the lines the source flags as volatile and worth close attention: import freight, duties and taxes, and shipping to customer — the presenter specifically notes freight costs varying wildly and shipping being a key management area for ecommerce.
- Quantify the payoff of a fix: if you can negotiate or eliminate a couple of dollars from any individual expense, that becomes an extra few dollars per order, which across thousands of orders changes profit by tens of thousands.
- Include payment processing explicitly. The source assumes about 2.75% of revenue for credit card processing in a subscription model and $3.65 to $3.79 per order in the case study — a line that scales with revenue and can be negotiated.
- Compare margins across periods and treat per-unit visibility as the point: a standard P&L that lumps all product and fulfillment costs into one COGS bucket hides whether the unit economics are improving or deteriorating.
- **Condition:** The case study's 29%/27% COGS, $31/$35 fulfillment and $3.65/$3.79 merchant fees are one brand's figures for two months, not benchmarks.
- **Condition:** Fulfillment scope differs by product and location, so which charges fall into it will vary; the source recommends defining your own margin definitions and measuring them consistently rather than assuming an industry standard.
- **Condition:** Saving a dollar only matters at volume — at low order counts the same per-order improvement is negligible.

#### Calculate pre-marketing contribution using explicit delivery costs
Card: `db1cf398804d63740e615183` · Source: Everything You Need to Know About Finance in eCommerce.docx · Section: 1

Separate accounting gross profit from the management contribution metric used to fund ecommerce acquisition.

Applies when: Before setting marketing KPIs on a product, deciding whether to keep or cut a SKU, or comparing your margin to competitor pricing.

- Start from revenue excluding pass-through taxes and recorded discounts/refunds.
- Subtract landed product cost, fulfillment, outbound shipping, payment fees and incremental expected return costs exactly once.
- Illustration: $100 collected less $9 tax gives $91 revenue. Product $30 + inbound $4 + outbound $11 + pick/pack $4 + fees $3 + assumed return loss $15 leaves $24 contribution, or 24/91 = 26.4%.
- If the $15 includes revenue refunds, remove those from the revenue denominator too; document the definition rather than mixing net and gross bases.
- Use pre-ad contribution dollars to fund acquisition, overhead and target profit; calculate separately for each SKU and channel.
- **Condition:** This is an internal contribution model, not a universal statutory COGS classification.
- **Condition:** The source calls its full-delivery metric gross margin; preserve explicit included costs when comparing reports.

#### Separate dropship product and shipping costs in margin analysis
Card: `79cf39d0f59ab5f641daf2c3` · Source: Calculating COGS_ What Ecommerce Businesses Get Wrong.docx · Section: 0

Compare dropship and stocked orders on complete order contribution, with a documented accounting policy.

Applies when: When calculating margin for a drop-shipped product line, or when deciding whether to offer free shipping on a SKU.

- Separate supplier product charges, inbound costs where relevant and customer-delivery charges.
- Document how bundled supplier invoices are allocated and reported under the applicable policy.
- Do not let free versus separately charged shipping alone determine accounting classification.
- Include all merchant-paid delivery costs when comparing order contribution for stocked and dropship products.
- Reconcile internal contribution reporting with the accountant's inventory and expense classifications.
- **Condition:** Presented as a general rule with explicit exceptions, not a universal standard; confirm treatment with your accountant for statutory accounts.
- **Condition:** Deciding whether to negotiate freight or find suppliers sits outside this method — that is a sourcing decision.

### Retrieval and applicability
Search: `landed COGS gross margin contribution shipping payment`
Related domains: measurement, sourcing, offers
Mixed-folder candidate IDs: 013834b51f3c09687d62b861, cb72f5171b60d51280f77753, 3a6d05bf8a2a5ceacde401bc

- Does this advice fit the product lifecycle, market, audience and requested deliverable?
- Does it require proof, access, budget or assets the brand does not have?
- Does it change a fixed price, offer, policy or other explicit constraint?
- Are platform details or numerical claims current and substantiated?

### Output checks
- Deliver the specified artifact, not general advice about creating it.
- Use supplied brand facts; label hypotheses and missing inputs separately.
- Preserve relevant source conditions; do not copy another business’s proof or results.
- Include an owner, measurement and decision rule when proposing a test.
- Check the output against the requested constraints and owner feedback.

Stop after the requested artifact passes factual and brief checks; allow at most two revision passes, then report the unresolved issue.

## Build a practical cash forecast
Workflow ID: `finance-and-accounting.cash-forecast`

**Deliverable:** Cash forecast and action triggers

### Proposed decision sequence
1. Reconcile opening cash and known obligations
2. Model receipts, inventory commitments and operating payments by period
3. Stress-test downside cases and identify funding gaps

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Build a Mini Cash Flow Statement to Find Working Capital Needs and Runway
Card: `9d2823e986940b6ded26e7f0` · Source: Finance for eCommerce (1).docx · Section: 4

Reconcile net income with inventory purchases to project real cash burn and how much capital the store must raise.

Applies when: Deciding how much funding or cash buffer the store needs and when, especially for inventory-heavy CPG or subscription-box businesses.

- In a simplified bridge, start with net income, add back inventory COGS expensed, then subtract all actual inventory supplier cash payments, whether goods have sold or not.
- Add other non-cash and working-capital adjustments separately. Do not also subtract inventory/payables movements already captured by the supplier-payment bridge.
- Add any starting capital (source scenario begins with $500k raised) and roll the cash balance month by month.
- Expect cash to be choppier than net income: the source's example shows cash going negative around month 8 and again needing a large inventory outlay shortly after.
- Use the trough of the cash curve to size the raise: in the source's example, the business needed roughly $1-1.5M cumulative to reach profitability even though operating income turned positive earlier.
- Separately note the store's revenue run rate (last month's revenue x 12) as a real-time pacing metric alongside trailing 12-month actuals, and be explicit which one you quote.
- **Condition:** This mini cash flow ignores other assets and liabilities by design — it is not a full three-statement model.
- **Condition:** Capital need figures are the source's scenario and depend heavily on lead times, payment terms and growth rate.

#### Cash conversion cycle explains why ecommerce can't scale arbitrarily fast
Card: `beb1703b3d17d1f7b84e5f95` · Source: Everything You Need to Know About Finance in eCommerce.docx · Section: 2

CCC (DIIO + DSO − DPO) plus supplier lead time and payment terms caps real growth speed regardless of ad efficiency.

Applies when: Setting growth targets, planning purchase orders, or evaluating whether rapid ad-spend scaling is fundable

- Formula: cash conversion cycle = days inventory outstanding + days sales outstanding − days payable outstanding.
- Work through the compounding: if $50 gross profit lets you buy 11 units next cycle and yields $55, which buys 12, inventory purchasing grows only incrementally off prior gross profit.
- Add supplier lead time — e.g., a 90-day lead time with full upfront payment means you must fund inventory 90 days before selling it, potentially forcing a 90-day stockout while waiting for cash.
- Levers to fix it: negotiate better supplier terms (e.g., only 20% upfront, paying the balance on shipment — the source's example reduces stockout from 90 days to ~20), reduce lead time via a different manufacturer, or use inventory financing.
- Compare financing cost, repayment timing, guarantees and collateral in actual quotes; stress-test slower sales before borrowing.
- **Condition:** The source describes spend rising from $20k to $200k per month, a tenfold increase, with substantial inventory financing; this is an anecdote, not a benchmark.
- **Condition:** Growth capacity depends on working capital, supplier terms, lead times and margins; no universal annual growth ceiling follows from this example.

#### Vendor Terms and Cost-of-Capital Arbitrage
Card: `377b3fd122bfca19109b2922` · Source: The $3B E-Commerce Strategist_ The Playbook That’s Making Everyone Else Rich.docx · Section: 2

Negotiate net terms using each partner's cost of capital and cash needs — pay more margin for longer terms, or take on consignment over dropshipping and full inventory ownership.

Applies when: When negotiating supplier, agency, or software contracts and choosing between dropshipping, buying inventory, or consignment.

- Understand each counterpart's cost of capital and cash cycle; suppliers with cheaper capital (e.g., subsidized manufacturing) may accept a small price increase in exchange for longer net terms.
- Aim for payment terms that extend past your production and sell-through timeline so your customer's money pays the manufacturer — a negative cash conversion cycle.
- Recognize the trade matrix: some vendors value margin, some want committed/long-term dollars, some need cash flow — offer the thing they value for the term you want.
- Target consignment as the ideal middle: a supplier holds inventory on your behalf and you pay when you sell — you get dropshipping's cash benefit plus inventory pricing.
- Build trust with suppliers over time; consignment and long terms are granted on demonstrated reliability, not negotiation alone.
- **Condition:** Consignment and extended terms require relationships built on trust and track record.
- **Condition:** Extreme structures (e.g., an in-house lender floated to a vendor) require scale and leverage most brands don't have.

### Retrieval and applicability
Search: `cash flow inventory payment terms forecast working capital`
Related domains: measurement, sourcing, offers
Mixed-folder candidate IDs: e9d130295214c8e5fc500397, 5529a92593b370ddae321e69, 1dcdad671ee9b96da563ff65

- Does this advice fit the product lifecycle, market, audience and requested deliverable?
- Does it require proof, access, budget or assets the brand does not have?
- Does it change a fixed price, offer, policy or other explicit constraint?
- Are platform details or numerical claims current and substantiated?

### Output checks
- Deliver the specified artifact, not general advice about creating it.
- Use supplied brand facts; label hypotheses and missing inputs separately.
- Preserve relevant source conditions; do not copy another business’s proof or results.
- Include an owner, measurement and decision rule when proposing a test.
- Check the output against the requested constraints and owner feedback.

Stop after the requested artifact passes factual and brief checks; allow at most two revision passes, then report the unresolved issue.

## Diagnose margin deterioration
Workflow ID: `finance-and-accounting.margin-diagnosis`

**Deliverable:** Margin bridge and recommended investigations

### Proposed decision sequence
1. Align periods and accounting definitions
2. Bridge changes in price, mix, costs, returns and acquisition spend
3. Prioritise actions supported by the bridge

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Five core finance practices to run an ecommerce brand
Card: `8d570963a07c01bd206aac7f` · Source: Everything You Need to Know About Finance in eCommerce.docx · Section: 3

A closing checklist of five financial operating habits—margin literacy, live dashboards, new/returning separation, cash vs P&L plays, and constraint diagnosis.

Applies when: Setting your store's monthly financial operating rhythm or auditing which finance disciplines your team is missing before scaling spend.

- 1) Know your gross margin and calculate it correctly: identify variable costs, and distinguish product margin from gross margin and how each flows into contribution margin. Use these definitions consistently across the team.
- 2) Define your metrics and build live dashboards—not daily ROAS reports. Track acquisition MER, profit contribution, and ideally LTGP to CAC. The source argues weekly ROAS reporting is unproductive for core decision-making.
- 3) Separate new vs returning customer metrics: track new-customer economics, acquisition MER, new-customer profit contribution, new-customer revenue and new-customer cohort size separately, because the underlying levers differ (and feed forecasting).
- Coordinate inventory and advertising: additional borrowing raises interest expense and reduces cash/net profit. Interest alone does not change MER (revenue/ad spend); model sales and spend separately.
- 5) Use the P&L to identify the constraint in the business: structure it out, set KPIs at each level, and when you fall below target look above that level in the P&L to find what changed and which lever to pull.
- Attribute the daily-vs-weekly ROAS stance to the source as an opinion, not a universal rule.
- **Condition:** The daily-vs-weekly ROAS preference is the presenter's opinion, not an established benchmark.
- **Condition:** The five-point list is a summary framework; it does not define numeric thresholds for any metric.

#### Calculate contribution margin per order and post-marketing contribution
Card: `957cabf05b5f780f958ce6f8` · Source: Finance for eCommerce (1).docx · Section: 3

Structure an ecommerce P&L into net revenue, product COGS, gross margin, fulfillment, contribution margin, CAC and post-marketing contribution so each expense can be optimized separately.

Applies when: Setting or reviewing product-level and order-level profitability, or diagnosing why a store that looks profitable at gross margin is not producing operating income.

- Start at gross revenue (product sales plus tax collected where applicable) and subtract discounts and returns, then add shipping income you charge customers. Result: net revenue, which is effectively your AOV after discounts and returns for the period.
- Split COGS into product cost (manufacturing plus import freight plus duties/taxes to get product to the warehouse) and keep it separate from fulfillment cost (pick and pack, packing materials, 3PL charges, shipping to customer). A generic P&L lumps these together; splitting them is what lets you see which line is moving.
- Compute gross margin = net revenue minus product COGS. In the source case study it ran about 70–75%.
- Compute contribution margin = net revenue minus product COGS minus fulfillment. In the source example, $134 net revenue with $64 contribution margin, just under 50%.
- Compute CAC as total marketing spend divided by first-time purchases, then post-marketing contribution = contribution margin minus CAC. Source example: $22 and $12 post-marketing contribution per order, i.e. profitable on the first order at roughly a 1.5 contribution-margin-to-CAC ratio.
- Check merchant/credit card processing fees and include them — the source uses about 2.75% of revenue as a working assumption.
- Finally subtract operating expense per order to reach operating income. In the source example opex was about $8 and $6 per order and operating income was 11% and 5%, i.e. about $15 and $6 profit per unit.
- Remember the leverage: small per-order changes (knocking a couple of dollars out of one line) multiplied across thousands of orders is the difference between tens of thousands of losses and tens of thousands of profit.
- **Condition:** Gross margin is the highest figure, contribution margin lower, post-marketing contribution lowest — mixing the terms (calling gross margin contribution margin) causes wrong decisions.
- **Condition:** All percentages in the source are one case-study supplement brand in a specific period; do not treat them as targets.
- **Condition:** After the first order, returning customers generally carry little or no marketing cost, so first-order profitability is the ideal state — the source calls businesses with strong first-order profit exceptional.

#### Four Quarter Accounting vs Cash Flow: Tradeoffs Are Purposeful
Card: `20d19584680857c7948e03ba` · Source: The $3B E-Commerce Strategist_ The Playbook That’s Making Everyone Else Rich.docx · Section: 2

Profitability and cash flow are different games — knowingly sacrifice gross margin or P&L efficiency when it accelerates cash and optionality.

Applies when: When weighing a decision that hurts P&L margin but improves cash position, such as liquidation, longer-term vendor deals, or consignment.

- Keep the two views distinct: four quarter accounting analyzes the P&L; cash flow and the balance sheet are managed separately and can call for opposing moves.
- Prioritize growing the bank account — it creates optionality, especially when M&A and funding are constrained.
- Accept tactics that worsen the P&L (liquidation margins, discounting, extended supplier terms) when they convert dead stock or float into usable cash.
- Reinvest recovered cash into new inventory bets or growth rather than holding it in depreciating assets.
- Review both views regularly so tradeoffs are deliberate rather than accidental.
- **Condition:** Repeated P&L erosion without cash conversion isn't strategy — the tradeoff must produce usable cash.
- **Condition:** Overstating balance-sheet inventory to satisfy asset ratios obscures the cash reality.

### Retrieval and applicability
Search: `P&L gross margin returns discounts cost diagnosis`
Related domains: measurement, sourcing, offers
Mixed-folder candidate IDs: 29f6666ae3104498c96f3f74, 6b261e1e25a56d59c79b8638, f82391a766c6158726c2f5f1

- Does this advice fit the product lifecycle, market, audience and requested deliverable?
- Does it require proof, access, budget or assets the brand does not have?
- Does it change a fixed price, offer, policy or other explicit constraint?
- Are platform details or numerical claims current and substantiated?

### Output checks
- Deliver the specified artifact, not general advice about creating it.
- Use supplied brand facts; label hypotheses and missing inputs separately.
- Preserve relevant source conditions; do not copy another business’s proof or results.
- Include an owner, measurement and decision rule when proposing a test.
- Check the output against the requested constraints and owner feedback.

Stop after the requested artifact passes factual and brief checks; allow at most two revision passes, then report the unresolved issue.
