---
name: mobile-first-qa
owner: site-specialist
version: 1
invoke_when: checking a page for real friction, mobile usability, or accessibility before or after launch
inputs: brand brain device split (from GA4), theme code, key templates (home, PDP, collection, cart, checkout)
outputs: friction fix list, mobile QA report, accessibility audit report
---
# Friction removal, mobile-first QA and accessibility audit

## Purpose
Check that a page works for a real person: no dead controls, no hidden content on mobile, and no barrier for someone using a keyboard or a screen reader.

## Steps
1. Strip navigation to logo, cart and one CTA on single-offer campaign pages; open a cart drawer on add-to-cart, never a reload.
2. Fire pop-ups only on real intent signals, never in the first 3-5 seconds; fix or remove dead controls and false affordances.
3. Build and review every page mobile-first, on the brand's own real device split, checking every screen width in responsive mode.
4. Pin the PDP CTA on mobile without covering the variant selector; never hide reviews or content behind a mobile-only carousel; cap mobile forms at 4 fields.
5. Run an automated WCAG scan on home, PDP, collection, cart and checkout templates.
6. Manually test forms, navigation and dynamic states with a keyboard and a screen reader, separating real failures from automated false positives.
7. Scope every remediation to the theme codebase so fixes survive future updates.

## Checks
- Every friction fix confirmed live, not assumed from a screenshot.
- Mobile QA run on the brand's real device split, not a generic phone size.
- Manual accessibility pass included, not the automated scan alone.

## Output
A friction fix list, a mobile QA report with screenshots per width, and an accessibility audit report.

## Example
"Cookie banner covers the Add to Cart button on iPhone 13 at 390px width. Fixed by repositioning the banner; confirmed with a real screenshot at that exact width."
