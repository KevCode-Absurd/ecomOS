# Ecommerce review: 21-OPS-team-and-management

## 1. Score: 2 of 5

The store-specific content is real and usable (revenue-stage hiring triggers, tech pack, critical path, 3PL RFP and SLA, forecast and reorder, CS tiering), but it is a minority of the ruleset and comes almost entirely from 1 single-operator, unverified source (04). The largest blocks, leadership practice (Multipliers-Diminishers) and team health (Five Dysfunctions plus the OD toolkit), are general management content with no store translation, even though the playbook admits in section 0 that 4 of 7 sources have no ecommerce case in the original text. Nothing here is wrong for a store; the problem is genericness, not misfit.

**Section 3 rule count by type (108 domain rules, R1 to R108; R109 to R113 are ecomOS governance rules, not scored here):**

| type | count | share |
|---|---|---|
| (a) store-specific | 29 | 27% |
| (b) generic, correctly applied to a store | 4 | 4% |
| (c) generic, no store framing | 75 | 69% |
| (d) out of scope for a store | 0 | 0% |

16 of the 29 (a) rules are section 3.7 (operating process ownership, all source 04). The other 13 sit in org-stage triggers (3.1), 1 hiring rule, 1 decision example (Lands' End), founder archetype, and R105 to R108. Section 3.3 (leadership, 20 rules), nearly all of 3.4 (team health, 28 of 29) and 3.5 (role tools, 7 rules) are entirely generic: a SaaS company, a law firm or a nonprofit would read the exact same words.

## 2. Prioritisation check: no priority block exists

Section 0's "which sections to load" table routes by task, not by what matters most. Nothing ranks levers by store type (hero SKU vs catalogue, low vs high AOV, subscription vs one-off, marketplace-heavy, luxury or considered purchase, mobile-first India vs US); none of those conditions appear in the document. Draft block below, built only from the playbook's own rules and section 7 conflicts.

**3.0 Ecommerce priority order**

1. Name 1 owner and cadence on every operating artefact and silo (tech pack, critical path, PO tracker, forecast, 3PL SLA, CS routing, scoreboard) first. An unowned process stalls a store faster than a missing person. R1, R86, C8.
2. Fix demand planning and inventory ownership before any peak or demand surge. Stockout and over-order are both existential for cash. R7, R90, R91.
3. Check utilisation and process ownership before adding headcount; do not hire to cover a process nobody owns. R4, P21, C8.
4. Keep the PO tracker, critical path and 3PL SLA and invoice audit running as standing processes; these gate revenue timing and cash more than any leadership practice. R89, R92, R94 to R97.
5. Diagnose the bottleneck (traffic vs conversion, segmented by source) before funding a hire or CRO project. R102, R103, P31.
6. Hire against the founder's proven weak side (sourcing and product vs media buying), not a generic "A player" title. R5, R6, R104.
7. Stage the org chart against the store's own revenue and order-volume numbers. R2, R3, P1.
8. Staff customer service from the sales forecast curve, not current ticket volume, and track cost per ticket. R98, P30.
9. Set 1 scoreboard on the store's own north-star metric (repeat rate, contribution margin, blended CAC), not a generic category list. `[general practice]`: the fable's own example is generic; a store version exists in the pass 1 mini playbook for source 02 but was dropped from this merge. R57, P9.
10. Run leadership and team-health practice (Multipliers, Five Dysfunctions) once the artefacts above are owned. They raise output per person but do not by themselves stop a stockout or a missed peak. `[general practice]`, no source ranks this order. R25 to R73.
11. Use compensation levers (equity, performance pay) only for scarce acquisition or ops roles once margin is checked, never as a first move. R21, P31 step 6.
12. Apply role and responsibility tools (Belbin, responsibility charting, force field analysis) only when 1 specific role or decision is stuck. They are generic OD tools, not a default first step. `[general practice]`. R74 to R80.

## 3. Rule rewrites (store-specific wording, same condition, sources and card ids)

1. **R4.** Check whether the ops manager, media buyer or CS lead is the underused one before hiring a second person into that seat.
2. **R9.** For most ecomOS-scale brands this triggers well under 250 staff; the signal is a weekly trading meeting that stops surfacing real numbers, not headcount.
3. **R10.** Give a launch brief or creative concept to 1 person; use a team only for a multi-SKU seasonal drop needing merchandising, creative and ops together.
4. **R11.** For a small brand, 5 to 12 people is the whole leadership team (merchandising, growth, retention, ops, finance), not 1 department.
5. **R15.** Score a store hire on whether they will flag a bad creative brief or a weak launch plan out loud, not only on channel or platform skill.
6. **R18.** Ask "which core function do you own" of an ops, media buying or merchandising candidate specifically; the answer maps to the silo they would fill.
7. **R22.** Walk a new hire through the current PO tracker, forecast owner and CS routing rules, not only the team's interpersonal norms.
8. **R24.** For a store, "destructive high performer" often means a media buyer or merchandiser who will not share test data or hits SKU targets by starving other channels.
9. **R57.** Reject "revenue" as the scoreboard's own goal; use a 5 to 7 line set built from repeat rate, contribution margin, days of stock, ticket backlog and delivered-on-time, not the fable's software-company categories.
10. **R61.** Expect the guarded-regression relapse right after a peak season, when everyone reverts to firefighting.
11. **R65.** Run the weekly meeting as a trading review on the jugular numbers (conversion, stockouts, CS backlog), not a status report.
12. **R70.** Judge a launch team by whether the drop shipped on time and sold through, not by the meeting's atmosphere alone.
13. **R74.** Map Belbin roles to merchandising, creative, growth and ops when staffing a seasonal launch team; flag a team stacked with only Implementers.
14. **R77.** Write the 1-R chart for price changes, promotions, site changes, PO releases, 3PL escalations, refund exceptions and hire requests (already in P14; pull into the rule itself).
15. **R81.** For a store, high-stakes examples are a pricing or offer change, a platform migration, a 3PL switch, a repositioning, or a large PO; everything else is an everyday call.

## 4. Missing store levers (up to 8)

1. **Compensation bands for common ecom roles** (media buyer, CS lead, ops manager). Goes in 3.2, feeding D3. No bands in this folder; 07 gives 1 unverified figure (media buyer "multiple hundreds of thousands") `[web check]`, otherwise `[general practice]`.
2. **Structured job description template.** Goes with D2. No source here; 04 says it gives "almost no detail" on job descriptions. `[general practice]`.
3. **Distributed team and agency-pod cadence** (async tooling, time zones, contractor-only rosters). Buried, not missing: the pass 1 mini playbook for source 02 has a full "founder plus contractors" and "agency pod" adaptation (`sources/02-the-five-dysfunctions-of-a-team.md`, card `[ee63844c33b6]`), but none of it reached PLAYBOOK.md; R14 only says "no source gives a rule," which understates what pass 1 wrote.
4. **Ecom-specific scoreboard categories** (repeat rate, contribution margin, blended CAC, not the software-fable list). Goes in R57 and P9. Found in `sources/02-the-five-dysfunctions-of-a-team.md` line 281, card `[25f1e4a02461]`, not carried into the merge.
5. **Marketplace-channel team structure** (Amazon, Walmart, Meta Shop ownership separate from DTC roles). Goes in 3.1 next to R1's silos. No source here; `[general practice]`.
6. **Subscription retention ownership** (win-back, dunning, churn as a named silo). Goes in R1. No source here; `[general practice]`.
7. **Individual performance review and raise cadence tied to store KPIs**, separate from the team-health assessment (P5), which is kept out of pay (R60). Goes in 3.2 and D4. No source here; `[general practice]`.
8. **Make-vs-buy for fulfilment** (in-house warehouse vs staying with a 3PL). Goes before P28. No source here; 04 only covers 3PL selection once outsourcing is decided. `[general practice]`.

## 5. Demotions to an appendix "General background"

1. **R25 to R44, leadership practice detail** (about 1,265 words): the 5 Multiplier disciplines and opposites, told through Cisco, GE, P&G, Kissinger and Sridhar, none ecommerce.
2. **P6, P7, P8, trust-building exercises** (about 590 words): personal histories, the team effectiveness exercise, strengths and weaknesses round. Generic HR scripts with no store tie; keep only a 1-line pointer from P5 and P9.
3. **R74, R76, R78 to R80 and P13, P15 to P17, OD technique write-ups** (about 700 words): Role Analysis Technique, role negotiation, force field analysis, process consultation. Keep P14's store decision list in the base layer; move the generic technique detail.
4. **R68's MBTI and Thomas-Kilmann background** (about 150 words): already flagged as contested; keep the 1-line caution, move the description.
5. **Illustrative anecdotes inside R19, R24, R30** (about 350 words): the Shackleton ad, the Fred story, the Bloom Energy case, the GE bus trip, the Prahalad article. Keep the rule and card id; move the story.

Total candidate: roughly 3,000 words, about 15% of the playbook.

## 6. Deliverables check (section 9)

D1 (org plan), D3 (hiring plan), D5 (SOP index), D6 (cadence calendar) and D7 (bottleneck report) are things a store team would actually open and use; they carry store numbers and artefacts by name.

D4 (team health report) and D8 (leadership 30-day plan) read as generic HR or coaching worksheets. Add a required field to D4, "which store metric moved this quarter (repeat rate, ticket backlog, launch on-time percent)," so it is not only an internal dysfunction score. Rename D8 to "Founder or lead capacity plan" and require it name which operating artefact or KPI the practice change is meant to move; as written it could go to any manager in any industry.

D9 (high-stakes decision brief) should list store examples in the template (pricing or offer change, inventory or PO commit, platform or 3PL migration, hire or no-hire) instead of a generic "the decision"; the examples now live only in P18.

## 7. The single highest-value change

Merge the ecommerce translations that already exist in the pass 1 mini playbooks, most notably source 02's north-star scoreboard categories (repeat rate, contribution margin, blended CAC), its agency-pod and founder-plus-contractor adaptations, and its "weekly trading meeting" framing, into section 3's rules instead of leaving them in `sources/`. A generic manager-coaching prompt would produce R25 through R73 almost word for word, 48 of 108 rules. The fix is not new sourcing; it is carrying forward what pass 1 already wrote and pass 2 dropped, and forcing every generic leadership or team-health rule to name which store artefact, KPI or revenue-stage trigger it moves, the way section 3.7 already does for operations.
