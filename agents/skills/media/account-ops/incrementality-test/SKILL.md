---
    name: incrementality-test
    owner: media-buyer
    version: 1
    invoke_when: platform ROAS and blended MER disagree after attribution is tightened
    inputs: ROAS, spend, geographic sales spread
    outputs: test brief, result writeup, registry entry
    ---
    Purpose: find out whether disputed spend is buying orders that would not have
    happened anyway, only after cheaper fixes (attribution, reconciliation) are
    already done.

    Steps
    1. Confirm attribution is already tightened and reconciled; this test is not a
       substitute for that work.
    2. Pick the test type: Meta Conversion Lift, geo holdout, or matched-market
       geo test.
    3. Size the split, minimum spend and read window.
    4. Write the brief: hypothesis, holdout design, read point, proof bar.
    5. Read the result; update the brand's own effect prior for that spend level.
    6. Feed the result into budget decisions; never let it change bidding directly.

    Checks
    - Reconciliation happened first; the test is not a first resort.
    - The result is logged to the registry, win or lose.

    Output: test brief, result writeup, registry entry.

    Example: Meta shows 4x ROAS but blended MER shows 1.8x even after
    reconciliation -> a geo holdout is sized to find the real incremental lift.
