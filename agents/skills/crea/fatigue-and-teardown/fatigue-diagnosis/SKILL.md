---
name: fatigue-and-teardown/fatigue-diagnosis
owner: crea-paid-creative-copy
version: 1
invoke_when: a live ad's numbers are declining and need sorting into
  worn-out-creative versus small-audience-pool before any fix is proposed
inputs: lifecycle metrics, delivery/frequency data, hook and structure
  history
outputs: cause split, fatigue diagnosis note
---
Purpose: stop a small, undertested audience pool from being misdiagnosed as
a tired creative, and vice versa, since the fix for each is completely
different and the wrong one wastes a production cycle.

Steps
1. Compare the ad's current frequency, hold rate and CPA trend against this
   account's own historical curve for that format, not a generic industry
   benchmark.
2. Check whether reach growth for the ad set has actually flattened; a
   declining CTR alongside reach that is still growing points to a
   targeting or sequencing issue, not creative wear-out.
3. Split the cause explicitly: audience-pool exhaustion or genuine creative
   fatigue, naming the specific number that decided it.
4. For a creative cause, name the specific part that wore out, the hook, the
   visual, or the whole concept, rather than a general "this ad is tired"
   verdict with nothing actionable in it.

Checks: cause split cites a specific number; creative diagnosis names one
specific part.

Output: the cause split and, for creative causes, the diagnosis note.

Example: CTR down 25% but ad-set reach still growing 15% week over week
means a sequencing problem, routed to MEDIA, not a creative revival.
