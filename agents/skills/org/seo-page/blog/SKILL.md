---
name: seo-page/blog
owner: ORG
version: 1
invoke_when: the page brief's page_type is blog, as one node in a content cluster
inputs: page brief, the cluster's pillar page, buyer questions for this node
outputs: title, body, pillar and sibling links, a quotable FAQ/summary block, publish date
---
# Blog and content-cluster SEO

## Purpose
Write one cluster node that answers a single buyer question in real depth and links back to its pillar, one cluster at a time, ahead of the season it targets, rather than a standalone blog post with nowhere to link.

## Steps
1. Confirm the pillar page this post belongs to; do not build a standalone post with no cluster.
2. Answer one real buyer question in depth.
3. Link up to the pillar and sideways to sibling posts in the same cluster.
4. Add a short, quotable FAQ or summary block that both search and AI answers can lift.
5. Record the publish date and enter the post into the content-refresh tracking list, since it now has a shelf life.

## Checks
- Links to its pillar exist.
- The buyer question is answered in depth, not skimmed.
- Enters refresh tracking on publish.

## Output
{title, body, pillar_link, sibling_links[], faq_block, publish_date}

## Example
Post "How to measure your hallway before buying a foldable stroller" links up to the pillar "Complete guide to foldable strollers in the US" and sideways to "Stroller weight limits explained".
