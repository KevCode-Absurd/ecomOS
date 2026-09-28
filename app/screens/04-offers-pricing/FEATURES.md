# Offers and pricing: features

Status: todo | doing | done | parked. One feature per commit. The first round is the skeleton; after that, features come in rounds of 10, stack-ranked by revenue impact, usefulness and how easy they are to build on dummy data.

## Round 0: skeleton (done 28 Sep 2026, S3.9, Bombas simulated data)

| # | Feature | Status |
|---|---|---|
| 0.1 | Page shell in the shared UI kit: header, simulated-data banner, tiles, insights, decision row, findings | done |
| 0.2 | `api.py`: `overview` and `findings` under `/api/04-offers-pricing/`, unavailable states, sample brand degrades | done |
| 0.3 | 3 tiles (free shipping threshold vs AOV and break-even, discount share of gross, multi-pack share), 2 insights as rules (threshold pull and move rule; discount creep), 1 chart (AOV and discount share by month, 24 months) | done |
| 0.4 | Offer stack from the brain: threshold, shipping under it, first-order code (ad library, first and last seen), code share in live ads, pack ladder, guarantee, return window, gifting; each with source, link and date | done |
| 0.5 | Free shipping threshold economics: order value in $5 bins (paid vs free), share $10 just under and just over, break-even (AOV + label / margin), the move rule | done |
| 0.6 | Discount policy: discount share by month, BFCM depth against the 28 days before | done |
| 0.7 | Pack ladder: revenue and packs by pack size, paid and list price per pair, drop per rung and vs the single | done |
| 0.8 | Guarantee against objections: top rung of each ladder, proof or none, returns per 1,000 orders for the matching reason | done |
| 0.9 | `audit.py`: OFFER-R01 threshold under break-even (money), OFFER-R03 per-SKU margin unavailable, OFFER-R04 deal-breaker rung with no proof (money floor from returns when above own median) | done |

Metrics added in their own commits: `order_value_distribution`, `returns_by_reason` (`app/contracts/metrics.md`, Offers section).

Known gaps from round 0:
- Per-SKU margin is unavailable: `finance_inputs.json` keys cost by codes like `BMB-SK-M-ANK-1`; products use `BB-ANK-1`. Break-even uses the target gross margin until they join.
- Order-level numbers (bins, returns by reason) read `data.sqlite`; the page shows them as shares or per-order rates and takes volume from the daily totals, so a scale 0.1 build and the scale 1.0 aggregates agree.
- Simulated orders charge $5.99 under the line and use their own codes; the brain's public values ($7.95, COMFORT20) are shown beside them.
- The brain lists 7 and 12 packs; the simulated catalogue has 1, 3, 4, 6 and 8. The 6-pack ankle sock gives no per-pair drop over the 4-pack (a LIFE-C39 candidate).

## Round 1: the execution surface (from 28 Sep 2026, depth contract)

