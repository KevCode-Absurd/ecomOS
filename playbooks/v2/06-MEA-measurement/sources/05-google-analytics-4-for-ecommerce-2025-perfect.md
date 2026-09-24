# Google Analytics 4 For eCommerce 2025 (Perfect for beginners)

source_id: 19zPkTFzbRWj1MTf9vQAbowNTQsmeQrpY  |  folder: /06-MEA-measurement  |  cards: 9  |  words: 3,430  |  type: transcript (YouTube video)

credibility: An unnamed YouTube creator who runs a Shopify store. The store sends email through Omnisend and runs CPC and paid Facebook traffic. The creator plugs their own YouTube channel. They sell no tool here. Evidence is 1 store's GA4 screens, read aloud (last 28 to 60 days), plus opinion. No sample sizes, no test results, no benchmarks from other stores. The source says it is for beginners. The file opens with a curator note (scope, "look for", "skip"). That note is not the creator's text; where it differs from the transcript, this file says so.
date signals: "2025" in the title. Uses the GA4 term "key events" and the metric "session key event rate". `[web check: date GA4 renamed conversions to key events, to confirm the advice is post-rename]` Names the GA4 Reports groups "business objectives", "life cycle", "search console" and "user", and the Insights tool with "suggested questions". All menu paths are from 2025 and can move.

## 1. What this source is for

It helps an operator read GA4 for a Shopify store without getting lost. It covers 4 jobs: see where traffic comes from and whether it engages, find conversion rate per channel and per medium, find conversion rate per landing page (product page), and find where shoppers drop out of the purchase funnel. The core warning: a GA4 "key event" is not always a purchase, so every conversion rate must be filtered to the purchase event. It is a click-path guide, not a measurement-integrity guide. It does not cover tracking setup (see 05-SET) or whether a difference between pages is statistically real (see 09-CRO).

## 2. Principles

1. **Use GA4 for what Shopify does not show.** Source says GA4 gives traffic-source detail, engagement quality and per-landing-page conversion that the Shopify dashboard does not give "with this much detail". Use Shopify for order and sales totals. The creator skips the GA4 home dashboard because most of its numbers are "things that I can find on Shopify". Condition: a Shopify store. The card adds that GA4 and Shopify numbers will differ, so pick 1 source of truth per question (card addition, not in the transcript). [1735fbb29aff]
2. **A key event is not a purchase.** GA4 counts many actions as events (page views, add to carts and more). Key events can include more than purchases. So "session key event rate" is only a conversion rate after you filter it to "purchase". Condition: always, for any report where you add a key-event metric. Evidence: the creator's own setup; their store read 1.7% overall after the filter. [d5605a4c54a8] [67d1533fdd9c]
3. **Engaged sessions are a relevance signal.** Source defines an engaged session as one that "lasted longer than 10 seconds". Source says 10+ seconds on a page means the page matched what the visitor was looking for. A very low engaged-session count on organic search is "a bad sign": people search, land, and do not find what they wanted, or the page is not relevant to the query. Condition: the source's reading, not a proven link to sales. The card says 10 seconds is GA4's definition, not a target. `[web check: full GA4 engaged-session definition; the source gives only the time rule, and GA4 may also count sessions with a key event or 2+ page views, and the 10-second timer may be adjustable]` [22a5b5e7d62e]
4. **Split by channel, then by medium.** Session primary channel group shows organic search, cross-network, paid and so on. Adding medium gives "a second level of knowledge": CPC, paid Facebook, and a named sender such as the Omnisend email flow. Condition: medium values come from UTM tags, so bad tagging makes this view wrong (card caveat, not in the transcript). [b84c5ad106a2] [5dde1ccb7160]
5. **Customize the default tables.** Default GA4 tables lack the metrics you need. Add them under Customize report, then Metrics, then save. The creator's chosen set: sessions, engaged sessions, engagement rate, average engagement time, events per session, event count, key events, session key event rate (filtered to purchase), total revenue. Condition: pick the metrics that "mean a lot" to you; the source gives no fixed list. [67d1533fdd9c]
6. **Compare product pages by purchase conversion rate.** Source says this rate is not in Shopify analytics. A low page has 1 of 3 causes: wrong traffic sent to it, a page that "needs more work", or a product that is less appealing. Find the cause before acting. Condition: pages with enough sessions; the card warns small traffic gives noisy rates. `[needs brand data: sessions per landing page to judge if a rate is stable]` [b700e12faf0c]
7. **Read the funnel for the scary drops, not the normal one.** The drop from session started to viewed product "is normal". The drops that matter are between add to cart, checkout and purchase. Condition: the source's opinion; it still says a big first drop is worth fixing (see rule 8). [000e5a39ddc8]
8. **Each drop points to a different fix.** Many sessions but few product views: collections unclear, visitors cannot find what they want, search bar may need work. Big drop add to cart to checkout: suspect the cart page. Big drop checkout to purchase: suspect high shipping rates, a checkout page that does not look trustworthy, or a broken checkout step. Condition: these are hypotheses to check, not proven causes. [000e5a39ddc8]
9. **Insights is for quick answers only.** GA4's AI Insights gives short answers to a limited, predefined list of suggested questions (example: which countries users come from). The creator uses it for "a very quick answer" only. Condition: verify in the full report before acting (card addition). The curator note says to skip this part. [7cef7f4d4e54]

