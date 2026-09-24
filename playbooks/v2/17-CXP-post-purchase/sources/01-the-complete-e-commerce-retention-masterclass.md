# The Complete E-Commerce Retention Masterclass

source_id: 1b6kx6AoloHFp2Y1pjdNpPBuaWJGeCSa3  |  folder: /17-CXP-post-purchase  |  cards: 28  |  words: 14,381  |  type: transcript (YouTube masterclass, 2 presenters, auto-generated captions)

credibility: Two presenters, switching back and forth. "Nathan" (no surname given in the transcript) frames himself as running a performance-marketing / growth agency: he pitches a free audit to e-commerce brands doing at least $5M a year and says he is "always hiring" performance marketers with 2+ years on Meta and Google ads. He covers finance, unit economics and paid media's role in retention. Angus Cowan runs an agency he calls "Marketing Emails" (heard by the transcriber as "Eclavio" once), based in Australia, described as an email/SMS specialist and, in his own words, running "the biggest email marketing agency in Australia" (unverified self-description). He covers Klaviyo segmentation, flow structure and RFM. Per the source's own ingestion header (see "scope note" below), Angus's section is roughly 70% of the video's runtime. Evidence offered: 2 named case examples (a "9-figure activewear retailer" 2025 Black Friday reach fix; a "9-figure subs retailer" mentioned only as a portfolio illustration for the 80/20 campaign rule), a run of "our clients"/"brands we work with" generalizations (e.g. "maybe 60% of the brands that we work with"), one vague reference to unnamed third-party "studies" on campaign incrementality, and otherwise stated personal experience, opinion and rules of thumb. No citations, no controlled tests, no sample sizes. The video ends with a paid-audit pitch and a hiring link, so read it as agency marketing content: useful operating heuristics from a real client base, not peer-reviewed research.

date signals: References a "9-figure activewear retailer" case worked "in 2025" and its "Black Friday... end of 2025" result, so recording is late 2025 or in 2026. This is an auto-generated transcript with clear ASR (speech-to-text) errors that should not be mistaken for content: "Klaviyo" is rendered "Clavio" / "Eclavio", "ROAS" is rendered "rollass" / "rorowaz", "CAC target" is rendered "calf target", "Angus Cowan" is rendered "Angus Cow". ("F stands for function" is a real quote, not a transcription error.) No specific platform UI version is named beyond "the Klaviyo marketing analytics tab" for RFM, so `[verify UI]` applies to exactly where that feature lives today.

scope note: The source's own ingestion header (a folder-routing block embedded at the top of the raw source text, written by whoever scoped this document for carding) classifies the document primarily under 06-MEA (measurement and economics): "why: Deconstructs lifetime value into a time-constrained profit metric (LTGP)... provides the specific margin math required to back-propagate an acquisition CAC target." That header explicitly instructs: "Skip. The entire middle segment of the video (approx. 70%) featuring Angus Cowan discussing Klaviyo email flows, RFM analysis, campaign reach vs. personalization, and post-purchase email structures. That content belongs entirely in 14-EML." Despite that instruction, all 28 cards for this source_id live under /17-CXP-post-purchase, and roughly 20 of the 28 actually cover Angus Cowan's Klaviyo flow-structure, segmentation, RFM, campaign-cadence and VIP material — the part the header says belongs in 14-EML. Only about 8 cards cover the Nathan / LTGP-CAC economics material the header calls this source's real subject. Pass 2 authors for 17-CXP-post-purchase should expect heavy overlap with whatever 14-EML holds on lifecycle flows and segmentation, and should check whether 14-EML also cards this same source_id.

## 1. What this source is for