| # | Feature | Status |
|---|---|---|
| 1.1 | Plan first: round 0 tiles, insight cards and the AOV chart removed; plan board from `rank` with 6 orientation numbers (AOV, threshold, orders under it, refunds share, ads with the code, contribution margin); what is wrong ranked; action cards with owner, steps and artefact; desk; audit at the bottom. `actions.py` (rank override), `model.py` (offer economics), `screen.css`. OFFER-R01 now fires from the aggregates and finance inputs when order rows are absent (money null with its reason) | done |
| 1.2 | Objection ladder to offer map: the top rung of every ladder with the offer or proof that answers it (`playbook.py`, brand-agnostic), what in the brain already covers it, cost per claim from finance inputs (item or returns processing, label, pick and pack, box), cost per 1,000 orders at the brain's planned claim rate, returns behind it (labelled fixture while `returns_by_reason` is unavailable). Each open rung is an action with the drafted spec, win and stop rules. OFFER-R04 severity high at 20 one-star mentions; rubric override reputation 4, satisfaction 4 | done |
| 1.3 | Free shipping line: order value bins with the $10 under the line shaded (labelled fixture while order rows are absent), break-even by month against the line (step chart), the gap, and a table of nearby lines with what each must achieve to pay: a higher line pays while fewer than N percent of orders between the lines walk away, a lower one only if orders in the band rise N percent (contribution before media from finance inputs, listed shipping rate from the brain). The test brief carries the walk-away limit. New rules OFFER-R05 (break-even moved more than 5 percent in a year, line did not) and OFFER-R06 (line not pulling, unavailable without order rows) | done |
| 1.4 | Pack ladder: per line, singles' share of packs, the pack saving per item, margin per pack from cogs_landed, and the deeper price test's arithmetic (money given to current pack buyers against margin per trade-up, so the share of single buyers who must trade up). Verdicts push (keep price, preselect the pack, show price per item), deepen (a price test pays back under 25 percent trade-up), add (a basics line sold only as a single gets a pack). New rules OFFER-R07 and OFFER-R09, one merged action per verdict with the drafted page spec, test brief or pack offer; thresholds in `playbook.py`. Ladder math moved to `model.py` | done |
| 1.5 | First-order offer: the code against 4 alternatives (free item, free shipping, dollars off at the line, first-order pack price) at the average list-price order: price paid, cost against full price, contribution before media, payback on paid media per new customer, and how much first-order conversion each can lose against the code. Flags that the code takes the average basket under the free shipping line (the line counts after discount). New rule OFFER-R08 (code in more than half the active ads and a price-keeping offer keeps more), with the test brief and paired ad variants. Money is labelled "at equal conversion" | done |
| 1.6 | Margin waterfall per offer (`Charts.waterfall`, pills to switch): the average order, the first order with the code, the first order with a free item, an order at the free shipping line, the average order with the wear promise; list price, discount, landed cost, pick pack and box, shipping net, payment fee, returns at the brain model rates, before media, paid media, contribution. Each step names its source; a missing input breaks the step and every total after it. Red line: a first order must pay its own media, other orders keep the target contribution margin; proposed offers under it cannot clear approval. New rule OFFER-R10 (live offer under the red line), merged into the first-order test when it is the code | done |
| 1.7 | Promo calendar: 8 US retail windows by date rule (`playbook.PROMO_WINDOWS`, a brand in another market swaps the list), next dates, the approval date (start minus the window's lead), last year's net sales per day against the 28 days before and the discount depth, and whether a brain `plans` record covers it. Timeline plus a verdict table. New rule OFFER-R11: a window due in 30 days with no plan becomes a dated offer spec (approve, briefs, site loaded, report dates), a margin check at last year's depth and a depth cap; money is last year's sales above baseline | done |
| 1.8 | Gifting and the holiday offer: a holiday index per line (its November and December share over the store's), the gift card and bulk gifting records, order-by dates for December 24 per shipping option from the brain (business days), the gift card ledger as unavailable. New rules OFFER-R12 (no line sells as a gift while a gift program runs; rides on the holiday window's action, whose artefact becomes the landing page spec: hero, gift boxes from packs of 6 or more, gift card, bulk gifting link, order-by bar, proof) and OFFER-R13 (gift card liability, a connect action) | done |
| 1.9 | Guarantee as an offer: its terms from the brain with the page type each was found on (url path rules in `playbook.PAGE_TYPES`), the ladder doubts it answers (rungs whose proof cites it) with one-star counts, and the planned refund and replacement rates from the brain's return model against actual claims (unavailable until returns connect). New rules OFFER-R14 (every term traces to a non-selling page while rungs cite it: a guarantee block for the product page and cart drafted from the brain's own terms, with its claim cost at plan and a stop at 1.5 times plan; first step checks the live page read-only) and OFFER-R15 (claims against plan, a connect action) | done |
| 1.10 | `rank` complete: every rule has a builder with a real title, owner, steps with who, a drafted artefact (offer, price_change, test_brief, page_section, landing_page, policy, report), win and stop rules and a check date; merged moves (pack verdicts, the code and its red line, the holiday window and gifting, the stale and pull rules into the threshold test) carry every finding id; connect actions merge by source ("Connect shopify, read-only, so 3 rules can run"). Tests: every finding in exactly one action, every action passes `validate_action`, no default titles on open work, a person approves every open move, same order on the same inputs, an older window validates | done |

### Round 1 note for Kevin (28 Sep 2026)

