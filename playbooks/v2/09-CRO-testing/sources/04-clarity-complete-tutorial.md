# Microsoft Clarity COMPLETE Tutorial in 2026 to Skyrocket Conversions

source_id: 1codPdK-qaL_2SoPf_nmftxOcUIzNczWB  |  folder: /09-CRO-testing  |  cards: 11  |  words: 7395  |  type: transcript (YouTube tutorial)
credibility: An unnamed presenter who runs a CRO agency that audits client sites for ecommerce, SaaS and B2B brands. The video ends with a pitch for a free website audit. Evidence is the presenter's own client work (audit screenshots, recordings from a delivery client, a B2B contact page, a SaaS pricing page) plus Clarity's public demo account. No sample sizes, no test results with numbers, no statistics. Benchmarks ("under 1 to 2% rage clicks is good", "5 to 7% CTA click-through", "60% never scroll past the hero") are the presenter's working heuristics or unsourced claims.
date signals: The title says 2026, but the recording itself says "today's July 29th 2024" and picks a date range from January 2024. So the walkthrough reflects the Clarity interface of mid-2024. Feature names (Insights block, Smart events, Area maps, Change screenshot, Edit areas, Skip inactivity, sort by Clicks and Pages) may have moved or been renamed since. `[verify UI]` on every Clarity step.
scope note: The source header says this belongs in 09-CRO (gathering behaviour data to form test hypotheses). It routes GA4 funnels and path explorations to 06-MEA and page redesign or copy changes to 07-LPG. It also says to skip the agency pitch and basic definitions.

## 1. What this source is for

It teaches an operator how to read Microsoft Clarity to find purchase-path friction and turn it into a test idea. It covers the dashboard Insights block (rage clicks, dead clicks, excessive scrolling, quick backs), click maps, scroll maps, Area maps, and session recordings. It gives a method for picking which recordings to watch and when to stop. It is a hypothesis-generation source. It does not cover test design, sample size or statistics.

## 2. Principles

1. **Start every map review from the page's one core action.** Before looking at a heatmap or scroll map, name the main thing the page should get people to do (add to cart, buy now, sign up, submit a form). Then ask 3 questions: do people reach that section, do they take the action, and if not, what would get them there. Applies to ecommerce and B2B alike. Evidence: presenter's method, shown on the Clarity demo site. [09583734387e] [6d2e6fafa7df]

2. **Clarity's value is the behaviour Insights and recordings, not the top-line metrics.** Scroll depth, active time, pages per session, sessions, smart events (add to cart, checkout), channel, campaign, source, browser, device and popular pages can all be pulled from Google Analytics, which the presenter says does funnels "a much better job". Focus on the Insights block: rage clicks, dead clicks, excessive scrolling, quick backs. Caveat from the card: keep top-line metrics as context and segmentation, do not throw them out. [e053644d5707]

3. **A percentage alone never justifies a change. Watch the recordings behind it.** Each Insight has a camera icon that opens the matching recordings `[verify UI]`. The presenter says it "doesn't really matter what the metrics are": if a real usability issue exists, fix it whatever the rate. When the rate is low and no clear issue shows, it is not a priority. [e053644d5707] [9d9871ee324b] [5b9da7dd1967]

4. **Rage clicks usually mean a shopper cannot get out of something or cannot make something work.** Typical causes: a popup that appears in the first 5 seconds before the visitor has even scrolled; a chat bot covering the add-to-cart or form submit button; a hard-to-hit close control. The presenter calls these "low hanging fruit". Condition: many causes are possible, so confirm in recordings before assuming it is a popup. [9d9871ee324b]

5. **Dead clicks matter only when the shopper expected something useful.** A dead click is a click on an element with no action. Some are fine: "As seen on" or "Featured in" press logos should often stay unclickable, because linking out sends shoppers away from the purchase. Others are real problems: pricing blocks where only 1 button works, a site logo that does not return to the homepage, informational check marks, product images that do not open a gallery. If the missing action would help the shopper toward purchase, it is a conversion hypothesis. [0eae610ddc62]

6. **Excessive scrolling and quick backs usually mean missing or buried information.** Excessive scrolling is fast top-to-bottom scrolling. Causes named: hunting for reviews, hunting for the add-to-cart button or price, or skimming past a long block of text. A quick back is landing on a page and returning to the previous page right away. On a product page it suggests the expected product information was not found. Condition: recordings must separate a real information gap from normal comparison shopping. [5b9da7dd1967]

