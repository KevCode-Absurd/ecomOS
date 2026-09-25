---
name: make-creatives/static
owner: crea-paid-creative-copy
version: 1
invoke_when: format is static, a single image ad for feed, story or search
inputs: concept brief, reference image, real product photo, brand kit, headline/primary-text set
outputs: static design brief plus draft image variant(s)
---
Purpose: turn an approved concept into a design-ready static ad spec and a first
draft image, using the real product photo wherever accuracy matters and a
competitor reference for layout and mood only.

Steps
1. Pick clarity-first (state the benefit plainly) or curiosity-first (a visual
   hook that earns the read) from the angle's awareness stage: cold traffic
   usually needs curiosity, warm traffic usually needs clarity.
2. Pair the real product image with the headline so the pairing states one
   benefit at first glance, not two competing ideas.
3. Set primary-text weight for the placement: short and punchy for feed, longer
   proof-led text where the placement supports an expand.
4. Generate the draft through the creative studio's /api/variants call, passing
   the real product photo and the tagged reference image, with product-accuracy
   mode on so the product itself is never redrawn.
5. Note any localisation flag (script, currency, trust badge) or catalogue/DPA
   flag the design will need at scale.
6. Check the draft against the reference: same mood or layout only, nothing of
   the competitor's own text, logo, product or face reused.

Checks: real photo present where fit or scale matters; no competitor asset
copied; reference credit recorded.

Output: static design brief (eye path, pairing, text weight, CTA) plus the
draft image file(s) from the studio.

Example: a cold-traffic protein-bar ad pairs a macro shot of the bar breaking
open with a curiosity headline ("the bar that doesn't taste like a bar"),
studio-generated with the real product photo, credited to one tagged
competitor reference for its close-up crop style only.
