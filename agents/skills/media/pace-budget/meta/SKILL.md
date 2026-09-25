---
    name: meta-test-sizing
    owner: media-buyer
    version: 1
    invoke_when: a new Meta creative test is ready to size
    inputs: target CPA, purchase cycle, planned test budget
    outputs: test brief, kill-rule sheet
    ---
    Purpose: size a Meta creative test so its result can actually be trusted,
    instead of leaning on the platform's own learning-phase suggestion.

    Steps
    1. Compute the test budget: target conversions x CPA / test days, in code.
    2. Set the kill-rule threshold: 3-5x target CPA before any judgement.
    3. Set the read window to match the purchase cycle; never under 5 days below
       $50k/month spend.
    4. Confirm the planned daily budget can reach the read-spend threshold within
       that window; if not, raise the budget or extend the window before launch.
    5. Never allow a same-day or $1-2-spend kill call.

    Checks
    - The budget came from the formula, not Meta's 50-conversions rule.
    - The ad set can mathematically reach its read threshold in the window given.

    Output: a test brief (budget, read window, kill rule) for the launch.

    Example: target CPA is $20, target 15 conversions to judge, test runs 5 days ->
    budget = 15 x $20 / 5 = $60/day.
