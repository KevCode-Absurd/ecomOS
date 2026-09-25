---
    name: google-remarketing
    owner: media-buyer
    version: 1
    invoke_when: a new remarketing campaign is needed or lists need a rebuild
    inputs: order history, GA4 events, the brand's 5 objections
    outputs: remarketing list plan, change list
    ---
    Purpose: build remarketing lists worth using, and make sure every abandonment
    ad answers a real objection instead of just repeating the offer.

    Steps
    1. Build the cart-abandoner list: GA4 add-to-cart minus purchase.
    2. Check list size against Google's usable minimum before launching.
    3. Exclude existing customers from every prospecting campaign using this data.
    4. Map each abandonment ad to one of the brand's 5 real objections.
    5. Set up full-catalog dynamic remarketing for warm audiences.
    6. Build a high-value customer list as a lookalike seed for cold.

    Checks
    - Every list that launched had reached its usable size first.
    - No abandonment ad is a generic "still thinking it over" with no objection.

    Output: remarketing list plan, change list.

    Example: cart abandoners cite shipping cost as the top exit reason -> the
    abandonment ad leads with the free-shipping threshold, not a generic discount.
