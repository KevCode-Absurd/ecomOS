---
name: seo-page/guide
owner: ORG
version: 1
invoke_when: the page brief's page_type is guide, covering both buying guides and comparison/alternatives pages
inputs: page brief, proprietary moat data, public competitor facts, season/timing target
outputs: subtype, title, outline, body, sourced competitor facts where relevant, linked money page, FAQ
---
# Buying guide and comparison page SEO

## Purpose
Build guide-format content ahead of the season it targets, always in support of one real money page, using either the brand's own proprietary facts (buying guide) or public, sourced facts about a named competitor (comparison) since these formats are what search and AI answers cite most for considered purchases.

## Steps
1. Confirm the subtype: buying_guide or comparison.
2. Schedule the build ahead of its target season against the content calendar.
3. For a buying guide, structure by real decision criteria using the brand's own tier-checked data.
4. For a comparison, state only public, sourced, dated facts about the named competitor; never invent or use private information about them.
5. Link the page to the one real money page it supports; skip building if none exists.
6. Add an FAQ from real buyer questions and internal links.

## Checks
- Every competitor fact is public, sourced and dated.
- The page links to a real money page.
- Built ahead of season, not after it has passed.

## Output
{subtype, title, outline, body_sections[], competitor_facts_sourced[], linked_money_page, faq[]}

## Example
Comparison page "Brand X vs [Competitor]" states the competitor's publicly listed weight and price with a source URL and date, links to the stroller-v2 product page as its money page.
