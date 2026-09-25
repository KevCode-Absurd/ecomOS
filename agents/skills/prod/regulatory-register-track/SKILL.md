---
name: prod/regulatory-register-track
owner: PROD
version: 1
invoke_when: the monthly compliance audit is due, a formula/price change occurred, or the quarterly/annual EPR filing is due
inputs: the SKU list with category, current FDA facility registration and state licence status (india: Legal
  Metrology and FSSAI licence status), state EPR packaging registration status (india: EPR plastic-packaging
  registration status), relabelling requirements
outputs: a compliance register, relabelling flags, and EPR filing status with any shortfall flagged
---
# Track FDA, net-quantity, state licence and EPR compliance

## Purpose
FDA facility registration, Fair Packaging and Labeling Act net-quantity declarations, state licensing (cosmetics,
food, supplements) and state EPR packaging filing are each recurring, concrete obligations that a brand either
tracks deliberately or handles ad hoc under deadline pressure. This skill keeps one register instead of several
scattered across people's memory. India: the same register tracks Legal Metrology (Packaged Commodities)
registration, an FSSAI licence and India's EPR plastic-packaging rules instead (markets: IN, reads null for US
brands).

## Steps
1. Keep one register listing which SKUs require FDA facility registration or a state cosmetics/food/supplement
licence, based on their actual category (India: Legal Metrology state registration or an FSSAI licence; markets:
IN).
2. Track each licence's current validity window, so an expiry is known well ahead of the date, not discovered
after it lapses.
3. Flag the relabelling a SKU needs on any formula, claim or price change: net quantity, ingredients and any
Prop 65 warning (India: on any MRP or GST change, keeping the original MRP visible as the rule requires; markets:
IN).
4. Register the brand's packaging under the relevant state's EPR rules (Oregon, California, Colorado, Maine;
India: under India's EPR rules; markets: IN), and track the annual filing deadline and recycling-target
obligation.
5. Flag when a shortfall against the recycling target means the brand needs to buy EPR credits, stating the
shortfall amount specifically.

## Checks
- Every licence's validity window reflects a checked, current status, never an assumption that it is still valid.
- A relabelling flag fires on every formula/claim/price change, not only when a licence comes up for renewal.

## Output
{licence_register[], relabelling_flags[], epr_status, epr_shortfall_flag}

## Example
Licence register: 14 of 18 SKUs require a state cosmetics licence or FDA registration, all current. One state
licence expiring in 45 days, flagged to the founder. A recent formula change on 3 SKUs triggered a relabelling
flag. Oregon EPR filing on track; no shortfall this cycle. India: the same brand's Legal Metrology/FSSAI register
and EPR filing run the equivalent check (markets: IN).
