---
    name: tiktok-spark-loop
    owner: media-buyer
    version: 1
    invoke_when: an organic post is ready to be tested as a paid Spark ad
    inputs: creator relationships, CREA-C38 authorization log
    outputs: Spark loop schedule, change list
    ---
    Purpose: turn a proven organic post into a paid Spark ad without ever running
    one that lacks a valid authorization, since that is a platform violation risk.

    Steps
    1. Post organically first; give it 5-7 days before judging it for Spark.
    2. Pick winners by real early engagement, not by which post the brand likes.
    3. Check CREA-C38's authorization log for a valid, unexpired code tied to that
       exact post. If missing, stop and hand the request to CREA, do not proceed.
    4. Keep any hook-test variant off the public organic profile; only the proven
       post gets Sparked.
    5. Set commission structure: open collabs for reach, targeted collabs for the
       brand's key partners.
    6. Schedule the Spark push once authorization is confirmed.

    Checks
    - Every Sparked post has a logged, unexpired authorization code.
    - No unapproved hook variant is public.

    Output: Spark loop schedule, change list.

    Example: a creator's post is performing well on day 6, but no authorization
    code is logged -> hold the Spark request, route to CREA for the code first.