## 3. Procedures

All paths below are the source's 2025 click paths. `[verify UI]` on every step.

### 3.1 Conversion rate by traffic channel and medium [5dde1ccb7160] [b84c5ad106a2] [67d1533fdd9c]

1. Open Reports, then Life cycle, then Traffic acquisition. `[verify UI]`
2. Set the date range (creator used last 28 days). Set the chart to daily, weekly or monthly. `[verify UI]`
3. Read the default view: sessions by session primary channel group. Scroll down for the full table. `[verify UI]`
4. Hover over any metric name to read its definition. `[verify UI]`
5. Add the medium dimension next to session primary channel group. The source does not say which control adds it. `[verify UI]`
6. Click Customize report, then Metrics. Add session key event rate (and any other metrics you want). Click Apply. `[verify UI]`
7. On the session key event rate column, change the event filter from all key events to "purchase". `[verify UI]`
8. Save the report so the setup stays. `[verify UI]`
9. Compare rows. The card's reading: a channel with strong sessions but weak purchase rate is a targeting or landing-page problem, not a volume problem (card addition). [5dde1ccb7160]

### 3.2 Event counts by type [67d1533fdd9c]

1. In the Traffic acquisition table, find the event count column. `[verify UI]`
2. Click "All events" and pick the event you care about (for example add to cart or purchase). `[verify UI]`
3. Choose which events "mean the most" to you. The source gives no list beyond add to cart and purchase.

### 3.3 Conversion rate per landing page (product page) [b700e12faf0c]

1. Open Reports, then Engagement, then Landing pages. `[verify UI]` The transcript says "reports ... acquisition and this time under engagement you go to landing pages", which is garbled. The curator note and the card say Reports, then Engagement, then Landing pages. `[web check: current GA4 location of the Landing page report]`
2. Edit the report (the creator says "the editor dashboard") and add session key event rate. It is not there by default. `[verify UI]`
3. Filter the metric to "purchase". `[verify UI]`
4. Compare your top product pages. Look for pages far above or far below the rest.
5. For a low page, test the 3 causes in turn: traffic mismatch, page quality, product appeal. The card adds: rule out traffic mismatch first, since a redesign will not fix wrong traffic (card addition). `[needs brand data: traffic source mix per landing page]`

### 3.4 Purchase funnel drop-off [000e5a39ddc8]

1. Open Reports, then Monetization, then Purchase journey. `[verify UI]`
2. Set the date range (creator used last 30 days). `[verify UI]`
3. Read the steps in order: session started, viewed product, added to cart, began checkout, purchased. Each step shows the share of the step before.
4. Accept a large drop from session started to viewed product as normal, but ask why if it is very large (see principle 8).
5. Find the largest drop among add to cart, checkout and purchase. Map it to the cause list in principle 8.
6. The source stops at "try to understand it". It gives no threshold for a "huge" drop and no test steps. `[needs brand data: step rates over several periods to know what is normal for the store]`

### 3.5 Wider review habit [1735fbb29aff]

1. If you run Google Ads, link GA4 to Google Ads and to the Shopify store. The source says to do this "using the Shopify integration" and calls it "quite simple". It gives no steps. `[verify UI]` Setup belongs to 05-SET.
2. Review all reports under Life cycle. The source says "all of them are important" but does not name them all. `[verify UI]`
3. Open the Ecommerce purchases report to see purchases per product and how customers behaved. The source does not give its path. `[verify UI]`
4. Optional: use Library to add or remove report groups in the left sidebar. The creator keeps the defaults. `[verify UI]`

