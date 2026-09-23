# Ad Copy Deployment — draft playbook

**Status:** source-linked draft; not owner-approved or outcome-tested.

Read [the operating contract](../OPERATING_CONTRACT.md) before using a workflow.

## Inputs
- Product facts
- audience evidence
- offer
- approved proof
- visual concept
- voice
- constraints

## Measures
- Owner preference
- editing needed
- claim accuracy
- later CPA

## Foundation candidates
Inferred principle labels do not establish universal applicability. Retain source conditions; empty means no matched labelled principle, not absence of foundational knowledge.

- **Rewrite Vague Claims with Short Words and Concrete Promises** (`581f8a1a98cd0852ea29eed6`): Trade formal abstraction for specific, benefit-led phrasing that the reader can see and believe.
  Applies when: Editing benefit claims, headlines, and PDP bullets to make them more concrete and persuasive.
  Condition: The source's specific example headlines are stylistic demonstrations, not tested winners.
  Condition: Don't swing to the other extreme of three-word sentences for every line; keep variety.

- **The Psychology of Simplicity: Readable Copy Is Non-Negotiable** (`17183d94160ce2f95770a9d7`): Advertising exists to get people to act, so it must be written to be understood - simple, direct, and readable.
  Applies when: Final QA on ad copy, PDP text, email, and any customer-facing copy before it ships.
  Condition: The source argues this is the foundation for everything else in the book - skip it and other techniques won't rescue the ad.
  Condition: Clarity work is not just correct grammar; wordy but grammatically perfect copy can still fail the test.

- **Direct Mental Movies With Specific Visual Words** (`8998cd84ed0c5d71e3f42fc3`): Replace vague benefit claims with specific visual language that makes prospects mentally simulate using the product.
  Applies when: Writing product descriptions, ad body copy, landing page sections or video scripts where a generic benefit statement is falling flat.
  Condition: Whitman's claim that imagery increases desire is a persuasion principle, not a measured conversion lift—test copy variants against your own baseline.
  Condition: Overwriting dense imagery can hurt readability; the source also recommends clear readability formulas and simplicity.

## Write ecommerce static-ad copy
Workflow ID: `ad-copy-deployment.write-static-copy`

**Deliverable:** Primary text, headline and CTA for each concept

### Proposed decision sequence
1. Choose one customer situation, promise and relevant objection
2. Use product evidence to support the promise and complement the visual
3. Write distinct finished variants and remove unsupported claims and filler

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Lead With 'What's In It For Me?' Benefits
Card: `40638b840ce1e28ea89b4b19` · Source: Cashvertising.docx · Section: 1

Consumers care about what the product does for them, not company facts, equipment or process.

Applies when: Reviewing product pages, about sections, ad copy or brochures that currently describe the company, factory or product specs.

- Audit each asset for self-serving content: company history, staff counts, square footage, equipment photos, 'unusual camera angles'. The source cites Daniel Starch's research showing readers ignore factory-focused ads.
- For each feature listed, write the corresponding consumer benefit and lead with the benefit.
- Put the single biggest benefit in the headline.
- Batch benefits throughout ('Bombard Your Readers With Benefits') rather than relying on one strong claim.
- Use the Flesch readability ease concept and clear layout so benefit statements land fast.
- **Condition:** This is the book's core 'advertising should move people to act' doctrine—it is a direct-response stance, not a brand-awareness stance; brand campaigns may weight emotion and imagery differently.

#### Abstract-to-Concrete Zoom-In Exercise
Card: `8e6c32baa35ff2f2aa1ef544` · Source: Learn Copywriting in 76 Minutes – Harry Dry.docx · Section: 1

Rewrite vague benefits by drilling down a two-column abstract/concrete sheet until you hit a picturable object or scenario.

Applies when: Your product benefits read as adjectives ('effective', 'convenient', 'premium') and you need concrete claims for ads, PDP bullets or category positioning.

