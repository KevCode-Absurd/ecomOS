# Ecommerce review: 02-AVT customer avatars and market research

Reviewer note: this file reports findings only. PLAYBOOK.md and TEMPLATE.md were not changed.

## 1. Ecommerce specificity score: 4 out of 5

The procedures, checklists and deliverables are strongly store specific: Amazon star bands, the Meta Ad Library, Shopify post-purchase surveys, PDP proof, cart abandoners, and named handoffs to 03-OFF, 07-LPG, 10-MCR and 24-DEP. Section 3, the decision rules, is weaker: about a quarter of the 108 rules carry the source's general jobs-to-be-done or B2B theory with no store hook at all, and there is no single place ranking what matters most for a store by store type. That gap, plus a benchmarks table of mostly single-source, unverified numbers rather than store economics (AOV, CAC, contribution margin), costs a point. Not more, because the folder is honest about every weak number and never invents a claim.

**Section 3 rule count by category** (108 rules, R1 to R108; judgment calls on borderline rules, counted once each):

- (a) Store-specific: 41 rules (about 38%). Examples: R13 (named failed solutions like minoxidil), R16 (little hire as repeat purchase or subscription retention), R34 (Amazon star-band mining), R59 (Shopify post-purchase survey), R77 (Meta sensitive-attribute policy), R103 to R108 (ecomOS overrides).
- (b) Generic but correctly applied to a store: 39 rules (about 36%). Examples: R1 (job not demographic, tied to copy and creative), R28 (segment by consequence and cohort), R55 (incentives, with a store credit substitute), R84 (scopes B2B ICP out of consumer stores).
- (c) Generic with no store framing: 28 rules (about 26%). Examples: R2 (functional, emotional, social split, illustrated with childcare), R43 (Keyword Planner, used as any business would), R60 (no focus groups), R100 (customer contact, illustrated with "a plumber, a farm, SaaS or DTC").
- (d) Out of scope: 0 rules. Where a source is B2B (02, 07), the playbook scopes it to a wholesale line (R84) or adapts it (R49, R59) instead of leaving it unscoped.

## 2. Prioritisation check: no, and here is the draft block

