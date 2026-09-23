# Active workflow: practical ecommerce intelligence

This replaces the legacy V1/V2 per-claim approval workflow. The user's September 22 instruction authorizes text-only processing of the complete library, CRO first, then product research and the other folders in numbered order. Ignore images. Overall ceiling: USD 200 including prior usage; the shared ledger retains its more conservative USD 160 working stop. No per-folder spending approval is required within this scope. Provider errors and unknown outcomes retain reservations.

## Cards

Clean text locally; keep coherent paragraphs together in larger sections. Generate task-sized cards with title, search summary, use_when, steps, caveats and specific tags. Attach private source/version identifiers automatically. Preserve distinctive examples and useful qualifications, without exact-quote mapping or a second review pass on every card. CRO source sections include relevant prior extracted notes to reuse previous work. Known disputed old claims are not used as hints.

Run `python scripts/build_library.py` to prepare the ordered manifest and rebuild local exports. Run `python scripts/build_library.py --execute --folder 09` for CRO, `--folder 01` for product research, or omit the folder to continue all incomplete sections sequentially. Calls use DeepSeek Flash with thinking disabled for this structured transformation after the initial low-reasoning trial wasted output on reasoning and truncated two responses. This does not restrict runtime agents. Results are cached and resumable; failures stop dispatch for inspection. Source changes change job identities; exports include only the current manifest, removing obsolete versions from active search. Each completed folder refreshes the semantic index.

Outputs in ignored `data/library-v3/`: cards.json, markdown per folder, search.sqlite, manifest.json and progress.json. No source data or credentials belong in Git.

### Ecommerce applicability

Every retained card must support a concrete merchant task; an ecommerce tag alone is insufficient. Preserve transferable frameworks from broad business books, but translate implementation into product selection, merchandising, offers, PDPs, checkout, acquisition, subscriptions, fulfillment or another store operation. Omit service-only sales calls, agency onboarding and coaching procedures that do not transfer. Label adapted examples as applications rather than source-proven ecommerce results.

`scripts/focus_ecommerce.py --folder 03` reuses previously extracted Offers cards for this adaptation. Its `--broad-sources` option uses OpenAI selectively for the two general business books whose first adaptation still retained service-business examples. Original extracted results remain under ignored `before-ecommerce-focus/`. This is targeted adaptation, not mandatory re-review of every future ecommerce-native source. The extraction prompt now carries the same ecommerce requirement for subsequent folders.

For the user's requested CRO cleanup, `scripts/focus_ecommerce.py --folder 09 --cro` applies the stronger merchant-focused pass to all existing CRO sections. Service sales calls, agency lead magnets, proposal followups and high-close-rate heuristics are removed rather than renamed. Transferable proof, CTA and objection-handling principles are applied to product pages, carts, checkout or store signup journeys. Analytics and experimentation cards retain their technical substance and are scoped to store outcomes. Scope version 3 records completion; refreshing exports and embeddings removes superseded cards from active retrieval while preserving private backups.

## Agent use

1. Identify the requested outcome, known brand facts and necessary subquestions. Simple questions need one search; a strategy may need searches across research, offer, creative and conversion.
2. Retrieve concise candidates, then include complete relevant cards within an explicit knowledge token budget. Keep room for brand data, tool results and the answer. Missing brand facts remain unknown; do not invent them.

   For a known domain, pass `--domain brand` (or the relevant stored domain) to search within it. Leave the domain unset for cross-domain tasks. Brand retrieval checks exposed ambiguity between premium positioning and promotional premiums; scoping prevents that mismatch without changing or deleting useful offer cards.

   For platform-specific implementation, also pass `--platform shopify` or `--platform woocommerce`. This filters by the card's platform tag, preventing similar setup terminology from mixing the two systems. Leave it unset for platform comparisons or broader strategy.
3. Combine curated advice with the brand's metrics, constraints and current external information. Search the web when current platform settings, market facts or knowledge gaps warrant it. The library does not replace current factual verification.
4. Distinguish source examples from brand-specific recommendations. Explain conflicting advice through applicability; request a missing critical fact when needed.
5. Use any suitable execution model, including frontier models. Evaluate the same model with and without cards, keeping task and brand inputs fixed. Also measure lower-cost model options separately.

## Quality and cost

Validate structure locally; inspect varied samples and flagged outputs. Evaluate retrieval relevance and answer specificity, not exact quote coverage. Coverage is a practical target, not a claimed measured 80% recall. No model training is needed to add knowledge. Card indexing is not a live execution integration or a hosted platform.

Hybrid search combines SQLite keyword search and OpenAI embedding similarity using reciprocal-rank fusion. `scripts/search_library.py` counts actual o200k_base tokens, defaults to 2,000 knowledge tokens for a focused task and 4,000 for a broad one, and includes complete cards only. The caller should pass the appropriate tokenizer/budget for other execution models. Broad requests can issue multiple targeted searches; automatic task decomposition is not yet a standalone agent service. The core keyword function has a conservative byte-count fallback.

Three same-model comparisons ran on CRO with GPT-5.6 Terra: low-volume testing, mobile checkout, and popup incrementality. These are smoke checks, not proof of superiority. The first low-volume answer over-applied a source's monthly-order heuristics; sampled cards were clarified to require actual sample-size planning. Raw paid responses remain cached; corrected cards live in the result exports. Semantic matches may include related but unnecessary advice, so the executing agent must select what applies.
