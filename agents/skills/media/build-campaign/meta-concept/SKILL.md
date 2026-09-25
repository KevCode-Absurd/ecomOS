---
    name: meta-concept
    owner: media-buyer
    version: 1
    invoke_when: a new SKU, pain point or offer is ready to test on Meta
    inputs: personas, offers, SKUs, creative references, prior audit
    outputs: ad set build plan, change list
    ---
    Purpose: turn one tested idea into one correctly built Meta ad set: broad,
    excluded from existing customers, with clean placements and enough ads to be
    read fairly.

    Steps
    1. Define the concept: one SKU, one pain point, one offer. Any change to one of
       these starts a new ad set, not an edit to this one.
    2. Check for persona overlap with a live ad set; keep non-overlapping personas
       apart.
    3. Go broad by default. Let price, page and reviews qualify the buyer; put
       targeting logic in the creative, not the settings. Cap any interest or
       lookalike test as a small, labelled sandbox.
    4. Exclude existing customers, sized to the repurchase cycle.
    5. Turn off weak placements and every automatic creative edit on product ads.
    6. Pick CBO by default (ABO only at high AOV, low volume); set any cap at ad
       set level.
    7. Load 2-6 exposures worth of ads (minimum 3: the concept ad plus 3 hooks).
    8. Pass the built ad set to the pre-launch QA skill before it goes live.

    Checks
    - One SKU, one pain point, one offer per ad set.
    - Existing customers excluded; broad targeting used; sandbox tests labelled and
      capped.

    Output: an ad set build plan a human applies, plus the change list.

    Example: new offer "buy 2 get 1 on travel mugs" for the commuter persona ->
    one new ad set, broad cold, commuter-persona exclusion of existing buyers,
    concept ad + 3 hooks, CBO, $0 interest narrowing.
