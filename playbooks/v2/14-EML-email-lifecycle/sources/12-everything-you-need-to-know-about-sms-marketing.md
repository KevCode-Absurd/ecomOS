# Everything You Need to Know About SMS Marketing in 2025

source_id: 1AMtIBd_PeRP4tnLvitYS4vmRri5QKpz4  |  folder: /14-EML-email-lifecycle  |  cards: 14  |  words: 4,200  |  type: transcript (solo YouTube video, auto-transcribed; "clavio" = Klaviyo, "postcript" = Postscript)

credibility: A single presenter who runs SMS for ecommerce clients (unnamed in the text). Sells consulting to brands above $50,000 a month and offers a free SMS "swipe file" doc and a longer pop-up video as lead magnets. Evidence: own client results ("tens of millions" of SMS sent, "millions of data points"), one unnamed client's 30-day revenue, and "I've tested this" claims. No sample sizes, test lengths, control groups or dates for any test. No studies. Opinion and own-client data only.
date signals: Title says 2025. Names Klaviyo, Attentive and Postscript. Shopify checkout opt-in. No platform versions, no RCS, no AI features beyond a dismissal of vendor "AI" pitches. File modified 20 Sep 2026. Costs, segment rules and vendor features are a 2025 snapshot.

Scope note: the source is written for US senders ("pretty much everybody in the US"). It says nothing about consent law, opt-out wording, quiet-hour law, sender registration or carrier rules. Any brand, including a non-US one, must check local rules before acting. `[web check: SMS consent, opt-out text, quiet-hour and sender registration rules in each country the brand sends to]`

## 1. What this source is for

It helps an operator set up a basic SMS program for a store: pick a platform, grow the list with a pop-up and a checkout checkbox, launch 5 core flows, and plan a month of campaigns at 1 to 2 sends a week. Its most useful part is the cost logic: SMS is paid per segment, so length, emojis and images all change cost. It is a beginner-to-intermediate baseline. It is thin on compliance, segmentation detail, flow timing and actual copy (the flow templates were shown on screen and are not in the text).

## 2. Principles

