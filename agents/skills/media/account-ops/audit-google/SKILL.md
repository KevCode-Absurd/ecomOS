---
    name: audit-google
    owner: media-buyer
    version: 1
    invoke_when: the monthly Google Ads audit is due
    inputs: account/campaign structure, spend, conversions
    outputs: audit report, diagnosis writeup, change list
    ---
    Purpose: diagnose a Google account top down, in the order a problem actually
    unfolds, instead of jumping straight to a setting change.

    Steps
    1. Pull account and campaign structure, spend and conversions.
    2. Diagnose top down: business level, then channel share, then campaign, then
       metric, then root cause.
    3. Apply the 3 pre-diagnosis rules before touching anything.
    4. Find the inflection date of any dip; check only the top 5 campaigns by
       spend around that date.
    5. Match the failure-mode checklist to the campaign type that dipped.
    6. Split CPA and clicks into impressions, CTR and CVR to isolate the real
       cause.
    7. Try the isolated fix first; propose a rebuild only after it has failed.

    Checks
    - The diagnosis order was followed, not skipped to a favorite fix.
    - An isolated fix was tried before any rebuild reached the roadmap.

    Output: audit report, diagnosis writeup with root cause, change list.

    Example: CPA rose 30% -> traced to a CTR drop, not a CVR drop -> points to an
    ad-fatigue or ranking cause, not a landing-page cause.
