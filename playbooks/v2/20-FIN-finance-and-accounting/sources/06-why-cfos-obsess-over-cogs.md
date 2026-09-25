# Why CFOs Obsess Over COGS

source_id: 1u39Ntqg9IsT72ZP0J9QGMTHUui7nPqSd  |  folder: /20-FIN-finance-and-accounting  |  cards: 9  |  words: 2576  |  type: transcript (YouTube talk, single presenter)
credibility: Presenter Bill Hannah, a financial controller who says he has about 20 years in corporate accounting and finance leadership. He sells courses on his website "the Controller Academy" and offers an Excel file that builds financial statements from sample data (both plugged). Evidence is his own experience plus 1 data point: a baby-food manufacturer where he worked ran about 30% gross margin. No studies, no client data sets, no worked numbers. Treat every rule as "Source 06 says". The source is written for finance leaders and founders of CPG (consumer packaged goods, makes physical products) and SaaS (software as a service) businesses. It never talks about online retail directly.
date signals: No year stated. Names AWS and Azure and says "most companies nowadays" rent servers instead of owning them. File modified in the library on 20 Sep 2026 (upload date, not publish date) `[web check: video publish date]`. The accounting ideas are basic and change slowly, but classification rules depend on the accounting standard in use.
scope note: The source header places this in 20-FIN. It routes supply chain sourcing and factory price negotiation to 18-COG, and product pricing and offer structure to 03-OFF. It says to skip the Controller Academy plug and like/subscribe requests. The header calls the scope "100% baseline" (basic definitions and reporting rules).

## 1. What this source is for

It helps an operator get cost of goods sold (COGS) right so that gross margin is true. A true gross margin tells you how much money each unit leaves for marketing and R&D, and it is what investors use, with revenue growth, to value the business. The source lists what goes into COGS for a physical-product business and for a software business, when those costs hit the P&L, typical gross margin ranges, and 6 common mistakes (waste, theft, freight, customer success, cloud costs, revenue share). It is strong on "what belongs where". It is thin on "how": no journal entries, no costing methods, no worked numbers.

## 2. Principles

### 2.1 COGS sets unit economics
From each unit sold, COGS decides how much money is left to spend on marketing and R&D. His example: "say we sell something for $10", COGS decides what is left from that $10. He gives no COGS number for the example. Card adaptation: if gross profit per unit cannot cover customer acquisition cost plus a share of overhead, the unit does not work at that price; this test is the card's, not the speaker's. [e65733468333] [aacabc94746b]

### 2.2 COGS drives valuation through gross margin
When VCs and private equity value a business they look at revenue growth and gross margin. Gross margin depends on COGS, so COGS matters to valuation. Card inference: a cost wrongly left out of COGS understates COGS, inflates gross margin and distorts the valuation. Card caveat: gross margin is not the only valuation input; growth, retention and market also count. [e65733468333]

### 2.3 COGS is only the cost of delivering the product or service
The source's test, stated for revenue share but used across all its mistakes: "COGS is only about the delivery of the service." If a cost does not make or deliver the product, it is not COGS. Selling and marketing costs go to operating expenses. [0dad09bf5876] [aacabc94746b]

### 2.4 Physical-product COGS is tangible
For CPG, the product can be touched, so COGS is tangible. Example company: Nike (sneakers and athletic wear). The COGS parts are listed in 3.1. [1939dcb79b5d]

### 2.5 Software COGS is mostly labor and servers
For SaaS, the product is not tangible (cloud based), and most COGS is labor: salaries of people who support delivery of the service. Example company: Salesforce (B2B sales and marketing platform). The COGS parts are listed in 3.2. [1939dcb79b5d]

### 2.6 Inventory is an asset until it sells
For CPG, making inventory creates an asset on the balance sheet. It moves to the P&L as COGS only when the inventory is sold. Card inference: building stock uses cash now and lowers reported profit later, so a stock-heavy quarter hurts cash before it hurts profit. [a490586f1272]