## 4. Rules, thresholds and numbers

| rule | number or threshold | condition | source's basis | card id |
|---|---|---|---|---|
| Engaged session | more than 10 seconds | GA4 definition as the source states it; not a target | GA4 metric tooltip, read aloud | [22a5b5e7d62e] |
| Filter key-event rate to purchase | always | any report using session key event rate | creator's setup; key events include non-purchase events | [d5605a4c54a8] |
| Example store conversion rate | 1.7% overall | creator's store, purchase-filtered, about last 28 days; example only | own store | [d5605a4c54a8] |
| Home dashboard date range | up to last 12 months | home screen; creator viewed 60 days | UI read aloud `[verify UI]` | none |
| Normal funnel drop | session started to viewed product | "normal"; source gives no number | opinion | [000e5a39ddc8] |
| Worrying funnel drops | add to cart to checkout to purchase | source gives no threshold | opinion | [000e5a39ddc8] |
| Example funnel | about 10K sessions, 53% viewed product, "99.2%" added to cart, 63% began checkout, 50% purchased | creator's store, last 30 days; see section 9 on the 99.2% figure | own store | [000e5a39ddc8] |

## 5. Diagnostics and checks

| check | how | good | bad | next step | card |
|---|---|---|---|---|---|
| Is the conversion rate really purchases? | Open the session key event rate column filter | Filter set to "purchase" | Filter on all key events | Set to purchase. Card adds: cross-check against total revenue in the same table, and re-check after any GA4 key-event change | [d5605a4c54a8] |
| Is traffic relevant? | Traffic acquisition: engaged sessions, engagement rate, average engagement time by channel | Source gives no number | "Very low" engaged sessions on a channel | Paid: check ad-to-page message match before adding spend. Organic: check the page matches search intent. Card adds: rule out bots and mis-tagged campaigns first | [22a5b5e7d62e] |
| Which channel or medium converts? | Traffic acquisition with medium and purchase-filtered rate | Rate in line with volume | High sessions, low purchase rate | Treat as a targeting or landing-page problem (card) | [5dde1ccb7160] [b84c5ad106a2] |
| Which product page leaks? | Landing pages with purchase-filtered rate | Top pages close to each other | 1 page far below similar pages | Check traffic mix, then page, then product appeal | [b700e12faf0c] |
| Where does the funnel break? | Monetization, then Purchase journey | Source gives no benchmark | "Huge" drop add to cart to checkout, or checkout to purchase | Cart page; shipping cost, trust, checkout steps | [000e5a39ddc8] |
| Few product views? | Purchase journey, first 2 steps | Source gives no benchmark | Many sessions, few product views | Collections, navigation, search bar | [000e5a39ddc8] |
| Are funnel steps tracked at all? | Card caveat only; source gives no method | All 5 steps show counts | A step missing or near 0 | Fix event tracking (05-SET) before reading drops | [000e5a39ddc8] |

## 6. Tools, settings and named features

- **GA4 home dashboard**: auto-picked metrics, date range up to 12 months, chart metric can be changed. Creator uses it for overview only. `[verify UI]` [1735fbb29aff]
- **Insights (suggested questions)**: AI answers to a fixed question list, grouped by topic such as demographics. `[verify UI]` [7cef7f4d4e54]
- **Left sidebar: Reports, Explore, Advertising.** Advertising shows Google Ads results once linked. The source does not cover Explore. `[verify UI]` [1735fbb29aff]
- **Reports groups**: business objectives, life cycle, search console, user. **Library** changes which groups show. `[verify UI]` [67d1533fdd9c]
- **Traffic acquisition** (Life cycle): session primary channel group, medium, sessions, engaged sessions, engagement rate, average engagement time, events per session, event count, key events, session key event rate, total revenue. `[verify UI]` [5dde1ccb7160] [b84c5ad106a2]
- **Customize report, then Metrics, then Apply, then Save.** `[verify UI]` [67d1533fdd9c]
- **Landing pages** (Engagement): per-page metrics; add session key event rate. `[verify UI]` [b700e12faf0c]
- **Purchase journey** (Monetization): 5-step funnel. `[verify UI]` [000e5a39ddc8]
- **Ecommerce purchases**: per-product purchases. Path not given. `[verify UI]` [1735fbb29aff]
- **Shopify integration**: links GA4 with Google Ads and the store. Steps not given. `[verify UI]` [1735fbb29aff]
- **Omnisend**: the creator's email tool; shows up as its own medium row. [b84c5ad106a2]