1. What a founder can do now: open the screen and approve 13 offer and price moves, each with its spec or test brief drafted, who does each step, and the win and stop rules.
2. Top of the plan: build the holiday gifting page and offer by 18 Oct and the Black Friday offer by 13 Oct (last year's lift and depth, dated prep plan, depth cap, order-by dates).
3. New judgement encoded: the 20 percent code takes the average first basket under the $75 line and loses $1.32 after media; a free item keeps $40.52 and can lose 24 percent of first-order conversion and still win.
4. Pack ladder: a deeper pack price would give millions to current pack buyers, so 5 lines get the pack preselected instead; 1 line gets a price test; 4 single-only basics lines get a pack.
5. Honest gaps: order rows and returns are not in this container, so bins and returns show labelled fixtures and 3 rules sit behind one "connect shopify" action.
6. Next (round 2): discount ladder discipline and creep, price elasticity from experiments, marketplace price parity through the data layer, loyalty and referral offers, the web pass on the best offer tools.

## Round 2: the market and the discipline (from 28 Sep 2026)

| # | Feature | Status |
|---|---|---|
| 2.1 | Price and offer position against the set (`Charts.positioningMap`): each competitor's median price per item from its price band in the brain, the discount its ads show (Ad Library offers seen), the proof its ads sell (hook types), against our paid price per item in the main category and the code share of our ads. New rule OFFER-R16 (discount-led in a proof-led set; reputation 5) with 3 ad briefs that lead with proof (guarantee terms, the top open doubt, the brand's price frame), competitor ads as signals only. Idea bank: MULTI-154, BRD-036 | done |
| 2.2 | Marketplace price parity: every marketplace listing in the brain with a price and a pack count in its title, its price per item against the site's paid price per item at the same pack size, the gap, the seller, and the channel's last full month from `marketplace_monthly` for scale. New rule OFFER-R17 (listings more than 10 percent under the site; reputation 4) with a person-owned parity list: check each seller, then minimum advertised price for authorised sellers, brand protection for unknown ones. Web pass: Prisync MAP and SmartPrice | done |
| 2.3 | Discount discipline: discount share by month (24 months) and a scorecard for the last 365 days against the 365 before (median day, promo days at 1.5 times the median, net sales on promo days, discount dollars spent on ordinary days, blended 90-day rate), and a discount policy drafted from the brand's own history (depth cap at last Black Friday, promo days cap, no stacking, the always-on code, a monthly review). New rules OFFER-R18 (room spec creep, money = extra points times gross) and OFFER-R19 (more than 75 percent of discount dollars on ordinary days while the code is in most ads; rides on the first-order code test). Web pass: Metricuno blended discount rate, Common Thread BFCM depth | done |
| 2.4 | Which item to give: single items ranked by paid price over landed cost (bar 4x, from the web pass; flagged when no item clears it). The first-order test, its money and the free-item waterfall now use the named item instead of a median item cost. Web pass: Common Thread (high perceived value, low cost gifts) | done |
| 2.5 | Cart reward ladder: tier 1 free shipping at the line, tier 2 the named gift one item past it (rounded to $5), its cost with the pick fee, the added value after which it pays (gift cost over the contribution share before media), how many times the climb covers it, and the leak of orders already past tier 2 (unavailable without order rows). New rule OFFER-R20 (the brain names a cart app but the offers have one reward) with the two-tier bar spec. Test and page steps now name the brand's own tools from the brain stack (A/B testing, upsell app). Web pass: Rebuy tiered progress bar | done |
| 2.6 | Test calendar (room spec: overlapping offer tests, offer test backlog): every open move declares the surface it changes (cart rewards, first order offer, ad angle, a theme's product page promise, the guarantee block, the pack selector, pack price, new packs, marketplace listing) and its length; the scheduler starts each 7 days out for approval, queues moves that share a surface, and keeps every move out of the promo windows. Verdict per move (starts first, waits, after the peak), what it waits for, CSV export | done |
| 2.7 | Promo depth by line: for each line's best-selling pack, the deepest tier (30, 25, 20, 15, 10 percent) that keeps the target contribution margin after its share of fulfilment and paid media, or a gift when no tier clears. The Black Friday offer spec now carries the tiers by line. Web pass: Common Thread (depth by margin and stock; stock waits on inventory rows) | done |
| 2.8 | Second-order offer: the cohort curve (share of new customers active in months 1 to 6, weighted by cohort size) and the month after which it falls most. New rule OFFER-R21 (no offers record speaks to past buyers) with a 3-message flow drafted to land before the drop: no percent off, the pack upgrade from the ladder, the cart gift; a 20 percent holdout; on the test calendar as its own surface. Web pass: Klaviyo (past buyers get no discount) | done |
| 2.9 | Cost against price: landed cost in force today against a year ago per SKU (finance history), paid price per pack over the last 3 full months against the same 3 a year before, margin leaked per pack and over 12 months, and a test price that restores margin dollars (rounded up to $1) with the conversion it can lose and still earn more. New rule OFFER-R22 (cost up more than 3 percent, price did not follow; money is the leak scaled to 28 days) with a price test brief that also cites our price against the set median. Web pass: Intelligems profit per visitor | done |
| 2.10 | The desk as 4 job tabs (Launch next, Offers, Prices and packs, Shipping and discounts) with the count of open moves in each, the last tab remembered per viewer; phone width fixed (action card rows wrap, tabs wrap, no content past 390 px); round 2 screenshot | done |

## Round 3: tests, loyalty and discipline over time (from 28 Sep 2026)

| # | Feature | Status |
|---|---|---|
| 3.1 | Experiment registry: read from the shared `registry` table when it exists, else the seed file events.md names (data only). Each test is mapped to this screen's surfaces (`playbook.REGISTRY_SURFACES`). Running tests hold their surface in the test calendar until their read point; a move whose surface and brain records match a running test becomes "read EXP-xxx, then roll out"; a finished test that cites a ladder rung becomes its proof (EXP-003's fit finder for the fit doubt). Price elasticity reads from finished price tests, unavailable until one exists. Desk block in Launch next | done |
| 3.2 | Referral offer: give one, get one, paid in product (2 gift items at landed cost plus the pick fee) against paid media per new customer, capped at half of paid CAC (room spec). New rule OFFER-R23 (no referral program named in the brain's offers or stack, and the offer clears the cap) with the spec, placements, win and stop rules; on the calendar as its own surface. Desk block "What do we offer people who already buy?" in Offers | done |
| 3.3 | Loyalty offer: 5 percent back in points, priced as a share of gross margin paid in cash against paid in product at landed cost (the product route costs about a quarter as much), against a 25 percent cap flagged as our own heuristic. New rule OFFER-R24 (no loyalty program in the brain) with the spec, placements, win and stop rules; the tool name comes from the brain stack when present | done |
| 3.4 | Discount ladder creep over time: each promo window's depth in its last two occurrences, the change in points and how much deeper than the 28 days before it ran, as a year-on-year table in the discount block. New rule OFFER-R25 (a window more than 2 points deeper than the time before; money is the extra points times the window's gross) with the discount policy as its action. For this brand every window held or cut its depth, so the rule is quiet | done |
| 3.5 | Subscription as a note, not built (founder: non-subscription first): the month 1 and month 6 repeat shares from the cohort curve, the deepest subscribe discount each top line could fund at the red line (from 2.7), and the 3 questions the data cannot answer yet (wear-out interval, repeat by first pack, cancel save rate). No rule, no action; the desk block says it is parked | done |
| 3.6 | depth.md section 3 on this screen: every open move now has a size, a stop rule and a check date (rule 5; 4 sizes and 4 stop rules added), no banned words or em dashes in any title, why, step or draft (rule 12), every desk block ends in a next-move line, including unavailable ones through the section helper (rule 9), and every desk heading is a question. Tests enforce all four | done |

