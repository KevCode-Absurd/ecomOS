# Google Analytics 4 tutorial for beginners (2026)

source_id: 1b4ZdpEvhYQ-L_FcGvMA86kE5bfoC8zQH  |  folder: /06-MEA-measurement  |  cards: 37  |  words: 11,516  |  type: transcript (1 YouTube tutorial, auto-captioned, no timestamps)

credibility: One presenter, Julius, of the "Analytics Mania" channel (full name not given in the text [web check: presenter identity]). He sells a paid Google Analytics course, other GTM and GA4 courses, and gives away free ebooks as lead magnets. Evidence is live demos in 2 places: his own empty demo property and a GA4 demo account with real ecommerce data (sweaters, apparel, a Black Friday newsletter, site search). The source does not name the demo account [web check: likely Google's public demo account]. One claim rests on his own "multiple experiments" (custom event before page_view does not cause "(not set)" landing pages). No client results, no studies. It is a setup and navigation tutorial, not an ecommerce strategy source. Several recommendations are stated as personal preference (GTM as install method, longer session timeout, 30-second engaged session, older report layout, total users over active users, turning off form interactions).

date signals: Title says 2026. Uses "key events" (Google's newer name for conversions) [web check: date of the conversions to key events rename]. Shows "Analytics Advisor", a Gemini-powered AI chat, marked beta. Shows Reports snapshot templates (page views and users, sales and revenue, marketing performance) and business objectives at property creation that unlock report collections, with an option for the older report layout. GTM tag types named "Google tag" and "GA4 Event". GA4 admin section names used: Data display, Data collection, Data filters, Data retention, Custom definitions, DebugView. The presenter notes several times that Google may change names and menus. Every UI path below carries `[verify UI]`.

## 1. What this source is for

It helps an operator stand up a working GA4 property from zero, install it (preferably through Google Tag Manager), prove it works with GTM Preview and DebugView, read the core standard reports (acquisition, landing pages, pages, monetization, checkout journey, demographics, tech), build 3 kinds of explorations (free form, funnel, path), send 1 custom event with custom parameters, and apply 5 admin settings on day 1. It does not teach ecommerce event tracking (view_item, add_to_cart, purchase with item data). The presenter says that is out of scope and points to docs and his paid course. So every ecommerce report below assumes those events already arrive from the platform, a developer or GTM `[needs brand data: which ecommerce events the store actually sends to GA4, and from where]`.

## 2. Principles

1. **One GA4 account per organization.** Condition: 1 business. Think of the account as the organization; it holds 1 or more properties. The same logic applies to GTM accounts. Basis: presenter's setup advice. [a61d1986b945]
2. **One property per user journey, not per website.** Condition: if visitors move between your websites and then convert (for example main site, then a separate checkout site, then purchase), put all of them in 1 property so the journey is visible in one place. If the sites are separate business lines whose data you never want mixed, give each its own property. Basis: presenter's rule, no data shown. [a61d1986b945] [60bd489184a8] [needs brand data: every domain a shopper touches from landing to thank-you page]
3. **One web data stream, even for several websites.** Condition: when several websites share 1 property. Source says Google "highly recommends" 1 web stream used on all sites. Which domain you type when you create the stream "does not matter much"; the stream still works on other domains. Separate streams are for mobile apps. [a61d1986b945]
4. **Test in 2 places before you publish.** Condition: every new or changed tag. GTM Preview proves the tag fired; GA4 DebugView proves GA4 received the event and its parameters. Publish only after both pass. Basis: presenter's standard workflow, shown twice. [80fdd796ee78] [0aad0a745c66] [6a6a1f68f1b4]
5. **Data needs 24 to 48 hours before reports are right.** Condition: after a new install, a new event or a new custom dimension. Some events show sooner but are "not fully processed", so traffic acquisition and other reports "remain inaccurate for a while". Use Realtime and DebugView for fast checks; judge reports the next day or later. [0aad0a745c66] [a043dadb24a2] [50fb683ebc09]
6. **GA4 does not track ecommerce out of the box.** Condition: always. Item views, add to cart, checkout steps, purchases, product data and revenue only appear if the site, a developer, GTM or a platform integration sends them. Stated 4 times in the source. Without them the monetization, checkout journey and funnel reports are empty or partial. [d6b4bece9591] [ae2ed547485e] [2cac3e89ff27] [70e866a19de2] [needs brand data: GA4 ecommerce event coverage and item parameters]
7. **Pick the report that matches the question: first touch or this session.** Condition: whenever you judge channels. User acquisition credits the first source that ever brought the user, for all their later sessions. Traffic acquisition credits each session's own source. Source says most marketers actually want traffic acquisition (his opinion). [a26e80bd2101]
8. **Mark only business outcomes as key events.** Condition: when choosing conversions. An event is any tracked interaction; key events are the ones that matter to the business (source examples: purchase, signup). Card adds "over-marking dilutes the signal"; the source itself does not say this. [70e866a19de2]
9. **Custom parameters are invisible in reports until registered.** Condition: any parameter you invent (not a standard GA4 parameter). Register it as a custom dimension with event scope, then wait for processing. [a043dadb24a2] [50fb683ebc09]
10. **Configure 5 settings on day 1, or at least consider them.** Condition: every new property, and as an audit of old ones. The intro calls them "necessary things you must configure in every analytics account from day one"; the closing section softens this to "configure ... or at least thoroughly consider". Retention first, because it cannot be recovered later. [8f32ae745a5b] [48b668a95917] [d2833e8633f3]
11. **Treat AI answers about your data as hypotheses.** Condition: Analytics Advisor or any AI chat. Fine for simple number lookups you can confirm in a report; not for explanations of why data looks wrong. You still need to understand GA4 to catch errors. Basis: 1 correct demo answer and 1 wrong one. [bb64df0f76c5] [1ed5edfed51c]
12. **Demographics are directional only.** Condition: age, gender and interests from Google signals. Source: "not that accurate, but it can still give you a general sense about your audience." Country, region and city do not need Signals. [3d2bb5de8e28] [374c795a2291]

## 3. Procedures

### 3.1 Create account, property and data stream `[verify UI]`

1. Go to analytics.google.com. If you already have a property, click Admin (bottom left), then Create account. If you have never used GA, you are prompted to create an account right away. [a61d1986b945]
2. Name the account (the organization). Review the data sharing settings (for example "recommendations for your business"); the presenter keeps the defaults. Click Next.
3. Name the property. Choose the reporting time zone (where the business is located) and the currency. Click Next. [needs brand data: business time zone and store currency, which must match the store and finance reports]
4. Business details: choose industry and business size. Click Next.
5. Business objectives: pick 1 or more. Each objective unlocks a collection of reports (for example "generate leads" unlocks a lead collection). The presenter prefers the older report layout and chooses "other business objectives". Google may change this.
6. Click Create. Accept the terms of service.
7. Create a data stream. Choose Web (apps get their own streams). Enter the website domain. If the property will cover several websites, enter any 1 of them.
8. Name the stream.
9. Enhanced measurement (automatic event tracking): keep most events on when starting out. The presenter turns off form interactions because "it's not very reliable". He says experienced users will turn off more over time; he does not say which.
10. Click Save, then Create and continue. GA4 now asks you to install the Google tag.

### 3.2 Install the Google tag: 3 methods `[verify UI]`

Pick 1. [53bd7d4a85c1]

A. **Developer adds the code (custom sites without a GA integration).** Give the Google tag snippet to a developer and ask for it on every page. Google recommends the `<head>`; the `<body>` is acceptable if the head is not possible. Exact steps depend on how the site is built; the source gives no universal method.

B. **Platform integration.** Paste the measurement ID (starts with `G-`) into the platform's GA or tracking ID field and save. Find the ID: on Home while no data has arrived yet, or at Admin > Data streams > your web stream > Measurement ID. [web check: current GA4 method for the store's platform, for example Shopify's Google channel app, and which ecommerce events it sends] [needs brand data: store platform]

C. **Google Tag Manager (presenter's preferred method).** Has a learning curve, but you can manage Google tags and other vendor tags (Meta pixel, LinkedIn Insight tag) mostly without a developer.
1. Go to tagmanager.google.com. Create a new account. Name it (1 account per organization is usually enough). Choose country.
2. Name the container (for example your domain). Choose Web. Click Create. Accept the terms of service.
3. GTM shows 2 code snippets. Add the first to all pages. The presenter says the second "can be ignored. It's not that important." (See section 9.)
4. In GTM: Tags > New > Tag configuration > Google Analytics > Google tag. Paste the measurement ID from GA4 Admin > Data streams. Name the tag (presenter uses "GA4 config"). Save.
5. Test (procedure 3.3).
6. Click Submit. Enter a version name (for example "installed GA4"). Click Publish. From this moment GA4 receives data from all visitors.

### 3.3 Test with GTM Preview and GA4 DebugView `[verify UI]`

1. In GTM click Preview. Enter the URL of a page where the GTM container is installed. Click Connect. [0aad0a745c66] [80fdd796ee78]
2. The site opens in a new tab or window and shows "Tag Assistant connected". Preview mode is working.
3. In the Preview panel, open Initialization and confirm the Google tag fired. For custom events, do the action on the site, then open that event in Preview and confirm your tag fired.
4. In GA4 go to Admin > DebugView (the source also shows it under Admin > Data display > DebugView). You should see events such as page_view, scroll, and possibly first_visit and session_start.
5. Click an event and check parameters. For page_view, page_location must match the URL you opened. For custom events, confirm your custom parameters are there, not only the automatic ones.
6. Only after both checks pass, Submit and Publish the GTM container.
7. If Preview does not work or disconnects, close the Preview window and the website tab and start Preview again. Click Preview again after every change to refresh it.
8. An "unknown tag type" note in Preview is a Preview bug; the presenter says tags still work.

### 3.4 Set up the Reports snapshot while data processes `[verify UI]`

1. Home shows "data collection is active" once hits arrive. Wait 24 to 48 hours for reports.
2. Reports > Reports snapshot: choose a template for your main priority. Page views and user counts; sales and revenue (purchases, carts); or marketing performance (users, sessions, top traffic sources). Click Preview template to see the widgets first. The presenter picks marketing performance.

### 3.5 Send a custom event with parameters through GTM (menu link click example) `[verify UI]`

Use when you need an interaction GA4 does not collect automatically. Automatic examples the source names: page view, scroll, file link clicks (for example PDF), video views. [50fb683ebc09] [6a6a1f68f1b4]

1. GTM > Triggers > New > Trigger configuration > Just Links. Keep "All link clicks". Name it "all link clicks". Save.
2. Click Preview to refresh. Connect to the page.
3. On the site, hold Ctrl (Cmd on Mac) and click a menu link so it opens in a new tab and the page does not unload.
4. In Preview, open the Link Click event.
5. If no click variables appear: GTM > Variables > Built-in variables > Configure > tick all Click variables. Refresh Preview and click the link again.
6. In Preview > Variables for that Link Click, read Click Text, Click URL and Click Classes.
7. Find a value that only your target links have. In the demo, Click Classes held a class naming it as a main-menu navigation link. Your site's classes will differ `[needs brand data: theme's CSS classes for the element]`.
8. Edit the trigger: Some Link Clicks > Click Classes > contains > the class value, without quotation marks. Rename the trigger. Save.
9. Copy the measurement ID (Admin > Data streams > web stream, or open the Google tag in GTM).
10. Tags > New > Tag configuration > Google Analytics > GA4 Event. Paste the measurement ID. A green check mark shows it is valid.
11. Event name: `menu_link_click`. Rule: all lowercase, underscores instead of spaces. [23f8bf44b13a]
12. Expand Event parameters. Add `menu_item_name` = `{{Click Text}}` and `menu_item_url` = `{{Click URL}}` (insert with the variable button). You may use standard parameters or your own; the demo uses custom ones.
13. Triggering: choose the link click trigger. Name the tag. Save.
14. Preview, click several menu links with Ctrl held, confirm the tag fired on each Link Click.
15. GA4 > Admin > Data display > DebugView: confirm `menu_link_click` events arrive with `menu_item_name` and `menu_item_url`.
16. Register the parameters (procedure 3.6).
17. GTM > Submit. Version name, for example "menu link click tracking in GA4". Publish.
18. Wait at least 24 hours before looking for it in reports.

### 3.6 Register custom parameters as custom dimensions `[verify UI]`

1. Confirm the parameter arrives in DebugView first. [a043dadb24a2]
2. GA4 > Admin > Data display > Custom definitions > Create custom dimension.
3. Event parameter: paste the exact key (for example `menu_item_name`). Card adds: names are case-sensitive and must match exactly across GTM, GA4 and filters [50fb683ebc09].
4. Dimension name: a readable label (demo: "menu item name").
5. Scope: Event. Save.
6. Repeat for each parameter (`menu_item_url`).
7. After processing, the dimensions show as widgets in the event's detail in the Events report, and can be used in explorations.

### 3.7 Where to read a custom event after 24 to 48 hours `[verify UI]`

1. **Events report**: find the event name; open it to see charts plus 1 widget per registered custom dimension. (The demo property shows the same for its site search event with a "search term" dimension.)
2. **Traffic acquisition**: in the event count column choose the event to see counts per traffic source.
3. **Free form exploration**: dimensions `menu_item_name`, `menu_item_url`, Event name; metrics Total users and Event count. Rows: both item dimensions. Values: both metrics. Filter: Event name exactly matches `menu_link_click` (copy the name from the GTM tag to be sure). The presenter prefers Total users over Active users. Event count here means clicks per menu item.

### 3.8 Read the traffic acquisition report for channels and campaigns `[verify UI]`

1. Reports > Acquisition > Traffic acquisition. Default rows are channel groups with sessions and, scrolled right, revenue. [a26e80bd2101]
2. Change the primary dimension to Session source / medium for detail.
3. Sort by clicking a column header (sessions, or Total revenue). The chart follows the sorted metric.
4. The chart shows the top 5 rows by default. Untick rows, tick the one you want, click Plot rows. If you clear all rows the chart goes blank; plot at least 1 row (or the total).
5. Change chart granularity (day to week) and the date range (demo: last 90 days).
6. Filter a channel: use the search box (matches any row containing the word, for example "email") or add a filter: Session medium > exactly matches > email > Apply. Remove it with the X.
7. Add a second dimension with the plus button: Session campaign name. Sort by sessions or revenue to see which campaign produced the most. Demo: 1 newsletter produced the most email revenue, which the presenter links to Black Friday in November.
8. Paid social pattern (presenter's example, not run on real data): Session medium exactly matches cpc (if that is the value your ads use) AND Session source contains facebook.com, then add Session campaign name. [needs brand data: the store's UTM conventions for Meta and other paid channels]

### 3.9 Build a free form exploration `[verify UI]`

Layout: 3 columns. Variables (dimensions, metrics, segments), Settings (differs by technique), Output. [20d5752ed796] [70c537e426a1]

Revenue by country and device:
1. Explore > Blank (defaults to Free form).
2. Dimensions plus: tick Device category and Country. Confirm.
3. Metrics plus: search "revenue", tick Purchase revenue. Confirm.
4. Drag or double-click: Country to Rows, Device category to Columns, Purchase revenue to Values.
5. Read revenue per country split into desktop, mobile, tablet. Change visualization: bar chart, heat map (darker = higher), or plain table.

Site search terms (assortment gaps): [0c84e8cf0da8]
1. Plus to add a new tab, Free form.
2. Dimensions plus: Event name and Search term. Metrics plus: Event count.
3. Search term to Rows, Event count to Values.
4. The first row is empty with a huge count because all events are included. Fix: Filters > Event name > exactly matches > the site search event (demo: `view_search_results`) > Apply. The filter list only offers dimensions already added to the Variables column.
5. Read top terms. Presenter's use: find gaps between what people search for and what the site offers `[needs brand data: site search event name and whether search_term is captured]`.

### 3.10 Build a funnel exploration `[verify UI]`

1. Explore > Funnel exploration, or plus on an open exploration > Funnel exploration. [2cac3e89ff27]
2. Steps > pencil icon.
3. Step 1 "Viewed product": event name `view_item`.
4. Step 2 "Added to cart": `add_to_cart`. Optional: Add parameter (for example item ID) to funnel 1 product, or add a condition on page hostname or page location.
5. Step 3 "Checkout": `begin_checkout` (source calls it the recommended ecommerce event GA4 "kind of requires").
6. Step 4 "Purchase": `purchase`. Apply.
7. Read users at each step and drop-off.
8. Add a Breakdown dimension: Device category. Demo: desktop completed better, which "might indicate" a weaker mobile experience worth a closer look.
9. Your property may not have these events or may use other names `[needs brand data: actual event names]`.

### 3.11 Build a path exploration, including backward from purchase `[verify UI]`

1. Plus > Path. Switch the node dimension from Event name to Page path. Demo: session_start most often begins on the homepage. Click nodes to expand where visitors go next. [85c9ae567054] [663dee00fd8e]
2. Backward: Start over > choose the ending point > Event name > search `purchase` > select. Switch to Page path. Expand backward past the checkout pages until non-checkout pages appear.
3. Checkout loop check: Start over > starting point Event name `begin_checkout` > Page path > expand. Demo: some users go to the account page and back to checkout. Presenter reads this as a possible confusing login or flow at checkout, "worth investigating further", not proven.

### 3.12 Share an exploration `[verify UI]`

1. Standard reports are visible to every user with property access. Explorations are private to their creator by default. [20d5752ed796]
2. Open the exploration, click the share icon, click OK. Needs enough permission (the presenter lacked it in the demo account).
3. Shared explorations are view-only. Others must make their own copy to change it. The presenter finds this inconvenient and says it may change.

### 3.13 Day-1 admin settings: the source's 5 `[verify UI]`

Most settings sit at property level; a few at account level. [48b668a95917] [8f32ae745a5b] [d2833e8633f3]

1. **Data retention.** Admin > Data retention: change event data retention from 2 months to 14 months. Save. Premium (paid GA) allows longer. Reason given: by default, explorations only reach the last 2 months. Do it as soon as the property exists. [017251ba79b0] [4bce06a3a94d]
2. **Domains (cross-domain tracking).** Only if 1 property tracks several websites. Admin > Data streams > web stream > scroll > Configure tag settings > Configure your domains. Add each root domain (demo: example.com and anotherwebsite.com). A root domain covers all its subdomains. If 5 domains are tracked, add all 5. Save. [f965ebdb8cdc] [014312f9dcef] [60bd489184a8]
3. **Internal traffic.** Condition: most staff work from an office or have static IPs. Configure tag settings > Show more > Define internal traffic > Create. Rule name, for example "office IP". Condition: IP address equals the real office IP (a link on the screen shows your current IP). Add more conditions if needed. Then Admin > Data collection > Data filters > the internal traffic filter shows "Testing" > Activate filter. From that moment staff traffic is excluded. [92193cbedb5d] [822ba43fffb7] [needs brand data: office and warehouse IPs, whether they are static]
4. **Session timeout and engaged session timer (presenter's personal recommendation; "some people might disagree").** Admin > Data streams > web stream > Configure tag settings > Show more > Adjust session timeout. Session timeout: default 30 minutes; he sets at least 4 hours and often the maximum 7 hours 55 minutes. Engaged session timer: default 10 seconds; he sets at least 30 seconds "or maybe even more". Save. [ca9e3c7b6aec] [c91c77718ecd] [ce843bc07545]
5. **Google signals.** Admin > Data collection > Google signals data collection > turn on (the demo shows 2 "turn on" clicks). Needed for age, gender and interests, which otherwise appear but stay empty. Enabling it turns on some Google advertising features; if the company is strict on legal requirements, talk to legal first. Data can take weeks to appear. [374c795a2291] [bc1344c5d961] [web check: current consent and regional rules for Google signals in the store's markets]

## 4. Rules, thresholds and numbers

| Rule | Number or threshold | Condition | Source's basis | Card id |
|---|---|---|---|---|
| Wait before trusting reports | 24 to 48 hours | New install, new event, new custom dimension | Presenter; some events show sooner but are not fully processed | 0aad0a745c66, a043dadb24a2 |
| Wait before checking a new custom event in reports | at least 24 hours | After publishing the GTM change | Presenter | 50fb683ebc09 |
| Event data retention | 2 months default; set 14 months | Every new property, at once; Premium can go longer | Explorations only reach the retention window | 017251ba79b0, 4bce06a3a94d, 8f32ae745a5b |
| Session timeout | 30 min default; at least 4 h; often max 7 h 55 min | Presenter's preference; trade-off stated | Fewer "(not set)" and checkout landing pages; fewer total sessions | ca9e3c7b6aec, c91c77718ecd |
| Engaged session timer | 10 s default; at least 30 s or more | Presenter's opinion that 10 s is "not engaged enough" | Opinion, no data | ce843bc07545, ca9e3c7b6aec |
| Active user definition | at least 10 s engagement, or a key event, or 2+ page views in the session, or a new user | As the presenter explains it | Presenter's description of GA4 | 5c2c65569229 |
| Realtime windows | last 5 min and last 30 min users; Realtime pages covers last 30 min | Checking data arrives | UI | none |
| Traffic acquisition chart | top 5 rows by default | Use Plot rows for others | UI | a26e80bd2101 |
| Domains in cross-domain list | all of them, e.g. 5 domains = 5 entries; root domain covers subdomains | 1 property, several sites | Presenter | f965ebdb8cdc |
| Event name format | lowercase, underscores instead of spaces | Every GA4 event | Presenter | 23f8bf44b13a |
| Custom dimension scope | Event | Event parameters | Presenter | a043dadb24a2 |
| Google signals demographics delay | "might take even weeks" | After enabling | Presenter | 374c795a2291 |
| Measurement ID format | starts with `G-` | Installing through a platform field | UI | 53bd7d4a85c1 |
| GA accounts per business | 1 usually enough | Same logic for GTM accounts | Presenter | a61d1986b945 |
| Web data streams per property | 1, even for several websites | Google's recommendation per source | Presenter citing Google | a61d1986b945 |
| Analytics Advisor demo answer | 125 purchases from organic search last week; confirmed correct in traffic acquisition | Example only | Demo | bb64df0f76c5 |

## 5. Diagnostics and checks

| Check | How | Good | Bad | Next step | Cards |
|---|---|---|---|---|---|
| Is data arriving? | Reports > Realtime overview (users last 5 and 30 min); Realtime pages | Users and pages appear | Nothing after visiting the site | Run GTM Preview; check tag published and container on every page | 0aad0a745c66 |
| Did the tag fire and did GA4 receive it? | GTM Preview (Initialization or the action event) then GA4 DebugView | Tag fired; event with correct page_location and custom parameters in DebugView | Tag not fired, or event missing, or parameters missing | Fix trigger or variables; enable Click variables; refresh Preview | 80fdd796ee78, 6a6a1f68f1b4 |
| Custom parameter missing from reports | Admin > Custom definitions | Registered, event scope, exact key | Not registered or key mismatch | Register; wait 24 to 48 h | a043dadb24a2 |
| Checkout pages listed as landing pages | Engagement > Landing page, sort by revenue | Landing pages are real entry pages (home, collections, product pages) | Checkout shows as a landing page | Cause per source: session expired (30 min default) mid-checkout, new session started on checkout. Consider a longer session timeout | 5c2c65569229, ca9e3c7b6aec |
| Many "(not set)" landing pages | Landing page report | Few | Many | Source: longer session timeout reduces them. Do not believe the claim that an event before page_view causes it; the presenter's experiments say it does not | ca9e3c7b6aec, bb64df0f76c5 |
| Checkout step with a device or browser problem | Monetization > Checkout journey; breakdown Device category, then Browser | Similar drop-off across browsers | 1 browser drops much more at 1 step | Reproduce the checkout in that browser; treat as a likely technical bug, not proven | ae2ed547485e |
| Mobile vs desktop funnel gap | Funnel exploration with Device category breakdown | Similar completion | Desktop much higher (as in the demo) | Look closer at mobile experience; hypothesis only | 2cac3e89ff27 |
| Shoppers looping at checkout | Path exploration from begin_checkout | Straight path to purchase | Checkout to account and back | Look at login flow at checkout; test | 85c9ae567054 |
| Products viewed but not bought | Monetization > E-commerce purchases: item views, add to carts, purchases, item revenue | Views convert to carts and purchases | High views, few carts or buys | Card adds: test price, images, product page copy. Source only shows the columns and sorts by item revenue | d6b4bece9591 |
| Searches with no matching product | Free form of search term by event count, filtered to the search event | Top terms match catalogue | Frequent terms you do not sell | Assortment or naming gap to review | 0c84e8cf0da8 |
| Staff traffic in data | Admin > Data filters | Internal traffic filter Active | Filter still in Testing | Activate | 92193cbedb5d |
| Exploration history too short | Admin > Data retention | 14 months | 2 months | Change now; past data beyond the window is not recovered (card claim) | 017251ba79b0 |
| Demographics empty | User attributes > Demographic details | Age, gender, interests populated | Dimensions show no data | Google signals is off; enable after legal review; wait weeks | 374c795a2291 |
| AI Advisor answer | Open the linked report, check date range, recount | Same number, right date range | Wrong range or wrong reasoning | Use the report, not the AI | bb64df0f76c5 |

Report reading notes the source gives:
- Pages and screens revenue is credited to the page where the conversion happened, so most revenue sits on checkout. The presenter says revenue "does not make a lot of sense" in this report. Use Landing page revenue to judge entry pages. [5c2c65569229]
- In Landing page, `/` is the homepage. Revenue shown is for sessions that started on that page.
- "Views" in Pages and screens means page views.
- User acquisition keeps a returning user and all their sessions under the first source, even after 5 later sessions from other sources. [a26e80bd2101]

## 6. Tools, settings and named features

All `[verify UI]`.

- **GA4 hierarchy**: Google account > GA4 account (organization) > property (data store for 1 or more sites) > data streams (web, apps). [a61d1986b945]
- **Enhanced measurement**: automatic events chosen at stream creation. Named: page view, scroll, file (PDF) link clicks, video, form interactions (presenter disables).
- **Measurement ID**: `G-` ID; in Admin > Data streams > stream, or on Home before data arrives.
- **Google Tag Manager**: tagmanager.google.com; account, container (Web), 2 snippets, Tags, Triggers (Just Links, All vs Some Link Clicks), Variables (built-in Click Text, Click URL, Click Classes; enable under Configure), Preview (Tag Assistant), Submit and Publish with version names. Tag types: Google tag, GA4 Event. [53bd7d4a85c1] [50fb683ebc09]
- **DebugView**: Admin > DebugView (or Admin > Data display > DebugView). Shows incoming debug events and their parameters. Card adds: shows only a recent window [80fdd796ee78].
- **Custom definitions**: Admin > Data display > Custom definitions > Create custom dimension (name, scope, event parameter).
- **Key events**: events marked as important; selectable in acquisition reports. [70e866a19de2]
- **Reports snapshot templates**: page views and users; sales and revenue; marketing performance.
- **Report collections** (names vary by chosen business objective): Realtime overview, Realtime pages; Acquisition overview, User acquisition, Traffic acquisition; Engagement (Landing page, Pages and screens, Events); Monetization or revenue (Overview, E-commerce purchases, Checkout journey); User attributes > Demographic details (country, region, city; age, gender, interests with Signals); Tech > Tech details (browser, operating system, device). [3d2bb5de8e28]
- **Report controls**: primary dimension switch, plus button for a secondary dimension, column sort, search box, quick filter (exactly matches, contains), Plot rows, day/week granularity, date range, event count and key event selectors.
- **Explore techniques**: Free form, Funnel exploration, Path exploration, Segment overlap, Cohort exploration, others. Presenter mostly uses the first 3. Visualizations in free form: bar chart, heat map, plain table. [20d5752ed796]
- **Analytics Advisor**: Gemini-powered AI chat, icon top right, beta; shows its reasoning and links to a report. [bb64df0f76c5]
- **Admin settings**: Data retention; Data streams > Configure tag settings (Configure your domains; Show more > Define internal traffic; Adjust session timeout incl. engaged session timer); Data collection > Data filters; Data collection > Google signals data collection.

## 7. Examples and case results

Examples only, from the presenter's demo accounts. Not benchmarks.
- Traffic acquisition in the demo ecommerce account: most sessions from Google organic, then Google paid, newsletters. The top email revenue came from 1 newsletter, which the presenter ties to Black Friday in November. [a26e80bd2101]
- Landing page report: many sessions start on `/` (homepage); top revenue entry pages include a new products list, apparel and a clearance page; checkout also appears as a landing page because of the 30-minute session timeout. [5c2c65569229]
- E-commerce purchases: top item by item revenue was a sweater. [d6b4bece9591]
- Free form: revenue by country, largest from United States, split by desktop, mobile, tablet. [20d5752ed796]
- Funnel: desktop completion rates higher than mobile. [2cac3e89ff27]
- Path from begin_checkout: users jump to the account page and back to checkout. [85c9ae567054]
- Analytics Advisor: "purchases from organic search last week" returned 125, matching Traffic acquisition with the purchase key event; asked why landing pages are "(not set)", it returned numbers and trends it was not asked for and repeated the myth that a custom event before page_view causes "(not set)". [bb64df0f76c5] [1ed5edfed51c]

## 8. Mistakes the source warns about

1. Expecting full reports right after install or after a new event. Wait 24 to 48 hours. [0aad0a745c66]
2. Publishing a GTM change without testing in Preview and DebugView. [80fdd796ee78]
3. Expecting ecommerce reports to fill without sending ecommerce events. [d6b4bece9591]
4. Reading User acquisition when you mean per-session channel performance. [a26e80bd2101]
5. Judging page value by revenue in Pages and screens (revenue sits on the conversion page). [5c2c65569229]
6. Leaving data retention at 2 months, which limits explorations to 2 months. [017251ba79b0]
7. Separate properties for sites in 1 journey, or separate web streams per site. [60bd489184a8] [a61d1986b945]
8. Forgetting to list all domains in Configure your domains when 1 property covers several sites. [f965ebdb8cdc]
9. Defining internal traffic but leaving the filter in Testing. [92193cbedb5d]
10. Event names with capitals or spaces. [23f8bf44b13a]
11. Sending custom parameters but not registering them as custom dimensions. [a043dadb24a2]
12. Building a free form report without filtering to the event you care about (gives a big empty row). Adding a filter on a dimension you have not first added to Variables (it will not be in the list). [0c84e8cf0da8]
13. Clicking a menu link without Ctrl or Cmd during Preview, so the page unloads (implied by the presenter's method).
14. Trusting Analytics Advisor on causes or blindly on numbers; it can use a wrong date range. [bb64df0f76c5]
15. Believing the "custom event before page_view causes (not set) landing page" myth, which also appears in blog posts. [bb64df0f76c5]
16. Enabling Google signals without legal review where the company is strict on legal requirements. [374c795a2291]
17. Treating age, gender and interests as accurate. [3d2bb5de8e28]
18. Relying on form interactions from enhanced measurement (presenter finds it unreliable).

## 9. Caveats, conflicts and what is missing

**Inside the source and its cards**
- The "5 settings" list is not stable. Source text: (1) retention, (2) domains, (3) internal traffic, (4) session timeout plus engaged session timer as 1 item, (5) Google signals. Card 8f32ae745a5b drops Google signals and splits engaged session out as its own item. Card d2833e8633f3 omits the engaged session timer. Cards 48b668a95917 and the source text agree. Use the source text order.
- "Must configure" (intro) versus "configure or at least thoroughly consider" (closing). Items 4 and 5 are opinion or carry legal trade-offs.
- Session timeout: the presenter states the trade-off himself: longer timeouts cut "(not set)" and false checkout landing pages but merge several same-day visits into 1 session, so session counts drop. Card c91c77718ecd adds that per-session conversion rate changes and historical comparisons break; the source does not say this. Card ca9e3c7b6aec adds that visit frequency is understated.
- Several card claims are not in the source text: exploration sampling and thresholds, explorations expiring, retention not affecting standard reports, retention increase not restoring deleted data, VPN and home-office IPs not filtered, filters not restating past data (the source does say "from this moment"), cross-domain limits with third-party checkouts, self-referrals, DebugView time window. Treat these as the card writer's additions `[web check: each before relying on it]`.
- The source says checkout drop-off by browser "might indicate" a bug and looping paths are "worth investigating". These are hypotheses, not findings.

**Against common ecommerce advice**
- Maximum session timeout (7 h 55 min) is a minority view. Many analysts keep 30 minutes for comparability with ad platforms and past data. The presenter admits "some people might disagree". Decide per brand and log the change date `[needs brand data: typical time from first visit to purchase]`.
- The engaged session timer has an upper limit the source does not state `[web check: current maximum engaged session timer]`. Changing it breaks engagement rate comparisons with older periods.
- Calling Google signals a day-1 setting conflicts with privacy-first advice for regions with consent rules; its role in reporting has also changed over time `[web check: current Google signals behavior, thresholding effect on reports, consent mode requirements]`.
- "The second GTM snippet can be ignored" conflicts with Google's install instructions, which place the noscript snippet after the opening body tag `[web check: current GTM install instructions]`. Low impact for most shoppers.
- The Facebook filter example (medium = cpc, source contains facebook.com) is a sketch. Ecommerce practice is to set UTM parameters on every paid ad and check how GA4's default channel group classifies them `[needs brand data: UTM template used on Meta ads]` `[web check: GA4 default channel group rules for paid social]`.
- GTM "on all pages" does not describe hosted checkouts where you cannot add code (for example Shopify checkout pages use a pixel or app system) `[web check: current Shopify customer events and GA4 integration]` `[needs brand data: store platform, checkout domain]`.

**Missing**
- How to send ecommerce events and item parameters (explicitly out of scope). This is the core need for a store.
- Purchase deduplication, transaction IDs, refunds, consent mode, UTM rules, attribution settings and model choice, BigQuery export, linking Google Ads or Search Console, audiences, user permissions.
- How to choose which key events to mark (only examples: purchase, signup).
- Which enhanced measurement events to disable beyond form interactions.
- Data thresholds for small segments, cohort and segment overlap explorations.
- GA4 versus store backend revenue reconciliation `[needs brand data: platform or Metabase order totals to compare against GA4 purchase revenue]`.

## 10. Card index

- 017251ba79b0 GA4 data retention: switch from 2 months to 14 months
- c91c77718ecd Prevent fragmented sessions by extending GA4 session timeout
- 014312f9dcef Configure cross-domain tracking for checkout on a separate domain
- 822ba43fffb7 Filter internal office IP traffic out of GA4
- 6a6a1f68f1b4 Create custom GA4 events via GTM with triggers and parameters
- a043dadb24a2 Register GTM custom parameters as GA4 Custom Dimensions
- 80fdd796ee78 Test GA4/GTM event setup before publishing the container
- 60bd489184a8 Use a single GA4 property across domains in one journey
- 663dee00fd8e Reverse-engineer the purchase path with Path Exploration
- 70c537e426a1 Build Free Form tables in GA4 Explorations
- ce843bc07545 Extend the engaged-session threshold above the 10-second default
- bc1344c5d961 Enable Google Signals for demographic audience data
- 23f8bf44b13a Apply GA4 naming conventions to custom events
- d2833e8633f3 Treat GA4 setup as a five-setting baseline for ecommerce accuracy
- 1ed5edfed51c Do not rely on AI chat assistants for GA4 technical configuration
- a61d1986b945 Structure a GA4 account for an ecommerce store
- 53bd7d4a85c1 Install the GA4 tag: CMS, hardcode, or GTM
- 0aad0a745c66 Test a GA4 tag with GTM Preview and DebugView
- a26e80bd2101 Read acquisition reports: first touch vs session
- d6b4bece9591 Use the ecommerce purchases report for product decisions
- ae2ed547485e Diagnose checkout drop-off by device or browser
- 5c2c65569229 Landing page vs pages and screens report
- 70e866a19de2 Mark key events and pick the right conversion metric
- 20d5752ed796 Build a free-form exploration for product/device decisions
- 0c84e8cf0da8 Mine site-search terms to find assortment gaps
- 2cac3e89ff27 Funnel exploration: build an ecommerce funnel with breakdowns
- 85c9ae567054 Path exploration: work backward from purchase or checkout events
- 50fb683ebc09 Create and register custom events and dimensions in GA4 via GTM
- 8f32ae745a5b Configure five settings in every new GA4 property
- bb64df0f76c5 Use Analytics Advisor cautiously for quick questions
- 3d2bb5de8e28 Demographics, tech and region reports for audience context
- 4bce06a3a94d Set GA4 event data retention to 14 months at property creation
- f965ebdb8cdc Register all business domains for cross-domain tracking in GA4
- 92193cbedb5d Exclude internal (employee) traffic from GA4 reports
- ca9e3c7b6aec Extend GA4 session timeout and engagement timer (source opinion)
- 374c795a2291 Enable Google Signals to populate demographics and interests
- 48b668a95917 Configure five foundational GA4 settings in the correct order
