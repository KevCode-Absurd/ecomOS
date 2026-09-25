---
name: seo-page (dispatcher)
owner: ORG
version: 1
invoke_when: a page brief is ready to become a structured, written page
inputs: page brief, brand facts and claims tiers, site architecture
outputs: the matched child skill's page spec plus a claims-check verdict
---
# SEO page build (dispatcher)

## Purpose
Route a page brief to the procedure built for its page type, since a collection page, a product page, a buying guide and a blog post each carry different structural rules and a different job to do for the buyer.

## Steps
1. Read the brief's page_type field: collection, product, guide, or blog.
2. Dispatch to the matching child skill.
3. Run shared/claim-check on the child's output before returning it.
4. If the brief names a page type the store's architecture does not support, stop and hand a proposal to a person instead of forcing a fit.

## Checks
- Exactly one child invoked per brief.
- No page type used outside the 4 supported ones.

## Output
Whatever the matched child returns, wrapped with {claims_check_verdict}.

## Example
A brief with page_type "guide" and a comparison subtype dispatches to org/seo-page/guide, which handles both buying guides and comparison/alternatives content.
