---
name: research-customers/onsite-behavior
owner: BRAND
version: 1
invoke_when: the source is the brand's own on-site search terms or browse-without-buy sessions
inputs: GA4 / site search log
outputs: unmet-search-term list, job clue notes
---
# Mine on-site search and behavior

## Purpose
What a shopper types into the brand's own search bar, and what they browse but never add to cart, is a direct clue to the job they came to do, unfiltered by what the brand chose to say on the page.

## Steps
1. Pull on-site search query volume for the period, ranked by frequency.
2. Pull sessions that visited a category or product page multiple times without adding to cart, and note which page.
3. Cluster search terms into groups by apparent intent (a size question, a use-case question, a comparison question).
4. Flag any search term with meaningful volume and no matching product or content on the site; this is a direct unmet-demand signal.
5. Cross-reference high-volume browse-without-buy pages against the objection map, if one exists, to see if a known objection explains the drop-off.

## Checks
- Terms are deduplicated and ranked by volume before being called a pattern; one search is not a trend.
- A browse-without-buy pattern is reported with the specific page, not "the site" in general.

## Output
`{unmet_search_term_list: [...], job_clue_notes: [...]}`

## Example
Search term "cotton saree fall stitching" (41 searches, 30 days) with no matching product or FAQ content: flagged as an unmet demand signal for Product and Content.
