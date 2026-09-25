---
name: theme-engineering
owner: site-specialist
version: 1
invoke_when: selecting a new theme, or checking a new section against the brand's design tokens
inputs: brand brain required features, current live theme CSS, candidate themes or mockups
outputs: theme shortlist with scores; design token doc; drift flags
---
# Theme engineering practice

## Purpose
Pick a theme on real fit, not a demo, and keep every later change consistent with one documented set of design tokens instead of drifting section by section.

## Steps
1. Write the required feature and section list before opening any theme.
2. Vet each candidate on a real product page and a real mobile width, not the homepage demo.
3. Score candidates against the list, note the runner-up and why it lost.
4. Once a theme is live, document its color, spacing, typography and component tokens.
5. Check every new homepage or PDP section, native or page-builder, against the token set.
6. Flag any drift (wrong radius, font size, spacing) before the section ships.

## Checks
- Vetting happened on PDP and mobile, never the homepage demo alone.
- Every new section was checked against the token doc, not shipped by eye.

## Output
A scored theme shortlist for a selection task, or a token doc plus drift flags for an ongoing design-system check.

## Example
"New FAQ accordion built in Replo used a 6px border radius; brand token is 4px. Flagged and corrected before publish."
