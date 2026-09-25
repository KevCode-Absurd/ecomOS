# What Metrics Matter In The Shopify Analytics Dashboard

source_id: 15nouc2hC_RGWuQdPq-kh4SyUxr6p5BdF  |  folder: /06-MEA-measurement  |  cards: 12  |  words: 3,429  |  type: transcript (single YouTube walkthrough video)

credibility: The presenter is not named. He speaks for an ecommerce agency or "e-commerce partner" with clients ("for some clients we", "we have seen really good success with a lot of clients"). He says his team has its own custom cohort models and the number 1 ranked video on YouTube and Google for Shopify cohort analysis "at least in Australia", so the team is likely Australian. He plugs 3 of his own videos (returning customer rate, AOV, cohort analysis) and 1 upcoming video (net profit margin limits growth rate). Evidence: one client dashboard shown with figures blurred, his own client experience, and opinion. No studies, no sample sizes. The Shopify metric definitions he gives are his reading of the UI and should be checked.
date signals: No year stated. He walks the default Analytics dashboard layout with a "Customize" button top right, a cohort analysis card he calls "one of the most useful reports that Shopify has ever rolled out", and a "Shipping charges" metric he says "used to be called shipping collected". One chart shows a dip on "January 26th". The document was filed on 19 Sep 2026. Shopify renames metrics and moves dashboard cards often, so every name and path here is stale-risk. [web check: current Shopify Analytics dashboard cards and metric names]

scope note: The folder header says the core is profit and contribution formulas and return rate, all baseline. It says to skip the video plugs and the sell-through and cash conversion cycle aside, which belongs in 20-FIN. The sell-through point is kept short in this file only because a card covers it. Paid social account structure goes to 11-ADC; Shopify store setup goes to 05-SET.

## 1. What this source is for

It helps an operator read the default Shopify Analytics dashboard: which cards to trust, which to ignore, and which need a click-through before they mean anything. Its main tool is a 3-lever check for any revenue change: sales = sessions x conversion rate x AOV. It also gives a funnel benchmark (4:2:1 from add to cart to purchase), a revenue definition (net sales + shipping charges), and a warning that returns booked on the refund date create false revenue dips.

## 2. Principles

1. **Use net sales + shipping charges as the top-line revenue number.** Source says this is "the most accurate way to understand cash collected" and "the best measure". Reasons given: total sales includes tax, which is a flow-through cost you do not want in profitability maths; gross sales is before discounts and returns, and discounts are not cash collected. Condition: see principle 2 for returns. Card [a3ae4e9e2a00] corrects the label: net sales + shipping is a sales-based figure, not cash collected and not profit. Sales reports can include unpaid orders; payments and refund transactions sit in payments or finance reports. [needs brand data: net sales, shipping charges, taxes and refunds for the period] [a3ae4e9e2a00] [9e9d4013f967]

2. **Returns land on the refund date, not the purchase date, so they can fake a revenue dip.** Source example: a fashion brand ramps ad spend, has a strong month, then 20% of those orders come back next month (wrong size, not as expected). The next month shows a big revenue dip. It looks like ads fell off, Meta got worse and blended CAC rose, when it is only the delay in processed returns. Condition: matters most when return rates are high (source names fashion). What the source does: "for some clients we even add returns back into our reporting", that is, they report sales without deducting returns so marketing decisions are not skewed. Card [a3ae4e9e2a00] prefers showing refund timing separately (for example by cohort) rather than adding refunds back and calling it cash. Both views are kept; see section 9. [needs brand data: return rate by month and by order month] [a3ae4e9e2a00] [9e9d4013f967]

3. **Every revenue change is sessions, conversion rate or AOV.** Total sales (source: "or at least let's call it net sales plus shipping charges") = total sessions x conversion rate x AOV. If sales drop, 1 or more of the 3 dropped. Source says it is "physically impossible" for sales to fall while all 3 are flat or up, with returns as "probably the only exception". Use the same check when sales rise. [9e9d4013f967]

4. **Small moves compound; do not chase single-digit dips.** Source example: a 5% AOV dip and a 4% conversion rate dip "magnified into a 10% dip in top line" is "probably just natural fluctuation". Do not stress over single-digit percent moves across a few core metrics. Condition: all 3 levers otherwise stable. Arithmetic note (computed, not from source): 0.95 x 0.96 = 0.912, an 8.8% drop; a 10% drop also needs about a 1.3% drop in sessions. [9e9d4013f967]

