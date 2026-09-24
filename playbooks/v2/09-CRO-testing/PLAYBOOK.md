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

