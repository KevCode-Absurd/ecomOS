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

