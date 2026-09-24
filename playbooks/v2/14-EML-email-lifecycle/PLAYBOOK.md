# 14-EML email lifecycle playbook

version: 2.0-draft  |  date: 2026-09-24  |  sources: 13  |  cards: 578  |  built from: sources/*.md

## 0. How to use this playbook

This is the base layer for the lifecycle agent: email, SMS and (where a brand has an app) push. It runs list growth, flows, campaigns, segments, deliverability and the monthly review. It is built from 13 mini playbooks. Every rule cites the mini playbook numbers (01 to 13) and card ids. Cards are in `data/library-v3/cards.json`.

Which sections to load for which task:

| Task | Load |
|---|---|
| Audit an account (flows, pop-ups, deliverability) | 3.1, 3.4 to 3.13, 3.18, 5, 6 |
| Build or fix a pop-up | 3.2, 3.3, 4.P3, 4.P4, 5.2, 7.1 to 7.3, 7.16, 7.17, 7.20 |
| Build or fix a flow | 3.4 to 3.13, 4.P5 to 4.P11, 4.P16, 5.1 |
| Build segments | 3.14, 4.P12 |
| Plan a month of campaigns | 3.15, 3.16, 4.P13 to 4.P15, 4.P19, 5.4, 9 |
| Write or design an email | 3.16, 3.17, 4.P18, 4.P26, 8 |
| Fix deliverability | 3.18, 4.P2, 4.P17, 5.3, 7.6, 7.7, 7.10, 7.13 |
| Run SMS | 3.19, 4.P20 to 4.P24, 5.5, 7.8, 7.15, 7.20 |
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

**R4. Email should drive at least 30% of total store revenue when the program is built.** Condition: Klaviyo-attributed revenue with transactional emails, bot clicks and Apple opens excluded (R179). Depends on the attribution window. Source 03 only, backed by client examples in 04 and 10. [465d3381b2a7] [0944381047ee] [46a5333c2392] `[needs brand data: email-attributed share and attribution window]`

**R5. Map the customer journey before building.** Ad or post, pop-up, welcome or abandonment flow, campaigns, first order, post-purchase, next order. Each touchpoint must match what the person already knows. A first-order discount to a 5-order customer is the failure case. Source 03. [a084662e8ae4]

**R6. Flows capture demand; campaigns create it.** If you send the same campaign every week, it should be a flow. Do not let campaigns plus welcome, cart and post-purchase emails hit the same person within 24 hours (R33, R109). Sources 02, 03. [7a1145af87dc] [24b8079fe1fe]

### 3.2 List growth and pop-ups

**R7. The offer is the biggest lever on opt-in rate.** Order of leverage: offer, then behaviour (trigger, steps), then copy, then design. A bad offer in a beautiful form still gets a bad rate; hacks move a bad-offer form from about 2% to 2.2%. Sources 01, 02, 03, 04, 12. [9eebdb581427] [60f8b169fd9a] [aa555d450d5a] [4c956b5e96a1] [ea0cb89619eb] [72945bee8a3a] [775acf1e29be]

**R8. Target an opt-in rate of 8% to 12% of site traffic.** Typical untested forms convert 1% to 4% (01: 1 to 3; 02: 1 to 3; 04: 2 to 4; 12: 2 to 3; 09: 5 to 6 on forms he reviews). Source 03 says above 9% and calls Klaviyo's 3% "excellent" badge not excellent. Sources 01, 02, 03, 04, 09, 12. [1c9b788208ca] [aa555d450d5a] [ea0cb89619eb] [40691f40d94c] [171673d6f3de] [51b9472f8d06] `[needs brand data: current opt-in rate by device]`

**R9. Choose percent off when AOV is under about $100 to $200 and dollars off above that.** 01: percent under $100, dollars over $100. 04: at $200 or more, dollars tend to win ($20 off vs 10% off at $200 AOV). 03: set the dollar amount at about 10% of AOV. Minimum that works: 10% off; 5% only for very high AOV (02, 04). Test it. Sources 01, 02, 03, 04. [60f8b169fd9a] [aa555d450d5a] [ea0cb89619eb] [72945bee8a3a] `[needs brand data: AOV, margin]`

**R10. Judge a signup offer on 4 numbers together, not on opt-in rate alone: opt-in rate, total signups, welcome flow placed order rate and revenue, and margin.** A higher opt-in rate with a collapsed welcome conversion may lose money. 04 example: a new offer had lower welcome CVR but higher AOV and revenue, so it won. Source 05 adds: test pop-up changes on full-site conversion rate, because a pop-up can lift opt-ins and lower checkout. Sources 02, 04, 05. [aa555d450d5a] [0590112c25d0] [c09dafafbc67] [1282cefafb08]

**R11. Ask for 1 input per step: email first, phone on a separate later step.** Never email and phone on 1 screen. No name, birthday or interests in step 1. Sources 01, 02, 03, 04, 09, 11, 12. [7ea9228eeda8] [2a3063dcd723] [9622afcc8844] [39aa68c94680] [9b9305f19394] [775acf1e29be] [75893d2892aa]

**R12. Put a micro-commitment step before the email field, and test it.** A yes/no question ("Do you want 10% off your first order?" with "Yes please" / "No thanks"), a 1-question quiz, or a scratch-off. 02: wins "in most cases" across 40+ brands. 03: wins "9 times out of 10". 04: most brands get a lift, some do better without. 09: quiz first "is what works in 2026". Condition: always A/B test per device. Sources 01, 02, 03, 04, 09. [92626e4998da] [e912865caec2] [4be0db20360f] [52d1b13d3d6e] [d80edbbaaf50] [75893d2892aa]

**R13. Gamified steps (spin to win, scratch-off) convert but carry a cost.** 01 calls spin to win "tacky" and "converts like crazy". 02: one brand went 11% to 14% with a scratch-off. Both tools show decoy prizes that never land. ecomOS: do not show prizes that cannot be won (R190). Sources 01, 02. [0419dcd84c79] [7da3ea843dc6] `[web check: local promotion and consumer rules on decoy prizes]`

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

**R27. Keep the consent text on the form.** 02 and 04 delete it for US-only stores. ecomOS: keep it legible on every form (R187). Source 01 shrinks the SMS consent text to size 8; do not copy that. Sources 02, 04; override in 3.21. [39aa68c94680] [72945bee8a3a] [397f14a8dca9]

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

**R83. Back in stock: use Klaviyo's "subscribed to back in stock" metric for the flow; use the campaign type only for real restocks.** 01: "you can use it for any new inventory, do not fake sell-outs". 09 and 12 send restock texts for items that did not restock. ecomOS forbids that (R186). Sources 01, 04; against 09, 12. [a1e654a1f091] [7eaef73fe8eb] [3f1ec5d057e8]

**R84. Review request sits about 3 days after the loyalty email, after delivery.** Non-reviewers can still get the thank-you code. Source 04; 01 names it as a goal without an email. [0a935c9bd091] [ebc0429d8032]

**R85. Birthday flow: trigger on the loyalty app's customer birthday event, and personalise with the points balance property.** Preview with 2 profiles to confirm the numbers differ. Source 03. [9b7b4dd86442] `[verify UI]`

### 3.14 Segments

**R86. Lists are static and hold opt-ins; segments are dynamic and receive campaigns.** Keep 1 master email list and 1 SMS list. Never send a campaign to a list or to the whole list (R98 gives the exceptions the sources allow). Sources 01, 02, 03, 04. [24e40adf1b4f] [d7c5cedcb3dd] [f24ba64fabd7] [bb790bf6e145]

**R87. Every segment starts with "can receive email marketing" joined by AND.** Using OR pulls in almost everyone. The presenters see this mistake "all the time". Sources 02, 03. [516248e6ac94] [1d456b02f483]

**R88. Engaged segment: the campaign workhorse.** Definition merged from the sources: can receive email marketing AND (opened email at least once in the last N days where Apple privacy open is false, OR clicked email at least once in the last N days where bot click is false, OR placed order OR checkout started OR active on site at least once in the last N days) AND bounced 0 and marked spam 0 over all time. Add "subscribed to list in the last 14 days" so new subscribers are not dropped (03). Sources 01, 02, 03, 04. [c049ecf47935] [6e06d938ff3f] [9720dfa509a1] [ff7571c5eb99] [1d456b02f483]

**R89. Engagement window N: 90 days as the base for evergreen sends.** 02: 90 (widen to 120 when opens reach 60% to 70%). 01: 60 default, start at 30 if new, widen at 50% opens, stop at 90 or 120. 03: 180 on email activity plus 14-day site and subscribe carve-outs, with 90, 180 and 365 tiers. 04: 120 as the main, with 30, 60, 90 clones. Use 30 or 14 only during repair (R146). Sources 01, 02, 03, 04. [e385d9458d21] [df98522f016b] [3f50ca527fa4] [ff7571c5eb99]

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

**R117. Regulated claims must be substantiated and allowed, stated or implied.** Source 08 says "imply" them; ecomOS rejects that (R191). [4dac36087f55] `[web check: implied claim rules in the selling market]`

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

**R142. Clicks, not opens, are the placement signal.** Since iOS 15 Apple Mail opens every email. Exclude Apple privacy opens from attribution and from engaged segments where the builder allows; judge on unique clicks, placed order rate and revenue per recipient. Open-rate gates (R143) apply only to opens with Apple opens excluded. Sources 03, 06; 01 and 02 never mention Apple. See 7.13. [3dca25bfe545] [dccf91db3e0a] [c5f48c89de68] [1ce671434e00]

**R143. Open-rate floors, where opens are used: below 30% to 35% signals a placement problem; 45% to 50%+ on engaged segments is healthy.** 01: under 40% is a problem, 50% healthy. 02: under 30 to 35 placement problem, 45 to 50 target. 03: open above 30% and click above 0.5% as floors; Klaviyo tab: open above 33%, click above 1.2%. Sources 01, 02, 03. [61807f09ea38] [75378f892825] [91d6fd433f58] [ea472261103e] [3dca25bfe545]

**R144. Click rate floor 0.5%; 1.2% is Klaviyo's "okay"; 02 aims at 2%+ on redesigned emails.** Source 02's "5%" is transcript damage; read 0.5%. Sources 02, 03. [91d6fd433f58] [ea472261103e] [7dccf4216521]

**R145. Improve the emails before chasing technical fixes.** Varied topics and layouts, real value, 1 above-the-fold CTA, conversational subject lines, category footer links, invite replies ("Ask us anything"). Sources 01, 02. [b7b58b63ae33] [660cfc96df62]

**R146. Repair ladder: send only to engaged 14 days, 3 campaigns a week, then widen to 30, 60, 90 as opens hold at or above 50%.** 01: 6 weeks, move up after 3 straight sends at 50%+. 02: 2 weeks and 6 sends per stage; below 50%, stay 2 more weeks; still below, remove site activity from the segment. 03: tighten from 90 to 30 or 60, hold, then widen. During repair keep only welcome, browse, cart, checkout and post-purchase (and site abandonment per 02). Sources 01, 02, 03. [0f792188c5ee] [20fd44bca0dd] [df98522f016b] [98d43fdb4da1] [e5dfe8e98a49]

**R147. Clean the list before the ladder: suppress no opens, clicks or site visits in 180 days with 10+ emails received, no email in a year, never emailed and created over a year ago, any spam mark, hard bounce or 4 soft bounces.** Source 02; 01 and 04 use 180-day and 365-day unengaged. [6dcb0bfce104] [c049ecf47935] [171bd57ff251]

**R148. Run a seed-list placement test monthly and read Klaviyo's deliverability tab by inbox provider and country.** Where 1 provider is weak (02 and 03 examples: Hotmail and Outlook), build a tighter engaged segment for that provider. Sources 02, 03. [75378f892825] [3dca25bfe545] `[web check: GlockApps features and pricing]`

**R149. Warm-up applies to new domains, new IPs and returning senders: engaged only for 2 to 4 weeks, steady daily volume, then widen.** Source 04 (Klaviyo notice); 01 and 02 ladders do the same job. [fc0425a31c0f] [0f792188c5ee]

**R150. Optional: BIMI (logo and Gmail blue check) at about $1,500 a year, for 8 and 9 figure brands.** Source 02. [e758ab334635] `[web check: BIMI cost and requirements]`

**R151. Never use invisible text to pad an image-heavy email.** 01 and 07's header describe it; ecomOS forbids it (R188). [bc0f81f5c30a] [9efe76ee1d22]

### 3.19 SMS (and RCS, iMessage)

**R152. SMS is high urgency and low frequency; nurture goes to email.** Send launches, drops, restocks (real), sales, flash sales, exclusive offers, trend alerts and big news. Testimonials, brand stories and evergreen bestsellers by SMS raised unsubscribes and gave poor ROI in 09 and 12. SMS unsubscribe runs 3% to 5% per send vs about 0.3% on email (09). Sources 02, 09, 11, 12. [b9130f4f4dca] [e6323f097649] [7eaef73fe8eb] [db06cdf5cc52] [bcc0f86cebc6] [bf9cd4297ad9]

**R153. Explicit SMS consent before any text; confirm the segment holds only SMS opt-ins; keep opt-out handling (STOP) on every program, including iMessage.** Source 13 says iMessage frees you from "reply STOP"; do not act on that. Sources 09, 11, 12; against 13. [ccceb9ed6344] [ee1a31c09fcc] [9e19056dd462] [59e016b15ca2] `[web check: TCPA, CTIA, state mini-TCPA, TRAI DLT for India, PECR for UK, consent and opt-out rules per country]`

**R154. Quiet hours: never send outside the legal window for the recipient's country and state, in recipient local time; keep Klaviyo quiet hours on.** 11: not before 8:00 a.m. or after 9:00 p.m. ("fines"). 12: not before 10:00 a.m. or after 7:30 p.m. (preference). Neither names a law. Sources 11, 12. [ccceb9ed6344] [a9df8fb1a06e] [5a21fae6ffd5] `[web check: legal quiet hours per country and US state; India TRAI promotional window]`

**R155. Best send window to start: 11:00 a.m. to 2:00 or 3:00 p.m.; test 4:00 to 5:00 p.m.; last-chance texts by 6:00 to 7:00 p.m.** Test on the brand's own clicks and revenue by hour. Sources 11, 12. [a9df8fb1a06e] [5a21fae6ffd5]

**R156. Campaign frequency is the biggest SMS disagreement.** 11: about 1 a week, test 2 only above 8 figures, more than 2 is "overkill". 12: 1 a week, 2 "every now and again". 09: about 2 a week, minimum 1, daily to non-buyers for heavy acquisition brands, 1 to 2 a day in a sale push. 05 (Postscript): 8 to 10 texts per subscriber per month with no unsub impact, step up by 1 a week until unsubscribes tick up, and a holdout where 2 a week beat 1 a week at 98% certainty. 02: launches, restocks and sales only. Safe start: 1 a week, then step up with a holdout (P24). See 7.8. [6f21ea67f481] [bf9cd4297ad9] [ec74b2c055f2] [52f701ac2a63] [bb28c48148d6] [651884bb18e3] [b9130f4f4dca]

**R157. Adjust frequency by purchase cycle and buyer state.** Apparel about quarterly, furniture about every 18 months (11). Past buyers of one-time products get less; active subscription customers get no campaign texts (09). Sources 09, 11. [77dd2ea812e0] [ec74b2c055f2] `[needs brand data: repeat purchase interval, subscription status]`

**R158. Keep each SMS to 1 segment: 160 GSM-7 characters, 70 if any emoji or Unicode character is present; read the platform's segment counter before sending.** The sources' emoji figures (35 to 70 characters each) are wrong; the cards correct them. Cost 1 to 3 cents per segment, typically about 1.5 cents (09). Sources 09, 11, 12. [0228dbaf571e] [fa8b517af050] [54ec55400d45] [ccceb9ed6344] `[needs brand data: per-segment rate on the brand's plan]`

**R159. MMS costs 2 to 3 times SMS; use images only where the image earns it, judged on net profit (revenue minus send cost), not on clicks or revenue alone.** 09 tests: image versions made more revenue with fewer clicks; net profit was positive but small. Reserve images for launches, new flavours, the welcome infographic and the abandonment text (Grüns example). Sources 09, 11, 12. [13f23c2e8c94] [f89925ebf6ad] [db06cdf5cc52]

**R160. Phone capture: email step first with the full offer, then a phone step that "activates" the same offer.** Button "Claim now", not "Continue". Copy: "Finish signing up with text to activate your 20% off." No extra discount for the phone number (09, 11). Conflict: 04 tests a bigger SMS offer (15%) or a VIP club; 02 mentions 10% email and 20% SMS. Target phone submit about 15% with a quiz-first form (09). Sources 09, 11, 12 against 04, 02. [75893d2892aa] [9b9305f19394] [775acf1e29be] [1bad712bca98] [8bb0c8c613c5]

**R161. SMS welcome: 2 to 3 texts inside about 5 days.** Day 1 immediate code with 1 short brand remark, day 3 reminder with 1 differentiator, day 5 last chance. 11: 2 texts, second 2 to 3 days later. 05 (Ridge): a 6-message welcome ending in a question. Aggressive daily onboarding (Grüns, 23 texts in 30 days) is a subscription-brand exception, not a default. Sources 05, 09, 11, 12. [6c2a73b99726] [136997a1cb23] [71d9f81273f0] [c2cd726a16ab] [52f701ac2a63]

**R162. Abandonment texts: 1 SMS per recipient per abandonment flow, sent within 48 hours of the event, browse after about 60 minutes, cart and checkout after 1 to 2 hours.** 09 calls more than 1 "illegal in the US" and shows Klaviyo enforcing it; 11 calls more than 1 "non-compliant" (welcome may hold 2). Neither names the rule. Split by buyer status: non-buyers get the welcome code, buyers a plain reminder. Sources 09, 11, 12. [ee1a31c09fcc] [136997a1cb23] [71d9f81273f0] `[web check: whether the 1-text-per-48-hours limit is law, CTIA guidance or Klaviyo policy; state rules]`

**R163. Post-purchase SMS: 1 text on day 10 to 14 (a few days after delivery), "are you liking it?" plus a soft cross-sell, no offer; replenishment text at supply plus delivery minus a few days; nothing more at first because buyers also get campaigns.** Source 09. [586799a976b3]

**R164. SMS win-back at 60 to 90 days or 2 times the average interval: a flash offer with 72 hours, then a last chance 2 days later.** Sources 09, 12. [c2903035a7f5] [71d9f81273f0]

**R165. SMS audience: a disagreement.** 09: broadcast to all SMS subscribers and exclude only people with 15+ texts and 0 clicks ever; people who never click still buy. 11: tighten to an engaged SMS segment when clicks fall under 5% or unsubscribes exceed 1%. 05: watch unsubscribes in each subscriber's first 30 days. See 7.9 SMS note. [74853693497f] [02f841a00c26] [52f701ac2a63]

**R166. SMS metrics: click rate 5% to 15%, unsubscribe under 1% (under 0.5% excellent), delivery over 90% (over 95% excellent), revenue per message, net profit per send.** Open rate is a vanity metric for SMS; "98% open rate" is uncited. Sources 11, 12, 05. [02f841a00c26] [bb9581c6a1d8] [76ea7acfff13]

**R167. Prove SMS incrementality with a holdout once the bill passes about $10K a month.** 3 cells: 50% normal, 25% no messages, 25% double cadence; compare revenue per subscriber to the no-message cell and subtract message cost. Source 05. [651884bb18e3] [9a17b76595cd]

**R168. Email and SMS together: a disagreement.** 03 (checkout section): send email and SMS at the same time or very close, because you cannot know which converts. 03 (multichannel section): SMS first, wait 2 hours, then email if no order. 11: email at 9:00 a.m., SMS 5 to 6 hours later for the same message. 02: SMS follow-up only to non-clickers where SMS revenue per recipient is strong (example 1.70 EUR). See 7.15. [fbfeb91636ec] [4c7296971696] [a9df8fb1a06e] [af644216425f]

**R169. Add a question to 1 existing flow to start conversational SMS, then staff the replies and tag objections into flows, PDPs and ads.** Start with the last welcome or abandonment text: "Do you have any questions I can answer?" Go conversation-first only for long-consideration or high-ticket products. Sources 05, 13. [c2cd726a16ab] [5bd6379a40ae] [d0012f077a0d] [324169289900] [3e359a2bee9b] `[needs brand data: who answers replies and how fast]`

**R170. RCS is a separate channel with SMS fallback; pilot it with a holdout and creative held constant; expect a novelty lift that fades; judge after the higher cost.** US-only claims in 05. iMessage (13) is a vendor pitch for iPhone-heavy North American lists; treat as test ideas only, and not for Android-heavy markets such as India. Sources 05, 13. [30309dfff699] [04f7be245280] [80442f6087a2] [3f1fb0650452] `[web check: RCS availability, fees and verification per country; Apple rules on business iMessage]` `[needs brand data: iPhone share of list]`

**R171. Platform choice matters little; consolidate with the email platform and price-shop Attentive and Postscript; ignore AI feature pitches.** Sources 09, 11, 12. [ef374a64ba7e] [af694ec3e7e4] [aa2a2140c1a0]

**R172. Push notifications need the brand's own app; add push steps to flows the same way as SMS.** Source 03 only. [4c7296971696] `[verify UI]`

### 3.20 Testing and metrics

**R173. Revenue per recipient and placed order rate decide tests; clicks second; opens last.** 02: revenue decides "95% of tests". 03: placed order rate for content tests, click rate for send-time tests, never open rate. 04: placed order rate, then click, then open. 06: CTR as main metric. 01: placed orders and revenue. See 7.13. Sources 01, 02, 03, 04, 06. [59ae581e3e7f] [659e9f913086] [5d7c84dc41ce] [c4cf02ddd233] [c5f48c89de68]

**R174. Test with a written hypothesis, 1 variable, manual 50/50 at 100% of the audience, manual winner.** Klaviyo's automatic 20/20/60 after 4 hours picks winners too early and sends the majority at a worse time. Sources 02, 03, 04. [ac370b420628] [659e9f913086] [e753b3fb98af]

**R175. Sample floors: 1,000 recipients per branch (500 if the gap is huge), about 2 weeks for flows; 3,000 to 5,000 impressions or 15 days for forms; 5 to 10 campaigns per send-time pair.** Do not call winners at 50 to 100 recipients. Sources 02, 04. [e8e1adc8fefe] [eed1632440b9] [9211d9b5ff9c]

**R176. Test priority: flow delay of email 1 in the biggest flows; content and offer; product vs collection; long vs short; text vs designed; send time; then subject lines; CTA colour last (skip under about $100k a month).** Sources 01, 02, 03, 04. [e846a075130e] [700ad4cccb44] [db47183f351f] [8cab23f94038] [97bfd09fd8e1]

**R177. Winners do not transfer between flows or campaigns; retest.** Sources 01, 02. [8b488b1b15d3] [2176f28aa94d]

**R178. In flow timing tests, duplicate every email onto both branches; do not rejoin after email 1.** Source 04. [5f42a553bc22]

**R179. Attribution settings: exclude transactional messages, bot clicks and Apple privacy opens; keep the window near 5 days (shorter for impulse, longer for long consideration); SMS window 1 day.** Expect reported revenue to drop. Sources 03, 04. [1ce671434e00] [fc0425a31c0f] `[web check: current Klaviyo default attribution window]`

**R180. Turn on anonymous visitor tracking so pre-signup views and carts backfill and feed browse and cart flows.** Sources 03, 04. [8796c9f1ffa6] [fc0425a31c0f]

**R181. Optimise unique counts, not rates.** Open rate down 10% with unique opens up 40% is a win. Source 03. [489a0deaff01]

**R182. Read the metric chain, not the headline: recipients, unique opens, open rate, unique clicks, click rate, unique conversions, conversion rate, revenue, revenue per recipient, AOV.** Opens down: deliverability. Clicks down: content. Conversions down with clicks steady: merchandising or offer. Under 5% change is noise; look for over 10%. Read revenue and order count together to catch AOV distortion. Source 03. [8183b1fcc7d0] [dccf91db3e0a] [7b7bba687f4a] [ea472261103e]

**R183. Flow revenue follows site traffic; a drop is only a red flag if traffic held.** Then check skips, filters and dynamic blocks. Source 03. [d2e68173f29a] [ac6fccd77bd7]

**R184. Monthly review is mandatory to catch silent breakage: a theme update that hides the pop-up, a cart flow that stopped, a broken integration that throws no error.** Sources 03, 11. [5d6743fc3f40] [059f73755fa8] [02f841a00c26]

**R185. AI analysis of Klaviyo exports gives hypotheses, not findings; verify against the CSV, then test.** Source 02. [7dccf4216521] [87afe3ecbaf6]

### 3.21 ecomOS rules that override any source

**R186. ecomOS: no fake restock, no fake sell-out, no fake "running low", no fake deadline.** Sources 09 and 12 send restock texts for items that did not restock; 01 says "do not fake sell-outs". Only real inventory events and real expiry dates. [7eaef73fe8eb] [3f1ec5d057e8] [a1e654a1f091] [cefa2905adfd]

**R187. ecomOS: no hidden unsubscribe, no pre-checked marketing consent, no shrunken consent text, no consent text removed.** 01 says the checkout checkbox "can be automatically checked" and shrinks SMS consent to size 8; 02 and 04 delete the disclaimer for US stores. Consent text stays legible on every form and every market. [3d97f72a2969] [397f14a8dca9] [39aa68c94680]

**R188. ecomOS: no invisible text.** The size 5, background-colour "About Us" block in 01 and the 07 header is a spam signal and a deception. Fix image-heavy emails with live text instead (R130). [bc0f81f5c30a] [9efe76ee1d22]

**R189. ecomOS: keep a visible close on every pop-up step.** 01, 02 and 04 hide the X (opacity 0, 1 px, size 5). A clear "No thanks" button plus a visible X is the floor. Owner may test a smaller X but never a hidden one. [397f14a8dca9] [9622afcc8844] [72945bee8a3a] `[web check: accessibility rules and Google interstitial guidance]`

**R190. ecomOS: gamified pop-ups must only show prizes that can be won.** No decoy wheel slices or fake scratch results. [7da3ea843dc6] [0419dcd84c79]

**R191. ecomOS: every claim, review count, guarantee, shipping time and "as seen on" logo must match the brand record.** Regulated claims are never implied to dodge the rule (08). AI-drafted claims are checked before send (10). [4dac36087f55] [f0580c1b1e80] [8e823019286f]

**R192. ecomOS: consent, quiet hours and sender registration follow the recipient's country, checked live.** No US number in this playbook applies to India, the UK or the EU without a `[web check]`. For Gehna (India) check TRAI DLT registration, header and template approval and the promotional time window before any SMS. [ccceb9ed6344] [5a21fae6ffd5]

**R193. ecomOS: no deliberate typos, no pretending an automated message is a person, and no "forget about email".** Source 13's tactics stay out of client work. The store is always identified as the sender. [324169289900] [dc0288dd127b]

**R194. ecomOS: competitor emails are for layout and mood only.** Never copy their text, logos, products or faces. Reverse-engineering structure with AI (07) is allowed; verbatim reuse is not. [fab16f82f356]

**R195. ecomOS: arithmetic in code, not in the model.** Revenue per recipient, net profit per SMS, opt-in rate and segment counts are computed from exports, never estimated. Missing values show as unavailable, not zero.

## 4. Procedures (implementation)

Every Klaviyo, Shopify, Figma, Aaliyah, Alia, Omnisend and DNS step below is `[verify UI]`. Menu names are as the sources spoke them in 2024 to 2026. Rollback for any flow change: set the flow's emails back to draft or manual with "update action statuses"; for any campaign, cancel the schedule before send time; for any segment, keep the old segment until the new one's preview count is checked.

### P1. Account, tracking and attribution setup

Goal: clean data before any build. Preconditions: Klaviyo account connected to Shopify. Sources 03, 04. [8796c9f1ffa6] [1ce671434e00] [fc0425a31c0f]

1. Shopify integration: turn on the Shopify app embed in the theme; tick "sync Shopify email subscribers to Klaviyo" into the master email list; do the same for SMS into the SMS list; leave "sync profiles to Shopify" off. `[verify UI]`
2. Sender name: brand, or founder plus brand. Sender email on the brand domain. Reply-to: the support inbox.
3. Email > sender preferences: Smart Sending on, 16 hours (campaigns use it; flows turn it off per email). `[verify UI]`
4. Attribution: 5-day open and click, last interacted; exclude Apple Mail Privacy Protection opens; exclude transactional messages; exclude bot clicks for email and SMS. SMS window 1 day. Shorter than 5 days only for impulse products; longer only for long consideration. Save. Expect reported revenue to fall if the old setup was inflated. `[verify UI]` `[web check: current Klaviyo defaults]`
5. Data: anonymous visitor tracking on. UTM tracking on with source, medium, campaign, id and term; "automatically add UTM parameters to links" on. `[verify UI]`
6. Brand library: logo, colours, primary web-safe font, custom fonts with a fallback (example: Geist with Tahoma), social links checked. `[verify UI]`
7. Consent pages: brand the preference, unsubscribe and (if double opt-in) confirmation pages. Add a thank-you line on the unsubscribe page. `[verify UI]`
8. Check: send a test campaign to 1 profile and confirm UTM parameters appear in the link and the profile shows the open and click.
Rollback: attribution changes only affect reporting; note the old values before changing them so a before-and-after comparison is possible.

### P2. Domain authentication and DMARC

Goal: branded sending domain live, SPF, DKIM and DMARC passing. Sources 02, 03, 04. [a192f5312b82] [e758ab334635] [fc0425a31c0f]

1. Settings > Account > Domains > add domain. Enter the root domain. Choose the sending subdomain (default "send"). Keep routing on dynamic. `[verify UI]`
2. Pick the DNS provider or "other". Copy each record Klaviyo lists (04 saw 4 NS records on host "send" plus 1 TXT on "@"; the header notes CNAME may now be used) into the DNS host. `[web check: current Klaviyo record types]`
3. Wait until the status shows "Active" (up to 48 hours). Do not send from the domain before that.
4. Tick Klaviyo's acknowledgement that sends may need to be limited to engaged recipients for 2 to 4 weeks. Then run P17 as a warm-up: engaged 14 or 30 days only, steady volume, widen weekly.
5. Set the default sender address on the new domain.
6. DMARC: add a TXT record at host `_dmarc`. Start with `v=DMARC1; p=none; rua=mailto:dmarc@yourdomain` (04's generator route) so reports flow. Read reports for 2 to 4 weeks. When every legitimate source aligns, move to `p=quarantine` (04's own record is quarantine with pct=90), then `p=reject`. Do not follow 03's "never quarantine or reject" (see 7.6). `[web check: Gmail and Yahoo DMARC minimums and current guidance]`
7. Check: run a DMARC checker (GlockApps free tool per 02) and a placement test. Confirm SPF and DKIM pass and align.
Rollback: if mail fails after a policy step up, return the policy to the previous value and read the aggregate reports for the unaligned source.

### P3. Build the pop-up (Klaviyo forms)

Goal: an 8% to 12% opt-in form per device. Preconditions: offer chosen per R9 and R10; master email list and SMS list exist. Sources 01, 02, 03, 04. [2a3063dcd723] [c5e1f30dd58d] [4be0db20360f] [d124c18b882e]

1. Sign-up forms > create form > template with a micro-yes step or a multi-step email and SMS template. Name it "Sitewide pop-up desktop". Email list: master list. SMS: the SMS list. Teaser on. `[verify UI]`
2. Form type: pop-up (beats fly-out; full page converts more but hurts experience).
3. Targeting and behaviour > timing: "based on rules". Desktop: time delay 6 seconds (test 4 vs 12), scroll 60% (test 30 to 90), exit intent on. "All conditions must be met" off. Frequency: after close, show again after 3 to 5 days; never after submit. Devices: desktop only. "Don't show to existing Klaviyo profiles" on. Exclude URLs: cart, checkout, wholesale. Location: ship-to countries only. Untick "click outside form to close" if it causes accidental closes (03), but keep the X visible (R189). `[verify UI]`
4. Step 1, micro-yes: headline "Do you want 10% off your first order?" with the offer number large (about size 55 to 60). Buttons: "Yes please" (action: show next step) and "No thanks" (action: close form). No image on this step is fine (03).
5. Step 2, email: headline "Unlock 10% off your first order". Delete the default sub-headline. Email field label "Enter your email here", light grey field on white. CTA "Claim my discount" (height 54 to 70 px). Consent text present and legible (R187). Secondary "No thanks, I'd rather pay full price" as a button, about 10 px below. Action: submit to the master list, then show next step.
6. Step 3, SMS: headline "Almost there. Finish signing up with text to activate your 10% off". Phone field; SMS consent text with required disclosures, legible; button "Claim now" (not "Continue"). Action: subscribe via text to the SMS list, then show next step. People who skip still enter the email welcome flow. `[web check: SMS consent wording per country]`
7. Step 4, success: same logo and fonts. "Your code is on its way. Check your inbox (and phone). Not there in 5 minutes? Check spam." Button "Start shopping" that closes the form (or "go to inbox"). Do not show the code (R21; 01 differs).
8. Brand every step: fonts, colours, buttons, input fields. Compress the logo and any image (tinypng or iLoveIMG).
9. Clone for mobile: three dots > clone > "Sitewide pop-up mobile". Devices: mobile only. Untick exit intent. Remove images. Sizes: CTA height 70 to 80, CTA text 24 to 30, offer number 60, input height 70, input text 20, "No thanks" 18 to 20, success text 22 to 24. Teaser as a small circle or corner. `[verify UI]`
10. Check: preview each step on an iPhone and a 4K desktop preview and on the live site; confirm the offer reads in 3 seconds, every step has a visible close, nothing overlaps chat or loyalty widgets, the SMS consent text is readable, the form loads with no lag.
11. Publish both forms. Confirm the welcome flow trigger (P5) points at the same list.
12. Amped, Aaliyah or Alia route (01, 02, 09): same structure; quiz or scratch-off first step; connect the tool to the Klaviyo list; static code must exist in Shopify; target new visitors (not signed up); re-show and popup-overlap rules; single opt-in for Klaviyo. Vendor claims of 15% to 20% come from presenters with affiliate ties. `[verify UI]` `[web check: pricing]`
Rollback: unpublish the new forms and republish the previous version; Klaviyo keeps the old form.

### P4. Pop-up A/B test

Goal: 1 clean test at a time, decided on total signups and welcome revenue. Sources 02, 03, 04. [00de729163a8] [e8e1adc8fefe] [ea0cb89619eb]

1. Open the form > "Create A/B test". Name it after the variable ("offer test"). A = current. B = challenger. Edit every element of B that carries the offer (micro-yes, email step, teaser). `[verify UI]`
2. Weight: manual 50/50. Winner selection: manual. Do not let Klaviyo pick on low volume.
3. Run for at least 3,000 to 5,000 impressions per variant or 15 days, whichever is longer. Test desktop and mobile separately.
4. Decide on total signups, welcome flow placed order rate and welcome revenue, plus site conversion rate (05). Not on opt-in rate alone.
5. Log the result and the next test from the leverage list (R23). Run 1 test at a time, monthly.
Rollback: end the test and keep A.

### P5. Welcome flow

Goal: deliver the code and convert 10% to 20% of entrants inside 72 hours. Sources 01, 02, 03, 04. [4d6f11a9f443] [f2c3f6895ad4] [ef1cb30f5c95] [6e89698da8b5]

1. Flows > create flow > build your own, or the template with a returning vs non-buyer split (delete that branch). Name "Welcome series". `[verify UI]`
2. Trigger: added to list = the pop-up's list. Re-entry off.
3. Profile filter: placed order 0 times over all time. Optional: exclude B2B tags. Save (the trigger cannot change after this; clone to change it).
4. Structure: Email 1A (0 delay) > wait 8 hours > Email 1B > wait 16 hours > Email 2 > wait 1 day > Email 3 > wait 1 day > Email 4 > wait 1 day > Email 5 > wait 1 day > Email 6 > wait 1 day > Email 7. Adjust to 2-day gaps late in the flow for high AOV (04).
5. Each email: subject, preview, sender name (test founder vs brand), sender email on the authenticated domain, smart sending OFF ("skip recently emailed profiles" unticked), UTM on. Name emails "Welcome email 1A" and so on.
6. Content per R44. Email 1A: code and CTA above the fold, 1 to 3 bestsellers, trust marks, code again at the bottom. 1B: plain text "just making sure you saw your code". 2: founder story with substance and a real face. 3: bestsellers with 1 reason each. 4: objections and us vs them, "code expires in 48 hours" only if it truly does. 5: reviews that name objections, "24 hours left". 6: last chance. 7: plain-text founder "extended 24 hours" only if the code was truly extended (use a unique code, R37).
7. Check: preview each email with a real profile; click every link; confirm the discount URL auto-applies (`/discount/CODE?redirect=/collections/handle` on Shopify); confirm a profile that orders after 1A does not get 1B.
8. Set emails live one by one with "update action statuses". After 30 days read revenue by email; if emails 5 to 7 earn nothing, reposition or cut them.
Rollback: set new emails to draft; the old flow stays untouched until the new one has run 2 weeks.

### P6. Site abandonment flow

Sources 01, 04. [75b807a7abce] [b0f7b82a2bb3]

1. Flows > build your own > "Site abandonment". Trigger: Active on Site (API metric). `[verify UI]`
2. Profile filters: viewed product 0, added to cart 0, checkout started 0, placed order 0, all since starting this flow; has not been in this flow in the last 30 days.
3. Delay 2 hours (test 1 vs 4 hours with a random-sample split, P16).
4. 1 email: "Lost in choices? Let us point you the right way", collections or bestsellers, light social proof, shop by category. Smart sending off, UTM on.
5. Check: preview with a profile that has no product view; confirm a profile that viewed a product is skipped.

### P7. Browse abandonment flow

Sources 01, 02, 03, 04. [5ad3da1bdb3a] [c83fa5e0d0d6] [909e75c1eb8d] [5aad4467fa44]

1. Flows > create flow > Essentials > browse abandonment template. Trigger: Viewed Product. `[verify UI]`
2. Filters: added to cart 0 (add this; the template lacks it; on Shopify use the Shopify metric), checkout started 0, placed order 0, all since starting this flow. Re-entry: not in this flow in the last 30 days.
3. Delay 1 hour (test 45 minutes vs 2 hours). Email 1 > 1 day > Email 2 > 1 day > Email 3 > 1 day > Email 4 (> 1 day > Email 5 optional).
4. Save the template's dynamic product block as universal content and restyle it. Fix the "shop now" link: preview, open event properties, copy the product URL property, paste it as the link (03).
5. Content per R53. Email 1 light reminder with viewed item and 4 related products; 2 risk reversal and objections; 3 product reviews; 4 small discount 48 hours or subscribe-and-save; 5 plain-text 24-hour closer.
6. Smart sending off, UTM on. Check: preview with 2 profiles that viewed different items and confirm the block and link change.

### P8. Cart and checkout abandonment flows

Goal: 2 flows that never overlap. Sources 01, 02, 03, 04. [d962429e9e36] [34204d0c3ce5] [d94eb68e5e18] [85117c7d0910] [fac642b0957b] [393737091e3e] [c42f60fa5fca]

1. Audit: open every flow named "abandoned cart" and read the trigger. If it is Checkout Started, rename it "Abandoned checkout". `[verify UI]`
2. Confirm Added to Cart fires: Analytics > Metrics, look for the Shopify "Added to Cart" metric with recent events. If absent, install Klaviyo's onsite snippet (01): theme editor > product template > add Custom Liquid block > paste > save; or theme code under the body tag wrapped in `{% if product %}` and `{% endif %}`. Test: open the store with a UTM carrying a test email, add to cart, find the profile, confirm an Added to Cart event. `[web check: whether the integration now sends it natively]`
3. Cart flow: create flow > search "cart" > the template whose trigger is Added to Cart (Shopify version, not API or manual). Filters: checkout started 0 since starting this flow; placed order 0 since starting this flow; not in this flow in the last 14 to 30 days (7 or less for weekly consumables). Remove the template's SMS branch unless SMS is live (then see P22).
4. Delay 30 minutes (test 15 minutes vs 1 hour, later 2 vs 4 hours). Email 1 > 1 day > Email 2 > 1 day > Email 3 > 1 day > Email 4 > 1 day > Email 5 > conditional split "placed order at least once over all time". Yes: Email 6A founder support, no discount (or a smaller one plus a final reminder 1 day later). No: Email 6B discount with 48 hours > 1 day > Email 7 plain-text 24 hours left.
5. Dynamic item block: split block, event image variable left, item name and price right, linked to the cart page or item. Content per R60. Product-specific proof in emails 3 and 4 via a collection split where the catalogue has a few main collections.
6. Checkout flow: clone the cart flow > name "Abandoned checkout" > trigger Checkout Started in the clone dialog. Delete the "checkout started 0" filter. Replace the dynamic block with the checkout table block (variables differ; never copy the cart block). Link every image and button to `{{ event.extra.checkout_url }}`. Rewrite for checkout objections (shipping fee, payment, delivery time); offer free shipping rather than a percentage where shipping is the objection (04).
7. Smart sending off and UTM on for every email in both flows; the clone resets nothing, so check each.
8. Check: preview each email with 3 profiles; confirm images, names, prices and links; add an item with a test profile and confirm entry into cart but not checkout; start checkout and confirm the cart flow exits and the checkout flow enters.
Rollback: set new emails to manual; the old checkout flow keeps running.

### P9. Post-purchase flow

Sources 01, 02, 03, 04. [58bdfe185e63] [5956a124a134] [55898f20e161] [0a935c9bd091] [9f9c84a1b824]

1. Flows > template "Post purchase follow-up order count split" or "Customer thank you" (04), or build your own. Trigger: Placed Order. `[verify UI]`
2. Filters: placed order 0 since starting this flow; cancelled order 0 since starting this flow. Optional: route subscription or B2B customers to their own flow.
3. Delay 10 to 30 minutes (Shopify's confirmation fires at once). Conditional split: placed order equals 1 over all time. Yes: first-time track. No: returning track (same shape, loyalty wording, no acquisition offer).
4. First-time track per R68: (1) founder thank-you, plain text, PS add-on within 24 hours; wait 1 to 2 days; (2) "on its way" with add-ons or a product feed; wait until expected delivery; (3) how-to, split by product or category; wait 3 days; (4) follow 1 social channel; wait 3 days; (5) loyalty program benefit; wait 3 days; (6) review request (or hand this to the reviews app's flow); wait 4 to 7 days; (7) founder check-in "how did everything go?"; optional (8) cross-sell with 48 hours then a 24-hour plain-text closer.
5. Do not fix a time of day; send relative to the order.
6. Smart sending off, UTM on. Check: preview with a first-time and a returning profile; confirm a cancelled order exits.
`[needs brand data: delivery times per region to set delays]`

### P10. Win-back flows (data-driven and predictive)

Sources 01, 03, 04, 09. [021057848a4f] [4bfa7e9cadf3] [61b12124e33c] [109f8c9de246]

1. Pull days between order 1 and order 2 from Shopify or Metabase; compute median and mean in code. Pick a point between them (03) or 2 times the average (01, 09); sanity check against days of supply plus shipping. `[needs brand data]`
2. Flows > Klaviyo "standard winback" template or build your own. Trigger: Placed Order. Filter: placed order 0 since starting this flow. First delay: the number from step 1 (not the template's 75 days). `[verify UI]`
3. Emails: (1) "It's been a while", new arrivals, no discount; wait 3 to 7 days; (2) reminder; wait 7 days; (3) unique dynamic code, 48 hours; wait 1 day; (4) plain-text 24 hours; optional wait 14 days; (5) bigger offer, 48 hours; (6) 24 hours plain text.
4. Optional split: historic or predicted CLV at least $1,000 gets a stronger, more personal offer.
5. Manage flow > add past profiles > "throughout the flow" so the first sends do not wait; this needs a static code, so use one in the first run.
6. Predictive version (03): flows > create manually > trigger date property "expected date of next order" > start on the date, 12 PM recipient local time, repeat never > filter placed order 0 since starting this flow > delay 5 days > first win-back email. Needs enough order history for predictions to populate.
7. Check: preview counts of entrants per week; confirm no active subscriber enters (filter on subscription tag).

### P11. Sunset flow and monthly suppression

Sources 02, 03, 04. [56d433c32a2b] [c57d2fe2264a] [171bd57ff251] [6dcb0bfce104]

1. Segment "Sunset trigger": can receive email marketing AND opened email 0 times in the last 120 (or 180) days AND clicked email 0 times in the last 120 (or 180) days AND received email at least 6 times in the window (04). Decide whether past buyers are excluded (02 keeps them; see 7.9). `[verify UI]`
2. Flows > build your own > "Sunset". Trigger: added to segment = Sunset trigger.
3. Profile filters: opened email 0 times since starting this flow AND clicked email 0 times since starting this flow (AND, not OR).
4. Email 1 immediately, plain text: "You haven't opened our emails in a while. Still interested? If not, unsubscribe here." Wait 5 days. Email 2: strongest offer, unique code. Wait 5 days. Email 3: "we'll remove you unless you click below to keep receiving updates". Wait 5 days. Update profile property: unengaged = true.
5. Segment "To suppress": unengaged = true AND can receive email marketing.
6. Monthly: segment three dots > suppress current members (04) or export CSV and import to suppressed profiles (03). Also suppress marked-as-spam, hard bounces and 4+ soft bounces. Takes 1 to 2 hours to update.
7. Check: preview count before suppressing; confirm the count is not most of the list (if it is, run P17 first).
Rollback: unsuppression rules differ; check Klaviyo before suppressing. `[web check: Klaviyo unsuppress rules]`

### P12. Core segments

Sources 01, 02, 03, 04. [c049ecf47935] [516248e6ac94] [9720dfa509a1] [ff7571c5eb99] [951b0132a90b] [171bd57ff251]

1. Audience > lists and segments > create segment. Build "Engaged 90": condition group 1 (OR): opened email at least once in the last 90 days (where Apple privacy open is false, if available); clicked email at least once in the last 90 days (bot click false); placed order at least once in the last 90 days; checkout started at least once in the last 90 days; active on site at least once in the last 90 days; subscribed to list at least once in the last 14 days. AND group 2: can receive email marketing (EU: because person subscribed). AND group 3: bounced email 0 times over all time; marked email as spam 0 times over all time. Check the preview count. `[verify UI]`
2. Clone for 14, 30, 60, 120, 180 and 365 days by changing the windows.
3. Clone Engaged 90 into "Engaged 90 prospects" (AND placed order 0 over all time) and "Engaged 90 customers" (AND placed order at least 1).
4. Exclusions: "Marked spam" (marked email as spam at least once over all time); "Bounced" (bounced at least once where type = hard, OR at least 4 times where type = soft); "Unengaged 180" (0 opens, 0 clicks, 0 site events in 180 days, received at least 6).
5. Buyer stage: non-buyers, first-time, returning, VIP (4+ orders or spend at 3 to 4 times AOV), high potential (site activity 30 days, 0 orders 30 days), win-back potential (order in 180 days, none in 90), abandoners (cart or checkout 90 days, 0 orders 90 days), window shoppers, interested in X, cross-sell X to Y.
6. Check each: AND and OR groups match intent; preview counts make sense (engaged under the list size; unengaged not larger than engaged unless the list is dead); clone rather than rebuild; unused segments go inactive after 45 days.

### P13. Build and send a campaign

Sources 01, 03, 04. [5b2cad894e44] [81300e87c081] [ba5c04225d61] [a891648996f4]

1. Campaigns > create campaign. Name, date, channel email, tags (type and pillar) for later analysis. `[verify UI]`
2. Send to: the engaged segment for the send (90 days evergreen; 365 days for Black Friday and big launches). Don't send to: marked spam, bounced, unengaged 180, and any dynamic exclusion (bought in the category in the last 3 days). Tick "determine recipients at send time".
3. Smart sending on (off only for a launch where a flow email in the last 16 hours should not block it). UTM on.
4. Content: subject (short, value first, curiosity), preview (adds a second reason), sender name, sender email. Template: saved template or new; drag in slices and live text (P18). Keep the unsubscribe block.
5. Optional follow-up resend (P19). Optional A/B test (P15).
6. Review screen: estimated recipients (included minus excluded), smart sending state, subject, preview, from and reply-to, unsubscribe link present, tracking on. Send a test to yourself; click every link on phone and desktop.
7. Schedule: fixed time (example 9 AM in the brand's main time zone, or recipient local time). For a launch, at least 1 email the morning the product goes live.
8. After 24 hours read placed orders and revenue per recipient, then clicks; log the result against the pillar.
Rollback: cancel the scheduled send before send time; a sent campaign cannot be recalled.

### P14. Monthly campaign calendar

Sources 01, 02, 04, 10. [6a19f9f385b5] [e5552f0a655e] [7a4e669c2511] [3e4696a51c71] [9641bcb4fcd1] [85157d54ac6e] [9077e5d437cb]

1. Tracker: Notion, Airtable, ClickUp, Monday or a Google Sheet. Fields: send date, campaign type and pillar, segment, status (idea, copy, design, build, review, scheduled, sent), owner, result. `[needs brand data: existing tracker]`
2. Set the monthly count: cadence x weeks (example 3 a week, 12 to 14 a month) on fixed send days (example Tue, Thu, Sun).
3. Lock fixed dates: launches, real restocks, planned sales (max 1 sales event a month; every other month is better), milestones. Add 2 to 3 supplementary sends per event (teaser, launch, reminder, last chance).
4. Add 1 to 2 awareness days that fit (nationaltoday.com or checkiday.com). No discount needed. `[web check: dates for the month]`
5. Map existing content to season (a summer skincare blog in May, not November): tease and link, or summarise and link to product.
6. Fill the rest with micro-topics from R104 and R105. Optional: an AI prompt with the brand context, cadence, fixed dates, content placed and the idea list; expect about 80% usable; check every idea for fit, assets and claims.
7. Mix check: per month 1 to 2 promo, 4 to 6 product, 4 to 6 education, 2 to 4 social proof, 2 to 4 brand; promo under one third; at least 5 non-discount per discount; no 2 consecutive of the same type; graphic to text about 3 or 4 to 1 with 1 to 3 plain-text sends.
8. Stay 2 weeks ahead: emails 2 weeks out are written, designed and in Klaviyo for review.
9. Month end, 20 to 30 minutes: top revenue, most clicks, lowest performers and why; feed patterns into next month (P25).

### P15. Campaign A/B test and send-time test

Sources 02, 03, 04. [ac370b420628] [4290660b631a] [659e9f913086] [eed1632440b9] [9211d9b5ff9c] [8cab23f94038]

1. Content test: build A; "create A/B test" > test content; change 1 element (offer, products featured, lifestyle vs product image, 1-image vs 4-image hero, CTA copy, product blocks vs none, categories vs products, long vs short). Name variations descriptively. `[verify UI]`
2. Winning metric: placed order rate. Test size 100% (50/50). Winning variation rollout 0%. No automatic winner.
3. Send-time test: "test send time"; 2 far-apart times (7 AM vs 7 PM); winning metric placed order rate (03 uses click rate here); size 100%. Repeat over 5 to 10 campaigns, compare average revenue, then narrow (7 vs 11 AM, then 11 AM vs 2 PM). Do not adopt Klaviyo's Smart Send Time, which optimises opens.
4. Read in the experiments section after 2 to 3 days: lift, win probability, significance. If Klaviyo warns the test-period winner differs from the overall winner, rerun longer and bigger. Small lists may accept a 98% win probability without significance as a judgement call (03).
5. Apply the learning to future sends and to flows; retest before assuming it transfers.

### P16. A/B test inside a flow

Sources 01, 02, 03, 04. [74b2b4379cdb] [1c24d38d786b] [0528a2003316] [5f42a553bc22] [b5c1274e5d10] [e753b3fb98af]

1. Timing test (manual split): before the first delay add a conditional split "random sample 50%". Yes path: delay A (30 minutes). No path: delay B (2 hours). Clone every email onto both paths; do not rejoin after email 1. Wait for 1,000 recipients per branch (500 if the gap is huge), about 2 weeks. Decide on placed order rate and revenue; watch spam complaints. Narrow next (if 4 hours beat 1, test 3 vs 4). `[verify UI]`
2. Structure test: regular (1 email a day) vs aggressive (every 12 hours) on the same split.
3. Content or subject test on 1 email: open the flow email > "create A/B test" > change 1 element in B > distribution manual 50/50 (turn off automatic, which can favour a variant too early; use automatic only if nobody can check) > winner by click rate (placed order rate is not offered at email level in 04's UI) > end by significance or manual > write the hypothesis in notes. `[verify UI]`
4. Test order: email 1 of welcome, then cart, checkout and browse; delay first, then content; skip flows with about 20 recipients a month.

### P17. Deliverability repair ladder

Preconditions: opens on engaged sends (Apple opens excluded) under 30% to 40%, or a placement test showing spam or heavy promotions, or a new domain. Sources 01, 02, 03. [0f792188c5ee] [20fd44bca0dd] [df98522f016b] [98d43fdb4da1] [6dcb0bfce104] [75378f892825]

1. Diagnose: last 5 campaigns > deliverability tab: open, click, bounce, unsubscribe, spam by inbox provider and by country. Run a GlockApps seed test (inbox vs promotions vs spam, blocklists, IP reputation). Confirm P2 is complete. `[verify UI]` `[web check: GlockApps]`
2. Improve the emails first (R145): varied layouts and topics, 1 above-the-fold CTA, live text, category footer, plain-text sends, replies invited.
3. Clean the list (R147): build the 5 cleaning segments and bulk suppress.
4. Build engaged 14, 30, 60, 90 (P12). If spam problems are severe, use opened or clicked only.
5. Weeks 1 to 2: turn off all flows except welcome, browse, cart, checkout, post-purchase (and site abandonment per 02). Send 3 strong campaigns a week to engaged 14 only.
6. Gate: after 6 sends (2 weeks) or 3 straight sends at 50%+ opens, move to engaged 30. Below 50%: stay 2 more weeks; still below: remove site activity from the segment and recheck content.
7. Repeat the gate at 30, then 60, then 90. At 90 make it the main audience and turn all flows back on. Widen to 120, 150 or 180 only while opens stay above 50% and only for some sends.
8. From week 6 onward (01): 1 normal campaign a month to the wider list so anyone who opens rejoins the engaged segment (or none, per 03; see 7.10).
9. Where 1 provider stays weak, build a tighter engaged segment for that provider (03).
10. If a country is weak, send only a tighter engaged segment there for a while (02).
Rollback: if opens fall at any stage, step back down 1 window and hold 2 weeks.

### P18. Email build: Figma slices plus live text, into Klaviyo

Sources 01, 03, 04, 07; live-text rules from 02, 04. [54eb9e4fd217] [1fa479fcc307] [8f1c460f5eed] [17b5705e3605] [046d714ac94c] [31b2f58bfc95] [8ae50e9df495] [2dabf0e92513] [acc8bc585d69]

1. Copy first: lay out the email in a Google Doc as a table, 1 row per section (logo, headline, sub-headline, body, CTA, hero, bridge or infographic, products, closing CTA, footer). Write per R111 to R121.
2. Figma: frame 600 px wide. Logo bar 600 x 100. Hero image 600 wide, cropped to about 600 x 500 so the next section shows soon; gradient overlay for text over faces. Button: rounded rectangle (radius 30 to 65), contrasting fill, text layer above. Bridge section with a shared background colour and gradients so sections do not look blocky; icons, not bullets. Product section: each product with its own Shop Now, rating and short descriptor; end with a general button. Us vs them block: brand left, competitor right, check and X icons, only true and provable points (no competitor names). Footer: category links, trust icons, social icons; legal and unsubscribe are added in Klaviyo. `[verify UI]`
3. Leave short text (headline, code, offer bar, footer text) out of the slices; rebuild those as live text in Klaviyo (R130).
4. Slice: 1 slice per link target (each product, each social icon, logo, hero, each button); never 1 giant image; export 2x JPEG or PNG.
5. Compress all slices in a batch (tinypng, iLoveIMG or Squoosh; typical 50% to 75% smaller). Check quality.
6. Klaviyo: create the email; delete default blocks except the unsubscribe footer. Add image blocks in order; padding 0 between stacked slices, about 20 px between sections; "full width on mobile" where needed. Add live text blocks for headline, code (bold before the CTA), offer bar; use native product blocks (static or a dynamic feed: bestsellers last 30 to 90 days, exclude low stock and items under a price floor) rather than image product grids where possible. Table block with image cells for side-by-side icons. `[verify UI]`
7. Link each image and button to the most specific page (product or collection, never the homepage); use the discount URL pattern to auto-apply codes; alt text on every image, including the offer text.
8. Text styles: 18 px desktop, at least 16 px mobile, line height 1.5, brand font with a web-safe fallback. Save the footer as a universal block.
9. Check: email size small enough to avoid Gmail clipping (04's demo: 35 KB); view with images off, the offer, products and footer still read; preview on phone and desktop; test send; click every link.
`[web check: Gmail clipping threshold]`

### P19. Resend to non-openers

Sources 01, 03. [d11a34c7dc7f] [6964a9fc308f]

1. Klaviyo sequence builder: toggle the follow-up on the campaign; new subject line; narrow the audience (first send engaged 90, resend engaged 30); delay cannot be under 48 hours. `[verify UI]`
2. Manual method (for sooner than 48 hours or Black Friday): copy the sent campaign's message ID from the URL; segment: received email at least once where message = ID AND opened email 0 times where message = ID; clone the campaign; change the subject and preview; send 1 to 2 days later. Rebuild the segment per campaign. On Black Friday do 2 to 3 manual resends.
3. Use only for launches, big sales and big announcements.

### P20. SMS setup in Klaviyo

Sources 09, 11, 12. [af694ec3e7e4] [ef374a64ba7e] [aa2a2140c1a0]

1. Decide the platform: Klaviyo if email is in Klaviyo; get a quote, take it to Attentive and Postscript, decide on price and ease, not AI features. `[web check: pricing and contract terms per country]`
2. Klaviyo: company name > Settings > SMS > set up SMS. Sending countries (each country has its own credit cost and rules; India needs DLT registration and template approval). Fill the form; toll-free or short code verification follows. Sender name = brand. `[verify UI]` `[web check: number types, registration and verification per country]`
3. Upload existing SMS subscribers only with consent records. `[needs brand data: consent records]`
4. SMS message add-ons: opt-out language (keep STOP; do not shorten to "unsub" unless the platform and carrier accept it). Terms of service and privacy links. `[web check: required disclosures]`
5. Sender preferences: SMS Smart Sending on (max 1 SMS campaign per person per 24 hours). SMS quiet hours on, set to the strictest legal window across send countries in recipient local time. `[web check: quiet hours per country and state]`
6. Keyword responses: JOIN keyword with an optional discount.
7. Check: send a test to a team phone; reply STOP and confirm the profile unsubscribes; confirm a send scheduled inside quiet hours is held.

### P21. SMS phone-capture step

Sources 09, 11, 12; P3 step 6 holds the form settings. [75893d2892aa] [9b9305f19394] [775acf1e29be]

1. Email step first with the full offer ("You've got 20% off"). Button "Claim now".
2. Phone step: "Finish signing up with text to activate your 20% off." Consent text with required disclosures, legible. Button "Claim now". No extra discount for the phone (09, 11); if the owner wants to test a bigger SMS offer or a VIP club (04), run it as an A/B test with the welcome flow revenue as the judge.
3. Track email submit rate and phone submit rate separately by device. Target: phone submit near 15% of form viewers with a quiz-first form (09's brands, vendor tool).
4. Check: a submitted phone lands in the SMS list with consent timestamp; the SMS welcome flow fires; the email welcome flow still fires for people who skip the phone step.

### P22. SMS flows

Sources 09, 11, 12, 05. [6c2a73b99726] [ee1a31c09fcc] [136997a1cb23] [586799a976b3] [c2903035a7f5] [71d9f81273f0] [c2cd726a16ab]

1. Welcome (trigger: subscribed to SMS via the form): text 1 immediately: "Welcome to [brand]. [1 short remark]. Use code WELCOME20 for 20% off your first order. [link]". Wait 2 days. Text 2: 1 differentiator plus code reminder. Wait 2 days. Text 3: "Your 20% off expires soon. [link]" only if it truly expires. Optional last text: "Any questions I can answer?" (05). Filter: placed order 0 since starting this flow. `[verify UI]`
2. Abandonment (4 flows or SMS steps inside the email flows): browse after 60 minutes; cart and checkout after 1 to 2 hours; site after 2 to 4 hours. Exactly 1 SMS per person per flow within 48 hours; Klaviyo enforces this on cart abandonment (09). Filters as in the email flows plus "has SMS consent". Split placed order at least once: non-buyers get "Looks like you forgot something. Finish your order [link]. Use code WELCOME20"; buyers get the reminder without a code. Test plain text vs 1 product image on net profit.
3. Sequence with email: pick 1 pattern per 7.15 (same time; SMS first then email after 2 hours if no order; email first then SMS 5 to 6 hours later) and hold it for the test period.
4. Post-purchase: 1 text on day 10 to 14: "Are you liking [product]? [cross-sell link]". Replenishment brands: text at days of supply plus delivery minus 2 to 3 days: "Running low? Reorder here". No offer at first.
5. Win-back: at 60 to 90 days or 2 times the average interval: flash offer, 72 hours, unique code; wait 2 days; "last chance".
6. Check every text in the segment counter (1 segment, GSM-7), with the opt-out text and link included; confirm quiet hours hold sends; confirm buyers exit.

### P23. SMS campaign calendar and cost check

Sources 09, 11, 12. [7eaef73fe8eb] [77dd2ea812e0] [3f1ec5d057e8] [ec74b2c055f2] [0228dbaf571e] [13f23c2e8c94]

1. Base cadence: 1 a week (11, 12) to 2 a week (09). Never more than the level the holdout (P24) has proven. Active subscription customers: no campaign texts.
2. Lock events: launch (teaser 1 to 2 days before, launch day, reminder 2 to 7 days later with real stock news), flash sale (day 1, last chance on the last day, sent by 6 to 7 PM with a real deadline), real restocks, SMS-exclusive offers, early access.
3. Fill gaps over 1 week with 1 to 2 real news items (giveaway, hero product spotlight, 1 brand send). No nurture, no testimonials, no evergreen bestsellers.
4. Pair key sends with that day's email (7.15). Send inside 11 AM to 3 PM local; never inside quiet hours.
5. Cost check per send: characters (GSM-7, 160; Unicode, 70), segments, credits, MMS only where the image has a net-profit case; compute expected cost = recipients x segments x rate in code.
6. After each send log revenue per message, clicks, unsubscribes and net profit.

### P24. SMS holdout test for cadence

Source 05. [651884bb18e3] [bb28c48148d6] [52f701ac2a63]

1. Baseline: messages per subscriber per month, revenue per message, channel revenue, unsubscribe rate (and first-30-day unsubscribes).
2. Randomise SMS subscribers into 3 cells: 50% current cadence, 25% no campaign texts, 25% double cadence (flows keep running for all).
3. Run long enough to read revenue (05 gives no length; size it from weekly revenue per subscriber). `[needs brand data: list size, revenue per subscriber]`
4. Compare revenue per subscriber in each cell against the no-message cell; subtract message cost from the extra revenue of the 2x cell. Compute in code.
5. If 2x beats holdout with confidence and unsubscribes hold, adopt it as the new baseline; else keep the base. Step up by 1 message a week (or every 2 weeks) and repeat; stop at the first rise in unsubscribes. Change 1 lever at a time.

### P25. Monthly review

Sources 03, 02, 11. [5d6743fc3f40] [d66d62f1a9cd] [41d10e199bc4] [8183b1fcc7d0] [d2e68173f29a] [3dca25bfe545] [bd8384e14e34] [02f841a00c26]

1. List growth: profiles > subscriber growth, 30 days: total, gained, lost, trend. Opt-in sources: checkout vs each pop-up. If checkout signups fell, compare with Shopify orders; only a gap means a broken sync. `[verify UI]`
2. Each pop-up: views and submit rate vs the prior 30 days. Views down with rate flat = traffic, not the form. Views near 0 after a theme update = the embed is off. End or continue the running test; set next month's test.
3. Campaigns: last 30 days sorted by revenue; then clicks and placed orders; then the lowest performers. Read order count with revenue. High-engagement, low-revenue newsletters get reformatted, not killed.
4. Experiments: lift, win probability, significance; rerun any test with a period-vs-overall warning.
5. Dashboards > business review: this month vs last (or last year if seasonal): Shopify revenue, attributed revenue, email share, campaign vs flow split. Walk the chain: recipients, unique opens, open rate, unique clicks, click rate, unique conversions, conversion rate, revenue, revenue per recipient, AOV. Under 5% is noise; explain anything over 10%.
6. Flows: revenue vs site traffic first; then the chain; then top flows vs last month; open any flow with a big gap: per-email rates and skips. Skips by design are fine; skips by accident mean a filter or split is wrong.
7. Deliverability tab: score and trend; bounce, spam, unsubscribe against R139 to R141; reports by inbox provider; flows flagged for high bounce or low click.
8. Segments: sizes of engaged, unengaged, bounced and spam; run the monthly suppression (P11).
9. SMS: cadence, clicks, unsubscribes, delivery, revenue per message, net profit; pick 1 lever for next month.
10. Write the month's 3 findings and the next 3 tests into the tracker.

### P26. Copy research routine before a new angle

Source 08; 01 for brand voice. [4dac36087f55] [d4e3dc152180] [100c73502444] [94e80b540e5c] [3c8f273100f4]

1. Baseline: GA4 or Meta audience demographics (age, gender, interests). `[verify UI]`
2. Meta Ad Library: search the category, country = main market, media = video, note competitors with many ad versions, open Page transparency for history, note the lead angle. Search the problem keyword too, and note what people dislike about incumbent solutions. Competitor ads are signals, not proof.
3. Amazon (target country): category and adjacent products, many reviews, filter Most Recent; log practical complaints, category-level objections, and what positive reviews praise (the buying barrier). Trustpilot and BBB for more. 30 to 60 minutes per category.
4. Podcasts and thought leaders for the science; comment sections for objections. Verify any study before quoting it. `[web check]`
5. The brand's own Instagram language, blog, support tickets and reviews tagged by objection.
6. Research doc (Notion): angles, benefits with mechanism, perk vs insecurity anchor, pains and the insecurity under each, honest external causes, objections with the brand's proof for each. 2 to 4 hours total; then 10 to 20 minutes per email.
7. Every claim that reaches a draft is checked against the brand record (R191).

### P27. AI analysis of Klaviyo exports

Source 02. [7dccf4216521] [87afe3ecbaf6] [a0d2e94690df]

1. Campaigns > three dots > export analytics > last 90 days or year to date > email only > include all A/B variations > CSV. Flows > options > export analytics > same range > aggregate by day > CSV. `[verify UI]`
2. Prompt: "You are an email marketing data specialist. Analyse this data set of email campaigns for [brand URL] and give me 10 observations with recommendations." Repeat for flows with 20 observations; then "focus on the welcome series and give me 10 findings".
3. Treat every finding as a hypothesis; check it against the CSV in code (revenue per recipient by email, opens by day, send-time clusters); turn the survivors into P15 and P16 tests. Optimise placed order rate, not opens.

## 5. Diagnostic checklists

Each row: what to check | how | good | bad | fix | source. A worker runs the rows top to bottom and records the result per row.

### 5.1 Flow audit (coverage, triggers, timing, exits)

| What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Coverage | List live flows | Welcome, site, browse, cart, checkout, post-purchase, win-back, sunset live; replenishment, back in stock, review, birthday where the brand needs them | Any core flow missing | Build in revenue order: welcome, cart, checkout, browse, post-purchase, site, win-back, sunset (P5 to P11) | 01, 04 [31dde167599f] [b8acdbab97a3] |
| Real cart flow | Read the trigger of every "abandoned cart" flow | 1 flow on Added to Cart and 1 on Checkout Started | Only Checkout Started | P8 | 01, 02, 03, 04 [d962429e9e36] [85117c7d0910] |
| Added to Cart metric | Metrics tab, recent events | Shopify Added to Cart fires | Missing or API-only | P8 step 2 | 01, 02 [34204d0c3ce5] |
| Welcome trigger and list | Open trigger; compare with each form's list | Same list | Mismatch (flow never fires) | Point trigger at the form's list | 01 [3b8a84dc1d94] |
| Welcome exit | Profile filters | Placed order 0 over all time (or since start) | No buyer filter | Add filter | 02, 03 [07f1b027ac4e] |
| Welcome timing | Delays | Email 1 at 0; day 0 to 3 carries most sends | 3-day default gaps; 1 email only | P5 | 02, 03, 04 [f2c3f6895ad4] |
| Welcome length and code | Count emails; search each for the code | 6 to 8 emails, code in every one | 1 email, or code missing | P5 | 01, 04 [b0ac0c5d9d9b] |
| Overlap filters | Each flow's filters | Cart has checkout 0; browse has cart 0; site has viewed 0; all "since starting this flow" | People get 2 flows at once | Add exits | 01, 02, 03, 04 [b6389565ed83] [9da5ac313720] |
| Re-entry rule | "Has not been in this flow" | 30 days browse; 7 to 30 cart and checkout by cycle | None, or 7 days on a slow cycle | Set per R57 | 01, 02, 04 [5ad3da1bdb3a] |
| First delays | Delay steps | Site 1 to 4 h; browse 30 min to 2 h; cart and checkout 15 min to 1 h; post-purchase 10 to 30 min | Klaviyo defaults (4 h cart, 1 d post-purchase, 3 d welcome) | Set per R35, then test (P16) | 02, 04 [d94eb68e5e18] |
| Smart sending | Each flow email's settings | Off | On | Untick "skip recently emailed" | 02, 04 [b837f7435caf] |
| UTM | Each email | On | Off | Turn on | 03, 04 [8796c9f1ffa6] |
| Discount timing | Read email 1 to 3 of browse, cart, checkout | No code before email 4; buyers get support not code; real deadline | 20% in email 1; static code with fake expiry | R36, R37 | 01, 02, 04 [bdbde349add0] [a69de45ff438] |
| Dynamic blocks | Preview each recovery email with 3 profiles | Image, name, price, link load; checkout links to checkout_url; browse links to product | Blank, wrong item, homepage link | P8 step 5 and 6; P7 step 4 | 01, 03 [c42f60fa5fca] [79cdac8bb86e] |
| Post-purchase split and cancel filter | Filters and split | First vs returning split; cancelled order 0 | No split; refunds get cross-sells | P9 | 02, 04 [9f9c84a1b824] |
| Win-back timing | Delay vs days between orders | Between median and mean, or 2x average | Template 75 or 90 days | P10 | 03, 04 [021057848a4f] |
| Sunset logic | Filters | AND on opened 0 and clicked 0 | OR | Fix | 03 [56d433c32a2b] |
| Flow revenue share | Flow revenue ÷ email revenue | 40% to 60% | About 30% | Extend cart, welcome, post-purchase | 01, 02 [0de6758fd7b5] |
| Flow revenue vs traffic | Both trends | Move together | Traffic up, flow revenue down | Open the flow: skips, filters, blocks | 03 [d2e68173f29a] |
| Skips | Show analytics per email | Skips by design | Skips by accident | Fix filters and splits | 03 [ac6fccd77bd7] |
| Long flows | Complaint and unsubscribe rate by email | Stable | Rising at late emails | Shorten or lengthen gaps | 04 [fac642b0957b] |

### 5.2 Pop-up review

| What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Opt-in rate | Submits ÷ form views, per device | 8% to 12% (03: above 9%) | 1% to 4% | Offer first, then the rows below | 01, 02, 03, 04, 12 [1c9b788208ca] [40691f40d94c] |
| Offer | Read the headline | Clear discount or gift worth the email; % under about $100 to $200 AOV, $ above | "Sign up for updates", 5% off on $500 AOV | R7, R9 | 01, 02, 04 [7ea9228eeda8] |
| Offer economics | Opt-in, total signups, welcome CVR and revenue, margin, site CVR | Revenue up at acceptable margin, site CVR flat | Opt-in up, welcome CVR or site CVR down | Revert or test another offer | 02, 04, 05 [aa555d450d5a] [1282cefafb08] |
| Fields per step | Look at each step | 1 input per step; email then phone | Email and phone together; name, birthday | Split steps | all [9622afcc8844] |
| Micro-yes | First step | Yes/no, quiz or scratch-off, tested | Straight to email, never tested | Test (P4) | 01, 02, 03, 04 [e912865caec2] |
| Trigger | Timing settings | 4 to 12 s delay, OR scroll, desktop exit intent only | Immediate, 30 s, mobile exit intent | R14, R15 (03 differs) | 01, 02, 04, 12 [c5e1f30dd58d] |
| Re-show | Frequency | 3 to 5 days after close; never after submit | Every visit | Set | 02, 04 [d124c18b882e] |
| Devices | Form list | Separate mobile and desktop (or 1 form proven equal) | 1 form with a desktop image on mobile | Clone per P3 step 9 | 01, 02, 04 [c2e8c7484a70] |
| Size and copy | View on phone | About 75% of screen, under 10 words, offer largest | Small, wordy, "exclusive offers" text | R18 | 01 [ff4c8404916f] |
| Close | Every step | Visible X plus "No thanks"; close works on success step | Hidden X; no way out of success step | R189 | 01, 02, 04 [397f14a8dca9] |
| Consent | Every step | Legible consent text; nothing pre-checked | Size 8 text; deleted; pre-checked | R187 | 01, 02, 04 [39aa68c94680] |
| Targeting | Rules | Existing profiles excluded; cart, checkout, wholesale excluded; ship-to countries | Shows to subscribers or at checkout | R19 | 02, 03, 04 [a877dc6c99dd] |
| Teaser | Setting | On, small shape on mobile, no widget collision | Off, or covering chat | R20 (01 differs) | 02, 03, 04 [53f37df1584e] |
| Success page | Read | Code sent by email; spam line | Code shown (allowed if the owner prefers; 01) | R21 | 02, 03, 04 [1f8be190a019] |
| Load speed | Preview on mobile data | Instant | Lag, heavy image | Compress; no image on mobile | 01, 02 [8b8c3454e9e7] |
| Test running | A/B tests page | 1 test, manual 50/50, manual winner, enough sample | Auto winner on low volume; no test | P4 | 02, 03, 04 [00de729163a8] |
| Gamified prizes | Wheel or scratch config | Every shown prize can be won | Decoy slices | R190 | 01, 02 [7da3ea843dc6] |
| Views trend | Views vs prior 30 days | Tracks traffic | Near 0 after theme update | Re-enable embed and form | 03 [5d6743fc3f40] |
| Phone step | Copy and button | "Finish signing up with text to activate"; "Claim now" | "Continue"; "sign up for texts" | P21 | 09, 11 [75893d2892aa] |

### 5.3 Deliverability check

| What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Branded domain | Settings > domains | Active on a sending subdomain | Shared Klaviyo domain, "in progress" | P2 | 02, 03, 04 [a192f5312b82] |
| SPF, DKIM, DMARC | DMARC checker; DNS | All pass and align; `_dmarc` present with reports | Missing DMARC | P2 step 6 | 02, 03, 04 [e758ab334635] |
| DMARC policy | Read the record | none with reports on a new setup; quarantine or reject once aligned | none forever; reject with unaligned sources | P2; 7.6 | 03, 04 [a192f5312b82] |
| One-click unsubscribe | Send a test to Gmail; look for the unsubscribe header | Present | Absent | Klaviyo handles it; verify `[web check]` | 02 [91d6fd433f58] |
| Spam complaint rate | Deliverability tab, last 5 campaigns and flows | Under 0.01% to 0.1% | Over 0.3% | Tighten audience, cut promos, P17 | 02, 03 [6d8587217a67] |
| Bounce rate | Same | Under 1% | Over 1% | Suppress hard bounces; clean list | 03 [6d8587217a67] |
| Unsubscribe rate | Same | Under 0.3% (03 accepts 0.67% with more revenue) | Over 1% steady | Content and cadence | 02, 03, 06 [91d6fd433f58] |
| Opens (Apple excluded) on engaged sends | Campaign reports | 45% to 50%+ | Under 30% to 35% | P17 | 01, 02, 03 [75378f892825] |
| Unique clicks and click rate | Same | Above 0.5% floor; 1.2% okay; trend flat or up | Falling clicks | Content, above-the-fold CTA, live text | 02, 03 [ea472261103e] |
| Placement | GlockApps seed test monthly | Inbox | Promotions or spam share high | P17; R145 | 02 [75378f892825] |
| By provider and country | Deliverability reports | Similar across providers | 1 provider or country far lower | Provider- or country-specific engaged segment | 02, 03 [3dca25bfe545] |
| Audience | Campaign send-to | Engaged segment plus exclusions | Whole list, or a list | P12, P13 | all [bb790bf6e145] |
| Segment logic | Read conditions | AND on "can receive"; OR on engagement | Wrong AND/OR | P12 | 02, 03 [516248e6ac94] |
| List hygiene | Sizes of spam, bounce, unengaged segments; last suppression date | Suppressed monthly | Never suppressed; 10% engaged | P11 | 01, 02, 04 [6dcb0bfce104] |
| Attribution exclusions | Settings | Transactional, bot clicks, Apple opens excluded | Defaults | P1 step 4 | 03, 04 [1ce671434e00] |
| Cadence gaps | Campaign calendar | No week without a send | Weeks of silence then a burst | R101 | 03 [dbd9ab70c7db] |
| Hidden text | Inspect the email source | None | Background-colour text block | Remove; R188 | 01, 07 [bc0f81f5c30a] |
| Image-only | View with images off | Offer, products, footer read as text | Blank | R130 | 02, 04 [31b2f58bfc95] |
| Warm-up | New domain or long silence | Engaged-only 2 to 4 weeks, steady volume | Full list on day 1 | P2 step 4; P17 | 04 [fc0425a31c0f] |

### 5.4 Campaign send checklist (run before every send)

| What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Audience | Review screen | Engaged segment; exclusions attached; recipients at send time | List or whole list; no exclusions | P13 step 2 | 03, 04 [81300e87c081] |
| Smart sending | Review screen | On (off only for a launch) | Off by accident | Toggle | 03 [ba5c04225d61] |
| Pillar and mix | Calendar | Fits the month's mix; not the same type as the last send; promo under one third | 2 promos in a row | Swap | 02, 04 [7a4e669c2511] |
| Subject and preview | Read on a phone | Short, value first, curiosity; preview hand-written and adds to it | Full sentence cut off; default preview | R118 | 01, 03, 04, 06 [685553ea4865] |
| One message | Read the draft | 1 takeaway, 1 CTA goal | 3 topics, 5 CTAs | Split or cut | 01, 03 [945e9b8a355c] |
| Above the fold | Phone preview | Headline, 1 to 2 sentences, big button, code if promo | Button far down | R123 | 01, 04, 07 [d1327991a91c] |
| Claims | Compare with brand record | Every claim, count, guarantee, logo matches | Invented or AI claim; "as seen on" without appearance | R191 | 08, 10 [f0580c1b1e80] |
| Urgency | Read | Real deadline, real stock | "Expires tonight" that does not | R37, R186 | 02, 04, 08 [8ae593fcc226] |
| Reviews | Read | Each answers an objection; no face on sensitive topics | "I love it" only | R115 | 02, 08 [6e5742c076f2] |
| Products | Count | 3 to 5, each with a button, 1 per row or 2x2 | 8 products, 3x2 grid | R126 | 02, 04, 08 [46502d7fa9bc] |
| Images | Each image | Alt text with offer; deep link; compressed; 1 link per slice | Missing alt; homepage link; MB files | R129 | 01, 03, 04, 07 [17b5705e3605] |
| Live text | Images off | Offer and footer readable | Blank | R130 | 02, 04 [31b2f58bfc95] |
| Discount code | Layout | Bold, right before the CTA; auto-applies via URL; exists in Shopify | Buried; code not created | R123; P18 step 7 | 03, 04 [82bb67e79aeb] |
| Footer | Bottom | Unsubscribe, address, category links | Missing | R132 | 03 [5fde08efd3f8] |
| Size | Klaviyo shows it | Small (04: 35 KB) | Near clip limit | Compress, cut | 04 [046d714ac94c] |
| Test send | To self on phone and desktop | Every link works; renders clean; no odd padding | Broken link | Fix, resend test | 01, 03, 04, 07 [bcc326384a22] |
| A/B test | Settings | 1 variable, 50/50, 100%, placed order rate, manual winner | Auto 20/20/60 | P15 | 02, 03, 04 [ac370b420628] |
| Schedule | Time | Planned slot; launch morning; recipient local if used | Random | P13 step 7 | 03 [5b2cad894e44] |

### 5.5 SMS compliance and quality check

| What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Consent | Segment definition; consent records | Only explicit SMS opt-ins with timestamp and source | Email-only or imported without consent | Remove; R153 | 09, 11, 12 [ccceb9ed6344] |
| Consent wording | The phone step | Required disclosures for each send country, legible | Missing, shrunk | R187; `[web check]` | 01, 11 [9b9305f19394] |
| Opt-out | Reply STOP to a test | Unsubscribes at once; STOP text in messages where required | "unsub" only; iMessage without STOP | P20 step 4; R153 | 11, 13 [af694ec3e7e4] |
| Quiet hours | Platform setting and schedule | On; strictest legal window per country in recipient local time; India DLT window | Off; 8 AM to 9 PM assumed for all countries | R154; `[web check]` | 11, 12 [a9df8fb1a06e] |
| Sender registration | Platform | Verified toll-free or short code; DLT headers and templates approved (India) | Unregistered | P20 step 2 | 11 [af694ec3e7e4] `[web check]` |
| Messages per abandonment flow | Open each flow | 1 SMS within 48 hours (welcome up to 2 to 3) | 2 or more | R162 | 09, 11 [ee1a31c09fcc] |
| Frequency | Count campaigns per week | 1 to 2 (or the holdout-proven level); 0 to active subscribers | 3+ without a holdout; texting active subscribers | R156, R157 | 09, 11, 12 [6f21ea67f481] |
| Content | Last 30 days of sends | Launch, restock, sale, exclusive, real news | Testimonials, evergreen, "restock" that did not restock | R152, R186 | 09, 12 [e6323f097649] |
| Length and cost | Segment counter | 1 segment; no stray Unicode | 2+ segments; emoji | R158 | 09, 11, 12 [0228dbaf571e] |
| MMS | Share of sends with images; net profit | Only where profit is proven | Habit images | R159 | 09, 12 [13f23c2e8c94] |
| Send time | Schedule | 11 AM to 3 PM local; last chance by 7 PM | Early morning, late night | R155 | 11, 12 [5a21fae6ffd5] |
| Email pairing | Flow and campaign timing | 1 chosen pattern (7.15) | Both channels within minutes by accident | P22 step 3 | 03, 11 [fbfeb91636ec] |
| Metrics | Campaign reports | Click 5% to 15%; unsub under 1%; delivery over 90% | Below | R166 | 11 [02f841a00c26] |
| Incrementality | Holdout on file | Holdout read exists once the bill passes about $10K a month | None | P24 | 05 [9a17b76595cd] |
| Conversation replies | Reply queue | Staffed; response target; objections tagged | Replies unanswered | R169 | 05, 13 [3e359a2bee9b] |
| Identity and honesty | Read texts | Store named; no fake typos; no fake person | 13's tactics | R193 | 13 [324169289900] |

### 5.6 Monthly review checklist

| What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| List growth | Subscriber growth 30 days | Gains above losses; opt-in tracks traffic | Losses above gains | Pop-up review; content | 03, 06 [d66d62f1a9cd] [c1faaf881fc4] |
| Opt-in sources | Checkout vs pop-ups vs Shopify orders | Same direction | Gap | Check sync | 03 [d66d62f1a9cd] |
| Pop-up test | A/B page | Decided or still sampling | Auto-ended early | P4 | 03 [ea0cb89619eb] |
| Email share of revenue | Business review | 30%+ and stable (attribution known) | Well below, or falling | R2 audit | 03 [465d3381b2a7] |
| Campaign chain | Metric chain | Driver named | Headline only | R182 | 03 [8183b1fcc7d0] |
| Flow chain | Flow revenue vs traffic, then chain | Explained | Unexplained drop | 5.1 rows | 03 [d2e68173f29a] |
| Deliverability | 5.3 | All rows good | Any bad | P17 | 02, 03 [3dca25bfe545] |
| Suppression | Date of last run | This month | Skipped | P11 | 01, 04 [c049ecf47935] |
| Mix and cadence | Calendar counts | Per R100 to R103 | Promo-heavy; gaps | P14 | 02, 04, 10 [e5552f0a655e] |
| Tests | Experiments | 1 campaign test and 1 flow test read; next 3 set | None run | P15, P16 | 02, 03 [659e9f913086] |
| SMS | 5.5 | Good | Bad | P23, P24 | 09, 11 [02f841a00c26] |
| Silent breakage | Pop-up views, cart flow sends, integration events | Steady | Zero after a change | Fix the embed, flow or integration | 03 [5d6743fc3f40] |
| Findings logged | Tracker | 3 findings, 3 tests | Nothing written | Write them | 02 [bd8384e14e34] |

## 6. Thresholds and benchmarks

Confidence: "4 sources" means 4 mini playbooks agree; "1 source" means only 1 states it; "conflict" means sources disagree (see section 7). All numbers are presenter or vendor claims unless marked as a Klaviyo value.

| Metric or setting | Value | Condition | Sources | Confidence |
|---|---|---|---|---|
| Pop-up opt-in rate, typical | 1% to 4% of visitors | untested form | 01, 02, 04, 12 | 4 sources |
| Pop-up opt-in rate, target | 8% to 12% (03: above 9%) | tested form, per device | 01, 02, 03, 04, 12 | 5 sources |
| Phone submit rate, target | about 15% of form viewers | quiz-first form, vendor tool | 09 | 1 source, vendor tie |
| Pop-up delay | 4 to 12 s, start 4 to 6 | not immediate, not 30 s | 01, 02, 04, 11, 12 | 5 sources; 03 conflicts |
| Scroll trigger | 50% to 60% (test 30 to 90) | desktop, OR logic | 02, 04 | 2 sources |
| Re-show after close | 3 to 5 days | Klaviyo default 5 | 01, 02, 03, 04 | 4 sources |
| Minimum signup discount | 10% off | 5% only at very high AOV | 02, 04 | 2 sources |
| $ vs % switch | about $100 to $200 AOV; $ at about 10% of AOV | test | 01, 03, 04 | 3 sources, ranges differ |
| Form test sample | 3,000 to 5,000 impressions per variant or 15 days | manual 50/50 | 02 | 1 source |
| Pop-up test cadence | monthly (03) to weekly (01) | 1 at a time | 01, 02, 03 | conflict on pace |
| Welcome conversion | 10% floor, 20% very good | per entrant | 01, 02 | 2 sources |
| Welcome timing | email 1 at 0; day 0 to 3 carries most revenue; 1-day gaps after | Klaviyo default 3 days too slow | 02, 03, 04 | 3 sources; 01 looser |
| Welcome length | 6 to 8 emails | plus evergreen extras | 01, 02, 03, 04 | 4 sources |
| Welcome email length | under 100 words | 3-second read | 01 | 1 source |
| Site abandonment delay | 1 to 4 h (01: 2 to 4) | 1 email | 01, 02, 04 | 3 sources |
| Browse first delay | 30 min to 2 h | Klaviyo default 2 h | 01, 02, 04 | 3 sources |
| Browse length | 4 to 6 emails | discount at email 3 to 4 | 01, 02, 04 | 3 sources |
| Cart and checkout first delay | 15 min to 1 h; test to 2 to 4 h | Klaviyo default 4 h too long | 01, 02, 03, 04 | 4 sources |
| Cart and checkout length | 6 to 8 emails, about 10 days; minimum 3 | 14 to 20 gets complaints | 01, 02, 03, 04 | 4 sources |
| Flow re-entry block | browse 30 d; cart and checkout 7 to 30 d | by purchase cycle | 01, 02, 03, 04 | 4 sources, values differ |
| First discount in flows | email 4 or 5, 48 h then 24 h | never-bought or 60 to 90 days since order | 01, 02, 04 | 3 sources |
| Returning-customer cart discount | none, or smaller (5% vs 10%) | margins allow | 02 | 1 source |
| Post-purchase first email | 10 to 30 min | after Shopify confirmation | 02, 04 | 2 sources; 01 (0 min) and 03 (1 day) conflict |
| Post-purchase email 2 | +1 to 2 days | on its way | 01, 02, 04 | 3 sources |
| Repeat window | most repeats within 30 days | client screenshots | 02 | 1 source |
| Replenishment reminder | days of supply + delivery, minus a few days (day 25 of 30; day 35 for 30+7) | consumables | 04, 09 | 2 sources |
| Win-back trigger | between median and mean days between orders, or 2x average; 60 to 90 d fallback | own data | 01, 03, 04, 09 | 4 sources, 2 methods |
| Win-back gaps | 3 to 7 days | never 1 day | 01, 03, 04 | 3 sources |
| Sunset trigger | 0 opens and clicks in 120 to 180 days, received 6+ | flow of 3, 5-day gaps | 02, 03, 04 | 3 sources; window conflict |
| Suppress | spam 1; hard bounce 1; soft bounce 4; unengaged 180 d | monthly | 01, 02, 03, 04 | 4 sources |
| Engaged window | 90 d base; 30 to 60 for repair; 365 for Black Friday | opened or clicked or site activity | 01, 02, 03, 04 | 4 sources; base differs 60 to 180 |
| VIP | 4+ orders (01: 5+) or 3 to 4x AOV spend | brand-specific | 01, 02, 04 | 3 sources |
| High potential | site activity 30 d, 0 orders 30 d | +1 to 2 emails a month | 01, 02, 04 | 3 sources |
| Campaign cadence | 3 to 4 a week to engaged | good content | 01, 02, 10 | 3 sources; 03, 04, 06 conflict |
| Cadence floor | 1 a week (03), 2 a week (01) | never skip weeks | 01, 03 | 2 sources |
| Cadence ceiling | 5 to 7 a week burns the list | | 01, 02, 10 | 3 sources |
| Promo share | under one third of sends; max 1 sale event a month; 5:1 to 10:1 non-discount | outside Q4 | 02, 04, 10 | 3 sources |
| Awareness-day emails | 1 to 2 a month | fit only | 02 | 1 source |
| Plain-text sends | 1 to 3 a month; graphic to text 3 or 4 to 1 | | 02, 10 | 2 sources |
| Products per email | 3 to 5; 1 per row or 2x2 | | 02, 04, 08 | 3 sources |
| Email width and text | 600 px; 18 px desktop, 16 px mobile; 1.5 line height | | 01, 04, 07 | 3 sources |
| Subject length | 2 to 5 words (01); under 50 characters (03) | value first | 01, 03 | 2 sources, different measures |
| Attribution window | 5 days open and click; SMS 1 day; exclude Apple opens, bots, transactional | Klaviyo | 03, 04 | 2 sources |
| Smart sending window | 16 h | campaigns only | 02, 03, 04 | 3 sources |
| Resend to non-openers | 1 to 2 days later; Klaviyo built-in minimum 48 h | launches and sales | 01, 03 | 2 sources |
| DNS verification | up to 48 h | new domain | 03 | 1 source |
| Warm-up | engaged only 2 to 4 weeks | new domain | 04 (Klaviyo notice) | 1 source |
| Spam complaint rate | under 0.01% target (02, Klaviyo tab); under 0.1% ideal, 0.3% ceiling (03) | Gmail and Yahoo | 02, 03 | conflict; keep strictest |
| Bounce rate | under 1% | | 03 | 1 source (Klaviyo value) |
| Unsubscribe rate | under 0.3% (Klaviyo); 0.42% normal (06); 0.67% accepted (03) | per send | 02, 03, 06 | 3 sources, tolerance differs |
| Open rate floor (Apple excluded) | under 30% to 35% = placement problem; 45% to 50%+ healthy | engaged sends | 01, 02, 03 | 3 sources |
| Click rate floor | 0.5%; 1.2% Klaviyo "okay"; 2% redesign target | campaigns | 02, 03 | 2 sources |
| Repair ladder | 14 to 30 to 60 to 90 d; 3 sends a week; gate 50% opens x 3 sends or 2 weeks | | 01, 02 | 2 sources |
| Flow test sample | 1,000 per branch (500 if huge gap), about 2 weeks | | 02 | 1 source |
| Send-time tests | 5 to 10 campaigns per pair | judge on orders | 02, 04 | 2 sources |
| Metric noise | under 5% noise; over 10% signal | monthly | 03 | 1 source |
| Email share of store revenue | 30%+ (03); 30% to 50% (10) | attributed | 03, 04, 10 | 3 sources, all attributed |
| Flow share of email revenue | 40% to 60% (01); 40% to 70% (02) | | 01, 02 | 2 sources |
| SMS share of store revenue | 5% to 15% (11); 10% to 20% (09) | done right | 09, 11, 12 | 3 sources |
| SMS campaign frequency | 1 a week (11, 12); 2 a week (09); 8 to 10 a month (05) | | 05, 09, 11, 12 | conflict |
| SMS welcome | 2 to 3 texts in about 5 days | | 09, 11, 12 | 3 sources |
| SMS per abandonment flow | 1 within 48 h | US, Klaviyo enforced | 09, 11 | 2 sources; basis unclear |
| SMS abandonment delay | browse 60 min; cart "a couple of hours" | | 09, 11 | 2 sources |
| SMS post-purchase | day 10 to 14 | after delivery | 09 | 1 source |
| SMS win-back | 60 to 90 d or 2x interval; 72 h offer; +2 d last chance | | 09 | 1 source |
| SMS length | 160 GSM-7; 70 with Unicode | 1 segment | 09, 11, 12 | 3 sources (cards correct emoji math) |
| SMS cost | 1 to 3 cents, about 1.5 | per segment, US | 09 | 1 source |
| MMS cost | 2 to 3x SMS | net-profit test | 09, 12 | 2 sources |
| SMS unsubscribe | 3% to 5% typical (09); under 1% target, under 0.5% excellent (11) | per send | 09, 11 | 2 sources, different bases |
| SMS click rate | 5% to 15% | campaigns | 11 | 1 source |
| SMS delivery | over 90% good, over 95% excellent | | 11 | 1 source |
| SMS send window | 11 AM to 2 or 3 PM; test 4 to 5 PM | | 11, 12 | 2 sources |
| SMS quiet hours (source view) | 8 AM to 9 PM (11); 10 AM to 7:30 PM (12) | law per country overrides | 11, 12 | conflict; `[web check]` |
| SMS holdout | 50 / 25 / 25; 2x beat holdout at 98% | 1 brand | 05 | 1 source, vendor |
| New SMS subscribers buying in 30 days | about 25% | Postscript aggregate | 05 | 1 source, vendor |
| SMS exclusion | 15+ texts, 0 clicks ever | broadcast otherwise | 09 | 1 source; 11 conflicts |
| Conversational text length | under 80 characters | iMessage vendor | 13 | 1 source, vendor |
| Research time | 2 to 4 hours per angle; 10 to 20 min per email after | | 08 | 1 source |

## 7. Where sources disagree

Each conflict: what each side says, when each is right, and what the agent should do.

### 7.1 Single vs double opt-in

- Single: 02 ("massively" cuts subscribers otherwise), 03 (most never click the confirmation), 04 (picks single because engaged segments and a sunset flow handle quality). Aaliyah recommends single for Klaviyo but double for Postscript and Attentive (02). [33c8d10a4bf5] [8c1b383c08cf] [fc0425a31c0f]
- Double: no source in this folder argues for it on quality grounds; the mini playbooks note it is expected or required in some EU markets and by some SMS platforms.
- When each is right: single opt-in fits US-style markets with engaged segments and a sunset flow. Double opt-in fits markets that require it, brands with a spam history, and SMS platforms that expect it.
- Agent: default to single opt-in for email in markets that allow it, only if P11 and P12 are live. Run `[web check: opt-in law per market]` before choosing; use double where required. Keep SMS consent explicit regardless.

### 7.2 Hidden pop-up close (and the success-page code)

- Hide the X: 01 (opacity 0 plus a "No thanks" button), 02 (1 px, transparent), 04 (size 5, background colour, "an ethical debate"). 03 keeps the X and only turns off "click outside to close". [397f14a8dca9] [9622afcc8844] [72945bee8a3a] [4bb4a381c989]
- The sources' reason: break the reflex close and force a decision. The cost: accessibility, user-choice norms and possible interstitial guidance issues.
- Related: withhold the code from the success page (02, 03, 04) vs show it (01). 02 calls it a 50/50 debate with a small conversion loss recovered in 72 hours.
- Agent: ecomOS R189 wins. Keep a visible X and a "No thanks" button; the owner may test a smaller or left-placed X, never a hidden one. For the code, default to sending it by email (3 sources) unless the owner prefers instant reveal; log the welcome email 1 open rate either way.

### 7.3 Pop-up trigger: immediate vs delayed

- Immediate: 03 shows the form on load and only tests a 5-second delay or 30% scroll as variants. [4d0639885e1a]
- Delayed: 01, 02, 04, 11, 12 use 4 to 12 seconds and call page-load display a "conversion killer" (04); 01 and 12 reject exit intent and scroll as misfiring; 02 and 04 add scroll and desktop exit intent. [e5cbaa0f3a12] [c5e1f30dd58d] [d124c18b882e] [3545eb404e90]
- When each is right: immediate can win on total submits when traffic bounces fast (01's own rule: judge delay by total submits, not rate). Delayed wins on experience and on site conversion.
- Agent: start at 4 to 6 seconds, test 4 vs 12, then immediate vs 4, and judge on total submits and site conversion rate (05), not opt-in rate. Mobile exit intent stays off.

### 7.4 Smart sending in flows: on or off

- Off in every flow: 02, 04 (flows carry high-intent revenue; a campaign in the last 16 hours must not block a cart email). On for campaigns. [4d6f11a9f443] [b837f7435caf]
- On at account level: 03 keeps the 16-hour default and only turns it off per campaign for launches; 03 also warns that a campaign plus 3 flow emails in 24 hours drives unsubscribes and complaints. [1ce671434e00] [24b8079fe1fe]
- When each is right: off is right for cart, checkout, browse and welcome email 1 (time-critical). On is safer for later post-purchase, win-back and sunset emails where an hour does not matter.
- Agent: off on welcome, browse, cart, checkout and post-purchase email 1; on for late post-purchase, win-back and sunset emails; on for campaigns; watch unsubscribes per person-week in the monthly review.

### 7.5 Whole list vs engaged segments (see also 7.10)

- Engaged only: 01, 02, 03, 04, 10. 03: "never send to the whole list, rarely to a list". [bb790bf6e145] [d7c5cedcb3dd]
- Broad beats narrow within engaged: 01 (3 to 4 campaigns to 50,000 beat 1 to 2 targeted to 10,000), 03 (do not micro-split under $20M a year), 10 (don't go crazy on segmentation). [24e40adf1b4f] [0ca859db0b00] [c28459447833]
- Agent: send to the engaged segment, not the list; do not split it into small audiences; personalise inside the email with dynamic blocks; use prospect vs customer splits for learning, not for halving reach.

### 7.6 DMARC: none vs quarantine vs reject

- p=none always: 03. His reason (reject sends spam-judged mail to spam) is wrong; DMARC acts on SPF and DKIM alignment failures, not on content. [a192f5312b82]
- Start at none, own record at quarantine pct=90: 04, who never says when to move up. [fc0425a31c0f]
- 02: add the `_dmarc` record; value not transcribed. [e758ab334635]
- When each is right: none is right on day 1 and while reports show unaligned legitimate sources. Quarantine and then reject are right once all legitimate mail aligns, and they protect the domain from spoofing.
- Agent: P2 step 6: none with reports, then quarantine (pct ramp), then reject. `[web check: current Gmail and Yahoo DMARC requirements]`

### 7.7 Spam limit: 0.3% vs 0.1% vs 0.01%

- 03: below 0.3% (Gmail and Yahoo), ideally below 0.1%; Klaviyo's tab shows "under 0.01%" as its recommendation and a client at 0.004%. 02: 0.01% or lower (spoken as "001%"). [6d8587217a67] [3dca25bfe545] [91d6fd433f58]
- These are different things: 0.3% is the provider ceiling above which mail is throttled; 0.1% is the safe zone; 0.01% is a healthy account's actual rate.
- Agent: treat 0.01% as the working target, 0.1% as the warning, 0.3% as the hard ceiling that triggers P17. `[web check: current Google Postmaster limits]`

### 7.8 SMS frequency: 1 to 2 a week vs 8 to 10 a month vs holdout results

- 1 a week, 2 rarely: 11 (more than 2 "overkill"), 12 (unsubscribes rise with volume). [6f21ea67f481] [bf9cd4297ad9]
- About 2 a week, daily for aggressive acquisition, 1 to 2 a day in sale pushes: 09. [ec74b2c055f2]
- 8 to 10 per subscriber per month with no unsub impact; step up until unsubscribes tick up; holdout where 2 a week beat 1 a week at 98% certainty: 05 (Postscript, paid per send). [52f701ac2a63] [bb28c48148d6] [651884bb18e3]
- Launches, restocks and sales only: 02. [b9130f4f4dca]
- When each is right: low cadence fits long purchase cycles and small lists (11: furniture every 18 months); higher cadence fits big-news brands with large lists and a holdout that proves it. Vendor advice is biased upward.
- Agent: start at 1 a week of real news; step up only through P24 (holdout plus unsubscribe watch); never text active subscribers; keep quiet hours and consent per country.

### 7.9 Sunset rule wording

- 03: 0 opens AND 0 clicks in 180 days; flow filters spoken as OR (bug). [56d433c32a2b]
- 04: 0 opens, clicks, orders, checkouts, carts, views and site visits in 120 days AND received at least 6 emails; 365-day email-only version with received at least 12. [171bd57ff251] [c57d2fe2264a]
- 02: unengaged 120 days as the sunset trigger, 180 as suppression, and past buyers kept on purpose. [336b88ac711f]
- 01: suppress no open 180 days, any bounce, any spam mark; 90 to 120 days as "unengaged" for a monthly nudge. [c049ecf47935] [fbb4bfea66bf]
- SMS analogue: 09 excludes 15+ texts with 0 clicks; 11 tightens when unsubscribes exceed 1%. [74853693497f] [02f841a00c26]
- Agent: use 04's wording with a 120-day window as the trigger (all events zero, received at least 6), AND in the flow filters, 180 days for suppression. Decide past-buyer handling per brand: keep buyers of slow-cycle products (02), sunset them for fast consumables. `[needs brand data: purchase cycle]`

### 7.10 Whole-list re-engagement sends

- 1 a month to the wider list after recovery so openers rejoin the engaged segment: 01. 1 to 2 a month to "all but unsubscribed and suppressed": 02. Never: 03. [e385d9458d21] [951b0132a90b] [d7c5cedcb3dd]
- When each is right: a monthly wider send is defensible once the list is clean and the sender is healthy; it is harmful during repair or with a dirty list.
- Agent: only after P17 is complete and spam is under 0.1%; at most 1 a month; exclude spam, bounces and 180-day unengaged; stop if spam or bounce rises.

### 7.11 Campaign cadence: fixed 3 to 4 vs data-driven

- 3 to 4 a week: 01 (tested 2 a day to 2 a month), 02 (120 brands), 10 (200 brands). [d435b73cfe27] [7a1145af87dc] [1dbc06e4564f]
- At least 1 a week and step up while CTR, unsubscribes and spam stay flat; commit to what you can sustain: 03. Tiers by revenue with an open-rate gate: 04. Quality threshold over any cadence; start monthly if you never mailed: 06. [dbd9ab70c7db] [a6116076fc6e] [c53d577bf872]
- When each is right: 3 to 4 fits brands with content capacity and an engaged list; the data-driven path fits small teams, small lists and long cycles.
- Agent: set the cadence the team can hold every week (never 0), start at 2 to 3, step up by 1 while unsubscribes, spam and revenue per send hold, cap at 4 unless segments keep each person near 3.

### 7.12 Text-only vs designed emails (and image-only)

- Text wins: 01's tests (founder text beat graphic on clicks and orders; plain 1.7% vs 1.2% placed order), 10 ("all of my best performing emails"), 06 (no images at all). [125460461476] [0adcc430d16d] [65281424ea63] [84e6a958f0b2]
- Designed carries the load: 10 (3 or 4 graphic to 1 text), 03 and 07 (Figma slices; 07 says image-only is fine in 2026), 01 (sliced designs). [92e649c06ecd] [cfa416cb8d27]
- Live text for Gmail's AI: 02 (alt text, native product blocks, live top bar and footer), 04 (rebuild short text as live text). [31b2f58bfc95] [8f1c460f5eed]
- Agent: designed emails for education and product sends with the offer, product names and footer as live text; 1 to 3 plain-text founder emails a month; test text vs designed per flow (P16) and per pillar (P15). Never image-only.

### 7.13 Open rate vs CTR vs revenue per recipient (and subject lines)

- Opens as the gate: 01 (40% to 50%), 02 (45% to 50%), 04 (30% for cadence). None of the 3 mention Apple Mail Privacy Protection. [61807f09ea38] [91d6fd433f58] [a6116076fc6e]
- Clicks and orders: 03 (clicks are the placement signal since iOS 15; placed order rate decides tests; RPR in the chain), 06 (CTR main metric), 11 and 12 (SMS: clicks, unsubscribes, delivery). [3dca25bfe545] [c5f48c89de68] [02f841a00c26]
- Revenue vs holdout: 05. [651884bb18e3]
- Subject lines: 01 and 10 say opens come from sender name and cadence and subject tests should be judged on orders; 03 and 04 skip campaign subject tests; 06 tests subject lines every send. [c4cf02ddd233] [32c744be62a5] [db47183f351f] [4516dab6a1af]
- Agent: revenue per recipient and placed order rate decide; unique clicks second; opens (Apple excluded) only as a deliverability gate; test subject lines only in flows or with spare capacity, judged on orders.

### 7.14 Abandoned cart trigger: Added to Cart vs Checkout Started

- All 4 Klaviyo courses (01, 02, 03, 04) agree: build both, and the template called "abandoned cart" is a checkout flow. [d962429e9e36] [d94eb68e5e18] [85117c7d0910] [fac642b0957b]
- Disagreement is on the metric source: 01 says install the snippet (and elsewhere that Klaviyo added it natively in September 2024); 02 says use the Shopify metric, not the API one; 04's header (not the speaker) says a snippet is needed.
- Agent: check the Metrics tab for a live Shopify Added to Cart metric; install the snippet only if it is absent; `[web check: current integration behaviour]`.

### 7.15 Email and SMS together vs SMS first

- Together or very close: 03 (checkout section). SMS first, wait 2 hours, then email if no order: 03 (multichannel section). Email at 9 AM then SMS 5 to 6 hours later: 11. SMS only to non-clickers where SMS RPR is strong: 02. 09: no rule. [fbfeb91636ec] [4c7296971696] [a9df8fb1a06e] [af644216425f]
- When each is right: together maximises speed for checkout abandonment; SMS-then-email or email-then-SMS lowers pressure and cost; SMS-to-non-clickers saves money on big lists.
- Agent: for cart and checkout, email at 30 minutes and 1 SMS at 1 to 2 hours if no order (1 SMS per flow, R162); for campaigns, email first then SMS 5 to 6 hours later for launches and sales only; test the alternative with P16 and read net profit.

### 7.16 Separate mobile and desktop forms

- Separate: 01, 02, 04. One form unless they convert differently: 03. [c2e8c7484a70] [f932973235fb] [4bb4a381c989]
- Agent: separate forms (3 sources); the mobile form has no image and no exit intent.

### 7.17 Teaser on or off

- On: 02, 03, 04 (02 says it raises signups). Off: 01 (gets in the way). [53f37df1584e] [f7f5d18ebe32]
- Agent: on, small shape on mobile; test off if opt-ins do not move.

### 7.18 Post-purchase first email timing

- 0 minutes: 01. 10 minutes: 02. 30 minutes: 04. 1 day, no fixed hour: 03. [05c3a4b18253] [58bdfe185e63] [d4ea5342470c] [55898f20e161]
- Agent: 10 to 30 minutes so it lands after the Shopify confirmation; test 30 minutes vs 4 hours in P16.

### 7.19 Browse abandonment split by buyer status

- No split unless margins are very tight: 02. Branch prospects vs customers: 03. [5ad3da1bdb3a] [f147a186a98d]
- Agent: no split by default; add it when the discount cannot go to past buyers.

### 7.20 Extra SMS offer for the phone number

- No extra offer, "activate" framing: 09, 11. Bigger SMS offer or VIP club as test angles: 04; 10% email and 20% SMS: 02. [75893d2892aa] [9b9305f19394] [1bad712bca98] [8bb0c8c613c5]
- Agent: full offer on the email step, "activate" on the phone step; test a VIP angle only if phone submits stay under 10%.

### 7.21 Guarantee window

- 08: a 180-day guarantee returns less than a 30-day one because buyers forget (claim, no data). No other source addresses it. [e447e1b8be41]
- Agent: use the brand's real guarantee; test window length only with refund data. `[needs brand data: refund rate by window]`

## 8. Common mistakes

Merged from all 13 sources, deduplicated, with the fix.

Pop-ups and consent
1. Weak offer ("sign up and be my friend", 5% off on a $500 AOV). Fix: R7, R9. [7ea9228eeda8] [9adb06995af6]
2. Email and phone (or name, birthday) on 1 step. Fix: R11. [39aa68c94680]
3. Immediate display, 30-second delay, or mobile exit intent. Fix: R14, R15. [d124c18b882e] [3545eb404e90]
4. Small form, long copy, "sign up" wording, offer buried under a greeting. Fix: R18. [ff4c8404916f]
5. 1 form for both devices, or a slow image on mobile. Fix: R17, R22. [f932973235fb]
6. Showing the form at checkout or to existing profiles. Fix: R19. [a877dc6c99dd]
7. Letting Klaviyo pick a form winner on low volume; testing design before offer. Fix: R23, P4. [00de729163a8]
8. Judging a pop-up on opt-in rate while site conversion drops. Fix: R10. [1282cefafb08]
9. Hidden X, pre-checked consent, shrunken consent text, decoy prizes, hard unsubscribe. Fix: R187 to R190, R30. [397f14a8dca9] [c1faaf881fc4]
10. Accepting Klaviyo's 3% "excellent" badge. Fix: R8. [ea0cb89619eb]

Flows
11. An "abandoned cart" flow that fires on Checkout Started and no Added to Cart flow. Fix: P8. [d962429e9e36] [85117c7d0910]
12. Copying checkout variables into the cart flow; browse emails linking to the homepage. Fix: R62, P7 step 4. [c42f60fa5fca] [79cdac8bb86e]
13. 1 or 2 recovery emails; a 1-email welcome; 2 to 3 dense welcome emails; a welcome that never repeats the code. Fix: R44, R45, R59. [ed0f5c1eb0f6] [b0ac0c5d9d9b]
14. Klaviyo default delays (welcome 3 days, cart 4 hours, post-purchase 1 day at 9 AM). Fix: R35, R43, R66. [d94eb68e5e18] [55898f20e161]
15. Discounts in email 1 or 2; discounts to past buyers; discounts without a deadline; fake deadlines on static codes. Fix: R36, R37. [bdbde349add0] [a69de45ff438]
16. No exit filters, so people get 2 flows at once. Fix: R31, R32. [9da5ac313720]
17. Smart sending on in flows; UTM off. Fix: R33, R34. [b837f7435caf]
18. Generic "great product" reviews; generic how-to emails; brand poetry in email 2. Fix: R47, R70. [38077a826b12] [5956a124a134]
19. Heavy urgency graphics in the last browse email; "brand is awesome" instead of objections in cart email 3. Fix: R53, R60. [8c9c22844f69]
20. Win-back on the template's 75 or 90 days with 1-day gaps; sunset filters joined with OR. Fix: R74, R75, R80. [021057848a4f] [56d433c32a2b]
21. Treating the first purchase as the finish line; skipping the proactive service check-in. Fix: R67 to R69. [b3058403e9f8] [55898f20e161]
22. Using template content as-is; set-and-forget flows "not updated since masks". Fix: R39, P25. [fd7d4c80cdb7] [b568ff652c08]
23. Skipping site abandonment because there is no template. Fix: P6. [b0f7b82a2bb3]

Segments and deliverability
24. Campaigns to the whole list or to a list; unengaged 2-year-olds still mailed; being proud of a big dead list. Fix: R86, R92, R93. [bb790bf6e145] [6dcb0bfce104]
25. Splitting campaigns into tiny segments and halving shots on goal. Fix: R91. [0ca859db0b00]
26. OR on "can receive email marketing"; mixed AND/OR. Fix: R87. [516248e6ac94]
27. No branded domain; no DMARC; DMARC stuck at none forever or reject with unaligned sources. Fix: P2. [a192f5312b82]
28. Judging deliverability by open rate; ignoring Apple opens; ignoring flow deliverability. Fix: R142, R179. [3dca25bfe545]
29. Weeks of silence then a Black Friday blast; a cadence you cannot keep. Fix: R101, 7.11. [dbd9ab70c7db]
30. Image-only emails; invisible footer text; marketing-sounding subject lines that land in Promotions. Fix: R130, R188, R118. [31b2f58bfc95] [bc0f81f5c30a]
31. Emailing people who marked spam or bounced. Fix: R92. [951b0132a90b]

Campaigns, copy and design
32. Discount after discount; more than 1 sale a month; a "national day" every week. Fix: R102. [46a5333c2392] [6a19f9f385b5]
33. 1 or 2 random sends a week; 5 to 7 a week; right cadence with generic content. Fix: R100, R105. [1dbc06e4564f]
34. Batching 1 type into 1 week; writing the day before (defaults to promos). Fix: R103, R107. [7a4e669c2511] [3e4696a51c71]
35. Several takeaways, text walls, fluff, corporate lines, features not outcomes, 10 messages in 1 email. Fix: R111 to R113. [99679e755f67] [945e9b8a355c]
36. First button far down; small buttons; nav rows at the top; 6 competing CTAs; product tiles that do not look clickable; no button at all. Fix: R123 to R125. [ca47b8d3f740] [26cdbc32e54d]
37. Same template every send; studio photos unlike the brand's Instagram; blurry or mismatched images. Fix: R128. [a744284f4af9]
38. Missing alt text; homepage links; uncompressed multi-MB slices; 1 giant image; HTML editor emails that break. Fix: R129, P18. [17b5705e3605] [8f1c460f5eed]
39. Shipping AI copy as-is; AI drafts with no CTA or invented claims. Fix: R121, R191. [8051e7b15977] [8e823019286f]
40. Judging subject lines on opens; testing button colours at small scale; calling winners at 50 recipients; automatic 20/20/60 winners; assuming winners transfer. Fix: R173 to R177. [c4cf02ddd233] [ac370b420628]
41. Killing high-engagement, low-revenue newsletters instead of adding merchandising. Fix: P25 step 3. [3c10a64f1966]
42. Implying regulated claims; blaming the customer; a face next to a sensitive review; 3x2 product grids. Fix: R115 to R117, R126. [b5dbf59a5f38] [6e5742c076f2]
43. Fake "as seen on" logos, resetting countdown timers, fake restocks and "running low". Fix: R186, R191. [f0580c1b1e80] [8ae593fcc226]

SMS
44. Sending SMS as often as email; nurture and testimonials by text; texting active subscribers. Fix: R152, R157. [bf9cd4297ad9] [ec74b2c055f2]
45. Texting anyone without explicit SMS consent; sending in quiet hours; removing STOP handling. Fix: R153, R154. [ccceb9ed6344]
46. 161 characters or an emoji that doubles cost; MMS by habit. Fix: R158, R159. [0228dbaf571e] [13f23c2e8c94]
47. "Continue" on the email step; "sign up for texts" copy; a bigger discount for the phone. Fix: P21. [75893d2892aa]
48. More than 1 SMS per abandonment flow; a welcome spread over weeks. Fix: R161, R162. [ee1a31c09fcc]
49. A large SMS bill with no holdout; setting cadence by fear or by vendor advice. Fix: R167, 7.8. [9a17b76595cd]
50. Choosing a platform on AI feature pitches; skipping the checkout opt-in checkbox (with proper consent). Fix: R171, R24. [aa2a2140c1a0]
51. Deliberate typos, fake personas, "forget about email", iMessage without opt-out. Fix: R193, R153. [324169289900]
52. Changing RCS format and creative at once. Fix: R170. [80442f6087a2]

## 9. Deliverables

What the lifecycle agent produces for each task, and the format. Every deliverable names its inputs, marks anything computed from brand data, and lists open `[needs brand data]` and `[web check]` items at the end.

### 9.1 Flow map with gaps

Format: 1 table, 1 row per flow (welcome, site, browse, cart, checkout, post-purchase, replenishment, win-back, sunset, back in stock, review, birthday, and each SMS flow). Columns: exists (yes/no), trigger as found, entry and exit filters as found, first delay, number of messages, discount position, smart sending state, UTM state, last 30-day revenue and revenue per recipient (computed), gap vs this playbook (rule number), priority (revenue weight: welcome, cart, checkout, browse, post-purchase first), fix reference (P number). Ends with the 5.1 checklist result and the 3 biggest gaps in plain sentences.

### 9.2 Flow build specs

Format: 1 spec per flow, ready for a builder. Sections: goal; trigger; filters (exact Klaviyo wording, "since starting this flow" vs "over all time"); re-entry; delay chain; splits (condition and branches); per message: name, channel, delay, subject, preview, sender, smart sending, UTM, content outline (blocks in order, dynamic blocks and their variables, links, code and its expiry rule), claims used and their brand-record source; QA steps (preview profiles, test entries, exit test); rollback. SMS messages carry the segment count and the consent and quiet-hour rule applied.

### 9.3 Email drafts

Format: per email, a Google Doc style table with 1 row per section (logo, headline, sub-headline, body, CTA, hero, bridge, products, closing CTA, footer), the copy in each row, the subject line (2 to 3 options) and preview text, the pillar and micro-topic, the format (designed or plain text), the reviews or proof used with their source, the claims checked against the brand record, alt text for each planned image, and the test send checklist (5.4) marked done. Under 300 words for a campaign, under 100 for a welcome email. Plain-text founder emails carry the founder's name and the reply promise the brand can keep.

### 9.4 Segment definitions

Format: 1 table, 1 row per segment: name, purpose, exact conditions with AND/OR groups as Klaviyo lists them, window, expected size (preview count) and share of the list, which sends use it (audience or exclusion), refresh or suppression schedule. Covers engaged tiers (14, 30, 60, 90, 120, 180, 365), prospects and customers, exclusions (spam, bounced, unengaged), unengaged and sunset triggers, VIP, high potential, win-back potential, buyer stages, abandoners, window shoppers, interest and cross-sell, location, and the SMS audience and exclusion.

### 9.5 Campaign calendar

Format: a month grid plus a table: date, send day slot, channel (email, SMS, both with the gap), pillar, micro-topic and angle (2 lines), format (designed or text), segment, offer (if any, with real expiry), fixed date it supports, status, owner, result fields (recipients, unique clicks, placed orders, revenue, RPR, unsubscribes). Ends with the mix check: counts per pillar, promo share, consecutive-type check, graphic to text ratio, sends per week, SMS per week, any week without a send.

### 9.6 Test plan

Format: a ranked list, 1 row per test: hypothesis (1 sentence), where (flow and email, or campaign), variable, control and variant, audience and split, sample floor and expected duration, winning metric (placed order rate or RPR), guard metrics (unsubscribes, spam), what happens on a win, owner, status. Order follows R176. Includes the SMS holdout (P24) when SMS spend exceeds the threshold.

### 9.7 Audit report (when asked for an audit)

Format: the 6 checklists of section 5 with every row filled, then the metric chain for the last 2 months, the deliverability numbers against section 6, and a 10-item fix list in revenue order with P references.

## 10. What needs live data or a web check

### 10.1 `[needs brand data]`

Brand record:
- AOV and gross margin (R9, R61, R159, P3)
- Discount policy: who may get a code, depth, frequency; margin room for flow incentives (R36, R61, R102, P8, P22)
- Ship-to countries and legal markets (R19, R26, R28, R154, R192)
- Founder name, photo, voice; support reply capacity and hours (R38, R169, P5, P9)
- Approved claims, guarantees, shipping times, returns policy; substantiation for every us-vs-them point (R117, R191, P18)
- Reviews and testimonials tagged by objection; reviewer photo consent (R47, R115, P5)
- Brand voice limits on fear or insecurity angles (R116)
- Owner's position on hidden close, code on success page, cadence ceiling (7.2, 7.11)
- Subscription, loyalty and reviews apps in use; B2B or wholesale customers (P9, P10, R71, R85)
- Content library and existing tracker (P14)
- Existing SMS list and consent records; SMS platform and per-segment rates; iPhone share of the list (P20, R158, R170)

Data layer (Klaviyo, Shopify, Metabase, GA4):
- Current opt-in rate by device; form views and submits; phone submit rate (R8, R10, P4, P21)
- Site conversion rate before and after pop-up changes, by device (R10, 7.3)
- Welcome flow placed order rate and revenue per offer (R10, R46)
- Flow and campaign revenue; flow share of email revenue; email share of store revenue and the attribution window (R3, R4)
- Opens with Apple opens excluded, unique clicks, click rate, placed order rate, RPR, unsubscribes, spam, bounces by campaign and flow; historical click rates on engaged segments (R139 to R144, P25)
- Send-time history; clicks and revenue by send hour (P15, R155)
- Median and mean days between orders; days of supply per product; delivery times by region (R72, R74, P9, P10)
- Order-count and spend distribution (R94)
- Bestsellers by first-order share; product collections (R44, P12)
- List size, engaged share, inbox provider mix, traffic by source and country (R89, R148, P17)
- Repeat purchase interval and subscription status per customer (R57, R157)
- Baseline unsubscribe rate and revenue per send at the current cadence; SMS unsubscribes in each subscriber's first 30 days (R100, R156, P24)
- SMS attributed revenue, cost per send, revenue per message, net profit per send; share of new SMS subscribers buying within 30 days (R166, R167, P23)
- Refund rate by guarantee window (7.21)
- Klaviyo campaign and flow exports for P27

### 10.2 `[web check]`

Consent and law:
- Email consent and double opt-in rules per market (GDPR, PECR, CASL, India DPDP) (R26, R29, 7.1)
- Pre-checked consent and checkout checkbox validity per market (R187, R24)
- SMS consent wording, separate checkbox, disclosure text, opt-out keywords, sender registration (TCPA, CTIA, state mini-TCPA, TRAI DLT in India, PECR) (R28, R153, P20)
- Legal quiet hours per country and US state, recipient local time; India promotional window (R154, P20)
- Whether the 1-abandonment-text-per-48-hours limit is law, carrier guidance or Klaviyo policy (R162)
- Business iMessage consent, opt-out and Apple policy; A2P 10DLC applicability (R170)
- Consumer protection rules on false scarcity, decoy prizes and implied health claims (R186, R190, R117)
- Data protection rules for storing health or family details from SMS replies (R169)
- Accessibility rules and Google's intrusive interstitial guidance for pop-ups (R189)

Platforms and providers:
- Gmail and Yahoo bulk sender requirements: SPF, DKIM, DMARC minimums, one-click unsubscribe, spam-rate limits (R30, R137 to R139, P2)
- Current DMARC policy guidance (7.6)
- Gmail AI inbox behaviour with marketing mail; Gmail clipping threshold; image blocking (R130, R133, P18)
- Apple Mail Privacy Protection share of opens and Klaviyo's handling (R142)
- Klaviyo current UI: form builder, flow templates and triggers, Shopify Added to Cart metric vs snippet, default delays, attribution defaults, sending domain record types, billing basis, unsuppress rules, segment library, SMS quiet-hour defaults and credit cost per country (every P; R56, R82, R179)
- Aaliyah, Alia, Amped, GlockApps, countdownmail, BIMI pricing and features (P3 step 12, P17, R150)
- SMS and MMS rates per country on the brand's platform; Attentive and Postscript pricing (R158, R171)
- RCS business messaging availability, fees, verification and calendar-action support outside the US (R170)
- Postscript API or MCP access for conversation data (R169)
- WhatsApp business messaging cost in the brand's markets (02 note)

Claims and statistics cited by the sources (do not reuse without a source): 70% to 85% cart abandonment, 26% buy from a competitor, 27% more likely to rebuy in 3 hours, $36 or $44 per $1 email ROI, 9x retention, 67% repeat spend, 98% SMS open rate, 3-minute SMS open time, 791% segmentation lift, 170 ads a day, 1,000 brands a week, 2x iMessage reply lift.

## 11. Freshness and stale-risk notes

| Area | What can change | Re-verify |
|---|---|---|
| Klaviyo UI and defaults | Menu paths, form builder options, flow templates and their triggers, Added to Cart metric behaviour, default delays, attribution defaults, sending domain record types (NS, CNAME), campaign sequence builder limits, billing basis, A/B test options, segment library. Sources were recorded 2024 to spring 2026 and already disagree with each other on defaults. | Before every build; every quarter for the checklists |
| Apple Mail Privacy Protection | Share of opens that are machine opens; Klaviyo's exclusion toggles; whether engaged segments can filter Apple opens. Open-rate gates in 01, 02 and 04 predate or ignore it. | Quarterly; before any open-rate gate is used |
| Gmail and Yahoo sender rules | Spam-rate thresholds, DMARC minimums, one-click unsubscribe, bulk-sender definitions, Gmail AI inbox treatment of promotions. 02 and 03 describe 2024 to 2026 states; 01 and 04 predate or skip them. | Quarterly; before P2 and P17 |
| DMARC policy guidance | Provider minimums and recommended escalation. 03's "never quarantine or reject" is already wrong. | With the sender rules |
| SMS law and carrier rules | TCPA and state rules, CTIA guidance, quiet hours, abandonment-message limits, DLT rules in India, PECR in the UK. All SMS sources are US-only and cite no law. | Before any SMS send in a new country; every 6 months |
| SMS and MMS pricing, Klaviyo credits per country | Rate cards move; Canada was 2 credits in early 2025 (11). | Before cost math in P23 |
| RCS | US availability, carrier fees, brand verification, iOS calendar action, novelty lift decay, availability outside the US. 05 is a spring 2026 vendor snapshot. | Before any RCS pilot; every 6 months |
| iMessage business messaging | Apple policy, account limits, opt-out rules. 13 is a vendor pitch. | Before any test |
| Pop-up tools | Aaliyah, Alia, Amped features and pricing; smart triggering; gamified steps. Presenters have affiliate ties. | Before choosing a tool |
| Deliverability tools | GlockApps features and price; BIMI cost (about $1,500 a year in 02). | Before P17 |
| AI tools | Custom GPT menus (10), model names, export analysis prompts. | Before P27 |
| Benchmarks | Every number in section 6 is a presenter or vendor claim from 2024 to 2026 client accounts. Replace with the brand's own data as soon as 2 months of clean exports exist. | Monthly |
| Market statistics | The uncited figures listed in 10.2. | Never reuse without a current source |

## 12. Source index

| No. | Title | Type | Credibility and bias | Contributed most |
|---|---|---|---|---|
| 01 | Ecommerce Email Marketing 2025 (Well Copy, "Max") | 16 joined YouTube transcripts, 188 cards | Email agency founder; sells services, templates, a newsletter; promotes Amped. Evidence: single-brand client A/B screenshots, no confidence levels, inconsistent revenue claims ($15M to $50M). Never mentions Apple privacy or authentication. Teaches an invisible-text trick. Medium credibility on flow structure and segments; low on deliverability and stats. | 7 core flows with email-by-email content, exact segment definitions, 29 campaign frameworks, popup checklist, 6-week repair ladder, weekly test roster with results |
| 02 | Klaviyo email (full course, 2026, "Magically" agency) | 1 long course, 99 cards | Agency owner; sells builds; affiliate for Aaliyah. Evidence: "120 brands, 7 years", client screenshots, 2 ChatGPT analyses; no sample sizes; transcript-damaged numbers (click 5% vs 0.5%). Medium credibility on flow ladders and campaign mix; vendor bias on pop-up tool. | 72-hour welcome front-load, browse and cart ladders with buyer-status split, 91 campaign types and the monthly mix, 4-step deliverability fix, list-cleaning segments, Gmail AI live-text rules, KPI targets |
| 03 | 2026 Klaviyo Email Marketing Full Course (Dispatch, "Elliot") | 1 course, mid 2025, 82 cards | Agency owner; sells Klaviyo and Figma services. Evidence: agency accounts on screen, 1 client business review; no tests shown; revenue Klaviyo-attributed. Wrong on DMARC "never quarantine". Medium to high on account settings, attribution hygiene and the monthly review; low on evidence. | Attribution exclusions (MPP, bots, transactional), engaged 180 with 14-day carve-outs, prospects vs customers, sunset flow build, predictive win-back, checkout_url link, monthly analytics routine, metric chain |
| 04 | Klaviyo Email Marketing Full Course 2025 (unnamed agency) | 1 course, recorded 2024, 82 cards | Agency owner; money-back pitch at the end. Evidence: client dashboards, demo account without Shopify; own defaults. Header adds claims the speaker never made. Medium on flow structure and popup settings; low on deliverability numbers. | 8 flows with tables, unengaged segments with "received at least 6", frequency tiers by revenue, 5:1 to 10:1 discount ratio, flow timing test method, buyer-stage segments, Figma to Klaviyo build with live text |
| 05 | Rethinking SMS Marketing: AI, RCS and LTV (Postscript podcast) | Podcast transcript, spring 2026, 19 cards | Postscript CCO (vendor paid per send) with 2 operator hosts. Evidence: cross-brand aggregates, 1 vendor-run holdout, anecdotes; 5 sponsor reads. High bias toward more sends and RCS; US only; no compliance. | Holdout test design, step-up cadence heuristic, SMS as acquisition, conversational SMS, RCS definition and pilot method, pop-up tests on site CVR |
| 06 | Learn Email Marketing in 39 Minutes (Hormozi) | Talk transcript, 19 cards | B2B info-product newsletter, not ecommerce; sells workshops and a community. Evidence: own 3-month newsletter stats, uncited third-party figures. Low fit for store flows; useful on plain text, CTR and easy unsubscribe. | CTR over open rate after Apple, plain-text formatting, easy unsubscribe, hand-written preview text, quality over cadence, send day and hour starting points |
| 07 | How to Design High Converting Ecommerce Emails in Figma (Well Copy) | Talk, 2026, 15 cards | Same agency as 01 and 09; Omnisend affiliate. Evidence: opinion and screenshots, no results. Says image-only is fine; header carries the hidden-text hack. Medium on layout mechanics; low on proof. | Copy, structure, design layers; button at top and end of each section; bridge infographics; seamless gradients; slicing, compression and ESP upload steps; us-vs-them block |
| 08 | Master Email Copywriting for E-commerce Brands (unnamed agency) | Course module, 16 cards | Agency owner; lead magnets; invented numbers in every example. Advises implying regulated claims (rejected here). Medium on the research routine and block method; low on evidence. | Research routine (Ad Library, Amazon Most Recent, podcasts, followers), perks vs insecurity anchors, honest blame shift, block-by-block copy, review per objection, 2x2 not 3x2, guarantee block |
| 09 | How to Create a SMS Marketing Strategy for $10M Shopify Brands (Well Copy) | Talk, 2026, 15 cards | Same agency as 01; sells services and a swipe file; uses Alia. Evidence: client dashboards, 2 small MMS tests; sends fake restocks (rejected here). Medium on cost logic and flow skeleton; US only. | Platform price-shopping, phone-capture copy, 160-character and MMS cost math, welcome day 1/3/5, 4 abandonment flows with 1 text, post-purchase and replenishment timing, win-back at 2x interval, broadcast-with-exclusion audience |
| 10 | Complete Ecommerce Email Marketing Strategy for 2026 (Well Copy) | Talk, late 2025, 12 cards | Same agency; Omnisend sponsor; custom GPT lead magnet. Evidence: taste and claims ("200 brands"), no numbers; internal arithmetic inconsistent. Campaigns only. Low to medium. | 4 non-discount pillars, micro-topics, graphic to text ratio, winning layout, 9 infographic types, sender name over subject line, light segmentation for broadcasts |
| 11 | The Only Ecommerce SMS Marketing Video You'll Ever Need (unnamed agency) | Talk, Feb 2025, 11 cards | Agency owner; swipe file lead magnet. Evidence: claims and 1 blurred screenshot; compliance statements without a named law. Medium on Klaviyo SMS setup and KPIs; US only. | Klaviyo SMS setup steps, 2-step "activate" pop-up, 1 to 2 a week cap, quiet hours and send window, email then SMS 5 to 6 hours, 1 SMS per flow claim, KPI targets, daily/weekly/monthly review |
| 12 | Everything You Need to Know About SMS Marketing in 2025 (unnamed) | Talk, 2025, 14 cards | SMS consultant; lead magnets; "tens of millions of texts". Evidence: 1 client's 30 days; own tests without numbers; recommends restock texts for non-restocked items (rejected). Medium on cost and calendar; US only. | 1 a week default, nurture-off-SMS rule, segment and encoding math (cards), checkout opt-in checkbox, launch and flash-sale message pattern, gap-filling, send windows |
| 13 | If I Started SMS Marketing in 2026, I'd Do This (SendBlue) | Talk, 6 cards | iMessage vendor pitch; lead-gen framing; unsafe compliance claims (drop STOP); recommends fake typos. Evidence: vendor "2x reply" with no method. Low credibility; not ecommerce-native; not for Android markets. | Conversational test ideas only: question-led first text, human handoff, short messages; the rest is rejected or flagged |

Cluster note: 01, 07, 09 and 10 are the same agency (Well Copy). Their agreement counts as 1 to 2 voices, not 4. 02, 03, 04, 08, 11 and 12 are 6 further agencies or consultants. 05 and 13 are vendors. 06 is a B2B newsletter talk.

Neighbour folders:
- Paid acquisition and Meta: the Meta and ad-deployment folders (24-DEP, 06-MEA in older numbering) hold ad research, creative and Ad Library method beyond the copy-research use here.
- Landing pages and site conversion: the landing page folder (07-LPG in older numbering) holds pop-up interaction with site conversion, PDP objections and checkout.
- Offers: the offers folder holds discount economics, guarantees and bundle design; this folder only sets where offers sit in flows.
- Ad copy: 11 (copywriting) holds long-form and ad copy frameworks; this folder keeps email and SMS copy only.
- Retention and loyalty: loyalty program design lives outside this folder; this folder holds the emails that promote it.
