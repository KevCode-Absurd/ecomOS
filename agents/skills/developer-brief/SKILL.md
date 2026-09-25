---
name: developer-brief
owner: shared (Site writes most)
version: 1
invoke_when: an approved item needs a person to change code, a theme, a setting or DNS
inputs: the approved idea record, the observed condition with evidence, the measured or expected effect, the surface (platform, page, setting), rollback path
outputs: one brief per change, in the founder page format (change, where, why, check, rollback)
---
# Developer brief

## Purpose
Turn an approved change into instructions a developer can follow without asking a question, and a founder can read.

## Steps
1. Name the change in one line, as an action ("Turn off Rocket Loader in Cloudflare").
2. Where: the exact place (platform, admin path, file, theme section, DNS record). Quote the current value from the brain snapshot.
3. Why: the observed condition and the number it moves, with the basis (measured on a copy, source claim, general practice).
4. Steps: numbered, one action each, no branching. If a step depends on a plan or plugin version, say which.
5. Check: what to look at after, and the number that should change. Give the measurement command or page.
6. Rollback: how to undo in one step, and how long it takes.
7. Risk: what could break, and who to tell.

## Checks before returning
- No placeholders. No "as needed".
- Current value quoted from the snapshot, dated.
- Check step names a metric from the contract or the speed lab.
- Rollback exists and is one step.
- Reading level under grade 10.

## Output
Markdown brief plus JSON: {change, where, why, steps[], check, rollback, risk, surface, needs_write}.
