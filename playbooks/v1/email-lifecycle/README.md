# Email Lifecycle — draft playbook

**Status:** source-linked draft; not owner-approved or outcome-tested.

Read [the operating contract](../OPERATING_CONTRACT.md) before using a workflow.

## Inputs
- Consent/segments
- customer events
- existing flows
- deliverability
- offers
- product facts

## Measures
- Contribution
- purchases
- unsubscribes
- complaints

## Foundation candidates
Inferred principle labels do not establish universal applicability. Retain source conditions; empty means no matched labelled principle, not absence of foundational knowledge.

- **Employ retention and account-level setup: where email sits in the 2026 lifecycle** (`e6ffa2358b86e68f9e088680`): Commit to a measured email cadence and a five-flow automated core, then extend with gamification, zero-party-data quizzes and split desktop/mobile experiences.
  Applies when: Roadmapping the lifecycle programme, deciding sending frequency, and prioritising which automations to build first.
  Condition: 3–4 campaigns per week plus flow volume is aggressive for some audiences; the source also tells you to learn whether emails are wanted, so cadence should be validated against engagement and spam complaints.
  Condition: The 72-hour welcome window and day-zero concentration are the source's observations across an agency portfolio, not a guarantee for every offer type.

- **Treat deliverability as a sender reputation score** (`61807f09ea38c7cfb41249af`): Inbox providers rank you like a credit score: good reputation lands in primary, bad lands in spam, mediocre lands in promotions.
  Applies when: When diagnosing why campaigns aren't being seen, or when deciding whether low revenue is a content problem or a placement problem.
  Condition: The credit-score framing is the source's analogy, not an official metric.
  Condition: The source's claim that a clean ESP dashboard means you're fine is a simplification — authentication and domain setup still deserve a direct check.

- **Have the Five Core Flows Plus Win-Back and Sunset in Place** (`b8acdbab97a3a717dea59f37`): Prioritize the essential lifecycle flows the source calls the biggest money-makers: welcome series, site abandon, browse abandon, cart abandon, checkout abandon, post-purchase, win-back, and sunset.
  Applies when: Auditing which automation flows a store still needs, or sequencing which flows to build first.
  Condition: Which flows are 'biggest money-makers' is the presenter's assessment, not a measured benchmark across stores.
  Condition: Build order should consider your data volume — some flows (e.g., back-in-stock) need inventory/restock events to exist.

## Plan lifecycle email flows
Workflow ID: `email-lifecycle.plan-flows`

**Deliverable:** Lifecycle flow specification

### Proposed decision sequence
1. Map lifecycle events and consent eligibility
2. Prioritise flows by customer need and implementation readiness
3. Define triggers, exclusions, message purpose and success measures

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Build the five core SMS flows (welcome + four abandonments + post-purchase)
Card: `3cf40cda910329753dde8a53` · Source: How to Create a SMS Marketing Strategy For $10M Shopify Brands.docx · Section: 0

Every brand should run a welcome flow, site/browse/cart/checkout abandonment, and a post-purchase replenishment or win-back flow.

Applies when: Setting up or auditing the automated (flow) side of an SMS program.

- Welcome flow: triggered when someone joins via the popup (often with a discount). Keep it simple — introduce the brand and drive the discount.
- Four abandonment flows, kept dead simple: site abandoned (browsed site, no product page), browse abandoned (viewed a product page), cart abandoned (added to cart), checkout abandoned (reached checkout).
- Post-purchase / replenishment / win-back flow: bring buyers back after their first order.
- Keep abandonment messages single and simple (see the US compliance card) and split by new vs. returning buyers when you can.
- Treat these basics as the moneymakers: the source reports one brand's core flows producing $517k, with $293k from welcome, $107k cart abandoned, $46k browse abandoned, $20k retention, and $13k site abandoned in a month.
- **Condition:** Revenue figures are a single agency portfolio example, not a benchmark to expect.
- **Condition:** Exact flow structure should be adjusted per brand context.

#### Keep only high-engagement flows during recovery
Card: `e5dfe8e98a4921473d54bb07` · Source: Ecommerce Email Marketing 2025.docx · Section: 12

