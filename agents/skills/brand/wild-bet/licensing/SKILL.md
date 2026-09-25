---
name: wild-bet/licensing
owner: BRAND
version: 1
invoke_when: the bet's type is a brand licensing deal, in either direction
inputs: proposed counterparty, category royalty norms, brand guidelines
outputs: feasibility packet, type-specific execution brief
---
# Wild bet: licensing deal

## Purpose
A licensing deal risks the brand's name and quality reputation in someone else's hands (or takes on someone else's IP under this brand's name). This skill checks the deal's economics and control terms before any negotiation.

## Steps
1. Research royalty norms for this product category and deal scale, from public deal reports or industry sources, dated.
2. Build a licensee (or licensor) scorecard: financial capacity to perform, fit with the brand's category and story, existing distribution reach, and any public quality-control or reputation history.
3. Draft deal-memo terms for the founder to negotiate from: royalty rate range, minimum guarantee, explicit quality-control approval rights on any product carrying the brand name, term length, and an exit clause if quality slips.
4. Flag legal review as mandatory for any licensing deal; this is never a bet the agent bounds without a lawyer's terms review.

## Checks
- Royalty norms cite a real, dated source, not a guess.
- Quality-control rights are explicit line items in the memo, not assumed to be standard.
- Legal review flag is always set to required for this bet type.

## Output
`{feasibility_packet: {royalty_norms, licensee_scorecard}, execution_brief: {deal_memo_terms, legal_review: required}}`

## Example
Proposed licensee scores strong on distribution (200+ retail doors) but weak on quality-control history (2 public recalls in another category); scorecard flags this as a founder discussion point before terms are drafted.
