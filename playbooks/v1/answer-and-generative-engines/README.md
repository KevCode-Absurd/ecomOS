# Answer And Generative Engines — draft playbook

**Status:** source-linked draft; not owner-approved or outcome-tested.

Read [the operating contract](../OPERATING_CONTRACT.md) before using a workflow.

## Inputs
- Product facts
- public pages
- target questions
- evidence
- observed answer visibility

## Measures
- Answer accuracy
- qualified referrals
- repeated visibility observations

## Foundation candidates
Inferred principle labels do not establish universal applicability. Retain source conditions; empty means no matched labelled principle, not absence of foundational knowledge.

- **Compete in AI citation by niching down the prompt, then expanding** (`1d269cb7fde523345240c2ba`): You cannot win broad AI queries like 'best CRM', so start with narrow, defensible prompt phrasings, build topical authority, then attempt broader terms.
  Applies when: Targeting AI-assistant answers in a crowded product category where broad 'best X' queries are dominated by incumbents.
  Condition: This is the source's stated approach; they explicitly say they lack a proven formula for citation lifetime or selection logic.
  Condition: No guaranteed ranking — success depends on category and competition.

- **Validate structured product and brand facts alongside visible copy** (`618db29e20911b3adccbf119`): Structured data spells out your business, products and social profiles in a machine-readable format AI crawlers read reliably.
  Applies when: Adding or auditing structured data on an ecommerce site to improve how LLMs interpret brand and product information.
  Condition: Schema improves interpretability but does not guarantee recommendation; the presenter treats it as one of several inputs.
  Condition: Exact schema types beyond Organization are in the linked checklist, not enumerated in the video.
  Condition: Google does not require special AI schema. Validate applicable product search features separately from any citation hypothesis.

- **Match Citation Strategy to Your Business Model** (`7a7c5e12d8bcf1543cfe845a`): B2B, commerce and marketplace queries pull from different citation sources and require different measurement approaches.
  Applies when: Choosing which review sites, publications or platforms to target for a B2B, DTC or marketplace store.
  Condition: The named publications are Smith's observations of what currently appears, not fixed rules; recheck current citations.

## Create answer-oriented product content
Workflow ID: `answer-and-generative-engines.answer-content`

**Deliverable:** Answer-content brief

### Proposed decision sequence
1. Select real product questions and supported answers
2. Structure clear answers and evidence on relevant pages
3. Specify structured data only where it matches visible facts

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Using and limiting schema markup for AEO
Card: `ccbc5be4692ffe2c9ec171a5` · Source: AI SEO Course for Beginners_ Complete AEO Tutorial.docx · Section: 2

Schema markup is low-risk but unproven for AI citation; add standard types as a good habit without over-investing for AEO alone.

Applies when: Deciding how much time to spend on structured data when setting up new store pages.

- For ecommerce, inspect accurate Product and Offer data on PDPs, with Organization, BreadcrumbList or Article where appropriate to page purpose.
- Recognize that evidence linking schema directly to AI citation is mixed — there's no confirmed data it improves AI citation odds.
- Keep accurate schema that supports current search features; correct inaccurate or conflicting markup rather than retaining it blindly.
- If setting up a new page, add the appropriate schema types as a good habit that makes content easier for any system to understand.
- Avoid spending significant time on schema specifically for AEO; deprioritize it relative to robots.txt, content quality, and rendering.
- **Condition:** The source is explicit that AEO benefit is unconfirmed; this is a 'doesn't hurt' recommendation, not a proven tactic.

#### Match Citation Strategy to Your Business Model
Card: `7a7c5e12d8bcf1543cfe845a` · Source: The ultimate guide to AEO_ How to get ChatGPT to recommend your product _ Ethan Smith.docx · Section: 1

B2B, commerce and marketplace queries pull from different citation sources and require different measurement approaches.

Applies when: Choosing which review sites, publications or platforms to target for a B2B, DTC or marketplace store.

- Identify the citation set for your model: Smith sees TechRadar appearing heavily for B2B questions; Glamour and Cosmopolitan for commerce; Eater, Yelp and TripAdvisor for marketplaces and local.
- Build your target list from the actual citations the engines return for your questions, not from generic top-domain lists.
- Measurement differs: many B2B answers have nothing clickable, so last-touch referral traffic undercounts impact — you need answer tracking plus a post-conversion 'how did you hear about us' question.
- Commerce does have clickable shoppable cards, so last-touch referral traffic gives a reasonable read of conversions.
- For commerce cards, rich snippet schema and the number of reviews matter for appearing in the carousel.
- B2B purchase cycles involve roughly dozens of touch points — nobody commits to large software from one search.
- **Condition:** The named publications are Smith's observations of what currently appears, not fixed rules; recheck current citations.

#### Run a commercial-page checklist: intent, one keyword, schema, design, specifics
Card: `ea6702f063e43c682e987e10` · Source: The Complete AI SEO Course 2026.docx · Section: 1

Five checks determine whether a product or collection page will perform, starting with search-intent match and including structured data and evidence.

Applies when: Finalising a new category, product or collection page before publishing.