It gives an operator two things. First, the finance side of retention: how to define lifetime value as a time-boxed profit number (LTGP, not raw "lifetime" revenue), how to turn a chosen LTGP window into a CAC ceiling, how to bound CAC itself with CPC and conversion rate, and how CPG/subscription brands justify and track a deliberate Day-0 loss (CAC payback period). Second, the Klaviyo/lifecycle side: how to structure flows and campaigns around 3 customer-journey stages (F1 acquisition, F2 first-to-second order, F3 top-20%-customer loyalty) so a single biggest drop-off can be found and fixed, how to segment for reach versus personalization, RFM-based lifecycle segmentation, VIP treatment, and paid media's narrow, situational role in serving existing customers. It opens with a framing stat — "only 20% of customers buy a second time from 80% of brands" — and a top-down "retention hierarchy" (product, portfolio, acquisition quality, CX, then owned media) that the whole video is organized around. It is thin on how: it gives no step-by-step Klaviyo flow build (the presenter explicitly defers "the nitty-gritty of how many emails, what triggers" to his own channel, `[web check: presenter's referenced channel for the full flow breakdown]`), and it does not define ROAS, contribution margin or general LTV formulas beyond LTGP itself.

## 2. Principles

### 2.1 Lifetime value as a time-boxed profit number (LTGP)

1. **Use lifetime gross profit (LTGP), not lifetime value (LTV) revenue.** In software, LTV and gross profit are nearly the same number because overhead is low; in e-commerce, revenue is "almost meaningless" across brands because unit economics differ, so always translate to gross-profit dollars. [2d30561e1938]
2. **LTV must carry a time constraint.** An unconstrained "lifetime" number (e.g. 70- or 80-year) is unmeasurable and irrelevant to cash needs; state it as "30-day LTGP", "90-day LTGP", "180-day LTGP" and build a cohort curve at 30/60/90/180/365 days. A customer might be worth $60 gross profit on day 0 and $100 by day 90 — track that growth path, not a single lifetime figure. [2d30561e1938] [b4ff45d77f83]
3. **Calculate LTGP from real order-level data, never AOV × assumed margin.** Example mistake: "my new customer AOV is about $110, my gross margin is around 80%, so I'll just times this by 80%" — this always gives an off number because AOV and margin move a lot per cohort, especially in discount periods (margin compression). Pull real order and refund line items (e.g. from Shopify) at least monthly. [2d30561e1938]
4. **Keep refunds out of CAC, but always inside LTGP.** New-customer counts used for CAC are pre-refund (100 acquired, 20 refund in a fashion example, so effectively 80 paid); the source explicitly recommends against adjusting CAC for this because CAC/platform efficiency has nothing to do with product-quality-driven refund rates — correcting CAC for refunds would cause you to blame the ad platform for a product problem. Instead, subtract refund rate on the LTGP side (this happens naturally once you extend to a 30-day-plus order-level view, where refund line items show up). If your revenue figure is already net of refunds, do not subtract refunds a second time. [2d30561e1938]

### 2.2 CAC targets and bounds

5. **CAC = total media spend across all channels ÷ new customers acquired in that period.** Pick a measurement period that fits your scale: an "enormous 9-10 figure retailer" should look at daily or hourly CAC; a 6-8 figure brand gets more useful signal zooming out to weekly or monthly trends.
6. **Set a CAC target by dividing chosen LTGP by a target LTGP:CAC ratio.** Bands: below 1 = losing money (workable only if deliberately running an aggressive, capital-funded growth strategy); 1-2 = inefficient but scalable with strong working capital or an exit-focused strategy; 2-3 = the target scaling band ("this is where we're always pushing clients to be scaling up budgets"); 3+ = leaving money on the table (arbitrage that "probably won't last too long"). [3861489d8286]
7. **Choose the LTGP window by growth appetite and capital, not by habit.** Default recommendation: 30-day LTGP for most stores, especially bootstrapped/profit-first ones and stores under roughly $15-20M/year; 90-day (or further) for CPG, supplements or other high-repeat categories, or for capital-rich/funded brands willing to run at a short-term loss. Loan-funded aggressive-growth models require sophisticated financial modelling that accounts for interest payments, and running that model well is "incredibly risky" for most brands under roughly $15-20M annual revenue. [5a300a3bc804]
8. **Model the incremental-volume trade-off before extending the window.** If raising the CAC ceiling by (e.g.) $10 buys meaningfully more customers (source example: 30-40% more), extending the window (e.g. 30-day to 90-day target) can grow the business materially and is worth doing if cash allows; if it barely moves volume, stay conservative and profitable on first purchase instead. Going colder always raises CAC (diminishing returns), but "diminishing returns are still returns" as long as the incremental volume is real. [5a300a3bc804] [3861489d8286]
9. **Bound CAC with CPC ÷ conversion rate, as a scenario range, not a promise.** This gives a best-case floor and a realistic case; the gap between them is the size of the paid-media opportunity. If the floor is already close to current CAC, further paid-efficiency gains are limited and the lever to pull is LTGP instead. CPC itself is called "a relatively vanity metric" that only correlates with performance at the extremes (very high CPC is bad, very low CPC often means terrible traffic). [f1d832540bbc]
10. **Decide which half of the LTGP:CAC ratio has real headroom before investing.** CAC has a hard floor (traffic quality degrades past a point); LTGP has a practical ceiling that shifts with offer, bundle and subscription work. Inexperienced operators typically underestimate how low CAC can realistically go and underestimate how high LTGP can be pushed through better front-end offers or retention. Re-run the comparison at least quarterly. [2e9e88a22775]
11. **For CPG/subscription brands taking a Day-0 loss, track a CAC payback period.** Accept the deficit explicitly (e.g. $50 CAC vs $45 Day-0 gross profit = -$5), then track the date cumulative gross profit from the cohort crosses that deficit into profit. Drive the payback date earlier with retention levers: subscription depth, replenishment cadence, second/third purchase rate. Put this on the finance dashboard as a standing KPI alongside contribution margin, and model how much working capital you can tie up while cohorts sit in the red before scaling spend. Requires a category with a genuinely high repeat/replenishment rate; it does not fit one-off or durable-goods purchases. [d1160b9862c5]
12. **Raise the LTGP ceiling through offer and subscription design, not just retention messaging.** Map the current 90/365-day LTGP ceiling including subscription attach; test bundles, starter kits and multi-month packs that raise AOV/starting gross profit without more paid spend; test front-end offer structures (one-time vs. subscribe-and-save, trial vs. full-size) and judge by cohort LTGP, not first-order AOV alone; treat subscription cancellation/retention as a leading LTV indicator; re-run the LTGP:CAC ratio after each change to confirm the extra paid headroom is real. [9f7c64c08aab]

### 2.3 Diagnosing retention before touching owned media

13. **Only about 20% of customers buy a second time from 80% of brands** — the source's framing stat for why this masterclass exists, and the diagnostic anchor for weak second-purchase conversion. Treat it as an observed pattern from the source's client base, not a universal benchmark; repeat rates differ widely by category (CPG vs. fashion vs. one-off products). [42e1ab9189e1]
14. **Work the retention hierarchy top-down before spending on email/SMS.** Order: 1) product quality, 2) product portfolio (natural cross-sell, upsell, replenishment — is there a reason to come back?), 3) acquisition quality, 4) customer experience across every touchpoint, 5) owned media (email, SMS, direct mail, WhatsApp). Owned media is described as "the amplifier" — it can only exploit a constraint once the first four are healthy; it "can't outmarket a flawed retention system." [290bef9daa56]
15. **Audit product quality with real customer evidence, not founder opinion.** Use surveys, NPS scores and verbatim feedback; "don't be biased... use real data." [290bef9daa56]
16. **Acquisition quality predicts repeat behaviour.** Low-AOV TikTok Shop buyers and customers acquired during 40-50% Black Friday-style flash sales repeat far less than a customer who spent $200 on their first order — "the behavior of a customer when they first shop with your business is a massive indicator" of long-term retention. [290bef9daa56]
17. **Customer experience includes how problems are handled, not just whether they happen.** Shipping updates, communication and support quality matter; a problem handled well can be an indicator a customer comes back, contrary to the assumption that any problem drives customers away. [290bef9daa56]
18. **Diagnose weak second-purchase conversion as a foundations problem before blaming email copy.** Check the hierarchy in order (product → portfolio → acquisition → CX) before assuming the fix is more flows; also check whether the store is misreading vanity signals (attribution dashboards, the Shopify returning-customer % metric — see 2.5) as proof retention is fine. [42e1ab9189e1]

### 2.4 Measuring retention correctly

19. **Reject "% of returning customers" as a retention/LTV KPI.** Shopify's metric = returning-customer orders ÷ total orders in the period, not repeat rate. It is driven by two things that have nothing to do with retention quality: business age (older stores naturally trend the ratio up as their existing base grows) and acquisition strength (acquiring fewer new customers makes the ratio look better) — so a brand can be incentivized to acquire less. Called "a terrible metric for indexing the performance of LTV." Its only legitimate use is slicing sale-period analytics (new vs. existing resonance), not judging LTV. [9444eb58b437]
20. **Balance attribution and profitability metrics; avoid both extremes.** Klaviyo/platform attribution (account, campaign and flow attributed revenue, revenue per recipient) is a north-star indicator only — take it "with a grain of salt." Outside studies the source cites suggest roughly 70-80% of campaign revenue may be incremental for some accounts, but "it really depends on your brand"; bigger brands can run their own incrementality tests. Chasing attribution alone optimizes for looking good in-platform; ignoring incremental repeat-revenue work in favour of only long-term LTV thinking means today's numbers never improve. Use attribution as the north star and profitability metrics (below) as the tool that actually finds the constraint. [2df157249026]
21. **Core profitability metrics to track: LTGP adjusted for 90 and 365 days (mapped across 30/60/90/180/365-day cohorts using real order-level data with refunds included), plus revenue from the top 20% of customers.** The top-20% figure indicates long-term loyalty and how well the top segment is being leveraged. [2df157249026] [b4ff45d77f83]
22. **Attribution submetrics worth tracking day-to-day:** campaign revenue (to find incremental gains from better segmentation/campaign styles/send timing), pop-up conversion (not opt-in rate — see 2.6), flow revenue used to find weaknesses/gaps in the flow stack (not as an aggregate number), and year-on-year Klaviyo growth relative to overall business growth. [2df157249026]
23. **Attribution target as an indicator only:** "you should be getting 30-50% of your revenue from email marketing" is described as a soft indicator of reach/engagement/flow coverage/cadence, explicitly "not a hard science." [2df157249026]

### 2.5 Structuring the customer journey (F1/F2/F3)

24. **Map every flow and the whole account into 3 functions: F1 = acquisition, F2 = first-to-second order conversion, F3 = revenue from the top 20% of customers, adjusted for gross profit.** ("F stands for function," per the source, not "phase.") F2 correlates with 90-day LTGP; F3 correlates with 365-day LTGP; F1 is the gate — none of the rest matters if you can't acquire the customer. [3c84840ee4fe]
25. **Split every flow's first branch by customer journey stage — new, returning, loyal/subscription — not by product.** New customers get more aggressive messaging tackling trust and price and introducing the brand; returning customers skip the introduction and go straight to what they need; loyal/subscription customers get the least aggressive messaging, focused on protecting and nurturing the relationship, ideally with no incentive at all. [3c84840ee4fe]
26. **Reject the two common flow-structure failure patterns.** Pattern 1: one linear trigger→email→email sequence for every entrant regardless of journey stage (a first-time browser gets the same messaging as a 5-time VIP). Pattern 2: splitting a flow first by arbitrary product attributes (who left denim vs. a t-shirt in cart) before splitting by journey stage — this can be tested later as a secondary split, but it is lower leverage and, done first, makes it impossible to isolate where the real constraint sits. [3c84840ee4fe]
27. **Use the F1/F2/F3 structure to walk directly to your constraint.** If your data shows the constraint is F2 (first-to-second order), go to the new→returning branch across every flow and diagnose there, rather than reacting with generic moves like "build another win-back flow" or "send more discount campaigns." [3c84840ee4fe]
28. **Flows matter more than campaigns for the customer journey because they run 24/7 and are triggered on distinct behaviour**, making them more incremental than campaign blasts (which often go to already-highly-engaged users, a common source of attribution overstatement). The campaign-revenue-vs-flow-revenue split itself is called month- and business-dependent and not worth optimizing as a fixed ratio. [3c84840ee4fe]

### 2.6 Segmentation, campaigns and reach

29. **Send elite content to the most people possible most of the time; reserve narrow segments for specific goals — roughly an 80/20 split.** 80% of the time, focus on reach: top/middle-of-funnel content (education, entertainment, social proof, reviews) sent to the engaged base. 20% of the time, execute specific-goal narrow segments (excess stock on a brand, a supplier-led national sale, a product-specific push) with one clear business reason. [097d09066f7a] [3121e4d083d4]
30. **Reject hyperpersonalization as the default campaign strategy**, despite it being "a massive narrative in the industry right now." The source's stated reasoning: the labour cost of building super-niche one-to-one campaigns rarely returns enough upside, you lose the ability to learn what "elite content" even looks like because everything is fragmented, and repeat-customer revenue arrives in waves tied to big moments — those moments only cash in if a large, engaged audience was built consistently beforehand. [097d09066f7a]
31. **Route personalization to flows, not campaigns.** Flows are behaviour-triggered (purchase, abandoned checkout, browse) with real data to act on, so personalize there; within flows, split by journey stage first, then layer product/collection splits for finer personalization. Campaigns are for reach, moments and messaging. Reasoning: only an estimated ~3% of an email list is "ready to buy today" — over-indexing campaigns on personalization to that 3% ignores the other ~97% who aren't ready but may still engage with broad, reach-oriented content. [3121e4d083d4]
32. **Define and grow an "engaged audience" segment as the primary sendable base.** Engaged = opened or clicked an email OR took an on-site action (added to cart, started checkout, placed an order) within a lookback window you set for your lifecycle. Source's own example windows: roughly 180 days for opens/clicks, roughly 220 days for on-site actions, roughly 280 days for placed orders — stated explicitly as source-specific heuristics to adapt, not fixed rules. Target at least 50% of the full list falling into the engaged definition by default, and track that share growing over time as the core retention KPI (not per-send opens/clicks in isolation). [83592aa3301a] [c5da5743237]
33. **Rebuild reach among dormant/unengaged subscribers gradually, not all at once.** Split the unengaged remainder into equal random samples (source used 10 samples); add one sample into the engaged send at a time with your best content; measure how many convert from unengaged to engaged (source's own math implies roughly 18-20% of the added sample opened in its example, described loosely as "20 or 30%"); fold newly engaged people into the permanent engaged segment; repeat over several months (source says 6-9 months); save the biggest dormant reactivation push for a marketing-calendar peak (e.g. Black Friday) when a strong offer is most likely to convert them. [83592aa3301a] [c5da5743237]
34. **Judge pop-up performance by pop-up conversion, AOV and gross profit of signed-up customers — not opt-in rate.** A 5% or 10% opt-in target "because someone told me" says nothing about the value of that audience; compare it against other acquisition sources before treating a high-volume, low-value pop-up cohort as a win. [4789763c9e99]
35. **Prioritize retention A/B tests by the identified F1/F2/F3 constraint, in this order: (1) structure and timing — flow architecture, split order, campaign cadence, segmentation, time of day, flow delays; (2) offers — incentive size, structure, conditions, timing relative to journey stage; (3) messaging — copy, angles, headlines, creative.** Testing only subject lines, click-through rate and time delays is framed as "being an email marketer" rather than a retention marketer — those tests are still legitimate executor-level work, just not the top-level testing agenda once a constraint is known. Keep one person on high-level retention strategy/profitability alongside executors handling creative and segmentation; both roles are needed. [ebe1e2f78000]
36. **Repeat-customer revenue arrives in peaks and troughs tied to the marketing calendar** (sales, new products, restocks, general marketing moments), unlike new-customer revenue which should scale closer to linear. Peaks only convert well if a large, engaged audience was built consistently in the quiet periods; plan the calendar in two layers — always-on engagement content for baseline, event-based campaigns for peaks. Judge success by year-on-year channel growth relative to the business, not any single send. [f6f96b40442]

### 2.7 Lifecycle cohorts and RFM

37. **Map subscription-business customers into 4 lifecycle cohorts with distinct goals:** never purchased → get the first sale, ideally straight onto subscription; purchased but not subscribed → upsell to subscription or the next purchase; active subscriber → retain/protect the relationship (least aggressive messaging, no incentive); cancelled subscriber → reactivate. [4d8506a387fd]
38. **For non-subscription brands, substitute RFM or simple loyalty tiers** ($500+, $1,000+, $3,000+ spend tiers) to get the same clarity of "who is this customer and what should they receive." [4d8506a387fd]
39. **RFM scores subscribers on Recency, Frequency and Monetary value, all relative to your own subscriber base**, not an external benchmark. Segments: Champions (top percentiles across all three), Loyal (just below Champions), Recent (recent purchase, not yet frequent/high-spend), At Risk (metrics slowing versus their own normal cadence — e.g. usually every 3 months, now 3.5 months since last purchase), Needs Attention (treated the same as At Risk in practice: get in front of them, especially if they were previously a Champion). [98fc8eced08a]
40. **Use RFM-driven triggers instead of arbitrary fixed-day win-back triggers.** A generic "anyone who hasn't purchased in 120 days" flow will hit a customer whose normal cycle is 200 days far too early with an unnecessary discount; RFM lets the win-back fire off the customer's own actual purchasing pattern. Apply RFM segments across win-back, replenishment, post-purchase and abandoned cart/checkout flows, and in the ~20%-of-time specific-goal campaigns. A useful segment example: "recent but not yet Loyal/Champion" customers as a first-to-second-order conversion target. RFM is available in Klaviyo's marketing analytics tab (and reportedly in other platforms too) `[verify UI]`. [98fc8eced08a]

### 2.8 VIPs

41. **Define VIPs by revenue and profit concentration: roughly 50%+ of revenue and roughly 80% of profit**, because these customers return more often, buy more frequently and rely less on discounts. Validate this split against your own data before building programs around it — it is the source's stated pattern, not a universal number. [3de8a595a9bb]
42. **Only invest in VIP-specific programming if VIP revenue is your actual constraint.** Most e-commerce brands under roughly $10-20M/year have first-to-second order conversion as their real constraint, not VIP revenue; above that range, VIP programs become higher leverage. [3de8a595a9bb]
43. **Reward VIPs with exclusivity, not broad discounts or generic-list treatment:** exclusive products, private sales, early access, offline experiences/community/events, and loyalty-perk reminders (since VIPs may not track their own accrued perks). Build dedicated VIP branches into flows (not the same path as everyone else) and use the 20%-of-time specific-goal campaign slot for VIP-focused sends when VIP revenue is the actual goal. [39c55eb82e67] [3de8a595a9bb]

### 2.9 Paid media's role in retention and its links back to acquisition

44. **Paid ads are primarily an acquisition tool; the default is little to no spend on existing customers.** The source states it previously held an even harder line ("you should spend nothing on existing customers") and now treats that as having been wrong in one specific case: fashion/frequent-drop brands, where email/SMS alone can't reliably surface every new arrival to the whole existing base (missed emails, unread emails), so dedicated existing-customer paid spend to surface new arrivals and current campaign shoots is justified there. [675be3b57a10]
45. **Set a much tighter efficiency target for existing-customer campaigns than for new-customer acquisition** — source example: if new-customer CPA target is $40, target $20 or lower for existing customers, because a warm audience should convert far more cheaply; hitting the same CPA on existing customers as new means you're overspending on existing, or the ads themselves are poor. [675be3b57a10]
46. **Existing-customer ad spend hits diminishing returns fast; measure the marginal cost, not just conversion volume.** Continuing to spend more into a small existing base doesn't force more purchases. Pull back spend while conversion volume holds, and reallocate the savings to acquisition. [675be3b57a10]
47. **Budget existing-customer paid spend as a dollar amount, not a percentage of total media spend:** (monthly send frequency, source suggests 4-7×) × (number of existing customers) × (CPM) ÷ 1,000. [675be3b57a10]
48. **Treat discount-driven acquisition as a hypothesis to test per brand, not a default strategy.** During discounting (Black Friday, EOFY, any activation), front-end metrics look better (ROAS, efficiency, new-customer volume up) because you've opened the funnel to a wider, more price-motivated demographic — but that demographic often doesn't repeat-buy once prices return to normal. The source generalizes that roughly 60% of the brands it works with see substantially worse LTV/repeat rate from discount-acquired cohorts, but explicitly notes some 9-figure retailers show no such penalty — pull your own cohort numbers by discount code before deciding. [34373cddcf01]
49. **Collect zero-party data (distinct from first-party data) to improve acquisition targeting, not just email personalization.** First-party = email, phone, name. Zero-party = what the customer tells you about themselves (weekend habits, the problem they're solving, what they like about the brand), often via post-purchase surveys. Analyze the top 20% of customers (typically driving ~80% of revenue) for shared persona, resonant angle and purchased offer, then overallocate paid spend toward that pattern; analyze the bottom 20% the same way — often they came in on a mismatched angle (source example: a skin-health supplement acquired on an "energy" angle) that produces returns, refunds and no repeat purchase, sometimes only surfacing through customer support feedback rather than analytics, even while the front-end ROAS looked strong ("a five ROAS"). Exclude or reduce spend on angles shown to attract mismatched, low-quality customers even if their front-end numbers look good. [e74d0b65f2db]

## 3. Procedures

### 3.1 Calculate Day-0 (and cohort) LTGP
1. Take new-customer AOV (NC AOV) as the revenue base. [2d30561e1938]
2. Subtract cost of goods sold (COGS). [2d30561e1938]
3. Subtract cost of delivery: shipping and fulfillment, plus 3PL/handling/pick-and-pack costs. [2d30561e1938]
4. Subtract transaction fees. [2d30561e1938]
5. Subtract refund rate on orders (do not skip this and do not also subtract it from CAC — see 3.2 note). If working from real order-level data, this shows up automatically as refund line items once the window extends past a few weeks. [2d30561e1938]
6. Repeat the calculation at 30, 60, 90, 180 and 365 days per acquisition cohort, using real order/refund data (Shopify or equivalent), not AOV × assumed margin. Refresh at least monthly since AOV and margin move, especially around discount periods. [2d30561e1938] [b4ff45d77f83]

### 3.2 Calculate CAC and keep it clean of refunds
1. Sum total media spend across all channels for the period. 
2. Divide by the count of new customers acquired in that same period (this count is pre-refund).
3. Choose a period that fits your scale: daily/hourly for 9-10 figure retailers; weekly/monthly trend view for 6-8 figure brands.
4. Do not net out refunded customers from the new-customer count to "fix" CAC — the source explicitly warns this corrupts the paid-media efficiency signal (you'd blame the ad platform for a product-quality problem). Route refund impact into LTGP instead (3.1, step 5). [2d30561e1938]

### 3.3 Set a CAC target from LTGP and a target ratio
1. Choose the LTGP window to manage against (30-day is the default; 90-day for CPG/supplements/high-repeat categories or capital-rich brands — see 2.2 principle 7). [3861489d8286] [5a300a3bc804]
2. Pick a target LTGP:CAC ratio band: <1 (losing money, aggressive-growth only), 1-2 (inefficient but workable with strong working capital), 2-3 (target scaling band), 3+ (leaving money on the table). [3861489d8286]
3. Divide chosen LTGP by the target ratio to get the CAC target. Worked examples from the source: $80 30-day LTGP ÷ 2 = $40 CAC target; $100 90-day LTGP ÷ 2 = $50 CAC target (extending the window from 30 to 90 days raised the CAC ceiling by 25% in this example). [3861489d8286]
4. Before committing to a higher CAC ceiling, forecast the incremental new-customer volume it would unlock (plot new customers acquired against CAC ceiling); if the extra volume is meaningful (source example: 30-40% more customers), the higher ceiling is worth funding; if it's marginal, stay conservative. [3861489d8286] [5a300a3bc804]

### 3.4 Bound CAC with CPC and conversion rate
1. Set an optimistic scenario: lowest realistic CPC ÷ highest realistic conversion rate. Source worked example: $0.70 ÷ 3% = about $23.33 CAC. [f1d832540bbc]
2. Set the realistic case using actual current performance. Source worked example: $1.00 CPC ÷ 2% conversion = $50 CAC. [f1d832540bbc]
3. Compare the floor to the realistic case: a wide gap means there's real room to improve paid efficiency; a narrow gap means paid is close to its floor and the lever to pull is LTGP instead (3.6, 3.7 below). [f1d832540bbc] [2e9e88a22775]
4. Use consistent attribution and customer definitions (e.g. click-to-new-customer conversion, not overall purchase conversion including returning customers, which would give cost-per-purchase rather than CAC). [f1d832540bbc]

### 3.5 Track CAC payback for a Day-0-loss/subscription brand
1. Confirm the category has real replenishment/subscription depth; this does not apply to one-off or durable-goods purchases. [d1160b9862c5]
2. Compute the Day-0 deficit: CAC minus Day-0 gross profit (source example: $50 CAC − $45 gross profit = -$5). [d1160b9862c5]
3. Track cumulative gross profit for the cohort over time (subscription renewals, replenishment orders). [d1160b9862c5]
4. Mark the date cumulative profit crosses the deficit back to zero — that is the CAC payback period. Put it on the finance dashboard alongside contribution margin. [d1160b9862c5]
5. Before scaling spend on this model, model how much working capital you can afford tied up while cohorts are still in the red. [d1160b9862c5]

### 3.6 Choose which side of the LTGP:CAC ratio to invest in
1. Estimate the CAC floor (3.4). [2e9e88a22775]
2. Estimate the LTGP ceiling using available levers: bundle restructuring, front-end offer tests, subscription strategy, retention programs within a 90-365 day window (3.7). [2e9e88a22775] [9f7c64c08aab]
3. Compare real headroom on each side; fund the side with more of it. [2e9e88a22775]
4. Revisit at least quarterly since both floors and ceilings shift as creative, media buying, offers and retention improve. [2e9e88a22775]

### 3.7 Raise the LTGP ceiling through offers and subscriptions
1. Map the current 90- and 365-day LTGP ceiling, including subscription attach rate. [9f7c64c08aab]
2. Test bundles, starter kits or multi-month packs that raise AOV/starting gross profit without more paid spend. [9f7c64c08aab]
3. Test front-end offer structures (one-time vs. subscribe-and-save; trial vs. full-size) and measure cohort LTGP outcomes, not first-order AOV alone. [9f7c64c08aab]
4. Treat subscription cancellation and retention events as leading LTV indicators. [9f7c64c08aab]
5. Re-run the LTGP:CAC ratio (3.6) after each change to confirm the paid-media headroom is real. [9f7c64c08aab]

### 3.8 Diagnose the retention hierarchy before building Klaviyo/email fixes
1. Audit product quality using surveys, NPS and verbatim customer feedback, not founder opinion. [290bef9daa56]
2. Check the product portfolio for a natural reason to return: cross-sell, upsell, replenishment; if absent, consider a new product/collection/subscription rather than more messaging. [290bef9daa56]
3. Check acquisition quality: identify low-AOV or heavy-discount acquisition channels correlated with poor repeat behaviour. [290bef9daa56]
4. Review the full customer experience: on-site/shopping experience, post-purchase communication, shipping updates, support quality and how problems are resolved. [290bef9daa56]
5. Only after the first 4 are healthy, invest in owned media (email/SMS/direct mail/WhatsApp) as the amplifier. [290bef9daa56]

### 3.9 Structure a Klaviyo account around F1/F2/F3
1. Define F1 (acquisition), F2 (first-to-second order conversion), F3 (top-20%-customer revenue, gross-profit adjusted). [3c84840ee4fe]
2. Identify your constraint using the metrics that map to each stage: F2 ≈ 90-day LTGP performance, F3 ≈ 365-day LTGP performance, first-to-second order conversion measured directly. [3c84840ee4fe] [b4ff45d77f83]
3. In every flow, make the first split new / returning / loyal-subscription, with messaging matched to each (aggressive trust-building for new; direct/no-intro for returning; least-aggressive, unincentivized for loyal). [3c84840ee4fe]
4. Layer secondary splits (cart value tier, product/collection interest, win-back timing) only after the journey-stage split is in place, and treat them as tests. [3c84840ee4fe]
5. When a constraint is identified (e.g. F2), go directly to that branch across all flows to diagnose and fix it, rather than reacting with generic new flows or blanket discount campaigns. [3c84840ee4fe]

### 3.10 Build and grow an engaged subscriber segment
1. Define "engaged" as opened/clicked an email OR took an on-site action (add-to-cart, started checkout, placed order) within chosen lookback windows (source example: ~180 days opens/clicks, ~220 days on-site actions, ~280 days orders — set your own based on purchase cycle). [83592aa3301a]
2. Build the segment in your ESP and record its current size as your sendable base; target at least 50% of the total list. [83592aa3301a] [c5da5743237]
3. Split the remaining unengaged/dormant portion into equal random samples (source used 10 samples). [83592aa3301a]
4. Add one sample into an engaged send at a time, using your best content. [83592aa3301a]
5. Measure how many of that added sample newly open/click or take an on-site action; fold those into the permanent engaged segment. [83592aa3301a] [c5da5743237]
6. Repeat over several months (source example: 6-9 months), tracking engaged-segment size as the core retention KPI. [83592aa3301a] [c5da5743237]
7. Save a full-list send to a marketing-calendar peak (e.g. Black Friday) once the engaged base has been substantially rebuilt. [83592aa3301a]

### 3.11 Plan campaign cadence (80/20 reach vs. specific goal)
1. Default 80% of campaign time/effort to reach: elite, broad content (education, entertainment, social proof, reviews) sent to the engaged segment. [097d09066f7a]
2. Reserve 20% for specific-goal narrow segments, each with one clear business reason (excess stock, supplier-led sale, product-specific push, VIP push). [097d09066f7a] [39c55eb82e67]
3. Route true one-to-one personalization to flows, not campaigns (3.9). [3121e4d083d4]
4. Measure campaign success via year-on-year channel growth relative to overall business, plus profitability metrics — not per-send revenue alone. [f6f96b40442]

### 3.12 Run RFM segmentation and RFM-driven win-backs
1. Score each subscriber on Recency, Frequency and Monetary value relative to your own subscriber base. [98fc8eced08a]
2. Classify into Champions, Loyal, Recent, At Risk, Needs Attention (treat the latter two similarly in practice). [98fc8eced08a]
3. Build a segment of former Champions now At Risk/Needs Attention for targeted win-back campaigns (part of the 20%-specific-goal slot). [98fc8eced08a]
4. Replace fixed-day win-back triggers with RFM-based triggers matched to each customer's own cadence. [98fc8eced08a]
5. Apply RFM segments across win-back, replenishment, post-purchase and abandoned cart/checkout flows. [98fc8eced08a]
6. Set this up in the ESP's analytics tab (Klaviyo named) `[verify UI]`. [98fc8eced08a]

### 3.13 Size an existing-customer paid ads budget (where applicable — see 2.9 principle 44 for when this applies)
1. Confirm you're in an exception case (e.g. fashion/frequent-drop) where email/SMS alone won't reach the whole existing base for new arrivals. [675be3b57a10]
2. Set a CPA target roughly half (or less) of your new-customer CPA target (source example: $40 new vs. $20 or lower existing). [675be3b57a10]
3. Compute the budget: (monthly send frequency, 4-7×) × (number of existing customers) × (CPM) ÷ 1,000. [675be3b57a10]
4. Watch for diminishing returns; if cutting spend barely reduces conversions, pull back and reallocate the savings to acquisition (worked example: $1,000/day → 50 conversions; $700/day → 47 conversions; the extra $300/day bought 3 conversions at $100 each — likely unprofitable). [675be3b57a10]

### 3.14 Audit discount-acquired cohorts
1. Run a cohort analysis broken down by discount code taken. [34373cddcf01]
2. Compare LTV and repeat purchase rate for discounted vs. full-price cohorts. [34373cddcf01]
3. Weigh the front-end lift (ROAS, efficiency, volume) against the long-term cohort quality before scaling the promotion. [34373cddcf01]

### 3.15 Use zero-party data to fix paid targeting
1. Collect zero-party data (persona, problem being solved, brand affinity) via post-purchase surveys or similar. [e74d0b65f2db]
2. Identify the top 20% of customers by revenue; extract their shared persona, the angle they responded to, and the offer they purchased. [e74d0b65f2db]
3. Overallocate paid spend toward creative/targeting that matches that top-20% pattern. [e74d0b65f2db]
4. Identify the bottom 20% of customers; extract their persona/angle/offer to find mismatches (e.g. wrong-problem angle). [e74d0b65f2db]
5. Reduce or exclude spend on angles that attract mismatched, low-repeat customers, even if front-end ROAS looks strong. [e74d0b65f2db]

## 4. Rules, thresholds and numbers

| rule | number or threshold | condition | source's basis | card id |
|---|---|---|---|---|
| LTGP formula | Revenue (NC AOV) − COGS − cost of delivery (shipping+fulfillment+3PL/handling/pick-pack) − transaction fees − refunds | Time-boxed cohort (day 0, 30, 90, 180, 365) | Stated formula | [2d30561e1938] |
| CAC formula | Total media spend ÷ new customers acquired in period | New-customer count is pre-refund; do not adjust for refunds | Stated formula | [2d30561e1938] |
| CAC measurement cadence | Daily/hourly (9-10 figure retailers); weekly/monthly (6-8 figure brands) | By business scale | Opinion/heuristic | (unlisted in cards; see 3.2) |
| LTGP:CAC ratio bands | <1 losing money; 1-2 inefficient; 2-3 target scaling band; 3+ leaving money on table | Applies to chosen LTGP window | Opinion/agency heuristic | [3861489d8286] |
| CAC target example | $80 30-day LTGP ÷ 2 = $40; $100 90-day LTGP ÷ 2 = $50 (25% CAC increase from window change) | Worked example, not a benchmark | Example | [3861489d8286] |
| Default LTGP window | 30-day for most/bootstrapped stores; 90-day for CPG/high-repeat or capital-rich brands | Roughly under vs. over $15-20M/year revenue | Opinion/heuristic | [5a300a3bc804] |
| Aggressive-loan-model risk threshold | "Incredibly risky" below roughly $15-20M/year revenue | Requires sophisticated interest-cost modelling | Opinion | [5a300a3bc804] |
| Volume-response test | e.g. +$10 CAC ceiling → 30-40% more customers = worth it; near-zero volume gain = stay conservative | Illustrative | Example | [5a300a3bc804] [3861489d8286] |
| CAC floor example (optimistic) | $0.70 CPC ÷ 3% conversion ≈ $23.33 | Best-case scenario | Worked example | [f1d832540bbc] |
| CAC realistic example | $1.00 CPC ÷ 2% conversion = $50 | Actual brand performance in example | Worked example | [f1d832540bbc] |
| CAC payback example | $50 CAC − $45 Day-0 gross profit = -$5 deficit | CPG/subscription, illustrative | Example | [d1160b9862c5] |
| Shopify "% returning customers" | = returning-customer orders ÷ total orders in period | Not repeat rate; use only for sale-period slicing | Definition + opinion | [9444eb58b437] |
| Klaviyo attribution soft target | 30-50% of revenue from email marketing | Soft indicator, "not a hard science" | Opinion | [2df157249026] |
| Campaign-revenue incrementality | ~70-80% of campaign revenue may be incremental for some accounts | Varies heavily by brand; unnamed outside studies | Cited studies (unnamed) | [2df157249026] |
| LTGP measurement cohorts | 30/60/90/180/365 days | Standard measurement windows in this source | Stated | [b4ff45d77f83] |
| Top-customer indicator | Revenue from top 20% of customers | Loyalty/leverage indicator | Stated | [2df157249026] [b4ff45d77f83] |
| Second-purchase failure rate | Only ~20% of customers buy a 2nd time from ~80% of brands | Source's opening framing stat, observed pattern | Opinion/observation | [42e1ab9189e1] |
| Campaign cadence split | 80% reach / 20% specific-goal | Rule of thumb, not fixed for every brand | Opinion/heuristic | [097d09066f7a] [3121e4d083d4] |
| Engaged-list target | At least 50% of list "engaged" by default | Track growth over time as core KPI | Opinion/heuristic | [83592aa3301a] [c5da5743237] |
| Engaged lookback windows | ~180 days (opens/clicks), ~220 days (on-site actions), ~280 days (orders) | Source example; adapt to your lifecycle | Example/heuristic | [83592aa3301a] |
| Dormant-audience rebuild | Split into 10 equal random samples, add back one at a time | Source's own method | Example | [83592aa3301a] |
| Ready-to-buy share of list | ~3% ready to buy "today" | Illustrative estimate | Opinion | [3121e4d083d4] |
| VIP definition | ~50%+ of revenue, ~80% of profit | Validate against own data | Opinion/heuristic | [3de8a595a9bb] |
| VIP-program leverage threshold | Higher leverage above roughly $10-20M/year revenue; below that, F2 (first-to-second order) is usually the bigger constraint | Revenue-scale heuristic | Opinion | [3de8a595a9bb] |
| Discount-acquired LTV penalty | ~60% of the source's client brands see substantially worse LTV/repeat rate from discount-acquired cohorts | Some 9-figure retailers show no penalty; check own data | Generalization from client base | [34373cddcf01] |
| Existing-customer CPA target | Roughly half (or less) of new-customer CPA (e.g. $40 new → $20 or lower existing) | Warm-audience efficiency expectation | Opinion/heuristic | [675be3b57a10] |
| Existing-customer send frequency | 4-7× per month | Used in the budget formula | Opinion/heuristic | [675be3b57a10] |
| Existing-customer budget formula | Frequency × existing customers × CPM ÷ 1,000 | Dollar-based, not % of spend | Stated formula | [675be3b57a10] |
| Existing-customer diminishing returns example | $1,000/day → 50 conversions; $700/day → 47 conversions ($100 marginal CAC on the extra 3) | Worked example | Example | [675be3b57a10] |
| Case: 9-figure activewear retailer (2025) | 750,000-person list; prior sends capped at 50,000-200,000 (≈550,000 unreached); rebuilt to full 750,000 send by end-of-2025 BFCM; beat prior-year BFCM by 40% YoY | Single-brand case, not a benchmark | Case example | [eacd1adfeb8d] [83592aa3301a] |
| Case: engaged-rebuild arithmetic | Engaged base 375,000; unengaged 375,000 split into 10 samples of 37,500; add-back total send "~410,000" (375,000+37,500=412,500 by direct math — source rounds down); ~20-30% of the added sample opens (source's own math implies ~7,000/37,500 ≈ 19%); new engaged size 382,000 | Source's own spoken, approximate arithmetic | Example | [83592aa3301a] |

Formulas the source does not give: general LTV (revenue-based), ROAS, contribution margin (referenced by name as things "Nathan's always saying you should be measuring for", but not defined here), CVR, AOV — pull these from 06-MEA-measurement sources instead.

## 5. Diagnostics and checks

| check | how | good | bad | next |
|---|---|---|---|---|
| Is LTV framed with a time window? | Ask what "LTV" means in your reporting | Always stated as 30/90/180-day LTGP | Bare "lifetime value" with no window | Rebuild reporting around cohort LTGP (3.1) [2d30561e1938] |
| Is LTGP built from real data? | Check whether 30/90-day LTGP is AOV × assumed margin or real order-level data | Real order/refund line items, refreshed monthly | AOV × flat margin assumption | Switch to order-level cohort calc (3.1) [2d30561e1938] |
| Are refunds double-counted or omitted? | Trace refund rate through both CAC and LTGP calculations | Refunds only in LTGP, never in CAC | Refunds subtracted from CAC, or missing from both | Move refund rate to LTGP only (3.1-3.2) [2d30561e1938] |
| Is the CAC target tied to a chosen LTGP window and ratio? | Check whether CAC ceilings in-platform trace back to an LTGP:ratio calculation | Explicit window + ratio behind every CAC target | CAC set from platform habit or competitor benchmarks | Run 3.3 [3861489d8286] |
| Is CAC near its realistic floor? | Compute CPC ÷ conversion-rate floor vs. actual CAC (3.4) | Floor is meaningfully below current CAC (real room) | Floor and current CAC are close | Shift investment to LTGP side (3.6) [f1d832540bbc] [2e9e88a22775] |
| Is "% returning customers" being used as an LTV KPI? | Check what metric leadership reviews for retention health | Cohort LTGP and F2 conversion used instead | Shopify returning-customer % cited as the retention number | Replace with cohort/F2 metrics (2.4, 3.9) [9444eb58b437] |
| Is attribution the only retention metric? | Review the retention dashboard's metric mix | Attribution (north star) + LTGP/top-20% profitability metrics both present | Only Klaviyo attributed-revenue % tracked | Add profitability metrics (2.4) [2df157249026] |
| Are flows split by journey stage first? | Open each flow and check the first branch | New / returning / loyal is the first split | Linear one-path flow, or first split by product | Restructure flows around F1/F2/F3 (3.9) [3c84840ee4fe] |
| What is the actual constraint (F1, F2 or F3)? | Compare acquisition volume, first-to-second order conversion rate, and top-20% revenue share against history/goals | Clear, data-backed answer | "We don't know" or guesswork | Build cohort/F-metric tracking (3.9, 4) [3c84840ee4fe] [b4ff45d77f83] |
| Is the engaged segment tracked and growing? | Pull engaged-segment size (definition in 3.10) over time | ≥50% of list, growing | Shrinking, unmeasured, or undefined | Run engaged-audience rebuild (3.10) [83592aa3301a] [c5da5743237] |
| Is the full list reachable for big moments? | Compare typical campaign send size to total list size | Sends approach full list at peaks | Sends capped far below list size (as in the 750k/200k case) | Rebuild engaged base ahead of the next peak (3.10) [eacd1adfeb8d] |
| Are win-backs arbitrary or RFM-based? | Check win-back flow trigger logic | Triggered by RFM At Risk/Needs Attention relative to own cadence | Fixed day-count (e.g. always 120 days) for everyone | Rebuild win-back off RFM (3.12) [98fc8eced08a] |
| Are VIPs treated differently from the general list? | Check flow/campaign paths for the VIP segment | Dedicated VIP branches and exclusivity rewards | Same flows/discounts as everyone | Build VIP pathways (2.8, 3.11) [39c55eb82e67] |
| Is VIP work the right investment right now? | Compare VIP revenue/profit share to F2 (first-to-second order) health | VIP share already strong; F2 is the constraint → work F2 first | VIP work prioritized despite VIP metrics already healthy and F2 weak | Redirect effort to F2 (2.8) [3de8a595a9bb] |
| Is existing-customer paid spend efficient? | Compare existing-customer CPA to new-customer CPA target; test spend cuts for conversion drop-off | Existing CPA well below new CPA target; cutting spend barely changes conversions | Existing CPA ≈ new CPA; cutting spend loses few conversions (marginal cost far above target) | Reset budget with the frequency×audience×CPM formula (3.13) [675be3b57a10] |
| Are discount-acquired cohorts checked for LTV quality? | Cohort-analyze by discount code taken | LTV/repeat rate comparable to full-price cohorts, or gap is known and accepted | No cohort check has been run before scaling the promotion | Run the discount-cohort audit (3.14) [34373cddcf01] |
| Is a strong front-end ROAS being trusted without a downstream check? | Cross-check refund/return rate and repeat purchase rate for the angle/creative in question | Downstream quality confirmed alongside front-end ROAS | High ROAS, but customer support/refund signals show mismatch, uninvestigated | Run the zero-party persona/angle audit (3.15) [e74d0b65f2db] |

## 6. Tools, settings and named features

| tool | use in source | notes |
|---|---|---|
| Klaviyo (heard/transcribed as "Clavio"/"Eclavio") | Primary ESP: campaigns, flows, attribution reporting, segmentation, RFM ("marketing analytics tab") | `[verify UI]` for exact location/name of the RFM feature and attribution reports today [98fc8eced08a] [2df157249026] |
| Shopify | Source of order-level revenue/refund data for real LTGP calculation; also the source of the "% returning customers" analytics-dashboard metric the source calls unreliable | `[verify UI]` for current dashboard metric wording/location [9444eb58b437] [2d30561e1938] |
| Meta, Google Ads | General paid-acquisition platforms referenced for CAC, CPC, existing-customer retargeting spend | No platform-specific settings named |
| TikTok Shop | Cited only as an example of a low-AOV acquisition channel correlated with weaker retention | Illustrative, not a how-to [290bef9daa56] |
| Presenter's own channel (unnamed in transcript) | Referenced as the place with a full breakdown of "exactly how to structure all your email flows" (every flow, triggers, email counts) | Out of scope for this document `[web check: identify and verify the referenced channel/content]` |

## 7. Examples and case results

All are examples or single-brand cases, not promises.

- **Brand A vs. Brand B (illustrative, not real brands).** Same product/niche/industry, both $40 CAC. Brand B gets a 30% lift in LTGP within 90 days: $100 on first purchase → $130 by day 90. Brand A: $100 → $112 by day 90. Because Brand B is outperforming on 90-day profit by roughly 10-15%, it can raise its CAC ceiling to $45, outbid Brand A in auctions, acquire more customers, and still out-earn Brand A — the source's argument for why unit economics and first-year LTV matter for scaling decisions. [used to frame 2d30561e1938 / 3861489d8286]
- **CAC target arithmetic.** $80 30-day LTGP ÷ 2 = $40 CAC target; $100 90-day LTGP ÷ 2 = $50 CAC target (a 25% CAC increase from extending the window). [3861489d8286]
- **CAC floor/ceiling.** Optimistic: $0.70 CPC ÷ 3% conversion ≈ $23.33. Realistic (the brand's actual average): $1.00 CPC ÷ 2% conversion = $50. [f1d832540bbc]
- **CPG Day-0 loss.** $50 CAC vs. $45 Day-0 gross profit = -$5 deficit, recovered via subscription/replenishment profit over time (CAC payback period). [d1160b9862c5]
- **Existing-customer diminishing returns.** $1,000/day existing-customer spend → 50 conversions/day; cut to $700/day → still 47 conversions/day; the extra $300/day only bought 3 conversions ($100 marginal cost each), likely unprofitable. [675be3b57a10]
- **9-figure activewear retailer, 2025 (named case).** ~750,000-person email list; campaigns historically capped at 50,000-200,000 sends, leaving roughly 550,000 profiles unreached. Rebuilt around an engaged-audience definition: found ~375,000 already engaged; split the remaining ~375,000 into 10 random samples of 37,500; added samples back gradually into engaged sends (source's own rounded math: engaged send grows to "about 410,000"; roughly 20-30% of the newly added sample opens, source states "7,000" became newly engaged from one 37,500 batch, bringing the engaged pool to 382,000); repeated over 6-9 months. Result: sent to the full 750,000 for their Black Friday launch at the end of 2025, and beat the prior year's Black Friday results by 40% year-on-year. [eacd1adfeb8d] [83592aa3301a] [c5da5743237]
- **9-figure supplements retailer (brief, unnamed illustration for the 80/20 rule).** A "thousand SKU" subs retailer where 80% of sends are reach-focused (education/engagement/entertainment/social proof) and 20% target specific goals, e.g. clearing excess stock of one product for one specific brand in the portfolio. No outcome numbers given. [supports 097d09066f7a]
- **Skin-health supplement / "energy" angle mismatch.** A supplement for skin health acquired via a Meta angle about energy production shows a strong front-end ROAS ("a five ROAS") but the product doesn't solve the problem the ad promised, leading to returns, refunds and no repeat purchase — surfaced only through customer support feedback, not the ad dashboard. [e74d0b65f2db]

## 8. Mistakes the source warns about

1. Treating Shopify's "% returning customers" as a retention/LTV KPI — it moves with business age and worsening acquisition, not with real repeat behaviour. [9444eb58b437]
2. Calculating LTGP from AOV × assumed gross margin instead of real order-level cohort data. [2d30561e1938]
3. Folding refund rate into the CAC calculation (corrupts the paid-media efficiency signal) or leaving refunds out of both CAC and LTGP. [2d30561e1938]
4. Optimizing only for Klaviyo/attribution dashboard metrics, or the opposite extreme of ignoring incremental repeat-revenue work in favour of only long-term LTV thinking. [2df157249026]
5. Chasing pop-up opt-in rate instead of pop-up conversion, AOV and gross profit of signed-up customers. [4789763c9e99]
6. Building one linear flow sequence for every entrant, or splitting flows first by product (denim vs. t-shirt) instead of by customer journey stage. [3c84840ee4fe]
7. Hyperpersonalizing broad campaigns into micro-segments — burns labour and starves reach, leaving large parts of the list unreached for big moments (the 750k/200k case). [097d09066f7a] [eacd1adfeb8d]
8. Prioritizing subject-line, click-through-rate and time-delay testing over structure/offer/messaging tests aimed at the identified constraint. [ebe1e2f78000]
9. Using arbitrary fixed-day win-back triggers instead of RFM-based triggers matched to each customer's real cadence. [98fc8eced08a]
10. Treating VIPs the same as the general list with broad discounts instead of exclusivity-based rewards. [39c55eb82e67]
11. Chasing VIP-revenue programs when the real constraint (usually first-to-second order conversion, especially under roughly $10-20M/year) lies elsewhere. [3de8a595a9bb]
12. Spending the same CPA target on existing customers as on new-customer acquisition, or continuing to scale existing-customer spend past the point of diminishing returns. [675be3b57a10]
13. Trusting a strong front-end ROAS as proof of a good acquisition angle without checking downstream refunds, returns and repeat behaviour. [e74d0b65f2db]
14. Assuming a discount-acquired cohort is equally valuable without a cohort/LTV check by discount code. [34373cddcf01]
15. Assuming continuous CAC reduction is always available, or underestimating how much LTGP can be raised through offer/subscription work. [2e9e88a22775]
16. Jumping to email/SMS fixes when the real constraint is product quality, portfolio, acquisition quality or customer experience. [290bef9daa56]
17. Running an aggressive, loan-funded, long-payback acquisition model without the financial-modelling sophistication to manage interest costs, especially under roughly $15-20M/year revenue. [5a300a3bc804]

## 9. Caveats, conflicts and what is missing

- **Scope conflict with the source's own ingestion header**, detailed above under "scope note": the header says to skip ~70% of this video (Angus Cowan's Klaviyo/flow/RFM/segmentation content) as belonging to 14-EML, yet most of the 28 cards for this source_id cover exactly that content and live under 17-CXP-post-purchase. Pass 2 for this folder should expect and reconcile overlap with 14-EML rather than treat this as a clean, non-duplicated source.
- **Both presenters' credentials are self-stated and unverifiable from the transcript.** Angus Cowan calls his agency "the biggest email marketing agency in Australia" — unverified. `[web check: Marketing Emails agency, Australia — verify size claim]`. Nathan's own agency name is never stated in the transcript. `[web check: presenter identity/agency, if precise attribution is needed]`.
- **Every numeric heuristic in this document is the presenters' own operating rule of thumb from their client base, not published research**: the 2-3 LTGP:CAC scaling band, the 80/20 reach/specific-goal campaign split, the ~$10-20M VIP-leverage and window-risk thresholds, the ~50%/80% VIP revenue/profit definition, the ~60%-of-brands discount-LTV generalization, the 4-7× existing-customer frequency, the 180/220/280-day engaged lookback windows, and the 10-sample dormant-reactivation method. The source itself repeatedly says to "pull your own numbers" — treat every threshold here as a starting point to test against a brand's actual data, not a fixed rule.
- **Direct, stated disagreement with a common industry position**: the source explicitly argues against the "massive narrative in the industry" toward one-to-one hyperpersonalization in campaigns, favouring reach-first (80/20) sending instead. This is the source's own contrarian stance, not a resolved consensus — flag it for Pass 2 reconciliation against any 14-EML source that recommends deeper personalization.
- **The source corrects its own earlier public position** on existing-customer paid spend ("about 2 or 3 years ago, we were of the position that you should spend nothing on existing customers... we have been wrong on this core assumption before"), then carves out the fashion/frequent-drop exception. Treat the exception as the source's current, revised view, not a long-settled rule.
- **The 750k-list case study's arithmetic doesn't fully reconcile**: 375,000 engaged + 37,500 added back = 412,500 by direct math, but the source states "something like 410,000"; similarly "7,000" newly engaged out of a 37,500 sample is closer to 19% than the stated "20 or 30%." This is spoken, approximate arithmetic — kept here as the source stated it, flagged rather than corrected, per this playbook's no-invention rule.
- **No formulas given for ROAS, contribution margin, general revenue-based LTV, or CVR/AOV themselves**, even though contribution margin and ROAS are referenced by name (attributed to "Nathan['s] always saying"). Pull those definitions from 06-MEA-measurement sources.
- **No concrete flow-build content** (email counts, subject-line examples, specific trigger logic, timing/delay values) — the presenter explicitly defers this to his own channel. `[web check: identify the referenced channel/content if a full flow build is needed]`.
- **No sample-size or statistical-significance guidance anywhere** — not for RFM percentile cutoffs, not for the engaged-audience lookback windows, not for the 10-sample dormant-reactivation method, not for the discount-cohort LTV comparison. All are presented as directional heuristics.
- **"Elite content" is never defined** beyond examples (education, entertainment, social proof, reviews) — no criteria for what makes content "elite" are given.
- **Second-party data** is mentioned once in passing by the source (in the context of first/zero/third-party data) with no definition or example given here; not carded under this source's 28 cards.
- **Ends with a commercial pitch**: a paid-audit offer for brands doing $5M+/year and a hiring link for performance marketers — a reminder that thresholds and framing in this video (e.g. what counts as "worth investing in VIP work," or when to run an audit) serve the presenters' own funnel.

## 10. Card index

- [2d30561e1938] Define Lifetime Gross Profit with a Time Constraint
- [290bef9daa56] Prioritize the Retention Hierarchy Before Touching Email and SMS
- [3861489d8286] Set a CAC Target from LTGP and an Efficiency Ratio
- [f1d832540bbc] Estimate a scenario bound for paid acquisition cost from CPC and conversion
- [d1160b9862c5] Use CAC Payback Period for Subscription-first Brands
- [5a300a3bc804] Decide the LTGP Window by Growth Appetite and Capital
- [9444eb58b437] Separate period returning-customer rate from cohort repeat purchase
- [2e9e88a22775] Inspect Which Half of the LTGP:CAC Ratio to Work On
- [2df157249026] Balance Attribution and Profitability Metrics in Your Owned Media KPIs
- [4789763c9e99] Focus on Pop-up Conversion Rather Than Opt-in Rate
- [3c84840ee4fe] Map the Customer Journey as F1/F2/F3 Functions and Structure Flows Around It
- [097d09066f7a] Segment Campaigns for Reach, Not Hyperpersonalization
- [eacd1adfeb8d] Find eligible subscribers missed by overly narrow campaign segments
- [4d8506a387fd] Plan Lifecycle Cohorts by Purchase and Subscription Stage
- [ebe1e2f78000] Prioritize retention tests by the constraint in the customer journey
- [f6f96b40442] Map Campaign Revenue to Calendar Peaks and Engagement Build
- [b4ff45d77f83] Measure Retention at 30/60/90/180/365 Day Cohorts and Top-20% Revenue
- [42e1ab9189e1] Diagnose weak second-purchase conversion before blaming email copy
- [9f7c64c08aab] Plan a Bundled, Subscription-first Offer Structure to Raise LTGP
- [83592aa3301a] Build and grow an engaged subscriber segment
- [3121e4d083d4] Use flows for personalization, campaigns for reach
- [3de8a595a9bb] Define VIPs by revenue and profit share
- [98fc8eced08a] Run RFM analysis to segment on real purchase behavior
- [675be3b57a10] Use paid ads to surface new arrivals to existing customers
- [34373cddcf01] Audit discount-acquired cohorts for LTV quality
- [e74d0b65f2db] Use zero-party data to improve acquisition targeting
- [c5da5743237] Measure engaged-segment growth as your core retention KPI
- [39c55eb82e67] Reward VIPs with exclusivity rather than broad discounts
