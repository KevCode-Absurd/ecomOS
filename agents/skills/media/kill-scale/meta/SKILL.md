---
    name: meta-kill-scale
    owner: media-buyer
    version: 1
    invoke_when: daily ad-set metrics need a keep, kill or scale call
    inputs: CPA, ROAS, frequency at ad-set level
    outputs: daily call list, change list for budget moves
    ---
    Purpose: make Meta's daily budget calls a fixed table read, and scale a winner
    by finding its real spend equilibrium instead of riding it blind.

    Steps
    1. Read the keep/yellow/kill table at 3-5x target CPA, at the ad-set level.
    2. Never touch a winning ad set directly; fork new creative beside it instead.
    3. Keep creative tests out of the scaling campaign entirely.
    4. For a high-conviction ad starved by CBO, rescue it in a small, capped,
       logged ad set of its own.
    5. Step a winner's budget up in sizes matched to the read window; find the
       point ROAS turns unprofitable, then pull back to just before it.
    6. Move only a confirmed equilibrium winner into the dedicated scaling
       campaign.
    7. Judge any raise over 7+ days; confirm new-customer share under 7-day click
       before briefing more of that creative.
    8. Flag rising frequency on a top-spending prospecting ad before scaling it.

    Checks
    - No call was made on one ad's number inside a larger ad set.
    - No winner was edited in place; it was forked or stepped.

    Output: daily call list, change list.

    Example: an ad set holds at 3.8x target CPA for 8 days after a 20% budget
    step -> equilibrium found; hold there, do not step again this week.
