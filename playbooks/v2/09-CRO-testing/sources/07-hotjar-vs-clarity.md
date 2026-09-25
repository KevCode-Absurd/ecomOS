# HotJar vs Microsoft Clarity: Which is Better For Your Website?

source_id: 1yY3I3VNfWb2BtD0j5_jj-E2erh0LUvJJ  |  folder: /09-CRO-testing  |  cards: 8  |  words: 1870  |  type: transcript (YouTube comparison video)
credibility: An unnamed presenter who runs "a conversion optimization firm and web design firm". Clients get 300,000 to 400,000 visitors per month. The firm was moving clients from Hotjar to Clarity at the time, mainly for cost. Evidence is the presenter's own client work: 1 Area map finding and 1 A/B test result (18% conversion lift) with no sample size, duration, confidence or baseline. Tool prices are quoted from the vendors' pages at the time. The presenter sells CRO and web design services, not either tool. The style and tool preferences (Area maps as a favourite feature) match source 04, but the transcript does not confirm it is the same person.
date signals: No year stated. "At the time of this recording Microsoft Clarity is completely free." Hotjar Plus at $32 per month for 100 daily sessions. Hotjar user interviews described as "a newer feature". Userbrain at $40 per tester. Pricing, plan limits and feature names are all time-sensitive. `[web check: current Clarity, Hotjar, Userbrain and Okendo pricing and limits]`
scope note: The source header places tool comparison, unbundled research stack and Area-map-based test design in 09-CRO. It routes GA4 funnel set-up and post-purchase surveys for marketing attribution to 06-MEA, and landing page redesign or copy changes to 07-LPG. It says to skip basic definitions of heatmaps, recordings and exit surveys, and pricing complaints without numbers.

## 1. What this source is for

It helps an operator choose behaviour-research tools for CRO and build a low-cost research stack. It compares Clarity and Hotjar feature by feature, names cheaper single-purpose tools for the jobs Clarity lacks (surveys, user tests, funnels), and gives 1 worked pattern for turning Area map data into an A/B test: find an element with high click share but low scroll reach, and move it up.

## 2. Principles

1. **For heatmaps and recordings, Clarity and Hotjar do "pretty much the exact same thing".** Both show recordings, scroll reach and clicks. Most behaviour tools are similar here. [9e1368a119b8]

2. **Cost at your traffic decides it when you only need heatmaps and recordings.** Clarity was free with no data limit at recording time. Hotjar charges by daily sessions and bills rise fast at high traffic. For clients with 300,000 to 400,000 monthly visitors, the firm was moving to Clarity "solely for that reason". For small stores, the presenter says you want to "extract as much value from your traffic" as possible, so Clarity also wins on collecting all the data. Condition: verify current terms. [9e1368a119b8] [3728f5d4ae33]

3. **Clarity's Area maps are easier to act on than Hotjar's Engagement Zones.** Area maps give the exact share of clicks on each region or element (example: 5.9% of clicks on one area; navigation clicks) and let you dissect specific elements. Engagement Zones show engagement as a spectrum, which the presenter finds harder to interpret. The card says this is an interpretation preference, not proof one dataset is more accurate. [9e1368a119b8]

4. **High click share plus low scroll reach means placement is hiding real demand.** If an element is one of the most clicked on the page even though few people scroll to it, move it up. "If people are clicking here there must be something to it." Card caveat: some clicks can reflect confusion, so check recordings. [de4dfe536e94] [3043da84ee0c]

5. **Read scroll depth and clicks together.** Scroll tells you what shoppers saw; clicks tell you what they tried to use. High clicks on a low-reach module suggest suppressed demand. Low clicks on a highly visible module suggest weak relevance, unclear affordance, or a less important need (card interpretation). Add recordings for sequence and context. [3043da84ee0c]

6. **Hotjar's real advantages are surveys, user interviews and funnels in one place.** Choose Hotjar when an all-in-one platform is worth the cost, knowing surveys and feedback are a separately paid component. [9e1368a119b8] [3728f5d4ae33]

7. **Unbundle when you can run several tools.** Clarity for heatmaps and recordings; Okendo for Shopify surveys; Userbrain for remote user tests; GA4 Explore for funnels. The presenter sees "no real downside" if you are fine using separate tools. Card caveat: the synthesis step across tools is essential, and centralised permissions and reporting may matter to some teams. [6e48c0e74fe7]

