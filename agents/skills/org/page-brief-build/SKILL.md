---
name: page-brief-build
owner: ORG
version: 1
invoke_when: monthly, and before any page is written
inputs: buyer-question map, Search Console data, budgeted web pass, existing site architecture
outputs: keyword-and-question map, structured page briefs by target and page type
---
# Keyword research and page-brief build

## Purpose
Build the target list the whole content program runs from, then turn each target into a structured brief before anyone writes a word, so no page gets built on a guess at intent.

## Steps
1. Merge the buyer-question map with a budgeted web pass for search volume and intent.
2. Classify each target's intent and the page type it fits: collection, product, guide, or blog.
3. Build the ranked keyword-and-question map.
4. Write each priority target's page brief: outline, buyer questions to answer, internal links to add, schema to add.
5. Check whether a ranking page already exists for the target; if so, hand it to org/content-refresh-audit instead of briefing a duplicate.
6. Hand the finished brief to the matching org/seo-page child.

## Checks
- No brief for a page type the store does not actually sell or serve.
- Every target checked against existing content first.
- Buyer questions come from real sources.

## Output
{keyword_question_map[], page_briefs[]}

## Example
Target "foldable stroller for small apartments India" classified as informational/guide intent, briefed as a new buying guide rather than added to the existing product page, which already covers transactional intent.
