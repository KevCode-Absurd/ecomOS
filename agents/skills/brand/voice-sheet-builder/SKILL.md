---
name: voice-sheet-builder
owner: BRAND
version: 1
invoke_when: a new brand needs a default voice, or an existing sheet needs building or refreshing after drift is found
inputs: Kevin's liked and disliked copy examples, brand story and values
outputs: voice and tone sheet, short and full versions
---
# Voice sheet builder

## Purpose
Any writer or model needs a concrete, example-based reference to sound consistently like this brand. A list of adjectives ("friendly, bold, premium") does not achieve that; real liked and disliked examples do.

## Steps
1. If no voice sheet exists yet, set a plain default voice (short sentences, digits not spelled-out numbers, no jargon) so copy work is not blocked, marked clearly as a placeholder.
2. Collect Kevin's real liked and disliked copy examples, from past brand work or explicit reference material; never invent an example for the exercise.
3. Derive 4-8 traits from the pattern in those examples (for example: "direct, never salesy," "warm but not cutesy").
4. For each trait, write one real liked example and one real disliked example, plus a one-line rule a writer can apply without re-reading the whole sheet.
5. Build a one-page cheat version (traits and rules only) and a longer full reference (with the examples and reasoning) for deeper onboarding.

## Checks
- Every trait's liked and disliked examples are real and sourced, never invented to fit the trait.
- The default voice, once a real sheet exists, is retired, not left stacked alongside it.

## Output
`{voice_and_tone_sheet: {short_version, full_version}}`

## Example
Trait: "confident, not boastful." Liked: "This chain won't tarnish. We tested it." Disliked: "Our chains are the best in the industry, guaranteed to amaze!" Rule: state the fact, skip the superlative.
