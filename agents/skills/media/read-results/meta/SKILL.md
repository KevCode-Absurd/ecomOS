---
    name: meta-daily-weekly-read
    owner: media-buyer
    version: 1
    invoke_when: the daily read, weekly read, or anomaly/forecast check is due
    inputs: spend, orders, revenue, trailing 14-day history
    outputs: daily read, weekly read, anomaly alert, spend forecast
    ---
    Purpose: give the founder one page a day and one a week on what is spent, what
    it returned, what moved sharply, and where the month is headed, all computed
    in code.

    Steps
    1. Blend spend, orders and revenue into MER in code.
    2. Compute the trailing 14-day median for spend and ROAS; flag days 50%+ off
       it.
    3. On a flagged day, check pixel/CAPI/feed health before blaming bidding; name
       the 3 ads that moved most.
    4. Treat sub-$1,000/day swings as noise, not signal.
    5. Split ROAS and conversion rate by device.
    6. Project month-end spend and MER from the trailing pace; flag a miss early.
    7. Mark any missing platform or day as unavailable, never zero.

    Checks
    - Every number traces to code, never model arithmetic.
    - No computed 0 hides a genuinely missing data point.

    Output: daily read, weekly read, anomaly alert, spend forecast.

    Example: ROAS drops 60% against the 14-day median on a Tuesday -> check CAPI
    health first; a dropped event, not bidding, explains the drop.
