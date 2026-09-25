---
name: content-lifecycle
owner: ORG
version: 1
invoke_when: weekly, to review the content library's shelf life
inputs: content/asset library with tags and dates, cross-channel usage log
outputs: reuse candidates by surface, a retirement list naming every surface an asset still lives on
---
# Content reuse and retirement tracking

## Purpose
Get more use out of content that already works (PDP, email, DM, post-purchase) before it is created new, and pull down content that has gone stale (a since-changed price, an ended season, a discontinued SKU) from every surface it reached, not just the original post.

## Steps
1. Pull every library asset with publish date, SKU tag and format.
2. Apply the right shelf-life rule: seasonal and price-specific content expires fast, evergreen how-tos last.
3. For still-valid assets, find an unused reuse slot: PDP gallery, email, DM auto-reply, post-purchase flow.
4. For expired assets, mark for retirement and list every surface it currently appears on.
5. Return both lists together so retirement is complete, not partial.

## Checks
- Every asset has a shelf-life rule applied, never a default guess.
- Retirement covers every live surface, not just the origin post.
- Price- or stock-specific content never stays live past its accuracy window.

## Output
{reuse_candidates[], retire_list[]}

## Example
A Diwali gifting reel from last year is retired from the PDP gallery and the post-purchase flow, both places it had been reused, not just the original Instagram post.
