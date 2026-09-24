# Google Analytics Tutorial For Beginners (2026 Update)

source_id: 1_b-LSsXC5eZ2Ul0IHuNkGn0mF7GrFwl0  |  folder: /06-MEA-measurement  |  cards: 24  |  words: 9,036  |  type: transcript (single YouTube tutorial, spoken walkthrough)

credibility: Presenter runs the "Loves Data" channel and blog (he names his test account "Loves Data" and his test site "loves-data-test.com"). He is based in Sydney. He sells a Google Analytics course, dedicated tutorials and a free "Google Analytics Glossary", and plugs them about 8 times. Evidence is live screen demos in Google's public demo property (Google Merchandise Store) and his own demo property. No brand results, no tests, no client data. The content is a UI walkthrough, so its value is accuracy of click paths and definitions, not strategy. Where he recommends something (GTM over the Google tag, "Other Business Objectives", 14-month retention), it is his opinion.
date signals: Title says "2026 Update". Uses current GA4 terms: "Key events" (not "conversions") inside GA4, "Data Display" and "Data Collection and Modification" admin groups, "Google Tag" as the GTM tag type, "Analytics Advisor" AI chat (Gemini powered per the filing header), Budgeting with "Projection" and "Scenario Planner" under Advertising, and a "Conversion Management" view that spans GA4 and Google Ads. Only 2 attribution models are compared (Last Click and Data Driven). File modified 19 Sep 2026. All UI paths are 2026 but can move at any time. `[web check: current GA4 admin menu names and report locations before following any step]`
header warning: The document starts with a 06-MEA folder note and a "Look for / Skip / Scope mix / Volume" block. That is filing metadata, not source content. The header says "GA4 Configuration tag"; the transcript itself uses the tag type "Google Tag". The header says internal traffic is filtered "via IP address"; the transcript never mentions IP. Follow the transcript.

## 1. What this source is for

A click-by-click beginner guide to Google Analytics 4 for a website. It covers creating the account, property and web data stream, reading every standard report family (Home, Realtime, Acquisition, Engagement, Monetization, User Attributes, Tech, Advertising), building 2 Explore reports (a campaign-only table and a checkout funnel), making a thank-you-page key event, building an exclusion audience, the key admin settings, and installing GA4 through Google Tag Manager with a test in Preview and DebugView. Use it to set up or audit a basic GA4 property, to find where a number lives, and to know what a GA4 term means before trusting it. It does not cover implementing ecommerce events on a store, Shopify specifics, or reconciling GA4 with the store's own order data.

## 2. Principles

1. **Account organizes, property holds the data, data stream feeds it.** One account per business. Usually 1 property per business, which can collect from 1 site or from several sites and apps. Each site or app is a data stream: 1 website = 1 stream, website plus app = 2 streams. If you set up GA4 for another business, create another account. [5c923d97e1f7]
2. **Pick the reporting time zone with care.** Changing it later causes a gap or overlap in data. Condition: applies at creation; the setting can be changed later in Property Details, but with that data break. [5c923d97e1f7] `[needs brand data: store's reporting time zone, ideally matching the store platform and finance reports]`
3. **Set currency to the primary currency the business uses.** GA4 converts values sent in other currencies into the property currency automatically (example: AUD values sent to a USD property show as USD). [5c923d97e1f7] `[needs brand data: store currency]`
4. **Enhanced measurement is a starting point, not a finished setup.** It tracks page views, scrolls, outbound clicks, site search, form interactions, embedded YouTube views and file downloads with no code. It is on by default. Review each event against what you want to measure and switch off the ones you do not want (source example: forms). [d5ffafc2403f]
5. **Prefer Google Tag Manager over the plain Google tag.** Source says GTM "provides added flexibility": it manages many tags, not just GA4, and can track many other actions and elements. This is the presenter's recommendation "in most cases", not a GA4 requirement. [9f5dc9b5cd04] `[web check: on Shopify, GTM cannot run inside checkout; current Shopify guidance is the Google and YouTube app or customer events pixels]`
6. **Reports monitor; Explore answers a specific question.** Reports are pre-configured and best for watching what is happening. Explore is for custom tables, funnels and paths when you have 1 question. The goal is not to learn every report, only the ones that explain your site. This is a mental model, not a product limit. [cadc7c256522]
7. **Events are any tracked action; key events are the ones that matter to the business.** Key events are GA4's name for conversions. Marking an event as key counts a key event every time that event is collected. [e2bcc61df786] [a8f35cf35c8e]
8. **Do not mark page_view as a key event to track 1 page.** That would count a conversion on every page view. To track a thank-you page, first make it a unique event, then mark that event as key. [e2bcc61df786]
9. **Key events (GA4) and Conversions (Google Ads) are different counts.** Google Ads conversions include GA4 key events imported into Ads plus any conversion actions made inside Ads. The Advertising reports in GA4 show both. A mismatch is expected, not an error. [a8f35cf35c8e]
10. **User Acquisition = first source ever; Traffic Acquisition = source of each session.** User Acquisition shows how users first found the site. Traffic Acquisition shows how they found it to start each session, with session-based metrics. Choose the report that fits the question. The card adds "first touch for brand and LTV talk, session for campaign and budget talk"; that split is the card's inference, not the presenter's. [0d831192ef28]
11. **"(not set)" means unknown.** GA4 collected the user but cannot give the value you asked for. Treat it as unknown, not as an error. [d54ee95e619b] This matches the ecomOS house rule: missing values show as unavailable, not zero.
12. **Total Revenue and Purchase Revenue differ only if non-purchase events carry value.** Total Revenue sums value from all events. Purchase Revenue is ecommerce transactions only. [2fa8beb663c8]
13. **Attribution models describe; they do not settle credit.** The Key Event Attribution Models report shows Last Click and Data Driven side by side with the % difference. The presenter frames it as seeing "how credit is given" under 2 models, not which is right. The card adds that model gaps are not incrementality; that is the card's caveat. [675a952696ec]
14. **Audiences are for reporting as well as ads.** You can build them only to study a group, even without Google Ads. [7425cd2ae91c]
15. **Automated insights and Analytics Advisor are starting points.** Insights flag unusual changes and differ per property. Analytics Advisor answers plain questions from the property's data. Treat both as leads for deeper work in Reports or Explore. [a338f3ce307d] [57ce958e9267]
16. **Realtime is for checking arrival, not for analysis.** Data shows within seconds. Standard reports can take 12 to 24 hours. [30843583e84d] [fbe6ee425691]
17. **Link Google Ads and Search Console.** Source recommends linking both under Product Links for extra reports and insights. Advertising reports look limited without the Ads link and key events. [c01dc627e7b1] [675a952696ec]
18. **Keep retention at 14 months.** Card and filing header say the default is 2 months; the transcript says the choices are 2 or 14. Presenter recommends 14 "so you have more historical data available in your reports". The card narrows this to Explore reports. [c01dc627e7b1] `[web check: whether retention affects standard reports or only explorations]`