## 7. Examples and case results

All from the creator's own store. Examples, not benchmarks or promises.

- Overall purchase conversion rate 1.7%, after filtering key events to purchase (about last 28 days). [d5605a4c54a8]
- Organic search was a large traffic source; the creator calls it "super important for any e-commerce business". [22a5b5e7d62e]
- Landing pages: 2 products had "very high" conversion rates next to a third. No numbers given. [b700e12faf0c]
- Purchase journey, last 30 days: almost 10K sessions started; 53% viewed a product; "99.2%" of those added to cart; 63% of those began checkout; 50% of those purchased. See section 9. [000e5a39ddc8]

## 8. Mistakes the source warns about

1. Reading session key event rate as conversion rate without filtering to purchase. Fix: set the filter to "purchase". [d5605a4c54a8]
2. Reading only the GA4 home dashboard. Fix: work in Reports, which has what Shopify lacks. [1735fbb29aff]
3. Reading channel group alone. Fix: add medium to see CPC, paid social and email senders apart. [b84c5ad106a2]
4. Leaving tables at default. Fix: customize and save. [67d1533fdd9c]
5. Panicking over the session-to-product-view drop. Fix: it is normal; focus on cart, checkout and purchase drops, while still checking collections and search if product views are very low. [000e5a39ddc8]
6. Treating Insights answers as full analysis. Fix: use it for quick pointers only. [7cef7f4d4e54]

## 9. Caveats, conflicts and what is missing

- **The 99.2% add-to-cart figure is likely a transcription error.** The creator says "only 99.2%", and "only" does not fit 99.2%. Arithmetic (done in code): with 99.2%, 10,000 sessions give about 1,656 purchases, a 16.6% session conversion rate. With 9.2%, they give about 154 purchases, 1.5%, close to the 1.7% the same creator reports. The card says "most viewers added to cart", which follows the 99.2% reading. Do not cite either figure as a benchmark. The 2 reports use different windows (28 vs 30 days), so they will not match exactly.
- **Engaged-session definition is partial.** The source gives only the 10-second rule. `[web check: full current GA4 definition and whether the timer is configurable]`
- **Landing pages path conflict.** Transcript says acquisition then engagement; curator note and card say Engagement then Landing pages. `[verify UI]`
- **No thresholds.** No "low" engagement rate, no "huge" drop size, no minimum sessions per page. Everything is relative to the store's own data. `[needs brand data: baseline engagement rate, funnel step rates and page conversion rates over several periods]`
- **Card additions not in the transcript:** UTM tagging caveats [5dde1ccb7160] [b84c5ad106a2], bot traffic [22a5b5e7d62e], revenue cross-check and key-event drift [d5605a4c54a8], small-sample noise [b700e12faf0c], missing-event fake drop-offs [000e5a39ddc8], GA4 vs Shopify differences [1735fbb29aff]. They are sensible but are the card writer's, not the creator's.
- **No attribution, no deduplication, no consent, no data quality.** The source never asks whether GA4 numbers are complete (consent loss, ad blockers, missing events). Those belong to other 06-MEA sources.
- **No significance.** "One page is performing way better" is judged by eye. Whether a gap is real belongs to 09-CRO.
- **Setup skipped.** GA4 install, key-event marking and Google Ads linking belong to 05-SET.
- **Explore is named but not taught.**
- **Single store, single creator.** All readings are opinion plus 1 store's screens.

## 10. Card index

- [d5605a4c54a8] Measure purchase conversion rate, not raw key event rate
- [5dde1ccb7160] Find conversion rate by traffic channel
- [22a5b5e7d62e] Read engaged sessions as a traffic-relevance signal
- [b700e12faf0c] Compare product-page conversion rates in the Landing Pages report
- [000e5a39ddc8] Diagnose funnel drop-off with the Purchase Journey report
- [b84c5ad106a2] Segment traffic by channel and medium together
- [67d1533fdd9c] Customize and save GA4 reports instead of reading defaults
- [1735fbb29aff] Use GA4 to fill gaps Shopify analytics leaves
- [7cef7f4d4e54] Read GA4's AI Insights for quick answers, not deep analysis
