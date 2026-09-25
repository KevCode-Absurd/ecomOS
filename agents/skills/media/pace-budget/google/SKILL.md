---
    name: google-bid-budget
    owner: media-buyer
    version: 1
    invoke_when: the weekly Google bid or budget review is due
    inputs: CPC, CPA, AOV, spend, current bid strategy
    outputs: bid stage plan, budget plan, pacing log
    ---
    Purpose: move Google bidding and budget forward in small, reversible steps
    tied to the brand's own break-even math, never a platform default or a big
    jump.

    Steps
    1. Cap a new account's bids at break-even CPA / conversion rate.
    2. Move to Maximize Conversion Value once conversions arrive; add Target ROAS
       only once volume supports it, set near the actual number.
    3. Size Shopping/Search launch budgets at 3-4x AOV/day; PMax at $50-100/day and
       3x non-brand CPA.
    4. Raise budgets in small weekly steps; cut faster than you raise.
    5. Treat "limited by budget" as a signal to test, not an automatic raise.
    6. Step bid targets gently; use an aggressive cut, not a timid one, to break a
       Target ROAS death spiral.

    Checks
    - No budget doubled or target halved in a single step.
    - Every cap traces to the brand's own break-even math.

    Output: bid stage plan, budget plan, pacing log.

    Example: account shows "limited by budget" on a campaign at 1.5x target ROAS ->
    treated as a signal to test a modest raise, not proof to double the budget.