### 2.7 Software costs mostly hit the P&L at once
SaaS also has a balance-sheet-to-P&L flow, but only for fixed assets used to deliver the service (computers, owned servers), which move into COGS over time as depreciation. Support wages and implementation wages are recorded straight into COGS. If servers are rented from AWS or Azure, the monthly fee goes straight to COGS. [a490586f1272] [fe778e54daef]

### 2.8 Physical products run low gross margins; software runs high
CPG and manufacturing: high COGS, low gross margin, "typically" 20% to 40%. SaaS: lower COGS relative to revenue, "typically" 70% to 90%. Condition: these are the speaker's rules of thumb, not calculated thresholds. Card rule: use the bands to flag a possible misclassification or a price that is too low, not as a target. [1939dcb79b5d]

### 2.9 Higher margin is not the only way to win
Asked "should I go into SaaS instead of CPG?", he says SaaS has higher gross margin, but the choice depends on your skill. A CPG product with fast, wide distribution can take a small slice of a very large pie and still win. A strong SaaS idea has appealing margins. Opinion, no data. [1939dcb79b5d]

### 2.10 Get elements, timing and waste right, and the margin can be trusted
His closing: record the right elements, at the right time, watch waste and misclassification, and you arrive at the correct gross margin. That margin decides unit economics, which decides whether to make more of a product or discontinue it and make a new one, and it supports the valuation. [aacabc94746b] [e65733468333]

## 3. Procedures

### 3.1 Build COGS for a physical product (CPG)
The source's formula, written out:

COGS (CPG) = raw materials + direct labor + manufacturing overhead + freight-in + packaging

1. Raw materials: what the product is made of. Sneaker example: rubber, leather, laces.
2. Direct labor: wages of the people on the manufacturing floor who make the product.
3. Overhead: other costs that keep manufacturing running. Named: factory rent, depreciation of the factory if owned, depreciation of equipment, maintenance, utilities.
4. Freight-in: the cost to bring inventory (direct materials and packaging) into the factory.
5. Packaging: the box the finished product goes into.
6. Leave out freight-out (shipping to customers). It is a selling cost in operating expenses (see 3.5).

The source does not say how to allocate overhead per unit, how to value inventory (FIFO, weighted average), or how a reseller who buys finished goods should build COGS. Card note: inventory costing methods are not covered. [1939dcb79b5d] [a490586f1272] `[needs brand data: per-SKU materials or purchase cost, freight-in per shipment and how it is split across units, packaging cost per unit, any in-house making labor and overhead]`

### 3.2 Build COGS for a software or digital product (SaaS)
The source's list, written out:

COGS (SaaS) = server cost + tools to deliver the service + customer support wages + implementation wages

1. Server cost. If you own the server: its depreciation over time. If you rent from AWS or Azure (the common case for small businesses): the monthly fee.
2. Tools to deliver the service: APIs and third-party tools needed to deliver the product.
3. Customer support wages: pay for support staff.
4. Implementation wages: salaries and benefits of the team that onboards the client onto the product they bought.
5. Leave out customer success wages and third-party revenue share for marketing partners (see 3.5).

Relevance to an online store: only where the store sells a hosted, app or subscription product. Card 332efa25ba89 applies the support-cost idea to subscription or membership stores. [1939dcb79b5d] [fe778e54daef] [332efa25ba89]

### 3.3 Record COGS at the right time
1. Physical products: when you make or buy inventory, record it as an asset on the balance sheet. Card adds: include freight-in in that inventory cost.
2. When a unit sells, move its cost from inventory to COGS on the P&L.
3. Software: record owned delivery assets (servers, computers) as fixed assets; depreciate them into COGS over time.
4. Record support wages, implementation wages and rented server fees straight into COGS as incurred.
5. Card addition: when auditing, match physical-goods cost to the period the sale happens, not the period the invoice arrived.
[a490586f1272] [aacabc94746b]

