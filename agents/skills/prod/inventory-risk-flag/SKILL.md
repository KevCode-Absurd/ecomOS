---
name: prod/inventory-risk-flag
owner: PROD
version: 1
invoke_when: a monthly structural-risk review is due, or a weekly dead-stock sweep is due
inputs: the supplier and country ledger, current FX/freight/duty rates, stock age and velocity by channel, the
  brand's dead-stock and long-term-storage thresholds
outputs: concentration risk flag, a refreshed landed cost, and a dead-stock alert with clearance options
---
# Flag concentration risk and dead stock, refresh landed cost

## Purpose
Two structural risks share one owner because both are about catching a slow-moving problem before it becomes an
expensive one: too much dependence on one supplier or country, and stock quietly ageing past the point it can be
sold at full price.

## Steps
1. Compute the share of spend or volume concentrated in any single supplier or country.
2. For any concentration above the brand's own threshold, confirm a real, vetted backup supplier exists in a
   second country: not just a name on a list, but a verified alternate from the sourcing skill.
3. Recompute landed cost the moment price, freight, FX or duty actually changes, rather than waiting for a fixed
   monthly calendar date, since a duty change can move margin materially overnight.
4. Watch stock age against velocity across every channel the SKU sells on, and flag a SKU against the long-term
   storage or dead-stock threshold before it becomes dead weight, not after.
5. Draft markdown, bundle, or discontinue options for a flagged SKU, each with its cash impact computed, so the
   founder is deciding between real numbers, not vague options.

## Checks
- Every backup supplier named is real and vetted, never an assumption.
- Landed cost is recomputed on an actual triggering event, not just a fixed calendar.
- Every clearance option's cash impact is computed, not estimated.

## Output
{concentration{}, backup_confirmed, refreshed_landed_cost, dead_stock_alerts[], clearance_options[]}

## Example
Concentration: 68% of SKU-1042's spend is with one supplier in one country: above the 50% threshold; a verified
backup in a second country exists. Landed cost refreshed after a 4% duty change, margin down 1.1pt. Dead-stock
alert: SKU-0810 at 210 days of stock against a 90-day threshold; clearance options drafted at 3 markdown depths
with cash impact for each.
