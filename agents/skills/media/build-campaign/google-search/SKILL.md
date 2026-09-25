---
    name: google-search
    owner: media-buyer
    version: 1
    invoke_when: the weekly Search loop is due, or new keywords/RSAs are needed
    inputs: offers, catalogue, current search-term report
    outputs: keyword/RSA plan, cleanup log, change list
    ---
    Purpose: bid only on proven or well-classified intent, and write ads that
    answer the real objection instead of just naming the product.

    Steps
    1. Classify keywords by intent; group into single-theme ad groups.
    2. Exact match on proven converters; broad match only with smart bidding and
       proof it works for this account.
    3. Write 7-9 RSA headlines from the brand's own offer; lead with product, price
       or offer, and let descriptions answer the real objection.
    4. Fix quality signals (landing page relevance, ad relevance) before raising a
       bid.
    5. Send cold, problem-aware clicks to an educational page, not straight to a
       buy box.
    6. Review search terms on a tighten-then-loosen cadence; promote converting
       broad terms to exact, remove clicked non-converters.
    7. Keep the account negative list clean, never blocking a real product search.

    Checks
    - No ad group mixes more than one search intent.
    - Every RSA answers an objection, not just a product description.

    Output: keyword/RSA plan, search-term cleanup log, change list.

    Example: "waterproof travel mug" search term converts well under a broad
    "travel mug" keyword -> promoted to its own exact-match keyword and ad group.
