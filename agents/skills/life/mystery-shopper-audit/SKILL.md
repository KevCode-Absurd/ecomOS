---
name: mystery-shopper-audit
owner: LIFE
version: 1
invoke_when: running the CX leg of the quarterly mystery-shopper brand journey
  audit (browse through a real support query)
inputs: checkout/site access, support contact channel, the brand's own stated
  promises (delivery estimate, guarantee, response time)
outputs: gap catalogue with evidence, routed to the workflow that owns each fix
---
# Mystery-shopper journey audit (CX leg)

## Purpose
Walks the brand's own post-purchase and support experience as a real customer
would and catalogues every place it falls short of what the brand itself states,
with evidence, then routes each gap to the specialist who owns the fix.

## Steps
1. Place a real or test-gateway order, logging every step's timestamp.
2. Quote every promise made at checkout and in the confirmation (delivery
   estimate, guarantee terms) verbatim.
3. Send a genuine, realistic support question through the brand's own channel.
4. Time the actual response against what the brand states or implies as its
   response time.
5. Catalogue every gap between promise and reality, each with a timestamp,
   screenshot or quoted message as evidence.
6. Route each gap to the owning workflow (delivery communication, support
   templates, checkout).

## Checks
Every gap is evidenced, not impressionistic. Comparison uses the brand's own
stated promise, never an assumed industry standard.

## Output
A gap catalogue, each entry routed to a named owning workflow or agent.

## Example
"Promise: '2-4 day delivery.' Reality: delivered day 6, no proactive update sent.
Routed to LIFE-W13 (delivery communication) for a stronger mid-transit update."
