---
    name: suggestion-filter
    owner: media-buyer
    version: 1
    invoke_when: the weekly platform-suggestion review is due
    inputs: platform suggestion log, past outcomes
    outputs: suggestion log, apply/reject change list
    ---
    Purpose: stop blind acceptance of platform-suggested changes, and keep a real
    record of whether each one actually helped last time.

    Steps
    1. Log every suggestion with its platform-stated expected effect.
    2. Sandbox-test where the suggestion is testable in isolation.
    3. Check whether a "targeting" suggestion is a real control or just a
       non-binding nudge.
    4. Confirm auto-apply and AI-generated assets are off by default.
    5. Record the real effect of anything applied, against what the platform
       claimed.

    Checks
    - No suggestion was applied without a logged reason.
    - Auto-apply is off unless the founder explicitly turned it on.

    Output: suggestion log, apply/reject change list.

    Example: Google suggests raising a Target ROAS bid; last quarter's identical
    suggestion cut conversions 15% -> logged and rejected, with the history cited.
