---
name: make-content/newsletter
owner: ORG
version: 1
invoke_when: the public organic newsletter's cadence calls for one issue
inputs: editorial calendar slot, brand voice file, claims tiers, prior issue performance
outputs: subject, preview text, body sections, one CTA, claims list, send recommendation
---
# Newsletter issue draft

## Purpose
Draft one issue of the brand's own public newsletter (Substack/Beehiiv style thought-leadership or editorial content), kept distinct from Life's lifecycle CRM email, which runs on triggers and flows rather than editorial cadence.

## Steps
1. Confirm the task is the public newsletter. If it is a promotional or flow email, stop and route it to the Lifecycle specialist instead.
2. Pick one editorial idea for the issue: a story, a teardown, a founder note. Never a grab-bag of unrelated links.
3. Write the subject line, under 50 characters, that the body actually pays off.
4. Write short body sections, one idea per section, with at least one first-hand fact the founder or team supplied, every factual line tier-checked.
5. Write exactly one CTA; a second competing CTA is cut.
6. Recommend a send day/time based on the last 4 issues' open pattern.

## Checks
- Confirmed as public newsletter, not CRM email.
- Subject line matches the body.
- One CTA only.

## Output
{subject, preview_text, body_sections[], cta, claims_used[], send_recommendation}

## Example
Subject: "The hinge that broke, and what we changed" - one CTA: reply with your own pothole story.
