---
    name: kill-scale
    owner: media-buyer
    version: 1
    invoke_when: a job needs a keep, kill or scale call
    inputs: platform, decision unit, the platform's own kill/keep/scale table
    outputs: routes to the correct platform sub-skill
    ---
    Purpose: keep every kill, keep or scale call a fixed table read, not a feeling,
    before the agent picks which platform's table and unit-of-decision applies.

    Steps
    1. Read the platform and the unit the call is made on: Meta ad set, TikTok ad
       group, a marketplace SKU, or a targeting layer.
    2. Route to the matching sub-skill.
    3. Read the table at the platform's own multiple of target CPA; never judge on
       one ad's own ROAS or same-day revenue.
    4. Log the call to the registry (`shared/registry-entry`) so the next read has
       the history.

    Checks
    - The call was made at the right unit, never one ad inside a winning ad set.
    - A winner was stepped or forked into a new unit, never edited directly.
    - Every kill or scale call is dated and has a reason a founder could repeat.

    Output: a routing decision to one platform sub-skill.

    Example: task says "should we kill the lookalike layer on TikTok?" Platform=
    tiktok, unit=targeting layer -> routes to `media/kill-scale/tiktok`.
