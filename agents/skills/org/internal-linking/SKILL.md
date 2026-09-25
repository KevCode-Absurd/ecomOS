---
name: internal-linking
owner: ORG
version: 1
invoke_when: monthly
inputs: site architecture, content inventory, orphan-page check, money-page list
outputs: linking map of links added, remaining orphans with a stated reason
---
# Internal linking program

## Purpose
Build and maintain links from content pages to money pages and back, fix orphan pages, and add navigational links on product and collection pages, so link equity and buyer paths both flow to where the store makes money.

## Steps
1. Run an orphan-page check for pages with zero internal links pointing to them.
2. Link content pages to the money pages they support, and money pages back to relevant guides.
3. Add navigational links between related products and collections.
4. Fix every orphan found, either with a new link or a decision to prune, handed to org/content-refresh-audit.
5. Return the linking map with what changed and what remains unaddressed and why.

## Checks
- Every content page links to a real money page.
- No orphan left without a stated reason.
- Links checked live at build time, not assumed valid.

## Output
{links_added[], orphans_remaining[]}

## Example
Guide "Foldable stroller buying guide" gets 3 new links to product pages it mentions; an orphaned old blog post is flagged for pruning instead of a forced link.
