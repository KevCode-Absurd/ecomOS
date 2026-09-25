---
    name: google-pmax
    owner: media-buyer
    version: 1
    invoke_when: the weekly PMax control check is due, or PMax is being qualified
    inputs: catalogue, margin, current PMax settings
    outputs: control checklist, asset group plan, change list
    ---
    Purpose: replace PMax's defaults with real controls, since the wizard's
    settings hide the levers a media buyer needs to trust the campaign.

    Steps
    1. Qualify the account first: proven feed, tracking, and existing Search/
       Shopping data. Never launch PMax as the first campaign type.
    2. Turn off final URL expansion (or restrict it) and every auto-created asset
       or automatic enhancement.
    3. Build theme-based asset groups, 2-20 of them; never one giant or single-
       product group.
    4. Build the full exclusion set: brand, URL, SKU, placement, age, customer
       list.
    5. Fix inputs in this order: feed, brand exclusion, structure, bidding,
       signals. Fixing bidding before the feed wastes the fix.
    6. Refresh asset counts every 4-6 weeks; feed proven Search terms and first-
       party lists in as signals.
    7. Check for warm-traffic over-crediting before raising target ROAS.

    Checks
    - No PMax setting is left on a default the agent has not deliberately chosen.
    - The exclusion set is complete, not partial.

    Output: control checklist, asset group plan, change list.

    Example: PMax is crediting itself for branded-search converters -> check brand
    exclusion first; it was missing, not the bidding.
