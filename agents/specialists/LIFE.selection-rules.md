# LIFE wave 4: workflows, skill tree and selection rules

30 workflows (LIFE-W01 to LIFE-W30) cover all 53 capability ids in LIFE.caps2.txt.
43 skills, including the two required nested trees: `build-flow` (8 sub-skills by
flow type) and `message` (3 sub-skills by channel). Shared skills reused by id.

## How LIFE picks a workflow

Given (bottleneck, card type, flow type, channel, store tags):

| Bottleneck / card | Flow type or focus | Channel | Store tag | Workflow |
|---|---|---|---|---|
| flow missing/broken | welcome, browse-cart-abandon, post-purchase, win-back, sunset, back-in-stock, replenishment, loyalty-vip | email/sms/whatsapp | any | W04 |
| India COD/RTO recovery | cart-abandon, order-update, COD-to-prepaid, NDR | whatsapp | india, cod | W09 |
| segmentation stale | - | - | any | W05 |
| weekly send plan | campaign | email/sms | any | W06 |
| deliverability degraded | - | email | any | W07 |
| channel cost/cadence unclear | - | sms/whatsapp/push | any | W08 |
| order-gap/churn signal | win-back routing, sub. save | any | subscription | W12 |
| WISMO tickets high | delivery comms, unboxing | any | any | W13 |
| return rate/speed issue | returns | - | any | W14 |
| support drift, AI agent | reply templates, tagging | any | any | W15 |
| review volume/response | review request/response | email, feed | any | W16 |
| offer/bundle/GWP/upsell card | offer package | - | any | W18 |
| subscription churn/cancel | subscription | any | subscription | W20 |
| marketplace ticket/claim | - | - | amazon, flipkart | W25 |
| India grievance/notice | - | - | india | W28 |
| considered-purchase warranty | - | - | luxury | W29 |

Each workflow above names its skills in LIFE.workflows.json. `build-flow` selects
`flow_type` from the 8 types listed; `message` selects `channel` from {email, sms,
whatsapp}. Every other skill is single-purpose; the calling workflow implies it.

## When no workflow matches

LIFE never improvises silently. Given a job with no matching workflow, LIFE: (1)
says plainly that none exists; (2) drafts a workflow proposal in the same shape
as the 30 above, citing the nearest existing workflow and what differs; (3) sends
the draft to a person for review before it enters the catalogue, never running it
un-reviewed; (4) if urgent and close to a modelled job (a new flow type outside
the 8), runs `build-flow`'s generic procedure and flags the type as
not-pre-modelled, so the read gets extra caution.

## Design notes

Capabilities that are the same job at different flow types (welcome through
loyalty-vip) share one workflow, W04: the procedure is identical each time
(confirm trigger, set filters, map steps, draft copy, check discount, assemble
brief); flow type is a skill-tree switch, not eight jobs. The same logic combines
C13/C14/C15 into the campaign pipeline (W06), C23/C24/C25 into one post-purchase
project (W13), C27/C49 into support governance (W15), C28/C52 into the review
program (W16), and C36/C39/C40/C41/C42 into one offer package (W18), since a real
specialist ships each as one connected deliverable, not five meetings.

Flagship workflows, at the founder's media-buying depth (12-14 steps, an
ask_founder_if gate, a registry entry): W04 (order-gap/flow type to live draft),
W06 (calendar to send-ready draft), W07 (deliverability fix), W09 (WhatsApp for
India), W12 (order-gap routed to a save program), W14 (returns), W15 (support
reply/tagging), W16 (review program), W18 (offer design from margin/AOV), W20
(subscription health).

India-aware: W09 (COD-to-prepaid, NDR recovery), W12/G02 (RBI e-mandate re-auth,
RTO-aware win-back), W27 (gifting timed to Diwali), W28 (E-Commerce Rules SLA,
e-Daakhil).

Shared guardrails: `discount-policy-check` gates W04, W06, W09, W18, W19, W21,
never reimplemented per workflow. `claim-check` gates every customer-facing
draft. Every founder_gate workflow ends in `plain-english-card` and logs through
`registry-entry`.

Out of scope: capabilities absent from LIFE.caps2.txt (C21, C31, C32, C34, C35,
C37, C44, C48, C50, C51, C54-57, C61-64, C66) stay in the full index for later.

## Coverage check

All 53 required capability ids appear in the workflows file; all 30 workflows
have 6-14 steps; all 43 skills validate against schema. `build-flow` has exactly
8 sub-skills (the 7 named in the brief plus loyalty-vip); `message` has exactly 3
sub-skills (email, sms, whatsapp).
