---
name: production-ops/predictive-scoring
owner: crea-paid-creative-copy
version: 1
invoke_when: a draft batch is finished and needs a pre-spend score before it
  enters paid testing
inputs: finished draft batch, this account's own past predictive-score-to-
  outcome record
outputs: predicted score per draft, fix list, calibrated post-fix score
---
Purpose: catch a weak, specific element (a muddy hook, a headline-image
mismatch, a hidden CTA) before spend touches it, while being honest about
whether the score itself has actually predicted this account's real results.

Steps
1. Run each draft through the predictive pass and record which specific
   element it flags: hook clarity, headline-image mismatch, CTA visibility,
   never just a single overall number with no detail behind it.
2. Check whether this account's own past predictive scores have actually
   tracked its real 14-day verdicts; if the match rate has been weak, state
   that plainly and treat the score as a rough filter, not a green light.
3. Send any flagged draft back for the exact fix named, not a general
   instruction to "make it better."
4. Re-run the pass on the fixed draft and log the post-fix score next to the
   original, building the calibration history for next time.
5. Clear the batch only once every draft passes, or carries a named,
   founder-accepted risk.

Checks: flags name a specific element; calibration against real outcomes is
shown, not assumed accurate.

Output: per-draft scores, the fix list, and the calibrated post-fix scores.

Example: a draft flags "CTA visibility" specifically, not a vague low score;
after the CTA is enlarged and repositioned, the re-score clears it.