7. **Assume most visitors see only the top section, then check it with your own scroll map.** The presenter states that "statistically 60% of people will never scroll past the most top section of the website", so most visitors never see services, case studies, testimonials or (for ecommerce) products lower down. This is an unsourced claim. The card says to treat it as a prompt to check store data, not a fact. `[needs brand data: scroll reach per section from Clarity scroll map]` [bc5a8130eee9]

8. **Put social proof above the fold for cold traffic.** A cold visitor "knows nothing about your company", so the page must give a reason to trust and scroll. The presenter says any high-converting site shows social proof (reviews, testimonials, publications) above the fold. Brand examples given as patterns, not minimums: MUD\WTR (49,000+ reviews, a testimonial, "as seen on"); a laser device brand (26,000+ reviews, 4.6 stars, "most trusted laser device brand on Amazon and Google", 365-day trial, free shipping); ZoomInfo (8,000+ G2 reviews, "trusted by 35,000+ businesses"); Clarity itself (Capterra and G2 ratings, 4.5 of 5 on G2). The source contrasts cold traffic, which needs proof up top, with warm traffic, but gives no separate rule for warm traffic. [bc5a8130eee9]

9. **The hero must say who you are, what you do and what is in it for the visitor, in 5 seconds or less.** If it does not, social proof will not save it, and you will see a large drop right after the hero instead of 93 to 95% reach. [bc5a8130eee9]

10. **Move what customers most want to see higher on the page.** If testimonials sit mid-page or at the bottom and only about 30% of people reach them, that is a placement problem. Decide what matters to customers (use surveys, feedback and your own knowledge of the business) and put it where more people will see it. The card adds: do not overload the hero with every proof element. [bc5a8130eee9]

11. **Less is more in UX.** Use Area maps to find redundant elements that get very few clicks and consider removing them, "cuz less is always more when it comes to user experience design". Confirm in recordings before removing. [09583734387e]

12. **Recordings: ask "why" about every action.** Why did they click here, skip that, go back up, leave now. The presenter says you must "apply a little bit of critical thinking" because the real issues are often subtle, not obvious. [0b8d2f6cc4d1]

13. **There is no fixed number of recordings.** Watch until you understand the main friction pattern. The presenter has watched about 100 for some clients and 400 to 450 for others. Stop when it gets repetitive. [0b8d2f6cc4d1]

14. **Recording review never ends.** After a change ships, watch fresh recordings of the new version to confirm the fix and find the next issue. [0b8d2f6cc4d1] [6d2e6fafa7df]

15. **Combine recordings, heatmaps and scroll maps.** The presenter says the full picture comes only from combining them. The card adds that heatmaps show behaviour, not cause; pair with recordings and, where possible, a controlled test. [09583734387e] [6d2e6fafa7df]

16. **Clarity evidence supports a hypothesis. It does not prove one.** The cards stress that Clarity shows behaviour, not causality or statistical significance. Use it to prioritise a test, then use normal experiment design and sample-size math before claiming a lift. The source itself gives no test outcomes. [6d2e6fafa7df] [0b8d2f6cc4d1]

## 3. Procedures

### 3.1 Set up a Clarity review `[verify UI]`
1. Open the Clarity dashboard.
2. Set the date range to a representative period. The presenter uses about the last 6 months (January to July 2024 in the video). If Clarity was installed more recently, use what exists, for example the last 90 days. The card notes 6 months is a habit, not a required sample, and a big site, merchandising or traffic change can make an older window less representative. [e053644d5707]
3. Skim the top-line metrics for context only (sessions, scroll depth, active time, pages per session).
4. Go to the Insights block. Read the rates for rage clicks, dead clicks, excessive scrolling and quick backs.
5. For each Insight, click the camera icon to open the recordings of sessions that had that behaviour.
6. Start with the most valuable and most visited journeys. Ecommerce: homepage or campaign landing page, collection page, product page, cart, checkout. B2B: homepage, contact, get a quote, service pages.
7. For each recurring pattern, note page, device, and the apparent blocker. [e053644d5707] [0b8d2f6cc4d1]