## Round 4: from approval to the brain (from 28 Sep 2026)

| # | Feature | Status |
|---|---|---|
| 4.1 | Save a move to the brand brain (`approvals.py`, `POST /api/04-offers-pricing/approve {id, mode}`): the move becomes a `plans` record written only through `Brain.put`. Mode proposed: status proposed, tier inferred, source agent with the finding ids as derived_from, so it lands in the brand brain review queue. Mode founder: status active, tier approved, source founder. The record carries the move id, the drafted artefact, steps, win and stop rules and check date, and the window for promo moves (OFFER-R11 then counts the window as planned once approved). A testable move also gets a proposed registry row in the events.md shape in this screen's outbox. Moves with a plan record leave the open plan and are listed under it. Two buttons on each action card | done |
| 4.2 | Approved offers become offer records: a founder-approved move of kind offer, price change or landing page also writes an `offers` record through `Brain.put`, proposed while planned (so no other screen reads it as live), carrying its terms, plan id and stop rule. `POST launched {id}` (the "Mark launched" button on the planned list) turns it active with valid_from today; it refuses before the founder approves | done |
| 4.3 | Bundles from pairs: products bought together in the last 90 days of orders (orders holding both, lift over chance, share of the first item's orders), each pair's paid prices, a bundle at 10 percent off and its margin where landed cost is on file. New rule OFFER-R26 with a "complete the set" offer for the top 3 pairs, placed in the upsell app named in the brain. Real on the sample brand's orders (tea towels with napkins at 3.0x); for Bombas it waits on order rows and joins the connect move. Desk block in Prices and packs. Web pass: Fast Bundle frequently bought together | done |
| 4.4 | The red line blocks approval (room spec): moves priced by a margin waterfall (the first-order test by the free-item offer, the wear promise by the promise waterfall) carry a margin check in their draft; a founder approval of a move under the red line is refused with the reason, while proposing it for review stays open | done |
| 4.5 | Approved moves first: a move with an active plan record in the brain takes its surfaces first in the test calendar and shows as approved; the registry block lists the rows this screen has proposed and not yet registered | done |
| 4.6 | Read launched offers: new rule OFFER-R27 fires when a live offer this screen launched passes its plan's check date, with net sales per day, AOV and discount share since launch against the 28 days before (store-wide, labelled a signal; the result lives in the registry) and a drafted read that ends in keep, change or end. The registry block lists the live offers. Tested end to end on a copy of the brain (approve, launch, read) | done |
| 4.7 | Upsell take rate (room spec): new rule OFFER-R28, unavailable until the upsell app the brain names (Rebuy for Bombas) connects, so it shows as its own connect move ("Connect Rebuy, read-only") with what to pull; silent for a brand whose brain names no upsell app | done |
| 4.8 | Export all briefs (depth.md section 7): `GET /api/04-offers-pricing/briefs` builds one plain-text file of every open move (why, owner, score, stake, steps with who, the drafted artefact, win and stop rules, check date); an "Export all briefs" button beside the plan downloads it. Works for a brand with no folder too | done |
| 4.9 | Stale inputs: a move that rests on a brain record older than 90 days names it in its why and gets a first step for a person to refresh it on the brand brain screen. Quiet for Bombas today (every record is current) | done |
| 4.10 | Round close: 786 screen tests run, only the 4 known site speed tests fail; rank tests green; phone width clean at 390 px; round4.png; this note | done |

### Round 4 note for Kevin (28 Sep 2026)

1. What a founder can do now: on any move, press "Propose as a plan" (it goes to the brand brain review queue) or "I approve: save as a plan" (an approved brain record), written only through the brain's own store.
2. An approved offer becomes an offer record, planned until you press "Mark launched"; from then it is live for every screen, and after its check date the screen drafts a before and after read with a keep, change or end decision.
3. The red line now blocks approval: an offer under its margin line can be proposed for review but not approved.
4. Every approved test is proposed to the experiment registry (waiting in this screen's outbox until the shared table exists), and approved moves take their slot first in the test calendar.
5. New from data: bundles from products bought together (real on the sample brand; Bombas waits on order rows), upsell take rate waits on Rebuy, and one export holds every brief.
6. Next (round 5): offer records read back into the stack and the waterfalls, gift card liability once the ledger connects, and the web pass again for what the best tools added since.

## Round 5: read back and new rules from the second web pass (from 28 Sep 2026)

| # | Feature | Status |
|---|---|---|
| 5.1 | Offer stack read-back: offers written by approvals on this screen appear in "What does a shopper get from us today?" as Planned or Live, with their terms, source and date, read back from the brain (proposed records included on purpose, marked planned) | done |
| 5.2 | Break-even discount and volume multiple per line (web pass 2: Saras, Nebulab): contribution before media over price is the deepest discount a line can take before it earns nothing, and the units a 20 percent cut needs to keep the same contribution. Two new columns in the promo depth table; the Black Friday spec carries a volume check | done |
| 5.3 | Profit per visitor as the test metric (web pass 2: Intelligems): every registry row this screen proposes names profit per visitor (revenue minus promo cost, landed cost and shipping, over visitors, per arm), direction up, 28 days minimum, registered on the day it is proposed | done |
| 5.4 | Pack labelling (web pass 2: Eightx on decoys and the target tier): the pack selector spec labels the pushed pack "Most popular" when it already leads its line's units, places it as the middle choice, and measures the pack mix, not only conversion | done |
| 5.5 | Pay in installments (room spec LIFE-C46; web pass 2: Shopify's documented $35 US minimum for Shop Pay Installments, lift claims not read in full so not used): new rule OFFER-R29 when packs at $35 or more carry a share of revenue and the brain names no installment provider. The action is a page test judged on profit per visitor after the provider fee, starting with a person confirming what checkout already offers | done |
| 5.6 | Loyalty calibration (web pass 2: Smile.io): the first reward is sized inside 3 to 10 percent of AOV and reached in 1 to 3 orders at the earn rate, with its cost paid in product; shown in the loyalty card and the spec | done |
| 5.7 | One free shipping line everywhere (web pass 2: Rebuy, the cart bar must match the real rule): new rule OFFER-R30 when the offers record and the shipping policy's free tier disagree, a broken policy promise, with a person-owned fix across the brain, the policy page, the cart bar and the shipping app on the same day. Quiet for Bombas ($75 in both) | done |
| 5.8 | Code-won customers (web pass 2: Saras): customers whose first order used a code against full-price first orders, repeat within 180 days, first orders at least 180 days old, at least 200 customers a group. New rule OFFER-R31 when code-won customers repeat 20 percent less; it rides on the first-order code test, else its own test judged on profit per visitor and repeat. Real on the sample brand's orders (33 percent both ways, so quiet); a connect move for Bombas | done |

## Round 6: depth pass, room jobs, 360 px (from 28 Sep 2026)

| # | Feature | Status |
|---|---|---|
| 6.1 | Depth pass, brand content only from the brain and tables: thresholds (single-pack share, minimum saving, depth cut, parity gap, approval days, snooze days) and the market name come from `settings` in the overview, not from text in screen.js. The positioning map leaves our point off when discount in ads is unavailable instead of drawing it at 0. A test fails if screen.js carries a percent, a market or a `|| 0` | done |

## Contract asks

- A shared `registry` table in the data layer that screens can append proposed rows to (events.md). Local fallback: 04 writes proposed rows to `app/screens/04-offers-pricing/outbox/registry.<brand>.json` (git-ignored); the experiments screen can read them from there until the table exists.

- Move the experiment registry seed into the data layer as the shared `registry` table (events.md). Local fallback: 04 reads `screens/25-experiments/fixtures/registry.json` as data, read-only, and prefers the table once it exists.

### Web pass (28 Sep 2026, public pages only)

Intelligems (threshold and price tests scored by profit per visitor), Rebuy (tiered cart progress bar), Kaching and Fast Bundle (quantity breaks), Prisync (SmartPrice floor and ceiling, MAP monitoring), Klaviyo (welcome depth by segment, no discount for past buyers), Yotpo (loyalty earn rate), Eightx (threshold math), Common Thread (BFCM depth by margin and stock, gifts with high perceived value), Metricuno (blended discount rate). Taken into rules: 2.2, 2.3, 2.4, 2.5, 2.7, 2.8, 2.9. Left for later: bundle pairs and upsell take rate (need order lines), loyalty earn rate against margin (no loyalty data), stock in promo depth (inventory rows). Idea bank ids used: OFF-044, OFF-045, SET-081, MULTI-154, BRD-036.

### Round 2 note for Kevin (28 Sep 2026)

1. What a founder can do now: see 18 ranked moves, then a calendar that says which can start on 4 Oct side by side and which must wait for a shared surface or the peak.
2. New money finding: landed cost rose 8 percent in April on 23 packs and prices did not follow; a price test per pack restores margin dollars and states the conversion it can lose.
3. Market position: we sell at $12.90 an item against a $25 set median and lead with 20 percent off, while pricier rivals sell guarantees; 3 proof-led ad briefs are drafted. 11 marketplace listings undercut the site.
4. Black Friday is now a tier table by line (20, 15, 10 percent or a gift) that keeps the red line; the first-order gift is a named item; the cart gets a gift tier at $90.
5. Discipline: 91 percent of discount dollars go out on ordinary days through the code; a discount policy is drafted from the brand's own history. Past buyers get a no-discount flow before the day 53 drop.
6. Next (round 3): the brain `plans` write-back when a move is approved, BFCM stock depth once inventory connects, bundle pairs and upsell take rate from order lines, a second brand test fixture.

## Room jobs

| Job | Question | Capability | Status |
|---|---|---|---|
| Design the offer's full value proposition | does this offer beat the buyer's biggest objection, priced and proven | LIFE-C36 | round 0: guarantee table, OFFER-R04 |
| Model offer and discount economics before launch | what does this discount cost in margin, and does it cross my red line | MONEY-C05 | round 0: threshold break-even, OFFER-R01; margin waits on COGS join |
| Govern discount policy and price integrity | are we training buyers to wait for a discount | LIFE-C38 | round 0: discount share, BFCM depth, creep rule |
| Design bundles and quantity-ladder pricing | does every tier have a reason to exist, is the middle one winning | LIFE-C39 | round 0: pack ladder table |
| Design gift-with-purchase offers | is the gift lifting the tier we want | LIFE-C40 | todo |
| Place upsell and cross-sell offers | which placements convert, and do they hurt margin | LIFE-C41 | todo |
| Design the guarantee and risk-reversal offer | does the guarantee remove risk without breaking margin | LIFE-C42 | todo (claims not tagged) |
| Design the subscription offer and cancel flow | is the reason to subscribe stronger than a flat discount | LIFE-C43 | parked (non-subscription first) |
| Design and model the pop-up first-order offer | does the pop-up offer pay for itself | LIFE-C02 | todo |
| Design referral and partner offers | is referral cheaper than paid media | LIFE-C45 | todo |
| Design payment terms, BNPL and trial pricing | is trial-to-full matching the model | LIFE-C46 | todo |
| Run the offer testing framework | what to test next, is any test untrustworthy | LIFE-C47 | todo |
| Track competitor and MAP pricing | did a competitor or reseller move price | BRN-C11, PROD-C46 | todo |
| Run the gift card program | outstanding gift card liability and redemption | LIFE-C58 | todo |

## Candidates from the room spec (pick 10 per round)

### Questions this screen should answer

- does this offer actually beat the buyer's single biggest objection, priced and proven  (LIFE-C36)
- what does this discount actually cost in margin, and does it cross my red line  (MONEY-C05)
- are we training buyers to wait for a discount  (LIFE-C38)
- does every tier in this ladder have a real reason to exist, and is the middle one winning  (LIFE-C39)
- is this gift lifting the tier we want, or just costing margin for no shift in behavior  (LIFE-C40)
- which placements are actually converting, and are they hurting margin anywhere  (LIFE-C41)
- does the guarantee remove real buyer risk without breaking margin if claims run high  (LIFE-C42)
- is the reason to subscribe stronger than a flat discount, and is the cancel-save offer working  (LIFE-C43)
- does the pop-up offer pay for itself once opt-ins, discount cost and ESP cost are counted  (LIFE-C02)
- is referral acquiring customers cheaper than paid media  (LIFE-C45)
- is the trial-to-full conversion rate matching what we modeled when we priced it  (LIFE-C46)
- what should be tested next, and is any test running so it can't be trusted  (LIFE-C47)
- did a named competitor or reseller just move price on us  (BRN-C11, PROD-C46, BRN-C11)
- how much outstanding gift card liability are we carrying, and is it being redeemed  (LIFE-C58)

### Metrics specified

- `margin_after_discount`: What is actually left after the discount, in dollars, not just percent off. order revenue − COGS − payment fee − discount amount, per order and rolled up per offer
- `free_shipping_threshold_breakeven`: The order value at which free shipping stops costing margin. AOV + (average shipping cost ÷ gross margin rate), recomputed from the brand's live numbers
- `discount_dependency_rate`: Share of revenue that only came in at a discount. revenue from orders with a discount code or automatic discount ÷ total revenue
- `discount_frequency_per_customer`: How often the same customer buys only when there is a discount. count of discounted orders ÷ total orders, per repeat customer
- `bundle_attach_rate`: Share of orders that take the bundle instead of a single item. bundle orders ÷ (bundle orders + single-item orders for the same product line)
- `average_selling_price_trend`: Whether the real price paid, after discounts, is rising or falling over time. total revenue ÷ total units, monthly
- `gwp_cost_share`: What the free gift costs as a share of the order it is attached to. gift COGS ÷ order revenue, for orders that received the gift
- `upsell_take_rate`: Share of eligible customers who accept an upsell or cross-sell offer. orders that included the upsell ÷ orders shown the upsell, by placement (cart, checkout, post-purchase)
- `guarantee_claim_rate`: Share of orders covered by the guarantee that actually file a claim. guarantee claims ÷ orders covered by that guarantee, in the guarantee's window
- `subscription_perk_redemption_rate`: Share of subscribers who actually use a given perk. perk redemptions ÷ active subscribers eligible for that perk
- `cancel_flow_save_rate`: Share of subscribers who accept the save offer instead of cancelling. saves ÷ (saves + completed cancellations)
- `popup_offer_net_economics`: Whether the pop-up offer pays for itself once every cost is counted. incremental revenue from pop-up-sourced first orders − (discount cost + ESP cost allocated to those contacts)
- `referral_program_cac`: Cost to acquire a customer through referral, versus paid CAC. total referral reward cost ÷ number of referred customers who placed an order
- `bnpl_trial_conversion_rate`: Share of trial or BNPL starts that convert to the full-price plan. trials converted to full price ÷ trials started
- `map_violation_count`: Number of listings selling below the agreed minimum advertised price. count of marketplace_listings rows where listed_price < map_price
- `competitor_price_index`: The brand's price versus named competitors, indexed. brand price ÷ average of named competitors' price for the matched product, per SKU family
- `gift_card_liability_outstanding`: Total value of gift cards sold but not yet redeemed. sum of issued_value − sum of redeemed_value, across active cards
- `gift_card_redemption_rate`: Share of issued gift card value that gets redeemed. redeemed value ÷ issued value, for cards past their typical redemption window
- `offer_test_backlog_status`: What is queued, running or done in the offer test backlog, and the win rate. count and status of entries in the offer test registry; win rate = tests won ÷ tests completed

### Insights specified (rules in code)

- discount creep: discount_dependency_rate rises more than 5 percentage points over the trailing 3 months → "discounted revenue went from {a}% to {b}% of sales over the last 3 months" (action LIFE-C38)
- margin red line breach: margin_after_discount for a live offer falls below the founder's stated red-line margin → "{offer} is running at {margin}% margin, below your {redline}% red line" (action MONEY-C05)
- MAP violation detected: map_violation_count > 0 for a listing in the current check → "{n} listings on {marketplace} are priced below the agreed MAP of {map_price}" (action PROD-C46)
- free shipping threshold stale: free_shipping_threshold_breakeven has not been recomputed since AOV or shipping cost moved more than 5 percent → "your free shipping threshold was set when AOV was {old}, it is now {new}" (action MONEY-C05)
- bundle cannibalizing full price: bundle_attach_rate is high (over 40 percent) while average_selling_price_trend for the product line is falling faster than the bundle's per-unit discount would explain → "the bundle is winning {pct}% of orders but per-unit price is falling faster than the bundle discount accounts for" (action LIFE-C39)
- gift cost creep with no lift: gwp_cost_share rises without a matching rise in average_selling_price_trend or bundle_attach_rate for the tier the gift was meant to lift → "the gift now costs {pct}% of order value with no lift in the tier it was meant to push" (action LIFE-C40)
- guarantee cost above plan: guarantee_claim_rate exceeds the claim-rate assumption used to price the guarantee by more than 50 percent relative → "claims are running at {actual}%, against a planned {planned}%" (action LIFE-C42)
- trial conversion miss: bnpl_trial_conversion_rate falls more than 20 percent relative below the modeled conversion used to price the trial → "trial-to-full conversion is {actual}%, against a modeled {planned}%" (action LIFE-C46)
- competitor price move: competitor_price_index moves more than 5 percent in either direction for a named competitor's matched SKU family within a week → "{competitor} moved price {pct}% on {product} this week" (action BRN-C11)
- referral beats paid CAC: referral_program_cac is less than half of blended paid CAC for the same period → "referral CAC is {referral}, less than half of paid CAC at {paid}" (action LIFE-C45)
- overlapping offer tests: two entries in the offer test_registry target the same product or segment with overlapping date ranges → "{test_a} and {test_b} are both running on {segment} at the same time, results cannot be trusted" (action LIFE-C47)
- gift card liability outpacing redemption: gift_card_liability_outstanding grows faster than gift_card_redemption_rate over 3 consecutive months → "outstanding gift card liability has grown {pct}% while redemption has not kept pace" (action LIFE-C58)
- subscription perk mismatch: subscription_perk_redemption_rate for a perk stays under 10 percent for 2 consecutive months → "only {pct}% of subscribers use the '{perk}' perk 2 months running" (action LIFE-C43)
- cancel save rate falling: cancel_flow_save_rate drops more than 10 percentage points versus its trailing 90-day average → "the cancel-flow save offer worked {old}% of the time, now {new}%" (action LIFE-C43)
- competitor policy change: a named competitor's public returns, loyalty or subscription-terms page changes materially since the last check → "{competitor} changed its {policy_type} page: {change}" (action BRN-C11)

### Visuals specified

- margin waterfall (waterfall chart): revenue down to net margin for a chosen offer or discount, step by step
- discount dependency trend (line chart): share of revenue at a discount, monthly, over the trailing 12 months
- free shipping threshold sensitivity (small interactive chart or table): break-even threshold recalculated as AOV, margin or shipping cost inputs change
- competitor price index (line chart): brand price index versus each named competitor over time
- bundle ladder funnel (funnel or bar chart): share of orders choosing each tier in the ladder, single item to largest bundle
- offer test backlog board (kanban-style list with win rate): offer tests planned, running, done, with hygiene flags
- gift card liability vs redemption (dual bar/line chart): outstanding liability and redemption rate over time

### Not in the usual tools

- The free shipping threshold is computed straight from this brand's own live AOV, margin and shipping cost, and flagged stale automatically when those inputs move
- A margin waterfall runs before an offer launches, and a founder-set red line blocks approval if it is crossed
- Discount dependency and price integrity are tracked as one running score across every offer and channel, not just a discount-usage count
- Competitor and MAP price tracking is tied directly into the brand's own offer test backlog and margin data
- Offer tests are checked for overlap (same segment, same window, two variables at once) automatically before a founder is asked to read results
- Gift card liability and redemption are shown together as a cash-flow signal, not just a balance

### Data this screen needs

- `orders`: order_id, sku, unit_count, price, discount_code, discount_amount, cogs, shipping_cost, placed_at (store order export, not yet connected)
- `product_costs`: sku, cogs, shipping_cost_avg (manual or ERP export, not yet connected)
- `discount_codes`: code, type, value, start_at, end_at, terms, conditionality (store discount export, not yet connected)
- `competitor_prices`: competitor, sku_family, price, url, captured_at (LIFE-C56 competitor price watch (agent, public web only))
- `marketplace_listings`: marketplace, sku, listed_price, map_price, checked_at (marketplace price pull, not yet connected)
- `gift_card_ledger`: card_id, issued_value, redeemed_value, issued_at, expiry_at (store gift card export, not yet connected)
- `subscription_plans`: plan_id, perks, price, cadence, redemption_log (subscription platform export (Recharge or equivalent), not yet connected)
- `guarantee_terms`: guarantee_id, coverage, length_days, cost_per_claim_estimate, planned_claim_rate (manual entry from LIFE-C42 design doc)
- `referral_program`: referrer_id, referred_id, reward_cost, order_id, referred_at (referral platform export, not yet connected)
- `bnpl_trials`: trial_id, customer_id, start_price, full_price, started_at, converted_flag, converted_at (BNPL/trial billing export, not yet connected)
- `offer_test_registry`: test_id, offer_type, hypothesis, segment, sku_scope, start, end, metric, result (LIFE-C47 offer testing framework log)

## Rounds

| Round | Features picked | Date | Notes |
|---|---|---|---|
| 0 | skeleton, 0.1 to 0.9 | 2026-09-28 | S3.9; screenshot round0.png |
| 6 | 6.1 onward: depth pass | 2026-09-28 | in progress |
| 5 | 5.1 to 5.10: stack read-back, break-even discount, profit per visitor, pack label, installments, loyalty calibration, line match, code-won cohorts, order bunches | 2026-09-28 | screenshot round5.png |
| 4 | 4.1 to 4.10: save to the brain, offer records, bundle pairs, red line gate, approved first, launched read, upsell connect, brief pack, stale inputs | 2026-09-28 | screenshot round4.png |
| 3 | 3.1 to 3.10: registry, referral, loyalty, window creep, subscription note, depth rules, plug and play, priors, decisions | 2026-09-28 | screenshot round3.png |
| 2 | 2.1 to 2.10: position, parity, discipline, gift pick, cart ladder, test calendar, depth by line, second order, cost against price, desk tabs | 2026-09-28 | screenshot round2.png |
| 1 | 1.1 plan first, 1.2 objection to offer map, 1.3 free shipping line, 1.4 pack ladder, 1.5 first-order offer, 1.6 margin waterfall, 1.7 promo calendar, 1.8 gifting and holiday, 1.9 guarantee as an offer, 1.10 rank complete | 2026-09-28 | manager session; screenshot round1.png (updated as the round lands) |


## Round 1 candidates (ranked 28 Sep 2026 by the lead session)

Ranked by revenue impact, usefulness to a founder deciding alone, and buildable on the simulated data. Kevin picked the 5 screens; the top 5 here are recommended for round 1. One feature per commit, this table updated in the same commit.

| # | Feature | Capability | Why buildable now | Impact |
|---|---|---|---|---|
| 1.1 * | Margin waterfall per offer, revenue down to net, with a founder red line that blocks approval | MONEY-C05 | orders, discount codes and finance inputs exist | high |
| 1.2 * | Free shipping threshold sensitivity: break-even recomputed live from AOV, margin and shipping cost, with the stale flag | MONEY-C05 | already a finding; make the inputs adjustable | high |
| 1.3 * | Discount dependency trend over 12 months with the discount-creep rule | LIFE-C38 | discounted revenue share by month from orders | high |
| 1.4 * | Bundle ladder funnel: share of orders per pack size with the cannibalization rule | LIFE-C39 | pack sizes in products and order_lines | high |
| 1.5 * | Competitor price index from Amazon listings and Ad Library offers, plus MAP violation count | BRN-C11 | marketplaces records and learnings; signals only | medium |
| 1.6 | Offer test backlog board wired to the experiment registry with the overlap check | LIFE-C47 | registry from screen 25 | medium |
| 1.7 | Guarantee claim rate against the modelled 2 percent replacement rate | LIFE-C42 | reversed_orders replacements versus the brain's return_share_model | medium |
| 1.8 | Gift card liability against redemption, on a fixture until the ledger connects | LIFE-C58 | gift cards exist in products; the ledger does not | low |
| 1.9 | Upsell take rate by placement | LIFE-C41 | unavailable until the upsell app connects (Rebuy is in the stack) | low |
| 1.10 | Referral CAC against paid CAC | LIFE-C45 | unavailable until a referral platform connects | low |

\* recommended for round 1
