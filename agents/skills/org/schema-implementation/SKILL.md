---
name: schema-implementation
owner: ORG
version: 1
invoke_when: on demand, for any money page missing or carrying stale structured data
inputs: page content, product/review/FAQ/price data, deployment method
outputs: schema spec, pre- and post-deployment validation results, a developer brief
---
# Structured data implementation and validation

## Purpose
Add and validate Product, Review, FAQ, Breadcrumb and Offer schema on every money page, using real page data only, deploying through Google Tag Manager when there is no direct theme access.

## Steps
1. Pick the schema types the page needs.
2. Populate every field from the live page and product record; no placeholder values.
3. Validate the markup with a structured-data testing tool before shipping.
4. When theme access is unavailable, package the deployment as a GTM tag and trigger spec instead.
5. Write the developer brief naming the change, location, reason, validation check and rollback.
6. After a human applies it, re-validate on the live page and log the result.

## Checks
- No placeholder field values.
- Validated before and after deployment.
- GTM used whenever theme access is unavailable.

## Output
{schema_spec[], validation_result_pre, deployment_method, developer_brief, validation_result_post}

## Example
Product schema for stroller-v2 populated with the live price ($119.99) and current stock status; validated, then re-validated after the GTM tag went live, both passing.
