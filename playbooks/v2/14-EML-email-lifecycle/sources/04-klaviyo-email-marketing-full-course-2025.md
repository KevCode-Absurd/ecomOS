# Klaviyo Email Marketing FULL COURSE 2025

source_id: 1gAs1Y6DDO4ld3V07pv7EQ4Hq585FJEwm  |  folder: /14-EML-email-lifecycle  |  cards: 82  |  words: 46,643  |  type: course (single long YouTube transcript)

credibility: An unnamed owner of an email agency for DTC ecommerce brands. He says he has done email for 5 years, worked with 30+ brands, helped them make "over 300 million" in revenue, and consults for other agencies. He sells done-for-you email work. The video ends with a pitch: "at least 20% more revenue in 60 days or your money back." Evidence is his own client dashboards (revenue share and growth figures, no sample sizes, no controls) plus live walkthroughs in a demo Klaviyo account that has no Shopify store connected. So several screens (Shopify metrics, revenue filter, bounce type) could not be shown. Most numbers are his working defaults, not tested benchmarks. The transcript is auto-generated and garbles names ("Cayo", "clay", "CFO" = Klaviyo; "Sent Lane" = SendLane; "DeMark" = DMARC).

date signals: Recorded in 2024 (it cites "the new Google rules which came out in 2024", builds a calendar for August 2024, and says Klaviyo was running UX tests in 2024 so screens may differ). The title says 2025. Google Domains is described as "now taken over by Squarespace". Klaviyo menu paths, template names, the "trigger filter" feature (called "new") and A/B test options all date to 2024. `[verify UI]` on every Klaviyo step. `[web check: current Gmail and Yahoo bulk sender rules, current Klaviyo sending domain record types]`.

scope note: The library header routes paid media and Meta setup to 06-MEA and site builds or CRO audits to 07-LPG (older folder numbers). SMS is only touched as a signup step. Skip the agency pitch and demo account creation.

header vs transcript: The library header (written when the source was filed) claims 3 things the speaker never says: (1) a "custom JavaScript snippet" is needed to track Added to Cart; (2) DMARC should move from p=none to quarantine or reject; (3) Yahoo rules. In the transcript, the Added to Cart point is only about picking a flow template whose trigger is Added to Cart. Do not cite this source for the snippet or the DMARC escalation. `[web check: whether Klaviyo's Shopify integration now sends Added to Cart natively or needs an onsite snippet]`.

## 1. What this source is for

It gives an operator a full Klaviyo build for a DTC store, end to end. Set up the account and sending domain. Build a desktop and a mobile popup. Build 8 core flows with triggers, filters, delays and email angles. Plan a campaign calendar with a discount cap and a send frequency. Design and slice emails. Build engagement, buyer and hygiene segments. Write copy. Run A/B tests judged on placed order rate. It is strongest on flow structure, popup settings and segment definitions. It is weak on deliverability numbers and has no evidence beyond the presenter's own clients.

## 2. Principles

1. **Email's job is LTV and AOV, next to paid ads, not instead of them.** Goals: grow the list fast, turn traffic into a first buyer, turn a first buyer into a repeat buyer. Evidence: agency client dashboards only (see section 7). [0944381047ee]
2. **Less friction means more conversion.** The presenter applies this everywhere: popup fields, input colour, auto-applied codes, simple design, easy words. Stated as a rule of thumb, no data. [72945bee8a3a] [6e550d63490a] [17b5705e3605]
3. **The offer drives signups more than design does.** Weak offer, and no setting will save the form. Condition: popup capture. Evidence: presenter's testing, no numbers. [72945bee8a3a] [9adb06995af6]
4. **Train subscribers to open your emails.** Keep the code off the success page so welcome email 1 earns the open. Presenter's reasoning: low opens on email 1 hurt deliverability for the whole system. Not tested in the source. [d319ea40cf4e]
5. **Each flow must stop when the person moves to the next journey stage.** Stages: active on site, viewed product, added to cart, checkout started, placed order. Filters exit people so they do not get 2 overlapping flows (spam risk). [9da5ac313720] [dfc548f661d2]
6. **The later the journey stage, the shorter the first delay.** Site abandon waits longest, cart and checkout the least. Presenter heuristic, always to be split tested. [3638d8afef7a]
7. **Hold discounts back in abandonment and winback flows.** Give trust content first. Put the first discount near email 4 or 5, always with a real deadline. Reason given: people who get a code early learn to wait for codes. Presenter opinion. [5aad4467fa44] [fac642b0957b] [a5998cc28759]
8. **Urgency must be real.** Use a dynamic code or a code that truly expires. Never "WELCOME10" with a fake deadline. [a69de45ff438] [6e89698da8b5]
9. **Plain text from the founder closes sequences well.** Presenter says plain text has better deliverability, lands in the primary tab more often, and feels personal. He uses it for the last welcome email, the last cart or checkout email, post-purchase email 1, winback deadlines and the whole sunset flow. No numbers given. [a69de45ff438] [ebb2548fab18]
10. **Smart sending off in flows, on in campaigns.** Flows carry the high-intent revenue and must not be skipped. [b837f7435caf] [a891648996f4]
11. **The first-to-second purchase is the hardest step.** Once a person has bought 2 or 3 times, more buys come easier. Post-purchase and winback flows exist to close this gap. Presenter framing, not measured. [f6a8fc1ece5f]
12. **Protect the brand from discount fatigue.** At least 5 non-discount emails per discount email; the presenter uses 10 to 1 and at most 1 discount email a month outside Q4. [81f4514ba7d3]
13. **Set send frequency from data, not gut feel.** Revenue tier gives a start; open rate and unsubscribe rate decide whether to add or cut sends. [a6116076fc6e]
14. **Email design is a conversion tool.** Short emails, a visual hierarchy toward 1 CTA, visuals instead of paragraphs, and an above-the-fold area with headline, support and CTA. [6e550d63490a] [73c535d638e2] [d1327991a91c]
15. **Rather lose unengaged subscribers than keep them.** They cost money (you pay per profile) and are more likely to hit the spam button. An unsubscribe is better than a complaint. [c57d2fe2264a] [171bd57ff251]
16. **Judge tests on placed order rate or revenue, then click rate, then open rate last.** Presenter has "seen it a lot of times" that the best open-rate send time is not the best order time. [5d7c84dc41ce] [eed1632440b9]
17. **Test the big levers and tests you can reuse.** Top flows and their first 2 to 3 emails; send time and content structure in campaigns. Skip one-off campaign subject line tests and small-store button colour tests. [c61791a6cbeb] [8cab23f94038] [97bfd09fd8e1]
18. **Copy: one message, easy words, real value.** 5th grade reading level, cut 20 to 30% when read aloud, personality, provide value first. [c5f693b5c277] [618c17167140] [2b0c87a53512]
19. **Templates are starting points.** Klaviyo's default flows "just not high converting"; build your own and test what fits the brand. [fd7d4c80cdb7] [96c06aef939a]

## 3. Procedures

