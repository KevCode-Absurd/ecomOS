---
    name: marketplace-read
    owner: media-buyer
    version: 1
    invoke_when: a marketplace or quick-commerce spend read is due
    inputs: seller dashboard export, SKU landed cost, ad console export
    outputs: contribution margin report, ACOS/TACOS read
    ---
    Purpose: read marketplace and quick-commerce ad results on the real number,
    since platform dashboards inflate ROAS 30-50% by pricing at MRP instead of
    transaction value.

    Steps
    1. Recompute ROAS on actual transaction value, net of platform commission
       (15-25%) and GST on the commission.
    2. Add inwarding fees, storage cost and a 2-5% MRP write-off budget for
       damage/expiry.
    3. Calculate the weekly per-dark-store order volume needed to clear the
       55-60% gross margin floor.
    4. Flag whether a shortfall is a volume problem (more orders fixes it) or a
       structural one (needs repricing or a COGS cut).
    5. Read Amazon/Flipkart ACOS or TACOS against the SKU's own margin.

    Checks
    - No ROAS number in the report is based on MRP.
    - Every margin flag names whether it is volume or structural.

    Output: contribution margin report, ACOS/TACOS read.

    Example: platform dashboard shows 4.2x ROAS; recomputed on transaction value
    net of commission and fees it is 2.6x -> the true number the SKU is judged on.
