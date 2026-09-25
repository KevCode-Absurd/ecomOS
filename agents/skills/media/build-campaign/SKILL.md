---
    name: build-campaign
    owner: media-buyer
    version: 1
    invoke_when: a job needs a new or rebuilt campaign, ad set, ad group or feed
    inputs: platform, channel, store type, brand brain catalogue and personas
    outputs: routes to the correct platform sub-skill
    ---
    Purpose: hold the one rule every campaign build shares before the agent picks a
    platform-specific procedure, so no build skips the basics because a specific
    sub-skill forgot to say it.

    Steps
    1. Read the platform (meta, google, tiktok, marketplace), the channel (search,
       shopping, feed, spark, retargeting) and, for a marketplace, the store type.
    2. Match to the one sub-skill whose select_by fields fit. Never guess between two.
    3. Hand the task to that sub-skill with the brand brain sections it needs already
       attached.
    4. If nothing matches, stop. Draft a one-page workflow proposal (what job, what
       inputs, what output) for a person to review. Never improvise a build.

    Checks
    - Every build gives the resulting campaign or ad set one stated job.
    - Every build excludes existing customers, brand terms or dead placements before
      it includes anything new, wherever that rule applies to the platform.
    - The name or naming pattern lets a person read results without opening the ad
      manager.

    Output: a routing decision to one platform sub-skill, or a workflow proposal.

    Example: task says "new Meta ad set for the travel-mug concept." Platform=meta,
    channel=cold ad set -> routes to `media/build-campaign/meta-concept`.