### 3.4 Control waste (expiry, obsolescence, theft)
1. Track expiry and obsolescence dates for your goods.
2. Ship the stock with the nearest expiry or obsolescence date first, before stock with a longer window.
3. If stock gets very close to expiry, run a fire sale: sell fast at a much lower margin to get it moving. Card caveat: a last resort to recover cash, not routine strategy.
4. Log inventory when it comes into the warehouse and when it goes out.
5. Run periodic inventory counts to check nobody is stealing stock.
6. Card additions (not in the transcript): investigate recurring count gaps as shrink or process error and feed the cost back into COGS assumptions; apply the same rotation to seasonal goods (oldest season first, discount before the next season lands). Card caveat: count frequency depends on volume and risk; the source gives none.
[2d244e2a4df6] `[needs brand data: stock by SKU with receive date and expiry or obsolescence date, inbound and outbound logs, last count results]`

### 3.5 Classify borderline costs
Apply the test in 2.3: does the cost make or deliver the product?
1. Freight-in (materials and packaging to the factory): COGS.
2. Freight-out (shipping product to customers): not COGS. It is a selling cost in operating expenses.
3. SaaS customer support and implementation wages: COGS.
4. SaaS customer success wages: not COGS. Customer success makes sure the user can use the product and buys more (upsells). It is a selling function, so operating expenses.
5. Revenue share paid to a third party that only markets your product: not COGS. It is a marketing cost in operating expenses. If the third party is involved in delivering the service, it can be COGS.
Cards 0f57ba17ebb2, 332efa25ba89 and 0dad09bf5876 soften this: identify what the charge buys, then follow the accounting policy that applies to you rather than a label from another business model, and track the charge separately per order or channel. [0f57ba17ebb2] [332efa25ba89] [0dad09bf5876] `[web check: freight-out and shipping cost classification under the accounting standard the brand reports under]`

### 3.6 Keep cloud costs tied to usage
1. Treat the monthly AWS or Azure fee as COGS (rented servers).
2. Tie cloud cost to business usage. When a B2B business adds a new enterprise client, tie the cost of that client to a line in the AWS or Azure bill.
3. Check you are not "paying double" for each added customer.
4. Hold periodic meetings between finance and engineering to agree how cost should move as the business grows. No cadence given.
5. Card addition: build a per-customer or per-usage view of infrastructure cost to see whether economics improve or get worse with scale.
Card caveat: cloud pricing and cost dashboards change `[verify UI]`. [fe778e54daef]

### 3.7 Use the corrected margin to decide (card-built, from the source's closing)
The transcript gives the goal; the steps are the cards' adaptation.
1. Audit each COGS line: goods-related costs in, selling and promotion costs out (3.5).
2. Audit timing (3.3).
3. Recalculate gross margin. Standard definitions, not written out in the source: gross profit per unit = price - COGS per unit; gross margin = (revenue - COGS) / revenue.
4. Card 0f57ba17ebb2 and siblings: reconcile gross profit down to contribution after variable fulfillment, commissions and support costs before setting CAC limits.
5. Check whether the margin still supports price, acquisition cost and overhead share.
6. Decide: make more of the product, reprice, or discontinue and build a new one. Pricing moves go to 03-OFF.
7. Keep 1 per-SKU gross profit sheet so pricing and promotion decisions use the same numbers shown to investors.
8. Redo the audit when the model changes, for example moving from self-fulfilment to a 3PL, or from owned to rented infrastructure. No cadence in the source; the card suggests monthly or quarterly.
[aacabc94746b] [e65733468333] [0f57ba17ebb2] `[needs brand data: price, discounts, COGS, shipping, payment and marketplace fees, commissions and support cost per order or SKU]`

## 4. Rules, thresholds and numbers

