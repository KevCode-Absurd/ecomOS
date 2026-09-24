# 06-MEA-measurement playbook

version: 2.0-draft  |  date: 24 Sep 2026  |  sources: 7 mini playbooks (6 independent voices: S01 and S07 are both Julius of Analytics Mania)  |  cards: 117  |  built from: sources/*.md

## 0. How to use this playbook

**Who runs it.** The measurement and data trust agent. Its job is to make every number the other agents use trustworthy before they use it. It sets up and audits GA4 and Google Tag Manager, checks ecommerce event coverage, checks the Meta pixel and Conversions API (CAPI) and their deduplication, judges server-side and gateway options, reads GA4 and Shopify reports without being fooled by them, reconciles platform purchases to store orders, keeps the brand's top metric fixed, and runs the daily trust check. It hands ad account structure to 24-DEP, Google Ads to 12-GAD, test design and significance to 09-CRO, landing page fixes to 07-LPG, email metrics to 14-EML, and P&L, COGS and contribution definitions to 20-FIN.

**ecomOS rules that override every source in this folder.**
1. ecomOS computes every metric in code, never in the model. Conversion rate, ROAS, funnel ratios, reconciliation gaps and trust scores come from a script or a calculator in `intelligence/`, with the inputs logged. The model may read and explain a number. It may not produce one. Sources S02, S05 and S06 do arithmetic out loud and get it wrong or unclear more than once (section 7, C13 and C14). That is the reason for this rule.
2. A missing or unsupported value shows as "unavailable", never as 0. GA4's "(not set)" means unknown, not zero (S03) [d54ee95e619b]. A blank Meta CAPI field means "not sent", not "0 sent". A Shopify metric the plan does not expose is "unavailable".
3. Period ROAS = total value ÷ total spend. Totals stay separate from breakdowns. Ad-level metrics stay ad-level when ads share an image. Dynamic or mixed creatives are flagged.
4. Meta is read-only. The Meta MCP exposes pixel and dataset write tools (`ads_pixel_event_create`, `ads_pixel_parameter_create` and similar). The agent never calls them. It reads (`ads_get_datasets`, `ads_get_dataset_quality`, `ads_get_dataset_stats`, `ads_pixel_event_read`) and writes a proposal for a human to apply.
5. Never print, paste or commit a pixel ID, dataset ID, CAPI access token, GTM container ID with credentials, or Metabase login. Source S04 stores a token in a text file and a GTM constant. ecomOS keeps tokens in `.env` or `secrets/` and never in a playbook, chat, page or commit.
6. Brands stay apart. Gehna's Meta account, Metabase sales and GA4 property are Gehna's. Peach Bucket and TrailFold data never mix with them. Every number in this playbook is a source's example, never a brand's.
7. Public web research stays separate from private business data. A `[web check]` result is a fact about a platform. It never contains brand data.

**Which sections to load for which task.**

| Task | Load |
|---|---|
| New GA4 property or GA4 audit | 3 groups B, C, D, E; P1 to P6; checklists 5.1, 5.2, 5.8; 6; 7 (C3, C4, C5) |
| Meta pixel and CAPI audit or build proposal | 3 groups G, H, I; P7 to P12; checklists 5.1, 5.3; 7 (C6, C7, C8) |
| Shopify store: what can and cannot be tagged | 3 group J; P2 step 0; 7 (C2); 10 |
| UTM and channel classification check | 3 group K; P17; checklist 5.4 |
| Attribution settings and platform conflicts | 3 group L; P18, P25; checklist 5.4; 7 (C9, C10) |
| Reconcile platform purchases to store orders | 3 group M; P21; checklist 5.5; 9.1 |
| Set or change the brand's top metric | 3 group N; P24; 7 (C11) |
| Read GA4 or Shopify reports for a decision | 3 groups F, O; P14 to P16, P19, P20; 6 |
| Daily trust check | 3 group P; P22; checklist 5.6; 9.3 |
| Onboard a new data source | P23; checklist 5.7; 9.3 |
| CAPI enrichment (gross profit, COGS) spec | 9.4; 3 group M; 20-FIN for field definitions |

**What the agent must fetch before acting.** Brand record: store platform, checkout domain, currency, time zone, selling countries and their consent rules, what installed the pixel and GA4, which Meta integrations are live, UTM convention, the chosen top metric, return rate. Data layer: store order export or Metabase for the same dates, GA4 purchase counts and revenue, Meta Events Manager counts and dedup status, Shopify Analytics figures, current GA4 admin settings. Web: current GA4 and Meta menu names before any `[verify UI]` step, current Shopify pixel and Google & YouTube app behaviour, current Meta dedup and event match quality guidance. Section 10 lists every item.

**How the sources were read.** S01 and S03 are generic GA4 beginner tutorials. Neither teaches ecommerce events (view_item, add_to_cart, begin_checkout, purchase with value, currency, items, transaction_id). S01 says this is out of scope 4 times [d6b4bece9591]. S03 stops at the Google tag [9bedc2d9534e]. Every GA4 ecommerce report rule below assumes the events arrive from the store platform, a developer or GTM and says so. S02 is a conceptual podcast with no formulas. S04 and S07 are Meta CAPI tutorials on demo sites that only send PageView and a contact form. S05 and S06 are single-store or single-agency Shopify report readings. No source covers event match quality, purchase deduplication by transaction_id, CAPI value enrichment, attribution windows, consent mode setup or BigQuery. Where this playbook states a rule none of the 7 sources states, it says "ecomOS rule" or "common practice" and carries a `[web check]`.

## 1. Scope and outcomes

**Covers.** GA4 account, property and stream structure. Install through GTM, a platform integration or hard code. Preview and DebugView testing. Day-1 GA4 settings (retention, domains, internal traffic, session timeout, Google Signals) and what to change or leave. Key events and why the purchase event, not a thank-you page view, is the sales key event. Ecommerce event coverage. Meta pixel plus CAPI through server-side GTM, with event ID dedup, consent gating and test event codes. The CAPI Gateway and what it cannot do. Shopify constraints on tagging. UTM discipline and channel grouping. Attribution model comparison and platform versus self-reported source conflicts. Reconciliation of GA4, Meta and Shopify purchase counts and revenue to store orders. Revenue definitions (net sales plus shipping charges, tax out, returns timing). Choosing 1 top metric and when to change it. Funnel ratios, bot checks and the sessions x conversion rate x AOV triage. Reading GA4 and Shopify reports without the common traps. Daily trust checks, trust scores and new-source onboarding.

**Does not cover.** Meta account structure, attribution window choice for buying, and campaign reads: 24-DEP. Google Ads conversion actions and Shopping: 12-GAD. Test design, sample size and significance: 09-CRO. Checkout and page fixes once a funnel leak is found: 07-LPG and 09-CRO. Cohort reading, LTV, CAC, contribution margin, COGS, cash conversion cycle and sell-through: 20-FIN (S06 raises them [37f16297a48e]; the formulas are not here). Email deliverability and per-send metrics: 14-EML. Store setup and theme code: a 05-SET folder that does not yet exist in v2; S01, S03 and S05 point there.

**Business measures it moves.** Fewer wrong budget decisions made on double-counted, bot-inflated or return-timed numbers (S06 return dip example; S04 double count before dedup). Faster decisions because 1 top metric and 1 source of truth per question are agreed (S02, S05). Higher share of Meta events matched and deduplicated (S04, S07; no source measures the lift). Less analyst time lost to numbers that later turn out wrong (S02: analytics must end in a decision).

## 2. Inputs the agent needs

| Input | From where | Required or optional | Why |
|---|---|---|---|
| Store platform, theme, checkout domain, whether checkout is hosted | Brand record | Required | Decides GTM vs native pixels (group J), cross-domain settings (R14) |
| Every domain a shopper touches from landing to thank-you page | Brand record, user | Required | 1 property per journey; Configure your domains (R8, R14) [60bd489184a8] |
| Business time zone and store currency | Brand record | Required | Property settings; changing time zone later breaks data (R10) [5c923d97e1f7] |
| Selling countries and the consent rules that apply | Brand record, `[web check]` | Required | Consent gating of pixel and CAPI, Google Signals decision (R52, R22) |
| What installed GA4 and the Meta pixel (app, theme code, GTM, developer), and which Meta integrations are live | Brand record, user, live site inspection | Required | Avoid double CAPI streams; decide if the gateway use case applies (R47, R57) |
| Current GA4 admin settings: retention, domains, internal traffic filter state, session timeout, Signals, key events list, custom definitions | Data layer (GA4 admin, `[verify UI]`) | Required | Settings audit (checklist 5.8) |
| GA4 ecommerce event list and parameters as they actually arrive (DebugView sample) | Data layer | Required | Event coverage check (checklist 5.2) [d6b4bece9591] |
| Meta Events Manager: events, browser vs server counts, dedup status, test events, dataset quality | Data layer (Meta MCP read tools) | Required | Dedup check (checklist 5.3) [8d023b8f223e] |
| Store orders for the same dates: count, net sales, shipping charges, tax, refunds by refund date and by order date, sales channel | Data layer (store admin export, Metabase, or platform API) | Required | Reconciliation (P21), revenue definition (R74), return timing (R75) [a3ae4e9e2a00] |
| GA4 purchase count and purchase revenue, transaction ID report | Data layer | Required | Reconciliation [2fa8beb663c8] |
| Shopify Analytics: sessions, conversion rate, AOV, funnel counts, sessions by location | Data layer | Required for Shopify stores | Triage and bot check (P19, P20) [9e9d4013f967] |
| GA4 sessions for the same dates | Data layer | Required | Bot check denominator (R61, R90) [084db9abd48b] |
| UTM convention and the campaign name list | Brand record | Required | Channel and campaign reads (group K) |
| The brand's chosen top metric (customers, revenue or profit) and the date it was set | Brand record, user | Required | Every report is framed on it (group N) [13ce65376d8f] |
| Return rate by month and by order month | Data layer | Optional, required for fashion or high-return categories | Return timing rule (R67) |
| Office, warehouse and agency IPs and whether they are static | Brand record | Optional | Internal traffic filter (R18) |
| Post-purchase survey answers ("how did you hear about us") | Data layer (survey tool) | Optional | Platform vs self-report conflict (P25) [45d7e49e638b] |
| Prior funnel step rates, engagement rate and landing page rates over several periods | Data layer | Optional | Baselines; the sources give almost no benchmarks (section 6) |
| Gross profit, COGS per SKU, shipping cost per order | Brand record, 20-FIN | Optional | CAPI enrichment spec (9.4) |
| Current GA4, Meta Events Manager, GTM and Shopify menu names | `[web check]` | Required before any `[verify UI]` step | Every UI path here is a 2025 or 2026 snapshot |

## 3. Decision rules

Each rule states the rule, its condition, the mini playbooks that support it (S01 to S07), conflicts, and card ids. Where only 1 source says it, the rule says "Source Sxx says". Where no source says it, the rule says "ecomOS rule" or "common practice" and carries a `[web check]`.

### Group A. Ground rules for any number

**R1. Every metric is computed in code, from logged inputs. The model never does the arithmetic.** Condition: always. Reason from the sources: S06's presenter calls a 5% AOV dip plus a 4% conversion dip "a 10% dip" (0.95 x 0.96 = 0.912, an 8.8% drop) [9e9d4013f967]; S02's presenter says $11,000 then corrects to $10,100 for a 1% lift [3a1918a526e2]; S05's transcript carries a 99.2% add-to-cart figure that cannot be right (R80) [000e5a39ddc8]. ecomOS rule. Supports: S02, S05, S06 by counterexample.

**R2. Missing, unsupported or thresholded values show as "unavailable", never as 0.** Condition: always, in every table, page and report. GA4 "(not set)" is unknown (S03) [d54ee95e619b]. An empty Monetization coupon or promotion card means the parameter is not sent, not that no coupons were used (S03) [2fa8beb663c8]. Empty age and gender means Signals is off, not that no data exists (S01, S03) [374c795a2291] [c01dc627e7b1]. ecomOS rule; supports: S01, S03.

**R3. Every report ends in a decision, even "keep doing the same thing".** Condition: any report the agent produces. Aim reports at open questions, not at metrics already understood. A report made to celebrate is not analytics. Source S02 says this [11a74e34ca53]. Show comparative series (revenue against AOV, profit, new customers and channel), never a single-line "revenue up month over month" chart [3a1918a526e2].

**R4. Pick 1 source of truth per question and write it down.** Condition: whenever 2 tools report the same thing. Use the store platform for order and sales totals, GA4 for traffic source, engagement and per-page conversion (S05) [1735fbb29aff]. Use GA4 or another session counter as the sessions denominator when Shopify sessions are suspect (S06) [084db9abd48b]. Use the store's payments or finance report for cash, not a sales report (S06 card) [a3ae4e9e2a00]. GA4 and Shopify numbers will differ; do not force them to match. Supports: S05, S06.

**R5. Start logging data before you know what it is worth.** Condition: any data point that might matter later (order attributes, survey answers, funnel step counts, refund dates). You cannot analyse history you never logged. Compute cost of acquisition before paid ads start, not after. Source S02 says this [776e59649374] [11a74e34ca53]. `[needs brand data: all acquisition cost lines before paid ads, and new-customer counts]`

**R6. Size analytics spend to the size of the decisions it can inform, counting analyst and decision-maker time.** Condition: any tool or headcount decision. S02's illustration: a $1M business makes $5K to $15K decisions from analytics; a $100M business makes $1M to $10M decisions. Illustrative, not a benchmark. Source S02 says this [11a74e34ca53].

### Group B. GA4 account, property and stream structure

**R7. 1 GA4 account per organization; 1 GTM account per organization.** Condition: 1 business. Set up another business in another account. Supports: S01 [a61d1986b945], S03 [5c923d97e1f7].

**R8. 1 property per user journey, not per website.** Condition: if a shopper moves across several of your domains before converting (main site, then a separate checkout domain), those domains share 1 property, and every one of them is listed under Configure your domains (R14). Give a site its own property only when it is a separate business line whose data you never want mixed. Supports: S01 [a61d1986b945] [60bd489184a8], S03 (usually 1 property per business) [5c923d97e1f7]. `[needs brand data: every domain a shopper touches from landing to thank-you page]`

**R9. 1 web data stream per property, even when several websites share it. Apps get their own streams.** Condition: web properties. S01 says Google "highly recommends" 1 web stream, and the domain typed at creation "does not matter much". S03 says 1 stream per site or app (website plus app = 2 streams). Conflict on wording only: S03 is describing web vs app, not several websites. Use S01's rule for several websites in 1 journey. Supports: S01 [a61d1986b945], S03 [5c923d97e1f7] [f2f53af85949].

**R10. Set reporting time zone and currency at creation to match the store and finance reports. Do not change time zone later.** Condition: property creation. A later time zone change causes a gap or overlap in data (S03). GA4 converts values sent in other currencies into the property currency (S03 example: AUD sent to a USD property shows as USD). Supports: S01, S03 [5c923d97e1f7]. `[needs brand data: business time zone and store currency]`

**R11. At property creation, pick the business objective that gives the full report set.** Condition: property creation. S01's presenter picks "other business objectives" for the older layout; S03's presenter picks "Other Business Objectives" because it "basically includes everything". Both are preferences. The report menu can be changed later in Library (editor or admin only). Supports: S01 (opinion), S03 (opinion) [5c923d97e1f7] [cadc7c256522]. `[verify UI]`

**R12. Review enhanced measurement instead of accepting it. Turn off form interactions.** Condition: stream creation and any audit. S01 turns off form interactions because "it's not very reliable". S03 says review all 7 automatic events (page views, scrolls, outbound clicks, site search, forms, video, file downloads) and switch off what you do not want. Neither says which others to disable. Supports: S01 (opinion), S03 [d5ffafc2403f].

### Group C. Install method and testing

**R13. Install GA4 through Google Tag Manager where the platform allows it. On a hosted checkout, use the platform's own integration for checkout pages.** Condition: GTM is both presenters' preferred method because it manages other vendor tags too (Meta pixel, LinkedIn) [53bd7d4a85c1] [9f5dc9b5cd04]. Both are opinions. Neither source covers Shopify. Shopify checkout pages cannot load GTM; the route there is the Google & YouTube app or a customer events (Web Pixels) pixel (S03 caveat, S01 caveat, S04 caveat). See group J and conflict C2. Supports: S01, S03. `[web check: current Shopify GA4 install path and which ecommerce events the Google & YouTube app sends]` `[needs brand data: store platform]`

**R14. When 1 property covers several domains, list every root domain under Configure your domains.** Condition: cross-domain journeys, including a checkout on a separate domain. 5 domains = 5 entries. A root domain covers its subdomains. Source S01 says this [f965ebdb8cdc] [014312f9dcef]. `[verify UI]` `[web check: cross-domain limits with third-party hosted checkouts; the card claim is not in the source]`

**R15. Test in 2 places before publishing any tag change: GTM Preview proves the tag fired; GA4 DebugView proves GA4 received the event and its parameters.** Condition: every new or changed tag. Publish only after both pass. In DebugView open the event and check parameters, not only the event name: page_location must match the URL; custom parameters must be present, not only automatic ones. DebugView proves arrival, not that a value is correct (S03 card). Supports: S01 [80fdd796ee78] [0aad0a745c66] [6a6a1f68f1b4], S03 [9bedc2d9534e], S04 (same 2-place logic for GTM server preview and Events Manager) [8d023b8f223e].

**R16. Judge standard reports only after processing: 24 to 48 hours (S01) or 12 to 24 hours (S03). Use Realtime and DebugView for same-day checks.** Condition: after a new install, a new event or a new custom dimension. Some events show sooner but are "not fully processed", so acquisition reports stay wrong for a while (S01). Keep the stricter 48-hour wait for any decision. Supports: S01 [0aad0a745c66] [a043dadb24a2], S03 [fbe6ee425691] [30843583e84d].

**R17. Event names are lowercase with underscores. Parameter keys match exactly across GTM, GA4 and filters.** Condition: every custom event and parameter. Names are case-sensitive. Register every custom parameter as a custom dimension (event scope) or it never appears in reports. Supports: S01 [23f8bf44b13a] [a043dadb24a2] [50fb683ebc09], S03 (custom definitions named, steps not shown) [d93703003497].

**R18. Define internal traffic and then activate the filter. A filter left in Testing excludes nothing.** Condition: staff with static IPs (office, warehouse, agency). Filters apply from activation forward; they do not restate the past. Source S01 gives the steps [92193cbedb5d] [822ba43fffb7]. S03 names the setting but gives no steps [c01dc627e7b1]. `[needs brand data: office and warehouse IPs and whether they are static]` `[verify UI]`

### Group D. Day-1 settings and what to leave alone

**R19. Set event data retention to 14 months the moment the property exists.** Condition: every new property; audit every old one. Default is 2 months. Data beyond the window is not recovered by changing the setting later (S01 card claim). Both sources agree on 14 months. Scope of the effect is disputed: S01 says explorations only reach the retention window; S03's transcript says "more historical data in your reports" while its card narrows this to Explore. Common understanding is that retention limits explorations, not standard aggregated reports. Supports: S01 [017251ba79b0] [4bce06a3a94d], S03 [c01dc627e7b1]. `[web check: whether retention affects standard reports or only explorations]` `[verify UI]`

**R20. Leave session timeout at the 30-minute default unless the brand decides otherwise in writing, and log the change date.** Condition: this is a brand decision, not a default. S01's presenter sets at least 4 hours and often the maximum 7 hours 55 minutes to cut "(not set)" and false checkout landing pages. He admits "some people might disagree" and states the cost: same-day visits merge, session counts fall, per-session conversion rate changes, and history is no longer comparable. S03 never raises it. Common practice keeps 30 minutes for comparability with ad platforms and past data. Conflict C5. Supports: S01 only (opinion) [ca9e3c7b6aec] [c91c77718ecd]. `[needs brand data: typical time from first visit to purchase]` `[verify UI]`

**R21. Do not raise the engaged session timer above the 10-second default without a brand decision, and never compare engagement rate across a change.** Condition: S01's presenter sets 30 seconds or more, by opinion. S05 reads the 10-second GA4 definition as the relevance signal and sets no target. Changing the timer breaks engagement rate comparisons. Supports: S01 (opinion) [ce843bc07545], S05 [22a5b5e7d62e]. `[web check: full current GA4 engaged-session definition (time, key event or 2+ page views) and the timer's maximum]`

**R22. Turn on Google Signals only after a consent review for every selling country; do not treat it as a day-1 default.** Condition: S01 lists it among 5 day-1 settings and adds "talk to legal first" for strict companies; S03 says enable it for age, gender, interests and Ads audiences and names Consent Settings as a separate admin item. Both are opinions from presenters outside the brand's markets. Demographics are directional only and "not that accurate" (S01). Signals can take weeks to populate. Conflict C4. Supports: S01 [374c795a2291] [bc1344c5d961] [3d2bb5de8e28], S03 [c01dc627e7b1]. `[web check: current Google Signals behaviour, reporting thresholds and consent mode requirements in the brand's markets]` `[needs brand data: selling countries]`

**R23. Run the 5-setting audit in this order on every property: retention, domains, internal traffic, session timeout and engaged timer (decide, do not blindly change), Google Signals (decide after legal).** Condition: new properties and audits. Retention first because it cannot be recovered. Items 4 and 5 are decisions, not defaults (R20 to R22). S01's intro calls them "must configure"; its closing says "configure or at least thoroughly consider". Cards 8f32ae745a5b and d2833e8633f3 list the 5 differently; use the transcript order. Source S01 [48b668a95917] [8f32ae745a5b] [d2833e8633f3].

**R24. Link Google Ads and Search Console under Product Links when the brand runs them. Set up Consent Settings before using EU users' data for Ads targeting.** Condition: the brand runs Google Ads or wants Search Console reports. Source S03 says this; no steps for consent mode are given [c01dc627e7b1]. Google Ads conversion actions belong to 12-GAD. `[web check: consent mode v2 setup for the store's platform and markets]` `[verify UI]`

### Group E. Key events and ecommerce event coverage

**R25. GA4 does not track ecommerce out of the box. Confirm which ecommerce events actually arrive before reading any monetization, funnel or purchase journey report.** Condition: always. view_item, add_to_cart, begin_checkout, add_payment_info, purchase, item data and revenue appear only if the platform, a developer, GTM or an app sends them. Without them the reports are empty or partial, and a "drop-off" may be a missing event (S05 card). Supports: S01 (stated 4 times) [d6b4bece9591] [ae2ed547485e] [2cac3e89ff27] [70e866a19de2], S03 [ac9071a3bbdd] [7425cd2ae91c], S05 [000e5a39ddc8]. `[needs brand data: GA4 ecommerce event coverage and item parameters as they arrive]`

**R26. The sales key event is the purchase event with value, currency, items and a unique transaction_id, never a thank-you page view.** Condition: any store. S03 shows a page_view-based created event on a URL containing "thank-you" and uses it for a lead form (generate_lead), not for sales; the card adds "rely on purchase instead" [e2bcc61df786]. S05 shows that key events include non-purchase events, so every conversion rate must be filtered to purchase [d5605a4c54a8]. S01 names purchase as the key event example [70e866a19de2]. Page reloads and revisits double count a URL match; a transaction_id lets GA4 deduplicate purchases. No source shows the transaction_id mechanism; this is common practice. Conflict C1. `[web check: current GA4 purchase deduplication by transaction_id and its time window]`

**R27. Mark only business outcomes as key events. Never mark page_view.** Condition: choosing key events. Marking page_view counts a conversion on every page (S03) [e2bcc61df786]. Over-marking dilutes the signal (S01 card, not transcript) [70e866a19de2]. For a thank-you page lead, first create a unique event, then mark it. Supports: S01, S03.

**R28. Keep the "Once per event" counting default for purchase. For leads, decide once per session or once per event per brand and log it.** Condition: S03 keeps "Once per event" for generate_lead by default; many practitioners count leads once per session. Purchase must count every transaction. Source S03 [e2bcc61df786]. `[web check: current GA4 counting options and Google's guidance per event type]`

**R29. Every conversion rate shown to a person is filtered to the purchase event and labelled with its denominator.** Condition: any GA4 report with session key event rate or key events. S05's store read 1.7% overall only after the purchase filter (example, not a benchmark) [d5605a4c54a8] [67d1533fdd9c]. Cross-check against total revenue in the same table, and re-check after any change to the key event list (S05 card). Source S05.

**R30. Total Revenue equals Purchase Revenue only when no non-purchase event carries value. Report Purchase Revenue for sales.** Condition: Monetization reports. An unexplained gap means some event sends a value parameter; list them. Source S03 says this [2fa8beb663c8].

**R31. GA4 key events and Google Ads conversions are different counts. A mismatch is expected.** Condition: Advertising reports after the Ads link. Ads adds its own conversion actions to imported key events. Use Conversion management to list both. Source S03 says this [a8f35cf35c8e]. Detail belongs to 12-GAD. `[verify UI]`

**R32. Register the parameters you will report on (coupon, item_list_name, promotion, custom fields) or their cards stay empty.** Condition: Monetization overview coupon, promotion and list cards, and any custom parameter. Supports: S01 [a043dadb24a2], S03 [2fa8beb663c8]. The sources do not show how to send these ecommerce parameters. `[web check: GA4 recommended ecommerce events and parameters]`

### Group F. Reading GA4 reports without the traps

**R33. Pick the acquisition report that matches the question: User acquisition is first touch ever; Traffic acquisition is the source of each session.** Condition: any channel judgement. A returning user's 5 later sessions all sit under the first source in User acquisition. S01's presenter says most marketers want Traffic acquisition. S03's card adds "first touch for brand and LTV talk, session for campaign and budget talk" (card inference). Supports: S01 [a26e80bd2101], S03 [0d831192ef28].

**R34. Read channel group, then add medium, then campaign.** Condition: Traffic acquisition. Channel group alone hides CPC vs paid social vs a named email sender (S05: Omnisend appears as its own medium). Medium values come from UTMs, so bad tagging makes this view wrong (S05 card). S01 shows the same with Session source / medium and Session campaign name. Supports: S01 [a26e80bd2101], S05 [b84c5ad106a2] [5dde1ccb7160].

**R35. Customize and save report tables; do not read defaults.** Condition: any recurring read. S05's set: sessions, engaged sessions, engagement rate, average engagement time, events per session, event count, key events, session key event rate (purchase), total revenue. Pick the set that fits the question; there is no fixed list. Source S05 [67d1533fdd9c]. `[verify UI]`

**R36. Judge entry pages in the Landing page report, never by revenue in Pages and screens.** Condition: page value questions. Pages and screens credits revenue to the page where the purchase happened, so revenue piles on checkout. Landing page revenue is for sessions that started on that page. Source S01 says this [5c2c65569229]. S03 and S05 use the Landing page report the same way [90bd1b325921] [b700e12faf0c].

**R37. A checkout page listed as a landing page is a session break, not a real entry.** Condition: Landing page report. Cause per S01: the session expired mid-checkout (30-minute default) and a new session began on checkout. Read it as a data artefact. Whether to change the timeout is R20. Source S01 [5c2c65569229] [ca9e3c7b6aec].

**R38. Compare product pages by purchase-filtered conversion rate only when each has enough sessions, and rule out traffic mismatch before blaming the page or product.** Condition: Landing page report with the purchase filter. A low page has 1 of 3 causes: wrong traffic sent to it, a page that needs work, or a weaker product. A redesign will not fix wrong traffic (S05 card). Small traffic gives noisy rates; whether a gap is real belongs to 09-CRO. Source S05 [b700e12faf0c]. `[needs brand data: sessions per landing page over several periods]`

**R39. Reports monitor; Explore answers 1 question. Explorations are private until shared, view-only when shared, and limited by retention.** Condition: choosing where to look. Free form for tables (revenue by country and device; site search terms), Funnel for step drop-off, Path for what happens before purchase or around checkout. Filter a free form to the event you care about or the first row is a huge empty total. Supports: S01 [20d5752ed796] [70c537e426a1] [0c84e8cf0da8], S03 [cadc7c256522] [8db1bf5fadc7]. `[verify UI]`

**R40. In a funnel exploration, keep "indirectly followed by" unless you mean to drop everyone who viewed another page between steps.** Condition: any funnel. "Directly followed by" changes the numbers a lot. Add a Device category breakdown; a desktop vs mobile gap is a hypothesis about the mobile experience, not a finding. Supports: S03 [ac9071a3bbdd], S01 [2cac3e89ff27].

**R41. Treat AI answers (Analytics Advisor, Insights) as leads to check in a report, never as findings.** Condition: any AI chat over GA4 data. S01's demo: 1 correct number (125 organic purchases), then a wrong date range and a repeated myth ("a custom event before page_view causes (not set) landing pages"; the presenter's own experiments say it does not). S05's creator uses Insights for a "very quick answer" only. Supports: S01 [bb64df0f76c5] [1ed5edfed51c], S03 [a338f3ce307d] [57ce958e9267], S05 [7cef7f4d4e54]. S02 predicts AI will soon run tests and reports with humans only setting guardrails; that is a forecast, not a method, and it conflicts with ecomOS owner review [0f952763382f].

**R42. Read "(not set)" as unknown and report its share. Investigate when the share is large; no source gives a threshold.** Condition: any dimension. Source S03 [d54ee95e619b]. Longer session timeouts reduce "(not set)" landing pages per S01 [ca9e3c7b6aec]; see R20 before changing anything. `[needs brand data: baseline "(not set)" share per report]`

**R43. Use the E-commerce purchases report (item views, add to carts, purchases, item revenue) for product decisions, and the Checkout journey report with Device category and Browser breakdowns for technical checkout problems.** Condition: ecommerce events present (R25). 1 browser dropping far more at 1 step is a likely bug to reproduce, not proven. Source S01 [d6b4bece9591] [ae2ed547485e]. `[verify UI]`

### Group G. Meta pixel, Conversions API and deduplication

**R44. Run the redundant setup: the same event from the browser pixel and from CAPI, merged by 1 shared event ID.** Condition: any Meta event sent both ways. S04 says this is "how Meta recommends" without a citation. Without dedup every event counts twice. Redundancy and dedup ship together or not at all; never publish a server stream before the dedup check passes. Supports: S04 [0b762a508449] [0954c80debf4], S07 (gateway dedups automatically) [90f2da80bf67]. `[web check: Meta's current redundant setup recommendation]`

**R45. The dedup proof is the same event ID on the browser copy and the server copy in Events Manager, found by searching the ID. A green tag is not proof.** Condition: every event type the store sends, not only PageView. S04: automatic forwarding of the event ID "sometimes doesn't work". S07's demo only checked PageView; its card adds per-event checks (PageView, AddToCart, Purchase) and watching for duplicate-event warnings and sudden conversion jumps after a few days. Supports: S04 [0954c80debf4] [8d023b8f223e], S07 [90f2da80bf67]. `[verify UI]`

**R46. Match event name as well as event ID between the 2 streams.** Condition: any dedup. S04 says only the ID must match, but its own setup keeps names aligned (PageView/PageView, Contact/Contact). Meta's documented rule is event name plus event ID within a time window (S04 caveat, not shown). Keep the strictest condition: same name, same ID. Conflict C8. Source S04 [0954c80debf4]. `[web check: Meta dedup rules, required matching fields and the dedup window]`

**R47. Before adding any CAPI route, list every Meta integration already live. Never run 2 server streams for the same pixel.** Condition: any store. A Shopify Meta channel app, a GTM server container and a CAPI Gateway can each send server events; 2 of them double-send. S07: if a platform plugin already sends pixel and CAPI, the gateway use case does not apply [94681676110e]. S04 caveat: running native Shopify CAPI plus server GTM could double-send. Supports: S04, S07. `[needs brand data: which Meta integrations are live on the store]` `[web check: native Shopify Meta channel CAPI option and how it dedups with a GTM or gateway setup]`

**R48. Server events arrive later than browser events. Wait before calling a server tag broken.** Condition: checking Events Manager. No delay figure is given. Source S04 [0b762a508449] [8d023b8f223e].

**R49. Store pixel ID and access token once per container as constant variables. Variables do not carry across the web and server containers.** Condition: GTM builds. Recreate the pixel ID constant in the server container. Treat the token as a secret (ecomOS rule 5). If Generate access token is greyed out you lack permission; ask the account admin. Source S04 [729a4812f715] [44e509c9fd36]. `[verify UI]`

**R50. Server triggers use Custom Event with an exact match on the incoming event name, plus the consent condition.** Condition: every server Meta tag. A name mismatch means the trigger never fires. Set Event Name Setup Method to Override so you name each Meta event (S04 preference; inherit is allowed for default events). Action Source: Website. Source S04 [44e509c9fd36]. `[verify UI]`

**R51. Map each store event to its Meta standard event (Purchase, InitiateCheckout, AddToCart, ViewContent) and carry value, currency and content IDs. Event match quality needs customer information parameters.** Condition: any store. Neither S04 nor S07 covers Purchase, value, currency, content IDs, customer information parameters (email, phone, external ID, fbp, fbc, IP, user agent), hashing or event match quality (EMQ). This is a gap in the sources, not a rule they state. The agent reads EMQ with `ads_get_dataset_quality` and proposes fixes; it never writes. `[web check: Meta customer information parameters, hashing rules and EMQ guidance]` `[web check: where Events Manager shows EMQ and dedup status today]` `[needs brand data: event map from store events to Meta standard events]`

### Group H. Consent and test event codes

**R52. Send nothing to Meta before consent where consent rules apply. Gate the client pixel on ad_storage and every server trigger on the consent-mode variable showing granted.** Condition: markets with a cookie banner and consent mode. S04 blocks all Meta data without ad_storage and does not cover regions without an opt-in rule or limited data sending. Source S04 [1cdafb95b157] [44e509c9fd36]. `[needs brand data: markets served and the consent rules that apply]` `[web check: current consent requirements for Meta in the brand's markets]`

**R53. Trigger a consent-gated pixel on the cookie consent update event, not on Initialization - All Pages.** Condition: consent-gated pixel with a banner. With Initialization the pixel is blocked on the first page and fires only on the next page, so the opt-in page view is lost. Source S04 (demo) [1cdafb95b157]. `[verify UI]`

**R54. A test event code exists only while GTM Debug Mode is true. Never hard-code it in a tag.** Condition: any server Meta tag. Build a Lookup Table variable: input Debug Mode, default empty, 1 row true = test code. A test code left in a published tag sends real events to Test events, where they do not count; S04's presenter "missed a lot of data" this way. The code can change between days; check it before each test session. Source S04 [e1c161b2fe2d]. `[verify UI]`

### Group I. Gateway vs server-side tagging

**R55. The CAPI Gateway is a pixel plus a relay. Anything that blocks the pixel also blocks the gateway.** Condition: evaluating the gateway. The browser pixel triggers the gateway request; with Ghostery on, neither the Facebook request nor the gateway request fired in S07's test. It cannot beat ad blockers and does not extend cookie lifetime. It accepts only Meta events; you cannot add other tags. Source S07 [94681676110e] [bab947623e26] [21d5b62f2a73].

**R56. Expect Meta's gateway lift claims (up to 13% better cost per result, 7% more conversions) to be claims, and expect S07's "at best 1 or 2%" to be an estimate. Neither is measured on a store.** Condition: any gateway or CAPI business case. Keep both numbers; do not average them. Conflict C6. Source S07 [94681676110e] [bab947623e26]. `[needs brand data: before and after event counts, match rate and dedup status in Events Manager if the brand tests any CAPI route]`

**R57. Choose the gateway only when all 3 hold: no developer or server-side skills, no platform app already sending CAPI, and blocker resistance is not the goal. Otherwise build server-side GTM.** Condition: S07's stated use cases are teams without server-side skills, teams wanting a low-tech path, and sites with a hard-coded pixel and no plugin. S07's presenter does not recommend it and sells the server-side alternative; its cards call it a "stopgap" the source never endorsed. S04 shows the server-side build. Conflict C7. Supports: S07 [94681676110e] [21d5b62f2a73], S04 [0b762a508449]. `[needs brand data: store platform, how the pixel was installed, whether CAPI is already active]`

**R58. If the gateway is used, map a dedicated subdomain, set the CNAME with proxy off, and wait before testing.** Condition: gateway setup. Use a subdomain nothing else serves. DNS takes minutes to hours; the subdomain went live in 5 to 10 minutes in S07's tests, up to about 1 hour for some. Stape charged $10 a month with a 7-day trial; Meta-hosted started at about $30. Source S07 [530daade4029]. `[web check: current Stape and Meta CAPI Gateway pricing and hosting options]` `[verify UI]`

**R59. Server-side tagging adds what the gateway lacks: a custom loader that changes the request URL, and cookie lifetime extension. Neither is quantified.** Condition: choosing between routes. S07 names Stape's loader; no numbers. S04's presenter also hosts on Stape (affiliate). Both sources have a Stape tie. Supports: S07 [21d5b62f2a73], S04 [0b762a508449]. `[web check: Stape custom loader and cookie extension features, and independent hosting alternatives]`

### Group J. Shopify constraints

**R60. On Shopify, GTM does not run inside checkout. Checkout and purchase events come from the platform's native routes (Google & YouTube app, Meta channel app, Web Pixels API customer events). Audit what those routes send before adding anything.** Condition: Shopify stores. S01 and S03 are platform-neutral and assume "GTM on all pages", which does not describe a hosted checkout (both sources' caveats). S05 says to link GA4 and Google Ads "using the Shopify integration" and gives no steps [1735fbb29aff]. S04 caveat: the Shopify Meta channel may already send CAPI. No source shows the Web Pixels API or the Google & YouTube app. Conflict C2. Supports: S01, S03, S04, S05 (all thin). `[web check: current Shopify customer events (Web Pixels API), Google & YouTube app GA4 event list, and Meta channel CAPI behaviour]` `[needs brand data: store platform, Shopify plan, checkout domain, apps installed]`

**R61. Shopify sessions include bot traffic; GA4 sessions are generally lower. Validate Shopify conversion rate against GA4 before acting on it.** Condition: Shopify Analytics reads. S06's presenter says GA4 "does a much better job" of not counting bots (his reading, not sourced). A sudden Shopify conversion dip may be a bot spike invisible in Shopify. Use both. Source S06 [084db9abd48b] [57a97c0614d6]. `[web check: Shopify help docs on sessions and bot filtering; GA4 bot filtering behaviour]`

**R62. Ignore every Shopify attribution and referral card for decisions. Read them as 1 signal among several at most.** Condition: total sales by social referral, sessions by social referral, top referrals by session, sales attributed to marketing, sessions by referrer, total sales by referrer. S06's presenter: "not accurate", "attribution is a futile effort". Card 561513b3e85e softens to "triangulate" with GA4, UTMs, attribution windows, consent coverage and incrementality tests. Conflict C10. Source S06 [561513b3e85e]. Card bcb81bfb6f41 infers a dashboard clean-up from the video: use the Customize button to remove attribution, social referral and returning customer rate cards and add net sales, shipping charges, sessions, conversion rate, AOV and the funnel. The list is the card's, not the presenter's `[verify UI]` `[web check: dashboard customisation on the brand's Shopify plan]` [bcb81bfb6f41].

**R63. Filter Shopify reports to the Online Store sales channel when paid media is judged.** Condition: store sells on more than 1 channel (POS, Shop app, draft orders). Source S06 [6ca5944157b0]. `[needs brand data: sales by channel]` `[verify UI]`

**R64. Do not read loyalty from Shopify's returning customer rate. Open the full cohort analysis report.** Condition: any period with changing new-customer volume. S06's presenter calls it "the most misleading metric": as he reads it, it is the share of orders in the period from returning customers, so it rises when acquisition slows and falls when acquisition scales. Cohort reading belongs to 20-FIN. Source S06 [8f85f33352f5]. `[web check: Shopify's current definition of returning customer rate, orders-based or customers-based]`

**R65. Shopify AOV excludes shipping and is a mean. Report AOV with shipping added when shipping is a notable share, and never act on AOV alone.** Condition: S06's presenter reads Shopify AOV as (gross sales minus discounts) ÷ orders with no shipping. His client collected about 7% to 8% of revenue as shipping, so real AOV was about 7% higher (example). Look at the distribution and new vs returning AOV before acting. Source S06 [9b3f534de0a2]. `[web check: Shopify's current AOV formula]` `[needs brand data: shipping charges as a share of revenue; AOV distribution]`

### Group K. UTM rules and channel classification

**R66. Every paid and owned link carries UTM parameters in the brand's convention. Medium and campaign reads are only as good as the tags.** Condition: always. No source gives a UTM standard. S05's card warns medium comes from UTMs; S01 sketches a paid social filter (Session medium exactly matches cpc AND Session source contains facebook.com, then Session campaign name) and notes ads must use that medium value; S03's campaign report depends on real names. Common practice, not a source rule. Supports: S01 [a26e80bd2101], S03 [8db1bf5fadc7], S05 [b84c5ad106a2]. `[needs brand data: the UTM template used on Meta, Google, email and affiliate links]` `[web check: GA4 default channel group rules for paid social and paid shopping]`

**R67. Real campaign names never start with "(" and end with ")". Filter Session campaign with Does Not Match Regex `^\(.*\)$` to see only named campaigns.** Condition: campaign tables in Explore. Drops "(organic)", "(direct)", "(not set)". Source S03 [8db1bf5fadc7]. `[verify UI]`

**R68. Check the default channel group before judging channels. By default GA4 puts Facebook, Instagram and LinkedIn in Organic Social; paid social needs the right medium or a custom channel group.** Condition: any channel read. Source S03 [0d831192ef28] [c01dc627e7b1]. `[verify UI]` `[web check: current default channel group definitions]`

### Group L. Attribution models, windows and conflicts between platforms

**R69. Attribution models describe how credit is given; they do not settle it. Read Last Click and Data Driven side by side and report the gap, never 1 model as truth.** Condition: Key event attribution models report. A large gap is a signal about a channel, not a measurement of incremental value (S03 card). Source S03 [675a952696ec]. Attribution window choice for buying (for example 7-day click on Meta) belongs to 24-DEP; no source here states a window. `[web check: current GA4 attribution settings: reporting model default, lookback windows, channels that can receive credit]`

**R70. When analytics and the customer disagree on source, neither wins by default. Write a rule for the brand and apply it every time.** Condition: post-purchase survey ("how did you hear about us") vs platform or GA4 credit. S02's presenter: "it's on you ... to decide how to handle that conflict". His cards go further and favour self-report for strategic channel calls; that is card advice. Card 7f3bed7f5dd1 adds: compute the gap per channel for the same window, treat platform numbers as directional, keep budget on channels customers name that platforms cannot see (word of mouth, podcasts, offline), and do not cut an over-claiming channel on platform data alone. Source S02 [e11ec2148e14] [9c479169d7e9] [45d7e49e638b] [7f3bed7f5dd1]. `[needs brand data: survey answers and platform credit for the same buyers and window]`

**R71. Incrementality (holdout) tests are the only way to settle credit. No source in this folder gives a method, volume, window or threshold.** Condition: before reallocating spend on attribution gaps. Card 859e4f5b289d sketches: define channel and outcome, hold out a random segment or geography, measure the difference over "a sufficient window", scale only where lift pays. The S02 speaker never says "incrementality". Test design belongs to 09-CRO and 24-DEP. Source S02 (card only) [859e4f5b289d].

**R72. Get data as close to the customer's mouth as possible, and hold zero-party, first-party and third-party data together. Zero-party answers must reach the CRM, not sit in a quiz tool.** Condition: any source-of-truth question about customers. Zero-party = the customer told you; first-party = you tracked it; third-party = aggregated (Meta, Google, Experian). Source S02 [e11ec2148e14] [9c479169d7e9] [7e8ec204ea88]. `[web check: privacy rules for third-party data in each selling country]`

### Group M. Reconciliation and revenue definitions

**R73. Reconcile platform purchases to store orders for the same dates, time zone and sales channel before any purchase count or revenue is used.** Condition: GA4, Meta and Shopify vs the store's order data (Shopify admin export, Metabase, or platform API). No source gives the method. S03 names the transaction ID report and its card says it can be used for reconciliation with the platform [2fa8beb663c8]. S04 and S01 name the need and give no steps [8d023b8f223e]. S05 says GA4 and Shopify "will differ"; pick 1 source of truth per question [1735fbb29aff]. ecomOS rule; procedure P21. `[needs brand data: order export with order id, timestamp, net sales, shipping, tax, refunds, channel]`

**R74. Top-line revenue for marketing maths is net sales plus shipping charges. Tax stays out. Label it "net sales + shipping", never "cash collected".** Condition: any revenue figure the agent reports. S06's presenter calls it "cash collected"; card a3ae4e9e2a00 corrects: it is a sales-based figure (sales reports can include unpaid orders), not cash and not profit; take cash from payments reports. Total sales includes tax; gross sales is before discounts and returns. Source S06 [a3ae4e9e2a00] [9e9d4013f967]. `[needs brand data: net sales, shipping charges, taxes and refunds for the period]`

**R75. Returns land on the refund date, not the order date. Check refund timing before reading any revenue dip.** Condition: matters most with high return rates (S06 names fashion: 20% of a strong month's orders came back the next month, faking a revenue dip and a CAC rise). S06 adds returns back for some clients; its card prefers showing refund timing separately by order cohort and never calling the add-back cash. Conflict C12. Source S06 [a3ae4e9e2a00]. `[needs brand data: refunds by processing date and by original order date; return rate by month]`

**R76. Any revenue change is sessions, conversion rate or AOV (returns excepted). Name the lever in code, on 1 basis, before anyone explains the change.** Condition: any period-over-period sales move. S06's identity: sales = sessions x conversion rate x AOV. Shopify's own 3 numbers will not multiply to net sales + shipping (its AOV excludes shipping; its sessions include bots), so compute all 3 on 1 basis first. Source S06 [9e9d4013f967].

**R77. Single-digit moves across several levers that compound into a larger top-line move are natural fluctuation when no lever moved sharply. S06 gives no statistical test.** Condition: all levers otherwise stable. S06 example: 5% AOV dip plus 4% conversion dip called "a 10% dip" (computed: 8.8%). Whether a move is real belongs to 09-CRO. Source S06 [9e9d4013f967].

**R78. Unshipped orders = orders minus orders fulfilled. Report the gap.** Condition: Shopify dashboard. A large gap is a fulfilment backlog to raise with operations. Source S06 [9d66cacbbfcd].

### Group N. The 1 top metric

**R79. The executive team picks 1 top metric: number of customers, revenue, or profit. It tells every department. Sometimes 2 can move; almost never all 3.** Condition: company level. Customers max at a free price; revenue sits with a reasonably priced product that makes money per sale; profit "typically is your highest priced product" (S02's claim). Source S02 [13ce65376d8f].

**R80. Match the top metric to stage and bankroll: early stage customers, then revenue, then profit. A stable business may choose profit.** Condition: setting or reviewing the metric. Bigger bankroll means a longer horizon; a small startup needs the next customer but must not burn them with a poor product. Source S02 [0c302f4b2883] [13ce65376d8f].

**R81. Keep the top metric fixed for about a year. Review big focus shifts quarterly at most. Allow quick-win KPI pushes of a couple of weeks to a month without changing it.** Condition: swapping monthly "causes turmoil". Quick-win examples: review count, referral coefficient, loyalty points used, products per order, purchase frequency. Source S02 [13ce65376d8f] [5869b757b0e7].

**R82. Change the main lever at the top of the S curve: when each extra dollar into it returns less and less.** Condition: S02's order for a store: conversion rate first, then AOV, then LTV. No numeric threshold. Source S02 [5869b757b0e7] [3a1918a526e2]. `[needs brand data: spend and result by lever over time]`

**R83. Before scaling a winner, list the metrics it may break: LTV, customer quality, brand affinity, customer experience.** Condition: any winning test or tactic. S02: higher conversion rate can lower LTV; higher AOV can lower LTV (stated, not measured); misspelled ads lifted conversions and hurt brand (second-hand, no numbers). Source S02 [06aa9f46abe7] [13ce65376d8f].

**R84. Data reveals its position; it is not there to back yours. Run the test instead of arguing; ask "can we do both?".** Condition: any HiPPO (highest paid person's opinion) moment. Source S02 [129ad3db527d] [c50f782181a7].

**R85. Classify each lever as compounding, incremental or one-off before ranking it, and check the arithmetic.** Condition: prioritising levers. S02 calls conversion rate and referral coefficient compounding. Its arithmetic ($10,000 x 1.01 = $10,100; 100 customers x 1.05 = 105) is a 1-time step, not compounding (S02 caveat). Source S02 [3a1918a526e2] [63817d833e21].

### Group O. Funnel ratios and bot checks

**R86. Read funnel steps from add to cart onward. The drop from session to product view is normal; still check collections, navigation and search when product views are very low.** Condition: GA4 Purchase journey or Shopify funnel card. Big drop add to cart to checkout: suspect the cart page. Big drop checkout to purchase: suspect shipping cost, trust, or a broken step. These are hypotheses. Supports: S05 [000e5a39ddc8], S06 [c8e57ed1cd0a].

**R87. Benchmark add to cart : reach checkout : purchase against 4:2:1 (S06's "general average"), and against 2:1:1 as a target for FMCG and low-ticket brands only.** Condition: Shopify funnel counts. 4:2:1 means 50% then 50%, 25% overall from cart. 2:1:1 means almost no drop from checkout to purchase. S06's basis is client experience; no industry source is cited. S06 claims fixes lifted conversion 40% to 50% "overnight" for clients (anecdote, not a promise). Source S06 [c8e57ed1cd0a]. `[web check: current Shopify funnel benchmarks by vertical and price point]` `[needs brand data: funnel counts by step over several periods]`

**R88. Do not cite S05's funnel example as a benchmark. Its "99.2%" add-to-cart figure is a probable transcription error.** Condition: any use of S05's numbers. The creator says "only 99.2%"; "only" does not fit. Computed in code: with 99.2%, about 10,000 sessions give about 1,656 purchases (16.6%); with 9.2%, about 154 purchases (1.5%), close to the same store's 1.7% purchase rate. Card 000e5a39ddc8 follows the 99.2% reading and is wrong on this point. Source S05 [000e5a39ddc8] [d5605a4c54a8].

**R89. Before reading any drop as behaviour, confirm every step event is tracked. A step at 0 or near 0 is a tracking gap.** Condition: any funnel. S05 card; S01 R25. Supports: S05 [000e5a39ddc8], S01 [2cac3e89ff27].

**R90. Suspect bots when Shopify shows a session spike or conversion dip GA4 does not, or when 1 city spikes in Sessions by location.** Condition: Shopify stores. A single-city spike "often means" a server hitting the site (S06). Filtering bots inside Shopify is not simple and may need third-party tools (S06 card). Use GA4 sessions as the denominator meanwhile. Source S06 [57a97c0614d6] [084db9abd48b]. `[needs brand data: Shopify vs GA4 sessions for the same dates]`

**R91. Very low engaged sessions on a channel is a relevance warning, after bots and mis-tagged campaigns are ruled out.** Condition: Traffic acquisition. Paid: check ad-to-page message match before adding spend. Organic: check the page matches search intent. Not a proven link to sales. Source S05 [22a5b5e7d62e].

### Group P. Daily trust and freshness

**R92. Run the daily trust check (P22) before any other agent reads yesterday's numbers. Score each source pass, warn or fail and publish the score with the data.** Condition: every day a report is produced. ecomOS rule built from S01 and S03 (Realtime and DebugView for arrival) [30843583e84d] [0aad0a745c66], S04 (browser and server both landing, dedup intact, no test code in production) [8d023b8f223e] [e1c161b2fe2d], S06 (Shopify vs GA4 sessions) [084db9abd48b], S03 (Total vs Purchase Revenue) [2fa8beb663c8].

**R93. Use Realtime to confirm arrival after a send or launch; never for analysis.** Condition: campaign send or site launch. Realtime shows within seconds; standard reports lag (R16). Supports: S03 [30843583e84d] [fbe6ee425691], S01 [0aad0a745c66].

**R94. Log every settings change (timeout, timer, key events, channel groups, filters, consent) with a date, and annotate reports across it.** Condition: any change that breaks comparability. S01 states the comparability cost of timeout changes; S05 card says to re-check rates after any key event change. ecomOS rule; supports S01 [c91c77718ecd], S05 [d5605a4c54a8].

### Group Q. Qualitative inputs

**R95. Quantitative tells what; qualitative tells why. Pair every quantitative drop with a recording, heatmap, survey verbatim or customer call before proposing a fix.** Condition: any diagnosis. Ask at every stage: before awareness, after awareness, on-site ("what is this page missing?"), post-purchase (source survey), after churn (for example no purchase for 1 year). Founders talk to at least 1 customer a week in the first 3 years (S02 opinion). Listen most to the 3% most loyal and 3% biggest haters (second-hand from ProfitWell). Source S02 [e2f188649f8f] [5dffd6bf5d3c] [7e8ec204ea88] [375f45ad5513] [338914784a95]. Research method belongs to 09-CRO.

## 4. Procedures (implementation)

**Meta is read-only in ecomOS; propose, do not execute.** Every step below that changes a Meta dataset, pixel or Events Manager setting is a proposal for a human operator. GA4, GTM and Shopify admin steps are also written as proposals unless the brand record says the agent holds edit access. Every platform step carries `[verify UI]` because GA4, GTM, Meta Events Manager and Shopify menus in the sources are 2025 and 2026 snapshots and change often. Before running any procedure, do a `[web check: current menu names]` for that platform once per session.

### P1. Create the GA4 account, property and web data stream

Goal: a property whose time zone, currency and structure will not need changing later.
Preconditions: inputs from section 2 (domains, time zone, currency, platform). Decide R7 to R12 first.
Steps:
1. Go to analytics.google.com (S01) or marketingplatform.google.com (S03). Existing GA users: Admin > Create > Account. First-time users are prompted at once. `[verify UI]` [a61d1986b945] [5c923d97e1f7]
2. Name the account after the organization. Keep the data sharing defaults unless the brand says otherwise. Next. `[verify UI]`
3. Name the property after what it measures. Set reporting time zone (country, then city) and currency to the store's. Next. `[needs brand data: time zone, currency]` `[verify UI]` [5c923d97e1f7]
4. Pick industry and business size. Next. `[verify UI]`
5. Business objectives: pick the option that gives the full report set ("Other Business Objectives" in both sources' recordings). Create. Accept terms for the brand's country. `[verify UI]` [cadc7c256522]
6. Platform: Web. Enter the store's main domain (any 1 domain if several share the property) and a stream name. `[verify UI]` [a61d1986b945]
7. Open the enhanced measurement settings before creating the stream. Turn off form interactions (S01). Review the other 6 and switch off what the brand does not want. Save. `[verify UI]` [d5ffafc2403f]
8. Create the stream. Copy the Measurement ID (starts with `G-`) from the stream details. Store it in the brand record, not in chat. `[verify UI]` [53bd7d4a85c1]
Checks after: Property Details shows the intended time zone and currency [5c923d97e1f7]. Only 1 web stream exists. Tech > Platform will read 100% Web on a web-only property once data arrives [f2f53af85949].
Rollback: a wrong time zone found after data arrives cannot be fixed cleanly; create a new property and log the cut-over date rather than editing the live one (R10).

### P2. Install GA4 through GTM and prove it in Preview and DebugView

Goal: the Google tag fires on every page the store controls, and GA4 receives page_view with the right page_location.
Preconditions: P1 done. Step 0 decided.
Steps:
0. Decide the install route by platform. Hosted checkout (Shopify): GTM cannot run in checkout; use the platform integration for checkout and purchase events and GTM only for storefront pages, or use the platform integration everywhere (R13, R60). `[web check: current Shopify GA4 install path]` `[needs brand data: store platform]` [9f5dc9b5cd04]
1. tagmanager.google.com > create an account (1 per organization) and a Web container named after the domain. Accept terms. `[verify UI]` [53bd7d4a85c1]
2. Place the first GTM snippet on all pages. S01's presenter says the second (noscript) snippet "can be ignored"; Google's install instructions place it after the opening body tag. Install both. `[web check: current GTM install instructions]`
3. In GTM: Tags > New > Google Analytics > Google tag. Tag ID: create a Constant variable "GA4 Measurement ID" holding the ID (S03), so every tag reuses it. Trigger: Initialization - All Pages. Name it (S03: "Google Tag, GA4, Page View"; S01: "GA4 config"). Save. `[verify UI]` [9f5dc9b5cd04]
4. Preview > enter the store URL > Connect. Confirm "Tag Assistant connected". In the Preview panel open Initialization and confirm the Google tag fired. `[verify UI]` [0aad0a745c66] [80fdd796ee78]
5. GA4 > Admin > DebugView (or Admin > Data display > DebugView). Confirm page_view, and possibly first_visit and session_start, arrive. Open page_view and check page_location matches the URL opened. `[verify UI]` [9bedc2d9534e]
6. If Preview disconnects, close the Preview window and the site tab and start again. Click Preview again after every change. An "unknown tag type" note is a Preview bug (S01). [0aad0a745c66]
7. Only after steps 4 and 5 pass: Submit > version name (for example "installed GA4") > Publish. [80fdd796ee78]
8. Wait 24 to 48 hours before reading standard reports (R16). Use Realtime meanwhile. [0aad0a745c66] [fbe6ee425691]
Checks after: Realtime shows users in the last 5 and 30 minutes after a test visit [30843583e84d]. Home shows "data collection is active" [0aad0a745c66].
Rollback: GTM keeps versions; publish the previous version. [80fdd796ee78]

### P3. Apply and audit the day-1 settings

Goal: retention, domains and internal traffic set; timeout, timer and Signals decided and logged.
Preconditions: P1. Brand decisions on R20 to R22 recorded.
Steps:
1. Admin > Data retention: event data retention from 2 months to 14 months. Save. Do this first. `[verify UI]` [017251ba79b0] [4bce06a3a94d] [c01dc627e7b1]
2. If 1 property covers several domains: Admin > Data streams > web stream > Configure tag settings > Configure your domains > add every root domain. Save. `[verify UI]` [f965ebdb8cdc] [014312f9dcef]
3. Internal traffic: Configure tag settings > Show more > Define internal traffic > Create. Rule name (for example "office IP"), condition IP address equals the office IP (the screen shows your current IP). Add warehouse and agency IPs. Then Admin > Data collection > Data filters > the internal traffic filter shows "Testing" > Activate. `[verify UI]` `[needs brand data: static IPs]` [92193cbedb5d] [822ba43fffb7]
4. Session timeout and engaged session timer: Configure tag settings > Show more > Adjust session timeout. Default 30 minutes and 10 seconds. Change only on a written brand decision (R20, R21); if changed, log the date in the brand record and annotate every report that crosses it. `[verify UI]` [ca9e3c7b6aec] [ce843bc07545]
5. Google Signals: Admin > Data collection > Google signals data collection. Turn on only after the consent review for every selling country (R22). Expect weeks before demographics fill. `[verify UI]` `[web check: current Signals behaviour and consent requirements]` [374c795a2291] [bc1344c5d961]
6. Consent Settings (Admin > Data collection and modification): check consent mode is detected before using EU users' data for Ads targeting. Setup steps are not in any source. `[verify UI]` `[web check: consent mode v2 setup for the store's platform]` [c01dc627e7b1]
7. Product Links: link Google Ads and Search Console if the brand runs them. `[verify UI]` [c01dc627e7b1]
8. Channel Groups: check where paid social lands (default: Organic Social for Facebook and Instagram). Create a custom group if the brand's UTMs need it (R68). `[verify UI]` [0d831192ef28]
9. Comparisons (Admin > Data display > Comparisons): segments that overlay standard reports. S03 names them and gives no steps; card 5e2819e7dfec adds steps and says they do not persist as saved views (card claim). `[verify UI]` [5e2819e7dfec]
Checks after: checklist 5.8, every row.
Rollback: retention and filters apply forward only; there is nothing to roll back except to re-open the filter to Testing. Timeout and timer changes can be reverted, but the data collected in between stays on the changed basis.

### P4. Mark the sales key event and any lead key event

Goal: purchase is the only sales key event; lead events are unique events, never page_view.
Preconditions: P2. Ecommerce events confirmed arriving (P6). Marketer, editor or admin access.
Steps:
1. Admin > Events (Admin > Data display > Events). Key Events tab and Recent Events tab. `[verify UI]` [e2bcc61df786]
2. Find `purchase` in the events list. Mark it as a key event (star icon left of the event, or the toggle in the list). If `purchase` is absent, stop: the store is not sending it (R25). `[verify UI]` [70e866a19de2]
3. Confirm purchase carries transaction_id, value, currency and items in DebugView (P6 step 3). Without transaction_id, GA4 cannot deduplicate a repeat purchase event from a reload. `[web check: GA4 purchase dedup by transaction_id and its window]` [e2bcc61df786]
4. Lead events only (contact, signup, quote): Create Event > name it (S03: `generate_lead`) > Mark as key event on > optional default value `[needs brand data: value per lead]` > counting "Once per event" (S03 default; decide per brand, R28) > Create without code > condition event name equals `page_view` and URL contains the confirmation path (S03: `thank-you`) > Create. `[verify UI]` `[needs brand data: exact confirmation URL pattern]` [e2bcc61df786]
5. Never use step 4's method for purchases (R26, conflict C1).
6. In every acquisition or landing page report, set the key event selector to purchase only (R29). `[verify UI]` [d5605a4c54a8]
Checks after: Realtime shows the key event after a test purchase or test lead; standard reports the next day [fbe6ee425691]. The Purchases predefined audience is no longer empty [7425cd2ae91c].
Rollback: unmark the key event; the events themselves keep collecting.

### P5. Send a custom event with parameters through GTM and register the dimensions

Goal: an interaction GA4 does not collect automatically arrives with its parameters and is reportable.
Preconditions: P2. The element's CSS class, text or URL known `[needs brand data: theme's CSS classes]`.
Steps (S01's menu link example; swap the trigger for the store's element):
1. GTM > Triggers > New > Just Links > All link clicks. Save. Preview and connect. `[verify UI]` [6a6a1f68f1b4]
2. On the site, hold Ctrl (Cmd on Mac) and click the element so it opens in a new tab and the page does not unload. In Preview open the Link Click event. [6a6a1f68f1b4]
3. If click variables are empty: Variables > Built-in variables > Configure > tick all Click variables. Refresh Preview. `[verify UI]`
4. Read Click Text, Click URL, Click Classes. Find a value only the target elements have. Edit the trigger: Some Link Clicks > Click Classes contains that value. Rename. Save. `[verify UI]`
5. Tags > New > Google Analytics > GA4 Event. Measurement ID from the constant. Event name lowercase with underscores (S01: `menu_link_click`). Event parameters: `menu_item_name` = `{{Click Text}}`, `menu_item_url` = `{{Click URL}}`. Trigger: the trigger from step 4. Save. `[verify UI]` [23f8bf44b13a] [50fb683ebc09]
6. Preview: click several elements with Ctrl held; confirm the tag fired each time. DebugView: confirm the event arrives with both parameters. [80fdd796ee78]
7. GA4 > Admin > Data display > Custom definitions > Create custom dimension: event parameter key exactly as sent, readable name, scope Event. Repeat per parameter. `[verify UI]` [a043dadb24a2]
8. Submit and Publish with a version name. Wait at least 24 hours before looking in reports. [50fb683ebc09]
Checks after: Events report shows the event with 1 widget per registered dimension; a free form exploration filtered to the event name lists the parameter values [70c537e426a1].
Rollback: publish the previous GTM version. Custom dimensions cannot be deleted quickly; archive them.

### P6. Check ecommerce event coverage

Goal: know which ecommerce events and parameters the store sends to GA4, from which route, before any funnel or revenue report is trusted.
Preconditions: P2. Access to DebugView. A test order path that does not create a real order, or a real test order that will be refunded and excluded `[needs brand data: test order policy]`.
Steps:
1. Record the route for each page type: storefront (GTM or platform integration), checkout (platform only on Shopify), thank-you page. `[needs brand data: apps and integrations]` [9f5dc9b5cd04]
2. Open DebugView. Walk the journey: collection page, product page, add to cart, begin checkout, add shipping, add payment, purchase. `[verify UI]` [9bedc2d9534e]
3. For each step record: event name present (view_item, add_to_cart, begin_checkout, add_shipping_info, add_payment_info, purchase), parameters present (value, currency, items with item_id, item_name, price, quantity; transaction_id, coupon, shipping, tax on purchase), and the route it came from. Mark each as pass, fail or unknown (9.1). [2cac3e89ff27] [ac9071a3bbdd]
4. Build the funnel exploration (P16 step B) for the last 7 days. A step at 0 or near 0 while the step before has volume is a tracking gap, not behaviour (R89). [000e5a39ddc8]
5. Monetization > Overview: coupon, promotion and item list cards empty means those parameters are not sent (R32). `[verify UI]` [2fa8beb663c8]
6. Tech > Platform: 100% Web on a web-only property; any app share means a stray stream (S03). `[verify UI]` [f2f53af85949]
7. Write the coverage table (9.1) and the fix list (9.2) with an owner per gap (developer, app settings, GTM).
Checks after: every funnel step has a route and a status. No step is "assumed".
Rollback: none; this procedure changes nothing.

### P7. Get the Meta credentials for CAPI

Goal: pixel (dataset) ID and a CAPI access token, held as secrets.
Preconditions: Business Manager admin access, or an admin who can generate the token `[needs brand data: which Business Manager owns the pixel and who administers it]`.
Steps:
1. Meta Events Manager > Data sources > select the pixel. Copy the ID (labelled "Dataset ID" in S04's recording). `[verify UI]` [729a4812f715]
2. Settings > Conversions API section > Generate access token. Copy it. If the button is greyed out, ask the account admin to generate and send it through a secret channel. `[verify UI]` [729a4812f715]
3. Store both in `.env` or `secrets/`. Never in a playbook, page, chat or commit (ecomOS rule 5). S04 stores them in a text file; do not copy that.
Checks after: the values are readable from the secret store and nowhere else.
Rollback: an exposed token is rotated by generating a new one in the same place; the old one must be replaced in the GTM constant.

### P8. Client-side Meta pixel in the web GTM container, consent-gated

Goal: the pixel fires on the same page as opt-in, never before consent, with an event ID on every event.
Preconditions: web GTM container live (P2). Consent Mode with a cookie consent update dataLayer event `[needs brand data: consent tool and its event name]`. Markets and rules known (R52).
Steps:
1. Variables > New > Constant "Meta Ads Pixel ID" = the pixel ID. Save. `[verify UI]` [729a4812f715]
2. Variables > New > Community Template Gallery > search "event ID" > the Event ID template (S04 uses Markus Baersch's; Stape's is "also very good"). No settings. Name it "Event ID". Save. `[verify UI]` `[web check: templates still in the gallery and maintained]` [0954c80debf4]
3. Tags > New > Community Template Gallery > "Facebook Pixel" by facebookarchive > add. Pixel ID `{{Meta Ads Pixel ID}}`. Event name PageView. More Settings > Event ID = `{{Event ID}}`. `[verify UI]` [1cdafb95b157] [0954c80debf4]
4. Advanced Settings > Consent Settings > Require additional consent for tag to fire > `ad_storage`. `[verify UI]` [1cdafb95b157]
5. Trigger: the cookie consent update event, not Initialization - All Pages (R53). Save. `[verify UI]` [1cdafb95b157]
6. Repeat step 3 for each store event mapped to a Meta standard event (ViewContent, AddToCart, InitiateCheckout, Purchase) with its own trigger and the same Event ID and consent settings. S04 shows only PageView and Contact; the mapping is the brand's `[needs brand data: event map]`. [44e509c9fd36]
7. Test in Preview (checklist 5.3 rows 1 and 2): before consent the tag shows "blocked by consent settings"; after "Allow all" it fires on the same page. To retest, delete the consent cookie in DevTools > Application > Cookies and refresh. [1cdafb95b157]
Checks after: Meta Pixel Helper shows the event with an event ID [90f2da80bf67]. No Meta request in DevTools Network before consent.
Rollback: publish the previous GTM version.

### P9. Server-side CAPI tags in the server GTM container

Goal: the same events reach Meta from the server, each with the event ID from the browser and a consent condition.
Preconditions: a server GTM container receiving GA4 hits from the web container (S04's earlier videos; hosting such as Stape `[web check: server GTM hosting options and cost]`). A consent-mode variable readable in the server container. P7 and P8 done.
Steps:
1. Web container: on every GA4 event tag that drives a Meta server event (page view, add to cart, begin checkout, purchase), add an event parameter carrying `{{Event ID}}`. S04 speaks the key as "event ID". `[web check: the exact parameter key the Stape Meta CAPI tag reads, often event_id]` `[verify UI]` [0954c80debf4]
2. Server container: Variables > Constant "Meta Ads Token" = the token; Constant "Meta Ads Pixel ID" = the ID (variables do not carry across containers). `[verify UI]` [44e509c9fd36] [729a4812f715]
3. Tags > New > Community Template Gallery > "Facebook Conversions API" by Stape. Event Name Setup Method: Override > PageView. Action Source: Website. API Access Token `{{Meta Ads Token}}`. Pixel ID `{{Meta Ads Pixel ID}}`. Test ID `{{Meta Ads Test ID}}` (P10). `[verify UI]` [44e509c9fd36]
4. Trigger "All Pages with consent": Page View > Some Page Views > consent-mode variable contains granted. Save. `[verify UI]` [44e509c9fd36]
5. For each conversion event: new tag with the same template, Override to the Meta standard event name. Trigger: Custom Event, event name exactly as it appears in server preview (turn on preview in both containers, do the action, read the incoming event name; on a thank-you page it may appear only after a refresh in S04's demo). Add the consent condition. Put the event name in the trigger title. Save. `[verify UI]` [44e509c9fd36]
6. Preview the server container. Open the incoming event > Event Data: the event ID parameter is present. Open the Meta tag's outgoing request: the event ID is in it. The tag shows "succeeded"; "failed" means re-check token and pixel ID. `[verify UI]` [0954c80debf4] [8d023b8f223e]
7. Events Manager > Test events: 1 browser and 1 server copy per event; the server copy marked deduplicated. Copy the browser event ID and Ctrl+F (Cmd+F) for it: both copies carry it (R45). Repeat per event type. `[verify UI]` [8d023b8f223e] [0954c80debf4]
8. Publish both containers only after step 7 passes for every event type.
Checks after: checklist 5.3 rows 3 to 8. After a few days, `ads_get_dataset_stats` and `ads_get_dataset_quality` (read only) show no duplicate warnings and no sudden conversion jump [90f2da80bf67].
Rollback: publish the previous server container version; the web pixel keeps working alone (with dedup no longer needed).

### P10. Test event code that exists only in Debug Mode

Goal: test events land in Test events during preview and never in production.
Preconditions: P9 in progress.
Steps:
1. Events Manager > Data sources > Test events tab. Copy the test event code. `[verify UI]` [e1c161b2fe2d]
2. Server container > Variables > New > Lookup Table "Meta Ads Test ID". Input variable: Debug Mode (enable it under built-in variables if not listed). Default value: empty. 1 row: input `true` > output = the code. Save. `[verify UI]` [e1c161b2fe2d]
3. Put `{{Meta Ads Test ID}}` in the Test ID field of every server Meta tag. [e1c161b2fe2d]
4. Before each test session, re-open Test events; if the code changed, update the row output. [e1c161b2fe2d]
Checks after: a normal (non-preview) visit sends no test ID and appears in live data, not in Test events (checklist 5.3 row 9).
Rollback: none needed; the variable is inert outside Debug Mode.

### P11. Dedup check on a live setup (any route: GTM, gateway or platform app)

Goal: prove each event type is counted once.
Preconditions: read access to Events Manager or the Meta MCP dataset read tools. Meta Pixel Helper installed for browser checks.
Steps:
1. List the routes sending events for this pixel (browser pixel, GTM server, gateway, Shopify Meta channel, other apps) `[needs brand data]`. More than 1 server route means a probable double count (R47). [94681676110e]
2. On the live site with DevTools Network filtered to "facebook": the direct Facebook request is present. Meta Pixel Helper shows an event ID on each event. `[verify UI]` [90f2da80bf67]
3. If a gateway is in use: find the request to the gateway subdomain and open its payload; the event ID equals the Pixel Helper one. [90f2da80bf67]
4. Events Manager > Test events (with the test code active, P10) or the event's detail view: browser and server copies of PageView, ViewContent, AddToCart, InitiateCheckout and Purchase each share 1 ID; server copies marked deduplicated. `[verify UI]` [0954c80debf4] [8d023b8f223e]
5. Read `ads_get_dataset_quality` and `ads_get_dataset_stats` (read only) for duplicate-event warnings, dedup rate and EMQ per event. `[web check: which fields these tools return for dedup and EMQ]` [90f2da80bf67]
6. Compare Meta Purchase count for the last 7 full days against store orders for the same days and channel (P21). A Meta count near 2x orders is a dedup failure; near 1x with a small gap is normal. Compute in code.
7. Write the result in the audit table (9.1) and the fix list (9.2).
Checks after: every event type has a pass, fail or unknown, and the reason.
Rollback: none; read only.

### P12. CAPI Gateway through Stape (only when R57 holds)

Goal: a relay that adds CAPI and dedup to a hard-coded pixel without developers.
Preconditions: R57 answered yes to all 3 conditions. DNS access `[needs brand data: who manages DNS and where]`. Business Manager admin.
Steps:
1. Baseline: DevTools Network, filter "facebook", reload: a Facebook request and a PageView event and nothing else means a pure client-side setup. `[verify UI]` [94681676110e]
2. Stape > Pricing > dedicated gateways > Meta conversions API gateway > learn more > start 7-day free trial. Email, gateway name, location. Agree, create. Confirm the email, set a password. Choose a plan ($10 a month in S07's recording). Wait for "running". `[verify UI]` `[web check: current price and trial]` [530daade4029]
3. Finish setup > the gateway's own interface: set a password, same email, create account. `[verify UI]`
4. Add data source > Facebook login > connect > select the business account > select the pixel > continue. From here the pixel also sends to CAPI. `[verify UI]` [530daade4029]
5. Configure DNS > optimize. Pick a subdomain used by nothing else (S07: cpg). Enter the root domain and the subdomain. At the DNS provider add a CNAME: name = subdomain, target = the domain the gateway shows. On Cloudflare set proxy off. Save. Wait (about 1 minute on Cloudflare in S07's demo; minutes to hours elsewhere). Continue. Good: "optimized" with a green check. `[verify UI]` [530daade4029]
6. Wait 5 to 10 minutes (up to about 1 hour) before testing. [530daade4029]
7. Verify: P11 steps 2 to 4. [90f2da80bf67]
8. Blocker test: install Ghostery, turn it on, reload, filter Network. Expected: the Facebook request is blocked and no gateway request fires. If blocker resistance was the goal, the gateway has not met it (R55). [bab947623e26]
Checks after: dedup IDs match on every event type; no second server route is live (R47).
Rollback: disconnect the pixel in the gateway and remove the CNAME; the pixel keeps working as before.

### P13. Thank-you page key event without code (leads only)

Covered in P4 step 4. Not for purchases (R26). [e2bcc61df786]

### P14. Conversion rate by channel and medium

Goal: purchase-filtered conversion rate per channel and per medium for a period.
Preconditions: purchase event confirmed (P6). UTMs known (R66).
Steps:
1. Reports > Life cycle > Acquisition > Traffic acquisition. Set the date range (S05: last 28 days) and granularity. `[verify UI]` [5dde1ccb7160]
2. Primary dimension: Session primary channel group. Add a second dimension with the plus button: Session medium (S05) or switch the primary to Session source / medium (S01). `[verify UI]` [b84c5ad106a2] [a26e80bd2101]
3. Customize report > Metrics > add session key event rate, key events, total revenue, engaged sessions, engagement rate. Apply. On the session key event rate and key events columns, set the event selector to purchase. Save the report. `[verify UI]` [67d1533fdd9c] [d5605a4c54a8]
4. Add Session campaign name as a further dimension to see which campaign produced revenue (S01: 1 Black Friday newsletter produced most email revenue). Sort by sessions or revenue. `[verify UI]` [a26e80bd2101]
5. Paid social check: filter Session medium exactly matches the brand's paid medium value and Session source contains facebook (S01 sketch). `[needs brand data: UTM values]` [a26e80bd2101]
6. Export the table. Compute rates in code from key events and sessions; do not transcribe the UI's rate. Flag any row with sessions below the brand's minimum `[needs brand data: minimum sessions per row]`.
Checks after: the key event selector reads "purchase" on both columns; revenue per row is consistent with the purchase count per row.
Rollback: none.

### P15. Conversion rate per landing page

Goal: purchase-filtered conversion rate per entry page, with traffic mismatch ruled out.
Preconditions: P6. Landing page report location confirmed `[web check: current GA4 location of the Landing page report]`.
Steps:
1. Reports > Engagement > Landing page. `[verify UI]` [b700e12faf0c] [90bd1b325921]
2. Customize > add session key event rate and key events; set both to purchase. Save. `[verify UI]` [b700e12faf0c]
3. Sort by sessions. Compare pages with enough sessions. Note pages far above or below similar pages. [b700e12faf0c]
4. For a low page: add Session source / medium as a second dimension. If its traffic mix differs from the peer pages, the cause is traffic, not the page (R38). [b700e12faf0c]
5. Hand page and product hypotheses to 09-CRO with the numbers, computed in code.
Checks after: `/` is the homepage; revenue shown is for sessions that started on that page, not for checkout pages (R36, R37) [5c2c65569229].
Rollback: none.

### P16. Funnel and path reads

Goal: find where shoppers drop, with tracking gaps ruled out first.
Preconditions: P6.
Steps:
A. Purchase journey (standard report): Reports > Monetization > Purchase journey. Date range (S05: last 30 days). Read session started, viewed product, added to cart, began checkout, purchased; each step shows the share of the step before. The first drop is normal; read the cart, checkout and purchase drops (R86). `[verify UI]` [000e5a39ddc8]
B. Funnel exploration: Explore > Funnel exploration. Steps: view_item, add_to_cart, begin_checkout, (add_payment_info), purchase. Keep "indirectly followed by" (R40). Breakdown: Device category. Optional: Trended funnel, Make open funnel. `[verify UI]` [2cac3e89ff27] [ac9071a3bbdd]
C. Checkout journey: Reports > Monetization > Checkout journey. Breakdown Device category, then Browser. 1 browser dropping much more at 1 step: reproduce the checkout in that browser (R43). `[verify UI]` [ae2ed547485e]
D. Path exploration backward: Explore > Path > Start over > ending point Event name = purchase > switch node to Page path > expand backward past checkout pages. Forward from begin_checkout: users going to the account page and back may be a confusing login step (hypothesis). `[verify UI]` [85c9ae567054] [663dee00fd8e]
E. Compute step ratios in code and compare against the brand's own prior periods first, S06's 4:2:1 second (R87). `[needs brand data: prior step rates]`
Checks after: every step has counts; no step is 0 with volume before it (R89).
Rollback: none.

### P17. Campaign-only table and UTM check

Goal: a clean list of named campaigns and a check that tagging matches the convention.
Preconditions: UTM convention in the brand record.
Steps:
1. Explore > blank > name "Campaigns". Dimensions: Session campaign (add Session source, Session medium). Metrics: Sessions, Active users, Key events (purchase), Purchase revenue. Rows and values as needed. `[verify UI]` [8db1bf5fadc7]
2. Filters > Session campaign > Does Not Match Regex > `^\(.*\)$` > Apply. `[verify UI]` [8db1bf5fadc7]
3. Export. In code, compare every campaign, source and medium value against the convention. List mismatches (typos, wrong case, missing medium, paid social landing in Organic Social). [0d831192ef28]
4. Admin > Data display > Channel groups: confirm where the brand's paid social and paid shopping mediums land. Create a custom group only on a brand decision, and log it (R94). `[verify UI]` [0d831192ef28]
Checks after: no real campaign is hidden by the regex `[needs brand data: campaign naming rule]`.
Rollback: none.

### P18. Attribution model comparison read

Goal: report how much credit changes between Last Click and Data Driven per channel, without picking a winner.
Preconditions: Google Ads linked if paid search matters (12-GAD). Key events set (P4).
Steps:
1. Advertising > Key event attribution models. Key events selector: purchase only. `[verify UI]` [675a952696ec]
2. Export channels with key events and revenue under Last Click and under Data Driven, and the % difference column. [675a952696ec]
3. Advertising > Key event attribution paths: note path lengths and typical sequences (S03: several organic visits before converting). `[verify UI]` [675a952696ec]
4. Conversion management: list GA4 key events and Google Ads conversion actions; explain any count gap by Ads-only actions (R31). `[verify UI]` [a8f35cf35c8e]
5. Advertising segments: read remarketing list sizes before any campaign is planned on them; below-minimum lists go to 12-GAD as a blocker. `[verify UI]` `[web check: current Google Ads minimum list sizes]` [510ee3226e4d]
6. Report the gap per channel in code. Say in the report that the gap is not incrementality (R69, R71).
Checks after: the report names both models and the window used `[web check: current GA4 attribution settings and lookback windows]`.
Rollback: none.

### P19. Revenue-change triage (sessions x conversion rate x AOV)

Goal: name the lever behind a sales change before anyone explains it.
Preconditions: store figures for the period and a comparison period; GA4 sessions for both; refunds by refund date and order date.
Steps:
1. Pull net sales + shipping charges, sessions, conversion rate and AOV for both periods, filtered to Online Store if paid media is the driver (R63). `[verify UI]` `[needs brand data]` [9e9d4013f967] [6ca5944157b0]
2. Put all 3 levers on 1 basis in code: sessions from GA4 (or both, side by side), conversion rate = orders ÷ that session count, AOV = (net sales + shipping) ÷ orders. Note that Shopify's own 3 numbers will not multiply to the same revenue (R76). [9e9d4013f967] [9b3f534de0a2]
3. Returns first: if refunds by refund date spiked in the period, the dip may be return timing (R75). Report refunds separately by order month. [a3ae4e9e2a00]
4. Name the lever: AOV fell (product mix pushed toward lower-AOV items?), conversion fell (natural variance, a bot spike per P20, or a site change?), sessions fell (Shopping campaign spend down, CPM or CPC up, spend cut?). Each is a question to check, not an answer. [9e9d4013f967]
5. If every lever moved single digits and none sharply, report "no single cause; within normal variation" (R77) and flag for 09-CRO if the brand wants a test.
6. Run the same steps for a rise.
Checks after: the product of the 3 levers on the chosen basis reproduces the period revenue within rounding; if not, the basis is mixed.
Rollback: none.

### P20. Bot traffic check

Goal: decide whether a session spike or conversion dip is bots before anyone touches the site or the ads.
Preconditions: Shopify Sessions over time and GA4 sessions for the same dates.
Steps:
1. Plot Shopify sessions and GA4 sessions by day for the period, in code. A Shopify spike or dip absent from GA4 is suspect (R90). `[verify UI]` [084db9abd48b]
2. Shopify Analytics > Sessions by location > open the full report > sort by city. 1 city spiking against the market spread "often means" a server (S06). `[verify UI]` [57a97c0614d6]
3. Recompute conversion rate with GA4 sessions as the denominator for the same days. [084db9abd48b]
4. Report both rates with their denominators named. S06 gives no exclusion method; filtering in Shopify may need a third-party tool (S06 card). `[web check: Shopify bot filtering options]`
Checks after: the report says which denominator each rate uses.
Rollback: none.

### P21. Platform-to-store reconciliation

Goal: for 1 period, the gap between each platform's purchase count and revenue and the store's orders, with the reason for each gap class.
Preconditions: store order export (order id, timestamp in the store time zone, net sales, shipping, tax, discounts, refunds, channel, test flag); GA4 purchase count, purchase revenue and the transaction ID report; Meta Purchase count and value (`ads_get_dataset_stats`, read only); Shopify Analytics orders. All for the same 7 or 28 full days. No source gives this procedure; it is an ecomOS composite built from S03 [2fa8beb663c8], S05 [1735fbb29aff], S06 [a3ae4e9e2a00] and S04 [8d023b8f223e].
Steps:
1. Fix the frame: the store's time zone (R10), the Online Store channel only (R63), test orders out, currency as stored.
2. Store truth: orders and net sales + shipping (tax out, discounts out, returns as of the order date shown separately) (R74, R75).
3. GA4: Monetization > E-commerce purchases and the transaction ID report; export transaction IDs for the period. `[verify UI]` [2fa8beb663c8]
4. Join GA4 transaction IDs to store order ids in code. Classes: matched; in store not in GA4 (consent, blockers, checkout route not tagged, event failed); in GA4 not in store (test orders, duplicates from reload where transaction_id is missing, cancelled orders). Duplicated transaction IDs in GA4 mean the purchase event lacks a unique id or fires twice (R26).
5. Meta: Purchase count and value for the period from Events Manager (read only). Meta has no order id join in the sources; compare counts and value only. Near 2x = dedup failure (P11). Value gaps: currency, shipping and tax included or not `[needs brand data: what the Meta Purchase value contains]`.
6. Shopify Analytics vs store orders: they should match for orders; sessions and conversion rate are the suspect side (P20).
7. Compute coverage = platform matched count ÷ store orders, and value ratio = platform value ÷ store net sales + shipping, per source. Missing inputs give "unavailable".
8. Write the reconciliation table (9.1) and open a fix per gap class with an owner (9.2).
Checks after: every gap class has a reason or is marked unknown. No number in the table was typed from a screen.
Rollback: none.

### P22. Daily trust check

Goal: a pass, warn or fail per source for yesterday, published before any other agent reads the numbers.
Preconditions: read access to GA4, Events Manager (Meta MCP read tools), Shopify Analytics or Metabase, and the store order feed. Thresholds from section 6 and the brand record.
Steps (all computed in code; each step maps to checklist 5.6):
1. Arrival: GA4 Realtime or yesterday's event counts show page_view, view_item, add_to_cart, begin_checkout and purchase at volumes inside the brand's normal band `[needs brand data: normal daily bands]`. A step at 0 with volume before it is a fail (R89). [30843583e84d] [000e5a39ddc8]
2. Purchase integrity: GA4 purchases vs store orders for yesterday (P21 short form); duplicated transaction IDs = fail. [2fa8beb663c8]
3. Meta: browser and server copies present for each event type; dedup status intact; no duplicate warnings; Purchase count vs store orders within the band; no events landing in Test events from real visitors (test code leak). [8d023b8f223e] [e1c161b2fe2d] [90f2da80bf67]
4. Sessions: Shopify vs GA4 sessions within the brand's usual ratio; 1-city spike check. [084db9abd48b] [57a97c0614d6]
5. Revenue definitions: GA4 Total Revenue = Purchase Revenue unless explained; store net sales + shipping with tax out; refunds by refund date listed separately. [2fa8beb663c8] [a3ae4e9e2a00]
6. Settings drift: key event list, internal traffic filter state, retention, timeout, channel groups unchanged since the last log entry (R94). `[verify UI]`
7. Score each source (9.3) and publish with the data. Any fail blocks downstream reports for that source until fixed or overridden by the brand owner in writing.
Checks after: the score file for the day exists with every source rated, and every "unavailable" is explained.
Rollback: none.

### P23. New-source onboarding

Goal: a new data source (a new pixel, a new app, a new GA4 property, a Metabase card, an affiliate feed) enters ecomOS only after its definitions and coverage are known.
Preconditions: the source's owner and purpose named. ecomOS composite; the sources give only fragments (S02 R5, S05 R4, S06 R74).
Steps:
1. Record: what it measures, its definitions (sessions, order, revenue: tax in or out, shipping in or out, refund timing), its time zone and currency, its refresh cadence, what installed it and who owns it. [a3ae4e9e2a00] [5c923d97e1f7]
2. Map its metrics to ecomOS metric names. Any metric it cannot give is "unavailable", never derived by the model.
3. Run P6 (if it sends events), P11 (if it sends to Meta), P21 (if it reports purchases or revenue) for 7 full days in parallel with existing sources before it is used.
4. Decide its role: source of truth for which questions (R4), or a cross-check only.
5. Add it to the daily trust check (P22) with its bands and thresholds.
6. Log the go-live date in the brand record and annotate reports across it (R94).
Checks after: checklist 5.7 all rows pass.
Rollback: remove it from reports; keep the data.

### P24. Set or review the top metric

Goal: 1 named top metric, dated, with the sub-metrics each team owns and the metrics a win may break.
Preconditions: stage and bankroll known `[needs brand data]`.
Steps:
1. Executive team picks customers, revenue or profit (R79, R80). Record the date. [13ce65376d8f] [0c302f4b2883]
2. Map each department's sub-metrics to it (conversion rate, AOV, referral coefficient, retention) (S02 card wording). [13ce65376d8f]
3. List the metrics a tactic may hurt (LTV, customer quality, brand, CX) and how they will be watched (R83). [06aa9f46abe7]
4. Set the review cadence: big shifts quarterly at most; the metric itself about yearly; quick-win pushes of 2 to 4 weeks allowed (R81). [5869b757b0e7]
5. Track return per dollar on the main lever over time; when it flattens, propose the next lever (R82). [5869b757b0e7]
6. Frame every report from this folder on the top metric (R3).
Checks after: every department names the same top metric when asked (S02 diagnostic).
Rollback: a metric change is a dated event, never a silent edit.

### P25. Platform vs self-reported attribution

Goal: a written rule for the brand on how to read source conflicts.
Preconditions: a 1-question post-purchase survey in place (S02 names Fairing) `[verify UI]` `[needs brand data: survey tool and question]`.
Steps:
1. Export survey answers and the platform or GA4 credited source for the same buyers and window. [e11ec2148e14] [45d7e49e638b]
2. Compute the gap per channel in code (card 7f3bed7f5dd1). [7f3bed7f5dd1]
3. Write the rule: which view is used for which decision (S02 leaves this open; its cards favour self-report for strategic channel calls). Record it in the brand record. [e11ec2148e14]
4. Do not cut an over-claiming channel on platform data alone; propose an incrementality test through 24-DEP and 09-CRO (R71). [859e4f5b289d]
Checks after: the rule exists, is dated, and every channel report cites it.
Rollback: none.

## 5. Diagnostic checklists

Written so a worker can run each row. "Fix" names the procedure or rule. Every UI path carries `[verify UI]`.

### 5.1 Tracking audit (pixel, CAPI, GA4)

| # | What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|---|
| 1 | What installed GA4 and the pixel, and which integrations are live | Brand record; view page source; app list; DevTools Network filter "facebook" and "google" | 1 route per destination, documented | Unknown, or 2 server routes to Meta | P11 step 1; R47 | S07 [94681676110e], S04 |
| 2 | Google tag fires on storefront pages | GTM Preview > Initialization `[verify UI]` | Fired | Not fired | P2 | S01 [0aad0a745c66], S03 [9f5dc9b5cd04] |
| 3 | GA4 receives page_view with correct page_location | DebugView `[verify UI]` | Matches URL | Missing or wrong | P2 | S01 [80fdd796ee78], S03 [9bedc2d9534e] |
| 4 | Checkout and purchase route on a hosted checkout | Platform integration settings `[verify UI]` | Purchase arrives from the platform route | No purchase, or GTM assumed to cover checkout | P2 step 0; R60 | S03 caveat, S01 caveat |
| 5 | Meta pixel present with event ID | Meta Pixel Helper `[verify UI]` | Event ID on each event | No event ID | P8 step 2, or P12 | S07 [90f2da80bf67] |
| 6 | Pixel blocked before consent | GTM Preview, banner unanswered | "blocked by consent settings" | Fires before consent | P8 step 4 | S04 [1cdafb95b157] |
| 7 | Pixel fires on the opt-in page | Delete consent cookie, preview, Allow all | Fires on the same page | Only on page 2 | P8 step 5 | S04 [1cdafb95b157] |
| 8 | Server Meta tag status | Server preview > tag | "succeeded" | "failed" | Re-check token and pixel ID (P9) | S04 [8d023b8f223e] |
| 9 | Both streams land | Events Manager > Test events | 1 browser + 1 server per event | Only browser | Wait (R48), then trigger name and consent condition (P9 step 5) | S04 [8d023b8f223e] |
| 10 | Test code not in production | Non-preview visit; Events Manager | Live events in live data | Live events in Test events | P10 | S04 [e1c161b2fe2d] |
| 11 | CAPI credentials held as secrets | Secret store | Present there only | In a doc, chat or commit | Rotate (P7 rollback) | ecomOS rule 5 |
| 12 | Event match quality per event | `ads_get_dataset_quality` (read only) `[web check: fields]` | Customer information parameters sent; EMQ read and logged | Unavailable or low | Propose parameter fixes; never write (R51) | No source; `[web check]` |
| 13 | Internal traffic filter | Admin > Data filters `[verify UI]` | Active | Testing | P3 step 3 | S01 [92193cbedb5d] |

### 5.2 Event coverage check (GA4)

| # | What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|---|
| 1 | view_item, add_to_cart, begin_checkout, add_shipping_info, add_payment_info, purchase arrive | DebugView walk (P6) `[verify UI]` | All present with the route named | Any missing or "assumed" | P6 step 7 fix list | S01 [d6b4bece9591], S03 [ac9071a3bbdd] |
| 2 | purchase carries transaction_id, value, currency, items | DebugView event detail | All present, unique id per order | Missing id or value | Developer or app settings (P6); R26 | S03 [e2bcc61df786], `[web check]` |
| 3 | Item parameters (item_id, item_name, price, quantity) | DebugView items array | Present | Missing | Developer or app settings | S01 [d6b4bece9591] |
| 4 | Coupon, promotion, item list cards | Monetization > Overview `[verify UI]` | Populated when used | Empty | Parameters not sent (R32) | S03 [2fa8beb663c8] |
| 5 | Funnel steps have counts | Funnel exploration, last 7 days | Every step > 0 with volume before it | A step at 0 | Tracking gap (R89) | S05 [000e5a39ddc8] |
| 6 | Purchases audience non-empty | Admin > Audiences `[verify UI]` | Has users | Empty | purchase not sent | S03 [7425cd2ae91c] |
| 7 | Custom parameters registered | Admin > Custom definitions `[verify UI]` | Registered, event scope, exact key | Missing | P5 step 7 | S01 [a043dadb24a2] |
| 8 | Platform 100% Web | Tech > Overview `[verify UI]` | 100% Web | App share on a web-only property | Check data streams | S03 [f2f53af85949] |
| 9 | Key events list | Admin > Events > Key events `[verify UI]` | purchase marked; leads as unique events; page_view not marked | page_view or a thank-you page_view marked for sales | P4; R26, R27 | S03 [e2bcc61df786], S05 [d5605a4c54a8] |

### 5.3 Dedup check (Meta)

| # | What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|---|
| 1 | Event ID on the browser copy | Pixel Helper | Present | Missing | P8 step 3 | S07 [90f2da80bf67] |
| 2 | Event ID on the GA4 event reaching the server | Server preview > Event Data | Present | Missing | P9 step 1 | S04 [0954c80debf4] |
| 3 | Event ID in the outgoing CAPI request | Server preview > Meta tag request | Present | Missing | Parameter key `[web check]` | S04 [0954c80debf4] |
| 4 | Same ID on browser and server copies | Ctrl+F in Events Manager | Same | Different or missing | Fix wiring; do not trust counts | S04 [0954c80debf4] [8d023b8f223e] |
| 5 | Same event name on both copies | Events Manager | Same | Different | R46 | S04 caveat |
| 6 | Server copy marked deduplicated | Test events | Yes | No | P9 step 7 | S04 [0954c80debf4] |
| 7 | Checked per event type | Repeat rows 1 to 6 for PageView, ViewContent, AddToCart, InitiateCheckout, Purchase | All pass | Only PageView checked | P11 step 4 | S07 card [90f2da80bf67] |
| 8 | No duplicate warnings after a few days | `ads_get_dataset_quality` (read only) | None | Warnings or a conversion jump | P11 | S07 [90f2da80bf67] |
| 9 | Meta Purchase count vs store orders | P21 step 5, in code | Near 1x | Near 2x | Dedup failure; P9 or P12 | ecomOS from S04 |
| 10 | Only 1 server route live | Integration list | 1 | 2 or more | R47 | S07 [94681676110e], S04 caveat |
| 11 | Test code current | Test events tab before a session | Matches lookup row | Changed | P10 step 4 | S04 [e1c161b2fe2d] |

### 5.4 Attribution settings and UTM check

| # | What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|---|
| 1 | Reporting model and lookback windows recorded | Admin > Attribution settings `[verify UI]` `[web check: current location and options]` | Recorded in the brand record with a date | Unknown | Record; R69 | No source states them |
| 2 | Key events selector set to purchase in every read | Report column selector | purchase | All key events | R29 | S05 [d5605a4c54a8] |
| 3 | Campaign table clean | Regex filter (P17) | Only named campaigns | (organic), (direct), (not set) rows | P17 | S03 [8db1bf5fadc7] |
| 4 | UTMs match the convention | Export and compare in code | 0 mismatches | Typos, missing medium | Fix links; R66 | S05 [b84c5ad106a2], S01 |
| 5 | Paid social in the right channel group | Admin > Channel groups; Traffic acquisition | Paid social row exists | Landing in Organic Social | R68 | S03 [0d831192ef28] |
| 6 | User vs Traffic acquisition used for the right question | Report choice | Session-based for campaign reads | First-touch used for campaign reads | R33 | S01 [a26e80bd2101], S03 [0d831192ef28] |
| 7 | Last Click vs Data Driven gap reported, not resolved | P18 | Both shown, gap named | 1 model shown as truth | R69 | S03 [675a952696ec] |
| 8 | GA4 key events vs Google Ads conversions gap explained | Conversion management | Explained by Ads-only actions | Unexplained | R31; 12-GAD | S03 [a8f35cf35c8e] |
| 9 | Shopify attribution cards not used for decisions | Report review | Not cited | Cited as evidence | R62 | S06 [561513b3e85e] |
| 10 | Survey vs platform rule exists | Brand record | Written and dated | Missing | P25 | S02 [e11ec2148e14] |
| 11 | Buying window (Meta) matches 24-DEP | 24-DEP playbook | Consistent | Differs | Align with 24-DEP | 24-DEP |

### 5.5 Platform-to-store reconciliation

| # | What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|---|
| 1 | Same frame: time zone, channel, test orders out, currency | P21 step 1 | Documented | Mixed | Re-run | S03 [5c923d97e1f7], S06 [6ca5944157b0] |
| 2 | Store revenue = net sales + shipping, tax out | P21 step 2 | Labelled correctly | Total sales or gross sales used | R74 | S06 [a3ae4e9e2a00] |
| 3 | Refunds by refund date shown separately | P21 step 2 | Separate column | Netted silently | R75 | S06 [a3ae4e9e2a00] |
| 4 | GA4 transaction IDs join to store order ids | P21 step 4, in code | Coverage inside the brand's band `[needs brand data]` | Below band, or duplicate ids | Consent, route, or dedup fix (9.2) | S03 [2fa8beb663c8] |
| 5 | GA4 Total Revenue = Purchase Revenue | Monetization overview | Equal or explained | Unexplained gap | R30 | S03 [2fa8beb663c8] |
| 6 | Meta Purchase count vs orders | P21 step 5 | Near 1x | Near 2x or far below | P11 | ecomOS from S04 |
| 7 | Meta Purchase value basis known | Brand record | Documented (shipping and tax in or out) | Unknown | `[needs brand data]` | No source |
| 8 | Shopify Analytics orders = store orders | Compare | Equal | Differ | Channel filter (R63) | S06 [6ca5944157b0] |
| 9 | Every number computed in code | Script log | Logged inputs | Typed from a screen | R1 | ecomOS |
| 10 | Unavailable shown as unavailable | Table | "unavailable" | 0 | R2 | ecomOS |

### 5.6 Daily trust check

| # | What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|---|
| 1 | Events arriving at normal volume | GA4 event counts vs bands | Inside band | Outside band or a step at 0 | P22 step 1; P6 | S01, S03 [30843583e84d], S05 |
| 2 | GA4 purchases vs store orders (yesterday) | P21 short form | Inside band | Outside band; duplicate ids | P21 | S03 [2fa8beb663c8] |
| 3 | Meta browser + server + dedup intact | Events Manager read | Both copies, deduplicated | Missing stream or duplicates | P11 | S04 [8d023b8f223e] |
| 4 | Meta Purchase count vs orders | Read tools, in code | Inside band | Near 2x or far below | P11 | ecomOS from S04 |
| 5 | No real events in Test events | Events Manager | None | Some | P10 | S04 [e1c161b2fe2d] |
| 6 | Shopify vs GA4 sessions ratio | In code | Usual ratio | Spike or dip in 1 only | P20 | S06 [084db9abd48b] |
| 7 | 1-city spike | Sessions by location | Spread matches market | 1 city spikes | P20 | S06 [57a97c0614d6] |
| 8 | Revenue definitions unchanged | Report config | net sales + shipping, tax out | Changed | R74 | S06 [a3ae4e9e2a00] |
| 9 | Settings drift | Admin snapshot vs log | No change | Change without a log entry | R94 | S01, S05 |
| 10 | Trust score published | Score file | Every source rated | Missing | 9.3 | ecomOS |

### 5.7 New-source onboarding

| # | What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|---|
| 1 | Definitions recorded (sessions, order, revenue basis, refund timing, time zone, currency) | Brand record | All present | Any missing | P23 step 1 | S06 [a3ae4e9e2a00], S03 [5c923d97e1f7] |
| 2 | Metrics mapped to ecomOS names | Mapping file | 1 to 1 or "unavailable" | Model-derived | P23 step 2 | ecomOS |
| 3 | 7 days in parallel | P6, P11, P21 | Gaps explained | Unexplained | Hold | ecomOS |
| 4 | Role decided (truth or cross-check) | Brand record | Decided per question | Undecided | R4 | S05 [1735fbb29aff] |
| 5 | In the daily trust check | P22 config | Present with bands | Absent | P23 step 5 | ecomOS |
| 6 | Go-live logged | Brand record | Dated | Missing | R94 | ecomOS |
| 7 | Zero-party data reaches the CRM (survey or quiz sources) | CRM fields | Fields flow | Silo | R72 | S02 [e11ec2148e14] |

### 5.8 GA4 settings audit

| # | What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|---|
| 1 | Retention | Admin > Data retention `[verify UI]` | 14 months | 2 months | P3 step 1 | S01 [017251ba79b0], S03 [c01dc627e7b1] |
| 2 | Domains listed | Configure your domains | Every root domain | Missing | P3 step 2 | S01 [f965ebdb8cdc] |
| 3 | Internal traffic filter | Data filters | Active | Testing | P3 step 3 | S01 [92193cbedb5d] |
| 4 | Session timeout and engaged timer | Adjust session timeout | Brand decision, logged | Changed without a log | R20, R21 | S01 [ca9e3c7b6aec] |
| 5 | Google Signals | Data collection | Decision logged after consent review | On without review | R22 | S01 [374c795a2291], S03 [c01dc627e7b1] |
| 6 | Consent settings | Consent settings | Consent mode detected where required | Not set | R24 | S03 [c01dc627e7b1] |
| 7 | Time zone and currency | Property details | Match store | Differ | R10 | S03 [5c923d97e1f7] |
| 8 | Enhanced measurement | Stream settings | Reviewed; forms off | Defaults | R12 | S01, S03 [d5ffafc2403f] |
| 9 | Product links | Product links | Ads and Search Console linked if used | Missing | R24 | S03 [c01dc627e7b1] |
| 10 | Access | Property access management | Named people, right roles | Unknown accounts | Review | S03 [c01dc627e7b1] |

## 6. Thresholds and benchmarks

Confidence: number of sources that state the value. "1 (opinion)" means 1 presenter's preference. All examples are examples, never promises.

| Value | Number | Condition | Source | Confidence |
|---|---|---|---|---|
| Wait before trusting standard reports | 24 to 48 hours (S01); 12 to 24 hours (S03) | New install, event or dimension; keep the stricter 48 hours | S01 [0aad0a745c66], S03 [fbe6ee425691] | 2 (numbers differ) |
| Realtime latency | seconds; windows of last 5 and 30 minutes | Arrival checks only | S01, S03 [30843583e84d] | 2 |
| Event data retention | 14 months (default 2) | Every property, at creation | S01 [017251ba79b0], S03 [c01dc627e7b1] | 2 |
| Session timeout | 30 minutes default; S01 sets at least 4 hours, often 7 hours 55 minutes | Brand decision; comparability cost | S01 [ca9e3c7b6aec] | 1 (opinion); conflict C5 |
| Engaged session timer | 10 seconds default; S01 sets 30 seconds or more | Brand decision | S01 [ce843bc07545], S05 uses 10 s [22a5b5e7d62e] | 1 (opinion) vs 1 default |
| Active user definition (as S01 explains it) | 10 s engagement, or a key event, or 2+ page views, or new user | Reading user counts | S01 [5c2c65569229] | 1 `[web check]` |
| Google Signals demographics delay | weeks | After enabling | S01 [374c795a2291] | 1 |
| Scroll event trigger | 90% of page | Enhanced measurement on | S03 | 1 |
| Home card default range | last 14 days | GA4 Home | S03 | 1 |
| Streams per property | 1 web stream (several sites); apps separate | Property design | S01 [a61d1986b945], S03 [5c923d97e1f7] | 2 |
| Access to create or mark key events | marketer, editor or admin | GA4 | S03 [e2bcc61df786] | 1 |
| Campaign-only regex | `^\(.*\)$`, Does Not Match Regex | Session campaign filter | S03 [8db1bf5fadc7] | 1 |
| Example store purchase conversion rate | 1.7% overall, purchase-filtered, about 28 days | 1 Shopify store; example only | S05 [d5605a4c54a8] | 1 (example) |
| Funnel average | 4 : 2 : 1 (add to cart : reach checkout : purchase); 25% overall from cart | "General average", check against your vertical | S06 [c8e57ed1cd0a] | 1 (client experience) |
| Funnel target | 2 : 1 : 1 | FMCG and low-ticket brands | S06 [c8e57ed1cd0a] | 1 (client experience) |
| Funnel fix lift | +40% to +50% conversion "overnight" | After fixing a big step drop | S06 [c8e57ed1cd0a] | 1 (anecdote) |
| S05 funnel example | about 10K sessions; 53% viewed product; "99.2%" (probable error, likely 9.2%) added to cart; 63% began checkout; 50% purchased | 1 store, 30 days; do not cite | S05 [000e5a39ddc8] | 1 (transcription error, R88) |
| Natural fluctuation | single-digit % moves across levers | No lever moved sharply; no test given | S06 [9e9d4013f967] | 1 (opinion) |
| Return-timing example | 20% of a strong month's orders returned next month | Fashion | S06 [a3ae4e9e2a00] | 1 (example) |
| Shipping share of revenue example | 7% to 8%; real AOV about 7% higher than Shopify AOV | 1 client | S06 [9b3f534de0a2] | 1 (example) |
| Shopify AOV formula (presenter's reading) | (gross sales minus discounts) ÷ orders, no shipping | `[web check]` | S06 [9b3f534de0a2] | 1 |
| Sessions gap | GA4 generally lower than Shopify | Bots in Shopify | S06 [084db9abd48b] | 1 |
| Meta gateway claimed lift | up to 13% better cost per result; 7% more conversions | Meta's claim, quoted | S07 [94681676110e] | 1 (vendor claim); conflict C6 |
| Gateway realistic gain vs blockers | "at best 1 or 2%" | Presenter estimate, unmeasured | S07 [bab947623e26] | 1 (opinion); conflict C6 |
| Gateway cost | Stape $10 a month, 7-day trial; Meta-hosted from about $30 | At recording | S07 [530daade4029] | 1 `[web check]` |
| DNS propagation | minutes to hours; about 1 minute on Cloudflare | Gateway CNAME | S07 [530daade4029] | 1 |
| Gateway subdomain live | 5 to 10 minutes; up to about 1 hour | After "optimized" | S07 [530daade4029] | 1 |
| Server event delay | arrives after the browser event; no figure | Events Manager checks | S04 [0b762a508449] | 1 |
| Dedup key | identical event ID (S04); plus identical event name (Meta rule per S04 caveat) | Every event sent both ways | S04 [0954c80debf4] | 1 + `[web check]`; conflict C8 |
| Test event code freshness | may change day to day | Before each test session | S04 [e1c161b2fe2d] | 1 |
| Top metric lifespan | about 1 year; big shifts quarterly at most; quick wins 2 to 4 weeks | Company level | S02 [13ce65376d8f] [5869b757b0e7] | 1 (opinion) |
| Founder customer calls | at least 1 a week, first 3 years | Opinion | S02 [7e8ec204ea88] | 1 (opinion) |
| Qualitative focus | top 3% loyal, bottom 3% haters | Second-hand heuristic | S02 [375f45ad5513] | 1 (second-hand) |
| Analytics decision size | $1M business: $5K to $15K decisions; $100M: $1M to $10M | Illustrative | S02 [11a74e34ca53] | 1 (illustration) |
| Churn interview trigger | no purchase 1 year after last | Physical products, example | S02 [7e8ec204ea88] | 1 (example) |
| Compounding arithmetic | $10,000 x 1.01 = $10,100; 100 x 1.05 = 105 | 1-time step, not compounding | S02 [3a1918a526e2] | 1 (flawed, R85) |
| EMQ score, dedup rate, coverage bands, "(not set)" share, minimum sessions per row | none given | | No source | 0 `[needs brand data]` `[web check]` |

## 7. Where sources disagree

Each conflict: what each side says, when each is right, what the agent should do. Conflicts are kept, not averaged.

**C1. Thank-you page view vs purchase event as the sales key event.** S03 creates a key event from page_view with URL contains "thank-you" and marks it key; it does so for a lead form (generate_lead), not a sale [e2bcc61df786]. S05 shows key events include non-purchase events and filters every rate to purchase [d5605a4c54a8]. S01 names purchase as the key event example [70e866a19de2]. When each is right: a URL match is fine for a lead page that cannot fire its own event. For sales it double counts reloads and revisits and carries no value, items or transaction_id. What the agent should do: mark purchase (with transaction_id) as the only sales key event (R26). Use S03's method only for leads, and log the counting choice (R28). `[web check: GA4 purchase dedup by transaction_id]`

**C2. GTM everywhere vs native Shopify pixels.** S01 and S03 prefer GTM for flexibility and assume "GTM on all pages" [53bd7d4a85c1] [9f5dc9b5cd04]. Both are platform-neutral; both sources' caveats say Shopify checkout cannot load GTM and that the Google & YouTube app or customer events pixels are the route. S05 says to link GA4 "using the Shopify integration" with no steps [1735fbb29aff]. S04 says a native Shopify Meta channel may already send CAPI [0b762a508449]. When each is right: GTM for storefront pages on any platform, and everywhere on a custom site. Native routes for Shopify checkout and purchase, and for CAPI if the Meta channel app is live. What the agent should do: audit routes first (checklist 5.1 row 1), never run 2 server routes to Meta (R47), treat every Shopify step as `[web check: current Web Pixels API, Google & YouTube app event list, Meta channel CAPI behaviour]`. The sources are thin here; the agent must say so in its deliverable.

**C3. Data retention scope.** S01: explorations only reach the retention window [017251ba79b0]. S03 transcript: "more historical data available in your reports"; its card narrows to Explore [c01dc627e7b1]. Both agree on 14 months. What the agent should do: set 14 months on day 1 either way. Do not tell a brand that standard reports lose history without a `[web check: retention effect on standard reports]`.

**C4. Google Signals on day 1 or not.** S01 lists it among 5 day-1 settings with "talk to legal first" for strict companies [374c795a2291]. S03 says enable it and names Consent Settings separately [c01dc627e7b1]. Neither presenter works in the brand's market. Common privacy-first advice adds consent checks and possible data thresholding. When each is right: a brand with consent mode live and no regional restriction can enable it for directional demographics. What the agent should do: treat Signals as a decision after a consent review per selling country (R22), never a default, and log it `[web check: current Signals behaviour, thresholding, consent requirements]`.

**C5. Session timeout: 30 minutes vs 4 hours or the 7 hour 55 minute maximum.** S01's presenter extends it to cut "(not set)" and checkout landing pages and admits "some people might disagree" [ca9e3c7b6aec] [c91c77718ecd]. S03 never raises it. Common practice keeps 30 minutes for comparability with ad platforms and history. When each is right: a long timeout suits a brand that reads landing pages daily and never compares session counts to other tools; 30 minutes suits any brand that compares sessions across GA4, Shopify and ad platforms, which is every ecomOS brand (P20, P21). What the agent should do: keep 30 minutes unless the brand owner decides otherwise in writing; log the date; annotate every report across the change (R20, R94). Same for the engaged timer (R21).

**C6. CAPI lift claims: Meta's 7% to 13% vs S07's 1% to 2%.** Meta says the gateway can improve cost per result by up to 13% on average and raise conversions by 7%; S07's presenter quotes them and says the real gain against aggressive blockers is "at best 1 or 2%" [94681676110e] [bab947623e26]. Neither is measured on a store. Meta's figure is a vendor claim about the gateway; S07's is a guess about blocker recovery only, and he sells the alternative. What the agent should do: cite both with their basis; put no lift number in a business case; propose a measured before-and-after in Events Manager if the brand tests any route `[needs brand data]`.

**C7. Gateway as a stopgap vs never.** S07's cards say "quick stopgap" and "start on the gateway, then move to a server container" [94681676110e] [21d5b62f2a73]. The S07 transcript says "I don't recommend it" and never proposes a staged path. S04 builds the server-side route directly [0b762a508449]. When each is right: a hard-coded pixel, no developer, no platform app, and a brand that accepts no blocker recovery: the gateway adds CAPI and automatic dedup for $10 a month. Any brand with a platform app or a developer: server-side or the native route. What the agent should do: apply R57's 3 conditions; if the gateway is chosen, write it as a stopgap with a review date, which is the card's stance, and say the source itself did not recommend it.

**C8. Dedup by event ID only vs event name plus ID within a window.** S04 says only the event ID must match [0954c80debf4]; its own setup keeps names aligned and its caveat notes Meta documents name plus ID within a time window. S07 says the gateway handles dedup automatically [90f2da80bf67]. What the agent should do: enforce the strictest condition (same name and same ID, checklist 5.3 rows 4 and 5), and `[web check: Meta dedup rules and window]` before writing any dedup spec.

**C9. Which attribution to trust: platform, self-report or neither.** S02's presenter leaves it to the analyst [e11ec2148e14]; his cards favour self-report for strategic channel calls and say first-party is "unreliable for attribution" [45d7e49e638b] [7f3bed7f5dd1] [9c479169d7e9]. S03 shows Last Click and Data Driven side by side and settles nothing [675a952696ec]. S06 says Shopify attribution is "futile" [561513b3e85e]. No source gives an incrementality method; card 859e4f5b289d sketches one. What the agent should do: report gaps between views, never 1 view as truth (R69, R70); write the brand's rule (P25); route any spend reallocation through 24-DEP with an incrementality proposal (R71).

**C10. Shopify attribution cards: ignore vs triangulate.** S06's presenter: ignore all of them [561513b3e85e]. Card 561513b3e85e: 1 input among several. What the agent should do: never cite a Shopify attribution or referral card as evidence for a budget move (R62). It may appear in a triangulation table with GA4 and UTMs, labelled as a low-trust signal.

**C11. Vanity metrics vs revenue metrics.** S02: single-line "revenue up month over month" charts and reports made to celebrate are not analytics; judge email send by send on revenue per channel [11a74e34ca53] [3a1918a526e2]. S05: a key event rate is not a conversion rate until filtered to purchase [d5605a4c54a8]. S06: session type cards and attribution cards carry "no real core information" [561513b3e85e]. No source names open rates or click rates directly; email metrics live in 14-EML. What the agent should do: every deliverable leads with the top metric and revenue-based measures computed in code (R3, R79); engagement, open-rate style and platform-claimed metrics appear only as supporting rows with their basis named, never as the headline.

**C12. Returns: add back or show separately.** S06's presenter adds returns back into reporting for some clients so marketing decisions are not skewed by refund timing, and also calls net sales + shipping (which deducts returns) "the best measure" [a3ae4e9e2a00]. Card a3ae4e9e2a00: show refund timing separately by order cohort; never call the add-back cash. What the agent should do: report 2 columns, net sales + shipping as booked, and refunds by original order month; decide per brand return rate `[needs brand data: return rate]`; never present an add-back as cash or profit (R75).

**C13. Sources doing arithmetic out loud.** S06: 5% AOV dip plus 4% conversion dip called "a 10% dip" (computed 8.8%) [9e9d4013f967]. S02: "$11,000" corrected to "$10,100" for a 1% lift, and "compounding" that is a 1-time step [3a1918a526e2]. S02's beauty box story says both "wasn't given permission" and "was able to run" the test, with "about $1M a month" and no traffic, duration or significance [129ad3db527d]. What the agent should do: never repeat a source's arithmetic; recompute in code (R1); mark case results as examples.

**C14. The 99.2% add-to-cart figure in S05.** The transcript says "only 99.2%" of product viewers added to cart; card 000e5a39ddc8 follows it ("most viewers added to cart"). The word "only" and the same store's 1.7% purchase rate fit 9.2%, not 99.2% (R88). What the agent should do: cite neither number as a benchmark; use the brand's own funnel history `[needs brand data]`.

**C15. "Cash collected" label.** S06's presenter calls net sales + shipping "cash collected" and "gross income within the P&L". Card a3ae4e9e2a00: it is sales-based, may include unpaid orders, and cash sits in payments reports. What the agent should do: use the formula, label it "net sales + shipping", and take cash from payments or finance reports (R74). Definitions of profit and contribution: 20-FIN.

**C16. Meta "recommends" the redundant setup.** S04 states it without a citation [0b762a508449]. It matches common advice. What the agent should do: keep the redundant setup as the default and `[web check: Meta's current recommendation]` before quoting Meta.

**C17. The second GTM snippet.** S01's presenter says the noscript snippet "can be ignored". Google's install instructions place it after the opening body tag. What the agent should do: install both (P2 step 2) `[web check: current GTM install instructions]`.

**C18. S01's list of 5 day-1 settings is unstable across its own cards.** Transcript: retention, domains, internal traffic, timeout plus engaged timer, Signals. Card 8f32ae745a5b drops Signals and splits the timer; card d2833e8633f3 omits the timer; cards 48b668a95917 and the transcript agree. What the agent should do: use the transcript order (R23).

**C19. Business objectives at property creation.** S01 picks "other business objectives" to get the older layout; S03 picks "Other Business Objectives" for the fullest report set. Same click, different reasons, both preferences. What the agent should do: pick it for the full report set; adjust the menu in Library later (R11).

**C20. Exclusion audience build order.** Card 7425cd2ae91c keeps the default include group and adds the exclude group; the S03 transcript deletes the include group first. What the agent should do: follow the transcript and `[verify UI]`.

**C21. "(not set)" landing page myth.** S01's Analytics Advisor and some blog posts say a custom event before page_view causes "(not set)" landing pages; the S01 presenter's experiments say it does not [bb64df0f76c5]. What the agent should do: do not repeat the myth; investigate session breaks and timeout (R37, R42).

## 8. Common mistakes

Merged from all sources, deduplicated, with the fix.

1. Publishing a tag without testing in Preview and DebugView. Fix: R15, P2. [80fdd796ee78] [9bedc2d9534e]
2. Expecting full reports the same day. Fix: R16; Realtime for arrival only. [0aad0a745c66] [fbe6ee425691]
3. Expecting ecommerce reports to fill without sending ecommerce events. Fix: P6, R25. [d6b4bece9591]
4. Marking page_view, or a thank-you page view, as the sales key event. Fix: R26, R27. [e2bcc61df786]
5. Reading session key event rate as conversion rate without the purchase filter. Fix: R29. [d5605a4c54a8]
6. Reading User acquisition when the question is per-session channel performance. Fix: R33. [a26e80bd2101] [0d831192ef28]
7. Judging page value by revenue in Pages and screens. Fix: R36. [5c2c65569229]
8. Leaving retention at 2 months. Fix: R19. [017251ba79b0] [c01dc627e7b1]
9. Changing the reporting time zone after data starts. Fix: R10. [5c923d97e1f7]
10. Separate properties for sites in 1 journey, or missing domains in Configure your domains. Fix: R8, R14. [60bd489184a8] [f965ebdb8cdc]
11. Defining internal traffic and leaving the filter in Testing. Fix: R18. [92193cbedb5d]
12. Event names with capitals or spaces; parameters not registered. Fix: R17. [23f8bf44b13a] [a043dadb24a2]
13. Changing session timeout or the engaged timer and then comparing to history. Fix: R20, R21, R94. [c91c77718ecd]
14. Enabling Google Signals without a consent review; treating demographics as accurate. Fix: R22. [374c795a2291] [3d2bb5de8e28]
15. Trusting Analytics Advisor or Insights for causes or date ranges. Fix: R41. [bb64df0f76c5] [7cef7f4d4e54]
16. Reading "(not set)" as an error or as 0. Fix: R2, R42. [d54ee95e619b]
17. Expecting GA4 key events to equal Google Ads conversions. Fix: R31. [a8f35cf35c8e]
18. Leaving campaign tables full of (organic), (direct), (not set). Fix: R67. [8db1bf5fadc7]
19. Picking "directly followed by" in a funnel by accident. Fix: R40. [ac9071a3bbdd]
20. Stopping the Meta build at "both streams fire". Fix: R44, R45, P9 step 7. [0b762a508449] [0954c80debf4]
21. Trusting automatic event ID forwarding without searching for the ID. Fix: R45. [0954c80debf4]
22. Checking dedup on PageView only. Fix: checklist 5.3 row 7. [90f2da80bf67]
23. Leaving a test event code in a published tag. Fix: R54, P10. [e1c161b2fe2d]
24. Using Initialization - All Pages for a consent-gated pixel. Fix: R53. [1cdafb95b157]
25. Sending to Meta without consent where consent applies. Fix: R52. [44e509c9fd36]
26. Assuming GTM variables carry across containers. Fix: R49. [729a4812f715]
27. A server trigger's custom event name not matching exactly. Fix: R50. [44e509c9fd36]
28. Calling a server tag broken before the delay has passed. Fix: R48. [0b762a508449]
29. Buying the gateway to beat ad blockers, or expecting longer cookie life from it. Fix: R55. [bab947623e26] [21d5b62f2a73]
30. Quoting Meta's 13% and 7% as expected results. Fix: R56. [94681676110e]
31. Reusing a shared subdomain, leaving the Cloudflare proxy on, or testing before DNS is live. Fix: R58. [530daade4029]
32. Running the gateway or GTM CAPI on top of a platform app that already sends CAPI. Fix: R47. [94681676110e]
33. Storing tokens in text files or docs. Fix: ecomOS rule 5, P7. [729a4812f715]
34. Using total sales (tax in) or gross sales as the revenue number. Fix: R74. [a3ae4e9e2a00]
35. Reading a return-driven revenue dip as ad performance falling. Fix: R75. [a3ae4e9e2a00]
36. Reading loyalty from returning customer rate. Fix: R64. [8f85f33352f5]
37. Acting on Shopify AOV alone, or forgetting it excludes shipping. Fix: R65. [9b3f534de0a2]
38. Trusting Shopify sessions and conversion rate without a GA4 cross-check. Fix: R61, P20. [084db9abd48b]
39. Using Shopify attribution or referral cards for decisions. Fix: R62. [561513b3e85e]
40. Blended revenue across POS, Shop app and draft orders when judging paid media. Fix: R63. [6ca5944157b0]
41. Stressing over single-digit lever moves; or trusting a presenter's arithmetic. Fix: R77, R1. [9e9d4013f967]
42. Citing S05's funnel example, or S06's 4:2:1, as an industry benchmark. Fix: R87, R88. [000e5a39ddc8] [c8e57ed1cd0a]
43. Reading a funnel drop before confirming every step is tracked. Fix: R89. [000e5a39ddc8]
44. Comparing product pages on tiny session counts. Fix: R38. [b700e12faf0c]
45. Single-line revenue charts; reports that end without a decision. Fix: R3. [11a74e34ca53] [3a1918a526e2]
46. Computing cost of acquisition only after paid ads start; not logging data early. Fix: R5. [776e59649374]
47. Swapping the top metric monthly; not telling departments which it is. Fix: R79, R81. [13ce65376d8f]
48. Scaling a winner without listing what it may break. Fix: R83. [06aa9f46abe7]
49. Letting the HiPPO pick the charts. Fix: R84. [129ad3db527d]
50. Trusting 1 attribution view as truth, or cutting a channel on platform data alone. Fix: R69, R70, R71. [675a952696ec] [7f3bed7f5dd1]
51. Leaving survey and quiz answers in a silo. Fix: R72. [e11ec2148e14]
52. Presenting a number the model computed. Fix: R1. ecomOS.
53. Showing 0 where the value is missing. Fix: R2. ecomOS.

## 9. Deliverables

Every deliverable is produced by a script, with inputs logged, and states the period, time zone, channel filter and the source of each number. Plain English, short sentences, digits, no em dashes, below tenth-grade reading level. No GPT or .env mentions on client pages.

### 9.1 Audit table (tracking, event coverage, dedup, settings, reconciliation)

Format: 1 row per check from section 5, with columns: check id (5.x row), what was checked, how (tool, path, date), result (pass, fail, unknown), evidence (screenshot name, export file, tool output id), owner, fix id (9.2). "Unknown" is used when the check could not be run (no access, feature unavailable, `[web check]` outstanding); it is never left blank and never counted as pass. The reconciliation block adds: store orders, GA4 matched, GA4 unmatched by class, Meta count and value, Shopify orders, coverage ratio and value ratio per source, each "unavailable" where an input is missing.

### 9.2 Fix list with owner

Format: fix id, what is wrong (1 line), evidence (audit row), the rule it breaks (R number), the proposed change (a proposal for GA4, GTM, Shopify or Meta; Meta changes are never applied by the agent), owner (developer, app admin, GTM editor, Meta admin, brand owner), effort (small, medium, large), risk to data if left, due date, verification step (which checklist row proves it fixed). Ordered by risk to data, then effort.

### 9.3 Trust score per source per day

Format: 1 row per source per day (GA4, Meta Events Manager, Shopify Analytics, store orders or Metabase, any onboarded source). Columns: date, source, checks run, checks passed, checks failed, checks unavailable, score (passed ÷ run, computed in code, "unavailable" if 0 checks ran), status (pass: no fails; warn: only band deviations; fail: any integrity fail such as duplicate transaction ids, missing purchase event, dedup broken, test code leak), the failing check ids, the note. A "fail" blocks that source's numbers in downstream reports until fixed or overridden in writing. The score file is appended daily and never edited in place.

### 9.4 CAPI enrichment spec draft (gross profit and COGS)

Purpose: a proposal for sending profit-based values to Meta so bidding can optimise on margin, not revenue. No source in this folder covers it; this is an ecomOS spec to be reviewed by 20-FIN and applied by a Meta admin, never by the agent. Format: (a) goal and the top metric it serves (R79); (b) events in scope (Purchase first); (c) fields: order id, order value basis (net sales + shipping, tax out, R74), COGS per line from `[needs brand data: COGS per SKU]`, shipping cost per order `[needs brand data]`, payment fees `[needs brand data]`, gross profit = value minus COGS minus shipping cost minus fees (definition from 20-FIN), currency, transaction time in the store time zone; (d) which field goes where (a custom parameter or the value field; Meta's current options `[web check: Meta CAPI custom data fields and value optimisation requirements]`); (e) dedup: same event ID and name as the browser Purchase (R44 to R46); (f) privacy: customer information parameters hashed per Meta rules `[web check]`, consent gating (R52); (g) test plan: P9 step 7 dedup check, then 7 days of P21 with the value ratio, then a proposed before-and-after read in Events Manager; (h) rollback: revert the server tag version. Every profit number is computed in code from brand data; if COGS is missing for a SKU, gross profit for that order is "unavailable" and the order is excluded from value, with the count reported.

### 9.5 Report reads (channel, landing page, funnel, triage)

Format: question, period, source of truth used (R4), the table exported from the tool, the computed rates with denominators named, the "(not set)" and "unavailable" shares, the settings in force (key events, timeout, channel groups, attribution model), the decision the read supports (R3), and what would change the decision. Hypotheses (mobile gap, checkout loop, bot spike) are labelled hypotheses with the next check.

### 9.6 Settings log

Format: date, property or container, setting, old value, new value, who decided, why, reports affected. Appended, never edited.

## 10. What needs live data or a web check

### 10.1 `[needs brand data]`

- Store platform, plan, theme, checkout domain, whether checkout is hosted, apps installed (R13, R60, P2 step 0).
- Every domain a shopper touches from landing to thank-you page (R8, R14).
- Business time zone and store currency (R10, P1).
- Selling countries and the consent rules that apply; markets served (R22, R52).
- What installed GA4 and the pixel; which Meta integrations are live; whether CAPI is already active (R47, R57, P11).
- Which Business Manager owns the pixel and who administers it (P7, P12).
- Who manages DNS and where (P12).
- Consent tool and its dataLayer event name (P8).
- Event map from store events to Meta standard events; the store's conversion events and their dataLayer names (R51, P8 step 6).
- What the Meta Purchase value contains (shipping, tax) (P21 step 5).
- GA4 ecommerce event coverage and item parameters as they arrive (R25, P6).
- Test order policy (P6).
- Office, warehouse and agency IPs and whether they are static (R18, P3).
- Typical time from first visit to purchase (R20).
- Value per lead; exact confirmation URL pattern (P4 step 4).
- Theme CSS classes for tracked elements (P5).
- Site search event name and whether search_term is captured (R39).
- UTM template for Meta, Google, email and affiliate links; campaign naming rule (R66, R67, P17).
- Minimum sessions per row and per landing page for a stable rate (R38, P14).
- Baseline engagement rate, funnel step rates, landing page rates, "(not set)" share, normal daily event bands, Shopify vs GA4 session ratio (R42, R87, P22).
- Order export with order id, timestamp, net sales, shipping, tax, discounts, refunds by refund date and order date, channel, test flag (R73, R74, R75, P21).
- Sales by channel (R63).
- Return rate by month and by order month (R75, C12).
- Shipping charges as a share of revenue; AOV distribution; new vs returning AOV (R65).
- Shopify vs GA4 sessions for the same dates (R90, P20).
- Cohort table (R64; reading in 20-FIN).
- Survey answers and platform credit for the same buyers and window; survey tool and question (R70, P25).
- All acquisition cost lines before paid ads and new-customer counts (R5).
- Spend and result by lever over time (R82).
- Stage and bankroll (P24).
- Customer list ranked by orders or LTV; refund, complaint and review records (R95).
- COGS per SKU, shipping cost per order, payment fees (9.4).
- Before and after event counts, match rate and dedup status if any CAPI route is tested (R56).

### 10.2 `[web check]`

- Current GA4 admin menu names and report locations, including the Landing page report (every `[verify UI]` step).
- Date and scope of the conversions to key events rename (S01, S03, S05 date signals).
- GA4 purchase deduplication by transaction_id and its window (R26, C1).
- GA4 recommended ecommerce events and parameters (R32).
- GA4 counting options for key events and Google's guidance per event type (R28).
- Retention effect on standard reports vs explorations (R19, C3).
- Full current GA4 engaged-session definition and the timer's maximum (R21).
- Current Google Signals behaviour, reporting thresholds and consent requirements per market (R22, C4).
- Consent mode v2 setup for the store's platform and markets (R24).
- GA4 attribution settings: reporting model default, lookback windows, channels that can receive credit (R69, checklist 5.4).
- GA4 default channel group rules for paid social and paid shopping (R66, R68).
- Google Ads minimum remarketing list sizes (S03 Advertising segments; 12-GAD).
- Cross-domain limits with third-party hosted checkouts (R14).
- Current GTM install instructions (second snippet) (C17).
- Current Shopify GA4 install path; Google & YouTube app event list; Shopify customer events (Web Pixels API); Meta channel CAPI behaviour and how it dedups with a GTM or gateway setup (R13, R47, R60, C2).
- Shopify help docs: AOV formula, returning customer rate definition, sessions and bot filtering, dashboard customisation by plan (R61, R64, R65, P20).
- Current Shopify funnel benchmarks by vertical and price point (R87).
- GA4 bot filtering behaviour (R61).
- Meta's current redundant setup recommendation (R44, C16).
- Meta dedup rules, required matching fields and the dedup window (R46, C8).
- Meta customer information parameters, hashing rules and EMQ guidance; where Events Manager shows EMQ and dedup status; which fields the Meta MCP dataset read tools return (R51, P11).
- Exact parameter key the Stape Meta CAPI tag reads for the event ID (P9 step 1).
- Event ID and CAPI templates still in the GTM gallery and maintained (P8 step 2).
- Server GTM hosting options and cost; Stape custom loader and cookie extension features; independent alternatives (R59, P9).
- Current Stape and Meta CAPI Gateway pricing, trial and hosting options; Meta-hosted gateway setup (R58).
- Meta CAPI custom data fields and value optimisation requirements (9.4).
- Current consent requirements for Meta in the brand's markets (R52).
- Privacy rules for buying or using third-party data per country (R72).
- Presenter identities and business models where credibility depends on them (S01 Julius, S02 eCommerceTech.io revenue model, S07 Stape relationship) (section 12).
- Who at ProfitWell stated the 3% rule (R95).

## 11. Freshness and stale-risk notes

- **GA4 UI (high risk, re-verify every session).** Admin groups ("Data display", "Data collection and modification"), report names (Purchase journey, Checkout journey, Landing page location), Explore controls, Analytics Advisor (beta), Reports snapshot templates and business objectives all moved between the sources' recordings and can move again. Every P1 to P6 and P14 to P18 step carries `[verify UI]`. S01, S03 and S05 are 2025 to 2026 snapshots; S01's presenter says Google may rename menus at any time.
- **GA4 definitions (medium risk, re-verify quarterly).** Engaged session definition and timer maximum, active user definition, retention scope, key event counting options, attribution settings, default channel group rules, purchase dedup by transaction_id. Rules R19, R21, R26, R28, R68, R69.
- **Google Signals and consent (medium risk, re-verify quarterly and on any regional law change).** R22, R24, R52. The sources give no market-specific rule.
- **Meta CAPI features (high risk, re-verify monthly).** Events Manager labels ("Dataset ID"), token generation location, test events, dedup display, EMQ display, gateway pricing and hosting, the Meta MCP dataset tools' fields, custom data fields for value optimisation. Rules R44 to R59, P7 to P12, 9.4. S04 and S07 are undated recordings filed in Sep 2026.
- **GTM templates (medium risk, re-verify quarterly).** Facebook Pixel template by facebookarchive, Facebook Conversions API template by Stape, Event ID templates by Markus Baersch and Stape. Gallery templates can be deprecated. P8, P9.
- **Shopify (high risk, re-verify monthly).** Checkout tagging limits, Web Pixels API customer events, Google & YouTube app event list, Meta channel CAPI, Analytics dashboard cards and metric names ("Shipping charges" was "shipping collected" per S06), AOV and returning customer rate definitions, bot handling, dashboard customisation by plan. Rules R60 to R65, P19, P20. S06 is undated.
- **Prices and trials (high risk).** Stape $10 a month and 7-day trial; Meta-hosted gateway from about $30 (S07). R58.
- **Vendor claims (high risk).** Meta's 13% and 7% gateway figures (S07). R56, C6.
- **Tool names (medium risk).** Fairing (formerly EnquireLabs), Octane AI, Typeform, Hotjar, Stape, Ghostery, Meta Pixel Helper. S02 tool names date from about 2023.
- **Slow-aging content.** S02's decision principles (1 top metric, S curve, HiPPO, data tiers), S06's revenue identity and return-timing warning, S05's "filter to purchase" rule, S04's dedup logic. These need no re-verification beyond the UI steps that implement them.
- **Card additions.** Several rules note claims that exist only in a card, not the transcript (S01 section 9 list, S02 incrementality cards, S03 card differences, S06 card paths and lists, S07 stopgap framing). Treat each as the card writer's view until a `[web check]` or brand data confirms it.

## 12. Source index

| # | Title | Type | Credibility and bias | Contributed most |
|---|---|---|---|---|
| S01 | Google Analytics 4 tutorial for beginners (2026), Julius, Analytics Mania | YouTube tutorial transcript, 11,516 words, 37 cards | Sells GA4 and GTM courses; live demos on an empty property and Google's demo ecommerce account; no client results. Several settings are stated preferences (GTM, long session timeout, 30-second engaged timer, older layout, total users, forms off). Generic GA4 tutorial: ecommerce events explicitly out of scope. Medium credibility on UI and mechanics, low on strategy. | Account and property structure, install and testing workflow, 5 day-1 settings, explorations (free form, funnel, path), landing page vs pages and screens, Analytics Advisor caution, session timeout trade-off |
| S02 | eCommerce Marketing Data 101, Derric Haynie (eCommerceTech.io) | Podcast interview transcript, 11,257 words, 23 cards | Runs a tool directory (revenue model unstated); 1 personal test story with self-contradiction, 1 second-hand anecdote, 1 second-hand heuristic; admits he decides "based on feel". No formulas, no attribution method. Incrementality and consent appear only in cards. Low credibility on numbers, medium on decision framing. AI futurism and career advice [0f952763382f] [ae8e451f0cae] and the tool directory plug [28a475f2a0fd] are context, not rules. | 1 top metric and when to change it, analytics ends in a decision, comparative charts, data tiers, platform vs self-reported attribution as an open conflict, what a winner breaks, log data early |
| S03 | Google Analytics Tutorial For Beginners (2026 Update), Loves Data | YouTube tutorial transcript, 9,036 words, 24 cards | Sells a GA course, plugs it about 8 times; demos on Google Merchandise Store and a test property; no client data. Generic GA4 tutorial: stops at the Google tag, no ecommerce events. Recommendations (GTM, Other Business Objectives, 14 months) are opinion. Medium credibility on click paths and definitions. | Thank-you page key event method (leads), campaign regex, checkout funnel exploration options, Advertising section (Last Click vs Data Driven, Conversion management), Total vs Purchase Revenue, "(not set)" = unknown, time zone and currency rules, admin settings map |
| S04 | Install Facebook (Meta Ads) Conversion API with server-side tagging, Leon | YouTube tutorial transcript, 5,023 words, 7 cards | Promotes a Stape affiliate link and uses Stape's template; live demo on his own site with PageView and a contact form only; no Purchase, no value, no EMQ, no results. "Meta recommends" stated without citation. High credibility on the GTM mechanics shown, none on outcomes. | Redundant pixel plus CAPI build, consent gating on both sides, cookie consent update trigger, constant variables per container, Debug Mode test code lookup table, event ID dedup wiring and the search-the-ID proof, server delay |
| S05 | Google Analytics 4 For eCommerce 2025 (Perfect for beginners), unnamed Shopify store owner | YouTube transcript, 3,430 words, 9 cards | 1 store's GA4 screens read aloud; plugs own channel; no benchmarks; a probable transcription error (99.2%). Several caveats exist only in cards. Low credibility on numbers, useful on the purchase-filter rule and the Shopify vs GA4 split. | Filter every key event rate to purchase, channel then medium, customise and save tables, landing page conversion by product page with 3 causes, Purchase journey reading, GA4 for what Shopify lacks |
| S06 | What Metrics Matter In The Shopify Analytics Dashboard, unnamed agency presenter (likely Australian) | YouTube walkthrough transcript, 3,429 words, 12 cards | Agency with clients; 1 blurred client dashboard; plugs 4 own videos; metric definitions are his reading of the UI; arithmetic error in the 10% example; strong opinions ("attribution is futile"). Medium credibility on the revenue identity and return timing, low on benchmarks and definitions. | Net sales + shipping, tax out; returns land on refund date; sessions x conversion rate x AOV triage; 4:2:1 and 2:1:1; bots in Shopify sessions and the 1-city check; ignore Shopify attribution cards; Online Store channel filter; returning customer rate warning; AOV limits |
| S07 | Facebook Conversions API gateway tutorial, Julius, Analytics Mania | YouTube tutorial transcript, 2,415 words, 5 cards | Same presenter as S01; sells a GTM course with server-side content (the alternative he recommends); links to Stape; 1 demo with PageView only; blocker test with Ghostery; Meta's numbers quoted, his 1 to 2% unmeasured. Cards go further than the transcript ("stopgap"). High credibility on the gateway mechanics, low on lift numbers. | What the gateway is and cannot do, blocker test, automatic dedup with the gateway, Stape setup and DNS steps, the 2 lift claims, server-side extras (custom loader, cookie extension) |

**Independent voices.** 6, not 7: S01 and S07 share a presenter. S04 and S07 both have Stape ties. S01, S03 and S05 all read Google's UI, so their agreement on GA4 mechanics is agreement about 1 product, not 3 independent tests.

**Neighbour folders.**
- 24-DEP-ad-deployment: Meta account structure, attribution window for buying (7-day click), campaign reads, existing-customer exclusions, incrementality proposals.
- 12-GAD-google-ads: Google Ads conversion actions, Shopping, the Ads side of Conversion management.
- 09-CRO-testing: funnel leak reads turned into hypotheses, research methods (recordings, surveys), sample size and significance for any "is the gap real" question.
- 07-LPG-landing-pages: page fixes after a landing page or funnel read.
- 14-EML-email-lifecycle: email metrics, per-send revenue, the medium rows that name an email sender.
- 20-FIN-finance-and-accounting: profit, contribution, COGS, cash vs sales, cohort and LTV reading, sell-through, cash conversion cycle.
- 17-CXP-post-purchase: post-purchase survey placement and returns handling.
- 05-SET (not in v2 yet): store setup, theme code, Shopify app installs. S01, S03 and S05 defer setup there.
