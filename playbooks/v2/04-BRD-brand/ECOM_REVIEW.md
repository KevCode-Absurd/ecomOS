# Ecommerce review: 04-BRD-brand

Reviewed against `playbooks/v2/TEMPLATE.md` and the brief that this domain is for stores: PDP, cart, checkout, shipping, returns, inventory, peaks, AOV, repeat rate, CAC and margin.

## 1. Ecommerce specificity score: 3 out of 5

None of the 12 sources is written for ecommerce; all are general marketing, branding, naming and design books, talks and podcasts, and section 0 says so: every PDP, packaging or cart mapping is a "pass 1 adaptation," not something a source stated. The 3, not lower, is earned by real editorial work in spots like the PDP and ad consistency checklist (5.5), the premium signal audit (5.6), the line-extension gate (P9, 5.7) and the small-brand process (P13), which read as built for a store. It stays at 3, not higher, because most of the 150 decision rules still read like a generic branding course, with no store framing and no ranking of what matters first.

Rule count by category, section 3, all 150 rules, judged by whether the rule's condition or example names a store mechanism (PDP, packaging, cart, checkout, marketplace listing, SKU, repeat purchase). Counts are judgment calls on about 10 to 15 borderline rules, not a machine count.

- (a) store-specific (source itself is ecommerce-native): 0. No source in this folder is written for a store.
- (b) generic but correctly applied to a store: 60 rules (40%). Mostly pass 1 adaptations: PDP headlines, packaging and unboxing, hero SKU gating, sellout-as-inventory-failure, premium ad metrics.
- (c) generic, no store framing: 90 rules (60%). Positioning theory, naming theory, brand psychology claims, content and audience advice, persistence and measurement philosophy.
- (d) out of scope for a store (B2B, SaaS, service, enterprise only): 0 in section 3 itself. The playbook already routes retail-margin and hiring content (source 04) to other folders, so nothing genuinely out of scope was left in the decision rules.

## 2. Prioritisation check: no, draft below

The playbook has a task-routing table (section 0), but nothing ranks levers by revenue impact, and nothing branches by store type (hero SKU vs catalogue, low vs high AOV, subscription vs one-off, marketplace-heavy, luxury vs impulse, mobile-first India vs US). Add this block after section 2. Store-type conditions are marked `[general practice]` where the playbook gives no ranking of its own.

**3.0 Ecommerce priority order**

1. Category rung and the one claim (R3, R4, R7). Hero-SKU brands claim a rung fast; catalogue stores claim it per hero category (R82, R101). `[general practice]` for the split.
2. Price band and premium-vs-value call, before design spend (R29 to R31, R33, C5). High-AOV brands protect price; low-AOV brands can use price as an entry creneau (R8). `[general practice]`
3. Claims register and provable-claims gate (override 1, R48). Before naming or ads, every store type; a false "first" or "only" claim is a legal and marketplace-policy risk.
4. Name and searchability (R57 to R60, R70, R71, C2). Marketplace-heavy stores weight descriptive names higher; a flagship brand with no marketplace listing can risk coined sooner. `[general practice]`
5. PDP and homepage brand consistency (checklist 5.5, R104, R105). Highest-traffic surface for any store; run before ad creative is greenlit.
6. Packaging or unboxing as the decisive touchpoint (R99, R41, R53). Above identity work for a physical product; below the PDP for a digital-only listing. `[general practice]`
7. SKU and line-extension gate (P9, R76 to R82, checklist 5.7). A hero-SKU brand waits until the hero clears its revenue bar (R79); a catalogue brand runs this on every new listing.
8. Promo cadence vs premium position (checklist 5.6, C5). High for a considered-purchase or premium brand; lower where discounting is part of the value story.
9. Founder-as-face decision (C13, R132). High for a founder-led DTC brand in years 1 to 3; drops out with no visible founder.
10. Voice sheet and reading-level compliance (R103, override 4, 9.6). Above full identity work; every piece of copy needs it now and it is cheap.
11. Owned audience and permission asset (R128). Higher for subscription and repeat-purchase brands, since R114's replenishment cues need a channel to land in.
12. Identity system depth: marks, colour, type (R89 to R102). Last; cheapest to iterate later and least likely to move revenue alone. `[general practice]`

## 3. Rule rewrites (15)

Condition, sources and card ids unchanged; only the wording changes to name the store mechanism.

1. **R1**: A PDP headline, price or pack change is a mind-share move; judge it by ladder movement, not a spec sheet.
2. **R2**: On a PDP or hero ad, cut to the one line a scrolling mobile shopper reads in 3 seconds; a subhead and at most 2 bullets carry the rest.
3. **R4**: Check who already claims the slot on the category's Amazon, Flipkart or Google Shopping results before writing a "first" claim.
4. **R5**: Do not build a PDP or comparison page that repeats the leader's exact promise (free shipping, fastest delivery); pick an angle the leader's listing does not use.
5. **R10**: A homepage written for every buyer (gift shopper, self-purchaser, wholesale) dilutes conversion; name the primary shopper in the hero and route the rest to a secondary collection.
6. **R11**: Size the target by how many repeat buyers at the store's AOV and margin sustain the business; a hero-SKU brand may need only a few thousand.
7. **R12**: Plot the brand against every checkout alternative, including doing nothing and a marketplace private label, on axes a shopper weighs mid-cart, like price vs delivery speed.
8. **R18**: Before shooting a PDP hero image, check whether competitors use the same category cliche shot; shoot the image shoppers have not scrolled past.
9. **R28**: Answer the 6 questions against the store's funnel: rung in category search results, the rung the PDP claims, whom the ad targets, whether the headline matches the hook.
10. **R37**: Test whether removing the product from a PDP or lifestyle hero image still signals the brand's promise; a generic lifestyle shot with no buyer-specific aspiration fails this.
11. **R60**: For product and collection titles, which double as search terms, default to a descriptive title with the benefit visible in the first 60 characters of a mobile result; save a coined name for the parent brand only.
12. **R89**: A refresh that changes only the logo, not the PDP template, the packaging insert and the shipping confirmation email, has not changed the brand.
13. **R117**: Test recognition from packaging alone, logo covered, at thumbnail size; relevant only once repeat buyers already recognise the brand, not for a store's first collection.
14. **R124**: A "low stock" or "selling fast" PDP badge must match the real stock file; a fabricated counter breaks override 1 and risks a marketplace policy strike.
15. **R143**: Classify every ad line as performance (ROAS, CAC) or brand (branded search lift, repeat rate); do not kill brand-building creative on a performance yardstick.

