---
    name: tiktok-staged-read
    owner: media-buyer
    version: 1
    invoke_when: a 24-hour/3-day read point or ladder week is due
    inputs: ad group metrics, the test's read schedule
    outputs: staged test read, ladder-week read
    ---
    Purpose: read TikTok tests on the schedule that actually produces a trustworthy
    signal, since TikTok's own data can look decisive before it is.

    Steps
    1. At 24 hours, read soft metrics only: CTR, video views, add-to-cart rate.
    2. At 3 days, read cost metrics: CPA, ROAS; only now cut the bottom half.
    3. For a targeting-ladder week, read that week's isolated result before adding
       the next layer.
    4. After a fixed placement-read period, decide which automatic placements to
       opt out, not before.

    Checks
    - No ad group was cut before its 3-day cost read.
    - A ladder layer was judged on its own week's data, not blended with prior
      weeks.

    Output: a staged test read, a ladder-week read.

    Example: at 24 hours one ad group has a weak CTR but decent add-to-cart -> held
    to the 3-day cost read rather than cut early on CTR alone.
