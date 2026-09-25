---
name: buyer-question-mapping
owner: ORG
version: 1
invoke_when: the content calendar or a keyword/page-brief cycle needs a fresh list of real buyer questions
inputs: support tickets, comments/DMs, marketplace and site reviews, Search Console queries, brand brain avatars
outputs: ranked question bank tagged by SKU, funnel stage and suggested channel
---
# Buyer and avatar question mapping

## Purpose
One shared source of real buyer language feeds both the content calendar (org/make-content) and the SEO page-brief pipeline (org/page-brief-build), so scripts and pages answer the same questions buyers actually ask, not guessed ones.

## Steps
1. Pull 90 days of support tickets, comments and DMs tagged with a product question.
2. Pull review text from Amazon, Walmart, Google and the site for the same SKUs (also Flipkart, India market option, reads null for a US-only brand). Quote the exact line and note the source and date.
3. Pull Search Console queries where connected; label People Also Ask and autocomplete pulls as web research, kept apart from private data.
4. Cluster by SKU and funnel stage: awareness objection, decision-stage spec question, post-purchase how-to.
5. Tag each cluster with a suggested channel: an objection with strong emotion or visual proof suits short video; a spec or comparison question suits a page; a trust or authority question suits the facts page.
6. Rank by how often the question appears and how close it sits to a stuck SKU.

## Checks
- Every question carries a quoted source and a date.
- No invented question.
- Each cluster names a real SKU.

## Output
{questions[{text, sku, funnel_stage, suggested_channel, sources[], count}]}

## Example
"Will the folding hinge rust after a rainy Seattle winter?" - stroller-v2, decision-stage, suggested_channel: page + video, 14 mentions across reviews and DMs since June.