8. **Surveys are voice of customer.** Exit-intent surveys ask non-buyers what stopped them; post-purchase surveys ask buyers what motivated them and what almost stopped them. "You get a ton of insight from this." [f89dbadb9131]

9. **User tests show what heatmaps cannot.** Ask testers for first impressions on landing, then give real tasks (add a product to cart and check out; find the contact form on a B2B site). [f375f7ffb264]

10. **Do not pay for a funnel feature you already have.** GA4 Explore builds custom funnels (example: homepage → contact form → thank-you page for B2B). [382d08d3f6aa]

## 3. Procedures

### 3.1 Choose Clarity or Hotjar
1. List the research jobs you actually use: heatmaps, recordings, exit or on-site surveys, post-purchase surveys, task-based user testing, funnel analysis. [9e1368a119b8]
2. If you mainly need heatmaps and recordings: pick Clarity (free, no data limit at recording time). `[web check: Clarity current terms]`
3. If you want heatmaps, recordings, surveys, interviews and funnels in one tool and will pay for it: pick Hotjar, noting several features are paid separately.
4. Budget Hotjar at real traffic: get normal and peak daily sessions, compare with the plan allowance (source: Plus $32/month for 100 daily sessions), and add the separately priced survey and feedback component. `[needs brand data: daily sessions, normal and peak]` `[web check: Hotjar pricing]` [3728f5d4ae33]
5. Compare that total with the unbundled stack (3.2).
6. If migrating from Hotjar, first confirm Clarity meets privacy, data-retention and implementation needs, and keep or replace any Hotjar feature in active use (card). [3728f5d4ae33]

### 3.2 Build the unbundled research stack `[verify UI]`
1. **Heatmaps and recordings:** install Microsoft Clarity.
2. **Surveys (Shopify):** install Okendo. The source says it collects unlimited responses and that volume "depends on your order data", unlike Hotjar's response limits. `[web check: Okendo plan and limits]`
3. **Remote user testing:** use Userbrain, $40 per tester at recording time. `[web check: Userbrain pricing]`
4. **Funnels:** in Google Analytics 4, open the **Explore** tab and build a custom funnel. Funnel configuration and event validation belong in 06-MEA.
5. **Synthesis (card addition):** pull findings from recordings, surveys, user tests and funnel drop-off into one prioritised hypothesis backlog. [6e48c0e74fe7]

### 3.3 Area map to A/B test `[verify UI]`
1. Open Clarity heatmaps for the page and switch to the Area map view.
2. Read each region's share of total clicks, including navigation and in-page modules.
3. Open the scroll map for the same page and device, and note what share of visitors reach each module.
4. Flag modules with high click share but low reach. Source example: "shop by industry" section with 10.41% of clicks, reached by only 30 to 35% of visitors, "one of the highest clicked elements on the page".
5. Check recordings to confirm the clicks are intent, not confusion (card).
6. Write a narrow hypothesis: moving the same module higher will send more shoppers into collection pages earlier.
7. Test the move alone. Keep the module design and destination pages unchanged so the test isolates placement (card).
8. Judge on purchase conversion plus downstream collection and product page behaviour (card). Size the test properly (see source 05). [de4dfe536e94]

### 3.4 Set up exit and post-purchase surveys
1. Exit-intent or on-site survey for leaving visitors. Questions from the source: "What stopped you from buying?", "What almost stopped you from converting today?", "What's the reason you're exiting the site?"
2. Post-purchase survey right after the order. Questions: "What motivated you to buy from us today?", "Was there something on the site that almost stopped you from buying?"
3. Tool: Hotjar Surveys (paid add-on), or Okendo on Shopify.
4. Group answers into themes (card): product uncertainty, price, shipping, trust gaps, missing info, comparison needs, unclear fit.
5. Use motivations to strengthen persuasion; use near-miss objections to define friction tests (card).
6. Treat answers as hypothesis input and cross-check with recordings and funnel data (card). [f89dbadb9131]

