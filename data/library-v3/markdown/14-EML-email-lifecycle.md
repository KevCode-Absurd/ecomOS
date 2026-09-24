## Set a defensible email revenue benchmark and KPI case
Use when: Deciding how much resource to put into email lifecycle, or building the internal case for hiring/agency/tooling spend.
- Frame the target at store level, not marketing level: the source states email should drive at least 30% of total ecommerce revenue (not 30% of marketing-attributed revenue). Treat this as the source's heuristic target, not a universal law — some catalogues and repeat-purchase categories will sit far above or below it.
- Argue the three strategic benefits the source gives: (1) it lowers blended customer acquisition cost because paid traffic lands on site and converts to subscribers you can convert later for free; (2) it raises LTV through engineered repeat purchases instead of hoping customers return; (3) it builds an owned audience that compounds and reduces dependence on Meta/Google/TikTok CPMs and algorithm changes.
- Map the counterfactual risk to your store: if the ad platform's CPMs double or your account is restricted tomorrow, how much of your revenue base can you still contact directly? That gap is your email opportunity size.
- Translate the target into a monthly revenue number and compare against your current email-attributed revenue using a defined attribution window so the gap is measured consistently (see attribution card).
Caveat: 30% is the presenter's stated benchmark from agency work, not a published industry statistic.
Caveat: Changes to attribution windows will change the measured percentage; be consistent or compare like-for-like.

Tags: email-lifecycle, measurement, attribution, retention, customer-lifetime-value, acquisition, strategy
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Complete the Klaviyo–Shopify integration and sync settings
Use when: Initial account setup, a re-platform migration, or auditing why checkout/pop-up subscribers and browse events are missing from Klaviyo.
- During signup select 'sell products online', choose Shopify as the primary platform, and enter your Shopify URL. If migrating from another platform (e.g. Mailchimp), declare your existing list size so Klaviyo can guide sending-limit warmup; if new, select that you have no contacts.
- Set your sender name (brand name, or 'Founder at Brand') and sender email address. This is what appears in the inbox, so it drives open behaviour as much as the subject line.
- Turn on the Shopify app embed for on-site tracking inside your Shopify theme; without it Klaviyo cannot see on-site events.
- Check 'sync your Shopify email subscribers to Klaviyo' and point them into your single main email list; mirror the same for SMS subscribers into one main SMS list.
- Leave 'sync profiles and custom properties from Klaviyo to Shopify' unchecked — the source sees no strong reason for most brands to push Klaviyo data back into Shopify.
- In Klaviyo data settings, enable anonymous visitor tracking. By default, views and add-to-carts before an email is captured are invisible, which suppresses browse-abandonment and cart-abandonment volume. Verify the current toggle location in your account, as the UI changes.
Caveat: Anonymous visitor tracking means pre-opt-in behaviour becomes attached to the profile once they identify — disclose this in your privacy policy where required.
Caveat: Menu names and toggles in Klaviyo change; confirm the current interface before instructing a team member.

Tags: email-lifecycle, klaviyo, shopify, integration, tracking, setup
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Configure smart sending and attribution windows
Use when: Initial account configuration, or when email revenue reporting looks implausibly high/low and you need defensible numbers.
- In Settings > Email > Sender preferences, keep Smart Sending ON with the default 16-hour window so a subscriber does not receive a campaign within 16 hours of another email. This is the source's recommended default; it is customisable per brand.
- Decide on 'ignore transactional messages': the source typically leaves this unchecked for most brands, meaning a just-purchased customer can still receive a marketing campaign.
- Set open/click attribution windows to reflect your consideration cycle. Klaviyo's default is 5-day open / 5-day click. The source advises shorter for impulse-purchase products and longer for long-consideration products (e.g. $10k furniture with a ~30-day decision), but says do not stray far outside the 5/5 default as a conservative anchor.
- In tracking/reporting exclusions, exclude transactional messages from attribution so order confirmations do not show up as revenue-driving email.
- Exclude bot clicks (email and SMS) and exclude Apple Mail Privacy Protection opens from attribution data — since iOS 15, Apple pre-opens mail, generating fake opens that would otherwise claim credit for purchases.
- Save, then re-check the reporting figures so you know whether your previous baseline was inflated.
Caveat: Attribution windows determine how much credit email claims; changing them changes the 30% revenue KPI and all subsequent comparisons.
Caveat: Apple privacy opens still appear in open-rate metrics generally unless filtered — for engagement segments, always filter with 'Apple privacy open is false'.

Tags: email-lifecycle, attribution, klaviyo, measurement, deliverability, reporting
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Set brand defaults, fonts and fallbacks for email design
Use when: Setting up Klaviyo for the first time, or when emails render in the wrong typeface or look unbranded on some devices.
- In the brand library, upload your logo — it appears in email headers and sometimes footers.
- Set brand colours for accent, body text, buttons and links so templates inherit a consistent palette.
- Set your primary font. Klaviyo does not support custom fonts natively for all inboxes; it supports websafe fonts, so pick the closest websafe match as the account default.
- Add custom fonts separately. Google fonts and Adobe fonts can be selected directly. Fully custom fonts require the 'hosted web font' route with Klaviyo's hosting instructions.
- Always define a fallback font — inbox providers such as Gmail may only render Google/web fonts, so an Adobe or bespoke typeface will silently substitute. Choose the closest visual match.
- Add social icons in the brand settings so footers populate automatically without manual entry in every template.
- Set brand voice if you use Klaviyo's AI copywriting, so generated copy matches tone.
Caveat: Header links are rarely useful for most brands given the design approach shown in the course; they can be skipped.
Caveat: Font rendering varies by inbox client; the fallback is what most recipients will actually see.

Tags: email-lifecycle, klaviyo, email-design, brand-consistency, templates
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Authenticate your domain: dedicated sending domain, SPF, DKIM, DMARC
Use when: New Klaviyo account, domain migration, or diagnosing poor inbox placement despite good content.
- In Settings > Domains > Add domain, enter your root domain (e.g. brand.com) and then create a sending subdomain such as send.brand.com. This isolates marketing sending reputation from your root domain.
- Choose the setup path: Klaviyo may offer an assisted integration partner (the source notes an 'Entry' integration option and that it may cost money); otherwise set up manually.
- Select your domain provider, copy the generated DNS records (name and value) into your host's DNS settings (e.g. GoDaddy), then click verify. Verification can take up to 48 hours — only verify after records are actually published.
- Add the SPF, DKIM and DMARC records the same way. SPF, DKIM and DMARC tell inbox providers you are who you claim to be and protect your brand from spoofers.
- Critical: when creating the DMARC record, ensure the policy reads p=none, not reject or quarantine. With reject/quarantine, any email the provider thinks is spam goes straight to spam; with none, it continues to be delivered to inboxes. The source calls this a huge difference in delivered mail.
- Confirm SPF/DKIM/DMARC are all passing before scaling volume.
Caveat: The source presents p=none as the safer setting for deliverability; security teams may prefer stricter policies, which can suppress delivery.
Caveat: DNS record formats and provider UIs differ; verify current instructions before editing live DNS.
Caveat: DNS propagation delays mean urgent sends may go out unauthenticated if you leave setup to the last minute.

Tags: email-lifecycle, deliverability, dns, email-authentication, spf, dkim, dmarc, klaviyo
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Maintain sender reputation with bounce, spam and engagement thresholds
Use when: Ongoing deliverability monitoring, or when opens collapse and you need to diagnose reputation damage.
- Understand the model: reputation is history-based and hard to rebuild once damaged; a good reputation gets primary inbox placement, a bad one gets spam or promotions tab.
- Keep bounce rate under 1%. Bounces come from invalid addresses — e.g. a fake email submitted through a pop-up form still triggering the welcome or abandoned-cart flow. Suppress hard-bouncing addresses and consider preventing obviously fake form entries.
- Keep spam complaint rate below 0.3%, and ideally below 0.1%, to stay inside Gmail and Yahoo's stricter 2024+ requirements. Locate these rates in your account reporting and review on a regular cadence.
- Maximise positive engagement signals: opens, clicks and especially replies tell inbox providers people want to hear from you. Low opens and low clicks act as negative signals.
- Send at a consistent cadence — the source cites an example of two campaigns a week plus flows sending daily — because erratic sending (long silence then a burst) is treated as a negative signal.
- Fix the root cause before re-sending: low opens usually means wrong audience (see 180-day cleaning and engagement segments), not a subject-line problem.
Caveat: Thresholds (0.3% complaint, 0.1% ideal, 1% bounce) are the source's targets and align with stated Gmail/Yahoo expectations; Google's published requirements should be checked for current limits.
Caveat: Reputation damage is slow to reverse, so prevention, not remediation, is the practical strategy.

Tags: email-lifecycle, deliverability, sender-reputation, spam-complaints, bounce-rate, engagement, gmail, yahoo
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Clean unengaged subscribers and use engagement-tiered segments
Use when: Replenishment/list hygiene work, or when deliverability declines from sending to a stale list.
- Define the benchmark: suppress profiles inactive past 180 days. Someone who signed up two years ago and has not opened, clicked or visited since is near-certainly uninterested, and every send to them dilutes your reputation.
- Build engagement filters using Klaviyo's activity windows rather than one blunt list. The source's framework uses 14-day, 30-day, 60-day and 90-day active windows to grade engagement tiers, letting you send the most aggressive cadence to the freshest tiers and reduce or suppress the tail.
- Within the engaged segment, always filter out fake signals: require 'opened email where Apple privacy open is false' OR 'clicked email where bot click is false'.
- Add recency carve-outs before suppressing: someone who subscribed in the last 14 days, or was active on site in the last 14 days, should stay in the engaged segment even with no opens — they may only have received one or two emails, or may be re-showing intent.
- Put a time limit on the carve-out: if a site-active subscriber does not engage within roughly two weeks, they should drop back out rather than staying engaged status for six months on one visit.
- Re-run the suppression periodically rather than once, so the tail is pruned continuously.
Caveat: Suppression reduces list size and short-term sends; the source frames this as necessary for future inbox placement rather than a loss.
Caveat: Engagement tiers only work if open/click tracking is filtered for Apple and bot events, otherwise inactive people will look engaged.

Tags: email-lifecycle, list-hygiene, segmentation, deliverability, engagement, suppression, klaviyo
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Configure preference pages and choose email opt-in deliberately
Use when: Account setup, when signup-to-list conversion is poor, or when unsubscribes look unbranded and abrupt.
- In Settings > Other, locate the four pages: preference page, subscribe page, email confirmation, and unsubscribe page.
- Brand the preference page and offer meaningful topic or frequency choices without obstructing unsubscribe.
- Edit the unsubscribe page to add brand-appropriate copy (e.g. a thank-you for being part of the brand) rather than a bare default page.
- Evaluate single versus double opt-in for email using signup completion, list quality and applicable requirements. The source preference for single opt-in is not a universal instruction and does not automatically apply to SMS.
- Check the footer of your email templates includes working preference and unsubscribe links.
- If a person reports still receiving emails after unsubscribing, use the profile's three-dot menu > Suppress to remove them from all sends — a genuinely unsubscribed person receiving mail is a spam-complaint risk.
Caveat: Single opt-in is the source's recommendation on volume grounds; double opt-in is stronger for consent quality and some regions' compliance expectations. GDPR-style consent rules may override the list-growth argument.
Caveat: Suppression and unsubscribe are different states; both must be respected.

Tags: email-lifecycle, opt-in, consent, compliance, klaviyo, list-growth, preference-center
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Map the customer journey before building flows and campaigns
Use when: Planning lifecycle architecture, or when you suspect campaigns and flows are contradicting each other.
- Trace the source's journey structure: first visit from Meta/organic/TikTok → pop-up form offer → first emails from automated flows (welcome/nurture, or abandoned cart if applicable) → recurring campaigns at least weekly → first order → post-purchase messaging designed to drive the next order.
- At the pop-up checkpoint, check the ad or content creative the visitor arrived from, then write the pop-up offer to speak only to what that traffic already knows. Mismatched offers are the most common journey break.
- Audit for cross-channel contradiction: the source's example failure is a first-time-customer discount sent to someone who has already placed five orders, which annoys and is unusable. Gate first-purchase offers to non-purchasers.
- Assign each touchpoint a single job and audience stage so content, offer and copy align with where the person is.
- Review flows and campaigns together on a schedule — this is the fix for the common pattern of channels being built 'in a silo'.
Caveat: The journey is described as a typical sequence; not every store has a pop-up-first entry or a long nurture phase.
Caveat: Journey logic is qualitative — treat it as an alignment discipline rather than a measurable model.

Tags: email-lifecycle, customer-journey, lifecycle-mapping, flow-architecture, personalization, positioning
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Use Klaviyo metrics as flow triggers and personalisation filters
Use when: Building or debugging flows, especially abandoned checkout/cart, and building personalised dynamic content.
- Understand the three metric sources: Klaviyo-native (received email, opened, clicked, unsubscribed, marked spam, dropped), Shopify (ordered product, placed order, fulfilled, refunded, checkout started, order cancelled), and API/integration events from other apps.
- Use metrics as flow triggers. The source's example: the 'Checkout Started' metric triggers the abandoned-checkout flow, with the first email sent about 2 hours later.
- Use metrics as filters and conditions for who should receive an email and who should not — e.g. don't send a first-purchase offer to someone with a 'Placed Order' metric in their history.
- Use metric properties for personalisation — an order metric carries what was purchased and for how much, enabling conditional and dynamic content.
- Confirm each required event is actually firing end-to-end (place a test order, start a test checkout) before relying on it as a trigger, since missing metrics mean silent flow failures.
Caveat: Because events drive triggers, a broken integration produces no errors — flows simply never fire. Test after every app or theme change.
Caveat: Event names differ between Shopify and any custom API implementations; map them deliberately.

Tags: email-lifecycle, klaviyo, automation, triggers, event-tracking, abandoned-checkout, personalization
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Read a Klaviyo profile to decide segmentation and personalisation
Use when: Designing segments, splits and conditional content, or investigating why one customer received the wrong message.
- Check subscription status first: email/SMS opt-in state, how and when they subscribed, and which form they used. This determines whether they are mailable at all.
- Review custom properties, which are brand-specific: source, prospect vs repeat purchaser flags, Shopify tags pulled through the integration, loyalty points balance. These are the fields you can filter on.
- Review standard data: language, location (from IP or checkout address), most recent acquisition source, last site visit, profile created/updated timestamps, first/last active.
- Read the event timeline on the right side to reconstruct the journey — active on site, submitted form, subscribed, each email open, product views, orders.
- Open Metrics & Insights and edit which metrics appear at a glance (orders placed, revenue, fulfilled). Add loyalty or other integration metrics if useful.
- Use predictive analytics fields: predicted CLV, predicted date of next order, and channel affinity (which channel the person prefers) to avoid double-sending email plus SMS to someone who prefers one channel.
- Use recently viewed products for dynamic content — show that person the products they actually looked at rather than a static recommendation block.
Caveat: Predictive analytics are model outputs and should inform, not dictate, targeting; the source frames them as attribution/hint data.
Caveat: Custom properties only exist if you or an integration creates them; a missing property cannot be used as a filter.

Tags: email-lifecycle, klaviyo, customer-research, segmentation, personalization, predictive-analytics, profiles
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Organise profiles into lists and segments, and never campaign to the whole list
Use when: Campaign sending setup, list growth tracking, or troubleshooting welcome flows sending the wrong message.
- Maintain one primary email list and one primary SMS list for organic opt-ins (pop-up forms and checkout). This concentrates welcome-flow triggering for your main traffic source.
- Use lists for opt-ins and as welcome/nurture flow triggers only — lists are static and never change membership once a person is added.
- Create separate lists for each non-organic import or campaign source (e.g. an Instagram giveaway). Reason 1: track how each source contributes to list growth. Reason 2: control welcome messaging — an Instagram giveaway subscriber should get a giveaway welcome, not the '10% off your first order' welcome.
- Build dynamic segments for sending campaigns. Segments update continuously based on behaviour, purchase status, engagement and other profile data.
- Apply the rule the source states emphatically: never send a campaign to your entire list, and it is rare to send to a list at all. Segments protect deliverability and personalisation.
- Confirm each list has a distinct associated welcome flow before importing, so the flow-to-source mapping is not accidental.
Caveat: Multiple lists mean multiple welcome flows to maintain; be deliberate about adding new ones.
Caveat: List membership is permanent for people once added, so list-based sending will accumulate stale contacts — another reason to send via segments.

Tags: email-lifecycle, klaviyo, list-management, segmentation, welcome-flow, list-growth, personalization
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Build the engaged prospect and engaged customer segments
Use when: Setting up your campaign sending audience, or improving deliverability and personalisation for campaigns.
- Apply the core principle: only send campaigns to people who have shown they want to hear from you. Continuing to send to a subscriber who has not opened or clicked in two years is a certain negative signal with no upside.
- Define engagement with OR conditions: opened email in the last 180 days (Apple privacy open = false) OR clicked email in the last 180 days (bot click = false) OR subscribed to a list in the last 14 days OR active on site at least once in the last 14 days.
- Add the mailability condition AND can/cannot receive email marketing, so unsubscribed and suppressed profiles are excluded even if they meet other criteria.
- Then split the segment into (a) prospects who have never purchased and (b) existing customers, and create both as reusable segments for every campaign send.
- Rationale for splitting: after each campaign you can see purchase results by segment, distinguishing first-order conversion from repeat purchases. A single blended engaged segment hides whether a campaign acquired or retained.
- Extend the split to brand-relevant axes where useful — the source's example is an apparel brand separating male-buyer and female-buyer history to see whether women's campaigns are being bought by men.
- Keep engagement criteria attached to every derived segment, including interest-based ones. A customer who has purchased ten times but never opens email still hurts deliverability if mailed.
Caveat: The 180-day and 14-day windows are the source's chosen thresholds, not proven optima; adjust to your purchase cycle.
Caveat: The prospect/customer split is a reporting and learning device first; targeting value is a secondary benefit.

Tags: email-lifecycle, segmentation, deliverability, engagement, campaigns, klaviyo, experiment-design
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Style campaign creative by segment learning
Use when: Writing campaign and welcome-series creative, or deciding what proof and offers to lead with for new vs returning buyers.
- Send campaigns to the split segments from the previous card so results are attributable to prospect or customer audiences.
- After the send, compare conversion between segments and note which content elements appear to drive the result. The source's illustrative example: if a prospect-heavy campaign featuring lots of reviews converts prospects well, add more reviews to prospect-facing campaigns and to the welcome series.
- Carry the learning forward by audience, not across the board: what works for first-time buyers does not automatically work for repeat buyers, because the two groups buy for fundamentally different reasons.
- Apply the same logic to discounts: prospect segments are where first-purchase offers belong; customer segments should receive non-discount value (new arrivals, replenishment, loyalty, education) instead.
- Iterate by changing one creative variable per send so the comparison remains interpretable.
Caveat: This is a directional learning loop, not a controlled creative test; the source presents it as observed practice rather than a measured effect size.
Caveat: Do not generalise a prospect creative win to customers without checking, and vice versa.

Tags: email-lifecycle, campaigns, creative-strategy, segmentation, experiment-design, welcome-flow, social-proof
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Employ retention and account-level setup: where email sits in the 2026 lifecycle
Use when: Roadmapping the lifecycle programme, deciding sending frequency, and prioritising which automations to build first.
- Set the base sending cadence at 3–4 campaigns per week, the source's recommended campaign frequency. Consistency matters as much as volume for reputation — erratic bursts are a negative signal.
- Prioritise the five core Klaviyo automated flows: Welcome, Browse Abandonment, Abandoned Cart, Abandoned Checkout and Post-Purchase. These are the standard set to build before advanced work.
- Give the welcome flow a fast clock: the first 72 hours after signup is the critical conversion window, with day zero driving the highest purchase volume. Put your best converting email first.
- After the core is in place, add advanced tactics the source lists: active gamification such as spin-to-win or scratch-off capture, zero-party data collection quizzes, and separate split-tested desktop and mobile experiences rather than one responsive template.
- Recognise that the inbox itself is now AI-curated (e.g. Gmail's AI inbox), so authentication, regular cleaning and engagement-tiered segmentation are the levers that put mail in the primary inbox rather than the promotions tab.
- Track cadence, flow coverage and inbox placement as programme health metrics, and be prepared to iterate rather than set and forget.
Caveat: 3–4 campaigns per week plus flow volume is aggressive for some audiences; the source also tells you to learn whether emails are wanted, so cadence should be validated against engagement and spam complaints.
Caveat: The 72-hour welcome window and day-zero concentration are the source's observations across an agency portfolio, not a guarantee for every offer type.

Tags: email-lifecycle, cadence, flow-architecture, welcome-flow, abandoned-cart, post-purchase, gamification, segmentation, klaviyo
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Engagement windows as sliding retargeting filters
Use when: Building or auditing your campaign send segments, and deciding whether dormant subscribers should still receive campaigns.
- Define engagement with four OR conditions, each time-bounded: opened email at least once in the last 180 days (with Apple privacy open = false), clicked email at least once in the last 180 days (with bot click = false), subscribed to list at least once in the last 14 days, or been active on site at least once in the last 14 days.
- Treat site activity as intent evidence the same way you would treat a site visitor from a paid ad you retarget for a week or two. Someone browsing your store again is showing intent, so let them back into the campaign audience.
- Cap the grace period. A returning visitor who then stops opening should stay in the engaged segment for roughly two weeks, not six months; if they do not engage again in that window, remove them.
- Combine the OR engagement block with AND conditions for mailability and purchase status, then save and check the profile count preview before sending.
- Re-verify the current Klaviyo filter names and privacy/bot filter labels, since interface naming changes.
Caveat: The 180/14-day windows are the source's chosen settings, not a universal benchmark; adjust for your send cadence and list size.
Caveat: Using OR for the mailability condition would include nearly everyone, so mailability and order history must be AND-ed to the engagement block.

Tags: email-lifecycle, segmentation, retention, klaviyo, deliverability, campaign-sending
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Build prospect and customer segments by cloning one definition
Use when: Setting up your initial Klaviyo segment structure before launching campaigns or flows.
- Build the prospect segment first: any engagement condition met AND can receive email marketing AND placed order zero times overall time.
- Clone it and change only the final condition to placed order at least once overall time to produce the one-time/existing customer version.
- Create three engagement windows per group: 90-day, 180-day and 365-day engaged, for both prospects and existing customers — six segments in total.
- Use the preview count in the segment builder to sanity-check each segment's size before creating it.
- Verify the current Klaviyo segment builder condition wording before rebuilding, since filter labels change between interface versions.
Caveat: Segment definitions only matter if the list feeding them is clean; prospects are defined as never-purchased, so order tracking must be wired to your store correctly.

Tags: email-lifecycle, segmentation, klaviyo, list-building, campaign-sending, measurement
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Match offer intensity to engagement window
Use when: Deciding which campaign content and offers go to your 90-day versus 365-day engaged segments.
- Send evergreen content — no huge offers, no huge new product announcements — to the 90-day engaged segment, because these people have shown recent interest and will keep engaging without a discount incentive.
- Send major sale moments such as Black Friday and large product launches to the 365-day engaged segment to attempt re-engagement with people who only want to hear from you a few times a year.
- Think of the customer type who shops a brand once a year specifically for the big deal — they do not want constant updates but do want the announcement, so the big offer is your reason to reach them.
- Keep evergreen, non-discount creative in the cadence for recent engagers so you are not training your best subscribers to wait for discounts.
Caveat: This is the source's agency practice at Dispatch, not a tested universal rule; the split between evergreen and promotional content should follow what your audience responds to.
Caveat: The 90/180/365 bands are source-specific heuristics, not calculated thresholds.

Tags: email-lifecycle, segmentation, campaign-sending, retention, promotion-strategy, offer-design
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Never send campaigns to the full list — and never to segments that are too small
Use when: Planning campaign send frequency and audience selection across your prospect and purchaser segments.
- Always include some engagement criteria in the campaign audience; never send a campaign to your entire list.
- Avoid splitting two weekly campaigns across two different small segments (for example one send to prospects only, one to one-time purchasers only), because it halves your recipients and each person gets half as many chances to buy.
- Recognize that you cannot know whether a given person will buy on Tuesday or Friday, so cutting their exposure removes shots on goal rather than improving relevance.
- Unless you have millions of subscribers and the resources to send high volumes to small segments, send broader evergreen content to all engaged subscribers and personalize within the email using dynamic content instead of segment exclusion.
- The source puts the cutoff at brands doing under roughly $20M a year, where broad engaged sending is the better trade.
Caveat: This is the presenter's strongly held opinion based on agency experience; it is a distribution argument, not a claim that personalization is worthless — pair it with dynamic content.

Tags: email-lifecycle, segmentation, campaign-sending, list-growth, promotion-strategy, dynamic-content
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Build filters so each flow only fires for the right lifecycle state
Use when: Setting up or debugging any automated flow where purchase or customer-type status should change who receives it.
- Add a profile filter to the welcome series requiring that the person has placed order zero times overall time.
- Rely on the fact that Klaviyo re-checks filters immediately before each email in the flow, so a subscriber who buys between email one and email two does not receive email two.
- Extend the same pattern to other flow logic: for example, filter out known B2B customers from a DTC welcome series when your brand serves both segments.
- Avoid using Klaviyo default flow templates for these flows; the source recommends building from scratch (build your own) so triggers, filters and timing match your actual customer journey.
- Verify current filter names and trigger options in your Klaviyo account before configuring.
Caveat: Profile filters only work as well as the data behind them; order and tag data must flow from your store into the profile.

Tags: email-lifecycle, automation, klaviyo, flows, segmentation, trigger-logic
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Micro-commitment first step in the pop-up form
Use when: Building or redesigning your sitewide pop-up form to convert more site traffic into subscribers.
- Step one, micro yes: present only the offer and two buttons, e.g. 'Claim 20% off' versus 'I'm not interested', with nothing asked in return. The micro commitment principle means someone who commits to wanting the offer is far more likely to give their email next.
- Step two, email opt-in: make the email field required with a 'field is required' message and set the button action to submit form, routing to your master email list.
- Step three, SMS opt-in: collect phone subscribers here even if you have not built out SMS marketing yet; you are otherwise leaving subscribers uncollected for no setup cost.
- Step four, success page: either show the code or send it to the inbox/phone. The source prefers sending it, because the first open and click boosts your sender reputation.
- Turn on the teaser so that if someone exits the form mid-way, a teaser stays on site and can reopen the form.
Caveat: The micro-commitment structure is based on the source's agency A/B testing across hundreds of forms, but the results are their client data, not a guarantee for your brand.
Caveat: Nine times out of ten the micro-commitment step tests better, per the source, but it is still worth an A/B test.

Tags: email-lifecycle, list-growth, popup-forms, conversion-optimization, klaviyo, offer-design, sms
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Form behavior settings that stop accidental opt-out loss
Use when: Configuring display and behavior settings on a pop-up form before going live.
- Uncheck 'click outside form to close' so the only exit is the X button. Otherwise a browsing visitor who clicks a product at the exact moment the pop-up appears closes the form never to reopen it.
- Set the form to load immediately rather than on a time delay, which the source reports performs better.
- Build without side images: with no image, attention goes straight to the offer, and the source says forms without images typically outperform those with images (still a good A/B test).
- Show the form to all website visitors who are not already subscribed, and keep frequency rules in mind if you do not want repeat visitors to see it daily.
- Check that the form renders correctly on both mobile and desktop rather than only on the device you are building on; most of your site traffic is mobile.
- Verify current setting labels in your form builder, since interface wording changes.
Caveat: Targeting all non-subscribers is the source's recommendation for maximum capture, but you may still exclude specific URLs such as the cart page where a discount could cut into margin on an imminent purchase.

Tags: email-lifecycle, list-growth, popup-forms, conversion-optimization, klaviyo, mobile
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Offer choice is the highest-leverage pop-up test
Use when: Planning your recurring pop-up form experiment roadmap.
- Test the offer first: percent off versus dollar off, 10% versus 15%, free shipping, cash back, or free gift with purchase, since offer makes the biggest difference to opt-in rate.
- If testing dollar off against percentage, take your AOV and pick a dollar amount that equals roughly 10% of that AOV, so the comparison is at least in the same value range.
- Test behavior second: micro-commitment step versus none, zero-party data questions in the form, load timing (immediate versus delay), which pages trigger it, and exit intent.
- Test copy third: short versus long copy, and whether to reveal the offer versus teasing a 'mystery offer'.
- Test design last: image versus no image, product versus lifestyle imagery, and text sizes, especially if your customer base skews older.
- Run a test every month; even a form already converting well is unlikely to be at its ceiling. Take the conversion-rate numbers the source cites for its own agency clients as an illustration of headroom, not as your target.
Caveat: The source's claim that Klaviyo's 'excellent' badge threshold is not actually excellent is the presenter's opinion, not a verified platform fact; treat it as a reason to keep testing.
Caveat: Offer data is audience-specific — your demographic may respond better to dollar off or free shipping than to percentage off.

Tags: email-lifecycle, list-growth, popup-forms, experiment-design, conversion-optimization, offer-design, klaviyo
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Targeting and location rules for offer differentiation
Use when: Setting up pop-up targeting rules for a sitewide form, a sale form, or a channel-specific offer test.
- Use URL rules to suppress the sitewide discount form where it hurts: for example exclude the cart page so an about-to-purchase visitor does not get handed extra margin away, and exclude a sale landing page if the sitewide discount cannot be stacked with the sale.
- Use location rules, driven by IP-based location, to show different offers by country — for example a different offer for Canadian versus US visitors.
- Use UTM parameters to target by traffic source: if traffic from one paid channel is much cheaper, you could test a richer offer for that source while showing the standard offer to everyone else.
- Use cart content value to trigger a form only above a threshold, such as over $1,000 in cart, so a strong offer lands on a high-value basket.
- Use targeting modes deliberately: show to all visitors for a sale link, show to email subscribers only when you want existing subscribers to opt into SMS if they skipped it.
- Do not restrict the sitewide form to the homepage only; the source explicitly discourages that.
- Verify the current targeting options and labels in your ESP, since these change.
Caveat: Cart-value thresholds such as $1,000 are examples of what the tool supports, not recommended thresholds for your store.
Caveat: Source-specific channel advice (for example TikTok versus Meta offers) depends on your own cost per acquisition and margin.

Tags: email-lifecycle, list-growth, popup-forms, segmentation, acquisition, klaviyo, offer-design
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Master list plus engaged segments as the base setup
Use when: Setting up or cleaning up your ESP account before building flows and campaigns.
- Create a single master email list fed by your pop-up form and checkout, so every acquisition source writes into the same list.
- Use the segment builder for audiences built from behaviour, properties and events — lists for who opted in, segments for what they have done.
- Know the condition types available: whether someone can receive email marketing (not unsubscribed or suppressed), what someone has or has not done across tracked metrics with either a date range or overall time, location proximity, and profile properties including store tags.
- Use property and tag conditions to target, for example, people carrying a specific Shopify tag or people who viewed specific items, so campaigns and flows can be personalized on that data.
- Connect SMS subscribers to a separate list, as recommended, rather than mixing phone and email subscribers on one list.
- Verify current Klaviyo list/segment tabs and builder condition names before implementing.
Caveat: A list implies opt-in consent; using segments to send to people who never opted in creates deliverability and compliance risk.
Caveat: The segment builder's exact property and metric names depend on your integrations and may differ from the example.

Tags: email-lifecycle, segmentation, klaviyo, list-building, deliverability, integration
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Campaigns versus flows, and stopping message overlap
Use when: Deciding whether a recurring send should become an automation, and diagnosing high unsubscribe or spam complaint rates.
- Route repetitive sends into flows: if you find yourself sending the same campaign weekly, monthly, or daily, it is probably a behaviour-triggered automation instead.
- Keep campaigns for genuinely one-off, time-sensitive moments such as a new sale, a product launch, seasonal content, or a new blog post.
- Use flows to extract lifetime value from the customer journey and campaigns to capitalize on moments that will not repeat.
- Before sending a campaign, check whether the same person is also due a welcome, abandoned cart, or post-purchase email in the same period; overlapping sends in a 24-hour window are a common cause of unsubscribes and spam complaints.
- Audit the campaign and flow calendars together as one customer journey rather than as separate programs.
Caveat: The source's observation about high unsubscribe and spam rates among audited brands is anecdotal from their agency work, not a measured benchmark.

Tags: email-lifecycle, automation, campaign-sending, flows, deliverability, retention
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Welcome series: trigger, filter and immediate code delivery
Use when: Building your first automated welcome flow after someone subscribes via pop-up or checkout.
- Set the trigger to 'added to list' on the same master list your pop-up form writes to, so every new subscriber enters the flow.
- Add a profile filter requiring zero orders overall time, so checkout subscribers and past purchasers are excluded.
- Remove any initial time delay for the first email: send the redemption code as soon as someone signs up so the promise made in the pop-up is fulfilled while intent is highest.
- Set email one's sender on your authenticated brand domain, and set reply-to to your customer support address so replies land in the service inbox.
- Structure the series so that by the end, the subscriber fully understands why your brand is the one to buy from in your category, not just that a discount exists.
- Use standardised flow and email naming (for example 'welcome series email number 1') so reporting views can trace performance back to its source.
- Verify current trigger, filter and naming fields in your ESP before building.
Caveat: Filter requirements differ by brand; the source adds B2B exclusions for brands serving both B2B and DTC, which may not apply to you.

Tags: email-lifecycle, automation, flows, klaviyo, welcome-series, trigger-logic, list-growth
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Design emails outside the ESP with image slices
Use when: Producing welcome, cart, post-purchase and campaign creative that must match your brand across devices and inboxes.
- Design in an external tool and export image slices, so the layout renders pixel for pixel the same on desktop and mobile; inside a template editor, headline wrapping and spacing differ across devices and inboxes, making QA harder.
- Understand the font problem: custom fonts need a web-safe fallback, and whether the brand font actually displays depends on the recipient's device and inbox provider, so what you see in the preview is not what every recipient sees.
- Keep the brand consistent from ad to site to pop-up to first email, because these touchpoints are where initial trust is built; a font that does not match the rest of the funnel breaks that consistency.
- Place the product block inside your externally designed email if you want products in it, since the product block is the one thing that must be set up in the ESP.
- Add a proper footer with social links and your organisation details and unsubscribe language; the ESP inserts a required unsubscribe link regardless, but a default one is ugly.
- Verify current editor capabilities and footer compliance requirements in your ESP.
Caveat: Fully image-sliced emails trade rendering control for reduced live-text accessibility and searchability; the source advocates the approach for branding fidelity, not as a universal standard.
Caveat: If you lack design resources, the source says choosing a template is acceptable, while noting template images often cannot be edited in the ESP.

Tags: email-lifecycle, email-design, branding, klaviyo, creative-strategy, product-page, rendering
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Dynamic product feeds for emails
Use when: Adding product recommendations to welcome, browse, cart or campaign emails, especially when inventory and bestsellers change often.
- Place a product block in the email; choose static products when you want fixed SKUs, or dynamic products when the selection should be recalculated each send.
- For dynamic feeds, set criteria such as bestselling products over a chosen window — the source shows options like the last 3 days or last 90 days — so the email reflects current demand.
- Add filters to avoid unhelpful recommendations: exclude a category, set a minimum price, or exclude products with very low stock.
- Choose deliberately between dynamic and static: a brand with constantly turning inventory and new styles may want current bestsellers, while a brand with ten always-in-stock SKUs may prefer to always show its two or three consistent bestsellers.
- Save the feed and attach it to the email; the ESP recalculates the products at send time as the underlying data changes.
- Verify current product-feed criteria and filter options in your ESP, since these change.
Caveat: Dynamic feeds depend on accurate product, price and stock data flowing from your store; stale data will produce stale or out-of-stock recommendations.
Caveat: The source's window examples (3 days, 90 days) are illustrations of available settings, not recommended values.

Tags: email-lifecycle, email-design, klaviyo, automation, merchandising, product-recommendations
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Design Welcome Emails Outside Klaviyo, Export as Image Slices
Use when: Designing your first welcome email for a new subscriber, where you need a branded look that Klaviyo's template/HTML editor can't produce (e.g., custom graphic placement).
- Design the full welcome series in Figma (or similar design tool) with the logo, offer code, hero graphic, and body content laid out exactly as you want it.
- Slice each visual block in the design into separate images and export each as PNG or JPEG.
- In Klaviyo, drag in an image block, upload the exported slice, and compress it.
- Repeat for each section, stacking image blocks until the email matches the Figma design.
- Add subject line and preview text after the design is assembled.
- Set one-day time delays between each welcome email, then set the emails live one by one.
Caveat: This workflow assumes design work happens outside Klaviyo; Klaviyo's templates and HTML editor are described as too rigid for advanced layouts.
Caveat: Image-heavy emails trade design control for text deliverability — the source does not address that tradeoff.

Tags: email-lifecycle, welcome-flow, email-design, figma, klaviyo, branding
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Welcome Series Content Blueprint for DTC Brands
Use when: Planning the content and sequence of your welcome flow after a subscriber joins via a pop-up offer.
- Email 1: deliver the pop-up offer code with the goal of getting the subscriber back to the site as fast as possible; include the logo plus one or two of: a short founder letter, brand values, USPs, or best-selling products/collections.
- Add a one-day delay, then email 2: explain your unique selling points — why they should buy from you rather than competitors.
- Email 3: guide subscribers to the best product for them by highlighting your top 3–5 best sellers or best-selling collections.
- One-day delay, email 4: feature the brand story, framing why the subscriber should care (e.g., the market problem the brand was created to solve).
- One-day delay, email 5: a direct us-vs-them comparison arguing why to buy from you over specific competitors.
- Then spotlight customer reviews/testimonials, then answer FAQs (many prospects never visit your FAQ page).
- Add brand-specific angle emails (e.g., heritage, trust) based on what your customers care about.
- In every email, keep a banner or line reminding them their offer is still valid.
Caveat: Presented as a baseline the source says fits ~99% of DTC brands based on their A/B tests, not a universal requirement.
Caveat: Not every brand has a brand story that drives conversion; the source acknowledges this.
Caveat: Withhold nothing that could help a subscriber convert — the goal is to give new subscribers everything they need to make a first purchase.

Tags: email-lifecycle, welcome-flow, customer-research, offer-design, retention, conversion-optimization
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Trigger Abandoned Checkout on checkout started With Order Filtering
Use when: Building the abandoned checkout flow in Klaviyo and setting the trigger and flow filters.
- In Klaviyo flow templates, search 'checkout'; the abandoned cart reminder template is actually triggered by the checkout started metric — Klaviyo names it cart but it fires on checkout.
- Confirm both an abandoned cart flow (added to cart trigger) and an abandoned checkout flow (checkout started trigger) exist, since a shopper who adds to cart without starting checkout will not enter the checkout flow.
- Add filter: placed order zero times since starting this flow, so Klaviyo checks they haven't already purchased before sending.
- Optionally add 'has not been in flow in the last X days' — the source keeps this at 2–3 days for clients so returning shoppers who restart checkout still get reminded, arguing interest justifies more sends.
Caveat: Flow filter windows (2–3 days vs. longer suppression) are a source opinion, not a benchmark; longer windows avoid over-messaging but the source believes shorter windows make more money.
Caveat: Verify current Klaviyo template naming and filter options in your account, as interface and labels can change.

Tags: email-lifecycle, abandoned-checkout, klaviyo, flow-filters, cart-recovery
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Test email and SMS sequencing in abandonment flows
Use when: Configuring the channel logic in an abandoned checkout or abandoned cart flow when you have both email and SMS.
- Review Klaviyo's default template split, which sends SMS if reachable and only sends email 4 hours later if SMS is not possible.
- Test the source simultaneous-send idea only for eligible recipients and within channel send-time and frequency rules; compare against a staggered sequence.
- Reason: you cannot know whether a given shopper converts from SMS or email; email carries advantages like visuals that SMS lacks, and after an abandoned checkout every hour counts.
- A/B test time delays (e.g., 4-hour vs. 2-hour first delay) for your own list rather than adopting a fixed default.
- Recheck purchase exclusions before messages and keep SMS quiet-hour settings enabled. https://help.klaviyo.com/hc/en-us/articles/9352115400219
Caveat: Source opinion that simultaneously sending beats SMS-first fallback; not backed by a cited benchmark.
Caveat: Shorter time delays 'typically convert better' is the source's testing observation, and they say to A/B test per client.

Tags: email-lifecycle, abandoned-checkout, abandoned-cart, sms, experiment-design, klaviyo
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Branch Abandonment Flows by Prospect vs. Existing Customer
Use when: Writing content and setting up conditional splits inside abandoned checkout and abandoned cart flows.
- Add a conditional split on 'has someone placed an order at least once over all time' — yes = existing customer, no = prospect.
- For prospects: remind them of the welcome offer they're still eligible for, show their abandoned products via Klaviyo dynamic cart content, and restate why they should buy from you (USPs).
- Use roughly a 20-hour delay between prospect emails as a starting point, then remind them of the offer and cart contents again and address 1–2 common objections (e.g., price, perceived value) using relevant customer reviews.
- Include a minimum of three abandoned cart emails for prospects, with the third addressing another objection.
- For existing customers: they are past the acquisition offer, so instead focus on other incentives — subscribe-and-save, loyalty programs, or other reasons to repurchase.
Caveat: The ~20-hour delay is a starting point the source says varies by brand.
Caveat: The three-email minimum is the source's stated floor, not a measured optimum.

Tags: email-lifecycle, abandoned-cart, abandoned-checkout, customer-segmentation, objection-handling, retention
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Link Abandonment Emails Directly Back to Checkout
Use when: Setting up links in abandoned checkout/cart email images and buttons so shoppers don't have to re-add products.
- On all image slices in the abandoned checkout flow, set the link address to the curly-bracket event variable event.extra.checkout URL.
- You can copy this link from the 'back to my cart' button that Klaviyo already includes in its abandoned cart template.
- This directs each specific person back to the checkout they started, with their products ready so they only need to place the order.
- For browse abandonment, do the equivalent: preview/test the email, open the event properties (product name, ID, price, URL), copy the product URL property, and paste it as the link on 'shop now' slices instead of Klaviyo's default organization URL.
Caveat: Dynamic variable names are Klaviyo-specific and may change — verify in the current template and event preview.
Caveat: Copying event properties requires previewing a real triggering event to see the field names.

Tags: email-lifecycle, abandoned-checkout, browse-abandonment, klaviyo, checkout, dynamic-content
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Use Klaviyo Templates Only For Dynamic Cart Tables
Use when: Building abandoned cart, abandoned checkout, or browse abandonment emails where you need a dynamic product table but custom design.
- Create the flow from Klaviyo's template (e.g., 'abandoned cart reminder') so the trigger, filters, and dynamic content are pre-built.
- The template includes a two-column table: column one pulls the product image via a dynamic variable, the other shows product title, quantity, and total.
- Delete quantity or total cells if you don't want them shown, keeping just the product name.
- Keep the graphic slices from your Figma design as separate image blocks above/below the dynamic table, mixing static design with the dynamic block.
- Preview for different profiles to confirm the right product images and titles render per recipient.
- Use the template primarily for the dynamic table because building that code from scratch is technical and time-consuming.
Caveat: For post-purchase flows with no dynamic content, the source builds from scratch instead of using a template.
Caveat: Verify current template structure and variable names in your Klaviyo account.

Tags: email-lifecycle, klaviyo, abandoned-cart, dynamic-content, email-design, abandoned-checkout
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Fix Browse Abandonment Filters and Link to the Viewed Product
Use when: Setting up the browse abandonment flow for shoppers who viewed a product but took no further action.
- Use Klaviyo's browse abandonment template (trigger: viewed product), but note the default profile filters only exclude checkout started and placed order.
- Add the missing filter: added to cart zero times since starting this flow, so only shoppers who haven't moved down the funnel receive it.
- Keep 'has not been in flow in the last 30 days' as a reasonable default for most brands, since browse-stage interest doesn't justify frequent reminders.
- Approve the source's warning about browse abandonment objectives: purchase intent is lower, so write copy that acknowledges this and consider suggesting other products.
- Emphasize social proof heavily for this audience, as they haven't signaled purchase interest yet.
- Branch prospects vs. existing customers and show the viewed products via the dynamic table; replace the template's organization-URL link with the product URL from the viewed-product event so 'shop now' goes to the product page, reducing friction.
Caveat: The 30-day flow re-entry window is the source's default preference, not a calculated rule.
Caveat: The source recommends more than the single email Klaviyo provides by default.

Tags: email-lifecycle, browse-abandonment, klaviyo, flow-filters, social-proof, product-page
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Design Post-Purchase Flows Around First-Time vs. Returning Customers
Use when: Planning the post-purchase flow that fires after an order, especially to improve first-purchase experience and repeat purchase.
- Trigger on placed order; add brand-specific filters (e.g., exclude subscription or B2B customers from the standard post-purchase content, or route them to a different flow).
- Do not schedule sends at a fixed time of day (e.g., 9 a.m.) — instead keep relative timing like '1 day after' so emails land when that buyer is typically active.
- For first-time buyers: thank them, then deliver education/resources and use cases so they get full value — a poor first experience makes a return purchase unlikely.
- Include a proactive plain-text customer-service check-in email ('how's it going, let us know if you need help'), which most brands skip and which requires no staff time once automated.
- Then move them toward a next purchase via subscription, loyalty, or other programs.
- Set a conditional split on 'placed order equals 1 over all time' to separate first-timers from returning customers, who instead get loyalty appreciation and personalized cross-sells.
Caveat: The source notes post-purchase flows are highly brand-specific, so filters and content must be set per brand rather than copied.
Caveat: The anti-9 a.m. opinion assumes buyer activity patterns match purchase time; it is a stated rationale, not a tested benchmark.

Tags: email-lifecycle, post-purchase, customer-retention, klaviyo, customer-service, cross-sell
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Time Your Win-Back Flow Using Actual Repurchase Data
Use when: Setting the initial time delay before your customer win-back flow sends its offer emails.
- Pull your order data (e.g., Shopify) and calculate the median and average number of days between a customer's purchases.
- Choose a delay between the median and average rather than guessing.
- Sanity-check the delay against your product's consumption cycle. Example from the source: a food/beverage product consumed within 30 days, with ~5 days shipping, means you can assume after ~45–50 days a customer has likely run out and may need a nudge.
- Build the flow on the placed order trigger with filter 'placed order zero times since starting this flow' so anyone who repurchases drops out automatically.
- Space the win-back emails with longer delays (e.g., 7 days and 5 days per the source) rather than one-day gaps, since you can't know exactly when the customer is ready.
- Content should say 'we miss you,' present a special exclusive offer with urgency, and reiterate why your brand beats the competition before they lapse.
Caveat: The 45–50 day example is a worked illustration, not a universal benchmark — derive your own from your data.
Caveat: Klaviyo's default ~90-day delay should not be accepted uncritically per the source.

Tags: email-lifecycle, win-back, repurchase, measurement, shopify-data, offer-design
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Build a Sunset Flow With a Segment Trigger and Profile Property
Use when: Setting up the sunset flow to remove chronically unengaged subscribers from your active list.
- Build a segment: opened an email zero times in the last 180 days AND clicked an email zero times in the last 180 days AND can still receive email marketing (not already suppressed).
- Create a flow triggered by 'added to segment' using that segment.
- Add profile filters: opened email zero times since starting this flow OR clicked email zero times since starting this flow, so anyone who engages drops out.
- Send three last-chance emails focused on a strong offer, with subject lines that highlight it; use a dynamic code so it can't leak.
- In the final email, tell them they'll be removed from the list unless they engage.
- After a further delay (e.g., 5 days), add a profile property update setting a boolean custom property (e.g., 'unengaged' = true) on anyone who never engaged.
- Create a second segment for 'unengaged = true' AND still able to receive email marketing; once a month, export that segment as CSV and import it under suppressed profiles.
Caveat: The 180-day engagement window is presented as 'usually good for most brands,' i.e., a heuristic.
Caveat: Suppression reduces active profiles and can lower Klaviyo billing, but the source frames the primary benefit as deliverability protection.

Tags: email-lifecycle, deliverability, sunset-flow, klaviyo, suppression, segmentation
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Set Campaign Cadence From Data, Not Ambition
Use when: Deciding how many campaigns per week to send for a brand roughly doing $1M–$10M/year.
- Decide the target volume based on two questions: what volume maximizes the balance of engagement, deliverability, and ROI, and what volume can you realistically sustain week after week.
- Track click-through rate, unsubscribe rate, and spam complaint rate as you increase frequency.
- If you go from one to four emails per week and those metrics stay roughly flat, you can send more — the list is signaling it wants that volume.
- If metrics deteriorate dramatically, reduce back toward the level that preserves them.
- Choose a cadence you can actually commit to: the source warns against promising four per week and delivering four one week and one the next.
- If needed, start at a sustainable two per week and invest in resources/team before increasing.
Caveat: The $1M–$10M revenue range is the source's stated sweet spot for this guidance.
Caveat: The 'metrics stay flat' test is described as a hypothetical illustration of the principle, not a fixed numeric threshold.
Caveat: Falling out of cadence risks higher unsubscribes and spam complaints and reduced engagement for seasonal peaks like Black Friday.

Tags: email-lifecycle, campaigns, cadence, deliverability, measurement, experiment-design
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Product and Collection Spotlight Campaigns
Use when: Choosing what to send in a weekly/regular campaign, especially for products you assume customers don't want.
- Product spotlight: pick one product and go deep on the details that make it better than competitors — materials, ingredients, construction — surfacing details that exist on the product page but that customers overlook.
- Frame the email around why someone should care about this product specifically, rather than letting it compete with the rest of the catalog.
- Collection spotlight: group products by a theme or common thread rather than by store category. Example cited: a 'head-to-toe neutrals' collection that pulls from separate tops and bottoms categories.
- Use this framing even for slower products — the source argues results often surprise brands that assume they aren't wanted.
Caveat: The claim that spotlighting non-bestsellers 'shocks' brands is anecdotal from the source's agency work, not a measured benchmark.
Caveat: The source reports these campaign types perform well for roughly 99% of brands based on agency data, not a controlled study.

Tags: email-lifecycle, campaigns, merchandising, product-page, collection-strategy, creative-strategy
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Benefit-Focused Campaigns: One Benefit Per Email
Use when: Planning campaign content when you have multiple selling points and want higher conversion from a specific customer segment.
- List the reasons different customer segments might buy your product (e.g., water savings, durability, materials).
- Pick one benefit that matters disproportionately to a segment on your list.
- Devote a full email to that benefit and its 'what's in it for me' — treat a single product-page bullet as the whole email premise.
- Example cited: a shower-head brand building an email around 'over a billion gallons saved' rather than listing it alongside other features.
- This approach lets you send more campaigns without repeating yourself, speaking to different benefits in turn.
Caveat: The source notes this works when one segment will overwhelmingly care about the angle — testing different angles is advised rather than assuming.
Caveat: Not a universal rule for every product with only one benefit to offer.

Tags: email-lifecycle, campaigns, offer-design, segmentation, creative-strategy, conversion-optimization
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Use Content and Education Campaigns to Seed Purchase Intent
Use when: Filling the campaign calendar when you don't have a promotion running, or when your product needs category education.
- Content spotlight: reformat existing blog or Instagram/TikTok content into an email, or use email to drive subscribers to content they haven't seen on other channels.
- Structure the email so the first section teases and links to the content, then a second section presents the product from that content as available to shop.
- Example cited: a client blog post on spotting food-allergy signs was turned into an email that teased the post and linked out, then promoted the brand's allergen-introduction products — parents learn the signs, then get offered a solution.
- Education spotlight: teach the category or ingredient deeply rather than listing benefits. Example cited: explaining everything about argan oil so readers connect the dots themselves, or a 'three reasons wet wipes are not your friend' email that makes the case against the alternative before presenting the brand's product.
- Use weekly newsletters (creation or curation — memes, playlists, industry news) to stay top of mind affordably when time is tight.
Caveat: The blog-email conversion success is an agency case example, not a guaranteed result.
Caveat: Education angles work best when your product/ingredients genuinely benefit from explanation.

Tags: email-lifecycle, campaigns, content-marketing, education, creative-strategy, retention
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Six campaign types to rotate in your email calendar
Use when: Planning next month's campaign calendar and deciding what kind of email to send each week.
- Evergreen content campaigns educate subscribers on a topic relevant to them and connect it back to why they'd buy from you (e.g., Tushy explaining a category issue and letting readers draw the conclusion to buy).
- Weekly newsletters can be created or curated; if you are tight on time, curate — memes, an industry roundup, a monthly Spotify playlist — the goal is engagement and being a brand people want to hear from, not direct revenue.
- Cultural event campaigns (Mother's Day, Father's Day, Black Friday, holidays) convert well because they tie your product to something already top-of-mind; explain why to buy for that reason (Absolut's 'serve one up for the moms who are selfless', Rebel Rabbit's 'survive the holiday hustle').
- Promotional emails split into four: teaser (warn a sale is coming / SMS gets early access), launch (sale is live — concise, sell the click not the product), last chance (final day urgency), and reminders (for multi-week sales, remind throughout instead of only at start and end; Ready Set Food adds a reminder module at the bottom of evergreen sends).
- New product launch announcements are typically among the highest revenue campaigns; send at least one the morning of launch with clear, benefit-led messaging about why the subscriber should care.
Caveat: The revenue claims for new product launches are the presenter's guarantee/opinion, not a measured benchmark.
Caveat: Newsletter-style sends often drive low revenue but high engagement — judge them on whether format can be changed to convert, not just revenue.

Tags: email-lifecycle, campaign-calendar, promotions, cultural-moments, new-product-launch, newsletter, engagement
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Message and offer matter 10x more than copy polish or design
Use when: Allocating limited time between writing/designing emails and deciding what to promote and which offer to run for a campaign.
- Before polishing a design, ask whether the product and offer actually fit the subscriber and the moment — e.g., promoting men's items for Mother's Day will not convert no matter how good the email looks.
- Treat merchandising, offer choice and topic selection as the highest-ROI activity; get granular about what you talk about and what you feature.
- For smaller brands especially, stop over-investing in pixel-perfect design and copywriting — the presenter reports auditing many brands that are overly focused on creative while the underlying offer or product choice is the real lever.
- Decide the core message and offer first, then let the copy and design serve that message rather than distract from it.
- Re-check any campaign where the featured product would not make sense to the recipient in that moment; swap the product or reframe the angle before sending.
Caveat: This is the presenter's strong opinion based on client audits, not a measured experiment; design still affects clicks and conversions, so this is about relative priority, not ignoring design entirely.

Tags: email-lifecycle, offer-design, merchandising, copywriting, campaign-strategy, prioritization
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Send campaigns to engaged segments only
Use when: Setting up the audience for any campaign in Klaviyo, especially new product launches or promos where some subscribers shouldn't receive it.
- Create engaged-time-window segments earlier (prospects engaged 90-day example) and select them in the 'send to' field of the campaign — do not send to raw lists.
- Use the 'don't send to' option to exclude subscribers for whom the message is inappropriate; for a new product launch, exclude anyone who purchased in the same category in the last 3 days by building that segment and adding it to the exclusion.
- Where a campaign resends to a narrower segment, choose that narrower segment separately (e.g., only those engaged in the last 30 days) to avoid over-mailing lower-engagement people.
- Check estimated recipients in the final review — Klaviyo shows it as the sum of included segments minus excluded segments.
- Verify your segments are updating as expected: if you want exclusions to reflect purchases at send time, use the 'determine recipients at send time' toggle when scheduling.
Caveat: If 'determine recipients at send time' is not ticked, dynamic segments are evaluated at scheduling rather than at the send moment — this is the wrong choice when excluding recent buyers.
Caveat: The specific engagement windows (90-day, 30-day, 3-day) are examples from the walkthrough, not universal thresholds.

Tags: email-lifecycle, segmentation, klaviyo, deliverability, audience-targeting, smart-sending
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Decide smart sending per campaign, not just at account level
Use when: Scheduling a high-priority campaign such as a big product launch or flagship promo, and deciding whether to let smart sending hold it back.
- Understand what smart sending does: it suppresses subscribers who recently received other emails so you don't over-send in a short window.
- Set the baseline smart-sending limitations at the account level in settings, then override per campaign when the content justifies it.
- Ask the specific question the presenter suggests: if someone received an abandoned cart email or a welcome series email within the last 16 hours, do we still want them to see this campaign?
- For a big new product launch, the presenter's guidance is to turn smart sending off for that campaign because the subscriber is likely to want to hear about it; for routine content, leave it on.
- After scheduling, confirm the smart-sending state in the final review screen — Klaviyo flags if it was disabled so you can verify it was intentional.
Caveat: Turning smart sending off for every campaign risks over-mailing and unsubscribes; this override is reserved for genuinely high-relevance sends in the presenter's view.

Tags: email-lifecycle, klaviyo, smart-sending, deliverability, new-product-launch, frequency-management
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Set up a new-product-launch campaign in Klaviyo end to end
Use when: Building and scheduling a new product launch (or similar announcement) campaign for a Shopify store.
- Go to the Campaigns tab, create a campaign, name it (e.g., 'new product launch'), set the send date, set type to email, and add campaign tags — tags help with later data analysis.
- Choose the audience segment (engaged segment) and apply any exclusions in 'don't send to'.
- Turn smart sending on or off for this campaign depending on launch priority.
- Include UTM parameters in tracking before moving on.
- Choose the creative path: reuse saved templates, use the Klaviyo email library and edit, or start new — if you built the email in Figma, use 'create new' and drag in each image slice to rebuild it.
- Write the subject line (intriguing, e.g., 'It's finally here...') and preview text (adds a second reason to open, e.g., 'the product that everyone's been asking for').
- Use the campaign sequence builder to optionally add a follow-up resend, then review settings — estimated recipients, subject, preview, content, from/reply addresses, unsubscribe link (required for compliance), and tracking.
- Schedule or send, choosing an exact send time (e.g., 9:00 a.m. Eastern when the product goes live on Shopify) or recipient local time zone, and toggle 'determine recipients at send time' if segments need to update at send.
Caveat: Klaviyo's interface changes over time; verify current menu labels and toggle locations before relying on these steps.
Caveat: The 9:00 a.m. launch-alignment timing is an example, not a rule — align send time with when the product actually goes live on your store.

Tags: email-lifecycle, klaviyo, new-product-launch, campaign-setup, utm-tracking, email-templates
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Add a follow-up resend to catch non-openers
Use when: Maximizing reach of a high-priority campaign such as a new product launch or a time-sensitive promotion.
- In the campaign sequence builder, toggle the resend to anyone who didn't open the first email.
- Write a different subject line for the resend — if the first subject line didn't engage them, try another angle (e.g., 'Brand T-shirts just in time for summer').
- Narrow the resend audience — for example if the first send went to a 90-day engaged segment, resend only to those engaged in the last 30 days to avoid over-mailing less engaged subscribers.
- Set the time delay: Klaviyo will not allow a delay under 48 hours on the built-in resend.
- For situations where you need faster or multiple resends, clone the campaign and send it manually instead of using the resend toggle.
Caveat: The 48-hour minimum limit applies to the built-in resend feature — the presenter notes this is fine for non-time-sensitive sends but inadequate for fast events like Black Friday, where you clone and resend manually.
Caveat: For Black Friday-type events the presenter suggests two or three resends of the same campaign to cut through inbox flooding — this is aggressive and should be weighed against unsubscribe risk.

Tags: email-lifecycle, klaviyo, resend, open-rate, promotions, new-product-launch, deliverability
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Write copy that sells the click, not the product
Use when: Writing a promo launch or new product launch email where the goal is to get subscribers clicking through to a product page.
- Recognize that the email's job is often to get the subscriber to the site — if they don't get there, they can't shop or buy.
- Write copy that earns the click rather than fully selling the product in the email.
- Use this especially when other campaigns or content have already done the educating — for example, a Black Friday promo email should just communicate the offer and get them out (Moment: 'up to 60% off sitewide, shop Black Friday deals').
- Keep promo launch copy short and to the point — the presenter says the best promo launch campaigns are concise.
- Ensure the destination (product page, collection page, landing page) carries the selling work, since the email is the doorway.
Caveat: This is the presenter's recommended approach for promos and launches specifically, where awareness and interest already exist; for a cold or educational campaign, more explanation in the email may be needed.

Tags: email-lifecycle, copywriting, conversion-optimization, promotions, new-product-launch, cta
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Write to one core message per email and cut fluff
Use when: Drafting a welcome email, campaign or any email that is drifting toward a kitchen-sink of messages.
- Choose the single core message for the email — avoid the common mistake of packing a welcome email with bestsellers, FAQs, a founder note and reasons to love the products all at once.
- Limit yourself to a maximum of one to two overarching themes across subject line, preview text and body.
- Cut unnecessary words and avoid paragraphs — where an icon or visual element can carry the message, use it instead of a paragraph.
- Remember that many subscribers won't read a paragraph — they'll see it, decide they don't have time, and move on.
- Write consistently in your recognized brand voice once you've defined it — if you haven't defined it, get clear on who you are as a brand and who your customer is first.
- Speak to your specific demographic rather than trying to be everything to everyone — messaging aimed at millennial women, for example, should use their language and their concerns.
Caveat: The 'shorter attention spans' rationale is the presenter's assertion, not a cited study.
Caveat: The one-to-two theme limit is a heuristic to improve clarity, not a hard technical rule.

Tags: email-lifecycle, copywriting, brand-voice, audience-research, email-design, clarity
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Lead with benefits framed for your specific customer
Use when: Writing product copy for campaigns, subscription reminders or a new product launch where the subscriber needs a reason to care.
- Define the audience first (e.g., millennial women with kids vs Gen Z men) because the same product needs different benefit framing.
- Convert product details into 'what's in it for them': instead of 'best beans grown in Ethiopia', say what the coffee does for the drinker.
- Adapt the benefit to the audience: for a busy parent millennial woman, promote energy to get through the day; for a Gen Z male audience, promote productivity for late nights or energy for sports.
- For a new product launch, ask 'why should they care?' and answer it explicitly in the email — do not leave the benefit only on the product page or packaging.
- Example from the walkthrough (Moment, still orange drink): state the benefit plainly — fights stress, boosts mood, enhances focus — plus limited stock and a try-now CTA.
Caveat: The examples are agency work shown in the course, not measured conversion results; the pattern is the transferable takeaway.

Tags: email-lifecycle, copywriting, positioning, audience-research, new-product-launch, benefit-messaging
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Subject lines and preview text: under 50 characters, frontload the value
Use when: Writing subject lines and preview text for any campaign where the subscriber sees only a truncated line in the inbox.
- Frontload the value: for a sitewide summer sale, do not write 'Summer's finally here, shop 50% off sitewide' — write '50% off sitewide' first, then use the preview text for the seasonal framing ('Summer's finally here, shop now').
- Test that if someone only reads the first three words, they still understand the value.
- Keep both subject line and preview text under 50 characters so truncation doesn't hide the offer.
- Use preview text to complement the subject line with extra detail or a curiosity hook that gives another reason to open.
- Don't over-invest in subject line perfection — the presenter says it is not the most important part of email marketing.
Caveat: The 50-character guideline and the claim that subject lines aren't the most important part are the presenter's guidance, not measured benchmarks.

Tags: email-lifecycle, subject-lines, preview-text, copywriting, open-rate, conversion-optimization
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Use persuasion levers: urgency, scarcity, social proof, curiosity gaps
Use when: Writing a promo, launch or content email and looking for a reliable way to increase clicks and purchases.
- Urgency and scarcity: state when a deal ends ('ends tonight') or that quantity is limited — the presenter says these reliably increase interest and action; use them only when true.
- Social proof: feature customer reviews, user-generated content, influencer testimonials or press mentions — anything from a voice other than the brand increases subscriber trust.
- Curiosity gap: tease content instead of revealing all of it; for a blog post, show a snippet and invite the click to read more rather than pasting the full post.
- Place the persuader where it supports the CTA (e.g., urgency near the redeem-by line, social proof near the product or checkout module).
- Do not fabricate what these devices assert — the persuasive effect collapses if the deadline or scarcity isn't real.
Caveat: The presenter frames these as effective/common but does not cite measured lift numbers; treat them as well-worn tactics, not guaranteed uplift.
Caveat: Fake urgency or invented social proof risks trust and compliance problems.

Tags: email-lifecycle, copywriting, persuasion, social-proof, urgency, conversion-optimization, cta
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Design in Figma, not in Klaviyo's drag-and-drop
Use when: Deciding where to design email creative before uploading into Klaviyo for a campaign or flow.
- Plan creative in Figma first; the presenter says strong layout and visual results shown in real examples are simply not achievable in Klaviyo's builder.
- When uploading, in the campaign template step choose 'create new' and drag in your image slices one by one until the email is built.
- The presenter's two structural reasons a Figma email outperforms: (1) structure and layout clarity, (2) the visual elements inside.
- Don't conclude your brand can't support beautiful email design — the presenter's agency file shows strong designs for bold, natural, luxe, playful and educational brands.
- After upload, verify the email renders with your brand fonts and that the layout is scannable on mobile, since sliced-image builds can be inflexible.
Caveat: The presenter's comparative walkthrough (three Klaviyo-designed emails vs client Figma emails) is illustrative, not a controlled test with click or revenue data.
Caveat: Sliced-image emails can hurt accessibility, text rendering, and load speed; this tradeoff is not addressed in the source.

Tags: email-lifecycle, email-design, figma, klaviyo, conversion-optimization, click-through-rate, brand-consistency
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Structure each email section as header, subheader, body, image, CTA
Use when: Designing a campaign or flow email layout, especially one with multiple product or content sections.
- Give each section clear headers and subheaders so the subscriber can scan without reading every word.
- Use enough white space so distinct messages read as their own sections rather than merging into a clutter.
- Follow the order the presenter calls a top performer: header, subheader, body copy if necessary, image, and CTA.
- If the section has multiple sub-sections, repeat that order within each one (as in multi-section client examples).
- Think of the layout as a visual funnel: the header creates awareness (top), body copy educates and builds interest (middle), the CTA is the ask (bottom).
- Test for scannability by asking whether a subscriber can see the offer (e.g., 15% off sitewide), the CTA, the merchandised favorites and the shipping USP without reading paragraphs.
Caveat: The specific order is the presenter's recommended hierarchy, not a proved universal rule; variations work when all elements are still clear.

Tags: email-lifecycle, email-design, layout, conversion-optimization, scannability, cta, white-space
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Three visual must-do's: CTA near products, icons not bullets, clear promo code
Use when: Finishing email visuals before sending a promo, collection or product-focused campaign.
- Put a CTA near each merchandised product so a subscriber whose eye is caught can go shop immediately — don't rely on the product image being clickable, as many brands don't even link it.
- Replace bullet points with icons (e.g., check marks) wherever the message allows — icons reinforce the point visually and are more engaging than a text list.
- For promotion emails, make the redemption code unmistakable: put it in bold immediately before the CTA (e.g., 'use code SUMMER15 at checkout').
- Watch for code placement that subscribers can miss — if the subject line says 25% off but the code is buried and 'Shop now' is the dominant element, subscribers will click without knowing they need a code and will be surprised at checkout.
- Use only high-resolution imagery, and only relevant imagery: don't place an unrelated product image next to a product, and don't use a woman in the hero of a men's clothing email.
Caveat: The warnings (missed code, blurred imagery) come from the presenter's inbox audit experience, not a measured test.

Tags: email-lifecycle, email-design, product-merchandising, promo-code, icons, imagery, conversion-optimization
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Monthly Klaviyo analytics audit: list growth, campaigns, flows
Use when: The recurring monthly review of email channel performance and technical health.
- Check list growth: in Profiles, view subscriber growth over 30 days; note total subscribers, net change, new vs lost subscribers and month-over-month trend.
- Drill into opt-in sources to see where subscribers came from (Shopify checkout and pop-up forms typically dominate) and their trends.
- Diagnose a drop: a checkout-subscriber drop that matches a proportional drop in purchases/checkouts on Shopify is not a concern; a big gap between the two suggests the integration may be broken.
- For a pop-up drop, open the form and compare views and submit rate across periods — if views fell but submit rate held or rose, the drop is traffic-driven, not form-driven.
- Review campaign performance sorted by revenue for the last 30 days; then look at click rate (interest in content/offer) and placed order rate (what drove purchases).
- Find the lowest performers and decide whether to cut, or — as with high-engagement newsletters — change the format to convert the engagement that already exists.
- Review AB tests in the experiments section, and if needed end tests manually, keeping the highest converter.
Caveat: The 27% month-over-month figure and other numbers are walkthrough examples, not benchmarks.
Caveat: Sorting by revenue is the presenter's top-KPI recommendation, not the only valid view — open rate and click rate explain why revenue changed.

Tags: email-lifecycle, measurement, klaviyo, list-growth, campaign-reporting, experiment-design, analytics
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Read open rate, click rate and placed orders as a diagnostic layer stack
Use when: Diagnosing why a specific campaign over- or under-performed and deciding what to change next time.
- Read open rate as a signal of subject line strength, targeting quality and send timing.
- Read click rate as the metric for whether subscribers cared about the content and the offer — this is the metric to judge content/offer fit.
- Read placed order rate (and revenue) as the indicator of what actually drove the purchase decision.
- Expect divergence: a campaign can drive more clicks but fewer purchases (content is engaging but the reason to buy is weaker), and less-clicked campaigns can drive more revenue when the offer is a strong purchase moment (e.g., Father's Day gifting).
- Use this reading to decide whether to fix subject line/targeting (low open), content/offer interest (low click), or offer strength (low orders), and check whether you're treating a high-engagement, low-revenue send (like a newsletter) as a failure when it's actually an audience-interest signal.
Caveat: The presenter asserts benchmarks that you should at minimum see open rates above 30% and click rates above 0.5%, calling anything lower a likely deliverability problem; they also warn that universal benchmark numbers are not reliable without a deep account audit.
Caveat: Machine opens can inflate open rates. Include click and purchase behavior in diagnosis; do not infer deliverability solely from opens. https://help.klaviyo.com/hc/en-us/articles/4416803987739

Tags: email-lifecycle, measurement, open-rate, click-through-rate, campaign-reporting, customer-research, diagnosis
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Use revenue and order count together to catch high-AOV distortion
Use when: Analyzing top and bottom campaigns to decide which products, collections or campaign types to repeat.
- Sort campaigns by revenue first, since revenue is the primary KPI when the goal is revenue growth.
- Then check placed order counts alongside revenue, especially for brands with high-priced, high-value products.
- Note that a higher-revenue campaign can drive fewer purchases (e.g., $300 more revenue but 15 purchases vs 22 on a lower-revenue campaign), and the fourth-best revenue campaign can have the most unique purchases of the month.
- If you're promoting products or collections that pull average order value down, the presenter suggests that may be a reason not to focus on them as much.
- Combine this with click rate to understand whether the issue is interest or unit economics.
Caveat: The specific numbers cited are from one walkthrough example, not general benchmarks; AOV distortion patterns vary by store.
Caveat: Revenue remains the presenter's recommended first KPI — this card is an adjustment to, not a replacement for, that.

Tags: email-lifecycle, measurement, revenue, average-order-value, campaign-reporting, merchandising, analytics
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Diagnose a subscriber drop by separating traffic from form performance
Use when: Monthly growth review shows a drop in new email subscribers and you need to decide whether to act on the form.
- Open opt-in sources and compare Shopify checkout subscribers and pop-up subscribers against Shopify purchase and checkout-started trends — a proportional drop suggests the integration and channel are fine.
- For pop-up forms, open the form's reporting and compare form views and submit rate across the last 30 days and the prior 30 days.
- If views dropped roughly 20% but submit rate rose from 2.19% to 2.28%, the subscriber decline was traffic-driven, not a broken form; the presenter treats this as no cause for concern.
- Check whether the submit rate dropped dramatically, since form conversion is what you can control in Klaviyo — optimize here if it did.
- Where form conversion is the issue, run or review an AB test on the form (the walkthrough shows an example test improving submit rate from 3.11% to 4.29%).
Caveat: Submit-rate figures and the 20% view drop come from the walkthrough example, not a general benchmark; traffic attribution to paid/organic varies by brand.

Tags: email-lifecycle, list-growth, pop-up-forms, klaviyo, attribution, measurement, experiment-design
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Interpret Klaviyo's AB test statistics before trusting a result
Use when: Deciding whether to call an A/B test campaign, subject line or flow variation a winner and roll it out.
- Open each AB test in Klaviyo's experiments section and read the lift in click rate, open rate or placed order rate and the win probability.
- Watch for the case where one variation had the highest result during the test window but a different variation had the highest result overall on the full send — Klaviyo notes this can occur due to random chance.
- When that happens, follow the guidance the platform gives: increase the length of the AB test period and/or increase the test size and rerun, taking the result with a grain of salt.
- Manually end tests once a month when needed and keep the highest-converting variation.
- Set up the next test each month regardless of outcome — the presenter argues that not testing means guessing about what your subscribers care about.
Caveat: Klaviyo's statistics UI and recommendations may change over time; verify the current interface.
Caveat: The presenter frames A/B testing as essential but doesn't establish a specific minimum sample size or duration.

Tags: email-lifecycle, experiment-design, klaviyo, measurement, statistical-significance, subject-lines, pop-up-forms
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Read top-level business review to attribute email revenue and understand month-over-month shifts
Use when: Reporting monthly email performance to the store owner and deciding whether growth came from campaigns or flows.
- Open dashboards > business review, set your time period and choose the comparison: previous period, or previous year if the brand is very seasonal.
- Note total store Shopify revenue and its month-over-month movement.
- Note attributed revenue and the percentage of total revenue coming from email — in the walkthrough example, just under 40% and up 9% month over month.
- Open the message type breakdown to separate campaign revenue from flow revenue and their respective trends (example: campaign revenue $43K, up 54% month over month; flow revenue down 16%).
- When a number moves sharply, dig underneath it — see the campaign revenue overview with conversion value, revenue and total recipients to understand what drove the shift, rather than reporting the headline alone.
Caveat: The revenue figures and percentages are from one client walkthrough and are not universal benchmarks.
Caveat: Attributed revenue depends on the attribution model in use; verify the model before presenting numbers as email's true contribution.

Tags: email-lifecycle, measurement, klaviyo, attribution, revenue, reporting, campaign-reporting, flows
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Ensure every email adds value before it ships
Use when: Final pre-send check on any campaign or flow email to catch content that has no clear subscriber benefit.
- Ask the presenter's test question: why is my subscriber going to care about this, and will they be glad they opened it?
- Answer against the three value types — does this email educate, entertain, or solve a problem?
- If the answer is 'no' or 'I'm not sure', go back to the drawing board and rewrite rather than scheduling it.
- Apply this equally to automated flow emails, not just campaigns.
- Use the same question when assessing why a low-revenue but high-engagement newsletter performed the way it did — if subscribers enjoy it, change the format to drive revenue rather than cutting it.
Caveat: The presenter's standard is subjective and their claim that new product launches are among the highest revenue campaigns is expressed as a personal guarantee, not a measured result.

Tags: email-lifecycle, copywriting, retention, audience-research, content-strategy, quality-control
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Monthly email business review: campaign revenue decomposition
Use when: Running a monthly email/retention performance review and you need to explain a revenue change rather than just report it.
- Pull total store revenue (e.g. Shopify), attributed email revenue, and email's share of total revenue; note month-over-month change in the email share.
- Break attributed revenue into campaign revenue vs flow revenue and note each one's month-over-month change separately — they move for different reasons.
- Under campaign revenue, look at conversion value, revenue and total recipients, then the metric rows beneath.
- Test the 'we just sent more' hypothesis first: if total recipients only rose a few percent (e.g. ~3.5%) while revenue rose 54%, volume is not the explanation.
- Then read the chain: unique opens, open rate, unique clicks, click rate. In the source's example unique opens +13.6%, open rate +9.8%, unique clicks +15.6%, click rate +11%.
- Find the outlier — in that example unique conversions +40% and order conversion rate from email +37% — and ask what merchandising or offer caused it (a sale, a launch, or just education content).
- Close the loop by checking top-performing campaigns this month vs last month to see which specific sends drove the outlier.
- Ladder the metrics back up: revenue per recipient and AOV should explain the remaining gap between click growth and revenue growth (source example: RPR +49%, AOV +17%).
Caveat: The source's numbers are one client's first month with an agency, not a benchmark; treat them as an example of the diagnostic logic.
Caveat: The source recommends building a custom dashboard tool for this at scale; Klaviyo's native reporting gives similar insight with more manual work. Verify the current Klaviyo interface.
Caveat: Numeric stage bands here are heuristics, not calculations.

Tags: email-lifecycle, measurement, email-analytics, campaign-reporting, revenue-per-recipient, retention
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Optimize for unique opens and unique clicks, not open rate and click rate
Use when: Deciding whether to add campaign sends or widen a segment, and deciding which metrics to report on and optimize.
- Translate every metric change into people counts: an open rate falling 10% while unique opens rise 40% means 40% more humans opened, all of whom are eligible to click.
- Accept that sending three campaigns a week instead of one can mechanically lower open rate and click rate while raising unique clicks; do not treat the rate drop as failure.
- Use unique opens as the leading indicator for how many people can act, and unique clicks as the leading indicator of real engagement and (per the source) inbox placement.
- Watch for the source's stated pattern: unique conversions can rise far more than unique clicks (example: +15% clicks, +40% purchases) because of what happens on site — a sale or product launch, not the email alone.
- Report unique metrics in your monthly review so volume decisions aren't punished by rate declines.
Caveat: This is an attributed agency opinion ('at Dispatch we optimize for unique clicks'), not a universal law; it makes most sense for accounts deliberately scaling send volume.
Caveat: Attributed revenue and unique conversions depend on your attribution window and platform tracking, so verify before treating a 40% swing as causal.

Tags: email-lifecycle, measurement, email-analytics, unique-clicks, deliverability, list-strategy
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Diagnose falling email metrics by which metric moved
Use when: A monthly review shows email revenue or engagement dropping and you need to decide where to investigate first.
- If open rates and unique opens are falling dramatically, investigate deliverability and list health first (sending to unengaged cohorts, list growth quality, sender reputation).
- If unique clicks or click rate are falling, treat it as a content/engagement problem — the emails or subject matter aren't landing with that audience.
- If unique conversions and order conversion rate are falling while clicks hold, treat it as a merchandising and offer problem: the products, offers, and CTAs in the campaigns aren't compelling enough to make people buy.
- Ignore small month-to-month noise — the source treats sub-5% moves as normal fluctuation and looks for jumps over ~10%.
- Check overlap and volume before blaming content: too many sends to the same people depresses rates without any content problem.
Caveat: Apple Mail privacy protection inflates/unreliably measures opens, which is why the source distrusts open rate as a deliverability signal and prefers clicks.
Caveat: These are diagnostic heuristics from the source, not statistically derived thresholds.

Tags: email-lifecycle, measurement, deliverability, email-analytics, conversion-optimization, diagnostics
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Flow revenue review: traffic first, then the flow chain
Use when: Monthly retention review of automated flows (welcome, abandoned cart, abandoned checkout, winback) when flow revenue moved.
- Gut-check site traffic first: flow revenue down ~30% is usually explained by ~30% fewer people seeing the popup, opting in, and entering the welcome flow. If traffic was up while flow revenue fell, that is the real red flag.
- Split flow revenue into conversion value and recipients, then read recipients: up means more traffic or more emails added into the flows versus last month.
- Read the engagement chain: unique opens, open rate, unique clicks, click rate. Ignore sub-5% moves; investigate >10% jumps.
- If click rate fell meaningfully (example −15%), consider deliverability first, since opens are polluted by Apple Mail privacy; clicks are the primary placement signal.
- Reconcile conversions vs revenue arithmetically: unique conversions −6% with revenue −15% implies AOV fell substantially — confirm in the AOV row (example: −15%).
- Check AOV drivers: a sitewide sale (e.g. 15% off for the month) mechanically cuts flow AOV, as does dynamic content serving lower-priced products than the prior month.
- Go to top-performing flows: expect welcome series then abandonment flows to lead; compare each flow's revenue to last month and open any flow with a large gap.
- Inside a flow, use the per-email analytics to compare open and click rates against the prior month, and check skip counts for people being filtered out unintentionally.
Caveat: The source notes Klaviyo does not natively surface per-flow delivery/click/RPR trends in one view; they use an external dashboard. Verify current Klaviyo reporting.
Caveat: AOV movement in flows is often outside email's control (sitewide promotions), so don't attribute it to email execution without checking.

Tags: email-lifecycle, email-analytics, flows, retention, measurement, abandoned-cart
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Audit flow skip logic when a flow's revenue drops
Use when: A specific flow (welcome, cart, post-purchase) lost revenue month over month and you've ruled out traffic.
- Open the flow and use the per-email analytics/skip view to compare this month against last month.
- Read the skip count against deliveries as a ratio, not in isolation — the source gives an example of 620 skipped vs 190 delivered that they knew was intentional, versus cases where subscribers are skipped inadvertently.
- Inspect trigger filters, conditional splits, and profile filters (e.g. 'has placed order 0 times since starting this flow') for conditions that are now excluding eligible people.
- Check for overlap suppression: flows that don't send because the person is also receiving a campaign or another flow.
- Fix unintended exclusions, then re-check opens, clicks, and purchases in the following period, since fewer deliveries mechanically ladders down to less of all three.
Caveat: A high skip count is not automatically a bug; it can be by design. The source only flags it as the first thing to examine, not as proof of a problem.

Tags: email-lifecycle, flows, email-analytics, segmentation, retention, diagnostics
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Run one high-leverage campaign A/B test per month
Use when: Planning the monthly campaign experiment in Klaviyo or equivalent, and choosing what to test.
- Build version A (control), then use the platform's 'create A/B test' option and choose content or send-time test. Verify button names in the current interface.
- For send-time tests, keep the copy and design identical and vary only the send hour; the source suggests click rate as the winning metric there, since opens are unreliable.
- For content tests, do not spend the test on subject line or preview text — the source says after hundreds of tests, email body content is the highest-leverage test.
- Test high-leverage content variables: the offer, which product types are featured, imagery type (lifestyle vs product, single image vs four-image layout, static vs GIF), and CTA copy (e.g. 'shop now' vs 'save now').
- Change exactly one thing between A and B. Do not vary subject line and content together, or stack a second content change on top — you won't know which change caused the result.
- Set the winning metric to placed order rate rather than open rate or even clicks, because the goal of every test is revenue.
- Keep size distribution at 100% for most brands so the whole audience is split 50/50; a 40% holdout that decides the winner is not statistically meaningful for typical list sizes.
- Name variations descriptively (e.g. 'one image hero' vs 'four image hero') so the result is readable later.
- Log the test in the experiments section so the learning rolls into the next month's planning.
Caveat: Source opinion: they always use placed order rate as the winning metric and say never to use open rate. This favours tests with enough volume to resolve on a downstream metric.
Caveat: The source explicitly says most brands can't reach statistical significance on a partial-holdout test, so a 100% split is a volume-constrained compromise, not a significance guarantee.

Tags: email-lifecycle, experiment-design, ab-testing, campaigns, conversion-optimization, measurement
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Flow A/B tests with automatic distribution
Use when: Testing two versions of an email inside a flow (welcome, abandoned cart, post-purchase) while the flow stays live.
- Open the specific email inside the flow, keep the current version as A, and use the create A/B test action at the bottom of that email.
- Set the same style of winning metric logic you use for campaigns — the source favours placed order rate as the revenue-linked goal.
- Because flows collect data continuously, select the automatic distribution option: the platform initially sends ~50/50 and shifts allocation as its model identifies a winner, then sends only the winner once significance is reached. Verify this option still exists in the current interface.
- Change only one element between the two versions, exactly as with campaign tests.
- Monitor progress in the experiments section rather than judging on the first few days.
Caveat: Automatic distribution depends on the platform's statistical model; results are only as trustworthy as the traffic volume in that flow email.

Tags: email-lifecycle, experiment-design, ab-testing, flows, conversion-optimization, klaviyo
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Reviewing completed and in-progress A/B tests
Use when: Your monthly review of experiment results, or deciding whether to ship a variation and pick next month's test.
- Open the experiment/flow A/B test view and compare version A and B on click rate and placed order rate, not on open rate.
- Read the reported win probability. In the source's example, version A showed a 98% win probability, which they describe as not statistically significant but supported by enough data to act.
- Consider account size: the source notes smaller brands may never reach formal significance even after several months of running a test.
- When one version is clearly driving more revenue and the difference is meaningful, declare the winner, keep it live, and move on to planning the next test rather than waiting indefinitely.
- Carry the learning into the test roadmap — for example, if four images beat one, treat that as a hypothesis to build on, not a permanent rule.
Caveat: Win probability is the platform's estimate, not proof; the source explicitly acknowledges the example was not statistically significant and still chose the winner.
Caveat: This is a pragmatic agency judgment call, not a statistical standard — hold it to a higher bar for tests that would change pricing or core offer structure.

Tags: email-lifecycle, experiment-design, ab-testing, measurement, campaigns, flows
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Monthly deliverability health check inside Klaviyo
Use when: Monthly email operations review, or when open/click metrics have been sliding and you suspect inbox placement.
- Open the deliverability tab and read the deliverability score, which the source says is based on open rates, click rates, bounce rates, unsubscribe rates, and spam complaint rates; track it over time.
- Compare your account rates to the platform's recommended healthy ranges. The source cites: open rate above 33% considered okay; click rate above 1.2% considered okay; bounce rate under 1%; unsubscribe rate under 0.3%; spam complaint rate under 0.01%. Re-check these numbers in the current interface as they change.
- Prioritize keeping bounce and spam complaint rates well under the guidelines — the source treats those two as the hard limits; unsubscribe slightly above the recommendation is described as tolerable when send volume drives more revenue.
- Read both sides of the account: recent campaigns and your flows, since flows contribute separately to sender reputation.
- Every ~30 days open the reports section to see performance by mailbox provider; in the source's example Gmail and Verizon sat near 63-70% opens while Hotmail/Outlook were ~46% with a lower click rate, and G Suite showed both high bounce and high unsubscribe rates.
- For weak providers, build tightly engaged segments specific to those providers to stop deteriorating reputation there.
- Verify placement with click rate rather than open rate, since Apple Mail privacy inflation has made opens unreliable.
Caveat: The thresholds above are Klaviyo's recommended values as presented in the source; verify current guidance before treating them as targets.
Caveat: The source says deliverability problems generally stem from failing the basics (unengaged segments, excessive sending, flow/campaign overlap) rather than from technical setup.

Tags: email-lifecycle, deliverability, measurement, list-health, segmentation, klaviyo
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Recover inbox placement by tightening the engagement segment
Use when: Deliverability remediation: your usual engaged segment is no longer producing healthy open and click rates.
- Confirm the trend is steady decline in both opens and clicks, not a one-month fluctuation (ignore sub-5% moves).
- If you normally send to a 90-day engaged segment, switch campaign and flow sends to a 30-day or 60-day engaged segment so the audience is more recently active.
- Hold that tighter segment until open and click rates climb back to healthy levels — the goal is to demonstrate to inbox providers that recipients want your mail.
- Expand the window gradually (e.g. 30 → 60 → 90 days) rather than jumping straight back to the wide segment.
- In parallel, check campaign/flow overlap so the same people aren't being hit twice, which drives unsubscribes and complaints.
Caveat: Tightening segments reduces short-term reach and revenue; the source frames it as a deliberate trade to repair reputation.
Caveat: No recovery timeline is given in the source; expect it to depend on your volume and reputation damage.

Tags: email-lifecycle, deliverability, segmentation, list-health, retention, campaigns
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Dynamic content blocks to merge segmented campaigns into one send
Use when: You would otherwise build two near-identical campaigns for different regions, tiers, or customer states (e.g. different free-shipping thresholds, unused acquisition offer, loyalty points balance).
- Inside the email block, open the block settings and find the display / show-hide logic area (verify current naming in the interface).
- Choose the profile property and set a condition, e.g. country equals United States.
- Match formatting exactly: the property value you type must use the same spelling and letters as stored on the profile — check a real US profile to copy the exact string (e.g. 'United States').
- Duplicate the block and invert the logic for everyone else (does not equal United States), then edit the copy for that group (e.g. free shipping over $150 instead of $100).
- Preview against test profiles that have the property set and unset — the source shows that a profile with no country set falls into the 'not United States' branch by default, so decide whether that default is acceptable.
- Apply the same technique to other data you hold: show reviews based on zero-party data, remind prospects of an unused acquisition offer, or tell existing customers their current loyalty points balance.
- Keep the blocks' content substantively different so personalisation is real, not cosmetic.
Caveat: Incorrect or inconsistent property formatting silently routes people to the wrong variant — always test both branches.
Caveat: Profiles missing the property fall to the negative branch; add an explicit fallback if the wrong message would be harmful.

Tags: email-lifecycle, personalization, dynamic-content, segmentation, campaigns, flows
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Trigger a winback from expected next order date
Use when: Building or upgrading a winback / reactivation flow so timing is personalised rather than based on a list-wide average.
- Create a flow manually and look for the date-property trigger option rather than a time-delay trigger.
- Select the expected-date-of-next-order property available on each profile.
- Choose to trigger on the date property value (not before it), because that is the date the model expects the repurchase; the source's example fires at 12:00 p.m. local time. Verify trigger timing options in the current interface.
- Set the flow to never repeat, since you don't want the same winback email firing monthly to someone who has already been contacted.
- Add a profile filter requiring zero orders placed since entering the flow, so anyone who buys drops out.
- Add a short delay (the source suggests ~5 days after the expected date) to give them a grace period before you introduce winback offers.
- Optionally branch on predicted or historic customer lifetime value (e.g. CLV at least $1,000) to give high-value customers a more personalised, stronger offer.
- Compare against a simple version of the same flow where you trigger on average days between orders, especially if you have limited data on an individual.
Caveat: Predictive dates are model estimates from Klaviyo and are less reliable for customers with few orders; verify the property is populated before relying on the trigger.
Caveat: Treating predicted high CLV customers as already-high-value is the source's suggestion for proactive retention, not a proven conversion lift.

Tags: email-lifecycle, retention, flows, winback, predictive-analytics, segmentation
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Use predictive CLV and churn risk in flow splits
Use when: Designing conditional splits in retention or winback flows to vary offer strength and personalisation by customer value.
- Locate the predictive properties on a customer profile (expected next order date, average time between orders, churn risk prediction, average order value, historic and predicted CLV) to confirm which are populated for your account.
- Build a conditional split on customer lifetime value — either historic CLV at least $1,000, or predicted CLV above the threshold.
- Send higher-value customers a more personalised, better discount in the winback path, on the reasoning that recovering them is worth more.
- Use predicted CLV to treat promising customers as high value earlier, before they have reached the threshold historically.
- As with any split, monitor performance per branch over time; the source treats this as personalisation upside and notes Klaviyo keeps improving these models.
Caveat: This is presented as an opportunity, not a tested result; the source gives no lift figures.
Caveat: Predictions require sufficient order history to be meaningful — thin accounts will have weak or empty values.

Tags: email-lifecycle, retention, predictive-analytics, flows, segmentation, personalization
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Build multichannel touchpoints into flows (email, SMS, push)
Use when: Designing or upgrading an abandoned cart, abandonment, or similar conversion flow where you already have email and want more touchpoints.
- In Klaviyo settings, find the SMS and push notification sections and complete setup — you get a phone number and compliance tooling for SMS, and push requires a custom mobile app; verify current setup requirements in the interface.
- Inside a flow, add an SMS or push step in addition to the email steps.
- Sequence channels by intent: in an abandoned cart flow the source gives the example of sending SMS first to convert, then waiting ~2 hours and sending the email to anyone who hasn't purchased yet.
- Rely on flow filters so someone who converts exits and doesn't receive the later, redundant touchpoint.
- Keep the offer and message consistent across channels so the follow-up feels like one conversation.
Caveat: Push notifications require your own mobile app; they are not available to a mobile-web-only store.
Caveat: SMS has consent and compliance obligations that vary by region — the source only notes Klaviyo supplies the compliance pieces, not that setup alone makes you compliant.

Tags: email-lifecycle, flows, sms, push-notifications, multichannel, abandoned-cart
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Integrate ecommerce apps to drive flow triggers and segmentation
Use when: Setting up or expanding a Klaviyo account and deciding which integrations to add first.
- Go to settings → integrations → add integrations and filter to all to see the available directory (source cites 187 live integrations); verify the current count in the interface.
- Start by integrating the apps you already run on Shopify, not new apps you don't use yet. The source's path: check Shopify's app list, then search those app names in Klaviyo's integration settings.
- Install directly from Klaviyo, and read the overview of what data the integration passes and which features it enables before connecting.
- Note that many integrations are configured inside the third-party app, not in Klaviyo — the source's loyalty example has the API key, status, and event triggers managed in the app.
- Map the resulting events to flows — the source's examples: a Recharge subscription pause triggers a flow to unpause; a reviews app passing 'left a review' prevents asking for a review on that product again.
- Map synced properties (e.g. points balance, loyalty status, VIP tier name, birthday, referral URL) to segmentation and personalisation.
- For ad platforms, pass email addresses from Klaviyo segments (e.g. a high-value purchaser segment) to Meta or Google for retargeting and lookalike audiences based on your own data.
Caveat: Integration directory contents and setup screens change — verify in the current interface before following exact menu paths.
Caveat: More integrations mean more data flowing, but the source advises starting with what you already use rather than integrating speculatively.

Tags: email-lifecycle, integrations, klaviyo, flows, segmentation, acquisition
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Trigger a birthday flow using loyalty app point properties
Use when: Running a loyalty-driven retention campaign where members earn birthday points and you want one email that renders per-customer numbers.
- Confirm the loyalty app passes a birthday event and the relevant profile properties (points earned on birthday, points balance, loyalty status, VIP tier) into Klaviyo.
- Create a flow triggered by that metric, e.g. the loyalty app's customer-birthday event, then add the email step.
- In the email, insert the event property for points earned in this specific event so each recipient sees their own number (e.g. 250 points earned).
- Add personalisation and search the integration's properties to insert the customer's current points balance, which will differ per person (source example: 1,669 for one customer, 355 for another).
- Use preview and test on the specific profile that triggered the metric to confirm the numbers render correctly, then check a second profile to confirm they differ.
- If different tiers earn different birthday points, the event property handles the variation without separate emails.
- Decide on placement — the source uses birthday as a trigger for both email and SMS — and whether to include a redeem link or code.
Caveat: The flow only works if the integration reliably fires the birthday event and the event property is present; test the event before building the creative.
Caveat: Copy used in the source's example is sample copy, not tested copy — build your own.

Tags: email-lifecycle, personalization, integrations, flows, loyalty, retention
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Use dynamic blocks to personalise shipping thresholds and offers in one send
Use when: Merchandising or offer communication that differs by country, tier, or subscriber state — free shipping thresholds, unused welcome offers, loyalty balances.
- Identify messages you currently split into multiple campaigns or segments — for example a US free-shipping-over-$100 message versus a rest-of-world free-shipping-over-$150 message.
- Build one email and add a text block at the top for the first variant, then apply show/hide logic on the property that distinguishes the groups (e.g. country equals United States).
- Duplicate the block, invert the logic, and rewrite the copy for the second group.
- For offer reminders, show prospects the acquisition offer they haven't used yet, and show existing customers their current loyalty points balance — using properties the integrations push onto profiles.
- For zero-party data, show different customer reviews or content based on what the subscriber told you.
- Preview against multiple test profiles, including one missing the property, so you know which branch default behaviour sends them to.
- The source also uses predictive data in the same spirit: a higher-value customer branch can receive a stronger offer.
Caveat: Property formatting must match exactly what is stored on the profile, or the condition won't match.
Caveat: Running one conditional email instead of multiple sends reduces work but means a single send's metrics mix groups — plan how you'll read results.

Tags: email-lifecycle, personalization, dynamic-content, merchandising, campaigns, segmentation
Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx

---

## Non-discount email strategy: replace constant promos with objection-handling content
Use when: Planning the overall email program for a store that currently relies on frequent sitewide discount blasts and is eroding margin.
- Audit current sends: count how often the whole list gets a % off promo versus value or education content; if discount-only is your main strategy, treat it as the problem to fix.
- Reframe email's job as handling buyer objections one at a time and slowly educating the customer toward a full-price purchase, rather than converting every send.
- Map the top objections a first-time buyer has (trust, 'who is this brand', 'why you over competitors', 'what do people say') and assign each to a content bucket.
- Keep discounts as an optional fifth bucket: the source recommends roughly one sale/discount offer per month so list members feel rewarded for staying subscribed.
- Send the non-discount program to the engaged segment at the target cadence rather than building heavy segmentation first; the source treats elaborate segmentation as unnecessary here.
- Track unsubscribes and engagement alongside revenue when shifting to non-discount content, since the source's claim that this yields 30-50% of store revenue is a description of his own client results, not a guaranteed benchmark.
Caveat: The revenue-share numbers come from the presenter's own client work and are examples, not promises.
Caveat: A once-monthly discount is a recommendation, not a universal rule; margins and category norms vary.

Tags: email-lifecycle, retention, email-strategy, offer-design, discount-strategy, objection-handling, broadcast-campaigns
Source: Complete Ecommerce Email Marketing Strategy For 2026.docx

---

## Send 3-4 broadcast emails per week to stay top-of-mind
Use when: Setting or revising the sending frequency for your recurring (non-triggered) email campaigns.
- Assess your current cadence: 1-2 sends/week risks customers forgetting the brand, failing to form an opening habit, and weak sender reputation with inbox providers; 5-7/week risks high unsubscribes, diluted messaging, and revenue plateauing.
- Target roughly 3-4 sends per week (about 16/month) to your engaged list as the source's default, based on his stated testing across 200+ brands.
- Keep content quality as the gating factor: lower unsubscribes at this cadence depend on sending the right content mix, not just sending more.
- Recognize the cadence is also a deliverability play -- consistent sending builds sender reputation so mail lands in the primary inbox.
- Treat brand specifics as adjustable: the source explicitly says every brand is different, so use 3-4 as a starting heuristic and test against your own unsubscribe and revenue data.
Caveat: 3-4x/week is a source-specific heuristic from his testing, not an industry benchmark; your list tolerance may differ.
Caveat: High frequency without the right content mix will still drive unsubscribes and fatigue.

Tags: email-lifecycle, retention, sending-frequency, deliverability, email-strategy, list-health
Source: Complete Ecommerce Email Marketing Strategy For 2026.docx

---

## Balance broadcasts across four non-discount content pillars plus an optional sales pillar
Use when: Building a monthly email content calendar and deciding what each broadcast should be about.
- Define the four non-discount buckets: educational (FAQs, ingredient education, how-to, 'how you've been using it wrong', what's not in the product, what happens if you stop); social proof (testimonials, media features, real-people results, influencers); community/brand (mission, brand timeline/history, values, why we exist, founder notes); product/collection highlights (trending, spotlights, gift guides, seasonal must-haves, product breakdowns).
- Add the optional fifth bucket: sales (teasers, launches, gift-with-purchase, mystery offers).
- Aim for a roughly even split across pillars. The source's example: for a 10-email month, do about 2-3 of each pillar, e.g., ~3 educational, 3 social proof, 3 product, 3 community/brand, and 2 sales.
- Keep the mix stable month to month so the list gets variety without becoming discount-dependent.
- Use the pillar split as the input to a calendar (AI or manual) so each slot is assigned a type before writing copy.
Caveat: The even-split ratio is an example from the presenter's own email revenue experience, not a calculated optimum.
Caveat: Bucket labels and counts can flex with seasonality (e.g., gift guides near holidays).

Tags: email-lifecycle, retention, content-calendar, email-strategy, broadcast-campaigns, content-pillars
Source: Complete Ecommerce Email Marketing Strategy For 2026.docx

---

## Turn macro topics into hyper-specific microtopics for each email
Use when: Filling calendar slots with campaign topics and writing subject lines/headlines for value emails.
- Start from the brand's macro topic (e.g., 'holistic health' or 'mental performance') and break it into hyper-specific angles.
- Write topics with a single takeaway, phrased concretely: 'three ways high performers use [product] to win the day', 'ingredient deep dive: what makes adaptogens powerful', 'how to use [product] for 30 days and what to expect', 'what happens if you stop using it', 'label decoder'.
- Avoid generic topics like 'our product is amazing' or 'get better overall health' -- the source identifies specificity as what makes non-discount emails convert.
- Tie social proof to a specific experience a reader may be having (e.g., collect testimonials from people who quit coffee for a 'finally ditched coffee' email) and pull matching quotes from the site.
- If topic generation is hard, use the pattern library: educational angles, social proof angles, community/brand angles, product/collection angles, then sales angles.
Caveat: Specificity of ingredient/health claims should satisfy any legal or regulatory constraints in your category.

Tags: email-lifecycle, retention, content-ideation, email-copywriting, microtopics, content-calendar
Source: Complete Ecommerce Email Marketing Strategy For 2026.docx

---

## Use a two-step ChatGPT priming workflow to generate calendar ideas and copy
Use when: Generating a month of campaign ideas or drafting email copy fast, when you have brand and product context ready to feed in.
- Step 1 - Prime: feed the model all brand voice, product details, target audience, and unique selling propositions before asking for anything.
- Step 2 - Instruct: ask for a punchy headline, a sub-headline, and exactly 2-3 sentences of body copy that lead to a CTA -- this mirrors the source's custom GPT ('email marketing brain') behavior.
- Ask for a balanced calendar across the five content types; verify the output's pillar counts (e.g., the source's sample month returned 4 educational, 3 social proof, 2 community/brand, 2 product/collection, 3 sales across weeks of 3-4 sends).
- For subject lines and preview text, treat them as the email's headline and sub-headline; the source argues sender name drives opens more than the subject line (a stated opinion, not a measured rule).
- Always review and edit AI output -- the source notes it is 'not going to be perfect' (e.g., a missing CTA) and must be checked.
- If the tool interface has changed since this source, re-verify menu options and prompts in the current interface before following the exact flow.
Caveat: LLM output must be fact-checked against actual product/ingredient facts; the source pulls final facts from the brand's own site.
Caveat: Custom GPT/tool specifics are vendor- and version-dependent and should be re-verified.

Tags: email-lifecycle, retention, chatgpt, ai-copywriting, prompt-engineering, email-copywriting, content-calendar
Source: Complete Ecommerce Email Marketing Strategy For 2026.docx

---

## Structure email layout as headline, sub-headline, short body, CTA, infographic, product block
Use when: Laying out any broadcast email before sending to design.
- Open the email with a clear headline and sub-headline that calls out a specific problem the reader has (e.g., 'brain fog has met its match').
- Follow with a short block of body copy (a few sentences) that introduces the mechanism/benefit, then an immediate CTA.
- Add a hero/graphic section, then an educational infographic section (e.g., ingredient breakdown) that visualizes the mechanism.
- End with a product/CTA section -- choose the offer (starter kit, multi-pack, or subscription) and link the CTA to the product page.
- Assemble this in a plain document (e.g., a table with a row per section) to visualize the email before handing to design.
- Keep total copy minimal -- the source stresses how little text is used and credits the layout, not length, for conversion.
Caveat: This is the source's demonstrated layout, not a proven maximum-conversion template; test variations.

Tags: email-lifecycle, retention, email-design, email-layout, conversion-optimization, product-page, cta
Source: Complete Ecommerce Email Marketing Strategy For 2026.docx

---

## Mix graphic-based and text-based emails at roughly 3-4:1
Use when: Deciding the format (graphic vs plain-text) for each send in the calendar.
- Default to graphic-based emails for education and infographic content that readers skim.
- Insert plain-text emails that look like a personal message from a real person (e.g., founder note) -- the source says his best-performing emails of all time are these text-based sends.
- At the source's example cadence of 16 emails/month, send roughly 12 graphic and 4 text-based to hit the ~3-4:1 ratio.
- Place text-based sends in the community/brand pillar where founder notes, mission, and behind-the-scenes content naturally fit.
- Write the text email in a conversational first-person voice (e.g., 'Hey, James here... I built this because...'), keep it short, and make sure it still includes a CTA if the draft omits one.
Caveat: The 3-4:1 ratio is the source's guideline, not a universal constant; test your own split.
Caveat: Plain-text sends still need a CTA and a clear linking target to convert.

Tags: email-lifecycle, retention, email-format, plain-text-email, founder-email, email-design, engagement
Source: Complete Ecommerce Email Marketing Strategy For 2026.docx

---

## Apply the skimable, clear/concise, engaging copywriting rules
Use when: Drafting or editing the body copy and headlines of any broadcast email, given short reader attention.
- Skimmable: eliminate blocks of copy, break content into short sections, and use bolded points and headlines so a reader can scan and self-identify (e.g., bolding '12-14g protein', 'zero sugar', 'gluten-free' so a gluten-free reader stops).
- Clear and concise: keep it short -- a headline, a few lines of body copy, a button, and a small supporting detail, rather than an essay.
- Engaging: choose a tone that either entertains (humor, playful framing) or educates with genuinely useful information.
- Use concrete stats and fun facts as engagement hooks where relevant (e.g., a stat about time spent somewhere, framed as a benefit) -- the source cites these as high-engagement devices.
- Write copy and design together, planning how each line will look in the email rather than writing text first and designing later.
Caveat: The 3-second attention claim is the source's framing, not a measured benchmark.
Caveat: Humor and stat-driven copy should fit brand voice and avoid unsupported claims.

Tags: email-lifecycle, retention, email-copywriting, copywriting, skimmability, engagement
Source: Complete Ecommerce Email Marketing Strategy For 2026.docx

---

## Replace paragraph copy with infographics that communicate value in seconds
Use when: Designing the education/benefit section of an email, or replacing a long benefits paragraph that isn't performing.
- Choose the infographic type by job: checklists for feature sets; icon graphics for calling out individual features; feature diagrams for what's inside the product; timelines for what a user feels over time (e.g., product effects); numbered lists for step sequences; comparison cards for 'us vs. them'; tables for structured specs; flowcharts to guide readers to the right product; graphs to visualize a stat instead of stating it.
- Show the product ingredients/components visually alongside short labels rather than writing them out in prose (the source points to supplement brands that show everything you get visually).
- Pair each infographic with minimal supporting copy (e.g., an ingredient name plus a one-line function such as 'reduces stress' / 'boosts focus').
- Combine copy and design rather than treating them separately -- the source's core claim is that copy alone won't be read.
- Treat the infographic as the education workhorse inside the standard email layout, placed after the hero/CTA and before the final product block.
Caveat: The source's claim that infographics are a 'cheat code' is an opinion based on his experience, not a controlled benchmark.
Caveat: Ingredient/benefit claims shown visually should still meet regulatory requirements for your category.

Tags: email-lifecycle, retention, email-design, infographics, visual-content, conversion-optimization
Source: Complete Ecommerce Email Marketing Strategy For 2026.docx

---

## Run plain-text vs long-form A/B tests on the same email
Use when: Optimizing a found er/community email where you're unsure whether short or longer copy converts better.
- Draft the short plain-text version first (e.g., a founder note with a PS and a CTA).
- Have the same idea rewritten as a longer, ~250-word email to use as the variation, keeping the core message and offer constant.
- Ensure both versions include a working CTA and link to the same destination so the test isolates length/format.
- Run the test and let results decide -- the source frames long-form as sometimes worse and sometimes workable, so treat it as a question to answer with your own data rather than a universal rule.
- Apply the winner to future sends in that pillar before testing additional variables.
Caveat: The source presents this as an example test, not a reported result.
Caveat: Long-form copy can still work in some cases; the source does not claim it always underperforms.

Tags: email-lifecycle, retention, experiment-design, ab-testing, email-copywriting, plain-text-email
Source: Complete Ecommerce Email Marketing Strategy For 2026.docx

---

## Use sender name (not subject line) as the primary open-rate lever
Use when: Writing subject lines and preview text and deciding how much testing budget to spend on them.
- Treat the subject line and preview text as the email's headline and sub-headline rather than as a standalone open-rate hack.
- Build sender recognition through the 3-4x/week cadence so the audience expects and recognizes your brand in the inbox.
- Write subject lines that create intrigue without revealing the full story (e.g., naming the benefit but not the mechanism, so the reader opens to find out 'why').
- Pair a curiosity-driven subject with preview text that builds on it and adds a concrete hook.
- Test subject lines where you have spare testing capacity, but do not assume large open-rate swings -- the source describes their effect as smaller than commonly believed (a stated opinion).
Caveat: This is a contested opinion; the source himself calls it 'controversial' and gives no measured data.
Caveat: Sender name effects still depend on deliverability and list familiarity.

Tags: email-lifecycle, retention, subject-lines, open-rate, deliverability, email-copywriting
Source: Complete Ecommerce Email Marketing Strategy For 2026.docx

---

## Keep segmentation light for broadcast campaigns
Use when: Deciding how much list segmentation effort to invest in your recurring broadcast program.
- Prioritize sending the right content mix and cadence to the engaged list over building complex segment logic.
- Use the engaged segment as the default audience for the 3-4x/week broadcast program.
- Note that this guidance is about manual/broadcast campaigns specifically; triggered lifecycle flows (cart abandonment, welcome series) are a separate, related discipline the source does not cover here.
- Revisit segmentation only when list data or deliverability problems point to a need, rather than as a first step.
Caveat: The source's stated scope is broadcast campaigns, not automated triggered flows.
Caveat: Light segmentation is the source's recommendation for this context and may not suit every list or deliverability situation.

Tags: email-lifecycle, retention, segmentation, broadcast-campaigns, list-health, email-strategy
Source: Complete Ecommerce Email Marketing Strategy For 2026.docx

---

## Reframe the 2024 Ecommerce Market Before Planning Funnel Spend
Use when: Deciding how to allocate budget and effort between cold ad acquisition and post-click email capture/retention for your store.
- Recognize the market shift the source describes: in 2020–2023 stimulus money and few competitors made impulse purchases easy, while in 2024 buyers have less disposable income, far more brand options, and prior bad/scam experiences online.
- Accept the practical implication: cold-traffic conversion rates hover around 1% or less, so paying repeatedly for cold retargeting rarely produces profit.
- Rebalance toward profit rather than top-line revenue: capture emails at the point of first site visit so you can convert warmed traffic cheaply instead of re-buying the same click.
- Keep paid ads for their real strength — acquiring attention and driving first/second visits — and use email for the conversion and follow-up work.
- Plan operations accordingly: you need the back end (flows, campaigns, list growth) built before scaling ad spend, or you will churn spend at roughly break-even.
Caveat: Market-evolution claims and 1% cold conversion figures are the presenter's observation, not measured benchmarks for your store; verify against your own analytics.
Caveat: This is a strategic reallocation argument, not a directive to cut ads.

Tags: email-lifecycle, acquisition, conversion-optimization, customer-research, unit-economics, positioning, measurement
Source: Ecommerce Email Marketing 2025.docx

---

## Build the 'Stand a Chance' Funnel: 10% Email Capture Instead of Paying to Retarget
Use when: Designing or auditing your site funnel to decide whether email capture is placed early enough to monetize cold ad traffic.
- Map your current funnel: ad click → site visit → purchase, and estimate how much of the traffic purchases versus leaves (the source describes ~1% purchasing and 99% leaving).
- Add a capture layer on the same traffic so at least a portion opts in — the source targets 10% of website traffic becoming email subscribers.
- Treat the opted-in segment as a cheap content channel: you can email them repeatedly at a fraction of a cent per send instead of paying for each retargeting impression.
- Scale the math to your traffic: the source's illustration is 50,000 monthly site viewers × 10% = 5,000 new subscribers per month, giving you a compounding list that no longer costs per-touch.
- Note the source's framing: a strong funnel does not guarantee winning, but a funnel without capture essentially guarantees churning ad spend.
Caveat: 10% opt-in and 1% purchase figures are the presenter's targets/illustrations, not universal benchmarks.
Caveat: Email revenue depends on the quality of content sent afterward, not just list size.

Tags: email-lifecycle, acquisition, conversion-optimization, list-growth, landing-page, unit-economics
Source: Ecommerce Email Marketing 2025.docx

---

## Use the Trust Threshold Model to Justify Content Over One-Shot Ads
Use when: Deciding how many touches and what mix of ads/email a product page visitor needs before you expect a purchase.
- Define your audience's trust threshold: the point where a shopper has seen enough information and repeated exposures to actually hand over money.
- Accept the source's claim: you cannot convert truly cold audiences in ecommerce — only audiences that know, like and trust you.
- Warm cold traffic by accumulating 'trust points' with content touches: ad impressions do this, but so do emails, and emails are cheap while impressions cost money each time.
- Where paid ads are the only touch, note the cost: brands relying solely on paid content often break even on the first order and depend entirely on back-end repeat purchases.
- So route a share of visitors into email (via pop-ups, opt-ins) so most of your content touches cost near zero and the same or higher conversion effect is achieved.
Caveat: The 'trust threshold' is a conceptual model, not a measurable number; do not invent a required exposure count.
Caveat: The source explicitly is not anti-ads — it positions ads as attention acquisition and email as conversion/content.

Tags: email-lifecycle, acquisition, customer-research, positioning, conversion-optimization, retention
Source: Ecommerce Email Marketing 2025.docx

---

## Win the Honeymoon Phase: Prioritize New Subscriber Capture
Use when: Deciding where to invest list-growth effort and how to sequence messaging for a newly opted-in shopper.
- Treat the window from opt-in through roughly the first or second purchase as the 'honeymoon phase', where the subscriber is most receptive to the brand.
- Recognize this is especially strong when the opt-in followed an ad click or an on-site visit, because intent is still top of mind.
- Prioritize capturing these fresh subscribers aggressively (pop-up, post-purchase checkbox) rather than relying on long-term list members who may have lost interest.
- Send high-value content and offers to new subscribers promptly while the honeymoon phase is active, since new-subscriber value is highest then.
- Keep serving long-term subscribers good content too, because interest decays and is only recovered through repeated useful sends.
- Treat 'new subscriber' as a distinct segment from 'past buyer' in your flows and campaign logic rather than mailing everyone the same thing.
Caveat: Honeymoon-phase value is the source's qualitative claim; measure your own new-subscriber revenue per contact.
Caveat: The point is prioritization, not a claim that existing subscribers have no value.

Tags: email-lifecycle, list-growth, retention, segmentation, welcome-flow, customer-research
Source: Ecommerce Email Marketing 2025.docx

---

## Deploy the Four List-Growth Methods and Know Their Roles
Use when: Setting up or auditing all the places your store can convert traffic into email subscribers.
- Install pop-up forms as the primary capture mechanism — the source targets a well-built pop-up converting around 10% of website traffic.
- Add a post-purchase opt-in checkbox (optionally pre-checked) so nearly every buyer lands on the list automatically.
- Create dedicated sign-up pages you can link from social, blog content, giveaways or other external properties.
- Add embedded sign-up forms on the homepage and footer with a clear incentive or reason to join.
- Sequence implementation roughly in that order of effectiveness: pop-ups first, then post-purchase, then sign-up pages, then embeds.
- Feed all four into the same flows and campaigns so no captured contact sits idle.
Caveat: Effectiveness ranking is the source's rough ordering; audit your own opt-in rates per method.
Caveat: Pop-up timing and design mistakes (see pop-up cards) can drag the 10% target well below 1–3%.

Tags: email-lifecycle, list-growth, conversion-optimization, pop-up, checkout, landing-page
Source: Ecommerce Email Marketing 2025.docx

---

## Balance Flows vs Campaigns at ~50/50 of Email Revenue
Use when: Auditing whether your automated email revenue is carrying its fair share or whether you are over-relying on manual sends.
- Set up the core flows every ecommerce brand needs with action-based triggers, described by the source as: welcome (joins list), website abandonment (visits and leaves), browse abandonment (views product and leaves), cart abandonment (adds to cart and leaves), checkout abandonment (reaches checkout and leaves), post-purchase, and win-back (no purchase in 60 days).
- Confirm each trigger is configured with the correct conditions/filters so it fires on the intended behavior rather than every visitor.
- Measure the split between flow revenue and campaign revenue; aim for the source's healthy band of roughly 40/60 to 60/40.
- If flows come in around 30% versus 70% campaigns, treat that as a signal there is substantial room to improve automations.
- Use well-built flows to relieve pressure on campaigns — automated revenue means you don't have to compensate for a slow month with a burst of manual sends.
- Use flows to capture high-intent abandonment and personalize post-purchase content around the specific item bought.
Caveat: The 50/50 and 40–60% bands are the source's heuristics, not a calculated formula for your store.
Caveat: Win-back timing of 60 days is the source's suggested default; adjust to your purchase cycle.

Tags: email-lifecycle, flows, abandoned-cart, welcome-flow, post-purchase, retention, measurement
Source: Ecommerce Email Marketing 2025.docx

---

## Run 3–4 Non-Discount Campaigns Weekly Using Microtopics
Use when: Planning weekly campaign content when your list is over-exposed to sales and you need to maintain open attention without heavy discounting.
- Commit to a cadence of three to four campaigns per week — the source's tested rhythm for best conversion across audiences.
- Make each email cover one microtopic (a single benefit, one ingredient, one feature, myth vs fact, a single customer review) rather than a comprehensive article that overwhelms readers.
- Avoid 'needy' buyer-focused content that only says buy/discount/exclusive/gone-forever; instead use value content like tips and tricks, a founder message, favorite picks, or industry watch-outs.
- Use the source's list of non-discount campaign angles as a library: single benefit, single feature, FAQ, what's inside, how it's made, how to use, back in stock, myth vs fact, brand progress update, customer transformation, treat yourself, tips and tricks, throwback content, staff picks, early access.
- Cycle through topics so you don't repeat the same angle; sending 3–4 per week from the library yields months of content.
- Frame non-discount sends as altruistic — present product and information and let buyers choose — which avoids burning out your discounts and positions you as a sought-after brand rather than a begging one.
- Keep sales pitches as the minority so discounts retain their power.
Caveat: The 3–4/week cadence is the source's tested recommendation for its client base; adjust to your audience's tolerance and measure unsubscribes.
Caveat: The 'don't sell' framing is the presenter's opinion on brand positioning, not a universal rule — transactional lists may still need more offer-led content.

Tags: email-lifecycle, campaigns, content-strategy, retention, positioning, deliverability, customer-research
Source: Ecommerce Email Marketing 2025.docx

---

## Build a Monthly Campaign Calendar from Key Dates Outward
Use when: Creating next month's editorial/email calendar so campaigns are planned in advance rather than ad hoc.
- Open a blank calendar for the upcoming month and mark the important fixed dates: scheduled sales, product launches and holidays.
- For each major event, add supplementary emails around it — the source's example is a sale launching on the 10th with a reminder on the 12th and a closer on the 14th.
- For a product launch, add supporting emails such as a teaser ahead of the launch.
- Once the anchor events and their supporting sends are placed, fill all remaining gaps with microtopic campaigns so you land at three to four sends per week.
- Draw the filler topics from your non-discount campaign library (single benefit, FAQ, how-it's-made, customer transformation, etc.).
- Repeat monthly so content planning is systematic rather than reactive.
Caveat: The example dates and per-event supplement counts are illustrative; scale supplementary touches to event size.
Caveat: Calendar density should be validated against your engagement metrics.

Tags: email-lifecycle, campaigns, content-strategy, planning, retention
Source: Ecommerce Email Marketing 2025.docx

---

## Diagnose the 9 Common Pop-Up Mistakes Killing Cost Per Acquisition
Use when: Auditing an existing pop-up that is converting below target before redesigning it or testing offers.
- Check the offer first — it is the most important element; 'sign up for updates' is not an offer. If no discount, use a giveaway, guide or similar value.
- Remove extra requests: ask only for email on screen one; request SMS or other fields only after the email submit.
- Set the fire delay around 4–12 seconds — not instant (harms experience) and not ~30 seconds (too few people see it).
- Fix load speed by compressing images (the source recommends tinypng.com for shrinking large files) and avoiding images on mobile and heavy files generally, so the form doesn't lag in.
- Enlarge the form — the source's guidance is roughly 75% of the screen on desktop and as much of the mobile screen as possible, since bigger forms tested better.
- Cut copy to the essential: remove implied lines like 'exclusive offers and promotions'; keep only the concrete offer (e.g., '10% off your first order').
- Simplify visuals — reduce colors, fonts, images and competing headlines; plain, minimal styling can outperform busy designs.
- Make the offer unmistakable and large; shoppers decide in roughly half a second whether to submit or exit.
- Defeat the reflexive close: shoppers automatically hit the top-right X, so move the close control (e.g., lower in the form, a separate in-form button, or another corner) to force a look at the offer.
Caveat: Close-button repositioning, size targets and delay ranges are the source's tested preferences; verify they don't increase bounce on your site.
Caveat: Compression tooling and platform interfaces change — confirm current options in your provider.

Tags: email-lifecycle, pop-up, conversion-optimization, list-growth, experiment-design, landing-page
Source: Ecommerce Email Marketing 2025.docx

---

## Choose the Right Pop-Up Offer Based on Average Order Value
Use when: Selecting or testing the incentive on your pop-up when opt-in rate is low or you are setting up a new form.
- Test whether the offer passes the source's filter: would you personally trade your email for it?
- If AOV is under $100, use percentage-off framing (at $50 AOV, '10% off' reads better than '$5 off').
- If AOV is over $100, switch to dollar-off framing — the source's example: on a $500 AOV, '5% off' sounds weak while '$25 off' performs better; dollar-off tested better in their experience.
- If discounting hurts margins, choose a creative alternative: monthly giveaway entry, free guide, free gift with order, free shipping (give away even if you already offer it), early access to deals, or a 'mystery discount' framing.
- Whatever you pick, make it explicit and prominent — vague 'early access' or hidden offers cause exits.
- Then run offer tests and evaluate trade-offs: compare opt-in rates for e.g. $10 off vs $15 off against the margin cost of the larger discount to judge whether the extra signups justify it.
Caveat: The $100 AOV threshold for dollar-vs-percentage framing is the source's tested heuristic, not a universal rule.
Caveat: Deeper discounts can improve opt-in rate while eroding margin — judge by total downstream value, not opt-in rate alone.

Tags: email-lifecycle, pop-up, offer-design, pricing, list-growth, experiment-design
Source: Ecommerce Email Marketing 2025.docx

---

## Run the 5-Step Pop-Up Build Process and a 7-Test Roadmap
Use when: Standing up a new pop-up program or optimizing an existing form toward 8–12% opt-in.
- Step 1 — Establish the offer (single offer to start) guided by margin and opt-in performance.
- Step 2 — Choose the form type. The source names five starting points; the recommended first tries are the 'classic' (straight to email, clear offer, no extra fields) and the 'micro-commit' (an extra step before the form, e.g. 'Do you want 10% off?'), then test the others against your audience.
- Step 3 — Create the form in your email platform (the source demonstrates Klaviyo and Amped) following the offer and design rules.
- Step 4 — Run the form through a pre-launch checklist covering the common mistakes before pushing live.
- Step 5 — Set up AB tests, monitor results, and iterate: expect opt-in to move up and down across many variants before reaching the target.
- Use the source's progress pattern as realistic: 2.5% → 3.3% → 4.1% → 3.7% etc., reaching around 10% only through continued testing (their example took roughly a fifth or sixth form iteration).
- Treat plug-and-play templates as a starting point that is usually left under-optimized; sustained testing is what produces the gains.
Caveat: 8–12% is the source's target range, and the client reaching ~10% is a case example, not a promise.
Caveat: AB testing requires sufficient traffic to reach conclusions; avoid calling winners on tiny samples.

Tags: email-lifecycle, pop-up, experiment-design, conversion-optimization, list-growth, measurement, klaviyo
Source: Ecommerce Email Marketing 2025.docx

---

## Design the offer before you design the popup
Use when: You are planning a list-growth popup (email/SMS capture) and need to decide what incentive to put behind it before building anything.
- Write out the actual offer you will give in exchange for the email, and make it concrete and valuable ('here is 10% off your order') rather than vague or insider-ish ('sign up for early access').
- Test whether you are genuinely willing to deliver that offer to every subscriber — if you are not, pick a different incentive such as free shipping, a dollar amount off, or a free guide.
- Only after the offer is set, choose the form type to test: the source's recommended starters are the classic form (straight to email address) and the micro-commit form (a yes/no question before the email field).
- Run classic and micro-commit head to head as your first test before adding complexity such as quizzes or gamified forms.
- When comparing offers, don't judge only by opt-in rate — check what happens to conversion once those subscribers are on the list, since that is the outcome that matters.
Caveat: Source opinion, not a universal law: strong offers beat weak ones, but the source also says copy matters less than the offer.
Caveat: Platform pricing and template availability change; verify the current interface.

Tags: email-lifecycle, popup-forms, offer-design, list-growth, conversion-optimization, experiment-design
Source: Ecommerce Email Marketing 2025.docx

---

## Micro-commit popups: ask a yes/no question before requesting the email
Use when: You are building a capture popup and want a low-effort form variant to test against a straight-to-email classic form.
- Build a first step that asks a single yes/no question tied to the offer, e.g. 'Do you want 10% off your first order?' with buttons like 'Yes please' and 'No thanks'.
- Configure the affirmative button action to advance to the next step in the form rather than submitting, so the email field appears only after the click.
- Reuse the same visual styling across steps (clone the step in your form builder) so the design stays consistent and you don't rebuild formatting.
- In the second step, restate the offer and take the email input; keep to one input per step.
- Test this against the classic version. The source's rationale is consistency bias — once someone clicks, they are more likely to finish.
Caveat: 'Works better in a lot of scenarios' is the source's claim from practice, not a documented benchmark; results depend on audience.
Caveat: Adds a click before capture, so measure total subscribers, not just conversion rate.

Tags: email-lifecycle, popup-forms, micro-commit, list-growth, conversion-optimization, experiment-design
Source: Ecommerce Email Marketing 2025.docx

---

## Quiz and gamified popups as alternative capture formats
Use when: You have already tested classic and micro-commit popups and want additional capture formats, or you need customer preference data for future segmentation.
- For a quiz form: ask a question that tells you something useful about the shopper (e.g. which problem they are trying to solve), then present the discount as the earned reward in exchange for that answer.
- Tag respondents by their answer in your ESP so you can send segment-specific follow-up emails later.
- For a spin-to-win or reveal-the-discount form: make the interaction reveal the reward, then gate claiming it with the email address; the source notes spin-to-win typically lands on the top prize.
- Try these formats periodically or rotate them rather than making them your permanent default if your brand positioning depends on a premium look.
- Compare formats by opt-in rate and downstream purchase conversion, and remember gamified formats may attract discount-motivated subscribers.
Caveat: Source's view: spin-to-win 'converts like crazy' but makes the brand look cheap — a positioning trade-off, not a universal recommendation.
Caveat: Quiz tools and gamified templates vary by platform; verify which templates your provider currently supports.

Tags: email-lifecycle, popup-forms, quiz-forms, segmentation, list-growth, brand-positioning
Source: Ecommerce Email Marketing 2025.docx

---

## Hide the X and force a claim-or-decline decision
Use when: You are designing a popup whose current form is being reflex-closed in the top corner without the offer being read.
- Reduce the X icon's visibility (e.g. set its opacity to zero) so the offer is the first thing read.
- Add your own secondary button beneath the primary claim button with copy such as 'No thanks, close form' so the shopper can still exit deliberately.
- Style the decline button to be visually quiet — blank background, readable text — so it does not compete with the offer.
- Keep the offer headline as the largest element on the form and reduce surrounding copy so it is unmistakably the focus.
- Keep the required legal SMS consent language small (source suggests roughly size 8) rather than letting it dominate the layout.
Caveat: Hiding the exit can frustrate shoppers; the source frames it as improving conversion but notes to keep an explicit decline path.
Caveat: Accessibility and platform policies may restrict or dislike hidden close controls — check your provider and local requirements.

Tags: email-lifecycle, popup-forms, conversion-optimization, form-design, experiment-design
Source: Ecommerce Email Marketing 2025.docx

---

## Mobile popup build: single-step capture with email then SMS as a separate step
Use when: You are configuring a mobile capture popup in your ESP and want a concrete layout order and settings to start from.
- Start from a multi-step email and SMS template, then clone it into a mobile-only form so mobile and desktop data can be analyzed separately.
- Set targeting to display on mobile only so the same design is not distorted across devices.
- Step 1: email opt-in with the offer as the hero headline; Step 2: phone number for SMS; Step 3: a success message with the discount code and a 'start shopping' style button.
- Do not place email and SMS inputs on the same step — the source states this hurts conversion.
- In the success step, tell SMS subscribers to confirm on their device and mention that anyone who skips SMS still enters the email welcome flow, so email subscribers are not lost.
- Check the success step has a working close/continue button since the X may be hidden.
Caveat: Different ESPs name steps and templates differently; tutorial videos referenced in the source may be outdated.
Caveat: The source's recommended form dimensions (roughly 750x500 on mobile) are a starting point for testing, not a proven optimum.

Tags: email-lifecycle, popup-forms, mobile, form-design, sms, list-growth
Source: Ecommerce Email Marketing 2025.docx

---

## Desktop popup design: go bigger, use a side image, keep one offer
Use when: You are designing the desktop version of a capture popup and deciding on size, layout and imagery.
- Clone your mobile form into a desktop-only version, then set targeting to display on desktop only.
- Use a popup (or a larger custom size) rather than a fly-out, since the source reports fly-outs as less effective.
- Use a product or lifestyle image on one side of the form. The source says 'right image' was tested as working best, but recommends testing left, right and no image.
- Compress any image before uploading to avoid a slow-loading form.
- Verify the layout holds after swapping images, since uploads can reset sizing and formatting.
- Ask whether you are willing to trade some browsing experience for a more prominent form; source says bigger forms generally convert better but are more intrusive.
Caveat: 'Right image works best' is the source's testing experience, not a universal rule — test it.
Caveat: Large popups can increase bounce for shoppers mid-browse; consider timing and frequency alongside size.

Tags: email-lifecycle, popup-forms, desktop, form-design, creative-strategy, conversion-optimization
Source: Ecommerce Email Marketing 2025.docx

---

## Form targeting: delay, frequency and avoiding exit-intent
Use when: You are setting the trigger and frequency rules for a popup and deciding when it appears and re-appears.
- Do not show the form immediately on load; the source recommends against it.
- Set the trigger to a time-on-page delay rather than exit intent, which the source says misfires and isn't very good.
- Start with a 4-second delay and test upward toward 12 seconds.
- Set a frequency rule so that after someone closes the form, it does not reappear for several days — the source uses about 5 days as an example.
- Restrict the form to the device type it was designed for (mobile-only or desktop-only) so each version's data stays clean.
- Advance the delay gradually and compare total submits, not just conversion rate, when choosing a final value.
Caveat: Time delay and frequency values are the source's starting heuristics; the right values depend on traffic volume, page speed and audience.
Caveat: Some platforms offer scroll-depth and page-count triggers as alternatives the source did not recommend over a time delay.

Tags: email-lifecycle, popup-forms, targeting, experiment-design, form-design
Source: Ecommerce Email Marketing 2025.docx

---

## Popup form QA checklist before launch
Use when: You have built a popup and are about to publish it; use this to catch obvious issues before sending traffic.
- Confirm only one input is requested per step — never email and SMS together.
- Confirm the time delay sits in the roughly 4-12 second range.
- Confirm the form loads instantly with no lag when it fires.
- Confirm the form covers at least about 75% of the screen so the offer is not easily ignored.
- Trim body copy to under about 10 words on the form.
- Confirm the offer itself is the largest visual element.
- Confirm there is no visible dismissive X, or replace it with a close-form button / an unclear X placement so the shopper makes a decision.
- Verify close functionality works on every step, including the success step, so users are not trapped.
Caveat: The source presents these as a strong starting checklist for testing, not a guarantee of performance; a strong offer can compensate for one missed item.
Caveat: 'Covers 75% of screen' and 'under 10 words' are the source's heuristics, not measured benchmarks.

Tags: email-lifecycle, popup-forms, quality-assurance, conversion-optimization, form-design
Source: Ecommerce Email Marketing 2025.docx

---

## Seven A/B tests to run on popup forms, in rough priority order
Use when: You have a live popup form and need a testing backlog ordered by likely impact on subscriber volume and revenue.
- Offer first (highest leverage): test 10% off versus $10 off versus free shipping versus a free guide, and include a mystery-offer variant; evaluate both opt-in rate and post-opt-in purchase conversion.
- Form type second: test popup versus full-page versus fly-out, and test variations within your chosen type.
- Close functionality third: test a close-form button versus an X, and test where the close control sits.
- Time delay fourth: compare 4 seconds versus 12 seconds. Judge by total submits, not conversion rate — a 30-second delay may show a higher conversion rate but far fewer total subscribers because few visitors stay that long.
- Image content fifth: test different photos and placements; on mobile consider whether an image belongs as the form background.
- Copy sixth: test longer versus shorter copy and different phrasing ('unlock my offer' versus 'you've got 10% off').
- Colors last: simpler color palettes tend to produce better opt-ins than busy ones.
Caveat: The source recommends running a test every couple of days; that cadence requires enough traffic to reach a read.
Caveat: The illustrative comparison (3% to 4% opt-in on 10,000 visitors equals roughly 100 extra subscribers a month) is arithmetic, not a performance promise.

Tags: email-lifecycle, popup-forms, experiment-design, offer-design, conversion-optimization, measurement
Source: Ecommerce Email Marketing 2025.docx

---

## Popup platform choice: built-in ESP forms versus a specialist tool
Use when: You are deciding whether to build capture forms inside your email platform or subscribe to a dedicated popup tool.
- If your ESP is also your email sender, start with its native form builder and templates, then realistically customize them for ecommerce rather than using the default template as-is.
- If popups are a meaningful growth channel and budget allows, evaluate a dedicated popup platform (the source cites one at roughly $100/month) and compare opt-in performance against your current forms.
- When evaluating a specialist vendor, ask whether they will build your first forms for you as part of onboarding, and confirm what the editor can customize.
- Inside a specialist editor, expect to edit copy, images and each step separately; formatting may need manual padding/spacing fixes per device view.
- Set targeting (e.g. anonymous visitors) and a time-on-page trigger such as 4 seconds, then preview locally and on your live site before publishing.
- Confirm any discount code referenced in the form is created in your store, or the form may fail to deliver the incentive.
Caveat: Pricing, free tiers and editor features change frequently — verify current pricing and interface before committing.
Caveat: The source states it has seen strong ROI from the specialist platform but does not provide a verified benchmark; treat this as testimonial, not proof.

Tags: email-lifecycle, popup-forms, email-platform, tooling, list-growth, conversion-optimization
Source: Ecommerce Email Marketing 2025.docx

---

## Flows versus campaigns: what each is for and how to split revenue
Use when: You are planning your email program structure and deciding how much revenue to expect from automated sequences versus one-off sends.
- Define flows as sequences triggered by a specific shopper action (site visit, product view, add to cart, checkout start, purchase, long lapsed purchase); once activated they fire automatically for every qualifying shopper.
- Define campaigns as manually created, manually sent emails to your list.
- Set up flow triggers through your ecommerce platform integration so events (cart abandonment, purchase) fire the sequence automatically.
- Aim for a rough balance — the source suggests targeting roughly 50% of revenue from flows and 50% from campaigns.
- Prioritize personalization: different customers are at different journey stages and should receive different information, which is the core advantage of flows over blasts.
- Treat this as ongoing work: flows need updating as brand, trends and customer base change.
Caveat: The 50/50 split is the source's heuristic, not a calculation derived from data presented here.
Caveat: Any revenue contribution figures quoted by the source are testimonials from its own client work, not forecasts for your store.

Tags: email-lifecycle, automation-flows, campaigns, segmentation, retention, measurement
Source: Ecommerce Email Marketing 2025.docx

---

## The six baseline flows to build first, in order
Use when: You are deciding which automated email flows to build or fix next, and whether to invest in advanced segmentation or upsell logic.
- Welcome flow: 8 emails for new subscribers.
- Site abandon flow: 1 email for someone who visited the site and left without deeper action.
- Browse abandon flow: 5 emails for someone who viewed a product and left.
- Cart abandon flow: 6-8 emails for someone who added to cart and left.
- Checkout abandon flow: 6-8 emails for someone who started checkout and left.
- Post-purchase flow: sequence after a purchase.
- Win-back flow: for customers who purchased months ago and have gone quiet.
- Audit your existing flows against these basics before adding advanced cross-sell, upsell or split tests — the source describes a case where a brand wanted advanced automations while the welcome flow was a single email and cart abandonment was not set up correctly.
Caveat: Email counts per flow are the source's recommended structure; your optimal counts depend on catalog, price point and purchase frequency.
Caveat: The described revenue improvement for one brand (roughly $45k to $133k in a month after fixing basics) is a case example, not a promised result.

Tags: email-lifecycle, automation-flows, abandoned-cart, welcome-flow, win-back, retention
Source: Ecommerce Email Marketing 2025.docx

---

## Build flows in a mobile-first multi-step pattern you can clone across devices
Use when: You are implementing capture forms across device types and want a repeatable build process rather than two independent designs.
- Build the mobile version first with the step sequence you want (micro-commit, email, SMS, success), then clone the form and convert the clone to desktop-only.
- Set display rules per clone so mobile and desktop data are analyzed separately rather than as one blended report.
- Ask your SMS platform how phone numbers collected in your ESP form flow into their system — the source notes SMS may live on a separate platform.
- If you want a micro-commit variant, clone the form again and move the new question step to the front, deleting the email field from that step.
- In a specialized popup platform, customize each step's copy and imagery individually, and check that padding and layout are re-applied after any image swap.
- Preview both versions before publishing and confirm each step's button actions are correct (advance step versus submit form).
Caveat: SMS and ESP integration specifics vary widely by platform and country regulations; verify consent language requirements.
Caveat: Tutorials referenced in the source may not match current platform interfaces.

Tags: email-lifecycle, popup-forms, mobile, email-platform, sms, form-design
Source: Ecommerce Email Marketing 2025.docx

---

## Prioritize core lifecycle flows over advanced segmentation
Use when: Planning your store's email lifecycle roadmap or deciding where to invest automation effort first.
- Adopt the seven core flows as your baseline stack: welcome (8 emails), site abandon (1 email), browse abandon (5 emails), cart abandon (6-8 emails), checkout abandon (6-8 emails), post-purchase (3+ emails) and win-back (3 emails).
- Resist the urge to build complex hypersegmentation first — per the source, advanced segmentation 'takes a lot of effort for not as many results' as nailing the basics.
- Treat the email counts and delays below as starting templates, not proven optima; the source explicitly says every brand must test.
- Set each flow to fire on its own distinct trigger and use exit filters so a customer moves through the funnel rather than receiving overlapping flows.
- After launch, move improvement effort into campaign testing (see the campaign-as-testing-ground card) rather than endless flow surgery.
Caveat: The flow counts and delays are the presenter's base outlines for 7-8 figure brands, not universal benchmarks — you must test per account.

Tags: email-lifecycle, flow-setup, automation, retention, prioritization
Source: Ecommerce Email Marketing 2025.docx

---

## Welcome flow: 8-email structure with exit filter
Use when: Setting up the new-subscriber welcome automation after your popup/form captures an email.
- Trigger on someone joining your email list; add a filter that exits anyone who makes a purchase (0 purchases since starting the flow) so buyers don't keep receiving discount prompts and instead enter the post-purchase flow.
- Email 1: strong introduction — deliver the welcome discount at the top of the email (not buried), plus USPs, light social proof and best sellers; keep it condensed.
- Email 2: brand background — founding story, face to the name, team photo, and sprinkle social proof into the story.
- Email 3: highlight best sellers and why they're good, reminding of the discount.
- Email 4: urgency — discount is expiring soon, add risk reversals (guarantees, shipping promise) and testimonials.
- Email 5: us-versus-them — clearly list why you differ from competitors the subscriber is likely also evaluating.
- Email 6: heavy social proof — brand testimonials and any media features.
- Email 7: last chance, kept super simple and aggressive.
- Email 8: note from the founder — check in, offer support via reply, and offer an extended discount (source says this email usually does well).
- Use 1-2 day delays between emails (source sometimes uses 2-3 days); remind recipients of the discount in every email.
Caveat: Source acknowledges discomfort with discounting first purchase but argues list value repays it; that is an opinion, not measured proof.
Caveat: Offer the founder a real reply channel only if you can handle responses.

Tags: email-lifecycle, welcome-flow, automation, offer-design, discount-strategy
Source: Ecommerce Email Marketing 2025.docx

---

## Welcome flow's two acceptable outcomes
Use when: Setting success metrics and email content priorities for the welcome automation.
- Outcome A: convert subscribers who would otherwise have left, using a strong popup form plus a welcome flow that addresses objections as they arrive.
- Outcome B: if they don't buy, treat the flow as objection-priming — deliver the information needed so that when the need arises, campaigns convert without fresh objection handling.
- Keep every email discount-visible so both outcomes retain the incentive thread.
- After the flow completes, move non-buyers into the regular campaign list rather than leaving them in the automation.
Caveat: Outcome B is hard to measure directly; treat it as a content-hygiene principle rather than an attribution claim.

Tags: email-lifecycle, welcome-flow, objection-handling, measurement, retention
Source: Ecommerce Email Marketing 2025.docx

---

## Site abandon flow: one-email nudge to keep browsing
Use when: Adding a recovery flow for visitors who hit your homepage or category pages and leave without viewing a product.
- Trigger on 'active on site' (the source uses Klaviyo/Shopify); exit anyone who views a product, adds to cart, reaches checkout, or purchases, so they enter the deeper flows instead.
- Add a suppression so a visitor can't receive this flow more than once in 30 days.
- Wait 2-4 hours before sending; the source found this window best but says to test it.
- Send one email: 'Do you need some help?' — remind them to keep shopping and surface best sellers, a few categories, and light social proof.
- Keep the email deliberately simple — don't overload it; the goal is to push them deeper into the funnel, not to sell a specific item.
Caveat: Site-visit frequency is low per visitor, so send consistency matters more than frequency here.
Caveat: An exit-filter misconfiguration can cause visitors to receive this alongside deeper abandon flows.

Tags: email-lifecycle, abandoned-cart, site-abandon, automation, re-engagement
Source: Ecommerce Email Marketing 2025.docx

---

## Browse abandon flow: 5-email recap that escalates slowly
Use when: Building the browse-abandonment automation for shoppers who viewed a PDP but didn't add to cart.
- Trigger on viewed product; exit anyone who adds to cart, starts checkout, or purchases; suppress repeat entrants for 30 days.
- Wait 45 minutes before the first email (source says test the interval). Email 1 shows the exact product they viewed via dynamic content (e.g., Klaviyo's dynamic block) with a simple reminder.
- Email 2 (1-2 days later): brand info and risk reversals, plus other products they can shop — the objection is buy-in on the brand.
- Email 3: testimonials and social proof on the viewed item, with dynamic content showing what they abandoned.
- Email 4: introduce a discount only after the free options — the source deliberately delays discounting to protect margins — framed as a 48-hour flash.
- Email 5: short closer, 'expires in 24 hours', discount reminder.
- Keep emails very simple and use dynamic blocks in each email so the visitor sees their actual product.
Caveat: Do not wait a week — source says this is too long while attention is fresh.
Caveat: Discount timing is a margin trade-off, not a proven revenue lift for your account; test.

Tags: email-lifecycle, browse-abandon, cart-recovery, automation, dynamic-content
Source: Ecommerce Email Marketing 2025.docx

---

## Cart abandon and checkout abandon are two separate flows
Use when: Auditing or building cart and checkout recovery automations.
- Recognize the difference: adding to cart is a different event from entering the payment/shipping checkout page, so each needs its own flow.
- Cart abandon trigger: added to cart; exit filters should include 'placed order 0 times' and 'checkout started' so anyone further down the funnel enters checkout abandon instead.
- Checkout abandon triggers on checkout start with its own exit filter on purchase.
- Reuse the same email content across both flows — the source uses identical content with different triggers.
- Source claims roughly 90% of brands audited lack a proper cart-abandon flow; verify your platform actually fires an abandoned-cart trigger (the source says Klaviyo added it via Shopify integration around September 2024) or build a custom trigger.
- Run 6-8 emails; first email ~30 minutes after the trigger (source's recommendation, test it), then 1-2 day gaps.
Caveat: Platform trigger availability changes — verify the current interface and event names in your platform before assuming it exists.

Tags: email-lifecycle, abandoned-cart, checkout, automation, flow-setup
Source: Ecommerce Email Marketing 2025.docx

---

## Cart/checkout abandon content sequence
Use when: Writing the emails inside cart-abandon and checkout-abandon flows.
- Email 1: simple reminder of the abandoned product with a shop-now CTA and dynamic block showing the item.
- Email 2: text-based nudge from the founder — informal, personal, 'you left something behind'.
- Email 3: brand USPs and why to choose you over other stores the shopper is likely comparing.
- Email 4: customer testimonials plus dynamic abandoned content.
- Email 5: last-chance urgency — 'your order is expiring, we can't hold it much longer'.
- Branch the final email: returning buyers get a founder check-in with support offer, no discount; first-time buyers get a discount opener (e.g., '15% off if you buy within 48 hours') followed by a founder 'everything okay?' discount closer.
- Place the dynamic abandoned-product block at the top of every email and add cross-sell recommendations at the bottom.
Caveat: The 15% / 48-hour figures are examples from the source, not calibrated thresholds for your store.
Caveat: Discounting checkout abandoners can train customers to abandon deliberately — consider testing versus a no-discount branch.

Tags: email-lifecycle, abandoned-cart, checkout, discount-strategy, cart-recovery
Source: Ecommerce Email Marketing 2025.docx

---

## Post-purchase flow: 3 emails that thank, bond, and enable
Use when: Building the automation that fires immediately after an order is placed.
- Trigger on order placed with no exit filter — everyone should receive it.
- Email 1, sent immediately: text-based thank-you from the founder using the customer's first name, tying the order to your mission, offering support by reply, and including a PS add-to-order offer within 24 hours — the source calls this an immediate big purchase window.
- Email 2, ~2 days later: invite them to your main social channel or community group to grow your owned audience.
- Email 3, ~3 days later: 'how to get the most from your product' — usage tips, routines, pairing suggestions that naturally set up the upsell, plus a recommended-products block based on customer activity.
- Keep it to about three emails; the source says four-plus is optional and three is fine.
Caveat: The add-to-order offer window depends on your fulfillment speed; if orders ship same-day, combine the add-on offer into the order confirmation instead.

Tags: email-lifecycle, post-purchase, retention, upsell, community
Source: Ecommerce Email Marketing 2025.docx

---

## Win-back flow: fire at double the average repurchase interval
Use when: Setting up reactivation automation for customers who bought months ago.
- Set the trigger based on elapsed time since last order — if average time between purchases is ~45 days, fire at ~90 days (source's rule of thumb: double the interval), or use 60/90/120 days.
- Exit anyone who makes a purchase after entering the flow.
- Email 1: 'it's been a while' brand reminder with a comeback nudge and a dynamic recommendation based on the customer's last purchase.
- Email 2 (about a week later): a unique, dynamically generated discount code per customer — the source says personalized codes convert better.
- Email 3: text-based last-chance from the founder, warm and understanding, restating the expiring discount.
- Keep the flow simple; the source argues most repeat purchases come from regular campaigns (3-4 sends per week), not the win-back flow, so treat it partly as customer experience.
Caveat: The double-the-interval rule is a heuristic, not a measured formula, and only works if you have a reliable average repurchase interval.
Caveat: Source's claim that ~99% of retention/repeat revenue comes from campaigns is the presenter's assertion, not a verified benchmark for your list.

Tags: email-lifecycle, win-back, retention, re-engagement, ltv
Source: Ecommerce Email Marketing 2025.docx

---

## Use campaigns as the testing ground for flow content
Use when: Deciding how to optimize lifecycle emails when flow testing is slow and hard to track.
- Send 3-4 email campaigns per week (minimum 2) so you get fast, 24-hour data on angles and subject lines.
- Track campaign performance; when an email wins, add its angle to the relevant flow: educational product-creation emails to the welcome flow (with discount added), usage-tip emails to the post-purchase flow, return-policy emails to the cart-abandon flow for risk reversal.
- Avoid maintaining dozens of simultaneous active tests across triggers — the source says flows are hard to monitor at scale and need spreadsheets to track.
- Only accept flow-specific test results when the sample is meaningful; wait for customer entry volume before judging a flow variant.
- Document what went into which flow so you don't re-test identical angles repeatedly.
Caveat: Campaign and flow audiences behave differently, so a campaign winner is a strong hypothesis, not a guaranteed flow winner.

Tags: email-lifecycle, experiment-design, measurement, content-strategy, flow-optimization
Source: Ecommerce Email Marketing 2025.docx

---

## Test flow time delays before content
Use when: Choosing and tuning send delays for site, browse, cart and checkout abandon flows.
- Pick one abandonment flow and test two delays for the first email — e.g., the source compared 30 minutes versus 4 hours for a website-abandon flow.
- Evaluate on placed-order rate, not just opens: in the source's example, the 30-minute delay got better open and click rates, but the 4-hour delay produced a much higher placed-order rate on a large sample.
- Do not assume faster is always better — the source explicitly says the placed-order result favored waiting longer in that case.
- Apply findings per flow, since attention windows differ (browse: 45 minutes recommended; cart: ~30 minutes; site: 2-4 hours; win-back: weeks).
- Re-test delays as your list and traffic composition change.
Caveat: The 30-minute versus 4-hour comparison is one case study; the source calls it a large sample but it does not establish a universal best delay.

Tags: email-lifecycle, experiment-design, timing, abandoned-cart, measurement
Source: Ecommerce Email Marketing 2025.docx

---

## Long-form versus short-form flow emails
Use when: Deciding email length and content depth in abandonment flows and campaigns.
- Test a long email that explicitly works through objections against a short one that just says 'you left this behind, shop now'.
- In the source's comparison on ~2,000 recipients, the short email achieved a 0.2% placed-order rate and 2.4% click rate versus better performance for the quick reminder — use this as a hypothesis, not a rule.
- Reason about intent: some abandoners need their objections talked through, while others have no objections and only need a reminder — segment or sequence accordingly.
- Combine both in sequence where possible: short reminder first, longer objection-handling email later in the flow.
- Judge by placed-order rate, not click rate alone, since long educational emails can earn clicks without purchases.
Caveat: Single A/B example, not a universal result; the source stresses it must be tested per account.

Tags: email-lifecycle, experiment-design, copywriting, abandoned-cart, objection-handling
Source: Ecommerce Email Marketing 2025.docx

---

## Subject line and preview text tests to run
Use when: Running subject line experiments for campaigns or flow emails.
- Test including versus excluding discount mentions (e.g., 'sale').
- Test including versus excluding emojis in subject lines and preview text.
- Test ellipses ('...') versus plain endings.
- Test ALL CAPS versus sentence case.
- Test different urgency timeframes stated in the subject line.
- Remember the source's caveat: subject-line test learnings are hard to transfer to future emails because so much varies — use them for immediate improvement rather than building a permanent subject-line rulebook.
Caveat: High variability makes subject-line learnings less durable; expect to keep re-testing.

Tags: email-lifecycle, experiment-design, subject-lines, copywriting, measurement
Source: Ecommerce Email Marketing 2025.docx

---

## Graphic-heavy versus text-based email design
Use when: Choosing email format for flow emails such as founder nudges, thank-yous and last-chance messages.
- Build a plain-text-style email (little or no imagery) that reads as a personal message, e.g., a founder note sign-off.
- Compare it against your standard template with heavy graphics on open rate, click rate and revenue.
- In the source's example, the text-based founder email beat the graphic email on opens, clicks and revenue — treat this as a directional hypothesis for your list.
- Use text-based design preferentially for personal messages — founder notes, thank-yous, cart nudges, win-back last chances — and keep graphic design for product showcases and social proof blocks.
- Re-test when you see sales drops or list composition changes.
Caveat: Performance varies by account; the source explicitly says to test rather than assume text always wins.

Tags: email-lifecycle, creative-strategy, experiment-design, copywriting, design
Source: Ecommerce Email Marketing 2025.docx

---

## Promoting categories versus individual products in email
Use when: Deciding what to feature in campaign and flow email blocks, especially for higher-ticket catalogs.
- Create one variant featuring specific products ('shop this jacket') and one featuring categories ('shop jackets, shop pants').
- Measure clicks and revenue, not just clicks.
- In the source's higher-ticket store example, categories produced higher clicks and higher revenue, so they biased future emails toward category promotion.
- Default to individual products when the flow is abandonment-driven and you can show the exact abandoned item dynamically.
- Revisit the bias as catalog breadth and price points change.
Caveat: Single-store example; the source presents it as a tested bias, not a universal rule.

Tags: email-lifecycle, merchandising, experiment-design, campaigns, category-strategy
Source: Ecommerce Email Marketing 2025.docx

---

## Seed welcome-flow social proof with early testimonials
Use when: Writing welcome-flow emails when you have a new or small brand with little social proof.
- Place light social proof in email 1, woven into the founder story rather than isolated.
- Save the heavy-proof email (brand testimonials, media features) for email 6, after brand education and before the aggressive last-chance email.
- Use existing proof even if modest — the source suggests sprinkling review counts or media mentions into the story rather than waiting for large numbers.
- Add testimonials to the urgency email (email 4) for recipients still on the fence, and repeat proof inside browse/cart recovery emails for the exact item abandoned.
- Do not fabricate proof; if the brand is new, use founder credibility and risk reversal instead of numerical claims.
Caveat: The source does not prescribe a minimum review count — do not invent one.

Tags: email-lifecycle, welcome-flow, social-proof, objection-handling, content-strategy
Source: Ecommerce Email Marketing 2025.docx

---

## Founder-message emails and when they convert
Use when: Writing personal-voice emails for welcome close, cart abandon, post-purchase thanks or win-back final send.
- Use the founder (or a named person) as sender with the customer's first name in the body.
- Keep it short and text-based; the source says these perform well because recipients feel personally reached.
- Offer a real support channel: invite recipients to reply to the email with questions.
- In abandonment flows, use it as the second email or the last-chance email, offering support and occasionally extending the discount by a day.
- In post-purchase, use it immediately after order placed to convey mission and offer add-ons within 24 hours.
- Expect and prepare for support replies — the source notes these emails generate customer questions.
Caveat: Requires a real inbox and response process; unmonitored replies can hurt trust.
Caveat: Founder credibility must be genuine — do not invent a persona.

Tags: email-lifecycle, copywriting, founder-voice, abandoned-cart, retention
Source: Ecommerce Email Marketing 2025.docx

---

## Customize flows with dynamic product blocks
Use when: Building browse-abandon, cart-abandon, post-purchase and win-back emails in Klaviyo or a comparable platform.
- Add a dynamic block showing the abandoned product (image, name, price, link) at the top of browse and cart/checkout abandonment emails.
- Use the platform's product-recommendation blocks based on the customer's activity in post-purchase and win-back emails.
- Generate per-customer dynamic discount codes in win-back flows so each recipient feels their offer is unique — the source says these convert better.
- In welcome-flow examples, keep discount code visible throughout; a generic graphic won't reproduce that per-recipient effect.
- Verify the current name and setup of dynamic blocks in your platform, as interfaces change.
Caveat: Dynamic blocks depend on your catalog and event data being clean; missing product data produces blank or wrong recommendations.

Tags: email-lifecycle, dynamic-content, personalization, klaviyo, cart-recovery
Source: Ecommerce Email Marketing 2025.docx

---

## Run 3-4 email campaigns per week to carry retention
Use when: Planning weekly retention calendar and deciding how much to rely on automation versus broadcasts.
- Send 3-4 campaigns per week (the source treats two as the floor).
- Use these campaigns as your testing ground for angles that later get ported into flows.
- Keep the win-back flow simple because recipients are still receiving your regular campaigns.
- Expect most repeat purchases to come from campaigns — the source asserts around 99% of retention and repeat purchases, but treat this as the presenter's claim, not a measured figure for your list.
- Watch engagement and unsubscribes when scaling frequency; adjust if list health degrades.
Caveat: The 99% claim is an unverified assertion in the source; do not plan forecasts around it.

Tags: email-lifecycle, campaigns, retention, measurement, send-frequency
Source: Ecommerce Email Marketing 2025.docx

---

## Risk reversal and urgency placement in sequence
Use when: Ordering content in welcome, browse, cart and checkout abandonment sequences.
- In the welcome flow, deliver the incentive first, then USPs/product education, then social proof, then urgency ('discount expiring soon') with risk reversal (30-day guarantee, shipping promise), then heavy proof, then last chance.
- In browse abandon, keep email 1 as a pure reminder, put risk reversal in email 2, and put the discount in email 4 with a 48-hour framing.
- In cart/checkout abandon, keep the last chance email separate from the discount branch, giving returning buyers a no-discount founder note instead.
- In win-back, reserve the unique discount for email 2 and the last-chance founder note for email 3.
- Use short, specific urgency ('expires in 24 hours') rather than vague pressure.
Caveat: Aggressive urgency in the last email may cost list goodwill; the source recommends testing timing and tone.

Tags: email-lifecycle, offer-design, urgency, risk-reversal, sequencing
Source: Ecommerce Email Marketing 2025.docx

---

## Why the welcome flow exists: email as the cheap way across the trust threshold
Use when: Deciding how much budget and effort to put into the post-signup welcome flow versus buying more ad impressions.
- Start from the source's funnel math: only a small share of site traffic (he cites ~2%) is ready to buy on the first visit; the rest arrive with objections about brand legitimacy, product quality and price. Those objections cannot be answered by one ad, so buyers need repeated exposure — the source calls this crossing the 'trust threshold'.
- Recognise that the only other channel that reaches people daily at low marginal cost is email — the source cites 4B+ global email users, 90%+ of the US population checking email daily, and average $44 returned per $1 spent on email versus roughly $2 per $1 on paid ads. Treat those ratios as the source's cited industry averages, not guaranteed results.
- Apply to your store: for each objection on your PDP (does this work, is this brand real, is it worth the price), assign at least one email in the flow that answers it, so paid spend does not have to be repeated to convince the same person.
- Keep the objective in mind for measurement: the welcome flow's job is partly immediate conversion and partly priming future purchases, so judging it only by its own revenue understates its value.
Caveat: ROAS and percentage figures are the source's cited averages; your niche, price point and traffic source will differ.
Caveat: Email only works if you are actually capturing addresses — without a popup or lead magnet, the flow has nobody to send to.

Tags: email-lifecycle, acquisition, retention, welcome-flow, conversion-optimization, measurement, customer-research
Source: Ecommerce Email Marketing 2025.docx

---

## Set the welcome flow length and goal by price point and buying cycle
Use when: Scoping how many emails and how many days your welcome/onboarding flow should cover before you write it.
- Default to a 7-14 day window for a normal AOV store — the source's typical recommendation.
- If AOV is very high (he gives the example of a ~$5,000 product), extend the flow well beyond that, potentially over two months, because the buying decision itself takes longer.
- Define two outcomes you are designing for: (a) converting the curious signups who would otherwise bounce, and (b) priming future customers by addressing objections up front. Priming shows up later, e.g. the source claims a campaign sent to a primed list can produce a far larger revenue day ($75k vs $5k in his illustrative example) — treat that as illustration, not a benchmark.
- Plan the flow as separate, spread-out emails rather than a couple of dense ones, and pick an email count that matches the length of the consideration window.
Caveat: The 7-14 day range and two-month high-ticket example are the source's heuristics, not tested universals.
Caveat: The revenue comparison used to illustrate priming is an anecdote; do not promise it internally as a forecast.

Tags: email-lifecycle, welcome-flow, retention, offer-design, pricing, customer-research
Source: Ecommerce Email Marketing 2025.docx

---

## Split dense welcome emails into short, skimmable, spread-out messages
Use when: Auditing an existing welcome flow that crams brand story, bestsellers, FAQ and offer into 2-3 long emails.
- Accept the skim reality: the source states customers spend at most roughly 5-7 seconds on an email, so the whole flow's information cannot live in two walls of text.
- Keep body copy minimal — the source calls anything over about 100 words 'too much' for these emails. Use short headlines and one idea per email.
- Structure every email so the reader can get the point in about three seconds: clear headline, one supporting proof or claim, discount reminder if one exists, and a button.
- Place a button near the top of every email so nobody has to scroll to act, and repeat a button at the bottom for readers who reach the end.
- Assign one job per email across the sequence (intro + incentive, brand story, bestseller, offer reminder, us-vs-them, social proof, last chance, founder note) rather than duplicating everything everywhere.
Caveat: The 100-word and 5-7 second figures are the source's rules of thumb for ecommerce promo email, not formal research.
Caveat: Short emails do not mean skipping the offer reminder — the source specifically criticises welcome emails that never restate the discount.

Tags: email-lifecycle, welcome-flow, copywriting, conversion-optimization, product-page, creative-strategy
Source: Ecommerce Email Marketing 2025.docx

---

## Email 1: deliver the incentive and prove legitimacy in the first screen
Use when: Writing or rewriting the first email a new subscriber receives after opting in.
- Put the welcome and the discount at the very top with the incentive code visible and a shop-now button above the fold, so the discount-only crowd can convert without scrolling.
- Add a short brand message headline (the source's example uses two words carrying the brand's positioning) so skimmers absorb what you stand for without reading a paragraph.
- Include one short social proof element and one or two differentiators (USPs), then the discount and another button.
- Show bestsellers below so people who do not know what to buy have a default choice, not a blank stare at your homepage.
- Close with a bottom button — the source notes most people will not scroll back up to find a top button if they end up at the base of the email.
Caveat: Design should be simple and clean; heavy layouts compete with the one action you want.
Caveat: Only discount-led lead capture suits this email; if your opt-in is a lead magnet or content offer, deliver that instead.

Tags: email-lifecycle, welcome-flow, offer-design, copywriting, conversion-optimization, product-page
Source: Ecommerce Email Marketing 2025.docx

---

## Email 2: put a face to the brand to convert skeptical new signups
Use when: Building the second email in the welcome flow for a store that customers find through ads and don't recognise.
- Assume the reason they have not purchased yet is partly that you are a faceless brand they stumbled on in an ad; the email's job is to make you feel like a real small company with a mission.
- Include a founding story in about two sentences, the mission, and — critically — a real face (photo of founders or maker), plus the reason the brand was started.
- State one or two differentiators (ingredients, process, sourcing) so the story is not only emotional but informative.
- Remind them of the discount above the button; include the button and a brand-aesthetic image.
- Do not expect this email to be a big revenue driver — the source says it will make some sales, but its real value is priming and trust building for later purchases.
Caveat: A fabricated or stock 'founder' image undermines the trust the email is meant to build.
Caveat: Emotional storytelling still needs factual product claims to satisfy skeptical buyers.

Tags: email-lifecycle, welcome-flow, customer-research, copywriting, positioning, conversion-optimization
Source: Ecommerce Email Marketing 2025.docx

---

## Email 3: use a bestseller email to collapse choice paralysis
Use when: Designing the mid-flow email for a store with a large catalogue where new subscribers don't know what to buy.
- Apply the source's observation that customers want choices but hate making them — so make the decision for them by featuring one or a few bestsellers rather than the full range.
- Give the bestseller a reason: not just the product name but specific, brief qualities (the example uses protein, fibre, prebiotics, plant ingredients), so the qualities you praise transfer to how the brand is perceived.
- Use one or two words or short bullets per point rather than sentences; keep proof concrete, not essay-length.
- Adapt the layout to a specific hero product, e.g. one shirt or one flavour, while keeping the same structure of headline, hero image, reasons, discount, buttons.
- Close with a discount reminder and a button, ideally with a button near the top as well.
Caveat: The 'wants choices but hates choosing' idea is the source's framing of consumer psychology, not a tested law.
Caveat: Featuring a product that is actually out of stock or barely stocked will burn the trust this email builds.

Tags: email-lifecycle, welcome-flow, merchandising, product-page, copywriting, conversion-optimization
Source: Ecommerce Email Marketing 2025.docx

---

## Email 4: add urgency plus risk reversal to push the fence-sitters
Use when: Writing the offer-reminder email mid-flow when subscribers are informed but still not purchasing.
- Write a headline that addresses the discount directly and states the code is expiring — the source's example pairs 'friendly reminder that your discount code is expiring' with 'we don't offer discounts often', which creates urgency and positions the brand as non-discount.
- Add risk reversals that answer the remaining purchase objections: free shipping, satisfaction guarantee, easy/free returns. The source flags the absence of risk reversals as the main improvement available in this kind of email.
- Use testimonials for trust, and consider pairing testimonials with individual products plus their discounts, so proof and offer sit together.
- Make the button large and unmistakable so clicking is trivially easy on mobile; the source argues an oversized button drives a very high click rate.
- Include a bottom link to browse the whole catalogue for readers who did not like the featured products.
Caveat: Frequent fake urgency erodes credibility — only claim expirations you will actually enforce.
Caveat: The 'we don't offer discounts often' line only works if it is true for your brand.

Tags: email-lifecycle, welcome-flow, offer-design, conversion-optimization, checkout, copywriting
Source: Ecommerce Email Marketing 2025.docx

---

## Email 5: answer 'why you instead of the competitor' head-on
Use when: Building the comparison email for a crowded niche where buyers are weighing several similar brands.
- Lead with the elephant in the room: in most niches there are thousands of alternatives, so state why someone should pick you.
- Use a short comparison table or list with brief 1-3 word points (the source's example contrasts customisation vs non-customisable, simple ordering vs complicated ordering, thoughtful gifting vs standard delivery). Keep it fast to scan.
- Follow the comparison with one expanded differentiator and an emotional benefit — the source's example describes what a delivered gourmet meal does for a corporate event or anniversary.
- Add a short testimonial for proof, then the discount and a shop-now button — the source also recommends a discount banner at the top of the email.
- Keep claims factual and comparable; you are giving shoppers the facts so they can choose, which is what the source argues makes the decision easy.
Caveat: Naming competitors invites regulatory and legal risk in some markets — check the rules before comparing by brand name.
Caveat: Overstated comparison points that customers can verify as false destroy the trust the rest of the flow built.

Tags: email-lifecycle, welcome-flow, positioning, competitor-research, copywriting, merchandising
Source: Ecommerce Email Marketing 2025.docx

---

## Email 6: dedicate a whole email to social proof
Use when: Building the trust email in the welcome flow, especially for new or unfamiliar brands.
- Fill the email almost entirely with proof: customer testimonials, verified reviews, review counts and ratings, media features. The source argues that even someone who only sees the subject line learns you are confident enough to stand behind your product.
- Visualise the rating distribution rather than just citing an average, and label reviews as verified — the source says his team tested that adding 'verified' next to a buyer's name improves conversions.
- Put a strong testimonial high in the email so it is visible on open, then add further reviews or a rating graphic.
- Include risk-reversal icons (secure payment, fast and free shipping, quality guarantee) and a button at the bottom for readers who are now in a buying mood.
- Use this email to answer the 'will this product actually work for me' objection, which is a reason people delay, not a reason they buy immediately.
Caveat: The claim that 'verified' next to a review lifts conversion is from the source's own testing, not a published benchmark.
Caveat: Do not invent or aggregate reviews you cannot verify — unverifiable proof is more damaging than none.

Tags: email-lifecycle, welcome-flow, conversion-optimization, customer-research, product-page, measurement
Source: Ecommerce Email Marketing 2025.docx

---

## Emails 7-8: close with hard urgency, then a founder's personal note
Use when: Writing the final two emails of a welcome flow, for subscribers who have received the whole sequence without buying.
- For email 7, keep it extremely simple: 'last chance' headline, product graphic, clear discount code, extreme urgency copy (the source's example ends the phrase with 'expires forever'), plus social proof icons and one big button.
- For email 8, switch to a plain text-based message from the founder: brief intro, reminder that the welcome discount was not used, an extension for one more day, a single shop-now link, and an invitation to reply with questions.
- Keep the text email to one action so there is nothing else to do but click; the source argues this simplicity, plus the personal tone, makes text-based founder emails among the highest-performing emails in the sequence.
- Use the final email to surface an objection: invite replies and commit to a response time, so anyone stuck on a question can get it answered and then buy.
Caveat: Treat the source's claim that text-based personal emails are top performers as his experience, not a universal result.
Caveat: Only extend the discount if you intend to honour it; repeat extensions train subscribers to wait.

Tags: email-lifecycle, welcome-flow, copywriting, conversion-optimization, offer-design, retention
Source: Ecommerce Email Marketing 2025.docx

---

## Configure the Clavio trigger and filter so buyers drop out of the flow
Use when: Setting up or auditing the automation behind your welcome/onboarding email sequence.
- Set the trigger to the specific list subscribers join from your popup (the source's example uses subscription to the 'newsletter' list), matching whatever your opt-in form actually adds people to.
- Add a flow filter set to 'placed order zero times since starting this flow' so a purchase removes the person from the sequence.
- Optionally use 'zero times over all time' if you want to be certain past purchasers never enter the flow; the source notes this as a more conservative option.
- Verify the settings in your own platform's current interface, since trigger and filter naming changes between versions and tools.
- Recheck the filter whenever you add a new popup, form or list, because a mismatched trigger means the flow silently never fires.
Caveat: The described Clavio trigger/filter wording is from the source's setup and may not match the current UI exactly.
Caveat: If your store sells high-frequency consumables, excluding all past purchasers may be wrong — decide based on whether the flow is genuinely welcome-only.

Tags: email-lifecycle, welcome-flow, klaviyo, retention, automation, measurement
Source: Ecommerce Email Marketing 2025.docx

---

## Give the welcome flow a target conversion rate and a testing loop
Use when: Reviewing welcome flow performance or deciding whether to invest in optimisation work.
- Set expectations with the source's heuristic: a 10% conversion rate from the welcome flow is his stated gold standard, and 20% would be considered very strong. Do not treat these as guaranteed outcomes.
- Accept that even at the gold standard, roughly 90% will not buy — so the flow's other job (priming) must continue through the rest of your email programme.
- A/B test the specific elements the source prioritises: subject lines and preview text, the offer structure (e.g. $10 off vs 10% off vs free shipping vs a free item with first order), which products are featured, and text-based versus graphic-based versions of individual emails.
- Also test linking to specific products versus linking to collections.
- In Clavio, the source prefers running the split with a conditional split because the numbers are easier to read; confirm the current split test tooling in your platform.
- Track small gains as compounding: his illustrative example is a store doing 100k/month with 10k from the flow, where a monthly 10% improvement adds ~1k in the first month and compounds thereafter.
Caveat: 10% and 20% are the source's stated targets for welcome flows, not universal benchmarks.
Caveat: The compounding arithmetic is an illustration, not a forecast; actual gains depend on traffic and repeatability.

Tags: email-lifecycle, welcome-flow, conversion-optimization, experiment-design, measurement, klaviyo
Source: Ecommerce Email Marketing 2025.docx

---

## Reuse winning campaigns as welcome-flow emails to save build time
Use when: Optimising the welcome flow when you have limited time to write new emails.
- Send 3-4 campaigns per week to your list, mostly non-promotional, and watch which angles outperform.
- When a campaign clearly crushes, adapt it for the flow: add a line such as 'use code XYZ for XYZ off your first order' and insert it into the sequence, or replace the weakest-performing welcome email.
- Use this to avoid building net-new emails while still refreshing the flow's content.
- Try campaign angles the source names as working well in welcome flows: myths vs facts in your industry, blog promotion, a specific product spotlight, a testimonial spotlight, a customer story, and product restock announcements.
- Keep the flow's core structure (intro, story, bestseller, urgency, proof, last chance) even as individual emails are swapped.
Caveat: Check the swapped email still fits the sequence logic and does not repeat what another email already says.
Caveat: Campaigns written for existing subscribers may assume context a new subscriber lacks; adjust the copy accordingly.

Tags: email-lifecycle, welcome-flow, crm, copywriting, retention, experiment-design
Source: Ecommerce Email Marketing 2025.docx

---

## Audit whether you actually have an abandoned cart flow (added-to-cart vs checkout started)
Use when: Auditing or rebuilding your cart/checkout recovery setup, or when your existing 'abandoned cart' flow underperforms despite being live.
- Open your ESP (Klaviyo, Mailchimp, etc.) and find the flow labeled 'abandoned cart' or 'abandoned checkout'. Read the actual trigger, not the name.
- Distinguish the two events: 'added to cart' fires when someone puts an item in the cart on a product/landing page; 'checkout started' fires only after they click checkout and reach payment. These are one funnel step apart.
- Klaviyo (via the Shopify integration) names the checkout-started flow 'abandoned cart' and adds it automatically; the added-to-cart metric is NOT installed by default. So a store can have 'an abandoned cart flow' that only catches far-down-funnel people.
- Check Klaviyo > Metrics to see whether 'Added to Cart' exists. If it doesn't, you have no true cart flow and are missing everyone who carted but never reached checkout.
- Install the added-to-cart snippet yourself (see the install card), then run a proper added-to-cart flow alongside the checkout-started flow. The source uses the same email content for both, cloned into two flows with different triggers.
Caveat: Source is strongly worded that ~90% of brands he audits have this mislabeled flow; that is a presenter observation, not an audited benchmark.
Caveat: Added-to-cart requires a manual snippet in most setups, so it is more technical than the auto-installed checkout trigger.

Tags: email-lifecycle, cart-recovery, klaviyo, measurement, checkout, conversion-optimization, flow-setup
Source: Ecommerce Email Marketing 2025.docx

---

## Why abandonment is so high and why recovery is high-leverage
Use when: Deciding how much to invest in cart/checkout recovery, or building the internal case to prioritize it over other store work.
- Reframe the add-to-cart: it is only half the sale. The source argues that in a market with thousands of brands per niche, getting a cart add is not a strong buying signal, so you must keep working the lead.
- Lead with the cost of inaction: every day a recovery flow is not live, abandoners are slipping away, and 26% of them reportedly buy the abandoned item from a competitor instead.
- Segment abandoners by the reason they left so you can address each: hard objection (they weren't convinced), distraction (kid threw a plate), or 'buy later' intent (waiting for a paycheck).
- Note that abandonment is now partly a browsing behavior: 59% of shoppers abandon just from browsing and use the cart as a 'save for later' / bookmark, like an Instagram like. That audience still needs a reminder.
- Recognize that more than 30% of shoppers plan to buy later but don't, because they forget, change their mind, or spend the money elsewhere. Automated reminders exist to beat the forgetting and the competitor.
Caveat: Statistics in the source (70-85% abandonment, 26% competitor purchase, 59% browsing, 30% plan-to-buy-later) are cited to external sources but presented without method detail; treat as directional.
Caveat: The 'burning cash' framing is the presenter's opinion about the opportunity cost of an inactive flow.

Tags: email-lifecycle, cart-recovery, customer-research, conversion-optimization, retention, competitive-analysis
Source: Ecommerce Email Marketing 2025.docx

---

## Design the recovery flow around the customer's decision cycle, not 1-2 emails
Use when: Planning the length, spacing, and branching of an abandoned cart/checkout email sequence.
- Don't stop at one or two emails over a couple of days. The source's target is a flow of roughly 6-8 emails (plus discount/support branches) spread across about 10 days to 1-2 weeks, to match a two-week decision window.
- Map why length matters: multiple reminders stop customers forgetting, keep you top of mind, give room to overcome objections, let good content out-position competitors, and give time for a considered decision.
- Branch the flow instead of sending one generic series: split by product/collection left behind (for product-specific info and testimonials), and split by prior-purchase status (for whether to offer a discount).
- Sequence by job: quick reminders first, then product-specific education and social proof, then a last-chance urgency email, then a buyer/non-buyer split into support vs discount emails.
- Keep the added-to-cart and checkout-started flows separate triggers but duplicate the same content so you maintain one set of emails.
Caveat: Length and spacing are the source's stated best practice, not a universal rule; every brand differs and the outline is a starting point, not a finished system.
Caveat: Spacing/timing should be tested for your audience rather than assumed.

Tags: email-lifecycle, cart-recovery, retention, flow-setup, experiment-design, conversion-optimization
Source: Ecommerce Email Marketing 2025.docx

---

## Write plain, item-first recovery copy that overcomes objections
Use when: Writing copy for any abandoned cart or checkout email.
- Make the item the number-one feature. Showing the exact product they left behind via dynamic product sections is described as carrying ~80% of the selling, so don't bury it under graphics or long copy.
- Keep copy short and to the point; the source states too many words or graphics distract the customer from completing the order.
- Focus copy on overcoming objections only: quick points on shipping, product use, customer reviews, and answers to FAQs.
- Use second-person, item-specific wording ('your order ships free') rather than generic broadcast copy ('all orders ship free') so it reads as addressed to them.
- Answer the questions a hesitant buyer would ask (is it healthy, how long does it last, when will it arrive) with concise facts, not a blog article.
- The source's stated purpose of every recovery email is narrow: remind, give the specific info needed to decide, and remove uncertainty about the buying process.
Caveat: The '80% carried by the item' figure is the presenter's estimate, not a measured benchmark.
Caveat: Tone can flex (one example uses playful copy), but the source still keeps product-specific substance central.

Tags: email-lifecycle, cart-recovery, product-page, copywriting, objection-handling, conversion-optimization
Source: Ecommerce Email Marketing 2025.docx

---

## Conversion-optimized recovery email layout
Use when: Designing or reviewing the template/layout for abandoned cart and checkout emails.
- Put a clear headline at the top that addresses the cart or states the value proposition (e.g., 'your order ships free').
- Place a prominent CTA button very high in the email so the customer can click without scrolling after opening.
- Display the abandoned item with all relevant info (name, price, image, link) via dynamic content.
- Add supporting sections/icons only if they are useful: shipping info, use of product, reviews.
- Stack risk-reversal and trust badges such as free returns, free return shipping, buy-now-pay-later, warranty, and 'talk with an expert'.
- Keep the whole design short and sweet — the source repeatedly warns against fancy graphics and long layouts for recovery emails.
Caveat: The layout principles are general recommendations; the specific example email (footwear brand) is illustrative, not a guaranteed result.
Caveat: Fewer elements per email risks needing more emails to cover all objections, which the source accepts as part of the spread-out flow.

Tags: email-lifecycle, cart-recovery, email-design, landing-page, conversion-optimization, trust-building
Source: Ecommerce Email Marketing 2025.docx

---

## Email 1: the 30-minute quick reminder
Use when: Setting up the first message and its send delay in a cart/checkout recovery flow.
- Time it short: the source typically sees best results sending email 1 about 30 minutes after abandonment; test 30/45 minutes against 1 hour and 4 hours, with 30-45 minutes usually winning.
- Keep the email minimal: 'take another look / we saved your items' plus a 'complete my order' CTA — do not add fancy graphics or extra words that distract.
- Show the specific items left behind via the dynamic product section.
- Add a short social proof line and risk reversals (e.g., ships in 1-3 days, free swatches) to nudge hesitant buyers.
- Purpose is narrow: simply remind the customer what they left behind and let them finish the order.
Caveat: The 30-45 minute timing is the presenter's observed best result; validate on your own list.
Caveat: A 'quick reminder' converts because the customer is still warm — it won't rescue cold or high-objection visitors.

Tags: email-lifecycle, cart-recovery, conversion-optimization, send-timing, experiment-design
Source: Ecommerce Email Marketing 2025.docx

---

## Email 2: second reminder with expanded social proof
Use when: Writing the second message in a recovery flow, roughly a day after the first.
- Reuse email 1's simple structure but add more social proof and risk-reversal than the first send.
- Aim it at two groups: those who just needed another reminder, and those who were waiting (paycheck) or comparing competitors.
- Include: a quick remark about the product, the dynamic product section, then expanded social proof and risk reversals (e.g., free shipping, free return shipping, buy-now-pay-later, warranty, chat with an expert).
- Keep it simple and similar to email 1 rather than inventing a new format.
- Let the extra reassurance carry skeptical buyers who weren't ready off a pure reminder.
Caveat: Same structure as email 1 means the value depends on the strength of your actual proof and guarantees, not the reminder itself.
Caveat: Timing is 'about a day later' per the source; adjust to your cycle.

Tags: email-lifecycle, cart-recovery, social-proof, conversion-optimization, objection-handling
Source: Ecommerce Email Marketing 2025.docx

---

## Emails 3-4: split by product for specific info, then specific testimonials
Use when: Building branching logic in the flow and creating product/collection-specific recovery content.
- Add a Klaviyo conditional split (or trigger split) based on which SKU/product/collection was left behind; you don't need one branch per product, a few main collections are enough.
- Email 3 gives product-specific information and overcomes objections specific to that product — e.g., for a cereal, the nutrition facts (sugar, carbs, protein, fiber, gluten-free) and how it compares. Keep it to the necessary facts, not a long article.
- Email 4 follows with testimonials specific to that same product (e.g., jacket abandonment gets jacket reviews, a 4.9/5 star rating with review count, customer quotes).
- The source's stated reason: a product-specific testimonial converts higher than a generic website testimonial in abandonments, because it speaks directly to the item and the person.
- Continue to include the dynamic product section in both.
- Show proof of why this works via A/B tests — the source cites a product-display test that produced ~6x more conversions (1 vs 6 purchases) on a higher-ticket product despite lower opens.
Caveat: ~6x conversion on a product-display test is a single cited test example, not a promised outcome.
Caveat: Targeting like the disease/health claims in the cereal example may carry compliance considerations in some categories.

Tags: email-lifecycle, cart-recovery, social-proof, customer-research, experiment-design, klaviyo
Source: Ecommerce Email Marketing 2025.docx

---

## Email 5: last-chance urgency email
Use when: Writing the mid-to-late recovery email that precedes the discount/support branch.
- Assume the customer now has the info from the product-specific and testimonial emails; the job of this email is to make them act.
- Go hard on urgency: a harsh deadline and 'your order is expiring' framing to trigger an impulse finish.
- Keep the format light: dynamic product section, urgency copy, social proof/risk-reversal icons, and finish-order CTA.
- Add a 'keep shopping' option because some people simply don't want that specific item — by this point (roughly day five / fifth email) showing alternatives can re-capture them.
- The source's rationale for delaying the 'keep shopping' suggestion: stay focused on the abandoned item in early emails, then broaden at the last-chance stage.
Caveat: Harsh deadlines only work if they are credible; the source stresses being strict on last-chance deadlines, so don't make deadlines you don't honor.
Caveat: Source preference for delaying 'keep shopping' is an opinion about focus, not a validated rule.

Tags: email-lifecycle, cart-recovery, urgency, conversion-optimization, merchandising
Source: Ecommerce Email Marketing 2025.docx

---

## Email 6A: buyer branch — founder support email, no discount
Use when: Configuring the prior-purchase branch in a recovery flow and writing the no-discount variant.
- Split the flow on whether the customer has purchased before; send this no-discount variant to past buyers only.
- Make it a plain text-style email from the founder (e.g., 'hey it's Mike, co-founder') to stand out from the rest of the sequence — the source notes this personal touch can make it one of the best-performing emails in the flow.
- Order the content: personal touch about the abandoned item, then an offer of support ('reply to this email, we'll get back to you within 24 hours'), then a final chance to order with a short urgency window.
- Keep it simple: founder voice, last chance, support offer.
- Rationale given: past buyers are the segment you least want to discount, and an unaddressed objection could be the reason for abandonment, so offering help may recover the sale without margin loss.
Caveat: The claim that this can be the best-performing email is the presenter's opinion based on client experience, not a guarantee.
Caveat: A 24-hour reply promise requires you can actually meet it; slow support could backfire.

Tags: email-lifecycle, cart-recovery, retention, positioning, customer-segmentation
Source: Ecommerce Email Marketing 2025.docx

---

## Email 6B: discount opener for first-time buyers, then a discount last-chance
Use when: Setting up the non-buyer branch of a recovery flow that uses a discount to acquire first-time customers.
- Send this branch only to customers who have never purchased, so the discount isn't given away to buyers who would convert without it.
- Email 6B: state the flash discount plainly (e.g., $10 off $200+) with urgency, plus the dynamic product section and a finish-my-order CTA. No elaborate graphics — the source says the dynamic section carries the load.
- Email 7 (discount last-chance): heavy urgency on the discount ('last chance, 25% off your cart, code expires today'). Keep it minimal and strict on the deadline.
- Email 8: for discount recipients who still didn't buy, mirror the founder support email but include the discount — personal founder touch, last chance to claim with the discount for a set window, and an offer of support with a reply-to-email.
- Rationale given: first-order discounts are accepted because once someone tries the product they're much more likely to come back, so the discount is an acquisition cost, not a margin giveaway to loyal buyers.
Caveat: Whether to discount at all, and the size/value threshold, is the presenter's choice ('depending on how averse you are to discounts'); he typically discounts only non-buyers or non-buyers in the last 60-90 days.
Caveat: Discount depth and urgency must be honored; non-credible deadlines hurt trust.

Tags: email-lifecycle, cart-recovery, offer-design, acquisition, urgency, customer-segmentation
Source: Ecommerce Email Marketing 2025.docx

---

## Install the added-to-cart metric and trigger in Klaviyo
Use when: Setting up or troubleshooting a true abandoned cart flow that captures add-to-cart abandoners.
- Check Klaviyo > Metrics. If 'Added to Cart' is missing, you need to install it. Verify against Klaviyo's current help doc since the interface changes.
- On the Shopify store, if your theme has custom liquid blocks and a section you can edit, go to the homepage/product section and paste the provided snippet in a custom liquid block, then Save.
- If you don't have an editable custom liquid block, edit theme code instead: insert the snippet under the body tag, wrapped with an 'if product' condition above and 'endif' below, per the guide, then Save.
- Test the snippet: append a UTM (email=whatever@youwant.com) to your store URL, visit the store, and add an item to the cart.
- In Klaviyo, search the email from the UTM and open the profile's activity feed; confirm an 'Added to Cart' event appears and the metric now exists.
- Set the flow trigger to 'Added to Cart' with filters: checkout started 0 times (so checkout abandoners route to the checkout flow instead), placed order 0 times, and not in this flow in the last 30 days. For the checkout-started flow, use the same filters minus the checkout exclusion.
Caveat: Klaviyo's snippet and metric setup can change; verify against Klaviyo's current documentation rather than relying on a saved snippet.
Caveat: Editing theme code incorrectly can break the store; the source says to contact Klaviyo support to get the correct dynamic sections if you get stuck.

Tags: klaviyo, cart-recovery, flow-setup, shopify, measurement, email-lifecycle
Source: Ecommerce Email Marketing 2025.docx

---

## Set up dynamic abandoned-item content (careful: cart and checkout variables differ)
Use when: Building the item-display block in recovery emails and troubleshooting broken/altered images or links.
- For added-to-cart dynamic content, use a split block: image on the left using the event image URL variable, and text on the right with item name and price variables. Point the checkout/cart link to your cart page (e.g., yoursite.com/cart) if you have one, otherwise Klaviyo's link sends them to the item they viewed.
- For checkout-started, the dynamic content is built as a table block that must be set to dynamic and customized, and it exposes more data because checkout passes more information from Shopify.
- Always preview with Klaviyo's preview feature to confirm the dynamic content loads before the flow goes live.
- Do not copy checkout dynamic content into the cart flow (or vice versa) — the triggers feed different information, so the variables won't map correctly.
- If the dynamic sections won't work, ask Klaviyo support (chat) for the correct variables for your trigger.
Caveat: Exact variable names and block options can change in Klaviyo; confirm current behavior in the app or with support.
Caveat: Source says ideally you have a cart page; without one, the fallback link sends people to a single item, which is a weaker recovery experience.

Tags: klaviyo, cart-recovery, email-design, flow-setup, checkout, measurement
Source: Ecommerce Email Marketing 2025.docx

---

## Set up A/B tests inside the flow rather than on the email
Use when: Running experiments on recovery emails and wanting quick visibility into results.
- Add a conditional split to the flow and create a random sample so branches split the audience evenly.
- Copy and paste the prior email into one branch as the variant.
- Reconnect the flow so both branches rejoin the main path afterward.
- Compare against Klaviyo's native 'create a test' option on the email itself; the source finds that harder to read because you must click into the email to see the data, whereas the flow method shows the numbers at a glance.
- Use the flow-level view to decide winners and iterate.
Caveat: The preference for flow-level splits is the presenter's workflow opinion, not an accuracy claim; both can be valid.
Caveat: Random-sample sizing and statistical significance are not covered here — don't over-read small test results.

Tags: klaviyo, experiment-design, email-lifecycle, measurement, cart-recovery
Source: Ecommerce Email Marketing 2025.docx

---

## Small A/B tests can compound into large revenue gains
Use when: Planning an ongoing optimization cadence for cart/checkout flows after initial launch.
- Treat the provided email outline as a starting point, not a finished system; every brand needs its own optimizations.
- Test small iterations, because the source says small changes can make or break the success of abandonment flows.
- Prioritize tests the source ran: subject line (one cited test tripled placed-order rate and roughly doubled click rate on the same volume), long-form vs short-form email (short-form reportedly better), content alignment (center vs left, cited at ~$5K extra in a month), product display (cited at ~6x conversions), text-based layout (cited at ~40% conversion boost), and email content (cited at ~2x conversions).
- Do the math on compounding: the source frames repeated 25-50% revenue boosts as compounding over time, using a Warren Buffett analogy.
- Run tests continuously rather than as one-offs, and pick one variable per test to keep results readable.
Caveat: All the percentage examples are the source's reported client test results, not guaranteed outcomes; do not treat them as benchmarks.
Caveat: The 25-50% revenue-boost range is the presenter's characterization of small-test upside; actual lift depends on your baseline and traffic.

Tags: experiment-design, email-lifecycle, measurement, conversion-optimization, cart-recovery
Source: Ecommerce Email Marketing 2025.docx

---

## Separate cart and checkout flows to avoid double-messaging
Use when: Configuring the triggers and filters of both recovery flows in Klaviyo.
- Build two flows: one triggered by 'Added to Cart', one triggered by 'Checkout Started'. Duplicate the same content into both so you maintain one set of emails.
- On the added-to-cart flow, add filters: 'Checkout Started = 0 times since starting this flow' (so anyone who moves to checkout exits and enters the checkout flow instead), 'Placed Order = 0 times since starting this flow', and 'has not been in this flow in the last 30 days'.
- On the checkout-started flow, use the same 'Placed Order = 0 times since starting this flow' and 'not in this flow in the last 30 days' filters, without the checkout exclusion (it's the trigger itself).
- Confirm both flows fire correctly and that a person who adds to cart then proceeds to checkout doesn't receive both sequences simultaneously.
Caveat: The 'last 30 days' re-entry window is the source's reset choice; adjust to your purchase frequency.
Caveat: Exclusion logic depends on trigger direction; verify in Klaviyo that your filters behave as intended.

Tags: klaviyo, cart-recovery, flow-setup, email-lifecycle, checkout, measurement
Source: Ecommerce Email Marketing 2025.docx

---

## Adapt to the 2024 more-competitive buyer who does due diligence
Use when: Setting the tone and content strategy of recovery and lifecycle messaging in a crowded niche.
- Assume the buyer has been burned online before (late shipping, not just non-delivery), so proactively answer logistics and quality questions: when will it arrive, will it arrive intact, what do reviews say, how long does it last.
- Assume the buyer is comparing you against many other brands in the same niche and may have added competitors' items to their cart too; your objection handling and content quality decide the win.
- Lead with risk reversal and specifics (shipping time, returns, warranty, reviews) rather than broad claims.
- Recognize shopping is entertainment for many buyers and carting is a bookmarking behavior, so reminders — not pressure — are often what's needed.
- Account for tighter budgets versus the stimulus-era spend; a discount targeted only at non-buyers can help first-time acquisition.
Caveat: This 2024 framing is the presenter's market read; timing-specific claims may age.
Caveat: Not every niche has thousands of brands or scam-scarred buyers — calibrate the level of proof to your category.

Tags: positioning, customer-research, trust-building, retention, email-lifecycle, objection-handling
Source: Ecommerce Email Marketing 2025.docx

---

## Build a six-email post-purchase flow with timed emotional beats
Use when: Setting up or rebuilding the post-purchase email flow for your store (replenishment/retention), especially if you currently only send an order confirmation and shipping notice.
- Set the trigger to 'order placed' with no filter so every buyer enters.
- Email 1 at 0 minutes: a plain, text-based thank-you from the founder. Split by purchase count (1st, 2nd, 3rd, 4th+) and change the wording slightly each time (e.g., 'you're almost a VIP' for repeat buyers). Include four things: sincere thanks, mission reminder, support offer, and a P.S. inviting an add-on to the order.
- Email 2 at ~24 hours: 'want to add more.' Send a general cross-sell of best sellers or split by product/category for curated recommendations tied to what they bought.
- Email 3 at ~3 days: a 'get excited, your order is being handled' message. You don't need a delivery trigger — estimate timing and link products at the bottom.
- Email 4 at ~6 days: 'how to get the most out of your product.' Split by what they ordered and give usage tips; add a recommended-product section to pair complementary items. This also reduces returns from misuse.
- Email 5 at ~7 days: ask them to follow one social platform (pick a single one, not several).
- Email 6 at ~1-2 weeks: a founder check-in asking how the order went, offering support, and optionally a review or repurchase prompt.
- After launch, analyze numbers and add or remove emails over time — this is a starting point, not a fixed template.
Caveat: Timing past the first day is estimated, not triggered by real delivery data.
Caveat: The presenter's claimed $48,000 in 30 days is a single case example, not an expected result.
Caveat: Higher-AOV products may see more buyer's remorse, so the reassurance emails matter more.

Tags: email-lifecycle, post-purchase, retention, flow-automation, upsell, product-education, founder-brand
Source: Ecommerce Email Marketing 2025.docx

---

## Exploit the 3-hour post-purchase buyer window
Use when: Designing the very first post-purchase email or deciding how aggressive to be with an immediate upsell after checkout.
- Send the first post-purchase email within minutes (the presenter's flow uses 0 minutes) rather than waiting a day.
- Use the founder gratitude email as the vehicle for the add-on P.S. — it reads genuine rather than pushy, so an add-on invite feels low-pressure.
- Reference the extra item the customer may have removed from their cart during checkout; a simple 'you can still add to your order' line is often enough to convert.
- Split the message by purchase count so repeat buyers get wording that acknowledges their loyalty, which makes the same add-on ask feel more personal.
- Track the placed-order rate of this single email; the presenter reports it converts unusually well for a plain text message.
Caveat: The 27% figure for repurchase within the first three hours is cited as third-party research — treat it as directional, not a guaranteed lift for your store.
Caveat: The presenter notes higher-AOV products carry more buyer's remorse, so push the gratitude/reassurance elements harder than the upsell.

Tags: email-lifecycle, post-purchase, upsell, timing, conversion-optimization, checkout
Source: Ecommerce Email Marketing 2025.docx

---

## Use founder-voice emails to build small-brand trust after purchase
Use when: Writing the copy and format for post-purchase gratitude and check-in emails where you want authenticity over polish.
- Write from the founder personally, using a plain text format with no heavy graphics — even if the customer doesn't buy, the email reads as sincere.
- Follow a fixed four-part order: (1) sincere thanks, (2) remind them of the brand mission, (3) offer support if they have questions, (4) encourage a repeat purchase or add-on.
- Use subject lines that reflect purchase count: 'your order means the world' (first), 'thank you again' (second), 'third time's a charm' (third), VIP framing (fourth).
- For the later check-in, write longer: reference the customer by name, the date of purchase, what results they should expect by now, cite a social-proof number (e.g., '150,000 others'), then offer the chance to shop and to reach out for support.
- Expect this check-in to generate useful qualitative feedback because it reads as a personal follow-up.
Caveat: The social-proof number must be real — do not invent customer counts or results.
Caveat: Persona varies: some brands use the actual founder, others a VP or named team member. Keep the voice consistent with who is really writing.

Tags: email-lifecycle, post-purchase, brand-voice, founder-brand, trust, copywriting
Source: Ecommerce Email Marketing 2025.docx

---

## Use product-education emails to cut returns and boost repeat orders
Use when: Writing post-purchase education emails (email 4 in the flow) or building usage guides for products with a learning curve.
- Split by what the customer ordered and give tips specific to that product, not generic advice.
- Include simple steps to use the product plus tips and tricks — this improves their chance of getting good results, which they will otherwise blame the brand for missing.
- Add a recommended-product section that shows how pairing with another product improves results — a subtle cross-sell framed as a benefit, not an ask.
- Use subject lines like 'how to get the most,' 'tips and tricks,' or '[Product] 101' to set the expectation of value rather than a sale.
- Reuse your strongest campaign content here: if a research or proof email performed well in campaigns, add it to the flow to reaffirm the purchase.
Caveat: The presenter notes the recommended-product section is the sales element — keep the email's primary focus on value so it doesn't read as a hard sell.
Caveat: Also cited as a way to 'stay fresh' by rotating successful campaign emails into flows over time.

Tags: email-lifecycle, post-purchase, product-education, returns, retention, cross-sell
Source: Ecommerce Email Marketing 2025.docx

---

## Set post-purchase email frequency to 3-4 sends per week
Use when: Deciding how many campaign emails (not flows) to send per week to your list.
- Choose a starting cadence of 3-4 campaigns per week — the presenter reports this outperformed both 1-2 per week and 5-7 per week on revenue and unsubscribes.
- Avoid 1-2 per week: the presenter says people see ~70 ecommerce brands per day (490 per week), so a weekly send gets forgotten and breaks the habit of opening your emails.
- Avoid 5-7 per week: while revenue rises, it plateaus, unsubscribes and complaints climb, and each message's impact is diluted.
- Keep every email's weight equal by spreading 3-4 sends across the week rather than clustering.
- Ramp gradually, as in the case where a client went from 2x to 4x per week and open rates went from under 50% to 61%.
Caveat: These are the presenter's own A/B-tested findings, not a universal rule your list will match — test on your own audience.
Caveat: The presenter warns that frequency is not the real lever: if you only send sales emails, even 1 per week will annoy your list.

Tags: email-lifecycle, campaign-frequency, deliverability, engagement, experiment-design, retention
Source: Ecommerce Email Marketing 2025.docx

---

## Send non-discount content to stay top-of-mind and win repeat purchases
Use when: Planning campaign content for a list you don't want to burn with constant promos, or when trying to protect margins.
- Shift campaign content toward value: tips and tricks, founder messages, brand stories, ingredient or product explanations, and 'our favorites' picks.
- Avoid relying on discount, buy-or-die, and 'gone forever' style emails — the presenter argues these read as needy and increase sales resistance.
- Aim for a healthy balance of product education and product promotion in every campaign calendar.
- Think of it as the 'top-of-mind effect': if you appear every other day, when a customer has a random need they think of you first.
- Use content to create the 'right place, right time' effect — more sends means more chances a customer happens to be in a buying mood.
Caveat: The point is to build a fan base and repeat purchases over time, not immediate sales on every send.
Caveat: The presenter frames this as protection against rising ad costs and shrinking margins — situational, not a promise.

Tags: email-lifecycle, content-strategy, campaign-calendar, retention, brand-positioning, margins
Source: Ecommerce Email Marketing 2025.docx

---

## Structure every email around one micro-topic and one takeaway
Use when: Choosing what each campaign email should say, or when you feel you have 'nothing to send.'
- Start from a large macro topic in your industry, product, or niche (e.g., for supplements: building muscle, burning fat, dieting, overall health).
- Break each macro topic into many micro-topics — e.g., 'best foods for dieting,' 'how to lower your appetite naturally,' 'best supplements to support dieting,' 'ingredient highlight.'
- Write one email per micro-topic and ask: 'What is the one thing I want the customer to know after reading this?'
- Use the problem-process-solution framework to structure it: educate on a problem, then the process, then position your product as the solution.
- Keep the takeaway to a single point — the presenter argues covering 6 topics means the customer remembers none, while one topic is remembered.
Caveat: The 3-5 second open window is the presenter's framing for why short, single-topic emails work.
Caveat: Micro-topics should still link back to a product benefit so education and positioning work in tandem.

Tags: email-lifecycle, content-strategy, micro-topics, copywriting, campaign-calendar, product-education
Source: Ecommerce Email Marketing 2025.docx

---

## Use the problem-process-solution framework to position your product
Use when: Writing campaign emails where you want to sell without an explicit discount, or when introducing a product to skeptical buyers.
- Educate on the problem first: 'why most people fail at XYZ' or 'why most solutions in this industry are bad.'
- Educate on the process: 'how to do XYZ,' 'how to overcome XYZ,' or 'the history / old way of XYZ.'
- Present the solution by positioning your product as the answer, then reinforce with how and why it works and how to use it.
- Answer the questions your customer is actually asking at each stage so their natural path leads toward the solution (your product).
- Use this to earn trust points the buyer needs before making a decision, and to remove friction for the due-diligence they do before buying.
Caveat: The presenter stresses subtly positioning the product — the education must be genuinely useful, not a disguised sales pitch.
Caveat: The framework assumes you can articulate a real problem your product solves.

Tags: email-lifecycle, content-strategy, positioning, copywriting, problem-solution, trust
Source: Ecommerce Email Marketing 2025.docx

---

## Generate unlimited micro-topics with a ChatGPT prompt
Use when: Building or refreshing your campaign calendar when you need many content ideas quickly.
- Define your macro topics first (the big themes in your niche or product), then ask ChatGPT to generate micro-topics under each.
- Use a prompt that requests ~100 micro-topic ideas tied to your product and industry, which the presenter says can cover a year of non-discount campaigns.
- Review the output and select topics you can genuinely educate on — the presenter notes the best topics come naturally, and AI just gives starting points.
- Recycle and refresh topics over time rather than discarding them, since the calendar is meant to keep evolving.
- Test the resulting topics against your own knowledge of the niche before sending — AI output is a draft, not final copy.
Caveat: The presenter emphasizes AI is 'not perfect' and the strongest ideas come from your own understanding of the market.
Caveat: The presenter notes the specific prompt and results are available in the free doc — verify the current interface of ChatGPT, which changes.

Tags: email-lifecycle, content-strategy, micro-topics, ai-tools, campaign-calendar, chatgpt
Source: Ecommerce Email Marketing 2025.docx

---

## Position email as warm-lead content between cold paid ads and repeat purchases
Use when: Deciding which email touchpoints to fund and how email fits with your paid acquisition channels.
- Use paid ads (Meta, Google, etc.) for the initial acquisition — getting cold traffic to your site and gaining their attention.
- Use email for the later stages: nurture the lead, hold their attention, and drive repeat purchases once they've bought.
- Rely on email over paid ads for repeat content because email is cheaper, you own the list, and it's predictable to scale.
- Use a pop-up to convert site visitors into subscribers, and plan for a known percentage of subscribers to purchase over time.
- Treat email as 'paid ads to people who already know, like, and trust you' — same function of driving traffic, far lower cost.
Caveat: The presenter stresses email needs paid ads to grow the list — this is not an argument against paid ads.
Caveat: Ownership of your list is a key advantage: no third-party platform can shut down your email channel.

Tags: email-lifecycle, acquisition, channel-strategy, audience-building, retention, paid-ads
Source: Ecommerce Email Marketing 2025.docx

---

## Understand the trust threshold before asking for a purchase
Use when: Setting expectations for email campaign performance with skeptical first-time buyers, or diagnosing low conversion from cold traffic.
- Assume most customers have been scammed online and do due diligence before buying — treat trust as the primary barrier, not price.
- Recognize the 'trust threshold': the point where a customer trusts you enough to make a purchase (even if they don't need the product yet).
- Deliver repeated exposures across multiple channels so that when a customer compares you with a competitor, you're the brand they've seen more often and gotten value from.
- Use email as the cheap, repeatable channel to stack those exposures after the first paid touchpoint.
- Expect that the customer who has seen you many times and gotten value will choose you over the brand they've only seen three times via paid ads.
Caveat: The presenter's comparison (brand seen 8 times across channels vs. 3 times via ads) is a heuristic illustration, not a study result.
Caveat: The trust threshold isn't measurable in a single number — the presenter describes it as an accumulation over time.

Tags: email-lifecycle, trust, customer-research, positioning, audience-building, conversion-optimization
Source: Ecommerce Email Marketing 2025.docx

---

## Run A/B tests on flows using the flow-level split, not the email-level test
Use when: Setting up an A/B test on an email inside a Klaviyo flow and choosing how to build the test.
- Add a conditional split to your flow and create a random sample to divide recipients between the two versions.
- Copy and paste the original email, edit the copy or design for the variant, then reconnect the flow so both paths continue to the next step.
- Use this method rather than the email-level 'create a test' button.
- Check results by opening the flow itself — the presenter prefers this because you can see the numbers right when you open the flow without clicking into the individual email.
- Review the split's overview numbers to decide which variant to keep.
Caveat: This is a tool workflow in Klaviyo; the exact interface and button labels may have changed — verify in your current version.
Caveat: The presenter prefers this method for visibility and flexibility, but notes it's an opinion, not the only correct approach.

Tags: email-lifecycle, experiment-design, flow-automation, klaviyo, measurement, ab-testing
Source: Ecommerce Email Marketing 2025.docx

---

## Add winning campaign emails into your post-purchase flow
Use when: Refreshing an existing post-purchase flow, or when you have a strong campaign email (e.g., a research/proof study) you want more mileage from.
- Identify campaign emails with strong performance — the presenter cites research-study or clinical-proof style emails as examples.
- Add that email into the post-purchase flow at a point where it reaffirms the purchase (e.g., after the product arrives).
- Frame it as reinforcing their decision — 'this is clinically proven' — rather than as a new pitch.
- Keep testing by adding and subtracting emails over time rather than setting the flow and forgetting it.
- Rotate content so customers in the flow don't see the same messages repeatedly.
Caveat: Only reuse emails that actually performed well; a weak campaign email won't improve in the flow.
Caveat: Any proof claims must be real and compliant — do not fabricate clinical or research claims.

Tags: email-lifecycle, post-purchase, content-reuse, flow-automation, retention, social-proof
Source: Ecommerce Email Marketing 2025.docx

---

## Use email frequency to build habitual opens and the exposure effect
Use when: Deciding whether to send more or less often, or when open rates are declining from infrequent sends.
- Send frequently enough (the presenter's tested sweet spot: 3-4 per week) that customers expect and look out for your emails.
- Make each email nice to look at and genuinely valuable, so each open delivers a small dopamine hit and they open the next one.
- Reinforce the loop: content, engagement, familiarity, loyalty — each cycle strengthens the relationship.
- Leverage the exposure effect — people learn to like what becomes familiar, so consistent good content turns subscribers into fans.
- Expect open rates from infrequent sending to fall, not rise, because the habit of opening is broken.
Caveat: The case mentioned — a client ramping from 2x to 4x per week saw open rates go from high 40s to 61% — is one example and partly reflects better content.
Caveat: The exposure effect is the presenter's framing; it only works if the content genuinely delivers value.

Tags: email-lifecycle, engagement, campaign-frequency, open-rate, retention, behavioral
Source: Ecommerce Email Marketing 2025.docx

---

## One-Benefit Email Framework
Use when: Planning your monthly email calendar and needing evergreen campaign angles for each product in the store.
- List 10+ distinct benefits per product, one benefit per email.
- Spread them out at roughly two per month (five months of coverage).
- State only one benefit per send; naming six benefits makes customers remember none.
- Lead with the benefit in the headline and keep the email visually simple, as in the 'banish festive fogginess' and Seed '61% of people experience digestive discomfort' examples.
- Reuse these campaigns repeatedly; repetition is how customers remember.
Caveat: The 'three-second read' and two-per-month cadence are the source's heuristics, not tested benchmarks.

Tags: email-lifecycle, campaign-planning, copywriting, content-calendar, product-marketing
Source: Ecommerce Email Marketing 2025.docx

---

## One-Feature Email: Selling Ingredient and Spec Differentiation
Use when: Writing product emails when every competitor claims the same benefit (e.g. protein powder that all says 'gain muscle').
- Write out every material or ingredient in the product; each can anchor its own email.
- Pick one feature per email rather than a benefits-only pitch — features like 'pre-digestive enzyme' or an AI capability are things people actively want to know.
- Assume the customer does not know what you consider common sense (David Ogilvy's point); spell the feature out.
- Show examples like 'tamanu oil' or 'what we mean by instantised creatine' — one specific item per email, not a list of five.
- For non-consumables, substitute the material or construction detail (e.g. clothing fabric composition).
Caveat: The source pushes back on 'benefits not features' as an oversimplification; both angles have a place.

Tags: email-lifecycle, product-marketing, positioning, copywriting, differentiation
Source: Ecommerce Email Marketing 2025.docx

---

## Single-FAQ Email to Kill Objections
Use when: Mining support tickets and reviews for purchase objections to turn into campaign content.
- Gather real questions from your support team and product reviews.
- Pick ONE question per email; a long FAQ dump gets ignored.
- Answer directly, then bridge into why your product solves it — e.g. 'how long until creatine works' answered with a timeframe and a shop link, or 'does whitening hurt teeth' answered with the damage-free alternative.
- Think like an alien who just discovered your product: what would they ask?
- Note that what's obvious to you as the industry expert is not obvious to the buyer.
Caveat: Timeframe numbers in examples are brand-specific; use your own verified claims.

Tags: email-lifecycle, objection-handling, customer-research, copywriting, conversion-optimization
Source: Ecommerce Email Marketing 2025.docx

---

## 'What's Inside' Email for Bundles and Consumables
Use when: Selling bundles, kits or consumable products where buyers don't know exactly what they'll receive.
- List every component of the bundle or product in a skimmable list format.
- Include free extras customers don't know about (installation guides, video guides, replacement parts) — brands often give these away without ever telling buyers.
- For consumables, list out everything in the food, beverage or supplement so buyers know what's entering their body.
- Use examples like an AG1-style unboxing of the welcome kit, or a 'seven super ingredients' list that keeps each item brief.
- Spread this across multiple emails rather than cramming everything into one.
Caveat: Keep each item short; the goal is scannability, not depth.

Tags: email-lifecycle, product-page, bundles, copywriting, offer-design
Source: Ecommerce Email Marketing 2025.docx

---

## How-It's-Made and How-To-Use Emails
Use when: Reducing hesitation on a product that seems complicated, or building brand story for a physical product.
- For 'how it's made': list every step from material gathering through factory, warehouse and shipment, or spotlight a single stage (e.g. 'we run every ingredient through three filters').
- Present the process with clear graphics or a simple A-to-Z sequence — a beer-style 'malt, mash, boil, ferment, bottle, age' layout works well.
- For 'how to use': write step-by-step instructions by actually using the product yourself and recording what you do.
- If the product is simple to use, reframe as 'how to get the most out of X' or 'how to style X' instead.
- Push the usage content into your post-purchase flow too; it fits both pre- and post-buy.
Caveat: Don't assume the customer knows your process even if all your competitors do the same thing — saying it still signals quality.

Tags: email-lifecycle, storytelling, post-purchase, objection-handling, brand
Source: Ecommerce Email Marketing 2025.docx

---

## Back-in-Stock Email Leveraging Popularity and Urgency
Use when: New inventory arrives, or you want a high-urgency campaign angle on restocked or returned items.
- Track when products or collections come back into stock.
- Draft a full feature email around the return — e.g. 'the Spidey Suds is back', 'the full glass is back in a new style'.
- Frame with limited-time language ('only here for a limited time') to add urgency.
- If a product didn't actually go out of stock, you can still use the restock angle when you receive new inventory.
- Buying signals to lean on: something went out of stock, so it's popular, and it may go out again.
Caveat: This is an attention angle, not a factual emergency; don't fabricate sell-outs you didn't have.

Tags: email-lifecycle, urgency, scarcity, campaign-planning, merchandising
Source: Ecommerce Email Marketing 2025.docx

---

## Trending Product Email — Frame Future, Not Past
Use when: Highlighting top sellers or building seasonal collection emails on your store.
- Pick the product or collection performing well and feature it.
- Frame as future trending ('these have been heating up; hottest trend for summer 2024') rather than past trending ('what was popular last summer').
- Create curated product selections linking to a collection page in Shopify-type platforms to lift conversions on the click-through.
- Lean into seasons whenever possible — seasonal selling performs especially well.
- Send these frequently; the source says you can't send too many.
Caveat: 'Future beats past trending' is the source's observed pattern, not a proven conversion benchmark.

Tags: email-lifecycle, merchandising, seasonality, collection-page, campaign-planning
Source: Ecommerce Email Marketing 2025.docx

---

## Reviews and Testimonials Email for Social Proof
Use when: Building trust for a newer brand or nudging hesitant subscribers with peer proof.
- Pull real reviews from your product pages and site.
- Use a maximum of two long reviews, or a handful of short ones — as in the Greens example using dated social-media comments.
- Include social media comments where possible; recent dated comments boost credibility.
- Keep the email short and simple, essentially just quotes plus a CTA.
- Testimonials do two jobs: prove you're a legit brand that delivers, and show others already bought and are happy.
Caveat: Only use real testimonials; the source emphasizes authenticity.

Tags: email-lifecycle, social-proof, retention, copywriting, customer-research
Source: Ecommerce Email Marketing 2025.docx

---

## Us vs Them Comparison Email
Use when: Competitive categories where buyers are weighing alternatives before purchase.
- Build a simple comparison table with digestible points — 'why we shine' or 'this product vs that product'.
- Show facts; do not beg for the purchase or lose frame, which increases sales resistance.
- Keep it skimmable so the customer can instantly see the differentiators.
- End with a clear CTA like 'shop now' and product link.
- Angle can also be used for product-vs-product within your own line.
Caveat: Keep claims accurate and verifiable; a table format doesn't excuse unsubstantiated comparisons.

Tags: email-lifecycle, positioning, comparison, conversion-optimization, copywriting
Source: Ecommerce Email Marketing 2025.docx

---

## Myth vs Fact Email
Use when: Your niche has persistent misinformation (sunscreen, supplements, etc.) that blocks purchases.
- Identify common misconceptions buyers hold about your product category.
- Structure emails as 'myth: X / fact: Y', either one myth per email or rapid-fire several.
- Use an intriguing headline, as in the sunscreen myth-busting example with multiple 'myth busted' sections.
- Keep copy punchy — customers won't read long explanations.
- Consider a series of myth emails; the source says series have worked well historically.
Caveat: Long myth-vs-fact copy underperforms; condense and make it scannable.

Tags: email-lifecycle, objection-handling, copywriting, customer-research, campaign-planning
Source: Ecommerce Email Marketing 2025.docx

---

## Blog Promo Email That Sells the Click
Use when: You have blog content and want engagement that moves people down the funnel without a hard pitch.
- Use an existing blog post with an intriguing headline.
- Give only a sneak peek — withhold enough that clicking is worthwhile; do not dump the whole article into the email.
- Sell the click aggressively via prominent buttons and a 'read more' / 'get the scoop' CTA.
- Place product recommendations further down in the email after the article context.
- Rationale: a subscriber clicking a blog is already committing to browsing, making later site shopping more likely; blog emails read as soft-sell and still drive sales.
Caveat: The source criticizes its own examples for giving too much info; reduce to preserve click incentive.

Tags: email-lifecycle, content-marketing, landing-page, traffic, soft-sell
Source: Ecommerce Email Marketing 2025.docx

---

## Research Study Highlight Email
Use when: Looking for high-credibility campaign content that your list rarely sees.
- Search Google Scholar for your industry niche; also possible via ChatGPT with a prompt.
- Spend no more than a few minutes; read the abstract to judge applicability.
- Pick a study that either busts a myth or supports an ingredient/material you use.
- Connect it to your brand even if it's not a study of your own product — e.g. 'new study reveals the link between soft gums and inflammation', then show your product solves soft gums.
- Lay out the study with a clear breakdown and a learn-more CTA.
Caveat: The source says this shouldn't take more than a couple minutes to find a decent one.

Tags: email-lifecycle, authority, content-marketing, research, trust
Source: Ecommerce Email Marketing 2025.docx

---

## Holiday Email Using Obscure Holidays
Use when: Filling campaign calendar gaps and adding engagement without overt promotion.
- Find random holidays; use sites like checkiday.com, blank calendar pages, or ChatGPT.
- Pick one that connects to a product or niche (e.g. National Irish Coffee Day used by Jameson, National Hiking Day used by AllTrails).
- Build a light, fun email around it with a natural product tie-in.
- You can still send standard major-holiday emails; these add incremental volume and engagement.
Caveat: Keep the tie-in plausible; a forced holiday-to-product link can feel gimmicky.

Tags: email-lifecycle, content-calendar, engagement, seasonality, campaign-planning
Source: Ecommerce Email Marketing 2025.docx

---

## 15 Rapid-Fire Campaign Angenres for Ecommerce Lists
Use when: When building monthly calendars and needing more micro-topic campaign angles across the store.
- Progress update: share company milestones and achievements — people like being part of a growing brand.
- Customer transformation and before/after: real before-and-after narratives of product impact.
- Puzzles and riddles: brain teasers related to your industry as a fun break.
- Note from the founder: personal CEO message with news or insights.
- Gift guide: curated recommendations (e.g. wedding season, summer).
- Treat yourself: self-care excuse to buy.
- Media publication: coverage in news or Shark Tank and similar.
- Behind the scenes: warehouse/office footage or product stories.
- Tips and tricks: valuable quick advice.
- UGC: tagged customer photos, reviews and influencer content.
- Sneak peeks: reward subscribers with early looks.
- Flashback/Throwback: nostalgic content and past milestones.
- Staff picks: bestsellers framed as individual staff favorites.
- Brand values: showcase what the brand stands for.
Caveat: Not one campaign type; use selectively against your list's appetite.

Tags: email-lifecycle, campaign-planning, content-calendar, engagement, creative-strategy
Source: Ecommerce Email Marketing 2025.docx

---

## Building a Monthly Campaign Calendar
Use when: Turning a library of campaign ideas into an actual send schedule for your store.
- Step 1: Determine important dates — holidays, product launches, sale dates — and insert them into the calendar first so everything else builds around them.
- Step 2: Add supplementary emails around those anchors — reminders for sales, teasers for launches.
- Step 3: Fill remaining gaps with micro-topic campaigns (one-benefit, one-feature, FAQ, etc.).
- Aim for three to four campaigns per week, each on a micro-topic.
- Example structure: a St Patrick's Day 20%-off sale, a new product drop, supplementary emails around each, and micro-topics filling the rest.
Caveat: The three-to-four-per-week cadence is the source's heuristic from agency work; adjust to list health.

Tags: email-lifecycle, content-calendar, campaign-planning, operations, seasonality
Source: Ecommerce Email Marketing 2025.docx

---

## Segmentation: Dynamic Segments vs Static Lists
Use when: Designing list architecture in Klaviyo or similar before building campaigns and flows.
- Distinguish lists (static, flat collections of people) from segments (dynamic, updating in real time based on criteria).
- In Klaviyo, lists and segments live under the same area but segments are the dynamic ones.
- Start with basics: email open behavior, click behavior, frequency.
- Intermediate: recent store activity like abandoned cart, recent purchase.
- Advanced: flow-specific engagement or product-category interest.
- Before hypersegmenting (e.g. by favorite color), weigh the tradeoff — the source argues three to four broad campaigns to 50,000 will beat one to two narrow campaigns to 10,000 '99 times out of 100'.
Caveat: That ratio is the source's claimed experience, not a measured guarantee; they do say there's a time and place for segmentation.

Tags: email-lifecycle, segmentation, klaviyo, deliverability, campaign-planning
Source: Ecommerce Email Marketing 2025.docx

---

## Email Engagement Segments for Deliverability
Use when: Setting up your base sending architecture so campaigns never blast the full list.
- Create an X-day engaged segment — 'opened an email at least once in last 60 days OR clicked in last 60 days' (the OR guards against missed open tracking).
- Add 'has not bounced an email ever' to exclude dead/fake addresses.
- Decide the X window: start at 30 days if new to segmentation, then expand to 60, 90, 120 as open rates climb.
- Target at least 40% opens before expanding; when opens hit ~50%, open the window to the next tier and repeat.
- Create an unengaged members segment (subscribed, opened at least once historically, but no open/click in ~90 days) and email them around once per month — or suppress entirely.
- Never send general campaigns to the whole list except major moments like Black Friday, because non-openers damage deliverability with inbox providers.
Caveat: The step-ladder and 40-50% thresholds are the source's recommendations, not universal benchmarks.

Tags: email-lifecycle, deliverability, segmentation, klaviyo, list-hygiene
Source: Ecommerce Email Marketing 2025.docx

---

## Store-Engagement Segments to Find Funnel Leaks
Use when: Diagnosing conversion loss and building targeted campaigns beyond flows.
- Viewed a product at least once in past 30 days but no purchase = interested customers.
- Added to cart or started checkout in past 30 days but no purchase = high likelihood to purchase; engage these hard.
- Placed an order = recent buyers.
- Placed five-plus orders = VIP customers.
- Viewed at least three products without purchasing = window shoppers.
- Use these to track where people are lost — e.g. lots of product views but few add-to-carts signals a product-page problem.
- Targeted campaigns (new colorway, special discount) can be sent only to product-category-interested segments without bothering the rest of the list.
Caveat: Mostly used alongside flows; campaigns are added on top, not instead.

Tags: email-lifecycle, segmentation, conversion-optimization, customer-research, product-page
Source: Ecommerce Email Marketing 2025.docx

---

## High Potential Purchaser Segment
Use when: Running an extra sale or push to people who are actively shopping but haven't purchased.
- Definition: subscribed AND placed zero orders in past 30 days AND (active on site OR viewed product OR added to cart OR started checkout in past 30 days).
- Use OR conditions between the activity triggers as a safety net for missed event tracking.
- Send these people one to two extra emails per month on top of your engaged list sends — a targeted sale or extra push.
- Reserve certain offers for this segment rather than the whole list so you don't discount for everyone.
Caveat: Some conditions overlap intentionally; the source keeps them to guard against broken triggers.

Tags: email-lifecycle, segmentation, conversion-optimization, klaviyo, retargeting
Source: Ecommerce Email Marketing 2025.docx

---

## VIP Segment Built on Purchase Count
Use when: Designing a loyalty/VIP segment and corresponding email cadence.
- Base definition: subscribed AND placed an order at least five times all-time.
- Prefer purchase count over total spend because spend thresholds are harder to predict — someone at $900 toward $1,000 might buy a $20 item and miss the goal, causing frustration.
- With a count-based threshold, after the fourth purchase you can notify them they're one order from VIP and a free gift.
- Send VIPs at most one extra email per month on top of the engaged list.
- Run a welcome flow for anyone entering the segment — thank them and give exclusive content or a generous offer.
- Send a VIP-only offer at least once a quarter.
Caveat: Five orders is the source's illustrative threshold; use one that fits your purchase frequency.

Tags: email-lifecycle, segmentation, retention, loyalty, loyalty-program
Source: Ecommerce Email Marketing 2025.docx

---

## Winback and Unengaged: Distinguishing Two Recovery Segments
Use when: Building reactivation and repurchase campaigns for your list.
- Unengaged members = email-side: subscribed and once engaged but no open/click in ~90 days; email roughly monthly with a comeback offer.
- Winback potential customers = purchase-side: past buyers who haven't purchased in a while; also email ~one extra per month on top of engaged sends.
- Set the winback window to the store's typical inter-purchase interval — hot tubs might be years, supplements much shorter.
- Regular campaigns to the engaged list can also be sent to the unengaged once a month as a low-effort recovery attempt.
- Don't send every campaign to unengaged people; it drags down open rates and sender reputation.
Caveat: The 90-day threshold isn't sacred; 120 days is similarly acceptable per the source.

Tags: email-lifecycle, segmentation, retention, winback, deliverability
Source: Ecommerce Email Marketing 2025.docx

---

## Predictive Analytics for AOV, CLV and Replenishment Timing
Use when: Upgrading segmentation beyond basic behavior to optimize offers and timing.
- Open Klaviyo predictive analytics and inspect average order value cohorts.
- If store AOV is ~$50, build a segment with AOV $100+ and target them with bundle deals or large inventory-clearing offers.
- Segment by predicted customer lifetime value to identify VIPs.
- Segment by average time between purchases — e.g. if a cohort reorders every 45 days, fire a reminder flow around day 40.
- Segment by predicted gender to tailor product recommendations and creative.
Caveat: The source notes Klaviyo predictions aren't perfect — treat as directional data.

Tags: email-lifecycle, predictive-analytics, klaviyo, segmentation, retention
Source: Ecommerce Email Marketing 2025.docx

---

## Location Segmentation for Pop-Ups and Regional Offers
Use when: Running pop-up shops, in-person events or country-specific storefronts.
- Build segments by city, state or country.
- For an in-person event, target subscribers in that city (e.g. a San Diego pop-up).
- Use location to handle compliance requirements and localized store experiences across countries.
- Also useful for brand-headquarters-area promotions.
Caveat: Requires reliable location data; some subscribers won't have it.

Tags: email-lifecycle, segmentation, events, personalization, localization
Source: Ecommerce Email Marketing 2025.docx

---

## Cadence and Content Rule: Send Three to Four Emails a Week
Use when: Deciding how many campaigns per week to run and worried about unsubscribes.
- Send three to four campaigns per week to the engaged segment, per the source's experience across 50+ ecommerce brands.
- Keep content strong; the source observed lower unsubscribe rates at this frequency than sending once a week.
- Each campaign should be built on a distinct micro-topic so the list doesn't fatigue.
- Frequency only works when paired with engagement segmentation; sending that much to unengaged people backfires on deliverability.
- Use the calendar structure: metrics (3-4/wk) and topic diversity are both required.
Caveat: The source's observation, not a universal rule; test against your own unsubscribe and spam rates.

Tags: email-lifecycle, campaign-planning, deliverability, list-health, retention
Source: Ecommerce Email Marketing 2025.docx

---

## Build core Klaviyo segments: VIP, winback, suppress, engaged
Use when: Setting up or auditing your store's email segmentation and deciding which lists to actually send to and suppress.
- VIP: customer can receive marketing and has placed 5+ orders all-time. Source's base definition uses order count because it is simpler and more predictable than combining orders and spend (e.g. 5+ orders AND $500+); try VIPs with a special offer at least once a quarter.
- Winback potential: customer can receive marketing, placed at least 1 order in the last 150 days, and 0 orders in the last 90 days — i.e. their last purchase fell in that 90-150 day window. Trigger a short flow when they enter; later in the flow, consider a discount for those who still haven't repurchased.
- Suppress list (send nothing): opened 0 emails in the past 180 days, OR has ever bounced, OR has ever marked an email as spam. Review it monthly and mark those profiles suppressed in Klaviyo settings to protect deliverability and cut list-based billing costs.
- Unengaged is strictly about email engagement; winback is strictly about past customers — keep them separate.
- Tune the winback window to the average buying cycle: a supplement brand on 30-day servings might start winback around day 45; a hot-tub seller may need years between purchases.
- Don't build dozens of tiny segments. The source's stated priority is to first have the basics done well — e.g. an 8-email abandoned-cart flow and a popup converting better than 3% — before chasing elaborate segmentation that may only add a few percent.
Caveat: All thresholds above are the source's own base definitions, not validated benchmarks; adapt them to your store's order data and buying cycle.
Caveat: Source is opinionated that beginners should fix basic flows and popup conversion before advanced segmentation; complex segments were framed as marginal gains.

Tags: email-lifecycle, segmentation, klaviyo, vip, winback, deliverability, retention
Source: Ecommerce Email Marketing 2025.docx

---

## Interest and cross-sell segments by product/category
Use when: Planning a product drop, category promo, or automated cross-sell (e.g. buyer of one item toward a complementary item).
- Interest-in-X segment: customer can receive marketing AND has viewed an item at least once where the category/collection is X, OR added to cart where category is X, OR started checkout where collection is X, OR placed an order where collection is X (all over all time).
- Use this for 1-2 extra sends per month on top of your engaged-list emails when you have a launch or sale tied to that product/category.
- Cross-sell segment: customer can receive marketing AND has placed an order at least once all-time where collection equals the trigger product (e.g. bought white shoes). Then run a flow/email selling the match (white socks) and reference the exact item they bought.
- Add a negative condition to protect the message: e.g. ordered protein at least once all-time AND ordered pre-workout 0 times all-time, so pre-workout buyers never get the pre-workout cross-sell.
- In Klaviyo, viewed/added-to-cart metrics use Klaviyo's category values while Shopify-native triggers (started checkout, placed order) use collections — make sure your products are organized in Shopify so both line up.
Caveat: Confirm current Klaviyo/Shopify metric names and filters in the live interface, as the terminology shifts between platforms and updates.

Tags: email-lifecycle, segmentation, klaviyo, cross-sell, shopify, flows, merchandising
Source: Ecommerce Email Marketing 2025.docx

---

## Resend unopened important emails with the campaign-ID segment trick
Use when: Maximizing reach on high-value sends like Black Friday, a major product release, or a big announcement.
- Open the sent campaign in Klaviyo and copy the campaign message ID code from the URL.
- Create a segment with two conditions: received email at least once all-time where message equals that code, AND opened email 0 times all-time where message equals that code. Klaviyo will resolve the campaign name for you.
- Duplicate the original campaign and send it only to that segment, 1-2 days after the original.
- Change the subject line and preview text so the resend doesn't read as a repeat to anyone who saw (but didn't open) the first.
- Source frames this as an 'instant revenue booster' — if the original had e.g. a 60% open rate, 40% never saw it.
Caveat: Treat any specific open-rate figure as an illustrative example, not a benchmark.
Caveat: This is a case-by-case tactic, not a permanent dynamic segment — rebuild it per campaign.

Tags: email-lifecycle, segmentation, campaigns, klaviyo, subject-lines, deliverability
Source: Ecommerce Email Marketing 2025.docx

---

## Optimize email copy for the skim, not the read
Use when: Writing or editing any campaign, welcome, or abandoned-cart email where copy currently appears as long paragraphs.
- Shift your mindset: design emails for skimming, not for reading, because inbox attention is short and readers open in bursts between tasks.
- Avoid blocks of text entirely — long paragraphs make the eye skip past; split copy with line breaks, subheaders and distinct sections.
- Bold your main points so the eye is forced to follow them; most people will read only the bolded lines, so those must carry the full message on their own.
- Use body copy underneath each bold point as the supporting justification and proof for those who read further.
- Turn enumerated benefits into short labeled lists or numbers instead of a paragraph — e.g. five points listed out with bolded labels rather than one dense block.
- Use comparison layouts (us vs. them, empty vs. daily) with bold subheads so readers grasp the contrast without reading the details.
Caveat: The specifics of how email clients render bold, formatting and line breaks vary — test appearance across devices before sending.

Tags: email-lifecycle, copywriting, skimmable-copy, email-design, conversion-optimization, campaigns
Source: Ecommerce Email Marketing 2025.docx

---

## Clear and concise email copy: short and sweet, one takeaway
Use when: Writing campaign or flow copy that risks cramming several benefits or messages into one send.
- Keep the email to roughly 1-2 phone scrolls maximum; source's guidance is shorter is better because only a few seconds of attention are available.
- Choose ONE takeaway per email and build the headline around it — e.g. a matcha email solely about 'enhances the benefits of caffeine', or a hair-loss email solely about growth potential.
- Ask yourself before sending: is there one clear thing the customer can take away? If the email tries to give 3+ takeaways, assume readers remember none.
- Split a benefit-stuffed email into a series: instead of one email listing estimator, graphs, alerts, multi-cook view, etc., dedicate a whole email to each feature one at a time.
- Cut implied information. On a welcome email, skip telling subscribers they get exclusive offers/insider access (they already know from the opt-in) and let the discount code sit in the clear space you save.
- Every sentence should move the reader toward a purchase; delete fluff that only fills space.
Caveat: Some emails (e.g. a flowchart or comparison email) are intentionally longer because the format itself is the engagement — length alone isn't the failure, unclear/multi-message copy is.

Tags: email-lifecycle, copywriting, welcome-flow, conversion-optimization, campaigns, message-clarity
Source: Ecommerce Email Marketing 2025.docx

---

## Write engaging copy: punchy, informational, entertaining
Use when: Writing campaign copy that feels flat, corporate, or repetitive and is underperforming on opens and clicks.
- Make copy punchy: short but information-dense, evoking emotion. Example structure packs a stat plus a benefit into a tiny space (e.g. a toilet-time stat tied to a digestive product benefit rather than a bland feature list).
- Make copy informational: give facts and education, because people want to make an educated purchase decision. Source's view is that anything that isn't information is fluff — 'highest quality ingredients' should be replaced with actual ingredient facts; aim for the reader to learn something every open.
- Make copy entertaining: use jokes, puns, puzzles and graphics, since TikTok-era dopamine tolerance means new/novel content works and repetition does not.
- Say 'we'll spill the milk' and lead with real facts instead of generic claims — the source's cereal example packs protein content and 'fewer cravings' into a playful, factual line.
- Source's rule of thumb: if a reader can clearly name the one takeaway (e.g. 'golden root is good for you and it's in this product'), the copy is working.
Caveat: Source is deliberately opinionated that copy needs humor and punch; brand-voice fit matters — a corporate/clinical brand may apply 'entertaining' more subtly and should test.

Tags: email-lifecycle, copywriting, engagement, brand-voice, campaigns, conversion-optimization
Source: Ecommerce Email Marketing 2025.docx

---

## Use infographics as email 'secret sauce' to hit all copy principles
Use when: Designing email layouts when deciding how to present benefits, comparisons, or product education beyond plain text.
- Map your own copy into one of these infographic formats and hand it to a designer rather than writing blocks of text: checklists, icon graphics, feature diagrams, timelines, numbered lists, comparison charts (us vs. them), tables, flowcharts, and graphs.
- Checklists: present benefits with checks so the reader's eye scoops them up without reading sentences; the designer can interpret the layout creatively.
- Icon graphics: attach simple icons (vegan, gluten-free, soy-free, non-GMO) to the product so a knowledgeable viewer recognizes them without reading labels.
- Feature diagrams: point call-outs at parts of the product image (e.g. 'large glossy violin-shaped leaves', 'upright trunk') to show exactly what the buyer receives.
- Timelines: map when results appear (month 1/2/3) or brand history — useful in post-purchase flows and welcome campaigns.
- Tables and comparison charts: lay out ingredient or plan differences side by side so undecided buyers can self-select; flowcharts demonstrate which product suits which use case.
- Source's practice: include at least one infographic inside every email.
Caveat: More creative formats (flowcharts, custom diagrams) take more production effort; the source notes it's a tradeoff against simply listing benefits.

Tags: email-lifecycle, email-design, infographics, skimmable-copy, product-page, conversion-optimization
Source: Ecommerce Email Marketing 2025.docx

---

## Outline email copy in a doc against an existing template
Use when: Briefing designers or building any email where you want control over layout placement, not just the words.
- Find an existing email you like (source searches sites like reallygoodemails.com or mill.com) and use it as the structural template.
- In a Google Doc, recreate the email's structure visually: label the headline, sub-headline, hero section, body, bullets, tables, and every CTA position ('shop now').
- Describe the visual treatment inline — e.g. 'simple hero section showing this on a GIF', 'try a new graphic style: table', 'fan favorites laid out here'.
- Include notes on layout spacing and ordering rather than dumping all copy in a list, because list-only briefs give you no control over where copy lands (top vs. bottom) and how it affects conversion.
- Keep every element mapped (headline → sub-headline → graphic → image of product → shop now) so the designer can execute without guessing.
Caveat: This is a workflow recommendation from the source, not a tested result; adjust the doc format to your team's handoff process.

Tags: email-lifecycle, copywriting, email-design, workflow, campaigns, creative-strategy
Source: Ecommerce Email Marketing 2025.docx

---

## Prime ChatGPT with your brand, then request punchy hero copy
Use when: Facing a blank page on a campaign, drop, or launch email and needing a fast first draft to refine.
- Step 1 — Prime: tell ChatGPT your e-commerce brand, product types, mission/goal, USPs, what makes your products unique, customer demographics and ages, brand voice preference, and customer goals/aspirations. Then ask 'Are you ready to write copy based on the topics I give you?' It retains this context within the same chat window.
- Newer models: paste your website URL and tell it to use the site as additional context (the source notes it can recognize the brand from the site, though this depends on the current interface — verify before relying on it).
- Step 2 — Request: state the email type and topic ('graphic-based email campaign with minimal copy, topic X'), supply the topic details and USPs, then ask for a quick punchy headline, a slightly longer sub-headline, 2-3 sentences of body copy, and a 'shop now' CTA.
- Treat the output as a starting point covering roughly the hero and bridge sections; add your own testimonials and further sections yourself.
- Edit the draft to sound less like ChatGPT and more like your brand before sending.
Caveat: Source's own view: it's always better to write it yourself and use ChatGPT only for a starting point; outputs need editing.
Caveat: Prompt behavior and what the model retains can change with ChatGPT versions — re-verify what context it actually holds.

Tags: email-lifecycle, copywriting, chatgpt, ai-tools, campaigns, workflow
Source: Ecommerce Email Marketing 2025.docx

---

## Prioritize basics before advanced segmentation and copy tricks
Use when: Deciding where to spend limited email/lifecycle effort when the store's fundamentals are still underperforming.
- Check the fundamentals first: does an abandoned-cart flow exist with around 8 emails, and is the popup form converting above 3%?
- If those basics are missing or weak, fix them before building intricate interest/cross-sell segments, since low-hanging fruit usually outperforms fragmentation.
- Source's stance: the fancier segmentation may only add a couple of percent in conversion or a little extra revenue, and shouldn't distract from the priority work.
- Once basics are solid, layer in the more advanced segments (VIP, winback, interest, cross-sell) and copy tactics.
Caveat: These specific figures (8 emails, 3% popup conversion) are the source's heuristics, not universal benchmarks — adapt to your store and test.

Tags: email-lifecycle, prioritization, abandoned-cart, popup, conversion-optimization, workflow
Source: Ecommerce Email Marketing 2025.docx

---

## Write email copy with an AI prompt + real email outline
Use when: You need campaign email copy (best sellers, restock, promo) and want a repeatable fast workflow instead of a blank page.
- Find a real email you like from a swipe source (the source names reallygoodemails.com and mill.com; verify current URLs) for the niche you're mailing.
- Map its blocks exactly as an outline: headline, body copy, sub-headline, product collection section with per-product blurbs, CTA, footer — this gives your designer a clear map.
- Improve the skeleton before writing: the source presenter added a 'Shop Now' button at the top linking to the best-sellers page, because the original's buttons sat too low; keeping a CTA above the fold is a stated preference, not a measured rule.
- Feed the AI a context block: brand name and what you sell, mission, what makes brand/products unique, ideal customer, brand voice (e.g. 'conversational, motivational, like a friendly coach who gives tough love'), customer goals, and your website URL.
- Then give a second prompt: campaign format (e.g. graphic-based, minimal copy), topic, and explicit asks — punchy headline, longer sub-headline, then 2–3 sentences of copy leading into the Shop Now CTA.
- Iterate in-thread: ask for multiple headline options, ask to make them more conversational or less corny, and switch direction if an angle stalls (the demo abandoned 'meet your MVPs' for 'PR day' because gym-goers recognize the term).
- Write per-product blurbs yourself from real product descriptions — short, voice-matched lines like 'minimal and smooth, perfect for arm day' — rather than generic AI filler.
Caveat: AI drafts need proofreading; the demo relied on Grammarly and manual editing.
Caveat: Don't invent product claims; pull specifics from the actual product description page.

Tags: email-lifecycle, copywriting, ai-tools, campaign-brief, creative-strategy, email-design
Source: Ecommerce Email Marketing 2025.docx

---

## Treat subject lines as frames, and test them on revenue
Use when: Setting up or interpreting A/B tests on subject lines for any campaign email, especially abandoned cart.
- Accept the stated premise that a strong sender reputation plus consistently good content is what drives routine opens — the presenter argues subject lines 'should not matter' for opens and aims for opens driven by sender name, like a creator whose audience watches regardless of title.
- Use subject/preview to set the buying frame instead of describing the email: the same email copy and design produced different sales depending on whether the frame was gentle ('did you mean to do this?') versus direct ('this is ready for you — check it out and buy').
- In the source's abandoned-cart example, the two variants had near-identical opens (68% vs 69%) but very different place-order rates (11.6% vs 3.8%) and clicks (14% vs 6.8%) — treat these as one case, not a benchmark.
- Configure your ESP test (e.g. Klaviyo A/B) to select the winner on revenue or place-order rate, not open rate, since opens can look equal while revenue diverges sharply.
- Review results per email type: the frame that wins on a cart email may not be the frame that wins on a launch.
Caveat: The presenter's claim that subject lines don't matter for opens is his opinion; he still writes them carefully because they move sales.
Caveat: Single-case numbers are illustrative examples, not predictions.

Tags: email-lifecycle, subject-lines, experiment-design, measurement, cart-recovery, conversion-optimization
Source: Ecommerce Email Marketing 2025.docx

---

## Subject line framework: 2–5 words, title case, curiosity loop
Use when: Drafting subject lines for any store campaign — launches, restocks, promos, educational sends.
- Keep it to 2–5 words so the notification is scannable while the recipient is scrolling another app; long sentence-like subject lines get swiped away, per the presenter.
- Use title case because the presenter finds it reads as more official and reports a positive effect on opens.
- End on an open loop: hint at the payoff but withhold it so the only way to close the loop is opening the email (his analogy: a song or movie title you can't recall nags at you).
- Use 1–2 emojis, not on every send: 'A Taste Of Sunshine' (emotional pull), 'Myth. Busted.' (curiosity), 'They're Finally Here' (anticipation), 'It's Literally This Easy' (mild cocky challenge).
- Puns and periods between words are allowed levers — the presenter likes periods for suspense and notes the reviewer's praise for 'Tallow Won't Fix This' / 'the grass-fed elephant in the room' as a strong curiosity pairing.
- Test emoji placement (beginning vs end) rather than assuming; the presenter prefers putting two emojis adjacent when using two.
Caveat: Everything here is the presenter's stated heuristic, not a measured rule; he reports 50–60% opens to engaged lists across his clients.
Caveat: Avoid the overused word 'secret' and don't stack multiple ideas (e.g. restock + sale) unless you can phrase them together.

Tags: email-lifecycle, subject-lines, copywriting, creative-strategy, deliverability
Source: Ecommerce Email Marketing 2025.docx

---

## Preview text framework: support the headline, end with an ellipsis
Use when: Writing preview text for any email where the subject line has already been drafted.
- Treat subject line as headline and preview text as sub-headline; build a visible hierarchy (shorter title-case subject, slightly longer regular-case preview).
- Add new information rather than repeating the subject — the preview should support and extend the hook.
- Use dot-dot-dot endings occasionally; the presenter finds an ellipsis strongly opens loops, but advises not using it on every send.
- Pair examples given: subject 'A Taste Of Sunshine' with preview 'This wasn't supposed to be made but now it's a bestseller...'; subject 'Myth. Busted.' with 'If you want the cold hard facts we got them...'; subject 'It's Literally This Easy' with 'No one is talking about this but it will make you more money...'.
- For restocks, pair 'They're Back' with 'And they're on sale for now' — the 'for now' adds urgency while the preview reveals the sale the subject omitted.
- Leave something withheld: the presenter criticizes previews like 'add this to your packing list' as lame and would move product/news detail into the preview while keeping the subject open-ended.
Caveat: The presenter explicitly says not to overthink preview text; content quality and cadence are the primary drivers.
Caveat: The 50–60% open figure is his agency's reported engaged-list average, not a universal expectation.

Tags: email-lifecycle, subject-lines, copywriting, preview-text, creative-strategy
Source: Ecommerce Email Marketing 2025.docx

---

## Build urgency and holidays into seasonal campaign angles
Use when: Planning a promo or content email with no launch hook — e.g. a nut-bar brand needing a July send.
- Ask an AI assistant for obscure or relevant holidays for the upcoming month to generate campaign topics (the demo used National Coconut Day for a coconut bar).
- Tie the product directly to the occasion so the email reads naturally rather than as a generic sale blast.
- Add urgency in preview text when inventory is genuinely constrained: the reviewed example 'Some SKUs already closed. Get yours now.' was praised for urgency.
- Note that sale-with-restock emails combine two messages; the presenter considered it acceptable only when phrased as one idea ('They're Back / And They're On Sale For Now').
- For travel or summer positioning, use simple seasonal framing ('Vacation Time') but push the specificity into the preview; the presenter found 'Trusted For Travel' too thin and rewrote it toward a benefit claim the reader has to open to verify.
Caveat: Holiday-driven emails work only if the product connects — forced occasion tie-ins read as filler.
Caveat: Don't claim scarcity ('some SKUs already closed') unless it is true.

Tags: email-lifecycle, campaign-planning, promotions, urgency, creative-strategy, seasonal
Source: Ecommerce Email Marketing 2025.docx

---

## Diagnose and fix weak inbox subject lines
Use when: Reviewing your own scheduled campaigns before send, or auditing past sends to improve format.
- Cut long descriptive subject lines: 'All New Summer Hiking Essentials' was judged too long; suggested replacing with a punchy repeat like 'New New' and pushing the product list into preview text.
- Lead with the strongest word or concept, not the category: the presenter would make 'The Sale?' the subject and 'Red White And All You...' the preview for a July 4th send, since 'Americana inspired favorites' was unnecessary.
- Make short subject lines work with a longer preview: two-word subjects pair well with five-plus-word previews for visible hierarchy.
- Don't capitalize seasons; 'built for summer' should read 'Built For Summer' under his title-case convention.
- Avoid flat previews with no hook ('The perfect sun hoodie'); instead end with a metaphor or pun plus ellipsis.
- Watch subject-line craft details: he dislikes two emojis split apart, all-caps used without reason, and overused words like 'secret'.
Caveat: These are the presenter's stated preferences and style conventions, not tested rules; he recommends testing emoji placement and phrasing for your own list.
Caveat: A/B results vary by audience and list engagement.

Tags: email-lifecycle, subject-lines, creative-strategy, copywriting, email-audit
Source: Ecommerce Email Marketing 2025.docx

---

## Prioritize content quality and cadence over subject-line tricks
Use when: Deciding how much effort to invest in subject-line optimization versus email content and send frequency.
- Build the presumption of opening: send content good enough that recipients open on sender name, then associate that experience with the next send (the presenter compares it to a creator whose audience watches regardless of title).
- Keep cadence consistent enough that subscribers expect you multiple times a week, similar to newspaper-reading habits — the source's stated goal is conditioning.
- Accept that subject line and preview text still exist to drive sales, so continue testing them on revenue even under this philosophy.
- When auditing a campaign that underperforms, first check whether the underlying offer/content is worth opening before blaming subject lines.
Caveat: The 'subject lines don't matter' position is explicitly the presenter's opinion and may conflict with standard deliverability practice; he still writes and tests them.
Caveat: Multiple weekly sends require enough content substance and list tolerance — not validated for every list size or niche in the source.

Tags: email-lifecycle, retention, send-cadence, content-strategy, subject-lines, list-health
Source: Ecommerce Email Marketing 2025.docx

---

## Rewrite subject lines as curiosity gap, then judge them by sales
Use when: Writing or testing the subject line and preview text for a campaign email, especially a new product or back-in-stock send.
- Aim for curiosity so the reader has a reason to click. A worked example: a tallow product email subject framed as 'Tallow won't fix this' followed by the preview text 'the grass-fed elephant in the room' — the presenter called this a strong example because it appears to talk down the product, then hints at an unresolved 'elephant in the room'.
- Write preview text as a continuation of the hook, not a repeat of the subject line. Example given: subject references vacation time, preview reads 'add this to your packing list...' to keep the reader wanting more.
- Don't overthink the mechanics. The presenter's position is that if you send good content, people open regardless of the specific subject line and preview text.
- Judge subject lines and preview text on sales rather than opens, and test what works for your own list. This is the presenter's stated rule, not a universal benchmark.
- Note that sender name also drives opens, so keep it recognizable.
Caveat: The 'send good content and people will open anyway' claim is the presenter's opinion, not a tested universal rule.
Caveat: Testing on sales instead of opens is a slower validation loop and needs enough volume to read.
Caveat: The tallow example is a demonstration the presenter invented live, not a measured result.

Tags: email-lifecycle, subject-lines, preview-text, copywriting, experiment-design, measurement, campaigns
Source: Ecommerce Email Marketing 2025.docx

---

## Design ecommerce emails in Figma instead of Canva
Use when: Setting up the design tooling and file structure for a store's recurring email design workflow.
- Choose Figma over Canva. The presenter states Canva is too simplistic and hard to organize, and that Figma can be just as simple while producing better emails and offering extra capabilities.
- Work at a fixed email width of 600px. Build sections as frames at that width so slices export cleanly later.
- Ignore most of Figma's feature surface — the presenter estimates roughly 90% of what you see is unused. Rely on shapes, text, image fills, gradients, alignment tools and slicing.
- Use the layers panel to select and edit nested elements. Selecting a layer highlights the corresponding element on canvas and exposes its properties (e.g. setting a logo width).
- Hold the format-appropriate modifier key when cropping images inside a frame (the presenter uses command) so a hero image can be reduced, e.g. to 600x500, without breaking the layout.
Caveat: Recommended tooling, not a measured conversion result.
Caveat: The 600px width is the presenter's convention; verify against current email client rendering.

Tags: email-lifecycle, email-design, figma, design-workflow, creative-production
Source: Ecommerce Email Marketing 2025.docx

---

## Write email copy as a layout brief before design starts
Use when: Briefing an email design (in-house or freelance) for any campaign or flow, to avoid rework between copy and layout.
- Instead of listing 'headline / body / CTA' abstractly, write the copy in the order and shape of the intended email sections so the layout is implied.
- For a back-in-stock email, the layout brief looked like: 'back in stock / they're back' headline, a small block of body copy, a button, a graphic, a core-values block, then fan favorites and bestsellers listed.
- The presenter's reasoning: as a former copywriter, emails would turn out very differently from what was imagined, so laying it out gives more control and gives designers a starting point rather than a blank canvas.
- Designers appreciate it because starting from nothing is hard; the brief becomes the scaffolding.
- Pair this with a Figma template library so the shape in the brief maps to an existing section.
Caveat: This is a process recommendation from the presenter's agency, not an A/B tested outcome.

Tags: email-lifecycle, copywriting, email-design, briefing, design-workflow
Source: Ecommerce Email Marketing 2025.docx

---

## Build a reusable email section template library
Use when: Producing email campaigns or flows regularly and wanting to cut design time while keeping section quality consistent.
- Create a template file containing multiple variants of hero sections, bridge sections and product sections. The presenter's file labels them e.g. 'hero section 7', '3', '2'.
- Each hero template contains a headline, body copy, a button and a graphic slot — the standard hero anatomy used in the walkthrough.
- When starting a new email, pick a matching template, paste it in, and use it as the reference while building the rest.
- Keep the template library separate from the working email file so variants aren't accidentally edited in place.
- The presenter offers these templates via newsletter signup; the mechanism matters less than maintaining your own consistent variants.
Caveat: Only three section types are described (hero, bridge, product); extend the library to cover your own recurring sections.
Caveat: Template reuse risks visual sameness — the source separately warns that identical layouts every send erode attention.

Tags: email-lifecycle, email-design, figma, design-workflow, creative-production, templates
Source: Ecommerce Email Marketing 2025.docx

---

## Gradient overlay to place text over a hero image without covering faces
Use when: Building an email hero where the photo is the background and copy must sit on top of it.
- Set the hero image to 600px wide and align it to the frame.
- Identify where text will sit and check it won't cover faces — in the walkthrough the subject's faces were in the upper area, so text was pushed lower.
- Add a rectangle at 600px width over the image, fill it black, and drag it so it blends into the photo.
- In the fill settings, switch to the gradient tab. Change direction from side-to-side to top-to-bottom.
- Set the bottom gradient stop to fully transparent and keep the top stop black, so the overlay fades from solid at the top into the image at the bottom.
- Adjust stop positions until the transition is smooth, then place headline and body copy on top.
- Set the hero frame to roughly 600x500 so the next section isn't pushed far down the scroll.
Caveat: Long hero sections force a long scroll before the next section — the presenter cropped the hero down for that reason.
Caveat: Figma gradient controls may change; verify the current interface.

Tags: email-lifecycle, email-design, figma, hero-section, creative-production
Source: Ecommerce Email Marketing 2025.docx

---

## Build a CTA button with a rounded rectangle and correct layer order
Use when: Creating the primary CTA in an email hero or section where no button template exists.
- Draw a rectangle, set corner radius (the presenter used ~65 initially) and increase corner rounding to get a pill shape.
- Set the button fill to contrast with the section — white on the dark hero, black on white sections.
- Add a text layer for the CTA label, e.g. 'shop best sellers' or 'shop now', and center it.
- If the label is hidden, it's a layer-order problem: move the text above the rectangle in the layers panel so it renders in front.
- Adjust button size and weight after placement rather than before; the presenter resized and bolded iteratively until it looked right.
Caveat: No specific button size is established as a best practice — sizing was tuned by eye.

Tags: email-lifecycle, email-design, figma, call-to-action, creative-production
Source: Ecommerce Email Marketing 2025.docx

---

## Put the first CTA button above the fold and keep buttons large
Use when: Restructuring an underperforming email template, or reviewing an existing template's CTA placement and button sizing.
- Check where the first button appears in the rendered email. In the Whoop teardown the first button sat very far down the email, so an opener would have to scroll substantially before being able to click — the presenter says this impairs click rates and ultimately sales.
- Move a prominent button into the hero so every opener sees it without scrolling. In the redesigned Whoop email a large button sits at the very top.
- Remove the top-of-email navigation row (Shop Women / Shop Men / category links). The presenter states that four or five buttons immediately on open overwhelm the reader, hurt conversions, and increase churn. Move navigation into the footer instead.
- For Birkenstock, an audience with a significant older demographic, increase font sizes and button sizes. The presenter's framing: make the buttons big enough that 'even a blind person could click these'.
- Use only one or two calls to action per email. The Birkenstock original had shop now, sign up for catalog, follow on Instagram, sign up for free membership, tag us on Instagram, and recommendations all in one email.
Caveat: These are the presenter's conversion principles based on agency experience, not controlled test results. Treat 'four or five buttons overwhelm' as a heuristic to test on your own list and audience.
Caveat: Accessibility framing about font and button size is a design heuristic, not a formal accessibility standard.

Tags: email-lifecycle, email-design, call-to-action, conversion-optimization, campaigns, creative-strategy
Source: Ecommerce Email Marketing 2025.docx

---

## Give every product its own Shop Now button, or at minimum underline the product name
Use when: Laying out a product grid or multi-product section in a campaign email.
- Add an individual Shop Now button to each product shown. The presenter's rule: each item gets its own link so the customer knows they can click through to that specific product page.
- If individual buttons aren't feasible in the layout, at minimum underline the product name so it reads as clickable. The Alo teardown found product tiles where it was unclear whether items were clickable at all.
- Make the clickable element the anchor for the destination link when slicing (each image export carries only one link, so the button and the product photo must be separate slices if they point to different URLs).
- Don't overload product tiles with copy. In the Gymshark walkthrough the presenter judged the email already had enough information and chose a lean tile: product image, product name, a short descriptor, a review count, and a Shop Now button.
Caveat: The presenter frames the underlining fallback as clearly weaker than a real button.
Caveat: No measured click-rate uplift is provided for either approach.

Tags: email-lifecycle, email-design, product-page, call-to-action, campaigns, merchandising
Source: Ecommerce Email Marketing 2025.docx

---

## Add review counts and short product descriptors to fill out product tiles
Use when: Designing or refreshing a multi-product email section that currently looks sparse.
- Insert a star icon and the review count for highly rated products. In the walkthrough the item was labeled with a rating such as 4.3 alongside a star graphic.
- Lock star icon proportions before resizing. In Figma, changing width alone distorts a star; enable proportional scaling so width and height change together.
- Add a short attribute line under the product name, e.g. 'light support' for a sports bra. Use lowercase or sentence case rather than all caps — Figma's text panel has an option to control case ('as typed' vs all caps).
- Style the attribute in a smaller size and a gray color so it reads as secondary to the product name, then adjust spacing so tiles stay aligned.
- The presenter's reasoning: the section looked bare, and review counts plus a small attribute add depth and information 'but not too much'.
Caveat: Review counts are used as a credibility signal; only display real review figures from the storefront.
Caveat: Exact tile content should be tested per brand — this is one worked example.

Tags: email-lifecycle, email-design, social-proof, product-page, merchandising, figma
Source: Ecommerce Email Marketing 2025.docx

---

## Build a visual theme and repeat it across sections for depth
Use when: An email section or whole campaign design reads as flat, two-dimensional or off-brand.
- Diagnose flatness. On the Gymshark core-values section the presenter said it looked 'two-dimensional' — a plain white background with no depth.
- Add soft gradients behind text blocks: draw a rectangle at 600px, place it behind the text, and set a gradient from a light gray into white or transparent, top-to-bottom to soften the block edge.
- Apply the gradient block one subgroup at a time rather than across the whole section — the presenter tried behind everything, then chose to go block by block.
- Carry a motif across sections. In the Gymshark build, thin black divider lines used in the core-values section were reused beside product images and in the product section to create depth and tie the email together.
- Vary backgrounds between sections (the walkthrough alternated a dark hero with a white core-values section) so sections are visually distinguishable and the email isn't uniformly dark.
Caveat: Gradient tuning was done by eye; the presenter adjusted stop position and lightness repeatedly before settling.
Caveat: The presenter notes brand-fit was uncertain for a Birkenstock redesign, showing that a modern restyle can conflict with brand guidelines.

Tags: email-lifecycle, email-design, figma, creative-strategy, brand-consistency
Source: Ecommerce Email Marketing 2025.docx

---

## Use layering and grouping to keep long email files navigable
Use when: Managing a large email design file that spans multiple sections and will need edits or reuse.
- Wrap the whole email in a single frame at the target width (600px) and name it after the brand, e.g. 'gymshark email'. Extend the frame height to make room as you add sections.
- Group all layers belonging to a section into one group and name it by section: 'logo', 'hero section', 'bridge section'.
- Within a section, group sub-elements further — the walkthrough grouped button elements into a 'button' group and renamed layers to 'headline' and 'subheadline'.
- Order the groups top-to-bottom to match the email reading order so the layer tree mirrors the rendered email.
- Do this as you build, not retroactively. The presenter admits skipping organization, then had to go back and clean it up.
Caveat: Purely a file-management practice; no conversion implication.

Tags: email-lifecycle, email-design, figma, design-workflow, creative-production
Source: Ecommerce Email Marketing 2025.docx

---

## Close with a general Shop Now CTA after the product section
Use when: Finishing any email that displays a grid or list of specific products.
- After the individual product tiles, add one general CTA such as 'shop best sellers' or 'shop all tops'.
- The presenter's rationale: the reader might not want any of the shown products but still wants to browse, so give them a general route — 'always always always' end product sections this way.
- Center and align the button with the rest of the section, and adjust section background height as needed.
- Where relevant, echo the CTA language used at the top of the email so the email bookends around a single shopping action.
- In the Alo redesign, the product section closed with a general 'shop all tops' CTA plus a brand line ('experience the Alo difference').
Caveat: The 'always' framing is the presenter's rule of thumb, not a tested law.

Tags: email-lifecycle, email-design, call-to-action, conversion-optimization, merchandising
Source: Ecommerce Email Marketing 2025.docx

---

## Build a footer with category shopping links plus trust icons
Use when: Designing or revising the standard footer block used across all campaign and flow emails.
- Add shop-by-category links in the footer. The presenter argues this generates a large volume of clicks because readers who reach the bottom may not want the featured items, and the footer gives them somewhere to go instead of leaving.
- Instead of separate emails segmented by gender, place two footer entries such as 'Women' and 'Men' so any email can serve both audiences. In the walkthrough these were rendered as labeled line sections rather than buttons.
- Include social media icons in the footer so every email carries a follow path.
- Include social proof / service icons. The Gymshark footer reused Afterpay, Klarna, free shipping or free returns, and world class support icons — screenshotting and reusing the brand's existing icons is the pragmatic route the presenter used.
- Keep the footer visually cleaner than the body and align the category columns. The Birkenstock redesign laid categories in a column or two columns; the presenter states this performed better.
- Add unsubscribe and legal blocks in the ESP (Klaviyo handles this) rather than designing them in Figma.
Caveat: 'You get a ton of clicks' from footer buttons is the presenter's observation from agency work, not a published benchmark.
Caveat: Trust badge icons must reflect services your store actually offers.

Tags: email-lifecycle, email-design, footer, retention, social-proof, campaigns
Source: Ecommerce Email Marketing 2025.docx

---

## Vary layout, imagery and copy between sends to prevent subscriber fatigue
Use when: Planning an email calendar and choosing which template or layout each campaign will use.
- Audit recent sends for sameness. The presenter pulled four random Gymshark emails that used the same layout every time and called this out as the easiest way to lose attention and subscribers.
- Vary layout, colors, themes and copy per send — the presenter's framing is that subscribers want novelty and varying 'dopamine'.
- Match email imagery to the brand's social channels. The Gymshark emails used studio-only product photography while their Instagram was full of people and life, creating a disconnected experience; the redesigned emails used lifestyle imagery instead.
- Build dedicated value and social-proof emails alongside promotional ones. Examples shown: a testimonial email ('by gym lovers for gym lovers') with verified review counts and a testimonial carousel, and a blog-style email breaking down dumbbell back exercises.
- Include a shop path even in non-promotional emails (blog, educational) so a reader who wants to buy can do so without leaving the email journey.
Caveat: The claim that repetition loses subscribers is the presenter's assertion, not a measured churn study.
Caveat: The redesigned examples were made by the presenter's team from public assets; no revenue results are reported here.

Tags: email-lifecycle, email-design, creative-strategy, retention, campaigns, content-marketing
Source: Ecommerce Email Marketing 2025.docx

---

## Shift CTA copy from 'learn more' to a concrete value proposition
Use when: Rewriting email hero copy and CTA labels for an offer-driven email.
- Identify the concrete thing the customer receives. For Whoop it was a free month trial — you can get a device sent to you and use it for a month, so that is what the presenter centered the CTAs on.
- Rewrite 'learn more' CTAs. The presenter's argument: nobody wants to learn more, they want to be given something.
- Show the value proposition directly in the hero rather than only listing features. The original copy ('discover how Whoop outperforms other wearables') listed features; the rewrite led with the offer.
- Repeat the offer at the bottom of the email as a reminder, after the design has carried the reader down.
- Keep tone matched to the audience — the presenter rewrote a line into a modern reference ('they not like us' / 'there's levels to this') to appeal to the audience of the moment, admitting brand-fit risk.
Caveat: The tone-matching rewrite is unvalidated; the presenter notes uncertainty about whether such a restyle matches brand guidelines.
Caveat: No conversion lift is reported for the copy changes.

Tags: email-lifecycle, copywriting, call-to-action, offer-design, conversion-optimization, landing-page
Source: Ecommerce Email Marketing 2025.docx

---

## Use vertical stacking over side-by-side layouts in email copy
Use when: Building a bridge or comparison section that contrasts the brand against competitors or alternatives.
- Take comparative copy out of side-by-side columns and stack it vertically. The presenter states that going back and forth is hard for the customer and that vertical layouts performed better in their work.
- Use this in bridge sections. The Whoop redesign used a bridge contrasting the competitor and the brand: 'they give you numbers, we give you insights'.
- Keep vertical blocks short and highly readable — the presenter described the goal as making it 'super easy to read'.
- Pair the vertical block with a background transition (the Whoop redesign used a transition over the section) to make the section feel immersive like the brand's site.
- Reserve the hero for the biggest share of design attention — the presenter's position is that about 75% of attention should go to the hero section.
Caveat: The '75% of attention on the hero' figure is the presenter's heuristic, not a measured metric.
Caveat: The vertical-layout preference is an observation from the presenter's work, not a controlled test.

Tags: email-lifecycle, email-design, copywriting, creative-strategy, campaigns
Source: Ecommerce Email Marketing 2025.docx

---

## Slice an email design into separate export images, one link each
Use when: Preparing a designed email for uploading into an ESP as a stack of image blocks.
- Use Figma's slice tool: highlight the region you want, position the slice precisely, then export it. Repeatedly copy and paste the slice, aligning each new slice to where the previous one ended.
- Split any region that needs a different link into its own slice. Each uploaded image can carry only one link, so a row containing multiple buttons must be sliced apart for each destination.
- Split product tiles individually so each product is separately clickable.
- Keep slices from being too large. Oversized image files load slowly in the ESP and in the recipient's inbox.
- Slice social icons into separate exports — in the walkthrough Facebook, Instagram and Pinterest each got its own slice.
- Export at 2X and as JPEG in the walkthrough; verify export options in the current Figma interface since these settings can change.
Caveat: A purely image-based email trades layout fidelity for editability — copy can't be edited in the ESP without a new export.
Caveat: Slice boundaries must align exactly or sections will show seams.

Tags: email-lifecycle, email-design, figma, image-optimization, esp, klaviyo
Source: Ecommerce Email Marketing 2025.docx

---

## Compress exported email images in a batch before uploading
Use when: After slicing an email design and before building the campaign in the ESP.
- Batch-upload all slices to a compressor at once. The presenter used iloveimg.com's compress image tool.
- Read the before/after figures. In the walkthrough a batch went from 1.72 MB to 327 KB — roughly an 80% reduction — and the tool had already downloaded the compressed set for re-upload.
- Upload the compressed files, not the originals, into the ESP.
- The presenter's stated reason for compressing is load speed inside the ESP and in the inbox, which connects to deliverability hygiene.
- Combine this step with careful slicing so no single slice is large in the first place.
Caveat: Compression settings and tool behavior change — verify the current interface and check quality after compressing.
Caveat: The 1.72 MB to 327 KB result is a single example, not a guaranteed reduction ratio.

Tags: email-lifecycle, image-optimization, deliverability, klaviyo, creative-production
Source: Ecommerce Email Marketing 2025.docx

---

## Assemble the sliced email in Klaviyo and attach links and alt text
Use when: Building the actual sendable campaign from exported image slices in Klaviyo or a comparable ESP.
- Create a campaign, choose the sending list, and use a blank email template.
- Delete all default blocks except the unsubscribe/legal footer, since Klaviyo supplies the compliance block.
- Drag an image block in, upload the compressed slices, then duplicate the block repeatedly and replace each with the next slice in order.
- Upload images directly rather than pulling from image URLs so each block can take its own link.
- For the social icon row, insert a table block instead of stacked images. Change the cell content type to image, add a column so there are as many cells as icons, and set padding to zero so icons fill the cell.
- Paste the destination URL into each image's link address — the logo to the homepage, each product button to its product page, category buttons to their collection pages.
- Add alt text where it helps. The presenter's position is that alt text is barely used because image blocking is very rare, but they still add descriptive text mirroring the copy (e.g. 'they're back') so an image-less reader can follow.
- Send yourself a preview and click through every link before sending. The presenter notes ESP interfaces change, so verify the current block and table settings in Klaviyo.
Caveat: The 'image blocking is very rare' characterization is the presenter's own view — verify against your list's client mix before deprioritizing alt text.
Caveat: Because the email is images, copy edits require re-slicing and a new export.

Tags: email-lifecycle, klaviyo, esp, email-design, deliverability, creative-production
Source: Ecommerce Email Marketing 2025.docx

---

## Keep site and email visual worlds consistent
Use when: Reviewing email templates against the storefront and social presence before a redesign.
- Compare the immersion level of the site against the email. The presenter noted Whoop's site is futuristic and immersive with different colors and transitions, while the email was plain, black and white, and followed the same layout repeatedly.
- Pull brand-appropriate visual elements from the site into the email — color, gradient transitions and graphic treatments — as the Whoop redesign did, and carry lifestyle imagery over from social as the Gymshark redesign did.
- Where brand identity conflicts with a modern restyle, flag it rather than assuming the redesign is correct. The presenter explicitly doubted whether the modern Birkenstock take fitted the brand's guidelines even while demonstrating the conversion principles.
- Use branded backdrops and set pieces rather than plain backgrounds — e.g. a testimonial email with the brand's logos in the background and testimonials over a phone frame.
- Seasonalize imagery for fashion brands. For a November send the Alo redesign used a winter lifestyle photo, with the presenter noting images are changed by season to stay current.
Caveat: No measurement supports the claim that consistency improves conversion; this is a design coherence argument.
Caveat: Modernizing a legacy brand's look can violate brand guidelines — treat the Birkenstock example as a demonstration, not a recommendation to imitate blindly.

Tags: email-lifecycle, email-design, brand-consistency, creative-strategy, merchandising, campaigns
Source: Ecommerce Email Marketing 2025.docx

---

## Redesign browse-abandonment automations to include a top CTA
Use when: Auditing or redesigning a browse-abandonment or recently-viewed automation that fires after a shopper browses a category.
- Check the trigger logic against what fired. In the Alo example the presenter browsed women's tops while shopping for a gift, and an email titled 'trending tops — definitely worth a second look' fired a few hours later, resurfacing tops.
- Verify the email contains at least one CTA. The Alo example had no working buttons at all — no top button and no keep-shopping button at the bottom — which the presenter called out as a serious defect for a large brand.
- Add a CTA button at the top so a distracted shopper returning hours later can continue immediately.
- Make product tiles obviously clickable: individual Shop Now buttons per item, or at minimum underlined product names.
- Fix font color and contrast problems — the presenter flagged a color/font issue in the Alo email that damaged readability.
- Add shop-by-category links in the footer so a shopper who no longer wants the browsed category can pivot to bottoms or other collections rather than abandoning.
- Match imagery to the season and rewrite copy playfully ('serve in your new top', 'grab your new piece') to reconnect with the shopper's context.
Caveat: This is a teardown of the presenter's own triggered sample; the browse trigger logic is inferred, not confirmed from the brand's account.
Caveat: No post-redesign performance data is provided.

Tags: email-lifecycle, browse-abandonment, automations, call-to-action, conversion-optimization, retention
Source: Ecommerce Email Marketing 2025.docx

---

## Use an interactive mix-and-match block to demonstrate outfit combinations
Use when: Building a merchandising email that needs a fresh layout idea for promoting multiple bestsellers together.
- Frame the section around combining products rather than listing them: the Gymshark example used copy like 'mix and match our favorites' and 'back in stock for guaranteed shirt shredding pump'.
- Build the section as a GIF that cycles through different items, so a single slot conveys multiple combinations.
- Follow the interactive block with a final CTA and a shop-by-category footer so the reader has both the featured route and a broader browse route.
- Pair this with an emotional hero (the same email used copy about the gym as a sanctuary and sweat drowning out doubt) to differentiate the send from standard catalog layouts.
- The presenter's stated purpose is variability — giving subscribers a different experience versus a repeating template.
Caveat: GIF support and animation behavior vary by email client; test rendering before sending.
Caveat: No conversion performance is reported for this specific block.

Tags: email-lifecycle, email-design, merchandising, bundles, creative-strategy, campaigns
Source: Ecommerce Email Marketing 2025.docx

---

## Use testimonial and social-proof emails to build trust for later purchases
Use when: Planning a non-discount campaign slot aimed at warming a list or an audience segment that hasn't purchased.
- Build the email around real reviews. The Gymshark example headlined 'by gym lovers for gym lovers' with 100+ verified reviews.
- Lay testimonials over a device frame and bold the key phrases inside each testimonial so skim readers catch the point.
- Place a large CTA button directly beneath the testimonials, before the photo gallery.
- Use a gradient background that fades from a gray tone into white to transition into the closing section without a hard edge.
- Include a photo gallery for branding value even if it isn't directly transactional.
- The presenter's expectation for this format: even if the reader doesn't convert off the email, they accumulate trust so they may buy later. This is a stated intent, not a measured outcome.
Caveat: Only quote real, verified reviews; the 100+ figure comes from the example.
Caveat: The later-conversion claim is the presenter's rationale, not tracked attribution.

Tags: email-lifecycle, social-proof, retention, email-design, campaigns, content-marketing
Source: Ecommerce Email Marketing 2025.docx

---

## Use value and educational emails that still carry a shop path
Use when: Filling a campaign slot with value content instead of a promotion, especially for an audience that buys gear or apparel.
- Base the email on a topic the audience actually searches for. The Gymshark example was built from a blog on dumbbell back exercises you can do without a gym.
- Headline it as a practical guide, e.g. 'top no-fuss dumbbell back exercises', with an aspirational image.
- Break the topic into parts to give genuine value — the example walked through back anatomy ('back anatomy 101') before the exercises.
- Keep shopping paths available: the footer shop-by-category buttons and any in-body product CTAs mean a reader who wants to buy doesn't have to leave the email journey.
- The presenter's rationale for the format is that the footer shop buttons ensure 'even if you're doing a blog email or an educational email' there are still clickable shopping routes.
Caveat: Educational content requires genuine subject-matter accuracy; the source does not address content sourcing or review.
Caveat: No performance data is given for this format.

Tags: email-lifecycle, content-marketing, retention, email-design, footer, merchandising
Source: Ecommerce Email Marketing 2025.docx

---

## Design emails as image slices, then link buttons in Klaviyo
Use when: You have approved email creative in Figma and need to ship it through your ESP (Klaviyo) for a campaign or flow.
- In Figma, use the Slice tool to cut the email into pieces aligned to where links differ (logo, each CTA, product blocks, footer). Export at 2x for quality, JPEG is fine.
- Do not make one giant slice for a long section; oversized image files slow inbox loading. Keep slices roughly small enough that no single image is very large — the source treats ~600px wide sections as the practical outer limit.
- Compress all slices before upload (the video used iloveimg.com; any compressor works). Example from the session: 2.84 MB of slices reduced to 469 KB.
- In Klaviyo, create a campaign/flow email, delete the default blocks, and add image blocks one by one in order, uploading the compressed slices top to bottom.
- Attach links to each image that represents a button so it routes to the correct page (blog, collection, product).
- Keep the footer social/footer text area as editable Klaviyo blocks (not images) so you can change social network links and the unsubscribe link.
- Add a block of real, visible-but-tiny text in the footer (source suggests size 5) drawn from your About Us copy to counteract an image-heavy email looking spammy to Gmail and help deliverability.
- Verify current Klaviyo image-block and campaign interface before executing — UI changes over time.
Caveat: Heavy image-only emails risk deliverability; the hidden/tiny text trick is a source recommendation, not a guaranteed deliverability fix.
Caveat: Email clients may block images; ensure key text is not only inside images where possible.

Tags: email-lifecycle, klaviyo, figma, email-design, deliverability, campaign-production, creative-strategy
Source: Ecommerce Email Marketing 2025.docx

---

## Use a non-discount email strategy: brand, value, social proof
Use when: Planning a campaign calendar or welcome/engagement flow and you want to protect margin rather than default to discount offers.
- Decide the angle per email up front: (1) a branded email carrying your brand voice and best sellers, (2) a value/education email, (3) a reviews/social-proof email.
- For the branded email, lead with a strong tagline tied to the brand (the session used a 'do gym' angle) and tie it into best sellers.
- For the value email, pick a blog post or educational concept that hits a customer pain point (e.g. training at home with dumbbells) and tease the click.
- For the social-proof email, pull real testimonials from your site that overcome objections and span different customer types.
- Promote products subtly throughout so the email does not feel salesy and add sales resistance, while still giving a clear path to buy.
- Find inspiration by scrolling the brand's Instagram and site to mine community language and angles, then carry that into email instead of plain corporate layouts.
Caveat: Non-discount emails aim to protect margin but may convert differently than a discount blast; the source presents this as his preferred approach, not a universal rule.

Tags: email-lifecycle, campaign-strategy, offer-design, retention, brand-voice, social-proof
Source: Ecommerce Email Marketing 2025.docx

---

## Source email angles from your own Instagram and website
Use when: You need campaign angles for a store and want ideas that feel on-brand and content-driven rather than purely promotional.
- Scroll the brand's Instagram to capture recurring community language and recurring phrases (the source noticed the brand treated 'gym' as a verb).
- Turn a repeated phrase or community theme into a tagline you can build a whole email around.
- Check whether the site has a blog and pick a post that addresses a real customer pain point (e.g. home workouts without machines).
- For that post, plan a blog email that teases the click and drives traffic back to the site, where readers can also shop.
- Pull testimonials from the site for a separate social-proof email.
- Note where the brand's email looks corporate/bland versus its livelier Instagram, and set the goal of bringing that life into email.
Caveat: This is a content-mining process, not a performance guarantee; the source's claim that it 'prints cash' is his framing.

Tags: email-lifecycle, content-strategy, social-media, campaign-strategy, customer-research, blog
Source: Ecommerce Email Marketing 2025.docx

---

## Pick email layouts from an inspiration bank of proven brands
Use when: You are laying out a new campaign email and need proven section structures for hero, product, and footer blocks.
- Keep a swipe inbox/folder of emails from brands you follow so you have a bank of layouts and sections.
- Mimic the winning structure for most emails: headline + body copy + button in the hero, especially a 'learn more' button for blog emails.
- Prefer centering the hero button and putting it prominently rather than leaving it small and off to the side.
- Lift section ideas such as a 'mix and match' product block or a 'chest/back anatomy' educational breakdown and adapt the content to your products.
- Keep the CTA goal singular: the source notes you can have many buttons as long as they all push one decision, not several competing ones.
Caveat: Copy the structure and layout, not another brand's copyrighted assets or copy.
Caveat: Button size/placement preferences are the source's tested opinions; test on your own list.

Tags: email-lifecycle, email-design, creative-strategy, campaign-production, layout
Source: Ecommerce Email Marketing 2025.docx

---

## Educate with a product 'bridge' section to justify the price
Use when: Designing product or launch emails where the hero alone just says 'shop our shoes' without explaining why the product is good.
- After the hero, add a bridge/education section that names concrete product features (the source's example: engineered mesh, dura outsole, 4mm lugs).
- Tie each feature to a benefit framed around the customer, not the product in isolation.
- For a content/blog email, use the bridge to summarize and add value (e.g. break down the parts of a muscle and their function) so the email teaches something.
- Keep teasing the click throughout so the reader goes to the site and can shop.
- Use visuals that support the education (labeled images, arrows pointing to parts) to make it feel immersive rather than blocky.
Caveat: Feature-to-benefit claims must be accurate for your product; do not invent specs.
Caveat: The source's specific product specs are examples from one brand, not benchmarks.

Tags: email-lifecycle, product-page, product-education, copywriting, campaign-strategy
Source: Ecommerce Email Marketing 2025.docx

---

## Build product interest with a GIF 'mix and match' section
Use when: Designing a merch/bestseller email where you want to show multiple product combinations without a wall of static images.
- In Figma, create a 600px-wide frame and place the first product pairing image plus a circle/arrows overlay hinting at flipping.
- Duplicate the frame and swap in the next top/bottom combination; repeat so it cycles tops while holding bottoms, then cycles bottoms.
- Select all frames and run a GIF plugin (the source uses one called Gif Canvas) to generate the animated file.
- Insert the GIF into the email design and verify playback in the preview; static Figma won't animate but the exported GIF will.
- Add a 'shop now' button beneath the GIF.
- Centering the GIF and giving it a clean button keeps the section usable across clients.
Caveat: GIF file size matters for load time — keep the animation reasonably compact.
Caveat: Verify plugin availability/behavior since Figma plugins can change.

Tags: email-lifecycle, figma, email-design, creative-strategy, gif, merchandising
Source: Ecommerce Email Marketing 2025.docx

---

## Add texture, gradients, and depth so emails don't look flat
Use when: Your email sections look like flat white blocks and you want to add life and flow without changing the copy.
- Pull a subtle background texture from the brand site and place it behind the hero content, then send it to the back so it doesn't block content.
- Use brand logos/logomarks as faint layered elements to add depth without distracting.
- To blend a gray section into a white footer, create a full-width rectangle, apply a linear gradient, set the top stop to the section color and the bottom stop to white so it flows.
- Use a background-removal plugin to cut a subject out of a photo, then place large outlined type behind the subject for a layered hero effect.
- Apply drop shadows to make photographic elements stand out (the source nudges the shadow offset sideways for depth).
- Use white/outlined text over dark image areas and add a black-to-transparent gradient behind text to keep it readable.
Caveat: Layering and gradients add file size; compress assets before upload.
Caveat: Verify current plugin names/behavior before relying on them.

Tags: email-lifecycle, figma, email-design, creative-strategy, visual-design
Source: Ecommerce Email Marketing 2025.docx

---

## Reduce thumb stretch: size and place CTAs for mobile taps
Use when: Placing buttons in an email hero or product section and deciding size and position for mobile readers.
- Avoid small buttons in the top-left corner: the source notes a right-handed thumb has to stretch to reach it, and says this measurably hurts conversions.
- Make the primary CTA large enough to be unmissable (the source jokes even a blind person would see it).
- Center the hero button and place it prominently rather than burying it.
- Underline text links or use a clear 'shop now' button — the source says he has A/B tested this consistently and clicks rise when links are underlined or buttons are explicit.
- Vary button placement occasionally so readers don't get the same layout every email, while keeping the key CTA prominent.
- Give each product block its own shop-now button, then a general CTA for shoppers who don't want the featured items.
Caveat: The thumb-reach and underline claims are the source's tested opinions; validate for your audience.
Caveat: Button sizing should be checked against your template/rendering across major clients.

Tags: email-lifecycle, conversion-optimization, email-design, checkout, mobile
Source: Ecommerce Email Marketing 2025.docx

---

## Give a fallback general CTA plus shop-by-collection at the bottom
Use when: An email features specific products or a niche angle (e.g. yoga) and you want it to convert non-targeted subscribers too.
- After listing featured products with their own CTAs, add a general 'shop now' so people who don't like those exact items can still browse.
- At the bottom, add shop-by-collection/category links (the source's example used running, workout, casual, yoga) so subscribers not doing that activity still have options.
- For activity-specific emails, add a line broadening the relevance (e.g. 'style doesn't stop at the mat') and show products plus testimonials.
- End with a large category CTA.
- Keep the email working for the whole list, not just the segment the angle targets.
Caveat: More CTAs risk diluting the message; the source argues it's fine as long as they point to one overall decision (shopping).

Tags: email-lifecycle, conversion-optimization, campaign-strategy, email-design, merchandising
Source: Ecommerce Email Marketing 2025.docx

---

## Use big aggregate review counts as a trust signal in emails
Use when: Building a social-proof or reviews email, or adding a trust section to a product email.
- Use the aggregate verified-review figure (the source's example displayed '100,000+ verified reviews') as a big selling point instead of a precise small number.
- Hand-pick testimonials that overcome specific objections and span customer types (the source made sure to include male and female reviewers).
- Bold the main points inside each testimonial so the value reads at a glance.
- Present testimonials visually (the source put them in framed text boxes on a phone graphic, with star icons made from shape tools).
- Frame the email personally with a headline like 'by gym lovers for gym lovers' to counter a corporate feel.
- Add a lifestyle photo gallery plus shop-now at the bottom to add life without overwhelming the reader.
- Keep it simple: the source skipped featuring products in the social-proof email, focusing on trust, then a shop button.
Caveat: The source states testimonials 'always help' based on testing for large brands; that's his opinion, not a universal result.
Caveat: Display only review numbers you can substantiate.

Tags: email-lifecycle, social-proof, conversion-optimization, email-design, trust, retention
Source: Ecommerce Email Marketing 2025.docx

---

## Write blog emails that sell the click and teach on the way
Use when: Sending a blog/content email to drive site traffic and downstream purchases.
- Lead with headline + body copy + a 'learn more' button at the top so the click is easy.
- Tease the content and sell the click in the body (the source framed it as a short list, e.g. 'top 5 dumbbell back exercises').
- Add a bridge section that gives real value inline — summarize and break down the topic (the source used a 'back anatomy 101' breakdown of muscle parts and functions) so the email isn't just a teaser.
- Connect each educational element back to the blog and site so readers who go deeper can shop.
- Include multiple 'learn more' reminders down the email and end with product photos plus the CTA.
- Use benefit/motivational copy to sell the click (the source emphasized the exercises work with minimal equipment and space, for busy-gym-to-small-living-room use).
Caveat: Multiple CTAs are fine here because they all point to one action (reading the post); don't mix in competing goals.
Caveat: Keep the inline education accurate and consistent with the linked post.

Tags: email-lifecycle, content-strategy, copywriting, campaign-strategy, blog, conversion-optimization
Source: Ecommerce Email Marketing 2025.docx

---

## Lay out copy section-by-section before designing
Use when: Starting a new campaign email and you want copy organized before touching the design tool.
- Lay out the email in a doc as distinct sections (headline, body, button, bridge, product block, footer) so you can see the structure.
- Write each section's copy against that plan, matching the winning hero pattern (headline + body + button).
- For brand-voice body copy, prompt an AI with the brand's voice and the desired tone (the source asked for two sentences in the brand's voice about the gym) and treat the output as a draft to work with, not final.
- Reference successful brands' emails while writing to borrow proven section structures rather than reinventing layout.
- Hand the sectioned doc to a designer with clear labels (e.g. 'insert photo gallery of lifestyle pictures', 'mix and match tops and bottoms') so they know what each block needs.
- Keep a consistent footer across emails with shop-by buttons (e.g. men/women) and social links.
Caveat: AI copy needs brand-voice checking; the source notes you sometimes have to work with the output.
Caveat: This is a production workflow, not a performance claim.

Tags: email-lifecycle, copywriting, campaign-production, brand-voice, ai-tools
Source: Ecommerce Email Marketing 2025.docx

---

## Choose a design tool that supports advanced layout
Use when: Deciding where to design campaign emails and needing layered type, gradients, background removal, and GIF plugins.
- Use Figma for composite/advanced email design: it organizes layers well and supports the plugins needed (background remover, GIF canvas).
- Note that the source rates Canva as good but more basic and harder to organize — fine for simpler emails, limited for advanced effects.
- Start each email with a 600px-wide frame as the canvas.
- Build buttons from a rectangle (set corner radius, e.g. 30) plus a text layer, then color and size them.
- Use shapes, images, text, strokes (outline type), gradients, and effects (drop shadow) to build immersive sections.
- Verify current plugin availability and UI, since Figma plugins and menus change.
Caveat: Tool preference is the source's opinion; use whatever your team can execute well.
Caveat: Plugin-dependent steps may break if a plugin is removed or renamed.

Tags: email-lifecycle, figma, email-design, design-tools, creative-strategy
Source: Ecommerce Email Marketing 2025.docx

---

## Keep the CTA goal singular even with many buttons
Use when: Designing a multi-section email and deciding how many CTAs to include.
- Pick the single action the email should drive (read the post, shop the collection, shop the product).
- Repeat that same CTA down the email (the source used multiple 'learn more' buttons) rather than introducing new, different asks.
- Place CTAs after key sections: hero, education bridge, product blocks, and bottom category links.
- Avoid telling the customer too many different things in one email; competing goals dilute the click.
- Use shop-by buttons in the footer (e.g. men/women) that still funnel toward shopping.
Caveat: This is the source's working rule of thumb, not a tested universal law; monitor your own click-through by placement.

Tags: email-lifecycle, conversion-optimization, email-design, campaign-strategy, cta
Source: Ecommerce Email Marketing 2025.docx

---

## Compress email images to protect load time
Use when: Preparing Figma slice exports for upload to your ESP.
- Export slices from Figma (the source exports at 2x for quality, JPEG format).
- Run all slices through an image compressor before uploading (the source used iloveimg.com).
- Check the size savings: the session went from 2.84 MB to 469 KB with little quality loss.
- Keep each slice reasonably small; avoid one giant image for a long section.
- Upload compressed slices into your ESP and rebuild the email there.
Caveat: Aggressive compression can degrade quality; balance size against visual fidelity.
Caveat: Verify current compressor interfaces as tools change.

Tags: email-lifecycle, email-design, deliverability, performance, figma, klaviyo
Source: Ecommerce Email Marketing 2025.docx

---

## Match email design and copy to the brand's voice
Use when: An email looks bland/corporate compared to the brand's social presence and you want it to feel on-brand.
- Use the actual brand font rather than a default font — the source notes it dramatically brings the design to life.
- Pull real brand assets: logo, colors, background textures, lifestyle images from the brand's own channels.
- Write copy in the brand's voice (the source prompted an AI to write in the brand's voice and then refined it).
- Aim for an immersive, fun feel rather than blocky, plain-white sections.
- Mirror the energy and community language of the brand's Instagram in the email.
- Add life to flat sections with lifestyle imagery and color rather than plain studio product shots.
Caveat: Brand-voice copy from AI must be checked against the brand's actual voice.
Caveat: Visual taste judgments are subjective; the source's '10/10' ratings are his opinion.

Tags: email-lifecycle, brand-voice, email-design, creative-strategy, copywriting
Source: Ecommerce Email Marketing 2025.docx

---

## Footer text block to offset image-heavy emails
Use when: Before scheduling a design-heavy campaign or hero-image email that contains little body copy, when you want to reduce the risk of promotions/spam placement.
- Recognize the pattern the source flags: if an email is mostly images with only a few lines of text, this can look 'fishy' to Gmail.
- Found a campaign that uses almost no text? Compensate by adding a large block of real prose (the source copies a brand's About Us page) at the bottom of the email.
- In the email builder, add a text block at the very bottom, paste the text, and center it.
- Style it to be effectively invisible: set font size very small (the source uses size five), set font color to the same color as the background, and reduce line spacing (the source uses about 5%) so it consumes almost no vertical space.
- Confirm the block is invisible in both desktop and mobile previews before sending.
- Send a test preview to yourself and check layout, links and rendering before scheduling.
Caveat: Presented by the source as a trick it likes to use, not a guaranteed deliverability fix; hidden text can itself be treated as a spam signal by some filters, so treat as an experiment and monitor placement.
Caveat: Only use text you have the right to reuse (the source copies another brand's About page content, which is not advisable for your own commercial emails).

Tags: email-lifecycle, deliverability, email-design, footer, spam-placement, campaign-production
Source: Ecommerce Email Marketing 2025.docx

---

## Link and alt-text pass before a campaign goes out
Use when: Final QA step on any campaign, after copy and design are done and before scheduling the send.
- Walk the email top to bottom and link every clickable element to the correct destination: the source links the main hero to the brand's home page, one section to the blog, and collection sections to the men's and women's category pages.
- Match each link to the section's intent rather than defaulting everything to the homepage.
- Add alt text to each image, briefly paraphrasing the message (the source's example: 'top no-fuss dumbbell back exercises').
- Note that image blocking affects a very small share of recipients (source says under 1%), so alt text is secondary but quick to add.
- Send yourself a test email and click every link, then check desktop and mobile rendering.
- Only then schedule or send the campaign.
Caveat: The source states alt text may sometimes help deliverability but is 'really not a big deal' — don't treat it as a major ranking lever.
Caveat: Exact button locations and preview options in your ESP may change; verify in the current interface.

Tags: email-lifecycle, email-qa, links, alt-text, test-send, campaign-production
Source: Ecommerce Email Marketing 2025.docx

---

## Treat deliverability as a sender reputation score
Use when: When diagnosing why campaigns aren't being seen, or when deciding whether low revenue is a content problem or a placement problem.
- Frame deliverability as your domain/IP 'credit score' — the question is whether you land in primary, promotions or spam.
- Understand the provider's incentive: inbox providers only surface emails users want so users keep using the platform; they watch engagement as the signal.
- Use open and click engagement as the practical proxy: if few people open or click, providers push you toward promotions or spam, which further reduces visibility — a self-reinforcing cycle.
- Check the technical layer first: the source says if your ESP (e.g., Klaviyo) shows no warning at the top of the homepage about domain setup, assume technical requirements are already in place.
- If technicals are fine, split the cause into two: either your emails are weak, or your sender reputation is poor and you are being filtered.
Caveat: The credit-score framing is the source's analogy, not an official metric.
Caveat: The source's claim that a clean ESP dashboard means you're fine is a simplification — authentication and domain setup still deserve a direct check.

Tags: email-lifecycle, deliverability, sender-reputation, spam-placement, engagement, diagnostics
Source: Ecommerce Email Marketing 2025.docx

---

## Improve the emails before chasing technical fixes
Use when: When open rates are low and you're tempted to look for technical hacks instead of fixing the content your list receives.
- Accept the source's framing: low engagement has two causes — emails people don't want to open, or poor sender reputation from placement.
- Attack the content side first: the source calls sending better content the number-one lever it sees for deliverability gains.
- Avoid the templated look: the source warns against 'send the same templated BS' where you drop a product into a template in five minutes with no clear value to the reader.
- Instead vary the topic and format each send so opening gives a small reward — the source describes this as a dopamine loop where a good past email makes the next open more likely.
- Use a clean design and genuinely good copy, and give people a reason to look forward to the send.
- Keep the format varied (the source sends different topics and layouts rather than one repeated template).
Caveat: This is the presenter's opinion grounded in agency experience, not a controlled benchmark.
Caveat: Improved content still won't help if authentication and reputation basics are broken.

Tags: email-lifecycle, deliverability, content-quality, engagement, email-design, retention
Source: Ecommerce Email Marketing 2025.docx

---

## Build 14/30/60/90-day engaged segments
Use when: Setting up the segment structure before running a deliverability recovery, or before deciding who should be in your base sending list.
- In your ESP segment builder, create four segments keyed on recency: opened or clicked in the last 14, 30, 60 and 90 days.
- Include an OR condition: opened email at least once in the window OR clicked email at least once in the window — the source adds this because click tracking can register without an open being logged.
- Add a subscribed condition so only marketable contacts are included.
- Add a condition requiring zero bounced emails.
- Repeat the same structure for each window so the segments nest: 14-day inside 30-day inside 60-day inside 90-day.
- Use these four segments as the gating logic for every campaign you send during recovery.
Caveat: The source notes click tracking can be unreliable in some ESPs, so the OR condition is a fail-safe rather than a perfect measure.
Caveat: Window lengths are the source's heuristics; adapt to your list size and send frequency.

Tags: email-lifecycle, segmentation, deliverability, engagement, list-hygiene, klaviyo
Source: Ecommerce Email Marketing 2025.docx

---

## Six-week deliverability recovery protocol
Use when: When campaigns are landing in spam/promotions and you want a structured plan to regain primary inbox placement.
- Weeks 1–3: build the 14/30/60/90-day engaged segments, and turn off all automated flows except the high-engagement ones — welcome, browse abandon, cart abandon, checkout abandon and post-purchase. The source argues these are opened at a high clip (people want their discount, their cart reminder, their order info) and therefore boost credibility.
- Weeks 1–3 onward: send three highly engaging campaigns per week to only the 14-day engaged list. The source argues sending one per week just stretches the same recovery over three times as long.
- Expand only when earned: once the 14-day segment is consistently at 50%+ opens for three straight campaigns, add the 30-day segment at three sends per week.
- Weeks 5–6: keep monitoring opens; if you dip below roughly 40–50%, tighten back to the smaller segment.
- Continue expanding to the 60-day segment as opens hold near 50%, then to the 90-day segment.
- Week 6+: treat the 90-day engaged list as your base sending list, and send one campaign per month to the full newsletter list to try to re-activate dormant contacts.
Caveat: The 40–50% and 50%+ thresholds and the three-per-week cadence are the source's own heuristics from agency work, not industry standards.
Caveat: Opening to the full list monthly works only if that campaign is genuinely engaging; the source says it can just be a normal email.
Caveat: The source states its main client case went from the 20–30% open range to about 60% opens after roughly 60 days — a single example, not a promise.

Tags: email-lifecycle, deliverability, warming, segmentation, cadence, recovery-protocol
Source: Ecommerce Email Marketing 2025.docx

---

## Keep only high-engagement flows during recovery
Use when: Deciding which automations to leave running while rebuilding sender reputation, or which flows to prioritize when you can't build everything at once.
- Turn off all flows except: welcome, browse abandonment, cart abandonment, checkout abandonment and post-purchase.
- Keep the welcome flow because contacts just opted in for a discount and will open the first email delivering it.
- Keep cart and checkout abandonment because the reminder about an item they were already considering earns strong engagement.
- Keep post-purchase because customers want order information.
- Understand why this matters during recovery: every send that gets opens and clicks is a vote of confidence with providers; flows generate those votes without needing new campaign content.
- Re-enable the remaining flows once engagement and placement have recovered.
Caveat: This is the source's recommended recovery posture, not a claim that other flows are worthless.
Caveat: If a flow's own engagement is weak for your brand, including it dilutes the signal you're trying to send.

Tags: email-lifecycle, automation-flows, deliverability, abandoned-cart, welcome-flow, post-purchase
Source: Ecommerce Email Marketing 2025.docx

---

## Three-to-four campaigns per week as your default cadence
Use when: Setting your ongoing campaign frequency after recovery, or testing whether your current once-a-week rhythm is too thin.
- Adopt 3–4 campaigns per week to the engaged list as the default — the source reports this as the sweet spot in roughly 90% of the cases it has tested.
- Accept the reasoning: if you send one email a week, people forget you and engagement decays.
- Recognize the conditional: the source explicitly says if your emails are bad, 3–4 per week is too much; frequency only works when content is good.
- Treat it as a compounding loop — good send, engagement, recognition, more engagement — rather than a one-off tactic.
- Watch open and click rate on the engaged segments; if engagement collapses, the lever to pull is tighter segments and better content, not necessarily fewer sends.
Caveat: The '90% of cases' figure is the presenter's own estimate from client work.
Caveat: This cadence is asserted as opinion based on generated revenue; it is not a study and will not hold for brands with weak content or tiny lists.

Tags: email-lifecycle, cadence, deliverability, engagement, campaign-planning, retention
Source: Ecommerce Email Marketing 2025.docx

---

## Text-based emails vs graphic emails A/B test
Use when: Planning a weekly A/B test, especially for a best-sellers or product roundup campaign where you'd default to heavy graphics.
- Set up a split test where variant A is a fully graphic email (product imagery, banners) and variant B is a text-based email with no product imagery.
- Run it on a campaign type where you assume graphics are required — the source's example was a best-sellers email, where the text version outperformed.
- Reason about why text can win: almost everyone sends graphics, so plain text stands out in a crowded inbox.
- Use the results to decide where text fits in your ongoing mix rather than replacing graphics entirely.
- The source recommends keeping both formats in rotation and using each where it performs.
Caveat: The source presents one brand's example results (text version showed roughly 50% better click rate and more placed orders) as an illustration, not a guaranteed outcome.
Caveat: Results will vary by brand and audience — the source explicitly says to test rather than assume.

Tags: email-lifecycle, experiment-design, email-design, copywriting, conversion-optimization, campaign-planning
Source: Ecommerce Email Marketing 2025.docx

---

## Judge subject-line tests on placed orders, not opens
Use when: Running subject-line tests on campaigns or abandonment emails, and deciding which subject line to roll out.
- Run the subject-line test as a proper split on the same email body.
- Read the open rate as a check but make the decision on placed order rate and order value — the source's abandonment example had nearly identical opens (the higher-open variant was slightly ahead) yet 11.6% vs 3.8% placed order rate.
- Test emotional framing: the source contrasts something lower-barrier like 'your order is ready to go / packed and ready, just click' against something like 'your order's waiting for you', and reports lower barrier-to-entry language driving the higher placed order rate.
- Test an exclusivity angle too, since the source says subject lines can affect whether and how someone buys.
- Repeat subject-line tests frequently (the source frames these as weekly tests), not once a month, and log placed order rate as the primary metric.
Caveat: The specific 11.6% vs 3.8% figures come from one anonymized brand test and are not benchmarks.
Caveat: Attribution on open rate can be noisy; the source itself notes open-rate differences may be variability.

Tags: email-lifecycle, experiment-design, subject-lines, abandoned-cart, measurement, conversion-optimization
Source: Ecommerce Email Marketing 2025.docx

---

## Products vs categories in the email body
Use when: Deciding how to merchandise a campaign for a catalog with many SKUs — show specific products or send people to browse a category.
- If you sell many SKUs, run this test early with a client/brand, because the result shapes how you merchandise emails going forward (the source says it tests this very early).
- Variant A: show or link categories — e.g., men's vs women's, or a category hub page.
- Variant B: show individual products directly in the email (e.g., four men's products, four women's products).
- The source's working hypothesis was that categories would win for a high-SKU store, but the test showed individual products had a higher click rate (1.14% vs 1.04%) and far more purchases.
- Reason about why: when you give shoppers many category options they must keep searching; showing the product directly shortens the path.
- Skip this test for single-product stores, and remember the outcome can flip by brand — the source says it sees both directions.
Caveat: The source reports only one brand's numbers and notes another brand could see categories win.
Caveat: The source declines to attribute the higher average order value to the email itself.

Tags: email-lifecycle, experiment-design, merchandising, product-selection, category-pages, conversion-optimization
Source: Ecommerce Email Marketing 2025.docx

---

## Long-form vs short-form email body copy
Use when: Writing a welcome-flow email or any campaign where you're tempted to explain product science, origin story or background at length.
- Create variant A: long form, e.g., a note from the founder explaining why the product is good, with substantial background and product detail.
- Create variant B: short form — the source's example was about six lines: a warm welcome, one interesting product fact, and a shop-now CTA.
- Run both on a meaningful sample (the source's example used ~2,000 recipients per side) and read click rate and placed order rate.
- In the source's test, the long version produced 2.4% clicks and a 0.2% placed order rate, while the short version produced 3.4% clicks and a 0.7% placed order rate.
- Reason: people don't read every word; long copy buries the call to action, while short copy keeps the CTA visible.
- Roll out the winner for that audience but keep testing, since the source notes the right length differs by audience.
Caveat: One brand's test result; not a rule that short always wins.
Caveat: The source's sample-size disclosure (~2,000 each side) is what it used to argue the result wasn't accidental — your own significance needs depend on your volumes.

Tags: email-lifecycle, experiment-design, copywriting, welcome-flow, conversion-optimization, product-page
Source: Ecommerce Email Marketing 2025.docx

---

## Test send time of day for campaigns
Use when: After you've settled cadence and content, when tuning when campaigns actually go out.
- Set up a same-day time split on a campaign — the source's example compared roughly 11 a.m. against 4 p.m.
- Read open rate, click rate and placed order rate; the source's example showed 36% opens in the morning vs 26% in the late afternoon, with placed orders much higher earlier in the day.
- Don't assume the intuitive answer: the source notes people often assume evenings or late afternoon work because shoppers are off work, but in its test the lunchtime-ish window performed better.
- Account for the sample issue: the source cautions there were too few placed orders at the lower-performing time to lean on that metric alone.
- Once you identify a better window, apply it persistently — the source frames the payoff as a fixed uplift per campaign that compounds over months.
- Re-test occasionally, since the best window is brand-specific.
Caveat: One brand's timing test with a thin placed-order sample; the source says results depend on the brand.
Caveat: Send-time tools and inbox behavior change; verify how your ESP handles time-zone splits.

Tags: email-lifecycle, experiment-design, send-time, campaign-planning, measurement, conversion-optimization
Source: Ecommerce Email Marketing 2025.docx

---

## Test flow delay timing for site abandonment
Use when: Setting the delay on a browse/site abandonment flow or any reminder email where you've assumed 'strike while the iron is hot'.
- Set up a test on the flow's first delay: variant A sends around 30 minutes after abandonment, variant B waits about 4 hours.
- Use the source's example as the hypothesis to challenge: the 30-minute version was assumed to be better because the visit was fresh, but it produced a much lower placed order rate (0.7%) than the 4-hour version, on a large sample.
- Read engagement carefully: the fast version had fewer opens and clicks, which the source interprets as people not being ready yet; the later send reached them when they had time to buy.
- Consider the context explanation: someone who abandons may be busy with kids or errands and still busy 30 minutes later, but settled in bed at night when the 4-hour reminder arrives.
- Apply the same testing discipline to delays between later messages in the flow, not just the first email.
Caveat: This is one brand's flow test; the source says delays will differ per flow and must be tested.
Caveat: Placed order rate on a flow depends on attribution windows — verify how your ESP attributes flow revenue.

Tags: email-lifecycle, experiment-design, abandoned-cart, flow-timing, automation-flows, retention
Source: Ecommerce Email Marketing 2025.docx

---

## Branded text email vs plain native text email
Use when: Executing text-based campaigns and deciding whether to include your logo and footer or send truly plain text.
- Define variant A — branded text: plain text body with your logo at the top (clickable, driving site visits) and your footer at the bottom, giving brand association.
- Define variant B — plain text: nothing but text, rendered in the inbox provider's native format (white background, black text, like an email from a friend), usually a bit shorter and easier to digest.
- Run the test and compare delivered volume, click rate and placed order rate; the source's example had 1,900 delivered on branded vs 1,400 on plain, similar revenue, but plain showed a higher placed order rate (1.7% vs 1.2%) and higher click rate (4% vs 3%).
- Choose per message intent: the source suggests plain/perceived-personal for founder-voice emails ('hey, it's Max, the founder'), and branded text when the message comes from the brand itself.
- Keep both in your rotation and lean toward the one performing better for your list.
Caveat: One brand's test with modest delivered volumes; the source notes results depend on the brand and message.
Caveat: The plain-text version sacrifices the clickable logo, which can cost some site traffic.

Tags: email-lifecycle, experiment-design, email-design, copywriting, branding, campaign-planning
Source: Ecommerce Email Marketing 2025.docx

---

## Weekly A/B test roster of high-leverage variables
Use when: Building a recurring experimentation plan for your email program so testing keeps producing revenue rather than becoming sporadic.
- Treat these as your roster of high-leverage variables to work through: graphic vs text-based email; subject lines; products vs categories; long vs short form; campaign send time; flow delay timing; branded vs plain text.
- Run them as real splits on meaningful samples — the source criticizes one-off 'change two words once a month' tests as not enough to maximize revenue.
- Read the right metric per test: placed order rate and revenue for subject lines, products-vs-categories and flow timing; click rate plus placed order rate for format and length tests.
- Rotate through the roster so each variable actually gets tested for your brand instead of assumed.
- Log results and roll the winner into the standing program, then re-test periodically since audiences shift.
Caveat: The source lists these variables from its own agency practice; they're a prioritization, not an exhaustive or statistically rigorous framework.
Caveat: Small lists will struggle to reach significance on split tests — the source's own examples lean on ~2,000-per-side samples.

Tags: email-lifecycle, experiment-design, measurement, conversion-optimization, campaign-planning, copywriting
Source: Ecommerce Email Marketing 2025.docx

---

## Prime an LLM with brand context before writing email copy
Use when: Setting up an AI-assisted email copy workflow for a store before generating any campaign copy.
- Write a priming prompt that dumps in as much brand information as possible: what you sell, mission, brand story, what makes the brand unique, ideal customer, brand voice, goals and aspirations.
- Use full paragraphs rather than quick sentences — the source stresses giving it as much space and information as you can.
- Include the store's website link so the model can pull additional context from it.
- Keep this priming block reusable so every subsequent copy prompt in the session inherits the same context.
- Expect the model to need product-level facts (materials, positioning, specific product copy) closer to when you draft.
Caveat: The source's example primer for a large apparel brand is described as 'pretty brief' — more is generally better.
Caveat: Model behavior and supported features change; verify what your current tool does with links and long prompts.

Tags: email-lifecycle, copywriting, ai-tools, brand-positioning, workflow, prompting
Source: Ecommerce Email Marketing 2025.docx

---

## Prompt for graphic-email copy structure, then iterate
Use when: Drafting hero and body copy for a graphic campaign and you want structured output instead of a wall of generic AI prose.
- State the format explicitly: 'we're creating a graphic based email campaign with minimal copy to send to our customers' — the source says without 'graphic based' the model returns letter-style text.
- State the topic in plain language, including the emotional angle (e.g., best sellers as your MVP in the gym, helping you break PRs).
- Request a 'quick and punchy' headline — the source says without 'punchy' you get a 20-word headline.
- Request a slightly longer subheadline plus 2–3 sentences of body copy leading into a shop-now CTA, mirroring the hero structure of headline → subheadline → body → button.
- Treat the first output as a draft: iterate ('make it more unique', 'make the headline more conversational', 'give me more options for headlines') and combine your favorite fragments.
- Do the final polish yourself — the source treats the model as a support player, not the finisher, and reports this is how its agency writes copy.
Caveat: The source warns AI copy is recognizable via clichés ('you're in luck', 'crafting', 'enthusiasts', 'we're diving into the exciting world', 'unleash your potential') and should not be shipped as-is.
Caveat: Prompt phrasing effectiveness is model- and version-dependent.

Tags: email-lifecycle, copywriting, ai-tools, prompting, creative-strategy, email-design
Source: Ecommerce Email Marketing 2025.docx

---

## Generate a year of non-discount email topics from micro-topics
Use when: Planning a campaign calendar and running out of non-discount angles, especially for niche or technical product categories.
- Write a prompt stating the niche, what you sell, your brand mission/benefits, your average customer and what they want.
- Ask for 10 overarching, general topics that tie into product benefits and customer lives.
- Ask for 10 very specific subtopics under each overarching topic, written to educate the customer and potentially position your product as a solution — the source's prompt produced roughly 100 usable ideas.
- Treat the output as raw material: for a supplement brand the source got themes like holistic health and wellness, sustainable muscle building and the science of natural supplements, with subtopics like adaptogens and stress, sleep and muscle recovery, gut health, and mental health and fitness.
- Turn each promising subtopic into one campaign, and let brand-specific angles you think of yourself take priority over the AI list.
- Feed the best ideas into your 3–4-per-week cadence so non-discount content fills most of the calendar.
Caveat: Output quality varies — the source notes some generated topics needed cleanup.
Caveat: The source insists AI is only a starting point and should never be the sole source of your content.

Tags: email-lifecycle, content-strategy, ai-tools, campaign-planning, prompting, retention
Source: Ecommerce Email Marketing 2025.docx

---

## Set SMS campaign frequency to 1–2 sends per week maximum
Use when: Deciding your monthly SMS campaign cadence and how many messages to schedule per week for your store's list.
- Treat 1 SMS per week as your standing default and 2 per week as the rare exception, reserving extra sends for big events.
- Recognize SMS is more intrusive than email because it triggers a notification sound and vibration in a primary app; the source says it is not comparable to sending 4–5 emails per week without backlash.
- Use segmentation and selective sending so only the relevant portion of the list gets each message, reducing annoyance while keeping total weekly volume low.
- Watch unsubscribe rate as your primary guardrail: the source reports unsubscribe rates on SMS run much higher than email, and that they rise the more you send.
- Plan a regular monthly cadence of roughly 1–2 sends per week rather than blasting everything at a launch and going silent.
Caveat: The 1–2 per week figure is the presenter's tested recommendation, not an industry standard; test against your own unsubscribe and revenue data.
Caveat: Back-to-back daily sends (e.g., flash sale launch day then last-chance day) are acceptable for major events per the source.

Tags: email-lifecycle, sms-marketing, retention, campaign-calendar, list-health, frequency-capping
Source: Everything You Need to Know About SMS Marketing in 2025.docx

---

## Budget SMS copy using the rendered segment count
Use when: Writing and editing SMS campaign or flow copy before sending, to control per-message cost.
- Preview the fully rendered message, including personalization, links and opt-out text.
- Standard GSM-7 SMS allows 160 characters in one segment; Unicode or emoji can reduce that to 70. Multipart limits differ.
- Use the provider segment counter and current destination pricing to estimate total campaign cost.
- Compare a concise version with the original on net contribution, preserving clarity and required information.
Caveat: An emoji does not simply cost a fixed 35-50 characters; it can change encoding for the whole message. https://help.klaviyo.com/hc/en-us/articles/13502982552347

Tags: email-lifecycle, sms-marketing, creative-strategy, cost-control, copywriting
Source: Everything You Need to Know About SMS Marketing in 2025.docx

---

## Check SMS encoding and segment cost before sending
Use when: Deciding whether to include emojis in SMS campaign or flow copy to add visual interest without images.
- Preview the fully rendered message, including personalization, links and opt-out text.
- Standard GSM-7 SMS allows 160 characters in one segment; Unicode or emoji can reduce that to 70. Multipart limits differ.
- Use the provider segment counter and current destination pricing to estimate total campaign cost.
- Compare a concise version with the original on net contribution, preserving clarity and required information.
Caveat: An emoji does not simply cost a fixed 35-50 characters; it can change encoding for the whole message. https://help.klaviyo.com/hc/en-us/articles/13502982552347

Tags: email-lifecycle, sms-marketing, creative-strategy, copywriting, cost-control
Source: Everything You Need to Know About SMS Marketing in 2025.docx

---

## Reserve MMS images for campaigns where they earn 2–3x the SMS revenue
Use when: Choosing between a plain-text SMS and an image MMS for a product launch or campaign send.
- Default to plain-text SMS for your regular campaign and flow sends, since SMS itself is already far more expensive than email per message.
- Before attaching an image, estimate whether the MMS send must produce 2–3x the revenue of the SMS version to break even on cost—the source says this is rarely achieved by one image.
- Restrict MMS to situations where the visual is essential (e.g., a highly visual product drop) and you can defend the cost with expected revenue.
- Compare MMS vs SMS versions of similar sends over time in your dashboard to see whether images genuinely lift response for your audience before scaling them up.
Caveat: The 2–3x cost multiplier is the presenter's stated range; your provider's rate card may differ, so confirm actual per-message pricing.
Caveat: The source's advice is to stick to SMS as much as possible, but treats MMS as a judgment call rather than a prohibition.

Tags: email-lifecycle, sms-marketing, cost-control, creative-strategy, campaign-strategy
Source: Everything You Need to Know About SMS Marketing in 2025.docx

---

## Choose an SMS platform that consolidates with your existing email stack
Use when: Selecting or switching an SMS provider for your store before building flows and campaigns.
- Check whether your current email platform also offers SMS; the source recommends Klaviyo users stay on Klaviyo to consolidate marketing in one place.
- If considering alternatives, the source names Attentive and Postscript as solid options alongside Klaviyo.
- Discount vendor comparisons built on novel AI features—the source argues these features are rarely used and the differences are marginal.
- Note that the main platforms are similarly priced, so switching to save money is often not the deciding factor.
- Expect the provider to support a dedicated phone number, data tracking, and automation setup; follow the provider's own setup guide, which the source says takes minutes.
- Verify current pricing, feature sets and setup steps directly with the vendor, as these change.
Caveat: The named tools reflect the source's opinion at time of recording; verify current capabilities and pricing.
Caveat: There is no single 'correct' platform per the source—consolidation and simplicity are the main criteria.

Tags: email-lifecycle, sms-marketing, tooling, stack-consolidation, vendor-selection
Source: Everything You Need to Know About SMS Marketing in 2025.docx

---

## Grow the SMS list with a post-purchase opt-in checkbox
Use when: Setting up checkout and post-purchase list growth to continuously add SMS subscribers without extra traffic.
- Place a checkbox on the purchase/checkout page asking the buyer to agree to receive marketing messages.
- Keep it on for all buyers so the list grows automatically with every order.
- Position SMS opt-in alongside email opt-in so the same checkout flow captures both channels.
- Treat this as the low-effort baseline channel; the source still calls pop-ups the most effective list-growth method, so run both.
- Confirm your checkout and SMS platform support the consent capture and that opt-ins sync to the right list.
Caveat: Post-purchase opt-ins yield fewer subscribers than a well-optimized pop-up per the source; they are a background contributor, not the main driver.
Caveat: Consent and messaging regulations vary by region—confirm compliance for your markets.

Tags: email-lifecycle, sms-marketing, list-growth, checkout, consent
Source: Everything You Need to Know About SMS Marketing in 2025.docx

---

## Delay the SMS/email pop-up trigger to 6–10 seconds after page load
Use when: Configuring the trigger and display rules of a website pop-up form that captures email and SMS subscribers.
- Set the pop-up trigger to a time delay of about 6–10 seconds after the page loads, which the source says is not too soon and has been tested.
- Avoid scroll-based or exit-intent triggers, which the source says can misfire; a simple time delay performs reliably.
- Reject long delays: the source argues few visitors stay 30 seconds, so waiting that long means few people ever see the form.
- Balance intrusiveness: the form should be seen by as many visitors as possible without harming website conversions, which is the stated fine line.
- Monitor both form conversion rate and overall site conversion rate after launch to confirm the delay is not hurting purchases.
Caveat: The 6–10 second window is the presenter's tested recommendation for their client set, not a universal optimum; test on your own traffic.
Caveat: Pop-up timing interacts with page speed and device type—validate on mobile specifically.

Tags: email-lifecycle, sms-marketing, list-growth, pop-up, conversion-optimization
Source: Everything You Need to Know About SMS Marketing in 2025.docx

---

## Build a two-step micro-commitment pop-up: email first, then phone
Use when: Designing the multi-step flow of a website signup pop-up to capture both email and SMS subscribers.
- Step one: state the offer plainly ('this is what you get') and ask only for the email address.
- Step two: immediately prompt for the phone number with copy that ties it to completing the offer, e.g. 'finish signing up to get your discount'.
- Use as few words as possible in both steps—simplicity is emphasized repeatedly.
- Never ask for birthday, product preferences, or other fields in the same step; the source says extra fields kill completion.
- Offer something of value—a discount, giveaway, or free guide—since the source notes people will not hand over a phone number for nothing.
- Test the two-step version against a single combined field to confirm the lift in your own funnel.
Caveat: The '10x better' comparison is the presenter's claim from their testing, not an independent benchmark.
Caveat: Discount offers trade margin on the first purchase; the source assumes a strong email/SMS backend recovers that margin over time.

Tags: email-lifecycle, sms-marketing, list-growth, pop-up, form-design, offer-design
Source: Everything You Need to Know About SMS Marketing in 2025.docx

---

## Aim pop-up forms at 8–10% conversion vs the 2–3% baseline
Use when: Benchmarking and improving the conversion rate of your site's email/SMS signup form against typical performance.
- Measure your current pop-up conversion rate (new subscribers divided by visitors who saw the form) to establish a baseline.
- Compare against the source's observed baseline: most audited brands sit around 2–3%.
- Apply the levers that drive the source's 8–10% results: a 6–10 second time delay, a strong offer, minimal copy, and the two-step email-then-phone flow.
- Track the form's impact on total site conversion so you can confirm the extra visibility is not costing more sales than it creates.
- Re-test offer strength separately from form design, since the source stresses you must give people a reason to sign up.
Caveat: 8–10% is an outcome the presenter reports from their own optimization work, not a guaranteed result; it is a target, not a promise.
Caveat: Results depend on traffic source, offer, and audience; poor-fit traffic may never reach those levels.

Tags: email-lifecycle, list-growth, pop-up, conversion-optimization, benchmarking
Source: Everything You Need to Know About SMS Marketing in 2025.docx

---

## Launch five core SMS automation flows before heavy campaign sending
Use when: Building the automated SMS flow system for a store, or deciding which flows to prioritize first.
- Welcome flow: deliver the promised discount to new subscribers in about 2–3 SMS messages.
- Browse abandonment: message users who viewed a product and left, prompting them to return and finish.
- Cart abandonment and checkout abandonment: remind people who added to cart or reached checkout to complete the order with a direct link.
- Win-back: re-engage customers who purchased months ago and have not returned, optionally with a discount.
- Keep flow volume light—do not overload customers with messages, since flows are meant for quick, high-converting, high-ROI touches rather than retention nurturing.
- Use your platform's templates and connect it to your store platform (e.g., Shopify) so triggers fire automatically; the source says setup is easy and templates exist for base flows.
Caveat: The source says you 'really don't need too much' in flows—avoid adding many extra steps.
Caveat: Template copy and trigger names may change in the platform interface; verify current setup steps in your tool.

Tags: email-lifecycle, sms-marketing, automation, flows, abandoned-cart, retention
Source: Everything You Need to Know About SMS Marketing in 2025.docx

---

## Keep SMS campaigns transactional, urgent, or announcement-based—not nurture
Use when: Choosing what content types belong in the SMS campaign calendar versus what should stay in email.
- Assign to SMS: product drops and launches, flash sales, special offers, back-in-stock/restock alerts, and important announcements.
- Assign to email: nurture, educational, and social-proof content; the source says email is where you can nurture without annoying people.
- Use angles that manufacture importance where relevant, e.g. a 'back in stock' message, since urgency fits the channel.
- Send mostly transactional-style content on SMS and reserve the bulk of relationship-building content for email.
- Cut any SMS campaign type that historically shows high unsubscribes and weak ROI in your own data, since the source found nurture/social-proof SMS underperformed.
Caveat: This reflects the presenter's tested experience; your audience may tolerate more or less nurture content, so test.
Caveat: Some announcement types (e.g., giveaways to grow social) are used as filler, not core revenue drivers.

Tags: email-lifecycle, sms-marketing, campaign-strategy, content-mix, segmentation
Source: Everything You Need to Know About SMS Marketing in 2025.docx

---

## Model the SMS month around launches and flash sales, then fill the gaps
Use when: Planning a store's monthly SMS campaign calendar around known launch and promotion dates.
- List the month's main events first; use the source's example of a brand with a Halloween product launch mid-month and a Halloween flash sale on the last two days.
- For a product launch, plan about 2–3 messages: an announcement on launch day (likely the biggest sales driver), a reminder or low-stock/urgency message about a week later, and optionally a teaser 1–2 days before to build hype.
- For a flash sale, send two messages: a launch message on day one and a last-chance message on the final day; the source says back-to-back daily sends are fine for big events.
- Identify gaps of more than a week without an SMS and insert 2–3 filler campaigns, e.g. a social media giveaway driving to Instagram, or a 'restock' alert for a popular item.
- Note the source's rationale for restock sends: an item that sold out proves popularity, and the restock itself creates urgency—you can even run one on an item that was not literally out of stock.
- Count total sends against the 1–2 per week ceiling and trim if the calendar exceeds it.
Caveat: The example calendar is an illustration for an eight-figure brand, not a template that fits every store size or category.
Caveat: The suggested restock angle may not be appropriate if it misrepresents inventory availability.

Tags: email-lifecycle, sms-marketing, campaign-calendar, launch-strategy, promotion-planning
Source: Everything You Need to Know About SMS Marketing in 2025.docx

---

## Test SMS send times; default to 11 a.m.–2 p.m. and 4–5 p.m.
Use when: Scheduling SMS campaigns and last-chance messages to maximize open and click response for your specific list.
- Run your own tests across times of day, since the source says every audience differs and there is no single right answer.
- Use 11 a.m.–2 p.m. as the safest default window, when people are between morning and lunch.
- Try early evening at 4–5 p.m. as a secondary window that the source says performs well.
- Avoid sending before 10 a.m. (people sleep in) and after about 7:30 p.m. (people go to bed or turn off phones).
- Schedule last-chance messages around 6–7 p.m. with a short deadline like '4 hours left', but not later than that window.
- Track clicks and revenue by send hour over multiple sends before locking in a standard time.
Caveat: These windows are the presenter's tested heuristics, not universal laws; confirm with your own A/B timing tests.
Caveat: Timezone spread in your list can blur results—segment or schedule per timezone where your platform allows.

Tags: email-lifecycle, sms-marketing, send-time, experiment-design, campaign-strategy, measurement
Source: Everything You Need to Know About SMS Marketing in 2025.docx

---

## Treat the SMS list as a channel asset for revenue you control
Use when: Deciding whether to invest budget and team time in building an SMS channel versus relying solely on paid acquisition.
- Evaluate SMS as an owned audience asset: contacts gave you their number, so they are not cold traffic and the list cannot be revoked by an ad platform.
- Recognize the reach mechanic: the source cites an average 98% open rate because text messages are seen almost immediately by nearly everyone.
- Expect automations to run continuously in the background after one-time setup, requiring only periodic checks and optimization.
- Judge channel value against your store's revenue mix; the source cites an example brand generating $750k in 30 days from SMS (roughly 20% of total revenue) and $422k from automations alone in the same window.
- Set expectations by tracking your own SMS-attributed revenue and automation click rates rather than adopting case-study numbers as targets.
Caveat: The 98% open rate and the $750k/$422k figures are the presenter's cited examples, not benchmarks or promises; your results depend on list size, offer, and product.
Caveat: Introductory framing of 'SMS is the future' is the presenter's opinion; treat it as a rationale for testing, not a guaranteed channel outcome.

Tags: email-lifecycle, sms-marketing, channel-strategy, retention, attribution, owned-audience
Source: Everything You Need to Know About SMS Marketing in 2025.docx

---

## Choose an SMS platform: consolidate with email, then price-shop
Use when: Selecting or renegotiating the SMS/text platform for your store's lifecycle messaging.
- Prioritize running SMS inside the same platform as your email (e.g., Klaviyo, Omnisend, Attentive) so lists, segments and reporting live in one place.
- Because consolidation often costs more, request a quote from your current email provider for their SMS add-on.
- Take that quote to the main SMS competitors (source names Attentive and Postscript as the 'big dogs'; others such as OneText exist) and ask them to beat it, letting them compete on price.
- Decide mainly on price and ease of management. The source argues the platforms' differentiating AI features are unlikely to be used and 'the basics will drive 99% of your revenue,' so don't agonize over the choice.
Caveat: This is the presenter's opinion (Max / Well Copy); platform pricing and feature sets change, so verify current quotes and contracts.
Caveat: Platform names and capabilities are source-specific and may be outdated.

Tags: email-lifecycle, sms-marketing, platform-selection, vendor-negotiation, klaviyo, list-growth
Source: How to Create a SMS Marketing Strategy For $10M Shopify Brands.docx

---

## Capture phone numbers in your popup from day one
Use when: Designing or revising the email/SMS signup popup that captures subscribers at store entry.
- Include a phone-number field in your popup even if you have no SMS list yet. The source's argument: if you start collecting SMS today and only decide to use it a year later, you already have a large list to market to; if you wait, you have zero.
- Use a popup tool optimized for SMS capture. The source recommends Alia (allpopups.com) over native platform popups, reporting native Klaviyo opt-ins around 3–4% vs. Alia submit rates around 9% and typically ~16% when the offer is strong.
- Track phone opt-in rate as a headline metric; the source frames getting ~60% of ad traffic to hand over a phone number as a major cheap-conversion unlock.
- Refresh offers/tests over time so capture rate is judged on its own, not against one weak offer.
Caveat: Opt-in rates cited (3–4%, 9%, ~16%) are the presenter's observed figures for specific brands, not guaranteed benchmarks.
Caveat: Tool names and interface details may change; verify current setup.

Tags: email-lifecycle, sms-marketing, list-growth, popup-optimization, lead-capture, klaviyo
Source: How to Create a SMS Marketing Strategy For $10M Shopify Brands.docx

---

## Use a quiz popup and 'activate your discount' copy to lift phone capture
Use when: Building the SMS/phone opt-in step of your store popup to raise subscriber capture rate.
- Start the popup with a quiz or micro-commitment (source: 'this is what works') before requesting email or phone — engage the visitor first, then ask.
- Choose a template that offers a discount (e.g., 10% off) and asks a qualifying question, then transitions to the contact step.
- Change the button label from 'Continue' (which signals another required step) to 'Claim now' to reduce drop-off.
- Replace generic SMS copy like 'Sign up for texts' or 'Get exclusive deals' with action-oriented continuity copy such as 'Finish signing up with text to activate your discount' — the visitor has already given email and wants the discount activated.
- Do not stack an extra discount for SMS. The source reports no marginal impact from offering extra % off for the phone number.
Caveat: Quiz-first flows and copy results are the presenter's experience, not a universal rule.
Caveat: Source claims 15%+ opt-in is achievable but notes most forms they review sit at 5–6% submit rate.

Tags: email-lifecycle, sms-marketing, list-growth, popup-optimization, copywriting, conversion-optimization
Source: How to Create a SMS Marketing Strategy For $10M Shopify Brands.docx

---

## Treat SMS as high-urgency, low-frequency — not a nurture channel
Use when: Deciding what content belongs in SMS blasts vs. email, and setting the tone of your text program.
- Recognize the cost of intrusion: source reports SMS unsubscribe rates of 3–5% vs. roughly 0.3% for email, because a text is a phone ding the customer notices.
- Send far less on SMS than on email. Cut nurture content (testimonials, brand storytelling, evergreen best-sellers) — the source says it 'doesn't work' on SMS and drives unsubscribes long-term.
- Reserve SMS for high-urgency events: product launches, back-in-stock/restock alerts, flash sales, private events, insider details.
- Make each text 'worth receiving' and get straight to the point; test whether a timely-urgency angle (e.g., 'selling fast this week') outperforms a generic nurture angle before scaling frequency.
Caveat: Unsubscribe-rate comparison is the presenter's cited figure, not a site metric.
Caveat: Source explicitly says this is a starting point; some brands they run send daily because it fits their context.

Tags: email-lifecycle, sms-marketing, campaign-strategy, retention, unsubscribe-management, urgency
Source: How to Create a SMS Marketing Strategy For $10M Shopify Brands.docx

---

## Budget SMS copy using the rendered segment count
Use when: Writing and budgeting SMS campaign and flow messages, especially for large lists.
- Preview the fully rendered message, including personalization, links and opt-out text.
- Standard GSM-7 SMS allows 160 characters in one segment; Unicode or emoji can reduce that to 70. Multipart limits differ.
- Use the provider segment counter and current destination pricing to estimate total campaign cost.
- Compare a concise version with the original on net contribution, preserving clarity and required information.
Caveat: An emoji does not simply cost a fixed 35-50 characters; it can change encoding for the whole message. https://help.klaviyo.com/hc/en-us/articles/13502982552347

Tags: email-lifecycle, sms-marketing, cost-management, copywriting, mms, budgeting
Source: How to Create a SMS Marketing Strategy For $10M Shopify Brands.docx

---

## Test SMS vs. MMS images on net profit, not revenue
Use when: Deciding whether to include product images in SMS campaigns or abandonment flows.
- Run A/B tests of identical messages with and without an image, and track revenue AND send cost for each version.
- Source example: the image version generated ~1.3x more revenue but cost 3x to send — worse ROI on revenue, yet net-profit-positive once the extra revenue ($1,300 back on $200 extra spend) is counted.
- Source example 2: no-image message did $620 revenue vs. $1,200 with image; the image cost only ~$15 more at low volume, so it was a clear win — showing results depend on list size and offer.
- Note the behavioral pattern: image messages often get lower click-through (people see the product and click with higher intent), but can produce more revenue.
- Use images deliberately for high-impact moments only (new flavor/product drop, key abandoned-cart/welcome messages). The source notes a 9-figure brand (Grain's) rarely uses images, reserving them for important sends.
Caveat: Both examples are low-volume/single-brand results, explicitly not guarantees; the source warns it 'doesn't always play out this way.'
Caveat: Retest on your own offers and list size, since cost scales with list size.

Tags: email-lifecycle, sms-marketing, experiment-design, mms, cost-management, conversion-optimization
Source: How to Create a SMS Marketing Strategy For $10M Shopify Brands.docx

---

## Build the five core SMS flows (welcome + four abandonments + post-purchase)
Use when: Setting up or auditing the automated (flow) side of an SMS program.
- Welcome flow: triggered when someone joins via the popup (often with a discount). Keep it simple — introduce the brand and drive the discount.
- Four abandonment flows, kept dead simple: site abandoned (browsed site, no product page), browse abandoned (viewed a product page), cart abandoned (added to cart), checkout abandoned (reached checkout).
- Post-purchase / replenishment / win-back flow: bring buyers back after their first order.
- Keep abandonment messages single and simple (see the US compliance card) and split by new vs. returning buyers when you can.
- Treat these basics as the moneymakers: the source reports one brand's core flows producing $517k, with $293k from welcome, $107k cart abandoned, $46k browse abandoned, $20k retention, and $13k site abandoned in a month.
Caveat: Revenue figures are a single agency portfolio example, not a benchmark to expect.
Caveat: Exact flow structure should be adjusted per brand context.

Tags: email-lifecycle, sms-marketing, automation-flows, abandoned-cart, welcome-flow, retention
Source: How to Create a SMS Marketing Strategy For $10M Shopify Brands.docx

---

## Structure the SMS welcome flow: day 1, day 3, day 5
Use when: Writing the SMS welcome series triggered by your popup signup.
- Send SMS 1 immediately: give the discount with no preamble (the person just signed up for it).
- Send SMS 2 about 2 days later (day 3) with a bit of brand/differentiation info or a reminder of the discount.
- Send SMS 3 on about day 5 as an 'absolute last chance' before the code expires.
- Keep the window tight — do not delay sends by weeks; hit people while they're warm.
- The more aggressive alternative (source cites Grain's) is a message every single day with the discount repeated, mixing in educational messages; the source frames both as valid but prefers the tighter three-message structure.
- If doubling up, keep messages short: e.g., 'Welcome to [brand], here's 20% off, code WELCOME20, shop now,' then a last-chance text days later. A/B test images and delay timing.
Caveat: Dense cadence (e.g., daily) should be tempered by your audience and follows compliance/consent rules.
Caveat: Delay timings are recommendations, not tested universals.

Tags: email-lifecycle, sms-marketing, welcome-flow, automation-flows, copywriting, retention
Source: How to Create a SMS Marketing Strategy For $10M Shopify Brands.docx

---

## Send only one SMS per abandonment event (US compliance)
Use when: Setting up SMS cart, browse, site, or checkout abandonment flows, especially for US customers.
- Build each abandonment flow to send exactly one SMS per recipient — the source states sending more than one SMS in an abandonment flow is illegal in the US.
- Schedule that single message to fire within 48 hours of the triggering event (source cites Klaviyo's built-in constraint of one SMS per recipient in cart abandonment within 48 hours).
- Confirm the recipient has SMS consent before the flow sends.
- Because you get one shot, make it simple: browse abandoned → 'Eyes on something? You have good taste. Keep shopping' (fire ~60 min after browse); cart/checkout → 'Looks like you forgot something — finish your order.'
- Optionally test adding an MMS product image against plain text, and split buy-intent: give non-buyers a welcome discount code (e.g., 'use WILDWELCOME20') while keeping buyers' messages simpler.
- Verify current carrier/platform compliance rules, which can change.
Caveat: 48-hour/one-message rule is described for the US; other jurisdictions differ.
Caveat: The source says this is a compliance ceiling, not a ceiling on how creative the single message can be.

Tags: email-lifecycle, sms-marketing, abandoned-cart, automation-flows, compliance, conversion-optimization
Source: How to Create a SMS Marketing Strategy For $10M Shopify Brands.docx

---

## Time post-purchase and replenishment SMS to the buy cycle
Use when: Building the post-purchase and replenishment SMS flow for your store.
- Send SMS 1 around day 10–14 after order delivery, while the buyer is in the honeymoon phase: ask if they're enjoying the product and suggest cross-sell/upsell or a repeat purchase.
- For consumable/replenishment products, add SMS 2 timed to when the product runs out. Calculate it: e.g., Athletic Greens — 30-day supply plus 7-day delivery → send on ~day 35, 'are you running low? reorder.'
- Hold offers initially; the source recommends not adding discounts to these early post-purchase messages until later.
- Don't over-send: remember buyers also receive your campaign blasts, so two well-timed post-purchase messages are usually enough.
- Consider keeping all win-back-style post-purchase messages in one flow triggered on order placement.
Caveat: The source says this flow varies so much brand-to-brand that no single verified template applies; the athletic-greens math is an illustration.
Caveat: Replenishment timing depends on your own product consumption and delivery cycle.

Tags: email-lifecycle, sms-marketing, automation-flows, replenishment, post-purchase, upsell
Source: How to Create a SMS Marketing Strategy For $10M Shopify Brands.docx

---

## Trigger SMS win-back at double the average time between purchases
Use when: Setting the trigger point and offer structure for an SMS win-back flow for lapsed buyers.
- Estimate average time between purchases for your store (e.g., 45 days) and multiply by two (→ ~90 days you'd likely consider a customer lapsed).
- At that trigger, send SMS 1 with a flash offer, e.g., 'We miss you — here's 30% off, exclusive code, expires in 72 hours.'
- Wait ~2 days and send SMS 2 as a last-chance/expiry reminder.
- Keep it to roughly two messages; the source says these two plus your post-purchase sends are all you need before the cycle repeats.
- Confirm your estimate with actual reorder-interval data rather than guessing.
Caveat: '2x average time between purchases' is a source heuristic, not a universal law.
Caveat: Offer depth (e.g., 30%) is an example; test margin impact before adopting.

Tags: email-lifecycle, sms-marketing, win-back, automation-flows, retention, offer-design
Source: How to Create a SMS Marketing Strategy For $10M Shopify Brands.docx

---

## Cap SMS blasts at about two campaigns per week for most brands
Use when: Setting the SMS campaign (blast) calendar and frequency for your store.
- Start with a baseline of about two SMS campaigns per week for a typical brand. Send at least one per week at minimum.
- For aggressive-acquisition brands spending heavily (source cites Grain's), sending an SMS every single day to people who've never bought is acceptable if you have a large list and lots of news.
- Ease off for existing buyers: for one-time-purchase or subscription brands, reduce frequency to buyers, and the source says don't text active subscribers at all.
- During major sale pushes you can increase to daily or even two-a-day (source references a 9-figure brand's calendar), then return to baseline after the push.
- Don't force sends: the source prefers saving SMS for big announcements to avoid unsubscribes — 'do not force out SMS if you don't have to.'
Caveat: Frequency recommendations are the presenter's opinion and depend on list size, brand news and consent.
Caveat: Buyer-vs-non-buyer cuts are specific to a sub/large-brand context.

Tags: email-lifecycle, sms-marketing, campaign-strategy, sending-frequency, unsubscribe-management, subscription
Source: How to Create a SMS Marketing Strategy For $10M Shopify Brands.docx

---

## Plan an SMS campaign calendar around high-urgency events
Use when: Building the monthly SMS campaign calendar and choosing which messages to send.
- Anchor sends to genuinely urgent, timely events: product launches, back-in-stock/restock alerts, flash sales, private events, insider news, and time-boxed 'selling fast this week' trend alerts.
- For a launch, send the announcement, then a reminder a couple days later (source example: sent on the 4th, reminder on the 6th).
- Use SMS-exclusive flash sales — the source highlights exclusive-to-list offers as especially effective.
- You can relabel messages with urgency even when literal urgency is absent (e.g., frame a past collection as a 'restock,' or a product as 'running low') because restocks perform well — but note the source's caution that non-urgent nurture performed worst and drove more unsubscribes.
- Example: a brand sent just five SMS in a month (pre-order collection, list-exclusive free-item offer, framed restock, reminder, launch) and reports >$100k and 16% of total store revenue — showing a lean, intentional calendar can perform.
Caveat: This revenue example is a single case, not a benchmark.
Caveat: Framing messages as 'restock' or 'running low' when untrue is the source's tactic; consider trust and advertising-standards implications before using.

Tags: email-lifecycle, sms-marketing, campaign-strategy, launch-planning, urgency, flash-sale
Source: How to Create a SMS Marketing Strategy For $10M Shopify Brands.docx

---

## Broadcast SMS to the full list with a tight exclusion list
Use when: Segmenting your SMS list for campaign sends and deciding send exclusions.
- Send to all SMS subscribers rather than narrow engaged segments. The source notes people who never click a text still purchase (they see the message and go to the site directly).
- Maintain a simple exclusion list: exclude a contact only after they've received ~15 texts with zero clicks ever.
- Also exclude anyone you've bought from in ways that make them a poor target (e.g., don't text active subscribers on a subscription).
- Clean the list about monthly to control cost, since SMS is expensive per send.
- For big announcements (e.g., a New Year's Eve sale), send to the entire list with no exclusions.
- Don't 'get too cute' building engaged segments — the source reports broadcasting usually makes the most money.
Caveat: '15 texts with zero clicks' is a source heuristic, not a tested threshold.
Caveat: Platform automation may handle exclusion lists differently; verify your setup.

Tags: email-lifecycle, sms-marketing, segmentation, list-hygiene, campaign-strategy, cost-management
Source: How to Create a SMS Marketing Strategy For $10M Shopify Brands.docx

---

## Test delays, offers and images before scaling SMS
Use when: Deciding what to change or expand once your core SMS flows and campaigns are running.
- Test message timing/delays (welcome day spacing, abandonment send windows, win-back trigger).
- Test offers: whether a discount changes behavior, and how deep, before adding them to flows (source found no marginal lift from extra SMS discounts).
- A/B test including images versus not in flows and campaigns, tracking net profit (revenue minus send cost) rather than revenue alone.
- Keep the tests attached to the core flows the source says drive most revenue; add complexity only after the basics are measured.
- Expect results to be brand-specific: the source explicitly says this isn't a copy-exactly recipe and cites running daily SMS or intricate flows for some brands.
Caveat: Source advises treating its structure as a starting point, not scripture; verify with your own data.
Caveat: Small-sample tests give directional, not definitive, reads.

Tags: email-lifecycle, sms-marketing, experiment-design, conversion-optimization, abandoned-cart, measurement
Source: How to Create a SMS Marketing Strategy For $10M Shopify Brands.docx

---

## Three components of a converting email: copy, structure, design
Use when: Planning a campaign or flow email (promo, launch, replenishment reminder) and deciding where a weak performer is failing before redesigning it.
- Split the email into three layers: copy (headline, body, CTA wording, social proof), structure (the order and placement of sections and buttons), and graphic design (buttons, colors, imagery, flow between sections).
- Judge each layer by whether it moves a skimming reader toward the product, not by whether it looks impressive; the presenter argues brands lose revenue by caring more about how the email looks than how it performs.
- Diagnose a low-performing email by location: if readers don't reach the offer, fix structure/button placement first; if they reach it but don't click, test copy clarity and offer framing; if it feels cheap or off-brand, fix design.
- Make copy and design reinforce each other — copy should be scannable in the same rhythm the design implies, with bolded points and short lines rather than dense paragraphs.
- Keep the design engaging enough that subscribers don't unsubscribe even when a specific email doesn't convert, since the presenter treats return engagement as part of the same asset.
Caveat: The $150M revenue figure is the presenter's agency claim, not a benchmark for any individual store.
Caveat: The presenter runs a paid agency; design judgment is his opinion, not a tested rule.

Tags: email-lifecycle, email-design, copywriting, creative-strategy, conversion-optimization, retention
Source: How to Design High Converting Ecommerce Emails In Figma.docx

---

## 'Button at the top' rule for non-scrollers
Use when: Designing or auditing the hero section of any promotional or lifecycle email where you need clicks from subscribers who never scroll.
- Put everything a customer needs to decide at the very top: logo, benefit/pain headline, one or two short sentences of body copy, and the CTA button — nothing below the first screen is required to act.
- Make the top button visually large; the presenter argues bigger buttons get more clicks and criticizes competitor emails where the hero button is small.
- Treat the top block as an elevator pitch: it should summarize the single offer or benefit, not educate or list features.
- Check where the fold actually lands on mobile in your ESP preview (the presenter reasons that most opens are mobile and non-scrollers never see below it).
- Place the CTA button directly below the hero copy rather than after a graphic, so a reader who stops after two sentences can still click.
Caveat: The exact fold position varies with device and ESP rendering; verify in preview rather than assuming a fixed pixel height.
Caveat: Making every button huge is the presenter's stylistic preference, not a tested universal rule.

Tags: email-lifecycle, email-design, product-page, conversion-optimization, button-design
Source: How to Design High Converting Ecommerce Emails In Figma.docx

---

## Email structure: hero, bridge, repeated CTAs, footer navigation
Use when: Building or templating a promotional email layout, or fixing an email where traffic stops partway down the page.
- Hero: headline calling out the pain or benefit, brief body copy, large CTA button, and a hero graphic.
- Bridge: justify the hero claim with short informational blocks — the presenter shows benefit bullets, checklists, icons and ingredient highlights rather than paragraphs — and include a CTA button at the end of the section.
- Add a final product or benefit section near the bottom with another CTA, so readers who scrolled the entire email still have a click target.
- Repeat the button at the end of every major section, because a reader who finishes a section and finds no button simply leaves.
- End with a footer containing 'shop by category' buttons (e.g., Men/Women) and additional links, to capture clicks from readers who reached the bottom but didn't want the featured product.
- Use a strong us-versus-them or comparison block near the end when the product's advantage needs to be made explicit before the closing CTA.
Caveat: The presenter's claim that category buttons in the footer recover lost clicks is his observation, not a measured result.
Caveat: Too many buttons can dilute the primary action — choose based on the email's single goal.

Tags: email-lifecycle, email-design, merchandising, conversion-optimization, cta-placement, email-structure
Source: How to Design High Converting Ecommerce Emails In Figma.docx

---

## Make the email scroll feel seamless with gradients and flowing backgrounds
Use when: Designing a long image-based email where readers drop off at section boundaries, or matching section backgrounds in Figma.
- Pick the main background color from the hero image or product photo so the palette is anchored to a real asset rather than chosen arbitrarily.
- Keep a consistent background color throughout the email instead of alternating white and colored blocks, which the presenter calls 'blocky' and associates with drop-off at section ends.
- Where two sections meet with slightly different shades, add a gradient rectangle that transitions from the top section's color to the bottom section's color so the seam disappears.
- Sample exact colors from the image or existing brand assets using Figma's color picker (eyedropper) so text, buttons and background stay matched.
- Repeat one accent color (e.g., the site's CTA red or an alert yellow) in small details — a discount bar, a 'last chance' label, button fills — to tie distant sections together.
- Preview the full email scrolled top to bottom to confirm no visible banding between sections.
Caveat: Gradients and background rectangles increase design complexity; the presenter uses a simpler first-pass layout before adding them.
Caveat: The link between smooth flow and higher scroll depth is the presenter's reasoning, not measured data.

Tags: email-lifecycle, email-design, figma, creative-strategy, conversion-optimization
Source: How to Design High Converting Ecommerce Emails In Figma.docx

---

## Skimmable copy: pain headline, one-sentence body, three selling points
Use when: Writing or editing the copy for a promo, launch or replenishment email, especially when the current draft is paragraph-heavy.
- Open with a headline that names the reader's pain or situation — the Bite example asks 'What's in your toothpaste matters?' — then differentiate in the body copy (e.g., 'we'll never include harsh chemicals, plastic tubes, or toxic fillers').
- Keep the largest body block in the email to roughly one sentence where every word is load-bearing; the presenter points out the biggest copy block in the Bite email is a single sentence.
- Limit the selling argument to three specific points even if the product has more features, reasoning that readers can only hold about three things at once.
- Move features into skimmable infographics — checklists, icons, timelines, short benefit labels highlighted larger than supporting text.
- Use bold only on your own claims in comparison blocks; the presenter deliberately left competitor points unbolded in his ButcherBox-for-Pets build so the brand's advantages read first.
- Structure the argument as: call out the problem, back it with punchy information, then tie in the product and stack the resulting benefits (e.g., healthier teeth, cleaner planet).
Caveat: The 'three things' limit and 3-second attention span are the presenter's heuristics, not measured thresholds.
Caveat: This style assumes a promo/consideration email; transactional emails may need more precise detail.

Tags: email-lifecycle, copywriting, customer-research, email-design, conversion-optimization
Source: How to Design High Converting Ecommerce Emails In Figma.docx

---

## Reverse-engineer competitor emails into a reusable copy template with ChatGPT
Use when: You need fast email copy drafts and have identified competitor emails whose structure and angle perform well in your category.
- Collect a competitor email that you consider well-written and structurally proven for your market (the presenter uses Bite's email as the model).
- Prompt ChatGPT to transcribe the email's copy into text.
- Ask it to analyse that copy and produce a reusable template describing the structural formula (headline type, body sequence, CTA placement, proof points).
- Supply your brand and product context, then ask it to write a new email following that exact template.
- Let the model ask for the angle and positioning, then answer with a specific hook — the presenter used 'if your soap is white and perfect looking it's probably fake' with an 'ancient craft' positioning.
- Review the output and edit before sending; the presenter says the draft took about two minutes and he would adjust details afterwards.
- Keep the template on file so future emails re-use the same structure with different angles instead of prompting from scratch.
Caveat: Treat output as a draft: verify claims, ingredient statements and any regulated language before sending.
Caveat: Copying a competitor's structure is the presenter's recommended practice, not legal advice on copying their copy verbatim.

Tags: email-lifecycle, copywriting, chatgpt, research, creative-strategy, positioning
Source: How to Design High Converting Ecommerce Emails In Figma.docx

---

## Build emails as stacked image slices, not one giant image
Use when: Producing an image-based email design and preparing assets for upload into Klaviyo, Omnisend or a similar ESP.
- Build the design inside a Figma frame, using roughly 600px width for the email as a starting dimension.
- Draw Figma 'slice' frames over each logical block and export at 2x, so each export is a manageable file rather than one email-length image.
- Slice by link destination, not just by visual section: because an image can only carry one link, split the footer logo, social icons and category buttons into separate slices with separate links.
- Compress the exported JPEGs before upload; the presenter uses iLoveIMG's compress tool and reports one set dropping from 4.4 MB to 1.26 MB (about 72% smaller).
- Upload the compressed images into the ESP and stack them in order, removing default image padding and side margins so the slices appear seamless.
- Assign one destination link per image, and add brief alt text (e.g., the headline) for the case where images don't load.
- Send a test email to your own inbox and check rendering and link behaviour before scheduling.
Caveat: Figma's slice tool and ESP padding controls may change; verify the current interface before relying on exact menu steps.
Caveat: Alt text is recommended but the presenter says he hasn't observed a clear deliverability impact from it.

Tags: email-lifecycle, figma, email-design, omnisend, klaviyo, image-optimization
Source: How to Design High Converting Ecommerce Emails In Figma.docx

---

## Hidden footer text to protect text-to-image deliverability ratio
Use when: Sending an email built mostly or entirely from images, where the HTML contains very little real text.
- Take a legitimate, on-brand text block such as your About Us copy and paste it at the very bottom of the email template.
- Set the font size very small (the presenter cites size 5), tighten line spacing (he cites around 5%), and set the font colour to match the background so it is effectively invisible to readers.
- Place it after the footer content so it doesn't interfere with the visible layout.
- Keep using real, relevant brand copy rather than keyword spam, so the block still reads as genuine email text if inspected.
- Verify the block doesn't break rendering or create extra scroll space by previewing the final email.
Caveat: This is presented as a workaround that 'tricks' filters; it may violate ESP or mailbox-provider terms and could backfire if detected.
Caveat: The presenter's claim that Gmail penalises image-heavy emails is his assertion, not documented platform policy; verify current deliverability guidance before adopting.

Tags: email-lifecycle, deliverability, email-design, spam-filters, technical-seo
Source: How to Design High Converting Ecommerce Emails In Figma.docx

---

## Laying out an email design in Figma without advanced tools
Use when: Starting a new email design from scratch and you need to establish section order before choosing images and colours.
- Create a Figma design file and draw a frame of about 600px width and a height long enough for the expected copy.
- Drop labelled text boxes for each section in order — logo, headline, body copy, CTA, graphic, sub-headline, body copy, infographic, CTA, footer — and size them roughly to the intended hierarchy (e.g., headline at ~30).
- Use this map to decide section order and see the whole email at a glance; the presenter recommends this specifically for getting unstuck when you don't know where to start.
- Import the brand logo and product images, dragging them into the frame; Figma shows centering guides automatically.
- Paste prepared copy from a document, then adjust fonts (the presenter used Montserrat) and weights (semibold rather than bold) to bring the layout to life.
- Build buttons by drawing a rectangle over the CTA text, grouping the two elements, and labelling the group (e.g., 'button one') so it can be copied and reused throughout the email.
- Choose the palette after the hero image is placed, sampling from it, so gradients and accent colours match real assets.
Caveat: Figma's menus and features change; verify current panel names if following step-by-step.
Caveat: This walkthrough deliberately skips copywriting — bring finished copy into the layout rather than writing in Figma.

Tags: email-lifecycle, figma, email-design, creative-strategy, workflow
Source: How to Design High Converting Ecommerce Emails In Figma.docx

---

## Us-versus-them comparison block built with icon checkmarks
Use when: Writing the bridge or product-proof section of an email where the differentiator needs to be stated clearly (e.g., ingredient quality, sourcing, process).
- Place your brand on one side and a generic competitor label (e.g., 'most human-grade brands') on the other, using the logo and a simple 'us'/'them' header.
- List your claims as short text points on your side and the corresponding competitor claims opposite; the presenter bolded only his brand's points to make them read first.
- Add a checkmark icon to each of your points and an X icon to each competitor point; the presenter downloads free icons from the Noun Project.
- Enclose each column in a rounded rectangle (Figma corner radius around 20) with a stroke outline, using a neutral background for the competitor column and white for yours so your side stands out.
- Place the comparison in the bridge section, after the hero and before the final CTA, then repeat the CTA button immediately after it.
- Keep the list short and skimmable — supporting copy above it should summarise the single strongest claim (e.g., 'not all human-grade dog food is created equal').
Caveat: Comparative claims about competitors can carry legal and platform-advertising risk; substantiate any factual claim before publishing.
Caveat: The presenter chose not to bold competitor points; this is a style choice, not a rule.

Tags: email-lifecycle, copywriting, email-design, positioning, figma, creative-strategy
Source: How to Design High Converting Ecommerce Emails In Figma.docx

---

## Put footer navigation to work for non-buyers
Use when: Designing the bottom of a promotional email where the featured product may not match every reader.
- Repeat the primary CTA (e.g., a link to a plan-builder or quiz) as the lead footer element so scrollers land on the main action.
- Add 'shop by category' buttons covering your main ranges so readers whose interest wasn't the featured product can still enter the store.
- Include a small number of social links and a website link for readers not ready to buy.
- In the Figma build, split these footer elements into separate slices so each button and icon can carry its own destination link.
- Reinforce accent colours by giving the footer its own subtle background shape so it doesn't float without visual anchoring.
Caveat: The presenter asserts this captures clicks from readers who reached the bottom, but provides no measured uplift data.

Tags: email-lifecycle, merchandising, email-design, email-structure, conversion-optimization
Source: How to Design High Converting Ecommerce Emails In Figma.docx

---

## Upload a finished image-design email into an ESP as stacked images
Use when: Publishing an image-based email built in Figma into Omnisend, Klaviyo or a similar platform.
- Create the campaign in the ESP, entering the subject line and preheader text (the presenter uses 'Last chance for 20% off' with preheader 'Open for your last gift opportunity').
- Open any template to get a canvas, then delete the template blocks so you start from an empty email.
- Add image elements one by one and upload your compressed slices, stacking them in the exact order they appear in the design.
- Select each image block and remove image padding plus any frame side padding so the stacked slices align edge to edge and look like one continuous design.
- Assign the destination link for each image — one link per image — and add short alt text describing the image.
- Preview and send a test email to your own address, checking that the unsubscribe link is present (the ESP added one automatically in the walkthrough) and that links and rendering are correct.
- Choose recipients — all subscribers or a specific segment with exclusions — review, then send.
Caveat: Omnisend and other ESP interfaces change frequently; verify current campaign, padding and image-upload controls.
Caveat: Sending entirely image-based emails means text-only recipients see alt text, so keep alt text meaningful.

Tags: email-lifecycle, omnisend, klaviyo, email-design, campaign-setup, checkout
Source: How to Design High Converting Ecommerce Emails In Figma.docx

---

## Image-only vs text-and-HTML emails: the presenter's position
Use when: Deciding whether to build an email as stacked images or as HTML text with styled blocks.
- Consider the presenter's evidence: he claims all of the 20-plus 7-9 figure brands he has worked with use image-only emails, and cites one roughly $200M/year brand doing so.
- Weigh that against the costs: all content depends on images loading, so blocked images reduce the email to alt text, and text is not selectable, searchable or easy to edit.
- If you go image-only, invest in the mitigating steps the presenter describes — compressed slices for load speed, alt text on every image, and hidden on-brand text at the bottom for deliverability ratio.
- Still build a plain-text or HTML text version where your ESP supports it, so readers with images disabled get the offer and CTA.
- Test rendering in your own inbox and in a preview tool before sending to the full list.
Caveat: This is the presenter's opinion, partly informed by his agency's client base; it is not an established rule and contradicts common deliverability and accessibility guidance.
Caveat: Image-only emails impair accessibility for screen readers and readers with images off — a real risk the source does not address.

Tags: email-lifecycle, email-design, deliverability, accessibility, conversion-optimization
Source: How to Design High Converting Ecommerce Emails In Figma.docx

---

## Compress and slice images to protect load time in the inbox
Use when: Exporting a long designed email from Figma and preparing the files for ESP upload.
- Avoid exporting the entire email as one image; the presenter's stated reason is file size and slow loading in the inbox.
- Slice the design into section-sized images and export at 2x for retina rendering.
- Run all exports through an image compressor (the presenter uses iLoveIMG's compress image tool) before uploading.
- Check the resulting file sizes; the presenter reports a sample set going from 4.4 MB to 1.26 MB after compression, roughly a 72% reduction, and treats smaller as better for load speed.
- Upload the compressed files to the ESP and confirm they display at full width without visible quality loss or seams between slices.
Caveat: The 4.4 MB to 1.26 MB figure is one example from the walkthrough, not a target threshold for every email.
Caveat: Compression settings vary by tool; check quality after compressing rather than assuming it is lossless.

Tags: email-lifecycle, image-optimization, figma, performance, email-design
Source: How to Design High Converting Ecommerce Emails In Figma.docx

---

## Design principles that keep emails converting and subscribers subscribed
Use when: Finishing or reviewing an email design before upload, especially when the layout works but feels flat or off-brand.
- Use large buttons throughout the email; the presenter points to Gymshark's oversized hero CTA as the model and says the bigger the button the more clicks.
- Match accent colours across sections — the Gymshark example repeats green across image borders, callouts and buttons, and the presenter's own build carries the site's red through the discount bar, button and 'last chance' label.
- Apply small depth details: a border and shadow on the button to give it a 3D feel, and a coloured border around the hero image so it pops against the background.
- Use infographics instead of paragraphs — checklists, icons, comparison graphs (the presenter shows a graph making gummies look better than tablets) and highlighted key words.
- Vary text weight (semibold vs regular, larger vs smaller) to create hierarchy rather than setting everything the same.
- Add lifestyle or product imagery to finish the email and bring colour and realism into the layout.
- Keep it restrained: the presenter's summary is to take the basics and elevate them rather than exploding the email with crazy colours.
Caveat: Bigger buttons and repeated accent colours are the presenter's design opinions, supported by examples rather than controlled tests.
Caveat: Engagement-focused design may not convert on a single send; the presenter frames it as protecting long-term subscriber engagement.

Tags: email-lifecycle, email-design, creative-strategy, conversion-optimization, figma
Source: How to Design High Converting Ecommerce Emails In Figma.docx

---

## Use conversational messaging to resolve product-purchase friction
Use when: When shoppers need help with product fit, compatibility or a cart decision.
- Audit messages for a concrete question the shopper can answer easily.
- Identify the store and use natural, clear language rather than pretending an automated message is a personal friend.
- Route replies to someone able to answer product, delivery and returns questions.
- Use the supported messaging channel for the recipient; do not assume blue bubbles improve every audience.
Caveat: The source promotes an iMessage tool; its claimed channel advantage is not independently established.

Tags: email-lifecycle, sms, conversational-commerce, cart-recovery
Source: If I Started SMS Marketing in 2026, I'd Do This.docx

---

## Reduce signup fields while retaining clear messaging consent
Use when: When simplifying a store text-message signup form.
- Collect only information needed for this signup and a useful follow-up.
- Keep the marketing permission and sender purpose clear; a phone number alone is not the marketing opt-in.
- Do not remove information the checkout needs to fulfill the order.
- Compare signup completion with downstream replies, purchases and opt-outs.
Caveat: Merchant adaptation of the source form-friction principle.

Tags: email-lifecycle, sms, conversational-commerce, signup-forms, list-growth
Source: If I Started SMS Marketing in 2026, I'd Do This.docx

---

## Test concise conversational welcome messages
Use when: When welcoming a shopper who opted into the store messaging program.
- Deliver any promised signup benefit and identify the store.
- Ask one useful question about product preferences or intended use if a response will change the help offered.
- The source suggests a five-minute delay and short copy; test timing within applicable send-time and message-count controls.
- Do not split one message into several merely to simulate a human or satisfy an arbitrary length limit.
Caveat: The source five-minute and 80-character preferences are heuristics, not optimal limits or billing rules.

Tags: email-lifecycle, sms, conversational-commerce, welcome-flow, copywriting
Source: If I Started SMS Marketing in 2026, I'd Do This.docx

---

## Hand product questions to a trained human
Use when: When a messaging flow receives replies requiring individualized help.
- Route replies to the support or product-specialist queue.
- Carry forward the relevant product and order context so the shopper does not repeat it.
- Answer the question and offer the appropriate product, size guide or cart link.
- Set a realistic response target and communicate availability.
Caveat: Human support requires staffing; the source response-rate anecdotes do not establish purchase uplift.

Tags: email-lifecycle, sms, conversational-commerce, customer-support, handoff
Source: If I Started SMS Marketing in 2026, I'd Do This.docx

---

## Use short product demos to answer a shopper question
Use when: When a opted-in conversation needs a clearer product explanation than text.
- Choose a short product demonstration or voice explanation only when the channel and shopper support it.
- Use the actual SKU and answer the specific question.
- Provide a text alternative when media is inaccessible or unavailable.
- Compare resolution and purchase outcomes with text-only support against production effort.
Caveat: Merchant application of the source multimedia conversation idea; channel capabilities and costs differ.

Tags: email-lifecycle, sms, conversational-commerce, product-demo
Source: If I Started SMS Marketing in 2026, I'd Do This.docx

---

## Measure conversational messaging by purchases and support outcomes
Use when: When evaluating store messaging flows or comparing supported channels.
- Track delivery, replies, opt-outs, support resolution, purchases and net contribution after messaging cost.
- Use consistent attribution windows and a comparable control when estimating incremental impact.
- Separate product inquiries from service appointment show-up or sales-call close rates.
- Treat the source reported twofold reply lift as an unverified vendor example, not expected purchase lift.
Caveat: Replies alone do not establish revenue impact.

Tags: email-lifecycle, sms, conversational-commerce, measurement, experiment-design
Source: If I Started SMS Marketing in 2026, I'd Do This.docx

---

## Email System Build Order: List Growth → Flows → Campaigns → Tests → Deliverability → AI
Use when: Planning an email marketing roadmap or auditing why email revenue is flat before buying new tactics or tools.
- Sequence work as: (1) list growth via high-converting signup forms, (2) core automated flows, (3) campaigns, (4) A/B testing, (5) segmentation, (6) deliverability, (7) AI to accelerate production.
- Justify the order: campaigns and flows monetize a list, so a weak capture layer caps everything downstream — no list growth means flow and campaign optimization has nothing to work on.
- Diagnose your store against the three gaps the source names: missing key flows, campaigns sent without a strategy, and trying to fix performance without knowing which underlying layer is broken.
- Deliverable: an audit of your own ESP account listing what to build, what to fix, and where the largest revenue opportunity sits — before adding new tools.
- Use the audit output to decide whether the next project is signup form optimization, a missing flow, or a campaign calendar, rather than doing all three at once.
Caveat: The order is the source's recommended build sequence for a new or underbuilt program; a mature program may need a different entry point based on measured gaps.
Caveat: No numeric benchmark is attached to the roadmap itself — the individual layers carry their own source-specific figures.

Tags: email-lifecycle, email-marketing, strategy, audit, automation, segmentation, deliverability
Source: Klaviyo email.docx

---

## Signup Form Offer Design and Margin Math
Use when: Choosing or refreshing the incentive on the popup, full-page or embedded opt-in form on the store.
- Treat the offer as the biggest lever on signup rate, ahead of design: the source states a strong offer with poor design still outperforms a poor offer beautifully designed.
- Offer types to test: buy one get one free; buy one get one at 50% off; free gift with purchase of X; free digital product; free shipping; fixed dollar amount off; dollar amount off over a threshold; percentage off; percentage off over a threshold; percentage off a subscription; cashback; early access to a sale; mystery discount (source's personal favorite).
- Evaluate each variant holistically: factor profit margin, signup rate, the welcome flow's conversion rate, and the revenue attributed to that welcome flow — not just the opt-in rate.
- If AOV is around $200, the source notes $20 off and 10% off are equivalent in value but $20 off carries higher perceived value; still confirm with your own split test.
- Note the source's general claim that anything under 10% off is less effective, and treat it as a starting hypothesis for testing rather than a rule.
- When the offer changes, update the headline, CTA button and any teaser/quiz copy so the promise is consistent across every step of the form.
Caveat: The sub-10% and $200 AOV figures are the source's heuristics, not established benchmarks — discount depth must be validated against your own margin structure.
Caveat: Aggressive discounting can train customers to wait for discounts and compress margin; the source does not model this trade-off.

Tags: email-lifecycle, offer-design, list-growth, signup-form, pricing, experiment-design, margin
Source: Klaviyo email.docx

---

## Standard Popup Structure: One Headline, One Field, One CTA, One Microcopy
Use when: Designing or auditing the layout of a desktop popup opt-in or full-page signup form.
- Use this structure: offer stated in the headline; one input field per step; a benefit-driven CTA button; a microcopy line under the button.
- Write the headline as the offer itself, e.g. 'Unlock 20% off your first order'. Do not hide the offer in body copy under a generic greeting — the source treats this as one of the most common mistakes.
- Delete sub-headlines like 'Sign up for special offers and updates' — the source argues the value is self-evident and the block adds friction.
- Simplify the email field placeholder to something like 'Enter your email here' so the expected input is unambiguous.
- Style the input field background so it stands out from the popup background (e.g. light grey field on white popup) to make it easier to find.
- Avoid the words 'sign up' and 'subscribe' in both the headline and CTA; instead state what the visitor gets, e.g. 'Get my discount now'.
- Add a microcopy line under the CTA giving a second, less attractive option, e.g. 'No thanks'. The source cites research that two options make people likelier to choose than a single CTA.
- Remove the US disclaimer text about agreeing to receive marketing email; if you sell into the EU, retention of privacy disclosures is a legal question the source flags rather than resolves.
- Remove any 'no thanks' alternative that competes with the CTA, and remove supporting text boxes describing your promotions.
Caveat: The 'remove US disclaimer' advice is the source's US-specific claim; EU privacy rules are explicitly said to be different — confirm with counsel for your markets.
Caveat: The two-option microcopy relies on cited research the source does not name; test it on your own audience.

Tags: email-lifecycle, signup-form, conversion-optimization, copywriting, offer-design, list-growth
Source: Klaviyo email.docx

---

## Micro-Commitment (Micro-Yes) Step Before the Email Field
Use when: Optimizing the opt-in form flow on a popup to raise email capture rate.
- Clone the email opt-in step and place a stripped-down version before it: remove the input field, change the primary CTA to something like 'Yes please', and keep a secondary 'No thanks'.
- Frame the question as the offer, e.g. 'Do you want 20% off your first order?', with emphasis on the number.
- Clicking 'Yes please' advances to the email field step; clicking 'No thanks' closes the form.
- Make the two-step flow visually coherent: logo, headline, one field or one question per screen.
- Split test the micro-yes step on versus off; the source reports testing across more than 40 ecommerce brands where it usually increased signup conversion, but it is not universal.
- Run the test separately on desktop and mobile, since the source says the micro step can win on one device and lose on the other.
- Judge the result on total signups and downstream welcome-flow revenue, not on signup rate in isolation.
Caveat: The 40-plus-brand experience is the source's own client work, not a controlled benchmark — treat as directional evidence, not a guarantee.
Caveat: If the step is added without a clean 'No thanks' exit, the form becomes a dark pattern and may increase closes or complaints.

Tags: email-lifecycle, signup-form, conversion-optimization, experiment-design, list-growth, zero-party-data
Source: Klaviyo email.docx

---

## Timing, Frequency and Device Targeting Rules for Popups
Use when: Configuring when and how often the opt-in popup fires on the storefront, generally or per device.
- Do not show the form immediately on load; switch targeting from 'immediately' to rule-based display so a visitor exiting right away is not interrupted.
- Set a starting delay of about 6 seconds as the source's default, and test within a 4–12 second range. Too short disrupts the visit and reads as spam; too long means fewer visitors ever see the form, so a high signup rate on tiny volume still yields few subscribers.
- Layer a scroll condition, with about 60% as the source's starting point, and optionally a minimum pages-viewed condition. The source leaves these conditions non-mandatory (AND logic off).
- Handle repeat exposure: set the closed form to re-display after about 3 days instead of the default 5.
- Build one desktop-only form and one mobile-only form rather than a single responsive form, so layout, timing and copy can differ by device and A/B results are not mixed.
- On mobile, disable the exit-intent trigger — the source calls mobile exit intent unreliable and says it fires when people are not leaving, harming experience.
- Exclude existing subscribers (e.g. 'don't show to existing profiles'), the cart page and the checkout page so visitors already about to purchase are not offered a discount, and exclude wholesale or other non-retail pages.
- If you only ship to one country, restrict display by location so the offer is relevant.
Caveat: The 6-second delay, 4–12 second range, 60% scroll and 3-day re-show are the source's recommended starting points, framed as things to split test rather than fixed rules.
Caveat: Excluding the cart and checkout pages is a deliberate choice to protect full-price orders; if your checkout abandonment is high, test the alternative before assuming it is right for you.

Tags: email-lifecycle, signup-form, popup-targeting, conversion-optimization, mobile, experiment-design
Source: Klaviyo email.docx

---

## Teaser / Floating Button Configuration
Use when: Adding or reviewing the teaser (Klaviyo) or floating button (Aliyah/Shopify app) that accompanies the opt-in popup.
- Enable the teaser so it displays both before the form appears and after the form is closed.
- On desktop, use a rectangular teaser carrying short offer text such as 'Save 20%' rather than a generic gift icon; style it for contrast (e.g. black background, white centered text).
- On mobile, switch the teaser to a circle and shorten the text so it does not occupy the full bottom bar — the source notes that stacked elements such as loyalty promotions can collide with a full-width bar.
- Verify the teaser does not overlap checkout, cart or other persistent UI.
- Split test teaser present versus absent; the source reports the teaser lifts both signup rate and the absolute number of subscribers.
Caveat: The claim that the teaser lifts both rate and absolute subscribers comes from the source's own testing and is not quantified.
Caveat: If your storefront already has several floating elements, a persistent teaser may add clutter; the source itself acknowledges this case.

Tags: email-lifecycle, signup-form, list-growth, conversion-optimization, mobile, merchandising
Source: Klaviyo email.docx

---

## Post-Opt-In Success Page: Withhold the Code, Train Email Opens
Use when: Writing the success/confirmation screen copy that appears after a visitor submits their email on the opt-in form.
- Make the success page visually identical to the form: same logo, same fonts, same colours.
- Write a future-pacing headline such as 'Your discount code is on its way' rather than revealing the code.
- Add instructions: check your inbox for the confirmation message containing the discount code.
- Add the fallback line: if no email arrives within 5 minutes, check your spam folder — the source says this pre-empts support tickets caused by deliverability issues.
- The source deliberately does not display the discount code on this page, arguing it removes any reason to open the first welcome email; a low open rate on a brand-new subscriber's very first email is a negative signal to inbox providers.
- Test the alternative if you have strong reason to believe instant code delivery converts better for your audience; the source acknowledges this is an active industry debate and states its own position rather than a universal rule.
Caveat: Holding back the code risks losing subscribers who never check email; this is the deliberate trade-off the source chooses, not a proven best practice.
Caveat: The deliverability reasoning is the presenter's explanation, not a documented provider policy.

Tags: email-lifecycle, signup-form, deliverability, welcome-flow, retention, list-growth
Source: Klaviyo email.docx

---

## Separate Desktop and Mobile Signup Forms
Use when: Adapting an existing opt-in popup for mobile traffic, or before starting device-level A/B tests.
- Clone the desktop form, name it as the mobile version, and set device targeting to mobile only; leave the original on desktop only.
- Remove the exit-intent rule on mobile because the trigger is unreliable there.
- Audit every element for size: check that fonts are legible and that nothing overflows the viewport.
- Increase the call-to-action button height (the source uses about 70 px) and raise CTA label size (about 30 px) so the button is comfortably tappable.
- Raise secondary action text (e.g. 'No thanks') to about 18 px.
- Increase emphasis sizes where the offer number appears inside the form (source uses 60 px in the micro-commitment step).
- Raise the input field height (about 70 px) and input text size (about 20 px) via the general styling settings.
- Increase success-page body text to about 22 px.
- Skip images on mobile entirely where possible, or compress the logo, because mobile load time depends on the visitor's connection — the source says images are a common conversion killer.
Caveat: Pixel sizes are the source's working values on a specific ESP builder and reproduce that presenter's config, not a universal standard; verify against your own template and your current interface.
Caveat: Because results can differ by device, keep desktop and mobile tested and reported separately rather than averaging them.

Tags: email-lifecycle, signup-form, mobile, conversion-optimization, experiment-design, page-speed
Source: Klaviyo email.docx

---

## Redirect Your Signup Offer Away From Cart and Checkout Traffic
Use when: Configuring URL inclusion and exclusion rules for the opt-in popup on an ecommerce store.
- Exclude the cart page from popup display so a visitor mid-cart is not interrupted or re-priced.
- Exclude the checkout page so a visitor about to purchase at full price is not offered a discount.
- Exclude wholesale, B2B or other non-retail pages where the consumer offer is irrelevant.
- Keep display on product, collection, homepage and content pages where the visitor is still exploring and the capture is additive.
- Review exclusions whenever the theme changes URLs or SPAs change the path structure, since URL rules can silently stop matching.
Caveat: This reduces capture volume in exchange for protecting full-price conversion; if your cart or checkout abandonment is high, test whether the loss of capture outweighs the protection.
Caveat: Excluding checkout does not solve abandonment — it must be paired with an abandoned-checkout flow.

Tags: email-lifecycle, signup-form, cart-abandonment, conversion-optimization, popup-targeting, checkout
Source: Klaviyo email.docx

---

## Compress Signup Form Images to Protect Load Time
Use when: Preparing product or lifestyle imagery for a signup popup, full-page form or landing page opt-in.
- Compress images externally before uploading to the email platform; the source names TinyPNG and Squoosh.
- Upload the compressed file to the form builder only after compression, because large originals slow the form down and long load times suppress conversion.
- Write descriptive alt text for every image, including the logo — alt text is what visitors see when an image fails to load.
- For mobile forms, avoid images altogether and compress the logo if you keep it, since mobile load speed depends on the visitor's connection.
- Check that the logo or hero image does not push the email field below the fold on small screens.
Caveat: Compression tools are third-party products whose interfaces and settings change — verify the current workflow before relying on instructions.
Caveat: The source claims load time is a major conversion killer but gives no measured threshold for image weight.

Tags: email-lifecycle, signup-form, page-speed, conversion-optimization, mobile, creative-assets
Source: Klaviyo email.docx

---

## Ten Common Signup Form Mistakes to Audit Against
Use when: Reviewing an underperforming opt-in form or onboarding a store's existing email capture setup.
- Offer too weak: if the incentive is not compelling, fix that first — the source ranks it above every design issue.
- Asking too much in one step: collect email, phone, first name, birthday and similar data in separate steps; if you collect phone number or other fields, add them after the email step. The source warns that visitors willing to give an email but not a phone number may abandon the whole form, losing the email entirely.
- Time delay too short or too long: balance visibility against positive experience (see delay guidance in the timing card).
- Form too small: the source's guidance is that a bigger form captures attention better, and suggests testing popup versus full-screen.
- Too much copy: no supporting text blocks explaining that subscribers will receive offers and promotions.
- Offer missing from the headline: the offer should be the first thing read, not buried in body copy.
- 'Sign up' / 'subscribe' language in headline or CTA: replace with the benefit.
- Single form for both devices: build and test desktop and mobile separately.
- Slow-loading form: compress images; skip images on mobile.
- Incentive revealed on the success page: direct people to the inbox instead (source's position; an industry debate).
Caveat: These are the source's observed common mistakes, not a validated ranking of conversion impact beyond the stated ordering of offer first.
Caveat: The phone-number advice assumes email is the primary identifier for your program; SMS-first brands may order capture differently.

Tags: email-lifecycle, signup-form, audit, conversion-optimization, list-growth, mobile
Source: Klaviyo email.docx

---

## Signup Form A/B Test Priority Order
Use when: Planning the next round of opt-in experiments, or deciding which variable to change when form volume is too low to test everything at once.
- Test 1 — offer: the highest-leverage variable; a strong offer with weak design beats a weak offer with strong design per the source.
- Test 2 — micro-commitment step on versus off: usually lifts conversion but not for every audience.
- Test 3 — time delay: a shorter delay raises signup rate but lowers total signups, so judge on total signups.
- Test 4 — popup versus full-page form: full-page has greater visibility and wins for some brands.
- Test 5 — headline copy, e.g. 'Save 20% now', 'Get 20% now', 'Take 20% now', 'Unlock 20% off now', 'Your discount awaits', 'Do you want 20% off?'.
- Test 6 — CTA button copy, e.g. 'Save 20% off now', 'Get 20% off now', 'Unlock my discount now', 'Reveal my discount now', 'I want my discount'.
- Test 7 — microcopy under the CTA: test variants such as 'No thanks', 'No thanks, I'll pay full price', 'No spam guaranteed', or social proof like 'Rated 4.9/5 by 5,000 customers', and test having microcopy versus none.
- Test 8 — colour and design: plain versus fully designed form, light versus dark form, input field colour, CTA colour. Lower leverage than the above.
- Test 9 — image versus no image: an image can distract from the form, so test both; also test different images (the source gives a client example where an image with a dog far outperformed one without, and explicitly warns against generalising that).
- Test 10 — SMS opt-in angle: same 20%-off question framed for phone capture, a higher discount for SMS than for email (e.g. 10% email vs 20% SMS), or positioning the SMS list as a VIP club.
Caveat: Priority order is the presenter's ranking of leverage, not a measured effect-size table.
Caveat: Most variables are low-leverage; do not spend signup-form test volume on colour before offer and flow structure are settled.
Caveat: Each audience differs, so a variable that wins elsewhere may lose here.

Tags: email-lifecycle, signup-form, experiment-design, conversion-optimization, offer-design, sms
Source: Klaviyo email.docx

---

## Configure a Signup A/B Test: Manual 50/50 and Winner Selection
Use when: Launching an A/B test on a popup or form inside your email platform.
- Create the test from the existing form, name it for the variable under test (e.g. 'offer test').
- Set variant A as the current control and variant B as the challenger, then update every dependent element of variant B — for an offer test that means the headline, the email opt-in, the teaser and the form's design copy all reflect the new offer.
- In test settings, set the traffic weight to manual 50/50 rather than automatic; the source's stated reason is that automatic allocation can favour a variant before there is enough volume to justify the conclusion.
- Enable winner selection but do not automatically end the test, so a human reviews the result before rollout.
- Measure on the same holistic basis used for offer decisions — signup rate plus welcome-flow conversion and attributed welcome-flow revenue — not signup rate alone.
- Run device-specific tests separately rather than pooling desktop and mobile results.
Caveat: The manual 50/50 preference is the presenter's stance, and it costs statistical efficiency compared with adaptive allocation; it trades speed for the operator's control.
Caveat: No minimum sample size is given; you must set your own stopping rule before reading results.

Tags: email-lifecycle, experiment-design, signup-form, measurement, conversion-optimization, platform-tools
Source: Klaviyo email.docx

---

## Full-Screen Opt-In Forms and Zero-Party Data Quizzes
Use when: Choosing a capture format, or adding a segmentation question at the point of opt-in for a Shopify store.
- Consider full-screen forms on both desktop and mobile rather than small popups, which the source argues hurt conversion; full-screen formats allow full brand treatment with background and imagery.
- Lead with one question — the source recommends keeping it to a single question even though multi-question quizzes are possible — such as 'What are you shopping for today, myself or someone else?'.
- Ask for motivation-relevant segmentation, e.g. for a health brand: lose weight, build muscle, or improve general health; for a gift-focused store, the recipient.
- Use a 'No thanks' exit so the full-screen takeover is escapable.
- Pass the zero-party answers through the platform integration into your email list so they become segmentation properties on the subscriber profile.
- Review survey-answer performance reporting to see which answers correlate with higher purchase behaviour, then weight acquisition and campaign targeting toward those segments.
Caveat: Full-screen popups are more intrusive; the source argues the format win justifies it, but this is not presented as a cross-store benchmark.
Caveat: Collecting a question before the email adds a step; the source argues the micro-commitment outweighs the friction, but it must be tested.
Caveat: Integration availability and the exact question/report UI vary by platform and change over time — verify the current interface.

Tags: email-lifecycle, zero-party-data, signup-form, segmentation, list-growth, shopify, conversion-optimization
Source: Klaviyo email.docx

---

## Gamified Opt-In First Steps: Spin-to-Win and Scratch-Off
Use when: Choosing the opening interaction on a full-screen capture form to raise engagement and signup rate.
- Spin-to-win: configure the wheel so every visitor receives a reward — the wheel always lands on the designated reward slice, and you may display other slices as decoy rewards. Choose the reward value (e.g. 5% or 10%).
- Scratch-off: use the interactive scratch surface with framing copy such as 'Try your luck — scratch below to see what you win'; the reward is revealed on scratch, producing a first brand interaction before the email ask.
- Place the mechanic as the first step, before the email field, so it functions as a micro-commitment.
- Split test the gamified first step against a mini quiz and against a plain yes/no micro-commitment; the source reports the mini quiz or scratch-off usually win, but says every audience differs.
- Judge on total subscribers and downstream revenue, not just the completion rate of the mechanic.
- If you already run a strong baseline, test one mechanic at a time so you can attribute the change.
Caveat: The source relates one brand moving from about 11% to about 14% conversion after adding a scratch-off, and separately a scratch-off revealing a discount; this is a single client anecdote, not a promised result.
Caveat: The scratch-off is described as a newer feature; availability and behaviour should be verified in the current platform interface.
Caveat: Decoy reward slices on a rigged wheel create a misleading expectation — weigh the engagement gain against trust and any local consumer-protection rules.

Tags: email-lifecycle, gamification, signup-form, conversion-optimization, experiment-design, list-growth
Source: Klaviyo email.docx

---

## Deliverability Hygiene: Authentication, Engagement Tiers and List Cleaning
Use when: Setting up or auditing sending infrastructure and list health, especially before scaling campaign volume.
- Implement the technical authentication trio — SPF, DKIM and DMARC — on your sending domain so mailbox providers can verify you.
- Segment by engagement recency using activity windows; the source names 14-day, 30-day, 60-day and 90-day active tiers as the segmentation structure.
- Use those tiers to differentiate sending: mail the most recently engaged tiers most often and reduce frequency or exclude the least engaged tiers.
- Clean the list by suppressing profiles that have been inactive past 180 days — the source's stated list-cleaning benchmark.
- Monitor inbox placement and sender reputation, particularly as AI-driven inbox curation changes how mail is sorted and surfaced.
- Re-check authentication records and suppression rules after any change of sending domain, ESP or marketing platform.
Caveat: The 180-day suppression threshold and the 14/30/60/90-day windows are the source's heuristics, not calculations derived from your data — adjust for your purchase cycle and list size.
Caveat: Suppressing inactive profiles reduces list size and can reduce short-term revenue; the source frames it as necessary for placement.
Caveat: Authentication setup depends on your DNS provider and ESP interface, both of which change — verify current configuration steps.

Tags: email-lifecycle, deliverability, list-hygiene, segmentation, suppression, infrastructure
Source: Klaviyo email.docx

---

## Core Automated Flows to Build and the 72-Hour Purchase Window
Use when: Deciding which lifecycle automations to build or fix next in an ecommerce email program.
- Build the five core flows: Welcome, Browse Abandonment, Abandoned Cart, Abandoned Checkout, and Post-Purchase.
- Front-load the welcome flow: the source identifies the first 72 hours as the critical purchase window, with day zero driving the highest conversion volume.
- Because day zero is the strongest, make the first welcome message carry the clearest offer and the clearest instruction (including where the discount code is), rather than saving the strongest message for later in the sequence.
- Pair each core flow with the capture and campaign layers so browse, cart and checkout abandonment have a path back to purchase.
- Review which flows exist and which are missing before adding new campaign volume — the source names missing key flows as one of the three common reasons email revenue is flat.
Caveat: The 72-hour window and day-zero emphasis are the source's framing of welcome-flow behaviour, not a benchmark tied to a specific dataset shown.
Caveat: Post-purchase flows serve retention, review and replenishment goals rather than immediate conversion; do not judge them purely on attributed revenue in the first days.

Tags: email-lifecycle, automation, welcome-flow, abandoned-cart, post-purchase, retention, prioritization
Source: Klaviyo email.docx

---

## Email Campaign Cadence and Audience Strategy
Use when: Setting or reviewing the weekly campaign calendar and checking whether sends are strategic or random.
- Use 3 to 4 campaigns per week as the source's recommended cadence reference point for the campaign layer of the email system.
- Ensure campaigns sit on top of a working list-growth and flow layer; the source names 'sending campaigns without a real strategy' as a common failure mode.
- Align campaign sends to the engagement tiers established for deliverability so higher-frequency sends go to more recently active subscribers.
- Treat the cadence as a starting hypothesis tied to list size and engagement — do not adopt it unchanged if your list is small or your engagement tiers are thin.
- Review performance by segment rather than as a blended average, so a strong campaign to an engaged tier is not obscured by weak delivery to inactive profiles.
Caveat: The 3–4 per week figure is the source's recommendation, not a derived benchmark, and should be adjusted to list size, purchase cycle and engagement.
Caveat: Sending more frequently into unengaged segments increases complaint and spam risk, which works against the deliverability practices the same source recommends.

Tags: email-lifecycle, campaigns, cadence, segmentation, deliverability, planning
Source: Klaviyo email.docx

---

## Use AI and Personalisation Tools Only After the Fundamentals Are In Place
Use when: Deciding whether to invest in AI personalisation, quiz tools or advanced targeting features before fixing list growth, flows or deliverability.
- Fix capture, flows, campaigns, segmentation and deliverability first; the source's stated reason is that most brands are missing key flows, sending without strategy, or treating symptoms, so advanced features amplify a broken base rather than fixing it.
- Once the base works, add active gamification (spin-to-win, scratch-offs) and zero-party data collection quizzes to lift engagement and enrich profiles.
- Split test distinct desktop and mobile experiences rather than assuming one experience transfers, because results diverge by device.
- Route collected zero-party data into segmentation so it drives targeting and campaign decisions instead of sitting unused in the capture tool.
- Re-evaluate the tool stack only when a measured gap remains after the fundamentals are in place.
Caveat: The source is explicit that AI is a speed-and-efficiency layer applied last, not a solution to a missing flow or a deliverability problem.
Caveat: Tool availability and integration behaviour change frequently; verify current capabilities in the interfaces you use.

Tags: email-lifecycle, ai, personalization, zero-party-data, strategy, prioritization, experiment-design
Source: Klaviyo email.docx

---

## Choose a popup first step: scratch-off, quiz, or micro-commitment
Use when: Deciding how to structure the first screen of your email capture popup so more store visitors begin the signup interaction.
- Recall the source's claimed example: for one ecom brand already converting at 11%, adding a scratch-off first step correlated with a move to 14%. Treat this as a single-case example, not a benchmark.
- Pick scratch-off or mini quiz as your primary test if you want a more engaging, gamified first interaction with the brand; the source presenter rates these as likely to outperform older formats, based on what they see across client accounts.
- Keep the older micro-commitment pattern as a backup test: a simple yes/no frame like 'claim 10% off or no thanks', or 'do you want a mystery discount?' followed by the email field. It still produces a decent signup rate.
- Optionally test skipping the first step entirely and showing the email opt-in immediately. Both presenters advise against it, but it can suit audiences that don't respond to games.
- Run the formats as real A/B tests on your own traffic and keep the winner, rather than adopting any one format permanently.
Caveat: The 11% to 14% lift is a source-reported client result, not a guaranteed outcome.
Caveat: The claim that quiz and scratch-off will 'probably' outperform micro-commitment is the presenter's observation, not a measured universal rule.

Tags: email-lifecycle, list-growth, popup-forms, conversion-optimization, experiment-design, signup-rate, lead-capture
Source: Klaviyo email.docx

---

## Decide whether the popup success page reveals the discount code or sends to email
Use when: Configuring the success/reward step of your email signup popup and choosing between showing the discount immediately or routing the subscriber to their inbox.
- Option A (source presenter's preference): show no reward on the success page. Use a plain 'you're in' confirmation plus copy telling them to check their inbox for the code, and to check spam or the promotions tab if it hasn't arrived within 5 minutes.
- Use this option when first-email engagement matters to you: the argument is that if the code is already in the popup, subscribers have no reason to open email one, and low opens on a brand-new subscriber's first email can signal spam to Gmail and push future sends to promotions or spam.
- Option B: reveal the discount code on the success page with a 'shop now' button. This removes friction and lets people buy immediately, at the cost of weaker first-email engagement.
- Test both, since the source describes the debate as roughly 50/50. The presenter reports their own client tests show only a minimal conversion downside for the no-reward option, offset by the welcome flow in the first 72 hours, plus deliverability upside.
- If you switch to the no-reward option, make sure your first welcome email delivers the promised code clearly, or you create unnecessary friction.
Caveat: The deliverability reasoning is the presenter's interpretation of how mailbox providers behave, not a documented provider rule.
Caveat: Reported minimal conversion downside is from the presenter's own client tests and may not hold for your list.

Tags: email-lifecycle, list-growth, popup-forms, deliverability, welcome-flow, signup-rate, conversion-optimization
Source: Klaviyo email.docx

---

## Configure single vs double opt-in for popup signup forms
Use when: Setting the opt-in method on your signup form, which determines whether the discount is shown on-screen or delivered by email.
- Single opt-in adds an eligible email subscriber without a separate confirmation click; reward placement is a separate design choice.
- Double opt-in requires confirmation before subscription. Explain the next step and verify delivery of the promised reward.
- Configure email and SMS permission separately; verify current channel and provider requirements.
- The presenter is not a fan of double opt-in because the confirm-click step reduces the number of new email subscribers you collect.
- If you still want the first welcome email opened while using single opt-in, rely on the success-page copy rather than adding a confirmation click.
Caveat: Provider recommendations (Postscript, Attentive) are stated as of the source and should be verified.
Caveat: The list-size downside of double opt-in is the presenter's stated experience, not a measured range.

Tags: email-lifecycle, list-growth, popup-forms, opt-in, compliance, deliverability, klaviyo
Source: Klaviyo email.docx

---

## Set popup trigger timing, scroll depth, and exit intent
Use when: Choosing when the email capture popup appears on your store, to avoid interrupting visitors too early or missing them entirely.
- Set a time-delay trigger between 4 and 12 seconds. The presenter always uses this band and starts experimentation with 4 seconds versus 12 seconds, then dials in the exact timing.
- Add a 60% scroll-depth trigger so the popup also fires for engaged readers who haven't hit the time threshold.
- Add exit intent: on desktop this fires when the mouse leaves the site, on mobile when the user quickly scrolls up.
- Where the tool allows, separate mobile-only and desktop-only rules so trigger behavior matches each device's exit behavior.
- Test smart/predictive triggering as an addition to your manual triggers: the source describes it as an AI model that learns the best moment to show the popup and fires it in addition to basic triggers.
- When testing smart triggering, expect the presenter's typical pattern: signup rate dips slightly while total signups rise, because the popup is shown more often. Both the presenter and the tool vendor favor leaving it on, with the caveat that some clients see the opposite.
Caveat: The 4-12 second band and 60% scroll depth are the source's recommended starting points, not validated universal thresholds.
Caveat: Smart triggering behavior is tool-specific (Aaliyah). Verify the current setting and its behavior in your own tool's interface.

Tags: email-lifecycle, list-growth, popup-forms, conversion-optimization, experiment-design, trigger-timing, signup-rate
Source: Klaviyo email.docx

---

## Build signup-form targeting rules for new vs returning visitors
Use when: Setting up popup audiences so you capture new emails without annoying existing subscribers, or to collect extra data from people already on your list.
- For your main signup form, target new visitors who have not signed up for email and have not signed up for SMS. This is the standard configuration the source uses.
- Set up a separate popup for returning visitors: has signed up for email or SMS, or is identified by a cookie.
- Use the returning-visitor popup to collect zero-party data, or to move an email subscriber onto your SMS list with a dedicated SMS opt-in form.
- Configure re-trigger suppression: choose how long before the same popup can be shown again (the source notes options from seconds to a year), and suppress if another popup was viewed in the last 15 seconds when running multiple popups.
- Set an overall store theme/branding once and reuse it across every popup so new forms stay visually consistent.
Caveat: Popup targeting terminology and available conditions vary between tools; verify field names in your current interface.
Caveat: The 15-second popup suppression is an example setting, not a recommended optimal value.

Tags: email-lifecycle, list-growth, popup-forms, segmentation, targeting, zero-party-data, sms
Source: Klaviyo email.docx

---

## Preview and QA signup popups across devices before publishing
Use when: Final QA before publishing a new email capture popup to your live storefront.
- Play the animation preview so you can see the popup as an end user experiences it, including multi-step transitions such as first step, email step, and reward step.
- Review the form on simulated devices — the source demonstrates an iPhone 15 and a 4K desktop — to confirm layout holds on both small and very wide viewports.
- Use the preview button in the top-right corner to open your actual website with the popup showing, verifying it appears correctly on the live storefront.
- Confirm the teaser/floating button (step one) looks correct before the full popup opens.
- Check styling levers left in the builder: colors, fonts, button styles, input styles.
- After publishing, create the reward in the rewards section: select a static code from your Shopify discount codes, generate a unique code, or use a custom reward such as a giveaway. Aaliyah's more granular preview options are noted as an advantage compared with the Klaviyo signup form.
Caveat: Device-simulation coverage and builder options are tool-specific; check what your popup tool currently offers.
Caveat: Some preview functionality described here may not exist in Klaviyo's signup form.

Tags: email-lifecycle, list-growth, popup-forms, qa-testing, mobile-optimization, shopify, merchandising
Source: Klaviyo email.docx

---

## Offer copy for signups: explicit discount vs mystery discount
Use when: Writing the headline and button copy of a signup popup to raise signup rate without changing your actual discount.
- Run a copy test between an explicit offer ('10% off', '50% off'), a mystery discount ('you've got a mystery discount'), an exclusive offer, and a special offer.
- Choose variants based on discount depth: the source states that if your discount is 10% or less, testing copy like mystery discount or exclusive discount is recommended.
- The presenter's own rule of thumb: everything under 20% off tends to work better with the mystery discount angle; they recommend the mystery discount angle even for discounts at 50% off or less.
- Let the A/B test decide for your audience rather than applying the rule of thumb blindly — the presenter explicitly says the data should confirm it.
- Use automated smart testing where available: the source describes an AI system that builds the variant (for example a fully generated mystery-discount version) and runs tests automatically, ending each test when results are significant and moving to the next.
Caveat: The under-20%-off and 50%-off-less thresholds are the presenter's heuristics, not measured cutoffs.
Caveat: The automated test sequencing is specific to Aaliyah's smart testing; other tools may require manual test setup.

Tags: email-lifecycle, list-growth, popup-forms, offer-design, copywriting, experiment-design, signup-rate
Source: Klaviyo email.docx

---

## Diagnose a monetization problem before blaming email or buying more traffic
Use when: Reviewing why paid acquisition costs keep rising and deciding whether to invest in welcome flows rather than more ad spend.
- Check whether you are overpaying for traffic and under-monetizing it: many brands buy Meta, Google, TikTok, influencer, affiliate and landing-page traffic and let visitors leave with only a pixel hit.
- Treat the resulting dependence on buying ever more traffic to hold revenue flat as the signal of a leaking funnel, not a traffic shortage.
- Audit the three consequences the source names: rising blended CAC from traffic leaking without converting; email getting blamed based on topline email revenue instead of whether the welcome series captures first-time buying intent; and over-reliance on retargeting to recover people you already paid for once.
- Invest in the welcome series as the fastest lever: it monetizes people you already paid to attract, improves first-time buyer conversion and payback speed.
- Use the welcome series to build trust at the exact moment a new subscriber is deciding whether you are worth buying from, since that trust gap is often the real blocker.
Caveat: This is a diagnostic frame from the source, not a measured causal model; rising CAC can have other drivers.
Caveat: The claim that most brands have a monetization problem rather than a traffic problem is the presenter's generalization.

Tags: email-lifecycle, welcome-flow, customer-acquisition-cost, retention, measurement, conversion-optimization, paid-acquisition
Source: Klaviyo email.docx

---

## Front-load the welcome flow around the first 72 hours
Use when: Designing or restructuring the welcome series cadence for new email subscribers.
- Recognize the pattern the source reports across accounts: the overwhelming majority of welcome-flow revenue is generated within the first three days after signup, with the highest number of conversions on day zero and a steep drop after that.
- Avoid stretched-out 10-, 14-, or 21-day welcome flows built mainly to 'build a relationship'; the source argues this wastes the moment of highest intent.
- Schedule two emails on day one: email 1A immediately after signup, then email 1B eight hours later as a plain-text reminder.
- Add a 16-hour delay after 1B so you reach 24 hours, then send email two, and continue daily through email six.
- Accept the tension: the first email usually generates the most revenue because people only want the promised offer, so the later emails are what separate mediocre welcome flows from strong ones.
- Use the later emails to build conviction quickly via social proof, brand credibility, product education, objection handling, USPs, category guidance, bestsellers, founder credibility, or urgency — not all of them, but enough to reduce hesitation fast.
Caveat: The 72-hour concentration and the day-zero peak come from the source's own account analytics; timing will vary by brand, price point and traffic source.
Caveat: The specific 8-hour and 16-hour delays are the source's recommended cadence, not tested universal optima.

Tags: email-lifecycle, welcome-flow, cadence, retention, conversion-optimization, measurement, automation
Source: Klaviyo email.docx

---

## Set welcome flow trigger filters and disable smart sending
Use when: Building or auditing the welcome flow automation settings in your ESP.
- Trigger the flow when someone is added to your main list (often the newsletter list).
- Add a profile filter: has placed order zero times over all time. This prevents existing buyers who re-subscribe from receiving the welcome discount again.
- Disable re-entry so a person can only go through the welcome series once.
- If working from a default template, delete the split for existing customers and remove any conditional split you're not using, then rebuild the delays.
- Add time delays of 8 hours after email 1A, then 16 hours after 1B, then one day before each subsequent email through email six.
- Turn off smart sending on every flow email. The source's reasoning: smart sending skips anyone who received an email in the last (default) 16 hours, but flow emails are trigger-based and must be delivered. For campaigns, the source advises the opposite — turn smart sending on. Verify the current smart sending window settings in your ESP.
- Enable UTM tracking on the flow emails.
Caveat: Filter names and default behaviors differ between ESPs and change over time; verify in your current account.
Caveat: The advice to turn smart sending off for flows assumes trigger-based flows; the presenter's rule is not a universal deliverability law.

Tags: email-lifecycle, welcome-flow, automation, klaviyo, segmentation, deliverability, utm-tracking
Source: Klaviyo email.docx

---

## Write welcome email 1A: deliver the code above the fold
Use when: Drafting or rewriting the first email of the welcome series.
- Put the offer, the discount code, and a one-click call to action in the above-the-fold section — the part visible without scrolling on mobile or desktop. The source's rationale: an estimated 90-99% of people only see the above-fold area before leaving the email.
- Do not bury the code or make subscribers work for it. The subscriber signed up for one thing; give it immediately rather than leading with brand news.
- Below the fold, show one to three bestsellers or a 'start here' selection to route them to a specific product or category.
- Add trust builders where applicable: reviews, press mentions, expert endorsements, social proof.
- Add risk reversals where applicable: free shipping, free returns, warranty, free trial.
- Keep the hero simple. The source's example ('Welcome to [brand], 10% off your first order, use code X') is deliberately plain but unambiguous, then repeats the code with a CTA at the bottom of the email.
Caveat: The 90-99% above-fold-only figure is the presenter's estimate, not a measured statistic.
Caveat: The described layout is a source example for one brand; the exact modules should match your product mix and AOV.

Tags: email-lifecycle, welcome-flow, email-copywriting, product-page, merchandising, social-proof, conversion-optimization
Source: Klaviyo email.docx

---

## Send a same-day plain-text founder reminder as welcome email 1B
Use when: Adding a second welcome-flow email on the day of signup to recover subscribers who didn't buy immediately.
- Send it eight hours after email 1A. The source's reasoning: momentum is highest on day zero and waiting 24 hours wastes it.
- Write it as a short, direct, human plain-text founder-style note, for example 'just making sure you saw your code'.
- Include a reminder of the discount code, one or two simple product or category references (bestsellers, bundles, top categories, or the most logical first purchase), and a direct CTA to the site.
- Do not add a designed template or design flourish; the format is the point because conversational, human-feeling emails tend to be rewarded by inbox providers through engagement, per the source.
- Expect a meaningful incremental revenue contribution from this second same-day email. The source reports this repeatedly in their tests and addresses the common concern that two emails in one day feels like too much.
Caveat: The claim that email 1B 'drives a surprising amount' of incremental revenue is the presenter's client experience, not a published benchmark.
Caveat: Two emails in one day may be inappropriate for very low-frequency or high-consideration catalogs; test on your own list.

Tags: email-lifecycle, welcome-flow, email-copywriting, plain-text, cadence, deliverability, conversion-optimization
Source: Klaviyo email.docx

---

## Use welcome email 2 to build brand trust with substance, not fluff
Use when: Writing the second-day welcome email that establishes credibility for new subscribers who haven't bought yet.
- Choose the trust angle that fits your niche: a founder story, mission statement, quality standards, ingredients, sourcing, craftsmanship, or product philosophy. It depends on the brand.
- Include a reminder of the welcome discount, a clear trust-building narrative, brand backstory or mission only if it actually matters, founder presence only if credible and relevant, and a clear CTA.
- Keep it short. The source explicitly warns against big paragraphs; the goal is to reduce uncertainty and increase belief in the brand, not to tell the founder's entire life story.
- Use a founder photo where it humanizes the brand — the example pairs a founder introduction with her product/category context and repeats the discount code.
- Avoid 'brand poetry' with no substance; every claim should help a hesitant shopper decide you're a legitimate choice versus the alternatives they're comparing.
Caveat: The source gives no length target; 'not too long' is a judgment call.
Caveat: Founder credibility framing is not appropriate for every brand or category.

Tags: email-lifecycle, welcome-flow, brand-positioning, email-copywriting, social-proof, conversion-optimization, trust
Source: Klaviyo email.docx

---

## Use welcome email 3 to guide overwhelmed subscribers to a first purchase
Use when: Writing the welcome-flow email that helps undecided subscribers pick a first product.
- Assume subscribers don't know what to do with the discount code; tell them explicitly rather than expecting them to figure out the catalog.
- Feature one to three bestsellers or best collections as recommended starting points.
- Use simple benefit-led positioning rather than specs. The source's example leads with outcomes (grams of plant-based carbs for fast energy, dual carbs for quick absorption, hydration and endurance in one) instead of product features.
- Explain why these are the best starting points and set clear expectations.
- Remind them of the welcome gift again, typically in a top bar and in the email body.
- Keep the email focused on routing, not on additional persuasion angles — that job belongs to later emails.
Caveat: Benefit-first framing is a general copywriting principle; the source's specific framing comes from a supplement/energy brand example.
Caveat: One to three featured products is the source's guidance; catalogs with very narrow assortment may need a different treatment.

Tags: email-lifecycle, welcome-flow, merchandising, email-copywriting, product-selection, conversion-optimization, bestsellers
Source: Klaviyo email.docx

---

## Welcome email 4: handle objections and differentiate at the product or category level
Use when: Writing the welcome-flow email that targets subscribers still hesitating after the first three sends.
- Assume remaining hesitation is friction and answer the questions they haven't asked: why buy from you instead of a competitor, why the price is justified, why they should trust your quality, and why act now.
- Include core brand or product/category-level differentiators plus objection handling.
- Remind them of the discount and add real urgency — a clear deadline if applicable (the source example: 'hurry, this code expires in 48 hours').
- Make urgency believable by using unique discount codes, or static codes that look unique. The source warns that generic codes like WELCOME10 make urgency look fake because everyone knows such a code won't expire.
- Add a review to support the argument.
- Keep the focus on trust and differentiation rather than another hard sell.
Caveat: The 48-hour deadline is a source example; your deadline must match your actual discount expiry for the urgency to be honest.
Caveat: Not every brand has product-level differentiators worth a dedicated email; adapt the angle.

Tags: email-lifecycle, welcome-flow, objection-handling, positioning, offer-design, urgency, email-copywriting
Source: Klaviyo email.docx

---

## Welcome email 5: escalate urgency with reviews that mirror buyer objections
Use when: Writing the welcome-flow email that uses a closing deadline plus social proof to convert hesitant subscribers.
- Communicate a clear urgency deadline and escalate from the prior email: if email 4 said 48 hours left, email 5 says 24 hours left. If you hadn't stated a deadline earlier, 48 hours is a usable starting point. The source notes the escalation depends on the chosen strategy.
- Add one to three reviews.
- Select reviews carefully: avoid generic reviews that just say 'great product'. Choose reviews that highlight a specific pain point or objection and make readers feel recognized, so the reviewer's outcome maps to the reader's situation.
- Prefer one strong, specific review over three generic ones.
- Keep the email straightforward — urgency plus social proof, no new persuasion angles.
Caveat: Deadline escalation only works if the deadlines are real; repeated fake deadlines damage trust.
Caveat: The source gives no data on optimal review count beyond preferring quality over quantity.

Tags: email-lifecycle, welcome-flow, social-proof, urgency, email-copywriting, conversion-optimization, objection-handling
Source: Klaviyo email.docx

---

## Welcome email 6: close with a final reason to act, and test the format
Use when: Writing the final email of the welcome series and choosing its format.
- Include a final reminder of the offer, strong urgency, and a clear indication of what to buy.
- Choose the strongest support angle for your brand: reviews, authority signals, or risk reversals.
- Test designed versus plain-text format for this email rather than assuming one wins.
- One route the source uses often: after email 4 at 48 hours and email 5 at 24 hours, make email 6 an 'extended sale' sent as a plain-text founder email ('we've extended your welcome discount for another 24 hours, act fast').
- A/B test the closing angle and treat this email's format as a variable, not a fixed rule.
- Keep the momentum assumption realistic: later emails in the flow generate less than the day-zero content, so expect incremental rather than dramatic returns.
Caveat: The 'extended sale' angle works well in the source's experience but implies the deadline was moved; only use it if it is truthful.
Caveat: The source presents two routes (designed vs plain text) as alternatives to test, not as a settled best practice.

Tags: email-lifecycle, welcome-flow, email-copywriting, experiment-design, urgency, offer-design, conversion-optimization
Source: Klaviyo email.docx

---

## Add proven evergreen campaigns to the welcome flow for extra revenue
Use when: Looking for incremental welcome-flow revenue after the core six-email structure is working.
- Review past campaigns and identify the ones that generated the best results for your brand.
- Check whether those top performers are evergreen, meaning they remain relevant and usable all year.
- Add the evergreen winners into the welcome flow after the closing emails.
- Candidate campaign types the source names: how-tos, blog promotions, review or user-generated content, myth-busting emails, product highlights, subscription promos, bundles, gift guides, and educational emails.
- Do not cap the welcome flow at seven emails. The source explicitly says not to cap it and treats this as an easy way to squeeze additional revenue.
- Set expectations modestly: because momentum is concentrated in the first 72 hours, treat the appended emails as incremental additions rather than major revenue drivers.
Caveat: Purely seasonal campaigns are not evergreen and shouldn't be appended as standing flow emails.
Caveat: The source does not quantify the incremental revenue, only that it is additional.

Tags: email-lifecycle, welcome-flow, campaigns, evergreen-content, retention, automation, revenue-optimization
Source: Klaviyo email.docx

---

## Position browse abandonment as mid-funnel persuasion, not lost-sale recovery
Use when: Deciding the strategy and tone for a browse abandonment flow targeting product-page visitors who didn't add to cart.
- Separate intent levels: browse abandoners viewed a product page but did not add to cart, so they are usually comparing alternatives in evaluation mode, not recovering a near-sale.
- Shift the priority order for this flow: trust matters more than urgency, objection handling matters more than giving away a discount, and positioning matters more than promotion.
- Do not clone your cart abandonment flow. The source says most brands get this wrong by treating browse abandonment as a weaker cart abandonment flow.
- Recognize the competitive reality the source describes: a visitor viewing your product page likely has competing product tabs open, so the flow's job is to stay in the decision process with controlled persuasion rather than desperation.
- Use the flow for margin- and LTV-conscious brands: follow up without immediately discounting, and reserve discounts for the later escalation emails.
Caveat: The 'three other tabs' description is the presenter's illustration of comparison behavior, not measured data.
Caveat: For very short deliberation categories, browse abandonment may behave more like cart abandonment.

Tags: email-lifecycle, browse-abandonment, retention, positioning, objection-handling, conversion-optimization, customer-journey
Source: Klaviyo email.docx

---

## Set browse abandonment trigger filters and a 30-day cooldown
Use when: Building or auditing the browse abandonment flow in your ESP so it fires only for genuinely unconverted browsers.
- Trigger the flow on viewed product.
- Add profile filters so the email only sends if the person has placed order zero times since starting this flow, has checkout started zero times since starting this flow, and has added to cart zero times since starting this flow.
- Allow re-entry after a 30-day time period to create a cooldown window.
- If you run Shopify, use the Shopify added-to-cart trigger rather than the API added-to-cart trigger. The source flags this as important.
- Do not split the browse abandonment flow between new and returning customers in most cases. Rationale: browse abandoners are low-intent window shoppers, and even previous buyers are re-evaluating and comparing you against alternatives.
- Exception: if margins are extremely tight and you truly cannot afford an incentive for returning buyers, consider a conditional split. The source argues that for most brands doing serious volume, the incremental revenue outweighs the marginal discount cost precisely because these visitors were not high-intent to begin with.
- Note the contrast with cart abandonment, where the source does recommend splitting returning customers from non-buyers because intent is higher.
Caveat: Filter and trigger names differ by ESP and change over time; verify in your current account.
Caveat: The no-split recommendation is the source's general preference with a stated margin-based exception, not an absolute rule.

Tags: email-lifecycle, browse-abandonment, automation, segmentation, shopify, klaviyo, conversion-optimization
Source: Klaviyo email.docx

---

## Time the browse abandonment delays and use dynamic product blocks
Use when: Building the timing and core content of the browse abandonment sequence.
- Set the first delay to roughly 30-45 minutes up to 2 hours. The source tests this range, uses 1 hour for demonstration, and notes that closer to the purchase moment you should email sooner.
- Calibrate by flow type: browse abandonment is around 2-4 hours at the loosest, cart abandonment shorter, and checkout abandonment shortest — as early as 15 minutes for the checkout flow.
- Structure as a four-part sequence: email one is a simple reminder, email two builds trust, emails three and four introduce the discount.
- Add a one-day delay between each email.
- Include a dynamic product block in every email, showing the product the person viewed.
- Build the block efficiently: copy a default template's dynamic product block, save it as universal/reusable content, and edit it to match your branding rather than building from scratch — the source says this saves a lot of time.
Caveat: The delay ranges are source heuristics for relative urgency across flow types, not measured optima; test on your own traffic.
Caveat: Dynamic product block features and universal content features are ESP-specific; verify availability.

Tags: email-lifecycle, browse-abandonment, cadence, dynamic-content, automation, klaviyo, conversion-optimization
Source: Klaviyo email.docx

---

## Write browse abandonment email 1 as a light, timely reminder
Use when: Drafting the first browse-abandonment email.
- Send it while the visit is still fresh — the source's range is 30 minutes to 2 hours after the product page view — so the person still remembers you.
- Keep it non-aggressive and not sales-heavy. A simple 'you were looking at this, are you still interested?' angle is enough.
- Include a dynamic product block showing the viewed product.
- Include a recommendations feed, for example four other products related to the viewed product.
- Add social proof such as reviews or user-generated content.
- Use a clear headline and CTA above the fold with body copy containing the dynamic product block and a second CTA, plus a related-products section.
- Expect this email alone to recover mainly high-intent browsers who simply got distracted — the source says that is what you're capturing at this stage.
Caveat: The source's claim about what share of intent this recovers is qualitative, not measured.
Caveat: Timing must be feasible with your ESP's trigger and delay configuration.

Tags: email-lifecycle, browse-abandonment, email-copywriting, dynamic-content, social-proof, timing, conversion-optimization
Source: Klaviyo email.docx

---

## Write browse abandonment email 2 to remove friction, not add pressure
Use when: Writing the second browse-abandonment email for viewers who ignored the first reminder.
- Assume the non-conversion reflects hesitation, which the source calls completely normal in browse abandonment.
- Think like the buyer and address the questions they have: is this worth the price, is this legit, what if it doesn't fit or work or last, is there a better alternative.
- Do not sell harder. Reduce uncertainty.
- Lead with risk reversals if you have them: guarantees, trials, free shipping, free returns.
- If you lack strong risk reversals, lean on social proof instead.
- Include a dynamic product block to guide them back to the viewed product.
- Add a brand-level reason to buy where you have one — the source's example uses a mission-based reason ('every tea they buy feeds five rescue dogs') with a supporting review.
- Treat this email as especially important for higher AOV brands, which need more convincing before a first purchase.
Caveat: The higher-AOV emphasis is the presenter's reasoning, not measured by AOV band.
Caveat: Mission-based angles only fit brands that genuinely have them.

Tags: email-lifecycle, browse-abandonment, objection-handling, risk-reversal, social-proof, email-copywriting, conversion-optimization
Source: Klaviyo email.docx

---

## Browse abandonment email 3: diagnose hesitation type before escalating with a discount
Use when: Writing the third browse-abandonment email, where the audience has ignored both the reminder and the trust-building email.
- Accept the interpretation: after two ignored emails, non-conversion is hesitation rather than forgetfulness — they are not sure they should buy from your store.
- Diagnose which of the three hesitation categories applies: price sensitivity, comparison shopping, or 'I'll buy later' procrastination.
- Escalate with an offer only at this stage, not before. The source structures the flow so discounts appear in emails three and four, after the reminder and trust emails.
- Match the escalation to the hesitation type rather than sending the same incentive to everyone.
- For returning customers specifically, the source suggests the same escalation logic: a small incentive, a subscription option where applicable, a bundle angle, or a compelling reason to act now.
- Aim to convert low intent into action rather than protecting loyalty perception — this is the source's stated goal for browse-abandonment sending.
Caveat: The three hesitation categories are the source's framework, not a measured taxonomy.
Caveat: Escalating discounts in browse abandonment can erode margin; the source accepts this trade-off for volume brands but notes the tight-margin exception.

Tags: email-lifecycle, browse-abandonment, offer-design, objection-handling, segmentation, conversion-optimization, retention
Source: Klaviyo email.docx

---

## Browse abandonment flow: 3-4 email escalation ladder
Use when: Building or auditing the browse abandonment flow for your store.
- Email 1: simple reminder with the viewed product in a dynamic product block plus CTA buttons, and risk reversals (guarantees, trials, free shipping/returns). Example shown: apparel brand 'every tea they buy feeds five rescue dogs' plus a review.
- Email 2: trust/risk reversal angle — three deeper reasons why people buy from this brand, with a dynamic product block.
- Email 3: treat remaining non-buyers as hesitant, not forgetful. Hesitation falls into one of three buckets: price sensitivity, comparison shopping, or 'I'll buy later' procrastination.
- For email 3, choose one of two escalation options. Option A: small time-sensitive incentive with a clear 48-hour deadline, clean design, single clear CTA. Option B: if you sell replenishables, push subscribe-and-save (e.g., 10% off), a bundle, or a starter-kit discount to protect margin instead of discounting a one-time purchase.
- Email 4: last chance before discount ends — plain-text email from the founder, short and direct, 24-hour deadline, reminding them of the code from the previous email. Source argues plain text at this stage feels personal while heavy design signals automation.
- Optional in emails 3-4: show product recommendations via the Klaviyo product feed (e.g., 'you might like these') so non-buyers see other products. Furniture example also used a footer bar highlighting a physical store to build trust.
Caveat: Source presents this ladder as its own recommended structure, not a universal rule.
Caveat: The presenter explicitly says the browse flow is where they see brands 'overdo it' with banners and urgency graphics — simplifying is the point.
Caveat: The source does not recommend splitting the browse flow between new and returning buyers because browse abandonment is low intent; even returning customers are comparison shopping. Only treat margins as the reason to split.

Tags: email-lifecycle, browse-abandonment, email-sequences, retention, conversion-optimization, discount-strategy, klaviyo
Source: Klaviyo email.docx

---

## Abandoned cart vs abandoned checkout: build side by side
Use when: Setting up abandoned cart and abandoned checkout flows inside Klaviyo (verify current interface).
- In Klaviyo, go to Flows > Create flow, search 'cart' to find the cart flow (it may not appear in the Essentials list — verify current UI).
- If your store is on Shopify, use the Shopify 'added to cart' trigger, not the generic one. Build the abandoned cart version first.
- Set flow filters: checkout started zero times since starting this flow, placed order zero times since starting this flow, and (via 'has not been in the flow in the last 30 days') no recent re-entry.
- Add the first time delay. Klaviyo defaults to 4 hours; the source says this is too long and recommends testing 15 minutes to 1 hour, e.g., 30 minutes. The principle: the closer to purchase intent, the sooner the email.
- Send email 1 at ~30 minutes, email 2 one day later, email 3 one day later.
- Add a conditional split: 'has placed order at least once (all time)' — yes = returning customer, no = non-buyer/first-time buyer.
- Non-buyers get two further emails: email 4 with discount (48-hour deadline) and email 5 one day later with a final discount reminder (24-hour deadline).
- Returning customers get the founder check-in email. Then clone the whole flow, rename to abandoned checkout, change the trigger to 'checkout started', and remove the 'checkout started zero times' filter since the trigger is now checkout started.
Caveat: Exact Klaviyo menus, defaults and filter names may have changed — verify the current interface before implementing.
Caveat: The 15-60 minute timing is a recommended starting point the presenter says to A/B test; it is not a proven benchmark.
Caveat: Only apply the discount branch if your margins allow it.

Tags: email-lifecycle, abandoned-cart, abandoned-checkout, automation, klaviyo, experiment-design, discount-strategy
Source: Klaviyo email.docx

---

## Abandoned cart/checkout email content: 3-stage objection sequence
Use when: Writing the copy for abandoned cart and abandoned checkout emails before any discount is offered.
- Email 1 (30 min-1 hour after abandonment): simple reminder only. No discount, no overselling. Most abandonment is distraction ('phone, a thousand things going on'), not a 'no'. Include a dynamic product block and your risk reversals (guarantees, trials, free shipping, free returns). Example: 'You left something tasty behind — complete my order — why spice fans love us — complete my order.'
- Email 2 (1 day later): plain-text personalized check-in from the founder. Tone should feel like a one-to-one email. Angle: 'Noticed you were checking out this product — wanted to make sure you didn't run into issues. By the way, here's why people love us.' Keep it 2-3 short paragraphs max, end with a simple CTA and a link back to their cart. This also performs well with Gmail's AI inbox prioritizing conversational email (source's 2026 claim).
- Email 3 (1 day later): objection handling, not 'our brand is awesome'. Address the real frictions: is it worth the price, shipping time, what if it doesn't fit, what if it doesn't work, what if it's not as good as the photos. Frame strongest USPs/products as answers to those objections (durability/warranty for price, certifications/press for trust, clear differentiation for comparison shopping). Include a dynamic product block.
- Example of objection handling from a vape brand: 'British made quality' (addresses trust/offshore concerns), '8X cheaper than cigarettes' (price concern), '100% BPA free' (safety concern), 'highly rated service' (social proof).
Caveat: This sequence deliberately holds discounts until escalation; the source argues giving discounts in email one destroys margins and trains customers to wait for discounts.
Caveat: The claim that this structure is 'the highest converting' is the presenter's opinion, not a measured benchmark.

Tags: email-lifecycle, abandoned-cart, email-copy, objection-handling, klaviyo, conversion-optimization, risk-reversal
Source: Klaviyo email.docx

---

## Discount vs no-discount fork: non-buyers vs returning customers
Use when: Deciding who gets a discount code in your abandoned cart/checkout flow and how much.
- Add a conditional split after emails 1-3: 'has placed order at least once (all time)'. Yes = returning customer, No = non-buyer/first-time buyer.
- Non-buyers (email 4): clean, simple, time-sensitive discount — code with a 48-hour deadline, dynamic product block, optional Klaviyo product feed recommendations, clear CTA. Examples shown: 'Take 10% off your cart, use code...', 'Enjoy 10% off today'.
- Non-buyers (email 5): final push, plain-text from the founder with the code and a 24-hour deadline. Example: 'it's Melanie here, founder of... good news, you can still claim your offer with 10% off, use code...' This is the source's claim: plain text closes first-time buyers who are '90% convinced' but need a deadline.
- Returning customers: no discount by default. Send one plain-text founder check-in offering concierge-level support — ask about sizing, specs, delivery, offer help. Source argues returning customers already trust the brand, are often just distracted, and may be comparison shopping for details, not loyalty.
- If margins are solid and you want to discount returning customers, source recommends a smaller discount than non-buyers — their example: 5-10% instead of 50% for non-buyers. In that case, add the matching final reminder email one day later.
Caveat: Discount amounts and deadlines (48h/24h) are source examples, not calibrated benchmarks.
Caveat: Source specifically warns not to train loyal customers to expect full discounts — offering returning customers the same discount as non-buyers is the most common mistake the presenter calls out.
Caveat: The 5-10% vs 50% example is illustrative, not a recommended ratio.

Tags: email-lifecycle, abandoned-cart, discount-strategy, segmentation, retention, klaviyo, margin-protection
Source: Klaviyo email.docx

---

## Post-purchase flow filters and timing
Use when: Setting up a post-purchase flow in Klaviyo that turns first-time buyers into repeat customers.
- Trigger: placed order. Set two flow filters: placed order zero times since starting this flow (so a second purchase re-triggers the flow and doesn't get the old one), and canceled order zero times since starting this flow.
- Wait 10 minutes before the first email. Don't send immediately — the customer already receives your transactional order/shipping emails from Shopify or your commerce platform, so a separate thank-you would be redundant.
- Turn OFF smart sending / 'skip recently emailed profiles' on every email in this flow. If a customer just bought from a campaign email, smart sending would suppress the post-purchase email, which is the opposite of what you want.
- Add a conditional split: 'has placed order equals one (all time)' — Yes = first-time buyer; No = returning customer. Optionally split again at two purchases for a separate three-plus-purchase track, which the source says is worth it for some brands but not necessary for most.
- Source's default structure: email 1 (thank you) at 10 minutes; email 2 (order on its way) 2 days later; email 3 (how-to, split by product/category); optional email 4 (social follow push); optional email 5 (loyalty program push); email 6 (post-delivery personal check-in from the founder).
Caveat: Klaviyo menu names and smart-sending settings may have changed — verify current interface.
Caveat: The 'order on its way' timing assumes standard shipping; adjust to your actual shipping times.

Tags: email-lifecycle, post-purchase, automation, klaviyo, retention, repeat-purchase, fulfillment
Source: Klaviyo email.docx

---

## Post-purchase email content: 6-email sequence
Use when: Writing the emails in your post-purchase flow after a customer's first order.
- Email 1 (10 minutes): plain-text thank-you from the founder. Confirm order progress, offer support, tell them what to expect. For first-time buyers make it a memorable first impression; for returning customers express gratitude for loyalty. Include a link back to your site (source says even just a site link gets a strong post-purchase place-order rate) and optionally recommend a specific product to cross-sell — the biggest repeat-purchase window is the first 30 days.
- Email 2 (2 days): 'your order is on its way'. Build excitement, reinforce the value of the purchase, and include recommendations — static blocks or the Klaviyo product feed. Examples: refills/cookbook/candle/kit for a spice brand; 'complete your stack' bundles pairing isolate with creatine or collagen for a nutrition brand; 'explore more' sabers plus a mystery saber (curiosity works).
- Email 3: how-to email, split by product or product category so it's actually relevant to what they bought. Provide clear actionable tips, links to FAQs/manuals/videos, and reassurance they made a good choice. This reduces returns and improves experience.
- Email 4 (optional): social media follow push — the more channels you hold a customer on, the better for repeat purchase.
- Email 5 (optional): loyalty program push. Make the benefit immediately clear (points, discounts, rewards for shopping/reviewing/referring) — people only join for a clear benefit.
- Email 6: post-delivery plain-text check-in from the founder — 'how did everything go?' The source says this is one of the highest-revenue emails because it shows genuine care and can invite the next purchase.
Caveat: Source claims retained customers are 9x more likely to convert and repeat customers spend 67% more than new customers; it does not provide the study for either, so treat as attributed statistics, not your expected results.
Caveat: Source claims 95% of customers receiving proactive post-purchase communication are less likely to return — also unaudited data, use as directional.
Caveat: The 'most returning customers buy within 30 days' statement is from one client screenshot, not a universal benchmark.
Caveat: Auto-applied source framing: how-to email 3 only makes sense if you have technical products; simple care instructions may be enough for apparel.

Tags: email-lifecycle, post-purchase, email-copy, retention, cross-sell, klaviyo, returns-reduction
Source: Klaviyo email.docx

---

## Post-purchase as the retention engine
Use when: Deciding how much post-purchase and replenishment effort to invest after the first order.
- Reframe the first purchase as the beginning of the relationship — a weak post-purchase experience loses repeat purchases, referrals, trust, and lifetime value.
- Prioritize the first 30 days: the source says most returning customers buy within 30 days of their initial order, so this is the window to improve first-to-second purchase rate.
- Use the flow to reduce returns by reinforcing purchase value, giving usage/care tips, and building excitement — buyer's remorse is a major return driver and returns cut into margin.
- Push replenishment appropriately within the post-purchase sequence: subscriptions or loyalty programs for replenishable products, and cross-sell/recommendations for everything else.
- Multi-channel touchpoints (email + SMS + social) are described as ways to increase repurchase rate — the more places you hold the customer, the more often you can reach them.
Caveat: The statistics cited (9x, 67%, 95%, 30-day window) are attributed to 'research' by the source without citations and are not benchmarks you should plan against.
Caveat: Return-rate and repeat-purchase effects will vary by category and AOV; the source presents them as typical, not universal.

Tags: email-lifecycle, retention, post-purchase, repeat-purchase, replenishment, subscriptions, customer-lifetime-value
Source: Klaviyo email.docx

---

## Email campaign frequency: aim for 3-4 per week
Use when: Deciding how often to send email campaigns to your ecommerce list.
- Sending once or twice a week feels respectful but backfires: subscribers can't place you, skip past you, and eventually forget you exist — 'less frequent doesn't mean less intrusive, it means less memorable'.
- Sending 5-7 times a week (every day) can produce short-term revenue but drives fatigue, higher unsubscribes, lower engagement, and deliverability damage. The degradation is slow enough that brands often don't notice until it's done.
- Target 3-4 campaigns per week. This keeps visibility without tipping into annoying, keeps engagement healthy, keeps churn manageable, and builds a consistent inbox presence rather than sporadic spikes.
- Because the volume is high, campaigns must be short, valuable, and easy to act on — a couple of seconds to make an impression; nobody wants a wall of text from a brand they bought from once.
Caveat: The 3-4x/week figure comes from the source's own testing across 120 ecommerce brands over 7 years; treat as a source-specific heuristic, not an industry benchmark.
Caveat: Frequency should still be tuned to your list size, engagement and deliverability; the source itself notes the flood of what you send matters as much as how often.

Tags: email-lifecycle, campaigns, list-health, deliverability, engagement, email-strategy
Source: Klaviyo email.docx

---

## Campaign mix: don't let promos dominate the calendar
Use when: Building or auditing your monthly/quarterly email campaign calendar.
- All campaign emails fall into one of seven buckets: promos/special offers; holiday/special events; product launches; product highlights; social proof; value-based/educational; company updates.
- Audit your calendar against those buckets. Most ecom brands over-index on promos because discounts drive immediate sales — but if every email is a promotion, subscribers learn to wait for the next deal and only buy at a discount, which kills margin.
- Add a subtler cost: constant 'buy now' emails make a brand feel desperate, and the source says desperate doesn't sell.
- Replace some promo volume with trust-building content. Source argues that in 2026 customers are skeptical, research and compare, and trust is what sits between being on your list and buying. Trust takes repetition across multiple touchpoints, not one clever subject line.
- The practical payoff the source claims: when customers trust you, they buy without needing a discount, improving both conversion rate and margins.
Caveat: The 'seven categories' is a planning framework used by the source, not a data-driven taxonomy.
Caveat: The source does not say promos are bad — it says they should sit alongside trust-building content, with discounts having a time and place.

Tags: email-lifecycle, campaigns, discount-strategy, trust-building, email-strategy, margin-protection
Source: Klaviyo email.docx

---

## Non-discounted campaign idea bank (social proof + education)
Use when: Filling your campaign calendar with non-discounted emails that build trust with your list.
- Social proof angles: testimonials, user-generated content, press mentions, media features, influencer reviews, before-and-after results from real customers, review roundups around one product or benefit, trust badges/certifications, star-rating highlights across platforms like Trustpilot or Google, peer video testimonials, customer milestones (long-time buyer or achievement), and community numbers (customers served, orders shipped, countries reached).
- Education angles: blog/article highlights, research highlights, myths debunked, FAQs, industry trends, common mistakes and fixes, glossary emails breaking down jargon, beginner's guides, advanced tips, debunking a competitor claim, expert interviews, book/resource recommendations, a single surprising 'stat of the week', your most-asked question pulled from support or social comments, and an ingredient/material spotlight explaining why one component matters.
- Use these to build trust through teaching — source argues that genuinely useful content makes you a credible source, not just another brand in the inbox.
- Keep each email short and easy to act on, since you're sending 3-4 per week.
Caveat: These are the source's idea prompts, not tested angles with known performance.
Caveat: Claims like 'educational content is one of the most effective trust builders' are the presenter's argument, not measured results.

Tags: email-lifecycle, campaigns, trust-building, social-proof, content-marketing, customer-research
Source: Klaviyo email.docx

---

## Non-discounted campaign idea bank (product, brand, occasion, engagement)
Use when: Planning campaign emails that highlight products or brand story rather than cutting price.
- Product-focused angles: bestsellers, new arrivals, trending products, staff picks, back-in-stock, bundles, essentials, gift guides, 'gift yourself', feature highlights, benefit highlights, us-vs-them competitor framing, problem-to-solution, before-and-after, how-to-use, how-it's-made, tips and tricks, coming-soon sneak peeks, limited-edition/seasonal (creates urgency without discounting), product comparisons to help choose between two of your own products, subscription/loyalty highlights, most underrated product, fan favorite, founder's pick, packaging highlight, product origin story, sensory description (food, beauty, lifestyle), complimentary products (soft cross-sell), build-a-routine, most gifted, and customer-favorite combinations/bundles.
- Brand and culture angles: brand story, founder story, meet the team, behind the scenes, recent developments, brand USPs, day in the life, community spotlight, brand values in action, 'our story so far' timeline, why we started, what we refuse to do (powerful trust/differentiation angle), mistakes you've made (rare, memorable, transparent), manufacturing process, suppliers/partners, team tradition, and growth announcements.
- Calendar/occasion angles: holidays, awareness days tied naturally to your niche, seasonal transitions, brand milestones (anniversaries, subscriber counts, units sold), new year/new routine, back to school, new season preview, end-of-year reflection.
- Engagement angles: quiz/survey teaser to find the right product, poll results tied back to products, 'ask us anything' (also good for deliverability), pick your favorites votes, challenge emails, waitlist/early access invites, referral program spotlights, and loyalty program updates.
Caveat: This is a long prompt list from the source, not a prioritization or performance ranking.
Caveat: It is not evidence that any single angle converts; test within your own list.

Tags: email-lifecycle, campaigns, product-marketing, brand-story, merchandising, bundles, engagement
Source: Klaviyo email.docx

---

## Campaign calendar tool setup and the minimum fields to track
Use when: Setting up or cleaning up the production calendar your team uses to plan campaign emails.
- Choose a tool based on how you work; the source says the tool matters less than consistent use. Options discussed: Notion (flexible visual workspace), Airtable (stronger filtering/sorting across high volumes, used by the source's agency), ClickUp or Monday (if your team already lives in a project management tool), or Google Sheets (underrated and sufficient for a simple setup everyone can access).
- Whatever the tool, track at least: campaign status, owner, send/planned date, campaign category, subject line and/or angle, main content or offer, and links to creative or the live campaign so the full campaign list doesn't become a graveyard.
- Use the tracked category column to enforce the non-promo mix — if every row says 'promo', your calendar is out of balance.
- Review the calendar on a regular cadence so you always know what is drafted, which email is next, and which tested angle hasn't been reused.
Caveat: The exact field list belongs to the source's own system; add fields that reflect how your team actually works.
Caveat: Tool features and interfaces change — verify current functionality before standardizing on one.

Tags: email-lifecycle, campaigns, operations, process, content-planning, team-workflow
Source: Klaviyo email.docx

---

## Run a campaign calendar in a tool your team will actually open
Use when: Setting up or replacing the email campaign planning system before a month of sends.
- Pick the tool by team behavior, not features: Notion suits visual, flexible team workspaces; Airtable is stronger for filtering/sorting large campaign volumes across many clients; ClickUp or Monday make sense if the team already lives in a PM tool and wants email alongside other marketing work; Google Sheets is enough for a basic, universally accessible start.
- Track these fields for every campaign: send date, campaign type, segment, status, and owner. Status values used by the source: idea, copywriting, design, implementation, ready to review, scheduled, sent.
- Use the owner field to name the person responsible for that specific step, not a general team.
- Note this is agency-practitioner experience, not a benchmark: the presenter reports switching tools over ~4 years and currently using Airtable; Google Sheets is described as underrated and sufficient.
- Verify the current UI and plan limits in whichever tool you choose, since interfaces change.
Caveat: Tool recommendations reflect one agency's workflow; a small store may never outgrow Sheets.
Caveat: A calendar only helps if it is updated consistently.

Tags: email-lifecycle, campaign-planning, content-calendar, notion, airtable, google-sheets, workflow
Source: Klaviyo email.docx

---

## Send campaigns only to engaged subscribers
Use when: Deciding the send list for any ecommerce campaign, especially after engagement or revenue has declined.
- Stop blasting the full email list; the source calls this one of the most common and costly email mistakes because unengaged sends hurt deliverability and push even strong campaigns into spam.
- Define an engaged segment in Klaviyo as people who opened or clicked within the last 30, 60, or 90 days.
- Choose the window based on your list size and sending volume — the source treats 30/60/90 as options, not a fixed rule.
- Send campaigns to that engaged segment only, and use deliverability/segmentation tutorials from the source's channel for setup detail.
- Verify current Klaviyo segment and suppression mechanics before building, since interfaces change.
Caveat: Aggressive suppression shrinks the addressable list; the method deliberately trades raw reach for inbox placement.
Caveat: The text does not state a numeric deliverability benchmark for this change — treat any lift as audience-dependent.

Tags: email-lifecycle, deliverability, segmentation, klaviyo, engagement, list-hygiene
Source: Klaviyo email.docx

---

## Anchor the calendar with fixed dates before filling content
Use when: Starting a new month of email campaign planning for a store with launches, restocks, or planned promotions.
- Open the calendar and mark every already-decided event for the month: product launches, back-in-stock products, planned sales or promotions, brand milestones and announcements.
- Treat these as anchors — do not place any other content until they are in.
- Layer optional holidays and awareness days on top afterward; find lesser-known dates via nationaltoday.com by searching the target month.
- Cap date-based emails at one or two per month, and remember you don't have to discount for them — relevant content alone is enough. Example from the source: a coffee brand owns National Coffee Day, but could also fit World Sleep Day or National Productivity Day if the positioning supports it.
- Avoid firing a 'national day' email every week; the source says it becomes annoying.
Caveat: Fixed-date clarity matters most when launches and promotions are already budgeted; for stores with no fixed events, holidays become the anchor instead.

Tags: email-lifecycle, campaign-planning, content-calendar, seasonal-marketing, promotions
Source: Klaviyo email.docx

---

## Keep sales events to one per month or fewer
Use when: Deciding how many discount or sale emails to schedule in a month and how to protect margin.
- Limit sales events to a maximum of one per month; the source says every other month is even better.
- Recognize the two costs of frequent discounting: subscribers learn to wait for the next sale instead of buying at full price, and the brand becomes perceived as a discount brand — a perception the source calls very hard to reverse.
- Treat scarcity as the mechanism: when the audience knows you rarely discount, a promotion creates urgency; when a sale is always around the corner, it creates patience.
- When planning the month, place the single sale event as a fixed anchor and build non-promotional campaigns around it.
- Sequence the calendar so full-price product and value campaigns sit in the weeks before and after the event rather than piling on more offers.
Caveat: This is the presenter's stated opinion ('I cannot stress this enough'), not a measured benchmark; inventory clearing or seasonal retail realities may justify more.

Tags: email-lifecycle, promotions, pricing, margin, campaign-planning, offer-design
Source: Klaviyo email.docx

---

## Reuse existing blog, video and social content for campaigns
Use when: Filling empty calendar slots for a store that lacks new creative bandwidth.
- Inventory existing blogs, YouTube videos, social posts, podcasts or any content generally useful to your audience.
- Match each piece to the right time of year: a summer skincare routine blog fits May or June, not November.
- Choose one of two routes per piece: tease the most interesting part and link to the full blog/video, or summarize the key takeaway and link directly to a relevant product.
- Mix or test the two routes against each other over time to learn what the audience prefers.
- If the content library is thin, search Google for topics the audience cares about and write a short educational email based on what you find — the source notes you don't need to be the original source of information, only the clear presenter who connects it to your brand.
- Verify current platform features if you plan to automate this reuse inside an ESP.
Caveat: Out-of-season content recycling can feel disconnected; timing the piece matters as much as the piece itself.

Tags: email-lifecycle, content-repurposing, campaign-planning, content-strategy, blog, education
Source: Klaviyo email.docx

---

## Plan a month of campaigns with an AI context block
Use when: Drafting a full month of email campaign ideas quickly instead of brainstorming from a blank calendar.
- Build a context block containing: brand name and what you sell; target customer and their problems; sending frequency (the source recommends three to four campaigns per week); the month being planned; fixed dates already locked in; content already placed; and the full list of campaign types from the source's library (downloadable via the free email marketing course linked in the video description).
- Prompt the AI (the source uses Claude; ChatGPT or Gemini also work) with a structured request: brand, customer, cadence, month, locked dates, the campaign-type list, then 'fill in the remaining slots with specific campaign ideas from the list that make sense for our brand and audience, including send date, campaign type, and a two-line angle description.'
- Review every suggestion against three questions: does it make sense for our brand right now; do we have the content, images and reviews to execute it; and is the overall mix balanced across the seven campaign categories.
- Swap out anything that doesn't fit and fill gaps from the idea list.
- Expect the source's claimed time of roughly 10–20 minutes for a full month; treat that as the presenter's experience, not a guaranteed benchmark.
Caveat: The output is a draft — the source explicitly says you won't use every suggestion as-is and will refine from there.
Caveat: AI planning quality depends entirely on context quality; thin inputs produce generic calendars.

Tags: email-lifecycle, campaign-planning, ai, claude, prompt-engineering, workflow
Source: Klaviyo email.docx

---

## Pressure-test the finished calendar with AI before finalizing
Use when: Doing a final quality check on a completed monthly email calendar.
- Once the calendar is filled in, paste it back into AI with a review prompt: 'Here's my email campaign calendar for [month]. Review the mix across campaign types and the weekly cadence. Flag anything that looks unbalanced, repetitive, or too promotional, and suggest alternatives where needed.'
- Use the output as a cheap pre-check that catches problems before they reach the list and before the human mix check.
- Treat AI comments as input, not verdict — the source says they are often genuinely useful but still require your judgment.
- Follow with the manual monthly and weekly mix checks described in the calendar-balance process.
- Verify current AI tool availability/features if you rely on a specific model.
Caveat: This is a supplementary check, not a replacement for reviewing the calendar yourself.
Caveat: AI cannot know your inventory, creative readiness or margin situation.

Tags: email-lifecycle, campaign-planning, ai, qa, review, content-calendar
Source: Klaviyo email.docx

---

## Check monthly mix across the seven campaign categories
Use when: Finalizing a monthly email campaign calendar and checking whether it is too sales-heavy.
- Spread the month's campaigns across the seven campaign categories used in the source's framework.
- Check the rough monthly ranges the source says work well for most ecommerce brands: one to two promotional or discount emails, four to six product-focused emails, four to six value or education emails, two to four social proof emails, and two to four brand emails.
- If more than a third of the content is promotional, remove some promotional sends and replace them with content or social proof emails.
- Treat the ranges as starting heuristics, not targets to force — the source presents them as a rough balance that works for most brands.
- Verify the category definitions in your own system if you use an ESP-native calendar.
Caveat: The bands are source-specific heuristics, not a calculated benchmark; list size, seasonality and launch cadence can shift them.

Tags: email-lifecycle, campaign-planning, content-mix, promotions, social-proof, review
Source: Klaviyo email.docx

---

## Alternate campaign types within each week, not just across the month
Use when: Sequencing a week of sends and checking why engagement dips despite a balanced monthly mix.
- Apply the rule: no two consecutive emails should be the same campaign type. If Monday is a testimonial, Wednesday cannot be another social proof send.
- Fix the common failure mode where a brand batches all social proof into one week, leaves only product highlights in the next, and produces a pattern subscribers start to ignore.
- Use the source's example well-paced week for four sends per week: Monday educational, Wednesday product-focused, Friday social proof, Sunday brand.
- Check that the week delivers a complete experience — the subscriber is educated, shown a product, given proof it works, and connected to the brand.
- Apply this week by week when finalizing the calendar rather than only auditing the month as a whole.
Caveat: Cadence depends on your sending frequency; three sends a week needs a different sequence than four.
Caveat: This is a source heuristic for variety, not an experimentally validated optimum.

Tags: email-lifecycle, campaign-planning, cadence, content-mix, engagement, social-proof
Source: Klaviyo email.docx

---

## Build a two-week execution buffer before sends go out
Use when: Fixing late, rushed campaign production that degrades email quality and coverage.
- Make two weeks of runway a non-negotiable workflow standard: emails going out in two weeks are already written, designed and queued for review.
- Recognize what writing the day before produces: quality drops, you default to promotions because they are easier under pressure, coordination with fixed dates is missed, and errors slip through with no time to catch them.
- Work backward from the calendar: two weeks before send date, the campaign should already be drafted; one week before, designed and reviewed.
- Use the buffer to coordinate launches, restocks and sale anchors with the surrounding campaign content.
- The source acknowledges this is difficult for many ecommerce brands but says to put in the effort to establish it.
Caveat: Requires enough creative and merchandising capacity to stay ahead; a hard backlog can make the two-week rule feel unattainable at first.

Tags: email-lifecycle, workflow, campaign-planning, operations, production
Source: Klaviyo email.docx

---

## Run a 20–30 minute monthly performance review
Use when: End-of-month review before planning the next month's email calendar.
- Spend 20–30 minutes at month end reviewing what went out and how it performed.
- Identify campaigns with the highest open rates; identify campaigns that drove the most clicks and revenue; identify underperformers and reason about why they underperformed.
- Keep the analysis shallow enough to be sustainable — the goal is spotting patterns, not a deep statistical study.
- Feed the patterns back into next month's calendar: repeat the formats, angles and timings that worked and drop the ones that consistently underperformed.
- Repeat monthly so the calendar sharpens over time.
Caveat: The presenter calls this super important, but the 20–30 minute figure is his own cadence, not a measured optimum.
Caveat: Small lists may not produce statistically meaningful monthly patterns.

Tags: email-lifecycle, measurement, analytics, campaign-planning, review, retention
Source: Klaviyo email.docx

---

## Put the product in every email, leading with value
Use when: Writing education, brand or social proof campaigns that risk becoming product-free content.
- Ensure every email — including those with nothing to do with a promotion — has your product somewhere in the picture.
- Lead with value: teach the audience about a problem, then position the product as the natural solution. The source frames this as useful rather than pushy.
- Rotate angles across the calendar so the relationship builds from different directions: build trust with social proof one week, educate the next, show behind-the-scenes the week after.
- Track that all these angles ultimately move the same needle — a compounding relationship that makes selling easier over time.
- Treat the campaign calendar as a system, not a hunt for a single killer email.
Caveat: This is the presenter's positioning philosophy; heavily editorial or community-led brands may deliberately separate content from product.

Tags: email-lifecycle, content-strategy, positioning, campaign-planning, brand, education
Source: Klaviyo email.docx

---

## Restrict SMS campaigns to launches, restocks and sales
Use when: Deciding which campaign calendar items get SMS versus email, especially outside the US.
- Use SMS only for three use cases: product launches, restocks and sales events.
- Route everything else on the campaign calendar to email — the source says email does the job at a fraction of the cost.
- Stop treating SMS like email: sending SMS campaigns every week burns through the SMS list and racks up costs, particularly outside the US and in Europe where rates are significantly higher.
- Monitor your SMS cost per send; the source states ROI outside these three use cases rarely makes sense given the cost.
- If based in Europe, test WhatsApp as an alternative — it is far more common there, cost per message is much lower than traditional SMS in most European markets, and the source says brands testing it now have an advantage as the channel matures.
Caveat: WhatsApp-for-ecommerce is described as still early; expect a learning curve and verify current platform support.
Caveat: This is the presenter's stated philosophy ('use it sparingly'), not an experimental result.

Tags: email-lifecycle, sms, whatsapp, campaign-planning, acquisition, cost-control
Source: Klaviyo email.docx

---

## Build a systematic AB testing mindset before running tests
Use when: Setting up an ecommerce email testing program or auditing why past tests produced no usable learning.
- Test consistently: run new tests every two to four weeks depending on volume. The source notes a brand doing over $100k/month has far more traffic and can test much faster than one doing around $10k/month.
- Write a clear hypothesis stating what you're testing, why, and the expected outcome. Instead of 'test two subject lines,' write 'adding an emoji to the subject line will increase the open rate because it will make the email stand out in the inbox.'
- Collect sufficient data before concluding. Source guidelines: at least 3–5,000 impressions per variant OR at least 15 days runtime for signup forms (7 days may be enough in some situations, but 15 is the general advice); at least 1,000 recipients per variant for flows; 500 recipients per variant can occasionally be enough if the gap is very large.
- Judge on revenue as the ultimate metric — the source says revenue decides roughly 95% of tests. Sometimes a lower click rate produces more revenue, and that trade is worth taking.
- Avoid the trap of endlessly testing only subject lines because they are easy; a winner with no hypothesis behind it teaches nothing transferable.
Caveat: The 3–5k / 15-day / 1,000-recipient figures are the source's general guidelines, explicitly qualified as situation-dependent, not universal law.
Caveat: Random tests without hypotheses produce winners you cannot reuse.

Tags: email-lifecycle, experiment-design, ab-testing, measurement, klaviyo, conversion-optimization
Source: Klaviyo email.docx

---

## Rank signup form tests by impact and work top-down
Use when: Prioritizing which signup form (popup) experiments to run first to grow the email list.
- Run the top-10 signup form tests in order of impact, starting at number one, to get the biggest gains fastest. The primary KPI for all of them is submit rate.
- 1. Offer/incentive — biggest impact by far; if the offer is bad, other hacks move submit rate only marginally (the source cites roughly 2% to 2.2% style gains). Options: BOGO, buy one get one 50% off, free gift with purchase, free digital product, free shipping, dollar-amount threshold, subscription incentive, cash back, early sale access (strong at Black Friday), mystery discount (the source's personal favorite).
- 2. Micro-step vs no micro-step — asking for a small commitment ('claim my deal' vs 'no thanks, I'll pay full price') before requesting the email. Spikes submit rate for most brands but not all; test separately for mobile and desktop because results often differ by device.
- 3. Time delay — default 6 seconds; test the 4–12 second range. Shorter delays can lower sign rate while raising total signups because more people see the form.
- 4. Scroll amount — default 60%, test 30–90%; also test exit intent on/off.
- 5. Popup vs full-page form (flyout forms, in the source's experience, never beat popups).
- 6. Headline copy — 'claim your mystery discount' style direct headlines; avoid 'welcome to Nike' or 'sign up for product updates.'
- 7. CTA button copy — first person tends to win ('claim my deal,' 'unlock my discount'); 'claim my deal' cited as consistently strong.
- 8. Microcopy — e.g. 'no thanks, I'll rather pay full price'; also test microcopy vs none.
- 9. Design/colors — plain simple forms tend to beat fully branded designs (black CTA on white, gray input fields for contrast).
- 10. Image vs no image and SMS signup angle.
- Take a holistic view on the offer test: a higher submit rate that produces much weaker welcome flow conversion may not be worth it, though you can keep nurturing those subscribers through other flows.
Caveat: The ranking is the agency's own analysis of their signup form tests, not a published benchmark.
Caveat: Being on-brand may conflict with the better-converting plain design; the source chooses conversion but says test it yourself.

Tags: email-lifecycle, signup-form, conversion-optimization, ab-testing, list-growth, offer-design, klaviyo
Source: Klaviyo email.docx

---

## Choose signup form images by device, not aesthetics
Use when: Deciding whether and which image to place in a popup or signup form.
- Test image vs no image per brand and niche — some perform better with a hero image, others plain.
- When using an image, follow the source's observed hierarchy: images with pets work best when applicable to the brand; images with human faces next; static product images perform weakest.
- Use the image as a visual cue toward the headline (the source's example shows people looking at the logo/headline text) — this pattern is described as working well.
- Skip images on mobile forms: mobile users are often on slower 4G/5G connections and loading speed matters.
- If you do use images on desktop forms, compress them to protect load speed.
Caveat: Pet imagery only makes sense if it fits the brand; forcing it is not recommended.
Caveat: These image preferences are agency observations, not measured benchmarks.

Tags: email-lifecycle, signup-form, creative-strategy, mobile, page-speed, conversion-optimization
Source: Klaviyo email.docx

---

## Test SMS signup angles against the email offer
Use when: Building or optimizing the SMS opt-in step, especially when email signup already exists.
- Decide which of three angles to test for SMS signup: the same incentive as the email list; a stronger incentive for SMS after someone joins the email list (for example 10% off email vs 50% off SMS); or the VIP club angle covering special discounts, pre-sales and early access.
- Run these as split tests rather than assuming the VIP angle wins.
- Remember SMS opt-ins carry ongoing send costs and compliance obligations, so a cheap opt-in that converts poorly downstream is not automatically good.
- Verify current SMS consent and compliance requirements for your region before launching the test.
Caveat: The source gives the three angles as test options without ranking them.
Caveat: SMS economics differ sharply outside the US, which changes how much an aggressive SMS offer is worth.

Tags: email-lifecycle, sms, signup-form, ab-testing, offer-design, list-growth
Source: Klaviyo email.docx

---

## Test the first email of every flow first
Use when: Allocating limited experimentation capacity across abandoned cart, browse, checkout, welcome and winback flows.
- Prioritize tests on the first email of each flow; the source states it has the highest impact by far across hundreds of ecommerce stores analyzed.
- Do not spend testing time on email six of a browse abandonment flow while email one is untested.
- Rank flow tests for the first email by expected impact: time delays, product block structure (hero image vs dynamic block above the fold), plain text vs designed, copy length and angle, then subject line and sender name.
- Test the whole flow's time-delay structure only after you have optimized the first email's delay.
- Recognize that flows generate the source's stated 40–70% of email revenue, which is why this reallocation matters.
Caveat: The 40–70% flow-revenue figure is the source's claim from client work, not a universal constant.
Caveat: A flow's later emails still matter for total revenue, just less per unit of testing effort.

Tags: email-lifecycle, flows, ab-testing, automation, measurement, prioritization
Source: Klaviyo email.docx

---

## Test flow time delays with flow-type reference ranges
Use when: Setting or testing send delays in site, browse, cart and checkout abandonment flows.
- Decide which of two delay tests to run: the whole delay structure, or just the delay on email one. Do the email-one test first because email one has the most impact.
- Compare an aggressive cart sequence (email one, then email two 12 hours later, then three and four at 12-hour intervals) against a regular day-by-day sequence; the source says aggressive works well for some brands.
- Use these starting windows for the first email by flow type: site abandonment 1–4 hours; browse abandonment 30 minutes to 2 hours; cart abandonment 50 minutes to 1 hour; checkout abandonment 50 minutes to 1 hour.
- Note the general pattern: the further down the customer journey, the shorter the appropriate delay.
- Set it up as a conditional split — a 50% random sample waits one duration and 50% waits another — then collect enough data before judging.
- Verify current flow-split configuration in Klaviyo, since the interface changes.
Caveat: The ranges are source-observed starting points ('massive differences' between brands), not fixed best practice.
Caveat: Running the delay test without sufficient recipients per branch produces noise.

Tags: email-lifecycle, flows, ab-testing, timing, cart-abandonment, browse-abandonment, klaviyo
Source: Klaviyo email.docx

---

## Test product blocks, dynamic feeds and hero images in flows
Use when: Optimizing abandoned browse, cart and checkout emails, and cross-sell or winback flows.
- Test product blocks vs product category blocks: some audiences want specific product recommendations, others prefer browsing general collections. Test this in welcome email one, abandonment series, post-purchase cross-sell, winback and campaigns — and re-test per situation, because a winner in welcome email one does not carry over to winback.
- Test static product blocks vs the Klaviyo product feed (which uses purchase, viewing and all-time history for recommendations). This is only relevant for stores with a large catalog, where specific recommendations are hypothesized to beat static random products.
- For abandonment series, test a hero image vs no hero image. Current structure is often a header image with a dynamic product block below; the alternative is a short headline with the dynamic product block above the fold so the exact viewed or carted product is the first thing the reader sees.
- Judge all of these on revenue, not just clicks.
Caveat: Hero-image results vary substantially by niche, per the source.
Caveat: The dynamic-feed vs static test requires enough catalog and data volume to be meaningful.

Tags: email-lifecycle, flows, ab-testing, merchandising, product-recommendations, klaviyo, personalization
Source: Klaviyo email.docx

---

## Test plain-text vs designed emails and copy variables in flows
Use when: Deciding email format and copy style for flow emails, particularly discount-bearing final emails.
- Split test plain text vs fully designed emails; some brands see plain text perform very well.
- Run this test on the first flow email (highest impact) and on the last email of the flow, especially when it contains a discount — a personal plain-text message from the founder is cited as performing well in certain niches.
- Test short copy (max three to five sentences) vs long, multi-paragraph copy.
- Test branded tone of voice vs direct-response style (harder sell).
- Test angle vs angle: pick the pain point used to persuade in one email and split test it against a different pain point; the source notes this is trickier to set up but can reveal which pain point triggers the most revenue.
- Judge on revenue rather than open or click rate.
Caveat: The source calls copy a broad subject with many possible variables; results are brand-specific.
Caveat: Angle testing is harder to isolate because the two emails necessarily differ in more than one way.

Tags: email-lifecycle, flows, ab-testing, copywriting, creative-strategy, plain-text, klaviyo
Source: Klaviyo email.docx

---

## Test landing page destinations from flow emails
Use when: Choosing where flow or campaign email links should send shoppers.
- Set up the test in Klaviyo even though it is not strictly an email AB test, then measure the end result — revenue, not clicks.
- Compare destinations such as collection page vs product page, homepage vs collection page, and a regular product page vs a purpose-built product landing page.
- Apply the general principle of making the desired action as easy as possible, which normally argues for the product page as the closest step to purchase.
- Still test the alternatives: the source notes collection or homepage can sometimes produce a better user experience and more revenue.
- Run this for campaigns too, where the same destination question recurs with each new send.
Caveat: Landing page tests mix many variables at once, so results are harder to generalize across campaigns.
Caveat: The source gives no numeric expectation for the size of the effect.

Tags: email-lifecycle, landing-page, ab-testing, product-page, conversion-optimization, flows
Source: Klaviyo email.docx

---

## Use manual 50/50 splits instead of automatic winner selection
Use when: Configuring any Klaviyo AB test for campaigns or flows.
- Always choose a manual 50/50 split: send version A to half and version B to half, 100% test size, 0% automatic winner rollout.
- Reject the automatic option (send 20% to A, 20% to B, then the winner to the remaining 60% after a few hours) for two stated reasons: the largest segment receives the email at a time that is not your optimal send time, and two to three hours is too short a window to determine a winner.
- Select place order rate as the winning metric for campaigns.
- Analyze results after a couple of days, then apply the learning to future sends.
- For flows, either let the test run while the sample accumulates or review after reaching the recipient threshold.
- Verify current Klaviyo test configuration options before building.
Caveat: Manual splits delay the winner reaching the full list, which is acceptable because you learn for future sends rather than optimize one send.
Caveat: The source attributes low statistical significance partly to auto-selection's short window.

Tags: email-lifecycle, ab-testing, klaviyo, experiment-design, measurement, campaign-planning
Source: Klaviyo email.docx

---

## Run systematic campaign-side tests, starting with send time
Use when: Deciding what to test on recurring newsletter-style campaigns rather than flows.
- Prioritize send time and date — the source calls it capable of dramatically affecting opens and revenue. Run exploratory tests at least five times to find audience-specific patterns.
- Look at revenue alongside open rate: a 7 a.m. send may win opens while a 2 p.m. send wins revenue, and the source says to favor revenue.
- Test email angles: which pain points or brand USPs trigger the best response.
- Test landing pages (collection vs product vs homepage vs dedicated page), and dynamic Klaviyo feed vs static product blocks.
- Also test subject lines, sender names and CTA buttons, but recognize campaigns are trickier than flows because each send has new content — a CTA winner on campaign A may not transfer to campaign B sent at a different time or with a different type.
- Verify current Klaviyo reporting fields when comparing revenue across send-time tests.
Caveat: Campaign tests rarely produce clean generalizable rules because content changes every send.
Caveat: The five-run minimum for send-time exploration is the source's recommendation, not a statistical guarantee.

Tags: email-lifecycle, campaign-planning, ab-testing, timing, measurement, copywriting
Source: Klaviyo email.docx

---

## Deprioritize subject line, sender name and CTA button tests
Use when: Choosing which email tests to run when testing capacity is limited.
- Recognize that subject line tests are easy and fast but generally do not have the biggest revenue impact; the source warns against falling into the trap of only testing subject lines.
- When testing subject lines, still make them strategic: emoji vs no emoji, first name vs no first name, urgency vs no urgency, offer in subject line vs preview text, specific numbers vs none.
- Test sender name (e.g. 'Apple' vs 'Tim from Apple'), which is interesting especially for plain-text founder emails and can boost open rate, but again has modest revenue impact.
- Recognize CTA button tests (text, size, color — 'buy now' vs 'shop now', regular vs high-contrast color) as the lowest-impact test on the flow list; don't start here even though it is popular.
- Sequence these after time delays, product blocks, plain text, copy and landing page tests are done.
Caveat: The source explicitly calls CTA button testing low impact and warns against starting there.
Caveat: Subject line and sender name tests still consume send volume and recipients, so they are not free.

Tags: email-lifecycle, ab-testing, subject-lines, prioritization, copywriting, campaign-planning
Source: Klaviyo email.docx

---

## Set the upper bound on test duration and sample per variant
Use when: Deciding when to call an email AB test and move to the next one.
- Wait for at least 1,000 recipients per variant as the rule of thumb for flows.
- Accept 500 recipients per variant only when the difference between variations is already massive.
- Plan roughly two weeks per test so multiple tests can run per month, and note the source's qualified exception: 7 days can be enough in some situations, but 15 days is the general advice for flows and signup forms.
- For signup forms, require at least 3–5,000 impressions per variant or 15 days of runtime, whichever takes longer — even if 3–5,000 impressions arrive in a single day, stretch the test over multiple days.
- Scale test throughput to list volume: higher-traffic brands reach thresholds faster and can test more per month; smaller brands need more calendar time per test.
Caveat: These thresholds are the source's general guidelines, explicitly described as situation-dependent rather than a statistical formula.
Caveat: Concluding early on a small sample produces false winners that then get applied to future sends.

Tags: email-lifecycle, ab-testing, measurement, experiment-design, sample-size, klaviyo
Source: Klaviyo email.docx

---

## Build segments that start with marketing eligibility
Use when: Creating or auditing send segments for campaigns and flows, especially in Europe.
- Create the segment under Lists & Segments → Create → Segment.
- Add the mandatory starting condition 'person can receive email marketing' so the segment only targets active profiles who can be marketed to.
- If based in the US, this condition is sufficient.
- If based in Europe, add a further filter for subscription/consent status under GDPR-aware rules, because the ability to receive marketing does not equal consent. Example from the source: someone who entered their email at checkout can receive email marketing but is not officially subscribed; similarly, a purchaser who never consented to email marketing.
- Build segmentation to make campaigns relevant to recipients rather than as an advanced extra.
- Verify current Klaviyo segment condition names and European consent handling, since both the interface and privacy requirements change.
Caveat: The source cautions that European rules add complexity beyond the single eligibility condition; confirm your own compliance obligations.
Caveat: Segments built without the eligibility filter risk sending to profiles that should be suppressed.

Tags: email-lifecycle, segmentation, klaviyo, gdpr, compliance, list-hygiene
Source: Klaviyo email.docx

---

## Build an engaged-90-day segment as your campaign workhorse
Use when: Setting up campaign send audiences or starting deliverability recovery in Klaviyo.
- Create a segment starting with the condition 'person can receive email marketing' as a base for every segment you build.
- Add condition: 'has opened email at least once in the last 90 days', then clone that condition and set it to 'has clicked email at least once in the last 90 days' — keep logic on OR, because an open may fail to track while a click registers.
- Keep everything on OR and add further conditions: placed order at least once in last 90 days, checkout started at least once, active on site at least once. Do not add 'viewed product' or 'added to cart' because these are already captured by active-on-site.
- Clone the segment and swap the timeframe to 14, 30, 60 and 120 days so you have a ladder of engagement windows.
- If you have severe spam issues, temporarily drop the website conditions and use only opened/clicked email until open rates recover.
- Use the engaged-90 segment as the default audience for most campaigns; use tighter windows (14/30) when repairing deliverability.
Caveat: The source reports typically achieving 50%+ open rates with engaged-90 segments for its clients; this is a source-specific experience, not a guaranteed benchmark.
Caveat: For EU lists you must filter further on 'because person subscribed' due to GDPR consent rules; US-based lists can rely on 'can receive email marketing' alone, though subscribed contacts usually engage better.

Tags: email-lifecycle, segmentation, klaviyo, deliverability, campaigns, or-logic
Source: Klaviyo email.docx

---

## Mandatory exclusion segments for every campaign
Use when: Before sending any campaign, or during a list-cleaning pass.
- Build a 'marked as spam' exclusion segment: person can receive email marketing AND has marked email as spam at least once over all time.
- Build a bounce exclusion segment with two branches: has bounced email at least 4 times over all time where bounce type = soft, OR has bounced email at least once over all time where bounce type = hard.
- Treat hard bounces as permanent (suppress after one) and soft bounces as temporary (allow up to four attempts before suppressing).
- Add these as exclusions on every single campaign you send.
- To remove them permanently, open the segment, click the three-dot menu, choose 'suppress current members', then bulk suppress.
- Allow roughly one to two hours for Klaviyo to update suppression counts depending on segment size.
- Maintain an 'all but unsubscribed and suppressed' master segment: can receive email marketing, email does not contain the text 'q.com' (bot addresses), and has marked email as spam zero times over all time.
- Send to this master segment roughly one to two times per month to give unengaged people a chance to re-engage without burning your reputation.
Caveat: Always send campaigns to segments, not lists, per the source's stated preference.
Caveat: Bot filters and suppression counts may need refreshing as data changes; re-check segment membership over time.

Tags: email-lifecycle, segmentation, deliverability, klaviyo, suppression, list-hygiene, bounces
Source: Klaviyo email.docx

---

## Build unengaged segments that exclude past customers
Use when: Building sunset flows and long-term suppression rules to protect deliverability and reduce Klaviyo costs.
- Create unengaged-120: opened email zero times in last 120 days AND clicked email zero times in last 120 days AND placed order zero times over all time AND checkout started zero times in last 120 days AND active on site zero times in last 120 days.
- Use AND here, not OR — you want fully inactive contacts, the opposite of the engaged-segment logic.
- Set placed order to 'zero times over all time' (not 120 days) so that anyone who ever bought stays on the list and can still be re-activated.
- Clone to unengaged-180 (six months) and use it as an exclusion segment and periodic suppression source.
- Use unengaged-120 as the trigger audience for a sunset/unengaged reactivation flow.
- Suppress the 180-day group over time if they never purchased, because removing them improves deliverability and lowers Klaviyo cost.
Caveat: The source deliberately keeps past buyers on the list indefinitely, reasoning that a customer from over a year ago can still be reactivated; this is a judgment call you can adjust to your margin structure.

Tags: email-lifecycle, segmentation, deliverability, klaviyo, sunset-flow, retention
Source: Klaviyo email.docx

---

## Specialty segments for buyer-stage targeting
Use when: Planning sales events, loyalty messaging or new-customer reactivation offers.
- First-time buyers: placed order = 1 over all time AND can receive email marketing — use for a specific second-purchase offer.
- Returning customers: placed order at least 2 times over all time — differentiate loyalty messaging from first-timer messaging.
- Non-buyers: placed order zero times over all time — during sales events the source gives non-buyers an extra discount on top of the event discount, since existing customers don't need the extra nudge.
- VIPs: define per brand, e.g. placed order at least 4 times over all time, or total spend at 3–4× AOV.
- High potentials: checkout started, added to cart, viewed product, or active on site at least once in the last 30 days, AND did not place an order in the last 30 days — use as a base for a targeted flow or one-off offer.
- Win-back: placed order at least once in the last 6 months but zero times in the last 90 days — use as the base for a win-back flow or a one-off campaign.
Caveat: VIP thresholds differ by brand and niche; the source explicitly says there is no universal definition — set thresholds from your own AOV and repeat-purchase data.
Caveat: The extra-discount-for-non-buyers tactic is the source's agency practice; validate margin impact before adopting.

Tags: email-lifecycle, segmentation, klaviyo, retention, win-back, offers, vip
Source: Klaviyo email.docx

---

## Diagnose deliverability with placement testing and Klaviyo metrics
Use when: Open rates are consistently low and you need to locate the cause before changing strategy.
- Treat open rates consistently below 30–35% as a likely inbox placement problem (the source cites 50%+ as achievable for engaged segments, so far below that signals an issue).
- Option 1: send a test campaign to a seed list via a placement tool (the source names GlockApps) to see primary-inbox, promotions and spam split, blocklist status and IP reputation; the source suggests running this monthly.
- Option 2: in Klaviyo, open the last five sent campaigns and go to the deliverability tab to review open rate, click rate, bounce rate, unsubscribe rate and spam complaint rate.
- Check 'performance by inbox provider' — a problem may exist only with Hotmail/Outlook while Gmail is healthy.
- Check 'performance by country' — if one country underperforms, send only to a tighter engaged segment there for a while to rebuild engagement.
Caveat: Tool names and menu locations change; verify current interfaces before relying on paths.
Caveat: The 30–35% and 50%+ figures are the source's heuristics for its own clients, not universal benchmarks.

Tags: email-lifecycle, deliverability, klaviyo, measurement, diagnostics, list-hygiene
Source: Klaviyo email.docx

---

## Four-step technical setup for email sending
Use when: Initial Klaviyo setup or auditing an account with unexplained placement problems.
- Add a branded sending domain in Klaviyo under Settings > Account > Domains; enter the root domain and add the required DNS records until status shows live.
- Set your default sender email address to an address ending in the branded domain (e.g. hello@yourbrand.com) — never a free-mail or unrelated domain.
- Add a DMARC record as a TXT record with name '_dmarc' in your DNS; the source identifies this as the most commonly missing piece when auditing ecommerce brands.
- Verify DMARC with a free checker tool (the source names GlockApps' DMARC checker) to confirm the record resolves correctly.
- Optionally implement BIMI to authenticate your logo in the inbox and, on some clients, display a blue verification check; the source cites roughly $1,500/year and says it's worth considering for eight- and nine-figure brands, sometimes seven-figure.
- Treat technical setup as necessary but rarely the main cause — the source states it rarely fixes a deliverability problem on its own.
Caveat: BIMI requires DNS configuration and provider support (Gmail, Yahoo and some Apple versions per the source); costs and requirements should be verified at implementation time.
Caveat: DMARC/SPF/DKIM values must match your specific provider's current instructions.

Tags: email-lifecycle, deliverability, klaviyo, dns, dmarc, technical-setup, bimi
Source: Klaviyo email.docx

---

## Five-step list-cleaning protocol
Use when: Any account with a large list and low engagement, or as a periodic hygiene pass.
- Segment 1 — long-term unengaged: opened email zero times in last 90 days, clicked zero, active on site zero in last 180 days, placed order zero times in last 365 days, received email at least 10 times in last 180 days, and can receive email marketing.
- Segment 2 — no recent sends: active or created at least a year ago, received email zero times in the last year, active on site zero times in the last year, and can still receive email marketing.
- Segment 3 — never opened: active or created at least a year ago and received email zero times over all time (i.e. essentially never contacted).
- Segment 4 — spam markers: marked email as spam at least once over all time.
- Segment 5 — bounces: soft bounced 4+ times over all time OR hard bounced at least once.
- Suppress each segment via the three-dot menu > suppress current members > bulk suppress; wait one to two hours for Klaviyo to process.
- Result: remaining list is engaged or semi-engaged, and you stop signaling to Gmail/Outlook that you mail people who report or reject you.
Caveat: Suppression is not reversible in bulk without re-adding contacts, so apply segments carefully and confirm counts before bulk suppressing.
Caveat: The '10 emails in 180 days' and '365 days' thresholds are the source's cleaning heuristics; seasonality or low-frequency programs may justify adapting them.

Tags: email-lifecycle, deliverability, list-hygiene, klaviyo, suppression, cost-reduction
Source: Klaviyo email.docx

---

## Ramp deliverability back with a staged engagement ladder
Use when: A store has a known deliverability problem (consistently low opens, spam complaints) and needs a recovery sequence.
- Week 1–2: turn off all flows except welcome, post-purchase and browse/checkout abandonment.
- Week 1–2: send 3 campaigns per week only to the engaged-14-day segment (6 emails total).
- After 2 weeks, check those campaigns' open rates. If at or above 50%, move up. If below 50%, repeat another 2 weeks at 14 days.
- If still below 50%, strip website activity from the engaged segments and use only opened/clicked email conditions.
- Then send 3 campaigns/week for 2 weeks to engaged-30; re-check. Expect a small dip but require it to stay near 50% to advance; otherwise repeat 2 more weeks.
- Continue the same two-week-per-stage process for engaged-60 and engaged-90.
- Once engaged-90 is stable, make it your main campaign audience and turn all flows back on.
- If opens trend toward 60%, you can keep widening to 120/150/180 days while staying above 50%, though the source still recommends keeping the majority of sends at engaged-90.
Caveat: The 50% open-rate gate is the source's operational target for its own clients, not a universal benchmark.
Caveat: Ramp speed depends on list size and existing reputation; smaller engaged windows may send very few emails in week one.

Tags: email-lifecycle, deliverability, klaviyo, campaigns, segmentation, recovery
Source: Klaviyo email.docx

---

## Make emails readable to Gmail's AI filter
Use when: Designing or auditing campaign templates for inbox placement.
- Write descriptive alt text for every image — say what is shown and include any discount and code (e.g. 'person eating pizza — 15% off with code X').
- Switch from design product blocks to Klaviyo's native product blocks so product information is live text rather than baked into an image.
- Use live-text top bars for offers instead of image banners.
- Put live text in the footer: product category links, loyalty status, store locator, support information.
- Keep sending plain-text emails regularly (the source suggests 1–3 per month) for AI readability and strong engagement.
- Do not abandon design entirely — the requirement is that the email is understandable without reading the images.
- Keep the above-the-fold section highly optimized since most readers never scroll: a single clear primary call to action with a contrasting button.
Caveat: This is the source's forward-looking adaptation to Gmail's AI features; results will vary as inbox providers change behavior.
Caveat: Plain-text emails should still carry your brand voice and offer, not be blank utility messages.

Tags: email-lifecycle, deliverability, creative-strategy, pdp, email-design, gmail, plain-text
Source: Klaviyo email.docx

---

## Structure emails for clicks and replies, not just opens
Use when: Writing or redesigning campaign templates after a low click-through or low reply rate.
- Use conversational subject lines; the source's test is whether a friend would send that subject line to a friend — if not, Gmail is likely to classify it as promotional.
- Keep emails short and use shorter body copy.
- Include a single primary call to action above the fold with a contrasting button.
- Share only 3–5 products per email, for example in a 2×2 grid, each with its own 'shop now' button, and end with a 'shop all' button for people who don't like the featured items.
- Periodically send plain-text emails to invite replies; the source stresses that replies are a powerful human-interaction signal for Gmail.
- Use live-text footer links to product categories, which the source reports reliably lifts click rates.
- Avoid sending a heavily promotional email every single week; mix in non-promotional sends.
Caveat: The source's click-rate targets (5%+ minimum, explicitly rejecting Klaviyo's reported 1–1.2% benchmark) are its own opinion and depend on list quality and offer strength.
Caveat: Reply invitations only work if someone monitors and responds to the inbox.

Tags: email-lifecycle, deliverability, creative-strategy, email-design, conversion-optimization, copywriting
Source: Klaviyo email.docx

---

## Use AI to analyze exported campaign analytics
Use when: You lack analyst bandwidth and need a quick diagnostic of recent campaign performance.
- In Klaviyo, go to Campaigns, open the three-dot menu and choose 'export analytics'.
- Select the time range (year-to-date or at least the last 90 days), choose email only (or include SMS), and include all A/B test message variations.
- Export the CSV and upload it to an AI assistant (the source uses ChatGPT).
- Prompt it as an email marketing data specialist and ask for a specific number of data-backed observations with recommendations.
- Example framing the source used: 'analyze this data set and give me 10 observations with recommendations on how to improve it'.
- Use the output to identify bottleneck metrics (e.g. high uncorrected opens but low unique clicks) and get concrete next actions like redesigning templates around one above-fold CTA, adding contrasting buttons and shortening copy.
- Look for the AI's diagnosis of day-of-week and send-time patterns, subject-line features (e.g. emoji presence) and bounce spikes, then design controlled tests from those hypotheses.
Caveat: Treat AI recommendations as hypotheses to test, not instructions; the AI may propose test windows or KPIs that don't match your business.
Caveat: The source notes it optimizes for placed-order rate rather than open rate when testing send times, since opens can be high in the morning while purchases concentrate in the evening.

Tags: email-lifecycle, measurement, experiment-design, campaigns, ai-tools, klaviyo
Source: Klaviyo email.docx

---

## Use AI to diagnose flow performance and prioritize tests
Use when: Deciding which email flow to optimize next, or auditing a mature automation program.
- In Klaviyo, go to Flows, open the options menu and choose 'export analytics'.
- Select at least the last 90 days (year-to-date is fine), aggregate by day, include all A/B test message variations, and export the CSV.
- Prompt the AI as an email marketing data specialist to analyze the flow data set and return a set number of data-backed observations with concrete recommendations.
- Use the output to rank flows by revenue contribution and to identify where a small lift compounds most.
- Prioritize A/B tests on the highest-volume, highest-revenue flow rather than low-traffic emails, because a lift on a flow with few recipients barely moves the business.
- Follow up with a focused prompt on one flow (e.g. the welcome series) to get email-by-email findings and prioritized actions.
Caveat: This is the source's workflow with ChatGPT on its agency client data; the specific observation counts and findings are examples, not promises.
Caveat: AI output quality depends on data completeness and the clarity of your prompt; always verify claims against the raw CSV before acting.

Tags: email-lifecycle, measurement, experiment-design, flows, ai-tools, klaviyo, prioritization
Source: Klaviyo email.docx

---

## Where welcome-flow revenue actually concentrates
Use when: Auditing or rebuilding a welcome/onboarding flow.
- Export welcome-flow analytics and check revenue by email. In the source's case, email one contributed roughly 88% of welcome-series revenue and the flow generated a large share of total flow revenue.
- Accept that email one converting hardest is natural — subscribers sign up to use the discount they just saw.
- Treat emails two through five-plus as nurture for the majority not ready to buy, with the goal of guiding them toward a future first purchase rather than matching email one's revenue.
- If trailing emails generate zero revenue, consider shortening the series or repurposing them as behavior-based follow-ups rather than sending low-impact messages.
- A/B test subject lines on email one first, since that is where volume is highest and any lift compounds fastest.
Caveat: The 88% figure comes from one client's data set in the source and should be treated as an illustrative example, not a benchmark you should expect.
Caveat: The source still notes that email marketing ROI is high, so cutting later emails should be justified by their poor incremental performance, not just low revenue.

Tags: email-lifecycle, flows, welcome-flow, retention, experiment-design, measurement
Source: Klaviyo email.docx

---

## Spot under-monetized flows and channel gaps
Use when: Reviewing browse abandonment, cart abandonment and cross-channel follow-up performance.
- For each flow, compare open rate, click rate and order rate; the source's example flagged a browse flow with 42% opens but only ~2.3% clicks and a 6% order rate.
- Where clicks are weak relative to opens, add dynamic product blocks and a single hero call to action to rebuild intent.
- For non-clickers, consider an SMS follow-up if your SMS flow shows strong revenue per recipient — in the source's case the SMS browse flow showed €1.70 per recipient while the email version underperformed.
- Check for channel-specific gaps: the source's analysis flagged checkout abandonment traffic as small, SMS checkout as a hidden gem, post-purchase leaving money on the table and win-back flows barely converting.
- Prioritize the fixes with the highest combination of traffic volume and revenue impact.
Caveat: The specific rates and €1.70 per-recipient figure are one client's data used as an illustration, not a benchmark.
Caveat: SMS follow-up requires separate consent collection and compliance, which the source does not detail here.

Tags: email-lifecycle, flows, measurement, sms, browse-abandonment, conversion-optimization, cross-channel
Source: Klaviyo email.docx

---

## 2026 deliverability KPI targets for ecommerce email
Use when: Reviewing Klaviyo campaign health or setting reporting thresholds for an email program.
- Open rate: target at least 45% minimum, ideally 50% or higher, on engaged segments.
- Click rate: target 5% or higher; the source explicitly argues against Klaviyo's suggested 1–1.2% benchmark because it forces overly tight segments.
- Spam complaint rate: keep at 0.01% or lower and actively monitor it.
- Unsubscribe rate: aim for 0.3% or lower, but treat it as less critical than in the past because one-click unsubscribe in Gmail has raised unsubscribe rates and unsubscribes don't directly hurt deliverability.
- Still minimize unsubscribes because a shrinking list costs long-term revenue.
- Track provider- and country-level breakdowns in addition to overall numbers, since averages can mask local problems.
Caveat: These thresholds are the source's recommendations for its own client work, not industry standards; they depend heavily on list source and offer strength.
Caveat: The source's disagreement with Klaviyo's click-rate guidance is an opinion — test against your own conversion economics rather than adopting either figure blindly.

Tags: email-lifecycle, deliverability, measurement, klaviyo, kpis, campaigns
Source: Klaviyo email.docx

---

## Sequence the email system as a connected chain, not isolated tactics
Use when: When planning the next quarter of email work or deciding which email project to start next in an ecommerce store.
- Start with list growth: the source argues that without a steady stream of new subscribers every other email effort operates on a shrinking audience, so fix signup capture before adding complexity elsewhere.
- Layer the five core flows next: welcome, browse abandonment, abandoned cart, abandoned checkout and post-purchase. These capture existing intent rather than trying to manufacture it.
- Add campaigns after flows: campaigns create momentum with your list, but they work better when triggered flows are already catching high-intent behaviour.
- Add A/B testing only on top of already-working elements; the source frames testing as sharpening what works, not as a rescue tool for broken flows.
- Layer segmentation to keep sends relevant, then treat deliverability as the foundation that decides whether any of it reaches the inbox.
- Use AI last, as an execution accelerator across the whole system rather than a replacement for the structure.
- Work through the sections one at a time as a buildout roadmap instead of implementing everything at once.
Caveat: The source is a course summary from an agency that also sells buildout services; the sequencing is the presenter's framework, not a measured benchmark.
Caveat: Stores with a large existing list but weak capture may reasonably prioritise flows over list growth.

Tags: email-lifecycle, automation, list-growth, campaigns, deliverability, segmentation, experiment-design
Source: Klaviyo email.docx

---

## Audit your email program against the six-layer dependency model
Use when: When email revenue has plateaued and you need to diagnose which stage of the ecommerce email program to invest in next.
- List the six layers: list growth/signup forms, core triggered flows, campaigns, A/B testing, segmentation and deliverability.
- For each layer, record whether it exists, how it is performing and whether the layer above it depends on it.
- Look for breaks in the chain: signup forms feeding flows, flows capturing intent, campaigns creating momentum, tests sharpening winners, segmentation keeping messages relevant and deliverability getting mail to the inbox.
- Prioritise the earliest broken link, because later layers inherit problems from earlier ones; a great campaign calendar wastes effort if subscribers are not being captured or mail is not landing.
- Implement fixes sequentially rather than simultaneously so you can tell what changed outcomes.
- Expect the payoff to be a cleaner system with better timing and more relevant messaging, not simply a higher volume of sends.
Caveat: This is the presenter's diagnostic framing from an email course, not a validated scoring model; treat layer priority as a judgement call for your store.
Caveat: If you sell agency services or build systems for clients, this audit works the same way for a client account, but the source's own pitch to book a buildout call is not a required step.

Tags: email-lifecycle, audit, automation, campaigns, deliverability, segmentation, measurement
Source: Klaviyo email.docx

---

## Write 12 months of emails in one sitting
Use when: Deciding whether to start or restart a store email program and dreading the ongoing workload.
- Commit to a small, finite batch first: 12 or 24 emails, not an open-ended commitment.
- Sit down once and write them all in one block (Hormozi says 24 emails took him roughly half a day).
- Realize from that session that a year of list communication costs about half a day, which reframes email as cheap rather than as another plate to spin.
- Start with once a month if you have never mailed; treat anything beyond the pre-written batch as bonus.
- Prefer a quality threshold over a rigid cadence if committing to a schedule makes your writing worse — send when you have good material, not to satisfy a calendar.
Caveat: Source-specific: this is Hormozi's own framing of his hesitation; the half-day figure is his, not a benchmark.
Caveat: Batching works for evergreen tactical content; it is poorly suited to inventory drops, launches or time-sensitive promotions.

Tags: email-lifecycle, email-cadence, content-planning, retention, newsletter-strategy
Source: Learn Email Marketing in 39 Minutes.docx

---

## Plain-text email format to stay out of the Promotions tab
Use when: Planning the HTML/template for any store campaign email, especially retention and re-engagement sends.
- Write the email as mostly text with a handful of sentences, approximating an everyday email between two people.
- Send zero images where possible; if you must, keep them minimal, since image-heavy 'Vegas Strip' promotional layouts read as pure promotion to filters.
- Limit to one or two links maximum per email.
- Remove money-related language from the body and subject where you can — Hormozi observed more money words correlate with a higher share landing in the Promotions tab.
- Ask recipients to reply as part of the flow (see the Reply Yes card) because replies signal engagement to providers.
- Mentally model the provider's objective: they want to deliver the highest-quality inbox experience, so align with that instead of hunting hacks.
Caveat: The source notes 16.9% of B2B marketing emails never reach the inbox at all, driven by domain reputation — plain text is one input, not a silver bullet.
Caveat: No images means you cannot show product photography, so this format suits tactical/editorial sends more than visual product launches.

Tags: email-lifecycle, deliverability, copywriting, promotions-tab, email-format, retention
Source: Learn Email Marketing in 39 Minutes.docx

---

## The Money Minute structure: reward on every step
Use when: Designing the standard template for a recurring store newsletter or retention email.
- Open with an immediate one-glance reward — a quote, a striking line or a tweet — so the reader is paid back the instant they open.
- Follow with one single tactical idea, kept to roughly 200 words (about a minute of reading); resist adding a second concept.
- Frame the tactic as problem → solution → how: name a condition that makes the solution necessary, give the solution, then the concrete tactic.
- Insert a contextual CTA that bridges from that specific content rather than a generic copy-pasted button.
- Close with a P.S., because after the subject line it is the most-read part of an email.
- Keep the format identical every send so readers know exactly what they are getting — the McDonalds principle: same shape, different quality burger each time.
Caveat: Hormozi explicitly says the 200-word limit is his format choice, not a rule of law — his colleague Lila sends longer story-based emails to higher-revenue segments and they perform well.
Caveat: Placement of CTA vs P.S. is flexible; the source says there is no science to it.

Tags: email-lifecycle, email-format, copywriting, newsletter-strategy, cta, retention
Source: Learn Email Marketing in 39 Minutes.docx

---

## Reward every step with a feedback-loop email design
Use when: Restructuring an underperforming store newsletter or welcome sequence where readers open but never act.
- Analyze behavior as after-the-fact reward, not as a preceding trigger: people repeat actions that previously paid off.
- Reward the open with a one-glance payoff at the very top of the body (quote, punchline, striking stat).
- Reward the read with a complete, usable tactic — the reader should be able to apply it to their business immediately.
- Reward the click by placing high-value hidden content behind the link (a video, a deeper document) rather than duplicating the email content.
- Protect the loop: one bad email can break the habit, so prefer extending a silence over sending something weak.
- Accept that failing to earn opens and clicks eventually pushes the sender toward the Promotions tab — the source calls this 'email death'.
Caveat: A single poor send can undo accumulated trust, so the model punishes volume without quality.
Caveat: Rewards must be real; promising value behind a link and not delivering it is treated by the source as the worst outcome.

Tags: email-lifecycle, retention, copywriting, customer-research, newsletter-strategy
Source: Learn Email Marketing in 39 Minutes.docx

---

## Reply Yes onboarding to train provider reputation
Use when: Setting up or revising the welcome and lead-magnet delivery flow for a store's opt-in.
- Structure the welcome email so the lead magnet is delivered only after the subscriber replies 'Yes'.
- Give a reason to reply by making the reward clearly worth the action (e.g. an exclusive chapter or asset).
- Use the pre-reward moment to sell regular communication, not just the freebie — subscribers who only want the magnet will ignore everything after.
- Place the lead magnet mention near the end, after you have sold the ongoing value, so you surprise and delight before giving the promised item.
- Inside the gated asset, continue the loop by pointing to specific pages and asking for further engagement.
- Treat this as building domain reputation with inbox providers — many small positive signals rather than one hack.
Caveat: Reputation is cumulative; the source describes it as '100 golden BBs', not a single silver bullet.
Caveat: Reply-gating adds friction, so it will reduce raw opt-in-to-magnet completion compared with instant delivery.

Tags: email-lifecycle, deliverability, welcome-sequence, lead-magnet, promotions-tab, retention
Source: Learn Email Marketing in 39 Minutes.docx

---

## Make unsubscribing easy to protect deliverability
Use when: Configuring the unsubscribe link, preference center and list hygiene for a store's email program.
- Make the unsubscribe action visible and simple rather than buried or requiring a support request.
- Reason from deliverability: uninterested subscribers who stay on the list drag down domain-level sending reputation over time.
- Treat a subscriber who unsubscribes as still aware of your brand — they may still buy later through another channel or inbox, so do not treat it as a loss.
- Accept a higher unsubscribe rate on your first send in a long while — the source calls this 'shaking the tree', effectively pulling forward churn.
- Benchmark against it: Hormozi reports over 1% on his first-ever send, settling to roughly 0.42% per email, and treats the program as healthy as long as list growth between sends exceeds unsubscribes.
Caveat: The 1% / 0.42% figures are one sender's list, not a target for all stores.
Caveat: If unsubscribes exceed growth, the reasoning inverts and the cadence or content is the problem.

Tags: email-lifecycle, deliverability, list-hygiene, retention, churn
Source: Learn Email Marketing in 39 Minutes.docx

---

## Segment the list by qualifier answers at opt-in
Use when: Designing the opt-in form and deciding who receives which store campaign or educational email.
- Add qualifying questions to the opt-in — for example revenue band, whether they run a business, or product-usage level for a store.
- Route sends by segment (e.g. a specific tactic only to the 500k+ group, another to 0–100k).
- Recognize that mismatch, not email quality, is usually why a send underperforms — advanced content to beginners or the reverse reads as 'not for me'.
- Encourage honest answers: subscribers who lie to get the 'better' tier receive content that does not apply to them.
- Cite the cited study result as context only: HubSpot research referenced in the source found segmented lists produced a 791% increase in email ROI.
Caveat: The 791% ROI lift is a third-party study result cited by the source, not a promise for your list.
Caveat: Every extra opt-in field costs signups, so weigh the segmentation gain against form friction.

Tags: email-lifecycle, segmentation, opt-in, customer-research, measurement, retention
Source: Learn Email Marketing in 39 Minutes.docx

---

## Make CTR the primary email metric, not open rate
Use when: Choosing the KPI for a store email program and reviewing send-to-send performance.
- Decide on the definition first: CTR can mean clicks as a share of all recipients, or of those who opened — the two produce very different numbers.
- Use clicks-as-share-of-sent as the metric tied to action, since it is independent of open-tracking accuracy.
- Report both so you can tell an open-rate problem from a click-rate problem.
- Evaluate over a rolling period rather than per email, balancing 'deposit' sends against harder 'withdraw' asks.
- Use the source's own figures only as orientation: roughly 35.7% open rate and 8.5% CTR across three months on his list, which he treats as a strong CTR.
- Accept that open-rate accuracy is degraded by privacy changes and treat it as directional.
Caveat: The 35.7% / 8.5% figures are one sender's list — not a benchmark to hold yourself to.
Caveat: The source states he is confident in CTR but not in the open-rate reporting.

Tags: email-lifecycle, measurement, click-through-rate, analytics, retention
Source: Learn Email Marketing in 39 Minutes.docx

---

## Split-test subject lines on a slice, then send the winner
Use when: Optimizing subject-line performance for recurring brand emails or product campaigns.
- Create two variants of the subject line and let the platform send each to a small percentage of the list.
- Wait for the winner to emerge, then send that variant to the remainder.
- Model the same pattern used for video thumbnails: automated variant testing picks the better performer.
- Weigh brand consistency: if you are building a named recurring format, keeping the same prefix every time can cost some short-term open rate in exchange for a habit-driven long-term open.
- Optimize the preview text as a separate asset — it is the first roughly 150 characters shown and the source reports up to a 24% open-rate lift from crafting it (source-reported figure).
- Do not let the preview default to the first 150 characters of the body, which is often a greeting and carries no curiosity value.
Caveat: The 24% preview-text lift is attributed to the source's reported experience, not a guaranteed result.
Caveat: Fixing a branded subject prefix sacrifices subject-line testing upside; the source frames this as a deliberate trade-off.

Tags: experiment-design, email-lifecycle, subject-lines, preview-text, measurement, conversion-optimization
Source: Learn Email Marketing in 39 Minutes.docx

---

## Send at the right day and hour for B2C vs B2B
Use when: Scheduling a store's campaign or newsletter sends across a week.
- For B2C, prefer Monday and Tuesday based on Nielsen/Neil Patel data cited in the source, with about an 18% average open-rate increase.
- For B2B, prefer Wednesday (source notes Wednesday delivered a comparable lift to the B2C Monday/Tuesday effect).
- Justify it as attention availability: consumers are more distracted early week; business buyers catch their breath midweek.
- Send in the pre-lunch and post-lunch windows — roughly 10:00–noon and 1:00–3:00 — since the first thing in the morning is dominated by genuine business mail.
- If you operate in a single time zone, use these windows deliberately; if your list is spread internationally, do not over-invest in timing precision.
- Pick a reference time zone and stay consistent with it.
Caveat: These day/time effects are described as small lifts, not transformative — the source calls them 'golden BBs'.
Caveat: Relevance drops sharply for multi-time-zone audiences.

Tags: email-lifecycle, send-time, scheduling, measurement, retention
Source: Learn Email Marketing in 39 Minutes.docx

---

## Keep cadence high but content value-only
Use when: Setting the sending frequency and give/ask balance for a store's list.
- Start at once a month if you are not mailing, then increase as quality holds.
- Target about three sends a week only when content stays strictly value-driven; the source reports this as the sweet spot after talking to experienced email marketers.
- Skip the classic promo/educational rotation: make every email valuable and simply make the path to your offer easily available, the way a link-in-bio works.
- Remove the need to balance a give/ask ratio by never treating a send as pure ask.
- Note the alternative: the source personally dislikes committing to a cadence and prefers sending when he has good material.
- If frequency is harming quality, lower frequency rather than lower quality.
Caveat: 'Three times a week' is passed on as advice from other email marketers, explicitly labelled as not a rule.
Caveat: Emailing more often than a store can produce honest value is expected to burn the list.

Tags: email-lifecycle, email-cadence, retention, newsletter-strategy, content-strategy
Source: Learn Email Marketing in 39 Minutes.docx

---

## Optimize for mobile rendering before sending
Use when: Final QA before sending any store email, especially image- or layout-heavy templates.
- Preview the email in both desktop and mobile formats before sending.
- Fix layout breakage now, because images and multi-column blocks are the most likely to mangle on small screens.
- Weigh the mobile share: the source cites roughly 58–60% of global internet traffic on mobile devices.
- Treat broken rendering as a direct CTR problem — the source says unprofessional-looking mobile layouts plummet click-through rates, with e-commerce most at risk because of heavy imagery.
- Consider that plain-text, image-free email sidesteps most mobile rendering risk entirely (see the plain-text card).
Caveat: The 58–60% mobile traffic figure is global internet traffic, not email opens specifically.
Caveat: Mobile preview tools vary by client and interface — verify in your current email platform.

Tags: email-lifecycle, mobile, email-format, product-page, conversion-optimization
Source: Learn Email Marketing in 39 Minutes.docx

---

## Confine links and CTAs to one per objective
Use when: Deciding how many links and buttons a store email should contain.
- Raise the link count deliberately: the source disagrees with the common 'one link only' rule and says one or two is safe.
- Require a clear reason for a reader to pick one link over another — each link should serve a different objective or audience.
- Avoid five or more links, which the source calls aggressive.
- Put a genuinely interesting nugget in the email and send readers to the full asset rather than pasting the whole blog post into the email.
- Treat clicks as training: each rewarded click makes the next click more likely, so build the habit deliberately over time.
- Keep the CTA contextual — the bridge into the link should follow from the email's specific content, not from a stock button pasted into every send.
Caveat: Click training only works if the destination is good; a weak linked asset degrades future click behavior.
Caveat: The one-link rule is a real practice elsewhere — this is presented as a situational alternative, not an absolute.

Tags: email-lifecycle, cta, copywriting, email-format, conversion-optimization
Source: Learn Email Marketing in 39 Minutes.docx

---

## Use annual renewal fees to lift revenue without touching the headline price
Use when: Pricing a subscription, membership or replenishment program in a store.
- Set the annual fee at about one to three months of the monthly price.
- Charge it only after the subscriber has stayed a year, so it never appears in the advertised entry price that drives signups.
- Reason about timing: someone who has already stayed twelve months is unlikely to leave over it.
- Estimate the impact: the source states the fee adds roughly 8–24% to revenue at no added cost, and on a 20% margin business that can roughly double profit.
- Example from the source: a $39/month plan with a $99 annual renewal moves annual revenue per customer from $468 to $567, a 21% increase and an effective $47/month.
- Keep advertised pricing unchanged because advertised price drives conversion.
Caveat: All figures are the source's illustrative math, not tested results across businesses.
Caveat: This works for recurring/recurring-charge models; it does not transfer to one-off product sales.
Caveat: Disclose the fee clearly in terms of service to avoid chargeback and trust damage.

Tags: email-lifecycle, pricing, subscriptions, retention, replenishment, offer-design
Source: Learn Email Marketing in 39 Minutes.docx

---

## Turn testimonials into hooks by asking for the worst moment
Use when: Sourcing customer testimonials for a store's PDP, ads or email content.
- Stop asking customers how life was before your product — that produces long stories with no usable hook.
- Instead ask one question: what was the worst moment?
- Expect a moment, not a summary; the specificity is what makes the hook powerful.
- Compare the source's own examples: 'two months away from shutting our doors', 'barely making enough to survive', and two separate testimonials that ended the month with $0 of profit — the detail, not the general struggle, is the value.
- Analyze which hooks win by reviewing many testimonials together (the source reviewed 2,500 and found the best shared a pain-based hook).
- Deploy the resulting line as the opening of an ad, the first line of an email, or the top of a review block.
Caveat: The 2,500-review finding is from Gym Launch testimonials in a coaching context; the transfer to a store's reviews is an adaptation.
Caveat: Pain-based hooks suit acquisition creative; testimonials used as reassurance on a PDP may need a different, outcome-focused framing.

Tags: email-lifecycle, customer-research, testimonials, creative-strategy, acquisition, product-page
Source: Learn Email Marketing in 39 Minutes.docx

---

## Give away a peeled-off bonus to make list membership worth something
Use when: Designing the incentive stack for a store's email opt-in.
- Identify work you already produced that is valuable but does not fit its main container — the source describes writing book chapters that did not flow with the book.
- Finish that material to full quality and reserve it as a subscriber-only gift.
- Make it platform-specific so there is a reason to be on the email list specifically, not just somewhere.
- Separate the recruitment message: sell regular communication first, then mention the free asset by the way.
- Back it with anticipation — tell subscribers a larger announcement is coming and they will hear it first.
- Verify the asset is genuinely good before gating it, because unsubscribing after a disappointing reward is the outcome the source says he worries about most.
Caveat: A weak lead magnet followed by nothing of ongoing value causes immediate unsubscribes or permanent dormancy.
Caveat: Exclusive-asset creation requires genuinely spare finished work; manufacturing filler defeats the purpose.

Tags: email-lifecycle, lead-magnet, opt-in, content-strategy, retention, welcome-sequence
Source: Learn Email Marketing in 39 Minutes.docx

---

## Prioritize fast follow-up over almost everything else
Use when: Deciding what to fix first in a store's lead handling and conversion process.
- Set up a system that calls or reaches a lead within about 60 seconds of opting in.
- Cite the source's basis: an HBR study he refers to showed an average 391% increase in sales, which he translates as roughly quadrupling.
- Run the prioritization test: if nothing else on the roadmap can quadruple sales, this should be the first priority.
- Reframe staffing as self-funding: the source argues you can afford the coverage out of the sales lift it produces.
- Treat it as simple to understand and hard to operate — the constraint is coverage and process, not the idea.
Caveat: The 391% is a study figure cited by the source, not a guaranteed outcome for your store.
Caveat: This applies to businesses with a sales follow-up step — direct-to-consumer self-serve checkouts may have no equivalent action.

Tags: email-lifecycle, lead-follow-up, conversion-optimization, measurement, acquisition
Source: Learn Email Marketing in 39 Minutes.docx

---

## Focus effort on CTR over open rate over time
Use when: Planning a store's monthly email mix and reviewing whether the program is trending up or down.
- Decide deliberately which sends are deposits (pure value, low ask) and which are withdrawals (a real conversion push).
- Avoid asking for the click with equal pressure in every send, since that erodes response over time.
- Deliver hidden high-value content behind links — the source cites Google Drive links to video sales letters and other gated assets as an effective pattern — to keep clicks rewarding.
- Watch the rolling metric rather than the single send; the source evaluates CTR across a period, not per email.
- Note the source's own orientation numbers as context only: about 8.5% CTR, which he interprets as roughly 8,500 clicks per 100,000 sends.
- Expect that training the audience to click is what governs future deliverability, since providers read engagement as quality.
Caveat: Google Drive link tactics are described by the source as a 2011-era advanced tactic — test whether it still behaves that way in current inbox environments.
Caveat: The 8.5% CTR is one sender's list, not a benchmark.

Tags: email-lifecycle, click-through-rate, measurement, conversion-optimization, deliverability, retention
Source: Learn Email Marketing in 39 Minutes.docx

---

## Use native-style links for deliverability
Use when: Choosing where a store's email link should point — sales page, video or gated document.
- Prefer links to mainstream properties the provider understands, such as a video platform link.
- For a sales letter or video sales letter, host the asset where the provider can identify the file type rather than on an unfamiliar domain.
- Test rough, duct-taped-looking assets too — the source says they sometimes convert better than polished destinations.
- Label this as a 2011-era tactic and verify current behavior before relying on it.
- Pair it with the broader principle: align with the provider's objective of delivering high-quality mail rather than looking for hacks.
Caveat: The source explicitly flags this as an old tactic, and provider routing behavior changes — verify before depending on it.
Caveat: Hosting sensitive assets on third-party storage may not suit branded or gated commercial offers.

Tags: email-lifecycle, deliverability, links, video, conversion-optimization
Source: Learn Email Marketing in 39 Minutes.docx

---

## Pre-flight: run audience + objection research before drafting any email copy
Use when: You are about to write a campaign, welcome flow or promo email and don't yet have written pain points, angles and objections for the product.
- Decide the product you're writing for and the country/demo you're targeting (the source uses the US as the biggest DTC market as an example) before touching any copy tool.
- In Facebook Ad Library, search the product category, filter by country, set ad category to 'All ads' and media type to 'Video' — the source argues video is more telling because only slightly bigger brands can run UGC video.
- Sort to find competitors running many ad variations (the source points to one running 85 versions vs. another with 5) — many variations suggests a working angle. Open the competitor's page > About > Page transparency > Ads to see the whole history.
- Open the product page and record the USPs, ingredients, bundle offers and claims the competitor is making.
- Start a plain Notion page as an idea dump (the source says no template is needed) and list product benefits, keywords, and the angle the competitor is leading with.
- Do this over multiple products and save findings. The source claims a few hours up front makes each email 10–20 minutes to write.
- The output is a single research doc you will pull banner angle, review selection, benefit copy and guarantee messaging from.
Caveat: The source's time estimates (few hours research, 10–20 minutes per email) are his own experience, not a benchmark.
Caveat: Filtering by only video ads skips image-based competitors that may also be performing.

Tags: email-lifecycle, customer-research, creative-strategy, facebook-ad-library, research, positioning
Source: Master Email Copywriting for E-commerce Brands.docx

---

## Mine Amazon reviews for pre-purchase objections, not praise
Use when: You are building objection-handling copy, review blocks or a guarantee for a consumable or problem-solution product.
- Go to the Amazon of the country you're targeting and search the product category plus adjacent categories (source example: sea moss and shilajit for a supplement brand).
- Pick products with a good volume of reviews, then filter to Most Recent — the source says top reviews are not always that useful.
- Scroll the negative and mixed reviews and list every practical complaint: difficult to scoop, air-dries, tastes bitter, hard to swallow, no energy increase, no noticeable change.
- Log category-level objections, not just one brand's: in the source example, lead content and lack of lab testing appear across shilajit products because they're sourced from different regions.
- Note positive reviews too — for sea moss the source found repeated 'easy to swallow / no bad taste' praise, showing taste is the category's buying barrier.
- Spend roughly 30–60 minutes per product category doing this, then decide how your product's process (e.g. purification method) answers each objection.
- Extend the same mining to Trustpilot, the Better Business Bureau, comment sections on the brand's and competitors' social posts, and podcast comment sections.
Caveat: The source doesn't trust reviews posted on the product page itself because they can be faked — prefer Amazon and third-party review sites.
Caveat: 30–60 minutes is the source's suggested minimum, not a validated threshold.
Caveat: Watch for regulated or medical claims when turning objections into copy.

Tags: email-lifecycle, customer-research, research, objection-handling, reviews, product-page
Source: Master Email Copywriting for E-commerce Brands.docx

---

## Pressure-test the market by searching Facebook Ad Library for problem keywords
Use when: You are deciding which angle or mechanism to lead with in acquisition emails or cold traffic and want evidence your framing is unsolved elsewhere.
- Type the problem phrase, not the product, into Facebook Ad Library (source example: 'hair loss').
- Look at the incumbent solutions that flood the results — in the source example, minoxidil ads.
- Note the objections people raise about those solutions: the source says minoxidil is effective but carries hormone influences and side effects.
- Position your product as the alternative the incumbent's customers are already looking for — in the source example, holistic or natural alternatives like sea moss or collagen.
- Turn that gap into the angle you lead acquisition emails with, then feed it into the banner block and the benefit highlight copy.
- Cross-check whether the complaint pattern also shows up in Amazon reviews of those incumbent products before committing to the angle.
Caveat: The minoxidil side-effect claim is the presenter's assertion about what people say in the market, not a verified medical statement — verify before using in copy.
Caveat: Ad Library interfaces and filters change; verify the current UI before instructing a team member.

Tags: email-lifecycle, creative-strategy, positioning, research, facebook-ad-library, acquisition, offer-design
Source: Master Email Copywriting for E-commerce Brands.docx

---

## Extrapolate benefits into underlying insecurities to write empathetic copy
Use when: You are writing longer-form benefit highlight copy or story blocks and the current draft reads generic or feature-led.
- List each product benefit plainly (source example: boosted energy, fat loss and muscle gain, thicker fuller hair, intense detoxification, improved skin).
- For each, write the immediate consequence (muscle gain leads to feeling and looking more confident).
- Then push one level deeper to the social or identity insecurity: not being able to approach people, nervousness in social settings, feeling inferior, seeing acne first every time you look in a mirror.
- Decide which benefits are 'perks' and which are true insecurity anchors — the source argues fat loss, muscle gain, hair loss and low testosterone carry much more emotional weight for men than energy or detox.
- Write benefit copy aimed at the insecurity, then resolve it with your product's mechanism (e.g. mineral deficiency, not personal failing).
- Keep the deep version to one benefit per email block; use icon-plus-short-label benefit rows when you need to show several at once.
- Keep the tone that of a friend trying to help, matching the short 100–300 word length of ecommerce emails rather than long-form advertorial.
Caveat: The source presents this as his own psychological extrapolation technique, not a researched model of buyer behaviour.
Caveat: Deeper insecurity angles can drift into regulated claims — the source notes he must imply rather than state them.

Tags: email-lifecycle, copywriting, customer-research, positioning, creative-strategy, benefit-highlights
Source: Master Email Copywriting for E-commerce Brands.docx

---

## Shift the blame outward to remove shame from the buying decision
Use when: You are writing problem-solution copy for a category where the customer may feel personally responsible for their problem (damaged hair, low energy, poor skin, low testosterone).
- Identify the behaviour the customer is privately blaming themselves for.
- Name the external cause instead: the source's example is telling women with damaged hair that chemical-laden hair dyes from large corporations ruined it, not their years of dyeing it.
- For a supplement brand the equivalent is framing symptoms as a biological deficiency rather than a personality flaw — e.g. nerves before approaching someone are a testosterone issue, not shyness.
- Present your product as the remedy that reverses damage which was not the customer's fault in the first place.
- Use this framing in the banner angle, benefit highlight copy and the objection-handling review you select, so the whole email is consistent.
- Keep it honest: the source frames this as ethical only when the external explanation is true, not as a manipulation tactic.
Caveat: The source explicitly calls this an ethical copy tactic — if the external blame is fabricated, the claim becomes deceptive.
Caveat: Avoid naming competitor brands or making unsubstantiated accusations about specific companies.

Tags: email-lifecycle, copywriting, positioning, offer-design, objection-handling, benefit-highlights
Source: Master Email Copywriting for E-commerce Brands.docx

---

## Build emails from modular blocks instead of writing long-form direct response
Use when: You are briefing a designer, creating Klaviyo templates, or training a junior writer on how to produce campaign and flow emails quickly.
- Write out the block list you'll use: banner, CTA, review, product display, benefit highlights, content or story, countdown timer, featured on, guarantee.
- Note which blocks carry real copy (story and benefit blocks) versus which are largely design (logo, footer, product display).
- For each email, pick only the blocks the email's goal needs — a launch email may be banner + countdown + product display + guarantee; a story email may be banner + long content block + review.
- Draft each block independently rather than writing a continuous letter, since ecommerce copy is short-form and design-led (the source puts typical emails at 100–300 words).
- Hand the block-level copy to the designer so they know what goes on each visual element.
- Build a reusable library of your own block designs so future emails are assembled rather than designed from scratch.
- Expect the copywriting itself to become fast — the source claims 10–20 minutes per email — once your research doc and block library exist.
Caveat: This is the presenter's own framework for ecommerce brands; it is not appropriate for long-form advertorial funnels.
Caveat: Design-tool specifics (the source demos Canva and mentions Figma as more professional) change over time — verify current capabilities.

Tags: email-lifecycle, copywriting, email-design, klaviyo, product-display, workflow
Source: Master Email Copywriting for E-commerce Brands.docx

---

## Write the banner block to state the email's purpose above the fold
Use when: You are drafting the top of a promotional, launch or flow email and want to maximise scroll-through to the rest of the message.
- Design and write for the mobile above-the-fold area only — the source compares the banner to opening a letter with 'I am writing to [purpose]'.
- Make it eye-catching and state the goal or offer of the email plainly.
- Optimise the aspect ratio for mobile phones so the key text isn't cropped halfway.
- Check the offer and CTA text are fully visible without scrolling.
- Expect roughly 9 out of 10 emails to have some form of banner — either a short strip or a longer one containing a CTA — so treat it as standard, not optional.
- Measure success by whether the reader reaches the next block of the email, since a cut-off or vague banner suppresses everything below it.
Caveat: The source's '9 out of 10 emails have a banner' is his own observation, not a study result.
Caveat: Banner rendering varies by inbox client; test in the clients your list actually uses.

Tags: email-lifecycle, copywriting, email-design, product-page, conversion-optimization, mobile
Source: Master Email Copywriting for E-commerce Brands.docx

---

## Keep CTA button copy to a single clear instruction
Use when: You are filling in button labels across a campaign, flow or template in your ESP.
- Write the action the reader is taking: Shop Now, Order Today, Learn More are the source's standard examples.
- Match the label to the intent of the email block above it — a countdown-driven offer email uses an order-oriented button, an education email uses a learn-more button.
- Keep it short enough to render on a mobile button without wrapping or truncating.
- Avoid loading the button with persuasion; the persuasion lives in the banner, benefit and review blocks.
Caveat: The source gives this minimal attention by design — treat this as the low-effort block, not a place to test elaborate copy unless you have reason to.

Tags: email-lifecycle, copywriting, email-design, conversion-optimization, checkout, cta
Source: Master Email Copywriting for E-commerce Brands.docx

---

## Select review blocks that answer a specific known objection
Use when: You are populating the social-proof block of an email or flow and want it to move undecided readers rather than decorate the email.
- Pull your research doc and list the top objections the audience has before buying.
- Match each review slot to one objection — for a sea moss/shilajit brand the source would pick one review about better hair and nails and one from a busy person whose energy improved without changing their lifestyle.
- Avoid reviews that only express general satisfaction, because the source argues they don't help the reader decide whether the product is for them.
- Pair reviews with UGC photos selectively: it can strengthen credibility, but the source warns against attaching a face to sensitive objections (his example is erectile dysfunction).
- Choose which objections are safe to pair with a face and which should stay anonymous, respecting the reviewer's privacy.
- Keep the review text short enough to sit in a mobile block.
Caveat: The privacy caution about matching faces to sensitive objections is the source's guidance, and he advises using UGC 'with caution' rather than as a rule.
Caveat: Do not assume a review that answers one objection answers the rest — one objection per review slot.

Tags: email-lifecycle, copywriting, reviews, objection-handling, customer-research, social-proof
Source: Master Email Copywriting for E-commerce Brands.docx

---

## Choose the product display layout before writing the copy
Use when: You are laying out a merchandising email that features one hero product or several SKUs.
- If the product needs descriptive copy alongside its image and CTA, use a row-by-row layout — the source uses this when copy accompanies the product.
- If you're showing several products with only an image and title, use a 2x2 grid, which fits a product image plus title without shrinking the text.
- Avoid wide grids like 3x2: the source warns products render too small on mobile for people to distinguish text.
- Envision the mobile rendering before writing the copy, because the column count determines how many words each product can carry.
- Write copy to the space the layout allows rather than the reverse.
Caveat: Grid thresholds are the source's design judgement, not a tested rule — verify against your own template's mobile rendering.
Caveat: The source demos in Canva for smaller brands and says Figma gives more professional output for larger teams.

Tags: email-lifecycle, copywriting, email-design, product-display, merchandising, mobile
Source: Master Email Copywriting for E-commerce Brands.docx

---

## Choose icon rows or longer copy for benefit highlights
Use when: You are writing the benefits section of an email and deciding how much persuasive copy to attach to each claim.
- For the icon route, write short benefit labels — the source's examples are boosted energy, fat loss and muscle gain, thicker fuller hair, intense detoxification — and attach custom icons that visually match each claim rather than a generic tick.
- For the long-copy route, focus on one benefit per block, open with the insecurity the benefit resolves, then resolve it with the product's mechanism (source example: acne is a mineral deficiency, and adding those minerals can help acne scars heal over time).
- Don't try to write deep emotional copy for perk-level benefits such as energy or detox; the source says you can't dive into insecurities with those angles.
- Match block choice to email length — icon rows for short promo emails, one long benefit block for story or education emails.
- Refine the first-draft sentence structure before shipping, since the source's own first-draft example is deliberately rough.
Caveat: The acne/mineral mechanism is the presenter's illustrative copy example, not a clinically established claim — do not reuse mechanisms you haven't verified for your own product.
Caveat: Keep regulated health claims out of benefit copy.

Tags: email-lifecycle, copywriting, email-design, benefit-highlights, objection-handling, creative-strategy
Source: Master Email Copywriting for E-commerce Brands.docx

---

## Use fact-only content and story blocks when you don't know copywriting tactics
Use when: You are a small brand owner writing an education, brand-story or ingredient email without a copywriter or an established voice-of-customer library.
- For a content block, state the fact plainly — the source's example is a study showing a 200mg dose of shilajit over two weeks raised average testosterone in the control group by 42% — and stop there.
- Support it with a simple chart if you can; the source says that alone constitutes the content block.
- For a story block, narrate facts in first person: the source's example is a founder seeing genetically receding hairlines in the family, learning prevention is the best cure, discovering micronutrient deficiencies, sourcing sea moss through relatives and shipping it through customs, then selling it after friends had results.
- Resist inserting copywriting frameworks — the source's point is that both examples sell on facts alone.
- Keep the block short enough to sit between a banner and a product display.
Caveat: Any study statistic you cite must be real and must actually support the claim for your product; the source's 42% figure is his own illustrative example, not a citable result.
Caveat: Verify the study before publishing, and check how the claim sits with advertising regulations in your market.

Tags: email-lifecycle, copywriting, content-strategy, brand-story, research, email-design
Source: Master Email Copywriting for E-commerce Brands.docx

---

## Use countdown timers to back an urgency claim
Use when: You are running a launch or sale email where an offer genuinely expires and you want urgency without writing more persuasive copy.
- Only deploy the timer when there is a real deadline — the source's example is a discount code expiring in 24 hours; the timer just substantiates the claim.
- Place it as its own block, typically near the offer or CTA.
- Use the tool the source recommends, countdownmail.com, which he describes as roughly $10/month with unlimited uses.
- Build a reusable countdown block in your ESP so future launches take minutes.
- Verify current pricing, ESP integrations and rendering behaviour of whichever countdown tool you choose before building it into a core template.
Caveat: A countdown attached to a deadline that resets or never actually expires damages trust; the source ties urgency to a genuine offer.
Caveat: Tool pricing and interfaces change — confirm before committing.

Tags: email-lifecycle, copywriting, urgency, email-design, promotion, tools
Source: Master Email Copywriting for E-commerce Brands.docx

---

## Feature logos as an authority block using 'as seen on' wording
Use when: You are adding a credibility layer to a welcome, launch or promotion email and have genuine press or media appearances to show.
- Use one of the two standard wordings: 'As seen on' or 'Featured on' — the source says that is all the copy needed.
- Lay out the logos of the outlets you've genuinely appeared in, for example Shark Tank or a relevant industry publication.
- Place it where it reinforces trust, typically after the banner or alongside the product display.
- Confirm you actually appeared in every logo you show — the source presents this purely as displaying real PR.
Caveat: The source treats this as a copy-light block, so don't expect it to carry the email; its job is trust reinforcement only.

Tags: email-lifecycle, copywriting, social-proof, email-design, authority, brand-trust
Source: Master Email Copywriting for E-commerce Brands.docx

---

## Reverse risk with a long unconditional guarantee — and expect fewer returns
Use when: You are deciding whether to add a guarantee block to acquisition or first-purchase emails and how long the window should be.
- Identify the two fears the guarantee addresses — being scammed, and the product not working for them, both described by the source as a fear of loss rather than a product objection.
- Offer an unconditional guarantee window and state it plainly in its own block on first-purchase and acquisition emails.
- Consider a long window such as 180 days over a short one such as 30 days: the source explains that with 30 days buyers hold themselves to the deadline and return, while with 180 days they procrastinate past the point of bothering and often forget entirely.
- If you're a bootstrapped brand worried about refund exposure, note the source's claim that guarantees barely move return or refund rates and that a longer window lowers them further on lower-ticket consumables.
- Repeat the guarantee in the flows most likely to be a customer's first purchase.
Caveat: This is the presenter's stated '180-day guarantee paradox' based on his own brand experience, not a published benchmark — test the window on your own refund data before adopting it.
Caveat: Check consumer-law requirements for guarantee and refund statements in your selling markets.
Caveat: A guarantee block doesn't replace answering objections — pair it with objection-handling reviews.

Tags: email-lifecycle, copywriting, guarantee, risk-reversal, offer-design, retention
Source: Master Email Copywriting for E-commerce Brands.docx

---

## Profile followers and ad comments to pin down who actually buys
Use when: You need a sharper customer profile for email segmentation, creative angles or list targeting and analytics only gives you aggregate age and gender.
- Open a competitor's Instagram and read comments on their latest posts for language and objections.
- Look at the top followers of a brand with a niche audience and open individual profiles — the source suggests checking roughly 50 to 75 to get a sense of the pattern.
- Record what recurs across those profiles: the source's example is seeing posts about motorbikes, fishing or holistic wellness and inferring that is the buyer's real interest set.
- Use Google Analytics and Facebook audience analytics for the baseline age range, gender and interest data if you have it, but treat the profile scan as the psychographic layer on top.
- Feed the findings back into the research doc alongside benefit and objection data.
- Use the profile to write the banner angle and select reviews for the email.
Caveat: This is observational inference, not statistically valid sampling — don't treat a 50–75 profile scan as audience research that stands alone.
Caveat: Review platform data-use terms before systematically scraping or viewing profiles.

Tags: email-lifecycle, customer-research, research, segmentation, creative-strategy, social-media
Source: Master Email Copywriting for E-commerce Brands.docx

---

## Test SMS/email send frequency with a holdout to prove incrementality
Use when: Deciding whether to increase lifecycle message cadence or justify a growing SMS bill to leadership.
- Split your subscriber base into three cohorts: hold steady at current cadence (for example 50%), send nothing at all (for example 25%), and send double the cadence (for example 25%).
- Run for a full cycle long enough to capture conversion behavior—Postscript's test moved brands from roughly one text per week to two.
- Compare revenue per subscriber across cohorts against the true holdout, not just platform-attributed revenue, to see incremental lift.
- If 2x shows a statistically significant revenue lift over holdout, raise cadence; if not, keep the baseline.
- Note that in the test described, more sending produced higher ROI with ~98% confidence the 2x group yielded significantly more revenue—treat this as one brand's result, not a universal benchmark.
Caveat: Every SMS has a real per-message cost, unlike email, so incremental revenue must clear the toll.
Caveat: Attribution tools report what happened; only a holdout shows what would have happened otherwise.

Tags: email-lifecycle, sms-marketing, incrementality, experiment-design, measurement, budget-allocation
Source: Rethinking SMS Marketing for Ecommerce_ AI, RCS & LTV.docx

---

## Set an SMS frequency baseline using subscriber LTV and unsub rate
Use when: Setting or revising monthly SMS cadence and worried about annoying the list.
- Track four metrics: % of list subscribing (acquisition rate), messages sent per subscriber per month, revenue per message, and unsubscribe rate.
- Watch unsubscribes inside the first 30 days as the key signal of over-messaging.
- Start near Postscript's observed sweet spot of roughly 8–10 texts per subscriber per month, which they report generates high returns with essentially zero impact on baseline unsub rate.
- Do not assume this is fixed—the correct baseline must be tested per brand by mapping the relationship between messages per subscriber, revenue, and unsub rate.
- Use the data, not gut fear of 'annoying people'—if frequency were a problem, it would surface in the unsub metric.
- Recognize real spread across brands: some large brands send ~2 texts/subscriber (e.g., a subscription-first model), while others (e.g., Grüns) send ~20+ in the first 30–45 days.
Caveat: 8–10/month is Postscript's observed range, not a guaranteed optimum for every store.
Caveat: High-frequency brands often accept higher spend for a specific goal such as converting to subscription; low-frequency brands may be filtering out long-term non-buyers to avoid fees.

Tags: email-lifecycle, sms-marketing, retention, measurement, list-management, frequency
Source: Rethinking SMS Marketing for Ecommerce_ AI, RCS & LTV.docx

---

## Treat SMS as an acquisition channel, not just retention
Use when: Allocating team ownership, budget, or optimization effort across paid acquisition and lifecycle channels.
- Recognize that the first action a Meta/Google click often triggers is the signup popup—so SMS/email pop-ups and welcome flows are part of the acquisition funnel.
- Track that roughly 25% of compliant double-opt-in subscribers buy within 30 days (Postscript's cross-brand figure); the remaining ~75% are unconverted subscribers whose first-purchase objections still need handling.
- Treat the pop-up → welcome series as your acquisition engine, distinct from campaigns that serve retention at day 15/30/45.
- Align org structure so one leader sees paid, creative, ecom, and retention—Postscript and operators report that siloed teams miss second-order effects (e.g., an ad change tanking SMS list growth).
- Test pop-up changes against full-site conversion rate, not just opt-in rate, because a pop-up can lift signups while hurting checkout.
- An operator predicts retention will become the next frontier as paid channels saturate—an opinion, not a guarantee.
Caveat: The 25% figure is an aggregate across Postscript's ~25,000 brands, not a target for your store.
Caveat: Centralizing teams is a recommendation from practitioners, not a proven universal structure.

Tags: email-lifecycle, sms-marketing, acquisition, list-growth, conversion-optimization, team-structure, pop-up
Source: Rethinking SMS Marketing for Ecommerce_ AI, RCS & LTV.docx

---

## Add a question to lifecycle flows to start conversations
Use when: Starting conversational commerce or sourcing zero-party data without new tooling.
- Pick any existing flow (welcome series, abandoned cart, delivery follow-up).
- After the standard link or message, append a plain question such as 'Is there anything else I can help you with today?' or 'Do you have any questions I can answer?'
- Test it: one operator split a 6-message welcome flow, with the variant ending in a question, and it performed well; keep the standard flow to convert the easy 25% then use the question to catch marginal prospects where conversation is required.
- Expect volume—operators report brands getting thousands of replies in the first week when they ask.
- Mine the replies for objection themes and use them to guide future flows and ad copy.
- Extend this to more touchpoints: post-delivery usage questions, winback, long-consideration prospects.
Caveat: For short-consideration, low-ticket impulse buys (e.g., a wallet before Father's Day), conversation at the end of the flow is sufficient—going conversation-first is overkill.
Caveat: For long-consideration or high-ticket categories (e.g., a $1,000 sofa with a ~90-day window), consider putting conversation earlier to compress the decision.

Tags: email-lifecycle, sms-marketing, conversational-commerce, abandoned-cart, welcome-series, customer-research, zero-party-data
Source: Rethinking SMS Marketing for Ecommerce_ AI, RCS & LTV.docx

---

## Match conversation strategy to consideration period and ticket size
Use when: Designing whether flows should lead with conversation or stay broadcast-first for a given product category.
- Identify your category's consideration period (time from click/opt-in to purchase).
- For short, impulse-driven buys, run a normal broadcast flow and reserve conversation for the end to handle stragglers.
- For long-consideration or high-ticket items, place conversation earlier—the source compares it to putting your best salesperson in front of a shopper while they compare you to competitors.
- For one-time-to-subscription conversion, which carries an outsized value bump, lean conversation-heavy to handle objections and upsell.
- Use winback and unconverted-senior-subscriber segments as conversation targets, since they've engaged with texts but never bought.
- Post-delivery, ask a follow-up question about product usage to open a dialogue at the best moment for repeat purchase.
Caveat: Consideration-period length is a judgment call per category; the source gives 90 days as an example for furniture, not a rule.

Tags: email-lifecycle, sms-marketing, conversational-commerce, lifecycle-flows, subscription, retention
Source: Rethinking SMS Marketing for Ecommerce_ AI, RCS & LTV.docx

---

## Use conversation data to build real zero-party customer attributes
Use when: Enriching subscriber profiles with personalization data and building one-to-one messaging.
- Instrument conversational replies so the content is queryable, not just answered in the moment.
- Separate static data (a purchase made a year ago, a SKU, a subscription tier) from ephemeral data that changes over time (a child ages from 1 to 2, seasonal location, a fitness or health change).
- Push attributes into your CRM/CDP so they can inform messaging beyond SMS—the source is building toward API/MCP access so personas like Claude can consume them (verify current availability).
- Build triggers around ephemeral attributes: a daughter's next birthday, a season change, a size change after a weight-loss journey.
- Treat this as the path to 'audience of one' personalization marketers have chased but lacked data to execute.
- Example of the kind of data conversations yield: a belt brand learned a wife buys for her husband, that he was on a health journey down 40 lbs, and that his size would keep changing—actionable but not obtainable from browsing data alone.
- Operators report subscribers who have a conversation with the brand show ~1.5x higher lifetime value—an internal metric, not a guarantee.
Caveat: Postscript's API/MCP access was in development at the recording—check current product docs.
Caveat: The 1.5x LTV lift is the vendor's observed metric; validate on your own list.

Tags: email-lifecycle, conversational-commerce, zero-party-data, personalization, segmentation, retention, cdp
Source: Rethinking SMS Marketing for Ecommerce_ AI, RCS & LTV.docx

---

## Use SMS/MMS/RCS as distinct channels and enable RCS for richer actions
Use when: Planning SMS creative formats and considering RCS rollouts for launches or drops.
- Understand RCS is not SMS/MMS—it's its own protocol; if a recipient can't receive RCS, messages fall back to SMS in tools like Postscript.
- Use RCS for rich formats: carousel scrolling, video, and native action buttons.
- For product drops, use the iOS calendar action button so recipients can add a launch date directly instead of a vague 'watch this space' text.
- Exploit native CTAs that integrate with the phone to expand use cases on the messaging channel.
- Operators report outsized performance on RCS over SMS/MMS—treat as early directional signal, not a benchmark.
- Confirm current carrier/device support and platform interface before committing budget, as RCS availability and features change.
Caveat: RCS performance claims are early-stage and vendor-reported.
Caveat: Feature availability (e.g., iOS calendar) varies by platform and time—verify in your messaging tool.

Tags: email-lifecycle, sms-marketing, rcs, creative-strategy, product-launch, new-channels
Source: Rethinking SMS Marketing for Ecommerce_ AI, RCS & LTV.docx

---

## Adapt to customer data through conversations
Use when: Diagnosing mid-funnel purchase blockers and reducing friction at PDP and checkout.
- Run ongoing conversations on your list to capture live objections people don't broadcast anywhere else.
- Look for objections that are too specific to design for: e.g., a shopper who would only buy 'Miracle Balm' if assured it holds up to a 5-hour-a-day gardening/sweating regimen, or a buyer whose cart total ($75) exceeded her budget ($68) and who needed a small offer to close.
- Use conversational tools to handle these at the moment of decision (the source's Shopper AI handles shade-matching and small price-gap offers automatically).
- Query conversation archives to surface trends and recurring blockers (the source's 'Ask Shopper' feature).
- Feed the discovered objections back into PDP copy, FAQ, and ad creative so future traffic self-serves.
- Treat conversation logs as arguably your richest consumer-insight stream, since many brands never text customers at all.
Caveat: The specific brand examples (Jones Road, belts) are illustrative, not benchmarks.
Caveat: Automated handling of price-gap offers requires merchant-defined guardrails—set them deliberately.

Tags: email-lifecycle, conversational-commerce, objection-handling, product-page, customer-research, conversion-optimization
Source: Rethinking SMS Marketing for Ecommerce_ AI, RCS & LTV.docx

---

## Chase incremental value in retention channels as paid channels saturate
Use when: Setting next-quarter growth priorities and allocating between paid acquisition and lifecycle optimization.
- Recognize that as paid opportunities are exhausted, marginal value moves into retention channels—the source quotes a CMO predicting retention would become the topic of focus after everybody exhausts paid incrementality.
- Shift toward precise optimization: for example, deciding whether 50K, 75K, or 100K of monthly SMS spend is most efficient at the margin, not just whether the current spend works.
- Scrutinize the SMS bill as a meaningful cost that lives between SaaS costs and performance marketing on the P&L—as it scales, so should the demand for incrementality evidence.
- Partner with a vendor or team willing to 'grade their own homework' with holdouts on large spend.
- Separate lead conversion (subscribing) from purchase conversion (buying) and from close rate—holdouts and cohort measurement track whether the channel produced net-new purchases.
Caveat: The CMO's retention prediction is a forecast, not a law.
Caveat: Retention-only isn't universal—brands with long consideration periods should still invest in top-of-funnel acquisition.

Tags: email-lifecycle, retention, incrementality, budget-allocation, measurement, sms-marketing, ltv
Source: Rethinking SMS Marketing for Ecommerce_ AI, RCS & LTV.docx

---

## Align pop-ups, flows, and campaigns to the true purchase decision
Use when: Deciding ownership and testing scope for pop-ups, welcome series, and campaigns.
- Treat the pop-up and welcome flow as part of the acquisition engine (ad → lander → pop-up → flow), because that chain is the first interaction with many paid visitors.
- Treat campaigns as a retention touchpoint where you speak to subscribers at day 15/30/45 with launches and first-party-data-driven messages.
- Ensure at least one leader sees both the flow and site behavior so signals aren't missed—e.g., an ad change lowering SMS list growth below forecast.
- Test pop-up experience against full-site conversion rate, not just opt-in rate, to catch changes that hurt checkout.
- Recognize the 'customer journey as a line' is misleading—people interact with all touchpoints in non-linear ways, so siloed assembly-line thinking invalidates decisions.
- Follow the source's 'just ask' rule: solicit conversations at the acquisition stage to intercept people who look like a converted customer but have a first-purchase objection.
Caveat: Full-site A/B testing of pop-ups requires sufficient traffic to detect conversion-rate impact.
Caveat: Org restructuring is contextual—not every store can centralize teams.

Tags: email-lifecycle, pop-up, welcome-series, conversion-optimization, acquisition, retention, experiment-design
Source: Rethinking SMS Marketing for Ecommerce_ AI, RCS & LTV.docx

---

## RCS vs SMS/MMS: what changes in the message
Use when: Deciding whether to pilot RCS for campaign sends or transactional/drop messaging, and scoping which message formats to build for it.
- Understand RCS as a separate protocol from SMS/MMS, not a formatting tweak: SMS is text-only, MMS adds an image, RCS supports carousels, scrolling, video and embedded web views inside the messaging thread. Where a recipient can't receive RCS, the message falls back to SMS, so keep an SMS-safe version of every send.
- Exploit native phone integrations for commerce use cases: action buttons can be programmed as any CTA, and calendar functionality lets a pre-launch drop message offer 'add to calendar' instead of 'watch this space' — replacing a reminder prompt with an actual saved event.
- Know that consumers are already trained on this interaction pattern (iMessage-style rich bubbles have existed for years), so richer messages don't require teaching the customer new behavior.
- Treat RCS as an early-adopter inbox-distinction play: the present lift partly comes from standing out versus SMS-only brands, and the source expects that advantage to diminish as adoption grows.
- Weigh the cost: RCS is somewhat more expensive than SMS because carriers take a cut, so a pilot should be judged on incremental performance, not just message-level cost.
Caveat: The source's claim of outsized RCS performance over SMS/MMS is a current observation from one provider and its brand base, not a benchmark; the source itself names carrier cost/performance as the main threat to the channel.
Caveat: RCS availability details vary and change quickly — verify current device and carrier coverage before planning a send.
Caveat: Live brand example mentioned: one brand switched to RCS with a holdout group running to measure incremental impact.

Tags: email-lifecycle, sms, rcs, creative-strategy, campaign-sends, measurement, retention, conversion-optimization
Source: Rethinking SMS Marketing for Ecommerce_ AI, RCS & LTV.docx

---

## Test RCS by holding out or running a clean flow
Use when: Launching or planning a first RCS campaign and needing to decide how to structure the test so results are trustworthy.
- Choose your measurement design up front. One option discussed: run a holdout so you can read the incremental impact of the new RCS experience versus the baseline SMS path. The other option: keep the RCS flow deliberately one-to-one and simple first, then test richer elements (carousels, cards) so the effect of each addition is cleaner.
- If you change flow and format at the same time, you can't attribute lift to RCS versus your new creative — separate the protocol change from the creative change where possible.
- Only after a clean baseline read should you layer richer formats: carousels for recommendations, web views for expanded browsing, action buttons for CTAs.
- Build the SMS fallback version of each RCS send so the holdout/control experience is a true comparison, not a broken message.
Caveat: The source only states this as an intended approach ('we'll probably go a little bit more one to one and then we'll test to get a cleaner read') — it is a plan, not a proven result.
Caveat: Early-adopter novelty effects can inflate RCS lift; expect the advantage to shrink as more brands adopt the channel.

Tags: email-lifecycle, sms, rcs, experiment-design, measurement, campaign-sends, conversion-optimization
Source: Rethinking SMS Marketing for Ecommerce_ AI, RCS & LTV.docx

---

## Conversational carousels for product recommendation
Use when: Merchandising and PDP/landing-page substitution inside SMS/RCS: when a customer asks for a recommendation and you need to move them to a purchase path in-thread.
- Treat the conversational recommendation as a replacement for sending bare links. Where the old flow produced a few links in reply to 'I'm buying for a guy who likes the outdoors — what do you recommend?', the richer flow returns a carousel of three items curated for that buyer type.
- Constrain the carousel to a small, opinionated set (the source uses three) so the customer makes a choice rather than browsing a catalog in a text thread.
- Lean on attached web view so the customer can expand into a native browser experience inside the messaging app — the whole browse-to-buy path stays in the thread.
- Use the carousel to serve best-seller logic for a persona/use-case rather than one generic product, and feed objection data from these conversations back into your other flows.
- Because the format relies on consumer familiarity with in-thread rich content, no new customer education is needed; the constraint is building the recommendation logic behind it.
Caveat: The recommendation-carousel capability is described as a future/planned application by the source, not a documented live result.
Caveat: Named brand (Ridge) is used illustratively — do not treat it as evidence of conversion lift.

Tags: email-lifecycle, sms, rcs, merchandising, product-recommendations, creative-strategy, conversion-optimization, retention
Source: Rethinking SMS Marketing for Ecommerce_ AI, RCS & LTV.docx

---

## List growth first: fix pop-up opt-in rate
Use when: Auditing SMS as an acquisition/growth channel and deciding where to spend first effort on list growth.
- Start with on-site opt-in. The source names it the fastest way to grow an SMS list, ahead of other capture methods, because it sits at the very top of your own-channel funnel and pays off in every future campaign.
- If you do nothing else, fix the pop-up acquisition rate first — treat it as the single most important list-growth lever before adding new flows or formats.
- Add fun/compelling content to the pop-up to lift opt-in rate; one brand explicitly says they had been under-optimizing pop-ups and are now doing it aggressively.
- Make this an owned-site-team responsibility: the source recommends having your site team drive the opt-in effort aggressively and watch that the metric trends up.
- Recognize the strategic logic: more numbers means more people you can text, and the source long considered list-growth capability the main differentiator between SMS providers (now shifting toward features like conversational commerce and RCS).
Caveat: The $5–10M annual revenue band is the source's own framing for who should prioritize this, not a universal threshold.
Caveat: The claim that on-site opt-in is 'the best' capture method is the source's opinion, stated alongside acknowledgement that other methods exist.

Tags: email-lifecycle, sms, list-growth, acquisition, conversion-optimization, pop-up, measurement
Source: Rethinking SMS Marketing for Ecommerce_ AI, RCS & LTV.docx

---

## Raise send cadence until unsubscribe rate ticks up
Use when: Setting campaign cadence for an established SMS program and deciding how many sends per week the list can absorb.
- Starting from your current cadence, add one more message per week (or one every two weeks if you send infrequently) as an increment, not a one-time jump.
- Measure the unsubscribe rate after each increment and keep pushing until you see the unsubscribe rate begin to tick up — that inflection is where you stop and reset the baseline.
- Do not treat the send-frequency question as separate from revenue: the point is to see how the added sends affect overall revenue from the channel, so track channel revenue alongside unsubscribes.
- Once you find the ceiling, hold that cadence as your new baseline rather than reverting to the old, more conservative one.
- Repeat the exercise periodically, since list composition and tolerance shift over time.
Caveat: This is the source's recommended operating heuristic, not a measured benchmark; the correct ceiling differs by list and offer.
Caveat: Pushing cadence without watching unsubscribe (and other list-health signals) can degrade the channel — the source explicitly uses unsub rate as the stop signal.

Tags: email-lifecycle, sms, campaign-cadence, retention, list-health, measurement, experiment-design
Source: Rethinking SMS Marketing for Ecommerce_ AI, RCS & LTV.docx

---

## Ask customers why they didn't buy to feed all flows
Use when: Running conversational SMS and using customer-research output to improve abandoned-cart, win-back, PDP and objection-handling flows.
- Start a conversational thread that asks questions rather than only pushing offers; the goal is to learn why people aren't purchasing, not solely to drive a sale in the thread.
- Capture the objection reasons as customer insight and route them into the team's decision-making as fast as possible — the source treats asking customers directly as the fastest way to get this data into the team's head.
- Apply the objections to your existing flows: if the recurring objection is shipping, sizing, price or trust, adjust the flow copy/offer that handles that stage.
- Use the same mechanism to feed conversational recommendation logic (e.g., carousels of best-sellers for a stated use case) once you know the buyer intents coming in.
- Run this before/alongside cadence expansion so you know what to say when you add sends.
Caveat: The source frames conversational questions as valuable mainly for objection insight and revenue; it does not supply benchmarks or expected response rates.
Caveat: If you use an AI 'shopper' assistant for conversational replies (the source's provider offers one), verify current capability and QA the answers before scaling.

Tags: email-lifecycle, sms, conversational-commerce, customer-research, retention, conversion-optimization, abandoned-cart, ai
Source: Rethinking SMS Marketing for Ecommerce_ AI, RCS & LTV.docx

---

## Capture experiment learnings causally so the model earns trust
Use when: Attributing and budgeting across SMS/email/paid channels where you need to know which sends add incremental revenue versus cannibalize.
- Run structured experiments — the source uses a platform for all experiments and geo-lift testing — rather than inferring incrementality from last-click channel revenue.
- Feed causal experiment results into your measurement mix model so the model is calibrated on tested lift; the source specifically values having experiments inform the MM ('causal MM') so it isn't a black box.
- Use the resulting incrementality read to set the channel roadmap and budget, not just to report on past performance.
- Apply the same framework to media mix and SMS sends so cadence and format decisions rest on observed lift rather than raw attributed revenue.
- Build the muscle to distinguish lead conversion, purchase conversion and lift in this context before acting on the numbers.
Caveat: This appears inside a sponsorship segment for a causal-MM vendor; treat the tool endorsement as promotional and evaluate measurement tools independently.
Caveat: Causal-MM methodology and availability change — verify current product behavior before relying on it.

Tags: email-lifecycle, measurement, incrementality, experiment-design, attribution, media-mix, geo-lift
Source: Rethinking SMS Marketing for Ecommerce_ AI, RCS & LTV.docx

---

## Tactical SMS starting order for a mid-size brand
Use when: Prioritizing the first 30–90 days of an SMS improvement program when the team is lean and everything feels urgent.
- Step 1 — List growth: maximize subscribers through the on-site opt-in/pop-up and fix its acquisition rate first; this is the top of your owned-channel funnel and pays off later.
- Step 2 — Cadence: add one send per interval and monitor unsubscribe rate, resetting your baseline at the point unsubs start rising; watch total channel revenue with it.
- Step 3 — Conversation: begin asking customers questions to learn objections and purchase intent, and route those insights into all your flows.
- Step 4 — Tooling/partner: if the team is lean and cannot execute the above, the source's own advice is to pick a hands-on platform that will push you toward the latest capabilities, accepting that this is the presenter's commercial pitch.
- Sequence matters: list size and opt-in rate bound what cadence and conversation can deliver, so don't start by adding formats if your capture is weak.
Caveat: The $5–10M band is the presenter's segmentation; smaller and larger brands may need a different order.
Caveat: Step 4 is a vendor recommendation from the vendor's own employee and should not be read as an independent assessment.

Tags: email-lifecycle, sms, prioritization, list-growth, campaign-cadence, conversational-commerce, acquisition, retention
Source: Rethinking SMS Marketing for Ecommerce_ AI, RCS & LTV.docx

---

## Checklist cadence: SMS/retention program for a growing brand
Use when: Running the day-to-day SMS/email lifecycle for a small ecom team and setting the review rhythm for list, cadence and messaging.
- Treat SMS/retention as small-team, high-frequency work: the source frames ecom as small teams doing big numbers where every hour matters and list, cadence and content are interconnected, so avoid optimizing one in isolation.
- Keep a standing check on three top-of-funnel metrics together: pop-up opt-in rate (list growth), unsubscribe rate (list health), and channel revenue (output).
- Change one lever at a time — a cadence increment or a format change — so you can tell what moved the unsubscribe rate.
- Feed conversational objections back into the flows on a regular loop so the talking points stay current with what customers actually say.
- Assign ownership: the source recommends the site team drive pop-up capture aggressively and watch the trend.
Caveat: This is a synthesis of the source's advice rather than a single prescribed process.
Caveat: Cadence and ceiling differ by list; no universal numeric target is established in the source.

Tags: email-lifecycle, sms, retention, operations, measurement, list-health, conversion-optimization
Source: Rethinking SMS Marketing for Ecommerce_ AI, RCS & LTV.docx

---

## Sizing the SMS channel for your store
Use when: Deciding whether to launch or resource an SMS channel, or benchmarking whether your current SMS program is underperforming relative to the channel's potential.
- Treat SMS as an owned retention channel like email: the list is not subject to ad auctions or algorithm changes, so revenue compounds month over month once built.
- Judge the channel on its sales-share contribution. The source's benchmark: done correctly, SMS should account for at least 5–15% of total brand sales. Treat this as the presenter's agency heuristic, not a computed industry figure.
- Compare channel cost to revenue: the source cites several client accounts spending less than $1,000/month on SMS to generate tens of thousands per month. Case-study result, not a promise.
- Check a simple list-size math argument before investing: going from 5,000 to 10,000 subscribers on identical campaigns does not double orders (diminishing returns) — the source's illustrative example is roughly 100 orders becoming 160–180, not 200. Growth still compounds, so not growing caps your ceiling.
- Audit which capabilities you already have in email before layering SMS, since most SMS revenue comes from omni-channel flows shared with email.
Caveat: 5–15% of sales and the sub-$1,000-bill examples come from the presenter's agency clients; your category, list quality and offer mix will differ.
Caveat: Diminishing returns are real: more subscribers from unqualified traffic dilutes performance.

Tags: email-lifecycle, sms-marketing, channel-strategy, retention, measurement, list-growth
Source: The Only Ecommerce SMS Marketing Video You'll Ever Need.docx

---

## Choose and configure an SMS platform for Shopify-style ecommerce
Use when: Setting up an SMS sending account for the first time, or migrating existing SMS subscribers into a platform that also holds your email.
- Choose a platform: the source names Klaviyo, Attentive and Postscript and says all three send essentially the same simple texts, so you cannot go badly wrong. It prefers Klaviyo so email and SMS flows live under one flow view rather than splitting email in Klaviyo and SMS in Attentive/Postscript.
- In platform settings, start SMS setup, pick your sending country, and verify a toll-free number. Note the source's caution: Canadian numbers can cost two SMS credits instead of one.
- Upload your existing SMS subscriber list from CSV or other file so previously collected consent carries over.
- Create the signup form — the platform states you need a form to keep collecting SMS subscribers; also keep an email pop-up active.
- Set opt-out language to whatever you prefer (e.g. 'unsub') under message add-ons.
- In sender preferences, decide on smart sending: when on, a subscriber will not receive more than one SMS campaign within a 24-hour window. Toggle per your cadence.
- Leave SMS quiet hours on default — it blocks delivery during the restricted hours rather than sending.
- Set keyword responses (e.g. texting JOIN to your number adds the person to the list and can trigger a discount), plus short links and terms. Verify the current interface, since menus change.
Caveat: Platform UIs and pricing change; verify current setup screens, credit costs and quiet-hour defaults before relying on this walkthrough.
Caveat: Country-specific costs and rules differ — the source only demonstrates a US setup.

Tags: email-lifecycle, sms-marketing, klaviyo, platform-setup, compliance, list-growth
Source: The Only Ecommerce SMS Marketing Video You'll Ever Need.docx

---

## Two-step pop-up to convert email visitors into SMS subscribers
Use when: Building or redesigning an onsite pop-up whose goal is to grow an SMS list from traffic you are already paying for.
- Do not put many fields on one pop-up. Avoid asking for first name, last name, occupation, location and phone all at once; each extra field is a hurdle that suppresses opt-in.
- Make the pop-up two steps: an email step first, then an SMS step. Smaller sequential hurdles convert better than one large ask.
- Decide the offer architecture. Many brands offer less for email and a bonus for SMS (e.g. 15% email, extra 5% SMS). The source disagrees: it prefers giving the best offer up front to email, because you get far more email opt-ins, then re-words the SMS step to capture SMS subscribers anyway. Test both if you are unsure.
- Use the source's tested SMS step copy: 'finish signing up with text to activate 20% off' — i.e. tell the visitor the SMS step is what activates the discount they already saw, rather than dangling a new incentive.
- Time the pop-up. The source's recommended delay is 6 to 10 seconds after page load — enough for the visitor to engage with the page before being interrupted.
- Track opt-in rate separately for the email step and the SMS step so you can tell which step is losing people.
Caveat: 'Finish signing up with text to activate 20% off' is the source's tested wording across its accounts, not a universal guarantee; validate on your own traffic.
Caveat: Whether the best offer goes up front or is split between email and SMS is contested — the source presents its preference against the common alternative, not a proven rule.

Tags: email-lifecycle, sms-marketing, list-growth, pop-up, conversion-optimization, offer-design
Source: The Only Ecommerce SMS Marketing Video You'll Ever Need.docx

---

## Other SMS list-growth levers beyond the pop-up
Use when: Planning next quarter's SMS subscriber acquisition when pop-up opt-ins alone are not adding enough subscribers.
- Make the onsite pop-up your primary method — the source calls it by far the number one way it grows client SMS lists.
- Add keyword opt-ins: configure a JOIN-style keyword so people who text it join the list and can claim a discount. Promote the keyword offsite where phone-first audiences are.
- Use the flow-generated opt-in surface: your existing SMS flows and signup forms are additional points where consent is captured, so make sure forms are live on the site rather than only in the platform.
- Only count qualified buyers as valuable subscribers. The source is explicit that the larger the list of actual buyers, the larger the impact; bought or unqualified numbers add cost and unsubscribes without proportional orders.
- Accept diminishing returns in your forecasting: doubling the list does not double orders on identical campaigns, but still increases order volume. Model the channel on incremental lift, not a linear multiple.
- Review weekly whether opt-ins are trending with traffic — a flat list with growing traffic means the capture surfaces are failing.
Caveat: The source says growth specifics are 'a whole other video' — treat this as a list of levers to prioritize, not complete build instructions.
Caveat: Keyword-based opt-in rules and required confirmation language vary by jurisdiction; verify compliance with your SMS platform and counsel.

Tags: email-lifecycle, sms-marketing, list-growth, acquisition, lead-capture, retention
Source: The Only Ecommerce SMS Marketing Video You'll Ever Need.docx

---

## Write SMS campaigns that only say things worth interrupting for
Use when: Drafting the SMS slot in your campaign calendar, or reviewing a flat-performing SMS calendar that is heavy on general brand messaging.
- Cut broad, general and vague campaigns. In a short text there is not enough room to build curiosity, so a non-specific message fails to capture attention.
- Anchor each campaign to a clear intention with an obvious click reason: sale, early access, restock/back-in-stock alert, new product launch.
- Keep the message within the 160-character limit; going over splits the message into multiple parts and you are billed for more than one SMS.
- Avoid MMS (image) messages unless the image is essential: the source notes images cost substantially more than a standard text. Compare marginal revenue against marginal send cost before defaulting to MMS.
- Test SMS concepts against your email calendar — many campaigns are stronger as an email plus a spaced SMS reminder about the same event than as two independent messages.
Caveat: 160-character single-message billing and MMS costing are platform/carrier-specific; confirm current pricing in your SMS provider.
Caveat: The source's direct-intent list reflects its own accounts and does not rule out well-executed brand campaigns — it warns that vague content is the main failure mode.

Tags: email-lifecycle, sms-marketing, campaign-strategy, copywriting, creative-strategy, cost-control
Source: The Only Ecommerce SMS Marketing Video You'll Ever Need.docx

---

## Set SMS sending frequency: one to two campaigns per week, never more
Use when: Deciding how many SMS campaign sends per week to schedule, or diagnosing an unsubscribe rate climbing above 1%.
- Start at roughly one SMS campaign per week. The source says this is the sweet spot it has personally found with clients.
- If the brand is pushing over 8 figures annually, you may experiment with two campaigns per week. Anything more than two is likely overkill and produces higher unsubscribe rates with diminishing returns.
- Set an unsubscribe-rate tripwire: above 1% means slow down your sending. Below 1% is normal; below 0.5% is excellent.
- Adjust frequency by purchase cadence. Apparel can be bought roughly once a quarter, so more contact is tolerable; a furniture brand bought once every 18 months will not convert from a casual SMS, so pushing the same cadence will burn the list. Split test within your category.
- Treat SMS as an intimate, personal channel: every send to a phone number is an intrusion, so only send when there is something concrete worth the interruption.
Caveat: One to two per week is a source-specific heuristic from an agency's client base, not a calculated optimal derived from data; the source explicitly says to split test and that the number is industry-specific.
Caveat: The 'over 8 figures annually' threshold is the presenter's rule of thumb.

Tags: email-lifecycle, sms-marketing, campaign-strategy, retention, list-hygiene, measurement
Source: The Only Ecommerce SMS Marketing Video You'll Ever Need.docx

---

## Build a calendar from retail events, not nurture filler
Use when: Laying out next month's SMS campaign calendar for a fashion or seasonal ecommerce brand.
- Start with the fixed calendar: slot the big sale events first (the source's example uses Memorial Day, which got multiple sends rather than one).
- Give major sales more than one send: e.g. a sale-start SMS on the Friday, an SMS on the actual holiday, and a VIP/subscriber early-access SMS on the Thursday before. Multiple sends on one event are a deliberate lever, not waste.
- Add seasonal relevance: back-in-stock for returning items, introducing the season's collection, and a mid-season clearance send highlighting the sale section (source example: up to 50% off).
- Layer gifting holidays that match the audience (e.g. Mother's Day for a women's fashion list).
- Add a product-focus send spotlighting the hero product from the new collection, and an occasional one-day or weekend flash sale on a specific collection or few products.
- Leave room for one brand/community-focused send with a call to action that is not purely transactional.
- Keep the monthly count at one to two per week even when the calendar looks full, then split test whether raising frequency on a big event beats adding a new event.
Caveat: The source populated about two SMS messages per week in its May example and immediately said your brand does not need to do that — it is an illustration, not a target.
Caveat: Campaign-type effectiveness varies by category and purchase cycle; the source says to split test rather than copy the calendar.

Tags: email-lifecycle, sms-marketing, campaign-strategy, calendar-planning, merchandising, promotions
Source: The Only Ecommerce SMS Marketing Video You'll Ever Need.docx

---

## Schedule SMS outside quiet hours and coordinate email timing
Use when: Choosing send times for SMS campaigns and pairing them with the day's email send.
- Apply current regional and recipient-local quiet-hour settings before scheduling; do not rely on one universal time band.
- Target the late morning to early afternoon window. The source's found sweet spot is roughly 11:00 a.m. to 3:00 p.m., when people are on lunch or on a break.
- Test a deliberate interval between related email and SMS messages; the source suggests about five to six hours as a starting hypothesis.
- Use the pairing deliberately for launches and offers: the customer sees the email in the morning and the SMS in the afternoon, giving the same message a second chance on a second device.
- Check how the current platform skips or defers each message type at quiet hours and whether a delayed offer will still be valid.
Caveat: The source late-morning preference is anecdotal; timing depends on recipients and current platform controls. https://help.klaviyo.com/hc/en-us/articles/4408737146651

Tags: email-lifecycle, sms-marketing, compliance, send-time-optimization, campaign-strategy, email-sms-coordination
Source: The Only Ecommerce SMS Marketing Video You'll Ever Need.docx

---

## Run SMS as a single-message omni-channel flow
Use when: Building the abandoned-cart, browse-abandonment and welcome automations for a store, or auditing whether existing SMS flows are compliant.
- Set up the three flows the source says drive the majority of revenue: welcome, abandoned cart, and browse abandonment.
- Respect the one-message rule: for most flows you may only send a single SMS message, because additional messages are non-compliant. The abandoned-cart flow, for example, should have exactly one SMS.
- Use the welcome-flow exception: you may have two SMS messages in the welcome flow. The source suggests the second goes out 2–3 days after the first, e.g. 'your 10% off is waiting' pointing to bestsellers.
- Write the welcome message plainly: thank them for signing up, deliver the first-purchase discount code (source example: 10% off), and tell them to go shop.
- Build the flows as omni-channel — SMS and email blended in the same automation — so email carries the longer content and SMS carries the short reminder. Klaviyo is preferred precisely because both appear under one flow.
- Rely on the timing advantage: an abandoned cart SMS firing a couple of hours after the abandonment reaches the customer while intent is still high, and may reach someone who is on their phone but not checking email that day.
- Plan for maintenance: the source says you get about 90% of the work done up front, then you split test, optimize and refresh periodically — do not literally set and forget.
- Add a conversion incentive inside abandonment flows if margins allow; the source says customers receiving an extra incentive in the flow are more likely to convert.
Caveat: The one-message-per-flow compliance rule and the two-message welcome exception are the source's stated understanding of SMS regulation; confirm current carrier and legal requirements before scaling.
Caveat: The source cites a client generating over $100,000 per month from one SMS flow — a case study, not an expected result.
Caveat: Extra abandonment incentives train customers to abandon; the source presents the tactic without addressing that risk.

Tags: email-lifecycle, sms-marketing, automation-flows, abandoned-cart, browse-abandonment, welcome-flow, compliance
Source: The Only Ecommerce SMS Marketing Video You'll Ever Need.docx

---

## Measure SMS on clicks, unsubscribes and delivery — not open rates
Use when: Reporting on SMS campaign performance, or setting up the dashboard and review cadence for the SMS channel.
- Ignore SMS open rates. The source calls them a vanity metric; click rate is the true read on engagement.
- Target click rate of at least 5%, up to about 15%.
- Keep unsubscribe rate below 1%; the source calls below 0.5% excellent. Above 1% means you are sending too much.
- Keep delivery rate above 90% (good) and above 95% (excellent).
- Diagnose and fix: for low click rates, tighten the engaged segment you send to and make the campaigns more direct. For high unsubscribe rates, send fewer messages, send to a more tightly engaged segment, and drop any informational/non-sales campaign. For low revenue per SMS, switch up the types of campaigns you send.
- Review Cadence: check the platform about once a day for how the day's campaign is doing; weekly, review trends, line up the week's campaigns and inspect flows; monthly, compare performance to prior months and choose one or two structural changes (e.g. send two campaigns for the next big sale instead of one) to test.
Caveat: During list growth, expect the unsubscribe rate to run higher simply because new subscribers are less engaged — the source notes this and does not treat early unsubscribes as a failure.
Caveat: The 5–15% click and sub-1% unsubscribe bands are the source's recommended targets, not guaranteed results for every category.

Tags: email-lifecycle, sms-marketing, measurement, kpis, retention, reporting-cadence
Source: The Only Ecommerce SMS Marketing Video You'll Ever Need.docx

---

## Avoid wasting budget through non-compliance and message-length errors
Use when: Auditing SMS list segments and send rules before a campaign, or onboarding a new SMS platform to reduce avoidable spend and legal risk.
- Segment only explicit SMS opt-ins. Unlike email, you cannot send SMS marketing to anyone who has not explicitly opted in — build the audience filter carefully and exclude ambiguous consent.
- Keep most automated flows to one SMS message; the welcome flow is the only exception allowing two.
- Enable quiet hours so no message is delivered before 8:00 a.m. or after 9:00 p.m.
- Keep messages within 160 characters to avoid being billed for multiple message parts.
- Default to standard SMS rather than MMS — images cost substantially more — and only choose MMS when the creative is essential to the offer.
- Be aware of country-level credit costs (the source notes Canadian numbers may cost two credits versus one) when budgeting sends.
Caveat: These rules are the source's stated compliance guidance and vary by jurisdiction and platform; verify with your SMS provider and legal counsel.
Caveat: Explicit opt-in requirements mean purchased or scraped phone lists cannot be used for marketing.

Tags: email-lifecycle, sms-marketing, compliance, list-hygiene, cost-control, deliverability
Source: The Only Ecommerce SMS Marketing Video You'll Ever Need.docx

---

## Klaviyo (or similar ESP) account setup essentials for a new store
Use when: Launching or migrating the store's email lifecycle platform (Klaviyo or similar) and deciding which technical settings must exist before the first campaign or flow sends.
- Create the account and connect the store so purchase and browse events flow in automatically (the source connects a Shopify store URL during onboarding).
- Choose the sending software against these criteria: easy setup and support, strong signup-form builder, strong flow builder, strong campaign builder, good email editor, data/segmentation capability, and built-in A/B testing. The source names Klaviyo (industry leader on technical setup, forms, flows, campaigns, segmentation, testing) and SendLane (newer, praised support) as the two it would pick; verify current pricing and feature sets before deciding.
- Decide single vs double opt-in. Double opt-in requires a confirmation click before subscribing: higher list quality, fewer subscribers because many never open the confirmation email. The source's preference is single opt-in, relying on engagement segmentation to suppress non-openers later.
- Set up a branded/dedicated sending domain by adding the provided NS records and TXT record at your DNS provider (e.g. GoDaddy, Google Domains/Squarespace) so mail appears to come from your brand.
- Add a DMARC TXT record at the root host; start with policy p=none (reporting only) with an aggregate-report address you control, then move to quarantine/reject once reports look clean. Use a DMARC record generator if needed, and use a separate inbox for reports.
- Turn on smart sending (the source uses a ~16-hour window) so a contact does not receive another email within that window; adjust to your cadence.
- Set attribution: last-interacted email within 5 days, and tick the option excluding Apple privacy opens so inflated opens don't earn revenue credit. SMS attribution defaults to 1 day.
- Enable anonymous visitor tracking so pre-identification browsing is backfilled onto the profile once identified.
- Set up brand assets (logo, colors, fonts from Google/Adobe with a web-safe fallback), design the preference/subscribe/unsubscribe pages in brand style, and turn on automatic UTM parameters for links.
- Verify the domain shows as active before sending; propagation takes time.
Caveat: Sending without a branded sending domain and DMARC risks filtering under Gmail/Yahoo 2024 inbox standards.
Caveat: UI paths and setting names change; verify inside the current interface.
Caveat: Attribution windows and smart-sending windows are conventions, not universal rules.

Tags: email-lifecycle, deliverability, dmarc, klaviyo, account-setup, measurement, attribution
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Rate signup forms against a 2–4% baseline and target 8–12%
Use when: Benchmarking the store's email capture rate and deciding whether the popup needs a rebuild to hit list-growth targets.
- Pull your current subscriber conversion rate (new subscribers divided by site sessions) for the same period.
- If you are near 2–4% of visitors, treat the form as underperforming; the source's high-converting target is roughly 8–12% of traffic entering the list.
- Do not rely on a footer signup form alone — the source's testing repeatedly shows popups outperform other form types despite bounce-rate objections.
- Rebuild toward the high-converting pattern: strong offer in the headline, single email field, prominent CTA button, secondary 'no thanks' option, and separate mobile and desktop forms.
- Track list growth and form submit rate weekly so improvements are visible and not assumed.
Caveat: 2–4% and 8–12% are the source's observed ranges, not guarantees; your traffic mix, price point and brand strength shift the achievable rate.
Caveat: Very broad or very narrow display rules can hit a high submit rate while total signups stay low — always pair submit rate with total subscribers.

Tags: email-lifecycle, list-growth, signup-form, conversion-optimization, measurement, popup
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Build a high-converting popup: offer, headline, single field, big CTA
Use when: Designing or redesigning the email capture popup for the storefront.
- Pick the incentive first — form success hinges on the offer more than on design. Research from the source's client work: for AOV around $200, $20 off often beats 10% off because '$20' reads larger than '10%'; anything below roughly 10% off is usually too weak unless your AOV is very high. Alternatives: BOGO, BOGO at 50%, free gift with purchase, free digital product, free shipping, cash back, early access (strong at Black Friday), mystery discount.
- Write the headline around the offer, e.g. 'Unlock 10% off your first order' — avoid 'sign up'/'subscribe' language and never bury the offer in body copy.
- Use one field: email. Ask for phone, name or preferences only in a second step after the email is captured.
- Set placeholder to something explicit like 'Enter your email here' and give the input field a contrasting fill (e.g. light grey) so it is obviously an input.
- Make the CTA large (the source uses ~70px height vs the ~54px default) and contrasting; note bigger buttons correlate with higher conversion, but not absurdly large.
- Give a de-emphasized second choice, e.g. 'No thanks, I'd rather pay full price' — two options (one attractive, one unattractive) lift signups versus one button.
- Keep the legal microcopy only where required (GDPR/EU); the source removes it for US stores.
- Compress all images (e.g. tinyPNG) since faster loading correlates with more conversions; add alt text to every image.
- Consider hiding the X: the source resizes it to minimum and matches its color to the background, since a visible second exit reduces signups — this is ethically debatable, and a 'no thanks' button already exists.
Caveat: The source's claims about hiding the X and about button size are practitioner observations, not universal benchmarks.
Caveat: Offer preference (e.g. % vs $ at the same AOV) should still be tested in your store.

Tags: email-lifecycle, signup-form, conversion-optimization, offer-design, creative-strategy, popup
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Timing and display rules for capture popups
Use when: Configuring when the store's popup appears so it captures engaged visitors without annoying first-timers.
- Never display immediately on page load; the source calls it a conversion killer because the visitor doesn't know the brand yet.
- Choose rule-based display: time delay, scroll depth, exit intent, or a combination.
- For desktop, use exit intent plus a time delay plus a scroll threshold; the source uses ~6 seconds and ~60% scroll, saying 4–10 seconds and 40–80% scroll are viable and should be split tested.
- Leave the OR toggle on (only all conditions met = AND). With OR, the form shows on exit OR after the delay OR after the scroll — a wider audience; the source never uses AND because it targets far too few people.
- Set reappearance frequency: default 5 days, the source often uses 3, and tick 'don't show again if submitted or if the go-to-URL button was clicked'.
- Target only non-subscribers ('don't show to existing profiles') so current subscribers aren't re-prompted.
- Exclude URLs such as cart/checkout, /wholesale and landing pages you're running paid traffic to, so you don't discount a visitor who is already about to buy.
- Optionally include/exclude visitor locations based on shipping coverage.
- Use a separate display setup for a list you already own: e.g. show an SMS-only signup form to existing email subscribers.
Caveat: Earlier display = more total signups but lower submit rate; later display = higher submit rate but a smaller exposed audience. Both metrics must be read together.
Caveat: Frequency, delay and scroll settings are brand-dependent; the source insists they be tested.

Tags: email-lifecycle, signup-form, conversion-optimization, popup, segmentation, experiment-design
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Always build separate mobile and desktop popups
Use when: Finishing the capture popup build and preparing it for mobile traffic, which is most of an ecommerce store's visitors.
- Clone the desktop form and rename it explicitly (e.g. 'mobile' / 'desktop').
- Set device targeting to mobile only on the clone, then adjust timing rules — drop exit intent on mobile because it is unreliable and annoying there.
- Increase input field and CTA size for thumbs: the source sets input text ~20px, input height ~70px, CTA height ~80px and CTA/microcopy text ~20–24px, versus smaller desktop values.
- Add extra padding above the CTA and between elements so users don't mistap.
- Skip the side image on mobile (no room); keep the layout vertical.
- Rework the teaser shape for small screens (e.g. rectangle to circle or corner tab) and shrink the text to fit.
- Enlarge success-page text (the source uses ~22–24px) so the confirmation is readable on a phone.
- Check the teaser placement against other on-site widgets (chatbot, loyalty promo, load-time banners) so nothing overlaps.
Caveat: Sizes in the source are examples from one build, not fixed specs; adjust to your brand and test.
Caveat: The two-form approach doubles maintenance — apply the same edits to both when you change an offer.

Tags: email-lifecycle, signup-form, mobile-optimization, conversion-optimization, popup, creative-strategy
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Withhold the discount code from the success page
Use when: Designing the popup success page and the first welcome email after email capture.
- Do not print the discount code on the success page — the source argues it removes any reason to open the first welcome email, which tanks the open rate, which in turn harms sending reputation and the whole email system.
- Replace it with a headline like 'Your discount is on its way — check your inbox for your confirmation and code'.
- Add a fallback line: didn't receive it within 5 minutes, check spam — new subscribers on Gmail are especially likely to land in spam, and this line reduces support tickets.
- Style that spam note in bold so it stands out.
- Match the success page visually to the opt-in (same logo, image, colors).
- Deliver the actual code inside the first welcome-series email, training recipients to open your mail over time.
Caveat: This delays the shopper's purchase by one email-open step; some brands may decide the immediate-purchase tradeoff is worth testing.
Caveat: The source states this as a strong preference for the email system's health, not a tested universal result.

Tags: email-lifecycle, signup-form, welcome-flow, deliverability, conversion-optimization, retention
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Teaser tab: keep the capture offer permanently reachable
Use when: Adding a persistent capture element to the storefront after a visitor dismisses the popup.
- Pick a shape (rectangle, circle, corner tab) and position it so it does not collide with your chatbot, loyalty widget or promo bar — check the live site on both devices.
- Write short benefit text such as 'Save 10% now' and make it bold.
- Choose when it shows: before the form, after the form is closed, or before and after (the source uses before and after).
- Give it a high-contrast background relative to the site (e.g. black tab with white text) and raise transparency to zero.
- On mobile, switch to a smaller circle or corner shape so it doesn't cover content.
- Test the placement against your actual pages, since overlapping on-site elements are a common failure.
Caveat: A permanently visible tab can feel pushy on content-heavy pages; still A/B test whether it lifts total signups.
Caveat: Positioning must be rechecked whenever you change your theme or add third-party widgets.

Tags: email-lifecycle, signup-form, conversion-optimization, creative-strategy, popup, merchandising
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Ten signup-form mistakes to audit before scaling list growth
Use when: Auditing an existing store popup that gets traffic but converts poorly.
- 1. Weak offer: the offer, not the design, drives signup; anything under ~10% off is generally ineffective unless AOV is very high.
- 2. Asking too much in step one: email only in the first step; move phone/name to a later step.
- 3. Wrong time delay: too short disrupts the visit and converts poorly; too long means few visitors ever see it — the source's range is roughly 4–10 seconds (up to 12).
- 4. Form too small: bigger forms get noticed; the source even suggests trying a full-page form as a test.
- 5. Too much copy: one headline, one field, one CTA button, microcopy — no paragraphs about exclusive offers.
- 6. Offer hidden in body copy: put the offer in the headline, largest and clearest.
- 7. Using 'sign up'/'subscribe' wording — people avoid those words.
- 8. One form for mobile and desktop.
- 9. Slow-loading images — compress with tinyPNG or similar.
- 10. Discount code given on the success page instead of in the welcome email.
Caveat: These are the source's practitioner observations from client work, not controlled benchmarks.
Caveat: Fixes 1, 3, 5 and 6 interact — changing only one may not move the submit rate.

Tags: email-lifecycle, signup-form, conversion-optimization, audit, popup, offer-design
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## A/B test the offer holistically, not by signup rate alone
Use when: Deciding which popup incentive (percentage off, dollar off, BOGO, gift, free shipping, mystery discount) the store should run.
- List candidate offers to test: percentage off, dollar amount off, dollar amount off above a threshold, free shipping, BOGO, BOGO at 50%, free gift with purchase, free digital product, subscription incentive, cash back, early access (strong at Black Friday), mystery discount (the discount is revealed only in the first welcome email; the source reports strong submit rates with this).
- Run each offer against a control form and let enough traffic accumulate to compare.
- Do not judge on form submit rate alone: the source reports a client case where a new offer had a lower welcome-flow placed-order rate but a much higher AOV and higher attributed welcome-flow revenue, so total revenue was higher.
- Track per-variant: form submit rate, welcome-flow placed-order rate, welcome-flow AOV, and attributed welcome-flow revenue.
- Choose the offer that wins on revenue, and if an offer is a good fit for a specific segment (e.g. early access for VIPs), route it accordingly.
Caveat: Offer outcomes are store- and price-point-specific; the client result is an example, not a promise.
Caveat: Testing many offers simultaneously fragments traffic and delays significance.

Tags: email-lifecycle, offer-design, experiment-design, welcome-flow, measurement, signup-form
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Add a micro-yes step before the email field
Use when: Optimizing the capture popup's form structure with an extra qualifying step.
- Clone your email opt-in step and place the clone in front of it in the form flow.
- Rewrite it as a question rather than a command, e.g. 'Do you want 10% off your first order?' instead of a statement.
- Keep the flow: micro-yes question, then a teed-up yes action, then the email field.
- The rationale the source gives: a first micro-commitment makes people more likely to say yes to the next step.
- A/B test micro-yes versus no micro-yes — the source says most brands see a submit-rate spike with it, but for some brands the version without it wins.
Caveat: Adds a click of friction; only keep it if your test shows a net gain in subscribers or revenue, not just submit rate.
Caveat: Effect varies by audience and offer strength.

Tags: email-lifecycle, signup-form, experiment-design, conversion-optimization, popup
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Reap the main email lifecycle payoff: LTV and AOV, not only last-click revenue
Use when: Planning the email channel's role in the store's overall acquisition and retention mix, and justifying budget and effort.
- Define objectives clearly: grow the list rapidly, and convert first-time buyers into returning customers.
- Position email next to, not instead of, paid ads: the source argues a store should not rely solely on paid traffic and treats email as an essential complementary channel.
- Use email to build a relationship that makes a customer more valuable than a one-time ad-driven buyer.
- Measure email's effect on LTV and AOV in addition to attributed revenue, since those are the outcomes the source attributes to the channel.
- Run standalone campaigns roughly a couple of times per week to nurture traffic into first purchase and first buyers into repeats.
- Use the offered campaign-calendar template as a planning artifact for the quarter.
Caveat: The dollar results cited in the source (e.g. 34–52% of revenue, revenue uplifts versus prior periods) come from that agency's clients — treat as illustrative examples, not benchmarks.
Caveat: Attribution of total revenue growth to email is questionable when paid spend, seasonality or product launches also changed.

Tags: email-lifecycle, retention, campaign-calendar, measurement, customer-lifetime-value, strategy
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Micro-yes signup step: ask for consent before email capture
Use when: Designing or A/B testing the newsletter/SMS signup form (popup or full page) for an ecommerce store.
- Add a step before the email opt-in that asks only a yes/no question, e.g. 'Do you want 10% off your first order?' with a single CTA button ('Yes please') and no input field.
- Remove the email input field from this step; clicking the button submits the micro-form and advances to the real email opt-in, which triggers the welcome flow.
- Keep microcopy under the button (e.g. 'No thanks, I'll pay full price', 'No spam guaranteed') to give an exit route.
- Split-test the form with and without the micro-yes step and compare the signup conversion rate for your own brand.
- Because the source reports that the micro-yes gives a spike in signups for most brands but some brands perform better without it, always validate rather than assume.
Caveat: Benefit is brand-dependent; source explicitly says to split-test it.
Caveat: The micro-yes is a lead-conversion (signup) tactic, not a purchase-conversion result.

Tags: email-lifecycle, signup-form, conversion-optimization, experiment-design, lead-capture, popup
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Signup form tests: delay, format, and audience size
Use when: Optimizing the newsletter signup popup for an ecommerce store, deciding timing and format.
- Run a time-delay A/B test, e.g. 4 seconds vs 12 seconds, and track total number of signups, not only the signup rate.
- Expect a shorter delay to lower the signup rate but possibly raise total signups because the form is shown to a larger audience.
- Test a popup form against a full-page form and compare signup rate and total signups.
- Test headline copy: 'Save 10% now', 'Get 10% now', 'Take 10% off now', 'Unlock 10% off now', 'Your discount awaits', 'Do you want 10% off'.
- Test CTA button text: 'Save 10% off now', 'Get 10% off now', 'Unlock my discount now', 'Reveal my discount now', 'I want my discount'.
- Test microcopy variants such as 'No thanks, I'll pay full price', 'No sales spam guaranteed', 'Rated 4.9/5 by 5,000 customers'.
Caveat: Signup rate and total signups can move in opposite directions; the source stresses watching total volume.
Caveat: Exact lift numbers are not promised; treat headline/CTA effects as testable, not guaranteed.

Tags: email-lifecycle, signup-form, conversion-optimization, experiment-design, copywriting, popup
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Visual signup form tests: color, images, and imagery content
Use when: Designing the visual layout of an ecommerce newsletter popup or signup page.
- Split-test a plain simple form against a fully designed form.
- Split-test a white form against a black form, and test input-field colors (contrasting color vs plain white).
- Test the CTA button color.
- Split-test a centered form with no side image against a form with a side image.
- When using images, test image content: the source cites a blanket brand where a blanket with a dog on it outperformed a plain blanket image.
Caveat: The blanket-with-dog result is a single brand example, not a universal benchmark.
Caveat: Image relevance to the product/category may matter more than image presence alone.

Tags: email-lifecycle, signup-form, conversion-optimization, design, experiment-design, creative-strategy
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## SMS opt-in angles after email signup
Use when: Adding or optimizing an SMS list opt-in step within the email signup flow.
- Build the SMS signup as an extra step after the email opt-in.
- Angle 1: use the same offer for SMS as email (e.g. 10% off both), and test it.
- Angle 2: offer a better SMS-only offer, e.g. email signup says 10% off, next step says 'Do you want 15% off? Sign up for SMS', and test it.
- Angle 3: use a VIP Club angle — email opt-in offers 10% off, SMS step offers 'Join our VIP Club for exclusive sales, pre-sales, early access', and test it.
- Split-test the angles against each other and measure SMS opt-in rate.
Caveat: The source presents these as testable angles, not guaranteed winners.
Caveat: Higher SMS discounts can erode margin; choose based on your own unit economics.

Tags: email-lifecycle, sms, signup-form, offer-design, experiment-design, retention
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Flow structure and profile filters in Klaviyo
Use when: Building or auditing Klaviyo flows for an ecommerce store so customers don't receive conflicting sequences.
- Pick a trigger based on customer journey stage: active on site, viewed product, added to cart, checkout started, placed order, or added to list/segment.
- After confirming a trigger, note it cannot be changed without duplicating the flow.
- Add profile filters under the trigger, e.g. 'has placed order 0 times since starting this flow', 'has checkout started 0 times since starting this flow', 'has added to cart 0 times since starting this flow'.
- For welcome series, add 'placed order 0 times', 'checkout started 0 times', and 'added to cart 0 times since starting this flow' so buyers and cart/checkout abandoners exit the welcome sequence.
- Consider excluding 'viewed product' and 'active on site' as well, but source prefers not to exclude those from welcome since browse/site abandonment flows are short and early in the journey.
- Use profile property updates (e.g. set 'in_welcome_series = true' at flow start, false at end) to segment flow participants in or out of regular campaigns.
- Use conditional splits with 'placed order since starting flow' to route buyers to a post-purchase email vs continuing the welcome series, or use a random 50/50 split to A/B test flow strategies.
Caveat: Trigger choice is locked after confirmation; you must duplicate the flow to change it.
Caveat: Excluding checkout-started and added-to-cart from a welcome series is the source's preferred approach but is presented as a judgment call.

Tags: email-lifecycle, klaviyo, automation, segmentation, flow-design, retention
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Use past profiles to backfill newly launched flows
Use when: Launching a winback, re-engagement, or time-delayed flow and wanting it to act on past behavior immediately.
- Open the flow's Manage Flow settings and choose 'Add past profiles'.
- Choose 'throughout the flow' so profiles are added based on where they would be if the flow had been live earlier, rather than only at the beginning.
- Example: a winback flow triggered 90 days after last order — adding past profiles throughout the flow lets someone whose last order was 80 days ago receive the first email in 10 days instead of waiting 90 days.
- Select 'eligible profiles' as the whole list or a specific segment.
- Note that flows containing dynamic coupons cannot use past profiles; if you need past profiles and a discount, use a static code instead.
Caveat: Past-profile backfill is unavailable for dynamic coupon flows — a real trade-off if you rely on dynamic codes.
Caveat: Adding profiles to the beginning vs throughout the flow produces very different behavior; choose deliberately.

Tags: email-lifecycle, klaviyo, automation, winback, flow-design, retention
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Turn off smart sending for flows, keep it on for campaigns
Use when: Configuring send settings inside any Klaviyo flow email for an ecommerce store.
- In each flow email's settings, uncheck 'Skip recently emailed profile' (smart sending) and save.
- Rationale: if a customer already received a campaign or other email within the last 16 hours, smart sending would skip them from a cart abandonment flow — losing high-intent, high-revenue sends.
- For campaigns, keep smart sending on in ~99.9% of cases unless there's a specific reason to disable it.
- The default smart-sending window is 16 hours and can be edited in general email settings (e.g. 8 hours), but the flow-level decision stays the same: off for flows.
- Enable UTM tracking in the same settings block (and optionally custom tracking) so revenue and behavior attribution works with Google Analytics.
Caveat: Source treats 'off for flows, on for campaigns' as its own strong rule; validate against your own send-frequency and deliverability data.
Caveat: Disabling smart sending can increase total email volume, which matters for spam-complaint rates.

Tags: email-lifecycle, klaviyo, deliverability, automation, attribution, flow-design
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Welcome series structure: 7 emails with distinct angles
Use when: Building or rewriting the welcome flow for an ecommerce store after newsletter signup.
- Email 1: deliver the discount code immediately (the promised incentive).
- Email 2 (~1 day later): brand story — founder message, origin, mission, what sets you apart — to build trust before pushing product.
- Email 3 (~1 day later): bestsellers; dive into unique features/benefits and the end result for the customer; cap at ~3–5 bestsellers depending on brand.
- Email 4 (~2 days later): reviews/UGC/press mentions — prioritize reviews about the specific pain points your subscriber has, not generic 'highly recommended' quotes.
- Email 5 (~2 days later): 'us vs them' USP comparison, since subscribers are comparing you to competitors.
- Email 6 (~2 days later): either a 48-hour discount reminder or a new/higher discount with a 48-hour deadline (source's split of two routes).
- Email 7 (~1 day later): 24-hour discount expiry as a plain-text email from the founder — plain text tends to improve deliverability and adds a personal touch.
- Remind subscribers of the discount code in every email, but give each email its own distinct angle.
- Add profile filters (placed order, checkout started, added to cart = 0 since starting flow) so buyers and cart/checkout abandoners exit the welcome series.
Caveat: The 3-day and 4-day defaults from Klaviyo are presented as slower than the source's preference; both are options, not proven superior.
Caveat: Fake urgency is explicitly cautioned against — make sure stated deadlines are real.
Caveat: Timing and email count are the source's opinion, not tested benchmarks.

Tags: email-lifecycle, welcome-series, copywriting, trust-building, flow-design, retention, social-proof
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Site abandonment flow: trigger, delay, and one guiding email
Use when: Recovering early-stage site visitors (homepage/blog visitors who did not view a product) for an ecommerce store.
- Create a flow with the 'active on site' API trigger.
- Add profile filters: 'has placed order 0 times', 'checkout started 0 times', 'added to cart 0 times', and 'viewed product 0 times since starting this flow' so anyone advancing in the journey exits.
- Add a time delay before email 1 of 1–4 hours; source suggests earlier journey stages can wait longer.
- Send one email that acts as a shop assistant: 'Is this what you're looking for?' with links to relevant collections or specific products depending on your catalog size.
- A/B test 1 hour vs 4 hours, and test 'guide to collections' vs 'guide to bestsellers' to see which drives product views.
- Turn off smart sending and enable UTM tracking in the email settings.
Caveat: The flow normally has a single email because these visitors are early in the journey and not yet high-intent.
Caveat: No default Klaviyo template exists for site abandonment; you must build it yourself.

Tags: email-lifecycle, site-abandonment, klaviyo, flow-design, browsing-intent, experiment-design
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Browse abandonment flow: trigger, filters, and review-led emails
Use when: Re-engaging shoppers who viewed a product but never added to cart on an ecommerce store.
- Use the 'viewed product' trigger.
- Add profile filters: 'checkout started 0 times', 'placed order 0 times', 'added to cart 0 times since starting this flow', and 'has not been in flow for the last 30 days'.
- Set the first-email delay — Klaviyo defaults to 2 hours; test 1 hour vs 3 hours and narrow down.
- Email 1: simple 'Did you see something you like?' reminder of the viewed product.
- Email 2 (~1 day later): reviews, UGC, press mentions to build confidence in the specific product.
- Use trigger filters to build product- or collection-specific browse flows, and make USP/review content specific to the viewed product — the source says specificity converts better.
- Delay any discount until around email 4–5; source argues giving discounts immediately trains shoppers to wait for codes.
- Aim for a 4–6 email sequence; turn off smart sending and enable UTM tracking.
Caveat: 'Wait to discount' is the source's opinion, not a tested benchmark across all stores.
Caveat: The 30-day flow suppression window is a default recommendation; your repurchase cycle and catalog should guide the choice.

Tags: email-lifecycle, browse-abandonment, klaviyo, flow-design, social-proof, offer-design, retention
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Abandoned cart flow: trigger distinction and 6–8 email structure
Use when: Setting up or fixing the abandoned cart sequence for an ecommerce store in Klaviyo.
- Select a Klaviyo template whose trigger is 'added to cart' — the popular 'abandoned cart' template actually uses 'checkout started', so verify the trigger before building.
- Add profile filters: 'checkout started 0 times', 'placed order 0 times', and 'has not been in flow for the last X days' (Klaviyo defaults to 7 days; source prefers ~14 days, adjusting for repurchase frequency).
- Set the first-email delay to 30 minutes–2 hours (Klaviyo default 4 hours is described as long), and A/B test 30 minutes vs 2 hours.
- Email 1: short reminder that the item is still in cart.
- Email 2 (~1 day later): reviews/UGC/press — the more specific to the exact product, the better.
- Email 3: objection handling — address reasons someone might hesitate to finish the purchase.
- Email 4: specific USPs of the product/brand.
- Email 5 (~1 day later): first discount (e.g. X% off) with 48-hour urgency, because a discount without urgency gives no reason to buy now.
- Email 6 (~1 day later): 24-hour deadline reminder.
- Emails 7–8 options: raise the discount, or send a plain-text founder email offering an extended 24-hour sale.
- Monitor spam-complaint, unsubscribe, and open rates as you lengthen the sequence; source warns long sequences (14–20+ emails) become annoying.
Caveat: Sources disagree on sequence length and suppression windows; treat 6–8 emails and 14 days as source preferences, not industry standards.
Caveat: Discounts should reflect margin realities; the source explicitly ties higher discounts to margins.
Caveat: Adding a post-purchase branch inside the cart flow is described as a common but not recommended pattern — the source prefers separate flows.

Tags: email-lifecycle, abandoned-cart, klaviyo, flow-design, social-proof, offer-design, deliverability, checkout
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Checkout abandonment flow: same structure, different objections
Use when: Recovering shoppers who started checkout but did not complete the purchase on an ecommerce store.
- Clone the abandoned cart flow and change its trigger to 'checkout started'.
- Remove the 'checkout started 0 times' profile filter (no longer relevant); keep 'placed order 0 times since starting this flow' and the flow-suppression window.
- Reuse the cart sequence structure but tailor copy to checkout-stage objections — the source cites surprise shipping costs as a common blocker.
- Consider offering free shipping instead of a percentage discount when shipping is the likely objection; source argues free shipping can cost less (for a $200 AOV) while converting the customer.
- Adjust reviews, USP content, and discount amounts to the later stage; these customers are one step closer to purchase.
- Keep discount timing late in the sequence (around email 5) and use urgency with any discount.
Caveat: The free-shipping-vs-discount trade-off depends on your margins and AOV; source gives a $200 AOV example, not a universal rule.
Caveat: Separate cart and checkout flows are both needed; do not rely on a single 'abandoned cart' template for both.

Tags: email-lifecycle, abandoned-checkout, klaviyo, flow-design, objection-handling, offer-design, checkout
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Time-delay heuristics by journey stage
Use when: Setting or tuning the first-email delay inside ecommerce abandonment flows.
- Site abandonment (no product viewed): 1–4 hours.
- Browse abandonment (product viewed): ~1–3 hours; Klaviyo default ~2 hours.
- Cart abandonment (added to cart): 30 minutes–2 hours; Klaviyo default 4 hours described as too long.
- Checkout abandonment: shortest delay, since intent is highest (structure follows cart flow with faster timing).
- Run A/B tests at each stage (e.g. 1 hour vs 4 hours for site abandonment) and narrow toward the best-performing delay.
- Inside time delays, you can also delay until a specific time of day or weekday, and choose store timezone, recipient local timezone, or specific days — use these to align sends with typical browsing/buying times.
Caveat: These are source heuristics, not tested universal timings — the source repeatedly says to split-test.
Caveat: Correct timing depends on niche, audience, and purchase frequency.

Tags: email-lifecycle, flow-design, send-timing, experiment-design, abandoned-cart, browse-abandonment
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Subject line, preview text, and sender name optimization
Use when: Configuring email metadata for ecommerce flows and campaigns in Klaviyo.
- In each email's edit settings, fill in subject line, preview text, sender name, and sender email address.
- Write a distinct, compelling preview text — the source calls it your second subject line; do not skip it.
- Note that plain-text emails have no preview text field, so only the subject line applies.
- Test sender name variants, e.g. a founder's name vs the company name, especially in welcome series.
- Use the same sender email address across all flows and campaigns to protect deliverability and consistency.
- Preview the email in desktop and mobile views before publishing.
Caveat: Plain-text emails can't use preview text, so you must rely on subject line alone — plan accordingly.
Caveat: No specific subject-line lift figures are given; treat this as a testable area.

Tags: email-lifecycle, subject-lines, copywriting, deliverability, experiment-design, klaviyo
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Bulk flow action status and flow analytics
Use when: Managing, launching, or reviewing ecommerce email flows in Klaviyo.
- In the flow's Manage Flow settings, update action statuses to set all emails to live, manual, or draft at once rather than editing each email individually.
- Add flow name and tags to keep flows organized.
- Use the Show Analytics view and select a time frame (including custom) to review flow performance.
- Use flow history to see changes over time.
- Note that trigger selection is permanent at the flow level; to change a trigger, duplicate the flow.
Caveat: Bulk status changes apply to all emails in the flow — verify no email is intentionally paused before switching to live.
Caveat: Klaviyo's interface changes frequently (the source notes the company was running UX tests in 2024), so verify current menu locations.

Tags: email-lifecycle, klaviyo, flow-design, measurement, operations
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Decide whether to use Klaviyo's default flow templates
Use when: Choosing whether to start an ecommerce flow from a Klaviyo template or build from scratch.
- When creating a flow, browse Klaviyo's prebuilt flows by goal (e.g. prevent lost sales, nurture subscribers) if you lack email marketing experience.
- Recognize that default templates are not optimized for your specific brand and audience.
- If you have the capability, build custom flows from scratch; the source recommends this approach for better conversion.
- If you do use a template, review and adjust triggers, delays, and content before launching — never ship a template unedited.
- Note the source's view: something is better than nothing, but custom flow work is worth the effort.
Caveat: 'Custom flows convert better than templates' is the source's opinion, not a measured benchmark.
Caveat: Template availability and naming in Klaviyo change; verify current options in the interface.

Tags: email-lifecycle, klaviyo, flow-design, conversion-optimization, operations
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Exclude engaged customers from overlapping flows
Use when: Designing or auditing ecommerce email flow logic to prevent a customer receiving conflicting or repetitive sequences.
- For each pre-purchase flow, add exclusion filters for later journey events: e.g. welcome series excludes placed order, checkout started, and added to cart.
- Site abandonment excludes placed order, checkout started, added to cart, and viewed product since starting the flow.
- Browse abandonment excludes checkout started, placed order, and added to cart since starting the flow.
- Cart abandonment excludes checkout started and placed order since starting the flow.
- Checkout abandonment excludes only placed order since starting the flow.
- Set a 'has not been in flow for the last X days' filter (30 days for browse, 7–14 days for cart/checkout) to prevent re-triggering the same flow too often.
- Rationale: overlapping flows send too many emails, which can trigger spam complaints and erode trust.
Caveat: Whether to exclude active-on-site and viewed-product from the welcome series is a judgment call; source prefers not to exclude those because their flows are short.
Caveat: Flow-suppression windows should match your repurchase cycle — a 7-day window is fine for weekly replenishment but too short for long repurchase cycles.

Tags: email-lifecycle, flow-design, segmentation, deliverability, retention, klaviyo
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Use trigger filters for product- and collection-specific flows
Use when: Building product-specific or collection-specific abandonment sequences in Klaviyo for an ecommerce catalog.
- Open the flow's trigger settings and add a trigger filter under Add trigger filter.
- Select dimensions to include or exclude specific products or collections — e.g. only send a browse-abandonment flow for a high-margin collection.
- Use trigger filters when you want different sequences for different product categories, each with its own reviews, USPs, and objections.
- For site abandonment flows, trigger filters are generally not used because no product has been viewed yet.
- Combine trigger filters with specific review/UGC content about the exact product or collection to increase relevance.
Caveat: The more product-specific flows you build, the more maintenance overhead; prioritize products/collections with enough traffic to justify it.
Caveat: Klaviyo's trigger-filter UI may move between versions; verify current setup in the interface.

Tags: email-lifecycle, klaviyo, flow-design, segmentation, browse-abandonment, abandoned-cart, personalization
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Use plain-text founder emails and real urgency for final conversion
Use when: Writing the final emails of ecommerce welcome, cart, checkout, or browse sequences to convert holdouts.
- Send the final email as plain text rather than a designed template — the source says plain text generally delivers better and feels more personal.
- Send it from the founder's name (a real or fictional person at the company), using the founder's voice.
- Use explicit urgency such as 'your discount expires in 24 hours', and make it true — the source stresses not using fake urgency.
- For discount expiry, use a dynamic coupon code so the deadline is genuine; avoid static codes like 'WELCOME10' as the urgency mechanism.
- Options for the final push: extended sale for 24 hours only, a higher discount, or a founder plain-text last-chance email.
- In welcome series, place this plain-text founder email around email 7; in cart/checkout flows, use it around emails 6–8.
Caveat: Fake urgency damages trust; use dynamic codes or genuinely expiring offers.
Caveat: Plain-text emails cannot include preview text, so the subject line carries the full burden.

Tags: email-lifecycle, copywriting, deliverability, urgency, founder-message, flow-design
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Clone the Core Pre-Purchase Flows Instead of Building from Scratch
Use when: Standing up pre-purchase automation for a store from zero, or when you need to ship cart/checkout abandonment emails quickly without redesigning content for each.
- Establish one pre-purchase flow as your structural template (commonly the abandoned cart flow). It holds the general email structure, delays, and offer logic you'll reuse.
- Clone it and rename for the next flow. Change the trigger to the matching event — for a checkout abandonment flow, the trigger is 'Checkout Started'.
- Add or remove profile filters so the flow only targets people who haven't already bought. For abandoned cart/checkout, a common filter is 'Placed Order zero times since starting this flow' so buyers don't get further abandon emails.
- Keep an additional filter such as 'has not been in this flow in the last 7 days' to avoid re-enrolling people too soon.
- Keep the general content structure but rewrite the copy toward the specific objection — for checkout abandonment the reason is different (usually payment/logistics friction) than for cart abandonment.
- Note the source positions the welcome, site abandon, browse abandon, cart abandon, and checkout abandon flows as the essential pre-purchase set.
Caveat: The filter logic and trigger names are platform-specific (Klaviyo/Shopify) — verify the current interface before building.
Caveat: Cloning is a starting point; you must tailor the content, not just the trigger.

Tags: email-lifecycle, flow-building, cart-abandonment, checkout, automation, klaviyo, pre-purchase
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Add a Cancelled-Order Filter to Post-Purchase Flows
Use when: Setting up a post-purchase or customer thank-you flow, where someone could place an order and then cancel before the flow finishes sending.
- Set the trigger to 'Placed Order'.
- Add a profile filter that reads roughly 'Placed Order / Cancelled Order equals zero times since starting this flow' — the source's default is 'cancelled order zero times since starting the flow'.
- Rationale from the source: a customer can place an order and then cancel it, and you don't want them receiving the rest of the thank-you/upsell content after a cancellation.
- Optionally make trigger filters based on specific collections or products if you want product-specific post-purchase flows.
- Ensure this filter sits before the first send so it gates the whole flow, not just one email.
Caveat: Filter naming and availability depend on the ESP and its cancel-order support — verify in the current interface.
Caveat: Product/collection-specific post-purchase flows require your ESP to expose product data on the order event.

Tags: email-lifecycle, post-purchase, flow-building, automation, klaviyo, filtering
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Time Your First Post-Purchase Email Around Transactional Emails
Use when: Designing the first email in a post-purchase/customer thank-you flow, deciding the initial send delay.
- Recognize that a purchase immediately triggers transactional emails (order confirmation, shipping updates) from your store platform. The source notes these go out right away if your system is configured correctly.
- Avoid sending your marketing post-purchase email instantly so you don't 'support-bomb' the customer with multiple emails at once.
- The source's default is to wait roughly 30 minutes after purchase before the first post-purchase email.
- Use the delay to let the transactional confirmation land first, then follow with the branded thank-you.
- Keep the first marketing email light on logistics (the transactional email already covers shipping) — just reinforce trust and set expectations.
Caveat: The 30-minute delay is the presenter's preferred default, not a benchmark — adjust based on your transactional setup and product.
Caveat: If your platform's transactional emails are delayed or missing, fix that first rather than compensating in the flow.

Tags: email-lifecycle, post-purchase, timing, flow-building, transactional-email
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Split Post-Purchase Email 1 by First-Time vs Returning Buyer, Then Merge Paths
Use when: Building the branching logic of a post-purchase flow and deciding which portions should be segmented.
- After the initial delay, add a conditional split on 'Placed Order equals 1 overall time' — Yes routes to first-time buyer content, No routes to returning/repeat customer content.
- Write different Email 1 copy for each branch: acknowledge whether they're new or returning, and set the tone accordingly.
- Turn OFF smart sending on these transactional-style thank-you emails so they send as intended rather than being delayed/skipped.
- The source notes you can extend the split further — e.g., buyers with ~4 purchases could be treated as VIPs with different content — but first-time vs returning is the useful baseline.
- After Email 1, merge both branches back into a single path and send the same content (Email 2 onward) to everyone; the source treats this as the default unless you have reason to keep separating.
- Decide per your brand whether returning customers even need emails 2+; the source keeps both and merges.
Caveat: This is a conditional-split pattern specific to the platform; verify the operator options available.
Caveat: Whether to keep returning customers in the full flow is a judgment call — test for your audience.

Tags: email-lifecycle, post-purchase, segmentation, conditional-split, flow-building, retention
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Use the First Post-Purchase Email to Reduce Buyer's Remorse and Cross-Sell Softly
Use when: Writing the first post-purchase email content, especially for the 24–48 hours after purchase when doubt peaks.
- Send it as a plain-text email written from the founder or team to feel personal.
- Acknowledge the purchase and explicitly recognize whether the buyer is first-time or returning — the source calls this 'really important' for feeling appreciated.
- Address buyer's remorse: the source explains that in the 24–48 hours after paying but before receiving the product, buyers second-guess whether the purchase was worth it and whether the brand is trustworthy.
- Include a short reassurance line like 'we're preparing your order and will keep you updated on shipping' — you don't need to repeat full logistics since transactional emails cover that.
- Add a soft cross-sell line: 'if you want to add something to your order, click here' linking to the store, so the extra item ships with the original order — the source says this increases average order value and reports good results.
- Keep the primary goal trust-building; treat the AOV lift as a side effect, not the main aim.
Caveat: The AOV benefit is the source's reported experience, not a guaranteed result.
Caveat: The cross-sell only works operationally if you can actually combine shipments — confirm your fulfillment supports it.

Tags: email-lifecycle, post-purchase, buyer-remorse, cross-sell, average-order-value, copywriting, retention
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Sequence the Post-Purchase Flow Around Shipping, Usage, Loyalty, Reviews and Cross-Sell
Use when: Mapping the full email sequence and delays of a post-purchase flow for a physical product.
- Email 1 (~30 min): thank-you and buyer's remorse reduction (see related card).
- Email 2 (~2 days): build excitement for delivery by giving product usage instructions. This future-paces the customer using the product, reduces buyer's remorse, and pre-empts support questions. If you sell multiple product types, use product-based splits to tailor this email to the item bought.
- Email 3 (~10 days): introduce your loyalty program. The source argues this is the moment the customer is happy having received and tried the product, making it a natural point to enroll them and move a first-time buyer toward repeating. Note: the delay depends on your shipping times — the source sets it after expected delivery.
- Email 4 (~+3 days): ask for a review, since by now the customer has enough usage to have formed an opinion. Offer a discount code as a thank-you for reviewing — the source notes it's optional but useful because even non-reviewers get a code and may rebuy.
- Email 5 & 6 (~7 days later, then +1 day): cross-sell with a discount and a 48-hour deadline, followed by a plain-text 24-hour deadline email from the founder. The source says founder plain-text emails 'work so well.'
- The delay to delivery and the review ask depend on your product type and shipping times; adjust accordingly. If you sell consumables, the source notes you can add a 'replacement reminder' (e.g., a 30-day product prompting at day ~25).
Caveat: Delays are the presenter's defaults and depend on shipping and product type — validate against your own data.
Caveat: The source flags review flows may be better as a separate flow when using a dedicated review platform (e.g., Judge.me) with its own triggers; otherwise you can host the ask inside the post-purchase flow.

Tags: email-lifecycle, post-purchase, flow-building, loyalty, reviews, cross-sell, timing
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Target the First-to-Second Purchase Gap as the Hardest Retention Step
Use when: Deciding where to invest retention/win-back effort — loyalty, post-purchase, and win-back flows — and setting expectations for which cohort to focus on.
- Recognize the source's framing: going from a first-time buyer to a second-time buyer is the hardest step; once a customer has bought 2–3 times, getting them to buy again is comparatively easy.
- Design the post-purchase flow (loyalty intro, review request, cross-sell) specifically to shorten that first-to-second gap.
- Use the win-back flow to catch first-time buyers who never returned within your typical buying cycle (see win-back card).
- In the loyalty introduction email, emphasize earning points and discounts on the next purchase to lower the barrier for a second order.
- Treat first-time buyer retention as the metric to watch, not just total repeat rate.
Caveat: This is the presenter's framing of relative difficulty, not a measured benchmark — your category may differ.
Caveat: Durability and consumable products may have structurally shorter repurchase cycles than the source's general claim.

Tags: email-lifecycle, retention, first-time-buyer, loyalty, win-back, post-purchase
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Set Win-Back Timing from Your Own Buying Cycle Data
Use when: Configuring the trigger and delay for a customer win-back flow for lapsed customers.
- Set the trigger to 'Placed Order' and add a profile filter like 'Placed Order zero times since starting this flow' so buyers exit.
- Choose the wait based on your brand's buying cycle — research how long customers typically take to repurchase (the source suggests checking your Shopify data). The source notes the platform default is ~75 days but that 40 or 90 days may fit better for your brand.
- A/B test the delay for your store to find what works best.
- Use the platform's 'add past profiles' feature (bulk enrollment) so people who would already have been at the right point in the flow are enrolled without waiting the full delay.
- Build the content: Email 1 ('it's been a while') highlights new arrivals or specific collections; the source suggests the default two-email win-back is thin and you can expand it.
Caveat: 75 days is a platform default, not a benchmark — derive your own delay from data.
Caveat: Bulk/past-profile enrollment behavior depends on your ESP — verify the feature before relying on it.

Tags: email-lifecycle, win-back, retention, timing, flow-building, segmentation, measurement
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Escalate Win-Back Offers Slowly with Long Delays to Avoid Annoying Lapsed Customers
Use when: Writing the email sequence and offer cadence for a customer win-back flow.
- Email 1: no discount — 'it's been a while', guide toward new arrivals or collections.
- Email 2 (short gap, the source suggests ~3 days rather than the default 15): reinforcement/reminder, still non-discounted.
- Email 3 (~7 days later): first discount with a 48-hour deadline if they haven't converted.
- Email 4 (~1 day later): another deadline email, optionally plain text, with a 24-hour deadline.
- Emails 5 & 6 (~2 weeks later): a higher/second discount with 48-hour and 24-hour deadlines, possibly plain text again.
- Use longer time delays throughout because recipients are disengaged; the source warns that sending many emails in a short window to lapsed customers risks annoyance, spam complaints, and deliverability damage.
- A/B test this flow heavily — the source singles out win-back as one that deserves a lot of testing, especially for reactivating first-time buyers.
Caveat: Recommended delays are the presenter's defaults — adjust to your brand and test.
Caveat: Discount escalation erodes margin if overused; the source ties offer discipline to list health (see campaign-mix card).

Tags: email-lifecycle, win-back, offer-design, timing, deliverability, experiment-design, retention
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Run a Sunset Flow to Re-Engage or Suppress Unengaged Subscribers
Use when: Cleaning your list and protecting deliverability by identifying and suppressing subscribers who haven't engaged in a long window (e.g., 90–120+ days).
- Trigger the flow off your unengaged segment (defined later in the course via segmentation) — subscribers who haven't opened in roughly 90, 120 days, or longer, depending on the segment you choose.
- Write Email 1 as a plain-text 'you haven't opened in a while — are you still interested? If not, click here to unsubscribe.' Actively inviting the unsubscribe is intentional.
- Send Emails 2 and 3 using your highest-permissible discount and clickbait-style subject lines — the only goal is to get an open, which re-engages the subscriber so campaigns can resume.
- Use plain text throughout because the source reports it delivers better than designed emails and reads more personally, improving the chance of landing in the primary inbox.
- If a subscriber doesn't open any email in the flow, update a profile property (e.g., 'unengaged = true') and build a segment on that property so you can suppress them.
- The source's framing: you'd rather have people unsubscribe than stay on the list costing you money and risking spam complaints.
Caveat: The source states this flow won't generate much revenue — its purpose is list hygiene/deliverability, not sales.
Caveat: The 90/120-day window is a segment choice, not a fixed threshold — set it from your own data.
Caveat: Verify property/segment tooling in your current ESP interface.

Tags: email-lifecycle, sunset-flow, deliverability, list-hygiene, re-engagement, segmentation, plain-text
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Have the Five Core Flows Plus Win-Back and Sunset in Place
Use when: Auditing which automation flows a store still needs, or sequencing which flows to build first.
- Confirm the pre-purchase set exists: welcome series, site abandon, browse abandon, cart abandon, checkout abandon.
- Confirm post-purchase and customer win-back exist as post-purchase flows.
- Confirm the sunset flow exists for list hygiene.
- The source singles out the welcome series, cart abandon, and browse abandon as the most important flows to keep optimizing over time — treat them as ongoing optimization targets, not set-and-forget.
- Beyond the core, the source lists optional/extended flows as the possibilities are 'endless': bounceback offer right after purchase, back-in-stock, replacement reminder (e.g., a 30-day consumable prompted at ~day 25), product/data-based cross-sell flows, and a tailored 'highly engaged but never purchased' window-shopper flow.
Caveat: Which flows are 'biggest money-makers' is the presenter's assessment, not a measured benchmark across stores.
Caveat: Build order should consider your data volume — some flows (e.g., back-in-stock) need inventory/restock events to exist.

Tags: email-lifecycle, flow-building, prioritization, welcome-series, abandonment, win-back, sunset-flow
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Turn Smart Sending Off for Flows, On for Campaigns
Use when: Configuring flow and campaign send settings to control when emails are skipped versus always delivered.
- In flows, turn smart sending OFF — the source says you always want flow emails to send as designed rather than being suppressed by recent-email logic.
- For example, turn off smart sending on the post-purchase thank-you emails so they aren't skipped.
- In campaigns, turn smart sending ON (the source says ~99.9% of the time) — this is the 'skip recently emailed profiles' toggle, avoiding duplicate sends to people who were just emailed.
- Enable UTM tracking on campaigns.
- When preparing a campaign, set the recipient list (start with the main/newsletter list but send to engaged people — see segmentation), confirm smart sending, then proceed to content, subject line, preview text, sender name, and sender address.
Caveat: Smart sending behavior and toggle location are platform-specific — verify in the current interface.
Caveat: Sending only to engaged people interacts with list hygiene; don't rely on smart sending as a substitute for a clean list.

Tags: email-lifecycle, smart-sending, campaigns, flow-building, deliverability, utm-tracking, klaviyo
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Choose Among Drag-and-Drop, Plain Text, or HTML Email Editors
Use when: Deciding which email editor to use when building a campaign or flow email.
- Default to the drag-and-drop editor for most campaigns — it's the source's go-to for designed emails.
- Use plain text (text-only) emails occasionally to feel more personal and improve deliverability; use them specifically in deliverability-sensitive flows like post-purchase thank-yous and the sunset flow, and for founder deadline emails.
- Avoid raw HTML: the source says you'll 'almost guaranteed' hit mobile/desktop rendering issues and it's hard to get pixel-perfect across browsers and apps.
- In the builder, create a blank email (or use the template library / saved templates) and assemble using the editor.
- After building, exit the editor, review the email, and double-check recipients, smart-sending setting, and subject line before scheduling or sending.
Caveat: These are the presenter's preferences, not absolute rules — some stores may have the design resources to make HTML work.
Caveat: Template availability and exact editor names vary by ESP version — verify the current interface.

Tags: email-lifecycle, email-design, plain-text, drag-and-drop, deliverability, campaigns
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Use Seven Campaign Buckets to Source Email Ideas
Use when: Generating campaign ideas and building a varied campaign calendar that doesn't fatigue your list.
- Bucket 1 — Promos and special offers: discounts.
- Bucket 2 — Holidays, special events, Black Friday, Christmas.
- Bucket 3 — Product launches: launch a new product with one or a sequence of emails.
- Bucket 4 — Product highlights: problem→product-solution angles, us-vs-them/competitor comparisons, bundles, essentials round-ups (e.g., top three skincare essentials), bestsellers, new arrivals, gift guides (strong in Q4 and before Valentine's), subscription content, back-in-stock/restock, ingredients and benefits.
- Bucket 5 — Social proof: reviews, user-generated content, influencer messages, press mentions.
- Bucket 6 — Value-based: blogs, articles, myths, how-tos that give value (strong if you have blog content).
- Bucket 7 — Company updates: brand updates, founder story, behind-the-scenes, product development.
- When planning a month, make sure you have a good mix spanning different buckets rather than leaning on one.
Caveat: The seven buckets are the source's organizing framework; not every brand will use all seven evenly.
Caveat: Some buckets (value-based, social proof) depend on assets — blog content, reviews, UGC — that you may need to build first.

Tags: email-lifecycle, campaigns, content-strategy, calendar, social-proof, product-launch, campaign-mix
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Cap Discount Frequency with a 5:1 to 10:1 Non-Discount Ratio
Use when: Planning campaign cadence and deciding how often to deploy discounts across your email calendar.
- Use at least a 5:1 ratio — five non-discounted emails for every one discounted email, as the minimum.
- For the source's own clients, target 10:1 (ten non-discounted per discounted) and cap discounts at roughly one per month.
- Be aware of Q4/Black Friday as the exception where discounting increases.
- In other months the source sometimes runs two months with zero discounts for some clients.
- Rationale from the source: constantly giving discounts trains your audience to ignore them ('you already did it last week'), so a rare discount creates real excitement; it also protects brand reputation and margin.
- This applies both to standalone campaigns and to the offer logic inside win-back and sunset flows — escalate offers rather than front-loading them.
Caveat: The 5:1 and 10:1 ratios and the one-per-month cap are the presenter's recommendations, not universal rules — set for your margin and category.
Caveat: Q4 is explicitly called out as an exception.

Tags: email-lifecycle, offer-design, campaign-mix, discounts, brand-strategy, margin
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Set Campaign Frequency from Revenue Tier, Then Adjust by Metrics
Use when: Deciding how many campaigns per week to send, and whether to scale frequency up or pull back.
- Starting guideline: stores under ~50k/month send roughly 2–3 campaigns/week.
- Stores over ~50k/month target roughly 3–4 campaigns/week.
- Stores over ~200k/month total revenue can send roughly 4–5 campaigns/week.
- The source's sweet spot for most clients is ~3–4 campaigns/week; it would 'almost never' go above 5/week, since that reads as spammy — unless you segment so each person only receives ~3/week.
- Adjust by data: if you currently send 1/week and open rate is above ~30% with low unsubscribes, you can increase to 2/week. If already at 2/week with open rate above ~30%, increase to 3/week.
- Pull back: if you send 4/week with open rate below ~30% and high unsubscribes, don't increase even if revenue is high — instead clean your list and possibly drop back to 3/week.
- Never decide frequency on gut feel — always look at the brand's data.
Caveat: The revenue tiers, 3–4/week sweet spot, ~5/week ceiling, and 30% open-rate threshold are the source's rough heuristics, not measured industry benchmarks.
Caveat: Higher frequency is only safe with solid segmentation so individual subscribers receive fewer messages.

Tags: email-lifecycle, campaign-cadence, measurement, open-rate, segmentation, deliverability, list-hygiene
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Plan the Campaign Calendar by Layering Events, Value Content, and Company News
Use when: Building out a month's campaign schedule and filling empty send slots with a non-repetitive mix.
- Step 1 — List key holidays and events, not just generalized ones. Consider days crucial to your brand and audience. Use a resource like nationaltoday.com, pick the target month, and list events that fit your brand (e.g., 'Sunscreen/Sun Safety Month' for a sunscreen seller). Don't leverage everything — pick what's relevant.
- Step 2 — Choose value-based content for the time of year — for instance, a 'top five skincare tips for fall' blog works in October but not May. YouTube content and existing blogs can be reused. Two routes: (a) summarize the blog and link to the full blog as the main CTA, or (b) summarize the blog and link to the products mentioned as the main CTA. The source says test both; if you have no blog, use Google to research valuable content and write an email around it.
- Step 3 — Add company events: back-in-stock, product launches (or a full sequence), upcoming holidays → gift guide, etc.
- Step 4 — Fill remaining blank slots with the other buckets: share user-generated content, reviews, address a common audience problem and tie it to your product, bust a myth in your niche and link a product.
- Layer the mix — e.g., in an August example the source set a product highlight every Sunday, value-based email Tuesdays, a VIP flash sale, a review email, and a company update, with sends on Tuesday/Thursday/Sunday.
Caveat: nationaltoday.com and calendar image tools are external tools — verify current availability; the specific holidays shown are examples, not endorsements of any holiday as universally relevant.
Caveat: The route that yields better results (link to blog vs link to products) differs by audience — the source insists you split-test rather than assume.
Caveat: Don't over-complicate or over-use holidays, and don't attach a discount to every event.

Tags: email-lifecycle, calendar, campaign-mix, content-strategy, campaigns, seasonality, experiment-design
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Run Campaign Calendar Planning in a Shared Planning Tool
Use when: Setting up the operational workflow and documentation for planning and shipping campaigns.
- Choose a planning tool — the source has used Notion and now uses Airtable, but notes ClickUp, Monday, and even a Google Sheet work fine.
- The tool choice doesn't matter; the source stresses the only requirements are consistency, logging everything, and clarity for everyone involved in the process.
- Optionally sketch the month visually first — e.g., a blank calendar page image imported into a whiteboard tool — then transfer the plan into your tracker.
- Once the rough calendar exists, build it out in whichever tool you selected.
- Keep it maintained as you produce and send, so the calendar reflects reality (not just the plan).
Caveat: Tool names are examples; the operative point is consistent, shared logging, not the specific software.
Caveat: This is a process/workflow recommendation, not a performance claim.

Tags: email-lifecycle, calendar, operations, workflow, airtable, documentation
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Design Emails for Conversion, Not Just Aesthetics — Favor Simplicity
Use when: Designing campaign and flow emails, especially deciding how much copy and visual decoration to include.
- Adopt the 'clean, tidy room vs messy room' framing: long paragraphs of text and too many colors are uninviting; a clear, uncluttered layout invites reading.
- Keep the email simple and to the point: one clear value proposition and a unique mechanism toward the end state — no blobs of text, no excessive callouts, nothing over the top.
- The source notes email design has shifted away from long-form copy toward simplicity because subscribers either lack the time or already expect persuasive fluff and tune it out.
- Remember the core principle: more friction → less conversion; less friction → more conversion. Aim to reduce friction in layout and copy.
- The source's example: a clearance email needs only two lines of copy plus a designed CTA button — not a wall of text to say '40% off clearance.'
- Ensure the email visually matches your website branding, since the source treats brand consistency as a primary reason design matters.
Caveat: This reflects a shift the source observed over recent years in e-commerce email — it's directional advice, not a hard rule for every brand or audience.
Caveat: Simpler design still needs a strong offer/copy — design alone won't convert.

Tags: email-lifecycle, email-design, conversion-optimization, copywriting, branding, campaigns
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Use Visual Hierarchies (Z, Inverted Triangle, F Patterns) to Guide the Eye to the CTA
Use when: Laying out an email's sections and deciding where to place headlines, body copy, images, and the CTA button.
- Z/zigzag pattern: alternate elements left-right following natural eye movement, with lines or imagery guiding the eye toward the different elements. The source cites Magic Spoon as a strong example, using generous whitespace and little copy.
- Inverted triangle: place an attention-grabbing headline at the wide top, then narrow the focus down through body copy to the primary CTA button at the point. The source cites Dr. Squatch as an example.
- F pattern: headline, then body copy, then CTA — simple and familiar. The source cites a lollipop brand example and says you 'can't go wrong' with it, but also warns to vary patterns so it doesn't get monotonous.
- Keep the goal clear: focus the reader toward the CTA button, which takes them to your site where a purchase can happen.
- Use visual hierarchies to reduce the bouncing between ideas; the more the reader has to jump around, the higher the friction and the more likely they close the email.
Caveat: These patterns are the source's framework, not tested performance guarantees — apply them in your brand's style and test.
Caveat: The source notes the F pattern is simple and safe but can get boring, so alternate patterns over time.

Tags: email-lifecycle, email-design, visual-hierarchy, conversion-optimization, call-to-action, campaigns
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Replace Long Paragraphs with Visual Formats (Checklists, Tables, Comparisons)
Use when: Writing email body copy that would otherwise become a long paragraph, especially product comparisons or multi-point explanations.
- Replace long paragraphs with visuals — the source names checklists, comparison tables, and graphs as examples that are 'way easier to digest.'
- Example from Magic Spoon: use a visual sequence ('Rise. Spoon. Shuffle to your kitchen. Pour Magic Spoon into the bowl.') leading to another CTA, communicating the promise visually rather than in prose.
- Example from Magic Mind: instead of explaining each hormone in a paragraph, present the information as a checklist of a few checkpoints — the source says readers are far more likely to read the checklist than the paragraph.
- Example from a bar brand: instead of a paragraph comparing bars, use a comparison table so benefits and differences are immediately clear.
- Keep emails short and snappy rather than one big wall of text.
- Note the source's framing that copy and design 'integrate with each other' — you're not writing copy and then decorating it, you're designing as you write.
Caveat: Visual formats still need accurate content — the presentation changes, not the substance.
Caveat: Very simple products or single-idea emails may not need a comparison/checklist; don't force a visual where two lines suffice.

Tags: email-lifecycle, email-design, copywriting, visual-hierarchy, conversion-optimization, campaigns
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Treat the Above-the-Fold Section as Decisive — Include Headline, Support, and CTA
Use when: Designing the top of any email — campaign or flow — where you choose what appears before the reader scrolls.
- Define the above-the-fold section as the viewable area of the email before scrolling on desktop or mobile (the term comes from newspapers optimizing their most visible part).
- The source readopts the 'people just bounce' assumption and argues, based on its own client data, that above-the-fold optimization still matters — including on mobile — because most viewing and clicking happens there.
- Include an attention-grabbing headline: readers decide in a few seconds whether to continue.
- Include supporting brand image and/or text that clarifies what the email is about.
- Include an interesting call to action button within this section so readers can act immediately.
- Example from Ritual: 'Enjoy 30% off for Memorial Day — shop now' with an aesthetic image and a CTA button makes the email's purpose instantly clear on mobile. Another example (Dr. Squatch) uses an arrow to guide the eye toward the CTA.
Caveat: The source explicitly notes there's ongoing debate about whether above-the-fold optimization still matters; its position is that it does, backed by its own data — but this is the presenter's view, not a universal law.
Caveat: The specific brand examples are illustrations, not endorsements or guarantees.

Tags: email-lifecycle, email-design, above-the-fold, conversion-optimization, call-to-action, campaigns
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Build a Modular Figma Email Template Library for Fast, Varied Design
Use when: Setting up an email design system, especially when producing many emails or serving multiple brands and needing variation.
- Use a cloud design tool like Figma so designers and clients can collaborate on email designs.
- Build basic template blocks: multiple header sections, product sections, body sections, and review blocks — the source's agency made roughly 25 header section variations alone.
- For each block type, create many variations (e.g., header with logo + title + text + CTA + image; header with logo + title + CTA; centered vs with/without supporting text; 2×2 product grids; zigzag product layouts; multiple review display styles).
- Assemble a full email by picking and matching sections, then layer your brand's fonts, colors, and styling on top — every brand's final design differs by its own branding.
- Include body-section visuals like checklists and other data visualizations, not just body copy.
- The source says this is especially helpful when producing many emails across clients where appearing original and varied is otherwise difficult.
Caveat: The specific template counts and section types are the source agency's setup — build what fits your brand and volume.
Caveat: Figma is the source's tool of choice for agency/client collaboration; other design tools can serve the same modular purpose.
Caveat: Templates are a starting point — you must apply branding to avoid generic-looking emails.

Tags: email-lifecycle, email-design, templates, figma, workflow, design-system, productivity
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Slice a Figma email into image sections before importing to Klaviyo
Use when: Importing a Figma-designed campaign into Klaviyo or another ESP, or diagnosing slow/clipped campaign emails.
- Do not export the whole email as one image: the file is large, loads slowly in the inbox, can cause deliverability problems, and allows only one link for the entire email.
- In Figma, switch the tool from Frame to Slice and select logical sections: hero/header, section titles, each product block, call-to-action button, footer.
- Leave short text elements (headings, section labels, legal lines) out of the slices if you plan to rebuild them as real text in the ESP, because real text helps deliverability.
- Export each slice as PNG or JPG, then compress all of them (e.g. TinyPNG, Squoosh, iLoveIMG) — one example reduced the hero from ~2 MB to ~522 KB and other slices by 50–74%.
- Upload the compressed images into the ESP and reconstruct the email block by block, then add text blocks, padding, links and alt text.
- Keep the mandatory unsubscribe block; delete other default ESP blocks before rebuilding.
- Verify the current Figma export and ESP upload interfaces, since both change.
Caveat: Compression ratios vary by image; check quality after compression.
Caveat: Slicing is only needed for image-heavy designed emails; text-heavy templates may not need it.

Tags: email-lifecycle, email-design, klaviyo, figma, image-optimization, deliverability, campaign-production
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Set alt text, deep links and auto-applied discount codes on email images
Use when: Building or QAing a campaign in an ESP, specifically linking product images and setting alt attributes.
- Fill in alt text for every image: it shows if the image fails to load and is read by inbox providers such as Gmail to understand the email.
- Write the alt text as a short description including the offer, e.g. '20% off shower products with code DIRTYDISCOUNT'.
- Link each image to the most specific relevant page — a category/collection page or a single product page — never just the homepage.
- Embed the discount code in the URL if the platform supports it (the source demonstrates a redirect parameter after the domain containing the code and destination collection), so the code is applied automatically at checkout.
- Test each modified URL in a browser before sending to confirm it resolves and the discount applies.
- Run through every link in the ESP preview on desktop and mobile to catch broken or wrong destinations.
Caveat: The exact URL/discount parameter format depends on the store platform; the source's example is one implementation — verify what your platform supports.
Caveat: Auto-applying the code reduces friction, but is not a replacement for showing the code in the email copy.

Tags: email-lifecycle, klaviyo, email-design, product-page, checkout, discounts, conversion-optimization, qa
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Size, pad and fix email images so they render correctly on mobile
Use when: Finalizing email layout in an ESP drag-and-drop builder and checking the mobile preview.
- Set base text styles before assembling: roughly 18px desktop and at least 16px mobile, line spacing around 1.5, and a chosen alignment — adjust to brand.
- After importing each image, set block padding — the source adds about 20px top and bottom between sections to recreate the whitespace from the design file, since whitespace makes content easier to digest.
- Where sections sit directly above each other, add padding only on the bottom to avoid doubling spacing.
- When a text block keeps desktop side padding in the mobile preview (visible as an over-indented paragraph), enable the full-width-on-mobile toggle on that block.
- Use the preview to compare desktop and mobile against the original design before scheduling.
- Verify padding controls, since ESP builders change their padding UI over time.
Caveat: Exact pixel values are the source's preference, not a rule; match the original design and brand.
Caveat: Sending a real test to your own inbox and checking mobile and desktop is the final step before scheduling.

Tags: email-lifecycle, klaviyo, email-design, mobile-optimization, campaign-production, qa
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Cap products per campaign email at three to four and keep the offer above the fold
Use when: Designing or reviewing a promotional campaign's layout and product selection.
- Put the headline offer, the discount code and a large CTA in the above-the-fold hero so nothing important requires scrolling.
- In the source's Dollar Shave Club example, the original email only showed the discount code far below a small button; the revamp moved code and a big CTA to the top.
- Limit the email to a maximum of three to four product blocks — the source argues too many links hurt deliverability and too many options stop people choosing.
- Use a zigzag or other visual hierarchy to present the chosen product blocks rather than a flat list.
- Repeat the offer and code with another CTA in the closing body copy.
- Include multiple category links in the footer so recipients who don't want the promoted category can still find something relevant.
Caveat: The three-to-four maximum is the source's recommendation, not a measured benchmark.
Caveat: The example is a redesign illustration, not a reported conversion result.

Tags: email-lifecycle, email-design, conversion-optimization, campaign-production, product-selection, deliverability
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Build reusable universal blocks for footer and repeated email sections
Use when: Setting up an ESP template system or updating a footer/category block across past and future campaigns.
- Build the section once (commonly the footer with category links and social icons) inside the ESP.
- Save it as a universal/reusable block rather than rebuilding it per campaign.
- Insert the universal block into every campaign and flow email that needs it.
- When a change is needed — e.g. adding a product category — edit the universal block once and it updates across all emails using it, instead of editing each campaign.
- Also export the footer slice from design files so the block has consistent imagery.
Caveat: Only sections that should be identical everywhere belong in a universal block; campaign-specific content should stay local.
Caveat: Feature naming and behavior vary by ESP — confirm in your platform's current docs.

Tags: email-lifecycle, klaviyo, templates, campaign-production, workflow, retention
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Use the four segmentation types to decide what to build first
Use when: Planning a store's segmentation structure or assigning messages to different customer groups.
- Behavioral: group by actions — recent purchasers, frequent site visitors, or product viewers who didn't buy — useful for triggering personalized emails.
- Demographic: group by age, gender or location — useful for regional promotions or demographic-specific collections (e.g. fashion lines).
- Engagement-level: group by how people interact with your emails — frequent openers, rare openers, and those who haven't opened in a while.
- Purchase history: group by past purchases, total spend or purchase frequency — useful for recommending similar products or loyalty offers.
- Map each planned campaign, flow or offer to the segment type that carries the right intent, then build only those segments.
Caveat: Types overlap in practice; the point is choosing the right logic per message, not using all four everywhere.

Tags: email-lifecycle, segmentation, customer-research, retention, personalization
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Build engaged segments across 30/60/90/120-day windows including website activity
Use when: Deciding who receives regular campaigns, or building the audience logic for retention and reactivation.
- Start with the condition that the person can receive email marketing so suppressed profiles are excluded.
- Add conditions (using OR between engagement events): placed order at least once, started checkout at least once, added to cart at least once, viewed product at least once, active on site at least once — all within the window (the source uses 120 days as the base).
- The source includes website activity alongside email opens/clicks because someone may ignore emails but still browse the brand.
- Optionally create a second version using email metrics only (opened email or clicked email in the window) if you want email-specific engagement.
- Clone the 120-day segment and change the window to 90, 60 and 30 days rather than rebuilding from scratch; add 14/7 or 180/365-day versions as needed.
- Expect segment computation to run in the background; you can leave the page while the ESP processes it.
Caveat: The 30/60/90/120 ladder is a source recommendation, not a settled standard.
Caveat: Segments may be auto-moved to inactive after a period (the source mentions ~45 days in Klaviyo) and require reactivation.

Tags: email-lifecycle, segmentation, klaviyo, retention, measurement, campaign-production
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Build buyer, non-buyer and repeat-buyer segments for tailored messaging
Use when: Planning campaigns and flows that treat new, repeat and never-purchased customers differently.
- All buyers: person can receive email marketing AND placed order at least once over all time.
- First-time buyers: clone the buyers segment and set placed order equals 1 over all time.
- 2x buyers: placed order equals 2 over all time; 3x+ (VIP candidates): placed order at least 3 over all time.
- Non-buyers: placed order 0 times over all time — this list-only, never-purchased group should get different campaigns and flows than repeat buyers because their mindset differs.
- Use these groups to size your customer base (how many buyers, first-timers, repeat buyers, never-bought) and to target appropriate offers.
Caveat: Cloning and editing one base segment is faster than building each from scratch.
Caveat: Thresholds (e.g. 3+ = VIP candidate) are starting points, not fixed definitions.

Tags: email-lifecycle, segmentation, klaviyo, retention, personalization, measurement
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Build abandonment and window-shopper segments for targeted recovery campaigns
Use when: Designing cart/checkout abandonment campaigns and browser-targeting flows.
- Abandoners: person can receive email marketing AND (started checkout at least once in last 90 days OR added to cart at least once in last 90 days) AND placed order 0 times in last 90 days.
- Send this group a specific recovery campaign, e.g. a final-chance offer.
- Window shoppers: (viewed product at least twice in last 30 days OR active on site at least twice in last 30 days OR clicked an email twice in last 30 days) AND placed order 0 times overall AND person can receive email marketing.
- Adjust the 'twice' threshold up or down based on your traffic volume and check the resulting segment size before building the flow.
- Give each segment its own tailored flow rather than one generic abandoned-browse email.
Caveat: The 90-day and 30-day windows and the 'twice' threshold are source defaults to test against your own data, not benchmarks.

Tags: email-lifecycle, segmentation, klaviyo, cart-abandonment, retention, conversion-optimization
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Define VIP segments by purchase count or spend relative to AOV
Use when: Setting up loyalty or VIP targeting, or deciding which customers get premium treatment.
- Start with person can receive email marketing.
- Add a purchase-count condition (the source's example: placed order at least 4 times over all time) OR a revenue condition (e.g. revenue at least $200 over all time where the revenue metric is available from the store integration).
- Set the revenue threshold as a multiple of AOV — the source suggests roughly 4x AOV as a base (AOV $50 → $200 minimum).
- Adjust the multiple (some brands treat 2x AOV or two purchases as VIP) and decide whether to use all-time or a trailing period such as one year.
- Use the VIP segment for loyalty rewards or premium offers.
Caveat: The 4x AOV figure is the source's suggested starting point, explicitly described as not set in stone and brand-dependent.
Caveat: The revenue condition requires a connected store integration; without it, only purchase-count logic is available.

Tags: email-lifecycle, segmentation, klaviyo, retention, loyalty, pricing, measurement
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Build unengaged segments, then suppress or exclude them
Use when: List hygiene, deliverability protection and building a sunset/re-engagement flow.
- Person can receive email marketing AND placed order 0, started checkout 0, added to cart 0 and viewed product 0 times in the window. Include all website metrics — the source notes that 'active on site' sometimes fails to fire, so redundant events prevent false positives.
- Add email metrics: opened email 0 times AND clicked email 0 times in the window.
- Add a 'received at least N emails' condition so people had a chance to engage. The source suggests at least 6 emails in the window if you send roughly three campaigns a week; treat this as trial-and-error and check segment size.
- Clone the 120-day version and change windows to 90, 60, 30, 180 and 365 days. For the 365-day version the source uses email-only metrics — e.g. 0 opens and 0 clicks in 365 days with at least ~12 emails received — as a strict clean-up list.
- To act on it, use the ESP's 'suppress current members' option on the segment rather than exporting/importing CSVs, and use the unengaged segment as the trigger for a sunset flow.
Caveat: The six-email and window values are tuning parameters, not universal thresholds.
Caveat: Suppressing is irreversible for future sends; review the segment contents before suppressing.
Caveat: Do not exclude soft bouncers immediately — see the bounce segment approach.

Tags: email-lifecycle, segmentation, klaviyo, deliverability, retention, list-hygiene, sunset-flow
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Create bounced-email and spam-complaint segments and exclude them by default
Use when: Protecting sender reputation and cleaning your sending list in the ESP.
- Spam complaints: person can receive email marketing AND person has marked email as spam at least once over all time. Exclude this segment from all campaigns by default and suppress them.
- Hard bounces: bounced email at least once over all time where bounce type equals hard — suppress immediately.
- Soft bounces: bounced email at least 4 times over all time where bounce type equals soft — tolerate a few because inboxes can be temporarily full, but exclude after repeated soft bounces.
- Instead of suppressing daily by hand, add these segments to your campaigns' default exclusion list; suppress only when you want them gone for good.
- Note the bounce-type and spam-marked conditions require the relevant integration/event data to be available in the account.
Caveat: The 4x soft-bounce threshold is the source's example; tune to your list.
Caveat: Suppression removes the profile from future sends; exclusions are reversible — choose per intent.

Tags: email-lifecycle, segmentation, klaviyo, deliverability, list-hygiene, retention
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Split subject line and preview text to stay readable on mobile
Use when: Writing campaign subject lines and preheaders for a store's promotions or content sends.
- Treat the subject line's only job as getting the open; it must create curiosity or intrigue and stand out in a crowded inbox.
- Treat the preview text as a second subject line — many brands skip or waste it by focusing only on the subject line.
- Follow up on the subject line's promise in the preview text and tease the content without lying; a high open rate from a broken promise leads to spam complaints or unsubscribes.
- Avoid full sentences: use a few words in the subject line and a few in the preview text. Because most opens happen on mobile, a long subject line is cut off — split one long idea between the two fields.
- Do not promise in subject/preview what the email doesn't deliver.
Caveat: The segment cuts off after listing the email's headline; exact character limits are not specified in the source.
Caveat: Open rates are not the only goal — delivering the promise protects sender reputation.

Tags: email-lifecycle, email-copywriting, subject-lines, mobile-optimization, conversion-optimization
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Write email headlines as outcomes, not features
Use when: Writing the hero/header copy for a product or promotional campaign email.
- Make the headline the first thing readers see in the header section, so it carries the hook.
- Translate features into outcomes. The source's Apple examples: '1,000 songs in your pocket' (iPod) resonates more than the storage spec, 'it's all screen' (iPhone X) and 'full screen ahead' (Apple Watch).
- Ask what the reader gets, not what the product has, and phrase the headline that way.
- In the Dollar Shave Club example the headline was the offer itself — 20% off shower products — because it is immediately clear what to expect and grabs attention.
- Keep it short enough to survive mobile rendering in the header block.
Caveat: The Apple and Dollar Shave Club examples are illustrations of the principle, not performance benchmarks.

Tags: email-lifecycle, email-copywriting, product-page, conversion-optimization, positioning
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Apply reading-level, brevity and one-message rules to email body copy
Use when: Drafting or editing campaign body copy and product-block descriptions.
- Write at approximately a fifth-grade reading level — the source cites marketing research that this is easiest to understand — and check drafts with a readability tool such as Hemingway.
- Use the tool as a guide, not an absolute: keep the brand's tone and voice.
- Read the copy aloud and delete fluff; the source finds most drafts can lose about 20–30% of words once spoken.
- Focus each email on one thing. Ten emails about one benefit is more digestible than one email covering many things; short attention spans mean multiple messages are forgotten.
- Make every sentence pull the reader to the next one, so the copy flows naturally toward the CTA.
- Keep sentences short and snappy, and use tools like Grammarly to catch spelling/grammar errors that look unprofessional.
Caveat: The fifth-grade and 20–30% figures come from the source's cited research and experience; treat as heuristics.
Caveat: Readability scores can conflict with brand voice — balance them.

Tags: email-lifecycle, email-copywriting, conversion-optimization, content-creation
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Do audience research before writing, and use copy frameworks as invisible scaffolding
Use when: Preparing to write a campaign or flow sequence for a specific customer group.
- Before writing, research the target audience: pain points, what makes them happy, what they want to hear from you, what makes them tick. The source estimates roughly 80% research and 20% writing, especially early on.
- Write copy that answers 'would I read my own newsletter?' — make it interesting to the recipient, not just about the product.
- Use frameworks as reference points: AIDA (attention, interest, desire, action) or PAS (pain, agitate, solve). The source notes these are rarely applied literally in modern email.
- Check completed copy against the frameworks — good copy almost always fits one of them naturally.
- Show personality and sound human; the source observes top brands all inject personality rather than generic lines.
- Use humor where it fits the brand and audience — the source suggests it works especially well for younger (roughly under-30) audiences — and use contractions ('you're', 'you'd', 'they've') to sound like talking to a friend.
- Provide value above all: frameworks, active voice and readability only finish copy that is genuinely useful.
Caveat: The 80/20 research-to-writing split is the source's heuristic, not a measured benchmark.
Caveat: Humor and voice must match the brand and audience; it is not universal.

Tags: email-lifecycle, email-copywriting, customer-research, positioning, content-creation
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Cut copy: easy words, active voice, no fluff
Use when: Final editing pass on campaign copy, PDP copy or ad copy before scheduling.
- Read the draft aloud, then remove words and sentences that add nothing — target cutting roughly 20–30%.
- Delete adverbs.
- Convert passive voice to active voice.
- Avoid alliteration and complicated/rare words; keep language simple.
- Use contractions (they've, you'd, you're) to make copy conversational.
- Confirm the remaining copy still conveys one clear message and leads to the CTA.
Caveat: This is the source's editing checklist, not a guaranteed conversion improvement.
Caveat: Brand tone may justify keeping some stylistic language — judge against the audience.

Tags: email-lifecycle, email-copywriting, conversion-optimization, content-creation
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Prioritize A/B tests by recipient volume, not by ease
Use when: Deciding which email or flow to test next when you can only run a limited number of experiments per month on your store's lifecycle program.
- Map each flow and campaign to its monthly recipient volume and revenue contribution before choosing a test target.
- Rank the biggest levers first: welcome series, abandoned checkout, abandoned cart, and post-purchase/winback flows, plus the first 2-3 emails of each.
- Within those, test high-recipient emails before testing minor flows that only reach tens of recipients per month.
- Treat improvements on a 20-recipient flow as marginal: it may lift that flow's conversion, but it will not move overall store revenue materially.
- Allocate test slots so at least the majority of experiments land on the top flows and top campaign sends.
Caveat: The source frames this as advice for general ecommerce stores, especially under roughly $100K/month; large multi-million-dollar stores can afford to chase smaller levers.
Caveat: Recipient volume ranking depends on your own account data, not a fixed universal list.

Tags: email-lifecycle, experiment-design, retention, flows, measurement, conversion-optimization
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Test send time against place order rate, not open rate
Use when: Scheduling campaign sends and deciding whether to trust Klaviyo's Smart Send Time or run your own send-time test.
- Create an A/B test on the campaign and choose 'test send time' rather than relying only on Smart Send Time.
- Pick two clearly different times (for example 7 a.m. versus 7 p.m.) to start with a meaningful contrast.
- In the test settings, set the winning metric to place order rate, not click rate and definitely not open rate, since revenue and placed orders are the KPIs that matter.
- Keep size distribution at 100 and track links separately per variation so you can attribute results correctly.
- Run the comparison across roughly 5-10 campaigns before concluding; one campaign is effectively zero data.
- Once a winner emerges, narrow the test (for example 7 a.m. versus 11 a.m., then 11 a.m. versus 2 p.m.) to pinpoint the best window.
Caveat: The source states it has repeatedly seen the best open-rate time differ from the best place-order time, but notes this is not universal across all brands.
Caveat: The 5-10 campaign range is a heuristic that depends on audience size and revenue level, not a fixed rule.

Tags: email-lifecycle, experiment-design, send-time, measurement, campaigns, conversion-optimization, klaviyo
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Test content structure in campaigns, not just subject lines
Use when: Planning campaign experiments and choosing which content variables to vary in your store's promotional and evergreen sends.
- Set up an A/B test on content rather than only on subject lines, since subject-line results on a one-time campaign cannot be reused elsewhere.
- Version A: original email with product blocks. Version B: same email without product blocks. Compare results.
- Run a second variant type on sitewide sales: one version highlighting three bestsellers versus one version highlighting product categories or new arrivals.
- Set the winning metric to place order rate where possible; the source notes Klaviyo does not allow place order rate for subject-line tests, so click rate is the next-best option there.
- Run each content test across multiple campaigns before drawing conclusions and before applying the pattern to flows.
Caveat: Subject-line tests on one-off campaigns yield data you cannot act on elsewhere; the source recommends deprioritizing them for that reason.
Caveat: Place order rate is not selectable as a winner metric for all test types in Klaviyo; verify the current interface.

Tags: email-lifecycle, experiment-design, campaigns, content-strategy, merchandising, conversion-optimization, klaviyo
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Use 50/50 manual distribution for email A/B tests
Use when: Configuring test settings for subject line or content A/B tests in campaigns and flows.
- In the test settings, turn off 'automatically chosen distribution' and set the split manually to 50/50.
- Expect automatic distribution to shift more sends toward whichever variant Klaviyo currently favors, which can bias the comparison.
- Accept the tradeoff: manual 50/50 requires you to check and analyze the test yourself, which the source's agency prefers because it wants full control.
- If you lack time to monitor tests, the source says enabling automatic distribution is acceptable.
- For winner selection, the default is click rate; configure to open rate if needed, but note place order rate is not available for subject-line tests, and click rate is the better fallback.
- Leave the winner-selection method on 'test by statistical significance' or choose the time limit; alternatively switch it off and pick the winner manually.
- Write a note on the test explaining your hypothesis so you can interpret it later.
Caveat: These are the source's stated preferences from agency practice, not universal requirements.
Caveat: Automatic distribution behavior and test-setting labels in Klaviyo may change; verify the current interface.

Tags: email-lifecycle, experiment-design, klaviyo, measurement, campaigns, flows
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## A/B test abandonment flow timing with conditional splits
Use when: Optimizing abandoned cart, abandoned checkout, or browse abandonment flow timing to lift placed orders while watching spam complaint rate.
- Add a conditional split at the top of the flow and set the condition to a random sample of 50%.
- Set the 'yes' path to one delay (for example 2 hours) and the 'no' path to another (for example 1 hour) so the difference at the start is meaningful.
- Duplicate every email so each path carries the full sequence rather than rejoining after the first email; the source prefers this because email 1 may perform worse at the longer delay while emails 2-3 perform better, and you want the full picture.
- After results come in, narrow the comparison (for example test 2 hours versus 3 hours) to pinpoint the ideal delay.
- Monitor spam complaint rate alongside placed order rate, since timing changes affect both.
- Repeat the same conditional-split approach for browse abandonment, starting with a wider gap such as 1 hour versus 3 hours.
Caveat: Splitting every email into two paths multiplies maintenance work; the source prefers it for full-sequence visibility, but it is a tradeoff.
Caveat: Ideal delays are store-specific; the 1/2/3/4-hour values are illustrative test values, not benchmarks.

Tags: email-lifecycle, flows, abandoned-cart, browse-abandonment, experiment-design, klaviyo, conversion-optimization
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Flow subject lines are worth testing, campaign subject lines usually are not
Use when: Deciding where to spend subject-line testing effort across your welcome, abandonment, and post-purchase flows versus one-time campaigns.
- For flow emails, go to the email you want to test, hit 'create a test', and enter an alternative subject line (for example 'did you see something you liked' versus 'oops you forgot something').
- Run the subject-line test on flows because they send continuously, so a winning line keeps producing results over time.
- For campaigns, treat subject-line testing as low-value: the send is one-time, so a winner gives you little actionable information afterward.
- Instead of campaign subject lines, direct campaign test effort toward send times and content variations that inform your flows and future campaigns.
- Still set the winning metric responsibly: use click rate when place order rate is not selectable.
Caveat: This is the source's stated preference and a judgment about actionability, not a claim that subject lines never matter.
Caveat: Klaviyo's test-creation flow and available metrics may change; verify the current interface.

Tags: email-lifecycle, subject-lines, flows, campaigns, experiment-design, klaviyo
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Skip CTA-color split tests at small store scale
Use when: Deciding how to allocate limited testing capacity for a small or mid-size store's email program, signup forms, or above-the-fold email content.
- Recognize that CTA color tests usually show meaningful differences only for very large senders, in the source's experience brands doing multiple millions per month with very large audiences.
- For stores under about $100K/month, redirect that test slot to bigger levers: flow timing, content structure, and first-email variants in top flows.
- If you do test above-the-fold email content, test headlines and calls to action rather than only button color.
- Note that color tests are technically possible and can produce a difference; the source's position is that the gain is minor relative to effort at small scale.
Caveat: The ~$100K/month threshold and the 'millions per month' scale are the source's heuristics based on agency observation, not measured benchmarks.
Caveat: A large-audience brand may legitimately find color tests worthwhile.

Tags: email-lifecycle, experiment-design, conversion-optimization, cta, measurement, small-business
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Write email copy that earns attention through value, not cleverness alone
Use when: Drafting campaign or flow email copy for product launches, promos, or category sales that need to fit your brand voice.
- Lead with value: the source frames value as more than half the battle, with tone and formatting tips finishing the job.
- Make the headline immediately clear about what the reader gets, for example a percent-off product sale, so attention is grabbed by clarity as well as offers.
- Write body copy in the brand's voice rather than generic promo language; a line that is a little edgy or funny fits a brand like Dollar Shave Club, whereas a generic 'hurry, selling out fast' line can convert but fits worse.
- Call out the discount code explicitly and pair it with a clear call-to-action button such as 'save now'.
- Insert recommended product blocks, then close with body copy that continues the same on-brand tone rather than reverting to generic urgency.
- Keep sentences short and snappy as a finishing pass after the value and voice are right.
Caveat: The Dollar Shave Club example is the source's constructed demo, not a measured performance case study.
Caveat: Brand-voice edginess is not a universal rule; a generic line may still convert.

Tags: email-lifecycle, copywriting, campaigns, brand-voice, content-strategy, offer-design
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Structure promo emails around headline, code, CTA, products, and closing copy
Use when: Building the layout and copy order for a discount or category-sale email in your store's campaign calendar.
- Open with an attention-grabbing headline that makes the offer immediately clear, such as '20% off shower products'.
- Follow with body copy written in your brand's tone so the email reads as a fit for your audience rather than a template.
- State the discount code prominently and place a clear call-to-action button, for example 'save now'.
- Add 'recommended for you' product blocks so recipients can act on the offer without leaving the email's context.
- Close with additional body copy that reinforces the sale and repeats the code, keeping the same voice throughout.
- Compare your draft against the generic alternative (plain percent-off plus urgency) to check whether your version is genuinely more on-brand.
Caveat: This layout comes from the source's demo campaign, not from a documented A/B test result.
Caveat: A generic urgency line may perform acceptably; brand fit is the differentiator the source argues for.

Tags: email-lifecycle, copywriting, campaigns, email-design, product-page, offer-design, merchandising
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Track place order rate as the primary email KPI hierarchy
Use when: Choosing the winning metric for any email A/B test or deciding which send-time or content variant to adopt in your store.
- Set revenue and place order rate as the top-level KPIs for email decisions.
- Rank click rate second and open rate last, since higher opens do not reliably translate to more orders.
- When comparing send times or content variants, prefer the option producing more placed orders even if its open rate is lower.
- Where a platform does not allow place order rate as the winner metric (the source notes this limitation for subject-line tests in Klaviyo), fall back to click rate rather than open rate.
- Check the platform's current metric options before configuring, since available selections can change.
Caveat: The source reports that the best open-rate time often differs from the best place-order time, but this is agency observation rather than a universal law.
Caveat: Metric availability in Klaviyo varies by test type.

Tags: email-lifecycle, measurement, conversion-optimization, experiment-design, klaviyo, retention
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Sequence send-time tests from wide contrast to narrow pinpointing
Use when: Establishing a default campaign send time for your store instead of relying on a single Smart Send Time suggestion.
- Start with a wide contrast between the two test times so any real difference is detectable.
- Let the test run across several campaigns (the source suggests roughly 5-10) rather than judging from one send.
- Take the winning hour and pair it against a neighboring hour in the next round, for example 7 a.m. versus 11 a.m.
- Repeat with a progressively tighter bracket, for example 11 a.m. versus 2 p.m., converging on the best window.
- Apply the resulting send time as your default, but keep monitoring place order rate rather than assuming the optimum is fixed.
Caveat: The number of campaigns needed scales with audience size and revenue in the source's framing; 5-10 is a heuristic.
Caveat: Results are brand-specific and may shift with seasonality or list changes.

Tags: email-lifecycle, send-time, experiment-design, campaigns, measurement, klaviyo
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx

---

## Expect to customize templates to your brand instead of copying them
Use when: Rolling out a new email program or onboarding templates into your store and setting realistic expectations for iteration.
- Treat any provided template as a starting point, not a finished system; the source states not every template will fit a brand's needs.
- Determine through testing which flows retarget your customers best, which email design engages them most, and which campaigns they want to see.
- Accept trial and error as part of finding the right system, strategy, design, and flows for your specific store.
- Prioritize iteration on high-recipient flows and sends so your trial and error produces compounding learning.
Caveat: The source promotes a paid service with a stated 20% revenue guarantee in 60 days; such claims are the presenter's marketing and are not independent evidence.
Caveat: No specific template or design is guaranteed to fit a given store.

Tags: email-lifecycle, flows, email-design, experiment-design, retention, template
Source: _Klaviyo Email Marketing FULL COURSE 2025.docx