## 3. Procedures

Every menu path and button name below is from the 2026 recording. `[verify UI]` applies to each step.

### 3.1 Create account, property and web data stream [5c923d97e1f7] [d5ffafc2403f]

1. Go to marketingplatform.google.com. Click "Sign In To Analytics" if you have an account, or "Get Started Today" if not. Log in with the Google account (Gmail or Workspace) that should own analytics. `[verify UI]`
2. If you already have GA4: Admin > Create > Account. A first-time user lands on this screen directly. `[verify UI]`
3. Name the account after the business. Review the data sharing options (presenter keeps defaults). Click Next. `[verify UI]`
4. Name the property after what it measures (site, app, or the set). Presenter reuses the account name. Name can be changed later. `[verify UI]`
5. Set the reporting time zone (country, then city). Take care: a later change makes a gap or overlap. `[verify UI]` `[needs brand data: time zone]`
6. Set currency to the business's primary currency. Values sent in other currencies convert to this. Click Next. `[verify UI]` `[needs brand data: currency]`
7. Choose industry category and business size. Click Next. `[verify UI]`
8. Choose business objectives. These control which pre-configured reports are added. Presenter picks "Other Business Objectives" because it gives "a full set of reports" and "basically includes everything" in the other 4 options. Click Create. `[verify UI]`
9. Pick the country for the terms of service and accept. `[verify UI]`
10. Choose platform "Web" to create a web data stream. Enter the site URL and a stream name. `[verify UI]`
11. Before creating, click the enhanced measurement configuration icon. Switch off any action you do not want tracked (page views, scrolls, outbound clicks, site search, forms, video engagement, file downloads). Save. `[verify UI]`
12. Click to create the stream. Wait for installation instructions. GA4 tries to detect the site platform; "view additional options" lets you pick a CMS for guided steps. `[verify UI]`
13. Copy the Measurement ID from the top right of the stream details. `[verify UI]`

### 3.2 Install GA4 through Google Tag Manager and test it [9f5dc9b5cd04] [9bedc2d9534e]

1. In GA4: Admin > Data Collection and Modification > Data Streams > select the stream > copy the Measurement ID (top right). `[verify UI]`
2. In GTM: create a new tag. Name it "Google Tag, GA4, Page View". `[verify UI]`
3. Tag Configuration > tag type "Google Tag". `[verify UI]`
4. Click the variable icon under "Tag ID" > plus sign (top right) > name "GA4 Measurement ID" > Variable Configuration > "Constant" > paste the Measurement ID as Value > Save. The constant lets you reuse the ID across tags. `[verify UI]`
5. Triggering: set "Initialization - All Pages". This loads the tag on every page and fires it before other tags. Save the tag. `[verify UI]`
6. Click Preview, enter the site URL, click Connect. Tag Assistant opens. `[verify UI]`
7. Browse the site and do the actions you track. In the Tag Assistant tab confirm the tag fired. `[verify UI]`
8. In GA4 open DebugView and confirm events from the test session arrive. `[verify UI]`
9. Back in GTM: Submit > name the version > Publish. Live traffic now flows to GA4. `[verify UI]`

