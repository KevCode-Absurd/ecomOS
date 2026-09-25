---
    name: read-results
    owner: media-buyer
    version: 1
    invoke_when: a job needs a performance read, forecast or staged test read
    inputs: platform, read cadence, metric contract
    outputs: routes to the correct platform sub-skill
    ---
    Purpose: keep every read built the same way, arithmetic in code, missing data
    marked unavailable, before the agent picks which platform's read shape applies.

    Steps
    1. Read the platform and the cadence: daily, a staged test read (24 hours,
       3 days), or a weekly blended read.
    2. Route to the matching sub-skill.
    3. Call `metric-read` for the fields needed; never estimate a field in prose.
    4. Keep totals separate from any breakdown; keep ad-level numbers when several
       ads share one image; flag dynamic or mixed creative instead of averaging it.

    Checks
    - No metric shows a computed 0 where the source was actually missing.
    - Every number a person will act on has a source and a date.
    - A read never states month-end or blended numbers as if they were today's actual.

    Output: a routing decision to one platform sub-skill.

    Example: task says "give me today's TikTok test read." Platform=tiktok,
    cadence=staged -> routes to `media/read-results/tiktok`.
