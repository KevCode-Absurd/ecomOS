---
    name: channel-pilot
    owner: media-buyer
    version: 1
    invoke_when: existing channels are near their scaling gates, or a DSP is being considered
    inputs: channel saturation state, candidate shortlist, CAC/ROAS targets
    outputs: go/no-go recommendation, pilot test plan
    ---
    Purpose: only add a new channel or DSP once the existing ones are genuinely
    saturated, and give any pilot the same stop/scale discipline as a creative
    test, read against the brand's own targets.

    Steps
    1. Confirm saturation with frequency and reach data before recommending
       anything new.
    2. Shortlist DSPs or surfaces by real fit to the brand's category and data,
       not by trend.
    3. Size the pilot budget as the smallest spend that produces a usable read.
    4. Set stop and scale thresholds before the pilot starts.
    5. Build minimum viable creative and tracking without pulling from the main
       creative pipeline.
    6. Read the pilot against the brand's own CAC/ROAS targets, not the new
       platform's benchmarks.
    7. Log the result to the registry whether it wins or fails.

    Checks
    - Saturation was confirmed with data, not assumed.
    - The pilot has a stop and a scale threshold set before it started.

    Output: go/no-go recommendation, pilot test plan.

    Example: Meta and Google retargeting frequency has plateaued at reach's edge
    -> a small, capped Criteo pilot is sized and read against the brand's own CAC
    target, not Criteo's benchmark.
