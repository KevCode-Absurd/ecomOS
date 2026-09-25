---
name: theme-pr-diff
owner: site-specialist
version: 1
invoke_when: any theme or site-repo change is about to ship, regardless of size
inputs: the change description, the platform (Shopify theme, WooCommerce, custom repo)
outputs: diff or PR link, rollback command, before/after screenshots
---
# Theme change as a reviewable diff

## Purpose
Make every theme or repo change reviewable and reversible, the single mechanic that every other Site workflow relies on when it touches the live storefront.

## Steps
1. Duplicate the theme (Shopify/WooCommerce) or create a branch (custom repo) before making any change.
2. Make the change only on the duplicate or branch, never the live theme or main.
3. Screenshot the affected page before and after the change.
4. Write the exact rollback command or step, and confirm it works.
5. Open a pull request for a custom repo; require a second reviewer or the founder gate on Shopify/WooCommerce too.
6. Verify the change on the live duplicate/staging URL, not only the editor preview.

## Checks
- No edit ever touches the live theme or main branch directly.
- Rollback command has been tested, not assumed to work.
- Before/after screenshots exist for every visual change.

## Output
A diff or PR link, a tested rollback command, and a before/after screenshot pair.

## Example
"PDP delivery-ETA badge added on branch `pdp-eta-badge`, PR #142, rollback: `git revert 4fa21c`, tested clean revert in 15 seconds."
