---
name: web-research-budgeted
owner: shared (Propose, Scout, Product, Organic)
version: 1
invoke_when: a run needs verification of a time-sensitive fact or new candidates the bank lacks
inputs: question or break, store tags, ideas already found, token budget (default 8,000 fetched tokens)
outputs: facts with URL and date; candidates with URL and date; budget used
---
# Budgeted web research

## Steps
1. Write the 3 to 6 questions the run needs answered. Verification first, discovery second.
2. Search. Prefer primary sources (platform docs, official help pages, dated studies) over blogs.
3. Fetch only pages that answer a question. Stop at the budget.
4. Record each fact as: claim, URL, date seen, page date if shown. Never merge a web fact into private data without the label "web".
5. For discovery: each candidate as an idea stub (title, signal, expected effect with the source's basis, URL, date). Write to the candidates file.

## Checks
- Every fact has a URL and a date.
- No brand-private data was sent in a query.
- Budget not exceeded; report tokens used.

## Output
{facts[], candidates[], budget_used}