5. **Returning customer rate misleads on loyalty; use cohort analysis.** Source calls it "by far the most misleading metric" in Shopify and "the worst possible metric" on the dashboard. His reading: it is the share of orders in the selected period that came from returning customers, so it measures repeat buyers in proportion to new customers in that window, not how many people come back. It skews up when acquisition is low and down when you scale acquisition fast. It does not predict profit or revenue over a customer's lifetime. Cohort analysis does. Condition: applies to any period with changing new-customer volume. [web check: Shopify's current definition of returning customer rate, orders-based or customers-based] [8f85f33352f5]

6. **Shopify AOV excludes shipping and is a mean; do not act on it alone.** Source says Shopify AOV = (gross sales - discounts) / orders, with no shipping charges. He calls that "a little bit silly" because shipping is cash collected at checkout. Adding free shipping or changing shipping fees will not show in Shopify AOV. It is a mean, not a median. Alone it "tells you almost nothing": look at the distribution, new vs returning customer AOV, and the product pathways that lead to each AOV band before acting. [web check: Shopify's current AOV formula] [needs brand data: shipping charges as a share of revenue; AOV distribution; new vs returning AOV] [9b3f534de0a2]

7. **Shopify sessions include bot traffic; check against GA4.** Source says GA4 does "a much better job" of not counting bots, so GA4 sessions are generally lower than Shopify's. Shopify's conversion rate is then "kind of incorrect" because bots sit in its denominator. A sudden conversion rate dip (his example: 26 January on a client chart) may be a bot spike you cannot see in Shopify. Use both Shopify and GA4 (or another platform that counts sessions) for all conversion rate and session analysis. [needs brand data: Shopify vs GA4 sessions for the same dates] [084db9abd48b] [57a97c0614d6]

8. **Ignore every Shopify attribution card.** Source names: total sales by social referral, sessions by social referral, top referrals by session, sales attributed to marketing, sessions by referrer and total sales by referrer. His words: "not accurate", "not helpful", "does not drive decision making", "attribution is a futile effort", especially with Shopify's own tracking; using them makes you "go around in circles". Card [561513b3e85e] softens this: treat it as a practitioner opinion and triangulate (attribution windows, channel definitions, consent coverage, GA4, UTMs, incrementality tests) rather than trusting any single view. [561513b3e85e]

9. **Hold an ecommerce partner to online store revenue.** If paid ads mainly drive the online store, filter every report to the Online Store sales channel. Other channels (POS, Shop app, draft orders) otherwise mix in. Condition: store sells on more than 1 channel. [needs brand data: sales by channel] [6ca5944157b0]

10. **The funnel card is one of the best snapshots for checkout troubleshooting.** Source says quick wins are "so common": a big drop after add to cart or after reach checkout often traces to something below the fold or out of place. Benchmarks in section 4. [c8e57ed1cd0a]

11. **Cohort analysis is useless as a dashboard card but one of Shopify's most useful reports once opened.** Source says it is "relatively rudimentary" compared with his team's custom models, but "an incredible resource". He says you likely cannot read it without a tutorial. [8f85f33352f5]

12. **Sell-through rate by product is "incredibly helpful" for inventory and cash planning.** Source ties it to growth limits: net profit margin funds future inventory in the cash conversion cycle, so margin caps the maximum growth rate, and sell-through is an input. Track it at product and category level. Scope: finance detail belongs in 20-FIN. [37f16297a48e]

## 3. Procedures

### 3.1 Revenue-change triage (source's core framework)

1. Set the period of the change and a comparison period. [needs brand data: sales, sessions, conversion rate, AOV for both periods]
2. Pull net sales + shipping charges, sessions, conversion rate and AOV. Filter to the Online Store channel if paid media is the driver (principle 9). [verify UI]
3. Check returns first. If a large batch of refunds landed in the period, the dip may be return timing, not demand (principle 2). [needs brand data: refunds by processing date and by original order date]
4. Find which lever moved:
   - **AOV fell:** ask why. Source example: did we start pushing lower-AOV products?
   - **Conversion rate fell:** ask whether it is natural variance or a special cause. Check Shopify vs GA4 sessions for a bot spike before blaming the site (principle 7).
   - **Sessions fell:** look at paid media first. Source examples: a Shopping campaign spent less (Shopping is "a great driver of high converting traffic"), CPMs or CPCs rose, or spend went down.
5. If all 3 are stable and the moves are single-digit percent, treat it as natural fluctuation (principle 4).
6. When sales rise, run the same steps to name the lever that drove it.
Source is thin on how to separate "natural variance" from a special cause; it gives no statistical test or range. [9e9d4013f967]

### 3.2 Funnel check

1. Open the funnel card (source: sessions to add to cart to reach checkout to purchase). [verify UI]
2. Compare add to cart : reach checkout : purchase against 4:2:1, then against the 2:1:1 target (section 4).
3. Find the step with the biggest drop. Source's diagnosis: something below the fold or placed so the next step is not intuitive.
4. Fix that step. Source claims fixes "immediately increased conversion rates by 40 to 50% overnight" for clients (example, not a promise). [needs brand data: funnel counts by step]
Card [c8e57ed1cd0a] adds causes to check (product page clarity, cart visibility, unexpected costs after add to cart; checkout friction, payment options, shipping fees after reach checkout). These are the card's, not the source's. [c8e57ed1cd0a]

### 3.3 Bot traffic check

1. Compare Shopify "Sessions over time" with GA4 sessions for the same dates. [verify UI]
2. If Shopify shows a spike or dip GA4 does not, suspect bots.
3. Open "Sessions by location", click into the full report, sort by city. [verify UI]
4. A spike from 1 city "often means" a server hitting the site. Source says it is traffic "you might want to exclude"; he does not say how. [57a97c0614d6] [084db9abd48b]
Card [084db9abd48b] adds: use GA4 sessions as the conversion rate denominator, or at least validate Shopify's rate against GA4. Card [57a97c0614d6] notes filtering bots inside Shopify is not simple and may need third-party tools.

### 3.4 Returning customer loyalty check

1. Do not read loyalty off the returning customer rate card.
2. Click into the cohort analysis card to open the full report. Card [8f85f33352f5] gives the path Analytics > Reports > Cohort analysis. [verify UI]
3. Read repeat behaviour by acquisition cohort over time. Source gives no reading steps here and points to his separate tutorial video. [needs brand data: cohort table]

### 3.5 Dashboard clean-up

1. Use the "Customize" button in the top right of the Analytics dashboard to change the default layout. [verify UI]
Source only says the button exists. Card [bcb81bfb6f41] adds: remove attribution, social referral and returning customer rate cards; add net sales, shipping charges, sessions, conversion rate, AOV and the funnel; save. That list is the card's inference from the video. [web check: whether the dashboard can be customised on the brand's Shopify plan] [bcb81bfb6f41]

