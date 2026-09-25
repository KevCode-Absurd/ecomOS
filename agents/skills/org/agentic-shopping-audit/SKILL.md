---
name: agentic-shopping-audit
owner: ORG
version: 1
invoke_when: weekly
inputs: Agentic Storefront query access, claims tiers, live product feed, frozen agentic prompt set
outputs: audit log of stated facts vs live values, mismatches routed to the right fix path
---
# Agentic storefront claims audit

## Purpose
As merchants now sell through Agentic Storefronts inside ChatGPT, Copilot, Google AI Mode and Gemini (managed from the Shopify Admin Knowledge Base app), check what these shopping agents actually tell a buyer against the claims tiers and the live feed, weekly, since a wrong price or stock status here costs a sale or a refund directly.

## Steps
1. Query each agentic shopping surface with the frozen prompt set for this brand's products.
2. Record exactly what each agent states: price, stock, shipping, product claims.
3. Check every stated fact against the claims tiers and the live feed, not brand intent.
4. Flag mismatches: wrong price, wrong stock, an unbacked or forbidden claim stated as fact.
5. Route price/stock mismatches to the feed fix path; route claim mismatches to the facts-page and correction workflow.
6. Log the week's results for a trend view over time.

## Checks
- Checked against the live feed, not a cached value.
- Mismatches routed correctly.
- Logged weekly for trend, not a one-off check.

## Output
{audit_log[], routed_fixes[]}

## Example
ChatGPT's shopping surface states stroller-v2 is "in stock, $99.99" when the live feed shows out of stock at $119.99: both a stock and a price mismatch, routed to the feed source-of-truth fix.