- Take a sheet of paper and draw a vertical line down the middle. Write 'abstract' at the top of the left column and 'concrete' at the bottom of the right.
- Write your current vague phrase in the left column (e.g. 'regain fitness', 'pretty people in big cities').
- Ask repeatedly, 'What do I actually mean here?' and rewrite the phrase lower and lower in the right column, converting intangible words into objects, people, places or actions a reader can picture.
- Worked example from the source: 'regain fitness' becomes 'getting people up off the couch to run 5K' — the source notes this is effectively the Couch to 5K naming logic.
- Second worked example: 'worn by pretty people in big cities and old people elsewhere' becomes 'worn by supermodels in London and dads in Ohio' — two picturable people in a funny juxtaposition.
- Use the resulting concrete phrasing directly as product name, headline or PDP bullet candidates, then run the three-question copy test on each.
- Sharpen concrete words further where possible: source critique of a Tesla line suggested preferring 'tougher than an F-150' over 'better truck than an F-150' for shorter, more picturable, more ownable phrasing.
- **Condition:** Drilling down takes real work and multiple rewrites; the source notes 'you can't just like' produce facts — research is required.
- **Condition:** Concrete wording can be less searchable or less category-obvious; you may need one concrete emotional line plus one plain functional line on the same PDP.

#### Sales-Page Template and Section Order
Card: `8ff8c16758242cbca73382e2` · Source: Copywriting 101_ eCommerce copywriting course FOR BEGINNERS.docx · Section: 2

Copy a fixed section order — hero, story, proof, price positioning, objections, FAQs, repeated CTAs — to prevent incoherent pages.

Applies when: Building a sales page, product landing page or long-form collection page and deciding section-by-section structure.

- Write the hero section first: headline, sub-headline and a call to action. Don't name the product unless you're a household brand like mercedes.com or apple.com — a Mercedes-level brand can get away with it, a newer store cannot.
- Write the story section at the length matching your audience's awareness stage.
- Show why they need the product, then show what happens without it.
- Insert testimonials and success stories, then position the price (offer stack or comparison).
- Handle objections ('what if you took my money and I want it back?'), add FAQs, then more testimonials.
- Slip in a call to action or pricing table every two or three content sections so the reader can buy at any point of readiness.
- **Condition:** The source gives the template as a starting point and adapts it — don't treat section order as a rigid law.
- **Condition:** The references to mercedes.com and apple.com are illustrative brand examples, not licensing to name-drop in your copy.

### Retrieval and applicability
Search: `copywriting headline benefits awareness proof concrete readability`
Related domains: avatars, brand, offers, paid-social-creative
Mixed-folder candidate IDs: b86b75e9bce9d133f6fb0bee, 010fe64918f47b6230e2899e, 299de15a096ab2575b0aec6a

- Does this advice fit the product lifecycle, market, audience and requested deliverable?
- Does it require proof, access, budget or assets the brand does not have?
- Does it change a fixed price, offer, policy or other explicit constraint?
- Are platform details or numerical claims current and substantiated?

### Output checks
- Deliver the specified artifact, not general advice about creating it.
- Use supplied brand facts; label hypotheses and missing inputs separately.
- Preserve relevant source conditions; do not copy another business’s proof or results.
- Include an owner, measurement and decision rule when proposing a test.
- Check the output against the requested constraints and owner feedback.

Stop after the requested artifact passes factual and brief checks; allow at most two revision passes, then report the unresolved issue.

## Revise copy using owner feedback
Workflow ID: `ad-copy-deployment.revise-copy`

**Deliverable:** Revised copy and concise change note

### Proposed decision sequence
1. Classify feedback as factual, voice, concept or structure
2. Revise the actual customer-facing text while preserving approved facts
3. Explain meaningful changes briefly and keep analysis out of copy

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### The Psychology of Simplicity: Readable Copy Is Non-Negotiable
Card: `17183d94160ce2f95770a9d7` · Source: Cashvertising.docx · Section: 3

Advertising exists to get people to act, so it must be written to be understood - simple, direct, and readable.

Applies when: Final QA on ad copy, PDP text, email, and any customer-facing copy before it ships.

- Apply the foundational rule: write so people can understand. The source calls this the #1 key to all effective written communication, and warns that an incomprehensible effective message is equivalent to no ad at all.
- Treat clarity as a prerequisite: you may be advertising, but until someone reads and understands, you're just talking to yourself - and you don't need to pay to do that.
- Audit readability yourself before publishing. The source notes there's no magic to it: you write, run the test, examine the score, and edit until it hits the range you want.
- Tighten sentences and reduce sentence length where the copy reads slowly. Long sentences can require fewer words overall but demand more mental processing, which loses readers.
- **Condition:** The source argues this is the foundation for everything else in the book - skip it and other techniques won't rescue the ad.
- **Condition:** Clarity work is not just correct grammar; wordy but grammatically perfect copy can still fail the test.