1. **SMS is an owned, high-attention channel.** Source says texts have an average open rate of 98%, so almost every subscriber sees a send. Subscribers "know, like and trust you" (they bought or gave their number), so they are not cold. An ad platform cannot shut the list down. Condition: 98% is a cited figure, not measured by the source; SMS opens are not tracked like email opens. Treat as framing, not a benchmark. `[web check: source of the 98% SMS open rate figure]` [bb9581c6a1d8]
2. **SMS is more intrusive than email, so send less.** A text lands in a main phone app with a ding and a vibration. Email can take 4 to 5 sends a week without backlash; SMS cannot. SMS unsubscribe rates are "way higher" than email and rise the more you send (source's own tests). Condition: presenter's tests, no numbers given for unsubscribe rates. `[needs brand data: SMS unsubscribe rate per send and by weekly cadence]` [bf9cd4297ad9]
3. **Only send important messages on SMS.** Launches, drops, special offers, product highlights, back in stock, flash sales, big announcements. Keep SMS "mostly transactional". Nurture, education and social proof go to email. Source says nurture and social-proof SMS gave poor ROI and higher unsubscribes in its tests. [bcc0f86cebc6] [bf9cd4297ad9]
4. **Every SMS costs real money, so spend must earn its return.** SMS costs far more than email ("a fraction of a cent" per email). So any extra cost (image, extra segment) must bring matching extra revenue. Source: it is "very, very rare" for an image or extra text to double revenue. Condition: presenter's experience; costs depend on provider and country. `[needs brand data: current per-segment SMS and MMS rates on the brand's plan]` [f89925ebf6ad] [fa8b517af050]
5. **Focus on when and what you send, not clever copy.** Because messages must be short and bare, results come from timing, offer and topic, not intricate copywriting. [fa8b517af050]
6. **Automations are set once and run in the background.** Set up, check in, optimize, let run. Flows are for quick, high-ROI touches; weekly campaigns do the retention work. [71d9f81273f0] [bb9581c6a1d8]
7. **No platform is clearly best; consolidate.** Main SMS platforms do much the same at similar prices. If the brand uses Klaviyo for email, use Klaviyo for SMS so all marketing sits in 1 place. Attentive and Postscript are "solid" too. Vendor AI features are "marginal" and rarely used. Condition: presenter opinion at time of recording. [aa2a2140c1a0]
8. **People will not hand over a phone number for nothing.** "It's not a charity." Give a discount, giveaway or free guide. A discount costs some margin on the first order; source says a strong email and SMS back end earns it back. Condition: assumes the brand has that back end. `[needs brand data: first-order margin after signup discount, repeat rate of discount signups]` [775acf1e29be]
9. **Pop-ups are the most effective list-growth method; checkout opt-in is the background method.** Run both. [9e19056dd462] [171673d6f3de]
10. **Restock messages combine proof and urgency.** A sold-out item was popular; a restock may sell out again. Source says these "always do well". Condition: see section 9 on the source's advice to send restock messages for items that were not out of stock. [3f1ec5d057e8]
11. **Send time has no universal answer; test it.** Every audience is different. Source gives safe starting windows (section 4). [5a21fae6ffd5]

## 3. Procedures

### 3.1 Set up the platform
1. Check if the current email platform offers SMS. If it is Klaviyo, source recommends staying on Klaviyo. [aa2a2140c1a0]
2. If not, pick Attentive, Postscript or similar. Do not choose on AI feature claims. Prices are "relatively the same". `[web check: current pricing and features for Klaviyo SMS, Attentive, Postscript]` [aa2a2140c1a0]
3. Follow the vendor's own setup guide. Source says it takes minutes and gives no steps. The platform gives you a phone number, tracking and automations. `[verify UI]` [aa2a2140c1a0]
4. Connect the platform to the store (Shopify or other) so flow triggers fire. `[verify UI]` [71d9f81273f0]

### 3.2 Grow the list: checkout opt-in
1. On the Shopify checkout (purchase) page, add a checkbox asking the buyer to agree to marketing messages. `[verify UI]` [9e19056dd462]
2. Keep it on for all clients and all buyers so the list grows with every order. [9e19056dd462]
3. Confirm opt-ins sync to the right SMS list in the SMS platform. (Card step; source does not say how.) `[verify UI]` [9e19056dd462]
4. Check consent rules for each market before relying on a checkbox as SMS consent. `[web check: whether a checkout checkbox counts as valid SMS marketing consent in each market]` [9e19056dd462]

### 3.3 Grow the list: pop-up form
1. Measure the current pop-up signup rate as a baseline. Source says most brands it audits convert about 2% to 3% of visitors. `[needs brand data: current pop-up signup rate, sessions, form views]` [171673d6f3de]
2. Trigger: time delay of 6 to 10 seconds after page load. Source uses 6 seconds. Do not use scroll or exit-intent triggers; source says they "can misfire". Do not wait 30 seconds; few visitors stay that long. `[verify UI]` [3545eb404e90]
3. Offer: something worth a phone number. Discount is most common; giveaway or free guide also work. [775acf1e29be]
4. Step 1 of the form: say what they get, ask for email only. Use as few words as possible. [775acf1e29be]
5. Step 2: ask for the phone number with copy tied to the offer, for example "finish signing up by entering your phone number" or "finish signing up to get your discount". Source claims this "works 10 times better" than asking for everything in 1 step. [775acf1e29be]
6. Do not ask for birthday, product interests or other fields in the same step. [775acf1e29be]
7. Track form signup rate and site conversion rate after launch. Target from source: 8% to 10% of visitors (about 3x the 2% to 3% baseline). The site conversion check is a card step; the source only says the pop-up must not "harm your website conversions". `[needs brand data: site conversion rate before and after pop-up change, split by mobile and desktop]` [171673d6f3de] [3545eb404e90]
8. The source refers to a separate 1-hour video and its setup in Klaviyo for the full build. That content is not in this text. [171673d6f3de]

### 3.4 Launch the 5 core flows
Use the platform's templates where they exist. Source says keep flows light; "you really don't need too much". Source gives no delays between messages and no message counts except for Welcome. [71d9f81273f0]

| Flow | Trigger (as source describes) | Messages | Content (source's words) |
|---|---|---|---|
| Welcome | New SMS signup | 2 to 3 SMS | Deliver the discount or whatever was promised |
| Browse abandonment | Viewed a product and left | not given | "Hey, where'd you go? You can finish your order here" |
| Cart abandonment | Added to cart, did not buy | not given | Remind them to come back, "finish your order right here" with link |
| Checkout abandonment | Started checkout, did not buy | not given | Same reminder with link |
| Win-back | Bought "months ago", has not come back | not given | "Let them know we're thinking about them"; discount optional |

- Source showed "copy and paste" templates on screen for all 5 flows and said they are tested "over millions of data points". The copy is not in the text. The source's free doc also has it; not in the library. `[needs brand data: brand's own flow copy and past flow results]` [71d9f81273f0]
- Win-back window is "months ago" with no number. `[needs brand data: typical days between 1st and 2nd order, to set the win-back trigger]` [71d9f81273f0]
- Flow timing (delay after trigger, gap between messages) is not given. `[verify UI]` for template defaults. [71d9f81273f0]

### 3.5 Write each SMS
1. Keep it under 160 characters, with 1 simple point and a link. Source: 161 characters bills as 2 messages, and each further 160 adds another. [fa8b517af050]
2. Avoid emojis. Source says each uses the equivalent of 35 to 50 characters. The cards correct this: any emoji or Unicode character can switch the whole message to Unicode, dropping the single-segment limit from 160 to 70 characters. [fa8b517af050] [54ec55400d45]
3. Preview the fully rendered message with personalization, link and opt-out text, and read the platform's segment counter before sending. (Card step, not in the source text.) `[verify UI]` [fa8b517af050] [54ec55400d45]
4. Use plain SMS by default. Use MMS (image or GIF) only when the image must earn 2 to 3 times the revenue of the text-only send, because MMS costs 2 to 3 times more. [f89925ebf6ad]
5. If an extra segment or an image is being considered, compare net contribution (revenue minus send cost) of the short version against the longer one. (Card step.) `[needs brand data: revenue per send and cost per send for SMS vs MMS and 1 vs 2 segments]` [fa8b517af050] [f89925ebf6ad]

### 3.6 Plan a month of campaigns
Source's worked example: an eight-figure brand in October. [3f1ec5d057e8]
1. List the month's main events first. Example: Halloween product launch on 10 Oct; Halloween flash sale 30 to 31 Oct.
2. Product launch, 2 to 3 messages:
   - Optional teaser 1 to 2 days before (8 or 9 Oct): "limited time item coming on 10 Oct, be ready". Source says teasers "really help" launch sales.
   - Launch day (10 Oct): announcement. Likely the biggest sales driver.
   - About a week later (15 Oct): reminder or urgency, for example "low on stock".
3. Flash sale, 2 messages: launch message on day 1 (30 Oct), "last chance, expiring in a few hours" on the last day (31 Oct). Back-to-back days are fine for big events.
4. Find gaps of more than a week with no SMS. Fill with 2 to 3 extra campaigns. Example fillers: social media giveaway driving to Instagram (4 Oct); restock of a popular item (23 Oct).
5. Check the total against 1 to 2 sends a week. Source says this October plan is "perfect" and needs nothing more. [bf9cd4297ad9] [3f1ec5d057e8]

Resulting example calendar (source's dates):

| Date | Send | Type |
|---|---|---|
| 4 Oct | Social media giveaway | Filler |
| 8 or 9 Oct | Launch teaser (optional) | Launch |
| 10 Oct | Launch announcement | Launch |
| 15 Oct | Reminder or low-stock urgency | Launch |
| 23 Oct | Restock of a popular item | Filler |
| 30 Oct | Flash sale launch | Sale |
| 31 Oct | Flash sale last chance | Sale |

That is 6 to 7 sends in 31 days, about 1.5 a week, with 2 back-to-back pairs (9 and 10 Oct if the teaser runs on 9 Oct; 30 and 31 Oct).

### 3.7 Pick send times
1. Start with 11:00 a.m. to 2:00 p.m. (after the morning, lunch at work). This is the "safest" window and where most messages should go. [5a21fae6ffd5]
2. Test 4:00 p.m. to 5:00 p.m. as a second window. [5a21fae6ffd5]
3. Do not send before 10:00 a.m. or after 7:30 p.m. [5a21fae6ffd5]
4. Last-chance messages can go at 6:00 to 7:00 p.m. with a short deadline, for example "4 hours left". Not later. [5a21fae6ffd5]
5. Test times on your own list; track clicks and revenue by send hour over several sends before fixing a default. Handle time zones per the platform. (Tracking and time-zone steps are from the card.) `[needs brand data: clicks and revenue by send hour]` `[verify UI]` [5a21fae6ffd5]

## 4. Rules, thresholds and numbers

| Rule | Number or threshold | Condition | Source's basis | Card |
|---|---|---|---|---|
| SMS campaign frequency | 1 a week default; 2 a week "every now and again" | Campaigns, not flows. Big events may go back to back | Presenter's tests; unsubscribes rose with volume | [bf9cd4297ad9] |
| Email frequency for comparison | 4 to 5 a week without backlash (also "4 times a week") | Email, not SMS | Opinion | [bf9cd4297ad9] |
| Single SMS length | 160 characters | GSM text, no emoji. 161 bills as 2 | Presenter | [fa8b517af050] |
| Unicode or emoji SMS length | 70 characters per single segment | Any emoji or Unicode character; multipart limits differ | Card correction (Klaviyo help article), not the source | [54ec55400d45] |
| Emoji cost (source's claim) | 35 to 50 characters each | Contradicted by cards; see section 9 | Presenter says he does not know "the science" | [fa8b517af050] |
| MMS cost | 2 to 3x SMS | Use only if image earns 2 to 3x revenue | Presenter; rate cards differ | [f89925ebf6ad] |
| Email cost | "a fraction of a cent" per send | For comparison | Presenter | [f89925ebf6ad] |
| Pop-up trigger | 6 to 10 seconds after load (source uses 6) | Time delay, not scroll or exit intent | Presenter tests | [3545eb404e90] |
| Pop-up delay to avoid | 30 seconds | Too few visitors stay | Opinion | [3545eb404e90] |
| Pop-up signup rate, typical | 2% to 3% of visitors | Brands the presenter audits | Own audits | [171673d6f3de] |
| Pop-up signup rate, target | 8% to 10% of visitors | After trigger, offer, short copy, 2-step fixes | Own client work; target, not promise | [171673d6f3de] |
| 2-step vs 1-step form | "10 times better" | Email first, then phone | Presenter claim, no data | [775acf1e29be] |
| Welcome flow length | 2 to 3 SMS | Delivers signup offer | Presenter | [71d9f81273f0] |
| Core flows | 5 | Welcome, browse, cart, checkout, win-back | Presenter | [71d9f81273f0] |
| Launch messages | 2 to 3 (teaser optional, launch, reminder about 1 week later) | Big product launch | Example calendar | [3f1ec5d057e8] |
| Flash sale messages | 2 (launch, last chance) | Back-to-back days fine | Example calendar | [3f1ec5d057e8] |
| Filler campaigns | 2 to 3 a month | Gaps over 1 week with no SMS | Example calendar | [3f1ec5d057e8] |
| Safe send window | 11:00 a.m. to 2:00 p.m. | Starting default; test | Presenter tests | [5a21fae6ffd5] |
| Second send window | 4:00 to 5:00 p.m. | Starting point; test | Presenter | [5a21fae6ffd5] |
| No-send hours | Before 10:00 a.m., after 7:30 p.m. | Brand preference, not a legal rule | Presenter | [5a21fae6ffd5] |
| Last-chance time | 6:00 to 7:00 p.m., e.g. "4 hours left" | Expiring offers | Presenter | [5a21fae6ffd5] |
| SMS open rate | 98% average | Cited, not measured | Unsourced | [bb9581c6a1d8] |
| Consulting fit | Brands above $50,000 a month | Sales pitch, not a rule | Pitch | none |

## 5. Diagnostics and checks

| Check | How | Good | Bad | Next step | Card |
|---|---|---|---|---|---|
| Campaign cadence | Count SMS campaigns per week over the last 4 to 8 weeks | 1 a week, sometimes 2 | 3 or more most weeks | Cut non-urgent sends; move nurture to email | [bf9cd4297ad9] |
| Unsubscribe trend | Unsub rate per send, compared with weekly volume | Flat as volume holds | Rising with more sends | Lower cadence; segment sends | [bf9cd4297ad9] |
| Campaign mix | Tag each send as launch, sale, restock, announcement, nurture, social proof | Mostly transactional or urgent | Nurture or social proof on SMS | Move those to email | [bcc0f86cebc6] |
| Segment count | Platform segment counter on the rendered message `[verify UI]` | 1 segment | 2 or more without a revenue case | Cut copy; remove emojis | [fa8b517af050] [54ec55400d45] |
| Encoding | Look for emojis, curly quotes or other Unicode in the rendered text | Plain GSM text | Unicode, 70-character limit | Remove the character or accept the cost | [54ec55400d45] |
| MMS use | Share of sends with images; revenue per send vs SMS sends | MMS only on essential visual drops | MMS on routine sends without 2 to 3x revenue | Switch to SMS | [f89925ebf6ad] |
| Pop-up signup rate | New subscribers ÷ visitors (card also says form viewers) | 8% to 10% | 2% to 3% | Fix trigger, offer, copy, 2-step flow | [171673d6f3de] |
| Pop-up trigger | Read form display settings `[verify UI]` | 6 to 10 second delay | Scroll, exit intent or 30 seconds | Set a time delay | [3545eb404e90] |
| Form fields | Count fields per step | Email only in step 1; phone only in step 2 | Birthday, interests or phone in step 1 | Split into 2 steps | [775acf1e29be] |
| Site conversion after pop-up change | Compare before and after, by device | No drop | Drop | Test a longer delay or a softer format | [3545eb404e90] [171673d6f3de] |
| Checkout opt-in | Look at checkout for a marketing checkbox; check sync to SMS list `[verify UI]` | Present and syncing | Missing | Add it | [9e19056dd462] |
| Flow coverage | List live SMS flows | All 5 core flows live | Gaps | Build from templates | [71d9f81273f0] |
| Monthly calendar gaps | Map sends on a calendar | No gap over 1 week, no week over 2 | Long silence then a burst | Add filler (giveaway, restock) or trim | [3f1ec5d057e8] |
| Send times | Clicks and revenue by send hour | Most sends 11 a.m. to 2 p.m., none before 10 a.m. or after 7:30 p.m. | Early morning or late night sends | Reschedule and test | [5a21fae6ffd5] |
| SMS revenue share | SMS-attributed revenue ÷ total revenue, flows vs campaigns | Brand's own trend | Using case numbers as targets | Track own data | [bb9581c6a1d8] |

`[needs brand data: SMS sends, unsubscribes, clicks, attributed revenue and cost by send, for all checks above]`

## 6. Tools, settings and named features

| Tool or feature | Used for | Notes |
|---|---|---|
| Klaviyo (email and SMS) | Recommended SMS platform if already used for email | Consolidation. Presenter's own setup videos are on Klaviyo. `[verify UI]` [aa2a2140c1a0] |
| Attentive | Alternative SMS platform | "Solid". Helped pick the presenter's 30-message swipe file. [aa2a2140c1a0] |
| Postscript | Alternative SMS platform | "Solid". [aa2a2140c1a0] |
| Shopify checkout | Marketing opt-in checkbox | `[verify UI]` for where the SMS consent setting lives. [9e19056dd462] |
| Pop-up form, time-delay trigger | List growth | 6 to 10 seconds. `[verify UI]` [3545eb404e90] |
| Multi-step (2-step) form | Email then phone | `[verify UI]` [775acf1e29be] |
| Flow templates | Welcome, browse, cart, checkout, win-back | Platform templates exist for base flows. `[verify UI]` [71d9f81273f0] |
| Segment counter / message preview | Cost control | Named in cards, not in the source. `[verify UI]` [fa8b517af050] |
| SMS vs MMS | Text only vs text plus image or GIF | MMS 2 to 3x cost. `[web check: current SMS and MMS rates per country on the brand's platform]` [f89925ebf6ad] |
| Vendor "AI" features | Not recommended as a selection reason | Presenter calls them marginal. [aa2a2140c1a0] |

## 7. Examples and case results

All are examples from the presenter's clients, not promises.

- **Unnamed client, last 30 days:** $750,000 from SMS, about 20% of the brand's total revenue. Flows alone: $422,000 in the same 30 days, with average click rates of 15%. No list size, attribution window or cost given. [bb9581c6a1d8]
- **Pop-up audits:** most brands audited convert 2% to 3%; the presenter's method reaches 8% to 10% ("tripling" signups). No count of brands. [171673d6f3de]
- **2-step form:** email then phone "works 10 times better" than asking for all fields at once. No data shown. [775acf1e29be]
- **Nurture and social proof on SMS:** "usually don't get a great ROI" and higher unsubscribes in the presenter's tests. No numbers. [bcc0f86cebc6]
- **October calendar:** mock plan for an eight-figure brand (section 3.6). Hypothetical, not a real result. [3f1ec5d057e8]
- **Flow copy:** example lines "Hey, where'd you go? You can finish your order here"; win-back "let them know we're thinking about them". Full templates not in the text. [71d9f81273f0]
- **Pop-up copy:** "Do you want this discount? Enter your email address", then "Finish signing up by entering your phone number". [775acf1e29be]
- **Last chance copy:** "4 hours left", sent 6 to 7 p.m. [5a21fae6ffd5]
- **Launch teaser copy (paraphrase):** "There's a limited time item coming to the store on October 10th, be ready." [3f1ec5d057e8]

## 8. Mistakes the source warns about

1. Sending SMS as often as email (4 to 5 a week). Raises unsubscribes on a list that was hard to build. Fix: 1 a week, 2 at most. [bf9cd4297ad9]
2. Sending nurture, education or social proof by SMS. Fix: keep those in email. [bcc0f86cebc6]
3. Going 1 character over 160. It doubles cost. Fix: cut copy to 1 segment. [fa8b517af050]
4. Using emojis to add visual interest. Fix: plain text. [fa8b517af050] [54ec55400d45]
5. Adding images (MMS) by default. Costs 2 to 3x and rarely pays back. Fix: text only unless the image is essential. [f89925ebf6ad]
6. Choosing a platform on AI feature pitches. Fix: consolidate with the email tool. [aa2a2140c1a0]
7. Pop-up on scroll or exit-intent triggers (can misfire) or a 30-second delay (few people see it). Fix: 6 to 10 second delay. [3545eb404e90]
8. Pop-up with no real offer. Fix: discount, giveaway or free guide. [775acf1e29be]
9. Asking for many fields at once (birthday, interests, phone with email). Fix: 2 steps, email then phone. [775acf1e29be]
10. Wordy pop-ups. Fix: as few words as possible. [775acf1e29be]
11. Building too many flows or too many flow messages. Fix: 5 core flows, kept short. [71d9f81273f0]
12. Sending before 10 a.m. or after 7:30 p.m., or a last-chance message too late. Fix: 11 a.m. to 2 p.m. default; last chance by 6 to 7 p.m. [5a21fae6ffd5]
13. Leaving gaps of over a week with no SMS, then bursts. Fix: add filler campaigns to keep 1 to 2 a week. [3f1ec5d057e8]
14. Skipping the checkout opt-in. Fix: always have the checkbox. [9e19056dd462]

## 9. Caveats, conflicts and what is missing

**Conflicts inside this source's cards**
- **Emoji cost.** Source says each emoji uses 35 to 50 characters and admits it does not know "the science". Cards [fa8b517af050] and [54ec55400d45] correct this: one emoji or Unicode character can switch the whole message to Unicode, cutting the single-segment limit from 160 to 70 characters. Multipart segment sizes also differ from 160. Agent should use the card version and the platform's segment counter. `[web check: current GSM-7 and Unicode segment sizes in the brand's SMS platform help docs]`
- **"Each 160 characters" billing.** Source says cost steps every 160 characters. The card says multipart limits differ, so a long message may take more segments than length ÷ 160 suggests. Use the counter. [fa8b517af050]
- **Restock messages for items that were not out of stock.** Source says "even if something isn't necessarily out of stock you can still send a message for it". Card [3f1ec5d057e8] flags this may misrepresent inventory. It conflicts with the ecomOS rule "no invented claims". Agent should only send restock messages for items that truly restocked. `[web check: false scarcity and consumer protection rules in each market]`
- **Manufactured importance.** Source suggests angles "that make something seem important like a back in stock message". Same caveat as above. [bcc0f86cebc6]

**Conflicts with other sources in this folder**
- **Frequency.** This source: 1 a week, rarely 2, because unsubscribes rise with volume. Mini playbook 05 (Postscript's chief customer officer) says more sends usually mean more revenue as long as unsubscribes do not rise, and cites a holdout where doubling from 1 to 2 texts a week beat the holdout. Both rest on thin evidence (presenter tests vs one vendor test). Postscript gains from more sends; this presenter gives no numbers. Agent should treat 1 a week as a safe start, then test higher cadence with a holdout and watch unsubscribes. `[needs brand data: revenue and unsubscribes by cadence]` [bf9cd4297ad9]
- **98% open rate** is widely repeated in the industry but SMS opens are not tracked the way email opens are. Do not report it as a brand metric. [bb9581c6a1d8]

**Conflicts with common ecommerce advice**
- Many operators and platforms use exit-intent pop-ups, often alongside a timed pop-up. This source rejects exit intent as prone to misfire. Test before dropping it. [3545eb404e90]
- The source's "no sends before 10 a.m. or after 7:30 p.m." is a brand preference. It is not a legal quiet-hours rule. Legal quiet hours, where they exist, differ by country and state. `[web check: legal quiet hours for marketing texts in each market]` [5a21fae6ffd5]
- Common advice is to use a separate consent step and required disclosure text for SMS. The source treats one checkout checkbox as enough. `[web check: SMS consent requirements, e.g. separate SMS checkbox and disclosure]` [9e19056dd462]

**What is missing**
- Compliance: no consent wording, opt-out keywords (for example STOP), disclosure text, double opt-in, sender registration, or country rules. This is the biggest gap. `[web check: SMS compliance rules for each market]`
- Flow timing: no delay after trigger and no gap between messages for any flow. No message count for browse, cart, checkout or win-back. No win-back trigger window beyond "months ago".
- Flow copy: templates were shown on screen and in an external doc; neither is in the text.
- Segmentation: named as a way to reduce annoyance, but no segments are defined. Also no guidance on excluding recent buyers from abandonment or campaign sends.
- Measurement: no attribution window, no incrementality test, no cost-per-send or profit per send figures. The 15% flow click rate and $422,000 have no base.
- Overlap between SMS and email flows (who gets which channel, and when) is not covered.
- Pop-up offer size: "a discount" with no percentage or value.
- Market: US framing throughout. Unknown fit for non-US brands. `[web check: SMS costs, deliverability and rules outside the US]`

## 10. Card index

- bf9cd4297ad9  Set SMS campaign frequency to 1–2 sends per week maximum
- fa8b517af050  Budget SMS copy using the rendered segment count
- 54ec55400d45  Check SMS encoding and segment cost before sending
- f89925ebf6ad  Reserve MMS images for campaigns where they earn 2–3x the SMS revenue
- aa2a2140c1a0  Choose an SMS platform that consolidates with your existing email stack
- 9e19056dd462  Grow the SMS list with a post-purchase opt-in checkbox
- 3545eb404e90  Delay the SMS/email pop-up trigger to 6–10 seconds after page load
- 775acf1e29be  Build a two-step micro-commitment pop-up: email first, then phone
- 171673d6f3de  Aim pop-up forms at 8–10% conversion vs the 2–3% baseline
- 71d9f81273f0  Launch five core SMS automation flows before heavy campaign sending
- bcc0f86cebc6  Keep SMS campaigns transactional, urgent, or announcement-based, not nurture
- 3f1ec5d057e8  Model the SMS month around launches and flash sales, then fill the gaps
- 5a21fae6ffd5  Test SMS send times; default to 11 a.m.–2 p.m. and 4–5 p.m.
- bb9581c6a1d8  Treat the SMS list as a channel asset for revenue you control