- Intent match: confirm the page answers the searcher's intent — a transactional query needs a page where the product can be bought or requested, not an article about the topic.
- One main keyword per page: assign a single primary target and use secondary/related terms naturally through subheadings and body copy rather than spreading several primaries across one page.
- Schema: add appropriate structured data (service/product schema as applicable) so search engines understand exactly what the page contains. The source says you can rank without it but you're giving up an advantage; SEO plugins often insert it, but validate the output rather than assuming.
- Conversion-friendly design and evidence: prefer real photos of the actual work/product over stock imagery where possible, be specific about prices, include reviews (ideally reviews mentioning that specific product/service), and add a how-it-works section.
- Body structure: use additional H2/H3s for related keywords, and include a short FAQ of the most-asked questions for that specific offering — the source advises keeping commercial-page FAQs to no more than about five so the page stays transactional.
- Use the first fold as the priority: pass the 2-second rule (what/where/next action), keep the headline plain, keep H1 exact, and place a primary CTA above the fold. If roughly 90% of these boxes are ticked, the source considers the page in good shape.
- **Condition:** The source deliberately avoids prescribing a word count — length should follow what the page needs, not a target.
- **Condition:** Blog/informational content should be kept off commercial pages beyond a short FAQ to avoid diluting transactional focus.
- **Condition:** Structured-data support and plugin behavior change; verify with a current validator.

### Retrieval and applicability
Search: `answer first conversational query citations evidence schema`
Related domains: search, brand, measurement
Mixed-folder candidate IDs: cf409d4e384dafeabda6b4fb, feb29848807a941be501368e, 239a4c7c70190b2325db780a

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

## Audit AI answer visibility
Workflow ID: `answer-and-generative-engines.visibility-audit`

**Deliverable:** Visibility observation log and corrections

### Proposed decision sequence
1. Define repeatable prompts, engines and observation dates
2. Record actual citations and factual errors across repeated observations
3. Prioritise useful content corrections without promising inclusion

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Prompt trackers: understand their limits before trusting AI visibility data
Card: `28b2634c43eb8c2b7c9613b8` · Source: Generative Engine Optimization_ Is It Safe and How to Do It the Right Way.docx · Section: 1

Automated AI prompt trackers can report inflated or meaningless visibility when answers vary run-to-run or the model never searched the web.

Applies when: Reviewing an AI visibility report from a tool, agency or in-house dashboard to decide whether the store is actually being recommended.

- Recognize how these tools work: they capture screenshots of a tracked prompt's answer inside ChatGPT or another assistant and upload them for comparison.
- Know the failure mode: if the assistant does not trigger a web search, there are no citations in the answer, so the screen contains no useful evidence of visibility.
- Treat citation counts with suspicion. The source argues citations are easy to inflate — one URL can be cited for an infinite number of branded term variations (e.g. 'how to get rid of mold brand name'), so 'we increased citations' does not mean 'we increased visibility'.
- Recognize that answers vary dynamically; a single tracked prompt is not a stable measurement.
- When reviewing reports, ask which prompts are commercially meaningful to the store, whether web search actually fired, and whether the reported change maps to revenue rather than mention counts.
- **Condition:** The source's view is that the whole citation-measurement system is of questionable value and partly vendor-driven; treat dashboard metrics as directional at best.
- **Condition:** Trackers and assistants change interfaces and behavior — verify the current mechanics before relying on any single metric.

#### Treat GEO as an ongoing monitoring and adaptation loop
Card: `d94670809e775a86f01cad8b` · Source: 7 Essential Tactics for Mastering Generative Engine Optimization (GEO).docx · Section: 0

Generative engine optimization is not one-time work; you must watch how AI platforms evolve and keep refining content.

Applies when: Setting a recurring workstream for AI search visibility alongside SEO analytics and rank tracking.

- Set up recurring monitoring of how AI platforms (ChatGPT, Perplexity, Gemini, Google AI Overviews) structure and cite responses to your target queries.
- Track visibility and engagement benchmarks across those platforms and review changes over time.
- Stay current on AI-driven search trends and refine your strategy rather than locking in a fixed playbook.
- Fold this into existing SEO analytics cadence — the source frames GEO as adapting SEO tracking frameworks, not replacing them.
- When a platform's answer format or citation behavior shifts, re-check whether your target pages still match it.
- **Condition:** Platform interfaces, features and availability change without notice — verify current tooling before relying on any specific monitoring method.
- **Condition:** GEO visibility metrics are newer and less standardized than classic rank tracking.

#### Track AI visibility with Search Console and Bing AI performance
Card: `4df3dc92ffaf5f8c4b520df4` · Source: The Complete AI SEO Course 2026.docx · Section: 2

Use clicks, impressions, average position, and queries from Search Console, and Bing's AI performance tab for citations.

Applies when: Monitoring whether your store is surfacing in AI overviews and chat results, and deciding what to do next month.

