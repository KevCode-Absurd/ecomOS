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
