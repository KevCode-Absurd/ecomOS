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

**Does not cover.** Meta account structure, attribution window choice for buying, and campaign reads: 24-DEP. Google Ads conversion actions and Shopping: 12-GAD. Test design, sample size and significance: 09-CRO. Checkout and page fixes once a funnel leak is found: 07-LPG and 09-CRO. Cohort reading, LTV, CAC, contribution margin, COGS, cash conversion cycle and sell-through: 20-FIN (S06 raises them; the formulas are not here). Email deliverability and per-send metrics: 14-EML. Store setup and theme code: a 05-SET folder that does not yet exist in v2; S01, S03 and S05 point there.

**Business measures it moves.** Fewer wrong budget decisions made on double-counted, bot-inflated or return-timed numbers (S06 return dip example; S04 double count before dedup). Faster decisions because 1 top metric and 1 source of truth per question are agreed (S02, S05). Higher share of Meta events matched and deduplicated (S04, S07; no source measures the lift). Less analyst time lost to numbers that later turn out wrong (S02: analytics must end in a decision).

## 2. Inputs the agent needs

| Input | From where | Required or optional | Why |
|---|---|---|---|
| Store platform, theme, checkout domain, whether checkout is hosted | Brand record | Required | Decides GTM vs native pixels (group J), cross-domain settings (R14) |
| Every domain a shopper touches from landing to thank-you page | Brand record, user | Required | 1 property per journey; Configure your domains (R8, R14) [60bd489184a8] |
| Business time zone and store currency | Brand record | Required | Property settings; changing time zone later breaks data (R6, R7) [5c923d97e1f7] |
| Selling countries and the consent rules that apply | Brand record, `[web check]` | Required | Consent gating of pixel and CAPI, Google Signals decision (R41, R21) |
| What installed GA4 and the Meta pixel (app, theme code, GTM, developer), and which Meta integrations are live | Brand record, user, live site inspection | Required | Avoid double CAPI streams; decide if the gateway use case applies (R47, R55) |
| Current GA4 admin settings: retention, domains, internal traffic filter state, session timeout, Signals, key events list, custom definitions | Data layer (GA4 admin, `[verify UI]`) | Required | Settings audit (checklist 5.8) |
| GA4 ecommerce event list and parameters as they actually arrive (DebugView sample) | Data layer | Required | Event coverage check (checklist 5.2) [d6b4bece9591] |
| Meta Events Manager: events, browser vs server counts, dedup status, test events, dataset quality | Data layer (Meta MCP read tools) | Required | Dedup check (checklist 5.3) [8d023b8f223e] |
| Store orders for the same dates: count, net sales, shipping charges, tax, refunds by refund date and by order date, sales channel | Data layer (store admin export, Metabase, or platform API) | Required | Reconciliation (P21), revenue definition (R66), return timing (R67) [a3ae4e9e2a00] |
| GA4 purchase count and purchase revenue, transaction ID report | Data layer | Required | Reconciliation [2fa8beb663c8] |
| Shopify Analytics: sessions, conversion rate, AOV, funnel counts, sessions by location | Data layer | Required for Shopify stores | Triage and bot check (P19, P20) [9e9d4013f967] |
| GA4 sessions for the same dates | Data layer | Required | Bot check denominator (R74) [084db9abd48b] |
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

**R41. Treat AI answers (Analytics Advisor, Insights) as leads to check in a report, never as findings.** Condition: any AI chat over GA4 data. S01's demo: 1 correct number (125 organic purchases), then a wrong date range and a repeated myth ("a custom event before page_view causes (not set) landing pages"; the presenter's own experiments say it does not). S05's creator uses Insights for a "very quick answer" only. Supports: S01 [bb64df0f76c5] [1ed5edfed51c], S03 [a338f3ce307d] [57ce958e9267], S05 [7cef7f4d4e54].

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

**R62. Ignore every Shopify attribution and referral card for decisions. Read them as 1 signal among several at most.** Condition: total sales by social referral, sessions by social referral, top referrals by session, sales attributed to marketing, sessions by referrer, total sales by referrer. S06's presenter: "not accurate", "attribution is a futile effort". Card 561513b3e85e softens to "triangulate" with GA4, UTMs, attribution windows, consent coverage and incrementality tests. Conflict C10. Source S06 [561513b3e85e].

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
