# CREA wave 4: selection rules and notes

## How CREA picks a workflow

CREA matches the card on bottleneck/card type first, then format, channel,
platform and store tags. First match wins.

| Bottleneck / card type | Format / channel / platform / store tag | Workflow | Key skills used |
|---|---|---|---|
| approved idea, new creative test | any format not yet fixed | CREA-W01 | research/objection-and-format-scan, angle-and-test/*, make-creatives/*, write-copy/*, compliance/copy-craft-rules |
| approved idea | format=video, source=founder/authority | CREA-W02 | make-creatives/founder-video, write-copy/scripts |
| approved idea, needs a real creator | format=video, source=ugc | CREA-W03 | make-creatives/ugc-video, special-formats/organic-ugc-scout |
| approved idea, needs real photography | any format needing a real shoot | CREA-W04 | briefing/shoot-and-photo-direction |
| founder request, "draft from this page" | product-page URL given | CREA-W05 | special-formats/product-page-to-ad, make-creatives/static, write-copy/headlines |
| card tagged for a new market or device | store_tag=india_mobile / non-US | CREA-W06 | briefing/localisation-spec, derivatives/resize-for-placement |
| weekly trigger, declining live ad | any | CREA-W07 | fatigue-and-teardown/fatigue-diagnosis |
| weekly trigger, general review | any | CREA-W08 | fatigue-and-teardown/winner-teardown |
| monthly trigger | any | CREA-W09 | production-ops/pipeline-planning |
| weekly trigger, cost | any | CREA-W10 | production-ops/cost-tracking |
| monthly trigger, spec drift | any | CREA-W11 | production-ops/naming-and-tagging |
| new AI tool or continuous check | any | CREA-W12 | compliance/ai-use-governance |
| card needs price copy | any | CREA-W13 | pricing-and-naming/price-framing |
| card needs a product/system name | any | CREA-W14 | pricing-and-naming/product-naming |
| on demand, objection refresh | any | CREA-W15 | special-formats/objection-retargeting-copy |
| store_tag=cod_heavy / india | any | CREA-W16 | special-formats/cod-prepaid-rto-messaging |
| any | channel=marketplace, platform=amazon/flipkart/myntra | CREA-W17 | special-formats/marketplace-modules |
| card needs a recurring character | any | CREA-W18 | special-formats/mascot-sheet |
| founder approved, no shoot | format=video, source=ai_actor | CREA-W19 | special-formats/ai-actor-ugc |
| consent on file | voice variants needed | CREA-W20 | special-formats/voice-clone-variants |
| event: before paid test | any | CREA-W21 | production-ops/predictive-scoring |
| event: master approved | any | CREA-W22 | derivatives/* |
| event: before ship, licensed assets used | any | CREA-W23 | compliance/rights-clearance |
| event: new catalogue / feed refresh | channel=dpa/catalogue | CREA-W24 | make-creatives/catalogue-dpa |
| event: batch approved for launch | any | CREA-W25 | production-ops/bulk-upload-sheet, production-ops/draft-upload-browser-agent |

## How CREA picks a sub-skill inside a workflow

Once a workflow runs, `make-creatives` and `write-copy` route on the task's
own fields, matched against each child's `select_by`: `format` (static,
video, catalogue, carousel), `source` (brand, ugc, founder, ai_actor) and
`copy_type` (primary_text, headline, hook, script). A video task resolves
two switches at once, format and source, since a video could be UGC,
founder-led or synthetic, never on format alone. Every other skill matches
on its own single `task` or `channel` key.

## When nothing matches

If no row fits, CREA does not improvise. It states the card's bottleneck,
format and channel, names the nearest workflow and why it does not fit, and
drafts a one-page workflow proposal (job, trigger, inputs, steps, output)
for a person to review before anything runs under it. The same rule covers
a task with no matching sub-skill: it stops one level up, in the parent
skill (`make-creatives` or `write-copy`), rather than forcing a near match.

## Notes

CREA's original capability list (`CREA.md`, 54 ids) and its current list
(`CREA.caps2.txt`, 39 ids) differ: a MECE review moved 16 capabilities
elsewhere. VOC mining and personas went to the Brand Brain Keeper;
offer-building, test design, channel routing, competitor-research
ownership and creator whitelisting went to MEDIA; page, marketplace, SMS
and lifecycle copy ownership, plus the claim-check and copy-QA gates,
went to Site, Lifecycle and the QA Gate; the holiday and sale-event
calendar (US holiday calendar first, India festive calendar as the market
option) went to ORG.
CREA-W01 still runs the equivalent research and compliance steps, but as
a consumer of another agent's record (the objection map, the claim-tier
check), not its owner. Every handoff (audience spec to MEDIA, page copy
to Site, email or SMS copy to Lifecycle) says so in the step, and CREA
never builds that destination itself. CREA-G01 (shoot production and
model releases) is new here, filling a gap between photo direction and
an actual booked shoot.
