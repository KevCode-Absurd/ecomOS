# Ecommerce specificity review: 14-EML email lifecycle

Reviewed against playbooks/v2/TEMPLATE.md and the 13 mini playbooks in sources/.

## 1. Score: 4 out of 5

This playbook is dense with ecommerce framing where it matters most: every core flow (welcome, browse, cart, checkout, post-purchase, replenishment, win-back, sunset, back in stock) is built from AOV, discount policy, days-between-orders and order-count data, not generic "nurture" advice. It loses a point because a large, self-contained block (deliverability, section 3.18, about 830 words plus matching procedures) reads like a generic email-sender manual that would not change for a SaaS client, and several copy and design rules never touch a store fact. The store-specific material is not thin, it just shares space with a generic email-marketing course merged in rather than translated.

Section 3 has 195 numbered decision rules (R1 to R195). Counting each rule once:

- (a) store-specific: 115 rules (59%). Nearly all of 3.5 to 3.13 (the 12 flow subsections), most of 3.2, 3.14, 3.19, and all 10 ecomOS override rules (3.21).
- (b) generic but correctly applied: 32 rules (16%). Mostly popup UX mechanics, consent law applied to marketing segments, and testing method applied to flow revenue.
- (c) generic, no store framing: 48 rules (25%). Concentrated in deliverability (3.18, 16 of 17 rules), plain copywriting and HTML design mechanics (3.16 to 3.17), and generic A/B test mechanics (3.20).
- (d) out of scope for a store: 0 rules. Even the 1 B2B-newsletter source (06) is filtered through store-relevant lessons.

This is a judgment call on borderline rules, so treat the split as approximate, not exact.

## 2. Prioritisation check: missing

The playbook has a task-routing table (section 0) and R2 hints at a build order, but nothing ranks levers by AOV, catalogue shape, subscription vs one-off, or market. Draft below, built only from the playbook's own rules and section 7 conflicts.

### 3.0 Ecommerce priority order (draft)