No. R82 gives a 2-tier order (dominant avatar first, then the highest-evidence untapped candidate) and R81 says one avatar per product line, but nothing conditions the approach on hero SKU versus catalogue, AOV, subscription versus one-off, marketplace-heavy sellers, considered purchase, or geography. Grepping `sources/` confirms it: AOV and catalogue appear only as one-off anecdotes (a competitor's AOV in 03, Mercer's B2B marketplace in 01), subscription appears only in the little-hire rule and one churn example (02's "Chicken Box"), and India, mobile-first and luxury do not appear at all. Draft block below.

**3.0 Ecommerce priority order**

1. Anchor on the brand's own top customers if it has buyers; anchor on competitor Ad Library data and reviews only if not (R19, R82). This decides every step after it.
2. Confirm scope: a consumer avatar, or a separate B2B, wholesale or gifting line (R84, R85). The wrong scope wastes the effort.
3. Run the mechanism audit before committing: no real product difference means avatar work is the main lever; a real difference routes to 01-PRD and 03-OFF (R24, C12).
4. Match research depth to the stake: a 60-minute sprint before a copy round, the full sequence before a launch or scale attempt (R32, P1, P2).
5. Single hero SKU: build one deep record. Multi-SKU catalogue: run the prioritise-and-count step per product line and cap it at one primary avatar per line this cycle (R81, R25, P25). `[general practice]` the catalogue framing itself; the sources speak to "product line," not to a large multi-SKU catalogue.
6. Mine the store's own passive data first (reviews by star band, tickets, returns, post-purchase survey) before public forums; it is cheaper and already store-specific (R30, R34, R59, R61).
7. Treat repeat purchase rate, or subscription retention where the brand sells on subscription, as the proof gate before an avatar counts as confirmed (R16). `[general practice]` naming subscription vs one-off as the condition; the source gives only the general little-hire rule.
8. Saturated or commodity catalogue: run the untapped-avatar pipeline instead of another angle for the same avatar (R96, R24).
9. Segment by consequence, cohort, and buyer versus user for gift-heavy or considered-purchase categories, where the buyer and the user are often different people (R28, R85). `[general practice]` flagging "considered purchase" and "gift-heavy" as the trigger; the rules exist but not this framing.
10. Push the record through the whole funnel for congruence before it reaches copy, and keep Meta targeting broad while the creative carries the avatar (R89, R90, R91, C6).
11. Route anxieties, failed solutions and the Why chain to the offer and page agents as flagged, not asserted, claims (R72, R92).
12. Re-run the dominant-avatar check and the persona-use audit every quarter; downgrade any record with no new first-party evidence (R83, R76, R100).

Marketplace-heavy sellers and India-versus-US mobile-first differences are not covered anywhere and are listed as missing levers below rather than forced into this order.

## 3. Rule rewrites (15)

Condition, sources and card ids stay; only the wording changes to a store example.

1. **R2**: mattress, not childcare: functional is pressure relief, emotional is "will I finally sleep," social is "what will guests think of the guest room."
2. **R4**: "feel confident" is a need; "premium" or "eco-friendly" is an attribute; the job is "look sharp for a pitch without ironing a shirt at 7am."
3. **R5**: run the verb-plus-noun test on a PDP job: "get my kitchen counter clear before guests arrive," then cross-category alternatives (an organizer, a bigger bin, decluttering, doing nothing).
4. **R38**: name category subreddits instead of "emotional" versus "tactical," for example r/SkincareAddiction for feeling, r/MaleFashionAdvice for how-to.
5. **R43**: record autocomplete phrases for the PDP title, meta description and ad headline, not only for niche sizing.
6. **R51**: add that an online stranger cannot be confirmed as a paying customer; the store's own order data can filter invites to real buyers.
7. **R52**: tie the count to the store's own purchase window (recent buyers, buyers past the return window, lapsed subscribers) instead of a generic sample size.
8. **R54**: phrase timeline questions in store terms: first saw the ad, added to cart, abandoned, came back, checked out.
9. **R60**: extend the ban to a PDP feature-vote widget or a reviews-page poll, not only a room-based focus group.
10. **R62**: storyboard the store's own journey: ad or search, PDP visit, cart, checkout, unboxing, first use, repeat or subscribe.
11. **R64**: the crutch risk is AI research run before the operator has read this brand's own reviews and tickets, not research generally.
12. **R68**: set content altitude per channel: PDP copy at 101, a retention email at 301, matched to the buyer's experience.
13. **R75**: chain a store benefit: "faster charging" leads to "less morning stress" leads to "not late for school drop-off."
14. **R76**: audit persona use across PDP copy, ad briefs and email flows by name, not just "briefs."
15. **R100**: keep DTC in the list but lead with the roles that should join calls: support, fulfilment, retention or email.

## 4. Missing store levers (8)

1. **AOV or price-tier segmentation of avatars.** No source; AOV appears only as one competitor anecdote in 03. `[general practice]`. Goes in 3.3, near R29's demand matrix.
2. **Marketplace-heavy sellers with no CRM or first-party list.** No source; every procedure assumes a data layer and a customer list. `[general practice]`. Goes in section 0 and 2, as a third branch beside R19's existing-versus-new split.
3. **Considered-purchase or long sales cycle depth.** Partial source: 02 names "impulse versus considered, single item versus cart-building" as an open gap it never fills [`bf1e76633e2e`]. Goes in 3.7, near R84.
4. **Mobile-first or regional differences (India versus US, WhatsApp, cash on delivery).** No source; every named platform (Reddit, Amazon, TikTok, the Ad Library) is treated as US and English-language. `[general practice]`. Goes in section 0's web-check list and R48.
5. **Subscription-specific split: acquisition avatar versus win-back or churn avatar.** Partial source: R16, R58 and 02's "Chicken Box" churn example [`2dfaff611f9a`], never built into its own lever. Goes in 3.2, near R16.
6. **Influencer or UGC creator matching to an avatar.** No real method; only background on Gymshark's creator sponsorships in 06 [`58497983a714`]. `[general practice]`. Goes in 3.8, near R91.
7. **Fit, size and return-reduction copy per avatar.** Partial source: R15 names sizing and fit fear as ecommerce negative jobs, but no size-guide deliverable follows. Goes in 3.6 and the D5 angle map.
8. **Customer support scripts or macros by avatar.** Partial source: 02's live-chat fix example [`2dfaff611f9a`]. Goes in the procedures, as a handoff note to 17-CXP.

## 5. Demotions to a "General background" appendix

- **R101** (SNHU and FranklinCovey measurement examples, about 150 words): organisational-design case history, not a store rule.
- **R102** (purpose brand: FedEx, IKEA, Volvo, V8, about 150 words): brand-theory history with no DTC case; section 1 already says it belongs in 04-BRD as a long-horizon note.
- **B2B ICP mechanics inside R84 and C7** (company firmographics, buying committee detail, about 150 to 200 words): keep the one-sentence scoping rule ("a consumer brand does not build an ICP layer"); move the taxonomy detail, since a store agent never runs it.
- **The unsourced vanity-numbers row in section 6** ("$10k, $30k, $100k days... $200 CPM and $5 CPC," about 30 words): the table itself says this row is "not used anywhere in this playbook." Drop it rather than keep it in a working benchmarks table.

Total: roughly 450 to 500 words of about 26,000.

## 6. Deliverables check (section 9)

Yes, mostly. D1 (avatar record), D2 (priority table), D3 (evidence file) and D5 (creative angle map) are things a store team would open and use: quote ids, Ad Library competition reads, little-hire metrics, and a direct handoff to 10-MCR, 11-ADC, 07-LPG and 03-OFF. This reads as a creative test plan input, not a generic persona slide.

Two changes:
- Rename **D2** from "Avatar set with priority" to "Avatar priority and test queue," matching the action-plan language used elsewhere in ecomOS.
- Fold **D6** (untapped avatar shortlist) into D2 as a labelled section instead of a separate file; both are ranked candidate lists for the same decision and a store team should not have to check two files to see the full queue.

## 7. The single highest-value change

Add the "3.0 Ecommerce priority order" block above, or one like it, as a real section instead of leaving the store-type logic scattered across R19, R24, R81, R82 and R84. Right now an agent has to reconstruct, from five different rules, whether it faces a hero-SKU or catalogue brand, subscription or one-off, saturated or not, before it can decide where to start. One ranked, conditioned block turns that into a checklist, and it forces the playbook to say plainly, in one place, that AOV tiers, marketplace-only sellers and regional or mobile-first differences are not covered yet, instead of leaving that gap to be found rule by rule.
