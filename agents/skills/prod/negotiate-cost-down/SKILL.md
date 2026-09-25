---
name: prod/negotiate-cost-down
owner: PROD
version: 1
invoke_when: a sample has passed and a final price needs locking, or a standing supplier relationship needs a
  cost review
inputs: the passed sample, a backup factory quote, a competitor teardown if available, category factory margin norms
outputs: the negotiated price and terms, with the leverage used stated
---
# Negotiate a cost-down with real leverage

## Purpose
Asking for a discount with no leverage rarely moves price and can damage the relationship. This skill builds real
leverage first, then negotiates from it, and never asks for a cost-down that would strain the relationship for more
than it is worth.

## Steps
1. Build real leverage before asking for anything: a vetted, willing alternate factory at a comparable or better
   price; a teardown of a competitor's comparable product showing where cost could come out; the category's normal
   factory margin so an ask is grounded in what is realistic, not arbitrary.
2. Present the ask with the specific leverage named plainly: "we have a comparable quote at X" carries far more
   weight than "can you do better."
3. Confirm the final price and terms in writing before treating the negotiation as closed.
4. Book the production slot at the exact factory that passed the sample gate: never a sister factory or a
   different production line, even if it is cheaper.

## Checks
- The leverage used is real: a vetted alternate that genuinely exists, not an empty threat.
- The booked slot is confirmed at the exact factory and line that passed the sample.

## Output
{leverage[], ask, outcome{price, terms}, slot_booked}

## Example
Leverage: a verified backup factory quoted 8% lower for the same spec. Ask presented with that quote referenced.
Outcome: factory matched within 3%, citing relationship history; final terms locked at 30/70 split. Slot booked for
week 6 at the same factory that passed the sample.
