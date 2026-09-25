---
    name: stock-check
    owner: media-buyer
    version: 1
    invoke_when: any surface is about to raise budget or scale an ad set
    inputs: live stock, days_of_stock, stockout projection
    outputs: pacing report, change list
    ---
    Purpose: never let ad spend outrun what the warehouse can actually ship, and
    catch a scaling opportunity for stock that has room to grow into.

    Steps
    1. Pull live stock and days_of_stock for every SKU in a budget-raise or
       scaling decision.
    2. Throttle spend on any SKU projected to stock out before the read window
       closes.
    3. Flag a scaling product early enough that a person can order more stock
       ahead of the ramp.
    4. Suggest a small clearance campaign for aged or grade-C inventory instead of
       leaving it to sell at full price alone.
    5. Suggest a new-arrivals campaign for fresh SKUs that have not had a fair
       chance yet.

    Checks
    - No scale-up is approved for a SKU with fewer days of stock than the read
      window needs.

    Output: pacing report, change list.

    Example: a winning ad set is about to get 2x budget but the SKU has 9 days of
    stock at current velocity and a 14-day read window -> hold the raise, flag the
    stock gap first.
