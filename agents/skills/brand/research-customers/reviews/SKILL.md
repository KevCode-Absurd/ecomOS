---
name: research-customers/reviews
owner: BRAND
version: 1
invoke_when: the source is the brand's own product reviews (site or marketplace)
inputs: reviews export by SKU with star rating and date
outputs: tagged quote set by star band, objection frequency list, candidate identity markers
---
# Mine reviews

## Purpose
Turn raw star-rated reviews into a tagged quote set and objection list an avatar record or copy brief can use directly, without re-reading the raw file.

## Steps
1. Export all reviews per SKU with star rating, date and marketplace (site, Amazon.in, Myntra, etc. as applicable).
2. Group by star band. Read 1 and 2 star reviews for the real objection, which is often not the same as the stated complaint (a "poor quality" review may really be a fit or expectation-setting problem).
3. Read 4 and 5 star reviews for the job the product actually did in the customer's life, not just that they liked it.
4. Scan every band for identity markers: phrases like "I am a", "as a", "for my [relationship]" that reveal who is talking.
5. Prioritize long, narrative reviews over short generic ones ("nice product") for quote quality.
6. Discount a single contradictory review; only act on a pattern that repeats across multiple reviews.
7. Capture every usable quote verbatim, with SKU, star band, source platform and date. Strip the reviewer's full name.
8. Flag any use case mentioned that no competitor's marketing targets, as a candidate for BRAND-W08 (untapped avatar).

## Checks
- Every quote has SKU, star band, source and date.
- No full reviewer name is kept.
- A theme is only reported as real once it appears in 2 or more reviews.

## Output
`{quotes_by_star_band: [...], objection_frequency_list: [...], candidate_identity_markers: [...]}`

## Example
1-star band, 6 occurrences: "the strap felt flimsy after 2 weeks of daily wear" tagged as a durability objection, source: Amazon.in review, dated 14 Aug 2026.
