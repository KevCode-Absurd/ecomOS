---
name: prod/build-tech-pack
owner: PROD
version: 1
invoke_when: a new SKU or a spec change needs a versioned, exact specification a factory can build to
inputs: approved candidate or SKU, reference sample if one exists, target unit cost, packaging requirements
outputs: versioned tech pack with BOM and a costed, tested packaging spec
---
# Build tech pack, BOM and packaging spec

## Purpose
Vague specs cause factory disputes and sample failures. This skill writes the exact, versioned document a factory
builds to, so any downstream dispute has a written reference to check against.

## Steps
1. Write every physical dimension with a stated tolerance band. A number with no tolerance is not a spec.
2. Build the bill of materials at the component level: each component gets its own spec line and target cost, not
   one blended unit-cost figure.
3. Price packaging as its own cost line, separate from the product's unit cost, so a packaging change never hides
   inside a "unit cost went up" surprise later.
4. Assign a version number to the whole pack and log it against the SKU record. Every future sample, RFQ and PO
   references this version number, never a verbal description.
5. Book the drop-test, tamper-evidence and transit-durability test the packaging design needs, sized to the actual
   transit mode (air, sea, last-mile courier). Track the result against a stated pass criterion.
6. If the test fails, revise the spec, bump the version number, and re-book the test. Never edit the failed version
   in place.

## Checks
- Every measurement carries a tolerance band.
- Packaging appears as its own cost line in every downstream cost model.
- A durability test is booked and resolved before the SKU proceeds to production, not after a shipment already
  failed in transit.

## Output
{tech_pack_version, dimensions[{name, value, tolerance}], bom[], packaging{spec, cost, test_result}}

## Example
Tech pack v3 (v2 failed the drop test at 90cm). Box wall thickness raised from 3mm to 4.5mm corrugate, packaging cost
line up ₹4.20/unit. Re-booked drop test passed at 120cm. Version 3 is the one cited in the next RFQ.
