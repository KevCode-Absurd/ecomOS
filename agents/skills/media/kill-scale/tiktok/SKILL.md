---
    name: tiktok-kill-scale
    owner: media-buyer
    version: 1
    invoke_when: a 3-day read or ladder week's result is in
    inputs: ad group metrics, the staged or ladder read
    outputs: scaling plan, kill list, change list
    ---
    Purpose: move a proven TikTok creative into a real scaling campaign while
    keeping the testing lane alive, and prune weak layers before they compound.

    Steps
    1. Cut the bottom half of ad groups/creatives at the 3-day cost read.
    2. Move a winner into its own CBO scaling campaign; keep testing running in the
       manual campaign in parallel.
    3. Opt out weak automatic placements after a placement read.
    4. Drop a targeting-ladder layer that did not earn its proving week before
       adding another.
    5. Run one controlled 7-day broad-vs-stack test before abandoning interests or
       lookalikes for good.

    Checks
    - Testing continued in the manual campaign even after a winner moved to
      scaling.
    - No ladder layer was kept past its proving week without a positive result.

    Output: scaling plan, kill list, change list.

    Example: a hook wins its 3-day read at 2.1x target CPA -> moved to its own CBO
    scaling campaign; the manual campaign keeps testing the next 3 hooks.
