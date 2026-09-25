---
    name: trafficking-qa
    owner: media-buyer
    version: 1
    invoke_when: any campaign, ad set or ad on any platform is about to go live
    inputs: the built campaign, the approved plan, platform creative specs
    outputs: a pass/fail QA checklist
    ---
    Purpose: run the same fixed check an ad ops trafficker runs by hand before any
    launch, on any platform, so a known gap never goes live by accident.

    Steps
    1. Confirm the conversion event and pixel/CAPI fire on the exact landing page
       the ad points to, not a similar one.
    2. Confirm geo, age and placement targeting matches the approved plan.
    3. Confirm the UTM string matches the governed naming schema.
    4. Confirm frequency cap and dayparting, where used, are set as specified.
    5. Confirm creative meets the platform's current spec: aspect ratio, length,
       safe zones, text ratio.
    6. If any check fails, hold the launch and flag the founder; never launch with
       a known gap "to fix later."

    Checks
    - Every item on the list has a pass or fail, not a skip.
    - A failed check held the launch, with no exception.

    Output: a pass/fail checklist per campaign, ad set or ad.

    Example: the UTM campaign parameter is misspelled against the naming schema ->
    launch held, one-line fix requested before it goes live.
