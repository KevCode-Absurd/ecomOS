---
    name: pace-budget
    owner: media-buyer
    version: 1
    invoke_when: a job needs a budget size, a bid setting or a stock-aware spend check
    inputs: platform, decision type, metric contract fields
    outputs: routes to the correct platform sub-skill
    ---
    Purpose: keep every budget number computed the same way, in code, from a named
    formula, before the agent picks which platform's formula applies.

    Steps
    1. Read the platform and the decision: sizing a new test, stepping a winner,
       pacing against stock, or moving through a bid stage ladder.
    2. Route to the matching sub-skill.
    3. Pull `metric-read` (shared skill) for the fields the formula needs; if a field
       is unavailable, say so and stop rather than substituting a guess.
    4. Never state a number the agent computed in its own reasoning; call the
       formula in code and report what it returns.

    Checks
    - Every number traces to a named formula, not a feeling.
    - Live stock is checked before any recommendation to raise spend, wherever stock
      applies to the decision.
    - No budget change is proposed on a surface the founder has not switched writes
      on for; the output is a change list.

    Output: a routing decision to one platform sub-skill.

    Example: task says "size the read window for the new hook test." Platform=meta,
    decision=test sizing -> routes to `media/pace-budget/meta`.
