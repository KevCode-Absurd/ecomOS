---
    name: audit-meta
    owner: media-buyer
    version: 1
    invoke_when: the monthly Meta account audit is due
    inputs: 12 months of account/campaign/ad-set/ad data
    outputs: audit report, ranked 90-day roadmap, change list
    ---
    Purpose: turn a raw Meta account into one ranked constraint a founder can act
    on, not a list of screenshots or ten equal-weight observations.

    Steps
    1. Pull 12 months of account, campaign, ad set and ad data from the gallery
       cache plus a fresh re-pull.
    2. Run the structure checklist: purpose lines, ad-set count vs spend tier,
       naming, CBO/ABO use.
    3. Run the creative review in order: volume, then diversity, then quality.
    4. Score the account on readable-data and commercial-alignment tests.
    5. Validate any structure change idea against 4 fixed questions before it
       enters the roadmap.
    6. Rank every finding by money at stake, not ease of fix.
    7. Write the roadmap as dated, ranked actions, each with the metric it should
       move.

    Checks
    - The roadmap names ONE biggest constraint, not a flat list.
    - Every finding has a number and a source.

    Output: audit report, ranked 90-day roadmap, change list.

    Example: naming is inconsistent AND creative volume is thin -> roadmap ranks
    creative volume first because it is costing more, names naming as a fast,
    smaller fix underneath it.
