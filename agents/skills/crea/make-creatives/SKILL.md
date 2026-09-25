---
name: make-creatives
owner: crea-paid-creative-copy
version: 1
invoke_when: a task needs a finished or draft ad asset, not just copy
inputs: concept brief, format decision, brand kit, claim tiers
outputs: routes to one child skill by format and source
---
Purpose: hold the one router every creative-build job passes through, so the agent
never guesses between two production paths and every build starts from the same
brief and claim-tier check.

Steps
1. Read the concept brief's stated format (static, video, catalogue, carousel) and
   source (brand-made, creator, synthetic actor).
2. Match to exactly one child: static, ugc-video, founder-video, catalogue-dpa or
   carousel, using the format and source fields together, never format alone,
   since a video could be UGC or founder-led.
3. Call the child with the brief, the tagged reference set and the claim tiers
   attached, unmodified.
4. If no child fits, for example a brand-new format not yet covered, stop and
   draft a one-page workflow proposal instead of forcing a near match.

Checks
- Every routed job names which child ran, in the handoff note.
- No build proceeds without a concept brief attached.
- A format with no matching child never gets forced into the nearest one.

Output: the child skill's exact output, plus a one-line routing note.

Example: brief says format=video, source=founder -> routes to
crea/make-creatives/founder-video, not ugc-video.
