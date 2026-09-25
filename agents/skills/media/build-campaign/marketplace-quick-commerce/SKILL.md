---
    name: marketplace-quick-commerce
    owner: media-buyer
    version: 1
    invoke_when: a rapid-delivery/grocery marketplace ad push is planned or a new listing is added (India only: a quick-commerce ad push)
    inputs: listing/stock status per fulfillment center (dark store, India only), category benchmarks, PROD-C49 margin report
    outputs: a retail media brief per platform
    ---
    Purpose: brief rapid-delivery and grocery marketplace ads (Instacart, DoorDash,
    Gopuff, Amazon Fresh; India only: Blinkit, Zepto, Instamart) only where a SKU's
    real transaction-value economics, not the platform's inflated list-price ROAS,
    already work, and only where stock can support the delivery.

    Steps
    1. Confirm the SKU is listed and in-stock at the fulfillment centers (dark
       stores, India only) the ad would run against.
    2. Read PROD-C49's contribution-margin report; require 3 consecutive positive
       weeks at that fulfillment center or dark store before proposing spend.
    3. Pick SKUs to sponsor by category search volume and current margin.
    4. Size the budget against the platform's own category CPC/ROAS benchmark, not
       a Meta or Google number.
    5. Flag stockout risk before any scale-up; rapid-delivery ad delivery can
       outpace local inventory fast.
    6. Keep the resulting report separate from Meta/Google in reporting.

    Checks
    - No SKU with a negative or unproven contribution margin is sponsored.
    - Stockout risk is checked before, not after, a budget increase.

    Output: a platform-specific retail media brief for a human to execute.

    Example: a SKU shows positive list-price-based ROAS on the platform dashboard
    but PROD-C49's transaction-value recompute shows negative margin (India only:
    the inflated number is MRP-based) -> brief holds that SKU back until the real
    number turns positive.
