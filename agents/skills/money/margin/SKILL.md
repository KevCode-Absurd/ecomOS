---
name: money/margin
owner: MONEY
version: 1
invoke_when: a margin or SKU-classification number is needed for a basket, SKU or channel
inputs: order export, landed cost per SKU, delivery and marketing cost
outputs: CM1/CM2/CM3 by scope, SKU classification
---
# Compute contribution margin by scope

## Purpose
Nobody should guess what a margin number includes. This skill always states which layer of cost it has subtracted.

## Steps
1. Compute CM1: revenue minus COGS.
2. Compute CM2: CM1 minus delivery and fulfillment cost.
3. Compute CM3: CM2 minus the marketing cost attributed to that scope.
4. Attach the scope label (SKU, basket or channel) to every figure.
5. Rank SKUs and classify each as champion, hidden gem, growth driver or underperformer, using contribution and cash tied up in inventory.

## Checks
- Every number states CM1, CM2 or CM3 explicitly.
- Classification uses both contribution and cash tied up, never contribution alone.

## Output
CM1, CM2, CM3 for the requested scope, plus a SKU classification tag where the scope is SKU.

## Example
A best-selling SKU shows strong CM1 but is classified underperformer once CM3 accounts for the paid spend driving most of its sales.
