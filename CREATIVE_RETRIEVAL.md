# Creative retrieval

The creative workflow now has explicit routes for writing principles, avatar research, landing pages and static ads. General knowledge search is unchanged; other business tasks can still search the whole library.

Use `intelligence.creative_retrieval.retrieve_campaign(engine, queries)`, where `queries` contains `avatar`, `landing_page` and `static_ad` strings. The helper adds a writing-principles search restricted to the ad-copy library, selects up to four cards per route, and excludes card IDs already returned by an earlier route. It preserves applicability and caveats in the compact context.

The result is an internal audit packet with queries, eligible counts, compact context and original cards. Pass only each result's `context` and its `purpose` to the writing model; retain the full audit server-side. Do not send both the compact context and full cards to the model.

The current route filter uses domain plus title/tags, with explicit exclusions for unrelated operational and security subjects. It is a relevance improvement, not a learned relevance judge. It can still admit a method that is in the right category but unsuitable for the brand or task, such as offer tiers when the offer must stay fixed. Do not treat route membership as verification or confidence.

The first controlled comparison is saved under `data/peach-visual-benchmark/writing-v2`. It holds the revised writing prompt, task, facts and model-specific plan fixed while comparing no cards, previous retrieval and routed retrieval. It does not regenerate images or publish assets.

Next gate: add task constraints (fixed offer, available proof, product type) to relevance selection, then validate on additional briefs. Do not globally remove useful offer-design cards merely because they are irrelevant to one fixed-offer campaign.