| rule | number or threshold | condition | source's basis | card id |
|---|---|---|---|---|
| CPG / manufacturing gross margin | 20% to 40% "typically" | physical product maker with high COGS | speaker's rule of thumb | 1939dcb79b5d |
| SaaS gross margin | 70% to 90% "typically" | software, low COGS | speaker's rule of thumb | 1939dcb79b5d |
| Baby-food maker gross margin | about 30% | 1 company he worked at; "typical for that kind of business" | own experience | 1939dcb79b5d |
| Freight-in | in COGS | bringing materials and packaging to the factory | stated as rule | 0f57ba17ebb2 |
| Freight-out | not COGS; selling cost in opex | shipping product to customers | stated as rule; cards defer to your accounting policy | 0f57ba17ebb2 |
| Packaging (product box) | in COGS | CPG | stated | 1939dcb79b5d |
| Owned server | into COGS as depreciation over time | owner of hardware | stated | a490586f1272 |
| Rented server (AWS, Azure) | monthly fee straight to COGS | most small companies | stated | fe778e54daef |
| Support and implementation wages | in COGS, recorded directly | SaaS | stated | 332efa25ba89 |
| Customer success wages | not COGS; opex | SaaS, team drives usage and upsell | stated | 332efa25ba89 |
| Revenue share to marketing partner | not COGS; marketing opex | partner not involved in delivery | stated | 0dad09bf5876 |
| Inventory | balance sheet asset until sold, then COGS | physical goods | stated | a490586f1272 |
| Stock rotation | nearest expiry or obsolescence date ships first | perishable or dated goods | stated | 2d244e2a4df6 |
| Fire sale | sell at much lower margin | stock very close to expiry | stated; card calls it last resort | 2d244e2a4df6 |

## 5. Diagnostics and checks

| check | how | good | bad | next step | card |
|---|---|---|---|---|---|
| Gross margin sanity | compute (revenue - COGS) / revenue and compare to the source's band for the model | inside or explained | far outside the band | look for misclassified costs or a price that is too low; do not treat the band as a target | 1939dcb79b5d |
| Freight-out in COGS | review COGS accounts for customer shipping charges | only freight-in in COGS | customer shipping booked to COGS | reclassify per your accounting policy `[web check: standard]`; still count it in contribution | 0f57ba17ebb2 |
| Freight-in missing | check inventory cost includes inbound freight | included | inbound freight expensed separately | add to inventory and COGS | a490586f1272 |
| Revenue share in COGS | list partner payouts in COGS | none unless partner delivers | marketing-only partner payouts in COGS | move to marketing opex; track per channel | 0dad09bf5876 |
| Customer success in COGS | split delivery team into support, success, implementation | success in opex | success wages in COGS | move to opex | 332efa25ba89 |
| Cloud cost vs usage | cloud cost per customer or per usage unit over time | flat or falling as you grow | rising fast, or new customers doubling cost | finance and engineering review | fe778e54daef |
| Expiry exposure | list stock by expiry or obsolescence date | nearest dates moving first | long-dated stock shipping while short-dated sits | rotate; fire sale if very close | 2d244e2a4df6 |
| Shrink | compare counts to in and out logs | counts match logs | gaps, or no outbound log | add outbound logging; count periodically; investigate | 2d244e2a4df6 |
| Timing | compare COGS period to sale period for goods | cost booked when unit sells | cost booked when invoice arrives | correct timing (card addition) | aacabc94746b |
| Unit viability (card) | gross profit per unit vs CAC plus overhead share | covers both | does not | reprice (03-OFF) or discontinue | e65733468333 |

## 6. Tools, settings and named features

- AWS (Amazon Web Services) and Azure: rented server space; monthly fee is SaaS COGS. Cost tools change `[verify UI]`. [fe778e54daef]
- Excel file from the speaker: builds financial statements from sample data. Plug; not described further.
- Controller Academy: the speaker's website. Plug; skip.
- No accounting software, inventory system or ecommerce platform is named.

## 7. Examples and case results

Examples only, not promises.
- $10 unit: COGS decides what is left for marketing and R&D. No COGS figure given.
- Nike (CPG): tangible COGS. Sneaker inputs rubber, leather, laces; factory floor labor; factory rent and equipment depreciation; freight-in; the shoe box.
- Salesforce (B2B SaaS): intangible product; COGS mostly labor supporting delivery.
- Baby-food manufacturer the speaker worked at: about 30% gross margin, which he calls typical for that business.
- No before-and-after results or dollar figures for any mistake.