- In Google Search Console's Performance tab, track total clicks and impressions — impressions typically rise first, then clicks; also watch average position across all ranking keywords.
- Expect lower clicks generally as AI search engines absorb some traffic; this is described as the new norm, not automatically an error.
- Keep Google Search Console performance separate from dedicated AI citation reporting; verify what each current report actually measures before labeling it AI visibility.
- Read total citations, average pages cited, and the queries you're cited for; growth in citations and average cited pages is good.
- Optionally use a paid AI-visibility tool for additional coverage: a performance tab (citations by engine), a brand tracker for instant checks, and prompt/keyword tracking.
- **Condition:** The source's visibility-tool data skews to US and English queries; that biases the picture for other markets.
- **Condition:** There is no target number for how fast citations should rise; the source says judge month-to-month improvement, not an absolute benchmark.
- **Condition:** Do not infer that every impression, click or rank movement in Search Console came from an AI feature.

### Retrieval and applicability
Search: `unbranded prompts visibility monitoring answer accuracy`
Related domains: search, brand, measurement
Mixed-folder candidate IDs: 7d460350a38096003d9e2fa5, 9d66422ea27f4f60461e750a, a39261c57a5ed84a91fa92a1

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

## Improve product and brand fact consistency
Workflow ID: `answer-and-generative-engines.entity-consistency`

**Deliverable:** Public fact-consistency plan

### Proposed decision sequence
1. Compare important facts across owned public pages
2. Resolve contradictions using approved brand evidence
3. Specify consistent updates and later checks

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Validate structured product and brand facts alongside visible copy
Card: `618db29e20911b3adccbf119` · Source: The Ultimate AI Visibility Checklist (AEO_GEO for 2026).docx · Section: 0

Structured data spells out your business, products and social profiles in a machine-readable format AI crawlers read reliably.

Applies when: Adding or auditing structured data on an ecommerce site to improve how LLMs interpret brand and product information.

- Structured data can clarify store facts; it is not a prerequisite for all AI systems and does not prevent hallucination.
- Add Organization schema to the homepage including founding date, description, and links to social profiles; this signals that you are a proper, reputable business.
- Use a schema generator tool to select a schema type, fill in the relevant fields, and copy the generated code onto the appropriate page.
- Apply the other schema types recommended in the source checklist to their matching page types (e.g. product-related types on product pages) rather than dumping all schema on one template.
- Link your YouTube channel and social profiles from your website and include them in schema markup alongside the rest of your brand data.
- Validate the markup after deployment so errors do not silently defeat the purpose.
- **Condition:** Schema improves interpretability but does not guarantee recommendation; the presenter treats it as one of several inputs.
- **Condition:** Exact schema types beyond Organization are in the linked checklist, not enumerated in the video.
- **Condition:** Google does not require special AI schema. Validate applicable product search features separately from any citation hypothesis.

#### Using and limiting schema markup for AEO
Card: `ccbc5be4692ffe2c9ec171a5` · Source: AI SEO Course for Beginners_ Complete AEO Tutorial.docx · Section: 2

Schema markup is low-risk but unproven for AI citation; add standard types as a good habit without over-investing for AEO alone.

Applies when: Deciding how much time to spend on structured data when setting up new store pages.

- For ecommerce, inspect accurate Product and Offer data on PDPs, with Organization, BreadcrumbList or Article where appropriate to page purpose.
- Recognize that evidence linking schema directly to AI citation is mixed — there's no confirmed data it improves AI citation odds.
- Keep accurate schema that supports current search features; correct inaccurate or conflicting markup rather than retaining it blindly.
- If setting up a new page, add the appropriate schema types as a good habit that makes content easier for any system to understand.
- Avoid spending significant time on schema specifically for AEO; deprioritize it relative to robots.txt, content quality, and rendering.
- **Condition:** The source is explicit that AEO benefit is unconfirmed; this is a 'doesn't hurt' recommendation, not a proven tactic.

#### Structure and schema-model pages for AI parsing
Card: `4ddb9e4eaae67ec08d76bdc3` · Source: 7 Essential Tactics for Mastering Generative Engine Optimization (GEO).docx · Section: 0

Well-structured pages with clear headings, lists, and schema markup are easier for AI engines to extract and reuse.

Applies when: Formatting PDPs, category pages, or guides, or when adding structured data for schedules, reviews, or pricing.

- Break content into clear sections with descriptive headings. The source's fitness-studio example: 'Benefits of Pilates', 'Beginner Pilates exercises', 'Advanced Pilates movements'.
- Use bullet points and short, concise paragraphs instead of dense blocks.
- Apply structured data and schema markup to surface the facts AI engines need — the source names class schedules, reviews, and pricing as examples.
- Translate that for ecommerce: mark up product price, availability, reviews/ratings, FAQs, and specifications so engines can lift clear answers.
- **Condition:** Schema types and platform support change; verify current supported markup before implementing.
- **Condition:** Schema improves machine readability but does not substitute for a direct answer in the body content.

### Retrieval and applicability
Search: `entity product facts schema reviews authority citations`
Related domains: search, brand, measurement
Mixed-folder candidate IDs: b4498bb660aa14c0efe067d1, efb0633227f5bba7a422760d, d14808598a83b96c68d5025c

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
