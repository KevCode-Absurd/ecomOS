---
name: packaging-label-brief
owner: BRAND
version: 1
invoke_when: a new SKU, new channel, or packaging change needs artwork briefed with mandatory declarations placed
inputs: product spec (PROD-C13), target channel(s), brand guidelines
outputs: layout draft, declaration-placed layout, completeness checklist result
---
# Packaging and mandatory label brief

## Purpose
Packaging artwork has two jobs at once: carry the brand's visual language, and legally declare what the law requires for this product category and channel in India. This skill briefs both together so nothing goes to print missing a required field.

## Steps
1. Pull the dieline, net quantity, and any per-channel packaging constraint from the Product and Supply specialist's spec; never re-derive these from guesswork.
2. Apply the brand guidelines' palette, typography and logo rules (clear space, minimum size) to the dieline layout.
3. Place every legally required declaration for the target market: MRP, Legal Metrology details (net quantity; manufacturer, packer or importer name and address; month and year of manufacture; consumer care contact), BIS or hallmark mark where the product category requires it, and the EPR mark where applicable.
4. Check any additional channel-specific rule (a marketplace's own barcode or return-label placement requirement) beyond the general legal requirements, for each target channel.
5. Run the full completeness checklist against the layout; a missing mandatory field blocks sign-off, it never goes to print with a "fix later" note.

## Checks
- Every mandatory declaration for this product category is present and legible at its required minimum size.
- Channel-specific rules are checked individually, never assumed identical to DTC packaging.
- A missing mandatory field blocks sign-off outright.

## Output
`{layout_draft, declaration_placed_layout, completeness_checklist_result}`

## Example
New SKU going to a marketplace channel for the first time: completeness check catches that the Legal Metrology month-of-manufacture field, present on the DTC box, was omitted from the marketplace-specific dieline draft: blocked until added.
