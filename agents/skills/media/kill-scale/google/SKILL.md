---
    name: google-scaling-gates
    owner: media-buyer
    version: 1
    invoke_when: a Google budget increase or new campaign type is proposed
    inputs: ROAS, spend, the account's 5 scaling gates
    outputs: scaling gate checklist result, change list
    ---
    Purpose: earn a Google budget increase through 5 fixed gates instead of a gut
    call, while still moving fast on a genuine winner.

    Steps
    1. Check the campaign already hits target ROAS at its current budget; if not,
       stop here.
    2. Run the 5 scaling gates in order and record a pass/fail on each.
    3. In steady state, cut underperformance fast; do not wait out a slow bleed.
    4. On a clear winner or a real demand spike, move fast rather than the usual
       small weekly step.
    5. For YouTube, scale in order: budget and creative first, then hooks and
       offers, then new formats.

    Checks
    - Every gate has a recorded pass/fail, not a summary judgement.
    - No increase went through with a failed gate unaddressed.

    Output: scaling gate checklist result, change list.

    Example: a campaign hits target ROAS but fails the frequency-of-conversion
    gate -> hold the budget increase until that gate passes.
