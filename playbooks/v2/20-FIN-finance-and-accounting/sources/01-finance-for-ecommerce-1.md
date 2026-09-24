# Finance for eCommerce (1)

source_id: 1GvhNMqu3NTACVEQwTEwpTWMlsVdrB_bV  |  folder: /20-FIN-finance-and-accounting  |  cards: 84  |  words: 64,922  |  type: transcript (compilation of 16 distinct YouTube video transcripts plus 1 live stream, all by the same presenter; the last segment repeats the discounts-vs-CAC video word for word)

credibility: All segments are by Eric Andrews ("Eric"), who runs a startup finance YouTube channel. He says he studied finance at Tulane University (graduated 2013), then worked in startups and consulting. He sells a "Finance for Startups" cohort course (he says 400+ executives have taken it), Excel courses, and runs a job board (startupfinancejobs.com). In later videos he is Director of Commerce Strategy at Ordergroove (transcribed "Order Group" or "Order Grove"), a subscription software vendor for enterprise brands. 6 segments are Ordergroove productions or sponsored by Ordergroove, so the prepaid, subscription and default-to-subscription advice comes from a vendor with a stake in it. Other sponsors: OpenStore (store valuation), Bainbridge (FP&A for Shopify), and an affiliate link for Clearco ($500 discount). Evidence: almost all numbers come from made-up or "anonymised" Excel models. A few claims cite Ordergroove merchant data with no sample size (retention curves for prepaid, 60 to 70% lift from defaulting the cart to subscription, 2.5x lifetime spend for prepaid). One case (Dollar Shave Club) uses third-party scraped transaction estimates. The accounting mechanics (3 statements, depreciation, capitalisation, churn denominator, cohort tables) are standard. Several transcript numbers are garbled by speech-to-text; corrected values are derived below where the arithmetic makes them certain.
date signals: "right now it is 2020" and freight costs "varying wildly" (contribution margin video). Coffee model roll-up labelled 2022 to 2025. Clearco "used to be called Clearbanc" (renamed around 2021). Dollar Shave Club bought by Unilever in 2016. Live stream near 20,000 subscribers. KPI video uses a "March 2026" cohort label. Ordergroove role and "400 executives" course line date the Ordergroove and Black Friday segments to the most recent years. US-specific assumptions throughout: merchant fees about 3% (or 2.75%), benefits 25% of salary including 401k, quarterly estimated tax, a 25% tax rate. No platform UI versions are named, so stale risk is low for the maths and high for fees, tax rules and financing offers.

scope note: The folder header says this source is core for unit economics and discount strategy. It also covers cash flow, runway, cohorts, churn, LTV, CAC payback, subscription models and Amazon FBA modelling, all in scope for 20-FIN. Amazon-specific launch tactics belong mainly in 22-AMZ; subscription offer and cart mechanics touch 03-OFF and 07-LPG; channel-level CAC and media buying belong in 11-ADC and 24-DEP. The header asks to skip Ordergroove pitches and the line-by-line $1.50 CPC grid; the grid's method and totals are kept here because the cards use them.

Segment map (used as T1 to T17 below):
- T1 Coffee subscription startup model in Excel, 48 months, $3M raise.
- T2 Most important ecommerce KPIs (trajectory, per-order unit economics, CAC, cohorts and LTV). Sponsor OpenStore.
- T3 Black Friday: 50% off sitewide vs buy one get one free.
- T4 How unit economics should evolve across the life cycle (idea to late stage), optimal vs sub-optimal.
- T5 Free cash flow case study (three-statement model).
- T6 Prepaid subscriptions and LTV (Ordergroove).
- T7 Contribution margins for ecommerce. Sponsor Bainbridge.
- T8 Discounts vs CAC (Ordergroove). T17 is an exact repeat.
- T9 Subscription box model part 1: unit economics, CAC, retention, revenue, KPIs.
- T10 Subscription box model parts 2 and 3: income statement, payroll, opex, tax loss, inventory, mini cash flow, runway.
- T11 Churn rate: calculation and lifetime.
- T12 Cohort analysis: retention, net revenue retention, LTV.
- T13 CAC payback for subscriptions (co-created with Ordergroove).
- T14 Live stream: subscription box case study, Dollar Shave Club, LTV levers, Q&A on LTV window.
- T15 Amazon FBA financial model and inventory financing (Clearco).
- T16 How to calculate customer lifetime value (coffee subscription).

## 1. What this source is for

It teaches an operator to prove, with arithmetic, whether a store makes money per order and per customer, and whether it has the cash to survive growth. The jobs: split the P&L into product cost, fulfillment, marketing and opex; compute contribution margin per order and post-marketing contribution; compute CAC, LTV (as lifetime contribution margin), CM:CAC, LTV:CAC and cohort-based CAC payback; model promos (percent off vs BOGO, discount vs ad spend); model subscriptions, prepaid bundles and churn; build a monthly model from ad spend down to operating income; and forecast inventory purchases and cash runway. It is strong on formulas and worked examples, weak on real benchmarks.

## 2. Principles

### 2.1 Margin definitions and the P&L

1. **Split COGS into product cost and fulfillment.** Product cost = manufacturing, import freight, duties and taxes, packaging and inbound freight to the fulfillment center (everything to get product ready to sell). Fulfillment = pick and pack, packing materials, 3PL charges, storage, shipping to the customer and (in T3 and T7) merchant fees. A standard accountant P&L lumps both into one COGS line; the source prefers the split so each line can be tracked and cut. Condition: this is the presenter's ecommerce convention, not GAAP presentation. (T2, T3, T4, T7) [4e8e7fd6e6e4] [ca717cbf0593] [1a6c983c0c2f] [957cabf05b5f]

2. **Three margins, three jobs.** Gross margin ("ecom gross margin") = revenue - product cost; highest. Contribution margin (CM) = revenue - product cost - fulfillment; the profit available for marketing and opex, and "the margin we work back from". Post-marketing contribution margin = CM - marketing; lowest; tells you if you made a profit after producing, delivering and acquiring. People use gross margin and CM interchangeably, so define them for your business and measure them as separate ideas. (T7) [68431c491a0c] [957cabf05b5f]. Conflict inside the source: in T9, T10 and T8 he says "people refer to gross profit in ecommerce mostly as contribution margin" and "gross profit AKA gross margin AKA contribution margin, they all mean the same thing", and his gross profit there already includes fulfillment. See section 9.

3. **CM is the ceiling on CAC.** "Your CAC should be $83 or less" when CM per order is $83 (T4). "You have $64 to spend before you are break even on the product" (T7). [ca717cbf0593] [68431c491a0c]

4. **Post-marketing contribution is the core profitability gauge.** If CM minus marketing is not positive, "your business cannot make money, there is no way", because nothing is left for payroll and opex. It is the P&L view of LTV - CAC. He calls it his favourite metric and says few businesses track it. Operating profit exists only when post-marketing CM exceeds all other opex. (T9, T10) [bf82ba8e8bc2]

5. **Small per-order savings decide profit at volume.** Knocking a couple of dollars off any single line (freight, pick and pack, fees) adds a few dollars per order, which across thousands of orders is "the difference between tens of thousands of dollars of losses or tens of thousands of dollars of profit". Condition: only matters at volume. (T7) [2978d63684ea]

6. **Know which count you analyse.** Units > orders > customers (orders often carry 1.1 to 1.3 units). Be explicit whether a metric is per unit, per order or per customer. (T2) [49110942deea]

7. **Percent-of-revenue view shows trajectory.** Lay every line next to its percent of revenue to answer: is revenue growing, are margins predictable, are we getting more efficient. Marketing percent will bounce while scaling. (T2) [c160135c9bd3]

8. **Unit economics decide everything.** "If your unit economics work, your business works. If your unit economics don't work, your business will never work." (T3) "If you don't know how much money you make on one order, stop everything you're doing and figure it out." (T14) [31dce846c93c]

### 2.2 CAC

9. **CAC (also CPA) = marketing spent to get 1 new customer to buy for the first time.** Denominator is new customers (first orders) only; returning customers are excluded because they come back through email, subscription or organic and need little paid marketing. Including them "gives you a CAC that makes no sense". (T2, T8, T14) [6fe6a3b41072] [8cab64f326b9]

10. **Blended CAC is directional; channel CAC needs a funnel map.** Blended CAC = total marketing / total new customer orders. Channel CAC (Facebook, Google) needs you to map top-of-funnel exposure, nurture (content) and conversion activities (deals, discounts) and piece them together. (T2) [6fe6a3b41072]

11. **Paid CAC is what constrains growth.** Blended CAC = total spend / all new customers; paid CAC = spend / paid-attributed new customers. Paid channels can scale fast (he says Facebook from $500 a day to $20,000 a day in one day, 20x in one month); organic is hard to grow fast and may be friends and family. So the test is whether paid CAC is below LTV. (T14) [8cab64f326b9]

12. **CAC is a function of conversion rate.** If more visitors convert, cost per acquisition falls. (T3, T8) [5425adb4473f] [1247e2cd031e]

13. **CAC is unknowable before launch.** It depends on copy, product, brand awareness and audience. Put in a placeholder, then replace with observed CAC and re-forecast. (T9) [563870c81120] [1b23d41ee499]

### 2.3 First order vs lifetime

14. **Ecommerce should try to break even or better on the first order.** Reason: many ecommerce customers buy only once. Exceptional stores are very profitable on the first order after marketing. If profitable on the first order, all later orders are "pure profit" because they carry little or no marketing. Condition: the presenter's stated preference, not a universal law. (T2, T4, T7) [c160135c9bd3] [a004a45541ef] [957cabf05b5f]

