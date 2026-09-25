# Klaviyo email.docx (full Klaviyo email system course, 2026)

source_id: 1WQcWqe36XxPolHopi-PTOYh8vY8HC1zr  |  folder: /14-EML-email-lifecycle  |  cards: 99  |  words: 51,480  |  type: transcript (one long YouTube course, about 12 sections, several recorded as separate videos and joined)

credibility: The presenter runs an ecommerce email agency (the name is transcribed as "Magically"). He sells done-for-you Klaviyo builds ("book a call"), a free email course, a free post-purchase playbook and a free A/B testing playbook, and he promotes Aaliyah (a Shopify popup app) with a free-trial link, so he has a commercial tie to that tool. His evidence is his own client work: "more than 40 ecommerce brands" for the micro-yes step, "120 ecom brands in the last 7 years" for send frequency, "thousands of A/B tests" and "hundreds of ecommerce stores" for test rankings, client screenshots (welcome revenue by day, time between orders, a deliverability recovery), and 2 ChatGPT analyses of client exports. No sample sizes, dates or significance are given for any claim. Post-purchase statistics (9x, 67%, 95%) are credited to unnamed "research". Many numbers are transcription-damaged (see section 9).
date signals: "in 2026" is said many times. Gmail "AI inbox" and Gemini reading emails are described as new in 2026. Aaliyah's scratch-off is "a new feature". iPhone 15 is a preview device. Aaliyah shows Easter templates (recorded around spring). The ChatGPT campaign export covers January to May 2025 and the flow export 1 March to 13 May. Gmail one-click unsubscribe is treated as already live. BIMI cost is "around $1,500 a year". Klaviyo defaults quoted: form re-show 5 days, welcome wait 3 days, browse wait 2 hours, cart wait 4 hours, smart sending 16 hours.

## 1. What this source is for

It is an end-to-end build guide for a Klaviyo email program for a Shopify-style store. It gives the build order (list growth, flows, campaigns, A/B tests, segmentation, deliverability, AI) and click-level steps for each layer: signup form settings and copy, 5 core flows with triggers, filters, delays, splits and email-by-email content, a campaign calendar method with 91 campaign types, a ranked A/B test list with sample rules, a segment set, a deliverability repair plan and AI prompts for analysing Klaviyo exports. Use it to build or audit an account and to pick the next fix. It is weak on SMS, win-back, sunset, site abandonment and replenishment flow builds, and it gives no controlled evidence.

## 2. Principles