## 4. Rules, thresholds and numbers

| rule | number or threshold | condition | source's basis | card id |
|---|---|---|---|---|
| Top-line revenue | net sales + shipping charges | for profitability and marketing maths; card says label it sales-based, not cash | presenter's definition | a3ae4e9e2a00 |
| Exclude tax | total sales includes tax, so do not use it | any profitability calc | presenter's reasoning | a3ae4e9e2a00 |
| Revenue identity | sales = sessions x conversion rate x AOV | returns are the exception | arithmetic identity, presenter's framing | 9e9d4013f967 |
| Natural fluctuation | single-digit percent dips across a few levers | all levers otherwise stable | opinion; example 5% AOV + 4% CR dip | 9e9d4013f967 |
| Return-driven dip example | 20% of orders returned the next month | fashion, after a strong ad-driven month | example | a3ae4e9e2a00 |
| Funnel average | 4 add to cart : 2 reach checkout : 1 purchase (50% then 50%, 25% overall) | "general average"; check against your industry | presenter's client experience | c8e57ed1cd0a |
| Funnel target | 2 add to cart : 1 reach checkout : 1 purchase (50% then about 100%, 50% overall) | "very little drop off between checkout and purchase"; source says this is more for FMCG and low-ticket brands | "really good success with a lot of clients" | c8e57ed1cd0a |
| Funnel fix lift | +40% to +50% conversion rate "overnight" | after fixing a big step drop-off | client anecdote | c8e57ed1cd0a |
| Shipping share of revenue | about 7% to 8% of revenue collected at checkout, so real AOV about 7% higher | 1 client brand | example | 9b3f534de0a2 |
| Shopify AOV formula | (gross sales - discounts) / orders, no shipping | as the presenter reads Shopify [web check] | presenter's reading | 9b3f534de0a2 |
| Sessions gap | GA4 generally lower than Shopify | bots counted in Shopify | presenter's reading | 084db9abd48b |
| Unshipped orders | orders - orders fulfilled | selected period | dashboard definition | 9d66cacbbfcd |

Computed checks (not from source): 0.95 x 0.96 = 0.912, so the 5% and 4% example is an 8.8% drop; 0.90 / 0.912 = 0.987, so a 10% drop implies about 1.3% fewer sessions as well.

## 5. Diagnostics and checks