The source stops here. It does not show how to send add_to_cart, begin_checkout, add_payment_info or purchase with value, currency, items or transaction id. The card notes DebugView proves arrival, not parameter correctness; that note is the card's, not the presenter's. [9bedc2d9534e]

### 3.3 Make a thank-you page a key event without code [e2bcc61df786]

Needs marketer, editor or administrator access. Demo property does not allow it.

1. Admin > Events (also Admin > Data Display > Events). Tabs: "Key Events" (default) and "Recent Events". `[verify UI]`
2. Click "Create Event". `[verify UI]`
3. Name the event. Source uses `generate_lead` for a lead form thank-you page. `[verify UI]`
4. Switch on "Mark as key event". `[verify UI]`
5. Optional: enter a default value for what the key event is worth. `[verify UI]` `[needs brand data: value per lead or action]`
6. Counting: leave the default "Once per event". `[verify UI]` `[web check: current count options and Google's guidance per event type]`
7. Keep "Create without code". Keep event name condition `page_view`. `[verify UI]`
8. Add a URL condition: contains `thank-you`. Any page view with a URL containing "thank-you" fires the new event. `[verify UI]` `[needs brand data: exact confirmation page URL pattern]`
9. Click Create. `[verify UI]`
10. Check Realtime right after a test visit. Check the standard Events report the next day (12 to 24 hour lag).

Alternative the source names but does not show: fire the event from a GTM tag when the thank-you page loads (for example `generate_lead` after a form). Other options in the same area: "Custom Configurations" > "Modifications" to change parameter values or rename an event; the star icon left of an event marks an existing event as key. `[verify UI]`

### 3.4 Build an audience of people who have not converted [7425cd2ae91c]

1. Admin > Data Display > Audiences. Existing audiences show. New properties have 2 predefined: "All Users" and "Purchases". "Purchases" stays empty if no purchase event is sent. `[verify UI]`
2. Click "New Audience". Suggested templates sit at the bottom; choose "Create a Custom Audience" at the top. `[verify UI]`
3. Name it (source: "Haven't Generated Lead"). `[verify UI]`
4. Click the trash can icon right of "Include Users When" to remove the include group. `[verify UI]`
5. Click "Add Group to Exclude". `[verify UI]`
6. Type the exact event name (`generate_lead`). A new event is not listed yet, so choose "Create Event" to add it as a condition. Events already collected appear in the list and can be picked. `[verify UI]`
7. Keep other defaults. Save. `[verify UI]`
8. Use it in reports, and for remarketing in a linked Google Ads account.

Note: card 7425cd2ae91c says to keep the default include condition and then add the exclude group. The transcript removes the include group first. Follow the transcript. `[verify UI]`

### 3.5 Explore report: campaigns only [8db1bf5fadc7]

1. Explore > blank exploration. Name it "Campaigns" (top left). `[verify UI]`
2. Plus sign next to Dimensions > search "Campaign" > tick "Session Campaign" > Confirm. `[verify UI]`
3. Plus sign next to Metrics > tick "Sessions", "Active Users", "Key Events" > Confirm. `[verify UI]`
4. Double click (or drag) Session Campaign into Rows. Double click the 3 metrics into Values. `[verify UI]`
5. The first rows are "(organic)", "(direct)", "(not set)". Scroll to Filters at the bottom of the second column > choose Session Campaign > "Does Not Match Regex" > enter `^\(.*\)$` > Apply. `[verify UI]`
6. Result: only named campaigns remain. The regex drops any value that starts and ends with a parenthesis.

`[needs brand data: UTM campaign naming, so real campaigns never start with "(" and end with ")"]`

### 3.6 Explore report: checkout funnel [ac9071a3bbdd]

1. Explore > blank exploration. Name it "Conversion Funnel". `[verify UI]`
2. At the top of the second column change "Free Form" to "Funnel Exploration". `[verify UI]`
3. Find "Steps" > pencil icon. `[verify UI]`
4. Step 1 name "Begin Checkout", condition event `begin_checkout`. `[verify UI]`
5. Add Step. Step 2 shows "is indirectly followed by" (default: users may view other pages or do other actions between steps). "is directly followed by" drops anyone who views another page in between. Presenter keeps indirect. `[verify UI]`
6. Optional per-step time limit (step must happen within a set time). Presenter leaves it off. `[verify UI]`
7. Step 2 name "Add Payment Info", condition `add_payment_info`. Step 3 name "Purchase", condition `purchase`. Apply (top right). `[verify UI]`
8. Read: bars show users reaching each step; drop-off per step sits below; a table breaks down metrics. `[verify UI]`
9. Options: "Make Open Funnel" lets users enter at any step. "Trended Funnel" shows each step over the date range. `[verify UI]`

