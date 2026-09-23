# CRO intelligence-layer checkpoint

22 September 2026. First extraction and initial review are complete for the seven CRO documents. Quality repair remains incomplete. All workers from this run have stopped. No cards have been published, no live business actions were taken, and nothing from this workspace has been pushed to GitHub.

## What is complete

- Seven documents, **96,125 source tokens** measured with o200k_base, processed through all **52 initial batches**.
- **943 first-pass candidate units** with source-version references. The exact-evidence validation also held 20 units separately; failed outputs remain preserved.
- Every first-pass candidate has an initial review verdict: **705 source-supported, 236 revise, 2 unsupported**. These are model-review findings about the supplied text, not an accuracy score or independent verification of truth, freshness or authorship.
- Repair requests attempted for **52 batches**. **32 repaired batches rechecked; 20 remain to be rechecked.** Some repair/review outputs are still held.
- **1,088 working revision candidates**, kept separately from the first pass. Revision counts are not directly comparable to first-pass verdict counts because additions and replacements create new versions.
- **56 tests pass**; Python compilation checks pass.

## Budget

The approved combined CRO ceiling remains **$10**. The overall $160 working/$200 absolute project ceilings are unchanged.

| Provider | Recorded usage estimate | Retained unknown-outcome reservation |
|---|---:|---:|
| DeepSeek | $3.1064 | $0.1758 |
| OpenAI | $6.0996 | $0.4617 |
| Total | $9.2060 | $0.6375 |

**Committed: $9.8435; headroom: $0.1565.** Five uncertain request outcomes retain their reservations. Separate cross-provider fallbacks did not release or resend those original requests. Figures use conservative configured rates; provider invoices remain authoritative. Earlier calibration spend is separate.

The ledger blocked a recheck when its full worst-case reservation did not fit. As other calls settled, serial checks used some released headroom. No paid worker remains running. The next expanded-context review requires more reservation headroom than remains.

## Quality findings that change the implementation

1. **Context boundaries matter.** Many notes about missing continuations refer to text already present in adjacent batches. Prepared 52 expanded context packets locally, preserving paragraph offsets and identifying the primary target span. Context-aware repair/review paths are implemented but have not been run through paid models yet.
2. **Editorial notes need separate treatment.** A structural audit flagged 80 revised cards with claim/action evidence only in apparent routing or editorial blocks. These are heuristic flags, not proven provenance labels. Seek body evidence before promoting them as practitioner instructions; preserve the notes as metadata.
3. **Some visual context is genuinely unresolved.** One transcript recommends a bolded subset for smaller stores. The DOCX has no embedded images, and its only explicitly enabled bold run is a section heading. Inherited styles were not exhaustively resolved. The subset must remain unresolved until its original visual context is recovered.
4. **Semantic review is essential.** Reviews caught a win-rate statement promoted into a universal requirement, missing confidence/power assumptions, omitted commercial affiliations, circular exclusions and broken dependencies. Repair output alone is not approval.
5. **Compactness must preserve qualifications.** Deduplicated source/evidence records reduced serialized card tokens from **779,845 to 622,994 (20.11%)** across 1,088 working cards. Conditions, unknowns, evidence, source limitations and review flags remain. This is a serialization measurement, not a retrieval, answer-quality or billing benchmark.

## Infrastructure changes

- Per-request durable reservations against both folder and overall ledgers, cached completed results, no automatic retry of unknown outcomes.
- A tested subprocess watchdog covering blocked Windows stdin as well as stalled HTTP. A real deliberately blocked local child process is terminated by the test.
- Multi-paragraph exact evidence binding; original API responses and earlier review/repair versions are retained.
- Response-local relationships resolved into stable IDs; short review aliases decoded locally, with unknown IDs rejected.
- Explicit cached-only repair recovery. One response with direct unit objects was wrapped into the requested repair envelope locally, with an audit record and no text changes or new API call.
- Review-aware revision index, remaining-work records, editorial-evidence audit and compact capsules. These remain separate from the legacy approved-card store and production retrieval.

## Remaining work

- Finish the **20 pending rechecks** and fix **2 review-validation issues**.
- Resolve **73 candidate-level semantic correction tasks**, **24 omission records**, and **5 batch-level evidence/structure issues** currently recorded. These are different task types and are not additive counts of unique cards. Further reviews may reveal more.
- Triage **51 batch-level unresolved-context notes**. Many can be addressed with local neighboring text; others are source limitations that should remain explicit, not guessed away.
- Verify editorial-only evidence against source bodies; retrieve the missing visual context where necessary.
- Perform cross-document semantic deduplication/conflict review and brand-scenario retrieval tests. A differentiated agent-quality benefit has not yet been demonstrated for this folder.

No complete batch currently passes every conservative next-evaluation gate, and no working card is production-approved. This does not mean every individual claim is unusable; it means remaining batch-level context, coverage or review issues have not been cleared.

## Cost trade-off before scaling

Repeating this developmental workflow unchanged across the library would not fit the original $160–$200 target. A naive source-token-ratio extrapolation of recorded CRO usage alone is about **$453**, before remaining quality work. That is not a production forecast: this run included calibration, retries after confirmed failures, schema repair and avoidable rework from missing surrounding context.

Before another folder, validate context-aware extraction, metadata/body separation and more economical review routing against quality cases. Do not promise whole-library completion within the target until that revised workflow has a measured estimate. Existing global budget guards prevent silently overrunning it.

## Proposed next bounded pass

Raise the CRO ceiling from **$10 to $15 total** only with the owner's approval. Prioritize context-aware fixes, body-evidence checks and pending review completion; retain all existing reservations. The additional $5 is a new checkpoint allowance, not a guarantee that every source ambiguity can be resolved. No additional API keys, hosting or account setup is needed for that pass.

A concrete reviewed example is saved privately at `data/cro-folder-v1/card-example.md`. Machine-readable state is in `quality-report.json`, `revision-index.json`, `remaining-work.json`, `context-packets.json`, `editorial-evidence-audit.json` and `compaction-report.json` under the same ignored folder.
