# BRAND wave 4: selection rules and notes

## How BRAND picks a workflow

The trigger or card names a bottleneck and a card type, sometimes a format, channel, platform or store tag. BRAND matches bottleneck plus card type first, then narrows by the rest.

| bottleneck | card type / signal | workflow | key skill |
|---|---|---|---|
| trust_brand | avatar evidence stale or missing | W01 research sweep -> W05 build avatar | research-customers/*, jtbd-writer, avatar-record-builder |
| trust_brand | a gap passive data can't fill | W02 interviews | research-customers/interviews |
| trust_brand | confirm a finding at scale | W03 survey | research-customers/surveys |
| trust_brand | positioning weak or contested | W04 -> W09 -> W10 | category-ladder-and-xy-map, positioning-statement |
| aov, margin_cogs | new niche or product proposed | W11 sizing/pricing | market-sizing, pricing-audit |
| trust_brand | new SKU, collection or brand name needed | W12 naming | name-screening-and-packaging (scope: brand\|sku) |
| trust_brand | new product line or market proposed | W13 architecture | none, framework applied inline |
| trust_brand | voice drift, or no voice sheet | W14 story/voice/promise | voice-sheet-builder, brand-story-and-promise |
| conversion, trust_brand | page/campaign needs a message stack | W15 messaging | messaging-hierarchy-builder |
| trust_brand | new brand or major refresh | W16 identity/guidelines | identity-brief-builder, brand-guidelines-builder |
| trust_brand | drift check, monthly/quarterly | W17 audit | brand-consistency-audit |
| trust_brand | monthly health check | W18 health | brand-health-tracking |
| repeat_retention | design an exclusive cohort | W19 -> W20 | community-cohort-design, ambassador-program-ops |
| trust_brand | launch, PR moment, monthly sweep | W21 PR | pr-angle-builder, media-list-builder, earned-media-sourcing (type) |
| trust_brand | complaint spike, viral criticism | W22 crisis | reputation-risk-monitor |
| trust_brand | collaboration proposed, biannual sweep | W23 partnership | partnership-sourcing-sweep, partnership-screen |
| trust_brand, acquisition_volume | in-person activation fits avatar | W24 event/pop-up | event-popup-design |
| trust_brand | competitor changes, quarterly win-loss | W25 competitive intel | competitive-intelligence |
| team_capacity, risk_compliance | wild bet sourced or proposed | W26 wild bet | wild-bet, wild-bet/<bet_type> |
| team_capacity | shortlist ready, before paid research | W27 pretest | ai-persona-pretest |
| team_capacity | founder asks an operating question | W28 advice | none, skill null |
| risk_compliance | new SKU, channel, packaging change | W29 packaging brief | packaging-label-brief |
| trust_brand | equity audit shows brand failing to win | W30 rebrand | none direct; sequences W10, W12, W14, W16 |

## Sub-skill switches

- **research-customers** by `source`: reviews, tickets, social, onsite_behavior are agent_does, monthly, no person needed. interviews and surveys are human_assist, run only for a named gap, never a general sweep.
- **wild-bet** by `bet_type`: new_line, new_market, licensing, wholesale, retail_popup. The parent runs first (backlog, screen, generic bound); type only changes the feasibility check and the brief's shape.
- **name-screening-and-packaging** by `scope`: brand (full 7-quality screen, clearance, story, tagline) or sku (lighter, defaults to a descriptive title).
- **earned-media-sourcing** by `type`: thought_leadership (monthly, founder placements) or award (quarterly, best-of submissions).
- **avatar-record-builder** by `task`: build (new avatar) or refresh (quarterly audit, never edits without new evidence).

## When no workflow matches

BRAND never improvises silently. When a card names a bottleneck, format or tag no row above covers, BRAND:

1. States plainly that nothing fits, naming the closest 1-2 candidates and why each falls short.
2. Drafts a workflow proposal in this file's schema (id, steps, inputs, outputs, checks), built from the idea bank and the nearest existing skills.
3. Sends the draft to a person for review before it ever runs, matching the shared rule for a skill drafted after 3 repeats.
4. Logs the gap to the registry, so a repeated pattern becomes a real workflow next review, not a one-off script each time.

## Boundary notes

BRAND stops at the angle map, avatar record, positioning, voice sheet and briefs. Paid Creative/Copy writes the copy, Site builds the page, Lifecycle runs loyalty at scale, Money and Ops owns the P&L and hiring math. Every founder_gate workflow shows sources and a plain verdict before anything ships. agent_does workflows run on schedule; the founder only sees the output.
