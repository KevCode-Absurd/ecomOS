---
name: prod/amazon-opportunity-screen
owner: PROD
version: 1
invoke_when: an Amazon-specific candidate needs its own elimination screen and review/keyword mining
inputs: the candidate, Amazon browse/search data (public), competing listing reviews, reverse-ASIN keyword tool
  access
outputs: an Amazon-specific screen result, a product-gap brief from reviews, and a mined keyword list
---
# Screen an Amazon opportunity and mine reviews/keywords

## Purpose
A candidate that cleared the general product screen (PROD-C01-C05) still needs Amazon-specific diligence: Amazon's
own price dynamics, keyword search behaviour, and review patterns work differently from the open web or DTC.

## Steps
1. Apply Amazon-specific elimination screens: a price floor below which margin cannot work after fees, the price
   spread across page-1 listings (a huge spread signals a confusing or commoditized category), keyword search
   variability, and how dominant one or two brands already are in the category.
2. Run a real fad filter against the candidate's Amazon search trend data: a single-month spike is not the same
   as sustained demand.
3. Read 1 to 3 star reviews on the closest competing listings for complaints this candidate's design could fix. Use
   the complaint as a design input, never copy the review's wording into any copy.
4. Confirm mid-rated, high-volume sellers exist in the category as a demand-and-gap signal: real search volume
   with real dissatisfaction is the strongest opportunity signal available.
5. Mine keywords from reverse-ASIN tools for the category, ranked by search volume where the tool provides it.

## Checks
- Every elimination screen states its specific reason.
- The fad filter is based on more than one data point over time.
- No review text is copied verbatim; only the underlying gap it points to is used.

## Output
{screen_result, fad_verdict, complaint_list[], keyword_list[]}

## Example
Screen: pass (price floor clears with FBA fees included, page-1 spread moderate). Fad filter: pass, 3-year steady
growth not a single spike. Complaints mined: "lid doesn't seal after 2 months" appears in 40+ reviews across 3
competitors: a fixable design input. Keywords ranked by volume for the listing build.
