---
name: prod/regulatory-register-track
owner: PROD
version: 1
invoke_when: the monthly compliance audit is due, an MRP/GST change occurred, or the quarterly/annual EPR filing is
  due
inputs: the SKU list with category, current Legal Metrology and FSSAI licence status, EPR plastic-packaging
  registration status, relabelling requirements
outputs: a compliance register, relabelling flags, and EPR filing status with any shortfall flagged
---
# Track Legal Metrology, FSSAI and EPR compliance

## Purpose
Legal Metrology registration, FSSAI licensing and EPR plastic-packaging filing are each recurring, concrete
obligations that a brand either tracks deliberately or handles ad hoc under deadline pressure. This skill keeps
one register instead of three separate ones scattered across people's memory.

## Steps
1. Keep one register listing which SKUs require Legal Metrology (Packaged Commodities) registration or an FSSAI
   licence, based on their actual category.
2. Track each licence's current validity window, so an expiry is known well ahead of the date, not discovered
   after it lapses.
3. Flag the relabelling a SKU needs on any MRP or GST change: this is a common, easy-to-miss trigger distinct from
   a licence renewal.
4. Register the brand's plastic packaging under India's EPR rules, and track the annual filing deadline and
   recycling-target obligation.
5. Flag when a shortfall against the recycling target means the brand needs to buy EPR credits, stating the
   shortfall amount specifically.

## Checks
- Every licence's validity window reflects a checked, current status, never an assumption that it is still valid.
- A relabelling flag fires on every MRP or GST change, not only when a licence comes up for renewal.

## Output
{licence_register[], relabelling_flags[], epr_status, epr_shortfall_flag}

## Example
Licence register: 14 of 18 SKUs require Legal Metrology registration, all current. One FSSAI licence expiring in
45 days, flagged to the founder. A recent MRP change on 3 SKUs triggered a relabelling flag. EPR filing on track;
no shortfall this cycle.