| check | how | good | bad | next step | card |
|---|---|---|---|---|---|
| Is the revenue dip real demand? | refunds by processing date vs order date | refunds flat | refund spike from a prior strong month | report returns separately; do not cut ads on it | a3ae4e9e2a00 |
| Which lever moved? | sessions, CR, AOV period over period | all within single digits | 1 lever down sharply | run 3.1 step 4 for that lever | 9e9d4013f967 |
| Are Shopify sessions inflated? | Shopify vs GA4 sessions, same dates | similar trend | Shopify spike or dip not in GA4 | run 3.3 | 084db9abd48b |
| Bot city spike? | Sessions by location, sort by city | spread matches market | 1 city spikes | treat as bot traffic; consider excluding | 57a97c0614d6 |
| Funnel health | ATC : checkout : purchase counts | 2:1:1 or better | worse than 4:2:1 | find the biggest step drop; fix layout | c8e57ed1cd0a |
| AOV understated? | shipping charges / revenue | shipping small | shipping a notable share (example 7% to 8%) | report AOV with shipping added | 9b3f534de0a2 |
| Right channel? | sales by channel | reports filtered to Online Store for paid media | POS, Shop app or draft orders mixed in | filter to Online Store | 6ca5944157b0 |
| Fulfilment backlog | orders - orders fulfilled | small gap | large gap | investigate unshipped orders | 9d66cacbbfcd |
| Loyalty signal | cohort report, not returning customer rate | cohort repeat curve read | decisions made on returning customer rate | switch to cohort view | 8f85f33352f5 |

Good and bad levels in this table are the source's only where it gave a number (funnel ratios, 7% to 8% shipping). Other thresholds are not given. [needs brand data: normal range for each lever]

## 6. Tools, settings and named features

All names as spoken in the video. [verify UI] on every item.
- **Shopify Analytics dashboard, "Customize" button (top right):** changes the default layout. [verify UI]
- **Gross sales, net sales, total sales:** context only; use net sales + shipping charges. [verify UI]
- **Shipping charges (formerly "shipping collected"):** add to net sales. [verify UI]
- **Returning customer rate:** ignore for loyalty. [verify UI]
- **Orders, orders fulfilled:** gap = orders not yet shipped. [verify UI]
- **Average order value:** excludes shipping per the source; mean only. [verify UI]
- **Sales channels (Online Store, POS, Shop app, draft orders):** filter to Online Store for paid media accountability. [verify UI]
- **Total sales by product:** helpful only when clicked into the full report; the 2-product card is "not really that helpful". [verify UI]
- **Sessions over time:** includes bots; compare with GA4. [verify UI]
- **Funnel (sessions, add to cart, reach checkout, purchase):** checkout troubleshooting. [verify UI]
- **Session types (mobile, desktop, tablet, other):** "no real core information"; source would not pay much attention. [verify UI]
- **Sessions by location:** click in, sort by city, find bot spikes. [verify UI]
- **Total sales by social referral, sessions by social referral, top referrals by session, sales attributed to marketing, sessions by referrer, total sales by referrer:** ignore. [verify UI]
- **Cohort analysis:** open the full report; one of Shopify's most useful. [verify UI]
- **Products sell-through rate:** inventory and cash planning (20-FIN). [verify UI]
- **POS analytics:** at the bottom; not discussed. [verify UI]
- **Google Analytics 4:** second source for sessions and conversion rate. [web check: GA4 bot filtering behaviour]

## 7. Examples and case results

All examples, none are promises.
- Fashion brand: strong ad-driven month, then 20% of orders returned next month, showing a false revenue dip and a false rise in blended CAC. [a3ae4e9e2a00]
- Client brand on screen: collects about 7% to 8% of revenue as shipping at checkout, so its real AOV is about 7% higher than Shopify shows. [9b3f534de0a2]
- Same client: a big conversion rate dip on 26 January that may have been a bot spike; not confirmed. [084db9abd48b]
- Clients: fixing an element below the fold or poorly placed in the funnel lifted conversion rate 40% to 50% "overnight". No counts or dates given. [c8e57ed1cd0a]
- Illustration: 5% AOV dip + 4% conversion rate dip, called a 10% top-line dip and "natural fluctuation". [9e9d4013f967]

## 8. Mistakes the source warns about

