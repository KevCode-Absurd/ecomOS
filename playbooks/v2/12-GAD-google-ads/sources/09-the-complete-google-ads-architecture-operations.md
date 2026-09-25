# The Complete Google Ads Architecture & Operations Manual (2026 Edition)

source_id: 1wZaOcKMTf-VGhMuD5ZaOmc5qF_babL-x  |  folder: /12-GAD-google-ads  |  cards: 22  |  words: 6048  |  type: article (compiled manual, no named author)
credibility: No author, company or byline. The document says it is "compiled from official Google documentation, platform changelogs, and operator-grade playbooks" and closes by naming Google Ads Help Center, Google Ads Developer Blog, Search Engine Journal, PPC Land and "operator-level campaign architecture analyses". No links, no own results, no client data. It sells nothing. Evidence is mostly restated platform facts plus unsourced averages and heuristics (PMax CPC $0.68, 4.1x ROAS, Ad Rank thresholds, Quality Score weights, 11% brand spend / 34% conversions, one case of 49% to 57% Shopping coverage). Treat it as a secondary summary, likely generated or derivative (see section 9).
date signals: File modified 21 Sep 2026. Text says "current as of September 2026". Dated changes it names: YouTube Video Action paused and archived 28 Feb 2026; enhanced conversions accept tag, Data Manager and API data together from April 2026; Demand Gen adds Google Maps May 2026; Smart Bidding relabel (Target CPA, Target ROAS standalone) June 2026; enhanced conversions single on/off switch June 2026; Standard Shopping Maximize conversion value without tROAS July 2026; PMax account-level placement exclusions expanded August 2026; Demand Gen inventory list "as of August 2026"; YouTube audio ads in the US limited to Pandora/SiriusXM 1 Sep 2026. Also names AI Max for Search, AI Mode queries and Waze as a PMax surface. Every one of these needs a live check [web check: each 2026 change in the appendix table].

## 1. What this source is for

Use it as a map of a full Google Ads account for an ecommerce store: which campaign type does which job (AI Max Search, Standard Search, Standard Shopping, PMax, Demand Gen, YouTube formats), how to stop PMax eating brand and high-intent Shopping traffic, how the auction prices a click, how to write feed titles and clean Merchant Center, how to wire GTM, enhanced conversions and server-side tracking, and when to pick Target ROAS, Maximize conversion value or portfolio bidding. Its most usable single tool is the 5-gate check before scaling spend (section 3.9). It is broad but thin on how: most items are 1 paragraph, and many numbers carry no source.

## 2. Principles

