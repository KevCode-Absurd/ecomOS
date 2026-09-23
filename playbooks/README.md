# Ecommerce playbooks

Start with [the domain catalog](v1/INDEX.md) and [operating contract](OPERATING_CONTRACT.md).

**Current ad-copy selection:** keep [version 1.2](ad-copy-v1.2/README.md) as the strongest tested candidate. Two further revisions added plain-language and credible before/product/after checks, then corrected task focus; neither beat v1.2 overall. See the [two-round decision](../AD_COPY_ITERATION_DECISION.md), [final comparison](../AD_COPY_TASK_FIRST_COMPARISON.html), and experimental [v1.3](ad-copy-v1.3/README.md) / [v1.4](ad-copy-v1.4/README.md). Reviewer re-rating varied substantially; scores are editorial signals, not conversion evidence. Load v1.2 explicitly using `--directory playbooks/ad-copy-v1.2`; no default route or other playbook was silently replaced.

**Ad-copy editorial update:** [version 1.1](ad-copy-v1.1/README.md) is a focused synthesis of ten reviewed source cards, with eight conditional principles and three revised workflows. Other domains remain v1 drafts. Load it explicitly with `python scripts/read_playbook.py --directory playbooks/ad-copy-v1.1 --workflow ad-copy-deployment.write-static-copy`. Its [system prompt](ad-copy-v1.1/SYSTEM_PROMPT.md) is included in the packet. It has not yet passed owner or generation testing; [six brief walkthroughs](ad-copy-v1.1/BRIEF_CHECKS.md) document expected behaviour.

The source cards remain in `data/library-v3/cards.json`. This independent layer contains 23 domain drafts, three task workflows per domain, and a mixed-source routing guide. Each domain provides JSON for software and Markdown for humans. `card-index.json` preserves its complete card inventory; supporting cards are locally selected candidates with original steps and conditions.

**Original v1 scaffold status: draft.** That first build is workflow scaffolding with traceable source candidates, not a completed semantic synthesis or a validated agent integration; it used no paid model calls. The separate ad-copy experiments above did use paid APIs. Existing default retrieval and routing remain unchanged.

## Use

From the project root, run `python scripts/read_playbook.py --list` to list workflows. Run `python scripts/read_playbook.py --workflow ad-copy-deployment.write-static-copy` to return that workflow and its evidence candidates. It does not generate copy or call an external service. Add `--with-foundations` only when those extra candidates are useful. Add `--card-id ID` (repeatable) to include only explicitly selected workflow candidates. Returned evidence still requires applicability checking.

## Versioning

Build a new version with `python scripts/build_playbooks.py --output playbooks/v2-draft`; the builder refuses to overwrite an existing directory. The generator uses current source cards and authored specifications in `domain_specs.py`; it does not carry manual changes from prior generated versions. Curated revisions therefore need an explicit reviewed change to the specification/generator or a separate versioned editorial workflow, not an unattended regeneration.

Use `feedback-template.json` to record feedback. Neither feedback submission nor a low rating triggers automatic updates. Follow the operating contract to route changes, test them and promote a version. `v1` stays a draft until owner review and output tests establish otherwise.

## Next editorial work

1. Review ad-copy candidate support for relevance and merge overlapping principles into a compact edited workflow.
2. Test generic prompt versus playbook versus playbook plus selected cards using the same brand facts/model/brief.
3. Let the owner judge actual usefulness; use automated checks only for facts, constraints and completeness.
4. Repeat the editorial cycle for other high-use workflows. Do not promote all 69 workflows because one performs well.