15. **Two valid models.** Route 1: good margins, break even or better on order 1 (needed for buy-once categories such as many apparel items). Route 2: very high lifetime orders (customers buy 5, 10, 15 times), which can lose more on order 1 and earn it back on the tail. Subscribe and save or subscription boxes are "an antidote to low lifetime orders" for consumables. CM:CAC below 1 on the first order: "yes if you have a lot of repeat buyers, no if you have a lot of one-time buyers". (T4) [a004a45541ef] [cd36c8b5eacc]

16. **Each new customer should be more profitable than the last.** If unit economics deteriorate, "your business at 10x the size might drive its profits to zero" or negative. He says many large DTC brands scaled beyond where they should with bad unit economics. (T4) [e2eaed277a0d]

17. **Do not scale spend to fix bad unit economics.** A business with CM:CAC and LTV:CAC below 1 "should not be scaling until it can fix its unit economics", even after raising a $20M Series A/B. (T4) [cd36c8b5eacc]

18. **LTV is lifetime profit, not lifetime revenue.** LTV = total contribution margin (or gross profit) a customer generates across all orders. "Your revenue is kind of irrelevant, what matters is how much profit." (T2, T4, T9, T12, T16) [613635831aff] [c1e5e9113ebe]

19. **Cohorts are the only real way to see retention and LTV.** "The only way to understand customer retention is using cohorts." Works for subscription and non-subscription stores. It is one of the first things a VC asks for. (T2, T12, T14) [540b5bdda637] [9e1b24779308]

20. **Hold CAC flat for repeat orders only if you spent nothing to get them.** In T2 he assumes repeat orders came via email list, so lifetime CM is divided by the same CAC. [a592b3f28c58]

### 2.4 Discounts and promos

21. **A discount and CAC are the same money.** "Whether you give $100 to Facebook via its ad platform or you give $100 to your customer via discount, the contribution margin post marketing is the same." Add discount + CAC together as the true cost of acquisition. If a discount lifts conversion enough to cut CAC by the same dollars, post-marketing CM per customer is unchanged. Condition: holds only when CAC falls by the same dollar amount as the discount. (T8) [aa80d087ca61] [8723bc22dfe2] [1247e2cd031e]

22. **Pick the discount level that maximises total profit, not per-customer margin.** Compare scenarios on total post-marketing CM at the same ad spend. "It's not necessarily that giving the biggest discount will make you the most money... it can go both ways." Some brands win on volume with worse unit economics; others shrink revenue and keep "spectacular unit economics on a smaller subset". (T8) [993ecc7a19f0]

23. **One pool for discounts and marketing.** Set one annual pool (his example $5M), spend it to zero, and choose the split between discounts and ad platforms that maximises sales and profit. Whoever runs marketing should own it. (T8) [1247e2cd031e] [8acd81a0345e]

24. **Attach the best discounts to a loyalty or subscription on-ramp, not a flash sale.** Flash-sale converters "a lot of times actually will not buy without a big discount"; people who join a loyalty or subscription program through the offer "self-selected into having a high customer lifetime value". "Give your best discounts to your best customers." He is "not advocating discounting like crazy", which can damage the brand. (T8) [8acd81a0345e] [aa80d087ca61]

25. **Percent off gives away revenue; BOGO gives away cost.** With 50% off, "what the customer gets, you lose". With two for one, the customer gets a unit worth the full price to them, but the extra unit costs you only its product cost. Customers read both as "twice as much for half the price", so conversion and CAC lift are similar. Condition: works when unit product cost is low and the extra unit ships in the same box at little extra weight. (T3) [5425adb4473f] [13df6c347b0e]

26. **Make money on Black Friday customers on the first order.** Black Friday customers "are notorious for having really bad retention" and many buy once. Subscription brands sometimes accept a loss and try to make it back later; he still advises everyone to be profitable. (T3) [5425adb4473f]

27. **Gift product when it is cheap to make.** Test buy two get one free or gift with purchase instead of percent off whenever product cost is low. (T3) [13df6c347b0e]

### 2.5 Subscriptions, prepaid and churn

28. **Churn applies only to subscriptions.** Churn rate = percent of subscribed customers who cancel in a stated period. A DTC store selling one order at a time has no churn; use cohort retention. Always state the period (11% monthly and 11% annual are very different). (T11) [d4b9ff187dc2]

29. **Churn denominator is the prior period's subscribers.** Cancellations happen at renewal, so they come from last period's base, not this period's total or this period's new signups. (T9, T11) [e587bb652cdc] [1903080a3a75]

30. **Average lifetime = 1 / churn.** Every subscription operator "should have memorised" it. Churn is a leading indicator of lifetime, so lower churn raises revenue, lowers marketing needed and raises customer profit, even when revenue is growing fast. (T11) [fe4a0757982c]

31. **Churn rate is a lazy fallback; cohorts are better.** Churn misses the shape of cancellation over the lifetime (Dollar Shave Club lost about 25% in month 1 but only about 10 points across all of year 2). Use it when you have little data. (T14) [136827bb25c7]

32. **Subscription customers have lower AOV and lower margin per order but higher lifetime value.** One-time buyers bundle big orders and rarely return; subscribers buy smaller orders for longer. He says subscriptions "usually drive 3 to 5 times as much revenue per customer". Blended CM percent falls as the subscription mix rises; that is expected. (T9, T10) [17cd13e806d9] [69e7ae8e0048]

33. **Flat subscribe-and-save attracts one-time takers.** Across "hundreds" of large Ordergroove programs, the highest LTV comes from increasing discounts over the lifetime (for example 10% off order 1, 15% order 2, 20% order 3, 25% order 4 onward) and from prepaid subscriptions. Flat incentives get people who "subscribe just as a one-time offer and then cancel right away". Vendor claim, no data shown. (T9) [d8e1973bffac] [17cd13e806d9]

34. **Prepaid subscriptions trade margin for locked retention and upfront cash.** Offer a bigger discount than anywhere else for prepaying 3, 6 or 12 orders shipped over time. Operators usually reject them on per-order margin and "underestimate the retention lift". Prepaid also creates negative net working capital: customers fund the inventory you will ship them. Common in B2B SaaS and education, rare in ecommerce. (T6) [d8e1973bffac]

35. **Default the cart to subscription to lift signups.** Ordergroove data: about 60 to 70% more new subscription signups. Vendor claim. (T9) [013b592e17af]

36. **Retention is the biggest LTV lever.** Cutting churn from 27% to 20% raised churn-based LTV 35% in T14. Tools: email, great customer service, flexible cancellation (skip, every other month, pause), and automation fast enough to catch the cancel. (T14) [86fcb4012931]

37. **Compete on value, not price.** Loyal customers are less price sensitive, which gives pricing power. Buyers who come for a cheap price focus on price. Raise AOV with tiers and upsells and price increases. (T14) [ed010f896be7]

38. **COGS falls with volume; renegotiate.** At about 50 orders a month you get the worst pricing (small batches, fulfillment minimums such as 100 orders a month). At thousands of orders, buy wholesale and renegotiate fulfillment and shipping. "Attack your LTV from every front." (T14) [482dba787e59]

### 2.6 Cash, inventory and financing

39. **Net income is often misleading; free cash flow shows what is really happening.** FCF = operating cash flow - investing cash flow; "once the business has funded 100% of its internal operations, is there any cash left over". (T5) [7404abfd63fa] [8c56490f81a2]

40. **The P&L hides lumpy cash.** Inventory is bought in big chunks but expensed only when sold. Depreciation spreads asset cost over 3 or 5 years. Capitalised software moves engineer payroll to the balance sheet (most software over 36 months). Loan principal repayments never hit the P&L (only interest does). Taxes accrue monthly but are paid quarterly as estimates. (T5) [2ff9cc0805c2] [8187da83315e]

41. **Operating profit is not "making money" in an inventory business.** The income statement matches unit cost to revenue at sale; cash and balance sheet show when cash actually left. You need both views. (T10) [9d2823e98694]

42. **Many ecommerce businesses die of liquidity, not unit economics.** "A lot of e-commerce businesses go broke not because they're not making money at the customer level but because they run out of liquidity and they have bad working capital dynamics." Inventory "will make or break your profitability and your cash flow". (T6, T10) [8187da83315e]

43. **Selling equity to fund inventory is expensive.** Selling permanent ownership to finance 3 months of inventory is, in his words, "absurd". He recommends looking at non-dilutive revenue-based financing (Clearco for ecommerce, Pipe for SaaS recurring revenue). He had an affiliate link. (T15) [a20812fa24c9]

44. **Know runway early.** Fundraising takes a long time; know when cash goes negative well in advance. (T1) [def705c265c2]

### 2.7 Modelling discipline

45. **Everything flows from ad spend.** New customers = ad spend / CAC; ad spend is the lever for burn, runway and revenue. Tweak spend and CAC at the end of the build. (T1, T9, T15) [563870c81120] [939b20dbac4b]

46. **Keep assumptions in one place, in blue.** Dark blue = hard-coded input; black = formula. (T1, T14) [7b2e56bcad5a]

47. **Keep payroll models simple.** Salary / 12 x headcount by bucket, plus benefits. "Please don't" build 700-row multi-tab payroll models unless necessary. (T10) [f39ad32b21d7]

48. **Plan for the unknown.** Add a catch-all opex line as a percent of revenue ("the I have no idea what's coming bucket"). (T1) [50708132adc1]

49. **Be conservative on churn and lifetime orders.** Use 25% monthly churn for a subscription box model ("better to be conservative... if you outperform that's just upside"); use the lifetime-orders figure from the cohort with the most history rather than extrapolating. (T2, T9) [b6fb728dba04] [1903080a3a75]

## 3. Procedures

### 3.1 Per-order unit economics and P&L waterfall (T2, T7, T14)

