# Orchestrator routing

How a break becomes work. The Orchestrator does not decide what to do; Diagnose and Propose do, and the founder approves. The Orchestrator decides who does it and with which workflow, from this table. Every row is deterministic. When no row matches, the Orchestrator does not improvise: it writes a routing proposal for a person to review.

## 1. From break to specialists

Diagnose names the break by pipeline stage. Propose builds the top 10 with the specialists that own that stage's surfaces. Each card carries `owner_specialist` and `workflow_id` chosen from the specialist's selection rules.

| Break (pipeline stage) | Bottleneck code | Surfaces audited | Specialists Propose asks | Typical workflows |
|---|---|---|---|---|
| Ad reach and cost | acquisition_volume, acquisition_efficiency | ad accounts, creatives, landing pages | MEDIA, CREA, SITE | MEDIA account audit, CREA creative test, SITE landing page |
| Page loads | site_speed | key pages on the speed lab | SITE | SITE speed audit and fix chain |
| Product views to add to cart | conversion | product and collection pages, search, reviews | SITE, CREA (copy), BRAND (avatar fit) | SITE CRO test, SITE page rebuild |
| Checkout to order | conversion, trust_brand | checkout, payment methods, address validation, policies | SITE, LIFE (offer), MONEY (payment ops) | SITE checkout audit, LIFE offer redesign |
| Order value | aov | offers, bundles, pricing, free shipping threshold | LIFE, PROD (bundle supply) | LIFE offer design |
| Repeat and retention | repeat_retention | flows, segments, CX, support reasons | LIFE, BRAND (voice) | LIFE flow build, LIFE win-back |
| Margin | margin_cogs | landed cost, discounting, shipping cost, returns and chargebacks | PROD, MONEY, LIFE (discount policy) | PROD landed cost, MONEY contribution margin |
| Cash and stock | cash_inventory | stock cover, reorder, settlements, payables | PROD, MONEY | PROD reorder, MONEY cash forecast |
| Fulfilment and CX | fulfilment_cx | carriers, failed deliveries, returns, chargebacks, support | PROD, LIFE | PROD courier scorecard, LIFE returns handling |
| Trust and brand | trust_brand | claims, reviews, positioning, answer engines | BRAND, ORG (AEO), QA | BRAND consistency audit, ORG facts page |
| Organic demand | acquisition_volume (organic) | content, SEO, answer engines | ORG, BRAND | ORG calendar, ORG SEO page briefs |
| Measurement | measurement_data | tracking, contract freshness, attribution | MONEY, BRN | MONEY tracking audit, BRN collector fix |
| Team capacity | team_capacity | queues, wait times, SOP coverage | MONEY (ops), ORCH | MONEY hiring or SOP, ORCH queue rebalance |
| Risk and compliance | risk_compliance | security scan, legal pages, marketplace health | MONEY (security), SITE, PROD | MONEY security fix list |

## 2. From decision to dispatch

| Decision on a card | Registrar | Orchestrator dispatch |
|---|---|---|
| Let the agent do it | entry: approved, owner = specialist | package context: card, brain sections the workflow lists, registry context, Scout references if the workflow asks; start the workflow; route the artefact through QA Gate; deliver |
| Send to a person | entry: waiting, owner = person | run the workflow up to its brief step; deliver the brief to the person's queue; watch for "done" to schedule the read |
| Not now, with reason | entry: parked, expiry from the reasons table | nothing runs; the card returns when the reason expires |
| Decision in chat | same as the button pressed | same |

## 3. Context package per dispatch

The Orchestrator assembles the 6-part prompt from the workflow's declared needs, never the whole brain.

| Part | Source | Rule |
|---|---|---|
| Role and scope | the specialist's agent file | fixed |
| Brand context | brain sections named in the workflow's `inputs_required` | quoted with freshness; missing sections stop the run with a founder question |
| Numbers | metric contract fields the workflow names | computed in code; unavailable stays unavailable |
| Task | the card, the founder's reason, registry history for the idea on this brand, Scout references when the workflow's first step asks | verbatim |
| Rules | global rules plus the agent's own | fixed |
| Output contract | the workflow's `outputs` and `qa` | the QA Gate checks against it |

Skills are not packaged. The specialist loads a skill at the step that names it.

## 4. Selection inside a specialist

Each specialist's wave 4 notes hold a decision table: given (bottleneck, card type, format, channel, platform, store tags) → workflow → skills. The Orchestrator passes the card's fields; the specialist matches. A sub-skill is chosen by its `select_by` switches (format, channel, platform, flow type, marketplace, supplier region). If two sub-skills match, the more specific wins; if none match, the parent skill runs and the gap is logged for a skill draft.

## 5. Scheduled work, no card needed

| Trigger | Agent | Workflow |
|---|---|---|
| Daily 04:00 | BRN | collectors, crawl and diff, contract compute |
| Daily 04:20 | DIAG, PROP, QA | break, top 10, gate |
| Daily | MEDIA, LIFE, PROD, MONEY | reads on running items (agent_does capabilities with a daily trigger) |
| Weekly | SITE (speed), MONEY (security), BRN (competitor snapshot), SCT (winners tagging), QA (claims audit), ORCH (business review) | as named in each agent's capability index |
| Monthly | ORCH (client report), ORG (calendar), MONEY (close), PROP (candidates file curation) | as named |
| Read point | REG | metric read, result, prior update |

## 6. Hand-offs between specialists

A workflow may hand a step to another specialist by naming it. The Orchestrator queues the hand-off as a sub-task under the same registry entry.

| From | To | What crosses |
|---|---|---|
| CREA | MEDIA | audience spec, creative set, launch checklist |
| MEDIA | CREA | fatigue read, winners and losers by angle |
| SITE | ORG | crawl findings that are content, not code |
| ORG | SITE | technical SEO briefs, speed findings |
| LIFE | CREA | copy blocks for flows (CREA writes words, LIFE owns timing) |
| PROD | MEDIA | feed and marketplace ad handoff |
| PROD | MONEY | landed cost, PO cash timing, settlements |
| MONEY | all | contract fields, tracking fixes, spend lines |
| BRAND | all | avatars, voice sheet, claims to tier (via BRN) |
| any | SCT | reference requests |
| any | QA | every artefact before delivery |

## 7. When nothing matches

The Orchestrator writes a routing proposal: the card, the closest rows, why they do not fit, and a suggested workflow outline. It goes to a person. Nothing runs until a row exists.