## 8. Mistakes the source warns about

1. Expired goods: not tracking expiry and obsolescence dates, so stock expires; fix with nearest-date-first rotation and, near expiry, a fire sale. [2d244e2a4df6]
2. Stolen products: no inventory control logging stock leaving the warehouse; fix with in and out logs plus periodic counts. [2d244e2a4df6]
3. Freight misclassification: booking freight-out to COGS; he says he sees this "often". [0f57ba17ebb2]
4. Customer success in COGS (SaaS): it is a selling function. [332efa25ba89]
5. Unchecked server costs (SaaS): AWS or Azure bills "rise quickly" if not tied to usage. [fe778e54daef]
6. Revenue share in COGS (SaaS): marketing-only partner payouts belong in operating expenses. [0dad09bf5876]
7. Card addition: understating COGS inflates gross margin and misleads valuation. [e65733468333]
8. Card addition: treating the margin bands as targets instead of as flags. [1939dcb79b5d]

## 9. Caveats, conflicts and what is missing

- Business model gap: the source covers makers (CPG) and SaaS. It does not cover online retailers who buy finished goods, so it says nothing about landed cost, import duties, supplier freight, 3PL pick and pack, payment processing fees, marketplace fees, returns, discounts or free shipping. Any ecommerce use is an adaptation. `[needs brand data: full cost per order breakdown]`
- Conflict with common ecommerce advice on freight-out: the source (and its header, "strict accounting rule") says customer shipping is never COGS. Many DTC operators, P&L dashboards and some large retailers put outbound shipping and fulfillment in cost of sales, and some standards let the business choose a policy and disclose it. The cards already soften the source: follow the accounting policy that applies and track the cost separately. What both sides agree on: outbound shipping is a variable cost that must be counted before setting CAC limits. `[web check: US GAAP ASC 606 shipping and handling policy election; Ind AS and IFRS treatment for Indian brands]`
- Margin bands: DTC brands with low unit costs often report gross margins above the 20% to 40% CPG band, so an ecommerce margin above 40% is not by itself a sign of error. `[web check: gross margin ranges by ecommerce category]`
- Customer success: some SaaS companies put part of customer success cost in COGS. The source states its view as a rule with no standard cited. `[web check: SaaS customer success COGS practice]`
- Cards 0f57ba17ebb2, 332efa25ba89 and 0dad09bf5876 share the same 4 generic bullets. Their "reconcile to contribution" step is the cards' idea, not the speaker's. Their caveat says service and software examples do not set COGS rules for a physical-product store; note that the freight rule is from the CPG part, not the software part.
- Missing how: no overhead allocation method, no inventory costing method (FIFO, weighted average), no write-down or shrink accounting entries, no count frequency, no meeting cadence for cloud review, no audit cadence, no worked COGS or margin calculation.
- Card additions beyond the transcript: per-SKU gross profit sheet, CAC coverage test, timing audit wording, seasonal rotation, count-variance investigation, re-audit on 3PL move. All reasonable; none stated by the speaker.
- Expiry and fire-sale advice applies to dated or perishable goods; for non-perishable goods only the obsolescence part applies.
- Sourcing and factory price negotiation live in 18-COG; pricing and offer structure live in 03-OFF.

## 10. Card index

- e65733468333 COGS Drives Unit Economics and Valuation
- 0f57ba17ebb2 Separate inbound inventory freight from customer delivery costs
- 1939dcb79b5d CPG vs SaaS Cost Structures and Margin Benchmarks
- a490586f1272 Balance Sheet to P&L Timing for Inventory Versus Services
- 332efa25ba89 Classify ecommerce customer support costs consistently
- 0dad09bf5876 Separate partner commissions from product acquisition cost
- fe778e54daef Tie Server and Hosting Costs to Business Usage
- 2d244e2a4df6 Waste Control: Expiry Rotation, Fire Sales and Inventory Controls
- aacabc94746b Correct COGS Gives a Trustworthy Gross Margin Signal