1. Gross revenue = product sales (T7 also includes taxes collected). [957cabf05b5f]
2. Subtract discounts and returns/refunds. Add shipping income charged to customers. Result = net revenue; net revenue / orders = AOV. [957cabf05b5f] [895584eaf5b7]
3. Product COGS = product cost + import freight + import duties and taxes (+ packaging and inbound freight in T3). Gross margin = net revenue - product COGS.
4. Fulfillment = pick and pack + packing materials + other 3PL charges + shipping to customer + merchant fees. CM = net revenue - product COGS - fulfillment.
5. Marketing: paid ads, influencers, other marketing, agencies. Post-marketing CM = CM - marketing.
6. Opex: payroll, software, consultants, rent, miscellaneous. Operating income = post-marketing CM - opex.
7. Put a percent-of-revenue column next to every line, month by month. Order the lines: revenue, product COGS, product gross profit, fulfillment, CM, marketing, post-marketing CM, opex, operating income. [c160135c9bd3]
8. Divide each line by total orders: AOV = revenue / orders; product COGS per order = product COGS / orders; fulfillment per order = fulfillment / orders; CM per order = AOV - product COGS per order - fulfillment per order. [49110942deea]
9. If months bounce, compute a trailing multi-month average: total revenue over the period / total orders over the period, and the same for each cost line. [49110942deea]
10. Divide each fulfillment line by revenue to see which charge is moving (for example shipping up while pick and pack stable). [4e8e7fd6e6e4] [2978d63684ea]
11. Pull a separate product-level report and compute revenue, gross profit and CM per unit for top SKUs. [2a88bf14790c]
12. Per-order CM is the number to compare with CAC per new order.

### 3.2 Blended and paid CAC (T2, T14)

1. Pull new customer orders (first orders only) and total marketing spend for the same period. [6fe6a3b41072]
2. Blended CAC = total marketing / total new customer orders.
3. Split new customers into paid-attributed and organic using Google Analytics, Google Ads and Facebook Ads Manager `[verify UI]`. Paid CAC = paid spend / paid new customers. [8cab64f326b9]
4. Compare CAC per new order with CM per order each month. A month where CAC > CM per order is likely a loss month (T2: July). [6fe6a3b41072]
5. For channel CAC, map the funnel by stage and channel (exposure, nurture, conversion). The source gives no further how. [6fe6a3b41072]

### 3.3 Cohort retention, NRR and LTV table (T2, T12, T14)

1. Group customers by first purchase month. Month of first purchase = month 0. Anyone buying later stays in their original cohort. [9e1b24779308] [540b5bdda637]
2. Fill each row with the count (or orders, or revenue) of that original group in month 1, 2, 3... Always reference the original group, not last month's survivors. [540b5bdda637]
3. Retention % = month n count / month 0 count. Lock the month 0 column (F4 in Excel adds the $) and copy across. [90b11f77327e]
4. To total one calendar month, read diagonally: this month's new cohort month 0 + last month's cohort month 1 + the cohort before that month 2, and so on. Check that the diagonal of repeat orders ties to reported returning-customer orders (T2: 122). [b6fb728dba04] [2650453af6e8]
5. Delete cells for future months instead of leaving zeros; recent cohorts are incomplete, so the table looks diagonal. [90b11f77327e] [2650453af6e8]
6. Build the same grid with revenue. Net revenue retention (NRR, NDR) = cohort revenue in month n / cohort revenue in month 0. Above 100% is expansion revenue (upsells, extra products), not an error. [20b50a304d0f]
7. Cumulative lifetime revenue = running sum of each cohort's revenue by month. Revenue per customer = cumulative revenue / original cohort count (locked). [e564ae6200ef] [f272a137245d]
8. LTV = revenue per customer x gross margin (lock the margin cell to flex it). [e564ae6200ef]
9. Orders per customer = cumulative cohort orders / cohort customers. Use the cohort with the most history as the lifetime-orders assumption. [b6fb728dba04]
10. Compare cumulative profit per customer with CAC month by month to find the crossover. [e564ae6200ef]
11. Data source: SQL from the database by an analyst, apps or plugins, or Google Analytics cohort reports `[verify UI]`. [90b11f77327e]

### 3.4 First-order vs lifetime test (T2, T4)

1. First order: revenue = AOV x 1; CM = AOV - product cost - fulfillment; CM:CAC = CM / CAC; first-order profit = CM - CAC. [a592b3f28c58]
2. Lifetime: revenue = AOV x lifetime orders; LTV = CM per order x lifetime orders; LTV:CAC = LTV / CAC; lifetime profit = LTV - CAC. [a592b3f28c58] [e2eaed277a0d]
3. If CM:CAC < 1 on the first order, check cohort repeat orders before scaling. [613635831aff] [a004a45541ef]

### 3.5 Promo modelling: percent off vs BOGO (T3)

1. Model the baseline: conversion rate, CAC, gross AOV, net AOV after refunds/returns, product COGS, fulfillment COGS, CM, CM - CAC, monthly orders. [5425adb4473f] [1a6c983c0c2f]
2. Model percent off: assume conversion lift and lower CAC; assume most buyers take 1 unit so order value falls; hold product COGS fixed; adjust only merchant fees on lower revenue. [5425adb4473f]
3. Model BOGO: price paid = normal AOV; product COGS doubles; shipping rises only a little for a light product in one box; pick and pack a little more; merchant fees about the same as normal. Assume a similar conversion and CAC lift. [13df6c347b0e]
4. Compare CM and CM - CAC per order, then multiply by expected promo order volume.
5. The source treats "no refunds or returns during a promo" as best practice. See section 9 for the legal caveat.

### 3.6 Discount vs CAC scenario grid (T8)

1. Hold ad spend equal across scenarios. Sessions = ad spend / blended CPC. [8723bc22dfe2] [1247e2cd031e]
2. For each discount level, net AOV = list price - discount.
3. Assume a conversion rate per discount level. Purchases = sessions x conversion rate. CAC = ad spend / purchases.
4. Per customer: CM (after discount) = net AOV - COGS; CM post-CAC = CM - CAC. Also compute discount + CAC as "true cost of acquisition".
5. Whole business: net sales = purchases x net AOV; total COGS = purchases x COGS; CM pre-marketing = net sales - total COGS; post-marketing CM = that - ad spend. [993ecc7a19f0]
6. Pick the scenario with the highest total post-marketing CM, within brand limits. Treat it as a "future strategy split test" before committing. [1247e2cd031e] The source does not say how to run that test.

### 3.7 Prepaid subscription LTV (T6)

1. Per segment (one-time, 3-order prepaid, 6-order prepaid): AOV after discount, product COGS, fulfillment, gross profit per order and margin. [d8e1973bffac]
2. Build a 12-month retention cohort of 1,000 new customers per segment.
3. Lifetime orders = total orders in 12 months / 1,000.
4. LTV = lifetime orders x gross profit per order.
5. Weighted LTV for a mix = sum of (segment share x segment LTV). Compare with today's mix.
6. Note the cash benefit: prepaid collects cash before product is made.

### 3.8 Subscription box model, part 1 (T9)

1. Unit economics per segment: transactional (ad hoc) and subscription, each with undiscounted AOV, refund %, discount %, net AOV, product COGS, fulfillment COGS, card fees (2.75% of collected revenue), CM and CM %. [17cd13e806d9]
2. Ad spend ramp by month (inputs in blue). [563870c81120]
3. CAC by month (placeholders, then observed). New customers = ROUND(ad spend / CAC, 0). [1b23d41ee499]
4. Split new customers into transactional vs subscription by month, and plan the triggers that shift the split (stronger offer, tilt discounts to subscribers, default cart to subscription). [013b592e17af] [1903080a3a75]
5. Transactional repeats: measure return rate = returning customers this month / customers acquired in the trailing 6 months. Forecast returning customers = trailing-6-month customers x return rate. Use whatever months exist until 6 have accrued. [c1e5e9113ebe]
6. Subscriptions: churned = prior month total subscriptions x churn rate (negative). Total subscriptions = prior total + new - churned. [1903080a3a75]
7. Revenue per segment: gross revenue = transactions x undiscounted AOV; subtract refunds and discounts; net revenue = new x net AOV + repeat x net AOV. For subscriptions, repeat = total subscriptions - new (the survivors). COGS = transactions x per-order COGS. [895584eaf5b7]
8. Check: rolled-up gross profit % per segment must equal the unit-economics % (68% and 59% in T9). If not, a formula is wrong. [f1bd2de486c0]
9. Consolidate: total orders, gross revenue, net revenue, COGS, CM; then post-marketing CM = CM - ad spend. [e3d22c4449b1]
10. KPIs: annualised run rate, subscription vs transactional revenue split, CAC, LTV per segment and weighted, LTV:CAC, LTV - CAC. [e3d22c4449b1]

### 3.9 Subscription box model, parts 2 and 3 (T10)

1. Income statement: gross revenue, refunds, discounts, net revenue (split first-time vs returning), COGS, CM, advertising, post-advertising CM. [895584eaf5b7]
2. Payroll: 3 to 4 functional buckets (for example marketing, creative, operations, exec/admin) with an average salary each; headcount grid by month; monthly cost = salary / 12 x headcount (lock the salary column); benefits and taxes = total monthly payroll x 25%. [f39ad32b21d7]
3. Other opex: other marketing (influencers, branding), consultants (1099 contractors), software, miscellaneous as manual budget lines. [f39ad32b21d7]
4. Operating income (EBIT) = CM - total opex (payroll + other opex including advertising). EBIT margin = EBIT / net revenue. [f39ad32b21d7]
5. Tax loss asset: track cumulative losses; pay tax (25% in the model) only after cumulative profits have used up past losses. Net income = operating income - taxes. [b8599dca5b33]
6. Inventory: pull forecast orders; set lead time (3 months) and cycle time (4 months); order today enough to arrive after the lead time and last the cycle; roll inventory = prior - orders + arrivals. [308a0d76128c]
7. PO cost = units x weighted product cost per unit (weights = order mix by segment). [308a0d76128c]
8. Mini cash flow: opening cash (money raised) + net income - inventory purchases + product COGS of units sold (added back because that inventory was paid for earlier) = closing cash. [9d2823e98694]
9. Find the lowest cash point. Size the raise to cover it; test raise timing (for example a second raise at month 6). [9d2823e98694]

