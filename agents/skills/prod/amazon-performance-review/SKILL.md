---
name: prod/amazon-performance-review
owner: PROD
version: 1
invoke_when: an Amazon sales change needs explaining, or the channel's next growth move needs planning
inputs: Business Reports, attribution data, a seasonality baseline, the current SKU portfolio, candidate growth
  levers
outputs: a sales diagnosis, a compliant promotion response, growth-lever test results, and a channel memo
---
# Diagnose Amazon performance and plan growth

## Purpose
A sales drop on Amazon has at least two very different causes: fewer people seeing the listing, or fewer people
buying once they see it: and confusing the two leads to the wrong fix. This skill forces that split before any
other conclusion, and keeps growth responses inside Amazon's own compliant tools.

## Steps
1. Split any sales change into a traffic component and a conversion component, using Business Reports data, before
   drawing any conclusion about the product.
2. Check attribution (is the traffic even coming from where it looks like) and seasonality (is this the normal
   pattern for this time of year) before calling a product a failure based on a raw sales number.
3. Respond only with Amazon's own compliant promotion tools: Lightning Deals, Coupons, Amazon-native ad formats: 
   never an outside workaround that risks a policy violation.
4. Decide whether to add a second SKU based on the diagnosis, not on a hunch, and test smaller situational growth
   levers (FBM to FBA conversion, Small and Light enrolment, a design-vendor bake-off, Amazon Live) each with a
   defined read set before the test starts.
5. Write the one-page memo behind any decision to add or expand the Amazon channel.

## Checks
- The traffic/conversion split happens before any conclusion about the product itself.
- Every growth-lever test has its read defined before the test starts, never decided after seeing results.

## Output
{diagnosis{traffic_change, conversion_change}, promotion_response, growth_tests[], channel_memo}

## Example
Sales down 22% week over week. Diagnosis: traffic down 3% (normal seasonality), conversion down 19%: points to a
listing or price issue, not a demand problem. Response: a compliant Coupon test with a defined 2-week read, not an
off-platform discount code.
