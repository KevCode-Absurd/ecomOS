# The BEST Conversion Rate Optimization Tutorial for Ecommerce (in 2025)

source_id: 1uPC993KlCT_DuV5jF-dGVTvPImMz7mfh  |  folder: /07-LPG-landing-pages  |  cards: 19  |  words: 8629  |  type: transcript (YouTube tutorial with screen share)
credibility: Solo presenter who names himself "Arsh" in the video. He runs a CRO agency (not named in the transcript) and says he has worked with "over 150 brands in over 80 different niches". He sells audits and agency services, and links a user testing template, a review mining checklist and a PXL spreadsheet in the video description (not in this document). Evidence: screen shares of 1 client's GA4, Microsoft Clarity and Userbrain data (an industrial or trade product store with "shop by industry" categories such as woodworking, agriculture and painting), plus 2 A/B test results from that client (18% and 64% conversion lifts) and 1 review mining example from a different product ("no spills or mess"). The funnel benchmarks and most thresholds are his own heuristics with no stated sample or source. No test durations, sample sizes or significance levels are given for any result.
date signals: The file title says "in 2025". GA4 metric names used are "user key event rate" and "session key event rate", so recorded after GA4 renamed conversions to key events (2024). Tools named: Google Analytics 4, Microsoft Clarity, Hotjar, Userbrain, Okendo (Shopify). Shopify checkout is described as "standardized". GA4 report paths and Clarity menus are the most time-sensitive parts. [verify UI]
transcript note: Several numbers lost their leading "0." in transcription. Read in context: mobile session conversion "84%" is almost certainly 0.84% (desktop is 1.4%); the "select options" button "86%" is likely 0.86%; the collection page "show" button "74%" is likely 0.74%; the "call an expert" button ".36%" / "36%" is 0.36%; "15,61" sessions is likely 15,601 (the presenter's own 15% calculation uses 15,601). "J4" and "G4" mean GA4. "Hot chart" means Hotjar. "Amy test" means A/B test.
scope note: The document header files this under LPG (landing pages and funnels) and points paid social buying to 06-MEA and email flows to 09-EML. Much of the method (GA4 audit, Clarity, surveys, PXL, hypothesis writing) overlaps 09-CRO-testing. This mini playbook keeps all of it.

## 1. What this source is for

It gives an operator a full CRO audit sequence for a Shopify-style store: find funnel leaks in GA4, see what users click and scroll in Clarity, learn why through surveys, user tests, review mining and recordings, then write hypotheses, score them with PXL and A/B test the top ones. It is strong on concrete GA4 report paths, Clarity area-map reading and page-element fixes on homepage, collection page and PDP. It is thin on test statistics, sample size, run length and how to build the variants. [7d3a4c37853c]

## 2. Principles

### 2.1 Process

1. **Analyse data before any optimization.** "You cannot optimize what you can't measure." Decisions on guesswork can lower conversion instead of raising it. Condition: applies before any page change; the card notes urgent fixes may still come before a full audit. Evidence: opinion from his audit practice. [7d3a4c37853c]
2. **Fix the worst funnel stage first, not everything at once.** Compare each step of the GA4 Purchase Journey to a benchmark band and focus on the stage furthest below it. "You cannot do everything at once." [f258739c8f9c]
3. **Quantitative data shows where and what; qualitative data shows why.** GA4 and heatmaps say where people click and drop. Surveys, interviews and user tests say why. [7d3a4c37853c] [bfbcb883a414]
4. **Qualitative research matters most at lower traffic.** Source says: under roughly 50,000 to 80,000 visitors a month, quantitative data "on its own is not going to give you a ton of data" and must be supplemented with qualitative feedback. Condition: his threshold, no basis given. [7d3a4c37853c] [75d6c6bbb420]
5. **Back each change with 2, 3 or 4 data points.** "We're not just talking about one data point, it's two, three, four pieces of data that supports our insight. That's true data-driven CRO." Example: the colour selector problem was seen in click maps (16.68% of PDP clicks) and in repeated session recordings. [63d3f8c37b06] [6f6f47a38de3]
6. **Validate with A/B tests, not by shipping.** A/B testing measures "in an objective controlled environment" whether version A beats version B. Every card turns a finding into a hypothesis and a test, not a live edit. Caveat from the cards: at low traffic some changes may have to ship on judgement with a rollback plan. [7d3a4c37853c] [bfbcb883a414]
7. **Primary goal of tests: raise motivation by clarifying the value proposition, and reduce fear, uncertainty and doubt (FUD) early in the journey.** Stated for his client's above-the-fold test. [6f6f47a38de3] [ac46f2bf0ebf]

### 2.2 Page design

8. **Heatmaps reduce to 1 question.** What are people clicking now, where do you want them to click, and how can the design move clicks to where you want them? Scroll maps: are people scrolling to where you want, how far do they get, and how should layout change so they see the priority information? [bfbcb883a414]
9. **Visual hierarchy follows click data.** If a small element (a product title at 3.2% of section clicks) earns more clicks than the bigger button, make it more prominent. Visual hierarchy is "the flow of information from top to bottom". [bfbcb883a414]
10. **Remove false affordances.** Elements styled like buttons (a grey border on "featured on" logos) draw clicks but go nowhere. Remove the button look or make them real links. [bfbcb883a414]
11. **Remove clutter that nobody clicks.** Clickable elements with near-zero click share (wishlist 0.09%, "call an expert" 0.36%, "show" filter button 0.74%) are removal candidates. "Remove clutter, remove things that people aren't clicking on, and just simplify the whole experience." Card caveat: low clicks do not always mean low value (sizing, returns and support content can prevent costly problems). [c6a46a3c8964] [88fb8838882b]
12. **Lead with social proof above the fold.** "Based on the principles of any high converting site, we always want to lead with social proof above the fold." Stated as a general principle; his only evidence is a scroll map where just 32% reached a logo strip. [ac46f2bf0ebf]
13. **Show as many products as possible up front on collection pages.** "A common theme that we follow when we build any collection page." Consolidate above-the-fold content so products appear earlier. [e03f2284af5e]
14. **Put FUD reducers where users drop off.** On long collection pages, place free shipping or money-back guarantee messages between product rows at the steepest drop-off points. Source says "we've AB tested this a lot and seen really big increases in conversions" but gives no numbers. [e03f2284af5e]
15. **More and better images sell.** "People buy when they look at images." The more images of the product, in use and in lifestyle shots, the more likely they buy "as a general statement". So expose thumbnails instead of tiny pagination dots. [c6a46a3c8964]
16. **Keep cause and effect close together on the PDP.** If a control (colour swatch) changes something far away (main image), users scroll up and down. Move the control near what it changes. [63d3f8c37b06] [c6a46a3c8964]
17. **One or two filter layers at most.** "There's no need for like three to four levels or layers of filtration. There's probably just a need for one or two max." Use clear filter labels. Condition: his client had a small-to-mid catalogue; card caveat says a large catalogue may need more facets. [88fb8838882b]

### 2.3 Funnel interpretation

18. **Low View Product rate means a discoverability problem.** People cannot find the right products; navigation does not funnel them. Source says View Product rate is the weakest stage in "90 to 95%" of brands he audits, so check it first. [f258739c8f9c]
19. **Low Purchase rate on Shopify is usually unexpected costs.** "Within Shopify, there's not a ton you can do because it's kind of a standardized checkout." Low purchase rate is "usually derived because of unexpected shipping cost or unexpected cost." [f258739c8f9c]
20. **A big mobile-versus-desktop gap means desktop exposes something mobile hides.** Form hypotheses about what that element is, then find it with heatmaps and recordings. [50b30a244eb6]
21. **Same product, different conversion by entry path is a clue.** Ask whether the better path sets the visitor up better (context, pre-selling). Card caveat: the difference may be traffic source, not page quality. [8f90616b8da5]

## 3. Procedures

### 3.1 Full audit sequence (order the source follows)

1. GA4 Purchase Journey (funnel benchmarks). 2. GA4 Path Exploration (forward from homepage). 3. GA4 Path Exploration (backward from Add to Cart). 4. GA4 Tech Overview by device. 5. GA4 Landing Pages. 6. Clarity heatmaps and scroll maps on homepage, collection page, PDP. 7. Post-purchase survey. 8. Mid-session product friction survey. 9. Userbrain user tests. 10. Review mining. 11. Clarity session recordings. 12. Write hypotheses with rationale and KPIs. 13. Score with PXL. 14. A/B test the top scores. 15. Re-run user tests after changes. [7d3a4c37853c]

### 3.2 GA4 Purchase Journey benchmark [verify UI]

1. Reports (left side) > Monetization > Purchase journey.
2. Set a date range with enough data. Source uses the last 12 months.
3. Read the step rates: session start > view product > add to cart > begin checkout > purchase.
4. Compare each rate to the benchmark bands in section 4.
5. Note the stage furthest below its band as the focus. Note smaller gaps as secondary.
6. Check that GA4 events map to the steps you expect (card caveat). [needs brand data: GA4 purchase journey rates for the last 6 to 12 months] [f258739c8f9c]

### 3.3 GA4 Path Exploration, forward from the homepage [verify UI]

1. Explore > Path exploration. Date range last 12 months.
2. Click the node type "Event name" and switch it to "Page path and screen class" so each node is a page.
3. Expand the homepage node. Note which collection pages get the traffic (example: 15,601 and 12,968 sessions).
4. Expand those collection pages. Look for returns to the homepage (example: 2,416 back to homepage).
5. Expand again to find loops (example: 310 back to the same collection page).
6. GA4 does not show percentages here. Compute by hand: returning ÷ originating × 100 (example: 2,416 ÷ 15,601 × 100 = about 15%). Do this in code or a sheet, not by eye.
7. Read loops (homepage > collection > homepage > collection) as a navigation or findability problem. Log it for testing and pair with qualitative data. [cbe719818c7a]

### 3.4 GA4 Path Exploration, backward from Add to Cart [verify UI]

1. In Path exploration click "Start over", then choose to start from the endpoint.
2. Set the endpoint node to Event name > add_to_cart.
3. Switch preceding nodes to Page path and screen class.
4. Expand the top node. Note which pages produce add to carts and how users reached them (example: 429 add to carts direct from 1 PDP; 321 from the same PDP reached via a collection page).
5. If many add to carts come after collection > PDP, hypothesise a quick add to cart on the collection page. Put it in the test backlog. [63a914e978db]

### 3.5 GA4 Tech Overview by device [verify UI]

1. Reports > Technology > Tech overview. Date range 6 or 12 months depending on data volume.
2. Scroll to the device category chart (example: about 80% mobile, 20% desktop). Click "View device categories".
3. Customize report (top right). Remove metrics you do not need. Add: user key event rate, session key event rate, bounce rate, average engagement time per session, average purchase revenue (AOV), average purchase revenue per active user (revenue per visitor, RPV). Apply.
4. Filter the key event columns to purchase so they show purchase conversion. Labels may differ with your GA4 setup.
5. Look at session conversion rate first (the "industry standard"), but check user conversion too. A user is 1 unique person; 1 person visiting 5 times is 5 sessions.
6. Look for anomalies between devices in conversion, RPV, bounce and engagement time. Note them for heatmap and recording follow-up. [needs brand data: device split of sessions, conversion, AOV, RPV] [50b30a244eb6]

### 3.6 GA4 Landing Pages report [verify UI]

1. Reports > Engagement > Landing page.
2. Metrics (top right): keep bounce rate, average session duration, session key event rate, user key event rate, views per session. Apply.
3. Filter key events to purchase.
4. Review the top 5 to 10 pages by traffic only.
5. Flag anomalies: short engagement on a high-traffic PDP (example 44 seconds versus about 1 minute 2 seconds on the homepage; source wants about 1 minute); the same product converting differently by entry URL (example 1.53% via homepage URL versus 1.29% via /collections/.../products URL).
6. Write the "why" question for each anomaly for later research. [8f90616b8da5]

### 3.7 Clarity heatmap area-map reading [verify UI]

1. Clarity > Heatmaps. Start with the most viewed page (usually homepage), then collection page, then PDP.
2. Switch from Clicks to Area. Click "Edit areas" and draw an area per element (image, title, button, price, reviews, each category tile, each filter control, thumbnails, swatches, wishlist).
3. Record each element's click share.
4. For each element ask: getting clicks but not clickable (false affordance)? Clickable but near zero clicks (clutter)? Heavily clicked but small or low on the page (promote it)?
5. Switch to Scroll. Read the 75%, average fold, 50% and 25% checkpoints. Note where priority content sits relative to reach.
6. Cross-check high-click sections against scroll reach. A section with high clicks but low reach should be surfaced higher.
7. Turn each finding into a hypothesis. Clarity sometimes fails to load images in the editor, so areas can be hard to place. [bfbcb883a414] [c7160f33c310]

### 3.8 Homepage category blocks

1. Area-map each category block. Record click share (example: woodworking 1.06%, second block 9%, sixth block 1.92%).
2. Reorder so the highest-click categories come first.
3. Check scroll reach for the section (example: only 25% reached it although it had some of the most clicks on the page).
4. If reach is low, add entry points near the top: small clickable category thumbnails styled like Instagram story icons, linking to the same collection pages.
5. A/B test it. Example result: +18% conversion rate for that client. [c7160f33c310]

### 3.9 Collection page filters

1. Area-map every filter, sort, view-as and sidebar control (example: "view as" 6.07%, "sidebar" 3.14%, "show" 0.74%).
2. Flag controls near or under 1% for removal (card threshold).
3. Confirm with user testing which control users want. In the example users wanted the sidebar filter; they clicked "show" and "sort by" while hunting for it.
4. Cut to 1 or 2 filter layers. Remove the weak control rather than restyle it (example: removed "show").
5. Rename controls in user language (example: "sidebar" renamed to "sort and filter").
6. A/B test and watch filter use and conversion. [88fb8838882b]

### 3.10 Collection page scroll and product order

1. Read scroll reach at each product row (example: 88% at the first 2 products, then 75%, 66%, 57%; about 10% lost per 2 products).
2. If many users never reach the first row's buttons (example: about 20% never reached "select options"), consolidate the above-the-fold content so products show higher.
3. Put the products you most want seen in the highest-reach rows. [needs brand data: best-converting and highest-margin products]
4. Insert FUD reducers (free shipping, money-back guarantee) between rows where drop-off is steepest.
5. A/B test the new layout. [e03f2284af5e]

### 3.11 PDP click and scroll fixes

1. Area-map the top PDPs.
2. Image pagination dots with a high share (example 7.35%, among the most clicked): replace with real, clickable image thumbnails. Test.
3. Colour selector with a high share (example 16.68%; the whole options area 21%): move colour higher, near the main image, since picking a colour swaps the image. Test.
4. Record the add to cart and upsell shares (example: upsells 1.74%, add to cart 1.42%) as context.
5. Remove near-zero elements (example: wishlist 0.09% removed; "call an expert" phone button 0.36% removed and run as an above-the-fold test).
6. Scroll map: if the main image pushes content down (example: 25% leave before the description) and a long description hides the button (example: only 36% reach add to cart, about 70% never do), shorten the description, shrink above-the-fold elements and remove empty white space.
7. Test changes separately where traffic allows (card). [c6a46a3c8964]

### 3.12 Post-purchase survey

1. Show it immediately after purchase. No incentive needed per source.
2. Q1: "What motivated you to buy from us today?" Multiple choice or open-ended. With less data, leave it open-ended.
3. Q2: "Did you have any concerns, doubts or uncertainties that almost stopped you from buying today?"
4. Group answers into themes (example themes: fit, sizing, plain-language vocabulary) and count them.
5. Feed top themes into PDP copy, size guides, FAQs, benefit bars and tests. [3b5634f1c703]

### 3.13 Mid-session product friction survey

1. Find average session duration. [needs brand data: average session duration]
2. Trigger the survey at about 60% of it (example: 2 minute sessions, fire at about 1 minute; note 60% of 2 minutes is 72 seconds, the source rounds to "around the 1 minute mark").
3. Q1 (yes/no): "Is there anything holding you back from buying this product right now?"
4. If yes: "What is the reason holding you back?" Use preset reasons plus "something else"; only "something else" opens a free text box (how the source set it for the client).
5. Tool: Okendo on Shopify, which has surveys and preset question templates. Source uses it for all clients. [verify UI] [web check: Okendo survey features and plan requirements]
6. Route themes into the test backlog. Watch conversion while it runs (card caveat). [0d65f4f7da9f]

### 3.14 User testing with Userbrain [verify UI]

1. Userbrain > Get testers. Filter by device type, country, age range and gender.
2. Add screening questions to exclude people outside the target market.
3. Ask for first impressions on landing, then set tasks tied to what matters for the brand (for example find a product and add to cart). Testers speak their thoughts aloud. Source example session ran 22 minutes.
4. Run 3 to 5 tests.
5. Log each hesitation, navigation failure and doubt. Convert to hypotheses.
6. Re-run the same tests after changes for a before-and-after view.
7. Source's user testing template is linked in the video description, not in this document. [75d6c6bbb420]

### 3.15 Review mining

1. Export reviews from every source: own site, Google, Trustpilot, Amazon.
2. Put them in 1 spreadsheet with what the customer said.
3. Tag each review by main topic (the most important field) and by motivation, value or anxiety, plus further tags from his checklist (not included in this document).
4. Pivot to count the most frequent topics, separately for positive and negative reviews.
5. Feed top topics into copy, design and A/B tests (example top topics: fun and social settings, easy to use, product satisfaction, no spills or mess). [1f3ae96ccb10]

### 3.16 Clarity session recordings [verify UI]

1. Clarity > Recordings. Sort by clicks high to low, or pages high to low.
2. Note device and country per recording.
3. Watch for patterns repeated across several recordings (example: user picks a colour low on the PDP, scrolls to the top image to see it, scrolls back down, repeats).
4. Turn the pattern into a layout hypothesis (bring colour closer to the product image). Combine with click-map data. [63d3f8c37b06]

### 3.17 Hypothesis, prioritisation, test

1. For each idea write: rationale (2 to 4 data points), primary goal, KPIs. Example KPIs: view product rate and conversion rate.
2. Hypothesis form: "If we do X, we will generate more [KPI] because [rationale]."
3. Example: "By having a clear value prop, introducing social proof and improving visual hierarchy of the above the fold section, this will increase the motivation for users to shop on product pages and therefore increase conversions."
4. List all ideas (often 100+ after an audit) in the PXL sheet and score them (section 4).
5. Total the scores. Run the highest totals first.
6. A/B test. Cards add: set the measurement window and success threshold before launch; the source does not. [6f6f47a38de3] [1bedb6cc7753]

### 3.18 Above-the-fold redesign (source's winning test)

1. One clear value proposition.
2. A primary button that stands out from everything around it.
3. Clear messaging; remove competing elements.
4. A benefits bar with shipping terms and 30-day free returns to reduce FUD.
5. Products shown above the fold.
6. Social proof high on the page.
7. Before-and-after A/B test. Example: +64% conversion rate, +52% RPV for that client. [ac46f2bf0ebf]

## 4. Rules, thresholds and numbers

| rule | number or threshold | condition | source's basis | card id |
|---|---|---|---|---|
| View product rate benchmark | 50 to 70% | GA4 Purchase Journey, sessions viewing a product | presenter heuristic, "industry benchmark" | f258739c8f9c |
| Add to cart rate benchmark | 12 to 20% | GA4 Purchase Journey | presenter heuristic | f258739c8f9c |
| Begin checkout rate benchmark | 40 to 60% | GA4 Purchase Journey | presenter heuristic | f258739c8f9c |
| Purchase rate benchmark | 45 to 60% | GA4 Purchase Journey | presenter heuristic | f258739c8f9c |
| View product is the weakest stage | in 90 to 95% of audited brands | his audits | own agency experience | f258739c8f9c |
| Data window for GA4 reports | 12 months (funnel, paths); 6 or 12 months (tech overview) | enough data to be reliable | presenter choice | f258739c8f9c, 50b30a244eb6 |
| Landing page review scope | top 5 to 10 pages | by traffic | presenter practice | 8f90616b8da5 |
| PDP engagement target | about 1 minute | PDP average engagement per session | his judgement vs 44 s example | 8f90616b8da5 |
| Drop-off after hero | about 60% never scroll past the hero | homepages he "normally" sees | own audits | bfbcb883a414 |
| Collection scroll decay | about 10% lost per 2 products | 1 client example, not a benchmark | 1 case | e03f2284af5e |
| Filter layers | 1 or 2 max, not 3 or 4 | collection pages | opinion from 1 case | 88fb8838882b |
| Filter removal candidate | under roughly 1% click share | per control | card threshold from 0.74% example | 88fb8838882b |
| Qualitative research becomes essential | under roughly 50,000 to 80,000 monthly visitors | low traffic | opinion | 7d3a4c37853c |
| User tests | 3 to 5 testers | enough to find most usability issues | presenter recommendation | 75d6c6bbb420 |
| Post-purchase survey completion | 85 to 90%, no incentive | shown right after purchase | his clients | 3b5634f1c703 |
| Mid-session survey trigger | about 60% of average session duration | PDP or active shopper | presenter rule | 0d65f4f7da9f |
| Rationale strength | 2 to 4 supporting data points per change | every hypothesis | presenter definition of data-driven | 6f6f47a38de3 |
| Backlog size after audit | often 100+ ideas | full audit | presenter experience | 1bedb6cc7753 |
| PXL: above the fold | 1 yes / 0 no | per idea | presenter sheet | 1bedb6cc7753 |
| PXL: noticeable within 5 seconds | 2 very noticeable / 0 not | per idea | presenter sheet | 1bedb6cc7753 |
| PXL: adding or removing an element | 2 / 0 (transcript: "adding a significant element, it's zero"; card reads 2 for removing) | per idea | presenter sheet, garbled in transcript | 1bedb6cc7753 |
| PXL: designed to increase user motivation | 1 / 0 | per idea | presenter sheet | 1bedb6cc7753 |
| PXL: running on a high traffic page | 1 / 0 | per idea | presenter sheet | 1bedb6cc7753 |
| PXL: addresses an issue found in user testing | 1 / 0 | per idea | presenter sheet | 1bedb6cc7753 |
| PXL: supported by heatmaps or eye tracking | 1 / 0 | per idea | presenter sheet | 1bedb6cc7753 |
| PXL: ease of implementation | scored, scale not stated | per idea | presenter sheet | 1bedb6cc7753 |
| PXL decision | run highest totals first | whole backlog | presenter rule | 1bedb6cc7753 |

## 5. Diagnostics and checks

| what to check | how | good | bad | next step | card |
|---|---|---|---|---|---|
| Funnel step rates | GA4 Purchase Journey, 12 months | inside the section 4 bands | below band (example: view product 28.6%, add to cart 9.9%, purchase 36.1%) | focus on the stage furthest below; view product first in most stores | f258739c8f9c |
| Low view product rate | Path exploration, heatmaps, user tests | users reach PDPs from home and collections | loops home > collection > home; high-click categories low on page | fix navigation, category order, surface categories near top, show products above the fold | cbe719818c7a, c7160f33c310 |
| Low purchase rate on Shopify | review shipping and extra costs shown before checkout | costs clear early | surprise shipping or fees | show costs earlier; source gives no further steps | f258739c8f9c |
| Navigation loops | Path exploration, hand-computed % | low return share | about 15% collection > home > collection (example) | test navigation, filters, category labels | cbe719818c7a |
| Add to cart paths | Path exploration from add_to_cart endpoint | direct, short paths | many add to carts need collection > PDP | test quick add on collection page | 63a914e978db |
| Device gap | Tech overview, custom metrics | similar RPV and conversion by device | desktop RPV about 2x mobile ($4.13 desktop, example); desktop conversion 1.4% vs mobile about 0.84% | find what desktop shows that mobile hides, via heatmaps and recordings | 50b30a244eb6 |
| Top landing pages | Landing page report, top 5 to 10 | PDP engagement near 1 minute | 44 s on a top PDP; same product converting 1.53% vs 1.29% by URL | investigate why; test copying the better path's context | 8f90616b8da5 |
| Click vs intent | Clarity area maps | priority elements get the clicks | clicked non-links; unclicked links; small elements with big click share | remove false affordance, remove clutter, promote clicked elements | bfbcb883a414 |
| Social proof reach | Clarity scroll map | social proof in the first screen | only 32% reach the logo strip | move it up | ac46f2bf0ebf |
| Collection first row reach | scroll map | nearly all users see the first products | about 20% never reach first row buttons | consolidate above-the-fold content | e03f2284af5e |
| PDP buy button reach | scroll map | most users reach add to cart | 36% reach it | shorten description, shrink hero elements, remove white space | c6a46a3c8964 |
| Hidden images | area map on thumbnails | thumbnails visible and clickable | dots take 7.35% of clicks | show real thumbnails | c6a46a3c8964 |
| Control far from its effect | recordings sorted by clicks | no back-and-forth scrolling | repeated colour > scroll up > scroll down | move the control near the image | 63d3f8c37b06 |
| Why buyers nearly left | post-purchase survey Q2 | few, known themes | recurring fit, sizing, vocabulary doubts | answer them in copy, size guide, FAQ, benefit bar | 3b5634f1c703 |
| Why shoppers stall now | mid-session survey | few "yes" answers | recurring reasons | add to backlog; watch that the survey itself does not cut conversion | 0d65f4f7da9f |
| Usability and trust | 3 to 5 Userbrain tests | tasks done without hesitation | navigation and filter trouble, low confidence in site or product (example) | hypotheses, then re-test after changes | 75d6c6bbb420 |

## 6. Tools, settings and named features

- **Google Analytics 4**: Purchase journey (Reports > Monetization), Path exploration (Explore), Tech overview (Reports > Technology), Landing page (Reports > Engagement). Metrics: user key event rate, session key event rate, bounce rate, average engagement time per session, average session duration, views per session, average purchase revenue (AOV), average purchase revenue per active user (RPV). Path exploration does not compute percentages. [verify UI] [f258739c8f9c] [cbe719818c7a] [50b30a244eb6] [8f90616b8da5]
- **Microsoft Clarity** (or Hotjar): heatmaps with Clicks, Area ("Edit areas") and Scroll views; scroll checkpoints 75%, average fold, 50%, 25%; Recordings sorted by clicks or pages high to low, with device and country shown. Source skips the main dashboard as it overlaps GA4. Images sometimes fail to render in the heatmap view. [verify UI] [bfbcb883a414] [63d3f8c37b06]
- **Okendo** (Shopify): surveys with preset questions and templates; used for both surveys. [verify UI] [web check: current Okendo survey product and pricing] [0d65f4f7da9f]
- **Userbrain**: recruited testers, "Get testers", filters for device, country, age range, gender, screening questions, recorded think-aloud sessions. [verify UI] [web check: Userbrain current features and pricing] [75d6c6bbb420]
- **Spreadsheet templates** from the presenter (user testing template, review mining checklist and pivot, PXL sheet): linked in the video description, not in this document. [web check: presenter's PXL template criteria] [1bedb6cc7753] [1f3ae96ccb10]
- **PXL framework**: named by the presenter as his prioritisation framework. He does not credit its origin. [web check: original PXL criteria and scoring, likely CXL] [1bedb6cc7753]

## 7. Examples and case results

All from 1 client store (trade or industrial products, about 80% mobile) unless noted. Examples, not promises.

- Funnel: view product 28.6% (band 50 to 70%), add to cart 9.9% (12 to 20%), begin checkout 50.3% (40 to 60%, fine), purchase 36.1% (45 to 60%). [f258739c8f9c]
- Paths: 199,830 homepage sessions; 15,601 and 12,968 to 2 collection pages; 2,416 back to homepage (about 15%); 310 back again to the collection. [cbe719818c7a]
- Add to cart paths: 429 direct from 1 PDP; 321 from the same PDP via a collection. Led to a quick-add idea. [63a914e978db]
- Device: desktop session conversion 1.4% vs mobile about 0.84%; desktop RPV $4.13, about 2x mobile; desktop bounce 7% higher and desktop sessions longer. [50b30a244eb6]
- Landing pages: top PDP 44 s engagement vs homepage 1 min 2 s; same product 1.53% (homepage URL) vs 1.29% (collection URL). [8f90616b8da5]
- Homepage section: image 75% of section clicks, title 3.2%, select options about 0.86%, price and reviews 0. Hypothesis: bigger title font. [bfbcb883a414]
- "Featured on" logos with grey borders got clicks but linked nowhere; only 32% of users reached them. [bfbcb883a414] [ac46f2bf0ebf]
- Category tiles: woodworking 1.06%, second tile 9%, sixth tile 1.92%; section reached by 25%. Category thumbnails added at the top: **+18% conversion rate** in an A/B test. [c7160f33c310]
- Homepage product rows: about 25% drop after the first 2 products, which he calls "pretty good" against the usual 60% drop after the hero. [bfbcb883a414]
- Collection filters: view as 6.07%, sidebar 3.14%, show 0.74%. User tests showed users wanted the sidebar filter. Removed "show", renamed "sidebar" to "sort and filter". No result given. [88fb8838882b]
- Collection scroll: 88%, 75%, 66%, 57% reach per pair of products. [e03f2284af5e]
- PDP: thumbnail dots 7.35%; options area 21% (colour 16.68%, upsells 1.74%, add to cart 1.42%); wishlist 0.09% (removed); call an expert 0.36% (removed, tested above the fold); 25% leave before the description; 36% reach add to cart. [c6a46a3c8964]
- Post-purchase survey: concerns about fit, sizing, vocabulary. 85 to 90% completion. [3b5634f1c703]
- User tests: navigation, filtering and low confidence in site and product. 1 recording ran 22 minutes. [75d6c6bbb420]
- Review mining (a different product): top topics fun and social settings, easy to use, product satisfaction, no spills or mess. [1f3ae96ccb10]
- Above-the-fold redesign (clear value prop, standout button, benefits bar with shipping and 30-day free returns, products above the fold): **+64% conversion rate, +52% RPV**. Many changes in 1 variant. [ac46f2bf0ebf] [6f6f47a38de3]
- Closing plug: "11 tricks" that "can generate 80% more revenue". Promotional, no data; ignore. 

## 8. Mistakes the source warns about

1. Optimizing on guesswork; it can lower conversion. [7d3a4c37853c]
2. Trying to fix every funnel stage at once. [f258739c8f9c]
3. Relying on quantitative data alone, especially on lower traffic. [7d3a4c37853c]
4. Over-complicating heatmaps. [bfbcb883a414]
5. Styling non-links like buttons (false affordance). [bfbcb883a414]
6. Keeping small, hard-to-see elements that users click most (small titles, image dots). [bfbcb883a414] [c6a46a3c8964]
7. Putting high-demand categories and social proof where few users scroll. [c7160f33c310] [ac46f2bf0ebf]
8. 3 to 4 layers of filters and confusing, overlapping labels ("sidebar", "show", "sort by"). [88fb8838882b]
9. Too much above-the-fold content on collection pages, so products appear late. [e03f2284af5e]
10. Big images and long descriptions that push add to cart out of reach. [c6a46a3c8964]
11. Clutter: wishlist and phone buttons nobody uses. [c6a46a3c8964]
12. Placing a control far from the thing it changes. [63d3f8c37b06]
13. Acting on 1 data point. [6f6f47a38de3]

## 9. Caveats, conflicts and what is missing

- **Benchmarks are unsourced.** The 4 funnel bands are called "industry benchmarks" with no source or sample. They will differ by niche, price and traffic mix, and depend on GA4 event setup. [web check: current ecommerce funnel benchmarks by vertical] [f258739c8f9c]
- **Checkout claim conflicts with common advice.** He says there is "not a ton you can do" on the Shopify checkout. Much ecommerce advice treats checkout (express pay, shipping thresholds, trust near payment, cost display) as a lever. His own fix hint (show shipping costs early) happens before checkout. [web check: current Shopify checkout customization options]
- **The winning test broke 1-change-per-test.** The +64% redesign bundled value prop, button, benefits bar, social proof and products. The card notes this makes attribution impossible. Common testing advice is to isolate changes, or accept that a bundle proves the package, not each part. [6f6f47a38de3]
- **No test statistics.** No sample size, run time, significance, or traffic per variant for the 18% and 64% results. No guidance on what to do when traffic is too low to test, beyond the card's "ship on judgement with rollback". [7d3a4c37853c]
- **Survey completion claim is high.** 85 to 90% post-purchase completion is his client figure; many sources report lower rates. [web check: typical post-purchase survey response rates] The cards also note post-purchase answers miss non-buyers, and a mid-session pop-up can itself suppress conversion. [3b5634f1c703] [0d65f4f7da9f]
- **PXL list is incomplete in the transcript.** "Same with this. Same with this" skips named criteria; the scoring of "adding or removing an element" and "ease of implementation" is garbled. Do not standardise on the card's version without the actual sheet. [1bedb6cc7753]
- **Removing low-click elements.** Near-zero clicks does not prove no value (a wishlist may serve returning visitors; a phone button may reassure without clicks). The source removed both; it gives no measured result for those removals. [c6a46a3c8964]
- **Filter rule is from 1 small-catalogue case.** Large catalogues may need more facets. [88fb8838882b]
- **Device diagnosis stops at the gap.** He says he will "come back to" the desktop versus mobile finding but never does; no mobile fix is given. [50b30a244eb6]
- **Entry-path conversion gap** may reflect traffic source, not page quality. [8f90616b8da5]
- **Review mining**: the motivation, value, anxiety definitions and extra tags are in a checklist not included. Amazon reviews may describe another seller's shipping or packaging. [1f3ae96ccb10]
- **Social proof above the fold** is stated as a universal principle from 1 scroll map. Card caveat: above-the-fold space is finite. [ac46f2bf0ebf]
- **Tracking accuracy**: he assumes GA4 is set up correctly and says labels may differ. Check purchase events before trusting any rate. [needs brand data: GA4 event setup audit]
- **Brand fit**: all numbers come from 1 trade-goods store. For any brand, rerun each report on its own data before acting. [needs brand data: GA4, Clarity, surveys, reviews]

## 10. Card index

- f258739c8f9c GA4 Purchase Journey Funnel Audit and Benchmarks
- cbe719818c7a Path Exploration for Navigation Loop Detection
- 63a914e978db Reverse-Path Analysis Around Add to Cart
- 50b30a244eb6 Segment Conversion Rate, AOV and RPV by Device
- 8f90616b8da5 Landing Page Report Anomaly Scan
- bfbcb883a414 Simplify Heatmap Reading to Clicks Versus Intent
- c7160f33c310 Reorder Category Sections Using Click Data and Scroll Reach
- 88fb8838882b Consolidate Collection Page Filters Using Click Share
- e03f2284af5e Place Products and Risk-Reducers by Collection Scroll Data
- c6a46a3c8964 Expose Image Thumbnails and Cut Dead PDP Controls
- 3b5634f1c703 Post-Purchase Survey: What Almost Stopped You
- 0d65f4f7da9f Mid-Session Friction Survey at 60% of Session Duration
- 75d6c6bbb420 Small-Sample User Testing with Userbrain
- 1f3ae96ccb10 Review Mining into Motivations, Value and Anxieties
- 63d3f8c37b06 Mine Session Recordings for Friction Patterns
- 6f6f47a38de3 Write Test Hypotheses in If-Then-Because Form
- 1bedb6cc7753 PXL Prioritisation Scoring for the Test Backlog
- ac46f2bf0ebf Priorities for an Above-the-Fold Redesign
- 7d3a4c37853c Storytelling That Moves Quant to Qual to Hypothesis to Test
