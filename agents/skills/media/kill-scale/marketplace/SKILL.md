---
    name: marketplace-kill-scale
    owner: media-buyer
    version: 1
    invoke_when: a quick-commerce or marketplace SKU's margin read is in
    inputs: PROD-C49 contribution margin report, stockout risk
    outputs: scale/hold/kill recommendation per SKU
    ---
    Purpose: scale a marketplace or quick-commerce SKU only once its real,
    transaction-value margin has proven positive for long enough to trust, and
    stop confusing a fixable volume problem with a structural one.

    Steps
    1. Read PROD-C49's per-SKU per-dark-store contribution margin.
    2. Hold any new SKU or city expansion until 3 consecutive positive-margin
       weeks.
    3. For a SKU below the margin floor, check whether more orders would clear it
       (volume) or whether price/cost is the real problem (structural).
    4. Kill or de-prioritise a structural loser rather than keep testing volume
       fixes on it.
    5. Check stockout risk before approving any scale-up.

    Checks
    - No scale-up happened before 3 consecutive positive weeks.
    - No structural loser was left running on the theory that more orders will
      fix it.

    Output: a scale/hold/kill recommendation per SKU.

    Example: a SKU has been margin-negative for 5 weeks despite rising order
    volume -> flagged structural (COGS or price), recommended for repricing or
    kill, not further ad spend.
