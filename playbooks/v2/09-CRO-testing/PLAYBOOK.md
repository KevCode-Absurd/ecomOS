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