### 3.1 Pick the software
1. Use Klaviyo (presenter's choice for most clients) or SendLane (newer, "best support in the industry"). He says these are the "only 2 correct answers". [fc0425a31c0f]
2. Check these abilities: easy setup and support, signup forms, flow builder, campaign builder, email editor, segmentation data, A/B testing. `[web check: current pricing and features]`

### 3.2 Account setup `[verify UI]`
1. Sign up. Business type: consumer goods, sells online. Connect the Shopify store URL. Enter contact count, business address, sender name and sender email. Pick email only, SMS only, or both. Activate by the email link. [fc0425a31c0f]
2. Main list: keep the default name "Newsletter" (or rename).
3. Opt-in: single or double. Double sends a confirmation email first: better quality, fewer subscribers (fewer open, fewer click confirm). Presenter picks single opt-in because his segments send only to engaged people and suppress the rest later. Condition: only if you will run engagement segments and a sunset flow. `[needs brand data: legal market; double opt-in may be required in some EU countries]` `[web check: GDPR opt-in rules by country]`
4. Dedicated (branded) sending domain. Presenter calls it "basically mandatory in 2024" under Google's rules.
   - Settings > Email > Domains > Branded sending domain > Add.
   - Enter the root domain. Keep the default subdomain "send" (send.yourdomain.com). Keep routing on Dynamic.
   - Pick your DNS provider (examples: GoDaddy, Google Domains now Squarespace).
   - At the DNS host add the records Klaviyo shows. In the demo: 4 NS records with host "send" (values ns1 to ns4 at Klaviyo) and 1 TXT record with host "@".
   - Back in Klaviyo, tick the acknowledgement that you may need to limit sends to engaged recipients for 2 to 4 weeks, then Activate.
   - Wait until status changes from "In progress" to "Active" before sending.
   `[web check: Klaviyo now may use CNAME records; the library header says "CNAME/NS"]`
5. DMARC record (also "mandatory" under the 2024 Google rules, per the presenter).
   - Host `_dmarc`, type TXT. His own live record reads roughly `v=DMARC1; p=quarantine; pct=90; sp=none` (the transcript is garbled: "p is quarantine p is 90 SP is none").
   - Or use a free "DMARC record generator": enter the domain, pick policy none (the generator's "reporting mode"; the presenter repeats this as the start), set an address for aggregate reports and for forensic failure reports. Use a separate inbox such as dmarc@yourdomain.
   - Add the TXT record it outputs at host `_dmarc`.
   - The source never says when to move from none to quarantine or reject. `[web check: current Gmail and Yahoo DMARC and spam-rate requirements]`
6. Smart sending: Settings > Email > Sending preferences. Presenter uses a 16-hour window (a profile that got any email in the last 16 hours is skipped). Can be set to other values, such as 8 hours. [b837f7435caf]
7. Attribution: keep 5 days, last interacted email. Touch points: "opened or clicked email, excluding Apple privacy opens" (Apple Mail privacy auto-opens would otherwise earn revenue credit). SMS window: keep 1 day. Push: 5 days (they never use push). Save.
8. Data: turn on anonymous visitor tracking (activity before a person is identified is backfilled once they become a profile).
9. Other: brand the consent pages (preference page, subscribe page, confirmation page if double opt-in, unsubscribe page).
10. UTM tracking: turn on auto-add UTM parameters to links. Save.
11. Brand library: upload the logo, set brand colours, pick fonts. Google Fonts and Adobe Fonts can be imported; always set a web-safe fallback (e.g. Arial) because not every app shows custom fonts. Presenter never uses header links under the logo. Klaviyo auto-fills social links from the site; check them.

### 3.3 Build the desktop popup `[verify UI]`
Preconditions: pick the offer first (section 3.5). [72945bee8a3a] [d124c18b882e]
1. Signup forms > browse templates > type Popup > category "Collect emails". Pick a template. Name it. Pick the list (Newsletter). Turn the teaser toggle on. Create.
2. Targeting and behaviour > Timing: change "immediately" to "based on rules". Never show on page load ("conversion killer").
3. Desktop rules: exit intent + time delay + scroll depth.
   - Delay: 4 to 10 seconds; presenter default 6 seconds ("one of the best settings for most brands").
   - Scroll: 40 to 80% range to test; presenter uses 50 to 60%, example 60%. Check your analytics for how far people scroll.
   - Leave "only display if all selected conditions are met" OFF (OR logic, wider audience). He never uses AND.
4. Frequency: after close, show again after 5 days (default); he often uses 3. Range 3 to 5 days by niche and how often people come back. Tick "don't show again if the form was submitted or the go-to-URL button was clicked".
5. Devices: desktop only. Turn on "click outside form to close" on desktop.
6. Targeting: keep "don't show to existing Klaviyo profiles".
7. URL exclusions: the cart page, /wholesale, checkout. Reason: a shopper there is about to buy; a discount is wasted and they join the list on purchase anyway. (Card [d124c18b882e] also lists paid-traffic landing pages; the transcript does not.)
8. Location by IP: show only to countries you ship to, or exclude others.
9. Design:
   - Side image with alt text.
   - Headline states the offer: "Unlock 10% off your first order" (capitalised). Avoid "sign up" and "subscribe".
   - Delete the subheadline "Sign up for special offers and updates" (wasted space).
   - Placeholder text: "Enter your email here".
   - Input field fill: light grey so it stands out from a white form.
   - CTA text: "Claim my discount now" (alternatives: "Get my discount now", "Claim my deal"). Colour that contrasts with form and site (black in demo). Height 54 to 70 px. Bigger buttons get more clicks "with emails but also with the sign-up form", within reason (150 px is too much).
   - Legal microcopy ("By signing up you agree..."): keep where required (EU, GDPR); removed for a US store. `[needs brand data: markets and legal counsel]`
   - Secondary option as a button: "No thanks, I'd rather pay full price". Add about 10 px padding between it and the CTA. Presenter cites "research" that 2 options, 1 attractive and 1 not, lift signups over 1 button.
   - Hide the X close: set size to about 5 and colour to the background. He calls it an "ethical debate" and only does it because the "no thanks" button already closes the form. `[needs brand data: owner's view on dark patterns]`
   - Add the logo. Compress every image (tinypng.com; logo 21 KB to 14 KB, 33% less).
   - Optional extra step for phone or personal details. The demo keeps 1 step.
10. Success page:
    - Same image and logo as the opt-in step.
    - Do not show the code. Headline like "Your discount is on its way. Check your inbox for the confirmation with your discount code."
    - Add a bold line: "Didn't receive an email within 5 minutes? Check your spam folder." New subscribers often land in spam (Gmail in 2024 is strict), and this line saves support tickets.
11. Teaser: shape rectangle, circle or corner; text "Save 10% now"; show before and after the form; high-contrast fill (black, transparency 0, white bold text, same font). Check it does not clash with chat widgets, loyalty popups or promo bars. [f7f5d18ebe32]

### 3.4 Build the mobile popup `[verify UI]`
1. Exit the desktop form without publishing. Clone it, name it "mobile". Set devices to mobile only. Rename the original "desktop". [f932973235fb]
2. Timing: same delay and scroll, but untick exit intent (unreliable and annoying on mobile).
3. Sizes in the demo: input text 16 to 20 px; input height 50 to 70 px; CTA height 70 to 80 px; CTA text 24 px; microcopy 20 px. Add padding above the CTA and between elements so thumbs do not mis-tap.
4. No side image on mobile.
5. Teaser: change to a small circle or corner; shrink text; check it does not cover other widgets.
6. Success page text: 22 to 24 px; reduce side padding.
7. Publish both forms.

### 3.5 Choose and test the popup offer
1. Offer options: % off, % off above a spend, $ off, $ off above a spend, free shipping, mystery discount (revealed only in welcome email 1; presenter uses it "a lot" for a good submit rate). [72945bee8a3a]
2. Floor: under 10% off is "generally not effective"; 5% only works for very high AOV products.
3. At AOV $200, 10% off and $20 off cost the same; $20 "most likely" feels bigger. Test it. Rule of thumb from the source: AOV of $200 or more, $ off tends to beat % off.
4. Extra offers to test: BOGO, BOGO 50% off, free gift with purchase, free digital product, % off a subscription, cashback, early access to a sale (strong at Black Friday). [c09dafafbc67]
5. Judge the offer on 3 numbers together: form submit rate, welcome flow placed order rate and AOV, and welcome flow attributed revenue. See the client example in section 7. `[needs brand data: margin per offer, AOV]`

### 3.6 Micro-yes step (test, not default)
1. Clone the email opt-in step, rename it "micro", move it in front. [52d1b13d3d6e] [45fac68dfd23]
2. Headline as a question: "Do you want 10% off your first order?" Remove the input field. CTA: "Yes please". Keep the "No thanks, I'd rather pay full price" microcopy.
3. "Yes please" submits and shows the email step.
4. A/B test with and without. Presenter: most brands get a signup spike; some do better without.

### 3.7 Flow builder basics `[verify UI]`
1. Flows > Create flow > Build your own (or pick a template by goal). Klaviyo templates are "better than nothing" but "just not high converting". [fd7d4c80cdb7]
2. Pick the trigger. Recommended list shows Checkout started, Added to list, Viewed product, Placed order, Added to cart, Added to segment, Date property (birthday, first-purchase anniversary). "Your metrics" shows Shopify metrics (cancelled, fulfilled, ordered product, placed order), Klaviyo metrics (subscribed to SMS, subscribed to back in stock) and API metrics (active on site, added to cart, viewed product, quiz or review app events).
3. Add profile filters (e.g. "Placed order zero times since starting this flow"). Conditions can count events, set time windows, and filter on the exact item bought.
4. Confirm and save. The trigger cannot be changed after this. To change it, clone the flow and pick a new trigger. Filters can still change. [dfc548f661d2] [e0cf57ece0ac]
5. Actions: email, SMS, profile property update, webhook, internal alert, time delay, conditional split.
   - Profile property: e.g. set "in welcome series = true" at the start and "false" at the end, so campaigns can exclude people in the welcome flow (some brands want this).
   - Time delay: minutes, hours, days; delay until a set time of day; account time zone or recipient local time; only on chosen weekdays (e.g. welcome email only on Monday).
   - Conditional split: yes and no paths. Use "random sample 50%" to A/B test 2 whole flow strategies.
6. Per email: subject line, preview text, sender name, sender email. Untick "Skip recently emailed profiles" (smart sending OFF). Tick UTM tracking. Save. [b837f7435caf] [3247c58dc8b5]
7. Manage flow: name, tags, flow history, Show analytics with custom date range, "Update action statuses" to set every email to live, manual or draft at once. [e0cf57ece0ac]
8. Add past profiles (Manage flow): enrol people who would have qualified before the flow went live. "At the beginning" or "throughout the flow" (placed where they would be now). Not allowed on flows with dynamic coupons, so use a static code if you need this. [a704ce6294f2]

### 3.8 Welcome series
Trigger: Added to list "Newsletter". Template: Klaviyo "Standard welcome series" (others exist: unique discount with reminder, SMS discount, customer vs non-customer, final email discount). [6e89698da8b5]
Profile filters: Placed order = 0, Checkout started = 0, Added to cart = 0, each "since starting this flow". Optional: Viewed product = 0 and Active on site = 0; the presenter usually leaves these out because site and browse flows are short and early. [dfc548f661d2]
Goal: deliver the code, build trust, get the first purchase.

| # | delay after previous | content | notes |
|---|---|---|---|
| 1 | none | Deliver the discount code | The promise from the popup |
| 2 | 1 day | Brand story, behind the scenes | Founder personal note "really does well"; origin, mission, what sets you apart |
| 3 | 1 day | Bestsellers | Max 3, maybe 4 to 5 by brand; 1 if single hero product. Unique features, benefits, end result |
| 4 | 2 days | Reviews, UGC, press | Reviews that name the subscriber's pain point and how the product solved it. Not "highly recommended, great company". Reader is comparing you with about 3 competitors |
| 5 | 2 days | Us vs them, USPs | Make the comparison easy for them |
| 6 | 2 days | Route A: discount reminder, expires in 48 h. Route B: new or bigger offer (e.g. $ off a bundle) with a 48 h deadline; then email 5 carries the 48 h urgency | Transcript says "10% in the form, you can now use 50% off"; likely 15%, unclear. Test the 2 routes |
| 7 | 1 day | "Discount expires in 24 hours", plain text from the founder | Better deliverability, personal |

- Every email reminds the reader of the code. Every email has its own angle.
- Klaviyo default for comparison: email 1, then 3 days (12 pm) email 2, then 4 days (12 pm) email 3. Presenter says it will convert but is slower than his plan.
- Test sender name: founder name ("Name from Brand") vs brand name. Keep the sender email the same in all flows and campaigns. [3247c58dc8b5]

### 3.9 Site abandonment
No Klaviyo template; build it. Presenter says many brands miss this flow for that reason and that it gets "great results" (no numbers). [b0f7b82a2bb3]
1. Trigger: Active on site (API metric). Audience: visited but viewed no product (home page, blog).
2. Profile filters: Placed order = 0, Checkout started = 0, Added to cart = 0, Viewed product = 0, since starting this flow.
3. No trigger filter needed.
4. Delay 1 to 4 hours before email 1. A/B test 1 h vs 4 h, then narrow.
5. 1 email only (early, low intent). Act as a shop assistant: "Is this what you're looking for?" Link to collections (e.g. men's, women's for fashion) or to specific products or bestsellers for small catalogues.
6. A/B test collections vs bestsellers. Goal: a product view.
7. Smart sending off, UTM on.

### 3.10 Browse abandonment
[5aad4467fa44]
1. Trigger: Viewed product (Klaviyo "Browse abandonment" template).
2. Filters: template has Checkout started = 0, Placed order = 0, Has not been in this flow in the last 30 days. Add by hand: Added to cart = 0 since starting this flow.
3. Optional trigger filter to make product- or collection-specific versions. [bccb578fdd8b]
4. First delay: template 2 hours. Test roughly 1 h vs 3 h, then narrow (e.g. vs 2 h).
5. Email 1: "See something you like?" reminder of the viewed product.
6. Email 2, 1 day later: reviews, UGC, press for that product.
7. Later emails: brand story, product USPs. Make reviews and USPs product-specific with conditional splits or separate flows.
8. Discount only from email 4 or 5.
9. Length: typically 4 to 6 emails. The presenter did not build it out in full; angles follow the welcome series.

### 3.11 Cart abandonment (Added to cart)
Key warning: Klaviyo has no "checkout abandonment" template, but several "abandoned cart" templates (e.g. "Abandoned cart reminder", the Shopify "standard email and SMS") trigger on **Checkout started**. Those are checkout flows. "This is where a lot of brands go wrong." Pick the template whose trigger is Added to cart and check it. [fac642b0957b]
1. Trigger: Added to cart.
2. Filters: Checkout started = 0, Placed order = 0, has not been in this flow in the last 7 days (template). Presenter prefers 14 days; weekly repurchase products can keep 7 or less; long repurchase gaps can go higher. `[needs brand data: repurchase interval]`
3. Remove the template's SMS branch if you do email only.
4. First delay: template 4 h is "quite long". Use 30 minutes to 2 hours; test 30 min vs 2 h.

| # | delay | content |
|---|---|---|
| 1 | 30 min | Short reminder: "You added this to your cart. Want to finish?" (e.g. shopper on a bus had to get off) |
| 2 | 1 day | Reviews, UGC, press. Product-specific reviews beat store-wide ones; "mandatory" for big catalogues, worth testing for 1 hero product |
| 3 | not stated | Objection handling: why might they not finish? Address it |
| 4 | 1 day | Specific product or brand USPs |
| 5 | 1 day | First discount, X% off, 48 hours only |
| 6 | 1 day | 24-hour deadline |
| 7 to 8 | not stated | Route A: bigger discount, if margins allow. Route B: plain-text founder email, "we extended the sale for you, 24 hours only" |
| 9 | optional | Plain-text extended sale after route A |

- No code in emails 2 to 4. A discount without urgency gives no reason to buy now.
- Typical length 6 to 8 emails. It could run 14 to 20, but watch spam complaint rate, unsubscribe rate and open rate. [fac642b0957b]
- Smart sending off, UTM on in every email (the clone step resets nothing; check each email).

### 3.12 Checkout abandonment (Checkout started)
[393737091e3e]
1. Clone the cart flow, name it "Abandoned checkout", set the trigger to Checkout started in the clone dialog.
2. Remove the "Checkout started = 0" filter. Keep Placed order = 0 since starting this flow and "not in flow last 7 days".
3. Same structure. Rewrite for checkout objections. Example: the shopper saw a $10 shipping fee. Instead of 10% off (at AOV $200 that costs at least $20), offer free shipping: lower cost, higher conversion in the presenter's view. `[needs brand data: shipping cost, AOV, margin]`
4. Delay: the source does not give a separate number; the clone keeps the cart timing. Card [3638d8afef7a] adds "shortest delay", which the speaker did not say.

### 3.13 Post-purchase
[9f9c84a1b824] [d4ea5342470c] [3da6d6371379] [c17894672b54] [0a935c9bd091]
1. Template: "Customer thank you" (better base than the "post-purchase" template). Trigger: Placed order.
2. Add filter (not in template): Cancelled order = 0 times since starting this flow.
3. Optional trigger filters for product- or collection-specific versions.
4. Template default for comparison: 1 day, 9 am, 1 email, with a split on "Placed order = 1 over all time" (first-time vs repeat).

| # | delay | content |
|---|---|---|
| 1 | 30 min | Plain-text thank you from the founder or team. Split: first-time vs returning buyer, acknowledge which. Reduce buyer's remorse (worst in the first 24 to 48 h). Line: "We're preparing your order; you'll get a shipping message and we'll keep you updated." Soft cross-sell line: "Want to add something? Click here and we'll ship it together." |
| 2 | 2 days (or 1) | Merge paths. Build excitement: how to use the product. Future-pacing lowers remorse and support tickets. Split by product bought if you sell different types |
| 3 | 10 days | Introduce the loyalty program (points, discounts on next order). Delay depends on shipping time: send after they have the product. Connect the loyalty app to Klaviyo |
| 4 | 3 days | Ask for a review. Optional thank-you discount code (even non-reviewers get a code, a soft cross-sell) |
| 5 | 7 days | Cross-sell with discount (optional if margins are tight), 48-hour deadline |
| 6 | 1 day | 24-hour deadline, plain text from the founder |

- Why 30 min, not instant: Shopify's transactional order confirmation fires at once; do not bombard. [d4ea5342470c]
- Split further if you like (e.g. 4+ orders = VIP content).
- Returning buyers may skip emails 2+; presenter merges paths and sends both the same.
- Review apps: if you use a dedicated review tool (transcript "Kendo", probably Okendo; card [0a935c9bd091] says Judge.me), presenter prefers a separate review flow on that tool's triggers.
- 3 goals in 1 flow: cut remorse, get loyalty sign-up and a review, get the next order.

### 3.14 Customer winback
[4bfa7e9cadf3] [a5998cc28759]
1. Template: Klaviyo "standard winback". Trigger: Placed order, then wait X days. Template X = 75. Set X from your buying cycle in Shopify data (e.g. 40 or 90). A/B test it. `[needs brand data: median days between order 1 and order 2]`
2. Filter: Placed order = 0 since starting this flow.
3. Use Add past profiles, "throughout the flow", so you do not wait 75 days for the first send (needs static codes if the flow has a discount).

| # | delay | content |
|---|---|---|
| 1 | X days after order | "It's been a while." New arrivals or specific collections. No discount |
| 2 | 3 days (template 15 is too long) | Reminder. No discount |
| 3 | 7 days | Discount, 48-hour deadline |
| 4 | 1 day | 24-hour deadline, can be plain text |
| 5 | about 2 weeks | Second, bigger discount, 48-hour deadline |
| 6 | 1 day | 24-hour deadline, plain text |

- Use long gaps: lapsed buyers are less engaged and complain faster.
- Presenter: "a really important flow to A/B test a lot", mainly to bring first-time buyers back.

### 3.15 Sunset flow
[c57d2fe2264a]
1. Template: 1 of 2 Klaviyo sunset templates. Trigger: added to the Unengaged segment (section 3.20; he uses the 120-day version).
2. Goal: an open, not a sale. Low open rates are expected.
3. All plain text.
4. Email 1: "You haven't opened our emails in a while. Still interested? If not, click here to unsubscribe."
5. Emails 2 and 3: the highest discount you can give plus "clickbaity" subject lines.
6. At the end, for people who opened nothing: profile property update "unengaged = true". Build a segment on it and suppress.
7. No delays are given for this flow.

### 3.16 Campaign setup `[verify UI]`
1. Campaigns > Create campaign. Name, date, channel (email, SMS or push). [a891648996f4] [ebb2548fab18]
2. Recipients: send to engaged segments, not the whole Newsletter list. Add the default exclusions (section 3.21).
3. Smart sending ON (99.9% of campaigns). UTM tracking ON.
4. Content: subject line, preview text, sender name, sender email.
5. Editor: drag and drop for most; text only "every now and then" (personal, better deliverability); avoid HTML ("almost guaranteed" rendering issues on some app or browser).
6. Review screen: check recipients, smart sending, subject line. Schedule or send.

### 3.17 Build a monthly campaign calendar
[85157d54ac6e] [bdb13d54947e] [23ed2f50d61a]
1. Pick a tracker: Notion (past), Airtable (now), ClickUp, Monday, or a Google Sheet. What matters: consistent use, everything logged, clear for everyone.
2. Set frequency and send days (section 4).
3. List key events and holidays, including niche days (nationaltoday.com). Use only those that fit. Not every holiday needs a discount; a mention may do.
4. Pick value-based emails that fit the season (a fall skincare tips blog fits October, not May). Two routes for blog emails: summary + link to the full blog, or summary + link to products in the blog. Test both. No blog? Research a useful topic on Google and write around it.
5. Add company events: back in stock, launches (better as a sequence), gift guide before a holiday.
6. Fill blank slots from the 7 buckets: UGC, reviews, a common problem your product fixes, a niche myth busted and tied to a product.
7. Optional sketch: download a blank month from blankcalendarpages.com, drop it in Miro, then move it to the tracker.
8. Check the mix: no 2 salesy emails in a row; follow a sales email with a value email.

### 3.18 Email design and build (Figma to Klaviyo) `[verify UI]`
[f20df437e0c5] [8f1c460f5eed] [17b5705e3605] [046d714ac94c] [46ef575d23c2]
1. Design in Figma from a block library (the agency has about 25 header layouts, plus review blocks, product blocks like zigzag and 2x2, and body blocks like checklists). Apply brand fonts and colours.
2. Pick a visual hierarchy: Z (zigzag), inverted triangle or F. [73c535d638e2]
3. Above the fold: attention headline, supporting image or text, CTA button. Put the code here in promo emails. [d1327991a91c] [46502d7fa9bc]
4. Max 3 to 4 products per email. Add a universal footer with category links.
5. Slice the design (Figma: switch Frame tool to Slice). One slice per section: hero, section title, each product, CTA, footer. Leave short text out if you will rebuild it as live text.
6. Export PNG or JPG. Compress (tinypng.com; alternatives Squoosh, iloveimg.com).
7. In Klaviyo: open the campaign, edit email. Delete default blocks except the unsubscribe block (mandatory).
8. Set styles: text 18 px desktop, at least 16 px mobile, line spacing 1.5, alignment by brand (demo: centre).
9. Upload slices in order (duplicate block, replace image).
10. Every image: alt text (shown if images fail; inbox providers read it), and a link to the most specific page (collection or product, never home page).
11. Auto-apply the code in links (Shopify pattern shown): `https://domain.com/discount/CODE?redirect=/collections/handle`. Test each link in a browser.
12. Block padding: about 20 px top and bottom; where blocks stack, pad only the bottom.
13. Rebuild short text as live text in the brand font (more live text helps deliverability). Paste through the source code view to avoid formatting issues. Match colours with a colour picker.
14. Save the footer as a universal block (edit once, updates every email).
15. Preview desktop and mobile. If a text block keeps desktop side padding on mobile, turn on "full width on mobile".
16. Check email size. Demo: about 35 KB, "not at risk of clipping in Gmail". `[web check: Gmail clipping threshold]`
17. Send a test to yourself. Check links, padding and look on phone and desktop. Then schedule.

### 3.19 Engaged, buyer and behaviour segments `[verify UI]`
Audience > Lists & segments > Create > Segment. Clone and edit instead of rebuilding. Segments are computed in the background. [ff7571c5eb99] [7ccc6c565f86] [b97e06f650c6] [14037b197111]

| segment | definition (all include "can receive email marketing") |
|---|---|
| Engaged 120 days | Placed order ≥1 OR Checkout started ≥1 OR Added to cart ≥1 OR Viewed product ≥1 OR Active on site ≥1 OR Opened email ≥1 OR Clicked email ≥1, all in last 120 days |
| Engaged 90 / 60 / 30 (also 200, 14, 7 optional) | Clone and change the window. Minimum set: 30, 60, 90, 120 |
| Engaged, email only (optional) | Opened or clicked in the window |
| All buyers | Placed order ≥1 over all time |
| First-time buyers | Placed order = 1 over all time |
| 2x buyers | Placed order = 2 over all time |
| 3x+ buyers | Placed order ≥3 over all time |
| Non-buyers | Placed order = 0 over all time |
| Abandoners, no purchase | (Checkout started ≥1 OR Added to cart ≥1 in last 90 days) AND Placed order = 0 in last 90 days. Use for a "one final chance" campaign |
| Window shoppers | (Viewed product ≥2 OR Active on site ≥2 OR Clicked email ≥2 in last 30 days) AND Placed order = 0 over all time. Raise to 3 or 4 if the segment is big. Feeds a window-shopper flow |
| VIP | Placed order ≥4 over all time OR Revenue ≥ about 4x AOV over all time (AOV $50 gives $200). Some brands use 2x AOV and 2 orders, or last 12 months only |

- Presenter includes site activity in "engaged" because someone can ignore email but still shop the brand.
- Other builder conditions: subscribed vs never subscribed (a buyer can get post-purchase flows without opting in to marketing), proximity to a postal code (e.g. 20 miles, regional promos), in a list, in the EU or US (GDPR), profile properties, predictive analytics such as expected next order date (needs Shopify).
- Unused segments move to "Inactive segments" after 45 days and must be reactivated. [ff7571c5eb99]
- `[needs brand data: AOV, order counts, list size per segment]`

### 3.20 Unengaged segments and suppression
[171bd57ff251]
1. Unengaged 120 days: can receive email marketing AND Placed order = 0, Checkout started = 0, Added to cart = 0, Viewed product = 0, Active on site = 0 AND Opened email = 0 AND Clicked email = 0, all in last 120 days, AND Received email ≥6 in last 120 days.
2. Why all site events: "Active on site" sometimes does not fire, so the extra events stop false positives.
3. Why "received ≥6": people must have had a chance to open. 6 fits about 3 campaigns a week (2 weeks of sends). Trial and error; check segment size. The demo used 5.
4. Clone for 90, 60, 30, 180 and 365 days.
5. 365-day version: email metrics only: Opened = 0 AND Clicked = 0 in 365 days AND Received ≥12 (a month of sends at 3 a week). Presenter would remove these people.
6. Act: segment menu (3 dots) > "Suppress current members" (replaces CSV export and import). `[verify UI]`
7. Use Unengaged 120 as the sunset flow trigger.

### 3.21 Default campaign exclusions
[62ea5bc24ef6]
1. Marked as spam: Marked email as spam ≥1 over all time. Exclude from every campaign and suppress.
2. Bounced: Bounced email ≥1 over all time where bounce type = hard, OR Bounced email ≥4 over all time where bounce type = soft. Remove hard bounces at once. Wait on soft bounces (e.g. full inbox).
3. Also exclude unengaged segments from campaigns.
4. Exclude these by default because you will not suppress by hand every day.

### 3.22 Campaign send-time test `[verify UI]`
[eed1632440b9] [9211d9b5ff9c]
1. Campaign > content step > Create A/B test > Test send time.
2. Pick 2 far-apart times: 7 am vs 7 pm.
3. Winning metric: placed order rate. Size distribution 100%. Track links separately per variation.
4. Repeat over 5 to 10 campaigns (more or fewer by list size and revenue). Compare average revenue.
5. Narrow: winner vs a nearer time (7 am vs 11 am), then (11 am vs 2 pm).
6. Do not just adopt Klaviyo's Smart Send Time, which picks the best open-rate time.

### 3.23 Campaign content test
[8cab23f94038]
1. Create A/B test > Test content. Version A "original with product blocks", version B "without product blocks".
2. Sitewide sale: 3 bestsellers vs product categories vs new arrivals.
3. Above the fold: headlines, CTAs.
4. Winner on placed order rate; run over several campaigns; apply the learning to flows.

### 3.24 Flow timing test with a split
[5f42a553bc22]
1. At the top of the flow add a conditional split: random sample 50%.
2. Yes path: delay 1 h. No path: delay 3 h (start with a wide gap).
3. Duplicate every email onto both paths (do not rejoin after email 1): email 1 may lose on the long delay while emails 2 and 3 win.
4. Narrow later (site: if 4 h beat 1 h, test 3 h vs 4 h; browse: 1 h vs 3 h, then vs 2 h).
5. Watch placed order rate and spam complaint rate.

### 3.25 Flow email subject or content test `[verify UI]`
[e753b3fb98af] [8f302c6bcdfe]
1. Open the flow email > Create A/B test. Example: "Did you see something you liked?" vs "Oops, you forgot something".
2. Turn off automatic distribution; set 50/50 by hand. Reason: Klaviyo sometimes favours a variant too early. Use automatic if you cannot check often.
3. Winner metric: click rate (default). Open rate is the other option. Placed order rate is not offered here.
4. Winner selection: "end test by statistical significance" (slow), a time limit, or off (manual).
5. Write the hypothesis in the notes field.

## 4. Rules, thresholds and numbers

| rule | number or threshold | condition | source's basis | card id |
|---|---|---|---|---|
| Typical popup list conversion | 2 to 4% of visitors | Average ecommerce brand | Presenter's observation | [40691f40d94c] |
| High-converting popup target | 8 to 12% of visitors | With his popup build | Presenter's client work | [40691f40d94c] |
| Popup time delay | 4 to 10 s (up to 12); default 6 s | Desktop and mobile | Heuristic, test it | [d124c18b882e] [9adb06995af6] |
| Popup scroll trigger | test 40 to 80%; use 50 to 60% | Check scroll depth in analytics | Heuristic | [d124c18b882e] |
| Popup re-show after close | 3 to 5 days (default 5) | By revisit frequency | Heuristic | [d124c18b882e] |
| Desktop CTA height | 54 px default to 70 px | Not absurd (150 px too big) | "Bigger CTA, more clicks" | [72945bee8a3a] |
| Mobile popup sizes | input text 20 px, input 70 px, CTA 80 px, CTA text 24 px, microcopy 20 px, success text 22 to 24 px | One demo build | Example | [f932973235fb] |
| Minimum offer | 10% off; 5% too weak | Unless very high AOV | Opinion | [72945bee8a3a] |
| $ off vs % off | $20 likely beats 10% at AOV $200 | AOV ≥ $200 | Perception, test it | [72945bee8a3a] |
| Spam check line on success page | "within 5 minutes" | New subscribers | Support-ticket saving | [d319ea40cf4e] |
| Smart sending window | 16 h (can set e.g. 8 h) | Campaigns only | Presenter setting | [b837f7435caf] |
| Smart sending in flows / campaigns | Off / on in 99.9% | Always | Presenter rule | [a891648996f4] |
| Email attribution window | 5 days, excluding Apple privacy opens | Account setting | Presenter setting | [fc0425a31c0f] |
| SMS attribution window | 1 day | Account setting | Klaviyo default kept | [fc0425a31c0f] |
| Sending domain warm-up | may limit to engaged for 2 to 4 weeks | After activating branded domain | Klaviyo notice in UI | [fc0425a31c0f] |
| Site abandon first delay | 1 to 4 h | Test 1 vs 4 h | Heuristic | [b0f7b82a2bb3] [3638d8afef7a] |
| Browse abandon first delay | about 1 to 3 h (template 2 h) | Test 1 vs 3 h | Heuristic | [5aad4467fa44] |
| Cart abandon first delay | 30 min to 2 h (template 4 h "too long") | Test 30 min vs 2 h | Heuristic | [fac642b0957b] |
| Browse flow re-entry block | not in flow last 30 days | Template default | Klaviyo default | [5aad4467fa44] |
| Cart and checkout re-entry block | 7 days default; presenter prefers 14 | Shorter for weekly repurchase | Heuristic | [fac642b0957b] [9da5ac313720] |
| Welcome series | 7 emails, delays 0, 1, 1, 2, 2, 2, 1 days | After popup signup | Presenter structure | [6e89698da8b5] |
| Browse abandon length | 4 to 6 emails | | Presenter habit | [5aad4467fa44] |
| Cart and checkout abandon length | 6 to 8 emails (9 optional); 14 to 20 gets annoying | Watch complaints | Presenter habit | [fac642b0957b] |
| First discount in abandon flows | from email 4 or 5, with 48 h deadline, then 24 h | Browse, cart, checkout | Opinion | [fac642b0957b] [5aad4467fa44] |
| Post-purchase first email | 30 min after order | After transactional email | Presenter default | [d4ea5342470c] |
| Post-purchase delays | 30 min, 2 d, 10 d, 3 d, 7 d, 1 d | 10 d depends on shipping time | Presenter default | [0a935c9bd091] |
| Buyer's remorse window | first 24 to 48 h after paying | Physical goods awaiting delivery | Presenter claim | [c17894672b54] |
| Winback wait | template 75 days; set from own cycle (e.g. 40 or 90) | Test it | Klaviyo default + opinion | [4bfa7e9cadf3] |
| Winback delays | X, +3 d, +7 d, +1 d, +about 14 d, +1 d | Template 15 d gap too long | Opinion | [a5998cc28759] |
| Replenishment reminder | e.g. day 25 of a 30-day pack | Consumables | Example | [b8acdbab97a3] |
| Sunset audience | no opens in 90 or 120+ days | By segment | Presenter setting | [c57d2fe2264a] |
| Non-discount to discount ratio | at least 5:1; presenter uses 10:1 | Not Q4 | Opinion | [81f4514ba7d3] |
| Discount emails per month | max 1; some clients 0 for 2 months | Not Q4 | Presenter habit | [81f4514ba7d3] |
| Campaigns per week by revenue | under $50k/mo: 2 to 3; over $50k: 3 to 4; over $200k: 4 to 5 | Monthly total revenue | Rough guide | [a6116076fc6e] |
| Campaign ceiling | almost never above 5/week | Unless segments keep each person near 3/week | Opinion | [a6116076fc6e] |
| Raise frequency | +1/week when open rate > 30% and unsubscribes low | Step by step | Heuristic | [a6116076fc6e] |
| Hold or cut frequency | open rate < 30% and high unsubscribes at 4/week: clean list, maybe drop to 3 | Even if revenue > $200k | Heuristic | [a6116076fc6e] |
| Products per email | max 3 to 4 | Promo and product emails | Links hurt deliverability; choice overload | [46502d7fa9bc] |
| Email text size | 18 px desktop, ≥16 px mobile, line height 1.5 | Brand dependent | Preference | [046d714ac94c] |
| Block padding | about 20 px top and bottom | Between image sections | Preference | [046d714ac94c] |
| Email file size | about 35 KB was "safe from Gmail clipping" | Demo email | Example; no limit stated | none |
| Engaged windows | 30, 60, 90, 120 minimum (+7, 14, 200 optional) | Campaign targeting | Presenter set | [ff7571c5eb99] |
| Unengaged: emails received | ≥6 in 120 days; ≥12 in 365 days | At about 3 campaigns/week | Trial and error | [171bd57ff251] |
| Window shopper | ≥2 views, site visits or clicks in 30 days, 0 orders ever | Tune up to 3 or 4 | Presenter default | [b97e06f650c6] |
| Abandoner segment | cart or checkout in 90 days, 0 orders in 90 days | Final-chance campaign | Presenter default | [b97e06f650c6] |
| VIP | ≥4 orders or spend ≥4x AOV | Brand dependent (2x AOV also used) | Opinion | [14037b197111] |
| Soft bounce exclusion | ≥4 soft bounces; hard bounce: 1 | All time | Presenter setting | [62ea5bc24ef6] |
| Inactive segment timeout | 45 days unused | Klaviyo behaviour 2024 | UI | [ff7571c5eb99] |
| Reading level | 5th grade | Body copy | "Research", uncited | [c5f693b5c277] |
| Copy cut when read aloud | 20 to 30% | Editing pass | Experience | [c5f693b5c277] [737d5783fddc] |
| Research vs writing time | 80% / 20% | Especially early | Saying, "kind of true" | [618c17167140] |
| Humor | works well for audiences under about 30 | If it fits the brand | Opinion | [618c17167140] |
| Send-time test length | 5 to 10 campaigns per pair | By list size and revenue | Heuristic | [eed1632440b9] |
| CTA colour tests | not worth it under about $100k/month | Worth it at multi-million/month | Opinion | [97bfd09fd8e1] |
| Low-value test target | flows with about 20 recipients/month | Skip | Opinion | [c61791a6cbeb] |
| Image compression example | 2 MB to 522 KB (74%); other slices 51 to 68% | TinyPNG | Demo | [8f1c460f5eed] |

## 5. Diagnostics and checks

| check | how | good | bad | next step | card |
|---|---|---|---|---|---|
| List growth rate | New subscribers ÷ sessions, same period | Near 8 to 12% | Near 2 to 4%, or footer form only | Rebuild popup (3.3 to 3.6); fix offer first | [40691f40d94c] |
| Popup vs 10 mistakes | Audit: offer strength, fields, delay, size, copy, offer in headline, "sign up" wording, separate mobile form, image weight, code on success page | All 10 clear | Any fail | Fix; offer first | [9adb06995af6] |
| Signup test read-out | Submit rate AND total signups AND welcome placed order rate, AOV, revenue | Wins on revenue | Wins only on submit rate | Pick the revenue winner | [c09dafafbc67] [28f913be3ee9] |
| Cart flow trigger | Open the "abandoned cart" flow, read the trigger | Added to cart | Checkout started (it is a checkout flow) | Build a real cart flow; keep the other as checkout | [fac642b0957b] |
| Both abandon flows exist | Flow list | Cart and checkout flows both live | Only 1 | Clone and change trigger | [393737091e3e] |
| Core flow coverage | Flow list | Welcome, site, browse, cart, checkout, post-purchase, winback, sunset | Missing any | Build in that order of revenue weight | [b8acdbab97a3] |
| Overlap filters | Each flow's profile filters | Matches section 3 per flow | People get 2 flows at once | Add "since starting this flow" exits | [9da5ac313720] |
| Smart sending in flows | Each flow email's settings | Off | On (skips high-intent sends) | Untick "Skip recently emailed profiles" | [b837f7435caf] |
| UTM tracking | Account + each email | On | Off | Turn on | [b837f7435caf] |
| Post-purchase cancel filter | Trigger filters | Cancelled order = 0 | Missing | Add | [9f9c84a1b824] |
| Urgency honesty | Codes in deadline emails | Dynamic or truly expiring | Static "WELCOME10" with a fake deadline | Switch to dynamic codes | [a69de45ff438] |
| Discount ratio | Count last 30 to 60 days of campaigns | ≥5:1 (presenter 10:1), ≤1 discount/month | Weekly discounts | Swap promos for value, proof, product highlight | [81f4514ba7d3] |
| Frequency vs metrics | Open rate and unsubscribe rate at current cadence | Open > 30%, low unsubs: can add | Open < 30%, high unsubs | Clean list, hold or cut | [a6116076fc6e] |
| Bucket mix | Calendar | Several of the 7 buckets each month; no 2 sales emails back to back | Mostly promos | Refill from buckets | [23ed2f50d61a] |
| Above the fold | Open on phone | Headline, support, CTA (and code for promos) visible | Code or CTA only after scrolling | Move them up | [d1327991a91c] [46502d7fa9bc] |
| Product count | Count product blocks | 3 to 4 max | More | Cut | [46502d7fa9bc] |
| Images | Alt text, link, compression | Every image has alt, deep link, compressed | Missing alt, home page links, MB-size files | Fix | [17b5705e3605] |
| Live text | Email body | Some real text | All one image | Slice and rebuild text | [8f1c460f5eed] |
| Size and clipping | Klaviyo shows email size | Small (demo 35 KB) | Clipped in Gmail | Compress, cut | none `[web check: Gmail clip size]` |
| Mobile render | Preview + test send | No odd padding | Indented text | "Full width on mobile" toggle | [046d714ac94c] |
| Links | Click every link in preview and test | All resolve, code applies | Broken or wrong page | Fix URL | [17b5705e3605] |
| Hygiene | Sizes of unengaged, bounce, spam segments | Excluded from all campaigns | Sent to | Add exclusions; suppress hard bounces and 365-day unengaged | [171bd57ff251] [62ea5bc24ef6] |
| Sending domain and DMARC | Klaviyo domain status; DNS TXT at _dmarc | Active; record present | Shared domain or no DMARC | Section 3.2 | [fc0425a31c0f] |
| Test metric | A/B test settings | Placed order rate (or click rate where it is the only choice) | Open rate | Change winner metric | [5d7c84dc41ce] |
| Test target | Recipients per month of the tested email | Top flow first emails, big campaigns | Tiny flows, one-off subject lines | Re-prioritise | [c61791a6cbeb] |
| Long flows | Spam complaint, unsubscribe, open rate per email | Stable | Rising complaints at later emails | Shorten, lengthen delays | [fac642b0957b] |

The source gives no complaint-rate, bounce-rate or open-rate thresholds for deliverability beyond the 30% open-rate frequency rule. `[web check: current Gmail/Yahoo spam complaint limits]`

## 6. Tools, settings and named features

- **Klaviyo** `[verify UI]`: signup forms (popup, flyout, embed, full page; teaser; steps; success page; targeting; URL, UTM and location rules); flows (triggers, trigger filters, profile filters, time delay with time of day, weekday and local time zone, conditional split with random sample, profile property update, webhook, internal alert, add past profiles, update action statuses, flow analytics, flow history); campaigns (smart sending, UTM, A/B test for send time or content, winner metric, distribution, end test by statistical significance, notes); editor (drag and drop, text only, HTML, template library, universal blocks, block padding, full width on mobile, source code view); segments (lists and segments, inactive segments, suppress current members, predictive analytics); settings (branded sending domain, sending preferences, attribution, anonymous visitor tracking, consent pages, UTM, brand library with Google and Adobe fonts). Klaviyo's "Smart Send Time" picks by open rate.
- **SendLane**: named alternative ESP.
- **Shopify**: store connection, transactional emails, discount URL `/discount/CODE?redirect=/collections/...`, revenue metric for VIP.
- **DNS host** (GoDaddy, Squarespace) for NS, TXT and DMARC records; any free **DMARC record generator**.
- **Figma**: design, Slice tool, PNG or JPG export.
- **TinyPNG** (also Squoosh, iloveimg.com): image compression.
- **Hemingway**: reading level. **Grammarly**: spelling and grammar.
- **Notion, Airtable, ClickUp, Monday, Google Sheets**: calendar tracker. **blankcalendarpages.com** and **Miro**: calendar sketch. **nationaltoday.com**: niche days.
- **Google Analytics**: scroll depth for popup rule; UTM data.
- Loyalty and review apps are named only in passing ("Kendo", likely Okendo).

## 7. Examples and case results

All are the presenter's own client or demo examples. None is a promise.

- Client A: $700k email revenue in first 3 months, 34% of total revenue, +280% vs the prior 3 months. [0944381047ee]
- Client B: $380k email revenue Jan to Jul, 52% of total revenue, +61% vs last year.
- Client C: "1.6 million, over $2 million" email revenue last year (garbled), +68.9% vs the year before.
- Client D: $112k email revenue in the first 60 days, 38.4% of total revenue, +237 (likely %) vs the prior 2 months; total store revenue +51%. No control for ad spend or season.
- Offer test: a new signup offer had a lower welcome-flow placed order rate but much higher AOV and higher welcome-flow attributed revenue, so it won. No figures. [c09dafafbc67]
- Blanket brand popup image: blanket with a dog on it beat a plain blanket "way, way better". No figures. [33fbda8be073]
- Dollar Shave Club redesign (not a client, not sent): original above the fold had only "Suds up, price down" and a sticker, no CTA, code at the bottom. Redesign: headline "20% off shower products", code DIRTYDISCOUNT and a big "Save now" CTA above the fold, on-brand image, "Recommended for you" zigzag of 3 products (body wash, hair and scalp shampoo, conditioner), closing copy "That's right, we're throwing a shower category sale so epic even your rubber duck is going to feel posh", repeat code and CTA, footer with category links (e.g. shave). No results measured. [46502d7fa9bc] [81608ccfcce2] [2b0c87a53512]
- Design examples: Magic Spoon (Z pattern; visual steps "Rise. Spoon. Shuffle to your kitchen. Pour."), Dr. Squatch (inverted triangle "top 3 scents women love"; quiz email with an arrow to the CTA), a lollipop brand (F pattern), Magic Mind ("Hack your happy hormones" checklist; "Get over the hump day slump"), a bar brand comparison table, Ritual ("Enjoy 30% off for Memorial Day, shop now"). A clearance email with a wall of text for "40% off, everything must go" is the bad example. [73c535d638e2] [aea3035bb04a] [d1327991a91c]
- Headline examples: Apple "1,000 songs in your pocket" (iPod), "It's all screen" (iPhone X), "Full screen ahead" (Apple Watch). [98dec094905b]
- Calendar example (August 2024, skincare brand with sunscreen, 3 sends a week Tue, Thu, Sun; he likes Sunday): Summer Sun Safety Month email at the start, National Sports Day (Aug 29, skin care after sport), product highlight every Sunday, value email every Tuesday, a 24-hour VIP flash sale, a review email, a behind-the-scenes company update. [85157d54ac6e]
- Popup copy test lists: headlines "Save 10% now", "Get 10% now", "Take 10% off now", "Unlock 10% off now", "Your discount awaits", "Do you want 10% off?"; CTAs "Save 10% off now", "Get 10% off now", "Take 10% off now", "Unlock my discount now", "Reveal my discount now", "Get my discount now", "Reveal the deal", "I want my discount"; microcopy "No thanks, I'll pay full price", "No thank you", "No spam guaranteed", "Recommended by 5,000 happy customers", "Rated 4.9 out of 5 by 5,000 customers". [28f913be3ee9]
- SMS step angles: same offer as email; better offer (10% email, then "Do you want 15% off? Join SMS"); VIP club (exclusive sales, pre-sales, early access). Measure SMS opt-in rate. [1bad712bca98]

## 8. Mistakes the source warns about

Popup:
1. Weak offer (the most important mistake). [9adb06995af6]
2. Asking for more than email in step 1 ("massive conversion killer").
3. Delay too short (annoys) or too long (few see it).
4. Form too small.
5. Too much copy.
6. Offer hidden in body copy instead of the headline.
7. Words "sign up" and "subscribe".
8. One form for mobile and desktop.
9. Slow images.
10. Code on the success page (low welcome email 1 opens, hurts deliverability).
11. Showing the popup immediately on load. [d124c18b882e]
12. Showing it on cart or checkout pages (discount to someone already buying).
13. Relying on a footer form. [40691f40d94c]

Flows:
14. Using an "abandoned cart" template that triggers on Checkout started and thinking you have a cart flow. [fac642b0957b]
15. Having only 1 of the 2 abandon flows. [393737091e3e]
16. Leaving smart sending on in flows. [b837f7435caf]
17. No exit filters, so people get overlapping flows and mark you as spam. [9da5ac313720]
18. Discount in email 1 or 2 of abandon flows (trains discount seekers). [5aad4467fa44]
19. Discount without a deadline. [fac642b0957b]
20. Fake urgency or a static "WELCOME10" code. [a69de45ff438]
21. Generic reviews ("highly recommended, great company") instead of pain-point reviews. [6e89698da8b5]
22. Sending the post-purchase email the instant the order lands. [d4ea5342470c]
23. Long winback or abandon sequences with short gaps (annoyance, complaints). [a5998cc28759]
24. Shipping Klaviyo templates unedited. [fd7d4c80cdb7]
25. Skipping the site abandonment flow because there is no template. [b0f7b82a2bb3]
26. Keeping unengaged people "for a big list". [c57d2fe2264a]

Campaigns and design:
27. Too many discounts; weekly 20% off kills excitement. [81f4514ba7d3]
28. Setting frequency by feel instead of open and unsubscribe data. [a6116076fc6e]
29. Using every holiday, or a discount on every holiday. [85157d54ac6e]
30. Long paragraphs, too many colours, walls of text. [6e550d63490a]
31. No CTA or code above the fold. [46502d7fa9bc]
32. Too many products or links. [46502d7fa9bc]
33. One big image email (slow, 1 link, worse deliverability). [8f1c460f5eed]
34. Missing alt text, links to the home page. [17b5705e3605]
35. HTML editor emails that break on some clients. [ebb2548fab18]
36. Skipping or wasting the preview text. [3247c58dc8b5] [589fc4bc3d9b]
37. Full-sentence subject lines that get cut on mobile. [589fc4bc3d9b]
38. Clickbait that the email does not deliver (spam complaints). [589fc4bc3d9b]
39. Talking features, not outcomes. [98dec094905b]
40. Many messages in 1 email. [c5f693b5c277]

Testing:
41. Campaign subject line tests with no hypothesis and no reuse. [8f302c6bcdfe]
42. Choosing send time by open rate (Smart Send Time). [eed1632440b9]
43. Judging from 1 campaign ("zero data"). [eed1632440b9]
44. Testing button colours at small scale. [97bfd09fd8e1]
45. Testing low-volume flows before the big 4. [c61791a6cbeb]

## 9. Caveats, conflicts and what is missing

- **Evidence is thin.** All numbers are one agency's defaults or client dashboards. No sample sizes, no holdouts. Revenue-share claims mix email with paid spend and season changes. [0944381047ee]
- **Header vs speaker.** The Added to Cart JavaScript snippet, DMARC escalation to reject, and Yahoo rules are only in the library header, not the transcript. The speaker's own DMARC record is p=quarantine with pct=90 while he tells viewers to start at none. He never says when to move up. `[web check]`
- **Deliverability numbers missing.** No spam complaint rate limit, bounce limit, warm-up schedule, one-click unsubscribe, or BIMI. The 2024 Google rules are named but not listed. `[web check: Gmail and Yahoo sender requirements, spam rate under which limit]`
- **Single opt-in vs common advice.** Many sources push double opt-in for list quality or legal reasons. He picks single opt-in and relies on sunset plus suppression. Check local law. `[needs brand data: markets]`
- **Hiding the X close button** is a dark pattern by his own "ethical debate" remark. Some platforms or laws may object. Treat as optional and owner-approved only.
- **Smart sending off in all flows** can raise total volume and complaints; he does not address that trade-off (card caveat [b837f7435caf]).
- **Welcome email 6 route B** says "50% off" after a 10% popup; likely a transcription error for 15%. Do not cite 50% as advice.
- **Checkout delay** is not given; card [3638d8afef7a] adds "shortest delay" as inference.
- **Cards that stretch the source:**
  - [c61791a6cbeb] lists post-purchase and winback among the biggest test levers. The speaker names welcome, checkout, cart and browse abandonment.
  - [b8acdbab97a3] names welcome, cart and browse as the top 3. The speaker named welcome, cart, checkout and browse.
  - [d124c18b882e] adds paid-traffic landing pages to URL exclusions. Not in transcript.
  - [0a53b00daef3] says clone 1 template for all 5 pre-purchase flows. The speaker only cloned cart into checkout.
  - [0a935c9bd091] names Judge.me; transcript says "Kendo".
  - [171bd57ff251] and [62ea5bc24ef6] say suppression is irreversible or permanent; the speaker does not say this. `[web check: Klaviyo unsuppress rules]`
- **Contradiction inside the source:** "remind the discount code in every welcome email" sits beside "hold discounts until email 4 or 5" in abandon flows. Both hold, because the welcome code is already promised; abandon flows start without an offer.
- **Frequency tiers** are by monthly revenue, not list size or engagement. The 30% open-rate test predates wider Apple privacy effects; he excludes Apple opens only in attribution, not in this rule. `[needs brand data: open rate excluding Apple MPP]`
- **Sunset timing** and email count after email 3 are not given. **Browse abandon** emails 3 to 6 are only sketched.
- **Replenishment, back in stock, bounceback, window shopper, birthday and anniversary flows** are named with no build steps.
- **SMS** is limited to the signup step; no SMS flow or compliance detail.
- **Metrics he never defines:** placed order rate formula, "high" unsubscribe rate, good click rate. `[needs brand data: baseline flow and campaign metrics]`
- **Discount URL format** is a Shopify pattern; check the store platform.
- **Legal:** GDPR microcopy is only touched for the EU; nothing on CAN-SPAM, India or other markets. `[needs brand data: markets served]`

## 10. Card index

- fc0425a31c0f: Klaviyo (or similar ESP) account setup essentials for a new store
- 40691f40d94c: Rate signup forms against a 2–4% baseline and target 8–12%
- 72945bee8a3a: Build a high-converting popup: offer, headline, single field, big CTA
- d124c18b882e: Timing and display rules for capture popups
- f932973235fb: Always build separate mobile and desktop popups
- d319ea40cf4e: Withhold the discount code from the success page
- f7f5d18ebe32: Teaser tab: keep the capture offer permanently reachable
- 9adb06995af6: Ten signup-form mistakes to audit before scaling list growth
- c09dafafbc67: A/B test the offer holistically, not by signup rate alone
- 52d1b13d3d6e: Add a micro-yes step before the email field
- 0944381047ee: Reap the main email lifecycle payoff: LTV and AOV, not only last-click revenue
- 45fac68dfd23: Micro-yes signup step: ask for consent before email capture
- 28f913be3ee9: Signup form tests: delay, format, and audience size
- 33fbda8be073: Visual signup form tests: color, images, and imagery content
- 1bad712bca98: SMS opt-in angles after email signup
- dfc548f661d2: Flow structure and profile filters in Klaviyo
- a704ce6294f2: Use past profiles to backfill newly launched flows
- b837f7435caf: Turn off smart sending for flows, keep it on for campaigns
- 6e89698da8b5: Welcome series structure: 7 emails with distinct angles
- b0f7b82a2bb3: Site abandonment flow: trigger, delay, and one guiding email
- 5aad4467fa44: Browse abandonment flow: trigger, filters, and review-led emails
- fac642b0957b: Abandoned cart flow: trigger distinction and 6–8 email structure
- 393737091e3e: Checkout abandonment flow: same structure, different objections
- 3638d8afef7a: Time-delay heuristics by journey stage
- 3247c58dc8b5: Subject line, preview text, and sender name optimization
- e0cf57ece0ac: Bulk flow action status and flow analytics
- fd7d4c80cdb7: Decide whether to use Klaviyo's default flow templates
- 9da5ac313720: Exclude engaged customers from overlapping flows
- bccb578fdd8b: Use trigger filters for product- and collection-specific flows
- a69de45ff438: Use plain-text founder emails and real urgency for final conversion
- 0a53b00daef3: Clone the Core Pre-Purchase Flows Instead of Building from Scratch
- 9f9c84a1b824: Add a Cancelled-Order Filter to Post-Purchase Flows
- d4ea5342470c: Time Your First Post-Purchase Email Around Transactional Emails
- 3da6d6371379: Split Post-Purchase Email 1 by First-Time vs Returning Buyer, Then Merge Paths
- c17894672b54: Use the First Post-Purchase Email to Reduce Buyer's Remorse and Cross-Sell Softly
- 0a935c9bd091: Sequence the Post-Purchase Flow Around Shipping, Usage, Loyalty, Reviews and Cross-Sell
- f6a8fc1ece5f: Target the First-to-Second Purchase Gap as the Hardest Retention Step
- 4bfa7e9cadf3: Set Win-Back Timing from Your Own Buying Cycle Data
- a5998cc28759: Escalate Win-Back Offers Slowly with Long Delays to Avoid Annoying Lapsed Customers
- c57d2fe2264a: Run a Sunset Flow to Re-Engage or Suppress Unengaged Subscribers
- b8acdbab97a3: Have the Five Core Flows Plus Win-Back and Sunset in Place
- a891648996f4: Turn Smart Sending Off for Flows, On for Campaigns
- ebb2548fab18: Choose Among Drag-and-Drop, Plain Text, or HTML Email Editors
- 23ed2f50d61a: Use Seven Campaign Buckets to Source Email Ideas
- 81f4514ba7d3: Cap Discount Frequency with a 5:1 to 10:1 Non-Discount Ratio
- a6116076fc6e: Set Campaign Frequency from Revenue Tier, Then Adjust by Metrics
- 85157d54ac6e: Plan the Campaign Calendar by Layering Events, Value Content, and Company News
- bdb13d54947e: Run Campaign Calendar Planning in a Shared Planning Tool
- 6e550d63490a: Design Emails for Conversion, Not Just Aesthetics: Favor Simplicity
- 73c535d638e2: Use Visual Hierarchies (Z, Inverted Triangle, F Patterns) to Guide the Eye to the CTA
- aea3035bb04a: Replace Long Paragraphs with Visual Formats (Checklists, Tables, Comparisons)
- d1327991a91c: Treat the Above-the-Fold Section as Decisive: Include Headline, Support, and CTA
- f20df437e0c5: Build a Modular Figma Email Template Library for Fast, Varied Design
- 8f1c460f5eed: Slice a Figma email into image sections before importing to Klaviyo
- 17b5705e3605: Set alt text, deep links and auto-applied discount codes on email images
- 046d714ac94c: Size, pad and fix email images so they render correctly on mobile
- 46502d7fa9bc: Cap products per campaign email at three to four and keep the offer above the fold
- 46ef575d23c2: Build reusable universal blocks for footer and repeated email sections
- b0096ce3ba62: Use the four segmentation types to decide what to build first
- ff7571c5eb99: Build engaged segments across 30/60/90/120-day windows including website activity
- 7ccc6c565f86: Build buyer, non-buyer and repeat-buyer segments for tailored messaging
- b97e06f650c6: Build abandonment and window-shopper segments for targeted recovery campaigns
- 14037b197111: Define VIP segments by purchase count or spend relative to AOV
- 171bd57ff251: Build unengaged segments, then suppress or exclude them
- 62ea5bc24ef6: Create bounced-email and spam-complaint segments and exclude them by default
- 589fc4bc3d9b: Split subject line and preview text to stay readable on mobile
- 98dec094905b: Write email headlines as outcomes, not features
- c5f693b5c277: Apply reading-level, brevity and one-message rules to email body copy
- 618c17167140: Do audience research before writing, and use copy frameworks as invisible scaffolding
- 737d5783fddc: Cut copy: easy words, active voice, no fluff
- c61791a6cbeb: Prioritize A/B tests by recipient volume, not by ease
- eed1632440b9: Test send time against place order rate, not open rate
- 8cab23f94038: Test content structure in campaigns, not just subject lines
- e753b3fb98af: Use 50/50 manual distribution for email A/B tests
- 5f42a553bc22: A/B test abandonment flow timing with conditional splits
- 8f302c6bcdfe: Flow subject lines are worth testing, campaign subject lines usually are not
- 97bfd09fd8e1: Skip CTA-color split tests at small store scale
- 2b0c87a53512: Write email copy that earns attention through value, not cleverness alone
- 81608ccfcce2: Structure promo emails around headline, code, CTA, products, and closing copy
- 5d7c84dc41ce: Track place order rate as the primary email KPI hierarchy
- 9211d9b5ff9c: Sequence send-time tests from wide contrast to narrow pinpointing
- 96c06aef939a: Expect to customize templates to your brand instead of copying them