1. **Run the account as a stack of layers, each with 1 job.** AI Max for Search finds net-new long-tail and conversational queries. PMax handles cross-channel conversion. Demand Gen fills the top of funnel. Branded and non-branded Search harvest ready demand. Condition: the source ties this to ecommerce advertisers spending $50K to $500K a month; it gives no advice for smaller accounts. Evidence: none beyond "the highest-performing ecommerce advertisers" do this. [61d89a7caa36] [needs brand data: monthly Google spend in the brand's currency]
2. **The layers depend on each other, with a lag.** Demand Gen warms people that PMax and Search later convert. The source says if you remove the assist layer, branded performance drops "weeks later". Condition: judge assist layers over a long enough window to see that lag; do not cut them on their own direct ROAS. Evidence: assertion only, no data. [61d89a7caa36] [needs brand data: branded search volume and conversions before and after any Demand Gen pause]
3. **Keep roles separate or campaigns cannibalise each other.** Standard Shopping and PMax bid on the same feed. Without role rules PMax takes brand and high-intent Shopping traffic and you lose cost visibility on your best queries. The source calls this "the single most common structural failure in 2026". Condition: any account running PMax next to Shopping or brand Search. [4eceae623d26] [9c25700ad918]
4. **Shopping is for precision, PMax is for scale.** Standard Shopping shows which products match which queries and allows product-group bids. PMax picks placements for you. Condition: use Shopping for top-revenue SKUs, brand terms and high-intent categories; use PMax for catalog-wide and multi-surface acquisition. [6a480c2ffb47]
5. **The auction is not a bidding war.** Bid is 1 input among auction-time quality (expected CTR, ad relevance, landing page experience), expected asset impact, competition for that exact query, and user context (location, device, time, language, query). A better ad and landing page can win a higher position for less money. Condition: applies to every search auction; each auction is fresh, so no position is "owned". [2d82081ef51f]
6. **Quality lowers cost for the same position.** Under the source's simplified second-price logic, your Quality Score divides the price you pay, so higher quality cuts actual CPC. Condition: the formula is a simplification Google does not publish. [1b89e99face8] [98dc5116df92]
7. **The visible Quality Score is a diagnostic, not what the auction reads.** The auction reads expected CTR, ad relevance and landing page experience live; the 1 to 10 number summarises them. [1267e0489b18]
8. **Landing page experience weighs as much as ad copy.** Source weights: expected CTR about 39%, landing page experience about 39%, ad relevance about 22%. The source says most advertisers over-invest in ad copy tests and under-invest in landing page relevance, speed and mobile experience. Condition: Search with keywords. Weights are approximate and unpublished. [1267e0489b18]
9. **In Shopping and PMax the feed is the ad.** There are no keywords; Google reads titles, descriptions, attributes, price and availability to decide which queries a product matches. The source calls the title "the most important line of advertising copy you will ever write". Condition: feed-led campaigns. This is the source's strong opinion. [7671c6e57a6e]
10. **Front-load searched attributes in titles, and keep one order across the catalog.** Consistency lets the algorithm learn patterns. [76f0f732dbe5]
11. **Brand demand and non-brand demand must be measured apart.** "Brand traffic captures demand. Non-brand traffic creates it." Blending them flatters account ROAS and hides whether prospecting pays. Condition: any account with meaningful brand search. [9c25700ad918]
12. **Intent is not equal, so bids should not be equal.** Group keywords by buyer intent tier, not by feature or volume. Each tier gets its own bids, landing pages and measurement. [e8f1dbe974c5]
13. **Build long-tail on purpose.** Long-tail has lower CPC, less auction pressure and cleaner conversion signal. It "compounds horizontally across markets, angles, and variations". The source calls head-term chasing "high ego"; that is opinion. [e8f1dbe974c5]
14. **Catalog breadth is "surface area".** Shopping and PMax need enough products to find profitable pockets of demand. Source says under 30 SKUs is not enough "at scale". [6a480c2ffb47] [needs brand data: count of approved, in-stock SKUs]
15. **Do not scale on bad inputs.** Scale amplifies feed problems and wrong conversion data; it does not fix them. "Fix inputs before chasing outputs." PMax performance is a function of feed data, conversion signals, audience signals and creative assets. [daa2070d28bf]
16. **Give Smart Bidding a value signal and room to learn.** Report conversion values before Target ROAS. Start Target ROAS below current actual ROAS. Move from Maximize conversions to a target only after enough conversions. [4b56cb53eee4] [daa2070d28bf] [1990ef8e4d09]
17. **Creative throughput limits PMax and Demand Gen.** The source calls Demand Gen a "content monster"; if you stop feeding it fresh creative, "the entire stack starves". [1990ef8e4d09] [daa2070d28bf]

## 3. Procedures

### 3.1 Build the 4-layer account
1. Map the current account to the 4 jobs: net-new long-tail intent (AI Max for Search), full cross-channel conversion (PMax), top-of-funnel awareness (Demand Gen), ready demand (branded and non-branded Search). [61d89a7caa36]
2. Use Standard Search for head terms, competitor terms, and any query where you need tight control of ad copy and landing page pairing. Use AI Max for Search for long-tail, conversational and "AI Mode" queries that keyword campaigns cannot cover well. The source says these have the lowest competition and cheapest clicks. [61d89a7caa36] [verify UI] [web check: AI Max for Search availability and settings]
3. Add Standard Shopping for top-revenue SKUs and high-intent categories (source section 1.3) and brand plus high-intent category terms (source sections 1.7 and 4.3). [4eceae623d26] [6a480c2ffb47]
4. Set role rules before launch (3.2). The source gives no launch order for the layers.
5. Check campaign-type availability and behaviour in the live interface before restructuring. [61d89a7caa36] [verify UI]

### 3.2 Stop PMax cannibalising brand and high-intent traffic (3 parallel actions)
1. Add branded negative keywords and brand exclusions to PMax campaigns so PMax cannot bid on branded queries. [4eceae623d26] [verify UI: where brand exclusions live, account or campaign level]
2. Add negative keywords (brand terms) to new-customer acquisition Search and Shopping campaigns so they do not absorb branded demand. [4eceae623d26] [9c25700ad918]
3. Create dedicated branded Search and Shopping campaigns that collect only branded traffic. [4eceae623d26]
4. Give brand campaigns budget that is uncapped relative to search volume. Judge them on ROAS, CPC and impression share, not growth. [4eceae623d26] [9c25700ad918]
5. Duplicate the feed with role rules: Shopping feed tuned for brand and high-intent category terms; PMax feed tuned for discovery and scaling. The source does not say how to build the 2 feeds or which rules to use. [4eceae623d26] [6a480c2ffb47] [verify UI]
6. Expect blended account ROAS to look worse after the split; the source (via card caveat) says that is the intended transparency gain. [4eceae623d26] [9c25700ad918]

### 3.3 Feed-only PMax (source version, with the card's correction)
Source steps:
1. Build a PMax campaign with zero manually added assets: no headlines, descriptions, images or videos. [2fcfa24a9f1f]
2. Explicitly turn off Google's auto-generation features, or the system scrapes your site to make assets. [2fcfa24a9f1f] [verify UI: asset automation settings]
3. Use it when: (a) the main goal is Shopping placement; (b) you lack strong video or lifestyle images; (c) you need strict budget separation between Shopping spend and YouTube/Display spend; or (d) an existing PMax over-spends on low-value networks and misses ROAS targets.

Card version (editorial correction, prefer this when acting):
1. Confirm Merchant Center link, eligible products, correct prices and stock, and tested purchase-value tracking. [2fcfa24a9f1f]
2. Treat feed-only as a test of less manual creative, not as a Shopping-only switch. Check actual asset-generation and URL-expansion settings in the current interface. [2fcfa24a9f1f] [verify UI]
3. Watch channel delivery, product performance, and new vs returning customer results. Compare contribution and acquisition cost against the existing Shopping or full-asset PMax. [2fcfa24a9f1f] [needs brand data: product margins, new vs returning split]
4. Do not call it remarketing-only and do not promise Shopping-only delivery. The card cites Google Help: audience signals do not restrict targeting, and Merchant Center data can generate assets automatically. [2fcfa24a9f1f] [web check: support.google.com/google-ads/answer/14530785 and answer/15865151]

### 3.4 PMax levers you control
1. URL expansion: use URL-contains rules to limit landing pages, or turn final URL expansion off. [verify UI]
2. Audience signals: add first-party data, Customer Match lists and custom segments to guide (not restrict) the algorithm. [needs brand data: customer lists with consent]
3. Placement exclusions: account-level placement exclusions now cover PMax (source says expanded August 2026). [verify UI] [web check: PMax placement exclusion scope]
4. Split PMax by intent: 1 prospecting PMax with broad signals and a high-priority feed, plus 1 PMax for remarketing or brand defence with different asset groups and audience signals. Source reason: cleaner learning, and prospecting is not starved of data by brand-driven conversions. [6a480c2ffb47] (Note the tension with 3.2 step 1; see section 9.)

The source gives no card id for the 3 levers paragraph in section 1.4; the placement and URL points appear only in the source text and in [2fcfa24a9f1f] as settings to review.

### 3.5 Standard PMax asset groups
1. Per asset group: at least 15 high-quality images and 5 video variations (source attributes this to "Google's creative playbook"). [daa2070d28bf] [web check: current Google PMax asset recommendations]
2. Headlines: minimum 3, maximum 15, each up to 30 characters, at least 1 of 15 characters or fewer. [verify UI]
3. Refresh creative every 4 to 6 weeks. [daa2070d28bf]

### 3.6 Set up Demand Gen as the assist layer
1. Build separate campaigns for prospecting and remarketing; they need different creative and bids. [1990ef8e4d09]
2. Optional: split by placement type (Shorts-only, in-stream-only, image surfaces) to isolate results. [1990ef8e4d09] [verify UI]
3. Start on Maximize conversions. After about 50 conversions, move to Target CPA or Target ROAS. The source does not say whether the 50 are per campaign or over what window. [1990ef8e4d09]
4. Let campaigns run at least 30 days before changing them. [1990ef8e4d09]
5. Use Reach Planner or Performance Planner for bid and budget suggestions. Before scaling, use the in-UI tCPA Scaling Simulator to forecast traffic from bid increases. [1990ef8e4d09] [verify UI]
6. On always-on campaigns, raise bids 5% to 10% (never more than 15%) every 5 to 7 days. Do not make 1 large change. [1990ef8e4d09]
7. Keep a steady creative supply; the source gives no number of new creatives per week. [1990ef8e4d09]
8. Confirm current inventory before planning creative. Source list as of August 2026: YouTube Shorts, in-feed, Home feed, watch-next, YouTube Search, Discover, Gmail, and (source section 1.5 and appendix) Google Maps and the Display Network. [1990ef8e4d09] [web check: Demand Gen placements]

### 3.7 Merchant Center feed titles
1. Use the order: Product Type, then Material, then Colour, then Fit/Size, then Key Feature, then Brand last. [76f0f732dbe5]
2. Put the attributes buyers type in the first ~70 characters; the source says Google weights these most for matching. [76f0f732dbe5]
3. Keep titles 60 to 150 characters. Text after ~70 characters is supplementary. [76f0f732dbe5]
4. Do not keyword-stuff; the source says Google penalises unnatural attribute density. [76f0f732dbe5]
5. For some verticals the source allows: Brand, then Product Type, then Key Feature, then Model, then Colour/Size. It does not say which verticals. [76f0f732dbe5]
6. Whatever order you pick, apply the same order across the whole catalog. [76f0f732dbe5]
7. Use a supplemental feed to override titles, product types and custom labels without touching the site or primary feed. Use it to test title variants, add promotional labels and isolate product sets for campaign roles. Channable and similar tools can sync titles into Merchant Center this way. [76f0f732dbe5] [verify UI]
8. Re-audit the feed when you add categories or price tiers. [7671c6e57a6e]
9. The source gives no method to measure a title test (no metric, no duration). [needs brand data: product-level impressions, clicks and conversion value before and after title changes]

### 3.8 Merchant Center diagnostics and disapproval fixes
1. Open Merchant Center, then Products, then Diagnostics. Issues are grouped by severity. [9972bf6ca8cf] [verify UI]
2. Filter "Disapproved" first. These products cannot show in any Shopping ad or free listing: immediate revenue loss. [9972bf6ca8cf]
3. Then filter "Warnings" and "Limited performance". These are approved but held back: optimisation work. [9972bf6ca8cf]
4. Check the Item Issues tab for affected SKUs; use "View & edit" for manual fixes. [9972bf6ca8cf] [verify UI]
5. Use the "Fix type" filter to isolate auto-fixable items (formatting errors, missing optional attributes), select all, run Autofix. [9972bf6ca8cf] [verify UI]
6. Fix by hand: policy violations, price mismatches, missing required attributes. [9972bf6ca8cf]
7. The source says every change made in the Merchant Center interface is reversible within 30 days. [9972bf6ca8cf] [web check: 30-day reversal claim]
8. Prevent: pre-validate the catalog against Google's specs before upload (source names SmartFeed and Feedonomics). [9972bf6ca8cf]
9. If prices change often: update the feed at least every 6 hours and turn on automatic item updates so Google can use crawled prices when the feed lags. [9972bf6ca8cf] [verify UI]

### 3.9 Five gates before scaling spend
Pass all 5 in order before raising budget. [daa2070d28bf]
1. Feed health clean: no disapprovals; warnings and limited-performance items worked down (the source says they are suppressed in discovery surfaces).
2. Tracking validated end to end: enhanced conversions active, server-side tags firing, conversion values accurate. [needs brand data: backend orders and revenue to reconcile against Google conversions]
3. Brand and non-brand in separate campaigns with separate budgets and separate reporting.
4. Creative throughput: PMax 15+ images and 5+ videos per asset group, refreshed every 4 to 6 weeks; Demand Gen continuous refresh.
5. Bid strategy maturity: about 50 conversions a month for basic stability, more in competitive auctions. Move from Maximize conversions to Target CPA or Target ROAS only after this.

The source gives no scaling step size for Search, Shopping or PMax budgets. The only step rule is the Demand Gen bid rule in 3.6 step 6.

### 3.10 GTM conversion tracking (web container)
1. Conversion Linker tag, firing on All Pages in most cases. [56853873c2c8] [verify UI]
2. GA4 Event tag for the key event: a recommended name (purchase, generate_lead, sign_up) or a custom event. [56853873c2c8]
3. Google Ads Conversion Tracking tag that fires on the key event, using the Conversion ID and label from Google Ads. [56853873c2c8] [verify UI]
4. For product feed clicks, set tracking in the Google Ads tracking template, not as hard-coded parameters in Merchant Center. [56853873c2c8] [verify UI]
5. Validate end to end before scaling; a misfiring purchase tag teaches bidding the wrong outcome (card step). [56853873c2c8]

### 3.11 Enhanced conversions
1. In GTM, open the Google Ads Conversion tag and turn on "Include user-provided data". [f866b580a9ae] [verify UI]
2. Map data layer variables for email, phone and address collected at checkout or on the lead form. The tag hashes them and adds them to the conversion ping. [f866b580a9ae] [needs brand data: which checkout fields the store's data layer exposes]
3. For lead conversions, data usually comes from lead form submits and is matched to offline conversion imports (low relevance for a pure store). [f866b580a9ae]
4. Know the 2026 changes the source reports: from April 2026, Google accepts user-provided data from tags, Data Manager and API at the same time; from June 2026, enhanced conversions for web and for leads are 1 on/off setting and method choices are gone from the UI. [f866b580a9ae] [web check: enhanced conversions 2026 changes] [verify UI]
5. Work through Google's enhanced conversions implementation checklist before launch. [f866b580a9ae]
6. After launch, open the enhanced conversions diagnostics report. [f866b580a9ae] [verify UI]
7. Card caveat: send customer data only with valid consent and a lawful basis. [f866b580a9ae]

### 3.12 Server-side GTM
1. Host a server container on a cloud provider (Google Cloud, Stape or similar). [966cf63d89ec]
2. Add a GA4 client to receive events. [966cf63d89ec]
3. Add the Google Ads Conversion Tracking tag with the correct conversion ID and label to forward conversions. [966cf63d89ec] [56853873c2c8]
4. Add a Conversion Linker tag in the server container too. [966cf63d89ec]
5. After migration, check conversions on both the browser and server paths and reconcile with backend order counts (card step, not in source text). [966cf63d89ec] [needs brand data: backend order counts]
6. Monitor the container; if it fails, conversions stop recording (card caveat). [966cf63d89ec]

### 3.13 Intent-tiered keyword research
1. Tier 1, transactional: highest bids, most specific landing pages. Source examples are software patterns ("[category] software", "[category] pricing", "[category] for [industry]"). [e8f1dbe974c5]
2. Tier 2, comparison: "[competitor] alternative", "[your category] vs [competitor]". Comparison ad copy and landing pages. Separate ad groups or campaigns so each is bid and measured alone. [e8f1dbe974c5]
3. Tier 3, problem-aware: broader, higher volume, pain-point terms. Lower conversion rate. Tightest negative keyword coverage, lowest starting bids. [e8f1dbe974c5]
4. Tier 4, competitor: rival product names. Own budget cap. Judge on its own conversion rate, not blended. [e8f1dbe974c5]
5. Build long-tail clusters on purpose across markets, angles and variations. [e8f1dbe974c5]
6. Adapt the query patterns to physical-product language; the source's examples are SaaS (card caveat). [e8f1dbe974c5] [needs brand data: search terms report, product categories]

### 3.14 Pick and set a value bid strategy
1. Report revenue or values with conversions first. Without them Target ROAS has nothing to optimise. [4b56cb53eee4]
2. Choose Target ROAS when you need a return floor across a campaign or portfolio, and when order values vary a lot (source example: a $200 order vs a $20 order). [4b56cb53eee4]
3. Choose Maximize conversion value when you want the most value within a set budget and accept lower marginal ROAS for more volume (growth phase). [4b56cb53eee4]
4. When setting Target ROAS, start 10% to 15% below current actual ROAS. [4b56cb53eee4] [needs brand data: current actual ROAS per campaign over a stable window]
5. Once stable, step the target up in small increments. Watch impression share and conversion volume. The source gives no step size or wait time. [4b56cb53eee4]
6. Use seasonality adjustments only for short (1 to 7 day) conversion rate jumps from unusual causes such as a promotion. Not for holidays or back-to-school, not for over 7 days. [44615a608690] [verify UI]

### 3.15 Portfolio bid strategies
1. Use when several campaigns share 1 goal (source examples: 700% ROAS, $50 CPA), when you want automatic budget shifts across them, when you need bid caps or floors (source says these exist only in portfolio bidding, even for 1 campaign), or when you want a Max CPC cap against spikes. [e5678cb19768] [verify UI]
2. Available strategies in a portfolio per source: Target ROAS, Target CPA, Maximize conversions, Maximize conversion value, Maximize clicks, Target impression share. [e5678cb19768]
3. Do not use when goals differ (awareness vs conversion), when you need manual per-campaign bids, or when campaigns are too low-volume to benefit from pooled learning. [e5678cb19768]
4. MCC-level: if every account in the MCC uses the same currency, you can pool campaigns from several countries in 1 portfolio. The source says this helps small markets that lack conversion volume alone. [e5678cb19768] [verify UI]

## 4. Rules, thresholds and numbers

| Rule | Number or threshold | Condition | Source's basis | Card id |
|---|---|---|---|---|
| Account size for the 4-layer model | $50K to $500K a month | Ecommerce advertisers the source calls "highest-performing" | Assertion | [61d89a7caa36] |
| PMax average CPC | about $0.68 vs $0.85 Google Ads overall | "Average across accounts" | Unsourced average | none (text only) |
| PMax average conversion rate and ROAS | 2.4% and 4.1x | "Average across accounts" | Unsourced average | none (text only) |
| PMax images per asset group | at least 15 | Standard (non feed-only) PMax | "Google's creative playbook" | [daa2070d28bf] |
| PMax videos per asset group | at least 5 | Standard PMax | Same | [daa2070d28bf] |
| PMax creative refresh | every 4 to 6 weeks | Standard PMax | Same | [daa2070d28bf] |
| PMax headlines | min 3, max 15, 30 characters each, at least 1 of 15 characters or fewer | Standard PMax | Platform spec as stated | none (text only) |
| Demand Gen switch from Maximize conversions | after about 50 conversions | Then move to tCPA or tROAS | Source heuristic | [1990ef8e4d09] |
| Demand Gen minimum run before iterating | 30 days | All Demand Gen campaigns | Source advice | [1990ef8e4d09] |
| Demand Gen bid increases | 5% to 10%, max 15%, every 5 to 7 days | Always-on campaigns | Source advice | [1990ef8e4d09] |
| Demand Gen product feed size | at least 50 approved products; larger catalogs benefit up to 10,000 | Demand Gen with product feeds | Stated as guidance | [6a480c2ffb47] |
| Minimum products per campaign | 1 supported; at least 4 recommended | "Maximise eligibility across all ad placements" | Stated as platform guidance | [6a480c2ffb47] |
| Catalog too small to scale | under 30 SKUs | Shopping and PMax "at scale" | Source heuristic | [6a480c2ffb47] |
| Hybrid budget split | PMax 70% to 80%, Standard Shopping 20% to 30% | Hybrid PMax plus Shopping for ecommerce | Source's "optimal" structure, no data | [6a480c2ffb47] |
| Shopping coverage case | 49% to 57% in 1 month | After feed duplication with strict role separation | "A documented case study", not cited | [6a480c2ffb47] |
| Brand share distortion | brand ~11% of search spend, ~34% of conversions | "In many accounts" | Observation, not a target | [9c25700ad918] |
| Ad Rank worked example | $3 x QS 10 = 30 beats $5 x QS 5 = 25 | Simplified formula | Arithmetic illustration | [98dc5116df92] |
| Top-of-page Ad Rank | about 6 to 10 | Brand-new accounts, 2026 | Source heuristic, not Google figure | [98dc5116df92] |
| Top-3 Ad Rank | about 30 | Mid-competitive markets | Source heuristic | [98dc5116df92] |
| #1 position Ad Rank | 50 or higher "usually" | Not stated | Source heuristic | [98dc5116df92] |
| Brand keyword Quality Score | 9+ "typically" | Brand owner on own brand terms | Source heuristic | [98dc5116df92] |
| Quality Score build-up | 1 base + up to 3.5 expected CTR + up to 3.5 landing page + up to 2.0 ad relevance | 2026, approximate | Unpublished weighting | [1267e0489b18] |
| Quality Score weights | expected CTR ~39%, landing page ~39%, ad relevance ~22% | Same | Same | [1267e0489b18] |
| Actual CPC formula | (Ad Rank below you / your QS) + $0.01 | Simplified; a competitor exists below you | Operator simplification | [1b89e99face8] |
| Seasonality adjustment window | 1 to 7 days only | Unusual, short conversion rate change (e.g. promotion) | Source rule | [44615a608690] |
| Title length | 60 to 150 characters; match weight in first ~70 | Merchant Center titles | Operator heuristic | [76f0f732dbe5] |
| Feed update frequency | at least every 6 hours | Dynamic pricing | Source advice | [9972bf6ca8cf] |
| Merchant Center change reversal | within 30 days | Changes made in the GMC interface | Stated as fact | [9972bf6ca8cf] |
| Server-side GTM | "increasingly the default" above $50K a month | Spend tier | Heuristic | [966cf63d89ec] |
| Starting Target ROAS | 10% to 15% below current actual ROAS | Setting tROAS | Source heuristic | [4b56cb53eee4] |
| Smart Bidding data floor | about 50 conversions a month, more in competitive auctions | Before scaling or moving to a target | Source heuristic | [daa2070d28bf] |
| Portfolio Max CPC case | CPC spikes to $25; cap $9; goal $30 CPA | B2B tCPA example | Illustration | [e5678cb19768] |
| Video length caps | see section 6 table | By format | Platform spec as stated | [98fda8f0ce74] |

All $ figures are USD. Convert to the brand's currency and market before use. [needs brand data: currency and market CPC levels]

## 5. Diagnostics and checks

1. **Is PMax eating brand?** Check: brand exclusions and brand negatives on PMax; dedicated brand campaigns exist; brand negatives on acquisition campaigns. Good: brand queries land only in brand campaigns. Bad: PMax or non-brand Shopping reports brand queries, or account ROAS stays suspiciously stable. Fix: 3.2. [4eceae623d26] [9c25700ad918] [verify UI: where PMax search term data is shown]
2. **Is non-brand really profitable?** Check: split spend, conversions and value by brand vs non-brand. Compare to the source's "many accounts" pattern (brand ~11% of spend, ~34% of conversions) only as a flag, not a target. Good: non-brand clears the brand's break-even ROAS on its own. Bad: non-brand only looks fine when blended. Fix: cut or rebuild non-brand; keep brand uncapped. [9c25700ad918] [needs brand data: break-even ROAS from margin, spend and value by brand vs non-brand]
3. **Why does a higher bid not win position?** Check expected CTR, ad relevance, landing page experience and assets for that keyword. Good: all rated well and assets active. Bad: a low component. Fix: improve that component before raising bids. [2d82081ef51f] [1267e0489b18] [verify UI: Quality Score component columns]
4. **Which Quality Score component to work on?** Expected CTR low: ad copy tests, assets, match type refinement, query-to-ad alignment. Ad relevance low: tighter ad group themes, keyword-to-copy match, landing page content on the query's intent. Landing page low: load speed, mobile, content relevance, ease of finding the conversion action. [1267e0489b18]
5. **Feed health.** Check Merchant Center Diagnostics. Good: zero disapproved; warnings and limited-performance shrinking. Bad: disapprovals from GTIN, price mismatch, missing shipping, policy, formatting or missing required attributes. Fix: 3.8. [9972bf6ca8cf] [verify UI]
6. **Price mismatch risk.** Check feed update frequency and automatic item updates when prices change often. Good: feed refreshed at least every 6 hours; automatic item updates on. [9972bf6ca8cf]
7. **Title check.** Good: product type and searched attributes in the first ~70 characters, 60 to 150 characters, same order across the catalog, no stuffing. Bad: brand plus model name first, attributes past 70 characters, mixed orders. [76f0f732dbe5]
8. **Tracking integrity.** Check: Conversion Linker on all pages; GA4 key event and Ads conversion tag fire on purchase with correct ID, label and value; enhanced conversions diagnostics report clean; server path firing if used; Google conversions reconciled with backend orders. Bad: missing or wrongly formatted user data, wrong in-page code, data layer variable mismatch (the 3 common problems the source names). [56853873c2c8] [f866b580a9ae] [966cf63d89ec] [needs brand data: backend orders]
9. **Undercounted conversions vs backend.** First suspects per cards: enhanced conversions not active or misformatted; browser restrictions blocking tags (consider server-side). [f866b580a9ae] [966cf63d89ec]
10. **Target ROAS starving delivery.** Symptom: low spend and falling impression share after setting a target. Likely cause per source: target set too high on a cold campaign. Fix: reset to 10% to 15% below actual ROAS, then step up. [4b56cb53eee4]
11. **Feed-only PMax check.** Check channel delivery and whether auto-generated assets appeared. Good: most spend on Shopping placements with contribution at or above the Shopping baseline. Bad: spend on low-value networks. Fix: review asset automation, URL expansion and placement exclusions. [2fcfa24a9f1f] [verify UI]
12. **Scale readiness.** Run the 5 gates in 3.9. Any gate failing: do not raise budget. [daa2070d28bf]
13. **Portfolio fit.** Good: same goal, enough combined conversions. Bad: mixed goals or tiny volume dragging the pool (card caveat). [e5678cb19768]
14. **After removing Demand Gen.** Watch branded search and branded conversions for weeks, not days, because the source claims a lagged drop. [61d89a7caa36] [needs brand data: weekly branded search volume and conversions]

## 6. Tools, settings and named features

- **AI Max for Search.** Search mode for long-tail, conversational and AI Mode queries. [61d89a7caa36] [verify UI] [web check: AI Max availability and controls]
- **Standard Search.** Keywords, match types, negative lists, manual or Smart Bidding. [verify UI]
- **Standard Shopping.** Product group bids, query-to-product visibility; source says Maximize conversion value without tROAS added July 2026. [4b56cb53eee4] [web check]
- **Performance Max.** Serves Search, Shopping, YouTube, Display, Discover, Gmail, Maps and "now Waze". Controls named: URL expansion (URL-contains rules or off), audience signals (first-party data, Customer Match, custom segments), account-level placement exclusions, brand exclusions, asset auto-generation toggles. [2fcfa24a9f1f] [4eceae623d26] [verify UI] [web check: Waze as a PMax surface]
- **Demand Gen.** Image and video across YouTube (Shorts, in-feed, Home, watch-next, YouTube Search), Discover, Gmail, Maps, Display. Replaced Discovery campaigns; absorbed Video Action campaigns (paused and archived 28 Feb 2026). 6 bid options: Target CPA, Target ROAS, Target CPC, Maximize conversions, Maximize conversion value, Maximize clicks. [1990ef8e4d09] [98fda8f0ce74] [verify UI]
- **Planning tools.** Reach Planner, Performance Planner, in-UI tCPA Scaling Simulator. [1990ef8e4d09] [verify UI]
- **YouTube formats** (as stated by source) [98fda8f0ce74] [verify UI]:

| Format | Placement | Length | Best for | Campaign types |
|---|---|---|---|---|
| Skippable in-stream | YouTube videos, GVP interstitials | No limit (3 min or less recommended) | Consideration, TrueView views | Demand Gen, Video View, Video Reach, PMax |
| In-feed | YouTube Home, Search, Watch Next | No limit | Discovery-stage engagement | Same as above |
| Non-skippable in-stream | YouTube videos, GVP interstitials | 15 to 60 sec (varies) | Full message delivery | Not stated |
| Bumper | YouTube videos, GVP interstitials | 6 sec (5 sec min) | Frequency, awareness | Video Reach only |
| Shorts | Shorts feed | 60 sec or less recommended | Mobile engagement | Demand Gen, Video View, Video Reach, PMax |
| Masthead | YouTube home page | No limit (10 sec or more recommended) | Mass awareness (CPM/CPH) | Reservation only |

- **YouTube audio ads.** Source says restricted to Pandora/SiriusXM in the US from 1 Sep 2026, so not available for US targeting via Google Ads. [98fda8f0ce74] [web check]
- **Smart Bidding labels.** From June 2026: "Target CPA" and "Target ROAS" are standalone options, separate from untargeted Maximize conversions and Maximize conversion value. Behaviour unchanged. [44615a608690] [4b56cb53eee4] [verify UI]
- **Seasonality adjustments.** 1 to 7 day use only. [44615a608690] [verify UI]
- **Portfolio bid strategies.** Bid caps and floors, cross-campaign pooling, MCC-level pooling for same-currency accounts. [e5678cb19768] [verify UI]
- **Google Merchant Center.** Products, Diagnostics; Item Issues tab; View & edit; Fix type filter; Autofix; automatic item updates; supplemental feeds; custom labels. [9972bf6ca8cf] [76f0f732dbe5] [verify UI]
- **Feed tools named.** Channable (supplemental title sync), SmartFeed and Feedonomics (pre-validation). Suggestions, not requirements. [76f0f732dbe5] [9972bf6ca8cf]
- **Google Tag Manager.** Conversion Linker tag, GA4 Event tag, Google Ads Conversion Tracking tag, "Include user-provided data" option, server container with GA4 client. [56853873c2c8] [f866b580a9ae] [966cf63d89ec] [verify UI]
- **Server hosting named.** Google Cloud, Stape. [966cf63d89ec]
- **Enhanced conversions.** Single on/off switch from June 2026; Data Manager and API accepted with tags from April 2026; diagnostics report; implementation checklist. [f866b580a9ae] [verify UI] [web check]
- **Google Ads tracking template.** For product click tracking instead of Merchant Center parameters. [56853873c2c8] [verify UI]
- **Customer Match.** As a PMax audience signal. [needs brand data: consented customer list]

## 7. Examples and case results

All are examples, not promises.

- Ad Rank arithmetic: $3 bid x Quality Score 10 = 30 beats $5 bid x Quality Score 5 = 25. Illustration of the simplified formula. [98dc5116df92]
- Shopping coverage went from 49% to 57% in 1 month after feed duplication with strict role separation. "A documented case study", no brand, spend or link given. [6a480c2ffb47]
- Brand terms took about 11% of search spend and 34% of conversions "in many accounts". No sample given. [9c25700ad918]
- B2B advertiser on tCPA saw CPC spikes up to $25 on low-demand days; portfolio bidding with a $9 Max CPC cap kept it near a $30 CPA goal. B2B, not ecommerce; no result numbers after the change. [e5678cb19768]
- Order value spread: $200 vs $20 orders need different bid economics, used to justify Target ROAS. [4b56cb53eee4]
- Portfolio goal examples: 700% ROAS, $50 CPA. [e5678cb19768]
- PMax "averages": CPC about $0.68 vs $0.85 overall, 2.4% conversion rate, 4.1x ROAS. No source, sample or date. Do not use as benchmarks. (text only)

## 8. Mistakes the source warns about

1. Running PMax and Standard Shopping on the same feed without role rules, so PMax eats brand and high-intent traffic and you lose cost visibility. [4eceae623d26]
2. Blending brand and non-brand, which flatters ROAS and hides whether prospecting is subsidised. [9c25700ad918]
3. Capping brand budget and losing brand impression share to a competitor, "one of the most avoidable ways to lose pipeline". [4eceae623d26] [9c25700ad918]
4. Judging brand campaigns on growth metrics instead of ROAS, CPC and impression share. [9c25700ad918]
5. Treating the auction as a bidding war and answering lost position only with higher bids. [2d82081ef51f]
6. Over-investing in ad copy tests and under-investing in landing page relevance, speed and mobile. [1267e0489b18]
7. Treating the visible Quality Score as what the auction reads, or planning around max bid instead of actual CPC. [1267e0489b18] [1b89e99face8]
8. Manufacturer-style titles (brand plus product name) that push searched attributes past 70 characters. Keyword stuffing. Mixed attribute order across the catalog. [76f0f732dbe5]
9. Ignoring supplemental feeds ("the most overlooked lever in GMC"). [76f0f732dbe5]
10. Leaving disapproved products unfixed (immediate revenue loss) and relying on Autofix for policy or price issues. [9972bf6ca8cf]
11. Slow feed updates with dynamic pricing, causing price mismatch disapprovals. [9972bf6ca8cf]
12. Hard-coding tracking parameters in Merchant Center instead of using the Google Ads tracking template. [56853873c2c8]
13. Building feed-only PMax but leaving auto-generation on, so Google scrapes the site for assets. [2fcfa24a9f1f]
14. Setting Target ROAS without reported conversion values, or too high on a cold campaign, which starves delivery. [4b56cb53eee4]
15. Using seasonality adjustments for holidays, back-to-school or anything over 7 days. [44615a608690]
16. Making 1 large bid jump instead of 5% to 10% steps every 5 to 7 days (Demand Gen). [1990ef8e4d09]
17. Stopping creative refresh in Demand Gen, which the source says starves the whole stack. [1990ef8e4d09]
18. Cutting the Demand Gen assist layer and not linking the later branded drop to it. [61d89a7caa36]
19. Chasing head terms instead of building long-tail clusters. [e8f1dbe974c5]
20. Blending competitor-term campaigns into account results; they have lower CTR and higher CPC than brand. [e8f1dbe974c5]
21. Using portfolio bidding across different goals or very low-volume campaigns. [e5678cb19768]
22. Scaling before feed, tracking, brand split, creative supply and conversion volume are ready. "Scale amplifies feed problems; it does not solve them." [daa2070d28bf]
23. Trying to control PMax output distribution instead of fixing its inputs. [daa2070d28bf]

## 9. Caveats, conflicts and what is missing

**Likely generated or derivative.** Signs: no author; "compiled from" a list of outlets with no links; a clean table-of-contents manual shape with even-length sections; round unsourced averages (PMax $0.68 CPC, 2.4% CVR, 4.1x ROAS); precise-looking but unpublished formulas (Quality Score point weights, Ad Rank thresholds); SaaS and B2B content inside an ecommerce manual ("[category] software", "pricing", "pipeline", a B2B tCPA case); and phrasing close to common PPC blog posts. It reads as a synthesis, likely AI-assisted, not a primary source. It overlaps in topic with source 06 in this folder (not read here). Weight it below any primary practitioner source in pass 2, and do not count its agreement with source 06 as independent confirmation if 06 is its origin.

**Header does not match body.** The Drive header and "Topics" block describe content the body does not contain: a "DOJ-disclosed ad score formula" with predicted CTR and a penalty variable "beta", a 4-step retrieval, elimination, ranking, auction model, "up to 40% of clicks" from top positions, a lean PMax that removes Gmail, Display, Maps and Discover, and "keyword-stuffed titles" in surface-area scaling. The body instead says avoid keyword stuffing, defines surface area as catalog breadth plus feed duplication, and has none of the DOJ, beta or 40% material. The header seems written for a different document (possibly source 06). Do not cite header claims from this source. No card here carries them.

**Internal conflicts.**
- Quality Score: section 2.3 says the visible score is not an auction input, yet the Ad Rank and actual CPC formulas in 2.2 and 2.5 multiply and divide by "Quality Score". Read the formulas as teaching models of auction-time quality, not of the 1 to 10 number. [1267e0489b18] [98dc5116df92] [1b89e99face8]
- Brand in PMax: sections 1.7 and 4.2 say exclude brand from PMax; section 4.3 suggests a separate PMax "for remarketing or brand defence". The source does not reconcile these. [4eceae623d26] [6a480c2ffb47]
- Standard Shopping role: section 1.3 says top-revenue SKUs and high-intent categories with tROAS and manual bid levers; sections 1.7 and 4.3 say brand and high-intent category terms. Section 1.3 also says Shopping "now supports" Maximize conversion value, dated July 2026 in the appendix.
- The 50-conversion threshold: "after approximately 50 conversions" for Demand Gen (no time window) vs "approximately 50 conversions per month" in Gate 5. [1990ef8e4d09] [daa2070d28bf]
- Feed-only PMax (no assets, Shopping-first) sits beside Gate 4, which says scale requires 15+ images and 5+ videos per asset group. The source does not say whether feed-only campaigns are exempt from Gate 4.
- Title order: the "proven" structure puts brand last, then an alternative puts brand first "for certain verticals" without naming them.
- Gate 2 requires server-side tags firing, while section 3.6 frames server-side as "increasingly the default" above $50K a month. For a smaller account Gate 2 may be stricter than the source's own spend heuristic.

**Card corrections to the source.** Card [2fcfa24a9f1f] corrects the feed-only PMax claims: omitting assets does not guarantee Shopping-only delivery, audience signals do not restrict targeting, and Merchant Center data can create assets. Prefer the card when acting.

**Doubtful or unverifiable claims.** [web check: each] The 30-day reversal of any Merchant Center change; Waze as a PMax surface; the June 2026 bid strategy relabel; the April and June 2026 enhanced conversions changes; Demand Gen on Maps from May 2026; YouTube audio ads limited to Pandora/SiriusXM in the US; AI Max inventory claims ("billions of net-new search queries"); "Google Ads Conversion Tracking tag, the server-side tag" wording in the web container list (it is described as server-side while listed as a web container component); the Conversion Linker described as letting "Google Ads send data to Tag Manager" (unusual wording, check its actual role); the 70-character matching weight (card says not published by Google).

**Currency and market.** All money figures are USD and US-flavoured. CPCs, spend tiers ($50K a month) and the $0.01 CPC increment need translation for other markets. [needs brand data: currency, market, typical CPC]

**What is missing (thin on how).**
- No steps for building the duplicated Shopping and PMax feeds or the rules each should use.
- No method or metric for title tests (duration, success metric, sample).
- No budget scaling step size for Search, Shopping or PMax; no rule for how much to raise Target ROAS each step or how long to wait.
- No negative keyword list method, no match type guidance beyond naming them, no search terms review routine.
- No margin or break-even ROAS method; ROAS is used without profit. [needs brand data: product margins, shipping and return costs]
- No incrementality or lift testing, despite claims about assist-layer lag and brand cannibalisation.
- No consent or privacy steps beyond "hashed" (card adds the lawful-basis caveat).
- No guidance for small catalogs or small budgets other than the under-30-SKU warning.
- No evidence for any case result.

## 10. Card index

- [61d89a7caa36] Four-Layer Google Ads Account Model for Ecommerce
- [2fcfa24a9f1f] Feed-Only Performance Max for a Feed-Led Retail Test
- [4eceae623d26] Stop PMax and Shopping Cannibalising Brand Demand
- [1990ef8e4d09] Configure Demand Gen as the Assist Layer
- [98fda8f0ce74] Match YouTube Ad Formats to Funnel Stage
- [2d82081ef51f] How the Google Ads Auction Actually Works
- [98dc5116df92] Ad Rank Formula and Position Threshold Heuristics
- [1267e0489b18] Use Quality Score as a Diagnostic, Not a Currency
- [1b89e99face8] Second-Price Logic: Why Higher Quality Lowers Actual CPC
- [44615a608690] Smart Bidding Basics, Relabelling and Seasonality Adjustments
- [7671c6e57a6e] Treat the Product Feed as the Advertising Copy
- [76f0f732dbe5] Product Title Architecture for Feed Matching
- [9972bf6ca8cf] Feed Health Diagnostics and Disapproval Remediation
- [56853873c2c8] Conversion Tracking Tag Architecture via GTM
- [f866b580a9ae] Enhanced Conversions Setup and Diagnostics
- [966cf63d89ec] Server-Side Tracking for Page Speed and Data Durability
- [e8f1dbe974c5] Intent-Tiered Keyword Research Workflow
- [9c25700ad918] Brand vs Non-Brand Segmentation and ROAS Distortion
- [6a480c2ffb47] Surface-Area Catalog Scaling with Feed Duplication
- [4b56cb53eee4] Target ROAS vs Maximize Conversion Value
- [e5678cb19768] Portfolio Bid Strategies for Stabilised Scale and Bid Guardrails
- [daa2070d28bf] Five Gates Before Scaling Google Ads Spend
