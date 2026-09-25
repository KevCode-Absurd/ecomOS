---
    name: rule-automation
    owner: media-buyer
    version: 1
    invoke_when: kill/keep/scale and bid thresholds are established and ready to standardise
    inputs: existing thresholds, platform automation capability
    outputs: documented rule set, firing log
    ---
    Purpose: turn thresholds the brand already uses by hand into standing,
    auditable automations, never a new rule invented on the spot, and never live
    until the founder switches writes on.

    Steps
    1. Translate each existing threshold into an explicit if-then rule per
       platform.
    2. Keep the rule set consistent across Meta, Google and TikTok, adapting only
       for each platform's own automation options.
    3. Log every firing with the before and after state.
    4. Auto-pause a rule that fires far more than expected; that usually means
       tracking broke, not that the rule found real signal.
    5. Hold every rule inactive on a surface until the founder switches writes on
       for it.

    Checks
    - Every rule traces to a threshold already approved elsewhere, not a new one.
    - No rule is live on a surface without writes switched on.

    Output: documented rule set, firing log.

    Example: the existing kill rule (3-5x target CPA) becomes an if-then rule that
    pauses an ad set at 4x CPA and logs the before/after spend -- but stays
    dormant until Meta writes are switched on.
