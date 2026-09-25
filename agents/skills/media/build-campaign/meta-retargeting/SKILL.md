---
    name: meta-retargeting
    owner: media-buyer
    version: 1
    invoke_when: existing-customer Meta spend needs setting up or resizing
    inputs: repurchase cycle, customer segments, LIFE-C32 budget/CPA memo
    outputs: retargeting campaign plan, change list
    ---
    Purpose: run existing-customer paid spend as one disciplined, isolated campaign
    at a budget the Lifecycle specialist set from margin, never a percentage
    guess or a bleed off cold budget.

    Steps
    1. Read the existing-customer budget dollar figure and CPA ceiling from LIFE-C32.
       If it is missing, stop; this is a founder-gated number, not one the media
       buyer sets.
    2. Build or confirm one dedicated existing-customer campaign; do not let this
       spend live inside a cold campaign.
    3. Size the budget in dollars and by target frequency, not as a percent of the
       account.
    4. Check whether a separate visitor-retargeting campaign is even needed; skip
       it unless the engaged segment is spend-starved.
    5. Write ad copy around a different objection or proof point than the cold ad.
    6. Time win-back messaging to the customer's typical reorder date.
    7. Set up a lapsed-customer campaign on its own strategy if one does not exist.

    Checks
    - Spend and CPA match the LIFE-C32 memo exactly.
    - No segmentation deeper than the plan calls for.

    Output: campaign plan and a change list for a human to apply.

    Example: LIFE-C32 sets $2,000/month at a 45-day CPA ceiling half the new-
    customer target -> one existing-customer campaign at that budget, non-buyer ad
    on a different objection, reorder-timed win-back ad.
