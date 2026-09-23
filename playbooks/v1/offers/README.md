# Offers — draft playbook

**Status:** source-linked draft; not owner-approved or outcome-tested.

Read [the operating contract](../OPERATING_CONTRACT.md) before using a workflow.

## Inputs
- Product prices
- costs
- margins
- inventory
- approved policies
- fixed-offer constraints

## Measures
- Contribution per visitor
- conversion
- AOV
- refunds

## Foundation candidates
Inferred principle labels do not establish universal applicability. Retain source conditions; empty means no matched labelled principle, not absence of foundational knowledge.

- **Maintain Offer Congruence From Ad Through Post-Purchase** (`511c3a0c4cf9e30365b7b86c`): Keep price, contents, incentives, guarantee, and deadline consistent across every customer touchpoint so shoppers do not discover conflicting terms after clicking or buying.
  Applies when: Launching or changing a promotion, bundle, bonus, guarantee, or pricing structure across paid acquisition, storefront, checkout, and lifecycle email.
  Condition: Congruence is baseline operational hygiene rather than differentiation by itself.
  Condition: Evergreen landing pages, cached ad creative, and automated lifecycle flows are common sources of stale terms; verify the current platform interfaces and publishing status.

- **Define the offer before choosing a mechanic** (`5a6c2fe3c2836fcbe3473011`): An offer is the total proposition before purchase—positioning, price architecture, value mechanic, risk reversal and urgency—not just a discount, and picking mechanics starts by defining all five variables together.
  Applies when: Planning a promotion or rebuilding a product page proposition and unsure whether to cut price or change something else
  Condition: The five-variable framing is the source's model; other offer frameworks exist, but this one forces margin and risk reversal into the same decision.
  Condition: Congruence across ad, page, checkout and email is stated as a baseline requirement — mismatched or expired offers are treated as a broken offer, not a creative issue.

- **Gate Offer Changes With Contribution Margin** (`c8b36a7d028ee03d06b6855a`): Approve discounts, bundles, bonuses, guarantees, and shipping incentives only after evaluating their effect on net contribution, not conversion or revenue alone.
  Applies when: Reviewing a proposed ecommerce offer change before it reaches paid traffic, email subscribers, or the storefront.
  Condition: Some acquisition offers intentionally accept lower first-order margin; that is a strategic decision that requires evidence rather than an accidental outcome.
  Condition: Lifetime-value assumptions do not justify indefinite losses unless cohort behavior validates them.

## Design a viable product offer
Workflow ID: `offers.design-offer`

**Deliverable:** Offer specification and economics comparison

### Proposed decision sequence
1. Diagnose perceived value and buying friction using customer evidence
2. Compare permitted bundle or guarantee options against contribution and fulfilment
3. Select a testable offer with transparent terms and real proof

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Use the Value Equation to Diagnose a Product Offer
Card: `110b031911f002a0f181f07f` · Source: $100M Offers_ How To Make Offers So Good People Feel Stupid Saying No.docx · Section: 0

Increase a product offer’s perceived value by improving the desired outcome and confidence while reducing wait time and customer effort.

Applies when: Designing a product bundle, subscription, or product-page promise that shoppers currently compare mainly by price.

- Assess the offer through four variables: Dream Outcome multiplied by Perceived Likelihood of Achievement, divided by Time Delay multiplied by Effort and Sacrifice.
- For the dream outcome, state the end benefit the product helps deliver rather than only its specifications. For example, a cookware set may promise simpler weeknight meals, provided that claim is supportable.
- Raise perceived likelihood with concrete product proof: compatible-use guidance, customer reviews, demonstrations, quality details, credible guarantees, and precise claims.
- Reduce time delay with inventory visibility, realistic delivery timing, immediate digital access where applicable, or a product configuration that helps customers start sooner.
- Reduce effort and sacrifice through preselected kits, clear variant guidance, simple setup instructions, replenishment options, and fewer decisions at checkout.
- Score all four levers before adding a discount. Repair the weakest credible lever, then evaluate conversion and contribution margin.
- **Condition:** Perceived value is subjective; validate the diagnosis through customer questions, reviews, behavior, and tests rather than internal assumptions.
- **Condition:** Do not make outcome claims that the product, fulfillment, or evidence cannot support.

