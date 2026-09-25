---
name: deliverability-audit
owner: LIFE
version: 1
invoke_when: the weekly deliverability check, or a sharp drop in a sender-health
  figure
inputs: ESP sender data, metric contract
outputs: health report plus repair-ladder plan
---
# Deliverability and list-hygiene audit

## Purpose
Monitors sender reputation and inbox placement, keeps the list clean, and runs the
repair ladder in the right order when a figure degrades, treating content quality
as the first fix, not authentication settings.

## Steps
1. Pull domain/IP reputation, bounce and spam-complaint rates, and the unengaged
   list share for the week, from the ESP's own reported numbers.
2. Compare against the brand's own trailing 8-week baseline first.
3. If degraded, diagnose content (subject lines, spam-trigger words, image-to-text
   ratio) before touching sending infrastructure.
4. Run the repair ladder in order: fix content, pause to the most unengaged
   segment, suppress or re-permission chronic non-openers, check authentication
   (SPF/DKIM/DMARC) only if earlier steps do not explain it.
5. Update suppression per the standing hygiene policy.

## Checks
Content checked before infrastructure. No recent purchaser (last 90 days) suppressed
without a specific, named reason.

## Output
Weekly health report plus a repair-ladder log of steps taken and pending.

## Example
"Complaint rate up 0.1pt vs baseline. Cause: last Tuesday's subject line flagged
2 spam-trigger words. Fix: rewrite subject rule; no infrastructure change needed."