### 3.10 48-month startup model (T1)

1. Timeline M1 to M48 across the top; freeze panes (View tab > Freeze Panes) `[verify UI]`. [111c8bab5864] [7b2e56bcad5a]
2. Acquisition tab: ad spend ramp; paid CAC improving over year 1; new customers = spend / CAC; monthly churn; total orders = (new + prior total) x (1 - churn). [111c8bab5864]
3. Assumptions block (blue): AOV, refunds % of new-order revenue, discounts % of new-order revenue, COGS lines as % of revenue, headcount and salaries, benefits %, other marketing, technology, unknown bucket. [111c8bab5864]
4. Revenue: gross = AOV x total orders; discounts = -(AOV x discount % x new orders); refunds = -(AOV x refund % x first orders); net revenue.
5. COGS lines = % x revenue (lock the revenue row with $). Gross profit = net revenue - COGS; gross margin % = gross profit / net revenue.
6. Personnel = salary / 12 x heads (F4 to lock); benefits = sum of salaries x 25%. [66d5d76e9b71]
7. Other opex = ad spend (linked from acquisition tab) + other marketing + technology + unknown bucket. Operating income = gross profit - total opex (pre-tax). [50708132adc1]
8. Roll-up tab: quarters and full year by year; only sums from the monthly model; add starting cash and cash balance; runway = periods until cash turns negative. Sanity check: last 12 months operating profit equal in both tabs. [def705c265c2]
9. Format: top and double-bottom borders on revenue, gross profit and operating profit; accounting format; suppress zeros; build keyboard-only where possible. [7b2e56bcad5a]
10. Use the model to test fixes (lower packaging or product cost %) and see if break-even moves earlier. [da1cbdf76860]

### 3.11 Churn and lifetime (T11, T16)

1. Collect per period: subscriptions at end of prior period, new subscriptions, cancellations. [e587bb652cdc]
2. Churn = cancellations / prior-period subscriptions. [e587bb652cdc]
3. Lifetime (in periods) = 1 / churn. For annual churn, convert to months by x 12. [fe4a0757982c]
4. Churn LTV = GP per order (or AOV x margin) x lifetime; with multiple orders per month, x orders per client per month. [0b060b80b16f] [136827bb25c7]
5. Check visually: start a cohort, multiply by (1 - churn) each month, sum revenue x margin until the cohort is gone, divide by starting clients. It should match. [8b747d69f620]

### 3.12 Cohort CAC payback (T13)

1. Take one monthly cohort (count N). Total CAC outlay = N x CAC. [9a3cda2fe90f]
2. Retention by order (or month): survivors in each period.
3. Gross profit per period = survivors x GP per order.
4. Cumulative GP; payback period = first period where cumulative GP >= total CAC outlay.
5. Measure in months for monthly-billed products; in number of orders when customers can skip or ship every 2 to 3 months. [9a3cda2fe90f]
6. After payback, read the tail: how much profit accrues after break-even. [d78b5a172074]
7. Scenario-test CAC values to see break-even month sensitivity. [9a3cda2fe90f]

### 3.13 Amazon FBA model (T15)

1. Unit economics: price, FBA fulfillment fee, landed product cost to Amazon; GP per order. [ab551552b79e]
2. Paid CAC = CPC / conversion rate. [e9dcc756a117]
3. Lifetime GP = GP per order x lifetime orders; LTV/CAC. [ab551552b79e]
4. Marketing budget ramp; paid orders = ROUND(budget / CAC, 0); organic orders = ROUND(paid orders x paid-to-organic ratio, 0), ratio rising each month; total = paid + organic. [e9dcc756a117]
5. Inventory: starting units; purchase row; arrival row = purchase shifted by lead time; total inventory = prior - sold + arrivals; never let it go negative; size the next PO from the first negative month. [49138d1247d7]
6. Inventory investment = units x unit cost; use this cash line (not per-unit COGS) for cash planning. [49138d1247d7] [939b20dbac4b]
7. Post-marketing profit = revenue - FBA fees - inventory investment - advertising; cash = starting cash + running profit. [939b20dbac4b]
8. If cash goes negative, model revenue-based financing: remove the inventory purchase row and add a repayment of a % of revenue from when that inventory sells, plus a flat fee. [a20812fa24c9] (The card rewrites this step; see section 9.)

## 4. Rules, thresholds and numbers

| rule | number or threshold | condition | source's basis | card id |
|---|---|---|---|---|
| CM:CAC on first order | > 1 (break even or better) | most ecommerce, all stages; buy-once categories must | T4 opinion and model | [7eeee3aaceae] [a004a45541ef] |
| Best businesses first-order CM:CAC | 3 to 5x | exceptional stores | T4 opinion | [7eeee3aaceae] |
| Late-stage LTV:CAC | 5+ (model shows 6.7) | repeat-driven business | T4 model | [7eeee3aaceae] |
| LTV:CAC 1.0 | not acceptable | leaves nothing for opex | T4, T14 | [e2eaed277a0d] [79a98ff8e618] |
| LTV:CAC target | 2 to 3 or above | subscription box to grow profitably | T14 opinion | [79a98ff8e618] |
| SaaS LTV:CAC | up to about 6 | lifetimes 5+ years | T14 opinion | [79a98ff8e618] |
| LTV:CAC below 1 | "impossible" / upside down | any business | T9, T10 | [e3d22c4449b1] |
| Max CAC | <= CM per order (first-order rule) or <= LTV (lifetime rule) | depends on repeat rate | T4, T14, T16 | [ca717cbf0593] [8b747d69f620] |
| Returns and refunds | 5 to 10% of gross revenue | "a lot of different verticals" | T3 opinion | [1a6c983c0c2f] |
| Refunds assumption | 5% of new-order revenue (T1); 4% (T9) | model inputs | T1 "pretty typical" | [111c8bab5864] [17cd13e806d9] |
| Merchant fees | about 3% of revenue (US, "basically always"); 2.75% (T9, T10) | US card processing | opinion | [2978d63684ea] |
| Benefits load | 25% of salary | US: healthcare, payroll tax, 401k | T1, T10 | [66d5d76e9b71] [f39ad32b21d7] |
| Unknown opex bucket | 10% of revenue forever | planning model | T1 | [50708132adc1] |
| VC model horizon | 48 months (4 years), monthly | investor model | T1 | [da1cbdf76860] |
| Software capitalisation | 36 months useful life | "most software" | T5 | [2ff9cc0805c2] |
| Depreciation | 3 or sometimes 5 years | depends on asset | T5 | [2ff9cc0805c2] |
| Subscription box churn | 25% monthly "common"; use it to be conservative | modelling | T9 opinion | [1903080a3a75] |
| Transactional return rate | often 3 to 5% of trailing-6-month customers per month | non-subscription | T9 his experience | [c1e5e9113ebe] |
| Default cart to subscription | +60 to 70% new subscription signups | Ordergroove data | T9 vendor claim | [013b592e17af] |
| Prepaid vs flat 20% subscribe and save | about 2.5x lifetime spend | Ordergroove data | T9 vendor claim | [17cd13e806d9] |
| Prepaid roll-off | about 50% roll off, 50% re-enroll at end of each prepaid term | Ordergroove merchants | T6 vendor claim | [d8e1973bffac] |
| One-time buyer retention | about 10% reach order 2, 5% order 3, 3% order 4; 1.2 orders in year 1 | T6 example | vendor "realistic" | [d8e1973bffac] |
| Subscriptions vs one-time | 3 to 5x revenue per customer | usual | T9 opinion | [17cd13e806d9] |
| Supplements gross margin | 50 to 70% | supplements only | T9 opinion | [17cd13e806d9] |
| Black Friday conversion | jumps to 4 to 5% (from 1.75%) | big list, organic, prospecting and remarketing | T3 "normal" | [5425adb4473f] |
| Amazon FBA fees | about 20 to 25% of revenue | depends on weight and size | T15 "what a lot of people find" | [ab551552b79e] |
| Amazon conversion | about 10% sitewide "supposedly"; category 2 to 4% up to 30% niche; model 7.5% | research per category | T15 | [e9dcc756a117] |
| Regular site conversion | 2 to 3% "pretty good" | own website | T15 opinion | [e9dcc756a117] |
| Amazon reviews target | about 100 (one founder) | before organic ranking | T15 anecdote | [14761dd09c81] |
| Paid-to-organic ramp | start 10%, +10 points a month | Amazon model | T15 assumption | [e9dcc756a117] |
| NRR in best SaaS | > 150% | SaaS, expansion revenue | T12 | [20b50a304d0f] |
| CAC payback error | real payback 20 to 100%, sometimes 200%, longer than people think | not cohortised | T13 his experience | [9a3cda2fe90f] |
| Churn lifetime bands | 25% = 4 mo; 20% = 5; 15% = 6.7; 10% = 10; 5% = 20; annual 40% = 2.5 yrs = 30 mo | constant churn | T11 | [fe4a0757982c] |
| LTV plateau window | about 12 months at 25% monthly churn | find where cumulative revenue stops rising | T14 Q&A | [8fcbcb2cd9ba] |
| Short LTV window | 60 to 90 days understates | long repurchase cycles, gifting | T14 Q&A | [8fcbcb2cd9ba] |
| Payroll model | no 700-row multi-tab models | simple startup | T10 | [f39ad32b21d7] |
| Clearco eligibility | ecommerce or SaaS with 6+ months of $10,000+ monthly revenue; Clear Angel $10,000 to $25,000 for $2,000 monthly revenue, 2% of revenue for 4 years | historical, affiliate | T15 `[web check: current Clearco products and terms]` | [a20812fa24c9] |
| Clearco cost | repay a % of revenue (example 30%) plus flat 6 to 12% fee; offer in 24 hours, funds in 3 to 5 days | historical | T15 `[web check]` | [a20812fa24c9] |
| OpenStore valuation | needs six figures annual revenue; offer in 24 hours | sponsor | T2 `[web check]` | none |
| Ordergroove fit | brands doing > $1M in subscriptions | vendor pitch | T6, T8, T9 | none |

