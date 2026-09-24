# 2026 Klaviyo Email Marketing Full Course (3+ Hours)

source_id: 1grdlATLu0lJAmHQTZ_0MyExN3jVkt8xi  |  folder: /14-EML-email-lifecycle  |  cards: 82  |  words: 49,414  |  type: course (single long YouTube screen-share walkthrough, auto-transcribed)

credibility: The presenter runs Dispatch ("the Dispatch agency"), an email and SMS agency for DTC brands. He uses "Elliot at Dispatch" as his example sender name, so the presenter is probably Elliot. Claims: set up email for "more than 30" 7 and 8-figure brands in about 3 years (transcript reads "37 and 8 figureure brands"; later "over 30 clients"); emails "directly attributable" to more than $50M in revenue; "hundreds and hundreds" of pop-up form A/B tests and "hundreds" of campaign and welcome A/B tests. Evidence is the agency's own client accounts shown on screen (Klaviyo reports, form tests, one client's business review), client email designs, and opinion. No test sizes, no confidence intervals, no controlled comparisons are shown. Revenue is Klaviyo-attributed, not incremental. He sells agency services, a weekly newsletter and a free checklist document. He openly says he is weak at paid ads, organic social and SEO. Strong commercial interest in "use Klaviyo" and "design in Figma" (the agency's service).
date signals: Title says 2026, but the body says "in 2025" several times and compares "May to April of 2025". A July 4th inbox tour dates filming to early July 2025. Names: Klaviyo (transcribed "Clavio", "Claio"), Shopify app embed, Entri DNS integration ("Entry", described as brand new), Klaviyo brand voice AI, logic builder for show/hide blocks, campaign sequence builder with one-click follow-up resend, the "go to inbox" form button, predictive analytics, deliverability tab and score, 187 live integrations, Gmail and Yahoo sender rules, iOS 15 Apple Mail Privacy Protection. Klaviyo menus, defaults and limits in this file can have changed. `[web check: current Klaviyo UI, defaults and limits before following any step]`
transcript note: Auto-transcription errors. "Clavio", "Claio", "Clavia" = Klaviyo. "Demark", "DMARK" = DMARC. "TKIM" = DKIM. "Entry" = Entri. "Gorgeous" = Gorgias. "Skios" = Skio. "YPO" = Yotpo. "Revo", "Repo" = a loyalty app, probably Rivo. "zeroarty" = zero-party. "flyyou" = flyout. "3,65" = 365. "aband" = abandoned. "Guist/Gist" = Geist font; "Tacoma" = Tahoma. "Evan Healey" = Evan Healy. "Absolute" = Absolut. "Duncan" = Dunkin. "DTOC" = DTC. Brand names in the inbox tour ("Regent Row", "R Porter") are kept as transcribed.
header note: The export starts with a folder note, a "Look for / Skip" block and a topic summary. That block is filing metadata, not the presenter. Several claims appear only there (3 to 4 campaigns a week, 2 welcome emails on day 0 in a 72-hour window, 14/30/60/90-day engagement tiers, 8% to 12% form target, 7 campaign content buckets, 91 campaign ideas, Gmail AI inbox, gamification). The body does not say them. Cards e6ffa2358b86 and 838c953697bd repeat some of them. See section 9.

## 1. What this source is for

A full build and run guide for Klaviyo on a Shopify store. It covers account settings, attribution and reporting hygiene, domain authentication, lists and engaged segments, a 4-step pop-up form, the 7 core flows (welcome, abandoned checkout, abandoned cart, browse abandonment, post-purchase, win-back, sunset), campaign cadence and campaign types, copy and design rules, a monthly analytics and deliverability review, A/B testing, dynamic content, predictive analytics, multichannel flows and integrations. It is strongest on exact Klaviyo settings, flow triggers and filters, and the monthly review routine. It is weakest on proof: every number is from the agency's own accounts or Klaviyo's recommended values.

## 2. Principles

1. **Email should drive at least 30% of total store revenue.** Source says 30% of all Shopify revenue, not 30% of marketing revenue. It lowers CAC (paid visitors become subscribers you convert later), raises LTV (engineered repeat orders), and builds an owned audience not exposed to Meta, Google or TikTok CPMs and algorithms. Presenter's heuristic from agency work, not a published statistic. The figure depends on the attribution window. [465d3381b2a7] `[needs brand data: email-attributed share of total revenue, attribution window in use]`
2. **Map the customer journey before building anything.** Journey: first visit from an ad or organic post, pop-up, first flow emails (welcome or abandoned cart), campaigns at least once a week, first order, post-purchase messages that drive the next order. Each touchpoint must match what the person already knows. The pop-up offer must match the ad or content they came from. Failure example: a first-order discount sent to someone with 5 orders. Qualitative discipline, not a model. [a084662e8ae4]
3. **Flows and campaigns do different jobs and must be coordinated.** Flows are behaviour-triggered and drive LTV. Campaigns are manual one-off sends for time-sensitive moments (sale, launch, seasonal content, new blog post). If you send the same campaign every week, month or day, it should be a flow. Audited brands with high unsubscribe and spam rates often sent a campaign plus welcome, abandoned cart and post-purchase emails to the same person within 24 hours. Anecdotal. [24b8079fe1fe]
4. **Metrics (events) are the automation engine.** Klaviyo metrics (received, opened, clicked, unsubscribed, marked as spam, dropped), Shopify metrics (ordered product, placed order, fulfilled order, refunded order, checkout started, cancelled order) and API or integration events. They trigger flows and act as filters. A broken integration throws no error; flows simply stop. [059f73755fa8]
5. **The profile is the single richest customer record.** Subscription status, form used, coupons, custom properties (source, prospect vs repeat, Shopify tags, loyalty points), location, events, predictive fields. Any data you can see on a profile can drive a filter, split or dynamic block. [eb3ee2d82966]
6. **Lists are static and for opt-ins. Segments are dynamic and for campaigns.** Keep 1 primary email list and 1 primary SMS list for organic opt-ins (forms and checkout). Make a new list for each import or other source (example: an Instagram giveaway gets a giveaway welcome, not "10% off your first order"). Never send a campaign to the whole list; rarely send to any list. [d7c5cedcb3dd] [f24ba64fabd7]
7. **Only send campaigns to engaged people.** Every send to someone who will not open hurts sender reputation. Even a 10-order customer who never opens hurts deliverability if mailed. Keep engagement criteria in every segment you build, including interest segments (for example men vs women buyers). [9720dfa509a1] [0ca859db0b00]
8. **Split engaged segments into prospects and customers for learning.** The 2 groups buy for different reasons. After a send you can see whether the campaign converted first-time or repeat buyers. Example: if prospects bought from a review-heavy campaign, add more reviews to prospect campaigns and the welcome series. Source says Dispatch is "one of the only agencies" doing this. [9720dfa509a1] [49f85dfebaf9]
9. **But do not send to segments that are too small.** Sending campaign 1 only to prospects and campaign 2 only to customers halves each person's "shots on goal". You cannot know if someone buys on Tuesday or Friday. Brands under about $20M a year should send evergreen content to all engaged subscribers and personalise with dynamic content. Presenter's strong opinion. [0ca859db0b00] `[needs brand data: annual revenue, list size]`
10. **Match offer size to engagement window.** Evergreen content (no big offer, no big launch) goes to the 90-day engaged segment. Black Friday and big launches go to the 365-day engaged segment to re-engage once-a-year shoppers. Dispatch practice, not a tested rule. [3f50ca527fa4]
11. **Grow the list as fast as possible from paid traffic.** Capturing paid visitors as subscribers is "one of the most important things" for profitable growth. Klaviyo's "excellent" badge at 3% form conversion is "not excellent"; a tested form should convert over 9% of site traffic. Agency client data. [ea0cb89619eb] [4be0db20360f] `[needs brand data: current form views and submit rate]`
12. **The offer is the biggest lever on form opt-in rate.** Offer beats behaviour, which beats copy, which beats design. Every customer demographic reacts differently. [ea0cb89619eb]
13. **Micro-commitment beats a straight email ask.** Step 1 asks only "Claim 20% off / I'm not interested". Once people say yes, far more give their email. "9 times out of 10" it wins, but still test it. [4be0db20360f]
14. **Deliverability is the least exciting and most important part.** Sender reputation works like a credit score: history-based and hard to rebuild. Inputs: bounces, spam complaints, engagement (opens, clicks, replies), consistent cadence, domain authentication. [6d8587217a67] [a192f5312b82]
15. **Consistent cadence protects revenue and reputation.** Several weeks with no campaign makes you fall out of mind; unsubscribes and spam complaints then rise. If you mail once a month, subscribers are not engaged when Black Friday comes. Example cadence given: 2 campaigns a week plus daily flows. [dbd9ab70c7db] [6d8587217a67]
16. **Do not use Klaviyo's default flow templates for content.** Flows are the backbone of the journey and every brand's journey differs. Exception: use templates for abandonment flows to inherit the trigger, filters and dynamic product table. [07f1b027ac4e] [a0bdafa6ea40]
17. **Profile filters are checked before every flow email.** So a welcome subscriber who buys between email 1 and 2 never gets email 2. [07f1b027ac4e]
18. **Branch abandonment and post-purchase flows by prospect vs customer.** Prospects need the welcome offer, USPs and objection handling. Customers are not eligible for the acquisition offer; use subscribe-and-save, loyalty or cross-sell. [f147a186a98d] [55898f20e161]
19. **In abandonment flows, shorter delays usually convert better.** Agency test observation; A/B test per brand. [fbfeb91636ec]
20. **The first purchase experience decides the second purchase.** Post-purchase emails must put product education, use cases and resources in front of first-time buyers. [55898f20e161]
21. **What you say matters 10 times more than how you say it.** Offer, product choice, message and CTA drive conversion. A beautiful Mother's Day email selling men's items will not convert. Small brands over-invest in pixel-perfect creative. Opinion from audits. [34710bc8ca91]
22. **Design in Figma and slice into Klaviyo.** Custom fonts fail in many inboxes; text wraps differently on desktop and mobile; templates make you look like every other brand. Image slices render pixel for pixel. Brand consistency from ad to site to pop-up to email builds first trust. The agency sells this service. [5fde08efd3f8] [92e649c06ecd] [b6185512bac6]
23. **Every email must add value.** It should educate, entertain or solve a problem. If you are not sure the subscriber will be glad they opened it, rewrite. Applies to flow emails too. [7ac91a47ef79]
24. **Optimise unique counts, not rates.** Open rate down 10% with unique opens up 40% means 40% more people can click. Sending 3 a week instead of 1 lowers rates but raises unique clicks. Dispatch philosophy. [489a0deaff01]
25. **Clicks, not opens, are the deliverability signal.** Since iOS 15, Apple Mail opens every email, so open rate no longer shows inbox placement. [3dca25bfe545] [dccf91db3e0a]
26. **Test monthly, on content not subject lines, and judge on placed order rate.** Content (offers, products featured, image type, CTA copy) is the highest-leverage test. Change 1 element. Never judge on open rate. [659e9f913086]
27. **Site traffic is the biggest driver of flow revenue.** Flow revenue down 30% usually means 30% fewer people saw the pop-up and entered flows. It is only a red flag if traffic was up. [d2e68173f29a]
28. **Monitor analytics monthly to catch silent breakage.** Example failures: a Shopify theme update stops the pop-up showing; abandoned cart flows stop sending. "Tens of thousands of dollars" slip away unnoticed. [5d6743fc3f40]
29. **Personalise inside one email before splitting into many sends.** Dynamic blocks, predictive fields and integration properties make one send behave like several. [9ba42019fe30] [03624b075480]

## 3. Procedures

### 3.1 Account creation and Shopify integration [8796c9f1ffa6] `[verify UI]`
1. Sign up. Choose "sell products online". Choose Shopify as primary platform. Enter the Shopify URL.
2. If migrating (example: from Mailchimp), state your existing list size. If new, choose "I don't have contacts yet".
3. Sender name: brand name, or founder plus brand (example "Elliot at Dispatch"). Set the sender email address.
4. Choose uses (email, SMS, push, reviews). The course covers email only.
5. On-site tracking: turn on the Shopify app embed in the Shopify theme (button takes you there).
6. Tick "sync your Shopify email subscribers to Klaviyo" so form and checkout sign-ups enter Klaviyo, into your main email list (3.7).
7. Do the same for SMS subscribers into the main SMS list.
8. Leave "sync profiles, profile data and custom properties from Klaviyo to Shopify" unticked. Source sees no reason for most brands.

### 3.2 Smart sending, attribution and reporting exclusions [1ce671434e00] `[verify UI]`
1. Email > sender preferences. Smart Sending ON. Default 16 hours. Source keeps 16 hours; customisable per brand.
2. "Ignore transactional messages": presenter leaves it unticked for most brands (a just-purchased person can still get a campaign). Your call.
3. Attribution settings: Klaviyo default 5-day open, 5-day click. Shorter for impulse products; longer for long-consideration products (example: $10,000 furniture, about 30 days of thinking). Do not go far from 5/5. Demo sets 3 days open, 3 days click. `[needs brand data: typical days from first visit to order]` `[web check: current Klaviyo default attribution window]`
4. Tracking and reporting data: tick exclude transactional messages from attribution (order confirmations must not claim revenue).
5. Tick exclude bot clicks for email. Tick exclude bot clicks for SMS.
6. Tick exclude Apple Mail Privacy Protection opens from attribution.
7. Save. Expect reported email revenue to drop if the old setup was inflated.

### 3.3 Data settings: anonymous tracking and UTMs [8796c9f1ffa6] `[verify UI]`
1. Data > anonymous visitor tracking (off by default). Turn it on. Views and adds to cart before sign-up then attach to the profile once the person subscribes (retroactive backfill). Result: more browse and cart abandonment sends.
2. UTM tracking: source defaults to Klaviyo, medium to message type (email or SMS). Also tick campaign, ID and term; custom parameters optional. "Better to have more than less."
3. Tick "automatically add UTM parameters to links". Needed for GA, Triple Whale and Shopify analytics to credit Klaviyo.

### 3.4 Brand library, fonts and social icons [b8afb62d37d6] `[verify UI]`
1. Brand: upload logo (used in headers, sometimes footers).
2. Set colours: accent, body text, buttons, links.
3. Primary font: Klaviyo supports only web-safe fonts here. Pick the closest match.
4. Header links: "not really useful for most brands". Optional.
5. Social icons: set once so footers fill in automatically. Save.
6. Fonts: add custom fonts. Google fonts and Adobe fonts can be selected; fully custom fonts use "hosted web font" with Klaviyo's hosting steps.
7. Set a fallback font for each custom font (example: Geist with Tahoma fallback). Gmail may show only Google or web fonts.
8. Optional: set brand voice for Klaviyo's AI copywriting.

### 3.5 Deliverability setup: sending domain and DNS [a192f5312b82] [6d8587217a67] `[verify UI]`
1. Account name > settings > domains > add domain.
2. Enter the root domain (the brand website). Next.
3. Choose a sending subdomain (example: send.brand.com).
4. Klaviyo may offer an Entri integration (may cost money). Source sets up manually.
5. Choose the DNS provider (or "other"). Copy each DNS record name and value into the registrar's DNS settings (example: GoDaddy).
6. Click verify only after the records are added. Verification can take up to 48 hours. Finish.
7. Add SPF, DKIM and DMARC records (source links a guide; steps not shown).
8. DMARC: source says it must always read p=none, never reject or quarantine. See section 9: this conflicts with standard guidance. `[web check: Gmail and Yahoo bulk sender DMARC requirements and recommended policy path]`
9. Keep spam complaints below 0.3% (Gmail and Yahoo), ideally below 0.1%. Keep bounces under 1%.

### 3.6 Consent pages and opt-in [8c1b383c08cf] `[verify UI]`
1. Settings > other: preference page, subscribe page, email confirmation page, unsubscribe page.
2. Edit the preference page with the drag and drop editor to match the brand (text, images, background, button colours). Edit its success page.
3. Footer must let subscribers update preferences or unsubscribe at any time. Legally required.
4. Source always chooses single opt-in over double opt-in because most people never click the confirmation. So it does not bother editing the subscribe or confirmation pages. See section 9 for the compliance caveat. `[web check: double opt-in rules in the markets the brand sells to]`
5. Unsubscribe page: add a thank-you line for being part of the brand.

### 3.7 Master list and the 6 core engaged segments [d7c5cedcb3dd] [9720dfa509a1] [1d456b02f483] [bf989ee22bb1] [f24ba64fabd7] `[verify UI]`
1. Audience > lists and segments > create list. Name it "Master email list". All pop-up and checkout sign-ups go here.
2. Create a separate SMS list.
3. Create segment. Build the engagement block with OR:
   - opened email at least once in the last 180 days, where Apple privacy open is false; OR
   - clicked email at least once in the last 180 days, where bot click is false; OR
   - subscribed to list at least once in the last 14 days; OR
   - active on site at least once in the last 14 days.
4. Then AND: can receive email marketing (not unsubscribed, not suppressed). Using OR here would pull in almost everyone.
5. Then AND: placed order zero times over all time. This is the prospects segment.
6. Check the preview count. Create.
7. Clone and change only the last condition to "placed order at least once over all time". This is the customers segment.
8. Make 90-day, 180-day and 365-day versions of each (change the open and click windows). Total 6 segments.
9. Why the 14-day carve-outs: new subscribers may have had only 1 or 2 emails; a returning site visitor is showing intent, like a retargeting window. If they do not engage in about 2 weeks, they fall out.
10. Other conditions available in the builder: location proximity (retail stores), in the EU or not, any profile property (example: Shopify tag contains text), viewed specific items.

### 3.8 Build the sitewide pop-up form [4be0db20360f] [4bb4a381c989] [4d0639885e1a] `[verify UI]`
1. Sign-up forms > create form. Start from a template that already has a micro-yes step, or a blank form.
2. Name it "Sitewide pop-up form". Email list = Master email list. Use a separate list for SMS (Klaviyo recommends it).
3. Form type: pop-up (beats flyout and full page in agency tests; still worth an A/B test).
4. Step 1, micro-yes: offer in the header, large and clear (example "You've got 20% off plus join our VIP list, get exclusive offers and product releases"). Buttons "Claim 20% off" and "I'm not interested". Button text must match the offer (demo changes $20 to 10% in both places).
5. Remove the side image ("no side image"). Forms without images usually convert better; attention goes to the offer.
6. Brand every step: fonts, colours, buttons, input fields, background.
7. Step 2, email: email input required, with a "field is required" message. Button action "submit form" to the Master email list, then show next step.
8. Step 3, SMS: collect phone even if no SMS program is live yet. Submit to the SMS list, then next step.
9. Step 4, success: either show the code, or say the code is on its way to inbox and phone. Source prefers sending it, so the first email gets opened and clicked (sender reputation boost). Use the "go to inbox" button action.
10. Button actions available: submit form, close form, go to URL (example: a 60% off collection), subscribe via text.
11. Mobile check: make the offer text and button text large enough on mobile. Build one form for both devices. Split into separate desktop and mobile forms (targeting and behaviours > device, then clone) only if they convert differently or the brand font will not work on both. "Really not necessary."
12. Teaser: turn on; shape (circle, corner, rectangle) and colours to brand; display after the form is closed.
13. Behaviour: show immediately, not "based on rules". A/B options: 5-second delay, or after 30% scroll.
14. Frequency: example, do not show again until 5 days after someone closes it.
15. Devices: all.
16. Untick "click outside form to close". Only the X closes it.
17. Targeting: do not show to existing Klaviyo profiles.
18. Optional targeting uses: show to all visitors (sale-link form); show to email subscribers only (exclusive sale, or to get email subscribers onto SMS); exclude URLs (cart page, so you do not give margin to someone already converting; a sale page if the 10% cannot stack); do not limit to the homepage; location by IP (different offer for Canada vs US); UTM source (example: test 20% for cheaper TikTok traffic, 10% for others); cart value (example: only over $1,000 in cart).

### 3.9 Monthly pop-up A/B test roadmap [ea0cb89619eb] [d66d62f1a9cd]
Run 1 test every month, even at 10% conversion. Order by leverage:
1. Offer: % off vs $ off, 10% vs 15%, free shipping, cash back, free gift with purchase. For $ vs %, set the $ amount at about 10% of AOV. `[needs brand data: AOV, margin]`
2. Behaviour: micro-yes vs none; a zero-party data question in the form (lifts conversion and gives data); load timing (immediate vs 10 seconds); which pages trigger it; exit intent.
3. Copy: short vs long (example "Get weekly updates on everything cool happening with the brand"); showing the offer vs a "mystery offer" (still 10% behind it).
4. Design: image vs none; product vs lifestyle image; which lifestyle image; text size (bigger for older customers).
5. End the test monthly if needed and keep the higher submit rate. Klaviyo may pick a winner automatically (example: after 32 days).

### 3.10 Welcome series [ef1cb30f5c95] [07f1b027ac4e] [65d6a163c4ce] [b6185512bac6] `[verify UI]`
1. Flows > create flow > build your own. Name "Welcome series".
2. Trigger: added to list = Master email list (same list as the form).
3. Profile filter: placed order zero times over all time. Save. Add brand-specific filters (example: exclude known B2B customers from a DTC welcome).
4. Email 1 with no initial delay. Name emails in a standard pattern ("Welcome series email 1") so dashboards stay readable.
5. Subject example "Welcome to [brand]". Preview example "10% off inside".
6. Sender email on the authenticated domain (example elliot@ or support@). Reply-to = customer support inbox.
7. Design in Figma, slice, upload (3.21). Add subject and preview after the design.
8. Content baseline "for 99% of DTC brands", from agency A/B tests:
   - Email 1 (immediate): logo, the code, get them back to the site fast. Add 1 or 2 of: short founder letter (mission, origin, story), brand values, what makes the products unique, bestsellers or collections.
   - 1-day delay. Email 2: USPs. Why you are the best in the market.
   - Email 3: what you offer. Top 3 to 5 bestsellers or collections.
   - 1-day delay. Email 4: brand story. Why the brand exists, the problem it solves, a human face. Not every story converts.
   - 1-day delay. Email 5: us vs them. Pick an angle (Starbucks vs every other coffee).
   - Next: customer reviews and testimonials.
   - Next: FAQs (prospects rarely find the FAQ page).
   - Then brand-specific angles (example: 100 years in business).
   - Most brands use 1-day delays between every email. (The spoken sequence skips the delay between emails 2 and 3; the summary says 1 day between each.)
9. Every email carries a reminder that the offer is still valid (example: a top banner). Each email has one focused reason to buy. Hold nothing back that could help conversion.
10. Set emails live one by one.

### 3.11 Abandoned checkout [85117c7d0910] [fbfeb91636ec] [f147a186a98d] [79cdac8bb86e] [a0bdafa6ea40] `[verify UI]`
1. Create flow and search "checkout". Nothing appears. Klaviyo calls it "Abandoned Cart Reminder"; the standard version's trigger is Checkout Started. Use the template for the dynamic product table.
2. Filter: placed order zero times since starting this flow.
3. Optional filter "has not been in flow in the last X days". Template or some brands use 7 days; Dispatch uses 2 to 3 days (a repeat checkout shows interest).
4. First delay: template 4 hours. A/B test 4 hours vs 2 hours; shorter usually wins.
5. Remove the template's SMS split (SMS if reachable, else email after 4 hours). Source sends email and SMS at the same time or very close. Reason: you cannot know which channel converts; email has visuals; every hour counts. (Section 3.28 gives a different example.)
6. Add a conditional split: placed order at least once over all time? Yes = customers. No = prospects.
7. Prospects email 1: welcome offer reminder, dynamic cart contents, USPs.
8. Delay about 20 hours ("good starting point", varies by brand).
9. Prospects email 2: offer, cart, 1 or 2 top objections (price; value, using reviews).
10. Prospects email 3: another objection plus cart. Minimum 3 emails for prospects.
11. Customers branch: returning-customer objections; incentives like subscribe-and-save or loyalty. No acquisition offer.
12. Dynamic table from the template: 2 columns. Column 1 image via dynamic variable. Column 2 product title, quantity, total. Delete quantity or total if not wanted. Place Figma slices above and below.
13. Link every image slice to `{{ event.extra.checkout_url }}` (copy it from the template's "back to my cart" button). This returns each person to their saved checkout.
14. Preview with several profiles to check images and titles.

### 3.12 Abandoned cart [85117c7d0910] [a0bdafa6ea40] `[verify UI]`
1. Create flow, search "cart", choose "abandoned cart reminder" with the Added to Cart trigger. Use the template.
2. Filters (default in template): checkout started zero times since starting this flow AND placed order zero times since starting this flow. So cart and checkout flows never overlap.
3. Content can match the checkout flow unless your cart and checkout experiences differ.
4. Why both flows: many brands only have the checkout version and think carts are covered; people who add to cart but never start checkout get nothing.

### 3.13 Browse abandonment [909e75c1eb8d] [79cdac8bb86e] `[verify UI]`
1. Create flow > browse abandonment template. Trigger: Viewed Product.
2. Default filters exclude only checkout started and placed order. Add AND: added to cart zero times since starting this flow.
3. Keep "has not been in flow in the last 30 days" (browse interest does not justify frequent reminders).
4. Template has 1 email; source suggests more.
5. Branch prospects vs customers.
6. Content: dynamic viewed products; what makes the brand unique; copy that accepts interest is lower; suggest other products; heavy social proof.
7. Fix the link: template links "shop now" to the organisation URL (homepage). Preview and test, open the event properties (name, ID, price, URL), copy the product URL property, paste it as the link. Example: "Cook the Book" link goes to that product page.

### 3.14 Post-purchase [55898f20e161] `[verify UI]`
1. Template "post-purchase follow-up" exists (trigger Placed Order, no default filters, 1-day delay at 9 AM). Source builds manually because no dynamic content is needed.
2. Trigger: placed order.
3. Filters are brand-specific: you may exclude subscription or B2B customers or send them to another flow.
4. Do not fix a time of day. Someone who bought at 10 PM likely shops at 10 PM; send 1 day after the action.
5. Conditional split: placed order equals 1 over all time = first-time buyers. Else returning.
6. First-time content: thank you; how to get the most from the product (use cases, education); a plain-text customer service check-in ("Hey, thank you so much for your first order. Would love to hear how things are going. Let us know if you need any help or if you have any questions."); then the next order (subscription, loyalty, next offers).
7. Returning content: appreciation for loyalty; offers that move them to higher LTV; dynamic cross-sells.

### 3.15 Win-back (average-based) [021057848a4f] `[verify UI]`
1. Trigger: placed order. Filter: placed order zero times since starting this flow.
2. First delay from your own data, not Klaviyo's default (presenter thinks it is 90 days). Dispatch formula: take the median and the average days between purchases and pick a point between them. `[needs brand data: median and mean days between orders from Shopify]`
3. Sanity-check against consumption. Example: a food or drink product used up in 30 days, about 5 days shipping, so 45 to 50 days; set the first delay to 45 days.
4. Content: "we miss you", a dynamic exclusive offer with urgency, why you beat competitors (Starbucks vs Dunkin or a local cafe).
5. Delays between emails 5 to 7 days, not 1 day.
6. Final email: urgency, the offer expires.

### 3.16 Sunset flow and monthly suppression [56d433c32a2b] `[verify UI]`
1. Create segment "Sunset flow trigger, unengaged subscribers": opened email zero times in the last 180 days AND clicked email zero times in the last 180 days AND can receive email marketing. 180 days is "usually good for most brands".
2. Flows > build your own > "Sunset flow" > trigger "added to segment" = that segment.
3. Profile filters: opened email zero times since starting this flow; clicked email zero times since starting this flow. Source joins them with OR. See section 9: AND matches the stated intent.
4. Email 1 immediately. Subject line highlights a strong offer.
5. Delay 5 days. Email 2. Delay 5 days. Email 3: tells them they will be removed unless they engage.
6. Delay 5 days. Update profile property: new boolean property "unengaged" = true.
7. Create segment "unengaged = true to suppress" AND can receive email marketing.
8. Once a month: manage segment > export segment to CSV. Profiles > view suppressed profiles > import the CSV to suppress.
9. Gumball example: "We miss seeing you around", a unique dynamic 10% code (cannot leak), a reminder, then "click below to keep receiving updates about fresh inventory, special discounts and vending tips".
10. Reasons: Klaviyo bills on active profiles; unengaged sends hurt deliverability. `[web check: current Klaviyo billing basis]`

### 3.17 A/B test inside a flow [909e75c1eb8d] [b5c1274e5d10]
Method A (timing test, manual split):
1. Before the time delay, add a conditional split: random sample 50%.
2. Clone the delay and email to the other branch.
3. Change 1 thing (example: 2 hours vs 4 hours).
Method B (content test):
1. Open the flow email, keep it as version A, click "create A/B test" at the bottom.
2. Change 1 element in version B.
3. Choose "automatically choose distribution". Klaviyo starts 50/50, shifts traffic as its model finds a winner, then sends only the winner once significant. `[verify UI]`
4. Track in the experiments section.

### 3.18 Choose campaign cadence [dbd9ab70c7db]
1. Question 1: how many should you send? For $1M to $10M brands, balance engagement, deliverability and ROI. Raise volume (example 1 to 4 a week) and watch click-through rate, unsubscribe rate and spam complaint rate. If they stay flat, send more.
2. Question 2 (more important): how many can you send every week without fail? If 4 would become 4 then 1, commit to a sustainable number (example 2 a week). Add team or agency support later if ROI is positive.
3. Minimum stated elsewhere in the course: at least 1 campaign a week. `[needs brand data: current cadence, CTR, unsubscribe and spam trends by week]`

### 3.19 Build and send a campaign [81300e87c081] [ba5c04225d61] [5b2cad894e44] `[verify UI]`
1. Campaigns > create campaign. Name (example "New product launch"). Date (example July 9). Type email. Add tags (example "new product launch") for later analysis.
2. Audience "send to": segments only, engaged (example: prospects engaged 90-day).
3. "Don't send to": exclusion segments (example: bought in the same category in the last 3 days; build that segment first).
4. Smart sending: on by default from account settings; turn off for a big launch where people who got a flow email in the last 16 hours will still want it. Leave on for routine content.
5. Tracking: UTM parameters on.
6. Template: saved templates, email library, or create new. For Figma builds choose create new and drag in slices one by one.
7. Subject: intriguing (example "It's finally here..."). Preview: a second reason to open (example "The product everyone's been asking for").
8. Campaign sequence builder: optional follow-up resend (3.20).
9. Review screen: estimated recipients (included minus excluded), smart sending state, subject, preview, content, from and reply-to, unsubscribe link present, tracking. Take 10 seconds to check.
10. Schedule: fixed time (example 9 AM Eastern when the product goes live on Shopify) or recipient's local time zone.
11. Tick "determine recipients at send time" when exclusions are dynamic (example: bought in last 3 days must be judged at send, not at scheduling).

### 3.20 Follow-up resend to non-openers [6964a9fc308f] `[verify UI]`
1. In the sequence builder, toggle the follow-up. It resends to people who did not open.
2. Write a new subject line (example "[Brand] T-shirts just in time for summer").
3. Narrow the audience (example: first send 90-day engaged, resend 30-day engaged).
4. Delay: Klaviyo's built-in resend cannot be under 48 hours. Fine for launches.
5. For Black Friday, inboxes are flooded; do 2 or 3 resends of the same campaign by cloning and sending manually.

### 3.21 Figma image-slice email build [5fde08efd3f8] [b6185512bac6] [92e649c06ecd]
1. Design the full email or series in Figma.
2. Slice each section. Export each slice as PNG or JPEG.
3. In Klaviyo, drag in an image block, upload the slice, compress it.
4. Repeat until the email matches the design.
5. Add any product block (static or dynamic) in Klaviyo; it cannot come from Figma.
6. Add a real footer (3.23).
If there is no time or design resource, a Klaviyo template is acceptable, but many template images (example: a GIF) cannot be edited in Klaviyo and replacements must match dimensions.

### 3.22 Dynamic product feed [66bb08b24b5c] `[verify UI]`
1. Add a product block. Static = chosen Shopify products. Dynamic = rule-based, recalculated each send.
2. Create a feed (example name "Bestsellers"): bestselling products over the last 3 days or last 90 days.
3. Filters: exclude a category; minimum price (example: nothing under $5); exclude low stock.
4. Create product feed and insert it.
5. Choice rule: fast-turning inventory with new styles, use dynamic bestsellers. A 10-SKU brand that is always in stock can show its 2 or 3 steady bestsellers statically.

### 3.23 Footer [5fde08efd3f8]
1. Social links (usually).
2. Required: organisation details and unsubscribe language. Klaviyo blocks sends without an unsubscribe link and adds an "ugly" default if you omit it.
3. Dynamic tags pull organisation name, full address and current year from settings. The unsubscribe tag creates a unique link per recipient.

### 3.24 Campaign A/B test [659e9f913086] `[verify UI]`
1. Build version A. Click "create A/B test". Choose content or send time.
2. Send-time test: same email at 2 times (demo 12 AM vs 1 AM). Winning metric click rate. Size 100%.
3. Content test: change 1 element only. Good candidates: the offer, product types featured, lifestyle vs product images, 1-image hero vs 4-image hero (or a GIF), image placement, CTA copy ("shop now" vs "save now"). Do not spend tests on subject or preview.
4. Name variations descriptively ("one image hero", "four image hero").
5. Winning metric: placed order rate (Dispatch always). Never open rate.
6. Size distribution 100% (50/50 split). Why: at 40% on 1,000 recipients, only 200 get each version, a 1-day test picks a winner, and the other 60% get it; most brands are too small for that to be significant.
7. Schedule as normal. Review in the experiments section.

### 3.25 Dynamic content block (show/hide) [9ba42019fe30] [03624b075480] `[verify UI]`
1. Add a text block (example "Free shipping on all orders over $100").
2. Block > display > show/hide logic > logic builder. Property: country equals "United States". Copy the exact spelling from a real US profile.
3. Duplicate the block. Logic: does not equal "United States". Copy: "over $150".
4. Preview and test with a profile that has the country and one that does not. A profile with no country falls into "does not equal".
5. Other uses: show reviews based on zero-party answers; remind prospects of an unused acquisition offer; show customers their loyalty points balance.

### 3.26 Predictive win-back by expected next order date [109f8c9de246] [6818bdf85834] `[verify UI]`
1. Flows > build your own > create manually. Trigger: date property > expected date of next order.
2. Start on the date (not before). Time 12 PM in the recipient's local time zone. Repeat: never.
3. Filter: placed order zero times since starting this flow.
4. Delay 5 days, then the first win-back email.
5. Optional conditional split: historic CLV at least $1,000, or predicted CLV at least $1,000, gets a stronger, more personal discount.
Profile predictive fields named: expected date of next order, average time between orders, churn risk, AOV, historic CLV, predicted CLV, channel affinity (email vs SMS). Predictions need enough order history.

### 3.27 Multichannel (SMS and push) [4c7296971696]
1. Settings: SMS section (Klaviyo gives a phone number and compliance tools) and push section (needs your own mobile app). `[verify UI]` `[web check: SMS consent rules in each market]`
2. Add SMS and push steps into flows. Source example: abandoned cart sends SMS first, waits 2 hours, then email if not converted, with flow filters removing buyers.

### 3.28 Integrations and a loyalty birthday flow [9ca8e23a01f3] [9b7b4dd86442] `[verify UI]`
1. Settings > integrations > add integrations > all (source counts 187).
2. Start with the Shopify apps you already use. Search each by name and install from Klaviyo. Read what data it passes.
3. Named apps: Shopify, Gorgias (support), Recharge and Skio (subscriptions), Yotpo (loyalty), Okendo and Judge.me (reviews), a loyalty app (probably Rivo), Meta and Google Ads.
4. Uses: a Recharge subscription pause triggers an "unpause" flow; a review event stops you asking for a review of the same product again; push Klaviyo segments (example: high-value purchasers) to Meta or Google for retargeting and lookalikes.
5. Many integrations are configured in the other app. Loyalty example: API key, status enabled, events (points earned, tier up, reward redeemed, customer birthday), profile properties (points balance, loyalty status, referral URL, VIP tier name, date of birth).
6. Birthday flow: flows > create manually, name "[App] customer birthday", trigger metric = the app's customer birthday event.
7. In the email, preview and test, copy the event property for points earned (example 250) and paste it with "points".
8. Add personalisation > search the app > insert points balance (examples 1,669 and 355 for 2 profiles).
9. Preview with 2 profiles to confirm the numbers differ.

### 3.29 Suppress someone who still gets email after unsubscribing [8c1b383c08cf]
1. Open the profile. Email section > 3 dots > suppress.

### 3.30 Monthly analytics review [5d6743fc3f40] [d66d62f1a9cd] [41d10e199bc4] [8183b1fcc7d0] [d2e68173f29a] [ac6fccd77bd7] [3dca25bfe545]
1. List growth: profiles > view subscriber growth > 30 days. Note total, % change, gained, lost, trends.
2. Opt-in sources: checkout vs each pop-up. For checkout, compare the trend with Shopify orders and checkouts started; only a gap signals a broken integration.
3. For each pop-up: open the form, compare views and submit rate this 30 days vs prior 30 days. Views down with submit rate flat or up = traffic problem, not form problem.
4. Pop-up A/B test: end if needed, keep the winner, set next month's test.
5. Campaigns: status sent, last 30 days, sort by revenue. Then read click rate and placed orders. Then the lowest performers.
6. Campaign A/B tests: experiments section, last 30 days; read lift, win probability, significance. If Klaviyo warns that the test-period winner differs from the overall winner, rerun with a longer period and a bigger test group [ced1f90d7686].
7. Dashboards > business review: choose the month; compare previous period, or previous year if seasonal. Read Shopify revenue, attributed revenue, email share, campaign vs flow revenue.
8. Campaign metrics chain: recipients, unique opens, open rate, unique clicks, click rate, unique conversions, conversion rate, revenue, revenue per recipient, AOV. Explain the change, then open the top campaigns vs last month.
9. Flows: flow revenue vs site traffic first. Then the same metric chain. Then top flows vs last month. Open any flow with a big gap: show analytics, per-email opens and clicks vs last month, and skips.
10. Flow A/B tests: read progress and win probability.
11. Deliverability tab and reports by inbox provider (3.31).
Above about $100K a month in email revenue, source says a deeper dashboard tool is worth it (per-flow deliveries, clicks, click rate, RPR; 12-month open, click, unsubscribe and bounce trends; email vs SMS). Tool not named.

### 3.31 Monthly deliverability check and repair [3dca25bfe545] [98d43fdb4da1]
1. Deliverability tab: read the score (built from open, click, bounce, unsubscribe and spam rates) and its trend.
2. Compare account rates to Klaviyo's recommended values (section 4).
3. Keep bounce and spam well under limits. Unsubscribe slightly above the recommendation is accepted when extra sends earn more.
4. Check both recent campaigns and flows flagged as needing attention (high bounce, low click).
5. Every 30 days open the reports by inbox provider. Where one provider is weak (example: Hotmail and Outlook 46% opens and lower clicks; G Suite high bounce and unsubscribe), build very engaged segments for that provider.
6. If opens and clicks fall steadily: move sends from the 90-day segment to 30-day or 60-day engaged. Hold until metrics recover. Then widen slowly. No recovery timeline given.

### 3.32 Campaign content, copy and design checklist [3c10a64f1966] [8c9297aaf4b4] [1cddc0a49ff8] [4410834af2cb] [945e9b8a355c] [685553ea4865] [82bb67e79aeb]
Campaign types "99% of brands" should rotate (agency data, no numbers):
1. Product spotlight: 1 product, deep on why it beats rivals (materials, ingredients, details the PDP has but shoppers miss). Try it on non-bestsellers too. Collection spotlight: a theme across store collections.
2. Benefit email: 1 PDP bullet becomes the whole email, aimed at the group that cares most.
3. Content spotlight (for brands with blog or social content): first section teases the content, second section sells the product it relates to.
4. Education spotlight: teach the ingredient or problem, let the reader connect it to the product.
5. Weekly newsletter: created or curated (memes, a monthly playlist, industry news). Built for engagement.
6. Cultural event: Mother's Day, Father's Day, holidays, Black Friday, tied to a reason to buy now.
7. Promotions, 4 types: teaser (sale coming; SMS gets early access), launch (short, sell the click), reminders through a long sale (a bottom module in evergreen sends works), last chance (final day).
8. New product launch: at least 1 email the morning of launch; say why the subscriber should care.
Copy:
1. Know the audience; write benefits for that group, not product details (coffee: energy for a busy parent vs late-night focus for a young man).
2. 1 core message per email, 2 at most, from subject line to body. Cut fluff. Use icons or visuals over paragraphs.
3. Keep one consistent brand voice.
4. Sell the click, above all in promo and launch emails where earlier emails did the teaching. The landing page does the selling.
5. Use real urgency or scarcity ("ends tonight", limited stock), social proof (reviews, UGC, influencers, press) and curiosity gaps (tease the blog, "read more"). Never fake them.
6. Subject and preview under 50 characters each. Put the value first ("50% off sitewide", preview "Summer's finally here, shop now"). Do not over-invest in subject lines.
7. Pre-send check: does it educate, entertain or solve a problem?
Design:
1. Scannable layout, white space, clear headers and subheaders, distinct sections.
2. Section order: header, subheader, body copy if needed, image, CTA. Repeat in each section. Header = awareness, body = interest, CTA = ask.
3. A CTA under each promoted product.
4. Icons (for example check marks) instead of bullet points.
5. Promo code in bold right before the CTA (example "use code SUMMER15 at checkout").
6. Only sharp, relevant images (no other product next to a product, no woman as the hero of a men's email).

## 4. Rules, thresholds and numbers

| rule | number or threshold | condition | source's basis | card id |
|---|---|---|---|---|
| Email share of total store revenue | at least 30% of all Shopify revenue | ecommerce brands | presenter heuristic | 465d3381b2a7 |
| Smart sending window | 16 hours (default, keep) | account level; override per campaign for big launches | Klaviyo default plus opinion | 1ce671434e00, ba5c04225d61 |
| Attribution window | default 5-day open / 5-day click; demo 3/3; do not stray far from 5/5 | shorter for impulse, longer for long consideration (example $10,000 furniture, ~30 days) | opinion | 1ce671434e00 |
| DNS verification time | up to 48 hours | new sending domain | Klaviyo UI | a192f5312b82 |
| DMARC policy | p=none, never reject or quarantine | always, per source | opinion; conflicts with standard advice | a192f5312b82 |
| Spam complaint rate | below 0.3%, ideally below 0.1% | Gmail and Yahoo rules | source citing providers | 6d8587217a67 |
| Spam complaint rate (Klaviyo tab) | "under 0.01%"; client at 0.004% | deliverability tab recommendation as spoken | Klaviyo value as read on screen | 3dca25bfe545 |
| Bounce rate | under 1%; client 0.67% | always | providers and Klaviyo | 6d8587217a67, 3dca25bfe545 |
| Unsubscribe rate | Klaviyo recommends under 0.3%; client 0.67% accepted | higher tolerated when more sends earn more | Klaviyo value plus opinion | 3dca25bfe545 |
| Open rate (Klaviyo tab) | above 33% "okay"; client 62% | account level | Klaviyo value | 3dca25bfe545 |
| Click rate (Klaviyo tab) | above 1.2% "okay"; client 1.71% | account level | Klaviyo value | 3dca25bfe545 |
| Minimum campaign rates | open above 30%, click above 0.5% | below this, deliverability is likely in trouble | presenter; says benchmarks otherwise depend on brand | ea472261103e |
| Engaged window | opened or clicked in 180 days; subscribed or active on site in 14 days | engaged segment definition | Dispatch setting | 9720dfa509a1, 1d456b02f483 |
| Segment tiers | 90, 180, 365 days x prospects, customers = 6 segments | campaign audiences | Dispatch setup | bf989ee22bb1 |
| Evergreen vs big-offer audience | evergreen to 90-day; Black Friday and big launches to 365-day | campaign planning | Dispatch practice | 3f50ca527fa4 |
| Do not micro-split sends | under about $20M a year | send to all engaged, personalise with dynamic content | opinion | 0ca859db0b00 |
| Pop-up conversion target | above 9% of site traffic; Klaviyo "excellent" badge at 3% | tested and optimised form | agency client data | ea0cb89619eb |
| $ offer size | about 10% of AOV | when testing $ off vs % off | opinion | ea0cb89619eb |
| Pop-up test cadence | 1 test a month | always, even at 10% conversion | opinion | ea0cb89619eb |
| Micro-yes win rate | wins "9 times out of 10" | still A/B test | agency tests | 4be0db20360f |
| Pop-up re-show frequency | example 5 days after close | returning visitors | example | 4d0639885e1a |
| Pop-up rule-based alternatives | 5-second delay or 30% scroll | only as an A/B variant | example | 4d0639885e1a |
| Cart-value targeting | example over $1,000 | a special offer for big carts | example only | 4d0639885e1a |
| Welcome email 1 delay | 0 (immediate) | always | opinion | ef1cb30f5c95 |
| Welcome gaps | 1 day between emails | most brands | agency baseline | 65d6a163c4ce, b6185512bac6 |
| Welcome bestsellers | top 3 to 5 | email 3 | baseline | 65d6a163c4ce |
| Checkout flow first delay | template 4 hours; test vs 2 hours | shorter usually wins | agency tests | fbfeb91636ec |
| Checkout flow re-entry | template 7 days; Dispatch 2 to 3 days | "has not been in flow" filter | opinion | 85117c7d0910 |
| Prospect abandonment gap | about 20 hours | starting point, varies | opinion | f147a186a98d |
| Prospect abandonment emails | minimum 3 | prospects branch | opinion | f147a186a98d |
| Browse re-entry | 30 days | most brands | opinion | 909e75c1eb8d |
| Metric-to-send example | checkout started, email 2 hours later | example | example | 059f73755fa8 |
| Post-purchase timing | 1 day after order, no fixed hour (template has 9 AM) | always | opinion | 55898f20e161 |
| Win-back first delay | between median and mean days between orders; Klaviyo default "probably 90 days" | use own data | Dispatch formula | 021057848a4f |
| Win-back worked example | 30-day product + ~5 days shipping = 45 to 50 days; set 45 | consumables | example | 021057848a4f |
| Win-back gaps | 5 to 7 days | between win-back emails | opinion | 021057848a4f |
| Predictive win-back | fire on expected date, 12 PM local, never repeat, first email 5 days later | predictive data populated | example | 109f8c9de246 |
| High-value split | historic or predicted CLV at least $1,000 | stronger offer | example | 6818bdf85834 |
| Sunset trigger | 0 opens and 0 clicks in 180 days | "usually good for most brands" | opinion | 56d433c32a2b |
| Sunset timing | 3 emails, 5-day gaps, property update 5 days after email 3 | then suppress monthly | Dispatch setup | 56d433c32a2b |
| Cadence floor | at least 1 campaign a week | all brands | opinion | a084662e8ae4 |
| Cadence test | raise (example 1 to 4 a week) while CTR, unsubscribes, spam stay flat | $1M to $10M brands | opinion | dbd9ab70c7db |
| Sustainable cadence | example 2 a week | if 4 cannot be sustained | opinion | dbd9ab70c7db |
| Resend delay | not under 48 hours in built-in resend | Klaviyo limit as shown | Klaviyo UI | 6964a9fc308f |
| Black Friday resends | 2 to 3 manual resends | flooded inboxes | opinion | 6964a9fc308f |
| Launch send | at least 1 email the morning of launch | new product launches | opinion | 3c10a64f1966 |
| Subject and preview length | each under 50 characters; value in first 3 words | all campaigns | opinion | 685553ea4865 |
| Themes per email | 1 core message, 2 at most | all emails | opinion | 945e9b8a355c |
| Metric noise | under 5% change = noise; look for over 10% | monthly review | opinion | dccf91db3e0a, d2e68173f29a |
| A/B size distribution | 100% (50/50) | most brands | opinion; 40% holdout too small | 659e9f913086 |
| A/B winning metric | placed order rate for content; click rate for send time; never open rate | all tests | Dispatch practice | 659e9f913086 |
| Accept a winner without significance | example 98% win probability | small brands may never reach significance | judgement call | bfa3ffd83c16 |
| Deeper dashboard | worth it above about $100K a month email revenue | reporting | opinion | 8183b1fcc7d0 |
| Live integrations | 187 | Klaviyo directory at filming | Klaviyo UI | 9ca8e23a01f3 |

## 5. Diagnostics and checks

| check | how | good | bad | next step | card |
|---|---|---|---|---|---|
| Is email big enough? | business review: attributed revenue / Shopify revenue | 30% or more | well below 30% | check flows live, form rate, cadence, segments | 465d3381b2a7, 41d10e199bc4 |
| Is reported revenue inflated? | attribution settings | transactional, bot clicks, Apple opens excluded; window fits journey | defaults with no exclusions | apply 3.2, re-baseline | 1ce671434e00 |
| Are browse and cart flows starved? | data settings | anonymous tracking on | off | turn on | 8796c9f1ffa6 |
| Is the domain authenticated? | settings > domains | branded sending subdomain verified; SPF, DKIM, DMARC present | Klaviyo shared domain, missing records | 3.5 | a192f5312b82 |
| Are campaigns hitting the whole list? | campaign audiences | engaged segments only | "all subscribers" list | build 6 segments | d7c5cedcb3dd |
| Segment logic right? | segment definition and preview count | engagement ORs, then AND mailable, AND order condition | OR on "can receive email marketing" | fix AND/OR | 1d456b02f483 |
| Checkout sign-ups fell | opt-in sources vs Shopify orders and checkouts | same % drop | big gap | check Shopify sync and integration | d66d62f1a9cd |
| Pop-up sign-ups fell | form views and submit rate vs prior 30 days | views down, rate flat or up (example 2.19% to 2.28%) | rate down sharply | fix or test the form | d66d62f1a9cd |
| Pop-up not showing | analytics month over month | steady views | views near 0 after a theme update | re-enable app embed and form | 5d6743fc3f40 |
| Both abandonment flows exist | flows list | Added to Cart flow and Checkout Started flow | only "abandoned cart reminder" on Checkout Started | build 3.12 | 85117c7d0910 |
| Browse filters complete | browse flow trigger filters | added to cart zero times since starting flow included | missing | add filter | 909e75c1eb8d |
| Recovery links | abandonment email links | checkout URL variable; product URL on browse | homepage link | 3.11 step 13, 3.13 step 7 | 79cdac8bb86e |
| Welcome gated | welcome filter | placed order zero times over all time | none | add filter | 07f1b027ac4e |
| Why did campaign revenue move? | business review metric chain | the driver is identified (volume, opens, clicks, conversions, AOV) | only the headline number reported | walk the chain | 8183b1fcc7d0 |
| Which layer broke? | which metric fell | n/a | opens and unique opens down: deliverability. Clicks down: content. Conversions down with clicks steady: merchandising and offers | fix that layer | dccf91db3e0a |
| Clicks vs revenue divergence | click rate vs placed orders per campaign | understood | a high-click, low-revenue send treated as a failure | reformat to add merchandising (newsletter case) | ea472261103e |
| High-AOV distortion | revenue vs order count | both read | revenue sort only | check orders and AOV | 7b7bba687f4a |
| Flow revenue drop | site traffic trend | fell in step with traffic | traffic up, flow revenue down | open the flows | d2e68173f29a |
| Flow revenue down 15%, conversions down 6% | AOV row | AOV explains it (sitewide sale) | unexplained | check dynamic blocks for lower-priced products | d2e68173f29a |
| Specific flow dropped | show analytics: per-email rates and skips vs last month | skips expected by design (example 620 skipped vs 190 delivered was fine) | people skipped by accident | fix filters, splits, overlap | ac6fccd77bd7 |
| A/B result trustworthy? | experiments: win probability, significance, Klaviyo warning | clear, significant, or high probability with meaningful gap | test-period winner differs from overall winner | rerun longer and bigger | ced1f90d7686, bfa3ffd83c16 |
| Deliverability health | deliverability tab vs Klaviyo values | above open and click values; bounce and spam well under | falling clicks, bounce or spam near limits | narrow segments (3.31) | 3dca25bfe545 |
| Inbox provider weak spot | reports by provider | similar across providers | one provider far lower or high bounce | provider-specific engaged segment | 3dca25bfe545 |
| Message overlap | calendar of campaigns plus flows per person | no pile-up | campaign plus 3 flow emails in 24 hours | coordinate, use smart sending | 24b8079fe1fe |
| Unsubscribed person still mailed | profile | suppressed | still receiving | suppress manually | 8c1b383c08cf |
| Pre-send value check | read the email | educates, entertains or solves a problem | "not sure" | rewrite | 7ac91a47ef79 |
| Promo code visible | email layout | bold code right before CTA | code buried, "shop now" dominant | move code | 82bb67e79aeb |

## 6. Tools, settings and named features

All `[verify UI]`.
- **Klaviyo sender preferences:** Smart Sending (16 hours), ignore transactional messages. [1ce671434e00]
- **Attribution settings and tracking/reporting exclusions:** transactional, bot clicks (email, SMS), Apple Mail Privacy Protection opens. [1ce671434e00]
- **Data settings:** anonymous visitor tracking; UTM tracking with auto-add. [8796c9f1ffa6]
- **Brand library:** logo, colours, web-safe primary font, custom fonts (Google, Adobe, hosted web font) with fallback, header links, social icons, brand voice. [b8afb62d37d6]
- **Domains:** add domain, sending subdomain, Entri integration or manual DNS. [a192f5312b82]
- **Consent pages:** preference, subscribe, email confirmation, unsubscribe; single vs double opt-in. [8c1b383c08cf]
- **Metrics tab, profiles, metrics and insights tab, predictive analytics.** [059f73755fa8] [eb3ee2d82966]
- **Lists and segments, segment builder** (can receive marketing, what someone has done, location proximity, EU, properties, preview count, clone). [f24ba64fabd7]
- **Sign-up forms builder:** templates with micro-yes, styles (pop-up, flyout, full page, side image), button actions (submit, close, go to URL, subscribe via text, go to inbox), teaser, targeting and behaviours (show immediately or by rules, frequency, devices, click outside to close, audience, URLs, location, UTM, cart content). [4be0db20360f] [4d0639885e1a]
- **Flows:** triggers (added to list, checkout started, added to cart, viewed product, placed order, added to segment, date property, integration metrics), profile filters, actions (email, SMS, update profile property, add or remove from list, webhook, internal alert), time delays, conditional and random-sample splits, show analytics, skips. [07f1b027ac4e]
- **Flow templates:** Abandoned Cart Reminder (Checkout Started and Added to Cart versions), browse abandonment, post-purchase follow-up. [a0bdafa6ea40]
- **Email editor blocks:** image, text, split, button, divider, social links, spacer, table, product block (static or dynamic feed). Dynamic tags for footer. Event variable `{{ event.extra.checkout_url }}`. Preview and test with event properties. [66bb08b24b5c] [79cdac8bb86e]
- **Show/hide logic (logic builder)** for dynamic blocks. [9ba42019fe30]
- **Campaigns:** tags, send to / don't send to, per-campaign smart sending, UTM, saved templates and email library, campaign sequence builder with follow-up resend (48-hour minimum), local time zone send, determine recipients at send time. [5b2cad894e44] [6964a9fc308f]
- **A/B testing:** create A/B test (content or send time), winning metric, size distribution, test duration, automatic distribution in flows, experiments section. [659e9f913086] [b5c1274e5d10]
- **Reporting:** subscriber growth, opt-in sources, form reports, campaigns list sorted by revenue, dashboards > business review (previous period or previous year, message type breakdown, performance summaries, top performing), deliverability tab (score, recommended values), reports by inbox provider. [5d6743fc3f40] [41d10e199bc4] [3dca25bfe545]
- **SMS and push settings.** [4c7296971696]
- **Integrations directory (187):** Shopify, Gorgias, Recharge, Skio, Yotpo, Okendo, Judge.me, a loyalty app (probably Rivo), Meta Ads, Google Ads. [9ca8e23a01f3]
- **Outside Klaviyo:** Figma (design and slicing), GoDaddy (DNS example), Google Analytics, Triple Whale, Shopify analytics, an unnamed agency dashboard tool.

## 7. Examples and case results

All are examples from the agency's accounts, not promises.
- **Welcome flow, gumball.com (vending machines):** Figma-built, graphic placement "cannot be done in Klaviyo". Post-purchase: "your vending journey begins", "you made a great choice", expert machine tips, "the secret to vending success: location", machine setup checklist, plain-text service check-in, dynamic cross-sells; returning buyers get "Welcome back to the family. Your trust in us means the world." Logic: a profitable machine leads to buying more machines. Sunset: 10% unique code. [55898f20e161] [56d433c32a2b]
- **Abandoned checkout, Red Stick Spice:** Figma slices plus Klaviyo's dynamic cart table. [a0bdafa6ea40]
- **Campaign examples (other brands, shown in inbox):** Lounge "head-to-toe neutrals" collection; Brondell "over a billion gallons saved"; Ready Set Food blog on spotting food allergy signs leading to allergen-introduction products, and a bottom module "complete system plans 60% off" during a month-long sale; Evan Healy argan oil education; Tushy "3 reasons wet wipes are not your friend"; Absolut Mother's Day "serve one up for the moms who are selfless"; Rebel Rabbit "survive the holiday hustle"; Moment "up to 60% off sitewide, shop Black Friday deals" and an orange drink launch ("made for mornings", fights stress, boosts mood, enhances focus, limited stock). [826d4337358d] [783cb03489e3] [d70e0719ccfa] [3c10a64f1966] [7f637dd1902a]
- **July 4th inbox tour:** 3 Klaviyo-built emails (Regent Row, a spa, R Porter) vs Dispatch clients Felt Right (15% off summer sale, bold code "SUMMER15" before CTA, customer favourites with a CTA under each product, USPs at the bottom), Young Nails (rewards email with check icons; client for about 3 years) and a New York acupuncture clinic (bookings). No click or revenue numbers given. [92e649c06ecd] [82bb67e79aeb]
- **Design range file:** bold, natural, luxe (Kin Euphorics, Aura, Felt Right, a premium matcha brand, Craig Hill), playful (Young Nails, Privileged Shoes, Cloud 10 Beauty, Gumball, a pet brand, a dance brand) and educational (AeroPress, TruDiagnostic, Outwork Nutrition, Jasper, Milky Mama, Ease Cushion; "click rates absolutely skyrocket", no numbers). [92e649c06ecd]
- **List growth review:** 16,000 subscribers, +0.1%; +226 gained, -208 lost; new subscribers -27%, losses -4.6%; checkout 116 (-27%); pop-up 116 (-27%); form views about 10,000 to 8,000 (about -20%), 190 submissions, submit rate 2.19% to 2.28%. Verdict: traffic drop, not form failure. [d66d62f1a9cd]
- **Pop-up A/B test:** submit rate 3.11% to 4.29%; Klaviyo picked the winner after 32 days. [d66d62f1a9cd]
- **Campaign review (June):** top campaign $2,000, Father's Day restaurant-quality BBQ recipes; #2 "benefits of cooking at home" had more than twice the clicks but less revenue; weekly newsletters lowest revenue but among highest engagement. Order counts: #2 earned $300 more than #3 with 15 purchases vs 22; #4 had the most unique purchases. [ea472261103e] [7b7bba687f4a]
- **Business review, first month with a new client (May vs April):** email just under 40% of total revenue, +9%; attributed $84K; campaigns $43K (43.7K) +54%; flows about $40K, -16%; recipients +3.5%, unique opens +13.6%, open rate +9.8%, unique clicks +15.6%, click rate +11%, unique conversions +40%, conversion rate +37%, revenue per recipient +49%, AOV +17%. [41d10e199bc4] [8183b1fcc7d0]
- **Flow review:** open rate slightly down; unique clicks -7%; click rate -15%; unique conversions -6%; revenue -15%; AOV -15%. Welcome example $16K in May vs $20K in April would trigger a flow check. Skips 620 vs 190 delivered (fine for that client). Flow A/B: version A at 98% win probability, not significant, chosen anyway. [d2e68173f29a] [ac6fccd77bd7] [bfa3ffd83c16]
- **Deliverability tab (client):** open 62% (okay above 33%), click 1.71% (okay above 1.2%), bounce 0.67% (under 1%), unsubscribe 0.67% (recommended under 0.3%), spam 0.004%. By provider: Gmail and Verizon about 63% to 70% opens; Hotmail and Outlook 46% with lower clicks; G Suite high bounce and unsubscribe. [3dca25bfe545]
- **Dynamic block:** US free shipping over $100, rest of world over $150. [9ba42019fe30]
- **Loyalty birthday:** 250 points earned; balances 1,669 and 355. [9b7b4dd86442]

## 8. Mistakes the source warns about

1. Treating email as dead or optional; relying only on paid platforms. [465d3381b2a7]
2. Leaving attribution at defaults with transactional emails, bot clicks and Apple opens counted, which inflates email revenue. [1ce671434e00]
3. Leaving anonymous visitor tracking off, which starves browse and cart flows. [8796c9f1ffa6]
4. Using only custom fonts with no fallback. [b8afb62d37d6]
5. No branded sending domain or DNS records; source says even long-time Klaviyo users skip this. [a192f5312b82]
6. Using double opt-in and losing subscribers who never confirm (source view). [8c1b383c08cf]
7. Building touchpoints in silos; sending a first-order discount to a 5-order customer. [a084662e8ae4]
8. Sending campaigns to the whole list, or to lists at all. [d7c5cedcb3dd]
9. Keeping people who have not engaged in 2 years on the send list. [9720dfa509a1]
10. Splitting campaigns into too-small segments and halving shots on goal. [0ca859db0b00]
11. Using OR instead of AND for the "can receive email marketing" condition. [1d456b02f483]
12. Accepting Klaviyo's 3% "excellent" form badge as good enough. [ea0cb89619eb]
13. Leaving "click outside form to close" on; using side images; adding load delays; only checking desktop. [4bb4a381c989]
14. Showing the pop-up only on the homepage; showing it on the cart page; showing a non-stackable discount on a sale page; showing it to existing profiles. [4d0639885e1a]
15. Not A/B testing the form every month; testing design before offer. [ea0cb89619eb]
16. Sending the same campaign repeatedly instead of building a flow. [24b8079fe1fe]
17. Campaigns and flows hitting the same person within 24 hours, driving unsubscribes and spam complaints. [24b8079fe1fe]
18. Using Klaviyo default flow templates for content. [07f1b027ac4e]
19. Giving the welcome offer in email 1 and never mentioning it again. [65d6a163c4ce]
20. Having only the "Abandoned Cart Reminder" flow (which is really checkout) and no Added to Cart flow. [85117c7d0910]
21. Using the template's SMS-first split that delays email by hours. [fbfeb91636ec]
22. Browse abandonment without the added-to-cart filter; linking browse emails to the homepage. [909e75c1eb8d] [79cdac8bb86e]
23. Fixing post-purchase sends at 9 AM. [55898f20e161]
24. Skipping the proactive customer service check-in. [55898f20e161]
25. Accepting Klaviyo's default win-back delay without using your own repurchase data; 1-day gaps in win-back. [021057848a4f]
26. Continuing to pay for and mail unengaged profiles. [56d433c32a2b]
27. Skipping weeks of campaigns, then expecting Black Friday to work. [dbd9ab70c7db]
28. Committing to a cadence you cannot keep. [dbd9ab70c7db]
29. Sending only when there is a product or promo; not testing content types. [3c10a64f1966]
30. Announcing a promo at the start and end of a month-long sale only. [3c10a64f1966]
31. Launching a product without explaining why the subscriber should care; leaving benefits on the PDP and packaging only. [7f637dd1902a]
32. Over-polishing design and copy while the offer or product choice is wrong. [34710bc8ca91]
33. 10 messages in one email; paragraphs where icons would do. [945e9b8a355c]
34. Burying the value at the end of the subject line. [685553ea4865]
35. No CTA under each product; bullets instead of icons; hidden promo code; blurry or mismatched images. [82bb67e79aeb]
36. Never checking analytics, so broken pop-ups and flows go unnoticed. [5d6743fc3f40]
37. Repeating a low-click collection campaign because no one checked results. [5d6743fc3f40]
38. Killing high-engagement, low-revenue newsletters instead of reformatting them. [3c10a64f1966]
39. Judging deliverability by open rate. [3dca25bfe545]
40. Testing subject lines instead of content; changing 2 things at once; using open rate as the winning metric; using a 40% test group on a small list. [659e9f913086]
41. Looking only at campaign deliverability and ignoring flows. [3dca25bfe545]
42. Sending 2 separate campaigns where one dynamic block would do. [9ba42019fe30]
43. Integrating apps you do not use before the ones you do. [9ca8e23a01f3]

## 9. Caveats, conflicts and what is missing

- **DMARC p=none "always" conflicts with standard guidance.** The source says reject or quarantine sends anything the provider thinks is spam to spam. DMARC policy applies only to mail that fails SPF or DKIM alignment, not to content judged as spam. Gmail and Yahoo require a DMARC record for bulk senders, and p=none is the minimum they accept. A brand whose mail is fully aligned can move to quarantine or reject. Do not copy the "never" rule. `[web check: Google and Yahoo bulk sender requirements; DMARC alignment and policy guidance]` [a192f5312b82]
- **Single opt-in "always" is opinion.** Double opt-in is expected or required in some markets (for example parts of the EU). Card 8c1b383c08cf already softens it. `[web check: consent law for each market]`
- **Spam threshold said 3 ways.** Setup section: below 0.3%, ideally below 0.1%. Deliverability tab: "under 0.01%" (client at 0.004%). This may be Klaviyo's own stricter recommendation or a misreading of 0.1%. `[web check: Klaviyo's current recommended spam rate]`
- **Rate floors differ.** Presenter's minimum: open above 30%, click above 0.5%. Klaviyo's "okay" values shown: open above 33%, click above 1.2%. Presenter also says fixed benchmarks mean little without an audit. Keep both; do not average.
- **Unsubscribe rate:** Klaviyo recommends under 0.3%; the agency accepts 0.67% for more revenue. A trade-off, not a rule.
- **Channel order in abandonment flows contradicts itself.** Section on abandoned checkout: send email and SMS together or very close; do not use SMS-first. Section on multichannel: SMS first, wait 2 hours, then email. Card fbfeb91636ec frames it as a test. Test both. `[web check: SMS quiet hours and consent rules]`
- **Sunset filter logic.** Source says filters "opened zero times since starting this flow OR clicked zero times since starting this flow" so anyone who engages drops out. With OR, someone who opens but does not click still passes and keeps getting sunset emails. AND matches the stated intent. Test the filter before going live. [56d433c32a2b]
- **Header-only claims.** "3 to 4 campaigns a week", "2 welcome emails on day 0 in a 72-hour window", "14/30/60/90-day engagement tiers", "8% to 12% form target vs 1% to 3% standard", "7 content buckets", "91 campaign ideas", "Gmail AI inbox", gamification (spin-to-win, scratch-offs) and "separate desktop and mobile experiences" come from the export's summary block, not from the presenter. The body says: at least 1 campaign a week, test up from there, commit to what you can sustain (example 2); welcome email 1 immediately then 1-day gaps; 90/180/365-day tiers plus 14-day carve-outs, and 30 or 60 days only for repair; form above 9%; separate device forms "really not necessary". Cards [e6ffa2358b86] and [838c953697bd] carry the header claims; treat them as unverified.
- **Card corrections.** Card 059f73755fa8 says the checkout flow sends "about 2 hours later"; that was only an illustration, and the template default is 4 hours. Card 3c10a64f1966 is titled "Six campaign types" but the body lists 8 types (product or collection spotlight, benefit, content spotlight, education, weekly newsletter, cultural event, 4 promo types, new product launch). Card 021057848a4f says gaps "7 days and 5 days"; source said "7-day and 5-day". Card 8796c9f1ffa6 says list size helps "sending-limit warmup"; the source does not say why Klaviyo asks.
- **Image-only emails.** The source pushes fully sliced emails. It does not address accessibility (screen readers, alt text), image blocking, dark mode, load weight or Gmail clipping. Cards 5fde08efd3f8 and 92e649c06ecd flag this. `[web check: image-only email deliverability and accessibility guidance]`
- **Pop-up shown immediately on mobile.** Source says immediate load wins. It does not discuss Google's guidance on intrusive mobile interstitials or page speed. `[web check: Google intrusive interstitial guidance]`
- **Attribution-based revenue.** All revenue figures are Klaviyo-attributed (5-day or 3-day windows), not incremental. The 30% target and all case numbers depend on that. No holdout tests are shown.
- **Gmail and Yahoo one-click unsubscribe** is not mentioned. `[web check: one-click unsubscribe (List-Unsubscribe) requirement and Klaviyo's handling]`
- **Thin "how":** SPF, DKIM and DMARC record steps are a linked guide, not shown. SMS setup, push setup and compliance are skipped. No subject line or copy test results. No guidance on discount depth for win-back or sunset beyond "strong" and "exclusive". No flow benchmarks (revenue per recipient, conversion rate) are given. No list size or revenue thresholds for when predictive analytics become reliable.
- **Open rate usage.** Source says open rate is unreliable but still uses opens (with Apple opens excluded) in engaged segments and as a subject line signal. Consistent if the Apple filter is on.
- **Agency bias.** "Use Klaviyo", "design in Figma" and "hire a team" match what Dispatch sells. The Figma claim rests on side-by-side screenshots with no numbers.
- **Needs brand data for any real use:** AOV and margin (offer size), median and mean days between orders, consumption cycle, annual revenue band ($1M to $10M, under $20M, over $100K a month email revenue), list size and inbox provider mix, current form views and submit rate, traffic by source and country, SMS program status, subscription and loyalty apps, B2B customers, top objections, bestsellers, reviews, brand fonts. `[needs brand data: each item listed]`

## 10. Card index

- 465d3381b2a7: Set a defensible email revenue benchmark and KPI case
- 8796c9f1ffa6: Complete the Klaviyo–Shopify integration and sync settings
- 1ce671434e00: Configure smart sending and attribution windows
- b8afb62d37d6: Set brand defaults, fonts and fallbacks for email design
- a192f5312b82: Authenticate your domain: dedicated sending domain, SPF, DKIM, DMARC
- 6d8587217a67: Maintain sender reputation with bounce, spam and engagement thresholds
- 838c953697bd: Clean unengaged subscribers and use engagement-tiered segments
- 8c1b383c08cf: Configure preference pages and choose email opt-in deliberately
- a084662e8ae4: Map the customer journey before building flows and campaigns
- 059f73755fa8: Use Klaviyo metrics as flow triggers and personalisation filters
- eb3ee2d82966: Read a Klaviyo profile to decide segmentation and personalisation
- d7c5cedcb3dd: Organise profiles into lists and segments, and never campaign to the whole list
- 9720dfa509a1: Build the engaged prospect and engaged customer segments
- 49f85dfebaf9: Style campaign creative by segment learning
- e6ffa2358b86: Employ retention and account-level setup: where email sits in the 2026 lifecycle
- 1d456b02f483: Engagement windows as sliding retargeting filters
- bf989ee22bb1: Build prospect and customer segments by cloning one definition
- 3f50ca527fa4: Match offer intensity to engagement window
- 0ca859db0b00: Never send campaigns to the full list, and never to segments that are too small
- 07f1b027ac4e: Build filters so each flow only fires for the right lifecycle state
- 4be0db20360f: Micro-commitment first step in the pop-up form
- 4bb4a381c989: Form behavior settings that stop accidental opt-out loss
- ea0cb89619eb: Offer choice is the highest-leverage pop-up test
- 4d0639885e1a: Targeting and location rules for offer differentiation
- f24ba64fabd7: Master list plus engaged segments as the base setup
- 24b8079fe1fe: Campaigns versus flows, and stopping message overlap
- ef1cb30f5c95: Welcome series: trigger, filter and immediate code delivery
- 5fde08efd3f8: Design emails outside the ESP with image slices
- 66bb08b24b5c: Dynamic product feeds for emails
- b6185512bac6: Design Welcome Emails Outside Klaviyo, Export as Image Slices
- 65d6a163c4ce: Welcome Series Content Blueprint for DTC Brands
- 85117c7d0910: Trigger Abandoned Checkout on checkout started With Order Filtering
- fbfeb91636ec: Test email and SMS sequencing in abandonment flows
- f147a186a98d: Branch Abandonment Flows by Prospect vs. Existing Customer
- 79cdac8bb86e: Link Abandonment Emails Directly Back to Checkout
- a0bdafa6ea40: Use Klaviyo Templates Only For Dynamic Cart Tables
- 909e75c1eb8d: Fix Browse Abandonment Filters and Link to the Viewed Product
- 55898f20e161: Design Post-Purchase Flows Around First-Time vs. Returning Customers
- 021057848a4f: Time Your Win-Back Flow Using Actual Repurchase Data
- 56d433c32a2b: Build a Sunset Flow With a Segment Trigger and Profile Property
- dbd9ab70c7db: Set Campaign Cadence From Data, Not Ambition
- 826d4337358d: Product and Collection Spotlight Campaigns
- 783cb03489e3: Benefit-Focused Campaigns: One Benefit Per Email
- d70e0719ccfa: Use Content and Education Campaigns to Seed Purchase Intent
- 3c10a64f1966: Six campaign types to rotate in your email calendar
- 34710bc8ca91: Message and offer matter 10x more than copy polish or design
- 81300e87c081: Send campaigns to engaged segments only
- ba5c04225d61: Decide smart sending per campaign, not just at account level
- 5b2cad894e44: Set up a new-product-launch campaign in Klaviyo end to end
- 6964a9fc308f: Add a follow-up resend to catch non-openers
- 8c9297aaf4b4: Write copy that sells the click, not the product
- 945e9b8a355c: Write to one core message per email and cut fluff
- 7f637dd1902a: Lead with benefits framed for your specific customer
- 685553ea4865: Subject lines and preview text: under 50 characters, frontload the value
- 1cddc0a49ff8: Use persuasion levers: urgency, scarcity, social proof, curiosity gaps
- 92e649c06ecd: Design in Figma, not in Klaviyo's drag-and-drop
- 4410834af2cb: Structure each email section as header, subheader, body, image, CTA
- 82bb67e79aeb: Three visual must-do's: CTA near products, icons not bullets, clear promo code
- 5d6743fc3f40: Monthly Klaviyo analytics audit: list growth, campaigns, flows
- ea472261103e: Read open rate, click rate and placed orders as a diagnostic layer stack
- 7b7bba687f4a: Use revenue and order count together to catch high-AOV distortion
- d66d62f1a9cd: Diagnose a subscriber drop by separating traffic from form performance
- ced1f90d7686: Interpret Klaviyo's AB test statistics before trusting a result
- 41d10e199bc4: Read top-level business review to attribute email revenue and understand month-over-month shifts
- 7ac91a47ef79: Ensure every email adds value before it ships
- 8183b1fcc7d0: Monthly email business review: campaign revenue decomposition
- 489a0deaff01: Optimize for unique opens and unique clicks, not open rate and click rate
- dccf91db3e0a: Diagnose falling email metrics by which metric moved
- d2e68173f29a: Flow revenue review: traffic first, then the flow chain
- ac6fccd77bd7: Audit flow skip logic when a flow's revenue drops
- 659e9f913086: Run one high-leverage campaign A/B test per month
- b5c1274e5d10: Flow A/B tests with automatic distribution
- bfa3ffd83c16: Reviewing completed and in-progress A/B tests
- 3dca25bfe545: Monthly deliverability health check inside Klaviyo
- 98d43fdb4da1: Recover inbox placement by tightening the engagement segment
- 9ba42019fe30: Dynamic content blocks to merge segmented campaigns into one send
- 109f8c9de246: Trigger a winback from expected next order date
- 6818bdf85834: Use predictive CLV and churn risk in flow splits
- 4c7296971696: Build multichannel touchpoints into flows (email, SMS, push)
- 9ca8e23a01f3: Integrate ecommerce apps to drive flow triggers and segmentation
- 9b7b4dd86442: Trigger a birthday flow using loyalty app point properties
- 03624b075480: Use dynamic blocks to personalise shipping thresholds and offers in one send
