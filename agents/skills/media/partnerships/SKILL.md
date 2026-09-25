---
    name: partnerships
    owner: media-buyer
    version: 1
    invoke_when: the job is about affiliates, ad policy standing, or a new channel
    inputs: affiliate policy, claim tiers, current channel saturation
    outputs: routes to the correct partnerships sub-skill
    ---
    Purpose: hold the jobs that touch a partner, a platform's trust and safety team,
    or a channel the brand has not proven yet, since these carry a different risk
    shape than a normal campaign build.

    Steps
    1. Read the job: affiliate program health, an ad rejection or account-quality
       flag, a pilot on an unproven surface, or building a standing automation rule.
    2. Route to the matching sub-skill.
    3. Every sub-skill here is founder_gate by default; assemble the numbers and the
       range of choices, never a single recommendation dressed as the only option.

    Checks
    - No affiliate is approved, no appeal is submitted, no pilot spends, and no
      automation rule goes live without the founder's decision on record.
    - Every fraud or rejection flag carries its evidence, not a suspicion.

    Output: a routing decision to one partnerships sub-skill.

    Example: task says "an affiliate's conversions are landing in under 90 seconds
    of the click." -> routes to `media/partnerships/affiliate-program`.
