---
name: seo-page/product
owner: ORG
version: 1
invoke_when: the page brief's page_type is product
inputs: page brief, product record, review data, image assets, subscription/variant status
outputs: title, meta description, full content stack, image alt text, template used, internal links
---
# Product page SEO

## Purpose
Write and structure a product page with a real title and a complete, fact-based content stack in the order a buyer actually asks questions, using the correct dedicated template for subscription or variant products instead of forcing the single-product default.

## Steps
1. Write a real, readable title and a meta description covering the target term.
2. Build the content stack: specs, materials, care, shipping, returns, warranty, ordered by real buyer question priority.
3. Write image alt text describing the actual product in each image.
4. Apply the subscription or variant template when the product needs it, not the single-product default.
5. Add review data and a Q&A section from real buyer questions.
6. Add internal links to the matching collection and any relevant guide.

## Checks
- Title is readable, not a SKU code.
- Every claim is site-backed.
- Subscription/variant products use their own template.

## Output
{title, meta_description, content_stack{}, image_alt_text[], template_used, internal_links[]}

## Example
A subscription refill SKU uses the subscription template, surfacing cadence and cancellation terms above the fold, instead of the plain one-time-purchase layout.
