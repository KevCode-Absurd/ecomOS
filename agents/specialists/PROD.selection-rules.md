# PROD wave 4: selection rules and notes

30 workflows, all 72 capability ids covered exactly once. 45 skills, including the two required
nested trees: `source` by supplier region (india, china) and `list-on-marketplace` by marketplace
(amazon, flipkart, myntra, nykaa, blinkit, zepto). All ids prefixed `prod/` unless marked shared.

## How PROD picks a workflow

Match top to bottom on the trigger, card or scheduled event. First match wins.

| bottleneck / event | trigger | channel / platform / tag | workflow | key skill |
|---|---|---|---|---|
| new product idea | candidate, on demand | any | W01 | screen-candidate |
| line extension | on demand | hero SKU exists | W02 | differentiation-angle |
| funding decision | on demand | any | W03 | margin-compliance-gate |
| angle needs field proof | on demand | any | W04 | shared/web-research-budgeted |
| new SKU / spec change | event | any | W05 | build-tech-pack |
| need a supplier | on demand | region: india | W06 | source/india |
| need a supplier | on demand | region: china | W06 | source/china |
| quotes needed/received | on demand | any | W07 | rfq-quote-compare |
| sample received | event | any | W08 | sample-qc-gate, negotiate-cost-down |
| deal closing | event | any | W09 | payment-terms-structure |
| shipment ready | event | any | W10 | shipment-readiness |
| onboarding/billing/defect | event, per cycle | any | W11 | sourcing-audit, defect-capa-trace |
| weekly reorder | weekly | channel: dtc or amazon | W12 | reorder-point-calc |
| structural/dead-stock risk | monthly, weekly | any | W13 | inventory-risk-flag |
| new channel / peak season | continuous, annual | any | W14 | inventory-network-plan |
| 3PL/WMS/returns setup | on demand, weekly | domestic fulfilment | W15 | fulfilment-ops-setup |
| daily shipping / NDR | daily, real time | any | W16 | daily-shipping-ops |
| monthly courier review | monthly | any | W17 | courier-scorecard |
| lost/damaged/reimbursement | event, weekly | courier or marketplace | W18 | claims-file |
| export/offline/recall/custom | event | type: one of the 4 | W19 | non-standard-ops/\<type\> |
| Amazon candidate | on demand | platform: amazon | W20 | amazon-opportunity-screen |
| Amazon economics | monthly | platform: amazon | W21 | amazon-fee-model |
| listing build/refresh | event | platform: any of the 6 | W22 | list-on-marketplace/\<platform\> |
| FBA shipment | event | platform: amazon | W23 | fba-shipment-prep |
| Amazon launch/account/Registry | event | platform: amazon | W24 | amazon-launch-sequence |
| weekly health check | weekly | any marketplace | W25 | marketplace-health-monitor |
| sales change / growth plan | on demand | platform: amazon | W26 | amazon-performance-review |
| feed build / quality audit | daily, weekly | any | W27 | catalogue-feed-audit |
| quick commerce onboarding | on demand | platform: blinkit/zepto/instamart | W28 | quick-commerce-onboard |
| quick commerce ops | weekly, daily | platform: blinkit/zepto | W29 | quick-commerce-ops |
| Legal Metrology/FSSAI/EPR | monthly, quarterly | regulated SKU | W30 | regulatory-register-track |

## Picking a sub-skill from a task

The `select_by` switch reads the task's own field, never a guess:
- `source`: the spec's stated or brand-default supplier region.
- `list-on-marketplace`: the target marketplace on the card or listing request.
- `non-standard-ops`: classifies the event into exactly one of the four types before routing;
  a request matching two types is split into two runs.

## When no workflow matches

PROD never improvises silently.
1. State which capability or job the task resembles and why no row above covers it.
2. Draft a workflow proposal in the same shape as the 30 above, from the nearest capability and
   existing skills.
3. Log the proposal to the registry and send it to a person for review before it is used; it is
   never run as if approved.
4. A task that repeats unmatched three times becomes a candidate for a real skill, per the
   standing lifecycle rule in `agents/README.md`.

## Notes

- Some workflows deliberately group several capability ids that are one real job at different
  cadences (W11 covers onboarding audits, billing-anomaly watching and SLA tracking together,
  since one sourcing/ops manager owns all three). Capability ids stay separate and traceable
  inside each workflow's `capabilities` array; none are dropped or merged away.
- The recall path inside W19 and every step of W24 before launch spend carry an explicit
  `ask_founder_if`, on top of their `founder_gate` autonomy, so neither gate can be skipped by
  treating the workflow as routine.
- `MONEY-C03`, `MONEY-C37` and `MONEY-C70` sit inside PROD workflows because PROD produces the
  inputs (landed cost, PO governance data, SLA logs) that Money and Ops owns and confirms; PROD
  never treats these as its own final output.
- `LOOP-C34` sits inside W17 because the renegotiation draft depends on the courier scorecard
  PROD already owns; it still reaches the founder gate before any courier is contacted.
