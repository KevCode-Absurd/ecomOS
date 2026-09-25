---
name: special-formats/voice-clone-variants
owner: crea-paid-creative-copy
version: 1
invoke_when: a consenting person's voice needs cloning to produce many
  voiceover variants without a new recording session, only after consent is
  on file
inputs: documented written consent, script variants needing voiceover
outputs: voiceover variant set, cadence QA, logged use
---
Purpose: scale a real, consenting person's voiceover across many script
variants without booking a new session each time, while never exceeding what
that person actually consented to.

Steps
1. Confirm the specific person's documented written consent is on file,
   dated, named, and specific to this use; a general past consent for a
   different purpose does not carry over.
2. Prepare the cloned voice model using only the consented source
   recording, never a recording gathered for another purpose without a
   separate consent covering cloning.
3. Generate voiceover for each approved, audited script variant using the
   model.
4. Check the generated read against the real person's known cadence and
   pronunciation, catching anything that would sound obviously wrong, a
   mispronounced name or term the real person would actually say correctly.
5. Tag every generated line with the consent record id and log the use, so
   total uses can be checked against any limit the consent specifies.

Checks: consent on file before generation; use logged against any consent
limit.

Output: the finished, QA'd voiceover set and its logged use record.

Example: a founder consents to voice cloning for up to 20 script variants
over 6 months; each generated line is tagged and counted against that
limit.