### 3.2 Read a heatmap page `[verify UI]`
1. Click the Heatmaps tab. Clarity lists the most popular pages by traffic (usually 5 to 10 on a real account).
2. Open a page. Check that the screenshot shows the real page. If a popup that fires in the first 3 to 5 seconds, or a misconfigured layout, was captured instead, click **Change screenshot** (top right) and pick another version from the list on the left. You can also pick a screenshot with the navigation menu open to see where menu clicks go.
3. Filter by device: desktop, tablet or mobile. Pick the device with the most traffic first. `[needs brand data: device split]`
4. Choose the map type: **Clicks**, **Scroll**, or **Area**.
5. Click map: find the core CTA and add up the clicks on and around it. Then look at the navigation, text, images and icons that are drawing clicks.
6. Scroll map: read the reach percentage at the top, then find the average fold and the 75%, 50% and 25% checkpoints. Locate the exact section where reach falls sharply.
7. Area map: click **Edit areas** and draw your own areas around the elements you want to compare (navigation, filters, sticky controls, banners, menu toggles, product cards). Read each area's share of clicks.
8. Open the live page next to the heatmap to see what the clicks sit on. [09583734387e] [edd07a1a15f6]

### 3.3 Pick and watch recordings `[verify UI]`
1. Click **Recordings**. The list shows time spent, source, device and more.
2. Open **Filters**. Options named in the source: time frame, device, user action (dead clicks, rage clicks, excessive scrolling), scroll depth, landing page, performance or speed (compare slow and fast experiences), page duration.
3. Click **Sort**. Sort by clicks high to low, then pages high to low. These are the most active visitors.
4. Reverse the sort: clicks low to high, then pages low to high. These are the least active visitors.
5. Compare the 2 groups on the same page type. What do engaged shoppers use that disengaged shoppers miss?
6. For long recordings, turn on skip inactivity and raise speed (the presenter used 4x for a 1-hour session and 1.5x for another). If you are new to Clarity, or hesitation may matter, leave inactivity visible.
7. Block 1 to 2 hours with no distractions.
8. Take notes on every key finding as you go.
9. Stop when new sessions repeat patterns you already have.
10. After shipping a fix, repeat with fresh recordings. [a1a3e1f62713] [0b8d2f6cc4d1]

### 3.4 What to look for in recordings (presenter's checklist)
1. Crucial pages first. Ecommerce: homepage, product page, checkout. B2B: homepage, contact, get a quote, service pages.
2. Common patterns: frequent clicks on non-clickable elements; repeated navigation patterns (for example going back to the top again and again to reach a filter).
3. Frustration signals: rapid clicking, excessive scrolling, skimming past content.
4. Navigation flow: how do people get from homepage to product or service page (menu, CTA button, scroll then CTA)?
5. Conversion issues and engagement time: which sections get more time than others, and what does that suggest?
6. Take notes.
7. Combine with heatmaps and scroll maps. [0b8d2f6cc4d1]

### 3.5 Turn a finding into a test
1. Name the page's single intended progression (view product, pick variant, add to cart, start checkout, complete checkout).
2. Use click and scroll maps to see whether shoppers reach and use the element.
3. Find the most specific barrier (long text block before add to cart, a filter only at the top, a static banner that looks like a button, missing delivery info).
4. Confirm it in recordings for the same page, device and behaviour.
5. Write the hypothesis as change plus reason. Card example: "Because shoppers repeatedly return to the top to change the collection filter, test a persistent filter trigger so refinements remain available while browsing products."
6. Name the metric to judge it by: reach to add-to-cart, CTA click share, filter use without scroll-back, product page views from collection, cart starts, checkout progress, or purchase conversion.
7. Apply normal experiment design and sample-size math before claiming conversion or revenue impact. The source gives none; see the testing sources in this folder. [6d2e6fafa7df]

## 4. Rules, thresholds and numbers