## 5. Diagnostics and checks

| what to check | how | good | bad | what to do next | card |
|---|---|---|---|---|---|
| Trajectory | revenue month over month; margin % by line | revenue up, CM % stable (T2: 43, 41.5, 42%) | margins drifting | find the line that moved | [c160135c9bd3] |
| Loss month cause | percent-of-revenue P&L | trace to 1 line (T2: marketing 29% to 39% caused the loss) | reacting before tracing | fix that line | [c160135c9bd3] |
| Order-level profit | CM per order vs CAC per new order | CM >= CAC | CAC > CM (T2 July) | cut CAC or raise CM before scaling | [6fe6a3b41072] |
| Fulfillment drift | each fulfillment line / revenue | stable | shipping or 3PL creeping up | renegotiate, check carrier | [4e8e7fd6e6e4] |
| SKU profit | per-unit GP and CM for top SKUs | know $ vs % leader | only order-level view | choose on cash per order or margin rate | [2a88bf14790c] |
| Promo margin dip | GM % in promo month vs next months | dip explained by discount, then recovery | dip from cost lines (air freight) | read each COGS line | [183999c47203] |
| Unit economics trend | CAC, AOV, CM %, lifetime orders by stage | CAC flat or falling, CM % rising | CAC rising with flat CM and low repeat (68 > 79 > 123 > 149) | stop scaling; fix supply chain, retention | [cd36c8b5eacc] |
| Post-marketing CM | CM - marketing each month | positive and above opex | negative | no opex cut can fix it; fix unit economics or wait for repeat base | [bf82ba8e8bc2] |
| Model integrity | rolled-up GP % vs unit-economics GP % per segment | equal | differ | find the formula error | [f1bd2de486c0] |
| Roll-up integrity | LTM operating profit in roll-up vs monthly tab | equal (T1: $508,419) | differ | fix sums | [def705c265c2] |
| Churn math | cancellations / prior-period base | stated with period | divided by current total or new signups | recalc | [e587bb652cdc] |
| Retention quality | cohort retention at the same age across cohorts | similar or improving | a cohort far lower (T12: Jan 74% vs Jul 91%) | ask what changed in acquisition | [540b5bdda637] |
| Revenue per survivor | NRR table | >= 100% | revenue per customer falling while headcount holds | check discounting, mix | [20b50a304d0f] |
| Payback | cohort cumulative GP vs N x CAC | short payback and a long profitable tail | barely pays back, no tail | rethink pricing, fundamentals | [9a3cda2fe90f] [d78b5a172074] |
| Segment LTV | LTV - CAC per segment | positive for each | one segment loses money (T9 transactional early) | correct that segment quickly | [e3d22c4449b1] |
| Cash vs profit | NI, FCF, cash balance side by side | FCF follows NI | NI positive and cash falling | walk inventory, capex, tax, debt lines | [7404abfd63fa] |
| Inventory cover | projected inventory by month | never negative | negative month = stockout | move or enlarge PO | [49138d1247d7] |
| Runway | cash balance by month | lowest point above zero with buffer | negative before next raise | raise earlier or larger, or finance inventory | [9d2823e98694] |
| LTV window | cumulative cohort revenue curve | plateau reached | using 60 to 90 days for a long-cycle product | extend window | [8fcbcb2cd9ba] |

## 6. Tools, settings and named features

