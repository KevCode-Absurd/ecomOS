---
name: wild-bet
owner: BRAND
version: 1
invoke_when: a wild bet candidate exists, from the backlog or a fresh proposal
inputs: idea bank folder 19-WLD, contribution margin, team capacity, brand values
outputs: backlog entry, screen verdict, bet type, 8-field bound, legal-review flag
---
# Wild bet (parent)

## Purpose
This is the entry point and generic bounding procedure for any wild bet, before it is known whether the bet is a new product line, a new market, a licensing deal, a wholesale/retail entry, or a pop-up. It keeps the backlog alive and applies the same discipline (a real bound before launch) to every type.

## Steps
1. Every month, source wild bet candidates: adjacent-industry moves worth borrowing, category norms this brand could credibly break, and gaps the brand's own research (reviews, tickets, social) has surfaced. Log each with a date and the specific norm or gap it targets.
2. When a bet is proposed by the founder or pulled from the backlog for action, screen it against the brand's stated values and current team capacity before spending any more time on it.
3. Classify the bet's type. This determines which child skill runs next: `wild-bet/new-line`, `/new-market`, `/licensing`, `/wholesale`, or `/retail-popup`.
4. Once the child skill returns its type-specific feasibility packet, write the 8-field bound: hypothesis, the category norm broken, budget cap, downside cap (a share of contribution margin, computed in code, never guessed), cohort and size, control design, a specific stop rule, and a read-point date.
5. Flag for legal review whenever the bet promises something, sends mail or texts, or gates access to anything; default to "needs review" when unsure.
6. Hand the bound to the founder gate before any execution brief is written.

## Checks
- A bet conflicting with a named brand value is flagged, never silently bounded.
- Downside cap is a computed share of contribution margin, not an estimate.
- All 8 bound fields are present and specific before the bound is presented; a missing read point or stop rule blocks presentation entirely.

## Output
`{backlog_entry, screen_verdict, bet_type, 8_field_bound: {hypothesis, norm_broken, budget_cap, downside_cap, cohort, control, stop_rule, read_point}, legal_review_flag}`

## Example
Backlog entry, Sep 2026: "adjacent brand X ran a 48-hour founder-only pre-drop; this brand has never tried scarcity pricing": bet_type classified as new_line once proposed, routed to the new-line child for sizing before bounding.