1. Using total sales (includes tax) or gross sales (before discounts and returns) as the revenue number. [a3ae4e9e2a00]
2. Reading a return-driven revenue dip as ad performance falling off or blended CAC rising, then changing marketing on it. [a3ae4e9e2a00]
3. Reading returning customer rate as the share of customers who come back. [8f85f33352f5]
4. Changing the business based on the single Shopify AOV number. [9b3f534de0a2]
5. Forgetting that shipping and free-shipping changes do not show in Shopify AOV. [9b3f534de0a2]
6. Trusting Shopify sessions and conversion rate without a GA4 cross-check. [084db9abd48b]
7. Using any Shopify attribution or referral card for decisions. [561513b3e85e]
8. Letting a partner report blended revenue across POS, Shop app and draft orders when paid ads drive the online store. [6ca5944157b0]
9. Judging the cohort analysis from the dashboard card instead of the full report. [8f85f33352f5]
10. Stressing over single-digit percent dips that compound into a larger top-line move. [9e9d4013f967]
11. New brands overlooking sell-through rate. [37f16297a48e]

## 9. Caveats, conflicts and what is missing

- **"Cash collected" label conflict.** Source calls net sales + shipping "cash collected" and "gross income within the P&L". Card [a3ae4e9e2a00] says it is a sales-based metric, not cash or profit, and that sales reports may include unpaid orders. Agent rule: use the source's formula for marketing revenue, label it "net sales + shipping", and take cash from payments reports. [a3ae4e9e2a00]
- **Returns: add back or separate.** Source adds returns back for some clients and also says separating returns "is sometimes really important" with high return rates, while calling net sales + shipping (which deducts returns) "the best measure". It never states when to use which. Card [a3ae4e9e2a00] says show refund timing separately and never call the add-back cash. Keep both; decide per brand return rate. [needs brand data: return rate]
- **Formula basis mismatch (observation, not from source).** The identity uses net sales + shipping on the left, but Shopify AOV excludes shipping and Shopify conversion rate uses bot-inflated sessions. The product of Shopify's own 3 numbers will not equal net sales + shipping exactly. Compute all 3 on one basis, in code, before claiming which lever moved.
- **2:1:1 scope is unclear.** Source says clients shifted to 2:1:1, then "this is more for FMCG brands as well as low ticket brands". Card [c8e57ed1cd0a] reads 2:1:1 as the target for low-ticket or FMCG only. 2:1:1 implies nearly 0 drop from checkout to purchase. No industry source is cited for 4:2:1. [web check: current Shopify funnel benchmarks by vertical and price point]
- **Metric definitions are the presenter's reading.** AOV formula, returning customer rate as orders-based, and Shopify keeping all bot traffic are not sourced. [web check: Shopify help docs for AOV, returning customer rate, sessions and bot filtering]
- **Attribution: absolute vs triangulate.** Source says ignore all attribution; card [561513b3e85e] says it is one input among several. Neither the source nor the card gives a replacement method beyond GA4.
- **Thin on how.** No steps to exclude bot traffic, no reading guide for cohort analysis (deferred to another video), no AOV analysis steps (deferred to another video), no threshold for "natural fluctuation", no definition of sell-through rate.
- **Card additions not in the source text:** sell-through = units sold / units received [37f16297a48e]; report paths "Analytics > Reports > ..." [8f85f33352f5] [57a97c0614d6] [6ca5944157b0] [c8e57ed1cd0a]; the list of cards to add or remove on the dashboard [bcb81bfb6f41]; fulfilment bottleneck causes, subscription churn and partial fulfilment notes [9d66cacbbfcd]; UTM and third-party attribution tools [561513b3e85e]; AOV levers like bundles and free-shipping thresholds [9b3f534de0a2]; funnel step causes [c8e57ed1cd0a].
- **Scope.** Sell-through and cash conversion cycle belong in 20-FIN per the folder header. Checkout fixes belong with CRO and landing page folders.

## 10. Card index

- a3ae4e9e2a00  Separate sales-based marketing revenue from actual cash receipts
- 9e9d4013f967  Revenue Troubleshooting Framework: Sessions x Conversion Rate x AOV
- 561513b3e85e  Cross-check Shopify attribution before reallocating spend
- 8f85f33352f5  Use Cohort Analysis Instead of Shopify's Returning Customer Rate
- c8e57ed1cd0a  Funnel Drop-off Ratios: 4:2:1 and 2:1:1
- 9b3f534de0a2  Average Order Value: Context and Limitations
- 084db9abd48b  Sessions Discrepancy: Shopify vs. Google Analytics 4
- 37f16297a48e  Product Sell-Through Rate for Inventory Planning
- bcb81bfb6f41  Customizing the Shopify Analytics Dashboard
- 57a97c0614d6  Identifying Bot Traffic via Location Report
- 9d66cacbbfcd  Orders vs. Orders Fulfilled for Operational Health
- 6ca5944157b0  Sales Channel Breakdown for Accountability
