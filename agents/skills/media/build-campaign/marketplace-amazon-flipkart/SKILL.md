---
    name: marketplace-amazon-flipkart
    owner: media-buyer
    version: 1
    invoke_when: a marketplace ad launch is coming, or the quarterly review is due
    inputs: marketplace catalogue, SKU margin, converting Google Search terms
    outputs: a ready-to-execute marketplace ad brief
    ---
    Purpose: since there is no Amazon, Walmart or Target connector (or Flipkart
    connector, India only), hand a human or agency a brief complete enough to
    build the campaign correctly the first time.

    Steps
    1. Pull bestseller and margin data; rank SKUs for sponsored placement priority.
    2. Seed keyword targets from the brand's own converting Google Search terms,
       plus the marketplace's own search suggestions.
    3. Build a negative keyword list for irrelevant marketplace searches.
    4. Set ACOS or TACOS targets from each SKU's real margin, not a category
       average.
    5. Propose a budget split across search, product-page and brand-store
       placements.
    6. Check the listing itself (bullets, images, A+ content) and flag anything
       that will cap ad performance before spend starts.

    Checks
    - Every ACOS/TACOS target traces to that SKU's own margin.
    - A weak listing is flagged, not launched into ads as-is.

    Output: a full campaign brief ready to build in the marketplace's own console
    (Amazon Seller Central, Walmart Connect, Target Roundel; Flipkart Ads Manager
    for the India option).

    Example: a SKU has only 3 product images and no bullet points -> flagged to fix
    the listing before its ACOS target is set or spend begins.