Pause most automations and lean on welcome, abandon and post-purchase flows, which reliably earn high engagement.

Applies when: Deciding which automations to leave running while rebuilding sender reputation, or which flows to prioritize when you can't build everything at once.

- Turn off all flows except: welcome, browse abandonment, cart abandonment, checkout abandonment and post-purchase.
- Keep the welcome flow because contacts just opted in for a discount and will open the first email delivering it.
- Keep cart and checkout abandonment because the reminder about an item they were already considering earns strong engagement.
- Keep post-purchase because customers want order information.
- Understand why this matters during recovery: every send that gets opens and clicks is a vote of confidence with providers; flows generate those votes without needing new campaign content.
- Re-enable the remaining flows once engagement and placement have recovered.
- **Condition:** This is the source's recommended recovery posture, not a claim that other flows are worthless.
- **Condition:** If a flow's own engagement is weak for your brand, including it dilutes the signal you're trying to send.

#### Have the Five Core Flows Plus Win-Back and Sunset in Place
Card: `b8acdbab97a3a717dea59f37` · Source: _Klaviyo Email Marketing FULL COURSE 2025.docx · Section: 3

Prioritize the essential lifecycle flows the source calls the biggest money-makers: welcome series, site abandon, browse abandon, cart abandon, checkout abandon, post-purchase, win-back, and sunset.

Applies when: Auditing which automation flows a store still needs, or sequencing which flows to build first.

- Confirm the pre-purchase set exists: welcome series, site abandon, browse abandon, cart abandon, checkout abandon.
- Confirm post-purchase and customer win-back exist as post-purchase flows.
- Confirm the sunset flow exists for list hygiene.
- The source singles out the welcome series, cart abandon, and browse abandon as the most important flows to keep optimizing over time — treat them as ongoing optimization targets, not set-and-forget.
- Beyond the core, the source lists optional/extended flows as the possibilities are 'endless': bounceback offer right after purchase, back-in-stock, replacement reminder (e.g., a 30-day consumable prompted at ~day 25), product/data-based cross-sell flows, and a tailored 'highly engaged but never purchased' window-shopper flow.
- **Condition:** Which flows are 'biggest money-makers' is the presenter's assessment, not a measured benchmark across stores.
- **Condition:** Build order should consider your data volume — some flows (e.g., back-in-stock) need inventory/restock events to exist.

### Retrieval and applicability
Search: `customer journey welcome abandoned cart post purchase flow`
Related domains: post-purchase, ad-copy-deployment, measurement
Mixed-folder candidate IDs: 36f24e817a8e9586163eb93a, d7082f8c3c813a3e82f869da, 1667a4459343b6e160a8233c

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

## Write an ecommerce email campaign
Workflow ID: `email-lifecycle.write-campaign`

**Deliverable:** Finished email copy and segment brief

### Proposed decision sequence
1. Select a relevant segment and one campaign purpose
2. Write subject, preheader, body and CTA using approved facts
3. Check offer consistency, exclusions and brand voice

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Split subject line and preview text to stay readable on mobile
Card: `589fc4bc3d9b3135629f70f8` · Source: _Klaviyo Email Marketing FULL COURSE 2025.docx · Section: 4

Short subject lines plus a complementary preview text raise the chance the whole first impression is read on a small screen.

Applies when: Writing campaign subject lines and preheaders for a store's promotions or content sends.

- Treat the subject line's only job as getting the open; it must create curiosity or intrigue and stand out in a crowded inbox.
- Treat the preview text as a second subject line — many brands skip or waste it by focusing only on the subject line.
- Follow up on the subject line's promise in the preview text and tease the content without lying; a high open rate from a broken promise leads to spam complaints or unsubscribes.
- Avoid full sentences: use a few words in the subject line and a few in the preview text. Because most opens happen on mobile, a long subject line is cut off — split one long idea between the two fields.
- Do not promise in subject/preview what the email doesn't deliver.
- **Condition:** The segment cuts off after listing the email's headline; exact character limits are not specified in the source.
- **Condition:** Open rates are not the only goal — delivering the promise protects sender reputation.

