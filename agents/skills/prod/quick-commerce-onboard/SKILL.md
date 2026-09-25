---
name: prod/quick-commerce-onboard
owner: PROD
version: 1
invoke_when: a new quick commerce launch is planned for Blinkit, Zepto or Instamart
inputs: GST, FSSAI, barcode and packaging documents, the target platform(s)
outputs: a submitted document packet, review status, initial listing, and go-live confirmation
---
# Onboard a brand on quick commerce

## Purpose
Quick commerce onboarding requires a specific document set and each platform runs its own review process and its
own unit-economics validation window (commonly around 90 days) before the brand is judged to be worth investing
in further. Missing a required document is the most common cause of onboarding delay.

## Steps
1. Assemble the GST, FSSAI, barcode and packaging documents the platform's own onboarding checklist requires,
   confirming every item is present before submission.
2. Submit through the platform's own onboarding channel, never a workaround or a third-party shortcut.
3. Track the document review status and respond to any query the platform raises within its stated window.
4. Prepare the initial catalogue listing using the matching Blinkit or Zepto listing skill.
5. Confirm the platform's own unit-economics validation window and what it requires the brand to demonstrate
   during it.
6. Get the brand live and confirm the first order flows correctly end to end before calling onboarding complete.

## Checks
- Every document the platform's checklist requires is present before submission.
- The validation window and its specific requirement are both logged, not assumed.

## Output
{document_packet, review_status, initial_listing, validation_window, go_live_confirmation}

## Example
Documents assembled: GST, FSSAI licence, barcode registration, packaging compliance declaration. Submitted through
the platform's seller onboarding portal. One query on FSSAI scope resolved within 2 days. First order confirmed to
flow correctly on day 12 of a stated 90-day validation window.
