---
    name: google-merchant-feed
    owner: media-buyer
    version: 1
    invoke_when: Merchant Center needs setup, a disapproval needs fixing, or the weekly feed check is due
    inputs: policies, product catalogue, reviews, current feed
    outputs: setup checklist, feed audit, rewrite batch, change list
    ---
    Purpose: keep the feed eligible, trustworthy and search-matchable, since a bad
    feed caps every Shopping and PMax result before bidding ever gets a chance.

    Steps
    1. Match Merchant Center's business info to the live site; enroll the 4 add-ons.
    2. Fix any disapproval first, before it becomes limited performance; never claim
       an identity attribute that is not true by Google's definition.
    3. Rewrite titles: converting search term + product type first, inside 70
       characters, no stuffing. Roll changes out in batches with a baseline.
    4. Give every variant its own GTIN; never duplicate a product at multiple
       prices; run one feed per currency.
    5. Refresh the feed at least every 6 hours; automate updates for frequent price
       changes.
    6. Tag custom labels for margin, bestseller status and stock priority.
    7. Test lifestyle vs plain images; supply a 4:5 image feed to beat auto-crop.

    Checks
    - No open disapproval past its warning window.
    - Every title change has a recorded baseline to measure against.
    - No duplicate GTIN, no duplicate product at two prices.

    Output: setup checklist, feed audit, rewrite batch, change list.

    Example: 12 SKUs are disapproved for a missing GTIN -> fix listed first, before
    any title rewrite batch goes out, since disapprovals cap everything else.