#### Upload a finished image-design email into an ESP as stacked images
Card: `400d584b7e15f2a88817da35` · Source: How to Design High Converting Ecommerce Emails In Figma.docx · Section: 0

Set up a campaign, strip the template, upload compressed slices in order, remove padding, add links, then test and send.

Applies when: Publishing an image-based email built in Figma into Omnisend, Klaviyo or a similar platform.

- Create the campaign in the ESP, entering the subject line and preheader text (the presenter uses 'Last chance for 20% off' with preheader 'Open for your last gift opportunity').
- Open any template to get a canvas, then delete the template blocks so you start from an empty email.
- Add image elements one by one and upload your compressed slices, stacking them in the exact order they appear in the design.
- Select each image block and remove image padding plus any frame side padding so the stacked slices align edge to edge and look like one continuous design.
- Assign the destination link for each image — one link per image — and add short alt text describing the image.
- Preview and send a test email to your own address, checking that the unsubscribe link is present (the ESP added one automatically in the walkthrough) and that links and rendering are correct.
- Choose recipients — all subscribers or a specific segment with exclusions — review, then send.
- **Condition:** Omnisend and other ESP interfaces change frequently; verify current campaign, padding and image-upload controls.
- **Condition:** Sending entirely image-based emails means text-only recipients see alt text, so keep alt text meaningful.

#### Clear and concise email copy: short and sweet, one takeaway
Card: `99679e755f67e645ee972b4e` · Source: Ecommerce Email Marketing 2025.docx · Section: 8

Keep emails to one to two scrolls and one clear takeaway; assume readers are overwhelmed and forget multiple points.

Applies when: Writing campaign or flow copy that risks cramming several benefits or messages into one send.

- Keep the email to roughly 1-2 phone scrolls maximum; source's guidance is shorter is better because only a few seconds of attention are available.
- Choose ONE takeaway per email and build the headline around it — e.g. a matcha email solely about 'enhances the benefits of caffeine', or a hair-loss email solely about growth potential.
- Ask yourself before sending: is there one clear thing the customer can take away? If the email tries to give 3+ takeaways, assume readers remember none.
- Split a benefit-stuffed email into a series: instead of one email listing estimator, graphs, alerts, multi-cook view, etc., dedicate a whole email to each feature one at a time.
- Cut implied information. On a welcome email, skip telling subscribers they get exclusive offers/insider access (they already know from the opt-in) and let the discount code sit in the clear space you save.
- Every sentence should move the reader toward a purchase; delete fluff that only fills space.
- **Condition:** Some emails (e.g. a flowchart or comparison email) are intentionally longer because the format itself is the engagement — length alone isn't the failure, unclear/multi-message copy is.

### Retrieval and applicability
Search: `email copy subject preheader offer benefit clarity`
Related domains: post-purchase, ad-copy-deployment, measurement
Mixed-folder candidate IDs: 7d460350a38096003d9e2fa5, 313c009481176a9875134da4, 3e457e257de62912678cab8e

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

## Audit email sending health
Workflow ID: `email-lifecycle.audit-deliverability`

**Deliverable:** Deliverability audit and correction plan

### Proposed decision sequence
1. Review authentication and available complaint/bounce evidence
2. Inspect consent, suppressions and engagement segments
3. Propose staged corrections and verify current provider requirements

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Treat deliverability as a sender reputation score
Card: `61807f09ea38c7cfb41249af` · Source: Ecommerce Email Marketing 2025.docx · Section: 12

Inbox providers rank you like a credit score: good reputation lands in primary, bad lands in spam, mediocre lands in promotions.

Applies when: When diagnosing why campaigns aren't being seen, or when deciding whether low revenue is a content problem or a placement problem.