## 4. Missing store levers (8)

1. **Catalogue and assortment strategy** (which SKUs get brand spotlight, which stay workhorses). Goes in Group E near R82, R101. Source: `02-this-is-marketing.md`, card `2b78cfe849b3` (long-tail escape), in the sources but not carried into pass 2.
2. **Channel-based product architecture** (which format scales on DTC vs marketplace vs retail). Goes in Group E near R79. Source: `04-premium-is-about-positioning.md`, card `b5c53d8871d1`, same gap.
3. **Subscription-specific brand promise** (replenishment ritual, churn-aware messaging, tier naming). Near R49 and R114. Source: `02-this-is-marketing.md` card `573fc71dee16` gives sizing only; the promise-writing part is `[general practice]`.
4. **Full-funnel touchpoint audit** (search result to PDP to cart to shipping email to unboxing to support, functional vs experiential). Buried as 1 line in R99. Source: `05-designing-brand-identity.md`, cards `c383852eb750` and `f4bd6b669b5c` (moments of truth), which give the full walk pass 2 compressed to one touchpoint.
5. **Returns and exchange policy as a brand trust signal**. Touched once in P11 step 5 as an unproven inference, never its own rule. Source: `09-building-a-brand-redesigning-a-business.md`, card `a9b87b90a092`, and `05-designing-brand-identity.md`, card `9ff53840ee86`.
6. **Marketplace brand-page and buy-box constraints** (Amazon A+ content, Flipkart brand store). No source in this folder, `[general practice]`. Goes in Group F, mechanics handed to 24-DEP.
7. **AOV-based journey branching** (impulse low-AOV vs considered high-AOV: trust badges, review placement, financing messaging). No dedicated source; R33 covers only the high-ticket half. `[general practice]`.
8. **Mobile-first and India-vs-US execution** (thumb-reach hero placement, COD trust, festival demand, payment-trust badges). Source 05 lists a mobile and apps chapter in its table of contents, but its own file says that chapter is missing from the extracted text. No source in this folder, `[general practice]`.

## 5. Demotions to an appendix "General background"

1. **R123**, the brand-vs-religion 10-trait checklist (about 150 words): a 65-subject scan and 14 interviews with no sampling method; not actionable for a store.
2. **R121**, the sonic-asset and Nokia ringtone test (about 120 words): most stores have no jingle or sonic mark.
3. **R66, R80, R83 case detail** (about 250 words): the 1980 initials-awareness survey, the Alka-Seltzer Plus case, the P&G Tide case. Keep each rule's 1-line takeaway; move the case narrative.
4. **Section 6 rows that are single 1960s to 1980s ad-agency case numbers** (about 300 words): Avis's profits, Protein 21, Pall Mall and Pringle's share drops, the Rolls-Royce unit count, Mailgram and Long Island Trust percentages. Already back rules elsewhere (R7, R76, R2, R11); the table is history, not a usable benchmark.
5. **R135 to R138** (about 400 words): video-hook structure, framework-building from a creator's own data, craft over metrics, PR as fame. Already routed to 13-ORG and 10-MCR; little left specific to store brand strategy.

## 6. Deliverables check (section 9)

Mostly usable. 9.1 (positioning statement and map), 9.5 (guidelines), 9.6 (voice sheet), 9.7 (PDP or ad consistency audit) and 9.8 (premium signal audit) are things a store team would open and use, not generic documents; 9.7 and 9.8 are store-native. 9.2 (brand brief) and 9.3 (naming shortlist) read closer to a standard agency deliverable, though 9.3 requires a PDP-header mock-up. Add **9.9, full-funnel touchpoint audit**, using missing lever 4 above, since nothing today delivers a whole-journey view; only the PDP and ad layer (9.7) stands alone.

## 7. The single highest-value change

Add the "3.0 Ecommerce priority order" block and branch it, and the section 0 task-routing table, by store type: hero SKU vs catalogue, low vs high AOV, subscription vs one-off, marketplace-heavy vs DTC-only, considered vs impulse. Today the playbook treats all 150 rules as equally load-bearing reference material and lets the agent pick sections by task name; it never says positioning and price should settle before naming, and naming before identity depth, or that a subscription brand should weight R114's replenishment ritual and R128's owned audience far above a one-off luxury brand's packaging work. That ranking turns a reference manual into a decision engine that tells the agent what to do first for Gehna, versus a hypothetical low-AOV subscription brand, without changing one underlying rule.
