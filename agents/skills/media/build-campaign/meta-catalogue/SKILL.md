---
    name: meta-catalogue
    owner: media-buyer
    version: 1
    invoke_when: DPA is running or about to launch, or the weekly catalogue check is due
    inputs: product catalogue, catalogue diagnostics, dynamic-ads health
    outputs: DPA health report, change list
    ---
    Purpose: keep dynamic product ads trustworthy by checking the feed before
    trusting the number, and by reading DPA on the attribution window that actually
    fits it.

    Steps
    1. Pull `ads_catalog_get_diagnostics` and `ads_catalog_get_dynamic_ads_health`.
    2. Check for missing images, prices, or stock-status gaps; flag any SKU with a
       gap before it gets more DPA spend.
    3. Confirm the product and customer sync into the catalogue ran on schedule and
       matches current order data.
    4. Confirm DPA lives in its own ad set outside the cold CBO campaign, capped as
       a share of total spend.
    5. Confirm DPA is read on 7-day click or incremental attribution, not the
       account's blended platform ROAS.

    Checks
    - No SKU with a missing image or wrong price is getting DPA spend.
    - DPA's reported number is never the same column as cold prospecting's ROAS.

    Output: a health report plus a change list for any feed or ad-set fix.

    Example: 40 SKUs show a stale price in the feed -> flag before scaling DPA,
    hand a developer brief to refresh the feed source, hold DPA spend at its
    current cap until fixed.