1. **Build in dependency order.** List growth first, then flows, campaigns, A/B testing, segmentation, deliverability, then AI. Each layer depends on the one below it. Condition: the source's order for a new or under-built account; the card notes a mature account or a large list with weak capture may start elsewhere. Evidence: presenter framework. [93e33dec853f] [1d17eaa95e56] [5a08594d02a9] [64a2c2916004]
2. **Most brands have a monetization problem, not a traffic problem.** Paid traffic leaves "with nothing but a pixel hit". Signs: blended CAC keeps rising, email is judged on topline revenue instead of whether the welcome flow captures first-time buying intent, and the brand leans on costly retargeting to recover people it already paid for. Condition: diagnostic frame, not a causal model; CAC can rise for other reasons. [9ed0b65913bb]
3. **A capture form is the gateway.** About 98% of visitors leave without buying (2% store conversion). A strong form captures 8% to 12% of traffic; the welcome flow converts 10% to 20% of new subscribers; other flows and campaigns convert more. Industry standard signup rate is 1% to 3%. Going from there to 8% to 12% means about 3x the list and, the presenter claims, about 3x email revenue. Condition: presenter's funnel numbers, no data shown. [aa555d450d5a] [93e33dec853f]
4. **The offer is the biggest lever on signup rate.** A bad offer in a beautiful form still gets a bad signup rate; a good offer in a poor design still wins. Other hacks move a bad-offer form only from about 2% to 2.2%. [aa555d450d5a] [4c956b5e96a1] [0590112c25d0]
5. **Judge form offers holistically.** Look at signup rate, total signups, the welcome flow conversion rate, welcome flow attributed revenue and profit margin. A higher signup rate with much lower welcome conversion may still be fine (you can nurture them) or may call for going back to the old offer. [aa555d450d5a] [0590112c25d0] [00de729163a8] `[needs brand data: margin per order, welcome flow CVR and revenue per offer]`
6. **Signup forms are never "set and forget".** Start where you are (for example 4%) and A/B test toward 8% to 12%. [aa555d450d5a] [4c956b5e96a1]
7. **Less friction, more conversion.** One input per step, no supporting copy, the offer in the headline, benefit words instead of "sign up" or "subscribe", clear input field. [9622afcc8844] [39aa68c94680]
8. **A small first commitment raises the next yes.** A yes/no step, a 1-question quiz, a scratch-off or a spin wheel before the email field lifts signups for most brands. Condition: tested on 40+ client brands, "in most cases" it wins, not always; results differ by device. [e912865caec2] [d80edbbaaf50] [7da3ea843dc6] [b9635f9e2351]
9. **Do not show the discount code on the success page (presenter's position, a 50/50 industry debate).** Reason: if the code is on screen, nobody opens welcome email 1; low opens on a new subscriber's first email are a bad signal to Gmail and Outlook. His client tests showed a "pretty minimal" conversion loss, recovered in the first 72 hours by the welcome flow. Condition: opinion plus unquantified client tests; the provider logic is his reading, not a documented rule. [1f8be190a019] [8e47ceff852b]
10. **The first 72 hours after signup carry almost all welcome revenue.** Day 0 is the highest converting day; after day 3 only "a bare minimum" remains. So front-load the welcome flow instead of stretching it over 10, 14 or 21 days. Evidence: "conversion by days from subscription" screenshots across accounts. [f2c3f6895ad4] [580319f842a5]
11. **The welcome flow's job is 3 things.** Deliver the promised offer, build confidence to buy now, guide to the right product. Not brand-heavy, story-heavy or slow. Email 1 makes most of the revenue; later emails build conviction (social proof, credibility, education, objections, USPs, category guidance, bestsellers, founder credibility, urgency). [f2c3f6895ad4] [a0d2e94690df]
12. **Match the delay to intent.** The closer someone is to buying, the sooner you email: site abandonment hours, browse 30 minutes to 2 hours, cart shorter, checkout as early as 15 minutes. [c83fa5e0d0d6] [0528a2003316] [d94eb68e5e18]
13. **Browse abandonment is mid-funnel persuasion, not lost-sale recovery.** Trust matters more than urgency, objection handling more than a discount, positioning more than a promotion. Browsers likely have competitor tabs open. Do not treat it as a weak cart flow. [d0e8f91819ba]
14. **Hold discounts back in abandonment flows.** Most cart abandoners are distracted, not saying no. Reminder, founder check-in and objection handling come first; the discount comes only in the escalation emails. A 20% code in email 1 "will generate revenue but destroy margins". [bdbde349add0] [8c9c22844f69]
15. **Split cart and checkout discounts by buyer status; do not split browse.** Returning customers already trust you and are often just distracted, so they get support, not a discount (or a smaller one). Browse abandoners are low intent even if they bought before, so everyone gets the same ladder unless margins are extremely tight. [4085ce710e47] [5ad3da1bdb3a]
16. **Plain-text founder emails feel human and are rewarded by inbox AI.** Used in welcome 1B, browse 4, cart 2 and 5, returning-customer check-ins and post-purchase 1 and 6. Condition: presenter says it works "for certain niches"; test designed vs plain text. [63691cee89e1] [00ade878eca2] [bdbde349add0]
17. **Urgency must look real.** Use unique codes, or static codes that look unique; "everyone knows WELCOME10 is not going to expire". Only use deadlines and "extended" offers that are true (card caveat). [cefa2905adfd] [18ddf0ee7ebf]
18. **The first purchase starts the relationship.** Most repeat purchases happen within 30 days of the first order (client screenshots), so the post-purchase flow works that window, reduces buyer's remorse and returns, and cross-sells. [b3058403e9f8] [5956a124a134]
19. **Flows capture demand; campaigns create it.** Campaigns are the lever to drive revenue on purpose instead of waiting for automation. [7a1145af87dc]
20. **Send 3 to 4 campaigns a week.** 1 to 2 a week makes you "less memorable", not less intrusive, while competitors at 3 to 4 stay top of mind. 5 to 7 a week burns the list slowly (fatigue, unsubscribes, lower engagement, deliverability damage). Evidence: tested across 120 ecom brands over 7 years, no data shown. [7a1145af87dc] [8db768330eb7]
21. **Do not let promos dominate.** Constant discounts train subscribers to wait, kill margin and make the brand feel desperate. Customers in 2026 are skeptical; trust needs repeated, useful touch points; trusted brands sell without discounts. [9bbb999b4ec9] [071d76074c86]
22. **Every email should show the product.** Teach a problem, then place the product as the natural solution. Useful, not pushy. [f5ac8bd65765]
23. **Send campaigns to engaged segments, never to the full list or to lists.** Mailing unengaged people hurts deliverability, and then even good campaigns land in spam. [bb790bf6e145] [6e06d938ff3f] [951b0132a90b]
24. **Test with a system.** Test every 2 to 4 weeks, from a written hypothesis, with enough data, judged on revenue ("the deciding factor in 95% of tests"). [59ae581e3e7f]
25. **Test where the volume is.** The first email of each flow has by far the most impact; flows make 40% to 70% of email revenue; the highest-volume flow (usually welcome) is where small lifts compound. A 2% to 2.5% lift on email 6 of a flow with 20 to 100 recipients a month does not matter. [700ad4cccb44] [87afe3ecbaf6] [a0d2e94690df]
26. **Deliverability in 2026 is an engagement game.** Gmail's AI detects marketing intent and files marketing-sounding mail in Promotions; opens, clicks and especially replies are the main signals; Gmail's AI inbox summarises, groups or ranks generic marketing lower. Promotions is "delivered" but earns less. Condition: presenter's reading of Gmail, not a Google statement. `[web check: current Gmail AI inbox behaviour and Google sender guidelines]` [4933eedd5bb2] [660cfc96df62] [31b2f58bfc95]
27. **Technical setup is required but rarely the main cause of poor placement.** List quality and engagement are. [e758ab334635]
28. **Inbox providers only care about their users.** Good signals: open, click, reply. Bad signals: ignore, spam report, unsubscribe. "Send better emails, not prettier emails." [660cfc96df62]
29. **Use SMS sparingly.** Only for launches, restocks and sales events; everything else goes by email. SMS is expensive, especially outside the US; in Europe test WhatsApp. [b9130f4f4dca]
30. **AI is the last layer.** It speeds up planning and analysis; it does not fix a missing flow or bad deliverability. Treat its output as a draft or as hypotheses. [64a2c2916004] [7dccf4216521] [e932614a8a69]

## 3. Procedures

All Klaviyo and Aaliyah menu names below are as spoken in the video. `[verify UI]` applies to every click path.

### 3.1 Build the desktop signup form in Klaviyo

Goal: an 8% to 12% signup rate. [c5e1f30dd58d] [9622afcc8844] [e912865caec2] [53f37df1584e] [1f8be190a019]

1. Left menu > Signup forms > Create form (top right). `[verify UI]`
2. Category: email only, email and SMS, or SMS only. The demo collects email only.
3. Form type: popup or full page perform best. Split test both later. The demo uses a popup.
4. Pick a template, name it (for example "demo desktop"), choose the list new subscribers join (usually "Newsletter"), and switch on the teaser. Create.
5. Targeting and behavior > Timing: change "immediately" to "based on rules". Desktop rules: when visitor is exiting the page; after a time delay of 6 seconds (test 4 to 12); after the visitor scrolls 60% (test 30% to 90%); optional page-count rule. Leave "all conditions must be met" off, so any one rule fires the form. `[verify UI]`
6. Frequency: "after a visitor closes the form, show again after" default 5 days; set 3 days.
7. Devices: desktop only. (Mobile gets its own form, see 3.2.)
8. Targeting: "don't show to existing Klaviyo profiles". Exclude URLs: cart page, checkout page, any wholesale page. Optional UTM rules. Location: only the countries you ship to; exclude countries as needed. [a877dc6c99dd] `[needs brand data: ship-to countries, wholesale URLs]`
9. Design the email opt-in step: side image with alt text; logo with alt text; headline that is the offer ("Unlock 20% off your first order"); delete the default sub-headline "Sign up for special offers and updates"; email field label "Enter your email here"; Edit styling > input field styles: light grey background so the field stands out on white; set brand fonts for text, headings and input; CTA "Get my discount now"; delete the "By signing up, you agree to receive email marketing" disclaimer if US-based (the EU "is a bit different"); microcopy "No thanks" that closes the form.
10. Hide the close X: set its size to 1 px and its colour transparency to 0. "No thanks" is then the only close path. (See conflict in section 9.)
11. Add the micro-yes step: clone the opt-in step, name it "micro yes", move it before the opt-in. Remove the input field. Headline "Do you want **20% off** your first order?" (only "20% off" bold, larger). Buttons "Yes please" (goes to email step) and "No thanks" (closes). Add padding.
12. Teaser: style rectangle on desktop; behavior "before displaying the form and after the form is closed"; text instead of the gift icon, "Save 20% now", black background, white centred text. Presenter's tests: the teaser raises signup rate and the absolute number of subscribers.
13. Success page: same logo and fonts as the form; headline "Your discount code is on its way"; body "Please check your inbox for the confirmation message with your discount code. Didn't receive an email within 5 minutes? Please check your spam box." in bold. Do not show the code. The spam line saves support tickets when there are deliverability issues.
14. Check: form looks on-brand, offer is the first thing read, only one field per step, no X, success page matches.

### 3.2 Clone the form for mobile

[c2e8c7484a70] [8b8c3454e9e7] [ef89709e3516]

1. On the desktop form: three dots > Clone > name "demo mobile". Targeting and behavior > display on mobile only. `[verify UI]`
2. Untick "when visitor is exiting the page": exit intent on mobile is unreliable and fires when people are not leaving.
3. Teaser: circle instead of rectangle (a full-width bar can collide with loyalty or other widgets); text "Save 20%".
4. Micro-yes and opt-in steps: CTA button height 70, CTA text 30, "No thanks" 18 px; offer number in the micro-yes headline 60.
5. General styling: input field height 70, input text 20.
6. Success page text 22.
7. Remove images on mobile (speed on 4G or 5G); keep only a compressed logo.
8. Check every font is readable and nothing overflows.

### 3.3 Set up a signup form A/B test in Klaviyo

[00de729163a8] [4c956b5e96a1] [0590112c25d0]

1. Open the form > "Create A/B test" (top left). Name it after the variable, for example "offer test". Variant A = current (20% off); variant B = challenger (mystery discount). `[verify UI]`
2. Edit every element of B that carries the offer: micro-yes headline ("Do you want a mystery discount?"), opt-in step, teaser.
3. Continue to test settings: weight = manual (50/50), not automatic. Reason: Klaviyo tends to favour one variant before there is enough volume.
4. Winner selection: manual. Do not auto-end the test.
5. Run until at least 3,000 to 5,000 impressions per variant or at least 15 days, whichever is longer (7 days can be enough in some cases). [e8e1adc8fefe] [59ae581e3e7f]
6. Test desktop and mobile separately.
7. Decide on total signups plus welcome flow conversion and revenue, not signup rate alone.

### 3.4 Build a full-screen popup in Aaliyah (Shopify app)

Presenter's optional route to higher signup rates ("up to 20%" seen vs 6% to 12% with Klaviyo forms). He promotes this app with a trial link. [b9635f9e2351] [7da3ea843dc6] [d80edbbaaf50] [143e7458c1be] [ba6a52eba2e9] [6f18ca80ca5c] [33c8d10a4bf5] [020eec5d0a13]

1. Integrations: connect Klaviyo (click connect); pick the Klaviyo list new subscribers join. Also works with Omnisend, Postscript, Attentive, Sendlane, Yotpo and others. `[verify UI]`
2. Campaigns > Build your first campaign > Get started > pick a template (full-screen on mobile and desktop; seasonal sets such as Easter and BFCM). Set brand theme (colours, fonts). Upload logo.
3. Floating button (Klaviyo's "teaser"): keep it on. Positions: bottom left, bottom right, vertical left, vertical right, or none. Presenter and Aaliyah both advise keeping it.
4. First step (micro commitment). Options, test them against each other:
   - Mini quiz: one question (presenter keeps it to 1), for example "What is your goal? Lose weight / Grow muscles / Improve my health", or "What are you shopping for today? Myself / Someone else". Highest signup rate "according to Aaliyah". Answers go to Klaviyo as zero-party data.
   - Spin to win: every visitor wins the one reward you set (for example 5% or 10% off); other slices are shown but never land.
   - Scratch-off: "Try your luck. Scratch below to see what you win." Example: one brand went from 11% to 14% signup conversion with this single change.
   - Old-school micro-yes: "You've got 10% off / a mystery discount. Claim 10% off / No thanks", or "Do you want a mystery discount?".
   - No first step: not recommended by Aaliyah or the presenter, but can be tested.
   Presenter: mini quiz or scratch-off usually wins.
5. Fields: email first; SMS as a later step. Add terms of service and privacy policy links; set the default SMS country code.
6. Reward display: presenter picks "no reward" on screen. Success copy: "You're in", check your inbox for the confirmation message with your discount code; check spam or the promotions tab if it is not there within 5 minutes.
7. Opt-in: single opt-in (Aaliyah recommends it for Klaviyo); Aaliyah recommends double opt-in for Postscript and Attentive. Presenter never uses double opt-in because the confirm click "massively" reduces new subscribers. `[web check: EU double opt-in expectations per market]`
8. Triggers: time delay 4 to 12 seconds (start with a 4 s vs 12 s test, then refine), scroll 60%, exit intent (desktop: mouse leaves; mobile: fast scroll up). Per-device options. Smart triggering (off by default): a predictive model that fires the popup once in addition to your rules. Presenter turns it on; typical test result: signup rate slightly lower, total signups higher (some clients the reverse).
9. Editor extras: re-show after close (seconds to a year); "don't trigger if another popup was viewed in the last 15 seconds" when you run several popups; play animations; preview on devices (iPhone 15, 4K desktop); Preview button opens the live site with the popup.
10. Targeting rules: main form to new visitors = not returning AND not signed up for email AND not signed up for SMS. Returning visitors = signed up for email OR SMS OR identified by cookie: use separate popups to collect zero-party data or move email subscribers to SMS.
11. Rewards: static code (pick a Shopify discount code), unique code (free shipping or discount), or custom (giveaway). Education steps exist; presenter does not use them (the welcome flow does that job).
12. Publish with the campaign toggle.
13. Smart test (optional automation): "Create smart test" > test pack "Optimization essentials": smart trigger on vs off; header and button copy (explicit offer vs "You've got a mystery discount" vs "exclusive offer" vs "special offer"; Aaliyah advises mystery or exclusive copy when the discount is 10% or less); first-step variants. It ends each test at significance, keeps the winner and starts the next. Manual tests available: trigger delay, header and button copy, custom content, remove mobile images, X button position, X button delay.
14. Reports: survey answers and "performance by survey answer" (example: health brand finds "lose weight" answerers buy more, so target that audience). [b9635f9e2351] `[needs brand data: purchase rate by quiz answer]`

### 3.5 Welcome flow (Klaviyo)

[4d6f11a9f443] [f2c3f6895ad4] [681426ed9a3a] [63691cee89e1] [d50bbcaf474a] [7f27679135bf] [cefa2905adfd] [38077a826b12] [18ddf0ee7ebf] [71218ab504b8]

Setup:
1. Flows > Create flow (top right) > search "welcome" > pick the email template that has a returning vs non-buyer split > select the list (Newsletter) > Use template. `[verify UI]`
2. Trigger: added to the main list (often "Newsletter").
3. Re-entry: off (a person gets the welcome series once).
4. Profile filter: placed order zero times over all time. Stops past buyers who re-subscribe from getting the welcome discount.
5. Delete the existing-customer branch and the conditional split.
6. Timing: Email 1A immediately > wait 8 hours (not the template's 3 days) > Email 1B > wait 16 hours (24 hours total) > Email 2 > wait 1 day > Email 3 > wait 1 day > Email 4 > wait 1 day > Email 5 > wait 1 day > Email 6.
7. On every email: smart sending OFF (it skips anyone emailed in the last 16 hours by default; the window is adjustable) and UTM tracking ON. Smart sending stays ON for campaigns.
8. Exits: the source only uses the entry filter above. It does not say whether buyers leave mid-flow. `[verify UI: add "placed order zero times since starting this flow" if you want buyers to exit]`

Email content:
- **1A (immediately): deliver the code.** Above the fold (what shows without scrolling, which "90% to 99%" of readers never go past): the offer, the code and a one-click CTA. Then 1 to 3 bestsellers or a "start here" pick. Trust builders if you have them (reviews, press, expert endorsements, social proof) and risk reversals (free shipping, free returns, guarantee, warranty, free trial). Keep the hero plain. Example "of Art": "Welcome to of Art. 10% off your first order. Use code SHOP10", short brand intro, code reminder, link to a collection, bestsellers, canvas editions, new arrivals, XL paintings, code and CTA again at the bottom.
- **1B (+8 hours): plain-text founder reminder.** Short, direct, human: "Hey, just making sure you saw your code." Code reminder, 1 or 2 product or category links (bestsellers, bundles, top categories, the most logical first purchase), a direct CTA. Presenter: a same-day second email drives "a surprising amount of incremental revenue" and is not too much.
- **2 (day 1): trust with substance, not "brand poetry".** Who you are, why trust you, why you over the alternatives they are comparing: founder story, mission, quality standards, ingredients, sourcing, craftsmanship or product philosophy, whichever fits. Discount reminder, founder presence only if credible, clear CTA. Keep it short. Example Freddy and Zoe: "Meet the human behind the cats. Hi, I'm Casper, the founder of Freddy and Zoe", founder photo with a cat, code reminder. `[needs brand data: founder story, proof of quality]`
- **3 (day 2): guide the first purchase.** People are overwhelmed and do not know what to buy. 1 to 3 bestsellers or collections, benefit-led, why they are the best place to start, welcome gift reminder (top bar and body). Example sports-nutrition brand: "Go further for longer with these bestsellers": energy bars ("50 grams of plant-based carbs to keep you moving"), gels ("fast energy with dual carbs for quick absorption"), drink powder ("hydration and endurance fuel in one"). `[needs brand data: bestsellers by first-order share]`
- **4 (day 3): objections and differentiation.** Answer the unasked questions: why you and not a competitor, why the price is fair, why trust the quality, why now. Core USPs, product or category differentiators, objection handling, discount reminder with a real deadline ("Hurry, this code expires in 48 hours"), a review. Example Empower Nutrition: "The difference is what's inside. Hint: only the cleanest ingredients."
- **5 (day 4): urgency plus social proof.** Deadline steps down (48 hours in email 4, "24 hours left" in email 5; or first deadline of 48 hours here if none before). 1 to 3 reviews that name a pain point or objection so the reader thinks "this is me". 1 specific review beats 3 generic "great product" reviews. `[needs brand data: reviews tagged by objection]`
- **6 (day 5): the close.** Final offer reminder, strong urgency, the strongest support angle (reviews, authority, or risk reversal; A/B test), what to buy. Test designed vs plain text. Alternative the presenter uses often: email 4 = 48 hours, email 5 = 24 hours, email 6 = plain-text founder note "we've extended your welcome discount for another 24 hours, but act fast".
- **After 6 (optional): evergreen campaign winners.** Do not cap the flow at 7 emails. Append past campaigns that performed well and are relevant all year: how-tos, blog promos, reviews, UGC, myth emails, product highlights, subscription promos, bundles, gift guides, educational emails. Expect modest extra revenue because momentum is in the first 72 hours. `[needs brand data: past campaign revenue ranking]`

### 3.6 Browse abandonment flow

[5ad3da1bdb3a] [c83fa5e0d0d6] [9d0646c87a39] [aaef1103dc77] [890a5c97d555] [8c9c22844f69] [d0e8f91819ba]

Setup:
1. Flows > Create flow > Essentials > Browse abandonment template > name it > Use template. `[verify UI]`
2. Trigger: Viewed Product.
3. Re-entry: allow after 30 days (cool-down).
4. Profile filters: checkout started zero times since starting this flow; placed order zero times since starting this flow; added to cart zero times since starting this flow. On Shopify, use the Shopify "Added to Cart" metric, not the API one. These filters are also the exits: a person who adds to cart, starts checkout or orders stops getting the flow.
5. First delay: Klaviyo default 2 hours. Test 30 to 45 minutes up to 2 hours (demo uses 1 hour).
6. Email 1 > wait 1 day > Email 2 > wait 1 day > Email 3 > wait 1 day > Email 4. (The one-day waits between 2, 3 and 4 are implied by cloning the delay.)
7. Dynamic product block in every email: open the default template in the editor, save its dynamic product block as universal content (for example "dynamic product block browse abandonment"), then restyle it to the brand. Faster than building from scratch.
8. No split between new and returning customers in most cases. Exception: extremely tight margins where you cannot afford any incentive to past buyers; then add a conditional split. `[needs brand data: contribution margin after discount]`

Email content:
- **1 (30 minutes to 2 hours): light reminder.** "You were looking at this. Are you still interested?" Not sales-heavy. Dynamic block with the viewed product, a Klaviyo product feed with 4 related products, social proof (reviews, UGC). Examples: "Still thinking about it? Return to store now"; a biscotti brand: "Don't let this delicious moment pass" with the product and UGC. Captures mainly high-intent browsers who got distracted.
- **2 (+1 day): remove friction, do not add pressure.** Buyer questions: is it worth the price, is it legit, will it fit, work or last, is there a better alternative? Lead with risk reversals (guarantee, trial, free shipping, free returns); if you have none, lead with social proof. Dynamic block. Most important for higher-AOV brands. Examples: Smokco "Feeling on the fence?" plus "Your order is 100% risk-free" with 3 reasons; Apparel Outpost "Still thinking about this one?" plus "every tee feeds 5 rescue dogs" plus a review.
- **3 (+1 day): escalate, but smartly.** Hesitation now means price sensitivity, comparison shopping or "I'll buy later". Option A: small discount with a 48-hour deadline, clean design, one CTA (worth it for most brands with healthy margins). Option B (replenishable products, subscriptions, bundles): "Subscribe and save 10%", "bundle and save", starter-kit discount, to protect margin. Dynamic block, optional product feed. Examples: "10% off just for you. Save 10% now"; Lost Interiors "Enjoy 10% off today. Use code SHOP10. Bring it home today" with 3 recommended products and a footer that points to their physical store.
- **4 (+1 day): last chance, plain text from the founder or a team member.** 24 hours left. Template: "Hi [name], [founder] here. Just a quick note to remind you that your exclusive X% off expires tonight at midnight. [CTA] Thanks again for checking out [brand], and I hope to see you back soon." Heavy design here "screams automation"; this is where most brands overdo it.

### 3.7 Abandoned cart and abandoned checkout flows

[d94eb68e5e18] [bdbde349add0] [4085ce710e47]

Setup (cart first):
1. Flows > Create flow > search "cart" (not in Essentials). On Shopify, pick the template with the Shopify "Added to Cart" trigger, not the generic or "manual icon" one. Name it, Use template. `[verify UI]`
2. Filters: checkout started zero times since starting this flow (cart flow only); placed order zero times since starting this flow; has not been in this flow in the last 30 days. The first two also act as exits.
3. First delay: Klaviyo default 4 hours is "way too long". Test 15 minutes to 1 hour (demo 30 minutes).
4. Remove the SMS step and the template's conditional split (SMS skipped in the demo).
5. Email 1 (+30 min) > wait 1 day > Email 2 > wait 1 day > Email 3 > wait (1 day) > conditional split: "placed order at least once over all time".
   - YES (returning customer): Email 4R, plain-text founder support check-in, no discount. Optional smaller discount if margins allow, plus a matching final reminder 1 day later.
   - NO (non-buyer): Email 4 discount opener, 48-hour deadline > wait 1 day > Email 5 final reminder, 24 hours left, plain text from the founder.
6. Checkout version: Clone the cart flow > name "abandoned checkout" > change trigger to Checkout Started > delete the "checkout started zero times" filter. Everything else stays the same.

Email content:
- **1 (15 minutes to 1 hour): simple reminder.** No discount, no overselling. Dynamic product block plus every risk reversal you have (guarantee, trial, free shipping, free returns). Example Spice Pots: "Looks like you left something tasty behind", the product, "Complete my order", 3 reasons "Why Spice Pots", "Complete my order". Presenter: converts most of the people who were only distracted.
- **2 (+1 day): plain-text founder check-in.** "Hey, noticed you were checking out this product. Just wanted to make sure you didn't run into any issues. By the way, here's why people love us." Then 1 core differentiator (guarantee, speed, quality, customer experience). 2 to 3 short paragraphs max. End with "Here's your cart if you still want it." Add risk reversals, or social proof if you have no strong risk reversal.
- **3 (+1 day, day 3): objection handling, not "our brand is awesome".** Name the real objections (worth the price? how long is shipping? what if it doesn't fit, doesn't work, isn't as good as the photos?) and answer each with a USP: price concern > durability, warranty, long-term value; trust concern > guarantee, certifications, press; comparison > how you differ. Dynamic block. Example Smokco: "Here's why customers choose Smokco", "Your saved cart is waiting", British-made quality, cheaper than cigarettes, 100% BPA free, highly rated service. `[needs brand data: top objections from reviews, support tickets, post-purchase surveys]`
- **4 non-buyer: clean discount, 48-hour deadline.** Dynamic block, optional product feed, one CTA. Example: "Take 10% off your cart? Yes please. Use code SHOP10. Complete your order before it's lost."
- **5 non-buyer: plain text, 24 hours left.** Example: "Hey, it's Melanie here, founder of Spice Pots. Just a personal check-in. Good news, you can still claim your offer with 10% off. Use code ... [Finish my order]." Closes first-time buyers who are "90% convinced" but need a deadline.
- **4 returning: concierge check-in.** "Hey, saw you were about to grab this. I just wanted to check in, everything good? Let me know if you have questions about sizing, specs, delivery." Works "extremely well" for higher-AOV brands. If you add a discount, make it smaller than the non-buyer one (example: non-buyers 10%, returning 5%) and add a final reminder email. Goal: loyal customers, not discount seekers.

### 3.8 Post-purchase flow

[58bdfe185e63] [5956a124a134] [b3058403e9f8]

Setup:
1. Flows > Create flow > template "Post purchase follow-up order count split" > name > Use template. `[verify UI]`
2. Trigger: Placed Order.
3. Filters: placed order zero times since starting this flow (a new order restarts the flow, so the old run stops); cancelled order zero times since starting this flow.
4. First delay: 10 minutes (not the template's 1 day). Shopify or WooCommerce already sent the transactional order and shipping emails.
5. Conditional split: "placed order equals 1 over all time": YES = first-time buyer, NO = returning. The template also splits at 2 orders, giving a 3+ order track; most brands only need first-time vs returning. More splits (2nd, 3rd, 4th order) suit some brands.
6. Smart sending OFF on every email ("skip recently emailed profiles"). Otherwise someone who bought from a campaign sent in the last hours misses the flow.

Email content (first-time track; returning track uses the same sequence with loyalty-focused wording):
- **1 (+10 minutes): thank you, plain text from the founder.** First-timers: thank them for trusting you, reassure them they chose well, make a memorable first impression. Returning: thank them for their loyalty. Confirm order progress, offer support, say what to expect. Optional cross-sell: even a plain link to the site gets "a really good placed order rate"; a specific product recommendation works well.
- **2 (+2 days after email 1): "your order is on its way".** Build excitement, reinforce the value, reduce buyer's remorse, recommend add-ons (static blocks or Klaviyo product feed), end with "Shop all". Examples: Spice Pots "Flavor on the way. Your Spice Pots are on the way. We're excited for you. While you wait, check these out" (refills, cookbook, candle, kit); a nutrition brand "Complete your fitness nutrition. Treat yourself to something extra" (isolate with creatine, multivitamin with collagen, isolate with collagen plus); a saber brand "Explore more sabers" with recommendations and a "mystery saber" for curiosity. `[needs brand data: shipping times; frequently bought together pairs]`
- **3: how-to, split by product or category.** Personal to what they bought: clear tips, reassurance, optional links to FAQs, manuals, videos. Reduces returns. Apparel may need only care instructions and no split; technical products need in-depth guides. Examples: Smokco "Getting started with your smoker e-cigarette" (use in 3 steps, when to change the refill, recharging the battery); a tea brand shows how to brew and links to a blog on temperatures and steep times.
- **4 (optional): social follow push.** More channels (email, SMS, social) = more touch points = higher repurchase. Examples: "Let's get social. Join the silly party on social media. Follow now" (with a cash prize for tagging the brand); Saber Pro "Be part of the Galaxy" with Instagram and Facebook buttons.
- **5 (optional): loyalty program push.** State the benefit at once (usually discounts). Example Smokco: "Earn points, save money with Smoke Points. Earn rewards every time you shop, review and refer a friend." Presenter expects loyalty programs to matter more in coming years. `[needs brand data: loyalty program terms]`
- **6 (after delivery): personal plain-text check-in from the founder.** "How did everything go with your order?" Offer support; guide back to the site. Presenter: "one of the emails that generates the most revenue".
- Timings for emails 3 to 6 are not given. `[needs brand data: delivery time to set email 6 after delivery]`

### 3.9 Plan a month of campaigns

[6a19f9f385b5] [071d76074c86] [5886ee2c2f40] [e932614a8a69] [dc7147515105] [e5552f0a655e] [7a4e669c2511] [3e4696a51c71] [bd8384e14e34] [7f77b49944bc] [4e9a379a0375]

0. Set up a calendar tool: Notion (visual, flexible; the agency used it 4 years), Airtable (the agency's current tool; better filtering across many clients), ClickUp or Monday (if the team already works there), or Google Sheets ("really underrated"). Fields per campaign: send date, campaign type, segment, status (idea, copywriting, design, implementation, ready to review, scheduled, sent), owner.
1. Lock fixed dates first: product launches, back-in-stock, planned sales or promotions, brand milestones and announcements. Maximum 1 sales event a month; every other month is better.
2. Optional: add holidays and awareness days that fit the brand (nationaltoday.com, search the month). 1 to 2 date-based emails a month at most; no discount needed. Example: a coffee brand uses National Coffee Day, and could use World Sleep Day or National Productivity Day if the positioning fits. `[web check: awareness dates for the month]`
3. Map existing content (blogs, YouTube, social posts, podcasts) to the right season (summer skincare blog in May or June, not November). Per piece, either tease it and link to the full content, or summarise the takeaway and link to a product. Test or mix. No content? Google topics your audience cares about and write a short educational email; you only need to present it clearly and tie it to the brand. `[needs brand data: content library]`
4. Fill the rest with AI (presenter prefers Claude; ChatGPT or Gemini also work). Context block: brand name and what you sell; target customer (who, what they care about, their problems); frequency (3 to 4 a week); the month; fixed dates; content already placed; the 91 campaign types. Prompt: "I run an e-commerce brand called [brand] that sells [products]. Our target customer is [customer description]. We send 3 to 4 email campaigns per week. I'm planning the month of [month]. Here are the dates already locked in: [fixed dates]. Here's a full list of campaign types I can choose from: [91 campaign list]. Please fill in the remaining slots for the month with specific campaign ideas from the list that make sense for our brand and audience. For each one include the send date, campaign type, and a two-line description of the angle." Expect about 80% usable. Check each idea: does it fit the brand now; do we have the content, images and reviews; is the mix balanced across the 7 buckets? Swap misfits. About 10 to 20 minutes per month.
5. AI pressure test (about 2 minutes): "Here's my email campaign calendar for [month]: [calendar]. Review the mix across campaign types and the weekly cadence. Flag anything that looks unbalanced, repetitive, or too promotional, and suggest alternatives where needed."
6. Manual mix check. Month: 1 to 2 promotional, 4 to 6 product, 4 to 6 value or education, 2 to 4 social proof, 2 to 4 brand. If more than one third is promotional, replace some with content or social proof. Week: no 2 consecutive emails of the same type. Example for 4 sends a week: Monday education, Wednesday product, Friday social proof, Sunday brand.
7. Stay 2 weeks ahead: emails for 2 weeks out are written, designed and sitting in Klaviyo for review. Last-minute work defaults to promos and lets mistakes through.
8. Month-end review, 20 to 30 minutes: highest open rates, most clicks and revenue, underperformers and why. Look for patterns, not a deep study. Feed them into next month.
9. Audience for every campaign: an engaged segment (see 3.12), not the whole list. SMS only for launches, restocks and sales. [bb790bf6e145] [b9130f4f4dca]

### 3.10 Test a flow time delay in Klaviyo

[0528a2003316] [700ad4cccb44]

1. Test email 1's delay first; test the whole delay structure only after.
2. In the flow, add a conditional split set to "random sample 50%". YES branch waits one duration (for example 2 hours); NO branch waits another (for example 30 minutes). `[verify UI]`
3. Starting ranges for email 1: site abandonment 1 to 4 hours; browse 30 minutes to 2 hours; cart 15 minutes to 1 hour; checkout the same as cart (see section 9 on the "50 minutes" wording).
4. Structure test: regular (1 email a day) vs aggressive (every 12 hours). Aggressive "works really well" for some brands.
5. Wait for at least 1,000 recipients per branch (500 only if the gap is huge); about 2 weeks. Decide on revenue.

### 3.11 Set up a campaign A/B test in Klaviyo

[ac370b420628] [4290660b631a]

1. Winning metric: placed order rate. Test size: 100% (50% variant A, 50% variant B). Winning variation rollout: 0%. `[verify UI]`
2. Do not use the automatic option (for example 20% A, 20% B, winner to the other 60% after 4 hours): the majority gets the email at a worse time, and 2 to 4 hours is too short to pick a winner, especially on revenue.
3. Analyse after a couple of days; apply the learning to future sends.
4. Send-time tests: run at least 5 exploratory tests to find the pattern. Judge on revenue or placed order rate, not open rate (7 a.m. may win opens while 2 p.m. wins revenue). `[needs brand data: send-time history]`

### 3.12 Build the core segments in Klaviyo

Lists and segments > Create > Segment. Start every segment with "Person can receive email marketing". In the EU also add "because person subscribed" (or keep 2 versions), since someone can be emailable without consent (for example a checkout email entry, or a purchase without marketing consent). Subscribed people usually engage better even in the US. Mind OR vs AND: OR = any condition qualifies; AND = all must be true. The presenter sees this "go wrong all the time". [516248e6ac94] [6e06d938ff3f] [951b0132a90b] [336b88ac711f] [3ffe21f635f9] `[verify UI]` `[web check: GDPR consent rules for your markets]`

| Segment | Conditions (as given) | Use |
|---|---|---|
| Engaged 90 days | can receive email marketing AND (opened email at least once in last 90 days OR clicked email at least once in last 90 days OR placed order at least once in last 90 days OR checkout started at least once in last 90 days OR active on site at least once in last 90 days) | Main campaign audience; usually 50%+ open rates. Clicked is included because open tracking can fail. Placed order and checkout started are included because a direct-to-checkout visit may not log "active on site". Viewed product and added to cart are not needed (covered by active on site). Some brands use email activity only. |
| Engaged 14, 30, 60, 120 days | clone of engaged 90 with the window changed (also 150, 180 in the repair plan) | Deliverability repair ladder; widen to 120 if 90-day opens reach 60% to 70% |
| Marked as spam (exclude) | can receive email marketing AND marked email as spam at least once over all time | Exclude from every campaign; suppress |
| Bounced (exclude) | (bounced email at least 4 times over all time where bounce type = soft) OR (bounced email at least once over all time where bounce type = hard); AND can receive email marketing | Exclude from every campaign; suppress |
| All but unsubscribed and suppressed | can receive email marketing (EU: because person subscribed) AND email does not contain "q.com" (bot addresses, as transcribed) AND marked email as spam zero times over all time | Send 1 to 2 emails a month to the whole list so unengaged people get a chance to come back. Never send campaigns to lists. |
| Unengaged 120 days | opened email zero times in last 120 days AND clicked zero times in last 120 days AND placed order zero times over all time AND checkout started zero times in last 120 days AND active on site zero times in last 120 days | Trigger for a sunset flow (flow not built in the source). Past buyers are kept on the list on purpose. |
| Unengaged 180 days | same, with 180 days | Exclusion segment; suppress over time (better deliverability, lower Klaviyo bill) |
| First-time buyers | placed order equals 1 over all time AND can receive email marketing | Second-purchase offers |
| Returning customers | placed order at least 2 times over all time AND can receive | Loyalty messages that differ from first-timers |
| Non-buyers | placed order zero times over all time | In a sale, give non-buyers an extra discount on top; customers do not get it |
| VIPs | for example placed order at least 4 times over all time, or total spend at 3 to 4x AOV | Brand-specific; no universal definition `[needs brand data: order-count and spend distribution, AOV]` |
| High potentials | (checkout started OR added to cart OR viewed product OR active on site at least once in last 30 days) AND placed order zero times in last 30 days | Base for a flow or a one-off special-offer campaign |
| Win-back customers | placed order at least once in last 6 months AND zero times in last 90 days | Base for a win-back flow (not built in the source) or a one-off campaign |

Klaviyo's own segment library is worth a look, with caveats: its "Engaged 30 days email" uses email activity only, "because person subscribed" and a "subscribed in the last 15 days" clause (the presenter drops that clause; the welcome flow covers new subscribers). Its "Refunds" segment (refunded order at least once over all time) can be useful to target. [516248e6ac94]

### 3.13 Fix deliverability in 4 steps

[75378f892825] [e758ab334635] [6dcb0bfce104] [df98522f016b] [31b2f58bfc95] [660cfc96df62] [91d6fd433f58] [4933eedd5bb2]

Diagnose first:
1. If campaign open rates sit below about 30% to 35%, you likely have a placement problem. Healthy brands sending to engaged segments see 50%+.
2. Placement test: GlockApps. Send a test campaign to its seed list; read inbox vs promotions vs spam share, blocklist status and IP reputation. Run monthly. It also has a free spam checker (send an email to its address and get a report) and a free DMARC checker. `[web check: GlockApps current tools and pricing]`
3. Or in Klaviyo: open the last 5 campaigns > Deliverability tab: open, click, bounce, unsubscribe and spam complaint rates; "performance by inbox provider" (Gmail may be fine while Hotmail or Outlook is not); "performance by country" (if one country is bad, send only a tighter engaged segment there for a while). `[verify UI]`

Step 1: technical setup (required, rarely the main fix).
1. Branded sending domain: Settings > Account > Domains > add your root domain > add the DNS records it lists > wait until it shows live. Presenter calls it mandatory. `[verify UI]`
2. Default sender address on that domain (for example name@yourdomain.com).
3. DMARC: in DNS add a TXT record named `_dmarc` with the value shown in the video (not transcribed). Often the missing piece in audits. DMARC uses SPF and DKIM to check that mail is authentic. Verify with a DMARC checker (GlockApps free tools; "pass" means it is set). The source gives no SPF or DKIM steps beyond what the branded domain setup adds. `[web check: current DMARC policy value and Google/Yahoo sender requirements]`
4. Optional BIMI: shows your logo in the inbox and, in Gmail, a blue check for verified senders; supported by Gmail, Yahoo and some Apple versions; about $1,500 a year; bimigroup.org. Worth it for 8- and 9-figure brands, sometimes 7-figure. `[web check: BIMI certificate cost and requirements]`

Step 2: clean the list. Many brands have huge lists with only 10% engaged. Build 5 segments and suppress their members (three dots > Suppress current members > Bulk suppress; takes about 1 to 2 hours to update). `[verify UI]`
1. Unengaged (as spoken): opened email zero times in the last 90 days, clicked email zero times, active on site zero times in the last 180 days, placed order zero times in the last 365 days, received email at least 10 times in the last 180 days, can receive email marketing. (Windows are mixed in the transcript; see section 9.)
2. No email in a year: first active or created at least 1 year ago AND received email zero times in the last year AND active on site zero times in the last year AND can receive email marketing.
3. Never emailed: first active or created at least 1 year ago AND received email zero times over all time AND can receive email marketing.
4. Marked as spam at least once over all time.
5. Bounced: soft at least 4 times over all time OR hard at least once over all time. Hard bounce = address cannot be reached; soft = temporary problem, allow 4 tries.
Result: an engaged or partly engaged list, lower Klaviyo cost, and no more mail to people who hurt your reputation.

Step 3: rebuild reputation with an engagement ladder.
1. Build engaged 14, 30, 60 and 90 day segments (opened OR clicked OR placed order OR checkout started OR active on site in the window). If spam problems are severe, use opened or clicked only.
2. Weeks 1 to 2: turn off all flows except welcome, post-purchase and the abandonment flows (site, browse, cart, checkout). Send 3 campaigns a week to engaged 14 days (6 emails).
3. Check the 6 open rates. At or above 50%: move up. Below 50%: 2 more weeks at 14 days. Still below: remove website activity from the engaged segments.
4. Engaged 30 days for 2 weeks (6 emails). A small dip is normal; if it stays about 50%, move to 60 days; if it drops below 50%, stay 2 more weeks.
5. Engaged 60 days for 2 weeks, same gate, then engaged 90 days.
6. At engaged 90 days: make it the main campaign audience and turn all flows back on.
7. If opens trend toward 60%, you may widen to 120, 150 or 180 days while opens stay above 50%, but keep most sends at 90 days.

Step 4: make emails readable for Gmail's AI (Gemini).
1. Do not rely on image-only emails. Alt text must describe the image and include any offer text (for example "Person eating pizza" or "50% off, use code ...").
2. Use Klaviyo's native product blocks (live text) instead of designed image product blocks.
3. Live-text top bars for offers, not image bars.
4. Live-text footer: category links, loyalty status, store locator, support info.
5. Send plain-text emails regularly (1 to 3 a month). Do not drop design; just make sure the email makes sense without images.

Ongoing engagement habits: conversational subject lines ("would a friend send this subject line to a friend?"); short emails and short body copy; a strong above-the-fold section with a big CTA (presenter: "99%" never scroll further); fewer promotions (not a promo every week); 1 to 3 plain-text emails a month; category links in the footer ("guaranteed" higher clicks); 3 to 5 products at most, for example a 2x2 grid, each with a "Shop now" button, ending with "Shop all"; invite replies ("Ask us anything" campaigns). Focus on what subscribers want, not only on what you want to sell.

### 3.14 Analyse Klaviyo exports with AI

[7dccf4216521] [87afe3ecbaf6] [a0d2e94690df] [af644216425f]

1. Campaign export: Campaigns > three dots > Export analytics > time range (year to date, or at least last 90 days; longer if you send few campaigns) > email only > include all A/B test message variations > export CSV. `[verify UI]`
2. Prompt (presenter used ChatGPT here): "You're an email marketing data specialist, and I want you to analyze this data set, which includes all the information of email campaigns we've sent for [company URL]. Can you analyze this data set and give me 10 observations with recommendations on how to improve it?"
3. Flow export: Flows > Options > Export analytics > time range (at least last 90 days or year to date) > aggregate by day > include all A/B test message variations > export CSV. `[verify UI]`
4. Prompt: same wording with "email flows we've sent for [brand URL] in the past few months" and "20 observations".
5. Drill-down prompt: "Now focus more on the welcome series flow and give me 10 findings and recommendations."
6. Treat findings as hypotheses. Check them against the raw CSV (card caveat) and turn them into controlled tests. For send-time findings, optimise placed order rate, not open rate: mornings may get more opens, evenings more purchases. `[needs brand data: Klaviyo campaign and flow exports]`

## 4. Rules, thresholds and numbers

| Rule | Number or threshold | Condition | Source's basis | Card |
|---|---|---|---|---|
| Store conversion without capture | 2% buy, 98% leave | Typical paid-traffic funnel | Presenter's framing | [aa555d450d5a] |
| Signup rate: industry standard | 1% to 3% | Default templates | Presenter claim | [aa555d450d5a] |
| Signup rate: target ("high converting") | 8% to 12% (Klaviyo forms "6% to 12%" elsewhere) | After offer and form testing | Agency experience | [aa555d450d5a] [0590112c25d0] |
| Signup rate with Aaliyah | "up to 20%" seen | Full-screen, gamified, smart triggers | Agency clients, vendor tie | [b9635f9e2351] |
| Welcome flow conversion of new subscribers | 10% to 20% | Strong form and welcome flow | Presenter claim | [aa555d450d5a] |
| Minimum discount that works | under 10% off "won't be as effective" | General heuristic; test | Opinion | [aa555d450d5a] |
| $ off vs % off | At $200 AOV, $20 off beats 10% off | Higher perceived value; test | Opinion | [aa555d450d5a] |
| Mystery discount copy | Use when discount is 10% or less (Aaliyah); under 20% off (presenter); also "50% off or less" | Test vs explicit offer | Vendor advice plus opinion; inconsistent | [020eec5d0a13] |
| Form time delay | 6 s start; test 4 to 12 s; Aaliyah test 4 s vs 12 s first | Desktop and mobile | Agency tests | [c5e1f30dd58d] [143e7458c1be] |
| Scroll trigger | 60% start; test 30% to 90% | Desktop and mobile | Agency tests | [c5e1f30dd58d] [0590112c25d0] |
| Re-show after close | 3 days (Klaviyo default 5) | Klaviyo form | Preference | [c5e1f30dd58d] |
| Popup suppression | "don't trigger if another popup viewed in last 15 s" | Several popups on site | Example setting | [ba6a52eba2e9] |
| Mobile form sizes | CTA height 70, CTA text 30, "No thanks" 18, offer text 60, input height 70, input text 20, success text 22 | Klaviyo mobile clone | Presenter's working values | [c2e8c7484a70] |
| Micro-yes step | On by default; "in most cases" lifts signups | Test per device | 40+ client brands | [e912865caec2] |
| Scratch-off example | 11% to 14% signup conversion | One brand, single change | Anecdote | [d80edbbaaf50] [7da3ea843dc6] |
| Success page spam line | "within 5 minutes" | Code sent by email | Support-ticket prevention | [1f8be190a019] |
| Form test sample | 3,000 to 5,000 impressions per variant or 15 days, whichever longer; 7 days sometimes | Signup forms | Agency guideline | [59ae581e3e7f] [e8e1adc8fefe] |
| Flow test sample | 1,000 recipients per variant; 500 if gap is massive; about 2 weeks | Flows | Agency guideline | [e8e1adc8fefe] |
| Testing cadence | New test every 2 to 4 weeks | Faster at >$100k/month revenue than at $10k/month | Agency guideline | [59ae581e3e7f] |
| Revenue as test metric | Decides "95%" of tests | All tests | Opinion | [59ae581e3e7f] |
| Flow share of email revenue | 40% to 70% | Typical account | Agency claim | [700ad4cccb44] |
| Welcome revenue window | Most in first 72 hours; day 0 highest | Across accounts | Client screenshots | [f2c3f6895ad4] [580319f842a5] |
| Welcome timings | 1A at 0 h, 1B at 8 h, 2 at 24 h, then daily to email 6 | Welcome flow | Agency template | [f2c3f6895ad4] [4d6f11a9f443] |
| Above-the-fold readers | "90% to 99%" (also "99%") see only above the fold | Any email | Estimate | [681426ed9a3a] [660cfc96df62] |
| Welcome deadlines | 48 h (email 4), 24 h (email 5), +24 h "extension" (email 6) | Only if true | Agency template | [cefa2905adfd] [38077a826b12] [18ddf0ee7ebf] |
| Smart sending | OFF for all flow emails; ON for campaigns; default window 16 h | Klaviyo | Preference | [4d6f11a9f443] [58bdfe185e63] |
| Browse first delay | 30 to 45 min up to 2 h (default 2 h) | Browse flow | Agency tests | [c83fa5e0d0d6] |
| Cart and checkout first delay | 15 min to 1 h (default 4 h "way too long") | Cart, checkout | Agency tests | [d94eb68e5e18] |
| Site abandonment first delay | 2 to 4 h (flows section); 1 to 4 h (testing section) | Site abandonment | Inconsistent in source | [c83fa5e0d0d6] [0528a2003316] |
| Aggressive delay structure | Every 12 h vs daily | Cart flow test | Works "for some brands" | [0528a2003316] |
| Flow re-entry cool-down | 30 days | Browse, cart, checkout | Preference | [5ad3da1bdb3a] [d94eb68e5e18] |
| Abandonment discount deadlines | 48 h then 24 h | Browse 3 to 4; cart non-buyer 4 to 5 | Agency template | [8c9c22844f69] [4085ce710e47] |
| Returning-customer cart discount | None by default; if any, smaller (10% non-buyer vs 5% returning; also "50% vs 5% to 10%") | Solid margins only | Opinion | [4085ce710e47] |
| Recommendation feed | 4 related products | Browse email 1 | Template | [9d0646c87a39] |
| Post-purchase first email | 10 min after order | Post-purchase | Preference | [58bdfe185e63] |
| Post-purchase email 2 | 2 days after email 1 | Adjust to shipping time | Preference | [58bdfe185e63] |
| Repeat purchase window | Most returning customers buy within 30 days | Client screenshots | Anecdotal | [b3058403e9f8] |
| Retention stats | Retained customers 9x likelier to convert; repeat customers spend 67% more; 95% of customers with proactive post-purchase communication "less likely to return" | Uncited "research" | Unverified | [5956a124a134] [b3058403e9f8] `[web check: original studies]` |
| Campaign frequency | 3 to 4 a week; 1 to 2 too few; 5 to 7 too many | Engaged segments | 120 brands, 7 years | [7a1145af87dc] [8db768330eb7] |
| Campaign buckets | 7 | Calendar planning | Framework | [9bbb999b4ec9] |
| Campaign ideas | 91 types | Enough for a year at 3 to 4 a week | Idea list | [e756efb90a3f] [50432b3f5d6e] |
| Monthly mix | 1 to 2 promo, 4 to 6 product, 4 to 6 education, 2 to 4 social proof, 2 to 4 brand | Most brands | Heuristic | [e5552f0a655e] |
| Promo ceiling | No more than 1/3 of sends | Monthly | Heuristic | [e5552f0a655e] |
| Sales events | Max 1 a month; every other month better | Calendar | Opinion | [071d76074c86] |
| Date-based emails | 1 to 2 a month max | Awareness days | Opinion | [6a19f9f385b5] |
| Same-type spacing | No 2 consecutive emails of the same type | Weekly | Heuristic | [7a4e669c2511] |
| Production buffer | 2 weeks ahead | Campaigns | Opinion | [3e4696a51c71] |
| Monthly review | 20 to 30 min | Month end | Presenter's cadence | [bd8384e14e34] |
| AI planning time | 10 to 20 min per month; output "80%" usable | With context block | Presenter experience | [e932614a8a69] |
| Send-time exploration | At least 5 tests | Campaigns | Guideline | [4290660b631a] |
| Engaged windows | 14, 30, 60, 90 (main), 120, 150, 180 days | Campaign audiences | Agency structure | [6e06d938ff3f] [df98522f016b] |
| Full-list sends | 1 to 2 a month to "all but unsubscribed and suppressed" | Re-engagement chance | Preference | [951b0132a90b] |
| Bounce suppression | Hard: 1; soft: 4 | All time | Agency rule | [951b0132a90b] [6dcb0bfce104] |
| Unengaged / suppression | 120 days = sunset trigger; 180 days = exclude and suppress; past buyers kept | Never-buyers only | Agency rule | [336b88ac711f] [4933eedd5bb2] |
| List-clean segment 1 | Received 10+ emails in last 180 days, no opens, clicks or site visits, no order in 365 days | Suppress | Agency rule (windows garbled) | [6dcb0bfce104] |
| Placement red flag | Opens below 30% to 35% | Campaigns | Heuristic | [75378f892825] |
| Open rate KPI | Minimum 45%; ideally 50%+ | Engaged segments | Agency target | [91d6fd433f58] |
| Repair ladder gate | 50% open rate to advance; 2 weeks and 6 sends per stage | Deliverability repair | Agency plan | [df98522f016b] |
| Click rate KPI | Transcript: "5% or higher" then "0.5 is all good"; rejects Klaviyo's "1% or 1.2%" | Campaigns | Opinion; likely 0.5% | [91d6fd433f58] [660cfc96df62] |
| Spam complaint KPI | "0.01% or lower" (spoken "001%") | Campaigns | Agency target | [91d6fd433f58] `[web check: Google bulk sender spam-rate limits]` |
| Unsubscribe KPI | 0.3% or lower; less important since Gmail one-click unsubscribe | Campaigns | Opinion | [91d6fd433f58] |
| Engaged share of big lists | Often only 10% engaged | Brands proud of list size | Observation | [6dcb0bfce104] |
| Plain-text frequency | 1 to 3 a month | Campaigns | Preference | [31b2f58bfc95] [660cfc96df62] |
| Products per email | 3 to 5, 2x2 grid, each with "Shop now", end with "Shop all" | Product sections | Preference | [660cfc96df62] |
| BIMI | About $1,500 a year; 8 to 9 figure brands, sometimes 7 | Optional | Presenter quote | [e758ab334635] |
| Suppression processing | About 1 to 2 hours | Bulk suppress | Observation | [6dcb0bfce104] |
| SMS use | Launches, restocks, sales only | Especially outside US | Opinion | [b9130f4f4dca] |
| SMS signup offer | Same offer; higher (email 10% vs SMS 20%, also "15%/50%" in another part); VIP club | Test | Test options | [4c956b5e96a1] [8bb0c8c613c5] |
| VIP definition | 4+ orders or spend 3 to 4x AOV | Brand-specific | Example | [3ffe21f635f9] |

## 5. Diagnostics and checks

| Check | How | Good | Bad | Next step | Cards |
|---|---|---|---|---|---|
| Which layer is broken | Walk the 6 layers in order: signup, flows, campaigns, tests, segmentation, deliverability | Each layer exists and performs | Missing flows, random campaigns, fixes without knowing the cause | Fix the earliest broken layer first, one at a time | [93e33dec853f] [5a08594d02a9] |
| Monetization leak | Compare blended CAC trend, retargeting spend, and welcome flow first-purchase conversion | Welcome flow captures first-time intent | Rising CAC, heavy retargeting, email judged only on topline | Rebuild form and welcome flow before buying traffic | [9ed0b65913bb] `[needs brand data: blended CAC, retargeting spend]` |
| Signup rate | Klaviyo form analytics (or Aaliyah submit rate) per device | 8% to 12% (Aaliyah up to 20%) | 1% to 3% | Run the ranked form tests (offer first) | [aa555d450d5a] [0590112c25d0] |
| Form audit | Check against the 10 mistakes (section 8) | None present | Any present | Fix offer first, then the rest | [39aa68c94680] |
| Offer quality | For each offer: signup rate, total signups, welcome flow CVR, welcome revenue, margin | Higher total revenue at acceptable margin | Higher signup rate but welcome CVR collapses | Keep, or revert to old offer | [aa555d450d5a] [0590112c25d0] |
| Form QA before launch | Preview animations, iPhone and 4K previews, live-site preview, teaser look | Renders cleanly, offer readable | Overlaps widgets, fonts too small | Adjust sizes and teaser shape | [6f18ca80ca5c] |
| Welcome revenue by day | Klaviyo "conversion by days from subscription" | Most revenue days 0 to 3 | Revenue spread thin, long drip | Front-load emails into 72 hours | [f2c3f6895ad4] |
| Welcome revenue by email | Flow export per email | Email 1 dominant, later emails add some | Later emails at zero revenue | Reposition or cut them; test email 1 first | [a0d2e94690df] |
| Flow settings | Open each flow: trigger, filters, re-entry, smart sending, UTM | Filters as in section 3; smart sending off | Smart sending on; no "placed order" filter; generic add-to-cart metric on Shopify | Fix settings | [4d6f11a9f443] [5ad3da1bdb3a] [d94eb68e5e18] [58bdfe185e63] |
| Under-monetized flow | Compare open, click and order rate per flow | Clicks track opens | Example: browse 42% open, 2.3% click | Add dynamic product blocks, one hero CTA; SMS follow-up for non-clickers if SMS revenue per recipient is strong (example 1.70 euro) | [af644216425f] |
| Test validity | Recipients or impressions per variant, days run, metric used | Meets sample rules; judged on revenue | 50 to 100 recipients; winner by opens; auto winner after hours | Keep test running; switch to manual 50/50 | [59ae581e3e7f] [e8e1adc8fefe] [ac370b420628] |
| Campaign mix | Count sends per bucket for the month; check consecutive types | Promo under 1/3; no back-to-back same type | Promo-heavy; clusters | Swap in education or social proof | [e5552f0a655e] [7a4e669c2511] |
| Campaign audience | Look at the segment on each send | Engaged segment plus spam and bounce exclusions | Whole list, or a list instead of a segment | Rebuild segments | [bb790bf6e145] [951b0132a90b] |
| Segment logic | Read each condition group | Engaged = OR; unengaged = AND | Mixed-up AND/OR | Rebuild | [516248e6ac94] [336b88ac711f] |
| Placement | Campaign open rates; GlockApps seed test monthly; Klaviyo Deliverability tab by provider and country | 50%+ opens on engaged; inbox not spam | Below 30% to 35%; one provider or country much worse | Run the 4-step fix; tighter segment for the bad country | [75378f892825] |
| Authentication | Klaviyo Domains page; DMARC checker | Branded domain live; DMARC passes | Shared sending domain; no DMARC | Add domain and DMARC TXT | [e758ab334635] |
| List health | Size of the 5 cleaning segments vs total list | Small dead-weight share | Big list, about 10% engaged | Bulk suppress | [6dcb0bfce104] |
| KPI health | Campaign averages | Opens 45% to 50%+, clicks about 0.5%+, spam 0.01% or lower, unsubscribes 0.3% or lower | Below these | Tighten audience, improve above-the-fold and plain-text mix | [91d6fd433f58] |
| AI readability | Look at the email with images off | Offer, products, footer readable as live text | Offer only inside an image | Add alt text, native product blocks, live top bar and footer | [31b2f58bfc95] |

## 6. Tools, settings and named features

- **Klaviyo signup forms** `[verify UI]`: form types popup, full page, flyout, embed, banner (flyout never beat popup in the agency's tests); categories email, SMS or both; timing "immediately" vs "based on rules" (exit intent, time delay, scroll %, pages viewed, "all conditions must be met" toggle); frequency "show again after" (default 5 days); devices (desktop only, mobile only); targeting "don't show to existing Klaviyo profiles", URL include or exclude, UTM, location; teaser (style rectangle, circle or corner; behavior before form, after close, or both); Edit styling (input field and text styles, fonts); close X size and colour transparency; Clone step; Clone form; Create A/B test with manual or automatic weight and winner selection. [c5e1f30dd58d] [53f37df1584e] [00de729163a8]
- **Klaviyo flows** `[verify UI]`: Create flow templates (welcome with returning/non-buyer split, browse abandonment in Essentials, cart found by search, "Post purchase follow-up order count split"); triggers Added to List, Viewed Product, Shopify Added to Cart (vs API or manual add to cart), Checkout Started, Placed Order; profile filters with "since starting this flow" and "over all time"; re-entry settings; time delays; conditional splits including "random sample 50%"; smart sending ("skip recently emailed profiles", default 16 hours); UTM tracking; dynamic product block; universal content; Klaviyo product feed (recommendations from purchase and viewing history); sender name per email. [4d6f11a9f443] [c83fa5e0d0d6] [0528a2003316] [2176f28aa94d]
- **Klaviyo campaigns** `[verify UI]`: A/B test with winning metric (placed order rate), test size, winning variation %; Export analytics (time range, email or SMS, include all A/B variations). [ac370b420628] [7dccf4216521]
- **Klaviyo lists and segments** `[verify UI]`: condition "Person can receive email marketing" and the "because person subscribed" option; OR/AND groups; condition clone button; metrics opened email, clicked email, placed order, checkout started, active on site, viewed product, added to cart, marked email as spam, bounced email (bounce type soft or hard), received email, refunded order, first active / created date; properties (email contains text); segment library; three dots > Clone; three dots > Suppress current members > Bulk suppress. [516248e6ac94] [951b0132a90b] [6dcb0bfce104]
- **Klaviyo deliverability** `[verify UI]`: campaign Deliverability tab (open, click, bounce, unsubscribe, spam complaint rates; performance by inbox provider; performance by country); Settings > Account > Domains for branded sending domain; default sender address. [75378f892825] [e758ab334635]
- **Aaliyah** (Shopify app; presenter promotes it with a trial link) `[verify UI]`: dashboard (email submit rate, phone submit rate, attributed sales, views, visitor funnel); Campaigns (each popup); A/B tests page; Reports (survey answers, performance by survey answer); Settings; Integrations (Shopify, Klaviyo, Omnisend, Postscript, Attentive, Sendlane, Yotpo); templates; brand theme; floating button; first steps (mini quiz, spin to win, scratch-off, micro-commitment, none); fields and legal links; reward display; single vs double opt-in; triggers (delay, scroll, exit intent, smart triggering); re-trigger and popup-overlap rules; device previews; Preview; targeting rules (new vs returning visitors); Rewards (static, unique, custom); Education; Smart test with "Optimization essentials" pack. [b9635f9e2351] [143e7458c1be] [ba6a52eba2e9] [6f18ca80ca5c] [020eec5d0a13]
- **Shopify / WooCommerce**: transactional order and shipping emails (reason for the 10-minute post-purchase delay); Shopify discount codes used as static rewards. [58bdfe185e63]
- **Image compression**: tinypng.com, squoosh.app. [8b8c3454e9e7]
- **Calendar tools**: Notion, Airtable, ClickUp, Monday, Google Sheets. [7f77b49944bc] [4e9a379a0375]
- **nationaltoday.com**: awareness days by month. [6a19f9f385b5]
- **AI assistants**: Claude (presenter's pick for calendar planning), ChatGPT (used for the export analyses), Gemini. [e932614a8a69] [7dccf4216521]
- **GlockApps** ("Clock Apps" in transcript): seed-list inbox placement test, blocklists, IP reputation, free spam checker, free DMARC checker, paid plan. [75378f892825] [e758ab334635] `[web check: current features and price]`
- **DNS**: TXT record `_dmarc`; branded sending domain records. [e758ab334635]
- **BIMI** (bimigroup.org): logo in inbox, Gmail blue check; Gmail, Yahoo, some Apple clients. [e758ab334635]
- **Gmail features named**: Promotions tab, AI inbox (summaries, grouping, ranking), Gemini reading email text, one-click unsubscribe. [31b2f58bfc95] [91d6fd433f58] `[web check: what Gmail currently does with marketing mail]`
- **SMS and WhatsApp**: SMS costs higher outside the US; WhatsApp cheaper per message in most European markets and "still early" for ecommerce. [b9130f4f4dca] `[web check: SMS and WhatsApp per-message pricing by market]`

## 7. Examples and case results

All are examples from the presenter's clients or demos, not promises.

- Scratch-off in Aaliyah: one brand from 11% to 14% signup conversion from that change alone. [d80edbbaaf50]
- Form image test: a dog image did "way, way better" than no dog for one client; the presenter says not to generalise it. Image hierarchy observed: pets, then human faces, then static product shots; people looking toward the headline act as a visual cue. [4c956b5e96a1] [ef89709e3516]
- Plain simple forms (white background, black CTA, grey input) usually beat fully designed forms. [0590112c25d0]
- First-person CTA ("Claim my deal", "Unlock my discount") usually beats "your". Default headline used: "Claim your mystery discount". Default microcopy: "No thanks, I'd rather pay full price". [0590112c25d0]
- Welcome emails: "of Art" (plain 10% hero, "conversion is just crazy", no number); Freddy and Zoe founder email with a cat; sports-nutrition bestseller email; Empower Nutrition "The difference is what's inside" with a 48-hour code. [681426ed9a3a] [d50bbcaf474a] [7f27679135bf] [cefa2905adfd]
- Browse emails: "Still thinking about it?"; biscotti visual with UGC; Smokco "Feeling on the fence?" 100% risk-free; Apparel Outpost "every tee feeds 5 rescue dogs"; "10% off just for you"; Lost Interiors with physical-store footer. [9d0646c87a39] [aaef1103dc77] [8c9c22844f69]
- Cart emails: Spice Pots "You left something tasty behind"; Smokco "Here's why customers choose Smokco" (British made, cheaper than cigarettes, 100% BPA free, highly rated service); "Take 10% off your cart? Yes please"; Melanie founder note. [bdbde349add0] [4085ce710e47]
- Post-purchase emails: Spice Pots "Flavor on the way"; nutrition "Complete your fitness nutrition" stacks; saber brand with "mystery saber"; Smokco getting-started guide; tea brewing guide; "Join the silly party" social push with a tagging prize; Saber Pro "Be part of the Galaxy"; Smoke Points loyalty. [5956a124a134]
- Deliverability recovery: a client's open rates went from 20% to 25% (23, 23, 22, 20, 21) to 50% to 60% (50, 56, 60, 51, 50, 51) after list cleaning, reputation work and content and design changes. No timeline given. [75378f892825] [df98522f016b]
- ChatGPT campaign analysis (one client, January to May 2025): average unique open rate 69% vs a low unique click rate ("clicks are the bottleneck"; the click figure is garbled as "26%"); advice to redesign around one above-the-fold CTA, contrasting buttons, shorter copy, test hero images vs GIFs, aim for 2%+ click-through ("1.3%+ unique clicks" given inflated opens); Saturday opens 71% vs Friday 67%, so move one send to the weekend; sends cluster at 8 to 9 a.m., so test 5 to 6 p.m.; emoji subject lines had higher opens and revenue for this client; a February bounce spike to clean. [7dccf4216521]
- ChatGPT flow analysis (one client, 1 March to 13 May): welcome series 56% of flow revenue (about 666k, per-recipient figure garbled); welcome email 1 = 88% of welcome revenue, suggestion to cut to 5 emails or reposition emails 2 to 5 ("330K low impact messages"); browse flow 42% open, 2.3% click, low order rate; SMS browse flow 1.70 euro per recipient; checkout SMS a "hidden gem"; post-purchase "leaves money on the table"; rest-of-world post-purchase lags the USA; win-back flows "barely convert". [87afe3ecbaf6] [a0d2e94690df] [af644216425f]

## 8. Mistakes the source warns about

Signup forms [39aa68c94680] [4c956b5e96a1]:
1. A weak offer. Nothing else fixes it.
2. Asking for email, phone, name or birthday in one step. People who will not give a phone number leave without giving the email. Ask for extra fields in later steps.
3. A time delay that is too short (feels like spam) or too long (few people see the form).
4. A form that is too small.
5. Too much copy or a supporting text box about "exclusive offers".
6. The offer hidden in body copy under a greeting like "Hey, how you doing?".
7. "Sign up" or "subscribe" in the headline or CTA.
8. One form for both desktop and mobile.
9. Slow-loading form images; images on mobile.
10. Showing the incentive on the success page (presenter's position).
11. Showing the popup "immediately" on page load; showing it on cart and checkout pages. [c5e1f30dd58d] [a877dc6c99dd]
12. Letting Klaviyo pick a form winner automatically on low volume. [00de729163a8]
13. Headlines like "Welcome to Nike" or "Sign up to be updated on our latest launches". [0590112c25d0]
14. Double opt-in (presenter: "massively" cuts new subscribers). [33c8d10a4bf5]

Flows:
15. Long, slow welcome drips (10, 14, 21 days) that waste the first 72 hours. [f2c3f6895ad4]
16. Burying the code in welcome email 1 or making people work for it. [681426ed9a3a]
17. Long, paragraph-heavy founder or brand emails. [d50bbcaf474a]
18. Generic codes like WELCOME10 with fake deadlines. [cefa2905adfd]
19. Generic "great product" reviews instead of objection-specific ones. [38077a826b12]
20. Treating browse abandonment as a weak cart flow; discounting in browse email 1. [d0e8f91819ba]
21. Heavy banners and urgency graphics in the last browse email. [8c9c22844f69]
22. A 20% discount in cart email 1 ("destroys margins"). [bdbde349add0]
23. Giving returning customers the same cart discount as non-buyers. [4085ce710e47]
24. Klaviyo's default delays (cart 4 hours, welcome 3 days, post-purchase 1 day). [d94eb68e5e18] [4d6f11a9f443] [58bdfe185e63]
25. Smart sending left on in flows. [4d6f11a9f443] [58bdfe185e63]
26. The generic or API add-to-cart trigger on a Shopify store. [5ad3da1bdb3a] [d94eb68e5e18]
27. Treating the first purchase as the finish line. [b3058403e9f8]
28. Generic how-to emails that do not match what the customer bought. [5956a124a134]

Campaigns:
29. Sending only 1 to 2 campaigns a week "to avoid annoying people", or daily sends that slowly burn the list. [7a1145af87dc]
30. Promo-heavy calendars that train people to wait; more than 1 sale a month. [9bbb999b4ec9] [071d76074c86]
31. Blasting the full list; sending to lists instead of segments. [bb790bf6e145] [951b0132a90b]
32. A "national day" email every week. [6a19f9f385b5]
33. Batching one campaign type into one week. [7a4e669c2511]
34. Writing campaigns the day before (defaults to promos, errors slip through). [3e4696a51c71]
35. Walls of text. [7a1145af87dc]
36. Treating SMS like email and sending it weekly. [b9130f4f4dca]

Testing:
37. Random tests with no hypothesis, especially easy subject-line tests. [59ae581e3e7f] [db47183f351f]
38. Calling winners at 50 to 100 recipients. [59ae581e3e7f]
39. Automatic winner selection on campaigns (20/20/60 after 4 hours). [ac370b420628]
40. Optimising open or click rate instead of revenue; judging send time by opens. [59ae581e3e7f] [4290660b631a]
41. Testing late emails in low-volume flows before email 1 of the main flows. [700ad4cccb44]
42. Starting with CTA button tests (lowest impact). [db47183f351f]
43. Assuming a winner in one flow or campaign carries over to another. [2176f28aa94d] [4290660b631a]

Segmentation and deliverability:
44. Mixing up AND and OR in segments. [516248e6ac94]
45. Being proud of a huge list that is 10% engaged; paying Klaviyo for dead profiles. [6dcb0bfce104]
46. Emailing people who marked you as spam or who bounced. [951b0132a90b]
47. Marketing-sounding subject lines that land in Promotions. [660cfc96df62]
48. Image-only emails that Gmail's AI cannot read. [31b2f58bfc95]
49. Treating technical setup as the cure; DMARC missing. [e758ab334635]

## 9. Caveats, conflicts and what is missing

Transcript damage and internal inconsistencies:
- Click-rate target: spoken as "5% or higher" and then "you do not need 1% or higher ... 0.5 is all good". The logic points to 0.5%. Cards [91d6fd433f58] and [660cfc96df62] repeat "5%". Treat 0.5% as the likely target and confirm with brand history. `[needs brand data: historical click rates on engaged segments]`
- Spam complaint target spoken as "001%": read as 0.01%. `[web check: Google and Yahoo bulk sender spam-rate limits]`
- Cart and checkout first delay: "15 minutes to 1 hour" in the flow build; "50 minutes to 1 hour" in the testing section (card [0528a2003316] copies "50 minutes"); "50 minutes can also be good" for checkout. Likely "15" misheard. Use 15 to 60 minutes as the test range.
- Site abandonment delay: 2 to 4 hours in one place, 1 to 4 hours in another. Card [c83fa5e0d0d6] wrongly says browse is "2 to 4 hours at the loosest"; the source gives 2 to 4 hours for site abandonment and 30 minutes to 2 hours for browse.
- Mystery discount: "under 20% off" and "50% off or less" in the same passage.
- SMS signup offer: "email 10%, SMS 20%" in one section; "10% email, then 50% for SMS" (possibly "15%") in another. Card [8bb0c8c613c5] keeps 50%.
- Returning-customer discount: "50% to non-buyers, 5% or 10% to returning" in one place and "10% vs 5%" in another. Card [4085ce710e47] keeps the 50% example.
- Smokco claim: transcript "8% cheaper than cigarettes", card [bdbde349add0] "8X cheaper". Unclear.
- List-clean segment 1 mixes 90, 180 and 365 day windows; the exact spoken condition set is garbled.
- Browse ladder card [8c9c22844f69] puts risk reversals and the Apparel Outpost example in email 1 and "three deeper reasons" in email 2; in the transcript, email 1 is the light reminder and both examples are email 2 (see 3.6).
- Card [4e9a379a0375] adds calendar fields (subject line, content, links) that the source did not list; the source lists 5 fields.
- Mobile exit intent: turned off for Klaviyo mobile forms (unreliable), but used in Aaliyah where mobile exit intent means a fast scroll up. Different tools, no stated rule.
- The welcome flow is called both "six emails" and "seven emails" (1A and 1B plus 2 to 6 = 7 sends).
- Aaliyah first-step preference: Klaviyo section says micro-yes "by default"; Aaliyah section says mini quiz or scratch-off "will probably perform better".

Conflicts with common ecommerce advice and platform rules:
- **Hiding the close X** (1 px, transparent) conflicts with accessibility and user-choice norms and may look like a dark pattern; on mobile it may also clash with search-engine guidance on intrusive interstitials. `[web check: Google intrusive interstitial guidance; accessibility rules]`
- **Removing the consent disclaimer** is framed as fine for US brands only; SMS capture in the US has its own consent rules and the EU needs consent. The source does not cover this. `[web check: TCPA/CTIA SMS consent wording; GDPR consent for email]`
- **Withholding the code** from the success page goes against the common practice of instant code reveal; the source admits it is a 50/50 debate and gives no numbers.
- **Spin to win with decoy slices** may raise consumer-protection questions (card caveat). `[web check: local promotion rules]`
- **Open rate as the main KPI and repair gate** (45% to 50%+) ignores Apple Mail Privacy Protection, which inflates opens; only the ChatGPT output mentions "inflated" opens. Clicks, placed order rate and placement tests are safer gates. `[web check: current share of MPP opens]`
- **Spam complaints and unsubscribes "less important"** conflicts with the 2024 Google and Yahoo bulk sender rules that set spam-rate limits and require one-click unsubscribe. The source does not mention those rules. `[web check: current Google/Yahoo sender requirements]`
- **3 to 4 campaigns a week** is higher than many brands send; the source ties it to engaged segments only. Brands with small lists or long buying cycles may need less (card caveat). `[needs brand data: list size, engagement, purchase cycle]`
- **Sending 1 to 2 emails a month to the whole list** (including unengaged) sits in tension with the same source's advice to suppress unengaged profiles.
- **Keeping past buyers on the list forever** is a judgment call; many sunset policies remove them too.
- **Smart sending off for all flows** means a person can get flow emails on top of 3 to 4 campaigns a week; the source does not discuss total email pressure.
- **Post-purchase statistics** (9x, 67%, 95%) are uncited and the 95% one is oddly phrased. `[web check: find original studies before using them]`
- **Aaliyah claims** come from a presenter with an affiliate link.

What is missing or thin:
- No SMS flow builds, no win-back flow, no sunset flow content, no site abandonment flow build, no back-in-stock, replenishment, birthday or review-request flows.
- No SPF or DKIM steps; the DMARC value was only shown on screen.
- No post-purchase timings after email 2; no returning-customer post-purchase copy beyond email 1.
- No numbers for most claims ("surprising amount", "crazy conversion", "massive difference").
- No statistical method; sample rules are rules of thumb.
- No guidance for brands outside the US on consent beyond "be careful in Europe".
- No discussion of discount codes' margin math beyond "factor in your margins". `[needs brand data: gross margin, AOV, discount redemption]`
- Klaviyo subject line and preview text ideas were in a downloadable guide, not in the video.

## 10. Card index

- [93e33dec853f] Email System Build Order: List Growth > Flows > Campaigns > Tests > Deliverability > AI
- [aa555d450d5a] Signup Form Offer Design and Margin Math
- [9622afcc8844] Standard Popup Structure: One Headline, One Field, One CTA, One Microcopy
- [e912865caec2] Micro-Commitment (Micro-Yes) Step Before the Email Field
- [c5e1f30dd58d] Timing, Frequency and Device Targeting Rules for Popups
- [53f37df1584e] Teaser / Floating Button Configuration
- [1f8be190a019] Post-Opt-In Success Page: Withhold the Code, Train Email Opens
- [c2e8c7484a70] Separate Desktop and Mobile Signup Forms
- [a877dc6c99dd] Redirect Your Signup Offer Away From Cart and Checkout Traffic
- [8b8c3454e9e7] Compress Signup Form Images to Protect Load Time
- [39aa68c94680] Ten Common Signup Form Mistakes to Audit Against
- [4c956b5e96a1] Signup Form A/B Test Priority Order
- [00de729163a8] Configure a Signup A/B Test: Manual 50/50 and Winner Selection
- [b9635f9e2351] Full-Screen Opt-In Forms and Zero-Party Data Quizzes
- [7da3ea843dc6] Gamified Opt-In First Steps: Spin-to-Win and Scratch-Off
- [4933eedd5bb2] Deliverability Hygiene: Authentication, Engagement Tiers and List Cleaning
- [580319f842a5] Core Automated Flows to Build and the 72-Hour Purchase Window
- [8db768330eb7] Email Campaign Cadence and Audience Strategy
- [64a2c2916004] Use AI and Personalisation Tools Only After the Fundamentals Are In Place
- [d80edbbaaf50] Choose a popup first step: scratch-off, quiz, or micro-commitment
- [8e47ceff852b] Decide whether the popup success page reveals the discount code or sends to email
- [33c8d10a4bf5] Configure single vs double opt-in for popup signup forms
- [143e7458c1be] Set popup trigger timing, scroll depth, and exit intent
- [ba6a52eba2e9] Build signup-form targeting rules for new vs returning visitors
- [6f18ca80ca5c] Preview and QA signup popups across devices before publishing
- [020eec5d0a13] Offer copy for signups: explicit discount vs mystery discount
- [9ed0b65913bb] Diagnose a monetization problem before blaming email or buying more traffic
- [f2c3f6895ad4] Front-load the welcome flow around the first 72 hours
- [4d6f11a9f443] Set welcome flow trigger filters and disable smart sending
- [681426ed9a3a] Write welcome email 1A: deliver the code above the fold
- [63691cee89e1] Send a same-day plain-text founder reminder as welcome email 1B
- [d50bbcaf474a] Use welcome email 2 to build brand trust with substance, not fluff
- [7f27679135bf] Use welcome email 3 to guide overwhelmed subscribers to a first purchase
- [cefa2905adfd] Welcome email 4: handle objections and differentiate at the product or category level
- [38077a826b12] Welcome email 5: escalate urgency with reviews that mirror buyer objections
- [18ddf0ee7ebf] Welcome email 6: close with a final reason to act, and test the format
- [71218ab504b8] Add proven evergreen campaigns to the welcome flow for extra revenue
- [d0e8f91819ba] Position browse abandonment as mid-funnel persuasion, not lost-sale recovery
- [5ad3da1bdb3a] Set browse abandonment trigger filters and a 30-day cooldown
- [c83fa5e0d0d6] Time the browse abandonment delays and use dynamic product blocks
- [9d0646c87a39] Write browse abandonment email 1 as a light, timely reminder
- [aaef1103dc77] Write browse abandonment email 2 to remove friction, not add pressure
- [890a5c97d555] Browse abandonment email 3: diagnose hesitation type before escalating with a discount
- [8c9c22844f69] Browse abandonment flow: 3-4 email escalation ladder
- [d94eb68e5e18] Abandoned cart vs abandoned checkout: build side by side
- [bdbde349add0] Abandoned cart/checkout email content: 3-stage objection sequence
- [4085ce710e47] Discount vs no-discount fork: non-buyers vs returning customers
- [58bdfe185e63] Post-purchase flow filters and timing
- [5956a124a134] Post-purchase email content: 6-email sequence
- [b3058403e9f8] Post-purchase as the retention engine
- [7a1145af87dc] Email campaign frequency: aim for 3-4 per week
- [9bbb999b4ec9] Campaign mix: don't let promos dominate the calendar
- [e756efb90a3f] Non-discounted campaign idea bank (social proof + education)
- [50432b3f5d6e] Non-discounted campaign idea bank (product, brand, occasion, engagement)
- [4e9a379a0375] Campaign calendar tool setup and the minimum fields to track
- [7f77b49944bc] Run a campaign calendar in a tool your team will actually open
- [bb790bf6e145] Send campaigns only to engaged subscribers
- [6a19f9f385b5] Anchor the calendar with fixed dates before filling content
- [071d76074c86] Keep sales events to one per month or fewer
- [5886ee2c2f40] Reuse existing blog, video and social content for campaigns
- [e932614a8a69] Plan a month of campaigns with an AI context block
- [dc7147515105] Pressure-test the finished calendar with AI before finalizing
- [e5552f0a655e] Check monthly mix across the seven campaign categories
- [7a4e669c2511] Alternate campaign types within each week, not just across the month
- [3e4696a51c71] Build a two-week execution buffer before sends go out
- [bd8384e14e34] Run a 20-30 minute monthly performance review
- [f5ac8bd65765] Put the product in every email, leading with value
- [b9130f4f4dca] Restrict SMS campaigns to launches, restocks and sales
- [59ae581e3e7f] Build a systematic AB testing mindset before running tests
- [0590112c25d0] Rank signup form tests by impact and work top-down
- [ef89709e3516] Choose signup form images by device, not aesthetics
- [8bb0c8c613c5] Test SMS signup angles against the email offer
- [700ad4cccb44] Test the first email of every flow first
- [0528a2003316] Test flow time delays with flow-type reference ranges
- [2176f28aa94d] Test product blocks, dynamic feeds and hero images in flows
- [00ade878eca2] Test plain-text vs designed emails and copy variables in flows
- [f0a945f5dff0] Test landing page destinations from flow emails
- [ac370b420628] Use manual 50/50 splits instead of automatic winner selection
- [4290660b631a] Run systematic campaign-side tests, starting with send time
- [db47183f351f] Deprioritize subject line, sender name and CTA button tests
- [e8e1adc8fefe] Set the upper bound on test duration and sample per variant
- [516248e6ac94] Build segments that start with marketing eligibility
- [6e06d938ff3f] Build an engaged-90-day segment as your campaign workhorse
- [951b0132a90b] Mandatory exclusion segments for every campaign
- [336b88ac711f] Build unengaged segments that exclude past customers
- [3ffe21f635f9] Specialty segments for buyer-stage targeting
- [75378f892825] Diagnose deliverability with placement testing and Klaviyo metrics
- [e758ab334635] Four-step technical setup for email sending
- [6dcb0bfce104] Five-step list-cleaning protocol
- [df98522f016b] Ramp deliverability back with a staged engagement ladder
- [31b2f58bfc95] Make emails readable to Gmail's AI filter
- [660cfc96df62] Structure emails for clicks and replies, not just opens
- [7dccf4216521] Use AI to analyze exported campaign analytics
- [87afe3ecbaf6] Use AI to diagnose flow performance and prioritize tests
- [a0d2e94690df] Where welcome-flow revenue actually concentrates
- [af644216425f] Spot under-monetized flows and channel gaps
- [91d6fd433f58] 2026 deliverability KPI targets for ecommerce email
- [1d17eaa95e56] Sequence the email system as a connected chain, not isolated tactics
- [5a08594d02a9] Audit your email program against the six-layer dependency model