1. Deliverability and tracking floor: a flagged sender or missing attribution invalidates every step below. R135 to R137, R179, P1, P2.
2. Cart and checkout abandonment flows: highest revenue per build hour; R55 says 90% of audited accounts lack a real Added to Cart flow. R55 to R64, P8.
3. Welcome flow: biggest per-entrant conversion win, 10% to 20% of entrants, most of it in 72 hours. R41 to R46, P5.
4. Popup and list growth: opt-in rate caps every downstream flow's volume; offer is the biggest lever on it. R7 to R10, P3, P4.
5. Post-purchase flow: most repeat purchases land inside 30 days of order 1; ranks higher for repeat or replenishable catalogues, lower for a 1-and-done gift item. R65 to R69, P9.
6. Core segments (engaged, VIP, prospects vs customers): needed before campaigns or suppression can run safely. R86 to R91, P12.
7. Campaign cadence and content mix: campaigns and flows split email revenue about 50/50 once flows exist; do this after steps 2 and 3, not before. R3, R100 to R102, P13, P14.
8. Win-back and replenishment: ranks higher for consumables and subscription-adjacent catalogues (time it from the brand's own days between orders), lower for a single considered purchase bought once. R72 to R78, P10.
9. Sunset and suppression: protects deliverability as the list ages; low priority for a new small list, high once list age passes 6 months. R79 to R82, R92 to R93, P11.
10. SMS program: only after flows and consent are solid (R25); ranks higher for mobile-first markets with heavy phone use such as India (R192), lower where iPhone share and iMessage vendor claims do not apply. R152, R157, R192.
11. Copy and design testing: marginal gains once structure exists; skip granular tests like CTA colour under about $100k a month (R176 says so directly). R173 to R176.
12. Loyalty, birthday and back-in-stock extras: highest value for catalogue brands with a loyalty app and repeat buyers, lowest for a single hero SKU with no program. R83 to R85, R94.

Lines 1, 6, 7 and 11 come from the playbook's own revenue-share and gating rules. Lines 5, 8, 10 and 12 add store-type conditions stated elsewhere but never ranked; those clauses are `[general practice]`, since no single source ranks flows end to end.

## 3. Rule rewrites (15)

Condition, sources and card ids unchanged; wording now names a store fact.

1. **R30** (honour unsubscribes at once): a subscriber who cannot leave sits inside win-back and sunset counts and skews the revenue-per-recipient math the program is judged on.
2. **R34** (UTM tracking on): turn it on so flow and campaign revenue split cleanly from paid and organic in Shopify or GA4, the split that decides R3 and R4.
3. **R101** (never skip weeks): silence then a Black Friday blast reads as re-engagement fraud to Gmail right when the brand needs inbox placement for its highest-revenue week.
4. **R110** (resend to non-openers): reserve this for launch day, a real restock, or a sale's last day, never an evergreen send with no expiry.
5. **R111** (write for skim): a shopper reads this one-handed while comparing your product to 2 open competitor tabs, not while relaxed; the first line has to survive that.
6. **R112** (simple words, 5th grade): write at the level of someone deciding if a $40 product solves their problem in the next 10 seconds, not a general reader.
7. **R117** (regulated claims): check claims about ingredients, materials, safety or shipping speed against the brand's spec sheet or returns data, never imply them.
8. **R118** (subject line rules): frame the curiosity gap around a product benefit, a real restock, or a real deadline; a subject that oversells the product invites returns.
9. **R120** (sender name consistency): keep 1 sender identity across the journey so a customer trusts the win-back email from the same "person" who sent the cart email.
10. **R122** (email width and text size): 600px and 16 to 18px exist so a product photo and price stay legible on the phone screen most orders come from.
11. **R124** (section order and CTA): every section ends on a path to a product page or the cart, never a generic "learn more"; the goal is a purchase, not a click.
12. **R127** (infographics over paragraphs): use them to show how the product works or a before-and-after, content a listing page cannot show as well.
13. **R135** (deliverability = reputation score): a low score silently shrinks the reach of every cart, browse and post-purchase flow, where the store's recovery revenue lives.
14. **R145** (improve the email before the technical fix): the fix that works is usually a real bestseller, a real product photo and a real founder voice, not a generic rewrite.
15. **R174** (test methodology): the winning metric for a store test is placed order rate or revenue per recipient, never open rate; state that in the hypothesis before testing.

## 4. Missing store levers (8)

1. **WhatsApp for non-US, mobile-first markets.** Source 02 recommends WhatsApp where SMS is expensive, and R170 already rules out iMessage for Android-heavy markets like India, with no alternative offered. `02-klaviyo-email.md`, card `b9130f4f4dca`. Goes in 3.19, next to R170.
2. **Loyalty events beyond birthday** (points earned, tier up, reward redeemed). Source 03 names all 3 as integration events, but only the birthday flow gets built (R85). `03-2026-klaviyo-email-marketing-full-course-3-hours.md`, card `9ca8e23a01f3`. Goes in 3.13, as R85a to R85c.
3. **A refunds segment and post-refund touch.** Klaviyo's own "Refunds" segment is named as usable but never becomes a rule. `02-klaviyo-email.md`, card `516248e6ac94`. Goes near the post-purchase split (R67).
4. **Subscription lifecycle emails**: charge reminder, pause-or-skip save flow, failed-payment recovery. Subscribers are only excluded from acquisition flows (R65, R157), never built for. No source in this folder, `[general practice]`.
5. **Gift-purchase handling**: a different post-purchase sequence for buyer versus recipient. Only generic "gift guide" content exists. No source in this folder, `[general practice]`.
6. **Size or fit follow-up to head off a return**, for size-dependent products. R70 covers how-to content by category, not a fit check. No source in this folder, `[general practice]`.
7. **International shipping-delay communication**, separate from the domestic timing in R66 to R68. Ship-to country only drives consent and popup targeting (R19, R154). No source in this folder, `[general practice]`.
8. **Marketplace-channel exclusion** for customers bought via Amazon or another marketplace the brand cannot email. Only wholesale exclusion exists, and only for the popup (R19). No source beyond wholesale, `[general practice]`.

## 5. Demotions to "General background"

- **Section 3.18, most of R135 to R151** (about 830 words): SPF, DKIM, DMARC mechanics, and the numeric spam, bounce, unsubscribe, open and click floors. None of this changes for a store versus a SaaS or publisher sender. Keep only the store tie-in, that a deliverability floor gates opening the cart, browse and post-purchase flows (R146).
- **Generic copy and design mechanics** (about 400 words: R111, R112, R118, R120, R122, R124, R125, R127, R131, R133): plain-language writing, HTML width, line height, plain-text ratio, font fallback. Standard email craft, not store-specific; the store reasons belong in the section 3 rewrites above.
- **Generic A/B test mechanics** (about 200 words: R174, R175, R177, R181, R185): sample size floors, manual versus automatic winners, "optimise unique counts." Standard method for any digital channel.
- **Consent and compliance basics** (about 150 words: R26, R28 to R30): single versus double opt-in, unsubscribe handling. Keep the store overlay (R192, law per ship-to country) in the main text; move the general definitions.

## 6. Deliverables check (section 9): pass, mostly

All 7 deliverables (flow map, flow build specs, email drafts, segment definitions, campaign calendar, test plan, audit report) are concrete and store-usable: each names Klaviyo objects, ties to brand-record checks, and states a runnable format. None read like a generic "email marketing plan." Gap: consent, quiet-hour and SMS registration checks scattered across section 10 never become a deliverable, so legal or ops has no single sign-off before an SMS launch. Add a short "9.8 SMS and email compliance sign-off" pulling the relevant `[web check]` and `[needs brand data]` items into 1 checklist per market.

## 7. The single highest-value change

Add the "3.0 Ecommerce priority order" block from section 2. The playbook holds huge, well-sourced detail on every flow, segment and channel, but gives an agent no way to decide what a specific store needs first: whether to spend the next hour on a cart flow, deliverability, or this month's campaigns depends on the store's size, catalogue shape, AOV and market, and none of that logic exists in the document today. A generic prompt could already produce most of this flow content with a good source; it cannot tell a single-SKU brand to build the cart flow before a loyalty program, or a subscription brand to skip a win-back flow it does not need. That ranking, conditioned on store type, is what makes this playbook worth loading over asking a model cold.
