# SITE wave 4: workflow and skill selection rules

77 capabilities (C01-C80 minus C17, C20, C34, C41, C49, C60, folded into
other agents by the review, plus G01-G03) grouped into 30 workflows and 43
skills (13 parents, 30 sub-skills). Every capability id sits in exactly one
workflow.

## How Site picks a workflow

Site reads the trigger first (cadence, event, approved card), then the
bottleneck tag and card fields (format, channel, platform, store tags), and
matches the row below. Ties break toward the more specific workflow.

| Bottleneck / trigger | Format, channel, platform, tags | Workflow | Key skills |
|---|---|---|---|
| New brand, no store | any platform | W01-W08 in order | store-setup-checklist, theme-engineering, theme-pr-diff |
| Hygiene, uptime, deploy risk | weekly / nightly / deploy | W09 | post-launch-hygiene, reliability-monitoring |
| Repeat purchase, wholesale, returns, stockout | feature request | W10 | feature-build |
| Homepage/PDP layout stale | on demand | W11 | homepage-collection-ux |
| site_speed | monthly, any template | W12 vitals -> W13 assets -> W14 infra -> W15 briefs/regression/peak | speed-audit family |
| New campaign/SKU | channel: paid | W16 | funnel-architecture |
| Before a page build, or ad changed | event | W17 | pre-build-research, message-match-audit, synthetic-validation |
| Hero/PDP first screen weak | format: hero \| pdp | W18 | hero-and-buybox |
| Copy, proof, urgency, price claims | format: body copy | W19 | body-copy-and-proof, pricing-integrity |
| Friction, mobile, accessibility | before launch / quarterly | W20 | mobile-first-qa |
| format: advertorial \| quiz \| sales page | any | W21 / W22 / W23 | long-form-funnel |
| cvr, backlog item approved | card: CRO test | W24 | cro-test-lifecycle family |
| on-site search bottleneck | tag: visual catalogue | W25 | discovery-and-personalization, visual-search |
| PDP drop-off with session data, offer underperforming | on demand | W26 | personalization-rules, computed-in-code-offers |
| Reviews/UGC strategy | on demand | W27 | reviews-ugc-strategy |
| tags: india, cod_heavy | rto/trust bottleneck | W28 | india-ops, whatsapp-buy-flow |
| founder approves assistant | G01 | W29 | ai-shopping-assistant |
| tag: india, 60 days pre-festival | G02 | W30 | festive-gifting-ops |
| brand has a mobile app, release due | G03 | W07 | platform-integrations |

## How a workflow picks a sub-skill

Each step's skill follows the catalogue's own switches: **format** (hero,
PDP, advertorial, quiz, sales page), **metric** (CLS/LCP/INP), **asset
type** (image/font/code), **layer** (scripts/caching/headless), **stage**
(design/launch/read/rollout/holdout), **decision** (image order vs
discount ceiling), and **platform** (Shopify vs WooCommerce vs custom repo
changes the tool, not the skill). A one-off judgment call with no reusable
procedure, like scoring a platform TCO comparison, carries `skill: null`.

## When no workflow matches

If a trigger or card names a bottleneck, format or tag with no row above
and no close relative, Site does not improvise. It drafts a workflow
proposal in this file's own schema (id, capabilities, trigger, steps,
outputs, qa), names the closest existing workflow it deviates from and
why, and routes it to a person before any artefact ships. The same applies
when a capability's autonomy is `founder_gate` and the matching step has no
`ask_founder_if` for the gap found: Site stops and asks.

## Notes on the grouping

Wave 2's new capabilities join existing families instead of standing
alone: engineering discipline (git/CI, staging, tokens, integrations,
automation, release tracking, regression, uptime) joins store-setup and
reliability; the four "no tool sells this yet" capabilities (image
sequencing, discount ceilings, visual search, competitor price watch) join
CRO's discovery family, since all four compute a decision in code from
real data, never a guess. C13, C63, C68, C71 and G03 share W07: one
discipline, govern what's installed, automate small rules, watch for
change, at different points of the stack.

Six wave-1 capabilities (C17, C20, C34, C41, C49, C60) do not appear here:
the review reassigned tracking to Money and ops, routing to a cross-cutting
behavior, compliance QA to the shared QA Gate, offer design to Lifecycle,
backlog scoring to Propose, and structured data to Organic. Site still
performs the underlying actions as skills inside its own workflows; it no
longer owns them as capabilities.
