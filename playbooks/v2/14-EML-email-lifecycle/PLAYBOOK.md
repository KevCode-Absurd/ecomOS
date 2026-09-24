# 14-EML email lifecycle playbook

version: 2.0-draft  |  date: 2026-09-24  |  sources: 13  |  cards: 578  |  built from: sources/*.md

## 0. How to use this playbook

This is the base layer for the lifecycle agent: email, SMS and (where a brand has an app) push. It runs list growth, flows, campaigns, segments, deliverability and the monthly review. It is built from 13 mini playbooks. Every rule cites the mini playbook numbers (01 to 13) and card ids. Cards are in `data/library-v3/cards.json`.

Which sections to load for which task:

| Task | Load |
|---|---|
| Audit an account (flows, pop-ups, deliverability) | 3.1, 3.4 to 3.13, 3.18, 5, 6 |
| Build or fix a pop-up | 3.2, 3.3, 4.P3, 4.P4, 5.2, 7.1 to 7.3 |
| Build or fix a flow | 3.4 to 3.13, 4.P5 to 4.P11, 4.P16, 5.1 |
| Build segments | 3.14, 4.P12 |
| Plan a month of campaigns | 3.15, 3.16, 4.P13 to 4.P15, 4.P19, 5.4, 9 |
| Write or design an email | 3.16, 3.17, 4.P18, 4.P26, 8 |
| Fix deliverability | 3.18, 4.P2, 4.P17, 5.3, 7.4 to 7.7 |
| Run SMS | 3.19, 4.P20 to 4.P24, 5.5, 7.8 to 7.12 |
| Monthly review | 3.20, 4.P25, 4.P27, 5.6, 6 |
| Any conflict between sources | 7 |

Before acting the agent must fetch:

1. From the brand record: AOV, gross margin, discount policy, ship-to countries, product categories, founder name and voice, guarantees, shipping times, approved claims, reviews tagged by objection, repeat-purchase intervals. Every claim in an email must match the brand record. If the record does not hold a claim, the agent does not make it.
2. From the data layer (Klaviyo, Shopify, Metabase): list size, opt-in rate by device, flow and campaign revenue, opens excluding Apple opens, clicks, placed order rate, revenue per recipient, unsubscribe, spam and bounce rates, days between orders (median and mean), order-count distribution.
3. From the web, tagged `[web check]`: consent and quiet-hour law per country, Gmail and Yahoo sender rules, Klaviyo UI defaults, SMS and RCS pricing and availability. Section 10 lists all of them.

Tags: `[verify UI]` marks platform steps that can change. `[needs brand data: x]` marks a value the agent must pull before acting. `[web check: x]` marks something to check live.

Rules that start with "ecomOS" override any source. They are in 3.21.

## 1. Scope and outcomes

Covers: list growth and pop-ups; consent and opt-in; the core flows (welcome, site abandonment, browse abandonment, cart abandonment, checkout abandonment, post-purchase, replenishment, win-back, sunset, back in stock, review request, birthday); segment definitions; campaign cadence, content pillars and calendar; copy structure and subject lines; email design; deliverability (authentication, warm-up, list hygiene, limits); SMS (consent, quiet hours, frequency, flows, cost, RCS and iMessage); metrics and the monthly review.

Does not cover: paid acquisition (the ads folders), landing page and site conversion (the site folder), offer design beyond the signup offer (the offers folder), loyalty program design (only the emails that promote it), reviews platform setup (only the request email), creative production for ads. The sources point paid media to the Meta folder and site builds to the landing page folder.

Business measures this domain moves:

- Email-attributed share of store revenue. Source 03 sets 30%+ as a target; source 10 claims 30% to 50%; source 04 clients show 34% to 52%. All are Klaviyo-attributed, not incremental. [465d3381b2a7] [46a5333c2392] [0944381047ee]
- SMS-attributed share: 5% to 15% (11), 10% to 20% (09), about 20% (12 example). [76ea7acfff13] [51b9472f8d06] [bb9581c6a1d8]
- List growth rate (opt-in rate x traffic), welcome flow conversion, repeat purchase rate, revenue per recipient, unsubscribe and spam rates.

## 2. Inputs the agent needs

| Input | From where | Required or optional | Why |
|---|---|---|---|
| AOV and gross margin | brand record | required | Offer type (% vs $), discount depth, whether MMS or a flow discount pays |
| Discount policy (who may get a code, max depth, frequency) | brand record | required | Cart, browse, win-back and welcome branches; campaign promo cap |
| Ship-to countries and legal markets | brand record | required | Consent wording, double opt-in, SMS quiet hours, pop-up location targeting |
| Founder name, photo, voice, willingness to sign emails | brand record | required | Plain-text founder emails in welcome, cart, post-purchase, win-back |
| Approved claims, guarantees, shipping times, returns policy | brand record | required | Risk-reversal blocks; every claim must match |
| Reviews and testimonials tagged by objection | brand record or reviews app | required | Review blocks that answer objections |
| Bestsellers by first-order share; product categories and collections | data layer (Shopify) | required | Welcome email 3, product feeds, interest segments |
| Median and mean days between orders; days of supply per product | data layer | required | Win-back and replenishment timing |
| Order-count and spend distribution | data layer | required | VIP definition |
| Current opt-in rate by device, form views, submits | data layer (Klaviyo forms) | required | Pop-up baseline and test sizing |
| Flow and campaign revenue, opens (Apple opens excluded), clicks, placed order rate, RPR, unsubscribes, spam, bounces | data layer (Klaviyo) | required | Every diagnostic and threshold in sections 5 and 6 |
| Traffic by source and country; site conversion rate | data layer (GA4, Shopify) | required | Flow revenue vs traffic; pop-up tests on site CVR |
| List size, engaged share, inbox provider mix | data layer | required | Cadence, segment windows, deliverability by provider |
| SMS program status, platform, per-message cost, iPhone share | brand record and SMS platform | required for SMS | Cost math, RCS and iMessage fit |
| Support reply capacity and hours | brand record | required | Founder emails promise replies; conversational SMS needs staff |
| Subscription, loyalty, reviews apps in use | brand record | optional | Integration-triggered flows |
| Content library (blogs, videos, social posts) | brand record | optional | Campaign calendar fill |
| Competitor emails and ads | inspiration and web | optional | Layout and mood only; never copy text |
| Current Klaviyo UI, Gmail and Yahoo sender rules, SMS law per country, RCS availability | web | required before build | Section 10 |
| Brand owner's view on hidden close buttons, insecurity-led copy, cadence ceiling | user | required | Sections 7.2 and 3.21 |

## 3. Decision rules

Each rule states the rule, the condition, the supporting mini playbooks, conflicts, and card ids. "Sources 01, 02" means mini playbooks 01 and 02. Where only 1 source supports a rule, it says so.

### 3.1 Program order and revenue structure

**R1. Build in dependency order: tracking and authentication, list growth, core flows, campaigns, segments, testing, then AI and personalisation.** Condition: a new or under-built account. A mature account with a large list but weak capture may start at list growth. Sources 02, 03, 04. [93e33dec853f] [5a08594d02a9] [1d17eaa95e56] [b8acdbab97a3]

**R2. Fix the basics before advanced work.** Test: is the pop-up above 3% (01) or 9% (03), is there a real cart flow of 6 or more emails, does the welcome flow have more than 1 email. If not, fix these first. Do not build cross-sell splits or hyper-segmentation before that. Sources 01, 02. [05d68e6eea8b] [b88c44dec23c] [64a2c2916004]

**R3. Flows and campaigns should each bring roughly half of email revenue.** 40/60 either way is fine. Flows at 30% means the flows need work. Source 02 gives 40% to 70% for flows. Condition: a heuristic, not a target; check the attribution window first. Sources 01, 02. [0de6758fd7b5] [8dcc18667354] [700ad4cccb44]

**R4. Email should drive at least 30% of total store revenue when the program is built.** Condition: Klaviyo-attributed revenue with transactional emails, bot clicks and Apple opens excluded (R181). Depends on the attribution window. Source 03 only, backed by client examples in 04 and 10. [465d3381b2a7] [0944381047ee] [46a5333c2392] `[needs brand data: email-attributed share and attribution window]`

**R5. Map the customer journey before building.** Ad or post, pop-up, welcome or abandonment flow, campaigns, first order, post-purchase, next order. Each touchpoint must match what the person already knows. A first-order discount to a 5-order customer is the failure case. Source 03. [a084662e8ae4]

**R6. Flows capture demand; campaigns create it.** If you send the same campaign every week, it should be a flow. Do not let campaigns plus welcome, cart and post-purchase emails hit the same person within 24 hours (R38, R109). Sources 02, 03. [7a1145af87dc] [24b8079fe1fe]

### 3.2 List growth and pop-ups

**R7. The offer is the biggest lever on opt-in rate.** Order of leverage: offer, then behaviour (trigger, steps), then copy, then design. A bad offer in a beautiful form still gets a bad rate; hacks move a bad-offer form from about 2% to 2.2%. Sources 01, 02, 03, 04, 12. [9eebdb581427] [60f8b169fd9a] [aa555d450d5a] [4c956b5e96a1] [ea0cb89619eb] [72945bee8a3a] [775acf1e29be]

**R8. Target an opt-in rate of 8% to 12% of site traffic.** Typical untested forms convert 1% to 4% (01: 1 to 3; 02: 1 to 3; 04: 2 to 4; 12: 2 to 3; 09: 5 to 6 on forms he reviews). Source 03 says above 9% and calls Klaviyo's 3% "excellent" badge not excellent. Sources 01, 02, 03, 04, 09, 12. [1c9b788208ca] [aa555d450d5a] [ea0cb89619eb] [40691f40d94c] [171673d6f3de] [51b9472f8d06] `[needs brand data: current opt-in rate by device]`

**R9. Choose percent off when AOV is under about $100 to $200 and dollars off above that.** 01: percent under $100, dollars over $100. 04: at $200 or more, dollars tend to win ($20 off vs 10% off at $200 AOV). 03: set the dollar amount at about 10% of AOV. Minimum that works: 10% off; 5% only for very high AOV (02, 04). Test it. Sources 01, 02, 03, 04. [60f8b169fd9a] [aa555d450d5a] [ea0cb89619eb] [72945bee8a3a] `[needs brand data: AOV, margin]`

**R10. Judge a signup offer on 4 numbers together, not on opt-in rate alone: opt-in rate, total signups, welcome flow placed order rate and revenue, and margin.** A higher opt-in rate with a collapsed welcome conversion may lose money. 04 example: a new offer had lower welcome CVR but higher AOV and revenue, so it won. Source 05 adds: test pop-up changes on full-site conversion rate, because a pop-up can lift opt-ins and lower checkout. Sources 02, 04, 05. [aa555d450d5a] [0590112c25d0] [c09dafafbc67] [1282cefafb08]

**R11. Ask for 1 input per step: email first, phone on a separate later step.** Never email and phone on 1 screen. No name, birthday or interests in step 1. Sources 01, 02, 03, 04, 09, 11, 12. [7ea9228eeda8] [2a3063dcd723] [9622afcc8844] [39aa68c94680] [9b9305f19394] [775acf1e29be] [75893d2892aa]

**R12. Put a micro-commitment step before the email field, and test it.** A yes/no question ("Do you want 10% off your first order?" with "Yes please" / "No thanks"), a 1-question quiz, or a scratch-off. 02: wins "in most cases" across 40+ brands. 03: wins "9 times out of 10". 04: most brands get a lift, some do better without. 09: quiz first "is what works in 2026". Condition: always A/B test per device. Sources 01, 02, 03, 04, 09. [92626e4998da] [e912865caec2] [4be0db20360f] [52d1b13d3d6e] [d80edbbaaf50] [75893d2892aa]

**R13. Gamified steps (spin to win, scratch-off) convert but carry a cost.** 01 calls spin to win "tacky" and "converts like crazy". 02: one brand went 11% to 14% with a scratch-off. Both tools show decoy prizes that never land. ecomOS: do not show prizes that cannot be won (R199). Sources 01, 02. [0419dcd84c79] [7da3ea843dc6] `[web check: local promotion and consumer rules on decoy prizes]`

**R14. Trigger the pop-up on a time delay of 4 to 12 seconds, starting at 4 to 6.** 01: 4 to 12, start at 4. 02: 6, test 4 to 12. 04: 4 to 10, default 6. 11 and 12: 6 to 10. Do not show on page load (01, 02, 04, 12) and do not wait 30 seconds (01, 12). Conflict: source 03 shows the form immediately and only tests a 5-second delay or 30% scroll. See 7.3. Sources 01, 02, 04, 11, 12 against 03. [e5cbaa0f3a12] [c5e1f30dd58d] [d124c18b882e] [3545eb404e90] [4d0639885e1a]

**R15. Add scroll depth and desktop exit intent as OR conditions; keep exit intent off on mobile.** 02: scroll 60% (test 30 to 90), exit intent desktop only. 04: scroll 50 to 60% (test 40 to 80), exit intent desktop, off on mobile. 01 and 12: no exit intent at all ("misfires"). Condition: set the rule logic to OR (any condition fires), never AND. Sources 02, 04; against 01, 12. [c5e1f30dd58d] [d124c18b882e] [e5cbaa0f3a12] [3545eb404e90]

**R16. Re-show after a close after 3 to 5 days.** Klaviyo default 5; 02 sets 3; 04 uses 3 to 5 by revisit frequency. Never show again after a submit. Sources 01, 02, 03, 04. [e5cbaa0f3a12] [c5e1f30dd58d] [d124c18b882e] [4d0639885e1a]

**R17. Build separate mobile and desktop forms.** Mobile: no image, larger text and buttons, no exit intent. Desktop: side image (right side "typically works best" in 01; 03 says no image usually wins). Conflict: 03 says 1 form for both is enough unless they convert differently. Sources 01, 02, 04 against 03. [d076884d7359] [c2e8c7484a70] [f932973235fb] [4bb4a381c989] [ef89709e3516]

**R18. Keep the form big, the copy short and the offer the largest element.** At least 75% of the screen (01), under 10 words (01), offer in the headline, no "sign up" or "subscribe" wording, benefit-word CTA in first person ("Claim my discount"), no sub-headline about "exclusive offers". Sources 01, 02, 04. [ff4c8404916f] [9622afcc8844] [0590112c25d0] [72945bee8a3a] [9adb06995af6]

**R19. Do not show the pop-up to existing profiles, on cart, checkout or wholesale pages, or to countries you do not ship to.** Sources 02, 03, 04. [a877dc6c99dd] [4d0639885e1a] [d124c18b882e] `[needs brand data: ship-to countries, wholesale URLs]`

**R20. Turn the teaser on.** 02: it raises opt-in rate and total subscribers. 03 and 04: on. Conflict: 01 leaves it off because it gets in the way. Use a circle or corner shape on mobile so it does not collide with chat or loyalty widgets. Sources 02, 03, 04 against 01. [53f37df1584e] [f7f5d18ebe32] [4d0639885e1a]

**R21. Withhold the discount code from the success page and send it in welcome email 1.** Reason given: the first email then earns an open and click, which helps sender reputation. Success copy: "Your code is on its way. Check your inbox. Not there in 5 minutes? Check spam." Sources 02, 03, 04 (02 admits it is a "50/50 debate" with a "pretty minimal" conversion loss). Conflict: 01 shows the code or tells the user to check their phone. See 7.2. [1f8be190a019] [8e47ceff852b] [d319ea40cf4e]

**R22. Compress every form image; no image on mobile.** Slow forms lose submits. Sources 01, 02, 04. [8b8c3454e9e7] [7ea9228eeda8]

**R23. Run pop-up tests in leverage order: offer, form type and first step, close mechanics, delay, image, copy, colours.** Cadence: 01 weekly; 02 every 2 to 4 weeks; 03 monthly even at 10%. Sample: 3,000 to 5,000 impressions per variant or 15 days, whichever is longer (02); manual 50/50 weight and manual winner, never automatic on low volume (02, 04). Judge delay tests on total submits, not rate (01). Sources 01, 02, 03, 04. [b5dc319521e1] [0590112c25d0] [00de729163a8] [e8e1adc8fefe] [ea0cb89619eb]

**R24. Use the other 3 growth methods too: checkout opt-in checkbox, signup pages for social and giveaways, footer and inline embeds.** Give each import or giveaway its own list and its own welcome, not the 10% off welcome. Sources 01, 03, 12. [3d97f72a2969] [d7c5cedcb3dd] [9e19056dd462]

**R25. Collect phone numbers from day 1 even with no SMS program.** The SMS list only earns as much as its size. Sources 03, 09. [51b9472f8d06] [4be0db20360f]

### 3.3 Consent and opt-in

**R26. Single opt-in is the sources' default for email; check the market first.** 02, 03, 04 all use single opt-in and rely on engaged segments plus a sunset flow. 02 says double opt-in "massively" cuts subscribers; Aaliyah recommends double opt-in for Postscript and Attentive. Double opt-in is expected or required in some EU markets. See 7.1. Sources 02, 03, 04. [33c8d10a4bf5] [8c1b383c08cf] `[web check: double opt-in rules per market]`

**R27. Keep the consent text on the form.** 02 and 04 delete it for US-only stores. ecomOS: keep it legible on every form (R197). Source 01 shrinks the SMS consent text to size 8; do not copy that. Sources 02, 04; override in 3.21. [39aa68c94680] [72945bee8a3a] [397f14a8dca9]

**R28. SMS consent must be explicit and separate from email consent.** Never text anyone who did not opt in to SMS. A checkout checkbox may not count as SMS consent in every market. Sources 09, 11, 12. [ccceb9ed6344] [ee1a31c09fcc] [9e19056dd462] `[web check: SMS consent wording, separate checkbox, disclosure text per country]`

**R29. In the EU add "because person subscribed" to segment conditions, or keep 2 segment versions.** Someone can be emailable without marketing consent (checkout entry). Source 02. [516248e6ac94] `[web check: GDPR consent rules for the brand's markets]`

**R30. Make unsubscribing easy and honour it at once.** Dormant subscribers who cannot leave hurt deliverability for everyone. Klaviyo blocks sends without an unsubscribe link. Gmail one-click unsubscribe is live (02). Sources 02, 03, 06. [c1faaf881fc4] [5fde08efd3f8] [91d6fd433f58] `[web check: Gmail and Yahoo one-click unsubscribe requirement]`

### 3.4 Flow rules that apply to every flow

**R31. Every flow has a trigger, entry filters, exit filters and a re-entry rule.** Filters with "since starting this flow" act as exits: placed order, checkout started, added to cart, viewed product, as the flow's stage requires. Filters are checked before every email, so a buyer between email 1 and 2 never gets email 2. Sources 02, 03, 04. [07f1b027ac4e] [dfc548f661d2] [9da5ac313720]

**R32. No 2 flows may run for the same person at the same journey stage.** Cart flow filters out checkout starters; browse flow filters out cart adders; site flow filters out product viewers. Sources 01, 02, 03, 04. [b6389565ed83] [5ad3da1bdb3a] [909e75c1eb8d] [9da5ac313720]

**R33. Smart sending OFF on every flow email; ON for campaigns.** Flows carry high-intent revenue and must not be skipped because a campaign went out. Klaviyo default window 16 hours. Condition: total pressure then rises; see 7.4. Sources 02, 04; 03 keeps it on at account level and turns it off per campaign for launches. [4d6f11a9f443] [58bdfe185e63] [b837f7435caf] [a891648996f4] [1ce671434e00]

**R34. UTM tracking ON on every flow and campaign email.** Sources 02, 03, 04. [8796c9f1ffa6] [b837f7435caf]

**R35. The later the journey stage, the shorter the first delay.** Site abandonment 1 to 4 hours; browse 30 minutes to 2 hours; cart 15 minutes to 2 hours; checkout as early as 15 minutes. Klaviyo defaults (cart 4 hours, welcome 3 days, post-purchase 1 day) are too slow. Sources 01, 02, 03, 04. [c83fa5e0d0d6] [0528a2003316] [d94eb68e5e18] [3638d8afef7a] [fbfeb91636ec]

**R36. Hold discounts back in flows.** Reminder, founder check-in, social proof and objection handling come first; the discount comes late (email 4 or 5), only with a real deadline (48 hours then 24 hours). Past buyers get a founder support email, not the acquisition discount, or a smaller one if margins allow (02: 10% non-buyers, 5% returning). Exception: the welcome code is already promised, so every welcome email reminds it. Sources 01, 02, 03, 04. [f0dfe6920491] [2fd76c2c2442] [bdbde349add0] [4085ce710e47] [5aad4467fa44] [f147a186a98d]

**R37. Urgency must be real.** Use unique dynamic codes or codes that truly expire. "WELCOME10 expires tonight" is a fake deadline. Sources 02, 04, 08. [cefa2905adfd] [a69de45ff438] [8ae593fcc226]

**R38. Plain-text founder emails close sequences.** Used as welcome 1B and the last welcome email, cart email 2 and the last cart email, post-purchase email 1 and 6, win-back and the whole sunset flow. Needs a real founder name and a reply inbox with a reply promise the brand can keep ("within 24 hours"). Sources 01, 02, 04. [287733c58cdd] [63691cee89e1] [a69de45ff438] [38c0bd0fee2b] `[needs brand data: founder name, support reply capacity]`

**R39. Do not use Klaviyo template content; use templates only to inherit triggers, filters and dynamic product tables.** Sources 03, 04. [07f1b027ac4e] [a0bdafa6ea40] [fd7d4c80cdb7]

**R40. Test email 1 of the highest-volume flow first, and test delay before content.** A 2% lift on email 6 of a flow with 50 recipients a month does not matter. Sources 01, 02, 04. [700ad4cccb44] [f64d1327c5bf] [c61791a6cbeb]

### 3.5 Welcome flow

**R41. Trigger: added to the list the pop-up writes to.** Re-check whenever a form or list is added; a mismatched list means the flow never fires. Re-entry off. Sources 01, 02, 03, 04. [2d5485f41fc3] [4d6f11a9f443] [ef1cb30f5c95] [6e89698da8b5]

**R42. Filter: placed order 0 times over all time.** So past buyers who re-subscribe do not get the acquisition discount. 04 adds checkout started 0 and added to cart 0 since starting this flow. Caveat (01 card): for high-frequency consumables an all-time exclusion may be wrong. Sources 02, 03, 04; 01 uses "since starting this flow" by default. [4d6f11a9f443] [07f1b027ac4e] [dfc548f661d2] [3b8a84dc1d94]

**R43. Front-load the flow into the first 72 hours.** Day 0 is the highest-converting day; after day 3 only "a bare minimum" remains (02, client screenshots). 02: email 1A at 0 hours, 1B at +8 hours, email 2 at 24 hours, then daily. 03 and 04: email 1 immediate, then 1-day gaps (04: 0, 1, 1, 2, 2, 2, 1 days). 01: 1 to 2 day gaps over 7 to 14 days; high AOV ($5,000) can run over 2 months. Klaviyo's 3-day default is too slow (all). Sources 02, 03, 04; 01 is looser. [f2c3f6895ad4] [580319f842a5] [65d6a163c4ce] [6e89698da8b5] [5b03b18152ec]

**R44. Length: 6 to 8 emails, each with 1 angle.** Merged order: (1) deliver the code above the fold plus 1 to 3 bestsellers and trust marks; (1B) same-day plain-text founder reminder (02); (2) brand story with substance: founder, mission, quality, sourcing; (3) bestsellers, max 3 to 5, why each; (4) objections and us vs them, code deadline 48 hours; (5) reviews that name an objection, 24 hours left; (6) last chance; (7) plain-text founder extension of 24 hours. Then optional evergreen campaign winners (01, 02). Sources 01, 02, 03, 04. [2d5485f41fc3] [1fef69d7fc18] [6ff7df41c99b] [5c60bad74418] [974086eb7dfa] [089beec94d13] [4240a92f17f1] [7ee979f51388] [681426ed9a3a] [d50bbcaf474a] [7f27679135bf] [cefa2905adfd] [38077a826b12] [18ddf0ee7ebf] [71218ab504b8] [debbcf824284]

**R45. Remind the code in every welcome email, and keep each email short.** 01: under about 100 words, readable in 3 seconds. Sources 01, 03, 04. [b0ac0c5d9d9b] [65d6a163c4ce] [6e89698da8b5]

**R46. Welcome conversion target: 10% of entrants as the floor, 20% as very good.** Sources 01, 02. [b568ff652c08] [aa555d450d5a] `[needs brand data: welcome flow placed order rate]`

**R47. Reviews in the welcome flow must name a pain point or objection.** 1 specific review beats 3 "great product" reviews. Sources 02, 04, 08. [38077a826b12] [6e89698da8b5] [6e5742c076f2]

### 3.6 Site abandonment flow

**R48. Trigger: Active on Site. Exit filters: viewed product 0, added to cart 0, checkout started 0, placed order 0, all since starting this flow. Re-entry: not in this flow in the last 30 days.** No Klaviyo template exists; build it (04). Sources 01, 04. [75b807a7abce] [b0f7b82a2bb3]

**R49. First delay 1 to 4 hours; 1 email.** 01: 2 to 4 hours, and a test where 4 hours beat 30 minutes on placed-order rate. 02 and 04: 1 to 4 hours, test 1 vs 4. Content: a shop-assistant email ("Lost in choices? Let us point you in the right direction"), bestsellers or collections, light social proof. Goal: a product view. Sources 01, 02, 04. [75b807a7abce] [70e9cc171c68] [0528a2003316] [b0f7b82a2bb3]

**R50. Keep it on during deliverability repair.** 02 keeps site abandonment on; 01 turns it off. Prefer 02 because the flow is small and high intent. Sources 02 against 01. [df98522f016b] [e5dfe8e98a49]

### 3.7 Browse abandonment flow

**R51. Trigger: Viewed Product. Filters: added to cart 0, checkout started 0, placed order 0, all since starting this flow. Re-entry: 30 days.** The Klaviyo template lacks the added-to-cart filter; add it by hand (03, 04). On Shopify use the Shopify Added to Cart metric, not the API one (02). Sources 01, 02, 03, 04. [f0dfe6920491] [5ad3da1bdb3a] [909e75c1eb8d] [5aad4467fa44]

**R52. First delay 30 minutes to 2 hours; then 1 day between emails.** 01: 45 minutes. 02: 30 to 45 minutes up to 2 hours (default 2, demo 1). 04: test 1 vs 3 hours. Sources 01, 02, 04. [c83fa5e0d0d6] [f0dfe6920491] [5aad4467fa44]

**R53. Length 4 to 6 emails, trust before urgency.** Browse is mid-funnel persuasion, not lost-sale recovery (02). Order: (1) light reminder with the viewed item and 4 related products; (2) risk reversal and objections; (3) product-specific reviews; (4) small discount with a 48-hour deadline, or subscribe-and-save for replenishables (02 puts this at email 3); (5) plain-text 24-hour closer. Link to the product URL, not the homepage (03). Sources 01, 02, 03, 04. [d0e8f91819ba] [9d0646c87a39] [aaef1103dc77] [890a5c97d555] [8c9c22844f69] [79cdac8bb86e]

**R54. No new vs returning split in browse by default.** Browsers are low intent even if they bought before, so everyone gets the same ladder; split only if margins cannot carry any incentive to past buyers (02). Conflict: 03 branches prospects vs customers. Sources 02 against 03. [5ad3da1bdb3a] [4085ce710e47] [f147a186a98d]

### 3.8 Cart abandonment and checkout abandonment

**R55. Build 2 flows: Added to Cart and Checkout Started.** Klaviyo's "Abandoned Cart Reminder" template fires on Checkout Started, so it is a checkout flow. 01 says 90% of brands he audits lack a real cart flow. People who add to cart but never start checkout get nothing otherwise. Sources 01, 02, 03, 04. [8d43aac07129] [d962429e9e36] [d94eb68e5e18] [85117c7d0910] [fac642b0957b] [393737091e3e]

**R56. Confirm the Added to Cart metric fires before building.** 01 gives snippet install steps; 01 also says Klaviyo added it natively in September 2024; 02 says pick the Shopify Added to Cart metric, not the API one. Test with a known profile. Sources 01, 02, 04. [34204d0c3ce5] [5ad3da1bdb3a] `[web check: whether Klaviyo's Shopify integration sends Added to Cart natively or needs the onsite snippet]`

**R57. Cart flow filters: checkout started 0 since starting this flow; placed order 0 since starting this flow; not in this flow in the last X days.** Checkout flow: placed order 0 since starting this flow; not in this flow in the last X days. X: 01 and 02 use 30 days; 04 template 7, prefers 14; 03 uses 2 to 3 days for checkout because a repeat checkout shows interest. Pick X from repurchase interval: weekly consumables 7 or less, otherwise 14 to 30. Sources 01, 02, 03, 04. [b6389565ed83] [d94eb68e5e18] [85117c7d0910] [fac642b0957b] `[needs brand data: repurchase interval]`

**R58. First delay 15 minutes to 1 hour; test up to 2 to 4 hours.** 01: 30 minutes (30 to 45 best; test 1 and 4 hours). 02: 15 minutes to 1 hour; default 4 hours is "way too long". 03: test 4 vs 2 hours, shorter usually wins. 04: 30 minutes to 2 hours. Sources 01, 02, 03, 04. [815150bfedbc] [d94eb68e5e18] [fbfeb91636ec] [fac642b0957b]

**R59. Length 6 to 8 emails over about 10 days, minimum 3 for prospects.** 1 or 2 emails let buyers "off the hook" before their decision cycle ends (01). 14 to 20 emails gets complaints (04). Sources 01, 02, 03, 04. [ed0f5c1eb0f6] [f147a186a98d] [fac642b0957b]

**R60. Sequence: reminder, founder check-in, objections, product-specific proof, last chance with alternatives, then split by buyer status.** (1) 30 minutes: "You left this behind", dynamic item, risk reversal, no discount. (2) +1 day: plain-text founder check-in "did you run into any issues?" with 1 differentiator (02), or social proof (01). (3) +1 day: objections answered with USPs (price, shipping, fit, quality). (4) product-specific testimonials (01: convert better than general ones). (5) last chance, "You may also like" alternatives about day 5. (6) split placed order at least once over all time: buyers get a founder support email, no discount or a smaller one; non-buyers get a discount with 48 hours, then a plain-text 24-hour closer. Sources 01, 02, 03, 04. [e502966b22d7] [815150bfedbc] [e7a5c9132999] [962de4f96ab5] [e99b377f856f] [2fd76c2c2442] [b9c909970c5b] [bdbde349add0] [4085ce710e47]

**R61. Discount only people who never bought, or have not bought in 60 to 90 days.** 01: 60 to 90 days "depending on how averse you are". 02: 20% off in email 1 "will generate revenue but destroy margins". Sources 01, 02, 03, 04. [b9c909970c5b] [bdbde349add0] [f147a186a98d] `[needs brand data: discount policy, margin]`

**R62. The dynamic item block is the most important part; cart and checkout variables differ.** Never copy one flow's block into the other. Checkout: link every slice to `{{ event.extra.checkout_url }}` (03). Cart: link to the cart page or the item. Preview with several profiles. Sources 01, 02, 03. [c42f60fa5fca] [79cdac8bb86e] [a0bdafa6ea40] `[verify UI]`

**R63. In the checkout flow, answer checkout objections.** A shopper who saw a $10 shipping fee responds to free shipping better and cheaper than to 10% off (04). Sources 03, 04. [393737091e3e] [f147a186a98d] `[needs brand data: shipping cost, AOV]`

**R64. Split by product or collection for emails 3 and 4 where the catalogue has a few main collections.** Not 20 splits. Source 01; 04 uses trigger filters for the same effect. [962de4f96ab5] [bccb578fdd8b]

### 3.9 Post-purchase flow

**R65. Trigger: Placed Order. Filters: placed order 0 since starting this flow (a new order restarts it); cancelled order 0 since starting this flow.** Optional: exclude subscription or B2B customers to their own flow (03). Sources 02, 03, 04. [58bdfe185e63] [9f9c84a1b824] [55898f20e161]

**R66. First email 10 to 30 minutes after the order, plain text from the founder.** Shopify's order confirmation fires at once, so do not send at 0 minutes (02: 10 minutes; 04: 30 minutes). Conflict: 01 sends at 0 minutes; 03 sends 1 day later with no fixed hour and warns against fixing 9 AM. Sources 02, 04; 01 and 03 differ. [58bdfe185e63] [d4ea5342470c] [05c3a4b18253] [55898f20e161]

**R67. Split first-time vs returning at the start.** First-timers: thanks for trusting us, reassurance, what happens next, soft cross-sell PS ("add to your order in the next 24 hours"). Returning: thanks for loyalty, no acquisition offer, subscribe-and-save, loyalty, cross-sell. Sources 01, 02, 03, 04. [1911a725b087] [5956a124a134] [55898f20e161] [3da6d6371379]

**R68. Merged sequence for the first-time track.** (1) +10 to 30 minutes: founder thank-you. (2) +1 to 2 days: "your order is on its way", add-ons, reduce remorse (worst in the first 24 to 48 hours). (3) after delivery: how to get the most from the product, split by product or category; cuts returns. (4) about day 7: follow 1 social channel, 1 CTA. (5) after delivery (04: day 10): loyalty program with the benefit stated at once. (6) +3 days: review request, optional thank-you code. (7) 1 to 2 weeks after delivery: founder check-in "how did everything go?" (02: "one of the emails that generates the most revenue"). (8) optional cross-sell with a 48-hour code, then a 24-hour plain-text closer (04). Sources 01, 02, 03, 04. [05c3a4b18253] [38c0bd0fee2b] [5b7ae7297305] [5956a124a134] [0a935c9bd091] [c17894672b54] [55898f20e161] `[needs brand data: fulfilment and delivery times]`

**R69. Most repeat purchases happen within 30 days of the first order; work that window.** The first-to-second purchase is the hardest step. Sources 02, 04. [b3058403e9f8] [f6a8fc1ece5f]

**R70. Post-purchase how-to content must match what the customer bought.** Apparel may need only care instructions; technical products need guides. Sources 02, 03. [5956a124a134] [55898f20e161]

**R71. If a reviews app is connected, run the review request on its triggers and stop asking once a review event exists.** Sources 03, 04. [9ca8e23a01f3] [0a935c9bd091]

### 3.10 Replenishment flow

**R72. Time the reminder to days of supply plus delivery time, a few days before the product runs out.** 04: day 25 of a 30-day pack. 09 (SMS): 30-day supply plus 7 days delivery, send about day 35. 01: predictive "average time between orders" reminder on day 40 for a 45-day cohort. Content: "Are you running low? Reorder here." No offer at first. Sources 01, 04, 09. [b8acdbab97a3] [586799a976b3] [7b644e511db9] `[needs brand data: days of supply per product, delivery time]`

**R73. Use Klaviyo's expected date of next order as the trigger when predictive data exists.** Fire on the date, 12 PM local time, never repeat, filter placed order 0 since starting this flow. Source 03. [109f8c9de246] [6818bdf85834] `[verify UI]`

### 3.11 Win-back flow

**R74. Trigger: Placed Order plus a wait; filter placed order 0 since starting this flow.** Set the wait from the brand's own data, never Klaviyo's default (04 template 75 days; 03 says default "probably 90"). Methods: 01 and 09: 2 times the average days between orders (45 becomes 90); 03: a point between the median and the mean days between orders, sanity-checked against consumption (30-day product plus 5 days shipping gives 45); 01 alternative: 60, 90, 120 days. Sources 01, 03, 04, 09. [61b12124e33c] [021057848a4f] [4bfa7e9cadf3] [c2903035a7f5] `[needs brand data: median and mean days between orders]`

**R75. Gaps between win-back emails are 3 to 7 days, not 1 day.** Lapsed buyers complain faster. 03: 5 to 7 days. 04: +3 days, +7 days, +1 day, +14 days, +1 day. 01: about 1 week. Sources 01, 03, 04. [021057848a4f] [a5998cc28759] [61b12124e33c]

**R76. Sequence: "It's been a while" with no discount and new arrivals; reminder; unique dynamic code with a 48-hour deadline; 24-hour plain-text closer; optional bigger second offer 2 weeks later.** Sources 01, 03, 04. [61b12124e33c] [021057848a4f] [a5998cc28759]

**R77. Use "add past profiles" so the first send does not wait 75 days; this needs a static code.** Source 04. [a704ce6294f2] `[verify UI]`

**R78. Expect low returns; campaigns carry most retention.** 01: campaigns drive "99% of retention" (unverified). 02's client export: win-back flows "barely convert". Split high-value customers (historic or predicted CLV at least $1,000) into a stronger offer (03). Sources 01, 02, 03. [1784ea2727ac] [af644216425f] [6818bdf85834]

### 3.12 Sunset flow and suppression

**R79. Sunset trigger: added to an unengaged segment.** Definitions differ: 03: 0 opens AND 0 clicks in 180 days; 04: 0 opens, clicks, orders, checkouts, carts, views, site visits in 120 days AND received at least 6 emails in 120 days; 02: 120 days with no order ever, past buyers kept. See 7.9. Sources 02, 03, 04. [56d433c32a2b] [c57d2fe2264a] [171bd57ff251] [336b88ac711f]

**R80. Flow filters: opened 0 AND clicked 0 since starting this flow.** 03 states OR by mistake; with OR someone who opens but does not click keeps getting sunset emails. Use AND. Source 03 (corrected). [56d433c32a2b]

**R81. 3 plain-text emails with 5-day gaps, then set profile property unengaged = true, then suppress monthly.** Email 1: "Still interested? If not, unsubscribe here." Emails 2 and 3: strongest offer, unique code, "we will remove you unless you click". Goal is an open or click, not a sale. Sources 03, 04. [56d433c32a2b] [c57d2fe2264a]

**R82. Suppress: anyone marked as spam, any hard bounce, 4 or more soft bounces, and the unengaged segment (120 to 180 days). Review monthly.** Klaviyo bills on active profiles. Sources 01, 02, 03, 04. [c049ecf47935] [951b0132a90b] [6dcb0bfce104] [62ea5bc24ef6] `[web check: Klaviyo billing basis and unsuppress rules]`

### 3.13 Back in stock, review request, birthday

**R83. Back in stock: use Klaviyo's "subscribed to back in stock" metric for the flow; use the campaign type only for real restocks.** 01: "you can use it for any new inventory, do not fake sell-outs". 09 and 12 send restock texts for items that did not restock. ecomOS forbids that (R196). Sources 01, 04; against 09, 12. [a1e654a1f091] [7eaef73fe8eb] [3f1ec5d057e8]

**R84. Review request sits about 3 days after the loyalty email, after delivery.** Non-reviewers can still get the thank-you code. Source 04; 01 names it as a goal without an email. [0a935c9bd091] [ebc0429d8032]

**R85. Birthday flow: trigger on the loyalty app's customer birthday event, and personalise with the points balance property.** Preview with 2 profiles to confirm the numbers differ. Source 03. [9b7b4dd86442] `[verify UI]`

### 3.14 Segments

**R86. Lists are static and hold opt-ins; segments are dynamic and receive campaigns.** Keep 1 master email list and 1 SMS list. Never send a campaign to a list or to the whole list (R98 gives the exceptions the sources allow). Sources 01, 02, 03, 04. [24e40adf1b4f] [d7c5cedcb3dd] [f24ba64fabd7] [bb790bf6e145]

**R87. Every segment starts with "can receive email marketing" joined by AND.** Using OR pulls in almost everyone. The presenters see this mistake "all the time". Sources 02, 03. [516248e6ac94] [1d456b02f483]

**R88. Engaged segment: the campaign workhorse.** Definition merged from the sources: can receive email marketing AND (opened email at least once in the last N days where Apple privacy open is false, OR clicked email at least once in the last N days where bot click is false, OR placed order OR checkout started OR active on site at least once in the last N days) AND bounced 0 and marked spam 0 over all time. Add "subscribed to list in the last 14 days" so new subscribers are not dropped (03). Sources 01, 02, 03, 04. [c049ecf47935] [6e06d938ff3f] [9720dfa509a1] [ff7571c5eb99] [1d456b02f483]

**R89. Engagement window N: 90 days as the base for evergreen sends.** 02: 90 (widen to 120 when opens reach 60% to 70%). 01: 60 default, start at 30 if new, widen at 50% opens, stop at 90 or 120. 03: 180 on email activity plus 14-day site and subscribe carve-outs, with 90, 180 and 365 tiers. 04: 120 as the main, with 30, 60, 90 clones. Use 30 or 14 only during repair (R152). Sources 01, 02, 03, 04. [e385d9458d21] [df98522f016b] [3f50ca527fa4] [ff7571c5eb99]

**R90. Big offers and Black Friday go to a wider window (365 days); evergreen content to 90 days.** Once-a-year shoppers only re-engage on big moments. Source 03; 01 allows Black Friday to "churned" no-open-120-days. [3f50ca527fa4] [e385d9458d21]

**R91. Split engaged into prospects (placed order 0 over all time) and customers (placed order at least 1) to learn what converts each, but send evergreen content to both.** Under about $20M a year, do not micro-split sends; 1 campaign to 50,000 beats 2 to 10,000 (01). Personalise inside 1 email with dynamic blocks instead. Sources 01, 03, 10. [9720dfa509a1] [49f85dfebaf9] [0ca859db0b00] [24e40adf1b4f] [9ba42019fe30] [c28459447833]

**R92. Exclusion segments on every campaign: marked as spam at least once over all time; hard bounced at least once or soft bounced 4 or more times; unengaged 120 to 180 days.** Sources 01, 02, 04. [951b0132a90b] [62ea5bc24ef6] [c049ecf47935]

**R93. Unengaged segments: 0 opens AND 0 clicks (AND 0 site events, 04) in the window, AND received at least 6 emails in the window (04), so people had a chance.** Windows: 90 (01), 120 (02 sunset trigger, 04), 180 (02, 03 suppression), 365 (04, email only, received at least 12). 02 keeps past buyers out of unengaged on purpose; see 7.9. Sources 01, 02, 03, 04. [fbb4bfea66bf] [336b88ac711f] [171bd57ff251] [56d433c32a2b]

**R94. VIP by order count: 4 or more orders (02, 04) or 5 or more (01); optional spend at 3 to 4 times AOV.** 01 prefers count because "1 order away from VIP" is a clean message. VIP gets at most 1 extra email a month, an entry flow and a quarterly offer. Sources 01, 02, 04. [766ca8aa5269] [3ffe21f635f9] [14037b197111] `[needs brand data: order-count and spend distribution]`

**R95. High-potential buyers: site activity (active on site, viewed product, added to cart or checkout started) at least once in the last 30 days AND placed order 0 in the last 30 days.** 1 to 2 extra emails a month. Sources 01, 02, 04. [aa2e8130acf6] [3ffe21f635f9] [b97e06f650c6]

**R96. Win-back potential: placed order at least once in the last 150 to 180 days AND 0 in the last 90 days.** Sources 01, 02. [c049ecf47935] [3ffe21f635f9]

**R97. Buyer-stage segments: non-buyers, first-time buyers (equals 1), returning (2 or more), 3+ buyers, window shoppers (2 or more views or visits in 30 days, 0 orders ever), abandoners without purchase (cart or checkout in 90 days, 0 orders in 90 days), interested in category X, cross-sell (bought X, never bought Y).** Sources 01, 02, 04. [68cf12bbb813] [3ffe21f635f9] [7ccc6c565f86] [b97e06f650c6] [29b075b3e1cf]

**R98. Whole-list sends are a disagreement.** 01: 1 campaign a month to the wider list after recovery. 02: 1 to 2 a month to "all but unsubscribed and suppressed" so the unengaged get a chance back. 03: never. See 7.10. [e385d9458d21] [951b0132a90b] [d7c5cedcb3dd]

**R99. Location and property segments: ship-to country, EU vs non-EU, proximity to a store, Shopify tags, quiz answers, predictive AOV and CLV.** Sources 01, 02, 03, 04. [cd65fcd0d48d] [7b644e511db9] [eb3ee2d82966] [f24ba64fabd7]

### 3.15 Campaign cadence and content

**R100. Default cadence: 3 to 4 campaigns a week to the engaged segment, if the content is good.** 01: tested 2 a day to 2 a month, 3 to 4 gave the highest revenue and lowest unsubscribes. 02: 3 to 4 across 120 brands. 10: 3 to 4 (2 to 4 acceptable). 1 to 2 a week is forgotten; 5 to 7 raises unsubscribes and revenue plateaus (01, 02, 10). Conflicts: 03 says at least 1 a week, raise while CTR, unsubscribes and spam stay flat, and commit only to what you can sustain (example 2); 04 sets tiers by revenue (under $50k a month 2 to 3, over $50k 3 to 4, over $200k 4 to 5) and adds 1 a week only when opens exceed 30% and unsubscribes stay low; 06 says quality over any fixed cadence and starts at once a month. See 7.11. [dfbf925e6f5d] [d435b73cfe27] [7a1145af87dc] [1dbc06e4564f] [dbd9ab70c7db] [a6116076fc6e] [c53d577bf872]

**R101. Never skip weeks.** Several weeks of silence then a Black Friday push fails; unsubscribes and complaints rise when you return. Minimum 1 a week (03), 2 a week (01). Sources 01, 03, 06. [dbd9ab70c7db] [d435b73cfe27] [e23b7d7d24b2]

**R102. Content mix: mostly non-discount.** 02: per month 1 to 2 promotional, 4 to 6 product, 4 to 6 education, 2 to 4 social proof, 2 to 4 brand; promo under one third. 04: at least 5 non-discount emails per discount email (he uses 10:1), max 1 discount email a month outside Q4. 10: 4 pillars (educational, social proof, community and brand, product) roughly equal plus about 1 sale a month. 01: 3 to 4 a week "mostly non-discount". Max 1 sales event a month; every other month is better (02). Sources 01, 02, 04, 10. [e5552f0a655e] [81f4514ba7d3] [9077e5d437cb] [071d76074c86] [46a5333c2392]

**R103. No 2 consecutive emails of the same type; follow a sales email with a value email.** Example week: Monday education, Wednesday product, Friday social proof, Sunday brand. Sources 02, 04. [7a4e669c2511] [23ed2f50d61a]

**R104. Content frameworks to rotate.** One benefit, one feature, single FAQ, what's inside, how it's made, how to use, back in stock (real), trending (frame future not past), reviews (max 2 long), us vs them (facts, no begging), myth vs fact, blog promo (sell the click), research study (read the study first), obscure holiday (1 to 2 a month max), product or collection spotlight, content spotlight, weekly newsletter, cultural event, launch (teaser, launch morning, reminders, last chance). Sources 01, 02, 03, 10. [a18c13f52100] [277143b6f6c2] [623d951e5d86] [dac289376b1c] [532cdab329e6] [a1e654a1f091] [4e7b9fc24619] [78a2320e9eca] [50ed5320f524] [255dda5b5409] [0fc7fc3f1f45] [fe4206a3d106] [eb45bf2a9d5c] [5960dbd3e3b0] [3c10a64f1966] [826d4337358d] [783cb03489e3] [d70e0719ccfa] [e756efb90a3f] [50432b3f5d6e] [9077e5d437cb]

**R105. One email, one micro-topic, one takeaway.** Build micro-topics from niche, macro topic, micro topic. "Ingredient deep dive: why we use adaptogens" beats "our product is amazing". Sources 01, 03, 10. [998246dfc602] [a45e96ee496c] [f124cc441468] [945e9b8a355c] [c6824f14bcd2]

**R106. Every email shows a path to product.** Teach the problem, then the process, then place the product as the solution. Sources 01, 02, 03. [e7738e173006] [f5ac8bd65765] [7ac91a47ef79]

**R107. Calendar method: lock fixed dates, add 1 to 2 awareness days, map existing content to season, fill gaps with micro-topics, check the mix, stay 2 weeks ahead, review at month end for 20 to 30 minutes.** Sources 01, 02, 04. [9641bcb4fcd1] [6a19f9f385b5] [5886ee2c2f40] [3e4696a51c71] [bd8384e14e34] [85157d54ac6e]

**R108. Use campaigns as the test lab for flows.** Campaigns give data in 24 hours. Port winners: an education email into welcome with the code added, usage tips into post-purchase, a returns-policy email into cart as risk reversal. Sources 01, 02. [18ba82281157] [debbcf824284] [1b02d04b4fff] [71218ab504b8]

**R109. Coordinate campaigns with flows.** Smart sending on for campaigns (off for a big launch where people who got a flow email still want it); exclude people who bought in the same category in the last 3 days; tick "determine recipients at send time" when exclusions are dynamic. Sources 03, 04. [ba5c04225d61] [5b2cad894e44] [24b8079fe1fe]

**R110. Resend to non-openers for launches and big sales, 1 to 2 days later with a new subject.** 01: message-ID segment trick. 03: sequence builder follow-up, 48-hour minimum, narrow to the 30-day segment; 2 to 3 manual resends on Black Friday. Sources 01, 03. [d11a34c7dc7f] [6964a9fc308f]

### 3.16 Copy, subject lines and preview text

**R111. Write for the skim: 3 to 5 seconds of attention.** Bold points, short sections, 1 to 2 mobile scrolls, 100 to 300 words for a campaign, under 100 for a welcome email. Sources 01, 04, 07, 08, 10. [e5a610bd2f19] [99679e755f67] [c5f693b5c277] [658d97cafe81] [effdf39b2845] [28952f8a6673]

**R112. Simple words, 5th grade level, cut 20% to 30% when read aloud, active voice.** Sources 04, 01. [c5f693b5c277] [737d5783fddc] [28bbeaa03336]

**R113. Headline names the pain or outcome, not the feature.** "Brain fog has met its match", "1,000 songs in your pocket". Then 1 to 2 sentences, then the first button. Sources 03, 04, 07, 10. [7f637dd1902a] [98dec094905b] [658d97cafe81] [7c77592817cb]

**R114. Research before writing.** 2 to 4 hours per new product or angle: Ad Library (video ads, many versions), Amazon reviews filtered to Most Recent, podcasts and thought leaders, Trustpilot, the brand's own Instagram language and support tickets. Then 10 to 20 minutes per email. Sources 01, 08. [4dac36087f55] [d4e3dc152180] [3c8f273100f4] [618c17167140]

**R115. Sell on 3 points, and pick reviews that answer 1 objection each.** No face next to a sensitive topic. Sources 02, 07, 08. [658d97cafe81] [6e5742c076f2] [38077a826b12]

**R116. Deep emotional copy only for insecurity-anchor benefits; perks get icon rows.** Shift blame to an external cause only when that cause is true and provable; never name competitor companies. Brand voice may rule out insecurity angles. Source 08. [14d83f5d3f3e] [fac6b8c9debd] [b5dbf59a5f38] `[needs brand data: brand voice limits]`

**R117. Regulated claims must be substantiated and allowed, stated or implied.** Source 08 says "imply" them; ecomOS rejects that (R200). [4dac36087f55] `[web check: implied claim rules in the selling market]`

**R118. Subject line: short, curiosity gap, value first.** 01: 2 to 5 words, Title Case, 1 to 2 emojis sometimes. 03: under 50 characters, value in the first 3 words. 02: conversational ("would a friend send this?"). 04: short, no clickbait the email does not deliver. Preview text: written by hand, longer than the subject, adds to it, often ends with "..." (01, 06). Sources 01, 02, 03, 04, 06. [966ff3299f67] [d97f313a3c32] [685553ea4865] [660cfc96df62] [589fc4bc3d9b] [4516dab6a1af]

**R119. Judge subject lines on placed orders, not opens.** 01: opens 68% vs 69%, placed order 11.6% vs 3.8% in a cart email. 01 and 10 say opens come from sender name and cadence. 03 and 04 say do not spend campaign tests on subject lines; 04 says flow subject lines are worth testing. 06 runs a subject A/B on every send. See 7.13. [c4cf02ddd233] [5143f6e2959a] [32c744be62a5] [db47183f351f] [8f302c6bcdfe] [4516dab6a1af]

**R120. Sender name: brand, or founder plus brand; test it; keep the sender email constant across flows and campaigns, on the authenticated domain, with reply-to at support.** Sources 03, 04. [3247c58dc8b5] [ef1cb30f5c95]

**R121. AI drafts are drafts.** Prime the model with brand, products, audience, voice and USPs; ask for a punchy headline, sub-headline and 2 to 3 sentences; strip AI tells ("crafting", "enthusiasts", "unleash"); write product blurbs yourself; fact-check every claim against the brand record; add the CTA the draft forgot. Sources 01, 02, 07, 10. [b33ded12e90b] [f248facd3631] [8051e7b15977] [e932614a8a69] [fab16f82f356] [8e823019286f]

### 3.17 Design

**R122. 600 px wide; text 18 px desktop and at least 16 px mobile; line height 1.5; about 20 px block padding.** Sources 01, 04, 07. [54eb9e4fd217] [046d714ac94c] [e34234698845]

**R123. Above the fold: headline, 1 to 2 sentences, big button, and the code in promo emails.** 90% to 99% never scroll further (02). Bold the code right before the CTA. Sources 01, 02, 03, 04, 07, 08. [ca47b8d3f740] [681426ed9a3a] [d1327991a91c] [82bb67e79aeb] [9a3babffe41e] [0dec9bea1128]

**R124. Section order: header, sub-header, short body, image, CTA; repeat per section; a CTA at the end of every section and under every product; end with "Shop all" or "Shop bestsellers".** 1 decision per email even with many buttons. Sources 01, 02, 03, 07. [4410834af2cb] [c69f1a6ad23e] [ba367d283c2b] [00d5eebb6a8f] [8d705e1b1a26] [660cfc96df62]

**R125. Buttons big and thumb-reachable.** Sources 01, 04, 07. [ccc4b7310f94] [72945bee8a3a] [9a3babffe41e]

**R126. 3 to 5 products max; 1 per row with copy, or a 2x2 grid; never 3x2 on mobile.** Sources 02, 04, 08. [660cfc96df62] [46502d7fa9bc] [974a7ea84ff1]

**R127. Infographics instead of paragraphs: checklists, icon rows, comparison tables, timelines, graphs, flowcharts; icons instead of bullets.** At least 1 per email (01). Sources 01, 03, 04, 07, 10. [ddcf74804625] [aea3035bb04a] [82bb67e79aeb] [c69f1a6ad23e] [5b56681c9114]

**R128. Vary layout, imagery and theme between sends; match the brand's site and Instagram; use real product photos where accuracy matters.** Sources 01, 03. [a744284f4af9] [f4b51595abf4] [9b7f9bd54fc3] [82bb67e79aeb]

**R129. Every image gets alt text that carries the offer and a deep link (collection or product, never homepage); compress every slice; 1 link per slice.** Sources 01, 02, 03, 04, 07. [bcc326384a22] [31b2f58bfc95] [17b5705e3605] [8ae50e9df495] [2dabf0e92513] [9d1475541314]

**R130. Keep the offer, product names and footer as live text, not only inside images.** Gmail's AI reads text; image-only emails read as empty. Use native product blocks, a live top bar, a live footer with category links, and rebuild short text as live text after slicing. Sources 02, 04 against 07's "image-only is fine" and 01/03's full-slice method. See 7.12. [31b2f58bfc95] [8f1c460f5eed] [cfa416cb8d27] [5fde08efd3f8]

**R131. Send 1 to 3 plain-text emails a month; keep a graphic to text ratio of about 3 or 4 to 1.** Plain text founder emails are the top performers in 01, 02, 04, 10; 01 tests: text beat graphic on clicks and orders. Sources 01, 02, 04, 10. [125460461476] [8c7fb0e97b5c] [0adcc430d16d] [31b2f58bfc95] [65281424ea63]

**R132. Footer: unsubscribe (mandatory), organisation name and address via dynamic tags, category links, trust icons, social icons.** Sources 01, 03, 07. [d71019e19cc1] [5fde08efd3f8] [5b334bf3aab6]

**R133. Custom fonts need a web-safe fallback; avoid the HTML editor; check email size stays well under Gmail's clip limit (04 demo: 35 KB).** Sources 03, 04. [b8afb62d37d6] [ebb2548fab18] `[web check: Gmail clipping threshold]`

**R134. Test send to yourself, click every link, check desktop and mobile, then schedule.** Sources 01, 03, 04, 06, 07. [bcc326384a22] [5b2cad894e44] [d1d5d6fe035a] [400d584b7e15]

### 3.18 Deliverability

**R135. Deliverability is a sender reputation score built from engagement, complaints, bounces, cadence and authentication.** Inbox providers reward opens, clicks and replies and punish ignores, spam reports and unsubscribes. Technical setup is required but rarely the main cause of poor placement; list quality is. Sources 01, 02, 03, 06. [61807f09ea38] [660cfc96df62] [e758ab334635] [6d8587217a67] [84e6a958f0b2]

**R136. Branded sending domain is mandatory.** Add the root domain, pick a sending subdomain (send.brand.com), add the DNS records Klaviyo lists, wait up to 48 hours for verification, then limit sends to engaged recipients for 2 to 4 weeks (Klaviyo's own notice, 04). Sources 02, 03, 04. [a192f5312b82] [e758ab334635] [fc0425a31c0f]

**R137. SPF, DKIM and DMARC must all be present.** Sources 02, 03, 04 name them; none shows SPF or DKIM steps beyond the domain setup. Add a `_dmarc` TXT record with reporting addresses. Sources 02, 03, 04. [e758ab334635] [a192f5312b82] `[web check: Gmail and Yahoo bulk sender requirements]`

**R138. DMARC policy is a disagreement.** 03: p=none "always, never quarantine or reject" (his reasoning is wrong: DMARC acts on alignment failures, not on content). 04: start at none via a generator; his own record is p=quarantine pct=90. Start at p=none with reports, then move to quarantine and reject once all legitimate mail aligns. See 7.6. [a192f5312b82] [fc0425a31c0f] `[web check: current DMARC guidance and provider minimums]`

**R139. Spam complaint limits: stay under 0.1%, alarm at 0.3%.** 03: below 0.3% (Gmail and Yahoo), ideally below 0.1%; Klaviyo's tab says under 0.01% (03 client at 0.004%); 02 target 0.01%. Keep the strictest as the working target (0.01%) and 0.3% as the hard ceiling. See 7.7. Sources 02, 03. [6d8587217a67] [3dca25bfe545] [91d6fd433f58] `[web check: current Google and Yahoo spam-rate limits]`

**R140. Bounce rate under 1%; hard bounces suppressed at once, soft bounces after 4.** Sources 02, 03, 04. [6d8587217a67] [951b0132a90b] [62ea5bc24ef6]

**R141. Unsubscribe rate under 0.3% (Klaviyo's value); 03 accepts up to 0.67% when extra sends earn more.** 06: about 0.42% per send is normal on his list; over 1% on the first send after a long silence is expected. Sources 02, 03, 06. [91d6fd433f58] [3dca25bfe545] [c1faaf881fc4]

**R142. Clicks, not opens, are the placement signal.** Since iOS 15 Apple Mail opens every email. Exclude Apple privacy opens from attribution and from engaged segments where the builder allows; judge on unique clicks, placed order rate and revenue per recipient. Open-rate gates (R143) apply only to opens with Apple opens excluded. Sources 03, 06; 01 and 02 never mention Apple. See 7.14. [3dca25bfe545] [dccf91db3e0a] [c5f48c89de68] [1ce671434e00]

**R143. Open-rate floors, where opens are used: below 30% to 35% signals a placement problem; 45% to 50%+ on engaged segments is healthy.** 01: under 40% is a problem, 50% healthy. 02: under 30 to 35 placement problem, 45 to 50 target. 03: open above 30% and click above 0.5% as floors; Klaviyo tab: open above 33%, click above 1.2%. Sources 01, 02, 03. [61807f09ea38] [75378f892825] [91d6fd433f58] [ea472261103e] [3dca25bfe545]

**R144. Click rate floor 0.5%; 1.2% is Klaviyo's "okay"; 02 aims at 2%+ on redesigned emails.** Source 02's "5%" is transcript damage; read 0.5%. Sources 02, 03. [91d6fd433f58] [ea472261103e] [7dccf4216521]

**R145. Improve the emails before chasing technical fixes.** Varied topics and layouts, real value, 1 above-the-fold CTA, conversational subject lines, category footer links, invite replies ("Ask us anything"). Sources 01, 02. [b7b58b63ae33] [660cfc96df62]

**R146. Repair ladder: send only to engaged 14 days, 3 campaigns a week, then widen to 30, 60, 90 as opens hold at or above 50%.** 01: 6 weeks, move up after 3 straight sends at 50%+. 02: 2 weeks and 6 sends per stage; below 50%, stay 2 more weeks; still below, remove site activity from the segment. 03: tighten from 90 to 30 or 60, hold, then widen. During repair keep only welcome, browse, cart, checkout and post-purchase (and site abandonment per 02). Sources 01, 02, 03. [0f792188c5ee] [20fd44bca0dd] [df98522f016b] [98d43fdb4da1] [e5dfe8e98a49]

**R147. Clean the list before the ladder: suppress no opens, clicks or site visits in 180 days with 10+ emails received, no email in a year, never emailed and created over a year ago, any spam mark, hard bounce or 4 soft bounces.** Source 02; 01 and 04 use 180-day and 365-day unengaged. [6dcb0bfce104] [c049ecf47935] [171bd57ff251]

**R148. Run a seed-list placement test monthly and read Klaviyo's deliverability tab by inbox provider and country.** Where 1 provider is weak (02 and 03 examples: Hotmail and Outlook), build a tighter engaged segment for that provider. Sources 02, 03. [75378f892825] [3dca25bfe545] `[web check: GlockApps features and pricing]`

**R149. Warm-up applies to new domains, new IPs and returning senders: engaged only for 2 to 4 weeks, steady daily volume, then widen.** Source 04 (Klaviyo notice); 01 and 02 ladders do the same job. [fc0425a31c0f] [0f792188c5ee]

**R150. Optional: BIMI (logo and Gmail blue check) at about $1,500 a year, for 8 and 9 figure brands.** Source 02. [e758ab334635] `[web check: BIMI cost and requirements]`

**R151. Never use invisible text to pad an image-heavy email.** 01 and 07's header describe it; ecomOS forbids it (R198). [bc0f81f5c30a] [9efe76ee1d22]