| rule | number or threshold | condition | source's basis | card id |
|---|---|---|---|---|
| Review window | about 6 months; 90 days if Clarity is newer | Longest representative period | Presenter habit | [e053644d5707] |
| Rage click rate that is "good" | under about 1 to 2% | Directional only; fix real defects at any rate | Presenter heuristic | [9d9871ee324b] |
| Demo rage click rate | 0.2% | Example from one account | Observation | [9d9871ee324b] |
| Demo excessive scrolling rate | under 0.01%, "not a major concern" | Example | Observation | [5b9da7dd1967] |
| Dead click rate | no threshold given | Judge by whether the missing action blocks purchase | None | [0eae610ddc62] |
| Quick back rate | no threshold given | Not every quick back is a defect | None | [5b9da7dd1967] |
| Popup timing that causes rage clicks | popup within the first 5 seconds (heatmap screenshot issue: 3 to 5 seconds) | When visitor has barely scrolled | Presenter experience | [9d9871ee324b] |
| Core CTA click-through target | 5 to 7% preferred; 4 to 5% "in and around the average"; under 1% or 3% seen on weak client sites | Directional; one site's click share | Presenter heuristic | [09583734387e] |
| Share never scrolling past top section | 60% | Check against own scroll data | Unsourced "statistically" claim | [bc5a8130eee9] |
| Time for hero to explain who, what, why | 5 seconds or less | All sites | Presenter rule | [bc5a8130eee9] |
| Scroll checkpoints to read | top, 75%, 50%, 25% (plus "average fold") | Every scroll map | Presenter method | [09583734387e] [edd07a1a15f6] |
| Testimonial reach that signals a placement problem | about 30% | Example | Presenter reasoning | [bc5a8130eee9] |
| Recordings to watch | no quota; about 100 for some clients, 400 to 450 for others | Stop when patterns repeat | Presenter practice | [0b8d2f6cc4d1] |
| Recording review block | 1 to 2 hours, no distractions | Each review session | Presenter tip | [0b8d2f6cc4d1] |
| Form fields (B2B forms) | 4 or fewer is "the sweet point"; 8 to 10 fields common, most people do not get past the 3rd or 4th | Lead or contact forms; drop phone number unless sales truly needs it | Presenter observation | none (text only) |

## 5. Diagnostics and checks

| check | how | good | bad | next step |
|---|---|---|---|---|
| Rage clicks | Insights rate, then camera icon to recordings | Low rate and no blocking cause in recordings | Repeated clicks on a popup close, chat widget, or control in the buy path | Remove or delay the blocker; recheck fresh recordings [9d9871ee324b] |
| Dead clicks | Insights, click map, recordings | Clicks on intentionally static items that do not block purchase (press logos) | Clicks on pricing blocks, logo that should go home, product images, delivery copy, check marks | Add the expected action, or make the static nature clear; validate with recordings [0eae610ddc62] |
| Excessive scrolling | Insights, recordings, scroll map | Very low rate, no hunting behaviour | Shoppers racing to find reviews, price, add to cart, or skipping a text wall | Move the missing item up or shorten the block; recheck [5b9da7dd1967] |
| Quick backs | Insights, recordings, click map | Normal comparison shopping | Shoppers leave a product page within seconds because key info is missing | Surface price, reviews, delivery, sizing sooner; recheck [5b9da7dd1967] |
| Core CTA click share | Click map, sum clicks on and around the CTA | 5 to 7% (presenter) | Under 1 to 3% | Emphasise, move up, or redesign the CTA; test [09583734387e] |
| Hero drop | Scroll map, reach just below hero | 93 to 95% still scrolling (demo site) | Large drop right after hero | Rewrite hero to state who, what, why in 5 seconds; add proof [bc5a8130eee9] |
| Section reach | Scroll map checkpoints 75/50/25 | Key proof and CTA sit where most people reach | Reviews or add to cart reached by 25 to 30% | Move key items up [bc5a8130eee9] [edd07a1a15f6] |
| Sharp drop after copy | Scroll map section by section | Smooth decay | Steep drop right after one paragraph | Cut or restructure the copy; compare with normal end-of-page decay [edd07a1a15f6] |
| Clicks in empty space | Click map vs live page | Clicks sit on real controls | Clicks where nothing is | Investigate further in recordings [09583734387e] |
| Clicks on hero image | Click map | Few | Many clicks on an explanatory image | Hypothesis: value prop unclear; test a video or clearer explanation (SaaS demo example) [09583734387e] |
| Element that looks like a button | Area map | Low click share on static banners | High click share on a non-button (46% example) | Make it work or restyle it; confirm frustration in recordings and user tests [09583734387e] |
| Redundant elements | Area map | Every element earns clicks | Elements with very few clicks add visual weight | Consider removing; confirm in recordings [09583734387e] |
| Repeated scroll-back to a control | Collection recordings | Shoppers refine then keep browsing | Scroll down, back to top for filter, down again | Test a sticky or easy-to-reopen filter; check across several sessions and devices first [11e64288067b] |
| Form drop-off | Scroll map and recordings on form pages | Most people see and finish the form | 25% drop before the form; drop at 3rd or 4th field; drop at phone field | Remove big "Contact us" header, move form up, cut fields to 4 or fewer [none: text only] |

