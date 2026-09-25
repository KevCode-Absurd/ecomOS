---
name: angle-and-test/format-economics
owner: crea-paid-creative-copy
version: 1
invoke_when: a concept is set and the format still needs choosing, compared
  by real economics, not habit or ROAS alone
inputs: angle brief, test brief, product's education/demo need, account's own
  cost-per-asset and format hit-rate history
outputs: format decision with the comparison shown
---
Purpose: pick the ad format from this account's own numbers, since a format
with a lower hit rate but a much lower cost per asset can beat a flashier,
expensive format on real profit per ad.

Steps
1. List every format the concept could reasonably run as: static, native
   platform format, UGC video, founder video, carousel, catalogue.
2. Pull this account's own cost-per-asset and win-rate history by format,
   using metric-read; a brand-new account with no history falls back to the
   product's education need alone, stated as such.
3. Compute expected profit per ad for each candidate format: hit rate times
   the average result value of a winning ad in that format, minus the real
   cost to produce one asset in that format.
4. Weigh this against the product's real education or demonstration need; a
   product that needs to be seen in motion should not default to static just
   because static is cheaper, if the computed profit favors video anyway.
5. State the final decision with the actual numbers shown, not a preference
   dressed as a conclusion.

Checks: decision has a number behind it; product's real demo need was
checked explicitly, not skipped.

Output: the format decision plus the profit-per-ad table that produced it.

Example: static costs 1/5th of a UGC video to produce and hits 22% of the
time versus 30% for UGC; on this account's numbers static still wins on
profit per ad because the cost gap outweighs the hit-rate gap.