Any collected event works as a step, including page views for a page-path funnel. The funnel depends on these ecommerce events being implemented on the site. `[needs brand data: which ecommerce events the store actually sends]`

### 3.7 Read the standard reports (tour order) [cadc7c256522] [30843583e84d] [0d831192ef28] [90bd1b325921] [2fa8beb663c8] [d54ee95e619b] [f2f53af85949]

1. **Home.** AI insights on top. Cards: active users, key events, sessions, purchases (source says totals are for the last 14 days; change via the date selector). Trend line with a dotted previous-period line of the same length. Active users in last 30 minutes. Recently viewed. Insights and recommendations, including custom insights you configure. `[verify UI]`
2. **Reports snapshot.** Active users, new users, average engagement time, event count. Top pages with Views, Active Users, event count, bounce rate. Cards for new-user sources, session sources, new vs returning. `[verify UI]`
3. **Realtime overview.** Users in last 30 and last 5 minutes. Bar charts read right to left: rightmost bar = current minute, each bar left = 1 minute earlier, 30 in total. Map, sources, audiences matched, pages, events, key events, user properties. **Realtime pages** lists pages being viewed now with users and views, with search and paging. `[verify UI]`
4. **Acquisition overview.** New users by "First user primary channel group". Switch a card's dimension (example: First User Medium: cpc = paid ads, organic = free search results, referral = other sites). Cards for sessions by primary channel group, Google Ads campaign sessions, average lifetime value. Links at the bottom open full reports. Date range: presets or custom; "Compare" shows increase or decrease vs a second range. `[verify UI]`
5. **User acquisition.** First way users found the site. Change the dimension from the dropdown; add a second dimension with the plus sign (example: Landing Page). `[verify UI]`
6. **Traffic acquisition.** Source at the start of each session, session metrics. `[verify UI]`
7. **Engagement > Events.** All collected events: page_view, enhanced measurement events, recommended and custom events. AI insights on top. `[verify UI]`
8. **Engagement > Pages and screens.** Rows by Page Path, sorted by Views. `[verify UI]`
9. **Engagement > Landing page.** First page of each session; key events after landing. Use for top entry points and cross-promotion. `[verify UI]`
10. **Monetization > Overview.** Total Revenue, Purchase Revenue, total purchasers and first-time purchasers (user-based), average purchase revenue per active user, top items, items by item list name, items by promotion, revenue by coupon code. `[verify UI]`
11. **Monetization > Ecommerce purchases.** Item-level metrics by item name; change the dimension. Also "Purchase journey", "Checkout journey", promotion (coupon) reports, and a transaction ID report. `[verify UI]`
12. **User attributes > Overview.** Country, city, gender, interests, age, language (from device settings). Missing gender, interests and age = Google Signals is off. **Demographic details**: switch Country to City and so on. `[verify UI]`
13. **Tech > Overview.** OS, device type, browser, device category (desktop, tablet, mobile), screen size. App-only cards are blank on a web-only property. "Platform" = data stream type (Web or App). **Tech details** defaults to browser; switch to Device Category. `[verify UI]`
14. **Library** (bottom of the reports menu) appears only for editor or admin users and customizes the menu. This is why menus differ between properties. `[verify UI]`

### 3.8 Advertising section [675a952696ec] [a8f35cf35c8e] [510ee3226e4d]

Useful once Google Ads is linked and key events exist.

1. **Advertising snapshot.** Conversions trend, conversions by default channel group, key events by default channel group, insights, top paths to key events. `[verify UI]`
2. **Key event performance.** Key events per channel. Top dropdown filters to a Google product (for example Google Ads). "Key Events" dropdown picks which key events count. Dimension switch above the table. `[verify UI]`
3. **Key event attribution paths.** Touchpoint sequences before a key event (example: several organic search visits, or multi-channel paths). Change the path dimension, the attribution model and the key events. `[verify UI]`
4. **Key event attribution models.** Channels on the left; key events and revenue under Last Click, then under Data Driven; far right shows % increase or decrease between them. `[verify UI]`
5. **Conversion reports.** After the Ads link: GA4 key events plus Google Ads conversions. `[verify UI]`
6. **Budgeting > Overview, Projection, Scenario Planner.** Forecasts for paid ads and how budget changes affect conversions and spend. `[verify UI]`
7. **Conversion management.** All conversions set in GA4 and linked Ads accounts; compare settings across platforms. `[verify UI]`
8. **Advertising segments.** Users available for targeting in Google Ads; check lists meet minimum remarketing sizes. `[verify UI]` `[web check: current Google Ads minimum list sizes]`