#### Strengthen Offers With the Four-Part Value Equation
Card: `4cc6038f44bf712243890a61` · Source: How To Create Winning Offers In Ecom.docx · Section: 0

Improve an offer beyond discount structure by raising perceived value across dream outcome, likelihood of achievement, time delay, and effort/sacrifice.

Applies when: An offer is already functional but you want more perceived value without discounting deeper.

- Dream outcome: align the site and ad with the strongest desire the customer holds, not a bland feature claim — e.g. framing around feeling attractive again rather than simply 'look slimmer'.
- Perceived likelihood of achievement: add proof that the outcome is achievable — UGC and unboxing videos, reviews, ingredient breakdowns, guarantees, and demonstration for the actual use case (e.g. parents asking 'will this work for my kid?').
- Time delay: shorten the gap between purchase and benefit — faster shipping options, delivery deadlines (why Amazon pushes 'get it before Christmas'), and fewer intermediate steps.
- Effort and sacrifice: reduce the work and risk required — try-before-you-buy, guarantees, and buy-now-pay-later options such as Shop Pay, Affirm or Afterpay; contrast a convenience product against the effort of diet and exercise.
- Apply these across the whole funnel, from the ad to the landing page, so the claim and the on-site offer reinforce each other.
- **Condition:** The four-factor framing is attributed in the source to Hormozi's value equation; the source says it has reviewed many offers, which is an opinion claim, not measured evidence.
- **Condition:** Guarantees and BNPL integrations carry real operational and financial cost — assess them against margin, not just conversion.

#### Apply the value equation to purchase conversion, not lead conversion
Card: `0f5c6cd39ab04eb263b9921e` · Source: Applying $100M Offers to E-Commerce_ I'm Pissed.docx · Section: 0

The Value Equation is presented as the general mechanism behind purchasing decisions — value must be perceived in excess of price — and is argued to apply to physical products as well as services.

