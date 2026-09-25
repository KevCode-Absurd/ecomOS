---
name: prod/screen-candidate
owner: PROD
version: 1
invoke_when: a product or category candidate needs a fast pass before any real research time is spent on it
inputs: candidate name or category, brand store tags, idea bank filter, public trend data
outputs: pass/caution/reject verdict with a trend and saturation read
---
# Screen a candidate

## Purpose
Kill a weak candidate before a single hour of deep research is spent on it. This is the front door of the research
funnel: every candidate that reaches sourcing spend passed through here first.

## Steps
1. Run the fixed checklist against the candidate: is the category big enough, is there real pain evidence (not just
   founder interest), is there scarcity or a real gap, does it fit the brand's store model.
2. Pull the category's multi-year trend line. A candidate riding a single-year spike gets flagged, not killed outright.
3. Count existing sellers or listings in the category to read competitive saturation. A crowded category needs a
   sharper angle than an open one.
4. Score every check pass, caution or reject, each with a one-line reason a person could check.
5. Combine into one verdict. A caution needs two or more supporting checks before it proceeds; a single caution alone
   does not clear the gate.

## Checks
- Every check states its reason; "just doesn't feel right" is never a valid reason.
- The trend line is real data, not a single number from memory.
- Saturation is counted, not guessed at.

## Output
{verdict, checks[{name, result, reason}], trend_read, saturation_count}

## Example
Verdict: caution. Category size: pass (₹40 Cr category, growing). Pain evidence: pass (3 review threads, 40+ mentions
of the same complaint). Scarcity: caution (2 close competitors, no clear open gap yet). Trend: 3-year CAGR 18%.
Saturation: 34 sellers on the nearest marketplace search. Verdict rests on the differentiation workflow closing the
scarcity gap before this proceeds.
