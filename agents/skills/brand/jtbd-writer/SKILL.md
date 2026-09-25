---
name: jtbd-writer
owner: BRAND
version: 1
invoke_when: a new avatar candidate needs its job statement and forces written
inputs: cross-verified research patterns, quote sets
outputs: job statement, 4-forces record
---
# Job-to-be-done writer

## Purpose
An avatar defined as a job, not a demographic, is what makes the record useful for copy and product decisions later. This skill turns research patterns into a job statement that passes real tests, not a description that sounds insightful but cannot be used.

## Steps
1. Write the job in the form: "When [situation], I want to [motivation], so I can [outcome]." The situation must be specific and observable, not a mood.
2. Cover all three sides: functional (what gets done), emotional (how they want to feel), social (how they want to be seen).
3. Run the verb-noun test: the job should read as a verb-noun action a person can picture doing, not a trait.
4. Run the cross-category test: the same job should plausibly exist even if this exact product category did not, proving it is a real job and not a repackaged product description.
5. Name the 4 forces driving the switch: the push (the problem getting worse), the pull (the attraction to a new solution), the anxiety (what could go wrong with switching), and the habit (the pull of staying put). Each needs at least one verbatim supporting quote.

## Checks
- Statement passes both the verb-noun and cross-category tests.
- Every force cites a real quote, not an inferred feeling.
- No demographic detail (age, income) is substituted for the actual job.

## Output
`{job_statement, forces_record: {push, pull, anxiety, habit}}`

## Example
"When my sister's wedding date is set and I have 6 weeks to find jewellery that photographs well but doesn't look rented, I want a piece I can wear again after, so I don't feel like I overspent on a one-time costume." Push: rental pieces look fake in photos (quoted). Pull: seeing a real friend's photos in a piece like this (quoted).