- Frame deliverability as your domain/IP 'credit score' — the question is whether you land in primary, promotions or spam.
- Understand the provider's incentive: inbox providers only surface emails users want so users keep using the platform; they watch engagement as the signal.
- Use open and click engagement as the practical proxy: if few people open or click, providers push you toward promotions or spam, which further reduces visibility — a self-reinforcing cycle.
- Check the technical layer first: the source says if your ESP (e.g., Klaviyo) shows no warning at the top of the homepage about domain setup, assume technical requirements are already in place.
- If technicals are fine, split the cause into two: either your emails are weak, or your sender reputation is poor and you are being filtered.
- **Condition:** The credit-score framing is the source's analogy, not an official metric.
- **Condition:** The source's claim that a clean ESP dashboard means you're fine is a simplification — authentication and domain setup still deserve a direct check.

#### Maintain sender reputation with bounce, spam and engagement thresholds
Card: `6d8587217a67915fe64068e6` · Source: 2026 Klaviyo Email Marketing Full Course (3+ Hours).docx · Section: 1

Treat sender reputation like a credit score and monitor the three inputs — bounce rate, spam complaints and engagement — against the source's thresholds.

Applies when: Ongoing deliverability monitoring, or when opens collapse and you need to diagnose reputation damage.

- Understand the model: reputation is history-based and hard to rebuild once damaged; a good reputation gets primary inbox placement, a bad one gets spam or promotions tab.
- Keep bounce rate under 1%. Bounces come from invalid addresses — e.g. a fake email submitted through a pop-up form still triggering the welcome or abandoned-cart flow. Suppress hard-bouncing addresses and consider preventing obviously fake form entries.
- Keep spam complaint rate below 0.3%, and ideally below 0.1%, to stay inside Gmail and Yahoo's stricter 2024+ requirements. Locate these rates in your account reporting and review on a regular cadence.
- Maximise positive engagement signals: opens, clicks and especially replies tell inbox providers people want to hear from you. Low opens and low clicks act as negative signals.
- Send at a consistent cadence — the source cites an example of two campaigns a week plus flows sending daily — because erratic sending (long silence then a burst) is treated as a negative signal.
- Fix the root cause before re-sending: low opens usually means wrong audience (see 180-day cleaning and engagement segments), not a subject-line problem.
- **Condition:** Thresholds (0.3% complaint, 0.1% ideal, 1% bounce) are the source's targets and align with stated Gmail/Yahoo expectations; Google's published requirements should be checked for current limits.
- **Condition:** Reputation damage is slow to reverse, so prevention, not remediation, is the practical strategy.

#### Deliverability Hygiene: Authentication, Engagement Tiers and List Cleaning
Card: `4933eedd5bb2a42ce6ed6980` · Source: Klaviyo email.docx · Section: 1

Implement SPF, DKIM and DMARC, segment by engagement recency, and suppress long-inactive subscribers to protect inbox placement.

Applies when: Setting up or auditing sending infrastructure and list health, especially before scaling campaign volume.

- Implement the technical authentication trio — SPF, DKIM and DMARC — on your sending domain so mailbox providers can verify you.
- Segment by engagement recency using activity windows; the source names 14-day, 30-day, 60-day and 90-day active tiers as the segmentation structure.
- Use those tiers to differentiate sending: mail the most recently engaged tiers most often and reduce frequency or exclude the least engaged tiers.
- Clean the list by suppressing profiles that have been inactive past 180 days — the source's stated list-cleaning benchmark.
- Monitor inbox placement and sender reputation, particularly as AI-driven inbox curation changes how mail is sorted and surfaced.
- Re-check authentication records and suppression rules after any change of sending domain, ESP or marketing platform.
- **Condition:** The 180-day suppression threshold and the 14/30/60/90-day windows are the source's heuristics, not calculations derived from your data — adjust for your purchase cycle and list size.
- **Condition:** Suppressing inactive profiles reduces list size and can reduce short-term revenue; the source frames it as necessary for placement.
- **Condition:** Authentication setup depends on your DNS provider and ESP interface, both of which change — verify current configuration steps.

### Retrieval and applicability
Search: `deliverability sender reputation authentication engagement`
Related domains: post-purchase, ad-copy-deployment, measurement
Mixed-folder candidate IDs: 1e164e5e7ed121f171ed7bbf, deb34829023625f9d15c451e, 2e93f14127165a325bea6753

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