- Microsoft Excel: freeze panes (View tab), F4 to toggle absolute references ($), Alt > H > B > O for a bottom border, Ctrl+Page Up to switch tabs, format painter, accounting format, ROUND for whole-number customers and orders. `[verify UI]` [7b2e56bcad5a] [90b11f77327e]
- Google Analytics cohort report, Google Ads, Facebook Ads Manager: to split new customers into paid and organic. `[verify UI]` [8cab64f326b9] [540b5bdda637]
- SQL by an analyst or data scientist, or plugins: to build cohort tables. [90b11f77327e]
- NetSuite, Google Workspace, AWS: named as typical technology opex. [111c8bab5864]
- Ordergroove: subscription and prepaid platform (presenter's employer and sponsor). Claims: customisable offers, increasing incentives, gift with purchase, benchmarks; clients named Dollar Shave Club, L'Oreal, La Colombe, PetSmart. `[web check: current features]`
- OpenStore: free Shopify store valuation (sponsor). `[web check]`
- Bainbridge: FP&A and cloud-connected financial model for Shopify brands (sponsor). `[web check]`
- Clearco (formerly Clearbanc): non-dilutive inventory and marketing financing, revenue-share repayment; Clear Angel program. Pipe: financing against recurring revenue for SaaS. `[web check: products, eligibility and fees today]` [a20812fa24c9]
- Amazon FBA and Amazon Ads (CPC). `[web check: current FBA and referral fees]` [ab551552b79e]
- Third-party scraped transaction site for Dollar Shave Club retention (not named). [1fafdae1c561]
- Downloadable Excel templates for each video (links not in the text).

## 7. Examples and case results

All are made-up or anonymised models unless stated. Treat as examples, never as promises.

**T1 coffee subscription (VC model).** $3M raised. Ad spend $5,000 in M1, ramp $7,500, $10,000, $15,000 from M7, then +7.5% a month from M13. Paid CAC $35 falling to $20 over year 1 as email list and organic grow. M1 new customers = 5,000 / 35 = 143. Churn 15% a month for all months. AOV $40. Refunds 5% and discounts 10% of new-order revenue (discounts only on first orders). COGS as % of revenue: product 35%, packaging 10%, fulfillment 8% falling to 5% with volume, customer service 7% falling to 4% by M12, merchant fees 3%. Salaries: marketing/sales $140,000, merchandising $80,000, product $125,000, technology $150,000, executive $175,000; benefits 25%. Start with 3 people (1 marketing, 1 IT, 1 exec); add tech in M3; one of each by M7; add marketing by M12; then +1 per role per year. Other marketing $7,500 a month; technology $5,000 a month for 12 months then $15,000; unknown bucket 10% of revenue. Result: gross margin 37%; M1 operating income -$64,000 (about -1,300% of revenue); first profit around M45; at M48 about $1.9M monthly revenue at a 12% profit margin. Burn $190,000 then $216,000 a month early; $250,000 left at end of year 2; cash negative early in year 3, so about 2 years of runway. Year 2: gross profit $1.4M vs opex $3.1M; year 3 loss $1.4M; year 4 profitable. [111c8bab5864] [def705c265c2] [da1cbdf76860]

**T2 KPI case (3 months).** Revenue +45% in July, +15% in August. Product cost 19%, 18%, 17.7% of revenue (he also says "about 73%" converts to product gross profit, which does not match). Fulfillment 30% rising to 32%. CM 43%, 41.5%, 42%. Marketing 29%, 39%, 31%. Post-marketing CM $42,000; $14,000 (3%); $56,000 (11%). Opex $20,000, $24,000, $23,000. Operating income 7.5%, -2.2%, 6.4%. Per order: AOV $232, product $62, fulfillment $71, CM $99; 3-month average AOV $238, product $64, fulfillment $74, CM about $100. SKU A (60% of sales): $230 revenue, $163 GP (71%), $92 CM (40%). SKU B (25%): $122, $104 (86%), $74 (61%). Blended CAC $74, $113, $100; overall $97 (marketing $91,000, $175,000, $162,000). Cohort: March 167 customers placed 238, 38, 22, 15, 11, 6 orders = 330 in 6 months = 1.98 orders each (1.67 over 5 months, 1.63 over 4). June: 1,123 new customers, 1,234 new orders, 122 returning orders from the diagonal. First order: CM $100 vs CAC $97 = 1.02, about $2 profit. Lifetime: revenue $238 x 1.98 = $469; LTV $197; LTV:CAC 2.02; about $99 profit per customer. His verdict: health "strong". (A card lists AOV as $138; that is a transcript slip; $238 is right.) [49110942deea] [2a88bf14790c] [6fe6a3b41072] [9e1b24779308] [a592b3f28c58] [b6fb728dba04]

**T3 Black Friday.** He says a brand he knew lost $500,000 on its last 50% off sitewide. Baseline: conversion 1.75%, CAC $75, AOV $135, $124 after refunds and returns; product $15 + duties, packaging, inbound freight = $21; fulfillment $12 ship and pack + $3 storage + $4 merchant fees = $19; CM $84; CM - CAC $9; 5,000 orders a month, about $600,000 revenue, about $50,000 CM after CAC (5,000 x $9 = $45,000 by the arithmetic). 50% off: CAC $33; buyers take 1 unit; order value $68, about 55% of normal net AOV with no refunds; product COGS still $21; CM $29; loss of about $4 per customer; volume 20,000 orders. BOGO: pays $135, no refunds; product COGS $42; CM $69; CM - CAC $36 (above the normal $9); at 20,000 orders about 2x the revenue of 50% off and "3/4 of a million dollars" (20,000 x $36 = $720,000). [5425adb4473f] [13df6c347b0e] [1a6c983c0c2f]

**T4 life-cycle benchmarks (optimal path).** Idea: CAC $65, AOV $165, CM 60% ($99), 3 lifetime orders, LTV $297, CM:CAC 1.5 ($34 after CAC), LTV:CAC "almost 5" (4.6). Launch: low CAC (friends, organic), AOV $89 (discounts), CM 39%, 1 lifetime order, CM:CAC about 1. Early (Facebook ads plus organic Instagram, 2,500 orders): CAC $68, AOV $134, CM 49%, 1.7 lifetime orders from the first 500 customers, LTV $112, CM:CAC about 1, LTV:CAC 1.6. Growth: CAC down a little, AOV $148, CM 51%, LTV $196, CM:CAC 1.4, LTV:CAC near 4. Late (250,000 orders): CAC $48 blended, AOV $162 (more products, bundles), CM 65% (larger runs, fixed supply chain), 3.1 lifetime orders, CM:CAC 2.1, LTV:CAC 6.7. [7eeee3aaceae]

**T4 sub-optimal path.** Same idea and launch. Early: CAC 68 rises to 79, AOV flat, CM lower (supply chain, distribution center in the wrong place, air freight), first 500 customers only 1.2 lifetime orders, LTV $66, CM:CAC and LTV:CAC below 1. After a $20M Series A/B: CAC $123, CM 48%, 1.5 orders, CM:CAC 0.58, LTV:CAC 0.87. Late: CAC $149 ("funding it with other people's money"), AOV $162, CM "86" (dollars per order, about 53%), 1.8 orders, CM:CAC 0.6, LTV:CAC 1.0. [cd36c8b5eacc]

**T4 GM vs CM.** Net revenue $175; product cost 27% = $47; ecom gross margin $128; CM $83, so fulfillment is $45 (a card says $40, which does not add up); CAC should be $83 or less. [ca717cbf0593]

**T5 FCF case.** Revenue about $415,000 a month with a sale spike; orders 3,000 to about 5,000; personnel $96,000 a month. Net income positive every month (for example $17,000, $77,000, $141,000) while FCF was about -$22,000 and -$94,000 in some months; only 2 of 6 profitable months had positive FCF. Inventory rose from $335,000 to $448,000 (+$113,000 cash out). Software platform spend $240,000 in 6 months ($100,000, $10,000, $50,000, $75,000, $5,000) vs $40,000 depreciation on the P&L. Tax paid in lumps of about $80,000 and $100,000 a quarter. Line of credit paid down about $25,000 a month. One month: net income $77,000, FCF -$95,000 (inventory buy plus engineers). Another: net income $140,000 (a card writes "$140"), FCF $272,000 (sell-through, little dev spend, no tax payment). Net cash flow slightly below FCF because of leverage. [7404abfd63fa] [2ff9cc0805c2] [8187da83315e]

**T6 prepaid (Ordergroove).** AOV $80; product $19; fulfillment $15; GP $46 (58%). 3-order prepaid at 25% off: $60 collected, GP $26. 6-order prepaid at 30% off: $56, GP $22 (39%). Cohort of 1,000 over 12 months: one-time 1.2 orders; 3-order prepaid 5.6; 6-order prepaid about 9. LTV: $54 (1.2 x $46), $146 (5.6 x $26, +169%, +$92), $198 (9 x $22, about 4x, +$144). Mix 85% one-time, 10% 3-order, 5% 6-order: weighted LTV $54 to $71 (+30%). Claim in the title: prepaid can lift LTV "100% or more". [d8e1973bffac]

**T7 CM case (2020).** Gross revenue $176,291; units 1,236 and 2,136; gross revenue per unit $142 and $136; net AOV $134. COGS 29% and 27% of net revenue ($39 and $35); gross margin 70 to 75%. Merchant fees $3.65 and $3.79 per order; total fulfillment $31 and $35 per order. CM $64 and $60 per order (total $79,000 and $128,000), a little under 50%. Marketing 31 to 36% of revenue, $42 and $48 per order. Post-marketing CM $22 and $12 per order ($27,000 in the first month). CM:CAC about 1.5 on the first order. Opex about $10,000 and $13,000 (1 to 2 people, software, consultants) = $8 and $6 per order. Operating income about 11% and 5% = $15 and $6 per unit. [957cabf05b5f] [2978d63684ea]

**T8 discount vs CAC.** $100,000 ad spend; $1.50 blended CPC; 66,667 sessions; list price $200; COGS $75 ($50 product, $25 fulfillment). A: no discount, 1.5% conversion, 1,000 buyers, CAC $100, per-customer $200 - $75 - $100 = $25. B: $30 off, 2.2%, 1,433 buyers, CAC $70, $170 - $75 - $70 = $25. C: $60 off (never offered before), 3.8%, 2,500 buyers, CAC $40, $140 - $75 - $40 = $25. Discount + CAC = $100 in all 3. Totals: A $200,000 sales, $75,000 COGS, $125,000 CM, $25,000 post-marketing; B $243,000, $107,000, $136,000, $36,000; C $350,000, $187,000, $162,000, $63,000 (the header calls it "from $25,000 to $63,000 on the same $100,000"). Arithmetic note: 66,667 x 2.2% = 1,467 and x 3.8% = 2,533, so the buyer counts are rounded assumptions. [8723bc22dfe2] [993ecc7a19f0] [1247e2cd031e]

**T9 supplements subscription model (36 months).** Transactional: AOV $90, refunds 4%, discounts 5% (email 5% off first order), net AOV about $81.90; product $7.70; fulfillment $16.20; card fees 2.75%; COGS about $26.20; CM about $55.70 (68%). Subscription: AOV $75, refunds 4%, 20% subscribe and save, collected about $57; product $6.50; fulfillment spoken as "$5.50", but the stated CM of $33.40 (59%) only works with about $15.50; card fees 2.75%. Ad spend $5,000, $10,000, then +$5,000 a month to M6, +$10,000 a month to M12, +$15,000 a month to M24, +$25,000 a month after; about $570,000 a month at M36. CAC $100 for the first months, $75 to M12, $60 after. M1 new customers 5,000 / 100 = 50. Split: 60/40 transactional/subscription in M1 to M3, 50/50 in M4 to M6, better subscription deal from M7, default cart to subscription from M10, 30/70 steady state. Transactional return rate 3.3% of trailing-6-month customers: M1 30 customers gives 1 return; M2 (30 + 61) x 3.3% = 3; M6 17; M36 576 returning vs 2,850 new = 3,426 transactions. Annual retention 3.3% x 12 = about 40%; lifetime orders 1 / (1 - 0.40) = 1.7. Subscription churn 25%; lifetime 4 orders. M2 subscriptions 20 + 40 - 5 = 55; M36 about 23,000 subscriptions. At M36: 27,000 orders a month, net revenue $1.6M a month, repeat subscription revenue $940,000 a month, CM $964,000 a month, run rate $19M vs trailing 12 months $14M. LTV transactional 1.7 x $55.70 = about $93; subscription 4 x $33.40 = about $134; weighted 0.6 x 93 + 0.4 x 134 = $109; LTV:CAC 1.09 at start, 2 at M36; LTV - CAC $9 to $62 (6x). Transactional customers lose money early. [17cd13e806d9] [563870c81120] [1903080a3a75] [c1e5e9113ebe] [e3d22c4449b1]

**T10 same model, P&L and cash.** Subscription share of revenue from 32% to over 80%. Post-advertising CM cannot cover anything until M11; covers payroll from about M14 to M15. Payroll: 1 marketing and 1 exec in M1, operations from M4, in-house creative in M13 (4 people); 25% benefits (example salary $90,000 becomes $112,500; the transcript garbles the salary). Operating income M1: CM $2,300 - opex $38,000 = about -$36,000; positive from M17 ($8,500, 2% margin); 19% EBIT margin at M36. No tax for about 11 months after turning profitable because of accumulated losses. Inventory: 5,000 starting units, 3-month lead time, 4-month cycle, POs every 4 months (for example 2,300, then 6,800, then 15,000, later 100,000+ units); weighted product cost 60% x $7.70 + 40% x $6.50 = $7.20; first PO about 2,400 x $7.20 = about $17,000; M5 PO about $47,000. Cash: $500,000 raised; M1 net income -$36,000 and cash out about $53,000; M2 cash out $37,600; M8 -$54,000; M9 -$154,000 (about $100,000 inventory); cash runs out by M8; the business consumes about $690,000 in year 1; a $500,000 raise at M6 is not enough; about $1.5M total needed to reach profitability. End of year 3: net income $230,000 a month on $1.6M net revenue a month. [f39ad32b21d7] [b8599dca5b33] [308a0d76128c] [9d2823e98694]

**T11 churn.** Monthly: 100 prior + 50 new - 9 cancelled = 141; churn 9 / 100 = 9% (not 9 / 141 = 6%); later months 13%, 17%, 11%, 16%. Annual: 53 prior + 31 new - 18 cancelled = 66; churn 18 / 53 = 34%; range 20 to 40%. [e587bb652cdc]

**T12 SaaS cohort ($50 a month).** January cohort 35 customers: retention 100%, then 86%, down to 26% at 12 months. July cohort 91% vs January 74% at the same age. April calendar total 85 purchasers across 4 cohorts. January revenue $1,750 in month 0, $14,000 cumulative by month 11, $406 per customer. GM 65%: $33 on the first $50; cumulative GP per customer $33, $65, $95, $123 (passes the $115 CAC at purchase 4), $264 by month 12 (more than 2x CAC). [540b5bdda637] [20b50a304d0f] [e564ae6200ef]

**T13 CAC payback.** Unit: $50 revenue, $22 COGS, $28 GP a month. Physical subscription, CAC $90: naive 90 / 28 = 3.2 months. Cohort 3,500 customers; CAC outlay $315,000; retention 100%, 75%, 50% (1,750) by order 3, most gone by order 18; GP $98,000 in month 1, $73,500 in month 2; cumulative -$217,000 after month 1; break even in month 8 (error about 150%, "almost 3x"); barely any profit after. SaaS, CAC $199: naive 7.1 months; outlay about $696,000; retention 45% at 12 months, 15% at 24, mostly gone by 36; GP $98,000, $93,000, $88,000...; break even month 9 (error about 27%); then LTV:CAC about 2 and rising. CAC sensitivity: $125 breaks even in month 5; $225 in month 11. [9a3cda2fe90f] [d78b5a172074]

**T14 international ingredients box (live stream).** $39 a month, free shipping built into the price. Product $8.64, fulfillment $4.50, shipping spoken as "30" (the $20.39 total and later renegotiation to $6.50 imply $7.25; a card lists $0.30, which is wrong); COGS $20.39; GP $18.61; margin 48%. Founder-guessed churn 27%; lifetime 3.7 months; LTV $69. Cohort: January 100 customers; 81, 75, 45 in months 1 to 3 (month-to-month churn 19% then 40%); revenue $3,750 then $3,000; cumulative almost $12,000; $38 revenue per customer in month 0 rising to $116; LTV $18, $33, $47, $55. May: spend $6,500; 134 new customers (101 paid, 33 organic); blended CAC $48.51; paid CAC $64; LTV:CAC 1.4 on blended ("not great"). Churn 27% to 20% lifts LTV $69 to $93 (+35%). Tiers $39 and $49. COGS renegotiated to product $7, fulfillment $4, shipping $6.50 lifts LTV to about $80. Gifting brand example: $20 first order, $200 over 3 years. [31dce846c93c] [136827bb25c7] [f272a137245d] [8cab64f326b9] [79a98ff8e618] [86fcb4012931] [ed010f896be7] [482dba787e59] [8fcbcb2cd9ba]

**T14 Dollar Shave Club.** $1 blades + $3.99 shipping, about $5 a month; grew by guerrilla/organic YouTube because about $50 paid conversions were unaffordable; bought by Unilever in 2016 for $1B. Scraped estimate, May 2014 cohort of 3,096 signups (also spoken as 396): 76% at month 1, 82% at month 2 (maybe pause and reactivate), 51% at month 10, 41% at month 20, 37% at month 24; $5 x 24 = $120. "Very few" subscription boxes see this. [1fafdae1c561] [c55db537e5fa]

**T15 Amazon FBA vegan protein powder.** Price $89; FBA fee $20.56; landed product $25.30; GP $43.14. CPC $3.10; conversion 7.5%; CAC 3.10 / 0.075 = $41; first-order profit $1.81. Lifetime orders 2.2; lifetime GP about $95; LTV/CAC 2.3. Budget $1,000, $1,500, then +$1,000 a month to M16; M2 paid orders 1,500 / 41 = 36; organic 10% of paid at start (24 paid gives 2 organic); after 4 to 5 months and about 300 orders, reviews start to lift ranking. Starting inventory 250 units x $25 = about $6,300 plus $1,000 cash. Lead time 4 months (a M2 order arrives in M5). POs 500, 500, 1,500, 4,000 units; 500 units cost about $12,000 to $13,000; 4,000 units about $100,000. One month's post-marketing profit $799. Cash goes negative before M2. With Clearco-style financing: $164,000 financed, $160,000 repaid M5 to M16 at 30% of revenue; profit positive every month. [e9dcc756a117] [ab551552b79e] [49138d1247d7] [a20812fa24c9]

**T16 coffee LTV.** 730 clients; 1.35 orders per client; 986 transactions; AOV $25; GM 60%; churn 22%; lifetime 4.5 months. LTV = 986 x $25 x 60% x 4.5 / 730 = $92 (same as $25 x 60% x 1.35 / 0.22). Cohort check: 986, 769 in month 2..., gone by about 3 years; total GP about $67,000 / 730 = $92. CAC example: $1,000 / 120 new customers = $8.33. $50 CAC works because the 4.5-month life repays it. [0b060b80b16f] [8b747d69f620]

## 8. Mistakes the source warns about

- Dividing marketing by all orders instead of new customer orders. [6fe6a3b41072] [8cab64f326b9]
- Lumping product and fulfillment into one COGS line, so you cannot see which cost moved. [4e8e7fd6e6e4] [2978d63684ea]
- Calling gross margin contribution margin (or the reverse) without defining it. [68431c491a0c]
- Judging a customer on the first order only when cohorts show repeat orders; or the reverse, running CM:CAC below 1 in a buy-once category. [a004a45541ef] [613635831aff]
- Scaling ad spend (often with VC money) while CAC rises and CM and repeat stay flat. [cd36c8b5eacc]
- Running 50% off sitewide: volume and revenue soar while CM after CAC goes negative because product and fulfillment cost do not fall. [5425adb4473f]
- Losing money on Black Friday customers and hoping to earn it back later. [5425adb4473f]
- Treating discounts and marketing as separate budgets. [1247e2cd031e]
- Putting deep discounts on flash sales instead of loyalty or subscription on-ramps. [8acd81a0345e]
- Assuming the biggest discount always wins. [993ecc7a19f0]
- Using flat subscribe-and-save that attracts subscribe-then-cancel buyers. [17cd13e806d9]
- Rejecting prepaid offers on per-order margin alone, ignoring retention. [d8e1973bffac]
- Quoting churn without a time period; comparing monthly and annual churn directly. [d4b9ff187dc2]
- Calculating churn as cancellations / current-month total, or applying churn to this month's new signups. [e587bb652cdc] [1903080a3a75]
- Asking for a churn rate in a non-subscription store. [d4b9ff187dc2]
- Reading retention from aggregate totals instead of cohorts; reading a calendar month across a row instead of diagonally. [540b5bdda637] [b6fb728dba04]
- Treating NRR above 100% as a data error. [20b50a304d0f]
- Computing CAC payback as CAC / monthly GP, which assumes 0% churn. [9a3cda2fe90f]
- Measuring payback in months when customers skip or order every 2 to 3 months. [9a3cda2fe90f]
- Using a 60 to 90 day LTV window for products bought again months later. [8fcbcb2cd9ba]
- Trusting net income as a sign of cash health; ignoring inventory buys, capitalised software, quarterly tax and loan principal. [7404abfd63fa] [2ff9cc0805c2]
- Expensing inventory per unit sold in a cash plan instead of showing lumpy purchase outflows. [49138d1247d7]
- Letting projected inventory go negative (stockouts). [49138d1247d7]
- Selling permanent equity to fund short-term inventory. [a20812fa24c9]
- Over-formatting models; building huge payroll models. [7b2e56bcad5a] [f39ad32b21d7]
- Competing on price and attracting price-only buyers. [ed010f896be7]
- Planning tax payments without counting accumulated losses. [b8599dca5b33]
- Using blended CAC alone when organic buyers are friends and family and cannot scale. [8cab64f326b9]

## 9. Caveats, conflicts and what is missing

**Conflicts inside the source.**
- Margin names. T7 insists gross margin (product only) and CM (product + fulfillment) are distinct. T8, T9 and T10 say gross profit and CM "all mean the same thing" in ecommerce, and T12 and T13 use "gross margin" or "gross profit" for revenue minus all delivery costs. When an agent reads any number from this source, check which costs it subtracts. [68431c491a0c] [17cd13e806d9]
- LTV base. T2, T4, T9 use lifetime CM. T6, T12, T13, T14, T16 use lifetime gross profit (which in T13 and T14 includes fulfillment and shipping, and in T12 is an assumed 65%). The source never nets out repeat-order marketing except by assumption.
- First-order rule. T3 and T4 say make money on the first order (especially Black Friday); T12, T14 and T16 happily accept a CAC well above first-order profit (T12: $115 CAC vs $33 first GP; T16: $50 vs $15) because of lifetime value. The condition decides it: repeat rate and cohort proof.
- LTV:CAC targets differ by segment: > 1 on first order and 5+ late stage (T4), 2 to 3 (T14), 1.09 accepted as a starting point with a path to 2 (T9).
- T1 uses the same discount and refund logic as T9 but treats refunds as first-order only; T9 applies refunds to all orders.

**Transcript errors found by arithmetic (use the corrected values).**
- T2 first-order AOV "138" is $238. Card [a592b3f28c58] repeats 138.
- T4 fulfillment in the $175 example is $45, not $40 as card [ca717cbf0593] says.
- T9 subscription fulfillment "$5.50" should be about $15.50 to give the stated 59% and $33.40. Card [17cd13e806d9] repeats $5.50.
- T14 shipping "30" is $7.25 (8.64 + 4.50 + 7.25 = 20.39). Cards [31dce846c93c] and [482dba787e59] say $0.30.
- T10 first inventory purchase "$177,000" is about $17,700 (2,400 x $7.20).
- T5 "net income only 140" is $140,000; card [8c56490f81a2] writes $140.
- T3 "$50,000" CM after CAC is $45,000 by 5,000 x $9.
- T2 product cost 17.7 to 19% of revenue does not fit "73% to product gross profit".
- Card [79a98ff8e618] garbles the paid-CAC ratio; paid LTV:CAC is $69 / $64 = 1.08, far thinner than the blended 1.4.

**Card-writer additions not in the source (do not cite as the presenter's view).**
- [b8599dca5b33] adds accountant checks on carryforwards and deferred tax assets; the source only says losses offset future profits before tax is paid.
- [14761dd09c81] adds "do not buy or incentivise reviews" and a no-organic downside case; the source only says accumulate reviews through paid sales.
- [a20812fa24c9] and [59714f58fac1] tell you to keep inventory payments in the cash schedule and not treat financing as revenue; the source's own model deletes the inventory row and replaces it with a revenue-share repayment. The card's version is the more correct accounting.
- [602ada5d7d4a] converts annual churn to monthly with 1 - (1 - a)^(1/12) (40% annual = 4.17% monthly, about 24 months). The source instead says 40% annual = 2.5 years = 30 months. The two give different lifetimes.
- [fe4a0757982c], [69e7ae8e0048] and [0b060b80b16f] rewrite the source's formulas more carefully (orders per active period, payback constraint).
- [d78b5a172074] contains a bullet about low-churn users who "forget to cancel"; that idea is not in the source.

**Where the source is thin or hedges.**
- No real benchmarks. Every number is a model input, a vendor claim or one anecdote.
- Channel CAC: says to map the funnel, gives no method. [6fe6a3b41072]
- Discount conversion lift: assumed, never measured; the "split test" is named but not designed. [1247e2cd031e]
- Promo returns: "best practice during any promo, don't offer refunds or returns" ignores consumer law. `[web check: statutory return and refund rights for online orders in the brand's country]`
- Black Friday: no guidance on cannibalisation of full-price buyers (a card adds it). [5425adb4473f]
- Amazon unit economics omit the Amazon referral fee and storage fees; only an FBA fee of 20 to 25% is used. `[web check: current Amazon referral and FBA fee schedule for the category]`
- Merchant fee rates, the 25% benefits load, 25% tax rate, quarterly estimated taxes and 401k are US-specific. `[needs brand data: payment gateway fee rate, payroll on-costs, tax rate and payment calendar for the brand's country]`
- Tax loss carryforward is described simply; rules vary by country. `[web check: loss carryforward rules]`
- Clearco and Pipe terms are historical and came with an affiliate link. `[web check: current offers]`
- Industry churn benchmarks: in the live stream he says he does not know a good published source. `[web check: category churn benchmarks]`
- Ordergroove claims (2.5x prepaid lifetime spend, 60 to 70% default-cart lift, prepaid roll-off curves, "100% or more" LTV lift) are vendor data with no sample. Treat as hypotheses to test.
- Default-to-subscription carts can create customer complaints or regulatory risk for negative-option billing; the source gives no downside. `[web check: auto-renewal and subscription consent rules in the brand's market]`
- Dollar Shave Club retention came from scraped third-party estimates.

**Conflicts with common ecommerce advice.**
- Common advice quotes LTV:CAC of 3:1 as healthy. This source sets a first-order CM:CAC test as the main gate and treats 2 to 3 (T14) or 5+ late stage (T4) as targets, and uses lifetime CM or GP, not revenue, for LTV.
- Common advice says discounts erode margin and brand. The source says a discount is mathematically the same as CAC and can be the cheaper way to buy customers, with the brand caveat.
- The "no returns during promo" line conflicts with standard consumer protection practice.

**Needs brand data before use.** `[needs brand data: net AOV, product COGS per unit, fulfillment and shipping per order, payment fees, returns rate, marketing spend, new vs returning orders, cohort orders and revenue by first-purchase month, subscription churn if any, inventory lead time and PO terms, opening cash, opex and payroll]`

**Overlap.** T5 is the same free cash flow case as mini playbook 05 in this folder (05-understanding-free-cash-flow-for-ecommerce.md); the Pass 2 merge should count it once.

## 10. Card index

- [111c8bab5864] Build a 48-month subscription financial model from ad spend down
- [aa80d087ca61] Discounts vs CAC: when a discount is mathematically neutral
- [4e8e7fd6e6e4] Split COGS into product and fulfillment to read ecommerce margins
- [c160135c9bd3] Read a monthly P&L as percent of revenue to spot trajectory and margin drift
- [49110942deea] Compute per-order unit economics: AOV, product cost, fulfillment, contribution
- [2a88bf14790c] Add per-unit product economics to find your most profitable SKU
- [6fe6a3b41072] Calculate blended CAC from total marketing and new customer orders
- [9e1b24779308] Build customer retention cohorts to measure true repeat purchase behaviour
- [613635831aff] Define LTV as lifetime contribution margin and test it against CAC
- [66d5d76e9b71] Simplify a startup payroll model with salary x headcount ÷ 12
- [50708132adc1] Include an unallocated 'unknown' opex bucket
- [def705c265c2] Set up a quarterly roll-up with starting cash to calculate runway
- [7b2e56bcad5a] Format a financial model for fast reading: colours, brackets, freeze panes
- [da1cbdf76860] Build a standard VC-style 4-year model: and know its limits
- [b6fb728dba04] Cohort Table Mechanics: Reading Repeat Orders Diagonally
- [a592b3f28c58] From First-Order Economics to Lifetime Value
- [5425adb4473f] Why 50% Off Sitewide Destroys Black Friday Unit Economics
- [13df6c347b0e] BOGO / Two-for-One as a Black Friday Cash Machine
- [e2eaed277a0d] The Core Unit Economics Stack: CAC, AOV, CM, LTV and Their Ratios
- [a004a45541ef] Two Valid Models: Break Even on Order One, or Lose Early and Earn Later
- [ca717cbf0593] Ecom Gross Margin vs Contribution Margin: Two Different Buckets
- [7eeee3aaceae] Healthy Unit Economics Benchmarks Across the Business Lifecycle
- [cd36c8b5eacc] Sub-Optimal Pattern: Rising CAC With Flat Contribution Margin
- [1a6c983c0c2f] Splitting COGS Into Product and Fulfillment Buckets for Promo Modeling
- [7404abfd63fa] Three-Statement Model as the Diagnostic for a Profitable-but-Cash-Poor Store
- [2ff9cc0805c2] Balance Sheet Cash Traps: Inventory, Capitalized Software, Quarterly Taxes
- [8c56490f81a2] Reading the Cash Flow Statement: Operating, Investing, Financing
- [183999c47203] Diagnosing Gross Margin Drops During Promo Months
- [8187da83315e] Free cash flow vs net income: inventory and tax timing as cash drivers
- [957cabf05b5f] Calculate contribution margin per order and post-marketing contribution
- [1247e2cd031e] Treat discount and CAC as one acquisition cost pool
- [d8e1973bffac] Price prepaid bundles by comparing margin loss against retention gain
- [17cd13e806d9] Build separate unit economics for transactional vs subscription customers
- [563870c81120] Forecast ad spend divided by CAC to drive new customer counts
- [2978d63684ea] Turn a contribution-margin model into a pricing and negotiation checklist
- [68431c491a0c] Define gross margin, contribution margin and post-marketing contribution consistently
- [1903080a3a75] Build a Linked Acquisition-to-Retention Model for Transactional + Subscription Mix
- [1b23d41ee499] Forecast Marketing Spend into New Customers via CAC Assumptions
- [013b592e17af] Use Trigger Events to Shift New Customers from One-Time to Subscription
- [c1e5e9113ebe] Forecast Transactional Repeat Customers with a 6-Month Rolling Return Rate
- [69e7ae8e0048] Compute Subscription Lifetime Orders from Monthly Churn
- [bf82ba8e8bc2] Report Post-Marketing Contribution Margin as the Core Profitability Gauge
- [f39ad32b21d7] Build a Simple Bucketed Payroll and Opex Forecast
- [b8599dca5b33] Model tax losses separately from book losses and cash tax payments
- [308a0d76128c] Forecast Inventory with Lead Time and Cycle Time Before You Model Cash
- [9d2823e98694] Build a Mini Cash Flow Statement to Find Working Capital Needs and Runway
- [895584eaf5b7] Gross Revenue to Net Revenue Bridge: Report Refunds and Discounts Separately
- [f1bd2de486c0] Reconcile Your Model: Gross Profit Percentage Must Match Unit Economics
- [e3d22c4449b1] Consolidate Segments and Report the Ecommerce KPI Set
- [d4b9ff187dc2] Churn rate only applies to subscriptions: use retention for one-off stores
- [e587bb652cdc] Calculate churn against the prior period's base, not the current month
- [fe4a0757982c] Convert churn into average customer lifetime with 1/churn
- [540b5bdda637] Build a cohort retention table as the only valid retention view
- [20b50a304d0f] Track net revenue retention separately from customer retention
- [e564ae6200ef] Derive customer lifetime value per cohort in three columns
- [9a3cda2fe90f] Calculate CAC payback from cohorts, not from flat monthly gross profit
- [d78b5a172074] Inspect what survives after payback, not just whether you break even
- [5a5c62ca14b3] Choose subscription-compatible products and structure the offer
- [c55db537e5fa] Recognize the churn-driven hurdles subscription boxes face with investors
- [602ada5d7d4a] Convert monthly and annual churn on a consistent survival basis
- [2650453af6e8] Read one calendar month diagonally across the cohort table
- [90b11f77327e] Build the cohort model in a spreadsheet with locked denominators
- [31dce846c93c] Unit economics first: profit per order before anything else
- [136827bb25c7] Use churn-rate lifetime as a fast fallback, not the real answer
- [f272a137245d] Read a retention cohort table to calculate lifetime revenue
- [8cab64f326b9] Blended vs paid CAC: calculate both and know why
- [79a98ff8e618] Interpret the LTV:CAC ratio with the source's heuristics
- [86fcb4012931] Lever 1: Raise LTV by cutting churn and adding pause options
- [ed010f896be7] Lever 2: Raise AOV without competing on price
- [482dba787e59] Lever 3: Renegotiate COGS as volume grows
- [8fcbcb2cd9ba] Decide how long a window to use for LTV
- [14761dd09c81] Model paid Amazon launch orders and uncertain organic follow-on sales
- [ab551552b79e] Model lifetime orders per customer before committing ad budget
- [939b20dbac4b] Sequence the forecast from marketing spend forward
- [1fafdae1c561] Subscription retention benchmarking lesson from Dollar Shave Club
- [e9dcc756a117] Build an Amazon FBA order forecast from marketing spend
- [49138d1247d7] Model inventory timing with a lead-time lag row
- [59714f58fac1] Forecast inventory funding gaps with a monthly cash bridge
- [a20812fa24c9] Evaluate non-dilutive inventory and marketing financing
- [0b060b80b16f] Calculate customer lifetime value from churn and gross margin
- [8b747d69f620] Spend above first-order profit when LTV justifies it
- [8723bc22dfe2] Model discounts and CAC as one combined acquisition cost
- [993ecc7a19f0] Choose the discount/CAC mix that maximises total contribution margin
- [8acd81a0345e] Attach your best discounts to a loyalty or subscription on-ramp