### 3.5 Run a remote user test
1. Set up a study in Userbrain (or Hotjar's interview feature).
2. First prompt: "What are your first impressions upon landing on the site?"
3. Tasks: add a product to cart and check out (ecommerce); find the contact form (B2B). Card adds: find a suitable product.
4. Watch for breakdowns: missed navigation, misread product details, missed key info, hesitation at cart, checkout doubts (card).
5. Turn repeated patterns into hypotheses and test material changes live (card). [f375f7ffb264]

### 3.6 Build a GA4 Explore funnel `[verify UI]`
1. GA4 → **Explore** tab → create a funnel.
2. Define steps. Source example (B2B): homepage → contact form → thank-you page. Ecommerce version (card): product view → add to cart → begin checkout → purchase.
3. Confirm ecommerce tracking is configured before reading it (card).
4. Find the biggest or most costly drop and investigate it with recordings, surveys and user tests (card). [382d08d3f6aa]

## 4. Rules, thresholds and numbers

| rule | number or threshold | condition | source's basis | card id |
|---|---|---|---|---|
| Clarity price | free, no data limit | At recording time | Presenter | [9e1368a119b8] `[web check]` |
| Hotjar Plus | $32/month for 100 daily sessions; higher tiers cost more | At recording time | Vendor pricing quoted | [3728f5d4ae33] `[web check]` |
| Hotjar surveys and feedback | separate paid component | At recording time | Presenter | [3728f5d4ae33] |
| Traffic where Hotjar gets costly | 300,000 to 400,000 visitors/month (firm's CRO clients) | Example | Presenter's clients | [3728f5d4ae33] |
| Userbrain | $40 per tester | At recording time; card notes it is unclear if per study or per session | Presenter | [f375f7ffb264] `[web check]` |
| Okendo survey responses | unlimited; tied to order data | Shopify only | Presenter | [6e48c0e74fe7] `[web check]` |
| Area map example click share | 5.9% on one region | Illustration | Presenter demo | none (text only) |
| High-click, low-reach pattern | 10.41% of clicks, 30 to 35% reach | One client example; no threshold | Presenter's client | [de4dfe536e94] |
| Test result from moving the module up | 18% conversion lift | One test; no sample, duration, confidence, or absolute vs relative stated | Presenter's client | [de4dfe536e94] |
| Click-share or reach threshold for testing | none given | Use real traffic and sizing | None | [de4dfe536e94] |

## 5. Diagnostics and checks

| check | how | good | bad | next step |
|---|---|---|---|---|
| Tool fit | List research jobs used vs paid | Paying only for jobs in use | Paying for bundled features nobody uses | Unbundle or downgrade [9e1368a119b8] |
| Hotjar coverage | Daily sessions vs plan allowance | Plan covers normal and peak traffic | Session cap samples a small share, or bill balloons | Move heatmaps and recordings to Clarity [3728f5d4ae33] |
| Hidden demand | Area map click share vs scroll reach | High-click elements sit where most people reach | High click share, low reach (10.41% vs 30 to 35%) | Test moving the element up [de4dfe536e94] |
| Visible but ignored | Clicks vs reach | Visible modules get clicks | Highly visible module with low clicks | Check relevance and affordance; consider removing (card) [3043da84ee0c] |
| Confusion clicks | Recordings of high-click elements | Clicks lead to progress | Clicks lead to repeats, exits | Treat as a friction problem, not demand [3043da84ee0c] |
| Survey gaps | Is there an exit and a post-purchase survey? | Both live | Neither | Set up 3.4 [f89dbadb9131] |
| Funnel drop | GA4 Explore funnel | Steady progression | Sharp drop at one step | Investigate that step with qual tools [382d08d3f6aa] |
| Tracking health | Funnel events vs orders | Consistent | Missing or inconsistent events | Fix tracking first (06-MEA) [382d08d3f6aa] |

## 6. Tools, settings and named features

All `[verify UI]` and `[web check: current pricing and features]`.

- **Microsoft Clarity:** recordings, heatmaps (click, scroll), **Area maps** with click share per region and element. No surveys, interviews or funnels (per source). Free, no data limit (at recording time).
- **Hotjar:** recordings, heatmaps; **Map types → Engagement zones** (on the right side of the heatmap view); **Surveys** tab with sample templates (exit intent, post-purchase), paid separately; **User interviews** (newer feature); **Funnels** (custom navigation funnels). Plus plan $32/month for 100 daily sessions.
- **Okendo:** Shopify app for on-site and post-purchase surveys, unlimited responses tied to order data.
- **Userbrain:** remote user testing, $40 per tester.
- **Google Analytics 4 → Explore:** custom funnels.

## 7. Examples and case results

- **"Shop by industry" move (client):** 10.41% of homepage clicks went to a "shop by industry" section further down the page that only 30 to 35% of visitors reached. The team ran "a simple A/B test", putting the same icons at the top of the homepage to send people into collection pages. Reported result: 18% increase in conversions "just from that one A/B test". No sample, duration, confidence or absolute vs relative definition given. Example only. [de4dfe536e94]
- **Hotjar to Clarity migration (in progress):** the firm was moving CRO clients with 300,000 to 400,000 visitors per month to Clarity for cost. No before/after business outcome reported. [3728f5d4ae33]

## 8. Mistakes the source warns about

- Paying Hotjar prices at high traffic just for heatmaps and recordings that Clarity gives free. [3728f5d4ae33]
- Paying for Hotjar survey, interview or funnel add-ons when Okendo, Userbrain or GA4 already cover them. [6e48c0e74fe7]
- Leaving a highly clicked element low on the page where few people reach it. [de4dfe536e94]
- Relying on engagement "spectrum" views when an exact click share is available (presenter preference). [9e1368a119b8]
Card additions:
- Choosing a tool from its feature list instead of the jobs you do and your traffic cost. [9e1368a119b8]
- Treating every high-click element as demand; some are confusion. [3043da84ee0c]
- Changing the module design and its position in the same test. [de4dfe536e94]
- Mixing attribution post-purchase surveys (06-MEA) with CRO research surveys. [f89dbadb9131]

## 9. Caveats, conflicts and what is missing

- **All pricing is dated.** Clarity "free, no limit", Hotjar $32 for 100 daily sessions, Userbrain $40 per tester, Okendo unlimited. `[web check]` before any budget.
- **1 result, no statistics.** The 18% lift has no sample, runtime, confidence or definition. [de4dfe536e94]
- **No thresholds.** No click-share, reach, response-rate or participant-count guidance. [de4dfe536e94] [f89dbadb9131] [f375f7ffb264]
- **Survey bias** (card): exit surveys hear only those who answer; buyer surveys cannot explain non-buyers. [f89dbadb9131]
- **User tests are small qualitative samples**, not conversion estimates (card). No recruiting criteria or participant count given. Source 05 cites 5 to 8 people per task test. [f375f7ffb264]
- **Unbundling costs** (card): implementation effort, identity matching and cross-tool synthesis time are not addressed. [6e48c0e74fe7]
- **Okendo is Shopify-specific.** [6e48c0e74fe7]
- **Privacy and consent** for either tool are not covered. `[web check: consent and data-retention terms]`
- **No conflict with source 04.** Both favour Clarity Area maps and pairing clicks with scroll reach. Source 04 adds the Insights block and recording method; this source adds the tool comparison and the unbundled stack.
- **Consistent with source 06**, which lists Hotjar, Clarity and VWO Insights for heatmaps and Hotjar Surveys, VWO and Qualtrics for feedback, without choosing.
- **Neighbours:** GA4 funnel set-up and attribution surveys: 06-MEA; redesign and copy changes from findings: 07-LPG.

## 10. Card index

- de4dfe536e9476c056717bdf: Use Clarity Area Maps to turn hidden category demand into a homepage test
- 3043da84ee0cbf4d2f4bd3cf: Read scroll depth and clicks together before changing an ecommerce page
- 9e1368a119b81a90e9a58044: Choose Clarity or Hotjar based on the research capabilities your store actually needs
- 6e48c0e74fe77b590f2022ee: Build a lower-cost ecommerce research stack when an all-in-one tool is unnecessary
- f89dbadb9131e6dc051f86c6: Use exit and post-purchase surveys to separate purchase friction from purchase motivation
- f375f7ffb2646291caf4caa6: Run task-based remote user tests on the ecommerce purchase path
- 382d08d3f6aa300a0d0a0560: Use GA4 Explore funnels to locate purchase-path drop-off
- 3728f5d4ae337bf2286dd90d: Budget Hotjar at real traffic volume before adopting its bundled workflow
