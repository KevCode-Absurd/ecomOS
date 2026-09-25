---
name: compliance/copy-craft-rules
owner: crea-paid-creative-copy
version: 1
invoke_when: any drafted copy needs the account's fixed writing rules applied,
  before the separate claim-tier check
inputs: draft copy
outputs: edited copy, reading-level score, edit log
---
Purpose: apply the same fixed craft rules to every draft regardless of which
skill wrote it, so voice and readability never drift by writer or by format.

Steps
1. Score reading level in code (not by eye) and rewrite until the draft
   clears the grade-10 target; a draft that reads clever but tests at grade
   13 gets simplified, not defended.
2. Check single-idea discipline: exactly one dominant appeal and exactly one
   CTA per asset, unless the approved idea explicitly calls for testing two
   in the same piece.
3. Order proof points from strongest real evidence to weakest, cutting any
   proof point with nothing behind it rather than padding the count.
4. Cut every em dash, every inflated or vague superlative with no fact
   behind it, and any phrasing that reads as generically AI-written rather
   than in the brand's real voice.
5. Replace spelled-out numbers with digits throughout.

Checks: grade-10 or below; single idea and single CTA; no em dash; digits,
not spelled-out numbers.

Output: the edited copy, its reading-grade score, and a short edit log
naming what changed and why.

Example: "we're absolutely thrilled to introduce an incredible new way to
elevate your morning" becomes "start your morning with 2 minutes of real
energy, no crash."
