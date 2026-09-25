---
name: messaging-hierarchy-builder
owner: BRAND
version: 1
invoke_when: a new campaign, page or channel needs its ranked message stack written
inputs: positioning statement, avatar record and objection map, the page/channel type
outputs: big idea, ranked supporting messages, page-fitted message stack
---
# Messaging hierarchy builder

## Purpose
Every asset on a page or channel should lead with the same one idea and back it the same way. This skill produces the ranked stack the executing specialist then writes the actual page or ad copy from.

## Steps
1. State the single big idea this page or channel must lead with, drawn directly from the approved positioning statement, never invented fresh per page.
2. Pull the strongest supporting messages from the objection map and avatar record's forces, ranked by how much buying friction each one removes, capped at 3.
3. Adjust order and depth for the specific page or channel type: a homepage leads broad, a PDP leads with the objection most relevant at that SKU's price point, an email leads with the relationship stage, an ad leads with the hook.
4. Run every message in the stack through `shared/claim-check` against the claims tiers.

## Checks
- The big idea traces directly to the current positioning statement.
- Each supporting message maps to a named objection or force, not a generic benefit.
- The stack respects the writing rules: short sentences, digits, no em dashes.

## Output
`{big_idea, ranked_supporting_messages: [...], page_fitted_stack}`

## Example
PDP stack for a ₹4,500 chain: big idea "wear it daily without worry," supporting messages ranked: (1) tarnish-resistance claim with test data, (2) size/length guide link, (3) return policy callout, matched to the top 3 PDP-stage objections in the objection map.
