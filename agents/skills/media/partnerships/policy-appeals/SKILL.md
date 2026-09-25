---
    name: policy-appeals
    owner: media-buyer
    version: 1
    invoke_when: a new disapproval lands or the daily account-quality check is due
    inputs: disapproval reasons, account-quality dashboards, claim tiers
    outputs: rejection log, appeal drafts, account-quality trend flag
    ---
    Purpose: treat every ad rejection as a diagnosable policy-clause problem with a
    named fix, instead of a one-off surprise, and catch an account-quality slide
    before it becomes a restriction.

    Steps
    1. Pull every disapproved ad and its stated reason daily.
    2. Map the reason to the exact policy clause and the likely real cause: claim,
       image text ratio, restricted-category wording, or landing page mismatch.
    3. Propose the smallest edit that clears the violation without changing the
       offer or claim tier.
    4. Draft an appeal only for a rejection believed wrongly applied; a human
       submits it.
    5. Watch the account-quality score for a downward trend and flag it early.
    6. Log rejection reasons by category to catch a repeating pattern.

    Checks
    - Every rejection has a named clause and a proposed fix.
    - No appeal is submitted without a human review of the draft.

    Output: rejection log, appeal drafts, account-quality trend flag.

    Example: 4 ads in one week rejected for the same "before/after" claim wording
    -> pattern logged, a claim-tier fix proposed once instead of firefighting each
    ad separately.
