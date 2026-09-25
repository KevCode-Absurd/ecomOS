---
name: funnel-design
owner: ORG
version: 1
invoke_when: the founder wants strangers turned into owned contacts, or a post risks going viral without a capture path
inputs: offer/lead-magnet candidate, pillar map, current DM-automation policy, buyer-question map
outputs: comment-to-DM flow spec, policy check, viral-spike overflow plan, destination handoff
---
# Comment-to-DM and lead-magnet funnel design

## Purpose
Design how a post turns a stranger into an owned contact without breaking platform policy or overwhelming a human at the moment a post goes viral.

## Steps
1. Confirm the lead magnet answers something the avatar has actually asked for, sourced from org/buyer-question-mapping, not a generic percent-off code.
2. Design the comment-keyword-to-DM flow: the trigger keyword, the auto-reply text, and where it hands off to a human or a link.
3. Check the flow against current Meta/Instagram DM-automation policy for rate limits and disclosure requirements.
4. Design an overflow plan: the comment/view velocity that needs a human on standby, and what the flow says if volume exceeds capacity.
5. Map where the captured contact lands and hand the after-capture sequence to the Lifecycle specialist.
6. Package the whole design as a founder-gate card naming cost and platform-policy risk.

## Checks
- Lead magnet traces to an evidenced buyer want.
- Automation checked against current policy, not last year's.
- An overflow plan exists before launch.

## Output
{lead_magnet, flow{}, policy_check, overflow_plan, destination_handoff}

## Example
Trigger keyword "SIZE" auto-DMs the size guide link and asks one qualifying question, with a human handoff after 2 replies; overflow message queues a reply within 4 hours past 200 comments/hour.
