---
name: visual-search
owner: site-specialist
version: 1
invoke_when: on-site search is diagnosed as a bottleneck and the catalogue is visually distinct enough to benefit from photo-based discovery
inputs: product photo catalogue, shopper-uploaded photo
outputs: visual search widget, similarity index
---
# On-site visual product search

## Purpose
Let a shopper find a real product from a photo they saw elsewhere or already own, matched only against the brand's own real product photos, never a competitor's or a generated redraw.

## Steps
1. Embed every live product's real photos once, using an image embedding model, and keep the index current as the catalogue changes.
2. Accept a shopper-uploaded photo, embed it the same way, and return the nearest real SKUs by visual similarity.
3. Cap the feature to product discovery only; never claim a visual match is exact.
4. Fall back cleanly to text search when no close visual match exists.
5. Keep uploaded shopper photos private and short-lived, never stored as training data or compared against a competitor's assets.

## Checks
- No visual match is ever presented as exact.
- No shopper-uploaded photo persists past the session.
- The similarity index refreshes as the catalogue changes, never stale.

## Output
A working visual search widget and its similarity index.

## Example
"Shopper uploads a photo of a jacket seen on Instagram; widget returns the brand's own 3 closest visual matches by silhouette and color, labelled 'similar styles', never 'exact match'."
