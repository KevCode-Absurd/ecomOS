# 09-CRO-testing playbook

version: 2.0-draft  |  date: 24 Sep 2026  |  sources: 7  |  cards: 177  |  built from: sources/*.md

## 0. How to use this playbook

**Who runs it.** The growth experimentation agent (CRO agent). It owns the funnel read, the research inputs, the hypothesis backlog, the repair-or-ship-or-test call, test design, validity checks, the readout, and the registry record. A page audit worker can run section 5 on its own. Page redesign and copy execution hand off to 07-LPG.

**Which sections to load for which task.**

| task | load |
|---|---|
| Find where the funnel leaks | 2, 3.1, 3.2, procedures P1 to P3, checklist 5.1 |
| Gather research (recordings, heatmaps, surveys, review mining, user tests) | 3.3, P4 to P9, checklist 5.7 |
| Audit a page type for test ideas | 3.10, checklists 5.2 to 5.6 |
| Write and rank hypotheses | 3.4, P10, P11 |
| Decide repair, ship or test | 3.5, P12, section 6 |
| Size and design a test | 3.6, 3.7, P13, P14, section 6 |
| Launch, monitor, audit validity | 3.7, P15, P16, checklist 5.8 |
| Read and close a test | 3.8, P17, P18 |
| Prove programme or feature value (holdouts) | 3.9, P19, P20, P23 |
| Price or offer test | 3.11, P21 |
| Shopify platform limits | 3.12, P22, section 11 |
| Any point where sources disagree | section 7 |
| What to hand back | section 9 |

**Fetch before acting.**

- From brand data: monthly sessions (GA4, not Shopify), monthly orders, conversion rate by page, device and traffic temperature, AOV including shipping collected, gross margin by SKU, funnel stage rates, weekly traffic on any candidate test page, review count and media-review share, past test log and which winners are still live. Full list in section 2 and section 10.
- From the data layer: behaviour tool (Microsoft Clarity or Hotjar), survey tool (post-purchase and exit), GA4 Explore funnel, Shopify analytics, the A/B testing tool and its stats engine.
- From the web: current Shopify checkout A/B options and plan limits, the testing vendor's stats engine and free tier, current tool prices, current Baymard figures. List in section 10, cadence in section 11.

**Source notes to keep in mind while reading.**

- Mini playbook 01 (Exposure Ninja CLOSER course, 2020) was built for lead generation and service businesses. Its presenter says the ecommerce lure is "obviously" the product and that the sales-process lesson is "only relevant for service companies". Every ecommerce use of 01 in this playbook (PDP proof placement, quiz design, cart reassurance, email-capture lures, form-field rules) is the card writers' adaptation, not the presenter's claim. Rules that rest only on 01 are marked "(01, lead-gen adaptation)" and are hypotheses to test, not proven ecommerce practice.
- Mini playbooks 05 and 06 carry header labels for 06-MEA. Parts of them belong to neighbour folders and are only pointed to here: tracking setup and GA4 funnel configuration (06-MEA), speed work (08-SPD), cart-recovery email and SMS flow builds (14-EML), ad-channel geo and platform lift tests (11-ADC), finance (20-FIN), page design output (07-LPG). This playbook keeps what an experimentation agent needs to design, run and judge on-site tests and holdouts.
- No case number here is a promise. None of the 7 sources reports sample size, duration and confidence for its own case results. Only 05 (the statistics manual) cites published studies with methods.
- Tags: `[verify UI]` for platform steps that change, `[needs brand data: what]` for anything that depends on the brand's own numbers, `[web check: what]` for anything to confirm live.

## 1. Scope and outcomes

**This folder covers.**

- Reading the purchase funnel and finding the biggest drop weighted by traffic and value.
- Research inputs that produce hypotheses: session recordings, click, scroll and Area maps, post-purchase and exit surveys, one-time surveys, review mining, user tests, customer interviews, self-purchase audits.
- Page-type audits (home, collection, PDP, cart, checkout, mobile) written as test-hypothesis checklists.
- Writing and ranking hypotheses with an evidence gate and a profit-weighted score.
- Deciding repair, ship or test by traffic, orders and the type of change.
- Sample size from a minimum detectable effect, runtime, stopping rules, validity checks (SRM, flicker, bots, tracking, promo overlap, peeking, multiple comparisons, novelty).
- Reading a result with a confidence interval, guardrails and business value; closing and recording it.
- Holdouts and incrementality for on-site work: feature holdouts and CRO programme holdouts. Channel holdouts and causal methods are described only far enough to route the question.
- Metric choice: revenue per visitor and contribution per visitor over conversion rate, with the traffic penalty that comes with revenue metrics.
- Price and offer test limits, Shopify platform limits, research tool choice.
- The registry record for every test, repair and holdout.

**This folder does not cover (neighbour folder).**

- Page design, copy rewrites, landing-page formats and offer construction as deliverables: 07-LPG. Section 3.10 keeps only the rules that seed test hypotheses.
- GA4 event setup, funnel configuration, attribution, tracking QA: 06-MEA. This playbook only says when broken tracking invalidates a read.
- Speed work (LCP, INP, images, scripts): 08-SPD. Section 3.10 keeps the mobile LCP target and the rule to isolate revenue impact.
- Cart-recovery email and SMS flows: 14-EML. This playbook keeps only "compare against a holdout".
- Ad-channel incrementality (geo holdouts, platform lift studies, on/off tests) and Meta ad-set splits: 11-ADC.
- Finance definitions beyond gross margin: 20-FIN.
- Difference-in-differences, BSTS, synthetic control, propensity matching, instrumental variables, regression discontinuity: named in 06 for routing only. They need specialist implementation and live with 06-MEA.

**Business measures this folder moves.**

- Revenue per visitor (RPV = conversion rate x AOV) and contribution per visitor (RPV x gross margin %). Primary outcomes.
- CAC, through conversion rate: CAC is about ad spend / (sessions x conversion rate), so a lift cuts CAC in proportion (02).
- Conversion rate by stage and segment, as a diagnostic.
- AOV, return rate, refund rate, repeat rate and LTV by acquisition angle, as guardrails.
- Programme value: net incremental lift against a holdout, not the sum of test lifts.

## 2. Inputs the agent needs

| input | from where | required or optional | why |
|---|---|---|---|
| Monthly sessions (GA4) and monthly orders, last 3 to 6 months | data layer (GA4, Shopify) | required | Picks the traffic band and the CRO model (R52 to R55). Shopify sessions include more bots (02). |
| Conversion rate by page, device, and traffic temperature (cold paid, warm, returning) | data layer | required | Diagnoses mix effects before any page change (R15). Baseline for sample size (R59). |
| AOV including shipping collected; revenue net of tax | data layer (Shopify: Net sales + Shipping collected) | required | Correct RPV (R3). |
| Gross margin by SKU or category | brand record or finance | required for ranking and RPV decisions | Profit-weighted prioritisation (R9, R44); contribution per visitor. |
| Funnel stage rates: PDP view, add to cart, checkout start, checkout complete, purchase, by device and channel | data layer (GA4 Explore funnel, Shopify) | required | Finds the biggest leak (R12). |
| Weekly eligible traffic on each candidate test page | data layer | required before any test | Runtime math (R62). |
| Weekly orders on the tested path | data layer | required before any test | Conversions per variant (R60). |
| Behaviour tool access (Clarity or Hotjar) with 90 days to 6 months of data | data layer | required | Insights, heatmaps, recordings (R23 to R30). |
| Post-purchase survey answers ("what almost stopped you") | data layer or user | required if it exists; else set it up (P7) | Objections that seed hypotheses (R31). |
| Exit-intent survey answers | data layer | optional | Non-buyer reasons (R32). |
| Review export (CSV) and review count, media-review share | data layer (review app) | required when 500 to 1,000+ reviews; optional below | Review mining (R34); proof rules (R104). |
| Past test log: hypotheses, results, which winners are still live | brand record | required | Avoid re-running losers; protect winners (R85, R87). |
| Repair log | brand record | required | Stops repairs being re-proposed as hypotheses (R50). |
| Active ad concepts by persona, offer and angle, with spend | brand record or 11-ADC | required for message-match audits | R108. |
| Checkout extras (shipping, tax, fees) as % of AOV | data layer | required for checkout audit | R116. |
| Returns, chargebacks, repeat rate and 365-day LTV by acquisition angle | data layer | optional, required before scaling a winning angle | R84. |
| Shopify plan tier and checkout extensibility status | brand record + `[web check]` | required before planning a checkout test | R123, R133. |
| Testing tool, its stats engine, prior (if Bayesian), SRM alert setting | data layer + `[web check: vendor docs]` | required before writing a brief | R67 to R69. |
| Marketing calendar (promos, launches, holidays) for the test window | user or brand record | required | Promo overlap check (R74). |
| Device split, logged-in or returning identified share | data layer | required | Mobile-first effort (R124); CUPED eligibility (C5). |
| Credibility asset inventory (reviews, UGC, certifications, press, warranty, customer counts) | brand record | optional | Proof hypotheses (R104). 01, lead-gen adaptation. |
| Brand voice and claims that are substantiated | brand record | required before any copy hypothesis ships | Health and beauty claims need substantiation (02). |
| Competitor and paid-ad landing pages | web (public) | optional | Pattern research only (R41). Keep separate from private data. |
| Current Baymard abandonment figures | `[web check]` | optional | Checkout hypotheses (R116). |

## 3. Decision rules

Every rule states the rule, when it applies, the mini playbooks that support it (by number), any conflict (by section 7 code), and card ids. Where only 1 source supports a rule, the rule says so. Where sources disagree, the strictest condition is kept here and the disagreement is written out in section 7.

### 3.1 Metric choice

**R1. Judge CRO on revenue per visitor or contribution per visitor, not on conversion rate.** RPV = conversion rate x AOV. Contribution per visitor = RPV x gross margin %. Condition: always as the decision lens; as the statistical primary metric only when traffic can power it (R6). Sources: 02, 03, 06; 05 agrees on the objective and adds the traffic penalty. Conflict: C8 (01 calls conversion rate "the only metric that matters"). Cards: [b9f3fede007a] [b2dc4e814c63] [372439a05cbd] [a9ed03163804] [83db79dbdb65] [25f9d85cd8e3] [7eeb62d20124].

**R2. Treat conversion rate as a diagnostic, never as a north star, and never compare it across brands.** 02 says it is the output of about 50 inputs, most of them off the page: category, price point, AOV, traffic source, how much the creative educates, purchase intent, cold-traffic share, product quality, return rate. 03 adds that a price cut raises conversion rate while cutting revenue per visitor. Condition: every readout and every benchmark comparison. Sources: 02, 03. Cards: [953e03390b0d] [b9f3fede007a] [83db79dbdb65].

**R3. Compute the numbers correctly before reading them.** Revenue: not Shopify "Total sales" raw (it includes tax); use Net sales + Shipping collected, or Total sales minus tax. AOV: Shopify's AOV excludes shipping collected; add it back. Sessions: use GA4, because Shopify sessions include more bot traffic. Conversion rate: corrected orders divided by GA4 sessions. Condition: every RPV or conversion figure this agent reports. Source: 02 only. `[verify UI]` `[needs brand data: GA4 vs Shopify session gap]`. Cards: [91d639e7e2e2].

**R4. Keep contribution per visitor gross.** Do not subtract CAC or ad spend from it. Read it next to LTGP:CAC, contribution profit and returning-customer rate, and track RPV as a long trend (02's agency uses about 2.5 years). Condition: reporting and trend reads. Source: 02 only. Cards: [b9f3fede007a] [91d639e7e2e2].

**R5. Never judge on one metric alone, because every single metric can be gamed.** Turn off paid ads and conversion rate rises while revenue falls. Run traffic campaigns and sessions rise with no revenue. Push high-AOV products and AOV rises while CAC makes them unprofitable. Cut prices and conversion rises while RPV falls. Raise opt-ins with a popup while purchases fall. Condition: every readout. Sources: 02, 03, 06. Cards: [91d639e7e2e2] [83db79dbdb65] [c076b110d253].

**R6. Pick the statistical primary metric by the decision and by the traffic.** Conversion rate is binary, low variance and fastest but ignores order value. Revenue per visitor captures both but is heavily skewed (97% of visitors spend $0; coefficient of variation about 750% in 05's example) and needs about 6x the traffic (about 175,000 vs 28,000 visitors per variant at a 3% baseline for the same relative MDE). Gross profit per visitor is "the honest objective" but has the same variance plus needs margin data. Condition: RPV as primary only when the store is in the 3,000+ orders per month band, winsorized; borderline near the top of the 300 to 3,000 band; below that, conversion rate primary with AOV, margin and RPV as guardrails. Sources: 05; 02 and 03 recommend RPV without this caveat. Conflict: C9. Cards: [7eeb62d20124] [0bda3b4d7e04] [b9f3fede007a] [a9ed03163804].

**R7. Guardrails must not get worse, even when the primary metric improves.** Standard guardrails: AOV, gross margin, return rate, refund rate, page load, add to cart, downstream purchase; add returns, chargebacks, repeat rate and 365-day LTV by acquisition angle before scaling a winning angle. A conversion win that tanks AOV, margin or LTV is not a win. Condition: every test brief and every readout. Sources: 05, 02, 06. Cards: [1f26cd618e2d] [7eeb62d20124] [dad9c85ea261] [c076b110d253].

**R8. Use a micro-conversion (add to cart, begin checkout, CTA click share, reach) as the primary metric only as a leading indicator, with purchase and revenue as guardrails.** Condition: low volume (30 to 300 orders per month), or when the tested step sits far from purchase (a collection filter, a homepage module). Never bank a micro-conversion lift without checking purchase. Sources: 05, 04. Cards: [67f74e89d43e] [1b7725e0ff57] [6d2e6fafa7df].

**R9. Weight by gross profit per conversion, not revenue, when ranking and reading.** A lift that shifts the mix toward low-margin SKUs can raise revenue and cut profit. Judge offers, bundles and thresholds on contribution, not AOV alone. Condition: prioritisation (R44) and any offer or mix test. Sources: 05, 02. `[needs brand data: SKU margin]`. Cards: [aad25dea9ed9] [0ca0ef2a3d5d].

**R10. Judge the programme on incremental revenue or margin against a counterfactual, not on tests launched or winners shipped.** "Would this have happened anyway? If you cannot answer that, you are optimising in the dark" (06). Condition: any programme review or agency report. Sources: 06, 05. Cards: [0eca60fd9161] [f671352f5b6e] [70db51ffb976].

**R11. Make the business case through CAC and the revenue equation, not through conversion rate itself.** CAC = ad spend / new-customer orders, about ad spend / (sessions x conversion rate). A conversion lift cuts CAC in proportion and lets spend rise back to the old CAC ceiling. 01's lead-gen version: at £1 CPC, 1% conversion is £100 per lead and 3% is £33. 06's version: revenue = traffic x conversion rate x AOV x repeat rate; CRO controls 3 of the 4. Condition: when deciding whether CRO work is worth funding versus more spend. 02 notes he has "almost never seen" anyone double conversion, and that conversion rate is only a small second-order input to Meta CPM. Sources: 02, 01, 06. Cards: [82fbec40a149] [b22709fcf770] [ab4878e2910b] [93fdbe5da8f2].

### 3.2 Reading the funnel and finding the biggest drop

**R12. Read the funnel before choosing a fix.** Instrument: sessions, product page view, add to cart, checkout start, checkout completion, purchase, plus AOV and RPV, by device and channel. For paid traffic also map ad, landing page, PDP, cart, checkout, thank-you page, post-purchase upsell. Pick the stage with the biggest leak weighted by the traffic and value passing through it. 03 calls funnel drop-off analysis a "non-negotiable" for every store, though a full GA4 analysis is not required under 300,000 sessions. Condition: first step of every engagement and after every shipped change. Sources: 03, 06, 05, 07. Funnel configuration itself: 06-MEA. `[needs brand data: stage conversion rates by device and channel]`. Cards: [bbe716a39c74] [9568c40e1d88] [25f9d85cd8e3] [f856d689f3d8] [382d08d3f6aa].

**R13. Compare each stage with the 06 bands, but treat them as directional because 06 names no study.** Overall conversion: poor under 1%, average 2 to 3%, good 3 to 5%, excellent over 5%. Add to cart: poor under 5%, average 8 to 12%, good 12 to 18%, excellent over 18%. Cart to checkout: poor under 30%, average 50 to 60%, good 60 to 70%, excellent over 70%. Checkout completion: poor under 50%, average 60 to 70%, good 70 to 80%, excellent over 80%. PDP conversion by vertical: beauty 2.5 to 4%, apparel 1.8 to 3%, electronics 1.2 to 2%, home 1.5 to 2.5%. Condition: check traffic intent, cold share and device mix before blaming design on a low band; 02 says conversion rate has a ceiling set by category, price and traffic quality. Source: 06 only for the bands; 02 for the ceiling. Cards: [25f9d85cd8e3] [953e03390b0d].

**R14. A drop shows where, not why.** Follow every funnel drop with recordings, heatmaps, surveys or user tests on that step before writing a hypothesis. Condition: always. Sources: 03, 07, 04. Cards: [bbe716a39c74] [382d08d3f6aa] [6d2e6fafa7df].

**R15. Before touching a page after a conversion-rate change, diagnose the mix.** Split conversion by traffic temperature (cold paid, warm, returning). If cold share rose, the blend falls with no page change (02's example: blended 2.8%, cold 1%, warm 4%). Check returning-customer share (it inflates conversion rate and AOV), category, price point, AOV and creative changes. Audit the page only if a segment's own rate fell with steady creative. If clarity, offer and proof are already good, look at product quality, first-order contribution, launches and repeat purchase before another redesign. Condition: any conversion-rate move that triggers a redesign request. Source: 02 only. `[needs brand data: cold vs warm conversion rates]`. Cards: [953e03390b0d] [372439a05cbd].

**R16. When checkout completion is the leak, fix checkout first, mostly as repairs rather than tests.** Baymard (as cited by 05 and 06): 70.22% average cart abandonment across 50 studies, about 32 checkout improvements available on a large site, about 35% checkout uplift available from UX fixes alone, 11.3 average form fields. 06 calls "fix checkout first" strategic priority 1. Condition: applies when the checkout completion band is poor or average (R13). Most checkout changes on standard Shopify plans cannot be A/B tested client-side (R123), so ship them as repairs and best practice, and measure with before-and-after stage rates as weak evidence (R55). Sources: 06, 05, 02. `[web check: current Baymard figures]`. Cards: [d4104b13110f] [3163cc34fa79].

**R17. Confirm tracking health before trusting any funnel read.** Compare event counts with orders in the store backend. Missing or inconsistent events mean fix tracking first (06-MEA). Broken tracking invalidates a test read. Condition: before every funnel read and every test launch. Sources: 07, 05. Cards: [382d08d3f6aa] [3eca46fe9ba3].

**R18. Category exit rate should sit near the site average.** A high exit rate means visitors leave the site instead of moving to product pages. Check traffic intent first, then design. Condition: collection pages with material traffic. Source: 06 only. Cards: [1e03a58f6fe1].

**R19. Treat every PDP and collection page that gets direct entrances as a cold-traffic landing page.** Search and ads send people to inner pages, so homepage proof and awards are not seen. Audit those pages as landing pages. Condition: pages with a material share of direct entrances. Source: 01 (lead-gen origin; the ecommerce use is the card writer's). `[needs brand data: which pages get direct entrances]`. Cards: [3127398d2368].

### 3.3 Research inputs

**R20. Research produces hypotheses, not tests, and every hypothesis needs at least 2 points of evidence before it enters the backlog.** Quantitative data shows what is happening; qualitative data shows why. Analytics plus 1 of: replay, heatmap, survey, user test, interview. 03 calls data "single-handedly the most important thing" in CRO. 05 notes DRIP's 36.3% win rate comes from pre-qualifying every hypothesis with analytics, recordings and heatmaps. Condition: every backlog entry. Sources: 03, 05, 04, 07. Cards: [25979af2691c] [f856d689f3d8] [aad25dea9ed9] [6d2e6fafa7df] [6e48c0e74fe7].

**R21. Run 03's non-negotiables at any traffic level.** Funnel drop-off analysis; a heatmap on the PDP ("at 10,000 or 10 million sessions"); a false-click and rage-click check; a post-purchase survey; and review mining once the store has 500 to 1,000+ reviews. Allow about 1 to 2 weeks to gather this under 300,000 sessions. Condition: every store before its first test. Source: 03; 05 and 07 agree on the inputs. Cards: [9568c40e1d88] [b4505f6c4061] [fc9b05411697] [bbe716a39c74].

**R22. Behaviour data supports a hypothesis; it never proves a lift.** Heatmaps, scroll maps and recordings show behaviour, not cause or statistical significance. Use them to prioritise a test, then apply sample-size math before claiming conversion or revenue impact. Condition: always. Sources: 04, 07, 05. Cards: [6d2e6fafa7df] [0b8d2f6cc4d1] [3043da84ee0c].

**R23. Start every map or recording review from the page's one core action.** Name it first (add to cart, buy now, start checkout, sign up). Then ask 3 questions: do people reach that section, do they take the action, and if not, what would get them there. Condition: every page review. Source: 04. Cards: [09583734387e] [6d2e6fafa7df].

**R24. In Clarity, read the Insights block and the recordings, and take top-line metrics from GA4.** Rage clicks, dead clicks, excessive scrolling and quick backs are Clarity's value. Sessions, scroll depth, pages per session, smart events, channel and device all come from GA4, which 04 says does funnels "a much better job". Keep top-line metrics only as context and for segmentation. Condition: any Clarity review. Source: 04. `[verify UI]`. Cards: [e053644d5707].

**R25. A percentage alone never justifies a change; watch the recordings behind it.** If a real usability issue exists, fix it whatever the rate. If the rate is low and no clear issue shows, it is not a priority. 04's heuristic: rage clicks under about 1 to 2% is "good" (demo account 0.2%); excessive scrolling under 0.01% "not a major concern". No threshold for dead clicks or quick backs. Condition: every Insight rate. Source: 04 only. Cards: [9d9871ee324b] [5b9da7dd1967] [e053644d5707].

**R26. Classify behaviour signals by what the shopper expected.** Rage clicks usually mean a shopper cannot get out of something or cannot make something work: a popup in the first 5 seconds, a chat widget covering add to cart or submit, a hard-to-hit close control. Dead clicks matter only when the missing action would help the purchase (site logo that does not go home, product image that does not open a gallery, pricing block with 1 working button, informational check marks); press logos can stay static so shoppers do not leave. Excessive scrolling and quick backs usually mean missing or buried information (reviews, price, add to cart, delivery). Elements styled like buttons or links that do nothing ("false clicks") cost money; 03 reports "massive" wins from removing them in high-volume stores. Condition: confirm the cause in recordings for the same page and device before assuming. Sources: 04, 03. Cards: [9d9871ee324b] [0eae610ddc62] [5b9da7dd1967] [9568c40e1d88] [a2d5c573076a].

**R27. Read scroll reach and click share together.** High click share on a module with low reach means placement is hiding real demand: test moving it up, alone, with the design and destination unchanged (07's example: a "shop by industry" module with 10.41% of homepage clicks reached by only 30 to 35% of visitors; a reported 18% conversion lift with no statistics). A highly visible module with few clicks means weak relevance, unclear affordance or a less important need. A sharp scroll drop right after one block (04's example: 93% reach above a long paragraph, about a 30% drop after it, only 25% reaching add to cart) means the block is in the way. Confirm intent versus confusion in recordings. Condition: any page with a scroll map and click or Area map. Sources: 07, 04, 03. Cards: [de4dfe536e94] [3043da84ee0c] [09583734387e] [edd07a1a15f6] [9568c40e1d88] [bc5a8130eee9].

**R28. Weight clicks by revenue when the tool allows; otherwise by click share, never by raw counts.** 05 says to weight heatmaps by revenue per click. 03 names heatmap.com for revenue-tied heatmaps (the presenter's partner, disclosed). Clarity gives exact click share per region in Area maps. Condition: any heatmap reading. Sources: 05, 03, 07. Cards: [9568c40e1d88] [9e1368a119b8].

**R29. Recordings: no quota; block 1 to 2 hours; compare engaged with disengaged; stop when patterns repeat; restart after every shipped change.** 04 watched about 100 for some clients and 400 to 450 for others. Sort by clicks and pages high to low (most active) then low to high (least active) and compare on the same page type. Ask "why" about every action. Engagement sorts can mislead: long sessions can mean intent, confusion or idleness. Condition: every research round. Source: 04. `[verify UI]`. Cards: [0b8d2f6cc4d1] [a1a3e1f62713].

**R30. Fix the heatmap screenshot and filter by the biggest device before reading.** If a popup that fires in the first 3 to 5 seconds, or a broken layout, was captured, use Change screenshot and pick another version. Read the device with the most traffic first. Read the scroll map at top, average fold, 75%, 50% and 25%. Condition: every heatmap read. Source: 04. `[verify UI]` `[needs brand data: device split]`. Cards: [09583734387e] [edd07a1a15f6].

**R31. Run a post-purchase survey with at least 2 questions: "What made you purchase today?" and "What made you almost not purchase today?"** 03 calls it "probably single-handedly the most effective way to optimise your store"; the second answer is the objection source for hero copy, FAQs and tests. Group answers into objections (quality, time to results, fit, shipping, guarantee, how to use) and check each is answered near the decision. Buyer-only bias: pair with an exit survey and user tests for non-buyers. Attribution questions ("how did you hear about us") belong to 06-MEA; do not mix them into CRO research. Condition: every store; set it up now if missing (P7). Sources: 03, 07, 05. `[verify UI]`. Cards: [b4505f6c4061] [91410aaad2c8] [f89dbadb9131].

**R32. Run an exit-intent survey for non-buyers.** Questions from 07: "What stopped you from buying?", "What almost stopped you from converting today?", "What's the reason you're exiting the site?" Group into themes: product uncertainty, price, shipping, trust gaps, missing info, comparison needs, unclear fit. Exit surveys hear only those who answer. Condition: any store with enough traffic for responses; treat answers as hypothesis input, cross-checked with recordings and funnel data. Sources: 07, 05. Cards: [f89dbadb9131].

**R33. If no post-purchase survey exists yet, bootstrap with a one-time survey.** Email customers and VIPs a Typeform or similar; 03's incentive example is a chance to win a $250 Amazon gift card. Condition: only until the post-purchase survey is live. Source: 03. `[verify UI]` `[web check: prize-draw and data-privacy rules in the brand's market]`. Cards: [b3b265cf22f6].

**R34. Mine reviews with an LLM, then read the source reviews to confirm.** Export reviews to CSV, prompt for commonalities, tone of voice, buzzwords, key phrases, friction points, objections and feedback that differentiates the product. Answer the objections on the front end; use the unique feedback for one-of-one positioning (02). Condition: 03 makes it non-negotiable at 500 to 1,000+ reviews; 02 uses it at any count for positioning. Sources: 03, 02. `[needs brand data: review export]`. Cards: [fc9b05411697] [cf0bc0f31721] [79bdf741dfc4].

**R35. Run task-based user tests with 5 to 8 people per task.** First prompt: first impressions on landing. Then real tasks: find a suitable product, add it to cart, check out. Watch for missed navigation, misread product details, missed key info, hesitation at cart, checkout doubts. These are small qualitative samples, not conversion estimates. Impartial testers matter: owners cannot judge their own site's first impression (01). Condition: before any redesign hypothesis; after any funnel drop with no obvious cause. Sources: 05 (5 to 8), 07, 03, 01. Cards: [f856d689f3d8] [f375f7ffb264] [c0690a74d2de] [9398191fe1b4].

**R36. Buy from your own store at least every 4 weeks, on mobile, desktop and tablet.** Hand your phone to a 70-year-old and watch them buy. Look for exit popups and cookie banners covering the PDP CTA or the cart button, and for bugs on any device. Condition: every 4 weeks and before every test launch. Source: 03. Cards: [a2d5c573076a].

**R37. Interview customers for motivation, anxiety and the words they use.** Call buyers: why did you buy, was it easy, was anything unclear. Interviews feed messaging hypotheses. Condition: any time survey answers are thin or ambiguous. Sources: 03, 05. Cards: [c0690a74d2de] [fc9b05411697].

**R38. Choose research tools by the jobs you use and your traffic cost, not by feature lists.** Clarity for heatmaps and recordings (free with no data limit at 07's recording time; 03 calls it "quite laggy"). Hotjar when an all-in-one platform (surveys, interviews, funnels) is worth the cost, noting surveys are a separately paid component and plans are priced by daily sessions (Plus $32 a month for 100 daily sessions at recording time; 07's firm moved 300,000 to 400,000-visitor clients to Clarity for cost). Unbundle when you can run several tools: Clarity, Okendo (Shopify surveys), Userbrain ($40 per tester at recording time), GA4 Explore funnels. Before migrating, confirm privacy, retention and any Hotjar feature in active use. Condition: any tool decision. Sources: 07, 03, 06 (lists without choosing), 02 (install Clarity). `[web check: current Clarity, Hotjar, Userbrain, Okendo pricing and limits]` `[needs brand data: daily sessions, normal and peak]`. Cards: [9e1368a119b8] [3728f5d4ae33] [6e48c0e74fe7] [373e2f9d659a] [a56c27356031].

**R39. Set the behaviour review window to the longest representative period.** 04 uses about 6 months; use 90 days if the tool is newer. A big site, merchandising or traffic change makes an older window less representative. Condition: every review. Source: 04. Cards: [e053644d5707].

**R40. Do not pay for a funnel feature you already have.** GA4 Explore builds custom funnels (product view, add to cart, begin checkout, purchase). Confirm ecommerce tracking is configured before reading it (06-MEA). Condition: any tool budget. Source: 07. `[verify UI]`. Cards: [382d08d3f6aa].

**R41. Use competitor and paid-ad landing pages as pattern research only.** Advertisers pay per click, so they are more likely to measure; but a paid ad does not prove a page is profitable. Use for layout and mood; never copy text, logos, products or faces (repo rule). Keep public web research separate from private brand data. Condition: hypothesis generation only. Source: 01 (lead-gen adaptation). Cards: [a8ff5e236f0f].

### 3.4 Writing and ranking hypotheses

**R42. Write every hypothesis in the pre-registration form.** "Because we observed [evidence], we believe [change] will cause [effect] for [segment], measured by [primary metric]. We will know it worked if [metric moves by at least MDE]." Equivalent shorter forms: change, expected outcome, rationale (03); IF [change] THEN [result] BECAUSE [reasoning] (06); change plus reason (04). The rationale must come from data. Condition: every backlog entry; the expected outcome is only possible after research. Sources: 05, 03, 06, 04. Cards: [1b7725e0ff57] [a6c0f42b99a3] [300b03fc0354] [6d2e6fafa7df].

**R43. Cross-check survey themes against funnel and heatmap data, and re-survey after shipping.** An objection that appears in surveys, shows as a drop at the matching step and shows as hunting behaviour in recordings has 3 points of evidence. After the fix ships, check whether the objection declines in new survey answers. Condition: every survey-derived hypothesis. Source: 03 (card additions). Cards: [25979af2691c] [b4505f6c4061].

**R44. Rank the backlog by expected profit, not expected lift.** Expected value = P(win) x expected lift x gross profit per conversion x traffic exposed, minus build cost. Add a ceiling estimate (the most it could be worth if it wins). Keep P(win) evidence-based or the formula gives false precision. A 20% lift on a low-margin, low-traffic page can be worth less than a 5% lift on the hero product's checkout. Condition: every ranking. Source: 05. `[needs brand data: SKU margin, page traffic]`. Cards: [aad25dea9ed9].

**R45. Use a scoring frame to organise ideas, then rank by R44.** ICE (Impact, Confidence, Ease, 1 to 10 each, multiply or average): fast but subjective; whoever pitches the idea scores it, so everything becomes 9/9/9 (05). PIE (Potential, Importance, Ease): forces a look at page traffic. PXL (about 10 to 14 evidence-tied, mostly yes-or-no criteria: above the fold, noticeable within 5 seconds, high-traffic page, backed by heatmaps, user tests, surveys or analytics, build difficulty): least subjective, slowest, best for mature programmes. RICE when audience size varies a lot. CIE is named by 06 with no scale. Condition: PXL-style evidence gating plus R44 is the default; ICE only for small teams building the habit. Sources: 02 (ICE), 03 (PXL, partly described), 05 (all), 06 (PIE, ICE, CIE). Conflict: C10. `[web check: PXL criteria]`. Cards: [a56c27356031] [4a2e3d77d68e] [a6c0f42b99a3] [aad25dea9ed9] [300b03fc0354].

**R46. Prefer changes that are above the fold, noticeable within 5 seconds, and on a high-traffic page.** 80% of 03's agency tests are bigger swings above the fold "because that's really what's going to drive the revenue increase"; this is their bias, not a law. 04's scroll data (a claimed 60% never scroll past the top section; hero reach 93 to 95% on the demo site) explains why. Condition: ranking; does not forbid below-fold tests where research points there. Sources: 03, 05 (PXL), 04. Cards: [4d0785cdcf2b] [aad25dea9ed9] [bc5a8130eee9].

**R47. Order on-page work: clarity and hierarchy, then copy, then offer, then proof, then friction.** 02 ranks these by ICE overall. The offer has the biggest impact ("a bad offer keeps conversion at 0%") but is the hardest, so it comes third; the card caveat is not to let offer problems wait. The same order is also a page structure top to bottom. Condition: when choosing which class of change to work on first for one page. Source: 02 only. Cards: [9e7d2fb74d83] [3965231e76dc] [347f8b289bd6].

**R48. Ship obvious clarity fixes directly; save tests for big swings.** 02: fixing an unclear page has a quick impact and "you're not going to really need to do any split testing". Test later the bigger swings: headline framing (pain or benefit led vs feature led), offer, message-matched page. Condition: the fix is unambiguous and research-backed; if both versions are plausibly viable, R52 applies. Sources: 02; 05 agrees through R50. Cards: [6503bc821ea6] [e02ace8044e5] [55e7424e6d18].

**R49. Re-audit after every shipped change.** Fixing 1 element can expose another. Watch fresh recordings of the new version, re-read the funnel step, re-survey. Condition: after every ship. Sources: 04, 01 (card addition), 03. Cards: [0b8d2f6cc4d1] [bdded17187e0] [b4505f6c4061].

### 3.5 Repair, ship or test

**R50. Repair, do not test, when the current state is objectively defective.** Defective means: page errors, a field that rejects valid input, add to cart failing on one browser, tracking firing twice, a known standard violated, a cart that empties silently (04's example, "had to get fixed straight away"), elements styled as buttons that do nothing, a popup or cookie bar covering the CTA. Do not randomise shoppers onto a broken experience to prove it hurts. Log every repair so it is not re-proposed as a hypothesis. Condition: always. Sources: 05, 04, 03. Cards: [3eca46fe9ba3] [0b8d2f6cc4d1] [9568c40e1d88] [a2d5c573076a].

**R51. Ship without a test when the change is a clarity fix, a proven checkout or landing-page practice at a store under 30 orders a month, or the removal of a blocker confirmed in recordings.** Confirm the ship with fresh recordings and the funnel step rate; treat any before-and-after shift as weak evidence (R55). Condition: the change cannot plausibly hurt, or the store cannot power a test. Sources: 02, 05, 04. Cards: [6503bc821ea6] [0bda3b4d7e04] [0b8d2f6cc4d1].

**R52. Test when both versions are plausibly viable, the better one is unknown, and the test can reach its planned sample in about 2 to 4 weeks.** Most store changes can plausibly hurt conversion, AOV, margin or experience, which is why two-tailed is the default (R64). Condition: everything not covered by R50 or R51. Source: 05. Cards: [3eca46fe9ba3] [00c82f0de25d].

**R53. Use the traffic gates as heuristics, and always compute the real sample size.** Four gates exist in the sources and they are not reconciled (C2, C7):
- Orders per month (05, author synthesis; assumes DTC, 2 to 3% conversion, anonymous traffic). Under 30: research and repairs only; no A/B, A/B/n, bandit or before-and-after with statistical claims (even a 30% lift needs about 120+ conversions per variant). 30 to 300: one bold A/B at a time on the highest-traffic page (home, hero product, cart) aimed at 20%+ relative lift, 2 to 4 weeks, fixed sample computed in advance, micro-conversion primary with purchase guardrail; no tweak tests, no A/B/n, no RPV primary. 300 to 3,000: regular A/B aimed at 10 to 20% on high-traffic pages, conversion rate primary, AOV, margin and return-rate guardrails, 2-week minimum, SRM checks, sequential engines; RPV primary and 2 to 3 arms borderline; no sub-5% lifts. 3,000 to 20,000: A/B/n, bandits for short campaigns, winsorized RPV, CUPED, pre-registered segments, 5 to 10% lifts on hero pages; no sub-2 to 3% lifts without long runtimes. 20,000+: full programme, 2 to 5% MDE, revenue and gross-profit primaries, always-valid monitoring, concurrent tests with FDR control, holdouts for surprising winners, A/A tests.
- Sessions per month (03, agency's 2025 internal update). Under about 300,000: big swings only; no button-colour, single-hero-image or text-snippet tests. Over about 300,000, with "good enough" conversion rate and order count (undefined): comprehensive CRO with 4 to 8 isolated tests a month.
- Visitors per month (05, heuristic). Under about 100,000: bold changes aimed at 10 to 20%+ effects on the highest-traffic pages.
- Online revenue (02, opinion). Micro-tweaks chasing about 0.1% lifts pay only at about $40M+ online.
Condition: use the orders band first because it maps to conversions per variant; use the others as sanity checks. Sources: 05, 03, 02. Cards: [0bda3b4d7e04] [67f74e89d43e] [91c7b6d064ec] [3d52bd4930fe] [365c9ff30a24] [e7dfd865fcfd] [e02ace8044e5] [699a7cd5ac4c].

**R54. Below the testing threshold, "test bigger, not more".** Bold changes aimed at 10 to 20%+ effects, on the highest-traffic pages, one at a time, backed by qualitative research; re-test surprising big winners with a holdout. One bold homepage test teaches more than 10 micro-tests on low-traffic category pages (05, citing SplitBase). 03's big-swings list for stores under 300,000 sessions: landing-page formats (listicle, sales page, advertorial), PDP redesigns from data, offer tests every month (buy 1 get 1, 3 for the price of 2, build-a-bundle, price points), free-shipping and price tests in cart, post-purchase upsells and surveys, ad-creative alignment. 02's list of what is worth testing: headline framing, offer, message-matched page. Condition: stores under the gates in R53. Sources: 05, 03, 02. Cards: [67f74e89d43e] [365c9ff30a24] [2d977920a505] [d12e614c0b4e] [e3ba0fb7d6f6] [e02ace8044e5] [55e7424e6d18].

**R55. Before-and-after comparisons are biased, not just noisy.** They confound the change with time: seasonality, promotions, weekday mix, traffic-source shifts, news. Use only for big structural changes where the effect dwarfs noise, with equal comparable periods and conditions held constant. Treat a clear, stable, explainable shift as weak evidence and confirm later with a randomised test. 06's difference-in-differences needs a comparable control group and belongs to 06-MEA. Condition: any non-randomised read, including checkout repairs on standard Shopify. Sources: 05, 06. Cards: [062507c94ee4] [04a08881ac09].

**R56. Do not add arms to test more ideas at once.** A/B/n needs the full per-variant sample for every arm, so total traffic scales with the number of arms. Multivariate only at high volume. Condition: A/B/n borderline at 300 to 3,000 orders a month with 2 to 3 arms; routine at 3,000+. Below that, "sequential A/B tests" (one after another, 06's meaning) are the safer choice. Sources: 05, 03, 06. Conflict: C12 on the word "sequential". Cards: [3b20905bfc58] [4d0785cdcf2b] [300b03fc0354].

**R57. Use A/B tests for durable decisions and bandits for short tactical ones.** A/B gives a clean causal read before a lasting change (redesign, pricing logic, navigation, checkout). Bandits (Thompson sampling, UCB) shift traffic to the better arm in real time and fit headlines, seasonal promos, banner creative and recommendations where showing the loser is costly and the window is short; they minimise regret, do not estimate effects well, and need sticky bucketing so returning users stay on one arm. Condition: routine bandits from about 3,000 orders a month; lower only for short regret-minimising campaigns. Source: 05 only. Cards: [3b20905bfc58].

**R58. Do not run 2 tests on the same page area at the same time.** A homepage test and a cart test can run together; an above-the-fold and a below-the-fold test on the same page can too. Many concurrent tests need FDR control (05, 20,000+ band). Condition: every test calendar. Sources: 03, 05. Cards: [7d481c590b57] [4d0785cdcf2b] [1f26cd618e2d].

### 3.6 Sample size and duration

**R59. Size every test from the minimum detectable effect, never from a magic conversion count.** Evan Miller's rule: n = 16 x sigma^2 / delta^2 per variant, where delta is the absolute effect and, for a conversion rate, sigma^2 = p(1-p). The 16 bakes in alpha 0.05 two-sided and 80% power. Halving the MDE quadruples the sample. Set the MDE to the smallest lift worth shipping, thought through in gross profit, not the smallest lift possible. Check whether the calculator wants relative or absolute (2% to 2.4% is +0.4 points absolute, +20% relative). Condition: every test. Source: 05. `[needs brand data: baseline conversion rate per page and device]`. Cards: [00c82f0de25d].

**R60. Think in conversions per variant.** At 80% power and 95% confidence the conversions needed per variant depend mainly on the relative MDE: about 3,830 for 5%, about 1,000 for 10%, about 260 for 20%, about 120 for 30%. 02 agrees on the anchor: about 1,000 conversions per variant for a 10 to 20% lift, which at 2.5% conversion is about 40,000 sessions per variant and 80,000 for a simple A/B. 03 says its agency runs 50,000 to 100,000 sessions "through a test", without saying per variant or total. Condition: always state per variant, then multiply by arms. Sources: 05, 02, 03. Conflict: C3. Cards: [00c82f0de25d] [699a7cd5ac4c] [4d0785cdcf2b].

**R61. Reject magic numbers.** "400 conversions a month" powers only a 30 to 40% lift in a month. "200 conversions per variant for a 20% lift" is roughly right but 250 to 260 is safer at 80% power. The HubSpot "20,000 per group" rule is email-oriented and equals about 400 control conversions at 2%. Condition: any brief or vendor claim that quotes a flat number. Source: 05. Cards: [00c82f0de25d].

**R62. Multiply by arms, divide by weekly eligible traffic on the tested page, round up to whole weeks.** Use traffic on the page or path, not sitewide sessions. If the runtime is unreasonable: raise the MDE (bolder change), move to a higher-traffic page, switch to a faster primary metric with purchase as guardrail (R8), or drop to research only. Condition: every test. Source: 05. `[needs brand data: weekly sessions on the tested page]`. Cards: [00c82f0de25d] [5fae1beab1ba] [67f74e89d43e].

**R63. Run at least 1 full week, in practice 2, and also reach the planned sample.** Weekends convert differently and buyers differ by day; 2 weeks captures one cycle of returning visitors (Kohavi, via 05). Cover each weekday twice (2 Mondays, 2 Tuesdays, and so on) so a one-day shock such as a competitor's Monday sale cannot trigger a wrong kill (03). Typical runtime 2 to 4 weeks; 03's comprehensive programme uses at least 2 weeks. Hitting significance early is not a reason to stop. Two weeks is a minimum, not a replacement for sample math. Condition: every test. Sources: 05, 03, 06. Self-contradiction: 02 suggests a 7 to 10 day delivery-time display test, which is short against 02's own sample math (C19). Cards: [5fae1beab1ba] [7d481c590b57] [300b03fc0354] [27026398ed8a].

**R64. Two-tailed is the default.** One-tailed reaches significance faster but only tests one direction. Use it only when a negative result would trigger the same action as a null (keep control either way), document that before launch, and recompute the sample because standard tables assume two-sided. It is never a shortcut to hide downside. Condition: every brief. Source: 05. Cards: [517a8bce6324].

**R65. Remove contamination from the test population.** Klaviyo or other retention sends spike conversion, and an on-page split tool forks email traffic into the test too. Options from 02: send tests custom landing pages that receive only cold Meta traffic; or fork traffic at the Meta ad-set or campaign level `[verify UI]` (set-up in 11-ADC). Account for multi-click journeys: on 02's big client brands about 1.5 Meta clicks per conversion on average, so about 50% of buyers click more than once and may see both variants without sticky bucketing. Condition: any test on a page that receives both paid and owned traffic. Source: 02 only; 05 supports through its SRM and contamination checks. Cards: [699a7cd5ac4c] [370ed8c02e34].

**R66. Randomise properly, keep allocation balanced, and use sticky bucketing.** The randomisation unit is the user; returning users must see the same arm. Condition: every test and every bandit. Sources: 03, 06, 05. Cards: [4d0785cdcf2b] [300b03fc0354] [3b20905bfc58].

### 3.7 Validity checks and stopping rules

**R67. A p-value is valid only under its planned stopping rule. Do not peek.** Fixed horizon means: fix the sample in advance, look once at the end. Stopping at the first p < 0.05 while checking continuously turns a nominal 5% false-positive rate into 26.1% in the worst case (Evan Miller); running 2 weeks and then checking daily for 2 more weeks turns it into about 17% (Kohavi and Sonnet); Etsy's simulation found over 50% chance of a false difference after 500 observations. The alternative is a validated sequential engine (mSPRT always-valid p-values, GAVI confidence sequences, group sequential with alpha spending, corrected alpha) whose stopping rule you follow and nothing else. 02: "peeking daily and stopping at significance inflates false positives"; do not call a test after 2 weeks and 100 conversions. Condition: every test. Sources: 05, 06, 02, 03. Cards: [e3ee87a025c5] [300b03fc0354] [699a7cd5ac4c] [c54652571336].

**R68. Bayesian tools are not immune to peeking.** Peeking every 100 observations and stopping at P(A > B) > 0.95 gave about an 80% false-positive rate in Molas's simulation (2025). Most commercial "Bayesian" tools use flat priors, which makes them close to frequentist but less transparent. If you cannot state the prior and whether the stopping threshold is protected against optional stopping, you cannot fully interpret or reproduce the result; treat it like a peeked frequentist test. Condition: any Bayesian engine (VWO SmartStats, AB Tasty, Eppo). Source: 05. `[web check: vendor stats engine docs]`. Cards: [e3ee87a025c5].

**R69. Choose the engine before writing the brief.** If you can estimate the expected sample well: fixed horizon or group sequential design (more powerful; Spotify's view). If you cannot, or stakeholders will watch daily: an always-valid method (mSPRT, GAVI, corrected alpha), accepting wider intervals. Confirm the tool's current engine in vendor docs. Condition: every brief. Source: 05. `[web check: vendor stats engine docs]`. Cards: [e3ee87a025c5].

**R70. Require statistical power, not just significance.** 03: significance without power is like 3 coin flips giving 2 heads; power means enough data that the result will repeat. Use a tool that reports significance, but size the test yourself. Condition: every test. Sources: 03, 05. Cards: [c54652571336] [4d0785cdcf2b] [00c82f0de25d].

**R71. Check sample ratio mismatch early and often.** Chi-square goodness-of-fit on users (the randomisation unit), not page views. Flag at p < 0.001 (Kameleoon's threshold). A designed 50/50 that returns 50.3/49.7 on a large sample can already be a mismatch. About 6% of Microsoft experiments show SRM. If present, stop trusting the result until the cause is found (bots, redirects, tracking, browser-specific failures). Condition: every test, at launch and at each planned look. Source: 05 only. Cards: [370ed8c02e34].

**R72. QA every test 2 or 3 times on real devices before launch, and confirm tracking fires in both arms.** A bug makes a winner look like a loser. Compare event counts per arm with orders in the store backend during the test. If tracking breaks mid-test, invalidate the read. Condition: every launch. Sources: 03, 05. Cards: [4d0785cdcf2b] [370ed8c02e34] [3eca46fe9ba3].

**R73. Check for flicker on a slow mobile connection.** In client-side tests the original can render before the variant. Flicker hurts UX and can inflate the effect by drawing the eye. Anti-flicker snippets hide the page for up to 3 to 4 seconds by default (DebugBear). AB Tasty says there is "no miracle fix". Prefer server-side or Shopify Rollouts for speed-sensitive paths. Condition: every client-side test. Source: 05 only. Cards: [370ed8c02e34] [7c932a3b4986].

**R74. Filter bots and check the marketing calendar for overlaps.** Promotions, holidays and traffic-mix shifts inside the window confound the read. Note the confound in the record and consider a re-run. Condition: every test window. Sources: 05, 03. Cards: [370ed8c02e34] [062507c94ee4] [7d481c590b57].

**R75. Pre-register segments and count your metrics.** Pre-register device, paid vs organic, new vs returning. Mobile and desktop can move in opposite directions, so a blended win can hide a mobile loss. Slicing after the fact until a winner appears is p-hacking; post-hoc slices only seed new tests. Multiple metrics inflate error: 1 metric 5%, 2 about 10%, 3 about 14% at alpha 0.05 each; apply Bonferroni or FDR (05 does not say which to prefer). 06 adds: segment only when the sample supports it and decide on the pre-declared overall metric. Condition: every brief and readout. Sources: 05, 06. Cards: [1f26cd618e2d] [c076b110d253].

**R76. Never kill or call a test on one bad or good day.** Early cumulative deltas are noisy. Condition: every test. Sources: 03, 05. Cards: [7d481c590b57] [5fae1beab1ba].

**R77. Apply Twyman's law: a surprising number is usually wrong.** A 50%+ lift, or hundreds of percent, is more likely an instrumentation bug, SRM, contamination, bot skew, tracking failure or promo overlap than a discovery. Realistic lifts: 1 to 5% on mature pages, 10 to 20%+ on early or unoptimised pages. A small-sample early-stopped winner (200 conversions instead of 2,000) inflates the lift (winner's curse). A case study without baseline, sample, runtime and validity checks is hypothesis material only; that applies to every case number in this playbook, including 07's 18% lift, 01's 60% ADT uplift, 03's monthly revenue figures and 06's case table. Condition: every readout and every case study. Sources: 05, 06, 07, 01, 03. Cards: [370ed8c02e34] [8dc46d4893e1] [300b03fc0354] [de4dfe536e94] [8121c53ef9d8].

**R78. Check novelty and primacy with daily plots, but be sceptical.** Novelty: a temporary bump because the change is new. Primacy: returning users dip then recover. Plot the daily effect and compare first-exposure with repeat-exposure conversion. Kohavi found most suspected effects are artifacts of noisy early cumulative deltas. Judge on the stable period. No threshold proves a real novelty effect. Condition: any test with returning traffic or a visible design change. Source: 05. Cards: [5fae1beab1ba].

**R79. Validate the platform with an A/A test when you start a programme or change tools.** A significant A/A difference means fix the platform before trusting tests. Condition: 05 lists it for the 20,000+ band; it is sensible at any volume when a tool is new. Source: 05. Cards: [0bda3b4d7e04].

### 3.8 Reading and closing a test

**R80. Report the effect with its confidence interval and decide against the MDE and business value, not against p < 0.05 alone.** "Significant" does not mean 95% likely real: if only 10% of ideas truly work and power is 80%, roughly 1 in 5 significant wins is a false positive. Compare the interval with the MDE, incremental gross profit, build cost and guardrails. Condition: every readout. Source: 05. Cards: [70db51ffb976].

**R81. A fully powered inconclusive test is a result.** It is evidence the effect is smaller than the MDE. Do not extend it to chase significance (that is peeking). Ship neither, or the cheaper and simpler version. A test that is clearly negative after 2 weeks: stop, do not wait for a reversal, fail fast. Condition: every inconclusive or negative readout. Source: 05. Cards: [70db51ffb976].

**R82. Replicate or hold out a surprising large win before banking the revenue.** Condition: any win above the realistic band in R77, or any win the team did not expect. Sources: 05, 06. Cards: [70db51ffb976] [370ed8c02e34] [f671352f5b6e].

**R83. Read the pre-registered device split before shipping.** If mobile and desktop move in opposite directions, do not ship blind; investigate. Condition: every readout. Source: 05. Cards: [1f26cd618e2d].

**R84. Run an LTV check before scaling a winning angle or page.** Dark patterns and over-claiming lift front-end conversion and lower CAC, then raise returns and chargebacks and cut repeat rate and lifetime gross profit (02's example: a supplement angle on eyesight that scales on Meta while customers feel no difference). Check returns, chargebacks, repeat rate and 365-day LTV by angle. Condition: any win driven by a claim, an angle or urgency. Sources: 02, 05 (guardrails). `[needs brand data: returns and LTV by acquisition angle]`. Cards: [dad9c85ea261] [1f26cd618e2d].

**R85. Ship winners and protect them.** Keep a live-winner register and check it after theme changes, app changes or team changes. 03's client saw new leadership overwrite winning tests; "a win will usually stick into perpetuity", so retained wins compound. Condition: every shipped winner, reviewed at least quarterly. Source: 03. `[needs brand data: past test log and which winners are still live]`. Cards: [f09cfbc3ef44] [bbab5b1b0329].

**R86. Expect most tests to lose, and record why.** 05's best-sourced anchor: about 10 to 20% of well-run tests produce a significant winner (Microsoft about 33% in 2009; Bing about 15%; Google Ads, Booking and Netflix about 10%; Airbnb Search about 8%; Optimizely 12% on primary metric across 127,000 experiments; VWO about 14%; CXL/Convert about 20%). 03 says 30 to 35% is "very, very well" while its own showcase record is 13 winners out of 135 tests (about 9.6%). 06's "60%+ win rate" is a "decisive" rate (wins over wins plus losses), not a significant-per-test rate. Learn why tests lose and feed that into the next hypothesis. Condition: never set a win-rate target above 05's anchor without stating the definition and sample. Sources: 05, 03, 06. Conflict: C4. Cards: [8dc46d4893e1] [bbab5b1b0329] [300b03fc0354].

**R87. Keep one experiment log for tests, repairs and holdouts.** Institutional memory stops re-running losers and flags surprising winners for replication. At Booking.com's scale "the bottleneck is not running tests but not fooling yourself with them". 06 calls the same thing a causal knowledge base: question, method, result with interval, decision. The record format is in P18 and section 9. Condition: every test, repair, holdout and causal analysis. Sources: 05, 06, 03. Cards: [70db51ffb976] [2b951af15841] [f09cfbc3ef44] [3eca46fe9ba3].

**R88. Winners do not add up.** Shipping 20 winners does not make conversion "20x better": interaction effects (a CTA that won alone may not work with a new layout that also won), cumulative drift (buyer mix, competition and seasons change), and attribution confusion (after 20 changes you cannot say which ones moved the 8%). Report programme value from a holdout (R91), never as the sum of test lifts. Condition: every programme report. Source: 06. Cards: [f671352f5b6e].

**R89. Verify after shipping.** Watch fresh recordings of the new version, re-read the funnel step, and re-survey for the objection the change addressed. Condition: every ship. Sources: 04, 03. Cards: [0b8d2f6cc4d1] [b4505f6c4061].

### 3.9 Holdouts and incrementality

**R90. Match the measurement design to the question.** "Did this specific test win?": A/B test. "Does this feature (popup, recommendations, personalisation) add net revenue?": feature holdout. "Has our whole CRO programme created value?": CRO programme holdout. "Does retargeting or Meta drive incremental revenue?": user-level or geo holdout (11-ADC). "What was the impact during peak season with no clean control?": BSTS or difference-in-differences (06-MEA, specialist). "We cannot randomise": synthetic control, propensity matching, regression discontinuity (06-MEA, specialist). Document question, method, result with confidence interval, business decision. Condition: before any measurement is designed. Source: 06 only. Cards: [0eca60fd9161] [2b951af15841] [04a08881ac09].

**R91. Prove programme value with a persistent programme holdout.** Randomly assign a small share of all traffic (06's example: 5%) to see the site as it was before the programme; everyone else gets every shipped winner; keep assignment stable for the period (example: 90 days); compare conversion rate and RPV at the end; report net lift with a confidence interval. Card caveats: 5% and 90 days are illustrative, compute whether traffic can detect a meaningful effect first; withholding major usability, accessibility or policy fixes from a permanent holdout raises operational and ethical concerns, so apply repairs (R50) to everyone. Condition: any programme that claims cumulative value; 06 gates user-level holdouts at over 100,000 monthly visitors (C7). Source: 06 only. `[needs brand data: monthly visitors, logged-in share]`. Cards: [f671352f5b6e].

**R92. Measure features by net revenue with a feature holdout, not by their own engagement metric.** Randomly hold out a group that never sees the feature (examples: popup 90% exposed / 10% holdout; recommendations 5% holdout). Tag and track both groups to purchase and, where relevant, repeat purchase. Decision metric RPV; support metrics conversion rate, AOV, opt-in rate. Look for trade-offs: more opt-ins but fewer purchases; more clicks but no bigger baskets. Segment only when the sample supports it; decide on the pre-declared overall metric. Keep the holdout long enough to capture delayed purchases. Condition: every popup, recommendation module, personalisation layer and cart-recovery flow. Source: 06 only. Cards: [c076b110d253].

**R93. Traffic gate for holdout designs: over about 100,000 monthly visitors for user-level holdouts, geo holdouts and switchbacks.** Below that, use longer holdouts or a causal method with a stated assumption. This 100,000 is 06's gate for holdout designs; 05 uses the same number for "bold changes only" A/B testing. They are different rules (C7). Condition: rough guidance; compute detectability. Source: 06. Cards: [0eca60fd9161].

**R94. Any causal method must state its identifying assumption and challenge it before the output is trusted.** Parallel trends (difference-in-differences), valid threshold (regression discontinuity), no unobserved confounding (propensity matching), pre-period similarity (synthetic control; 06's Hourglass geo example matched markets at 0.96 to 0.99 correlation). These need specialist implementation and live in 06-MEA and 11-ADC. Condition: whenever randomisation is impossible. Source: 06. Cards: [04a08881ac09] [e353aade03ae].

**R95. Judge cart-recovery flows against a holdout, and do not make discounts the only answer.** Frequent discounts can train shoppers to abandon on purpose. 06's timing framework (first contact within 1 hour, escalation over 72 hours) is a framework to test, not a rule. Flow build belongs to 14-EML. Condition: any abandonment flow. Sources: 06, 02. Cards: [e46b405d55df] [3163cc34fa79].

### 3.10 Page-level rules that seed hypotheses

These rules tell the agent what to look for on each page type. Design and copy execution live in 07-LPG. Every case number here is an example with no sample size or duration.

**Home**

**R96. The homepage orients; it rarely converts.** Its job is to route visitors to the right products fast and build credibility. Hero passes a 3-second test; 1 clear conversion offer (newsletter with a concrete incentive); simple navigation with clear category entry points; curated selection. 06's reported experiments: a broad head-to-toe assortment cut add to cart 6.07% and CTR 10.4%; bestsellers for visitors with no history lifted CTR to product pages 23.01% versus static featured products; personalised recommendations lifted CTR 136% versus static. 07's pattern: a high-click, low-reach module moved up. Condition: homepage hypotheses; check first what share of sessions even start on the homepage. Sources: 06, 07, 03. Cards: [5e578ca91bcc] [de4dfe536e94] [1823c8a7c180].

**R97. Design the menu as a guide, not a directory.** New visitors open the mega menu to see what is on offer (03's recordings). Put a bestsellers carousel at the top, icons and some social proof, and move non-money links (contact, reviews, FAQs) to the bottom. Use customer words, not jargon; do not sort alphabetically; past about 6 options people forget the first (01's phone-menu analogy); a click should open a useful page, not an intermediate "home" page; keep the menu icon familiar (01's law-firm site with a quirky hamburger had a "massive" bounce rate). Condition: navigation hypotheses. Sources: 03, 01 (lead-gen adaptation for the analogy). Cards: [033531683bba] [1823c8a7c180] [f5942adec72b] [d4484bf96e29].

**Collection**

**R98. Define the collection page's job before designing it: browsing, deciding or buying.** 06: on browsing pages, Add to Cart buttons create decision conflict because the visitor is still asking "what options exist"; visitors want clear subcategories, visual hierarchy, filters that narrow without overwhelming, and click-through to PDPs. 03: for consumable repeat-buy products, putting the price on the collection card button and allowing add to cart from the grid was a winning test for Boom ($30,000 a month with labels combined); "doesn't work with every single product or niche". Condition: add-to-cart-from-grid is a hypothesis for repeat-buy consumables with returning traffic, not for first-time browsing. Sources: 06, 03. Conflict: C14. Cards: [1e03a58f6fe1] [6f635b9d003d].

**R99. On mobile, show products above the fold and keep controls in the thumb zone.** 03: a 2 x 2 grid, 4 products visible; if a hero banner or text block hides them, "start again". 06: hero banners no more than 30 to 40% of the first view; the first 2 rows get most taps; tap targets at least 44px; a sticky bottom filter bar or floating "Filter" pill (06 claims 75% of mobile users abandon if they cannot refine quickly; unsourced). 04: shoppers scrolling back to the top to reach a filter is a sticky-filter hypothesis, confirmed across several sessions first. Labels (bestseller, new, low in stock, trending) on a few products only, never all; must reflect real data. Condition: mobile collection hypotheses. Sources: 03, 06, 04. Cards: [6f635b9d003d] [1e03a58f6fe1] [11e64288067b].

**R100. Keep promo messaging consistent from collection to PDP, and from ad to page.** When the collection promo is reinforced on the PDP, add to cart is more likely (06). Condition: any promo. Sources: 06, 02. Cards: [1e03a58f6fe1] [a5cf6ee34972].

**PDP**

**R101. A PDP must answer 4 questions above the fold on a phone: what is it, why this one (unique mechanism), why now, why trust you.** Order elements by persuasive weight: value proposition, proof, price, CTA. Leave SKU details, size and quantity pickers out of the hero (handle in cart, or default to the larger size or a bundle). Add a scroll cue so the page does not look finished. 02's recap says "core five questions" while its body lists 4 (C19). Condition: every PDP audit, checked on a phone. Source: 02 only. Cards: [bb761687ad68] [36f1d8130259] [e76096210c1d] [e10616e94452].

**R102. Put purchase drivers next to the buy box.** 03's Boom PDP test (nearly $40,000 a month, +$0.50 per paid PDP visitor, 5 changes combined): reviews and stars moved higher, visible savings, sticky add to cart, gallery thumbnails instead of dots, gallery used as a mini landing page (benefits, testimonials, UGC, video, guarantee), money-back guarantee un-collapsed next to the CTA for an older audience. 03 claims more people swipe the whole carousel than scroll the whole page (no data). 06: Add to Cart above the fold, trust signals and social proof near the decision. 01: make the conversion goal the most visible element (Amazon's bordered buy box). Condition: PDP hypotheses; do not credit any single change with the combined case result. Sources: 03, 06, 01. Cards: [116d1016fa3b] [fc7c739888fc] [e18bae3af3dd] [a360a5796cb7].

**R103. Price, shipping cost, returns and a realistic delivery estimate must be easy to find, with consistent currency and origin cues.** 01's Shark Proof teardown: a "$75 free shipping" note on a pounds price made a UK buyer worry about US shipping time; delivery times shown inconsistently; review dates clustered. Condition: every PDP audit. Sources: 06, 01, 02. Cards: [fc7c739888fc] [e24c4415d85e] [27026398ed8a].

**R104. Proof: get reviews first, sort media first, match proof to the claim, and show a believable distribution.** 02: going from 0 to about 100 reviews roughly doubled conversion on his own 2019 to 2020 stores, mostly in the jump from 0 to 80, beyond that "immeasurable"; image and video reviews are worth far more than text, auto-sort them first; 5 hyper-relevant reviews beat 400 generic ones; a 4.8 reads as more genuine than 5.0 (opinion). 06: a mix of 4 and 5 stars feels more real than a wall of 5 stars. 01: review volume often beats average rating (seminar exercise); build volume by sending review links; if you have 2 reviews, use the 2; specifics ("at age 50", "dropped 30 lbs") build belief and must be true and permissioned. Incentivise photo reviews only where legal (02: $10 gift card or cash back for submitting a review with an image; you can reward submitting, not a rating). Condition: proof hypotheses; volume matters up to about 100 reviews (02), relevance after that. Sources: 02, 06, 01. `[needs brand data: review count, media-review share]` `[web check: incentivised-review rules in the brand's markets]`. Cards: [a507cc86ec03] [0a1f9ee893a3] [1d5e67c73cdd] [e18bae3af3dd] [affc22a52d1b] [3ef8c77c4464] [f95f16ca7611] [1cdf5f4a3630].

**R105. Trust badges: remove generic security seals unless a test says otherwise; test specific policy and proof statements beside the CTA.** 02: footer security seals "do absolutely nothing to close anyone"; guarantees and returns are table stakes but useful as risk reversal after the proof. 03: winning designs include a "trust policy bar" (easy returns, support, satisfaction guarantee, money-back guarantee) in cart and trust seals by the CTA (money-back guarantee, "over 10,000 happy customers", vegan-friendly, made in the US, "featured in" logos, only if true). 06: one DTC brand moved trust icons inline next to Add to Cart and reported +18% revenue per session after 3 weeks; 06 also lists payment trust signals at a 40.5% test win rate (unsourced). 01: secure-checkout logos, awards and Trustpilot badges as credibility. Condition: the disagreement is about generic security seals versus specific policy and proof statements; see C1 for what to do. Sources: 02, 03, 06, 01. Conflict: C1. Cards: [cdd5df001439] [1d5e67c73cdd] [84ebf548938d] [4653645c47ac] [e18bae3af3dd].

**R106. A long text block between the shopper and add to cart is a hypothesis to cut or restructure it.** 04's example: 93% reach above the paragraph, about a 30% drop right after it, 25% reaching add to cart. 03: turn description blocks into benefit-driven bullets, bold key words, outcomes not features. Long copy is not always bad; detailed products may need it; the problem is presentation that blocks scanning. Condition: scroll map shows a steep drop after one block, not normal end-of-page decay. Sources: 04, 03, 02. Cards: [edd07a1a15f6] [116d1016fa3b] [790f6b3372c2].

**R107. Answer the top "almost did not buy" objection in the hero or beside the CTA, and build the FAQ from real objections.** 03: a sandal brand's answers were about leather quality, so the hero was rewritten around craftsmanship, sourcing and handcrafting ($77,000 a month reported); a supplement's "did not know how long results take" becomes a "results in the first 6 weeks" section below the fold (illustration). 02: FAQs answer the top reasons people do not buy, not shipping policy or brand story. 01: handle objections to the first step, not only to the product (will a salesperson call, do you serve my area); state exactly what happens after the click. Condition: every PDP and landing page. Sources: 03, 02, 01 (lead-gen adaptation). Cards: [d8e9c11154e5] [109929fb0656] [91410aaad2c8] [499b4e67252a] [182f13121915] [f62861431f31] [16c2667cb67c].

**R108. Keep message match from ad to page, and send cold unaware traffic to a landing page, not a plain PDP.** If the ad changes persona or offer, use a separate page; if it changes angle (unique mechanism), keep the page on that 1 angle rather than listing every benefit (02's collagen example: arthritis as benefit 9 of many converted worse). Match hero, mechanism, objections, testimonials and CTA to the ad's promise and wording. 03: sending paid traffic straight to PDPs, homepages or collection pages "is leaving money on the table"; a pre-sell listicle for Boom reported $20,000 a month and allowed cold-traffic scaling. Prioritise concepts with meaningful spend, since each page adds build and QA. Condition: every paid concept. Sources: 02, 03. `[needs brand data: active ad concepts by persona, offer, angle]`. Cards: [a5cf6ee34972] [19d7eed88979] [322887ac21c3] [aa0e72b56778] [2d977920a505] [6695665021f2].

**R109. Headline framing (pain-led or benefit-led versus feature-led) is one of the few above-the-fold changes worth a split test.** Big swing, seen by everyone. Condition: stores with enough traffic per R53. Source: 02. Cards: [55e7424e6d18].

**R110. Number of CTAs: many repeated CTAs are fine only if they all do the same thing; competing offers add friction.** 01 praises 7 or more identical "get in touch" access points on 1 page including a sticky bar. 03 wants "one clear call to action" on a sales-page hero and to explain what happens on click ("shop bestsellers" if unsure). Condition: repeat 1 action; never stack different offers. Sources: 01 (lead-gen adaptation), 03. Conflict: C6. Cards: [a360a5796cb7] [4653645c47ac].

**R111. Popups in the first 5 seconds, chat widgets over add to cart, and cookie bars over the cart button are repairs, not tests.** They show up as rage clicks (04) and in self-purchase audits (03). Condition: always. Sources: 04, 03. Cards: [9d9871ee324b] [a2d5c573076a].

**Cart**

**R112. Remove the discount-code box from cart when no promotion is live; keep it working when one is.** Shoppers leave to search "[brand] discount code", hit coupon sites and popups, and do not come back; worse for older shoppers. Part of a $40,000-a-month combined cart result (03). Condition: any store with a visible coupon field and no live promo. Source: 03 only. Cards: [19e8c5c27387] [84ebf548938d].

**R113. Add purchase reassurance in the cart: returns, support, satisfaction or money-back guarantee.** 03's trust policy bar replaced the coupon field. See C1 for the badge debate. Condition: cart hypotheses. Source: 03. Cards: [84ebf548938d].

**R114. Use the cart drawer to raise contribution, judged on RPV, not AOV alone.** Free-shipping progress message ("spend $12 more for free shipping"), gift-with-purchase thresholds that unlock as spend rises, 1-click upgrade from the single item to a routine bundle, in-cart upsells (03's clothing client: nearly $60,000 a month with AOV stuck at $60 to $80 before). Set the free-shipping threshold above typical carts (02's examples $66 and $75; "most brands set the threshold too low"); price bundle discounts from fulfilment savings (02: $136 value, $122 price, $14 equal to the shipping and fulfilment of 3 separate orders). Condition: offer hypotheses; check margin first. Sources: 02, 03. `[needs brand data: fulfilment cost per order, typical cart value]`. Cards: [6baa7dce36c7] [23f840cd83b0] [c6984ab0f0cc] [e3ba0fb7d6f6] [d5a74f7edadd] [1e7c5456a957].

**R115. A multi-buy offer below add to cart ("buy 3, save 20%") fits low-price items people own several of, not luxury.** 03's sunglasses client ($30 to $40 products) reported over $180,000 a month. Condition: consumables and multiples. Source: 03. Cards: [e3ba0fb7d6f6].

**Checkout**

**R116. Keep total checkout extras under about 10% of AOV and show them before checkout begins.** 02: sum shipping, tax and fees; on a $100 order stay under $10; "internally" found lower has no material gain; shipping collected up to about 10% of AOV had no material conversion effect in his own 2019 to 2020 tests (02 also states this as "10% of total revenue", C19). Baymard as cited: 39% of abandoners leave because of late extra costs (02, 06); 21% slow delivery; 19% card trust; 19% forced account (06 gives 16 to 24%); 18% checkout too long; 15% returns; 14% total not shown up front. Show the total early; no drip pricing (02's IM8 example: monthly price on page, quarterly-only in cart); if tax is included but shown as a line, label it. Condition: every checkout audit. Sources: 02, 06, 05. `[needs brand data: checkout extra costs as % of AOV]` `[web check: current Baymard figures]`. Cards: [27026398ed8a] [8b2d9df04dfb] [3163cc34fa79] [d4104b13110f].

**R117. Guest checkout is the default and prominent; collect email during it and build the account after purchase.** Baymard as cited by 06: 62% of sites do not make guest checkout prominent enough. 02 "believes" forced accounts may be a Shopify default; check. Condition: every store. Sources: 02, 06. `[verify UI]`. Cards: [94a63f9f740b] [d4104b13110f].

**R118. Put express payment first and offer the market's methods.** Shop Pay, Apple Pay, Google Pay at the top; UPI in India; recognisable payment brands; no redirects or context switches. Condition: every checkout. Sources: 02, 06. `[verify UI]`. Cards: [a5c46083a30f] [d4104b13110f].

**R119. Cut fields to the strictly necessary, enable autofill, add progress indicators on multi-step flows.** 02: make fields optional, shorten the address block. Baymard average is 11.3 checkout fields (05). Form-field evidence from lead-gen sources, adaptation only: 04's B2B forms lose most people by the 3rd or 4th field and 4 or fewer is "the sweet point", phone number causes "a substantial drop off"; 01's HubSpot study showed conversion falling from 3 to 10 fields and also lower at 1 to 2 fields, with free-text boxes worst; ask only for what you will use. Condition: checkout and any capture form. Sources: 02, 06, 05, 04, 01 (adaptation). Conflict: C18 (01 allows deliberate friction for costly free services). Cards: [c6984ab0f0cc] [d4104b13110f] [4ae56138baa5] [8accb09355e6].

**R120. State the returns policy at the decision point, but do not rush to free returns, above all in fashion.** Test and accept some loss only if more profitable. Condition: returns hypotheses. Sources: 02, 06. Cards: [1e401776f34b] [d4104b13110f].

**R121. One-page versus multi-step checkout is a test, not a rule.** 02's agency data says one-page converts "a little" better (data not shared). 06's marketplace switchback (12 days, rotating hourly) found the 3-page checkout raised AOV 2.1% at 98% significance and improved RPV, "flipping" the fewer-steps advice; the card calls it context-specific. Condition: Shopify Plus or server-side only (R123). Sources: 02, 06. Conflict: C15. Cards: [c6984ab0f0cc] [04a08881ac09].

**R122. Slow delivery: get faster options before you consider hiding dates.** 02 suggests a 7 to 10 day split test of hiding delivery times, noting hiding adds ambiguity and lowers conversion. That runtime is short against 02's own sample math, and hiding may conflict with consumer disclosure rules. Condition: only with legal review and a properly sized test. Source: 02. `[web check: delivery disclosure rules]`. Cards: [27026398ed8a].

**R123. Shopify checkout cannot be A/B tested client-side on standard plans.** Since checkout extensibility replaced checkout.liquid (general rollout August 2024), JavaScript injection into checkout is gone, and there is no built-in way to show a checkout customisation to one group and hide it from another. Shopify Plus has checkout extensibility (Checkout Blocks, UI extensions, Functions, Branding API) and some apps run limited checkout-element tests. About 80% of high-impact ecommerce tests happen before checkout anyway. Condition: any checkout hypothesis; ship as repairs on standard plans. Source: 05. `[verify UI]` `[web check: current Shopify checkout A/B options, yearly]`. Cards: [7c932a3b4986].

**Mobile**

**R124. Mobile first: put about 90% of CRO effort on mobile and check every page on a phone.** 02: 60% to 95% of traffic is mobile depending on brand (80% in the hero section). 06: mobile is about 60% of traffic and sales, converts at about half the desktop rate, and mobile cart abandonment is about 85%. Priorities: one-page or wallet checkout; guest checkout; tap targets at least 44px; floating key CTAs and critical actions in the thumb zone; clickable phone and email fields; social proof visible where decisions happen; no desktop grids squeezed onto mobile; no filters hidden in hamburger menus. Condition: every audit and every test's pre-registered device split. Sources: 02, 06. `[needs brand data: device split]`. Cards: [a56c27356031] [bb761687ad68] [1e03a58f6fe1] [d4104b13110f].

**R125. Speed is a lever; measure it with real-user data and isolate its revenue effect with a test or holdout.** 06's target: mobile LCP under 2 seconds; hero images under 100KB, grid images under 60KB. 06's elasticities contradict each other (100ms slower = 3.5% lower conversion; 100ms = 7% drop "in one large analysis"; 1 second = "up to 7%"), so use them to justify investigation, not to forecast. 02 calls load time "one of the easiest leverage points" (mockup 4.8 s vs 0.9 s) with no how. The work lives in 08-SPD. Condition: any speed hypothesis. Sources: 06, 02. Cards: [9461d45dfbe7] [36f1d8130259].

**Email capture and quizzes (01, lead-gen adaptations)**

**R126. Give every capture CTA a lure that matches the shopper's stage.** "Subscribe to our newsletter" offers nothing. A buyer guide for shoppers who do not know what to buy; a first-order discount or free postage for shoppers who know but delay. Check discount and shipping cost against margin first; measure signup-to-first-purchase, not signup volume. Condition: email capture hypotheses. Source: 01 (lead-gen adaptation). Cards: [ea8b1b83867d] [d043167a017f] [6026a7303e2a].

**R127. In a quiz or multi-step flow, ask about the need before asking for contact details.** Asking the problem first feels like a diagnosis; asking name, email and phone first feels like lead capture. Be honest about what the result step is. Condition: quiz funnels. Source: 01 (lead-gen adaptation). Cards: [9ed6a0a32b9f].

**R128. Say what happens after the click, and lower the commitment to match the shopper's stage.** "Get a free quote" beat "Book a free survey" by 60% at ADT because buyers only wanted a price (no sample given). Use permission phrases ("no obligation"). If you do not tell people what they will get, they assume the worst. Condition: any CTA that starts a process (quiz, consultation, pre-order, subscription). Sources: 01 (lead-gen adaptation), 03. Cards: [16c2667cb67c] [a4d2ce6b188a] [8121c53ef9d8] [a01ac2d91e2d] [4653645c47ac].

### 3.11 Price and offer tests

**R129. Never show different prices for the same SKU to different users at the same time.** It is legal in the US and EU when not based on protected characteristics, the EU requires disclosure of personalised prices, and even where legal it is "an ethics and brand landmine" (Amazon's 2000 DVD test ended with 6,896 refunds and Bezos saying "even that was a mistake"). Test instead: price presentation, savings framing, payment framing (instalments), tiers, bundles, or offerings that add or remove real features at different prices. Document refund, support and price-match handling before exposing traffic. 03 recommends monthly price-point testing with a tool (the presenter's conference sponsor); apply 05's limits to it. Condition: every price test. Sources: 05, 03. Conflict: C13. `[web check: jurisdiction rules on personalised pricing]`. Cards: [34fa165a64fe] [d12e614c0b4e] [e3ba0fb7d6f6].

**R130. Test offers on a cadence at stores that cannot power micro-tests.** Buy 1 get 1, 3 for the price of 2 (03 transcribed "3 for the power of 2"; confirm), build-a-bundle, thresholds, gifts with purchase (02: $30 perceived value, $4 to $5 COGS, over $60), post-purchase 1-click upsell (02: $19 bag, "usually $35 to $40", 50% off for 5 minutes). Judge on RPV and contribution. Condition: 03 says monthly under 300,000 sessions. Sources: 03, 02. Cards: [d12e614c0b4e] [1e7c5456a957] [0ca0ef2a3d5d].

**R131. Prefer positioned offers to blanket discounts.** 02: a "New Year's reset" bundle at full price converted better than the product ever did on sale; 20% off everything lifts revenue, cuts profit and trains customers to wait; free shipping teaches customers to value delivery separately, so give it only at a threshold that pulls AOV up. Condition: offer hypotheses. Source: 02 only. Cards: [0ca0ef2a3d5d] [1e7c5456a957] [23f840cd83b0].

### 3.12 Platform rules (Shopify)

**R132. Client-side tools for front-end visuals; server-side or Shopify Rollouts for checkout, pricing logic and speed-sensitive paths.** Client-side: marketer-owned, visual editor, fast, but flicker, extra JavaScript, easier to break, logic is public. Server-side: no flicker, faster, can test backend logic, works with feature flags, but needs engineers and a deploy cycle. Rollouts: server-side theme split before the page ships, no flicker, reports numbers with no significance verdict (you do the stats), paid plan tier. Condition: every test plan. Source: 05. `[verify UI]` `[web check: Shopify Rollouts availability and plan tier]`. Cards: [7c932a3b4986].

**R133. Check the plan before planning.** Basic, Shopify, Advanced: test everything before checkout (product, collection, cart, homepage, add to cart, trust elements, pricing display); tools like Varify run via a head snippet on all plans. Plus: checkout extensibility plus native theme A/B. Re-verify yearly. Condition: every engagement start. Source: 05. `[verify UI]` `[web check: Shopify checkout extensibility A/B options]`. Cards: [7c932a3b4986].

**R134. Confirm the testing vendor's engine, prior, SRM alerting and free tier before committing.** Named by 05 (all time-sensitive): VWO SmartStats (Bayesian; free up to 50,000 tested users a month), AB Tasty (Bayesian), Convert, Kameleoon (SRM flag at p < 0.001), Optimizely Web (mSPRT always-valid plus FDR; CUPED default on), GrowthBook (open source; frequentist and Bayesian; sequential; CUPED), Statsig (corrected-alpha sequential; free up to 1M events a month), Eppo (Bayesian with shrinkage plus GAVI). Google Optimize was sunset 30 September 2023. Condition: tool choice. Source: 05. `[web check: current engines, pricing, free tiers]`. Cards: [e3ee87a025c5] [0bda3b4d7e04].

### 3.13 Programme rules

**R135. A comprehensive programme (03: over about 300,000 sessions with good conversion and orders) runs deep audits, isolated A/B tests at 4 to 8 a month, a full data stack, learning loops on wins and losses, and a cross-functional team.** 03's agency spends 2 to 3 weeks on an audit of about 100 pages for such clients. Condition: only above the gates in R53; below them, R54. Source: 03. Cards: [3d52bd4930fe] [bbab5b1b0329].

**R136. Cadence follows power, not ambition.** 06 praises weekly testing ("test relentlessly", ShopClues at least 1 test a week). 05 says low-volume stores should test bigger, not more. Condition: the number of tests a month is whatever the traffic can power at the chosen MDE with no overlap on the same page area (R58). Sources: 05, 06. Conflict: C11. Cards: [67f74e89d43e] [300b03fc0354].

**R137. Research-prequalified programmes show higher win rates; unresearched ones lower.** 05 cites DRIP's 36.3% win rate against its pre-qualification. Condition: any programme review where the win rate is low; check the evidence gate (R20) before blaming the ideas. Source: 05. Cards: [f856d689f3d8] [8dc46d4893e1].

## 4. Procedures (implementation)

Each procedure names its goal, preconditions, steps with settings, checks, and rollback. Platform steps carry `[verify UI]`.

### P1. Build correct conversion and RPV numbers (02)

Goal: a baseline the agent can trust. Preconditions: Shopify analytics and GA4 access.
1. Revenue: pull Net sales + Shipping collected for the period, or Total sales minus tax. Do not use Total sales raw. `[verify UI]`
2. AOV: revenue from step 1 divided by orders. Shopify's AOV excludes shipping collected, so it will differ. `[verify UI]`
3. Sessions: pull GA4 sessions for the same period. Note the gap to Shopify sessions. `[needs brand data: GA4 vs Shopify session gap]`
4. Conversion rate = orders / GA4 sessions.
5. RPV = conversion rate x AOV. Contribution per visitor = RPV x gross margin %. Do not subtract CAC.
6. Repeat by device and by traffic temperature (cold paid, warm, returning).
7. Write RPV as a trend, not a point (02's agency uses about 2.5 years).
Check: the corrected RPV is higher than Shopify's naive figure (shipping added back) and the conversion rate is higher than Shopify's (fewer bot sessions). If not, a step is wrong. Rollback: none; this is a read. Cards: [91d639e7e2e2] [b9f3fede007a].

### P2. Read the funnel and find the biggest drop (03, 06, 07)

Goal: name the stage to work on. Preconditions: tracking confirmed (R17); P1 done.
1. In GA4, open Explore and build a funnel: product view, add to cart, begin checkout, purchase (07). Add checkout completion if the events exist. `[verify UI]` Funnel configuration itself is 06-MEA.
2. For paid traffic, extend the map: ad, landing page, PDP, cart, checkout, thank-you page, post-purchase upsell (03).
3. Read each stage rate by device and channel.
4. Compare with 06's bands (R13) as a directional check only.
5. Weight each drop by the sessions and revenue that pass through it. A 10-point drop on the hero PDP outranks a 30-point drop on a page with 200 sessions a month.
6. Compare event counts with orders in the store backend. If they do not match, stop and route to 06-MEA.
7. Write the funnel memo: stage rates, the biggest weighted leak, device and channel splits, what is unknown.
Check: the leak is stated with the traffic behind it, not only as a percentage. Rollback: none. Cards: [382d08d3f6aa] [bbe716a39c74] [9568c40e1d88] [25f9d85cd8e3].

### P3. Diagnose a conversion-rate change before touching the page (02)

Goal: rule out mix effects before a redesign. Preconditions: P1 by segment.
1. Split conversion by traffic temperature: cold paid, warm, returning.
2. Check whether cold share rose. If yes, the blend can fall with no page change (02: blended 2.8%, cold 1%, warm 4%).
3. Check returning-customer share; high returning share inflates conversion rate and AOV.
4. Check category, price point, AOV, creative and offer changes in the period.
5. If a segment's own rate fell with steady creative, audit the page (section 5). If only the blend moved, report a mix effect and stop.
6. If clarity, offer and proof are already strong, look at product quality, first-order contribution, launches and repeat purchase before another redesign.
7. Judge on RPV or contribution per visitor.
Check: the memo names which segment moved. Rollback: none. Cards: [953e03390b0d] [372439a05cbd].

### P4. Set up a behaviour review in Clarity (04) `[verify UI]`

Goal: a list of friction patterns by page and device. Preconditions: Clarity installed with at least 90 days of data. Interface as of July 2024; names may have moved.
1. Set the date range to the longest representative period (about 6 months; 90 days if newer).
2. Skim top-line metrics for context only.
3. Open the Insights block. Note the rates for rage clicks, dead clicks, excessive scrolling, quick backs.
4. For each Insight, click the camera icon to open the matching recordings.
5. Start with the most valuable and most visited journeys: homepage or campaign landing page, collection, PDP, cart, checkout.
6. For each recurring pattern, record page, device, the apparent blocker, and whether it blocks the purchase path.
7. Classify each pattern by R26 (blocked exit, useful missing action, buried information, false click).
Check: every pattern has at least 1 recording reference. Rollback: none. Cards: [e053644d5707] [9d9871ee324b] [0eae610ddc62] [5b9da7dd1967].

### P5. Read a heatmap page and turn an Area map into a test (04, 07) `[verify UI]`

Goal: placement and reach hypotheses for 1 page. Preconditions: P4 or a known page to inspect.
1. Open Heatmaps. Pick the page. Check the screenshot shows the real page; if a popup or broken layout was captured, use Change screenshot and pick another version.
2. Filter by the device with the most traffic first. `[needs brand data: device split]`
3. Name the page's core action (R23).
4. Click map: add up the clicks on and around the core CTA (04's heuristic: 5 to 7% preferred, 4 to 5% "in and around the average", under 1 to 3% weak). Note clicks on non-clickable elements and in empty space.
5. Scroll map: read reach at the top, the average fold, 75%, 50%, 25%. Find the exact section where reach falls sharply. Note the reach of reviews, guarantee, price and add to cart.
6. Area map: Edit areas, draw regions around navigation, filters, sticky controls, banners, menu toggles, product cards, key modules. Read each region's share of clicks.
7. Flag modules with high click share and low reach (07: 10.41% of clicks, 30 to 35% reach). Flag highly visible modules with few clicks. Flag a static element with a high click share (04: a banner that looked like a button took 46% of clicks).
8. Open recordings for the flagged elements to separate intent from confusion.
9. Write each finding as a narrow hypothesis (R42). For a placement finding, test the move alone: same module design, same destination, new position; primary metric purchase conversion with collection and PDP behaviour as support.
Check: every hypothesis names page, device, evidence and metric. Rollback: none. Cards: [09583734387e] [edd07a1a15f6] [de4dfe536e94] [3043da84ee0c] [bc5a8130eee9].

### P6. Pick and watch recordings (04) `[verify UI]`

Goal: the main friction pattern for a page or step. Preconditions: P4 flagged a page, or P2 found a drop.
1. Open Recordings. Filter: time frame, device, user action (dead clicks, rage clicks, excessive scrolling), scroll depth, landing page, performance (slow vs fast), page duration.
2. Sort by clicks high to low, then pages high to low: the most active visitors. Reverse the sort: the least active. Compare the 2 groups on the same page type.
3. Turn on skip inactivity and raise speed (04 used 4x for a 1-hour session, 1.5x for another). If hesitation may matter, leave inactivity visible.
4. Block 1 to 2 hours with no distractions. Take notes on every key finding.
5. Watch for: clicks on non-clickable elements; repeated navigation loops (back to the top for a filter); rapid clicking, excessive scrolling, skimming; how people move from home to product; which sections get time.
6. Ask "why" about every action.
7. Stop when new sessions repeat patterns you already have (04: about 100 for some clients, 400 to 450 for others).
8. After a fix ships, repeat with fresh recordings of the new version.
Check: the pattern is seen across several sessions and at least 2 devices before it becomes a hypothesis (1 return-to-top is not a pattern). Rollback: none. Cards: [0b8d2f6cc4d1] [a1a3e1f62713] [11e64288067b].

### P7. Set up surveys (03, 07) `[verify UI]`

Goal: objections and motivations in customer words.
1. Post-purchase survey on the thank-you page (KnoCommerce or Okendo on Shopify; Zipify is 03's host's product). Ask at least: "What made you purchase today?" and "What made you almost not purchase today?" Keep attribution questions ("how did you hear about us") in a separate 06-MEA survey or clearly separated.
2. Exit-intent survey (Hotjar Surveys paid add-on, or Okendo): "What stopped you from buying?", "What almost stopped you from converting today?", "What's the reason you're exiting the site?"
3. If no post-purchase survey exists yet: email customers and VIPs a one-time Typeform with the same questions; 03's incentive example is a $250 Amazon gift card draw. `[web check: prize-draw and data-privacy rules]`
4. After 2 to 4 weeks (or 100+ answers, whichever first; no source gives a count), group answers into themes: product uncertainty, quality, time to results, fit, price, shipping, returns, guarantee, how to use, trust gaps, missing info, comparison needs.
5. For each theme, check whether it is answered near the decision on the PDP, cart and checkout. Unanswered themes become hypotheses (R107).
6. Cross-check each theme with the funnel step and recordings (R43).
7. Re-survey after the fix ships and see whether the theme declines.
Check: buyer answers are not used to explain non-buyers; exit survey and user tests cover non-buyers. Rollback: remove the survey app. Cards: [b4505f6c4061] [91410aaad2c8] [b3b265cf22f6] [f89dbadb9131].

### P8. Mine reviews (03, 02)

Goal: objections, tone, buzzwords and unique feedback. Preconditions: review export; 03 says 500 to 1,000+ reviews for this to be non-negotiable.
1. Export all reviews to CSV from the review app. `[verify UI]` `[needs brand data: review export]`
2. Upload to an LLM (03: GPT; 02: Claude or ChatGPT) and prompt for: commonalities, tone of voice, buzzwords, key phrases, friction points, objections, and unique feedback that differentiates the product from alternatives.
3. Read the source reviews behind each claimed theme to confirm; the model can over-generalise.
4. Objections go to the FAQ and hero (R107). Unique feedback goes to positioning (02's one-of-one angle: "the first retinol that didn't make me peel"); claim it only if competitors cannot honestly say the same.
5. Include verbatims in the hypothesis rationale.
Check: every theme has at least 3 verbatim reviews behind it. Rollback: none. Cards: [fc9b05411697] [cf0bc0f31721] [79bdf741dfc4].

### P9. User tests, interviews and the self-purchase audit (03, 05, 07, 01)

Goal: what heatmaps cannot show.
1. Self-purchase: buy from the store on mobile, desktop and tablet within the last 4 weeks. Hand a phone to a 70-year-old and watch. Note popups and cookie bars covering the PDP CTA or cart button, and bugs. These are repairs (R50).
2. Remote user test (Userbrain at $40 per tester at 07's recording time, or Hotjar interviews): recruit 5 to 8 people per task (05). First prompt: first impressions on landing. Tasks: find a suitable product, add it to cart, check out. Note missed navigation, misread details, missed key info, hesitation at cart, checkout doubts.
3. Impartial first-impression check (01): ask people who have never seen the site what they expect about quality, service and legitimacy from the page alone.
4. Customer interviews (03): call recent buyers; why did you buy, was it easy, was anything unclear, what words do you use for the product.
5. Turn repeated patterns into hypotheses. These are qualitative samples, never conversion estimates.
Check: each pattern seen in at least 2 testers or interviews. Rollback: none. Cards: [a2d5c573076a] [f375f7ffb264] [f856d689f3d8] [c0690a74d2de] [9398191fe1b4].

### P10. Write the hypothesis and the test brief (05, 03, 06)

Goal: a pre-registered brief that a reader can run and audit. Preconditions: at least 2 points of evidence.
1. Hypothesis: "Because we observed [evidence], we believe [change] will cause [effect] for [segment], measured by [primary metric]. We will know it worked if [metric moves by at least MDE]."
2. Page, device scope, audience (all, cold paid only, new only).
3. One primary decision metric (conversion rate, RPV or gross profit per visitor per R6). State why.
4. Guardrails with thresholds: AOV, margin, return rate, refund rate, page load, add to cart, downstream purchase. 05 gives no threshold values; set and pre-register them per brand. `[needs brand data: guardrail baselines]`
5. MDE (relative and absolute), planned sample per variant, number of arms, planned dates.
6. Pre-registered segments: device, paid vs organic, new vs returning.
7. Tails (two-sided default; one-sided only with the R64 justification) and stopping method (fixed horizon, or which sequential engine).
8. Runtime: at least 1 full week, in practice 2, covering each weekday twice, plus time to reach the sample.
9. Contamination plan: exclude retention traffic, or run on a cold-only landing page (R65).
10. Validity plan: SRM check, tracking QA, flicker check, bot filter, marketing calendar check.
11. Action for win, loss and inconclusive, written before launch.
12. Expected-value estimate and ceiling (R44).
Check: a colleague can compute the same sample from the brief. Rollback: not applicable. Cards: [1b7725e0ff57] [1f26cd618e2d] [a6c0f42b99a3] [300b03fc0354].

### P11. Prioritise the backlog (05, 03, 02, 06)

Goal: a ranked leaderboard. Preconditions: hypotheses in R42 form.
1. Gate entry: no idea enters without 2 points of evidence (analytics plus replay, survey, user test or interview).
2. Score with a frame to organise: PXL-style criteria (above the fold; noticeable within 5 seconds; high-traffic page; backed by heatmap, user test, survey or analytics; build difficulty), or ICE 1 to 10 x 3 multiplied (02) for a small team. Do not let the idea's owner be the only scorer.
3. Compute expected value: P(win) x expected lift x gross profit per conversion x traffic exposed, minus build cost. Add the ceiling (most it could be worth). `[needs brand data: SKU margin, page traffic]`
4. Keep P(win) honest: 05's anchor is 10 to 20% for well-run tests; raise it only for strong evidence.
5. Sort by expected value. Break ties with the frame score.
6. Check the calendar: no 2 tests on the same page area at once (R58).
7. Repairs and clarity fixes skip the queue and ship (R50, R51).
Check: the top 5 all have named evidence and a computed sample. Rollback: none. Cards: [aad25dea9ed9] [4a2e3d77d68e] [a6c0f42b99a3] [a56c27356031] [300b03fc0354].

### P12. Decide repair, ship or test (05, 02, 04)

Goal: the right path for each backlog item.
1. Is the current state objectively defective (errors, rejected valid input, browser failure, double tracking, blocked CTA, silent cart wipe, false-click element)? Yes: repair now, log it, verify with fresh recordings. Stop.
2. Is it an obvious clarity fix, or proven checkout or landing-page practice, and the store is under 30 orders a month, or the change cannot plausibly hurt? Yes: ship, log it, watch the funnel step and recordings, treat any before-and-after shift as weak evidence.
3. Are both versions plausibly viable and the better one unknown? Compute the sample (P13). If reachable in 2 to 4 weeks: test.
4. If not reachable: raise the MDE (bolder change), move to a higher-traffic page, switch to a micro-conversion primary with purchase guardrail, or ship as a bold change with research backing and a later holdout.
5. Record the decision and the reason in the registry.
Check: nothing defective is queued for a test. Rollback: for a shipped change, keep the previous theme version or section so it can be restored in 1 step. Cards: [3eca46fe9ba3] [6503bc821ea6] [0bda3b4d7e04] [0b8d2f6cc4d1].

### P13. Size a test and set runtime (05, 02, 03)

Goal: sample per variant, total, and weeks. Preconditions: baseline conversion rate of the tested page and metric; weekly eligible traffic. `[needs brand data: baseline conversion rate per page and device; weekly sessions on the tested page]`
1. Baseline p: conversion rate of the page for the audience in the test (not sitewide).
2. MDE: the smallest relative lift worth shipping, thought through in gross profit. Convert to absolute delta = p x relative MDE.
3. Confirm the calculator's input type (relative vs absolute).
4. Alpha 0.05, power 0.80, two-sided (R64).
5. n per variant = 16 x p(1-p) / delta^2, or read the table below, or use Evan Miller's calculator. Check against conversions per variant: about 3,830 (5%), 1,000 (10%), 260 (20%), 120 (30%).
6. Total = n x number of arms.
7. Weeks = total / weekly eligible traffic, rounded up to whole weeks; minimum 1, in practice 2; cover each weekday twice.
8. If RPV is the primary metric, multiply the traffic need by about 6 (05) and pre-register a winsorization cap or a threshold-proportion metric; 05 gives no cap value.
9. If weeks are unreasonable (05: months), go back to P12 step 4.
10. Write MDE, n per variant, arms, total, weeks and dates into the brief.

Sample size per variant, 95% confidence, 80% power, two-sided (05, statsunlock.com, consistent with Evan Miller):

| baseline | 5% rel | 10% rel | 20% rel | 30% rel | 50% rel |
|---|---|---|---|---|---|
| 1% | 637,010 | 163,095 | 42,693 | 19,827 | 7,750 |
| 2% | 315,206 | 80,682 | 21,109 | 9,798 | 3,826 |
| 3% | 207,938 | 53,211 | 13,914 | 6,455 | 2,518 |
| 5% | 122,124 | 31,234 | 8,158 | 3,780 | 1,471 |

Check: a second person gets the same n from the brief. Cross-check with 02's anchor (about 1,000 conversions per variant for a 10% lift). Rollback: none. Cards: [00c82f0de25d] [5fae1beab1ba] [699a7cd5ac4c] [7eeb62d20124].

### P14. Choose the stats engine and stopping method (05)

Goal: a stopping rule the p-value is valid under.
1. Can you estimate the expected sample well (stable traffic, known baseline)? Yes: fixed horizon (look once at the planned sample) or group sequential with alpha spending (more powerful). No, or stakeholders will watch daily: always-valid method (mSPRT, GAVI, corrected alpha), accepting wider intervals.
2. If the tool is Bayesian, find its prior and whether its stopping threshold is protected against optional stopping. If you cannot state the prior, treat results like a peeked frequentist test and size as fixed horizon.
3. Confirm the tool's current engine and SRM alerting in vendor docs. `[web check: vendor stats engine docs]`
4. Write the method into the brief. Under fixed horizon, no interim reads are acted on. Under a sequential engine, only its rule stops the test.
5. New tool or new programme: run an A/A test first (R79).
Check: the brief names the engine and the exact stopping rule. Rollback: none. Cards: [e3ee87a025c5] [0bda3b4d7e04].

### P15. QA, launch and monitor (03, 05, 02)

Goal: a clean test. Preconditions: brief approved.
1. QA the variant 2 or 3 times on real devices (mobile first), browsers and connection speeds. Check add to cart, cart, checkout start in both arms.
2. Confirm tracking fires in both arms and that the tool's conversion count matches the store backend for a short window.
3. Check flicker on a slow mobile connection; if the original flashes, move to server-side or Rollouts, or accept the anti-flicker cost (up to 3 to 4 seconds hidden) and record it.
4. Exclude retention traffic (Klaviyo sends) from the test population, or run on a cold-only landing page; confirm sticky bucketing. `[verify UI]`
5. Check the marketing calendar for promos, launches and holidays in the window; move dates if a sale falls inside.
6. Launch with the planned split.
7. Day 1 and then at each planned look: SRM chi-square on users; flag p < 0.001; if flagged, pause trusting the result and find the cause (bots, redirects, tracking, browser failures).
8. Filter bots.
9. Do not read significance between planned looks. Do not kill or call on one day.
10. Watch for tracking breakage; if it breaks, invalidate the read and restart.
Check: SRM clean, tracking matched, no promo overlap. Rollback: end the test and restore control to 100%; keep the brief and log the reason. Cards: [4d0785cdcf2b] [370ed8c02e34] [699a7cd5ac4c] [7d481c590b57] [3eca46fe9ba3].

### P16. Audit a result or a case study (05, 06)

Goal: decide whether a number can be trusted. Use for your own tests and for any case study, including every case in this playbook.
1. SRM: chi-square goodness-of-fit on the randomisation unit; p above 0.001.
2. Flicker: did the original render first in the variant arm?
3. Tracking: did any pixel or event break mid-test? Do tool conversions match backend orders?
4. Bots filtered?
5. Seasonality or promotions overlapping the window?
6. Stopping: was the test stopped at the planned sample or by a sequential rule, or at the first p < 0.05?
7. Runtime: at least 1 full week, in practice 2, whole weeks?
8. Metric count: how many metrics and segments were read? Bonferroni or FDR applied? Were segments pre-registered?
9. Twyman's law: is the lift plausible (1 to 5% mature, 10 to 20%+ unoptimised)? 50%+ or hundreds of percent: hunt for bugs before celebrating.
10. Guardrails: AOV, margin, returns, refunds, page load, add to cart flat or better?
11. Device split: same direction on mobile and desktop?
12. For a case study: does it state baseline, sample, runtime and validity checks? If not, hypothesis material only.
Output: pass, fail, or hypothesis-only, with the failing checks named. Cards: [370ed8c02e34] [8dc46d4893e1] [1f26cd618e2d] [300b03fc0354].

### P17. Read, decide and close (05, 03, 02)

Goal: a decision and a learning.
1. Report the effect on the primary metric with its confidence interval, per arm, with sample and dates.
2. Compare the interval with the MDE, incremental gross profit, build cost and guardrails.
3. Plot the daily effect; if novelty is suspected, compare first-exposure with repeat-exposure conversion; judge on the stable period.
4. Read the pre-registered segments (device, paid vs organic, new vs returning). Opposite directions: do not ship blind.
5. Win within the realistic band and guardrails flat or better: ship to 100%, add to the live-winner register, schedule the post-ship verification (P6 step 8, P7 step 7).
6. Win that is surprising or large: replicate or hold out before banking the revenue.
7. Fully powered inconclusive: record "effect smaller than MDE"; ship neither, or the simpler and cheaper version; do not extend.
8. Clearly negative: stop; do not wait for a reversal; record why it lost.
9. Before scaling a winning angle: check returns, chargebacks, repeat rate and 365-day LTV by angle.
10. Write the registry record (P18).
Rollback: a shipped winner keeps its control version stored so it can be restored in 1 step if guardrails degrade after launch. Cards: [70db51ffb976] [5fae1beab1ba] [1f26cd618e2d] [dad9c85ea261] [f09cfbc3ef44].

### P18. Write the registry record (05, 06, 03)

Goal: one record per test, repair, holdout or causal analysis, in one log. Fields:
1. id, date opened, owner, status (planned, live, closed, shipped, reverted).
2. type: A/B, A/B/n, bandit, feature holdout, programme holdout, repair, before-and-after, causal method.
3. page, device scope, audience, platform tool and engine.
4. hypothesis in R42 form, with the evidence list (each point: source, date, what it showed) and verbatims.
5. primary metric and why; guardrails with thresholds; pre-registered segments.
6. MDE relative and absolute; baseline; planned sample per variant; arms and split; planned dates; tails; stopping method.
7. validity plan and results: QA passes, SRM values per look, tracking match, flicker check, bots filtered, promo overlap notes.
8. actual sample per variant, actual dates, whether the sample was reached.
9. results: effect and confidence interval per metric per segment; guardrail results; daily plot note (novelty).
10. Twyman check: plausible or investigated.
11. decision: ship, kill, inconclusive, replicate, hold out; the action pre-written in the brief versus the action taken.
12. learning: why it won or lost; what the next hypothesis is.
13. shipped date; live-winner check dates; any later reversion and why.
14. for repairs: what was broken, evidence, fix, verification.
15. for holdouts: question, groups and shares, period, net lift with interval, decision.
Check: a reader with no context can compute the same sample and reproduce the decision. Cards: [70db51ffb976] [2b951af15841] [f09cfbc3ef44] [3eca46fe9ba3].

### P19. Run a CRO programme holdout (06)

Goal: net programme value. Preconditions: user-level randomisation available; 06's rough gate is over 100,000 monthly visitors. `[needs brand data: monthly visitors, logged-in share]`
1. Compute detectability first: with the holdout share and period, can the holdout reach enough conversions to detect the effect you care about (P13 math with unequal arms)? 06's 5% and 90 days are illustrations.
2. Randomly assign the holdout share (example 5%) to see the site as it was before the programme; sticky by user.
3. Everyone else gets every shipped winner.
4. Apply repairs and accessibility, policy and major usability fixes to both groups; do not withhold them.
5. Keep assignment stable for the period (example 90 days).
6. At the end, compare conversion rate and RPV with confidence intervals. Report net lift, not the sum of test lifts.
7. Record which experiences each group could receive, the interval and the decision (P18).
Check: the holdout was never exposed to a shipped winner (check the tool's audience logs). Rollback: end the holdout and expose everyone. Cards: [f671352f5b6e].

### P20. Run a feature holdout (06)

Goal: net revenue effect of a popup, recommendation module, personalisation layer or cart-recovery flow.
1. Define the decision metric: RPV. Support: conversion rate, AOV, opt-in rate, repeat purchase.
2. Randomly hold out a group that never sees the feature (examples: popup 90/10; recommendations 5% holdout). Sticky by user.
3. Tag both groups and track through to purchase and, if the feature targets it, repeat purchase.
4. Run long enough to capture delayed purchases; compute the detectable effect first.
5. Read trade-offs: more opt-ins but fewer purchases; more clicks but no bigger baskets.
6. Segment only if the sample supports it; decide on the pre-declared overall metric.
7. Decision: keep, rework, or remove. Record (P18).
Rollback: expose everyone or remove the feature. Cards: [c076b110d253] [e46b405d55df].

### P21. Run a price or offer test (05, 03, 02)

Goal: a legal, ethical test of value perception.
1. Legal and ethics review for the market. `[web check: jurisdiction rules on personalised pricing and disclosure]`
2. Never base price differences on protected characteristics. Do not show different prices for the same SKU to different users at the same time.
3. Choose what to test instead: price presentation, savings framing, payment framing (4 payments of $12), tiers, bundles, gift thresholds, free-shipping thresholds, post-purchase upsells, or different offerings at different prices.
4. Price bundle discounts from fulfilment savings (02) so margin holds; check gift COGS against perceived value.
5. Document refund, support and price-match handling before exposing traffic.
6. If a price-test app is used (05 names TestSignal; 03's sponsor is likely Intelligems `[web check: tool name]`), check how it assigns prices, handles disclosure, and records revenue and margin.
7. Primary metric: contribution per visitor where powered; otherwise conversion rate with AOV and margin guardrails.
8. Size, run, audit and close as P13 to P17.
Rollback: restore the single price and offer for everyone. Cards: [34fa165a64fe] [d12e614c0b4e] [d5a74f7edadd] [0ca0ef2a3d5d].

### P22. Plan a Shopify test around platform limits (05) `[verify UI]`

Goal: a test the platform can actually run.
1. Check the plan tier. `[web check: Shopify checkout extensibility and A/B options, yearly]`
2. Basic, Shopify, Advanced: test only before checkout (product, collection, cart, homepage, add to cart, trust elements, pricing display). A head-snippet tool (Varify named) runs on all plans. Checkout changes ship as repairs, measured by stage rates as weak evidence.
3. Shopify Plus: checkout extensibility (Checkout Blocks, UI extensions, Functions, Branding API); some apps (Personizely, Checkout Boost named) run limited checkout-element tests via Checkout Blocks.
4. Theme tests: consider Shopify Rollouts (server-side, no flicker, numbers with no significance verdict, paid tier); do the stats yourself (P13, P14).
5. Client-side for visuals; server-side or Rollouts for checkout, pricing logic and speed-sensitive paths.
6. Record the platform constraint in the brief.
Cards: [7c932a3b4986].

### P23. Route a measurement question (06)

Goal: the right design for the question, and the right folder.
1. "Did this specific test win?": A/B test, this folder.
2. "Does this feature add net revenue?": feature holdout (P20), this folder.
3. "Has the CRO programme created value?": programme holdout (P19), this folder.
4. "Does retargeting drive incremental revenue?": user-level holdout (06's illustration: 30-day non-buyers, 80/20 split, 14 days; holdout rate divided by exposed rate is the share that would have bought anyway). Route to 11-ADC.
5. "Does Meta drive incremental sales?": geo holdout (06's Hourglass example: 10 DMAs paused 6 weeks, market correlations 0.96 to 0.99). Route to 11-ADC.
6. "Does this email campaign drive incremental purchases?": list holdout (example 10%; lift = promoted rate minus holdout rate). Route to 14-EML.
7. "What was the impact of a site-wide change during peak season?": difference-in-differences or BSTS. Route to 06-MEA; state the identifying assumption.
8. "We cannot randomise": synthetic control, propensity matching, regression discontinuity. Route to 06-MEA.
9. Whatever the route, write the question, method, result with interval and decision into the shared log (P18).
Cards: [0eca60fd9161] [ddbbe8061d10] [e353aade03ae] [04a08881ac09] [2b951af15841].

## 5. Diagnostic checklists

Written for a worker. Columns: what to check, how, good, bad, fix, source. "Fix" means the hypothesis or repair to raise, not a promise. Case figures are examples. Anything from 01 is a lead-gen adaptation.

### 5.1 Funnel read

| what to check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| Tracking health | Compare funnel event counts with backend orders for the same period | Within a few % | Missing or inconsistent events | Fix tracking first (06-MEA); no test until fixed | 07 [382d08d3f6aa], 05 [3eca46fe9ba3] |
| Session and revenue definitions | Check that sessions are GA4 and revenue excludes tax, includes shipping collected | Corrected figures used | Shopify raw totals | Rebuild with P1 | 02 [91d639e7e2e2] |
| Overall conversion band | Orders / GA4 sessions vs 06 bands | 3 to 5% "good" | Under 1% | Check traffic quality and mix (P3) before page work | 06 [25f9d85cd8e3] |
| Add-to-cart rate | Add to cart / PDP views | 12 to 18% | Under 5% | PDP work (5.4) | 06 [25f9d85cd8e3] [fc7c739888fc] |
| Cart-to-checkout rate | Checkout starts / carts | 60 to 70% | Under 30% | Cart work: cost transparency, reassurance (5.5) | 06 [25f9d85cd8e3] |
| Checkout completion | Purchases / checkout starts | 70 to 80% | Under 50% | Checkout audit (5.6), mostly repairs | 06 [d4104b13110f] |
| Biggest weighted leak | Multiply each drop by sessions and revenue passing through it | One stage clearly dominates | Working on a low-traffic page while the hero PDP leaks | Re-point the backlog | 03 [bbe716a39c74], 05 [f856d689f3d8] |
| Mix effect | Split conversion by cold, warm, returning; check cold share over time | Segment rates steady; blend moved by mix | A segment's own rate fell with steady creative | Audit the page only in the second case | 02 [953e03390b0d] |
| Device split | Stage rates by device | Mobile close to half desktop or better (06) | Mobile far below | Mobile checklist (5.7) | 06 [1e03a58f6fe1] |
| Category exit rate | Exit rate on collections vs site average | Near average | Well above | Check traffic intent, then 5.3 | 06 [1e03a58f6fe1] |
| Direct entrances | Landing-page report: which PDPs and collections get direct entries | Those pages carry their own proof and delivery info | Proof only on homepage | Audit them as landing pages | 01 [3127398d2368] |

### 5.2 Homepage

| what to check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| Share of sessions that start here | Landing-page report | Known before any homepage work | Assumed | Work the real entry pages first | 01 [3127398d2368] |
| 3-second hero | Show the hero to a stranger for 3 seconds: who, what, why | They can say it | Vague line ("Expert hand, human touch") | Rewrite hero (07-LPG); hypothesis on clarity | 06 [5e578ca91bcc], 04 [bc5a8130eee9], 01 |
| Hero drop | Scroll map reach just below the hero | About 93 to 95% still scrolling (04 demo) | Large drop right after hero | Hero clarity plus proof above the fold | 04 [bc5a8130eee9] |
| Curation | Count promoted items and categories in the first 2 screens | Focused selection, clear category entry points | Head-to-toe assortment across many categories | Test a curated set (06 example: broad set cut ATC 6.07%) | 06 [5e578ca91bcc] |
| New-visitor merchandising | What do visitors with no history see | Bestsellers | Static featured products | Test bestsellers for new visitors (06 example +23.01% CTR) | 06 [5e578ca91bcc], 03 [1823c8a7c180] |
| Mega menu | Recordings: do new visitors open it; what is on top | Bestsellers carousel, icons, proof; non-money links at the bottom | Plain default links; contact and FAQ on top | Mega menu test (03 case) | 03 [033531683bba] |
| Menu structure | Count options; check labels; click each | Customer words; under about 6 top options; clicks land on useful pages | Alphabetical, jargon, "commercial home" style intermediate pages | Restructure menu | 01 [f5942adec72b] |
| Menu icon | Mobile: is the menu control familiar | Standard icon and position | Quirky icon or hidden control | Repair | 01 [d4484bf96e29] |
| Hidden demand | Area map click share vs scroll reach per module | Most-clicked modules sit where most people reach | High click share, low reach (07: 10.41% clicks, 30 to 35% reach) | Test moving the module up alone | 07 [de4dfe536e94] |
| Ignored modules | Area map: highly visible modules with few clicks | Every module earns clicks | Static banners that look like buttons; dead modules | Make it work, restyle or remove; confirm in recordings | 04 [09583734387e], 07 [3043da84ee0c] |
| Proof above the fold | Is social proof visible before scrolling | Rating, review count, press or customer count in the hero | Proof only on About or reviews page | Test proof in hero | 04 [bc5a8130eee9], 01 [ba8350548af5] |
| One conversion offer | Count offers competing in the first screen | One newsletter or promo offer with a concrete incentive | Several competing offers | Reduce to one | 06 [5e578ca91bcc], 03 [4653645c47ac] |
| Popups and chat | Recordings and rage clicks in the first 5 seconds | Nothing covers the hero CTA or menu in the first seconds | Popup within 5 s; chat covering a button | Repair: delay or move | 04 [9d9871ee324b] |

### 5.3 Collection page

| what to check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| Page job | Decide: browsing, deciding or buying, from traffic and recordings | Design matches the job | Add to Cart buttons on a browsing page | Test removing them; or, for repeat-buy consumables, test price on card plus add to cart (C14) | 06 [1e03a58f6fe1], 03 [6f635b9d003d] |
| Products above the fold (mobile) | Open on a phone | 2 x 2 grid, 4 products visible | Hero banner or text block hides products | Cut banner to 30 to 40% of first view or less; "start again" (03) | 03 [6f635b9d003d], 06 [1e03a58f6fe1] |
| Labels | Count labelled cards | A few products labelled (bestseller, new, low stock); labels true | Every product labelled; invented scarcity | Reduce; only real data | 03 [6f635b9d003d], 06 [e18bae3af3dd] |
| Filters on mobile | Recordings: do shoppers scroll back to the top to refine | Sticky bottom filter bar or floating pill | Filter only at the top; hidden in hamburger | Test sticky filter, after confirming across several sessions | 04 [11e64288067b], 06 [1e03a58f6fe1] |
| Tap targets | Measure controls | At least 44px with whitespace | Tiny thumbnails, cramped desktop grid | Resize | 06 [1e03a58f6fe1] |
| Subcategory entry | Page review | Clear subcategories, visual hierarchy, swipeable carousels | Wall of undifferentiated products | Add structure | 06 [1e03a58f6fe1] |
| Promo consistency | Compare promo message on collection and on its PDPs | Same promo reinforced | Promo vanishes on PDP | Align messaging | 06 [1e03a58f6fe1] |
| Exit rate | Analytics | Near site average | Well above | Check traffic intent; then design | 06 [1e03a58f6fe1] |
| Image weight | Grid image sizes | Under 60KB, WebP, lazy-loaded below the fold | Heavy images | 08-SPD | 06 [9461d45dfbe7] |

### 5.4 Product page

| what to check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| 4 questions above the fold | Open on a phone; ask what is it, why this one, why now, why trust | All 4 answered; order value, proof, price, CTA | Generic title ("Face serum 30 ml"), no reason to choose, no urgency, no proof | Hero rewrite (07-LPG); headline framing test | 02 [bb761687ad68] [36f1d8130259] |
| Above-fold clutter | Count pickers in the hero | No SKU details, size or quantity pickers in the hero (or defaulted) | Pickers push proof and CTA down | Move pickers to cart or default them | 02 [e10616e94452] |
| Scroll cue | Look at the fold | Cue that more is below | Page looks finished at the fold | Add cue | 02 [36f1d8130259] |
| Add to Cart position | Scroll map reach at the CTA | CTA above the fold and sticky | Reached by 25% (04 example) | Sticky add to cart; move up | 06 [fc7c739888fc], 03 [116d1016fa3b], 04 [edd07a1a15f6] |
| CTA click share | Click map: sum clicks on and around the CTA | 5 to 7% (04 heuristic) | Under 1 to 3% | Emphasise, move, redesign; test | 04 [09583734387e] |
| Reviews position | Where do stars and count first appear | In the hero | Reviews only far below | Move stars up | 03 [116d1016fa3b], 02 [36f1d8130259] |
| Review count and mix | Review widget | About 100+ reviews; media reviews first; mix of 4 and 5 stars; 4.8 reads real | 0 reviews; wall of 5.0; text only | Get reviews first; sort media first; show real distribution | 02 [a507cc86ec03] [0a1f9ee893a3], 06 [e18bae3af3dd] |
| Proof matches claim | Read the featured reviews against the hero claim | Reviews prove the specific claim; specifics (age, result, time) | Generic "great product" wall | Curate claim-matched reviews and before-and-afters | 02 [1d5e67c73cdd], 01 [f95f16ca7611] |
| Review authenticity cues | Review dates | Spread over time | Bunched around the same dates | Fix collection cadence; do not fake | 01 [e24c4415d85e] |
| Gallery | Swipe the carousel | Thumbnails, not dots; gallery sells (benefits, UGC, video, guarantee) | Dots; product-only shots | Test gallery as mini landing page | 03 [116d1016fa3b] |
| Guarantee visibility | Find the guarantee | Visible next to the CTA (older or risk-averse audiences) | Collapsed accordion | Un-collapse; test | 03 [116d1016fa3b] |
| Trust elements | List every badge and statement near the CTA | Specific policy and proof statements (returns, guarantee, customer count) | Generic security seals as the only "proof" | Remove generic seals; test policy statements (C1) | 02 [cdd5df001439], 03 [84ebf548938d], 06 [e18bae3af3dd] |
| Price, shipping, returns, delivery | Find each without clicking | All visible; consistent currency and origin | "Add to cart to see shipping"; $ note on a £ price; inconsistent times | Surface and align | 06 [fc7c739888fc], 01 [e24c4415d85e] |
| Long copy block | Scroll map section by section | Smooth decay | Steep drop after one paragraph (04: about 30%) | Bullets, bold, restructure | 04 [edd07a1a15f6], 03 [116d1016fa3b] |
| "So what" on every line | Read each feature line | Outcome first, feature as proof | "30 ml, vegan, triple peptide" as headlines | Rewrite (07-LPG) | 02 [790f6b3372c2] |
| Table stakes given hero space | Look for free shipping, fast dispatch, great service as headlines | Shrunk to small points low on the page | Given hero space as differentiators | Shrink | 02 [cf0bc0f31721] |
| Top objection answered | Compare "almost did not buy" themes with hero and CTA area | Top objection answered in hero or beside CTA | Objection unanswered (leather quality; time to results) | Hero or section test (03 cases) | 03 [d8e9c11154e5] [109929fb0656] |
| FAQ content | Read the FAQ | Top 3 real objections from research | Shipping policy, brand story | Rebuild from research | 02 [499b4e67252a] |
| Alternatives handled | Read the end of the copy | Every other solution addressed | Silent on cheaper or existing options | Add section | 02 [9f610afef497] |
| Message match | Open each active ad next to the page | Same persona, promise, words | Specific ad into a generic 9-benefit PDP | Message-matched page per persona or offer | 02 [a5cf6ee34972], 03 [6695665021f2] |
| Cold-traffic format | Where does unaware or VSL traffic land | Landing page or advertorial with hook, problem, mechanism, objections, proof, risk reversal, CTA | Plain PDP | Pre-sell page test (C2 for traffic) | 02 [aa0e72b56778], 03 [2d977920a505] |
| Dead clicks | Insights, click map, recordings | Static items do not block purchase | Images that do not open, logo that does not go home, pricing block with 1 live button | Add the expected action | 04 [0eae610ddc62] |
| Quick backs and hunting | Insights, recordings | Normal comparison shopping | Leaving within seconds; racing to find price, reviews, delivery | Surface the missing item sooner | 04 [5b9da7dd1967] |
| Popups and chat | Recordings, rage clicks | Nothing covers ATC in the first 5 s | Popup within 5 s; chat over ATC; cookie bar over button | Repair | 04 [9d9871ee324b], 03 [a2d5c573076a] |
| Demographic fit | Fonts, images, readability vs buyer | Target-age images, larger fonts, scannable text for older buyers | Young models for a pro-age brand; small text | Redesign (07-LPG); test | 03 [116d1016fa3b] [6695665021f2] |
| AI-referred visitors | Segment AI referral traffic; read landing mix and conversion | PDP confirms product type, size, price, delivery, use case at once | Generic page forces re-browsing | Tailor PDP facts; measure RPS | 06 [86c233f0eb39] |
| Load time | Real-user LCP on mobile | Under 2 s | 2.5 s+ | 08-SPD; isolate revenue with a test or holdout | 06 [9461d45dfbe7], 02 [36f1d8130259] |

### 5.5 Cart

| what to check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| Coupon field | Is a discount-code box shown with no live promo | Hidden when no promo; working when one is | Box shown, no promo | Remove (03 case) | 03 [19e8c5c27387] |
| Reassurance | Is there a returns, support, guarantee bar | Present near the checkout button | None | Add trust policy bar; test (C1) | 03 [84ebf548938d] |
| Free-shipping progress | Add an item below threshold | "Spend $12 more" message | No message; threshold too low or absent | Add message; set threshold above typical cart | 02 [c6984ab0f0cc] [23f840cd83b0] |
| Upgrade path | Add a single item | 1-click upgrade to routine or bundle that unlocks gift and shipping | Nothing | Cart drawer offer test | 02 [6baa7dce36c7] |
| Gift thresholds | Raise cart value | Gifts unlock as spend rises (low COGS, high perceived value) | None | Gamification test (03 case) | 03 [e3ba0fb7d6f6], 02 [0ca0ef2a3d5d] |
| In-cart upsells | Review cart | Relevant, low-friction add-ons | None, or irrelevant | Test | 03 [e3ba0fb7d6f6] |
| Cost preview | Look for shipping, tax, fees | Shown or estimated before checkout | Appear only at last step | Show early (39% abandon for late costs) | 06 [d4104b13110f], 02 [27026398ed8a] |
| Cart wipe or state bugs | Recordings; self-purchase; switch menus and variants at checkout | Cart persists | Silent cart wipe (04 case) | Repair immediately | 04 [0b8d2f6cc4d1] |
| Cookie bar over cart button | Phone test | Clear | Covered | Repair | 03 [a2d5c573076a] |
| Judge on | Metrics for any cart test | RPV and contribution | AOV alone | Set metrics per R1, R9 | 02 [0ca0ef2a3d5d] |

### 5.6 Checkout

| what to check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| Testability | Plan tier and checkout extensibility status | Known before hypotheses are written | Client-side checkout test planned on a standard plan | Ship as repairs; Plus for tests (P22) | 05 [7c932a3b4986] |
| Total extras | Sum shipping, tax, fees on a typical order | Under about 10% of AOV | $26 of extras on a $100 order (02 mockup) | Cut or fold into price; threshold shipping | 02 [27026398ed8a] |
| Total shown early | Walk through | Total before checkout; no drip pricing | Monthly price on page, quarterly in cart (02 IM8) | Show true total | 02 [8b2d9df04dfb] |
| Tax line | Look at the order summary | Included tax labelled clearly | Looks like a new charge | Label | 02 [8b2d9df04dfb] |
| Guest checkout | Walk through as a new user | Guest is default and prominent; email collected during it | Forced or hidden account step (62% of sites, Baymard) | Turn off forced accounts `[verify UI]` | 02 [94a63f9f740b], 06 [d4104b13110f] |
| Express pay | Look at the top of checkout | Shop Pay, Apple Pay, Google Pay first; UPI in India | Missing or buried; redirects | Enable and move up `[verify UI]` | 02 [a5c46083a30f], 06 [d4104b13110f] |
| Field count | Count fields | Essentials only; optional marked; autofill works | Baymard average 11.3; bloated address block | Cut fields | 02 [c6984ab0f0cc], 06, 05 |
| Progress indicator | Multi-step flow | Present | Absent | Add | 06 [d4104b13110f] |
| Returns policy | Find it during checkout | Stated plainly ("30-day returns") | Hidden | Surface; do not rush free returns in fashion | 02 [1e401776f34b], 06 |
| Delivery expectations | Read the delivery options | Realistic dates; fast options offered | Slow only; or dates hidden without legal review | Add fast options; hide-dates test only sized and reviewed (R122) | 02 [27026398ed8a] |
| Payment trust cues | Look for payment logos, security indicators | Recognisable brands present | Startup-looking checkout with no brand presence | Add proof and brand presence, not generic seals (C1) | 06 [d4104b13110f], 02 [cdd5df001439] |
| One-page vs multi-step | Note current design | Decided by a test or held constant | Changed on opinion | Test on Plus or server-side (C15) | 02 [c6984ab0f0cc], 06 [04a08881ac09] |
| Mobile checkout | Phone walk-through | Large tap targets; wallet or one-page | Tiny fields; redirects | Mobile repairs | 06 [d4104b13110f] |
| Abandonment flows | Are email and SMS recovery flows live | Live, measured against a holdout, not discount-only | Absent, or discount-only with no holdout | 14-EML build; P20 holdout | 02 [3163cc34fa79], 06 [e46b405d55df] |
| Payment errors and completion tracked | Separate events for checkout start, payment error, completion by device | Tracked before and after changes | Only purchases tracked | 06-MEA | 06 [d4104b13110f] |

### 5.7 Mobile

| what to check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| Effort split | Where is CRO time going | About 90% mobile | Desktop first | Re-plan | 02 [a56c27356031] |
| Device conversion gap | Mobile vs desktop conversion | Mobile near half of desktop or better (06) | Far below | Mobile audit | 06 [1e03a58f6fe1] |
| Mobile cart abandonment | Carts vs purchases on mobile | Better than about 85% (06) | Worse | Cart and checkout mobile fixes | 06 [d4104b13110f] |
| Thumb zone | Where are key actions on a phone | Lower half; floating CTA; sticky filter | Top-only controls | Move controls | 06 [1e03a58f6fe1] |
| Tap targets | Measure | At least 44px | Cramped | Resize | 06 [1e03a58f6fe1] |
| Desktop grid squeezed | Compare layouts | Mobile-designed grid | Tiny thumbnails, unreadable text | Redesign | 06 [1e03a58f6fe1] |
| Clickable phone and email | Tap them | Open dialler and mail | Static text | Repair | 06 [d4104b13110f] |
| Wallets | Checkout on phone | Apple Pay, Google Pay, Shop Pay | Card entry only | Enable | 02 [a5c46083a30f], 06 |
| LCP and INP | Chrome UX Report, Shopify Web Performance, PageSpeed Insights (real-user) `[verify UI]` | LCP under 2 s | 2.5 s+ | 08-SPD | 06 [9461d45dfbe7] |
| Image weights | Inspect | Hero under 100KB, grid under 60KB, WebP, lazy-load | Heavy | 08-SPD | 06 [9461d45dfbe7] |
| Hero check on a phone | Open every PDP on a phone, not a computer | 4 questions answered (5.4) | Only checked on desktop | Re-audit | 02 [36f1d8130259] |
| Test segment | Every brief pre-registers device | Mobile read separately | Blended read only | Add to brief | 05 [1f26cd618e2d] |

### 5.8 Behaviour signals (Clarity or Hotjar)

| what to check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| Rage clicks | Insights rate, then camera icon to recordings | Under about 1 to 2% and no blocking cause | Repeated clicks on a popup close, chat widget, or a control in the buy path | Remove or delay the blocker; recheck | 04 [9d9871ee324b] |
| Dead clicks | Insights, click map, recordings | Static items do not block purchase (press logos) | Pricing blocks, logo, product images, check marks clicked with no action | Add the expected action or make static nature clear | 04 [0eae610ddc62] |
| Excessive scrolling | Insights, recordings, scroll map | Very low rate; no hunting | Racing to find reviews, price, ATC; skipping a text wall | Move the item up or shorten | 04 [5b9da7dd1967] |
| Quick backs | Insights, recordings | Normal comparison | Leaving a PDP within seconds for missing info | Surface price, reviews, delivery, sizing sooner | 04 [5b9da7dd1967] |
| False clicks | Click map vs live page | Clicks sit on real controls | Clicks on button-styled non-buttons; clicks in empty space | Make them work or restyle; "massive" wins reported (03) | 03 [9568c40e1d88], 04 [09583734387e] |
| Screenshot validity | Heatmap screenshot vs live page | Real page captured | Popup or broken layout captured | Change screenshot | 04 [09583734387e] |
| Scroll checkpoints | Top, average fold, 75%, 50%, 25% | Key proof and CTA where most reach | Reviews or ATC reached by 25 to 30% | Move up | 04 [bc5a8130eee9] [edd07a1a15f6] |
| Reach vs clicks | Area map click share vs scroll reach | Aligned | High clicks, low reach; or high reach, no clicks | Placement test; relevance check | 07 [de4dfe536e94] [3043da84ee0c] |
| Engaged vs disengaged | Sort recordings by clicks and pages both ways | Clear difference in what engaged shoppers use | Sorts reflect page complexity, not intent | Read with caution; add filters | 04 [a1a3e1f62713] |
| Pattern confirmation | Count sessions and devices showing the pattern | Several sessions, 2+ devices | 1 recording | Keep watching before writing a hypothesis | 04 [11e64288067b] |
| Post-ship recheck | Fresh recordings of the new version | Friction gone; next issue found | Not rechecked | Schedule the recheck | 04 [0b8d2f6cc4d1] |
| Tool cost | Daily sessions vs plan allowance | Paying only for jobs used | Hotjar bill or sampling at high traffic for heatmaps alone | Move heatmaps and recordings to Clarity `[web check: pricing]` | 07 [3728f5d4ae33] |
| Survey coverage | Is there a post-purchase and an exit survey | Both live | Neither | P7 | 07 [f89dbadb9131], 03 [b4505f6c4061] |

### 5.9 Test validity (run before, during and after every test)

| what to check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| Repair or test | Is the current state objectively broken | Both versions viable | Bug, broken tracking, blocked CTA | Repair; do not test | 05 [3eca46fe9ba3] |
| Evidence gate | Count evidence points in the brief | 2 or more | Opinion only | Back to research | 05 [aad25dea9ed9], 03 [25979af2691c] |
| Powered | Sample table or calculator vs weekly page traffic | Planned sample in 2 to 4 weeks | Needs months; MDE under 10% at low volume | Bolder change, bigger page, micro primary, or research only | 05 [00c82f0de25d] [67f74e89d43e] |
| Relative vs absolute MDE | Read calculator input | Matches plan | +0.4 points confused with +20% | Recompute | 05 [00c82f0de25d] |
| Tails | Brief | Two-sided, or one-sided with documented reason | One-sided to hit significance | Revert, recompute | 05 [517a8bce6324] |
| Stopping rule | Brief names fixed horizon or a sequential engine | Named and followed | Stopped at first p < 0.05 | Result unreliable; re-run | 05 [e3ee87a025c5], 02 [699a7cd5ac4c] |
| Bayesian prior | Vendor docs | Prior and stopping protection stated | Flat hidden prior; stopped on a peek | Treat as peeked; re-run | 05 [e3ee87a025c5] |
| Runtime | Dates | 2 full weeks or more; each weekday twice; sample met | Under 1 week; split weeks | Extend only if pre-planned | 05 [5fae1beab1ba], 03 [7d481c590b57] |
| SRM | Chi-square on users | p above 0.001 | p < 0.001 or visible skew | Do not trust; find cause | 05 [370ed8c02e34] |
| Flicker | Load variant on slow mobile | No original flash | Flash then swap | Server-side; record anti-flicker cost | 05 [370ed8c02e34] |
| Tracking | Tool conversions vs backend orders per arm | Match | Pixel broke mid-test | Invalidate | 05 [3eca46fe9ba3] |
| Contamination | Traffic sources in the test | Retention traffic excluded or isolated; sticky bucketing | Klaviyo sends in the test; multi-click exposure to both arms | Cold-only page or ad-set split | 02 [699a7cd5ac4c] |
| Bots | Filter applied | Yes | No | Filter and re-read | 05 [370ed8c02e34] |
| Promo overlap | Marketing calendar vs dates | Clean window | Sale or holiday inside | Note confound; consider re-run | 05 [062507c94ee4] |
| QA | 2 to 3 passes on devices | Done | Bug in variant | Fix and restart | 03 [4d0785cdcf2b] |
| Concurrent tests | Test calendar | No overlap on the same page area | Two tests on one PDP area | Serialise | 03 [7d481c590b57] |
| Multiple comparisons | Count metrics and segments read | 1 primary; pre-registered segments; correction applied | Many metrics; post-hoc slices | Bonferroni or FDR; slices seed new tests | 05 [1f26cd618e2d] |
| Device direction | Pre-registered mobile vs desktop | Same direction | Blended win hides mobile loss | Investigate before shipping | 05 [1f26cd618e2d] |
| Guardrails | AOV, margin, returns, refunds, load, ATC | Flat or better | Any worse | Not a win | 05 [7eeb62d20124], 02 [dad9c85ea261] |
| Plausibility | Lift vs page maturity | 1 to 5% mature; 10 to 20% unoptimised | 50%+ | Twyman audit; replicate or hold out | 05 [370ed8c02e34] [8dc46d4893e1] |
| Novelty | Daily plot; first vs repeat exposure | Stable | Early spike that fades | Judge on stable period | 05 [5fae1beab1ba] |
| Inconclusive handling | Decision at full power | Recorded as "smaller than MDE"; not extended | Extended to chase significance | Close it | 05 [70db51ffb976] |
| Winner still live | Live-winner register vs site | Live | Overwritten by theme or team change | Restore | 03 [f09cfbc3ef44] |
| Platform sanity | A/A test | No difference | Significant A/A | Fix platform | 05 [0bda3b4d7e04] |
| Case study claim | Baseline, sample, runtime, validity stated | Stated | Not stated | Hypothesis only | 05 [370ed8c02e34], 06 |

