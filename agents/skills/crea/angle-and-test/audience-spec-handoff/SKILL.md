---
name: angle-and-test/audience-spec-handoff
owner: crea-paid-creative-copy
version: 1
invoke_when: an angle's persona needs to become a concrete targeting spec for
  MEDIA, without CREA touching the ad account
inputs: angle brief, persona/avatar record, past audience performance
outputs: audience spec record handed to MEDIA
---
Purpose: translate a persona into age, traits and exclusions a media buyer can
act on, while keeping account-building and launch strictly on MEDIA's side of
the line.

Steps
1. Pull the persona's real, research-grounded traits: age range, stated
   interests, in-group language, and what they say they already tried and
   rejected.
2. Translate each trait into a field a targeting spec actually uses: an age
   range, an interest or behavior category, or a lookalike seed source; a
   trait that cannot translate honestly is left out rather than forced.
3. Set exclusions explicitly: current customers who should not see a cold
   angle, brand-term searchers, and any persona this specific angle would
   alienate.
4. Package the spec with the source persona id and the angle id so MEDIA can
   trace it back to the research behind it.
5. Hand the spec to MEDIA as a structured request and stop; CREA never opens
   an ads-manager targeting screen itself.

Checks: every trait traces to the persona record; exclusions stated, not
assumed; handoff is a request, not an action.

Output: the audience spec record, logged and sent to MEDIA.

Example: persona "budget-anxious new parent, 24-34" becomes age 24-34,
interest tags for baby-gear comparison content, lookalike seed from past
90-day purchasers, exclusion on existing customers and brand-term searchers.
