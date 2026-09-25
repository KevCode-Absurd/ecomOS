---
    name: cross-border-setup
    owner: media-buyer
    version: 1
    invoke_when: a new market launch is planned
    inputs: markets served, shipping policy
    outputs: market setup checklist, change list
    ---
    Purpose: set every new market up with its own honest currency, duty and
    delivery message before ads run there, since a wrong promise on delivery time
    or landed cost creates the exact objection the ad should be preventing.

    Steps
    1. Set local currency, payment methods and language defaults for the new,
       mobile-first, non-US market.
    2. Write duty and delivery-time messaging specific to that market into the ad
       copy.
    3. Show shipping cost and import duty in the Google feed for cross-border
       orders.
    4. Run one Google feed per currency; never mix currencies in one feed.

    Checks
    - Every market's ads state its own delivery time and duty, not a generic one.
    - No feed mixes currencies.

    Output: market setup checklist, change list.

    Example: launching into UAE from an India-based store -> new feed in AED,
    duty and delivery time called out in ad copy, separate from the India feed.
