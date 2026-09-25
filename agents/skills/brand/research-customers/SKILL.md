---
name: research-customers
owner: BRAND
version: 1
invoke_when: a research cycle starts and the evidence source needs picking before mining begins
inputs: brand brain products, the research question, which connectors are live
outputs: per-source evidence packets, unmerged
---
# Research customers (parent)

## Purpose
This is the router for all customer research. It does not mine anything itself; it decides which source-specific sub-skill runs, in what order, and hands each one the same standing rule: nothing enters an avatar record without a source and a date.

## Steps
1. Read what the run needs: a general monthly sweep, or a specific open question a prior workflow could not answer.
2. For a general sweep, run reviews, tickets, social and onsite-behavior (all agent_does, no waiting on a person). For a specific gap, add interviews or surveys (human_assist, need a person to run them).
3. Route to each sub-skill by source. Each sub-skill owns its own connector, its own read pattern (star band, ticket tag, forum search, search-term log, guide, or questionnaire), and its own output shape.
4. If a connector for a picked source is not live (for example, no support desk export configured), mark that source unavailable in the packet rather than skipping it silently, so the founder knows a gap exists.
5. Return every sub-skill's packet, unmerged, to the calling workflow, which does the cross-source pattern check.

## Checks
- Every source that ran is named in the output.
- A source with no connector shows as unavailable.
- Packets are not merged or summarized here; that happens one level up, after cross-checking.

## Output
List of per-source packets: `{source, status: ran|unavailable, packet}`.

## Example
A monthly sweep for Gehna returns packets for reviews (12 tagged quotes), tickets (4 struggle themes), social (2 sub-avatar notes), and onsite-behavior (unavailable, no GA4 connector live yet).