## 6. Tools, settings and named features

All `[verify UI]`. Interface as of July 2024.

- **Microsoft Clarity dashboard**: date range picker; top-line metrics (sessions, scroll depth, active time, pages per session); **Insights** block with rage clicks, dead clicks, excessive scrolling, quick backs, each with a camera icon linking to recordings; **Smart events** (funnel stages such as add to cart and checkout); channel, campaign, source, browser, device, popular pages. [e053644d5707]
- **Heatmaps tab**: list of most popular pages; **Change screenshot** button (top right) to pick another captured version of the page; device filter (desktop, tablet, mobile); map types **Clicks**, **Scroll** and **Area**. [09583734387e]
- **Area map**: **Edit areas** lets you draw custom regions and read each one's share of clicks. The presenter calls this his favourite Clarity feature. [09583734387e]
- **Scroll map**: shows reach per position, an "average fold" marker and checkpoint markers. [edd07a1a15f6]
- **Recordings tab**: list with time spent, source, device; **Filters** (time frame, device, user action, scroll depth, landing page, performance or speed, page duration); **Sort** (clicks and pages, high to low and low to high); **Skip inactivity** toggle; playback speed (1.5x, 4x used). [a1a3e1f62713]
- **Google Analytics**: named as better for funnels and the top-line metrics. Funnel setup lives in 06-MEA.
- **Surveys and user tests**: mentioned as ways to decide what content matters and to confirm frustration, no tool named. [bc5a8130eee9]

## 7. Examples and case results

All are examples from the presenter's clients or the demo account. None report a conversion result.

- **SaaS pricing page (audit report)**: many clicks around pricing elements, but only the "get X free credits" button was clickable. Classed as a harmful dead click because shoppers wanted the price. [0eae610ddc62]
- **Logo not clickable**: on one site, visitors clicked the centre logo from the checkout and product pages to get home. It did nothing, which raised dead clicks and caused rage clicks. Seen on dashboard, heatmap and recordings. [0eae610ddc62]
- **Clarity demo homepage**: clicks spread across nav, headline, body text and informational check marks (not clickable, "a potential area of enhancement"). Core CTA clicks 0.19% + 0.91% + 3.93%, read as about 4 to 5% total. Clicks in an empty part of the nav, and on the hero image. Hypothesis: add a video explaining the platform, because the headline "better your business" does not state the value prop. Scroll reach 96% then 87%, staying high. [09583734387e]
- **Delivery service client, Area map** (the recordings below name a CBD delivery company with the same on-demand and full menu, so likely the same client): on-demand menu 4% of clicks vs full menu 1.74%. A "your browsing" element that looked like a button but was a static banner got 46% of clicks (the transcript says this was about a thousand clicks; the word is garbled). User recordings and user tests showed people tried to switch menus there, got frustrated and left. Top nav 8.48% of clicks; sticky filter at bottom 5.58%. [09583734387e]
- **CBD delivery client, recordings**: a 1-hour mobile session showed a shopper scrolling down through products then all the way back up to reach the on-demand menu, because the filter was only at the top and not sticky. Found "in like 2 minutes". [11e64288067b]
- **CBD delivery client, cart wipe bug**: a shopper already at checkout switched from full menu to on-demand, which silently emptied the cart. The warning popup appeared only after the cart was removed. The shopper hit an empty category page, got stuck and left after 21 minutes. The presenter says it "had to get fixed straight away". [0b8d2f6cc4d1]
- **Product page with long text block**: 93% reach above the paragraph, then about a 30% drop right after it, then 60% falling to 25%, so only 25% reached add to cart. Conclusion: text too long, cut it down. [edd07a1a15f6]
- **B2B contact page**: a large "Contact" heading pushed the form below the fold. About 25% of visitors dropped off immediately and never saw the form. [bc5a8130eee9]
- **Form fields**: sites with 8 to 10 fields where most visitors stop by the 3rd or 4th. Asking for phone number causes "a substantial drop off". (Text only; no card.)

## 8. Mistakes the source warns about

