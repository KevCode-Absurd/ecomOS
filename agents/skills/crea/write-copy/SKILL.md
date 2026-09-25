---
name: write-copy
owner: crea-paid-creative-copy
version: 1
invoke_when: a task needs written copy, not a visual or video build
inputs: angle brief, product facts, claim tiers, platform character limits
outputs: routes to one child skill by copy_type
---
Purpose: hold the one router every copywriting job passes through, so a hook
request never lands on the headline child by mistake and every draft carries
the same brand facts.

Steps
1. Read the copy_type the step names: primary text, headline, hook, or a
   full script.
2. Route to exactly one child. A cold-open video needs both hooks and scripts:
   call hooks first, then feed the winning hook into scripts.
3. Pass the angle brief, product facts and claim tiers to the child unchanged.
4. Return the child's output with a one-line note on which child ran, so the
   downstream compliance step knows which checklist applies.

Checks
- The right child ran for the stated copy_type.
- No copy is treated as finished before the compliance pass (a separate step in
  every workflow) runs on it.
- A copy_type with no matching child stops and asks a person rather than
  forcing a near match.

Output: the child skill's exact output plus a one-line routing note.

Example: task says copy_type=hook, format=video -> routes to
crea/write-copy/hooks; the winning hook then feeds crea/write-copy/scripts.
