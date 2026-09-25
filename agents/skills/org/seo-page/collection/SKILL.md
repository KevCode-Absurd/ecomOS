---
name: seo-page/collection
owner: ORG
version: 1
invoke_when: the page brief's page_type is collection
inputs: page brief, product grid rules, review data, buyer-question map
outputs: title, meta description, on-page copy, grid rules, FAQ, internal links
---
# Collection page SEO

## Purpose
Write and structure a collection page so it both ranks and genuinely helps a buyer choose between the products it lists, not just a keyword-stuffed header above a grid.

## Steps
1. Write the title and meta description covering the target term and the real buying decision it represents.
2. Write on-page copy as a buying-decision aid: how to choose within this set, not filler.
3. Set grid rules: default sort, filters, and an honest out-of-stock display that never hides an item without showing why or offering a substitute.
4. Write an FAQ from real buyer questions tagged to this collection.
5. Confirm collection-level review data displays where available.
6. Add the internal links the brief specifies.

## Checks
- Copy helps a buyer choose, not just describes.
- Out-of-stock items are never silently hidden.
- FAQ traces to real sources.

## Output
{title, meta_description, on_page_copy, grid_rules, faq[], internal_links[]}

## Example
Collection "foldable strollers" FAQ includes "does folded size matter for a hatchback boot?", sourced from 9 real customer questions, not invented.
