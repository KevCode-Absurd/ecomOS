---
name: asset-weight
owner: site-specialist
version: 1
invoke_when: images, fonts, or unsplit code are adding measurable page weight
inputs: connector: shopify admin | woocommerce media library, brand brain brand fonts, results/*.json history
outputs: image fix list, font fix list, code-splitting plan, developer brief
---
# Cut image, font and code weight

## Purpose
Cut the 3 biggest sources of unnecessary page weight, in the right order, each proven with a before/after byte count.

## Steps
1. Check images directly; never trust automatic platform compression alone.
2. Resize to about 2,000px, use JPEG for photos and PNG only for transparency, confirm WebP/AVIF delivery, and set lazy-load below the fold, eager above it.
3. Add width/height or aspect-ratio to every image to prevent shift, and sweep the media library for stray heavy files.
4. Cap font variations to about 3, self-host as WOFF2, add font-display: swap, and match the fallback font's metrics.
5. Subset fonts to the characters used on a framework storefront.
6. Only after images and fonts are fixed, minify and split CSS/JS by page type.
7. Delay non-critical CSS (modals, drawers, filters) and make inlined critical CSS complete per template.

## Checks
- Before/after byte counts recorded for every fix.
- No visible text jump on font swap, checked with a filmstrip.
- Code splitting done last, never first.

## Output
An image fix list, a font fix list, and a code-splitting plan, each with a before/after number.

## Example
"Hero image: 1.8MB JPEG at 4000px, resized to 2000px and re-compressed to 210KB, WebP delivery confirmed. 1.6MB saved on the PDP's first paint."
