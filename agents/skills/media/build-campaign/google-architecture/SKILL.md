---
    name: google-architecture
    owner: media-buyer
    version: 1
    invoke_when: new account, an audit flags structure, or the monthly brand check is due
    inputs: catalogue, margin, brand terms, prior audit
    outputs: architecture diagram, brand/non-brand split plan, change list
    ---
    Purpose: give every Google campaign one job, and make sure brand-name traffic
    never gets counted as growth.

    Steps
    1. Map every campaign to one funnel job; flag any overlap.
    2. Default to one campaign per job; a second campaign for the same job needs a
       written reason.
    3. One campaign per country; never mix locations inside one PMax.
    4. Set safe defaults on anything new: Sales objective, Purchase-only goal,
       Search Partners and Display off, Presence targeting, tablets/TV off.
    5. Split brand from non-brand everywhere it can run: Search, Shopping, PMax.
    6. Exclude brand from cold campaigns with a negative list AND an audience
       exclusion, not just one of the two.
    7. Put brand on manual bidding or impression share at a higher ROAS target;
       check impression share actually covers the brand name.
    8. Scan cold-campaign search terms monthly for brand leakage; merge orphan
       campaigns into the account's real structure.

    Checks
    - Every campaign traces to one job and, if extra, a written reason.
    - No brand traffic inflates the non-brand growth number.

    Output: architecture diagram, split plan, change list.

    Example: a PMax campaign is running for both the US and Canada -> split into two
    country campaigns with a written reason (currency and duty messaging differ).
