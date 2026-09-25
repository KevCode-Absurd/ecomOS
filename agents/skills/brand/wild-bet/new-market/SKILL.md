---
name: wild-bet/new-market
owner: BRAND
version: 1
invoke_when: the bet's type is entry into a new country or region
inputs: target region, current regulatory/tax posture, logistics partner options
outputs: feasibility packet, type-specific execution brief
---
# Wild bet: new market entry

## Purpose
Entering a new country or region carries regulatory, tax and logistics exposure a domestic wild bet does not. This skill front-loads exactly those checks so the founder decides with real constraints, not just opportunity size.

## Steps
1. Check what regulatory registration, import duty, or product-compliance requirement applies to selling into the target market (for example, a US FDA-adjacent labeling rule, or an EU CE-style requirement, depending on category).
2. Check the tax posture: for a new US state, sales tax nexus and registration thresholds on the home side; for a new country, US export treatment plus import duty, VAT (EU or UK) or GST on the destination side (GST applies only when the destination is India, markets: IN); state it in plain terms, flagging what needs a real accountant's sign-off versus what is a simple lookup.
3. Check who already competes there and at what price, so the entry is not blind.
4. Check logistics feasibility: realistic shipping cost and delivery time to that region, and how returns would even work.
5. Write the execution brief around the smallest reversible test (a limited SKU set, a marketplace listing rather than a full localized site) before any larger investment.

## Checks
- Regulatory and tax findings are specific to the named country, not assumed from general knowledge.
- Logistics costs are from a real quote or a published carrier rate, not estimated.
- The brief proposes the smallest reversible entry, not a full market launch.

## Output
`{feasibility_packet: {regulatory, tax, competitor_read, logistics}, execution_brief}`

## Example
Target: UAE. Regulatory check flags a municipality trading-license requirement for a local entity; recommendation is a marketplace-only test (Namshi/Noon) instead of a owned-site launch, pending that entity question.