Applies when: Deciding whether to translate a services-origin framework (Hormozi's $100M Offers) into a DTC or physical-product business.

- Treat the four variables as the universal layer: a buyer must want the delivered outcome, believe they can get it, get it fast, and expend little effort or sacrifice.
- Translate each variable into physical-product mechanics rather than copying the service examples: reviews and demos for likelihood, shipping speed for time delay, one-click rails for effort, outcome naming for the dream outcome.
- Treat scarcity, urgency, guarantees, bonuses, and naming as enhancers layered on top of the four variables to shift the value-price ratio further.
- Recognize that the specific vehicle differs by category — services show a practitioner demonstrating a skill, physical products show the item in use and what happens after checkout.
- Use this as the argument for charging more than a bare-listing competitor: the source's claim is that checking these boxes makes buyers willing to pay higher prices, not just buy more often.
- **Condition:** This is the source's position, argued against a podcast comment that the framework does not apply to ecommerce; it is a framework argument, not a test result.
- **Condition:** Service-business and B2B examples from the book are out of scope here; only the transferable logic is retained.

### Retrieval and applicability
Search: `bundle value equation guarantee offer economics`
Related domains: finance-and-accounting, avatars, landing-pages
Mixed-folder candidate IDs: e345aac91cf443d84d08c371, afe614ed1856dd695e2a1bcd, 96733f0bc647c804fff4e803

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

## Improve presentation of a fixed offer
Workflow ID: `offers.audit-fixed-offer`

**Deliverable:** Fixed-offer messaging corrections

### Proposed decision sequence
1. Record price, inclusions and terms that cannot change
2. Find misunderstandings across ad, page and checkout
3. Improve explanation and proof without silently adding discounts or promises

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Maintain Offer Congruence From Ad Through Post-Purchase
Card: `511c3a0c4cf9e30365b7b86c` · Source: $100M Offers_ How To Make Offers So Good People Feel Stupid Saying No.docx · Section: 0

Keep price, contents, incentives, guarantee, and deadline consistent across every customer touchpoint so shoppers do not discover conflicting terms after clicking or buying.

Applies when: Launching or changing a promotion, bundle, bonus, guarantee, or pricing structure across paid acquisition, storefront, checkout, and lifecycle email.

- Create a single offer record containing product or variant, price, contents, bundle savings method, bonus, shipping treatment, guarantee, eligibility, inventory limit, and deadline.
- Use that record to check the acquisition ad, landing page or PDP, cart drawer, checkout copy, confirmation page, transactional emails, and scheduled campaign flows.
- Remove expired offer banners, old creative, discontinued bonuses, stale product descriptions, and automated emails that still mention previous terms.
- Check that urgency and scarcity claims agree. A page cannot credibly say both “unlimited availability” and “only 20 left” for the same item without a clear distinction.
- Assign an owner and a launch/change checklist so merchandising, paid media, email, and support update together.
- After deployment, place a test order and inspect the customer-facing experience end to end, including any discount logic and confirmation messaging.
- **Condition:** Congruence is baseline operational hygiene rather than differentiation by itself.
- **Condition:** Evergreen landing pages, cached ad creative, and automated lifecycle flows are common sources of stale terms; verify the current platform interfaces and publishing status.

#### Treat the Offer as Extending From Ad to Site
Card: `0a570cacb9523e316e31710e` · Source: How To Create Winning Offers In Ecom.docx · Section: 0

The offer is the total package — product, price, bonus, claims, guarantees and conditions — across every touchpoint, not just the on-site buy-X-get-Y.

Applies when: Auditing whether ad, landing page and checkout present one coherent value proposition.

- Define the offer as everything the customer receives in total and the value they perceive at purchase, including product, price, bonuses, claims, guarantees and conditions.
- Map the offer across touchpoints: ad hook, landing-page claims, product page, guarantee and risk reversal, and checkout/payment options.
- Check that the same dream outcome and proof appear in the ad and on the page, so interest generated by the ad isn't lost at the buy decision.
- Include non-discount components in the offer — free gifts, subscription incentives, proof assets — as alternatives to bundle discounting.
- Test full-funnel variations where feasible, since a stronger ad-level offer can improve conversion even when the on-site mechanic is unchanged.
- **Condition:** The source's claim that a strong offer can take a store from unprofitable to profitable is anecdotal from other merchants; no verified unit-margin data is offered.
- **Condition:** Ad copy construction and campaign deployment are outside this module's scope.

#### Use Value Stacking and Price Framing Without Hiding the Total
Card: `e3d657e18bdc9092842339df` · Source: How to Create Irresistible Offers The Easiest Way on Earth to Make Your Marketing Generate More Leads, Orders, and Sales (1).docx · Section: 1

Bonuses, installment options, and per-day framing can make a legitimate offer easier to evaluate, but they must not conceal total price or weaken pricing clarity.

Applies when: Structuring a product bundle, subscription, prepaid replenishment plan, or higher-priced cart offer where shoppers need help understanding total value and payment terms.

- Establish the baseline offer first: clear product contents, total price, shipping or recurring terms, and a standard return or guarantee policy where applicable.
- Stack distinct value against the asking price by showing the core product plus meaningful included items, services, guides, or access. Each item should be real, understandable, and relevant to the buyer.
- If offering installments or recurring billing, state the payment amount, cadence, number of payments where applicable, and total commitment in the same decision area. The source uses payment fractioning to reduce perceived lump-sum burden, but the total must remain prominent.
- Use per-day or per-use framing only as a secondary context after the actual price. It can help shoppers compare the cost to the duration of use, especially for annual plans or replenishment programs.
- Where a bonus has an assigned value, validate that value through a genuine standalone sale or otherwise avoid presenting it as a retail price.
- Test the offer structure against a clear-price control and judge results by completed purchases, margin, refunds, and subscription retention rather than clicks alone.
- **Condition:** The source classifies these as advanced, growth-side mechanics, not substitutes for a clear core offer.
- **Condition:** Per-day and installment language can mislead if total cost, renewal, financing, or cancellation terms are obscured; verify applicable consumer-protection requirements.

### Retrieval and applicability
Search: `offer congruence clarity objection guarantee`
Related domains: finance-and-accounting, avatars, landing-pages
Mixed-folder candidate IDs: 414f3d559f4e716ff8ec26ab, b60bbbefb2a73bd7e30e8f6e, 42a366d5ecc75b44e1c8300b

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

## Plan a bounded promotion
Workflow ID: `offers.test-promotion`

**Deliverable:** Promotion brief with contribution guardrails

### Proposed decision sequence
1. Define the business objective and available stock
2. Model contribution and cannibalisation risks for permitted incentives
3. Specify genuine timing, measurement and stop conditions

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Scarcity and Urgency Implementation
Card: `483d4914fae6b0e24de4d7af` · Source: I Studied Every Ecommerce Offer So You Don’t Have To.docx · Section: 0

Use live stock states, time-gated deals, and drop models to create honest urgency.

Applies when: Planning promotions, limited releases, or on-site urgency mechanics

- Display live SKU inventory counts so shoppers see remaining stock in real time.
- Run time-gated lightning deals with a clear start and end window.
- Use drop-model constraints: a limited release with a defined quantity or window.
- Keep the scarcity transparent: the source puts 'transparent stock states' in the baseline category, meaning the mechanic only works when it is true.
- Place scarcity mechanics where the purchase decision happens (PDP, cart, or promotion landing page).
- **Condition:** Source classifies drop-urgency as a growth tactic, while simply showing transparent stock is baseline.
- **Condition:** Fabricated scarcity risks trust and is not what the source describes.

#### Use real deadlines and credible inventory scarcity
Card: `ea94a39e0ec67857cc94e9f3` · Source: How to Create Irresistible Offers The Easiest Way on Earth to Make Your Marketing Generate More Leads, Orders, and Sales (1).docx · Section: 3

Urgency works when a sale end date or stock limit is operationally true, communicated consistently, and actually enforced.

Applies when: Planning a seasonal promotion, product drop, limited-edition launch, preorder, email campaign, cart promotion, or low-stock PDP message.

- Choose the appropriate constraint: a genuine promotion end date, a response window, a limited quantity, capacity for a handmade or customized run, or an event-like enrollment limit.
- Use a specific calendar deadline only when campaign timing is fully controlled. The source distinguishes this from generic response windows used in direct mail; in ecommerce, a live date and time is usually preferable when the storefront and emails can be updated reliably.
- Give a truthful reason for scarcity when one exists: manufacturing capacity, limited-edition production, remaining stock, preorder allocation, personalization slots, or event seats. The source stresses that a downloadable file cannot credibly be described as limited to a fixed number of copies.
- Use reminder communication near a real expiry and stop the offer when promised. Confirm inventory synchronization across storefront, ads, email, and customer support before launch.
- **Condition:** Do not reset or extend supposedly final deadlines without an honest explanation; repeated false urgency trains customers to wait.
- **Condition:** The source advises legal review for time-limited promotional copy. Verify current consumer-protection and advertising requirements in relevant markets.

#### Audit an ecommerce offer before scaling traffic
Card: `65ce1e16b1cee00d5d241695` · Source: $100M Offers_ How To Make Offers So Good People Feel Stupid Saying No.docx · Section: 5

Before buying more traffic, verify that the product offer is differentiated, economically viable, clearly valued, and supported by scarcity, urgency, bonuses, risk reversal, and a resonant name where appropriate.

Applies when: Preparing a new product launch, bundle, promotional landing page, or acquisition campaign for additional paid traffic.

- Check whether the offer is commoditized. Improve differentiation through product selection, bundle composition, use-case positioning, customer segment, or a distinctive buying experience rather than relying only on lower price.
- Confirm market fit and niche focus: identify a specific shopper and the job, occasion, or problem the offer addresses. The source’s principle is that narrower relevance can support stronger positioning.
- Verify price and unit economics before scaling: include product cost, fulfillment, payment fees, discounts, returns, customer support, and acquisition cost assumptions.
- Build the value stack: explain the primary product, complementary components, bonuses, and delivery experience in terms of why each helps the buyer.
- Use real scarcity and urgency, such as limited inventory, a genuine campaign deadline, or a seasonal cutoff. Do not manufacture constraints.
- Add a credible guarantee or clearly explain a justified no-return policy, then give the offer a shopper-facing name that fits the intended audience.
- Treat this as an offer readiness review, not a promise of revenue. The source describes a strong, high-margin, de-commoditized offer as a business foundation; profitable acquisition remains a separate discipline.
- **Condition:** Scarcity, urgency, and guarantees must be truthful and operationally supportable.
- **Condition:** A polished offer cannot compensate for poor product quality, inaccurate claims, or unprofitable acquisition economics.

### Retrieval and applicability
Search: `promotion urgency scarcity contribution discount`
Related domains: finance-and-accounting, avatars, landing-pages
Mixed-folder candidate IDs: 743b6f53913cf3cf0674f4ad, fdc00c6aa447fc96327d375d, 11bcf453bac4bf67d9aa91dd

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