#### Formatting Rules That Keep Long Copy Readable
Card: `28ee2e3aa4ff11299cd991b6` · Source: 8 Hour Copywriting Course For Beginners.docx · Section: 4

Long centered text blocks, very long lines and repetitive phrasing make copy physically hard to read and cause skips.

Applies when: Formatting a sales page, long-form email, or PDP description section before publishing.

- Left-align body text — source calls centered body copy on a sales page extremely confusing and hard to read.
- Mix short, medium and long lines rather than a wall of long sentences.
- Break the email or page into distinct sections instead of accumulating separate topics in one piece.
- Replace repetitive stock phrasing (repeated 'sleep in, travel, be your own boss' and 'chat-GPT-style' double-dash constructions) with varied, specific language.
- Shorten CTAs to a simple action phrase rather than a long sentence about getting your foot in the door.
- In ecommerce: apply the same left-align and line-length rules to PDP descriptions and landing page body copy, not just emails.
- **Condition:** Source's complaints are editorial judgments from live critiques; legibility problems were inferred partly from line length before reading, so use your own readability checks too.

#### Write a one-paragraph messaging strategy before any copy
Card: `20fa6900506ffc06314306b2` · Source: COPY HACKERS.docx · Section: 1

A short written messaging strategy gives every copy and design decision a rationale so you stop choosing words by what 'sounds good'.

Applies when: You are about to write or rewrite PDP copy, homepage copy or ad creative for a store and need a shared standard for what the copy should do, especially when several people or freelancers touch it.

- Before writing any copy, write down the guiding principles your copy must follow as a short document. Joanna Wiebe's example for Page99Test.com is a single paragraph: copy is 'short, friendly and to the point', assumes visitors want to read book excerpts not marketing copy, keeps words to a minimum, and wherever a screenshot, press logo, button, video demo or icon can be used it should replace copy without sacrificing clarity.
- Pick the principles that matter for your store from the source's list of candidate principles: let copy guide design because good writing is good design; some visitors want to read a lot and some don't, and both are customers; support messages with social proof like testimonials or media reviews; support key concepts with video demonstrations; just because you say it doesn't make it true, so prove it; strive for clarity above cleverness; let the message match the medium at an exact point of need; all visitors can be persuaded to join or upgrade; engage visitors with content, experiences or mobile/app options.
- Treat the document as a living document, not etched in stone: update it as you learn your customers' language and as you add or change products.
- Share the strategy with designers, developers and freelancers so they understand your brand and messaging approach before they produce assets.
- Draft your own version in one sitting without censoring yourself, then edit afterward rather than trying to reach a final version on the first, second or third try.
- **Condition:** The source frames this for startups; a longer or more detailed strategy is not required for it to work.
- **Condition:** The strategy governs copy, not formatting or layout — establish messages before formatting bullets, headlines and buttons.

### Retrieval and applicability
Search: `copywriting clarity specificity voice edit readability`
Related domains: avatars, brand, offers, paid-social-creative
Mixed-folder candidate IDs: 7d460350a38096003d9e2fa5, b86b75e9bce9d133f6fb0bee, 62247a5dc49e3b6106c7f866

- Does this advice fit the product lifecycle, market, audience and requested deliverable?
- Does it require proof, access, budget or assets the brand does not have?
- Does it change a fixed price, offer, policy or other explicit constraint?
- Are platform details or numerical claims current and substantiated?

### Output checks
- Deliver the specified artifact, not general advice about creating it.
- Use supplied brand facts; label hypotheses and missing inputs separately.
- Preserve relevant source conditions; do not copy another business’s proof or results.
- Include an owner, measurement and decision rule when proposing a test.
- Check the output against the requested constraints and owner feedback.

Stop after the requested artifact passes factual and brief checks; allow at most two revision passes, then report the unresolved issue.

## Write copy addressing a buying objection
Workflow ID: `ad-copy-deployment.objection-copy`

**Deliverable:** Objection-led ad copy variants

### Proposed decision sequence
1. Select an evidenced objection that the product can actually address
2. Choose appropriate proof and avoid amplifying unsupported fears
3. Write a clear promise, support and next action without changing the offer

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Show, Don't Tell: Demonstrate Why You're Convinced
Card: `e9741d568a978ac5f209974d` · Source: 8 Hour Copywriting Course For Beginners.docx · Section: 4

Claims create objections while demonstrated personal results create belief, so show your own before-and-after instead of asserting an outcome.

Applies when: Writing product-page proof sections or ad hooks where a headline claim about results would trigger skepticism.

