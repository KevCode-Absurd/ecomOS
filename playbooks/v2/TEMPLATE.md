# Playbook v2: format and rules

Playbooks v2 are the knowledge an execution agent runs from. They are built in 2 passes per folder.

- Pass 1: one mini playbook per source document, written from the full source text plus its cards. One agent run per source, so each read is focused and any file can be redone alone.
- Pass 2: one folder playbook that merges all mini playbooks into a single, detailed, actionable document.

Cards in `data/library-v3/cards.json` stay unchanged. Playbooks cite card ids so an agent can look up the original.

## Writing rules

- Plain English. Short sentences. Digits for numbers. No em dashes. No hype words.
- Every rule states its condition: when it applies, when it does not.
- Keep the source's numbers, thresholds and examples. Mark a case result as an example, never as a promise.
- Keep the source's disagreements. Do not average two sources into a rule neither of them stated.
- Never turn one presenter's opinion into a universal law. Say "Source X says" when only one source says it.
- Platform steps that can change carry the tag `[verify UI]`.
- Anything that depends on a brand's own data carries the tag `[needs brand data: what]`.
- Anything that should be checked live on the web carries the tag `[web check: what]`.
- Cite card ids in square brackets like `[a1b2c3d4e5f6]` (first 12 characters are enough).
- Do not invent steps the source did not give. If the source is thin on how, say so.
- No length cap. Detail wins. But no padding: each sentence must carry a rule, a number, a step, a check or a caveat.

## Pass 1: mini playbook per source

File: `playbooks/v2/<folder>/sources/<NN>-<short-slug>.md`

```
# <Source title>

source_id: <id>  |  folder: <folder>  |  cards: <n>  |  words: <n>  |  type: book / course / talk / article / transcript
credibility: who the author is, what they sell, what their evidence is (own results, client data, studies, opinion)
date signals: year mentioned, platform versions named, anything that dates the advice

## 1. What this source is for
2 to 5 lines. The job it helps an operator do.

## 2. Principles
Numbered. Each: the principle, the condition, the evidence the source gives, card ids.

## 3. Procedures
Step-by-step sequences the source gives. Numbered steps. Settings, names, order. `[verify UI]` where needed.

## 4. Rules, thresholds and numbers
A table: rule | number or threshold | condition | source's basis | card id.

## 5. Diagnostics and checks
What to check, how to check it, what good and bad look like, what to do next.

## 6. Tools, settings and named features
Tools named, what they are used for, `[verify UI]`.

## 7. Examples and case results
Brief. Marked as examples. Include the numbers the source gave.

## 8. Mistakes the source warns about

## 9. Caveats, conflicts and what is missing
Where the source hedges, contradicts itself or other sources, or skips the how.

## 10. Card index
All card ids from this source, one line each: id, title.
```

## Pass 2: folder playbook

File: `playbooks/v2/<folder>/PLAYBOOK.md`

```
# <Folder name> playbook

version: 2.0-draft  |  date  |  sources: <n>  |  cards: <n>  |  built from: sources/*.md

## 0. How to use this playbook
Which agent runs it. Which sections to load for which task. What the agent must fetch from brand data, the data layer, and the web before acting.

## 1. Scope and outcomes
What this domain covers, what it does not (point to the neighbour folder), and the business measures it moves.

## 2. Inputs the agent needs
Table: input | from where (brand record, data layer, inspiration, web, user) | required or optional | why.

## 3. Decision rules
Numbered, grouped by sub-topic. Each rule: the rule, the condition, the sources that support it (by mini playbook number), conflicts if any, card ids. This is the longest section.

## 4. Procedures (implementation)
Step-by-step, grouped by task. Each procedure: goal, preconditions, steps with settings, checks after each step, rollback, `[verify UI]` tags.

## 5. Diagnostic checklists
Per sub-topic: what to check | how | good | bad | fix | source. Written so a worker can run it.

## 6. Thresholds and benchmarks
One table for the whole folder. Value, condition, source, confidence (how many sources agree).

## 7. Where sources disagree
Each conflict: what each side says, when each is right, what the agent should do.

## 8. Common mistakes
Merged from all sources, deduplicated, with the fix.

## 9. Deliverables
What the agent produces for each task in this domain, and the format.

## 10. What needs live data or a web check
Everything tagged `[needs brand data]` or `[web check]`, grouped.

## 11. Freshness and stale-risk notes
Which rules depend on platform UI or pricing and should be re-verified, and how often.

## 12. Source index
Each mini playbook: number, title, type, credibility, what it contributed most. Then the neighbour folders and what lives there.
```

## Layering after pass 2

The folder playbook is the base layer and stays traceable to the sources. Additions go on top as separate files, never edited into the base:

- `playbooks/v2/<folder>/overlays/<agent-or-task>.md`: extra rules, checklists or procedures one agent needs.
- `brands/<brand>/overlays/<folder>.md`: one brand's exceptions and preferences for this domain.
- New sources: add a new mini playbook under `sources/`, then re-run the pass 2 merge. The merge is repeatable.

## Quality bar for pass 2

- Every decision rule traces to at least 1 mini playbook and card id.
- No rule appears twice. Near-duplicates are merged, and the merged rule keeps the strictest condition.
- Conflicts are kept in section 7, not silently resolved.
- A reader who has never seen the sources could run the procedures.
- The playbook names what it cannot know without brand data or the live web.
