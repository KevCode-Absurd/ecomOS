# Writing retrieval: first improvement cycle

Implemented explicit creative routes and a copywriting-principles route. Completed nine new copy packages: three models × no cards / previous retrieval / routed retrieval. Fourteen retrieval regression tests passed. Original visual outputs and library card text were preserved.

## Controlled results

| Model | No cards | Previous retrieval | Routed + principles |
|---|---:|---:|---:|
| gpt-6-luna | 3 | 2 | 2 |
| gpt-6-sol | 4 | 3 | 3 |
| gpt-6-astra | 4 | 3 | 3 |

Scores are 0–4 from one blinded GPT-6 Sol review simulating an agency owner. Copy only; not a live conversion test or real customer satisfaction measure. One sample per condition and same-family reviewer bias limit inference.

G is the first draft I’d hand to a designer and client: it is focused, specific and closely matched to its ad. D is a strong alternative with a particularly effective opening. Both need only routine copy review, not a new approach.

## What changed

The initial review lacked the shared research memo and incorrectly treated a supplied compatibility claim as invented. It is preserved as `review-incomplete-evidence.json`, excluded from the result table, and included in cost accounting. The corrected review receives the same research memo as every writer. Reviewer score changes also show why a single simulated review is not a stable business-outcome measure.

In the corrected review, no-card drafts scored higher than both retrieval conditions for all three models. The new routing improved category relevance and reduced knowledge-context size by 7.5–15.1%, but this run did not demonstrate improved copy quality. Do not roll it out as a proven quality improvement or force retrieval into every writing task.

- Avatar, landing-page, static-ad and writing-principles searches now use explicit category and topic eligibility. General search is unchanged.
- The writing-principles route specifically uses ad-copy material. Retrieved sources include Cashvertising, Copy Hackers and the copywriting course; avatar sources include Competing Against Luck.
- Repeated card IDs are removed across the four searches. Applicability and caveats are retained.
- The revised prompt asks for direct brand voice and keeps internal research qualifications out of customer copy. All three conditions use this same revised prompt, so its effect is not credited to retrieval.

## Cost and context

| Model | Condition | Knowledge tokens | Input / output tokens | Generation USD | Generation seconds |
|---|---|---:|---:|---:|---:|
| gpt-6-luna | none | 0 | 6485 / 5291 | $0.00346 | 52.2 |
| gpt-6-luna | old | 5043 | 11728 / 6151 | $0.00454 | 59.9 |
| gpt-6-luna | routed | 4284 | 10956 / 5162 | $0.00395 | 52.5 |
| gpt-6-sol | none | 0 | 6456 / 5858 | $0.07472 | 72.4 |
| gpt-6-sol | old | 4949 | 11602 / 5350 | $0.08250 | 63.7 |
| gpt-6-sol | routed | 4576 | 11224 / 5394 | $0.08200 | 65.4 |
| gpt-6-astra | none | 0 | 7332 / 7553 | $0.46930 | 160.1 |
| gpt-6-astra | old | 5066 | 12602 / 6338 | $0.47442 | 137.9 |
| gpt-6-astra | routed | 4456 | 11981 / 8555 | $0.57751 | 179.6 |

Additional generation plus copy-review estimate: **$1.93**, plus very small query-embedding charges. Uses the existing capped visual-benchmark ledger; no images were regenerated. Planning/research was reused and is not charged again in this table. Output tokens include reasoning; input pricing is conservative and does not subtract cache discounts.

Cumulative text ledger for the visual benchmark and this improvement cycle: [["settled", 21, 3.355587]]. Earlier image-tool billing remains unexposed and is not treated as zero.

## Remaining problems and next gate

The clearly unrelated security and staff-permissions categories no longer enter these creative packets. This is verified mechanically, not a claim of 90% relevance. The routing still lacks full task constraints: Sol retrieved offer-tier advice despite a fixed-offer brief, and some matches require adaptation to a non-consumable product. Correct category alone does not prove usefulness.

Book-derived cards contain examples from other industries. Those examples illustrate a principle; they are not facts or claims to copy into Peach Bucket marketing. A later context-compaction pass can keep the actionable principle and its conditions while removing irrelevant examples; this cycle did not rewrite the corpus.

We have not passed the proposed 80/20 launch gate. This is one brand and one campaign brief, not the required representative multi-brand task set. Next: add explicit fixed-offer/product/proof constraints to selection and validate on several different briefs before connecting autonomous execution.

## Review details

### gpt-6-luna — routed
The page repeatedly restates fit and supervision cautions, then slips into researcher voice with “The brand advertises” in a customer-facing FAQ.
Before launch: Cut the duplicate cautions and FAQ answers; state the support and guarantees in the brand’s own voice.

### gpt-6-sol — routed
The photo warning—“rather than using the photograph to infer how many of each part are included”—interrupts otherwise practical sales copy.
Before launch: Replace it with a brief pointer to the kit details for quantities, and tighten the repeated fit guidance.

### gpt-6-luna — none
“The brand advertises” recurs in the setup and FAQs, while “Component quantities and fit can vary by use and home setup” is muddled.
Before launch: Use direct brand voice, clarify that quantities should be checked in the listing, and remove one repeated contents rundown.

### gpt-6-astra — none
A few component descriptions feel padded, particularly “A separate lock category for another door your child may begin reaching for.”
Before launch: Tighten those descriptions while keeping the clear pulling-up scenario, offer and matched ad.

### gpt-6-astra — old
Fit and supervision cautions appear in the hero, ad and later answers, making a useful product explanation feel longer than necessary.
Before launch: Keep one concise caveat in the ad and the fuller guidance on the page; shorten the component and FAQ sections.

### gpt-6-astra — routed
The page revisits the same table-to-kitchen checklist in the contents, benefit and setup sections.
Before launch: Combine the overlapping sections so the concrete product descriptions and installation offer stand out.

### gpt-6-sol — none
“We advertise the kit for compatible Indian 5A/15A sockets” sounds like internal marketing commentary rather than copy to a parent.
Before launch: Rephrase the supplied compatibility claim naturally, retaining the instruction to check the fit of each component.

### gpt-6-luna — old
Abstract phrasing such as “everyday touchpoints,” the stilted “Pay prepaid,” and repeated policy explanations weaken the parent-facing pitch.
Before launch: Lead with a specific crawling or pulling-up moment, say “Save ₹299 when you prepay,” and substantially trim the repeated FAQs.

### gpt-6-sol — old
The distinctive dinner-prep scenario is diluted by repeated “our advertised” phrasing and multiple rounds of fit cautions.
Before launch: Keep the page-and-ad scenario, put the offers in direct brand voice, and consolidate the cautions.

## Files

PEACH_BUCKET_WRITING_V2.html: side-by-side final copy, prompts, exact context, source cards, costs and review.
data/peach-visual-benchmark/writing-v2/: frozen packets, runs, protocol hashes, review and CSV metrics.
CREATIVE_RETRIEVAL.md: how to use the routed helper.