- Identify every sentence in your draft that 'tells' the reader a result ('you can lose 20 lbs in 8 weeks').
- Rewrite it as a first-person demonstration of the same claim ('here's how my arms went from skinny to ripped in 8 weeks').
- Pair the demonstration with visual or numeric proof in the same sentence or block.
- Use the phrase 'in my experience' or 'for me it was' instead of issuing an instruction, so the reader is shown rather than instructed.
- In ecommerce: instead of 'our strips improve sleep,' describe your own tossing-and-turning nights, what changed after using them, and the specific improvements you noticed (waking refreshed, breaking a gym plateau).
- **Condition:** Source gives this as the angle to use roughly 90% of the time in copy — treat that percentage as the presenter's heuristic, not a measured rule.

#### Use Verifiable Evidence to Convert Belief into Purchase
Card: `a9db8de6d903f43da80e956e` · Source: Cashvertising.docx · Section: 3

Evidence - facts, figures, testimonials, endorsements, research, charts - persuades more effectively than claims you made yourself.

Applies when: Writing copy for higher-priced or considered-purchase products where prospects need justification before buying.

- Use the source's operational definition: evidence is 'any factual statement, object, or opinion not created by the source that is used by that source as support' (Reinhard, 1988). Facts, figures, testimonials, endorsements, research, and charts qualify. Your own claims do not.
- Layer evidence on top of emotional appeal. You must provoke emotion to get the prospect excited enough to spend, but especially for costlier products you must supply enough reasoning so they can justify the purchase and satisfy their sense of responsibility.
- Present evidence clearly and simply. Peripheral thinkers - most readers - won't work through dense data; they'll scan, decide, and move on. Colorful charts and graphs, plus quotes from trusted professionals, let them absorb the proof fast.
- Anticipate the source's key point: buyers want to believe your claims (because believing lets them enjoy the benefits), and strong evidence is what lets them give themselves permission.
- **Condition:** The source argues evidence is most effective with important or expensive products where buyers think carefully. Lower-cost impulse goods may rely more on emotion.
- **Condition:** Central-route thinkers will scrutinize and check your evidence - make sure it holds up.

#### Choose Solution-Aware for Mechanism-Led Ads
Card: `79e75a8b36451e7d0b516267` · Source: How To Make Your Meta Ads Scale.docx · Section: 0

When viewers know the category but haven't picked a product, make your unique mechanism the centre of the creative.

Applies when: When advertising to audiences who have tried or researched competitors in your category, or when producing mid-funnel creative after top-of-funnel volume is running.

- Confirm the audience already knows the category exists — e.g., has used whitening strips or worked with marketing agencies before — since you then don't need category education.
- Make the differentiating mechanism visible within the creative, per the source: purple whitening strips vs normal strips, your agency's audit process vs other agencies, a specific formulation or material.
- Consider how the ad sits across stages: the source's whitening-strip video argues most of its education is about which product to choose, not about whether whitening strips exist, which places it at solution aware.
- Use proof and early product introduction once the mechanism lands — in the Nero gym-short example the product appears around nine seconds in, and being 'the only short in the world like this' removes direct comparison.
- Trim category education from the script — it wastes valuable hook time on people who already know the basics.
- **Condition:** Judging which stage a real ad occupies is interpretive; the source notes even he and colleagues argue about the exact placement.
- **Condition:** Mechanism-only framing assumes prior category knowledge and will underperform on unaware cold audiences.

### Retrieval and applicability
Search: `objection belief proof mechanism awareness copy`
Related domains: avatars, brand, offers, paid-social-creative
Mixed-folder candidate IDs: 010fe64918f47b6230e2899e, 4930a1df56a64e44337df968, 5c6cc037d679f4ee76b992d7

- Does this advice fit the product lifecycle, market, audience and requested deliverable?
- Does it require proof, access, budget or assets the brand does not have?
- Does it change a fixed price, offer, policy or other explicit constraint?
- Are platform details or numerical claims current and substantiated?

### Output checks
- Deliver the specified artifact, not general advice about creating it.
- Use supplied brand facts; label hypotheses and missing inputs separately.
- Preserve relevant source conditions; do not copy another business’s proof or results.
- Include an owner, measurement and decision rule when proposing a test.
- Check the output against the requested constraints and owner feedback.

Stop after the requested artifact passes factual and brief checks; allow at most two revision passes, then report the unresolved issue.
