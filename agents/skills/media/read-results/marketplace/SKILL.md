---
    name: marketplace-read
    owner: media-buyer
    version: 1
    invoke_when: a marketplace or rapid-delivery/grocery spend read is due (India only: quick-commerce)
    inputs: seller dashboard export, SKU landed cost, ad console export
    outputs: contribution margin report, ACOS/TACOS read
    ---
    Purpose: read marketplace and rapid-delivery/grocery ad results on the real
    number, since platform dashboards inflate ROAS 30-50% by pricing at list price
    (MRP, India) instead of transaction value.

    Steps
    1. Recompute ROAS on actual transaction value, net of platform commission
       (15-25%) and applicable US sales tax on the commission (GST, India only).
    2. Add inwarding fees, storage cost and a 2-5% list-price write-off budget for
       damage/expiry.
    3. Calculate the weekly per-fulfillment-center order volume needed to clear the
       55-60% gross margin floor (per-dark-store, India only).
    4. Flag whether a shortfall is a volume problem (more orders fixes it) or a
       structural one (needs repricing or a COGS cut).
    5. Read Amazon/Walmart/Target ACOS or TACOS against the SKU's own margin
       (Flipkart, India only).

    Checks
    - No ROAS number in the report is based on list price (MRP, India only).
    - Every margin flag names whether it is volume or structural.

    Output: contribution margin report, ACOS/TACOS read.

    Example: platform dashboard shows 4.2x ROAS; recomputed on transaction value
    net of commission and fees it is 2.6x -> the true number the SKU is judged on.
