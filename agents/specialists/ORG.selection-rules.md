# ORG wave 4: selection rules and notes

## How ORG picks a workflow

ORG reads the trigger first (cadence, approved card, or event), then matches bottleneck, format, channel, platform and store tag against the table below, in row order; first full match wins. A page-type card routes through `org/seo-page`; a format card through `org/make-content`; a channel task through `org/channel-ops`: none hold drafting logic of their own, only routing.

| bottleneck / card type | format / channel / platform / tag | Workflow | Key skills |
|---|---|---|---|
| new brand, platform under review | any | ORG-W01 | organic-channel-strategy |
| monthly calendar, script or shoot needed | video, carousel, long-form, pin, newsletter | ORG-W02 | make-content/* |
| idea bank low, or a post outperforms | any | ORG-W03 | format-design |
| daily comment/DM queue | comments, DMs | ORG-W04 | community-response-drafting |
| lead-capture funnel needed | comment-to-DM | ORG-W05 | funnel-design |
| new verified reviews/photos | UGC | ORG-W06 | ugc-repurposing |
| event: post scheduled | any | ORG-W07 | destination-qa |
| weekly library review | any | ORG-W08 | content-lifecycle |
| creator supply low/discovery due | Instagram, YouTube, Pinterest | ORG-W09 | creator-seeding-and-discovery |
| monthly organic report | any | ORG-W10 | organic-performance-read |
| trend/sentiment check | social, review, forum | ORG-W11 | social-listening-digest |
| Pinterest content or board review | pin, board (pinterest_active) | ORG-W12 | make-content/pinterest-pin |
| founder LinkedIn cadence, hiring event | LinkedIn, employer-brand (b2b_or_hiring) | ORG-W13 | founder-and-employer-brand-writing |
| monthly, or feedback spike | comments, DMs, reviews | ORG-W14 | community-feedback-mining |
| upload, podcast/newsletter cadence | YouTube, podcast, newsletter (owns_channel) | ORG-W15 | channel-ops/* |
| new long-form recording | podcast, talk, livestream | ORG-W16 | video-repurposing-pipeline |
| founder asks SEO/AEO priority | any | ORG-W17 | seo-aeo-roadmap |
| monthly, before a page is written | any | ORG-W18 | page-brief-build |
| quarterly technical review | any | ORG-W19 | technical-crawl-audit |
| page_type: product or collection | product, collection | ORG-W20 | seo-page/* |
| money page missing schema | any | ORG-W21 | schema-implementation |
| page_type: guide or blog | guide, blog, comparison | ORG-W22 | seo-page/* |
| revenue-at-risk page decay | any | ORG-W23 | content-refresh-audit |
| monthly link-graph review | any | ORG-W24 | internal-linking |
| monthly PR/outreach cycle | any | ORG-W25 | digital-pr-outreach |
| weekly, physical location | GBP, reviews (has_physical_location) | ORG-W26 | local-seo-and-reviews |
| monthly SEO report | any | ORG-W27 | seo-reporting-and-diagnosis |
| a vendor pitch arrives | any | ORG-W28 | vendor-vetting |
| monthly probe, or wrong fact found | AI answer engines | ORG-W29 | ai-visibility-probe, fact-consistency-management |
| weekly agentic audit | agentic shopping surfaces (sells_via_agentic_storefront) | ORG-W30 | agentic-shopping-audit |

## Sub-skill selection inside a workflow

`make-content` matches one child by `format`/`platform` (short-video, carousel, youtube-long, pinterest-pin, newsletter). `seo-page` matches one child by `page_type` (collection, product, guide, blog); `guide` splits again on `subtype` (buying_guide vs comparison). `channel-ops` matches by named channel (youtube, or the merged audio-and-newsletter path). No task reaches two children.

## When no workflow matches

ORG never improvises silently. It checks the capability index for a match under an unfamiliar name; if none fits, it drafts a proposal in this file's shape (trigger, inputs, steps, output, QA), naming skills it would reuse or need, and sends it to a person. Nothing runs until approved once.

## Hand-offs, not scope creep

Paid amplification goes to Media. A site-speed fix found during a technical audit goes to Site with a developer brief, never fixed here. A naming or positioning question surfaces as a flag inside the roadmap workflow (ORG-W17) for Brand strategist, not a call ORG makes. CRO test design on a page ORG just optimized goes to Site.

## Build notes

30 workflows cover all 43 capability ids from `ORG.caps2.txt`, including `LOOP-C38`, none left out or double-owned. 43 skills, including three parents (`make-content`: 5 children, `seo-page`: 4, `channel-ops`: 2), stay inside the 20-45 range. Four flagship, multi-capability workflows match the founder's media-buying depth: the monthly calendar (W02), keyword-to-brief (W18), crawl-to-developer-brief (W19), and probe-to-facts-to-correction (W29).