### 3.9 Property settings to set once [c01dc627e7b1] [d93703003497] [5e2819e7dfec]

1. Admin > Data Display > Comparisons: segments you can apply to standard reports; pre-configured or custom. Source gives no steps. `[verify UI]`
2. Admin > Data Display > Custom Definitions: register event parameters as custom dimensions or custom metrics. Source gives no steps. `[verify UI]`
3. Admin > Data Display > Channel Groups: control how traffic is classed. Default puts Facebook, LinkedIn and Instagram in "Organic Social". Create your own groups. `[verify UI]`
4. Admin > Data Display > DebugView: live view of events while you test. `[verify UI]`
5. Admin > Property > Property Details: rename property, check time zone and currency, move property to another account. `[verify UI]`
6. Admin > Property Access Management: control who has access. `[verify UI]`
7. Admin > Data Collection and Modification > Data Streams: Measurement ID and tracking code. `[verify UI]`
8. Admin > Data Collection and Modification > Data Collection: enable Google Signals (needed for age, gender, interests and for using audiences in linked Google Ads). `[verify UI]` `[web check: consent and privacy duties before enabling; current effect of Signals on reporting thresholds]`
9. Admin > Data Collection and Modification > Data Retention: set 14 months. `[verify UI]`
10. Admin > Data Collection and Modification > Data Filters: filter to exclude internal traffic. Source gives no steps (no IP rule, no activation step). `[verify UI]` `[web check: how to define internal traffic and activate the filter]`
11. Admin > Data Collection and Modification > Consent Settings: shows whether consent mode is set up. Needed to use EU users' data for Google Ads targeting. Source gives no setup steps. `[verify UI]` `[web check: consent mode v2 setup for the store's platform and markets]`
12. Admin > Product Links: link Google Ads and Google Search Console. `[verify UI]`

Note on paths 1 to 4: the presenter reaches Events and Audiences under "Data Display" and then lists Comparisons, Custom Definitions, Channel Groups and DebugView in the same run; he does not say the group name for each. `[verify UI]`

### 3.10 Ask Analytics Advisor [a338f3ce307d] [57ce958e9267]

1. Click the Analytics Advisor icon, top right. `[verify UI]`
2. Ask a plain question (source: "How is the website performing year on year?"). Wait a few moments.
3. Read the summary of year-on-year changes. Check it in Reports or Explore before acting.

The filing header says to skip this demo as a generic query tool. Card 57ce958e9267 is titled "Forecast"; the source only shows a year-on-year summary, not a forecast.

## 4. Rules, thresholds and numbers

| rule | number or threshold | condition | source's basis | card id |
|---|---|---|---|---|
| Accounts per business | 1 | each business gets its own account | presenter's structure advice | 5c923d97e1f7 |
| Properties per business | usually 1 | may hold several sites and apps | presenter | 5c923d97e1f7 |
| Data streams | 1 per site or app | web + app = 2 streams | presenter | 5c923d97e1f7, f2f53af85949 |
| Business objective pick | "Other Business Objectives" | at property creation | presenter: gives full report set | 5c923d97e1f7 |
| Enhanced measurement events | 7 types | on by default; review each | GA4 feature description | d5ffafc2403f |
| Scroll event trigger | 90% of a page | enhanced measurement on | presenter | (text only) |
| Home card default range | last 14 days | as shown in the demo | presenter's demo | (text only) |
| Realtime window | last 30 min and last 5 min | Realtime overview | UI | 30843583e84d |
| Realtime latency | a few seconds | Realtime reports only | presenter | 30843583e84d, fbe6ee425691 |
| Standard report latency | 12 to 24 hours | new events, standard reports | presenter; card says it may vary | fbe6ee425691, e2bcc61df786 |
| Data retention choices | 2 or 14 months | Admin > Data Retention | UI | c01dc627e7b1 |
| Retention setting to use | 14 months | presenter recommends | opinion | c01dc627e7b1 |
| Key event count method | "Once per event" (default kept) | thank-you page `generate_lead` | presenter's demo | e2bcc61df786 |
| Thank-you URL match | URL contains `thank-you` | page_view based created event | demo | e2bcc61df786 |
| Campaign-only regex | `^\(.*\)$` with "Does Not Match Regex" | Session Campaign filter in Free Form | demo | 8db1bf5fadc7 |
| Checkout funnel steps | 3: begin_checkout, add_payment_info, purchase | events implemented | demo; card: an example, not a benchmark | ac9071a3bbdd |
| Funnel step link | "indirectly followed by" (default) | other pages allowed between steps | presenter's pick | ac9071a3bbdd |
| Attribution models compared | 2: Last Click, Data Driven | Key Event Attribution Models report | UI | 675a952696ec |
| Access to create events, mark key events, modify | marketer, editor or admin | own property | UI | e2bcc61df786 |
| Access to Library | editor or admin | own property | UI | cadc7c256522 |
| Predefined audiences | 2: All Users, Purchases | new property | UI | 7425cd2ae91c |
| Total vs Purchase Revenue | equal | only if no non-purchase event carries value | definition | 2fa8beb663c8 |

## 5. Diagnostics and checks

| check | how | good | bad | next |
|---|---|---|---|---|
| Tag installed and firing | GTM Preview > Tag Assistant; GA4 DebugView [9f5dc9b5cd04] [9bedc2d9534e] | Google Tag fires on Initialization; events show in DebugView | tag missing or no events | fix tag or trigger before Publish |
| New event recorded | Realtime right away; standard Events report next day [fbe6ee425691] | event in Realtime now, in reports after 12 to 24 h | missing from Realtime | recheck event conditions (name, URL match) |
| Campaign traffic landing after a send | Realtime overview and Realtime pages after an email or ad goes out [30843583e84d] | expected landing pages and sources show | wrong pages or no users | check links and UTMs `[needs brand data: campaign send time and links]` |
| Demographics missing | User attributes shows no age, gender, interests [d54ee95e619b] | fields filled | fields empty | enable Google Signals (after consent review) |
| "(not set)" rows | any report [d54ee95e619b] | small share, read as unknown | large share | investigate collection; source gives no threshold |
| Revenue sanity | Monetization overview: Total Revenue vs Purchase Revenue [2fa8beb663c8] | equal, or gap explained by valued non-purchase events | unexplained gap | list events with value; `[needs brand data: store order revenue for same dates]` |
| Coupon, promotion, list cards empty | Monetization overview [2fa8beb663c8] | populated | empty | the parameters are not sent; source gives no fix |
| Purchases audience empty | Admin > Audiences [7425cd2ae91c] | has users | empty | purchase event not sent |
| Web vs app mixed | Tech overview "Platform" [f2f53af85949] | 100% Web on a web-only property | App share where none expected | check data streams |
| Checkout drop-off | Funnel exploration (3.6) [ac9071a3bbdd] | not given by source | not given by source | source gives no benchmark `[needs brand data: prior funnel rates]` |
| Entry page quality | Landing page report: entrances vs key events [90bd1b325921] | pages with traffic also get key events | high entrances, low key events (card's reading) | card suggests merchandising or content change |
| Model disagreement | Key event attribution models, % difference column [675a952696ec] | small gap | large gap (card: channel under or over valued by last click) | card: treat as a signal, test incrementality where feasible |
| GA4 vs Google Ads counts differ | Conversion management [a8f35cf35c8e] | difference explained by Ads-only conversion actions | unexplained | list conversion actions in both |
| Remarketing list size | Advertising segments [510ee3226e4d] | meets minimum | below minimum | do not plan a campaign on it yet `[web check: minimum sizes]` |
| Channel classification | Admin > Channel Groups [0d831192ef28] | groups match how you judge channels | social traffic lands in Organic Social by default | create a custom channel group |

## 6. Tools, settings and named features

- **Google Marketing Platform site** (marketingplatform.google.com): sign in or start GA4. `[verify UI]`
- **Google demo account / Google Merchandise Store property**: real data to practise on; no admin rights, no User Exploration, no Library. `[verify UI]`
- **Property switcher** (top dropdown): switch accounts and properties. `[verify UI]`
- **Enhanced measurement**: automatic page_view, scroll, outbound click, site search, form, YouTube video, file download events. `[verify UI]`
- **Automated insights / custom insights**: AI-flagged changes on Home and some reports; custom insights on chosen metrics and conditions. `[verify UI]`
- **Analytics Advisor**: AI chat on the property's data, icon top right. `[verify UI]`
- **Comparisons (date)**: Compare toggle in the date picker. `[verify UI]`
- **Explore techniques**: Free Form, Funnel Exploration, Path Exploration, Segment Overlap, Cohort Exploration, User Lifetime, User Exploration (own property only). Each opens a template. Saved explorations list below. `[verify UI]`
- **Funnel options**: indirectly vs directly followed by, step time limit, Make Open Funnel, Trended Funnel. `[verify UI]`
- **Explore filter "Does Not Match Regex"**. `[verify UI]`
- **Create Event, Modifications, star to mark key event**. `[verify UI]`
- **Audiences** with suggested templates, include and exclude groups. `[verify UI]`
- **Comparisons (segments)**, **Custom Definitions**, **Channel Groups**, **DebugView**. `[verify UI]`
- **Google Signals**, **Data Retention**, **Data Filters**, **Consent Settings**, **Product Links**, **Property Access Management**, **Property Details**. `[verify UI]`
- **Advertising**: Snapshot, Key Event Performance, Key Event Attribution Paths, Key Event Attribution Models, Conversion reports, Budgeting (Overview, Projection, Scenario Planner), Conversion Management, Advertising Segments. `[verify UI]`
- **Google Tag Manager**: tag type Google Tag, Constant variable, Initialization - All Pages trigger, Preview, Tag Assistant, Submit, Publish. `[verify UI]`
- **Library**: customize the report menu (editor or admin). `[verify UI]`

## 7. Examples and case results

No business results. Demo examples only:
- Account "Loves Data", property "Loves Data", time zone Australia/Sydney, currency USD, stream "Loves Data Website" at loves-data-test.com. Example only. [5c923d97e1f7]
- Currency example: AUD values sent to a USD property are shown converted to USD. [5c923d97e1f7]
- Demo property is Google Merchandise Store (Google-branded t-shirts, hats, accessories): 100% "Web" under Platform. [f2f53af85949]
- Attribution paths example: some users used organic search several times before converting; other paths mix channels. No numbers given. [675a952696ec]
- Analytics Advisor example question: "How is the website performing year on year?" returned a year-on-year summary. No numbers shown in the transcript. [57ce958e9267]
- Audience example: "Haven't Generated Lead", for reporting and Google Ads remarketing to non-leads. [7425cd2ae91c]
- Card 510ee3226e4d and card c01dc627e7b1 give no numbers beyond those in section 4.

## 8. Mistakes the source warns about

1. Changing the reporting time zone after data collection starts: causes a gap or overlap. [5c923d97e1f7]
2. Accepting enhanced measurement without review: may track actions you do not want in reports (example: forms). [d5ffafc2403f]
3. Marking page_view as a key event to track 1 page: every page view becomes a conversion. [e2bcc61df786]
4. Expecting a new event in standard reports the same day: wait 12 to 24 hours; use Realtime to confirm now. [fbe6ee425691]
5. Reading "(not set)" as an error: it means unknown. [d54ee95e619b]
6. Reading missing demographics as no data: Google Signals is off. [d54ee95e619b] [c01dc627e7b1]
7. Expecting GA4 key events to equal Google Ads conversions: Ads adds its own actions. [a8f35cf35c8e]
8. Keeping default 2-month retention: less history for lookbacks. [c01dc627e7b1]
9. Leaving campaign tables full of (organic), (direct), (not set) rows: filter with the regex. [8db1bf5fadc7]
10. Picking "directly followed by" without meaning to: drops anyone who viewed another page between steps and changes the numbers. [ac9071a3bbdd]
11. Expecting the demo property to allow Create Event, key event stars, Library or User Exploration: it does not. [cadc7c256522] [e2bcc61df786]
12. Using EU users' data for Google Ads targeting without consent mode. [c01dc627e7b1]

## 9. Caveats, conflicts and what is missing

**What this source covers that a generic GA4 beginner tutorial may not** (source 01 was not read, so this is a list of the distinct parts, not a verified diff):
- The exact campaign-only regex `^\(.*\)$` with "Does Not Match Regex" on Session Campaign. [8db1bf5fadc7]
- A checkout funnel built on ecommerce events (begin_checkout, add_payment_info, purchase), with indirect vs direct steps, time limit, open funnel and trended funnel. [ac9071a3bbdd]
- The Advertising section in depth: Key events vs Google Ads Conversions, Key Event Attribution Models (Last Click vs Data Driven with % gap), Attribution Paths, Budgeting with Projection and Scenario Planner, Conversion Management, Advertising Segments for list sizes. [675a952696ec] [a8f35cf35c8e] [510ee3226e4d]
- Monetization detail: Total vs Purchase Revenue, item list name, promotion and coupon cards, Purchase and Checkout journey, transaction ID report. [2fa8beb663c8]
- 2026 features: Analytics Advisor, Data Display admin grouping, Google Tag type in GTM with a Constant variable and Initialization trigger. [a338f3ce307d] [9f5dc9b5cd04]
- Small but useful: currency auto-conversion, time zone gap/overlap warning, realtime bar chart read right to left, Platform = stream type, language = device setting, "(not set)" = unknown.

**Conflicts with common ecommerce advice** (flag, do not resolve here):
- Thank-you page as a key event. Source makes a page_view-based event on a URL match. Common ecommerce practice is to count sales from the `purchase` event with value, currency, items and transaction_id, since page reloads and revisits can double count a URL match. Source uses it for leads, not purchases. The card adds "rely on purchase instead"; that is the card's caveat. [e2bcc61df786] `[web check: GA4 purchase deduplication by transaction_id]`
- "Once per event" for a lead key event. Many practitioners count leads once per session. Source keeps the default. `[web check: current GA4 counting options and Google's guidance]`
- GTM for installation. On Shopify, GTM cannot load inside checkout and store apps or customer events pixels are the usual route. Source is platform-neutral. [9f5dc9b5cd04] `[web check: Shopify GA4 install path]`
- Google Signals. Source says to enable it for demographics and Ads audiences. Common advice adds consent checks and notes possible data thresholding. The card adds the privacy caveat. [c01dc627e7b1] `[web check: current Signals behavior on reporting identity and thresholds]`
- Data retention. Source says 14 months gives more history "in your reports". The card says Explore reports. Common understanding is that retention limits explorations, not standard aggregated reports. `[web check]`

**Card vs transcript differences:**
- Card c01dc627e7b1 and the header say filter internal traffic "via IP address". The transcript does not mention IP.
- Card 7425cd2ae91c keeps the include group; the transcript deletes it before adding the exclude group.
- Card 5e2819e7dfec gives steps for using Comparisons inside a report and says they do not persist as saved views. The transcript only says Comparisons are segments for standard reports and defers to another video. Those steps and the persistence claim are the card's.
- Card d93703003497 says the presenter warns against creating custom definitions freely and that text maps to dimension, number to metric. Neither is in the transcript.
- Card 0d831192ef28 adds "first touch for brand and LTV, session for campaign and budget" and a note on attribution windows. Not in the transcript.
- Card 675a952696ec adds "undervalued channel" reading and incrementality testing. Not in the transcript.
- Card 2fa8beb663c8 adds "transaction-ID reports for reconciliation with your platform". Transcript only says the report shows individual transaction IDs.
- Card 57ce958e9267 title says "Forecast"; the transcript shows no forecast.
- Card d5ffafc2403f adds the newsletter field example on form events. Not in the transcript.
- Card 510ee3226e4d adds "may need enough historical conversion data". Not in the transcript.

**What is missing for an ecommerce operator:**
- How to implement ecommerce events (view_item, add_to_cart, begin_checkout, add_payment_info, purchase) and their parameters (value, currency, items, transaction_id, coupon, item_list_name, promotion). Source only says you "can implement" them. `[web check: GA4 recommended ecommerce events]`
- Any Shopify, WooCommerce or other platform install path.
- UTM rules and naming, although the campaign report depends on them. `[needs brand data: UTM convention]`
- Reconciling GA4 revenue with store orders or finance data. `[needs brand data: store order export for same dates and time zone]`
- Attribution settings (lookback windows, reporting model default, channels that can receive credit).
- Internal traffic filter setup, consent mode setup, custom definitions setup, comparisons setup: named, not shown.
- BigQuery export, cross-domain tracking, data thresholds, sampling: not mentioned.
- Any benchmark for funnel drop-off, "(not set)" share or engagement. Source gives none.
- Budgeting projections and Analytics Advisor: shown as features only; source gives no evidence of accuracy.

## 10. Card index

- 5c923d97e1f7  Structure a GA4 account and property for your store
- d5ffafc2403f  Review enhanced measurement instead of accepting defaults
- e2bcc61df786  Create a thank-you-page event as a purchase-adjacent key event
- 9f5dc9b5cd04  Deploy the GA4 tag via Google Tag Manager
- ac9071a3bbdd  Use Explore funnels for checkout drop-off analysis
- 8db1bf5fadc7  Filter campaign rows out of a Free Form Explore report
- 0d831192ef28  Choose User Acquisition vs Traffic Acquisition for the question at hand
- 2fa8beb663c8  Read the Monetization reports for purchase revenue, items, and list/promotion breakdowns
- 90bd1b325921  Analyze landing page performance with the Landing Page report
- 675a952696ec  Compare Last Click and Data Driven attribution for channel decisions
- c01dc627e7b1  Enable Google Signals and extend data retention
- 7425cd2ae91c  Build audiences in GA4 for retention and remarketing segmentation
- 30843583e84d  Use GA4's realtime reports to sanity-check store launches and campaigns
- cadc7c256522  Use Reports for monitoring and Explore for specific store questions
- a8f35cf35c8e  Distinguish Key Events in GA4 from Conversions in Google Ads
- 510ee3226e4d  Check audience size and budget projections in the Advertising reports
- 9bedc2d9534e  Use DebugView to test store event implementation
- d93703003497  Register custom dimensions and metrics for store-specific reporting
- 5e2819e7dfec  Create and use Comparisons as segment overlays on Reports
- a338f3ce307d  Use AI-driven insights and Analytics Advisor as starting points
- fbe6ee425691  Check data freshness expectations before acting on GA4 numbers
- f2f53af85949  Verify the Platform dimension when blending web and app data
- d54ee95e619b  Use User Attributes reports and treat 'not set' as unknown
- 57ce958e9267  Forecast with Analytics Advisor only as a first-pass input
