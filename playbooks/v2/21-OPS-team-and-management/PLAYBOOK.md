# 21-OPS team and management playbook

version: 2.0-draft  |  date: 24 Sep 2026  |  sources: 7 mini playbooks (7 independent voices)  |  cards: 258  |  built from: sources/*.md

## 0. How to use this playbook

**Who runs it.** The team and operations agent. Its job is to help a brand owner or agency lead design the org for the current revenue stage, decide and prepare the next hire, run the leadership and team health practices, put 1 named owner and 1 cadence on every operating process, and diagnose whether a plateau is a people problem, a process problem, a traffic problem or a conversion problem. It prepares decisions. A human makes every hiring, firing and pay decision (section 3.9).

**What the sources are.** 4 of the 7 sources are general management with no ecommerce case anywhere in the original text: 01 (Multipliers, a 2009 to 2010 leadership book built on 144 interviewed leaders), 02 (The Five Dysfunctions of a Team, a 2001 consultant's fable plus a 15-item questionnaire), 03 (an undated, unattributed public-sector team-building handbook), 05 (a Wharton interview built on watching about 100 executive simulation teams). Every ecommerce mapping in those 4 mini playbooks (agency pods, trading meetings, top-20 SKU launches, founder-plus-contractor rosters, Belbin roles mapped to merchandising and creative) was written by the pass 1 author, not by the source. This playbook marks each of those as `[pass 1 adaptation]` and never cites one as a source claim. The other 3 sources are founder or coach videos: 04 (the Oodie founder's operations guide, monetised with affiliate links and a mentorship pitch), 06 (a short YouTube talk with no data or client named), 07 (a 10-minute coaching call with a single self-reported founder and a lead-magnet pitch at the end). Their figures are self-reported and unverified. Section 12 rates each source.

**Which sections to load for which task.**

| task | load |
|---|---|
| Org chart vs revenue stage, next hire | 3.1, 3.2, 4 (P1 to P4), 5.1, 5.2, 9 |
| Leadership coaching for a founder or lead | 3.3, 4 (P18 to P21), 5.3, 7 (C1, C8) |
| Team health, meetings, cadence | 3.4, 3.6, 4 (P5 to P12, P24), 5.3, 5.4, 6 |
| Role clarity, who approves what, a stalled change | 3.5, 4 (P13 to P17) |
| A high-stakes decision (pricing, migration, 3PL switch, repositioning) | 3.6, P18, C1 |
| Operating process ownership: sourcing gates, forecasting, PO, 3PL, CS staffing | 3.7, 4 (P25 to P30), 5.5, 5.6, 6 |
| Plateau or "we need to hire" request | 3.8, P2, P31, 5.7, C5, C8 |

**What the agent must fetch before acting.** From the brand record: current roster with reporting lines, each person's demonstrated (not titled) strengths, current meeting cadence, whether a single overarching goal exists and who owns it, the list of process artefacts (tech pack, critical path, PO tracker, forecast sheet, 3PL SLA, CS routing rules) and their owners. From the data layer: revenue and order volume by month, ticket volume, conversion by traffic source, delivered-on-time percent, 3PL invoices and order counts, days of stock by SKU, cash position. From the user: the growth target, the hire budget, and any constraint the human has already set (no new headcount, no equity). Everything in this playbook that depends on those inputs is tagged `[needs brand data: ...]` and grouped in section 10. Nothing in the sources gives a benchmark that beats the brand's own numbers.

**Known source errors to carry forward.** Source 04's transcript says a $11,000 container split over 1,000 units costs "$1 per unit". The correct figure is $11 per unit; card [4cf8302e51b7] already corrects it, and this playbook uses $11. Source 03's team culture scale states both "below 60 of 100 is low team spirit" and "below 25 is low team spirit" without reconciling them; treat that instrument as a discussion prompt, not a measurement [50dadc5d2305]. Source 01 studied 144 leaders and rated 48 leadership practices; "48" is practices, never leaders [01bfefe3ebdb].

**Ecommerce first.** This playbook is for stores, not general management. Section 3.0 is the ranking: load it first, since it says which levers matter most before the detail groups below. Store-type conditions (hero SKU vs catalogue, low vs high AOV, subscription vs one-off, marketplace-heavy, luxury or considered purchase, mobile-first India vs US) decide which rules in the sections below apply to a given brand; check the condition stated in each rule before applying it.

## 1. Scope and outcomes

**Covers.** Org design by revenue stage (the 5 silos, founder-covers-until-volume-forces-a-hire, hiring order, span of control at the top). Hiring and vetting (the hiring bar, who interviews, the few interview questions the sources give, comp levers, onboarding through the team). Leadership practice (the 5 Multiplier disciplines and their Diminisher opposites, accidental diminisher checks, 30-day experiments, leadership style by information and time). Team health (the 5 dysfunctions chain, the 15-item assessment, the trust exercises, one overarching goal and a 5 to 7 line scoreboard, meeting cadence and ground rules, cascading messaging, the commit-check-close loop, stages of team development). Role and responsibility tools (Belbin roles, Role Analysis Technique, responsibility charting, role negotiation, force field analysis, process consultation). Operating process ownership (who owns the tech pack gate, the critical path, the forecast and reorder review, the PO tracker, the 3PL RFP, SLA and invoice audit, the CS tier split and capacity plan; the KPIs and cadences for each). Bottleneck diagnosis (traffic vs conversion, product-founder vs media-founder archetypes, utilisation before headcount).

**Routed to neighbour folders.** Source 04 is mostly supply chain and cost mechanics. This playbook keeps the team, process and management parts of it and routes the rest:
- To 18-COG-sourcing: the full tech pack contents list (drawings, GSM, grading, hardware, labels, packaging), supplier co-development vs independent designer and who owns the IP, MOQ and price negotiation tactics and the "about 20% improvement" example, de-speccing a product, Alibaba Trade Assurance and QC agents (Alibaba inbuilt QC, SGS), refund and quantity tolerance terms, freight forwarder selection and monthly re-shopping, ASN mechanics [24613aeb6cad] [9268b8dd340f] [48773124dba7] [0bfbfacfd9fe].
- To 20-FIN-finance-and-accounting: the landed cost formula and the Brand A vs Brand B $21 vs $28 example, duties vs sales tax treatment, the Shopify "Cost per item" field and daily profit reporting, ERP cost figures, the cash flow strain of fast growth, the equity vs cash comp structure itself [4cf8302e51b7] [05d7d9c866b8] [0ff782611bef] [b835681136c8] [22f9b83f5cae] [826839431464].
- To 17-CXP-post-purchase: helpdesk tool choice (Zendesk vs Gorgias), macro writing, ticket resolution diagnostics in detail, tracking codes, receipts and packaging that keep post-purchase emotion alive [d55c91623549] [08a8a291428f] [b22ff38bde5c].
- To 09-CRO-testing and 06-MEA-measurement: the mechanics of segmenting conversion by source and the leaky bucket funnel audit [5013501dc466] [4ccb3499516c].
- To 04-BRD-brand: marketing that encodes brand values and the "brand after revenue" sequencing detail [a22920b70388] [59f0f71e9914].

**Does not cover.** Ad copy (11-ADC), ad account work (24-DEP), offers (03-OFF), email (14-EML). None of the 7 sources gives a compensation band, a job description template, an SOP template, a trial task, or a remote-work tooling stack. Where the brief asks for one of those, this playbook says "not sourced" and leaves the field for the human.

**Business measures it moves.** Output per person (source 01's claim: 2x between the worst and best leaders, self-reported). Decision speed and execution after a decision (02, 01). Stockouts and over-ordering (04). 3PL overcharges and late picks (04). CS cost per ticket (04). Time lost to unresolved recurring issues (02). None of these has a benchmark in the sources beyond single-case figures; the brand's own before and after numbers are the measure.

## 2. Inputs the agent needs

| input | from where | required or optional | why |
|---|---|---|---|
| Revenue by month, last 12 to 24 months, and order volume | data layer | required | Stage gates in R3, R7, R100 use revenue and volume triggers; forecast base needs in-stock days |
| Current roster: name, role, reporting line, employee or contractor, hours | brand record | required | Org chart vs stage review (P1); silo coverage (R1) |
| Each person's demonstrated strengths and observed Belbin-type behaviours | brand record, user | required | Native genius (R28), role gap check (R75), archetype (R104) |
| Growth target and time window | user | required | Sets the one overarching goal (R57) and the hire trigger |
| Hire budget, equity willingness, any "no headcount" constraint | user | required | R21, R4, C8 |
| Current meeting list: name, length, attendees, agenda, owner | brand record | required | Cadence audit (5.4), R63 to R65 |
| Whether a single overarching goal exists, its number, deadline and owner | brand record | required | R57; if absent, run P9 first |
| Process artefact list and owners: tech pack, critical path, PO tracker, forecast sheet, 3PL SLA, CS routing rules | brand record | required | R87, SOP completeness check (5.5) |
| Ticket volume by week, CS cost (software plus agents) | data layer | required for CS staffing | R98, P30 |
| Conversion rate by traffic source, campaign and geo | data layer | required for bottleneck work | R102, R103, P31 |
| Delivered-on-time percent, pick time, 3PL invoice and Shopify order count for the month | data layer, 3PL portal | required for 3PL review | R96, R97, P29 |
| Days of stock by SKU, supplier lead time, stockout days in the trailing period | data layer, warehouse | required for forecast review | R91, P26 |
| Cash position and 13-week view | 20-FIN output | optional here, required before a growth push | R107 |
| Team assessment answers (15 statements per person) | user, collected by P5 | optional until team health work starts | R47 |
| Founder's own read of which core function they own | user | required for plateau work | R104 |
| Live web: current standing of MBTI and TKI, multipliersbook.com tools, acquisition.com/roadmap, tool names in 04 | web | optional | Section 11 |

## 3. Decision rules

Each rule: the rule, when it applies, the mini playbooks that support it (by number), conflicts (by section 7 code), card ids. When only 1 source supports a rule, it says so. Where sources disagree, the strictest condition is kept here and the disagreement is written out in section 7. `[pass 1 adaptation]` marks a mapping the pass 1 author added that the source never said.

### 3.0 Ecommerce priority order

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

Load this block first; the groups below are the detail.

### 3.1 Org design by revenue stage

**R1. Name the 5 silos before the first hire and give each 1 owner.** The 5: administrator (buying contracts, partnerships, reporting, strategy, brand image), customer service, order fulfilment, digital marketing, web development and design. A silo with no named owner (the founder counts) is a launch blocker. Applies to any ecommerce launch. Source 06 only, presenter's opinion with no data. [4c580913957e] [98fae764cd32]

**R2. The founder takes the administrator seat and personally covers the core tasks of the other silos while budget is tight. Do not hire 1 generalist to weakly cover all 5.** Applies from pre-launch until volume makes the founder's load unmanageable. Source 06 [98fae764cd32] [4c580913957e]. Source 04 agrees from the operations side: below about $1M revenue the founder holds every operational role and buys discrete tasks (a tech pack, for example) from freelancers, not staff [0ff782611bef] [87a5258c4926]. 2 sources, both single-operator opinion.

**R3. Add a person only when volume forces it, and name the trigger in the brand's own numbers before the hire.** 06 gives no number ("once you're settled"). 04 gives 2 revenue triggers: dedicated headcount to keep the shared PO and freight tracker reliable at about $5M to $10M revenue (past that 1 person cannot keep it current), and an ERP at about $30M to $50M. Strictest condition kept: write the trigger (orders per week, tickets per week, or revenue) into the hiring plan, and set it at or below the point where the current owner can no longer keep the process artefact current. Sources 06, 04. [4c580913957e] [5eb084517f52] [b835681136c8] `[needs brand data: order volume, ticket volume, revenue by month]`

**R4. Check whether the ops manager, media buyer or CS lead is the underused one before hiring a second person into that seat.** Source 01: answer a growth target with the logic of multiplication (get more from the people you have) before the logic of addition (more output needs more people). The logic of addition produces people who are "overworked and underutilized". Run the capability gap check (P21): if key people estimate their manager gets 50% or less of their capability, fix leadership before hiring. Applies whenever a growth target arrives with no budget, or a hire request is justified by "we are stretched". Source 01 only. Conflict C8 (04 says the missing ops role cost Oodie 30 to 40% of growth). [9417ffc8e0f0] [249b9719a074] [8abb782bbe28]

**R5. Define the hire around the specific missing function, never as "an A player for management".** Source 07 [12805cde65c1]. Source 05's third failure mode (a goals talk that never becomes "who does what") supports it [12ad1d771f2c]. 2 sources.

**R6. When a founder plateaus, hire the archetype the founder is not.** Source 07: owners are usually product and sourcing focused or media buying focused, rarely both. Ask the founder which core function they own. A confident, evidenced answer on one side means that side is fine; hedging ("I don't know", "not sure") on the other side is a weak signal that it is the missing capability. Applies at a plateau, before any hire. The source itself warns a founder may be modest about a skill they have. Source 07 only, advisor's pattern-matching, 1 self-reported case. [5813209a4dbd] [12805cde65c1]

**R7. Put an operations and planning owner in place before the first demand surge, not after.** Source 04: Oodie had nobody on planning when COVID demand spiked in year 2 (about $25M revenue), did not reorder enough, sold out; the founder's own retrospective estimate is 30 to 40% more growth with the role in place. The owner can be an ops manager, not a dedicated demand planner, once the business is profitable enough to pay one. Source 04 only, single-operator retrospective. [48e4499ac999] [87a5258c4926]

**R8. When a COO exists, the COO owns Product, Supply Chain, Fulfilment and Customer Service.** Source 04 names CEO, CFO, CMO, COO and gives the COO's 4 areas. No timing rule is given for when to create the role. Source 04 only. [0ff782611bef]

**R9. For most ecomOS-scale brands this triggers well under 250 staff; the signal is a weekly trading meeting that stops surfacing real numbers, not headcount.** Source 02: the trigger is staff meetings that no longer allow fluid, substantive discussion because too many people report to the top. The fable's numbers: past 250 employees, the CEO's 8 direct reports were regrouped to 5 under a COO and CFO. Judge the redesign by whether decisions and handoffs get faster, not by the chart looking cleaner. Numbers are illustration only. Source 02 only. [0fde892e7e47]

**R10. Give a launch brief or creative concept to 1 person; use a team only for a multi-SKU seasonal drop needing merchandising, creative and ops together.** Source 05 [9f7764e0e51b]. Source 03 draws the same line between a group (common boss, separable work) and a team (shared goal, interdependence, collective accountability) [6fa65887a2ae] [41fe0f74c164]. 2 sources.

**R11. For a small brand, 5 to 12 people is the whole leadership team (merchandising, growth, retention, ops, finance), not 1 department.** Source 03: a problem-solving team is 5 to 12 people from the same department; oversized teams suffer poor task division and friction, too-lean teams lack coverage [41fe0f74c164] [f9b3d93a12d9]. Source 02's model assumes roughly 5 to 9 direct reports around 1 leader [0fde892e7e47]. 2 sources, both conventions, no data.

**R12. Do not build the operation around 1 hero.** Source 05 calls the "great person theory" (over-relying on 1 dominant or visionary person) "almost always a big mistake" [12ad1d771f2c]. Source 01 names the leader-side version: Empire Builder (hoards talent), Know-It-All (caps the ceiling at what the leader knows) [d7ddc08248a1] [ec007ef36f5e] [9aef12c19ce2]. Source 01 also gives the antidotes: add backup without reducing ownership ("two in a box") [f78fe4052829], build leaders so you can step away [37aafeee291c], hand over leadership before it becomes a dependency [7216e54fa5f1]. 2 sources. Conflict C2 (few elite generalists vs redundancy).

**R13. Roles are explicit; stretch is on top of the role, not instead of it.** Source 05: the goals, roles, norms conversation must be explicit, and skipping the roles part is a named failure [d35411c91008] [12ad1d771f2c]. Source 03: Role Analysis Technique for any ambiguous role [ae9c30902c6c]. Source 02: accountability fails on ambiguity about who owns what [401b22a4cb2f]. Source 01's Hexal case (no org chart, "ameba" roles, talent flows to where the energy is) is 1 company's story [f7812fc26044]; 01's own Investor rule is to define ownership up front and then stretch the role 1 level above comfort [d150234124c0] [cb138faa8112]. Strictest condition kept: every role written, then stretched. 4 sources on explicit roles. Conflict C2.

**R14. Agency vs in-house, contractors and pods: no source gives a rule.** What the sources do say: buy discrete tasks from freelancers below about $1M (04) [87a5258c4926]; for a scarce skill, either learn it yourself or bring in a "star" and pay with cash plus performance pay or equity when margin is thin (07) [826839431464]; look for talent beyond the org chart, including people you do not own (01) [dbbe8a2e0b3d] [d70f32fe72f8]. "Pods with P&Ls" appear in no source. The founder-plus-contractors and agency-pod mappings in mini playbooks 01 and 02 are `[pass 1 adaptation]`. Treat any pod or agency structure as `[needs brand data: current vendor list, scope, cost and who reviews their output]` and decide with the human.

**R114. Set a cadence, async tooling and time-zone overlap for a founder-plus-contractors roster or an agency pod, the same way any team needs one (R63).** A full adaptation for this already exists in the pass 1 mini playbook for source 02 and was not carried into R14 above; do not treat contractor and pod structure as unsourced when it is only unmerged. Source 02 mini playbook, `sources/02-the-five-dysfunctions-of-a-team.md`. [ee63844c33b6] `[pass 1 adaptation]`

**R115. Give marketplace channels (Amazon, Walmart, Meta Shop) their own named owner, separate from the 5 DTC silos in R1.** A marketplace listing, ad account and fulfilment method differ enough from DTC that folding them into an existing silo hides who owns them. `[general practice]` No library source; verify against brand data before use.

**R116. Name a subscription retention owner (win-back, dunning, churn) as its own silo alongside R1's 5, when the store runs a subscription programme.** A subscription book decays without 1 named owner tracking churn and failed payments; folding it into CS or marketing hides the metric. `[general practice]` No library source; verify against brand data before use.

### 3.2 Hiring and vetting

**R15. Score a store hire on whether they will flag a bad creative brief or a weak launch plan out loud, not only on channel or platform skill.** Source 02: the candidate must be able to show vulnerability-based trust, engage in conflict about ideas, commit to group decisions, hold peers accountable, and put team results over ego [2ca0bcfdd550]. Source 06 adds drive toward a defined next level, and for a marketing hire, understanding of the company's objectives and ethics, not only channel skill [94576193b1cf] [a22920b70388]. 2 sources.

**R16. 1 owner runs the search; the whole team meets the finalist; screen fast, then go deep.** Source 02: the whole team interviews, 1 person owns the process [2ca0bcfdd550]. Source 01's Hexal case: 3-minute first interviews for 8 candidates, then 3 hours with the finalist [de18b6e39887] [f7812fc26044]. Strictest condition kept: short first screens are allowed, but no offer without the deep finalist round and the team's input. Conflict C7. 2 sources, both single cases.

**R17. Internal promotion vs external hire: debate it openly, invite last input, then the leader decides and states the criterion.** Source 02's criterion in the fable: can the candidate grow the function, and is any internal candidate close to ready. This is 1 situational choice; the source does not claim external beats internal. Source 02 only. [2ca0bcfdd550]

**R18. Ask "which core function do you own" of an ops, media buying or merchandising candidate specifically; the answer maps to the silo they would fill.** The questions: "What is the next challenge for you?" and "What is getting in the way of your being successful?" (01, the Romney Talent Magnet questions) [d70f32fe72f8]; the native genius probe, "what do you do better than anything else you do, without effort, without being asked, without needing to be paid", asked 3 ways and checked for convergence (01) [c9002d8e9d33]; "how have you broken through a previous goal" as a proxy for drive (06, no rubric) [94576193b1cf]; "which core function do you own", watching for hedging (07, aimed at founders, usable on candidates only as `[pass 1 adaptation]`) [12805cde65c1]. Trial tasks and an "SOP as promotion gate" are not in any source; leave both as `[not sourced: human designs]`.

**R19. Write the job ad honest and demanding.** Source 01: an honest, demanding ad draws well-suited applicants even when the work sounds hard. 1 anecdote. Source 01 only. [d7ddc08248a1] Shackleton ad text moved to Appendix A.

**R20. Look for talent past the org chart: contractors, adjacent roles, the support rep with an unusual strength.** Source 01: a $9 per hour part-time CS rep with a "listening spike" was moved to coaching in 3 weeks and launched the company's highest-margin product a year later (1 example, "more than a tenfold increase in value", not typical) [56fb92416c2f] [dbbe8a2e0b3d]. Source 01 only.

**R21. Compensation levers.** Source 07: when margin cannot support market cash pay for a scarce hire (its example: a top media buyer at "multiple hundreds of thousands of dollars a year", unverified), use equity, performance pay or other levers; equity is given up, not free [826839431464] `[web check: current market pay for senior ecommerce media buyers]`. Source 02: shift reward weight from individual to collective outcomes; tie rewards to results not effort; do not rely on money as the sole motivator; keep 360 feedback out of compensation [f865719ea5b4] [30d9d9379f95] [59329495c17e]. ecomOS: the human sets pay (R111). 2 sources.

**R22. Walk a new hire through the current PO tracker, forecast owner and CS routing rules, not only the team's interpersonal norms.** Source 02: each existing member teaches the newcomer 1 part of the operating model; cover each peer's role and the current collective goals; review the newcomer's working style against the team's; put them into a live debate the same day; let them watch peers hold each other accountable [1cab46c8ddf7]. Source 03's stage model says a new group forms, storms, norms, then performs; expect a short storming period and do not read normal friction as failure [98f70de504bd] (applying this to 1 new hire is `[pass 1 adaptation]`). 2 sources.

**R23. Confirm role fit with an assignment change before adding headcount.** Source 02's fable moves a resentful COO to head of sales rather than hiring. Source 02 only. [9cffbb518f9e]

**R24. For a store, "destructive high performer" often means a media buyer or merchandiser who will not share test data or hits SKU targets by starving other channels.** Source 01: remove the "prima donna" who cannot collaborate; the book says waiting too long to remove one is the common error [770627149af5] [3c9e69b660b3]. Source 02: promoting a talented but disliked analyst can cost several staff quickly; the lesson stated is that the manager's tolerance, not the employee, was the failure [f9f956b15e91]. Condition: only after specific observed behaviour is named and a real choice to change is offered (P22). The human decides (R111). 2 sources, both anecdote. Bloom Energy and Fred story detail moved to Appendix A.

**R117. Set comp bands for the common ecom roles (media buyer, CS lead, ops manager) before opening a search, not after a candidate asks.** Source 07's only figure, a senior media buyer at "multiple hundreds of thousands of dollars a year", is 1 unverified case [826839431464] `[web check: current market pay for senior ecommerce media buyers]`. No source gives a band for a CS lead or ops manager. `[general practice]` No library source; verify against brand data and current market pay before use. Feeds D3.

**R118. Use a structured job description template for every store role, not a free-text ad.** Source 04 says it gives "almost no detail" on job descriptions; no source here gives a template. `[general practice]` No library source; verify against brand data before use. Feeds D2.

**R119. Run an individual performance review and raise cadence tied to store KPIs, kept separate from the team-health assessment (P5) and out of pay per R60.** No source here gives a cadence or template. `[general practice]` No library source; verify against brand data before use. Feeds D4.

### 3.3 Leadership practice (Multipliers and Diminishers)

R25 to R44 moved to Appendix A: the 5 Multiplier disciplines and Diminisher opposites (Talent Magnet, Liberator, Challenger, Debate Maker, Investor), the accidental diminisher check, the 30-day practice change, and the cross-source agreement notes on vulnerability, hierarchy and expectations. General leadership content, no ecommerce case in the source text (see the ecommerce review's rule-count table). All rule ids and card ids kept with the moved text.

### 3.4 Team health

**R45. Treat the 5 dysfunctions as a chain and fix the lowest broken layer first.** Absence of trust causes fear of conflict, which causes lack of commitment, then avoidance of accountability, then inattention to results. Start where the chain is broken (usually trust), not where the pain shows (usually results). Source 02 only. [f0b5fc985510] [e77489155f5e]

**R46. Trust means willingness to be vulnerable, not predictability.** Admitting weakness, mistakes and skill gaps and asking for help without fear. Source 02 [0ae728a0b4ef] [2221f16dc981]. Source 03: trust is built slowly through shared positive experience and destroyed in a single careless act; leadership commits first and visibly [0de5f24898f1] [9ed83f4b4706]. Source 05: build trust mainly one-on-one, since group dynamics get complex [712acd79637a]. 3 sources.

**R47. Diagnose with the 15-statement assessment before intervening; re-run it; treat bands as rough.** Scoring 3 Usually, 2 Sometimes, 1 Rarely; 3 statements per dysfunction, max 9; 8 to 9 probably fine, 6 to 7 could be a problem, 3 to 5 probably needs addressing; compare the spread between members, not only the average. Source 02 only; not validated [9df78b1b4685]. Source 03's 30-item team culture scale has inconsistent bands (below 60 and below 25 both called low) and is a discussion prompt only [50dadc5d2305]. Conflict C9. Use 02's instrument for the team, and 03's items 25 to 30 (leadership sub-score, max 24, midpoint 12) only as a talking point.

**R48. Conflict is about ideas, never people; healthy conflict can look heated.** Source 02 [3b39fde08344] [c873496d4cc0]. Source 03's constructive vs destructive signs: constructive opens and clarifies issues, increases involvement, releases emotion; destructive diverts energy, polarises sub-groups, produces name-calling [4e22b3eaf48a]. Source 03: conflict is inevitable and needed; suppressing it during storming breeds resentment, apathy or exit [98f70de504bd]. 2 sources, plus 01's debate rules (R83).

**R49. A recurring, unresolved agenda item with a roughly even split is a fear-of-conflict signal, and "let's take it off-line" is avoidance.** Avoiding conflict does not save time; the same issue returns meeting after meeting, and suppressed disagreement goes underground as personal attacks. Source 02 only. [95958a74d490] [c873496d4cc0]

**R50. Assign a miner of conflict, give real-time permission, and restrain the leader.** Someone's job in a meeting is to surface buried disagreement and stay with it. When people retreat, interrupt to say the discomfort is expected, then confirm afterward it was useful. The leader does not break up conflict early to protect people. Source 02 only. [01b6d56e05d2] [620d53a81dad] [68855d5d9f02]

**R51. Commitment comes from clarity and buy-in, not consensus. When agreement does not emerge, the leader makes the call.** Source 02: "reasonable human beings do not need to get their way... They just need to be heard" [28c1fbbb868f] [6b7f86825119] [3c366caa7b8f]. Source 03: consensus is explicitly not 100% agreement; proceed on what is agreed and resolve the rest as work continues (Pitroda) [63cb980cc32a] [36ba5d087ea6] [788f0cb90b86]. 2 sources. The words differ but the rule is the same once "consensus" is defined.

**R52. A decision is better than no decision on ordinary calls; decide boldly and change boldly.** Source 02: delaying for more data "breeds paralysis" [6b7f86825119]. Applies to the everyday decisions that 01 says do not warrant debate (R82). Conflict C1 for high-stakes calls. Source 02 only for the wording.

**R53. Reduce fear of deciding with deadlines, a named worst case, and low-risk practice.** Source 02: set and honour deadlines for decisions (not only deliverables); state the worst case up front to show it is survivable; decide low-stakes items with real discussion but less analysis to recalibrate an over-studying team [f585db3667ae] [9580c914ef46] [f6a0ee547b86]. Source 03: before committing, list the unknowns, assess worst cases and the probability of overcoming them, research what can be researched (others' experience, a small pilot), and name the irreducible risk openly rather than hiding it [f1897dcf47ec]. 2 sources.

**R54. Spend the last 10 minutes of every staff meeting on cascading messaging.** Review the decisions made, agree what will be told to whom, mark what stays confidential, and treat any disagreement about what was decided as a cheap early catch. Source 02 only. [74974350d958]

**R55. Peer pressure is the primary accountability mechanism; the leader steps in only as a last resort.** Source 02: "as politically incorrect as it sounds", peer pressure beats bureaucracy; a leader who is the only source of discipline creates an accountability vacuum where the team stays silent [00e9c7d1cd6a] [e3909b2c8cdc] [acd8b1cd9f28]. Applies to a team of peers with mutual stakes. Conflict C4 for contractor rosters. Source 02 only.

**R56. Publish goals, owners and standards; run simple, regular progress reviews.** Source 02 [401b22a4cb2f] [14e6bb26ffbb]. Source 01's visible scoreboard (R32) and source 03's review mechanisms among the 10 team-building practices [36ba5d087ea6] agree. 3 sources.

**R57. Reject "revenue" as the scoreboard's own goal; use a 5 to 7 line set built from repeat rate, contribution margin, days of stock, ticket backlog and delivered-on-time, not the fable's software-company categories.** Source 02: argue the candidates out loud until 1 survives; reject renamed duplicates; the leader sets the final number after hearing everyone and says there is "no science here"; revenue or profit alone is not the scoreboard because it lags; monthly not quarterly because a quarter gives too few chances to correct; the owner must state target and result at every review [42e38198eea1] [f89975959127] [25f1e4a02461] [fcdcb7354b0c] [5e46d0e232dd]. Source 05: goals few and simple, or teams "get overwhelmed" [352063f0fa58] [712acd79637a]. 2 sources.

**R58. Each leader's first team is the leadership team, not their department.** A "my department comes first" answer is not automatically wrong, but watch for go-betweens, bad news kept local, and company commitments traded for departmental goodwill. Source 02 only. [a5a2bf1b017e] [ee63844c33b6]

**R59. The model assumes the team wants to win.** For a team that exists only to exist, no amount of trust, conflict, commitment or accountability compensates. Confirm the desire before running the results tools. Source 02 only. [3455fb9fc7e8]

**R60. Rewards lean toward collective results; 360 stays out of pay.** Source 02 [f865719ea5b4] [252c4066c43e] [30d9d9379f95] [59329495c17e]. Source 03: 360 without training becomes disguised criticism [60f28329351e]. 2 sources on 360. Human sets pay (R111).

**R61. Expect the guarded-regression relapse right after a peak season, when everyone reverts to firefighting.** Source 02: a typical first response after an offsite is guarded regression; real change takes months [bf4fc35fbd0f] [d9382f94958b]. Source 05: drift from agreed goals, roles and norms is "natural" and "almost inevitable" because people sit on several teams [d35411c91008]. Source 03: teams move through forming, storming, norming, performing, adjourning [98f70de504bd]. 3 sources.

**R62. Run the 3x3 loop: commit explicitly to goals, roles and norms; check in; close the saying-doing gap with 1 small step and an environment change.** Source 05: the commit conversation must be explicit, not assumed; at check-in ask "are we still committed, does our working style still hold, how do we share information and decide"; close with a small specific step, engineer the surroundings to support it, and apply "realistic optimism" (think ahead about what will block it) [d35411c91008] [0396231dd3a9] [352063f0fa58]. Source 05 only for the loop; 02's re-run assessment (R47) and 03's review mechanisms agree on repetition.

**R63. A written check-in cadence must exist; its length is the brand's call.** Source 05 refuses a fixed ratio of check-in to working time ("it depends" on appetite for process) and warns against converting it to a rule [d35411c91008] [ab649028be47]. Source 02 gives a fixed cadence (R64). Source 04 gives a forecast review cadence of weekly, fortnightly or monthly [87a5258c4926]. Strictest condition kept: the cadence is written and owned; the interval is chosen with the human and recorded. Conflict C6.

**R64. Source 02's meeting cadence, as an example: annual 3-day off-site, quarterly 2-day off-site, weekly 2-hour on-site staff meeting, ad hoc 2-hour topical meetings; about 8 days per quarter, under 3 days a month.** 1 fictional company's model. Keep the 4 meeting types; compressing lengths for a small brand (half-day quarterly, 30 to 45 minute weekly) is `[pass 1 adaptation]`. Source 02 only. [e7f4cb5fa94f]

**R65. Meeting ground rules: be present and participate, no laptops; if there is nothing worth debating, do not hold the meeting; run staff reviews as debates on the jugular issues, not report-outs.** Source 02 [49328275a84b] [95958a74d490]. Source 01: Bill Campbell pre-circulated 5 crucial topics and opened with "take off your functional hat" [1599a2d6489d]. 2 sources.

**R66. Observe first, change second.** Source 02's new CEO spent 2 weeks in silent one-on-ones and meetings before changing anything. Source 02 only. [c1ebfcd84f31]

**R67. Handle moments of truth face to face, not by email.** Source 02 [f5195fd1f7a6]. Source 03: resolve a recurring interpersonal conflict by process consultation (define the problem with the person, develop options together, the person owns the recommendation) rather than a verdict [0b4cac182293]. 2 sources.

**R68. Personality instruments are self-disclosure tools, not assessments; MBTI's standing is contested.** `[web check: current I-O psychology critique of MBTI reliability and validity, and licensing cost]` Source 03 says choose a conflict mode deliberately [059d6a41d014]. 2 sources on conflict-mode awareness. Do not recommend MBTI to a client as a serious diagnostic without the web check. MBTI and Thomas-Kilmann instrument description moved to Appendix A.

**R69. Experiential and ropes-course exercises are not a standalone fix.** Source 02: they have "lost some of their luster... and deservedly so", and outdoor benefits "do not always translate" to work; use only on top of the fundamental tools [f0b5fc985510]. Source 03 lists outward-bound training and sensitivity training among workshop formats without judgement [e1daf5ed03eb]. Conflict C3.

**R70. Judge a launch team by whether the drop shipped on time and sold through, not by the meeting's atmosphere alone.** Source 03's 12: relaxed informal atmosphere; task understood and accepted; high listening; open expression; conflict on ideas not personalities; the group aware of its own process; consensus decisions with clear follow-up; clear purpose; frank interaction; participation at all levels; shared leadership; diversity of styles [1154b29c520f] [0a2959ee32d4]. Source 03 only.

**R71. When a team performs badly, check 3 categories and 2 layers before acting.** Categories: communication (listening, information sharing, interpretation, nonverbal), structural (size, turnover, participation, rewards, interdependence), personal (self-esteem, goals, values). Layers: internal process, and the external system (design, culture, selection, training, rewards) that existed before the team formed. Failure signs: resentment over resources, cost overruns, slipped schedules, members unclear on responsibilities, essential members losing focus. Source 03 only. [b5da25e5c81d] [aee0bbdc19b9]

**R72. Set communication norms by work type, and cut reporting sludge in distributed teams.** Source 03's matrix: routine vs emerging work, autonomous vs interdependent; the leader's role shifts by quadrant (Defender, Manager, Lookout, Facilitator); technology makes over-reporting easy and people disengage from what matters. Source 03 only. [795d8f346c0e] [2e0b75591c56]

**R73. Free a dominated meeting.** Source 03: the leader steps out so the group can work [0bf329725971]. Source 01: poker chips for the dominant talker; hold silence so a quiet member fills it (Lokesh went from near zero to "50 percent or more" of a conversation) [d4d1178321c5] [adf7a15b25a4]. 2 sources.

**R120. Build the scoreboard from ecom categories, not a software-company list: repeat rate, contribution margin, blended CAC, days of stock, ticket backlog and delivered-on-time.** The pass 1 mini playbook for source 02 sets out these categories; they were not carried into R57 or P9 before this pass. Source 02 mini playbook, `sources/02-the-five-dysfunctions-of-a-team.md`, line 281. [25f1e4a02461] `[pass 1 adaptation]` Feeds R57 and P9.

### 3.5 Roles and responsibility tools

**R74. Map Belbin roles to merchandising, creative, growth and ops when staffing a seasonal launch team; flag a team stacked with only Implementers.** Source 03 only [eeae888bdd37] [75f75373e390] [e9522d20d039] [158432c03eb2] [402ac024a0bf] [cc0dedea96db]. `[web check: the standard name is Completer Finisher; source shortens it]` Generic Belbin taxonomy (9 roles, the 3 essential, task-stage matching) moved to Appendix A.

**R75. Staff both task roles and process roles; the leader does not hold every role because they are busy.** Source 03 only. [6dc36d7f5601]

**R76.** Moved to Appendix A: the Role Analysis Technique write-up (source 03). [ae9c30902c6c]

**R77. Write the 1-R chart for price changes, promotions, site changes, PO releases, 3PL escalations, refund exceptions and hire requests.** Responsibility charting: decisions down the side, actors across the top, each cell R (initiates and ensures it is done), A-V (approve or veto), S (support), I (inform, cannot influence). Source 03 [f684ff28794c]. Source 01: 1 owner with 51% of the vote [d150234124c0]. Source 02: 1 named owner per scoreboard category and per goal driver [25f1e4a02461] [78f85b7bed71]. Source 05: the roles conversation [12ad1d771f2c]. 4 sources on 1 named owner.

**R78.** Moved to Appendix A: the role negotiation write-up (source 03). [10b3930ea6dc]

**R79.** Moved to Appendix A: the force field analysis write-up (source 03). [6572b0c296da]

**R80.** Moved to Appendix A: choose a conflict mode on purpose, detail (source 03, source 02's TKI). [059d6a41d014] [dd193a22adc1]

### 3.6 Decisions and debate

**R81. For a store, high-stakes examples are a pricing or offer change, a platform migration, a 3PL switch, a repositioning, or a large PO; everything else is an everyday call.** Source 01's own FAQ [7a618f532beb]. Source 05: go fast and skip process when speed matters; slow down when the decision needs several perspectives [ab649028be47]. Source 02: low-risk exposure therapy for over-studying teams [f6a0ee547b86]. 3 sources agree on the split; conflict C1 on where the line sits.

**R82. Frame before debating: the exact question, the right people (knowledge, stake, execution), data in advance, and who decides, said up front.** Source 01: Tim Cook expects data-backed positions; Jim Barksdale's "we'll just use my opinion" is the anti-pattern. Source 01 only. [112a27eb807d] [786432b573e1]

**R83. Run the debate with safety and rigour at once.** Safety: the leader's view last, someone argues the other side, facts over hierarchy. Rigour: evidence for both sides, keep asking why, do not let the group settle early. Source 01 [a6d1d161e875] [ffc3fd5842db]. Shared inquiry rules: the leader only asks, claims need evidence, everyone participates [786432b573e1]. Source 02's miner of conflict and real-time permission (R50) are the same job. 2 sources.

**R84. Close the debate explicitly: decided now or more data; team call or leader's call; communicate the decision and the reasoning; make the debate visible where you can.** Source 01: announcing a decision after collecting opinions without debating them leaves people "debating the soundness of the decision instead of executing it" (Jonathan Akers); Lutz Ziob's "Theater" doubled the chairs so anyone could watch [7a618f532beb] [8b7d0cbcfc56] [963a88a25024]. Source 02's cascading messaging (R54) is the same close. 2 sources.

**R85. Run a full-input debate before high-stakes inventory and forecasting decisions.** Source 01's Lands' End example: bringing IT and senior planners into the room up front replaced rushed "Band-Aid" forecasting fixes with a new in-season method. Source 01 only. Feeds R91. [abd37c037189]

### 3.7 Operating process ownership (from 04; mechanics routed, see section 1)

**R86. Every operating artefact has 1 named owner and a fixed update cadence; "I'll update it later" is the top failure.** Source 04: a shared manual sheet works only with a disciplined, dedicated owner; stale data propagates into other teams' decisions [5eb084517f52]. Source 02: an owner who must state target and result at every review [25f1e4a02461]. Source 04: 1 owner per critical path step [2f17c3eca340]. 2 sources.

**R87. No large purchase order without a tech pack on file.** The tech pack is the evidence base for any quality or IP dispute (Oodie weighed a fabric square against the GSM spec, proved substitution, got replacements). If the team cannot write one, commission a freelancer with a defined deliverable; the source's "shouldn't cost more than 200 bucks" is anecdotal `[web check: current tech pack freelance pricing]`. Contents list and supplier route: 18-COG. Source 04 only. [24613aeb6cad] [9268b8dd340f]

**R88. The PO owner chooses 1 lever per SKU: low MOQ (small budget), low price (margin) or short lead time (cash turns); a supplier rarely gives all 3.** Compare at least 2 factories and check landed cost against the intended retail price before committing. Negotiation detail and the landed cost formula: 18-COG and 20-FIN. Source 04 only. [48773124dba7]

**R89. Run a critical path with 1 owner and 1 date per step, worked back from the hard deadline, and never give suppliers edit access.** Steps: strike-offs, first sample, revised sample, production sample, QC, bulk, freight, inbound. Book a QC agent for at least the first run, ideally the first 3. Example durations: a DHL sample from China about 5 days. Tool is the team's choice (Monday.com, Asana, Notion, Excel named) `[verify UI]`. Source 04 only. [2f17c3eca340]

**R90. Forecast from in-stock days only, pad lead time with the average, then set days of stock and safety stock.** Exclude stockout days from the base (if 15 of 30 days were in stock, extrapolate from 15); under about a year of history or fast growth, use month-on-month trend; if seasonality dominates (source says 90 to 95% of ecommerce has it), build a month-by-month curve and check product seasonality on Google Trends; enter manufacturing lead time (not shipping) padded with an average, not best case; target 4, 8 or 12 weeks of stock by volatility and capital; add 5 to 10 days of safety stock only after lead time is padded; read the sell-out date and replenishment quantity; review weekly, fortnightly or monthly with 1 owner. Source 04 only. [69512d4531fe] [87a5258c4926] [48e4499ac999]

**R91. Both under-ordering and over-ordering are existential; every added colour or size multiplies forecast risk and capital.** Source 04: zero stock is zero revenue against fixed costs; over-ordering locks profit and cash in inventory and cuts off marketing and tax. Source 04 only. [48e4499ac999]

**R92. The PO is a cross-functional document: 1 authoritative copy in accounting software, 1 team-visible tracker, ETA changes pushed to the team, and a check before any discontinuation or mass refund.** Finance, ops, marketing and CS all read the same PO data. Add departure date, ETA, vessel, bill of lading (or air tracking) as they arrive. Internal only; supplier changes come through 1 channel. Source 04 only. [e50d8f082b51] [e252e690a92c]

**R93. Freight: compare 2 to 3 providers, re-shop monthly, prefer providers in your own region.** Detail: 18-COG. Source 04 only. [0bfbfacfd9fe]

**R94. Choose a 3PL by competitive RFP with a facility visit; never on 1 quote; never on price alone.** Send the identical RFP (dimensions, history, and above all the growth forecast) to several 3PLs; visit or see interior footage (refusal is a red flag); confirm barcode scanning inbound and outbound; judge whether you will be a valued account; price pick and pack, inbound, outbound and storage separately; give forecasts you intend to hit. Source 04: a 3PL that "completely couldn't ship any orders" in an October to November peak forecast at $45M to $50M cost over $20M in lost revenue (self-reported). Source 04 only. [875b2b81d78d] [25bacdb89696]

**R95. Put the 3PL SLA in writing: pick time 24 to 48 hours off-peak, a stated consequence for a missed pick (discount or free pick), delivered-on-time language, at least 2 cycle counts a year, and ASN and booking rules.** Source 04 only. [30a460679b7f] [875b2b81d78d]

**R96. Audit every monthly 3PL invoice against your own order volume.** Rebuild expected pick and pack, inbound, outbound and storage from Shopify order counts and compare; source claims 30 to 40% of one mentorship client sample were overcharged somewhere (unverified). Source 04 only. [9b59cf172fa6] `[needs brand data: monthly 3PL invoice and order count]`

**R97. Track delivered-on-time yourself; below about 95%, find whether pick time or the carrier is the cause before asking for a refund.** 3PLs will not put delivered-on-time in the SLA. Show the metric as unavailable, never 0, when the data is missing (R113). Source 04 only. [30a460679b7f]

**R98. Customer service staffing: split tiers by ticket complexity, define "complex" in advance, plan agents from the sales forecast, and track cost per ticket.** Source 04: route simple repeatable tickets to offshore agents (Philippines, Fiji named) and nuanced or escalated ones to local agents near the source of truth; do not assume offshore is cheaper, since local agents can be about twice as efficient without training and macros; onboard extra agents before a peak using the sales curve, not current ticket volume; cost per ticket = (software plus agents) / tickets, and a rising figure means headcount or routing lags the forecast [d55c91623549] [3f6fb0e7eecd] [08a8a291428f]. Source 06: pre-purchase CS exists to clear confusion so people finish checkout ("a confused mind always says no") [6168b9f862f4]. Helpdesk tools and macros: 17-CXP. 2 sources.

**R99. Reviews and resolution time are lagging outputs of the rest of operations; trace upstream before blaming support.** Diagnose in order: missing internal information, slow agents or systems, weak macros; then PO accuracy, freight, 3PL pick time. Source 04 only. [08a8a291428f]

**R100. Tooling by stage: spreadsheet plus accounting software until about $30M to $50M, then consider an ERP that absorbs about 90% of coordination; a dedicated tracker owner from about $5M to $10M.** ERP implementations the source quotes at "over $200 grand" and its own "upwards of half a million dollars". Source 04 only, single operator. [b835681136c8] [5eb084517f52] [e252e690a92c]

**R101. Judge every operations change by the customer-facing output, cost and process load together, not by an internal metric alone.** Source 04 only. [0ff782611bef]

**R121. Decide make-vs-buy for fulfilment (an in-house warehouse vs staying with a 3PL) before running the 3PL RFP (P28).** Source 04 only covers 3PL selection once outsourcing is already the decision; no source here compares in-house fulfilment against a 3PL. `[general practice]` No library source; verify against brand data before use.

### 3.8 Bottleneck diagnosis

**R102. Diagnose the constraint before buying a fix; split "growth is limited" into "are people reaching the site" and "are they converting once there".** Source 07 [c1dfbfcedccd] [5013501dc466]. Source 07 only.

**R103. Segment conversion by source, campaign and geo before running CRO. Uniformly low means a site problem; a few sources dragging the average means a traffic match problem.** Source 07: "the easiest way to improve your conversion is just get better people" applies only when segmentation shows it; do not apply it as a default over CRO [5013501dc466]. Source 06: the site is a leaky bucket and the developer role exists to seal leaks from landing to checkout [4ccb3499516c]. Strictest condition kept: segment first, then act on the side the data shows. Conflict C5. Mechanics: 09-CRO, 06-MEA.

**R104. Locate the founder's proven strength and build the team around it, not around an assumed skill.** Confirm the strong side with evidence (the memorabilia founder buys at about $200 and sells at about $2,000); treat the hedged side as the gap. Source 07 only, 1 case. [5813209a4dbd] [12805cde65c1] [990f21a57b6e]

**R105. A sourcing edge substitutes for brand only short-term; it erodes as competitors find the supply.** Source 07 only. [990f21a57b6e]

**R106. For a first-mover product, fix acquisition and revenue first, brand next; not a universal order.** Source 07 says a more differentiated business may justify earlier brand work. Source 07 only. [59f0f71e9914]

**R107. Model cash separately from the revenue target before any growth push; ecommerce scales fast and the cash strain arrives right after.** Source 07 [22f9b83f5cae]. Source 04: over-ordering locks cash [48e4499ac999]. Detail: 20-FIN. 2 sources.

**R108. Recurring pre-purchase questions are a page fix, not a "answer faster" fix.** Source 06 only. [6168b9f862f4] [4ccb3499516c]

### 3.9 ecomOS rules that override any source

**R109. No invented claims.** Every number an agent quotes from this playbook carries its source and its confidence (section 6). The 30 to 40% figures in 04, the "3 to 6 in 60 days" in 07, the 2x effect in 01 and the fable numbers in 02 are examples, never promises.

**R110. Brand and warehouse data beat source figures.** Where the brand's own conversion, ticket volume, days of stock, pick time or 3PL invoice exists, it replaces any threshold in section 6.

**R111. Hiring, firing and pay decisions stay with a human.** The agent prepares the role scorecard, the trigger, the comp options and the evidence for a removal; it never sends an offer, a termination or a pay change.

**R112. Credentials never go in files.** 3PL portals, helpdesk logins, Alibaba accounts and forecasting tools are accessed through `.env` and `secrets/`; none appear in a playbook, deliverable or tracker.

**R113. Missing metrics show as unavailable, never 0.** Delivered-on-time, cost per ticket, days of stock and utilisation estimates are blank when the data is missing.

## 4. Procedures (implementation)

Each procedure: goal, preconditions, steps, checks, rollback. The agent can run every step that reads data or drafts a document; every step that changes a person's job, pay or employment is a recommendation to the human.

### 4.1 Org design and hiring

**P1. Org chart vs stage review.** Goal: confirm every silo and every operating artefact has 1 owner, and find the next hire trigger. Preconditions: roster, revenue and order volume by month, artefact list. Steps:
1. List the 5 silos (R1) and write the owner of each. Founder-covered is allowed; blank is a blocker.
2. List the operating artefacts (tech pack, critical path, PO tracker, forecast sheet, 3PL SLA, CS routing rules, scoreboard) and their owner and update cadence (R86).
3. Mark revenue stage against the only stage triggers the sources give: below about $1M founder holds all ops roles (04); about $5M to $10M a dedicated tracker owner (04); about $30M to $50M consider an ERP (04); top team no longer able to debate, regroup functions (02, illustrative at more than 250 staff and 8 reports). All single-source.
4. For each artefact with a stale update (past its cadence) or an owner who also owns 3 or more other artefacts, note "capacity risk".
5. Run P21 (capability gap check) before proposing a hire (R4).
6. Output the org plan by stage (section 9).
Checks: no silo blank; every artefact has an owner and a last-updated date. Rollback: none, read-only.

**P2. Decide the next hire.** Goal: a written hire trigger and role definition. Preconditions: P1 done, growth target, budget constraint. Steps:
1. Ask the founder which core function they own and note hedging (R6, R104).
2. If a plateau, run P31 first; the constraint decides the role (media, product, ops, CS, dev).
3. Define the role around the missing function (R5); write what "good" looks like as behaviours and results (R15).
4. Write the trigger in brand numbers (orders per week, tickets per week, revenue) at or below the point the current owner cannot keep the artefact current (R3).
5. List comp options for the human: cash within margin, performance pay, equity if margin is thin (R21, 07); note equity is given up, not free.
6. Consider an assignment change for an existing person before a new head (R23), and a contractor for a discrete task below $1M (R2).
7. Hand to the human with the hiring plan (section 9). Human decides.
Checks: the role names 1 function; the trigger is a number; the comp list has at least 2 options. Rollback: none.

**P3. Run a hire.** Goal: a candidate the team has vetted against the bar. Preconditions: P2 approved by the human. Steps:
1. Name 1 search owner (02).
2. Write an honest, demanding ad that states the hard parts (01, Shackleton).
3. Screen fast: short first conversations across the shortlist (01's Hexal example: 3 minutes each for 8 people; use as an example, not a rule).
4. Deep finalist round: 3 hours (01 example) with the whole team involved (02).
5. Ask only sourced questions (R18): next challenge, what gets in the way, the native genius probe 3 ways, "how have you broken through a previous goal", which core function they own.
6. Score against the behaviour bar (R15): trust, conflict on ideas, commit, hold peers accountable, results over ego, drive, fit with objectives and ethics.
7. If internal vs external is open, run the open debate, invite last input, the leader decides and states the criterion (R17).
8. Recommend to the human. Trial tasks and rubrics: `[not sourced: human designs]`.
Checks: every interviewer used the same questions; the team's input is recorded before the decision. Rollback: no offer without the deep round.

**P4. Onboard a new member through the team.** Goal: the newcomer sees the operating model in use on day 1. Preconditions: hire made, team has a goal and roles written. Steps (02):
1. Assign each existing member 1 part of the operating model (trust, conflict, commitment, accountability, results; or goals, roles, norms) to teach.
2. Walk through every peer's role and the current overarching goal and scoreboard.
3. Compare the newcomer's working style with the team's and say how peers tend to disagree.
4. Put them in a live debate the same day.
5. Let them watch peers hold each other accountable; steer tension back to results.
6. Expect a short storming period (03) and do not read it as failure `[pass 1 adaptation]`.
Checks: after week 1 the newcomer can name the overarching goal, each peer's role and who decides what. Rollback: none.

### 4.2 Team health

**P5. Run the five dysfunctions team assessment.** Goal: find the lowest broken layer. Preconditions: a team of peers around 1 leader, all willing to answer honestly. Steps (02):
1. Each member scores the 15 statements below 3 Usually, 2 Sometimes, 1 Rarely, without overthinking.
2. Total per dysfunction: Trust = 4 + 6 + 12; Conflict = 1 + 7 + 10; Commitment = 3 + 8 + 13; Accountability = 2 + 11 + 14; Results = 5 + 9 + 15. Max 9 each.
3. Read bands: 8 to 9 probably not a problem; 6 to 7 could be; 3 to 5 probably needs addressing. Rough only, not validated.
4. Compare spread between members; a wide spread on the same dysfunction is itself a trust or communication signal.
5. Discuss as a team and agree 1 behaviour change for the next quarter.
6. Start remediation at the lowest broken layer (R45).
7. Re-run each quarter, or after any senior change.
The 15 statements: (1) discussion is passionate and unguarded; (2) members call out each other's deficiencies or unproductive behaviour; (3) members know what peers work on and how it helps the team; (4) members apologise quickly and genuinely; (5) members sacrifice budget, turf or headcount for the team; (6) members admit weaknesses and mistakes; (7) meetings are compelling, not boring; (8) members leave meetings confident peers are committed even after disagreement; (9) morale is hit by missing team goals; (10) the most important and difficult issues are put on the table; (11) members are concerned about letting peers down; (12) members know about each other's personal lives and discuss them comfortably; (13) discussions end with clear resolutions and calls to action; (14) members challenge each other's plans and approaches; (15) members are slow to seek credit and quick to give it. [9df78b1b4685]
Checks: every member answered; totals computed in code, not by eye. Rollback: none; results are development data, not pay data (R60).

P6, P7 and P8 (personal histories exercise, team effectiveness exercise, strengths and weaknesses round) moved to Appendix A: generic HR trust-building scripts with no store tie. Run P5 and P9 for the store's own team health and scoreboard work; use P6 to P8 only if the human wants a deeper trust exercise.

**P9. Set the scoreboard and the 1 overarching goal.** Goal: 5 to 7 owned categories and 1 quantified goal with a deadline. Preconditions: leadership team in a room; revenue and cost data on hand. Steps (02):
1. Small groups propose result categories, not yet quantified.
2. Merge and cut to 5 to 7 that are simple and daily-actionable (the fable's example: revenue, expenses, new customers, customer satisfaction, employee retention, market awareness, product quality). Revenue alone is rejected as lagging.
3. Assign 1 named owner per category who states target and result at every review.
4. Set the review to monthly, not quarterly.
5. Separately list every plausible overarching goal for the period and argue each against the others until 1 remains; reject renamed duplicates by asking whether the measure is actually different.
6. The leader sets the final number and deadline after hearing everyone, says full agreement is not expected, and tells whoever was overruled exactly why.
7. Only then map what each function must do to make the number possible.
8. Record it where everyone, including contractors, can see it (R56).
[25f1e4a02461] [42e38198eea1] [f89975959127] [fcdcb7354b0c] Checks: 1 goal, 1 number, 1 date, 1 owner per category. `[needs brand data: which metric is the brand's north star this period]` Rollback: re-run at the next quarterly session if the goal proves wrong; do not add a second goal.

**P10. Weekly accountability review.** Goal: the agreed goal, not status updates, is the agenda. Preconditions: P9 done. Steps (02):
1. Open on the overarching goal.
2. Decompose it into a short list of named drivers (the fable's: product demos, competitive analysis, sales training, brochures).
3. Each driver has 1 owner and 1 date; the owner reports ahead or behind without spin.
4. When an owner blames someone else's slowness, ask them to name the blocker and treat their failure to escalate earlier as the issue.
5. Name out loud why a given person is hard to hold accountable (too helpful, too defensive, too intimidating).
6. Push with respect, and push anyway; hold the same standard for the leader.
7. Close each driver with a decision or a reassignment; next meeting starts from the same list.
8. Last 10 minutes: cascading messaging (P11).
[78f85b7bed71] [1255f54db7d3] Checks: every driver closed with a decision or reassignment; ground rules kept (be present, no laptops). Rollback: if nothing is worth debating, cancel the meeting (R65).

**P11. Cascading messaging.** Goal: 1 consistent message leaves the room. Preconditions: any staff meeting or offsite, last 10 minutes. Steps (02): review the decisions made; agree exactly what goes to employees, clients or vendors about each; mark what stays confidential and what goes out fast and in full; treat any disagreement about what was decided as a cheap catch. For contractor calls, send the same recap in writing after the call `[pass 1 adaptation]`. [74974350d958] Checks: the recap exists before anyone leaves. Rollback: none.

**P12. The 3x3 loop (commit, check in, close).** Goal: goals, roles and norms explicit and re-checked. Preconditions: any team, any size. Steps (05):
1. Commit: 1 dedicated conversation on goals (what), roles (who does what) and norms (how we share information and decide). Keep all 3 few and simple.
2. Check in on a written cadence (R63): are we still committed; does our working style still hold; how do we decide now.
3. Close: name the gap between what was said and what is done; pick 1 small specific change; alter the surroundings to support it (a template, a meeting slot, a visible board); apply realistic optimism (what will block this).
4. Return to step 2.
For check-in conversations: name style differences (introvert and extrovert, comfort with conflict); build trust one-on-one; cap the agenda to a few topics. [d35411c91008] [0396231dd3a9] [352063f0fa58] [712acd79637a] Checks: a goals, roles, norms document exists `[needs brand data: the brand's own format; the source gives none]`. Rollback: none.

**P13.** Moved to Appendix A: the Role Analysis Technique procedure (source 03). [ae9c30902c6c]

**P14. Responsibility charting.** Goal: every recurring decision has exactly 1 R. Steps (03): list decision types down the left (price change, promotion, site change, PO release, 3PL escalation, refund policy exception, hire request); list actors across the top; fill each cell R, A-V, S or I; any row with 0 or 2 R values is fixed in the meeting. [f684ff28794c] Checks: 1 R per row; the chart is published (R56). Rollback: none.

**P15.** Moved to Appendix A: the role negotiation procedure (source 03). [10b3930ea6dc]

**P16.** Moved to Appendix A: the force field analysis procedure (source 03). [6572b0c296da]

**P17.** Moved to Appendix A: the process consultation procedure (source 03). [0b4cac182293]

### 4.3 Leadership practice

**P18. Debate Maker process for a high-stakes decision.** Goal: a decision the organisation executes instead of relitigating. Preconditions: the decision passes the debate-worthiness check (R81): high stakes or hard to reverse (a pricing or offer change, a platform migration, a 3PL switch, a major repositioning, a large PO). Steps (01):
1. Frame: write the exact question; invite people with knowledge, stake and execution duty; require data in advance; state up front what is being decided, why now, and who decides.
2. Spark: leader speaks last; assign someone to argue the other side; ask for evidence on both sides; keep asking why; ignore rank when weighing input; do not let the group settle fast.
3. Drive: state whether it is decided now or needs more data; team call or leader's call; make the call or delegate it explicitly; communicate the decision and the reasoning; where possible let others watch.
4. End with cascading messaging (P11).
[112a27eb807d] [a6d1d161e875] [7a618f532beb] [963a88a25024] Checks: the "who decides" line was said before the debate started. Rollback: if the decision was announced without debate, expect execution drag; reopen once with the data, then close.

**P19. Investor delegation (give 51%, hand back the pen).** Goal: 1 owner with real ownership of a whole outcome. Steps (01):
1. Name the owner and say the split: 51% of the vote, 100% of the responsibility; you stay in the loop.
2. Give the whole outcome (the email programme, the ad copy queue, the reorder review), not a slice; stretch the role 1 level above current comfort.
3. Coach with questions, not answers; add a second person as sounding board without moving accountability.
4. When a problem returns, ask "what would you like to do to fix this?"; never accept an AWK without a FIX.
5. If you must grab the pen (a stuck late-night storyline), hand it back before the work is done.
6. Let natural consequences run; do not rescue.
7. Put the owner's numbers on a visible scoreboard.
[d150234124c0] [bc22e9ec9c05] [cb138faa8112] [38f23ceae927] [f78fe4052829] [10e31326d248] [4c69b917bb9f] [9c377403f19f] [f09a30ff919d] Checks: after 2 weeks, who is doing most of the thinking on this work; if the leader, it was taken back. Rollback: reset the split out loud; do not quietly resume control.

**P20. 30-day one-practice challenge.** Goal: 1 new leadership habit. Steps (01): rate yourself on the 5 disciplines (formal 360 or informal); pick the single weakest and single strongest (R36); choose exactly 1 practice inside 1 discipline (examples the book gives: label each person's genius in a staff meeting; hold silence for a quiet member; make a high performer owner of an open-ended role; bring planners and IT into the forecasting debate; give a remote person a board-facing deliverable); run it 30 days; journal; at day 30 judge by others' behaviour, not your effort; then add the next layer and hold 1 question for the year with a peer partner. [887d2303442c] [7edcea17b5cb] [adf7a15b25a4] [b01e4fd98eff] [abd37c037189] [de26d8c0e741] [20942ff19843] [64aaf10b52e5] Checks: the journal has entries for at least 20 of 30 days. Rollback: pick a smaller practice, not a second one.

**P21. Capability gap and accidental diminisher check.** Goal: find out whether the team is underused before hiring. Steps (01):
1. Privately ask each key person to name a past manager and estimate what percent of their capability that manager got, then the same for their current manager. 40 to 60% or lower is an underuse signal (self-reported, retrospective).
2. Assumption audit: before a delegation, write how you would handle it under "they will never figure it out" and under "they are smart and will figure it out"; note which you did.
3. Tense vs intense check after the next hard meeting (R29).
4. Ownership check: are returned problems solved by you or returned with a question.
5. Accidental Diminisher quiz on multipliersbook.com `[web check: still live]`.
6. If gaps show, run P20 before P2.
[249b9719a074] [4fa842955f55] [6444ffb70c8e] [10e31326d248] [25c379ab794f] Checks: answers are private and never used for pay (R60). Rollback: none.

### 4.4 Removal and succession

**P22. Handle a destructive team member: confront, then exit if needed.** Goal: a real choice offered, then a clean decision by the human. Preconditions: specific observed behaviour written down (eye-rolling, disrespect to a peer, skipping a stated priority); the cost of tolerance estimated (R44). Steps (02, 01):
1. Private conversation; go to the core issue first, not small complaints.
2. Cite the specific behaviours.
3. Expect denial, blame, escalation threats; repeat the specifics calmly.
4. Offer a real choice: the behaviour change must be complete and fast; say honestly you doubt they want to.
5. Volunteer no concessions in the room; let them name terms first.
6. If departure: written agreement with HR on severance, vesting and the official characterisation.
7. Attribute the damage to your own tolerance, not only the person.
[35ddf3a597fa] [f9f956b15e91] [770627149af5] [3c9e69b660b3] Checks: the human made the decision; nothing in the file names pay or legal terms beyond what HR wrote. Rollback: if the behaviour changes fully and fast, keep the person and say so.

**P23. Communicate after a senior departure.** Steps (02): tell the leadership team first and say some detail stays confidential; give the plain reason (unwilling to change behaviour that hurt the team); answer the practical questions (how they took it, interim plan, what employees and press hear); name the interim plan and state confidence; 1 simple line outside ("moving on"); then deliberately open the conversation about how the team feels, expect mourning and self-doubt even after a deserved exit, and let concerns surface before responding. [eb9ccdf68487] [031f14e62d4b] Checks: the interim owner of the function is named the same day. Rollback: none.

**P24. Review leadership span.** Steps (02): watch for staff meetings that no longer allow substantive discussion; list decisions stalling on unclear ownership or too many attendees; regroup functions under a layer (ops under a COO, HR under a CFO in the fable); tell each affected person individually with the reasoning before publishing; address "am I being demoted" directly; judge by faster decisions and handoffs. [0fde892e7e47] Checks: fewer direct reports and a named owner per regrouped function. Rollback: revert if handoffs slow.

### 4.5 Operating process ownership

**P25. Critical path from sample to bulk.** Goal: no missed seasonal window. Preconditions: tech pack on file (R87); hard deadline known (Christmas cut-off, launch date). Steps (04): list every step (strike-offs, first sample, revised sample, production sample, QC, bulk, freight, inbound); sequence in the team's tool `[verify UI]`; assign a duration per step (DHL sample from China about 5 days); set dates back from the deadline; 1 owner per step; monitor daily with overdue reminders; when a step slips, push downstream dates or use slack; no supplier edit access; QC agent booked for the first run, ideally the first 3. [2f17c3eca340] Checks: every step has owner and date; the supplier is not an editor. Rollback: if the path cannot reach the deadline, decide early to skip the window rather than land stock in January.

**P26. Forecast and reorder review.** Goal: a replenishment decision on a clean base with 1 owner. Preconditions: sales by day with stockout days flagged; supplier lead time; days of stock policy set with the human. Steps (04):
1. Base period: in-stock days only.
2. Under a year of history or fast growth: month-on-month trend (100, 120, 145, 175 suggests about 20% growth).
3. Seasonal category: month-by-month curve (example: Jul 200, Aug 210, Sep 205, Oct 2,000, Nov 4,000, then a drop after the shipping cut-off); check Google Trends; hemispheres reversed.
4. Enter manufacturing lead time padded with the average (example 100 days).
5. Set days of stock: 4, 8 or 12 weeks by volatility and capital `[needs brand data: cash available for stock]`.
6. Add 5 to 10 days safety stock only after step 4.
7. Read sell-out date and recommended quantity; raise the PO (P27).
8. Cadence weekly, fortnightly or monthly; owner is the ops manager.
9. For a large or unusual order, run P18 first (R85).
[69512d4531fe] [87a5258c4926] [48e4499ac999] [abd37c037189] Checks: the base period excludes stockout days; the tool's lead time is the padded figure. Rollback: if the forecast missed by about 50% (the source's growing-brand figure), re-check the base period before changing the growth assumption. Tool named by the source: Inventory Planner (affiliate) `[web check: current features and pricing]`.

**P27. PO tracker across departments.** Steps (04): raise a formal PO (product, price, quantities, ship-to, terms); keep the authoritative copy in accounting software (Xero, MYOB named) `[verify UI]`; keep a team-visible tracker (Sheets or Airtable) with SKU, quantity, PO number, departure date, ETA, vessel, bill of lading or air tracking; push every ETA change to the team channel; internal only; check the tracker before discontinuing a product or issuing mass refunds; from about $5M to $10M assign a dedicated owner; from about $30M to $50M consider an ERP. [e50d8f082b51] [e252e690a92c] [5eb084517f52] [b835681136c8] Checks: last-updated date within the cadence; estimated and actual dates both logged. Rollback: none.

**P28. 3PL RFP and SLA.** Goal: a 3PL chosen on comparable quotes with a written SLA. Preconditions: growth forecast the brand intends to hit; product dimensions; order history. Steps (04):
1. Master RFP: dimensions, history, growth forecast.
2. Send the identical document to several 3PLs (the source keeps its own list of about 10, an affiliate list).
3. Facility visit or interior footage; refusal is a red flag (the source's example: a 3PL moving stock in stolen supermarket trolleys).
4. Confirm barcode scanning inbound and outbound.
5. Judge account value: smallest or largest customer on their book affects service; watch sales behaviour during the RFP.
6. Price 4 components separately: pick and pack, inbound, outbound (each 3PL holds its own carrier account, so this varies most), storage.
7. Write the SLA: pick 24 to 48 hours off-peak, consequence for a missed pick (discount or free pick), delivered-on-time expectations, at least 2 cycle counts a year, ASN and booking rules.
8. Give honest forecasts; do not pick the cheapest by default.
9. Store the SLA and the RFP responses in the brand record; credentials stay out (R112).
[875b2b81d78d] [25bacdb89696] [30a460679b7f] Checks: every quote priced on the same 4 components; SLA signed before the first inbound. Rollback: keep a second qualified 3PL from the RFP on file in case of failure (the source's own $20M loss story is the reason).

**P29. 3PL invoice audit.** Steps (04): each month, pull Shopify order count, units, inbound receipts and pallets stored; compute expected pick and pack, inbound, outbound and storage from the SLA rates in code; compare to the invoice line by line; flag any line above expected; pull delivered-on-time and pick time; if delivered-on-time is under about 95%, separate pick lag from carrier lag before asking for a credit. [9b59cf172fa6] [30a460679b7f] Checks: arithmetic in code; missing data shown as unavailable (R113). Rollback: none. `[needs brand data: SLA rate card, monthly invoice, order count]`

**P30. Customer service capacity plan.** Steps (04): define "complex" ticket in writing; route simple repeatable tickets to the offshore tier and complex or escalated ones to the local tier (or either for a small brand); build training and macros before judging offshore cost; plan hiring and training dates from the sales forecast curve so agents are productive before the peak; use the offshore tier to ramp up and down around peak; compute cost per ticket monthly; if it rises while tickets rise, headcount or routing lags. Reviews and resolution time are read as upstream signals (R99). [d55c91623549] [3f6fb0e7eecd] [08a8a291428f] Checks: the "complex" definition exists; cost per ticket computed in code. Rollback: none. Tool choice: 17-CXP.

### 4.6 Bottleneck diagnosis and commitment

**P31. Bottleneck diagnosis.** Goal: name the constraint before a hire or a CRO project. Preconditions: conversion by source, campaign, geo; founder's self-assessment. Steps (07, 06, 01):
1. Ask what limits growth; split the answer into traffic reaching the site and conversion on site.
2. Pull conversion by source, campaign and geo; do not read the blended number.
3. If a few sources or geos convert near 0 while others are normal: traffic match problem; fix targeting first (24-DEP).
4. If uniformly low: site problem; run the leaky-bucket audit from landing to checkout (09-CRO, 07-LPG).
5. Ask the founder which core function they own; confirm the strong side with evidence; treat the hedged side as the gap.
6. Check margin (the source's case: $400k on $3M, about 13.3%) against what a hire on the missing side would cost `[web check: current pay for the role]`.
7. Before proposing headcount, run P21 (utilisation).
8. Model cash separately before any growth push (20-FIN).
9. Output: the bottleneck diagnosis report (section 9).
[c1dfbfcedccd] [5013501dc466] [4ccb3499516c] [5813209a4dbd] [12805cde65c1] [826839431464] [22f9b83f5cae] [9417ffc8e0f0] Checks: the diagnosis names 1 constraint with the data that shows it. Rollback: none. `[needs brand data: conversion by source, margin]`

**P32. Five-step commitment ladder for a new direction.** Goal: real commitment to a change (a new cadence, a new tracker, a new 3PL). Steps (03): state a vision bigger than a paycheck and picture success out loud; expect a doubt phase and do not read it as disloyalty; leadership commits first, and lists the unknowns, assesses worst cases, researches what can be researched (a small pilot), and names the irreducible risk; bring others in small groups with non-assumptive questions ("what do you think?"), listening without judging, and directed response (answer now, give a timeline, or say "I don't know"); let teammates propose the tasks. [9ed83f4b4706] [f1897dcf47ec] [63cb980cc32a] Checks: the unknowns list exists; at least 1 doubt was voiced and answered. Rollback: if people "pretend to commit" (say yes, mean maybe), you skipped the support phase; return to step 3.

**P33. Team culture check (03's instrument, discussion prompt only).** Steps (03): administer the 30 items on a 0 to 4 scale; total the first 25 (max 100); compute the odd and even sums and the odd-to-even gap for items 1 to 24 (gap over 24 read as poor team support; odd sum under 24 low involvement; even sum over 24 high engagement); items 25 to 30 as the leadership sub-score (max 24, midpoint 12). The source's total bands are inconsistent (below 60 and below 25 both called low), so use the numbers to start a conversation, not to rank teams. [50dadc5d2305] Checks: the inconsistency is stated when results are shown. Rollback: prefer P5 when only 1 instrument will be run.

## 5. Diagnostic checklists

Written so a worker can run them. Each row: what to check | how | good | bad | fix | source.

### 5.1 Org chart vs stage review

| what to check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| 5 silos owned | List administrator, CS, fulfilment, marketing, web dev; write owner | Every silo has a name (founder allowed) | Any blank | Assign before launch or next campaign (R1) | 06 |
| Founder load | Count silos and artefacts the founder owns | Founder covers extras below about $1M with freelancers for discrete tasks | Founder owns everything above the volume they can keep current | Name hire trigger (P2) | 06, 04 |
| Artefact owners | For each of tech pack, critical path, PO tracker, forecast, SLA, CS routing, scoreboard: owner and last update | Owner named, updated within cadence | No owner, or stale | Assign owner and cadence (R86) | 04, 02 |
| Tracker capacity | Revenue vs about $5M to $10M | Dedicated tracker owner exists past that band | 1 person keeps it "later" | Hire or reassign (R100) | 04 |
| Planning role | Is anyone accountable for the reorder review before the peak | Yes, named | Nobody until stockout | Ops manager owns P26 (R7) | 04 |
| Top team span | Can the staff meeting still debate | Yes | Too many attendees, decisions stall | P24 | 02 |
| Hero dependence | Who holds the only copy of key knowledge | Backup named for each critical process | 1 person, no backup | Two in a box; succession plan (R12) | 01, 05 |
| Team vs individual work | For each recurring job: needs many perspectives, or 1 expert | Matched | Committees doing expert work; 1 hero doing cross-functional work | Reassign (R10) | 05, 03 |

### 5.2 Hire readiness check

| what to check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| Utilisation first | P21 answers | Key people report 70%+ used | 50% or lower | Leadership fix (P20) before hire | 01 |
| Role definition | Read the role scorecard | Names 1 function, behaviours and results | "A player", "manager" | Rewrite (R5) | 07, 05 |
| Trigger | Read the hiring plan | A number in orders, tickets or revenue | "when we're settled" | Write it (R3) | 04, 06 |
| Founder archetype | Ask which core function they own | Confident, evidenced | Hedging on the side the hire fills | Hire that side (R6) | 07 |
| Assignment change tried | Was an existing person considered | Yes, with reasoning | No | R23 | 02 |
| Behaviour bar | Scorecard includes trust, conflict, commit, accountability, results, drive | Yes | Skills only | Add (R15) | 02, 06 |
| Interview plan | Questions listed | Only sourced questions plus brand-specific ones marked as such | Invented rubric presented as sourced | Mark as not sourced (R18) | 01, 06, 07 |
| Comp options | List for the human | 2+ options within margin | Full market cash assumed on thin margin | Add equity or performance pay option (R21) | 07 |
| Who decides | Check the plan | Human named | Agent implied | R111 | ecomOS |

### 5.3 Team health assessment run

| what to check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| Desire to win | Ask; watch reaction to missed goals | Morale moves with results | Team exists to exist | Do not run results tools yet (R59) | 02 |
| Assessment done | P5 totals per dysfunction | 8 to 9 | 3 to 5 on any layer | Start at lowest broken layer (R45) | 02 |
| Spread | Range of scores per dysfunction across members | Narrow | Wide | Trust or communication issue; P6, P7 | 02 |
| Silence | Do people known to disagree privately debate in meetings | Yes | Calm agreement | Miner of conflict; P7 (R29, R50) | 02, 05, 01 |
| Recurring item | Any issue on 3+ agendas with an even split | None | Present | Force the debate with a deadline (R49, R53) | 02 |
| Leader vulnerability | Did the leader admit a mistake first this quarter | Yes, unstaged | Never, or staged | R28, R46 | 01, 02, 03 |
| One goal | Is there 1 number with a date and owner | Yes | Several, or revenue only | P9 | 02, 05 |
| Owners per category | Each scoreboard line has a name | Yes | "Someone tracks that" | P9 step 3 | 02 |
| Accountability source | Who calls out a miss | Peers | Only the leader | R55; P10 | 02 |
| First team | Ask each lead | Leadership team | Own department | Discuss (R58) | 02 |
| Relapse plan | Is there a next session date | Yes | One offsite only | Quarterly re-run (R61) | 02, 05 |
| Effective team traits | Score the 12 characteristics after a meeting | Most present | Conflict on people; 1 or 2 talkers | R70, R73 | 03 |
| Cause layer | Check communication, structural, personal; internal and external | Both layers reviewed | Only process blamed | R71 | 03 |

### 5.4 Meeting cadence audit

| what to check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| Cadence written | Find the list of meetings, owners, lengths | Exists and owned | Ad hoc only | Write it; interval is the brand's call (R63) | 05, 02 |
| 4 meeting types | Annual reset, quarterly deep dive, weekly operating, ad hoc | All 4 exist in some length | 1 recurring call for everything | Add types; lengths per brand (R64) | 02 |
| Agenda | Weekly meeting opens on the goal | Yes | Status round | P10 | 02 |
| Worth holding | Anything to debate | Yes | Nothing; meeting held anyway | Cancel (R65) | 02 |
| Ground rules | Present, participate, no laptops | Kept | Laptops open | Restate (R65) | 02 |
| Cascading messaging | Last 10 minutes | Done, recap written | Skipped | P11 | 02 |
| Decision deadlines | Each open decision has a date | Yes | Open-ended | R53 | 02, 03 |
| Talk share | Who speaks; any dominant voice | Balanced | 1 or 2 dominate | Poker chips; leader steps out (R73) | 01, 03 |
| Forecast review | Weekly, fortnightly or monthly with owner | Yes | Reactive | P26 (R90) | 04 |
| Freight re-shop | Monthly | Yes | Locked in | R93 | 04 |
| 3PL invoice audit | Monthly | Yes | Paid at face value | P29 | 04 |
| Reporting sludge | Count reports nobody reads (remote teams) | Trimmed | Growing | R72 | 03 |
| Check-in loop | 3x3 check-in held on the written cadence | Yes | Drifted | P12 | 05 |

### 5.5 SOP completeness check

No source gives an SOP template. This checklist lists the process documents the sources say must exist and what each must contain; the format is the brand's `[needs brand data: SOP format]`.

| document | must contain | good | bad | fix | source |
|---|---|---|---|---|---|
| Tech pack per product | Drawing, fabric spec (GSM), grading, graphics, hardware, labels, packaging, sample photos | On file before the PO | Missing; disputes unwinnable | P25 precondition; 18-COG for contents | 04 |
| Critical path | Steps, owner, duration, date per step; supplier read-only | Live and monitored daily | Suppliers edit dates | R89 | 04 |
| Forecast sheet or tool | Base period rule, growth or seasonality method, padded lead time, days of stock, safety stock, owner, cadence | All fields set | Stockout days in the base | P26 | 04 |
| PO record and tracker | Authoritative PO in accounting software; visible tracker with SKU, qty, PO number, dates, vessel | Both exist, internal only | Alibaba order lines only | P27 | 04 |
| 3PL SLA | Pick time, consequence, cycle counts, ASN rules, 4 price components | Signed | Verbal | P28 | 04 |
| Invoice audit sheet | Rate card, expected cost formula, monthly comparison | Run monthly in code | Not run | P29 | 04 |
| CS routing rules | Definition of "complex", tier split, macros, ramp plan tied to forecast | Written | Undefined | P30 | 04 |
| Goals, roles, norms | The 3 foundations, written and dated | Exists | Assumed | P12 | 05 |
| Scoreboard and 1 goal | 5 to 7 categories with owners; 1 number and date | Published | Revenue only | P9 | 02 |
| Responsibility chart | 1 R per decision type | Published | 0 or 2 R values | P14 | 03 |
| Role profiles | Written for every role with recent ambiguity | Exists | Verbal | P13 | 03 |
| Meeting cadence | List, owner, length, agenda type | Exists | Ad hoc | 5.4 | 02, 05 |
| SOP as promotion gate, trial tasks | Not in any source | n/a | Presented as sourced | Mark "human designs" (R18) | none |

### 5.6 3PL SLA review

| what to check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| Pick time | SLA term vs actual from 3PL data | 24 to 48 hours off-peak, met | Missed, no consequence applied | Apply the written consequence; escalate | 04 |
| Delivered on time | Own CS or fulfilment data | About 95% or above | Below about 95% | Split pick lag from carrier lag before a credit claim (R97) | 04 |
| Cycle counts | Count in the last 12 months | 2 or more | Fewer | Enforce SLA | 04 |
| Barcode scanning | Inbound and outbound confirmed | Both | Either missing | Missing stock cannot be resolved; fix or re-RFP | 04 |
| Invoice vs expected | P29 comparison | Within tolerance | Any line above expected | Dispute; source says 30 to 40% of one sample overcharged | 04 |
| Forecast given | Last forecast sent vs actual | Honest, close | Over-promised | Re-send realistic numbers (R94) | 04 |
| Peak staffing | 3PL's plan for Black Friday and Christmas | Written | None | Raise now; source's peak failure cost over $20M | 04 |
| Account standing | Are you their smallest or largest client | Valued | Ignored | Consider re-RFP | 04 |
| Backup 3PL | Second qualified 3PL on file | Yes | No | Keep RFP runner-up warm | 04 |
| Data shown | Any metric missing | Shown as unavailable | Shown as 0 | R113 | ecomOS |

### 5.7 Bottleneck diagnosis

| what to check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| Traffic vs conversion split | Ask; then pull both | Both measured | Only blended CR | P31 step 2 | 07 |
| Conversion by source | Segment by source, campaign, geo | Most near category norm, a few dragging | Uniformly low | Traffic match (24-DEP) vs site (09-CRO) | 07, 06 |
| Recurring pre-purchase questions | Read tickets for themes | Few | Sizing, shipping, returns repeated | Fix the page, not response time (R108) | 06 |
| Founder archetype | Ask; note hedging | Clear strong side with evidence | Hedging both sides | Weak signal; confirm with data (R104) | 07 |
| Sourcing edge | How long has the supply been exclusive | Still scarce | Competitors found it | Do not treat as moat (R105) | 07 |
| Utilisation | P21 | 70%+ | 50% or lower | Leadership before headcount (R4) | 01 |
| Margin for the hire | Profit / revenue vs role cost | Supports cash comp | Thin (source case about 13%) | Equity or performance pay option (R21) | 07 |
| Cash for growth | 13-week view (20-FIN) | Covers inventory and ad spend ahead of revenue | Gap | Secure levers first (R107) | 07, 04 |
| Planning role | Anyone owning reorders before the peak | Yes | No | R7 | 04 |

## 6. Thresholds and benchmarks

Confidence: number of sources that agree, and the basis. "Single operator" means 1 founder or coach video with self-reported figures. "Convention" means the author's own scoring rule with no validation.

| value | condition | source | confidence |
|---|---|---|---|
| 5 silos (admin, CS, fulfilment, marketing, web dev) | Any launch | 06 | 1, opinion |
| Founder holds all ops roles below about $1M revenue; freelancers for discrete tasks | Early stage | 04 | 1, single operator |
| Dedicated tracker owner at about $5M to $10M revenue | Shared PO and freight sheet | 04 | 1, single operator |
| ERP at about $30M to $50M revenue; cost "over $200 grand", own case "upwards of half a million" | Outgrowing spreadsheets | 04 | 1, single operator |
| Problem-solving team 5 to 12 people | Same department, weekly meeting | 03 | 1, convention |
| 5 to 9 direct reports assumed by the model | Executive team | 02 | 1, model assumption |
| Regroup at more than 250 staff, 8 reports to 5 | Fable example | 02 | 1, fiction |
| Diminisher extracts 20 to 50% of capability; Multiplier 70 to 100%+; ratio about 2x (2.1x with over-100 answers) | Self-reported recall, 144 leaders, 2007 to 2009 | 01 | 1, self-reported research |
| Under a Diminisher people run at about 50%; 11-person team gives back "5 full-time people" | Illustrative maths | 01 | 1, illustration |
| Strong in 3 of 5 disciplines is enough | Multiplier status | 01 | 1, author's pattern |
| Zenger-Folkman percentiles: 0 strengths 34th, 1 at 64th, 2 at 72nd, 3 at 81st, 4 at 89th | 8,000 leaders, 2002 | 01 citing external study | 1, external, dated |
| 30 days for 1 practice; 1 year on 1 question | Habit building | 01 | 1, assertion, no study named |
| 30% answer in 2 days | Pacing ambiguity | 01 | 1, 1 case |
| Hexal: 3-minute screens x 8, 3 hours with finalist | Hiring speed | 01 | 1, 1 case |
| Assessment bands 8 to 9 fine, 6 to 7 maybe, 3 to 5 address | 15 statements, 3 per layer | 02 | 1, convention, not validated |
| Personal histories 30 minutes minimum | Trust | 02 | 1, practice |
| Team effectiveness exercise 60 minutes minimum | Trust with baseline | 02 | 1, practice |
| MBTI session 4 hours minimum | Style disclosure | 02 | 1, practice; validity `[web check]` |
| Cascading messaging 10 minutes, every meeting | Alignment | 02 | 1, practice |
| Scoreboard 5 to 7 categories, 1 owner each, monthly review | Results | 02 | 1, fable; goals few and simple agreed by 05 |
| Cadence: annual 3 days, quarterly 2 days, weekly 2 hours, ad hoc 2 hours, about 8 days a quarter | Executive team | 02 | 1, fable |
| Observe 2 weeks before changing anything | New leader | 02 | 1, fable |
| Fred story: 3 of 7 quit in 2 weeks; recovery in about a month with 3 fewer | Toxic promotion | 02 | 1, anecdote |
| Check-in to working time ratio: none | Any team | 05 | 1, explicit refusal |
| "Well over half" of people withhold their views | Meetings | 05 | 1, uncited research |
| Role negotiation 1 day minimum; 2 days plus follow-up at 1 month best | Power-based resistance | 03 | 1, practice |
| Team culture scale: 30 items, 0 to 4; total of first 25 max 100; low below 60 (also stated below 25); odd-even gap not over 24; odd sum under 24 low involvement; even sum over 24 high engagement; leadership items 25 to 30 max 24, midpoint 12 | Culture check | 03 | 1, convention, internally inconsistent |
| 3 essential Belbin roles: Co-ordinator, Plant, Monitor Evaluator | Team composition | 03 | 1, Belbin via handbook |
| Tech pack freelance about $200 | Upwork | 04 | 1, anecdote `[web check]` |
| About 20% price improvement from comparing factories | Negotiation | 04 | 1, single operator example |
| Container $11,000 / 1,000 units = $11 per unit (transcript says $1; wrong) | Sea freight | 04 | 1, worked example with a slip |
| Days of stock 4, 8 or 12 weeks | By volatility and capital | 04 | 1, heuristic |
| Safety stock 5 to 10 days after padded lead time | Reorder | 04 | 1, heuristic |
| Lead time example 100 days | Forecast input | 04 | 1, example only |
| Forecast miss about 5% big-box, about 50% growing ecommerce | Accuracy | 04 | 1, uncited baseline and own estimate |
| 90 to 95% of ecommerce has meaningful seasonality | Forecast method | 04 | 1, single operator |
| DHL sample from China about 5 days | Critical path | 04 | 1, example |
| Freight providers 2 to 3, re-shop monthly | Freight | 04 | 1, single operator |
| SLA pick 24 to 48 hours off-peak | 3PL | 04 | 1, recommendation |
| Cycle counts 2 per year minimum | 3PL | 04 | 1, recommendation |
| Delivered-on-time investigate below about 95% | Internal metric | 04 | 1, single operator |
| 30 to 40% of a client sample overcharged by 3PL or courier | Invoice audit | 04 | 1, unverified client-sample claim |
| 3PL failure: over $20M lost against a $45M to $50M peak forecast | 1 incident | 04 | 1, self-reported |
| Missing ops role: "30 to 40% bigger" | COVID surge at about $25M | 04 | 1, retrospective estimate |
| Local CS agents about 2x as efficient as untrained offshore | CS tiers | 04 | 1, single operator |
| Founder case: $3M revenue, $400k profit (about 13.3%), about 1% conversion, target $6.5M | 1 UK memorabilia brand | 07 | 1, self-reported |
| Buy about $200, sell about $2,000 | 1 item type | 07 | 1, founder example |
| "3 to 6 in 60 days"; "3 to 10, 12" with the right acquisition hire | Advisor's claim | 07 | 1, opinion, explicitly not a promise |
| Senior media buyer pay "multiple hundreds of thousands" | Comp | 07 | 1, unverified `[web check]` |
| Hire trigger for CS or fulfilment | Any | 06 | 0, none given `[needs brand data]` |

## 7. Where sources disagree

**C1. Debate slowly (01) vs decide fast (02).**
- 01: for high-stakes calls, frame, debate with safety and rigour, then decide and explain; deciding in an inner circle and announcing leaves the org "spinning" instead of executing (Akers vs Ziob) [d4847b17a26b] [8b7d0cbcfc56].
- 02: a decision is better than no decision; delaying for more data breeds paralysis; decide boldly and change boldly [6b7f86825119]. 02 also runs a 2-day fact-based debate before the Affymetrix recall in 01's telling, so the fast rule is about ordinary calls.
- 05 sits between: fast when speed matters, slow when several perspectives are needed [ab649028be47]. 03 adds: list the unknowns and research what can be researched before committing, then proceed on what is agreed [f1897dcf47ec] [788f0cb90b86].
- When each is right: 01 for pricing and offer changes, platform migrations, 3PL switches, repositioning, large POs (hard to reverse). 02 for everything the team revisits without new data.
- What the agent does: run the debate-worthiness check (R81) first. Hard to reverse or high stakes: P18 with a decision deadline (R53). Everything else: decide in the meeting, close with cascading messaging, and log it. A recurring item that keeps returning is treated as a fear-of-conflict signal (R49), not as a reason to debate longer.

**C2. Few elite generalists (01 Hexal, 06, 04 below $1M) vs redundancy and key-person risk (05, 01 backup, 04 above $5M, 04's 3PL failure).**
- For lean: 01's Hexal ran with no org chart and loosely defined roles, sold for $7.6B (1 case) [f7812fc26044]; 06 says the founder covers the extra silos personally rather than hiring a weak generalist [98fae764cd32]; 04 says the founder holds every ops role below about $1M [0ff782611bef]; 02's Fred story shows performance rising with 3 fewer people [f9f956b15e91].
- For redundancy: 05 calls the "great person theory" almost always a big mistake [12ad1d771f2c]; 01 says add backup without reducing ownership, build leaders so you can step away, hand over leadership before it becomes a dependency [f78fe4052829] [37aafeee291c] [7216e54fa5f1]; 04 says 1 person cannot keep the tracker reliable past about $5M to $10M and that a single 3PL failure cost over $20M [5eb084517f52] [875b2b81d78d].
- When each is right: lean below about $1M and for work that 05 says belongs to 1 expert. Redundancy for any process whose failure stops shipping or cash (the tracker, the reorder review, the 3PL), and for any person who holds the only copy of a process.
- What the agent does: keep roles lean in headcount but never lean in coverage. For each artefact in 5.5, name a backup (two in a box) even if the backup is the founder. Keep a runner-up 3PL warm. Never propose a hire only to reduce key-person risk without first documenting the process (R86) so the risk is smaller.

**C3. Ropes-course team building (03 lists it) vs the Lencioni exercises (02).**
- 02: experiential and outdoor exercises have "lost some of their luster... and deservedly so"; gains "do not always translate" to work; use only on top of the fundamental tools [f0b5fc985510].
- 03: lists outward-bound training, sensitivity training, interdependency exercises and visioning alongside skills workshops without evaluating them [e1daf5ed03eb].
- When each is right: 03's workshop list is for skills (listening, role clarity, consensus). 02's tools are for the causal chain (trust, conflict, commitment).
- What the agent does: propose P6, P7, P8 and P9 first; a skills workshop from 03's list only for a named skill gap; an outdoor event only if the human wants it and never as the trust fix.

**C4. Peer pressure (02) vs process (03, 04) for contractor teams.**
- 02: peer pressure is the most effective accountability mechanism and reduces the need for formal performance management; the leader steps in only as a last resort [00e9c7d1cd6a] [e3909b2c8cdc]. 02's model assumes full-time peers with mutual stakes; the contractor limit is `[pass 1 adaptation]` in mini playbook 02, not the book's claim.
- 03 and 04: published responsibility charts, role profiles, owners with dates on every artefact, and written SLAs with consequences [f684ff28794c] [2f17c3eca340] [30a460679b7f]. 01: visible scoreboard so people manage themselves [f09a30ff919d].
- When each is right: peer pressure inside a stable team of employees who share results. Written process for contractors, vendors and a 3PL, who are not peers and have no ambient context.
- What the agent does: for employees, R55 and P10. For contractors and vendors, R56, P11 in writing after every call, P14, and the SLA pattern of P28 (deliverable, date, consequence). Do not ask a contractor roster to hold each other accountable.

**C5. Fix CRO first (06) vs fix traffic match first (07).**
- 06: the site is a leaky bucket; the developer role exists to find and seal drop-off from landing to checkout [4ccb3499516c].
- 07: "the easiest way to improve your conversion is just get better people"; CRO obsession is a top overlooked failure; but only when segmentation shows some sources converting near 0 while others are normal [5013501dc466].
- When each is right: 06 when conversion is uniformly low across sources. 07 when a few sources or geos drag the blended number.
- What the agent does: never act on a blended conversion rate. P31 step 2 first. Recurring pre-purchase questions (06) are a page fix in either case (R108).

**C6. Fixed check-in cadence (02, 04) vs "it depends" (05).**
- 02: weekly 2 hours, quarterly 2 days, annual 3 days, monthly scoreboard review [e7f4cb5fa94f] [25f1e4a02461]. 04: forecast review weekly, fortnightly or monthly; freight and invoices monthly [87a5258c4926].
- 05: no fixed ratio; "it depends" on appetite for process; what matters is that check-ins happen at all; the source warns against turning this into "check in weekly" [d35411c91008] [ab649028be47].
- When each is right: 02's numbers for a full-time executive team; 04's for operating artefacts with real cost of staleness; 05's for the team-health check-in itself.
- What the agent does: R63. A cadence is always written and owned. Operating artefacts get 04's intervals as defaults because staleness has a measurable cost. Team check-ins get an interval chosen with the human and recorded, and the 4 meeting types from 02 are kept in some length.

**C7. Fast-first hiring (01, Hexal) vs whole-team deep interviews (02).**
- 01: 3-minute first interviews for 8 candidates, 3 hours with the finalist [de18b6e39887].
- 02: the whole team interviews; 1 owner runs the search; the bar includes team behaviours [2ca0bcfdd550].
- What the agent does: both, in that order (R16, P3). Fast screens are allowed; the deep finalist round with the team is not skipped.

**C8. Multiplication before addition (01) vs the missing ops role cost 30 to 40% (04).**
- 01: check utilisation before headcount; a 2x gap is common under a Diminisher [9417ffc8e0f0].
- 04: no planning owner during the COVID surge meant stockouts; the founder estimates 30 to 40% lost growth [48e4499ac999].
- When each is right: 01 when the team reports low utilisation. 04 when a process has no owner at all; nobody can be "underutilised" on work nobody owns.
- What the agent does: P1 first (ownership), then P21 (utilisation), then P2. An unowned artefact is assigned before a hire is proposed; a hire is proposed only when the assigned owner cannot keep it current at the stated trigger.

**C9. Two team instruments (02's 15 statements vs 03's 30-item scale).**
- Both are conventions, neither validated; 03's bands contradict each other.
- What the agent does: P5 as the primary instrument, P33 only as a discussion prompt with the inconsistency stated.

**C10. Consensus (02 "consensus is horrible" vs 03 "consensus-based decisions").**
- 02 rejects consensus-seeking and wants buy-in with the leader deciding [28c1fbbb868f]. 03 defines consensus as not 100% agreement and proceeds on what is agreed [63cb980cc32a] [788f0cb90b86].
- What the agent does: the rule is the same once defined (R51): everyone heard, leader decides when agreement does not emerge, start before full agreement. Do not use the word "consensus" in a deliverable without this definition.

## 8. Common mistakes

Merged and deduplicated. Fix in brackets.

1. Hiring before checking whether the current team is underused, or hiring 1 generalist to cover all 5 silos. [P21, then P2; founder covers extras] (01, 06)
2. Leaving a silo or an artefact with no named owner, and "I'll update it later" on the shared tracker. [R1, R86] (06, 04)
3. Hiring "an A player" without naming the function, or skipping the roles conversation after a good goals talk. [R5, R13] (07, 05)
4. Building the operation around 1 hero, or a leader hoarding talent, showing off knowledge, or deciding in an inner circle. [R12, R26] (05, 01)
5. Tolerating a talented but destructive performer; waiting too long to remove them. [R24, P22] (01, 02)
6. Confusing a tense climate with an intense one; punishing questions or mistakes in front of the group; assuming silence is agreement. [R28, R29] (01, 02, 05)
7. Demanding outcomes outside a person's control instead of best effort and execution. [R28] (01)
8. Taking delegated work back, the bungee boss, rescuing people from consequences, accepting an AWK without a FIX. [R33, R34, P19] (01)
9. Trying to develop all 5 disciplines at once. [R36] (01)
10. Treating one offsite as the fix; expecting no relapse. [R61] (02, 05)
11. Seeking consensus, or delaying ordinary decisions for more data. [R51, R52] (02)
12. Several overarching goals, or revenue alone as the scoreboard. [R57] (02)
13. The leader as the only source of accountability; peers staying quiet. [R55] (02)
14. Skipping cascading messaging, so managers who sat in the same meeting say different things. [R54] (02)
15. Faking vulnerability; delivering an accurate diagnosis so bluntly the team unites against the leader. [R28, R46] (02)
16. Rewards that pit individuals against the shared result; 360 tied to pay or run without training. [R60] (02, 03)
17. Suppressing conflict during storming; demanding total agreement before starting; treating idea criticism as personal attack. [R48, R51, R42] (03)
18. Team size by default; a team stacked with 1 type; an Implementer as leader; the leader holding every role. [R11, R74, R75] (03)
19. Authoritarian style as routine; yelling; delegating to shift blame. [R35] (03)
20. Reporting sludge in distributed teams. [R72] (03)
21. Ignoring the external system (selection, rewards, training) when a team underperforms. [R71] (03)
22. No tech pack before a large order; supplier communication spread across channels; no refund or tolerance terms before wiring money. [R87; 18-COG] (04)
23. Suppliers editing the critical path or tracker. [R89, R92] (04)
24. Stockout days in the forecast base; SKU expansion without counting the forecast and capital risk. [R90, R91] (04)
25. POs living only as Alibaba order lines; discontinuing or refunding while a PO is landing. [R92] (04)
26. 1-quote 3PL selection; chasing the cheapest 3PL; no facility visit; no barcode scanning; accepting invoices at face value; under-forecasting the 3PL's peak staffing. [R94 to R96] (04)
27. Assuming offshore CS is cheaper without training and macros; staffing CS from current tickets instead of the sales forecast; blaming agents for upstream failures. [R98, R99] (04)
28. Acting on a blended conversion rate; CRO obsession when traffic is mismatched, or targeting changes when the site is uniformly weak. [R103] (07, 06)
29. Assuming a sourcing edge is a moat; pushing growth without modelling cash; treating equity as free. [R105, R107, R21] (07)
30. Over-reading a founder's hedging as proof of a skill gap. [R6] (07)
31. Quoting a source figure (2x, 30 to 40%, "3 to 6 in 60 days", $200 tech pack) as a target. [R109] (all)

## 9. Deliverables

**D1. Org plan by stage.** A 1-page table: silo | current owner | employee, contractor or founder | artefacts owned | backup | stage trigger for the next change (in brand numbers) | source of the trigger and its confidence. Plus a note on top-team span and who the COO-scope functions report to if a COO exists. Built by P1. Marks every `[pass 1 adaptation]` and `[not sourced]` item (pods, agency vs in-house).

**D2. Role scorecards.** 1 per open or ambiguous role: the single function it fills, outcomes owned (whole outcomes, not slices), decision rights from the responsibility chart, the behaviour bar (trust, conflict on ideas, commit, hold peers accountable, results over ego, drive), the sourced interview questions, and a blank block labelled "trial task and rubric: human designs, not sourced". Built by P2, P3, P13.

**D3. Hiring plan.** Ordered list of hires with: trigger number, function, why an assignment change or contractor will not do, comp options within margin (cash, performance, equity) for the human, search owner, and the screen-then-deep interview plan. States that the human decides (R111). Built by P2, P3, P31.

**D4. Team health report.** Assessment totals per dysfunction with bands and spread, the lowest broken layer, the 1 behaviour change for the quarter, the exercise plan (P6 to P9), the overarching goal and scoreboard with owners, the accountability read (who calls out a miss), first-team answers, the next re-run date, and a required field: which store metric moved this quarter (repeat rate, ticket backlog, launch on-time percent). Never linked to pay. Built by P5 to P10.

**D5. SOP index.** The 5.5 table filled in for the brand: each process document, its owner, cadence, last update, backup owner, and what is missing. Includes the 3PL SLA summary and the invoice audit status. Built by P1, P25 to P30.

**D6. Operating cadence calendar.** All meetings and reviews with owner, length, agenda type and interval: the 4 meeting types (annual, quarterly, weekly, ad hoc), the monthly scoreboard review, the forecast review, the monthly freight re-shop, the monthly 3PL invoice audit, the quarterly assessment re-run, the 30-day leadership challenge check-in, and cascading messaging as the last 10 minutes of every staff meeting. Intervals chosen with the human where 05 says "it depends". Built by 5.4 and P12.

**D7. Bottleneck diagnosis report.** The constraint named with the data that shows it (conversion by source, ticket themes, utilisation answers, margin, cash), the founder's archetype and evidence, and the recommended next move (targeting, site, hire, leadership practice, process ownership) with its source and confidence. Built by P31.

**D8. Founder or lead capacity plan.** The 5-discipline self-rating, the 1 weakness and 1 strength chosen, the single practice, the journal template, the day-30 check question, and which operating artefact or KPI the practice change is meant to move. Built by P20, P21.

**D9. High-stakes decision brief.** For any P18 decision (a pricing or offer change, an inventory or PO commit, a platform or 3PL migration, a hire or no-hire): the exact question, who decides, data required, the assigned opposing view, the deadline, the decision, the reasoning, and the cascading message. Built by P18.

## 10. What needs live data or a web check

**Needs brand data**
- Order volume, ticket volume and revenue by month, for every hire trigger (R3, P1, P2).
- Current roster, reporting lines, demonstrated strengths, where handoffs break (R1, R27, R74, P1).
- Current meeting cadence and whether a single overarching goal is agreed and reviewed monthly (R57, R63, P9, 5.4).
- The brand's own goals, roles, norms document format; SOP format (P12, 5.5).
- Which metric is the north star this period (P9).
- Conversion by source, campaign and geo; margin; cash view (P31, R103, R107).
- Days of stock by SKU, stockout days in the trailing period, supplier lead time, cash available for stock (P26).
- 3PL SLA rate card, monthly invoice, order count, delivered-on-time, pick time (P29, 5.6).
- CS spend, ticket volume, definition of "complex" (P30).
- Vendor and contractor list with scope, cost and reviewer (R14).
- Team assessment answers from every member (P5).

**Web check**
- Current standing and licensing of MBTI and the Thomas-Kilmann instrument; I-O psychology critique of MBTI validity (R68).
- multipliersbook.com Accidental Diminisher quiz and The Wiseman Group 360 still live (R38, P21).
- acquisition.com/roadmap still exists and is free; identity of the source 07 advisor (section 12).
- BBC story on the Oodie founder and the brand's current standing before citing source 04 publicly (section 12).
- Oodie founding year and COVID-era revenue if the case is dated in a deliverable.
- Current pay ranges for senior ecommerce media buyers (R21).
- Current tech pack freelance pricing (R87).
- Current features and pricing of Inventory Planner, Gorgias, Zendesk, NetSuite, Fulfil, Triple Whale, Monday.com, Asana, Notion, Xero, MYOB, Airtable (all `[verify UI]`).
- Standard Belbin role name "Completer Finisher"; attribution of the stage model (Tuckman) and force field analysis (Lewin) if cited; publisher and date of the 03 handbook.
- Current status of any named company or person from source 01 (frozen at 2010) before client-facing use.
- The study behind 05's "well over half" withholding claim, if precision is needed.
- Verification of 01's "42% higher at delivering world-class results" figure, whose derivation is not shown.

## 11. Freshness and stale-risk notes

- **Management books dated 2001 to 2010.** 02 was written in late 2001; 01's interviews ran 2007 to 2009 and its "current role" data is frozen at 2010; 03 is undated. The behavioural content does not depend on platforms and does not go stale for that reason. Company outcomes cited in 01 (Oracle, Gymboree, GMDAT, Affymetrix, Better Place) are single-company results at one time and some later reversed (GMDAT posted a loss; Better Place is not evaluated here). Re-verify any named company before client-facing use; the rules themselves need no re-check.
- **MBTI and TKI.** 02 calls MBTI "based in research" as of 2001. Its reliability and validity have been widely contested since. Re-check before recommending to a client; treat as self-disclosure only (R68). Annual check.
- **Tooling names in 04.** Zendesk vs Gorgias, Inventory Planner, NetSuite, Fulfil, Triple Whale, Monday.com, Asana, Notion, Xero, MYOB, Airtable, Alibaba Trade Assurance and inbuilt QC, the Shopify cost-per-item field. All carry `[verify UI]`; 04 discloses affiliate links for Triple Whale, Inventory Planner and its own 3PL list, and flags AI-driven disruption in customer service tooling. Re-check every 6 months and before any recommendation.
- **Source 04's revenue thresholds ($1M, $5M to $10M, $30M to $50M) and cost figures (ERP "over $200 grand", $200 tech pack).** Single operator, undated (recording sits around 2020 to 2023 by internal signals). Treat as order-of-magnitude only; the brand's own numbers replace them.
- **Source 07's pay claim and growth claims.** Undated, unverified; re-check pay annually.
- **Source 01's companion tools (multipliersbook.com, TheWisemanGroup.com) and 07's acquisition.com/roadmap.** Check the URLs before referring anyone.
- **The 3PL SLA terms (24 to 48 hour pick, 2 cycle counts).** Market norms and carrier accounts change; re-shop at each RFP and re-read the SLA yearly.
- **Nothing in 02, 03 or 05 references pricing or platforms**; only the named instruments above need a web check.

- **24 Sep 2026: ecommerce specificity pass applied from ECOM_REVIEW.md.** Priority block 3.0 added, 13 rules reworded for store-specific wording, 8 store levers added (R114 to R121), and about 2,150 words of generic leadership, team-health and OD-technique detail moved to Appendix A.

## 12. Source index

| no. | title | type | credibility and bias | contributed most |
|---|---|---|---|---|
| 01 | Multipliers: How the Best Leaders Make Everyone Smarter (Wiseman, McKeown) | book, 2009 to 2010, 104 cards | Author ran talent development at Oracle; 2-year study of 144 leaders via nominator interviews and a 48-practice survey; self-reported, retrospective, not peer-reviewed or replicated; Diminisher cases anonymised and unverifiable; secondary citations for the mindset science; sells a 360 and a quiz through its own site. Rating: strongest evidence base in the folder, still directional not causal. No ecommerce content; all store and agency mappings are pass 1 adaptation. | The 5 disciplines and their opposites, accidental diminisher checks, 30-day challenge, debate process, Investor delegation devices, utilisation check before headcount |
| 02 | The Five Dysfunctions of a Team (Lencioni) | book, 2001, 73 cards | Consultant whose firm sells team-health consulting; a fictional fable plus a 15-item questionnaire; no data, no real client cases, no outside research; every number is illustration or the author's heuristic. Rating: widely used framework, unvalidated; bias toward selling the model. No ecommerce content; contractor and agency-pod mappings are pass 1 adaptation. | The 5-layer chain, the assessment, the trust exercises, 1 overarching goal and the scoreboard, meeting cadence, cascading messaging, peer accountability, removal and succession procedures |
| 03 | Handbook on team building | training handbook, undated, unattributed, 36 cards | No author or publisher; Indian public-sector training register; synthesises Belbin, Dayal and Thomas, an unattributed Tuckman stage model and Lewin force field; no data; its team culture scale has inconsistent score bands (below 60 and below 25 both "low"); closing essay is 1 person's opinion on national work culture. Rating: useful catalogue of OD tools, no evidence, cannot be cited by name. No ecommerce content; Belbin-to-function mapping is pass 1 adaptation. | Belbin roles, Role Analysis Technique, responsibility charting, role negotiation, force field analysis, process consultation, the 5-step commitment ladder, leadership style by information and time |
| 04 | Complete E-commerce Operations Guide (the Oodie founder, "Davey") | YouTube transcript, undated (about 2020 to 2023), 22 cards | Founder of a claimed $650M lifetime-sales brand; sells a mentorship (Daily Mentor) and discloses affiliate links (Triple Whale, Inventory Planner, own 3PL list); all figures self-reported or from his client sample; self-reports a BBC "scammer" story after a 3PL failure; contains an arithmetic slip ($1 per unit spoken, $11 correct). Rating: the only source with real ecommerce operating mechanics; single operator, monetised, unverified; use its processes, not its numbers. | Process ownership: tech pack gate, critical path, forecast inputs (in-stock base, padded lead time, days of stock, safety stock), PO tracker, 3PL RFP, SLA and invoice audit, CS tiers and cost per ticket, revenue-stage thresholds |
| 05 | Building High Performance Teams (Mario Musa, Knowledge at Wharton) | interview transcript, after 2011, 8 cards | Co-author of "Committed Teams"; evidence is observation of about 100 executive simulation teams at Wharton's EDP by the authors (2 anthropologists); qualitative, not controlled; not ecommerce; refuses to give a check-in cadence; the "well over half" statistic is uncited. Rating: modest, honest about its limits; all ecommerce examples in its cards are the card writer's. | The 3x3 loop (commit, check in, close), team vs individual work, the 3 failure modes, psychological safety, fast vs slow process, "it depends" on cadence |
| 06 | How to Build an E-commerce Team from Scratch ("Mac", Analytics of Life) | YouTube talk, undated, 7 cards | No agency, client, dataset or case named; channel promotion; every claim is opinion; gives no numbers, no hiring triggers, no process. Rating: weakest source; a starting inventory of roles only. | The 5 silos, founder covers extras until volume forces a hire, screen for drive, CS clears pre-purchase confusion, the leaky bucket framing |
| 07 | Helping a $3M/Year E-Commerce Brand Build a Team (unnamed advisor, acquisition.com pitch) | live coaching call transcript, undated, 8 cards | Unnamed advisor (affiliation implied by the closing lead-magnet pitch, `[web check]`); 1 founder's self-reported numbers ($3M, $400k, 1% conversion); no data pulled; growth claims ("3 to 6 in 60 days") are opinion; ends with a funnel pitch. Rating: a useful diagnostic script, zero evidence; every figure is this 1 business's self-report. | Traffic vs conversion split, segment before CRO, founder archetypes, hire the missing side, comp levers when margin is thin, cash before growth |

**Neighbour folders.** 18-COG-sourcing: tech pack contents, supplier and MOQ negotiation, QC, freight forwarders. 20-FIN-finance-and-accounting: landed cost, duties vs tax, cost per item, ERP cost, cash flow, comp structure economics. 17-CXP-post-purchase: helpdesk tools, macros, ticket diagnostics, tracking and packaging. 09-CRO-testing and 06-MEA-measurement: conversion segmentation and funnel audits. 24-DEP-ad-deployment: traffic targeting fixes. 04-BRD-brand: brand values in marketing, brand sequencing. 03-OFF-offers: any pricing or offer decision that P18 debates.


## Appendix A. General background

Moved here during the 24 Sep 2026 ecommerce specificity pass (ECOM_REVIEW.md section 5). The text below is unchanged from the base layer; only its location moved, so the store-facing sections above stay short and store-specific. Every rule id and card id below is the same one cited from its original spot; a citation elsewhere in this playbook that names one of these ids still resolves here.

### A.1 Leadership practice detail (moved from section 3.3, R25 to R44)

General leadership content from source 01 (Multipliers), with agreement notes from sources 02, 03 and 05. None of it has an ecommerce case in the original text; the Cisco, GE, P&G, Kissinger and Sridhar examples are all general management, not store examples.

**R25. Audit the assumption before copying a practice.** Source 01: Diminishers assume intelligence is scarce and fixed ("they will never figure it out without me"); Multipliers assume it is abundant and grows ("people are smart and will figure it out"). Behaviour follows assumption, so practices copied without the assumption do not hold. Source 01 only. [4fa842955f55] [603d1eea8a50]

**R26. Rate yourself on the 5 disciplines and their opposites. Strong in 3 of 5 is enough; never sit in Diminisher range on any.** The pairs: Talent Magnet vs Empire Builder; Liberator vs Tyrant; Challenger vs Know-It-All; Debate Maker vs Decision Maker; Investor vs Micromanager. Source 01's own data: most studied Multipliers were strong in 3, some in 4 or 5, and rarely weak in any. Source 01 only. [d70f32fe72f8] [1dbed4a92007] [ec007ef36f5e] [d4847b17a26b] [a9866b2456b8] [0d9014408391] [3446271d07b3]

**R27. Talent Magnet: find each person's native genius, label it publicly, use it at its highest point, remove blockers including yourself.** Native genius is what a person does easily and freely, narrower than a 360 strength; ask "why" about 3 times past a surface skill. Public labelling raises awareness and confidence (Jack Bossidy's staff meeting; the Hancock camp introductions). Source 01 only. [c9002d8e9d33] [a359bd6d6129] [56fb92416c2f] [770627149af5] [7edcea17b5cb] [675b8b35b46d]

**R28. Liberator: create space, demand best work, run rapid learning cycles.** Create space: talk far less than you listen; operate predictably; give a dominant talker poker chips (a fixed number of talk turns); label your comments soft or hard opinion so a casual remark does not become policy. Demand best work: ask "is this your best work?" (Kissinger); hold people to effort and execution, never to outcomes outside their control (Sridhar: zero tolerance for not running the experiment, no penalty for the result). Learning cycles: admit your own mistakes first and publicly. Source 01 [40f7b4e398fb] [d4d1178321c5] [213b38f15546] [de0b8b082153] [7176608e359f] [16e8102cd5ec]. Source 02 agrees the leader is vulnerable first and cannot stage it [52a8c149b778]. Source 03 agrees: Wexner's "Hall of Shame", and yelling at a mistake in front of peers destroys trust [0de5f24898f1] [60f28329351e]. 3 sources.

**R29. Intense, not tense. Assume people are withholding until the climate proves otherwise.** Source 01: after a hard meeting, ask whether people offered only safe, leader-agreeable ideas (tense) or bold ones and stayed engaged (intense) [6444ffb70c8e] [1dbed4a92007] [9fdf2daba130]. Source 05: "well over half the time" people do not share what they think (uncited research); psychological safety is the 1 thing Musa would pick [c94641818f5e]. Source 02: silence and calm agreement are the classic low-trust symptom; a prompt to check, not proof [0ae728a0b4ef]. 3 sources.

**R30. Challenger: seed the need, lay down a concrete challenge, withhold your answer, make it believable, co-create the plan, stage 1 early visible win.** Seed by showing the need (the GE bus trip to a trade show), by challenging assumptions (Prahalad's fake bankruptcy article), or by reframing a bottleneck as an opportunity (P&G Pringles). Lay a specific stretch target and ask the hard questions. "Helicopter down" to a ground-level proof point, let the executors co-create the plan, orchestrate 1 small early win before the big one. Source 01 [9087c1c9126b] [277ce40b634b] [475ce7aec24c] [53e8883c06ff] [7d7a0e4359e1] [7d46fb99d397] [263531838555] [808359b68558] [bcb9bdd6f85f]. Source 03's 5-step commitment ladder (vision, expect doubt, leadership commits first, inclusion in small groups, teammates propose the tasks) is the same shape [9ed83f4b4706] [63cb980cc32a]. 2 sources.

**R31. Control the pace of ambiguity: ask for a 30 percent answer in 2 days before deciding whether to invest in the 100 percent answer.** Source 01 only. [3d3c12db2fff]

**R32. Investor: define ownership up front (51 percent of the vote, 100 percent of the responsibility), give the whole outcome not a slice, stretch the role 1 level up, coach with questions, add backup without removing ownership, hand the pen back, let natural consequences run, make the scoreboard visible.** Source 01 [d150234124c0] [bc22e9ec9c05] [cb138faa8112] [38f23ceae927] [f78fe4052829] [4c69b917bb9f] [f90b88789a93] [9c377403f19f] [f09a30ff919d] [5d38c10d11cb]. Source 02 agrees on publishing goals, owners and standards so nobody can quietly ignore them [401b22a4cb2f] [25f1e4a02461]. 2 sources.

**R33. Never accept an AWK without a FIX, in either direction.** Do not hand a problem upward without a proposed fix, and when a delegated problem comes back, return it with "what would you like to do to fix this?" rather than solving it yourself. If you are doing most of the thinking on delegated work, you have taken it back. Source 01 only. [d7f2b6fe2bc3] [10e31326d248] [62673dab8487]

**R34. Avoid the bungee boss and the morning directive.** Jumping in only when something is visible to senior people, and re-deciding the team's day each morning, both destroy ownership. Source 01 only. [62673dab8487]

**R35. Directive leadership is allowed only as an extreme exception: a genuine crisis, the leader's insight verifiably greater, and no time for others to catch up.** Source 01's own FAQ [01bfefe3ebdb]. Source 03 agrees: choose authoritarian, participative or delegative by who holds the information and how much time there is; authoritarian rarely; yelling, demeaning language and threats have "no place"; delegating keeps responsibility with the leader and is not a way to shift blame [84d62308900c]. 2 sources.

**R36. Develop by working the extremes: neutralise your 1 worst discipline to acceptable, push your 1 strongest to world-class. Do not work all 5 at once.** Source 01 cites Zenger and Folkman's 360 data on 8,000 leaders: no distinguishing strength puts a leader at the 34th percentile; 1 strength 64th; 2 at 72nd; 3 at 81st; 4 at 89th. Source 01 only. [f51995e58591] [0d9014408391]

**R37. Change 1 practice for 30 days, then hold 1 question for a year.** Pick exactly 1 practice inside 1 discipline, run it 30 days, keep a journal. Then build layer by layer, commit to a year on 1 guiding question, and find a partner or peer group for accountability. The 30-day habit figure is the author's assertion with no study named. Source 01 only. [887d2303442c] [a49dc2d60271] [20942ff19843] [64aaf10b52e5] [a0c170241cea]

**R38. Run the accidental diminisher check; most Diminishers do not know and can change with feedback.** Source 01: many were promoted for personal brilliance and assumed the boss's job is to be the smartest person; others "went native" under Diminisher bosses. The book's quiz (10 scenarios, "A.D. score", lower is better) sits on multipliersbook.com `[web check: still live]`. Source 01 only. [d6302d3157e7] [25c379ab794f]

**R39. Multiply beyond the inner circle.** A leader can be rated a Multiplier by direct reports and a Diminisher by everyone else: "the farther removed people were from the leader, the more diminished they felt". Source 01 only. [3446271d07b3]

**R40. You do not need a Multiplier boss to start; build 1 visible team and expand.** Source 01 only, anecdote. [4478f914f73b] [80ec8f28a9ab] [8e62a8e6d487]

**R41. Do not hand these ideas to a "raging Diminisher" in a diminishing way.** "You can't diminish people into being Multipliers." Source 01 only. [0e3e89ef279a]

**R42. Counteract hierarchy on purpose: reach past it for frontline insight, and separate criticism of an idea from criticism of the person.** Source 01: org charts and approval matrices skew power up and reward compliance [b96dc4113fbb] [85b352b6b189]. Source 03: teams that conflate idea criticism with personal attack suppress dissent, including dissent aimed at leadership [788f0cb90b86]. 2 sources.

**R43. Set high expectations and model the vision; ask more than you tell.** Source 03 [d50bb3e8d0a0]. Source 01: questioning is the single highest-leverage leader habit [4c552fae77ce] [a41c5570c8d7]. 2 sources.

**R44. Count the cost of a Diminisher in a key role before acting.** Estimate the team at about 50% under that person and what full use of the rest would be worth; on an 11-person team the book's arithmetic gives back "the equivalent of five full-time people". Illustrative maths on a self-reported finding. Source 01 only. [8abb782bbe28] [3c9e69b660b3]

### A.2 Trust-building exercises (moved from section 4.2, P6 to P8)

Generic HR scripts from source 02's fable with no store tie. Use P5 and P9 for the store's own team health and scoreboard work; run these only if the human wants a deeper trust exercise.

**P6. Personal histories exercise (low risk).** Goal: a first, small lift in trust. Preconditions: a meeting or offsite, at least 30 minutes. Steps (02): round-robin, leader included: siblings, hometown, a unique childhood challenge, hobbies, first job, worst job. Keep the boundary explicit ("your life as a child, not your inner child"). Move into real work while the group is still loose; the effect fades. Note who stays outside the warmth. [a50879793a42] [acbe5b2bf41c] Checks: the leader went first. Rollback: none.

**P7. Team effectiveness exercise (higher risk, more useful).** Goal: peer feedback that turns into assignments. Preconditions: some baseline trust; at least 60 minutes. Steps (02): each member privately names, for each peer, the single most important contribution and the 1 thing to improve or stop. Report 1 person at a time, all peers giving input while that person listens without defending. Start with the leader. Follow up each development area in later one-on-ones. [1c7756fd2d21] Checks: every named development area has a follow-up date. Rollback: stop if it turns into personal attack; restate R48.

**P8. Strengths and weaknesses round tied to business impact.** Goal: named gaps that become assignments, coaching or hires. Preconditions: P6 done. Steps (02): 5 minutes each to write 1 biggest strength and 1 biggest weakness framed as contribution to the team's success or failure; ban soft weaknesses and false modesty; leader first; let peers sharpen a shallow answer; do not force a defensive person deeper; stop a peer who lands a joke at someone's expense. Use the output for staffing. [242e9d4d282d] Checks: each gap has an action. Rollback: none.

### A.3 OD technique write-ups (moved from sections 3.5 and 4.2)

Role Analysis Technique, role negotiation, force field analysis and process consultation, from the undated source 03 handbook. Keep P14's responsibility-charting decision list in the base layer (section 4.4); these are the generic technique mechanics behind the other role and responsibility rules.

**R76. Clarify an ambiguous role with the Role Analysis Technique.** Pick the focal role, define it jointly with the incumbent and the team, the incumbent writes the role profile, the accepted profile becomes the role. Best for new teams or role confusion. Source 03 only. [ae9c30902c6c]

**R78. Use role negotiation only when resistance is power-based.** Contract on work behaviours, not feelings: each person states what to start, stop, continue; each fills a form per colleague (more, less, unchanged); pairs trade; a follow-up meeting checks the contract. Minimum 1 full day; 2 days plus a follow-up a month later is best. Source 03 only. [10b3930ea6dc]

**R79. Unblock a stalled situation with force field analysis, and add a stabilising step at the end.** Describe current and desired states, list driving and restraining forces, split them by what you control, choose moves that raise driving and cut restraining forces, then plan how to hold the new state. Source 03 only. [6572b0c296da]

**R80. Choose a conflict mode on purpose.** Source 03 [059d6a41d014]; source 02's TKI [dd193a22adc1]. 2 sources.

**P13. Role Analysis Technique.** Goal: 1 written role profile for an ambiguous role. Steps (03): pick the focal role; the incumbent and team define its requirements together; the incumbent writes the role profile; the accepted profile becomes the role. [ae9c30902c6c] Checks: the profile names outputs, decision rights and handoffs. Rollback: re-run when the role changes.

**P15. Role negotiation (power-based resistance only).** Goal: a behaviour contract between people whose influence a change threatens. Preconditions: at least 1 full day; 2 days plus a follow-up 1 month later is best. Steps (03): contract on work behaviours not feelings (start, stop, continue); each person writes for every other what to do more, less, unchanged; pairs trade until both feel the return is fair; follow-up meeting checks the contract. [10b3930ea6dc] Checks: every trade is written and dated. Rollback: if resistance is doubt not power, use P32 instead.

**P16. Force field analysis.** Goal: unblock a stalled change (a 3PL switch, a new meeting cadence, a tracker nobody updates). Steps (03): describe the current state and why change is needed; describe the desired state fully; list driving and restraining forces; split by what you control; pick moves that raise driving and cut restraining forces; once reached, plan how to hold it. [6572b0c296da] Checks: at least 1 restraining force removed, not only driving forces added. Rollback: none.

**P17. Process consultation for a recurring interpersonal conflict.** Steps (03): define the problem with the conflicted person involved; develop options together; the final recommendation is owned by the person, not handed down. Counselling means listening and helping the person find their own way, advice only when needed. [0b4cac182293] Checks: the person states the recommendation in their own words. Rollback: escalate to P22 only after specific repeated behaviour.

### A.4 Belbin role taxonomy detail (moved from R74)

9 roles: Co-ordinator, Shaper, Plant, Monitor Evaluator, Implementer, Team Worker, Resource Investigator, Completer Finisher, Specialist. 3 are essential: Co-ordinator, Plant, Monitor Evaluator. Map by observed behaviour, not title. Flag a team stacked with 1 type. Do not make an Implementer the leader (lacks vision, reacts badly to ambiguity). Match roles to task stage. The mapping of Belbin roles to merchandising, creative, margin review and QA in mini playbook 03 is `[pass 1 adaptation]`.

### A.5 MBTI and Thomas-Kilmann instrument description (moved from R68)

Source 02 prefers MBTI (minimum 4 hours) and says people identify their own type [d2ff2bd42550] [e3a83ce7c404]. Source 02 also names the Thomas-Kilmann instrument for conflict style [dd193a22adc1] [a1fdc9095aec].

### A.6 Illustrative anecdotes (moved from R19 and R24)

Source 01's Shackleton ad: "Small wages, bitter cold... safe return doubtful"; it drew hundreds of well-suited applicants. [d7ddc08248a1]

Source 01: Bloom Energy fired a world-expert scientist 18 months before a beta and missed the deadline by 2 days [770627149af5] [3c9e69b660b3]. Source 02's Fred story: promoting a talented but disliked analyst lost 3 of 7 staff in 2 weeks; after Fred left, performance recovered in about a month with 3 fewer people [f9f956b15e91].