- Relying on Clarity's top-line metrics that GA already gives, instead of the Insights and recordings. [e053644d5707]
- Acting on an Insight percentage without watching its recordings. [9d9871ee324b] [0eae610ddc62]
- Ignoring a real usability issue because its rate looks low. [5b9da7dd1967]
- Reading a heatmap captured behind a popup or broken layout without changing the screenshot. [09583734387e]
- Popups that fire in the first 5 seconds, and chat widgets that cover add to cart or submit. [9d9871ee324b]
- Making every clicked element a link. Press logos can stay static so shoppers do not leave. [0eae610ddc62]
- Non-clickable logos, banners that look like buttons, pricing blocks with 1 working button. [0eae610ddc62] [09583734387e]
- Hero that does not state who, what and why in 5 seconds. [bc5a8130eee9]
- Social proof and key info placed where only a minority scroll. [bc5a8130eee9]
- Long text blocks between the shopper and the add-to-cart button. [edd07a1a15f6]
- Filters that exist only at the top of a long product list. [11e64288067b]
- Wasting top-of-page space on "Contact us" or "Get started" headings on pages where the visitor already knows where they are. [bc5a8130eee9]
- Long forms, and asking for phone number when sales does not need it. (text only)
- Watching recordings with distractions, or without asking "why". [0b8d2f6cc4d1]
- Setting a fixed recording quota, or stopping review after one round. [0b8d2f6cc4d1]

## 9. Caveats, conflicts and what is missing

- **Dated interface.** Recorded July 2024 despite the 2026 title. All feature names and menu paths need `[verify UI]`.
- **Unsourced numbers.** The 60% no-scroll claim, 1 to 2% rage click benchmark and 5 to 7% CTA target have no stated study or sample. Treat them as presenter heuristics. `[needs brand data: own scroll reach and CTA click share by page and device]`
- **No results.** The source shows how problems were found, not whether fixing them lifted conversion. No sample sizes, no test durations, no significance.
- **No causal claims.** Heatmaps and recordings show behaviour, not cause. Cards add that a controlled test is needed before claiming revenue. [6d2e6fafa7df]
- **Engagement sorts can mislead.** Sorting by clicks or pages can reflect page complexity, not intent; long sessions can mean intent, confusion or idleness. [a1a3e1f62713] [0b8d2f6cc4d1]
- **Sticky filter is a proposed fix, not a tested one.** One return-to-top is not a pattern. [11e64288067b]
- **Long copy is not always bad.** Detailed products may need it; the problem is presentation that blocks scanning. [edd07a1a15f6]
- **Warm vs cold traffic.** The header mentions the difference; the transcript only covers cold traffic. No rule for warm traffic is given.
- **Mixed audience.** Many examples are SaaS or B2B. Ecommerce transfer is the card writers' adaptation.
- **Privacy, consent and install steps** for Clarity are not covered. `[web check: current Clarity install, consent and data retention terms]`
- **Conflict with source 07 (Hotjar vs Clarity)**: none. Both prefer Area maps. Source 07 adds the scroll-reach vs click-share test pattern.
- **Neighbours.** GA4 funnel setup: 06-MEA. Page redesign and copy changes from these findings: 07-LPG.

## 10. Card index

- e053644d5707bb7ba5507da1: Set up a Clarity review around ecommerce friction signals
- 9d9871ee324b9ac0cb55e4e2: Investigate rage clicks as blocked purchase actions or failed exits
- 0eae610ddc62a88491e01ab0: Classify dead clicks by whether the shopper expected a useful action
- 5b9da7dd19670be22eec374f: Use excessive scrolling and quick backs to find missing PDP information
- 09583734387ef245bda10295: Read click, scroll, and Area Maps against the page's core shopping action
- bc5a8130eee9118a83acf4b4: Move purchase-critical value and proof into the first viewport when maps show it is unseen
- edd07a1a15f691586b7e945e: Diagnose sharp scroll drop-offs after long product copy
- 0b8d2f6cc4d11e19b254690b: Run focused recording reviews until the purchase-path pattern is clear
- a1a3e1f6271379b44645e080: Compare engaged and disengaged sessions with Clarity sorts and filters
- 11e64288067ba073e53244fe: Fix collection controls that shoppers repeatedly scroll back to reach
- 6d2e6fafa7df9f658707accc: Turn Clarity evidence into a testable ecommerce hypothesis
