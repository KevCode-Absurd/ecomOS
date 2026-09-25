---
name: production-ops/naming-and-tagging
owner: crea-paid-creative-copy
version: 1
invoke_when: any asset needs a stable id and tags, or the platform-spec sheet
  or schema is due its periodic refresh
inputs: asset metadata, current platform specs, current naming schema
outputs: named/tagged asset, refreshed spec sheet, updated schema when needed
---
Purpose: keep every asset findable by a fixed schema, and keep the platform
spec sheet current, since a copy set built to a stale character limit fails
silently on upload.

Steps
1. Apply the fixed naming schema across its layers, campaign, ad-set, ad, so
   any asset's id tells a person what it is without opening the file.
2. Tag every asset on all 7 fixed fields: concept, persona, angle, offer,
   format, stage and source; a missing tag is a stop, not a skip.
3. Check the platform character-limit and spec sheet's last-checked date; if
   it is over 30 days old, re-check it against the platform's current help
   documentation before any copy gets written to that limit.
4. Periodically audit a sample of recently shipped assets against the
   current schema, naming every instance of drift found, and re-tag them.
5. Update the schema itself only when a genuinely new format, persona or
   offer type has entered the pipeline, never as a casual edit, and never in
   a way that breaks an existing asset's stable id.

Checks: every asset has a stable id; every asset carries all 7 tags; spec
sheet checked within 30 days when in active use.

Output: the tagged asset, or the refreshed spec sheet and schema.

Example: a static's id reads
concept-priceanchor_persona-budgetparent_angle-value_format-static_stage-cold,
so a person can read what it is from the filename alone.
