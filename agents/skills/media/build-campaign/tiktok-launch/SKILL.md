---
    name: tiktok-launch
    owner: media-buyer
    version: 1
    invoke_when: a new TikTok account or relaunch needs its first campaign
    inputs: catalogue, creative library, TikTok account state
    outputs: launch checklist, change list, first test read
    ---
    Purpose: get a TikTok account's first campaign live correctly, broad, and read
    on a fixed schedule, since a wrong first setup wastes the account's early data.

    Steps
    1. Complete account setup (business center, pixel, catalog connection if used)
       before any spend.
    2. Test every pixel event; stop if Purchase or Add to Cart fails to fire.
    3. Launch a manual Sales campaign, catalog off for the first test.
    4. Set the ad group to broad targeting, Complete Payment optimisation, no
       target CPA yet.
    5. Keep interests to 2-5 parent categories; never stack 15-20 interests.
    6. Set daily budget at the greater of $50 or 2x current CPA per ad group.
    7. Run 2 ad groups by 3 creatives by $50/day for 3-4 days.
    8. Read soft metrics at 24 hours, cost metrics at 3 days; cut the bottom half.
    9. Run the pre-launch QA check before anything goes live.

    Checks
    - Pixel events confirmed firing before spend.
    - No more than 5 stacked interests in any ad group.

    Output: launch checklist, change list, first test read.

    Example: Purchase event fires but with no value passed -> hold the launch,
    send a developer brief to fix value passing before spending.
