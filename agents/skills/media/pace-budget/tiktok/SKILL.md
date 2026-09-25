---
    name: tiktok-budget-ladder
    owner: media-buyer
    version: 1
    invoke_when: a TikTok ad group needs budget set, or the ladder's next week is due
    inputs: current CPA per ad group, current ladder week
    outputs: budget and ladder pacing plan
    ---
    Purpose: size TikTok budget from a fixed floor tied to CPA, and add targeting
    layers on a controlled weekly cadence instead of all at once.

    Steps
    1. Set daily budget at the greater of $50 or 2x current CPA, per ad group.
    2. Add structure only with budget growth: broad first, then one interest ad
       group, capped at 4 ad groups total.
    3. Run the 4-week targeting ladder, one new layer per week.
    4. Before dropping interests or lookalikes entirely, run one controlled 7-day
       broad-vs-stacked test rather than guessing.
    5. Wait for a new audience to finish populating before spending against it.

    Checks
    - No ad group runs under the $50/2xCPA floor.
    - No more than one new targeting layer was added in a week.

    Output: a budget and ladder pacing plan.

    Example: current CPA is $30 -> daily budget floor is $60 (2x CPA), not $50.
